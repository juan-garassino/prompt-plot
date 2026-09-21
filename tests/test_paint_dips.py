"""Multi-paint brush reloads: one well per colour, count restarts at each swap."""

from promptplot.config import BrushConfig
from promptplot.models import GCodeCommand, GCodeProgram
from promptplot.postprocess import insert_paint_dips


def _stroke(color, x):
    return [
        GCodeCommand(command="G0", x=x, y=0.0),
        GCodeCommand(command="M3", s=1000, color=color),
        GCodeCommand(command="G1", x=x + 1.0, y=0.0, f=1000, color=color),
        GCodeCommand(command="M5"),
    ]


def _dips(cmds):
    """(x, y) of every reload travel, in order."""
    out = []
    for i, c in enumerate(cmds):
        if c.comment == "dip into ink":
            g0 = cmds[i - 1]
            out.append((g0.x, g0.y))
    return out


def test_dips_go_to_the_current_colours_well():
    cfg = BrushConfig(
        enabled=True,
        strokes_before_reload=2,
        charge_position=(1.0, 1.0),
        charge_positions={0: (100.0, 5.0), 1: (200.0, 5.0)},
    )
    cmds = []
    for k in range(4):
        cmds += _stroke(0, k * 10.0)  # 4 strokes of colour 0 → reloads before #2 and #4
    for k in range(4):
        cmds += _stroke(1, k * 10.0)  # 4 strokes of colour 1 → same, at ITS well
    out = insert_paint_dips(GCodeProgram(commands=cmds), cfg)
    assert _dips(out.commands) == [(100.0, 5.0), (100.0, 5.0), (200.0, 5.0), (200.0, 5.0)]
    assert out.metadata["brush_reloads"] == 4


def test_count_restarts_at_a_colour_swap():
    cfg = BrushConfig(enabled=True, strokes_before_reload=3, charge_position=(9.0, 9.0))
    cmds = []
    cmds += _stroke(0, 0.0)
    cmds += _stroke(0, 10.0)  # 2 strokes of colour 0: no reload yet
    cmds += _stroke(1, 20.0)  # swap → count restarts at 1
    cmds += _stroke(1, 30.0)
    cmds += _stroke(1, 40.0)  # 3rd of colour 1 → reload here
    out = insert_paint_dips(GCodeProgram(commands=cmds), cfg)
    assert out.metadata["brush_reloads"] == 1
    # the reload sits right before the 5th stroke's M3, not after the 3rd overall
    m3s = [i for i, c in enumerate(out.commands) if c.command == "M3"]
    dip_idx = [i for i, c in enumerate(out.commands) if c.comment == "dip into ink"][0]
    assert m3s[3] < dip_idx < m3s[4]


def test_colour_without_a_well_falls_back_to_the_default():
    cfg = BrushConfig(enabled=True, strokes_before_reload=1, charge_position=(7.0, 8.0), charge_positions={3: (50.0, 50.0)})
    out = insert_paint_dips(GCodeProgram(commands=_stroke(2, 0.0) + _stroke(3, 0.0)), cfg)
    assert _dips(out.commands) == [(7.0, 8.0), (50.0, 50.0)]


def test_from_dict_parses_wells():
    cfg = BrushConfig.from_dict(
        {"enabled": True, "charge_position": [1, 2], "charge_positions": {"0": {"x": 10, "y": 20}, "4": [30, 40]}}
    )
    assert cfg.charge_position == (1.0, 2.0)
    assert cfg.charge_positions == {0: (10.0, 20.0), 4: (30.0, 40.0)}
    assert cfg.well_for(4) == (30.0, 40.0)
    assert cfg.well_for(9) == (1.0, 2.0)
    assert cfg.well_for(None) == (1.0, 2.0)
