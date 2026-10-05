"""SUMS TO ONE — r07 (iterate) of `attention-weaving`, parent r06.
Built on encoding.md Revision 1 (2026-09-29): ONE REED, ONE CLOTH.

  ABOVE THE WALL  unchanged order: 22 Q streamlines of the aperture's elliptic
                  coordinates + 16 K spirals; Q over K where s_ij >= 0. Every K
                  turns onto its own streamline and ends ON THE HILL, inside its
                  own equal bin, at maximum clearance from the lanes.
  THE SLIT (R3)   52 mm, 16 equal bins of 3.25 mm. The hill is the exact-area
                  least-curvature histopolant of Q11's row, ZERO at both cut
                  edges (no shelf, no jamb step), crown in bin 7.
  THE LANES (R2)  22 queries cross at ONE pitch (2.25 mm); position is order
                  only (seriated on B), Q11 pinned on the centre line.
  THE CLOTH (R1)  the 22 lanes continue as the Z = AV warp, ruled by the normals
                  of the upper selvage (so every lane is an offset of it and the
                  picks meet every lane square). ONE gold weft of 16 picks: pick
                  g carries the value of the key in hill bin g-1; gold over green
                  <=> a_ij > 1/16 at all 352 crossings, no override. Picks only
                  where the lanes stand >= 3.6 mm apart, so no float is < 5 mm.

CANON: Deco, flat (the fan-shell under the sunburst). LINEAGE: Anni Albers,
*Black-White-Gold I* (1950): over/under as information.
Contract: attention_weaving_reed(rng, bounds, colors=6)
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

# pen slots = layer order, light -> dark: goldenrod, dodgerblue, crimson, darkgreen, black, black(text)
V_PEN, K_PEN, Q_PEN, Z_PEN, BLACK, TEXT = 0, 1, 2, 3, 4, 5

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



def _histopolate_ramp_once(edges, weights, step, beta):
    import numpy as np
    """Least-curvature h >= 0 with EXACT trapezoid area a_g over each bin, and
    a RAMP condition instead of a plateau: rising up to the peak bin, falling
    after it, every step at least beta x the local slope of the bin-mean
    staircase. Active set (primal): violated ramp rows become equalities."""
    xs, owner = [], []
    nb = len(weights)
    for g in range(nb):
        a, b = edges[g], edges[g + 1]
        n = max(3, int(round((b - a) / step)))
        for k in range(n):
            xs.append(a + (b - a) * k / n)
            owner.append(g)
    xs.append(edges[-1]); owner.append(nb - 1)
    X = np.array(xs); M = len(X); dx = np.diff(X)
    rows = []
    for i in range(1, M - 1):
        r = np.zeros(M); dl, dr = dx[i - 1], dx[i]
        r[i - 1] = 2.0 / (dl * (dl + dr)); r[i] = -2.0 / (dl * dr); r[i + 1] = 2.0 / (dr * (dl + dr))
        rows.append(r * math.sqrt(0.5 * (dl + dr)))
    D = np.array(rows); Q = 2.0 * D.T @ D
    tot = float(sum(weights)); target = [w / tot for w in weights]
    C = []
    for g in range(nb):
        r = np.zeros(M)
        for i in range(M - 1):
            if owner[i] == g:
                r[i] += 0.5 * dx[i]; r[i + 1] += 0.5 * dx[i]
        C.append(r)
    b = list(target)
    wid = [edges[g + 1] - edges[g] for g in range(nb)]
    mean = [target[g] / wid[g] for g in range(nb)]
    pk = max(range(nb), key=lambda g: mean[g])
    cen = [0.5 * (edges[g] + edges[g + 1]) for g in range(nb)]
    # staircase slope at x: between the neighbouring bin means
    def stair_slope(x):
        g = min(nb - 2, max(0, int(np.searchsorted(cen, x) - 1)))
        return (mean[g + 1] - mean[g]) / (cen[g + 1] - cen[g])
    peak_x = cen[pk]
    lo_peak = edges[pk] ; hi_peak = edges[pk + 1]
    ramp = {}
    for i in range(M - 1):
        xm = 0.5 * (X[i] + X[i + 1])
        if lo_peak - 0.5 * wid[pk] < xm < hi_peak + 0.5 * wid[pk]:
            continue                    # the crown is free
        s = stair_slope(xm)
        if xm < peak_x:
            ramp[i] = (+1, beta * max(s, 0.0))
        else:
            ramp[i] = (-1, beta * max(-s, 0.0))
    act = set()
    h = None
    for _ in range(400):
        Cf = list(C); bf = list(b)
        for i in sorted(act):
            sg, e = ramp[i]
            r = np.zeros(M); r[i], r[i + 1] = -1.0, 1.0
            Cf.append(r); bf.append(sg * e * dx[i])
        Ca = np.array(Cf)
        K = np.block([[Q, Ca.T], [Ca, np.zeros((len(Cf), len(Cf)))]])
        rhs = np.concatenate([np.zeros(M), np.array(bf)])
        try:
            sol = np.linalg.solve(K, rhs)
        except np.linalg.LinAlgError:
            sol = np.linalg.lstsq(K, rhs, rcond=None)[0]
        h = sol[:M]
        bad = [i for i, (sg, e) in ramp.items() if i not in act and
               sg * (h[i + 1] - h[i]) < e * dx[i] - 1e-13]
        if not bad:
            break
        # add the worst few
        bad.sort(key=lambda i: ramp[i][0] * (h[i + 1] - h[i]) - ramp[i][1] * dx[i])
        act.update(bad)
    areas = [0.0] * nb
    for i in range(M - 1):
        areas[owner[i]] += 0.5 * (h[i] + h[i + 1]) * dx[i]
    return list(X), list(h), areas


def _histopolate_ramp(edges, weights, step: float = 1.0 / 16.0):
    """One smooth hill whose area over every bin is EXACT: the least-curvature
    curve with a RAMP condition (rising to the peak bin, falling after it, each
    step at least beta x the local slope of the bin-mean staircase) — the ramp
    is what stops the exact-area curve ringing into false humps, and it can
    never pin a plateau. beta is lowered only if the ramp makes the area
    system infeasible for these weights. Returns (xs, hs, areas, beta)."""
    import numpy as np
    tot = float(sum(weights))
    for beta in (0.20, 0.12, 0.06, 0.0):
        xs, hs, ar = _histopolate_ramp_once(edges, weights, step, beta)
        err = max(abs(a - w / tot) for a, w in zip(ar, weights))
        if err < 1e-12 and min(hs) > -1e-9:
            return xs, [max(0.0, v) for v in hs], ar, beta
    return xs, [max(0.0, v) for v in hs], ar, beta


def _merged_gaps(poly: Poly, marks, r: float, min_piece: float):
    """Over/under gaps on one strand as arclength intervals. ``marks`` are
    (x, y, gap?) for EVERY crossing on the strand; a gap is cut where gap? is
    true. Consecutive gaps whose piece between would be shorter than
    ``min_piece`` merge into one gap (the strand runs under the whole run) —
    only when no crossing where this strand is ON TOP lies between them.
    Returns (intervals, n_merged)."""
    import numpy as np
    if not marks:
        return [], 0
    P = np.asarray(poly)
    s_ = _arclen(poly)
    mk = []
    for px, py, gp in marks:
        k_ = int(np.argmin(np.hypot(P[:, 0] - px, P[:, 1] - py)))
        best = s_[k_]
        for kk in (k_ - 1, k_):
            if 0 <= kk < len(poly) - 1:
                ax_, ay_ = poly[kk]
                bx_, by_ = poly[kk + 1]
                L_ = math.hypot(bx_ - ax_, by_ - ay_) or 1e-9
                u_ = ((px - ax_) * (bx_ - ax_) + (py - ay_) * (by_ - ay_)) / L_ ** 2
                if -1e-6 <= u_ <= 1 + 1e-6:
                    best = s_[kk] + u_ * L_
        mk.append((best, gp))
    mk.sort()
    tops = [s for s, gp in mk if not gp]
    ivs: List[List[float]] = []
    n_m = 0
    for s, gp in mk:
        if not gp:
            continue
        a_, b_ = s - r, s + r
        if ivs and a_ - ivs[-1][1] < min_piece and not any(ivs[-1][1] < u < a_ for u in tops):
            ivs[-1][1] = b_
            n_m += 1
        else:
            ivs.append([a_, b_])
    return [tuple(iv) for iv in ivs], n_m


def _split_by_gaps(poly: Poly, gaps) -> List[Poly]:
    """The pieces of ``poly`` outside the arclength intervals ``gaps``."""
    from bisect import bisect_right
    if not gaps:
        return [list(poly)]
    s_ = _arclen(poly)

    def pt_at(x: float):
        k = max(0, min(len(s_) - 2, bisect_right(s_, x) - 1))
        L_ = s_[k + 1] - s_[k] or 1e-9
        u_ = (x - s_[k]) / L_
        return (poly[k][0] + (poly[k + 1][0] - poly[k][0]) * u_,
                poly[k][1] + (poly[k + 1][1] - poly[k][1]) * u_)

    marks = sorted({0.0, s_[-1]} | {v for iv in gaps for v in iv if 0 < v < s_[-1]})
    runs: List[Poly] = []
    for a_, b_ in zip(marks, marks[1:]):
        m_ = 0.5 * (a_ + b_)
        if any(g0 < m_ < g1 for g0, g1 in gaps):
            continue
        runs.append([pt_at(a_)] + [poly[k] for k in range(len(poly)) if a_ < s_[k] < b_]
                    + [pt_at(b_)])
    return runs


def _near_dist(pts: Poly, poly: Poly):
    """Distance from every point of ``pts`` to the polyline ``poly`` (numpy)."""
    import numpy as np

    P = np.asarray(pts, dtype=float)
    A = np.asarray(poly[:-1], dtype=float)
    B = np.asarray(poly[1:], dtype=float)
    AB = B - A
    L2 = (AB ** 2).sum(1)
    L2[L2 < 1e-12] = 1e-12
    out = np.full(len(P), 1e9)
    for k0 in range(0, len(P), 256):
        Pk = P[k0:k0 + 256]
        AP = Pk[:, None, :] - A[None, :, :]
        t = np.clip((AP * AB[None]).sum(2) / L2[None], 0.0, 1.0)
        pr = A[None] + t[..., None] * AB[None]
        d = np.sqrt(((Pk[:, None, :] - pr) ** 2).sum(2))
        out[k0:k0 + 256] = d.min(1)
    return out


def _arclen(poly: Poly) -> List[float]:
    s = [0.0]
    for a, b in zip(poly, poly[1:]):
        s.append(s[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return s


def _bezier2(a, b, c_, n: int = 24) -> Poly:
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * b[0] + t * t * c_[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * b[1] + t * t * c_[1])
            for t in (k / n for k in range(n + 1))]


def _hermite(p0, t0, p1, t1, n: int = 60) -> Poly:
    out: Poly = []
    for k in range(n + 1):
        t = k / n
        h00 = 2 * t ** 3 - 3 * t ** 2 + 1
        h10 = t ** 3 - 2 * t ** 2 + t
        h01 = -2 * t ** 3 + 3 * t ** 2
        h11 = t ** 3 - t ** 2
        out.append((h00 * p0[0] + h10 * t0[0] + h01 * p1[0] + h11 * t1[0],
                    h00 * p0[1] + h10 * t0[1] + h01 * p1[1] + h11 * t1[1]))
    return out


def _apportion(weights: Sequence[float], n: int) -> List[int]:
    """Largest-remainder (Hamilton) apportionment of n seats by weight."""
    tot = float(sum(weights))
    share = [w * n / tot for w in weights]
    base = [int(s) for s in share]
    rem = n - sum(base)
    for _, g in sorted(((share[g] - base[g], g) for g in range(len(weights))),
                       reverse=True)[:rem]:
        base[g] += 1
    return base


# ---- r07 decisions (every one is stated in NOTES.md) -----------------------
K_START_LO, K_START_SPAN = 0.050, 0.223   # K sweep starts (r06), fraction of pi
D_HOOK_DEG, D_HOOK_R = -28.0, 6.0         # upper selvage: hook off the right jamb
D_END_DEG, D_ARC_R = -5.0, 190.0          # ... then one arc, then straight
D_JOIN = 32.0                             # mm along the arc where the cloth begins
D_CLOTH = 77.0                            # selvage-to-selvage in the cloth (21 x 3.667)
D_ALPHA, D_BETA = 0.05, 0.45              # lower selvage's cubic off the left jamb
MOUTH_MIN = 3.0
PICK_PITCH = 3.64                         # weave floor: lanes >= 3.6 apart on a pick
PICK_LAST_X = 223.5                       # pick 16 meets the upper selvage here
V_LEAD_Y, V_LEAD_XA, V_LEAD_K1, V_LEAD_K2 = 86.0, 96.0, 14.0, 4.0
V_OUT_DROP, V_OUT_K1, V_OUT_K2 = 9.0, 6.0, 7.0
BOLD_PITCH = 0.25                         # the principal thread: 2 passes, registered
TYPE_WEIGHT = 2.0


# ---------------------------------------------------------------------------
# r07 additions
# ---------------------------------------------------------------------------
def _histopolate_pinned(nb: int, weights, step: float, beta: float):
    """Least-curvature h >= 0 on unit bins [0, nb] whose trapezoid area over
    every bin is EXACTLY weights[g] / sum, PINNED TO ZERO at both ends (no
    shelf, no jamb step: the profile leaves the wall at its cut edges), with a
    ramp condition (rising to the crown, falling after it, each step at least
    beta x the slope of the bin-mean staircase). Active set on the ramp rows."""
    import numpy as np
    xs, owner = [], []
    for g in range(nb):
        n = max(3, int(round(1.0 / step)))
        for k in range(n):
            xs.append(g + k / n)
            owner.append(g)
    xs.append(float(nb))
    owner.append(nb - 1)
    X = np.array(xs)
    M = len(X)
    dx = np.diff(X)
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
    tot = float(sum(weights))
    target = [w / tot for w in weights]
    C, b = [], []
    for g in range(nb):
        r = np.zeros(M)
        for i in range(M - 1):
            if owner[i] == g:
                r[i] += 0.5 * dx[i]
                r[i + 1] += 0.5 * dx[i]
        C.append(r)
        b.append(target[g])
    for i in (0, M - 1):                       # the two cut edges: height 0
        r = np.zeros(M)
        r[i] = 1.0
        C.append(r)
        b.append(0.0)
    mean = target
    pk = max(range(nb), key=lambda g: mean[g])
    cen = [g + 0.5 for g in range(nb)]

    def stair_slope(x):
        g = min(nb - 2, max(0, int(np.searchsorted(cen, x) - 1)))
        return (mean[g + 1] - mean[g]) / (cen[g + 1] - cen[g])

    ramp = {}
    for i in range(M - 1):
        xm = 0.5 * (X[i] + X[i + 1])
        if pk - 0.5 < xm < pk + 1.5:
            continue                           # the crown is free
        s = stair_slope(xm)
        if xm < pk + 0.5:
            ramp[i] = (+1, beta * max(s, 0.0))
        else:
            ramp[i] = (-1, beta * max(-s, 0.0))
    act: set = set()
    h = None
    for _ in range(400):
        Cf, bf = list(C), list(b)
        for i in sorted(act):
            sg, e = ramp[i]
            r = np.zeros(M)
            r[i], r[i + 1] = -1.0, 1.0
            Cf.append(r)
            bf.append(sg * e * dx[i])
        Ca = np.array(Cf)
        K = np.block([[Q, Ca.T], [Ca, np.zeros((len(Cf), len(Cf)))]])
        rhs = np.concatenate([np.zeros(M), np.array(bf)])
        sol = np.linalg.lstsq(K, rhs, rcond=None)[0]
        h = sol[:M]
        bad = [i for i, (sg, e) in ramp.items() if i not in act and
               sg * (h[i + 1] - h[i]) < e * dx[i] - 1e-13]
        if not bad:
            break
        act.update(bad)
    areas = [0.0] * nb
    for i in range(M - 1):
        areas[owner[i]] += 0.5 * (h[i] + h[i + 1]) * dx[i]
    return list(X), list(h), areas


def _hill_exact(weights):
    tot = float(sum(weights))
    for beta in (0.25, 0.15, 0.12, 0.08, 0.0):
        xs, hs, ar = _histopolate_pinned(len(weights), weights, 1.0 / 16.0, beta)
        err = max(abs(a - w / tot) for a, w in zip(ar, weights))
        if err < 1e-9 and min(hs) > -1e-9:
            return xs, [max(0.0, v) for v in hs], ar, beta
    return xs, [max(0.0, v) for v in hs], ar, beta


def _cubic(p0, p1, p2, p3, n: int = 60) -> Poly:
    out: Poly = []
    for k in range(n + 1):
        t = k / n
        a, b_, c_, d_ = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b_ * p1[0] + c_ * p2[0] + d_ * p3[0],
                    a * p0[1] + b_ * p1[1] + c_ * p2[1] + d_ * p3[1]))
    return out


def _ray_hit(p, d, poly) -> Optional[float]:
    """First t > 0 at which the ray p + t d meets the polyline ``poly``."""
    import numpy as np
    A = poly[:-1]
    B = poly[1:]
    r = B - A
    den = d[0] * r[:, 1] - d[1] * r[:, 0]
    with np.errstate(divide="ignore", invalid="ignore"):
        t = ((A[:, 0] - p[0]) * r[:, 1] - (A[:, 1] - p[1]) * r[:, 0]) / den
        u = ((A[:, 0] - p[0]) * d[1] - (A[:, 1] - p[1]) * d[0]) / den
    ok = (np.abs(den) > 1e-12) & (t > -1e-9) & (u >= -1e-9) & (u <= 1 + 1e-9)
    if not ok.any():
        return None
    return float(np.min(np.where(ok, t, 1e18)))


def _heading_curve(start, segs, ds: float, x_stop: float):
    """Integrate a curve by its heading. ``segs`` = [(target_deg, radius), ...];
    each turn runs a sin^2 curvature bump (curvature 0 at both ends, so the
    joins are curvature-continuous); after the last segment, straight until
    x > x_stop. Returns (points, headings, index where each seg ends)."""
    x, y = start
    b = -math.pi / 2.0
    pts = [(x, y)]
    hs = [b]
    ends = []
    for tgt, rad in segs:
        tb = math.radians(tgt)
        L = abs(tb - b) * rad
        n = max(1, int(round(L / ds)))
        wts = [math.sin(math.pi * (k + 0.5) / n) ** 2 for k in range(n)]
        sw = sum(wts)
        db = tb - b
        for k in range(n):
            b += wts[k] / sw * db
            x += math.cos(b) * ds
            y += math.sin(b) * ds
            pts.append((x, y))
            hs.append(b)
        ends.append(len(pts) - 1)
    while x < x_stop:
        x += math.cos(b) * ds
        y += math.sin(b) * ds
        pts.append((x, y))
        hs.append(b)
    return pts, hs, ends


def _solid_text(text: str, x: float, y: float, height: float, weight: float,
                pen, tip: float = 0.5, pitch: float = 0.30, spaced: bool = True,
                f: int = 2200) -> List[GCodeCommand]:
    """Display type with ONE construction for every stroke: each glyph segment
    is a band ``weight`` wide filled by a serpentine at ``pitch`` (so a
    diagonal is exactly as heavy as a stem), and every interior vertex that
    turns more than 12 deg gets a filled round join. Flat terminals."""
    from promptplot.generative.engine.kit import _GLYPHS
    sc = height / 6.0
    adv = 5.6 * sc
    half = max(0.0, (weight - tip) / 2.0)
    npass = max(2, int(math.ceil(2 * half / pitch)) + 1)
    out: List[GCodeCommand] = []
    cx = x
    s_ = _spaced(text) if spaced else text
    for ch in s_:
        strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        for stroke in strokes:
            pts = [(cx + gx * sc, y + gy * sc) for gx, gy in stroke]
            for a, b in zip(pts, pts[1:]):
                dx, dy = b[0] - a[0], b[1] - a[1]
                L = math.hypot(dx, dy)
                if L < 1e-9:
                    continue
                nx, ny = -dy / L, dx / L
                serp: Poly = []
                for i in range(npass):
                    d = -half + 2 * half * i / (npass - 1)
                    p0 = (a[0] + nx * d, a[1] + ny * d)
                    p1 = (b[0] + nx * d, b[1] + ny * d)
                    serp += [p0, p1] if i % 2 == 0 else [p1, p0]
                out += _poly(serp, color=pen, f=f)
            closed = len(pts) > 2 and math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1e-6
            joins = list(range(1, len(pts) - 1)) + ([0] if closed else [])
            for k in joins:
                p_prev = pts[k - 1] if k > 0 else pts[-2]
                p, p_next = pts[k], pts[k + 1]
                a1 = math.atan2(p[1] - p_prev[1], p[0] - p_prev[0])
                a2 = math.atan2(p_next[1] - p[1], p_next[0] - p[0])
                turn = abs((a2 - a1 + math.pi) % (2 * math.pi) - math.pi)
                if turn > math.radians(12) and half > 0.05:
                    out += fill_disc(p[0], p[1], half, spacing=pitch, pen=pen, f=f)
        cx += adv
    return out


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def attention_weaving_reed(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_q: int = 22,
    n_k: int = 16,
    feed: int = 2200,
) -> List[GCodeCommand]:
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    k_v = _pen(V_PEN, colors)
    k_k = _pen(K_PEN, colors)
    k_q = _pen(Q_PEN, colors)
    k_z = _pen(Z_PEN, colors)
    k_black = _pen(BLACK, colors)
    k_txt = _pen(TEXT, colors)
    out: List[GCodeCommand] = []
    LAST_STATS.clear()
    box = G.Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)
    GAP = 1.15                  # storm over/under gap radius (r06)

    # ======================================================================
    # THE NUMBERS — the same seeded draws as r03-r06 (encoding.md §4a)
    # ======================================================================
    d = 16

    def _unit(n: int = d):
        v = [rng.gauss() for _ in range(n)]
        s = math.sqrt(sum(t * t for t in v)) or 1.0
        return [t / s for t in v]

    Qv = [_unit() for _ in range(n_q)]
    Kv = [_unit() for _ in range(n_k)]
    Vv_raw = [_unit(38) for _ in range(n_k)]
    Vv = [[t for t in v[:d]] for v in Vv_raw]
    principal = n_q // 2
    for j, w_ in ((5, 0.90), (11, 0.70), (2, 0.54), (14, 0.40), (8, 0.30)):
        Kv[j] = [w_ * Qv[principal][t] + math.sqrt(1 - w_ * w_) * Kv[j][t] for t in range(d)]
        n_ = math.sqrt(sum(t * t for t in Kv[j])) or 1.0
        Kv[j] = [t / n_ for t in Kv[j]]
    S = [[sum(Qv[i][t] * Kv[j][t] for t in range(d)) * math.sqrt(d)
          for j in range(n_k)] for i in range(n_q)]
    lo_t, hi_t = 0.05, 30.0
    for _ in range(64):
        mid = 0.5 * (lo_t + hi_t)
        if max(_softmax(S[principal], mid)) > 0.190:
            lo_t = mid
        else:
            hi_t = mid
    TEMP = 0.5 * (lo_t + hi_t)
    A = _softmax(S[principal], TEMP)
    A_all = [_softmax(S[i], TEMP) for i in range(n_q)]
    a_max = max(A)
    Hbits = _entropy_bits(A)
    row_sum_err = max(abs(sum(r) - 1.0) for r in A_all)
    UNIF = 1.0 / n_k

    # bins: keys sorted by Q11's a, dealt alternately about the crown (§4a)
    DEAL = [7, 8, 6, 9, 5, 10, 4, 11, 3, 12, 2, 13, 1, 14, 0, 15]
    srt = sorted(range(n_k), key=lambda j: -A[j])
    korder: List[int] = [0] * n_k
    for r_, j in enumerate(srt):
        korder[DEAL[r_]] = j
    bin_of = {j: g for g, j in enumerate(korder)}
    Ag = [A[j] for j in korder]
    above_bins = [g for g in range(n_k) if Ag[g] > UNIF]

    # ======================================================================
    # THE SLIT (R3): 52 mm, 16 equal bins; 22 lanes at ONE pitch (R2)
    # ======================================================================
    SLIT = 52.0
    c = SLIT / 2.0
    w_bin = SLIT / n_k
    ax = x0 + 0.425 * W
    ay = y0 + 0.620 * H
    ap = Aperture(ax=ax, ay=ay, c=c)
    edges = [ax - c + g * w_bin for g in range(n_k + 1)]
    PITCH = 2.25
    p_lane = n_q // 2
    lanes_x = [ax + (k - p_lane) * PITCH for k in range(n_q)]
    ZMAX = 0.074 * H

    # ---- the hill: exact area, zero at both cut edges ---------------------
    _ux, _uh, _uarea, hill_beta = _hill_exact(Ag)
    hx = [ax - c + w_bin * u for u in _ux]
    hy = [v / w_bin for v in _uh]
    hscale = ZMAX / max(hy)
    curve = [(px, ay + py * hscale) for px, py in zip(hx, hy)]
    h_area = list(_uarea)
    HILL_HALF = 0.60            # 5 passes centred on the curve: -0.6 .. +0.6
    HILL_GAP = 1.25             # strands stop 1 mm of paper + half a pen above
    K_CLEAR = HILL_HALF + 0.75
    top_ = G.offset(curve, HILL_HALF + HILL_GAP)
    band_poly = top_ + [(top_[-1][0], ay - 0.05), (top_[0][0], ay - 0.05)]
    hill_band = G.Polygon(band_poly)
    bin_mean = [Ag[g] / w_bin * hscale for g in range(n_k)]
    srt_mean = sorted(bin_mean)
    peak_med = max(bin_mean) / (0.5 * (srt_mean[7] + srt_mean[8]))
    tick_h = UNIF / w_bin * hscale                  # the 1/16 level, mean-height scale
    summit_x = max(curve, key=lambda p: p[1])[0]

    def _inv(ap_: Aperture, x: float, y: float) -> Tuple[float, float]:
        import cmath
        z = complex((x - ap_.ax) / ap_.c, (y - ap_.ay) / ap_.c)
        wv = cmath.acosh(z)
        phi_, psi_ = wv.real, wv.imag
        if phi_ < 0:
            phi_, psi_ = -phi_, -psi_
        return phi_, psi_ % (2 * math.pi)

    # ---- K landings: K_j rides the streamline whose SLIT crossing sits at
    # maximum clearance from the lane slots (streamlines never cross, so the
    # clearance holds all the way up), and it must land inside its own bin
    cv = np.asarray(curve)

    def _landing(xs_slit: float):
        ps = ap.psi_for_slit_x(xs_slit - ax)
        prev = None
        for kk in range(1, 900):
            ph = kk * 0.002
            p_ = ap.pt(ph, ps)
            ytop = float(np.interp(p_[0], cv[:, 0], cv[:, 1]))
            if p_[1] > ytop and float(_near_dist([p_], curve)[0]) >= K_CLEAR:
                return p_, ph, ps
        return None

    ktg = []
    k_slit = []
    for g in range(n_k):
        cen = 0.5 * (edges[g] + edges[g + 1])
        best = None
        for xs_ in np.linspace(edges[g] - 1.5, edges[g + 1] + 1.5, 181):
            if not (ax - c + 0.3 < xs_ < ax + c - 0.3):
                continue
            cl = min(abs(xs_ - lx) for lx in lanes_x)
            if cl < 0.6:
                continue
            land = _landing(float(xs_))
            if land is None:
                continue
            (lx_, ly_), ph, ps = land
            in_x = edges[g] + 0.45 <= lx_ <= edges[g + 1] - 0.45
            in_flow = edges[g] + 0.3 <= xs_ <= edges[g + 1] - 0.3 and ax - c + 0.5 <= lx_ <= ax + c - 0.5
            if not (in_x or in_flow):
                continue
            key = (1 if in_x else 0, round(min(cl, 0.5 * PITCH), 4), -abs(lx_ - cen))
            if best is None or key > best[0]:
                best = (key, (lx_, ly_, ph, ps), float(xs_))
        if best is None:
            raise RuntimeError(f'no K landing for bin {g} [{edges[g]:.2f},{edges[g+1]:.2f}]')
        ktg.append(best[1])
        k_slit.append(best[2])
    k_lane_clear = min(abs(xs_ - lx) for xs_ in k_slit for lx in lanes_x)
    k_flow_bins = [g for g in range(n_k) if not (edges[g] <= ktg[g][0] <= edges[g + 1])]
    k_off = [round(ktg[g][0] - 0.5 * (edges[g] + edges[g + 1]), 3) for g in range(n_k)]

    # ---- query identity per slot: seriated on B, Q11 pinned at slot 11 ----
    Bm = [[1 if A_all[i][korder[g]] > UNIF else 0 for g in range(n_k)] for i in range(n_q)]

    def _ham(a_: int, b_: int) -> int:
        return sum(1 for g in range(n_k) if Bm[a_][g] != Bm[b_][g])

    pool = set(i for i in range(n_q) if i != principal)
    left: List[int] = []
    right: List[int] = []
    while pool:
        for side, cap in ((right, n_q - 1 - p_lane), (left, p_lane)):
            if not pool or len(side) >= cap:
                continue
            tip = side[-1] if side else principal
            nxt = min(pool, key=lambda i: (_ham(tip, i), i))
            side.append(nxt)
            pool.discard(nxt)
    qid = list(reversed(left)) + [principal] + right

    def _cost(q_):
        return sum(_ham(a_, b_) for a_, b_ in zip(q_, q_[1:]))

    improved = True
    while improved:
        improved = False
        for a_ in range(n_q):
            for b_ in range(a_ + 1, n_q):
                if p_lane in (a_, b_):
                    continue
                q2 = list(qid)
                q2[a_], q2[b_] = q2[b_], q2[a_]
                if _cost(q2) < _cost(qid):
                    qid, improved = q2, True
    assert qid[p_lane] == principal

    # ======================================================================
    # Q — pure streamlines of the aperture, one per slot
    # ======================================================================
    PHI_MAX = 2.85
    psi_q = [ap.psi_for_slit_x(xx - ax) for xx in lanes_x]

    def q_path(t: int) -> Poly:
        ps = psi_q[t]
        return [ap.pt(PHI_MAX * (1.0 - u / 170.0) ** 1.22, ps) for u in range(171)]

    q_polys = [_resample(q_path(t), 1.1) for t in range(n_q)]

    # ======================================================================
    # K — r06's sweep + tangent-continuous turn onto its own streamline,
    # ending on the hill inside its own bin; starts carried to the frame
    # ======================================================================
    c_old = 0.118 * W

    def _phi_keep(phi_old: float) -> float:
        return math.acosh(max(1.0, math.cosh(phi_old) * c_old / c))

    psi_k_end = [ktg[bin_of[j]][3] for j in range(n_k)]
    phi_k_end = [ktg[bin_of[j]][2] for j in range(n_k)]
    order = sorted(range(n_k), key=lambda j: psi_k_end[j])
    rank = {j: r for r, j in enumerate(order)}
    psi_k_start = [K_START_LO * math.pi + K_START_SPAN * math.pi * (rank[j] / max(1, n_k - 1))
                   for j in range(n_k)]
    phi_k = [_phi_keep(1.52 + 1.52 * (rank[j] / max(1, n_k - 1))) for j in range(n_k)]
    K_FIL_A = 0.08
    K_FIL_B = 0.55
    psi_q_min = min(psi_q)

    def _pp(pts):
        return [ap.pt(f, s) for f, s in pts]

    def _k_floor(a0: float) -> float:
        below = [q for q in psi_q if q < a0 - 0.015]
        if below:
            return max(below) + 0.45 * (a0 - max(below))
        return min(0.80 * a0, psi_q_min - 0.05)

    k_lin_ok = {j: True for j in range(n_k)}
    k_lin_exit = {j: psi_k_start[j] for j in range(n_k)}

    def k_param(j: int, force_exp: bool = False, psi_f_set: Optional[float] = None):
        a0, a1 = psi_k_start[j], psi_k_end[j]
        P0 = (phi_k[j], a0)
        Pc = (0.56 * phi_k[j], a1)
        phi_end = phi_k_end[j]
        L1 = math.hypot(P0[0] - Pc[0], P0[1] - Pc[1])
        A_ = (Pc[0] + (P0[0] - Pc[0]) * K_FIL_A, Pc[1] + (P0[1] - Pc[1]) * K_FIL_A)
        lb = min(K_FIL_B * K_FIL_A * L1, 0.45 * (Pc[0] - phi_end))
        B_ = (Pc[0] - lb, a1)
        sweep = [(P0[0] + (A_[0] - P0[0]) * u / 120.0, P0[1] + (A_[1] - P0[1]) * u / 120.0)
                 for u in range(121)]
        fil = _bezier2(A_, Pc, B_, 40)
        tail = [(B_[0] + (phi_end - B_[0]) * u / 160.0, a1) for u in range(161)]
        body = sweep + fil[1:] + tail[1:]
        ext: List[Tuple[float, float]] = []
        sx, sy = ap.pt(*P0)
        if x0 + 1 < sx < x1 - 1 and sy < y1 - 1:
            dphi, dpsi = P0[0] - Pc[0], P0[1] - Pc[1]
            lin: List[Tuple[float, float]] = []
            ok = False
            for u in range(1, 4000):
                tau = u * 0.002
                ph, ps = P0[0] + dphi * tau, P0[1] + dpsi * tau
                if ps < 0.5 * a0:
                    break
                lin.append((ph, ps))
                ex_, ey_ = ap.pt(ph, ps)
                if ex_ > x1 + 3 or ey_ > y1 + 3:
                    ok = ey_ > ay + 6.0
                    break
            k_lin_ok[j] = ok
            k_lin_exit[j] = lin[-1][1] if lin else a0
            if ok and not force_exp:
                ext = list(reversed(lin))
            else:
                psi_f = psi_f_set if psi_f_set is not None else _k_floor(a0)
                kk = -dpsi / (dphi * max(1e-6, a0 - psi_f))
                tau = 0.0
                while True:
                    tau += 0.004
                    ph = P0[0] + tau
                    ps = psi_f + (a0 - psi_f) * math.exp(-kk * tau)
                    ext.append((ph, ps))
                    ex_, ey_ = ap.pt(ph, ps)
                    if ex_ > x1 + 3 or ey_ > y1 + 3 or tau > 4:
                        break
                ext = list(reversed(ext))
        return ext, body, len(ext) + len(sweep) + len(fil) - 1

    def _build_k():
        for j in range(n_k):
            k_param(j)
        by_rank = sorted(range(n_k), key=lambda j: rank[j])
        r_fail = max([rank[j] for j in range(n_k) if not k_lin_ok[j]], default=-1)
        k_floor: dict = {}
        ceiling = None
        for j in reversed(by_rank):
            if rank[j] > r_fail:
                ceiling = k_lin_exit[j] if ceiling is None else min(ceiling, k_lin_exit[j])
                continue
            f_ = _k_floor(psi_k_start[j])
            if ceiling is not None:
                f_ = min(f_, ceiling - 0.03)
            k_floor[j] = f_
            ceiling = f_
        kp, kd, ke = [], [], []
        for j in range(n_k):
            ext, body, i_drop = k_param(j, force_exp=rank[j] <= r_fail, psi_f_set=k_floor.get(j))
            pts = _pp(ext + body)
            kp.append(_resample(pts, 1.1))
            kd.append(pts[i_drop:])
            ke.append(pts[-1])
        return kp, kd, ke

    def _mouths(polys, who):
        res = []
        for n_, pl in enumerate(polys):
            for r in G.clip(pl, box, keep="inside"):
                for e in (r[0], r[-1]):
                    if e[1] > y1 - 1.2:
                        res.append(("top", e[0], who, n_))
                    elif e[0] > x1 - 1.2:
                        res.append(("right", e[1], who, n_))
        return res

    def _mouths_side(polys, side):
        res = []
        for pl in polys:
            for r in G.clip(pl, box, keep="inside"):
                for e in (r[0], r[-1]):
                    if side == "left" and e[0] < x0 + 1.2:
                        res.append(("left", e[1]))
                    elif side == "right" and e[0] > x1 - 1.2 and e[1] > ay:
                        res.append(("right", e[1]))
        return res

    def _mouth_gaps(ms):
        out_ = []
        for side in ("top", "right"):
            lst = sorted([m for m in ms if m[0] == side], key=lambda m: m[1])
            out_ += [(b_[1] - a_[1], a_, b_) for a_, b_ in zip(lst, lst[1:])]
        return sorted(out_, key=lambda t_: t_[0])

    # A22: reed mouths >= MOUTH_MIN apart. A K start that lands on a Q mouth
    # (or on another K) is nudged along its sweep until the reed is clear.
    q_mouths = _mouths(q_polys, "Q")
    k_polys, k_drops, k_end_pt = _build_k()
    n_nudge = 0
    for _ in range(60):
        gaps_ = _mouth_gaps(q_mouths + _mouths(k_polys, "K"))
        worst = next((g_ for g_ in gaps_ if g_[0] < MOUTH_MIN and "K" in (g_[1][2], g_[2][2])), None)
        if worst is None:
            break
        j = worst[1][3] if worst[1][2] == "K" else worst[2][3]
        base = psi_k_start[j]
        best = None
        for dlt in (0.012, -0.012, 0.024, -0.024, 0.04, -0.04):
            psi_k_start[j] = base + dlt
            kp_ = _build_k()
            gg = _mouth_gaps(q_mouths + _mouths(kp_[0], "K"))
            score = min(g_[0] for g_ in gg if "K" in (g_[1][2], g_[2][2]))
            nb = sum(1 for g_ in gg if g_[0] < MOUTH_MIN)
            if best is None or (nb, -score) < best[0]:
                best = ((nb, -score), dlt, kp_)
        psi_k_start[j] = base + best[1]
        k_polys, k_drops, k_end_pt = best[2]
        n_nudge += 1

    # ---- Q.K^T: every crossing, over/under by sign(s_ij) ------------------
    n_cross = 0
    qk_ang: List[float] = []
    k_marks: List[list] = [[] for _ in range(n_k)]
    q_marks: List[list] = [[] for _ in range(n_q)]
    for j in range(n_k):
        for t in range(n_q):
            for px, py, ang in _crossings_ang(k_polys[j], q_polys[t]):
                if not (x0 + 1 < px < x1 - 1 and ay + 1.0 < py < y1 - 1):
                    continue
                n_cross += 1
                qk_ang.append(ang)
                k_under = S[qid[t]][j] >= 0.0
                k_marks[j].append((px, py, k_under))
                q_marks[t].append((px, py, not k_under))
    kk_where = [(a_, b_, round(h_[0], 1), round(h_[1], 1)) for a_ in range(n_k) for b_ in range(a_ + 1, n_k)
                for h_ in _crossings_ang(k_polys[a_], k_polys[b_]) if x0 < h_[0] < x1 and y0 < h_[1] < y1]
    kk_x = len(kk_where)
    qk_low = sorted((round(a_, 1), round(px_, 1), round(py_, 1)) for j in range(n_k) for t in range(n_q)
                    for px_, py_, a_ in _crossings_ang(k_polys[j], q_polys[t]) if py_ > ay + 1)[:4]

    # ======================================================================
    # BELOW THE WALL — the warp (R1): 22 lanes ruled by the upper selvage's
    # normals, and ONE gold weft of 16 picks along those normals
    # ======================================================================
    DS = 0.2
    c21, h21, ends21 = _heading_curve((lanes_x[-1], ay), [(D_HOOK_DEG, D_HOOK_R), (D_END_DEG, D_ARC_R)],
                                      DS, x1 + 30.0)
    C21 = np.asarray(c21)
    B21 = np.asarray(h21)
    N21 = np.stack([np.cos(B21 - math.pi / 2), np.sin(B21 - math.pi / 2)], 1)   # outer normal
    i_hook = ends21[0]
    iJ = i_hook + int(round(D_JOIN / DS))
    # lower selvage: from the left lane's slit point, straight down, then one
    # cubic onto the concentric offset of the upper selvage (distance D_CLOTH)
    S0 = (lanes_x[0], ay)
    J0 = C21[iJ] + D_CLOTH * N21[iJ]
    tJ = (math.cos(B21[iJ]), math.sin(B21[iJ]))
    lam = (J0[0] - S0[0]) / tJ[0]
    Cc = (J0[0] - lam * tJ[0], J0[1] - lam * tJ[1])
    P1 = (S0[0] + D_ALPHA * (Cc[0] - S0[0]), S0[1] + D_ALPHA * (Cc[1] - S0[1]))
    P2 = (J0[0] + D_BETA * (Cc[0] - J0[0]), J0[1] + D_BETA * (Cc[1] - J0[1]))
    C0 = np.vstack([np.asarray(_cubic(S0, P1, P2, tuple(J0), 400)),
                    C21[iJ + 1:] + D_CLOTH * N21[iJ + 1:]])
    conn = np.full(len(C21), np.nan)
    for i in range(len(C21)):
        tt = _ray_hit(C21[i] - 1e-3 * N21[i], N21[i], C0)
        if tt is not None:
            conn[i] = tt - 1e-3
    conn[0] = lanes_x[-1] - lanes_x[0]
    good = ~np.isnan(conn)
    idx = np.nonzero(good)[0]
    fk = [(n_q - 1 - k) / (n_q - 1) for k in range(n_q)]     # lane k = C21 + fk t N
    lane_polys: List[Poly] = []
    for k in range(n_q):
        P_ = C21[idx] + (fk[k] * conn[idx])[:, None] * N21[idx]
        pl = [tuple(p) for p in P_ if p[0] <= x1 + 2 and p[1] >= y0 - 2]
        pl = [(pl[0][0], ay - 0.8)] + [p for p in pl if p[1] <= ay - 0.8]
        lane_polys.append(_resample(pl, 0.8))
    slit_err = max(abs(lane_polys[t][0][0] - lanes_x[t]) for t in range(n_q))

    # ---- the picks: 16 normals of the upper selvage, equal arclength ------
    sig = np.arange(len(C21)) * DS
    i1 = next(i for i in range(iJ, len(C21)) if good[i] and conn[i] / (n_q - 1) >= PICK_PITCH)
    i16 = next(i for i in range(i1, len(C21)) if C21[i][0] >= PICK_LAST_X)
    pick_i = [int(round(i1 + (i16 - i1) * g / 15.0)) for g in range(16)]
    pick_sp21 = (sig[i16] - sig[i1]) / 15.0
    E_EXT = 2.6
    pick_seg = []            # (start, end) in weft order
    cross_at = []            # per pick: list of (lane k, point) in weft order
    for g, i in enumerate(pick_i):
        n_ = N21[i]
        tt = conn[i]
        e_out = C21[i] + (tt + E_EXT) * n_
        e_in = C21[i] - E_EXT * n_
        pts_k = [(k, C21[i] + fk[k] * tt * n_) for k in range(n_q)]
        if g % 2 == 0:                 # outer -> inner (lane 0 first)
            pick_seg.append((e_out, e_in))
            cross_at.append(pts_k)
        else:
            pick_seg.append((e_in, e_out))
            cross_at.append(list(reversed(pts_k)))
    # the weft as one path: lead-in, picks, turns, lead-out
    weft: Poly = []
    ranges = []

    def _app(seg: Poly):
        if weft and math.hypot(weft[-1][0] - seg[0][0], weft[-1][1] - seg[0][1]) < 1e-6:
            weft.extend(seg[1:])
        else:
            weft.extend(seg)

    yL = V_LEAD_Y
    e0, e1_ = pick_seg[0]
    dir0 = ((e1_[0] - e0[0]), (e1_[1] - e0[1]))
    l0 = math.hypot(*dir0)
    dir0 = (dir0[0] / l0, dir0[1] / l0)
    XA = V_LEAD_XA
    lead_in = [(x0, yL), (XA, yL)] + _cubic((XA, yL), (XA + V_LEAD_K1, yL),
                                           (e0[0] - V_LEAD_K2 * dir0[0], e0[1] - V_LEAD_K2 * dir0[1]),
                                           (float(e0[0]), float(e0[1])), 80)[1:]
    lead_in = _resample(lead_in, 0.5)
    _app(lead_in)
    n_lead_in = len(weft)
    for g in range(16):
        a_, b_ = pick_seg[g]
        s_start = len(weft)
        _app([(float(a_[0]), float(a_[1])), (float(b_[0]), float(b_[1]))])
        ranges.append(("pick", g))
        if g < 15:
            na, nb_ = pick_seg[g + 1]
            dg = (b_[0] - a_[0], b_[1] - a_[1])
            lg = math.hypot(*dg)
            dg = (dg[0] / lg, dg[1] / lg)
            dn = (nb_[0] - na[0], nb_[1] - na[1])
            ln = math.hypot(*dn)
            dn = (dn[0] / ln, dn[1] / ln)
            span = math.hypot(na[0] - b_[0], na[1] - b_[1])
            kq = 0.66 * span
            turn = _cubic((float(b_[0]), float(b_[1])), (b_[0] + kq * dg[0], b_[1] + kq * dg[1]),
                          (na[0] - kq * dn[0], na[1] - kq * dn[1]), (float(na[0]), float(na[1])), 40)
            _app(turn)
    e15a, e15b = pick_seg[15]
    d15 = (e15b[0] - e15a[0], e15b[1] - e15a[1])
    l15 = math.hypot(*d15)
    d15 = (d15[0] / l15, d15[1] / l15)
    yR = float(lane_polys[0][-1][1]) - V_OUT_DROP
    lead_out = _cubic((float(e15b[0]), float(e15b[1])),
                      (e15b[0] + V_OUT_K1 * d15[0], e15b[1] + V_OUT_K1 * d15[1]),
                      (x1 - V_OUT_K2, yR), (x1, yR), 80)
    _app(_resample(lead_out, 0.5))
    weft = _resample(weft, 0.4)
    s_w = _arclen(weft)
    WP = np.asarray(weft)

    def _s_on_weft(p) -> float:
        k_ = int(np.argmin(np.hypot(WP[:, 0] - p[0], WP[:, 1] - p[1])))
        best_ = s_w[k_]
        for kk in (k_ - 1, k_):
            if 0 <= kk < len(weft) - 1:
                ax_, ay_ = weft[kk]
                bx_, by_ = weft[kk + 1]
                L_ = math.hypot(bx_ - ax_, by_ - ay_) or 1e-9
                u_ = ((p[0] - ax_) * (bx_ - ax_) + (p[1] - ay_) * (by_ - ay_)) / L_ ** 2
                if -1e-6 <= u_ <= 1 + 1e-6:
                    best_ = s_w[kk] + u_ * L_
        return best_

    # ---- over/under: gold over green  <=>  a_ij > 1/16, at every crossing -
    R_GAP = 1.1
    R_BOLD = R_GAP + 0.125
    gold_gaps: List[List[float]] = []
    lane_marks: List[list] = [[] for _ in range(n_q)]
    B_drawn = [[None] * n_k for _ in range(n_q)]       # by query index
    n_over = 0
    cross_ang: List[float] = []
    for g in range(16):
        j = korder[g]
        run: Optional[List[float]] = None
        for k, p in cross_at[g]:
            over = A_all[qid[k]][j] > UNIF
            B_drawn[qid[k]][g] = over
            s_ = _s_on_weft(p)
            if over:
                n_over += 1
                lane_marks[k].append((float(p[0]), float(p[1]), True))
                if run is not None:
                    gold_gaps.append(run)
                    run = None
            else:
                r_ = R_BOLD if k == p_lane else R_GAP
                if run is None:
                    run = [s_ - r_, s_ + r_]
                else:
                    run[1] = s_ + r_
        if run is not None:
            gold_gaps.append(run)
    # crossing angles (measured on the drawn lanes)
    for g in range(16):
        a_, b_ = pick_seg[g]
        seg = [(float(a_[0]), float(a_[1])), (float(b_[0]), float(b_[1]))]
        for k in range(n_q):
            for px, py, ang in _crossings_ang(seg, lane_polys[k]):
                cross_ang.append(ang)
    # the rule, checked against the matrix: 352 decisions, 0 overrides
    rule_ok = sum(1 for i in range(n_q) for g in range(16)
                  if B_drawn[i][g] == (A_all[i][korder[g]] > UNIF))
    # the non-pick parts of the weft must cross nothing
    weft_lane_x = sum(len(_crossings_ang(weft, lane_polys[k])) for k in range(n_q))
    lane_lane_x = sum(len(_crossings_ang(lane_polys[k], lane_polys[k + 1])) for k in range(n_q - 1))
    # the pieces of gold
    gold_pieces = _split_by_gaps(weft, [tuple(g_) for g_ in gold_gaps])
    gold_len = [_arclen(p)[-1] for p in gold_pieces]

    # green: a gap wherever gold is over (never merged)
    lane_gaps = []
    for k in range(n_q):
        r_ = R_GAP
        gk, _nm = _merged_gaps(lane_polys[k], lane_marks[k], r_, 0.0)
        lane_gaps.append(gk)
    green_pieces = [_split_by_gaps(lane_polys[k], lane_gaps[k]) for k in range(n_q)]

    # ---- measured spacings ------------------------------------------------
    lane_pitch = 1e9
    lane_pitch_at = None
    for k in range(n_q - 1):
        pa = [p for p in lane_polys[k] if x0 < p[0] < x1 and y0 < p[1] < ay]
        dd = _near_dist(pa, lane_polys[k + 1])
        m_ = int(np.argmin(dd))
        if dd[m_] < lane_pitch:
            lane_pitch = float(dd[m_])
            lane_pitch_at = (k, round(pa[m_][0], 1), round(pa[m_][1], 1))
    kq_pitch = 1e9
    kq_at = None
    for j in range(n_k):
        tail_pts = _resample(k_drops[j], 0.5)
        for t in range(n_q):
            dd_ = _near_dist(tail_pts, q_polys[t])
            m_ = int(np.argmin(dd_))
            if dd_[m_] < kq_pitch:
                kq_pitch = float(dd_[m_])
                kq_at = (j, t, round(tail_pts[m_][0], 1), round(tail_pts[m_][1], 1))
    pick_pitch = [conn[i] / (n_q - 1) for i in pick_i]
    # pick spacing along every lane (the tightest lane is the upper selvage)
    pick_sp_lane = []
    for k in range(n_q):
        pts_ = [np.asarray(cross_at[g][[kk for kk, _ in cross_at[g]].index(k)][1]) for g in range(16)]
        pick_sp_lane.append(min(float(np.hypot(*(pts_[g + 1] - pts_[g]))) for g in range(15)))
    L0 = np.asarray(lane_polys[0])
    lane0_x_at_150 = float(np.interp(150.0, L0[::-1, 1], L0[::-1, 0]))

    # gold clearance from lanes it does not cross (turns, leads)
    # distance of every weft point that is not within 1.2 mm of a crossing
    xpts = np.asarray([p for g in range(16) for _, p in cross_at[g]])
    far = [p for p in weft if np.min(np.hypot(xpts[:, 0] - p[0], xpts[:, 1] - p[1])) > 3.0]
    gold_lane_clear = min(float(_near_dist(far, lane_polys[k]).min()) for k in range(n_q))

    # ======================================================================
    # LABELS (text layer) — placed, then honoured as halos
    # ======================================================================
    halos: List[G.Region] = []
    labels: List[Tuple[str, float, float, float]] = []

    def label(text: str, x: float, y: float, h: float, pad: float = 1.3, spaced: bool = False):
        s_ = _spaced(text) if spaced else text
        w_ = _text_width(s_, h)
        labels.append((s_, x, y, h))
        halos.append(G.Rect(x - pad, y - pad, x + w_ + pad, y + h + pad))
        return w_

    label("SOFTMAX", ax + c + 10.5, ay + 2.0, 2.6, pad=1.0, spaced=True)
    LAB_H = 4.6
    lm = [m[1] for m in _mouths_side(q_polys + k_polys, "left")]
    rm = [m[1] for m in _mouths_side(q_polys + k_polys, "right")]
    q_lab_y = max(np.arange(ay + 40.0, y1 - 40.0, 0.25),
                  key=lambda yy: min([abs(yy + 0.5 * LAB_H - v) for v in lm + rm] + [99.0]))
    label("Q", x0 + 0.012 * W, q_lab_y, LAB_H, pad=1.2)
    label("K", x1 - 0.012 * W - _text_width("K", LAB_H), q_lab_y, LAB_H, pad=1.2)
    label("V", x0 + 1.5, yL + 3.0, LAB_H, pad=1.0)
    # the bold lane's exit: '11' sits in the gap just above its tick
    ex11 = lane_polys[p_lane][-1]
    ey11 = float(np.interp(x1 - 2.0, [p[0] for p in lane_polys[p_lane]],
                           [p[1] for p in lane_polys[p_lane]]))
    lab11_h = 1.7
    label("11", x1 - 0.6 - _text_width("11", lab11_h), ey11 + 0.95, lab11_h, pad=0.35)
    th = 13.0
    base_sums, base_one = y0 + 53.0, y0 + 34.0
    for word, yy in (("SUMS", base_sums), ("TO ONE", base_one)):
        ww = giant_type_width(word, th, spaced=True)
        halos.append(G.Rect(x0 + 0.5 - 1.5, yy - 2.5, x0 + 1.5 + ww + 2.5, yy + th + 2.5))
    zl = "Z = AV"
    zl_h = 4.6
    label(zl, x0 + 158.0 + 44.0 - _text_width(zl, zl_h), base_one, zl_h, pad=1.2)
    hal = G.Union(*halos)

    def cut_halo(src: Poly) -> List[Poly]:
        runs = G.clip(src, box, keep="inside")
        return [r for run in runs for r in G.clip(run, hal, keep="outside")]

    # ======================================================================
    # EMIT
    # ======================================================================
    EDGE_STUB = 2.0
    STORM_MIN = 3.0
    n_edge_stub = 0
    n_storm_merge = 0
    storm_runs: List[float] = []
    Q_STUB = 3.0
    n_stub = 0
    def _bold(run: Poly) -> Poly:
        """Two registered passes as ONE stroke: out on one side, back on the other."""
        pa = G.offset(run, -0.5 * BOLD_PITCH)
        pb = G.offset(run, +0.5 * BOLD_PITCH)
        return pa + list(reversed(pb))

    def _emit_serp(strands: List[List[Poly]], pen, bold_idx: int = -1):
        """Strands in order, alternate strands reversed (pieces and points), so
        the nearest-neighbour optimiser chains them: travel stays short."""
        for n, runs in enumerate(strands):
            seq = runs if n % 2 == 0 else [list(reversed(r)) for r in reversed(runs)]
            for r in seq:
                out.extend(_poly(_bold(r) if n == bold_idx else r, color=pen, f=feed))

    # crimson: Q, stopping above the hill; the principal query bold
    q_strands: List[List[Poly]] = []
    for t in range(n_q):
        gq, nm = _merged_gaps(q_polys[t], q_marks[t], GAP, STORM_MIN)
        n_storm_merge += nm
        runs_t: List[Poly] = []
        for piece in _split_by_gaps(q_polys[t], gq):
            for run in cut_halo(piece):
                for r2 in G.clip(run, hill_band, keep="outside"):
                    L_ = _arclen(r2)[-1]
                    if r2[-1][1] < ay + ZMAX + 3.0 and L_ < Q_STUB:
                        n_stub += 1
                        continue
                    if L_ < EDGE_STUB:
                        n_edge_stub += 1
                        continue
                    storm_runs.append(L_)
                    runs_t.append(r2)
        q_strands.append(runs_t)
    _emit_serp(q_strands, k_q, bold_idx=p_lane)
    # blue: K, in rank order
    k_strands: List[List[Poly]] = []
    for j in order:
        gk, nm = _merged_gaps(k_polys[j], k_marks[j], GAP, STORM_MIN)
        n_storm_merge += nm
        runs_j: List[Poly] = []
        for piece in _split_by_gaps(k_polys[j], gk):
            for run in cut_halo(piece):
                if len(run) < 2:
                    continue
                L_ = _arclen(run)[-1]
                if L_ < EDGE_STUB:
                    n_edge_stub += 1
                    continue
                storm_runs.append(L_)
                runs_j.append(run)
        k_strands.append(runs_j)
    _emit_serp(k_strands, k_k)
    # green: the 22 warps, gaps where gold is over; Z11 bold
    green_runs: List[float] = []
    z_strands: List[List[Poly]] = []
    for k in range(n_q):
        runs_k: List[Poly] = []
        for piece in green_pieces[k]:
            for run in cut_halo(piece):
                if len(run) < 2:
                    continue
                L_ = _arclen(run)[-1]
                if L_ < EDGE_STUB:
                    n_edge_stub += 1
                    continue
                green_runs.append(L_)
                runs_k.append(run)
        z_strands.append(runs_k)
    _emit_serp(z_strands, k_z, bold_idx=p_lane)
    # gold: the one weft
    gold_runs: List[float] = []
    for piece in gold_pieces:
        for run in G.clip(piece, box, keep="inside"):
            if len(run) < 2:
                continue
            gold_runs.append(_arclen(run)[-1])
            out += _poly(run, color=k_v, f=feed)

    # black: the wall, broken by the slit
    for k in range(5):
        dy = -0.62 + 0.31 * k
        out += _poly([(x0 + 0.4, ay + dy), (ax - c, ay + dy)], color=k_black, f=feed)
        out += _poly([(ax + c, ay + dy), (x1 - 0.4, ay + dy)], color=k_black, f=feed)
    # black: the hill, 5 passes centred on the exact-area curve
    for k in range(5):
        dk = -HILL_HALF + 2 * HILL_HALF * k / 4.0
        sil = G.offset(curve, dk)
        for sub in G.clip(sil, box, keep="inside"):
            out += _poly(sub, color=k_black, f=feed)
    # black: the one chart mark in the throat — the 1/16 level, outside the slit
    out += _poly([(ax + c + 0.4, ay + tick_h), (ax + c + 3.4, ay + tick_h)], color=k_black, f=feed)

    # black: reed ticks at every strand mouth
    reed_mouths: List[Tuple[str, float, str]] = []

    def reed(polys: Sequence[Poly], who: str, edges_=("top", "right", "left")):
        for pl in polys:
            for r in G.clip(pl, box, keep="inside"):
                for e in (r[0], r[-1]):
                    L = 3.0
                    if hal.contains(min(max(e[0], x0 + 2.0), x1 - 2.0), min(max(e[1], y0 + 2.0), y1 - 2.0)):
                        continue
                    if "top" in edges_ and e[1] > y1 - 1.2:
                        out.extend(_poly([(e[0], y1 - 0.6), (e[0], y1 - 0.6 - L)], color=k_black, f=feed))
                        reed_mouths.append(("top", e[0], who))
                    elif "right" in edges_ and e[0] > x1 - 1.2:
                        out.extend(_poly([(x1 - 0.6, e[1]), (x1 - 0.6 - L, e[1])], color=k_black, f=feed))
                        reed_mouths.append(("right", e[1], who))
                    elif "left" in edges_ and e[0] < x0 + 1.2:
                        out.extend(_poly([(x0 + 0.6, e[1]), (x0 + 0.6 + L, e[1])], color=k_black, f=feed))
                        reed_mouths.append(("left", e[1], who))

    reed(q_polys, "Q")
    reed(k_polys, "K")
    reed(lane_polys, "Z", edges_=("right",))
    reed([weft], "V", edges_=("left", "right"))

    # black: giant type, one construction for every stroke
    out += _solid_text("SUMS", x0 + 1.5, base_sums, th, TYPE_WEIGHT, k_black, f=feed)
    out += _solid_text("TO ONE", x0 + 1.5, base_one, th, TYPE_WEIGHT, k_black, f=feed)

    # text layer: labels + footer
    for text, lx, ly, lh in labels:
        out += _stroke_text(text, lx, ly, lh, color=k_txt, f=feed)
    n_over_all = sum(1 for i in range(n_q) for g in range(16) if A_all[i][korder[g]] > UNIF)
    lines = [
        ("ATTENTION AS WEAVING · ONE REED, ONE CLOTH", 2.4, True),
        (f"{n_q} Q · {n_k} K → {n_q} Z     Σa = 1     a MAX {a_max:.3f}     "
         f"H {Hbits:.2f} / {math.log(n_k, 2):.2f} BITS", 2.0, False),
        (f"SLIT {SLIT:.0f} MM · {n_k} EQUAL BINS · LANES EQUAL PITCH {PITCH:.2f} MM, ORDER ONLY",
         2.0, False),
        (f"BOLD = QUERY {principal}, ITS ROW IS THE HILL · GOLD OVER GREEN WHERE a > 1/16 "
         f"({n_over_all} / {n_q * n_k}) · TICK = 1/16", 2.0, False),
    ]
    LEAD = 5.0
    fy = y0 + 19.5
    for k, (txt, hh, sp) in enumerate(lines):
        yy = fy - k * LEAD
        s_txt = _spaced(txt) if sp else txt
        room = W - 4.0
        while _text_width(s_txt, hh) > room and hh > 1.4:
            hh -= 0.05
        out += _stroke_text(s_txt, x0 + 2.0, yy, hh, color=k_txt, f=feed)

    # ---- checks ------------------------------------------------------------
    k_end_bins = [max(0, min(n_k - 1, int((k_end_pt[j][0] - (ax - c)) // w_bin))) for j in range(n_k)]
    mouths = {}
    for side, v_, who in reed_mouths:
        mouths.setdefault(side, []).append((v_, who))
    mouth_min = {}
    for side, lst in mouths.items():
        lst.sort()
        gaps_ = [(round(b_[0] - a_[0], 2), a_[1] + b_[1], round(a_[0], 1)) for a_, b_ in zip(lst, lst[1:])]
        mouth_min[side] = sorted(gaps_)[:4]
    q_z_x = max(abs(q_polys[t][-1][0] - lane_polys[t][0][0]) for t in range(n_q))
    LAST_STATS.update(
        sum_a=sum(A), row_sum_err=row_sum_err, a_max=a_max, entropy_bits=Hbits, temp=TEMP,
        korder=korder, Ag=[round(a, 4) for a in Ag], above_bins=above_bins,
        slit=SLIT, w_bin=w_bin, lanes_x=[round(v, 2) for v in lanes_x], qid=qid,
        seriation_cost=_cost(qid), identity_cost=_cost(list(range(n_q))),
        area_err=max(abs(h_area[g] - Ag[g] / sum(Ag)) for g in range(n_k)), hill_beta=hill_beta,
        hill_end_heights=(hy[0] * hscale, hy[-1] * hscale),
        hill_first=[round(v * hscale, 2) for v in hy[:20:2]], summit_x=summit_x - ax,
        peak=max(hy) * hscale, peak_med=peak_med, tick_h=tick_h,
        k_off=k_off, k_lane_clear=k_lane_clear, k_flow_bins=k_flow_bins, k_slit=[round(v - ax, 2) for v in k_slit],
        k_end_in_own_bin=sum(1 for j in range(n_k) if k_end_bins[j] == bin_of[j]),
        n_nudge=n_nudge, kq_pitch=kq_pitch, kq_at=kq_at, kk_where=kk_where, qk_low=qk_low, qk_crossings=n_cross, qk_ang_min=min(qk_ang) if qk_ang else None,
        kk_crossings=kk_x, storm_merges=n_storm_merge, storm_min=min(storm_runs),
        q_stubs=n_stub, edge_stubs=n_edge_stub,
        slit_err=slit_err, q_z_x=q_z_x, lane_pitch=lane_pitch, lane_pitch_at=lane_pitch_at,
        lane0_x_at_150=lane0_x_at_150, lane_exit_y=(round(lane_polys[0][-1][1], 1), round(lane_polys[-1][-1][1], 1)),
        lane_lane_x=lane_lane_x,
        pick_pitch=(round(min(pick_pitch), 3), round(max(pick_pitch), 3)), pick_sp21=pick_sp21,
        pick_sp_lane_min=round(min(pick_sp_lane), 3), pick_sp_lane0=round(pick_sp_lane[0], 3),
        pick1=(tuple(np.round(pick_seg[0][0], 1)), tuple(np.round(pick_seg[0][1], 1))),
        pick16=(tuple(np.round(pick_seg[15][0], 1)), tuple(np.round(pick_seg[15][1], 1))),
        cross_ang_min=min(cross_ang), n_cross_cloth=len(cross_ang), weft_lane_x=weft_lane_x,
        rule_ok=rule_ok, n_over=n_over, n_over_all=n_over_all,
        bold_under_picks=[g + 1 for g in range(16) if not B_drawn[principal][g]],
        bold_over_picks=[g + 1 for g in range(16) if B_drawn[principal][g]],
        gold_min=min(gold_len), gold_pieces=len(gold_len), gold_runs_min=min(gold_runs),
        green_min=min(green_runs), gold_lane_clear=gold_lane_clear,
        mouth_min=mouth_min, lead_in_y=yL, lead_out_y=yR,
        weft_len=s_w[-1],
    )
    return out
