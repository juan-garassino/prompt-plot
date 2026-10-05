"""Plate jobs — a multi-pen plate plotted on Leo in one long, resumable session.

One engine, two seats: ``promptplot plot plate`` (keypress for swaps and
re-zeros) and the gallery server's ``action: "plate"`` (``/plotter/continue``).
Both build a :class:`PlatePlan`, a :class:`PlateJob` and run a
:class:`PlateJobRunner`. The spec is ``studio/PLOT_JOBS.md``.

The sequence the runner owns::

    connect (opening the port resets Grbl — it zeroes wherever the head sits)
    [resume only] pen up · WAIT awaiting_rezero — "is the head on the corner?"
    frame trace, pen up (first act of a fresh job)
    for each layer:
        [pen changes] pen up · park (0,0) · WAIT awaiting_swap
        pen up · rapid to the batch's first drawn point
        for each batch of ``batch_strokes`` strokes:
            stream_chunk(enforce_pen_state=True)
            save the job file                     <- the resume point
            [pause asked]    park · state paused · disconnect
            [rezero_every]   park · WAIT awaiting_rezero · pen-up approach
    park (0,0) · done

How Leo is not saturated
------------------------
Nothing here writes to the port. Every line goes through
``SerialPlotter.send_command`` (``promptplot/plotter.py``), which holds
``_io_lock`` across write + ``readline`` and returns only when Grbl answers:
send-one-line, wait-for-``ok``. At most ONE line (< 60 bytes) is ever in
flight, so Grbl's 128-byte RX buffer cannot overflow, and Grbl withholds the
``ok`` until the line fits its planner — the controller paces us, not the
other way round. The heartbeat is off (``enable_heartbeat=False``), so the
ack loop is the only reader of the port; HTTP threads never touch the plotter,
they only set ``threading.Event``s. Batches are therefore not flow control:
they are the stop / drift-check / resume granularity, and they always end on a
stroke boundary (``slice_stroke_range``). A failed or timed-out ack ABORTS the
job (pen up, park) instead of carrying on, because a lost ``ok`` shifts every
later ack by one line and a lost ``M5`` drags the pen.
"""

from __future__ import annotations

import asyncio
import contextlib
import hashlib
import json
import logging
import math
import os
import re
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, Iterator, List, Optional, Sequence

from .config import PaperConfig
from .engine import PenState
from .models import GCodeCommand, GCodeProgram
from .orchestrate import (
    _first_drawn_point,
    slice_stroke_range,
    split_color_layers,
    stream_chunk,
    stroke_spans,
    trace_frame_full,
    validate_chunk,
)

logger = logging.getLogger(__name__)

JOB_SCHEMA_VERSION = "1.0.0"
DEFAULT_JOB_DIR = Path.home() / ".promptplot" / "plot_jobs"
JOB_ID_RE = re.compile(r"^j-\d{8}-\d{6}(-\d+)?$")
MAX_JOB_LOG = 300

# ---- Leo's time model ------------------------------------------------------
# Same constants as scripts/gallery_index.py (LEO_*), which prices PRINT.md;
# that script cannot import the package, so they are mirrored, not shared.
LEO_DRAW_MM_MIN = 600.0     # feed for a G1 that carries none (memory: F600 streak-free, 2026-09-13)
LEO_TRAVEL_MM_MIN = 2000.0  # G0 rapid rate as Leo actually moves (memory: F2000 travels)
LEO_DWELL_S = 2.0           # per pen cycle when a file has NO G4 dwells (1.0 s each side)
SWAP_S = 90.0               # a human pen swap — estimate, not measured
REZERO_S = 20.0             # a human origin check — estimate, not measured
# Leo drags ink at fast feeds and short dwells (memory: slow-feeds-long-pen-dwells):
DEFAULT_MAX_FEED = 500      # cap every G1 feed; 0 streams the file's feeds as-is
DEFAULT_MIN_DWELL = 1.0     # floor every G4; 0 streams the file's dwells as-is
DEFAULT_BATCH_STROKES = 400
DEFAULT_REZERO_EVERY = 2000
PARK_XY = (0.0, 0.0)        # EXACTLY (0,0): reconnecting re-zeroes wherever the head sits


class JobState(str, Enum):
    PENDING = "pending"
    FRAMING = "framing"
    AWAITING_SWAP = "awaiting_swap"
    STREAMING = "streaming"
    AWAITING_REZERO = "awaiting_rezero"
    PAUSED = "paused"
    STOPPED = "stopped"
    DONE = "done"
    ERROR = "error"


class PlotRefused(ValueError):
    """The job must not start (or continue): nothing unsafe has been sent."""


class JobStopped(Exception):
    """Stop requested — raised between two commands, never mid-command."""


class CommandFailed(RuntimeError):
    """The controller answered error/alarm, or the ack never came."""


class PlotterBusy(RuntimeError):
    """Another job (this process or another one) owns the plotter."""


# ---------------------------------------------------------------------------
# Paper, preparation, bounds, time model
# ---------------------------------------------------------------------------

def paper_from_spec(spec: str, margin: float) -> PaperConfig:
    """``a5:landscape`` / ``a4`` / ``170x240`` → PaperConfig (landscape default)."""
    size, orient = spec.split(":", 1) if ":" in spec else (spec, "landscape")
    return PaperConfig.from_size(size, orientation=orient, margin=margin)


def prepare_commands(
    cmds: Sequence[GCodeCommand], max_feed: float = 0, min_dwell: float = 0
) -> List[GCodeCommand]:
    """Leo-safe copy of ``cmds``, same length and order (stroke indices hold).

    * every draw carries an EXPLICIT feed — Grbl resets on reconnect, so a
      resumed batch cannot lean on a modal ``F`` set in an earlier batch;
    * ``max_feed`` caps it; ``min_dwell`` floors every ``G4`` (the loader parses
      ``G4 P0.2`` as ``P0``, so without a floor file dwells can vanish).
    """
    out: List[GCodeCommand] = []
    feed: Optional[float] = None
    for c in cmds:
        upd: Dict[str, Any] = {}
        if c.command in ("G1", "G2", "G3"):
            if c.f is not None:
                feed = c.f
            f = feed if feed is not None else LEO_DRAW_MM_MIN
            if max_feed and f > max_feed:
                f = max_feed
            f = int(round(f))
            if c.f != f:
                upd["f"] = f
        elif c.command == "G4" and min_dwell and (c.p is None or c.p < min_dwell):
            upd["p"] = float(min_dwell)
        out.append(c.model_copy(update=upd) if upd else c)
    return out


def check_bounds(cmds: Sequence[GCodeCommand], paper: PaperConfig) -> List[str]:
    """Coordinates the paper cannot take. ``G1`` must stay in the drawable area
    (``stream_chunk`` inks every ``G1``), ``G0`` on the sheet — the same rule as
    ``validate_chunk``, whose pen-fix notes are ignored because the stream's
    pen guardrail fixes those."""
    _fixed, warnings, _pen = validate_chunk(list(cmds), PenState(), paper)
    return [w for w in warnings if "clamped" in w]


def stroke_seconds(cmds: Sequence[GCodeCommand]) -> List[float]:
    """Modelled seconds per stroke, over the same spans ``slice_stroke_range``
    cuts (stroke k = its positioning travel up to the next stroke's travel)."""
    m3 = stroke_spans(list(cmds))
    if not m3:
        return []
    starts = [max(0, i - 1) for i in m3]
    has_dwells = any(c.command == "G4" for c in cmds)
    secs = [0.0] * len(m3)
    k = 0
    x = y = 0.0
    feed = LEO_DRAW_MM_MIN
    for i, c in enumerate(cmds):
        while k + 1 < len(starts) and i >= starts[k + 1]:
            k += 1
        if c.command in ("G0", "G1", "G2", "G3"):
            nx = c.x if c.x is not None else x
            ny = c.y if c.y is not None else y
            d = math.hypot(nx - x, ny - y)
            if c.command == "G0":
                secs[k] += d / LEO_TRAVEL_MM_MIN * 60.0
            else:
                if c.f:
                    feed = float(c.f)
                secs[k] += d / max(feed, 1.0) * 60.0
            x, y = nx, ny
        elif c.command == "G4" and c.p:
            secs[k] += float(c.p)
        elif c.command == "M3" and not has_dwells:
            secs[k] += LEO_DWELL_S
    return secs


# ---------------------------------------------------------------------------
# The plan: which runs of which pens, prepared and priced
# ---------------------------------------------------------------------------

@dataclass
class PlateLayer:
    run: int                       # index into split_color_layers(program)
    color: int
    commands: List[GCodeCommand]
    seconds: List[float]           # modelled seconds per stroke

    @property
    def strokes(self) -> int:
        return len(self.seconds)


@dataclass
class PlatePlan:
    paper: PaperConfig
    layers: List[PlateLayer]

    @property
    def total_strokes(self) -> int:
        return sum(L.strokes for L in self.layers)

    def swaps(self) -> int:
        """Pen loads the job will wait for (the first pen counts)."""
        n, prev = 0, None
        for L in self.layers:
            if L.color != prev:
                n += 1
            prev = L.color
        return n

    def remaining_seconds(self, unit: int, stroke: int, rezero_every: int = 0,
                          swap_pending: bool = False) -> float:
        """Modelled seconds from ``(unit, stroke)`` to the end, human waits included."""
        s = 0.0
        strokes = 0
        swaps = 1 if swap_pending else 0
        for ui in range(unit, len(self.layers)):
            L = self.layers[ui]
            lo = stroke if ui == unit else 0
            s += sum(L.seconds[lo:])
            strokes += max(0, L.strokes - lo)
            if ui > unit and L.color != self.layers[ui - 1].color:
                swaps += 1
        rezeros = strokes // rezero_every if rezero_every else 0
        return s + swaps * SWAP_S + rezeros * REZERO_S


def build_plan(
    program: GCodeProgram,
    paper: PaperConfig,
    *,
    layers: Optional[Sequence[int]] = None,
    max_feed: float = DEFAULT_MAX_FEED,
    min_dwell: float = DEFAULT_MIN_DWELL,
) -> PlatePlan:
    """Split ``program`` into colour runs, keep the requested pens, prepare and
    bounds-check EVERY layer up front — a plate that would leave the sheet on
    its fourth pen is refused before the first one inks.

    Order: the file's run order, or the order of ``layers`` (colour indices;
    all runs of one colour in file order). Empty runs are dropped."""
    prepared = GCodeProgram(
        commands=prepare_commands(program.commands, max_feed, min_dwell),
        metadata=dict(program.metadata or {}),
    )
    runs = split_color_layers(prepared)
    if layers is None:
        order = list(range(len(runs)))
    else:
        present = {c for c, _ in runs}
        missing = [c for c in layers if c not in present]
        if missing:
            raise PlotRefused(f"no layer with colour {missing} (file has {sorted(present)})")
        order = [i for c in layers for i, (rc, _) in enumerate(runs) if rc == c]

    out: List[PlateLayer] = []
    problems: List[str] = []
    for i in order:
        color, cmds = runs[i]
        if not stroke_spans(cmds):
            continue
        bad = check_bounds(cmds, paper)
        if bad:
            problems.append(f"colour {color}: {len(bad)} out of bounds ({'; '.join(bad[:2])})")
        out.append(PlateLayer(run=i, color=color, commands=cmds, seconds=stroke_seconds(cmds)))
    if problems:
        raise PlotRefused("out of bounds for "
                          f"{paper.width:g}x{paper.height:g}: " + " | ".join(problems))
    if not out:
        raise PlotRefused("nothing to draw: no strokes in the selected layers")
    return PlatePlan(paper=paper, layers=out)


# ---------------------------------------------------------------------------
# The job record (the file IS the resume point)
# ---------------------------------------------------------------------------

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()


@dataclass
class PlateJob:
    id: str
    target: str                     # what the operator asked for (gallery-relative in the server)
    path: str                       # absolute gcode path
    sha256: str                     # resume refuses if the file changed underneath
    paper: str
    margin: float
    layers: Optional[List[int]] = None
    batch_strokes: int = DEFAULT_BATCH_STROKES
    rezero_every: int = DEFAULT_REZERO_EVERY
    max_feed: float = DEFAULT_MAX_FEED
    min_dwell: float = DEFAULT_MIN_DWELL
    state: str = JobState.PENDING.value
    waiting_for: Optional[str] = None      # "swap" | "rezero" | None
    wait_seq: int = 0                       # bumps per wait: a continue names the wait it answers
    message: str = ""
    units: List[Dict[str, int]] = field(default_factory=list)
    cursor: Dict[str, int] = field(default_factory=lambda: {"unit": 0, "stroke": 0, "batch": 0})
    progress: Dict[str, List[int]] = field(default_factory=lambda: {"layer": [0, 0], "overall": [0, 0]})
    eta_min: Optional[float] = None
    est_total_min: Optional[float] = None
    pace: float = 1.0                       # measured / modelled stream time
    strokes_since_rezero: int = 0
    framed: bool = False                    # this job traced the frame for its paper
    errors: List[str] = field(default_factory=list)
    log: List[str] = field(default_factory=list)
    created: float = field(default_factory=time.time)
    updated: float = field(default_factory=time.time)
    action: str = "plate"
    schema: str = JOB_SCHEMA_VERSION

    @property
    def resumable(self) -> bool:
        return self.state != JobState.DONE.value

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["resumable"] = self.resumable
        return d

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "PlateJob":
        known = set(cls.__dataclass_fields__)  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in d.items() if k in known})


def new_job(
    path: Path,
    *,
    target: Optional[str] = None,
    paper: str,
    margin: float,
    layers: Optional[Sequence[int]] = None,
    batch_strokes: int = DEFAULT_BATCH_STROKES,
    rezero_every: int = DEFAULT_REZERO_EVERY,
    max_feed: float = DEFAULT_MAX_FEED,
    min_dwell: float = DEFAULT_MIN_DWELL,
    job_id: Optional[str] = None,
) -> PlateJob:
    if batch_strokes < 0 or rezero_every < 0 or max_feed < 0 or min_dwell < 0:
        raise PlotRefused("batch_strokes, rezero_every, max_feed and min_dwell must be >= 0")
    path = Path(path).resolve()
    return PlateJob(
        id=job_id or time.strftime("j-%Y%m%d-%H%M%S"),
        target=target or str(path), path=str(path), sha256=file_sha256(path),
        paper=paper, margin=float(margin),
        layers=[int(c) for c in layers] if layers is not None else None,
        batch_strokes=int(batch_strokes), rezero_every=int(rezero_every),
        max_feed=float(max_feed), min_dwell=float(min_dwell),
    )


def plan_for_job(job: PlateJob) -> PlatePlan:
    """Load the job's gcode and rebuild its plan (also the resume path)."""
    from .config import get_config
    from .pipeline import FilePipeline

    path = Path(job.path)
    if not path.is_file():
        raise PlotRefused(f"gcode is gone: {job.path}")
    if file_sha256(path) != job.sha256:
        raise PlotRefused("the gcode changed since the job started — stroke indices "
                          "no longer mean the same strokes; start a new job")
    program = FilePipeline(get_config()).load_gcode_file(str(path))
    return build_plan(program, paper_from_spec(job.paper, job.margin), layers=job.layers,
                      max_feed=job.max_feed, min_dwell=job.min_dwell)


class JobStore:
    """``~/.promptplot/plot_jobs/<id>.json``, written atomically."""

    def __init__(self, root: Optional[Path] = None) -> None:
        self.root = Path(root) if root is not None else DEFAULT_JOB_DIR

    def path(self, job_id: str) -> Path:
        if not JOB_ID_RE.match(str(job_id)):
            raise ValueError(f"not a job id: {job_id!r}")
        return self.root / f"{job_id}.json"

    def unique_id(self, job_id: str) -> str:
        cand, n = job_id, 1
        while self.path(cand).exists():
            n += 1
            cand = f"{job_id}-{n}"
        return cand

    def save(self, job: PlateJob) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        job.updated = time.time()
        p = self.path(job.id)
        tmp = p.with_suffix(".json.tmp")
        with open(tmp, "w") as f:
            json.dump(job.to_dict(), f, indent=1)
        os.replace(tmp, p)
        return p

    def load(self, job_id: str) -> PlateJob:
        p = self.path(job_id)
        if not p.is_file():
            raise PlotRefused(f"no such job: {job_id}")
        with open(p) as f:
            return PlateJob.from_dict(json.load(f))

    def list(self, limit: int = 20) -> List[Dict[str, Any]]:
        if not self.root.is_dir():
            return []
        rows = []
        for p in self.root.glob("j-*.json"):
            try:
                with open(p) as f:
                    d = json.load(f)
            except (OSError, ValueError):
                continue
            rows.append({k: d.get(k) for k in (
                "id", "target", "paper", "state", "cursor", "progress", "eta_min",
                "units", "updated", "resumable", "message")})
        rows.sort(key=lambda r: r.get("updated") or 0, reverse=True)
        return rows[:limit]

    @contextlib.contextmanager
    def port_lock(self) -> Iterator[None]:
        """One job owns the plotter across processes (terminal vs server)."""
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            import fcntl
        except ImportError:  # not POSIX: the in-process one-job rule still holds
            yield
            return
        fh = open(self.root / "plotter.lock", "w")
        try:
            try:
                fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise PlotterBusy("another plot job owns the plotter "
                                  f"(lock {self.root / 'plotter.lock'})") from None
            try:
                yield
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)
        finally:
            fh.close()


# ---------------------------------------------------------------------------
# Operator controls
# ---------------------------------------------------------------------------

class JobControl:
    """Thread-safe knobs: HTTP threads (or a signal handler) set them, the
    job's event loop polls them. Nothing here touches the serial port."""

    poll_s = 0.2

    def __init__(self) -> None:
        self._continue = threading.Event()
        self._pause = threading.Event()
        self._stop = threading.Event()

    def request_continue(self) -> None:
        self._continue.set()

    def request_pause(self) -> None:
        self._pause.set()

    def request_stop(self) -> None:
        self._stop.set()

    @property
    def pause_requested(self) -> bool:
        return self._pause.is_set()

    @property
    def stop_requested(self) -> bool:
        return self._stop.is_set()

    def reset(self) -> None:
        for e in (self._continue, self._pause, self._stop):
            e.clear()

    def arm(self) -> None:
        """Forget any continue sent before this wait began."""
        self._continue.clear()

    async def wait_for_operator(self, kind: str, message: str) -> str:
        """Block until continue / pause / stop. Returns which."""
        while True:
            if self._stop.is_set():
                return "stop"
            if self._pause.is_set():
                return "pause"
            if self._continue.is_set():
                self._continue.clear()
                return "continue"
            await asyncio.sleep(self.poll_s)


class AutoContinueControl(JobControl):
    """Rehearsal operator (``--dry-run``): every wait continues at once and is
    recorded, so a dry run walks exactly the sequence the machine would."""

    def __init__(self) -> None:
        super().__init__()
        self.waits: List[str] = []

    async def wait_for_operator(self, kind: str, message: str) -> str:
        self.waits.append(kind)
        if self._stop.is_set():
            return "stop"
        return "pause" if self._pause.is_set() else "continue"


class KeypressControl(JobControl):
    """Terminal operator: Enter continues, ``p`` pauses (resumable), ``s`` stops."""

    def __init__(self, prompt: Callable[[str], None] = print) -> None:
        super().__init__()
        self._print = prompt

    async def wait_for_operator(self, kind: str, message: str) -> str:
        self._print(f"\n  >> {message}\n     Enter = continue · p = pause (resumable) · s = stop")
        answer: List[str] = []

        def _read() -> None:
            try:
                answer.append(input("  > ").strip().lower())
            except (EOFError, KeyboardInterrupt):
                answer.append("s")

        threading.Thread(target=_read, daemon=True).start()  # daemon: never blocks exit
        while not answer:
            if self._stop.is_set():
                return "stop"
            if self._pause.is_set():
                return "pause"
            await asyncio.sleep(self.poll_s)
        a = answer[0]
        return "stop" if a.startswith("s") else "pause" if a.startswith("p") else "continue"


# ---------------------------------------------------------------------------
# The guarded plotter: every command still goes through plotter.send_command
# ---------------------------------------------------------------------------

class _GuardedPlotter:
    """Wraps a plotter for ``stream_chunk``: checks stop between commands,
    raises on the first failed ack, tracks pen state and strokes started."""

    def __init__(self, inner: Any, control: JobControl) -> None:
        self.inner = inner
        self.control = control
        self.pen_down = False
        self.m3_sent = 0

    async def send_command(self, gcode: str) -> bool:
        if self.control.stop_requested:
            raise JobStopped()
        return await self.send(gcode)

    async def send(self, gcode: str) -> bool:
        """Send without the stop check (park / pen-up after a stop)."""
        ok = await self.inner.send_command(gcode)
        word = gcode.split(None, 1)[0].upper() if gcode.strip() else ""
        if not ok:
            status = getattr(self.inner, "status", None)
            detail = getattr(status, "last_error", None) or getattr(status, "last_response", None)
            raise CommandFailed(f"{gcode!r} not acknowledged ({detail or 'timeout / no ok'})")
        if word == "M3":
            self.pen_down = True
            self.m3_sent += 1
        elif word == "M5":
            self.pen_down = False
        return ok


# ---------------------------------------------------------------------------
# The runner
# ---------------------------------------------------------------------------

Connect = Callable[[], Awaitable[Any]]


class PlateJobRunner:
    """Runs one :class:`PlateJob` against one plotter connection.

    ``trace_frame`` — first act is the pen-up frame trace (a fresh job always).
    ``framed`` — a frame for this paper is already known good (server: traced
    in this process; terminal resume: this job traced it). Without one of the
    two the runner refuses to ink.
    ``resuming`` — the port was just reopened on a job with progress: wait for
    the operator to confirm the origin before anything moves.
    """

    def __init__(
        self,
        job: PlateJob,
        plan: PlatePlan,
        *,
        connect: Connect,
        control: Optional[JobControl] = None,
        store: Optional[JobStore] = None,
        trace_frame: bool = True,
        framed: bool = False,
        resuming: bool = False,
        on_update: Optional[Callable[[Dict[str, Any]], None]] = None,
        on_framed: Optional[Callable[[], None]] = None,
        say: Optional[Callable[[str], None]] = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.job = job
        self.plan = plan
        self.connect = connect
        self.control = control or JobControl()
        self.store = store
        self.trace_frame = trace_frame
        self.framed = framed
        self.resuming = resuming
        self.on_update = on_update
        self.on_framed = on_framed
        self._say_cb = say
        self.clock = clock
        self._model_streamed = 0.0
        self._wall_streamed = 0.0
        self.guard: Optional[_GuardedPlotter] = None
        job.units = [{"run": L.run, "color": L.color, "strokes": L.strokes} for L in plan.layers]
        job.progress["overall"][1] = plan.total_strokes
        job.est_total_min = round(plan.remaining_seconds(
            0, 0, job.rezero_every) / 60.0, 1)
        self._refresh_progress()

    # ---- bookkeeping ----

    def say(self, msg: str) -> None:
        line = f"{time.strftime('%H:%M:%S')}  {msg}"
        self.job.log.append(line)
        del self.job.log[:-MAX_JOB_LOG]
        logger.info("plate %s: %s", self.job.id, msg)
        if self._say_cb:
            self._say_cb(msg)

    def _refresh_progress(self, swap_pending: bool = False) -> None:
        j, plan = self.job, self.plan
        ui, s = j.cursor["unit"], j.cursor["stroke"]
        done = sum(L.strokes for L in plan.layers[:ui]) + (s if ui < len(plan.layers) else 0)
        j.progress["overall"] = [done, plan.total_strokes]
        if ui < len(plan.layers):
            j.progress["layer"] = [s, plan.layers[ui].strokes]
        rem = plan.remaining_seconds(ui, s, j.rezero_every, swap_pending)
        j.eta_min = round(rem * j.pace / 60.0, 1)

    def _set(self, state: JobState, message: Optional[str] = None, save: bool = True) -> None:
        self.job.state = state.value
        if message is not None:
            self.job.message = message
            self.say(message)
        if save:
            self._save()
        else:
            self._emit()

    def _save(self) -> None:
        if self.store is not None:
            self.store.save(self.job)
        self._emit()

    def _emit(self) -> None:
        if self.on_update:
            self.on_update(self.job.to_dict())

    # ---- machine moves (all through the guard → plotter.send_command) ----

    async def _pen_up(self) -> None:
        await self.guard.send("M5")
        await self.guard.send(f"G4 P{max(self.job.min_dwell, 0.3):g}")

    async def _park(self) -> None:
        """Pen up, (0,0), and a dwell — Grbl acks a G4 only once the planner
        has drained, so the wait that follows starts with the head home."""
        await self._pen_up()
        await self.guard.send(f"G0 X{PARK_XY[0]:g} Y{PARK_XY[1]:g}")
        await self.guard.send("G4 P0.5")

    async def _approach(self, chunk: List[GCodeCommand]) -> None:
        """Pen-UP rapid to the chunk's first drawn point: never drag from home."""
        fp = _first_drawn_point(chunk)
        await self._pen_up()
        if fp is not None:
            await self.guard.send(f"G0 X{fp[0]:.3f} Y{fp[1]:.3f}")
            await self.guard.send(f"G4 P{max(self.job.min_dwell, 0.3):g}")

    async def _safe_park(self) -> None:
        """After a stop or failure: lift (retried — a lost M5 drags), then park."""
        if self.guard is None:
            return
        for _ in range(3):
            try:
                await self.guard.send("M5")
                break
            except Exception:  # noqa: BLE001 — keep trying to lift
                logger.warning("pen-up retry after failure")
        try:
            await self.guard.send(f"G4 P{max(self.job.min_dwell, 0.3):g}")
            await self.guard.send(f"G0 X{PARK_XY[0]:g} Y{PARK_XY[1]:g}")
        except Exception:  # noqa: BLE001
            self.say("could not park after the failure — check the head by hand")

    async def _wait(self, kind: str, state: JobState, message: str) -> str:
        self.control.arm()
        self.job.wait_seq += 1
        self.job.waiting_for = kind
        self._set(state, message)
        decision = await self.control.wait_for_operator(kind, message)
        self.job.waiting_for = None
        self.say(f"{kind}: {decision}")
        return decision

    def _halt(self, decision: str) -> PlateJob:
        if decision == "pause":
            self._set(JobState.PAUSED, f"paused at layer {self.job.cursor['unit'] + 1}, "
                                       f"stroke {self.job.cursor['stroke']} — resume with "
                                       f"{self.job.id}")
        else:
            self._set(JobState.STOPPED, f"stopped at layer {self.job.cursor['unit'] + 1}, "
                                        f"stroke {self.job.cursor['stroke']} — resumable "
                                        f"({self.job.id})")
        return self.job

    # ---- the sequence ----

    async def run(self) -> PlateJob:
        if not (self.trace_frame or self.framed):
            self.job.errors.append("no frame")
            self._set(JobState.ERROR, "refused: trace the frame first — no pen-up frame "
                                      f"has been traced for {self.job.paper}")
            return self.job
        if self.store is not None:
            try:
                with self.store.port_lock():
                    return await self._run_connected()
            except PlotterBusy as e:
                self.job.errors.append(str(e))
                self._set(JobState.ERROR, f"refused: {e}")
                return self.job
        return await self._run_connected()

    async def _run_connected(self) -> PlateJob:
        j = self.job
        try:
            plotter = await self.connect()
        except Exception as e:  # noqa: BLE001 — report, do not crash the server
            j.errors.append(f"connect: {e}")
            self._set(JobState.ERROR, f"could not connect: {e}")
            return j
        self.guard = _GuardedPlotter(plotter, self.control)
        self._in_batch_from: Optional[int] = None
        self._m3_at_batch = 0
        try:
            return await self._sequence()
        except JobStopped:
            self._rewind_partial()
            await self._safe_park()
            return self._halt("stop")
        except CommandFailed as e:
            self._rewind_partial()
            j.errors.append(str(e))
            await self._safe_park()
            self._set(JobState.ERROR, f"ABORTED — {e}. Pen lifted, parked. The job resumes "
                                      f"at layer {j.cursor['unit'] + 1} stroke {j.cursor['stroke']}")
            return j
        except PlotRefused as e:
            j.errors.append(str(e))
            await self._safe_park()
            self._set(JobState.ERROR, f"refused: {e}")
            return j
        except Exception as e:  # noqa: BLE001 — a hardware failure must not kill the caller
            logger.exception("plate job failed")
            j.errors.append(f"{type(e).__name__}: {e}")
            await self._safe_park()
            self._set(JobState.ERROR, f"{type(e).__name__}: {e}")
            return j
        finally:
            with contextlib.suppress(Exception):
                await plotter.disconnect()

    def _rewind_partial(self) -> None:
        """A batch cut short: move the cursor to the stroke that was being drawn
        (redrawn on resume — one overdrawn stroke beats a half-missing one)."""
        g, j = self.guard, self.job
        if g is None or self._in_batch_from is None:
            return
        started = g.m3_sent - self._m3_at_batch
        done = started - 1 if g.pen_down else started
        j.cursor["stroke"] = self._in_batch_from + max(0, done)
        self.say(f"cut mid-batch — cursor rewound to stroke {j.cursor['stroke']}")
        self._in_batch_from = None
        self._refresh_progress()

    async def _sequence(self) -> PlateJob:
        j, plan, g = self.job, self.plan, self.guard
        W, H = plan.paper.width, plan.paper.height
        n = len(plan.layers)
        first_ui = j.cursor["unit"]

        if self.resuming:
            await g.send("M5")
            L = plan.layers[min(first_ui, n - 1)]
            d = await self._wait("rezero", JobState.AWAITING_REZERO,
                                 "RESUME: reopening the port re-zeroed Grbl where the head sits. "
                                 f"Check the head is on the paper corner (0,0) and pen #{L.color} "
                                 f"is loaded, then continue (layer {first_ui + 1}/{n}, "
                                 f"stroke {j.cursor['stroke']}/{L.strokes})")
            if d != "continue":
                return self._halt(d)
            j.strokes_since_rezero = 0

        if self.trace_frame:
            self._set(JobState.FRAMING, f"tracing {W:g}x{H:g} margin {j.margin:g} — PEN UP")
            await trace_frame_full(g, W, H, j.margin)
            j.framed = True
            if self.on_framed:
                self.on_framed()
            self.say("frame traced")

        for ui in range(first_ui, n):
            L = plan.layers[ui]
            j.cursor["unit"] = ui
            start = j.cursor["stroke"] if ui == first_ui else 0
            if ui != first_ui:
                j.cursor["stroke"] = 0
                j.cursor["batch"] = 0
            # Each layer is re-checked right before it streams, not just at plan time.
            bad = check_bounds(L.commands, plan.paper)
            if bad:
                raise PlotRefused(f"colour {L.color} out of bounds: {'; '.join(bad[:3])}")

            new_pen = (ui == first_ui and not self.resuming) or (
                ui > first_ui and L.color != plan.layers[ui - 1].color)
            if new_pen:
                await self._park()
                self._refresh_progress(swap_pending=True)
                d = await self._wait("swap", JobState.AWAITING_SWAP,
                                     f"load pen #{L.color} — layer {ui + 1}/{n}, "
                                     f"{L.strokes} strokes; head parked at (0,0)")
                if d != "continue":
                    return self._halt(d)
                j.strokes_since_rezero = 0

            approach = True
            s = start
            while s < L.strokes:
                e = L.strokes - 1
                if j.batch_strokes:
                    e = min(e, s + j.batch_strokes - 1)
                if j.rezero_every:
                    e = min(e, s + max(1, j.rezero_every - j.strokes_since_rezero) - 1)
                chunk = slice_stroke_range(L.commands, s, e)
                if approach:
                    await self._approach(chunk)
                    approach = False
                self._set(JobState.STREAMING,
                          f"colour {L.color}: strokes {s}..{e} of {L.strokes}", save=False)
                self._in_batch_from, self._m3_at_batch = s, g.m3_sent
                t0 = self.clock()
                await stream_chunk(chunk, g, enforce_pen_state=True,
                                   settle_dwell=max(j.min_dwell, 0.3))
                if g.pen_down:  # a batch never ends with the pen on the paper
                    await self._pen_up()
                self._in_batch_from = None
                self._account(L, s, e, self.clock() - t0)
                s = e + 1
                j.cursor.update(unit=ui, stroke=s, batch=j.cursor["batch"] + 1)
                self._refresh_progress()
                self._save()  # the resume point, after EVERY batch

                more = s < L.strokes or ui + 1 < n
                if more and self.control.stop_requested:
                    raise JobStopped()
                if more and self.control.pause_requested:
                    await self._park()
                    return self._halt("pause")
                pen_changes_next = s >= L.strokes and ui + 1 < n and \
                    plan.layers[ui + 1].color != L.color
                if (more and j.rezero_every and j.strokes_since_rezero >= j.rezero_every
                        and not pen_changes_next):
                    await self._park()
                    d = await self._wait("rezero", JobState.AWAITING_REZERO,
                                         f"RE-ZERO CHECK after {j.strokes_since_rezero} strokes: "
                                         "the head is at (0,0) — is it on the paper corner? "
                                         "Continue, or stop if it drifted")
                    if d != "continue":
                        return self._halt(d)
                    j.strokes_since_rezero = 0
                    approach = True
            j.cursor.update(unit=ui + 1, stroke=0, batch=0)
            self._refresh_progress()

        await self._park()
        j.cursor.update(unit=n, stroke=0)
        j.eta_min = 0.0
        j.progress["overall"] = [plan.total_strokes, plan.total_strokes]
        self._set(JobState.DONE, f"plate done — {plan.total_strokes} strokes, "
                                 f"{n} layers; parked (0,0)")
        return j

    def _account(self, L: PlateLayer, s: int, e: int, wall: float) -> None:
        """Strokes toward the re-zero budget + measured pace for the ETA."""
        self.job.strokes_since_rezero += e - s + 1
        self._model_streamed += sum(L.seconds[s:e + 1])
        self._wall_streamed += wall
        if self._model_streamed >= 60.0 and self._wall_streamed > 0:
            self.job.pace = round(min(4.0, max(0.25, self._wall_streamed / self._model_streamed)), 3)
