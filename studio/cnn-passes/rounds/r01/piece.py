"""CNN — FORWARD AND BACKWARD.  Faithful recreation, r01.

Recreation of ``studio/cnn-passes/ref/reference.png`` (1536x1024): two stacked
registers of the same pipeline, activations left->right on top, gradients
right->left underneath, every forward stage sitting on the SAME x column as its
gradient twin.

The vocabulary is the reference's, unchanged: tilted parallelogram plane stacks
with line-fill textures, dotted flow bundles that fan and pinch between stages,
tensor-shape annotations, kernel swatch rows, the classifier bar + softmax fan,
a five-cell legend strip, registration crosses, ``C N N`` in spaced caps.

WHAT IS EXACT (not decorated) -- one real forward/backward pass drives the
whole sheet.  A single scalar field ``f(u, v)`` (a sum of three low-frequency
sinusoids) plays the role of the pre-activation A1, and every other stage is
COMPUTED from it:

    A1 = f                      R1 = max(0, f)          P1 = maxpool_2x2(R1)
    dL/dP1 -> unpool (one cell per 2x2 window, at the argmax)
           -> dL/dR1 -> * 1[f > 0] -> dL/dA1

so the blank regions of the forward ReLU plane, the mask plane and the dL/dA1
plane are the SAME silhouette drawn three times, and the unpooled gradient
plane carries exactly one mark per pooling window.  The classifier end is a
real softmax of seven logits (p3 = 0.556 wins) and the per-class gradient tiles
carry |p - y| exactly, so the true class is the densest tile.

CROWDING FIXES (the rubric's "OVERLAP IS A DECISION" outranks fidelity):

1. flow bundles are CLIPPED OUT of every plane, the input plates, the
   classifier bars and every label halo, so they pass BEHIND the stacks and
   reappear in the gaps -- in the reference they sit on top and turn the plane
   interiors to mud;
2. the bundles' waists are sized from the pen tip (n_strands x 1.05 mm), so a
   pinch is a real pinch and still never crosses the plotting floor;
3. stacks are narrower (4-7 planes at a 0.30 w step instead of the reference's
   ~8 at 0.45 w) which buys 18-40 mm of clear paper in every inter-stage gap
   instead of the reference's ~11 mm;
4. a 15 mm gutter of bare paper separates the two registers, crossed only by
   the seven dotted column-registration ticks -- which are the plate's thesis;
5. plane textures run at a >= 1.05 mm pitch (>= 0.91 mm after the worst-case
   shear compression) and every dense family goes through
   ``policies.enforce_line_spacing``.

Occlusion is exact: a plane's texture and border are clipped out of the union
of the NEARER planes in its stack with ``engine.geometry.clip``, never with a
hand-rolled ``hidden=`` test and never with a z-buffer (these are flat
parallelograms; polygon clipping is both exact and cheaper).

Pens (``colors=3``): 0 black (structure, type, furniture), 1 blue (the
highlighted forward channel), 2 red (the backward pass).

Entry point: ``cnn_passes``.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from promptplot.generative.engine.geometry import (
    HalfPlane,
    Intersect,
    Rect,
    Region,
    Union,
    clip,
)
from promptplot.generative.engine.kit import _clip_runs, circle
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

BLACK, BLUE, RED = 0, 1, 2

F_DRAW = 2200
F_TYPE = 2400
MIN_PITCH = 1.05  # mm, pre-shear; worst-case shear compression is x0.86


# ===========================================================================
# sheet schedule.  x is mm ACROSS from the frame's left edge, d is mm DOWN
# from the frame's top edge.  Both registers read off ONE column table, which
# is the entire point of the plate: break it and it says nothing.
# ===========================================================================
FRAME_INSET = 3.0

# --- columns (mm across) ---------------------------------------------------
X_INPUT = 17.0
X_CONV = 82.0
X_MAPS = 140.0
X_RELU = 196.0
X_POOL = 249.0
X_ELL = 277.5  # the "..." the plate admits it skips
X_DEEP = 305.0
X_CLS = 340.0
X_PROB = 360.0
X_BRACKET = 372.0
X_PLABEL = 376.0

COLUMNS = (X_CONV, X_MAPS, X_RELU, X_POOL, X_DEEP, X_CLS)

# gentle vertical drift so the chain undulates instead of marching; MIRRORED
# in the backward register, which is what makes the two read as a reflection.
COL_DRIFT = {X_CONV: 0.0, X_MAPS: -7.0, X_RELU: 5.0, X_POOL: -6.0, X_DEEP: 7.0}

# --- vertical schedule (mm down) ------------------------------------------
D_LAB1_F, D_LAB2_F = 9.5, 15.8
D_BAND_F = (22.0, 88.0)
D_SYM_F, D_SHP_F = 96.5, 103.5
D_SWATCH_F = (91.0, 103.0)
D_SWL_F, D_SWS_F = 110.5, 117.5

D_GUTTER = (119.0, 134.0)  # bare paper, crossed only by the column ticks

D_LAB1_B, D_LAB2_B = 139.5, 145.8
D_BAND_B = (152.0, 218.0)
D_SYM_B, D_SHP_B = 226.5, 233.5
D_SWATCH_B = (221.0, 233.0)
D_SWL_B = 240.5

D_LEG_TOP = 243.0
D_LEG_CAP1, D_LEG_CAP2 = 248.0, 253.2
D_LEG_ART = (255.5, 269.0)
D_LEG_BOT = 269.0
D_CNN = 270.5

# --- legend cell dividers (mm across) --------------------------------------
LEG_DIV = (108.0, 173.0, 231.0, 308.0)

# --- type sizes ------------------------------------------------------------
CAP_STAGE = 2.55
CAP_SUB = 2.02
TRACK_SUB = 0.09  # the parenthesised second lines run tight: at full
# tracking '(more abstract spectra)' and '(linear + softmax)' touch, and two
# captions sharing a glyph is the one collision no reader forgives.
CAP_SYM = 3.30
CAP_SHAPE = 2.20
CAP_LEG = 2.15
CAP_REG = 2.85

# --- the seven logits the classifier end is built from ---------------------
LOGITS = (0.4, 1.1, 2.6, 0.9, -0.3, 0.2, 0.6)
TRUE_CLASS = 2


def _softmax(z: Sequence[float]) -> List[float]:
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


PROBS = _softmax(LOGITS)
DLOGITS = [p - (1.0 if k == TRUE_CLASS else 0.0) for k, p in enumerate(PROBS)]


# ===========================================================================
# frame
# ===========================================================================
class Frame:
    def __init__(self, bounds: Bounds, inset: float = FRAME_INSET):
        x0, y0, x1, y1 = bounds
        self.x0, self.y0 = x0 + inset, y0 + inset
        self.x1, self.y1 = x1 - inset, y1 - inset
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0

    def X(self, mm: float) -> float:
        return self.x0 + mm

    def D(self, mm: float) -> float:
        return self.y1 - mm

    def P(self, mm_x: float, mm_d: float) -> Pt:
        return (self.x0 + mm_x, self.y1 - mm_d)


# ===========================================================================
# type — proportional stroke text with optional super/subscript runs
# ===========================================================================
TRACK = 0.17  # extra advance between glyphs, as a fraction of cap height


def _w(text: str, cap: float, track: float = TRACK) -> float:
    return _text_width(text, cap, proportional=True) + len(text) * cap * track


def _lay(
    text: str, x: float, baseline: float, cap: float, pen: Optional[int],
    track: float = TRACK,
) -> List[GCodeCommand]:
    """Proportional stroke type with uniform LETTER-TRACKING.

    The shared font's proportional metrics set lowercase side bearings tight
    enough that 'softmax' and 'non-linearity' collide glyph-to-glyph at caption
    size; the reference's type is monospaced and airy. Monospacing here would
    make '(kernels as wave filters)' 60 mm wide and eat the column gap, so the
    air is bought as tracking instead."""
    sc = cap / 6.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=F_TYPE, proportional=True)
        cx += _glyph_advance(ch) * sc + cap * track
    return out


def _text(
    text: str,
    x: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    align: str = "left",
    track: float = TRACK,
) -> List[GCodeCommand]:
    w = _w(text, cap, track)
    if align == "centre":
        x -= w / 2.0
    elif align == "right":
        x -= w
    return _lay(text, x, baseline, cap, pen, track)


Run = Tuple[str, float, float]  # (text, cap, dy) -- dy in mm above the baseline


def _rich_w(runs: Sequence[Run]) -> float:
    return sum(_w(t, cap) for t, cap, _ in runs)


def _rich(
    runs: Sequence[Run],
    x: float,
    baseline: float,
    pen: Optional[int],
    align: str = "left",
) -> List[GCodeCommand]:
    """A line of type mixing sizes and baselines: ``A^1``, ``H/2^L``, ``p_3``."""
    total = _rich_w(runs)
    if align == "centre":
        x -= total / 2.0
    elif align == "right":
        x -= total
    out: List[GCodeCommand] = []
    cx = x
    for t, cap, dy in runs:
        out += _lay(t, cx, baseline + dy, cap, pen)
        cx += _w(t, cap)
    return out


def _sup(base: str, sup: str, cap: float = CAP_SYM) -> List[Run]:
    return [(base, cap, 0.0), (sup, cap * 0.62, cap * 0.62)]


def _big_sigma(x: float, baseline: float, cap: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Capital sigma — the shared 80-glyph stroke font has no summation sign."""
    s = cap / 6.0
    pts = [
        (x + 3.7 * s, baseline + 6.0 * s),
        (x + 0.3 * s, baseline + 6.0 * s),
        (x + 2.4 * s, baseline + 3.1 * s),
        (x + 0.3 * s, baseline + 0.0 * s),
        (x + 3.9 * s, baseline + 0.0 * s),
    ]
    return _poly(pts, color=pen, f=F_TYPE)


def _sigma_w(cap: float) -> float:
    return 4.9 * cap / 6.0


def _mark(kind: str, x: float, baseline: float, cap: float, pen: Optional[int]):
    """``[``, ``]`` and ``>`` — three more holes in the shared stroke font.
    Drawn in the same 4x6 glyph metric so they track with real type."""
    s = cap / 6.0
    shapes = {
        "[": [[(3.0, 6.0), (1.4, 6.0), (1.4, 0.0), (3.0, 0.0)]],
        "]": [[(1.2, 6.0), (2.8, 6.0), (2.8, 0.0), (1.2, 0.0)]],
        ">": [[(0.8, 4.4), (3.3, 3.0), (0.8, 1.6)]],
    }
    out: List[GCodeCommand] = []
    for st in shapes[kind]:
        out += _poly([(x + gx * s, baseline + gy * s) for gx, gy in st], color=pen, f=F_TYPE)
    return out, 4.6 * s


def _brace(
    x: float, y0: float, y1: float, depth: float, pen: Optional[int]
) -> List[GCodeCommand]:
    """Right-facing curly brace, ``}`` — also missing from the font."""
    ym = (y0 + y1) / 2.0
    pts: Poly = []
    n = 26
    for k in range(n + 1):
        t = k / n
        y = y0 + (y1 - y0) * t
        bulge = math.sin(math.pi * t) ** 0.85
        tip = depth * (1.0 - abs(2 * t - 1)) ** 4
        pts.append((x + depth * 0.55 * bulge - tip * 0.0, y))
    pts.insert(0, (x, y0))
    pts.append((x, y1))
    spike = [(x + depth * 0.55, ym), (x + depth * 1.25, ym)]
    return _poly(pts, color=pen, f=F_TYPE) + _poly(spike, color=pen, f=F_TYPE)


# ===========================================================================
# stroke plumbing
# ===========================================================================
def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _dash(poly: Poly, on: float = 1.3, off: float = 1.0, phase: float = 0.0) -> List[Poly]:
    """Split a polyline into ``on`` mm dashes separated by ``off`` mm.

    The phase is an explicit on/off state with a remaining length, never
    ``arclength % period`` — the modulo form lands epsilon below the switch
    once float error accumulates and the walk never terminates.
    """
    out: List[Poly] = []
    cur: Poly = []
    period = on + off
    if period <= 0:
        return [list(poly)]
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


def _guard(polys: Sequence[Poly], pen: Optional[int], min_dist: float = 0.82,
           f: int = F_DRAW) -> List[GCodeCommand]:
    """``enforce_line_spacing`` + re-emit, so every stroke keeps a leading G0.

    The policy rebuilds strokes and can drop the ``G0`` that positions one; the
    merged program then starts that stroke from the machine origin, which shows
    up as a stray point at (0, 0) and a bounds violation.  Re-emitting from the
    thinned runs is cheap and makes the guard safe to use anywhere.  One pen per
    call, so the colour survives the round-trip.
    """
    cmds = _emit(polys, pen, f=f)
    thinned = enforce_line_spacing(cmds, min_dist=min_dist, resample=0.40)
    runs: List[Poly] = []
    cur: Poly = []
    pending: Optional[Pt] = None
    for c in thinned:
        if c.command == "G0" and c.x is not None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            pending = (c.x, c.y)
        elif c.command == "M3":
            # A NEW stroke starts here whether or not a G0 preceded it. Keying
            # only off G0 is how a dropped positioning move welds two distant
            # strokes together and lays a stray line across the whole sheet.
            if len(cur) >= 2:
                runs.append(cur)
            cur = [pending] if pending is not None else []
            pending = None
        elif c.command == "G1" and c.x is not None:
            cur.append((c.x, c.y))
        elif c.command == "M5":
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            pending = None
    if len(cur) >= 2:
        runs.append(cur)
    return _emit(runs, pen, f=f)


def _smooth(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def _rect_poly(x0: float, y0: float, x1: float, y1: float) -> Poly:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def _disc(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid dot as a tight spiral — small enough that a spiral cannot flood."""
    turns = max(3, int(r / 0.22))
    n = turns * 20
    pts = [
        (
            x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            y + r * (k / n) * math.sin(2 * math.pi * turns * k / n),
        )
        for k in range(n + 1)
    ]
    return _poly(pts, color=pen, f=1600) + circle(x, y, r, pen=pen, f=1600, n=24)


# ===========================================================================
# the plane — a parallelogram with VERTICAL left/right edges whose right edge
# is raised by ``skew`` (the reference's shallow shared axonometric).  All
# texture is authored in plane-local mm and mapped through, so a texture is
# in-bounds by construction and the shear never has to be reasoned about twice.
# ===========================================================================
class Plane:
    def __init__(self, x: float, y: float, w: float, h: float, skew: float):
        self.x, self.y, self.w, self.h, self.skew = x, y, w, h, skew

    def at(self, a: float, b: float) -> Pt:
        return (self.x + a, self.y + b + (a / self.w) * self.skew)

    def map(self, poly: Sequence[Pt]) -> Poly:
        return [self.at(a, b) for a, b in poly]

    def corners(self) -> Poly:
        return [
            self.at(0.0, 0.0),
            self.at(self.w, 0.0),
            self.at(self.w, self.h),
            self.at(0.0, self.h),
            self.at(0.0, 0.0),
        ]

    def region(self, pad: float = 0.0) -> Region:
        return _poly_region(self.corners()[:-1], pad)

    def bbox(self) -> Bounds:
        xs = [p[0] for p in self.corners()]
        ys = [p[1] for p in self.corners()]
        return (min(xs), min(ys), max(xs), max(ys))


def _poly_region(pts: Sequence[Pt], pad: float = 0.0) -> Region:
    """Convex CCW polygon as an intersection of half-planes, grown by ``pad``."""
    hps: List[Region] = []
    n = len(pts)
    for i in range(n):
        ax, ay = pts[i]
        bx, by = pts[(i + 1) % n]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1.0
        nx, ny = dy / L, -dx / L  # outward normal for a CCW ring
        hps.append(HalfPlane(nx, ny, -(nx * ax + ny * ay) - pad))
    return Intersect(*hps)


def _clip_out(polys: Sequence[Poly], region: Optional[Region]) -> List[Poly]:
    if region is None:
        return [list(p) for p in polys]
    out: List[Poly] = []
    for p in polys:
        out.extend(clip(p, region, keep="outside"))
    return out


# ===========================================================================
# the ONE field.  f is the pre-activation A1; everything downstream is
# computed from it, so the forward/backward silhouettes agree by construction.
# ===========================================================================
def field_f(u: float, v: float) -> float:
    """Pre-activation A1 over the unit plane.

    Three low-frequency sinusoids, chosen (over a small search) for the SHAPE
    of their sign set rather than for looks: at these phases 1[f>0] is 47% of
    the plane and is cut by one full-width dead band plus two corner lobes.
    A busy mask is a grey smudge on paper; this one is a silhouette you can
    recognise three columns later, which is the whole argument of the plate.
    """
    return (
        1.00 * math.sin(2 * math.pi * 1.35 * u + 0.90)
        + 0.80 * math.sin(2 * math.pi * 0.95 * v + 2.40)
        + 0.65 * math.sin(2 * math.pi * 1.25 * (u - v) + 1.10)
        - 0.05
    )


def field_relu(u: float, v: float) -> float:
    return max(0.0, field_f(u, v))


def field_grad(u: float, v: float) -> float:
    """Incoming gradient dL/dR1 — a smooth, unrelated field (it comes from
    upstream, it is NOT a function of f).  Gating it by 1[f>0] is what makes
    dL/dA1's silhouette equal the forward ReLU's."""
    return 0.75 * math.sin(2 * math.pi * 0.62 * v + 1.9) + 0.55 * math.cos(
        2 * math.pi * 0.55 * u - 0.7
    )


# --- the ReLU mask boundary, once, as exact iso-0 chains --------------------
_MS_TABLE = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),),
    5: ((3, 2), (0, 1)), 6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),),
    9: ((0, 2),), 10: ((0, 3), (1, 2)), 11: ((1, 2),), 12: ((1, 3),),
    13: ((0, 1),), 14: ((0, 3),),
}


def _iso_chains(fn: Callable[[float, float], float], n: int = 56, iso: float = 0.0):
    """Iso-contour of ``fn`` over the unit square, as chained polylines in (u, v)."""
    g = [[fn(i / n, j / n) for i in range(n + 1)] for j in range(n + 1)]
    segs = []
    for j in range(n):
        for i in range(n):
            a, b = g[j][i], g[j][i + 1]
            c, d = g[j + 1][i + 1], g[j + 1][i]
            case = (
                (1 if a > iso else 0)
                | (2 if b > iso else 0)
                | (4 if c > iso else 0)
                | (8 if d > iso else 0)
            )
            if case in (0, 15):
                continue
            xa, xb = i / n, (i + 1) / n
            ya, yb = j / n, (j + 1) / n

            def lerp(pa, pb, va, vb):
                t = (iso - va) / (vb - va) if vb != va else 0.5
                return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))

            e = (
                lerp((xa, ya), (xb, ya), a, b),
                lerp((xb, ya), (xb, yb), b, c),
                lerp((xb, yb), (xa, yb), c, d),
                lerp((xa, yb), (xa, ya), d, a),
            )
            for p, q in _MS_TABLE[case]:
                segs.append((e[p], e[q]))
    return [list(ch) for ch in _chain_segments(segs)]


MASK_CHAINS = _iso_chains(field_f)


def _mask_frac() -> float:
    n = 48
    on = sum(1 for j in range(n) for i in range(n) if field_f(i / n, j / n) > 0)
    return on / float(n * n)


MASK_FRACTION = _mask_frac()


# ===========================================================================
# plane textures.  Every one is authored in plane-local mm and returns
# polylines in SHEET coordinates.
# ===========================================================================
def tex_wave(
    pl: Plane,
    value: Callable[[float, float], float],
    gate: Optional[Callable[[float, float], bool]] = None,
    n_lines: int = 15,
    amp: float = 3.0,
    n_pts: int = 66,
    inset: float = 1.1,
    dead: Optional[List[Poly]] = None,
) -> List[Poly]:
    """A ridgeline wave train: ``n_lines`` rules displaced by ``value``.

    ``gate`` blanks a line wherever it returns False — this is how the ReLU
    mask survives into the backward register as the SAME silhouette.  Pass a
    list as ``dead`` to CAPTURE the gated-out stretches instead of discarding
    them: the forward ReLU plane needs them, because relu's output there is
    exactly zero, which is a flat baseline and not bare paper.
    """
    w, h = pl.w, pl.h
    aw, ah = w - 2 * inset, h - 2 * inset
    pitch = ah / max(1, n_lines - 1)
    if pitch < MIN_PITCH:
        n_lines = max(2, int(ah / MIN_PITCH) + 1)
        pitch = ah / max(1, n_lines - 1)
    out: List[Poly] = []
    for j in range(n_lines):
        v = j / max(1, n_lines - 1)
        b0 = inset + v * ah
        run: Poly = []
        drun: Poly = []
        for k in range(n_pts + 1):
            u = k / n_pts
            a = inset + u * aw
            if gate is not None and not gate(u, v):
                if len(run) >= 2:
                    out.append(pl.map(run))
                run = []
                if dead is not None:
                    drun.append((a, b0))
                continue
            if dead is not None and len(drun) >= 2:
                dead.append(pl.map(drun))
            drun = []
            run.append((a, b0 + amp * value(u, v)))
        if len(run) >= 2:
            out.append(pl.map(run))
        if dead is not None and len(drun) >= 2:
            dead.append(pl.map(drun))
    return out


def tex_whorl(
    pl: Plane,
    cu: float,
    cv: float,
    rings: int,
    pitch: float = 1.15,
    ecc: float = 1.35,
    rot: float = 0.4,
    wobble: float = 0.16,
    rng: Optional[SeededRNG] = None,
    inset: float = 1.0,
) -> List[Poly]:
    """A conical whorl: concentric rings at a CONSTANT pitch (a linear cone,
    never a Gaussian — Gaussian rings spread exactly at the summit)."""
    w, h = pl.w, pl.h
    cx, cy = inset + cu * (w - 2 * inset), inset + cv * (h - 2 * inset)
    ca, sa = math.cos(rot), math.sin(rot)
    phases = [0.0] * 6
    if rng is not None:
        phases = [rng.uniform(0, 2 * math.pi) for _ in range(6)]
    out: List[Poly] = []
    for k in range(1, rings + 1):
        r = k * pitch
        run: Poly = []
        n = max(28, int(14 * r))
        for m in range(n + 1):
            th = 2 * math.pi * m / n
            wob = 1.0 + wobble * (
                0.6 * math.sin(3 * th + phases[0]) + 0.4 * math.sin(5 * th + phases[1])
            )
            px = r * wob * math.cos(th) * ecc
            py = r * wob * math.sin(th) / ecc
            a = cx + px * ca - py * sa
            b = cy + px * sa + py * ca
            if inset <= a <= w - inset and inset <= b <= h - inset:
                run.append((a, b))
            else:
                if len(run) >= 2:
                    out.append(pl.map(run))
                run = []
        if len(run) >= 2:
            out.append(pl.map(run))
    return out


def tex_lattice(
    pl: Plane,
    nx: int,
    ny: int,
    tone: Optional[Callable[[float, float], float]] = None,
    inset: float = 1.2,
    mark: float = 0.55,
    dy: float = 0.0,
    vertical: bool = False,
) -> List[Poly]:
    """A tick lattice whose MARK LENGTH carries tone (never its spacing — a
    spacing-driven gradient always floods past some tone).

    ``vertical`` turns the tick across its cell's long grid lines: a horizontal
    tick sitting beside a horizontal window rule merges with it and the lattice
    reads as a barcode instead of as cells.
    """
    w, h = pl.w, pl.h
    aw, ah = w - 2 * inset, h - 2 * inset
    out: List[Poly] = []
    for j in range(ny):
        v = (j + 0.5) / ny
        for i in range(nx):
            u = (i + 0.5) / nx
            t = 1.0 if tone is None else max(0.0, min(1.0, tone(u, v)))
            if t < 0.06:
                continue
            a, b = inset + u * aw, inset + v * ah + dy
            L = mark * (0.35 + 0.65 * t)
            out.append(pl.map([(a, b - L), (a, b + L)] if vertical
                              else [(a - L, b), (a + L, b)]))
    return out


def tex_grid(pl: Plane, nx: int, ny: int, inset: float = 1.2) -> List[Poly]:
    w, h = pl.w, pl.h
    aw, ah = w - 2 * inset, h - 2 * inset
    out: List[Poly] = []
    for i in range(nx + 1):
        a = inset + aw * i / nx
        out.append(pl.map([(a, inset), (a, inset + ah)]))
    for j in range(ny + 1):
        b = inset + ah * j / ny
        out.append(pl.map([(inset, b), (inset + aw, b)]))
    return out


def tex_mask_outline(pl: Plane, inset: float = 1.1) -> List[Poly]:
    """The exact iso-0 knife of the ReLU mask, mapped onto a plane."""
    w, h = pl.w, pl.h
    aw, ah = w - 2 * inset, h - 2 * inset
    return [pl.map([(inset + u * aw, inset + v * ah) for u, v in ch]) for ch in MASK_CHAINS]


def tex_glyph_rows(
    pl: Plane, rng: SeededRNG, rows: int, weights: Sequence[float], inset: float = 0.9
) -> List[Poly]:
    """Tiny illegible marks, one row per weight — the classifier matrix.  The
    number of marks in a row is |w| quantised, so the texture carries data."""
    w, h = pl.w, pl.h
    aw, ah = w - 2 * inset, h - 2 * inset
    pitch = ah / rows
    out: List[Poly] = []
    for j in range(rows):
        b = inset + (j + 0.5) * pitch
        mag = weights[j % len(weights)]
        n_marks = 1 + int(3.99 * min(1.0, abs(mag)))
        for m in range(n_marks):
            a = inset + aw * (0.14 + 0.72 * (m + 0.5) / n_marks)
            k = rng.randint(0, 3)
            s = aw * 0.09
            if k == 0:
                out.append(pl.map([(a - s, b - s * 0.6), (a + s, b - s * 0.6), (a + s, b + s * 0.6)]))
            elif k == 1:
                out.append(pl.map([(a - s, b + s * 0.6), (a, b - s * 0.6), (a + s, b + s * 0.6)]))
            elif k == 2:
                out.append(pl.map([(a - s, b), (a + s, b), (a, b + s * 0.7), (a - s, b)]))
            else:
                out.append(pl.map([(a - s, b - s * 0.5), (a + s, b + s * 0.5)]))
    return out


# ===========================================================================
# stacks
# ===========================================================================
def deck(
    cx: float, cy: float, n: int, pw: float, ph: float, skew: float,
    dx_frac: float = 0.30, dy_frac: float = 0.30,
) -> List[Plane]:
    """A receding deck: plane 0 is FARTHEST (back-left-up), plane n-1 NEAREST
    (front-right-down).  Returned far -> near, which is the draw order."""
    dx, dy = dx_frac * pw, dy_frac * ph
    tw = pw + (n - 1) * dx
    th = ph + (n - 1) * dy
    x0 = cx - tw / 2.0
    y1 = cy + th / 2.0
    return [
        Plane(x0 + k * dx, y1 - ph - k * dy, pw, ph, skew) for k in range(n)
    ]


def bank(
    cx: float, cy: float, pw: float, ph: float, skew: float,
    cols: int = 2, rows: int = 3, dxc: float = 0.50, dyc: float = 0.28,
    dxr: float = 0.09, dyr: float = 0.52,
) -> List[Plane]:
    """The staggered filter bank of the convolution column: ``cols`` columns of
    ``rows``, the right column dropped — the reference's 2x3 scatter."""
    dxc, dyc, dxr, dyr = dxc * pw, dyc * ph, dxr * pw, dyr * ph
    tw = pw + (cols - 1) * dxc + (rows - 1) * dxr
    th = ph + (cols - 1) * dyc + (rows - 1) * dyr
    x0, y1 = cx - tw / 2.0, cy + th / 2.0
    out: List[Plane] = []
    for r in range(rows):
        for c in range(cols):
            out.append(
                Plane(
                    x0 + c * dxc + r * dxr,
                    y1 - ph - (c * dyc + r * dyr),
                    pw, ph, skew,
                )
            )
    # far -> near: up-and-left first
    out.sort(key=lambda p: (-p.y, p.x))
    return out


def draw_stack(
    planes: Sequence[Plane],
    textures: Sequence[List[Poly]],
    pens: Sequence[Optional[int]],
    border_pen: Optional[int] = BLACK,
    guard: float = 0.0,
    keep: Optional[Callable[[Pt], bool]] = None,
) -> List[GCodeCommand]:
    """Exact hidden-line for flat planes: each plane's content is clipped OUT of
    the union of the NEARER planes in the stack, so near planes read solid and
    the deck has real depth.  No z-buffer: these are convex polygons.

    ``keep`` additionally cuts the highlighted ribbon's lane out of the texture
    AND the borders, so the one mark that runs in front of everything gets bare
    paper to run on."""
    out: List[GCodeCommand] = []
    for i, pl in enumerate(planes):
        nearer = [p.region(0.0) for p in planes[i + 1:]]
        occl = Union(*nearer) if nearer else None
        tex = _clip_out(textures[i], occl)
        border = _clip_out([pl.corners()], occl)
        if keep is not None:
            tex = _clip_runs(tex, keep)
            border = _clip_runs(border, keep)
        pen = pens[i]
        if guard > 0:
            out += _guard(tex, pen, min_dist=guard)
        else:
            out += _emit(tex, pen, f=2500)
        out += _emit(border, border_pen, f=1900)
    return out


# ===========================================================================
# flow bundles — fan out of one stack, pinch, fan into the next
# ===========================================================================
def strand(
    x0: float, y0: float, xw: float, yw: float, x1: float, y1: float,
    wobble: float = 0.0, phase: float = 0.0, n: int = 74,
) -> Poly:
    """One flow line: smoothstep from the source spread into the waist, then out
    again.  Zero derivative at both ends, so the strand enters and leaves each
    stack flat and the waist joins without a kink."""
    pts: Poly = []
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        if x <= xw:
            t = (x - x0) / max(1e-6, xw - x0)
            y = y0 + (yw - y0) * _smooth(t)
        else:
            t = (x - xw) / max(1e-6, x1 - xw)
            y = yw + (y1 - yw) * _smooth(t)
        if wobble:
            g = math.sin(math.pi * (x - x0) / max(1e-6, x1 - x0))
            y += wobble * g * math.sin(3.1 * math.pi * (x - x0) / max(1e-6, x1 - x0) + phase)
        pts.append((x, y))
    return pts


def bundle(
    rng: SeededRNG,
    x0: float, span0: Tuple[float, float],
    x1: float, span1: Tuple[float, float],
    xw: float, yw: float,
    n: int,
    hot: int,
    gap: float = 1.15,
) -> Tuple[List[Poly], Poly]:
    """``n`` strands from one span to another through a waist at ``(xw, yw)``.

    The waist is sized from the pen tip — ``n * gap`` — so the pinch is a real
    pinch (a 60 mm spread down to ~14 mm) that still never crosses the plotting
    floor.  The reference's waists run at ~0.3 mm and turn solid.
    """
    a0, b0 = span0
    a1, b1 = span1
    out: List[Poly] = []
    hot_poly: Poly = []
    for k in range(n):
        t = (k + 0.5) / n
        ys = a0 + (b0 - a0) * t
        ye = a1 + (b1 - a1) * t
        yw_k = yw + (t - 0.5) * gap * n
        s = strand(
            x0, ys, xw, yw_k, x1, ye,
            wobble=rng.uniform(0.4, 1.5), phase=rng.uniform(0, 6.28),
        )
        if k == hot:
            hot_poly = s
        else:
            out.append(s)
    return out, hot_poly


# ===========================================================================
# the input plate — a square of concentric dotted ripples
# ===========================================================================
def ripple_plate(
    rng: SeededRNG, cx: float, cy: float, size: float, pen: int,
    phase: float = 0.0, k: float = 0.62, taper: float = 1.0,
) -> List[GCodeCommand]:
    """Concentric dotted ripples inside a square frame.

    ``phase`` shifts the ring ladder: the backward plate is drawn at a QUARTER
    PERIOD offset from the forward one, because the gradient of a ripple peaks
    exactly where the ripple crosses zero.  Hold the two plates side by side and
    the rings interleave — that is the statement, not decoration.
    """
    half = size / 2.0
    out: List[GCodeCommand] = []
    out += _emit([_rect_poly(cx - half, cy - half, cx + half, cy + half)], BLACK, f=1900)
    r = 1.1
    ring = 0
    while r < half * 1.40:
        amp = math.cos(2 * math.pi * (k * r + phase))
        dens = 0.30 + 0.70 * (0.5 + 0.5 * amp)
        fall = max(0.0, 1.0 - (r / (half * 1.42)) ** 2.1) ** taper
        dens *= 0.25 + 0.75 * fall
        n = max(8, int(2 * math.pi * r / 1.55))
        j0 = rng.uniform(0, 2 * math.pi)
        for m in range(n):
            if rng.random() > dens:
                continue
            th = j0 + 2 * math.pi * m / n
            px, py = cx + r * math.cos(th), cy + r * math.sin(th)
            if abs(px - cx) > half - 0.7 or abs(py - cy) > half - 0.7:
                continue
            out += _dot(px, py, r=0.30, color=pen)
        r += 1.45
        ring += 1
    return out


# ===========================================================================
# composition
# ===========================================================================
def cnn_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    fr = Frame(bounds)
    X, D, P = fr.X, fr.D, fr.P

    def pen(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    K, B, R = pen(BLACK), pen(BLUE), pen(RED)

    out: List[GCodeCommand] = []
    halos: List[Region] = []

    def halo(x: float, d: float, w: float, cap: float, align: str = "left", pad: float = 1.3):
        if align == "centre":
            x -= w / 2.0
        elif align == "right":
            x -= w
        halos.append(
            Rect(X(x) - pad, D(d) - pad * 0.5, X(x) + w + pad, D(d) + cap + pad * 0.7)
        )

    # ======================================================================
    # 0. type — placed FIRST so the halo set exists before any flow is clipped
    # ======================================================================
    F_STAGES = (
        (X_CONV, "convolution", "(kernels as wave filters)"),
        (X_MAPS, "feature maps", "(frequency responses)"),
        (X_RELU, "non-linearity", "(ReLU)"),
        (X_POOL, "pooling", "(downsample)"),
        (X_DEEP, "deeper layers", "(more abstract spectra)"),
        (X_CLS, "classifier", "(linear + softmax)"),
    )
    for cx, l1, l2 in F_STAGES:
        out += _text(l1, X(cx), D(D_LAB1_F), CAP_STAGE, K, align="centre")
        out += _text(l2, X(cx), D(D_LAB2_F), CAP_SUB, K, align="centre", track=TRACK_SUB)
        halo(cx, D_LAB1_F, _w(l1, CAP_STAGE), CAP_STAGE, "centre")
        halo(cx, D_LAB2_F, _w(l2, CAP_SUB, TRACK_SUB), CAP_SUB, "centre")

    B_STAGES = (
        (X_CONV, [("∂L/∂(conv)", CAP_STAGE, 0.0)], "(filter gradients)"),
        (X_MAPS, [("∂L/∂A", CAP_STAGE, 0.0), ("1", CAP_STAGE * 0.62, CAP_STAGE * 0.62)], ""),
        (X_RELU, [("∂L/∂(ReLU)", CAP_STAGE, 0.0)], "(mask)"),
        (X_POOL, [("∂L/∂P", CAP_STAGE, 0.0), ("1", CAP_STAGE * 0.62, CAP_STAGE * 0.62)], "(unpool)"),
        (X_DEEP, [("∂L/∂A", CAP_STAGE, 0.0), ("L", CAP_STAGE * 0.62, CAP_STAGE * 0.62)], ""),
        (X_CLS, [("∂L/∂z", CAP_STAGE, 0.0)], ""),
        (X_PROB + 6.0, [("∂L/∂W", CAP_STAGE, 0.0), ("c", CAP_STAGE * 0.62, CAP_STAGE * 0.62)],
         "(classifier gradients)"),
    )
    for cx, runs, l2 in B_STAGES:
        out += _rich(runs, X(cx), D(D_LAB1_B), K, align="centre")
        halo(cx, D_LAB1_B, _rich_w(runs), CAP_STAGE, "centre")
        if l2:
            out += _text(l2, X(cx), D(D_LAB2_B), CAP_SUB, K, align="centre",
                         track=TRACK_SUB)
            halo(cx, D_LAB2_B, _w(l2, CAP_SUB, TRACK_SUB), CAP_SUB, "centre")

    # tensor shapes under the forward register
    SHAPES_F = (
        (X_MAPS, _sup("A", "1"), [("H × W × C'", CAP_SHAPE, 0.0)]),
        (X_RELU, _sup("R", "1"), [("H × W × C'", CAP_SHAPE, 0.0)]),
        (X_POOL, _sup("P", "1"), [("H/2 × W/2 × C'", CAP_SHAPE, 0.0)]),
        (X_DEEP, _sup("A", "L"),
         [("H/2", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62),
          (" × W/2", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62),
          (" × C", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62)]),
        (X_CLS, _sup("W", "c"),
         [("C", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62),
          (" × K", CAP_SHAPE, 0.0)]),
    )
    for cx, sym, shp in SHAPES_F:
        out += _rich(sym, X(cx), D(D_SYM_F), K, align="centre")
        out += _rich(shp, X(cx), D(D_SHP_F), K, align="centre")
        halo(cx, D_SYM_F, _rich_w(sym), CAP_SYM, "centre")
        halo(cx, D_SHP_F, _rich_w(shp), CAP_SHAPE, "centre")

    SHAPES_B = (
        (X_MAPS, [("∂L/∂A", CAP_SHAPE, 0.0), ("1", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62)]),
        (X_POOL, [("1 of 2×2", CAP_SHAPE, 0.0)]),
        (X_DEEP, [("H/2", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62),
                  (" × W/2", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62),
                  (" × C", CAP_SHAPE, 0.0), ("L", CAP_SHAPE * 0.62, CAP_SHAPE * 0.62)]),
        (X_CLS, [("p - y", CAP_SHAPE, 0.0)]),
    )
    for cx, shp in SHAPES_B:
        out += _rich(shp, X(cx), D(D_SHP_B), K, align="centre")
        halo(cx, D_SHP_B, _rich_w(shp), CAP_SHAPE, "centre")

    # 1[ A^1 > 0 ] — three of these five marks are missing from the font
    cap = CAP_SHAPE
    parts: List[Tuple[str, str]] = [
        ("t", "1"), ("m", "["), ("t", "A"), ("s", "1"), ("m", ">"), ("t", "0"), ("m", "]")
    ]
    widths = []
    for kind, s in parts:
        if kind == "t":
            widths.append(_w(s + " ", cap))
        elif kind == "s":
            widths.append(_w(s, cap * 0.62))
        else:
            widths.append(4.6 * cap / 6.0 + 0.5)
    cx = X(X_RELU) - sum(widths) / 2.0
    for (kind, s), wd in zip(parts, widths):
        if kind == "t":
            out += _stroke_text(s, cx, D(D_SHP_B), cap, color=K, f=F_TYPE, proportional=True)
        elif kind == "s":
            out += _stroke_text(s, cx, D(D_SHP_B) + cap * 0.62, cap * 0.62, color=K,
                                f=F_TYPE, proportional=True)
        else:
            out += _mark(s, cx, D(D_SHP_B), cap, K)[0]
        cx += wd
    halo(X_RELU, D_SHP_B, sum(widths), CAP_SHAPE, "centre")

    # register labels, top-left of each band.  The plate's second read at 3 m
    # after the two texture bars themselves, so they carry real cap height.
    for lines, d0, arrow_dir, apen in (
        (("forward", "pass", "(activations)"), 26.0, +1, K),
        (("backward", "pass", "(gradients)"), 156.0, -1, K),
    ):
        d = d0
        for ln in lines:
            cap = CAP_REG + 0.75 if ln != lines[-1] else CAP_SUB + 0.3
            out += _text(ln, X(0.0), D(d), cap, apen)
            halo(0.0, d, _w(ln, cap), cap)
            d += 6.6
        ay = D(d - 3.4)
        ax0, ax1 = X(0.0), X(24.0)
        out += _emit([[(ax0, ay), (ax1, ay)]], apen, f=2000)
        out += _emit([[(ax0, ay - 0.34), (ax1, ay - 0.34)]], apen, f=2000)
        tipx = ax1 if arrow_dir > 0 else ax0
        s = -3.0 * arrow_dir
        out += _emit([[(tipx + s, ay + 1.35), (tipx, ay - 0.17), (tipx + s, ay - 1.7)]],
                     apen, f=2000)
        halos.append(Rect(ax0 - 1.5, ay - 2.6, ax1 + 1.5, ay + 2.6))

    # softmax caption + rule (forward, above the probability column)
    sm_cx = X(X_PLABEL - 4.0)
    out += _text("softmax", sm_cx, D(D_BAND_F[0] + 5.0), CAP_STAGE, K, align="centre")
    halo(X_PLABEL - 4.0, D_BAND_F[0] + 5.0, _w("softmax", CAP_STAGE), CAP_STAGE, "centre")
    out += _emit([[(sm_cx, D(D_BAND_F[0] + 8.5)), (sm_cx, D(D_BAND_F[0] + 15.5))]], K, f=2000)

    HALOS = Union(*halos) if halos else None

    # ======================================================================
    # 1. the two registers
    # ======================================================================
    fwd = _register(rng, fr, D_BAND_F, forward=True, pens=(K, B, R), halos=HALOS)
    bwd = _register(rng, fr, D_BAND_B, forward=False, pens=(K, B, R), halos=HALOS)
    out += fwd
    out += bwd

    # ======================================================================
    # 2. column registration ticks across the gutter — the plate's thesis,
    #    stated in the one place where nothing else is allowed to go.
    # ======================================================================
    g0, g1 = D_GUTTER
    for cx in COLUMNS + (X_INPUT, X_PROB):
        line = [(X(cx), D(g0 + 0.5)), (X(cx), D(g1 - 0.5))]
        out += _emit(_dash(line, 0.9, 2.4), K, f=2000)

    # ======================================================================
    # 3. kernel swatch rows (forward W1, backward dL/dW1)
    # ======================================================================
    out += _swatches(rng, fr, D_SWATCH_F, forward=True, pens=(K, B, R))
    out += _swatches(rng, fr, D_SWATCH_B, forward=False, pens=(K, B, R))
    out += _rich(_sup("W", "1"), X(X_CONV), D(D_SWL_F), K, align="centre")
    out += _rich([("k × k × C × C'", CAP_SHAPE, 0.0)], X(X_CONV), D(D_SWS_F), K,
                 align="centre")
    out += _rich(
        [("∂L/∂W", CAP_SYM, 0.0), ("1", CAP_SYM * 0.62, CAP_SYM * 0.62)],
        X(X_CONV), D(D_SWL_B), K, align="centre",
    )

    # ======================================================================
    # 4. legend strip + furniture
    # ======================================================================
    out += _legend(rng, fr, pens=(K, B, R))
    out += _furniture(fr, K)
    return out


# ===========================================================================
# one register (forward or backward)
# ===========================================================================
def _register(
    rng: SeededRNG,
    fr: Frame,
    band: Tuple[float, float],
    forward: bool,
    pens: Tuple[Optional[int], Optional[int], Optional[int]],
    halos: Optional[Region],
) -> List[GCodeCommand]:
    """One register: input plate, six stage stacks, the classifier end, and the
    flow between them.

    Built in two passes.  Pass one places every plane and generates its texture
    but draws nothing; pass two computes the highlighted channel's ribbon,
    KNOCKS THE RIBBON'S CORRIDOR OUT OF EVERY TEXTURE, and only then emits.
    That ordering is the whole reason the ribbon can run in FRONT of the stacks
    instead of hiding behind them: it gets a clean 3.4 mm lane of bare paper the
    whole width of the sheet, so the plate's dominant mark is a decision and not
    an ink-on-ink collision.
    """
    K, B, R = pens
    HOT = B if forward else R  # the highlighted channel / the gradient trace
    X, D = fr.X, fr.D
    d0, d1 = band
    mid = (d0 + d1) / 2.0

    def cy(col: float) -> float:
        return D(mid + (1.0 if forward else -1.0) * COL_DRIFT.get(col, 0.0))

    out: List[GCodeCommand] = []
    blockers: List[Region] = []  # everything the flow must pass BEHIND
    stacks: Dict[float, List[Plane]] = {}
    hot_planes: Dict[float, Plane] = {}
    jobs: List[Tuple[List[Plane], List[List[Poly]], List[Optional[int]]]] = []

    # ---------------------------------------------------------------- input
    # The plate sits 10 mm BELOW the band centre in both registers (not
    # mirrored): the register label block owns the top-left corner of each
    # band, and mirroring the plate would drive it into that block.
    plate_size = 26.0
    px, py = X(X_INPUT), D(mid + 10.0)
    out += ripple_plate(
        rng, px, py, plate_size, HOT,
        phase=0.0 if forward else 0.25,  # gradient peaks where the ripple zeroes
        taper=1.0 if forward else 0.75,
    )
    blockers.append(Rect(px - plate_size / 2, py - plate_size / 2,
                         px + plate_size / 2, py + plate_size / 2))
    if forward:
        out += _rich([("X", 4.2, 0.0)], px, py - plate_size / 2 - 6.4, K, align="centre")
        out += _rich([("H × W × C", CAP_SHAPE, 0.0)], px,
                     py - plate_size / 2 - 11.6, K, align="centre")
        blockers.append(Rect(px - 16.0, py - plate_size / 2 - 13.4, px + 16.0,
                             py - plate_size / 2 - 2.0))
    else:
        # the stacked fraction, as in the reference
        fy = py - plate_size / 2 - 7.0
        out += _rich([("∂L", 3.4, 0.0)], px, fy + 2.4, K, align="centre")
        out += _emit([[(px - 3.4, fy + 1.3), (px + 3.4, fy + 1.3)]], K, f=2000)
        out += _rich([("∂x", 3.4, 0.0)], px, fy - 3.6, K, align="centre")
        blockers.append(Rect(px - 6.5, fy - 4.6, px + 6.5, fy + 7.2))

    # --------------------------------------------------------------- stacks
    # CONV — a 2x3 filter bank of whorls
    conv = bank(X(X_CONV), cy(X_CONV), 17.0, 21.0, 5.0)
    stacks[X_CONV] = conv
    conv_tex: List[List[Poly]] = []
    conv_pens: List[Optional[int]] = []
    conv_eyes: List[GCodeCommand] = []
    for i, pl in enumerate(conv):
        # The bank steps right and DOWN, so a far plane is exposed only on its
        # upper-left sliver; an eye placed at random lands behind a nearer
        # plane and two of six filters come out blank. Walk the eye from the
        # exposed corner on the far planes to the centre on the near ones.
        f_i = i / (len(conv) - 1.0)
        cu = 0.30 + 0.45 * f_i ** 2 + 0.06 * ((i * 7) % 3)
        cv = 0.74 - 0.40 * f_i ** 2 - 0.05 * ((i * 5) % 3)
        rings = 7 if forward else 4  # gradients CONCENTRATE at the eye
        tex = tex_whorl(pl, cu, cv, rings, pitch=1.35, ecc=1.26 + 0.14 * (i % 3),
                        rot=0.35 + 0.42 * i, rng=rng)
        hot_plane = (i == 4)
        if hot_plane:
            hot_planes[X_CONV] = pl
        if not forward:
            ecx, ecy = pl.at(1.0 + cu * (pl.w - 2.0), 1.0 + cv * (pl.h - 2.0))
            conv_eyes += _disc(ecx, ecy, 0.85, HOT if hot_plane else K)
        conv_tex.append(tex)
        conv_pens.append(HOT if hot_plane else K)
    jobs.append((conv, conv_tex, conv_pens))

    # MAPS (A1 / dL/dA1) and RELU (R1 / the mask) share a plane size: conv and
    # the non-linearity do not change H x W, and the plate has to say so.
    def gate(u: float, v: float) -> bool:
        return field_f(u, v) > 0.0

    for col, kind in ((X_MAPS, "maps"), (X_RELU, "relu")):
        pls = deck(X(col), cy(col), 4, 18.0, 22.5, 5.6, dx_frac=0.34, dy_frac=0.34)
        stacks[col] = pls
        tex: List[List[Poly]] = []
        tp: List[Optional[int]] = []
        for i, pl in enumerate(pls):
            hot_plane = (i == 2)
            if hot_plane:
                hot_planes[col] = pl
            if kind == "maps":
                if forward:
                    t = tex_wave(pl, field_f, None, n_lines=19, amp=2.05)
                else:
                    # dL/dA1 = dL/dR1 * 1[A1 > 0]  ->  GATED
                    t = tex_wave(pl, field_grad, gate, n_lines=19, amp=2.05)
                    t += tex_mask_outline(pl)
            else:
                if forward:
                    # R1 = max(0, A1).  Live lobes keep the full excursion; the
                    # dead region is a flat baseline (relu's output there is
                    # exactly zero, not absent), drawn as a sparse dotted rule
                    # on every third row so it reads QUIETER than the lobes.
                    dead: List[Poly] = []
                    t = tex_wave(pl, field_relu, gate, n_lines=19, amp=2.05, dead=dead)
                    for di, q in enumerate(dead):
                        if di % 3 == 0:
                            t += _dash(q, 0.42, 2.3)
                    t += tex_mask_outline(pl)
                else:
                    # the mask itself: hatched where 1, bare paper where 0
                    t = tex_wave(pl, lambda u, v: 0.0, gate, n_lines=17, amp=0.0)
                    t += tex_mask_outline(pl)
            tex.append(t)
            tp.append(HOT if hot_plane else K)
        jobs.append((pls, tex, tp))

    # POOL — forward P1 is the COARSE map, one mark in every window cell.
    # Backward dL/dP1 unpools onto the same windows, each quartered by a dotted
    # cross, with exactly ONE mark, in the argmax quadrant: the same 30 marks on
    # 120 cells, so the gradient plane sits at a quarter of its twin's occupancy
    # and the drawn subdivision is what makes that visible rather than merely
    # true.
    NX, NY = 10, 12
    pls = deck(X(X_POOL), cy(X_POOL), 5, 15.0, 18.6, 4.4, dx_frac=0.34, dy_frac=0.34)
    stacks[X_POOL] = pls
    tex, tp = [], []
    for i, pl in enumerate(pls):
        hot_plane = (i == 3)
        if hot_plane:
            hot_planes[X_POOL] = pl
        t = tex_grid(pl, NX // 2, NY // 2)
        t += _pool_marks(pl, NX, NY, forward)
        tex.append(t)
        tp.append(HOT if hot_plane else K)
    jobs.append((pls, tex, tp))

    # DEEP — smaller planes, MORE of them: H,W shrink while C grows.
    pls = deck(X(X_DEEP), cy(X_DEEP), 7, 11.0, 13.6, 3.4, dx_frac=0.34, dy_frac=0.34)
    stacks[X_DEEP] = pls
    tex, tp = [], []
    for i, pl in enumerate(pls):
        hot_plane = (i == 5)
        if hot_plane:
            hot_planes[X_DEEP] = pl
        val = (lambda u, v, i=i: 0.85 * math.sin(2 * math.pi * 0.55 * u + 1.1 * v + 0.6 * i)) \
            if forward else \
            (lambda u, v, i=i: 0.80 * math.cos(2 * math.pi * 0.48 * v - 0.9 * u + 0.5 * i))
        tex.append(tex_wave(pl, val, None, n_lines=11, amp=1.7, inset=0.9))
        tp.append(HOT if hot_plane else K)
    jobs.append((pls, tex, tp))

    # CLASSIFIER bar
    bar_h = 48.0
    bar_w = 6.6
    bx, by = X(X_CLS) - bar_w / 2.0, cy(X_CLS) - bar_h / 2.0
    bar = Plane(bx, by, bar_w, bar_h, 0.0)
    rows = 26
    wts = [abs(math.sin(2.3 * k + 0.7)) for k in range(rows)] if forward else \
          [abs(math.cos(1.7 * k + 0.2)) for k in range(rows)]
    bar_tex = tex_glyph_rows(bar, rng, rows, wts)
    blockers.append(Rect(bx - 0.8, by - 0.8, bx + bar_w + 0.8, by + bar_h + 0.8))

    for pls in stacks.values():
        for pl in pls:
            blockers.append(pl.region(0.9))

    # -------------------------------------------------- probabilities / tiles
    n_cls = len(PROBS)
    col_h = 36.0
    ptop = cy(X_CLS) + col_h / 2.0
    node_ys = [ptop - col_h * k / (n_cls - 1) for k in range(n_cls)]
    if forward:
        out += _softmax_column(fr, node_ys, pens)
    else:
        out += _grad_tiles(fr, node_ys, pens)
    blockers.append(Rect(X(X_PROB) - 3.5, min(node_ys) - 4.5, fr.x1, max(node_ys) + 4.5))

    # ---------------------------------------------------------------- flow
    # the "..." the plate admits it skips is a hole in the flow, not a mark on
    # top of it
    blockers.append(Rect(X(X_ELL) - 6.5, D(mid) - 3.8, X(X_ELL) + 6.5, D(mid) + 3.8))
    BLOCK = Union(*blockers, *([halos] if halos is not None else []))

    def span(col: float, side: str) -> Tuple[float, float, float]:
        """(x at the stack edge, y_lo, y_hi) of a column's silhouette."""
        pl_list = stacks[col]
        xs = [c[0] for pl in pl_list for c in pl.corners()]
        ys = [c[1] for pl in pl_list for c in pl.corners()]
        x = min(xs) if side == "left" else max(xs)
        return (x, min(ys) + 1.5, max(ys) - 1.5)

    def hot_edge(col: float, side: str) -> Pt:
        """Mid-height of the highlighted plane's left/right edge."""
        pl = hot_planes[col]
        return pl.at(0.0 if side == "left" else pl.w, pl.h / 2.0)

    gaps: List[Tuple[float, Tuple[float, float], float, Tuple[float, float], int, Pt, Pt]] = []
    # input plate -> conv: the pinch is AT the plate, and the fan is huge
    lx, lo, hi = span(X_CONV, "left")
    gaps.append((px + 13.0, (py - 0.9, py + 0.9), lx, (lo, hi), 19,
                 (px + 13.0, py), hot_edge(X_CONV, "left")))
    prev = X_CONV
    for col in (X_MAPS, X_RELU, X_POOL, X_DEEP):
        ax, alo, ahi = span(prev, "right")
        bx2, blo, bhi = span(col, "left")
        gaps.append((ax, (alo, ahi), bx2, (blo, bhi), 19,
                     hot_edge(prev, "right"), hot_edge(col, "left")))
        prev = col
    # deep -> classifier bar (a hard pinch into the matrix)
    ax, alo, ahi = span(X_DEEP, "right")
    gaps.append((ax, (alo, ahi), bx - 0.5, (cy(X_CLS) - 1.2, cy(X_CLS) + 1.2), 21,
                 hot_edge(X_DEEP, "right"), (bx - 0.5, cy(X_CLS))))

    flow_hot: List[Poly] = []
    flow_cold: List[Poly] = []
    hots: List[Poly] = []
    for x0, s0, x1, s1, n, ha, hb in gaps:
        yw = ((s0[0] + s0[1]) / 2.0 + (s1[0] + s1[1]) / 2.0) / 2.0
        xw = x0 + (x1 - x0) * (0.52 if s1[1] - s1[0] > 6 else 0.80)
        strands, _ = bundle(rng, x0, s0, x1, s1, xw, yw, n, hot=-1, gap=0.92)
        # two strands in the register's pen for every one in black — the
        # reference's mixed dotted wash, with the colour carrying the pass.
        for k, s in enumerate(strands):
            (flow_cold if k % 3 == 2 else flow_hot).append(s)
        # The highlighted channel does NOT ride the middle of the bundle: it
        # runs from the previous stack's BLUE plane to the next one's, so the
        # ribbon visibly climbs and drops with the stage it belongs to. Riding
        # the bundle's midline gave a flat highlighter bar across the sheet.
        hots.append(strand(ha[0], ha[1], (ha[0] + hb[0]) / 2.0,
                           (ha[1] + hb[1]) / 2.0, hb[0], hb[1], n=60))

    # The ribbon is ONE line: the per-gap hot strands are stitched THROUGH each
    # stack, entering its blue plane on the left and leaving on the right, so
    # the highlighted channel crosses the whole sheet without a break.
    ribbon: Poly = []
    for h in hots:
        if ribbon:
            a, b = ribbon[-1], h[0]
            n = 26
            ribbon += [
                (a[0] + (b[0] - a[0]) * m / n, a[1] + (b[1] - a[1]) * _smooth(m / n))
                for m in range(1, n)
            ]
        ribbon += h
    ribbons = [ribbon]

    # long carriers: the reference's full-width wash, kept to 9 well-separated
    # sweeps instead of ~60 at sub-millimetre spacing.
    cx0, cx1 = px + 3.0, X(X_CLS) + 20.0
    for k in range(15):
        t = (k + 0.5) / 15.0
        amp = 7.0 + 12.0 * math.sin(math.pi * t)
        base = cy(X_CONV) + (t - 0.5) * 66.0
        ph = rng.uniform(0, 6.28)
        carrier = [
            (
                cx0 + (cx1 - cx0) * m / 220.0,
                base + amp * math.sin(2 * math.pi * 1.3 * m / 220.0 + ph) * 0.34,
            )
            for m in range(221)
        ]
        (flow_hot if k % 2 else flow_cold).append(carrier)

    # ------------------------------------------------- the ribbon's lane
    lane = _Corridor(ribbons, 1.45)
    keep = lambda p: not lane.near(p)

    # ------------------------------------------------- draw, back to front
    for pl_list, tex_list, pen_list in jobs:
        out += draw_stack(pl_list, tex_list, pen_list, border_pen=K, guard=0.80, keep=keep)
    out += conv_eyes
    out += _emit(_clip_runs(bar_tex, keep), K, f=2500)
    out += _emit([bar.corners()], K, f=1900)

    for polys, p, on, off in ((flow_hot, HOT, 3.0, 1.8), (flow_cold, K, 2.6, 2.2)):
        dashed: List[Poly] = []
        for i, q in enumerate(_clip_runs(_clip_out(polys, BLOCK), keep)):
            dashed += _dash(q, on, off, phase=(i * 0.63) % (on + off))
        out += _guard(dashed, p, min_dist=0.78, f=2600)

    # The highlighted channel: ONE solid FIVE-pass ribbon, ~1.1 mm wide, running
    # the full width IN FRONT of every stack inside the lane cut for it above.
    # Scarce and loud, and the plate's 3 m read — one blue ribbon going right
    # over one red ribbon coming back.
    for p in (_clip_out(ribbons, halos) if halos is not None else ribbons):
        for dy in (-0.45, -0.15, 0.15, 0.45):
            out += _emit([[(q[0], q[1] + dy) for q in p]], HOT, f=2200)
    # …and it points: the arrowhead states the direction of the pass.
    ahx = X(X_CLS) - 12.0 if forward else px + 15.5
    ahy = cy(X_CLS) if forward else py
    d = 1.0 if forward else -1.0
    out += _emit([[(ahx - 3.6 * d, ahy + 2.0), (ahx, ahy), (ahx - 3.6 * d, ahy - 2.0)]],
                 HOT, f=2000)
    out += _emit([[(ahx - 3.6 * d, ahy + 1.55), (ahx - 0.5 * d, ahy),
                   (ahx - 3.6 * d, ahy - 1.55)]], HOT, f=2000)

    return out


class _Corridor:
    """A spatial hash of the highlighted ribbon's centreline, used to cut a
    clean lane of bare paper through every texture it crosses.

    Polygon Regions are the right tool for a plane; they are the wrong tool for
    a 300 mm polyline (a Union of 450 rectangles is 1800 half-plane tests per
    segment).  This answers the only question that matters — "is this point
    within ``half`` mm of the ribbon" — in O(1), and ``kit._clip_runs`` bisects
    the boundary to 14 digits, so the cut still lands exactly on the lane edge.
    """

    def __init__(self, polys: Sequence[Poly], half: float):
        self.half = half
        self.cell = half * 2.0
        self.grid: Dict[Tuple[int, int], List[Pt]] = {}
        step = half * 0.7
        for p in polys:
            for a, b in zip(p, p[1:]):
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                n = max(1, int(L / step))
                for m in range(n + 1):
                    t = m / n
                    q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                    self.grid.setdefault(
                        (int(q[0] / self.cell), int(q[1] / self.cell)), []
                    ).append(q)

    def near(self, p: Pt) -> bool:
        ci, cj = int(p[0] / self.cell), int(p[1] / self.cell)
        h2 = self.half * self.half
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for qx, qy in self.grid.get((ci + di, cj + dj), ()):
                    if (qx - p[0]) ** 2 + (qy - p[1]) ** 2 < h2:
                        return True
        return False


def _pool_marks(pl: Plane, nx: int, ny: int, forward: bool,
                inset: float = 1.2) -> List[Poly]:
    """The pooling pair, drawn on ONE shared lattice so the sparsity is a fact
    you can see rather than one you have to be told.

    Both planes carry the same 2x2 window grid.  FORWARD puts a short tick in
    every live fine cell and a LONG tick in the cell each window selected — the
    map arriving, partitioned, with the pooled winners called out.  BACKWARD
    keeps only the long ticks: unpooling sends the gradient to one cell per
    window and nothing anywhere else.  Same lattice, a quarter of the marks.

    Windows the forward pass rectified away entirely get nothing in either
    plane, which is also exact: no gradient flows back through a dead window.
    """
    w, h = pl.w, pl.h
    aw, ah = w - 2 * inset, h - 2 * inset
    out: List[Poly] = []
    for j in range(ny // 2):
        for i in range(nx // 2):
            best, arg = -1.0, (0, 0)
            for dj in (0, 1):
                for di in (0, 1):
                    uu = (2 * i + di + 0.5) / nx
                    vv = (2 * j + dj + 0.5) / ny
                    val = field_relu(uu, vv)
                    if val > best:
                        best, arg = val, (di, dj)
            if best <= 0.02:
                continue
            for dj in (0, 1):
                for di in (0, 1):
                    u = (2 * i + di + 0.5) / nx
                    v = (2 * j + dj + 0.5) / ny
                    a, b = inset + u * aw, inset + v * ah
                    if (di, dj) == arg:
                        L = 0.52 + 0.58 * min(1.0, best / 1.9)
                        out.append(pl.map([(a, b - L), (a, b + L)]))
                    elif forward:
                        val = field_relu(u, v)
                        if val <= 0.02:
                            continue
                        L = 0.22 + 0.24 * min(1.0, val / 1.9)
                        out.append(pl.map([(a, b - L), (a, b + L)]))
    return out


# ===========================================================================
# the classifier end
# ===========================================================================
def _softmax_column(fr: Frame, node_ys: Sequence[float], pens) -> List[GCodeCommand]:
    K, B, R = pens
    X, D = fr.X, fr.D
    out: List[GCodeCommand] = []
    nx = X(X_PROB)
    for k, y in enumerate(node_ys):
        p = PROBS[k]
        r = 0.72 + 0.95 * math.sqrt(p)
        winner = k == TRUE_CLASS
        out += circle(nx, y, r, pen=B if winner else K, f=1800, n=40)
        if winner:
            out += _disc(nx, y, r * 0.52, B)
        # a tick whose LENGTH is p_k exactly: one clear winner, the rest small
        bar_len = 15.0 * p
        wpen = B if winner else K
        out += _emit([[(nx + r + 0.9, y), (nx + r + 0.9 + bar_len, y)]], wpen, f=2000)
        if winner:
            out += _emit([[(nx + r + 0.9, y + 0.38), (nx + r + 0.9 + bar_len, y + 0.38)]],
                         wpen, f=2000)
            out += _emit([[(nx + r + 0.9, y - 0.38), (nx + r + 0.9 + bar_len, y - 0.38)]],
                         wpen, f=2000)
    # bracket + p labels
    y0, y1 = min(node_ys), max(node_ys)
    bxx = X(X_BRACKET)
    out += _emit([[(bxx + 1.4, y1), (bxx, y1), (bxx, y0), (bxx + 1.4, y0)]], K, f=2000)
    labels = ["1", "2", "3", "", "", "", "K"]
    for k, y in enumerate(node_ys):
        if not labels[k]:
            continue
        out += _rich(
            [("p", 3.0, 0.0), (labels[k], 1.95, -0.95)],
            X(X_PLABEL), y - 1.1, B if k == TRUE_CLASS else K,
        )
    midy = (node_ys[3] + node_ys[5]) / 2.0
    for dy in (-1.5, 0.0, 1.5):
        out += _dot(X(X_PLABEL) + 1.2, midy + dy, r=0.32, color=K)
    return out


def _grad_tiles(fr: Frame, node_ys: Sequence[float], pens) -> List[GCodeCommand]:
    """Per-class gradient tiles: line density is |p_k - y_k|, exactly."""
    K, B, R = pens
    X = fr.X
    out: List[GCodeCommand] = []
    nx = X(X_PROB)
    gmax = max(abs(g) for g in DLOGITS)
    for k, y in enumerate(node_ys):
        g = abs(DLOGITS[k]) / gmax
        tpen = R if k == TRUE_CLASS else K
        out += _disc(nx, y, 0.62 + 0.55 * g, tpen)
        tx0 = X(X_PLABEL) - 4.0
        sw, sh = 6.6, 5.4
        out += _emit([_rect_poly(tx0, y - sh / 2, tx0 + sw, y + sh / 2)], tpen, f=1900)
        # spacing is FIXED at 0.9 mm and the NUMBER of lines carries |p - y|;
        # a density-by-spacing tile floods solid on the true class.
        n_lines = int(round(1 + 4 * g))
        for m in range(n_lines):
            yy = y - sh / 2 + sh * (m + 0.5) / n_lines
            out += _emit([[(tx0 + 0.45, yy), (tx0 + sw - 0.45, yy)]], tpen, f=2200)
        out += _emit([[(nx + 1.8, y), (tx0 - 1.2, y)]], K, f=2100)
    return out


# ===========================================================================
# kernel swatch rows
# ===========================================================================
def _swatches(
    rng: SeededRNG, fr: Frame, band: Tuple[float, float], forward: bool, pens
) -> List[GCodeCommand]:
    K, B, R = pens
    X, D = fr.X, fr.D
    d0, d1 = band
    size = d1 - d0
    out: List[GCodeCommand] = []
    gap = 5.5
    total = 3 * size + 2 * gap
    x0 = X(X_CONV) - total / 2.0
    for k in range(3):
        sx = x0 + k * (size + gap)
        sy = D(d1)
        pl = Plane(sx, sy, size, size, 0.0)
        pen = K
        if forward and k == 1:
            pen = B
        if (not forward) and k == 1:
            pen = R
        if k == 0:
            tex = tex_lattice(
                pl, 7, 7,
                tone=lambda u, v: 0.30 + 0.70 * abs(math.sin(5.0 * u + 4.0 * v)),
                mark=0.45, inset=1.0,
            )
        elif k == 1:
            tex = tex_whorl(pl, 0.5, 0.5, 4 if forward else 3, pitch=1.25, ecc=1.02,
                            rot=0.0, wobble=0.05, inset=0.9)
            tex += tex_lattice(pl, 5, 5, tone=lambda u, v: 0.4, mark=0.30, inset=1.2)
        else:
            tex = tex_whorl(pl, 0.5, 0.5, 4, pitch=1.30, ecc=1.02, rot=0.0,
                            wobble=0.02, inset=0.9)
        out += _emit(tex, pen, f=2500)
        out += _emit([pl.corners()], K, f=1900)
    return out


# ===========================================================================
# legend strip
# ===========================================================================
def _legend(rng: SeededRNG, fr: Frame, pens) -> List[GCodeCommand]:
    K, B, R = pens
    X, D = fr.X, fr.D
    out: List[GCodeCommand] = []
    for dx in LEG_DIV:
        out += _emit([[(X(dx), D(D_LEG_TOP)), (X(dx), D(D_LEG_BOT))]], K, f=2000)

    a0, a1 = D_LEG_ART
    amid = (a0 + a1) / 2.0

    def cap(lines: Sequence[str], x: float) -> None:
        nonlocal out
        for i, ln in enumerate(lines):
            out += _text(ln, X(x), D(D_LEG_CAP1 + i * 5.2), CAP_LEG, K)

    # --- 1. convolution = local correlation -------------------------------
    # indented 9 mm from the frame so the bottom-left registration cross keeps
    # its own paper; in the reference the cross sits clear to the left too.
    cap(("convolution = local correlation", "(in frequency domain)"), 15.0)
    gp = Plane(X(17.0), D(a1), 11.0, 11.0, 0.0)
    out += _emit(tex_grid(gp, 4, 4, inset=0.0), K, f=2300)
    for (i, j) in ((1, 1), (2, 2), (1, 2)):
        out += _dot(X(17.0) + (i + 0.5) * 2.75, D(a1) + (j + 0.5) * 2.75, r=0.3, color=K)
    out += _text("∗", X(31.5), D(amid + 1.4), 3.2, K)
    out += _wave_cluster(X(37.0), D(amid), 21.0, 3.4, 4, B, K, phase=0.0)
    out += _text("=", X(61.5), D(amid + 1.0), 2.8, K)
    out += _wave_cluster(X(67.0), D(amid), 23.0, 3.4, 4, B, K, phase=1.6, tighten=True)

    # --- 2. non-linearity (ReLU) ------------------------------------------
    cap(("non-linearity (ReLU)",), 116.0)
    ax, ay = X(124.0), D(a1 - 3.6)
    out += _emit([[(ax, ay + 9.4), (ax, ay), (ax + 24.0, ay)]], K, f=2000)
    out += _emit([[(ax + 2.0, ay), (ax + 12.0, ay), (ax + 22.0, ay + 8.6)]], R, f=2000)
    out += _emit([[(ax + 2.4, ay + 0.34), (ax + 12.0, ay + 0.34), (ax + 21.6, ay + 8.9)]],
                 R, f=2000)
    out += _text("y = max(0, x)", X(124.0), D(D_LEG_BOT + 0.6), CAP_LEG - 0.15, K)

    # --- 3. pooling -------------------------------------------------------
    cap(("pooling (e.g. 2 × 2)",), 179.0)
    p1 = Plane(X(181.0), D(a1), 12.0, 12.0, 0.0)
    out += _emit(tex_grid(p1, 4, 4, inset=0.0), K, f=2300)
    out += _emit([[(X(196.5), D(amid)), (X(204.0), D(amid))]], K, f=2000)
    out += _emit([[(X(202.0), D(amid) + 1.1), (X(204.0), D(amid)),
                   (X(202.0), D(amid) - 1.1)]], K, f=2000)
    p2 = Plane(X(206.5), D(amid + 3.4), 6.8, 6.8, 0.0)
    out += _emit(tex_grid(p2, 2, 2, inset=0.0), K, f=2300)

    # --- 4. softmax -------------------------------------------------------
    cap(("softmax",), 237.0)
    fx0, fx1 = X(236.0), X(268.0)
    for k in range(6):
        t = (k + 0.5) / 6.0
        y0 = D(a1) + (a1 - a0) * t
        y1 = D(amid) + (t - 0.5) * 8.0
        pw = B if k in (2, 3) else K
        out += _emit([strand(fx0, y0, (fx0 + fx1) / 2, (y0 + y1) / 2, fx1, y1, n=34)],
                     pw, f=2300)
    for k in range(6):
        t = (k + 0.5) / 6.0
        out += circle(fx1 + 1.2, D(amid) + (t - 0.5) * 8.0, 0.52, pen=K, f=1800, n=16)
    out += _brace(fx1 + 3.2, D(amid) - 5.4, D(amid) + 5.4, 2.4, K)
    sx = fx1 + 8.0
    out += _stroke_text("σ", sx, D(amid) - 1.2, 3.0, color=K, f=F_TYPE, proportional=True)
    out += _stroke_text("(z)", sx + _sigma_w(3.0), D(amid) - 1.2, 3.0, color=K, f=F_TYPE,
                        proportional=True)

    # --- 5. loss ----------------------------------------------------------
    cap(("loss (e.g. cross-entropy)",), 314.0)
    lx, ly = X(320.0), D(amid - 0.6)
    cx = lx
    out += _stroke_text("L  =  -", cx, ly, 2.8, color=K, f=F_TYPE, proportional=True)
    cx += _w("L  =  -", 2.8) + 1.2
    out += _big_sigma(cx, ly - 0.7, 4.4, K)
    out += _stroke_text("i", cx + 0.8, ly - 4.0, 1.9, color=K, f=F_TYPE, proportional=True)
    cx += _sigma_w(4.4) + 1.6
    out += _rich(
        [("y", 2.8, 0.0), ("i", 1.8, -0.9), (" log p", 2.8, 0.0), ("i", 1.8, -0.9)],
        cx, ly, K,
    )
    return out


def _wave_cluster(
    x: float, y: float, w: float, amp: float, n: int,
    pen_hot: Optional[int], pen_cold: Optional[int],
    phase: float = 0.0, tighten: bool = False,
) -> List[GCodeCommand]:
    """A small bundle of sine curves — the legend's 'wave filter' mark."""
    out: List[GCodeCommand] = []
    for k in range(n):
        t = (k - (n - 1) / 2.0) / max(1, n - 1)
        f = 1.5 + (0.35 * k if not tighten else 0.12 * k)
        a = amp * (1.0 - 0.35 * abs(t) * (2.0 if tighten else 1.0))
        pts = [
            (x + w * m / 60.0, y + a * math.sin(2 * math.pi * f * m / 60.0 + phase + 1.3 * t))
            for m in range(61)
        ]
        out += _poly(pts, color=pen_hot if abs(t) < 0.26 else pen_cold, f=2400)
    return out


# ===========================================================================
# furniture
# ===========================================================================
def _furniture(fr: Frame, K: Optional[int]) -> List[GCodeCommand]:
    X, D = fr.X, fr.D
    out: List[GCodeCommand] = []
    for x, d in ((5.0, 5.0), (fr.w - 5.0, 5.0), (5.0, fr.h - 5.0), (fr.w - 5.0, fr.h - 5.0)):
        cx, cy = X(x), D(d)
        out += _emit([[(cx - 4.2, cy), (cx + 4.2, cy)]], K, f=2000)
        out += _emit([[(cx, cy - 4.2), (cx, cy + 4.2)]], K, f=2000)
    out += _text("C N N", X(fr.w - 16.0), D(D_CNN), 2.5, K, align="right")
    # the ellipsis the plate admits it skips — solid discs, not pen scratches:
    # a 1.4 mm dash disappears into a field of 1.4 mm flow dashes
    for dx in (-4.2, 0.0, 4.2):
        out += _disc(X(X_ELL) + dx, D((D_BAND_F[0] + D_BAND_F[1]) / 2.0), 0.85, K)
        out += _disc(X(X_ELL) + dx, D((D_BAND_B[0] + D_BAND_B[1]) / 2.0), 0.85, K)
    return out
