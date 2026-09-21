"""STABLE DIFFUSION AS TOPOGRAPHY — faithful recreation, r01.

Recreation of ``studio/stable-diffusion/ref/reference.png`` (1672x941, ratio
1.777) on a 420x240 mm sheet, with an explicit licence to fix the reference's
crowding (DESIGN_RUBRIC dimension 4, "OVERLAP IS A DECISION NEVER A SYMPTOM").

Every element's position was MEASURED off the raster with colour masks and
row/column profiles, and is recorded below in normalised sheet coordinates
``(u, v)``, u = 0 left .. 1 right, v = 0 TOP .. 1 bottom, mapped onto a
composition frame inset inside the drawable area.  Reference pixel boxes, for
the record:

    x nest (red)          x   51.. 269   y 169..379
    E horn (black)        x  250.. 439   y 155..345
    z0 nest (ochre)       x  432.. 565   y 209..331
    forward row states    x  ~500, 683, 845, 1005, 1180   y ~270 centre
    y nest (blue)         x   67.. 294   y 610..810
    tau horn              x  254.. 401   y 636..789
    c blob (blue)         x  401.. 499   y 681..743
    bowtie eps_theta      x  560..1104   y 380..639   (544 x 259 px = 2.10:1)
    gold sampling loop    x  631..1240   y 560..779
    z0 nest right         x 1150..1257   y 475..585
    D horn                x 1290..1415   y 438..613
    x-tilde nest (red)    x 1437..1630   y 400..665

WHAT MOVED, and why (the crowding fixes):

1.  The reference funnels `t`, the blue conditioning sheaf and the gold loop
    return into ONE channel at the bowtie's left waist, three bundles inside
    about 12 mm.  Here they arrive at three separated places on the network:
    `t` horizontally at the left tip (v 0.560), the conditioning sheaf into the
    lower-left flank (v 0.612), the gold return into the lower-left wing's
    underside (v 0.676).  Three inputs, three docks, 11 and 20 mm apart.
2.  The forward row's pitch went from 0.6x to 1.4x the state width, so the
    `...` between states sits in real paper instead of inside a dot cloud, and
    the clouds carry a knockout around each `...` box.
3.  A 11 mm band of clear paper separates the forward row's lowest ink from the
    bowtie's top silhouette; the droplines cross it and nothing else does.
4.  The sampling loop became ONE circulation with ONE direction (out of the
    waist, down, left along the bottom, up into the lower-left wing), instead
    of the reference's two ambiguous nested sweeps with arrows both ways.
5.  z_T and the recovered z0 share a vertical axis at u = 0.760 — the sampler
    starts at the top of that line and lands at the bottom of it.

WHAT IS EXACT (the maths, not eyeballed):

*   Forward schedule — cosine (Nichol & Dhariwal), ``abar(u) = cos^2(pi/2 *
    (u+s)/(1+s))``, s = 0.008, sampled at u = k/5.  A state's surviving ring
    count, dash duty and contour wobble are all one function of the noise-to-
    signal ratio ``w = C * sqrt(1-abar)/sqrt(abar)`` (the std of the injected
    noise measured in units of the signal that is left), and ``duty =
    1/(1+w^2)``.  That ratio is 0.33, 0.73, 1.38, 3.08, inf at the five steps:
    structure barely moves early and collapses late and fast, which a linear
    ramp would have lied about.
*   Isotropy — a fraction ``sqrt(abar)`` of a state's cloud is sampled inside
    the blob (structured), the rest from an isotropic Gaussian.  At z_T that is
    100% isotropic by construction, so no residual lobe can survive.
*   The lossy round trip — ``x~`` is ``x``'s own radial harmonic series pushed
    through the autoencoder's band limit: mode k is returned with gain
    ``g_k = min(1, (k_c/k)^2)``, k_c = 4, plus a phase error 0.055*k rad on the
    modes the latent does not keep.  So x~ rhymes with x, is smoother than x,
    and is not a copy of it.
*   Latent vs pixel — the z nests are 26 mm across against 46 mm for x and x~,
    a 1.77:1 ratio, and they carry 7 rings against x's 13.  The expensive loop
    lives entirely among the small things.
*   Contour ladders — every ring family is a level set of a CONICAL field.  The
    blobs use the distance to their own outline (|grad d| = 1, so the ring
    pitch is exactly the level step); the bowtie uses
    ``PHI = -sigma*log(F)`` of a sum of exponential cusps, which is linear in r
    around each cusp, so uniform PHI steps give a uniform ring pitch there too.
    No Gaussian peaks, no uniform iso-VALUES (DESIGN_RUBRIC dimension 5).

Pens (``colors=4``): 0 black (networks, type, furniture), 1 crimson (pixel
space: x, x~), 2 goldenrod (latent space: every z, and the sampling loop),
3 dodgerblue (conditioning: y, c).  Colour encodes WHICH SPACE a thing lives
in — that is the plate's key.

Entry point: ``stable_diffusion``.
"""

from __future__ import annotations

import logging
import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

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

logger = logging.getLogger(__name__)

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, RED, GOLD, BLUE = 0, 1, 2, 3

F_DRAW = 2200
MIN_PITCH = 0.82  # mm — plotting floor; no ring family may go under this


# ===========================================================================
# measured layout  (normalised sheet coords; v = 0 TOP)
# ===========================================================================
FRAME_INSET = 4.0

# --- header / captions --------------------------------------------------
TITLE_CAP = 3.8
TITLE_U = 0.008
TITLE_V = (0.046, 0.080)  # baselines
TITLE_W = 62.0  # tracked width of the longer line

Q_CAP = 5.2
Q_V = 0.108  # baseline of q(z_t | z_{t-1})
Q_ARROW_V = 0.146
Q_ARROW_U = (0.400, 0.648)

FOOT_CAP = 2.5
FOOT_L_U = 0.008
FOOT_L_V = (0.908, 0.934, 0.960, 0.986)
FOOT_R_U = 0.992
FOOT_R_V = (0.908, 0.934, 0.960, 0.986)

# --- top band: pixel -> latent -> forward process ------------------------
ROW_V = 0.283
X_C = (0.072, ROW_V)
E_MOUTH_U, E_APEX_U = 0.152, 0.238
ROW_U0, ROW_DU = 0.294, 0.0932
N_STATES = 6
ROW_U = tuple(ROW_U0 + k * ROW_DU for k in range(N_STATES))  # last = 0.760

X_RX, X_RY = 23.0, 22.0  # mm, half-extents of the pixel-space nests
Z_RX, Z_RY = 13.0, 12.0  # mm, half-extents of the latent nests  (1.77:1)
HORN_HALF_H = 21.0

# --- the denoiser --------------------------------------------------------
EPS_C = (0.500, 0.560)
BOW_HW, BOW_HH = 59.0, 29.5  # mm
BOW_PITCH = 1.28
BOW_RINGS = 30

# --- conditioning --------------------------------------------------------
COND_V = 0.768
Y_C = (0.072, COND_V)
T_MOUTH_U, T_APEX_U = 0.152, 0.238
C_C = (0.300, COND_V)
Y_RX, Y_RY = 24.0, 21.0
C_RX, C_RY = 11.0, 8.0

# --- the three docks on the network's left flank -------------------------
DOCK_T = (0.352, 0.560)  # timestep, horizontal, black
DOCK_C = (0.366, 0.612)  # conditioning sheaf, blue, from lower-left
DOCK_LOOP = (0.414, 0.676)  # sampling-loop return, gold, from below

# --- the sampling loop ---------------------------------------------------
LOOP_C = (0.500, 0.688)
LOOP_RX = (0.102, 0.120, 0.138)
LOOP_RY = (0.108, 0.130, 0.152)
OUT_V = 0.700  # waist underside: where z_{t-1} leaves
ZTM1_V = 0.876  # label baseline, below the outermost arc

# --- decoder -------------------------------------------------------------
DEC_V = 0.583
ZR_C = (0.760, DEC_V)
D_APEX_U, D_MOUTH_U = 0.804, 0.848
XT_C = (0.925, DEC_V)

# --- radial harmonic series (k, amplitude, phase) ------------------------
X_HARM = ((4, 0.300, 0.55), (3, 0.100, 2.10), (5, 0.085, 0.40), (7, 0.045, 1.30))
Z_HARM = ((4, 0.260, 0.90), (3, 0.075, 0.20), (5, 0.050, 2.40))
Y_HARM = ((3, 0.300, 1.90), (2, 0.160, 0.60), (5, 0.060, 0.90))
C_HARM = ((3, 0.220, 2.60), (4, 0.100, 0.30))
K_CUTOFF = 4.0  # the latent's band limit


# ===========================================================================
# the forward schedule — cosine, used exactly
# ===========================================================================
_S = 0.008


def _abar(u: float) -> float:
    u = 0.0 if u < 0.0 else (1.0 if u > 1.0 else u)
    return math.cos(0.5 * math.pi * (u + _S) / (1.0 + _S)) ** 2


def _nsr(u: float) -> float:
    """Injected-noise std measured in units of the surviving signal.

    ``sqrt(1-abar)/sqrt(abar)``.  Every dissolution decision on the forward row
    is one function of this single number, which is why the row collapses late
    and fast instead of fading linearly.
    """
    ab = _abar(u)
    if ab <= 1e-9:
        return float("inf")
    return math.sqrt(max(0.0, 1.0 - ab) / ab)


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

    def du(self, mm: float) -> float:
        return mm / self.w

    def dv(self, mm: float) -> float:
        return mm / self.h


# ===========================================================================
# type
# ===========================================================================
def _tracked(
    text: str, x: float, baseline: float, cap: float, pen: Optional[int],
    target_w: Optional[float] = None, f: int = 2300,
) -> List[GCodeCommand]:
    """Proportional stroke type with uniform tracking to hit ``target_w``."""
    sc = cap / 6.0
    nat = _text_width(text, cap, proportional=True)
    extra = (target_w - nat) / (len(text) - 1) if (target_w and len(text) > 1) else 0.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * sc + extra
    return out


def _tw(text: str, cap: float) -> float:
    return _text_width(text, cap, proportional=True)


def _text_at(
    text: str, baseline: float, cap: float, pen: Optional[int],
    left: Optional[float] = None, centre: Optional[float] = None,
    right: Optional[float] = None, target_w: Optional[float] = None,
) -> List[GCodeCommand]:
    w = target_w if target_w is not None else _tw(text, cap)
    if left is not None:
        x = left
    elif centre is not None:
        x = centre - w / 2.0
    else:
        x = (right or 0.0) - w
    return _tracked(text, x, baseline, cap, pen, target_w)


def _tau(x: float, baseline: float, cap: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Greek lower-case tau as ONE drawn mark, left edge at ``x``.

    The shared single-stroke font carries eps/theta/sigma but not tau, so
    ``tau_theta`` would silently degrade.  Drawn in the same 4x6 glyph metric;
    the font gap is recorded in NOTES.md for central fixing.
    """
    sc = cap / 6.0
    bar = [(x + 0.2 * sc, baseline + 4.0 * sc), (x + 4.0 * sc, baseline + 4.0 * sc)]
    stem = [
        (x + 2.1 * sc, baseline + 4.0 * sc),
        (x + 1.85 * sc, baseline + 1.5 * sc),
        (x + 2.25 * sc, baseline + 0.15 * sc),
        (x + 3.3 * sc, baseline + 0.45 * sc),
    ]
    return _poly(bar, color=pen, f=2300) + _poly(stem, color=pen, f=2300)


def _tau_w(cap: float) -> float:
    return 4.6 * cap / 6.0


def _math(
    parts: Sequence[Tuple[str, str]],
    baseline: float, cap: float, pen: Optional[int],
    left: Optional[float] = None, centre: Optional[float] = None,
) -> List[GCodeCommand]:
    """Lay out a math label as (kind, text) runs.

    kind: 'r' roman, 'sub' subscript (0.62 cap, dropped), 'tau' the tau mark.
    The font has no subscript digits, so subscripts are SET, not substituted:
    same face, 0.62 of the cap, baseline dropped 0.26 of the cap.
    """
    sub_cap = cap * 0.62
    sub_drop = cap * 0.26
    widths = []
    for kind, txt in parts:
        if kind == "tau":
            widths.append(_tau_w(cap))
        elif kind == "sub":
            widths.append(_tw(txt, sub_cap))
        else:
            widths.append(_tw(txt, cap))
    total = sum(widths)
    x = left if left is not None else (centre or 0.0) - total / 2.0
    out: List[GCodeCommand] = []
    for (kind, txt), w in zip(parts, widths):
        if kind == "tau":
            out += _tau(x, baseline, cap, pen)
        elif kind == "sub":
            out += _tracked(txt, x, baseline - sub_drop, sub_cap, pen)
        else:
            out += _tracked(txt, x, baseline, cap, pen)
        x += w
    return out


def _math_w(parts: Sequence[Tuple[str, str]], cap: float) -> float:
    sub_cap = cap * 0.62
    t = 0.0
    for kind, txt in parts:
        t += _tau_w(cap) if kind == "tau" else _tw(txt, sub_cap if kind == "sub" else cap)
    return t


def _tilde_over(cx: float, baseline: float, cap: float, pen: Optional[int]) -> List[GCodeCommand]:
    """A drawn tilde accent centred over a glyph (the font has no composed x~)."""
    sc = cap / 6.0
    w = 2.6 * sc
    y = baseline + 4.9 * sc
    pts = [
        (cx - w, y),
        (cx - w * 0.45, y + 0.72 * sc),
        (cx + w * 0.45, y - 0.72 * sc),
        (cx + w, y),
    ]
    return _poly(pts, color=pen, f=2300)


# ===========================================================================
# contouring — numpy-prefiltered marching squares, chained
# ===========================================================================
_MS_TABLE = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),),
    5: ((3, 2), (0, 1)), 6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),),
    9: ((0, 2),), 10: ((0, 3), (1, 2)), 11: ((1, 2),), 12: ((1, 3),),
    13: ((0, 1),), 14: ((0, 3),),
}


def _iso_chains(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, iso: float) -> List[Poly]:
    v0, v1 = F[:-1, :-1], F[:-1, 1:]
    v2, v3 = F[1:, 1:], F[1:, :-1]
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


def _grid(box: Bounds, step: float):
    x0, y0, x1, y1 = box
    xs = np.arange(x0, x1 + step, step)
    ys = np.arange(y0, y1 + step, step)
    X, Y = np.meshgrid(xs, ys)
    return xs, ys, X, Y


# ===========================================================================
# outlines + distance fields
# ===========================================================================
def _amoeba(harmonics: Sequence[Tuple[int, float, float]], n: int = 320) -> Poly:
    """Closed radial blob ``r(theta) = 1 + sum a_k cos(k theta + phi_k)``."""
    pts: Poly = []
    for k in range(n):
        t = 2 * math.pi * k / n
        r = 1.0
        for kk, a, ph in harmonics:
            r += a * math.cos(kk * t + ph)
        pts.append((r * math.cos(t), r * math.sin(t)))
    return pts


def _bandlimit(harmonics, k_c: float = K_CUTOFF, phase_err: float = 0.055):
    """Push a harmonic series through the autoencoder's band limit.

    Mode k comes back with gain ``min(1, (k_c/k)^2)`` and, for the modes the
    latent does not keep, a phase error.  This is the ONLY difference between
    ``x`` and ``x~``: the round trip is lossy and the plate says so.
    """
    out = []
    for k, a, ph in harmonics:
        g = 1.0 if k <= k_c else (k_c / k) ** 2
        out.append((k, a * g, ph + (phase_err * k if k > k_c else 0.0)))
    return tuple(out)


def _place(poly: Poly, cx: float, cy: float, rx: float, ry: float) -> Poly:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    sx = 2.0 * rx / (max(xs) - min(xs))
    sy = 2.0 * ry / (max(ys) - min(ys))
    mx, my = (max(xs) + min(xs)) / 2.0, (max(ys) + min(ys)) / 2.0
    return [(cx + (p[0] - mx) * sx, cy + (p[1] - my) * sy) for p in poly]


def _dist_field(poly: Poly, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Distance to the boundary, positive INSIDE, 0 outside.  |grad d| = 1."""
    P = np.asarray(poly, float)
    A, B = P, np.roll(P, -1, axis=0)
    d = np.full(X.shape, 1e9)
    inside = np.zeros(X.shape, bool)
    for (ax, ay), (bx, by) in zip(A, B):
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        if L2 > 1e-12:
            t = np.clip(((X - ax) * vx + (Y - ay) * vy) / L2, 0.0, 1.0)
            d = np.minimum(d, np.hypot(X - (ax + t * vx), Y - (ay + t * vy)))
        cond = (ay > Y) != (by > Y)
        if cond.any():
            xint = np.where(abs(by - ay) > 1e-12, ax + (Y - ay) * vx / (by - ay + 1e-30), ax)
            inside ^= cond & (X < xint)
    return np.where(inside, d, 0.0)


def _pt_in_poly(px: float, py: float, poly: Poly) -> bool:
    inside = False
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        if (ay > py) != (by > py):
            xint = ax + (py - ay) * (bx - ax) / (by - ay + 1e-30)
            if px < xint:
                inside = not inside
    return inside


def _value_noise(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    i0, j0 = np.floor(U).astype(int), np.floor(V).astype(int)
    fu, fv = U - i0, V - j0
    su, sv = fu * fu * (3 - 2 * fu), fv * fv * (3 - 2 * fv)

    def h(a, b):
        n = (a * 374761393 + b * 668265263) & 0xFFFFFFFF
        n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFFFF) / 0xFFFFFF

    a00, a10 = h(i0, j0), h(i0 + 1, j0)
    a01, a11 = h(i0, j0 + 1), h(i0 + 1, j0 + 1)
    return (a00 * (1 - su) + a10 * su) * (1 - sv) + (a01 * (1 - su) + a11 * su) * sv


def _fbm(rng: SeededRNG, X: np.ndarray, Y: np.ndarray, scale: float, oct_: int = 3):
    Z = np.zeros(X.shape)
    amp, frq, norm = 1.0, 1.0, 0.0
    for _ in range(oct_):
        ox, oy = rng.uniform(-40, 40), rng.uniform(-40, 40)
        Z += amp * _value_noise(X * scale * frq + ox, Y * scale * frq + oy)
        norm += amp
        amp *= 0.5
        frq *= 2.0
    return Z / norm


# ===========================================================================
# stroke helpers
# ===========================================================================
def _dash(poly: Poly, on: float = 2.2, off: float = 1.9, phase: float = 0.0) -> List[Poly]:
    """Split a polyline into ``on`` mm dashes separated by ``off`` mm.

    The phase is an explicit on/off state with a remaining length, never
    ``arclength % period`` — the modulo form lands epsilon below the switch
    point once float error accumulates and the walk never terminates.
    """
    if on <= 0.0:
        return []
    if off <= 1e-9:
        return [list(poly)]
    out: List[Poly] = []
    cur: Poly = []
    period = on + off
    s = phase % period
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


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 72) -> Poly:
    out: Poly = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        out.append((
            m ** 3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
            m ** 3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return out


def _arc(cx: float, cy: float, rx: float, ry: float, a0: float, a1: float, n: int = 120) -> Poly:
    return [
        (cx + rx * math.cos(a0 + (a1 - a0) * k / n), cy + ry * math.sin(a0 + (a1 - a0) * k / n))
        for k in range(n + 1)
    ]


def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _disc(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid dot as a tight spiral plus one rim pass — cannot flood at this size."""
    turns = max(3, int(r / 0.20))
    n = turns * 20
    pts = [
        (x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
         y + r * (k / n) * math.sin(2 * math.pi * turns * k / n))
        for k in range(n + 1)
    ]
    rim = [(x + r * math.cos(2 * math.pi * k / 24), y + r * math.sin(2 * math.pi * k / 24))
           for k in range(25)]
    return _poly(pts, color=pen, f=1600) + _poly(rim, color=pen, f=1600)


def _head(tip: Pt, ang: float, size: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid arrowhead — three hatch passes so it reads as a filled triangle."""
    w = size * 0.42
    bx = tip[0] - size * math.cos(ang)
    by = tip[1] - size * math.sin(ang)
    nx, ny = -math.sin(ang), math.cos(ang)
    a = (bx + w * nx, by + w * ny)
    b = (bx - w * nx, by - w * ny)
    out = _poly([tip, a, b, tip], color=pen, f=1800)
    for t in (0.34, 0.58, 0.80):
        pa = (tip[0] + (a[0] - tip[0]) * t, tip[1] + (a[1] - tip[1]) * t)
        pb = (tip[0] + (b[0] - tip[0]) * t, tip[1] + (b[1] - tip[1]) * t)
        out += _poly([pa, pb], color=pen, f=1800)
    return out


def _head_on(path: Poly, t: float, size: float, pen: Optional[int], back: bool = False):
    """Arrowhead riding a path at fractional arclength ``t``."""
    n = len(path)
    i = max(1, min(n - 1, int(t * (n - 1))))
    dx = path[i][0] - path[i - 1][0]
    dy = path[i][1] - path[i - 1][1]
    ang = math.atan2(dy, dx) + (math.pi if back else 0.0)
    return _head(path[i], ang, size, pen)


def _guard(cmds: List[GCodeCommand], min_dist: float = MIN_PITCH) -> List[GCodeCommand]:
    """``enforce_line_spacing`` + re-emit, so every stroke keeps a leading G0.

    The policy rebuilds strokes and can drop the ``G0`` that positions one; the
    merged program then starts that stroke from the machine origin, which shows
    up as a stray point at (0, 0) and a bounds violation.
    """
    thinned = enforce_line_spacing(cmds, min_dist=min_dist, resample=0.40)
    runs: List[Tuple[Optional[int], Poly]] = []
    cur: Poly = []
    pen: Optional[int] = None
    for c in thinned:
        if c.command == "G0" and c.x is not None:
            if len(cur) >= 2:
                runs.append((pen, cur))
            cur = [(c.x, c.y)]
        elif c.command == "M3":
            pen = c.color if c.color is not None else pen
        elif c.command == "G1" and c.x is not None:
            cur.append((c.x, c.y))
            if c.color is not None:
                pen = c.color
        elif c.command == "M5":
            if len(cur) >= 2:
                runs.append((pen, cur))
            cur = []
    if len(cur) >= 2:
        runs.append((pen, cur))
    out: List[GCodeCommand] = []
    for p, r in runs:
        out += _poly(r, color=p, f=F_DRAW)
    return out


# ===========================================================================
# 1. the ring-filled blobs  (x, z, y, c, x~)
# ===========================================================================
def _ring_blob(
    rng: SeededRNG,
    outline: Poly,
    pen: int,
    pitch: float,
    wobble: float = 0.30,
    detail: bool = True,
    dash: Optional[Tuple[float, float]] = None,
    max_rings: Optional[int] = None,
) -> List[GCodeCommand]:
    """Amoeba filled with concentric rings that follow its own outline.

    The field is the DISTANCE to the boundary: |grad d| = 1 everywhere, so a
    uniform level ladder gives a ring pitch of exactly ``pitch``.  ``detail``
    adds the interior smudges and loose discs that mark PIXEL space; the latent
    nests are drawn without them, which is half of the plate's argument.
    """
    xs_o = [p[0] for p in outline]
    ys_o = [p[1] for p in outline]
    pad = 2.0
    box = (min(xs_o) - pad, min(ys_o) - pad, max(xs_o) + pad, max(ys_o) + pad)
    step = 0.42 if detail else 0.38
    xs, ys, X, Y = _grid(box, step)
    D = _dist_field(outline, X, Y)
    wob = (_fbm(rng, X, Y, 1.0 / 11.0, 3) - 0.5) * 2.0 * (wobble * pitch)
    F = np.where(D > 0, D + wob, 0.0)

    rings: List[GCodeCommand] = []
    dmax = float(F.max())
    k = 1
    while k * pitch < dmax and (max_rings is None or k <= max_rings):
        chains = _iso_chains(F, xs, ys, k * pitch)
        if dash is not None:
            dashed: List[Poly] = []
            for ch in chains:
                dashed += _dash(ch, dash[0], dash[1], phase=1.7 * k)
            rings += _emit(dashed, pen)
        else:
            rings += _emit(chains, pen)
        k += 1

    out = _guard(rings, MIN_PITCH)

    # the boundary is the heaviest line on the blob: a deliberate double pass,
    # drawn AFTER the guard so the 0.26 mm offset survives it
    closed = outline + [outline[0]]
    out += _emit([closed], pen)
    out += _emit([[(px + 0.26, py) for px, py in closed]], pen)

    if detail:
        cx = sum(xs_o) / len(xs_o)
        cy = sum(ys_o) / len(ys_o)
        for _ in range(26):
            px = rng.uniform(box[0], box[2])
            py = rng.uniform(box[1], box[3])
            if not _pt_in_poly(px, py, outline):
                continue
            out += _disc(px, py, rng.choice([0.40, 0.55, 0.75]), pen)
        out += _disc(cx, cy, 1.55, BLACK)
    return out


# ===========================================================================
# 2. the horns — compression drawn as a shape that narrows
# ===========================================================================
def _horn(
    apex: Pt, mouth_x: float, half_h: float, shells: int, pen: int,
    bulge: float = 0.30,
) -> List[GCodeCommand]:
    """A funnel: nested closed curves from a wide mouth converging on one point.

    Shell j is the same curve with the mouth half-height scaled to j/shells, so
    every shell shares the apex.  Drawn once per encoder/decoder; the encoder's
    apex is on the RIGHT (compression), the decoder's on the LEFT (expansion).
    """
    ax, ay = apex
    span = mouth_x - ax
    out: List[GCodeCommand] = []
    for j in range(1, shells + 1):
        h = half_h * j / shells
        b = bulge * h
        top = _bez((ax, ay), (ax + span * 0.30, ay + h * 0.16),
                   (ax + span * 0.72, ay + h * 0.80), (mouth_x, ay + h))
        mouth = _bez((mouth_x, ay + h), (mouth_x - b, ay + h * 0.42),
                     (mouth_x - b, ay - h * 0.42), (mouth_x, ay - h))
        bot = _bez((mouth_x, ay - h), (ax + span * 0.72, ay - h * 0.80),
                   (ax + span * 0.30, ay - h * 0.16), (ax, ay))
        out += _emit([top + mouth[1:] + bot[1:]], pen, f=2000)
    out += _disc(ax, ay, 0.85, pen)
    return out


# ===========================================================================
# 3. the denoiser — the bowtie
# ===========================================================================
_BOW = dict(L=34.0, wy=8.0, sxw=13.0, syw=18.0, Aw=1.0,
            Ac=0.72, scx=4.6, scy=17.0,
            An=0.50, nh=26.0, snx=32.0, sny=13.0,
            Ae=0.40, ex=70.0, esx=12.0, esy=24.0)
_BOW_FLOOR = 0.22
_BOW_SIG = 13.0
_BOW_KX, _BOW_KY = 1.090, 0.945  # coordinate scale onto BOW_HW x BOW_HH


def _bow_field(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Sum of exponential (CONICAL) cusps: four wing masses, one narrow central
    column, two notches carving the waist, two notches tapering the far ends.

    Conical and not Gaussian on purpose: for ``a*exp(-r/sigma)`` the level
    ``PHI = -sigma*log(F)`` is linear in r, so a uniform PHI ladder puts the
    rings a fixed distance apart.  A Gaussian peak spreads its rings exactly at
    the summit, which is where this shape needs them tightest.
    """
    P = _BOW
    U, V = X / _BOW_KX, Y / _BOW_KY
    F = np.zeros(U.shape)
    for sx in (-P["L"], P["L"]):
        for sy in (-P["wy"], P["wy"]):
            F += P["Aw"] * np.exp(-np.hypot((U - sx) / P["sxw"], (V - sy) / P["syw"]))
    F += P["Ac"] * np.exp(-np.hypot(U / P["scx"], V / P["scy"]))
    for sy in (-P["nh"], P["nh"]):
        F -= P["An"] * np.exp(-np.hypot(U / P["snx"], (V - sy) / P["sny"]))
    for sx in (-P["ex"], P["ex"]):
        F -= P["Ae"] * np.exp(-np.hypot((U - sx) / P["esx"], V / P["esy"]))
    return F


def _bowtie(cx: float, cy: float) -> Tuple[List[GCodeCommand], Poly, List[Pt]]:
    """Returns (commands, outer silhouette, the three eyes)."""
    xs, ys, X, Y = _grid((cx - BOW_HW - 4, cy - BOW_HH - 4,
                          cx + BOW_HW + 4, cy + BOW_HH + 4), 0.44)
    F = _bow_field(X - cx, Y - cy)
    PHI = np.where(F > 0, -_BOW_SIG * np.log(np.clip(F, 1e-9, None)), 1e6)
    p0 = -_BOW_SIG * math.log(_BOW_FLOOR)

    rings: List[GCodeCommand] = []
    silhouette: Poly = []
    for k in range(BOW_RINGS):
        chains = _iso_chains(-PHI, xs, ys, -(p0 - BOW_PITCH * k))
        if k == 0 and chains:
            silhouette = max(chains, key=len)
        rings += _emit(chains, BLACK, f=2000)
    out = _guard(rings, MIN_PITCH)

    # the three eyes: central maximum and the two wing ridges' waists
    eyes = [(cx, cy),
            (cx - _BOW["L"] * _BOW_KX * 0.60, cy),
            (cx + _BOW["L"] * _BOW_KX * 0.60, cy)]
    out += _disc(eyes[0][0], eyes[0][1], 1.9, BLACK)
    for ex, ey in eyes[1:]:
        out += _disc(ex, ey, 0.85, BLACK)
    return out, silhouette, eyes


def _bow_top_at(sil: Poly, x: float, cy: float) -> float:
    """Highest silhouette point (smallest y, since v runs down the sheet) at x."""
    band = [p[1] for p in sil if abs(p[0] - x) < 1.4 and p[1] > cy]
    return max(band) if band else cy + BOW_HH * 0.4


def _bow_bot_at(sil: Poly, x: float, cy: float) -> float:
    band = [p[1] for p in sil if abs(p[0] - x) < 1.4 and p[1] < cy]
    return min(band) if band else cy - BOW_HH * 0.4


# ===========================================================================
# 4. the forward row — one state
# ===========================================================================
def _state(
    rng: SeededRNG, cx: float, cy: float, u: float,
    base: Poly, knockouts: Sequence[Bounds],
) -> List[GCodeCommand]:
    """One z_t: surviving ochre rings + the isotropic cloud taking over.

    Every decision is the noise-to-signal ratio ``w`` and nothing else:
        duty   = 1/(1+w^2)            rings survive while they do not collide
        rings  = round(7 * duty)
        cloud  = 470 * (1-abar)^0.7   dots
        sigma  = R * (0.34 + 0.62*min(1,w))
        pen    = GOLD with probability sqrt(abar), else BLACK
        shape  = sqrt(abar) of the cloud inside the blob, the rest isotropic
    """
    ab = _abar(u)
    sq = math.sqrt(max(0.0, ab))
    w = _nsr(u)
    duty = 0.0 if math.isinf(w) else 1.0 / (1.0 + w * w)
    n_rings = int(round(7 * duty))
    R = (Z_RX + Z_RY) / 2.0

    out: List[GCodeCommand] = []

    if n_rings >= 1:
        shrink = 0.80 + 0.20 * sq  # the signal is scaled by sqrt(abar_t)
        poly = [(cx + (p[0] - cx) * shrink, cy + (p[1] - cy) * shrink) for p in base]
        pitch = max(MIN_PITCH + 0.3, 1.45)
        on = max(0.7, 9.0 * duty ** 1.6)
        off = 0.0 if duty > 0.97 else max(0.7, 2.6 * (1.0 - duty))
        out += _ring_blob(
            rng, poly, GOLD, pitch,
            wobble=min(1.4, 0.25 + 0.9 * (0.0 if math.isinf(w) else w)),
            detail=False,
            dash=None if off <= 0.0 else (on, off),
            max_rings=n_rings,
        )

    n_dots = int(round(470 * max(0.0, 1.0 - ab) ** 0.7))
    sigma = R * (0.34 + 0.62 * min(1.0, 0.0 if math.isinf(w) else w if w < 1 else 1.0))
    if math.isinf(w):
        sigma = R * 0.96
    struct = sq  # fraction of the cloud that still knows the shape

    def blocked(px: float, py: float) -> bool:
        for bx0, by0, bx1, by1 in knockouts:
            if bx0 <= px <= bx1 and by0 <= py <= by1:
                return True
        return False

    for _ in range(n_dots):
        if rng.random() < struct:
            for _try in range(12):
                px = cx + rng.uniform(-Z_RX, Z_RX) * 1.05
                py = cy + rng.uniform(-Z_RY, Z_RY) * 1.05
                if _pt_in_poly(px, py, base):
                    break
            else:
                continue
        else:
            a = rng.uniform(0, 2 * math.pi)
            rr = abs(rng.gauss(0.0, 1.0)) * sigma
            if rr > 2.9 * sigma:
                continue
            px, py = cx + rr * math.cos(a), cy + rr * math.sin(a) * 0.94
        if blocked(px, py):
            continue
        pen = GOLD if rng.random() < sq else BLACK
        r = rng.choice([0.28, 0.28, 0.34, 0.44])
        if r > 0.40:
            out += _disc(px, py, r, pen)
        else:
            out += _dot(px, py, r=r, color=pen, f=1600)

    out += _disc(cx, cy, 1.45, BLACK)
    return out


# ===========================================================================
# 5. furniture
# ===========================================================================
def _plus(x: float, y: float, s: float, pen: int) -> List[GCodeCommand]:
    return _poly([(x - s, y), (x + s, y)], color=pen, f=2300) + _poly(
        [(x, y - s), (x, y + s)], color=pen, f=2300
    )


def _dots3(cx: float, cy: float, gap: float, pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for k in (-1, 0, 1):
        out += _disc(cx + k * gap, cy, 0.62, pen)
    return out


# ===========================================================================
# entry point
# ===========================================================================
def stable_diffusion(rng: SeededRNG, bounds, colors: int = 4) -> List[GCodeCommand]:
    fr = Frame(bounds)
    P = fr.p
    out: List[GCodeCommand] = []

    def mmx(mm: float) -> float:
        return fr.du(mm)

    def mmy(mm: float) -> float:
        return fr.dv(mm)

    # ---------------------------------------------------------------- pens
    def pen(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    K, Rd, G, Bl = pen(BLACK), pen(RED), pen(GOLD), pen(BLUE)

    # =================================================================
    # corner sweeps + registration, laid down first so everything crosses them
    # =================================================================
    for (ccu, ccv, r_mm, a0, a1) in (
        (0.255, -0.30, 115.0, 1.55, 2.62),
        (0.815, -0.22, 96.0, 0.52, 1.60),
        (0.205, 1.28, 104.0, 3.80, 4.75),
        (0.775, 1.30, 120.0, 4.72, 5.74),
    ):
        ccx, ccy = P(ccu, ccv)
        pth = _arc(ccx, ccy, r_mm, r_mm, a0, a1, 200)
        pth = [p for p in pth if fr.x0 <= p[0] <= fr.x1 and fr.y0 <= p[1] <= fr.y1]
        if len(pth) >= 2:
            out += _emit(_dash(pth, 4.2, 3.0), K, f=2400)

    for (pu, pv, ps) in (
        (0.268, 0.100, 3.0), (0.806, 0.166, 3.4), (0.222, 0.470, 2.6),
        (0.548, 0.930, 3.0), (0.938, 0.762, 3.2), (0.086, 0.556, 2.4),
        (0.690, 0.905, 2.4),
    ):
        px, py = P(pu, pv)
        out += _plus(px, py, ps, K)

    for (ru, rv, rl, vert) in (
        (0.646, 0.030, 16.0, True), (0.352, 0.975, 13.0, True),
        (0.884, 0.058, 11.0, True), (0.128, 0.962, 10.0, True),
        (0.742, 0.470, 12.0, False), (0.196, 0.372, 9.0, False),
    ):
        rx, ry = P(ru, rv)
        seg = [(rx, ry - rl / 2), (rx, ry + rl / 2)] if vert else [(rx - rl / 2, ry), (rx + rl / 2, ry)]
        out += _emit(_dash(seg, 2.0, 1.8), K, f=2400)

    for _ in range(16):
        du_ = rng.uniform(0.02, 0.98)
        dv_ = rng.uniform(0.02, 0.98)
        dx, dy = P(du_, dv_)
        out += _disc(dx, dy, rng.choice([0.48, 0.62, 0.80]), K)

    # =================================================================
    # the denoiser first: everything else docks onto its silhouette
    # =================================================================
    ex_c, ey_c = P(*EPS_C)
    bow_cmds, sil, eyes = _bowtie(ex_c, ey_c)

    # =================================================================
    # left: pixel space -> encoder -> latent
    # =================================================================
    x_poly = _place(_amoeba(X_HARM), *P(*X_C), X_RX, X_RY)
    out += _ring_blob(rng, x_poly, Rd, 0.98, wobble=0.30, detail=True)

    e_apex = P(E_APEX_U, ROW_V)
    e_mouth_x = fr.u(E_MOUTH_U)
    out += _horn(e_apex, e_mouth_x, HORN_HALF_H, 13, K)

    # red tendrils: pixel space spilling from x into the encoder's mouth
    xr = fr.u(X_C[0]) + X_RX
    for j in range(5):
        t = (j - 2) / 2.0
        a = (xr - 2.0, fr.v(ROW_V) + t * X_RY * 0.72)
        b = (e_mouth_x + 1.5, fr.v(ROW_V) + t * HORN_HALF_H * 0.80)
        pth = _bez(a, (a[0] + 9, a[1] + t * 5), (b[0] - 11, b[1] + t * 5), b)
        out += _emit(_dash(pth, 2.6, 2.0, phase=1.1 * j), Rd, f=2300)

    # apex -> z0: the compressed code, one solid line
    z_base = _amoeba(Z_HARM)
    z0_c = P(ROW_U[0], ROW_V)
    out += _emit([[e_apex, (z0_c[0] - Z_RX * 0.92, z0_c[1])]], K, f=2200)

    # =================================================================
    # the forward row
    # =================================================================
    row_y = fr.v(ROW_V)
    ell_boxes: List[Bounds] = []
    for k in range(N_STATES - 1):
        mx = fr.u((ROW_U[k] + ROW_U[k + 1]) / 2.0)
        ell_boxes.append((mx - 6.5, row_y - 3.4, mx + 6.5, row_y + 3.4))

    state_polys: List[Poly] = []
    for k in range(N_STATES):
        cx, cy = P(ROW_U[k], ROW_V)
        poly = _place(_amoeba(Z_HARM), cx, cy, Z_RX, Z_RY)
        state_polys.append(poly)
        out += _state(rng, cx, cy, k / (N_STATES - 1), poly, ell_boxes)

    for bx0, by0, bx1, by1 in ell_boxes:
        out += _dots3((bx0 + bx1) / 2.0, (by0 + by1) / 2.0, 2.6, K)

    # the row's own axis, a dotted rule through every state
    axis = [(fr.u(ROW_U[0]) - Z_RX - 5.0, row_y), (fr.u(ROW_U[-1]) + Z_RX + 6.0, row_y)]
    out += _emit(_dash(axis, 0.9, 3.4), K, f=2400)

    # q(z_t | z_{t-1}) caption + its dotted arrow
    q_parts = [("r", "q("), ("r", "z"), ("sub", "t"), ("r", " | "), ("r", "z"),
               ("sub", "t"), ("r", "-"), ("sub", "1"), ("r", ")")]
    out += _math(q_parts, fr.v(Q_V), Q_CAP, K, centre=fr.u(0.512))
    qa = [P(Q_ARROW_U[0], Q_ARROW_V), P(Q_ARROW_U[1], Q_ARROW_V)]
    out += _emit(_dash(qa, 1.0, 2.4), K, f=2400)
    out += _head(qa[1], 0.0, 3.4, K)

    # the transition swoops: one dotted arc per q(z_t | z_{t-1}) step
    for k in range(N_STATES - 1):
        a = P(ROW_U[k], ROW_V - mmy(Z_RY * 0.55))
        b = P(ROW_U[k + 1], ROW_V - mmy(Z_RY * 0.55))
        top = fr.v(0.196 - 0.004 * k)
        pth = _bez(a, (a[0] + 4, top), (b[0] - 4, top), b)
        out += _emit(_dash(pth, 1.0, 2.6, phase=0.7 * k), K, f=2400)
        out += _head_on(pth, 0.96, 3.0, K)

    # =================================================================
    # droplines: every state feeds the network
    # =================================================================
    for k in range(N_STATES):
        sx = fr.u(ROW_U[k])
        top_y = row_y - Z_RY - 2.6
        if fr.u(0.360) <= sx <= fr.u(0.640):
            land = _bow_top_at(sil, sx, ey_c) + 0.6
            pth = [(sx, top_y), (sx, land)]
            bold = abs(sx - ex_c) < mmx(0.0) + fr.w * 0.055
            if bold:
                out += _emit([pth], K, f=2200)
                out += _emit([[(p[0] + 1.5, p[1]) for p in pth]], K, f=2200)
                out += _head((sx, land), -math.pi / 2, 4.6, K)
            else:
                out += _emit(_dash(pth, 1.0, 2.4), K, f=2400)
                out += _head((sx, land), -math.pi / 2, 3.4, K)
        else:
            inward = 1.0 if sx < ex_c else -1.0
            tx = ex_c - inward * fr.w * 0.115
            land = _bow_top_at(sil, tx, ey_c) + 0.6
            a = (sx, top_y)
            b = (tx, land)
            pth = _bez(a, (a[0], a[1] - 26), (b[0] - inward * 30, b[1] - 24), b)
            out += _emit(_dash(pth, 1.0, 2.6), K, f=2400)
            out += _head_on(pth, 0.985, 3.4, K)

    out += bow_cmds

    # eps_theta, seated in the clear paper above the waist
    eps_parts = [("r", "ε"), ("sub", "θ")]
    out += _math(eps_parts, fr.v(0.470), 7.2, K, centre=ex_c)

    # =================================================================
    # t — the timestep, a solid arrow into the left tip
    # =================================================================
    tx0, ty = P(0.236, DOCK_T[1])
    tx1 = fr.u(DOCK_T[0])
    out += _disc(tx0, ty, 1.35, K)
    out += _emit([[(tx0 + 2.2, ty), (tx1 - 4.4, ty)]], K, f=2200)
    out += _head((tx1, ty), 0.0, 4.4, K)
    out += _tracked("t", tx0 - 6.6, ty - 2.4, 6.4, K)

    # =================================================================
    # conditioning: y -> tau_theta -> c -> the network's lower-left flank
    # =================================================================
    y_poly = _place(_amoeba(Y_HARM), *P(*Y_C), Y_RX, Y_RY)
    out += _ring_blob(rng, y_poly, Bl, 1.05, wobble=0.32, detail=True)

    t_apex = P(T_APEX_U, COND_V)
    t_mouth_x = fr.u(T_MOUTH_U)
    out += _horn(t_apex, t_mouth_x, HORN_HALF_H, 13, K)

    yr = fr.u(Y_C[0]) + Y_RX
    for j in range(6):
        t = (j - 2.5) / 2.5
        a = (yr - 3.0, fr.v(COND_V) + t * Y_RY * 0.78)
        b = (t_mouth_x + 1.5, fr.v(COND_V) + t * HORN_HALF_H * 0.82)
        pth = _bez(a, (a[0] + 10, a[1] + t * 4), (b[0] - 12, b[1] + t * 6), b)
        if j % 2:
            out += _emit(_dash(pth, 2.4, 1.9, phase=1.3 * j), Bl, f=2300)
        else:
            out += _emit([pth], Bl, f=2300)
            out += _head_on(pth, 0.97, 3.2, Bl)

    c_poly = _place(_amoeba(C_HARM), *P(*C_C), C_RX, C_RY)
    out += _emit([[t_apex, (fr.u(C_C[0]) - C_RX * 0.9, fr.v(COND_V))]], K, f=2200)
    out += _ring_blob(rng, c_poly, Bl, 1.0, wobble=0.28, detail=False)
    out += _disc(fr.u(C_C[0]), fr.v(COND_V), 1.3, BLACK)

    # the sheaf into DOCK_C — dashed, because conditioning is a different
    # kind of input from the latent
    cxr = fr.u(C_C[0]) + C_RX
    dcx, dcy = P(*DOCK_C)
    for j in range(6):
        t = (j - 2.5) / 2.5
        a = (cxr + 1.0, fr.v(COND_V) + t * C_RY * 0.85)
        b = (dcx - 1.0 + t * 1.4, dcy + t * 4.6)
        pth = _bez(a, (a[0] + 16, a[1] + 1.0), (b[0] - 15, b[1] - 12 - 3 * t), b)
        if j % 2:
            out += _emit(_dash(pth, 3.0, 2.2, phase=1.6 * j), Bl, f=2300)
        else:
            out += _emit([pth], Bl, f=2300)
        out += _head_on(pth, 0.975, 3.4, Bl)

    # =================================================================
    # the sampling loop — ONE circulation, out of the waist and back in
    # =================================================================
    out_x = ex_c
    out_y0 = _bow_bot_at(sil, out_x, ey_c) - 0.8
    out_y1 = fr.v(0.745)
    out += _emit(_dash([(out_x, out_y0), (out_x, out_y1 + 4.4)], 1.1, 2.2), K, f=2400)
    out += _head((out_x, out_y1 + 1.4), -math.pi / 2, 4.2, K)
    jx, jy = out_x, out_y1 - 1.0
    out += _disc(jx, jy, 1.5, G)

    lcx, lcy = P(*LOOP_C)
    dock_x, dock_y = P(*DOCK_LOOP)
    for j in range(3):
        rx = fr.w * LOOP_RX[j]
        ry = fr.h * LOOP_RY[j]
        # v runs DOWN the sheet, so "below" is -y on the plotter
        pth = _arc(lcx, lcy, rx, ry, -0.16, -math.pi + 0.16, 150)
        pth = [(px, lcy - (py - lcy)) for px, py in pth]  # mirror to below
        # pull the two ends onto the network's underside
        n = len(pth)
        a_end = (dock_x + j * 3.0, dock_y)
        pth = pth[:-1] + [a_end]
        b_end = (out_x + 6.0 + j * 3.0, _bow_bot_at(sil, out_x + 6.0 + j * 3.0, ey_c) - 0.4)
        pth = [b_end] + pth[1:]
        out += _emit([pth], G, f=2200)
        out += _head_on(pth, 0.52, 4.0, G)          # travelling left
        out += _head_on(pth, 0.985, 4.0, G)         # entering the network
        if j == 0:
            out += _emit([[(jx, jy), (b_end[0], b_end[1])]], G, f=2200)

    # z_{t-1}, below the outermost arc, inside the loop's own quiet zone
    z_parts = [("r", "z"), ("sub", "t"), ("r", "-"), ("sub", "1")]
    zw = _math_w(z_parts, 6.4)
    out += _math(z_parts, fr.v(ZTM1_V), 6.4, K, centre=lcx)
    out += _dots3(lcx - zw / 2.0 - 12.0, fr.v(ZTM1_V) + 2.0, 2.8, K)
    out += _dots3(lcx + zw / 2.0 + 12.0, fr.v(ZTM1_V) + 2.0, 2.8, K)

    # =================================================================
    # exit to the decoder: after T passes the loop lets go
    # =================================================================
    zr_c = P(*ZR_C)
    exit_a = (ex_c + fr.w * 0.118, fr.v(0.742))
    exit_b = (zr_c[0] - Z_RX - 3.0, zr_c[1])
    e_pth = _bez(exit_a, (exit_a[0] + 30, exit_a[1] + 2), (exit_b[0] - 22, exit_b[1] - 24), exit_b)
    out += _emit([e_pth], G, f=2200)
    out += _head_on(e_pth, 0.985, 4.2, G)
    ghost = _bez((exit_a[0] - 3, exit_a[1] - 4.5), (exit_a[0] + 30, exit_a[1] - 3),
                 (exit_b[0] - 22, exit_b[1] - 29), (exit_b[0] - 1, exit_b[1] - 5.0))
    out += _emit(_dash(ghost, 3.0, 2.4), G, f=2400)

    # =================================================================
    # right: latent -> decoder -> pixel space
    # =================================================================
    zr_poly = _place(_amoeba(_bandlimit(Z_HARM, K_CUTOFF, 0.03)), *zr_c, Z_RX, Z_RY)
    out += _ring_blob(rng, zr_poly, G, 1.45, wobble=0.28, detail=False, max_rings=7)
    out += _disc(zr_c[0], zr_c[1], 1.45, BLACK)

    d_apex = P(D_APEX_U, DEC_V)
    d_mouth_x = fr.u(D_MOUTH_U)
    out += _horn(d_apex, d_mouth_x, HORN_HALF_H, 13, K)
    out += _emit([[(zr_c[0] + Z_RX * 0.92, zr_c[1]), d_apex]], K, f=2200)

    xt_poly = _place(_amoeba(_bandlimit(X_HARM)), *P(*XT_C), X_RX, X_RY)
    out += _ring_blob(rng, xt_poly, Rd, 0.98, wobble=0.30, detail=True)

    xtl = fr.u(XT_C[0]) - X_RX
    for j in range(5):
        t = (j - 2) / 2.0
        a = (d_mouth_x - 1.5, fr.v(DEC_V) + t * HORN_HALF_H * 0.80)
        b = (xtl + 2.0, fr.v(DEC_V) + t * X_RY * 0.72)
        pth = _bez(a, (a[0] + 11, a[1] + t * 5), (b[0] - 9, b[1] + t * 5), b)
        out += _emit(_dash(pth, 2.6, 2.0, phase=1.1 * j), Rd, f=2300)
        out += _head_on(pth, 0.96, 3.0, Rd)

    # =================================================================
    # labels
    # =================================================================
    def lab(txt: str, u: float, v: float, cap: float, p: Optional[int], sub: str = ""):
        parts: List[Tuple[str, str]] = [("r", txt)]
        if sub:
            parts.append(("sub", sub))
        return _math(parts, fr.v(v), cap, p, left=fr.u(u))

    out += lab("x", X_C[0] - mmx(X_RX) - mmx(9.0), ROW_V + mmy(10.0), 7.0, K)
    out += _tracked("E", fr.u(0.184), fr.v(ROW_V) - 2.6, 7.4, K)
    out += lab("z", ROW_U[0] - mmx(3.0), ROW_V + mmy(Z_RY) + mmy(6.4), 5.8, K, sub="0")
    out += lab("z", ROW_U[2] + mmx(Z_RX) + mmx(4.0), ROW_V + mmy(Z_RY) + mmy(2.0), 5.8, K, sub="t")
    out += lab("z", ROW_U[5] - mmx(2.0), ROW_V + mmy(Z_RY) + mmy(8.4), 5.8, K, sub="T")
    out += lab("y", Y_C[0] - mmx(Y_RX) - mmx(9.0), COND_V + mmy(11.0), 7.0, K)
    out += _math([("tau", ""), ("sub", "θ")], fr.v(COND_V) - 2.2, 6.6, K,
                 left=fr.u(0.178))
    out += lab("c", C_C[0] - mmx(1.0), COND_V + mmy(C_RY) + mmy(6.0), 6.4, K)
    out += lab("z", ZR_C[0] - mmx(3.0), DEC_V + mmy(Z_RY) + mmy(6.4), 5.8, K, sub="0")
    out += _tracked("D", fr.u(0.816), fr.v(DEC_V) - 2.8, 7.4, K)
    xt_lab_x = fr.u(XT_C[0]) + X_RX + 5.0
    out += _tracked("x", xt_lab_x, fr.v(DEC_V + mmy(10.0)) - 0.0, 7.0, K)
    out += _tilde_over(xt_lab_x + _tw("x", 7.0) * 0.44, fr.v(DEC_V + mmy(10.0)), 7.0, K)

    # =================================================================
    # type
    # =================================================================
    out += _text_at("STABLE DIFFUSION", fr.v(TITLE_V[0]), TITLE_CAP, K,
                    left=fr.u(TITLE_U), target_w=TITLE_W)
    out += _text_at("AS TOPOGRAPHY", fr.v(TITLE_V[1]), TITLE_CAP, K,
                    left=fr.u(TITLE_U), target_w=TITLE_W * 0.80)
    rule_y = fr.v(TITLE_V[1] + 0.020)
    out += _emit([[(fr.u(TITLE_U), rule_y), (fr.u(TITLE_U) + TITLE_W, rule_y)]], K, f=2300)

    for txt, vv in zip(("NOISE", "CONDITION", "DENOISE", "GENERATE"), FOOT_L_V):
        out += _text_at(txt, fr.v(vv), FOOT_CAP, K, left=fr.u(FOOT_L_U), target_w=26.0)
    for txt, vv in zip(("IMAGES", "THROUGH", "LATENT", "LANDSCAPES"), FOOT_R_V):
        out += _text_at(txt, fr.v(vv), FOOT_CAP, K, right=fr.u(FOOT_R_U), target_w=30.0)

    # =================================================================
    # bounds guard — nothing may leave the drawable area
    # =================================================================
    bx0, by0, bx1, by1 = bounds
    clipped = 0
    for c in out:
        if c.x is not None:
            nx = min(max(c.x, bx0 + 0.2), bx1 - 0.2)
            ny = min(max(c.y, by0 + 0.2), by1 - 0.2)
            if abs(nx - c.x) > 1e-6 or abs(ny - c.y) > 1e-6:
                clipped += 1
            c.x, c.y = nx, ny
    if clipped:
        logger.warning("stable_diffusion: %d points clamped to the drawable area", clipped)
    logger.info("stable_diffusion: %d commands", len(out))
    return out
