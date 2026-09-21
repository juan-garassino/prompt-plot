"""Polygon region + Bezier + arc-length resampling — the scene-compiler foundation.

These lock the exactness claim: a polyline clipped against a concave facet stops
ON the facet edge, a Union of Polygons occludes like a cover stack, and the Bezier
flattening reproduces the oracle drawings' step rule.
"""

import math

import pytest

from promptplot.generative.engine.geometry import (
    Polygon,
    Union,
    bezier_flatten,
    clip,
    polyline_length,
    resample_by_arclength,
)

# a "C" shape: 10x10 square with a 4-wide notch cut from the right side
C_SHAPE = [(0, 0), (10, 0), (10, 3), (6, 3), (6, 7), (10, 7), (10, 10), (0, 10)]


def test_concave_contains():
    c = Polygon(C_SHAPE)
    assert c.contains(2, 5)  # body
    assert c.contains(8, 1.5)  # lower arm
    assert c.contains(8, 8.5)  # upper arm
    assert not c.contains(8, 5)  # inside the notch = outside the polygon
    assert not c.contains(11, 5)
    assert not c.contains(-1, 5)


def test_closed_ring_is_accepted_and_deduped():
    a = Polygon(C_SHAPE)
    b = Polygon(C_SHAPE + [C_SHAPE[0]])
    assert len(a.pts) == len(b.pts) == 8


def test_clip_polyline_against_concave_polygon_is_exact():
    c = Polygon(C_SHAPE)
    # horizontal line through the notch: inside 0..6, outside 6..10 (the notch), never re-enters
    kept = clip([(-2, 5), (12, 5)], c, keep="inside")
    assert len(kept) == 1
    (a, b), = [(run[0], run[-1]) for run in kept]
    assert a == pytest.approx((0.0, 5.0), abs=1e-9)
    assert b == pytest.approx((6.0, 5.0), abs=1e-9)  # stops ON the notch wall

    # horizontal line through the lower arm: inside the whole 0..10 span
    kept = clip([(-2, 1.5), (12, 1.5)], c, keep="inside")
    assert len(kept) == 1
    assert kept[0][0] == pytest.approx((0.0, 1.5), abs=1e-9)
    assert kept[0][-1] == pytest.approx((10.0, 1.5), abs=1e-9)


def test_clip_outside_keeps_the_complement():
    c = Polygon(C_SHAPE)
    out = clip([(-2, 5), (12, 5)], c, keep="outside")
    spans = sorted((round(r[0][0], 6), round(r[-1][0], 6)) for r in out)
    assert spans == [(-2.0, 0.0), (6.0, 12.0)]


def test_union_of_polygons_occludes_like_a_cover_stack():
    front = Polygon([(3, 3), (7, 3), (7, 7), (3, 7)])
    other = Polygon([(8, 8), (9, 8), (9, 9), (8, 9)])
    covered = Union(front, other)
    # a back object's hatch line crossing the front cover loses exactly the covered span
    visible = clip([(0, 5), (10, 5)], covered, keep="outside")
    spans = sorted((round(r[0][0], 6), round(r[-1][0], 6)) for r in visible)
    assert spans == [(0.0, 3.0), (7.0, 10.0)]


def test_segment_entirely_inside_and_entirely_outside():
    sq = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    assert sq.inside_intervals((2, 2), (8, 8)) == [(0.0, 1.0)]
    assert sq.inside_intervals((12, 2), (18, 8)) == []


def test_bezier_flatten_step_rule_and_endpoints():
    ctrl = [(0.0, 0.0), (10.0, 20.0), (30.0, 20.0), (40.0, 0.0)]
    hull = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(ctrl, ctrl[1:]))
    pts = bezier_flatten(ctrl, max_seg=2.0)
    assert len(pts) == max(8, math.ceil(hull / 2.0)) + 1
    assert pts[0] == pytest.approx(ctrl[0])
    assert pts[-1] == pytest.approx(ctrl[-1])
    # symmetric control polygon → curve mirrors about x = 20 sample-for-sample
    for k in range(len(pts)):
        assert pts[k][0] + pts[-1 - k][0] == pytest.approx(40.0, abs=1e-9)
        assert pts[k][1] == pytest.approx(pts[-1 - k][1], abs=1e-9)


def test_bezier_flatten_quadratic_and_minimum_steps():
    pts = bezier_flatten([(0, 0), (1, 1), (2, 0)], max_seg=2.0)
    assert len(pts) == 9  # tiny curve still gets the 8-step floor
    assert pts[4] == pytest.approx((1.0, 0.5))


def test_bezier_flatten_rejects_wrong_arity():
    with pytest.raises(ValueError):
        bezier_flatten([(0, 0), (1, 1)])


def test_resample_by_n_keeps_endpoints_and_spacing():
    poly = [(0, 0), (10, 0), (10, 10)]  # length 20, corner at 10
    pts = resample_by_arclength(poly, n=5)
    assert len(pts) == 5
    assert pts[0] == (0, 0) and pts[-1] == (10, 10)
    assert pts[2] == pytest.approx((10.0, 0.0))  # the midpoint of the arc is the corner
    gaps = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    assert all(g == pytest.approx(5.0) for g in gaps)


def test_resample_by_step():
    poly = [(0, 0), (30, 0)]
    pts = resample_by_arclength(poly, step=7.0)
    assert len(pts) == math.ceil(30 / 7.0) + 1
    assert polyline_length(pts) == pytest.approx(30.0)


def test_two_guides_resampled_to_same_n_correspond_by_fraction():
    a = resample_by_arclength([(0, 0), (100, 0)], n=11)
    b = resample_by_arclength([(0, 10), (50, 10)], n=11)
    for k in range(11):
        assert a[k][0] == pytest.approx(10.0 * k)
        assert b[k][0] == pytest.approx(5.0 * k)
