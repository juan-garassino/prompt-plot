"""Drive the plotter from the gallery viewer — one job at a time, frame first.

The viewer already knows which ``.gcode`` belongs to the plate on screen; this
turns that into a physical plot without a detour through the shell.

Safety, because a browser button now moves a real machine:

* the server must be started with ``--allow-plot``; otherwise every endpoint
  here reports ``enabled: false`` and refuses;
* the request must carry ``confirm: true``;
* the target must resolve inside ``gallery/`` and end in ``.gcode``;
* **the pen-up frame trace is mandatory and enforced here, not by convention**:
  an ink job is refused until a frame has been traced for that same paper in
  this server session (``promptplot plot frame`` from another terminal cannot
  satisfy it — this process has to have seen it);
* the layer is bounds-checked against the paper before a single command goes
  out, and a job that would draw outside it is refused;
* one job at a time, cancellable.

Plate jobs (``action: "plate"``) run the shared engine in
``promptplot/plotjob.py``: frame trace first, then per layer park at (0,0) and
WAIT for ``/plotter/continue`` (pen swap), pen-up approach, batches of
``batch_strokes``, a park-and-wait re-zero check every ``rezero_every`` strokes,
and the job file ``~/.promptplot/plot_jobs/<id>.json`` rewritten after every
batch. ``/plotter/pause`` stops at the next batch boundary; ``/plotter/resume``
reopens the port on a saved job. HTTP threads only flip ``threading.Event``s —
the job's own thread is the single owner (and single reader) of the port.

Imports of ``promptplot`` are deferred to the moment a job runs, so the gallery
server keeps working on a bare interpreter that cannot resolve the package.
"""

from __future__ import annotations

import asyncio
import logging
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

MAX_LOG = 400


class PlotterBridge:
    """Owns the serial port for the lifetime of a job. Thread-safe façade."""

    def __init__(self, gallery: Path, *, allow: bool = False,
                 port: Optional[str] = None, paper: str = "a4:landscape",
                 margin: float = 15.0, job_dir: Optional[Path] = None) -> None:
        self.gallery = gallery.resolve()
        self.job_dir = job_dir  # None → ~/.promptplot/plot_jobs
        self.allow = allow
        self.port = port
        self.paper = paper
        self.margin = margin
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None
        self._cancel = threading.Event()
        self._log: List[str] = []
        self._job: Optional[Dict[str, Any]] = None
        self._framed: Optional[str] = None  # the paper spec traced this session
        self._control: Any = None  # plotjob.JobControl of the running plate job

    # ---------- state ----------

    def _say(self, msg: str) -> None:
        line = f"{time.strftime('%H:%M:%S')}  {msg}"
        with self._lock:
            self._log.append(line)
            del self._log[:-MAX_LOG]
        logger.info("plotter: %s", msg)

    def state(self) -> Dict[str, Any]:
        with self._lock:
            job = dict(self._job) if self._job else None
            plate = job if job and job.get("action") == "plate" else {}
            return {
                "enabled": self.allow,
                "busy": bool(self._thread and self._thread.is_alive()),
                "port": self.port,
                "paper": self.paper,
                "margin": self.margin,
                "framed": self._framed,
                "frame_ok": self._framed == self.paper,
                "job": job,
                "waiting_for": plate.get("waiting_for"),
                "cursor": plate.get("cursor"),
                "progress": plate.get("progress"),
                "eta_min": plate.get("eta_min"),
                "log": list(self._log[-60:]),
                "reason": None if self.allow else
                          "server started without --allow-plot",
            }

    # ---------- helpers ----------

    def resolve_target(self, target: str) -> Path:
        p = (self.gallery / str(target)).resolve()
        if not p.is_relative_to(self.gallery):
            raise ValueError(f"target escapes the gallery: {target!r}")
        if p.suffix != ".gcode":
            raise ValueError(f"not a gcode file: {target!r}")
        if not p.is_file():
            raise ValueError(f"no such gcode: {target!r}")
        return p

    def _paper_wh(self) -> Tuple[float, float]:
        from promptplot.config import PaperConfig

        spec = self.paper
        if ":" in spec:
            size, orient = spec.split(":", 1)
        else:
            size, orient = spec, "landscape"
        pc = PaperConfig.from_size(size, orientation=orient, margin=self.margin)
        return pc.width, pc.height

    def _load(self, path: Path):
        from promptplot.config import PaperConfig, get_config
        from promptplot.pipeline import FilePipeline

        config = get_config()
        spec = self.paper
        size, orient = spec.split(":", 1) if ":" in spec else (spec, "landscape")
        config.paper = PaperConfig.from_size(size, orientation=orient, margin=self.margin)
        if self.port:
            config.serial.port = self.port
        return config, FilePipeline(config).load_gcode_file(str(path))

    def layers(self, target: str) -> Dict[str, Any]:
        """Colour layers in a gcode file, with the numbers the viewer shows."""
        from promptplot.orchestrate import split_color_layers, stroke_spans

        path = self.resolve_target(target)
        _config, program = self._load(path)
        out = []
        for color, cmds in split_color_layers(program):
            draw = sum(1 for c in cmds if c.command == "G1")
            out.append({"color": color, "strokes": len(stroke_spans(cmds)),
                        "commands": len(cmds), "draws": draw})
        return {"target": target, "layers": out}

    # ---------- jobs ----------

    def start(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        if not self.allow:
            raise ValueError("plotting disabled — start the server with --allow-plot")
        if not spec.get("confirm"):
            raise ValueError("refused: the request must carry confirm=true")
        with self._lock:
            if self._thread and self._thread.is_alive():
                raise ValueError("a job is already running")

        action = str(spec.get("action") or "")
        if action not in {"frame", "layer", "plate"}:
            raise ValueError(f"unknown action {action!r} (frame|layer|plate)")
        if action == "plate":
            return self._start_plate(spec)

        job: Dict[str, Any] = {"action": action, "started": time.time()}
        if action == "layer":
            # Validate the request before the frame gate, so a bad target reports
            # what is actually wrong with it rather than the missing frame.
            target = str(spec.get("target") or "")
            path = self.resolve_target(target)
            color = spec.get("color")
            if color is None:
                raise ValueError("a layer job needs a colour index")
            if self._framed != self.paper:
                raise ValueError(
                    "refused: trace the frame first — no pen-up frame has been "
                    f"traced for {self.paper} in this session")
            job.update(target=target, path=str(path), color=int(color),
                       strokes=spec.get("strokes"))

        self._cancel.clear()
        with self._lock:
            self._job = dict(job, state="running")
            self._log.clear()
        self._thread = threading.Thread(target=self._run, args=(job,), daemon=True)
        self._thread.start()
        return {"ok": True, "job": job}

    def stop(self) -> Dict[str, Any]:
        self._cancel.set()
        if self._control is not None:
            self._control.request_stop()
        self._say("stop requested — finishing the command in flight")
        return {"ok": True}

    # ---------- plate jobs ----------

    def _store(self):
        from promptplot.plotjob import JobStore

        return JobStore(self.job_dir)

    def _busy(self) -> bool:
        with self._lock:
            return bool(self._thread and self._thread.is_alive())

    def _plate_opts(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        from promptplot import plotjob as pj

        layers = spec.get("layers")
        if layers is not None:
            if not isinstance(layers, list) or not all(
                    isinstance(c, int) and not isinstance(c, bool) for c in layers):
                raise ValueError("layers must be a list of colour indices")
        opts = {"layers": layers}
        for key, default, cast in (("batch_strokes", pj.DEFAULT_BATCH_STROKES, int),
                                   ("rezero_every", pj.DEFAULT_REZERO_EVERY, int),
                                   ("max_feed", pj.DEFAULT_MAX_FEED, float),
                                   ("min_dwell", pj.DEFAULT_MIN_DWELL, float)):
            v = spec.get(key)
            opts[key] = default if v is None else cast(v)
        return opts

    def _start_plate(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """One click, whole plate. The job's first act is the frame trace, so
        the frame gate is satisfied by construction, never skipped."""
        from promptplot import plotjob as pj

        target = str(spec.get("target") or "")
        path = self.resolve_target(target)
        store = self._store()
        job = pj.new_job(path, target=target, paper=self.paper, margin=self.margin,
                         **self._plate_opts(spec))
        job.id = store.unique_id(job.id)
        plan = pj.plan_for_job(job)  # every layer bounds-checked BEFORE anything moves
        self._launch(job, plan, store, trace_frame=True, framed=False, resuming=False)
        return {"ok": True, "job": {"id": job.id, "action": "plate",
                                    "units": job.units, "eta_min": job.eta_min}}

    def resume(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Reopen the port on a saved job and continue from its cursor. Nothing
        is re-traced unless ``retrace``; with no frame traced in this process,
        ``retrace`` is required (the frame gate)."""
        from promptplot import plotjob as pj

        if not self.allow:
            raise ValueError("plotting disabled — start the server with --allow-plot")
        if not spec.get("confirm"):
            raise ValueError("refused: the request must carry confirm=true")
        if self._busy():
            raise ValueError("a job is already running")
        store = self._store()
        job = store.load(str(spec.get("job_id") or ""))
        if not job.resumable:
            raise ValueError(f"{job.id} is already done")
        if (job.paper, float(job.margin)) != (self.paper, float(self.margin)):
            raise ValueError(f"{job.id} was plotted on {job.paper} margin {job.margin:g}; "
                             f"this server is on {self.paper} margin {self.margin:g}")
        if self.resolve_target(job.path) != Path(job.path):  # raises if outside gallery/
            raise ValueError("the job's gcode is not inside the gallery")
        retrace = bool(spec.get("retrace"))
        framed = self._framed == self.paper
        if not (framed or retrace):
            raise ValueError("refused: no frame traced for "
                             f"{self.paper} in this session — resume with retrace")
        plan = pj.plan_for_job(job)  # refuses if the gcode changed underneath
        job.errors = []
        self._launch(job, plan, store, trace_frame=retrace, framed=framed, resuming=True)
        return {"ok": True, "job": {"id": job.id, "action": "plate", "cursor": job.cursor}}

    def _launch(self, job, plan, store, *, trace_frame: bool, framed: bool,
                resuming: bool) -> None:
        from promptplot import plotjob as pj

        with self._lock:
            if self._thread and self._thread.is_alive():
                raise ValueError("a job is already running")
        self._cancel.clear()
        self._control = pj.JobControl()
        runner = pj.PlateJobRunner(
            job, plan, connect=self._connect, control=self._control, store=store,
            trace_frame=trace_frame, framed=framed, resuming=resuming,
            on_update=self._on_job, on_framed=self._mark_framed, say=self._say)
        with self._lock:
            self._job = job.to_dict()
            self._log.clear()
        self._thread = threading.Thread(target=self._run_plate, args=(runner,), daemon=True)
        self._thread.start()

    def _on_job(self, snapshot: Dict[str, Any]) -> None:
        with self._lock:
            self._job = snapshot

    def _mark_framed(self) -> None:
        self._framed = self.paper

    def _run_plate(self, runner) -> None:
        try:
            asyncio.run(runner.run())
        except Exception as exc:  # the runner reports its own failures; belt and braces
            logger.exception("plate job crashed")
            self._finish("error", f"{type(exc).__name__}: {exc}")

    def _plate_running(self) -> bool:
        with self._lock:
            return bool(self._thread and self._thread.is_alive() and self._job
                        and self._job.get("action") == "plate")

    def continue_(self, spec: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Acknowledge a pen swap or a re-zero check. ``wait_seq`` (sent by the
        viewer) must name the wait on screen, so a stale or double click can
        never acknowledge the NEXT pen swap before anyone has seen it."""
        if not self._plate_running():
            raise ValueError("no plate job is running")
        with self._lock:
            waiting = (self._job or {}).get("waiting_for")
            seq = (self._job or {}).get("wait_seq")
        if not waiting:
            raise ValueError("the job is not waiting for anything")
        want = (spec or {}).get("wait_seq")
        if want is not None and int(want) != seq:
            raise ValueError("refused: the job has moved on to another wait — "
                             "read the new message, then continue")
        self._control.request_continue()
        self._say(f"{waiting} acknowledged")
        return {"ok": True, "continued": waiting}

    def pause(self) -> Dict[str, Any]:
        """Stop at the next batch boundary (or now, if waiting); resumable."""
        if not self._plate_running():
            raise ValueError("no plate job is running")
        self._control.request_pause()
        self._say("pause requested — stopping at the end of this batch")
        return {"ok": True}

    def jobs(self) -> Dict[str, Any]:
        return {"jobs": self._store().list()}

    def _finish(self, state: str, msg: str) -> None:
        with self._lock:
            if self._job:
                self._job["state"] = state
                self._job["message"] = msg
        self._say(msg)

    def _run(self, job: Dict[str, Any]) -> None:
        try:
            with self._store().port_lock():
                asyncio.run(self._run_async(job))
        except Exception as exc:  # a hardware failure must not kill the server
            logger.exception("plot job failed")
            self._finish("error", f"{type(exc).__name__}: {exc}")

    async def _connect(self):
        from promptplot.plotter import SerialPlotter

        from promptplot.config import get_config

        config = get_config()
        port = self.port or config.serial.port
        p = SerialPlotter(port=port, baud_rate=config.serial.baud_rate,
                          timeout=60.0, enable_heartbeat=False)
        self._say(f"connecting to {port}")
        if not await p.connect():
            raise RuntimeError(f"could not connect to {port}")
        self._say("connected")
        return p

    async def _run_async(self, job: Dict[str, Any]) -> None:
        if job["action"] == "frame":
            await self._do_frame()
        else:
            await self._do_layer(job)

    async def _do_frame(self) -> None:
        from promptplot.orchestrate import trace_frame_full

        w, h = self._paper_wh()
        p = await self._connect()
        try:
            self._say(f"tracing {w:g}x{h:g} margin {self.margin:g} — PEN UP")
            await trace_frame_full(p, w, h, self.margin)
        finally:
            await p.disconnect()
        self._framed = self.paper
        self._finish("done", f"frame traced for {self.paper} — safe to ink")

    async def _do_layer(self, job: Dict[str, Any]) -> None:
        from promptplot.engine import PenState
        from promptplot.orchestrate import (
            _first_drawn_point, slice_stroke_range, split_color_layers,
            stream_chunk, validate_chunk,
        )

        config, program = self._load(Path(job["path"]))
        bucket = next((c for col, c in split_color_layers(program)
                       if col == job["color"]), None)
        if bucket is None:
            raise RuntimeError(f"no layer with colour {job['color']}")
        if job.get("strokes"):
            s, e = (int(v) for v in str(job["strokes"]).split(":", 1))
            bucket = slice_stroke_range(bucket, s, e)

        # Bounds gate: refuse rather than let the head hunt for the limit switch.
        _checked, warnings, _pen = validate_chunk(bucket, PenState(), config.paper)
        if warnings:
            raise RuntimeError("out of bounds: " + "; ".join(warnings[:3]))

        fp = _first_drawn_point(bucket)
        self._say(f"colour {job['color']}: {len(bucket)} commands, first stroke at {fp}")

        p = await self._connect()
        try:
            await p.send_command("M5")
            if fp is not None:  # pen-up approach — never drag out of home
                await p.send_command(f"G0 X{fp[0]:.3f} Y{fp[1]:.3f}")
                await p.send_command("G4 P1.0")

            stopped = False

            def on_pause(done: int, total: int):
                nonlocal stopped
                with self._lock:
                    if self._job:
                        self._job["progress"] = [done, total]
                if self._cancel.is_set():
                    stopped = True
                    return False
                return None

            ok, err = await stream_chunk(bucket, p, on_pause=on_pause, verbose=False)
            await p.send_command("M5")
            await p.send_command("G4 P1.0")
            await p.send_command("G0 X0 Y0")
        finally:
            await p.disconnect()

        state = "stopped" if stopped or self._cancel.is_set() else "done"
        self._finish(state, f"colour {job['color']}: {ok} ok, {err} errors — parked (0,0)")
