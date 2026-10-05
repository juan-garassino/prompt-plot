"""CONVOLUTIONS — r03 · sliding-window (abstract) · parent r01.

ORDER: a LATTICE WITH A TRAVELLING WINDOW.  Nothing is depicted and nothing is
boxed except the one thing a convolution is: a k x k window that steps across a
sampled field at stride s and leaves one number behind each time it stops.

What is on the sheet, and what each mark carries (all computed, nothing
decorative):

* X — one large field in the left 60 %: a trefoil outline filled with the
  level sets of its own distance field d(p) (|grad d| = 1, so the ring pitch is
  exactly the level step).  X is SAMPLED on a lattice of CELL mm cells; the
  pixel value is the exact cell-average of d (6 x 6 quadrature per cell).
* K — a 5 x 5 zero-sum Laplacian-of-Gaussian (sigma = 1 cell), drawn once, at
  the head of the sweep, as signed Ben-Day discs: disc AREA = |w|, crimson =
  positive tap, blue = negative tap.
* The sweep — the window stamped along ONE diagonal of the output lattice at
  stride 2.  Consecutive stamps overlap by exactly k - s = 3 cells, and the
  corridor the window has already read is cut out of the thumbprint: inside it
  the continuous rings are replaced by the lattice samples they became (dot
  area = pixel value).  The staircase edge of the corridor steps once per
  stamp, so the stride is a visible spacing (2 cells = 13 mm) and the corridor
  width is the kernel (5 cells).
* Each finished stamp leaves its response y = sum(K * patch) as a nested ring
  set at the stamp centre: ring COUNT = round(4 |y| / max|y|), pen = sign.
  A zero-sum symmetric kernel annihilates any linear ramp exactly, and d is a
  ramp almost everywhere, so most stamps come back SILENT; they fire only where
  d bends — crimson on the outline (convex kink), blue on the medial ridge.
* Y — the complete output map K * X (valid, stride 2) on the right, drawn with
  the same count/sign mapping at a smaller ring pitch.  Because the kernel only
  sees curvature, the map it returns is the trefoil's SKELETON: a blue Y inside
  a crimson outline.  The thumbprint X, convolved, is the letter Y.

Pens (colors=3): 0 black (field, lattice, window, title) · 1 crimson (positive
response / positive taps) · 2 blue (negative response / negative taps).

Entry point: ``convolutions_sliding_window``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Polygon, Region, clip
from promptplot.generative.engine.kit import circle, giant_type, giant_type_width
from promptplot.generative.engine.policies import enforce_line_spacing
from promptplot.generative.generators import (
    _chain_segments,
    _poly,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, RED, BLUE = 0, 1, 2

F_DRAW = 2200
MIN_PITCH = 0.85  # mm — plotting floor; no ring family may go under this
FRAME_INSET = 3.0  # mm inside the drawable area (same frame as r01)

# --- the lattice and the operator ------------------------------------------
CELL = 6.5  # mm — one input pixel
NX, NY = 25, 28  # input lattice (cells) -> 162.5 x 182 mm, the left 60 %
KSIZE = 5
STRIDE = 2
LOG_SIGMA = 1.0  # cells
BLOB_INSET = 1.35  # cells between the lattice edge and the trefoil's bbox

# the sweep: output-lattice nodes (col, row-from-top) visited, one per stamp
PATH_START = (0, 1)  # the main diagonal: enters at the left frame edge
PATH_LEN = 11  # stamps on the diagonal, to the far corner of the lattice
HEAD = 7  # index of the stamp the window is sitting on now

N_RINGS = 4  # ring count for max |y|
X_RING_PITCH = 1.0  # thumbprint ring pitch
STAMP_PITCH = 1.9  # response rings on the sheet-scale stamps
Y_PITCH_NODE = 8.5  # output lattice pitch (mm)
Y_RING_PITCH = 0.9  # response rings in the output map


# ===========================================================================
# helpers carried over from r01 (contouring, distance fields, strokes)
# ===========================================================================
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
# the computation — everything the sheet shows is read off this dict
# ===========================================================================
def log_kernel(size: int = KSIZE, sigma: float = LOG_SIGMA) -> np.ndarray:
    """Discrete Laplacian of Gaussian, made exactly zero-sum.

    Zero-sum + point symmetry means sum(K * (a + b.x)) = 0 for ANY linear ramp,
    which is why the stamps over the thumbprint's straight slopes come back
    silent and the response concentrates on the outline and the medial ridge.
    """
    h = size // 2
    ii = np.arange(size) - h
    I, J = np.meshgrid(ii, ii)
    R2 = (I * I + J * J) / (2.0 * sigma * sigma)
    K = -(1.0 - R2) * np.exp(-R2)
    return K - K.mean()


def build_model(bounds: Bounds) -> Dict:
    x0, y0, x1, y1 = bounds
    fx0, fy0 = x0 + FRAME_INSET, y0 + FRAME_INSET
    fx1, fy1 = x1 - FRAME_INSET, y1 - FRAME_INSET
    lat_x0 = fx0
    lat_y0 = fy0 + ((fy1 - fy0) - NY * CELL) / 2.0
    lat = (lat_x0, lat_y0, lat_x0 + NX * CELL, lat_y0 + NY * CELL)

    ins = BLOB_INSET * CELL
    box = (lat[0] + ins, lat[1] + ins, lat[2] - ins, lat[3] - ins)
    # phi_3 = -pi/2 puts the three lobes at 30 / 150 / 270 deg: two arms up,
    # one stem down, so the medial axis is an upright Y.
    outline = _fit_poly(
        _amoeba([(3, 0.46, -math.pi / 2), (2, 0.06, 0.55), (1, 0.05, -0.60), (5, 0.035, 2.2)]),
        box,
    )

    # exact cell averages of d  (6 x 6 midpoint quadrature per cell)
    sub = 6
    xs = lat[0] + (np.arange(NX * sub) + 0.5) * CELL / sub
    ys = lat[1] + (np.arange(NY * sub) + 0.5) * CELL / sub
    Xg, Yg = np.meshgrid(xs, ys)
    D = _dist_field(outline, Xg, Yg)
    P = D.reshape(NY, sub, NX, sub).mean(axis=(1, 3))  # P[j, i], j = row from BOTTOM

    K = log_kernel()
    oy = (NY - KSIZE) // STRIDE + 1
    ox = (NX - KSIZE) // STRIDE + 1
    Yr = np.zeros((oy, ox))
    for j in range(oy):
        for i in range(ox):
            Yr[j, i] = float((K * P[j * STRIDE : j * STRIDE + KSIZE, i * STRIDE : i * STRIDE + KSIZE]).sum())
    ymax = float(np.abs(Yr).max())
    count = np.rint(N_RINGS * np.abs(Yr) / ymax).astype(int)

    def cell_centre(ci: int, cj: int) -> Pt:
        return (lat[0] + (ci + 0.5) * CELL, lat[1] + (cj + 0.5) * CELL)

    # the sweep, as output nodes (i, j) with j from the BOTTOM
    path = []
    ci0, rt0 = PATH_START
    for t in range(PATH_LEN):
        i = ci0 + t
        j = (oy - 1) - (rt0 + t)
        path.append((i, j))

    def window(i: int, j: int) -> Bounds:
        wx0 = lat[0] + i * STRIDE * CELL
        wy0 = lat[1] + j * STRIDE * CELL
        return (wx0, wy0, wx0 + KSIZE * CELL, wy0 + KSIZE * CELL)

    def stamp_centre(i: int, j: int) -> Pt:
        return cell_centre(i * STRIDE + KSIZE // 2, j * STRIDE + KSIZE // 2)

    return dict(
        lat=lat, box=box, outline=outline, P=P, K=K, Y=Yr, ymax=ymax, count=count,
        ox=ox, oy=oy, path=path, window=window, stamp_centre=stamp_centre,
        cell_centre=cell_centre, frame=(fx0, fy0, fx1, fy1),
    )


# ===========================================================================
# drawing pieces
# ===========================================================================
def _staircase(wins: Sequence[Bounds]) -> Poly:
    """Outline of the union of equal squares stepped down-right by a constant
    offset (s < k): one tread per stamp on each side, so the stride reads."""
    top: Poly = []
    bot: Poly = []
    for n, (a0, b0, a1, b1) in enumerate(wins):
        if n == 0:
            top.append((a0, b1))
        top += [(a1, b1)] if n == 0 else [(wins[n - 1][2], b1), (a1, b1)]
    # right edge of the last square, then the bottom staircase back
    last = wins[-1]
    top.append((last[2], last[1]))
    for n in range(len(wins) - 1, -1, -1):
        a0, b0, a1, b1 = wins[n]
        bot.append((a0, b0) if n == len(wins) - 1 else (wins[n + 1][0], b0))
        bot.append((a0, b0))
    bot.append((wins[0][0], wins[0][3]))
    ring = top + bot
    # drop consecutive duplicates
    clean: Poly = []
    for p in ring:
        if not clean or abs(clean[-1][0] - p[0]) > 1e-9 or abs(clean[-1][1] - p[1]) > 1e-9:
            clean.append(p)
    return clean


def _thumbprint(rng: SeededRNG, outline: Poly, box: Bounds, pitch: float) -> List[Poly]:
    """Level sets of the distance-to-outline field at a constant pitch."""
    x0, y0, x1, y1 = box
    pad = 2.0
    xs, ys, X, Y = _grid((x0 - pad, y0 - pad, x1 + pad, y1 + pad), 0.42)
    D = _dist_field(outline, X, Y)
    wob = (_fbm_grid(rng, X, Y, 1.0 / 15.0, 3) - 0.5) * 2.0 * (0.12 * pitch)
    F = np.where(D > 0, D + wob, 0.0)
    chains: List[Poly] = []
    k = 1
    dmax = float(F.max())
    while k * pitch < dmax:
        chains += [c for c in _iso_chains(F, xs, ys, k * pitch) if _plen(c) >= 3.0]
        k += 1
    return chains


def _plen(poly: Poly) -> float:
    return sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(poly, poly[1:]))


def _offset_out(ring: Poly, d: float) -> Poly:
    if d == 0.0:
        return list(ring)
    area = 0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))
    sgn = 1.0 if area > 0 else -1.0  # CCW -> outward normal is (dy, -dx)
    n = len(ring)
    out: Poly = []
    for k in range(n):
        a, b = ring[k - 1], ring[(k + 1) % n]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        out.append((ring[k][0] + sgn * d * ty / L, ring[k][1] - sgn * d * tx / L))
    return out


def _rings(
    cx: float, cy: float, n: int, pitch: float, pen: int, seg: int = 64, r0: Optional[float] = None
) -> List[GCodeCommand]:
    """n concentric rings: the first at ``r0`` (default one pitch), then one pitch apart."""
    out: List[GCodeCommand] = []
    first = pitch if r0 is None else r0
    for k in range(n):
        r = first + k * pitch
        out += circle(cx, cy, r, pen=pen, f=F_DRAW, n=max(24, int(seg * (k + 1) / n)))
    return out


def _lane(p: Pt, q: Pt, hw: float) -> Polygon:
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * hw, dx / L * hw
    return Polygon([(p[0] + nx, p[1] + ny), (q[0] + nx, q[1] + ny), (q[0] - nx, q[1] - ny), (p[0] - nx, p[1] - ny)])


def _dotted(
    p: Pt, q: Pt, gap: float = 1.7, pen: int = BLACK, skip: Sequence[Tuple[float, float, float]] = ()
) -> List[GCodeCommand]:
    """Dotted projection line; dots inside any ``skip`` disc (x, y, r) are left out."""
    L = math.hypot(q[0] - p[0], q[1] - p[1])
    n = max(1, int(L / gap))
    out: List[GCodeCommand] = []
    for k in range(n + 1):
        t = k / n
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if any(math.hypot(x - sx, y - sy) < sr for sx, sy, sr in skip):
            continue
        out += circle(x, y, 0.22, pen=pen, f=F_DRAW, n=6)
    return out


# ===========================================================================
# the plate
# ===========================================================================
def convolutions_sliding_window(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    M = build_model(bounds)
    box, outline = M["box"], M["outline"]
    P, K, Yr, count = M["P"], M["K"], M["Y"], M["count"]
    path, window, stamp_centre, cell_centre = M["path"], M["window"], M["stamp_centre"], M["cell_centre"]
    fx0, fy0, fx1, fy1 = M["frame"]
    out: List[GCodeCommand] = []

    swept = path[: HEAD + 1]
    wins = [window(i, j) for (i, j) in swept]
    corridor = _staircase(wins)
    corr_region = Polygon(corridor)

    # future track: head centre -> the remaining stamp centres -> lattice edge
    head_c = stamp_centre(*path[HEAD])
    tail_c = stamp_centre(*path[-1])
    step = (STRIDE * CELL, -STRIDE * CELL)
    track_end = (tail_c[0] + step[0] * 0.9, tail_c[1] + step[1] * 0.9)
    head_win = wins[-1]
    track_start = (head_win[2], head_c[1] - (head_win[2] - head_c[0]))  # where the diagonal leaves the head window
    lane = _lane(track_start, track_end, 1.3)

    # ---------------- 1. the thumbprint X (black) ----------------------------
    chains = _thumbprint(rng, outline, box, X_RING_PITCH)
    ring_polys: List[Poly] = []
    # the rings stop a full plotting gap SHORT of the corridor edge, so a ring
    # running tangent to a stair tread can never crowd it
    halo = 0.85
    halo_corr = Polygon(_staircase([(a - halo, b - halo, c + halo, d + halo) for a, b, c, d in wins]))
    cut: Region = halo_corr | lane
    for ch in chains:
        for piece in clip(ch, cut, keep="outside"):
            if _plen(piece) >= 1.2:  # no crumbs at the corridor edge
                ring_polys.append(piece)
    ring_cmds = _emit(ring_polys, BLACK)
    out += _guard_spacing(ring_cmds, 0.80)
    # the boundary is the heaviest line on X: a second pass offset OUTWARD
    # along the normal, so ring 1 keeps its full pitch from both passes
    for off in (0.0, 0.28):
        ol = _offset_out(outline, off)
        out += _emit(clip(ol + [ol[0]], corr_region, keep="outside"), BLACK)

    # ---------------- 2. the corridor: samples + finished stamps ------------
    hx0, hy0, hx1, hy1 = head_win
    # the head's own heavy square carries the corridor edge where they coincide
    head_zone = Polygon(_rect(hx0 - 0.5, hy0 - 0.5, hx1 + 0.5, hy1 + 0.5)[:-1])
    out += _emit(clip(corridor + [corridor[0]], head_zone, keep="outside"), BLACK, f=1800)

    pmax = float(P.max())
    stamp_discs = []  # (cx, cy, R) knock-outs for the pixel samples
    for t, (i, j) in enumerate(swept[:-1]):
        cx, cy = stamp_centre(i, j)
        n = int(count[j, i])
        R = max(n, 1) * STAMP_PITCH
        stamp_discs.append((cx, cy, R + 0.9))
    hx0, hy0, hx1, hy1 = head_win

    for cj in range(NY):
        for ci in range(NX):
            px, py = cell_centre(ci, cj)
            if not corr_region.contains(px, py):
                continue
            if hx0 < px < hx1 and hy0 < py < hy1:
                continue  # under the kernel
            v = float(P[cj, ci]) / pmax
            r = 0.28 + 0.85 * math.sqrt(max(v, 0.0))
            if any(math.hypot(px - sx, py - sy) < sr + r for sx, sy, sr in stamp_discs):
                continue
            if v <= 1e-6:
                out += circle(px, py, 0.3, pen=BLACK, f=F_DRAW, n=8)
            else:
                out += _disc(px, py, r, BLACK)

    for t, (i, j) in enumerate(swept[:-1]):
        cx, cy = stamp_centre(i, j)
        n = int(count[j, i])
        y = float(Yr[j, i])
        under_head = hx0 < cx < hx1 and hy0 < cy < hy1
        if n == 0:
            if not under_head:  # under the head it would ring the corner tap
                out += circle(cx, cy, 0.9, pen=BLACK, f=F_DRAW, n=20)  # looked, saw nothing
            continue
        pen = RED if y > 0 else BLUE
        out += _rings(cx, cy, n, STAMP_PITCH, pen)
        out += _disc(cx, cy, 0.45, pen)

    # ---------------- 3. the kernel, sitting on the head stamp ---------------
    for dx in (0.0, 0.35):
        out += _emit([_rect(hx0 - dx, hy0 - dx, hx1 + dx, hy1 + dx)], BLACK, f=1800)
    wabs = float(np.abs(K).max())
    ci0, cj0 = path[HEAD][0] * STRIDE, path[HEAD][1] * STRIDE
    for a in range(KSIZE):
        for b in range(KSIZE):
            w = float(K[b, a])
            px, py = cell_centre(ci0 + a, cj0 + b)
            r = 2.5 * math.sqrt(abs(w) / wabs)
            pen = RED if w > 0 else BLUE
            if r < 0.45:
                out += circle(px, py, 0.45, pen=pen, f=F_DRAW, n=14)
            else:
                out += _disc(px, py, r, pen)

    # ---------------- 4. the track still to run -----------------------------
    future = []
    for (i, j) in path[HEAD + 1 :]:
        cx, cy = stamp_centre(i, j)
        if hx0 < cx < hx1 and hy0 < cy < hy1:
            continue  # the next stop already sits on the kernel's corner tap
        future.append((cx, cy, 1.3 + 0.9))
        out += circle(cx, cy, 1.3, pen=BLACK, f=F_DRAW, n=22)
    out += _dotted(track_start, track_end, 1.8, BLACK, skip=future)

    # ---------------- 5. the output map Y -----------------------------------
    ox, oy = M["ox"], M["oy"]
    yw, yh = ox * Y_PITCH_NODE, oy * Y_PITCH_NODE
    yx1 = fx1
    yx0 = yx1 - yw
    yy0 = fy1 - yh
    for j in range(oy):
        for i in range(ox):
            cx = yx0 + (i + 0.5) * Y_PITCH_NODE
            cy = yy0 + (j + 0.5) * Y_PITCH_NODE
            n = int(count[j, i])
            if n == 0:
                out += circle(cx, cy, 0.3, pen=BLACK, f=F_DRAW, n=8)
                continue
            pen = RED if Yr[j, i] > 0 else BLUE
            # centre mark r 0.25 + first ring at 1.15 -> 0.9 mm clear, and the
            # outermost ring (1.15 + 3 x 0.9 = 3.85) leaves 0.8 mm to the next node
            out += _rings(cx, cy, n, Y_RING_PITCH, pen, seg=40, r0=1.15)
            out += circle(cx, cy, 0.25, pen=pen, f=F_DRAW, n=8)
    # the swept diagonal, marked in the output at output scale
    ywins = []
    for (i, j) in swept[:-1]:
        ywins.append((yx0 + i * Y_PITCH_NODE, yy0 + j * Y_PITCH_NODE,
                      yx0 + (i + 1) * Y_PITCH_NODE, yy0 + (j + 1) * Y_PITCH_NODE))
    out += _emit([_staircase(ywins) + [_staircase(ywins)[0]]], BLACK, f=1800)
    # same grammar as the sweep on X: thin staircase = done, heavy square =
    # the slot the head is writing now, dotted diagonal = still to come
    hi, hj = path[HEAD]
    hq = (yx0 + hi * Y_PITCH_NODE, yy0 + hj * Y_PITCH_NODE,
          yx0 + (hi + 1) * Y_PITCH_NODE, yy0 + (hj + 1) * Y_PITCH_NODE)
    for dx in (0.0, 0.35):
        out += _emit([_rect(hq[0] - dx, hq[1] - dx, hq[2] + dx, hq[3] + dx)], BLACK, f=1800)
    ti, tj = path[-1]
    y_tail = (yx0 + (ti + 1.0) * Y_PITCH_NODE, yy0 + tj * Y_PITCH_NODE)
    y_future = []
    for (i, j) in path[HEAD + 1 :]:
        y_future.append((yx0 + (i + 0.5) * Y_PITCH_NODE, yy0 + (j + 0.5) * Y_PITCH_NODE, 1.2))
    out += _dotted((hq[2] + 0.6, hq[1] - 0.6), y_tail, 1.8, BLACK, skip=y_future)

    # ---------------- 6. title ----------------------------------------------
    # the title spans exactly the output map's width: one right column
    th = 7.0 * yw / giant_type_width("CONVOLUTIONS", 7.0)
    out += giant_type("CONVOLUTIONS", yx0, fy0, th, pen=BLACK, weight=0.8, tip=0.4)

    return out
