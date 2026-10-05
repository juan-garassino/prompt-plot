"""SUMS TO ONE — r06 (iterate) of `attention-weaving`, forked from r04 (mirror-drain).

The keys die in the hill. Same seeded Q, K, V and the same softmax row as r03/r04
(22 queries x 16 keys, a_max = 0.190, H = 3.76 bits); the topology at the wall
changes, not the parameters:

  THE SLIT   16 EQUAL key bins. Key j's K spiral turns (tangent-continuous, in
             the conformal elliptic coordinates) onto its own streamline and
             ends ON THE HILL over the centre of bin j — consumed by softmax.
             Only the 22 Q streamlines cross the slit, apportioned to bins by
             the largest remainder of 22*a (seed 7: 1,1,1,1,4,3,2,1,...).
  THE HILL   exact-area histopolant on equal bins (area over bin j = a_j, so
             mean height over bin j is proportional to a_j), ramp-constrained so
             it cannot ring into false humps nor pin a plateau; drawn opaque:
             every Q/K strand stops 1.25 mm above its top pass.
  THE DRAIN  the 22 Q lanes continue as the 22 Z = AV rows (one per QUERY), the
             phi < 0 half of the same system folded down-right. 16 gold V arcs,
             born at one compact reed on the left margin, sweep the fan at
             constant depth (turned toward the lanes' normal only where the
             fold would make them cross flatter than 56 deg) and end on the
             selvage (the outermost lane). Over/under at V_j x Z_i is
             A_ij > 1/16; under-runs merge; no gold piece under 5 mm.
  PITCH      the slit is widened (bins never unequalised) until every adjacent
             pair of strands keeps >= 0.90 mm where it is tightest, measured.

CANON: Deco, flat (occlusion is the only depth cue).
LINEAGE: Anni Albers, *Black-White-Gold I* (1950): over/under as information.
Contract: attention_weaving_iterate(rng, bounds, colors=3)
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


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def attention_weaving_iterate(
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
    k_black = _pen(BLACK, colors)
    k_q = _pen(Q_PEN, colors)
    k_k = _pen(K_PEN, colors)
    k_v = _pen(V_PEN, colors)
    k_z = _pen(Z_PEN, colors)
    out: List[GCodeCommand] = []
    LAST_STATS.clear()

    box = G.Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)
    GAP = 1.15                  # over/under gap radius in the storm (r03/r04)

    # ======================================================================
    # THE NUMBERS — same seeded draws as r03/r04, so A is the same row
    # ======================================================================
    d = 16

    def _unit(n: int = d):
        v = [rng.gauss() for _ in range(n)]
        s = math.sqrt(sum(t * t for t in v)) or 1.0
        return [t / s for t in v]

    Qv = [_unit() for _ in range(n_q)]
    Kv = [_unit() for _ in range(n_k)]
    # value vectors: the draws r04 made (one 38-vector per key); the first d
    # components are used as the d_v = 16 value vector, so the RNG stream and
    # therefore every weight stays identical to the parent.
    Vv_raw = [_unit(38) for _ in range(n_k)]
    Vv = [[t for t in v[:d]] for v in Vv_raw]
    principal = n_q // 2
    for j, w_ in ((5, 0.90), (11, 0.70), (2, 0.54), (14, 0.40), (8, 0.30)):
        Kv[j] = [w_ * Qv[principal][t] + math.sqrt(1 - w_ * w_) * Kv[j][t] for t in range(d)]
        n_ = math.sqrt(sum(t * t for t in Kv[j])) or 1.0
        Kv[j] = [t / n_ for t in Kv[j]]

    S = [[sum(Qv[i][t] * Kv[j][t] for t in range(d)) * math.sqrt(d)
          for j in range(n_k)] for i in range(n_q)]
    A_MAX_TARGET = 0.190
    lo_t, hi_t = 0.05, 30.0
    for _ in range(64):
        mid = 0.5 * (lo_t + hi_t)
        if max(_softmax(S[principal], mid)) > A_MAX_TARGET:
            lo_t = mid
        else:
            hi_t = mid
    TEMP = 0.5 * (lo_t + hi_t)
    A = _softmax(S[principal], TEMP)
    # the FULL attention matrix at the same temperature: 22 rows, each sums to 1
    A_all = [_softmax(S[i], TEMP) for i in range(n_q)]
    a_max = max(A)
    Hbits = _entropy_bits(A)
    row_sum_err = max(abs(sum(r) - 1.0) for r in A_all)

    # keys dealt around the peak (a permutation of the key index; attention is
    # invariant to it) so the hill over the equal bins is ONE hill
    N_LEFT = 4        # keys dealt left of the crown (every 3rd, up to 4): the crown
                      # sits at bin 4 — off the centre, where the fold squeezes
                      # hardest, but close enough that the Q storm stays balanced
    _srt = sorted(range(n_k), key=lambda j: -A[j])
    _lf: List[int] = []
    _rt: List[int] = []
    for i, j in enumerate(_srt):
        (_lf if (i and i % 3 == 0 and len(_lf) < N_LEFT) else _rt).append(j)
    korder = list(reversed(_lf)) + _rt          # bin g holds key korder[g]
    bin_of = {j: g for g, j in enumerate(korder)}
    Ag = [A[j] for j in korder]
    nq_bin = _apportion(Ag, n_q)                # Q lanes crossing in bin g
    assert sum(nq_bin) == n_q

    # ======================================================================
    # THE SLIT — 16 EQUAL key bins. Key j's K strand lands ON THE HILL at the
    # centre of its own bin (so the 16 landings stand exactly one bin apart).
    # Only the 22 Q lanes cross the slit: bin g passes nq_bin[g] of them.
    # Lanes are placed in FLOW coordinates: a K landing high on the hill rides
    # a streamline that meets the slit nearer the centre, and no Q may share
    # it — so every lane keeps DKQ from each K streamline (DKR on the side
    # K approaches from, where it turns), PQ from every other lane.
    # ======================================================================
    PQ = 0.95        # Q-Q pitch inside a clump
    DKQ = 0.92       # K's drop to a Q lane (true separation above the hill)
    DKR = 0.92       # ... on the side K turns in from (its approach side)
    EDGE = 0.10      # a lane never sits on a bin edge
    DELTA = 0.32     # the principal query crosses 0.32 mm left of the centre line
    PB = n_k // 2 - 1                           # the bin just left of the centre
    HILL_T = 1.2     # the hill: 5 passes over 1.2 mm (normal offsets)
    HILL_GAP = 1.0 + 0.25   # strands pass UNDER it: 1 mm of paper + half a pen
    K_CLEAR = HILL_T + 0.75  # K stops 0.75 mm above the hill's top pass
    ZMAX = 0.074 * H
    c_old = 0.118 * W        # r04's half-slit (for keeping the storm's size)
    ax = x0 + 0.425 * W
    ay = y0 + 0.620 * H

    def _inv(ap_: Aperture, x: float, y: float) -> Tuple[float, float]:
        import cmath
        z = complex((x - ap_.ax) / ap_.c, (y - ap_.ay) / ap_.c)
        wv = cmath.acosh(z)
        phi_, psi_ = wv.real, wv.imag
        if phi_ < 0:
            phi_, psi_ = -phi_, -psi_
        return phi_, psi_ % (2 * math.pi)

    # the hill does not depend on the bin width (equal bins: it only
    # stretches), so it is solved ONCE on unit bins and scaled
    _ux, _uh, _uarea, hill_beta = _histopolate_ramp(list(range(n_k + 1)), Ag)

    def _hill(w: float):
        c_ = 8.0 * w
        edges_ = [ax - c_ + g * w for g in range(n_k + 1)]
        hx_ = [ax - c_ + w * u for u in _ux]
        hy_ = [v / w for v in _uh]
        hs_ = ZMAX / max(hy_)
        curve_ = [(px, ay + py * hs_) for px, py in zip(hx_, hy_)]
        return c_, edges_, hx_, hy_, list(_uarea), hs_, curve_

    def _k_targets(ap_: Aperture, edges_, curve_):
        """Where each bin's K meets the hill: on the bin's centre line, K_CLEAR
        from the drawn curve; returned with the streamline it rides."""
        cv = np.asarray(curve_)
        out_ = []
        for g in range(n_k):
            kc = 0.5 * (edges_[g] + edges_[g + 1])
            ys = np.linspace(ay, ay + ZMAX + 12.0, 900)
            dd = _near_dist([(kc, yy) for yy in ys], curve_)
            ytop = float(np.interp(kc, cv[:, 0], cv[:, 1]))
            above = [(yy, dv) for yy, dv in zip(ys, dd) if yy > ytop]
            yt = next(yy for yy, dv in above if dv >= K_CLEAR)
            ph, ps = _inv(ap_, kc, yt)
            ratio = math.sqrt(math.sinh(ph) ** 2 + math.sin(ps) ** 2) / max(1e-6, math.sin(ps))
            out_.append((kc, yt, ph, ps, ap_.ax + ap_.c * math.cos(ps), ratio))
        return out_

    KB, BR = 0.225, 1.15     # the fold of the lower fan (Z = AV bends the flow)
    P_FAN = 0.91             # the pitch every pair of lanes must keep IN THE FAN

    def _kappa(c_: float):
        """Fan compression kappa(x): the narrowest separation, anywhere below
        the wall, of two lanes that cross the slit 0.4 mm apart at x, over
        0.4. The fold squeezes the lanes near the centre (kappa ~ 0.8), so
        the slit pitch there must be P_FAN / kappa for the fan to hold P_FAN."""
        ap_ = Aperture(ax=ax, ay=ay, c=c_)

        def lane_(xs_):
            ps = ap_.psi_for_slit_x(xs_ - ax)
            pts = []
            for k in range(0, 721):
                s = 3.9 * (k / 720) ** 1.35
                m = KB + (1.0 - KB) / math.cosh(BR * s)
                x_, y_ = ap_.pt(-s, ps * m)
                if x0 < x_ < x1 and y0 < y_ < y1:
                    pts.append((x_, y_))
            return np.asarray(pts)

        xs = np.linspace(ax - c_ + 0.3, ax + c_ - 1.3, 29)
        ks = []
        for xs_ in xs:
            P, Q_ = lane_(xs_), lane_(xs_ + 1.0)
            dmin = np.sqrt(((P[:, None, :] - Q_[None, :, :]) ** 2).sum(2)).min()
            ks.append(min(1.0, dmin / 1.0))
        return lambda x: float(np.interp(x, xs, ks))

    def _lanes(edges_, w: float, kxs: List[float], kap):
        """DP over bins: each bin's lanes as at most two clumps, inside the bin,
        clear of every K streamline, every adjacent pair at the pitch that
        survives the fold (max(PQ, P_FAN / kappa)). Maximise the worst
        clearance, then keep clumps near their bin centre.
        Returns (positions, lane_bin, score) or None."""
        import bisect
        STEP = 0.05
        LIP = 1.5
        # K's streamline and a Q lane are both streamlines: their separation
        # above the hill is the slit separation x ratio(phi_end) — exact
        forb = [(xs_ - DKQ / r_, xs_ + DKR / r_) for xs_, r_ in kxs]
        xp = ax - DELTA

        def req(x: float) -> float:
            return max(PQ, P_FAN / max(0.5, kap(x)))

        def clear(x: float) -> float:
            m = 9.0
            for a_, b_ in forb:
                if a_ < x < b_:
                    return -1.0
                m = min(m, a_ - x if x <= a_ else x - b_)
            return m

        def clump(s: float, k: int) -> List[float]:
            out_ = [s]
            for _ in range(k - 1):
                out_.append(out_[-1] + req(out_[-1]))
            return out_

        def gen(n: int, lo: float, hi: float, centre: float):
            if n == 0:
                return [([], (9.0, 0.0))]
            grid = [lo + STEP * k for k in range(int((hi - lo) / STEP) + 1)]
            res = []
            for k1 in range(1, n + 1):
                for s1 in grid:
                    c1 = clump(s1, k1)
                    if c1[-1] > hi + 1e-9:
                        break
                    rest = n - k1
                    if rest == 0:
                        seconds = [None]
                    else:
                        seconds = [s2 for s2 in grid[::2] if s2 >= c1[-1] + req(c1[-1]) + 0.3]
                    for s2 in seconds:
                        pos = c1 + ([] if s2 is None else clump(s2, rest))
                        if pos[-1] > hi + 1e-9:
                            continue
                        cl = min(clear(p) for p in pos)
                        if cl < 0:
                            continue
                        dev = abs(0.5 * (pos[0] + pos[-1]) - centre)
                        res.append((pos, (min(cl, 1.0) - (0.25 if s2 is not None else 0.0), dev)))
            return res

        def better(u, v):          # (bottleneck, deviation): high, then low
            return u[0] > v[0] + 1e-9 or (abs(u[0] - v[0]) <= 1e-9 and u[1] < v[1])

        states = [(-1e9, (9.0, 0.0), [])]
        lane_bin_: List[int] = []
        for g in range(n_k):
            n = nq_bin[g]
            lo = edges_[g] + (LIP if g == 0 else EDGE)
            hi = edges_[g + 1] - (LIP if g == n_k - 1 else EDGE)
            centre = 0.5 * (edges_[g] + edges_[g + 1])
            if g == PB:
                if n < 1 or clear(xp) < 0:
                    return None
                cands = []
                for pos, sc in gen(n - 1, lo, xp - req(xp - 1.2) - 0.2, centre):
                    cands.append((pos + [xp], (min(sc[0], min(clear(xp), 1.0)), sc[1])))
            else:
                cands = gen(n, lo, hi, centre)
            states.sort(key=lambda s: s[0])
            lasts = [s[0] for s in states]
            pref = []
            for s in states:
                if not pref or better(s[1], pref[-1][1]):
                    pref.append(s)
                else:
                    pref.append(pref[-1])
            best_by_last: dict = {}
            for pos, sc in cands:
                if pos:
                    k = len(states) - 1
                    while k >= 0 and (pos[0] - lasts[k] < req(lasts[k]) + (
                            0.2 if abs(lasts[k] - xp) < 1e-9 else 0.0) - 1e-9):
                        k -= 1
                    if k < 0:
                        continue
                    pl, psc, ppos = pref[k]
                    v = (min(psc[0], sc[0]), psc[1] + sc[1])
                    key = round(pos[-1], 3)
                    if key not in best_by_last or better(v, best_by_last[key][1]):
                        best_by_last[key] = (pos[-1], v, ppos + pos)
                else:
                    for s in states:
                        v = (min(s[1][0], sc[0]), s[1][1])
                        key = round(s[0], 3)
                        if key not in best_by_last or better(v, best_by_last[key][1]):
                            best_by_last[key] = (s[0], v, s[2])
            if not best_by_last:
                return None
            states = list(best_by_last.values())
            lane_bin_ += [g] * n
        best = states[0]
        for s in states[1:]:
            if better(s[1], best[1]):
                best = s
        return best[2], lane_bin_, best[1][0]

    def _try(w: float):
        c_, edges_, hx_, hy_, h_area_, hs_, curve_ = _hill(w)
        ap_ = Aperture(ax=ax, ay=ay, c=c_)
        ktg_ = _k_targets(ap_, edges_, curve_)
        lay_ = _lanes(edges_, w, [(t_[4], t_[5]) for t_ in ktg_], _kappa(c_))
        return lay_, (c_, edges_, hx_, hy_, h_area_, hs_, curve_, ap_, ktg_)

    # widen the SLIT (never unequalise the bins) until every lane fits:
    # coarse steps up from r04's slit cut into 16, then bisect back down
    w_lo = 51.92 / 16.0
    lay, pack = _try(w_lo)
    w_bin = w_lo
    if lay is None:
        w_hi = w_lo
        while lay is None:
            w_lo, w_hi = w_hi, w_hi + 0.25
            lay, pack = _try(w_hi)
        good = (w_hi, lay, pack)
        while w_hi - w_lo > 0.02:
            wm = 0.5 * (w_lo + w_hi)
            lm, pm = _try(wm)
            if lm is None:
                w_lo = wm
            else:
                w_hi, good = wm, (wm, lm, pm)
        w_bin, lay, pack = good
    c, edges, hx, hy, h_area, hscale, curve, ap, ktg = pack
    lanes_x, lane_bin, lay_score = lay
    n_lane = len(lanes_x)
    assert n_lane == n_q
    principal_lane_x = ax - DELTA
    p_lane = min(range(n_lane), key=lambda t: abs(lanes_x[t] - principal_lane_x))
    slit_pitch = min(b - a for a, b in zip(lanes_x, lanes_x[1:]))
    k_xs = [t_[4] for t_ in ktg]
    kq_slit = min(abs(lx - kx) for lx in lanes_x for kx in k_xs)

    # query identity per lane: which query rides which lane is free (attention
    # is permutation-invariant over queries) — seriate them so that, lane to
    # lane, the pattern "attends value j above uniform" changes as little as
    # possible; the principal query is pinned to the centre line.
    UNIF = 1.0 / n_k
    Bm = [[1 if A_all[i][j] > UNIF else 0 for j in range(n_k)] for i in range(n_q)]

    def _ham(a_: int, b_: int) -> int:
        return sum(1 for j in range(n_k) if Bm[a_][j] != Bm[b_][j])

    others = [i for i in range(n_q) if i != principal]
    # greedy chain from the principal outward, then 2-opt on each side
    seq = [principal]
    pool = set(others)
    left_n, right_n = p_lane, n_lane - 1 - p_lane
    left: List[int] = []
    right: List[int] = []
    while pool:
        for side in (right, left):
            if not pool:
                break
            if side is right and len(right) >= right_n:
                continue
            if side is left and len(left) >= left_n:
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
        for a_ in range(n_lane):
            for b_ in range(a_ + 1, n_lane):
                if p_lane in (a_, b_):
                    continue
                q2 = list(qid)
                q2[a_], q2[b_] = q2[b_], q2[a_]
                if _cost(q2) < _cost(qid):
                    qid, improved = q2, True
    seriation_cost = _cost(qid)
    ident_cost = _cost(list(range(n_q)))

    # ======================================================================
    # THE SOFTMAX HILL — histopolant on EQUAL bins: the area over bin g IS
    # a_g, so the mean height over bin g is exactly proportional to a_g.
    # ======================================================================
    prof = [(ax - c, ay)] + curve + [(ax + c, ay)]
    bin_mean = [Ag[g] / w_bin * hscale for g in range(n_k)]
    srt_mean = sorted(bin_mean)
    peak_med = max(bin_mean) / (0.5 * (srt_mean[7] + srt_mean[8]))
    # the hill is OPAQUE to the storm: a Q strand stops HILL_GAP above the
    # hill's top pass and re-emerges below the slit as its Z lane
    top_ = G.offset(curve, HILL_T + HILL_GAP)
    band_poly = top_ + [(top_[-1][0], ay - 0.05), (top_[0][0], ay - 0.05)]
    hill_band = G.Polygon(band_poly)

    # ======================================================================
    # Q — pure streamlines, one per query, landing on its lane
    # ======================================================================
    PHI_MAX = 2.85
    psi_q = [ap.psi_for_slit_x(xx - ax) for xx in lanes_x]

    def q_path(t: int) -> Poly:
        ps = psi_q[t]
        return [ap.pt(PHI_MAX * (1.0 - u / 170.0) ** 1.22, ps) for u in range(171)]

    q_polys = [_resample(q_path(t), 1.1) for t in range(n_lane)]

    def _phi_keep(phi_old: float) -> float:
        """The phi on the wider aperture whose ellipse has r04's semi-major."""
        return math.acosh(max(1.0, math.cosh(phi_old) * c_old / c))

    # ======================================================================
    # K — r04's sweep; then a tight tangent-continuous turn onto its own
    # streamline, which it rides down to the hill over its own bin. The start
    # is carried back to the frame when it began inside the sheet.
    # ======================================================================
    psi_k_end = [ktg[bin_of[j]][3] for j in range(n_k)]
    phi_k_end = [ktg[bin_of[j]][2] for j in range(n_k)]
    order = sorted(range(n_k), key=lambda j: psi_k_end[j])
    rank = {j: r for r, j in enumerate(order)}
    # the sweep starts of r04, except the lowest are lifted off the wall's arm
    # (0.018 pi -> 0.050 pi) so that, carried back, they reach the right frame
    # as a spread fan instead of a bundle hugging the wall
    psi_k_start = [0.050 * math.pi + 0.223 * math.pi * (rank[j] / max(1, n_k - 1))
                   for j in range(n_k)]
    phi_k = [_phi_keep(1.52 + 1.52 * (rank[j] / max(1, n_k - 1))) for j in range(n_k)]
    K_FIL_A = 0.08              # fillet leg on the sweep, fraction of its length
    K_FIL_B = 0.55              # ... and on the drop, relative to the first leg

    def _pp(pts):
        return [ap.pt(f, s) for f, s in pts]

    k_drop_from: List[int] = []

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
            dphi, dpsi = P0[0] - Pc[0], P0[1] - Pc[1]      # backward direction
            # (a) the sweep's own straight line in (phi, psi), carried back:
            #     the same spiral, if it reaches the frame above the wall
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
                # (b) otherwise bend toward a ray BELOW every Q ray (so the
                #     carried-back start crosses nothing) and leave the frame
                # the floor sits BETWEEN the two Q streamlines that bracket
                # a0, so the carried-back start crosses no Q at all
                if psi_f_set is not None:
                    psi_f = psi_f_set
                else:
                    psi_f = _k_floor(a0)
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

    psi_q_min = min(psi_q)
    k_polys: List[Poly] = []
    k_drops: List[Poly] = []
    k_end_pt: List[Tuple[float, float]] = []
    def _k_floor(a0: float) -> float:
        below = [q for q in psi_q if q < a0 - 0.015]
        if below:
            return max(below) + 0.45 * (a0 - max(below))
        return min(0.80 * a0, psi_q_min - 0.05)

    # pass 1: which starts can be carried back as the same spiral?
    k_lin_ok = {j: True for j in range(n_k)}
    k_lin_exit = {j: psi_k_start[j] for j in range(n_k)}
    for j in range(n_k):
        k_param(j)
    # pass 2: every K at or below the highest rank that cannot, bends to a
    # floor; floors rise strictly with rank so the carried-back starts nest
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
    for j in range(n_k):
        ext, body, i_drop = k_param(j, force_exp=rank[j] <= r_fail,
                                    psi_f_set=k_floor.get(j))
        pts = _pp(ext + body)
        k_polys.append(_resample(pts, 1.1))
        k_drops.append(pts[i_drop:])
        k_end_pt.append(pts[-1])


    # ---- Q.K^T: every crossing on the sheet, over/under by sign(s_ij) ------
    q_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_lane)]
    k_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_k)]
    n_cross = 0
    qk_ang: List[float] = []
    k_marks: List[list] = [[] for _ in range(n_k)]
    q_marks: List[list] = [[] for _ in range(n_lane)]
    qk_where: list = []
    for j in range(n_k):
        for t in range(n_lane):
            for px, py, ang in _crossings_ang(k_polys[j], q_polys[t]):
                if not (x0 + 1 < px < x1 - 1 and ay + 1.0 < py < y1 - 1):
                    continue
                n_cross += 1
                qk_ang.append(ang)
                qk_where.append((round(ang, 1), j, t, round(px, 1), round(py, 1)))
                k_under = S[qid[t]][j] >= 0.0
                (k_cuts[j] if k_under else q_cuts[t]).append((px, py, GAP))
                k_marks[j].append((px, py, k_under))
                q_marks[t].append((px, py, not k_under))

    # ======================================================================
    # BELOW THE WALL — the 22 Q lanes continue as the 22 Z = AV rows, the
    # phi < 0 half of the same system, bent down-right (r04's fold).
    # ======================================================================

    def bend(s: float) -> float:
        return KB + (1.0 - KB) / math.cosh(BR * s)

    def low(s: float, psi: float) -> Tuple[float, float]:
        return ap.pt(-s, psi * bend(s))

    S_LANE = 3.9
    NL = 360

    def lane_s(k: int) -> float:
        return S_LANE * (k / NL) ** 1.35

    lane_polys = [_resample([low(lane_s(k), psi_q[t]) for k in range(NL + 1)], 1.1)
                  for t in range(n_lane)]
    slit_err = max(abs(lane_polys[t][0][0] - lanes_x[t]) for t in range(n_lane))

    # ---- V: born at the left-margin reed, sweeping the fan like K sweeps Q -
    GAP_LO = 0.62

    def _jac(s: float, psi: float):
        e = 1e-4
        p0 = low(s, psi)
        ps = low(s + e, psi)
        pp = low(s, psi + e)
        return p0, ((ps[0] - p0[0]) / e, (ps[1] - p0[1]) / e), \
            ((pp[0] - p0[0]) / e, (pp[1] - p0[1]) / e)

    def v_trace(s0: float, psi0: float, psi_end: float, pitch: float,
                step: float = 0.5) -> Poly:
        s, psi = s0, psi0
        pts: Poly = []
        for _ in range(1600):
            p0, Js, Jp = _jac(s, psi)
            pts.append(p0)
            if psi <= psi_end or s < 0.3:
                break
            tl = math.hypot(*Js) or 1.0
            T = (Js[0] / tl, Js[1] / tl)
            N = (T[1], -T[0])
            if N[0] * Jp[0] + N[1] * Jp[1] > 0:
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
        return pts

    PSI_A = 0.5 * (math.pi + max(psi_q))       # just outside the fan's open flank
    selvage = n_lane - 1                        # the outermost lane: V ends ON it
    psi_sel = psi_q[selvage]
    # V is K's mirror: an arc of CONSTANT depth s across the whole fan (K
    # sweeps the storm along its own ellipse, V sweeps the drain along its
    # own), from just outside the open flank to the selvage — the outermost
    # lane, where it ends. Depths spaced evenly; the deepest stays clear of
    # the title. Before the flank each V is carried from ONE compact reed on
    # the left margin, so gold fans out from its mouth the way Q does.
    V_MIN_ANG = 56.0

    def v_arc(s0: float, psi0: float, psi_end: float, step: float = 0.35) -> Poly:
        """Walk the constant-depth arc s = s0 toward the selvage; wherever that
        arc would meet the lanes flatter than V_MIN_ANG, turn it toward the
        lanes' normal just enough to cross at V_MIN_ANG (so depth drifts only
        where the fold forces it)."""
        s, psi = s0, psi0
        pts: Poly = []
        cmin = math.cos(math.radians(V_MIN_ANG))
        for _ in range(3000):
            p0, Js, Jp = _jac(s, psi)
            pts.append(p0)
            if psi <= psi_end or not (x0 - 5 < p0[0] < x1 + 5 and y0 - 5 < p0[1] < y1 + 5):
                break
            tl = math.hypot(*Js) or 1.0
            T = (Js[0] / tl, Js[1] / tl)                  # lane direction
            ul = math.hypot(*Jp) or 1.0
            U = (-Jp[0] / ul, -Jp[1] / ul)                # constant-s, psi falling
            N = (T[1], -T[0])
            if N[0] * U[0] + N[1] * U[1] < 0:
                N = (-N[0], -N[1])
            cu = U[0] * T[0] + U[1] * T[1]                # cos(angle to lane)
            if abs(cu) > cmin:
                # rotate within the (T, N) frame to exactly V_MIN_ANG
                sgn = 1.0 if cu > 0 else -1.0
                ang = math.radians(V_MIN_ANG)
                D = (N[0] * math.sin(ang) + sgn * T[0] * math.cos(ang),
                     N[1] * math.sin(ang) + sgn * T[1] * math.cos(ang))
            else:
                D = U
            det = Js[0] * Jp[1] - Js[1] * Jp[0]
            if abs(det) < 1e-12:
                break
            ds = (D[0] * Jp[1] - D[1] * Jp[0]) / det
            dp = (Js[0] * D[1] - Js[1] * D[0]) / det
            s += ds * step
            psi += dp * step
        return _resample(pts, 0.5)

    V_S_IN, V_S_OUT = 0.60, 1.52
    V_SEL_CLEAR = 0.8
    v_polys: List[Poly] = []
    v_reed_y: List[float] = []
    v_entry: List[Tuple[float, float]] = []
    V_REED_TOP, V_REED_DY = ay - 16.0, 2.6
    for g in range(n_k):
        s_g = V_S_IN + (V_S_OUT - V_S_IN) * g / max(1, n_k - 1)
        body = v_arc(s_g, PSI_A, psi_sel - 0.04)
        dsel = _near_dist(body, lane_polys[selvage])
        cut = len(body)
        for u in range(3, len(body)):
            if dsel[u] <= V_SEL_CLEAR:
                cut = u
                break
        body = body[:cut]
        e0, e1 = body[0], body[3]
        tl = math.hypot(e1[0] - e0[0], e1[1] - e0[1]) or 1.0
        tan1 = ((e1[0] - e0[0]) / tl, (e1[1] - e0[1]) / tl)
        # ONE compact reed on the left margin (the loom's reed): the gold
        # leaves it square to the frame and fans out to its depth in the fan
        ry = V_REED_TOP - g * V_REED_DY
        L = math.hypot(e0[0] - x0, e0[1] - ry)
        t0 = (0.55 * L, 0.0)
        appr = _hermite((x0 - 2.0, ry), t0, e0, (tan1[0] * 0.55 * L, tan1[1] * 0.55 * L), 90)
        v_polys.append(_resample(appr[:-1] + body, 1.0))
        v_reed_y.append(ry)
        v_entry.append(e0)

    # ---- Z = AV, computed: one output row per QUERY -------------------------
    # z_i = sum_j A_ij v_j ; the lane's outlet reed length is |z_i|
    Zrow = [[sum(A_all[qid[t]][j] * Vv[j][u] for j in range(n_k)) for u in range(d)]
            for t in range(n_lane)]
    Znorm = [math.sqrt(sum(v * v for v in z)) for z in Zrow]

    # ---- V x Z: over/under = does query i attend value j above uniform? ----
    V_MIN_PIECE = 5.0
    lane_cuts: List[List[Tuple[float, float, float]]] = [[] for _ in range(n_lane)]
    v_gaps: List[List[Tuple[float, float]]] = [[] for _ in range(n_k)]   # arclength
    lane_marks: List[list] = [[] for _ in range(n_lane)]
    n_vx = 0
    n_flip = 0
    n_merge = 0
    v_angles: List[float] = []
    per_pair: List[int] = []
    flips: List[Tuple[int, int, float]] = []
    for g in range(n_k):
        j = korder[g]
        vp = v_polys[g]
        sv = _arclen(vp)
        VP = np.asarray(vp)
        hits = []            # [arclength, x, y, angle, lane, over?, |a - 1/16|]
        for t in range(n_lane):
            if t == selvage:
                continue
            hh = _crossings_ang(vp, lane_polys[t])
            on = [(px, py, a) for px, py, a in hh
                  if x0 + 0.5 < px < x1 - 0.5 and y0 + 0.5 < py < y1 - 0.5]
            per_pair.append(len(on))
            for px, py, a in on:
                k_ = int(np.argmin(np.hypot(VP[:, 0] - px, VP[:, 1] - py)))
                # refine the arclength on the segment either side of vertex k_
                best_s = sv[k_]
                for kk in (k_ - 1, k_):
                    if 0 <= kk < len(vp) - 1:
                        ax_, ay_ = vp[kk]
                        bx_, by_ = vp[kk + 1]
                        L_ = math.hypot(bx_ - ax_, by_ - ay_) or 1e-9
                        u_ = ((px - ax_) * (bx_ - ax_) + (py - ay_) * (by_ - ay_)) / L_ ** 2
                        if -1e-6 <= u_ <= 1 + 1e-6:
                            best_s = sv[kk] + u_ * L_
                hits.append([best_s, px, py, a, t, A_all[qid[t]][j] > UNIF,
                             abs(A_all[qid[t]][j] - UNIF), False])
        hits.sort(key=lambda h: h[0])
        # CRAFT RULE (declared): no gold piece shorter than 5 mm.
        #  1. consecutive V-under gaps with no V-over between them MERGE into
        #     one gap (V passes under the run of lanes in one stroke) — no lie;
        #  2. a short piece that holds a V-over crossing is resolved by turning
        #     the crossing whose weight is CLOSEST to uniform — counted.
        for _ in range(400):
            # gap intervals from unders, merged when the piece between is short
            # and no over-crossing sits in it
            unders = [h for h in hits if not h[5]]
            overs_s = [h[0] for h in hits if h[5]]
            ivs: List[List[float]] = []
            for h in unders:
                a_, b_ = h[0] - GAP_LO, h[0] + GAP_LO
                if ivs and a_ - ivs[-1][1] < V_MIN_PIECE and not any(
                        ivs[-1][1] < s_ < a_ for s_ in overs_s):
                    ivs[-1][1] = b_
                else:
                    ivs.append([a_, b_])
            # pieces between gaps (and the two ends)
            cuts_ = [0.0] + [v for iv in ivs for v in iv] + [sv[-1]]
            bad = None
            for k in range(0, len(cuts_), 2):
                pa, pb = cuts_[k], cuts_[k + 1]
                if pb - pa < V_MIN_PIECE and not (k == 0 and k + 1 == len(cuts_) - 1):
                    bad = (pa, pb)
                    break
            if bad is None:
                break
            # the crossings that bound or sit in the short piece
            inv = [h for h in hits if bad[0] - GAP_LO - 1e-6 <= h[0] <= bad[1] + GAP_LO + 1e-6
                   and not h[7]]
            if not inv:
                break
            h = min(inv, key=lambda h: h[6])
            h[5] = not h[5]
            h[7] = True
            n_flip += 1
            flips.append((g, h[4], round(h[6], 4)))
        n_merge += sum(1 for iv in ivs if iv[1] - iv[0] > 2 * GAP_LO + 1e-6)
        v_gaps[g] = [tuple(iv) for iv in ivs]
        for sv_, px, py, a, t, over, _m, _f in hits:
            n_vx += 1
            v_angles.append(a)
            lane_marks[t].append((px, py, over))
            if over:
                lane_cuts[t].append((px, py, GAP_LO))
    V_PIECES: List[float] = []

    def _keep_by_s(poly: Poly, gaps: Sequence[Tuple[float, float]]) -> List[Poly]:
        s_ = _arclen(poly)
        runs: List[Poly] = []
        cur: Poly = []
        gi = 0

        def in_gap(x: float) -> bool:
            return any(a_ < x < b_ for a_, b_ in gaps)

        def pt_at(x: float):
            k = max(0, min(len(s_) - 2, bisect_right(s_, x) - 1))
            L_ = s_[k + 1] - s_[k] or 1e-9
            u_ = (x - s_[k]) / L_
            return (poly[k][0] + (poly[k + 1][0] - poly[k][0]) * u_,
                    poly[k][1] + (poly[k + 1][1] - poly[k][1]) * u_)
        from bisect import bisect_right
        marks = sorted({0.0, s_[-1]} | {v for iv in gaps for v in iv if 0 < v < s_[-1]})
        for a_, b_ in zip(marks, marks[1:]):
            mid_ = 0.5 * (a_ + b_)
            if in_gap(mid_):
                continue
            seg = [pt_at(a_)] + [poly[k] for k in range(len(poly)) if a_ < s_[k] < b_] + [pt_at(b_)]
            runs.append(seg)
            V_PIECES.append(b_ - a_)
        return runs


    # the same craft rule for green: consecutive lane gaps (V over) whose
    # green piece between would be shorter than LANE_MIN merge into one gap
    # — the lane dips under a run of gold — unless a V-under sits between
    LANE_MIN = 2.5
    lane_gaps: List[List[Tuple[float, float]]] = []
    n_lane_merge = 0
    for t in range(n_lane):
        LP = np.asarray(lane_polys[t])
        sl = _arclen(lane_polys[t])
        mk = []
        for px, py, over in lane_marks[t]:
            k_ = int(np.argmin(np.hypot(LP[:, 0] - px, LP[:, 1] - py)))
            mk.append((sl[k_], over))
        mk.sort()
        unders_s = [s_ for s_, ov in mk if not ov]
        ivs: List[List[float]] = []
        for s_, ov in mk:
            if not ov:
                continue
            a_, b_ = s_ - GAP_LO, s_ + GAP_LO
            if ivs and a_ - ivs[-1][1] < LANE_MIN and not any(
                    ivs[-1][1] < u_ < a_ for u_ in unders_s):
                ivs[-1][1] = b_
                n_lane_merge += 1
            else:
                ivs.append([a_, b_])
        lane_gaps.append([tuple(iv) for iv in ivs])

    vv_x = sum(len(_crossings_ang(v_polys[g], v_polys[h_]))
               for g in range(n_k) for h_ in range(g + 1, n_k))
    ll_x = sum(len(_crossings_ang(lane_polys[t], lane_polys[t + 1]))
               for t in range(n_lane - 1))
    kk_x = sum(len(_crossings_ang(k_polys[a_], k_polys[b_]))
               for a_ in range(n_k) for b_ in range(a_ + 1, n_k))

    # ---- measured pitches (true separations, not matched-depth) ------------
    def _clip_pts(pl):
        return [p for p in pl if x0 < p[0] < x1 and y0 < p[1] < y1]

    lane_exit = []
    for t in range(n_lane):
        e_ = next((p for p in lane_polys[t] if not (x0 < p[0] < x1 and y0 < p[1] < y1)), None)
        lane_exit.append("none" if e_ is None else ("right" if e_[0] >= x1 else "bottom"))
    lane_pitch = 1e9
    lane_pitch_at = None
    for t in range(n_lane - 1):
        pa = _clip_pts(lane_polys[t])
        dd = _near_dist(pa, lane_polys[t + 1])
        k_ = int(np.argmin(dd))
        if dd[k_] < lane_pitch:
            lane_pitch = float(dd[k_])
            lane_pitch_at = (t, round(pa[k_][0], 1), round(pa[k_][1], 1))
    # K's drop vs every Q lane (only the part below the fillet: the parallel run)
    kq_pitch = 1e9
    for j in range(n_k):
        tail_pts = _resample(k_drops[j], 0.5)
        for t in range(n_lane):
            dd = _near_dist(tail_pts, q_polys[t])
            kq_pitch = min(kq_pitch, float(dd.min()))
    vv_pitch = 1e9
    vv_at = None
    for g in range(n_k - 1):
        pa = _clip_pts(v_polys[g])[::2]
        dd = _near_dist(pa, v_polys[g + 1])
        k_ = int(np.argmin(dd))
        if dd[k_] < vv_pitch:
            vv_pitch = float(dd[k_])
            vv_at = (g, round(pa[k_][0], 1), round(pa[k_][1], 1))
    kk_pitch = 1e9
    for r_ in range(n_k - 1):
        ja, jb = order[r_], order[r_ + 1]
        dd = _near_dist(_clip_pts(k_polys[ja])[::2], k_polys[jb])
        kk_pitch = min(kk_pitch, float(dd.min()))
    min_pitch = min(slit_pitch, lane_pitch, kq_pitch, vv_pitch, kk_pitch)

    # ======================================================================
    # LABELS — placed, then honoured as halos
    # ======================================================================
    halos: List[G.Region] = []
    labels: List[Tuple[str, float, float, float, Optional[int]]] = []

    def label(text: str, x: float, y: float, h: float, pen, pad: float = 1.3,
              spaced: bool = False):
        s_ = _spaced(text) if spaced else text
        w_ = _text_width(s_, h)
        labels.append((s_, x, y, h, pen))
        halos.append(G.Rect(x - pad, y - pad, x + w_ + pad, y + h + pad))
        return w_

    # SOFTMAX against the right jamb, on the wall's arm
    label("SOFTMAX", ax + c + 1.9, ay + 1.4, 2.6, k_black, pad=1.0, spaced=True)
    # Q at the left margin; K mirrors it at the right margin
    LAB_H = 4.6
    q_lab_y = y1 - 0.135 * H
    label("Q", x0 + 0.012 * W, q_lab_y, LAB_H, k_q, pad=1.2)
    label("K", x1 - 0.012 * W - _text_width("K", LAB_H), q_lab_y, LAB_H, k_k, pad=1.2)
    # the principal query, named where it enters the sheet
    pl_txt = f"Q{principal} · ITS ROW IS THE HILL"
    pl_h = 2.1
    label(pl_txt, principal_lane_x + 2.2, y1 - 9.0, pl_h, k_q, pad=0.9)
    # V at its mouth: above the top reed, flush with the frame
    label("V", x0 + 0.012 * W, max(v_reed_y) + 3.0, LAB_H, k_v, pad=1.2)
    # the title is a mass the flow must respect: its boxes are halos too
    th = 15.0
    ty = y0 + 0.205 * H
    base_one = ty - th * 1.62
    for word, yy in (("SUMS", ty), ("TO ONE", base_one)):
        ww = giant_type_width(word, th, spaced=True)
        halos.append(G.Rect(x0 + 0.5 - 1.5, yy - 2.5, x0 + 1.5 + ww + 2.5, yy + th + 2.5))
    # Z = AV on the TO ONE baseline, flush right to the frame, at the outlet
    zl = "Z = AV"
    zl_h = 4.6
    label(zl, x1 - 0.012 * W - _text_width(zl, zl_h), base_one, zl_h, k_z, pad=1.2)

    # ======================================================================
    # EMIT — back to front
    # ======================================================================
    hal = G.Union(*halos) if halos else None

    def cut_halo(src: Poly) -> List[Poly]:
        runs = G.clip(src, box, keep="inside")
        if hal is not None:
            runs = [r for run in runs for r in G.clip(run, hal, keep="outside")]
        return runs

    # (no scaffold: r04's dotted equipotentials crossed the throat and the
    #  label; the storm and the drain carry the coordinate system themselves)

    # the storm: Q passes UNDER the hill (the band is cut out of it)
    Q_STUB = 3.0     # a Q piece left inside a low hill shorter than this is
                     # not drawn: the strand simply goes under and re-emerges
    n_stub = 0
    short_bits: list = []
    EDGE_STUB = 2.0  # a piece the frame or a label halo leaves under 2 mm is dropped
    n_edge_stub = 0
    STORM_MIN = 3.0  # no Q or K piece between two under-gaps shorter than this
    n_storm_merge = 0
    storm_runs: List[float] = []
    for t in range(n_lane):
        gq, nm = _merged_gaps(q_polys[t], q_marks[t], GAP, STORM_MIN)
        n_storm_merge += nm
        for piece in _split_by_gaps(q_polys[t], gq):
            for run in cut_halo(piece):
                for r2 in G.clip(run, hill_band, keep="outside"):
                    if r2[-1][1] < ay + ZMAX + 3.0 and _arclen(r2)[-1] < Q_STUB:
                        n_stub += 1
                        continue
                    if _arclen(r2)[-1] < EDGE_STUB:
                        n_edge_stub += 1
                        continue
                    storm_runs.append(_arclen(r2)[-1])
                    if storm_runs[-1] < 2.5:
                        short_bits.append(('Q', t, round(r2[0][0], 1), round(r2[0][1], 1), round(storm_runs[-1], 2)))
                    out += _cut_and_emit(r2, [], k_q, box, f=feed,
                                         passes=2 if t == p_lane else 1, pitch=0.34)
    for j in range(n_k):
        gk, nm = _merged_gaps(k_polys[j], k_marks[j], GAP, STORM_MIN)
        n_storm_merge += nm
        for piece in _split_by_gaps(k_polys[j], gk):
            for run in cut_halo(piece):
                if len(run) >= 2 and _arclen(run)[-1] < EDGE_STUB:
                    n_edge_stub += 1
                    continue
                if len(run) >= 2:
                    storm_runs.append(_arclen(run)[-1])
                    if storm_runs[-1] < 2.5:
                        short_bits.append(('K', j, round(run[0][0], 1), round(run[0][1], 1), round(storm_runs[-1], 2)))
                    out += _poly(run, color=k_k, f=feed)

    # THE WALL: one black rule, one hole
    for k in range(5):
        dy = -0.62 + 0.31 * k
        out += _poly([(x0 + 0.4, ay + dy), (ax - c, ay + dy)], color=k_black, f=feed)
        out += _poly([(ax + c, ay + dy), (x1 - 0.4, ay + dy)], color=k_black, f=feed)

    gold_runs: List[float] = []
    # the drain: Z lanes, then V
    green_runs: List[float] = []
    for t in range(n_lane):
        for piece in _keep_by_s(lane_polys[t], lane_gaps[t]):
            for run in cut_halo(piece):
                if len(run) < 2:
                    continue
                if _arclen(run)[-1] < EDGE_STUB:
                    n_edge_stub += 1
                    continue
                green_runs.append(_arclen(run)[-1])
                if green_runs[-1] < 2.5:
                    short_bits.append(('Z', t, round(run[0][0], 1), round(run[0][1], 1), round(green_runs[-1], 2)))
                out += _poly(run, color=k_z, f=feed)
    for g in range(n_k):
        for piece in _keep_by_s(v_polys[g], v_gaps[g]):
            for run in cut_halo(piece):
                gold_runs.append(_arclen(run)[-1])
                out += _poly(run, color=k_v, f=feed)

    # THE HILL on top: 5 passes, normal offsets, jambs down to the wall
    for k in range(5):
        dk = HILL_T * k / 4.0
        sil = G.offset(prof, dk)
        for sub in G.clip(sil, box, keep="inside"):
            out += _poly(sub, color=k_black, f=feed)

    # ---- reeds: every strand that meets the frame gets its tick ------------
    def reed(polys: Sequence[Poly], pen, lens=None, edges_=("top", "right", "left")):
        for n_, pl in enumerate(polys):
            L = 3.0 if lens is None else lens[n_]
            for r in G.clip(pl, box, keep="inside"):
                for e in (r[0], r[-1]):
                    if hal is not None and hal.contains(e[0] - 1.5 if e[0] > x1 - 2 else e[0], e[1]):
                        continue
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
    zmax_abs = max(Znorm) or 1.0
    reed(lane_polys, k_black, lens=[1.2 + 4.2 * z / zmax_abs for z in Znorm],
         edges_=("right", "bottom"))
    reed(v_polys, k_black, edges_=("left",))

    # ---- type ---------------------------------------------------------------
    out += giant_type("SUMS", x0 + 1.5, ty, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
    out += giant_type("TO ONE", x0 + 1.5, base_one, height=th, pen=k_black,
                      weight=1.9, tip=0.4, spaced=True, f=feed)
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
        (f"{n_q} Q · {n_k} K → {n_lane} Z    Σa = 1    a MAX {a_max:.3f}    "
         f"H {Hbits:.2f} / {math.log(n_k, 2):.2f} BITS", 1.9),
        (f"{n_k} EQUAL BINS OF {w_bin:.2f} MM    SLIT {2 * c:.1f} MM    "
         f"MIN PITCH {min_pitch:.2f} MM", 1.9),
        ("GOLD OVER GREEN WHERE a > 1/16", 1.9),
    ]
    for k, (txt, hh) in enumerate(lines):
        yy = fy - k * LEAD
        room = min(x_edge(yy + hh) - 5.0, x1 - 14.0) - (x0 + 2.0)
        s_txt = _spaced(txt)
        while _text_width(s_txt, hh) > room and hh > 1.4:
            hh -= 0.05
        out += _stroke_text(s_txt, x0 + 2.0, yy, hh, color=k_black, f=feed)

    for text, lx, ly, lh, pen in labels:
        out += _stroke_text(text, lx, ly, lh, color=pen, f=feed)

    k_bins = sorted(bin_of[j] for j in range(n_k))
    k_end_bins = []
    for j in range(n_k):
        ex_ = k_end_pt[j][0]
        k_end_bins.append(max(0, min(n_k - 1, int((ex_ - (ax - c)) // w_bin))))
    LAST_STATS.update(
        sum_a=sum(A), row_sum_err=row_sum_err, a_max=a_max, entropy_bits=Hbits,
        n_q=n_q, n_k=n_k, n_z=n_lane, nq_bin=list(nq_bin), Ag=[round(a, 4) for a in Ag],
        w_bin=w_bin, slit=2 * c,
        area_err=max(abs(h_area[g] - Ag[g] / sum(Ag)) for g in range(n_k)), hill_beta=hill_beta,
        prof_min=min(hy) * hscale, peak_med_bins=peak_med,
        k_end_in_own_bin=sum(1 for j in range(n_k) if k_end_bins[j] == bin_of[j]),
        k_bins_hit=len(set(k_end_bins)),
        slit_pitch=slit_pitch, lane_pitch=lane_pitch, lane_pitch_at=lane_pitch_at,
        kq_pitch=kq_pitch, vv_pitch=vv_pitch, vv_at=vv_at, qk_low=sorted(qk_where)[:6], kk_pitch=kk_pitch, min_pitch=min_pitch,
        qk_crossings=n_cross, qk_ang_min=min(qk_ang) if qk_ang else None,
        v_crossings=n_vx, v_flips=n_flip, flips=flips, v_merged_gaps=n_merge,
        gold_min_piece=min(gold_runs) if gold_runs else None,
        green_min_piece=min(green_runs) if green_runs else None, lane_merges=n_lane_merge,
        seriation_cost=seriation_cost, identity_cost=ident_cost, kq_slit=kq_slit,
        lay_score=lay_score, qid=qid,
        v_pairs_once=sum(1 for n_ in per_pair if n_ == 1), v_pairs=len(per_pair),
        v_angle_min=min(v_angles) if v_angles else None,
        v_angle_med=sorted(v_angles)[len(v_angles) // 2] if v_angles else None,
        vv_crossings=vv_x, lane_self_crossings=ll_x, kk_crossings=kk_x,
        slit_err=slit_err, short_bits=short_bits, edge_stubs=n_edge_stub, storm_merges=n_storm_merge, storm_min_piece=min(storm_runs) if storm_runs else None, lane_exit=lane_exit, q_stubs_dropped=n_stub, znorm=[round(z, 3) for z in Znorm], p_lane=p_lane,
        principal_x=principal_lane_x, ax=ax, lanes_x=[round(v, 2) for v in lanes_x],
        k_xs=[round(v, 2) for v in k_xs],
    )
    return out
