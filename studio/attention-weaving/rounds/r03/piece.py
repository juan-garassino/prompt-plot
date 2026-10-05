"""SUMS TO ONE — attention transposed to the flow field through a single slit.

r03 of the `attention-weaving` family. r01/r02 recreate the reference braid.
This round keeps what the reference is ABOUT — strand craft, the inevitability
of the constriction, Q and K meeting before the waist and V only after — and
transposes it into a different abstract ORDER.

ORDER: potential flow through ONE APERTURE in a wall — a double sunburst whose
mirror plane is a black rule with one hole in it. Everything on the sheet is
the elliptic coordinate system of that aperture:

    z = A + c*cosh(phi + i*psi)     x = ax + c*cosh(phi)*cos(psi)
                                     y = ay + c*sinh(phi)*sin(psi)

  * phi > 0 is above the wall, phi < 0 below, phi = 0 IS the slit.
  * Every streamline psi = const crosses the wall at exactly one point,
    x = ax + c*cos(psi) — inside the slit, always. "Everything passes through
    one constriction" is not a narrative here, it is the definition of the
    coordinate system.
  * The orthogonal family phi = const are the confocal ellipses (the
    equipotentials) — the only scaffold, dotted, behind.

MECHANISM -> GEOMETRY (exact, one line each)
  Q_i       a streamline psi_i                        (a query is a direction)
  K_j       a spiral that sweeps the whole Q fan high in the sheet and then
            drops into the slit    (a key is compared against every query, once)
  s_ij      the crossing of K_j and Q_i; sign(s_ij) decides over/under
  softmax   TWICE, exactly, at the same place:
              WIDTH  — filament group j holds p_j = round(a_j * N) filaments,
                       sum(p_j) = N; the groups are packed with a constant gap,
                       so a heavy key is a wide clump and a dead key is one
                       crushed hairline. Same layout at the slit and in the rope.
              HEIGHT — the stepped profile standing on the wall: step j is that
                       clump wide and a_j tall. The steps tile the slit exactly.
  count     N filaments enter the slit, N leave. Nothing is born below the wall
            and nothing dies above it.
  Z = AV    the cable leaves the gate as bare green hairlines and only gains
            its gold where V is woven in — every gold filament is absorbed into
            its own lane group, interlacing over/under on the way.

CANON: ART DECO (STYLES.md #2) — ray fans, nested arcs, the stepped ziggurat,
thin/thick by passes, wide-tracked spaced caps, cream stock. THE TWIST: the
Deco sunburst is the machine age's emblem of radiance pouring outward. Here it
is drawn twice, mirrored, and the mirror plane is a wall with one small hole.
All that radiance above; below, a thin rope and a large silence. The sunburst
is a drain, and the silence is the probability mass the softmax threw away.

Contract: attention_weaving(rng, bounds, colors=3) -> list[GCodeCommand]
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


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def attention_weaving(
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
    Vv = [_unit() for _ in range(n_k)]          # the value vectors
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

    # ---- the stepped profile: the distribution, standing on the wall -------
    # step j is its own clump wide and a_j tall: width = the weight quantised
    # to filaments, height = the weight exactly. The steps tile the slit.
    ZMAX = 0.080 * H
    pad = GAPG * 0.5
    # knots: the EXACT weight at the EXACT centre of its own clump. Height is
    # linear in a_g (no gamma), so the curve's height IS the weight.
    kx: List[float] = []
    ky: List[float] = []
    bx: List[float] = []                       # clump boundaries (registration)
    cxs: List[float] = []                      # clump centres (the knot discs)
    for g in range(n_k):
        g0, g1 = group_span[g]
        lo = ax - c if g == 0 else ax + g0 - pad
        hi = ax + c if g == n_k - 1 else ax + g1 + pad
        ins = 0.26 * (hi - lo)
        h = ZMAX * Ag[g] / a_max
        # TWO knots per clump: the curve is flat at exactly a_g across the
        # middle of its own clump and only bends in the outer third, so the
        # profile is smooth AND every step is still its exact height and width.
        kx += [lo + ins, hi - ins]
        ky += [h, h]
        cxs.append(0.5 * (lo + hi))
        if g < n_k - 1:
            bx.append(hi)
    edges_span = sum((ax + c if g == n_k - 1 else ax + group_span[g][1] + pad)
                     - (ax - c if g == 0 else ax + group_span[g][0] - pad)
                     for g in range(n_k))
    prof = [(px, ay + py) for px, py in _pchip(kx, ky, per=12)]
    zig: Poly = [(ax - c, ay)] + prof + [(ax + c, ay)]
    zig_r = _resample(zig, 0.8)

    # the cumulative: monotone by construction, and it arrives at EXACTLY 1.000
    cum, acc = [0.0], 0.0
    cux = [ax - c]
    for g in range(n_k):
        acc += Ag[g]
        cum.append(acc)
        cux.append(ax + group_span[g][1] + pad if g < n_k - 1 else ax + c)
    cum[-1] = 1.0
    cum_poly = [(px, ay + ZMAX * py) for px, py in _pchip(cux, cum, per=12)]

    for i in range(n_q):
        for hx, hy in _crossings(q_polys[i], zig_r):
            q_cuts[i].append((hx, hy, 1.0))
    for j in range(n_k):
        for hx, hy in _crossings(k_polys[j], zig_r):
            k_cuts[j].append((hx, hy, 1.0))

    # ---- scaffold: the confocal ellipses (equipotentials), dotted, behind --
    for phi in (0.72, 1.48):
        up = [ap.pt(phi, math.pi * t / 300.0) for t in range(301)]
        out += _dotted(_resample(up, 1.0), k_black, box, on=3, off=4, f=feed)
    for phi, o in ((0.62, 4), (1.62, 5)):
        dn = [ap.pt(-phi, math.pi * t / 300.0) for t in range(301)]
        out += _dotted(_resample(dn, 1.0), k_black, box, on=2, off=o, f=feed)

    # ---- the storm --------------------------------------------------------
    for i in range(n_q):
        out += _cut_and_emit(q_polys[i], q_cuts[i], k_q, box, f=feed,
                             passes=2 if i == principal else 1, pitch=0.34)
    for j in range(n_k):
        out += _cut_and_emit(k_polys[j], k_cuts[j], k_k, box, f=feed,
                             passes=2 if p[j] >= 4 else 1, pitch=0.34)

    # ---- THE WALL: one black rule, one hole -------------------------------
    for k in range(5):
        dy = -0.62 + 0.31 * k
        out += _poly([(x0 + 0.4, ay + dy), (ax - c, ay + dy)], color=k_black, f=feed)
        out += _poly([(ax + c, ay + dy), (x1 - 0.4, ay + dy)], color=k_black, f=feed)

    # ---- below the wall: the rope ----------------------------------------
    # A STEEP fall out of the gate, then a hard turn: the cable runs nearly
    # vertical exactly where V cuts across it, so every crossing is at ~55 deg
    # and reads as an event instead of two curves lying alongside each other.
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

        sx = cr(pprev[0], pa[0], pb[0], pnext[0])
        sy = cr(pprev[1], pa[1], pb[1], pnext[1])
        nx, ny = pb[0] - pa[0], pb[1] - pa[1]
        L = math.hypot(nx, ny) or 1.0
        return sx, sy, -ny / L, nx / L

    def lane_path(idx: int) -> Poly:
        psi = ap.psi_for_slit_x(lands[idx])
        pts: Poly = []
        for t in range(181):
            u = t / 180.0
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

    # ---- V: one gold filament per key, entering from the left rim ---------
    # Each V is absorbed into its OWN lane group, and the absorption stations
    # march down the rope (heaviest first, at the gate; the tail far downstream)
    # so V reads as a comb feeding the rope along its length, not as a lens.
    # V_j is absorbed into lane group j — value j added to lane j, which is what
    # Z = AV does. On the way in it crosses whatever groups lie between it and
    # the flank, and every one of those crossings is a real over/under decided
    # by the sign of that value component.
    vt = [0.400 - 0.270 * (g / max(1, n_k - 1)) for g in range(n_k)]
    v_polys: List[Poly] = []
    v_pass = [3 if pg[g] >= 4 else 2 for g in range(n_k)]
    knot = (x0 + 0.300 * W, y0 + 0.535 * H)     # each bundle's own waist
    for g in range(n_k):
        idxs = [t for t in range(n_lane) if lane_key[t] == g]
        lp = lane_polys[idxs[len(idxs) // 2]]
        u_t = vt[g]
        tgt = lp[int(u_t * (len(lp) - 1))]
        sx, sy, nx, ny = _spine_at(u_t)
        # approach from the flank this lane is NEAREST: the unimodal deal puts
        # the heavy keys mid-cable, so the deepest cuts are the heaviest values
        # and the tail keys graze their own edge.
        lat_g = lat[idxs[len(idxs) // 2]]
        r = g / max(1, n_k - 1)
        y_entry = y0 + (0.452 + 0.158 * r) * H
        start = (x0 - 0.05 * W, y_entry)
        side = 1.0 if ((start[0] - sx) * nx + (start[1] - sy) * ny) >= 0 else -1.0
        c2 = (tgt[0] + nx * side * 0.100 * H, tgt[1] + ny * side * 0.100 * H)
        # part-converge on a shared knot so V travels as ONE bundle and only
        # opens into its comb in the last stretch before the cable.
        own = (0.50 * start[0] + 0.50 * c2[0], y_entry - 0.006 * H)
        c1 = (0.40 * knot[0] + 0.60 * own[0], 0.40 * knot[1] + 0.60 * own[1])
        _ = lat_g

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
    n_vx = 0
    # A lane is one component of the value vector, so the over/under at each
    # V x lane crossing is sign(v_j[component]) — real data, exactly as
    # sign(s_ij) is upstream. That is what makes this an interlace and not an
    # overlap: each gold filament alternates over and under as it cuts through.
    for g in range(n_k):
        vj = Vv[korder[g]]
        q25 = sorted(vj)[max(0, len(vj) // 4 - 1)]     # this vector's lower quartile
        for t in range(n_lane):
            for hx, hy in _crossings(v_polys[g], lane_polys[t]):
                n_vx += 1
                # gold dips UNDER only where its own component falls in the
                # lowest quartile — one family dominant, which is what a weave
                # looks like, and still decided by the value matrix.
                over = vj[t % d] > q25
                (lane_cuts[t] if over else v_cuts[g]).append(
                    (hx, hy, 1.25 if over else 0.9))

    # ---- emit the rope: DASHED before its V, solid after ------------------
    for t in range(n_lane):
        lp = lane_polys[t]
        m = int(vt[lane_key[t]] * (len(lp) - 1))
        ycut = lp[m][1]
        head, tail = lp[: m + 1], lp[m:]
        hc = [cc for cc in lane_cuts[t] if cc[1] > ycut]
        tc = [cc for cc in lane_cuts[t] if cc[1] <= ycut]
        out += _cut_and_emit(head, hc, k_z, box, f=feed)
        out += _cut_and_emit(tail, tc, k_z, box, f=feed)

    for g in range(n_k):
        out += _cut_and_emit(v_polys[g], v_cuts[g], k_v, box, f=feed,
                             passes=v_pass[g], pitch=0.36)

    # ---- the profile sits ON TOP ------------------------------------------
    # the cumulative first (fine, behind), then the density silhouette
    for sub in G.clip(cum_poly, box, keep="inside"):
        out += _poly(sub, color=k_black, f=feed)
    out += _poly([(ax + c - 4.0, ay + ZMAX), (ax + c + 3.0, ay + ZMAX)], color=k_black, f=feed)
    out += fill_disc(ax + c, ay + ZMAX, 0.85, spacing=0.3, pen=k_black, f=feed)
    out += _poly([(ax + c, ay + ZMAX), (ax + c + 4.6, ay + ZMAX)], color=k_black, f=feed)
    for k in range(5):
        sil = [(px, py + 0.30 * k) for px, py in zig]
        for sub in G.clip(sil, box, keep="inside"):
            out += _poly(sub, color=k_black, f=feed)
    # registration: the partition is still discrete — a short tick hanging from
    # the curve at every clump boundary.
    for px in bx:
        h = _pchip_at(kx, ky, px)
        out += _poly([(px, ay + h), (px, ay + h - 2.6)], color=k_black, f=feed)
    # every knot carries its weight as AREA: r = r0*sqrt(a_g/a_max)
    for g in range(n_k):
        r = 1.60 * math.sqrt(Ag[g] / a_max)
        out += fill_disc(cxs[g], ay + ZMAX * Ag[g] / a_max,
                         max(0.32, r), spacing=0.32, pen=k_black, f=feed)

    # ---- reeds: where the strands leave the sheet -------------------------
    def reed(polys: Sequence[Poly], pen, edges=("top", "right", "left")):
        for pl in polys:
            for r in G.clip(pl, box, keep="inside"):
                for e in (r[0], r[-1]):
                    if "top" in edges and e[1] > y1 - 1.2:
                        out.extend(_poly([(e[0], y1 - 0.6), (e[0], y1 - 3.6)],
                                         color=pen, f=feed))
                    elif "right" in edges and e[0] > x1 - 1.2:
                        out.extend(_poly([(x1 - 0.6, e[1]), (x1 - 3.6, e[1])],
                                         color=pen, f=feed))
                    elif "left" in edges and e[0] < x0 + 1.2:
                        out.extend(_poly([(x0 + 0.6, e[1]), (x0 + 3.6, e[1])],
                                         color=pen, f=feed))

    reed(q_polys, k_black)
    reed(k_polys, k_black)
    reed(lane_polys, k_black, edges=("right",))
    reed(v_polys, k_black, edges=("left",))

    # ---- type: Deco spaced caps, monumental, standing in the silence ------
    th = 18.0
    while giant_type_width("TO ONE", th, spaced=True) > 0.62 * W and th > 8:
        th -= 0.5
    ty = y0 + 0.205 * H
    out += giant_type("SUMS", x0 + 1.5, ty, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
    out += giant_type("TO ONE", x0 + 1.5, ty - th * 1.62, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
    sub = _spaced("ATTENTION AS A FLOW THROUGH ONE APERTURE")
    out += _stroke_text(sub, x0 + 2.0, ty - th * 2.55, 2.6, color=k_black, f=feed)

    f1 = _spaced(f"SIGMA A = 1.000   A MAX = {a_max:.3f}   H = {Hbits:.2f} OF {math.log(n_k, 2):.2f} BITS")
    f2 = _spaced(f"{n_cross} OF {n_q*n_k} SCORES CROSS    "
                 f"{total_f} FILAMENTS IN, {total_f} OUT")
    f3 = _spaced(f"SLIT {2*c:.0f} OF {W:.0f} MM    LANE PITCH {min_pitch:.2f} MM")
    out += _stroke_text(f1, x0 + 2.0, y0 + 0.072 * H, 2.0, color=k_black, f=feed)
    out += _stroke_text(f2, x0 + 2.0, y0 + 0.044 * H, 2.0, color=k_black, f=feed)
    out += _stroke_text(f3, x0 + 2.0, y0 + 0.016 * H, 2.0, color=k_black, f=feed)

    LAST_STATS.update(
        sum_a=sum(A), a_max=a_max, entropy_bits=Hbits, n_k=n_k, n_q=n_q,
        filaments_in=total_f, filaments_out=n_lane, sum_p=sum(p),
        partition_span=edges_span, slit=2 * c,
        knot_err=max(abs(_pchip_at(kx, ky, cxs[g]) - ZMAX * Ag[g] / a_max)
                     for g in range(n_k)),
        cum_end=cum[-1], min_pitch=min_pitch, qk_crossings=n_cross, v_crossings=n_vx,
    )

    # bundle marks
    out += _stroke_text(_spaced("Q"), x0 + 0.012 * W, y1 - 0.135 * H, 4.6, color=k_q, f=feed)
    out += _stroke_text(_spaced("K"), x1 - 0.075 * W, y1 - 0.052 * H, 4.6, color=k_k, f=feed)
    out += _stroke_text(_spaced("V"), x0 + 0.020 * W, y0 + 0.620 * H, 4.6, color=k_v, f=feed)
    out += _stroke_text(_spaced("Z = A V"), x1 - 0.275 * W, y0 + 0.130 * H, 4.6,
                        color=k_z, f=feed)
    sm = _spaced("SOFTMAX")
    smw = _text_width(sm, 2.6)
    out += _stroke_text(sm, min(x1 - smw - 2.0, ax + c + 13.0), ay + 5.0, 2.6,
                        color=k_black, f=feed)

    return out
