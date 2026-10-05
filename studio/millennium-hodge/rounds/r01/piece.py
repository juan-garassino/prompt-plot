"""HODGE CONJECTURE — faithful reconstruction, r01.  Millennium plate 5.

A CIRCLE IS TWO STRAIGHT LINES.  The real points of the smooth quadric
Q = P1 x P1, drawn as the hyperboloid x^2 + y^2 - z^2 = 1 (|z| <= 2) and ONLY
as its two families of straight rulings: blue A(a, s) = (cos a - s sin a,
sin a + s cos a, s) = the cycles of class [A], gold B(b, s) = (cos b + s sin b,
sin b - s cos b, s) = class [B].  A plane turned about the tangent line at
p = (cos a0, sin a0, 0) cuts the pencil z = tan(psi) (n.X - 1): circle (psi 0)
-> ellipses -> parabola (45) -> hyperbolas -> at psi 90 the pair of strings
A(a0) u B(a0).  Every member is ONE class, [A] + [B].  Green (blue + yellow)
is the sum.  The lower row: genuine curves of class a[A] + b[B] on the same
surface, (p, q) windings a = q u + c, b = p u.

Lineage: Naum Gabo, *Linear Construction in Space No. 1* (1942-43, Tate
T00191).  Order taken: a curved surface made only of straight strings, with
a void bounded by their envelopes.  Here the strings are the algebraic
cycles and the void is the see-through throat.

FAITHFUL thesis: an illustrator's reconstruction of ``ref/reference.png``
(1024 x 1536).  Measured off the raster (colour masks: blue b-r > 25, gold
r-b > 45 & g-b > 20; dark text mask; closed-mask BFS for the hole), in
normalised sheet (u right, v DOWN):

    hero colour mass   u 0.238..0.918, v 0.032..0.500, centroid (0.540, 0.291)
                       blue centroid u 0.431 (left), gold centroid u 0.681
                       (right): the reference splits the colours by side
    hero hole          u 0.467..0.623, v 0.284..0.344, centre (0.538, 0.312)
                       = 0.156 W x 0.060 H (~46 x 25 mm @A3)
    title              u 0.036..0.499, v 0.021..0.089, two lines, caps
                       v 0.021-0.045 and 0.057-0.087 (~10 mm @A3)
    left text column   u 0.036..0.231, v 0.180..0.445
    right text column  u 0.809..0.971, v 0.029..0.455 (-> cut, one corner caption)
    row C0..C4         u 0.128..0.927, v 0.573..0.663
    row sums           u 0.058..0.838, v 0.716..0.839 (CUT: dossier lie 4)
    footer tagline     u 0.127..0.872, v 0.916..0.954 (-> honesty line)

On this sheet (A3, v down): hero u 0.27..0.95, v 0.14..0.62; the eye centre
(0.634, 0.383), 66.7 x 27.2 mm tilted -30 deg (larger than the reference's
hole, and real); row v 0.73..0.86; title v 0.035..0.09.

Faithful to: hero upper-right leaning, the lens hole just right of centre,
a text column down the left, a five-cell row below, blue + gold fine line
on cream.  Every form replaced by a real one (encoding.md 5F table).

Design space: the A3 portrait sheet in mm, y measured UP, frame
[15, 282] x [15, 405]; mapped uniformly onto the passed bounds.  Physical
floors (0.8 mm string gap, 1.3 mm pencil stagger, caps >= 1.8 mm) are held
in PAPER mm and re-run -- never scaled -- on smaller paper.

Visibility is exact: a surface sample P is hidden iff the ray P + t v
(t > 0, v toward the viewer) meets x^2 + y^2 - z^2 = 1 again with |z| <= 2.
On the surface that is one closed-form root t* = -2 P.D.v / v.D.v.  Every
visibility / LOD / halo flip is bisected in the curve parameter, so each
blue or gold run is ONE straight G1 from end to end.

Pens (colors >= 4), plotting order light -> dark:
    0 GOLD   ochre pigment fineliner 0.2   family B, the [B] cycles
    1 BLUE   ultramarine fineliner 0.2     family A, the [A] cycles
    2 GREEN  deep green 0.5                sums a[A] + b[B]
    3 TEXT   black 0.3                     type, own layer

Entry point: ``hodge_circle_is_two_lines_faithful``.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.material import suppress_parallel
from promptplot.generative.engine.scene3d import HIDE, Scene3D
from promptplot.generative.generators import _GLYPHS
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

GOLD, BLUE, GREEN, TEXT = range(4)

# ---------------------------------------------------------------------------
# the mathematics (encoding.md section 4) -- all exact
# ---------------------------------------------------------------------------

H = 2.0                          # rims |z| <= 2: rim radius sqrt(5)
N_HERO = 96                      # strings per family, hero
N_CELL = 32                      # strings per family, row cells
ALPHA0 = math.radians(235.0)     # the hinge p, index 0 of both families
PSI_DEG = (0.0, 15.0, math.degrees(0.5 * math.atan(2.0)), 45.0, 60.0, 75.0)

# ---------------------------------------------------------------------------
# layout (A3 design mm, y up) -- encoding.md 5F
# ---------------------------------------------------------------------------

FRAME = (15.0, 15.0, 282.0, 405.0)
ELEV = math.radians(50.0)        # viewer azimuth 0, elevation 50 (48..54 allowed)
ROLL = math.radians(-30.0)       # screen roll, shared by hero and every cell (NOTES: why -30)
HERO_BOX = (95.0, 140.0, 282.0, 378.0)
CELL_Y = (60.0, 114.0)
CELL_W = 44.0
CELL_PITCH = 55.75

FLOOR = 0.8                      # same-family gap floor, paper mm
STAGGER = 0.8 + 0.5              # green gap floor: 0.8 + green nib
X_PASS_OFF = 0.15                # the X's 3 passes, paper mm apart
MIN_RUN = 4.0                    # no string run shorter than this (paper mm)
CAP_MIN = 1.4                     # caps >= 1.4 mm on paper (A5); A3 caps are all >= 1.8 by design
NIB = {GOLD: 0.2, BLUE: 0.2, GREEN: 0.5, TEXT: 0.3}
F_DRAW = 1800


class Sheet:
    """Uniform map from the A3 design frame onto the passed bounds."""

    def __init__(self, bounds: Bounds):
        bx0, by0, bx1, by1 = bounds
        fx0, fy0, fx1, fy1 = FRAME
        self.k = min((bx1 - bx0) / (fx1 - fx0), (by1 - by0) / (fy1 - fy0))
        self.ox = bx0 + 0.5 * ((bx1 - bx0) - self.k * (fx1 - fx0))
        self.oy = by0 + 0.5 * ((by1 - by0) - self.k * (fy1 - fy0))

    def pt(self, p: Pt) -> Pt:
        return (self.ox + self.k * (p[0] - FRAME[0]), self.oy + self.k * (p[1] - FRAME[1]))

    def phys(self, mm: float) -> float:
        return mm / self.k

    def cap(self, c: float) -> float:
        return max(c, CAP_MIN / self.k)


# ------------------------------------------------------------------ surface


def ruling(fam: str, a: float, s):
    """A (blue) or B (gold) string through the waist point at angle a."""
    ca, sa = math.cos(a), math.sin(a)
    s = np.asarray(s, dtype=float)
    if fam == "A":
        return np.stack([ca - s * sa, sa + s * ca, s], -1)
    return np.stack([ca + s * sa, sa - s * ca, s], -1)


def ruling_dirs(fam: str, a: float, s: float) -> Tuple[np.ndarray, np.ndarray]:
    """(d/da, d/ds) of a ruling at (a, s)."""
    ca, sa = math.cos(a), math.sin(a)
    if fam == "A":
        return np.array([-sa - s * ca, ca - s * sa, 0.0]), np.array([-sa, ca, 1.0])
    return np.array([-sa + s * ca, ca + s * sa, 0.0]), np.array([sa, -ca, 1.0])


def torus_point(a, b):
    """P(a, b) = A(a, tan((b - a)/2)): the point on string A(a) and string B(b)."""
    a = np.asarray(a, dtype=float)
    s = np.tan(0.5 * (np.asarray(b, dtype=float) - a))
    return np.stack([np.cos(a) - s * np.sin(a), np.sin(a) + s * np.cos(a), s], -1), s


class View:
    """Orthographic view: azimuth 0, elevation ELEV, screen roll ROLL,
    k design-mm per unit, centred at (cx, cy)."""

    def __init__(self, k: float, cx: float, cy: float, elev: float = ELEV,
                 roll: Optional[float] = None):
        roll = ROLL if roll is None else roll
        self.k, self.cx, self.cy = k, cx, cy
        self.v = np.array([math.cos(elev), 0.0, math.sin(elev)])       # toward viewer
        r = np.array([0.0, 1.0, 0.0])
        u = np.array([-math.sin(elev), 0.0, math.cos(elev)])
        c, s = math.cos(roll), math.sin(roll)
        self.ex = c * r - s * u
        self.ey = s * r + c * u
        self.vDv = self.v[0] ** 2 + self.v[1] ** 2 - self.v[2] ** 2    # cos 2e

    def xy(self, P) -> np.ndarray:
        P = np.asarray(P, dtype=float)
        return np.stack([self.cx + self.k * (P @ self.ex), self.cy + self.k * (P @ self.ey)], -1)

    def vec(self, d) -> np.ndarray:
        d = np.asarray(d, dtype=float)
        return np.stack([self.k * (d @ self.ex), self.k * (d @ self.ey)], -1)

    def visible(self, P) -> np.ndarray:
        """Exact: the second root of the ray-quadric equation from a point ON
        the surface, t* = -2 P.D.v / v.D.v, occludes iff t* > 0 and |z| <= H."""
        P = np.atleast_2d(np.asarray(P, dtype=float))
        pdv = P[:, 0] * self.v[0] + P[:, 1] * self.v[1] - P[:, 2] * self.v[2]
        t = -2.0 * pdv / self.vDv
        z = P[:, 2] + t * self.v[2]
        hidden = (t > 1e-9) & (np.abs(z) <= H)
        return ~hidden


def fit_view(box: Tuple[float, float, float, float]) -> View:
    """k and centre so the whole clipped surface's projection fills ``box``."""
    a = np.linspace(0, 2 * np.pi, 721)
    s = np.linspace(-H, H, 161)
    A, S = np.meshgrid(a, s)
    P = np.stack([np.cos(A) - S * np.sin(A), np.sin(A) + S * np.cos(A), S], -1).reshape(-1, 3)
    v1 = View(1.0, 0.0, 0.0)
    Q = v1.xy(P)
    x0, y0, x1, y1 = box
    k = min((x1 - x0) / np.ptp(Q[:, 0]), (y1 - y0) / np.ptp(Q[:, 1]))
    cx = 0.5 * (x0 + x1) - k * 0.5 * (Q[:, 0].min() + Q[:, 0].max())
    cy = 0.5 * (y0 + y1) - k * 0.5 * (Q[:, 1].min() + Q[:, 1].max())
    return View(k, cx, cy)


# ------------------------------------------------------------------ intervals


def intervals(pred: Callable[[np.ndarray], np.ndarray], t0: float, t1: float, n: int,
              tol: float) -> List[Tuple[float, float]]:
    """Maximal sub-intervals of [t0, t1] where ``pred`` holds; every flip
    bisected to ``tol`` in the parameter."""
    ts = np.linspace(t0, t1, n + 1)
    ok = pred(ts)
    out: List[Tuple[float, float]] = []

    def flip(a: float, b: float, a_ok: bool) -> float:
        while b - a > tol:
            m = 0.5 * (a + b)
            if bool(pred(np.array([m]))[0]) == a_ok:
                a = m
            else:
                b = m
        return 0.5 * (a + b)

    start = t0 if ok[0] else None
    for i in range(1, len(ts)):
        if ok[i] != ok[i - 1]:
            x = flip(ts[i - 1], ts[i], bool(ok[i - 1]))
            if ok[i]:
                start = x
            else:
                out.append((start, x))
                start = None
    if start is not None:
        out.append((start, t1))
    return out


def in_boxes(Q: np.ndarray, boxes: Sequence[Tuple[float, float, float, float]]) -> np.ndarray:
    m = np.zeros(len(Q), dtype=bool)
    for bx0, by0, bx1, by1 in boxes:
        m |= (Q[:, 0] >= bx0) & (Q[:, 0] <= bx1) & (Q[:, 1] >= by0) & (Q[:, 1] <= by1)
    return m


# ------------------------------------------------------------------ strings


def string_runs(view: View, fam: str, i: int, n: int, sh: Sheet,
                halos: Sequence = (), lod: bool = True) -> List[Tuple[Pt, Pt]]:
    """Visible, LOD-qualified, halo-free straight runs of string ``i`` of
    ``n``.  LOD by halving: at (a, s) the projected gap to the same-family
    neighbour is g1 = |P_a x P_s| / |P_s| * 2pi/n; the level is the least L
    with g1 * 2^L >= FLOOR, and the string keeps drawing iff i = 0 mod 2^L
    (index 0 survives every level).  Silenced stretches pause and resume."""
    a = ALPHA0 + 2 * math.pi * i / n
    da = 2 * math.pi / n
    floor = sh.phys(FLOOR)

    ca, sa = math.cos(a), math.sin(a)
    if fam == "A":
        ps = np.array([-sa, ca, 1.0])
    else:
        ps = np.array([sa, -ca, 1.0])
    qs = view.vec(ps)
    qs_n = math.hypot(*qs)

    def lod_ok(s: np.ndarray) -> np.ndarray:
        if not lod or i == 0:
            return np.ones(len(s), dtype=bool)
        if fam == "A":
            pa = np.stack([-sa - s * ca, ca - s * sa, 0.0 * s], -1)
        else:
            pa = np.stack([-sa + s * ca, ca + s * sa, 0.0 * s], -1)
        qa = view.vec(pa)
        g1 = np.abs(qa[:, 0] * qs[1] - qa[:, 1] * qs[0]) / max(1e-12, qs_n) * da
        # least power of two m with g1 * m >= floor; string i draws iff i % m == 0
        with np.errstate(divide="ignore"):
            m = np.exp2(np.ceil(np.log2(np.maximum(floor / np.maximum(g1, 1e-12), 1.0))))
        return (m < n) & (np.mod(i, m) == 0)

    def pred(s: np.ndarray) -> np.ndarray:
        P = ruling(fam, a, s)
        ok = view.visible(P) & lod_ok(s)
        if halos:
            ok &= ~in_boxes(view.xy(P), halos)
        return ok

    runs = []
    for s0, s1 in intervals(pred, -H, H, 240, 2e-6):
        p0, p1 = view.xy(ruling(fam, a, [s0, s1]))
        if math.hypot(*(p1 - p0)) >= sh.phys(MIN_RUN):
            runs.append(((float(p0[0]), float(p0[1])), (float(p1[0]), float(p1[1]))))
    return runs


def offset_passes(run: Tuple[Pt, Pt], off: float, passes: int = 3) -> List[Poly]:
    """``passes`` parallel copies of a straight run, ``off`` apart, alternating
    direction (the X's weight: a ~0.5 mm band of 0.2 mm lines)."""
    (x0, y0), (x1, y1) = run
    L = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    out = []
    for k in range(passes):
        o = (k - (passes - 1) / 2) * off
        a = (x0 + nx * o, y0 + ny * o)
        b = (x1 + nx * o, y1 + ny * o)
        out.append([a, b] if k % 2 == 0 else [b, a])
    return out


# ------------------------------------------------------------------ curves


def pencil_member(psi_deg: float):
    """(param -> 3D point, param range) for the plane z = tan(psi)(n.X - 1)
    through the tangent line at p.  Parametrised by the A-string it meets:
    d = a - a0, s = T (cos d - 1) / (1 + T sin d).  d = 0 is p."""
    T = math.tan(math.radians(psi_deg))

    def P(d: np.ndarray):
        d = np.asarray(d, dtype=float)
        den = 1.0 + T * np.sin(d)
        with np.errstate(divide="ignore", invalid="ignore"):
            s = T * (np.cos(d) - 1.0) / den
        a = ALPHA0 + d
        return np.stack([np.cos(a) - s * np.sin(a), np.sin(a) + s * np.cos(a), s], -1), s

    return P


def pq_curve(p: int, q: int, c1: float):
    """alpha = a0 + q u + c1, beta = a0 + p u: a real algebraic curve of class
    p[A] + q[B] (degree p + q)."""

    def P(u: np.ndarray):
        u = np.asarray(u, dtype=float)
        return torus_point(ALPHA0 + q * u + c1, ALPHA0 + p * u)

    return P


def curve_runs(view: View, P, t0: float, t1: float, n: int, closed: bool = False,
               cut: Optional[Tuple[float, float]] = None) -> List[Poly]:
    """Visible, in-rim runs of a parametric curve, flips bisected, each run
    sampled densely then simplified to <= 0.02 mm.  ``cut`` = an open
    parameter interval removed (the pencil stagger around p)."""

    def pred(t: np.ndarray) -> np.ndarray:
        X, s = P(t)
        ok = np.isfinite(s) & (np.abs(s) <= H + 1e-12)
        good = np.where(ok)[0]
        if len(good):
            ok[good] = view.visible(X[good])
        if cut is not None:
            ok &= ~((t > cut[0]) & (t < cut[1]))
        return ok

    ivs = intervals(pred, t0, t1, n, 1e-9)
    if closed and len(ivs) >= 2 and ivs[0][0] == t0 and ivs[-1][1] == t1:
        first = ivs.pop(0)
        last = ivs.pop(-1)
        ivs.append((last[0], first[1] + (t1 - t0)))
    out = []
    for a, b in ivs:
        m = max(8, int((b - a) / (t1 - t0) * n * 6))
        ts = np.linspace(a, b, m + 1)
        X, _ = P(ts)
        Q = view.xy(X)
        out.append(simplify([(float(x), float(y)) for x, y in Q], 0.02))
    return [r for r in out if len(r) >= 2 and poly_len(r) > 0.5]


def poly_len(p: Poly) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))


def simplify(pts: Poly, eps: float) -> Poly:
    """Douglas-Peucker (iterative)."""
    if len(pts) < 3:
        return pts
    P = np.array(pts)
    keep = np.zeros(len(P), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(P) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = P[i], P[j]
        d = b - a
        L = math.hypot(*d)
        seg = P[i + 1:j] - a
        if L < 1e-12:
            dist = np.hypot(seg[:, 0], seg[:, 1])
        else:
            dist = np.abs(seg[:, 0] * d[1] - seg[:, 1] * d[0]) / L
        k = int(np.argmax(dist))
        if dist[k] > eps:
            m = i + 1 + k
            keep[m] = True
            stack.append((i, m))
            stack.append((m, j))
    return [tuple(x) for x in P[keep]]


def dist_to_polys(Q: np.ndarray, polys: Sequence[Poly]) -> np.ndarray:
    """Min distance from each point of Q to a set of polylines."""
    best = np.full(len(Q), np.inf)
    for p in polys:
        A = np.array(p)
        if len(A) < 2:
            continue
        a, b = A[:-1], A[1:]
        d = b - a
        L2 = np.maximum((d ** 2).sum(1), 1e-18)
        for s0 in range(0, len(Q), 2048):
            q = Q[s0:s0 + 2048][:, None, :]
            t = np.clip(((q - a) * d).sum(2) / L2, 0, 1)
            proj = a + t[..., None] * d
            dd = np.sqrt(((q - proj) ** 2).sum(2)).min(1)
            best[s0:s0 + 2048] = np.minimum(best[s0:s0 + 2048], dd)
    return best


def resample(poly: Poly, step: float) -> np.ndarray:
    P = np.array(poly)
    seg = np.hypot(*np.diff(P, axis=0).T)
    arc = np.concatenate([[0.0], np.cumsum(seg)])
    n = max(2, int(math.ceil(arc[-1] / step)) + 1)
    t = np.linspace(0.0, arc[-1], n)
    return np.stack([np.interp(t, arc, P[:, 0]), np.interp(t, arc, P[:, 1])], -1)


def near_dir(Q: np.ndarray, polys: Sequence[Poly]) -> Tuple[np.ndarray, np.ndarray]:
    """(min distance, |cos| between Q's local direction and the nearest
    segment) for each point of a densely resampled polyline Q."""
    dq = np.gradient(Q, axis=0)
    dq /= np.maximum(np.hypot(dq[:, 0], dq[:, 1]), 1e-12)[:, None]
    best = np.full(len(Q), np.inf)
    cosb = np.zeros(len(Q))
    for p in polys:
        A = np.array(p)
        if len(A) < 2:
            continue
        a, d = A[:-1], np.diff(A, axis=0)
        L2 = np.maximum((d ** 2).sum(1), 1e-18)
        un = d / np.sqrt(L2)[:, None]
        for s0 in range(0, len(Q), 1024):
            q = Q[s0:s0 + 1024][:, None, :]
            t = np.clip(((q - a) * d).sum(2) / L2, 0, 1)
            dd = np.sqrt(((q - (a + t[..., None] * d)) ** 2).sum(2))
            j = dd.argmin(1)
            m = dd[np.arange(len(j)), j]
            c = np.abs((dq[s0:s0 + 1024] * un[j]).sum(1))
            upd = m < best[s0:s0 + 1024]
            best[s0:s0 + 1024] = np.where(upd, m, best[s0:s0 + 1024])
            cosb[s0:s0 + 1024] = np.where(upd, c, cosb[s0:s0 + 1024])
    return best, cosb


def green_yield(runs: Sequence[Poly], kept: Sequence[Poly], sh: Sheet,
                align: float = 0.93, min_piece: float = 3.0) -> List[Poly]:
    """The pencil stagger, done structurally: a later member yields every
    stretch that runs closer than STAGGER AND near-parallel (|cos| > align)
    to a green curve already kept.  Around p (all members tangent to the
    hinge line) this stops each member where it has opened to 1.3 mm, so the
    loops pinch into p at staggered lengths; at the throat's apparent contour
    (where every curve turns tangent to the fold) it stops the false second
    pinch.  Crossings pass untouched."""
    thr = sh.phys(STAGGER)
    step = sh.phys(0.25)
    out: List[Poly] = []
    for r in runs:
        Q = resample(r, step)
        if kept:
            d, c = near_dir(Q, kept)
            bad = (d < thr) & (c > align)
        else:
            bad = np.zeros(len(Q), dtype=bool)
        i = 0
        while i < len(Q):
            if bad[i]:
                i += 1
                continue
            j = i
            while j + 1 < len(Q) and not bad[j + 1]:
                j += 1
            piece = [(float(x), float(y)) for x, y in Q[i:j + 1]]
            if len(piece) >= 2 and poly_len(piece) >= sh.phys(min_piece):
                out.append(simplify(piece, 0.02))
            i = j + 1
    return out


def declutter(strings: List[Tuple[str, int, Tuple[Pt, Pt]]], greens: Sequence[Poly],
              sh: Sheet) -> List[Tuple[str, int, Tuple[Pt, Pt]]]:
    """Two structural passes after the LOD, both keeping every run straight.

    1. ``material.suppress_parallel`` over BOTH families at once (0.8 mm,
       |cos| > 0.93): where the throat folds, two sheets of the surface
       overlap on paper and strings from far-apart parts of the model run
       side by side -- the local-neighbour LOD cannot see that.  Longest
       claims first; index 0 (the X) is exempt.
    2. Shadowing: a string stretch running < 0.8 mm from a green curve or
       from the X and near-parallel to it for > 3 mm yields (encoding
       section 10) -- so the X keeps its paper on both sides.

    The engine returns resampled pieces of each input line; every piece is a
    sub-segment of a straight run, so it is re-emitted as ONE G1 between its
    end points and mapped back to its family by collinearity."""
    floor = sh.phys(FLOOR)
    xs = [t for t in strings if t[1] == 0]
    rest = [t for t in strings if t[1] != 0]
    kept = suppress_parallel([list(t[2]) for t in rest], min_dist=floor, align=0.93,
                             sample=sh.phys(0.3), min_run_len=sh.phys(MIN_RUN))

    def owner(a: Pt, b: Pt):
        for t in rest:
            (x0, y0), (x1, y1) = t[2]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 1e-9:
                continue
            for q in (a, b):
                if abs((q[0] - x0) * dy - (q[1] - y0) * dx) / L > 1e-6:
                    break
                u = ((q[0] - x0) * dx + (q[1] - y0) * dy) / (L * L)
                if u < -1e-6 or u > 1 + 1e-6:
                    break
            else:
                return t
        return None

    out = list(xs)
    for piece in kept:
        a, b = piece[0], piece[-1]
        t = owner(a, b)
        if t is None:
            continue
        (x0, y0), (x1, y1) = t[2]
        # keep the run's drawing direction
        if (b[0] - a[0]) * (x1 - x0) + (b[1] - a[1]) * (y1 - y0) < 0:
            a, b = b, a
        out.append((t[0], t[1], ((float(a[0]), float(a[1])), (float(b[0]), float(b[1])))))

    shadows = list(greens) + [list(t[2]) for t in xs]
    if not shadows:
        return out
    step = sh.phys(0.25)
    final = []
    for fam, i, (a, b) in out:
        if i == 0:
            final.append((fam, i, (a, b)))
            continue
        Q = resample([a, b], step)
        d, c = near_dir(Q, shadows)
        bad = (d < floor) & (c > 0.93)
        # only stretches longer than 3 mm count as shadowing
        idx = np.where(bad)[0]
        mask = np.zeros(len(Q), dtype=bool)
        if len(idx):
            groups = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
            for g in groups:
                if (g[-1] - g[0]) * step >= sh.phys(3.0):
                    mask[g[0]:g[-1] + 1] = True
        j = 0
        while j < len(Q):
            if mask[j]:
                j += 1
                continue
            k = j
            while k + 1 < len(Q) and not mask[k + 1]:
                k += 1
            p0, p1 = Q[j], Q[k]
            if math.hypot(*(p1 - p0)) >= sh.phys(MIN_RUN):
                final.append((fam, i, ((float(p0[0]), float(p0[1])), (float(p1[0]), float(p1[1])))))
            j = k + 1
    return final


# ---------------------------------------------------------------------------
# type -- proportional stroke caps with authored glyphs
# ---------------------------------------------------------------------------

_EXTRA = {
    "?": [[(0.6, 4.8), (1.2, 5.8), (2.8, 5.8), (3.4, 4.8), (3.4, 4.0), (2.0, 2.9), (2.0, 1.6)],
          [(1.8, 0.0), (2.2, 0.0), (2.2, 0.4), (1.8, 0.4), (1.8, 0.0)]],
    "—": [[(0.0, 3.0), (5.0, 3.0)]],
    "∩": [[(0.2, 0.0), (0.2, 3.4)] + [(2.1 + 1.9 * math.cos(t), 3.4 + 1.9 * math.sin(t))
                                      for t in np.linspace(math.pi, 0.0, 13)] + [(4.0, 0.0)]],
    # double-struck C and Q: the font's C / Q plus an inner stem
    "ℂ": [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5)], [(1.0, 0.25), (1.0, 5.75)]],
    "ℚ": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0), (1, 0)],
          [(2.6, 1.4), (4.2, -0.4)], [(1.0, 0.25), (1.0, 5.75)]],
    "\u00a0": [],
    "⊕": [[(2.0 + 2.2 * math.cos(t), 3.0 + 2.2 * math.sin(t))
           for t in np.linspace(0, 2 * math.pi, 29)],
          [(2.0, 0.8), (2.0, 5.2)], [(-0.2, 3.0), (4.2, 3.0)]],
}
_SB = 0.75
_SPACE = 3.0
_GCACHE: dict = {}


def _glyph(ch: str):
    if ch in _GCACHE:
        return _GCACHE[ch]
    if ch in (" ", "\u00a0"):
        res = ([], _SPACE)
    else:
        strokes = _EXTRA.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper(), [])
        if ch == "0":
            strokes = strokes[:1]
        xs = [p[0] for st in strokes for p in st]
        if not xs:
            res = ([], _SPACE)
        else:
            x0 = min(xs)
            sh = [[(gx - x0 + _SB, gy) for gx, gy in st] for st in strokes]
            res = (sh, (max(xs) - x0) + 2 * _SB)
    _GCACHE[ch] = res
    return res


Run = Tuple[str, str]


def parse(markup: str) -> List[Run]:
    """'H^{p,q}' -> [('H','n'), ('p,q','sup')]."""
    out: List[Run] = []
    i = 0
    while i < len(markup):
        j = markup.find("^{", i)
        if j < 0:
            out.append((markup[i:], "n"))
            break
        if j > i:
            out.append((markup[i:j], "n"))
        k = markup.index("}", j)
        out.append((markup[j + 2:k], "sup"))
        i = k + 1
    return [r for r in out if r[0]]


def runs_width(runs: Sequence[Run], cap: float, track: float) -> float:
    w, n = 0.0, 0
    for txt, mode in runs:
        c = cap * (0.62 if mode == "sup" else 1.0)
        for ch in txt:
            w += _glyph(ch)[1] * c / 6.0
            n += 1
    return w + track * cap * max(0, n - 1)


def text_runs(runs: Sequence[Run], x: float, y: float, cap: float, track: float = 0.0,
              align: str = "left") -> List[Poly]:
    if align == "right":
        x -= runs_width(runs, cap, track)
    out: List[Poly] = []
    cx = x
    for txt, mode in runs:
        c = cap * (0.62 if mode == "sup" else 1.0)
        base = y + (0.62 * cap if mode == "sup" else 0.0)
        sc = c / 6.0
        for ch in txt:
            strokes, adv = _glyph(ch)
            for st in strokes:
                out.append([(cx + gx * sc, base + gy * sc) for gx, gy in st])
            cx += adv * sc + track * cap
    return out


def text(s: str, x: float, y: float, cap: float, track: float = 0.0, align: str = "left"):
    return text_runs(parse(s), x, y, cap, track, align)


def text_width(s: str, cap: float, track: float = 0.0) -> float:
    return runs_width(parse(s), cap, track)


def wrap(markup: str, cap: float, track: float, max_w: float) -> List[str]:
    lines: List[str] = []
    cur = ""
    for w in markup.split(" "):
        trial = w if not cur else cur + " " + w
        if cur and text_width(trial, cap, track) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def paragraph(markup: str, x: float, y_top: float, cap: float, lead: float, max_w: float,
              track: float = 0.08) -> Tuple[List[Poly], float]:
    """Flush-left block; returns (polys, baseline of the last line)."""
    out: List[Poly] = []
    y = y_top - cap
    for ln in wrap(markup, cap, track, max_w):
        out += text(ln, x, y, cap, track)
        y -= lead
    return out, y + lead


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------

CONJECTURE = ("X SMOOTH COMPLEX PROJECTIVE. IS EVERY RATIONAL HODGE CLASS "
              "— H^{2p}(X,ℚ) ∩ H^{p,p} — A RATIONAL COMBINATION OF CLASSES "
              "OF SUBVARIETIES? (CLAY\u00a0·\u00a0DELIGNE)")
KEY = ("REAL POINTS OF THE COMPLEX QUADRIC P¹×P¹. BLUE, GOLD: ITS TWO FAMILIES "
       "OF LINES [A], [B]. GREEN: CURVES OF CLASS a[A]+b[B]. HERE EVERY CLASS "
       "IS HODGE AND ALGEBRAIC.")
CELLS = (
    ("[A]", "LINE"),
    ("[B]", "LINE"),
    ("[A]+[B]", "CONIC"),
    ("[A]+2[B]", "TWISTED CUBIC"),
    ("2[A]+3[B]", "QUINTIC"),
)


def emit_strings(L: Dict[int, List[Poly]], runs, sh: Sheet, heavy=frozenset()) -> None:
    """Gold then blue, index order, boustrophedon (odd indices reversed) so
    each stroke starts near where the last one ended.  ``heavy`` strings get
    the 3-pass weight."""
    for fam, layer in (("B", GOLD), ("A", BLUE)):
        for i in sorted({t[1] for t in runs if t[0] == fam}):
            rs = [t[2] for t in runs if t[0] == fam and t[1] == i]
            # order along the string by the projected start
            rs.sort(key=lambda r: (r[0][0], r[0][1]))
            if i % 2:
                rs = [(b, a) for a, b in reversed(rs)]
            for r in rs:
                if (fam, i) in heavy:
                    L[layer] += offset_passes(r, sh.phys(X_PASS_OFF))
                else:
                    L[layer].append([r[0], r[1]])


def best_phase(view: View, p: int, q: int) -> float:
    """The free phase c1 (every phase is the same class) that shows the most
    visible in-rim parameter."""
    best, arg = -1.0, 0.0
    u = np.linspace(0, 2 * np.pi, 1441)[:-1]
    for c in np.radians(np.arange(0, 360, 5)):
        X, s = pq_curve(p, q, c)(u)
        ok = np.isfinite(s) & (np.abs(s) <= H)
        vis = np.zeros(len(u), dtype=bool)
        vis[ok] = view.visible(X[ok])
        f = vis.mean()
        if f > best + 1e-9:
            best, arg = f, float(c)
    return arg


def build(sh: Sheet, roll: float = ROLL):
    """All marks in design units: {layer: [polylines]} plus statistics."""
    L: Dict[int, List[Poly]] = {GOLD: [], BLUE: [], GREEN: [], TEXT: []}
    stats: Dict[str, object] = {}
    global ROLL
    ROLL = roll

    hero = fit_view(HERO_BOX)
    stats["hero_k"] = hero.k

    # ---- tags [A] [B] at the upper-rim end of the X strings ------------------
    tag_cap = sh.cap(3.2)
    tags = []
    halos = []
    for fam, name in (("A", "[A]"), ("B", "[B]")):
        top = hero.xy(ruling(fam, ALPHA0, [H]))[0]
        inner = hero.xy(ruling(fam, ALPHA0, [H - 0.3]))[0]
        d = top - inner
        d /= math.hypot(*d)
        w = text_width(name, tag_cap, 0.05)
        gap = sh.phys(2.2)
        # anchor the label box beyond the string end, along its direction
        cx = top[0] + d[0] * (gap + 0.5 * w)
        cy = top[1] + d[1] * (gap + 0.5 * tag_cap)
        x0, y0 = cx - 0.5 * w, cy - 0.5 * tag_cap
        tags.append((name, x0, y0))
        pad = sh.phys(1.4)
        halos.append((x0 - pad, y0 - pad, x0 + w + pad, y0 + tag_cap + pad))

    # ---- the pencil, psi ascending, with the stagger around p ---------------
    p_scr = hero.xy(np.array([[math.cos(ALPHA0), math.sin(ALPHA0), 0.0]]))[0]
    kept: List[Poly] = []
    for psi in PSI_DEG:
        P = pencil_member(psi)
        closed = psi < 45.0 - 1e-9
        runs = curve_runs(hero, P, -math.pi, math.pi, 4000, closed=closed)
        if psi > 0.0:
            runs = green_yield(runs, kept, sh)
        kept += runs
        L[GREEN] += runs
        ends = [q for r in runs for q in (r[0], r[-1])]
        stop = min(math.hypot(q[0] - p_scr[0], q[1] - p_scr[1]) for q in ends) if ends else None
        stats[f"psi_{psi:.2f}"] = {"runs": len(runs), "stop_from_p_mm": stop and round(stop, 1),
                                   "len": round(sum(poly_len(r) for r in runs), 1)}

    # ---- hero strings: LOD runs, declutter, then boustrophedon by index ----
    raw = [(fam, i, r) for fam in ("B", "A") for i in range(N_HERO)
           for r in string_runs(hero, fam, i, N_HERO, sh, halos)]
    clean = declutter(raw, L[GREEN], sh)
    stats["hero_runs"] = {"lod": len(raw), "after_declutter": len(clean)}
    emit_strings(L, clean, sh, heavy={("A", 0), ("B", 0)})

    # ---- the row: five cells, same projection, smaller k --------------------
    cells_meta = []
    for ci, (cls, name) in enumerate(CELLS):
        x0 = FRAME[0] + ci * CELL_PITCH
        cv = fit_view((x0, CELL_Y[0], x0 + CELL_W, CELL_Y[1]))
        cells_meta.append((cv, x0))
        cell_green: List[Poly] = []
        if ci == 2:
            cell_green = curve_runs(cv, pencil_member(0.0), -math.pi, math.pi, 2000, closed=True)
        elif ci >= 3:
            p, q = (1, 2) if ci == 3 else (2, 3)
            c1 = best_phase(cv, p, q)
            # start the parameter where the curve passes through infinity
            u = np.linspace(0, 2 * np.pi, 7201)
            _, s = pq_curve(p, q, c1)(u)
            u_inf = float(u[int(np.nanargmax(np.abs(s)))])
            cell_green = curve_runs(cv, pq_curve(p, q, c1), u_inf, u_inf + 2 * np.pi, 6000)
            stats[f"cell_{p}{q}"] = {"phase_deg": round(math.degrees(c1), 1),
                                     "runs": len(cell_green)}
        L[GREEN] += cell_green
        raw = [(fam, i, r) for fam in ("B", "A") for i in range(N_CELL)
               for r in string_runs(cv, fam, i, N_CELL, sh)]
        heavy = {("A", 0)} if ci == 0 else ({("B", 0)} if ci == 1 else set())
        emit_strings(L, declutter(raw, cell_green, sh), sh, heavy=heavy)

    # ---- type ----------------------------------------------------------------
    T = L[TEXT]
    x_l = FRAME[0]
    tcap = sh.cap(9.0)
    T += text("HODGE", x_l, 396.0, tcap, 0.32)
    T += text("CONJECTURE", x_l, 382.0, tcap, 0.32)
    scap = sh.cap(2.8)
    T += text("IN COHOMOLOGY A CIRCLE", x_l, 370.0, scap, 0.22)
    T += text("IS TWO STRAIGHT LINES.", x_l, 364.0, scap, 0.22)

    col_w = 88.0 - x_l
    bcap = sh.cap(2.2)
    lead = 2.2 * bcap
    polys, _ = paragraph(CONJECTURE, x_l, 345.0, bcap, lead, col_w)
    T += polys
    csub, cdec = sh.cap(1.8), sh.cap(1.9)
    ecap3 = max(sh.cap(3.4), 1.3 * csub)
    T += text("H^{k}(X,ℂ) = ⊕ H^{p,q}", x_l, 262.0, ecap3, 0.06)
    xo = x_l + text_width("H^{k}(X,ℂ) = ", ecap3, 0.06) + 0.5 * text_width("⊕", ecap3)
    y_sub = 262.0 - 2.0 * csub
    T += text("p+q=k", xo - 0.5 * text_width("p+q=k", csub, 0.04), y_sub, csub, 0.04)
    y_dec = y_sub - 3.2 * cdec
    T += text("THE HODGE DECOMPOSITION —", x_l, y_dec, cdec, 0.1)
    T += text("BOOKKEEPING, NOT DRAWN.", x_l, y_dec - 2.37 * cdec, cdec, 0.1)
    polys, _ = paragraph(KEY, x_l, 222.0, bcap, lead, col_w)
    T += polys

    ccap = sh.cap(2.0)
    T += text("REAL POINTS OF X²+Y²−Z²=1 · |Z| ≤ 2 · ORTHOGRAPHIC", 282.0, 401.0, ccap,
              0.12, align="right")

    for name, x0, y0 in tags:
        T += text(name, x0, y0, tag_cap, 0.05)

    T += text("EVERY CURVE ON IT IS a[A]+b[B]", x_l, 124.0, sh.cap(3.0), 0.12)
    for ci, (cls, name) in enumerate(CELLS):
        x0 = FRAME[0] + ci * CELL_PITCH
        T += text(cls, x0, 51.0, sh.cap(2.4), 0.06)
        T += text(name, x0, 51.0 - 2.78 * sh.cap(1.8), sh.cap(1.8), 0.14)

    # ---- footer: the rebus and the honesty line ------------------------------
    rc = (24.0, 27.0)
    rr = 9.0 - 0.5 * sh.phys(NIB[GREEN])
    L[GREEN].append([(rc[0] + rr * math.cos(t), rc[1] + rr * math.sin(t))
                     for t in np.linspace(0, 2 * math.pi, 145)])
    ecap = sh.cap(6.0)
    xe = 37.0
    T += text("=", xe, 24.0, ecap)
    # the slashes copy the on-sheet slants of the X strings
    slash = 17.0
    xs = xe + text_width("=", ecap) + 3.0
    slants = {}
    for fam in ("A", "B"):
        d = hero.vec(ruling_dirs(fam, ALPHA0, 0.0)[1])
        d = d / math.hypot(*d)
        if d[0] < 0:
            d = -d
        slants[fam] = d
    stats["slant_deg"] = {f: round(math.degrees(math.atan2(v[1], v[0])), 1) for f, v in slants.items()}

    def slash_at(x_left: float, d) -> Tuple[Pt, Pt, float]:
        w, h = abs(d[0]) * slash, abs(d[1]) * slash
        cy = 27.0
        a = (x_left, cy - 0.5 * d[1] * slash)
        b = (x_left + w, cy + 0.5 * d[1] * slash)
        return a, b, w

    a, b, w = slash_at(xs, slants["A"])
    L[BLUE] += offset_passes((a, b), sh.phys(X_PASS_OFF))
    xp = xs + w + 2.5
    T += text("+", xp, 24.0, ecap)
    xg = xp + text_width("+", ecap) + 3.0
    a, b, w = slash_at(xg, slants["B"])
    L[GOLD] += offset_passes((a, b), sh.phys(X_PASS_OFF))

    hcap = sh.cap(2.2)
    T += text("EVERYTHING DRAWN IS A THEOREM (LEFSCHETZ 1924).", 282.0, 28.0, hcap, 0.12,
              align="right")
    T += text("THE OPEN CASES BEGIN IN REAL DIMENSION 8.", 282.0, 28.0 - 2.73 * hcap, hcap, 0.12,
              align="right")
    return L, stats


def _pens(colors: int) -> Dict[int, Optional[int]]:
    if colors >= 4:
        return {GOLD: 0, BLUE: 1, GREEN: 2, TEXT: 3}
    if colors == 3:
        return {GOLD: 0, BLUE: 1, GREEN: 2, TEXT: 1}
    if colors == 2:
        return {GOLD: 0, BLUE: 1, GREEN: 1, TEXT: 1}
    return {GOLD: None, BLUE: None, GREEN: None, TEXT: None}


def hodge_circle_is_two_lines_faithful(
    rng: SeededRNG, bounds, colors: int = 4, roll_deg: float = -30.0
) -> List[GCodeCommand]:
    """Plate 5: the pencil on the string hyperboloid, the (p, q) row, the
    rebus.  Nothing is random; ``rng`` is accepted for the contract only."""
    sh = Sheet(tuple(bounds))
    L, _ = build(sh, math.radians(roll_deg))
    pens = _pens(colors)
    sc = Scene3D(rng, None, feed=F_DRAW, tip=0.2, fit="none")
    for layer in (GOLD, BLUE, GREEN, TEXT):
        lines = []
        for poly in L[layer]:
            pts = [sh.pt(p) for p in poly]
            lines.append([(x, y, 0.0, pens[layer]) for x, y in pts])
            lines.append([(0.0, 0.0, HIDE, pens[layer])])
        # exact emission: every sample kept, runs split only at the HIDE
        # sentinels already bisected into the geometry above
        sc.lines(lines, mode="over")
    return sc.render()


if __name__ == "__main__":  # quick stats
    import json
    import sys

    roll = float(sys.argv[1]) if len(sys.argv) > 1 else -12.0
    _L, st = build(Sheet(FRAME), math.radians(roll))
    print(json.dumps(st, indent=1, default=str))
    for k, v in _L.items():
        print(k, len(v), round(sum(poly_len(p) for p in v) / 1000, 2), "m")
