"""Tests for promptplot/postprocess.py — pen safety, optimization, paint dips, dwells, pipeline."""

import pytest
from promptplot.models import GCodeCommand, GCodeProgram
from promptplot.config import PromptPlotConfig, PenConfig, BrushConfig
from promptplot.postprocess import (
    ensure_pen_safety,
    extract_strokes,
    optimize_stroke_order,
    optimize_gcode_program,
    insert_paint_dips,
    insert_pen_dwells,
    run_pipeline,
)


def _make(data):
    return [GCodeCommand(**c) for c in data]


def _prog(data):
    return GCodeProgram(commands=_make(data))


class TestEnsurePenSafety:
    def test_adds_initial_m5(self):
        cmds = _make([
            {"command": "G0", "x": 10, "y": 10},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        result = ensure_pen_safety(cmds)
        assert result[0].command == "M5"

    def test_inserts_m5_before_g0_when_pen_down(self):
        cmds = _make([
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "G0", "x": 100, "y": 100},  # missing M5 before travel
        ])
        result = ensure_pen_safety(cmds)
        # Find the G0 and check M5 comes before it
        for i, cmd in enumerate(result):
            if cmd.command == "G0" and cmd.x == 100:
                assert result[i - 1].command == "M5"
                break

    def test_inserts_m3_before_g1_when_pen_up(self):
        cmds = _make([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},  # missing M3
        ])
        result = ensure_pen_safety(cmds)
        for i, cmd in enumerate(result):
            if cmd.command == "G1":
                assert result[i - 1].command == "M3"
                break

    def test_ensures_final_pen_up(self):
        cmds = _make([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            # Missing final M5
        ])
        result = ensure_pen_safety(cmds)
        # Should end with M5 then G0 X0 Y0
        pen_up_found = False
        for cmd in reversed(result):
            if cmd.command == "M5":
                pen_up_found = True
                break
        assert pen_up_found

    def test_ensures_return_home(self):
        cmds = _make([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        result = ensure_pen_safety(cmds)
        last_g0 = None
        for cmd in reversed(result):
            if cmd.command == "G0":
                last_g0 = cmd
                break
        assert last_g0 is not None
        assert last_g0.x == 0.0 and last_g0.y == 0.0

    def test_uses_config_s_value(self):
        pen = PenConfig(pen_down_s_value=500)
        cmds = _make([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
        ])
        result = ensure_pen_safety(cmds, pen)
        m3_cmds = [c for c in result if c.command == "M3"]
        assert len(m3_cmds) > 0
        assert m3_cmds[0].s == 500


class TestExtractStrokes:
    def test_basic_strokes(self):
        cmds = _make([
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 100, "y": 100, "f": 2000},
            {"command": "M5"},
        ])
        strokes = extract_strokes(cmds)
        assert len(strokes) == 2

    def test_unclosed_stroke(self):
        cmds = _make([
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
        ])
        strokes = extract_strokes(cmds)
        assert len(strokes) == 1
        assert strokes[0][-1].command == "M5"  # Auto-closed


class TestOptimizeStrokeOrder:
    def test_single_stroke_unchanged(self):
        cmds = _make([
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        strokes = extract_strokes(cmds)
        ordered = optimize_stroke_order(strokes)
        assert len(ordered) == 1

    def test_reorders_to_minimize_travel(self):
        # Stroke 1: far away (100, 100)
        # Stroke 2: near origin (5, 5)
        # Starting from (0,0), should pick stroke 2 first
        cmds = _make([
            {"command": "G0", "x": 100, "y": 100},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 110, "y": 110, "f": 2000},
            {"command": "M5"},
            {"command": "G0", "x": 5, "y": 5},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 15, "y": 15, "f": 2000},
            {"command": "M5"},
        ])
        strokes = extract_strokes(cmds)
        ordered = optimize_stroke_order(strokes)
        # The stroke near origin should come first
        first_g1 = [c for c in ordered[0] if c.command == "G1"][0]
        assert first_g1.x == 15.0


class TestOptimizeGCodeProgram:
    def test_single_stroke_passthrough(self):
        prog = _prog([
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        result = optimize_gcode_program(prog)
        assert len(result.commands) >= 1


class TestInsertPaintDips:
    def test_disabled_passthrough(self):
        prog = _prog([
            {"command": "M5"},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        brush = BrushConfig(enabled=False)
        result = insert_paint_dips(prog, brush)
        assert len(result.commands) == len(prog.commands)

    def test_inserts_dip_at_interval(self):
        cmds_data = [{"command": "M5"}]
        for i in range(5):
            cmds_data.extend([
                {"command": "M3", "s": 1000},
                {"command": "G1", "x": i * 10 + 10, "y": i * 10 + 10, "f": 2000},
                {"command": "M5"},
            ])
        prog = _prog(cmds_data)
        brush = BrushConfig(enabled=True, strokes_before_reload=2)
        result = insert_paint_dips(prog, brush)
        # Should have more commands due to dip sequences
        assert len(result.commands) > len(prog.commands)
        # Should have G4 dwell commands (hold in ink)
        g4_cmds = [c for c in result.commands if c.command == "G4"]
        assert len(g4_cmds) > 0


class TestInsertPenDwells:
    def test_adds_dwells_after_m3_m5(self):
        prog = _prog([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        pen = PenConfig(pen_down_delay=0.2, pen_up_delay=0.2)
        result = insert_pen_dwells(prog, pen)
        g4_cmds = [c for c in result.commands if c.command == "G4"]
        assert len(g4_cmds) >= 2  # At least one after M3 and one after M5

    def test_zero_delay_no_dwells(self):
        prog = _prog([
            {"command": "M5"},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "M5"},
        ])
        pen = PenConfig(pen_down_delay=0.0, pen_up_delay=0.0)
        result = insert_pen_dwells(prog, pen)
        g4_cmds = [c for c in result.commands if c.command == "G4"]
        assert len(g4_cmds) == 0


class TestRunPipeline:
    def test_full_pipeline(self):
        prog = _prog([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 50, "y": 50, "f": 2000},
            {"command": "G1", "x": 80, "y": 80, "f": 2000},
            {"command": "M5"},
            {"command": "G0", "x": 0, "y": 0},
        ])
        config = PromptPlotConfig()
        result = run_pipeline(prog, config)
        assert isinstance(result, GCodeProgram)
        assert len(result.commands) > 0
        # Should start with M5 and end with G0 X0 Y0
        assert result.commands[0].command == "M5"

    def test_pipeline_handles_single_command(self):
        prog = _prog([
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
        ])
        config = PromptPlotConfig()
        result = run_pipeline(prog, config)
        assert isinstance(result, GCodeProgram)


def _inked_segments(cmds):
    """Set of (start, end) segments drawn with the pen down."""
    segs, pos, down = set(), (0.0, 0.0), False
    for c in cmds:
        if c.command == "M3":
            down = True
        elif c.command == "M5":
            down = False
        elif c.command in ("G0", "G1"):
            nxt = (c.x if c.x is not None else pos[0], c.y if c.y is not None else pos[1])
            if down and c.command == "G1" and nxt != pos:
                segs.add(tuple(sorted((pos, nxt))))
            pos = nxt
    return segs


class TestStrokeStartRegression:
    """Reordering must never add ink: each stroke starts where its pen went down."""

    def test_z_only_g0_does_not_hide_xy_travel(self):
        cmds = _make([
            {"command": "M5"},
            {"command": "G0", "x": 150, "y": 150},
            {"command": "G0", "z": 0},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 190, "y": 190, "f": 2000},
            {"command": "G0", "z": 5},
            {"command": "M5"},
            {"command": "G0", "x": 30, "y": 30},
            {"command": "G0", "z": 0},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 60, "y": 30, "f": 2000},
            {"command": "M5"},
        ])
        out = optimize_gcode_program(GCodeProgram(commands=ensure_pen_safety(cmds)))
        assert _inked_segments(out.commands) == _inked_segments(cmds)

    def test_relowered_pen_without_travel_keeps_start(self):
        cmds = _make([
            {"command": "M5"},
            {"command": "G0", "x": 100, "y": 100},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 140, "y": 100, "f": 2000},
            {"command": "M5"},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 140, "y": 140, "f": 2000},
            {"command": "M5"},
            {"command": "G0", "x": 10, "y": 10},
            {"command": "M3", "s": 1000},
            {"command": "G1", "x": 20, "y": 10, "f": 2000},
            {"command": "M5"},
        ])
        out = optimize_gcode_program(GCodeProgram(commands=cmds))
        assert _inked_segments(out.commands) == _inked_segments(cmds)


def _seg(x0, y0, x1, y1, color=None):
    return [
        GCodeCommand(command="G0", x=x0, y=y0),
        GCodeCommand(command="M3", s=1000, color=color),
        GCodeCommand(command="G1", x=x1, y=y1, f=2000, color=color),
        GCodeCommand(command="M5"),
    ]


class TestOrderingImprovements:
    def test_reverse_stroke_keeps_ink(self):
        from promptplot.postprocess import reverse_stroke

        stroke = _seg(10, 10, 20, 10)[:-1] + [
            GCodeCommand(command="G1", y=30, f=900),  # partial coordinate
            GCodeCommand(command="M5"),
        ]
        rev = reverse_stroke(stroke)
        assert (rev[0].x, rev[0].y) == (20, 30)
        assert [(c.x, c.y) for c in rev if c.command == "G1"] == [(20, 10), (10, 10)]
        assert rev[2].f == 900  # feed travels with its segment
        assert _inked_segments(rev) == _inked_segments(stroke)

    def test_reversal_used_when_end_is_closer(self):
        strokes = [_seg(10, 10, 100, 10), _seg(200, 10, 101, 10)]
        ordered = optimize_stroke_order(strokes)
        assert (ordered[1][0].x, ordered[1][0].y) == (101, 10)

    def test_input_order_kept_when_not_worse(self):
        strokes = [_seg(1, 0, 2, 0), _seg(3, 0, 4, 0), _seg(5, 0, 6, 0)]
        assert optimize_stroke_order(strokes) is strokes

    def test_contiguous_strokes_merge_into_one_pen_down(self):
        cmds = _seg(10, 10, 20, 10) + _seg(20, 10, 20, 20) + _seg(50, 50, 60, 60)
        out = optimize_gcode_program(GCodeProgram(commands=cmds))
        assert sum(c.command == "M3" for c in out.commands) == 2
        assert _inked_segments(out.commands) == _inked_segments(cmds)
        unmerged = optimize_gcode_program(GCodeProgram(commands=cmds), merge=False)
        assert sum(c.command == "M3" for c in unmerged.commands) == 3

    def test_merge_never_joins_different_colours(self):
        from promptplot.postprocess import merge_contiguous_strokes

        merged = merge_contiguous_strokes([_seg(10, 10, 20, 10, 0), _seg(20, 10, 30, 10, 1)])
        assert len(merged) == 2

    def test_brush_mode_keeps_every_pen_down(self):
        from promptplot.postprocess import run_pipeline

        cfg = PromptPlotConfig()
        cfg.brush.enabled = True
        cmds = _seg(20, 20, 30, 20) + _seg(30, 20, 30, 30)
        out = run_pipeline(GCodeProgram(commands=cmds), cfg)
        assert sum(c.command == "M3" for c in out.commands) == 2
