"""THE MIRROR FORGETS — cnn-passes, round r03.

NOT a recreation of ``studio/cnn-passes/ref/reference.png``.  The reference is a
left-to-right pipeline of stacked planes, forward on top and backward below.
This round keeps what the reference is ABOUT — the forward/backward mirror, the
constriction of spatial detail into a class probability, gating and scattering —
and transposes it into a different abstract ORDER.

    THE ORDER: NESTED ANNULI.  A polar lattice that trades angular resolution
    for radial resolution, turn by turn.  One band = one stage.  Its OUTER half
    carries the forward pass, its INNER half the gradient, so a stage and its
    twin share a RADIUS exactly the way the reference's twins share a column.
    Forward runs inward and ends as one number; the gradient is born there and
    climbs back out through the same lattice.

The exact mappings (per DESIGN_RUBRIC: "the maths supplies the NUMBERS, the
order supplies the FORM, and the mapping is exact and stated in one line"):

    angular cell count  = spatial resolution      (halves at every pool)
    radial sub-ring     = one channel             (doubles at every conv)
    arc duty in a cell  = |activation|            (magnitude; spacing is fixed)
    blank paper         = relu closed             (the negative lobes of the
                                                   stage's angular response)
    same angle, both halves of a band  = the chain rule shares the mask
    sector angle        = softmax probability     (they close the circle)
    thread break        = a gradient that died    (measured, printed)

Style canon: SWISS / INTERNATIONAL TYPOGRAPHIC (STYLES.md #3).  A documented
modular grid (10 x 7, 4 mm gutter) that every element snaps to, flush-left type
at poster scale, ONE huge element cropped hard at two edges, radical negative
space, zero ornament, no leader line that crosses another.

Flatness is DECLARED, per dimension 7: Swiss is a flat canon, and here the
radius is the depth axis — it carries the whole argument — so a picture-plane
depth cue would compete with the one thing the plate is about.  The single
overlap on the sheet is the tracked channel's thread, which passes OVER every
ring it crosses and knocks a 1.15 mm gap in it.  That knockout is computed
analytically from the spiral's own equation, never left to chance.

Pens (``colors=3``): 0 black = the forward lattice, structure, type.
1 dodgerblue = the ONE tracked channel and the class it elects — scarce and
loud.  2 crimson = the whole backward pass.  Cream paper is the fourth colour
and it is what does the gating.

Entry point: ``cnn_passes``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import (
    _clip_runs,
    _rect_keep,
    _runs_from_cmds_pens,
    giant_type,
)
from promptplot.generative.generators import _poly, _stroke_text, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]
Iv = Tuple[float, float]

BLACK, BLUE, RED = 0, 1, 2
F_DRAW = 2200
F_FINE = 2400
TAU = 2.0 * math.pi

MIN_PITCH = 0.85   # mm — hard floor on any ring family (DESIGN_RUBRIC dim 5)
KNOCKOUT = 1.15    # mm of blank paper either side of the thread


# ===========================================================================
# 1.  the network
# ===========================================================================
# n = angular cells (spatial resolution).  c = radial sub-rings (channels).
# conv preserves n and grows c; pool halves n and preserves c.
# Read outward-to-inward = the forward pass.


class Stage:
    def __init__(self, key, n, c, kind, label, shape, note):
        self.key, self.n, self.c, self.kind = key, n, c, kind
        self.label, self.shape, self.note = label, shape, note


STAGES: List[Stage] = [
    Stage("x",  256, 3,  "input", "x",  "256 x 3",  "input"),
    Stage("a1", 256, 6,  "conv",  "a1", "256 x 6",  "conv  relu"),
    Stage("p1", 128, 6,  "pool",  "p1", "128 x 6",  "max pool 2"),
    Stage("a2", 128, 12, "conv",  "a2", "128 x 12", "conv  relu"),
    Stage("p2", 64,  12, "pool",  "p2", "64 x 12",  "max pool 2"),
]

N_CLASS = 9
M0 = 22          # top angular frequency the input carries
RIM = 3.5        # mm of paper outside the input band
CORE_R = 22.0    # mm — the classifier disc
GAP_FB = 1.15    # mm between a band's forward half and its backward half
GAP_BAND = 6.0   # mm between bands.  DELIBERATELY 5x GAP_FB: it is what makes
                 # a band read as ONE object with a black half and a crimson
                 # half, instead of ten unrelated rings.

WEDGE_DEG = 22.5   # one sixteenth of the field — the plate's "column"


class Band:
    """One stage placed on the sheet: its radii and its two masks."""

    def __init__(self, st):
        self.st = st
        self.r_fwd: List[float] = []
        self.r_bwd: List[float] = []
        self.act = None      # (c, n) relu'd activation
        self.on = None       # (c, n) bool — forward inked
        self.alive = None    # (c, n) bool — gradient inked
        self.r_out = 0.0
        self.r_in = 0.0


# ===========================================================================
# 2.  geometry helpers
# ===========================================================================


def _arc_pts(cx, cy, r, a0, a1, step: float = 1.1) -> Poly:
    span = a1 - a0
    n = max(2, int(abs(span) * r / step) + 1)
    return [(cx + r * math.cos(a0 + span * k / n),
             cy + r * math.sin(a0 + span * k / n)) for k in range(n + 1)]


def _ray(cx, cy, r0, r1, a) -> Poly:
    return [(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
            (cx + r1 * math.cos(a), cy + r1 * math.sin(a))]


def _emit(polys: Sequence[Poly], pen: int, f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _seg(a: Pt, b: Pt) -> Poly:
    return [a, b]


def _text(s, x, y, h, pen, f: int = F_FINE) -> List[GCodeCommand]:
    return _stroke_text(s, x, y, h, color=pen, f=f)


def _sub_intervals(iv: Iv, cuts: Sequence[Iv]) -> List[Iv]:
    parts: List[Iv] = [iv]
    for c0, c1 in cuts:
        nxt: List[Iv] = []
        for a0, a1 in parts:
            if c1 <= a0 or c0 >= a1:
                nxt.append((a0, a1))
                continue
            if c0 > a0:
                nxt.append((a0, c0))
            if c1 < a1:
                nxt.append((c1, a1))
        parts = nxt
    return [p for p in parts if p[1] - p[0] > 2e-4]


def _runs_from_mask(mask: Sequence[bool]) -> List[Tuple[int, int]]:
    """Maximal runs of True as (start, end_exclusive), wrapping at the seam."""
    n = len(mask)
    if all(mask):
        return [(0, n)]
    if not any(mask):
        return []
    start = next(i for i in range(n) if mask[i] and not mask[i - 1])
    runs: List[Tuple[int, int]] = []
    i = 0
    while i < n:
        k = (start + i) % n
        if mask[k]:
            j = i
            while j < n and mask[(start + j) % n]:
                j += 1
            runs.append((start + i, start + j))
            i = j
        else:
            i += 1
    return runs


# ===========================================================================
# 3.  the gate field
# ===========================================================================
# Every stage shares ONE set of Fourier coefficients and keeps only its first
# M_l of them.  That is what pooling physically is — a low-pass — and it is
# also what makes the wide blank wedges line up radially across the whole
# plate: the coarse structure survives every stage, the fine structure does
# not.  The alignment is not a layout choice; it is the low-pass.


class GateField:
    def __init__(self, rng: SeededRNG):
        self.amp = [1.0 / (m ** 0.85) for m in range(1, M0 + 1)]
        self.ph = [rng.uniform(0.0, TAU) for _ in range(M0)]
        self.norm = math.sqrt(sum(a * a for a in self.amp) * 0.5)

    def eval(self, theta: np.ndarray, m_max: int, dtheta: float = 0.0) -> np.ndarray:
        z = np.zeros_like(theta)
        for m in range(1, m_max + 1):
            z += self.amp[m - 1] * np.cos(m * (theta + dtheta) + self.ph[m - 1])
        return z / self.norm


def _m_for(n: int) -> int:
    return max(3, int(round(M0 * n / STAGES[0].n)))


# ===========================================================================
# 4.  bands
# ===========================================================================


def _radii(R: float) -> Tuple[List[Band], float]:
    sum_c = sum(s.c for s in STAGES)
    budget = R - RIM - CORE_R - GAP_FB * len(STAGES) - GAP_BAND * (len(STAGES) - 1)
    pitch = max(MIN_PITCH, budget / (2.0 * sum_c))

    bands: List[Band] = []
    r = R - RIM
    for i, st in enumerate(STAGES):
        b = Band(st)
        b.r_out = r
        b.r_fwd = [r - k * pitch for k in range(st.c)]
        r -= (st.c - 1) * pitch + GAP_FB
        b.r_bwd = [r - k * pitch for k in range(st.c)]
        r -= (st.c - 1) * pitch
        b.r_in = r
        if i < len(STAGES) - 1:
            r -= GAP_BAND
        bands.append(b)
    return bands, pitch


def _forward(bands: List[Band], gf: GateField, rng: SeededRNG) -> None:
    for b in bands:
        st = b.st
        m = _m_for(st.n)
        th = np.arange(st.n) * TAU / st.n + TAU / (2 * st.n)
        shear = 0.5 * (TAU / m)     # channels are the same bank, rotated a little
        act = np.zeros((st.c, st.n))
        on = np.zeros((st.c, st.n), dtype=bool)
        for c in range(st.c):
            d = shear * ((c / max(1, st.c - 1)) - 0.5)
            bias = rng.gauss(0.0, 0.30) - 0.14
            z = gf.eval(th, m, d) + bias
            if st.kind == "input":
                act[c] = np.abs(z) + 0.2      # the raw image is not gated
                on[c] = True
            else:
                act[c] = np.maximum(0.0, z)
                on[c] = z > 0.0
        b.act, b.on = act, on


def _argmax_window(act: np.ndarray, w: int) -> np.ndarray:
    c, n = act.shape
    keep = np.zeros((c, n), dtype=bool)
    for ch in range(c):
        for j in range(0, n, w):
            keep[ch, j + int(np.argmax(act[ch, j:j + w]))] = True
    return keep


def _smear(prof: np.ndarray, k: int = 1) -> np.ndarray:
    out = prof.copy()
    for s in range(1, k + 1):
        out = out | np.roll(prof, s) | np.roll(prof, -s)
    return out


def _backward(bands: List[Band], rng: SeededRNG) -> None:
    """Gradient support, computed from the core OUTWARD — the return trip.

    p2  dense    every pooled activation is wired to the classifier
    a2  sparse   unpool: one cell per 2-window, and only where relu let it
    p1  medium   the conv backward smears each live cell over the kernel
    a1  sparse   unpool again
    x   medium   the conv backward; the input itself has no gate
    """
    carried: Optional[np.ndarray] = None
    for b in reversed(bands):
        st = b.st
        if carried is None:
            b.alive = np.ones((st.c, st.n), dtype=bool)
        elif st.kind == "conv":
            w = max(1, st.n // carried.shape[1])
            up = np.repeat(carried, w, axis=1)[:, :st.n]
            if up.shape[0] != st.c:
                up = np.resize(up, (st.c, st.n))
            keep = _argmax_window(b.act, w) if w > 1 else np.ones_like(b.on)
            b.alive = b.on & keep & up
        else:
            prof = carried.any(axis=0)
            w = max(1, st.n // carried.shape[1])
            prof = np.repeat(prof, w)[:st.n] if w > 1 else prof[:st.n]
            prof = _smear(prof, 1)
            live = np.tile(prof, (st.c, 1))
            if st.kind == "input":
                b.alive = live
            else:
                thin = np.array([[rng.random() < 0.84 for _ in range(st.n)]
                                 for _ in range(st.c)])
                b.alive = live & thin
        carried = b.alive


# ===========================================================================
# 5.  the tracked channel's thread — the one intentional overlap
# ===========================================================================


class Corridor:
    """One sixteenth of the field, rim to core.  Its two edges are the two
    passes: the counter-clockwise edge runs IN (blue, whole), the clockwise
    edge runs OUT (crimson, broken wherever that gradient died).

    This replaced a spiral thread.  However steep the spiral was made it still
    read as one more ring, and its crimson twin sat on top of it.  The wedge
    had to exist anyway — it is the registration column — so making its two
    EDGES the two passes collapses three devices into one: the column that
    proves both passes share an angle, the trace of one channel rim-to-core
    and back, and the single intentional overlap on the sheet.
    """

    def __init__(self, a_out: float, a_back: float, r_hi: float, r_lo: float):
        self.a_out, self.a_back = a_out, a_back
        self.r_hi, self.r_lo = r_hi, r_lo

    def cuts_at(self, r: float, gap: float) -> List[Iv]:
        """Angular intervals a ring at radius r must leave blank so the
        corridor reads as passing OVER it.  Constant in r — solved, never
        sampled."""
        out: List[Iv] = []
        d = gap / max(3.0, r)
        for a in (self.a_out, self.a_back):
            a %= TAU
            out += [(a - d, a + d), (a - d - TAU, a + d - TAU),
                    (a - d + TAU, a + d + TAU)]
        return out


def _survival(bands: List[Band], a: float, track: int,
              r_lo: float, r_hi: float) -> float:
    """How far back out one trace's gradient gets before a pool drops it."""
    r = r_lo
    while r <= r_hi and _alive_at(bands, r, a, track):
        r += 0.4
    return r


def _alive_at(bands: List[Band], r: float, a: float, track: int) -> bool:
    for b in bands:
        if b.r_in - GAP_BAND * 0.5 <= r <= b.r_out + GAP_BAND * 0.5:
            c = min(track, b.st.c - 1)
            k = int(((a % TAU) / TAU) * b.st.n) % b.st.n
            return bool(b.alive[c, k])
    return True


def _chevron(cx, cy, r, a, inward: bool) -> Poly:
    d = -1.0 if inward else 1.0
    w = 0.030
    return [(cx + (r + d * 3.6) * math.cos(a - w),
             cy + (r + d * 3.6) * math.sin(a - w)),
            (cx + r * math.cos(a), cy + r * math.sin(a)),
            (cx + (r + d * 3.6) * math.cos(a + w),
             cy + (r + d * 3.6) * math.sin(a + w))]


# ===========================================================================
# 6.  the plate
# ===========================================================================


def cnn_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    fx0, fy0, fx1, fy1 = x0 + 4.0, y0 + 4.0, x1 - 4.0, y1 - 4.0
    W, H = fx1 - fx0, fy1 - fy0

    # ---- the module: 10 columns x 7 rows, 4 mm gutter.  Everything snaps. --
    COLS, ROWS, GUT = 10, 7, 4.0
    cw = (W - GUT * (COLS - 1)) / COLS
    rh = (H - GUT * (ROWS - 1)) / ROWS
    colx = lambda c: fx0 + c * (cw + GUT)
    rowy = lambda r: fy1 - r * (rh + GUT)          # r counted from the TOP

    cx, cy = colx(7.5), rowy(4.5)                  # the huge element, on-grid
    R = 0.50 * H

    TYPE_L = fx0 + 1.5                              # the flush-left axis
    TYPE_W = 118.0                                  # leaves a 33 mm crescent

    bands, pitch = _radii(R)
    gf = GateField(rng)
    _forward(bands, gf, rng)
    _backward(bands, rng)

    # THE CORRIDOR — one sixteenth of the field, rim to core, cut through all
    # ten sub-bands.  The reference's shared COLUMN, transposed to the polar
    # order; its two edges are the two passes.
    r_hi, r_lo = bands[0].r_out + 7.0, CORE_R - 1.0
    cell0 = TAU / STAGES[0].n
    cand = []
    # 130..190 deg: the arc on which both edges, out to r_hi, stay inside the
    # frame AND cross inked lattice rather than a wedge the gate emptied.
    for k in range(int(math.radians(130) / cell0), int(math.radians(190) / cell0)):
        a = k * cell0
        cand.append((_survival(bands, a, 1, r_lo, r_hi), a))
    cand.sort()
    a_back = cand[len(cand) // 2][1]                    # the median angle
    cor = Corridor(a_out=a_back + 16 * cell0, a_back=a_back,
                   r_hi=r_hi, r_lo=r_lo)                 # exactly 16 cells wide
    wedge = (cor.a_back, cor.a_out)

    out: List[GCodeCommand] = []
    out += _lattice(bands, cor, cx, cy)
    out += _registration(bands, cx, cy, wedge)
    out += _core(rng, cx, cy)
    cmds, l_out, l_back = _corridor(bands, cor, cx, cy, track=1)
    out += cmds
    out += _orientation(cx, cy, R, TYPE_L, TYPE_W)
    out += _typography(bands, cx, cy, R, fx0, fy0, fx1, fy1,
                       TYPE_L, TYPE_W, rowy, l_out, l_back, pitch)

    # ---- crop at the frame EXACTLY.  Clamping folds a stroke onto the
    # margin and draws a false straight edge; this cuts it. -----------------
    clipped: List[GCodeCommand] = []
    keep = _rect_keep((fx0, fy0, fx1, fy1), 0.0)
    by_pen: dict = {}
    for pen, run in _runs_from_cmds_pens(out):
        by_pen.setdefault(pen, []).append(run)
    for pen in sorted(by_pen, key=lambda p: (p is None, p)):
        clipped += _emit(_clip_runs(by_pen[pen], keep), pen, f=F_DRAW)
    return clipped


# ---------------------------------------------------------------------------
# 6a.  the lattice
# ---------------------------------------------------------------------------


def _cell_intervals(s: int, e: int, duty: np.ndarray, n: int, cell: float,
                    lo: float, hi: float) -> List[Iv]:
    """One angular interval per live cell, its length = |magnitude|.

    Spacing is FIXED (the cell grid); only the DUTY moves, per DESIGN_RUBRIC
    "tone drives DUTY, never SPACING".  Consecutive saturated cells are welded
    so a strong passage reads as one continuous arc instead of a dotted line.
    """
    ivs: List[Iv] = []
    for k in range(s, e):
        d = lo + (hi - lo) * float(duty[k % n])
        d = max(0.10, min(1.0, d))
        mid = (k + 0.5) * cell
        a0, a1 = mid - 0.5 * d * cell, mid + 0.5 * d * cell
        if d > 0.965:
            a0, a1 = k * cell, (k + 1) * cell
        if ivs and a0 - ivs[-1][1] < 1e-9:
            ivs[-1] = (ivs[-1][0], a1)
        else:
            ivs.append((a0, a1))
    return ivs


def _ring(cx, cy, r, n, mask, duty, pen, lo, hi, thr: Corridor) -> List[GCodeCommand]:
    cuts = thr.cuts_at(r, KNOCKOUT)
    cell = TAU / n
    polys: List[Poly] = []
    for s, e in _runs_from_mask(list(mask)):
        for a0, a1 in _cell_intervals(s, e, duty, n, cell, lo, hi):
            for p0, p1 in _sub_intervals((a0, a1), cuts):
                if (p1 - p0) * r < 0.32:
                    continue
                polys.append(_arc_pts(cx, cy, r, p0, p1))
    return _emit(polys, pen, f=F_DRAW)


def _lattice(bands: List[Band], thr: Corridor, cx: float, cy: float
             ) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    TRACK = 1
    for bi, b in enumerate(bands):
        st = b.st
        hi = float(np.percentile(b.act[b.act > 0], 92)) if np.any(b.act > 0) else 1.0
        duty = np.clip(b.act / max(hi, 1e-6), 0.0, 1.0)
        # the gradient fades as it climbs out: it is loudest beside the loss
        # and a scatter of ticks by the time it reaches the input.
        fade = 0.95 - 0.150 * (len(bands) - 1 - bi)
        c_track = min(TRACK, st.c - 1)
        for c, r in enumerate(b.r_fwd):
            # forward duty lives high: a strong passage reads CONTINUOUS
            lo = 0.30 if st.kind == "input" else 0.60
            if c != c_track:
                out += _ring(cx, cy, r, st.n, b.on[c], duty[c],
                             BLACK, lo, 1.0, thr)
                continue
            # the tracked channel.  Blue is spent only where this feature
            # actually fires — the top 45% of its own activation — so the
            # accent stays scarce and still carries a quantity.  Where it is
            # quiet the ring is blank paper, which is also data.
            if st.kind == "input":          # there is no "feature" yet
                out += _ring(cx, cy, r, st.n, b.on[c], duty[c],
                             BLACK, 0.30, 1.0, thr)
                continue
            loud = b.on[c] & (duty[c] > float(np.percentile(duty[c], 74)))
            for dr in (-0.18, 0.18):
                out += _ring(cx, cy, r + dr, st.n, loud, duty[c],
                             BLUE, 0.60, 1.0, thr)
        for c, r in enumerate(b.r_bwd):
            # ...and backward duty lives LOW, so the return is always broken.
            # A gradient below the floor is not drawn: the crimson half thins
            # out instead of felting into an even crimson mass.
            g = np.clip(duty[c] ** 1.55 * fade, 0.0, 1.0)
            out += _ring(cx, cy, r, st.n, b.alive[c] & (g > 0.115), g,
                         RED, 0.20, 0.62, thr)
    return out


# ---------------------------------------------------------------------------
# 6b.  registration — the corridor's rungs and the band rules
# ---------------------------------------------------------------------------


def _registration(bands: List[Band], cx: float, cy: float, wedge: Iv
                  ) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    r_out = bands[0].r_out

    # THE WEDGE — one sixteenth of the field, rim to core, through every
    # sub-band of every stage.  16 cells wide at the input, 4 at the last pool,
    # and the ticks inside it are countable: this is where the halving is
    # MEASURED rather than asserted.
    a_mid = 0.5 * (wedge[0] + wedge[1])
    # the label sits clear of the rim: inside, it lay on the input band.
    lab = "1/16 of the field"
    lw = _text_width(lab, 2.4)
    # a fixed height in the crescent, clear of the caption's baselines above
    # and of the two orientation marks below: on the bisector it landed 3 mm
    # from the end of a caption line, on the same baseline, which reads as a
    # collision however small the gap.
    ly = cy + 0.26 * (bands[0].r_out + RIM)
    # stop 5 mm clear of wherever the rim actually is at this height
    rim_x = cx - math.sqrt(max(1.0, (bands[0].r_out + RIM) ** 2 - (ly - cy) ** 2))
    out += _text(lab, rim_x - 5.0 - lw, ly - 1.0, 2.4, BLACK)
    for b in bands:
        # two passes: a hairline rung is invisible crossing a dashed band, and
        # these rungs are the registration, so they have to win the crossing.
        for r in (b.r_out, b.r_in):
            for dr in (-0.2, 0.2):
                out += _emit([_arc_pts(cx, cy, r + dr, wedge[0], wedge[1],
                                       step=0.9)], BLACK, f=F_FINE)
        # the cell comb runs OUTWARD into the 6 mm of blank between bands,
        # so 16 / 16 / 8 / 8 / 4 stays countable over the lattice.
        cell = TAU / b.st.n
        for k in range(int(wedge[0] / cell) + 1, int(wedge[1] / cell) + 1):
            out += _emit([_ray(cx, cy, b.r_out + 0.6, b.r_out + 3.6, k * cell)],
                         BLACK, f=F_FINE)

    # each band's own register rules: the two edges of its three widest closed
    # wedges, drawn ACROSS the band so the blank paper is seen to have the same
    # angular address on the forward half and on the backward half.
    for b in bands:
        if b.st.kind == "input":
            continue
        prof = b.on.any(axis=0)
        gaps = sorted(_runs_from_mask(list(~prof)), key=lambda se: se[1] - se[0],
                      reverse=True)
        cell = TAU / b.st.n
        for s, e in gaps[:2]:
            for a in (s * cell, e * cell):
                out += _emit([_ray(cx, cy, b.r_in - 0.7, b.r_out + 0.7, a)],
                             BLACK, f=F_FINE)

    # No rim-to-core spokes: with the wedge present they were a second set of
    # long rays saying the same thing, and three of them crossing a gated
    # lattice read as damage rather than as structure.
    return out


# ---------------------------------------------------------------------------
# 6c.  the core
# ---------------------------------------------------------------------------


def _core(rng: SeededRNG, cx: float, cy: float) -> List[GCodeCommand]:
    """softmax as a closed circle: the sector ANGLE is the probability, so
    normalisation is literally the circle closing.

    The network is confidently WRONG — the argmax is not the true class — which
    is the only state in which a gradient is worth drawing.  dL/dz = p - y, and
    the sign is which way the tick points.
    """
    z = [rng.gauss(0.0, 0.9) for _ in range(N_CLASS)]
    win, truth = 3, 6
    z[win] += 2.4
    z[truth] += 0.5
    e = [math.exp(v - max(z)) for v in z]
    s = sum(e)
    p = [v / s for v in e]

    out: List[GCodeCommand] = []
    rc = CORE_R
    a = math.radians(96.0)
    edges = []
    for k in range(N_CLASS):
        w = p[k] * TAU
        edges.append((a, a + w, k))
        a += w

    out += _emit([_arc_pts(cx, cy, rc, 0.0, TAU, step=0.9)], BLACK, f=F_FINE)
    for a0, a1, k in edges:
        out += _emit([_ray(cx, cy, rc - 6.0, rc, a0)], BLACK, f=F_FINE)

    # the elected class: the only filled mass on the sheet, and the thread's
    # destination.  Its angle IS its probability.
    for a0, a1, k in edges:
        if k != win:
            continue
        r = 6.2
        while r < rc - 1.1:
            out += _emit([_arc_pts(cx, cy, r, a0 + 0.04, a1 - 0.04)], BLUE, f=F_DRAW)
            r += 1.12
        for aa in (a0, a1):
            out += _emit([_ray(cx, cy, 5.0, rc, aa)], BLUE, f=F_FINE)

    # dL/dz = p - y, drawn as a crown in the blank annulus OUTSIDE the disc,
    # where crimson is legible: inside, it vanished against the elected
    # sector's fill.  Length is the magnitude; OUTWARD of the ring is
    # positive, INWARD negative — one true class pulls the other way.
    rg = rc + 4.6
    out += _emit([_arc_pts(cx, cy, rg, 0.0, TAU, step=1.2)], RED, f=F_FINE)
    for a0, a1, k in edges:
        g = p[k] - (1.0 if k == truth else 0.0)
        mid = 0.5 * (a0 + a1)
        r1 = rg + min(9.0, abs(g) * 12.0) + 0.9 * (1 if g > 0 else -1)
        if g < 0:
            r1 = rg - min(9.0, abs(g) * 12.0) - 0.9
        for dd in (-0.25, 0.25) if g < 0 else (0.0,):
            out += _emit([_ray(cx, cy, rg, r1, mid + dd / rg)], RED, f=F_FINE)

    # the scalar.  Everything the sheet holds arrives here, and leaves from it.
    out += _emit([_arc_pts(cx, cy, 4.0, 0.0, TAU, step=0.55)], RED, f=F_FINE)
    r = 0.45
    while r < 2.4:
        out += _emit([_arc_pts(cx, cy, r, 0.0, TAU, step=0.5)], RED, f=F_DRAW)
        r += 0.6
    return out


# ---------------------------------------------------------------------------
# 6d.  the corridor
# ---------------------------------------------------------------------------


def _corridor(bands: List[Band], cor: Corridor, cx: float, cy: float,
              track: int):
    """Draw both edges and MEASURE them.  The figure printed in the caption is
    the inked length of the return over the inked length of the outbound — the
    plate reading off how much of the forward pass survives the trip back."""
    out: List[GCodeCommand] = []

    # outbound: whole, three passes so it reads as a bar, chevron at the core
    for dd in (-0.24, 0.0, 0.24):
        out += _emit([_ray(cx, cy, cor.r_lo, cor.r_hi,
                           cor.a_out + dd / cor.r_hi)], BLUE, f=F_DRAW)
    out += _emit([_chevron(cx, cy, cor.r_lo, cor.a_out, True)], BLUE, f=F_FINE)
    l_out = cor.r_hi - cor.r_lo

    # return: ONE run from the core outward, stopping at the first cell the
    # gradient never reaches.  Not the union of everywhere crimson appears —
    # a trace that is dropped at a pool is dropped, and nothing further out on
    # that path hears about it again.
    r_far = _survival(bands, cor.a_back, track, cor.r_lo, cor.r_hi)
    r_far = min(r_far, cor.r_hi)
    l_back = r_far - cor.r_lo
    for dd in (-0.24, 0.0, 0.24):
        out += _emit([_ray(cx, cy, cor.r_lo, r_far,
                           cor.a_back + dd / cor.r_hi)], RED, f=F_DRAW)
    out += _emit([_chevron(cx, cy, r_far, cor.a_back, False)], RED, f=F_FINE)
    # a hairline tie across the corridor at the radius where it ran out: the
    # outbound edge carries on past it, and the gap between the two ends IS
    # the number printed in the caption.
    out += _emit([_arc_pts(cx, cy, r_far, cor.a_back, cor.a_out, step=1.4)],
                 RED, f=F_FINE)
    return out, l_out, l_back


# ---------------------------------------------------------------------------

# 6e.  orientation — two marks in the crescent, the only arrows on the sheet
# ---------------------------------------------------------------------------


def _orientation(cx, cy, R, TYPE_L, TYPE_W) -> List[GCodeCommand]:
    """The only two arrows on the sheet, and they live in the crescent — the
    band of paper between the orthogonal column and the polar mass, which
    nothing else is allowed to enter."""
    out: List[GCodeCommand] = []
    xl = TYPE_L + TYPE_W + 5.0
    for dy, pen, lab, inward in ((52.0, BLACK, "forward", True),
                                 (43.0, RED, "gradient", False)):
        y = cy + dy
        xr = cx - math.sqrt(max(1.0, R * R - dy * dy))
        out += _emit([_seg((xl, y), (xr - 2.0, y))], pen, f=F_FINE)
        tipx = (xr - 2.0) if inward else xl
        d = 1.0 if inward else -1.0
        out += _emit([[(tipx - d * 2.6, y + 1.5), (tipx, y),
                       (tipx - d * 2.6, y - 1.5)]], pen, f=F_FINE)
        out += _text(lab, xl, y + 1.9, 2.3, pen)
    return out


# ---------------------------------------------------------------------------
# 6f.  type
# ---------------------------------------------------------------------------


def _typography(bands, cx, cy, R, fx0, fy0, fx1, fy1,
                TYPE_L, TYPE_W, rowy, l_out, l_back, pitch) -> List[GCodeCommand]:
    """Flush left on one axis, flush right on the frame, everything hanging
    from a rule it shares.  Nothing is placed 'in a corner'."""
    out: List[GCodeCommand] = []

    cap = 13.4
    out += giant_type("THE MIRROR", TYPE_L, fy1 - 16.0, cap, pen=BLACK,
                      weight=1.2, tip=0.5, f=F_DRAW)
    out += giant_type("FORGETS", TYPE_L, fy1 - 34.5, cap, pen=BLACK,
                      weight=1.2, tip=0.5, f=F_DRAW)
    ry = fy1 - 41.5
    out += _emit([_seg((TYPE_L, ry), (fx1, ry))], BLACK, f=F_FINE)
    out += _text("a convolutional network / both passes, one set of rings",
                 TYPE_L, ry - 6.0, 2.3, BLACK)

    # measured off the masks this run built — not asserted
    conv = [b for b in bands if b.st.kind == "conv"]
    nc = sum(b.on.size for b in bands if b.st.kind != "input")
    no = sum(int(b.on.sum()) for b in bands if b.st.kind != "input")
    lit = sum(int(b.on.sum()) for b in conv)
    back = sum(int((b.on & b.alive).sum()) for b in conv)
    for i, (k, v) in enumerate((
            ("paper the gate leaves blank", "%d %%" % round(100 - 100 * no / nc)),
            ("of what fired, gradient re-enters", "%d %%" % round(100 * back / lit)),
            ("ring pitch", "%.2f mm" % pitch))):
        yy = ry + 4.0 + (2 - i) * 5.4
        out += _text(v, fx1 - _text_width(v, 2.3), yy, 2.3, BLACK)
        kw = _text_width(k, 2.3)
        out += _text(k, fx1 - 20.0 - kw, yy, 2.3, BLACK)

    # ---- the stage table.  Read it rim to core; that is the forward pass. --
    ty = rowy(1.72)
    out += _text("rim", TYPE_L, ty + 6.4, 2.1, BLACK)
    out += _text("core", TYPE_L + 84.0, ty + 6.4, 2.1, BLACK)
    out += _emit([_seg((TYPE_L + 11.0, ty + 7.1), (TYPE_L + 82.0, ty + 7.1))],
                 BLACK, f=F_FINE)
    out += _emit([[(TYPE_L + 79.0, ty + 8.4), (TYPE_L + 82.0, ty + 7.1),
                   (TYPE_L + 79.0, ty + 5.8)]], BLACK, f=F_FINE)
    out += _emit([_seg((TYPE_L, ty + 3.6), (TYPE_L + TYPE_W, ty + 3.6))],
                 BLACK, f=F_FINE)
    out += _text("cells", TYPE_L + 66.0, ty + 0.6, 2.05, BLACK)
    out += _text("channels", TYPE_L + 93.0, ty + 0.6, 2.05, BLACK)
    step = 7.0
    for i, b in enumerate(bands):
        yy = ty - 3.6 - i * step
        out += _text(b.st.label, TYPE_L, yy, 2.45, BLACK)
        out += _text(b.st.shape, TYPE_L + 13.5, yy, 2.45, BLACK)
        out += _text(b.st.note, TYPE_L + 39.0, yy, 2.45, BLACK)
        # THE TRADE, drawn twice at one fixed pitch: the left comb is the
        # cells the corridor holds (16 16 8 8 4) and it HALVES down the
        # column; the right comb is one tick per channel and it DOUBLES.
        # Same pitch, opposite staircases — that is the whole mechanism.
        for j in range(b.st.n // 16):
            px = TYPE_L + 66.0 + j * 1.5
            out += _emit([_seg((px, yy - 0.4), (px, yy + 3.0))], BLACK, f=F_FINE)
        for c in range(b.st.c):
            px = TYPE_L + 93.0 + c * 1.5
            out += _emit([_seg((px, yy - 0.4), (px, yy + 3.0))], BLACK, f=F_FINE)
    yy = ty - 3.6 - 5 * step
    out += _text("z", TYPE_L, yy, 2.45, BLACK)
    out += _text("9", TYPE_L + 13.5, yy, 2.45, BLACK)
    out += _text("softmax  /  L", TYPE_L + 40.0, yy, 2.45, BLACK)
    out += _emit([_seg((TYPE_L, yy - 3.4), (TYPE_L + TYPE_W, yy - 3.4))],
                 BLACK, f=F_FINE)

    # ---- the caption.  It confirms; it does not explain. -------------------
    cy0 = rowy(3.95)
    for i, ln in enumerate([
        "rings are layers. inward is the forward pass,",
        "outward the gradient. every pool halves the angular",
        "cells and doubles the channels: resolution traded for",
        "depth until the whole field is one number.",
        "blank paper is relu, and it is blank on BOTH passes.",
        "pooling keeps one cell per window, so the return can",
        "re-enter only the cells the outbound remembered.",
    ]):
        out += _text(ln, TYPE_L, cy0 - i * 5.3, 2.3, BLACK)
    base = cy0 - 7 * 5.3 - 0.6
    out += _emit([_seg((TYPE_L, base), (TYPE_L + TYPE_W, base))], BLACK, f=F_FINE)
    out += _text("the corridor:  out %d mm   back %d mm   %d%% (median angle)"
                 % (round(l_out), round(l_back),
                    round(100.0 * l_back / max(l_out, 1e-6))),
                 TYPE_L, base - 6.4, 2.5, RED)

    out += _legend_gate(bands, TYPE_L, rowy(5.42), TYPE_W)
    out += _legend_pool(TYPE_L, rowy(6.25), TYPE_W)

    fy = fy0 + 8.5
    out += _emit([_seg((TYPE_L, fy + 4.4), (TYPE_L + TYPE_W, fy + 4.4))],
                 BLACK, f=F_FINE)
    out += _text("3 pens   seeded   a3 landscape", TYPE_L, fy, 2.15, BLACK)
    out += _text("C N N", TYPE_L + TYPE_W - _text_width("C N N", 2.5), fy,
                 2.5, BLACK)
    return out


def _legend_gate(bands, x, y, w) -> List[GCodeCommand]:
    """The response that gates the rings, unrolled onto a straight line.
    Positive lobes inked, negative lobes blank paper — the key to every wedge,
    and the one place on the sheet where the gate is seen side-on."""
    out: List[GCodeCommand] = []
    b = bands[1]
    prof = b.on.any(axis=0)
    n, amp, ww = b.st.n, 5.0, w * 0.70
    out += _emit([_seg((x, y), (x + ww, y))], BLACK, f=F_FINE)
    z = b.act[min(1, b.st.c - 1)]
    hi = max(float(np.max(z)), 1e-6)
    lobes, cur = [], []
    for k in range(n + 1):
        kk = k % n
        px = x + ww * k / n
        if prof[kk]:
            cur.append((px, y + amp * float(z[kk]) / hi))
        else:
            if len(cur) >= 2:
                lobes.append(cur)
            cur = []
    if len(cur) >= 2:
        lobes.append(cur)
    out += _emit(lobes, BLACK, f=F_DRAW)
    for s, e in _runs_from_mask(list(~prof)):
        ax = x + ww * (s % n) / n
        bx = x + ww * min(n, e) / n
        if bx - ax >= 0.6:
            out += _emit([_seg((ax, y - 2.0), (bx, y - 2.0))], RED, f=F_FINE)
    out += _text("relu  y = max(0, x)      crimson = the closed wedges",
                 x, y - 6.4, 2.15, BLACK)
    return out


def _legend_pool(x, y, w) -> List[GCodeCommand]:
    """16 cells -> 8 forward; 8 -> 16 backward with half of them left blank."""
    out: List[GCodeCommand] = []
    span, h = w * 0.285, 3.2
    for xx, n in ((x, 16), (x + span * 1.38, 8)):
        for k in range(n + 1):
            px = xx + span * k / n
            out += _emit([_seg((px, y), (px, y + h))], BLACK, f=F_FINE)
        out += _emit([_seg((xx, y), (xx + span, y))], BLACK, f=F_FINE)
    ax = x + span + 2.2
    out += _emit([_seg((ax, y + h * 0.5), (ax + span * 0.3, y + h * 0.5))],
                 BLACK, f=F_FINE)
    yb = y - 6.8
    keep = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1]
    for k in range(9):
        px = x + span * k / 8
        out += _emit([_seg((px, yb), (px, yb + h))], RED, f=F_FINE)
    out += _emit([_seg((x, yb), (x + span, yb))], RED, f=F_FINE)
    xx = x + span * 1.38
    for k in range(16):
        if keep[k]:
            px = xx + span * k / 16
            out += _emit([_seg((px, yb), (px, yb + h))], RED, f=F_FINE)
    out += _emit([_seg((xx, yb), (xx + span, yb))], RED, f=F_FINE)
    out += _emit([_seg((ax + span * 0.3, yb + h * 0.5), (ax, yb + h * 0.5))],
                 RED, f=F_FINE)
    out += _text("max pool 2            unpool: one cell per window",
                 x, yb - 4.2, 2.15, BLACK)
    return out
