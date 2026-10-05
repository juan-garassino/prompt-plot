"""SUPERPOSITION r04 — iterate (merge of r02's layout with r03's field grammar).

Data (unchanged from r02): GPT-2 small, layer 11, head 8, on

    "The pen plotter drew a black hole while the transformer watched itself think."

``../r02/head.npz``, written by ``../r02/mechanism.py`` (numpy forward pass,
matched to HuggingFace/torch attention at <= 2.3e-6 on all 12 layers).
Query followed: " itself" (token 12).

THE RULE (Manfred Mohr: one stated projection, the rule is the image)
  every vector c ... f(x) = sum_{k<3} (c . e_k) H_k(x / sigma), H_k the
                     orthonormal Hermite functions.  Linear + orthonormal, so
                     a weighted sum of vectors IS the same weighted sum of
                     curves, and the overlap integral of two curves drawn in
                     one frame is their dot product.
  Q and K share ONE frame: e_0 = q(itself)/|q(itself)|, e_1, e_2 = principal
                     directions of the queries and keys 1..14 orthogonal to it.
                     So " itself" is the one pure red bell, and the bell part
                     (H_0) of every blue key is exactly its score with
                     " itself":  integral f_itself f_key = q(itself) . k.
  V and Z share ONE frame: e_0 = z/|z|, e_1, e_2 = principal directions of the
                     weighted values a_j v_j orthogonal to z.  z is therefore a
                     pure bell by construction: every lean cancels in the sum.
  sign convention .. e_1: the family's summed coefficient is positive;
                     e_2: negative (so a width term sharpens a bell).

THE STATIONS (top to bottom, the reference's rhythm)
  Q (crimson), K (blue) ... the 15 queries / keys, Q ruler unfolding left from
                     the centre and K right, so their strands nest.
  strands .......... query i runs down the left gutter and arrives horizontally
                     on row i; key t drops, steps left and runs down its own
                     column onto the causal knife at its diagonal cell.
  field (black) .... the causal matrix as a RIGHT triangle, key 0 the vertical
                     left edge, the knife (key <= query) down to the lower
                     right.  Encoded value: lift = ln(A_ij (i+1)), attention
                     over uniform.  Field = upper envelope of one cone per cell
                     (height = lift, one slope for every cone), so the field at
                     every cell centre IS the lift, and the level sets are
                     exact offsets of each other: ring n sits at
                     A (i+1) = 1.2^n, one ring per mm, everywhere.
  row 12 ........... the " itself" query strand threads its row; its five
                     above-uniform keys drop straight down their key columns.
  softmax .......... spikes of height A_12,j at 72 mm per unit, under their
                     columns.
  V (ochre) ........ the 13 values " itself" can see, under their columns.
                     Drops land on the curve crests; ink fraction = a_j/max a.
  Z (green) ........ z by visible addition: the partial sums hole, +transformer,
                     +plot, +ter, +watched, +rest, in V's rule and V's scale,
                     one centre (the attention-weighted mean column), one
                     baseline.  The last one IS R(z).  Every V -> Z strand
                     (ink fraction = a_j/max a) ends ON the curve its term
                     creates.

Pens, plot order light -> dark: 0 goldenrod V · 1 dodgerblue K · 2 crimson Q ·
3 forestgreen Z · 4 black field/knife/softmax/drops · 5 fine black type (last).
Nothing is random; the seed is unused.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import HalfPlane, Rect, Union, clip, resample_by_arclength
from promptplot.generative.engine.scene3d import Occupancy
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "r02" / "head.npz"
Pt = Tuple[float, float]
Poly = List[Pt]

OCHRE, BLUE, RED, GREEN, BLACK, TYPE = 0, 1, 2, 3, 4, 5

# design box: A4 portrait drawable, 190 x 277 mm, origin TOP-left, y DOWN
DW, DH = 190.0, 277.0

QI = 12            # the query we follow: " itself"
T = 15
MODES = 3

# ---------------------------------------------------------------- Q / K band
Y_QK = 19.5        # Q / K baselines
SIG_QK = 3.3       # Hermite x-scale (mm), Q and K
S_QK = 1.85        # mm per unit, Q and K
QK_STEP = 5.2      # ruler pitch
XQ0 = 86.0         # Q token 0 (the ruler unfolds LEFT)
XK0 = 108.0       # K token 0 (the ruler unfolds RIGHT)
G = 1.0            # strand bundle pitch (gutter lanes, turn bands)

# ---------------------------------------------------------------- the field
X0 = 21.0          # key -1/2: the triangle's vertical left edge
PX = 10.8          # mm per key
PY = 5.7           # mm per query
LV = math.log(1.2)  # one ring = x1.2 of attention over uniform (ring 0 = uniform)
RING = 0.82        # ring pitch, mm (constant, by construction)
SLOPE = LV / RING  # nat per mm, the same for every cone
L0 = 4.0           # key-0 leg: K band bottom -> knife
KNIFE2 = 0.9       # the knife is two passes, 0.9 mm apart (the sheet's heaviest line)

# ---------------------------------------------------------------- lower stations
Y_SM = 162.0       # softmax baseline
H_SM = 72.0        # mm per unit attention (r02, measured exact by science)
Y_V = 196.5        # V baseline
SIG_V = 6.6        # Hermite x-scale (mm), V and Z (the SAME rule)
S_V = 4.0          # mm per unit, V and Z (the SAME scale)
Y_Z = 262.0        # Z baseline
ZK = 2.5           # Z is drawn at a DECLARED x2.5 of V's rule (both axes); the 1x R(z) stands beside it
SIG_Z, S_Z = ZK * SIG_V, ZK * S_V
Y_CAP = 268.4      # the caption (the punchline)
Y_FOOT = 272.6     # footer lines (provenance, rule)

TAIL = 0.35
FLOOR = 0.8


# ======================================================================
# data
# ======================================================================
def _hermite(nmax: int, x: np.ndarray) -> np.ndarray:
    """Orthonormal Hermite functions H_0..H_{nmax-1} at x (rows)."""
    out = np.zeros((nmax, len(x)))
    out[0] = math.pi ** -0.25 * np.exp(-x * x / 2.0)
    if nmax > 1:
        out[1] = math.sqrt(2.0) * x * out[0]
    for n in range(1, nmax - 1):
        out[n + 1] = math.sqrt(2.0 / (n + 1)) * x * out[n] - math.sqrt(n / (n + 1)) * out[n - 1]
    return out


def _frame(e0: np.ndarray, X: np.ndarray, r: int) -> np.ndarray:
    """e0, then the top r-1 principal directions of X's rows orthogonal to e0.
    Sign convention (data-free, stated): mode 1 makes the family's summed
    coefficient positive, mode 2 negative (a width term sharpens a bell)."""
    e0 = e0 / np.linalg.norm(e0)
    P = X - np.outer(X @ e0, e0)
    _, _, Wt = np.linalg.svd(P, full_matrices=False)
    E = [e0]
    for n, w in enumerate(Wt[: r - 1], start=1):
        for e in E:
            w = w - (w @ e) * e
        w = w / np.linalg.norm(w)
        s = (X @ w).sum()
        if (n == 1 and s < 0) or (n == 2 and s > 0):
            w = -w
        E.append(w)
    return np.vstack(E)


def _captured(X: np.ndarray, E: np.ndarray) -> np.ndarray:
    C = X @ E.T
    return (C ** 2).sum(1) / (X ** 2).sum(1)


class Mech:
    """Everything the plate draws, computed once from Q, K, V."""

    def __init__(self) -> None:
        d = np.load(DATA)
        self.tokens = [str(t) for t in d["tokens"]]
        self.Q, self.K, self.V = d["Q"], d["K"], d["V"]
        self.layer, self.head = int(d["layer"]), int(d["head"])
        S = self.Q @ self.K.T / 8.0
        S = np.where(np.tril(np.ones((T, T), bool)), S, -np.inf)
        A = np.exp(S - S.max(1, keepdims=True))
        A /= A.sum(1, keepdims=True)
        self.err_A = float(np.abs(A - d["A"]).max())
        self.A = A
        self.a = A[QI, : QI + 1]
        self.z = self.a @ self.V[: QI + 1]
        self.err_z = float(np.abs(self.z - d["Z"][QI]).max())
        self.scores = self.Q[QI] @ self.K[: QI + 1].T          # raw q.k
        # Q and K: ONE frame, e0 = q(itself)
        self.EQK = _frame(self.Q[QI], np.vstack([self.Q[1:], self.K[1:]]), MODES)
        self.cq = self.Q @ self.EQK.T
        self.ck = self.K @ self.EQK.T
        # V and Z: ONE frame, e0 = z
        Vs = self.V[: QI + 1]
        self.EV = _frame(self.z, self.a[:, None] * Vs, MODES)
        self.cv = Vs @ self.EV.T
        self.cz = self.z @ self.EV.T
        # overlap identity: integral f_itself f_k (in units of sigma) = q.k
        self.overlap = self.cq[QI] @ self.ck[: QI + 1].T
        # lift (the encoded value)
        L = np.zeros((T, T))
        for i in range(T):
            for j in range(i + 1):
                L[i, j] = max(0.0, math.log(A[i, j] * (i + 1)))
        self.lift = L
        # partial sums, weight order: 5 named terms, then the rest in one go
        uni = 1.0 / (QI + 1)
        self.named = [int(j) for j in np.argsort(-self.a) if self.a[j] > uni]
        self.rest = [j for j in range(QI + 1) if j not in self.named]
        acc = np.zeros(MODES)
        self.partials: List[np.ndarray] = []
        for j in self.named:
            acc = acc + self.a[j] * self.cv[j]
            self.partials.append(acc.copy())
        for j in self.rest:
            acc = acc + self.a[j] * self.cv[j]
        self.partials.append(acc.copy())          # == cz
        self.term_of = {j: k for k, j in enumerate(self.named)}
        for j in self.rest:
            self.term_of[j] = len(self.named)

    def report(self) -> str:
        t = self.tokens
        lines = [
            f"GPT-2 small L{self.layer}H{self.head}, query {t[QI]!r}",
            f"|A(recomputed) - A(file)| = {self.err_A:.2e};  |a.V - z| = {self.err_z:.2e}",
            "overlap f_itself.f_key - q.k: max %.2e" % np.abs(self.overlap - self.scores).max(),
            "q.k(hole) = %.3f  /8 = %.4f" % (self.scores[7], self.scores[7] / 8),
            "captured Q %s" % np.round(_captured(self.Q, self.EQK), 2).tolist(),
            "captured K %s" % np.round(_captured(self.K, self.EQK), 2).tolist(),
            "captured V %s" % np.round(_captured(self.V[: QI + 1], self.EV), 2).tolist(),
            "cz = %s" % np.round(self.cz, 12).tolist(),
            "partials: " + " | ".join(str(np.round(p, 3).tolist()) for p in self.partials),
            "a = %s" % np.round(self.a, 4).tolist(),
        ]
        return "\n".join(lines)


# ======================================================================
# sheet
# ======================================================================
class Sheet:
    def __init__(self) -> None:
        self.strokes: List[Tuple[int, Poly, bool]] = []   # (pen, pts, halo-clippable)
        self.halos: List[Tuple[float, float, float, float]] = []

    def line(self, pts: Sequence[Pt], pen: int, halo: bool = True) -> None:
        pts = [(float(x), float(y)) for x, y in pts]
        if len(pts) >= 2:
            self.strokes.append((pen, pts, halo))

    def dashed(self, pts: Sequence[Pt], pen: int, duty: float, period: float = 9.0,
               min_dash: float = 1.6) -> int:
        """Ink fraction = ``duty`` exactly, and the run starts AND ends on ink,
        so a strand touches both of its ends.  n dashes of length d and n-1
        gaps g with d / (d + g) = duty; n is chosen so d + g ~ ``period``,
        reduced if a dash would fall under ``min_dash`` (duty is kept, never
        the dash shortened).  Returns the number of dashes."""
        duty = max(0.0, min(1.0, duty))
        P = np.asarray(pts, float)
        seg = np.hypot(*np.diff(P, axis=0).T)
        s = np.concatenate([[0.0], np.cumsum(seg)])
        total = float(s[-1])
        if duty >= 0.97:
            self.line(pts, pen)
            return 1
        if duty <= 0.0 or total * duty < min_dash:
            return 0
        n = max(1, int(round(total / period)))

        def dash_len(n: int) -> float:
            return total / (n + (n - 1) * (1.0 - duty) / duty) if n > 1 else total

        while n > 1 and dash_len(n) < min_dash:
            n -= 1
        if n == 1:
            # one dash cannot touch both ends: two dashes, one at each end
            n = 2
            if dash_len(2) < min_dash:
                return 0
        d = dash_len(n)
        g = d * (1.0 - duty) / duty
        for k in range(n):
            a0 = k * (d + g)
            a1 = min(total, a0 + d)
            ts = np.concatenate([[a0], s[(s > a0) & (s < a1)], [a1]])
            self.line(list(zip(np.interp(ts, s, P[:, 0]), np.interp(ts, s, P[:, 1]))), pen)
        return n


def _plen(pts: Sequence[Pt]) -> float:
    P = np.asarray(pts, float)
    return float(np.hypot(*np.diff(P, axis=0).T).sum()) if len(P) > 1 else 0.0


def _curve(c: np.ndarray, x0: float, base: float, sig: float, scale: float,
           span: float = 4.4, n: int = 200, tail: float = TAIL) -> Poly:
    """Hermite curve of coefficients c centred at x0 on baseline ``base``
    (up = -y).  Tails are cut where the curve stays within ``tail`` of it."""
    u = np.linspace(-span, span, n)
    h = (c @ _hermite(len(c), u)) * scale
    big = np.nonzero(np.abs(h) > tail)[0]
    if len(big) == 0:
        return []
    lo, hi = max(0, big[0] - 1), min(n - 1, big[-1] + 1)
    return [(x0 + u[k] * sig, base - h[k]) for k in range(lo, hi + 1)]


def _curve_at(c: np.ndarray, x: float, x0: float, base: float, sig: float, scale: float) -> float:
    u = np.array([(x - x0) / sig])
    return float(base - (c @ _hermite(len(c), u))[0] * scale)


def _clear_start(pts: Poly, occ: Occupancy, limit: float = 14.0) -> Poly:
    """Drop a strand's leading stretch while it runs within the crowd distance
    of its family's ink (a strand leaving a steep flank would otherwise ride
    it under 0.8 mm).  Only the first ``limit`` mm are examined."""
    dense = resample_by_arclength([tuple(p) for p in pts], step=0.2)
    k = 0
    while k < len(dense) - 2 and k * 0.2 < limit and occ.crowded(*dense[k]):
        k += 1
    return dense[k:]


def _fillet_path(corners: Sequence[Pt], radii: Sequence[float], n: int = 10) -> Poly:
    """Orthogonal polyline through ``corners`` with a circular fillet of
    radius radii[k] at every interior corner k (1..len-2)."""
    out: Poly = [corners[0]]
    for k in range(1, len(corners) - 1):
        p0, p1, p2 = (np.array(corners[k - 1]), np.array(corners[k]), np.array(corners[k + 1]))
        d0 = (p1 - p0) / max(1e-9, np.linalg.norm(p1 - p0))
        d1 = (p2 - p1) / max(1e-9, np.linalg.norm(p2 - p1))
        r = min(radii[k], 0.49 * np.linalg.norm(p1 - p0), 0.49 * np.linalg.norm(p2 - p1))
        a = p1 - d0 * r
        b = p1 + d1 * r
        c = a + d1 * r                      # the fillet centre
        ta = math.atan2(*(a - c)[::-1])
        tb = math.atan2(*(b - c)[::-1])
        dt = (tb - ta + math.pi) % (2 * math.pi) - math.pi
        for m in range(n + 1):
            t = ta + dt * m / n
            out.append((c[0] + r * math.cos(t), c[1] + r * math.sin(t)))
    out.append(corners[-1])
    return out


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 90) -> Poly:
    t = np.linspace(0.0, 1.0, n)[:, None]
    P = ((1 - t) ** 3) * np.array(p0) + 3 * ((1 - t) ** 2) * t * np.array(p1) \
        + 3 * (1 - t) * t * t * np.array(p2) + (t ** 3) * np.array(p3)
    return [tuple(p) for p in P]


class Family:
    """One line family under the engine's native crowd control (``Occupancy``
    + pause-and-resume): lines are laid in priority order, a later line goes
    silent through any stretch within ``sep`` of an earlier one."""

    def __init__(self, sep: float = 0.85, warmup: int = 3, min_run: float = 1.6):
        self.occ = Occupancy(sep)
        self.warmup = warmup
        self.min_run = min_run
        self.runs: List[Poly] = []
        self.silenced = 0.0

    def seed(self, pts: Sequence[Pt]) -> None:
        for p in resample_by_arclength(list(pts), step=0.3):
            self.occ.add(p[0], p[1])

    def add(self, pts: Sequence[Pt]) -> None:
        if len(pts) < 2:
            return
        dense = resample_by_arclength([tuple(p) for p in pts], step=0.3)
        run: Poly = []
        kept: Poly = []
        out: List[Poly] = []
        for k, p in enumerate(dense):
            if (self.warmup < k < len(dense) - 1 - self.warmup) and self.occ.crowded(*p):
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
            if _plen(r) >= self.min_run:
                self.runs.append(r)

    def draw(self, S: Sheet, pen: int) -> None:
        for r in self.runs:
            S.line(r, pen)


# ======================================================================
# type — glyphs placed by their INK extents (the shared font's advance
# table under-spaces i/l)
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


def label(S: Sheet, text: str, x: float, y: float, h: float, anchor: str = "left",
          gap: float = 1.05, space: float = 2.6, pad: float = 0.9) -> Tuple[float, float, float, float]:
    """Baseline at y (y down), cap height h, on the fine type pen; registers a
    halo so every other line is clipped around it."""
    sc = h / 6.0
    w = text_width(text, h, gap, space)
    left = x - (w if anchor == "right" else w / 2.0 if anchor == "center" else 0.0)
    cx = left
    lo_y, hi_y = 0.0, 6.0
    for ch in text:
        if ch == " ":
            cx += space * sc
            continue
        g, gx0, gx1, gy0, gy1 = _glyph_box(ch)
        lo_y, hi_y = min(lo_y, gy0), max(hi_y, gy1)
        for stroke in g:
            S.line([(cx + (gx - gx0) * sc, y - gy * sc) for gx, gy in stroke], TYPE, halo=False)
        cx += (gx1 - gx0) * sc + gap * sc
    box = (left - pad, y - hi_y * sc - pad, left + w + pad, y - lo_y * sc + pad)
    S.halos.append(box)
    return box


# ======================================================================
# geometry of the matrix
# ======================================================================
class Grid:
    """Key kx and query qy (token units, cell centres on integers) <-> mm."""

    def __init__(self, ya: float) -> None:
        self.ya = ya                        # y of query -1/2 (top of row 0)

    def x(self, kx: float) -> float:
        return X0 + (kx + 0.5) * PX

    def y(self, qy: float) -> float:
        return self.ya + (qy + 0.5) * PY

    def knife_region(self) -> HalfPlane:
        # inside (key <= query, cell-inclusive): kx <= qy + 1/2
        #   (x - X0)/PX - 1/2 - (y - ya)/PY + 1/2 - 1/2 <= 0
        return HalfPlane(1.0 / PX, -1.0 / PY, -X0 / PX + self.ya / PY - 0.5)

    def knife_x(self, y: float) -> float:
        qy = (y - self.ya) / PY - 0.5
        return self.x(qy + 0.5)

    def apex(self) -> Pt:
        return (self.x(-0.5), self.y(-1.0))


def _q_x(t: int) -> float:
    return XQ0 - t * QK_STEP


def _k_x(t: int) -> float:
    return XK0 + t * QK_STEP


# ======================================================================
# stations
# ======================================================================
def draw_qk(S: Sheet, M: Mech) -> Dict[str, float]:
    info = {}
    for fam, pen in (("Q", RED), ("K", BLUE)):
        C = M.cq if fam == "Q" else M.ck
        xs = [_q_x(t) if fam == "Q" else _k_x(t) for t in range(T)]
        base = ([(min(xs) - 9.0, Y_QK), (max(xs) + 8.0, Y_QK)] if fam == "Q"
                else [(min(xs) - 11.0, Y_QK), (max(xs) + 8.5, Y_QK)])   # 3 mm apart at x 94-97
        S.line(base, pen)
        F = Family()
        F.seed(base)
        curves = {t: _curve(C[t], xs[t], Y_QK, SIG_QK, S_QK) for t in range(T)}
        if fam == "Q":
            rank = [QI] + sorted((t for t in range(T) if t != QI), key=lambda t: -C[t][0])
        else:
            rank = sorted(range(T), key=lambda t: -abs(C[t][0]))   # the bells " itself" reads first
        dip, top = 0.0, 1e9
        for t in rank:
            F.add(curves[t])
            if curves[t]:
                dip = max([dip] + [p[1] - Y_QK for p in curves[t]])
                top = min([top] + [p[1] for p in curves[t]])
        F.draw(S, pen)
        info[fam + "_occ"] = F.occ
        info[fam + "_dip"] = dip
        info[fam + "_top"] = top
    return info


def draw_q_strands(S: Sheet, M: Mech, g_top: float, grid: Grid, F: np.ndarray, fx, fy,
                   occ: Optional[Occupancy] = None) -> Dict[str, float]:
    """Query i: down from its ruler tick, left along its turn line g_i, down its
    gutter lane, right along row i onto the left edge.  Outer strands (later
    tokens, further left) turn higher and run in outer lanes: they nest."""
    xl0 = X0 - 2.6
    r0 = 1.4
    out = {}
    for i in range(T):
        g = g_top + (T - 1 - i) * G
        lane = xl0 - i * G
        row = grid.y(i)
        corners = [(_q_x(i), Y_QK), (_q_x(i), g), (lane, g), (lane, row), (X0, row)]
        radii = [0, 1.4, r0 + i * G, 1.6, 0]
        pts = _fillet_path(corners, radii)
        if occ is not None:
            pts = _clear_start(pts, occ)
        if i == QI:
            # " itself" arrives on its row like every query; its row is then sliced
            xs = np.linspace(X0, grid.knife_x(row), 900)
            run: Poly = []
            thread: List[Poly] = []
            for x in xs:
                if _field_at(F, fx, fy, x, row) >= -FLOOR * SLOPE:
                    if len(run) >= 2:
                        thread.append(run)
                    run = []
                else:
                    run.append((float(x), row))
            if len(run) >= 2:
                thread.append(run)
            # the slice: row 12 drawn on the operations pen (black), silent
            # inside every eye it meets
            S.line(pts, RED)
            for r in thread:
                if _plen(r) >= 1.6:
                    S.line(r, BLACK)
            out["itself_thread_runs"] = len(thread)
        else:
            S.line(pts, RED)
    out["g_bottom"] = g_top + (T - 1) * G
    return out


def draw_k_strands(S: Sheet, M: Mech, h_top: float, grid: Grid,
                   occ: Optional[Occupancy] = None) -> None:
    """Key t: down from its ruler tick to its turn line h_t, left to its own
    column, down the column onto the knife at the diagonal cell (t, t).  Later
    keys turn lower: a nested staircase that never crosses itself."""
    for t in range(T):
        h = h_top + t * G
        col = grid.x(t)
        land = grid.y(t - 0.5) - KNIFE2 * math.hypot(PX, PY) / PX   # the knife's outer pass
        corners = [(_k_x(t), Y_QK), (_k_x(t), h), (col, h), (col, land)]
        pts = _fillet_path(corners, [0, 1.6, 1.6, 0])
        S.line(_clear_start(pts, occ) if occ is not None else pts, BLUE)


def _field(M: Mech, grid: Grid, step: float = 0.1):
    """F = upper envelope of equal-slope cones: one per cell (height = lift),
    plus one CAPSULE per pair of neighbouring attended cells whose eyes merge
    anyway (the envelope of the cones along the segment between them, heights
    interpolated).  Every piece has slope SLOPE, so level n and n+1 are exact
    offsets RING mm apart everywhere, the value at every cell centre is its
    own lift, and two merging eyes form one tapered body instead of pinching
    into a neck under the pen floor."""
    xs = np.arange(X0 - 1.0, DW + 0.01, step)
    ys = np.arange(grid.y(-1.2), grid.y(T - 1) + 14.0, step)
    F = np.full((len(ys), len(xs)), -1.0)

    def paint(cx0, cy0, cx1, cy1, l0, l1):
        rr = max(l0, l1) / SLOPE + 0.5
        ix = (xs >= min(cx0, cx1) - rr) & (xs <= max(cx0, cx1) + rr)
        iy = (ys >= min(cy0, cy1) - rr) & (ys <= max(cy0, cy1) + rr)
        X, Y = np.meshgrid(xs[ix], ys[iy])
        best = np.full(X.shape, -1.0)
        for t in (np.linspace(0.0, 1.0, 49) if (cx0, cy0) != (cx1, cy1) else [0.0]):
            cx, cy, lam = cx0 + t * (cx1 - cx0), cy0 + t * (cy1 - cy0), l0 + t * (l1 - l0)
            best = np.maximum(best, lam - SLOPE * np.hypot(X - cx, Y - cy))
        sub = np.ix_(iy, ix)
        F[sub] = np.maximum(F[sub], best)

    cells = [(i, j) for i in range(T) for j in range(i + 1) if M.lift[i, j] > 0.0]
    for i, j in cells:
        paint(grid.x(j), grid.y(i), grid.x(j), grid.y(i), M.lift[i, j], M.lift[i, j])
    pairs = 0
    for a_, (i, j) in enumerate(cells):
        for (k, l) in cells[a_ + 1:]:
            if abs(k - i) > 1 or abs(l - j) > 1:
                continue
            la, lb = M.lift[i, j], M.lift[k, l]
            d = math.hypot(grid.x(j) - grid.x(l), grid.y(i) - grid.y(k))
            if la > 0.0 and lb > 0.0 and la / SLOPE + lb / SLOPE > d:
                paint(grid.x(j), grid.y(i), grid.x(l), grid.y(k), la, lb)
                pairs += 1
    _field.pairs = pairs  # type: ignore[attr-defined]
    return F, xs, ys


def _field_at(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, x: float, y: float) -> float:
    if x < xs[0] or x > xs[-1] or y < ys[0] or y > ys[-1]:
        return -1.0
    i = int(round((y - ys[0]) / (ys[1] - ys[0])))
    j = int(round((x - xs[0]) / (xs[1] - xs[0])))
    return float(F[min(i, F.shape[0] - 1), min(j, F.shape[1] - 1)])


def draw_field(S: Sheet, M: Mech, grid: Grid, F, xs, ys) -> Dict[str, float]:
    """Contours of the cone envelope at n * LV (n = 0: the coast, uniform
    attention), clipped EXACTLY to the causal
    triangle, whose three sides are all drawn: every ring that stops, stops on
    ink."""
    import contourpy

    gen = contourpy.contour_generator(xs, ys, F, line_type="Separate")
    y_base = grid.y(T - 0.5)
    region = grid.knife_region() & HalfPlane(0.0, 1.0, -y_base)
    nlev = int(math.floor(M.lift.max() / LV))
    rings, dropped, lakes = 0, 0, 0
    pieces: List[Poly] = []
    ax, ay = grid.apex()
    edges = [((ax, ay), (grid.knife_x(y_base), y_base)), ((X0, y_base), (DW, y_base))]
    for n in range(0, nlev + 1):
        for line in gen.lines(max(n * LV, 1e-6)):
            pts = [tuple(p) for p in np.asarray(line)]
            if len(pts) < 3:
                continue
            closed = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1e-6
            if closed and _plen(pts) < 8.0:
                cxy = np.mean(np.asarray(pts), axis=0)
                if _field_at(F, xs, ys, cxy[0], cxy[1]) < n * LV:     # a lake, not an eye
                    lakes += 1
                    continue
            for run in clip(pts, region, keep="inside"):
                if len(run) < 2:
                    continue
                if _plen(run) < 3.0:
                    dropped += 1
                    continue
                pieces.extend(_cut_edge_grazes(run, edges))
    # any neck the capsules did not remove: the engine's pause-and-resume
    # silences the later (shorter) run where it comes within 0.78 mm
    fam = Family(sep=0.78, warmup=0, min_run=1.6)
    for run in sorted(pieces, key=lambda r: -_plen(r)):
        fam.add(run)
    fam.draw(S, BLACK)
    rings = len(fam.runs)
    silenced = fam.silenced
    ax, ay = grid.apex()
    kend = (grid.knife_x(y_base), y_base)
    S.line([(ax, ay), kend], BLACK)                 # the knife, apex to base
    nrm = np.array([PY, -PX]) / math.hypot(PX, PY)  # toward the masked future
    S.line([(ax + KNIFE2 * nrm[0], ay + KNIFE2 * nrm[1]),
            (kend[0] + KNIFE2 * nrm[0], kend[1] + KNIFE2 * nrm[1])], BLACK)   # its second pass
    S.line([kend, (X0, y_base)], BLACK)             # the base
    S.line([(X0, y_base), (ax, ay)], BLACK)         # key -1/2: the left edge
    return {"levels": nlev, "ring_strokes": rings, "dropped_under_3mm": dropped,
            "lakes": lakes, "neck_silenced_mm": silenced, "knife_end": kend, "y_base": y_base}


def _dist_seg(p: Pt, a: Pt, b: Pt) -> Tuple[float, np.ndarray]:
    A, B, P_ = np.array(a), np.array(b), np.array(p)
    d = B - A
    t = max(0.0, min(1.0, float((P_ - A) @ d / (d @ d))))
    return float(np.linalg.norm(P_ - (A + t * d))), d / np.linalg.norm(d)


def _cut_edge_grazes(run: Poly, edges, gap: float = 0.8, min_angle: float = 40.0) -> List[Poly]:
    """A ring may END on a drawn edge (the knife or the base) when it meets it
    at >= ``min_angle``.  Wherever it runs within ``gap`` mm of an edge more
    shallowly (grazing it, or ending on it at a glancing angle) that stretch
    is cut: two lines under 0.8 mm would ink as one wedge."""
    dense = resample_by_arclength([tuple(p) for p in run], step=0.15)
    n = len(dense)
    if n < 3:
        return []
    sn = math.sin(math.radians(min_angle))
    bad = np.zeros(n, bool)
    for k in range(n):
        q0 = dense[max(0, k - 3)]
        q1 = dense[min(n - 1, k + 3)]
        tv = np.array(q1) - np.array(q0)
        nt = float(np.linalg.norm(tv))
        if nt < 1e-9:
            continue
        for a, b in edges:
            dd, dv = _dist_seg(dense[k], a, b)
            if dd < gap and abs(float(dv[0] * tv[1] - dv[1] * tv[0])) / nt < sn:
                bad[k] = True
                break
    out: List[Poly] = []
    cur: Poly = []
    for k in range(n):
        if bad[k]:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
        else:
            cur.append(dense[k])
    if len(cur) >= 2:
        out.append(cur)
    return [r for r in out if _plen(r) >= 1.6]


def draw_drops_softmax(S: Sheet, M: Mech, grid: Grid, F, fx, fy) -> Dict[int, float]:
    """The five above-uniform keys of row 12 drop straight down their columns
    to their spike's apex; a drop passes UNDER any other eye it meets."""
    xs = [grid.x(j) for j in range(QI + 1)]
    S.line([(xs[0] - 6.0, Y_SM), (xs[-1] + 6.0, Y_SM)], BLACK)
    tops = {}
    for j, x in enumerate(xs):
        h = M.a[j] * H_SM
        tops[j] = Y_SM - h
        if h > 2 * TAIL:
            u = np.linspace(-3.4, 3.4, 70)
            y = Y_SM - h * np.exp(-0.5 * u * u)
            pts = [(x + uu * 1.15, yy) for uu, yy in zip(u, y) if Y_SM - yy > TAIL]
            if _plen(pts) >= 1.6:
                S.line(pts, BLACK)
    for j in M.named:
        x = xs[j]
        lam = M.lift[QI, j]
        y0 = grid.y(QI) + lam / SLOPE      # the eye's outer ring (ring 0, the coast)
        y1 = tops[j]
        ys = np.linspace(y0, y1, int((y1 - y0) / 0.1) + 2)
        run: Poly = []
        runs: List[Poly] = []
        for k, y in enumerate(ys):
            other = y > y0 + 0.6 and _field_at(F, fx, fy, x, y) >= -FLOOR * SLOPE
            if other:
                if len(run) >= 2:
                    runs.append(run)
                run = []
            else:
                run.append((x, float(y)))
        if len(run) >= 2:
            runs.append(run)
        for r in runs:
            if _plen(r) >= 1.6:
                S.line(r, BLACK)
    return tops


def draw_v(S: Sheet, M: Mech, grid: Grid) -> Dict[str, object]:
    base = [(4.0, Y_V), (DW - 3.0, Y_V)]
    S.line(base, OCHRE)
    F = Family()
    F.seed(base)
    curves = {j: _curve(M.cv[j], grid.x(j), Y_V, SIG_V, S_V) for j in range(QI + 1)}
    dip = 0.0
    for j in sorted(curves, key=lambda j: -M.a[j]):           # heaviest weight on top
        F.add(curves[j])
        if curves[j]:
            dip = max([dip] + [p[1] - Y_V for p in curves[j]])
    F.draw(S, OCHRE)
    for j in (13, 14):          # the future: " itself" cannot see these values
        x, r = grid.x(j), 0.9
        S.line([(x + r * math.cos(a), Y_V + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 25)], OCHRE)
    crest = {j: _curve_at(M.cv[j], grid.x(j), grid.x(j), Y_V, SIG_V, S_V) for j in range(QI + 1)}
    return {"dip": dip, "crest": crest}


def draw_v_drops(S: Sheet, M: Mech, grid: Grid, crest: Dict[int, float]) -> Dict[int, int]:
    amax = M.a.max()
    n = {}
    for j in M.named:
        x = grid.x(j)
        n[j] = S.dashed([(x, Y_SM), (x, crest[j])], OCHRE, duty=M.a[j] / amax, period=6.0)
    return n


def z_x(M: Mech, grid: Grid) -> float:
    """Z's centre: the attention-weighted mean key column."""
    return grid.x(float((M.a * np.arange(QI + 1)).sum()))


def draw_z(S: Sheet, M: Mech, grid: Grid) -> Dict[str, object]:
    """Six partial sums on one centre and one baseline, in V's rule and scale.
    Outermost (= R(z)) first and whole; each inner sum goes silent only where
    it runs within 0.85 mm of a sum outside it (pause-and-resume)."""
    xz = z_x(M, grid)
    xg = xz + GHOST_DX
    base = [(xz - 66.0, Y_Z), (xg + 17.0, Y_Z)]
    S.line(base, GREEN)
    F = Family(sep=0.85, warmup=0, min_run=2.0)
    F.seed(base)
    kept: Dict[int, List[Poly]] = {}
    for k in range(len(M.partials) - 1, -1, -1):
        n0 = len(F.runs)
        F.add(_curve(M.partials[k], xz, Y_Z, SIG_Z, S_Z, n=520))
        kept[k] = F.runs[n0:]
    F.draw(S, GREEN)
    # the ghost: R(z) at 1x, V's own scale, on the same baseline (dashed)
    S.dashed(_curve(M.cz, xg, Y_Z, SIG_V, S_V, n=240, tail=0.9), GREEN, duty=0.55, period=3.2)
    # nesting check: consecutive sums never cross (report the min gap, mm)
    u = np.linspace(-3.0, 3.0, 601)
    H = _hermite(MODES, u)
    gaps = [float(((M.partials[k + 1] - M.partials[k]) @ H).min() * S_Z)
            for k in range(len(M.partials) - 1)]
    return {"xz": xz, "xg": xg, "kept": kept, "nest_min_gap_mm": gaps}


def _y_on(runs: List[Poly], x: float) -> Optional[float]:
    for run in runs:
        for q in range(len(run) - 1):
            (xa, ya), (xb, yb) = run[q], run[q + 1]
            if (xa - x) * (xb - x) <= 0 and xa != xb:
                return ya + (x - xa) / (xb - xa) * (yb - ya)
    return None


def draw_vz(S: Sheet, M: Mech, grid: Grid, zinfo: Dict[str, object], vinfo) -> Dict[str, object]:
    """Every value with a visible weight pours into Z and ENDS ON the partial
    sum its term creates.  Landing x rises with the token index, so no two
    strands cross; each landing is at least 0.9 mm (vertically) from every
    other green curve."""
    amax = M.a.max()
    xz = zinfo["xz"]
    kept: Dict[int, List[Poly]] = zinfo["kept"]
    js = [j for j in range(QI + 1) if M.a[j] / amax >= STRAND_MIN]
    n = len(js)
    land: Dict[int, Pt] = {}
    prev_x = -1e9
    for r, j in enumerate(js):
        k = M.term_of[j]
        want = xz + (r - (n - 1) / 2.0) * LAND_STEP
        best, bc = None, 1e9
        for run in kept[k]:
            if _plen(run) < 2.5:
                continue
            xs_ = [p[0] for p in run]
            for x in np.arange(min(xs_) + 0.6, max(xs_) - 0.6, 0.1):
                if any(abs(x - q[0]) < 2.6 for q in land.values()):
                    continue
                y = _y_on([run], x)
                if y is None:
                    continue
                if any(o is not None and abs(o - y) < 0.9
                       for m in kept if m != k for o in [_y_on(kept[m], x)]):
                    continue
                c = abs(x - want) + (6.0 + 3.0 * (prev_x - x) if x < prev_x else 0.0)
                if c < bc:
                    best, bc = (float(x), float(y)), c
        if best is None:
            continue
        land[j] = best
        prev_x = max(prev_x, best[0])
    ndash = {}
    # one common arrival height above the whole nest: between Y_V and y_a the
    # strands are monotone curves with ordered ends (they cannot cross); below
    # it each drops vertically, >= 2.6 mm from its neighbours, onto its own sum
    ztop = min(p[1] for runs in kept.values() for r in runs for p in r)
    y_a = ztop - 2.5
    for j, (x1, y1) in land.items():
        x0 = grid.x(j)
        g = y_a - Y_V
        pts = _bez((x0, Y_V), (x0, Y_V + 0.45 * g), (x1, y_a - 0.55 * g), (x1, y_a), n=160)
        pts = pts + [(x1, y_a + t * (y1 - y_a)) for t in np.linspace(0.05, 1.0, 20)]
        ndash[j] = S.dashed(pts, OCHRE, duty=M.a[j] / amax, period=10.0)
    return {"land": land, "dashes": ndash, "js": js}


LAND_STEP = 5.5
GHOST_DX = 71.0
STRAND_MIN = 0.15   # a value under 0.15 of the top weight sends no strand (its term still enters +rest)



def draw_type(S: Sheet, M: Mech, grid: Grid, qk: Dict[str, float], zinfo, vz) -> None:
    """All type lives in ONE band at the foot (so the fine pen never crosses
    the sheet): the five attended keys where their strands leave V, Z = AV,
    the caption, and two small lines of provenance and rule."""
    side = {2: -1, 3: +1, 7: +1, 10: -1, 11: +1}
    for j in M.named:
        x = grid.x(j)
        sd = side.get(j, +1)
        label(S, M.tokens[j].strip(), x + sd * 1.4, Y_V + 5.2, 1.8,
              anchor="left" if sd > 0 else "right")
    xz = zinfo["xz"]
    label(S, "Z = AV", xz - 50.0, Y_Z - 11.0, 3.0, anchor="right")
    label(S, "×2.5", xz - 50.0, Y_Z - 6.2, 1.9, anchor="right")
    label(S, "×1", zinfo["xg"] + 8.5, Y_Z - 9.5, 1.9)
    order = M.named
    rest = 1.0 - sum(M.a[j] for j in order)
    terms = " + ".join(f"{M.a[j]:.2f}".lstrip("0") + " " + M.tokens[j].strip() for j in order)
    cap = f"itself = {terms} + " + f"{rest:.2f}".lstrip("0") + " rest"
    label(S, cap, DW / 2.0, Y_CAP, 2.1, anchor="center")
    line1 = ("GPT-2 small  L11 H8  reading 'The pen plotter drew a black hole while "
             "the transformer watched itself think.'")
    line2 = ("f(x) = Σₖ (c·eₖ) Hₖ(x/σ), Hermite k<3   Q,K: e₀ = q(itself)   V,Z: e₀ = z   "
             "ring n: A·(i+1) = 1.2ⁿ   itself·hole = 16.9/8 = 2.11")
    label(S, line1, DW / 2.0, Y_FOOT, 1.75, anchor="center", gap=0.95, space=2.3)
    label(S, line2, DW / 2.0, Y_FOOT + 4.3, 1.75, anchor="center", gap=0.95, space=2.3)


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
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        hit = any(not (max(xs) < b[0] or min(xs) > b[2] or max(ys) < b[1] or min(ys) > b[3])
                  for b in S.halos)
        if not hit:
            out.append((pen, pts))
            continue
        for run in clip(pts, region, keep="outside"):
            if _plen(run) >= 1.6:
                out.append((pen, run))
    return out


def _chain_order(polys: List[Poly], start: Pt) -> List[Poly]:
    """Greedy nearest END (either end; the stroke is reversed to suit) from the
    park point.  The pipeline's nearest-START pass reproduces this chain."""
    heads = np.array([p[0] for p in polys])
    tails = np.array([p[-1] for p in polys])
    alive = np.ones(len(polys), bool)
    pos = np.array(start)
    out: List[Poly] = []
    for _ in range(len(polys)):
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


def _pipeline_greedy(starts: np.ndarray, ends: np.ndarray, start: Pt = (0.0, 0.0)):
    """Exactly what ``postprocess.optimize_stroke_order`` will do to a layer:
    from the park point, repeatedly take the stroke whose START is nearest,
    never reversing.  Returns (order, hops)."""
    n = len(starts)
    alive = np.ones(n, bool)
    pos = np.asarray(start, float)
    order, hops = [], []
    for _ in range(n):
        d = np.hypot(starts[:, 0] - pos[0], starts[:, 1] - pos[1])
        d[~alive] = np.inf
        k = int(d.argmin())
        order.append(k)
        hops.append(float(d[k]))
        alive[k] = False
        pos = ends[k]
    return order, hops


def _cost(hops: List[float], cap: float) -> float:
    inner = hops[1:]                      # hops[0] is the layer's entry travel
    return sum(inner) + sum(1e4 + 100.0 * (h - cap) ** 2 for h in inner if h > cap)


def _order_layer(polys: List[Poly], cap: float = 55.0, passes: int = 4) -> List[Poly]:
    """Batch-friendly order that SURVIVES the pipeline.  Start from a greedy
    nearest-end chain (reversing strokes to suit), then flip stroke directions
    (a flip changes which end the pipeline's nearest-start pass sees) while the
    simulated pipeline travel improves, weighting every in-layer hop over
    ``cap`` mm heavily.  Deterministic: flips are tried in a fixed order."""
    polys = _chain_order(polys, (0.0, 0.0))
    flip = np.zeros(len(polys), bool)
    heads = np.array([p[0] for p in polys])
    tails = np.array([p[-1] for p in polys])

    def sim(fl):
        st = np.where(fl[:, None], tails, heads)
        en = np.where(fl[:, None], heads, tails)
        return _pipeline_greedy(st, en)

    order, hops = sim(flip)
    best = _cost(hops, cap)
    for _ in range(passes):
        improved = False
        # candidates: strokes on either side of the worst hops first, then all
        bad = [order[i] for i, h in enumerate(hops) if i > 0 and h > cap]
        bad += [order[i - 1] for i, h in enumerate(hops) if i > 0 and h > cap]
        cands = list(dict.fromkeys(bad + list(range(len(polys)))))
        if len(polys) > 260 and not bad:
            break
        for k in cands:
            flip[k] = ~flip[k]
            o2, h2 = sim(flip)
            c2 = _cost(h2, cap)
            if c2 < best - 1e-6:
                best, order, hops = c2, o2, h2
                improved = True
            else:
                flip[k] = ~flip[k]
        if not improved:
            break
    return [polys[k][::-1] if flip[k] else polys[k] for k in order]


def build(M: Optional[Mech] = None):
    M = M or Mech()
    S = Sheet()
    qk = draw_qk(S, M)
    g_top = Y_QK + max(qk["Q_dip"], qk["K_dip"]) + 2.0
    g_bottom = g_top + (T - 1) * G
    h_top = g_bottom + 2.0
    grid = Grid(ya=h_top + L0)
    F, fx, fy = _field(M, grid)
    qs = draw_q_strands(S, M, g_top, grid, F, fx, fy, qk["Q_occ"])
    draw_k_strands(S, M, h_top, grid, qk["K_occ"])
    st = draw_field(S, M, grid, F, fx, fy)
    tops = draw_drops_softmax(S, M, grid, F, fx, fy)
    vinfo = draw_v(S, M, grid)
    vd = draw_v_drops(S, M, grid, vinfo["crest"])
    zinfo = draw_z(S, M, grid)
    vz = draw_vz(S, M, grid, zinfo, vinfo)
    draw_type(S, M, grid, qk, zinfo, vz)
    st.update({"grid_ya": grid.ya, "g_top": g_top, "h_top": h_top, "qk": qk,
               "v_dip": vinfo["dip"], "vz": vz, "vdrops": vd, "xz": zinfo["xz"], "qs": qs})
    return S, M, grid, st, (F, fx, fy)


def superposition_iterate(rng: SeededRNG, bounds, colors: int = 6) -> List[GCodeCommand]:
    try:  # cream stock, hairline preview — never touches the gcode
        from promptplot.config import get_config

        viz = get_config().visualization
        viz.paper_color = "cream"
        viz.line_width = 0.5
    except Exception:  # pragma: no cover
        pass

    S, M, grid, stats, _ = build()
    x0, y0, x1, y1 = bounds
    k = min((x1 - x0) / DW, (y1 - y0) / DH)
    ox = x0 + ((x1 - x0) - DW * k) / 2.0
    oy = y1 - ((y1 - y0) - DH * k) / 2.0

    def P(p: Pt) -> Pt:
        return (ox + p[0] * k, oy - p[1] * k)

    polys: Dict[int, List[Poly]] = {}
    for pen, pts in _clip_halos(S):
        pen = pen if pen < colors else pen % max(1, colors)
        polys.setdefault(pen, []).append([P(p) for p in pts])
    out: List[GCodeCommand] = []
    for pen in sorted(polys):
        for pts in _order_layer(polys[pen]):
            out += _poly(pts, color=pen, f=1500)
    superposition_iterate.stats = stats  # type: ignore[attr-defined]
    superposition_iterate.report = M.report()  # type: ignore[attr-defined]
    return out


if __name__ == "__main__":
    print(Mech().report())
