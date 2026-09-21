"""Painterly substrate: image grid, palette quantisation, flow strokes.

Needs Pillow (the ``vision`` extra); skipped otherwise, like test_generative's
image tests.
"""

import math

import numpy as np
import pytest

PIL = pytest.importorskip("PIL.Image")

from promptplot.generative.engine.geometry import Polygon  # noqa: E402
from promptplot.generative.engine.material import (  # noqa: E402
    flow_strokes,
    load_image_grid,
    quantize_palette,
    snap_color,
)
from promptplot.generative.rng import SeededRNG  # noqa: E402


def _stripes(tmp_path, w=120, h=80):
    """Vertical stripes, red on the left half and blue on the right: a strong
    horizontal-gradient field whose contour tangent is VERTICAL."""
    img = PIL.new("RGB", (w, h))
    px = img.load()
    for x in range(w):
        for y in range(h):
            dark = (x // 6) % 2 == 0
            base = (200, 30, 30) if x < w // 2 else (30, 60, 200)
            px[x, y] = tuple(int(v * (0.35 if dark else 1.0)) for v in base)
    p = tmp_path / "stripes.png"
    img.save(p)
    return p


def test_load_image_grid_covers_bounds_and_flips_to_paper_up(tmp_path):
    p = _stripes(tmp_path)
    g = load_image_grid(str(p), (10.0, 20.0, 130.0, 100.0), cell=4.0)  # 120x80 mm, landscape like the image
    assert (g.gw, g.gh) == (30, 20)
    assert g.rgb.shape == (20, 30, 3) and g.tone.shape == (20, 30)
    # left half red, right half blue, in paper coordinates
    r, gg, b = g.rgb_at(15.0, 60.0)
    assert r > b
    r, gg, b = g.rgb_at(125.0, 60.0)
    assert b > r
    # cell lookup clamps at the edges
    assert g.cell_of(-100, -100) == (0, 0)
    assert g.cell_of(1e6, 1e6) == (29, 19)


def test_orientation_field_follows_the_stripes(tmp_path):
    p = _stripes(tmp_path)
    g = load_image_grid(str(p), (0.0, 0.0, 120.0, 80.0), cell=2.0)
    # stripes run vertically → contour tangent ≈ ±90°, coherence high
    angs = [abs(math.sin(g.tangent(i, j))) for j in range(3, g.gh - 3) for i in range(3, g.gw - 3)]
    cohs = [g.coherence(i, j) for j in range(3, g.gh - 3) for i in range(3, g.gw - 3)]
    assert np.median(angs) > 0.9
    assert np.median(cohs) > 0.5


def test_quantize_palette_finds_the_two_families_and_sorts_dark_to_light(tmp_path):
    p = _stripes(tmp_path)
    g = load_image_grid(str(p), (0.0, 0.0, 120.0, 80.0), cell=2.0)
    pal = quantize_palette(g.rgb, k=4)
    assert len(pal) == 4
    lum = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in pal]
    assert lum == sorted(lum)
    reds = [c for c in pal if c[0] > c[2]]
    blues = [c for c in pal if c[2] > c[0]]
    assert reds and blues


def test_snap_color_nearest():
    pal = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    assert snap_color((0.9, 0.1, 0.1), pal) == 1
    assert snap_color((0.1, 0.1, 0.8), pal) == 2
    assert snap_color((0.05, 0.05, 0.05), pal) == 0


def test_flow_strokes_follow_the_field_and_carry_palette_indices(tmp_path):
    p = _stripes(tmp_path)
    g = load_image_grid(str(p), (0.0, 0.0, 120.0, 80.0), cell=2.0)
    pal = quantize_palette(g.rgb, k=4)
    strokes = flow_strokes(g, None, SeededRNG(7), length=8.0, step=1.0, density=0.3, palette=pal)
    assert 100 < len(strokes) < 2000  # density bounds it
    # strokes ride the vertical stripes: mostly vertical, ~length long
    vert = 0
    for poly, idx in strokes:
        assert idx is not None and 0 <= idx < 4
        dx = abs(poly[-1][0] - poly[0][0])
        dy = abs(poly[-1][1] - poly[0][1])
        if dy > dx:
            vert += 1
    assert vert / len(strokes) > 0.8
    # left-half strokes snap to red-ish palette entries, right-half to blue-ish
    left_idx = {idx for poly, idx in strokes if poly[0][0] < 50}
    right_idx = {idx for poly, idx in strokes if poly[0][0] > 70}
    assert all(pal[i][0] >= pal[i][2] for i in left_idx)
    assert all(pal[i][2] >= pal[i][0] for i in right_idx)


def test_flow_strokes_respect_region_and_are_deterministic(tmp_path):
    p = _stripes(tmp_path)
    g = load_image_grid(str(p), (0.0, 0.0, 120.0, 80.0), cell=2.0)
    reg = Polygon([(20, 20), (60, 20), (60, 60), (20, 60)])
    a = flow_strokes(g, reg, SeededRNG(3), density=0.5)
    b = flow_strokes(g, reg, SeededRNG(3), density=0.5)
    assert a == b
    assert all(20 - 1e-6 <= x <= 60 + 1e-6 and 20 - 1e-6 <= y <= 60 + 1e-6 for poly, _ in a for x, y in poly)
