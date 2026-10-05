"""SOFTMAX IS A VANISHING POINT — attention as a pencil of lines through one point.

ABSTRACT ORDER: PROJECTIVE.  One operation builds the whole plate — a rail cut
by a pencil of concurrent lines — and every stage of attention is an instance
of it.

    similarity   a plane collapses onto a line: the key cloud projected on q,
                 each perpendicular the component the dot product throws away
    exp          each foot opens a cell on the raw rail; the total is arbitrary
    softmax      a pencil through ONE apex cuts that rail down to a unit bar.
                 The apex is left unpainted: a vanishing point is not a place.
    merge        the unit's cells carry v as area; the output is the level at
                 which the solid surplus exactly fills the empty deficit
    backward     the SAME rays, continued past the apex — reversed in order,
                 flat-topped, because every value gets one number split by the
                 same widths:  dL/dv_j = a_j . dL/dz

The mirror is not a second register: forward and backward are one set of lines
seen on both sides of their own vanishing point.  Nothing is inherited from the
axonometric stacks (bauhaus_relevance / attention-dag), the wavepacket rows
(studio/resonance*), the head grid (attention_matrix) or the sink chords
(bauhaus_attention).

Contract:  attention_passes(rng, bounds, colors=3) -> list[GCodeCommand]
Pens:      0 black (structure, K, the pencil, type) · 1 dodgerblue (Q) ·
           2 crimson (V, the output level, and the gradient)
"""

from __future__ import annotations

import logging
import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import (  # noqa: F401
    _dot,
    _poly,
    _stroke_text,
    _text_width,
    giant_type,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

log = logging.getLogger(__name__)

Bounds = Tuple[float, float, float, float]
XY = Tuple[float, float]

BLACK, BLUE, RED = 0, 1, 2

# ---------------------------------------------------------------------------
# the design frame.  t runs along the query direction, h runs perpendicular to
# it (h increasing = down the sheet).  q sets the axis of the IMAGE; the type
# stays on the orthogonal sheet grid, and the rake between the two is the
# plate's only tension device.
# ---------------------------------------------------------------------------

THETA = 4.5                      # deg: q rakes up to the right
A0 = (14.0, 194.0)               # design-sheet position of (t=0, h=0)
CLIP = (5.0, 4.0, 384.0, 274.0)  # the design box; rays crop at it, by intent

H_SCORE = 0.0                    # the q axis — similarity happens here
H_RAW = 46.0                     # raw rail: cells = exp(s); total arbitrary
H_UNIT = 120.0                   # unit bar: cells = a; total exactly one
H_APEX = 164.0                   # the vanishing point
T_APEX = 268.0

T_RAW = 336.0                    # raw rail length: the widest thing on the sheet
T_K0, T_K1 = 24.0, 214.0         # key field extent along q
H_K0, H_K1 = -50.0, -9.0         # key field depth off the q axis

HV = 52.0                        # mm per unit of v
TARGET = 0.43                    # the loss target z is compared against
SCORE_SCALE = 42.0               # mm of q axis per unit of score
T_SCORE_MID = 128.0

N_KEYS = 12
MIN_CELL = 1.25                  # mm: below this a cell cannot be ruled at all
APEX_GAP = 4.2                   # mm: the unpainted hole at the vanishing point

_C = math.cos(math.radians(THETA))
_S = math.sin(math.radians(THETA))


def TH(t: float, h: float) -> XY:
    """(t, h) in the query frame -> design-sheet mm."""
    return (A0[0] + t * _C + h * _S, A0[1] + t * _S - h * _C)


# ---------------------------------------------------------------------------
# line primitives
# ---------------------------------------------------------------------------


def _line(p0: XY, p1: XY, passes: int = 1, gap: float = 0.32,
          pen: Optional[int] = None, f: int = 1900) -> List[GCodeCommand]:
    """Straight sheet-space line; ``passes`` parallel passes = line weight."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    if L < 1e-9:
        return []
    nx, ny = -dy / L, dx / L
    out: List[GCodeCommand] = []
    for k in range(passes):
        d = 0.0 if passes == 1 else -gap * (passes - 1) / 2.0 + gap * k
        out += _poly([(p0[0] + nx * d, p0[1] + ny * d),
                      (p1[0] + nx * d, p1[1] + ny * d)], color=pen, f=f)
    return out


def _tline(t0: float, h0: float, t1: float, h1: float, passes: int = 1,
           pen: Optional[int] = None, f: int = 1900) -> List[GCodeCommand]:
    return _line(TH(t0, h0), TH(t1, h1), passes=passes, pen=pen, f=f)


def _hatch_th(t0: float, t1: float, h0: float, h1: float, spacing: float,
              along: str = "t", pen: Optional[int] = None,
              f: int = 2100) -> List[GCodeCommand]:
    """Serpentine fill of a (t, h) rectangle.  ``along`` chooses the grain."""
    if t1 - t0 < 0.3 or h1 - h0 < 0.3:
        return []
    pts: List[XY] = []
    flip = False
    if along == "t":
        h = h0
        while h <= h1 + 1e-9:
            row = [(t0, h), (t1, h)]
            pts.extend(reversed(row) if flip else row)
            flip = not flip
            h += spacing
    else:
        t = t0
        while t <= t1 + 1e-9:
            col = [(t, h0), (t, h1)]
            pts.extend(reversed(col) if flip else col)
            flip = not flip
            t += spacing
    return _poly([TH(t, h) for t, h in pts], color=pen, f=f)


def _rect_th(t0: float, t1: float, h0: float, h1: float, passes: int = 1,
             pen: Optional[int] = None) -> List[GCodeCommand]:
    ring = [(t0, h0), (t1, h0), (t1, h1), (t0, h1), (t0, h0)]
    out: List[GCodeCommand] = []
    for i in range(4):
        out += _tline(*ring[i], *ring[i + 1], passes=passes, pen=pen)
    return out


def _clip(p0: XY, p1: XY, box: Tuple[float, float, float, float]):
    """Liang-Barsky.  Rays past the apex run off the sheet; they crop there."""
    x0, y0, x1, y1 = box
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    u0, u1 = 0.0, 1.0
    for pp, qq in ((-dx, p0[0] - x0), (dx, x1 - p0[0]),
                   (-dy, p0[1] - y0), (dy, y1 - p0[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return None
            continue
        r = qq / pp
        if pp < 0:
            u0 = max(u0, r)
        else:
            u1 = min(u1, r)
        if u0 > u1:
            return None
    return ((p0[0] + dx * u0, p0[1] + dy * u0),
            (p0[0] + dx * u1, p0[1] + dy * u1))


def _ray(pa: XY, pb: XY, apex: XY, passes: int = 1, pen: Optional[int] = None,
         f: int = 2000) -> List[GCodeCommand]:
    """A ray of the pencil, drawn with a hole punched around the apex."""
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]
    L = math.hypot(dx, dy)
    if L < 1e-9:
        return []
    d_ap = math.hypot(apex[0] - pa[0], apex[1] - pa[1])
    out: List[GCodeCommand] = []
    for s0, s1 in ((0.0, max(0.0, (d_ap - APEX_GAP) / L)),
                   (min(1.0, (d_ap + APEX_GAP) / L), 1.0)):
        if s1 - s0 < 1e-3:
            continue
        seg = _clip((pa[0] + dx * s0, pa[1] + dy * s0),
                    (pa[0] + dx * s1, pa[1] + dy * s1), CLIP)
        if seg is None:
            continue
        out += _line(seg[0], seg[1], passes=passes, pen=pen, f=f)
    return out


def _ring(cx: float, cy: float, r: float, pen: Optional[int] = None,
          n: int = 20, f: int = 2300) -> List[GCodeCommand]:
    return _poly([(cx + r * math.cos(2 * math.pi * k / n),
                   cy + r * math.sin(2 * math.pi * k / n))
                  for k in range(n + 1)], color=pen, f=f)


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def attention_passes(rng: SeededRNG, bounds: Bounds,
                     colors: int = 3) -> List[GCodeCommand]:
    blk = BLACK % colors if colors > 1 else None
    blu = BLUE % colors if colors > 1 else None
    red = RED % colors if colors > 1 else None

    out: List[GCodeCommand] = []

    # =============== the numbers — exact, and all derived here ============
    step = (T_K1 - T_K0) / N_KEYS
    ts = sorted(T_K0 + step * (i + 0.5 + rng.uniform(-0.48, 0.48))
                for i in range(N_KEYS))
    hs = [rng.uniform(H_K0, H_K1) for _ in range(N_KEYS)]
    # the perpendicular IS the component the dot product discards, so its
    # length has to visibly vary: pin one key onto the axis and one far off.
    hs[-2] = H_K1 - 1.0
    hs[3] = H_K0 + 0.5

    # q points LEFT: the leftmost key scores highest.  The raw rail then runs
    # wide -> narrow and its crowded end sits under the apex, where a vanishing
    # point turns crowding into angular spread instead of a smear.
    scores = [(T_SCORE_MID - t) / SCORE_SCALE for t in ts]
    exps = [math.exp(s) for s in scores]
    E = sum(exps)
    att = [e / E for e in exps]

    vals = [rng.uniform(0.20, 1.0) for _ in range(N_KEYS)]
    vals[0] = 0.86          # the winner carries a large value ...
    vals[1] = 0.27          # ... its neighbour almost none ...
    vals[2] = 0.99          # ... and a near-loser the loudest of all, so the
    vals[4] = 0.21          # output is a real average, not the argmax
    Z = sum(a * v for a, v in zip(att, vals))
    G = 2.0 * (Z - TARGET)  # dL/dz for a square loss against TARGET
    G_draw = min(max(abs(G), 0.22), 0.62)   # keep the back rail on the sheet
    if abs(abs(G) - G_draw) > 1e-9:
        log.warning("gradient rail drawn at %.3f, not %.3f (off-sheet)", G_draw, G)

    cum = [0.0]
    for e in exps:
        cum.append(cum[-1] + e)
    t_raw = [T_RAW * c / E for c in cum]

    def ray_t(t_r: float, h: float) -> float:
        """Where the ray through (t_r, H_RAW) and the apex meets height h."""
        return T_APEX + (h - H_APEX) / (H_RAW - H_APEX) * (t_r - T_APEX)

    f_unit = (H_UNIT - H_APEX) / (H_RAW - H_APEX)
    h_grad = H_APEX - G_draw * f_unit * (H_RAW - H_APEX)
    t_unit = [ray_t(t, H_UNIT) for t in t_raw]
    t_grad = [ray_t(t, h_grad) for t in t_raw]
    L_unit = t_unit[-1] - t_unit[0]
    L_grad = t_grad[0] - t_grad[-1]
    h_grad_back = h_grad + G_draw * HV
    h_z = H_UNIT - Z * HV
    apex = TH(T_APEX, H_APEX)

    win = max(range(N_KEYS), key=lambda j: att[j])
    order = sorted(range(N_KEYS), key=lambda j: att[j], reverse=True)
    tail = [j for j in range(N_KEYS) if (t_unit[j + 1] - t_unit[j]) < MIN_CELL]

    log.info(
        "attention_passes N=%d  sum exp=%.3f  a_max=%.4f  Z=%.4f  dL/dz=%.4f | "
        "rails  raw=%.1f  unit=%.1f  grad=%.1f mm | crush %.2f x | "
        "tail %d cells = %.3f mass | min cell %.2f mm",
        N_KEYS, E, att[win], Z, G, T_RAW, L_unit, L_grad, T_RAW / L_unit,
        len(tail), sum(att[j] for j in tail),
        min(t_unit[j + 1] - t_unit[j] for j in range(N_KEYS)),
    )

    def w_of(j: int) -> int:
        """line weight from the attention share — the plate's only tone scale"""
        a = att[j]
        return 3 if j == win else (2 if a > 0.085 else 1)

    # =============== 1. THE KEY FIELD — a plane collapses onto a line =====
    # q: one oriented line, no magnitude, running off both edges of the plate.
    seg = _clip(TH(-14.0, H_SCORE), TH(T_RAW + 40.0, H_SCORE), CLIP)
    out += _line(seg[0], seg[1], passes=3, pen=blu, f=1700)
    tq = -4.0
    while tq < T_RAW + 24.0:
        # a direction has a sense but no origin: the ladder grows toward +q
        g = 0.9 + 4.2 * max(0.0, 1.0 - tq / (T_RAW + 24.0)) ** 1.6
        out += _tline(tq, -g, tq, g, passes=2 if g > 3.2 else 1, pen=blu, f=2400)
        tq += 10.5

    for j in range(N_KEYS):
        p = w_of(j)
        out += _tline(ts[j], hs[j], ts[j], -0.9, passes=p, pen=blk, f=2000)
        out += _ring(*TH(ts[j], hs[j]), 1.45, pen=blk)
        if j == win:
            out += _dot(*TH(ts[j], H_SCORE), r=1.15, color=blk)
            out += _dot(*TH(ts[j], H_SCORE), r=0.75, color=blk)
        else:
            out += _dot(*TH(ts[j], H_SCORE), r=0.55, color=blk)

    # the gradient comes back up the same three lines: the only arrowheads here
    for j in order[:3]:
        ch = 0.52 * hs[j]
        out += _line(TH(ts[j] - 1.6, ch + 2.8), TH(ts[j], ch), passes=2, pen=blk, f=2400)
        out += _line(TH(ts[j] + 1.6, ch + 2.8), TH(ts[j], ch), passes=2, pen=blk, f=2400)

    # =============== 2. EXP — each foot opens a cell on the raw rail ======
    for j in range(N_KEYS):
        tc = 0.5 * (t_raw[j] + t_raw[j + 1])
        out += _tline(ts[j], 2.0, tc, H_RAW - 1.4,
                      passes=2 if j == win else 1, pen=blk, f=2000)

    out += _tline(t_raw[0], H_RAW, t_raw[-1], H_RAW, passes=3, pen=blk, f=1700)
    for j in range(N_KEYS + 1):
        out += _tline(t_raw[j], H_RAW - 3.0, t_raw[j], H_RAW + 3.0, pen=blk, f=2300)

    # =============== 3. THE PENCIL — softmax ==============================
    h_end = h_grad_back + 2.5
    for j in range(N_KEYS + 1):
        # the two outer rays are the walls of the funnel: draw them heavier so
        # the constriction reads as a SHAPE, not as a bundle of hairlines.
        p = 2 if j in (0, N_KEYS) else 1
        out += _ray(TH(t_raw[j], H_RAW), TH(ray_t(t_raw[j], h_end), h_end),
                    apex, passes=p, pen=blk)
    # the traced weights: cell centre lines, the winner heaviest — one path you
    # can follow key -> foot -> cell -> one -> apex -> gradient without a break
    for j in order[:3]:
        tc = 0.5 * (t_raw[j] + t_raw[j + 1])
        out += _ray(TH(tc, H_RAW), TH(ray_t(tc, h_end), h_end), apex,
                    passes=w_of(j), pen=blk, f=1800)
    out += _ring(*apex, APEX_GAP, pen=blk, n=48)
    out += _ring(apex[0] + 0.34, apex[1], APEX_GAP, pen=blk, n=48)

    # =============== 4. THE UNIT BAR — one, and the merge =================
    out += _tline(t_unit[0], H_UNIT, t_unit[-1], H_UNIT, passes=3, pen=blk, f=1700)

    # ONE stepped silhouette: cell width = a_j, cell height = v_j, so every
    # cell's AREA is a_j.v_j and the whole area is the output.
    # cells under the pen tip are merged into ONE step at their weighted mean
    # v -- drawing a 0.7 mm zigzag would be a lie the plotter cannot tell.
    steps: List[Tuple[float, float, float]] = []
    j = 0
    while j < N_KEYS:
        if t_unit[j + 1] - t_unit[j] >= MIN_CELL:
            steps.append((t_unit[j], t_unit[j + 1], vals[j]))
            j += 1
            continue
        k = j
        wa = wv = 0.0
        while k < N_KEYS and t_unit[k + 1] - t_unit[k] < MIN_CELL:
            wa += att[k]
            wv += att[k] * vals[k]
            k += 1
        steps.append((t_unit[j], t_unit[k], wv / wa if wa else 0.0))
        j = k

    prof: List[XY] = [(t_unit[0], H_UNIT)]
    for t0, t1, v in steps:
        h_top = H_UNIT - v * HV
        prof += [(t0, h_top), (t1, h_top)]
    prof += [(t_unit[-1], H_UNIT), (t_unit[0], H_UNIT)]
    out += _poly([TH(t, h) for t, h in prof], color=red, f=1800)
    out += _poly([TH(t, h + 0.34) for t, h in prof], color=red, f=1800)

    # solid, grain ALONG the rails (the forward grain).  The output level then
    # states the balance directly: the crimson standing above the rule has
    # exactly the area of the paper left under it.
    for t0, t1, v in steps:
        out += _hatch_th(t0 + 0.5, t1 - 0.5, H_UNIT - v * HV + 0.5, H_UNIT - 0.4,
                         0.86, along="t", pen=red, f=2200)

    # the output: the level at which surplus and deficit are equal areas
    out += _tline(t_unit[0] - 15.0, h_z, t_unit[-1] + 9.0, h_z,
                  passes=4, pen=red, f=1700)

    if tail:
        t0, t1 = t_unit[min(tail)], t_unit[max(tail) + 1]
        out += _tline(t0, H_UNIT + 4.5, t1, H_UNIT + 4.5, pen=blk, f=2300)
        out += _tline(t0, H_UNIT + 2.6, t0, H_UNIT + 6.4, pen=blk, f=2300)
        out += _tline(t1, H_UNIT + 2.6, t1, H_UNIT + 6.4, pen=blk, f=2300)

    # =============== 5. THE GRADIENT RAIL — past the apex =================
    gl, gr = min(t_grad[0], t_grad[-1]), max(t_grad[0], t_grad[-1])
    out += _tline(gl, h_grad, gr, h_grad, passes=2, pen=blk, f=1700)
    out += _hatch_th(gl + 0.35, gr - 0.35, h_grad + 0.35, h_grad_back - 0.35,
                     0.72, along="h", pen=red, f=2200)
    out += _tline(gl - 9.0, h_grad_back, gr + 7.0, h_grad_back,
                  passes=4, pen=red, f=1700)
    out += _tline(gl, h_grad, gl, h_grad_back, passes=2, pen=blk, f=2000)
    out += _tline(gr, h_grad, gr, h_grad_back, passes=2, pen=blk, f=2000)

    # =============== 6. TYPE — flush left, on the orthogonal sheet grid ===
    out += _line((26.0, 116.0), (70.0, 116.0), passes=3, pen=blk, f=1800)
    out += _stroke_text("forward and backward", 26.0, 106.0, 2.7, color=blk)
    for i, ln in enumerate(("SOFTMAX", "IS A", "VANISHING", "POINT")):
        out += giant_type(ln, 26.0, 91.0 - 18.0 * i, 14.0, pen=blk,
                          weight=0.8, tip=0.35)

    data = [
        "12 keys · sum exp s = %.2f · sum a = %.3f · a max = %.3f · z = %.3f"
        % (E, sum(att), att[win], Z),
        "one = %.0f mm cut from %.0f mm  ·  ∂L/∂v j = %.3f × a j  ·  same rays"
        % (L_unit, T_RAW, G),
        "%d cells fall under the pen tip: %.3f of the mass, merged"
        % (len(tail), sum(att[j] for j in tail)),
    ]
    for i, ln in enumerate(data):
        out += _stroke_text(ln, 26.0, 23.0 - 6.2 * i, 2.3, color=blk)

    # =============== 7. the three kinds, named once, on their geometry ====
    out += giant_type("q", *TH(-7.0, 21.0), 16.0, pen=blu, weight=0.5, tip=0.35)
    j_hi = min(range(N_KEYS), key=lambda j: hs[j])
    out += giant_type("k", *TH(ts[j_hi] + 8.0, hs[j_hi] - 8.0), 16.0, pen=blk,
                      weight=0.5, tip=0.35)
    j_tall = max(range(N_KEYS), key=lambda j: vals[j])
    out += giant_type("v", *TH(t_unit[j_tall] - 17.0,
                               H_UNIT - vals[j_tall] * HV + 0.5),
                      16.0, pen=red, weight=0.5, tip=0.35)

    out += _stroke_text("softmax", apex[0] + 6.5, apex[1] + 4.8, 3.0, color=blk)
    out += _stroke_text("s = q · k j", *TH(7.0, 26.0), 3.0, color=blk)
    out += _stroke_text("exp s", *TH(5.0, H_RAW - 7.0), 3.0, color=blk)
    out += _stroke_text("one", *TH(t_unit[0] - 26.0, H_UNIT + 1.5), 3.0, color=blk)
    out += giant_type("z", *TH(t_unit[0] - 26.0, h_z - 2.4), 10.0, pen=red,
                      weight=0.5, tip=0.35)
    out += _stroke_text("∂L/∂z", *TH(gl - 30.0, h_grad_back + 6.0), 3.2, color=red)

    # registration: two marks only — they also declare the design box
    for cx, cy in ((9.0, 269.0), (376.0, 9.0)):
        out += _line((cx - 4.5, cy), (cx + 4.5, cy), pen=blk, f=2400)
        out += _line((cx, cy - 4.5), (cx, cy + 4.5), pen=blk, f=2400)

    return _fit(out, bounds)


# ---------------------------------------------------------------------------


def _fit(cmds: Sequence[GCodeCommand], bounds: Bounds,
         inset: float = 0.6) -> List[GCodeCommand]:
    """Uniform fit of the whole composition into the drawable area."""
    xs = [c.x for c in cmds if c.x is not None]
    ys = [c.y for c in cmds if c.y is not None]
    if not xs or not ys:
        return list(cmds)
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    x0, y0, x1, y1 = bounds
    tw, th = (x1 - x0) - 2 * inset, (y1 - y0) - 2 * inset
    sc = min(tw / max(bx1 - bx0, 1e-6), th / max(by1 - by0, 1e-6))
    ox = x0 + inset + (tw - (bx1 - bx0) * sc) / 2.0
    oy = y0 + inset + (th - (by1 - by0) * sc) / 2.0
    out: List[GCodeCommand] = []
    for c in cmds:
        if c.x is None and c.y is None:
            out.append(c)
            continue
        out.append(c.model_copy(update={
            "x": None if c.x is None else round(ox + (c.x - bx0) * sc, 3),
            "y": None if c.y is None else round(oy + (c.y - by0) * sc, 3),
        }))
    log.info("fit: design %.1f x %.1f mm -> scale %.4f", bx1 - bx0, by1 - by0, sc)
    return out
