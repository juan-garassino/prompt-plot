"""CNN — FORWARD AND BACKWARD, r02: TRUE MECHANISM.

Two registers of the same pipeline, column-registered: activations left-to-right
on top, gradients right-to-left underneath.  The variant's thesis is literalism —
**every field on this sheet is a real computed array**, not a texture that looks
like one.  ``net.py`` runs one honest forward pass and one honest backward pass
of a small CNN in numpy (verified against central differences to ~1e-9 relative
error, see NOTES.md); this module does nothing but *draw those arrays*.

    forward   X -> W1 -> A1 -> R1 = max(0,A1) -> P1 (2x2 max) -> A2 -> P2 -> z -> p
    backward  dz = p - y -> dWc -> dP2 -> unpool -> dA2 -> dP1 -> unpool -> dA1 -> dW1 -> dX

What each mark carries:

* input plate      dot RADIUS = |X| (Ben-Day: radius is a magnitude), sign by
                   filled/open.  The rings are the chirp's real wavefronts.
* kernel planes    marching-squares isolines of the real 5x5 Gabor filters.
* feature planes   isolines of the real A1; the heavy closed curve is the exact
                   iso-0 — the ReLU frontier.
* ReLU planes      isolines of R1 = max(0, A1).  Where the pass zeroed, the
                   plane is BARE PAPER.  51.1% of it is.
* pooling planes   one mark per pooled cell, radius = P1 value, on the coarse
                   10x10 lattice — visibly half the forward resolution.
* deeper planes    six planes of A2 at 8x8; more channels, less space.
* classifier bar   32 rows of ticks, length = mean |Wc| over 3 rows of Wc.
* softmax column   circle AREA = p_k, so the whole column's ink area is
                   conserved at 1 — normalisation drawn, not asserted.
* unpool plane     the real dR1 scatter: one cell per 2x2 window, 368/1600.
* mask plane       the same scatter after dA1 = dR1 * M1, inside the real
                   iso-0 outline of A1 (the SAME curve as the forward twin).
* gradient tiles   hatch DUTY = |dWc| column norm, hatch ANGLE = sign of dz.

The twist: the pass drawn here is one the network gets WRONG.  The top register
is the answer it gives (class 0, p = 0.533); the bottom register is the sheet
telling it the answer was class 5.  Backprop only exists because of the gap
between the two, so the plate draws the case where it does something.

Pens (``colors=3``): 0 black structure/type/furniture, 1 dodgerblue the
highlighted forward channel, 2 crimson the whole backward register.

Entry point: ``cnn_passes``.
"""

from __future__ import annotations

import math
from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import (
    _offset_polyline,
    circle,
    fill_disc,
    giant_type,
    plus_mark,
)
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

# the piece is loaded BY PATH (importlib.spec_from_file_location), so its own
# directory is not on sys.path and the sibling numerics module would not import.
import os as _os
import sys as _sys

_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)

from net import build as build_net  # noqa: E402  (sibling module, loaded by path)

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, BLUE, RED = 0, 1, 2

F_DRAW = 2000
MIN_PITCH = 0.95          # mm — contour ring floor
INSET = 3.0

# ---------------------------------------------------------------------------
# layout — v measured DOWNWARD from the frame top, u rightward from frame left
# ---------------------------------------------------------------------------
LAB_CAP = 2.45
SHAPE_CAP = 2.05
SIDE_CAP = 2.5

FWD_LAB_V = (5.4, 9.9)
FWD_TOP, FWD_BOT = 16.0, 95.0
FWD_AXIS = 0.5 * (FWD_TOP + FWD_BOT)
FWD_SHAPE_V = (102.5, 107.9)

SWATCH_V = (113.0, 125.0)
SWATCH_CAP_V = 130.0

MID_RULE_V = 139.5

BWD_LAB_V = (145.0, 149.2)
BWD_TOP, BWD_BOT = 153.5, 214.5
BWD_AXIS = 0.5 * (BWD_TOP + BWD_BOT)
BWD_SHAPE_V = 222.0

GSWATCH_V = (219.0, 230.0)
GSWATCH_CAP_V = 235.0

LEG_RULE_V = 241.0
LEG_TOP, LEG_BOT = 245.0, 269.0

# column centres (u, mm from frame left)
U_SPINE = 7.0             # right edge of the giant vertical register names
U_PLATE = 27.5
U_C1 = 78.0
U_C2 = 135.5
U_C3 = 192.5
U_C4 = 246.5
U_ELL = 277.0
U_C5 = 308.0
U_BAR = 344.0
U_SOFT = 368.0

KU = 0.20                 # plane shear: the bottom edge rises to the right


# ===========================================================================
# frame
# ===========================================================================
class Frame:
    def __init__(self, bounds: Bounds, inset: float = INSET):
        x0, y0, x1, y1 = bounds
        self.x0, self.y0 = x0 + inset, y0 + inset
        self.x1, self.y1 = x1 - inset, y1 - inset
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0
        self.sx = self.w / 394.0
        self.sy = self.h / 271.0

    def u(self, u: float) -> float:
        return self.x0 + u * self.sx

    def v(self, v: float) -> float:
        return self.y1 - v * self.sy

    def p(self, u: float, v: float) -> Pt:
        return (self.u(u), self.v(v))

    def du(self, d: float) -> float:
        return d * self.sx

    def dv(self, d: float) -> float:
        return d * self.sy


# ===========================================================================
# type
# ===========================================================================
def _text(text: str, x: float, baseline: float, cap: float, pen: Optional[int],
          align: str = "left") -> List[GCodeCommand]:
    w = _text_width(text, cap, proportional=True)
    if align == "centre":
        x -= w / 2.0
    elif align == "right":
        x -= w
    return _stroke_text(text, x, baseline, cap, color=pen, f=2300, proportional=True)


def _tw(text: str, cap: float) -> float:
    return _text_width(text, cap, proportional=True)


# ===========================================================================
# planes — a parallelogram with vertical sides and a sheared bottom edge
# ===========================================================================
class Plane:
    """A parallelogram: origin + a*U + b*V.

    Deliberately NOT a dataclass: render_candidate loads the piece with
    ``spec_from_file_location`` and never registers it in ``sys.modules``, and
    ``@dataclass`` resolves its annotations through ``sys.modules[cls.__module__]``
    — which is ``None`` here and raises at import time.
    """

    __slots__ = ("ox", "oy", "ux", "uy", "vx", "vy")

    def __init__(self, ox, oy, ux, uy, vx, vy):
        self.ox, self.oy = ox, oy
        self.ux, self.uy = ux, uy
        self.vx, self.vy = vx, vy

    def pt(self, a: float, b: float) -> Pt:
        return (self.ox + a * self.ux + b * self.vx,
                self.oy + a * self.uy + b * self.vy)

    def quad(self) -> Poly:
        return [self.pt(0, 0), self.pt(1, 0), self.pt(1, 1), self.pt(0, 1), self.pt(0, 0)]

    def inside(self, p: Pt, pad: float = 0.0) -> bool:
        """Solve p = o + a*U + b*V for (a, b) — exact for a parallelogram."""
        dx, dy = p[0] - self.ox, p[1] - self.oy
        det = self.ux * self.vy - self.uy * self.vx
        if abs(det) < 1e-12:
            return False
        a = (dx * self.vy - dy * self.vx) / det
        b = (self.ux * dy - self.uy * dx) / det
        return -pad <= a <= 1 + pad and -pad <= b <= 1 + pad


def make_stack(frame: Frame, u_centre: float, v_axis: float, n: int,
               w: float, h: float, dx: float, dy: float) -> List[Plane]:
    """``n`` planes marching up-and-right; index 0 is the FRONT (lower-left)."""
    bw = w + (n - 1) * dx
    bh = h + w * KU + (n - 1) * dy
    u0 = u_centre - bw / 2.0
    v0 = v_axis + bh / 2.0            # bottom of the bbox, in v-down coords
    planes: List[Plane] = []
    for k in range(n):
        ox, oy = frame.p(u0 + k * dx, v0 - k * dy)
        planes.append(Plane(ox, oy,
                            frame.du(w), frame.dv(w * KU),
                            0.0, frame.dv(h)))
    return planes


def _occluder(front: Sequence[Plane]) -> Callable[[Pt], bool]:
    """keep(p) — true when p is NOT hidden by any nearer plane."""
    def keep(p: Pt) -> bool:
        for pl in front:
            if pl.inside(p, pad=0.004):
                return False
        return True
    return keep


# ===========================================================================
# clipping (bisected cuts — same technique as kit._clip_runs)
# ===========================================================================
def _cut(inside: Pt, outside: Pt, keep, iters: int = 12) -> Pt:
    a, b = inside, outside
    for _ in range(iters):
        m = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        if keep(m):
            a = m
        else:
            b = m
    return a


def clip_runs(runs: Sequence[Poly], keep) -> List[Poly]:
    out: List[Poly] = []
    for pts in runs:
        cur: Poly = []
        for i, p in enumerate(pts):
            if i == 0:
                if keep(p):
                    cur.append(p)
                continue
            a = pts[i - 1]
            ka, kb = keep(a), keep(p)
            if ka and kb:
                if not cur:
                    cur = [a]
                cur.append(p)
            elif ka and not kb:
                if not cur:
                    cur = [a]
                cur.append(_cut(a, p, keep))
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
            elif kb and not ka:
                cur = [_cut(p, a, keep), p]
        if len(cur) >= 2:
            out.append(cur)
    return out


def _band(runs: Sequence[Poly], w: float = 0.34) -> List[Poly]:
    """Two passes either side of the centreline — a line with real weight."""
    out: List[Poly] = []
    for r in runs:
        if len(r) < 3:
            out.append(r)
            continue
        out.append(_offset_polyline(r, -w / 2.0))
        out.append(_offset_polyline(r, +w / 2.0))
    return out


def emit(runs: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for r in runs:
        out += _poly(r, color=pen, f=f)
    return out


# ===========================================================================
# marching squares (vectorised case selection, chained with the house helper)
# ===========================================================================
_MS = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),),
    5: ((3, 2), (0, 1)), 6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),),
    9: ((0, 2),), 10: ((0, 3), (1, 2)), 11: ((1, 2),), 12: ((1, 3),),
    13: ((0, 1),), 14: ((0, 3),),
}


def iso_chains(F: np.ndarray, iso: float) -> List[Poly]:
    """Iso-contour of F[j, i] in UNIT coordinates a = i/(nx-1), b = j/(ny-1)."""
    ny, nx = F.shape
    if nx < 2 or ny < 2:
        return []
    v0, v1 = F[:-1, :-1], F[:-1, 1:]
    v2, v3 = F[1:, 1:], F[1:, :-1]
    case = ((v0 > iso).astype(np.uint8) | ((v1 > iso).astype(np.uint8) << 1)
            | ((v2 > iso).astype(np.uint8) << 2) | ((v3 > iso).astype(np.uint8) << 3))
    jj, ii = np.nonzero((case != 0) & (case != 15))
    if len(jj) == 0:
        return []
    ax, ay = 1.0 / (nx - 1), 1.0 / (ny - 1)
    segs = []
    for j, i in zip(jj.tolist(), ii.tolist()):
        xa, xb = i * ax, (i + 1) * ax
        ya, yb = j * ay, (j + 1) * ay
        a, b, c, d = float(v0[j, i]), float(v1[j, i]), float(v2[j, i]), float(v3[j, i])

        def lp(pa, pb, va, vb):
            t = (iso - va) / (vb - va) if vb != va else 0.5
            return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))

        e = (lp((xa, ya), (xb, ya), a, b), lp((xb, ya), (xb, yb), b, c),
             lp((xb, yb), (xa, yb), c, d), lp((xa, yb), (xa, ya), d, a))
        for p, q in _MS[int(case[j, i])]:
            segs.append((e[p], e[q]))
    return [list(ch) for ch in _chain_segments(segs, tol=1e-4)]


def upsample(A: np.ndarray, factor: int, smooth: int = 1) -> np.ndarray:
    """Smooth display upsample (bilinear + one box pass). Values unchanged at
    the original samples up to the smoothing — this is a DISPLAY resample of
    the real array, exactly what any contour plot does."""
    ny, nx = A.shape
    ys = np.linspace(0, ny - 1, (ny - 1) * factor + 1)
    xs = np.linspace(0, nx - 1, (nx - 1) * factor + 1)
    j0 = np.clip(np.floor(ys).astype(int), 0, ny - 2)
    i0 = np.clip(np.floor(xs).astype(int), 0, nx - 2)
    fy = (ys - j0)[:, None]
    fx = (xs - i0)[None, :]
    sy = fy * fy * (3 - 2 * fy)
    sx = fx * fx * (3 - 2 * fx)
    a00 = A[np.ix_(j0, i0)]
    a10 = A[np.ix_(j0, i0 + 1)]
    a01 = A[np.ix_(j0 + 1, i0)]
    a11 = A[np.ix_(j0 + 1, i0 + 1)]
    out = (a00 * (1 - sx) + a10 * sx) * (1 - sy) + (a01 * (1 - sx) + a11 * sx) * sy
    for _ in range(max(1, smooth)):
        pad = np.pad(out, 1, mode="edge")
        sm = np.zeros_like(out)
        for a in range(3):
            for b in range(3):
                sm += pad[a:a + out.shape[0], b:b + out.shape[1]] / 9.0
        out = sm
    return out


def even_levels(F: np.ndarray, pitch_mm: float, cell_mm: float,
                quantile: float = 0.82, n_max: int = 46) -> List[float]:
    """Levels stepped by ``pitch * quantile(|grad F|)`` so rings sit a FIXED
    distance apart wherever they run (DESIGN_RUBRIC: contour levels by
    gradient, never by value)."""
    gy, gx = np.gradient(F, cell_mm)
    g = np.hypot(gx, gy).ravel()
    g = g[np.isfinite(g)]
    if g.size == 0:
        return []
    q = float(np.quantile(g, quantile))
    step = pitch_mm * q
    if step <= 1e-12:
        return []
    lo, hi = float(F.min()), float(F.max())
    n = min(n_max, max(1, int((hi - lo) / step)))
    return [lo + step * (k + 0.5) for k in range(n)]


def plane_contours(F: np.ndarray, plane: Plane, pitch: float, pen: Optional[int],
                   keep, up: int = 4, zero: bool = False,
                   zero_pen: Optional[int] = None,
                   positive_only: bool = False, smooth: int = 1) -> List[GCodeCommand]:
    """Contour a real array inside a plane. ``zero`` adds the exact iso-0."""
    G = upsample(F, up, smooth=smooth)
    w_mm = math.hypot(plane.ux, plane.uy)
    cell = w_mm / max(1, G.shape[1] - 1)
    out: List[GCodeCommand] = []
    levels = even_levels(G, pitch, cell)
    if positive_only:
        levels = [L for L in levels if L > 1e-9]
    for L in levels:
        runs = [[plane.pt(a, b) for a, b in ch] for ch in iso_chains(G, L)]
        out += emit(clip_runs(runs, keep), pen)
    if zero:
        runs = [[plane.pt(a, b) for a, b in ch] for ch in iso_chains(G, 0.0)]
        out += emit(clip_runs(runs, keep), zero_pen if zero_pen is not None else pen)
    return out


# ===========================================================================
# marks
# ===========================================================================
def mark(x: float, y: float, r: float, pen: Optional[int], filled: bool) -> List[GCodeCommand]:
    """A magnitude mark: radius carries |value|, filled/open carries the sign."""
    if r < 0.14:
        return []
    if filled:
        out = _dot(x, y, r=r, color=pen)
        if r > 0.45:
            out += _dot(x, y + 0.34, r=r * 0.8, color=pen)
            out += _dot(x, y - 0.34, r=r * 0.8, color=pen)
        return out
    return circle(x, y, max(r, 0.32), pen=pen, f=F_DRAW, n=9)


def plane_marks(F: np.ndarray, plane: Plane, pen: Optional[int], keep,
                r_max: float, scale: Optional[float] = None,
                thresh: float = 0.04, signed: bool = True,
                only_nonzero: bool = False) -> List[GCodeCommand]:
    """One mark per array cell: radius = |value|, filled = positive."""
    ny, nx = F.shape
    m = scale if scale is not None else float(np.abs(F).max())
    if m <= 0:
        return []
    out: List[GCodeCommand] = []
    for j in range(ny):
        for i in range(nx):
            v = float(F[j, i])
            if only_nonzero and v == 0.0:
                continue
            t = abs(v) / m
            if t < thresh:
                continue
            p = plane.pt((i + 0.5) / nx, 1.0 - (j + 0.5) / ny)
            if not keep(p):
                continue
            out += mark(p[0], p[1], r_max * math.sqrt(t), pen, (v >= 0) or not signed)
    return out


# ===========================================================================
# bundles — dotted flow curves whose DASH DUTY is a real magnitude
# ===========================================================================
def bundle(p0: Pt, p1: Pt, waist: Pt, duty: float, pen: Optional[int],
           n: int = 52, period: float = 1.75) -> List[GCodeCommand]:
    """One quadratic-Bezier flow line, dashed at ``duty`` (0..1) on-fraction.

    The dash period is short and the duty is capped well below 1 on purpose:
    a fan of 24 SOLID curves through a shared neck reads as a scribble, while
    the same 24 dotted curves read as a bundle — which is also what the
    reference plate does.
    """
    duty = max(0.06, min(0.58, duty))
    pts = []
    for k in range(n + 1):
        t = k / n
        it = 1 - t
        pts.append((it * it * p0[0] + 2 * it * t * waist[0] + t * t * p1[0],
                    it * it * p0[1] + 2 * it * t * waist[1] + t * t * p1[1]))
    out: List[GCodeCommand] = []
    run: Poly = []
    s = 0.0
    for k in range(len(pts)):
        if k:
            s += math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1])
        on = (s % period) < period * duty
        if on:
            run.append(pts[k])
        else:
            if len(run) >= 2:
                out += _poly(run, color=pen, f=F_DRAW)
            run = []
    if len(run) >= 2:
        out += _poly(run, color=pen, f=F_DRAW)
    return out


def fan(frame: Frame, u0: float, v_src: Sequence[float], u1: float,
        v_dst: Sequence[float], weights: np.ndarray, pen_of, waist_v: float,
        pinch: float = 0.30) -> List[GCodeCommand]:
    """A weighted bipartite bundle: one dashed curve per (src, dst) pair, its
    dash duty proportional to the real coupling weight between them.

    Each pair gets its OWN waist, pulled ``pinch`` of the way to the register
    axis, so the family converges into a shared neck without every curve
    crossing at one point — a single shared waist turned the 4x6 coupling
    between pooling and the deeper stack into an unreadable knot.
    """
    W = np.abs(np.asarray(weights, float))
    m = W.max() if W.size and W.max() > 0 else 1.0
    uw = 0.5 * (u0 + u1)
    out: List[GCodeCommand] = []
    for si, vs in enumerate(v_src):
        for di, vd in enumerate(v_dst):
            duty = 0.58 * float(W[si, di] / m) ** 0.55
            if duty < 0.105:
                continue
            mid = 0.5 * (vs + vd)
            wv = waist_v + (mid - waist_v) * pinch
            out += bundle(frame.p(u0, vs), frame.p(u1, vd), frame.p(uw, wv),
                          duty, pen_of(si, di))
    return out


def channel_fan(fr: Frame, planes_src: Sequence[Plane], planes_dst: Sequence[Plane],
                profiles: Sequence[np.ndarray], pen_of, axis: float,
                strands: int = 5, pinch: float = 0.30,
                rightward: bool = True) -> List[GCodeCommand]:
    """One bundle PER CHANNEL, each a sheaf of ``strands`` dotted curves.

    A channel is a whole feature MAP, not a point, so a single curve per
    channel under-draws the transport and the register's flow disappears.
    Each strand leaves its plane at a different height and its dash duty is
    that band's real row-energy in the channel's array — the bundle is a
    readout of where in the map the signal actually lives.
    """
    # The bundle must LEAVE the far side of its source stack and ENTER the
    # near side of its destination, so a right-to-left (backward) sheaf reads
    # its sides mirrored. Getting this wrong drew the strands straight THROUGH
    # both stacks as solid bars.
    a_side, b_side = (1.0, 0.0) if rightward else (0.0, 1.0)
    sgn = 1.0 if rightward else -1.0
    u_src = (max if rightward else min)(pl.pt(a_side, 0.5)[0] for pl in planes_src)
    u_dst = (min if rightward else max)(pl.pt(b_side, 0.5)[0] for pl in planes_dst)
    u0 = (u_src - fr.x0) / fr.sx + 1.2 * sgn
    u1 = (u_dst - fr.x0) / fr.sx - 1.2 * sgn
    uw = 0.5 * (u0 + u1)
    out: List[GCodeCommand] = []
    for c, (ps, pd) in enumerate(zip(planes_src, planes_dst)):
        prof = np.asarray(profiles[c], float)
        m = float(prof.max()) or 1.0
        for k in range(strands):
            t = (k + 0.5) / strands
            band = prof[int(t * len(prof))]
            duty = 0.58 * (float(band) / m) ** 0.55
            if duty < 0.09:
                continue
            vs = (fr.y1 - ps.pt(a_side, t)[1]) / fr.sy
            vd = (fr.y1 - pd.pt(b_side, t)[1]) / fr.sy
            wv = axis + (0.5 * (vs + vd) - axis) * pinch
            out += bundle(fr.p(u0, vs), fr.p(u1, vd), fr.p(uw, wv), duty, pen_of(c, k))
    return out


def arrow(frame: Frame, u0: float, u1: float, v: float, pen: Optional[int],
          head: float = 3.2) -> List[GCodeCommand]:
    a, b = frame.p(u0, v), frame.p(u1, v)
    d = 1.0 if u1 > u0 else -1.0
    hx = frame.du(head) * d
    hy = frame.dv(head * 0.42)
    return (_poly([a, b], color=pen, f=F_DRAW)
            + _poly([(b[0] - hx, b[1] + hy), b, (b[0] - hx, b[1] - hy)], color=pen, f=F_DRAW))


def hatch_tile(frame: Frame, u0: float, v0: float, u1: float, v1: float,
               duty: float, angle: float, pen: Optional[int],
               spacing: float = 1.15) -> List[GCodeCommand]:
    """A square whose hatch DUTY is a magnitude and whose ANGLE is a sign."""
    out: List[GCodeCommand] = []
    box = [frame.p(u0, v0), frame.p(u1, v0), frame.p(u1, v1), frame.p(u0, v1), frame.p(u0, v0)]
    out += _poly(box, color=pen, f=F_DRAW)
    w, h = u1 - u0, v1 - v0
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    diag = math.hypot(w, h)
    n = max(1, int(diag / spacing))
    cu, cv = (u0 + u1) / 2.0, (v0 + v1) / 2.0
    keep = lambda p: (u0 <= p[0] <= u1 and v0 <= p[1] <= v1)  # noqa: E731
    for k in range(-n, n + 1):
        off = k * spacing
        seg = []
        steps = 26
        for m in range(steps + 1):
            t = -diag / 2 + diag * m / steps
            pu = cu + t * ca - off * sa
            pv = cv + t * sa + off * ca
            inside = keep((pu, pv))
            on = inside and ((m % 5) / 5.0) < duty
            if on:
                seg.append(frame.p(pu, pv))
            else:
                if len(seg) >= 2:
                    out += _poly(seg, color=pen, f=F_DRAW)
                seg = []
        if len(seg) >= 2:
            out += _poly(seg, color=pen, f=F_DRAW)
    return out


# ===========================================================================
# THE PLATE
# ===========================================================================
def cnn_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    fr = Frame(bounds)
    net = build_net(rng.seed if hasattr(rng, "seed") else 7)
    blk = BLACK if colors > 1 else None
    blu = (BLUE % colors) if colors > 1 else None
    red = (RED % colors) if colors > 1 else None

    X, W1, A1, R1, P1 = net["X"], net["W1"], net["A1"], net["R1"], net["P1"]
    A2, P2, Wc, p = net["A2"], net["P2"], net["Wc"], net["p"]
    dX, dW1, dA1, dR1, dP1 = net["dX"], net["dW1"], net["dA1"], net["dR1"], net["dP1"]
    dA2, dWc, dz = net["dA2"], net["dWc"], net["dz"]
    W2, dW2 = net["W2"], net["dW2"]
    win, target = net["win"], net["target"]
    C1n, C2n, K = A1.shape[0], A2.shape[0], p.size

    # the highlighted forward channel = the one carrying the most activation
    hot = int(np.argmax(np.abs(A1).sum(axis=(1, 2))))

    out: List[GCodeCommand] = []

    # ---------------------------------------------------------------- stacks
    fwd_specs = [
        (U_C1, C1n, 26.0, 30.0, 4.6, 6.2),
        (U_C2, C1n, 28.0, 31.0, 5.0, 6.5),
        (U_C3, C1n, 27.0, 30.0, 4.8, 6.3),
        (U_C4, C1n, 23.0, 26.0, 4.2, 5.6),
        (U_C5, C2n, 18.0, 20.0, 3.4, 4.6),
    ]
    # Every gradient twin is the SAME SIZE as its forward stage, on the same
    # column centre. "Column registration is the whole idea" (BRIEF): with the
    # backward stacks shrunk to 86% the twin curves were no longer congruent
    # and the reader had to take the registration on trust. They are congruent
    # now — the ReLU frontier at column 3 is literally the same curve, drawn
    # once in black above and once in crimson below.
    F = [make_stack(fr, u, FWD_AXIS, n, w, h, dx, dy) for u, n, w, h, dx, dy in fwd_specs]
    B = [make_stack(fr, u, BWD_AXIS, n, w, h, dx, dy) for u, n, w, h, dx, dy in fwd_specs]

    def draw_stack(planes, arrays, pitch, pen_of, *, mode="contour", zero=False,
                   r_max=0.7, positive_only=False, only_nonzero=False,
                   scale=None, border=True, thresh=0.05, smooth=1):
        """Front-to-back with true occlusion: each plane is clipped out of the
        union of every NEARER plane's quad."""
        cmds: List[GCodeCommand] = []
        for k, pl in enumerate(planes):
            keep = _occluder(planes[:k])
            pen = pen_of(k)
            if border:
                cmds += emit(clip_runs([pl.quad()], keep), blk)
            A = arrays[k]
            if mode == "contour":
                cmds += plane_contours(A, pl, pitch, pen, keep, zero=zero,
                                       zero_pen=pen, positive_only=positive_only,
                                       smooth=smooth)
            else:
                cmds += plane_marks(A, pl, pen, keep, r_max, scale=scale,
                                    thresh=thresh, only_nonzero=only_nonzero)
        return cmds

    # order channels so the highlighted one is FRONT
    def chan_order(n, hot_):
        return [hot_] + [c for c in range(n) if c != hot_]

    ordF = chan_order(C1n, hot)
    ordD = list(range(C2n))

    pen_hot = lambda k: blu if k == 0 else blk       # noqa: E731  front = hot
    pen_all_blk = lambda k: blk                      # noqa: E731
    pen_red = lambda k: red                          # noqa: E731
    pen_red_hot = lambda k: red if k == 0 else blk   # noqa: E731

    # --- col 1 forward: the real Gabor kernels ---------------------------
    out += draw_stack(F[0], [W1[c] for c in ordF], 1.35, pen_hot, zero=True)
    # --- col 2 forward: A1 with its exact iso-0 (the ReLU frontier) ------
    out += draw_stack(F[1], [A1[c] for c in ordF], 1.25, pen_hot, zero=True)
    # --- col 3 forward: R1 — dead regions are BARE PAPER -----------------
    out += draw_stack(F[2], [R1[c] for c in ordF], 1.25, pen_all_blk,
                      positive_only=True)
    # THE MASK FRONTIER — the exact iso-0 of A1.  It is drawn as a two-pass
    # band here AND, identically, in the backward twin directly below, so the
    # same curve appears once in each register on the same column.  That
    # correspondence is the plate's argument.
    for k, pl in enumerate(F[2]):
        keep = _occluder(F[2][:k])
        G = upsample(A1[ordF[k]], 4)
        runs = [[pl.pt(a, b) for a, b in ch] for ch in iso_chains(G, 0.0)]
        out += emit(_band(clip_runs(runs, keep)), blu if k == 0 else blk)
    # --- col 4 forward: P1 on the coarse 10x10 lattice -------------------
    out += draw_stack(F[3], [P1[c] for c in ordF], 0.0, pen_hot, mode="marks",
                      r_max=0.78, scale=float(P1.max()), thresh=0.03)
    # --- col 5 forward: A2 — fewer, smoother forms (the abstraction story)
    out += draw_stack(F[4], [A2[c] for c in ordD], 1.45, pen_all_blk, zero=True)

    # --- col 1 backward: the real filter gradients -----------------------
    out += draw_stack(B[0], [dW1[c] for c in ordF], 2.2, pen_red, zero=True)
    # --- col 2 backward: the same dA1 as a CONTOURED field.  Same display
    # resample as every other contoured plane on the sheet (upsample + box
    # smooth), so what the isolines enclose is where the real gradient is.
    out += draw_stack(B[1], [dA1[c] for c in ordF], 2.1, pen_red, smooth=4)
    # --- col 3 backward: THE MASK — same iso-0 curve as the forward twin -
    out += draw_stack(B[2], [dA1[c] for c in ordF], 0.0, pen_red, mode="marks",
                      r_max=0.66, scale=float(np.abs(dA1).max()),
                      only_nonzero=True, thresh=0.02, border=True)
    for k, pl in enumerate(B[2]):
        keep = _occluder(B[2][:k])
        G = upsample(A1[ordF[k]], 4)
        runs = [[pl.pt(a, b) for a, b in ch] for ch in iso_chains(G, 0.0)]
        out += emit(_band(clip_runs(runs, keep)), red)
    # --- col 4 backward: the unpool scatter, 368/1600 --------------------
    out += draw_stack(B[3], [dR1[c] for c in ordF], 0.0, pen_red, mode="marks",
                      r_max=0.68, scale=float(np.abs(dR1).max()),
                      only_nonzero=True, thresh=0.02)
    # --- col 5 backward: dA2 -------------------------------------------
    # only 48 of 384 second-stage gradients survive the mask, so the plane is
    # nearly empty by construction. The few that live are drawn LOUD rather
    # than faint — the emptiness is the statement, not an accident.
    out += draw_stack(B[4], [dA2[c] for c in ordD], 0.0, pen_red, mode="marks",
                      r_max=1.15, scale=float(np.abs(dA2).max()),
                      only_nonzero=True, thresh=0.02)

    # ------------------------------------------------------------- plates
    out += _input_plate_art(fr, X, U_PLATE, FWD_AXIS, 39.0, blk, blu)
    # dL/dx is a high-frequency array: at the forward plate's floor every cell
    # inks and the plate reads as noise. Only the cells carrying at least 14%
    # of the peak gradient are drawn, and the radius law is steeper, so the
    # structure that IS there survives. Nothing is invented — cells are
    # dropped, never added.
    out += _input_plate_art(fr, dX, U_PLATE, BWD_AXIS, 39.0, red, red,
                            floor=0.14, gamma=0.75)

    # ------------------------------------------------- classifier + softmax
    out += _classifier_bar(fr, Wc, U_BAR, FWD_AXIS, 46.0, blk)
    out += _classifier_bar(fr, dWc, U_BAR, BWD_AXIS, 40.0, red)
    out += _softmax_column(fr, p, win, U_SOFT, FWD_AXIS, blk, blu)
    out += _grad_column(fr, dz, dWc, target, U_SOFT, BWD_AXIS, red, blk)

    # -------------------------------------------------------------- bundles
    out += _all_bundles(fr, net, F, B, hot, ordF, ordD, blk, blu, red)

    # ------------------------------------------------------------ swatches
    out += _swatch_row(fr, [W1[c] for c in ordF], U_C1, SWATCH_V, blk, blu, hot_first=True)
    out += _swatch_row(fr, [dW1[c] for c in ordF], U_C1, GSWATCH_V, red, red, hot_first=False)

    # ---------------------------------------------------------------- type
    out += _labels(fr, net, blk, red, blu, hot)

    # -------------------------------------------------------------- legend
    out += _legend(fr, net, blk, blu, red)

    # ----------------------------------------------------------- furniture
    for u, v in ((0.0, 0.0), (394.0, 0.0), (0.0, 271.0), (394.0, 271.0)):
        x, y = fr.p(u, v)
        out += plus_mark(x, y, s=fr.du(2.5), pen=blk)
    out += _text("C N N", fr.u(391.0), fr.v(267.5), 3.2, blk, align="right")

    return out


# ===========================================================================
# components
# ===========================================================================
def _input_plate_art(fr: Frame, A: np.ndarray, u_c: float, v_c: float, size: float,
                     pen: Optional[int], hot_pen: Optional[int],
                     floor: float = 0.035, gamma: float = 0.5) -> List[GCodeCommand]:
    """The stimulus (or its gradient) as a Ben-Day plate: dot RADIUS = |value|,
    filled = positive.  The rings you see are the array's real wavefronts."""
    u0, u1 = u_c - size / 2.0, u_c + size / 2.0
    v0, v1 = v_c - size / 2.0, v_c + size / 2.0
    out = _poly([fr.p(u0, v0), fr.p(u1, v0), fr.p(u1, v1), fr.p(u0, v1), fr.p(u0, v0)],
                color=pen, f=F_DRAW)
    ny, nx = A.shape
    m = float(np.abs(A).max())
    step = size / nx
    r_max = step * 0.46
    for j in range(ny):
        for i in range(nx):
            v = float(A[j, i])
            t = abs(v) / m
            if t < floor:
                continue
            uu = u0 + (i + 0.5) * step
            vv = v0 + (j + 0.5) * step
            x, y = fr.p(uu, vv)
            out += mark(x, y, fr.du(r_max * t ** gamma), pen, v >= 0)
    return out


def _classifier_bar(fr: Frame, W: np.ndarray, u_c: float, v_c: float, height: float,
                    pen: Optional[int]) -> List[GCodeCommand]:
    """The weight matrix as a tall narrow bar of ticks: each row of the bar is
    the mean |W| over a contiguous block of the matrix's rows."""
    rows = 32
    w = 8.0
    u0, u1 = u_c - w / 2.0, u_c + w / 2.0
    v0, v1 = v_c - height / 2.0, v_c + height / 2.0
    out = _poly([fr.p(u0, v0), fr.p(u1, v0), fr.p(u1, v1), fr.p(u0, v1), fr.p(u0, v0)],
                color=pen, f=F_DRAW)
    mag = np.abs(W).mean(axis=1)
    blocks = np.array_split(mag, rows)
    vals = np.array([b.mean() for b in blocks])
    vals = vals / vals.max()
    pitch = height / rows
    for k, t in enumerate(vals):
        vv = v0 + (k + 0.5) * pitch
        ln = (w - 1.6) * float(t)
        out += _poly([fr.p(u0 + 0.8, vv), fr.p(u0 + 0.8 + ln, vv)], color=pen, f=F_DRAW)
    return out


def _softmax_column(fr: Frame, p: np.ndarray, win: int, u_c: float, v_c: float,
                    pen: Optional[int], hot: Optional[int]) -> List[GCodeCommand]:
    """Circle AREA = p_k.  The column's total inked area is therefore constant
    at 1 — the normalisation is drawn, not asserted."""
    K = p.size
    pitch = 9.6
    R = 7.6
    out: List[GCodeCommand] = []
    for k in range(K):
        vv = v_c - (K - 1) / 2.0 * pitch + k * pitch
        x, y = fr.p(u_c, vv)
        r = fr.du(R * math.sqrt(float(p[k])))
        pn = hot if k == win else pen
        # spiral-filled at a FIXED 0.58 mm pitch, so the ink LENGTH in each
        # disc is proportional to its area, i.e. to p_k exactly. The column's
        # total ink is therefore constant however the distribution moves.
        if r > fr.du(0.9):
            out += fill_disc(x, y, r, spacing=fr.du(0.58), pen=pn, f=F_DRAW)
            out += circle(x, y, r, pen=pn, f=F_DRAW, n=44)
        else:
            out += mark(x, y, max(r, fr.du(0.3)), pn, True)
        out += _text(f"p{k + 1}", fr.u(u_c + 10.5), y - fr.dv(0.9), 2.1, pen)
    return out


def _grad_column(fr: Frame, dz: np.ndarray, dWc: np.ndarray, target: int,
                 u_c: float, v_c: float, pen: Optional[int],
                 blk: Optional[int]) -> List[GCodeCommand]:
    """Nodes: radius = |dz_k|.  Tiles: hatch duty = |dWc[:, k]| column norm,
    hatch angle = sign(dz_k)."""
    K = dz.size
    pitch = 7.2
    out: List[GCodeCommand] = []
    cn = np.abs(dWc).sum(axis=0)
    cn = cn / cn.max()
    m = float(np.abs(dz).max())
    for k in range(K):
        vv = v_c - (K - 1) / 2.0 * pitch + k * pitch
        x, y = fr.p(u_c - 4.0, vv)
        r = fr.du(2.4 * math.sqrt(abs(float(dz[k])) / m))
        out += mark(x, y, max(r, fr.du(0.3)), pen, dz[k] >= 0)
        out += hatch_tile(fr, u_c + 3.0, vv - 2.6, u_c + 8.2, vv + 2.6,
                          float(cn[k]) ** 0.8, 45.0 if dz[k] >= 0 else -45.0, pen,
                          spacing=1.0)
    return out


def _swatch_row(fr: Frame, kers: Sequence[np.ndarray], u_c: float, v: Tuple[float, float],
                pen: Optional[int], hot: Optional[int], hot_first: bool) -> List[GCodeCommand]:
    """Three of the real k x k kernels (or their gradients), contoured."""
    n = 3
    h = v[1] - v[0]
    w = h
    gap = 3.4
    total = n * w + (n - 1) * gap
    u0 = u_c - total / 2.0
    out: List[GCodeCommand] = []
    for k in range(n):
        uu = u0 + k * (w + gap)
        pl = Plane(*fr.p(uu, v[1]), fr.du(w), 0.0, 0.0, fr.dv(h))
        out += _poly(pl.quad(), color=pen, f=F_DRAW)
        pn = hot if (k == 0 and hot_first) else pen
        out += plane_contours(kers[k], pl, 1.15, pn, lambda q: True, up=6, zero=True,
                              zero_pen=pn)
    return out


def _all_bundles(fr: Frame, net, F, B, hot: int, ordF, ordD,
                 blk, blu, red) -> List[GCodeCommand]:
    """Every bundle's dash duty is a real coupling magnitude."""
    out: List[GCodeCommand] = []
    W1, W2, dW2 = net["W1"], net["W2"], net["dW2"]
    A1, A2, Wc, dWc = net["A1"], net["A2"], net["Wc"], net["dWc"]
    dA1, dA2 = net["dA1"], net["dA2"]
    C1n, C2n = A1.shape[0], A2.shape[0]

    def edges(stack, side, spread=0.82):
        """v-positions on a stack's left(0)/right(1) edge, one per plane."""
        vs = []
        for pl in stack:
            x, y = pl.pt(side, 0.5)
            vs.append(( (fr.y1 - y) / fr.sy, (x - fr.x0) / fr.sx ))
        return vs

    def vlist(stack, side):
        return [e[0] for e in edges(stack, side)]

    def ulist(stack, side):
        return [e[1] for e in edges(stack, side)]

    # --- forward -------------------------------------------------------
    # input -> kernels: one curve per kernel, duty = kernel energy
    ke = np.sqrt((W1 ** 2).sum(axis=(1, 2)))[ordF][:, None]
    out += fan(fr, U_PLATE + 20.5, [FWD_AXIS], min(ulist(F[0], 0)) - 1.0,
               vlist(F[0], 0), ke.T, lambda s, d: blu if d == 0 else blk, FWD_AXIS, pinch=0.22)
    # kernels -> feature maps -> relu -> pool: one sheaf per channel, each
    # strand's duty = that band's real row energy in the channel's array.
    rows = lambda A: np.abs(A).mean(axis=1)[::-1]   # noqa: E731  (v is top-down)
    pen_f = lambda c, k: blu if c == 0 else blk     # noqa: E731
    out += channel_fan(fr, F[0], F[1], [rows(A1[c]) for c in ordF], pen_f, FWD_AXIS)
    out += channel_fan(fr, F[1], F[2], [rows(net["M1"][c]) for c in ordF], pen_f,
                       FWD_AXIS)
    out += channel_fan(fr, F[2], F[3], [rows(net["R1"][c]) for c in ordF], pen_f,
                       FWD_AXIS)
    # pool -> deeper: the REAL 4 x 6 coupling ||W2[k, c]||
    cpl = np.sqrt((W2 ** 2).sum(axis=(2, 3))).T[ordF][:, ordD]
    out += fan(fr, max(ulist(F[3], 1)) + 1.0, vlist(F[3], 1),
               min(ulist(F[4], 0)) - 1.0, vlist(F[4], 0), cpl,
               lambda s, d: blu if s == 0 else blk, FWD_AXIS, pinch=0.26)
    # deeper -> classifier: duty = ||Wc block|| for that channel
    blocks = np.abs(Wc).sum(axis=1).reshape(C2n, -1).sum(axis=1)[ordD]
    out += fan(fr, max(ulist(F[4], 1)) + 1.0, vlist(F[4], 1),
               U_BAR - 5.0, [FWD_AXIS], (blocks / blocks.max())[:, None],
               lambda s, d: blu if s == 0 else blk, FWD_AXIS, pinch=0.26)
    # classifier -> softmax
    K = net["p"].size
    soft_v = [FWD_AXIS - (K - 1) / 2.0 * 8.4 + k * 8.4 for k in range(K)]
    zn = np.abs(net["z"]) / np.abs(net["z"]).max()
    out += fan(fr, U_BAR + 5.0, [FWD_AXIS], U_SOFT - 7.5, soft_v,
               zn[None, :], lambda s, d: blu if d == net["win"] else blk,
               FWD_AXIS, pinch=0.22)

    # --- backward (right to left, crimson) ------------------------------
    gz = np.abs(net["dz"]) / np.abs(net["dz"]).max()
    gsoft_v = [BWD_AXIS - (K - 1) / 2.0 * 7.2 + k * 7.2 for k in range(K)]
    out += fan(fr, U_SOFT - 7.0, gsoft_v, U_BAR + 5.0, [BWD_AXIS],
               gz[:, None], lambda s, d: red, BWD_AXIS, pinch=0.22)
    gblocks = np.abs(dWc).sum(axis=1).reshape(C2n, -1).sum(axis=1)[ordD]
    out += fan(fr, U_BAR - 5.0, [BWD_AXIS], max(ulist(B[4], 1)) + 1.0,
               vlist(B[4], 1), (gblocks / gblocks.max())[None, :],
               lambda s, d: red, BWD_AXIS, pinch=0.22)
    gcpl = np.sqrt((dW2 ** 2).sum(axis=(2, 3)))[ordD][:, ordF]
    out += fan(fr, min(ulist(B[4], 0)) - 1.0, vlist(B[4], 0),
               max(ulist(B[3], 1)) + 1.0, vlist(B[3], 1), gcpl,
               lambda s, d: red, BWD_AXIS, pinch=0.26)
    rows_b = lambda A: np.abs(A).mean(axis=1)[::-1]   # noqa: E731
    pen_b = lambda c, k: red                          # noqa: E731
    out += channel_fan(fr, B[3], B[2], [rows_b(net["dR1"][c]) for c in ordF],
                       pen_b, BWD_AXIS, rightward=False)
    out += channel_fan(fr, B[2], B[1], [rows_b(dA1[c]) for c in ordF],
                       pen_b, BWD_AXIS, rightward=False)
    out += channel_fan(fr, B[1], B[0], [rows_b(net["dW1"][c]) for c in ordF],
                       pen_b, BWD_AXIS, rightward=False)
    ge = np.abs(net["dW1"]).sum(axis=(1, 2))[ordF]
    out += fan(fr, min(ulist(B[0], 0)) - 1.0, vlist(B[0], 0),
               U_PLATE + 20.5, [BWD_AXIS], ge[:, None] / ge.max(),
               lambda s, d: red, BWD_AXIS, pinch=0.22)
    return out


def _labels(fr: Frame, net, blk, red, blu, hot: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    p = net["p"]
    fwd = [
        (U_C1, "convolution", "(kernels as wave filters)"),
        (U_C2, "feature maps", "(frequency responses)"),
        (U_C3, "non-linearity", "(ReLU)"),
        (U_C4, "pooling", "(downsample)"),
        (U_C5, "deeper layers", "(more abstract spectra)"),
        (U_BAR + 12.0, "classifier", "(linear + softmax)"),
    ]
    for u, a, b in fwd:
        out += _text(a, fr.u(u), fr.v(FWD_LAB_V[0]), LAB_CAP, blk, align="centre")
        out += _text(b, fr.u(u), fr.v(FWD_LAB_V[1]), LAB_CAP * 0.80, blk, align="centre")

    shapes = [
        (U_PLATE, "X", "24 × 24 × 1"),
        (U_C1, "W1", "5 × 5 × 1 × 4"),
        (U_C2, "A1", "20 × 20 × 4"),
        (U_C3, "R1", "20 × 20 × 4"),
        (U_C4, "P1", "10 × 10 × 4"),
        (U_C5, "A2", "8 × 8 × 6"),
        (U_BAR, "Wc", "96 × 6"),
    ]
    for u, a, b in shapes:
        vv = SWATCH_CAP_V if u == U_C1 else FWD_SHAPE_V[0]
        out += _text(a, fr.u(u), fr.v(vv), SHAPE_CAP * 1.25, blk, align="centre")
        if u != U_C1:
            out += _text(b, fr.u(u), fr.v(FWD_SHAPE_V[1]), SHAPE_CAP, blk, align="centre")
        else:
            out += _text(b, fr.u(u), fr.v(vv + 5.0), SHAPE_CAP, blk, align="centre")

    bwd = [
        (U_C1, "∂L/∂(conv)", "(filter gradients)"),
        (U_C2, "∂L/∂A1", ""),
        (U_C3, "∂L/∂(ReLU)", "(mask)"),
        (U_C4, "∂L/∂P1", "(unpool)"),
        (U_C5, "∂L/∂A2", ""),
        (U_BAR, "∂L/∂Wc", "(96 × 6)"),
        (U_SOFT + 3.0, "∂L/∂z", "(per-class tiles)"),
    ]
    for u, a, b in bwd:
        out += _text(a, fr.u(u), fr.v(BWD_LAB_V[0]), LAB_CAP, red, align="centre")
        if b:
            out += _text(b, fr.u(u), fr.v(BWD_LAB_V[1]), LAB_CAP * 0.80, red, align="centre")
    out += _text("∂L/∂x", fr.u(U_PLATE), fr.v(BWD_SHAPE_V), SHAPE_CAP * 1.3, red,
                 align="centre")
    out += _text("∂L/∂W1", fr.u(U_C1), fr.v(GSWATCH_CAP_V), SHAPE_CAP * 1.3, red,
                 align="centre")

    # The plate's subject, at poster scale: two words running up the left
    # margin, one per register.  Caption-sized type everywhere is the
    # technical-drawing default (DESIGN_RUBRIC) and the register symmetry is
    # the whole idea, so it gets the only display type on the sheet.
    out += _spine(fr, "FORWARD PASS", FWD_TOP, FWD_BOT, blk)
    out += _spine(fr, "BACKWARD PASS", BWD_TOP, BWD_BOT, red)
    out += _text("activations", fr.u(U_SPINE + 6.5), fr.v(FWD_TOP + 3.4),
                 SIDE_CAP * 0.8, blk)
    out += arrow(fr, U_SPINE + 6.5, U_SPINE + 28.5, FWD_TOP + 7.0, blk)
    out += _text("gradients", fr.u(U_SPINE + 6.5), fr.v(BWD_TOP + 3.4),
                 SIDE_CAP * 0.8, red)
    out += arrow(fr, U_SPINE + 28.5, U_SPINE + 6.5, BWD_TOP + 7.0, red)

    # the register rule + one registration tick per column
    out += _poly([fr.p(0.0, MID_RULE_V), fr.p(394.0, MID_RULE_V)], color=blk, f=F_DRAW)
    for u in (U_PLATE, U_C1, U_C2, U_C3, U_C4, U_C5, U_BAR, U_SOFT):
        out += _poly([fr.p(u, MID_RULE_V - 1.6), fr.p(u, MID_RULE_V + 1.6)],
                     color=blk, f=F_DRAW)

    # the ellipsis the plate admits to — clear of the bundle neck, which is
    # exactly where it sat in v1 and where it read as part of the knot
    for k in range(3):
        x, y = fr.p(U_ELL - 4.5 + k * 4.5, FWD_AXIS - 27.0)
        out += mark(x, y, fr.du(0.85), blk, True)
        x, y = fr.p(U_ELL - 4.5 + k * 4.5, BWD_AXIS - 27.0)
        out += mark(x, y, fr.du(0.85), red, True)

    out += _text("softmax", fr.u(U_SOFT), fr.v(FWD_TOP + 2.5), LAB_CAP, blk, align="centre")
    return out


def _spine(fr: Frame, text: str, v_top: float, v_bot: float,
           pen: Optional[int]) -> List[GCodeCommand]:
    """The register name at poster scale, running UP the left margin."""
    cap = 5.0
    w = _text_width(text, cap, proportional=True)
    span = v_bot - v_top
    while w > span - 2.0 and cap > 3.4:
        cap -= 0.1
        w = _text_width(text, cap, proportional=True)
    v_start = v_top + (span + w) / 2.0          # baseline of the first glyph
    return giant_type(text, fr.u(U_SPINE), fr.v(v_start), fr.du(cap), pen=pen,
                      weight=fr.du(0.42), tip=0.34, angle=90.0, proportional=True,
                      f=F_DRAW)


def _legend(fr: Frame, net, blk, blu, red) -> List[GCodeCommand]:
    """Five cells, each carrying the real numbers from this pass."""
    out: List[GCodeCommand] = []
    out += _poly([fr.p(0.0, LEG_RULE_V), fr.p(394.0, LEG_RULE_V)], color=blk, f=F_DRAW)
    n = 5
    w = 394.0 / n
    for k in range(1, n):
        out += _poly([fr.p(k * w, LEG_TOP - 2.5), fr.p(k * w, LEG_BOT + 0.5)],
                     color=blk, f=F_DRAW)

    cap = 1.9
    X, W1, A1 = net["X"], net["W1"], net["A1"]
    p, dz, L = net["p"], net["dz"], net["L"]

    # 1 — convolution = local correlation, drawn as the real 1-D slice
    u0 = 3.0
    out += _text("convolution = local correlation", fr.u(u0), fr.v(LEG_TOP), cap, blk)
    out += _text("row 12 of X  ∗  centre row of kernel 1  =  the drawn result",
                 fr.u(u0), fr.v(LEG_TOP + 4.2), cap * 0.88, blk)
    row = X[12]
    ker = W1[0][2]
    res = np.correlate(row, ker, mode="valid")   # the real 1-D correlation

    def trace(u_a: float, u_b: float, vmid: float, arr, amp: float, pen):
        m = float(np.abs(arr).max()) or 1.0
        pts = [fr.p(u_a + (u_b - u_a) * i / (len(arr) - 1), vmid - amp * float(arr[i]) / m)
               for i in range(len(arr))]
        return _poly(pts, color=pen, f=F_DRAW)

    vmid = LEG_TOP + 14.0
    out += trace(u0, u0 + 22.0, vmid, row, 4.2, blk)
    out += _text("∗", fr.u(u0 + 24.0), fr.v(vmid + 1.0), cap * 1.3, blk)
    out += trace(u0 + 27.0, u0 + 38.0, vmid, ker, 4.2, blu)
    out += _text("=", fr.u(u0 + 40.0), fr.v(vmid + 1.0), cap * 1.3, blk)
    out += trace(u0 + 43.0, u0 + 74.0, vmid, res, 4.2, blk)

    # 2 — ReLU, with the real alive fraction
    u0 = w + 3.0
    out += _text("non-linearity (ReLU)", fr.u(u0), fr.v(LEG_TOP), cap, blk)
    ax_v = LEG_TOP + 17.0
    out += _poly([fr.p(u0 + 2.0, ax_v), fr.p(u0 + 26.0, ax_v)], color=blk, f=F_DRAW)
    out += _poly([fr.p(u0 + 14.0, ax_v + 1.5), fr.p(u0 + 14.0, ax_v - 12.0)],
                 color=blk, f=F_DRAW)
    out += _poly([fr.p(u0 + 2.0, ax_v), fr.p(u0 + 14.0, ax_v), fr.p(u0 + 25.0, ax_v - 11.0)],
                 color=red, f=F_DRAW)
    out += _text("y = max(0, x)", fr.u(u0 + 2.0), fr.v(LEG_TOP + 21.5), cap * 0.88, blk)
    out += _text(f"alive  {int(net['M1'].sum())}  of  {net['M1'].size}  =  "
                 f"{net['M1'].mean():.3f}", fr.u(u0 + 30.0), fr.v(LEG_TOP + 6.5),
                 cap * 0.88, blk)
    out += _text(f"gradient killed  {int((net['dR1'] != 0).sum() - (net['dA1'] != 0).sum())}"
                 f"  of  {int((net['dR1'] != 0).sum())}", fr.u(u0 + 30.0),
                 fr.v(LEG_TOP + 11.0), cap * 0.88, red)

    # 3 — pooling: a REAL 4x4 patch of R1 -> 2x2, argmax marked
    u0 = 2 * w + 3.0
    out += _text("pooling (2 × 2 max)", fr.u(u0), fr.v(LEG_TOP), cap, blk)
    patch = net["R1"][0][6:10, 6:10]
    cell = 2.9
    top = LEG_TOP + 5.5
    for j in range(4):
        for i in range(4):
            out += _poly([fr.p(u0 + i * cell, top + j * cell),
                          fr.p(u0 + (i + 1) * cell, top + j * cell),
                          fr.p(u0 + (i + 1) * cell, top + (j + 1) * cell),
                          fr.p(u0 + i * cell, top + (j + 1) * cell),
                          fr.p(u0 + i * cell, top + j * cell)], color=blk, f=F_DRAW)
    pm = float(np.abs(patch).max()) or 1.0
    for j in range(2):
        for i in range(2):
            blk4 = patch[2 * j:2 * j + 2, 2 * i:2 * i + 2]
            a = int(np.argmax(blk4))
            jj, ii = 2 * j + a // 2, 2 * i + a % 2
            x, y = fr.p(u0 + (ii + 0.5) * cell, top + (jj + 0.5) * cell)
            out += mark(x, y, fr.du(1.05), red, True)
    out += arrow(fr, u0 + 13.2, u0 + 18.6, top + 5.8, blk, head=2.2)
    top2 = top + 2.9
    for j in range(2):
        for i in range(2):
            out += _poly([fr.p(u0 + 20.5 + i * cell, top2 + j * cell),
                          fr.p(u0 + 20.5 + (i + 1) * cell, top2 + j * cell),
                          fr.p(u0 + 20.5 + (i + 1) * cell, top2 + (j + 1) * cell),
                          fr.p(u0 + 20.5 + i * cell, top2 + (j + 1) * cell),
                          fr.p(u0 + 20.5 + i * cell, top2 + j * cell)], color=blk, f=F_DRAW)
            v = float(patch[2 * j:2 * j + 2, 2 * i:2 * i + 2].max())
            x, y = fr.p(u0 + 20.5 + (i + 0.5) * cell, top2 + (j + 0.5) * cell)
            out += mark(x, y, fr.du(1.15 * math.sqrt(abs(v) / pm)), blk, True)
    out += _text("R1 patch (rows 6-9)", fr.u(u0 + 30.0), fr.v(LEG_TOP + 6.5),
                 cap * 0.88, blk)
    out += _text("the gradient returns", fr.u(u0 + 30.0), fr.v(LEG_TOP + 11.0),
                 cap * 0.88, red)
    out += _text("to the red cell only", fr.u(u0 + 30.0), fr.v(LEG_TOP + 15.0),
                 cap * 0.88, red)

    # 4 — softmax, real values
    u0 = 3 * w + 3.0
    out += _text("softmax  σ(z)", fr.u(u0), fr.v(LEG_TOP), cap, blk)
    for k in range(p.size):
        vv = LEG_TOP + 5.2 + k * 2.9
        ln = 32.0 * float(p[k])
        pen = blu if k == net["win"] else blk
        out += _text(f"p{k + 1}", fr.u(u0 + 0.5), fr.v(vv + 0.8), cap * 0.8, pen)
        out += _poly([fr.p(u0 + 6.0, vv), fr.p(u0 + 6.0 + max(ln, 0.4), vv)],
                     color=pen, f=F_DRAW)
        out += _text(f"{p[k]:.3f}", fr.u(u0 + 41.0), fr.v(vv + 0.8), cap * 0.86, pen)
    out += _text("sum p = 1.000", fr.u(u0 + 0.5), fr.v(LEG_BOT - 0.5), cap * 0.88, blk)

    # 5 — loss + the gradient it makes
    u0 = 4 * w + 3.0
    out += _text("loss (cross-entropy)", fr.u(u0), fr.v(LEG_TOP), cap, blk)
    out += _text(f"argmax = class {net['win'] + 1},  target = class {net['target'] + 1}",
                 fr.u(u0), fr.v(LEG_TOP + 4.6), cap * 0.88, blk)
    out += _text(f"L = - log p{net['target'] + 1} = {L:.4f}", fr.u(u0),
                 fr.v(LEG_TOP + 9.6), cap * 1.1, blk)
    out += _text("∂L/∂z = p - y", fr.u(u0), fr.v(LEG_TOP + 15.0), cap * 1.1, red)
    out += _text("  ".join(f"{v:+.3f}" for v in dz[:3]), fr.u(u0), fr.v(LEG_TOP + 19.4),
                 cap * 0.8, red)
    out += _text("  ".join(f"{v:+.3f}" for v in dz[3:]), fr.u(u0), fr.v(LEG_TOP + 23.0),
                 cap * 0.8, red)
    out += _text(f"sum = {dz.sum():+.1e}", fr.u(u0 + 30.0), fr.v(LEG_TOP + 23.0),
                 cap * 0.8, red)
    return out
