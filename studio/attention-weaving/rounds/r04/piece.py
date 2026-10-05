"""SUMS TO ONE — MIRROR-DRAIN. r04 of `attention-weaving`, parent r03 (v19).

The upper half is r03's storm, unchanged: Q streamlines and K spirals of the
elliptic coordinate system of ONE slit in a black wall,

    x = ax + c*cosh(phi)*cos(psi),   y = ay + c*sinh(phi)*sin(psi),

phi > 0 above the wall, phi = 0 IS the slit. This round draws the other half.

BELOW THE WALL (new) — the phi < 0 half of the same system:
  Z lanes   the 38 streamlines psi = const continued through the slit: each
            leaves exactly where its Q or K strand arrived, vertical, and
            fans out — the mirror sunburst. Z = AV bends it down-right:
            psi' = psi * m(|phi|), m = KB + (1-KB)/cosh(BR*|phi|); monotone in
            psi at every depth, so no lane crosses another (measured: 0).
  V         a second spiral family, the mirror of K: the orthogonal
            trajectories of the drawn lanes, pitched into spirals. Each V_j
            crosses every lane exactly once (608 / 608, measured) at >= 65 deg;
            over/under at V_j x lane t = sign(v_j[t]) — lane t IS output
            component t, and the outlet reed's length is |z_t|, z = sum_j a_j v_j.
            V never touches the slit: V joins after the waist.
SOFTMAX (new) — one smooth hill, partitioned by AREA: the least-curvature
            h(x) >= 0 whose integral over clump g is exactly a_g (KKT solve,
            measured on the drawn polyline to 1e-15). No flat tops, no knot
            discs; clump boundaries are ticks on the wall line. The fine curve
            is the running integral of the hill and lands on 1.000, labelled.

CANON: ART DECO — the double sunburst finally exists. The sunburst is a drain.
Contract: attention_weaving_mirror_drain(rng, bounds, colors=3)
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

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

# filled on every call so the exactness claims can be CHECKED, not asserted
LAST_STATS: dict = {}


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


def _softmax(scores: Sequence[float], temp: float) -> List[float]:
    m = max(scores) / temp
    e = [math.exp(s / temp - m) for s in scores]
    z = sum(e)
    return [v / z for v in e]


def _entropy_bits(p: Sequence[float]) -> float:
    return -sum(v * math.log(v, 2) for v in p if v > 1e-12)


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


def _dash(poly: Poly, on: float = 4.6, off: float = 1.7) -> List[Poly]:
    """Split a polyline into dashes by arclength."""
    out: List[Poly] = []
    cur: Poly = [poly[0]] if poly else []
    d, drawing = 0.0, True
    for p0, p1 in zip(poly, poly[1:]):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        if L < 1e-9:
            continue
        t = 0.0
        while t < L:
            need = (on - d) if drawing else (off - d)
            step = min(need, L - t)
            t += step
            d += step
            px = p0[0] + (p1[0] - p0[0]) * t / L
            py = p0[1] + (p1[1] - p0[1]) * t / L
            if drawing:
                cur.append((px, py))
            if d >= (on if drawing else off) - 1e-9:
                if drawing and len(cur) >= 2:
                    out.append(cur)
                drawing = not drawing
                cur = [(px, py)] if drawing else []
                d = 0.0
    if drawing and len(cur) >= 2:
        out.append(cur)
    return out


def _pchip(xs: Sequence[float], ys: Sequence[float], per: int = 14) -> Poly:
    """Fritsch-Carlson monotone cubic through the knots. It INTERPOLATES every
    knot exactly and cannot overshoot, so a smooth profile drawn this way still
    passes through the exact value at every clump centre."""
    n = len(xs)
    if n < 2:
        return [(xs[0], ys[0])] if n else []
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    dl = [(ys[i + 1] - ys[i]) / h[i] if h[i] else 0.0 for i in range(n - 1)]
    d = [0.0] * n
    d[0], d[-1] = dl[0], dl[-1]
    for i in range(1, n - 1):
        if dl[i - 1] * dl[i] <= 0.0:
            d[i] = 0.0
        else:
            w1, w2 = 2 * h[i] + h[i - 1], h[i] + 2 * h[i - 1]
            d[i] = (w1 + w2) / (w1 / dl[i - 1] + w2 / dl[i])
    out: Poly = []
    for i in range(n - 1):
        for k in range(per + (1 if i == n - 2 else 0)):
            t = k / per
            t2, t3 = t * t, t * t * t
            H0 = 2 * t3 - 3 * t2 + 1
            H1 = t3 - 2 * t2 + t
            H2 = -2 * t3 + 3 * t2
            H3 = t3 - t2
            out.append((xs[i] + h[i] * t,
                        H0 * ys[i] + H1 * h[i] * d[i] + H2 * ys[i + 1] + H3 * h[i] * d[i + 1]))
    return out


def _pchip_at(xs: Sequence[float], ys: Sequence[float], x: float) -> float:
    """Sample the same interpolant at one x (used to hang the boundary ticks)."""
    poly = _pchip(xs, ys, per=26)
    for a, b in zip(poly, poly[1:]):
        if a[0] <= x <= b[0]:
            t = (x - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0.0
            return a[1] + (b[1] - a[1]) * t
    return poly[0][1] if x < poly[0][0] else poly[-1][1]


def _cut_and_emit(
    poly: Poly,
    cuts: Sequence[Tuple[float, float, float]],
    pen: Optional[int],
    box: G.Region,
    f: int = 2200,
    passes: int = 1,
    pitch: float = 0.38,
    dashed: bool = False,
) -> List[GCodeCommand]:
    """Clip to ``box``, punch a gap at every (x, y, r) cut (the UNDER side of a
    crossing), optionally dash, emit at ``passes`` parallel passes, re-clipping
    so an offset pass can never leave the sheet."""
    runs = G.clip(poly, box, keep="inside")
    if cuts:
        holes = G.Union(*[G.Circle(cx, cy, r) for cx, cy, r in cuts])
        runs = [r for run in runs for r in G.clip(run, holes, keep="outside")]
    if dashed:
        runs = [d for run in runs for d in _dash(run)]
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
                out += _poly(sub, color=pen, f=f)
    return out


def _dotted(poly: Poly, pen: Optional[int], box: G.Region, on: int = 2, off: int = 7,
            f: int = 2200) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for run in G.clip(poly, box, keep="inside"):
        seg: Poly = []
        for k, p in enumerate(run):
            if (k % (on + off)) < on:
                seg.append(p)
            else:
                if len(seg) >= 2:
                    out += _poly(seg, color=pen, f=f)
                seg = []
        if len(seg) >= 2:
            out += _poly(seg, color=pen, f=f)
    return out


def _crossings_ang(pa: Poly, pb: Poly) -> List[Tuple[float, float, float]]:
    """Every crossing of two polylines, with the crossing angle in degrees
    (0..90) — so 'crosses at >= 45 deg' is measured, not eyeballed.
    Vectorised: all segment pairs at once (numpy)."""
    import numpy as np

    A = np.asarray(pa, dtype=float)
    B = np.asarray(pb, dtype=float)
    if len(A) < 2 or len(B) < 2:
        return []
    if (A[:, 0].max() < B[:, 0].min() or B[:, 0].max() < A[:, 0].min()
            or A[:, 1].max() < B[:, 1].min() or B[:, 1].max() < A[:, 1].min()):
        return []
    p0, r = A[:-1], A[1:] - A[:-1]
    q0, s = B[:-1], B[1:] - B[:-1]
    den = r[:, None, 0] * s[None, :, 1] - r[:, None, 1] * s[None, :, 0]
    qp = q0[None, :, :] - p0[:, None, :]
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (qp[..., 0] * s[None, :, 1] - qp[..., 1] * s[None, :, 0]) / den
        u = (qp[..., 0] * r[:, None, 1] - qp[..., 1] * r[:, None, 0]) / den
    ok = (np.abs(den) > 1e-12) & (t >= 0) & (t <= 1) & (u >= 0) & (u <= 1)
    ii, jj = np.nonzero(ok)
    hits: List[Tuple[float, float, float]] = []
    for i, j in zip(ii, jj):
        px, py = p0[i] + r[i] * t[i, j]
        ua = math.atan2(r[i, 1], r[i, 0])
        ub = math.atan2(s[j, 1], s[j, 0])
        d = abs(math.degrees(ua - ub)) % 180.0
        hits.append((float(px), float(py), min(d, 180.0 - d)))
    # a crossing exactly on a shared vertex is found twice — keep one
    ded: List[Tuple[float, float, float]] = []
    for h in hits:
        if all(math.hypot(h[0] - e[0], h[1] - e[1]) > 0.05 for e in ded):
            ded.append(h)
    return ded


def _histopolate(edges: Sequence[float], weights: Sequence[float],
                 step: float = 0.35, pin_ends: bool = False, monotone: bool = False,
                 tension: float = 0.0,
                 ) -> Tuple[List[float], List[float], List[float]]:
    """The least-curvature curve h(x) >= 0 over [edges[0], edges[-1]], zero at
    both ends, whose integral over [edges[g], edges[g+1]] is EXACTLY
    weights[g] / sum(weights) of the whole. Solved as an equality-constrained
    quadratic programme (KKT, numpy), with an active set for h >= 0. Areas are
    measured with the trapezoid rule on the returned polyline itself — the
    drawn curve, not a model of it — and every clump edge is a node.
    Returns (xs, hs, areas_normalised)."""
    import numpy as np

    xs: List[float] = []
    owner: List[int] = []
    for g in range(len(weights)):
        a, b = edges[g], edges[g + 1]
        n = max(3, int(round((b - a) / step)))
        for k in range(n):
            xs.append(a + (b - a) * k / n)
            owner.append(g)
    xs.append(edges[-1])
    X = np.array(xs)
    M = len(X)
    dx = np.diff(X)
    # second-difference operator on a non-uniform grid, weighted by cell size
    rows = []
    for i in range(1, M - 1):
        r = np.zeros(M)
        dl, dr = dx[i - 1], dx[i]
        r[i - 1] = 2.0 / (dl * (dl + dr))
        r[i] = -2.0 / (dl * dr)
        r[i + 1] = 2.0 / (dr * (dl + dr))
        rows.append(r * math.sqrt(0.5 * (dl + dr)))
    D = np.array(rows)
    Q = 2.0 * D.T @ D
    if tension > 0.0:
        # tension: a first-derivative term, so the curve pulls taut between
        # the clump constraints instead of ringing (a tension spline)
        R1 = np.zeros((M - 1, M))
        for i in range(M - 1):
            R1[i, i], R1[i, i + 1] = -1.0 / dx[i], 1.0 / dx[i]
            R1[i] *= math.sqrt(dx[i])
        Q = Q + 2.0 * tension ** 2 * R1.T @ R1
    tot = float(sum(weights))
    target = [w / tot for w in weights]
    # clump-area rows (trapezoid), then the two lips pinned to zero
    C = []
    for g in range(len(weights)):
        r = np.zeros(M)
        for i in range(M - 1):
            if owner[i] == g:
                r[i] += 0.5 * dx[i]
                r[i + 1] += 0.5 * dx[i]
        C.append(r)
    b = list(target)
    if pin_ends:
        for i in (0, M - 1):
            r = np.zeros(M)
            r[i] = 1.0
            C.append(r)
            b.append(0.0)
    # UNIMODAL: rising up to the heaviest clump, falling after it. Enforced by
    # an active set — wherever the unconstrained optimum wiggles the wrong way,
    # that step is pinned level and the programme re-solved.
    peak_g = max(range(len(weights)), key=lambda g: weights[g] / (edges[g + 1] - edges[g]))
    peak_i = owner.index(peak_g) + sum(1 for o in owner if o == peak_g) // 2
    flat: set = set()
    fixed: set = set()
    h = None
    for _ in range(200):
        Cf = list(C) + [np.eye(M)[i] for i in sorted(fixed)]
        bf = list(b) + [0.0] * len(fixed)
        for i in sorted(flat):
            r = np.zeros(M)
            r[i], r[i + 1] = -1.0, 1.0
            Cf.append(r)
            bf.append(0.0)
        Ca = np.array(Cf)
        K = np.block([[Q, Ca.T], [Ca, np.zeros((len(Cf), len(Cf)))]])
        rhs = np.concatenate([np.zeros(M), np.array(bf)])
        sol = np.linalg.lstsq(K, rhs, rcond=None)[0]
        h = sol[:M]
        neg = [i for i in range(M) if h[i] < -1e-12 and i not in fixed]
        bad = [i for i in range(M - 1) if monotone and i not in flat and (
            (i < peak_i and h[i + 1] < h[i] - 1e-12) or
            (i >= peak_i and h[i + 1] > h[i] + 1e-12))]
        if not neg and not bad:
            break
        fixed.update(neg)
        flat.update(bad)
    h = np.maximum(h, 0.0)
    areas = [0.0] * len(weights)
    for i in range(M - 1):
        areas[owner[i]] += 0.5 * (h[i] + h[i + 1]) * dx[i]
    s = sum(areas)
    return list(X), list(h), [a / s for a in areas]


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def attention_weaving_mirror_drain(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_q: int = 22,
    n_k: int = 16,
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
    LAST_STATS.clear()

    box = G.Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)
    GAP = 1.15

    # ---- the aperture -----------------------------------------------------
    c = 0.118 * W
    ap = Aperture(ax=x0 + 0.425 * W, ay=y0 + 0.620 * H, c=c)
    ax, ay = ap.ax, ap.ay

    # ---- the numbers ------------------------------------------------------
    d = 16

    def _unit():
        v = [rng.gauss() for _ in range(d)]
        n = math.sqrt(sum(t * t for t in v)) or 1.0
        return [t / n for t in v]

    Qv = [_unit() for _ in range(n_q)]
    Kv = [_unit() for _ in range(n_k)]
    # the value vectors live in the OUTPUT space: one component per lane
    # (n_q + n_k = 38), so Z = AV is a real 38-vector, one entry per lane.
    def _unit_n(n: int):
        v = [rng.gauss() for _ in range(n)]
        s = math.sqrt(sum(t * t for t in v)) or 1.0
        return [t / s for t in v]

    Vv = [_unit_n(n_q + n_k) for _ in range(n_k)]
    principal = n_q // 2
    # four keys carry a graded echo of the principal query — that is what makes
    # a real attention row PEAKED WITH A TAIL rather than flat or degenerate.
    for j, w in ((5, 0.90), (11, 0.70), (2, 0.54), (14, 0.40), (8, 0.30)):
        Kv[j] = [w * Qv[principal][t] + math.sqrt(1 - w * w) * Kv[j][t] for t in range(d)]
        n = math.sqrt(sum(t * t for t in Kv[j])) or 1.0
        Kv[j] = [t / n for t in Kv[j]]

    S = [[sum(Qv[i][t] * Kv[j][t] for t in range(d)) * math.sqrt(d)
          for j in range(n_k)] for i in range(n_q)]

    # temperature solved by bisection so a_max lands on the target exactly —
    # peaked, with a readable tail, never guessed.
    A_MAX_TARGET = 0.190          # 4.8x uniform: peaked, with a readable tail
    lo_t, hi_t = 0.05, 30.0
    for _ in range(64):
        mid = 0.5 * (lo_t + hi_t)
        if max(_softmax(S[principal], mid)) > A_MAX_TARGET:
            lo_t = mid
        else:
            hi_t = mid
    A = _softmax(S[principal], 0.5 * (lo_t + hi_t))
    a_max = max(A)
    Hbits = _entropy_bits(A)

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

    # ---- the grouped layout: clumps by weight, constant gap between ---------
    # A heavy key is a wide clump of filaments; a dead key is one crushed
    # hairline. The GAPS are constant, so only the CLUMPS carry the weight.
    # Keys are dealt around the peak — heaviest at the crown, then alternately
    # right and left in decreasing order (2 right for every 1 left, so the hill
    # is skewed, not symmetric). That is a permutation of the key index, which
    # attention is invariant to, and it makes the profile a single smooth hill
    # instead of 24 steps of noise or a cliff against a flat line.
    _srt = sorted(range(n_k), key=lambda j: -A[j])
    _lf: List[int] = []
    _rt: List[int] = []
    for i, j in enumerate(_srt):
        (_lf if (i and i % 3 == 0) else _rt).append(j)
    korder = list(reversed(_lf)) + _rt
    Ag = [A[j] for j in korder]
    pg = [p[j] for j in korder]

    FP = 0.95                    # filament pitch INSIDE a clump — the pen floor
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
    lane_key: List[int] = []           # lane -> GROUP index (0 = heaviest)
    for g in range(n_k):
        lane_key += [g] * pg[g]
    half_raw = slit_half
    lat = [q / slit_half for q in raw]                      # -1 .. 1 at the slit
    lat_rope = [q / (0.5 * ROPE_W) for q in raw_rope]       # -1 .. 1 downstream
    lands = list(raw)
    # Q and K INTERLEAVE inside the gate, dealt proportionally (n_q need not
    # equal n_k), so neither family owns a side of the slit.
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
    q_land = [lands[t] for t in q_idx]
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
    order = sorted(range(n_k), key=lambda j: psi_k_end[j])   # nested: K never self-crosses
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

    # ---- Q.K^T: one crossing per pair, over/under by sign(s_ij) ------------
    q_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_q)]
    k_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_k)]
    n_cross = 0
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
            (k_cuts[j] if S[i][j] >= 0.0 else q_cuts[i]).append((px, py, GAP))

    # ======================================================================
    # THE SOFTMAX PROFILE — one smooth hill, partitioned by AREA
    # ======================================================================
    # A histopolating curve: the least-curvature h(x) >= 0 on the slit, zero at
    # both lips, whose integral over clump g is EXACTLY a_g of the total. The
    # partition is carried by area, not by knot height, so nothing forces a
    # plateau: the silhouette is one hill and every clump still owns exactly
    # its weight. The fine curve is the running integral of the thick one.
    edges = [ax - c]
    for g in range(n_k - 1):
        edges.append(ax + group_span[g][1] + 0.5 * GAPG)
    edges.append(ax + c)
    hx, hy, h_area = _histopolate(edges, Ag)
    LAST_STATS['edges'] = list(edges); LAST_STATS['Ag'] = list(Ag)
    LAST_STATS['means'] = [round(Ag[g] / (edges[g + 1] - edges[g]), 4) for g in range(n_k)]
    LAST_STATS['widths'] = [round(edges[g + 1] - edges[g], 2) for g in range(n_k)]
    ZMAX = 0.074 * H
    hscale = ZMAX / max(hy)
    prof = [(ax - c, ay)] + [(px, ay + py * hscale) for px, py in zip(hx, hy)] + [(ax + c, ay)]
    # running integral (trapezoid on the DRAWN polyline) -> the cumulative
    cum_v = [0.0]
    for k in range(1, len(hx)):
        cum_v.append(cum_v[-1] + 0.5 * (hy[k] + hy[k - 1]) * (hx[k] - hx[k - 1]))
    cum_end_raw = cum_v[-1]
    CUM_H = ZMAX * 1.08
    cum_poly = [(px, ay + CUM_H * v / cum_end_raw) for px, v in zip(hx, cum_v)]
    zig_r = _resample(prof, 0.8)

    for i in range(n_q):
        for cx_, cy_ in _crossings(q_polys[i], zig_r):
            q_cuts[i].append((cx_, cy_, 1.0))
    for j in range(n_k):
        for cx_, cy_ in _crossings(k_polys[j], zig_r):
            k_cuts[j].append((cx_, cy_, 1.0))

    # ======================================================================
    # LABELS FIRST — their halos cut every strand that would run through them
    # ======================================================================
    halos: List[G.Region] = []
    labels: List[Tuple[str, float, float, float, Optional[int]]] = []

    def label(text: str, x: float, y: float, h: float, pen, pad: float = 1.3):
        w = _text_width(text, h)
        labels.append((text, x, y, h, pen))
        halos.append(G.Rect(x - pad, y - pad, x + w + pad, y + h + pad))
        return w

    # ---- the lower system: the phi < 0 half of the SAME aperture ----------
    # Below the wall the lanes are the streamlines psi = const of the same
    # elliptic coordinates, continued to phi < 0: each leaves the slit exactly
    # where its Q or K strand arrived, vertical — the mirror sunburst. Z = AV
    # BENDS the aftermath down-right: the stream coordinate is scaled
    #     psi' = psi * m(|phi|),   m = KB + (1 - KB) / cosh(BR * |phi|)
    # m = 1 at the slit (so the join is exact and tangent-continuous) and falls
    # to KB far out, folding the 180 deg mirror fan into a KB*180 deg wedge that
    # opens down-right and leaves the lower-left to the title. m depends only
    # on |phi|, so at every depth psi -> psi' is monotone: lanes never cross.
    # BR is the fastest bend the pen allows — the lane pitch below the wall is
    # measured and never falls under the floor.
    KB, BR = 0.330, 1.30

    def bend(s: float) -> float:
        return KB + (1.0 - KB) / math.cosh(BR * s)

    def low(s: float, psi: float) -> Tuple[float, float]:
        return ap.pt(-s, psi * bend(s))

    psi_lane = [ap.psi_for_slit_x(o) for o in lands]
    S_LANE = 3.5
    NL = 360

    def lane_s(k: int) -> float:
        return S_LANE * (k / NL) ** 1.35

    def lane_path(t: int) -> Poly:
        return [low(lane_s(k), psi_lane[t]) for k in range(NL + 1)]

    lane_polys = [_resample(lane_path(t), 1.1) for t in range(n_lane)]
    slit_err = max(abs(lane_polys[t][0][0] - (ax + lands[t])) for t in range(n_lane))

    # ---- V: the second spiral family, the mirror of K ----------------------
    # K sweeps the Q fan high above the wall and falls into the slit. V comes
    # in from the left rim and sweeps the Z fan along the ORTHOGONAL
    # TRAJECTORIES of the drawn lanes (the equipotentials of the bent flow),
    # pitched outward by V_PITCH so each one is a spiral — so it crosses every
    # lane exactly once at 90 - V_PITCH deg. It NEVER touches the slit: V joins
    # after the waist. Nested by rank (heaviest innermost, nearest the waist).
    V_PITCH = math.radians(-24.0)       # negative: V spirals INWARD, like K
    GAP_LO = 0.62            # the fan is finer than the storm: a tighter gap

    def _jac(s: float, psi: float):
        e = 1e-4
        p0 = low(s, psi)
        ps = low(s + e, psi)
        pp = low(s, psi + e)
        return p0, ((ps[0] - p0[0]) / e, (ps[1] - p0[1]) / e), \
            ((pp[0] - p0[0]) / e, (pp[1] - p0[1]) / e)

    def v_trace(s0: float, psi0: float, psi_end: float, pitch: float = V_PITCH,
                step: float = 0.7) -> Poly:
        s, psi = s0, psi0
        pts: Poly = []
        for _ in range(900):
            p0, Js, Jp = _jac(s, psi)
            pts.append(p0)
            if psi <= psi_end or s < 0.62 or not (x0 - 2 < p0[0] < x1 + 2 and y0 - 2 < p0[1] < y1 + 2):
                break
            tl = math.hypot(*Js) or 1.0
            T = (Js[0] / tl, Js[1] / tl)                # lane direction (outward)
            N = (T[1], -T[0])                           # perpendicular
            if N[0] * Jp[0] + N[1] * Jp[1] > 0:         # point toward DEcreasing psi
                N = (-N[0], -N[1])
            D = (N[0] * math.cos(pitch) + T[0] * math.sin(pitch),
                 N[1] * math.cos(pitch) + T[1] * math.sin(pitch))
            det = Js[0] * Jp[1] - Js[1] * Jp[0]
            if abs(det) < 1e-12:
                break
            ds = (D[0] * Jp[1] - D[1] * Jp[0]) / det
            dp = (Js[0] * D[1] - Js[1] * D[0]) / det
            s += ds * step
            psi += dp * step
        LAST_STATS.setdefault('v_s_min', []).append(round(s, 3))
        return pts

    PSI_A, PSI_B = 0.955 * math.pi, 0.100 * math.pi
    v_rank = list(range(n_k))                       # group order: heaviest first
    s_in = [1.40 + 1.00 * (r / max(1, n_k - 1)) ** 0.85 for r in v_rank]

    # V starts mid-air on the fan's open (left) flank — the mirror of K's
    # mid-air start on the right of the storm — and leaves through the right
    # frame. No approach bundle: nothing on the sheet but the order.
    # the inner (heaviest) spirals wind more gently so none of them sinks
    # toward the slit before it has crossed the last lane
    v_pitch = [math.radians(5.0 - 29.0 * (r / max(1, n_k - 1)) ** 0.8) for r in v_rank]
    v_polys = [_resample(v_trace(s_in[g], PSI_A, PSI_B, v_pitch[g]), 1.1) for g in range(n_k)]

    # ---- Z = AV, computed: lane t is output component t --------------------
    Zt = [sum(Ag[g] * Vv[korder[g]][t] for g in range(n_k)) for t in range(n_lane)]

    lane_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_lane)]
    v_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_k)]
    n_vx = 0
    v_angles: List[float] = []
    per_pair: List[int] = []
    for g in range(n_k):
        vj = Vv[korder[g]]
        for t in range(n_lane):
            hits = _crossings_ang(v_polys[g], lane_polys[t])
            on = [(px, py, a) for px, py, a in hits
                  if x0 + 0.5 < px < x1 - 0.5 and y0 + 0.5 < py < y1 - 0.5]
            per_pair.append(len(on))
            if len(on) != 1:
                LAST_STATS.setdefault('miss', []).append((g, t, len(hits)))
            for px, py, a in on:
                n_vx += 1
                v_angles.append(a)
                # over/under is the SIGN of that value component
                if vj[t] >= 0.0:
                    lane_cuts[t].append((px, py, GAP_LO))
                else:
                    v_cuts[g].append((px, py, GAP_LO))

    # nesting: V never crosses V, lane never crosses lane
    vv_x = sum(len(_crossings_ang(v_polys[g], v_polys[h_]))
               for g in range(n_k) for h_ in range(g + 1, n_k))
    ll_x = sum(len(_crossings_ang(lane_polys[t], lane_polys[t + 1])) for t in range(n_lane - 1))
    LAST_STATS.update(vv_crossings=vv_x, lane_self_crossings=ll_x)
    # lane pitch below the wall, measured at matched depths
    lp_min = 1e9
    for k in range(2, NL + 1, 3):
        s = lane_s(k)
        pts = [low(s, psi_lane[t]) for t in range(n_lane)]
        for a_, b_ in zip(pts, pts[1:]):
            if x0 < a_[0] < x1 and y0 < a_[1] < y1:
                dd = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                if dd < lp_min:
                    lp_min = dd
                    LAST_STATS["pitch_at"] = (round(a_[0], 1), round(a_[1], 1), round(s, 3))

    # ---- labels (placed, then honoured as halos) --------------------------
    sm_h = 2.6
    cum_end = cum_poly[-1]
    one_txt = "1.000"
    label(one_txt, cum_end[0] + 3.2, cum_end[1] - 1.2, 2.4, k_black, pad=1.0)
    label(_spaced("SOFTMAX"), ax + c + 3.2, ay + 2.4, sm_h, k_black, pad=1.0)
    # the title is a mass the flow must respect: its boxes are halos too
    th = 15.0
    ty = y0 + 0.205 * H
    for word, yy in (("SUMS", ty), ("TO ONE", ty - th * 1.62)):
        ww = giant_type_width(word, th, spaced=True)
        halos.append(G.Rect(x0 + 0.5 - 1.5, yy - 2.5, x0 + 1.5 + ww + 2.5, yy + th + 2.5))

    # ======================================================================
    # EMIT — back to front
    # ======================================================================
    hal = G.Union(*halos) if halos else None

    def cut_halo(polys_cmds_src: Poly) -> List[Poly]:
        runs = G.clip(polys_cmds_src, box, keep="inside")
        if hal is not None:
            runs = [r for run in runs for r in G.clip(run, hal, keep="outside")]
        return runs

    # scaffold: the confocal equipotentials, dotted, behind — above the wall the
    # true ellipses, below it the SAME ellipses carried through the bend.
    for phi in (0.72, 1.48):
        up = [ap.pt(phi, math.pi * t / 300.0) for t in range(301)]
        for run in cut_halo(_resample(up, 1.0)):
            out += _dotted(run, k_black, box, on=3, off=4, f=feed)
    for s in (0.62,):
        dn = [low(s, math.pi * t / 300.0) for t in range(301)]
        for run in cut_halo(_resample(dn, 1.0)):
            out += _dotted(run, k_black, box, on=2, off=5, f=feed)

    # the storm (unchanged)
    for i in range(n_q):
        for run in cut_halo(q_polys[i]):
            out += _cut_and_emit(run, q_cuts[i], k_q, box, f=feed,
                                 passes=2 if i == principal else 1, pitch=0.34)
    for j in range(n_k):
        for run in cut_halo(k_polys[j]):
            out += _cut_and_emit(run, k_cuts[j], k_k, box, f=feed,
                                 passes=2 if p[j] >= 4 else 1, pitch=0.34)

    # THE WALL: one black rule, one hole
    for k in range(5):
        dy = -0.62 + 0.31 * k
        out += _poly([(x0 + 0.4, ay + dy), (ax - c, ay + dy)], color=k_black, f=feed)
        out += _poly([(ax + c, ay + dy), (x1 - 0.4, ay + dy)], color=k_black, f=feed)

    # the drain: Z lanes, then V spirals
    for t in range(n_lane):
        for run in cut_halo(lane_polys[t]):
            out += _cut_and_emit(run, lane_cuts[t], k_z, box, f=feed)
    for g in range(n_k):
        for run in cut_halo(v_polys[g]):
            out += _cut_and_emit(run, v_cuts[g], k_v, box, f=feed,
                                 passes=2 if pg[g] >= 4 else 1, pitch=0.34)

    # the profile ON TOP: cumulative (fine) first, then the hill (5 passes)
    for sub in G.clip(cum_poly, box, keep="inside"):
        out += _poly(sub, color=k_black, f=feed)
    out += fill_disc(cum_end[0], cum_end[1], 0.8, spacing=0.3, pen=k_black, f=feed)
    for k in range(5):
        sil = [(px, py + 0.30 * k) for px, py in prof]
        for sub in G.clip(sil, box, keep="inside"):
            out += _poly(sub, color=k_black, f=feed)
    # clump boundaries: registration ticks ON THE WALL LINE, in the gaps
    for ex in edges[1:-1]:
        out += _poly([(ex, ay - 1.0), (ex, ay + 1.4)], color=k_black, f=feed)

    # ---- reeds: where the strands leave the sheet -------------------------
    def reed(polys: Sequence[Poly], pen, lens=None, edges_=("top", "right", "left")):
        for n_, pl in enumerate(polys):
            L = 3.0 if lens is None else lens[n_]
            for r in G.clip(pl, box, keep="inside"):
                for e in (r[0], r[-1]):
                    if "top" in edges_ and e[1] > y1 - 1.2:
                        out.extend(_poly([(e[0], y1 - 0.6), (e[0], y1 - 0.6 - L)],
                                         color=pen, f=feed))
                    elif "right" in edges_ and e[0] > x1 - 1.2:
                        out.extend(_poly([(x1 - 0.6, e[1]), (x1 - 0.6 - L, e[1])],
                                         color=pen, f=feed))
                    elif "bottom" in edges_ and e[1] < y0 + 1.2:
                        out.extend(_poly([(e[0], y0 + 0.6), (e[0], y0 + 0.6 + L)],
                                         color=pen, f=feed))
                    elif "left" in edges_ and e[0] < x0 + 1.2:
                        out.extend(_poly([(x0 + 0.6, e[1]), (x0 + 0.6 + L, e[1])],
                                         color=pen, f=feed))

    reed(q_polys, k_black)
    reed(k_polys, k_black)
    zmax_abs = max(abs(z) for z in Zt) or 1.0
    # the outlet reed IS the output: tick length = |z_t|, z = sum_j a_j v_j
    reed(lane_polys, k_black, lens=[1.2 + 4.2 * abs(z) / zmax_abs for z in Zt],
         edges_=("right", "bottom"))
    reed(v_polys, k_black, edges_=("right", "bottom"))

    # ---- type: Deco spaced caps, monumental, in the lower-left void --------
    out += giant_type("SUMS", x0 + 1.5, ty, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
    out += giant_type("TO ONE", x0 + 1.5, ty - th * 1.62, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
    # the fan's open flank (the leftmost lane) is the right margin of the
    # type: every footer line is fitted to the room the flow leaves it.
    edge = [pt for pt in lane_polys[0] if y0 <= pt[1] <= ay]

    def x_edge(y: float) -> float:
        best = x1
        for p0_, p1_ in zip(edge, edge[1:]):
            if min(p0_[1], p1_[1]) <= y <= max(p0_[1], p1_[1]) and p0_[1] != p1_[1]:
                best = min(best, p0_[0] + (p1_[0] - p0_[0]) * (y - p0_[1]) / (p1_[1] - p0_[1]))
        return best

    LEAD = 4.8
    fy = ty - th * 2.40
    lines = [
        ("ATTENTION AS A FLOW THROUGH ONE APERTURE", 2.5),
        (f"SIGMA A = 1.000   A MAX = {a_max:.3f}   H = {Hbits:.2f} / {math.log(n_k, 2):.2f} BITS", 1.9),
        (f"{n_cross} / {n_q*n_k} SCORES CROSS    {n_vx} / {n_k*n_lane} VALUES CROSS", 1.9),
        (f"{total_f} IN, {n_lane} OUT    SLIT {2*c:.0f} MM    PITCH {min(min_pitch, lp_min):.2f} MM", 1.9),
    ]
    for k, (txt, hh) in enumerate(lines):
        yy = fy - k * LEAD
        room = x_edge(yy + hh) - 5.0 - (x0 + 2.0)
        s_txt = _spaced(txt)
        while _text_width(s_txt, hh) > room and hh > 1.4:
            hh -= 0.05
        out += _stroke_text(s_txt, x0 + 2.0, yy, hh, color=k_black, f=feed)
    LAST_STATS["footer_room"] = [round(x_edge(fy - k * LEAD) - x0, 1) for k in range(4)]

    # bundle marks — V and Z = AV stand in the silence on the fan's open flank
    # both marks hang off ONE vertical: 6 mm left of where the innermost V
    # spiral starts, which is also where the flow's open flank begins.
    vs = v_polys[0][0]
    x_rule = min(vs[0], x_edge(ay - 0.105 * H)) - 6.0
    vl = "V"
    out += _stroke_text(vl, x_rule - _text_width(vl, 4.6), vs[1] - 2.3, 4.6,
                        color=k_v, f=feed)
    zl = "Z = AV"
    zy = ay - 0.105 * H
    out += _stroke_text(zl, x_rule - _text_width(zl, 4.6), zy, 4.6, color=k_z, f=feed)
    out += _stroke_text(_spaced("Q"), x0 + 0.012 * W, y1 - 0.135 * H, 4.6, color=k_q, f=feed)
    out += _stroke_text(_spaced("K"), x1 - 0.075 * W, y1 - 0.052 * H, 4.6, color=k_k, f=feed)
    for text, lx, ly, lh, pen in labels:
        out += _stroke_text(text, lx, ly, lh, color=pen, f=feed)

    LAST_STATS.update(
        sum_a=sum(A), a_max=a_max, entropy_bits=Hbits, n_k=n_k, n_q=n_q,
        filaments_in=total_f, filaments_out=n_lane, sum_p=sum(p),
        area_err=max(abs(h_area[g] - Ag[g]) for g in range(n_k)),
        prof_min=min(hy), cum_end=cum_end_raw, min_pitch_slit=min_pitch,
        min_pitch_fan=lp_min, qk_crossings=n_cross, v_crossings=n_vx,
        v_pairs_once=sum(1 for n_ in per_pair if n_ == 1), v_pairs=len(per_pair),
        v_angle_min=min(v_angles) if v_angles else None,
        v_angle_med=sorted(v_angles)[len(v_angles) // 2] if v_angles else None,
        z=Zt, slit_err=slit_err,
    )
    return out
