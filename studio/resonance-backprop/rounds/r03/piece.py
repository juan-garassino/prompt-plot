"""ATTENTION AS RESONANCE — GRADIENT AS PHASE (resonance-backprop r03).

Thesis ``gradient-as-phase`` (mechanism).  One hero field, and the backward
pass drawn INSIDE it, as a phase.  Every array on this sheet is computed in
this file; nothing is traced and nothing is invented.

The model (a real, if small, attention head — every step exact)
-----------------------------------------------------------------
Two coherent sources, Q and K, a whole number of wavelengths apart
(d = N * lam, the family's construction).  A token at position x receives
the query and the key as unit phasors rotated by path length — rotary position
encoding, with position = distance from the source:

    q(x) = exp(i (k |x - Q| + phi_Q))      k(x) = exp(i (k |x - K| + phi_K))

    score        s(x)  = beta * Re(q conj k) = beta * cos(psi),
                 psi   = k (|x-Q| - |x-K|) + phi_Q - phi_K     (interference)
    attention    A     = softmax over every token of s
    values       V(x)  = w_i(x) * u_i       (three token patches; u_i is a
                                             wave packet of the same carrier,
                                             phases 0, 120, 240 degrees)
    output       Z     = sum_x A(x) V(x)    (a packet: the attention-weighted
                                             mixture of u_1, u_2, u_3)
    loss         Loss  = 1/2 || Z - u_1 ||^2          (the answer is V1)

Backward, exactly (autograd-equivalent, checked by central differences):

    dLoss/dZ     = Z - u_1
    dLoss/dA(x)  = < Z - u_1, V(x) >
    g(x)         = dLoss/ds(x) = A(x) (dLoss/dA(x) - sum_y A(y) dLoss/dA(y))
    dLoss/dq(x)  = beta * g(x) * k(x)          <- the KEY's wave
    dLoss/dk(x)  = beta * g(x) * q(x)          <- the QUERY's wave

So the gradient that arrives at the query is the key's own wave scaled by
the real number beta*g(x); and a real factor can only do two things to a
phase: nothing (g > 0) or HALF A WAVELENGTH (g < 0).  That is the plate:

* black      — the forward crests: |x - Q| = m lam and |x - K| = m lam.
* crimson    — dLoss/dQ: crests of the key's wave, drawn ON the black K crests
               where g > 0 (the colour takes the crest over) and exactly half
               a wavelength off them where g < 0 (a second family interleaves).
* blue       — dLoss/dK: the same on the query's rings.
* goldenrod  — the value packets u_i in the three token patches.
* green      — Z and dLoss/dZ, the output and the residual, same carrier.

The coloured crests are drawn only where |g| >= GATE * max|g| — the gradient
is literally absent where the softmax is dark, so the stitches break along the
dark fringes.  The patch the loss wants (V1) gets g < 0 and interleaves; the
patches it wants less of (V2, V3) get g > 0 and are recoloured.

The two crest families are drawn together only where they cross at >= 25
degrees (the family's _Guard angle).  The locus of a constant crossing angle is
a circle through both sources, so the moire is bounded by exact circular arcs;
outside them only the nearer source's rings are drawn.  No dashes, no thinning.

Lineage: Bridget Riley, *Current* (1964) — one line family whose phase drift
makes the surface.  Here the drift is the gradient.

Entry point: ``gradient_as_phase``.  Deterministic (no randomness is used; the
``rng`` argument is kept for the contract).
"""

from __future__ import annotations

import math
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, Union, clip
from promptplot.generative.generators import _GLYPHS, _glyph_advance, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# Pen slots in STREAM order, light -> dark (the render palette below).  The
# family grammar is by COLOUR: Q crimson, K blue, V goldenrod, Z green, black.
OCHRE, BLUE, GREEN, RED, BLACK = 0, 1, 2, 3, 4
PALETTE = "goldenrod,dodgerblue,forestgreen,crimson,black"

PEN_MM = 0.35            # the nib the plate is drawn for (0.3-0.4 mm fineliner)
DOT_PITCH = 1.0          # family dotted pitch: round dots, 1.0 mm centre to centre
HALO_PAD = 0.9           # mm of clear paper around every label / window

# ---------------------------------------------------------------------------
# the design frame: 190 x 277 mm (the A4 portrait drawable), mapped uniformly
# ---------------------------------------------------------------------------
FW, FH = 190.0, 277.0

LAM = 3.0                # wavelength (crest pitch) in mm
N_LAM = 10               # source separation in wavelengths: d = N * lam
D_SRC = N_LAM * LAM      # 30 mm
CX, CY = 99.7, 140.0     # field edges land on the type grid x = 14 and x = 186    # field centre (design frame)
R_FIELD = 72.0           # each source radiates rings out to this radius
AX_ANG = math.radians(-24.0)   # the source axis: Q upper-left, K lower-right
_UX, _UY = math.cos(AX_ANG), math.sin(AX_ANG)


def axis_pt(a: float, b: float) -> Tuple[float, float]:
    """(along the Q->K axis, across it) from the field centre -> design mm."""
    return (CX + a * _UX - b * _UY, CY + a * _UY + b * _UX)


Q_SRC = axis_pt(-D_SRC / 2.0, 0.0)
K_SRC = axis_pt(+D_SRC / 2.0, 0.0)
PHI_Q = 0.0
PHI_K = 0.0

BETA = 1.0               # softmax inverse temperature
TOK_H = 0.25             # token lattice pitch (mm)
CROSS_MIN = 25.0         # the moire is drawn where the families cross at >= this
STEP_ETA = 1000.0
COLO_Y = 26.0
QK_YQ = 236.0
QK_YK = 44.0
QK_XQ = 40.0
QK_XK = 150.0
ROW_Y = (46.0, 32.0, 18.0)
MIN_RUN = 2.5            # a crest run shorter than this (mm) is a crumb: dropped
GATE = 0.06              # draw a gradient crest where |g| >= GATE * max|g|

# token patches: (centre, flat-top radius, value phase)
PATCHES = [
    (axis_pt(8.0, 40.0), 17.0, 0.0),                     # V1 — the answer
    (axis_pt(-12.0, -38.0), 14.0, 2.0 * math.pi / 3),    # V2
    (axis_pt(26.0, -36.0), 11.0, 4.0 * math.pi / 3),     # V3
]
U_SIGMA = 4.0            # value packet envelope (mm)
U_SPAN = 13.0            # value packet drawn over +-U_SPAN


class Stroke(NamedTuple):
    pts: List[Pt]
    pen: Optional[int]
    kind: str            # "type" | "line" | "dot" | "crest"
    f: int


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# THE MECHANISM — every number the plate draws comes from here
# ---------------------------------------------------------------------------


def _patch_w(x: np.ndarray, y: np.ndarray, i: int) -> np.ndarray:
    (px, py), rp, _ = PATCHES[i]
    rho = np.hypot(x - px, y - py)
    return np.where(rho <= 1.25 * rp, np.exp(-((rho / rp) ** 8)), 0.0)


def _psi(x, y, phi_q=PHI_Q, phi_k=PHI_K):
    k = 2 * math.pi / LAM
    return k * (np.hypot(x - Q_SRC[0], y - Q_SRC[1]) - np.hypot(x - K_SRC[0], y - K_SRC[1])) \
        + phi_q - phi_k


class Head:
    """The attention head, forward and backward, on the token lattice."""

    def __init__(self) -> None:
        xs, ys, ps = [], [], []
        for i, ((px, py), rp, _) in enumerate(PATCHES):
            g = np.arange(-1.25 * rp, 1.25 * rp + 1e-9, TOK_H)
            X, Y = np.meshgrid(px + g, py + g)
            m = np.hypot(X - px, Y - py) <= 1.25 * rp
            xs.append(X[m]); ys.append(Y[m]); ps.append(np.full(int(m.sum()), i))
        self.x = np.concatenate(xs)
        self.y = np.concatenate(ys)
        self.p = np.concatenate(ps)
        self.w = np.choose(self.p, [_patch_w(self.x, self.y, i) for i in range(len(PATCHES))])
        # value packets on a sample axis t (mm), same carrier as the field
        self.t = np.linspace(-3.4 * U_SIGMA, 3.4 * U_SIGMA, 1601)
        self.dt = float(self.t[1] - self.t[0])
        self.U = np.stack([self.packet(ph) for _, _, ph in PATCHES])
        self.forward()

    def packet(self, phase: float, t: Optional[np.ndarray] = None) -> np.ndarray:
        t = self.t if t is None else t
        return np.exp(-t ** 2 / (2 * U_SIGMA ** 2)) * np.cos(2 * math.pi * t / LAM + phase)

    # -- forward -----------------------------------------------------------
    def scores(self, dq=None, dk=None):
        """s(x) for per-token phase perturbations dq, dk (for the FD check)."""
        k = 2 * math.pi / LAM
        tq = k * np.hypot(self.x - Q_SRC[0], self.y - Q_SRC[1]) + PHI_Q
        tk = k * np.hypot(self.x - K_SRC[0], self.y - K_SRC[1]) + PHI_K
        q = np.exp(1j * tq)
        kk = np.exp(1j * tk)
        if dq is not None:
            q = q + dq
        if dk is not None:
            kk = kk + dk
        return q, kk, BETA * np.real(q * np.conj(kk))

    def loss_of(self, s: np.ndarray) -> float:
        e = np.exp(s - s.max())
        A = e / e.sum()
        alpha = np.array([(A * self.w * (self.p == i)).sum() for i in range(len(PATCHES))])
        Z = alpha @ self.U
        return 0.5 * float(((Z - self.U[0]) ** 2).sum() * self.dt)

    def forward(self) -> None:
        self.q, self.k, self.s = self.scores()
        self.smax = float(self.s.max())
        e = np.exp(self.s - self.smax)
        self.zsum = float(e.sum())
        self.A = e / self.zsum
        n = len(PATCHES)
        self.alpha = np.array([(self.A * self.w * (self.p == i)).sum() for i in range(n)])
        self.Z = self.alpha @ self.U
        self.dZ = self.Z - self.U[0]
        self.loss = 0.5 * float((self.dZ ** 2).sum() * self.dt)
        # backward
        self.c = np.array([float((self.dZ * self.U[i]).sum() * self.dt) for i in range(n)])
        self.dA = self.w * self.c[self.p]
        self.abar = float((self.A * self.dA).sum())
        self.g = self.A * (self.dA - self.abar)
        self.dq = BETA * self.g * self.k          # dLoss/dq(x), complex
        self.dk = BETA * self.g * self.q          # dLoss/dk(x), complex
        self.gmax = float(np.abs(self.g).max())

    def g_at(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """g(x) evaluated off-lattice (the same closed form the lattice uses)."""
        A = np.exp(BETA * np.cos(_psi(x, y)) - self.smax) / self.zsum
        out = np.zeros_like(x, dtype=float)
        for i in range(len(PATCHES)):
            w = _patch_w(x, y, i)
            out += np.where(w > 0, A * (w * self.c[i] - self.abar), 0.0)
        return out

    # -- checks --------------------------------------------------------------
    def fd_check(self, n: int = 6, h: float = 1e-6) -> float:
        """Central differences on the real/imag parts of q and k at n tokens,
        against the analytic gradient.  Returns the worst relative error."""
        idx = np.argsort(-np.abs(self.g))[:n]
        worst = 0.0
        for j in idx:
            for which in ("q", "k"):
                for comp in (1.0, 1j):
                    pert = np.zeros_like(self.q)
                    pert[j] = comp * h
                    kw_p = {("dq" if which == "q" else "dk"): pert}
                    kw_m = {("dq" if which == "q" else "dk"): -pert}
                    lp = self.loss_of(self.scores(**kw_p)[2])
                    lm = self.loss_of(self.scores(**kw_m)[2])
                    num = (lp - lm) / (2 * h)
                    an = self.dq[j] if which == "q" else self.dk[j]
                    ana = an.real if comp == 1.0 else an.imag
                    worst = max(worst, abs(num - ana) / max(abs(ana), 1e-12))
        return worst

    def step_loss(self, eta: float) -> float:
        """Loss after ONE gradient-descent step on every token's q and k."""
        s = BETA * np.real((self.q - eta * self.dq) * np.conj(self.k - eta * self.dk))
        return self.loss_of(s)


# ---------------------------------------------------------------------------
# mark primitives (millimetres, sheet space)
# ---------------------------------------------------------------------------


class _Map:
    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.sc = min((x1 - x0) / FW, (y1 - y0) / FH)
        self.ox = x0 + ((x1 - x0) - FW * self.sc) / 2.0
        self.oy = y0 + ((y1 - y0) - FH * self.sc) / 2.0
        self.halos: List[Tuple[float, float, float, float]] = []
        self.frame = (x0, y0, x1, y1)

    def p(self, x: float, y: float) -> Pt:
        return (self.ox + x * self.sc, self.oy + y * self.sc)

    def s(self, v: float) -> float:
        return v * self.sc

    def halo_box(self, box, pad: float = HALO_PAD) -> None:
        x0, y0, x1, y1 = box
        self.halos.append((x0 - pad, y0 - pad, x1 + pad, y1 + pad))

    def halo(self, strokes: Sequence[Stroke], pad: float = HALO_PAD) -> None:
        xs = [x for st in strokes for x, _ in st.pts]
        ys = [y for st in strokes for _, y in st.pts]
        if xs:
            self.halo_box((min(xs), min(ys), max(xs), max(ys)), pad)


def _S(pts: Sequence[Pt], pen, kind: str = "line", f: int = 2000) -> List[Stroke]:
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    return [Stroke(list(pts), pen, kind, f)]


def _touch(cx: float, cy: float, pen, kind: str = "dot") -> List[Stroke]:
    """One round dot: the nib itself, a 0.06 mm touch (never a micro-dash)."""
    return _S([(cx - 0.03, cy), (cx + 0.03, cy)], pen, kind, 1200)


def _disc(cx: float, cy: float, r: float, pen, kind: str = "dot") -> List[Stroke]:
    """A solid round disc of radius r for a PEN_MM nib, one pen-down."""
    h = PEN_MM / 2.0
    if r <= h + 0.08:
        return _touch(cx, cy, pen, kind)
    turns = max(2, int(math.ceil((r - h) / 0.25)) + 1)
    n = turns * 24
    pts = []
    for j in range(n + 1):
        t = j / n
        rr = (r - h) * (1.0 - t)
        a = 2 * math.pi * turns * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _S(pts, pen, kind, 1600)


def _circle(cx: float, cy: float, r: float, pen, n: int = 0, kind: str = "line") -> List[Stroke]:
    n = n or max(24, int(2 * math.pi * r / 0.5))
    return _S([(cx + r * math.cos(2 * math.pi * j / n), cy + r * math.sin(2 * math.pi * j / n))
               for j in range(n + 1)], pen, kind, 2000)


def _cum(pts: Sequence[Pt]) -> List[float]:
    c = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        c.append(c[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return c


def _at(pts, cum, s: float) -> Pt:
    lo, hi = 0, len(cum) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cum[mid] <= s:
            lo = mid
        else:
            hi = mid
    seg = cum[hi] - cum[lo]
    t = 0.0 if seg < 1e-12 else (s - cum[lo]) / seg
    a, b = pts[lo], pts[hi]
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _dotted(pts: Sequence[Pt], pen, pitch: float = DOT_PITCH) -> List[Stroke]:
    """A CONTINUOUS dotted line (Juan, 2026-09-28): one round touch-dot every
    ``pitch`` mm, END-ANCHORED — n = round(len / pitch) intervals, dots at
    k * len / n for k = 0..n, so both ends carry a dot and the pitch never
    drifts by more than pitch / (2 n)."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    cum = _cum(pts)
    L = cum[-1]
    if L < 1e-6:
        return _touch(*pts[0], pen)
    n = max(1, int(round(L / pitch)))
    out: List[Stroke] = []
    for j in range(n + 1):
        out += _touch(*_at(pts, cum, L * j / n), pen)
    return out


# ---------------------------------------------------------------------------
# type — the shared stroke font (it carries lowercase, subscripts, the partial
# sign and the double bar), proportional advances, weight fused to one pen-down
# ---------------------------------------------------------------------------


def _weighted(pts: List[Pt], w: float) -> List[Pt]:
    if w <= 0:
        return pts
    n = max(1, int(math.ceil(w / 0.26)))
    offs = [(w * j / n, 0.0) for j in range(n + 1)]
    path: List[Pt] = []
    for i, (ox, oy) in enumerate(offs):
        seq = [(x + ox, y + oy) for x, y in pts]
        path += seq if i % 2 == 0 else seq[::-1]
    return path


def _adv(ch: str, track: float) -> float:
    return _glyph_advance(ch) * track


def text_width(text: str, h: float, track: float = 1.0) -> float:
    return sum(_adv(c, track) for c in text) * (h / 6.0)


def type_run(M: _Map, text: str, x: float, y: float, h: float, pen, track: float = 1.0,
             weight: float = 0.0, align: str = "left", halo: bool = True,
             sub: Optional[Dict[int, float]] = None) -> List[Stroke]:
    """Single-stroke type, (x, y) = baseline anchor in the DESIGN frame (mm).
    ``sub`` maps a character index to a scale for subscripts (drawn lowered)."""
    sub = sub or {}
    sc_des = h / 6.0
    widths = []
    for i, ch in enumerate(text):
        f = sub.get(i, 1.0)
        widths.append(_adv(ch, track) * sc_des * f)
    tw = sum(widths)
    if align == "center":
        x -= tw / 2.0
    elif align == "right":
        x -= tw
    out: List[Stroke] = []
    cx = x
    for i, ch in enumerate(text):
        f = sub.get(i, 1.0)
        sc = sc_des * f
        dy = -0.35 * h if f < 1.0 else 0.0
        for st in _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []:
            pts = [M.p(cx + gx * sc, y + dy + gy * sc) for gx, gy in st]
            out += _S(_weighted(pts, M.s(weight)), pen, "type", 2200)
        cx += widths[i]
    if halo:
        M.halo(out)
    return out


# ---------------------------------------------------------------------------
# the wave packet (carrier = the field's wavelength)
# ---------------------------------------------------------------------------


def packet_curve(M: _Map, x0: float, y0: float, t: np.ndarray, v: np.ndarray, amp: float,
                 pen, rev: bool = False) -> List[Stroke]:
    """A packet drawn as ONE carrier stroke: (x0 + t, y0 + amp * v) in design mm."""
    pts = [M.p(x0 + float(a), y0 + amp * float(b)) for a, b in zip(t, v)]
    if rev:
        pts = pts[::-1]
    return _S(pts, pen, "pk", 2400)


def envelope(M: _Map, x0: float, y0: float, t: np.ndarray, e: np.ndarray, amp: float,
             pen, floor: float = 1.4) -> List[Stroke]:
    """The packet envelope as a continuous dotted line, only where it stands
    >= ``floor`` mm off the axis (upper run, then lower run back)."""
    out: List[Stroke] = []
    for sgn in (1.0, -1.0):
        run: List[Pt] = []
        for a, b in zip(t, e):
            if amp * b >= floor:
                run.append(M.p(x0 + float(a), y0 + sgn * amp * float(b)))
            elif run:
                out += _dotted(run, pen)
                run = []
        if run:
            out += _dotted(run, pen)
    return out


# ---------------------------------------------------------------------------
# THE FIELD — forward crests (black) and the gradient crests (crimson / blue)
# ---------------------------------------------------------------------------


def _arc_runs(cx: float, cy: float, r: float, keep, step: float = 0.22,
              min_run: float = 1.2) -> List[List[Pt]]:
    """Sample a circle and return the runs where keep(x, y) holds; each run's
    ends are refined by bisection so two complementary predicates meet
    EXACTLY (a crest that changes pen along its length has no gap, no overlap)."""
    n = max(48, int(2 * math.pi * r / step))
    th = np.linspace(0.0, 2 * math.pi, n + 1)
    xs = cx + r * np.cos(th)
    ys = cy + r * np.sin(th)
    m = keep(xs, ys)
    if m.all():
        return [list(zip(xs.tolist(), ys.tolist()))]
    if not m.any():
        return []

    def edge(a: float, b: float, ina: bool) -> float:
        for _ in range(18):
            c = 0.5 * (a + b)
            inc = bool(keep(np.array([cx + r * math.cos(c)]), np.array([cy + r * math.sin(c)]))[0])
            if inc == ina:
                a = c
            else:
                b = c
        return 0.5 * (a + b)

    # walk the circle from a False sample; angles are taken by POSITION in the
    # walk (monotone, never wrapping), so a bisection bracket is always one step
    k0 = int(np.argmin(m))
    dth = 2 * math.pi / n
    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    prev = False
    for step_i in range(1, n + 1):
        i = (k0 + step_i) % n
        a1 = th[k0] + step_i * dth
        a0 = a1 - dth
        mi = bool(m[i])
        if mi and not prev:
            e = edge(a0, a1, False)
            cur = [(cx + r * math.cos(e), cy + r * math.sin(e)), (float(xs[i]), float(ys[i]))]
        elif mi and prev:
            cur.append((float(xs[i]), float(ys[i])))
        elif prev and not mi:
            e = edge(a0, a1, True)
            cur.append((cx + r * math.cos(e), cy + r * math.sin(e)))
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
        prev = mi
    runs = [r_ for r_ in runs if sum(math.hypot(b[0] - a[0], b[1] - a[1])
                                     for a, b in zip(r_[:-1], r_[1:])) >= min_run]
    return runs


def _ang_interval(src, run: List[Pt]) -> Tuple[float, float]:
    """The angular interval (start, sweep) a run covers, walked CCW."""
    r = math.hypot(run[0][0] - src[0], run[0][1] - src[1])
    if sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(run[:-1], run[1:])) \
            > 2 * math.pi * r - 1e-3:
        return 0.0, 2 * math.pi                      # the whole ring
    a0 = math.atan2(run[0][1] - src[1], run[0][0] - src[0]) % (2 * math.pi)
    a1 = math.atan2(run[-1][1] - src[1], run[-1][0] - src[0]) % (2 * math.pi)
    return a0, (a1 - a0) % (2 * math.pi)


def _in_intervals(x, y, src, ivs) -> np.ndarray:
    out = np.zeros(np.shape(x), bool)
    if not ivs:
        return out
    th = np.arctan2(y - src[1], x - src[0]) % (2 * math.pi)
    for a0, sweep in ivs:
        out |= ((th - a0) % (2 * math.pi)) <= sweep
    return out


def _dist_to_family(x, y, src, off: float = 0.0):
    """Distance (mm) from each point to the nearest crest of a source's family
    r = (m - off) lam, and the family's radial unit vector there."""
    r = np.hypot(x - src[0], y - src[1])
    rr = r / LAM + off
    return np.abs(rr - np.round(rr)) * LAM


def field(M: _Map, H: Head, colors: int) -> List[Stroke]:
    """Black forward crests, crimson dLoss/dQ crests, blue dLoss/dK crests."""
    black, red, blue = _pen(BLACK, colors), _pen(RED, colors), _pen(BLUE, colors)
    gthr = GATE * H.gmax

    def gate_pos(x, y):
        g = H.g_at(x, y)
        return g >= gthr

    def gate_neg(x, y):
        g = H.g_at(x, y)
        return g <= -gthr

    def in_field(x, y):
        return (np.hypot(x - Q_SRC[0], y - Q_SRC[1]) <= R_FIELD + 1e-6) | \
               (np.hypot(x - K_SRC[0], y - K_SRC[1]) <= R_FIELD + 1e-6)

    # WHERE THE TWO FAMILIES MAY BOTH BE DRAWN.  Near the source axis the two
    # crest families run nearly parallel, and d = N lam puts them ON each
    # other there.  Rather than thinning them into dashes (r01's guard), the
    # moire is drawn only where the families cross at >= CROSS_MIN degrees.
    # The locus of a constant crossing angle is a circle through BOTH sources
    # (inscribed angle), so the boundary of the moire is two exact circular
    # arcs; beyond them only the NEARER source's rings are drawn.
    cmin = math.cos(math.radians(CROSS_MIN))

    def near_only(x, y, src_this, src_other):
        ax, ay = x - src_this[0], y - src_this[1]
        bx, by = x - src_other[0], y - src_other[1]
        ra = np.hypot(ax, ay) + 1e-9
        rb = np.hypot(bx, by) + 1e-9
        cosang = np.abs((ax * bx + ay * by) / (ra * rb))
        return (cosang > cmin) & (ra > rb)

    out: List[Stroke] = []
    n_ring = int(R_FIELD / LAM + 1e-9)
    for src, other, gpen in ((Q_SRC, K_SRC, blue), (K_SRC, Q_SRC, red)):
        # the gradient that lives on THIS source's rings is the OTHER tensor's:
        # dLoss/dK = beta g q  -> on Q's rings (blue); dLoss/dQ -> on K's (crimson)
        for m in range(1, n_ring + 1):
            r = m * LAM

            # g > 0: the gradient crest IS this crest — the colour takes it
            # over.  Runs shorter than MIN_RUN are crumbs and go back to black,
            # so the crest itself never breaks.
            def col_pos(x, y, src=src, other=other):
                return gate_pos(x, y) & ~near_only(x, y, src, other)

            def col_neg(x, y, src=src, other=other):
                return gate_neg(x, y) & ~near_only(x, y, src, other)

            taken = _arc_runs(src[0], src[1], r, col_pos, min_run=MIN_RUN)
            for run in taken:
                out += _S([M.p(*p) for p in run], gpen, "crest", 2000)
            ivs = [_ang_interval(src, run) for run in taken]

            def keep_black(x, y, src=src, other=other, ivs=ivs):
                return in_field(x, y) & ~_in_intervals(x, y, src, ivs) & \
                    ~near_only(x, y, src, other)

            for run in _arc_runs(src[0], src[1], r, keep_black):
                out += _S([M.p(*p) for p in run], black, "crest", 2000)
            # g < 0: half a wavelength off — a second family interleaves
            rh = r - LAM / 2.0
            if rh > LAM / 2.0 - 1e-9:
                for run in _arc_runs(src[0], src[1], rh, col_neg, min_run=MIN_RUN):
                    out += _S([M.p(*p) for p in run], gpen, "crest", 2000)
    # the two sources: small solid discs
    for s in (Q_SRC, K_SRC):
        out += _disc(*M.p(*s), 0.55, black, "dot")
    return out


# ---------------------------------------------------------------------------
# layout blocks
# ---------------------------------------------------------------------------


def value_windows(M: _Map, H: Head, colors: int) -> List[Stroke]:
    ochre = _pen(OCHRE, colors)
    out: List[Stroke] = []
    t = np.linspace(-U_SPAN, U_SPAN, 700)
    amp = 2.3
    for i, ((px, py), rp, ph) in enumerate(PATCHES):
        v = H.packet(ph, t)
        pk = packet_curve(M, px, py, t, v, amp, ochre)
        out += pk
        # the window: the packet's box, cleared of every crest
        x0, y0 = M.p(px - U_SPAN, py - amp)
        x1, y1 = M.p(px + U_SPAN, py + amp)
        M.halo_box((x0, y0, x1, y1), pad=1.1)
        lab = type_run(M, "V" + "₁₂₃"[i], px + U_SPAN + 1.6, py - 1.2, 3.0, ochre, )
        out += lab
    return out


def qk_packets(M: _Map, H: Head, colors: int) -> List[Stroke]:
    """The query and key as packets of the field's own carrier."""
    red, blue = _pen(RED, colors), _pen(BLUE, colors)
    out: List[Stroke] = []
    t = np.linspace(-20.0, 20.0, 900)
    for x, y, pen, name, ph, lx in ((QK_XQ, QK_YQ, red, "Q", PHI_Q, -27.0),
                                    (QK_XK, QK_YK, blue, "K", PHI_K, 23.0)):
        v = np.exp(-t ** 2 / (2 * 6.5 ** 2)) * np.cos(2 * math.pi * t / LAM + ph)
        out += packet_curve(M, x, y, t, v, 4.6, pen)
        out += envelope(M, x, y, t, np.exp(-t ** 2 / (2 * 6.5 ** 2)), 4.6, pen)
        out += type_run(M, name, x + lx, y - 3.0, 6.0, pen, weight=0.35)
    return out


def output_rows(M: _Map, H: Head, colors: int) -> List[Stroke]:
    """V1 (the answer), Z (the output) and dLoss/dZ (the residual): one carrier.
    dLoss/dZ = Z - V1 is V1 turned half a wavelength over, plus Z."""
    green, ochre = _pen(GREEN, colors), _pen(OCHRE, colors)
    out: List[Stroke] = []
    x0 = 58.0
    amp = 5.0
    rows = [
        (ROW_Y[0], H.Z, green, "Z = AV"),
        (ROW_Y[1], H.U[0], ochre, "V₁"),
        (ROW_Y[2], H.dZ, green, "∂L/∂Z"),
    ]
    for y, v, pen, name in rows:
        out += packet_curve(M, x0, y, H.t, v, amp, pen)
        out += type_run(M, name, 14.0, y - 1.2, 2.8, pen)
    return out


def titles(M: _Map, H: Head, colors: int) -> List[Stroke]:
    black = _pen(BLACK, colors)
    out: List[Stroke] = []
    out += type_run(M, "A T T E N T I O N   A S   R E S O N A N C E", 14.0, 264.0, 4.2, black,
                    track=1.0)
    out += type_run(M, "the backward pass is the same wave, half a wavelength over", 14.0, 256.0,
                    2.6, black, track=1.06)
    return out


def colophon(M: _Map, H: Head, colors: int) -> List[Stroke]:
    """The checkable numbers, set small at the foot (30 cm detail)."""
    black = _pen(BLACK, colors)
    lo = H.step_loss(STEP_ETA)
    lines = [
        "L = Σ (Z − V₁)² / 2    λ = %g mm   d = %d λ   β = %g   %d tokens" % (
            LAM, N_LAM, BETA, len(H.x)),
        "one step down the drawn gradient: L %.3f → %.3f" % (H.loss, lo),
    ]
    out: List[Stroke] = []
    for i, ln in enumerate(lines):
        out += type_run(M, ln, 186.0, COLO_Y - 4.6 * i, 2.3, black, align="right")
    return out


def frame(M: _Map, colors: int) -> List[Stroke]:
    black = _pen(BLACK, colors)
    out: List[Stroke] = []
    arm = 4.0
    for x, y in ((4.0, 271.0), (186.0, 271.0), (4.0, 6.0), (186.0, 6.0)):
        out += _S([M.p(x - arm, y), M.p(x + arm, y)], black)
        out += _S([M.p(x, y - arm), M.p(x, y + arm)], black)
    return out


# ---------------------------------------------------------------------------
# sheet passes: halos, ordering, emit
# ---------------------------------------------------------------------------


def _apply_halos(strokes: List[Stroke], M: _Map) -> List[Stroke]:
    boxes = M.halos
    out: List[Stroke] = []
    for st in strokes:
        if st.kind in ("type", "pk"):
            out.append(st)
            continue
        xs = [p[0] for p in st.pts]
        ys = [p[1] for p in st.pts]
        bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
        hit = [b for b in boxes if not (bx1 < b[0] or bx0 > b[2] or by1 < b[1] or by0 > b[3])]
        if not hit:
            out.append(st)
            continue
        if st.kind == "dot" or max(bx1 - bx0, by1 - by0) < 0.5:
            cx, cy = xs[0], ys[0]
            if any(b[0] <= cx <= b[2] and b[1] <= cy <= b[3] for b in hit):
                continue
            out.append(st)
            continue
        region = Union(*[Rect(*b) for b in hit])
        for run in clip(st.pts, region, keep="outside"):
            if sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(run[:-1], run[1:])) >= 0.4:
                out.append(Stroke(run, st.pen, st.kind, st.f))
    return out


def _order(strokes: List[Stroke]) -> List[Stroke]:
    """Per pen: greedy nearest-END walk with reversal, so the emitted order is
    a spatially continuous path (the post-processor's nearest-start pass
    cannot reverse a stroke, so it is given strokes already oriented)."""
    by_pen: Dict[Optional[int], List[Stroke]] = {}
    for st in strokes:
        by_pen.setdefault(st.pen, []).append(st)
    out: List[Stroke] = []
    for pen in sorted(by_pen, key=lambda p: (p is None, p)):
        rest = by_pen[pen]
        pts0 = np.array([s.pts[0] for s in rest])
        pts1 = np.array([s.pts[-1] for s in rest])
        alive = np.ones(len(rest), bool)
        pos = np.array([0.0, 0.0])
        for _ in range(len(rest)):
            d0 = np.hypot(*(pts0 - pos).T)
            d1 = np.hypot(*(pts1 - pos).T)
            d0[~alive] = np.inf
            d1[~alive] = np.inf
            i0, i1 = int(np.argmin(d0)), int(np.argmin(d1))
            if d0[i0] <= d1[i1]:
                st = rest[i0]
                alive[i0] = False
            else:
                st = rest[i1]
                alive[i1] = False
                st = Stroke(st.pts[::-1], st.pen, st.kind, st.f)
            out.append(st)
            pos = np.array(st.pts[-1])
    return out


def _emit(strokes: Sequence[Stroke]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for st in strokes:
        out += _poly(st.pts, color=st.pen, f=st.f)
    return out


_HEAD: Optional[Head] = None


def head() -> Head:
    global _HEAD
    if _HEAD is None:
        _HEAD = Head()
    return _HEAD


def build_strokes(bounds: Bounds, colors: int = 5) -> Tuple[List[Stroke], _Map]:
    M = _Map(bounds)
    H = head()
    s: List[Stroke] = []
    s += titles(M, H, colors)
    s += qk_packets(M, H, colors)
    s += value_windows(M, H, colors)
    s += output_rows(M, H, colors)
    s += field(M, H, colors)
    s += frame(M, colors)
    s += colophon(M, H, colors)
    s = _apply_halos(s, M)
    return _order(s), M


def gradient_as_phase(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    strokes, _ = build_strokes(bounds, colors)
    return _emit(strokes)


if __name__ == "__main__":  # the checkable statistics quoted in NOTES.md
    H = head()
    print("tokens", len(H.x), "alpha", np.round(H.alpha, 4), "sum", round(float(H.alpha.sum()), 4))
    print("loss", round(H.loss, 5), "c", np.round(H.c, 4), "abar", round(H.abar, 5))
    print("g: max|g|", H.gmax, " patch signs", [
        (int((H.g[H.p == i] > 0).sum()), int((H.g[H.p == i] < 0).sum())) for i in range(3)])
    print("FD worst rel err", H.fd_check())
    for eta in (1e2, 1e3, 1e4):
        print("eta", eta, "loss after one step", H.step_loss(eta))
