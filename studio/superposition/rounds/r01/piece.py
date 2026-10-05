"""EXACT RECREATION candidate — `superposition`.

Reproduction (not redesign) of ``studio/superposition/ref/reference.png``: the
five-stage attention plate — Q and K families of overlapping Gaussian bumps,
a contoured Q.K^T similarity field, a softmax spike row, a wide V family and a
nested Z = AV bell — wired together by four sweeping dotted connector fans.

Everything is authored in REFERENCE PIXEL SPACE (1122 x 1402, y down, plate
centre line x = 561) and mapped to the drawable area at the end.  The sheet is
A4 portrait (aspect 0.686) while the reference is 0.800, so vertical EXTENTS
measured from a stage baseline are pre-divided by the stretch factor ``k`` —
bump shapes keep the reference's aspect, the slack lands in the gaps between
stages (which is where the fans live).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import (  # noqa: F401
    _chain_segments,
    _marching_squares,
    _poly,
    circle,
    fill_disc,
    giant_type,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

try:  # numpy ships with the viz extra; the field needs it
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

Bounds = Tuple[float, float, float, float]

REF_W, REF_H = 1122.0, 1402.0
CX = 561.0

RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

# stage baselines, in reference pixels
Y_QK = 312.0
Y_AXIS = 548.0
Y_SM = 839.0
Y_V = 1106.0
Y_Z = 1316.0


# ---------------------------------------------------------------------------
# sheet transform
# ---------------------------------------------------------------------------


class _Sheet:
    def __init__(self, bounds: Bounds):
        x0, y0, x1, y1 = bounds
        self.sx = (x1 - x0) / REF_W
        self.sy = (y1 - y0) / REF_H
        self.ox, self.oy = x0, y1
        # 1.0 = the whole plate stretches uniformly onto the taller A4 sheet, so
        # every element keeps the reference's FRACTION of the sheet. Lower it
        # (sx/sy = 0.86) to keep each bell's local aspect instead — that pays
        # for it with 14% shorter bumps and wider gaps, which reads worse.
        self.k = 1.0

    def P(self, p) -> Tuple[float, float]:
        return (self.ox + p[0] * self.sx, self.oy - p[1] * self.sy)

    def mm(self, px: float) -> float:
        return px * self.sx

    def C(self, anchor: float, py: float) -> float:
        """Aspect-correct a reference y measured from ``anchor``."""
        return anchor + (py - anchor) * self.k


def _E(S: _Sheet, pts, pen: Optional[int], f: int = 1700) -> List[GCodeCommand]:
    return _poly([S.P(p) for p in pts], color=pen, f=f)


# ---------------------------------------------------------------------------
# dotted line engine  (the plate is more dotted than solid)
# ---------------------------------------------------------------------------


def _arc_samples(pts, step: float, phase: float = 0.0):
    out = []
    s_next = phase
    s = 0.0
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy)
        if L < 1e-12:
            continue
        ux, uy = dx / L, dy / L
        while s_next <= s + L:
            t = s_next - s
            out.append(((ax + ux * t, ay + uy * t), (ux, uy)))
            s_next += step
        s += L
    return out


def _dotted(
    S: _Sheet, pts, pen: Optional[int], pitch: float = 10.0, dash: float = 2.0,
    f: int = 2200, phase: float = 0.0
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p, (ux, uy) in _arc_samples(pts, pitch, phase):
        out += _E(S, [(p[0] - ux * dash / 2, p[1] - uy * dash / 2),
                      (p[0] + ux * dash / 2, p[1] + uy * dash / 2)], pen, f)
    return out


# ---------------------------------------------------------------------------
# marks
# ---------------------------------------------------------------------------


def _ring(S: _Sheet, px: float, py: float, r_px: float, pen, f: int = 2300):
    cx, cy = S.P((px, py))
    return circle(cx, cy, S.mm(r_px), pen=pen, f=f, n=max(20, int(r_px * 7)))


def _disc(S: _Sheet, px: float, py: float, r_px: float, pen, f: int = 2000):
    cx, cy = S.P((px, py))
    r = S.mm(r_px)
    if r <= 0.18:
        return _poly([(cx - r, cy), (cx + r, cy)], color=pen, f=f)
    # solid ink dot: a tight spiral + its rim. The 0.30 mm pitch is a deliberate
    # exception to the >=0.8 mm line-spacing rule — a plotted dot has to be a
    # dot, and every one of these is under 1.6 mm across.
    out = fill_disc(cx, cy, r, spacing=0.30, pen=pen, f=f)
    out += circle(cx, cy, r, pen=pen, f=f, n=26)
    return out


def _bullseye(S: _Sheet, px: float, py: float, r_px: float, pen):
    return _ring(S, px, py, r_px, pen) + _disc(S, px, py, r_px * 0.45, pen)


# ---------------------------------------------------------------------------
# curves
# ---------------------------------------------------------------------------


# a bell tail is truncated where it comes within TAIL_FLOOR px (~0.35 mm) of
# the baseline: past that the tails of a dozen bells and the baseline itself all
# run along the same line, re-inking it for tens of mm under the 0.8 mm floor.
TAIL_FLOOR = 2.8


def _gauss(S: _Sheet, cxp: float, base_y: float, h: float, sig: float,
           span: float = 3.15, n: int = 110):
    if h <= TAIL_FLOOR * 1.25:
        return []
    span = min(span, math.sqrt(2.0 * math.log(h / TAIL_FLOOR)))
    pts = []
    for i in range(n + 1):
        t = -span + 2 * span * i / n
        x = cxp + t * sig
        if x < 16.0 or x > 1106.0:      # stay on the sheet
            continue
        pts.append((x, base_y - h * S.k * math.exp(-0.5 * t * t)))
    return pts


def _bez(p0, p1, p2, p3, n: int = 120):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1.0 - t
        pts.append((
            mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0],
            mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return pts


def _baseline(S: _Sheet, y: float, xa: float, xb: float, pen,
              tail_l: float = 0.0, tail_r: float = 0.0, f: int = 1600):
    out = _E(S, [(xa, y), (xb, y)], pen, f)
    if tail_l:
        out += _dotted(S, [(xa - 8.0, y), (xa - 8.0 - tail_l, y)], pen, pitch=16.0, dash=2.6)
    if tail_r:
        out += _dotted(S, [(xb + 8.0, y), (xb + 8.0 + tail_r, y)], pen, pitch=16.0, dash=2.6)
    return out


# ---------------------------------------------------------------------------
# the bump families
#   (cx, height, sigma, kind)   kind: s solid / g fine-dotted ghost / d dotted
# ---------------------------------------------------------------------------

Q_BUMPS = [
    (95.0, 22.0, 17.0, "s"),
    (137.0, 41.0, 21.0, "s"),
    (166.0, 30.0, 17.0, "s"),
    (195.0, 112.0, 27.0, "s"),
    (232.0, 57.0, 22.0, "s"),
    (270.0, 201.0, 25.0, "s"),
    (279.0, 161.0, 31.0, "s"),
    (262.0, 133.0, 45.0, "s"),
    (284.0, 112.0, 36.0, "s"),
    (268.0, 88.0, 57.0, "s"),
    (292.0, 62.0, 44.0, "s"),
    (258.0, 45.0, 68.0, "s"),
    (306.0, 79.0, 20.0, "s"),
    (334.0, 103.0, 26.0, "s"),
    (361.0, 62.0, 20.0, "s"),
    (401.0, 47.0, 23.0, "s"),
    (437.0, 33.0, 19.0, "s"),
    (462.0, 18.0, 15.0, "s"),
    # light ghosts
    (215.0, 68.0, 52.0, "g"),
    (300.0, 118.0, 74.0, "g"),
    (352.0, 48.0, 46.0, "g"),
    (176.0, 33.0, 40.0, "g"),
    (247.0, 185.0, 46.0, "d"),
]

# (cx, dropline top height above baseline, baseline mark, apex marks)
#   marks: (height, radius, kind)  kind: f filled / o open / b bullseye
Q_DROPS = [
    (95.0, 62.0, (3.6, "f"), [(22.0, 2.6, "f")]),
    (137.0, 108.0, (3.0, "f"), [(41.0, 4.0, "o")]),
    (195.0, 168.0, (4.4, "f"), [(112.0, 4.8, "o")]),
    (232.0, 96.0, (2.2, "f"), [(57.0, 2.4, "f")]),
    (270.0, 266.0, (5.6, "f"), [(201.0, 5.8, "f"), (161.0, 4.8, "o"),
                                (133.0, 2.4, "f"), (88.0, 2.4, "f"), (45.0, 2.2, "f")]),
    (306.0, 219.0, (2.6, "f"), [(79.0, 2.4, "f")]),
    (334.0, 150.0, (3.2, "f"), [(103.0, 4.4, "o")]),
    (361.0, 112.0, (2.2, "f"), [(62.0, 3.8, "o")]),
    (401.0, 92.0, (5.0, "o"), [(47.0, 3.0, "o")]),
    (437.0, 68.0, (2.6, "f"), [(33.0, 2.2, "f")]),
    (462.0, 44.0, (2.2, "f"), []),
]

V_OFFSETS = [0.0, 87.0, 153.0, 209.0, 301.0, 378.0, 436.0]
# per |offset| rank: (main height, sigma, nest heights)
V_CLUSTER = {
    0.0: (118.0, 27.0, [92.0, 70.0, 48.0]),
    87.0: (47.0, 22.0, [30.0]),
    153.0: (118.0, 26.0, [96.0, 74.0, 52.0, 32.0]),
    209.0: (51.0, 23.0, [33.0]),
    301.0: (110.0, 25.0, [86.0, 64.0, 44.0]),
    378.0: (132.0, 26.0, [104.0, 80.0, 56.0, 34.0]),
    436.0: (42.0, 21.0, [26.0]),
}

Z_NEST = [
    (130.0, 78.0, "s"),
    (118.0, 70.0, "s"),
    (106.0, 64.0, "s"),
    (95.0, 58.0, "s"),
    (84.0, 53.0, "s"),
    (73.0, 48.0, "s"),
    (62.0, 44.0, "s"),
    (51.0, 40.0, "s"),
    (40.0, 36.0, "s"),
    (30.0, 32.0, "s"),
    (21.0, 28.0, "s"),
    (80.0, 106.0, "d"),
]

SM_PEAKS = [(419.0, 54.0, 14.5), (486.0, 95.0, 14.0), (562.0, 133.0, 14.5),
            (637.0, 76.0, 14.0), (707.0, 50.0, 14.0)]
SM_GHOSTS = [(356.0, 44.0, 44.0), (408.0, 68.0, 48.0), (522.0, 104.0, 52.0),
             (652.0, 54.0, 45.0), (752.0, 40.0, 40.0)]


# ---------------------------------------------------------------------------
# the Q.K^T field
# ---------------------------------------------------------------------------

_BLOBS = [  # (cx, cy, amp, sx, sy) — the low, broad envelope
    (561.0, 548.0, 0.44, 132.0, 40.0),
    (487.0, 577.0, 0.22, 54.0, 29.0),
    (639.0, 527.0, 0.24, 52.0, 29.0),
    (386.0, 540.0, 0.22, 56.0, 27.0),
    (738.0, 556.0, 0.21, 56.0, 27.0),
    (600.0, 612.0, 0.16, 52.0, 23.0),
    (466.0, 482.0, 0.15, 46.0, 21.0),
    (686.0, 606.0, 0.13, 40.0, 19.0),
    (424.0, 604.0, 0.12, 38.0, 18.0),
    (708.0, 480.0, 0.11, 34.0, 16.0),
    (535.0, 519.0, 0.13, 28.0, 16.0),
    (340.0, 552.0, 0.10, 34.0, 18.0),
    (784.0, 546.0, 0.10, 34.0, 18.0),
]
_CUSPS = [  # (cx, cy, amp, decay, y-aspect) — the eyes; `decay` IS the ring
    (639.0, 527.0, 1.00, 66.0, 1.28),   # radius, and rings = amp / level step
    (487.0, 577.0, 0.93, 68.0, 1.52),
    (535.0, 519.0, 0.24, 26.0, 1.25),
]

MAP_X0, MAP_X1 = 296.0, 828.0
MAP_Y0, MAP_Y1 = 412.0, 672.0
# Hand-set ladder (fractions of the field range) instead of a uniform sweep:
# three close-packed DOTTED outer rings hugging the boundary, then a uniform
# 0.062 solid step.  Ring pitch inside an eye is decay * step * range, which is
# what keeps the cores at ~0.9 mm rather than the reference's unplottable 0.3.
LEVELS_DOTTED = [0.128, 0.183, 0.238]
LEVELS_SOLID = [0.288 + 0.062 * i for i in range(12)]


def _field(rng: SeededRNG):
    cell = 1.7
    xs = [MAP_X0 + i * cell for i in range(int((MAP_X1 - MAP_X0) / cell) + 1)]
    ys = [MAP_Y0 + j * cell for j in range(int((MAP_Y1 - MAP_Y0) / cell) + 1)]
    X = np.asarray(xs)[None, :]
    Y = np.asarray(ys)[:, None]
    F = np.zeros((len(ys), len(xs)))
    for cx, cy, a, sx, sy in _BLOBS:
        F += a * np.exp(-0.5 * (((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2))
    for cx, cy, a, sg, asp in _CUSPS:
        r = np.sqrt((X - cx) ** 2 + ((Y - cy) * asp) ** 2)
        F += a * np.exp(-r / sg)
    # a little seeded terrain so the outer rings are lumpy, not elliptical
    pert = np.zeros_like(F)
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            pert[j, i] = rng.fbm(x * 0.0165, y * 0.0165, octaves=3)
    F += 0.195 * pert
    return F, xs, ys


def _contour_map(S: _Sheet, rng: SeededRNG) -> Tuple[List[GCodeCommand], list]:
    if np is None:
        return [], []
    F, xs, ys = _field(rng)
    lo, hi = float(F.min()), float(F.max())
    Fl = F.tolist()
    out: List[GCodeCommand] = []
    chains_all = []
    for lv, frac in enumerate(LEVELS_DOTTED + LEVELS_SOLID):
        iso = lo + (hi - lo) * frac
        chains = [c for c in _chain_segments(_marching_squares(Fl, xs, ys, iso)) if len(c) >= 8]
        dotted = lv < len(LEVELS_DOTTED)
        for ch in chains:
            pts = [(px, S.C(Y_AXIS, py)) for px, py in ch]
            if dotted:
                out += _dotted(S, pts, BLACK, pitch=7.6, dash=1.35, f=2300)
            else:
                out += _E(S, pts, BLACK, f=1500)
            chains_all.append(pts)
    return out, chains_all


# ---------------------------------------------------------------------------
# fans
# ---------------------------------------------------------------------------


def _fan(S: _Sheet, srcs, targets, pen, a, b, q=0.10,
         pitch: float = 8.6, dash: float = 1.35, tip=None):
    """Nested dotted connector bundle.

    Each strand is a cubic whose control polygon is MONOTONE downward: leave the
    source vertically (``a`` of the gap), arrive at the target vertically
    (``b`` of the gap).  ``a`` + ``b`` < 1 or the strand loops back on itself,
    which is what made the first round bulge outside the family it came from.
    """
    out: List[GCodeCommand] = []
    n = len(srcs)
    for j in range(n):
        sx, sy = srcs[j]
        tx, ty = targets[j]
        u = j / (n - 1) if n > 1 else 0.0
        gap = ty - sy
        aa = a(u, j) if callable(a) else a
        bb = b(u, j) if callable(b) else b
        qq = q(u, j) if callable(q) else q
        p1 = (sx, sy + gap * aa)
        p2 = (tx + (sx - tx) * qq, ty - gap * bb)
        pts = _bez((sx, sy), p1, p2, (tx, ty))
        out += _dotted(S, pts, pen, pitch=pitch, dash=dash, f=2300)
        if tip is not None and tip(j):
            out += _disc(S, tx, ty, 3.2, pen)
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def superposition(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    try:  # cream stock, hairline pen — preview only, never touches the GCode
        from promptplot.config import get_config

        viz = get_config().visualization
        viz.paper_color = "cream"
        viz.line_width = 0.62
    except Exception:  # pragma: no cover
        pass

    S = _Sheet(bounds)
    out: List[GCodeCommand] = []

    # ---------------- Q / K families (K is the mirror about x = 561) --------
    for side, pen in ((-1, RED), (+1, BLUE)):
        def mx(x, side=side):
            return CX + side * (CX - x) if side > 0 else x

        bx0, bx1 = sorted((mx(68.0), mx(468.0)))
        out += _baseline(S, Y_QK, bx0, bx1, pen,
                         tail_l=46.0 if side < 0 else 0.0,
                         tail_r=0.0 if side < 0 else 46.0)
        for cxp, h, sig, kind in Q_BUMPS:
            pts = _gauss(S, mx(cxp), Y_QK, h, sig)
            if kind == "s":
                out += _E(S, pts, pen, f=1600)
            elif kind == "g":
                out += _dotted(S, pts, pen, pitch=6.0, dash=1.5, f=2400)
            else:
                out += _dotted(S, pts, pen, pitch=10.0, dash=2.1, f=2300)
        for cxp, dtop, (rb, kb), apexes in Q_DROPS:
            x = mx(cxp)
            top = S.C(Y_QK, Y_QK - dtop)
            out += _dotted(S, [(x, Y_QK), (x, top)], pen, pitch=9.0, dash=1.9)
            out += _disc(S, x, top, 2.4, pen)
            out += (_disc(S, x, Y_QK, rb, pen) if kb == "f" else _ring(S, x, Y_QK, rb, pen))
            for h, r, kind in apexes:
                y = S.C(Y_QK, Y_QK - h)
                if kind == "f":
                    out += _disc(S, x, y, r, pen)
                elif kind == "o":
                    out += _ring(S, x, y, r, pen)
                else:
                    out += _bullseye(S, x, y, r, pen)

    # ---------------- contour map ------------------------------------------
    cmds, chains = _contour_map(S, rng)
    out += cmds

    # faint tone inside the field
    if np is not None:
        F, xs, ys = _field(rng)
        lo, hi = float(F.min()), float(F.max())
        iso_tone = lo + (hi - lo) * 0.36
        step = 6.2
        yy = MAP_Y0 + 6.0
        while yy < MAP_Y1:
            xx = MAP_X0 + 6.0 + (step * 0.5 if int((yy - MAP_Y0) / step) % 2 else 0.0)
            while xx < MAP_X1:
                jx = xx + rng.uniform(-3.1, 3.1)
                jy = yy + rng.uniform(-3.1, 3.1)
                i = int((jx - MAP_X0) / 1.7)
                j = int((jy - MAP_Y0) / 1.7)
                if 0 <= j < len(ys) and 0 <= i < len(xs) and F[j][i] > iso_tone:
                    out += _dotted(S, [(jx - 0.9, S.C(Y_AXIS, jy)), (jx + 0.9, S.C(Y_AXIS, jy))],
                                   BLACK, pitch=4.0, dash=1.7, f=2400)
                xx += step
            yy += step

    # node dots riding the contours
    if chains:
        placed: List[Tuple[float, float]] = []
        tries = 0
        while len(placed) < 54 and tries < 900:
            tries += 1
            ch = chains[rng.randint(0, len(chains) - 1)]
            px, py = ch[rng.randint(0, len(ch) - 1)]
            if not (330.0 < px < 800.0):
                continue
            if any(math.hypot(px - qx, py - qy) < 15.0 for qx, qy in placed):
                continue
            placed.append((px, py))
            out += _disc(S, px, py, rng.uniform(1.3, 3.8), BLACK)

    # loose dot scatter under the map, the way the reference lets the field
    # shed nodes on its way down to the softmax row
    for _ in range(18):
        sx = CX + rng.uniform(-215.0, 215.0)
        sy = rng.uniform(640.0, 684.0)
        if abs(sx - CX) > 48.0 or sy > 664.0:
            out += _disc(S, sx, sy, rng.uniform(1.5, 3.0), BLACK)

    # ---------------- the Q.K^T axis ---------------------------------------
    ax_y = Y_AXIS
    out += _dotted(S, [(199.0, ax_y), (922.0, ax_y)], BLACK, pitch=11.0, dash=2.6, f=2300)
    for x, r, kind in [(271.0, 5.4, "o"), (561.0, 5.6, "o"), (851.0, 5.4, "o"),
                       (357.0, 2.4, "f"), (687.0, 4.6, "f"), (610.0, 2.2, "f"),
                       (770.0, 2.2, "f")]:
        out += (_ring(S, x, ax_y, r, BLACK) if kind == "o" else _disc(S, x, ax_y, r, BLACK))
    # the red / blue vertical ticks through the outer axis circles
    for x, pen in ((271.0, RED), (851.0, BLUE)):
        out += _dotted(S, [(x, S.C(ax_y, 440.0)), (x, S.C(ax_y, 622.0))], pen,
                       pitch=9.0, dash=1.9)

    # ---------------- centre line ------------------------------------------
    out += _dotted(S, [(CX, 330.0), (CX, 384.0)], BLACK, pitch=9.0, dash=1.9)
    out += _dotted(S, [(CX, 412.0), (CX, 1124.0)], BLACK, pitch=9.0, dash=1.9)
    out += _dotted(S, [(CX, 1124.0), (CX, 1362.0)], GREEN, pitch=9.0, dash=1.9)

    # ---------------- Q -> map and K -> map fans ---------------------------
    q_src_x = [c[0] for c in Q_DROPS][1:]       # 10 strands; x=95 keeps a stub only
    n = len(q_src_x)
    for side, pen in ((-1, RED), (+1, BLUE)):
        x = CX + side * (CX - 95.0) if side > 0 else 95.0
        out += _dotted(S, [(x, Y_QK + 6.0), (x, Y_QK + 62.0)], pen, pitch=9.0, dash=1.9)
    for side, pen in ((-1, RED), (+1, BLUE)):
        srcs, tgts = [], []
        for j, xq in enumerate(q_src_x):
            kk = n - 1 - j                       # 0 = innermost source
            x = CX + side * (CX - xq) if side > 0 else xq
            srcs.append((x, Y_QK + 6.0))
            tgx = CX + side * (46.0 + 11.5 * kk)
            tgts.append((tgx, S.C(Y_AXIS, 448.0 + 8.5 * kk)))
        rank = (lambda j: n - 1 - j) if side < 0 else (lambda j: j)
        out += _fan(S, srcs, tgts, pen,
                    a=lambda u, j: 0.33 + 0.018 * rank(j),
                    b=lambda u, j: 0.44 - 0.013 * rank(j),
                    q=0.10, tip=lambda j: rank(j) in (1, 4, 7))

    # ---------------- softmax stage ----------------------------------------
    out += _baseline(S, Y_SM, 317.0, 805.0, BLACK, tail_l=44.0, tail_r=44.0)
    for cxp, h, sig in SM_GHOSTS:
        out += _dotted(S, _gauss(S, cxp, Y_SM, h, sig), BLACK, pitch=6.0, dash=1.5, f=2400)
    for cxp, h, sig in SM_PEAKS:
        out += _E(S, _gauss(S, cxp, Y_SM, h, sig), BLACK, f=1600)
    sm_marks = [(419.0, 54.0, 4.6, "f"), (486.0, 95.0, 5.0, "f"), (562.0, 133.0, 5.8, "f"),
                (637.0, 76.0, 5.0, "b"), (707.0, 50.0, 4.6, "o")]
    for cxp, h, r, kind in sm_marks:
        y = S.C(Y_SM, Y_SM - h)
        if kind == "f":
            out += _disc(S, cxp, y, r, BLACK)
        elif kind == "o":
            out += _ring(S, cxp, y, r, BLACK)
        else:
            out += _bullseye(S, cxp, y, r, BLACK)
        out += _dotted(S, [(cxp, Y_SM), (cxp, y)], BLACK, pitch=8.0, dash=1.8)
    # droplines that come down from the map
    for cxp in (486.0, 562.0, 637.0):
        out += _dotted(S, [(cxp, S.C(Y_AXIS, 640.0)), (cxp, Y_SM)], BLACK, pitch=9.0, dash=1.9)
    for x, r, kind in [(366.0, 2.4, "f"), (419.0, 2.6, "f"), (485.0, 4.4, "o"),
                       (562.0, 6.0, "o"), (637.0, 2.6, "f"), (707.0, 3.8, "f"),
                       (760.0, 2.2, "f")]:
        out += (_ring(S, x, Y_SM, r, BLACK) if kind == "o" else _disc(S, x, Y_SM, r, BLACK))

    # ---------------- V family ---------------------------------------------
    v_centres = sorted({CX + s * o for o in V_OFFSETS for s in (-1, 1)})
    out += _baseline(S, Y_V, 68.0, 1054.0, OCHRE, tail_l=40.0, tail_r=40.0)
    for cxp in v_centres:
        o = abs(cxp - CX)
        h, sig, nest = V_CLUSTER[min(V_CLUSTER, key=lambda k: abs(k - o))]
        out += _E(S, _gauss(S, cxp, Y_V, h, sig), OCHRE, f=1600)
        # nest members are OFFSET and alternately narrower/wider so their
        # outlines CROSS (the reference reads as a thicket, not as onion rings)
        for m, hh in enumerate(nest):
            wob = (1.0 + 0.34 * (m + 1)) if m % 2 == 0 else (0.72 + 0.16 * m)
            off = (8.0 if m % 2 == 0 else -9.0) * (1.0 + 0.3 * m)
            out += _E(S, _gauss(S, cxp + off, Y_V, hh, sig * wob), OCHRE, f=1600)
        out += _dotted(S, _gauss(S, cxp, Y_V, h * 0.72, sig * 2.4), OCHRE,
                       pitch=6.0, dash=1.5, f=2400)
        top = S.C(Y_V, Y_V - h - 34.0)
        out += _dotted(S, [(cxp, Y_V), (cxp, top)], OCHRE, pitch=9.0, dash=1.9)
        out += _disc(S, cxp, top, 2.4, OCHRE)
        apex = S.C(Y_V, Y_V - h)
        big = h > 100.0
        if (cxp - CX) < 0:
            out += (_ring(S, cxp, apex, 5.0, OCHRE) if big else _disc(S, cxp, apex, 3.0, OCHRE))
        else:
            out += (_disc(S, cxp, apex, 5.0, OCHRE) if big else _ring(S, cxp, apex, 3.4, OCHRE))
        out += (_ring(S, cxp, Y_V, 4.6, OCHRE) if big else _disc(S, cxp, Y_V, 2.8, OCHRE))

    for o in (44.0, 120.0, 182.0, 252.0, 340.0, 408.0):
        for sgn in (-1.0, 1.0):
            out += _E(S, _gauss(S, CX + sgn * o, Y_V, 24.0, 19.0), OCHRE, f=1600)

    # ---------------- softmax -> V fan (diverging) -------------------------
    sm_off = [-150.0, -120.0, -90.0, -58.0, -28.0, 0.0, 28.0, 58.0, 90.0, 120.0, 150.0]
    v_tgt = [CX - 378.0, CX - 301.0, CX - 209.0, CX - 153.0, CX - 87.0, CX,
             CX + 87.0, CX + 153.0, CX + 209.0, CX + 301.0, CX + 378.0]
    srcs = [(CX + o, Y_SM + 6.0) for o in sm_off]
    tgts = [(x, S.C(Y_V, Y_V - 150.0)) for x in v_tgt]
    out += _fan(S, srcs, tgts, OCHRE,
                a=lambda u, j: 0.34 + 0.07 * abs(u - 0.5) * 2.0,
                b=lambda u, j: 0.33 + 0.17 * abs(u - 0.5) * 2.0, q=0.05)
    for o in sm_off:
        out += _disc(S, CX + o, Y_SM + 12.0, 2.2, OCHRE)

    # ---------------- V -> Z fan (converging) ------------------------------
    srcs, tgts = [], []
    for cxp in v_centres:
        o = cxp - CX
        side = -1 if o < 0 else 1
        kk = V_OFFSETS.index(min(V_OFFSETS, key=lambda k: abs(k - abs(o))))
        srcs.append((cxp, Y_V + 6.0))
        tgts.append((CX + side * (24.0 + 13.0 * kk), S.C(Y_Z, Y_Z - 150.0 + 11.0 * kk)))
    out += _fan(S, srcs, tgts, OCHRE,
                a=lambda u, j: 0.30 + 0.10 * abs(u - 0.5) * 2.0,
                b=lambda u, j: 0.32 + 0.18 * abs(u - 0.5) * 2.0, q=0.12)
    for cxp in v_centres:
        out += _disc(S, cxp, Y_V + 12.0, 2.2, OCHRE)

    # ---------------- Z = AV -----------------------------------------------
    out += _baseline(S, Y_Z, 250.0, 872.0, GREEN, tail_l=52.0, tail_r=52.0)
    for idx, (h, sig, kind) in enumerate(Z_NEST):
        pts = _gauss(S, CX, Y_Z, h, sig)
        if kind == "s":
            out += _E(S, pts, GREEN, f=1600)
        else:
            out += _dotted(S, pts, GREEN, pitch=7.0, dash=1.6, f=2400)
    for h, r, kind in [(150.0, 3.0, "f"), (130.0, 5.4, "f"), (98.0, 4.6, "o"), (73.0, 5.0, "f")]:
        y = S.C(Y_Z, Y_Z - h)
        out += (_disc(S, CX, y, r, GREEN) if kind == "f" else _ring(S, CX, y, r, GREEN))
    for x, r, kind in [(333.0, 5.0, "o"), (561.0, 6.0, "o"), (789.0, 5.0, "o"),
                       (250.0, 3.0, "f"), (203.0, 2.6, "f"), (872.0, 3.0, "f"),
                       (919.0, 2.6, "f")]:
        out += (_ring(S, x, Y_Z, r, GREEN) if kind == "o" else _disc(S, x, Y_Z, r, GREEN))
    for x, h in [(407.0, 22.0), (714.0, 22.0), (620.0, 96.0), (500.0, 96.0)]:
        out += _disc(S, x, S.C(Y_Z, Y_Z - h), 2.4, GREEN)

    # ---------------- type --------------------------------------------------
    out += _type(S)
    return out


def _type(S: _Sheet) -> List[GCodeCommand]:
    """Labels, set to the reference's own measured ink boxes.

    Sizes are cap height (ascender height for ``softmax``) read off the
    reference masks, not guessed: Q/K 27 px, V 25 px, Q.K^T 27 px, softmax
    17 px, Z = AV 23 px. ``proportional=True`` gives each glyph its own
    advance, with the font's per-case side bearings (1.02 caps / 0.55
    lowercase): "Z = AV" lands at 109.5 px against the reference's 110 and
    "softmax" at 77.9 px against 77. No local tracking compensation is needed
    or wanted here - the font metrics carry it.
    """
    out: List[GCodeCommand] = []

    def label(text, px, py, h_px, pen):
        """Monoline, proportional, case as written. NO weight= passes:
        giant_type thickens a glyph by offsetting copies ~0.28 mm apart,
        which is under the 0.8 mm floor."""
        x, y = S.P((px, py))
        return giant_type(text, x, y, S.mm(h_px), pen=pen, proportional=True)

    out += label("Q", 115.0, 143.0, 27.0, RED)
    out += label("K", 977.0, 146.0, 27.0, BLUE)
    out += label("V", 117.0, 968.0, 25.0, OCHRE)
    # Q . K^T  — the reference sets this 122 px wide; a monoline sans cannot
    # fill that at a 27 px cap, so the group is spread on the glyph positions.
    out += label("Q", 520.0, 410.0, 27.0, BLACK)
    out += _disc(S, 556.0, 400.0, 2.4, BLACK)
    out += label("K", 572.0, 410.0, 27.0, BLACK)
    out += label("T", 606.0, 394.0, 16.0, BLACK)
    out += label("softmax", 656.0, 716.0, 17.0, BLACK)
    out += label("Z = AV", 757.0, 1264.0, 23.0, GREEN)
    return out
