"""SUPERPOSITION r02 — SUPERPOSITION, COMPUTED (mechanism).

The reference's vertical rhythm, Q/K -> field -> softmax -> V -> Z, redrawn so
that every curve is a number out of GPT-2 small.

Data: ``head.npz`` beside this file, written by ``mechanism.py`` (numpy-only
forward pass of GPT-2 small, checked against HuggingFace/torch attention for
all 12 layers, max |diff| 2.3e-6) on

    "The pen plotter drew a black hole while the transformer watched itself think."

Head: layer 11, head 8.  Query followed: " itself" (token 12).  In this head
" itself" spreads its attention over the nouns that could be its antecedent
(hole .26, transformer .14, plot .14, ter .13, watched .11): the pronoun is
literally a weighted superposition of candidate referents.

THE MAPPING (one line each)
  every vector .. a 64-d vector c is drawn as the curve  f(x) = sum_n (c . e_n) phi_n(x/sigma)
                  where phi_n are the orthonormal Hermite functions and e_n an
                  orthonormal frame of the head space (3 modes shown: bell,
                  lean, width).  Hermite
                  functions are orthonormal, so the OVERLAP INTEGRAL of two
                  curves drawn in one frame is the dot product of their
                  projections; the map is linear, so a weighted sum of vectors
                  is drawn as the same weighted sum of curves.
  Q (red) ....... the 15 queries, frame e_0 = q_itself (e_1, e_2 = principal
                  directions of queries 1..14): " itself" is the one pure
                  bell.  Ruler mirrored (token 0 at the centre).
  K (blue) ...... the 15 keys, frame e_0 = mean key of tokens 1..14.  The sink
                  " The" is left out of both PCAs (|q| 17, |k| 15, orthogonal
                  to every other token) and is drawn by its projection.
  map (black) ... the causal attention matrix as a pyramid: row i (query i) is
                  the i-th stratum and holds i+1 cells, key 0 on the left edge,
                  the diagonal on the right edge.  Height of cell (i, j) =
                  ln(A_ij * (i+1)) = log-lift over uniform attention
                  (= Q.K^T/8 shifted by each row's own constant, the one shift
                  softmax cannot see); below uniform is sea (blank paper).  The
                  terrain is the sum of one CONE per cell, height = lift,
                  radius = 11.2 mm x lift / max lift: every cone has the same
                  slope, so one level step (0.177 nat) is one ring pitch
                  (0.95 mm) on every island -- count the rings, read the lift.
                  Exact at every cell centre except the two neighbours of
                  '.'->'.' (the corner eye spills onto them).
  slice ......... the dashed line through the pyramid is row 12, " itself".
  softmax ....... the spikes stand under their cells: height = A_12,j.  The
                  dashed line is uniform attention 1/13 = the map's coastline.
  V (ochre) ..... the 13 values " itself" can see, frame e_0 = z-hat, e_1, e_2
                  = principal directions of the weighted parts a_j v_j
                  orthogonal to z.  Open rings = the two future values.
  fans .......... Q -> row, K -> column: one strand per token.  softmax -> V and
                  V -> Z: ink fraction of each strand = a_j / max a.
  Z (green) ..... the partial sums  sum_{top m} a_j v_j  in weight order, in
                  the z frame.  The last one IS z, and because e_0 = z-hat it
                  is a pure Gaussian: every lopsided term cancels in the sum.
                  A partial sum is drawn only if it stands 1.8 mm clear of the
                  ones kept; each ends where it merges into its neighbours.

Pens (plot order, light -> dark): 0 goldenrod V + ochre fans · 1 dodgerblue K ·
2 crimson Q · 3 forestgreen Z · 4 black map, slice, softmax, all type.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Polygon, Rect, Union, clip, resample_by_arclength
from promptplot.generative.engine.scene3d import Occupancy
from promptplot.generative.generators import _GLYPHS, _chain_segments, _marching_squares, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

HERE = Path(__file__).resolve().parent
Pt = Tuple[float, float]
Poly = List[Pt]

OCHRE, BLUE, RED, GREEN, BLACK = 0, 1, 2, 3, 4

# design box: A4 portrait drawable, 190 x 277 mm, origin TOP-left, y DOWN
DW, DH = 190.0, 277.0
XC = 95.0

QI = 12            # the query we follow: " itself"
T = 15
MODES = 3          # bell (phi0) + lean (phi1) + width (phi2)

# ----------------------------------------------------------------- stations
Y_QK = 45.0        # Q / K baselines
APEX = 62.0        # pyramid row 0
HY = 5.6           # pyramid row pitch
WC = 9.2           # pyramid cell pitch (x)
Y_SM = 174.0       # softmax baseline
H_SM = 72.0        # mm per unit attention
Y_V = 223.0        # V baseline
Y_Z = 264.0        # Z baseline

SIG_QK = 3.3       # Hermite x-scale (mm) for Q, K
SIG_V = 3.4
SIG_Z = 12.0
S_QK = 3.1         # mm per unit, Q and K share it
S_V = 3.2          # mm per unit, V
S_Z = 7.0          # mm per unit, Z
Q_STEP = 4.9       # ruler pitch, Q and K
V_X0, V_X1 = 8.0, 182.0

TAIL = 0.35        # a curve is cut where it comes within TAIL mm of its baseline
TAIL_Z = 0.9       # Z nest: tails converge, so they stop higher
NEST_GAP = 1.8     # a partial sum is drawn only if it stands this far from every kept one
FLOOR = 0.8        # line-spacing floor (mm)


# ======================================================================
# data
# ======================================================================
def _load() -> Dict[str, np.ndarray]:
    d = np.load(HERE / "head.npz")
    return {k: d[k] for k in d.files}


def _hermite(nmax: int, x: np.ndarray) -> np.ndarray:
    """Orthonormal Hermite functions phi_0..phi_{nmax-1} at x (rows)."""
    out = np.zeros((nmax, len(x)))
    out[0] = math.pi ** -0.25 * np.exp(-x * x / 2.0)
    if nmax > 1:
        out[1] = math.sqrt(2.0) * x * out[0]
    for n in range(1, nmax - 1):
        out[n + 1] = math.sqrt(2.0 / (n + 1)) * x * out[n] - math.sqrt(n / (n + 1)) * out[n - 1]
    return out


def _frame(e0: np.ndarray, X: np.ndarray, r: int) -> np.ndarray:
    """Orthonormal frame: e0, then the top r-1 principal directions of the rows
    of X with their e0 component removed.  Each mode's sign is fixed so the
    family's summed coefficient is positive (a stated, data-free convention)."""
    e0 = e0 / np.linalg.norm(e0)
    P = X - np.outer(X @ e0, e0)
    _, _, Wt = np.linalg.svd(P, full_matrices=False)
    E = [e0]
    for w in Wt[: r - 1]:
        w = w - (w @ e0) * e0
        for e in E[1:]:
            w = w - (w @ e) * e
        w = w / np.linalg.norm(w)
        if (X @ w).sum() < 0:
            w = -w
        E.append(w)
    return np.vstack(E)


def _captured(X: np.ndarray, E: np.ndarray) -> np.ndarray:
    C = X @ E.T
    return (C ** 2).sum(1) / (X ** 2).sum(1)


class Mech:
    """Everything the plate draws, computed once."""

    def __init__(self) -> None:
        d = _load()
        self.tokens = [str(t) for t in d["tokens"]]
        self.Q, self.K, self.V = d["Q"], d["K"], d["V"]
        self.A, self.Z = d["A"], d["Z"]
        self.layer, self.head = int(d["layer"]), int(d["head"])
        # recompute what the file claims, from Q K V alone
        S = self.Q @ self.K.T / 8.0
        S = np.where(np.tril(np.ones((T, T), bool)), S, -np.inf)
        A = np.exp(S - S.max(1, keepdims=True))
        A /= A.sum(1, keepdims=True)
        self.err_A = float(np.abs(A - self.A).max())
        self.a = A[QI, : QI + 1]
        self.z = self.a @ self.V[: QI + 1]
        self.err_z = float(np.abs(self.z - self.Z[QI]).max())
        # frames
        # PCA of tokens 1..14: the sink ' The' (|q| 17, |k| 15, orthogonal to
        # every other token) would otherwise claim a whole mode for itself
        self.EQ = _frame(self.Q[QI], self.Q[1:], MODES)
        self.EK = _frame(self.K[1:].mean(0), self.K[1:], MODES)
        Vs = self.V[: QI + 1]
        zh = self.z / np.linalg.norm(self.z)
        self.EV = _frame(zh, self.a[:, None] * Vs, MODES)
        self.cq = self.Q @ self.EQ.T
        self.ck = self.K @ self.EK.T
        self.cv = Vs @ self.EV.T
        self.cz = self.z @ self.EV.T
        # map
        L = np.zeros((T, T))
        for i in range(T):
            for j in range(i + 1):
                L[i, j] = max(0.0, math.log(self.A[i, j] * (i + 1)))
        self.lift = L

    def report(self) -> str:
        lines = [
            f"GPT-2 small L{self.layer}H{self.head}, query {self.tokens[QI]!r}",
            f"|A(recomputed) - A(file)| = {self.err_A:.2e};  |a.V - z| = {self.err_z:.2e}",
            f"z-frame coefficients of z: {np.round(self.cz, 12).tolist()}",
            "captured by the %d drawn modes: Q %s" % (MODES, "%s") % np.round(_captured(self.Q, self.EQ), 2).tolist(),
            "                     K %s" % np.round(_captured(self.K, self.EK), 2).tolist(),
            "                     V %s" % np.round(_captured(self.V[: QI + 1], self.EV), 2).tolist(),
            "a = %s" % np.round(self.a, 4).tolist(),
        ]
        return "\n".join(lines)


# ======================================================================
# drawing primitives (design coords: mm, y down)
# ======================================================================
class Sheet:
    def __init__(self) -> None:
        self.strokes: List[Tuple[int, Poly, bool]] = []   # (pen, pts, halo-clippable)
        self.marks: List[Tuple[int, str, float, float, float]] = []
        self.halos: List[Tuple[float, float, float, float]] = []

    def line(self, pts: Sequence[Pt], pen: int, halo: bool = True) -> None:
        pts = [(float(x), float(y)) for x, y in pts]
        if len(pts) >= 2:
            self.strokes.append((pen, pts, halo))

    def dashed(self, pts: Sequence[Pt], pen: int, period: float, duty: float,
               phase: float = 0.0, halo: bool = True, min_dash: float = 0.6) -> None:
        """Dashes that FOLLOW the curve; ink fraction = duty.  Symmetric: the
        run starts and ends on ink.  Tone drives duty, never spacing."""
        duty = max(0.0, min(1.0, duty))
        if duty >= 0.97:
            self.line(pts, pen, halo)
            return
        dash = max(min_dash, duty * period)
        P = np.asarray(pts, float)
        seg = np.hypot(*np.diff(P, axis=0).T)
        s = np.concatenate([[0.0], np.cumsum(seg)])
        total = s[-1]
        if total < dash:
            return
        n = max(1, int(round((total - dash) / period)))
        per = (total - dash) / n if n else period
        for k in range(n + 1):
            a0 = k * per
            a1 = a0 + dash
            ts = np.concatenate([[a0], s[(s > a0) & (s < a1)], [a1]])
            xs = np.interp(ts, s, P[:, 0])
            ys = np.interp(ts, s, P[:, 1])
            self.line(list(zip(xs, ys)), pen, halo)

    def disc(self, x: float, y: float, r: float, pen: int) -> None:
        self.marks.append((pen, "disc", x, y, r))

    def ring(self, x: float, y: float, r: float, pen: int) -> None:
        self.marks.append((pen, "ring", x, y, r))


def _curve(c: np.ndarray, x0: float, base: float, sig: float, scale: float,
           span: float = 4.2, n: int = 160, tail: float = TAIL) -> Poly:
    """Hermite curve of coefficients ``c`` centred at x0 on baseline ``base``
    (up = -y).  Tails are cut where the curve stays within TAIL of the base."""
    u = np.linspace(-span, span, n)
    f = c @ _hermite(len(c), u)
    h = f * scale
    big = np.nonzero(np.abs(h) > tail)[0]
    if len(big) == 0:
        return []
    lo, hi = big[0], big[-1]
    lo = max(0, lo - 1)
    hi = min(n - 1, hi + 1)
    return [(x0 + u[k] * sig, base - h[k]) for k in range(lo, hi + 1)]


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 90) -> Poly:
    t = np.linspace(0.0, 1.0, n)[:, None]
    P = ((1 - t) ** 3) * np.array(p0) + 3 * ((1 - t) ** 2) * t * np.array(p1) \
        + 3 * (1 - t) * t * t * np.array(p2) + (t ** 3) * np.array(p3)
    return [tuple(p) for p in P]


def _strand(src: Pt, dst: Pt, a: float = 0.42, b: float = 0.42) -> Poly:
    """Leave vertically, run, arrive vertically (monotone control polygon)."""
    (sx, sy), (tx, ty) = src, dst
    g = ty - sy
    return _bez((sx, sy), (sx, sy + a * g), (tx, ty - b * g), (tx, ty))


class Family:
    """One line family under the engine's native crowd control
    (``Occupancy`` + pause-and-resume, the rule ``Scene3D.lines`` applies):
    lines are laid in priority order; a later line goes silent through any
    stretch within ``sep`` of an earlier one and resumes where space opens.
    ``seed`` lines (a baseline) occupy space without being re-drawn."""

    def __init__(self, sep: float = 0.85, warmup: int = 3, min_run: float = 1.2):
        self.occ = Occupancy(sep)
        self.warmup = warmup
        self.min_run = min_run
        self.runs: List[Poly] = []
        self.silenced = 0.0

    def seed(self, pts: Sequence[Pt]) -> None:
        for p in resample_by_arclength(list(pts), step=0.3):
            self.occ.add(p[0], p[1])

    def add(self, pts: Sequence[Pt], test=None) -> None:
        """``test(p)`` (optional) limits the crowd check to part of the line."""
        if len(pts) < 2:
            return
        dense = resample_by_arclength([tuple(p) for p in pts], step=0.3)
        run: Poly = []
        kept: Poly = []
        out: List[Poly] = []
        for k, p in enumerate(dense):
            if (k > self.warmup and k < len(dense) - 1 - self.warmup
                    and (test is None or test(p)) and self.occ.crowded(*p)):
                self.silenced += 0.3
                if len(run) >= 2:
                    out.append(run)
                run = []
            else:
                run.append(p)
                kept.append(p)
        if len(run) >= 2:
            out.append(run)
        for p in kept:
            self.occ.add(*p)
        for r in out:
            if sum(math.hypot(r[i + 1][0] - r[i][0], r[i + 1][1] - r[i][1])
                   for i in range(len(r) - 1)) >= self.min_run:
                self.runs.append(r)

    def add_crest(self, pts: Sequence[Pt]) -> None:
        """Nest rule: keep only the uncrowded run through the curve's crest
        (lowest y), so a nested curve ENDS where it merges into its
        neighbours instead of resuming as a floating fragment."""
        if len(pts) < 2:
            return
        dense = resample_by_arclength([tuple(p) for p in pts], step=0.3)
        k0 = min(range(len(dense)), key=lambda k: dense[k][1])
        ok = [not self.occ.crowded(*p) for p in dense]
        if not ok[k0]:
            self.silenced += 0.3 * len(dense)
            return
        a = k0
        while a > 0 and ok[a - 1]:
            a -= 1
        b = k0
        while b < len(dense) - 1 and ok[b + 1]:
            b += 1
        run = dense[a: b + 1]
        self.silenced += 0.3 * (len(dense) - len(run))
        for p in run:
            self.occ.add(*p)
        if len(run) >= 2:
            self.runs.append(run)

    def draw(self, S: "Sheet", pen: int) -> None:
        for r in self.runs:
            S.line(r, pen)


# ======================================================================
# type (own layout: glyphs are placed by their INK extents, because the
# shared font's advance table under-spaces i/l in proportional mode)
# ======================================================================
def _glyph_box(ch: str):
    g = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
    xs = [p[0] for s in g for p in s]
    ys = [p[1] for s in g for p in s]
    if not xs:
        return g, 0.0, 0.0, 0.0, 0.0
    return g, min(xs), max(xs), min(ys), max(ys)


def text_width(text: str, h: float, gap: float = 1.05, space: float = 2.6) -> float:
    sc = h / 6.0
    w = 0.0
    for k, ch in enumerate(text):
        if ch == " ":
            w += space * sc
            continue
        _, x0, x1, _, _ = _glyph_box(ch)
        w += (x1 - x0) * sc + (gap * sc if k < len(text) - 1 else 0.0)
    return w


def label(S: Sheet, text: str, x: float, y: float, h: float, pen: int = BLACK,
          anchor: str = "left", gap: float = 1.05, space: float = 2.6,
          pad: float = 1.0) -> Tuple[float, float, float, float]:
    """Set ``text`` with its baseline at y (design coords, y down), cap height h.
    Registers a halo box so other lines are clipped around it."""
    sc = h / 6.0
    w = text_width(text, h, gap, space)
    cx = x - (w if anchor == "right" else w / 2.0 if anchor == "center" else 0.0)
    lo_y, hi_y = 0.0, 6.0
    for ch in text:
        if ch == " ":
            cx += space * sc
            continue
        g, x0, x1, y0, y1 = _glyph_box(ch)
        lo_y, hi_y = min(lo_y, y0), max(hi_y, y1)
        for stroke in g:
            S.line([(cx + (gx - x0) * sc, y - gy * sc) for gx, gy in stroke], pen, halo=False)
        cx += (x1 - x0) * sc + gap * sc
    box = (x - (w if anchor == "right" else w / 2.0 if anchor == "center" else 0.0) - pad,
           y - hi_y * sc - pad, x - (w if anchor == "right" else w / 2.0 if anchor == "center" else 0.0) + w + pad,
           y - lo_y * sc + pad)
    S.halos.append(box)
    return box


# ======================================================================
# the stations
# ======================================================================
def _q_x(t: int) -> float:
    return XC - 10.0 - t * Q_STEP


def _k_x(t: int) -> float:
    return XC + 10.0 + t * Q_STEP


def _cell(i: int, j: int) -> Pt:
    return (XC + (j - i / 2.0) * WC, APEX + i * HY)


# pyramid outline (the causal mask): just outside every cell cone's support
KR_MM = 11.2        # cone radius (mm), isotropic: round eyes, one ring pitch
RING_MM = 0.95    # ring pitch (mm) on every island   # ring step = RING_MM x the 97th-percentile slope
OUT_PAD_X, OUT_PAD_Y = 0.95 * WC, 0.95 * HY


def _outline() -> Poly:
    top = (XC, APEX - OUT_PAD_Y * 1.6)
    bl = (XC - 7.0 * WC - OUT_PAD_X * 1.35, APEX + 14 * HY + OUT_PAD_Y)
    br = (XC + 7.0 * WC + OUT_PAD_X * 1.35, APEX + 14 * HY + OUT_PAD_Y)
    return [top, bl, br, top]


def _edge_x(y: float, side: int) -> float:
    top, bl, br, _ = _outline()
    far = bl if side < 0 else br
    t = (y - top[1]) / (far[1] - top[1])
    return top[0] + t * (far[0] - top[0])


def draw_qk(S: Sheet, M: Mech) -> Dict[str, float]:
    dips = {}
    for fam, pen in (("Q", RED), ("K", BLUE)):
        C = M.cq if fam == "Q" else M.ck
        xs = [_q_x(t) if fam == "Q" else _k_x(t) for t in range(T)]
        x_lo, x_hi = min(xs) - 9.0, max(xs) + 9.0
        base = [(x_lo, Y_QK), (x_hi, Y_QK)]
        S.line(base, pen)
        fam_lines = Family()
        fam_lines.seed(base)
        curves = {t: _curve(C[t], xs[t], Y_QK, SIG_QK, S_QK) for t in range(T)}
        first = [QI] if fam == "Q" else []
        rank = first + sorted((t for t in range(T) if t not in first),
                              key=lambda t: min(p[1] for p in curves[t]))
        dip = 0.0
        for t in rank:
            fam_lines.add(curves[t])
            dip = max([dip] + [p[1] - Y_QK for p in curves[t]])
        fam_lines.draw(S, pen)
        dips[fam] = dip
        # apex marker for the followed query; a ruler tick for every token
        for t in range(T):
            S.line([(xs[t], Y_QK + 0.9), (xs[t], Y_QK + 2.4)], pen)
        if fam == "Q":
            pk = _curve(C[QI], xs[QI], Y_QK, SIG_QK, S_QK)
            top = min(p[1] for p in pk)
            S.disc(xs[QI], top - 2.2, 0.75, pen)
    return dips


def draw_fans_qk(S: Sheet, M: Mech, dips: Dict[str, float]) -> None:
    """Query t -> the start of row t (left edge); key t -> the start of
    column t (the diagonal, right edge)."""
    for fam, pen, side in (("Q", RED, -1), ("K", BLUE, +1)):
        for t in range(T):
            sx = _q_x(t) if fam == "Q" else _k_x(t)
            y_row = APEX + t * HY
            tx = _edge_x(y_row, side)
            src = (sx, Y_QK + dips[fam] + 1.6)
            dst = (tx, y_row)
            pts = _strand(src, dst, a=0.30 + 0.012 * t, b=0.52 - 0.012 * t)
            if t % 2:
                pts = pts[::-1]
            if fam == "Q" and t == QI:
                S.line(pts, pen)
            else:
                S.dashed(pts, pen, period=6.0, duty=0.5)
        # landing ticks on the outline are the strands' ends; nothing else


def _field(M: Mech):
    x0, x1 = XC - 7.0 * WC - 3.0 * WC, XC + 7.0 * WC + 3.0 * WC
    y0, y1 = APEX - 3.0 * HY, APEX + 14 * HY + 3.0 * HY
    cell = 0.45
    xs = np.arange(x0, x1 + 1e-9, cell)
    ys = np.arange(y0, y1 + 1e-9, cell)
    X, Y = np.meshgrid(xs, ys)
    F = np.zeros_like(X)
    # one CONE per cell, height = lift, RADIUS PROPORTIONAL TO LIFT: every
    # cone has the same slope, so one uniform level step gives one ring pitch
    # on every island (the bigger the attention, the bigger the eye).
    lmax = float(M.lift.max())
    for i in range(T):
        for j in range(i + 1):
            lam = M.lift[i, j]
            if lam <= 0.0:
                continue
            cx, cy = _cell(i, j)
            r = np.hypot(X - cx, Y - cy)
            F += lam * np.clip(1.0 - r / (KR_MM * lam / lmax), 0.0, None)
    return F, xs, ys, cell


def draw_map(S: Sheet, M: Mech) -> Dict[str, float]:
    F, xs, ys, cell = _field(M)
    # uniform level step, sized by the field's gradient so rings sit ~1 mm apart
    gy, gx = np.gradient(F, cell)
    g = np.hypot(gx, gy)
    # every cone has slope lmax / KR_MM, so this step puts rings exactly
    # RING_MM apart on every island; where two cones overlap their slopes add
    # and the Family below silences the stretch that would crowd
    step = RING_MM * float(M.lift.max()) / KR_MM
    levels = np.arange(step * 0.5, F.max(), step)
    Fl = F.tolist()
    xl, yl = xs.tolist(), ys.tolist()
    inside = Polygon(_outline()[:-1])
    fam = Family(sep=0.88, warmup=0)
    fam.seed(_outline())
    n_chains = 0
    for lv in levels:
        for ch in _chain_segments(_marching_squares(Fl, xl, yl, float(lv))):
            if len(ch) < 6:
                continue
            L = sum(math.hypot(ch[k + 1][0] - ch[k][0], ch[k + 1][1] - ch[k][1])
                    for k in range(len(ch) - 1))
            if L < 3.0:
                continue
            for run in clip(ch, inside, keep="inside"):
                fam.add(run)
            n_chains += 1
    fam.draw(S, BLACK)
    o = _outline()
    for k in range(3):             # three strokes: each edge is a batch boundary
        S.line([o[k], o[k + 1]], BLACK)
    return {"step": step, "levels": len(levels), "chains": n_chains, "Fmax": float(F.max()),
            "silenced_mm": fam.silenced, "min_pitch": step / float(g.max())}


def draw_slice_softmax(S: Sheet, M: Mech) -> None:
    y_row = APEX + QI * HY
    xl, xr = _edge_x(y_row, -1), _edge_x(y_row, +1)
    S.dashed([(xl, y_row), (xr, y_row)], BLACK, period=3.2, duty=0.55)
    S.ring(xl, y_row, 1.1, BLACK)
    S.ring(xr, y_row, 1.1, BLACK)
    # softmax row
    xs = [_cell(QI, j)[0] for j in range(QI + 1)]
    S.line([(xs[0] - 7.0, Y_SM), (xs[-1] + 7.0, Y_SM)], BLACK)
    uni = 1.0 / (QI + 1)
    S.dashed([(xs[0] - 7.0, Y_SM - uni * H_SM), (xs[-1] + 7.0, Y_SM - uni * H_SM)],
             BLACK, period=4.0, duty=0.45)
    for j, x in enumerate(xs):
        h = M.a[j] * H_SM
        S.line([(x, Y_SM + 0.9), (x, Y_SM + 2.2)], BLACK)
        if h > TAIL * 2:
            u = np.linspace(-3.4, 3.4, 60)
            y = Y_SM - h * np.exp(-0.5 * u * u)
            keep = np.abs(Y_SM - y) > TAIL
            pts = [(x + uu * 1.15, yy) for uu, yy, k in zip(u, y, keep) if k]
            S.line(pts, BLACK)
        if M.a[j] > uni:
            # the cell's own vertical: from the slice to the spike's crown
            S.line([(x, _outline()[1][1] + 1.2), (x, Y_SM - h - 2.2)], BLACK)
            S.disc(x, Y_SM - h - 2.2, 0.7, BLACK)


def _v_x(j: int) -> float:
    return V_X0 + j * (V_X1 - V_X0) / (T - 1)


def draw_v(S: Sheet, M: Mech) -> Dict[str, float]:
    base = [(3.0, Y_V), (187.0, Y_V)]
    S.line(base, OCHRE)
    fam = Family()
    fam.seed(base)
    tops, dip = {}, 0.0
    curves = {j: _curve(M.cv[j], _v_x(j), Y_V, SIG_V, S_V) for j in range(QI + 1)}
    for j in sorted(curves, key=lambda j: -M.a[j]):      # heaviest weight on top
        fam.add(curves[j])
        tops[j] = min(p[1] for p in curves[j])
        dip = max([dip] + [p[1] - Y_V for p in curves[j]])
    fam.draw(S, OCHRE)
    for j in range(T):
        x = _v_x(j)
        if j > QI:          # the future: " itself" cannot see these values
            S.ring(x, Y_V, 0.9, OCHRE)
            continue
        S.line([(x, Y_V + 0.9), (x, Y_V + 2.2)], OCHRE)
    return {"top": min(tops.values()), "dip": dip}


def draw_fans_v(S: Sheet, M: Mech, vinfo: Dict[str, float]) -> None:
    amax = M.a.max()
    xs = [_cell(QI, j)[0] for j in range(QI + 1)]
    land_y = vinfo["top"] - 4.0
    for j in range(QI + 1):
        duty = M.a[j] / amax
        if duty < 0.04:
            continue
        pts = _strand((xs[j], Y_SM + 3.5), (_v_x(j), land_y), a=0.40, b=0.45)
        S.dashed(pts[::-1] if j % 2 else pts, OCHRE, period=5.0, duty=duty)
        S.ring(_v_x(j), land_y + 1.2, 0.9, OCHRE)
    # V -> Z : strands pour into the bell
    zc = M.cz
    for j in range(QI + 1):
        duty = M.a[j] / amax
        if duty < 0.04:
            continue
        tx = XC + (j - QI / 2.0) * 4.4
        u = (tx - XC) / SIG_Z
        fz = float(zc @ _hermite(MODES, np.array([u]))[:, 0]) * S_Z
        pts = _strand((_v_x(j), Y_V + vinfo["dip"] + 1.6), (tx, Y_Z - fz - 2.0), a=0.35, b=0.50)
        S.dashed(pts[::-1] if j % 2 else pts, OCHRE, period=5.0, duty=duty)


def draw_z(S: Sheet, M: Mech) -> Dict[str, float]:
    base = [(XC - 52.0, Y_Z), (XC + 52.0, Y_Z)]
    S.line(base, GREEN)
    order = np.argsort(-M.a)
    acc = np.zeros(MODES)
    partial = []
    for j in order:
        acc = acc + M.a[j] * M.cv[j]
        partial.append(acc.copy())
    # z itself first, then every partial sum that stands at least NEST_GAP
    # clear of the last one kept: a sum is drawn whole or not at all, so the
    # nest stays a family of continuous curves (tails stop TAIL_Z above base)
    u = np.linspace(-4.2, 4.2, 240)
    H = _hermite(MODES, u)
    kept: List[np.ndarray] = []
    drawn = 0
    fam = Family(sep=0.9, warmup=0, min_run=3.0)
    fam.seed(base)
    for c in partial[::-1]:
        f = c @ H * S_Z
        if kept and min(np.abs(f - g).max() for g in kept) < NEST_GAP:
            continue
        kept.append(f)
        # only the converging TAILS (lowest 4 mm) are under crowd control
        fam.add_crest(_curve(c, XC, Y_Z, SIG_Z, S_Z, n=240, tail=TAIL_Z))
        drawn += 1
    fam.draw(S, GREEN)
    return {"nest": drawn}


def _sea_spot(M: Mech, w: float, h: float) -> Pt:
    """Lower-left corner (baseline) of a w x h box that lies inside the
    pyramid, touches no island (F == 0 with a 2.5 mm margin) and sits nearest
    the upper-left third of the sea."""
    F, xs, ys, _ = _field(M)
    poly = Polygon(_outline()[:-1])
    target = (XC - 0.30 * 7.0 * WC, APEX + 0.40 * 14 * HY)
    best, bd = (XC - 20.0, APEX + 30.0), 1e9
    for y in np.arange(APEX + 8.0, APEX + 14 * HY, 1.0):
        for x in np.arange(XC - 7.0 * WC, XC, 1.0):
            corners = [(x - 2.5, y + 2.5), (x + w + 2.5, y + 2.5), (x - 2.5, y - h - 2.5),
                       (x + w + 2.5, y - h - 2.5)]
            if not all(poly.contains(*c) for c in corners):
                continue
            ix = (xs >= x - 2.5) & (xs <= x + w + 2.5)
            iy = (ys >= y - h - 2.5) & (ys <= y + 2.5)
            if F[np.ix_(iy, ix)].max() > 0.0:
                continue
            d = math.hypot(x + w / 2 - target[0], y - h / 2 - target[1])
            if d < bd:
                best, bd = (float(x), float(y)), d
    return best


def draw_type(S: Sheet, M: Mech) -> None:
    label(S, "Q", 5.0, 16.0, 4.4)
    # the data, once: the sentence GPT-2 read
    label(S, "The pen plotter drew a black hole while the transformer watched itself think.",
          XC, 9.0, 1.9, anchor="center")
    label(S, "K", 185.0, 16.0, 4.4, anchor="right")
    label(S, "itself", _q_x(QI), Y_QK + 6.4, 2.0, anchor="center")
    # Q.K^T is set in the SEA (blank paper = below-uniform attention), in the
    # clear spot nearest the upper-left of the pyramid
    xq, yq = _sea_spot(M, w=17.0, h=5.0)
    label(S, "Q", xq, yq, 3.4)
    S.disc(xq + 4.8, yq - 1.7, 0.45, BLACK)
    label(S, "K", xq + 6.6, yq, 3.4)
    label(S, "T", xq + 10.2, yq - 2.8, 2.0)
    label(S, "softmax", _cell(QI, QI)[0] + 9.0, Y_SM - 1.4, 2.6)
    label(S, "1/13", _cell(QI, QI)[0] + 9.0, Y_SM - H_SM / (QI + 1) + 0.9, 1.8)
    label(S, "V", 5.0, Y_V - 40.0, 4.2)
    label(S, "Z = AV", XC + 40.0, Y_Z - 12.0, 3.6)
    uni = 1.0 / (QI + 1)
    prev, low_prev = -9, False
    for j in range(QI + 1):
        if M.a[j] > uni:
            low = 2.9 if j == prev + 1 and not low_prev else 0.0
            label(S, M.tokens[j].strip(), _v_x(j), Y_V + 6.6 + low, 1.9, anchor="center")
            low_prev, prev = bool(low), j
    # the punchline: the pronoun as a weighted sum of its candidate referents
    order = [j for j in np.argsort(-M.a) if M.a[j] > uni]
    rest = 1.0 - sum(M.a[j] for j in order)
    terms = " + ".join(f"{M.a[j]:.2f}".lstrip("0") + " " + M.tokens[j].strip() for j in order)
    cap = f"itself = {terms} + {rest:.2f}".replace("0.", ".") + " rest"
    label(S, cap, XC, 274.0, 2.1, anchor="center")


# ======================================================================
# emit
# ======================================================================
def _clip_halos(S: Sheet) -> List[Tuple[int, Poly]]:
    if not S.halos:
        return [(p, pts) for p, pts, _ in S.strokes]
    region = Union(*[Rect(*b) for b in S.halos])
    out: List[Tuple[int, Poly]] = []
    for pen, pts, halo in S.strokes:
        if not halo:
            out.append((pen, pts))
            continue
        bx = [b for b in S.halos]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        hit = any(not (max(xs) < b[0] or min(xs) > b[2] or max(ys) < b[1] or min(ys) > b[3]) for b in bx)
        if not hit:
            out.append((pen, pts))
            continue
        for run in clip(pts, region, keep="outside"):
            L = sum(math.hypot(run[k + 1][0] - run[k][0], run[k + 1][1] - run[k][1])
                    for k in range(len(run) - 1))
            if L > 0.5:
                out.append((pen, run))
    return out


def _mark_poly(kind: str, x: float, y: float, r: float) -> Poly:
    if kind == "ring":
        n = max(18, int(r * 30))
        return [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n))
                for k in range(n + 1)]
    # solid dot: one spiral out to r, then the rim — a single stroke.  Pitch
    # 0.3 mm: a declared exception to the 0.8 mm floor; every dot is < 2 mm.
    turns = max(2, int(r / 0.3))
    n = turns * 24
    pts = [(x + r * k / n * math.cos(2 * math.pi * turns * k / n),
            y + r * k / n * math.sin(2 * math.pi * turns * k / n)) for k in range(n + 1)]
    pts += [(x + r * math.cos(2 * math.pi * k / 30), y + r * math.sin(2 * math.pi * k / 30))
            for k in range(31)]
    return pts


def _chain_order(polys: List[Poly], start: Pt) -> List[Poly]:
    """Batch-friendly order for one pen layer: greedy nearest END (either end,
    the stroke is reversed to suit), starting from the park point.  The
    pipeline's own nearest-START pass then reproduces this chain."""
    left = list(range(len(polys)))
    heads = np.array([p[0] for p in polys])
    tails = np.array([p[-1] for p in polys])
    alive = np.ones(len(polys), bool)
    pos = np.array(start)
    out: List[Poly] = []
    for _ in left:
        dh = np.where(alive, np.hypot(*(heads - pos).T), np.inf)
        dt = np.where(alive, np.hypot(*(tails - pos).T), np.inf)
        ih, it = int(dh.argmin()), int(dt.argmin())
        if dh[ih] <= dt[it]:
            k, pts = ih, polys[ih]
        else:
            k, pts = it, polys[it][::-1]
        alive[k] = False
        out.append(pts)
        pos = np.array(pts[-1])
    return out


def superposition_computed(rng: SeededRNG, bounds, colors: int = 5) -> List[GCodeCommand]:
    try:  # cream stock, hairline preview — never touches the gcode
        from promptplot.config import get_config

        viz = get_config().visualization
        viz.paper_color = "cream"
        viz.line_width = 0.55
    except Exception:  # pragma: no cover
        pass

    M = Mech()
    S = Sheet()
    dips = draw_qk(S, M)
    draw_fans_qk(S, M, dips)
    stats = draw_map(S, M)
    draw_slice_softmax(S, M)
    vinfo = draw_v(S, M)
    draw_fans_v(S, M, vinfo)
    stats.update(draw_z(S, M))
    draw_type(S, M)

    x0, y0, x1, y1 = bounds
    k = min((x1 - x0) / DW, (y1 - y0) / DH)
    ox = x0 + ((x1 - x0) - DW * k) / 2.0
    oy = y1 - ((y1 - y0) - DH * k) / 2.0

    def P(p: Pt) -> Pt:
        return (ox + p[0] * k, oy - p[1] * k)

    polys: Dict[int, List[Poly]] = {}
    for pen, pts in _clip_halos(S):
        polys.setdefault(pen, []).append([P(p) for p in pts])
    for pen, kind, x, y, r in S.marks:
        polys.setdefault(pen, []).append([P(p) for p in _mark_poly(kind, x, y, r)])
    out: List[GCodeCommand] = []
    for pen in sorted(polys):
        for pts in _chain_order(polys[pen], (0.0, 0.0)):
            out += _poly(pts, color=pen, f=1500)
    superposition_computed.stats = stats  # type: ignore[attr-defined]
    superposition_computed.report = M.report()  # type: ignore[attr-defined]
    return out


if __name__ == "__main__":
    print(Mech().report())
