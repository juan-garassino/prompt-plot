"""ATTENTION — FORWARD AND BACKWARD.  Faithful recreation, r01.

Recreation of ``studio/attention-passes/ref/reference.png`` with the brief's
explicit licence to fix the reference's crowding (DESIGN_RUBRIC dimension 4:
"OVERLAP IS A DECISION, NEVER A SYMPTOM" outranks fidelity).

Layout is expressed in normalised sheet coordinates ``(u, v)``, u = 0 left ..
1 right, v = 0 TOP .. 1 bottom, mapped onto a composition frame inset inside
the drawable area — the ``convolutions`` idiom.  The stage columns come from
the reference, measured off the 1499 px raster: well nodes u = 0.165
(ref 188/1499), similarity 0.428 (660), weighted values 0.832 (1228),
Z 0.952 (1430).  Softmax is the ONE column that moved — 0.618 against the
reference's 0.584 — because the funnel between similarity and softmax is the
plate's argument and at the reference's spacing it had 12 mm to happen in.

WHAT IS TRUE HERE (every mark carries a number)
-----------------------------------------------
* ``S = Q Kᵀ / sqrt(d)`` is computed from real sinusoidal positional encodings
  pushed through two seeded projections (d = 24) — the lattice's 28 x 34 dot
  radii ARE |S_ij|, and its axis ticks say which way the matrix runs.
* The comb is ``softmax(S[q*] / 0.20)`` over those same 34 keys: tick length
  is the weight, INK PASSES are the weight (one extra pass per 6 % of mass),
  and the ticks sum to one.  At seed 7 the top weight is 0.18 against a
  1/34 = 0.029 uniform floor, the next 0.14, and 8 of 34 fall under 0.005 —
  visibly peaked, with a real tail, and still ~26 ticks of dense comb.
* ``q*`` is chosen, and the choice is stated: among the sharpest rows, the one
  whose peak key lies nearest the middle of the key axis.  Its lattice row is
  bracketed on the right-hand edge.
* Right of the comb the fans are positioned by the INVERSE CDF of that same
  distribution, so line density IS probability mass — "weighted values" is not
  a caption, it is where the lines bunch.  Each bead on that rule sits where a
  line crosses and is sized by the magnitude that line carries.
* The backward comb replays the IDENTICAL weight vector at 0.58 amplitude —
  dL/dV is the attention weights re-applied, so the two combs are one
  silhouette drawn twice.

THE THREE WELLS ARE THREE DIFFERENT ORDERS (the brief's hard requirement — a
previous version of this subject was rejected for Q and K reading as twins)
* Q = DIRECTION.  Confocal parabolic WAVEFRONTS, ``r = p/(1 − cos t)`` about
      the node: vertices march LEFT from the focus and the arms open RIGHT
      along the row, so every ray leaving the focus exits parallel and hands
      straight over to the bundle.  OPEN curves, never closed.  Vertex pitch
      0.80 mm.  The flattest and smallest of the three (20 x 40 mm).
* K = FIELD.  A union-of-cones nest over FOUR cusps of different strength,
      analytic (the boundary of a union of discs; F = max_i (a_i − r_i) is
      conical so |grad F| = 1 and the ring pitch is 1.25 mm everywhere by
      construction).  The cusps are spread far enough that even the outermost
      level shows the concave notches where the lobes merge.  CLOSED, lumpy,
      multi-centred, and the biggest of the three (33 x 42 mm).
* V = STRATA.  A lobed silhouette filled with horizontal laminae at FIXED
      1.45 mm spacing whose dash duty is that row's value-vector norm (rubric:
      "tone drives DUTY, never SPACING").  No rings at all, one direction only.

ROW REGISTRATION.  The gradient wells are a RIGID translation of the forward
ones by dv = 0.452 (123.4 mm): every gradient well centre sits at exactly
``row + dv``, all six nodes share the column u = 0.165, and Z / dL-dZ share
u = 0.952 — four exact vertical twin pairs.  The left register rule carries
those six row squares so the pitch can be read straight off the margin.  Row
registration binds the WELLS only, so the stages between them are free: the
backward lattice and comb are squeezed to 0.80 about their own centres
(``BWD_MID``) and the wells to 0.74, which is what makes the lower band read
as the quieter echo it is without moving a single row.

DECLARED FLATNESS + DEPTH.  The plate is an instrument register, flat on
purpose (rubric dimension 7 allows declared flatness).  Depth comes from
``occlude_crossings`` — red over black over blue cuts a 0.9 mm gap at every
cross-pen crossing — and from the fade-in dotting that makes each bundle
condense out of its well instead of starting at a hard edge.

CROWDING FIXES vs THE REFERENCE
 1. 24 mm of blank paper between the registers; only the left register rule is
    allowed across it;
 2. Q and K no longer share a corridor: Q owns the upper 0.56 of the lattice's
    left edge, K the lower 0.56, with a four-row band of deliberate overlap.
    Neither bundle ever travels inside the other's lane, which is what turned
    the reference's black curtain back into lines;
 3. the funnel between ``similarity`` and ``softmax`` is a real reduction in
    LANE COUNT (34 lattice columns -> 20 query lines -> one distribution), so
    the destruction of information is drawn as arithmetic, not as a pile;
 4. Q's rings stop at a 0.80 mm throat instead of flooding into the node;
 5. Z is a ``focal_void`` clearing — strokes stop exactly on a 7 mm circle and
    three hero lines thread it;
 6. the red arc rides high over the black bundle in the right half, so the two
    pens own different halves instead of stacking into a lens;
 7. every label reserves a halo box that all geometry is clipped out of;
 8. per-pen ``enforce_line_spacing`` at 0.95 mm, so no bundle can mud.

Pens (``colors=3``): 0 black (K, structure, type), 1 blue (Q), 2 red (V).
Entry point: ``attention_passes``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.policies import (
    enforce_line_spacing,
    focal_void,
    occlude_crossings,
)
from promptplot.generative.generators import _glyph_advance, _poly, _stroke_text, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, BLUE, RED = 0, 1, 2
F_DRAW = 2200
F_FINE = 2400

FRAME_INSET = 2.0

# --------------------------------------------------------------------------
# columns  (u)
# --------------------------------------------------------------------------
U_REG = 0.013        # left register rule — the one element crossing the gutter
U_LABEL_R = 0.058    # right edge of every row label
U_WELL_L = 0.088     # hard left stop for every well field
U_NODE = 0.165       # the six well nodes, and nothing else
U_EXIT = 0.196       # where the bundles leave the wells
U_SIM = 0.428
U_SOFT = 0.618
U_WV = 0.832
U_Z = 0.952

LAT_HALF = 0.072     # 28.5 mm each side of U_SIM
COMB_MAX = 0.052     # longest softmax tick, each side

# --------------------------------------------------------------------------
# rows  (v, 0 = top).  DV is the rigid register offset.
# --------------------------------------------------------------------------
V_Q, V_K, V_V = 0.120, 0.246, 0.400
V_Z = 0.278
DV = 0.452

V_LAT = (0.096, 0.358)      # lattice vertical span, forward
V_COMB = (0.108, 0.368)     # comb vertical span, forward

V_RULE_TOP = 0.072
V_RULE_FWD_BOT = 0.462
V_RULE_BWD_TOP = 0.540
V_RULE_BWD_BOT = 0.905
V_STAGE_LABEL = 0.044
V_AXIS = 0.952

BWD_SCALE = 0.74      # gradient wells, relative to their forward twins
BWD_MID = 0.80        # gradient STAGES (lattice, comb) — the wells never move

N_KEYS = 34
N_QUERIES = 28
D_MODEL = 24


# ==========================================================================
# frame
# ==========================================================================
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

    def du(self, d: float) -> float:
        return d * self.w

    def dv(self, d: float) -> float:
        return d * self.h


# ==========================================================================
# primitives
# ==========================================================================
def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _seglen(poly: Poly) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:]))


def _dotted(polys: Sequence[Poly], step: float, r: float, pen: Optional[int],
            phase: float = 0.0) -> List[GCodeCommand]:
    """Place dots along polylines every ``step`` mm.

    The reference's fields are DOT fields, not dashes; a dot is drawn as a
    short horizontal stroke of length 2r, which is exactly what a 0.5 mm tip
    leaves on paper.
    """
    out: List[GCodeCommand] = []
    for poly in polys:
        if _seglen(poly) < step * 0.5:
            continue
        acc = phase % step
        for a, b in zip(poly, poly[1:]):
            seg = math.hypot(b[0] - a[0], b[1] - a[1])
            if seg < 1e-9:
                continue
            t = (step - acc) if acc > 0 else 0.0
            while t <= seg:
                fx = a[0] + (b[0] - a[0]) * t / seg
                fy = a[1] + (b[1] - a[1]) * t / seg
                out.append(GCodeCommand(command="G0", x=round(fx - r, 3), y=round(fy, 3)))
                out.append(GCodeCommand(command="M3", s=1000, color=pen))
                out.append(GCodeCommand(command="G1", x=round(fx + r, 3), y=round(fy, 3),
                                        f=1200, color=pen))
                out.append(GCodeCommand(command="M5"))
                t += step
            acc = (acc + seg) % step
    return out


def _mark(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """One plotted dot: a single stroke when it is tip-sized, a SERPENTINE of
    chords when it is not.

    Not a spiral.  The lattice holds ~950 dots and an Archimedean spiral costs
    ~50 commands each, which alone put the plate at 64 k commands and 21 m of
    travel; a chord serpentine is a dozen and looks identical at 0.7 mm.
    """
    if r <= 0.30:
        return [
            GCodeCommand(command="G0", x=round(x - r, 3), y=round(y, 3)),
            GCodeCommand(command="M3", s=1000, color=pen),
            GCodeCommand(command="G1", x=round(x + r, 3), y=round(y, 3), f=1200, color=pen),
            GCodeCommand(command="M5"),
        ]
    if r <= 1.05:
        rows = max(2, int(2 * r / 0.40))
        pts: Poly = []
        for k in range(rows + 1):
            yy = y - r + 2 * r * k / rows
            half = math.sqrt(max(0.0, r * r - (yy - y) ** 2))
            row = [(x - half, yy), (x + half, yy)]
            pts.extend(reversed(row) if k % 2 else row)
        return _poly(pts, color=pen, f=1500)
    turns = max(2, int(r / 0.42))
    n = turns * 24
    pts = [
        (x + r * k / n * math.cos(2 * math.pi * turns * k / n),
         y + r * k / n * math.sin(2 * math.pi * turns * k / n))
        for k in range(n + 1)
    ]
    return _poly(pts, color=pen, f=1600)


def _square(x: float, y: float, s: float, pen: Optional[int]) -> List[GCodeCommand]:
    """The filled node square — serpentine fill at the pen tip."""
    pts: Poly = []
    yy = y - s / 2.0
    flip = False
    while yy <= y + s / 2.0 + 1e-9:
        row = [(x - s / 2.0, yy), (x + s / 2.0, yy)]
        pts.extend(reversed(row) if flip else row)
        flip = not flip
        yy += 0.42
    return _poly(pts, color=pen, f=1500)


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 70) -> Poly:
    out: Poly = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        out.append((
            m ** 3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
            m ** 3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return out


def _flow(p0: Pt, p1: Pt, bow: float = 0.55, sag: float = 0.0, n: int = 70) -> Poly:
    """A sweep with horizontal tangents at both ends — the bundle idiom."""
    dx = p1[0] - p0[0]
    return _bez(p0, (p0[0] + bow * dx, p0[1] + sag), (p1[0] - bow * dx, p1[1] + sag), p1, n)


def _drop(p0: Pt, p1: Pt, rise: float, bow: float = 0.5, n: int = 70) -> Poly:
    """A sweep that leaves horizontally and ARRIVES VERTICALLY — used for the
    key bundle, which enters the lattice's top edge because keys are its
    columns.  ``rise`` is how far above the arrival point the tangent sits."""
    dx = p1[0] - p0[0]
    return _bez(p0, (p0[0] + bow * dx, p0[1]), (p1[0], p1[1] + rise), p1, n)


def _dash(poly: Poly, on: float, off: float, phase: float = 0.0) -> List[Poly]:
    """Split a polyline into dashes.  Explicit on/off state, never a modulo:
    the modulo form lands epsilon below the switch point and never terminates.
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


def _fade_in(poly: Poly, frac: float = 0.22, dot: float = 0.75, gap0: float = 4.6,
             gap1: float = 0.15, phase: float = 0.0) -> List[Poly]:
    """Dot the first ``frac`` of a sweep with a gap that CLOSES, so the bundle
    condenses out of the well's dot field instead of starting at a hard edge.
    The remainder is left solid.
    """
    total = _seglen(poly)
    if total < 6.0:
        return [poly]
    cut = total * frac
    out: List[Poly] = []
    s = 0.0
    head: Poly = []
    tail: Poly = []
    for a, b in zip(poly, poly[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if s + seg <= cut:
            head.append(a)
        elif s > cut:
            tail.append(a)
        else:
            f = (cut - s) / max(seg, 1e-9)
            mid = (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
            head.append(a)
            head.append(mid)
            tail.append(mid)
        s += seg
    tail.append(poly[-1])
    # graduated dotting of the head
    hl = _seglen(head)
    t = phase % 3.0
    while t < hl:
        q = t / max(hl, 1e-9)
        gap = gap0 + (gap1 - gap0) * q
        a = _at(head, t)
        b = _at(head, min(hl, t + dot))
        if a and b:
            out.append([a, b])
        t += dot + max(0.25, gap)
    if len(tail) >= 2:
        out.append(tail)
    return out


def _at(poly: Poly, s: float) -> Optional[Pt]:
    acc = 0.0
    for a, b in zip(poly, poly[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + seg >= s and seg > 1e-9:
            f = (s - acc) / seg
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)
        acc += seg
    return poly[-1] if poly else None


def _arrowhead(poly: Poly, t: float, size: float, pen: Optional[int]) -> List[GCodeCommand]:
    """A small SOLID triangle on ``poly`` at fractional arclength ``t``,
    pointing ALONG the path.

    Every backward path is built from dL/dZ on the right towards its well on
    the left, so this points LEFT — which is the whole job of these marks, and
    they are the only filled triangles on the sheet.  (It pointed the other way
    for four rounds because the tangent was flipped by a stray ``+ pi``: the
    plate then read as two forward passes.)"""
    total = _seglen(poly)
    if total < size * 4:
        return []
    want = total * t
    s = 0.0
    for a, b in zip(poly, poly[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if s + seg >= want and seg > 1e-9:
            f = (want - s) / seg
            px, py = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            ang = math.atan2(b[1] - a[1], b[0] - a[0])
            ca, sa = math.cos(ang), math.sin(ang)
            hw = size * 0.42
            tip = (px + size * ca, py + size * sa)
            lp = (px - hw * sa, py + hw * ca)
            rp = (px + hw * sa, py - hw * ca)
            out: List[GCodeCommand] = []
            for k in range(5):
                q = k / 4.0
                out += _poly([(lp[0] + (tip[0] - lp[0]) * q, lp[1] + (tip[1] - lp[1]) * q),
                              (rp[0] + (tip[0] - rp[0]) * q, rp[1] + (tip[1] - rp[1]) * q)],
                             color=pen, f=1500)
            return out
        s += seg
    return []


def _chevron(x: float, y: float, d: int, size: float, pen: Optional[int]) -> List[GCodeCommand]:
    """An OPEN axis chevron — deliberately not the filled flow arrowhead."""
    return _poly([(x - d * size, y + size * 0.55), (x, y), (x - d * size, y - size * 0.55)],
                 color=pen, f=F_FINE)


# ==========================================================================
# type
# ==========================================================================
def _tracked(text: str, x: float, baseline: float, cap: float, pen: Optional[int],
             target_w: Optional[float] = None, f: int = F_FINE) -> List[GCodeCommand]:
    sc = cap / 6.0
    nat = _text_width(text, cap, proportional=True)
    extra = (target_w - nat) / (len(text) - 1) if (target_w and len(text) > 1) else 0.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * sc + extra
    return out


def _tw(text: str, cap: float, target_w: Optional[float] = None) -> float:
    return target_w if target_w is not None else _text_width(text, cap, proportional=True)


def _text_at(text: str, baseline: float, cap: float, pen: Optional[int],
             left: Optional[float] = None, centre: Optional[float] = None,
             right: Optional[float] = None, target_w: Optional[float] = None
             ) -> Tuple[List[GCodeCommand], Bounds]:
    w = _tw(text, cap, target_w)
    if left is not None:
        x = left
    elif centre is not None:
        x = centre - w / 2.0
    else:
        x = (right or 0.0) - w
    return (_tracked(text, x, baseline, cap, pen, target_w),
            (x, baseline - cap * 0.34, x + w, baseline + cap * 1.22))


def _fraction(num: str, den: str, baseline: float, cap: float, pen: Optional[int],
              right: float) -> Tuple[List[GCodeCommand], Bounds]:
    """dL/dQ drawn as a real fraction — numerator, rule, denominator."""
    wn = _text_width(num, cap, proportional=True)
    wd = _text_width(den, cap, proportional=True)
    w = max(wn, wd)
    x = right - w
    out: List[GCodeCommand] = []
    out += _tracked(num, x + (w - wn) / 2.0, baseline + cap * 0.60, cap, pen)
    out += _poly([(x - 0.5, baseline + cap * 0.28), (x + w + 0.5, baseline + cap * 0.28)],
                 color=pen, f=F_FINE)
    out += _tracked(den, x + (w - wd) / 2.0, baseline - cap * 1.18, cap, pen)
    return out, (x - 1.3, baseline - cap * 1.55, x + w + 1.3, baseline + cap * 1.85)


# ==========================================================================
# the numbers: Q Kᵀ and its softmax
# ==========================================================================
def _positional(n: int, d: int, stride: float, phase: float = 0.0) -> np.ndarray:
    P = np.zeros((n, d))
    for i in range(n):
        p = phase + i * stride
        for j in range(d):
            f = 1.0 / (10000.0 ** ((j // 2 * 2) / d))
            P[i, j] = math.sin(p * f) if j % 2 == 0 else math.cos(p * f)
    return P


def _scores(rng: SeededRNG) -> Tuple[np.ndarray, np.ndarray, int]:
    """Real ``S = Q Kᵀ / sqrt(d)`` plus the softmax of one focal query row."""
    d = D_MODEL
    Wq = np.array([[rng.gauss(0, 1) for _ in range(d)] for _ in range(d)]) / math.sqrt(d)
    Wk = np.array([[rng.gauss(0, 1) for _ in range(d)] for _ in range(d)]) / math.sqrt(d)
    Q = _positional(N_QUERIES, d, 1.9, 0.4) @ Wq
    K = _positional(N_KEYS, d, 1.0) @ Wk
    S = (Q @ K.T) / math.sqrt(d)
    # Which query we follow is a curatorial choice, and it is made explicit:
    # among the sharpest rows, take the one whose peak key sits nearest the
    # middle of the key axis, so the comb's waist lands on the sheet's spine
    # instead of at one end of the column.
    sharp = S.max(axis=1) - S.mean(axis=1)
    mid = (N_KEYS - 1) / 2.0
    order = np.argsort(sharp)[::-1]
    cand = order[: max(4, N_QUERIES // 2)]
    q_star = int(min(cand, key=lambda j: abs(int(np.argmax(S[j])) - mid)
                     - 3.0 * float(sharp[j]) / float(sharp.max())))
    # Temperature 0.20 rather than 1.0: at the raw scale this head's row is
    # almost uniform (top weight 0.03 against a 1/34 floor of 0.029) and the
    # comb would be a picket fence.  Colder than this (0.14 was tried) collapses
    # it the other way — two long bars on a bare spine, which loses the DENSE
    # comb the reference is built around.  0.20 keeps ~26 ticks legible with the
    # top weight at 6x uniform, and it holds across seeds.
    row = S[q_star] / 0.20
    row = row - row.max()
    w = np.exp(row)
    w = w / w.sum()
    return S, w, q_star


def _inverse_cdf(w: np.ndarray, n: int) -> np.ndarray:
    """n positions in [0, 1] drawn by inverse-CDF of ``w`` — line DENSITY
    becomes probability mass, which is what 'weighted values' means."""
    cdf = np.concatenate([[0.0], np.cumsum(w)])
    cdf = cdf / cdf[-1]
    targets = (np.arange(n) + 0.5) / n
    idx = np.clip(np.searchsorted(cdf, targets, side="right") - 1, 0, len(w) - 1)
    frac = (targets - cdf[idx]) / np.maximum(cdf[idx + 1] - cdf[idx], 1e-12)
    return (idx + frac) / len(w)


# ==========================================================================
# WELL 1 — Q: DIRECTION (nested parabolic wavefronts, focus at the node)
# ==========================================================================
def _well_q(fr: Frame, cy: float, scale: float, pen: Optional[int]
            ) -> Tuple[List[GCodeCommand], float]:
    """r = p/(1 − cos t) about the node: confocal parabolae, vertices marching
    LEFT from the node, arms opening RIGHT along the row.  Every ray leaving
    the focus exits parallel — that is exactly what a query direction is, and
    the arms hand straight over to the bundle.  Open curves, never closed;
    vertex pitch = pitch/2 = 0.80 mm, the tightest gap on the well."""
    nx, ny = fr.u(U_NODE), cy
    x_min = fr.u(U_WELL_L)
    x_max = fr.u(U_EXIT) - 1.0
    sy = 0.60 * scale
    pitch = 1.60 * scale
    p0 = 1.30 * scale
    h_max = 10.0 * scale
    out: List[GCodeCommand] = []
    polys: List[Poly] = []
    for k in range(13):
        p = p0 + k * pitch
        pts: Poly = []
        for t in np.linspace(0.18, 2 * math.pi - 0.18, 420):
            c = math.cos(t)
            if 1 - c < 1e-3:
                continue
            r = p / (1 - c)
            x = nx + r * c
            y = ny + r * math.sin(t) * sy
            if x < x_min or x > x_max or abs(y - ny) > h_max:
                if len(pts) >= 2:
                    polys.append(pts)
                pts = []
                continue
            pts.append((x, y))
        if len(pts) >= 2:
            polys.append(pts)
    out += _dotted(polys, 1.55 * scale, 0.30 * scale, pen)

    # the axis of the direction: a short dotted run through the focus, the one
    # ray that is the query itself
    out += _dotted([[(nx - 11.0 * scale, ny), (x_max, ny)]], 1.5 * scale, 0.28 * scale, pen)
    out += _square(nx, ny, 1.85 * scale, pen)
    return out, h_max


# ==========================================================================
# WELL 2 — K: FIELD (exact union-of-cones nest, four cusps)
# ==========================================================================
def _union_circles(centres: Sequence[Pt], radii: Sequence[float], n: int = 260) -> List[Poly]:
    """Boundary of a union of discs.  F = max_i (a_i − r_i) is conical
    (|grad F| = 1), so equal level steps give EXACTLY equal ring pitch
    everywhere — the rubric's contour law satisfied by construction."""
    runs: List[Poly] = []
    for i, (c, r) in enumerate(zip(centres, radii)):
        if r <= 0.15:
            continue
        cur: Poly = []
        for k in range(n + 1):
            a = 2 * math.pi * k / n
            p = (c[0] + r * math.cos(a), c[1] + r * math.sin(a))
            inside = any(
                j != i and math.hypot(p[0] - centres[j][0], p[1] - centres[j][1]) < radii[j] - 1e-6
                for j in range(len(centres))
            )
            if inside:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
            else:
                cur.append(p)
        if len(cur) >= 2:
            runs.append(cur)
    return runs


K_CUSPS = [((0.0, 0.0), 10.4), ((-11.5, 6.8), 9.4), ((-17.5, -2.8), 8.6), ((-6.5, -9.2), 7.6)]


def _well_k(fr: Frame, cy: float, scale: float, pen: Optional[int]
            ) -> Tuple[List[GCodeCommand], float]:
    nx, ny = fr.u(U_NODE), cy
    ax, ay = 1.12, 1.06                       # anisotropy applied AFTER the union
    pitch = 1.25
    out: List[GCodeCommand] = []
    a_max = max(a for _, a in K_CUSPS)
    levels = [a_max - pitch * k for k in range(1, int(a_max / pitch))]
    for li, L in enumerate(levels):
        radii = [max(0.0, a - L) for _, a in K_CUSPS]
        runs = _union_circles([c for c, _ in K_CUSPS], radii)
        mapped = [[(nx + p[0] * ax * scale, ny + p[1] * ay * scale) for p in run] for run in runs]
        out += _dotted(mapped, (1.45 + 0.035 * li) * scale,
                       (0.30 - 0.004 * li) * scale, pen, phase=0.37 * li)
    out += _square(nx, ny, 1.95 * scale, pen)
    for c, _a in K_CUSPS[1:]:
        out += _mark(nx + c[0] * ax * scale, ny + c[1] * ay * scale, 0.40 * scale, pen)
    return out, 17.0 * scale


# ==========================================================================
# WELL 3 — V: STRATA (lobed silhouette, laminae at fixed pitch, duty = |v_i|)
# ==========================================================================
def _lobed(cx: float, cy: float, rx: float, ry: float,
           harm: Sequence[Tuple[int, float, float]], n: int = 320) -> Poly:
    pts: Poly = []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        r = 1.0 + sum(amp * math.cos(m * a + ph) for m, amp, ph in harm)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def _row_spans(poly: Poly, y: float) -> List[Tuple[float, float]]:
    xs: List[float] = []
    for a, b in zip(poly, poly[1:]):
        if (a[1] - y) * (b[1] - y) < 0:
            t = (y - a[1]) / (b[1] - a[1])
            xs.append(a[0] + (b[0] - a[0]) * t)
    xs.sort()
    return [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]


V_HARM = [(2, 0.185, 0.55), (3, 0.125, 2.10), (5, 0.070, 4.40), (1, 0.150, 3.05)]


def _well_v(fr: Frame, cy: float, scale: float, pen: Optional[int],
            norms: Sequence[float]) -> Tuple[List[GCodeCommand], float]:
    nx, ny = fr.u(U_NODE), cy
    rx, ry = 17.5 * scale, 10.5 * scale
    cx = nx - 12.5 * scale
    outline = _lobed(cx, ny, rx, ry, V_HARM)
    out: List[GCodeCommand] = []
    out += _dotted([outline], 1.55 * scale, 0.29 * scale, pen)

    pitch = 1.45 * scale                     # FIXED — tone drives duty, not spacing
    y = ny - ry * 1.34
    row = 0
    while y <= ny + ry * 1.34:
        duty = norms[row % len(norms)]
        for x0, x1 in _row_spans(outline, y):
            if x1 - x0 < 1.0:
                continue
            on = max(0.6, 3.0 * duty) * scale
            off = max(0.85, 2.6 - 1.8 * duty) * scale
            out += _emit(_dash([(x0 + 0.3, y), (x1 - 0.3, y)], on, off, phase=1.9 * row),
                         pen, f=1900)
        y += pitch
        row += 1
    out += _square(nx, ny, 1.85 * scale, pen)
    return out, ry * 1.34


# ==========================================================================
# similarity lattice + softmax comb
# ==========================================================================
def _lattice(fr: Frame, S: np.ndarray, cv: Tuple[float, float], sub: int,
             pen: Optional[int], amp: float = 1.0) -> List[GCodeCommand]:
    x_l, x_r = fr.u(U_SIM - LAT_HALF), fr.u(U_SIM + LAT_HALF)
    y_t, y_b = fr.v(cv[0]), fr.v(cv[1])
    smax = float(np.abs(S).max())
    out: List[GCodeCommand] = []
    for j in range(0, N_QUERIES, sub):
        y = y_t + (y_b - y_t) * (j + 0.5) / N_QUERIES
        for i in range(0, N_KEYS, sub):
            x = x_l + (x_r - x_l) * (i + 0.5) / N_KEYS
            r = 0.66 * amp * (abs(S[j, i]) / smax) ** 0.55
            if r > 0.10:
                out += _mark(x, y, r, pen)
    # AXIS SCALES.  The bundles no longer state which way the matrix runs, so
    # the lattice does: key ticks along the top edge, query ticks down the
    # left.  Rows are queries, columns are keys — said in furniture, not in a
    # caption.
    for i in range(0, N_KEYS, 4):
        x = x_l + (x_r - x_l) * (i + 0.5) / N_KEYS
        out += _poly([(x, y_t + 1.4 * amp), (x, y_t + (3.8 if i % 8 == 0 else 2.6) * amp)],
                     color=pen, f=F_FINE)
    for j in range(0, N_QUERIES, 4):
        y = y_t + (y_b - y_t) * (j + 0.5) / N_QUERIES
        out += _poly([(x_l - 1.4 * amp, y), (x_l - (3.8 if j % 8 == 0 else 2.6) * amp, y)],
                     color=pen, f=F_FINE)
    return out


def _comb(fr: Frame, w: np.ndarray, cv: Tuple[float, float], pen: Optional[int],
          amp: float = 1.0) -> Tuple[List[GCodeCommand], float]:
    """The loudest mark on the sheet: tick length IS the normalised weight."""
    xa = fr.u(U_SOFT)
    y_t, y_b = fr.v(cv[0]), fr.v(cv[1])
    wmax = float(w.max())
    L = fr.du(COMB_MAX) * amp
    out: List[GCodeCommand] = []
    peak_y = y_t
    pitch = abs(y_b - y_t) / N_KEYS
    for i in range(N_KEYS):
        y = y_t + (y_b - y_t) * (i + 0.5) / N_KEYS
        h = L * (w[i] / wmax)
        if w[i] >= wmax * 0.999:
            peak_y = y
        if h > 0.30:
            # INK WEIGHT IS PROBABILITY: a tick is redrawn once per 6% of mass,
            # so the few loud keys are physically blacker on the paper, not
            # merely longer.  Passes are offset by 0.34 mm, under the pitch.
            passes = 1 + int(w[i] / 0.06)
            for q in range(passes):
                off = (q - (passes - 1) / 2.0) * min(0.34, pitch * 0.30)
                out += _poly([(xa - h, y + off), (xa + h, y + off)], color=pen, f=1800)
        rr = 1.05 * amp * (w[i] / wmax) ** 0.50
        out += _mark(xa, y, max(0.22, rr), pen)
    # the axis continues BEYOND the comb: graduated dots, the distribution's
    # tail running off the ends of the support
    hi, lo = max(y_t, y_b), min(y_t, y_b)
    span = hi - lo
    for t, rr in ((0.035, 1.5), (0.062, 0.95), (0.090, 0.55)):
        out += _mark(xa, hi + span * t, rr * amp, pen)
        out += _mark(xa, lo - span * t, rr * amp, pen)
    return out, peak_y


# ==========================================================================
# bundle helpers
# ==========================================================================
def _spread(x: float, y0: float, y1: float, n: int) -> List[Pt]:
    return [(x, y0 + (y1 - y0) * (k + 0.5) / n) for k in range(n)]


def _guard(cmds: List[GCodeCommand], pen: Optional[int], min_dist: float = 0.95
           ) -> List[GCodeCommand]:
    """``enforce_line_spacing`` + re-emit, so every stroke keeps its leading G0
    (the policy can drop it, which shows up as a stray stroke from the origin).
    Called PER PEN so pens never thin each other."""
    thinned = enforce_line_spacing(cmds, min_dist=min_dist, resample=0.45)
    runs: List[Poly] = []
    cur: Poly = []
    for c in thinned:
        if c.command == "G0" and c.x is not None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [(c.x, c.y)]
        elif c.command == "G1" and c.x is not None:
            cur.append((c.x, c.y))
        elif c.command == "M5":
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return _emit(runs, pen)


def _clip_boxes(polys: Sequence[Poly], boxes: Sequence[Bounds]) -> List[Poly]:
    """Cut every polyline out of the reserved label halos."""
    if not boxes:
        return list(polys)

    def inside(p: Pt) -> bool:
        return any(b[0] <= p[0] <= b[2] and b[1] <= p[1] <= b[3] for b in boxes)

    out: List[Poly] = []
    for poly in polys:
        cur: Poly = []
        for p in poly:
            if inside(p):
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
            else:
                cur.append(p)
        if len(cur) >= 2:
            out.append(cur)
    return out


def _clip_cmds(cmds: Sequence[GCodeCommand], boxes: Sequence[Bounds],
               pen: Optional[int]) -> List[GCodeCommand]:
    """Same halo knockout, but for already-emitted commands (the wells)."""
    if not boxes:
        return list(cmds)

    def inside(x: float, y: float) -> bool:
        return any(b[0] <= x <= b[2] and b[1] <= y <= b[3] for b in boxes)

    out: List[GCodeCommand] = []
    buf: List[GCodeCommand] = []
    drop = False
    for c in cmds:
        if c.command == "G0":
            if buf and not drop:
                out.extend(buf)
            buf = [c]
            drop = c.x is not None and inside(c.x, c.y)
        else:
            if c.x is not None and inside(c.x, c.y):
                drop = True
            buf.append(c)
    if buf and not drop:
        out.extend(buf)
    return out


# ==========================================================================
# the plate
# ==========================================================================
def attention_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    fr = Frame(bounds)
    U, V = fr.u, fr.v

    def P(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    K_PEN, Q_PEN, V_PEN = P(BLACK), P(BLUE), P(RED)

    S, w, q_star = _scores(rng)
    norms = [min(1.0, 0.26 + 0.74 * abs(rng.gauss(0, 0.66))) for _ in range(17)]

    type_cmds: List[GCodeCommand] = []
    halos: List[Bounds] = []

    def label(c: List[GCodeCommand], box: Bounds, px: float = 2.0, py: float = 1.4) -> None:
        type_cmds.extend(c)
        halos.append((box[0] - px, box[1] - py, box[2] + px, box[3] + py))

    # ---------------- 1. row labels --------------------------------------
    for text, vv, pen in (("Q", V_Q, Q_PEN), ("K", V_K, K_PEN), ("V", V_V, V_PEN)):
        label(*_text_at(text, V(vv) - 3.4, 9.4, pen, right=U(U_LABEL_R)), px=2.6, py=1.8)
    for num, den, vv, pen in (("∂L", "∂Q", V_Q + DV, Q_PEN), ("∂L", "∂K", V_K + DV, K_PEN),
                              ("∂L", "∂V", V_V + DV, V_PEN)):
        label(*_fraction(num, den, V(vv), 3.5, pen, U(U_LABEL_R)), px=1.8, py=1.0)
    label(*_text_at("Z", V(V_Z) - 3.4, 9.4, K_PEN, left=U(U_Z) + 5.0), px=2.4, py=1.8)
    label(*_fraction("∂L", "∂Z", V(V_Z + DV), 3.5, K_PEN, U(U_Z) + 13.5), px=1.8, py=1.0)

    # ---------------- 2. stage labels ------------------------------------
    for text, uu, tw in (("similarity", U_SIM, 21.0), ("softmax", U_SOFT, 16.5),
                         ("weighted values", U_WV, 31.0)):
        label(*_text_at(text, V(V_STAGE_LABEL), 2.9, K_PEN, centre=U(uu), target_w=tw),
              px=2.4, py=1.8)
    label(*_text_at("backpropagate", V(V_RULE_BWD_TOP + 0.028), 2.6, K_PEN,
                    right=U(0.990), target_w=25.5), px=1.8, py=1.2)
    label(*_text_at("gradients", V(V_RULE_BWD_TOP + 0.052), 2.6, K_PEN,
                    right=U(0.990), target_w=18.0), px=1.8, py=1.2)

    # ---------------- 3. the six wells -----------------------------------
    q_well, hq = _well_q(fr, V(V_Q), 1.0, Q_PEN)
    k_well, hk = _well_k(fr, V(V_K), 1.0, K_PEN)
    v_well, hv = _well_v(fr, V(V_V), 1.0, V_PEN, norms)
    gq_well, ghq = _well_q(fr, V(V_Q + DV), BWD_SCALE, Q_PEN)
    gk_well, ghk = _well_k(fr, V(V_K + DV), BWD_SCALE, K_PEN)
    gv_well, ghv = _well_v(fr, V(V_V + DV), BWD_SCALE, V_PEN, norms)

    # ---------------- 4. lattice + comb ----------------------------------
    # Row registration binds the WELLS, not the stages between them, so the
    # backward register's middle is squeezed to 0.80 about its own centre.
    # That is what makes the gradient band read as the quieter, smaller echo
    # it is, while Q/dQ, K/dK, V/dV and Z/dZ stay exactly aligned.
    def shrink(span: Tuple[float, float], k: float = BWD_MID) -> Tuple[float, float]:
        c = (span[0] + span[1]) / 2.0 + DV
        h = (span[1] - span[0]) / 2.0 * k
        return (c - h, c + h)

    V_LAT_B, V_COMB_B = shrink(V_LAT), shrink(V_COMB)

    lat_f = _lattice(fr, S, V_LAT, 1, K_PEN, amp=1.0)
    lat_b = _lattice(fr, S, V_LAT_B, 2, K_PEN, amp=0.95)
    comb_f, peak_f = _comb(fr, w, V_COMB, K_PEN, amp=1.0)
    comb_b, peak_b = _comb(fr, w, V_COMB_B, K_PEN, amp=0.58)

    x_lat_l, x_lat_r = U(U_SIM - LAT_HALF), U(U_SIM + LAT_HALF)
    y_lat_t, y_lat_b = V(V_LAT[0]), V(V_LAT[1])
    y_lb_t, y_lb_b = V(V_LAT_B[0]), V(V_LAT_B[1])
    x_soft, x_wv, x_z = U(U_SOFT), U(U_WV), U(U_Z)
    y_c_t, y_c_b = V(V_COMB[0]), V(V_COMB[1])
    y_cb_t, y_cb_b = V(V_COMB_B[0]), V(V_COMB_B[1])
    L_comb = fr.du(COMB_MAX)

    # which query row the comb is the softmax OF
    y_star = y_lat_t + (y_lat_b - y_lat_t) * (q_star + 0.5) / N_QUERIES
    bracket = _emit([[(x_lat_r + 1.8, y_star + 2.6), (x_lat_r + 3.8, y_star + 2.6),
                      (x_lat_r + 3.8, y_star - 2.6), (x_lat_r + 1.8, y_star - 2.6)]],
                    K_PEN, f=F_FINE)

    # ---------------- 5. FORWARD bundles ---------------------------------
    xe = U(U_EXIT)

    # Q and K each own a BAND of the lattice's left edge — Q the upper 0.56,
    # K the lower 0.56, with a four-row band of deliberate overlap where they
    # interleave.  Routing them into one edge but two bands is what killed the
    # curtain: neither bundle ever travels inside the other's corridor.
    n_q = 15
    q_flow = [_flow(a, b, bow=0.40) for a, b in
              zip(_spread(xe, V(V_Q) - hq * 0.88, V(V_Q) + hq * 0.88, n_q),
                  _spread(x_lat_l, y_lat_t, y_lat_t + (y_lat_b - y_lat_t) * 0.56, n_q))]

    n_k = 17
    k_flow = [_flow(a, b, bow=0.38) for a, b in
              zip(_spread(xe, V(V_K) - hk * 0.88, V(V_K) + hk * 0.88, n_k),
                  _spread(x_lat_l, y_lat_t + (y_lat_b - y_lat_t) * 0.44, y_lat_b, n_k))]

    # the FUNNEL: 20 query lines out of the lattice converging on one waist.
    n_f = 20
    waist = (x_soft - L_comb - 5.0, peak_f)
    funnel = [_flow(a, (waist[0], waist[1] + (k - (n_f - 1) / 2.0) * 0.30), bow=0.70)
              for k, a in enumerate(_spread(x_lat_r, y_lat_t, y_lat_b, n_f))]

    # out of the comb: positions at `weighted values` set by the INVERSE CDF
    # of w, so the fan's density IS the distribution.  The black fan owns the
    # band BELOW the Z row; red owns everything above it.  Two pens, two
    # halves, no lens.
    n_o = 16
    o_src = [(x_soft + L_comb + 4.0, peak_f + (k - (n_o - 1) / 2.0) * 0.32) for k in range(n_o)]
    o_lo, o_hi = V(V_Z + 0.012), V(V_COMB[1])
    o_wv = [(x_wv, o_lo + (o_hi - o_lo) * float(p)) for p in _inverse_cdf(w, n_o)]
    out_o = [_flow(a, b, bow=0.74) for a, b in zip(o_src, o_wv)]
    to_z = [_flow(b, (x_z, V(V_Z)), bow=0.34) for b in o_wv]

    # V (red) sweeps UNDER the lattice — V takes no part in QKᵀ — joins at the
    # softmax column, then rides HIGH over the black bundle into Z.
    n_v = 13
    v_src = _spread(xe, V(V_V) - hv * 0.86, V(V_V) + hv * 0.86, n_v)
    v_join = [(x_soft - L_comb * 0.10, y_c_b - 2.0 - k * 0.95) for k in range(n_v)]
    v_flow = [_bez(a, (a[0] + 0.62 * (b[0] - a[0]), a[1] - 3.0 - 0.6 * i),
                   (b[0] - 0.40 * (b[0] - a[0]), b[1] - 8.0), b)
              for i, (a, b) in enumerate(zip(v_src, v_join))]
    v_top, v_bot = V(V_COMB[0] - 0.062), V(V_Z - 0.016)
    v_wv = [(x_wv, v_bot + (v_top - v_bot) * float(p)) for p in _inverse_cdf(w, n_v)]
    v_up = [_bez(a, (a[0] + 0.5 * (b[0] - a[0]), a[1]),
                 (b[0] - 0.48 * (b[0] - a[0]), b[1] + 9.0), b)
            for a, b in zip(v_join, v_wv)]
    v_to_z = [_flow(b, (x_z, V(V_Z)), bow=0.30) for b in v_wv]

    # ---------------- 6. BACKWARD bundles --------------------------------
    xz_b, yz_b = x_z, V(V_Z + DV)
    n_b = 13
    b_wv = [(x_wv, y_cb_t + (y_cb_b - y_cb_t) * float(p)) for p in _inverse_cdf(w, n_b)]
    b_from_z = [_flow((xz_b, yz_b), b, bow=0.55) for b in b_wv]
    b_in = [(x_soft + L_comb * 0.62 + 4.0, peak_b + (k - (n_b - 1) / 2.0) * 0.30)
            for k in range(n_b)]
    b_comb_in = [_flow(a, b, bow=0.62) for a, b in zip(b_wv, b_in)]

    n_bk = 14
    b_out = [(x_soft - L_comb * 0.62 - 4.0, peak_b + (k - (n_bk - 1) / 2.0) * 0.30)
             for k in range(n_bk)]
    b_lat_r = _spread(x_lat_r, y_lb_t, y_lb_b, n_bk)
    b_spread = [_flow(a, b, bow=0.66) for a, b in zip(b_out, b_lat_r)]
    b_to_k = [_flow(a, b, bow=0.38) for a, b in
              zip(_spread(x_lat_l, y_lb_t + (y_lb_b - y_lb_t) * 0.44, y_lb_b, n_bk),
                  _spread(xe, V(V_K + DV) - ghk * 0.88, V(V_K + DV) + ghk * 0.88, n_bk))]

    n_bq = 12
    b_to_q = [_flow(a, b, bow=0.40) for a, b in
              zip(_spread(x_lat_l, y_lb_t, y_lb_t + (y_lb_b - y_lb_t) * 0.56, n_bq),
                  _spread(xe, V(V_Q + DV) - ghq * 0.88, V(V_Q + DV) + ghq * 0.88, n_bq))]

    # dL/dV: the SAME weights re-applied, straight back through the comb
    n_bv = 13
    bv_wv = [(x_wv, y_cb_t - fr.dv(0.040) * float(p) + fr.dv(0.048))
             for p in _inverse_cdf(w, n_bv)]
    bv_from_z = [_flow((xz_b, yz_b), b, bow=0.58) for b in bv_wv]
    bv_join = [(x_soft - L_comb * 0.15, y_cb_b - 2.4 - k * 0.48) for k in range(n_bv)]
    bv_mid = [_bez(a, (a[0] - 0.5 * (a[0] - b[0]), a[1]),
                   (b[0] + 0.45 * (a[0] - b[0]), b[1] + 5.0), b)
              for a, b in zip(bv_wv, bv_join)]
    bv_back = [_bez(a, (a[0] - 0.55 * (a[0] - b[0]), a[1] - 3.0),
                    (b[0] + 0.42 * (a[0] - b[0]), b[1] - 5.0), b)
               for a, b in zip(bv_join,
                               _spread(xe, V(V_V + DV) - ghv * 0.82,
                                       V(V_V + DV) + ghv * 0.82, n_bv))]

    # ---------------- 7. emit the bundles --------------------------------
    def bundle(polys: Sequence[Poly], pen: Optional[int], fade: float = 0.0,
               arrows: Sequence[float] = (), size: float = 2.1) -> List[GCodeCommand]:
        clipped = _clip_boxes(polys, halos)
        cmds: List[GCodeCommand] = []
        if fade > 0:
            for i, p in enumerate(clipped):
                cmds += _emit(_fade_in(p, frac=fade, phase=(i * 1.31) % 3.0), pen)
        else:
            cmds += _emit(clipped, pen)
        cmds = _guard(cmds, pen, 0.95)
        for i, p in enumerate(clipped):
            for t in arrows:
                cmds += _arrowhead(p, (t + 0.05 * (i % 3)) % 0.92, size, pen)
        return cmds

    fwd: List[GCodeCommand] = []
    fwd += bundle(q_flow, Q_PEN, fade=0.20)
    fwd += bundle(k_flow, K_PEN, fade=0.20)
    fwd += bundle(funnel, K_PEN)
    fwd += bundle(out_o, K_PEN)
    fwd += bundle(to_z, K_PEN)
    fwd += bundle(v_flow, V_PEN, fade=0.20)
    fwd += bundle(v_up, V_PEN)
    fwd += bundle(v_to_z, V_PEN)

    bwd: List[GCodeCommand] = []
    bwd += bundle(b_from_z, K_PEN, arrows=(0.40, 0.76))
    bwd += bundle(b_comb_in, K_PEN, arrows=(0.55,))
    bwd += bundle(b_spread, K_PEN, arrows=(0.52,))
    bwd += bundle(b_to_k, K_PEN, arrows=(0.52,))
    bwd += bundle(b_to_q, Q_PEN, arrows=(0.54,))
    bwd += bundle(bv_from_z, V_PEN, arrows=(0.44,))
    bwd += bundle(bv_mid, V_PEN, arrows=(0.52,))
    bwd += bundle(bv_back, V_PEN, arrows=(0.32, 0.70))

    # the Z clearing: blank paper where 34 lines land, three hero lines through
    fwd = focal_void(fwd, r=7.0, cx=x_z, cy=V(V_Z), keep=3, min_len=1.4)
    bwd = focal_void(bwd, r=6.0, cx=xz_b, cy=yz_b, keep=3, min_len=1.4)

    # depth: red over black over blue, 0.9 mm cut at every cross-pen crossing
    flows = occlude_crossings(fwd + bwd, gap=0.9, min_len=0.8,
                              priority=[V_PEN, K_PEN, Q_PEN])

    # ---------------- 8. compose -----------------------------------------
    out: List[GCodeCommand] = []
    out += _clip_cmds(q_well + gq_well, halos, Q_PEN)
    out += _clip_cmds(k_well + gk_well, halos, K_PEN)
    out += _clip_cmds(v_well + gv_well, halos, V_PEN)
    out += _clip_cmds(lat_f + lat_b + comb_f + comb_b, halos, K_PEN)
    out += bracket

    # BEADS ON THE `weighted values` RULE.  The third stage was the only one
    # with nothing on its rule, which left it reading as a bare guide line.
    # Each bead sits exactly where a fan line crosses, and its radius is the
    # magnitude that line is carrying: |v_i| for the red content lines, the
    # attention mass per lane (1/n of the distribution) for the black ones.
    beads: List[GCodeCommand] = []
    for i, (bx, by) in enumerate(v_wv):
        beads += _mark(bx, by, 0.30 + 0.55 * norms[i % len(norms)], V_PEN)
    for i, (bx, by) in enumerate(o_wv):
        beads += _mark(bx, by, 0.26 + 0.34 * ((i % 4) / 3.0), K_PEN)
    for i, (bx, by) in enumerate(bv_wv):
        beads += _mark(bx, by, (0.30 + 0.55 * norms[i % len(norms)]) * BWD_MID, V_PEN)
    for i, (bx, by) in enumerate(b_wv):
        beads += _mark(bx, by, (0.26 + 0.34 * ((i % 4) / 3.0)) * BWD_MID, K_PEN)
    out += beads
    out += flows
    out += _square(x_z, V(V_Z), 3.2, K_PEN)
    out += _square(xz_b, yz_b, 2.7, K_PEN)
    out += _furniture(rng, fr, K_PEN)
    out += type_cmds
    return out


# ==========================================================================
# furniture
# ==========================================================================
def _furniture(rng: SeededRNG, fr: Frame, pen: Optional[int]) -> List[GCodeCommand]:
    U, V = fr.u, fr.v
    out: List[GCodeCommand] = []

    # the three stage rules — dotted, BROKEN at the gutter so the two registers
    # read as two registers
    for uu, bwd_top in ((U_SIM, V_RULE_BWD_TOP), (U_SOFT, V_RULE_BWD_TOP),
                        (U_WV, V_RULE_BWD_TOP + 0.072)):
        out += _emit(_dash([(U(uu), V(V_RULE_TOP)), (U(uu), V(V_RULE_FWD_BOT))], 2.4, 3.1),
                     pen, f=F_FINE)
        out += _emit(_dash([(U(uu), V(bwd_top)), (U(uu), V(V_RULE_BWD_BOT))], 2.4, 3.1),
                     pen, f=F_FINE)

    # the LEFT REGISTER RULE — the one element allowed across the gutter.  Its
    # six squares make the row registration readable: three above, three below,
    # at identical pitch and identical offset.
    out += _emit(_dash([(U(U_REG), V(V_RULE_TOP)), (U(U_REG), V(V_RULE_BWD_BOT))], 1.9, 3.4),
                 pen, f=F_FINE)
    for vv in (V_Q, V_K, V_V):
        for row in (vv, vv + DV):
            out += _square(U(U_REG), V(row), 1.5, pen)
            out += _poly([(U(U_REG) + 1.7, V(row)), (U(U_REG) + 5.0, V(row))],
                         color=pen, f=F_FINE)

    # graduated dots running off the ends of the `similarity` and `weighted
    # values` rules, matching the comb's tail: every stage axis carries marks,
    # none is a bare guide line
    for uu, v_hi, v_lo in ((U_SIM, V_LAT[0], V_LAT[1]),
                           (U_WV, V_COMB[0] - 0.040, V_Z + 0.034)):
        for reg, amp, band in ((0.0, 1.0, (V_RULE_TOP, V_RULE_FWD_BOT)),
                               (DV, BWD_MID, (V_RULE_BWD_TOP, V_RULE_BWD_BOT))):
            for dv_, rr in ((0.018, 1.25), (0.036, 0.78), (0.056, 0.46)):
                a, b = v_hi - dv_ + reg, v_lo + dv_ + reg
                if band[0] + 0.006 <= a <= band[1] - 0.006:
                    out += _mark(U(uu), V(a), rr * amp, pen)
                if band[0] + 0.006 <= b <= band[1] - 0.006:
                    out += _mark(U(uu), V(b), rr * amp, pen)

    # short tick rules beside the registers (the reference's margin marks)
    for uu, v0, v1 in ((0.072, V_K - 0.062, V_K - 0.020),
                       (0.072, V_V + 0.022, V_V + 0.064),
                       (0.966, V_Z + 0.032, V_Z + 0.080),
                       (0.940, V_Z + DV - 0.066, V_Z + DV - 0.022)):
        out += _poly([(U(uu), V(v0)), (U(uu), V(v1))], color=pen, f=F_FINE)

    # registration crosses, four corners
    for uu, vv in ((0.028, 0.028), (0.972, 0.028), (0.028, 0.972), (0.972, 0.972)):
        x, y = U(uu), V(vv)
        out += _poly([(x - 5.2, y), (x + 5.2, y)], color=pen, f=F_FINE)
        out += _poly([(x, y - 5.2), (x, y + 5.2)], color=pen, f=F_FINE)

    # bottom axis: forward left, backward right, one dot between
    ya = V(V_AXIS)
    fx0, fx1 = U(0.028), U(0.468)
    bx0, bx1 = U(0.532), U(0.972)
    tw_f, tw_b = 24.0, 26.0
    cf, cb = (fx0 + fx1) / 2.0, (bx0 + bx1) / 2.0
    out += _poly([(fx0, ya), (cf - tw_f / 2.0 - 3.5, ya)], color=pen, f=F_FINE)
    out += _poly([(cf + tw_f / 2.0 + 3.5, ya), (fx1, ya)], color=pen, f=F_FINE)
    out += _chevron(fx1, ya, 1, 2.6, pen)
    out += _tracked("forward pass", cf - tw_f / 2.0, ya - 1.2, 2.7, pen, target_w=tw_f)
    out += _poly([(bx0, ya), (cb - tw_b / 2.0 - 3.5, ya)], color=pen, f=F_FINE)
    out += _poly([(cb + tw_b / 2.0 + 3.5, ya), (bx1, ya)], color=pen, f=F_FINE)
    out += _chevron(bx0, ya, -1, 2.6, pen)
    out += _tracked("backward pass", cb - tw_b / 2.0, ya - 1.2, 2.7, pen, target_w=tw_b)
    out += _mark(U(0.500), ya, 1.15, pen)

    # a handful of quiet floating dots, kept out of every dense zone
    forbid = [
        (U(0.0), V(0.480), U(1.0), V(0.055)),
        (U(0.0), V(0.915), U(1.0), V(0.525)),
        (U(0.0), V(V_AXIS + 0.030), U(1.0), V(V_AXIS - 0.025)),
    ]
    done: List[Pt] = []
    tries = 0
    while len(done) < 6 and tries < 1500:
        tries += 1
        px = rng.uniform(fr.x0 + 6, fr.x1 - 6)
        py = rng.uniform(fr.y0 + 6, fr.y1 - 6)
        if any(a <= px <= c and b <= py <= d for a, b, c, d in forbid):
            continue
        if any(math.hypot(px - qx, py - qy) < 30.0 for qx, qy in done):
            continue
        out += _mark(px, py, rng.choice([0.42, 0.65, 1.0]), pen)
        done.append((px, py))
    return out
