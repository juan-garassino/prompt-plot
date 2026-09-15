"""plot command group: path fallback, layer listing, batch span math."""

from pathlib import Path

from click.testing import CliRunner

from promptplot.cli._group import cli
from promptplot.models import GCodeCommand
from promptplot.orchestrate import slice_stroke_range, stroke_spans

GCODE = """M5
G0 X10.000 Y10.000
M3 S1000 ; color=0
G1 X20.000 Y10.000 F1500 ; color=0
M5
G0 X30.000 Y10.000
M3 S1000 ; color=1
G1 X40.000 Y10.000 F1500 ; color=1
M5
G0 X50.000 Y10.000
M3 S1000 ; color=1
G1 X60.000 Y10.000 F1500 ; color=1
M5
G0 X0 Y0
"""


def _tmp_gcode(tmp_path: Path) -> Path:
    f = tmp_path / "toy.gcode"
    f.write_text(GCODE)
    return f


def test_plot_layer_list(tmp_path):
    f = _tmp_gcode(tmp_path)
    r = CliRunner().invoke(cli, ["plot", "layer", str(f), "--list"])
    assert r.exit_code == 0, r.output
    assert "color 0: 1 strokes" in r.output
    assert "color 1: 2 strokes" in r.output


def test_plot_layer_dry_run_batch(tmp_path):
    f = _tmp_gcode(tmp_path)
    r = CliRunner().invoke(cli, ["plot", "layer", str(f), "1", "--strokes", "1:1", "--dry-run"])
    assert r.exit_code == 0, r.output
    assert "dry-run" in r.output
    assert "(50.0, 10.0)" in r.output  # second stroke's pen-up approach point


def test_plot_path_fallback_dispatches_to_file(tmp_path):
    f = _tmp_gcode(tmp_path)
    out = tmp_path / "prev.png"
    r = CliRunner().invoke(cli, ["plot", str(f), "--preview-only", "-o", str(out)])
    assert r.exit_code == 0, r.output
    assert out.exists()


def test_stroke_span_math():
    cmds = [
        GCodeCommand(command="G0", x=1, y=1),
        GCodeCommand(command="M3", s=1000),
        GCodeCommand(command="G1", x=2, y=2, f=500),
        GCodeCommand(command="M5"),
        GCodeCommand(command="G0", x=3, y=3),
        GCodeCommand(command="M3", s=1000),
        GCodeCommand(command="G1", x=4, y=4, f=500),
        GCodeCommand(command="M5"),
    ]
    assert stroke_spans(cmds) == [1, 5]
    sl = slice_stroke_range(cmds, 1, 1)
    assert sl[0].command == "G0" and sl[0].x == 3  # includes the positioning travel
    assert sl[-1].command == "M5"
