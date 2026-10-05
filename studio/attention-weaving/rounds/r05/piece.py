"""SUMS TO ONE — r05 · thesis AREA-SMOOTH · parent r03.

The aperture plate (r03) with its softmax made smooth WITHOUT faking a number,
and every field on the sheet driven by one real attention row.

WHAT CHANGED FROM r03 (the mechanism)
  * The numbers are REAL. A = softmax(QK^T/sqrt(d)) of GPT-2 small, LAYER 2
    HEAD 9, on the 15-token sentence "The pen plotter drew a black hole while
    the transformer watched itself think." (cached by
    scripts/extract_gpt2_attention.py at ~/.promptplot/attn_gpt2.npz — the
    same source as r02). The slit carries the row of the query " itself"
    (q* = 12): transformer 0.416, watched 0.377, itself 0.111, ... Keys 13-14
    are causally masked for that query, so the slit holds the 13 keys it can
    see, in SENTENCE ORDER — no permutation, no temperature, no target.
  * Queries = the 15 tokens, keys = the 13 visible ones: N = 28 filaments
    in, 28 out.
  * Q x K over/under is the real score sign: the centred log-attention
    c_ij = log A_ij - mean_{k<=i} log A_ik equals the centred scaled score
    (softmax is shift-invariant), so sign(c_ij) IS sign of the score against
    the row mean. A MASKED pair (j > i) is the key hidden from that query:
    the key goes under with a wider gap.
  * V x lane over/under is the real row: the gold strand of key j passes OVER
    a lane of clump k iff a_j >= a_k — the heavier value rides on top.

THE SOFTMAX PROFILE (the thesis)
  r03 drew a monotone interpolant through TWO knots per clump at height a_g:
  flat tops, i.e. the staircase it meant to remove. r05 draws a
  HISTOPOLANT: one smooth positive curve f(x) over the slit whose AREA over
  each clump's own span equals a_j exactly.
      f(x) = exp(g(x)),  g = natural cubic spline, knots at the clump centres (ends on the jambs)
  The 13 knot values are solved by Newton so that the trapezoid area of the
  DRAWN polyline over each clump span equals a_j to 1e-15. exp(.) keeps it
  positive; the spline makes it C2. Width still encodes the quantised weight
  (filament count p_j = 1 + round share of 15), and AREA now encodes the
  exact weight; the height is therefore a density, and the curve is one hill.
  The cumulative is literally the running integral of the drawn hill — it
  passes through every exact partial sum at every clump boundary and lands on
  1.000 at the right jamb, which is where the causal mask begins.

Contract: attention_weaving_area_smooth(rng, bounds, colors=3) -> list[GCodeCommand]
"""

from __future__ import annotations

import math
import os
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import geometry as G
from promptplot.generative.engine.kit import (
    _pen,
    fill_disc,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    giant_type,
    giant_type_width,
)

Bounds = Tuple[float, float, float, float]
Poly = List[Tuple[float, float]]

# pen slots — palette order: black, crimson, dodgerblue, goldenrod, darkgreen
BLACK, Q_PEN, K_PEN, V_PEN, Z_PEN = 0, 1, 2, 3, 4

NPZ = os.path.expanduser("~/.promptplot/attn_gpt2.npz")
LAYER, HEAD, QSTAR = 2, 9, 12
TOKENS = [
    "The", " pen", " plot", "ter", " drew", " a", " black", " hole", " while",
    " the", " transformer", " watched", " itself", " think", ".",
]

# filled on every call so the exactness claims can be CHECKED, not asserted
LAST_STATS: dict = {}


# ---------------------------------------------------------------------------
# the data: one real attention layer
# ---------------------------------------------------------------------------
def _numpy_attention(rng: SeededRNG, T: int = 15, d: int = 32) -> np.ndarray:
    """Fallback only: a real (seeded) numpy attention layer if the cache is gone."""
    g = np.random.default_rng(rng.seed)
    pos = np.arange(T)[:, None]
    ch = np.arange(d)[None, :]
    E = np.sin(pos / (10000 ** (2 * (ch // 2) / d)) + (ch % 2) * math.pi / 2)
    E = E + 0.35 * g.standard_normal((T, d))
    Wq = g.standard_normal((d, d)) / math.sqrt(d)
    Wk = g.standard_normal((d, d)) / math.sqrt(d)
    S = (E @ Wq) @ (E @ Wk).T / math.sqrt(d)
    S = np.where(np.tril(np.ones((T, T), bool)), S, -np.inf)
    S = S - S.max(1, keepdims=True)
    A = np.exp(S)
    return A / A.sum(1, keepdims=True)


def _attention(rng: SeededRNG) -> Tuple[np.ndarray, str]:
    A = None
    src = "GPT-2 L%d H%d" % (LAYER, HEAD)
    if os.path.exists(NPZ):
        try:
            raw = np.load(NPZ)["attn"].astype(np.float64)
            if raw.ndim == 4 and raw.shape[0] > LAYER and raw.shape[1] > HEAD:
                A = raw[LAYER, HEAD].copy()
        except Exception:
            A = None
    if A is None:
        A = _numpy_attention(rng)
        src = "NUMPY LAYER"
    A = A / A.sum(1, keepdims=True)          # float32 cache -> float64 rows
    return A, src


# ---------------------------------------------------------------------------
# the histopolant: a smooth positive curve with EXACT per-bin areas
# ---------------------------------------------------------------------------
def _nat_spline(xk: np.ndarray, yk: np.ndarray, xs: np.ndarray) -> np.ndarray:
    """Natural cubic spline through (xk, yk). The end knots sit ON the jambs,
    so it is only ever evaluated inside [xk0, xkn] — no extrapolated spike
    (v1) and no clamped flat shelf (v2)."""
    n = len(xk)
    h = np.diff(xk)
    M = np.zeros((n, n))
    r = np.zeros(n)
    # left end: level (g' = 0) on the jamb — a natural end there turned the
    # first-token sink into a needle (v3); right end: natural.
    M[0, 0], M[0, 1] = 2.0 * h[0], h[0]
    r[0] = 6.0 * ((yk[1] - yk[0]) / h[0])
    M[-1, -1] = 1.0
    for i in range(1, n - 1):
        M[i, i - 1] = h[i - 1]
        M[i, i] = 2.0 * (h[i - 1] + h[i])
        M[i, i + 1] = h[i]
        r[i] = 6.0 * ((yk[i + 1] - yk[i]) / h[i] - (yk[i] - yk[i - 1]) / h[i - 1])
    m = np.linalg.solve(M, r)
    out = np.empty_like(xs)
    for q, x in enumerate(xs):
        i = max(0, min(n - 2, int(np.searchsorted(xk, x) - 1)))
        A_ = (xk[i + 1] - x) / h[i]
        B_ = (x - xk[i]) / h[i]
        out[q] = (A_ * yk[i] + B_ * yk[i + 1]
                  + ((A_ ** 3 - A_) * m[i] + (B_ ** 3 - B_) * m[i + 1]) * h[i] ** 2 / 6.0)
    return out


def _trap(y: np.ndarray, x: np.ndarray) -> float:
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def histopolant(edges: Sequence[float], a: Sequence[float], step: float = 0.18):
    """f(x) = exp(natural spline) with trapezoid area over bin j == a[j].

    Returns (xs, f, bin_slices, max_area_err). xs contains every bin edge, so
    the area of the DRAWN polyline over each bin is exactly what is solved."""
    edges = np.asarray(edges, float)
    a = np.asarray(a, float)
    nb = len(a)
    xs_parts = []
    slices = []
    start = 0
    for j in range(nb):
        k = max(4, int(math.ceil((edges[j + 1] - edges[j]) / step)))
        seg = np.linspace(edges[j], edges[j + 1], k + 1)
        xs_parts.append(seg if j == 0 else seg[1:])
        slices.append((start, start + k))
        start += k
    xs = np.concatenate(xs_parts)
    xk = 0.5 * (edges[:-1] + edges[1:])
    xk[0], xk[-1] = edges[0], edges[-1]      # end knots ON the jambs: no shelf
    B = np.stack([_nat_spline(xk, np.eye(nb)[k], xs) for k in range(nb)], axis=1)
    g = np.log(a / np.diff(edges))
    err = 1.0
    for _ in range(200):
        f = np.exp(B @ g)
        F = np.array([_trap(f[s:e + 1], xs[s:e + 1]) for s, e in slices]) - a
        err = float(np.max(np.abs(F)))
        if err < 1e-16:
            break
        J = np.array([[_trap((f * B[:, k])[s:e + 1], xs[s:e + 1]) for k in range(nb)]
                      for s, e in slices])
        dg = np.linalg.solve(J, -F)
        big = float(np.max(np.abs(dg)))
        if big > 1.5:
            dg *= 1.5 / big
        g = g + dg
    f = np.exp(B @ g)
    F = np.array([_trap(f[s:e + 1], xs[s:e + 1]) for s, e in slices]) - a
    return xs, f, slices, float(np.max(np.abs(F)))


# ---------------------------------------------------------------------------
# bespoke geometry: the aperture's elliptic coordinate system
# ---------------------------------------------------------------------------
class Aperture:
    """Elliptic coordinates about a slit of half-width ``c`` centred at (ax, ay)."""

    def __init__(self, ax: float, ay: float, c: float):
        self.ax, self.ay, self.c = ax, ay, c

    def pt(self, phi: float, psi: float) -> Tuple[float, float]:
        return (
            self.ax + self.c * math.cosh(phi) * math.cos(psi),
            self.ay + self.c * math.sinh(phi) * math.sin(psi),
        )

    def psi_for_slit_x(self, off: float) -> float:
        t = max(-0.99995, min(0.99995, off / self.c))
        return math.acos(t)


def _smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def _resample(poly: Poly, step: float = 1.4) -> Poly:
    if len(poly) < 2:
        return list(poly)
    out: Poly = [poly[0]]
    carry = 0.0
    for p0, p1 in zip(poly, poly[1:]):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        t = step - carry
        while t <= L:
            out.append((p0[0] + dx * t / L, p0[1] + dy * t / L))
            t += step
        carry = (carry + L) % step
    out.append(poly[-1])
    return out


def _bbox(poly: Poly) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def _seg_x(p0, p1, q0, q1):
    r = (p1[0] - p0[0], p1[1] - p0[1])
    s = (q1[0] - q0[0], q1[1] - q0[1])
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-12:
        return None
    t = ((q0[0] - p0[0]) * s[1] - (q0[1] - p0[1]) * s[0]) / den
    u = ((q0[0] - p0[0]) * r[1] - (q0[1] - p0[1]) * r[0]) / den
    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        return (p0[0] + r[0] * t, p0[1] + r[1] * t)
    return None


def _crossings(pa: Poly, pb: Poly) -> List[Tuple[float, float]]:
    ax0, ay0, ax1, ay1 = _bbox(pa)
    bx0, by0, bx1, by1 = _bbox(pb)
    if ax1 < bx0 or bx1 < ax0 or ay1 < by0 or by1 < ay0:
        return []
    hits: List[Tuple[float, float]] = []
    for p0, p1 in zip(pa, pa[1:]):
        lo_x, hi_x = (p0[0], p1[0]) if p0[0] < p1[0] else (p1[0], p0[0])
        lo_y, hi_y = (p0[1], p1[1]) if p0[1] < p1[1] else (p1[1], p0[1])
        if hi_x < bx0 or lo_x > bx1 or hi_y < by0 or lo_y > by1:
            continue
        for q0, q1 in zip(pb, pb[1:]):
            if max(q0[0], q1[0]) < lo_x - 0.1 or min(q0[0], q1[0]) > hi_x + 0.1:
                continue
            if max(q0[1], q1[1]) < lo_y - 0.1 or min(q0[1], q1[1]) > hi_y + 0.1:
                continue
            h = _seg_x(p0, p1, q0, q1)
            if h:
                hits.append(h)
    return hits


def _cut_and_emit(
    poly: Poly,
    cuts: Sequence[Tuple[float, float, float]],
    pen: Optional[int],
    box: G.Region,
    f: int = 2200,
    passes: int = 1,
    pitch: float = 0.38,
    halo: Optional[G.Region] = None,
) -> List[GCodeCommand]:
    """Clip to ``box``, punch a gap at every (x, y, r) cut (the UNDER side of a
    crossing) and out of every label halo, emit at ``passes`` parallel passes,
    re-clipping so an offset pass can never leave the sheet."""
    runs = G.clip(poly, box, keep="inside")
    if cuts:
        holes = G.Union(*[G.Circle(cx, cy, r) for cx, cy, r in cuts])
        runs = [r for run in runs for r in G.clip(run, holes, keep="outside")]
    if halo is not None:
        runs = [r for run in runs for r in G.clip(run, halo, keep="outside")]
    # a crossing gap must not leave a crumb: drop runs shorter than 0.9 mm
    runs = [r for r in runs if len(r) >= 2 and G.polyline_length(r) >= 0.9]
    out: List[GCodeCommand] = []
    for run in runs:
        if len(run) < 2:
            continue
        if passes <= 1:
            out += _poly(run, color=pen, f=f)
            continue
        for k in range(passes):
            dd = -pitch * (passes - 1) / 2.0 + pitch * k
            for sub in G.clip(G.offset(run, dd), box, keep="inside"):
                if halo is not None:
                    for s2 in G.clip(sub, halo, keep="outside"):
                        out += _poly(s2, color=pen, f=f)
                else:
                    out += _poly(sub, color=pen, f=f)
    return out


def _dotted(poly: Poly, pen: Optional[int], box: G.Region, on: int = 2, off: int = 7,
            f: int = 2200, halo: Optional[G.Region] = None) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    runs = G.clip(poly, box, keep="inside")
    if halo is not None:
        runs = [r for run in runs for r in G.clip(run, halo, keep="outside")]
    for run in runs:
        seg: Poly = []
        for k, p in enumerate(run):
            if (k % (on + off)) < on:
                seg.append(p)
            else:
                if len(seg) >= 2 and G.polyline_length(seg) >= 0.6:
                    out += _poly(seg, color=pen, f=f)
                seg = []
        if len(seg) >= 2 and G.polyline_length(seg) >= 0.6:
            out += _poly(seg, color=pen, f=f)
    return out


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def attention_weaving_area_smooth(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    feed: int = 2200,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    k_black = _pen(BLACK, colors)
    k_q = _pen(Q_PEN, colors)
    k_k = _pen(K_PEN, colors)
    k_v = _pen(V_PEN, colors)
    k_z = _pen(Z_PEN, colors)
    out: List[GCodeCommand] = []

    box = G.Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)
    GAP = 1.15

    # ---- the aperture -----------------------------------------------------
    c = 0.118 * W
    ap = Aperture(ax=x0 + 0.425 * W, ay=y0 + 0.620 * H, c=c)
    ax, ay = ap.ax, ap.ay

    # ---- the numbers: one real attention layer -----------------------------
    Afull, src = _attention(rng)
    T = Afull.shape[0]
    qstar = min(QSTAR, T - 1)
    n_q = T                                  # every token is a query
    n_k = qstar + 1                          # the keys " itself" can see
    A = [float(v) for v in Afull[qstar, :n_k]]
    a_max = max(A)
    j_max = A.index(a_max)
    Hbits = -sum(v * math.log(v, 2) for v in A if v > 0)
    principal = qstar

    # centred log-attention == centred scaled score (softmax is shift-invariant)
    S = [[0.0] * n_k for _ in range(n_q)]
    masked = [[False] * n_k for _ in range(n_q)]
    for i in range(n_q):
        vis = [math.log(max(Afull[i, j], 1e-300)) for j in range(min(i, n_k - 1) + 1)]
        mu = sum(vis) / len(vis)
        for j in range(n_k):
            if j > i:
                masked[i][j] = True
            else:
                S[i][j] = math.log(max(Afull[i, j], 1e-300)) - mu

    # ---- filament quantisation: N filaments dealt out by weight ------------
    total_f = n_q + n_k
    p = [1] * n_k
    left = total_f - n_k
    share = [A[j] * left for j in range(n_k)]
    base = [int(s) for s in share]
    for j in range(n_k):
        p[j] += base[j]
    rem = left - sum(base)
    for _, j in sorted(((share[j] - base[j], j) for j in range(n_k)), reverse=True)[:rem]:
        p[j] += 1
    assert sum(p) == total_f

    # keys in SENTENCE ORDER along the slit — no permutation
    Ag = list(A)
    pg = list(p)

    FP = 1.50                    # filament pitch INSIDE a clump (floor 0.8)
    ROPE_W = 0.290 * W           # the rope relaxes wider than the slit

    def _layout(width: float):
        """Pack the clumps across ``width`` with a constant inter-clump gap."""
        gap = (width - sum(pg[g] - 1 for g in range(n_k)) * FP) / (n_k - 1)
        raw: List[float] = []
        spans: List[Tuple[float, float]] = []
        cur = 0.0
        for g in range(n_k):
            g0 = cur
            for t in range(pg[g]):
                raw.append(cur + t * FP)
            cur += (pg[g] - 1) * FP
            spans.append((g0, cur))
            cur += gap
        mid = 0.5 * (raw[0] + raw[-1])
        return ([q - mid for q in raw],
                [(a - mid, b - mid) for a, b in spans], gap)

    slit_half = c - 1.7
    raw, group_span, GAPG = _layout(2 * slit_half)
    raw_rope, _, GAP_ROPE = _layout(ROPE_W)

    n_lane = len(raw)
    lane_key: List[int] = []
    for g in range(n_k):
        lane_key += [g] * pg[g]
    lat = [q / slit_half for q in raw]
    lat_rope = [q / (0.5 * ROPE_W) for q in raw_rope]
    lands = list(raw)
    # Q and K INTERLEAVE inside the gate, dealt proportionally
    q_idx: List[int] = []
    k_idx: List[int] = []
    qi = ki = 0
    for t in range(n_lane):
        if ki >= n_k or (qi < n_q and (qi + 0.5) / n_q <= (ki + 0.5) / n_k):
            q_idx.append(t)
            qi += 1
        else:
            k_idx.append(t)
            ki += 1
    # the principal query (" itself") takes the lane nearest the slit centre and
    # falls dead straight; the other queries keep sentence order left to right.
    centre_slot = min(range(n_q), key=lambda s: abs(lands[q_idx[s]]))
    others = [i for i in range(n_q) if i != principal]
    q_of_slot: List[int] = []
    for s in range(n_q):
        q_of_slot.append(principal if s == centre_slot else others.pop(0))
    q_land = [0.0] * n_q
    for s, i in enumerate(q_of_slot):
        q_land[i] = lands[q_idx[s]]
    k_land = [lands[t] for t in k_idx]
    min_pitch = min(lands[t + 1] - lands[t] for t in range(n_lane - 1))

    # ---- Q: pure streamlines ----------------------------------------------
    PHI_MAX = 2.85
    psi_q = [ap.psi_for_slit_x(o) for o in q_land]

    def q_path(i: int) -> Poly:
        ps = psi_q[i]
        return [ap.pt(PHI_MAX * (1.0 - t / 170.0) ** 1.22, ps) for t in range(171)]

    # ---- K: sweep the fan HIGH, then drop into the slit --------------------
    psi_k_end = [ap.psi_for_slit_x(o) for o in k_land]
    order = sorted(range(n_k), key=lambda j: psi_k_end[j])
    rank = {j: r for r, j in enumerate(order)}
    U_SWEEP = 0.68
    psi_k_start = [0.018 * math.pi + 0.255 * math.pi * (rank[j] / max(1, n_k - 1))
                   for j in range(n_k)]
    phi_k = [1.52 + 1.52 * (rank[j] / max(1, n_k - 1)) for j in range(n_k)]

    def k_phi_psi(j: int, u: float) -> Tuple[float, float]:
        a0, a1 = psi_k_start[j], psi_k_end[j]
        if u <= U_SWEEP:
            w = u / U_SWEEP
            return phi_k[j] * (1.0 - 0.44 * _smoothstep(w)), a0 + (a1 - a0) * _smoothstep(w)
        w = (u - U_SWEEP) / (1.0 - U_SWEEP)
        return phi_k[j] * 0.56 * (1.0 - w) ** 1.5, a1

    def k_path(j: int) -> Poly:
        return [ap.pt(*k_phi_psi(j, t / 230.0)) for t in range(231)]

    q_polys = [_resample(q_path(i), 1.1) for i in range(n_q)]
    k_polys = [_resample(k_path(j), 1.1) for j in range(n_k)]

    # ---- Q.K^T: one crossing per pair, over/under by the REAL score --------
    q_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_q)]
    k_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_k)]
    n_cross = n_cross_masked = 0
    for j in range(n_k):
        a0, a1 = psi_k_start[j], psi_k_end[j]
        if abs(a1 - a0) < 1e-6:
            continue
        for i in range(n_q):
            target = psi_q[i]
            if not (min(a0, a1) < target < max(a0, a1)):
                continue
            fr = (target - a0) / (a1 - a0)
            lo, hi = 0.0, U_SWEEP
            for _ in range(34):
                m = 0.5 * (lo + hi)
                if _smoothstep(m / U_SWEEP) < fr:
                    lo = m
                else:
                    hi = m
            px, py = ap.pt(*k_phi_psi(j, 0.5 * (lo + hi)))
            if not (x0 + 1 < px < x1 - 1 and ay + 2.0 < py < y1 - 1):
                continue
            n_cross += 1
            if masked[i][j]:
                # the causal mask: the key is HIDDEN from this query
                n_cross_masked += 1
                k_cuts[j].append((px, py, 1.75))
            elif S[i][j] >= 0.0:
                k_cuts[j].append((px, py, GAP))
            else:
                q_cuts[i].append((px, py, GAP))

    # ---- THE SOFTMAX HILL: an area-exact smooth density --------------------
    pad = GAPG * 0.5
    edges = [ax - c]
    for g in range(n_k - 1):
        edges.append(ax + group_span[g][1] + pad)
    edges.append(ax + c)
    hx, hf, hsl, area_err = histopolant(edges, Ag)
    f_max = float(hf.max())
    ZMAX = 0.100 * H
    Kmm = ZMAX / f_max                                  # mm of height per unit density
    prof = [(float(x), ay + Kmm * float(v)) for x, v in zip(hx, hf)]
    zig: Poly = [(ax - c, ay)] + prof + [(ax + c, ay)]
    zig_r = _resample(zig, 0.8)
    x_peak = float(hx[int(np.argmax(hf))])
    # the area of every clump, measured on the polyline that is actually drawn
    clump_area_mm2 = [_trap(Kmm * hf[s:e + 1], hx[s:e + 1]) for s, e in hsl]

    # the cumulative: the running integral of the drawn hill
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (hf[1:] + hf[:-1]) * np.diff(hx))])
    ZC = 1.0 * ZMAX
    cum_poly = [(float(x), ay + ZC * float(v)) for x, v in zip(hx, cum)]
    cum_at_edges = [float(cum[e]) for _, e in hsl]
    partial = list(np.cumsum(Ag))
    cum_err = max(abs(u - v) for u, v in zip(cum_at_edges, partial))

    for i in range(n_q):
        for hx_, hy_ in _crossings(q_polys[i], zig_r):
            q_cuts[i].append((hx_, hy_, 1.0))
    for j in range(n_k):
        for hx_, hy_ in _crossings(k_polys[j], zig_r):
            k_cuts[j].append((hx_, hy_, 1.0))

    # ---- labels first, so every strand can keep clear of them (halos) ------
    labels: List[Tuple[str, float, float, float, Optional[int]]] = []
    halos: List[G.Region] = []

    def label(txt: str, lx: float, ly: float, h: float, pen, halo_pad: float = 1.2):
        labels.append((txt, lx, ly, h, pen))
        wdt = _text_width(txt, h)
        halos.append(G.Rect(lx - halo_pad, ly - halo_pad, lx + wdt + halo_pad, ly + h + halo_pad))

    one_txt = "1.000"
    label(one_txt, ax + c + 3.4, ay + ZC - 1.1, 2.3, k_black, 1.0)
    sm = _spaced("SOFTMAX")
    label(sm, ax + c + 3.4, ay + 2.6, 2.4, k_black)
    top3 = sorted(range(n_k), key=lambda j: -A[j])[:3]
    tok = (lambda j: TOKENS[j].strip().upper()) if T == len(TOKENS) else (lambda j: "K%d" % j)
    for r_, j in enumerate(top3):          # the three heaviest keys, named
        label(_spaced("%.3f %s" % (A[j], tok(j))), ax + c + 3.4, ay - 5.2 - 3.6 * r_,
              1.8, k_black, 1.8)
    label(_spaced("Q"), x0 + 0.030 * W, y1 - 0.180 * H, 4.6, k_q)
    label(_spaced("K"), x1 - 0.075 * W, y1 - 0.052 * H, 4.6, k_k)
    halo = G.Union(*halos) if halos else None

    # ---- scaffold: the confocal ellipses (equipotentials), dotted, behind --
    for phi in (0.72, 1.48):
        up = [ap.pt(phi, math.pi * t / 300.0) for t in range(301)]
        out += _dotted(_resample(up, 1.0), k_black, box, on=3, off=4, f=feed, halo=halo)
    for phi, o in ((0.62, 4), (1.62, 5)):
        dn = [ap.pt(-phi, math.pi * t / 300.0) for t in range(301)]
        out += _dotted(_resample(dn, 1.0), k_black, box, on=2, off=o, f=feed, halo=halo)

    # ---- the storm --------------------------------------------------------
    for i in range(n_q):
        out += _cut_and_emit(q_polys[i], q_cuts[i], k_q, box, f=feed,
                             passes=2 if i == principal else 1, pitch=0.34, halo=halo)
    for j in range(n_k):
        out += _cut_and_emit(k_polys[j], k_cuts[j], k_k, box, f=feed,
                             passes=2 if p[j] >= 4 else 1, pitch=0.34, halo=halo)

    # ---- THE WALL: one black rule, one hole -------------------------------
    for k in range(5):
        dy = -0.62 + 0.31 * k
        out += _poly([(x0 + 0.4, ay + dy), (ax - c, ay + dy)], color=k_black, f=feed)
        out += _poly([(ax + c, ay + dy), (x1 - 0.4, ay + dy)], color=k_black, f=feed)

    # ---- below the wall: the rope ----------------------------------------
    spine = [
        (ax, ay),
        (ax + 0.008 * W, ay - 0.100 * H),
        (ax + 0.038 * W, ay - 0.183 * H),
        (ax + 0.112 * W, ay - 0.238 * H),
        (ax + 0.248 * W, ay - 0.267 * H),
        (ax + 0.455 * W, ay - 0.281 * H),
        (x1 + 0.22 * W, ay - 0.288 * H),
    ]

    def _spine_at(u: float) -> Tuple[float, float, float, float]:
        """Catmull-Rom position AND its analytic tangent, so the lane normals
        are continuous (r03 took the chord direction: the normal jumped at every
        knot and the lanes chevroned at the bend)."""
        f_ = u * (len(spine) - 1)
        k0 = min(len(spine) - 2, int(f_))
        tt = f_ - k0
        pa, pb = spine[k0], spine[k0 + 1]
        pprev = spine[max(0, k0 - 1)]
        pnext = spine[min(len(spine) - 1, k0 + 2)]

        def cr(a, b, cc, dd):
            return 0.5 * ((2 * b) + (-a + cc) * tt
                          + (2 * a - 5 * b + 4 * cc - dd) * tt * tt
                          + (-a + 3 * b - 3 * cc + dd) * tt ** 3)

        def dcr(a, b, cc, dd):
            return 0.5 * ((-a + cc) + 2 * (2 * a - 5 * b + 4 * cc - dd) * tt
                          + 3 * (-a + 3 * b - 3 * cc + dd) * tt * tt)

        sx = cr(pprev[0], pa[0], pb[0], pnext[0])
        sy = cr(pprev[1], pa[1], pb[1], pnext[1])
        tx = dcr(pprev[0], pa[0], pb[0], pnext[0])
        ty = dcr(pprev[1], pa[1], pb[1], pnext[1])
        L = math.hypot(tx, ty) or 1.0
        return sx, sy, -ty / L, tx / L

    def lane_path(idx: int) -> Poly:
        psi = ap.psi_for_slit_x(lands[idx])
        pts: Poly = []
        for t in range(241):
            u = t / 240.0
            sx, sy, nx, ny = _spine_at(u)
            e = _smoothstep(max(0.0, min(1.0, (u - 0.38) / 0.60)))
            half = slit_half * (1 - e) + 0.5 * ROPE_W * e
            w = (lat[idx] * (1 - e) + lat_rope[idx] * e) * half
            if u < 0.085:
                b = u / 0.085
                ex, ey = ap.pt(-0.40 * b, psi)
                pts.append((ex * (1 - b) + (sx + nx * w) * b,
                            ey * (1 - b) + (sy + ny * w) * b))
            else:
                pts.append((sx + nx * w, sy + ny * w))
        return pts

    lane_polys = [_resample(lane_path(t), 1.2) for t in range(n_lane)]
    # the lanes must never cross one another (that is what read as a tangle)
    lane_x = 0
    for t in range(n_lane - 1):
        lane_x += len(_crossings(lane_polys[t], lane_polys[t + 1]))

    # ---- V: one gold filament per key, entering from the left rim ---------
    vt = [0.400 - 0.270 * (g / max(1, n_k - 1)) for g in range(n_k)]
    v_polys: List[Poly] = []
    v_pass = [3 if pg[g] >= 4 else 2 for g in range(n_k)]
    knot = (x0 + 0.300 * W, y0 + 0.535 * H)
    for g in range(n_k):
        idxs = [t for t in range(n_lane) if lane_key[t] == g]
        lp = lane_polys[idxs[len(idxs) // 2]]
        u_t = vt[g]
        tgt = lp[int(u_t * (len(lp) - 1))]
        sx, sy, nx, ny = _spine_at(u_t)
        r = g / max(1, n_k - 1)
        y_entry = y0 + (0.452 + 0.158 * r) * H
        start = (x0 - 0.05 * W, y_entry)
        side = 1.0 if ((start[0] - sx) * nx + (start[1] - sy) * ny) >= 0 else -1.0
        c2 = (tgt[0] + nx * side * 0.100 * H, tgt[1] + ny * side * 0.100 * H)
        own = (0.50 * start[0] + 0.50 * c2[0], y_entry - 0.006 * H)
        c1 = (0.40 * knot[0] + 0.60 * own[0], 0.40 * knot[1] + 0.60 * own[1])
        pts: Poly = []
        for t in range(171):
            e = t / 170.0
            px = ((1 - e) ** 3 * start[0] + 3 * (1 - e) ** 2 * e * c1[0]
                  + 3 * (1 - e) * e ** 2 * c2[0] + e ** 3 * tgt[0])
            py = ((1 - e) ** 3 * start[1] + 3 * (1 - e) ** 2 * e * c1[1]
                  + 3 * (1 - e) * e ** 2 * c2[1] + e ** 3 * tgt[1])
            pts.append((px, py))
        v_polys.append(_resample(pts, 1.1))

    lane_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_lane)]
    v_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_k)]
    n_vx = n_v_over = 0
    # Z = AV: the gold of key g passes OVER a lane of clump k iff a_g >= a_k —
    # the heavier value rides on top. Real row, no seeded vectors.
    for g in range(n_k):
        for t in range(n_lane):
            for hx_, hy_ in _crossings(v_polys[g], lane_polys[t]):
                n_vx += 1
                over = Ag[g] >= Ag[lane_key[t]]
                n_v_over += int(over)
                (lane_cuts[t] if over else v_cuts[g]).append(
                    (hx_, hy_, 1.25 if over else 0.9))

    for t in range(n_lane):
        out += _cut_and_emit(lane_polys[t], lane_cuts[t], k_z, box, f=feed, halo=halo)
    for g in range(n_k):
        out += _cut_and_emit(v_polys[g], v_cuts[g], k_v, box, f=feed,
                             passes=v_pass[g], pitch=0.36, halo=halo)

    # ---- the hill sits ON TOP --------------------------------------------
    for sub in G.clip(cum_poly, box, keep="inside"):
        out += _poly(sub, color=k_black, f=feed)
    out += _poly([(ax + c, ay + ZC), (ax + c + 2.4, ay + ZC)], color=k_black, f=feed)
    out += fill_disc(ax + c, ay + ZC, 0.7, spacing=0.3, pen=k_black, f=feed)
    for k in range(4):
        sil = [(px, py + 0.30 * k) for px, py in zig]
        for sub in G.clip(sil, box, keep="inside"):
            out += _poly(sub, color=k_black, f=feed)
    # the partition, as a ruler on the wall line: one tick per clump boundary,
    # hanging below the hole's baseline, in the gap between two clumps.
    for bx in edges[1:-1]:
        out += _poly([(bx, ay + 0.6), (bx, ay - 2.4)], color=k_black, f=feed)

    # ---- reeds: where the strands leave the sheet -------------------------
    def reed(polys: Sequence[Poly], pen, edges_=("top", "right", "left")):
        for pl in polys:
            for rr in G.clip(pl, box, keep="inside"):
                for e in (rr[0], rr[-1]):
                    if "top" in edges_ and e[1] > y1 - 1.2:
                        out.extend(_poly([(e[0], y1 - 0.6), (e[0], y1 - 3.6)],
                                         color=pen, f=feed))
                    elif "right" in edges_ and e[0] > x1 - 1.2:
                        out.extend(_poly([(x1 - 0.6, e[1]), (x1 - 3.6, e[1])],
                                         color=pen, f=feed))
                    elif "left" in edges_ and e[0] < x0 + 1.2:
                        out.extend(_poly([(x0 + 0.6, e[1]), (x0 + 3.6, e[1])],
                                         color=pen, f=feed))

    reed(q_polys, k_black)
    reed(k_polys, k_black)
    reed(lane_polys, k_black, edges_=("right",))
    reed(v_polys, k_black, edges_=("left",))

    # ---- type: Deco spaced caps, monumental, standing in the silence ------
    th = 18.0
    while giant_type_width("TO ONE", th, spaced=True) > 0.62 * W and th > 8:
        th -= 0.5
    ty = y0 + 0.205 * H
    out += giant_type("SUMS", x0 + 1.5, ty, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
    out += giant_type("TO ONE", x0 + 1.5, ty - th * 1.62, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)

    # footer: one leading for every line
    lead = 0.026 * H
    fy = ty - th * 2.55
    foot = [
        (_spaced("ATTENTION AS A FLOW THROUGH ONE APERTURE"), 2.6),
        (_spaced(f"{src}   ROW ITSELF   Σa = {sum(A):.9f}"), 2.0),
        (_spaced(f"A MAX = {a_max:.3f} TRANSFORMER   H = {Hbits:.2f} OF {math.log(n_k, 2):.2f} BITS"), 2.0),
        (_spaced(f"{n_cross} OF {n_q*n_k} SCORES CROSS   "
                 + ("NONE MASKED   " if n_cross_masked == 0 else f"{n_cross_masked} MASKED   ")
                 + f"{total_f} IN {n_lane} OUT"), 2.0),
    ]
    for k, (txt, h) in enumerate(foot):
        out += _stroke_text(txt, x0 + 2.0, fy - k * lead, h, color=k_black, f=feed)

    # ---- labels (own layer, drawn last, strands already keep clear) --------
    for txt, lx, ly, h, pen in labels:
        out += _stroke_text(txt, lx, ly, h, color=pen, f=feed)
    out += _stroke_text(_spaced("V"), x0 + 0.020 * W, y0 + 0.620 * H, 4.6, color=k_v, f=feed)
    out += _stroke_text(_spaced("Z = A V"), x1 - 0.275 * W, y0 + 0.130 * H, 4.6,
                        color=k_z, f=feed)

    LAST_STATS.clear()
    LAST_STATS.update(
        src=src, row=[round(v, 6) for v in A], sum_a=sum(A), a_max=a_max,
        argmax=TOKENS[j_max] if T == len(TOKENS) else j_max,
        entropy_bits=Hbits, n_k=n_k, n_q=n_q, p=list(p),
        filaments_in=total_f, filaments_out=n_lane,
        edges_span=edges[-1] - edges[0], slit=2 * c,
        area_err=area_err, cum_end=float(cum[-1]), cum_err_at_edges=cum_err,
        hill_area_mm2=sum(clump_area_mm2), clump_area_mm2=clump_area_mm2,
        mm2_per_unit=Kmm, x_peak_u=(x_peak - x0) / W, f_min_over_max=float(hf.min() / f_max),
        min_pitch=min_pitch, qk_crossings=n_cross, qk_masked=n_cross_masked,
        v_crossings=n_vx, v_over=n_v_over, lane_lane_crossings=lane_x,
    )
    return out
