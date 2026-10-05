"""CONVOLUTIONS — r05 · iterate · parent r04.

ORDER: ONE LATTICE, ONE WAVEFRONT, AND THE FRAME IS THE IMAGE EDGE.  r04's
single sampled field X and its staircase frontier are kept with all their
arithmetic; what changes is what the frame does to X.  The input lattice is
now 37 x 25 samples and fills the sheet's width: its top and right edges ARE
the crop, and X is larger than the image, so the unread rings run out through
the top and the right of the sheet.  No outer contour closes anywhere.

What each mark carries (all computed; nothing decorative):

* X — a Y-shaped field (three smooth-unioned capsules; the third, unread, is a
  funnel leaving the image through its top-right corner): the
  distance-to-outline field d (|grad d| = 1).  Unswept side:
  level sets of d at a constant 1.05 mm pitch (ring index = d / pitch).  Swept
  side: the same field sampled on a CELL mm lattice, dot AREA = cell-average d.
* K — a 5 x 5 zero-sum Laplacian-of-Gaussian (sigma = 1 cell), drawn once as
  the head: a CARD lying on the field, a 4-pass keyline (the heaviest line on
  the sheet) and a 3.2 mm drop shadow hatched at 45 degrees.  Each tap is a Ben-Day collar around the sample it multiplies; the
  collar's INK AREA = a0 |w| (full rings, then one partial ring whose sweep
  carries the remainder), crimson +, blue -.
* Y = K * X, valid, stride 2 — 17 x 11 output nodes (every other X node).  The
  wavefront order is i + j <= 10: the same 66 windows as r04.  Every swept node
  carries its real response as rings centred on its own input sample: ring
  count = rint(4|y| / max|y|) over the read nodes, pen = sign; no ring =
  |y| < max|y| / 8.
* The wavefront: the whole staircase boundary of the 66 read windows, from the
  image's top edge to its bottom edge; its foot is the key's column.
* The finding: a symmetric zero-sum kernel annihilates every linear ramp and a
  distance field is a ramp almost everywhere, so K * X is X's SKELETON (blue,
  where X peaks) and its RIM (crimson, where X starts).

Pens (colors=3), streamed in index order: 0 crimson · 1 dodgerblue · 2 black.

Entry point: ``convolutions_cropfield``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from matplotlib.path import Path as MplPath

from promptplot.generative.engine.geometry import Circle, Polygon, Rect, Region, clip
from promptplot.generative.engine.policies import enforce_line_spacing
from promptplot.generative.generators import _GLYPHS, _chain_segments, _poly, _stroke_text
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

# stream order = index order: colour first, black (keylines, dots, type) last
RED, BLUE, BLACK = 0, 1, 2

F_DRAW = 2200
FRAME_INSET = 3.0  # mm inside the drawable area: the crop line
NIB = 0.30  # mm — the stated pen (0.3 fineliner) every pitch below is checked against

# --- the lattice and the operator ------------------------------------------
CELL = 7.2  # mm — one input pixel (r04)
NX, NY = 37, 25  # input lattice -> 266.4 x 180 mm; output 17 x 11
KSIZE = 5
STRIDE = 2
LOG_SIGMA = 1.0  # cells

T_FRONT = 10  # swept output nodes: i + j <= T_FRONT (j counted from the bottom)
HEAD = (5, 6)  # the node the kernel sits on now (i + j = T_FRONT + 1): the fork of Y

N_RINGS = 4  # ring count for max |y|
X_RING_PITCH = 1.05  # thumbprint ring pitch (perpendicular, exact: |grad d| = 1)
HAIRPIN_W = 2.0  # closed level loops thinner than this are dropped (no slits)

DOT_RMAX = 1.13  # sample dot radius at max x  (area = x)
DOT_RMIN = 0.30  # plotting floor for a sample dot: declared in the key
GAP = 0.85  # clearance between any two unrelated marks (pen floor 0.8)
RESP_R1 = DOT_RMAX + GAP  # first response ring clears the largest centre sample
RESP_PITCH = 1.02

# --- the head card -----------------------------------------------------------
SHADOW = 3.2  # mm: hatched drop-shadow band, right and bottom only
SHADOW_HATCH = 0.9  # mm pitch of the 45-degree shadow hatch
KEY_PASSES = 4  # card keyline passes (outward): the heaviest line on the sheet
KEY_PITCH = 0.25  # < NIB, so the passes fuse into one 1.05 mm solid line
KEY_BAND = (KEY_PASSES - 1) * KEY_PITCH + NIB / 2.0  # outer ink edge beyond the card edge
COLLAR_PAPER = 0.60  # bare paper between a sample dot's ink and its collar's ink
COLLAR_PITCH = 0.32  # >= NIB: collar passes never overdraw

# --- X: three capsules in CELL units (fork on the head node's centre) --------
FORK = (12.5, 14.5)
CAPSULES = (
    (FORK, (12.5, 6.2), 4.7, 4.7),  # stem, read
    (FORK, (5.0, 18.25), 4.1, 4.1),  # left arm, read: its ridge runs through nodes (3,7) and (1,8)
    # right arm, unread: a FUNNEL that leaves the image through its top-right
    # corner.  It opens as it goes (half-angle ~9 deg), so its ridge climbs and
    # the rings cross it as chevrons pointing back at the kernel, never as a
    # flat-crest slit; the whorl's eye lies beyond the corner, so every unread
    # ring runs out through the top or the right and none closes on the sheet.
    (FORK, (30.0, 23.5), 3.6, 6.8),
    ((30.0, 23.5), (42.0, 29.0), 6.8, 7.6),
)
SMOOTH_K = 1.6  # polynomial smooth-min radius (cells)

LAST: Dict = {}  # the last build's named stroke families (for measurement only)


# ===========================================================================
# fields
# ===========================================================================
_MS_TABLE = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),), 5: ((3, 2), (0, 1)),
    6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),), 9: ((0, 2),), 10: ((0, 3), (1, 2)),
    11: ((1, 2),), 12: ((1, 3),), 13: ((0, 1),), 14: ((0, 3),),
}


def _iso_chains(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, iso: float) -> List[Poly]:
    """Iso-contour of F[j, i] (j indexes ys) as chained polylines."""
    v0, v1, v2, v3 = F[:-1, :-1], F[:-1, 1:], F[1:, 1:], F[1:, :-1]
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


def _capsule_sdf(X: np.ndarray, Y: np.ndarray, a: Pt, b: Pt, r: float) -> np.ndarray:
    vx, vy = b[0] - a[0], b[1] - a[1]
    if vx * vx + vy * vy < 1e-12:
        return np.hypot(X - a[0], Y - a[1]) - r
    t = np.clip(((X - a[0]) * vx + (Y - a[1]) * vy) / (vx * vx + vy * vy), 0.0, 1.0)
    return np.hypot(X - a[0] - t * vx, Y - a[1] - t * vy) - r


def _smin(a: np.ndarray, b: np.ndarray, k: float) -> np.ndarray:
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1 - h) + a * h - k * h * (1 - h)


def _outline_cells() -> Poly:
    """The support of X in CELL units: the zero set of a smooth capsule union.

    Only used to define the OUTLINE; the field itself is then the exact
    Euclidean distance to that outline, so |grad d| = 1 and the ring pitch is
    constant.  The domain is larger than the image: the right arm ends ~10
    cells beyond the lattice's right edge, so the polygon closes off-sheet.
    """
    step = 0.08
    xs = np.arange(-6.0, 58.0, step)
    ys = np.arange(-6.0, 38.0, step)
    X, Y = np.meshgrid(xs, ys)
    F = None
    for a, b, r0, r1 in CAPSULES:
        if abs(r1 - r0) < 1e-9:
            s = _capsule_sdf(X, Y, a, b, r0)
        else:  # a round cone as the exact union of discs along the axis
            s = None
            for t in np.linspace(0.0, 1.0, 90):
                c = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
                sd = np.hypot(X - c[0], Y - c[1]) - (r0 + t * (r1 - r0))
                s = sd if s is None else np.minimum(s, sd)
        F = s if F is None else _smin(F, s, SMOOTH_K)
    chains = _iso_chains(-F, xs, ys, 0.0)
    ring = max(chains, key=len)
    if math.hypot(ring[0][0] - ring[-1][0], ring[0][1] - ring[-1][1]) < 1e-6:
        ring = ring[:-1]
    return ring


def _resample_ring(ring: Poly, step: float) -> Poly:
    pts = ring + [ring[0]]
    out: Poly = [pts[0]]
    acc = 0.0
    for p, q in zip(pts, pts[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        acc += L
        if acc >= step:
            out.append(q)
            acc = 0.0
    return out


def _dist_field(poly: Poly, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Exact distance to the outline polygon, positive INSIDE, 0 outside."""
    P = np.asarray(poly, float)
    B = np.roll(P, -1, axis=0)
    keep = ((B - P) ** 2).sum(axis=1) > 1e-12
    A, B = P[keep], B[keep]
    V = B - A
    L2 = (V ** 2).sum(axis=1)
    sx0, sx1 = np.minimum(A[:, 0], B[:, 0]), np.maximum(A[:, 0], B[:, 0])
    sy0, sy1 = np.minimum(A[:, 1], B[:, 1]), np.maximum(A[:, 1], B[:, 1])

    def seg_dist(px: np.ndarray, py: np.ndarray, idx: np.ndarray) -> np.ndarray:
        ax, ay = A[idx, 0][:, None], A[idx, 1][:, None]
        vx, vy = V[idx, 0][:, None], V[idx, 1][:, None]
        t = np.clip(((px[None] - ax) * vx + (py[None] - ay) * vy) / L2[idx][:, None], 0.0, 1.0)
        return np.hypot(px[None] - (ax + t * vx), py[None] - (ay + t * vy))

    # exact, tiled: a segment can only be the nearest one to a tile's points if
    # its bbox lower bound is within the smallest corner-distance upper bound
    # (distance to a segment is convex, so its max over a box is at a corner)
    d = np.empty(X.shape)
    T = 48
    allidx = np.arange(len(A))
    for j0 in range(0, X.shape[0], T):
        for i0 in range(0, X.shape[1], T):
            tx = X[j0:j0 + T, i0:i0 + T]
            ty = Y[j0:j0 + T, i0:i0 + T]
            bx0, bx1, by0, by1 = tx.min(), tx.max(), ty.min(), ty.max()
            cx = np.array([bx0, bx1, bx1, bx0])
            cy = np.array([by0, by0, by1, by1])
            ub = seg_dist(cx, cy, allidx).max(axis=1).min()
            gx = np.maximum(0.0, np.maximum(sx0 - bx1, bx0 - sx1))
            gy = np.maximum(0.0, np.maximum(sy0 - by1, by0 - sy1))
            idx = allidx[np.hypot(gx, gy) <= ub + 1e-9]
            dd = seg_dist(tx.ravel(), ty.ravel(), idx).min(axis=0)
            d[j0:j0 + T, i0:i0 + T] = dd.reshape(tx.shape)
    inside = MplPath(P).contains_points(np.c_[X.ravel(), Y.ravel()]).reshape(X.shape)
    return np.where(inside, d, 0.0)


# ===========================================================================
# stroke helpers
# ===========================================================================
def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _cmds_polys(cmds: Sequence[GCodeCommand]) -> List[Poly]:
    """The pen-down polylines of a command list (for measurement)."""
    polys: List[Poly] = []
    cur: Optional[Poly] = None
    pos: Pt = (0.0, 0.0)
    for c in cmds:
        if c.command == "G0" and c.x is not None:
            pos = (c.x, c.y)
        elif c.command == "M3":
            cur = [pos]
            polys.append(cur)
        elif c.command == "M5":
            cur = None
        elif c.command == "G1" and c.x is not None and cur is not None:
            cur.append((c.x, c.y))
    return [p for p in polys if len(p) >= 2]


def _chain_order(polys: Sequence[Poly], start: Pt = (0.0, 0.0)) -> List[Poly]:
    """Greedy nearest-END order with reversal.  The pipeline's per-pen
    optimiser only looks at stroke STARTS, so a family of parallel open rings
    all running the same way costs one sheet-crossing travel per ring; this
    turns them into a boustrophedon the optimiser then follows."""
    left = [list(p) for p in polys if len(p) >= 2]
    out: List[Poly] = []
    pos = start
    while left:
        best, bd, rev = 0, 1e18, False
        for k, p in enumerate(left):
            d0 = (p[0][0] - pos[0]) ** 2 + (p[0][1] - pos[1]) ** 2
            d1 = (p[-1][0] - pos[0]) ** 2 + (p[-1][1] - pos[1]) ** 2
            if d0 < bd:
                best, bd, rev = k, d0, False
            if d1 < bd:
                best, bd, rev = k, d1, True
        p = left.pop(best)
        if rev:
            p = p[::-1]
        out.append(p)
        pos = p[-1]
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
    # the spiral ends at (x + r, y), where the rim starts: one pen-down, not two
    m = max(14, int(26 * r))
    pts += [(x + r * math.cos(2 * math.pi * k / m), y + r * math.sin(2 * math.pi * k / m))
            for k in range(1, m + 1)]
    return _poly(pts, color=pen, f=1600)


def _arc(x: float, y: float, r: float, sweep: float, start: float = math.pi / 2) -> Poly:
    """Clockwise arc from 12 o'clock (a gauge), ``sweep`` radians."""
    m = max(3, int(math.ceil(sweep * r / 0.25)))
    return [(x + r * math.cos(start - sweep * k / m), y + r * math.sin(start - sweep * k / m))
            for k in range(m + 1)]


def collar_polys(x: float, y: float, r_in: float, area: float) -> Tuple[List[Poly], float]:
    """A collar whose INK AREA is ``area`` (mm^2) at nib NIB.

    Passes are concentric at COLLAR_PITCH (>= NIB, so no pass overdraws the
    last); a full pass of radius r inks 2 pi r NIB.  Full passes are laid from
    r_in outward while they fit the budget; the remainder is ONE partial pass,
    a clockwise arc from 12 o'clock whose sweep = remainder / (r NIB).  So a
    tap below one full ring is a gauge whose angle is proportional to |w|.
    Returns the polylines and the ink area actually drawn (model).
    """
    polys: List[Poly] = []
    left = area
    r = r_in
    drawn = 0.0
    while left > 1e-9:
        full = 2 * math.pi * r * NIB
        if left >= full:
            polys.append(_arc(x, y, r, 2 * math.pi))
            left -= full
            drawn += full
            r += COLLAR_PITCH
            continue
        sweep = left / (r * NIB)
        polys.append(_arc(x, y, r, sweep))
        drawn += sweep * r * NIB
        left = 0.0
    return polys, drawn


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


def _arc_param(src: Poly, pt: Pt) -> float:
    """Arc-length position of ``pt`` along the polyline ``src`` (nearest point)."""
    A = np.asarray(src[:-1], float)
    B = np.asarray(src[1:], float)
    V = B - A
    L = np.hypot(V[:, 0], V[:, 1])
    cum = np.concatenate([[0.0], np.cumsum(L)])[:-1]
    t = np.clip(((pt[0] - A[:, 0]) * V[:, 0] + (pt[1] - A[:, 1]) * V[:, 1]) / np.maximum(L * L, 1e-12),
                0.0, 1.0)
    d = np.hypot(A[:, 0] + t * V[:, 0] - pt[0], A[:, 1] + t * V[:, 1] - pt[1])
    k = int(np.argmin(d))
    return float(cum[k] + t[k] * L[k])


def _bridge(pieces: List[Poly], gap: float, src: Poly) -> List[Poly]:
    """Re-join consecutive clip pieces when what the cut removed between them
    is shorter than ``gap`` MEASURED ALONG THE RING (a ring grazing a corner
    comes back as a hook, not a cut).  Measuring the chord instead joined the
    two arms of a chevron whose tip dips under the cut: a 0.6 mm sliver with a
    tick across it."""
    out: List[Poly] = []
    for pc in pieces:
        if out and math.hypot(out[-1][-1][0] - pc[0][0], out[-1][-1][1] - pc[0][1]) < gap:
            removed = _arc_param(src, pc[0]) - _arc_param(src, out[-1][-1])
            if 0.0 <= removed < gap:
                out[-1] = out[-1] + pc
                continue
        out.append(list(pc))
    return out


def _front_chain(ring: Poly, lat: Bounds) -> Poly:
    """The staircase part of the read region's boundary ring: every vertex
    that is not on the lattice's left, bottom or top edge, as one open chain from
    the image's top edge to its bottom edge."""
    n = len(ring)
    on_border = [abs(p[0] - lat[0]) < 1e-6 or abs(p[1] - lat[1]) < 1e-6 or abs(p[1] - lat[3]) < 1e-6
                 for p in ring]
    # start at the first vertex after the border run
    k0 = next(k for k in range(n) if on_border[k - 1] and not on_border[k])
    chain: Poly = []
    k = k0 - 1  # include the border vertex the staircase leaves from
    while True:
        chain.append(ring[k % n])
        k += 1
        if on_border[k % n]:
            chain.append(ring[k % n])
            break
    return chain


def _rect(x0: float, y0: float, x1: float, y1: float) -> Poly:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


# ===========================================================================
# the computation — everything the sheet shows is read off this dict
# ===========================================================================
def log_kernel(size: int = KSIZE, sigma: float = LOG_SIGMA) -> np.ndarray:
    """Discrete Laplacian of Gaussian, made exactly zero-sum."""
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
    # the lattice fills the crop's width and hangs from its top edge: the
    # image's top and right edges ARE the crop
    lat_x0 = fx1 - NX * CELL
    lat_y0 = fy1 - NY * CELL
    lat = (lat_x0, lat_y0, lat_x0 + NX * CELL, lat_y0 + NY * CELL)

    oc = _outline_cells()
    outline = _resample_ring([(lat_x0 + c * CELL, lat_y0 + r * CELL) for c, r in oc], 0.9)

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
    swept = [(i, j) for j in range(oy) for i in range(ox) if i + j <= T_FRONT]
    # normalise by the strongest READ response: the one the sheet can show
    ymax = max(abs(float(Yr[j, i])) for i, j in swept)
    count = np.rint(N_RINGS * np.abs(Yr) / ymax).astype(int)

    read = np.zeros((NY, NX), bool)
    for (i, j) in swept:
        read[j * STRIDE: j * STRIDE + KSIZE, i * STRIDE: i * STRIDE + KSIZE] = True
    ring_cells = _mask_ring(read)
    shown = read.copy()
    hi, hj = HEAD
    shown[hj * STRIDE: hj * STRIDE + KSIZE, hi * STRIDE: hi * STRIDE + KSIZE] = True
    # dot area = x / (the largest x the sheet SHOWS as a dot); the whorl's
    # unread core is 3x larger and is carried by rings, not dots
    pmax = float(P[shown].max())

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
        lat=lat, outline=outline, P=P, pmax=pmax, shown=shown, K=K, Y=Yr, ymax=ymax, count=count,
        ox=ox, oy=oy, swept=swept, read=read, front=[to_mm(p) for p in ring_cells],
        window=window, node_centre=node_centre, cell_centre=cell_centre,
        frame=(fx0, fy0, fx1, fy1),
    )


# ===========================================================================
# drawing pieces
# ===========================================================================
def _thumbprint(outline: Poly, crop: Bounds, pitch: float) -> List[Poly]:
    """Level sets of the distance-to-outline field at a constant pitch, over
    the crop only (the field continues beyond it)."""
    x0, y0, x1, y1 = crop
    step = 0.30
    xs = np.arange(x0 - 1.0, x1 + 1.0 + step, step)
    ys = np.arange(y0 - 1.0, y1 + 1.0 + step, step)
    X, Y = np.meshgrid(xs, ys)
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


def _rings_polys(cx: float, cy: float, n: int, start: float = 0.0) -> List[Poly]:
    """``n`` response rings; ``start`` is the angle where each ring begins and
    ends (it only decides where the pen lands, i.e. the stroke order)."""
    polys = []
    for k in range(n):
        r = RESP_R1 + k * RESP_PITCH
        m = max(40, int(14 * r))
        polys.append([(cx + r * math.cos(start + 2 * math.pi * t / m),
                       cy + r * math.sin(start + 2 * math.pi * t / m)) for t in range(m + 1)])
    return polys


def sample_radius(v: float) -> float:
    """Dot AREA = x (normalised): r = RMAX * sqrt(v), floored for the pen."""
    return max(DOT_RMIN, DOT_RMAX * math.sqrt(max(v, 0.0)))


def _hatch(region: Region, box: Bounds, pitch: float) -> List[Poly]:
    """45-degree hatch FALLING to the right (lines x + y = c) over ``box``,
    clipped to ``region``.  Falling, not rising: the unread rings leave the
    card rising at 30-45 degrees, and a shadow hatched parallel to them read
    as more field, not as a shadow."""
    x0, y0, x1, y1 = box
    out: List[Poly] = []
    step = pitch * math.sqrt(2)
    c = math.floor((x0 + y0) / step) * step  # phase-locked to the sheet origin
    while c <= x1 + y1:
        seg = [(c - y0, y0), (c - y1, y1)]
        for pc in clip(seg, region, keep="inside"):
            if _plen(pc) >= 0.6:
                out.append(pc)
        c += step
    return out


def head_geometry(M: Dict) -> Dict:
    hi, hj = HEAD
    hx0, hy0, hx1, hy1 = M["window"](hi, hj)
    S = SHADOW
    # card + shadow silhouette (CCW, rectilinear): what field marks stop at
    sil = [(hx0, hy0), (hx0 + S, hy0), (hx0 + S, hy0 - S), (hx1 + S, hy0 - S),
           (hx1 + S, hy1 - S), (hx1, hy1 - S), (hx1, hy1), (hx0, hy1)]
    # the visible shadow: shadow rect minus card (an L), right and bottom only
    L = [(hx0 + S, hy0 - S), (hx1 + S, hy0 - S), (hx1 + S, hy1 - S), (hx1, hy1 - S),
         (hx1, hy0), (hx0 + S, hy0)]
    return dict(card=(hx0, hy0, hx1, hy1), sil=sil, L=L)


# ===========================================================================
# the plate
# ===========================================================================
def convolutions_cropfield(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    M = build_model(bounds)
    outline = M["outline"]
    P, K, Yr, count = M["P"], M["K"], M["Y"], M["count"]
    node_centre, cell_centre = M["node_centre"], M["cell_centre"]
    lat = M["lat"]
    crop = lat  # the image's top and right edges are the crop
    crop_r = Rect(lat[0] - 50.0, lat[1] - 50.0, lat[2], lat[3])
    out: List[GCodeCommand] = []

    front = M["front"]
    front_cut = Polygon(_grow_rectilinear(front, GAP))

    H = head_geometry(M)
    hx0, hy0, hx1, hy1 = H["card"]
    # field marks stop GAP beyond the card's keyline ink and the shadow's edge
    sil_cut = Polygon(_grow_rectilinear(H["sil"], GAP + KEY_BAND))
    cut: Region = front_cut | sil_cut

    # ---------------- 1. X ahead of the wavefront (black) --------------------
    rings: List[Poly] = []
    for ch in _thumbprint(outline, crop, X_RING_PITCH):
        for part in clip(ch, crop_r, keep="inside"):
            for piece in _bridge(clip(part, cut, keep="outside"), 1.2, part):
                if _plen(piece) >= 3.0:  # no crumbs at the cut
                    rings.append(piece)
    # every level set is exactly X_RING_PITCH from the next (|grad d| = 1), so
    # the only places two ring lines can come closer than the pen floor are
    # the chevron tips on the unread arm's ridge, where both flanks of one
    # level meet.  The engine's spacing guardrail opens those tips: the ridge
    # stays a line of bare paper instead of a dark seam.
    ring_cmds = enforce_line_spacing(_emit(_chain_order(rings, (lat[2], lat[3])), BLACK),
                                     min_dist=GAP - 0.05, min_run=3.0)
    LAST["rings"] = _cmds_polys(ring_cmds)
    out += ring_cmds
    # the outline (x = 0 level) is X's heaviest ring: a second pass outward
    # pass 1 runs from the wavefront out to the frame, pass 2 comes back, so
    # the plotter never crosses the sheet to start the second pass
    ol_polys: List[Poly] = []
    for k, off in enumerate((0.0, NIB)):
        ol = _offset_out(outline, off)
        for part in clip(ol + [ol[0]], crop_r, keep="inside"):
            for p in clip(part, cut, keep="outside"):
                if _plen(p) < 1.5:
                    continue
                p = list(p)
                if (p[0][0] > p[-1][0]) != (k == 1):
                    p = p[::-1]
                ol_polys.append(p)
    LAST["outline"] = ol_polys
    out += _emit(ol_polys, BLACK)

    # the wavefront: the read boundary, the WHOLE staircase from the image's
    # top edge to its bottom edge.  Where X = 0 it is the only trace of the
    # windows that read nothing (12 of the 66 read exact zeros), and its foot
    # is the column the key and the title stand on.
    wave = [q for q in clip(_front_chain(front, lat) , sil_cut, keep="outside") if _plen(q) >= 2.0]
    LAST["front"] = wave
    out += _emit(wave, BLACK, f=1800)

    # ---------------- 2. behind the wavefront: every sample X (black) -------
    pmax = M["pmax"]
    read = M["read"]
    hi, hj = HEAD
    head_cells = {(hi * STRIDE + a, hj * STRIDE + b) for a in range(KSIZE) for b in range(KSIZE)}
    dots: List[Tuple[float, float, float]] = []
    for cj in range(M["P"].shape[0]):
        for ci in range(M["P"].shape[1]):
            if not (read[cj, ci] or (ci, cj) in head_cells):
                continue
            if P[cj, ci] <= 1e-9:
                continue  # x = 0 is paper (dot area = x)
            px, py = cell_centre(ci, cj)
            r = sample_radius(float(P[cj, ci]) / pmax)
            dots.append((px, py, r))
            out += _disc(px, py, r, BLACK)

    # ---------------- 3. the head: a card lying on the field ---------------
    for k in range(KEY_PASSES):
        d = k * KEY_PITCH
        out += _emit([_rect(hx0 - d, hy0 - d, hx1 + d, hy1 + d)], BLACK, f=1600)
    # hatched drop shadow; the samples beneath it stay visible (a shadow is a
    # tone, not a cover): the hatch stops COLLAR_PAPER + NIB short of each dot
    shade: Region = Polygon(H["L"])
    for (px, py, r) in dots:
        if hx0 - 6 < px < hx1 + SHADOW + 6 and hy0 - SHADOW - 6 < py < hy1 + 6:
            shade = shade & ~Circle(px, py, r + NIB + COLLAR_PAPER)
    L = H["L"]
    lb = (min(p[0] for p in L), min(p[1] for p in L), max(p[0] for p in L), max(p[1] for p in L))
    out += _emit(_hatch(shade, lb, SHADOW_HATCH), BLACK, f=1800)

    # ---------------- 4. Y = K * X, written on X's own nodes -----------------
    for (i, j) in M["swept"]:
        n = int(count[j, i])
        if n == 0:
            continue
        cx, cy = node_centre(i, j)
        pen = RED if Yr[j, i] > 0 else BLUE
        kept: List[Poly] = []
        for pl in _rings_polys(cx, cy, n):
            kept += [p for p in clip(pl, sil_cut, keep="outside") if _plen(p) >= 1.0]
        out += _emit(kept, pen)

    # the kernel's taps: collars around the samples they multiply
    for (px, py, pen, polys) in head_collars(M)[0]:
        out += _emit(polys, pen, f=1800)

    # ---------------- 5. key + title (the image's blank lower right) --------
    out += _key_and_title(M)
    return out


def head_collars(M: Dict):
    """Collar ink area = a0 |w| on every tap.  a0 is the largest value for
    which every collar still fits inside its own cell minus half a pen gap."""
    P, K = M["P"], M["K"]
    pmax = M["pmax"]
    hi, hj = HEAD
    r_max = CELL / 2.0 - GAP / 2.0 - NIB / 2.0  # outermost pass centreline
    taps = []
    a0 = None
    for a in range(KSIZE):
        for b in range(KSIZE):
            ci, cj = hi * STRIDE + a, hj * STRIDE + b
            px, py = M["cell_centre"](ci, cj)
            r_dot = sample_radius(float(P[cj, ci]) / pmax)
            r_in = r_dot + NIB + COLLAR_PAPER  # pass centreline: ink edge 0.6 mm off the dot's ink
            n_full = int((r_max - r_in) / COLLAR_PITCH) + 1
            cap = sum(2 * math.pi * (r_in + k * COLLAR_PITCH) * NIB for k in range(n_full))
            w = float(K[b, a])
            a0 = cap / abs(w) if a0 is None else min(a0, cap / abs(w))
            taps.append((px, py, r_in, w, a, b))
    out = []
    table = []
    for (px, py, r_in, w, a, b) in taps:
        polys, drawn = collar_polys(px, py, r_in, a0 * abs(w))
        out.append((px, py, RED if w > 0 else BLUE, polys))
        table.append((a, b, w, a0 * abs(w), drawn))
    return out, table, a0


# ===========================================================================
# type
# ===========================================================================
def _weighted_glyph(ch: str, x: float, y: float, h: float, weight: float, pen: int) -> List[GCodeCommand]:
    """One display glyph with real weight, offset SEGMENT by segment.

    kit.giant_type offsets a whole stroke by averaged vertex normals, which
    collapses at the N's acute joins and left both diagonals as hairlines
    (A12).  Here every straight segment gets its own parallel passes."""
    sc = h / 6.0
    passes = max(2, int(round(weight / 0.25)) + 1)
    out: List[GCodeCommand] = []
    for stroke in _GLYPHS[ch]:
        pts = [(x + gx * sc, y + gy * sc) for gx, gy in stroke]
        for p, q in zip(pts, pts[1:]):
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(dx, dy)
            if L < 1e-9:
                continue
            nx, ny = -dy / L, dx / L
            # the passes of one segment as ONE boustrophedon stroke: the
            # 0.25 mm step between passes lies inside the inked width
            zig: Poly = []
            for k in range(passes):
                d = -weight / 2.0 + weight * k / (passes - 1)
                a = (p[0] + nx * d, p[1] + ny * d)
                b = (q[0] + nx * d, q[1] + ny * d)
                zig += [a, b] if k % 2 == 0 else [b, a]
            out += _poly(zig, color=pen, f=2000)
    return out


def _title(text: str, x: float, y: float, h: float, weight: float) -> List[GCodeCommand]:
    """Set glyph by glyph on its INK box (shift by the glyph's own left ink
    edge, advance = ink width + one bearing), so a serifed I sits centred."""
    sc = h / 6.0
    bearing = 1.25
    cmds: List[GCodeCommand] = []
    cx = x
    for ch in text:
        xs = [pt[0] for stroke in _GLYPHS[ch] for pt in stroke]
        x0g, x1g = min(xs), max(xs)
        cmds += _weighted_glyph(ch, cx - x0g * sc, y, h, weight, BLACK)
        cx += (x1g - x0g + bearing) * sc
    return cmds


def _title_width(text: str, h: float) -> float:
    sc = h / 6.0
    w = 0.0
    for ch in text:
        xs = [pt[0] for stroke in _GLYPHS[ch] for pt in stroke]
        w += (max(xs) - min(xs) + 1.25) * sc
    return w - 1.25 * sc


KEY_TH = 2.2  # key cap height
KEY_LEAD = 4.4  # line pitch inside a key row


def key_layout(M: Dict) -> Dict:
    """Title and key share ONE left edge, which is a lattice column line; the
    title's baseline is a lattice row centre."""
    lat = M["lat"]
    # half a cell right of the front's foot (its last riser is column line 25)
    kx0 = lat[0] + 25.5 * CELL
    kx1 = lat[2] - 7.0  # 10 mm inside the drawable edge
    title = "CONVOLUTIONS"
    th = (kx1 - kx0) / _title_width(title, 1.0)
    base = lat[1] + 0.5 * CELL  # bottom sample row
    return dict(kx0=kx0, kx1=kx1, th=th, base=base, title=title)


def _key_and_title(M: Dict) -> List[GCodeCommand]:
    lat = M["lat"]
    Lk = key_layout(M)
    kx0, th, base = Lk["kx0"], Lk["th"], Lk["base"]
    out: List[GCodeCommand] = []
    out += _title(Lk["title"], kx0, base, th, 0.5)

    # every icon's left ink edge sits on kx0, the title's left ink edge
    lx = kx0 + 12.0  # text column

    def text(s: str, y: float) -> List[GCodeCommand]:
        return _stroke_text(s, lx, y, KEY_TH, color=BLACK, f=2000)

    # rows are laid from the title up, on lattice rows (one row = one CELL)
    def row_y(k: int) -> float:
        return lat[1] + (k + 0.5) * CELL

    # 1. X  (top row): pin, mid, max
    y = row_y(9)
    xr = kx0
    for v in (0.07, 0.35, 1.0):
        r = sample_radius(v)
        out += _disc(xr + r, y, r, BLACK)
        xr += 2 * r + 1.0
    out += text("X   dot area = x", y + 0.9)
    floor = 100.0 * (DOT_RMIN / DOT_RMAX) ** 2  # below this x the dot is held at the pen floor
    out += text("no dot: x = 0 \u00b7 smallest: x < %d%%" % round(floor), y - KEY_LEAD + 0.9)
    # 2. K: a collar gauge (two full passes + a partial one)
    y = row_y(7)
    r_in = 0.8 + NIB + COLLAR_PAPER
    polys, _ = collar_polys(0.0, 0.0, r_in, 2 * math.pi * NIB * (2 * r_in + COLLAR_PITCH) + 2.0)
    r_out = r_in + 2 * COLLAR_PITCH
    ix = kx0 + r_out
    out += _disc(ix, y, 0.8, BLACK)
    out += _emit([[(px + ix, py + y) for px, py in pl] for pl in polys], BLUE, f=1800)
    out += text("K   5\u00d75 LoG, stride 2", y + 0.9)
    out += text("collar ink = |w|", y - KEY_LEAD + 0.9)
    # 3. Y
    y = row_y(5)
    ix = kx0 + RESP_R1 + 2 * RESP_PITCH
    out += _disc(ix, y, 0.6, BLACK)
    # where each key ring starts decides the per-pen optimiser's route (it
    # orders strokes by their start points): the sign icon below starts on the
    # side facing the field, the Y icon's rings start upper-right, so the pen
    # enters the key at the sign icon and leaves it from the Y icon, the end
    # nearest the kernel card (A19: crimson's longest travel 114 mm, was 123)
    out += _emit(_rings_polys(ix, y, 3, start=0.25 * math.pi), RED)
    out += text("Y = K \u2217 X   1-4 rings by |y|", y + 0.9)
    out += text("no ring: |y| < max|y| / 8", y - KEY_LEAD + 0.9)
    # 4. what it found: each sign icon sits on its own line
    y = row_y(3)
    c1 = (kx0 + RESP_R1, y + 0.9 + 1.1)
    c2 = (kx0 + RESP_R1 + 2.1, y - KEY_LEAD + 0.9 + 1.1)
    out += _disc(c1[0], c1[1], 0.35, BLACK) + _emit(_rings_polys(c1[0], c1[1], 1, start=0.874 * math.pi), RED)
    out += _disc(c2[0], c2[1], 0.35, BLACK) + _emit(_rings_polys(c2[0], c2[1], 1), BLUE)
    out += text("crimson +  where X starts", y + 0.9)
    out += text("blue \u2212  where X peaks (skeleton)", y - KEY_LEAD + 0.9)
    out += text("blank  X flat, \u2207\u00b2X ~ 0", y - 2 * KEY_LEAD + 0.9)
    return out
