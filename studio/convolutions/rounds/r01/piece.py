"""CONVOLUTIONS — recreation with a respaced layout, r01.

Reproduction of ``studio/convolutions/ref/reference.png`` (1536x1024) with an
explicit licence to fix the reference's crowding.  Every element's position was
MEASURED off the raster (colour masks + long-run scans for the tile borders,
row-band profiles for the type) and is recorded here in normalised sheet
coordinates ``(u, v)``, u = 0 left .. 1 right, v = 0 top .. 1 bottom, mapped
onto a composition frame inset inside the drawable area.

The vocabulary is the reference's, unchanged.  Only the GEOMETRY OF PLACEMENT
moved — see ``NOTES.md`` for the full list.  The five layout fixes:

1. nothing is clipped: the whole plate lives inside the frame;
2. the big dashed ellipses are clipped OUT of the tile-strip slab, and the
   connector bundles are clipped out of each tile rectangle, so they pass
   *behind* the strip and reappear in the gaps;
3. the three lower zones share one bottom baseline and one caption baseline,
   with 39 / 31 mm gutters (the reference has 33 / 17 and no shared baseline);
4. a 13 mm horizontal band of clear paper separates the flow band from the
   lower band;
5. the tile gap goes from 0.28x to 0.43x the tile width.

Contour rings everywhere come from CONICAL fields — a distance-to-boundary
field for the blobs (|grad d| = 1, so ring pitch is exactly the level step) and
``a*exp(-r/sigma)`` cusps for the whorls.  A Gaussian peak would spread its
rings at the summit, which is the opposite of the tight fingerprint the
reference shows.

Pens (``colors=4``): 0 black, 1 red, 2 blue, 3 olive.

Entry point: ``convolutions``.
"""

from __future__ import annotations

import math
from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, Region, Union, clip
from promptplot.generative.engine.kit import circle, plus_mark, tone_dots
from promptplot.generative.engine.policies import enforce_line_spacing
from promptplot.generative.generators import (
    _chain_segments,
    _dot,
    _glyph_advance,
    _poly,
    _stroke_text,
    _text_width,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, RED, BLUE, OLIVE = 0, 1, 2, 3

F_DRAW = 2200
MIN_PITCH = 0.85  # mm — plotting floor; no ring family may go under this


# ===========================================================================
# measured layout  (normalised sheet coords; v = 0 TOP)
# ===========================================================================
# Reference measurements, for the record (px on the 1536x1024 raster):
#   title caps          x   31.. 294  y  30.. 46   (cap height 16 px = 2.9 mm)
#   3 lowercase lines   x   31.. 285  y  87..142   (14 px = 2.5 mm, pitch 21 px)
#   upper-right block   x 1430..1497  y  31.. 88   (10 px = 1.8 mm, pitch 16 px)
#   five tiles          x  399..1075  y 397..528   (w 110, gap 31, h 131)
#   kernel bank         x   44.. 417  y 673..1008  (cell 110x102, gap 21/14)
#   feature maps        x 1024..1464  y 787..937   (cell 133x150, gap 17)
#   blob X (black)      x   32.. 399  y 212..699
#   blob Y (olive)      x 1224..1496  y 198..665
#   receptive cone      x  600.. 930  y 735..955   (apex on the sheet centreline)

FRAME_INSET = 3.0  # mm inside the drawable area

# --- header -------------------------------------------------------------
TITLE_CAP = 3.0
TITLE_W = 47.0
TITLE_V = 0.010  # cap TOP
RULE_V = 0.048
SUB_CAP = 2.5
SUB_V = (0.070, 0.0922, 0.1144)
SUB_W = 46.0
UR_CAP = 1.85
UR_V = (0.010, 0.0265, 0.043, 0.0595)
UR_RULE_V = 0.082
UR_W = 18.0

# --- three vertical anchors.  Everything left-aligned sits on u = 0, the
# spine / tile strip / cone share u = 0.5, everything right-aligned sits on
# u = 1.  Gaps are a MODULE, not whatever was left over: one cell gap inside
# every grid, one gutter between the lower zones, and the two lower gutters
# come out equal by construction because the two outer zones are the same
# width and the cone is centred.
CELL_GAP = 3.2  # inside the kernel bank AND the feature-map strip

# --- flow band ----------------------------------------------------------
# The blobs are narrower and start lower than a naive scaling of the
# reference would put them: at v = 0.145 the top lobe came within 3.5 mm of
# 'continuous perception', which is a collision, not a decision.  Dropping to
# 0.170 buys 8.7 mm and costs the blob 4 mm of height.
BX_U = (0.000, 0.168)
BX_V = (0.170, 0.470)
BY_U = (0.832, 1.000)
BY_V = (0.183, 0.483)

TILE_W = 18.5
TILE_H = 22.5
TILE_GAP = 8.0  # ref 5.6 mm at this scale -> 0.28x width; now 0.43x
N_TILES = 5
STRIP_CU = 0.500  # = midpoint of the two blobs' inner edges -> equal clearance
TILE_TOP_V = 0.303

TILE_PENS = (RED, BLACK, BLUE, OLIVE, RED)

# --- the gutter: 14 mm of paper nobody is allowed into --------------------
GUTTER_V = (0.538, 0.615)

# --- lower band ---------------------------------------------------------
BASE_V = 0.925  # shared bottom baseline of all three lower zones
CAP_BASE_V = 0.9605  # shared caption baseline
LOWER_TOP_V = 0.615  # shared top of the kernel bank + the cone apex

ZONE_CELL_W = 20.0  # SAME in both outer zones -> the two gutters are equal
KB_CELL_H = 16.87  # = (lower band - 2 gaps) / 3
FM_CELL_H = 22.6
CONE_HALF = 33.0


# ===========================================================================
# frame mapping
# ===========================================================================
class Frame:
    def __init__(self, bounds: Bounds, inset: float = FRAME_INSET):
        x0, y0, x1, y1 = bounds
        self.x0, self.y0 = x0 + inset, y0 + inset
        self.x1, self.y1 = x1 - inset, y1 - inset
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0

    def u(self, u: float) -> float:
        return self.x0 + u * self.w

    def v(self, v: float) -> float:
        return self.y1 - v * self.h

    def p(self, u: float, v: float) -> Pt:
        return (self.u(u), self.v(v))


# ===========================================================================
# type
# ===========================================================================
def _tracked(
    text: str,
    x: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    target_w: Optional[float] = None,
    f: int = 2300,
) -> Tuple[List[GCodeCommand], float]:
    """Proportional stroke type with uniform letter-tracking to hit ``target_w``.

    Cap height stays at the MEASURED value and the extra width is spent on
    tracking, instead of scaling the glyphs up (which is how recreation labels
    end up 30% oversized)."""
    sc = cap / 6.0
    nat = _text_width(text, cap, proportional=True)
    extra = 0.0
    if target_w is not None and len(text) > 1:
        extra = (target_w - nat) / (len(text) - 1)
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * sc + extra
    return out, (cx - extra - x) if len(text) > 1 else nat


def _tracked_w(text: str, cap: float, target_w: Optional[float]) -> float:
    if target_w is not None:
        return target_w
    return _text_width(text, cap, proportional=True)


def _text_at(
    text: str,
    baseline: float,
    cap: float,
    pen: Optional[int],
    left: Optional[float] = None,
    centre: Optional[float] = None,
    right: Optional[float] = None,
    target_w: Optional[float] = None,
) -> List[GCodeCommand]:
    w = _tracked_w(text, cap, target_w)
    if left is not None:
        x = left
    elif centre is not None:
        x = centre - w / 2.0
    else:
        x = (right or 0.0) - w
    return _tracked(text, x, baseline, cap, pen, target_w)[0]


def _sigma(x: float, baseline: float, cap: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Greek lower-case sigma as ONE drawn mark, left edge at ``x``.

    The shared font has 78 glyphs and neither 'sigma' nor the middle dot, so
    the activation label would silently degrade to 'o(.)'.  This is a single
    stroked mark in the same 4x6 glyph metric, NOT a local glyph table — the
    font gap is recorded in NOTES.md for central fixing.
    """
    sc = cap / 6.0
    pts = []
    for k in range(37):
        a = math.radians(38 + 360 * k / 36)
        pts.append((x + (1.95 + 1.75 * math.cos(a)) * sc, baseline + (2.0 + 1.95 * math.sin(a)) * sc))
    flag = [pts[0], (x + 4.55 * sc, baseline + 3.62 * sc)]
    return _poly(pts, color=pen, f=2300) + _poly(flag, color=pen, f=2300)


def _sigma_w(cap: float) -> float:
    return 4.9 * cap / 6.0


# ===========================================================================
# contouring — numpy-prefiltered marching squares, chained with the house
# `_chain_segments`.  Only cells the level actually crosses are visited, which
# is what makes four render rounds affordable.
# ===========================================================================
_MS_TABLE = {
    1: ((3, 0),),
    2: ((0, 1),),
    3: ((3, 1),),
    4: ((1, 2),),
    5: ((3, 2), (0, 1)),
    6: ((0, 2),),
    7: ((3, 2),),
    8: ((2, 3),),
    9: ((0, 2),),
    10: ((0, 3), (1, 2)),
    11: ((1, 2),),
    12: ((1, 3),),
    13: ((0, 1),),
    14: ((0, 3),),
}


def _iso_chains(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, iso: float) -> List[Poly]:
    """Iso-contour of F[j, i] (j indexes ys) as chained polylines."""
    v0 = F[:-1, :-1]
    v1 = F[:-1, 1:]
    v2 = F[1:, 1:]
    v3 = F[1:, :-1]
    case = (
        (v0 > iso).astype(np.uint8)
        | ((v1 > iso).astype(np.uint8) << 1)
        | ((v2 > iso).astype(np.uint8) << 2)
        | ((v3 > iso).astype(np.uint8) << 3)
    )
    jj, ii = np.nonzero((case != 0) & (case != 15))
    if len(jj) == 0:
        return []
    segs = []
    for j, i in zip(jj.tolist(), ii.tolist()):
        xa, xb = float(xs[i]), float(xs[i + 1])
        ya, yb = float(ys[j]), float(ys[j + 1])
        a, b, c, d = float(v0[j, i]), float(v1[j, i]), float(v2[j, i]), float(v3[j, i])

        def lerp(pa, pb, va, vb):
            t = (iso - va) / (vb - va) if vb != va else 0.5
            return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))

        e = (
            lerp((xa, ya), (xb, ya), a, b),
            lerp((xb, ya), (xb, yb), b, c),
            lerp((xb, yb), (xa, yb), c, d),
            lerp((xa, yb), (xa, ya), d, a),
        )
        for p, q in _MS_TABLE[int(case[j, i])]:
            segs.append((e[p], e[q]))
    return [list(ch) for ch in _chain_segments(segs)]


# ===========================================================================
# outlines + distance fields
# ===========================================================================
def _amoeba(harmonics: Sequence[Tuple[int, float, float]], n: int = 300) -> Poly:
    """Closed radial blob r(theta) = 1 + sum a_k cos(k theta + phi_k), unit scale.

    A DOMINANT k = 3 term is the whole trick.  A near-convex blob's distance
    field has one long medial ridge, so its rings come out as a plain onion;
    a trefoil with waists deep enough to pinch (a_3 ~ 0.46) has a Y-shaped
    medial axis, and the rings split into the reference's three fingerprint
    eyes.  The smaller harmonics only break the symmetry.
    """
    pts: Poly = []
    for k in range(n):
        t = 2 * math.pi * k / n
        r = 1.0
        for kk, a, ph in harmonics:
            r += a * math.cos(kk * t + ph)
        pts.append((r * math.cos(t), r * math.sin(t)))
    return pts


def _fit_poly(poly: Poly, box: Bounds) -> Poly:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, y0, x1, y1 = box
    sx = (x1 - x0) / (max(xs) - min(xs))
    sy = (y1 - y0) / (max(ys) - min(ys))
    return [(x0 + (p[0] - min(xs)) * sx, y0 + (p[1] - min(ys)) * sy) for p in poly]


def _dist_field(poly: Poly, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Distance to the boundary, positive INSIDE, 0 outside. |grad| = 1 inside."""
    P = np.asarray(poly, float)
    A = P
    B = np.roll(P, -1, axis=0)
    d = np.full(X.shape, 1e9)
    inside = np.zeros(X.shape, bool)
    for (ax, ay), (bx, by) in zip(A, B):
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        if L2 > 1e-12:
            t = np.clip(((X - ax) * vx + (Y - ay) * vy) / L2, 0.0, 1.0)
            d = np.minimum(d, np.hypot(X - (ax + t * vx), Y - (ay + t * vy)))
        if (ay > Y).any() or (by > Y).any():
            cond = (ay > Y) != (by > Y)
            if cond.any():
                xint = np.where(
                    abs(by - ay) > 1e-12, ax + (Y - ay) * vx / (by - ay + 1e-30), ax
                )
                inside ^= cond & (X < xint)
    return np.where(inside, d, 0.0)


def _grid(box: Bounds, step: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x0, y0, x1, y1 = box
    xs = np.arange(x0, x1 + step, step)
    ys = np.arange(y0, y1 + step, step)
    X, Y = np.meshgrid(xs, ys)
    return xs, ys, X, Y


def _cone_levels(peak: float, sigma: float, pitch: float, n: int, base: float = 0.0):
    """Level ladder for a CONICAL field that gives a uniform RADIAL pitch.

    For ``F = a exp(-r/sigma)`` the ring at level ``F_k`` sits at
    ``r_k = sigma ln(a/F_k)``, so a ladder of UNIFORM LEVEL STEPS puts the
    radii at ``sigma ln((k+1)/k)`` apart — 0.69*sigma for the first gap and
    ``sigma/k`` near the summit.  At 16 levels on a sigma = 5.4 mm cusp the
    innermost gap is 0.33 mm, well under the 0.85 mm plotting floor, and the
    eye floods.  A GEOMETRIC ladder, ``F_k = a exp(-k pitch / sigma)``, puts
    the rings at exactly ``pitch`` apart everywhere, which is the whole reason
    the field is conical in the first place.
    """
    return [base + peak * math.exp(-k * pitch / sigma) for k in range(1, n + 1)]


def _cusps(X: np.ndarray, Y: np.ndarray, cusps: Sequence[Tuple[float, float, float, float]]):
    """sum a * exp(-r/sigma) — CONICAL, so uniform levels give uniform ring pitch."""
    F = np.zeros(X.shape)
    for cx, cy, sig, amp in cusps:
        F += amp * np.exp(-np.hypot(X - cx, Y - cy) / sig)
    return F


def _fbm_grid(rng: SeededRNG, X: np.ndarray, Y: np.ndarray, scale: float, oct_: int = 3):
    Z = np.zeros(X.shape)
    amp, frq = 1.0, 1.0
    norm = 0.0
    for _ in range(oct_):
        ox, oy = rng.uniform(-40, 40), rng.uniform(-40, 40)
        Z += amp * _value_noise(X * scale * frq + ox, Y * scale * frq + oy)
        norm += amp
        amp *= 0.5
        frq *= 2.0
    return Z / norm


def _value_noise(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    i0, j0 = np.floor(U).astype(int), np.floor(V).astype(int)
    fu, fv = U - i0, V - j0
    su = fu * fu * (3 - 2 * fu)
    sv = fv * fv * (3 - 2 * fv)

    def h(a, b):
        n = (a * 374761393 + b * 668265263) & 0xFFFFFFFF
        n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFFFF) / 0xFFFFFF

    a00, a10 = h(i0, j0), h(i0 + 1, j0)
    a01, a11 = h(i0, j0 + 1), h(i0 + 1, j0 + 1)
    return (a00 * (1 - su) + a10 * su) * (1 - sv) + (a01 * (1 - su) + a11 * su) * sv


# ===========================================================================
# stroke helpers
# ===========================================================================
def _dash(poly: Poly, on: float = 2.2, off: float = 1.9, phase: float = 0.0) -> List[Poly]:
    """Split a polyline into dashes of ``on`` mm separated by ``off`` mm.

    The phase is carried as an explicit on/off state with a remaining length,
    never as ``arclength % period``: the modulo form lands epsilon below the
    switch point once float error accumulates, the step collapses to ~1e-16 and
    the walk never terminates.
    """
    out: List[Poly] = []
    cur: Poly = []
    period = on + off
    s = phase % period if period > 0 else 0.0
    drawing = s < on
    rem = (on - s) if drawing else (period - s)
    for p, q in zip(poly, poly[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        seg = math.hypot(dx, dy)
        if seg < 1e-12:
            continue
        t = 0.0
        while t < seg - 1e-12:
            step = min(rem, seg - t)
            if drawing:
                a = (p[0] + dx * t / seg, p[1] + dy * t / seg)
                t2 = t + step
                b = (p[0] + dx * t2 / seg, p[1] + dy * t2 / seg)
                if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
                    cur.append(b)
                else:
                    if len(cur) >= 2:
                        out.append(cur)
                    cur = [a, b]
            else:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
            t += step
            rem -= step
            if rem <= 1e-12:
                drawing = not drawing
                rem = on if drawing else off
    if len(cur) >= 2:
        out.append(cur)
    return out


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 64) -> Poly:
    out: Poly = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        out.append(
            (
                m**3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t**3 * p3[0],
                m**3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t**3 * p3[1],
            )
        )
    return out


def _ellipse(cx: float, cy: float, rx: float, ry: float, rot: float = 0.0, n: int = 220) -> Poly:
    ca, sa = math.cos(rot), math.sin(rot)
    out: Poly = []
    for k in range(n + 1):
        t = 2 * math.pi * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return out


def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _guard_spacing(cmds: List[GCodeCommand], min_dist: float = 0.80) -> List[GCodeCommand]:
    """``enforce_line_spacing`` + re-emit, so every stroke keeps a leading G0.

    The policy rebuilds strokes and can drop the ``G0`` that positions one; the
    merged program then starts that stroke from the machine origin, which shows
    up as a stray point at (0, 0) and a bounds violation.  Re-emitting from the
    thinned runs is cheap and makes the guard safe to use anywhere.
    """
    thinned = enforce_line_spacing(cmds, min_dist=min_dist, resample=0.40)
    runs: List[Poly] = []
    cur: Poly = []
    pen: Optional[int] = None
    for c in thinned:
        if c.command == "G0" and c.x is not None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [(c.x, c.y)]
        elif c.command == "M3":
            pen = c.color if c.color is not None else pen
        elif c.command == "G1" and c.x is not None:
            cur.append((c.x, c.y))
            if c.color is not None:
                pen = c.color
        elif c.command == "M5":
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return _emit(runs, pen)


def _clip_out(polys: Sequence[Poly], region: Region) -> List[Poly]:
    out: List[Poly] = []
    for p in polys:
        out.extend(clip(p, region, keep="outside"))
    return out


def _clip_in(polys: Sequence[Poly], box: Bounds) -> List[Poly]:
    """Keep the parts of each polyline INSIDE an axis-aligned box.

    A dedicated Liang-Barsky clip rather than ``geometry.clip``: the tiles,
    kernel cells and feature maps between them clip a few thousand contour
    chains, and the general Region machinery costs four half-plane calls per
    segment. ``geometry.clip`` is still used where the region is not a plain
    box (the strip knockout) and exactness at the boundary matters.
    """
    x0, y0, x1, y1 = box
    out: List[Poly] = []
    for poly in polys:
        cur: Poly = []
        for p, q in zip(poly, poly[1:]):
            t0, t1 = 0.0, 1.0
            dx, dy = q[0] - p[0], q[1] - p[1]
            ok = True
            for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
                if pp == 0.0:
                    if qq < 0.0:
                        ok = False
                        break
                    continue
                r = qq / pp
                if pp < 0.0:
                    if r > t1:
                        ok = False
                        break
                    if r > t0:
                        t0 = r
                else:
                    if r < t0:
                        ok = False
                        break
                    if r < t1:
                        t1 = r
            if not ok:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
                continue
            a = (p[0] + dx * t0, p[1] + dy * t0)
            b = (p[0] + dx * t1, p[1] + dy * t1)
            if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
                cur.append(b)
            else:
                if len(cur) >= 2:
                    out.append(cur)
                cur = [a, b]
            if t1 < 1.0 - 1e-12:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
        if len(cur) >= 2:
            out.append(cur)
    return out


def _rect(x0: float, y0: float, x1: float, y1: float) -> Poly:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def _disc(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid dot as a tight spiral — small enough that a spiral cannot flood."""
    turns = max(3, int(r / 0.20))
    n = turns * 22
    pts = [
        (
            x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            y + r * (k / n) * math.sin(2 * math.pi * turns * k / n),
        )
        for k in range(n + 1)
    ]
    pts.append((x + r, y))
    return _poly(pts, color=pen, f=1600) + circle(x, y, r, pen=pen, f=1600, n=26)


# ===========================================================================
# 1. the ring-filled blobs (X input, Y output)
# ===========================================================================
def _ring_blob(
    rng: SeededRNG,
    outline: Poly,
    box: Bounds,
    pen: int,
    pitch: float = 0.95,
    smudges: Sequence[Tuple[float, float, float, float]] = (),
) -> List[GCodeCommand]:
    """Amoeba filled with concentric contour rings that follow its own outline.

    The field is the DISTANCE to the boundary: |grad d| = 1 everywhere, so a
    uniform level ladder gives a ring pitch of exactly ``pitch`` — the
    fingerprint stays tight all the way to the medial axis, where the rings
    split into the reference's 'eyes'.  A small fbm perturbation adds the
    hand-drawn wobble; its gradient is bounded at ~0.13 so the worst-case pitch
    stays above the plotting floor.
    """
    x0, y0, x1, y1 = box
    pad = 2.0
    xs, ys, X, Y = _grid((x0 - pad, y0 - pad, x1 + pad, y1 + pad), 0.42)
    D = _dist_field(outline, X, Y)
    wob = (_fbm_grid(rng, X, Y, 1.0 / 13.0, 3) - 0.5) * 2.0 * (0.30 * pitch)
    F = np.where(D > 0, D + wob, 0.0)

    out: List[GCodeCommand] = []
    rings_cmds: List[GCodeCommand] = []

    dmax = float(F.max())
    k = 1
    while k * pitch < dmax:
        lvl = k * pitch
        chains = _iso_chains(F, xs, ys, lvl)
        if k == 2:
            dashed: List[Poly] = []
            for ch in chains:
                dashed += _dash(ch, 3.4, 1.5, phase=1.7)
            rings_cmds += _emit(dashed, pen)
        else:
            rings_cmds += _emit(chains, pen)
        k += 1

    # A trefoil's distance field is exactly what makes the fingerprint eyes,
    # and it is also why two branches of one contour run together to nothing
    # just before they merge at a waist: measured median neighbour spacing was
    # 0.05 mm there.  That convergence is geometric, not a parameter, so the
    # house guardrail thins it instead of the pitch being raised everywhere.
    out += _guard_spacing(rings_cmds, 0.80)

    # the boundary is the heaviest line on the blob: two passes, drawn AFTER
    # the guard so the deliberate 0.28 mm double-stroke survives it
    out += _emit([outline + [outline[0]]], pen)
    out += _emit(
        [[(px + 0.28, py) for px, py in outline] + [(outline[0][0] + 0.28, outline[0][1])]],
        pen,
    )

    # the reference's dark smudges: tone_dots, so density is bounded by the
    # cell size however dark the tone goes — a hand-rolled stipple would flood.
    for sm in smudges:
        sx, sy, sr, amp = sm

        def tone(px, py, sx=sx, sy=sy, sr=sr, amp=amp):
            if not _pt_in_poly(px, py, outline):
                return 0.0
            return max(0.0, 1.0 - (math.hypot(px - sx, py - sy) / sr) ** 1.6) * amp

        out += tone_dots((sx - sr, sy - sr, sx + sr, sy + sr), tone, rng, pen=pen, cell=0.95)

    # loose dots of many sizes over the whole blob, as in the reference
    for _ in range(46):
        px = rng.uniform(x0, x1)
        py = rng.uniform(y0, y1)
        if not _pt_in_poly(px, py, outline):
            continue
        out += _disc(px, py, rng.choice([0.45, 0.6, 0.85, 1.15]), pen)

    return out


def _label_slot(
    outline: Poly, box: Bounds, side: int, cap: float, w: float, clear: float = 3.0
) -> Tuple[float, float]:
    """Find a baseline for a display label beside a blob, with real clearance.

    Scans candidate heights over the blob's middle third and returns the one
    where the gap between the blob's silhouette and the box edge is largest,
    so the label always lands on paper.
    """
    x0, y0, x1, y1 = box
    best = None
    for k in range(24):
        v = 0.20 + 0.60 * k / 23.0
        py = y1 - v * (y1 - y0)
        band = [p[0] for p in outline if abs(p[1] - py) < cap * 0.75]
        if not band:
            continue
        gap = (min(band) - x0) if side < 0 else (x1 - max(band))
        if best is None or gap > best[0]:
            best = (gap, py, min(band) if side < 0 else max(band))
    if best is None:
        return (x0, (y0 + y1) / 2.0)
    gap, py, edge = best
    lx = (edge - w - clear) if side < 0 else (edge + clear)
    lx = min(max(lx, x0 - w - clear - 1.0), x1 + clear + 1.0)
    return (lx, py - cap * 0.5)


def _pt_in_poly(px: float, py: float, poly: Poly) -> bool:
    inside = False
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        if (ay > py) != (by > py):
            if px < ax + (py - ay) * (bx - ax) / (by - ay + 1e-30):
                inside = not inside
    return inside


# ===========================================================================
# 2. the five centre tiles — radial burst / vortex
# ===========================================================================
def _burst_tile(
    rng: SeededRNG,
    box: Bounds,
    pen: int,
    n_eyes: int = 2,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2.0
    cy = (y0 + y1) / 2.0
    w, h = x1 - x0, y1 - y0
    keep = (x0 + 0.25, y0 + 0.25, x1 - 0.25, y1 - 0.25)
    out: List[GCodeCommand] = []

    # secondary eyes, offset from the main one
    # every cusp's sigma stays close to the main one: a level ladder is set by
    # the TIGHTEST cusp in the field, and a sigma-2.1 secondary next to a
    # sigma-5.4 primary forced the primary's rings to 0.37 mm to keep the
    # secondary legal.
    cusps = [(cx, cy, 5.4, 1.0)]
    for _ in range(n_eyes):
        cusps.append(
            (
                cx + rng.uniform(-0.34, 0.34) * w,
                cy + rng.uniform(-0.32, 0.32) * h,
                rng.uniform(3.6, 4.6),
                rng.uniform(0.34, 0.52),
            )
        )

    xs, ys, X, Y = _grid((x0 - 1, y0 - 1, x1 + 1, y1 + 1), 0.30)
    F = _cusps(X, Y, cusps)
    F += 0.055 * (_fbm_grid(rng, X, Y, 1.0 / 7.0, 3) - 0.5)

    # geometric ladder -> exactly 1.0 mm between rings, summit included
    rings: List[Poly] = []
    for lvl in _cone_levels(float(F.max()), min(cu[2] for cu in cusps), 0.95, 20):
        rings += _iso_chains(F, xs, ys, lvl)
    rings = _clip_in(rings, keep)
    # dotted contours — the reference's tiles are stippled, not line-drawn
    dashed: List[Poly] = []
    for ch in rings:
        dashed += _dash(ch, 1.05, 0.72, phase=rng.uniform(0, 1.7))
    out += _emit(dashed, pen, f=2600)

    # radial rays out of the main eye, curled into a vortex
    n_rays = 22
    for k in range(n_rays):
        a0 = 2 * math.pi * k / n_rays + rng.uniform(-0.05, 0.05)
        rmax = rng.uniform(0.30, 0.72) * max(w, h) * 0.62
        curl = rng.uniform(-0.22, 0.22)
        ray = []
        r = 1.1
        while r < rmax:
            a = a0 + curl * math.log(max(r, 1.0))
            ray.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            r += 0.6
        out += _emit(_clip_in([ray], keep), pen, f=2600)

    # scattered dots of many sizes
    for _ in range(72):
        px = rng.uniform(x0 + 0.8, x1 - 0.8)
        py = rng.uniform(y0 + 0.8, y1 - 0.8)
        rr = math.hypot(px - cx, py - cy)
        if rng.random() > math.exp(-rr / 9.0) * 0.95 + 0.06:
            continue
        s = rng.choice([0.28, 0.28, 0.4, 0.55, 0.75])
        out += _disc(px, py, s, pen if rng.random() < 0.72 else BLACK)

    out += _disc(cx, cy, 1.45, pen)
    out += _disc(cx, cy, 1.0, BLACK)
    out += _emit([_rect(x0, y0, x1, y1)], BLACK, f=1800)
    return out


# ===========================================================================
# 3. the kernel bank — this is what makes the plate about CONVOLUTION
# ===========================================================================
def _kernel_cell(
    rng: SeededRNG,
    box: Bounds,
    pen: int,
    tap: Tuple[int, int],
    hatch_cells: Sequence[Tuple[int, int]],
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sw, sh = w / 3.0, h / 3.0
    out: List[GCodeCommand] = []
    keep = (x0 + 0.2, y0 + 0.2, x1 - 0.2, y1 - 0.2)

    # 3x3 subdivision in the cell's own colour
    for k in (1, 2):
        out += _emit([[(x0 + k * sw, y0), (x0 + k * sw, y1)]], pen, f=2400)
        out += _emit([[(x0, y0 + k * sh), (x1, y0 + k * sh)]], pen, f=2400)

    # hatched sub-cells
    for (i, j) in hatch_cells:
        hx0, hy0 = x0 + i * sw, y0 + j * sh
        for t in np.arange(-sh, sw + sh, 1.15):
            a = (hx0 + t, hy0)
            b = (hx0 + t + sh, hy0 + sh)
            out += _emit(
                _clip_in([[a, b]], (hx0 + 0.15, hy0 + 0.15, hx0 + sw - 0.15, hy0 + sh - 0.15)),
                pen,
                f=2600,
            )

    # dot lattice — 2 dots per sub-cell axis => 6x6 over the cell
    for j in range(6):
        for i in range(6):
            px = x0 + (i + 0.5) * w / 6.0
            py = y0 + (j + 0.5) * h / 6.0
            r = 0.26 if (i % 2 and j % 2) else 0.36
            out += _disc(px, py, r, BLACK if rng.random() < 0.45 else pen)

    # the tap: a conical whorl in the cell colour with a solid black centre
    tx = x0 + (tap[0] + 0.5) * sw
    ty = y0 + (tap[1] + 0.5) * sh
    xs, ys, X, Y = _grid((x0 - 0.5, y0 - 0.5, x1 + 0.5, y1 + 0.5), 0.26)
    F = _cusps(X, Y, [(tx, ty, 3.4, 1.0)])
    # 4-lobed clover, as in the reference
    TH = np.arctan2(Y - ty, X - tx)
    F *= 1.0 - 0.42 * np.cos(2 * TH)
    F += 0.03 * (_fbm_grid(rng, X, Y, 1.0 / 4.0, 2) - 0.5)
    rings: List[Poly] = []
    for lvl in _cone_levels(float(F.max()), 3.4, 0.95, 11):
        rings += _iso_chains(F, xs, ys, lvl)
    dashed: List[Poly] = []
    for ch in _clip_in(rings, keep):
        dashed += _dash(ch, 0.85, 0.62, phase=rng.uniform(0, 1.4))
    out += _emit(dashed, pen, f=2600)

    out += _disc(tx, ty, 1.45, pen)
    out += _disc(tx, ty, 1.0, BLACK)
    out += _emit([_rect(x0, y0, x1, y1)], BLACK, f=1800)
    return out


# ===========================================================================
# 4. the receptive-field cone
# ===========================================================================
def _receptive_cone(
    rng: SeededRNG, apex: Pt, base_y: float, half: float, pen: int = BLACK
) -> List[GCodeCommand]:
    """The receptive field: a dashed PARABOLA envelope over a nest of closed
    teardrop contours, a bounded stipple and the apex dot ladder.

    Measured off the reference crop rather than guessed: the envelope is a
    parabola (not a triangle), the solid contours reach only ~0.5 of the
    envelope's half-width, the stipple ~0.65, and most of the figure is white
    paper.  Two earlier attempts contoured a radial field inside a triangular
    wedge and both came out as a solid black wedge — the contours are drawn
    explicitly here so their pitch is exact and the paper survives.
    """
    ax, ay = apex
    H = ay - base_y
    out: List[GCodeCommand] = []

    # --- dashed parabola envelope -------------------------------------
    env = [
        (ax + half * t, ay - H * t * t)
        for t in [(-40 + k) / 40.0 for k in range(81)]
    ]
    out += _emit(_dash(env, 3.0, 2.6), pen, f=2400)

    def in_env(px, py):
        t = abs(px - ax) / half
        return base_y - 1e-6 <= py <= ay - H * t * t + 1e-6

    # --- nested teardrops: ellipses whose centre walks down as they grow,
    #     so each loop hugs the apex above and bulges toward the mouth.
    # Each loop is a TEARDROP, not an ellipse: narrow where it hugs the eye,
    # flaring toward the mouth.  The three growth rates are set so the pitch
    # is >= 1.1 mm at the crown (0.34), 1.9 mm across (0.58) and 5.1 mm at the
    # bottom (1.55) — the crown is the only place a nested family can crowd.
    cy = ay - 0.20 * H
    pitch = 3.30
    up, down, wide = 0.34, 1.55, 0.66
    # hw(u) = C u^0.85 (1-u)^0.5 : zero at the crown, zero at the mouth, widest
    # at 63% down.  The earlier u^0.6 form never returned to zero, so every
    # loop closed with a horizontal jump and the nest read as stacked U-tubes.
    p_top, p_bot = 0.85, 0.50
    u_max = p_top / (p_top + p_bot)
    norm = 1.0 / (u_max**p_top * (1.0 - u_max) ** p_bot)
    for k in range(1, 10):
        r = k * pitch
        ytop, ybot, Wk = cy + up * r, cy - down * r, wide * r
        loop: Poly = []
        for sgn in (1.0, -1.0):
            rng_m = range(73) if sgn > 0 else range(71, -1, -1)
            for m in rng_m:
                u = m / 72.0
                hw = Wk * norm * (u**p_top) * ((1.0 - u) ** p_bot)
                loop.append((ax + sgn * hw, ytop - (ytop - ybot) * u))
        loop.append(loop[0])
        run: Poly = []
        for pt in loop:
            if in_env(*pt):
                run.append(pt)
            else:
                if len(run) >= 2:
                    out += _emit([run], pen, f=2500)
                run = []
        if len(run) >= 2:
            out += _emit([run], pen, f=2500)

    # --- stipple: a grey core at the apex plus a speckled band toward the
    #     mouth.  tone_dots, so density is capped at 1/cell^2 by construction.
    def tone(px, py):
        if not in_env(px, py):
            return 0.0
        core = 0.88 * math.exp(-math.hypot((px - ax) * 1.5, py - cy) / 6.5)
        t = (ay - py) / H
        edge = abs(px - ax) / max(half * math.sqrt(max(t, 1e-6)), 1e-6)
        band = 0.40 * max(0.0, t - 0.30) * 1.4 * (0.25 + 0.75 * edge**2.0)
        return min(0.88, core + band)

    out += tone_dots((ax - half, base_y, ax + half, ay), tone, rng, pen=pen, cell=1.05)

    # --- apex dot ladder + spine --------------------------------------
    out += _emit(_dash([(ax, ay + 7.0), (ax, base_y - 3.0)], 2.6, 2.6), pen, f=2400)
    out += _disc(ax, cy, 1.70, pen)
    out += _disc(ax, ay, 1.15, pen)
    out += _disc(ax, ay + 5.6, 0.62, pen)
    for k in range(3):
        out += _disc(ax, cy + (k + 1) * 0.30 * H / 3.0, 0.52 - 0.10 * k, pen)
    return out


# ===========================================================================
# 5. the feature maps — flow-field contour squares
# ===========================================================================
def _feature_map(rng: SeededRNG, box: Bounds, pen: int) -> List[GCodeCommand]:
    x0, y0, x1, y1 = box
    keep = (x0 + 0.25, y0 + 0.25, x1 - 0.25, y1 - 0.25)
    xs, ys, X, Y = _grid((x0 - 1, y0 - 1, x1 + 1, y1 + 1), 0.34)
    # a FLOW field, not a bullseye: anisotropic cusps sheared along one
    # common direction, then domain-warped, so the isolines stream.
    th = rng.uniform(-0.7, 0.7)
    ca, sa = math.cos(th), math.sin(th)
    WX = (X - x0) * ca + (Y - y0) * sa
    WY = -(X - x0) * sa + (Y - y0) * ca
    warp = 1.9 * (_fbm_grid(rng, X, Y, 1.0 / 8.0, 3) - 0.5)
    F = np.zeros(X.shape)
    # The anisotropy is kept mild (0.85 / 1.25 rather than 0.62 / 1.5) so the
    # ratio between the field's broadest and tightest directions is 1.47, not
    # 2.4.  A geometric ladder is set by the TIGHTEST direction, and at 2.4
    # the ladder that kept the tight axis legal left the broad axis with six
    # lonely contours per tile.
    sg_tight = 99.0
    for _ in range(4):
        cu = rng.uniform(3.0, (x1 - x0) - 3.0)
        cv = rng.uniform((y1 - y0) * 0.05, (y1 - y0) * 0.85)
        sg = rng.uniform(4.6, 8.0)
        sg_tight = min(sg_tight, sg / 1.25)
        F += rng.uniform(0.60, 1.0) * np.exp(
            -np.hypot((WX - cu + warp) * 0.85, (WY - cv) * 1.25) / sg
        )
    F += 0.11 * (_fbm_grid(rng, X, Y, 1.0 / 10.0, 3) - 0.5)
    out: List[GCodeCommand] = []
    lo, hi = float(F.min()), float(F.max())
    rings: List[Poly] = []
    for lvl in _cone_levels(hi - lo, sg_tight, 1.25, 18, base=lo):
        rings += _iso_chains(F, xs, ys, lvl)
    out += _guard_spacing(_emit(_clip_in(rings, keep), pen, f=2500), 0.80)
    for _ in range(3):
        out += _disc(rng.uniform(x0 + 3, x1 - 3), rng.uniform(y0 + 3, y1 - 3), 0.8, BLACK)
    out += _emit([_rect(x0, y0, x1, y1)], BLACK, f=1800)
    return out


# ===========================================================================
# the plate
# ===========================================================================
def convolutions(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    fr = Frame(bounds)
    out: List[GCodeCommand] = []

    def U(u):
        return fr.u(u)

    def V(v):
        return fr.v(v)

    # ---------------- geometry of placement (all derived, nothing hard-coded
    # in mm off the frame edges) --------------------------------------------
    strip_w = N_TILES * TILE_W + (N_TILES - 1) * TILE_GAP
    strip_x0 = U(STRIP_CU) - strip_w / 2.0
    tile_top = V(TILE_TOP_V)
    tile_bot = tile_top - TILE_H
    tiles: List[Bounds] = []
    for k in range(N_TILES):
        tx0 = strip_x0 + k * (TILE_W + TILE_GAP)
        tiles.append((tx0, tile_bot, tx0 + TILE_W, tile_top))

    base_y = V(BASE_V)
    lower_top = V(LOWER_TOP_V)
    cap_base = V(CAP_BASE_V)

    # Both outer zones are 3 * ZONE_CELL_W + 2 * CELL_GAP wide, one is flush
    # left and one flush right, and the cone is centred -> the two gutters are
    # identical by construction rather than by luck.
    zone_w = 3 * ZONE_CELL_W + 2 * CELL_GAP
    kb_x0 = U(0.0)
    kb_h = 3 * KB_CELL_H + 2 * CELL_GAP
    kb_y1 = base_y + kb_h
    fm_x1 = U(1.0)
    fm_x0 = fm_x1 - zone_w
    cone_x = U(0.5)
    kb_w = fm_w = zone_w

    # ---------------- 1. header --------------------------------------------
    out += _text_at(
        "CONVOLUTIONS",
        V(TITLE_V) - TITLE_CAP,
        TITLE_CAP,
        BLACK,
        left=U(0.0),
        target_w=TITLE_W,
    )
    out += _emit([[(U(0.0), V(RULE_V)), (U(0.0) + 7.6, V(RULE_V))]], BLACK, f=1800)
    for line, vv in zip(
        ("local patterns", "global structures", "continuous perception"), SUB_V
    ):
        out += _text_at(line, V(vv) - SUB_CAP, SUB_CAP, BLACK, left=U(0.0), target_w=SUB_W)

    ur_left = U(1.0) - UR_W
    for line, vv in zip(("stride", "padding", "dilation", "channels"), UR_V):
        out += _text_at(line, V(vv) - UR_CAP, UR_CAP, BLACK, left=ur_left, target_w=UR_W)
    out += _emit([[(ur_left, V(UR_RULE_V)), (ur_left + 10.3, V(UR_RULE_V))]], BLACK, f=1800)

    # ---------------- 2. the two blobs -------------------------------------
    bx_box = (U(BX_U[0]), V(BX_V[1]), U(BX_U[1]), V(BX_V[0]))
    by_box = (U(BY_U[0]), V(BY_V[1]), U(BY_U[1]), V(BY_V[0]))

    # phi_3 places the three lobes.  X: peaks at 45 / 165 / 285 deg, which the
    # box's vertical stretch turns into the reference's upper-right,
    # upper-left and long lower lobe.  Y is the same construction, rotated.
    x_out = _fit_poly(
        _amoeba([(3, 0.46, -2.356), (2, 0.15, 0.55), (1, 0.10, -0.60), (5, 0.06, 2.2)]),
        bx_box,
    )
    y_out = _fit_poly(
        _amoeba([(3, 0.45, -0.95), (2, 0.13, -1.30), (1, 0.09, 1.80), (5, 0.055, 0.4)]),
        by_box,
    )
    bxc = ((bx_box[0] + bx_box[2]) / 2.0, (bx_box[1] + bx_box[3]) / 2.0)
    byc = ((by_box[0] + by_box[2]) / 2.0, (by_box[1] + by_box[3]) / 2.0)

    out += _ring_blob(
        rng,
        x_out,
        bx_box,
        BLACK,
        pitch=0.95,
        smudges=((bxc[0] - 4.0, bxc[1] + 8.0, 8.0, 0.92), (bxc[0] + 5.0, bxc[1] - 9.0, 5.5, 0.55)),
    )
    out += _ring_blob(rng, y_out, by_box, OLIVE, pitch=1.0, smudges=())

    # hub dots on each blob (where the connector bundles attach)
    x_hub = (bx_box[2] - 5.0, bxc[1] + 3.0)
    y_hub = (by_box[0] + 5.0, byc[1] + 4.0)
    out += _disc(*x_hub, 1.5, BLACK)
    out += _disc(*y_hub, 1.5, BLACK)
    for _ in range(9):
        out += _disc(
            rng.uniform(by_box[0] + 3, by_box[2] - 3),
            rng.uniform(by_box[1] + 3, by_box[3] - 3),
            rng.choice([0.55, 0.8, 1.1]),
            BLACK,
        )

    # ---------------- 3. labels around the blobs ---------------------------
    # The labels sit in the paper BESIDE each blob, never on it: the slot is
    # searched for rather than guessed, so a reshaped blob can't collide with
    # its own label.  (The reference lets 'X' graze the outline; 3 mm of
    # clearance costs the plate nothing, so that overlap was crowding.)
    xl, xb = _label_slot(x_out, bx_box, side=-1, cap=3.95, w=4.6, clear=3.0)
    out += _text_at("X", xb, 3.95, BLACK, left=xl)
    yl, yb = _label_slot(y_out, by_box, side=+1, cap=4.65, w=5.4, clear=3.0)
    out += _text_at("Y", yb, 4.65, BLACK, left=yl)

    cr_x = U(0.026)
    cr_y = V(0.508)
    out += _emit([[(cr_x, V(0.478)), (cr_x, V(0.534))]], BLACK, f=2200)
    out += _emit([[(U(0.0), cr_y), (U(0.128), cr_y)]], BLACK, f=2200)
    out += _text_at("input x", V(0.4955), 2.5, BLACK, left=U(0.052), target_w=17.0)
    out += _disc(cr_x, V(0.5335), 1.05, BLACK)

    # ---------------- 4. the tile strip ------------------------------------
    # protected slab: the big dashed ellipses never enter it
    slab = Rect(
        strip_x0 - 2.6, tile_bot - 2.6, strip_x0 + strip_w + 2.6, tile_top + 2.6
    )
    # the two display labels keep their own clear boxes, from every layer
    label_boxes = Union(
        Rect(tiles[2][0] - 3.0, V(0.262) - 1.2, tiles[2][2] + 3.0, V(0.262) + 5.6),
        Rect(tiles[3][2] - 2.5, V(0.262) - 1.2, tiles[4][0] + 2.5, V(0.262) + 5.6),
    )
    # per-tile knockouts: sweeping connectors pass BEHIND each tile
    tile_regions = Union(
        *[Rect(t[0] - 1.1, t[1] - 1.1, t[2] + 1.1, t[3] + 1.1) for t in tiles],
        label_boxes,
    )

    # ---------------- 5. connector bundles (drawn under the tiles) ---------
    conn: List[Tuple[Poly, int, bool]] = []
    t0 = tiles[0]
    n_in = 10
    for k in range(n_in):
        fy = t0[1] + (k + 0.5) * (t0[3] - t0[1]) / n_in
        sag = (k / (n_in - 1.0) - 0.5) * 34.0 + rng.uniform(-4.0, 4.0)
        curve = _bez(
            x_hub,
            (x_hub[0] + 15.0, x_hub[1] + sag * 0.9),
            (t0[0] - 20.0, fy + sag * 0.55),
            (t0[0] + TILE_W * 0.5, fy),
            76,
        )
        pen = (RED, BLACK, BLACK, RED, BLACK, BLACK, RED, BLACK, RED, BLACK)[k]
        conn.append((curve, pen, k in (1, 4, 8)))
    # long sweeps that cross the whole strip and continue to Y
    t4 = tiles[-1]
    for k in range(6):
        fy = t4[1] + (k + 0.5) * (t4[3] - t4[1]) / 6.0
        sag = rng.uniform(-11.0, 11.0)
        curve = _bez(
            (t4[2] - TILE_W * 0.5, fy),
            (t4[2] + 20.0, fy + sag),
            (y_hub[0] - 22.0, y_hub[1] + sag * 0.5),
            y_hub,
            72,
        )
        conn.append((curve, (OLIVE, BLUE, OLIVE, BLUE, OLIVE, BLUE)[k], k == 3))
    # two long dashed arcs that leave X, rise well over the strip and drop
    # back onto it — the reference's signature sweep, kept because it ties the
    # input to the whole chain rather than to one tile.
    for k, (pen, lift, land) in enumerate(
        ((RED, 30.0, 1), (BLACK, 22.0, 2))
    ):
        tgt = tiles[land]
        conn.append(
            (
                _bez(
                    x_hub,
                    (x_hub[0] + 24.0, x_hub[1] + lift),
                    (tgt[0] - 10.0, tgt[3] + lift * 0.9),
                    ((tgt[0] + tgt[2]) / 2.0, tgt[3] + 1.0),
                    80,
                ),
                pen,
                True,
            )
        )

    # inter-tile links, living in the widened gaps
    for k in range(N_TILES - 1):
        a, b = tiles[k], tiles[k + 1]
        for m in range(3):
            ya = a[1] + (m + 0.7) * (a[3] - a[1]) / 3.5
            yb = b[1] + (m + 0.7) * (b[3] - b[1]) / 3.5 + rng.uniform(-2.5, 2.5)
            curve = _bez(
                (a[2] - 2.0, ya),
                (a[2] + TILE_GAP * 0.45, ya),
                (b[0] - TILE_GAP * 0.45, yb),
                (b[0] + 2.0, yb),
                34,
            )
            conn.append((curve, TILE_PENS[k], False))

    for curve, pen, dashed in conn:
        parts = _clip_out([curve], tile_regions)
        if dashed:
            dd: List[Poly] = []
            for p in parts:
                dd += _dash(p, 2.4, 2.0)
            parts = dd
        out += _emit(parts, pen, f=2400)
        # the reference's fat dots riding the connectors
        if rng.random() < 0.7 and parts:
            p = rng.choice(parts)
            q = p[len(p) // 2]
            out += _disc(q[0], q[1], rng.choice([0.7, 0.95, 1.25]), BLACK)

    # ---------------- 6. the big dashed ellipses, ROUTED AROUND the strip ---
    # In the reference these cut straight through the five tiles and drop into
    # the zone below.  Here they are clipped out of THREE regions: the tile
    # slab (so the plate's main statement reads clean), the two display labels,
    # and everything below the flow band (so the gutter stays empty paper).
    # What survives is the part that arcs over and under the strip — which is
    # the one reading worth keeping: overlapping receptive fields.
    keep_out = Union(
        slab,
        Rect(fr.x0 - 5, V(GUTTER_V[0]) - 200.0, fr.x1 + 5, V(GUTTER_V[0])),
        label_boxes,
    )
    ell_specs = [
        (0.300, 0.420, 30.0, 17.0, -0.10, BLACK),
        (0.430, 0.432, 36.0, 21.0, 0.06, BLACK),
        (0.585, 0.424, 33.0, 18.0, -0.05, BLUE),
        (0.715, 0.432, 35.0, 20.0, 0.09, OLIVE),
        (0.500, 0.400, 59.0, 28.0, 0.0, BLACK),
    ]
    for cu, cv, rx, ry, rot, pen in ell_specs:
        e = _ellipse(U(cu), V(cv), rx, ry, rot)
        for part in _clip_out([e], keep_out):
            out += _emit(_dash(part, 2.9, 2.6), pen, f=2400)

    # tiles last, so they sit ON TOP of everything that swept past them
    for k, t in enumerate(tiles):
        out += _burst_tile(rng, t, TILE_PENS[k], n_eyes=2 if k % 2 == 0 else 1)
        # short droplines hanging off the strip
        out += _emit([[(t[0] + TILE_W * 0.35, t[3] + 1.6), (t[0] + TILE_W * 0.35, t[3] + 7.5)]],
                     BLACK, f=2400)

    out += _text_at("K * X", V(0.262), 3.95, BLACK, centre=(tiles[2][0] + tiles[2][2]) / 2.0,
                    target_w=15.2)
    # sigma(dot): neither glyph is in the shared 78-glyph font (see NOTES.md).
    sg_cap = 3.95
    sg_w = _sigma_w(sg_cap) + _text_width("( )", sg_cap, proportional=True)
    sg_x = (tiles[3][2] + tiles[4][0]) / 2.0 - sg_w / 2.0
    out += _sigma(sg_x, V(0.262), sg_cap, BLACK)
    out += _text_at("(", V(0.262), sg_cap, BLACK, left=sg_x + _sigma_w(sg_cap))
    out += _disc(sg_x + _sigma_w(sg_cap) + _text_width("( ", sg_cap, proportional=True) * 0.62,
                 V(0.262) + sg_cap * 0.33, 0.55, BLACK)
    out += _text_at(")", V(0.262), sg_cap, BLACK, left=sg_x + sg_w - _text_width(")", sg_cap, True))

    # ---------------- 7. lower band: kernel bank ---------------------------
    taps = [(1, 1), (1, 1), (1, 1), (0, 1), (1, 1), (1, 1), (1, 2), (1, 1), (1, 0)]
    hatches = [
        [],
        [],
        [],
        [],
        [],
        [(0, 0), (2, 0), (0, 2), (2, 2)],
        [(0, 2)],
        [(2, 0)],
        [(2, 0), (2, 1), (2, 2)],
    ]
    kb_pens = [RED, BLACK, BLUE, OLIVE, RED, RED, BLUE, OLIVE, BLACK]
    for j in range(3):
        for i in range(3):
            idx = j * 3 + i
            cx0 = kb_x0 + i * (ZONE_CELL_W + CELL_GAP)
            cy1 = kb_y1 - j * (KB_CELL_H + CELL_GAP)
            out += _kernel_cell(
                rng,
                (cx0, cy1 - KB_CELL_H, cx0 + ZONE_CELL_W, cy1),
                kb_pens[idx],
                taps[idx],
                hatches[idx],
            )
    out += _text_at("kernel bank", cap_base, 2.5, BLACK, centre=kb_x0 + kb_w / 2.0, target_w=24.5)

    # ---------------- 8. lower band: receptive field -----------------------
    out += _receptive_cone(rng, (cone_x, lower_top), base_y, CONE_HALF, BLACK)
    out += _text_at("receptive field", cap_base, 2.5, BLACK, centre=cone_x, target_w=31.2)

    # ---------------- 9. lower band: feature maps --------------------------
    for k, pen in enumerate((RED, BLUE, OLIVE)):
        cx0 = fm_x0 + k * (ZONE_CELL_W + CELL_GAP)
        out += _feature_map(rng, (cx0, base_y, cx0 + ZONE_CELL_W, base_y + FM_CELL_H), pen)
    out += _text_at(
        "feature maps", cap_base, 2.5, BLACK, centre=fm_x0 + fm_w / 2.0, target_w=28.6
    )

    # ---------------- 10. furniture ----------------------------------------
    out += _furniture(rng, fr, tiles, slab, (kb_x0, base_y, kb_x0 + kb_w, kb_y1),
                      (fm_x0, base_y, fm_x1, base_y + FM_CELL_H), cone_x, lower_top)
    return out


def _furniture(
    rng: SeededRNG,
    fr: Frame,
    tiles: Sequence[Bounds],
    slab: Region,
    kb: Bounds,
    fm: Bounds,
    cone_x: float,
    lower_top: float,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    U, V = fr.u, fr.v

    # the two dashed spines
    # the centre spine stops above the K*X label and resumes below the strip:
    # in the reference it runs straight through the 'K', which is a collision,
    # not a decision — 4 mm of clearance costs the axis nothing.
    for uu, v_lo, v_hi in ((0.500, 0.000, 0.232), (0.878, 0.000, 0.500)):
        out += _emit(
            _dash([(U(uu), V(v_lo)), (U(uu), V(v_hi))], 3.0, 3.4), BLACK, f=2400
        )
    out += _emit(_dash([(U(0.5), V(0.445)), (U(0.5), V(0.528))], 3.0, 3.4), BLACK, f=2400)

    # curved L-brackets
    for cu, cv, r, qx, qy in (
        (0.312, 0.052, 9.5, -1, -1),
        (0.560, 0.058, 8.5, 1, -1),
        (0.688, 0.140, 10.5, 1, -1),
        (0.988, 0.660, 7.0, -1, 1),
    ):
        cx, cy = U(cu), V(cv)
        arc = [
            (cx + qx * r * math.cos(a), cy + qy * r * math.sin(a))
            for a in np.linspace(0, math.pi / 2, 30)
        ]
        out += _emit([arc], BLACK, f=2200)
        out += _emit([[(arc[0][0], arc[0][1]), (arc[0][0] + qx * 5.0, arc[0][1])]], BLACK, f=2200)
        out += _emit([[(arc[-1][0], arc[-1][1]), (arc[-1][0], arc[-1][1] + qy * 5.0)]],
                     BLACK, f=2200)

    # plus marks
    for cu, cv in ((0.222, 0.252), (0.150, 0.452), (0.772, 0.690), (0.372, 0.335)):
        out += plus_mark(U(cu), V(cv), 3.0, pen=BLACK, f=2200)

    # small open squares + one filled square
    out += _emit([_rect(U(0.878), V(0.706), U(0.878) + 7.0, V(0.706) + 7.0)], BLACK, f=2000)
    out += _emit([_rect(U(0.952), V(0.520), U(0.952) + 3.0, V(0.520) + 3.0)], BLACK, f=2000)
    out += _disc(U(0.9535) + 1.5, V(0.520) + 1.5, 1.4, BLACK)

    # short vertical rules
    for cu, cv, L in ((0.418, 0.512, 10.0), (0.598, 0.516, 8.0), (0.540, 0.690, 7.0)):
        out += _emit([[(U(cu), V(cv)), (U(cu), V(cv) - L)]], BLACK, f=2200)

    # floating dots — kept out of the tile slab and the lower zones
    # the gutter is a zone too: keeping it EMPTY is what makes it read as a
    # gutter rather than as more background.
    forbid = [
        (kb[0] - 3, kb[1] - 3, kb[2] + 3, kb[3] + 3),
        (fm[0] - 3, fm[1] - 3, fm[2] + 3, fm[3] + 3),
        (cone_x - CONE_HALF - 3, V(BASE_V) - 3, cone_x + CONE_HALF + 3, lower_top + 3),
        (fr.x0 - 1, V(GUTTER_V[1]), fr.x1 + 1, V(GUTTER_V[0])),
        (fr.x0 - 1, V(CAP_BASE_V) - 2, fr.x1 + 1, V(CAP_BASE_V) + 4),
    ]
    # dart-throwing with a minimum separation: three dots landing in a clump
    # is the random generator's accident, not a constellation.
    done: List[Pt] = []
    tries = 0
    while len(done) < 34 and tries < 2500:
        tries += 1
        px = rng.uniform(fr.x0, fr.x1)
        py = rng.uniform(fr.y0, fr.y1)
        if slab.contains(px, py):
            continue
        if any(a <= px <= c and b <= py <= d for a, b, c, d in forbid):
            continue
        if any(math.hypot(px - qx, py - qy) < 9.0 for qx, qy in done):
            continue
        out += _disc(px, py, rng.choice([0.4, 0.55, 0.8, 1.1, 1.4]), BLACK)
        done.append((px, py))
    return out
