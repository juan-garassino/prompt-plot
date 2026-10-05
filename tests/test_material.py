"""The material grammar — how a mark is made, per material.

Constants and invariants come from the reference reconstructions; these tests
lock the behaviours that make each grammar what it is.
"""

import math

import numpy as np
import pytest

from promptplot.generative.engine.geometry import Polygon, polyline_length
from promptplot.generative.engine.material import (
    brush_family,
    cut_tone,
    flow_family,
    gauss_tone,
    hatch_polygon,
    physical_inset,
    physical_spacing,
    shadow_cross,
    suppress_parallel,
    surface_grid,
)
from promptplot.lamina.styles import CUBIST_RULES, PenRule, PenRules, get_style
from promptplot.scene import HatchRule, Mark, Scene, SceneObject, compile_scene

SQUARE = [(0, 0), (40, 0), (40, 40), (0, 40)]
C_SHAPE = [(0, 0), (10, 0), (10, 3), (6, 3), (6, 7), (10, 7), (10, 10), (0, 10)]


# ------------------------------------------------------------- cubist planes


def test_hatch_polygon_fills_a_square_at_the_requested_spacing():
    # edges at .5 so no boundary sits ON a grid line (in practice physical_inset
    # always pulls the hatch inward, so a boundary-coincident line never occurs)
    sq = [(0.5, 0.5), (40.5, 0.5), (40.5, 40.5), (0.5, 40.5)]
    runs = hatch_polygon(sq, spacing=4.0, angle_deg=0.0)
    ys = sorted(round(r[0][1], 6) for r in runs)
    assert ys == [4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0]  # phase-locked to the origin
    assert all(abs(r[0][1] - r[-1][1]) < 1e-9 for r in runs)  # horizontal
    assert all(polyline_length(r) == pytest.approx(40.0) for r in runs)


def test_hatch_polygon_is_phase_locked_across_adjacent_facets():
    left = hatch_polygon([(0, 0), (10, 0), (10, 10), (0, 10)], spacing=3.0, angle_deg=0.0)
    right = hatch_polygon([(10, 0), (20, 0), (20, 10), (10, 10)], spacing=3.0, angle_deg=0.0)
    ly = sorted(round(r[0][1], 6) for r in left)
    ry = sorted(round(r[0][1], 6) for r in right)
    assert ly == ry  # collinear lines across the shared edge


def test_hatch_polygon_respects_concavity_and_angle():
    runs = hatch_polygon(C_SHAPE, spacing=1.0, angle_deg=0.0)
    # a row through the notch (y=5) is a single run x 0..6, not 0..10
    row5 = [r for r in runs if abs(r[0][1] - 5.0) < 1e-6]
    assert len(row5) == 1
    assert max(p[0] for p in row5[0]) == pytest.approx(6.0)
    # an angled fill still lands strictly inside
    diag = hatch_polygon(SQUARE, spacing=3.0, angle_deg=45.0)
    assert diag and all(-1e-6 <= p[0] <= 40 + 1e-6 and -1e-6 <= p[1] <= 40 + 1e-6 for r in diag for p in r)


def test_hatch_polygon_inset_pulls_lines_in_from_the_edge():
    runs = hatch_polygon(SQUARE, spacing=4.0, angle_deg=0.0, inset=2.0)
    xs = [p[0] for r in runs for p in r]
    ys = [p[1] for r in runs for p in r]
    assert min(xs) == pytest.approx(2.0) and max(xs) == pytest.approx(38.0)
    assert min(ys) >= 2.0 - 1e-6 and max(ys) <= 38.0 + 1e-6


def test_physical_floors():
    # 0.10 mm nib on a page where 1 unit = 0.19 mm: floor is 2.4*0.1/0.19 ≈ 1.263 units
    assert physical_spacing(3.0, 0.10, 0.19) == pytest.approx(3.0)
    assert physical_spacing(0.5, 0.10, 0.19) == pytest.approx(2.4 * 0.10 / 0.19)
    assert physical_spacing(3.0, 0.10, 0.19, density=10.0) == pytest.approx(2.4 * 0.10 / 0.19)  # density can't beat it
    # inset: ½·0.5 + ½·0.1 + 0.035 = 0.335 mm → /0.19 units
    assert physical_inset(0.0, 0.5, 0.1, 0.19) == pytest.approx(0.335 / 0.19)
    assert physical_inset(5.0, 0.5, 0.1, 0.19) == pytest.approx(5.0)
    assert shadow_cross({"spacing": 2.0, "angle": 10.0}) == {"spacing": 3.0, "angle": 77.0}


# ------------------------------------------------------------- cut_tone


def _line(n=201, L=100.0):
    return [(L * i / (n - 1), 0.0) for i in range(n)]


def _inked_fraction(runs, L=100.0):
    return sum(polyline_length(r) for r in runs) / L


def test_cut_tone_duty_ramp_and_floors():
    line = _line()
    assert cut_tone(line, 0.06) == []  # at the ramp foot: duty 0 → nothing
    assert cut_tone(line, 0.10) == []  # below the 0.13 ink floor → nothing
    frac_40 = _inked_fraction(cut_tone(line, 0.40, period=10.0))
    assert frac_40 == pytest.approx((0.40 - 0.06) / 0.65, abs=0.06)  # ≈ 0.52 duty
    solid = cut_tone(line, 0.71, period=10.0)
    assert len(solid) == 1 and _inked_fraction(solid) == pytest.approx(1.0)  # continuous at 0.71
    assert len(cut_tone(line, 0.93, period=10.0)) == 1


def test_cut_tone_phase_shifts_the_gaps():
    line = _line()
    a = cut_tone(line, 0.40, period=10.0, phase=0.0)
    b = cut_tone(line, 0.40, period=10.0, phase=2.5)
    assert a[0][0][0] != pytest.approx(b[0][0][0]) or a[0][-1][0] != pytest.approx(b[0][-1][0])


def test_cut_tone_accepts_callable_and_array_tone():
    line = _line()
    by_fn = cut_tone(line, lambda xs, ys: np.where(xs < 50, 0.9, 0.0), period=10.0)
    assert by_fn and max(p[0] for r in by_fn for p in r) <= 50.0 + 1e-6
    arr = np.linspace(0.0, 1.0, len(line))
    by_arr = cut_tone(line, arr, period=10.0)
    assert by_arr and by_arr[-1][-1][0] == pytest.approx(100.0)  # dark end is solid


def test_gauss_tone_form():
    f = gauss_tone(0.2, [(0.5, 0.5, 0.5, 0.1, 0.1), (-0.2, 0.0, 0.0, 0.2, 0.2)])
    u = np.array([0.5, 0.0])
    v = np.array([0.5, 0.0])
    out = f(u, v)
    assert out[0] == pytest.approx(0.7 + -0.2 * math.exp(-0.5 * (6.25 + 6.25)), abs=1e-6)
    assert out[1] == pytest.approx(0.0 + 0.5 * math.exp(-0.5 * (25 + 25)), abs=1e-6)


# ------------------------------------------------------------- flow_family


def test_flow_family_track_count_from_percentile_width():
    a = [(0.0, 0.0), (100.0, 0.0)]
    b = [(0.0, 10.0), (100.0, 10.0)]  # constant 10 apart
    fam = flow_family(a, b, spacing=2.0)
    assert fam.count == 5  # 10 / 2
    assert len(fam.tracks) == 5
    # tracks never coincide with the guides
    ys = sorted(t[0][1] for t in fam.tracks)
    assert ys[0] > 0.0 and ys[-1] < 10.0
    assert all(polyline_length(t) == pytest.approx(100.0, rel=0.02) for t in fam.tracks)


def test_flow_family_pinched_lobe_keeps_density_of_its_fat_part():
    # guide b pinches to meet a at both ends: widths run 0 → 20 → 0
    a = [(x, 0.0) for x in np.linspace(0, 100, 51)]
    b = [(x, 20.0 * math.sin(math.pi * x / 100.0)) for x in np.linspace(0, 100, 51)]
    fam = flow_family(a, b, spacing=2.0)
    # 76th percentile of a half-sine of peak 20 ≈ 20·sin(0.76·π/2)… well above the
    # median; the count must be many, not ~0 as a min-width rule would give
    assert 6 <= fam.count <= 10


def test_flow_family_highlight_breaks_tracks_and_clips_to_region():
    a = [(0.0, 0.0), (100.0, 0.0)]
    b = [(0.0, 10.0), (100.0, 10.0)]
    solid = flow_family(a, b, spacing=2.0)
    lit = flow_family(a, b, spacing=2.0, highlight=True)
    assert len(lit.tracks) > len(solid.tracks)  # the notch splits tracks
    total_lit = sum(polyline_length(t) for t in lit.tracks)
    total_solid = sum(polyline_length(t) for t in solid.tracks)
    assert total_lit < total_solid
    clipped = flow_family(a, b, spacing=2.0, region=Polygon([(20, -5), (60, -5), (60, 15), (20, 15)]))
    assert all(20 - 1e-6 <= p[0] <= 60 + 1e-6 for t in clipped.tracks for p in t)


def test_flow_family_dark_edge_adds_two_rims():
    fam = flow_family([(0, 0), (50, 0)], [(0, 6), (50, 6)], spacing=1.5, dark_edge=True)
    assert len(fam.rims) == 2
    ys = sorted(r[0][1] for r in fam.rims)
    assert ys[0] == pytest.approx(0.15) and ys[1] == pytest.approx(5.85)


def test_brush_family_around_one_guide():
    strokes = brush_family([(0, 0), (50, 0), (100, 10)], n=5, spread=4.0)
    assert len(strokes) == 5
    ys = sorted(s[0][1] for s in strokes)
    assert ys[0] == pytest.approx(-2.0, abs=1e-6) and ys[-1] == pytest.approx(2.0, abs=1e-6)


# ------------------------------------------------------------- surface_grid


def test_surface_grid_rows_stay_inside_and_protect_holes():
    ring = [(0, 0), (60, 0), (60, 80), (0, 80)]
    tone = gauss_tone(0.5, [])
    g = surface_grid(ring, tone, row_spacing=6.0, bend=6.0, protect=[(20, 30, 40, 50)])
    assert g.rows
    pts = [p for r in g.rows for p in r]
    assert all(0.7 - 1e-6 <= x <= 59.3 + 1e-6 and 0.7 - 1e-6 <= y <= 79.3 + 1e-6 for x, y in pts)
    # nothing lands inside the protected ellipse (centre 30,40 radii 10,10)
    assert not any((x - 30) ** 2 / 100 + (y - 40) ** 2 / 100 < 0.98 for x, y in pts)


def test_surface_grid_cross_family_only_in_shadow():
    ring = [(0, 0), (60, 0), (60, 80), (0, 80)]
    light = surface_grid(ring, gauss_tone(0.30, []), row_spacing=6.0, bend=0.0)
    dark = surface_grid(ring, gauss_tone(0.85, []), row_spacing=6.0, bend=0.0)
    assert light.cross == []  # tone 0.30 → (0.30−0.40)·2.7 < 0 → no cross hatch
    assert dark.cross  # tone 0.85 → dense cross family
    # dark rows are SOLID (few long runs); light rows are DASHED (many short runs):
    # more ink in the dark, more pieces in the light
    ink = lambda runs: sum(polyline_length(r) for r in runs)  # noqa: E731
    assert ink(dark.rows) > ink(light.rows)
    assert len(light.rows) > len(dark.rows)


def test_surface_grid_bend_makes_rows_curve():
    ring = [(0, 0), (60, 0), (60, 80), (0, 80)]
    flat = surface_grid(ring, gauss_tone(0.9, []), row_spacing=8.0, bend=0.0, cross=False)
    bent = surface_grid(ring, gauss_tone(0.9, []), row_spacing=8.0, bend=8.0, cross=False)
    span = lambda g: max(max(p[1] for p in r) - min(p[1] for p in r) for r in g.rows)  # noqa: E731
    assert span(flat) < 1e-6
    assert span(bent) > 3.0


# ------------------------------------------------------------- suppress_parallel


def test_suppress_parallel_drops_near_parallel_keeps_crossings():
    a = [(0.0, 0.0), (100.0, 0.0)]
    b = [(0.0, 0.5), (100.0, 0.5)]  # too close AND parallel → dropped
    c = [(50.0, -10.0), (50.0, 10.0)]  # crosses a at a right angle → kept whole
    d = [(0.0, 5.0), (100.0, 5.0)]  # far enough → kept
    kept = suppress_parallel([a, b, c, d], min_dist=1.55, align=0.93)
    total = sum(polyline_length(k) for k in kept)
    assert total == pytest.approx(100 + 20 + 100, rel=0.02)


# ------------------------------------------------------------- PenRules + fills


def test_pen_rules_first_match_wins_separately_for_ink_and_width():
    rules = PenRules(
        ink_rules=(PenRule(r"^queen.*veil", ink="red"), PenRule("", ink="black")),
        width_rules=(PenRule("", role="hatch", width_mm=0.10), PenRule(r"^queen", width_mm=0.48), PenRule("", width_mm=0.24)),
    )
    assert rules.resolve("queen veil plane", "contour") == ("red", 0.48)
    assert rules.resolve("queen veil plane", "hatch") == ("red", 0.10)
    assert rules.resolve("board file 3", "contour") == ("black", 0.24)


def test_cubist_rules_encode_the_reference_semantics():
    # a PLANE is red but only 0.18 — the 0.48 weight is for silhouette-class parts
    assert CUBIST_RULES.resolve("queen veil plane", "contour") == ("red", 0.18)
    assert CUBIST_RULES.resolve("queen face plane", "contour") == ("black", 0.48)
    assert CUBIST_RULES.resolve("king outer cloak", "contour") == ("blue", 0.48)
    assert CUBIST_RULES.resolve("cello body shade", "hatch") == ("yellow", 0.10)
    assert CUBIST_RULES.resolve("board rank 3", "contour") == ("black", 0.16)
    # label-role marks are 0.18 by default (the oracle promotes big type via a
    # text_height field we do not model); the `^title` 0.50 rule is for contour marks
    assert CUBIST_RULES.resolve("title", "label")[1] == 0.18
    assert CUBIST_RULES.resolve("title", "contour")[1] == 0.50
    assert get_style("cubist_plate").rules is CUBIST_RULES


def test_fills_expand_over_cover_with_physical_floors_and_get_occluded():
    plate = SceneObject(
        name="back plane",
        cover=[(0, 0), (100, 0), (100, 100), (0, 100)],
        width_mm=0.5,
        fills=[HatchRule(spacing=10.0, angle=0.0)],
    )
    front = SceneObject(
        name="front block",
        cover=[(30, 30), (70, 30), (70, 70), (30, 70)],
        marks=[Mark(points=[(30, 30), (70, 30), (70, 70), (30, 70), (30, 30)])],
    )
    s = Scene(canvas=(100, 100), paper="a4", widths_mm=[0.1, 0.5], objects=[plate, front])
    cmds, plan = compile_scene(s)
    passes = [p for p in plan if "pen" in p]
    hatch_pass = [p for p in passes if p["width_mm"] == 0.1][0]
    # 10-unit spacing over 100 units → ~11 rows, minus the inset trim; rows at y 40..60
    # cross the front block and split in two → more strokes than rows
    assert hatch_pass["strokes"] > 11
    # the hatch is clipped exactly at the front cover's (eroded) edge: no hatch x in (30.02, 69.98) at y=50
    hatch_ci = hatch_pass["pen"]
    mid_row = [c for c in cmds if c.color == hatch_ci and c.command == "G1"]
    assert mid_row


def test_fills_without_cover_is_rejected():
    with pytest.raises(ValueError):
        SceneObject(name="x", fills=[HatchRule(spacing=2.0)])


def test_compile_uses_style_rules_when_given():
    s = Scene(
        canvas=(100, 100),
        inks={"black": "#111111", "red": "#cb292a", "yellow": "#d6a009", "blue": "#176aab"},
        widths_mm=[0.1, 0.5],
        objects=[
            SceneObject(name="king outer cloak", marks=[Mark(points=[(0, 0), (50, 50)])]),
            SceneObject(name="board rank 1", marks=[Mark(points=[(0, 50), (100, 50)])]),
        ],
    )
    _, plan = compile_scene(s, rules=CUBIST_RULES.as_compile_rules())
    passes = {(p["ink"], p["width_mm"]) for p in plan if "pen" in p}
    assert ("blue", 0.5) in passes  # 0.48 snaps to 0.5
    assert ("black", 0.1) in passes  # 0.16 snaps to 0.1
