"""CNN — ONE VALLEY, ONE MARK, ONE SUMMIT (r04, thesis: iterate · parent r03).

The same single forward pass as r02/r03 (Keras MobileNetV2, ImageNet weights,
on the scikit-image cat "chelsea", centre-crop 300² -> bicubic 224²; arrays
cached in ``maps.npz`` by ``compute_maps.py``, NOT re-run), drawn under ONE
rule, the Schotter rule:

    every map is drawn only as continuous horizontal hidden-line PROFILE ROWS,
    each row tested against its own layer's z-buffer.

    plane 0  224x224  input luminance    38 rows (every 6th pixel row)
    plane 1   56x56   ||block_2||        28 rows (every 2nd unit row)
    plane 2   28x28   ||block_5||        19 rows (every 1.5 unit rows, bicubic)
    plane 3   14x14   ||block_12||       14 rows (every unit row)
    plane 4    7x7    CAM - mean CAM      7 rows (every unit row, SIGNED)

Row count falls strictly and flat pitch rises strictly up the stack; relief
rises on a declared monotone progression (RELIEF), and the CAM is drawn at the
largest height scale at which all 13 CAM cells >= 20 % of the peak still show
their own crest ON THE SHEET (the real top-plane drawing is re-run inside the
sweep and each crest is looked for in the kept ink).

r04 rebuilds the HEAD (7x7 CAM): bicubic like every other map (no per-unit
hills), signed about its mean (no flat clipped rows), the summit isolines are
closed level sets of the DRAWN field around unit (4,3) above the level where
they would swallow the runner-up (3,3), drawn visible-only. The four 50 %-ERF
loops lie on their own surfaces and are hidden (with 0.8 mm clear) wherever a
nearer ridge of the same map rises in front of them.

One projection basis for all five planes: paper = (X + KX*D, KY*D + Z),
D = DEPTH * width. r04 opens KY (0.58 -> 0.66) uniformly on every plane: the
lower summit freed vertical space, and the extra depth pitch is what raises
the CAM visibility bound.

Front edge of every plane = the image's BOTTOM edge (image row 223 / unit row 6).

Type: one flush-left axis at the input plane's front-left corner (x = 17.75):
single-pass title top-left, 3-line caption under the input plane.
Plot order: pen 0 black (maps nearest-neighbour, then title, then caption),
pen 1 crimson (4 ERF loops + summit rings).

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
CAM = np.asarray(_D["cam"], dtype=float)
CAM_MEAN = float(CAM.mean())
CAMC = CAM - CAM_MEAN                 # the drawn quantity, CAM units, signed
STRONG = CAMC >= 0.2 * CAMC.max()     # the 13 cells the science mandate names
LAST_STATS: dict = {}


def _cr(t):
    t2, t3 = t * t, t * t * t
    return (-0.5 * t3 + t2 - 0.5 * t, 1.5 * t3 - 2.5 * t2 + 1.0, -1.5 * t3 + 2.0 * t2 + 0.5 * t, 0.5 * t3 - 0.5 * t2)


def sample(A: np.ndarray, u, v):
    """Bicubic (Catmull-Rom) sample; unit (r, c) sits at ((c+.5)/N, (r+.5)/N).
    Catmull-Rom interpolates: the drawn value AT a unit centre is the unit's value."""
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


def erf_area_fraction(G: np.ndarray, frac: float = 0.5, n: int = 400) -> float:
    """Share of the map's area inside the 50 % ERF ellipse (clipped to the map)."""
    mu, Lc, r, _ = erf_ellipse(G, frac)
    c = (np.arange(n) + 0.5) / n
    U, V = np.meshgrid(c, c)
    Ci = np.linalg.inv(Lc @ Lc.T)
    dU, dV = U - mu[0], V - mu[1]
    m = Ci[0, 0] * dU * dU + 2 * Ci[0, 1] * dU * dV + Ci[1, 1] * dV * dV
    return float((m <= r * r).mean())


def rdp(pts, tol):
    """Douglas-Peucker: drop vertices within ``tol`` mm of the chord."""
    if len(pts) < 3:
        return list(pts)
    P = np.asarray(pts, dtype=float)
    keep = np.zeros(len(P), dtype=bool)
    keep[0] = keep[-1] = True
    if math.hypot(*(P[-1] - P[0])) < 1e-6:
        # closed ring: the chord is degenerate, so split at the farthest vertex
        far = int(np.argmax(np.hypot(*(P - P[0]).T)))
        keep[far] = True
        stack = [(0, far), (far, len(P) - 1)]
    else:
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


def order_runs(runs, start=(0.0, 0.0)):
    """Greedy nearest-neighbour ordering of one pen's runs (with reversal)."""
    left = [list(r) for r in runs]
    out, cur = [], start
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


def run_len(run):
    return sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(run, run[1:]))


def densify(run, step=0.25):
    out = [run[0]]
    for p, q in zip(run, run[1:]):
        n = max(1, int(math.hypot(q[0] - p[0], q[1] - p[1]) / step))
        for k in range(1, n + 1):
            t = k / n
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return np.asarray(out)


def seg_dist(P, run):
    """min distance from point P to a polyline."""
    A = np.asarray(run[:-1], float)
    B = np.asarray(run[1:], float)
    AB = B - A
    L2 = np.maximum((AB ** 2).sum(1), 1e-12)
    t = np.clip(((P - A) * AB).sum(1) / L2, 0, 1)
    Q = A + AB * t[:, None]
    return float(np.sqrt(((Q - P) ** 2).sum(1)).min())


def flood(mask, seed):
    """4-connected component of ``mask`` containing ``seed`` (no scipy):
    vectorised dilation until it stops growing."""
    comp = np.zeros_like(mask, dtype=bool)
    if not mask[seed]:
        return comp
    comp[seed] = True
    while True:
        g = comp.copy()
        g[1:, :] |= comp[:-1, :]
        g[:-1, :] |= comp[1:, :]
        g[:, 1:] |= comp[:, :-1]
        g[:, :-1] |= comp[:, 1:]
        g &= mask
        if g.sum() == comp.sum():
            return g
        comp = g


def join_runs(runs, tol=0.05):
    """Join runs whose endpoints meet (a closed ring broken at its seam)."""
    runs = [list(r) for r in runs]
    changed = True
    while changed:
        changed = False
        for i in range(len(runs)):
            for j in range(len(runs)):
                if i == j:
                    continue
                a, b = runs[i], runs[j]
                if math.hypot(a[-1][0] - b[0][0], a[-1][1] - b[0][1]) < tol:
                    runs[i] = a + b[1:]
                    del runs[j]
                    changed = True
                    break
            if changed:
                break
    return runs


def parallel_pairs(runs, dmax=0.8, cos_min=0.93, step=0.2):
    """Closest same-pen PARALLEL approach between DIFFERENT runs (mm), and the
    ink length (mm) that sits parallel closer than ``dmax`` to another run."""
    pts, dirs, owner = [], [], []
    for k, r in enumerate(runs):
        P = densify(r, step)
        if len(P) < 2:
            continue
        d = np.gradient(P, axis=0)
        n = np.hypot(d[:, 0], d[:, 1])
        n[n == 0] = 1
        pts.append(P)
        dirs.append(d / n[:, None])
        owner.append(np.full(len(P), k))
    if not pts:
        return float("inf"), 0.0
    P, Dn, O = np.concatenate(pts), np.concatenate(dirs), np.concatenate(owner)
    best, close = np.full(len(P), np.inf), np.zeros(len(P), bool)
    for a in range(0, len(P), 1500):
        sl = slice(a, a + 1500)
        d = np.sqrt(((P[sl, None, :] - P[None, :, :]) ** 2).sum(2))
        cs = np.abs((Dn[sl, None, :] * Dn[None, :, :]).sum(2))
        m = (O[sl, None] != O[None, :]) & (cs > cos_min)
        d = np.where(m, d, np.inf)
        best[sl] = d.min(1)
    close = best < dmax
    return float(best.min()), float(close.sum() * step)


ERF_AREA = [erf_area_fraction(_D[k]) for k in ("g224", "g56", "g28", "g14")]
ERF_AREA_PCT = int(round(100 * ERF_AREA[0]))

# ---------------------------------------------------------------- the plate
KX, KY, DEPTH = 0.50, 0.66, 0.45    # the ONE basis: paper = (X + KX*D, KY*D + Z), D = DEPTH * width
INSET = 5.0                          # every edge this far inside the drawable frame
WIDTHS = [146.0, 134.5, 123.0, 111.5, 100.0]   # constant 11.5 mm step (r03)
STRIDES = [6, 2, 1.5, 1, 1]          # rows 38 / 28 / 19 / 14 / 7
RELIEF = [3.0, 3.2, 7.0, 9.6]        # mm per unit of the normalised map, planes 0-3 (monotone)
PX_BAND = 2                          # input pixels averaged ALONG a row
U_PER_UNIT = [None, 2, 3, 6, 16]     # bicubic samples per unit along a row
ZB_SUB = [1, 3, 3, 3, None]          # z-buffer sub-rows per drawn row (top: dense 97)
SUMMIT_TOP_MAX = 3.0                 # top ink this far under the INSET line
SCALE_SAFETY = 0.98                  # drawn CAM scale = SAFETY x largest passing scale
RING_SEP = 1.1                       # summit isolines: min paper spacing on the front/flank rays (mm)
CRIMSON_CLEAR = 1.0                  # black stops this far from crimson on the top plane
ERF_LIFT = (0.4, 0.4, 0.25, 0.25)    # mm the ERF loop rides above its surface
ERF_ON_SURFACE = (False, False, True, True)   # 28²/14²: loop ON the bicubic surface
ERF_GAP = 0.8                        # occlusion break: clear paper each side (mm)
ERF_HID_MIN = 0.6                    # a hidden stretch shorter than this is grazing noise
MIN_RUN = 3.0                        # no ink run shorter than this, mm
MIN_RUN_TOP = 4.0                    # top plane: no fragment shorter than this, mm
RDP_TOL = 0.04
PX = (900, 520)                      # z-buffer raster per plane
CAP_H, CAP_PITCH, CAP_DESC = 1.5, 3.6, 0.2    # caption: cap height, line pitch, comma descender (mm)
CAP_BAND = CAP_DESC + 2 * CAP_PITCH + CAP_H + 8.0  # caption block + 8 mm air under the input plane
TITLE_LEAD = 2.1                      # title leading, x cap height
CREST_TOL = 0.3                      # a crest is "shown" if kept ink passes this close


def row_positions(N, s):
    if float(s).is_integer():
        idx = np.arange(0, N, int(s)).astype(float)
        idx = idx + (N - 1 - idx[-1]) // 2
    else:
        idx = np.arange(0, N - 1 + 1e-9, s)
        idx = idx + ((N - 1) - idx[-1]) / 2
    return idx


# ---------------------------------------------------------------- the head
_N7 = 7
_RR, _CC = ARGMAX
_G = np.linspace(-1.0, 2.0, 121)
_CU = (_CC + _G) / _N7
_CV = (_RR + _G) / _N7
_CUU, _CVV = np.meshgrid(_CU, _CV)
_CZ = sample(CAMC, _CUU, _CVV)
_SEED = (int(np.argmin(np.abs(_CV - (_RR + 0.5) / _N7))), int(np.argmin(np.abs(_CU - (_CC + 0.5) / _N7))))


def _summit_floor():
    """Lowest level whose component about (4,3) holds NO other unit centre."""
    others = [(int(np.argmin(np.abs(_CV - (r + 0.5) / _N7))), int(np.argmin(np.abs(_CU - (c + 0.5) / _N7))))
              for r in range(_N7) for c in range(_N7)
              if (r, c) != ARGMAX and abs(r - _RR) <= 1 and abs(c - _CC) <= 1]
    def clean(lam):
        comp = flood(_CZ >= lam, _SEED)
        edge = comp[0, :].any() or comp[-1, :].any() or comp[:, 0].any() or comp[:, -1].any()
        return not (edge or any(comp[o] for o in others))

    lo, hi = 0.0, float(CAMC.max()) - 0.05     # clean(hi) holds, clean(lo) fails
    for _ in range(30):
        m = 0.5 * (lo + hi)
        if clean(m):
            hi = m
        else:
            lo = m
    lam0 = hi
    return float(lam0)


SUMMIT_FLOOR = _summit_floor() + 0.05       # first level strictly above the (3,3) merge
_COMP_LO = flood(_CZ >= SUMMIT_FLOOR, _SEED)


def ring_levels(s, L):
    """Summit levels, from SUMMIT_FLOOR up: each next level is the lowest one
    whose front, left and right crossings (rays from the peak) all sit at least
    RING_SEP mm on paper from the previous ring's. Spacing is a paper fact, not
    a fixed level step (the slopes differ ~3x between the flanks and the front)."""
    N = _N7
    pu, pv = (_CC + 0.5) / N, (_RR + 0.5) / N
    t = np.linspace(0, 1.0 / N, 400)
    rays = [(pu + 0 * t, pv + t), (pu - t, pv + 0 * t), (pu + t, pv + 0 * t)]   # front, left, right

    def crossings(lv):
        out = []
        for ru, rv in rays:
            z = sample(CAMC, ru, rv)
            k = int(np.argmax(z < lv)) if (z < lv).any() else len(z) - 1
            u, v = ru[k], rv[k]
            d = (1 - v) * L * DEPTH
            out.append(np.array([u * L + KX * d, KY * d + s * lv]))
        return out

    levels = [SUMMIT_FLOOR]
    prev = crossings(SUMMIT_FLOOR)
    for lv in np.arange(SUMMIT_FLOOR + 0.02, CAMC.max() - 0.15, 0.02):
        cur = crossings(lv)
        if all(np.hypot(*(a - b)) >= RING_SEP for a, b in zip(cur, prev)):
            levels.append(float(lv))
            prev = cur
    return levels


def top_plane(scene, s, ox, oy, L):
    """Draw the 7x7 CAM plane at height scale ``s`` (mm per CAM unit) with its
    origin at (ox, oy). Returns (black_runs, crimson_runs, info) of the KEPT ink."""
    N = _N7
    us = np.linspace(0.5 / N, 1 - 0.5 / N, (N - 1) * U_PER_UNIT[4] + 1)
    rows_v = (np.arange(N) + 0.5) / N

    def P(u, v, z, lift=0.0):
        u, v, z = np.asarray(u, float), np.asarray(v, float), np.asarray(z, float)
        d = (1 - v) * L * DEPTH
        X = ox + u * L
        Z = oy + s * z + lift
        return X + KX * d, KY * d + Z, KX * X - d + KY * Z

    vv = np.linspace(rows_v[0], rows_v[-1], 49)
    UU, VV = np.meshgrid(us, vv)
    SX, SY, DP = P(UU, VV, sample(CAMC, UU, VV))
    scene._rasterize(SX, SY, DP)
    start = len(scene.out)

    # ---- the summit: closed level sets of the DRAWN field about unit (4,3),
    #      outermost first; visible-only; pause-resume (0.8 mm) silences the
    #      inner rings' back arcs where the back slope foreshortens them together
    levels = ring_levels(s, L)
    ring_runs = []
    for lv in levels:
        comp = flood(_CZ >= lv, _SEED)
        Zm = np.where(comp, _CZ, np.minimum(_CZ, lv - 1e-3))
        for ch in _chain_segments(_marching_squares(Zm.tolist(), list(_CU), list(_CV), lv)):
            if len(ch) < 6:
                continue
            if math.hypot(ch[0][0] - ch[-1][0], ch[0][1] - ch[-1][1]) > 1e-6:
                ch = ch + [ch[0]]
            cu = np.array([p[0] for p in ch])
            cv = np.array([p[1] for p in ch])
            # start each ring at its FRONT-most point so a back break never splits the front arc
            k0 = int(np.argmax(cv))
            cu = np.concatenate([cu[k0:-1], cu[:k0 + 1]])
            cv = np.concatenate([cv[k0:-1], cv[:k0 + 1]])
            a, b, c = P(cu, cv, np.full_like(cu, lv), lift=0.05)
            ring_runs.append([(float(x), float(y), float(d), CRIMSON) for x, y, d in zip(a, b, c)])
    scene.lines(ring_runs, mode="pause_resume", sep_mm=0.8, warmup=0, min_kept=3)
    rings0 = join_runs([r for pen, r in _runs_from_cmds_pens(scene.out[start:]) if pen == CRIMSON])
    del scene.out[start:]
    crim_pts = np.concatenate([densify(r) for r in rings0]) if rings0 else np.zeros((0, 2))

    # ---- the 7 rows, front first, one shared occupancy. Rows at or in front
    #      of the peak row stop inside the lowest ring and CRIMSON_CLEAR short
    #      of crimson; rows BEHIND the peak keep their ink (crimson yields below)
    occ = scene.occupancy(0.8)
    black, back_black = [], []
    for r_ in range(N - 1, -1, -1):
        v = rows_v[r_]
        vs = np.full_like(us, v)
        a, b, c = P(us, vs, sample(CAMC, us, vs))
        hide = np.zeros(len(us), bool)
        if r_ >= _RR:
            iu = np.clip(np.searchsorted(_CU, us), 0, len(_CU) - 1)
            iv = np.clip(np.searchsorted(_CV, vs), 0, len(_CV) - 1)
            hide = (us >= _CU[0]) & (us <= _CU[-1]) & (vs >= _CV[0]) & (vs <= _CV[-1]) & _COMP_LO[iv, iu]
            if len(crim_pts):
                dd = np.sqrt(((np.stack([a, b], 1)[:, None, :] - crim_pts[None, :, :]) ** 2).sum(2)).min(1)
                hide = hide | (dd < CRIMSON_CLEAR)
        mk = len(scene.out)
        scene.lines([[(float(x), float(y), HIDE if h else float(d), BLACK) for x, y, d, h in zip(a, b, c, hide)]],
                    mode="pause_resume", occupancy=occ, warmup=0, min_kept=3)
        rr = [q for pen, q in _runs_from_cmds_pens(scene.out[mk:]) if pen == BLACK and run_len(q) >= MIN_RUN_TOP]
        black += rr
        if r_ < _RR:
            back_black += rr

    # ---- crimson yields CRIMSON_CLEAR to the rows behind the peak
    crimson = []
    bb = np.concatenate([densify(q) for q in back_black]) if back_black else np.zeros((0, 2))
    for q in rings0:
        Q = densify(q, 0.2)
        if len(bb):
            keep = np.sqrt(((Q[:, None, :] - bb[None, :, :]) ** 2).sum(2)).min(1) >= CRIMSON_CLEAR
        else:
            keep = np.ones(len(Q), bool)
        cur = []
        for pt, kk in zip(Q, keep):
            if kk:
                cur.append((float(pt[0]), float(pt[1])))
            else:
                if len(cur) >= 2 and run_len(cur) >= MIN_RUN:
                    crimson.append(cur)
                cur = []
        if len(cur) >= 2 and run_len(cur) >= MIN_RUN:
            crimson.append(cur)
    crimson = join_runs(crimson, tol=0.3)

    # ---- the science test, on the kept ink
    shown, missing = 0, []
    for r in range(N):
        for c in range(N):
            if not STRONG[r, c]:
                continue
            x, y, _ = P((c + 0.5) / N, (r + 0.5) / N, CAMC[r, c])
            Pt = np.array([float(x), float(y)])
            if (r, c) == ARGMAX:
                ok = len(crimson) > 0 and len(levels) >= 3
            else:
                ok = any(seg_dist(Pt, rb) < CREST_TOL for rb in black)
            shown += bool(ok)
            if not ok:
                missing.append((r, c))
    info = dict(shown=shown, missing=missing, levels=len(levels), start=start)
    return black, crimson, info


def cam_scale_sweep(L, table_scales=()):
    """Largest s (mm/CAM unit) at which all 13 strong crests are on the sheet,
    by bisection on the real top-plane drawing, plus a table at fixed scales."""
    def count(s):
        sc = Scene3D(None, None, fit="none", px=PX)
        _, _, info = top_plane(sc, s, 0.0, 0.0, L)
        return info["shown"], info["missing"]

    lo, hi = 0.6, 1.6
    assert count(lo)[0] == int(STRONG.sum())
    for _ in range(7):
        m = 0.5 * (lo + hi)
        if count(m)[0] == int(STRONG.sum()):
            lo = m
        else:
            hi = m
    table = []
    for s in table_scales:
        n_, miss = count(s)
        table.append((s, n_, miss))
    return lo, table


def cnn_one_summit(rng, bounds, colors: int = 2, feed: int = 2200, sweep_table: bool = False):
    x0, y0, x1, y1 = bounds
    fx0, fy0, fx1, fy1 = x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET
    n = len(LAYERS)
    widths = list(WIDTHS)

    # ---------------- the CAM height scale: measured, not chosen
    import os
    if os.environ.get("PP_CNN_SCALE"):          # dev only: skip the sweep while iterating
        s_max, sweep = float(os.environ["PP_CNN_SCALE"]), []
    else:
        s_max, sweep = cam_scale_sweep(widths[-1], (0.8, 1.0, 1.2, 1.4, 1.6, 1.9, 2.5, 4.0, 6.79) if sweep_table else ())
    S_CAM = round(SCALE_SAFETY * s_max, 3)
    amps = RELIEF + [S_CAM]

    # ---------------- per-layer terrain height H(u, v) (map units)
    pixn = norm01(LAYERS[0][1])
    fields = [pixn] + [norm01(A) for (_, A, _) in LAYERS[1:-1]] + [CAMC]

    def zfun(i, u, v):
        if i == 0:
            u, v = np.asarray(u, float), np.asarray(v, float)
            c = np.clip((u * 224).astype(int), 0, 223)
            r = np.clip((v * 224).astype(int), 0, 223)
            return pixn[r, c]
        return sample(fields[i], u, v)

    rows_of, us_of = [], []
    for i, (key, A, _) in enumerate(LAYERS):
        N = A.shape[0]
        rows_of.append((row_positions(N, STRIDES[i]) + 0.5) / N)
        if i == 0:
            us_of.append((np.arange(0, 224, PX_BAND) + PX_BAND / 2) / 224)
        else:
            us_of.append(np.linspace(0.5 / N, 1 - 0.5 / N, (N - 1) * U_PER_UNIT[i] + 1))

    def row_z(i, v):
        if i == 0:
            r = int(round(v * 224 - 0.5))
            return pixn[r].reshape(-1, PX_BAND).mean(axis=1)
        return zfun(i, us_of[i], np.full_like(us_of[i], v))

    origins: List[Tuple[float, float]] = [(0.0, 0.0)] * n

    def paper(i, u, v, z, lift=0.0):
        ox, oy = origins[i]
        L = widths[i]
        X = ox + np.asarray(u) * L
        D = (1.0 - np.asarray(v)) * L * DEPTH
        Z = oy + np.asarray(z) * amps[i] + lift
        return X + KX * D, KY * D + Z, KX * X - D + KY * Z

    for i in range(n):
        L = widths[i]
        origins[i] = (fx1 - (us_of[i][-1] * L + KX * (1 - rows_of[i][0]) * L * DEPTH), 0.0)

    xg = np.linspace(x0 - 20, x1 + 20, 900)

    def envelope(i):
        top = np.full_like(xg, -np.inf)
        bot = np.full_like(xg, np.inf)
        vv = rows_of[i] if i < n - 1 else np.linspace(rows_of[i][0], rows_of[i][-1], 49)
        for v in vv:
            zz = row_z(i, v) if i < n - 1 else sample(CAMC, us_of[i], np.full_like(us_of[i], v))
            sx, sy, _ = paper(i, us_of[i], np.full_like(us_of[i], v), zz)
            yi = np.interp(xg, sx, sy, left=np.nan, right=np.nan)
            m = np.isfinite(yi)
            top[m] = np.maximum(top[m], yi[m])
            bot[m] = np.minimum(bot[m], yi[m])
        return top, bot

    envs = [envelope(i) for i in range(n)]

    def stack(G):
        oys = [fy0 + CAP_BAND - float(np.nanmin(np.where(np.isfinite(envs[0][1]), envs[0][1], np.nan)))]
        for i in range(1, n):
            pt = envs[i - 1][0] + oys[i - 1]
            bb = envs[i][1]
            m = np.isfinite(pt) & np.isfinite(bb)
            oys.append(float(np.max(pt[m] - bb[m])) + G)
        return oys

    def top_of(oys):
        return float(np.nanmax(np.where(np.isfinite(envs[-1][0]), envs[-1][0], np.nan))) + oys[-1]

    lo, hi = 0.0, 80.0
    for _ in range(40):
        g = 0.5 * (lo + hi)
        if top_of(stack(g)) <= fy1 - SUMMIT_TOP_MAX:
            lo = g
        else:
            hi = g
    G = lo
    oys = stack(G)
    origins = [(origins[i][0], oys[i]) for i in range(n)]

    stats: dict = dict(gap_mm=round(G, 2), KY=KY, widths=widths, cam_scale=S_CAM, cam_scale_max=round(s_max, 3),
                       cam_sweep=sweep, origins=[(round(a, 1), round(b, 1)) for a, b in origins],
                       summit_floor=round(SUMMIT_FLOOR, 3))

    scene = Scene3D(rng, bounds, feed=feed, fit="none", px=PX)

    def samples(i, us, vs, zs, pen, lift=0.0):
        sx, sy, dp = paper(i, us, vs, zs, lift)
        return [(float(a), float(b), float(c), pen) for a, b, c in zip(sx, sy, dp)]

    per_layer = []   # (black runs, crimson runs) per plane, kept ink
    for i, (key, A, G_) in enumerate(LAYERS):
        N = A.shape[0]
        us = us_of[i]
        stats[key] = dict(N=N, stride=STRIDES[i], rows=len(rows_of[i]),
                          pitch_mm=round(KY * widths[i] * DEPTH / N * STRIDES[i], 2))
        if i == n - 1:
            # verify ON THE SHEET; the raster is re-anchored by the placement, so
            # step the scale down 1 % at a time until all 13 crests are kept
            tries = 0
            while True:
                mk = len(scene.out)
                black, crimson, info = top_plane(scene, S_CAM, origins[i][0], origins[i][1], widths[i])
                if info["shown"] == int(STRONG.sum()) or tries >= 8:
                    break
                del scene.out[mk:]
                S_CAM = round(S_CAM * 0.99, 4)
                tries += 1
            stats["cam_scale"] = S_CAM
            stats["cam_scale_steps_down"] = tries
            stats[key].update(relief_mm=round(S_CAM * float(np.ptp(CAMC)), 1),
                              peak_mm=round(S_CAM * float(CAMC.max()), 1), rings=info["levels"],
                              ring_runs=len(crimson))
            stats["crests_shown"] = f"{info['shown']} / {int(STRONG.sum())}"
            stats["crests_missing"] = info["missing"]
            per_layer.append((black, crimson))
            continue

        mark = len(scene.out)
        # ---- this layer's own z-buffer (dense between drawn rows)
        if ZB_SUB[i] > 1:
            vv_ = np.linspace(rows_of[i][0], rows_of[i][-1], (len(rows_of[i]) - 1) * ZB_SUB[i] + 1)
        else:
            vv_ = rows_of[i]
        UU, VV = np.meshgrid(us, vv_)
        ZZ = np.stack([row_z(0, v) for v in vv_]) if i == 0 else zfun(i, UU, VV)
        SX, SY, DEP = paper(i, UU, VV, ZZ)
        scene._rasterize(SX, SY, DEP)

        # ---- the rows: front row first so it owns the space (pause-resume)
        lines = [samples(i, us, np.full_like(us, v), row_z(i, v), BLACK) for v in rows_of[i][::-1]]
        scene.lines(lines, mode="pause_resume", sep_mm=0.8, warmup=0, min_kept=3)
        black = [r for pen, r in _runs_from_cmds_pens(scene.out[mark:]) if pen == BLACK and run_len(r) >= MIN_RUN]
        stats[key].update(relief_mm=amps[i])

        # ---- the ERF loop, occluded by its own map's nearer relief
        mu, Lc, r, held = erf_ellipse(G_, 0.5)
        t = np.linspace(0, 2 * math.pi, 2881)
        E = mu[:, None] + r * Lc @ np.stack([np.cos(t), np.sin(t)])
        eu = np.clip(E[0], us[0], us[-1])
        ev = np.clip(E[1], rows_of[i][0], rows_of[i][-1])
        if ERF_ON_SURFACE[i]:
            zc = zfun(i, eu, ev)                              # exactly the drawn bicubic surface
        else:
            # raster-noise maps: ride the local crest envelope, smoothed along the loop
            rad = 0.5 * STRIDES[i] / N
            zc = np.zeros_like(eu)
            ang = np.linspace(0, 2 * math.pi, 8, endpoint=False)
            for k, (a, b) in enumerate(zip(eu, ev)):
                pu = np.clip(np.concatenate([[a], a + rad * np.cos(ang)]), 0, 1)
                pv = np.clip(np.concatenate([[b], b + rad * np.sin(ang)]), 0, 1)
                zc[k] = float(np.max(zfun(i, pu, pv)))
            ker = np.ones(41) / 41.0
            zc = np.convolve(np.concatenate([zc[-20:], zc, zc[:20]]), ker, mode="same")[20:-20]
        smp = samples(i, eu, ev, zc, CRIMSON, lift=ERF_LIFT[i])
        vis = np.array([scene.visible(a, b, c) for a, b, c, _ in smp])
        Pp = np.array([(a, b) for a, b, _, _ in smp])
        arc = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(Pp, axis=0).T))])
        hid = ~vis
        # drop grazing flicker: hidden stretches shorter than ERF_HID_MIN
        spans, k = [], 0
        while k < len(hid):
            if hid[k]:
                j = k
                while j + 1 < len(hid) and hid[j + 1]:
                    j += 1
                spans.append((k, j))
                k = j + 1
            else:
                k += 1
        hid_d = np.zeros_like(hid)
        real = [(a, b) for a, b in spans if arc[b] - arc[a] >= ERF_HID_MIN]
        for a, b in real:
            hid_d |= (arc >= arc[a] - ERF_GAP) & (arc <= arc[b] + ERF_GAP)
        # the loop is closed: rotate so it starts inside a hidden span (one run
        # per visible stretch, no seam break)
        if hid_d.any() and not hid_d.all():
            k0 = int(np.flatnonzero(hid_d)[0])
            order = list(range(k0, len(smp) - 1)) + list(range(0, k0 + 1))
        else:
            order = list(range(len(smp)))
        loop = [(smp[k][0], smp[k][1], HIDE if hid_d[k] else smp[k][2], CRIMSON) for k in order]
        before = len(scene.out)
        scene.lines([loop], mode="over")
        crimson = [r_ for pen, r_ in _runs_from_cmds_pens(scene.out[before:]) if run_len(r_) >= MIN_RUN]
        stats[key].update(erf_mu=[round(float(x), 3) for x in mu], erf_r_sigma=round(r, 3),
                          erf_mass_held=round(held, 3), erf_runs=len(crimson), erf_breaks=len(real),
                          erf_hidden_mm=round(float(sum(arc[b] - arc[a] for a, b in real)), 1),
                          erf_on_surface=ERF_ON_SURFACE[i])
        per_layer.append((black, crimson))

    # ---------------- per-plane grammar stats (kept ink), thin vertices
    by_pen: dict = {BLACK: [], CRIMSON: []}
    for k, (key, *_r) in enumerate(LAYERS):
        black, crimson = per_layer[k]
        ls = [run_len(r) for r in black]
        stats[key].update(black_runs=len(black), breaks_per_row=round(len(black) / len(rows_of[k]) - 1, 2),
                          median_run=round(float(np.median(ls)), 1) if ls else 0,
                          shortest_run=round(min(ls), 1) if ls else 0,
                          black_mm=round(sum(ls)))
        by_pen[BLACK] += [rdp(r, RDP_TOL) for r in black]
        by_pen[CRIMSON] += [rdp(r, RDP_TOL) for r in crimson]

    top_black, top_crim = per_layer[-1]
    if top_black and top_crim:
        bp = np.concatenate([densify(r) for r in top_black])
        cp = np.concatenate([densify(r) for r in top_crim])
        stats["black_crimson_min_mm"] = round(float(np.sqrt(((bp[:, None, :] - cp[None, :, :]) ** 2).sum(2)).min()), 2)

    # ---------------- type: one flush-left axis = the input plane's front-left corner
    pix_black = per_layer[0][0]
    tx = round(min(p[0] for r in pix_black for p in r), 2)
    stats["type_axis_x"] = tx
    th = 5.4    # title cap height: MEANING must end left of the top plane (x 81.8)
    TW = 0.0   # title: single pass
    cap_top = y1 - 6.0 - TW / 2
    base0 = cap_top - th
    title_cmds = []
    for k, word in enumerate(("FROM", "PIXELS", "TO", "MEANING")):
        title_cmds += giant_type(word, tx, base0 - k * TITLE_LEAD * th, th, pen=BLACK, weight=0.0,
                                 spaced=True, f=feed)
    # A11: the title is drawn SINGLE-PASS (the weighted two-pass inline type
    # doubled at every acute join: M, N, A measured 0.30-0.39 mm apart)
    kept_title = [r for _, r in _runs_from_cmds_pens(title_cmds)]
    stats["title_parallel_min_mm"], stats["title_parallel_close_mm"] = [
        round(x, 2) for x in parallel_pairs(kept_title, 0.8)]

    cls = str(_D["class_name"]).replace("_", " ").upper()
    p1 = float(_D["top5"][0][1])
    lines_txt = [
        "BOTTOM → TOP  224²  56²  28²  14²  7²    HEIGHT = INPUT LUMINANCE / ‖ACTIVATION‖ OF BLOCKS 2, 5, 12 / CAM − MEAN, SIGNED",
        f"CRIMSON = 50% OF THE GRADIENT MASS OF ∂CAM(4,3) ON EACH MAP (~{ERF_AREA_PCT}% OF IMAGE VS ONE CELL = 2%)"
        f"    RINGS = CAM LEVELS ABOVE {SUMMIT_FLOOR:.1f}",
        f"MOBILENETV2 / IMAGENET    CHELSEA, CENTRE-CROP 300² → 224²    P({cls}) = {p1:.2f}    FRONT EDGE = IMAGE BOTTOM",
    ]
    cap_cmds = []
    for k, s_ in enumerate(lines_txt):
        cap_cmds += _stroke_text(s_, tx, fy0 + CAP_DESC + (len(lines_txt) - 1 - k) * CAP_PITCH, CAP_H, color=BLACK, f=feed)
    yb = fy0 + (len(lines_txt) - 1) * CAP_PITCH
    stats["caption_baseline"] = round(yb, 1)

    # ---------------- plot order: pen 0 (maps, then type), pen 1 (crimson)
    final = []
    black_order = order_runs(by_pen[BLACK], start=(x0, y0))
    for run in black_order:
        final += _poly(run, color=BLACK, f=feed)
    for r in kept_title:
        final += _poly(r, color=BLACK, f=feed)
    final += cap_cmds
    for run in order_runs(by_pen[CRIMSON], start=(x0, y0)):
        final += _poly(run, color=CRIMSON, f=feed)

    stats["runs"] = {pen: len(v) for pen, v in by_pen.items()}
    stats["ink_top"] = round(max(p[1] for v in by_pen.values() for r in v for p in r), 1)
    LAST_STATS.clear()
    LAST_STATS.update(stats)
    return final
