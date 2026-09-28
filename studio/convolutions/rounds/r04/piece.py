"""CONVOLUTIONS — r04 · iterate · parent r03.

ORDER: ONE LATTICE, ONE WAVEFRONT.  A single sampled field X; a staircase
frontier crossing it diagonally; behind the frontier the field has been READ and
WRITTEN, ahead of it the field is still continuous.  There is no second panel:
every output is drawn on the X lattice node where its window was centred.

What each mark carries (all computed; nothing decorative):

* X — a trefoil "thumbprint": the distance-to-outline field d (|grad d| = 1).
  Unswept side: the level sets of d at a constant 1.05 mm pitch, so ring index
  = d / pitch (the rings ARE the value, by construction).  Swept side: the same
  field sampled on a CELL mm lattice, dot AREA = cell-average of d.
* K — a 5 x 5 zero-sum Laplacian-of-Gaussian (sigma = 1 cell).  Drawn once, as
  the head: a plane lying on the field on the frontier, with a 1.5 mm drop
  shadow.  Each tap is a Ben-Day WASHER around the input sample it multiplies,
  washer AREA = |w| (crimson +, blue -), so every input under the head stays
  visible.
* Y = K * X, valid, stride 2 — an 11 x 11 output whose nodes are the window
  centres, i.e. every other X node.  The wavefront order is i + j <= T (outputs
  are independent, so any order is valid).  Every swept node carries its real
  response as rings CENTRED on its own input sample: ring count = |y| bin
  (rint(4|y|/max|y|)), pen = sign; no ring = y bins to 0.
* The twist: a symmetric zero-sum kernel annihilates every linear ramp, and a
  distance field is a ramp almost everywhere, so K * X is the trefoil's
  SKELETON: a blue letter Y grows inside the thumbprint behind the wavefront.

Pens (colors=3): 0 black (field, samples, head, key, title) · 1 crimson
(positive response / positive taps) · 2 dodgerblue (negative).

Entry point: ``convolutions_wavefront``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Polygon, Rect, Region, clip
from promptplot.generative.engine.kit import circle, giant_type
from promptplot.generative.generators import _chain_segments, _poly, _stroke_text
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, RED, BLUE = 0, 1, 2

F_DRAW = 2200
FRAME_INSET = 3.0  # mm inside the drawable area (same frame as r01 / r03)

# --- the lattice and the operator ------------------------------------------
CELL = 7.2  # mm — one input pixel (r03: 6.5; enlarged so rings fit between samples)
NX, NY = 25, 25  # input lattice -> 180 x 180 mm; output (25-5)/2+1 = 11 x 11
KSIZE = 5
STRIDE = 2
LOG_SIGMA = 1.0  # cells
BLOB_INSET = 1.35  # cells between the lattice edge and the trefoil's bbox

T_FRONT = 10  # swept output nodes: i + j <= T_FRONT (j counted from the bottom)
HEAD = (5, 6)  # the node the kernel sits on now (i + j = T_FRONT + 1): the fork of Y

N_RINGS = 4  # ring count for max |y|
X_RING_PITCH = 1.05  # thumbprint ring pitch (perpendicular, exact: |grad d| = 1)
HAIRPIN_W = 2.0  # closed level loops thinner than this are dropped (no slits)

DOT_RMAX = 1.13  # sample dot radius at max x  (area = x)
DOT_RMIN = 0.30  # plotting floor for a sample dot
GAP = 0.85  # clearance between any two unrelated marks (pen floor 0.8)
RESP_R1 = DOT_RMAX + GAP  # first response ring clears the largest centre sample
RESP_PITCH = 1.02
SHADOW = 1.5  # head drop shadow, mm
WASHER_FILL = 0.28  # concentric fill pitch inside a washer (solid ink band)
FRONT_LINE = True  # draw the read boundary as a keyline across X
COLLAR = 0.45  # paper between a sample dot and the tap collar around it


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



# ===========================================================================
# stroke helpers
# ===========================================================================
def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _plen(poly: Poly) -> float:
    return sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(poly, poly[1:]))


def _ring_area(ring: Poly) -> float:
    return 0.5 * abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1])))


def _offset_out(ring: Poly, d: float) -> Poly:
    """Vertex-normal offset of a smooth closed ring (outward for d > 0)."""
    if d == 0.0:
        return list(ring)
    area = 0.5 * sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))
    sgn = 1.0 if area > 0 else -1.0
    n = len(ring)
    out: Poly = []
    for k in range(n):
        a, b = ring[k - 1], ring[(k + 1) % n]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        out.append((ring[k][0] + sgn * d * ty / L, ring[k][1] - sgn * d * tx / L))
    return out


def _disc(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid dot as a tight spiral + rim — small enough that a spiral cannot flood."""
    turns = max(2, int(r / 0.20))
    n = turns * 22
    pts = [
        (
            x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            y + r * (k / n) * math.sin(2 * math.pi * turns * k / n),
        )
        for k in range(n + 1)
    ]
    return _poly(pts, color=pen, f=1600) + circle(x, y, r, pen=pen, f=1600, n=max(14, int(26 * r)))


def _washer(x: float, y: float, r_in: float, r_out: float, pen: int) -> List[GCodeCommand]:
    """Solid annulus between r_in and r_out: concentric passes at WASHER_FILL.

    A band thinner than one fill pitch is a single circle on its mid-radius.
    """
    out: List[GCodeCommand] = []
    band = r_out - r_in
    if band < WASHER_FILL:
        return circle(x, y, 0.5 * (r_in + r_out), pen=pen, f=1800, n=36)
    n = int(math.ceil(band / WASHER_FILL))
    for k in range(n + 1):
        r = r_in + band * k / n
        out += circle(x, y, r, pen=pen, f=1800, n=max(28, int(18 * r)))
    return out


# ===========================================================================
# rectilinear regions on the lattice
# ===========================================================================
def _mask_ring(mask: np.ndarray) -> Poly:
    """Boundary of a simply-connected cell mask (mask[j, i]) as a CCW vertex ring
    in CELL coordinates, collinear vertices merged."""
    edges: Dict[Tuple[int, int], Tuple[int, int]] = {}
    und = set()
    H, W = mask.shape
    for j in range(H):
        for i in range(W):
            if not mask[j, i]:
                continue
            for a, b in (((i, j), (i + 1, j)), ((i + 1, j), (i + 1, j + 1)),
                         ((i + 1, j + 1), (i, j + 1)), ((i, j + 1), (i, j))):
                if (b, a) in und:
                    und.discard((b, a))
                else:
                    und.add((a, b))
    for a, b in und:
        edges[a] = b
    start = min(edges)
    ring = [start]
    cur = edges[start]
    while cur != start:
        ring.append(cur)
        cur = edges[cur]
    # merge collinear
    clean: Poly = []
    n = len(ring)
    for k in range(n):
        p, q, r = ring[k - 1], ring[k], ring[(k + 1) % n]
        if (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0]) != 0:
            clean.append((float(q[0]), float(q[1])))
    return clean


def _grow_rectilinear(ring: Poly, h: float) -> Poly:
    """Mitred outward offset of a CCW rectilinear ring (exact for h < half the
    shortest edge)."""
    n = len(ring)
    out: Poly = []
    for k in range(n):
        p, q, r = ring[k - 1], ring[k], ring[(k + 1) % n]
        d1 = (q[0] - p[0], q[1] - p[1])
        d2 = (r[0] - q[0], r[1] - q[1])
        l1 = math.hypot(*d1)
        l2 = math.hypot(*d2)
        n1 = (d1[1] / l1, -d1[0] / l1)  # outward normal of a CCW edge
        n2 = (d2[1] / l2, -d2[0] / l2)
        out.append((q[0] + h * (n1[0] + n2[0]), q[1] + h * (n1[1] + n2[1])))
    return out


def _bridge(pieces: List[Poly], gap: float) -> List[Poly]:
    """Re-join consecutive clip pieces whose cut-out gap is shorter than ``gap``.

    A ring that only grazes the corner of a cut region comes back as two pieces
    whose ends almost touch (measured 0.13 mm at a stair corner): a hook, not a
    cut.  Such a ring is kept whole instead.
    """
    out: List[Poly] = []
    for pc in pieces:
        if out and math.hypot(out[-1][-1][0] - pc[0][0], out[-1][-1][1] - pc[0][1]) < gap:
            out[-1] = out[-1] + pc
        else:
            out.append(list(pc))
    return out


def _rect(x0: float, y0: float, x1: float, y1: float) -> Poly:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


# ===========================================================================
# the computation — everything the sheet shows is read off this dict
# ===========================================================================
def log_kernel(size: int = KSIZE, sigma: float = LOG_SIGMA) -> np.ndarray:
    """Discrete Laplacian of Gaussian, made exactly zero-sum.

    Zero-sum + point symmetry means sum(K * (a + b.x)) = 0 for ANY linear ramp,
    which is why the windows over the thumbprint's straight slopes come back
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
            Yr[j, i] = float(
                (K * P[j * STRIDE: j * STRIDE + KSIZE, i * STRIDE: i * STRIDE + KSIZE]).sum()
            )
    ymax = float(np.abs(Yr).max())
    count = np.rint(N_RINGS * np.abs(Yr) / ymax).astype(int)

    # the wavefront: swept output nodes and the cells their windows read
    swept = [(i, j) for j in range(oy) for i in range(ox) if i + j <= T_FRONT]
    read = np.zeros((NY, NX), bool)
    for (i, j) in swept:
        read[j * STRIDE: j * STRIDE + KSIZE, i * STRIDE: i * STRIDE + KSIZE] = True
    ring_cells = _mask_ring(read)

    def to_mm(p: Pt) -> Pt:
        return (lat[0] + p[0] * CELL, lat[1] + p[1] * CELL)

    def cell_centre(ci: int, cj: int) -> Pt:
        return (lat[0] + (ci + 0.5) * CELL, lat[1] + (cj + 0.5) * CELL)

    def node_centre(i: int, j: int) -> Pt:
        return cell_centre(i * STRIDE + KSIZE // 2, j * STRIDE + KSIZE // 2)

    def window(i: int, j: int) -> Bounds:
        wx0 = lat[0] + i * STRIDE * CELL
        wy0 = lat[1] + j * STRIDE * CELL
        return (wx0, wy0, wx0 + KSIZE * CELL, wy0 + KSIZE * CELL)

    return dict(
        lat=lat, box=box, outline=outline, P=P, K=K, Y=Yr, ymax=ymax, count=count,
        ox=ox, oy=oy, swept=swept, read=read, front=[to_mm(p) for p in ring_cells],
        window=window, node_centre=node_centre, cell_centre=cell_centre,
        frame=(fx0, fy0, fx1, fy1),
    )


# ===========================================================================
# drawing pieces
# ===========================================================================
def _thumbprint(outline: Poly, box: Bounds, pitch: float) -> List[Poly]:
    """Level sets of the distance-to-outline field at a constant pitch.

    No wobble: |grad d| = 1 makes the perpendicular gap exactly ``pitch``
    everywhere, including the 45-degree stretches.  Closed loops whose mean
    width (2 * area / perimeter) is under HAIRPIN_W are dropped — those are the
    thin slits a flat medial ridge produces, and they are what inked as seams.
    """
    x0, y0, x1, y1 = box
    pad = 2.0
    xs, ys, X, Y = _grid((x0 - pad, y0 - pad, x1 + pad, y1 + pad), 0.30)
    D = _dist_field(outline, X, Y)
    chains: List[Poly] = []
    k = 1
    dmax = float(D.max())
    while k * pitch < dmax:
        for c in _iso_chains(D, xs, ys, k * pitch):
            L = _plen(c)
            if L < 3.0:
                continue
            closed = math.hypot(c[0][0] - c[-1][0], c[0][1] - c[-1][1]) < 1e-6
            if closed and 2.0 * _ring_area(c) / L < HAIRPIN_W:
                continue
            chains.append(c)
        k += 1
    return chains


def _rings(cx: float, cy: float, n: int, pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for k in range(n):
        r = RESP_R1 + k * RESP_PITCH
        out += circle(cx, cy, r, pen=pen, f=F_DRAW, n=max(40, int(14 * r)))
    return out


def _rings_polys(cx: float, cy: float, n: int) -> List[Poly]:
    polys = []
    for k in range(n):
        r = RESP_R1 + k * RESP_PITCH
        m = max(40, int(14 * r))
        polys.append([(cx + r * math.cos(2 * math.pi * t / m), cy + r * math.sin(2 * math.pi * t / m))
                      for t in range(m + 1)])
    return polys


def sample_radius(v: float) -> float:
    """Dot AREA = x (normalised): r = RMAX * sqrt(v), floored for the pen."""
    return max(DOT_RMIN, DOT_RMAX * math.sqrt(max(v, 0.0)))


def washer_scale(K: np.ndarray, P: np.ndarray, hi: int, hj: int, pmax: float) -> float:
    """Ben-Day washers: each tap is a collar around the sample it multiplies,
    collar AREA = a0 * |w|.  a0 is set so the largest collar fills its cell
    minus a pen gap; every other collar follows from the exact area ratio, so
    crimson area = blue area on the paper (the kernel is zero-sum)."""
    r_c = CELL / 2.0 - GAP / 2.0
    best = None
    for a in range(KSIZE):
        for b in range(KSIZE):
            r_in = sample_radius(float(P[hj * STRIDE + b, hi * STRIDE + a]) / pmax) + COLLAR
            cand = math.pi * (r_c * r_c - r_in * r_in) / max(abs(float(K[b, a])), 1e-12)
            best = cand if best is None else min(best, cand)
    return float(best)


# ===========================================================================
# the plate
# ===========================================================================
def convolutions_wavefront(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    M = build_model(bounds)
    box, outline = M["box"], M["outline"]
    P, K, Yr, count = M["P"], M["K"], M["Y"], M["count"]
    node_centre, cell_centre, window = M["node_centre"], M["cell_centre"], M["window"]
    fx0, fy0, fx1, fy1 = M["frame"]
    out: List[GCodeCommand] = []

    front = M["front"]
    front_cut = Polygon(_grow_rectilinear(front, GAP))

    hi, hj = HEAD
    hx0, hy0, hx1, hy1 = window(hi, hj)
    # the head + its 1.5 mm shadow, grown by the pen gap: rings stop here
    plane_cut = Rect(hx0 - GAP, hy0 - SHADOW - GAP, hx1 + SHADOW + GAP, hy1 + GAP)
    cut: Region = front_cut | plane_cut

    # ---------------- 1. the thumbprint X, ahead of the wavefront ------------
    rings: List[Poly] = []
    for ch in _thumbprint(outline, box, X_RING_PITCH):
        for piece in _bridge(clip(ch, cut, keep="outside"), 1.2):
            if _plen(piece) >= 3.0:  # no crumbs at the cut
                rings.append(piece)
    out += _emit(rings, BLACK)
    # the boundary is the heaviest line on X: a second pass offset OUTWARD
    for off in (0.0, 0.28):
        ol = _offset_out(outline, off)
        out += _emit([p for p in clip(ol + [ol[0]], cut, keep="outside") if _plen(p) >= 1.5], BLACK)

    # the wavefront itself: the read boundary, drawn only where it crosses X
    if FRONT_LINE:
        fr = list(front) + [front[0]]
        blob = Polygon(_offset_out(outline, 0.9))
        wave = [q for q in clip(fr, blob, keep="inside") if _plen(q) >= 2.0]
        wave = [q for pc in wave for q in clip(pc, plane_cut, keep="outside") if _plen(q) >= 2.0]
        out += _emit(wave, BLACK, f=1800)

    # ---------------- 2. behind the wavefront: every sample X ---------------
    pmax = float(P.max())
    read = M["read"].copy()
    head_cells = set()
    for a in range(KSIZE):
        for b in range(KSIZE):
            head_cells.add((hi * STRIDE + a, hj * STRIDE + b))
    # dot AREA = x, so a sample with x = 0 has zero area: it is paper, and the
    # key says so ("no dot: x = 0"), exactly as "no ring: y = 0".  Every other
    # sample behind the frontier, and all 25 under the head, is drawn.
    for cj in range(NY):
        for ci in range(NX):
            if not (read[cj, ci] or (ci, cj) in head_cells):
                continue
            if P[cj, ci] <= 1e-9:
                continue
            px, py = cell_centre(ci, cj)
            out += _disc(px, py, sample_radius(float(P[cj, ci]) / pmax), BLACK)

    # ---------------- 3. the head: K as a plane lying on the field ----------
    for dx in (0.0, 0.30):
        out += _emit([_rect(hx0 - dx, hy0 - dx, hx1 + dx, hy1 + dx)], BLACK, f=1800)
    out += _emit([[(hx0 + SHADOW, hy0), (hx0 + SHADOW, hy0 - SHADOW), (hx1 + SHADOW, hy0 - SHADOW),
                   (hx1 + SHADOW, hy1 - SHADOW), (hx1, hy1 - SHADOW)]], BLACK, f=1800)

    # ---------------- 4. Y = K * X, written on X's own nodes -----------------
    for (i, j) in M["swept"]:
        n = int(count[j, i])
        if n == 0:
            continue
        cx, cy = node_centre(i, j)
        pen = RED if Yr[j, i] > 0 else BLUE
        polys = _rings_polys(cx, cy, n)
        kept: List[Poly] = []
        for pl in polys:
            kept += [p for p in clip(pl, plane_cut, keep="outside") if _plen(p) >= 1.0]
        out += _emit(kept, pen)

    # the kernel's taps: washers around the samples they multiply
    a0 = washer_scale(K, P, hi, hj, pmax)
    for a in range(KSIZE):
        for b in range(KSIZE):
            w = float(K[b, a])
            ci, cj = hi * STRIDE + a, hj * STRIDE + b
            px, py = cell_centre(ci, cj)
            r_in = sample_radius(float(P[cj, ci]) / pmax) + COLLAR
            r_out = math.sqrt(r_in * r_in + a0 * abs(w) / math.pi)
            out += _washer(px, py, r_in, r_out, RED if w > 0 else BLUE)

    # ---------------- 5. key + title (the quiet right column) ---------------
    out += _key_and_title(M, fx1)
    return out


def _title(text: str, x: float, y: float, h: float, weight: float) -> Tuple[List[GCodeCommand], float]:
    """Display title set glyph by glyph on its INK box: each glyph is shifted by
    its own left ink edge and advanced by ink width + one bearing, so a serifed
    'I' sits centred between its neighbours (r03 read "CONVOLUT IONS")."""
    from promptplot.generative.generators import _GLYPHS

    sc = h / 6.0
    bearing = 1.25
    cmds: List[GCodeCommand] = []
    cx = x
    for ch in text:
        st = _GLYPHS[ch]
        xs = [pt[0] for stroke in st for pt in stroke]
        x0g, x1g = min(xs), max(xs)
        cmds += giant_type(ch, cx - x0g * sc, y, h, pen=BLACK, weight=weight, tip=0.25)
        cx += (x1g - x0g + bearing) * sc
    return cmds, cx - x - bearing * sc


def _title_width(text: str, h: float) -> float:
    from promptplot.generative.generators import _GLYPHS

    sc = h / 6.0
    w = 0.0
    for ch in text:
        xs = [pt[0] for stroke in _GLYPHS[ch] for pt in stroke]
        w += (max(xs) - min(xs) + 1.25) * sc
    return w - 1.25 * sc


def _key_and_title(M: Dict, fx1: float) -> List[GCodeCommand]:
    lat = M["lat"]
    out: List[GCodeCommand] = []
    # every ink edge of the column keeps 10 mm to the drawable edge (fx1 is the
    # 3 mm frame, so 7 mm more); the column starts ~14 mm right of X's ink
    kx0 = lat[2] + 6.0
    width = (fx1 - 7.0) - kx0
    top_c = lat[1] + (NY - 1.5) * CELL  # the highest sample row that carries ink
    bot_c = lat[1] + 1.5 * CELL  # the lowest sample row that carries ink

    # title: display weight, set to the column width, baseline on the bottom row
    title = "CONVOLUTIONS"
    th = width / _title_width(title, 1.0)
    cmds, _ = _title(title, kx0, bot_c, th, 0.8)
    out += cmds

    # the key: one strip, top-aligned to the top sample row
    TH = 2.2  # cap height
    lx = kx0 + 14.0  # text column
    ix = kx0 + 5.5  # icon centre
    pitch = 12.0
    rows_y = [top_c - k * pitch for k in range(5)]

    def text(s: str, x: float, y: float) -> List[GCodeCommand]:
        return _stroke_text(s, x, y, TH, color=BLACK, f=2000)

    def row(y: float, a: str, b: str) -> List[GCodeCommand]:
        return text(a, lx, y + 0.6) + text(b, lx, y - 0.6 - TH - 1.6)

    # 1. X
    y = rows_y[0]
    for k, v in enumerate((0.15, 0.5, 1.0)):
        out += _disc(ix - 3.6 + 3.6 * k, y, sample_radius(v), BLACK)
    out += row(y, "X   dot area = x", "no dot: x = 0")
    # 2. K
    y = rows_y[1]
    out += _disc(ix, y, DOT_RMAX, BLACK)
    out += _washer(ix, y, DOT_RMAX + COLLAR, CELL / 2.0 - GAP / 2.0, BLUE)
    out += row(y, "K   5\u00d75 LoG, stride 2", "collar area = |w|")
    # 3. Y
    y = rows_y[2]
    out += _disc(ix, y, 0.6, BLACK)
    out += _rings(ix, y, 3, RED)
    out += row(y, "Y = K \u2217 X", "rings = round(4|y| / max|y|)")
    # 4. sign
    y = rows_y[3]
    out += _disc(ix - 2.6, y, 0.45, BLACK)
    out += _rings(ix - 2.6, y, 1, RED)
    out += _disc(ix + 2.6, y, 0.45, BLACK)
    out += _rings(ix + 2.6, y, 1, BLUE)
    out += row(y, "crimson +   blue \u2212", "no ring: y = 0")
    return out
