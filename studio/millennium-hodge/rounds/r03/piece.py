"""HODGE CONJECTURE -- r03, thesis ITERATE (parent r02, abstract).  Plate 5 of
the MILLENNIUM series.

r03 re-seats r02's construction with ONE measured survey of slab + view
(``survey.py`` in this folder): the slab becomes asymmetric, -2 <= z <= 0.8,
viewed at elevation 48 deg, hinge 357 deg.  At that view both index-0 strings
(the X) are visible end to end with no occlusion gap, the waist circle shows
97 % of its length, the far vertex of the 31.72 deg ellipse (where it grazes
the bottom rim) is visible, and the eye is >= 45 mm tall.

A CIRCLE IS TWO STRAIGHT LINES.

Lineage: Naum Gabo, *Linear Construction in Space No. 1* (1942-43, Tate
T00191).  Order taken: a curved surface made ONLY of straight strings, with a
lens-shaped void bounded by the strings' envelopes.  Here the strings are the
algebraic cycles and the void is the see-through throat.  Canon: Constructivism,
Gabo/Pevsner spatial branch -- diagonal thrust and counter-thrust, depth made
only by tensioned straight lines, volume never outlined.

Everything on the sheet is exact:

    surface   the real points of the smooth quadric  x^2 + y^2 - z^2 = 1,
              clipped to the slab ZLO <= z <= ZHI = -2 <= z <= 0.8 (never outlined -- its curvature exists
              only as the envelope of its strings)
    BLUE      family A: A(a, s) = (cos a - s sin a, sin a + s cos a, s)   [A]
    GOLD      family B: B(b, s) = (cos b + s sin b, sin b - s cos b, s)   [B]
              N = 96 per family, index 0 at the hinge p = (cos a0, sin a0, 0)
    GREEN     the pencil of planes through the tangent line l at p,
              z = tan(psi) * (n.P - 1): circle (0), ellipses (15, 31.72 =
              arctan(2)/2 -- the last whole ellipse), parabola (45),
              hyperbolas (60, 75).  Every member has class [A] + [B].
    the X     psi = 90: the tangent plane cuts the surface in exactly the two
              index-0 strings, A(a0) U B(a0) -- one blue + one gold, weighted.

Visibility is EXACT, not a z-buffer: a surface point P is hidden iff the ray
P + t v (t > 0, towards the viewer) meets the quadric again inside the slab.
Because P is on the quadric the second root is closed form,
t* = -2 P.D.v / v.D.v with D = diag(1, 1, -1).  Visibility flips are bisected
to 0.005 mm, so every blue/gold run is ONE straight G1.

Anti-crowding (house law, engine-native): the strings are thinned by the
engine's ``Occupancy`` in HALVING-LOD priority order (index 0, then i = 0 mod
8, 4, 2, 1), pause-and-resume -- a silenced string resumes where space opens.
Cross-family near-parallel pairs (|cos| > 0.93, < 0.8 mm) yield the
later-drawn stretch (``material.suppress_parallel`` semantics with priority).

Design sheet: A3 portrait, mm, y UP, drawable [15, 282] x [15, 405].  The
design is uniformly fitted to ``bounds``; PHYSICAL quantities (0.8 mm floor,
X band offsets, caps >= 1.8 mm) are held in real millimetres on any paper.

Pens / layers, plotted in index order (light -> dark, black last):
    0 GOLD   ochre pigment fineliner 0.2   family B, [B]  (incl. X, rebus)
    1 BLUE   ultramarine fineliner 0.2     family A, [A]  (incl. X, rebus)
    2 GREEN  deep green 0.5                class [A]+[B]: the pencil, rebus circle
    3 TEXT   black 0.3                     type, tags, rebus '=' '+'

Entry point: ``hodge_circle_is_two_lines``.
"""

from __future__ import annotations

import itertools
import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine import Occupancy
from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

# ===========================================================================
# the mathematics
# ===========================================================================
ZLO = -2.0  # bottom rim (the 31.72 deg ellipse grazes it: min z = -tan(2 psi) = -2)
ZHI = 0.8  # top rim, lowered from 2 by the r03 survey (asymmetric slab)
H = ZHI  # legacy name: the X's upper (rim) end
N = 96  # strings per family
DQ = np.array([1.0, 1.0, -1.0])  # the quadric form diag(1, 1, -1)
PSI_DEG = (0.0, 15.0, math.degrees(math.atan(2.0) / 2.0), 45.0, 60.0, 75.0)
PSI_LAST_ELLIPSE = math.degrees(math.atan(2.0) / 2.0)  # 31.717 deg, tan = 1/phi
assert abs(math.tan(math.radians(PSI_LAST_ELLIPSE)) - (math.sqrt(5) - 1) / 2) < 1e-12
# stagger priority, halving over the index 0..5 (+ the X as 6): 0, 4, 2, 1, 3, 5
PENCIL_ORDER = (PSI_DEG[0], PSI_DEG[4], PSI_DEG[2], PSI_DEG[1], PSI_DEG[3], PSI_DEG[5])


def string_A(al: float, s):
    s = np.asarray(s, dtype=float)
    return np.stack(
        [np.cos(al) - s * np.sin(al), np.sin(al) + s * np.cos(al), s], axis=-1
    )


def string_B(be: float, s):
    s = np.asarray(s, dtype=float)
    return np.stack(
        [np.cos(be) + s * np.sin(be), np.sin(be) - s * np.cos(be), s], axis=-1
    )


def on_quadric(P) -> float:
    P = np.asarray(P)
    return float(np.abs((P * P * DQ).sum(-1) - 1.0).max())


# ===========================================================================
# the design sheet (A3 portrait, mm, y up)
# ===========================================================================
SHEET = (15.0, 15.0, 282.0, 405.0)

# ONE view for the whole sheet (house law: one projection basis).
VIEW = dict(
    # chosen by the r03 survey (survey.py, table in NOTES).  e 48 is the
    # lowest allowed elevation (3 deg off the 45 deg degeneracy) and, at every
    # hinge, the elevation with the widest X crossing (the on-sheet angle is a
    # function of hinge and elevation ONLY: 67.6 deg here, 69.2 at most in the
    # 330-360 window).  At hinge 357 with the top rim at 0.8 both index-0
    # strings are visible rim to rim (gap-free up to H_top 0.85), the waist
    # circle shows 97.7 %, the 31.72 deg ellipse's graze vertex is visible
    # through the throat, and blue : gold length is 0.96.
    elev=48.0,
    hinge=357.0,  # alpha0: p on the front flank, 3 deg off the viewer
    # roll -14: the construction leans; the gold X falls at -49 deg as the
    # thrust against the blue's +18 deg counter-thrust (at -20 the blue went
    # flat and the rebus slant read as a minus sign)
    roll=-14.0,
    k=62.0,  # mm per unit (eye 0.731 unit tall -> 45.3 mm)
    cx=184.0,  # shoved against the right frame, which crops the lower lobe;
    cy=210.0,  # the bottom rim stays on the sheet so the graze is seen
)


class View:
    """Orthographic view: viewer at azimuth 0, elevation e; screen roll rho."""

    def __init__(self, elev, hinge, roll, k, cx, cy):
        e = math.radians(elev)
        self.v = np.array([math.cos(e), 0.0, math.sin(e)])
        self.r = np.array([0.0, 1.0, 0.0])
        self.u = np.array([-math.sin(e), 0.0, math.cos(e)])
        self.vDv = float((self.v * DQ) @ self.v)
        assert abs(self.vDv) > 0.1, "elevation too close to 45 deg: strings collapse to points"
        self.a0 = math.radians(hinge)
        self.c, self.s = math.cos(math.radians(roll)), math.sin(math.radians(roll))
        self.k, self.cx, self.cy = k, cx, cy

    def proj(self, P) -> np.ndarray:
        P = np.asarray(P, dtype=float)
        x = P @ self.r
        y = P @ self.u
        return np.stack(
            [self.cx + self.k * (self.c * x - self.s * y), self.cy + self.k * (self.s * x + self.c * y)],
            axis=-1,
        )

    def visible(self, P) -> np.ndarray:
        """Exact: hidden iff the ray towards the viewer re-enters the clipped quadric."""
        P = np.asarray(P, dtype=float)
        t = -2.0 * ((P * DQ) @ self.v) / self.vDv
        Z = P[..., 2] + t * self.v[2]
        return ~((t > 1e-9) & (Z >= ZLO - 1e-12) & (Z <= ZHI + 1e-12))

    def sees_through(self, X, Y) -> np.ndarray:
        """Screen points whose sight-line misses the clipped surface (the eye)."""
        x = ((X - self.cx) * self.c + (Y - self.cy) * self.s) / self.k
        y = (-(X - self.cx) * self.s + (Y - self.cy) * self.c) / self.k
        O = x[..., None] * self.r + y[..., None] * self.u
        a = self.vDv
        b = 2.0 * ((O * DQ) @ self.v)
        cc = (O * O * DQ).sum(-1) - 1.0
        disc = b * b - 4 * a * cc
        sq = np.sqrt(np.maximum(disc, 0.0))
        hit = np.zeros(np.shape(X), bool)
        for sg in (-1.0, 1.0):
            t = (-b + sg * sq) / (2 * a)
            zz = O[..., 2] + t * self.v[2]
            hit |= (disc >= 0) & (zz >= ZLO) & (zz <= ZHI)
        return ~hit

    def in_eye(self, X, Y) -> np.ndarray:
        """The EYE: sight-lines that miss the clipped surface by running
        INSIDE it through both openings (not the paper outside the envelope).
        Such a line is inside the quadric where it crosses z = 0."""
        X, Y = np.asarray(X, float), np.asarray(Y, float)
        x = ((X - self.cx) * self.c + (Y - self.cy) * self.s) / self.k
        y = (-(X - self.cx) * self.s + (Y - self.cy) * self.c) / self.k
        O = x[..., None] * self.r + y[..., None] * self.u
        t = -O[..., 2] / self.v[2]
        Q = O + t[..., None] * self.v
        return self.sees_through(X, Y) & ((Q * Q * DQ).sum(-1) < 1.0)


# ===========================================================================
# design -> sheet transform (paper-agnostic)
# ===========================================================================
class Fit:
    def __init__(self, bounds):
        bx0, by0, bx1, by1 = bounds
        w, h = SHEET[2] - SHEET[0], SHEET[3] - SHEET[1]
        self.k = min((bx1 - bx0) / w, (by1 - by0) / h)
        self.ox = bx0 + ((bx1 - bx0) - w * self.k) / 2.0 - SHEET[0] * self.k
        self.oy = by0 + ((by1 - by0) - h * self.k) / 2.0 - SHEET[1] * self.k

    def pt(self, p: Pt) -> Pt:
        return (self.ox + p[0] * self.k, self.oy + p[1] * self.k)

    def run(self, r: Sequence[Pt]) -> Run:
        return [self.pt(p) for p in r]

    def phys(self, mm: float) -> float:
        """A physical length in mm -> design units."""
        return mm / self.k


# ===========================================================================
# geometry helpers
# ===========================================================================
def in_frame(xy: np.ndarray, pad: float = 0.0) -> np.ndarray:
    x0, y0, x1, y1 = SHEET
    return (
        (xy[..., 0] >= x0 + pad)
        & (xy[..., 0] <= x1 - pad)
        & (xy[..., 1] >= y0 + pad)
        & (xy[..., 1] <= y1 - pad)
    )


def clip_to_frame(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Point where segment a(inside)->b(outside) crosses the frame (exact)."""
    x0, y0, x1, y1 = SHEET
    t_best = 1.0
    d = b - a
    for axis, lo, hi in ((0, x0, x1), (1, y0, y1)):
        if abs(d[axis]) < 1e-15:
            continue
        for edge in (lo, hi):
            t = (edge - a[axis]) / d[axis]
            if 0.0 <= t <= t_best:
                q = a + t * d
                o = 1 - axis
                lo_o, hi_o = (y0, y1) if o == 1 else (x0, x1)
                if lo_o - 1e-9 <= q[o] <= hi_o + 1e-9:
                    t_best = t
    q = a + t_best * d
    # land ON the frame, never a float hair outside it (bounds are strict)
    return np.array([min(max(q[0], x0 + 1e-6), x1 - 1e-6), min(max(q[1], y0 + 1e-6), y1 - 1e-6)])


def in_boxes(xy: np.ndarray, boxes) -> np.ndarray:
    m = np.zeros(xy.shape[:-1], bool)
    for bx0, by0, bx1, by1 in boxes:
        m |= (xy[..., 0] >= bx0) & (xy[..., 0] <= bx1) & (xy[..., 1] >= by0) & (xy[..., 1] <= by1)
    return m


def runs_of(mask: np.ndarray) -> List[Tuple[int, int]]:
    """Inclusive (i0, i1) index spans where mask is True."""
    out, i, n = [], 0, len(mask)
    while i < n:
        if mask[i]:
            j = i
            while j + 1 < n and mask[j + 1]:
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


class DirGrid:
    """Hashed (x, y, tx, ty) samples for the near-parallel yield test."""

    def __init__(self, cell: float):
        self.cell = cell
        self.g: Dict[Tuple[int, int], List[Tuple[float, float, float, float]]] = {}

    def add(self, x, y, tx, ty):
        self.g.setdefault((int(math.floor(x / self.cell)), int(math.floor(y / self.cell))), []).append(
            (x, y, tx, ty)
        )

    def parallel_near(self, x, y, tx, ty, dist: float, align: float) -> bool:
        kx, ky = int(math.floor(x / self.cell)), int(math.floor(y / self.cell))
        d2 = dist * dist
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for qx, qy, ux, uy in self.g.get((kx + dx, ky + dy), ()):
                    if (qx - x) ** 2 + (qy - y) ** 2 < d2 and abs(ux * tx + uy * ty) > align:
                        return True
        return False


# ===========================================================================
# the green pencil (exact rational parametrisation through p)
# ===========================================================================
def pencil_point(view: View, psi: float, th):
    """Point of the conic z = tan(psi)(n.P - 1) on the line through p with
    in-plane direction w(th) = cos th * l + sin th * (cos psi n + sin psi z)."""
    a0 = view.a0
    n = np.array([math.cos(a0), math.sin(a0), 0.0])
    l = np.array([-math.sin(a0), math.cos(a0), 0.0])
    zh = np.array([0.0, 0.0, 1.0])
    th = np.asarray(th, dtype=float)
    w = np.cos(th)[..., None] * l + np.sin(th)[..., None] * (math.cos(psi) * n + math.sin(psi) * zh)
    den = np.cos(th) ** 2 + np.sin(th) ** 2 * math.cos(2 * psi)
    lam = -2.0 * np.sin(th) * math.cos(psi) / den
    return n + lam[..., None] * w


def pencil_member(view: View, psi_deg: float, step_mm: float) -> List[np.ndarray]:
    """The visible, in-frame, inside-|z|<=H pieces of one pencil member, in
    3D (arrays of points), each piece ordered by th.  Ends are exact: rim
    crossings and visibility flips are bisected."""
    psi = math.radians(psi_deg)
    eps = 1e-7
    th = np.linspace(eps, math.pi - eps, 60001)
    P = pencil_point(view, psi, th)
    finite = np.isfinite(P).all(-1)
    zz = np.where(finite, P[:, 2], 99.0)
    inside = finite & (zz >= ZLO) & (zz <= ZHI)

    def ok_at(t):
        Q = pencil_point(view, psi, np.array([t]))[0]
        if not np.isfinite(Q).all() or not (ZLO <= Q[2] <= ZHI):
            return 0
        if not view.visible(Q[None])[0]:
            return 1
        if not in_frame(view.proj(Q[None]))[0]:
            return 2
        return 3

    S = view.proj(np.where(finite[:, None], P, 0.0))
    vis = view.visible(np.where(finite[:, None], P, 0.0))
    good = inside & vis & in_frame(S)
    pieces = []
    for i0, i1 in runs_of(good):
        ts = list(th[i0 : i1 + 1])
        # refine both ends by bisection on the 'good' predicate
        if i0 > 0:
            lo, hi = th[i0 - 1], th[i0]
            for _ in range(50):
                m = 0.5 * (lo + hi)
                if ok_at(m) == 3:
                    hi = m
                else:
                    lo = m
            ts[0] = hi
        if i1 < len(th) - 1:
            lo, hi = th[i1], th[i1 + 1]
            for _ in range(50):
                m = 0.5 * (lo + hi)
                if ok_at(m) == 3:
                    lo = m
                else:
                    hi = m
            ts[-1] = lo
        Pp = pencil_point(view, psi, np.array(ts))
        # decimate to ~step_mm on screen (chord error << 0.3 mm at these radii)
        Sp = view.proj(Pp)
        keep = [0]
        acc = 0.0
        for j in range(1, len(Sp)):
            acc += float(np.hypot(*(Sp[j] - Sp[j - 1])))
            if acc >= step_mm:
                keep.append(j)
                acc = 0.0
        if keep[-1] != len(Sp) - 1:
            keep.append(len(Sp) - 1)
        pieces.append(Pp[keep])
    joined: List[np.ndarray] = []
    for pc in pieces:
        if joined and np.linalg.norm(joined[-1][-1] - pc[0]) < 1e-6:
            joined[-1] = np.vstack([joined[-1], pc[1:]])
        else:
            joined.append(pc)
    return joined


# ===========================================================================
# type: a small setter on the house stroke font
# ===========================================================================
# authored glyphs the house font lacks (same 4 x 6 cell, same stroke logic)
_EXTRA = {
    "?": [
        [(0.7, 4.7), (1.1, 5.6), (2.0, 6.0), (2.9, 5.6), (3.3, 4.7), (3.0, 3.9), (2.0, 3.1), (2.0, 1.8)],
        [(1.7, 0), (2.3, 0), (2.3, 0.5), (1.7, 0.5), (1.7, 0)],
    ],
    # the house comma is a 1.3-unit tick that reads as a full stop at 2.1 mm
    # caps -- which turned h^{2,0} into "h^{2.0}".  A head plus a hooked tail.
    ",": [[(1.7, 0.7), (2.4, 0.7), (2.4, 0.0), (2.1, -0.8), (1.5, -1.4)]],
}


def set_text(txt: str, x: float, y: float, cap: float, track: float = 0.0) -> Tuple[List[Run], float]:
    """Set a line on the house stroke font.  ``^{...}`` sets a superscript
    (0.62 cap, raised 0.52 cap) -- used for the Hodge number h^{2,0}."""
    runs: List[Run] = []
    cx = x
    i, sup = 0, False
    while i < len(txt):
        if txt.startswith("^{", i):
            sup, i = True, i + 2
            continue
        if sup and txt[i] == "}":
            sup, i = False, i + 1
            continue
        ch = txt[i]
        sc = cap / 6.0 * (0.62 if sup else 1.0)
        yo = cap * 0.52 if sup else 0.0
        glyph = _EXTRA.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper())
        assert glyph is not None or ch == " ", f"no glyph for {ch!r}"
        for st in glyph or []:
            runs.append([(cx + gx * sc, y + yo + gy * sc) for gx, gy in st])
        cx += 5.6 * sc + (track * 0.6 if sup else track)
        i += 1
    return runs, (cx - x - track) if txt else 0.0


def text_width(txt: str, cap: float, track: float = 0.0) -> float:
    return set_text(txt, 0.0, 0.0, cap, track)[1]


def fit_lines(lines: Sequence[str], cap: float, track: float, maxw: float) -> List[str]:
    """Keep authored breaks; split a too-wide line into the fewest balanced lines."""
    out: List[str] = []
    for ln in lines:
        if text_width(ln, cap, track) <= maxw:
            out.append(ln)
            continue
        words = ln.split(" ")
        best = None
        for n in (2, 3, 4):
            if n > len(words):
                break
            for cuts in itertools.combinations(range(1, len(words)), n - 1):
                idx = (0,) + cuts + (len(words),)
                parts = [" ".join(words[a:b]) for a, b in zip(idx, idx[1:])]
                mw = max(text_width(q, cap, track) for q in parts)
                if mw <= maxw and (best is None or mw < best[0]):
                    best = (mw, parts)
            if best:
                break
        out += best[1] if best else [ln]
    return out


def weighted(runs: Sequence[Run], off: float) -> List[Run]:
    """Display weight: each stroke as three passes (-off, 0, +off), chained
    out-back-out into one pen-down."""
    out = []
    for r in runs:
        a = _offset_polyline(r, -off)
        c = _offset_polyline(r, off)
        out.append(a + list(r)[::-1] + c)
    return out


# ===========================================================================
# pens
# ===========================================================================
LAYERS = ("gold", "blue", "green", "text")


def _pen_map(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 4:
        return {k: i for i, k in enumerate(LAYERS)}
    if colors == 3:
        return {"gold": 0, "blue": 1, "green": 2, "text": 2}
    if colors == 2:
        return {"gold": 0, "blue": 1, "green": 1, "text": 1}
    return {k: None for k in LAYERS}


# ===========================================================================
# the plate
# ===========================================================================
LAYOUT = dict(
    title_cap=8.5,
    title_base=(391.5, 377.5),
    stmt_cap=2.6,
    stmt_base=365.0,
    colo_cap=2.1,
    colo_w=44.0,  # the left type column (the paper L's vertical arm)
    type_clear=6.0,  # mm of bare paper between any type block and the envelope
    block_gap=10.0,  # mm between stacked type blocks (> 2 leads: blocks read apart)
    small_paper_shrink=0.75,  # k *= grow ** -this when the type floor bites
    cap_w=66.0,
)

STATS: Dict[str, object] = {}

# The X (and the rebus slants that copy it) is the ONE weighted line family:
# seven passes of the 0.2 nib at 0.15 mm -> a ~1.1 mm solid band, the same for
# blue and gold, heavier than the 0.5 green.  Physical mm.
X_HALF = 0.45
X_N = 7
# a string run shorter than this on paper is a crumb, not a line: dropped by
# LOD (A3: no blue/gold fragment under 8 mm anywhere on the sheet).
MIN_RUN = 8.0


def X_PASSES(ph):
    return [ph(-X_HALF + 2 * X_HALF * q / (X_N - 1)) for q in range(X_N)]


def build_layers(fit: Fit, view: View) -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}
    ph = fit.phys
    # same-colour spacing floor 0.8 mm, tested point-to-point on samples every
    # 0.3 mm: 0.88 holds >= 0.8 mm between the segments themselves (0.83 left
    # 0.74 mm residues where two sheets fold over each other at the eye tips)
    floor = ph(0.88)
    step = ph(0.3)  # string sample step on the page
    align = 0.93

    # ---- the X: the two index-0 strings, and their on-sheet directions ----
    a0 = view.a0
    xa = view.proj(string_A(a0, [ZLO, ZHI]))
    xb = view.proj(string_B(a0, [ZLO, ZHI]))
    dir_a = (xa[1] - xa[0]) / np.linalg.norm(xa[1] - xa[0])  # s increasing
    dir_b = (xb[1] - xb[0]) / np.linalg.norm(xb[1] - xb[0])
    p_scr = view.proj(np.array([[math.cos(a0), math.sin(a0), 0.0]]))[0]
    STATS["p"] = tuple(np.round(p_scr, 2))
    STATS["X_angles_deg"] = (
        round(math.degrees(math.atan2(dir_a[1], dir_a[0])), 2),
        round(math.degrees(math.atan2(dir_b[1], dir_b[0])), 2),
    )

    # ---- TEXT boxes that strings must respect (tags only) ------------------
    T: Dict[str, List[Run]] = {k: [] for k in ("colo", "honest", "cap", "tags", "rebus", "stmt", "title")}
    tag_cap = max(2.6, ph(1.8))
    tag_boxes = []
    pad = ph(1.4)
    def tag_box(end, d, w):
        gap = ph(2.2)
        tx = end[0] + d[0] * gap - (w if d[0] < 0 else 0.0)
        ty = end[1] + d[1] * gap - (tag_cap if d[1] < 0 else 0.0)
        tx = min(max(tx, SHEET[0]), SHEET[2] - w)
        return tx, ty

    def box_on_paper(x0, y0, x1, y1) -> bool:
        """Bare paper OUTSIDE the construction: see-through, in frame, and not
        the eye (the eye holds zero ink, tags included)."""
        xs = np.arange(x0 - pad, x1 + pad + 1e-9, ph(0.5))
        ys = np.arange(y0 - pad, y1 + pad + 1e-9, ph(0.5))
        X, Y = np.meshgrid(xs, ys)
        if not (in_frame(np.stack([X, Y], -1)).all() and view.sees_through(X, Y).all()):
            return False
        return not bool(view.in_eye(np.array([x0, x1, x0, x1]), np.array([y0, y0, y1, y1])).any())

    STATS["tags"] = {}
    for lab, xx, d in (("[A]", xa, dir_a), ("[B]", xb, dir_b)):
        # the tag names the string at a RIM end that lies on bare paper: the
        # BOTTOM rim end first (beyond it is the paper outside the envelope,
        # never the eye); the top rim end only if the bottom one is cropped.
        w = text_width(lab, tag_cap)
        choice = None
        for end, dd, nm in ((xx[0], -d, "bottom"), (xx[1], d, "top")):
            if not in_frame(end[None], pad=ph(3.0))[0]:
                continue
            tx, ty = tag_box(end, dd, w)
            if box_on_paper(tx, ty, tx + w, ty + tag_cap):
                choice = (tx, ty, nm)
                break
        if choice is None:  # no bare paper at either end: bottom end, haloed
            end = xx[0] if in_frame(xx[0][None], pad=ph(3.0))[0] else xx[1]
            dd = -d if end is xx[0] else d
            choice = (*tag_box(end, dd, w), "haloed")
        tx, ty, nm = choice
        STATS["tags"][lab] = nm
        T["tags"] += set_text(lab, tx, ty, tag_cap)[0]
        tag_boxes.append((tx - pad, ty - pad, tx + w + pad, ty + tag_cap + pad))

    # ---- GREEN: the pencil through p (computed first: strings yield to it) --
    green_pieces: Dict[float, List[np.ndarray]] = {}
    for psi in PSI_DEG:
        pcs = pencil_member(view, psi, ph(0.5))
        for pc in pcs:
            assert on_quadric(pc) < 1e-12
            # plane residual
            n = np.array([math.cos(a0), math.sin(a0), 0.0])
            res = np.abs(pc[:, 2] - math.tan(math.radians(psi)) * (pc @ n - 1.0)).max()
            assert res < 1e-9, res
        green_pieces[psi] = [view.proj(pc) for pc in pcs]

    # pencil stagger: all members are tangent to l at p.  The circle and the X
    # reach p; every other member stops where its gap to the nearest
    # continuing member falls below floor + nib (0.8 + 0.5 mm).
    thr = ph(0.8 + 0.5)
    reach = ph(40.0)
    cont: List[np.ndarray] = [xa, xb]  # the X strings (2-point segments)

    def seg_dist(q: np.ndarray, poly: np.ndarray) -> float:
        a = poly[:-1]
        b = poly[1:]
        ab = b - a
        t = np.clip(((q - a) * ab).sum(-1) / np.maximum((ab * ab).sum(-1), 1e-18), 0, 1)
        d = a + t[:, None] * ab - q
        return float(np.sqrt((d * d).sum(-1)).min())

    # the same HALVING law as the strings: index the pencil 0..6 by psi (6 =
    # the X, psi = 90).  The X and the circle (0) reach p; then 4 (60 deg),
    # then 2 (31.7), then the odd members.  Each member yields to every member
    # already laid, so the loops merge into p pairwise, like the strings
    # thin toward the envelope.
    def seg_dist_par(q: np.ndarray, tq: np.ndarray, poly: np.ndarray) -> float:
        """Distance to the near-PARALLEL segments of poly only (|cos| > 0.9).
        The stagger is about members running side by side into p; a member
        that merely CROSSES another somewhere is a point, not a flood."""
        a = poly[:-1]
        b = poly[1:]
        ab = b - a
        lab = np.maximum(np.sqrt((ab * ab).sum(-1)), 1e-18)
        cosv = np.abs((ab * tq).sum(-1)) / (lab * max(float(np.hypot(*tq)), 1e-18))
        m = cosv > 0.9
        if not m.any():
            return 1e9
        a, ab = a[m], ab[m]
        t = np.clip(((q - a) * ab).sum(-1) / np.maximum((ab * ab).sum(-1), 1e-18), 0, 1)
        d = a + t[:, None] * ab - q
        return float(np.sqrt((d * d).sum(-1)).min())

    # r03 stagger (S1): ONLY the ends AT p are staggered.  Every other end of
    # every member is left exactly where the geometry puts it (a rim, a true
    # occlusion edge or the frame) -- no green is trimmed anywhere else.
    # Members are laid in ASCENDING psi after the circle; each p-end first
    # takes its natural stop (the last sample within `reach` of p where it
    # runs closer than floor + nib, near-parallel, to the circle, the X or a
    # member already laid); then a backward pass makes the stops STRICTLY
    # DECREASING in psi on each side (a lower-psi member only ever gets
    # shorter -- less ink never breaks the floor), so the loops close onto the
    # X in pencil order: 15 stops farthest from p, 75 nearest.
    green_final: Dict[float, List[np.ndarray]] = {}
    pcs0 = green_pieces[0.0]
    if len(pcs0) >= 2 and np.hypot(*(pcs0[0][0] - p_scr)) < ph(0.05) and np.hypot(
        *(pcs0[-1][-1] - p_scr)
    ) < ph(0.05):
        # the circle is one closed curve cut at p by the parametrisation:
        # re-join its two ends there so p is crossed, not a stroke end.
        pcs0 = [np.vstack([pcs0[-1], pcs0[0][1:]])] + pcs0[1:-1]
    green_final[0.0] = pcs0
    cont += pcs0

    def dist_from_p(seq: np.ndarray) -> np.ndarray:
        return np.hypot(seq[:, 0] - p_scr[0], seq[:, 1] - p_scr[1])

    # p-ends: (psi, piece index, which end: 0 = start, 1 = end, side key)
    natural: Dict[Tuple[float, str], float] = {}
    pend: Dict[Tuple[float, str], Tuple[int, int]] = {}
    for psi in PSI_DEG[1:]:
        pcs = green_pieces[psi]
        for ip, pc in enumerate(pcs):
            for end in (0, 1):
                seq = pc if end == 0 else pc[::-1]
                if np.hypot(*(seq[0] - p_scr)) >= ph(0.05):
                    continue
                # which side of p: the sign of the screen tangent's x at p
                side = "L" if (seq[min(5, len(seq) - 1)][0] - p_scr[0]) < 0 else "R"
                j, walked, jj = 0, 0.0, 0
                while jj < len(seq) - 1 and walked < reach:
                    if min(seg_dist_par(seq[jj], seq[jj + 1] - seq[jj], c) for c in cont) < thr:
                        j = jj + 1
                    walked += float(np.hypot(*(seq[jj + 1] - seq[jj])))
                    jj += 1
                natural[(psi, side)] = float(dist_from_p(seq)[j])
                pend[(psi, side)] = (ip, end)
                cont.append(seq[j:])
    # backward pass: strictly decreasing in psi on each side, in steps of at
    # least 3 mm so the order is legible on paper, not only in the numbers
    stop = dict(natural)
    step_mm = ph(3.0)
    for side in ("L", "R"):
        seq_psi = [q for q in PSI_DEG[1:] if (q, side) in stop]
        for hi, lo in zip(seq_psi[::-1], seq_psi[::-1][1:]):
            stop[(lo, side)] = max(stop[(lo, side)], stop[(hi, side)] + step_mm)
    stops: Dict[float, List[float]] = {}
    for psi in PSI_DEG[1:]:
        out = []
        for ip, pc in enumerate(green_pieces[psi]):
            arr = pc
            for (q, side), (ip2, end) in pend.items():
                if q != psi or ip2 != ip:
                    continue
                seq = arr if end == 0 else arr[::-1]
                dp = dist_from_p(seq)
                far = np.nonzero(dp >= stop[(q, side)])[0]
                j = int(far[0]) if len(far) else len(seq) - 1
                stops.setdefault(psi, []).append((side, round(float(dp[j]) * fit.k, 1)))
                seq = seq[j:]
                arr = seq if end == 0 else seq[::-1]
            if len(arr) >= 2:
                glen = float(np.hypot(*np.diff(arr, axis=0).T).sum())
                if glen > ph(3.0):
                    out.append(arr)
                else:
                    STATS.setdefault("green_dropped_mm", []).append((psi, round(glen * fit.k, 2)))
        green_final[psi] = out
    STATS["pencil_stops_mm"] = stops
    STATS["pencil_stops_natural_mm"] = {f"{q}{sd}": round(v * fit.k, 1) for (q, sd), v in natural.items()}

    ggrid = DirGrid(max(floor, 1e-6))
    for psi in PSI_DEG:
        for pc in green_final[psi]:
            tang = np.gradient(pc, axis=0)
            tl = np.maximum(np.hypot(tang[:, 0], tang[:, 1]), 1e-12)
            for (x, y), (tx, ty) in zip(pc, tang / tl[:, None]):
                ggrid.add(float(x), float(y), float(tx), float(ty))
            L["green"].append([tuple(map(float, q)) for q in pc])
            STATS.setdefault("green_runs", []).append((psi, [tuple(map(float, q)) for q in pc]))
    STATS["green_len_mm"] = round(
        sum(float(np.hypot(*np.diff(np.array(r), axis=0).T).sum()) for r in L["green"]) * fit.k, 1
    )

    # ---- BLUE + GOLD: the strings, halving-LOD priority, exact runs --------
    occ = {"A": Occupancy(floor), "B": Occupancy(floor)}
    dgrid = {"A": DirGrid(floor), "B": DirGrid(floor)}
    order: List[Tuple[str, int]] = [("A", 0), ("B", 0)]
    seen = set(order)
    for mod in (8, 4, 2, 1):
        for i in range(N):
            if i % mod == 0:
                for fam in ("A", "B"):
                    if (fam, i) not in seen:
                        order.append((fam, i))
                        seen.add((fam, i))

    runs_by: Dict[Tuple[str, int], List[Tuple[np.ndarray, np.ndarray]]] = {}
    n_runs_vis = 0
    vis_len = 0.0
    for fam, i in order:
        ang = a0 + 2 * math.pi * i / N
        F = string_A if fam == "A" else string_B
        ends = view.proj(F(ang, [ZLO, ZHI]))
        Ls = float(np.hypot(*(ends[1] - ends[0])))
        n = max(3, int(math.ceil(Ls / step)) + 1)
        s = np.linspace(ZLO, ZHI, n)
        P = F(ang, s)
        S = view.proj(P)
        vis = view.visible(P)
        fr = in_frame(S)
        halo = in_boxes(S, tag_boxes)
        cand = vis & fr & ~halo
        # the raw visible length (before LOD), for the budget
        for i0, i1 in runs_of(vis & fr):
            vis_len += float(np.hypot(*(S[i1] - S[i0])))
        d = (ends[1] - ends[0]) / Ls
        tx, ty = float(d[0]), float(d[1])
        other = "B" if fam == "A" else "A"
        keep = cand.copy()
        gsh = np.zeros(n, bool)
        if i != 0:  # the X claims first and never yields
            for j in np.nonzero(cand)[0]:
                x, y = float(S[j, 0]), float(S[j, 1])
                if occ[fam].crowded(x, y) or dgrid[other].parallel_near(x, y, tx, ty, floor, align):
                    keep[j] = False
                elif ggrid.parallel_near(x, y, tx, ty, floor, align):
                    gsh[j] = True
            # green shadowing cuts only if it lasts over 3 mm
            for g0, g1 in runs_of(gsh):
                if (g1 - g0) * Ls / (n - 1) > ph(3.0):
                    keep[g0 : g1 + 1] = False
        # a pause shorter than 1 mm is a stutter, not relief: bridge it (only
        # LOD pauses -- never a visibility, frame or halo cut)
        for g0, g1 in runs_of(cand & ~keep):
            if g0 > 0 and g1 < n - 1 and keep[g0 - 1] and keep[g1 + 1] and (g1 - g0 + 2) * Ls / (n - 1) < ph(1.0):
                keep[g0 : g1 + 1] = True
        # runs; drop crumbs shorter than 3 mm
        spans = []
        for i0, i1 in runs_of(keep):
            if float(np.hypot(*(S[i1] - S[i0]))) < ph(MIN_RUN):
                continue
            # exact ends: bisect visibility flips / clip at the frame
            def refine(j_in: int, j_out: int) -> np.ndarray:
                if not fr[j_out] and vis[j_out]:
                    return clip_to_frame(S[j_in], S[j_out])
                if not vis[j_out]:
                    lo, hi = s[j_in], s[j_out]
                    for _ in range(40):
                        m = 0.5 * (lo + hi)
                        if view.visible(F(ang, [m]))[0]:
                            lo = m
                        else:
                            hi = m
                    q = view.proj(F(ang, [lo]))[0]
                    if not in_frame(q[None])[0]:
                        return clip_to_frame(S[j_in], q)
                    return q
                return S[j_in]

            a = refine(i0, i0 - 1) if i0 > 0 else S[i0]
            b = refine(i1, i1 + 1) if i1 < n - 1 else S[i1]
            spans.append((a, b))
            for j in range(i0, i1 + 1):
                occ[fam].add(float(S[j, 0]), float(S[j, 1]))
                dgrid[fam].add(float(S[j, 0]), float(S[j, 1]), tx, ty)
            if i == 0:  # register the X band's flanks too
                nx, ny = -ty, tx
                for off in X_PASSES(ph):
                    for j in range(i0, i1 + 1, 2):
                        occ[fam].add(float(S[j, 0] + nx * off), float(S[j, 1] + ny * off))
        runs_by[(fam, i)] = spans
        n_runs_vis += len(spans)
    STATS["visible_string_len_mm_preLOD"] = round(vis_len * fit.k, 1)

    # emit: index order, boustrophedon (i up, i+1 down); the X as 3 passes
    for fam, layer in (("B", "gold"), ("A", "blue")):
        flip = False
        for i in range(N):
            spans = runs_by.get((fam, i), [])
            if not spans:
                continue
            if i == 0:
                d = spans[0][1] - spans[0][0]
                d = d / np.linalg.norm(d)
                nrm = np.array([-d[1], d[0]])
                def into_ink(pt_in, pt_out):
                    """Pull a flank-pass end back until it no longer pokes
                    into the see-through eye (the centre line ends ON it)."""
                    if not view.sees_through(np.array(pt_out[0]), np.array(pt_out[1])):
                        return pt_out
                    lo, hi = np.array(pt_in), np.array(pt_out)
                    for _ in range(30):
                        mid = 0.5 * (lo + hi)
                        if view.sees_through(np.array(mid[0]), np.array(mid[1])):
                            hi = mid
                        else:
                            lo = mid
                    return lo

                for a, b in spans:
                    for q, off in enumerate(X_PASSES(ph)):  # boustrophedon passes
                        a2, b2 = a + nrm * off, b + nrm * off
                        mid = 0.5 * (a2 + b2)
                        a2, b2 = into_ink(mid, a2), into_ink(mid, b2)
                        # a flank pass at a frame crop ends ON the frame too
                        a2 = a2 if in_frame(np.asarray(a2)[None])[0] else clip_to_frame(mid, np.asarray(a2))
                        b2 = b2 if in_frame(np.asarray(b2)[None])[0] else clip_to_frame(mid, np.asarray(b2))
                        seg = [tuple(a2), tuple(b2)]
                        L[layer].append(seg if q % 2 == 0 else seg[::-1])
                continue
            seq = spans[::-1] if flip else spans
            for a, b in seq:
                L[layer].append([tuple(b), tuple(a)] if flip else [tuple(a), tuple(b)])
            flip = not flip

    n_geom = {k: len(L[k]) for k in ("gold", "blue", "green")}  # construction only

    # ---- REBUS: [circle] = [blue slant] + [gold slant] --------------------
    # AS CLASSES: every glyph sits in the same square brackets as the [A]/[B]
    # tags -- [o] = [/] + [\\] is an equality in H^2(Q, Q), not of shapes.
    # Set flush-RIGHT on the frame in the title band; its bracket band runs
    # from the title's lower baseline to its upper cap line.
    tcap = max(LAYOUT["title_cap"], ph(1.8))
    ry = LAYOUT["title_base"][1]
    rh = LAYOUT["title_base"][0] + tcap - ry  # bracket height
    yc = ry + rh / 2.0
    gh = rh * 0.74  # glyph height inside the brackets
    gap = rh * 0.22
    bar = rh * 0.36
    bw = rh * 0.16  # bracket serif
    bi = rh * 0.10  # bracket to glyph
    ow = ph(0.18)

    def slant_geom(d):
        """A stroke parallel to the real X string.  Both slants have the SAME
        length (the two strings are equal cycles), sized so the steeper one
        spans the glyph height; the flatter one sits centred."""
        dx, dy = float(d[0]), float(d[1])
        if dy < 0:
            dx, dy = -dx, -dy
        steep = max(abs(float(dir_a[1])), abs(float(dir_b[1])))
        Ln = gh / steep
        return dx, dy, Ln, abs(dx) * Ln

    ga, gb = slant_geom(dir_a), slant_geom(dir_b)
    brk = 2 * (bw + bi)  # the two brackets' share of a unit's width
    total = (gh + brk) + gap + bar + gap + (ga[3] + brk) + gap + bar + gap + (gb[3] + brk)
    x = SHEET[2] - total - ph(0.2)
    rebus_x0 = x

    def black_bar(x0, y0, x1, y1):
        return weighted([[(x0, y0), (x1, y1)]], ow)

    def bracket(x0, opening: bool):
        """'[' (opening) or ']' as one stroke, weighted like the = and +."""
        y0, y1 = ry, ry + rh
        if opening:
            pts = [(x0 + bw, y0), (x0, y0), (x0, y1), (x0 + bw, y1)]
        else:
            pts = [(x0, y0), (x0 + bw, y0), (x0 + bw, y1), (x0, y1)]
        return weighted([pts], ow)

    def unit(x0, inner_w, draw):
        T["rebus"] += bracket(x0, True)
        draw(x0 + bw + bi)
        T["rebus"] += bracket(x0 + bw + bi + inner_w + bi, False)
        return inner_w + brk

    def circle(xl):
        rr = gh / 2.0
        # green circle, two passes (0.5 nib, 0.35 apart) -> ~0.85 mm band
        for rad in (rr, rr - ph(0.35)):
            L["green"].append(
                [(xl + rr + rad * math.cos(t), yc + rad * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 181)]
            )

    def slant_at(g, layer):
        def draw(xl):
            dx, dy, Ln, w_ = g
            h_ = dy * Ln
            y0 = yc - h_ / 2
            if dx >= 0:
                a, b = (xl, y0), (xl + w_, y0 + h_)
            else:
                a, b = (xl + w_, y0), (xl, y0 + h_)
            ux, uy = (b[0] - a[0]) / Ln, (b[1] - a[1]) / Ln
            nrm = (-uy, ux)
            for q, off in enumerate(X_PASSES(ph)):
                seg = [(a[0] + nrm[0] * off, a[1] + nrm[1] * off), (b[0] + nrm[0] * off, b[1] + nrm[1] * off)]
                L[layer].append(seg if q % 2 == 0 else seg[::-1])
        return draw

    x += unit(x, gh, circle) + gap
    T["rebus"] += black_bar(x, yc + rh * 0.09, x + bar, yc + rh * 0.09)  # '='
    T["rebus"] += black_bar(x, yc - rh * 0.09, x + bar, yc - rh * 0.09)
    x += bar + gap
    x += unit(x, ga[3], slant_at(ga, "blue")) + gap
    T["rebus"] += black_bar(x, yc, x + bar, yc)  # '+'
    T["rebus"] += black_bar(x + bar / 2, yc - bar / 2, x + bar / 2, yc + bar / 2)
    x += bar + gap
    x += unit(x, gb[3], slant_at(gb, "gold"))
    STATS["rebus_box"] = (round(rebus_x0, 1), ry, round(x, 1), ry + rh)
    text_boxes = [(rebus_x0, ry, x, ry + rh)]

    # ---- TEXT ------------------------------------------------------------
    tc = max(LAYOUT["title_cap"], ph(1.8))
    ttr = tc * 0.30
    for word, yb in zip(("HODGE", "CONJECTURE"), LAYOUT["title_base"]):
        # optical flush-left: the weight passes (+-0.18 mm) stay inside the frame
        T["title"] += weighted(set_text(word, SHEET[0] + ph(0.2), yb, tc, track=ttr)[0], ph(0.18))
    sc_ = max(LAYOUT["stmt_cap"], ph(1.8))
    for j, ln in enumerate(("IN COHOMOLOGY A CIRCLE", "IS TWO STRAIGHT LINES.")):
        T["stmt"] += set_text(ln, SHEET[0], LAYOUT["stmt_base"] - j * sc_ * 1.9, sc_, track=sc_ * 0.12)[0]

    # small type: 2.1 mm caps on A3, never under 1.4 mm on small paper (Leo
    # A5).  Authored breaks are KEPT -- the column widens with the cap instead
    # of re-wrapping -- so the three blocks keep their shapes on every paper.
    cc = max(LAYOUT["colo_cap"], ph(1.4))
    grow = cc / LAYOUT["colo_cap"]
    ctr = cc * 0.08
    lead = cc * 1.85
    # The three small blocks are set flush-LEFT on x = 15 (the title's axis)
    # and each drops into the first stretch of bare paper that clears the
    # construction's envelope by TYPE_CLEAR mm -- tested exactly with the
    # see-through predicate, not by eye.  The construction is never punched
    # for type; the type goes where the paper is.
    blocks = {
        "colo": [  # the question: hangs from the statement
            "CLAY PROBLEM:",
            "ON A SMOOTH COMPLEX",
            "PROJECTIVE VARIETY,",
            "IS EVERY RATIONAL",
            "HODGE CLASS A",
            "RATIONAL COMBINATION",
            "OF CLASSES OF",
            "SUBVARIETIES? OPEN.",
        ],
        "cap": [  # the key: what is drawn, then why it is a Hodge case
            "REAL POINTS OF",
            "X²+Y²−Z²=1 IN THE",
            "SLAB −2 ≤ Z ≤ 0.8,",
            "ORTHOGRAPHIC, CUT",
            "BY THE FRAME.",
            "BLUE, GOLD: ITS TWO",
            "FAMILIES OF LINES,",
            "[A] AND [B].",
            "GREEN: THE CURVES",
            "CUT BY PLANES",
            "TURNING ABOUT THE",
            "TANGENT LINE AT THE",
            "CROSSING. EACH ONE,",
            "CIRCLE TO X,",
            "IS [A]+[B].",
            "HERE h^{2,0}=0: EVERY",
            "CLASS IS A HODGE",
            "CLASS, AND ALL ARE",
            "BUILT FROM [A]",
            "AND [B].",
        ],
        "honest": [  # the honesty line: stands on the bottom margin
            "EVERYTHING DRAWN",
            "HERE IS A THEOREM",
            "(LEFSCHETZ 1924).",
            "THE OPEN CASES BEGIN",
            "IN REAL DIMENSION 8",
            "AND CANNOT BE DRAWN.",
        ],
    }
    for blk in blocks.values():
        assert max(text_width(q, cc, ctr) for q in blk) <= LAYOUT["colo_w"] * grow + 1e-6
    clear = ph(LAYOUT["type_clear"])

    def paper_clear(x0, y0, x1, y1) -> bool:
        xs = np.arange(x0 - clear, x1 + clear + 1e-9, ph(0.7))
        ys = np.arange(y0 - clear, y1 + clear + 1e-9, ph(0.7))
        X, Y = np.meshgrid(xs, ys)
        keep = in_frame(np.stack([X, Y], -1))
        return bool(view.sees_through(X[keep], Y[keep]).all())

    def place(lines, y_hi, y_lo, from_top):
        """Top of the first flush-left box in [y_lo, y_hi] that clears."""
        w = max(text_width(q, cc, ctr) for q in lines)
        hgt = cc + lead * (len(lines) - 1)
        tops = np.arange(y_hi, y_lo + hgt - 1e-9, -ph(0.5))
        for top in tops if from_top else tops[::-1]:
            if paper_clear(SHEET[0], top - hgt, SHEET[0] + w, top):
                return float(top), hgt
        raise AssertionError(f"no paper for block {lines[0]!r}")

    stmt_bottom = LAYOUT["stmt_base"] - sc_ * 1.9
    gap = ph(LAYOUT["block_gap"])
    top_q, h_q = place(blocks["colo"], stmt_bottom - gap, SHEET[1], True)
    top_h, h_h = place(blocks["honest"], top_q - h_q - gap, SHEET[1], False)
    # the key centres on the waist notch: the silhouette point (0, -1, 0)
    notch_y = float(view.proj(np.array([[0.0, -1.0, 0.0]]))[0, 1])
    h_k = cc + lead * (len(blocks["cap"]) - 1)
    lo_k, hi_k = top_h + gap, top_q - h_q - gap
    want = min(max(notch_y + h_k / 2, lo_k + h_k), hi_k)
    for dt in np.arange(0.0, hi_k - lo_k, ph(0.5)):
        cand = [t for t in (want + dt, want - dt) if lo_k + h_k <= t <= hi_k]
        hit = [t for t in cand if paper_clear(SHEET[0], t - h_k, SHEET[0] + max(
            text_width(q, cc, ctr) for q in blocks["cap"]), t)]
        if hit:
            top_k = hit[0]
            break
    else:
        raise AssertionError("no paper for the key")
    STATS["type_blocks_top"] = dict(colo=round(top_q, 1), cap=round(top_k, 1), honest=round(top_h, 1))
    for key, top in (("colo", top_q), ("cap", top_k), ("honest", top_h)):
        yb = top - cc
        for ln in blocks[key]:
            T[key] += set_text(ln, SHEET[0], yb, cc, track=ctr)[0]
            yb -= lead

    # clearance audit: construction ink (strings + pencil) vs every type block
    clear = {}
    for k_ in ("colo", "honest", "cap", "rebus", "stmt", "title"):
        pts = np.array([q for r in T[k_] for q in r] or [(0.0, 0.0)])
        bx = (pts[:, 0].min(), pts[:, 1].min(), pts[:, 0].max(), pts[:, 1].max())
        if k_ == "rebus":
            bx = text_boxes[0]
        best = 1e9
        for lay in ("gold", "blue", "green"):
            for r in L[lay][: n_geom[lay]]:
                a_, b_ = np.array(r[0]), np.array(r[-1])
                q = np.array(r) if len(r) > 2 else np.linspace(a_, b_, max(2, int(np.hypot(*(b_ - a_)) / 0.5)))
                dx_ = np.maximum(np.maximum(bx[0] - q[:, 0], q[:, 0] - bx[2]), 0)
                dy_ = np.maximum(np.maximum(bx[1] - q[:, 1], q[:, 1] - bx[3]), 0)
                best = min(best, float(np.hypot(dx_, dy_).min()))
        clear[k_] = round(best * fit.k, 1)
    STATS["type_clearance_mm"] = clear
    # stroke order: bottom-right key -> bottom-left honesty -> tags -> question
    # -> statement -> title -> rebus (a short walk round the sheet)
    for k_ in ("cap", "honest", "tags", "colo", "stmt", "title", "rebus"):
        L["text"] += T[k_]
    return L


def view_for(fit: Fit) -> View:
    """The ONE view, with its footprint (k) shrunk -- never its projection --
    when small paper holds the type at its 1.4 mm floor and the three type
    blocks grow by `grow`.  On A3 grow = 1 and this is VIEW exactly."""
    grow = max(1.0, fit.phys(1.4) / LAYOUT["colo_cap"])
    v = dict(VIEW)
    if grow > 1.0:
        kf = grow ** -LAYOUT["small_paper_shrink"]
        v["k"] = VIEW["k"] * kf
        # shrink about the BOTTOM-RIGHT frame corner: the construction keeps
        # its crop at the right and bottom frames and the paper L (top band +
        # left type column) widens by exactly what the grown type needs
        v["cx"] = SHEET[2] + (VIEW["cx"] - SHEET[2]) * kf
        v["cy"] = SHEET[1] + (VIEW["cy"] - SHEET[1]) * kf
    return View(**v)


def hodge_circle_is_two_lines(rng: SeededRNG, bounds, colors: int = 4) -> List[GCodeCommand]:
    """A CIRCLE IS TWO STRAIGHT LINES: the pencil on the string hyperboloid.

    Deterministic: the plate is exact mathematics; ``rng`` is accepted for the
    contract and deliberately unused (nothing on the sheet is random).
    """
    _ = rng
    fit = Fit(bounds)
    view = view_for(fit)
    STATS.clear()
    L = build_layers(fit, view)
    pens = _pen_map(colors)
    out: List[GCodeCommand] = []
    for layer in LAYERS:
        f = 2200
        for r in L[layer]:
            out += _poly(fit.run(r), color=pens[layer], f=f)
    return out
