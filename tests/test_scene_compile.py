"""Scene model, both occlusion walks, and the compiler — the Phase 1 foundation.

Stub-free: everything here is pure geometry in, GCode out.
"""

import json

import pytest

from promptplot.config import PromptPlotConfig
from promptplot.scene import (
    Mark,
    Scene,
    SceneObject,
    compile_scene,
    compile_to_program,
    cover_walk,
    erode_ring,
    paint_walk,
)


def _square(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _hatch_rows(x0, x1, ys):
    return [Mark(role="hatch", points=[(x0, y), (x1, y)]) for y in ys]


def _two_object_scene(**kw):
    """A back plate hatched edge-to-edge, and a front square sitting on it."""
    back = SceneObject(
        name="back plate",
        cover=_square(0, 0, 100, 100),
        marks=[Mark(role="contour", points=_square(0, 0, 100, 100) + [(0, 0)])]
        + _hatch_rows(0, 100, [20, 40, 50, 60, 80]),
    )
    front = SceneObject(
        name="front square",
        cover=_square(30, 30, 70, 70),
        ink="red",
        width_mm=0.5,
        marks=[Mark(role="contour", points=_square(30, 30, 70, 70) + [(30, 30)])],
    )
    return Scene(
        canvas=(100, 100),
        paper="a4",
        inks={"black": "#111111", "red": "#cb292a"},
        widths_mm=[0.1, 0.5],
        objects=[back, front],
        **kw,
    )


# ---------------------------------------------------------------- models


def test_scene_json_round_trip():
    s = _two_object_scene(title="round trip")
    js = s.model_dump_json()
    s2 = Scene.model_validate_json(js)
    assert s2 == s
    assert json.loads(js)["objects"][1]["name"] == "front square"


def test_unknown_ink_or_stage_is_rejected():
    with pytest.raises(ValueError):
        Scene(canvas=(10, 10), objects=[SceneObject(name="x", ink="chartreuse")])
    with pytest.raises(ValueError):
        Scene(canvas=(10, 10), objects=[SceneObject(name="x", stage="varnish")])


def test_width_snaps_to_nearest_available():
    s = Scene(canvas=(10, 10), widths_mm=[0.5, 0.1, 0.25])
    assert s.widths_mm == [0.1, 0.25, 0.5]
    assert s.snap_width(0.18) == 0.25
    assert s.snap_width(0.4) == 0.5
    assert s.snap_width(None) == 0.1


# ---------------------------------------------------------------- cover walk


def test_erode_ring_moves_inward_regardless_of_winding():
    ccw = _square(0, 0, 10, 10)
    cw = list(reversed(ccw))
    for ring in (ccw, cw):
        e = erode_ring(ring, 1.0)
        xs = [p[0] for p in e]
        ys = [p[1] for p in e]
        assert min(xs) == pytest.approx(1.0) and max(xs) == pytest.approx(9.0)
        assert min(ys) == pytest.approx(1.0) and max(ys) == pytest.approx(9.0)


def test_cover_walk_hides_back_hatch_under_front_cover_but_not_its_outline():
    s = _two_object_scene()
    out = cover_walk(s)
    by_obj = {}
    for idx, m, runs in out:
        by_obj.setdefault(idx, []).append((m.role, runs))

    back_hatch = [runs for role, runs in by_obj[0] if role == "hatch"]
    # rows at y=20 and y=80 miss the front square: one full run each
    # rows at y=40,50,60 cross it: split into two runs, ending ON x=30 and starting ON x=70
    split = [runs for runs in back_hatch if len(runs) == 2]
    whole = [runs for runs in back_hatch if len(runs) == 1]
    assert len(split) == 3 and len(whole) == 2
    for runs in split:
        (a, b) = sorted(runs, key=lambda r: r[0][0])
        assert a[-1][0] == pytest.approx(30.0, abs=0.02)  # eroded cover: 0.01 inside
        assert b[0][0] == pytest.approx(70.0, abs=0.02)

    # the front square's own outline survives its own cover intact
    front_contour = [runs for role, runs in by_obj[1] if role == "contour"]
    assert len(front_contour) == 1 and len(front_contour[0]) == 1
    assert len(front_contour[0][0]) == 5

    # the back plate's outline is not hidden by the front square (it does not cross it)
    back_contour = [runs for role, runs in by_obj[0] if role == "contour"]
    assert len(back_contour[0]) == 1


def test_cover_walk_labels_are_protected_from_hatch_only():
    label = SceneObject(
        name="title",
        marks=[Mark(role="label", points=[(45, 48), (55, 48), (55, 52), (45, 52)])],
    )
    plate = SceneObject(
        name="plate",
        cover=_square(0, 0, 100, 100),
        marks=_hatch_rows(0, 100, [50]) + [Mark(role="contour", points=[(0, 50), (100, 50)])],
    )
    s = Scene(canvas=(100, 100), objects=[plate, label])
    out = cover_walk(s, label_pad=2.0)
    hatch_runs = [runs for _, m, runs in out if m.role == "hatch"][0]
    contour_runs = [runs for _, m, runs in out if m.role == "contour"][0]
    assert len(hatch_runs) == 2  # cut around the label box (43..57)
    assert hatch_runs[0][-1][0] == pytest.approx(43.0)
    assert hatch_runs[1][0][0] == pytest.approx(57.0)
    assert len(contour_runs) == 1  # contours never yield to labels


# ---------------------------------------------------------------- paint walk


def test_paint_walk_culls_fully_covered_and_keeps_partly_covered():
    thin_under = (0.9, [(10.0, 10.0), (30.0, 10.0)])
    fat_over = (4.0, [(5.0, 10.0), (35.0, 10.0)])  # painted later, fully covers the thin one
    thin_partial = (0.9, [(20.0, 5.0), (20.0, 40.0)])  # crosses the fat one, sticks out both sides
    lone = (0.9, [(60.0, 60.0), (70.0, 60.0)])
    keep = paint_walk([thin_under, thin_partial, lone, fat_over])
    assert keep == [False, True, True, True]


def test_paint_walk_order_matters():
    a = (0.9, [(10.0, 10.0), (30.0, 10.0)])
    b = (4.0, [(5.0, 10.0), (35.0, 10.0)])
    assert paint_walk([a, b]) == [False, True]  # b painted after a → a hidden
    assert paint_walk([b, a]) == [True, True]  # a painted after b → a on top, both visible


# ---------------------------------------------------------------- compiler


def test_compile_passes_ordered_fine_before_broad_and_pen_plan_matches():
    s = _two_object_scene()
    cmds, plan = compile_scene(s)
    passes = [p for p in plan if "pen" in p]
    assert [(p["ink"], p["width_mm"]) for p in passes] == [("black", 0.1), ("red", 0.5)]
    assert passes[0]["strokes"] == 1 + 2 + 3 * 2  # contour + 2 whole rows + 3 split rows
    assert passes[1]["strokes"] == 1
    # every M3 carries its pass index, and pass 0 is emitted before pass 1
    colors = [c.color for c in cmds if c.command == "M3"]
    assert colors == sorted(colors)
    assert set(colors) == {0, 1}


def test_compile_is_byte_stable():
    s = _two_object_scene()
    a, pa = compile_scene(s)
    b, pb = compile_scene(s)
    assert [c.model_dump() for c in a] == [c.model_dump() for c in b]
    assert pa == pb


def test_compile_maps_source_units_to_paper_mm_with_y_flip():
    s = Scene(
        canvas=(100, 200),
        paper="a4",
        orientation="portrait",
        margin_mm=10.0,
        objects=[SceneObject(name="l", marks=[Mark(points=[(0, 0), (100, 0)])])],
    )
    cmds, _ = compile_scene(s)
    pts = [(c.x, c.y) for c in cmds if c.x is not None]
    # a4 portrait 210x297, margin 10 → scale = min(190/100, 277/200) = 1.385; centred
    scale = min(190 / 100, 277 / 200)
    off_x = (210 - 100 * scale) / 2
    off_y = (297 - 200 * scale) / 2
    # source y=0 is the TOP → lands at the highest paper y
    assert pts[0] == pytest.approx((off_x, off_y + 200 * scale), abs=1e-3)
    assert pts[1] == pytest.approx((off_x + 100 * scale, off_y + 200 * scale), abs=1e-3)


def test_compile_dedups_exact_duplicates_widest_wins():
    line = [(0, 50), (100, 50)]
    s = Scene(
        canvas=(100, 100),
        widths_mm=[0.1, 0.5],
        objects=[
            SceneObject(name="fine", width_mm=0.1, marks=[Mark(points=line)]),
            SceneObject(name="bold", width_mm=0.5, marks=[Mark(points=line)]),
        ],
    )
    _, plan = compile_scene(s)
    passes = [p for p in plan if "pen" in p]
    assert [(p["width_mm"], p["strokes"]) for p in passes] == [(0.5, 1)]


def test_compile_paint_grammar_orders_by_stage_and_culls_hidden():
    s = Scene(
        canvas=(100, 100),
        inks={"navy": "#172c38", "ochre": "#caa047"},
        widths_mm=[0.9, 1.8, 4.0],
        stages=["underpainting", "body", "accents"],
        occlusion="paint",
        objects=[
            SceneObject(
                name="sky mass",
                ink="navy",
                stage="underpainting",
                width_mm=4.0,
                marks=[Mark(points=[(10, 50), (90, 50)])],
            ),
            SceneObject(
                name="buried accent",
                ink="ochre",
                stage="accents",
                width_mm=0.9,
                # drawn BEFORE (declared earlier than) the later underpainting below? no — stage
                # order puts accents last, so this stays visible
                marks=[Mark(points=[(20, 50), (40, 50)])],
            ),
            SceneObject(
                name="second sky mass",
                ink="ochre",
                stage="underpainting",
                width_mm=4.0,
                marks=[Mark(points=[(10, 50), (90, 50)])],
            ),
        ],
    )
    cmds, plan = compile_scene(s)
    passes = [p for p in plan if "pen" in p]
    # the navy 4mm stroke lies exactly under the later ochre 4mm stroke → culled,
    # and a pass with nothing left in it is NOT emitted (no empty layers)
    culled = [p for p in plan if "culled_hidden_strokes" in p]
    assert culled and culled[0]["culled_hidden_strokes"] == 1
    assert [(p["stage"], p["ink"], p["strokes"]) for p in passes] == [
        ("underpainting", "ochre", 1),
        ("accents", "ochre", 1),
    ]
    # stage order dominates: the accent is drawn AFTER the underpainting
    colors = [c.color for c in cmds if c.command == "M3"]
    assert colors == [0, 1]


def test_compile_to_program_sets_palette_from_pen_plan():
    s = _two_object_scene(title="plate")
    cfg = PromptPlotConfig()
    prog, plan = compile_to_program(s, cfg)
    assert cfg.color.enabled is True
    assert cfg.color.palette == ["#111111", "#cb292a"]
    assert prog.metadata["scene_title"] == "plate"
    assert any(c.command == "G1" for c in prog.commands)
