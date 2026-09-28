"""Plate jobs (promptplot/plotjob.py) and the gallery server's job layer.

Stub classes only — no MagicMock, no serial port. The plotter is a
SimulatedPlotter subclass that records every line, position and pen state, and
can be scripted to fail or to trigger a pause/stop at a given moment.
"""

from __future__ import annotations

import asyncio
import json
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import pytest

from promptplot import plotjob as pj
from promptplot.models import GCodeCommand
from promptplot.plotter import SimulatedPlotter

REPO = Path(__file__).resolve().parent.parent
PAPER = "a5:landscape"  # 210 x 148, drawable [15,195] x [15,133] at margin 15


# ---------------------------------------------------------------------------
# fixtures: gcode, stubs
# ---------------------------------------------------------------------------

def _stroke_xy(color: int, k: int) -> Tuple[float, float, float, float]:
    x = 20.0 + 25.0 * color
    y = 20.0 + 6.0 * k
    return x, y, x + 10.0, y + 2.0


def make_gcode(colors: int, strokes: int, bad_color: Optional[int] = None) -> str:
    """The shape the renders have: M5 / dwell / G0 / M3 ; color / dwell / G1 ; color."""
    out = []
    for c in range(colors):
        for k in range(strokes):
            x0, y0, x1, y1 = _stroke_xy(c, k)
            if c == bad_color:
                x1 = 260.0  # off an A5 sheet
            out += ["M5", "G4 P0.2 ; pen up dwell", f"G0 X{x0:.3f} Y{y0:.3f}",
                    f"M3 S1000 ; color={c}", "G4 P0.2 ; pen down dwell",
                    f"G1 X{x1:.3f} Y{y1:.3f} F2200 ; color={c}"]
    out += ["M5", "G0 X0 Y0"]
    return "\n".join(out) + "\n"


def write_gcode(tmp_path: Path, colors: int, strokes: int, **kw) -> Path:
    p = tmp_path / f"plate_{colors}x{strokes}.gcode"
    p.write_text(make_gcode(colors, strokes, **kw))
    return p


class _StubPlotter(SimulatedPlotter):
    """Records (command, pen_down_before, position_before); scriptable."""

    def __init__(self, fail_at: Optional[int] = None,
                 hook: Optional[Callable[["_StubPlotter", str], None]] = None) -> None:
        super().__init__(command_delay=0)
        self.fail_at = fail_at
        self.hook = hook
        self.sent: List[str] = []
        self.status.last_error = None

    async def send_command(self, command: str) -> bool:
        idx = len(self.sent)
        self.sent.append(command)
        if self.hook:
            self.hook(self, command)
        if self.fail_at is not None and idx == self.fail_at:
            self.status.last_error = "error:9"
            return False
        return await super().send_command(command)

    def inked(self) -> List[Tuple[float, float, float, float]]:
        return [tuple(round(v, 3) for v in s[:4]) for s in self.lines if s[4]]


class _ScriptedControl(pj.JobControl):
    """Answers waits from a script (default: continue) and records each wait
    with where the head was and whether the pen was up."""

    def __init__(self, plotter: _StubPlotter, answers: Optional[List[str]] = None) -> None:
        super().__init__()
        self.plotter = plotter
        self.answers = list(answers or [])
        self.waits: List[Tuple[str, Tuple[float, float], bool, int]] = []

    async def wait_for_operator(self, kind: str, message: str) -> str:
        p = self.plotter
        self.waits.append((kind, p.position, p.pen_down, len(p.sent)))
        if self._stop.is_set():
            return "stop"
        if self._pause.is_set():
            return "pause"
        return self.answers.pop(0) if self.answers else "continue"


class _RecordingStore(pj.JobStore):
    def __init__(self, root: Path) -> None:
        super().__init__(root)
        self.snapshots: List[Dict] = []

    def save(self, job):
        p = super().save(job)
        self.snapshots.append(json.loads(p.read_text()))
        return p


def _connect(plotter: _StubPlotter, calls: Optional[List[int]] = None):
    async def connect():
        if calls is not None:
            calls.append(1)
        await plotter.connect()
        return plotter
    return connect


def _job_and_plan(path: Path, **kw):
    job = pj.new_job(path, paper=PAPER, margin=15.0, **kw)
    return job, pj.plan_for_job(job)


def _run(job, plan, plotter, control, store=None, **kw):
    runner = pj.PlateJobRunner(job, plan, connect=_connect(plotter), control=control,
                               store=store, **kw)
    return asyncio.run(runner.run())


def _expected_ink(colors: List[int], strokes: int):
    return [tuple(round(v, 3) for v in _stroke_xy(c, k)) for c in colors for k in range(strokes)]


def _first_move_after(plotter: _StubPlotter, sent_index: int) -> str:
    return next(c for c in plotter.sent[sent_index:] if c.startswith(("G0", "G1")))


# ---------------------------------------------------------------------------
# preparation, bounds, ETA
# ---------------------------------------------------------------------------

def test_prepare_caps_feed_makes_it_explicit_and_floors_dwells():
    cmds = [GCodeCommand(command="G1", x=1, y=1, f=2200),
            GCodeCommand(command="G1", x=2, y=2),
            GCodeCommand.from_string("G4 P0.2"),  # the loader keeps sub-second dwells
            GCodeCommand(command="G4", p=2.0)]
    assert cmds[2].p == 0.2
    out = pj.prepare_commands(cmds, max_feed=500, min_dwell=1.0)
    assert [c.f for c in out[:2]] == [500, 500]  # modal feed made explicit (resume-safe)
    assert out[2].p == 1.0 and out[3].p == 2.0
    assert len(out) == len(cmds)
    raw = pj.prepare_commands(cmds, max_feed=0, min_dwell=0)
    assert raw[0].f == 2200 and raw[1].f == 2200 and raw[2].p == 0.2


def test_eta_model_matches_hand_arithmetic():
    cmds = [GCodeCommand(command="M5"), GCodeCommand(command="G4", p=1.0),
            GCodeCommand(command="G0", x=60.0, y=80.0),         # 100 mm @ 2000 → 3 s
            GCodeCommand(command="M3", s=1000), GCodeCommand(command="G4", p=1.0),
            GCodeCommand(command="G1", x=120.0, y=80.0, f=600)]  # 60 mm @ 600 → 6 s
    assert pj.stroke_seconds(cmds) == [pytest.approx(11.0)]
    # no dwells in the file → priced per pen cycle instead
    bare = [c for c in cmds if c.command != "G4"]
    assert pj.stroke_seconds(bare) == [pytest.approx(9.0 + pj.LEO_DWELL_S)]


def test_eta_sanity_on_a_plan(tmp_path):
    path = write_gcode(tmp_path, colors=2, strokes=4)
    job, plan = _job_and_plan(path, rezero_every=0)
    draw = sum(sum(L.seconds) for L in plan.layers)
    total = plan.remaining_seconds(0, 0, 0, swap_pending=True)
    assert total == pytest.approx(draw + 2 * pj.SWAP_S)          # two pens loaded
    assert plan.remaining_seconds(1, 2) < plan.remaining_seconds(0, 0)
    assert plan.remaining_seconds(0, 0, rezero_every=3) == pytest.approx(
        plan.remaining_seconds(0, 0) + (8 // 3) * pj.REZERO_S)
    # 10 mm draws at the capped F500 dominate each stroke's draw time
    ten_mm = 10.2 / 500 * 60
    assert all(s > ten_mm for L in plan.layers for s in L.seconds)


def test_bounds_refusal_names_the_bad_layer(tmp_path):
    path = write_gcode(tmp_path, colors=3, strokes=2, bad_color=2)
    job = pj.new_job(path, paper=PAPER, margin=15.0)
    with pytest.raises(pj.PlotRefused, match="colour 2"):
        pj.plan_for_job(job)
    # the same plate is fine without the bad pen
    job2 = pj.new_job(path, paper=PAPER, margin=15.0, layers=[0, 1])
    assert [L.color for L in pj.plan_for_job(job2).layers] == [0, 1]


def test_runner_rechecks_each_layer_before_it_streams(tmp_path):
    good = write_gcode(tmp_path, colors=2, strokes=2)
    job, plan = _job_and_plan(good, batch_strokes=0, rezero_every=0)
    # Corrupt layer 2 AFTER planning: only the per-layer re-check can catch it.
    L = plan.layers[1]
    L.commands = [c.model_copy(update={"x": 300.0}) if c.command == "G1" else c
                  for c in L.commands]
    plotter = _StubPlotter()
    ctl = _ScriptedControl(plotter)
    _run(job, plan, plotter, ctl)
    assert job.state == "error" and "out of bounds" in job.message
    assert len(plotter.inked()) == 2                       # layer 1 only
    assert all(seg[2] <= 195.0 for seg in plotter.inked())
    assert plotter.position == (0.0, 0.0) and not plotter.pen_down


# ---------------------------------------------------------------------------
# the sequence
# ---------------------------------------------------------------------------

def test_full_three_layer_sequence(tmp_path):
    path = write_gcode(tmp_path, colors=3, strokes=5)
    job, plan = _job_and_plan(path, batch_strokes=2, rezero_every=3)
    plotter = _StubPlotter()
    ctl = _ScriptedControl(plotter)
    store = _RecordingStore(tmp_path / "jobs")
    _run(job, plan, plotter, ctl, store=store)

    assert job.state == "done", job.message
    # 1. frame first, pen up: nothing inks before the full edge + margin tour
    first_m3 = next(i for i, c in enumerate(plotter.sent) if c.startswith("M3"))
    frame = plotter.sent[:first_m3]
    assert frame[0] == "M5" and "G0 X210 Y0" in frame and "G4 P3" in frame
    assert "G0 X195 Y133" in frame  # the margin rectangle
    # 2. per layer: swap wait at (0,0) pen up; re-zero every 3 strokes in-layer
    kinds = [w[0] for w in ctl.waits]
    assert kinds == ["swap", "rezero"] * 3
    for _kind, pos, pen_down, _ in ctl.waits:
        assert pos == (0.0, 0.0) and not pen_down
    # 3. after every wait, the first move is a pen-UP rapid to the next stroke
    for (_kind, _pos, _pen, at), (x0, y0) in zip(
            ctl.waits, [_stroke_xy(c, k)[:2] for c in range(3) for k in (0, 3)]):
        assert _first_move_after(plotter, at) == f"G0 X{x0:.3f} Y{y0:.3f}"
    # 4. every stroke inked exactly once, in order, and nothing dragged from home
    assert plotter.inked() == _expected_ink([0, 1, 2], 5)
    assert all((s[0], s[1]) != (0.0, 0.0) for s in plotter.inked())
    # 5. parked, pen up, progress complete
    assert plotter.position == (0.0, 0.0) and not plotter.pen_down
    assert job.progress["overall"] == [15, 15] and job.eta_min == 0.0
    # feeds capped on the wire
    assert all("F500" in c for c in plotter.sent if c.startswith("G1"))


def test_ink_job_refused_without_a_frame(tmp_path):
    path = write_gcode(tmp_path, colors=2, strokes=2)
    job, plan = _job_and_plan(path)
    plotter = _StubPlotter()
    calls: List[int] = []
    runner = pj.PlateJobRunner(job, plan, connect=_connect(plotter, calls),
                               control=_ScriptedControl(plotter),
                               trace_frame=False, framed=False)
    asyncio.run(runner.run())
    assert job.state == "error" and "trace the frame first" in job.message
    assert calls == [] and plotter.sent == []   # the port was never even opened


def test_pause_stops_at_a_batch_boundary(tmp_path):
    path = write_gcode(tmp_path, colors=2, strokes=6)
    job, plan = _job_and_plan(path, batch_strokes=4, rezero_every=0)
    ctl_box: List[pj.JobControl] = []

    def hook(p: _StubPlotter, cmd: str) -> None:
        # ask for a pause while the SECOND stroke of the first batch is drawing
        if cmd.startswith("M3") and sum(c.startswith("M3") for c in p.sent) == 2:
            ctl_box[0].request_pause()

    plotter = _StubPlotter(hook=hook)
    ctl = _ScriptedControl(plotter)
    ctl_box.append(ctl)
    store = _RecordingStore(tmp_path / "jobs")
    _run(job, plan, plotter, ctl, store=store)

    assert job.state == "paused"
    assert job.cursor["unit"] == 0 and job.cursor["stroke"] == 4   # the batch finished
    assert len(plotter.inked()) == 4                              # never mid-stroke
    assert plotter.position == (0.0, 0.0) and not plotter.pen_down
    on_disk = json.loads(store.path(job.id).read_text())
    assert on_disk["state"] == "paused" and on_disk["cursor"]["stroke"] == 4


def test_job_file_written_after_every_batch(tmp_path):
    path = write_gcode(tmp_path, colors=2, strokes=5)
    job, plan = _job_and_plan(path, batch_strokes=2, rezero_every=0)
    plotter = _StubPlotter()
    store = _RecordingStore(tmp_path / "jobs")
    _run(job, plan, plotter, _ScriptedControl(plotter), store=store)

    batch_saves = [(s["cursor"]["unit"], s["cursor"]["stroke"]) for s in store.snapshots
                   if s["state"] == "streaming"]
    assert batch_saves == [(0, 2), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5)]
    etas = [s["eta_min"] for s in store.snapshots if s["state"] == "streaming"]
    assert etas == sorted(etas, reverse=True)                    # ETA only goes down
    final = pj.JobStore(tmp_path / "jobs").load(job.id)
    assert final.state == "done" and not final.resumable
    assert pj.JobStore(tmp_path / "jobs").list()[0]["id"] == job.id


def test_resume_continues_at_the_exact_stroke_without_redrawing(tmp_path):
    path = write_gcode(tmp_path, colors=3, strokes=5)
    store = pj.JobStore(tmp_path / "jobs")
    job, plan = _job_and_plan(path, batch_strokes=2, rezero_every=0)
    first = _StubPlotter()
    ctl = _ScriptedControl(first, answers=["continue", "continue", "pause"])  # pause at swap 3
    _run(job, plan, first, ctl, store=store)
    assert job.state == "paused" and job.cursor == {"unit": 2, "stroke": 0, "batch": 0}

    # A new process: load the file, rebuild the plan, reopen the port.
    job2 = store.load(job.id)
    plan2 = pj.plan_for_job(job2)
    second = _StubPlotter()
    ctl2 = _ScriptedControl(second)
    _run(job2, plan2, second, ctl2, store=store, trace_frame=False, framed=job2.framed,
         resuming=True)

    assert job2.state == "done", job2.message
    assert "G4 P3" not in second.sent                   # the frame was NOT re-traced
    kind, pos, pen_down, at = ctl2.waits[0]
    assert kind == "rezero" and second.sent[:at] == ["M5"]   # nothing moved before the check
    x0, y0 = _stroke_xy(2, 0)[:2]
    assert _first_move_after(second, at) == f"G0 X{x0:.3f} Y{y0:.3f}"
    both = first.inked() + second.inked()
    assert both == _expected_ink([0, 1, 2], 5)          # no gap, no overdraw


def test_resume_mid_layer_after_pause(tmp_path):
    path = write_gcode(tmp_path, colors=1, strokes=7)
    store = pj.JobStore(tmp_path / "jobs")
    job, plan = _job_and_plan(path, batch_strokes=3, rezero_every=0)
    box: List[pj.JobControl] = []
    first = _StubPlotter(hook=lambda p, c: box[0].request_pause()
                         if c.startswith("M3") and sum(x.startswith("M3") for x in p.sent) == 1
                         else None)
    ctl = _ScriptedControl(first)
    box.append(ctl)
    _run(job, plan, first, ctl, store=store)
    assert job.cursor["stroke"] == 3

    job2 = store.load(job.id)
    second = _StubPlotter()
    _run(job2, pj.plan_for_job(job2), second, _ScriptedControl(second), store=store,
         trace_frame=False, framed=True, resuming=True)
    assert second.inked() == _expected_ink([0], 7)[3:]
    assert first.inked() + second.inked() == _expected_ink([0], 7)


def test_stop_mid_batch_lifts_parks_and_rewinds_to_the_open_stroke(tmp_path):
    path = write_gcode(tmp_path, colors=1, strokes=6)
    store = pj.JobStore(tmp_path / "jobs")
    job, plan = _job_and_plan(path, batch_strokes=0, rezero_every=0)
    box: List[pj.JobControl] = []

    def hook(p: _StubPlotter, cmd: str) -> None:
        if cmd.startswith("M3") and sum(c.startswith("M3") for c in p.sent) == 3:
            box[0].request_stop()          # pen goes down on stroke index 2, then stop

    plotter = _StubPlotter(hook=hook)
    ctl = _ScriptedControl(plotter)
    box.append(ctl)
    _run(job, plan, plotter, ctl, store=store)
    assert job.state == "stopped" and job.resumable
    assert job.cursor["stroke"] == 2          # the open stroke is redrawn on resume
    assert not plotter.pen_down and plotter.position == (0.0, 0.0)
    assert plotter.sent[-3:][0] == "M5"


def test_failed_ack_aborts_lifts_and_parks(tmp_path):
    path = write_gcode(tmp_path, colors=1, strokes=5)
    job, plan = _job_and_plan(path, batch_strokes=0, rezero_every=0)
    probe = _StubPlotter()
    _run(*_job_and_plan(path, batch_strokes=0, rezero_every=0), probe, _ScriptedControl(probe))
    third_draw = [i for i, c in enumerate(probe.sent) if c.startswith("G1")][2]

    plotter = _StubPlotter(fail_at=third_draw)
    _run(job, plan, plotter, _ScriptedControl(plotter))
    assert job.state == "error" and "error:9" in job.message
    assert plotter.sent[third_draw + 1] == "M5"            # the very next line lifts the pen
    assert len(plotter.sent) <= third_draw + 4              # and nothing else streams
    assert not plotter.pen_down and plotter.position == (0.0, 0.0)
    assert job.cursor["stroke"] == 2                        # redraw the failed stroke


def test_six_colour_plate_end_to_end(tmp_path):
    path = write_gcode(tmp_path, colors=6, strokes=3)
    job, plan = _job_and_plan(path, batch_strokes=2, rezero_every=0)
    plotter = _StubPlotter()
    ctl = _ScriptedControl(plotter)
    _run(job, plan, plotter, ctl, store=pj.JobStore(tmp_path / "jobs"))
    assert job.state == "done"
    assert [w[0] for w in ctl.waits] == ["swap"] * 6
    assert plotter.inked() == _expected_ink(list(range(6)), 3)
    assert [u["color"] for u in job.units] == [0, 1, 2, 3, 4, 5]


def test_layers_option_orders_and_subsets(tmp_path):
    path = write_gcode(tmp_path, colors=6, strokes=2)
    job, plan = _job_and_plan(path, layers=[5, 0, 3], rezero_every=0)
    plotter = _StubPlotter()
    ctl = _ScriptedControl(plotter)
    _run(job, plan, plotter, ctl)
    assert [w[0] for w in ctl.waits] == ["swap"] * 3
    assert plotter.inked() == _expected_ink([5, 0, 3], 2)
    with pytest.raises(pj.PlotRefused, match="no layer with colour"):
        _job_and_plan(path, layers=[9])


def test_resume_refused_when_the_gcode_changed(tmp_path):
    path = write_gcode(tmp_path, colors=2, strokes=2)
    job = pj.new_job(path, paper=PAPER, margin=15.0)
    path.write_text(make_gcode(2, 3))
    with pytest.raises(pj.PlotRefused, match="changed"):
        pj.plan_for_job(job)


def test_one_job_owns_the_plotter(tmp_path):
    store = pj.JobStore(tmp_path / "jobs")
    with store.port_lock():
        with pytest.raises(pj.PlotterBusy):
            with pj.JobStore(tmp_path / "jobs").port_lock():
                pass
    with store.port_lock():  # released
        pass


def test_job_ids_cannot_escape_the_store(tmp_path):
    with pytest.raises(ValueError):
        pj.JobStore(tmp_path).path("../../etc/passwd")


def test_cli_plate_dry_run_rehearses_the_whole_sequence(tmp_path):
    from click.testing import CliRunner

    from promptplot.cli._group import cli

    path = write_gcode(tmp_path, colors=6, strokes=3)
    r = CliRunner().invoke(cli, ["plot", "plate", str(path), "--paper", PAPER,
                                 "--batch-strokes", "2", "--dry-run"])
    assert r.exit_code == 0, r.output
    text = " ".join(r.output.split())  # rich wraps at the terminal width
    assert "layer 6: colour 5" in text
    assert "waits: swap, swap, swap, swap, swap, swap → done" in text
    bad = write_gcode(tmp_path, colors=2, strokes=2, bad_color=1)
    r = CliRunner().invoke(cli, ["plot", "plate", str(bad), "--paper", PAPER, "--dry-run"])
    assert r.exit_code != 0 and "refused" in r.output


# ---------------------------------------------------------------------------
# the gallery server's bridge (scripts/gallery_plotter.py)
# ---------------------------------------------------------------------------

sys.path.insert(0, str(REPO / "scripts"))
import gallery_plotter  # noqa: E402


class _SimBridge(gallery_plotter.PlotterBridge):
    """The bridge with its serial connection replaced by a recording simulator."""

    def __init__(self, gallery: Path, **kw) -> None:
        super().__init__(gallery, allow=True, paper=PAPER, margin=15.0,
                         job_dir=gallery / "_jobs", **kw)
        self.plotters: List[_StubPlotter] = []

    async def _connect(self):
        p = _StubPlotter()
        await p.connect()
        self.plotters.append(p)
        return p


def _until(pred: Callable[[], bool], timeout: float = 20.0) -> None:
    t0 = time.time()
    while not pred():
        if time.time() - t0 > timeout:
            raise AssertionError("timed out waiting for the bridge")
        time.sleep(0.02)


def _answer(get_state: Callable[[], dict], act: Callable[[], object]) -> None:
    """Wait for the job to wait, answer, then wait until the runner has acted
    on it (its log grows) — a fast simulator can leave one wait and enter the
    next before a poll ever sees ``waiting_for`` go back to None."""
    _until(lambda: get_state()["waiting_for"] is not None)
    n = len(get_state()["job"]["log"])
    act()
    _until(lambda: len(get_state()["job"]["log"]) > n)


def _drive(bridge: _SimBridge, answers: List[str]) -> None:
    """Answer each wait the job reaches, then let the thread finish."""
    for a in answers:
        _answer(bridge.state, bridge.continue_ if a == "continue" else bridge.pause)
    _until(lambda: not bridge.state()["busy"])


@pytest.fixture
def gallery(tmp_path):
    g = tmp_path / "gallery"
    (g / "plates").mkdir(parents=True)
    (g / "plates" / "p.gcode").write_text(make_gcode(3, 3))
    return g


def test_bridge_plate_job_swaps_and_finishes(gallery):
    b = _SimBridge(gallery)
    out = b.start({"action": "plate", "target": "plates/p.gcode", "confirm": True,
                   "batch_strokes": 2, "rezero_every": 0})
    assert out["ok"] and len(out["job"]["units"]) == 3
    with pytest.raises(ValueError, match="already running"):
        b.start({"action": "plate", "target": "plates/p.gcode", "confirm": True})
    _until(lambda: b.state()["waiting_for"] == "swap")
    st = b.state()
    assert st["cursor"]["unit"] == 0 and st["progress"]["overall"] == [0, 9]
    assert st["eta_min"] > 0 and st["frame_ok"]      # the job traced the frame itself
    _drive(b, ["continue"] * 3)
    st = b.state()
    assert st["job"]["state"] == "done" and st["progress"]["overall"] == [9, 9]
    assert b.plotters[0].inked() == _expected_ink([0, 1, 2], 3)
    assert b.jobs()["jobs"][0]["state"] == "done"
    with pytest.raises(ValueError, match="no plate job"):
        b.continue_()


def test_bridge_refusals(gallery):
    b = _SimBridge(gallery)
    with pytest.raises(ValueError, match="confirm"):
        b.start({"action": "plate", "target": "plates/p.gcode"})
    with pytest.raises(ValueError, match="escapes"):
        b.start({"action": "plate", "target": "../x.gcode", "confirm": True})
    (gallery / "plates" / "bad.gcode").write_text(make_gcode(2, 2, bad_color=1))
    with pytest.raises(ValueError, match="out of bounds"):
        b.start({"action": "plate", "target": "plates/bad.gcode", "confirm": True})
    with pytest.raises(ValueError, match="trace the frame first"):
        b.start({"action": "layer", "target": "plates/p.gcode", "color": 0, "confirm": True})
    assert b.plotters == []                                  # nothing ever connected


def test_bridge_pause_then_resume_in_a_new_server(gallery):
    b = _SimBridge(gallery)
    b.start({"action": "plate", "target": "plates/p.gcode", "confirm": True,
             "rezero_every": 0})
    _drive(b, ["continue", "pause"])                         # pause at the 2nd pen swap
    job_id = b.state()["job"]["id"]
    assert b.state()["job"]["state"] == "paused"

    b2 = _SimBridge(gallery)                                 # restarted server: no frame
    with pytest.raises(ValueError, match="retrace"):
        b2.resume({"job_id": job_id, "confirm": True})
    b2.resume({"job_id": job_id, "confirm": True, "retrace": True})
    _drive(b2, ["continue", "continue"])                     # origin check, last swap
    assert b2.state()["job"]["state"] == "done"
    assert b.plotters[0].inked() + b2.plotters[0].inked() == _expected_ink([0, 1, 2], 3)
    with pytest.raises(ValueError, match="already done"):
        b2.resume({"job_id": job_id, "confirm": True, "retrace": True})


def test_server_routes(gallery, monkeypatch):
    import gallery_serve
    from http.server import ThreadingHTTPServer

    b = _SimBridge(gallery)
    monkeypatch.setattr(gallery_serve, "BRIDGE", b)
    srv = ThreadingHTTPServer(("127.0.0.1", 0), gallery_serve.Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"

    def call(route: str, body: Optional[dict] = None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(base + route, data=data,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            with e:
                return e.code, json.loads(e.read())

    try:
        assert call("/plotter/jobs") == (200, {"jobs": []})
        code, out = call("/plotter/continue", {})
        assert code == 400 and "no plate job" in out["error"]
        code, out = call("/plotter/job", {"action": "plate", "target": "plates/p.gcode",
                                          "confirm": True, "rezero_every": 0})
        assert code == 200, out
        for _ in range(3):
            _answer(lambda: call("/plotter/state")[1],
                    lambda: call("/plotter/continue", {}))
        _until(lambda: not call("/plotter/state")[1]["busy"])
        assert call("/plotter/state")[1]["job"]["state"] == "done"
        code, out = call("/plotter/resume", {"job_id": "j-bad", "confirm": True})
        assert code == 400
    finally:
        srv.shutdown()
        srv.server_close()


def test_bridge_continue_must_name_the_wait_on_screen(gallery):
    b = _SimBridge(gallery)
    b.start({"action": "plate", "target": "plates/p.gcode", "confirm": True,
             "rezero_every": 0})
    _until(lambda: b.state()["waiting_for"] == "swap")
    first = b.state()["job"]["wait_seq"]
    _answer(b.state, lambda: b.continue_({"wait_seq": first}))
    _until(lambda: b.state()["waiting_for"] == "swap" and b.state()["job"]["wait_seq"] > first)
    with pytest.raises(ValueError, match="moved on"):
        b.continue_({"wait_seq": first})            # a double click on the old swap
    assert b.state()["waiting_for"] == "swap"         # ... did not acknowledge this one
    b.stop()
    _until(lambda: not b.state()["busy"])
    assert b.state()["job"]["state"] == "stopped"
