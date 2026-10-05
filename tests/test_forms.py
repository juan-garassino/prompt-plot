"""The form vocabulary: rings, nests, dissolve, bursts, ribbons."""

import math

import pytest

from promptplot.generative.engine.forms import (
    close_ring,
    contour_nest,
    dissolve,
    dot_cloud,
    funnel_ring,
    hourglass_ring,
    lobed_ring,
    radial_burst,
    ribbon,
    rounded_rect_ring,
)
from promptplot.generative.engine import forms
from promptplot.generative.engine.geometry import Polygon, polyline_length
from promptplot.generative.rng import SeededRNG


def _bbox(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


# ------------------------------------------------------------------ rings


def test_lobed_ring_has_the_requested_lobes():
    ring = lobed_ring(0, 0, 10, lobes=4, amp=0.3)
    # radius maxima count = lobes
    radii = [math.hypot(x, y) for x, y in ring]
    peaks = sum(
        1
        for i in range(len(radii))
        if radii[i] > radii[i - 1] and radii[i] >= radii[(i + 1) % len(radii)]
    )
    assert peaks == 4
    assert max(radii) == pytest.approx(13.0, rel=1e-3)
    assert min(radii) == pytest.approx(7.0, rel=1e-3)


def test_lobed_ring_wobble_is_seeded_and_differentiating():
    a = lobed_ring(0, 0, 10, wobble=0.15, rng=SeededRNG(1))
    b = lobed_ring(0, 0, 10, wobble=0.15, rng=SeededRNG(1))
    c = lobed_ring(0, 0, 10, wobble=0.15, rng=SeededRNG(2))
    assert a == b  # same seed → same blob
    assert a != c  # different seed → a sibling, not a clone


def test_hourglass_pinches_at_the_waist():
    ring = hourglass_ring(0, 0, 100, 60, 12)
    at_centre = [y for x, y in ring if abs(x) < 1.0]
    at_end = [y for x, y in ring if abs(x) > 49.0]
    assert max(at_centre) - min(at_centre) == pytest.approx(12.0, abs=0.5)
    assert max(at_end) - min(at_end) == pytest.approx(60.0, abs=1.0)


def test_funnel_narrows_from_mouth_to_tip():
    ring = funnel_ring(0, 0, 40, 0, 30, 6, bow=0.0)
    left = [y for x, y in ring if x < 1.0]
    right = [y for x, y in ring if x > 39.0]
    assert max(left) - min(left) == pytest.approx(30.0, abs=0.5)
    assert max(right) - min(right) == pytest.approx(6.0, abs=0.5)


def test_rounded_rect_stays_in_bounds_and_closes():
    ring = rounded_rect_ring(0, 0, 40, 20, r=5)
    x0, y0, x1, y1 = _bbox(ring)
    assert (x0, y0, x1, y1) == pytest.approx((0, 0, 40, 20), abs=1e-6)
    closed = close_ring(ring)
    assert closed[0] == closed[-1]


# ------------------------------------------------------------------ nests


def test_contour_nest_is_nested_and_shrinking():
    ring = lobed_ring(0, 0, 20, lobes=4, amp=0.25)
    nest = contour_nest(ring, n=8)
    assert len(nest) == 8
    areas = []
    for r in nest:
        x0, y0, x1, y1 = _bbox(r)
        areas.append((x1 - x0) * (y1 - y0))
    assert areas == sorted(areas, reverse=True)  # each ring inside the last
    assert all(r[0] == r[-1] for r in nest)  # all closed


def test_contour_nest_step_controls_physical_spacing():
    ring = rounded_rect_ring(0, 0, 60, 60)
    nest = contour_nest(ring, n=5, step=3.0)
    assert len(nest) == 5  # not vacuous: every requested ring must exist
    # a cornered polygon keeps its edges parallel — each ring inset 3 mm per side
    widths = [(_bbox(r)[2] - _bbox(r)[0]) for r in nest]
    gaps = [a - b for a, b in zip(widths, widths[1:])]
    assert len(gaps) == 4
    assert all(g == pytest.approx(6.0, abs=1e-6) for g in gaps)


def test_smoothness_is_detected_from_the_geometry():
    from promptplot.generative.engine.forms import _is_smooth

    assert _is_smooth(lobed_ring(0, 0, 20, lobes=4))  # sampled curve
    assert _is_smooth(hourglass_ring(0, 0, 100, 60, 12))
    assert not _is_smooth(rounded_rect_ring(0, 0, 60, 60))  # 4 hard corners
    assert not _is_smooth([(0, 0), (10, 0), (10, 10), (0, 10)])


def test_nest_perimeters_shrink_inward():
    """The spike test that matters. A ring INSIDE another cannot be longer than
    it; a folding/spiking offset shows up as a perimeter that grows. (Angle is
    the wrong metric — offsetting past the curvature radius yields a genuine
    cusp, and smoothing only redistributes one.)"""
    for amp in (0.15, 0.30):
        nest = contour_nest(lobed_ring(0, 0, 40, lobes=4, amp=amp), n=12)
        assert len(nest) >= 6
        lens = [polyline_length(r) for r in nest]
        for a, b in zip(lens, lens[1:]):
            assert b <= a * 1.02


def test_max_erode_matches_the_shapes_real_limit():
    from promptplot.generative.engine.forms import max_erode

    # a disc can be eroded to its radius; a deep clover collapses at its
    # valleys' concave curvature, far sooner than its 28 mm inradius
    disc = max_erode(lobed_ring(0, 0, 40, lobes=4, amp=0.0))
    clover = max_erode(lobed_ring(0, 0, 40, lobes=4, amp=0.30))
    assert disc == pytest.approx(40.0, rel=0.15)
    assert 2.0 < clover < 20.0
    assert clover < disc


def test_contour_nest_stops_instead_of_folding_inside_out():
    ring = rounded_rect_ring(0, 0, 10, 10)
    nest = contour_nest(ring, n=50, step=1.0)  # would collapse well before 50
    assert 1 <= len(nest) < 50
    for r in nest:
        x0, y0, x1, y1 = _bbox(r)
        assert x1 > x0 and y1 > y0  # nothing inverted


# ------------------------------------------------------------------ dissolve


def test_dissolve_t0_is_the_nest_untouched():
    nest = contour_nest(lobed_ring(0, 0, 20), n=6)
    assert dissolve(nest, 0.0, SeededRNG(1)) == [list(p) for p in nest]


def test_dissolve_breaks_then_shrinks_then_scatters():
    nest = contour_nest(lobed_ring(0, 0, 25, lobes=4), n=10)
    solid = sum(polyline_length(p) for p in nest)
    mid = dissolve(nest, 0.35, SeededRNG(2))
    late = dissolve(nest, 0.85, SeededRNG(2))
    ink_mid = sum(polyline_length(p) for p in mid)
    ink_late = sum(polyline_length(p) for p in late)
    assert len(mid) > len(nest)  # rings broken into many dashes
    assert ink_mid < solid  # gaps opened
    assert ink_late < ink_mid  # dashes shrank toward dots
    # late marks are short: the ring structure is gone
    assert max(polyline_length(p) for p in late) < max(polyline_length(p) for p in mid)


def test_dissolve_scatter_pushes_marks_off_their_ring():
    nest = contour_nest(lobed_ring(0, 0, 20), n=6)
    tight = dissolve(nest, 0.8, SeededRNG(3), scatter=0.0)
    loose = dissolve(nest, 0.8, SeededRNG(3), scatter=8.0)
    assert _bbox([p for poly in loose for p in poly])[2] > _bbox([p for poly in tight for p in poly])[2]


def test_dissolve_is_deterministic():
    nest = contour_nest(lobed_ring(0, 0, 20), n=6)
    assert dissolve(nest, 0.5, SeededRNG(9)) == dissolve(nest, 0.5, SeededRNG(9))


# ------------------------------------------------------------------ clouds / bursts


def test_dot_cloud_is_isotropic_and_dot_sized():
    dots = dot_cloud(0, 0, 20, 400, SeededRNG(4), dot=0.4, falloff=0.0)
    assert len(dots) == 400
    assert all(polyline_length(d) == pytest.approx(0.4) for d in dots)
    xs = [d[0][0] for d in dots]
    ys = [d[0][1] for d in dots]
    # no preferred direction: x and y spreads match
    assert abs(max(xs) - max(ys)) < 6.0
    assert all(math.hypot(x, y) <= 20.0 + 1e-6 for x, y in [(d[0][0], d[0][1]) for d in dots])


def test_dot_cloud_falloff_concentrates_the_centre():
    flat = dot_cloud(0, 0, 20, 500, SeededRNG(5), falloff=0.0)
    peaked = dot_cloud(0, 0, 20, 500, SeededRNG(5), falloff=2.0)
    mean_r = lambda c: sum(math.hypot(d[0][0], d[0][1]) for d in c) / len(c)  # noqa: E731
    assert mean_r(peaked) < mean_r(flat)


def test_radial_burst_dashes_lengthen_outward_and_clip_to_a_panel():
    rays = radial_burst(0, 0, 20, 24, SeededRNG(6))
    assert rays
    near = [polyline_length(s) for s in rays if math.hypot(*s[0]) < 6]
    far = [polyline_length(s) for s in rays if math.hypot(*s[0]) > 14]
    assert sum(near) / len(near) < sum(far) / len(far)

    panel = Polygon([(-8, -8), (8, -8), (8, 8), (-8, 8)])
    clipped = radial_burst(0, 0, 20, 24, SeededRNG(6), region=panel)
    assert all(-8 - 1e-6 <= x <= 8 + 1e-6 and -8 - 1e-6 <= y <= 8 + 1e-6 for s in clipped for x, y in s)


# ------------------------------------------------------------------ ribbons


def test_ribbon_connects_endpoints_and_bows():
    (curve,) = ribbon((0, 0), (100, 0), n=1, bow=0.2)
    assert curve[0] == pytest.approx((0.0, 0.0))
    assert curve[-1] == pytest.approx((100.0, 0.0))
    assert max(abs(y) for _, y in curve) > 5.0  # actually bowed
    straight = ribbon((0, 0), (100, 0), n=1, bow=0.0)[0]
    assert max(abs(y) for _, y in straight) < 1e-9


def test_ribbon_fans_n_curves_across_spread():
    fan = ribbon((0, 0), (100, 0), n=5, bow=0.1, spread=20.0)
    assert len(fan) == 5
    offsets = sorted(c[0][1] for c in fan)
    assert offsets[0] == pytest.approx(-10.0)
    assert offsets[-1] == pytest.approx(10.0)


def test_radial_nest_fills_all_the_way_in_where_offsetting_cannot():
    """The two nesting rules, and why both exist. A deep clover can only be
    OFFSET as far as its valleys' curvature, so contour_nest piles its rings in
    a band near the rim; radial_nest scales and reaches the centre."""
    from promptplot.generative.engine.forms import max_erode, radial_nest

    ring = lobed_ring(0, 0, 40, lobes=4, amp=0.30)
    assert max_erode(ring) < 24.0  # short of the 28 mm inradius: the valleys go first

    offset_nest = contour_nest(ring, n=14)
    scaled = radial_nest(ring, n=14, inner=0.10)
    assert len(scaled) == 14  # scaling never folds, so every ring exists

    def inmost(nest):
        return min(math.hypot(x, y) for r in nest for x, y in r)

    assert inmost(scaled) < 4.0  # reaches the centre
    assert inmost(offset_nest) > 10.0  # leaves a hollow middle


def test_radial_nest_is_self_similar_and_gamma_biases_spacing():
    from promptplot.generative.engine.forms import radial_nest

    ring = lobed_ring(10, -5, 30, lobes=3, amp=0.2)
    nest = radial_nest(ring, n=6, inner=0.2)
    areas = []
    for r in nest:
        x0, y0, x1, y1 = _bbox(r)
        areas.append((x1 - x0) * (y1 - y0))
    assert areas == sorted(areas, reverse=True)
    assert all(r[0] == r[-1] for r in nest)

    rim = radial_nest(ring, n=8, inner=0.1, gamma=2.0)
    mid = radial_nest(ring, n=8, inner=0.1, gamma=1.0)
    span = lambda n, k: _bbox(n[k])[2] - _bbox(n[k])[0]  # noqa: E731
    assert span(rim, 4) > span(mid, 4)  # gamma>1 bunches contours at the rim


# ---------------------------------------------------------------------------
# field_nest — the rule that holds a constant PHYSICAL gap
# ---------------------------------------------------------------------------
def _nearest_gaps(nest):
    """For every point on every ring, the distance to the nearest other ring."""
    import numpy as np

    arrs = [np.asarray(p, float) for p in nest]
    out = []
    for i, A in enumerate(arrs):
        d = np.full(len(A), 1e9)
        for j, B in enumerate(arrs):
            if i == j:
                continue
            dd = np.hypot(A[:, None, 0] - B[None, :, 0],
                          A[:, None, 1] - B[None, :, 1]).min(axis=1)
            d = np.minimum(d, dd)
        out.append(d)
    return np.concatenate(out)


def test_field_nest_holds_the_pitch_where_radial_nest_collapses():
    """The regression that turned a mass into a blot.

    ``radial_nest`` scales about the centroid, so on a lobed shape its gap runs
    with the local radius — at 26 rings the closest ink measured 0.66 mm, under
    every pen tip we own, and the mass filled solid. ``field_nest`` walks level
    sets of the distance field, so the gap is the pitch everywhere.
    """
    ring = forms.lobed_ring(0, 0, 40, lobes=4, amp=0.30, phase=0.0)

    gaps = _nearest_gaps(forms.field_nest(ring, pitch=2.5))
    assert gaps.min() > 2.0, f"field_nest closed to {gaps.min():.2f} mm"
    assert gaps.max() < 3.2, f"field_nest opened to {gaps.max():.2f} mm"

    bad = _nearest_gaps(forms.radial_nest(ring, n=26, inner=0.06, gamma=0.8))
    assert bad.min() < 1.0, "radial_nest is expected to collapse here"


def test_field_nest_pitch_is_physical():
    ring = forms.lobed_ring(0, 0, 40, lobes=4, amp=0.20)
    fine = forms.field_nest(ring, pitch=2.0)
    coarse = forms.field_nest(ring, pitch=4.0)
    assert len(fine) > len(coarse)
    # Halving the pitch must not halve the reach: both run to the medial axis.
    assert _nearest_gaps(coarse).min() > 3.2


def test_field_nest_reaches_the_centre_of_a_concave_shape():
    """``contour_nest`` cannot: an inward offset dies at the tightest valley."""
    ring = forms.lobed_ring(0, 0, 40, lobes=4, amp=0.30)
    nest = forms.field_nest(ring, pitch=2.5)
    innermost = min(
        max(math.hypot(x, y) for x, y in poly) for poly in nest
    )
    assert innermost < 6.0, f"nest stops {innermost:.1f} mm short of the centre"


def test_field_nest_caps_ring_count_with_n():
    ring = forms.lobed_ring(0, 0, 40, lobes=4, amp=0.20)
    assert len(forms.field_nest(ring, pitch=1.5, n=4)) <= 4


def test_field_nest_rejects_degenerate_input():
    assert forms.field_nest([(0.0, 0.0), (1.0, 1.0)], pitch=1.0) == []
    ring = forms.lobed_ring(0, 0, 10, lobes=3, amp=0.1)
    assert forms.field_nest(ring, pitch=0.0) == []
