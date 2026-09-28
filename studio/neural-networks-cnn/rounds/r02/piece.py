"""CNN — ONE VALLEY (r02, thesis: one-valley / mechanism).

Every terrain on the sheet is the SAME forward pass of a real trained CNN
(Keras MobileNetV2, ImageNet weights) on ONE real photograph (the scikit-image
test cat "chelsea"). Nothing is noise:

    PIXELS   224x224  input luminance                        -> raster scanlines
    stride 4   56x56  ||block_2 output||  over 24 channels   -> unit-line mesh
    stride 8   28x28  ||block_5 output||  over 32 channels   -> unit-line mesh
    stride 16  14x14  ||block_12 output|| over 96 channels   -> unit-line mesh
    stride 32   7x7   ReLU(CAM - mean CAM) of the top-1 class (tiger cat, p 0.43):
                      the share of the class logit each location adds above average

Mapping, one line: HEIGHT is the activation, a MESH LINE is a row/column of
units (so line pitch is the layer's stride), CRIMSON is the one argmax unit of
the top map (its cell, as isolines) and, on every layer below, the second-moment
ellipse holding exactly half of that unit's gradient mass (its EFFECTIVE
receptive field, sum_c |d unit / d A_c|); dashed crimson rails join the ellipse
extremes layer to layer up to the unit's cell edges.

Lineage: Georg Nees, *Schotter* (c. 1968) -- order to disorder down the sheet.
Here the data supplies both ends: raster noise at the foot, one peak at the head.

The arrays come from ``compute_maps.py`` (torch, run once) and are cached in
``maps.npz`` beside this file. See NOTES.md for the checks.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np

from promptplot.generative.engine import HIDE, Scene3D
from promptplot.generative.engine.geometry import Rect, clip
from promptplot.generative.engine.kit import (
    _poly,
    _runs_from_cmds_pens,
    _spaced,
    _stroke_text,
    _text_width,
    even_contour_levels,
    giant_type,
)
from promptplot.generative.generators import _chain_segments, _marching_squares

HERE = Path(__file__).resolve().parent
BLACK, CRIMSON = 0, 1

# ---------------------------------------------------------------- the data
_D = np.load(HERE / "maps.npz")
LAYERS = [
    # key, activation map, ERF map, draw mode
    ("pix", _D["pix"], _D["g224"]),
    ("a56", _D["a56"], _D["g56"]),
    ("a28", _D["a28"], _D["g28"]),
    ("a14", _D["a14"], _D["g14"]),
    ("cam", _D["cam"], _D["g7"]),
]
ARGMAX = tuple(int(v) for v in _D["argmax"])  # (row, col) on the 7x7 map
TOP5 = _D["top5"]
LAST_STATS: dict = {}


# ------------------------------------------------------------ interpolation
def _cr(t):
    """Catmull-Rom weights for the 4 taps around a fractional position."""
    t2, t3 = t * t, t * t * t
    return (
        -0.5 * t3 + t2 - 0.5 * t,
        1.5 * t3 - 2.5 * t2 + 1.0,
        -1.5 * t3 + 2.0 * t2 + 0.5 * t,
        0.5 * t3 - 0.5 * t2,
    )


def sample(A: np.ndarray, u, v):
    """Bicubic (Catmull-Rom) sample of a unit grid at sheet-normalised (u, v);
    unit (r, c) sits at its CENTRE ((c+.5)/N, (r+.5)/N). Clamped edges."""
    N, M = A.shape
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    x = np.clip(u * M - 0.5, 0, M - 1)
    y = np.clip(v * N - 0.5, 0, N - 1)
    xi, yi = np.floor(x).astype(int), np.floor(y).astype(int)
    tx, ty = x - xi, y - yi
    wx, wy = _cr(tx), _cr(ty)
    out = np.zeros(np.broadcast(u, v).shape)
    for a in range(4):
        rr = np.clip(yi - 1 + a, 0, N - 1)
        for b in range(4):
            cc = np.clip(xi - 1 + b, 0, M - 1)
            out = out + wy[a] * wx[b] * A[rr, cc]
    return out


def norm01(A):
    A = np.asarray(A, dtype=float)
    lo, hi = float(A.min()), float(A.max())
    return (A - lo) / ((hi - lo) or 1.0)


def erf_ellipse(G: np.ndarray, frac: float = 0.5):
    """The effective receptive field as its SECOND-MOMENT ellipse, scaled so it
    encloses exactly ``frac`` of the |gradient| mass. Returns (mu, L, r, held)
    with points mu + r * L @ (cos t, sin t)."""
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


# ---------------------------------------------------------------- the plate
RASTER = 112  # every layer's z-buffer grid: 112 = 2*56 = 4*28 = 8*14 = 16*7

# composition (fractions of the drawable width W); one basis, footprints differ
KX, KY, DEPTH = 0.50, 0.58, 0.45       # depth -> paper (KX, KY) per mm; depth length = DEPTH * width
WIDTHS = [0.84, 0.70, 0.62, 0.58, 0.74]
LEFTS = [-0.04, 0.08, 0.18, 0.26, 0.28]
AMPS = [4.5, 6.0, 12.0, 20.0, 66.0]     # relief, mm
GAP = 6.0                               # clear air between layer silhouettes, mm
CONTOUR_MM, CONTOUR_FLOOR = 2.2, 0.06   # top-layer isolines: plan spacing, lowest level
ERF_LIFT = 2.5                          # mm of view depth the ERF ring floats above its terrain
CELL_OUTLINE = False                    # draw the argmax cell's draped border
MIN_RUN_MM = 1.2                        # debris floor: shorter black runs are dropped
SCAN_BAND = 7                           # input pixels averaged into one scanline


def cnn_one_valley(rng, bounds, colors: int = 2, feed: int = 2200):
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    scene = Scene3D(rng, bounds, feed=feed, fit="none", px=(460, 300))
    widths = [f * W for f in WIDTHS]
    amps = AMPS
    n = len(LAYERS)

    # ---- the terrain of each layer, on its own units
    pix = np.asarray(LAYERS[0][1], dtype=float)
    n_scan = pix.shape[0] // SCAN_BAND
    scan = norm01(pix.reshape(n_scan, SCAN_BAND, pix.shape[1]).mean(axis=1))  # 32 x 224
    Zs = [None] + [norm01(A) for (_, A, _) in LAYERS[1:-1]]
    # top: the CAM's excess over its own mean, ReLU'd -- the locations that pull
    # the class logit up more than an average location does (mean CAM + bias
    # IS the logit, so this is exactly the above-average share of the decision)
    cam = np.asarray(LAYERS[-1][1], dtype=float)
    ex = np.maximum(cam - cam.mean(), 0.0)
    Zs.append(ex / ex.max())

    def zs_(i, u, v):
        z = sample(Zs[i], u, v)
        return np.maximum(z, 0.0) if i == len(Zs) - 1 else z

    def zat(i, u, v):
        if i == 0:
            u, v = np.asarray(u, float), np.asarray(v, float)
            return scan[np.clip((v * n_scan).astype(int), 0, n_scan - 1),
                        np.clip((u * scan.shape[1]).astype(int), 0, scan.shape[1] - 1)]
        return zs_(i, u, v)

    def raster_grid(i):
        if i == 0:
            vs = (np.arange(n_scan) + 0.5) / n_scan
            us = (np.arange(scan.shape[1]) + 0.5) / scan.shape[1]
            uu, vv = np.meshgrid(us, vs)
            return uu, vv, scan
        # only the hull of the unit CENTRES: a mesh line is a row of units, so
        # nothing overhangs the first/last unit by the half-cell border
        h = RASTER // LAYERS[i][1].shape[0] // 2
        t = np.arange(h, RASTER - h + 1) / RASTER
        uu, vv = np.meshgrid(t, t)
        return uu, vv, zs_(i, uu, vv)

    # ---- world: layer i point = (ox_i + u L, (1-v) L DEPTH, oy_i + z amp_i);
    # paper = (X + KX D, KY D + Z); view depth = KX X - D + KY Z (larger = nearer)
    origins: List[Tuple[float, float]] = []

    def world(i, u, v, z):
        ox, oy = origins[i] if i < len(origins) else (0.0, 0.0)
        L = widths[i]
        return ox + u * L, (1.0 - v) * L * DEPTH, oy + z * amps[i]

    def to_paper(X, D, Z):
        return X + KX * D, KY * D + Z, KX * X - D + KY * Z

    # ---- stack placement: each layer sits GAP mm clear above the one below,
    # column by column on the real silhouettes (interlocks along the diagonal)
    xg = np.linspace(x0 - 40, x1 + 80, 600)
    prev_top = None
    for i in range(n):
        uu, vv, zz = raster_grid(i)
        L = widths[i]
        SX = x0 + LEFTS[i] * W + uu * L + KX * (1 - vv) * L * DEPTH
        SY = KY * (1 - vv) * L * DEPTH + zz * amps[i]
        idx = np.clip(np.searchsorted(xg, SX.ravel()), 0, len(xg) - 1)
        if prev_top is None:
            oy = y0 + 4.0 - float(SY.min())
        else:
            bot = np.full_like(xg, np.inf)
            np.minimum.at(bot, idx, SY.ravel())
            m = np.isfinite(bot) & np.isfinite(prev_top)
            oy = float(np.max(prev_top[m] - bot[m])) + GAP
        origins.append((x0 + LEFTS[i] * W, oy))
        top = np.full_like(xg, -np.inf)
        np.maximum.at(top, idx, SY.ravel() + oy)
        prev_top = np.where(np.isfinite(top), top, np.nan)

    def paper(i, u, v, z, lift=0.0):
        sx, sy, dp = to_paper(*world(i, u, v, z))
        return sx, sy, dp + lift

    def samples_on(i, us, vs, zs, pen, lift=0.0):
        sx, sy, dp = paper(i, us, vs, zs, lift)
        return [(float(a), float(b), float(c), pen) for a, b, c in zip(sx, sy, dp)]

    # ---- crimson anchors, computed up front: the ERF ellipse on every layer
    # below the top, the one argmax unit on the top
    stats: dict = {}
    ellipses, anchors = [], []
    for i, (key, A, G) in enumerate(LAYERS):
        if key == "cam":
            rr, cc = ARGMAX
            su, sv = (cc + 0.5) / 7, (rr + 0.5) / 7
            cu4 = np.array([cc / 7, (cc + 1) / 7, su, su])
            cv4 = np.array([sv, sv, rr / 7, (rr + 1) / 7])
            anchors.append([(float(a), float(b), float(zs_(i, a, b))) for a, b in zip(cu4, cv4)])
            ellipses.append(None)
            continue
        mu, Lc, r, held = erf_ellipse(G, 0.5)
        t = np.linspace(0, 2 * math.pi, 361)
        E = mu[:, None] + r * Lc @ np.stack([np.cos(t), np.sin(t)])
        eu, ev = np.clip(E[0], 0, 1), np.clip(E[1], 0, 1)
        ez = zat(i, eu, ev)
        ellipses.append((eu, ev, ez))
        k4 = [int(np.argmin(eu)), int(np.argmax(eu)), int(np.argmin(ev)), int(np.argmax(ev))]
        anchors.append([(float(eu[k]), float(ev[k]), float(ez[k])) for k in k4])
        stats[key] = dict(erf_mu=[round(float(x), 3) for x in mu], erf_r_sigma=round(r, 3), erf_mass_held=round(held, 3))

    # dashed rails between consecutive anchors, as world-interpolated samples
    DASH, PITCH = 2.0, 5.2

    def rail_dashes(i, k):
        a = np.array(world(i, *anchors[i][k]))
        b = np.array(world(i + 1, *anchors[i + 1][k]))
        pa, pb = to_paper(*a)[:2], to_paper(*b)[:2]
        seg = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
        m = max(1, int(seg / PITCH))
        dashes = []
        for j in range(m):
            t0 = (j + 0.5) / m - 0.5 * DASH / seg
            ts = np.linspace(t0, t0 + DASH / seg, 6)
            P = a[None, :] + ts[:, None] * (b - a)[None, :]
            sx, sy, dp = to_paper(P[:, 0], P[:, 1], P[:, 2])
            dashes.append([[float(x), float(y), float(d), CRIMSON] for x, y, d in zip(sx, sy, dp)])
        return dashes

    rails = {i: [rail_dashes(i, k) for k in range(4)] for i in range(n - 1)}

    # ---- draw, layer by layer, each against its own z-buffer
    for i, (key, A, G) in enumerate(LAYERS):
        uu, vv, zz = raster_grid(i)
        SX, SY, DEP = paper(i, uu, vv, zz)
        scene._rasterize(SX, SY, DEP)  # the engine's z-buffer, this layer only
        L = widths[i]

        if key == "pix":
            rows = [samples_on(i, uu[r], vv[r], zz[r], BLACK) for r in range(n_scan)]
            scene.lines(rows[::-1], mode="pause_resume", sep_mm=0.9, warmup=0, min_kept=3)
            stats[key].update(scanlines=n_scan, band_px=SCAN_BAND, pitch_mm=round(KY * L * DEPTH / n_scan, 2))
        else:
            N = A.shape[0]
            s = RASTER // N
            col_pitch = L / N * KY / math.hypot(KX, KY)
            row_pitch = KY * L * DEPTH / N
            cs = max(1, math.ceil(1.5 / col_pitch))
            rs = max(1, math.ceil(1.5 / row_pitch))
            # strided unit lines, both END units always included so no line
            # overhangs the last drawn line of the other family
            r_idx = np.unique(np.round(np.linspace(0, N - 1, math.ceil((N - 1) / rs) + 1)).astype(int))
            c_idx = np.unique(np.round(np.linspace(0, N - 1, math.ceil((N - 1) / cs) + 1)).astype(int))
            rows = [samples_on(i, uu[s * r], vv[s * r], zz[s * r], BLACK) for r in r_idx]
            cols = [samples_on(i, uu[:, s * c], vv[:, s * c], zz[:, s * c], BLACK) for c in c_idx]
            scene.lines(rows[::-1], mode="pause_resume", sep_mm=0.9, warmup=0, min_kept=3)
            scene.lines(cols, mode="pause_resume", sep_mm=0.9, warmup=0, min_kept=3)
            stats.setdefault(key, {}).update(N=N, row_stride=rs, col_stride=cs, rows_drawn=len(r_idx), cols_drawn=len(c_idx),
                                             row_pitch_mm=round(row_pitch * rs, 2), col_pitch_mm=round(col_pitch * cs, 2))

        if ellipses[i] is not None:
            eu, ev, ez = ellipses[i]
            scene.lines([samples_on(i, eu, ev, ez, CRIMSON, lift=ERF_LIFT)], mode="over")
        else:
            rr, cc = ARGMAX
            su, sv = (cc + 0.5) / 7, (rr + 0.5) / 7
            Zf = zz
            levels = [lv for lv in even_contour_levels(Zf.tolist(), spacing=CONTOUR_MM / (L / RASTER), cell=1.0)
                      if lv > CONTOUR_FLOOR]
            t1 = [float(x) for x in uu[0]]

            def in_cell(u, v):
                return (cc / 7 <= u <= (cc + 1) / 7) and (rr / 7 <= v <= (rr + 1) / 7)

            n_ring = 0
            for lv in levels:
                for ch in _chain_segments(_marching_squares(Zf.tolist(), t1, t1, lv)):
                    if len(ch) < 4:
                        continue
                    cu = np.array([p[0] for p in ch])
                    cv = np.array([p[1] for p in ch])
                    sx, sy, dp = paper(i, cu, cv, zs_(i, cu, cv), 0.4)
                    pens = [CRIMSON if in_cell(a, b) else BLACK for a, b in zip(cu, cv)]
                    n_ring += CRIMSON in pens
                    scene.lines([[(float(a), float(b), float(c), p) for a, b, c, p in zip(sx, sy, dp, pens)]], mode="over")
            # the one unit's cell, draped: the receptive field's apex
            tt = np.linspace(0, 1, 40)
            bu = np.concatenate([cc / 7 + tt / 7, np.full(40, (cc + 1) / 7), (cc + 1) / 7 - tt / 7, np.full(40, cc / 7)])
            bv = np.concatenate([np.full(40, rr / 7), rr / 7 + tt / 7, np.full(40, (rr + 1) / 7), (rr + 1) / 7 - tt / 7])
            if CELL_OUTLINE:
                scene.lines([samples_on(i, bu, bv, zs_(i, bu, bv), CRIMSON, lift=0.6)], mode="over")
            stats[key].update(levels=len(levels), crimson_rings=n_ring)

        # rails: the segment rising FROM this layer is tested against it now
        # (hidden where this layer's own ridges stand in front of it); the
        # segment arriving at this layer is drawn now against this layer's
        # buffer, keeping only samples that also passed the layer below.
        if i < n - 1:
            for dashes in rails[i]:
                for d in dashes:
                    for smp in d:
                        smp.append(scene.visible(smp[0], smp[1], smp[2]))
        if i > 0:
            for dashes in rails[i - 1]:
                for d in dashes:
                    scene.lines([[(x, y, dp if ok else HIDE, pen) for x, y, dp, pen, ok in d]], mode="over")

    # crop at the frame (exact, per stroke) and drop mesh debris; type is
    # added afterwards so no glyph stroke is ever mistaken for debris
    frame = Rect(x0, y0, x1, y1)
    final = []
    dropped = 0
    for pen, run in _runs_from_cmds_pens(scene.render()):
        for seg in clip(run, frame, keep="inside"):
            ln = sum(math.hypot(q[0] - p_[0], q[1] - p_[1]) for p_, q in zip(seg, seg[1:]))
            if pen == BLACK and ln < MIN_RUN_MM:
                dropped += 1
                continue
            final += _poly(seg, color=pen, f=feed)

    th = 6.0
    for k, word in enumerate(("FROM", "PIXELS", "TO", "MEANING")):
        final += giant_type(word, x0 + 1.0, y1 - 1.0 - th - k * 2.2 * th, th, pen=BLACK, weight=0.5, tip=0.5,
                            spaced=True, f=feed)
    cls = str(_D["class_name"]).replace("_", " ").upper()
    foot = f"MOBILENETV2 . IMAGENET . P({cls}) = {TOP5[0][1]:.2f}"
    final += _stroke_text(foot, x0 + 1.0, y1 - 1.0 - th - 3 * 2.2 * th - 9.0, 1.8, color=BLACK, f=feed)
    LAST_STATS.clear()
    LAST_STATS.update(stats, debris_dropped=dropped, origins=[(round(a, 1), round(b, 1)) for a, b in origins])
    return final
