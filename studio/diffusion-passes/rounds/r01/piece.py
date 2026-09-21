"""DIFFUSION — FORWARD, NETWORK, REVERSE.  Faithful recreation, r01.

Reproduction of ``studio/diffusion-passes/ref/reference.png`` (1510x1041,
ratio 1.451 -> A3 landscape, drawable 400x277 = 1.444) as three horizontal
registers: the top destroys, the bottom rebuilds, and the band between them
is the only learned thing on the sheet.

Every element's position was MEASURED off the raster (paper/ink mask, row
bands, per-band column runs) and is recorded below in normalised frame
coordinates ``(u, v)``, u = 0 left .. 1 right, v = 0 TOP .. 1 bottom.

WHAT IS EXACT (not eyeballed)
-----------------------------
1. ``abar_t`` is the real cosine schedule (Nichol & Dhariwal 2021, s = 0.008)
   sampled at t/T = 0, .2, .4, .6, .8, 1.  sqrt(abar) = 1.000, 0.948, 0.805,
   0.585, 0.308, 0.000 — the collapse is LATE AND FAST, which is the whole
   point of the row and cannot be got by spacing "noisiness" by eye.
2. Each state draws ``x_t = sqrt(abar_t) x_0 + sqrt(1-abar_t) sigma e`` as its
   two terms.  The SIGNAL is the level sets of ``sqrt(abar) x_0``: scaling a
   field's values never moves its contours, so the nest keeps its size and
   its column, and pays the attenuation in contrast instead — the ladder is
   decimated (1, 1, 2, 3, 5, gone) as rings stop clearing the noise's level
   spread, and what survives is drawn at duty ``abar`` (1.00, .90, .65, .34,
   .09).  The NOISE is ``e`` itself, as isotropic speckle (0, 51, 205, 420,
   595, 700 dots).  One x_0 and one e serve a whole row, so the six states
   are one trajectory, not six unrelated drawings.
3. ``sigma`` is set to the data's own per-axis RMS spread.  That makes the
   process VARIANCE-PRESERVING, which is why every state occupies the same
   footprint without a fudge factor: Var = abar*Var(x_0) + (1-abar)*sigma^2
   = Var(x_0) for all t.
4. At abar = 0 the signal term is gone entirely and only the speckle is left,
   so ``x_T`` is an i.i.d. Gaussian sample — genuinely ISOTROPIC, no residual
   lobe, no preferred direction.  The silhouette gets a duty FLOOR because it
   is the highest-contrast contour on the form (its level jump is the whole
   field, not one ladder step), which is why a lobed outline is still legible
   inside the cloud at x_t3 and x_t4.
5. The U-Net's four resolution levels halve: measured bulge half-heights on
   the reference are 107 : 62 : 33 : 17 px = 1 : .58 : .31 : .16.  The piece
   uses 1 : .58 : .30 : .155 and a tiny waist at .075.

FIXES TO THE REFERENCE (the rubric's "OVERLAP IS A DECISION" outranks fidelity)
------------------------------------------------------------------------------
a. COLUMN REGISTRATION.  The reference's reverse row runs its colour ramp
   backwards (black, red, pink, purple, blue) and puts x_T at u 0.824 while
   the forward x_T is at u 0.905, so no state sits above its counterpart.
   Here both rows share ONE six-column grid and ONE ramp direction: column k
   carries the same t in both rows, so the plate's argument — "the same
   sequence in opposite directions" — is readable by looking straight down.
   Only the direction of TRAVEL differs, and that is carried by the arrows.
b. A right SIDEBAR (u 0.862..0.985) is reserved for the two keyword stacks
   and the loss.  In the reference the bottom stack and the bottom x_T fight
   over the same 14 mm.
c. The U-Net title, the skip-arc bundle and the "skip connections" label get
   three separate horizontal bands.  In the reference the title overlaps the
   bowtie and the label sits inside the tube.
d. The reverse-process formula and the bottom-row state labels are on
   separate baselines; in the reference the formula runs through the x_t3
   blob.
e. State gaps go from 0.10 x D (reference) to 0.28 x D.

PLOTTABILITY
------------
Contour nests are level sets of a DISTANCE field (|grad d| = 1), so a uniform
level ladder gives a ring pitch of exactly ``RING_PITCH`` everywhere — the
rubric's "contour levels by gradient" rule, for free.  The bowtie uses dyadic
LOD on the streamline family so the perpendicular gap never falls under
``MIN_GAP``: in the bells every line is drawn, at the waist only every 16th,
which is also why the waist reads as the bottleneck.

Pens (``colors = 5``): 0 black, 1 dodgerblue, 2 mediumpurple,
3 palevioletred, 4 crimson.  Black is structure, type, furniture, the clean
x_0 and the isotropic x_T; the t-ramp blue->purple->pink->red is the time
axis and runs left-to-right in all three registers.

Entry point: ``diffusion_passes``.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.policies import enforce_line_spacing
from promptplot.generative.generators import (
    _GLYPHS,
    _chain_segments,
    _glyph_advance,
    _poly,
    _stroke_text,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

# --- pens ------------------------------------------------------------------
BLACK, BLUE, PURPLE, PINK, RED = 0, 1, 2, 3, 4
RAMP = (BLACK, BLUE, PURPLE, PINK, RED, BLACK)  # the six state columns

F_DRAW = 2200
F_TYPE = 2400

RING_PITCH = 0.80   # mm between contour rings of a clean state
MIN_GAP = 0.80      # mm — plotting floor used by the bowtie LOD + the guard
FRAME_INSET = 3.0


# ===========================================================================
# frame
# ===========================================================================
class Frame:
    """Normalised (u, v) -> sheet mm.  v = 0 is the TOP edge."""

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
# measured layout  (normalised; reference px in the comments)
# ===========================================================================
# six state columns.  The reference's are at u .105 .268 .427 .589 .750 .905
# with only a 0.10 x D gap and x_T 13 mm off the right edge; the grid below
# keeps the pitch but pulls the band left so the sidebar can exist.
COL_U = (0.0900, 0.2294, 0.3688, 0.5082, 0.6476, 0.7870)
STATE_D = 40.0          # mm, form diameter (reference 58 top / 43 bottom)
SEP_GAP = 0.28          # "..." separator sits here, as a fraction of the pitch

SIDEBAR_L, SIDEBAR_R = 0.869, 0.980

# --- header ---------------------------------------------------------------
TITLE_V, TITLE_CAP, TITLE_W = 0.0230, 4.20, 50.0      # px y 28..43, x 28..214
SUB_V = (0.0520, 0.0725, 0.0930)
SUB_CAP = 2.65
KWA_V0, KW_PITCH, KW_CAP = 0.0290, 0.0205, 2.80       # px y 36..104
FWD_LBL_V, FWD_ARR_V, FWD_MATH_V = 0.0620, 0.0765, 0.1035
HDR_CAP = 2.85

# --- top register ---------------------------------------------------------
TOPLBL_V, LBL_CAP = 0.1400, 2.90
TOPFORM_TOP = 0.1510
CAP1_V, CAP2_V, CAP_CAP = 0.3230, 0.3470, 2.30
AXIS_V = 0.3690
AXIS_U = (0.1020, 0.8300)

# --- U-Net ----------------------------------------------------------------
UNET1_V, UNET1_CAP = 0.3920, 3.60
UNET2_V, UNET2_CAP = 0.4150, 2.30
SKIP_LBL_V = 0.4390
BOWTIE_V = 0.5870
BOWTIE_H = 27.0         # mm half-height at the bell (reference 29)
XT_IN_U = 0.1300
EPS_OUT_U = 0.7180
LOSS_RULE_U = 0.8680
LOSS_V = 0.5870

# --- reverse register -----------------------------------------------------
REV_LBL_V, REV_ARR_V, REV_MATH_V = 0.7060, 0.7205, 0.7480
BOTLBL_V = 0.7760
BOTFORM_TOP = 0.7870
BCAP1_V, BCAP2_V = 0.9480, 0.9720
KWB_V0 = 0.8880
FOOT_V, FOOT_CAP = 0.9930, 3.00

# --- copy -----------------------------------------------------------------
KW_TOP = ("noise", "schedules", "score matching", "denoising", "generative sampling")
KW_BOT = (
    "latent diffusion",
    "text conditioning",
    "classifier-free guidance",
    "high-dimensional data",
    "iterative refinement",
)
STATE_LABELS = ("x_{0}", "x_{t1}", "x_{t2}", "x_{t3}", "x_{t4}", "x_{T}")


# ===========================================================================
# the cosine noise schedule (Nichol & Dhariwal 2021, "Improved DDPM", eq. 17)
# ===========================================================================
COS_S = 0.008


def alpha_bar(tf: float) -> float:
    """abar at t/T = ``tf``.  f(t)/f(0) with f = cos^2(((t+s)/(1+s)) pi/2)."""

    def f(u: float) -> float:
        return math.cos(((u + COS_S) / (1.0 + COS_S)) * math.pi / 2.0) ** 2

    return max(0.0, f(tf) / f(0.0))


T_FRACS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
ABAR = tuple(alpha_bar(t) for t in T_FRACS)


# ===========================================================================
# math typesetting
# ===========================================================================
# The shared 88-glyph font has no alpha, mu, radical, script N/E/L, norm bars
# or brackets, so every formula on this plate would silently lose characters.
# These are LOCAL strokes in the same 4x6 glyph metric (caps 0..6, x-height
# 0..4), not an edit to the shared table — the font gap is logged in NOTES.md.
def _arc(cx, cy, rx, ry, a0, a1, n=44) -> Poly:
    return [
        (cx + rx * math.cos(a0 + (a1 - a0) * k / n), cy + ry * math.sin(a0 + (a1 - a0) * k / n))
        for k in range(n + 1)
    ]


_RAD = math.radians
_ALPHA: List[Poly] = [_arc(1.70, 2.00, 1.45, 1.95, _RAD(62), _RAD(62 + 320)) + [(3.55, -0.05)]]
_ALPHA_BAR: List[Poly] = _ALPHA + [[(0.15, 5.05), (3.45, 5.05)]]
_MU: List[Poly] = [
    [(0.55, 4.00), (0.55, -1.60)],
    [(0.55, 1.05), (0.95, 0.25), (1.75, 0.00), (2.55, 0.35), (2.98, 1.10), (2.98, 4.00)],
    [(2.98, 1.30), (3.55, 0.35)],
]
_SCRIPT_N: List[Poly] = [
    [(0.10, 0.00), (0.10, 5.00), (0.48, 5.62), (1.00, 5.48)],
    [(0.10, 5.00), (3.15, 0.38)],
    [(3.15, 0.00), (3.15, 5.00), (3.55, 5.58), (4.05, 5.42)],
    [(0.62, 0.20), (0.62, 4.55)],
]
_BB_E: List[Poly] = [
    [(0.35, 0.00), (0.35, 6.00)],
    [(0.82, 0.00), (0.82, 6.00)],
    [(0.35, 6.00), (3.50, 6.00)],
    [(0.82, 3.15), (2.85, 3.15)],
    [(0.35, 0.00), (3.50, 0.00)],
]
_SCRIPT_L: List[Poly] = [
    [
        (3.55, 5.25), (3.05, 6.00), (2.25, 6.05), (1.78, 5.50), (1.78, 4.60),
        (2.22, 3.40), (2.62, 2.20), (2.60, 1.20), (2.08, 0.32), (1.20, 0.08), (0.35, 0.50),
    ],
    [(0.50, 1.55), (1.40, 2.20), (2.50, 2.72), (3.55, 2.85)],
]
_NORM: List[Poly] = [[(1.20, -0.90), (1.20, 5.40)], [(2.20, -0.90), (2.20, 5.40)]]
_ARROW_R: List[Poly] = [[(0.10, 2.00), (3.90, 2.00)], [(3.00, 2.78), (3.90, 2.00), (3.00, 1.22)]]
_ARROW_L: List[Poly] = [[(0.10, 2.00), (3.90, 2.00)], [(1.00, 2.78), (0.10, 2.00), (1.00, 1.22)]]
_LBRK: List[Poly] = [[(3.10, 6.20), (1.55, 6.20), (1.55, -1.00), (3.10, -1.00)]]
_RBRK: List[Poly] = [[(0.90, 6.20), (2.45, 6.20), (2.45, -1.00), (0.90, -1.00)]]
# epsilon-hat: the font's epsilon plus a caret, so the network's prediction is
# visibly the SAME symbol as the noise it is estimating.
_EPS_HAT: List[Poly] = [list(s) for s in _GLYPHS["ε"]] + [
    [(0.95, 4.85), (2.05, 5.75), (3.15, 4.85)]
]

# escape -> (strokes, advance in cell units)
_EXTRA: Dict[str, Tuple[List[Poly], float]] = {
    "a": (_ALPHA, 4.60),
    "A": (_ALPHA_BAR, 4.60),
    "m": (_MU, 4.60),
    "N": (_SCRIPT_N, 5.10),
    "E": (_BB_E, 4.60),
    "L": (_SCRIPT_L, 4.70),
    "n": (_NORM, 3.40),
    ">": (_ARROW_R, 5.00),
    "<": (_ARROW_L, 5.00),
    "[": (_LBRK, 3.30),
    "]": (_RBRK, 3.30),
    "h": (_EPS_HAT, 4.35),
}
_SUB_SCALE, _SUP_SCALE = 0.62, 0.62
_SUB_DROP, _SUP_RISE = -0.28, 0.52   # x cap


def _group(s: str, i: int) -> Tuple[str, int]:
    """Read a ``{...}`` group starting at ``s[i] == '{'``; returns (body, next)."""
    if i >= len(s) or s[i] != "{":
        return (s[i] if i < len(s) else ""), i + 1
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
        j += 1
    return s[i + 1 :], len(s)


def mtext(
    s: str, x: float, baseline: float, cap: float, pen: Optional[int], f: int = F_TYPE
) -> Tuple[List[GCodeCommand], float]:
    r"""Single-stroke math typesetting.  Returns (commands, advance).

    Markup: ``_{..}`` subscript, ``^{..}`` superscript, ``\R{..}`` radical with
    a vinculum over the group, and the escapes ``\a`` alpha, ``\A`` alpha-bar,
    ``\m`` mu, ``\e`` epsilon, ``\t`` theta, ``\s`` sigma, ``\N`` script-N,
    ``\E`` blackboard-E, ``\L`` script-L, ``\n`` double bar, ``\[ \]``
    brackets, ``\> \<`` arrows, ``\-`` minus, ``\~`` tilde, ``\.`` middot.
    """
    sc = cap / 6.0
    out: List[GCodeCommand] = []
    cx = x
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            code = s[i + 1]
            i += 2
            if code == "R":
                body, i = _group(s, i)
                inner_x = cx + 2.35 * sc
                sub, w = mtext(body, inner_x, baseline, cap, pen, f)
                out += sub
                top = baseline + 5.35 * sc
                out += _poly(
                    [
                        (cx + 0.05 * sc, baseline + 2.45 * sc),
                        (cx + 0.75 * sc, baseline + 1.95 * sc),
                        (cx + 1.55 * sc, baseline - 0.45 * sc),
                        (cx + 2.15 * sc, top),
                        (inner_x + w + 0.35 * sc, top),
                    ],
                    color=pen,
                    f=f,
                )
                cx = inner_x + w + 0.75 * sc
                continue
            if code in _EXTRA:
                strokes, adv = _EXTRA[code]
                for st in strokes:
                    out += _poly([(cx + gx * sc, baseline + gy * sc) for gx, gy in st], color=pen, f=f)
                cx += adv * sc
                continue
            lit = {"-": "-", "~": "~", ".": "·", "e": "ε", "t": "θ", "s": "σ"}
            ch = lit.get(code, code)
            out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
            cx += _glyph_advance(ch) * sc
            continue
        if ch in "_^":
            body, i = _group(s, i + 1)
            scale = _SUB_SCALE if ch == "_" else _SUP_SCALE
            dy = (_SUB_DROP if ch == "_" else _SUP_RISE) * cap
            sub, w = mtext(body, cx, baseline + dy, cap * scale, pen, f)
            out += sub
            cx += w + 0.10 * sc
            continue
        if ch == " ":
            cx += 2.10 * sc
            i += 1
            continue
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * sc
        i += 1
    return out, cx - x


def mwidth(s: str, cap: float) -> float:
    return mtext(s, 0.0, 0.0, cap, None)[1]


def mat(
    s: str,
    baseline: float,
    cap: float,
    pen: Optional[int],
    left: Optional[float] = None,
    centre: Optional[float] = None,
    right: Optional[float] = None,
    f: int = F_TYPE,
) -> List[GCodeCommand]:
    w = mwidth(s, cap)
    if left is not None:
        x = left
    elif centre is not None:
        x = centre - w / 2.0
    else:
        x = (right or 0.0) - w
    return mtext(s, x, baseline, cap, pen, f)[0]


def tracked(
    text: str,
    x: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    target_w: Optional[float] = None,
    f: int = F_TYPE,
) -> Tuple[List[GCodeCommand], float]:
    """Proportional type with uniform letter-tracking to hit ``target_w``.

    Cap height stays at the measured value and the extra width goes into
    tracking, rather than scaling the glyphs up — which is how recreation
    headings end up 30% oversized.
    """
    sc = cap / 6.0
    nat = sum(_glyph_advance(c) for c in text) * sc
    extra = (target_w - nat) / (len(text) - 1) if (target_w and len(text) > 1) else 0.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * sc + extra
    return out, (cx - extra - x if len(text) > 1 else nat)


def tat(
    text: str,
    baseline: float,
    cap: float,
    pen: Optional[int],
    left: Optional[float] = None,
    centre: Optional[float] = None,
    right: Optional[float] = None,
    target_w: Optional[float] = None,
) -> List[GCodeCommand]:
    sc = cap / 6.0
    w = target_w if target_w else sum(_glyph_advance(c) for c in text) * sc
    if left is not None:
        x = left
    elif centre is not None:
        x = centre - w / 2.0
    else:
        x = (right or 0.0) - w
    return tracked(text, x, baseline, cap, pen, target_w)[0]


def twidth(text: str, cap: float) -> float:
    return sum(_glyph_advance(c) for c in text) * (cap / 6.0)


# ===========================================================================
# stroke helpers
# ===========================================================================
def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _dash(poly: Poly, on: float, off: float, phase: float = 0.0) -> List[Poly]:
    """Split a polyline into ``on`` mm dashes separated by ``off`` mm.

    The phase is an explicit on/off state with a remaining length, never
    ``arclength % period``: the modulo form lands epsilon below the switch
    once float error accumulates, the step collapses to ~1e-16 and the walk
    never terminates.
    """
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


def _disc(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid dot as a tight spiral — small enough that a spiral cannot flood."""
    turns = max(3, int(r / 0.20))
    n = turns * 20
    pts = [
        (
            x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            y + r * (k / n) * math.sin(2 * math.pi * turns * k / n),
        )
        for k in range(n + 1)
    ]
    ring = [
        (x + r * math.cos(2 * math.pi * k / 26), y + r * math.sin(2 * math.pi * k / 26))
        for k in range(27)
    ]
    return _poly(pts, color=pen, f=1600) + _poly(ring, color=pen, f=1600)


def _guard(cmds: List[GCodeCommand], min_dist: float = MIN_GAP) -> List[GCodeCommand]:
    """``enforce_line_spacing`` + re-emit, so every stroke keeps a leading G0.

    The policy rebuilds strokes and can drop the ``G0`` that positions one;
    the merged program would then start that stroke from the machine origin.
    """
    thinned = enforce_line_spacing(cmds, min_dist=min_dist, resample=0.45)
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


def _arrow(p0: Pt, p1: Pt, pen: Optional[int], head: float = 2.6, dashed: bool = False,
           on: float = 3.4, off: float = 2.6) -> List[GCodeCommand]:
    shaft = [p0, p1]
    out = _emit(_dash(shaft, on, off) if dashed else [shaft], pen)
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    for da in (2.55, -2.55):
        out += _emit(
            [[(p1[0] + head * math.cos(a + da), p1[1] + head * math.sin(a + da)), p1]], pen
        )
    return out


# ===========================================================================
# marching squares (numpy-prefiltered, chained with the house helper)
# ===========================================================================
_MS = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),), 5: ((3, 2), (0, 1)),
    6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),), 9: ((0, 2),), 10: ((0, 3), (1, 2)),
    11: ((1, 2),), 12: ((1, 3),), 13: ((0, 1),), 14: ((0, 3),),
}


def _iso(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, iso: float) -> List[Poly]:
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
        for p, q in _MS[int(case[j, i])]:
            segs.append((e[p], e[q]))
    return [list(ch) for ch in _chain_segments(segs)]


# ===========================================================================
# the data manifold: a lobed amoeba and its distance field
# ===========================================================================
def _amoeba(rng: SeededRNG, lobes: int, n: int = 360) -> Poly:
    """Closed radial blob, unit max radius, with ``lobes`` deep waists.

    A dominant k = ``lobes`` term is the whole trick: a near-convex blob's
    distance field has one long medial ridge and its rings come out as a
    plain onion, while waists deep enough to pinch give a star-shaped medial
    axis, so the rings split into the reference's per-petal eyes and a dark
    junction where the arms meet.
    """
    a_main = rng.uniform(0.30, 0.37)
    ph = rng.uniform(0, 2 * math.pi)
    harm = [(lobes, a_main, ph)]
    for k in (2, 3, 5, 7):
        if k == lobes:
            continue
        harm.append((k, rng.uniform(0.04, 0.13), rng.uniform(0, 2 * math.pi)))
    pts: Poly = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1.0 + sum(a * math.cos(kk * t + p) for kk, a, p in harm)
        pts.append((r * math.cos(t), r * math.sin(t)))
    m = max(math.hypot(*p) for p in pts)
    return [(p[0] / m, p[1] / m) for p in pts]


def _dist_field(poly: Poly, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Distance to the boundary, positive INSIDE, 0 outside.  |grad| = 1."""
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


def build_x0(rng: SeededRNG, R: float, lobes: int, pitch: float = RING_PITCH):
    """The clean state: contour rings of the manifold, centred on (0, 0).

    Returns ``(chains, sigma)``: a list of polylines in form-local mm, and the
    RMS per-axis spread of their points, which is the sigma the forward
    process uses (making it variance-preserving).
    """
    outline = [(p[0] * R, p[1] * R) for p in _amoeba(rng, lobes)]
    pad = 1.5
    step = 0.34
    xs = np.arange(-R - pad, R + pad + step, step)
    ys = np.arange(-R - pad, R + pad + step, step)
    X, Y = np.meshgrid(xs, ys)
    D = _dist_field(outline, X, Y)
    # a bounded fbm wobble (|grad| <= ~0.13) so the rings read hand-drawn
    # without the pitch ever dropping below the floor
    ox, oy = rng.uniform(-40, 40), rng.uniform(-40, 40)
    wob = (_value_noise(X / 11.0 + ox, Y / 11.0 + oy) - 0.5) * (0.42 * pitch)
    F = np.where(D > 0, D + wob, 0.0)

    chains: List[Tuple[int, Poly]] = [(0, outline + [outline[0]])]
    dmax = float(F.max())
    k = 1
    while k * pitch < dmax:
        chains.extend((k, ch) for ch in _iso(F, xs, ys, k * pitch))
        k += 1
    pts = np.asarray([q for _, ch in chains for q in ch], float)
    sigma = float(math.sqrt(0.5 * (pts[:, 0].var() + pts[:, 1].var())))
    return chains, sigma, _sample_manifold(chains, N_SPECKLE)


def _sample_manifold(chains: Sequence[Tuple[int, Poly]], n: int) -> List[Pt]:
    """``n`` points spread evenly over the manifold's own contour set.

    These are the x_0 the forward process acts on.  The order is decorrelated
    by a fixed stride so that taking the FIRST k of them samples the whole
    form rather than the outermost ring — which is what lets one epsilon draw
    be revealed progressively along the row.
    """
    total = sum(
        math.hypot(b[0] - a[0], b[1] - a[1]) for _, ch in chains for a, b in zip(ch, ch[1:])
    )
    step = max(0.25, total / max(n, 1))
    pts: List[Pt] = []
    acc = 0.0
    for _, ch in chains:
        for a, b in zip(ch, ch[1:]):
            seg = math.hypot(b[0] - a[0], b[1] - a[1])
            acc += seg
            while acc >= step:
                acc -= step
                t = 1.0 - acc / max(seg, 1e-9)
                t = min(max(t, 0.0), 1.0)
                pts.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    m = len(pts)
    if m == 0:
        return []
    stride = 977 if m > 977 else 7
    while math.gcd(stride, m) != 1:
        stride += 1
    return [pts[(i * stride) % m] for i in range(m)]


# ===========================================================================
# the forward process, applied to the drawing
# ===========================================================================
def _smooth_field(rng: SeededRNG, corr: float) -> Callable[[float, float], Pt]:
    """Unit-variance smooth 2-D vector noise with correlation length ``corr``.

    Eight random plane waves per component.  A continuous stroke can only
    carry the LOW-frequency part of a noise field and stay a stroke; the
    white part is what breaks it into dashes and then into dots.
    """
    modes = []
    for _ in range(8):
        a = rng.uniform(0, 2 * math.pi)
        k = (2 * math.pi / corr) * rng.uniform(0.6, 1.5)
        modes.append((k * math.cos(a), k * math.sin(a), rng.uniform(0, 2 * math.pi),
                      rng.uniform(0, 2 * math.pi)))
    norm = math.sqrt(2.0 / len(modes))

    def field(x: float, y: float) -> Pt:
        ex = ey = 0.0
        for kx, ky, p1, p2 in modes:
            ex += math.cos(kx * x + ky * y + p1)
            ey += math.cos(kx * x + ky * y + p2)
        return (ex * norm, ey * norm)

    return field


def _white(seed: int, ring: int, bucket: int) -> Pt:
    """Two i.i.d. standard normals, keyed to a PHYSICAL place on the manifold.

    Keying on (ring, arclength bucket) rather than on the mark index is what
    makes ONE noise draw serve the whole row: the dash schedule changes with
    t, but the same point of x_0 always gets the same epsilon, so the six
    states really are one trajectory.
    """
    n = (seed * 2654435761 + ring * 40503 + bucket * 2246822519) & 0xFFFFFFFF
    n = (n ^ (n >> 15)) * 2246822519 & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 3266489917 & 0xFFFFFFFF
    u1 = (((n ^ (n >> 16)) & 0xFFFFFF) + 1) / 0x1000001
    m = (n * 1274126177 + 12345) & 0xFFFFFFFF
    m = (m ^ (m >> 15)) * 2246822519 & 0xFFFFFFFF
    u2 = ((m ^ (m >> 16)) & 0xFFFFFF) / 0xFFFFFF
    r = math.sqrt(-2.0 * math.log(u1))
    return (r * math.cos(2 * math.pi * u2), r * math.sin(2 * math.pi * u2))


W_WARP = 0.26     # the share of the noise a CONTINUOUS stroke can carry
W_JIT = 0.10      # the share carried as a rigid per-mark offset
N_SPECKLE = 700   # dots in a fully noised state
LEVEL_NOISE = 1.6  # the noise's level spread, in ring pitches (see _keep_every)


def _keep_every(ab: float) -> int:
    """How far apart surviving contours must be, in ladder steps.

    A ring is still a ring only while the SIGNAL's level gap clears the
    noise's level spread: ``sqrt(abar) * pitch > sqrt(1-abar) * LEVEL_NOISE *
    pitch``.  Below that, neighbouring contours merge and the ladder has to
    be decimated.  This is why the FINE DETAIL DIES FIRST in a diffusion
    forward process — and, conveniently, it is also the only way a pen can
    keep the nest off the plotting floor.  Ratios at the six columns:
    1, 1, 2, 3, 5, (gone).
    """
    sa = math.sqrt(max(ab, 1e-9))
    sn = math.sqrt(max(0.0, 1.0 - ab))
    return max(1, int(math.ceil(LEVEL_NOISE * sn / sa))) if sa > 1e-6 else 10 ** 6


def _duty(ab: float) -> Tuple[float, float]:
    """(on, off) mm for the signal nest.  The drawn FRACTION is abar.

    Level sets do not move when the signal is attenuated — sqrt(abar) x_0 has
    exactly the same contours as x_0 — so the nest must not shrink.  What the
    attenuation destroys is the contour's CONTRAST against the noise, and a
    pen has one way to spend contrast: duty.  on/(on+off) = abar, so at
    abar = .90 the nest is all but solid, at .34 it is a broken dash and at
    .095 it is a crumb — the late, fast collapse the schedule really gives.
    """
    if ab >= 0.9995:
        return (1e9, 0.0)
    on = max(0.50, 8.0 * ab ** 1.10)
    off = min(7.0, on * (1.0 - ab) / max(ab, 0.055))
    return (on, off)


def render_state(
    chains: Sequence[Tuple[int, Poly]],
    sigma: float,
    sample: Sequence[Pt],
    ab: float,
    eta: Callable[[float, float], Pt],
    seed: int,
    cx: float,
    cy: float,
    pen: Optional[int],
    core_dot: bool = True,
) -> List[GCodeCommand]:
    """One state of ``x_t = sqrt(abar) x_0 + sqrt(1-abar) sigma e``, in two layers.

    SIGNAL — the level sets of ``E[x_t | x_0] = sqrt(abar) x_0``.  Scaling a
    FIELD's values does not move its contours, so the nest keeps its size and
    its place in the column; what the attenuation costs it is contrast, spent
    two ways: the ladder is decimated (``_keep_every``) as rings stop clearing
    the noise, and the surviving rings are drawn at duty ``abar``.  A slow
    warp of amplitude ``sqrt(1-abar) sigma W_WARP`` carries the low-frequency
    share of the noise; its correlation length is long enough that
    neighbouring rings translate together instead of crossing.

    NOISE — the realisation ``e``, as i.i.d. Gaussian speckle of spread
    ``sigma``, count ``N_SPECKLE (1-abar)^0.9``.  The dots come from ONE fixed
    sequence keyed to the row, so the same epsilon is revealed further along
    it.  At abar = 0 nothing but the speckle is left, so x_T is exactly an
    isotropic Gaussian sample: no residual lobe, no preferred direction.

    sigma is the data's own RMS spread, which makes the process
    variance-preserving — the footprint is the same in every column, which is
    what lets a reader compare straight down a column.
    """
    sn = math.sqrt(max(0.0, 1.0 - ab))
    warp = sn * sigma * W_WARP
    jit = sn * sigma * W_JIT
    on, off = _duty(ab)
    keep = _keep_every(ab)
    if ab > 0.02:
        keep = min(keep, max(1, len(chains)))  # level 0 always survives
    out: List[GCodeCommand] = []

    if ab > 0.02:
        for ri, (lvl, chain) in enumerate(chains):
            if len(chain) < 2 or (lvl % keep):
                continue
            c_on, c_off = (_duty(max(ab, 0.42)) if lvl == 0 else (on, off))
            for mark in _dash(chain, c_on, c_off, phase=(ri * 1.37) % max(c_on + c_off, 1e-6)):
                mid = mark[len(mark) // 2]
                bucket = int((mid[0] * 7.31 + mid[1] * 11.87) / 0.9)
                xi = _white(seed, ri, bucket)
                dx, dy = jit * xi[0], jit * xi[1]
                pts: Poly = []
                for px0, py0 in mark:
                    ex, ey = eta(px0, py0)
                    pts.append((cx + px0 + warp * ex + dx, cy + py0 + warp * ey + dy))
                if len(pts) >= 2:
                    out += _poly(pts, color=pen, f=F_DRAW)
                    if lvl == 0:
                        out += _poly(
                            [(qx, qy + 0.30) for qx, qy in pts], color=pen, f=F_DRAW
                        )

    n = int(round(min(N_SPECKLE, len(sample)) * (1.0 - ab) ** 1.15))
    drawn = 0
    i = -1
    while drawn < n and i < 6 * N_SPECKLE:
        i += 1
        ux, uy = _white(seed, 9, i)
        # truncated at 2.2 sigma so the cloud stays inside its column; the
        # tail is REJECTED, never clamped, or the missing 2% would pile onto a
        # hard circle and give the cloud a drawn edge
        if math.hypot(ux, uy) > 2.20:
            continue
        drawn += 1
        px = cx + sigma * ux
        py = cy + sigma * uy
        a = math.atan2(uy, ux)
        out += _poly(
            [
                (px - 0.28 * math.cos(a), py - 0.28 * math.sin(a)),
                (px + 0.28 * math.cos(a), py + 0.28 * math.sin(a)),
            ],
            color=pen,
            f=1500,
        )

    if core_dot and ab > 0.30:
        out += _disc(cx, cy, 0.95 * ab ** 0.5, pen)
    return out


# ===========================================================================
# the U-Net bowtie
# ===========================================================================
# measured half-heights on the reference: bell 107 px, then 62, 33, 17 —
# a clean halving, i.e. the resolution pyramid.  Knots are (s, amplitude)
# with s = |x - centre| / half-width.
_UNET_KNOTS = (
    (0.000, 0.075),   # the waist: the bottleneck
    (0.057, 0.013),
    (0.115, 0.155),   # level 3
    (0.172, 0.020),
    (0.235, 0.300),   # level 2
    (0.345, 0.033),
    (0.465, 0.580),   # level 1
    (0.700, 0.058),
    (0.925, 1.000),   # level 0, the bell mouth
)
BULGE_S = (0.925, 0.465, 0.235, 0.115)   # outer -> inner, for the skip arcs


def _catmull(knots: Sequence[Tuple[float, float]]) -> Callable[[float], float]:
    """Catmull-Rom through (s, log amplitude) so the profile stays positive."""
    ss = [k[0] for k in knots]
    ls = [math.log(k[1]) for k in knots]

    def f(s: float) -> float:
        s = min(max(s, ss[0]), ss[-1])
        i = 0
        while i < len(ss) - 2 and s > ss[i + 1]:
            i += 1
        p0 = ls[max(0, i - 1)]
        p1, p2 = ls[i], ls[i + 1]
        p3 = ls[min(len(ls) - 1, i + 2)]
        t = (s - ss[i]) / (ss[i + 1] - ss[i])
        v = 0.5 * (
            (2 * p1)
            + (-p0 + p2) * t
            + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
            + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t
        )
        return math.exp(v)

    return f


_PROFILE = _catmull(_UNET_KNOTS)


def unet_h(s: float) -> float:
    """Tube half-height as a fraction of ``BOWTIE_H``, s in [0, 1]."""
    s = abs(s)
    if s >= 1.0:
        return 0.0
    if s > 0.925:
        # elliptical cap: the streamline family closes into a rounded BELL
        # instead of a point, which is what the reference's mouth is
        return math.sqrt(max(0.0, 1.0 - ((s - 0.925) / 0.075) ** 2))
    return _PROFILE(s)


def _tz(j: int) -> int:
    """Trailing-zero count — the dyadic refinement level of streamline j."""
    if j == 0:
        return 30
    n = 0
    while not (j >> n) & 1:
        n += 1
    return n


def render_unet(
    x_l: float, x_r: float, y_c: float, colors: int, n_half: int = 48
) -> List[GCodeCommand]:
    """The bowtie as a nested family of closed streamlines with dyadic LOD.

    ``y = y_c +- c_j h(x)``, so the perpendicular gap between neighbours at
    refinement level L is ``dc 2^L h(x) cos(atan(h'))``.  A REQUIRED LEVEL is
    computed per x from the profile alone — never per line — and line j is
    drawn wherever its own dyadic level clears it.  Deciding per line made
    the gap test flicker along the steep flank of every bulge and combed each
    lens into crumbs; deciding per x gives clean dyadic merges and leaves
    every streamline continuous between the pinches, which is the property
    the whole plate is built on.

    Every line is drawn in the bells and one in sixteen at the waist, so the
    bottleneck is visibly the sparsest place on the sheet — the one thing the
    piece has to say about a U-Net.
    """
    half = (x_r - x_l) / 2.0
    xc = (x_l + x_r) / 2.0
    N = 600
    xs = [x_l + (x_r - x_l) * k / N for k in range(N + 1)]
    ss = [abs(x - xc) / half for x in xs]
    hs = [unet_h(s) * BOWTIE_H for s in ss]
    dh = [0.0] * (N + 1)
    for k in range(1, N):
        dh[k] = (hs[k + 1] - hs[k - 1]) / (xs[k + 1] - xs[k - 1])
    dh[0], dh[N] = dh[1], dh[N - 1]

    dc = 1.0 / n_half
    req: List[int] = []
    for k in range(N + 1):
        eff = dc * hs[k] / math.sqrt(1.0 + dh[k] ** 2)
        L = 0
        while L < 8 and eff * (2 ** L) < MIN_GAP:
            L += 1
        req.append(L if hs[k] > 0.05 else 99)
    # one sample of hysteresis: a lone dip must not punch a hole in a lens
    req = [max(req[max(0, k - 1) : min(N + 1, k + 2)]) for k in range(N + 1)]

    out: List[GCodeCommand] = []
    for j in range(1, n_half + 1):
        c = j * dc
        lvl = 30 if j == n_half else _tz(j)
        for sign in (1, -1):
            run: Poly = []
            for k in range(N + 1):
                if lvl >= req[k]:
                    run.append((xs[k], y_c + sign * c * hs[k]))
                else:
                    if len(run) >= 2:
                        out += _emit_ramp(run, x_l, x_r, colors)
                    run = []
            if len(run) >= 2:
                out += _emit_ramp(run, x_l, x_r, colors)
    return out


def _tube_pen(x: float, x_l: float, x_r: float, colors: int) -> Optional[int]:
    """The pen of the state column directly above: the ramp is the time axis."""
    u = (x - x_l) / (x_r - x_l)
    idx = BLUE if u < 1 / 6 else PURPLE if u < 0.5 else PINK if u < 5 / 6 else RED
    return idx % colors if colors > 1 else None


def _emit_ramp(run: Poly, x_l: float, x_r: float, colors: int) -> List[GCodeCommand]:
    """Emit a streamline split at the ramp's pen boundaries."""
    out: List[GCodeCommand] = []
    cur: Poly = [run[0]]
    pen = _tube_pen(run[0][0], x_l, x_r, colors)
    for p in run[1:]:
        q = _tube_pen(p[0], x_l, x_r, colors)
        cur.append(p)
        if q != pen:
            out += _poly(cur, color=pen, f=F_DRAW)
            cur = [p]
            pen = q
    if len(cur) >= 2:
        out += _poly(cur, color=pen, f=F_DRAW)
    return out


def render_skips(x_l: float, x_r: float, y_c: float, fr: Frame, pen: Optional[int]):
    """Dashed arcs joining each encoder level to its MIRRORED decoder level."""
    half = (x_r - x_l) / 2.0
    xc = (x_l + x_r) / 2.0
    out: List[GCodeCommand] = []
    apex_v = (0.4530, 0.4720, 0.4910, 0.5100)
    for i, s in enumerate(BULGE_S):
        xa = xc - s * half
        xb = xc + s * half
        ya = y_c + unet_h(s) * BOWTIE_H * 0.62
        apex = fr.v(apex_v[i])
        arc: Poly = []
        n = 90
        for k in range(n + 1):
            t = k / n
            x = xa + (xb - xa) * t
            y = (1 - t) ** 2 * ya + 2 * (1 - t) * t * (apex * 2 - (ya + ya) / 2) + t ** 2 * ya
            arc.append((x, y))
        out += _emit(_dash(arc, 2.5, 2.0), pen, f=2400)
        tail = arc[-6:]
        out += _arrow(tail[0], (xb, ya), pen, head=2.0)
        out += _emit([[(xa, ya), (xa, ya - 1.6)]], pen)
    return out


# ===========================================================================
# the plate
# ===========================================================================
def _pen(idx: int, colors: int) -> Optional[int]:
    return idx % colors if colors > 1 else None


def diffusion_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    fr = Frame(bounds)
    U, V = fr.u, fr.v
    out: List[GCodeCommand] = []
    P = lambda i: _pen(i, colors)  # noqa: E731

    R = STATE_D / 2.0
    top_cy = V(TOPFORM_TOP + (STATE_D / 2.0) / fr.h)
    bot_cy = V(BOTFORM_TOP + (STATE_D / 2.0) / fr.h)

    # ---- the two samples ---------------------------------------------------
    # different draws from the same family: the reverse row must arrive at an
    # x_0 that is recognisably of the data distribution, not a replay of the
    # forward row's.
    fwd_chains, fwd_sigma, fwd_pts = build_x0(rng, R, lobes=3)
    fwd_eta = _smooth_field(rng, corr=R * 3.2)
    rev_chains, rev_sigma, rev_pts = build_x0(rng, R, lobes=4)
    rev_eta = _smooth_field(rng, corr=R * 3.2)

    for k, (u, ab) in enumerate(zip(COL_U, ABAR)):
        out += render_state(
            fwd_chains, fwd_sigma, fwd_pts, ab, fwd_eta, 11, U(u), top_cy, P(RAMP[k])
        )
        out += render_state(
            rev_chains, rev_sigma, rev_pts, ab, rev_eta, 29, U(u), bot_cy, P(RAMP[k])
        )

    # ---- state labels ------------------------------------------------------
    for k, u in enumerate(COL_U):
        out += mat(STATE_LABELS[k], V(TOPLBL_V), LBL_CAP, P(BLACK), centre=U(u))
        out += mat(STATE_LABELS[k], V(BOTLBL_V), LBL_CAP, P(BLACK), centre=U(u))

    # ---- "..." separators --------------------------------------------------
    pitch = COL_U[1] - COL_U[0]
    for k in range(5):
        cu = COL_U[k] + pitch / 2.0
        for d in (-1, 0, 1):
            out += _disc(U(cu) + d * 2.4, top_cy, 0.45, P(BLACK))
            out += _disc(U(cu) + d * 2.4, bot_cy, 0.45, P(BLACK))

    out += _header(fr, colors)
    out += _unet_band(fr, colors)
    out += _reverse_band(fr, colors)
    out += _captions(fr, colors)
    out += _furniture(rng, fr, colors)
    return out


def _header(fr: Frame, colors: int) -> List[GCodeCommand]:
    U, V = fr.u, fr.v
    P = lambda i: _pen(i, colors)  # noqa: E731
    out: List[GCodeCommand] = []

    out += tat("DIFFUSION", V(TITLE_V), TITLE_CAP, P(BLACK), left=U(0.020), target_w=TITLE_W)
    for i, line in enumerate(("probabilistic", "generative", "modeling")):
        out += tat(line, V(SUB_V[i]), SUB_CAP, P(BLACK), left=U(0.020), target_w=None)

    for i, line in enumerate(KW_TOP):
        out += tat(line, V(KWA_V0 + i * KW_PITCH), KW_CAP, P(BLACK), left=U(SIDEBAR_L))

    cu = (COL_U[0] + COL_U[5]) / 2.0
    out += tat(
        "forward process (noising)", V(FWD_LBL_V), HDR_CAP, P(BLACK), centre=U(cu), target_w=86.0
    )
    a0, a1 = U(0.2200), U(0.7600)
    out += _arrow((a0, V(FWD_ARR_V)), (a1, V(FWD_ARR_V)), P(BLACK), dashed=True, on=4.0, off=3.2)
    out += mat(
        r"q(x_{t} | x_{0}) = \N(\R{\A_{t}} x_{0}, (1 \- \A_{t}) I)",
        V(FWD_MATH_V), HDR_CAP, P(BLACK), centre=U(cu),
    )
    return out


def _unet_band(fr: Frame, colors: int) -> List[GCodeCommand]:
    U, V = fr.u, fr.v
    P = lambda i: _pen(i, colors)  # noqa: E731
    out: List[GCodeCommand] = []
    x_l, x_r = U(COL_U[1]), U(COL_U[4])
    y_c = V(BOWTIE_V)
    xc = (x_l + x_r) / 2.0

    out += mat(r"U-Net   \e_{\t}(x_{t}, t)", V(UNET1_V), UNET1_CAP, P(BLACK), centre=xc)
    out += tat(
        "predicts noise (or v, or x0)", V(UNET2_V), UNET2_CAP, P(BLACK), centre=xc, target_w=62.0
    )

    out += render_unet(x_l, x_r, y_c, colors)
    out += render_skips(x_l, x_r, y_c, fr, P(BLACK))
    out += tat("skip connections", V(SKIP_LBL_V), 2.30, P(BLACK), centre=xc, target_w=40.0)
    out += _emit(
        _dash([(xc, V(SKIP_LBL_V) - 1.6), (xc, V(0.4530) + 0.8)], 1.8, 1.8), P(BLACK), f=2400
    )

    # x_t in: an isotropic red dot cloud (the same i.i.d. draw the top row's
    # x_T is made of) with a solid arrow into the bell
    sig = STATE_D * 0.215
    for i in range(660):
        dx, dy = _white(77, 3, i)
        px, py = U(XT_IN_U) + sig * dx, y_c + sig * dy
        a = math.atan2(dy, dx)
        out += _poly(
            [
                (px - 0.30 * math.cos(a), py - 0.30 * math.sin(a)),
                (px + 0.30 * math.cos(a), py + 0.30 * math.sin(a)),
            ],
            color=P(RED),
            f=1500,
        )
    out += mat("x_{t}", V(0.4930), LBL_CAP, P(BLACK), centre=U(XT_IN_U))
    out += tat("noisy sample", V(0.6800), 2.20, P(BLACK), centre=U(XT_IN_U))
    out += _arrow(
        (U(XT_IN_U) + 24.0, y_c), (x_l - 3.0, y_c), P(BLACK), head=2.8
    )

    # eps-hat out
    out += _eps_hat(U(EPS_OUT_U), y_c, P(BLACK))
    out += mat(r"\h", V(0.4930), LBL_CAP, P(BLACK), centre=U(EPS_OUT_U))
    out += tat("predicted noise", V(0.6800), 2.20, P(BLACK), centre=U(EPS_OUT_U))
    out += _arrow((x_r + 3.0, y_c), (U(EPS_OUT_U) - 13.0, y_c), P(BLACK), head=2.8)

    # the loss, behind a rule in the right sidebar
    out += _emit([[(U(LOSS_RULE_U), V(0.5350)), (U(LOSS_RULE_U), V(0.6400))]], P(BLACK))
    out += mat(
        r"\L = \E_{t,x0,\e} \[ \n\e \- \e_{\t}(x_{t}, t)\n^{2} \]",
        V(LOSS_V), 2.70, P(BLACK), left=U(SIDEBAR_L),
    )
    return out


def _eps_hat(cx: float, cy: float, pen: Optional[int]) -> List[GCodeCommand]:
    """The predicted noise: a small lobed blob in black, the clean sibling of
    the coloured states — the network's answer is a SAMPLE, not a cloud."""
    sub = SeededRNG(915)
    chains, sigma, pts = build_x0(sub, 13.0, lobes=3, pitch=0.95)
    eta = _smooth_field(sub, 40.0)
    return render_state(chains, sigma, pts, 1.0, eta, 915, cx, cy, pen)


def _reverse_band(fr: Frame, colors: int) -> List[GCodeCommand]:
    U, V = fr.u, fr.v
    P = lambda i: _pen(i, colors)  # noqa: E731
    out: List[GCodeCommand] = []
    cu = (COL_U[0] + COL_U[5]) / 2.0
    out += tat(
        "reverse process (denoising)", V(REV_LBL_V), HDR_CAP, P(BLACK), centre=U(cu), target_w=92.0
    )
    a0, a1 = U(0.7600), U(0.2200)
    out += _arrow((a0, V(REV_ARR_V)), (a1, V(REV_ARR_V)), P(BLACK), dashed=True, on=4.0, off=3.2)
    out += mat(
        r"p_{\t}(x_{t\-1} | x_{t}) = \N(\m_{\t}(x_{t}, t), \s_{t}^{2} I)",
        V(REV_MATH_V), HDR_CAP, P(BLACK), centre=U(cu),
    )
    return out


def _captions(fr: Frame, colors: int) -> List[GCodeCommand]:
    U, V = fr.u, fr.v
    P = lambda i: _pen(i, colors)  # noqa: E731
    out: List[GCodeCommand] = []

    out += tat("data distribution", V(CAP1_V), CAP_CAP, P(BLACK), centre=U(COL_U[0]))
    out += mat("p_{data}(x)", V(CAP2_V), CAP_CAP + 0.3, P(BLACK), centre=U(COL_U[0]))
    out += tat("isotropic noise", V(CAP1_V), CAP_CAP, P(BLACK), centre=U(COL_U[5]))
    out += mat(r"\N(0, I)", V(CAP2_V), CAP_CAP + 0.3, P(BLACK), centre=U(COL_U[5]))

    # the t axis
    y = V(AXIS_V)
    out += _arrow((U(AXIS_U[0]), y), (U(AXIS_U[1]), y), P(BLACK), head=2.6)
    out += tat("t = 0", y + 1.4, 2.10, P(BLACK), left=U(AXIS_U[0]))
    out += tat("t = T", y + 1.4, 2.10, P(BLACK), right=U(AXIS_U[1]))
    out += tat("increasing noise", y + 1.4, 2.10, P(BLACK), centre=U(0.4385), target_w=34.0)

    out += tat("generated sample", V(BCAP1_V), CAP_CAP, P(BLACK), centre=U(COL_U[0]))
    out += mat(r"x \~ p_{\t}(x)", V(BCAP2_V), CAP_CAP + 0.3, P(BLACK), centre=U(COL_U[0]))
    out += tat("sample from", V(BCAP1_V), CAP_CAP, P(BLACK), centre=U(COL_U[5]))
    out += mat(r"\N(0, I)", V(BCAP2_V), CAP_CAP + 0.3, P(BLACK), centre=U(COL_U[5]))

    for i, line in enumerate(KW_BOT):
        out += tat(line, V(KWB_V0 + i * KW_PITCH), KW_CAP, P(BLACK), left=U(SIDEBAR_L))

    out += tat("PEN PLOTTER", V(FOOT_V), FOOT_CAP, P(BLACK), left=U(0.020), target_w=58.0)
    out += _emit([[(U(0.180), V(FOOT_V) + 1.1), (U(0.232), V(FOOT_V) + 1.1)]], P(BLACK))
    return out


def _furniture(rng: SeededRNG, fr: Frame, colors: int) -> List[GCodeCommand]:
    U, V = fr.u, fr.v
    P = lambda i: _pen(i, colors)  # noqa: E731
    out: List[GCodeCommand] = []

    # Registration crosses sit ON the plate's own grid lines — the sidebar
    # edge, the sheet centreline, the two register baselines — so they read
    # as the grid being declared, not as scattered drafting confetti.
    for cu, cv, sz in (
        (0.4385, 0.0180, 4.4),
        (0.0180, BOWTIE_V, 4.4),
        (0.4385, 0.9880, 4.4),
    ):
        x, y = U(cu), V(cv)
        out += _emit([[(x - sz, y), (x + sz, y)], [(x, y - sz), (x, y + sz)]], P(BLACK))

    # one small filled square above each sidebar block, sharing the block's
    # left edge — a marker ON the column, never a mark beside the text
    for cv in (KWA_V0 - 0.0190, LOSS_V - 0.0560, KWB_V0 - 0.0190):
        x, y = U(SIDEBAR_L), V(cv)
        out += _emit([[(x, y), (x + 2.4, y), (x + 2.4, y + 2.4), (x, y + 2.4), (x, y)]], P(BLACK))
        out += _disc(x + 1.2, y + 1.2, 1.0, P(BLACK))

    # dashed quarter-arcs, each tucked into a corner of clear paper
    for cu, cv, r, qx, qy in (
        (0.2100, 0.0250, 12.0, -1, -1),
        (0.8880, 0.1900, 10.0, 1, 1),
        (0.8880, 0.7500, 10.0, 1, -1),
        (0.3250, 0.9760, 12.0, -1, 1),
    ):
        cx, cy = U(cu), V(cv)
        arc = [
            (cx + qx * r * math.cos(a), cy + qy * r * math.sin(a))
            for a in np.linspace(0, math.pi / 2, 40)
        ]
        out += _emit(_dash(arc, 2.6, 2.2), P(BLACK))

    # short dashed rules down the middle of the sidebar gutter
    for cu, v0, v1 in ((SIDEBAR_L - 0.0155, 0.1450, 0.3300),
                       (SIDEBAR_L - 0.0155, 0.7900, 0.9300)):
        out += _emit(_dash([(U(cu), V(v0)), (U(cu), V(v1))], 3.0, 3.2), P(BLACK))
    out += _emit(_dash([(U(0.0180), V(0.1450)), (U(0.0180), V(0.3300))], 3.0, 3.2), P(BLACK))
    return out
