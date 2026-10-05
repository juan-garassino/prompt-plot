"""CNN — ONE VALLEY, ONE MARK (r03, thesis: iterate · parent r02).

The same single forward pass as r02 (Keras MobileNetV2, ImageNet weights, on
the scikit-image cat "chelsea"; arrays cached in ``maps.npz`` by
``compute_maps.py``), redrawn under ONE rule, the Schotter rule:

    every map is drawn only as continuous horizontal hidden-line PROFILE ROWS,
    one row per map row, each row tested against its own layer's z-buffer.

Nothing else is black. Row count and row pitch carry the resolution by
themselves (224 -> 56 -> 28 -> 14 -> 7 rows of units); a row is stride-thinned
only where its flat paper pitch would fall under 1.0 mm. Roughness is the data.

    layer 0  224x224  input luminance (every 6th pixel row, 2-px means along it)
    layer 1   56x56   ||block_2 output||   (every 2nd unit row)
    layer 2   28x28   ||block_5 output||   (every unit row)
    layer 3   14x14   ||block_12 output||  (every unit row)
    layer 4    7x7    ReLU(CAM - mean CAM), top-1 class tiger_cat, p 0.43

Crimson is exactly five things: on each lower layer ONE closed loop, the
ellipse holding 50 % of the gradient mass of the argmax unit (4,3) (its
effective receptive field), occluded by that layer's own nearer relief; and on
the top layer the closed isolines of unit (4,3)'s own hill. Nothing crimson
sits between the layers; the funnel is the loops shrinking toward the summit.

One projection basis for all five planes (paper = X + KX*D, KY*D + Z); plane
widths shrink by a declared constant step; every plane is whole inside the
frame; the clear air between consecutive layers is one constant G.

Lineage: Georg Nees, *Schotter* (c. 1968): one element, one parameter.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple

import numpy as np

from promptplot.generative.engine import HIDE, Scene3D
from promptplot.generative.engine.kit import _poly, _runs_from_cmds_pens, _stroke_text, giant_type
from promptplot.generative.generators import _chain_segments, _marching_squares

HERE = Path(__file__).resolve().parent
BLACK, CRIMSON = 0, 1

# ---------------------------------------------------------------- the data
_D = np.load(HERE / "maps.npz")
LAYERS = [
    ("pix", _D["pix"], _D["g224"]),
    ("a56", _D["a56"], _D["g56"]),
    ("a28", _D["a28"], _D["g28"]),
    ("a14", _D["a14"], _D["g14"]),
    ("cam", _D["cam"], _D["g7"]),
]
ARGMAX = tuple(int(v) for v in _D["argmax"])  # (row, col) on the 7x7 map
TOP5 = _D["top5"]
LAST_STATS: dict = {}
HILL_P = 6.0  # p-norm of the unit-hill envelope (top layer)


def _cr(t):
    t2, t3 = t * t, t * t * t
    return (-0.5 * t3 + t2 - 0.5 * t, 1.5 * t3 - 2.5 * t2 + 1.0, -1.5 * t3 + 2.0 * t2 + 0.5 * t, 0.5 * t3 - 0.5 * t2)


def sample(A: np.ndarray, u, v):
    """Bicubic (Catmull-Rom) sample; unit (r, c) sits at ((c+.5)/N, (r+.5)/N)."""
    N, M = A.shape
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    x = np.clip(u * M - 0.5, 0, M - 1)
    y = np.clip(v * N - 0.5, 0, N - 1)
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int)
    wx, wy = _cr(x - xi), _cr(y - yi)
    out = np.zeros(np.broadcast(u, v).shape)
    for a in range(4):
        rr = np.clip(yi - 1 + a, 0, N - 1)
        for b in range(4):
            cc = np.clip(xi - 1 + b, 0, M - 1)
            out = out + wy[a] * wx[b] * A[rr, cc]
    return out


def unit_hills(A: np.ndarray, u, v, reach: float = 1.0, p: float = HILL_P):
    """The 7x7 CAM as 49 unit hills: each unit a cos^2 hill of its own value,
    radius ``reach`` cells; the terrain is their p-norm envelope (a max with
    rounded valleys). A hill never reaches past its neighbours' centres, so
    each row profile peaks at the 7 unit values of its row, and a level above
    ~half the argmax hill closes INSIDE that unit's own cell."""
    N = A.shape[0]
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    out = np.zeros(np.broadcast(u, v).shape)
    for r in range(N):
        for c in range(N):
            if A[r, c] <= 0:
                continue
            d = np.hypot(u * N - (c + 0.5), v * N - (r + 0.5)) / reach
            b = np.where(d < 1.0, np.cos(0.5 * math.pi * np.minimum(d, 1.0)) ** 2, 0.0)
            out = out + (A[r, c] * b) ** p
    return out ** (1.0 / p)


def norm01(A):
    A = np.asarray(A, dtype=float)
    lo, hi = float(A.min()), float(A.max())
    return (A - lo) / ((hi - lo) or 1.0)


def erf_ellipse(G: np.ndarray, frac: float = 0.5):
    """Second-moment ellipse of |gradient| mass, scaled to hold ``frac`` of it."""
    G = np.asarray(G, dtype=float)
    n = G.shape[0]
    w = G / G.sum()
    c = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(c, c)
    mu = np.array([(w * U).sum(), (w * V).sum()])
    dU, dV = U - mu[0], V - mu[1]
    C = np.array([[(w * dU * dU).sum(), (w * dU * dV).sum()], [(w * dU * dV).sum(), (w * dV * dV).sum()]])
    Lc = np.linalg.cholesky(C)
    Ci = np.linalg.inv(C)
    m = Ci[0, 0] * dU * dU + 2 * Ci[0, 1] * dU * dV + Ci[1, 1] * dV * dV
    lo, hi = 0.05, 4.0
    for _ in range(40):
        r = 0.5 * (lo + hi)
        if w[m <= r * r].sum() < frac:
            lo = r
        else:
            hi = r
    r = 0.5 * (lo + hi)
    return mu, Lc, r, float(w[m <= r * r].sum())


def rdp(pts, tol):
    """Douglas-Peucker: drop vertices within ``tol`` mm of the chord."""
    if len(pts) < 3:
        return list(pts)
    P = np.asarray(pts, dtype=float)
    keep = np.zeros(len(P), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(P) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        seg = P[b] - P[a]
        n = math.hypot(*seg) or 1e-12
        d = np.abs(seg[0] * (P[a + 1:b, 1] - P[a, 1]) - seg[1] * (P[a + 1:b, 0] - P[a, 0])) / n
        k = int(np.argmax(d))
        if d[k] > tol:
            keep[a + 1 + k] = True
            stack += [(a, a + 1 + k), (a + 1 + k, b)]
    return [tuple(p) for p in P[keep]]


def order_runs(runs):
    """Greedy nearest-neighbour ordering of one pen's runs, reversing a run
    when its far end is nearer (runs are open polylines; closed loops too)."""
    left = [list(r) for r in runs]
    out, cur = [], (0.0, 0.0)
    while left:
        best, bi, rev = 1e18, 0, False
        for k, r in enumerate(left):
            d0 = (r[0][0] - cur[0]) ** 2 + (r[0][1] - cur[1]) ** 2
            d1 = (r[-1][0] - cur[0]) ** 2 + (r[-1][1] - cur[1]) ** 2
            if d0 < best:
                best, bi, rev = d0, k, False
            if d1 < best:
                best, bi, rev = d1, k, True
        r = left.pop(bi)
        if rev:
            r = r[::-1]
        out.append(r)
        cur = r[-1]
    return out


def _layer_ink(cmds):
    """black runs of one layer: count, median length, share of ink in runs >= 10 mm."""
    ls = [run_len(r) for pen, r in _runs_from_cmds_pens(cmds) if pen == BLACK]
    ls = [x for x in ls if x >= MIN_RUN]
    if not ls:
        return {}
    tot = sum(ls)
    return dict(runs=len(ls), median_mm=round(float(np.median(ls)), 1),
                ink_m=round(tot / 1000, 2), share_ge10mm=round(sum(x for x in ls if x >= 10) / tot, 2))


def run_len(run):
    return sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(run, run[1:]))


def erf_area_fraction(G: np.ndarray, frac: float = 0.5, n: int = 400) -> float:
    """Share of the map's area inside the 50 % ERF ellipse (clipped to the map)."""
    mu, Lc, r, _ = erf_ellipse(G, frac)
    c = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(c, c)
    Ci = np.linalg.inv(Lc @ Lc.T)
    dU, dV = U - mu[0], V - mu[1]
    m = Ci[0, 0] * dU * dU + 2 * Ci[0, 1] * dU * dV + Ci[1, 1] * dV * dV
    return float((m <= r * r).mean())


ERF_AREA = [erf_area_fraction(_D[k]) for k in ("g224", "g56", "g28", "g14")]
ERF_AREA_PCT = int(round(100 * ERF_AREA[0]))

# ---------------------------------------------------------------- the plate
KX, KY, DEPTH = 0.50, 0.58, 0.45   # the ONE basis: depth -> paper (KX, KY) per mm; depth = DEPTH * width
INSET = 5.0                         # every edge this far inside the drawable frame
L_BOTTOM, L_STEP = 146.0, 11.5      # plane widths: 146, 134.5, 123, 111.5, 100 mm (constant step)
AMPS = [2.0, 3.0, 9.0, 16.0, 68.0]  # relief, mm
MIN_PITCH = 1.0                     # flat row pitch floor, mm
PX_BAND = 2                         # input pixels averaged ALONG a row (0.65 mm px -> 1.3 mm samples)
U_PER_UNIT = [None, 2, 3, 6, 16]    # bicubic samples per unit along a row
GAP_MIN = 10.0                      # minimum constant clear air between layers
SUMMIT_TOP_MAX = 3.0                # summit sits this far under the INSET line (and above)
CAP_STEP_MM = 3.6                   # summit isolines: height step on paper
ERF_LIFT = 0.8                      # mm of relief the ERF loop rides above the local crest
MIN_RUN = 3.0                       # no ink run shorter than this, mm
RDP_TOL = 0.04                      # vertex thinning tolerance, mm
TYPE_X = INSET                      # the one flush-left type axis (offset from x0)


def cnn_one_valley_rows(rng, bounds, colors: int = 2, feed: int = 2200):
    x0, y0, x1, y1 = bounds
    fx0, fy0, fx1, fy1 = x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET
    n = len(LAYERS)
    widths = [L_BOTTOM - L_STEP * i for i in range(n)]

    # ---------------- per-layer terrain field z(u, v) in [0, 1] and its rows
    pix = np.asarray(LAYERS[0][1], dtype=float)
    pixn = norm01(pix)
    cam = np.asarray(LAYERS[-1][1], dtype=float)
    ex = np.maximum(cam - cam.mean(), 0.0)
    camn = ex / ex.max()
    fields = [pixn] + [norm01(A) for (_, A, _) in LAYERS[1:-1]] + [camn]

    def zfun(i, u, v):
        if i == 0:
            u, v = np.asarray(u, float), np.asarray(v, float)
            c = np.clip((u * 224).astype(int), 0, 223)
            r = np.clip((v * 224).astype(int), 0, 223)
            return pixn[r, c]
        if i == n - 1:
            return unit_hills(camn, u, v)
        return sample(fields[i], u, v)

    rows_of: List[np.ndarray] = []   # v of each drawn row
    us_of: List[np.ndarray] = []     # u samples along a row
    stride_of = []
    for i, (key, A, _) in enumerate(LAYERS):
        N = A.shape[0]
        L = widths[i]
        pitch = KY * L * DEPTH / N
        s = max(1, math.ceil(MIN_PITCH / pitch))
        r_idx = np.arange(0, N, s)
        # centre the kept rows in the map (symmetric margin of skipped rows)
        r_idx = r_idx + (N - 1 - r_idx[-1]) // 2
        rows_of.append((r_idx + 0.5) / N)
        stride_of.append(s)
        if i == 0:
            us_of.append((np.arange(0, 224, PX_BAND) + PX_BAND / 2) / 224)
        else:
            k = U_PER_UNIT[i]
            us_of.append(np.linspace(0.5 / N, 1 - 0.5 / N, (N - 1) * k + 1))

    def row_z(i, v):
        """Height along row v. Input rows are 2-px means of the real pixel row."""
        if i == 0:
            r = int(round(v * 224 - 0.5))
            row = pixn[r]
            return row.reshape(-1, PX_BAND).mean(axis=1)
        return zfun(i, us_of[i], np.full_like(us_of[i], v))

    # ---------------- world <-> paper, one basis
    origins: List[Tuple[float, float]] = [(0.0, 0.0)] * n

    def paper(i, u, v, z, lift=0.0):
        ox, oy = origins[i]
        L = widths[i]
        X = ox + np.asarray(u) * L
        D = (1.0 - np.asarray(v)) * L * DEPTH
        Z = oy + np.asarray(z) * AMPS[i] + lift
        return X + KX * D, KY * D + Z, KX * X - D + KY * Z

    # left edges: the stack is right-flush on the frame's inner line, so the
    # diagonal is carried by the left edges stepping in
    for i in range(n):
        L = widths[i]
        N = LAYERS[i][1].shape[0]
        u_hi = us_of[i][-1]
        v_lo = rows_of[i][0]
        ox = fx1 - (u_hi * L + KX * (1 - v_lo) * L * DEPTH)
        origins[i] = (ox, 0.0)

    # silhouettes over x at oy = 0, from every drawn row + the ERF loop crest
    xg = np.linspace(x0 - 20, x1 + 20, 900)

    def envelope(i):
        top = np.full_like(xg, -np.inf)
        bot = np.full_like(xg, np.inf)
        for v in rows_of[i]:
            sx, sy, _ = paper(i, us_of[i], np.full_like(us_of[i], v), row_z(i, v))
            xi = np.interp(xg, sx, sy, left=np.nan, right=np.nan)
            m = np.isfinite(xi)
            top[m] = np.maximum(top[m], xi[m])
            bot[m] = np.minimum(bot[m], xi[m])
        return top, bot

    envs = [envelope(i) for i in range(n)]

    def stack(G):
        oys = [fy0 - float(np.nanmin(np.where(np.isfinite(envs[0][1]), envs[0][1], np.nan)))]
        for i in range(1, n):
            pt = envs[i - 1][0] + oys[i - 1]
            bb = envs[i][1]
            m = np.isfinite(pt) & np.isfinite(bb)
            oys.append(float(np.max(pt[m] - bb[m])) + G)
        return oys

    # the gap G: the largest constant clear air that still puts the summit
    # inside the frame (bisection); never below GAP_MIN
    top_of = lambda oys: float(np.nanmax(np.where(np.isfinite(envs[-1][0]), envs[-1][0], np.nan))) + oys[-1]
    lo, hi = 0.0, 60.0
    for _ in range(40):
        g = 0.5 * (lo + hi)
        if top_of(stack(g)) <= fy1 - SUMMIT_TOP_MAX:
            lo = g
        else:
            hi = g
    G = lo
    oys = stack(G)
    origins = [(origins[i][0], oys[i]) for i in range(n)]

    stats: dict = dict(gap_mm=round(G, 2), widths=widths,
                       origins=[(round(a, 1), round(b, 1)) for a, b in origins])

    scene = Scene3D(rng, bounds, feed=feed, fit="none", px=(700, 420))

    def samples(i, us, vs, zs, pen, lift=0.0):
        sx, sy, dp = paper(i, us, vs, zs, lift)
        return [(float(a), float(b), float(c), pen) for a, b, c in zip(sx, sy, dp)]

    layer_marks = []
    rr4, cc4 = ARGMAX
    cap_levels: List[float] = []
    for i, (key, A, G_) in enumerate(LAYERS):
        N = A.shape[0]
        us = us_of[i]
        mark = len(scene.out)
        layer_marks.append(mark)
        # ---- this layer's own z-buffer: the surface through its drawn rows
        # (the top layer: its full unit-hill field, so the summit hides what
        # is behind it between rows too)
        if i == n - 1:
            vv_ = np.linspace(rows_of[i][0], rows_of[i][-1], 97)
        else:
            vv_ = rows_of[i]
        UU, VV = np.meshgrid(us, vv_)
        if i == 0:
            ZZ = np.stack([row_z(0, v) for v in vv_])
        else:
            ZZ = zfun(i, UU, VV)
        SX, SY, DEP = paper(i, UU, VV, ZZ)
        scene._rasterize(SX, SY, DEP)

        # ---- the cap (top layer): unit (4,3)'s own closed isolines
        cap_mask = None
        if i == n - 1:
            su, sv = (cc4 + 0.5) / N, (rr4 + 0.5) / N
            # closed inside the cell iff above every other hill at the cell
            # boundary; with cos^2 hills of reach 1 cell that is 1/2 of the peak
            t = np.linspace(0, 1, 400)
            bu = np.concatenate([cc4 + t, np.full(400, cc4 + 1.0), cc4 + t, np.full(400, float(cc4))]) / N
            bv = np.concatenate([np.full(400, float(rr4)), rr4 + t, np.full(400, rr4 + 1.0), rr4 + t]) / N
            lam0 = float(zfun(i, bu, bv).max())
            dz = CAP_STEP_MM / AMPS[i]
            cap_levels = list(np.arange(lam0 + 0.02, 0.985, dz))
            # fine local grid over the cell for marching squares
            g = np.linspace(0, 1, 121)
            cu_ = (cc4 + g) / N
            cv_ = (rr4 + g) / N
            CU, CV = np.meshgrid(cu_, cv_)
            CZ = zfun(i, CU, CV)
            n_loops = 0
            for lv in cap_levels:
                for ch in _chain_segments(_marching_squares(CZ.tolist(), list(cu_), list(cv_), lv)):
                    if len(ch) < 6:
                        continue
                    closed = math.hypot(ch[0][0] - ch[-1][0], ch[0][1] - ch[-1][1]) < 1e-6
                    if not closed:
                        ch = ch + [ch[0]]
                    cu = np.array([p[0] for p in ch])
                    cv = np.array([p[1] for p in ch])
                    scene.lines([samples(i, cu, cv, np.full_like(cu, lv), CRIMSON, lift=0.0)], mode="over")
                    n_loops += 1
            cap_lo = cap_levels[0] if cap_levels else 1.0

            def in_cap(u, v):
                inside_cell = (u >= cc4 / N) & (u <= (cc4 + 1) / N) & (v >= rr4 / N) & (v <= (rr4 + 1) / N)
                return inside_cell & (zfun(i, u, v) >= cap_lo)

            cap_mask = in_cap
            stats["cap"] = dict(boundary_max=round(lam0, 3), levels=len(cap_levels), loops=n_loops,
                                level_lo=round(cap_lo, 3), cell=[rr4, cc4])

        # ---- the rows: front row first so it owns the space (pause-resume)
        lines = []
        for v in rows_of[i][::-1]:
            vs = np.full_like(us, v)
            zs = row_z(i, v)
            smp = samples(i, us, vs, zs, BLACK)
            if cap_mask is not None:
                m = cap_mask(us, vs)
                smp = [(a, b, HIDE if mk else c, p) for (a, b, c, p), mk in zip(smp, m)]
            lines.append(smp)
        scene.lines(lines, mode="pause_resume", sep_mm=0.8, warmup=0, min_kept=3)
        stats[key] = dict(N=N, row_stride=stride_of[i], rows=len(rows_of[i]),
                          pitch_mm=round(KY * widths[i] * DEPTH / N * stride_of[i], 2),
                          samples_per_row=len(us))

        if i == n - 1:
            stats[key]["ink"] = _layer_ink(scene.out[mark:])
        # ---- the ERF loop (lower layers): one closed ellipse holding 50 % of
        # d unit(4,3) / d layer mass, riding the local crest, occluded by
        # this layer's nearer relief
        if i < n - 1:
            mu, Lc, r, held = erf_ellipse(G_, 0.5)
            t = np.linspace(0, 2 * math.pi, 721)
            E = mu[:, None] + r * Lc @ np.stack([np.cos(t), np.sin(t)])
            eu, ev = np.clip(E[0], 0, 1), np.clip(E[1], 0, 1)
            # crest height: the max of the drawn surface within ~one drawn row
            # pitch around the loop, then smoothed along the loop
            rad = max(1.5 / N * stride_of[i], 0.012)
            zc = np.zeros_like(eu)
            for k, (a, b) in enumerate(zip(eu, ev)):
                ang = np.linspace(0, 2 * math.pi, 12, endpoint=False)
                pu = np.clip(np.concatenate([[a], a + rad * np.cos(ang), a + 0.5 * rad * np.cos(ang)]), 0, 1)
                pv = np.clip(np.concatenate([[b], b + rad * np.sin(ang), b + 0.5 * rad * np.sin(ang)]), 0, 1)
                zc[k] = float(np.max(zfun(i, pu, pv)))
            ker = np.ones(31) / 31.0
            zc = np.convolve(np.concatenate([zc[-15:], zc, zc[:15]]), ker, mode="same")[15:-15]
            scene.lines([samples(i, eu, ev, zc, CRIMSON, lift=ERF_LIFT)], mode="over")
            stats[key]["ink"] = _layer_ink(scene.out[mark:])
            stats[key].update(erf_mu=[round(float(x), 3) for x in mu], erf_r_sigma=round(r, 3),
                              erf_mass_held=round(held, 3))

    # measured clear air between consecutive layers' INK (column envelopes)
    layer_marks.append(len(scene.out))
    xs = np.linspace(x0, x1, 1901)

    def ink_env(cmds):
        top = np.full_like(xs, -np.inf)
        bot = np.full_like(xs, np.inf)
        for _, run in _runs_from_cmds_pens(cmds):
            if run_len(run) < MIN_RUN:
                continue
            for (ax, ay), (bx, by) in zip(run, run[1:]):
                lo_, hi_ = min(ax, bx), max(ax, bx)
                m = (xs >= lo_) & (xs <= hi_)
                if not m.any():
                    continue
                t = (xs[m] - ax) / ((bx - ax) or 1e-9)
                yy = ay + np.clip(t, 0, 1) * (by - ay)
                top[m] = np.maximum(top[m], yy)
                bot[m] = np.minimum(bot[m], yy)
        return top, bot

    envs_ink = [ink_env(scene.out[layer_marks[k]:layer_marks[k + 1]]) for k in range(n)]
    gaps = []
    for k in range(1, n):
        d = envs_ink[k][1] - envs_ink[k - 1][0]
        d = d[np.isfinite(d)]
        gaps.append(round(float(d.min()), 1) if d.size else None)
    stats["ink_gaps_mm"] = gaps

    # ---------------- clean-up: frame check, no run under MIN_RUN, thin vertices
    final = []
    dropped = {BLACK: 0, CRIMSON: 0}
    by_pen: dict = {BLACK: [], CRIMSON: []}
    for pen, run in _runs_from_cmds_pens(scene.render()):
        if run_len(run) < MIN_RUN:
            dropped[pen] = dropped.get(pen, 0) + 1
            continue
        by_pen[pen].append(rdp(run, RDP_TOL))
    for pen in (BLACK, CRIMSON):
        for run in order_runs(by_pen[pen]):
            final += _poly(run, color=pen, f=feed)
    stats["runs"] = {pen: len(v) for pen, v in by_pen.items()}
    stats["shortest_run_mm"] = round(min(run_len(r) for v in by_pen.values() for r in v), 2)

    # ---------------- type: one flush-left axis at x0 + INSET
    tx = x0 + TYPE_X
    th = 6.0
    TW = 0.8  # title stroke band: 2 passes 0.8 mm apart, band centred on the glyph path
    cap_top = y1 - 6.0 - TW / 2  # INK top 6 mm under the top margin
    base0 = cap_top - th
    for k, word in enumerate(("FROM", "PIXELS", "TO", "MEANING")):
        final += giant_type(word, tx + TW / 2, base0 - k * 2.2 * th, th, pen=BLACK, weight=TW, tip=TW,
                            spaced=True, f=feed)
    ch = 1.5
    cls = str(_D["class_name"]).replace("_", " ").upper()
    lines_txt = [
        "224²  56²  28²  14²  7²:  CAM − MEAN, CLIPPED AT 0",
        "CRIMSON: 50% OF ∂CAM(4,3) GRADIENT MASS",
        f"~{ERF_AREA_PCT}% OF IMAGE VS CELL 1/49    P({cls}) = {TOP5[0][1]:.2f}",
    ]
    yb = base0 - 3 * 2.2 * th - 9.0
    for k, s in enumerate(lines_txt):
        final += _stroke_text(s, tx, yb - k * 2.4 * ch, ch, color=BLACK, f=feed)

    LAST_STATS.clear()
    LAST_STATS.update(stats, dropped_short=dropped, caption_baseline=round(yb, 1))
    return final
