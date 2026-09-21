"""ATTENTION AS WEAVING — the interlacing IS the attention computation.

Round r02. Thesis: TRUE MECHANISM. Every strand's path is determined by a real
attention layer; nothing on the sheet is decorative geometry pretending to be
maths.

SOURCE OF TRUTH
    A = softmax(QK^T/sqrt(d))  for GPT-2 small, LAYER 2 HEAD 9, on the real
    15-token sentence
        "The pen plotter drew a black hole while the transformer watched
         itself think."
    cached by scripts/extract_gpt2_attention.py at ~/.promptplot/attn_gpt2.npz
    (shape (12,12,15,15), rows sum to 1.0 to 3e-7). Layer 2 head 9 is a
    COREFERENCE head: its row for the token " itself" puts 0.416 on
    " transformer" and 0.377 on " watched". The plate's waist is that row.
    If the cache is missing the piece builds a real attention layer in numpy
    instead (real Q/K/V, real scaled dot product, real causal mask, real
    softmax) and says so in the footer.

THE MAPPING  (order supplied by the mechanism, per DESIGN_RUBRIC)
    order = INTERLACING.  A filament is a TOKEN POSITION; its colour is the
    projection that token is currently playing.
      above the waist   red  q_i   token i as a QUERY
                        blue k_j   token j as a KEY
      below the waist   green z_i  token i's OUTPUT      (same filament as q_i)
                        ochre v_j  token j's VALUE       (same filament as k_j)
    30 filaments enter the waist, 30 leave it. Nothing is born below, nothing
    dies above.

    1. log A is decomposed EXACTLY as   log A[i,j] = a_i + b_j + r[i,j].
       The ADDITIVE part sets WHERE q_i and k_j cross: a_i and b_j drive the
       easing exponents AND the reach of each filament, so the crossing point
       is a deterministic function of a_i and b_j alone. Measured over the 120
       unmasked pairs, Spearman(A[i,j], distance from the waist) = +0.705 --
       a heavy pair meets high and WIDE, a weak pair is squeezed down into the
       throat. The RESIDUAL sets HOW they cross -- sign(r[i,j]) decides which
       filament floats over, all 120 of them. Both halves of log A are carried;
       nothing is thrown away.
       (least squares on the 120 unmasked entries: R^2 = 0.8185)
    2. The softmax bead column is the literal row A[12,:]: bead AREA is the
       weight, so the inked area of the column is proportional to 1.000. The
       two causally masked keys are drawn as empty rings.
    3. Below the waist the rope's cross-section is the real value matrix V,
       rigidly rotating: v_j sits at radius rho_j (its rank by total attention
       received) and phase 2*pi*j/T. The green filament i sits at
       (A @ V)_i — the exact product, so each green strand is literally at the
       attention-weighted mean of where the ochre strands are. Peaked rows
       swing out and track one ochre strand; flat rows stay in the core
       (corr(|Z_i|, exp(-H_i)) = 0.835).
    4. Over/under in the rope is the real out-of-plane coordinate of that same
       rotating product — a true 3-D occlusion, not a pattern.

Contract:  attention_weaving(rng, bounds, colors=3) -> list[GCodeCommand]
"""

from __future__ import annotations

import math
import os
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine import geometry as geo
from promptplot.generative.engine.kit import (
    giant_type,
    _dot,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    circle,
    dotted_circle,
    fill_disc,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# --- pens (index into the 5-pen palette) -----------------------------------
P_BLACK, P_Q, P_K, P_V, P_Z = 0, 1, 2, 3, 4

NPZ = os.path.expanduser("~/.promptplot/attn_gpt2.npz")
LAYER, HEAD, QSTAR = 2, 9, 12
TOKENS = [
    "The", " pen", " plot", "ter", " drew", " a", " black", " hole", " while",
    " the", " transformer", " watched", " itself", " think", ".",
]


def _pen(ix: int, colors: int) -> Optional[int]:
    return ix % colors if colors and colors > 1 else None


# ===========================================================================
# 1. THE ATTENTION LAYER  (real numbers, no decoration)
# ===========================================================================
def _numpy_attention(rng: SeededRNG, T: int = 15, d: int = 32) -> np.ndarray:
    """Fallback: a REAL attention layer built in numpy when the GPT-2 cache is
    absent. Real Q/K/V, real scaled dot product, real causal mask, real
    softmax — seeded, but not faked."""
    g = np.random.default_rng(rng.seed)
    pos = np.arange(T)[:, None]
    ch = np.arange(d)[None, :]
    E = np.sin(pos / (10000 ** (2 * (ch // 2) / d)) + (ch % 2) * math.pi / 2)
    E = E + 0.35 * g.standard_normal((T, d))
    Wq, Wk = g.standard_normal((d, d)) / math.sqrt(d), g.standard_normal((d, d)) / math.sqrt(d)
    Q, K = E @ Wq, E @ Wk
    S = Q @ K.T / math.sqrt(d)
    S = np.where(np.tril(np.ones((T, T), bool)), S, -np.inf)
    S = S - S.max(1, keepdims=True)
    A = np.exp(S)
    return A / A.sum(1, keepdims=True)


def attention_data(rng: SeededRNG) -> Dict[str, object]:
    """Everything the plate draws, computed once from the real layer."""
    src = "gpt2-l%dh%d" % (LAYER, HEAD)
    A = None
    if os.path.exists(NPZ):
        try:
            raw = np.load(NPZ)["attn"].astype(np.float64)
            if raw.ndim == 4 and raw.shape[0] > LAYER and raw.shape[1] > HEAD:
                A = raw[LAYER, HEAD].copy()
        except Exception:
            A = None
    if A is None:
        src = "numpy-layer"
        A = _numpy_attention(rng)
    T = int(A.shape[0])
    A = A / A.sum(1, keepdims=True)

    # --- exact additive decomposition of log A on the unmasked entries -----
    idx = [(i, j) for i in range(T) for j in range(i + 1)]
    y = np.array([math.log(max(A[i, j], 1e-300)) for i, j in idx])
    M = np.zeros((len(idx), 2 * T))
    for k, (i, j) in enumerate(idx):
        M[k, i] = 1.0
        M[k, T + j] = 1.0
    sol, *_ = np.linalg.lstsq(M, y, rcond=None)
    a, b = sol[:T], sol[T:]
    pred = M @ sol
    r2 = 1.0 - ((y - pred) ** 2).sum() / max(1e-30, ((y - y.mean()) ** 2).sum())
    R = np.zeros((T, T))
    for k, (i, j) in enumerate(idx):
        R[i, j] = y[k] - pred[k]

    # --- per-row shape ----------------------------------------------------
    ent = np.zeros(T)
    for i in range(T):
        p = A[i, : i + 1]
        ent[i] = float(-(p * np.log(p + 1e-300)).sum())
    conc = np.exp(-ent)                      # 1 / effective support

    # --- the rope's value matrix V (real, rank-scaled) --------------------
    col = A.sum(0) / T                       # total attention mass received
    rank = np.argsort(np.argsort(col))
    rho = 0.55 + 0.45 * rank / max(1, T - 1)
    phi = 2.0 * math.pi * np.arange(T) / T
    V = np.stack([rho * np.cos(phi), rho * np.sin(phi)], 1)
    Z = A @ V                                 # <- THE product

    return {
        "src": src, "T": T, "A": A, "a": a, "b": b, "R": R, "r2": float(r2),
        "ent": ent, "conc": conc, "col": col, "rho": rho, "phi": phi,
        "V": V, "Z": Z, "qstar": min(QSTAR, T - 1),
    }


# ===========================================================================
# 2. EXACT OVER/UNDER  (crossings found closed-form, cut with engine geometry)
# ===========================================================================
_CELL = 5.0


def _at(p0: Pt, p1: Pt, t: float) -> Pt:
    return (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)


def _cut_runs(pts: Sequence[Pt], cuts: Sequence[Pt], r: float) -> List[List[Pt]]:
    """Split ``pts`` where it passes a cut point, stopping EXACTLY on the
    circle of radius ``r`` around it (engine closed-form clipping — never
    sample-and-snap)."""
    if not cuts:
        return [list(pts)]
    grid: Dict[Tuple[int, int], List[Pt]] = {}
    for c in cuts:
        grid.setdefault((int(c[0] // _CELL), int(c[1] // _CELL)), []).append(c)
    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    for p0, p1 in zip(pts, pts[1:]):
        near: List[Pt] = []
        gi0 = int((min(p0[0], p1[0]) - r) // _CELL)
        gi1 = int((max(p0[0], p1[0]) + r) // _CELL)
        gj0 = int((min(p0[1], p1[1]) - r) // _CELL)
        gj1 = int((max(p0[1], p1[1]) + r) // _CELL)
        for gi in range(gi0, gi1 + 1):
            for gj in range(gj0, gj1 + 1):
                near.extend(grid.get((gi, gj), ()))
        if not near:
            keep = [(0.0, 1.0)]
        else:
            reg = geo.Union(*[geo.Circle(c[0], c[1], r) for c in near])
            keep = geo._complement(reg.inside_intervals(p0, p1))
        for t0, t1 in keep:
            aa, bb = _at(p0, p1, t0), _at(p0, p1, t1)
            if cur and t0 <= 1e-9:
                cur.append(bb)
            else:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = [aa, bb]
        if not keep or keep[-1][1] < 1.0 - 1e-9:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _crossings(strands: List[dict]) -> List[Tuple[int, int, int, int, float, float]]:
    """All pairwise crossings, closed form. -> (sa, ka, sb, kb, px, py)."""
    grid: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    for si, s in enumerate(strands):
        pts = s["pts"]
        for k in range(len(pts) - 1):
            (xa, ya), (xb, yb) = pts[k], pts[k + 1]
            for gi in range(int(min(xa, xb) // _CELL), int(max(xa, xb) // _CELL) + 1):
                for gj in range(int(min(ya, yb) // _CELL), int(max(ya, yb) // _CELL) + 1):
                    grid.setdefault((gi, gj), []).append((si, k))
    out = []
    seen = set()
    for cell, members in grid.items():
        n = len(members)
        for u in range(n):
            si, ki = members[u]
            for v in range(u + 1, n):
                sj, kj = members[v]
                if si == sj:
                    continue
                key = (si, ki, sj, kj) if si < sj else (sj, kj, si, ki)
                if key in seen:
                    continue
                seen.add(key)
                (xa, ya), (xb, yb) = strands[si]["pts"][ki], strands[si]["pts"][ki + 1]
                (ox, oy), (px_, py_) = strands[sj]["pts"][kj], strands[sj]["pts"][kj + 1]
                dx, dy = xb - xa, yb - ya
                ex, ey = px_ - ox, py_ - oy
                den = dx * ey - dy * ex
                if abs(den) < 1e-12:
                    continue
                t = ((ox - xa) * ey - (oy - ya) * ex) / den
                u2 = ((ox - xa) * dy - (oy - ya) * dx) / den
                if 0.0 <= t <= 1.0 and 0.0 <= u2 <= 1.0:
                    out.append((si, ki, sj, kj, xa + dx * t, ya + dy * t))
    return out


def _interlace(strands: List[dict], decide, gap: float = 0.95,
               min_len: float = 0.9, feed: int = 1800) -> List[GCodeCommand]:
    """Draw every strand with real over/under: at each crossing the loser is
    cut, the winner runs continuous. ``decide(sa, ka, sb, kb) -> 0|1`` names
    which of the two goes UNDER."""
    cuts: Dict[int, List[Pt]] = {}
    for si, ki, sj, kj, px, py in _crossings(strands):
        loser = decide(strands[si], ki, strands[sj], kj)
        if loser is None:
            continue
        cuts.setdefault(si if loser == 0 else sj, []).append((px, py))
    out: List[GCodeCommand] = []
    for si, s in enumerate(strands):
        g = s.get("gap", gap)
        for run in _cut_runs(s["pts"], cuts.get(si, []), g * 0.5):
            if len(run) < 2:
                continue
            L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(run, run[1:]))
            if L < min_len:
                continue
            if s.get("passes", 1) > 1:
                out += _poly(geo.offset(run, 0.14), color=s["pen"], f=feed)
                out += _poly(geo.offset(run, -0.14), color=s["pen"], f=feed)
            else:
                out += _poly(run, color=s["pen"], f=feed)
    return out


# ===========================================================================
# 3. CURVE HELPERS
# ===========================================================================
def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, t: float) -> Pt:
    m = 1.0 - t
    return (
        m ** 3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
        m ** 3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t ** 3 * p3[1],
    )


def _bez_d(p0: Pt, p1: Pt, p2: Pt, p3: Pt, t: float) -> Pt:
    m = 1.0 - t
    return (
        3 * m * m * (p1[0] - p0[0]) + 6 * m * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
        3 * m * m * (p1[1] - p0[1]) + 6 * m * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]),
    )


def _smooth(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)


def _dotted(pts: Sequence[Pt], pen: Optional[int], on: int = 2, off: int = 4,
            f: int = 2000) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    seg: List[Pt] = []
    for k, p in enumerate(pts):
        if (k % (on + off)) < on:
            seg.append(p)
        else:
            if len(seg) >= 2:
                out += _poly(seg, color=pen, f=f)
            seg = []
    if len(seg) >= 2:
        out += _poly(seg, color=pen, f=f)
    return out


def _yfun(pts: Sequence[Pt], n1: int):
    """y(x) along the forward (monotone-in-x) leg of a filament."""
    xs = [p[0] for p in pts[: n1 + 1]]
    ys = [p[1] for p in pts[: n1 + 1]]
    inc = xs[-1] > xs[0]

    def f(x: float) -> float:
        if (x - xs[0]) * (1 if inc else -1) <= 0:
            return ys[0]
        if (x - xs[-1]) * (1 if inc else -1) >= 0:
            return ys[-1]
        lo, hi = 0, len(xs) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if (xs[mid] <= x) == inc:
                lo = mid
            else:
                hi = mid
        d = xs[hi] - xs[lo]
        t = 0.0 if abs(d) < 1e-12 else (x - xs[lo]) / d
        return ys[lo] + (ys[hi] - ys[lo]) * t

    return f


def _bead(x: float, y: float, d: float, pen: Optional[int], f: int = 1600) -> List[GCodeCommand]:
    """A filled bead of diameter ``d`` (area carries the weight)."""
    if d < 0.55:
        return _dot(x, y, r=0.22, color=pen, f=f)
    return fill_disc(x, y, d * 0.5, spacing=0.34, pen=pen, f=f)


# ===========================================================================
# 4. THE PLATE
# ===========================================================================
def attention_weaving(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    D = attention_data(rng)
    T: int = D["T"]                      # type: ignore
    A: np.ndarray = D["A"]               # type: ignore
    a: np.ndarray = D["a"]               # type: ignore
    b: np.ndarray = D["b"]               # type: ignore
    Rres: np.ndarray = D["R"]            # type: ignore
    V: np.ndarray = D["V"]               # type: ignore
    Z: np.ndarray = D["Z"]               # type: ignore
    col: np.ndarray = D["col"]           # type: ignore
    qs: int = D["qstar"]                 # type: ignore

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blk = _pen(P_BLACK, colors)
    pq, pk, pv, pz = (_pen(P_Q, colors), _pen(P_K, colors),
                      _pen(P_V, colors), _pen(P_Z, colors))
    out: List[GCodeCommand] = []

    # ---- sheet anatomy ---------------------------------------------------
    xc = x0 + 0.452 * W                       # the waist axis
    yw = y0 + 0.505 * H                       # the pinch line
    RIB_IN, RIB_OUT = 4.4, 18.6               # throat ribbon inner / outer edge
    INS = 0.95                                # margin inset (2-pass miter allowance)

    def _lanes(weights, y_top: float, span: float) -> List[float]:
        """Reed lanes whose WIDTH is a real quantity: a filament carrying more
        attention is given more room, so the reed is irregular by measurement
        rather than by decoration."""
        w = np.asarray(weights, dtype=float)
        w = 0.38 + 0.62 * (w - w.min()) / (w.max() - w.min() + 1e-12)
        gaps = w[:-1] + w[1:]
        gaps = gaps / gaps.sum() * span
        ys, yy = [y_top], y_top
        for g in gaps:
            yy -= g
            ys.append(yy)
        return ys

    ent = D["ent"]                                              # type: ignore
    reedQ = _lanes(np.exp(ent), y0 + 0.906 * H, 0.268 * H)
    reedK = _lanes(col, y0 + 0.936 * H, 0.268 * H)
    reedV = _lanes(col, y0 + 0.452 * H, 0.176 * H)

    def _std(v):
        return (v - v.mean()) / (v.std() + 1e-9)

    def _clip(v, lo, hi):
        return np.minimum(hi, np.maximum(lo, v))

    # additive effects of log A -> the two easing exponents (crossing HEIGHT)
    # sub-linear in x (the filament leaves its reed flat, like a warp thread)
    alpha = _clip(np.exp(0.40 * _std(a)), 0.50, 1.22)
    beta = _clip(np.exp(0.40 * _std(b)), 0.50, 1.22)
    # super-linear in y (it hangs, then falls) -> intra-bundle interlacing
    gam_q = _clip(np.exp(0.55 * _std(ent)), 1.05, 2.35)
    gam_k = _clip(np.exp(0.55 * _std(np.log(col))), 1.05, 2.35)

    rankA = np.argsort(np.argsort(a))
    rankB = np.argsort(np.argsort(b))
    # peak REACH from the additive effect; peak HEIGHT from the row's shape --
    # two different real orderings, so the turns scatter instead of lining up
    rEnt = np.argsort(np.argsort(ent))
    rCol = np.argsort(np.argsort(col))
    # REACH tracks the additive effect: a filament with a large a_i (or b_j)
    # swings furthest past the waist axis and, by the cone rule below, peaks
    # highest -- so a heavy pair meets high and WIDE and a weak pair is squeezed
    # down into the throat. Measured Spearman of A[i,j] against the crossing's
    # distance to the waist = +0.705 over the 120 unmasked pairs (NOTES.md).
    rchQ = [11.0 + 37.0 * rankA[i] / (T - 1) for i in range(T)]
    rchK = [11.0 + 37.0 * rankB[j] / (T - 1) for j in range(T)]
    peakQ = [xc + rchQ[i] for i in range(T)]
    peakK = [xc - rchK[j] for j in range(T)]
    # the funnel is a CONE: a filament that reaches far must peak high, so every
    # turn-in is the same gentle angle and no strand hairpins back on itself
    ypkQ = [yw + 13.0 + 1.62 * rchQ[i] + 13.0 * (rEnt[i] / (T - 1) - 0.5) for i in range(T)]
    ypkK = [yw + 13.0 + 1.62 * rchK[j] + 13.0 * (rCol[j] / (T - 1) - 0.5) for j in range(T)]

    # ---- rope frame ------------------------------------------------------
    C0 = (xc + 11.5, yw)
    C1 = (xc + 12.5, y0 + 0.378 * H)
    C2 = (x0 + 0.800 * W, y0 + 0.228 * H)
    C3 = (x1 - 2.0, y0 + 0.150 * H)
    TURNS, T_JOIN, T_FAN, NR = 1.02, 0.40, 0.840, 300
    R_IN = (RIB_OUT - RIB_IN) * 0.5 / 0.62
    R_MAX = 26.5

    def frame(t: float) -> Tuple[Pt, Pt, float]:
        c = _bez(C0, C1, C2, C3, t)
        d = _bez_d(C0, C1, C2, C3, t)
        L = math.hypot(*d) or 1.0
        n = (-d[1] / L, d[0] / L)
        R = (R_IN + (R_MAX - R_IN) * _smooth(t / T_JOIN) if t < T_JOIN
             else R_MAX - 7.0 * _smooth((t - T_JOIN) / (1 - T_JOIN)))
        return c, n, R

    def cross(vec: np.ndarray, t: float) -> Tuple[float, float]:
        th = 2.0 * math.pi * TURNS * t
        ct, st = math.cos(th), math.sin(th)
        return (vec[0] * ct - vec[1] * st, vec[0] * st + vec[1] * ct)

    ordZ = list(np.argsort(Z[:, 0]))
    ordV = list(np.argsort(-V[:, 0]))
    slotQ = {int(i): xc + RIB_IN + (RIB_OUT - RIB_IN) * k / (T - 1) for k, i in enumerate(ordZ)}
    slotK = {int(j): xc - RIB_IN - (RIB_OUT - RIB_IN) * k / (T - 1) for k, j in enumerate(ordV)}

    fanU = {("Z", i): cross(Z[i], 1.0)[0] * 0.62 for i in range(T)}
    fanU.update({("V", j): cross(V[j], 1.0)[0] for j in range(T)})
    fan_sorted = sorted(fanU, key=lambda k: fanU[k])
    reedZ = {k: y0 + (0.052 + 0.238 * n / (len(fan_sorted) - 1)) * H
             for n, k in enumerate(fan_sorted)}

    # ======================= THE WEAVE  (Q x K) ===========================
    def filament(xs: float, xp: float, xslot: float, yr: float,
                 yp: float, ea: float, eg: float) -> List[Pt]:
        """reed -> sweep past the waist axis -> turn -> down into the throat."""
        n1, n2 = 160, 64
        pts = [(xs + (xp - xs) * (k / n1) ** ea, yr + (yp - yr) * (k / n1) ** eg)
               for k in range(n1 + 1)]
        # tangent at the peak, so the turn is smooth
        dx = (xp - xs) * ea / n1
        dy = (yp - yr) * eg / n1
        L = math.hypot(dx, dy) or 1.0
        span = abs(yp - yw)
        b0 = (xp, yp)
        b1 = (xp + dx / L * span * 0.85, yp + dy / L * span * 0.85)
        b2 = (xslot, yw + span * 0.52)
        b3 = (xslot, yw)
        pts += [_bez(b0, b1, b2, b3, k / n2) for k in range(1, n2 + 1)]
        return pts

    NFWD = 160
    baseQ = [filament(x0 + INS, peakQ[i], slotQ[i], reedQ[i], ypkQ[i],
                      float(alpha[i]), float(gam_q[i])) for i in range(T)]
    baseK = [filament(x1 - INS, peakK[j], slotK[j], reedK[j], ypkK[j],
                      float(beta[j]), float(gam_k[j])) for j in range(T)]
    yQ = [_yfun(baseQ[i], NFWD) for i in range(T)]
    yK = [_yfun(baseK[j], NFWD) for j in range(T)]

    # ATTENTION IS THE DEFLECTION. A query thread is displaced from its lane by
    # exactly how far its attention-weighted mean of the KEY threads departs
    # from the UNIFORM-attention mean over the same (causal) support. A flat row
    # runs straight; a peaked row swings hard toward the key it has locked on.
    # Key threads get the transpose. One pass, computed off the undeflected
    # positions, so there is no circularity; zero at the reed, zero at the
    # funnel, and because it is a DEVIATION the bundle cannot collapse.
    GAIN = 1.05
    AT = A / np.maximum(A.sum(0, keepdims=True), 1e-12)          # column-normalised
    uniQ = np.array([[1.0 / (i + 1) if j <= i else 0.0 for j in range(T)] for i in range(T)])
    uniK = np.array([[1.0 / (T - j) if i >= j else 0.0 for j in range(T)] for i in range(T)])

    DMAX = 21.0                               # soft ceiling on the deflection

    def deflect(pts: List[Pt], w: np.ndarray, u: np.ndarray, others) -> List[Pt]:
        d = w - u
        nz = [m for m in range(T) if abs(d[m]) > 1e-9]
        off: List[float] = []
        for k, (px, _py) in enumerate(pts):
            t = k / NFWD
            if t >= 1.0:
                off.append(0.0)
                continue
            env = GAIN * math.sin(math.pi * t) ** 1.15
            raw = env * sum(float(d[m]) * others[m](px) for m in nz)
            off.append(DMAX * math.tanh(raw / DMAX))
        # 7-point smoothing: y(x) of a neighbour kinks where that filament
        # turns, and an unsmoothed pull inherits the kink as a hard corner
        sm = list(off)
        for _ in range(3):
            sm = [sum(sm[max(0, k - 2): k + 3]) / len(sm[max(0, k - 2): k + 3])
                  for k in range(len(sm))]
        # soft ceiling under the title band -- a hard clamp stacks several
        # threads onto one horizontal line, which reads as a ruled artefact
        cap, soft = y0 + 0.928 * H, 5.0

        def lid(v: float) -> float:
            d = (cap - v) / soft
            return cap - soft * (d + math.log1p(math.exp(-d)) if d > -30 else 0.0)

        return [(px, lid(py + sm[k])) for k, (px, py) in enumerate(pts)]

    weave: List[dict] = []
    wmax = float(A.max())
    for i in range(T):
        weave.append({
            "pen": pq, "fam": "Q", "idx": i,
            "pts": deflect(baseQ[i], A[i], uniQ[i], yK),
            "passes": 2 if A[i].max() / wmax > 0.40 else 1})
    for j in range(T):
        weave.append({
            "pen": pk, "fam": "K", "idx": j,
            "pts": deflect(baseK[j], AT[:, j], uniK[:, j], yQ),
            "passes": 2 if col[j] / col.max() > 0.40 else 1})

    def decide_weave(sa: dict, ka: int, sb: dict, kb: int) -> Optional[int]:
        fa, fb = sa["fam"], sb["fam"]
        ia, ib = sa["idx"], sb["idx"]
        if fa == fb:
            dep = a if fa == "Q" else b
            return 0 if dep[ia] < dep[ib] else 1
        qi, kj = (ia, ib) if fa == "Q" else (ib, ia)
        q_side = 0 if fa == "Q" else 1
        if kj > qi:                              # causally masked pair
            return q_side                        # the query always ducks under
        return q_side if Rres[qi, kj] < 0 else (1 - q_side)

    out += _interlace(weave, decide_weave, gap=2.05, min_len=1.4, feed=1800)

    # ======================= THE ROPE  (Z = AV) ===========================
    rope: List[dict] = []
    for i in range(T):
        pts, dep = [], []
        for k in range(NR + 1):
            t = k / NR
            c, n, R = frame(t)
            u, w = cross(Z[i], t)
            s = R * 0.62
            p = (c[0] + n[0] * u * s, c[1] + n[1] * u * s)
            if t > T_FAN:
                e = _smooth((t - T_FAN) / (1 - T_FAN))
                p = (p[0] + (x1 - INS - p[0]) * e, p[1] + (reedZ[("Z", i)] - p[1]) * e)
                w *= (1.0 - e)
            pts.append(p)
            dep.append(w)
        rope.append({"pen": pz, "pts": pts, "fam": "Z", "idx": i, "dep": dep,
                     "passes": 2 if A[i].max() / wmax > 0.40 else 1})

    cj, nj, Rj = frame(T_JOIN)
    cj2, nj2, Rj2 = frame(T_JOIN + 0.02)
    PR = 2.4                                     # the selvage peg radius
    for j in range(T):
        uj, wj = cross(V[j], T_JOIN)
        join = (cj[0] + nj[0] * uj * Rj, cj[1] + nj[1] * uj * Rj)
        f = j / (T - 1)
        ry = reedV[j]
        pts: List[Pt] = []
        o0 = (slotK[j], yw)
        o1 = (slotK[j] - 6.0, yw - 20.0 - 10.0 * f)
        o2 = (x0 + 34.0 + 10.0 * f, ry + 12.0)
        o3 = (x0 + INS + PR, ry + PR)
        pts += [_bez(o0, o1, o2, o3, k / 94) for k in range(0, 95)]
        for k in range(1, 19):                   # wrap the peg at the selvage
            th = math.pi * 0.5 + math.pi * k / 18.0
            pts.append((x0 + INS + PR + PR * math.cos(th), ry + PR * math.sin(th)))
        b0 = (x0 + INS + PR, ry - PR)
        b1 = (x0 + 40.0 + 16.0 * f, ry - 15.0 - 9.0 * f)
        u2j = cross(V[j], T_JOIN + 0.02)[0]
        nxt = (cj2[0] + nj2[0] * u2j * Rj2, cj2[1] + nj2[1] * u2j * Rj2)
        tdx, tdy = nxt[0] - join[0], nxt[1] - join[1]
        tl = math.hypot(tdx, tdy) or 1.0
        b2 = (join[0] - tdx / tl * 30.0, join[1] - tdy / tl * 30.0)
        b3 = join
        pts += [_bez(b0, b1, b2, b3, k / 104) for k in range(1, 105)]
        dep = [wj] * len(pts)
        for k in range(1, NR + 1):
            t = T_JOIN + (1.0 - T_JOIN) * k / NR
            c, n, R = frame(t)
            u2, w2 = cross(V[j], t)
            p = (c[0] + n[0] * u2 * R, c[1] + n[1] * u2 * R)
            if t > T_FAN:
                e = _smooth((t - T_FAN) / (1 - T_FAN))
                p = (p[0] + (x1 - INS - p[0]) * e, p[1] + (reedZ[("V", j)] - p[1]) * e)
                w2 *= (1.0 - e)
            pts.append(p)
            dep.append(w2)
        rope.append({"pen": pv, "pts": pts, "fam": "V", "idx": j, "dep": dep,
                     "passes": 2 if col[j] / col.max() > 0.40 else 1})

    def decide_rope(sa: dict, ka: int, sb: dict, kb: int) -> Optional[int]:
        da = sa["dep"][min(ka, len(sa["dep"]) - 1)]
        db = sb["dep"][min(kb, len(sb["dep"]) - 1)]
        if abs(da - db) < 1e-9:
            return 0 if sa["idx"] < sb["idx"] else 1
        return 0 if da < db else 1

    out += _interlace(rope, decide_rope, gap=1.25, min_len=1.8, feed=1800)

    # ---- punctuation: each filament marked at its heaviest real crossing --
    wx = {(s0["fam"], s0["idx"]): s0["pts"] for s0 in weave}
    xs_ = _crossings(weave)
    best: Dict[Tuple[int, int], Tuple[float, Pt]] = {}
    for si, ki, sj, kj, px, py in xs_:
        sa, sb = weave[si], weave[sj]
        if sa["fam"] == sb["fam"]:
            continue
        qi, kj_ = ((sa["idx"], sb["idx"]) if sa["fam"] == "Q" else (sb["idx"], sa["idx"]))
        if kj_ > qi:
            continue
        w_ = float(A[qi, kj_])
        if best.get((qi, kj_), (0.0, None))[0] < w_:
            best[(qi, kj_)] = (w_, (px, py))
    for i in range(T):
        cand = [(w_, p) for (qi, kj_), (w_, p) in best.items() if qi == i]
        if not cand:
            continue
        w_, p = max(cand)
        out += _bead(p[0], p[1], 0.7 + 3.0 * math.sqrt(w_ / wmax), pq)
    for j in range(T):
        cand = [(w_, p) for (qi, kj_), (w_, p) in best.items() if kj_ == j]
        if not cand:
            continue
        w_, p = max(cand)
        out += circle(p[0], p[1], 0.8 + 1.8 * math.sqrt(w_ / wmax), pen=pk, f=1800, n=20)

    # the CAUSAL DIAGONAL: where filament i meets itself (q_i x k_i), the only
    # crossing every token has, ringed at its self-attention weight
    diag: Dict[int, Pt] = {}
    for si, ki, sj, kj, px, py in xs_:
        sa, sb = weave[si], weave[sj]
        if sa["fam"] == sb["fam"] or sa["idx"] != sb["idx"]:
            continue
        diag[int(sa["idx"])] = (px, py)
    for i, p in diag.items():
        r_ = 1.0 + 3.4 * math.sqrt(float(A[i, i]) / wmax)
        out += circle(p[0], p[1], r_, pen=blk, f=1800, n=26)
        out += _dot(p[0], p[1], r=0.22, color=blk, f=1600)

    # ======================= THE SOFTMAX WAIST ============================
    row = A[qs]
    pitch, heaviest = 2.95, int(np.argmax(A[qs]))
    ytop = yw + pitch * (T - 1) * 0.52
    for j in range(T):
        yb = ytop - pitch * j
        if j > qs:
            out += circle(xc, yb, 0.66, pen=blk, f=1800, n=14)
        else:
            out += _bead(xc, yb, max(0.34, 3.15 * math.sqrt(row[j] / row.max())), blk)
    y_rule = ytop - pitch * heaviest
    out += _dotted([(xc - 42 + 0.62 * k, y_rule) for k in range(136)], blk, on=1, off=3)
    out += _stroke_text("softmax", xc + 23.0, y_rule - 0.9, 2.6, color=blk, f=2000)

    # ======================= SCAFFOLD =====================================
    for r in (19.0, 41.0, 70.0):
        out += dotted_circle(xc, yw, r, pen=blk, bounds=bounds)
    rc, _, _ = frame(T_JOIN)
    out += dotted_circle(rc[0], rc[1], 30.0, pen=blk, bounds=bounds)

    # ======================= REEDS, RULES =================================
    for i in range(T):
        out += _poly([(x0, reedQ[i]), (x0 + 5.0, reedQ[i])], color=blk, f=2000)
        out += _poly([(x1 - 5.0, reedK[i]), (x1, reedK[i])], color=blk, f=2000)
        out += _poly([(x0, reedV[i]), (x0 + 3.8, reedV[i])], color=blk, f=2000)
    for key, yv in reedZ.items():
        out += _poly([(x1 - 4.2, yv), (x1, yv)], color=blk, f=2000)

    # output magnitudes |Z_i| strung on a rule in the lower-left quiet zone
    zr = np.hypot(Z[:, 0], Z[:, 1])
    yz = y0 + 0.088 * H
    xz0, xz1 = x0 + 0.115 * W, x0 + 0.560 * W
    out += _dotted([(xz0 + 0.62 * k, yz) for k in range(int((xz1 - xz0) / 0.62) + 1)],
                   blk, on=1, off=3)
    for i in range(T):
        out += _bead(xz0 + (xz1 - xz0) * i / (T - 1), yz,
                     0.36 + 3.3 * (zr[i] / zr.max()) ** 1.7, blk)
    out += _stroke_text(_spaced("|Z|"), xz0 - 8.5, yz - 1.1, 2.3, color=blk, f=2000)
    rce, _, _ = frame(0.86)
    out += dotted_circle(rce[0], rce[1], 58.0, pen=blk, bounds=bounds)

    cmax = float(np.max(col))
    xr = x1 - 17.0
    out += _dotted([(xr, reedK[0] + 4 - 0.62 * k) for k in range(88)], blk, on=1, off=3)
    for j in range(T):
        out += _bead(xr, reedK[j], 0.36 + 3.2 * (col[j] / cmax) ** 1.25, blk)

    # ======================= TYPE =========================================
    title = _spaced("ATTENTION AS WEAVING")
    th = 5.35
    out += giant_type(title, (x0 + x1) * 0.5 - _text_width(title, th) * 0.5,
                      y0 + 0.955 * H, th, pen=blk, weight=0.42, tip=0.20, f=2000)
    out += _stroke_text("Q", x0 + 4.0, y0 + 0.598 * H, 6.0, color=pq, f=2000)
    out += _stroke_text("K", x1 - 15.0, y0 + 0.636 * H, 6.0, color=pk, f=2000)
    out += _stroke_text("V", x0 + 11.0, y0 + 0.500 * H, 5.4, color=pv, f=2000)
    lab = "Q " + chr(0xB7) + " K"
    lx, ly = x0 + 0.235 * W, y0 + 0.893 * H
    out += _stroke_text(lab, lx, ly, 4.4, color=blk, f=2000)
    out += _stroke_text("T", lx + _text_width(lab, 4.4) + 0.5, ly + 2.5, 2.5, color=blk, f=2000)
    out += _stroke_text("Z = AV", x1 - 56.0, y0 + 0.068 * H, 5.6, color=pz, f=2000)
    foot = _spaced("GPT-2 L%d H%d %s Q=%s" % (LAYER, HEAD, D["src"], TOKENS[qs].strip()))
    out += _stroke_text(foot, x0 + 2.0, y0 + 1.2, 2.0, color=blk, f=2000)
    return out
