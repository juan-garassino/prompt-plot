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
    """Elliptic coordinates about a slit of half-width ``c`` centred at (ax, ay),
    with a REED COMB near the slit (r09, S9).

    The plain map is (ax + c cosh(phi) cos(psi), ay + c sinh(phi) sin(psi)). r09
    replaces cosh(phi) in x by g(phi) = 1 + B(phi) (cosh(phi) - 1), where B is 0
    for phi <= phi0, a smoothstep up to 1 at phi1, and 1 beyond. For phi <= phi0
    every streamline is therefore exactly VERTICAL at its own slit x; beyond
    phi1 the storm is the untouched r07 field. The level sets of phi are
    ellipses with semi-axes (c g(phi), c sinh(phi)), both non-decreasing in
    phi, so they are nested: the map stays injective and NO two strands can
    cross because of the comb (every storm crossing is the one r07 had)."""

    def __init__(self, ax: float, ay: float, c: float, phi0: float = 0.0, phi1: float = 0.0):
        self.ax, self.ay, self.c = ax, ay, c
        self.phi0, self.phi1 = phi0, phi1

    def g(self, phi: float) -> float:
        ch = math.cosh(phi)
        if self.phi1 <= self.phi0 or phi >= self.phi1:
            return ch
        if phi <= self.phi0:
            return 1.0
        t = (phi - self.phi0) / (self.phi1 - self.phi0)
        b = t * t * t * (10.0 - 15.0 * t + 6.0 * t * t)       # C2 smootherstep
        return 1.0 + b * (ch - 1.0)

    def pt(self, phi: float, psi: float) -> Tuple[float, float]:
        return (
            self.ax + self.c * self.g(phi) * math.cos(psi),
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
V_LEAD_Y, V_LEAD_XA, V_LEAD_K1, V_LEAD_K2 = 84.0, 98.0, 16.0, 12.0   # §5 lead-in
V_OUT_Y, V_OUT_K1, V_OUT_K2 = 50.0, 4.0, 4.0                            # §5 lead-out
# ---- r09: the fan-shell (encoding Revision 1.1 §5), sheet mm relative to (x0, y0)
FAN_O_REL = (-166.0, 117.0)        # O = (-156, 127) on the 24x30 sheet
FAN_AXIS_DEG, FAN_DTH = -2.0, 1.0 / 68.5
FAN_R0, FAN_R1, FAN_S = 300.0, 308.0, 4.8      # virtual reed, pick 1, pick spacing
# the drain: a band of parallels (see NOTES: the encoding's lane-0 waypoint and
# 'pitch never decreases' cannot both hold; the band keeps pitch >= 2.1 mm)
DRAIN_DEG, DRAIN_XQ, DRAIN_P = -66.0, 92.0, 2.10
DRAIN_RT0, DRAIN_RT21 = 12.0, 3.0
POST_FILLET, TICK_LEN = 1.5, 3.4               # outer-corner fillet; 1/16 tick to x ~133.75
BOLD_PITCH = 0.25                         # the principal thread: 2 passes, registered
TYPE_WEIGHT = 2.0
# r09: the reed comb (S9) — every strand vertical for phi <= COMB_PHI0
COMB_PHI0, COMB_PHI1 = 0.95, 1.85


# ---------------------------------------------------------------------------
# r07 additions
# ---------------------------------------------------------------------------
def _histopolate_pinned(nb: int, weights, step: float, beta: float, pin: bool = True):
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
    for i in ((0, M - 1) if pin else ()):      # r07 pinned the cut edges to 0
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
    """Revision 1.1 A1: FREE ends. The hill's ends float at the data's own
    floor (a_min is not zero, so neither is the curve), area exact per bin."""
    tot = float(sum(weights))
    for beta in (0.25, 0.15, 0.12, 0.08, 0.0):
        xs, hs, ar = _histopolate_pinned(len(weights), weights, 1.0 / 16.0, beta, pin=False)
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
    ap = Aperture(ax=ax, ay=ay, c=c, phi0=COMB_PHI0, phi1=COMB_PHI1)
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

    # r09 (Revision 1.1 A2, §4d): with the reed comb every K arrives VERTICAL,
    # so its landing x IS its slit x. The landing must sit inside its own bin
    # (>= 0.25 mm from the never-drawn bin edges), >= K_LANE mm from every lane
    # slot, and on the SAME side of the 1/16 level as its bin mean, by a
    # margin a straightedge cannot misread (>= 1.5 mm for the four bins above
    # 1/16, >= 0.6 mm for the other twelve). Among those: maximum lane
    # clearance, then nearest the bin centre.
    K_LANE = 0.92
    level_y = ay + tick_h

    def _hill_at(x: float) -> float:
        return float(np.interp(x, cv[:, 0], cv[:, 1]))

    ktg = []
    k_slit = []
    k_margin = []
    k_relaxed: List[int] = []
    for g in range(n_k):
        cen = 0.5 * (edges[g] + edges[g + 1])
        above = Ag[g] > UNIF
        need = 1.5 if above else 0.6
        best = None
        # other seeds: if no point meets the straightedge margin, the margin
        # is relaxed (stated in LAST_STATS['k_relaxed']), never the bin
        for need_ in (need, 0.0, -99.0):
            for xs_ in np.linspace(edges[g] + 0.25, edges[g + 1] - 0.25, 276):
                cl = min(abs(xs_ - lx) for lx in lanes_x)
                if cl < K_LANE:
                    continue
                m_ = _hill_at(float(xs_)) - level_y
                if (m_ if above else -m_) < need_:
                    continue
                key = (round(min(cl, 0.5 * PITCH), 3), -abs(xs_ - cen))
                if best is None or key > best[0]:
                    best = (key, float(xs_), m_)
            if best is not None:
                if need_ != need:
                    k_relaxed.append(g)
                break
        if best is None:
            raise RuntimeError(f'no K landing for bin {g} [{edges[g]:.2f},{edges[g+1]:.2f}]')
        land = _landing(best[1])
        if land is None:
            raise RuntimeError(f'K in bin {g} never clears the hill')
        (lx_, ly_), ph, ps = land
        ktg.append((lx_, ly_, ph, ps))
        k_slit.append(best[1])
        k_margin.append(round(best[2], 2))
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
    # BELOW THE WALL (Revision 1.1 A3) — a Deco FAN-SHELL. In the cloth every
    # lane is an exact RAY of one centre O and every pick an exact ARC about
    # O: weft is orthogonal to warp at all 352 crossings by construction.
    # ======================================================================
    FO = np.array([x0 + FAN_O_REL[0], y0 + FAN_O_REL[1]])
    th_k = [math.radians(FAN_AXIS_DEG) + (k - (n_q - 1) / 2.0) * FAN_DTH for k in range(n_q)]
    e_k = [np.array([math.cos(t_), math.sin(t_)]) for t_ in th_k]
    nrm_k = [np.array([-e_[1], e_[0]]) for e_ in e_k]          # +theta side (toward lane 21)
    R_pick = [FAN_R1 + FAN_S * g for g in range(16)]

    def _ray_pt(k: int, R: float) -> np.ndarray:
        return FO + R * e_k[k]

    def _lint(p, d_, q, e_):
        M_ = np.array([d_, -e_]).T
        t_, _ = np.linalg.solve(M_, q - p)
        return p + t_ * d_

    def _fillet(I, d1, d2, r, ds=0.2):
        """Circular fillet of radius r turning from direction d1 onto d2 at the
        corner I: (in-tangent point, out-tangent point, points)."""
        a1 = math.atan2(d1[1], d1[0])
        a2 = math.atan2(d2[1], d2[0])
        D = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
        tt = r * math.tan(abs(D) / 2.0)
        Tin = I - tt * d1
        n_ = max(3, int(abs(D) * r / ds) + 1)
        sg = 1.0 if D > 0 else -1.0
        pts_ = [Tin + sg * r * np.array([math.sin(a1 + D * u) - math.sin(a1),
                                         -math.cos(a1 + D * u) + math.cos(a1)])
                for u in np.linspace(0.0, 1.0, n_)]
        return Tin, I + tt * d2, np.asarray(pts_)

    # ---- the drain: each lane leaves the slit vertical, bends onto a band of
    # parallels heading DRAIN_DEG (pitch DRAIN_P), then one fillet onto its own
    # ray, tangent at the virtual reed R = FAN_R0. The band is the only way to
    # keep lane 0 out of the A21 crop and still >= 2 mm pitch (see NOTES).
    Hd = math.radians(DRAIN_DEG)
    dH = np.array([math.cos(Hd), math.sin(Hd)])
    nH = np.array([-dH[1], dH[0]])
    c0 = float(nH @ np.array([DRAIN_XQ, 150.0]))
    down = np.array([0.0, -1.0])
    lane_polys: List[Poly] = []
    drain_r = []
    for k in range(n_q):
        P0 = (c0 + DRAIN_P * k) * nH
        J = _lint(np.array([lanes_x[k], ay]), down, P0, dH)
        Dtop = Hd + math.pi / 2.0
        rmax = max(0.3, (ay - 1.0 - J[1]) / math.tan(Dtop / 2.0))
        rt = min(DRAIN_RT0 + (DRAIN_RT21 - DRAIN_RT0) * k / (n_q - 1), rmax)
        _, T2, A1 = _fillet(J, down, dH, rt)
        I = _lint(P0, dH, FO, e_k[k])
        RI = float((I - FO) @ e_k[k])
        Dbot = th_k[k] - Hd
        rb = (FAN_R0 - RI) / math.tan(Dbot / 2.0)
        T3, _, A2 = _fillet(I, dH, e_k[k], rb)
        # the ray, from the virtual reed to beyond the right frame
        Rx = (x1 + 2.0 - FO[0]) / e_k[k][0]
        ray = [tuple(_ray_pt(k, R_)) for R_ in np.linspace(FAN_R0, Rx, 40)]
        pl = [(lanes_x[k], ay - 0.8)] + [tuple(p_) for p_ in A1] + [tuple(p_) for p_ in A2] + ray[1:]
        lane_polys.append(_resample(pl, 0.4))
        drain_r.append((round(rt, 2), round(rb, 2), round(float((T3 - T2) @ dH), 1)))
    slit_err = max(abs(lane_polys[t][0][0] - lanes_x[t]) for t in range(n_q))

    # ---- the weft: lead-in, 16 arcs, 15 semicircle turns, lead-out ---------
    TR = FAN_S / 2.0                       # ONE turn radius: half the pick spacing
    e0, e21 = e_k[0], e_k[-1]
    n0_out = -nrm_k[0]                     # outside lane 0 (the -theta side)
    n21_out = nrm_k[-1]                    # outside lane 21 (the +theta side)
    weft_parts: List[Tuple[str, int, np.ndarray]] = []

    def _arc_pts(R_: float, ta: float, tb: float) -> np.ndarray:
        n_ = max(8, int(abs(tb - ta) * R_ / 0.2) + 1)
        tt = np.linspace(ta, tb, n_)
        return np.c_[FO[0] + R_ * np.cos(tt), FO[1] + R_ * np.sin(tt)]

    def _semi(C, e_, n_out, sweep: float) -> np.ndarray:
        ph = np.linspace(0.0, sweep, max(12, int(sweep * TR / 0.15) + 1))
        return np.asarray([C + TR * (-math.cos(p_) * e_ + math.sin(p_) * n_out) for p_ in ph])

    yL = V_LEAD_Y
    T0 = _ray_pt(0, FAN_R0) + TR * n0_out
    T0b = _ray_pt(0, R_pick[0] - TR) + TR * n0_out
    lead = [(x0, yL), (V_LEAD_XA, yL)]
    lead += _cubic((V_LEAD_XA, yL), (V_LEAD_XA + V_LEAD_K1, yL),
                   tuple(T0 - V_LEAD_K2 * e0), tuple(T0), 120)[1:]
    lead += [tuple(T0b)]
    Cq = _ray_pt(0, R_pick[0] - TR)
    quarter = [tuple(Cq + TR * (math.cos(p_) * n0_out + math.sin(p_) * e0))
               for p_ in np.linspace(0.0, math.pi / 2.0, 16)]
    weft_parts.append(("lead", -1, np.asarray(_resample(lead, 0.25)[:-1] + quarter)))
    for g in range(16):
        ta, tb = (th_k[0], th_k[-1]) if g % 2 == 0 else (th_k[-1], th_k[0])
        weft_parts.append(("pick", g, _arc_pts(R_pick[g], ta, tb)))
        if g < 15:
            if g % 2 == 0:
                weft_parts.append(("turn", g, _semi(_ray_pt(n_q - 1, R_pick[g] + TR), e21, n21_out, math.pi)))
            else:
                weft_parts.append(("turn", g, _semi(_ray_pt(0, R_pick[g] + TR), e0, n0_out, math.pi)))
    q_out = _semi(_ray_pt(0, R_pick[15] + TR), e0, n0_out, math.pi / 2.0)
    q_end = q_out[-1]
    yR = V_OUT_Y
    tail = _cubic(tuple(q_end), tuple(q_end + V_OUT_K1 * e0), (x1 - V_OUT_K2, yR), (x1, yR), 60)
    weft_parts.append(("lead", 99, np.vstack([q_out, np.asarray(tail[1:])])))
    weft: Poly = []
    part_rng = []
    for kind, g, P_ in weft_parts:
        pts_ = [tuple(map(float, p_)) for p_ in P_]
        if weft and math.hypot(weft[-1][0] - pts_[0][0], weft[-1][1] - pts_[0][1]) < 1e-6:
            pts_ = pts_[1:]
            a_ = len(weft) - 1
        else:
            a_ = len(weft)
        weft.extend(pts_)
        part_rng.append((kind, g, a_, len(weft)))
    s_w = _arclen(weft)
    pick_s0 = {g: s_w[a_] for kind, g, a_, b_ in part_rng if kind == "pick"}

    # ---- over/under: gold over green  <=>  a_ij > 1/16, all 352, NO MERGE --
    R_U = 0.9                              # gold under-gap radius
    R_G = 1.1                              # green gap under gold
    R_GB = 1.25                            # ... around the bold lane
    R_UB = 1.0                             # under the bold lane: gap 2.0 mm (§11.2 cap)
    gold_gaps: List[Tuple[float, float]] = []
    lane_marks: List[list] = [[] for _ in range(n_q)]
    B_drawn = [[None] * n_k for _ in range(n_q)]
    n_over = 0
    for g in range(16):
        j = korder[g]
        ta = th_k[0] if g % 2 == 0 else th_k[-1]
        for k in range(n_q):
            over = A_all[qid[k]][j] > UNIF
            B_drawn[qid[k]][g] = over
            p_ = _ray_pt(k, R_pick[g])
            s_ = pick_s0[g] + R_pick[g] * abs(th_k[k] - ta)
            if over:
                n_over += 1
                lane_marks[k].append((float(p_[0]), float(p_[1]), True))
            else:
                r_ = R_UB if k == p_lane else R_U
                gold_gaps.append((s_ - r_, s_ + r_))
    gold_gaps.sort()
    rule_ok = sum(1 for i in range(n_q) for g in range(16)
                  if B_drawn[i][g] == (A_all[i][korder[g]] > UNIF))
    cross_ang: List[float] = []
    for g in range(16):
        arc_ = [tuple(p_) for p_ in _arc_pts(R_pick[g], th_k[0] - 0.01, th_k[-1] + 0.01)]
        for k in range(n_q):
            cross_ang += [a_ for _, _, a_ in _crossings_ang(arc_, lane_polys[k])]
    # every non-pick part of the weft (leads, turns) must cross NO lane; its
    # ends touch the selvage exactly where a pick begins, so hits within
    # 0.3 mm of a pick end are the pick's own crossing
    pick_ends = np.asarray([_ray_pt(k, R_) for R_ in R_pick for k in (0, n_q - 1)])
    weft_lane_x = 0
    for kind, g, a_, b_ in part_rng:
        if kind == "pick":
            continue
        part = weft[a_:b_]
        for k in range(n_q):
            for hx_, hy_, _ in _crossings_ang(part, lane_polys[k]):
                if np.min(np.hypot(pick_ends[:, 0] - hx_, pick_ends[:, 1] - hy_)) > 0.3:
                    weft_lane_x += 1
    lane_lane_x = sum(len(_crossings_ang(lane_polys[k], lane_polys[k + 1])) for k in range(n_q - 1))
    gold_pieces = _split_by_gaps(weft, gold_gaps)
    gold_len = [_arclen(p)[-1] for p in gold_pieces]
    # visibility per pick, between lane 0 and lane 21, and the longest hidden run
    vis_pick = []
    hid_max = 0.0
    for g in range(16):
        L_ = R_pick[g] * abs(th_k[-1] - th_k[0])
        s_a = pick_s0[g]
        hid = sum(max(0.0, min(b_, s_a + L_) - max(a_, s_a)) for a_, b_ in gold_gaps)
        vis_pick.append(round(1.0 - hid / L_, 3))
        hid_max = max([hid_max] + [b_ - a_ for a_, b_ in gold_gaps])

    # green: a gap wherever gold is over (never merged)
    lane_gaps = []
    for k in range(n_q):
        gk, _nm = _merged_gaps(lane_polys[k], lane_marks[k], R_GB if k == p_lane else R_G, 0.0)
        lane_gaps.append(gk)
    green_pieces = [_split_by_gaps(lane_polys[k], lane_gaps[k]) for k in range(n_q)]

    # ---- measured spacings --------------------------------------------------
    lane_pitch = 1e9
    lane_pitch_at = None
    for k in range(n_q - 1):
        pa = [p for p in lane_polys[k] if x0 < p[0] < x1 and y0 < p[1] < ay - 0.9]
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
    L0 = np.asarray(lane_polys[0])
    m150 = (L0[:, 1] > 100) & (L0[:, 1] < 150)
    lane0_x_min_void = float(L0[m150, 0].min())
    # gold clearance from lanes it does not cross (turns + leads away from crossings)
    xpts = np.asarray([_ray_pt(k, R_pick[g]) for g in range(16) for k in range(n_q)])
    far = [p for p in weft if np.min(np.hypot(xpts[:, 0] - p[0], xpts[:, 1] - p[1])) > 2.5]
    gold_lane_clear = min(float(_near_dist(far, lane_polys[k]).min()) for k in range(n_q))
    lead_in_clear = float(_near_dist([p for p in weft_parts[0][2][:-16].tolist()], lane_polys[0]).min())
    apex_up = [float((_ray_pt(n_q - 1, R_pick[g] + TR) + TR * n21_out - FO) @ n21_out - (0.0))
               for g in range(0, 15, 2)]
    exits = [float(np.interp(x1, [p[0] for p in lane_polys[k]], [p[1] for p in lane_polys[k]]))
             for k in range(n_q)]

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

    # black: the wall, broken by the slit, TURNING UP at each cut edge into a
    # POST (Revision 1.1 A1). One stroke per pass: frame -> wall -> 1.5 mm outer
    # fillet -> post -> square top at the 1/16 level. The posts' inner ink edges
    # are the slit (52.0 mm); the right post's top runs on as the 1/16 tick.
    WALL_O = [-0.62, -0.31, 0.0, 0.31, 0.62]
    NIB_B = 0.25                                   # half the 0.5 black nib
    RC = POST_FILLET - WALL_O[-1]                  # centre-line fillet radius
    level = ay + tick_h
    PxL = ax - c - NIB_B - WALL_O[-1]
    PxR = 2.0 * ax - PxL

    def _arm(o: float, x_frame: float) -> Poly:
        """Left-arm pass at offset o (o > 0 = the inner-corner side)."""
        cxy = (PxL - RC, ay + RC)
        rr = RC - o
        pts_: Poly = [(x_frame, ay + o), (cxy[0], ay + o)]
        pts_ += [(cxy[0] + rr * math.cos(a_), cxy[1] + rr * math.sin(a_))
                 for a_ in np.linspace(-math.pi / 2.0, 0.0, 14)[1:]]
        pts_ += [(PxL - o, level)]
        return pts_

    arms_L = [_arm(o, x0 + 0.4) for o in WALL_O]
    arms_R = [[(2.0 * ax - px, py) for px, py in _arm(o, 2.0 * ax - (x1 - 0.4))] for o in WALL_O]
    for k, pl in enumerate(arms_L):
        out += _poly(pl if k % 2 == 0 else list(reversed(pl)), color=k_black, f=feed)
    # black: the hill, 5 passes centred on the exact-area curve, butting the
    # posts' inner ink edges (no overlap)
    hill_box = G.Rect(ax - c + NIB_B, ay - 1.0, ax + c - NIB_B, ay + ZMAX + 5.0)
    for k in range(5):
        dk = -HILL_HALF + 2 * HILL_HALF * k / 4.0
        sil = G.offset(curve, dk)
        for sub in G.clip(sil, hill_box, keep="inside"):
            out += _poly(sub if k % 2 == 0 else list(reversed(sub)), color=k_black, f=feed)
    # right post + the 1/16 tick + the right arm
    out += _poly([(PxR + TICK_LEN, level), (PxR, level)], color=k_black, f=feed)
    for k, pl in enumerate(arms_R):
        out += _poly(list(reversed(pl)) if k % 2 == 0 else pl, color=k_black, f=feed)
    post_ink = (round(PxL - WALL_O[-1] - NIB_B, 2), round(PxL + WALL_O[-1] + NIB_B, 2),
                round(PxR - WALL_O[-1] - NIB_B, 2), round(PxR + WALL_O[-1] + NIB_B, 2))
    post_regions = [G.Rect(post_ink[0], ay - 1.0, post_ink[1], level + NIB_B),
                    G.Rect(post_ink[2], ay - 1.0, post_ink[3], level + NIB_B)]

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
        (f"{n_q} Q · {n_k} K → {n_q} Z WARPS × {n_k} V PICKS   Σa = 1   a MAX {a_max:.3f}   "
         f"H {Hbits:.2f} / {math.log(n_k, 2):.2f} BITS", 2.0, False),
        (f"SLIT {SLIT:.0f} MM · {n_k} EQUAL BINS · LANES EQUAL PITCH {PITCH:.2f} MM, ORDER ONLY · "
         f"a MIN {min(A):.3f} - NO KEY GETS ZERO", 2.0, False),
        (f"BOLD = QUERY {principal}, ITS ROW IS THE HILL · GOLD OVER GREEN WHERE a > 1/16 "
         f"({n_over_all} / {n_q * n_k}) · POSTS = 1/16", 2.0, False),
    ]
    LEAD = 5.0
    fy = y0 + 19.5
    footer_h = []
    for k, (txt, hh, sp) in enumerate(lines):
        yy = fy - k * LEAD
        s_txt = _spaced(txt) if sp else txt
        room = W - 4.0
        while _text_width(s_txt, hh) > room and hh > 1.4:
            hh -= 0.05
        footer_h.append((round(hh, 2), round(_text_width(s_txt, hh), 1)))
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
    # S9, measured on the DRAWN crimson: the lowest end of each strand, its
    # offset from its own lane slot, and how long it is vertical before it
    q_end_dx, q_vert = [], []
    for t in range(n_q):
        runs_t = q_strands[t]
        low = min(runs_t, key=lambda r_: min(r_[0][1], r_[-1][1]))
        pl = low if low[-1][1] < low[0][1] else list(reversed(low))
        q_end_dx.append(round(pl[-1][0] - lanes_x[t], 3))
        vlen = 0.0
        for a_, b_ in zip(reversed(pl[:-1]), reversed(pl[1:])):
            if abs(a_[0] - lanes_x[t]) > 0.05:
                break
            vlen += math.hypot(b_[0] - a_[0], b_[1] - a_[1])
        q_vert.append(round(vlen, 2))
    k_end_dx = [round(k_end_pt[j][0] - k_slit[bin_of[j]], 3) for j in range(n_k)]
    # paper between any storm strand and the post ink (centre distance - half nibs)
    post_clear = 1e9
    for strands_ in (q_strands, k_strands):
        for runs_ in strands_:
            for r_ in runs_:
                for px_, py_ in _resample(r_, 0.3):
                    if py_ > level + 8.0:
                        continue
                    for (xa_, xb_) in ((post_ink[0], post_ink[1]), (post_ink[2], post_ink[3])):
                        dx_ = max(xa_ - px_, 0.0, px_ - xb_)
                        dy_ = max(0.0, py_ - (level + NIB_B))
                        post_clear = min(post_clear, math.hypot(dx_, dy_) - 0.15)
    hill_ends = (hy[0] * hscale, hy[-1] * hscale)
    k_hill_margin = {g: k_margin[g] for g in range(n_k)}
    LAST_STATS.update(
        sum_a=sum(A), row_sum_err=row_sum_err, a_max=a_max, a_min=min(A), entropy_bits=Hbits, temp=TEMP,
        korder=korder, Ag=[round(a, 4) for a in Ag], above_bins=above_bins,
        slit=SLIT, w_bin=w_bin, lanes_x=[round(v, 2) for v in lanes_x], qid=qid,
        seriation_cost=_cost(qid), identity_cost=_cost(list(range(n_q))),
        area_err=max(abs(h_area[g] - Ag[g] / sum(Ag)) for g in range(n_k)), hill_beta=hill_beta,
        hill_end_heights=hill_ends, post_top_minus_end=(tick_h - hill_ends[0], tick_h - hill_ends[1]),
        summit_x=summit_x, peak=max(hy) * hscale, peak_med=peak_med, tick_h=tick_h, level_y=level,
        post_ink=post_ink, slit_ink=post_ink[2] - post_ink[1],
        k_x=[round(v, 2) for v in k_slit], k_off=k_off, k_relaxed=k_relaxed, k_hill_margin=k_hill_margin,
        k_lane_clear=k_lane_clear, k_end_dx_max=max(abs(v) for v in k_end_dx),
        k_end_in_own_bin=sum(1 for j in range(n_k) if k_end_bins[j] == bin_of[j]),
        n_nudge=n_nudge, kq_pitch=kq_pitch, kq_at=kq_at, kk_crossings=kk_x, qk_crossings=n_cross,
        qk_ang_min=min(qk_ang) if qk_ang else None, qk_low=qk_low,
        storm_merges=n_storm_merge, storm_min=min(storm_runs), q_stubs=n_stub, edge_stubs=n_edge_stub,
        q_end_dx=q_end_dx, q_end_dx_max=max(abs(v) for v in q_end_dx), q_vert_min=min(q_vert),
        q0_end=None, post_clear=post_clear,
        slit_err=slit_err, lane_pitch=lane_pitch, lane_pitch_at=lane_pitch_at, drain_r=drain_r,
        lane0_x_min_void=lane0_x_min_void, exits=(round(exits[0], 2), round(exits[-1], 2)),
        exit_pitch_min=min(b_ - a_ for a_, b_ in zip(exits, exits[1:])), exit11=round(exits[p_lane], 2),
        lane_lane_x=lane_lane_x,
        pick_pitch=(R_pick[0] * FAN_DTH, R_pick[-1] * FAN_DTH),
        pick1=(tuple(np.round(_ray_pt(0, R_pick[0]), 1)), tuple(np.round(_ray_pt(n_q - 1, R_pick[0]), 1))),
        pick16=(tuple(np.round(_ray_pt(0, R_pick[15]), 1)), tuple(np.round(_ray_pt(n_q - 1, R_pick[15]), 1))),
        cross_ang_min=min(cross_ang), n_cross_cloth=len(cross_ang), weft_lane_x=weft_lane_x,
        rule_ok=rule_ok, n_over=n_over, n_over_all=n_over_all,
        bold_under_picks=[g + 1 for g in range(16) if not B_drawn[principal][g]],
        bold_over_picks=[g + 1 for g in range(16) if B_drawn[principal][g]],
        gold_min=min(gold_len), gold_pieces=len(gold_len), gold_runs_min=min(gold_runs),
        gold_draw=sum(gold_runs), vis_pick_min=min(vis_pick), vis_pick=vis_pick, hidden_run_max=hid_max,
        green_min=min(green_runs), gold_lane_clear=gold_lane_clear, lead_in_clear=lead_in_clear,
        mouth_min=mouth_min, lead_in_y=yL, lead_out_y=yR, weft_len=s_w[-1], footer=footer_h,
    )
    return out
