"""The crowned Q head, constructed by hand — not traced from the image.

A cubist head is a set of flat facets. A facet is a polygon hatched at one
angle, and the angle is what reads as its orientation in space. That is
line-native, so it suits a plotter far better than a photograph does.
"""
from __future__ import annotations

import math
from typing import List, Tuple

from promptplot.models import GCodeCommand
from demo import gesture, _poly          # sibling import; the loader puts us on sys.path

Pt = Tuple[float, float]


def _hatch(poly: List[Pt], ang_deg: float, gap: float) -> List[List[Pt]]:
    """Parallel fill lines clipped to a polygon, by scanline in a rotated frame."""
    a = math.radians(ang_deg)
    ca, sa = math.cos(-a), math.sin(-a)
    R = [(x * ca - y * sa, x * sa + y * ca) for x, y in poly]
    ys = [p[1] for p in R]
    y0, y1 = min(ys) + gap * 0.4, max(ys) - gap * 0.4
    ca2, sa2 = math.cos(a), math.sin(a)
    out: List[List[Pt]] = []
    y = y0
    while y <= y1:
        xs = []
        for (x1_, y1_), (x2_, y2_) in zip(R, R[1:] + R[:1]):
            if (y1_ <= y < y2_) or (y2_ <= y < y1_):
                t = (y - y1_) / (y2_ - y1_)
                xs.append(x1_ + t * (x2_ - x1_))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            p = (xs[i], y); q = (xs[i + 1], y)
            if q[0] - p[0] > gap * 0.5:
                out.append([(p[0] * ca2 - p[1] * sa2, p[0] * sa2 + p[1] * ca2),
                            (q[0] * ca2 - q[1] * sa2, q[0] * sa2 + q[1] * ca2)])
        y += gap
    return out


# --- the head, in local mm, origin between the eyes -------------------------
SIL = [(-22, 52), (0, 58), (20, 54), (30, 40), (34, 18), (30, -6),
       (22, -26), (6, -38), (-10, -40), (-24, -28), (-32, -4), (-30, 26)]

# facets: (polygon, hatch angle). The angle IS the plane's orientation.
FACETS = [
    ([(-22, 52), (0, 58), (2, 32), (-24, 28)], 72, 0.0),      # forehead frontal - LIT, bare
    ([(0, 58), (20, 54), (30, 40), (14, 30), (2, 32)], 20, 2.6),   # turning away
    ([(-24, 28), (2, 32), (0, 2), (-30, 0)], 88, 0.0),        # cheek frontal - LIT, bare
    ([(2, 32), (14, 30), (30, 40), (34, 18), (12, 8), (0, 2)], 38, 1.7),  # profile, shadow
    ([(-30, 0), (0, 2), (-2, -22), (-24, -28)], 60, 3.4),     # jaw frontal, half tone
    ([(0, 2), (12, 8), (30, -6), (22, -26), (-2, -22)], 12, 1.5),  # jaw profile, darkest
]

CROWN = [(-22, 52), (-16, 74), (-10, 54), (-4, 78), (2, 56),
         (8, 80), (14, 56), (20, 76), (24, 52)]

EYE_F = [(-20, 20), (-13, 25), (-5, 21), (-12, 15)]           # frontal eye, almond
NOSE = [(2, 32), (9, 6), (2, -2), (-3, 0)]                    # ridge down the split
MOUTH = [(-2, -14), (10, -12), (16, -16)]
SPLIT = [(2, 58), (2, 32), (0, 2), (-2, -22), (-6, -38)]      # frontal | profile


def _place(pts, cx, cy, s):
    return [(cx + x * s, cy + y * s) for x, y in pts]


def _draw(forms, rng, mode, pen=0):
    out = []
    for f in forms:
        if mode == "gesture":
            for s in gesture(f, rng, overshoot=(1.2, 4.5), searching=(1, 2),
                             wobble=0.55, break_up=False, step=1.0):
                out += _poly(s, pen=pen)
        else:
            out += _poly(f, pen=pen)
    return out


def head(cx, cy, s, rng, mode="gesture"):
    out: List[GCodeCommand] = []
    # 1. facet fills first (they sit under the structure)
    for poly, ang, gap in FACETS:
        if gap <= 0:
            continue                      # bare paper IS the lit plane
        P = _place(poly, cx, cy, s)
        for seg in _hatch(P, ang, gap * s):
            out += _poly(seg, pen=0)
    # 2. crown, hatched alternately
    C = _place(CROWN, cx, cy, s)
    for i in range(0, len(C) - 2, 2):
        tri = [C[i], C[i + 1], C[i + 2]]
        if i % 4 == 0:                    # alternate points solid / outline only
            for seg in _hatch(tri, 62, 1.5 * s):
                out += _poly(seg, pen=1)
    # 3. structure lines, as gestures
    out += _draw([_place(SIL + [SIL[0]], cx, cy, s), _place(C, cx, cy, s),
                  _place(SPLIT, cx, cy, s), _place(NOSE, cx, cy, s),
                  _place(MOUTH, cx, cy, s)], rng, mode)
    out += _draw([_place(EYE_F + [EYE_F[0]], cx, cy, s)], rng, mode)
    # pupil
    out += _poly(_place([(-13, 20), (-11, 21), (-12, 18), (-14, 19), (-13, 20)],
                        cx, cy, s), pen=0)
    # facet edges, gestured — these are what read as cubism
    for poly, _a, _g in FACETS:
        out += _draw([_place(poly + [poly[0]], cx, cy, s)], rng, mode)
    return out


def head_demo(rng, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    s = min(W / 300.0, H / 185.0)
    out = []
    out += head(x0 + W * 0.27, y0 + H * 0.46, s, rng, mode="clean")
    out += head(x0 + W * 0.73, y0 + H * 0.46, s, rng, mode="gesture")
    return out
