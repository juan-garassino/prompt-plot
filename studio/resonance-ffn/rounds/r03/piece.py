"""ATTENTION AS RESONANCE (FFN) — r03 · "two interferences" (mechanism) · parent r01.

The plate is built on the rhyme r01 found: the hero interference figure on top
and its 0.39-scale gradient twin below, the ONLY two figures, joined by ONE
feed-forward fan.  A horizontal spine through the fan is the sheet's mirror:
everything above it is the FORWARD pass, everything below it is the BACKWARD
pass, and each forward element has its transformed image below.

    above the spine (forward)            below the spine (backward)
    Q, K rows feeding the hero sources   dL/dQ, dL/dK rows feeding the twin
    the hero field  A                    the twin field  dL/dA   (0.39 scale)
    V rows (a_j v_j) summing into Z      dL/dZ
    fan top: tanh(h_k s)                 fan bottom: g_k s sech^2(h_k s)
                       the right node Y is the loss, where the pass turns

Every number on the sheet is a REAL computed array (``_model``): a 4-token,
d=8 single-head attention step followed by a tanh FFN (d_ff = 12) with a
residual, a squared-error loss, and the exact backward pass.  All randomness
is drawn from the passed ``SeededRNG``, so a new seed is a new (still exact)
forward/backward computation.

The mappings, one line each
---------------------------
* ROW (Q, K, V, Z and every gradient row): the vector is ONE wave packet —
  dimension i rides harmonic F0 + i*DF under a shared Gaussian envelope, with
  Lowdin-orthonormalised coefficients (``_whiten``), so the overlap integral
  of two drawn rows equals the dot product of the two vectors EXACTLY:
  ``q . k`` IS the resonance of the Q and K packets.
* V rows are drawn at a_j * v_j (the softmax weight times the value), on the
  same mm-per-unit as Z, so the green Z row is literally their sum.
* HERO: two-source Huygens crest loci r_s = m L (the approved construction),
  d = 54 L.  The right source lags by phi = angle(q, k*) (sub-millimetre:
  (phi/2pi) L <= 0.6 mm of ring radius).
* TWIN: the same object at 0.39 scale, placed by the homothety through the
  fan's left node with ratio -0.39 (reflected across the spine and shrunk),
  fed by dL/dq and dL/dk*; its phase lag is the angle between those two.
* FAN: along the fan the unit's input is ramped 0 -> h_k -> 0 by s(u).
  Above: tanh(h_k s)  (|.|, one line per hidden unit; units the pen cannot
  part, < 0.9 mm everywhere, are drawn as one line).
  Below: |dL/da_k| * s * sech^2(h_k s) = the derivative of the line above
  w.r.t. h_k times the upstream gradient (profile exact, per-unit height
  square-root compressed).  s(u) = sin(pi u)^2.  Saturated
  units fuse at the flat top above and cut a notch below: the twin peaks are
  not drawn, they fall out of sech^2.

Lineage: Charles Csuri & James Shaffer, *Sine Curve Man* (1967) — a form and
its function-mapped copy on one plotter sheet; the function is the content.

Pens, in STREAM order (light -> dark): 0 goldenrod V · 1 dodgerblue K, dL/dK ·
2 forestgreen Z, dL/dZ · 3 crimson Q, dL/dQ · 4 darkviolet FFN fan, Y, dL/dY ·
5 black hero, twin, droplines, title.

Entry point: ``two_interferences``.
"""

from __future__ import annotations

import math
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, Union, clip
from promptplot.generative.engine.kit import _GLYPHS, _glyph_advance, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# Pen slots in STREAM order (light -> dark).  Family grammar is by colour.
OCHRE, BLUE, GREEN, RED, PURPLE, BLACK = 0, 1, 2, 3, 4, 5
PALETTE = "goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black"

PEN_MM = 0.35            # nib the plate is drawn for (0.3-0.4 mm fineliner)

# THE DOT (Juan 2026-09-28: "more continuous dots").  One round dot, one size,
# one pitch, family-wide: a closed loop of radius DOT_R (inks ~0.6 mm under a
# 0.35 nib), centre-to-centre DOT_PITCH, end-anchored so both ends carry a dot.
DOT_PITCH = 1.0
DOT_R = 0.12

MIN_RUN = 9.0            # mm: shortest streamline fragment worth a pen cycle
HALO_PAD = 1.0           # mm of clear paper around every label

# ---------------------------------------------------------------------------
# design space: the A4-portrait drawable, 190 x 277 mm, origin lower-left.
# ``_emit`` fits it uniformly into whatever bounds the caller passes.
# ---------------------------------------------------------------------------
DW, DH = 190.0, 277.0

AX = 84.0                # the plate's vertical axis: hero, fan node, twin
HERO_Y = 188.0
HERO_D = 66.0            # source separation (mm)
HERO_N = 54              # d = 54 L  ->  L = 1.222 mm crest pitch
TWIN_SCALE = 0.39
SPINE_Y = 92.0
FAN_X1 = 181.0           # the Y / loss node
FAN_UP = 30.0            # forward half height (mm)
FAN_DN = 26.0            # backward half height (mm)

TOP_REG_Y = 244.0        # Q | K rows
ROW_LEN = 46.0

# The backward figure is the forward one under the homothety through the fan's
# left node with ratio -TWIN_SCALE: reflected across the spine AND shrunk.
TWIN_Y = SPINE_Y - TWIN_SCALE * (HERO_Y - SPINE_Y)          # dL/dA centre
BOT_REG_Y = SPINE_Y - TWIN_SCALE * (TOP_REG_Y - SPINE_Y)     # dL/dQ | dL/dK rows


class Stroke(NamedTuple):
    pts: List[Pt]
    pen: Optional[int]
    kind: str            # "type" | "line" | "dot"
    f: int


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# the real computation
# ---------------------------------------------------------------------------


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - x.max())
    return e / e.sum()


def _model(rng: SeededRNG, T: int = 4, d: int = 8, dff: int = 12) -> Dict[str, np.ndarray]:
    """One single-head attention step + tanh FFN + residual, forward AND backward.

    Everything the plate draws is read out of this dict."""
    g = rng.np
    X = g.standard_normal((T, d))
    Wq = g.standard_normal((d, d)) / math.sqrt(d)
    Wk = g.standard_normal((d, d)) / math.sqrt(d)
    Wv = g.standard_normal((d, d)) / math.sqrt(d)
    W1 = g.standard_normal((dff, d)) * (2.2 / math.sqrt(d))
    b1 = 0.3 * g.standard_normal(dff)
    W2 = g.standard_normal((d, dff)) / math.sqrt(dff)
    tgt = g.standard_normal(d)
    return _forward_backward(X, Wq, Wk, Wv, W1, b1, W2, tgt)


def _forward_backward(X, Wq, Wk, Wv, W1, b1, W2, tgt) -> Dict[str, np.ndarray]:
    d = X.shape[1]
    q = X[0] @ Wq
    K = X @ Wk
    V = X @ Wv
    s = K @ q / math.sqrt(d)
    a = _softmax(s)
    z = a @ V
    h = W1 @ z + b1
    act = np.tanh(h)
    y = W2 @ act + z
    loss = 0.5 * float(np.sum((y - tgt) ** 2))
    # ---- backward (exact) ----
    gy = y - tgt
    gact = W2.T @ gy
    gh = gact * (1.0 - act ** 2)
    gz = W1.T @ gh + gy
    ga = V @ gz
    gs = a * (ga - float(a @ ga))
    gq = (K.T @ gs) / math.sqrt(d)
    gK = np.outer(gs, q) / math.sqrt(d)
    j = int(np.argmax(a))
    return dict(q=q, K=K, V=V, s=s, a=a, z=z, h=h, act=act, y=y, loss=np.array(loss),
                gy=gy, gact=gact, gh=gh, gz=gz, ga=ga, gs=gs, gq=gq, gK=gK,
                j=np.array(j), k=K[j], gk=gK[j])


def _angle(u: np.ndarray, v: np.ndarray) -> float:
    c = float(u @ v) / (float(np.linalg.norm(u) * np.linalg.norm(v)) + 1e-12)
    return math.acos(max(-1.0, min(1.0, c)))


# ---------------------------------------------------------------------------
# stroke primitives (design mm)
# ---------------------------------------------------------------------------


def _S(pts: Sequence[Pt], pen, kind: str = "line", f: int = 2000) -> List[Stroke]:
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    return [Stroke(list(pts), pen, kind, f)]


def _disc(cx: float, cy: float, r: float, pen, kind: str = "line") -> List[Stroke]:
    """Solid round disc for a PEN_MM nib: one pen-down.  Spiral at 0.25 mm."""
    hh = PEN_MM / 2.0
    if r <= hh + 0.08:
        return _S([(cx - 0.03, cy), (cx + 0.03, cy)], pen, kind, 1200)
    rr0 = r - hh
    turns = max(2, int(math.ceil(rr0 / 0.25)) + 1)
    n = turns * 24
    pts = []
    for k in range(n + 1):
        t = k / n
        rr = rr0 * (1.0 - t)
        a = 2 * math.pi * turns * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _S(pts, pen, kind, 1600)


def _circle(cx: float, cy: float, r: float, pen, n: int = 40) -> List[Stroke]:
    return _S([(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
               for k in range(n + 1)], pen, "line", 2000)


def _the_dot(cx: float, cy: float, pen) -> Stroke:
    """THE dot: a closed loop of radius DOT_R, one pen-down, always the same."""
    return Stroke([(cx + DOT_R * math.cos(2 * math.pi * k / 8),
                    cy + DOT_R * math.sin(2 * math.pi * k / 8)) for k in range(9)],
                  pen, "dot", 1200)


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


def _dots(pts: Sequence[Pt], pen) -> List[Stroke]:
    """A dotted LINE: dots at a constant arclength pitch (the one family pitch,
    rounded so it divides the path exactly), END-ANCHORED so both ends carry a
    dot — no stubs, no bunching, no gap at either end."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    cum = _cum(pts)
    L = cum[-1]
    if L < 0.5:
        return [_the_dot(*pts[0], pen)]
    n = max(1, int(round(L / DOT_PITCH)))
    return [_the_dot(*_at(pts, cum, L * k / n), pen) for k in range(n + 1)]


def _bez(p0, c1, c2, p1, n: int = 80) -> List[Pt]:
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((u * u * u * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p1[0],
                    u * u * u * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p1[1]))
    return out


# ---------------------------------------------------------------------------
# type — the shared single-stroke font with proportional advances
# ---------------------------------------------------------------------------


class _Labels:
    def __init__(self) -> None:
        self.boxes: List[Tuple[float, float, float, float]] = []

    def halo(self, strokes: Sequence[Stroke], pad: float = HALO_PAD) -> None:
        xs = [x for st in strokes for x, _ in st.pts]
        ys = [y for st in strokes for _, y in st.pts]
        if xs:
            self.boxes.append((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))


def _glyph(ch: str):
    st = _GLYPHS.get(ch)
    if st is None:
        st = _GLYPHS.get(ch.upper(), [])
    return st


def _tw(text: str, cap: float, tracking: float = 1.0) -> float:
    return sum(_glyph_advance(c) for c in text) * (cap / 6.0) * tracking


def _weighted(pts: List[Pt], w: float) -> List[Pt]:
    """Offset passes chained into ONE pen-down, passes <= 0.28 mm apart."""
    if w <= 0:
        return pts
    n = max(1, int(math.ceil(w / 0.28)))
    m = max(1, int(math.ceil(0.9 * w / 0.28)))
    offs = [(w * k / n, 0.0) for k in range(n + 1)] + [(w * 0.5, 0.9 * w * j / m) for j in range(1, m + 1)]
    path: List[Pt] = []
    for i, (ox, oy) in enumerate(offs):
        seq = [(x + ox, y + oy) for x, y in pts]
        path += seq if i % 2 == 0 else seq[::-1]
    return path


def _type(LB: _Labels, text: str, x: float, y: float, cap: float, pen, tracking: float = 1.0,
          align: str = "left", weight: float = 0.0, halo: bool = True) -> List[Stroke]:
    """(x, y) is the baseline anchor; align left | center | right."""
    sc = cap / 6.0
    w = _tw(text, cap, tracking)
    cx = x - (w / 2.0 if align == "center" else w if align == "right" else 0.0)
    out: List[Stroke] = []
    for ch in text:
        for st in _glyph(ch):
            pts = [(cx + gx * sc, y + gy * sc) for gx, gy in st]
            out += _S(_weighted(pts, weight), pen, "type", 2200)
        cx += _glyph_advance(ch) * sc * tracking
    if halo:
        LB.halo(out)
    return out


def _frac(LB: _Labels, num: str, den: str, cx: float, ry: float, cap: float, pen,
          tracking: float = 1.05) -> List[Stroke]:
    """numerator / rule / denominator, centred on cx with the rule at ry."""
    half = max(_tw(num, cap, tracking), _tw(den, cap, tracking)) / 2.0 + 0.5
    out = _S([(cx - half, ry), (cx + half, ry)], pen, "type", 2000)
    gap = 0.55 * cap
    out += _type(LB, num, cx, ry + gap * 0.8, cap, pen, tracking, "center", halo=False)
    out += _type(LB, den, cx, ry - gap * 0.8 - cap, cap, pen, tracking, "center", halo=False)
    LB.halo(out)
    return out


# ---------------------------------------------------------------------------
# the ROW: a vector drawn as a train of wavelets, one per dimension
# ---------------------------------------------------------------------------


F0 = 0.19                # cycles / mm: dimension i rides harmonic F0 + i * DF
DF = 0.045
ENV_SIG = 8.7            # mm: the shared Gaussian envelope, the same for every row


def _basis(x: np.ndarray, d: int = 8) -> np.ndarray:
    """phi_i(x) = w(x) cos(2 pi (F0 + i DF) x), x measured from the row centre."""
    w = np.exp(-(x / ENV_SIG) ** 2 / 2.0)
    return np.stack([w * np.cos(2 * np.pi * (F0 + i * DF) * x) for i in range(d)])


_WHITEN: Dict[int, np.ndarray] = {}


def _whiten(d: int = 8) -> np.ndarray:
    """G^(-1/2) for the Gram matrix G_ij = integral phi_i phi_j (Lowdin).

    The harmonics are only NEAR-orthogonal under a Gaussian envelope (adjacent
    overlap 0.22), so a row is drawn with coefficients c = G^(-1/2) x.  Then
    integral f_a f_b = c_a^T G c_b = a . b EXACTLY: the overlap of two drawn
    rows IS the dot product of the two vectors."""
    if d not in _WHITEN:
        xs = np.linspace(-6 * ENV_SIG, 6 * ENV_SIG, 6001)
        B = _basis(xs, d)
        G = np.trapezoid(B[:, None, :] * B[None, :, :], xs, axis=2)
        ev, U = np.linalg.eigh(G)
        _WHITEN[d] = U @ np.diag(ev ** -0.5) @ U.T
    return _WHITEN[d]


def _row_values(xs: np.ndarray, comp: Sequence[float]) -> np.ndarray:
    comp = np.asarray(comp, dtype=float)
    c = _whiten(len(comp)) @ comp
    return c @ _basis(xs, len(comp))


def _row_curve(x0: float, x1: float, y: float, comp: Sequence[float], mm_per_unit: float
               ) -> List[Pt]:
    """A vector as ONE wave packet under the shared envelope (see _whiten)."""
    c = 0.5 * (x0 + x1)
    n = int((x1 - x0) / 0.18) + 1
    xs = np.linspace(x0, x1, n + 1)
    v = _row_values(xs - c, comp)
    return [(float(x), y + mm_per_unit * float(vv)) for x, vv in zip(xs, v)]


def _row_peak(comp: Sequence[float], L: float = 50.0) -> float:
    """max |packet| in units, for setting the mm-per-unit scales."""
    xs = np.linspace(-L / 2, L / 2, 801)
    return float(np.abs(_row_values(xs, comp)).max())


def _row(x0: float, x1: float, y: float, comp, mm_per_unit: float, pen,
         node: str = "right") -> List[Stroke]:
    """The carrier IS the axis: one stroke, node to node.  An open circle marks
    the node end that feeds a dropline; a solid disc the free end."""
    out = _S(_row_curve(x0, x1, y, comp, mm_per_unit), pen, "line", 2200)
    nx, fx = (x1, x0) if node == "right" else (x0, x1)
    out += _circle(nx, y, 0.95, pen, n=28)
    out += _disc(fx, y, 0.55, pen)
    return out


# ---------------------------------------------------------------------------
# the interference figure (the approved Huygens crest construction)
# ---------------------------------------------------------------------------


class _Guard:
    """Parallel-crowding guard (mm): reject a point only when another stroke is
    within ``sep`` AND within 25 degrees of parallel — crossings survive."""

    def __init__(self, sep: float = 0.82) -> None:
        self.sep = sep
        self.s2 = sep * sep
        self.g: dict = {}

    def ok(self, x: float, y: float, ux: float, uy: float, sid: int) -> bool:
        cx, cy = int(x / self.sep), int(y / self.sep)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for qx, qy, qu, qv, qs in self.g.get((cx + dx, cy + dy), ()):
                    if qs == sid or abs(ux * qu + uy * qv) < 0.906:
                        continue
                    if (qx - x) ** 2 + (qy - y) ** 2 < self.s2:
                        return False
        return True

    def add(self, x: float, y: float, ux: float, uy: float, sid: int) -> None:
        self.g.setdefault((int(x / self.sep), int(y / self.sep)), []).append((x, y, ux, uy, sid))


def _commit(run: Sequence[Pt], guard: _Guard, sid: int) -> None:
    for j, (x, y) in enumerate(run):
        qx, qy = run[min(j + 1, len(run) - 1)]
        px_, py_ = run[max(j - 1, 0)]
        du, dv = qx - px_, qy - py_
        dn = math.hypot(du, dv) or 1.0
        guard.add(x, y, du / dn, dv / dn, sid)


def _guarded_runs(pts: Sequence[Pt], guard: _Guard, sid: int, keep=None,
                  min_pts: int = 4, commit: bool = True) -> List[List[Pt]]:
    """Walk a polyline through the guard (pause-and-resume): points that crowd a
    parallel neighbour are dropped, the run resumes when it clears."""
    runs: List[List[Pt]] = []
    run: List[Pt] = []
    n = len(pts)
    for j, (x, y) in enumerate(pts):
        ok = keep is None or keep(x, y)
        if ok:
            qx, qy = pts[min(j + 1, n - 1)] if j < n - 1 else pts[j]
            px_, py_ = pts[j - 1] if j == n - 1 else (x, y)
            du, dv = qx - px_, qy - py_
            dn = math.hypot(du, dv) or 1.0
            du, dv = du / dn, dv / dn
            if guard.ok(x, y, du, dv, sid):
                if commit:
                    guard.add(x, y, du, dv, sid)
            else:
                ok = False
        if ok:
            run.append((x, y))
        else:
            if len(run) >= min_pts:
                runs.append(run)
            run = []
    if len(run) >= min_pts:
        runs.append(run)
    return runs


def _crest_field(cx: float, cy: float, d: float, n_lam: int, m_max: int, phase: float,
                 pen) -> List[Stroke]:
    """Crest loci r_1 = m L about the left source and r_2 = (m + phase/2pi) L
    about the right, clipped to the lens (a, b) = (0.87 d, 0.50 d), emitted
    interleaved by m so the two families share the central lens."""
    lam = d / n_lam
    sl, sr = cx - d / 2, cx + d / 2
    a_c, b_c = 0.872 * d, 0.50 * d
    guard = _Guard(0.82)

    def keep(x, y):
        return ((x - cx) / a_c) ** 2 + ((y - cy) / b_c) ** 2 <= 1.0

    out: List[Stroke] = []
    sid = 0
    for m in range(1, m_max + 1):
        for sx, shift in ((sl, 0.0), (sr, phase / (2 * math.pi))):
            r = (m + shift) * lam
            if r <= 0.3:
                continue
            n = max(48, int(2 * math.pi * r / 0.45))
            ring = [(sx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n))
                    for t in range(n + 1)]
            sid += 1
            for run in _guarded_runs(ring, guard, sid, keep):
                out += _S(run, pen, "line", 2600)
    for sx in (sl, sr):
        out += _disc(sx, cy, 0.9 * d / HERO_D + 0.35, pen)
    return out


# ---------------------------------------------------------------------------
# the FFN fan — one bundle, forward above the spine, its derivative below
# ---------------------------------------------------------------------------


RAMP_P = 2.0             # the ramp along the fan: s(u) = sin(pi u)^RAMP_P
MERGE_MM = 0.9           # units whose drawn lines never part by more than this are one line
FAN_STATS: Dict[str, object] = {}


def _ramp(u: float) -> float:
    return math.sin(math.pi * min(max(u, 0.0), 1.0)) ** RAMP_P


def _merge(profiles: List[List[float]], order: Sequence[int]) -> List[List[int]]:
    """Group units (in drawing order) whose drawn profiles stay within MERGE_MM
    of the group's first member everywhere: the pen cannot part them, so they
    are drawn as ONE line instead of a line and its guard-cut fragments."""
    groups: List[List[int]] = []
    for k in order:
        for g in groups:
            if max(abs(a - b) for a, b in zip(profiles[g[0]], profiles[k])) < MERGE_MM:
                g.append(k)
                break
        else:
            groups.append([k])
    return groups


def _fan(xa: float, xb: float, y: float, h: np.ndarray, gact: np.ndarray, pen) -> List[Stroke]:
    span = xb - xa
    steps = int(span / 0.35)
    us = [t / steps for t in range(steps + 1)]
    guard = _Guard(0.80)
    out: List[Stroke] = []
    LIFT = 0.5
    n = len(h)

    # the spine registers first so no streamline runs along it
    spine = [(xa + span * u, y) for u in us]
    for x, yy in spine:
        guard.add(x, yy, 1.0, 0.0, -1)
    out += _S(spine, pen, "line", 2200)

    # forward: |tanh(h_k s(u))|, heights exact up to one mm-per-unit
    ah = np.abs(h)
    fmax = float(np.tanh(ah.max()))
    fwd = [[FAN_UP / fmax * math.tanh(ah[k] * _ramp(u)) for u in us] for k in range(n)]
    g_f = _merge(fwd, [int(k) for k in np.argsort(-ah)])   # outermost first
    sid = 0
    for g in g_f:
        sid += 1
        k = g[0]
        pts = [(xa + span * u, y + o) if o >= LIFT else None for u, o in zip(us, fwd[k])]
        out += _stream(pts, guard, sid, pen)

    # backward: |dL/da_k| * s * sech^2(h_k s) — d/dh_k of the line above, times
    # the upstream gradient.  Profile exact; per-unit HEIGHT compressed by a
    # square root (monotone) so a saturated unit's twin peaks stay pen-sized.
    def bwd(k: int, u: float) -> float:
        s_ = _ramp(u)
        return abs(gact[k]) * s_ / math.cosh(h[k] * s_) ** 2

    raw = [[bwd(k, u) for u in us] for k in range(n)]
    peaks = [max(r) for r in raw]
    pmax = max(peaks)
    bk_ = [[FAN_DN * math.sqrt(peaks[k] / pmax) * v / peaks[k] for v in raw[k]] for k in range(n)]
    g_b = _merge(bk_, [int(k) for k in np.argsort(-np.array(peaks))])
    for g in g_b:
        sid += 1
        k = g[0]
        pts = [(xa + span * u, y - o) if o >= LIFT else None for u, o in zip(us, bk_[k])]
        out += _stream(pts, guard, sid, pen)

    mid = len(us) // 2
    FAN_STATS.update(
        forward_groups=g_f, backward_groups=g_b,
        twin_peaked=[k for k in range(n) if raw[k][mid] < 0.98 * peaks[k]],
        mid_fwd_mm=[round(fwd[k][mid], 2) for k in range(n)],
        mid_bwd_mm=[round(bk_[k][mid], 2) for k in range(n)],
    )
    return out


def _stream(pts: Sequence[Optional[Pt]], guard: _Guard, sid: int, pen) -> List[Stroke]:
    """One streamline: split where it dips under LIFT (a twin-peaked derivative
    line becomes its two humps), then walk each piece through the guard and
    keep every clear run of at least MIN_RUN — a unit the pen cannot part from its
    neighbour runs until it meets it and stops there (a saturated unit's two
    shoulders merge INTO the silhouette); pieces under MIN_RUN are dropped."""
    out: List[Stroke] = []
    seg: List[Pt] = []
    for p in list(pts) + [None]:
        if p is None:
            if len(seg) >= 4:
                for run in _guarded_runs(seg, guard, sid, commit=False):
                    if _length(run) >= MIN_RUN:
                        _commit(run, guard, sid)
                        out += _S(run, pen, "line", 2400)
            seg = []
        else:
            seg.append(p)
    return out


# ---------------------------------------------------------------------------
# the sheet
# ---------------------------------------------------------------------------


def build_strokes(rng: SeededRNG, colors: int = 6):
    Mx = _model(rng)
    LB = _Labels()
    oc, bl, gr, rd, pu, bk = (_pen(i, colors) for i in (OCHRE, BLUE, GREEN, RED, PURPLE, BLACK))
    s: List[Stroke] = []

    # ---------------- scales (mm per unit), one forward, one backward -------
    av = Mx["a"][:, None] * Mx["V"]
    # three mm-per-unit scales: Q|K share one (their overlap is the score),
    # V|Z share one (Z is literally the sum of the V rows), every gradient row
    # shares one (dL/dQ, dL/dK, dL/dZ are comparable to each other).
    fwd_amp = 6.0 / max(_row_peak(Mx["q"]), _row_peak(Mx["k"]))
    v_amp = min(6.0 / _row_peak(Mx["z"]), 2.9 / max(_row_peak(r) for r in av))
    bwd_amp = 6.0 / max(_row_peak(Mx["gq"]), _row_peak(Mx["gk"]), _row_peak(Mx["gz"]))
    Mx["scales"] = np.array([fwd_amp, v_amp, bwd_amp])

    # ---------------- HERO ---------------------------------------------------
    phi = _angle(Mx["q"], Mx["k"])
    hero_ml = int(round(0.8 * HERO_N))
    s += _crest_field(AX, HERO_Y, HERO_D, HERO_N, hero_ml, phi, bk)
    hsl, hsr = AX - HERO_D / 2, AX + HERO_D / 2
    hb = 0.5 * HERO_D

    # Q | K rows, top register, ending on the sources' verticals
    s += _row(hsl - ROW_LEN, hsl, TOP_REG_Y, Mx["q"], fwd_amp, rd, node="right")
    s += _row(hsr, hsr + ROW_LEN, TOP_REG_Y, Mx["k"], fwd_amp, bl, node="left")
    s += _dots([(hsl, TOP_REG_Y - 1.9), (hsl, HERO_Y + _lens_y(hsl - AX, HERO_D) + 1.6)], rd)
    s += _dots([(hsr, TOP_REG_Y - 1.9), (hsr, HERO_Y + _lens_y(hsr - AX, HERO_D) + 1.6)], bl)
    s += _type(LB, "Q", hsl - ROW_LEN, TOP_REG_Y + 8.6, 5.2, rd, weight=0.45)
    s += _type(LB, "K", hsr + ROW_LEN, TOP_REG_Y + 8.6, 5.2, bl, align="right", weight=0.45)

    # ---------------- TWIN ---------------------------------------------------
    td = HERO_D * TWIN_SCALE
    tn = int(round(HERO_N * TWIN_SCALE))
    tphi = _angle(Mx["gq"], Mx["gk"])
    s += _crest_field(AX, TWIN_Y, td, tn, int(round(0.8 * tn)), tphi, bk)
    tsl, tsr = AX - td / 2, AX + td / 2
    tlen = tsl - 19.0                     # left end on the left-arm column
    s += _row(tsl - tlen, tsl, BOT_REG_Y, Mx["gq"], bwd_amp, rd, node="right")
    s += _row(tsr, tsr + tlen, BOT_REG_Y, Mx["gk"], bwd_amp, bl, node="left")
    s += _dots([(tsl, BOT_REG_Y + 1.9), (tsl, TWIN_Y - _lens_y(tsl - AX, td) - 1.2)], rd)
    s += _dots([(tsr, BOT_REG_Y + 1.9), (tsr, TWIN_Y - _lens_y(tsr - AX, td) - 1.2)], bl)
    s += _frac(LB, "∂L", "∂Q", tsl - tlen - 6.2, BOT_REG_Y, 2.4, rd)
    s += _frac(LB, "∂L", "∂K", tsr + tlen + 6.2, BOT_REG_Y, 2.4, bl)

    # ---------------- the spine, the fan, the loss node ---------------------
    s += _fan(AX, FAN_X1, SPINE_Y, Mx["h"], Mx["gact"], pu)
    s += _disc(AX, SPINE_Y, 1.1, pu)
    s += _circle(FAN_X1, SPINE_Y, 1.3, pu, n=32)
    s += _disc(FAN_X1, SPINE_Y, 0.45, pu)
    s += _type(LB, "Y", FAN_X1 + 1.8, SPINE_Y + 3.2, 3.6, pu, weight=0.3)
    s += _frac(LB, "∂L", "∂Y", FAN_X1 + 4.6, SPINE_Y - 7.0, 2.4, pu)

    # the MIRROR: the spine continued to the left margin as a dotted horizon —
    # above it the forward pass, below it the backward pass
    s += _dots([(2.0, SPINE_Y), (AX - 2.6, SPINE_Y)], bk)

    # hero -> node (A, forward) and node -> twin (dL/dA, backward)
    s += _dots([(AX, HERO_Y - hb - 1.6), (AX, SPINE_Y + 2.8)], bk)
    s += _dots([(AX, SPINE_Y - 2.8), (AX, TWIN_Y + 0.5 * td + 1.4)], bk)

    # ---------------- Z, dL/dZ and the V rows (left arm) ---------------------
    zx0, zx1 = 19.0, AX - 16.0          # rows; their labels sit in the gutter left of x0
    zy, gzy = SPINE_Y + 10.0, SPINE_Y - 10.0
    s += _row(zx0, zx1, zy, Mx["z"], v_amp, gr, node="right")
    s += _row(zx0, zx1, gzy, Mx["gz"], bwd_amp, gr, node="right")
    # three dotted paths meet at the node: each ends >= 2 pitches from the others
    s += _dots(_bez((zx1 + 1.3, zy), (zx1 + 8.0, zy), (AX - 5.0, SPINE_Y + 4.5),
                    (AX - 2.0, SPINE_Y + 2.0)), gr)
    s += _dots(_bez((AX - 2.0, SPINE_Y - 2.0), (AX - 5.0, SPINE_Y - 4.5),
                    (zx1 + 8.0, gzy), (zx1 + 1.3, gzy)), gr)
    s += _type(LB, "Z", zx0 - 3.0, zy - 1.8, 3.6, gr, align="right", weight=0.3)
    s += _frac(LB, "∂L", "∂Z", zx0 - 6.2, gzy, 2.4, gr)

    T = av.shape[0]
    order = np.argsort(-Mx["a"])
    vy0 = zy + 12.0
    bus_x = zx1
    ys = []
    for r, j in enumerate(order):
        vy = vy0 + 6.4 * (T - 1 - r)
        ys.append(vy)
        s += _row(zx0, zx1, vy, av[j], v_amp, oc, node="right")
    # the addends gather into Z's node: one dotted bus, node to node
    ys = sorted(ys) + []
    stops = [zy] + ys
    for ya, yb in zip(stops[:-1], stops[1:]):
        s += _dots([(bus_x, ya + 1.35), (bus_x, yb - 1.35)], oc)
    s += _type(LB, "V", zx0 - 3.0, vy0 + 3.2 * (T - 1) - 1.8, 3.6, oc, align="right", weight=0.3)

    # ---------------- title ---------------------------------------------------
    s += _type(LB, "ATTENTION AS RESONANCE", DW - 2.0, 3.0, 3.2, bk, tracking=1.55, align="right",
                weight=0.18)

    return _apply_halos(s, LB), Mx


def _lens_y(dx: float, d: float) -> float:
    """Half-height of the clip lens at horizontal offset dx from its centre."""
    a, b = 0.872 * d, 0.5 * d
    t = 1.0 - (dx / a) ** 2
    return b * math.sqrt(max(t, 0.0))


def _length(pts: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def _apply_halos(strokes: List[Stroke], LB: _Labels) -> List[Stroke]:
    """Clip non-type ink OUT of every label box (exact Region clip); a dot that
    touches a box is dropped whole."""
    boxes = LB.boxes
    out: List[Stroke] = []
    for st in strokes:
        if st.kind == "type":
            out.append(st)
            continue
        xs = [p[0] for p in st.pts]
        ys = [p[1] for p in st.pts]
        bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
        hit = [b for b in boxes if not (bx1 < b[0] or bx0 > b[2] or by1 < b[1] or by0 > b[3])]
        if not hit:
            out.append(st)
            continue
        if st.kind == "dot" or max(bx1 - bx0, by1 - by0) < 3.0:
            continue
        region = Union(*[Rect(*b) for b in hit])
        for run in clip(st.pts, region, keep="outside"):
            if _length(run) >= 0.3:
                out.append(Stroke(run, st.pen, st.kind, st.f))
    return out


def _order(strokes: List[Stroke]) -> List[Stroke]:
    """Per pen, one clean layer: greedy nearest-neighbour from the top-left
    corner, a stroke may be drawn in either direction.  Consecutive strokes are
    therefore spatial neighbours, so any contiguous batch of a layer is local
    and no hop crosses the sheet unless the layer itself does."""
    by_pen: Dict[Optional[int], List[Stroke]] = {}
    for st in strokes:
        by_pen.setdefault(st.pen, []).append(st)
    out: List[Stroke] = []
    for pen in sorted(by_pen, key=lambda p: -1 if p is None else p):
        todo = by_pen[pen]
        cell = 6.0
        grid: Dict[Tuple[int, int], List[int]] = {}
        for i, st in enumerate(todo):
            for q in (st.pts[0], st.pts[-1]):
                grid.setdefault((int(q[0] // cell), int(q[1] // cell)), []).append(i)
        used = [False] * len(todo)
        cx, cy = 0.0, DH
        for _ in range(len(todo)):
            best, bd, brev = -1, 1e18, False
            ring = 0
            gx, gy = int(cx // cell), int(cy // cell)
            while best < 0 or ring * cell < math.sqrt(bd) + cell:
                for i_ in range(gx - ring, gx + ring + 1):
                    for j_ in range(gy - ring, gy + ring + 1):
                        if max(abs(i_ - gx), abs(j_ - gy)) != ring:
                            continue
                        for i in grid.get((i_, j_), ()):
                            if used[i]:
                                continue
                            st = todo[i]
                            for rev, q in ((False, st.pts[0]), (True, st.pts[-1])):
                                dd = (q[0] - cx) ** 2 + (q[1] - cy) ** 2
                                if dd < bd:
                                    best, bd, brev = i, dd, rev
                ring += 1
                if ring > 400:
                    break
            used[best] = True
            st = todo[best]
            pts = st.pts[::-1] if brev else st.pts
            out.append(Stroke(pts, st.pen, st.kind, st.f))
            cx, cy = pts[-1]
    return out


def _emit(strokes: Sequence[Stroke], bounds: Bounds) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    k = min((x1 - x0) / DW, (y1 - y0) / DH)
    ox = x0 + ((x1 - x0) - DW * k) / 2.0
    oy = y0 + ((y1 - y0) - DH * k) / 2.0
    out: List[GCodeCommand] = []
    for st in _order(list(strokes)):
        out += _poly([(ox + x * k, oy + y * k) for x, y in st.pts], color=st.pen, f=st.f)
    return out


def two_interferences(rng: SeededRNG, bounds: Bounds, colors: int = 6) -> List[GCodeCommand]:
    strokes, _ = build_strokes(rng, colors)
    return _emit(strokes, bounds)
