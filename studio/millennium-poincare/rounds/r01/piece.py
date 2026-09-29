"""THE POINCARÉ CONJECTURE — Millennium plate 6, r01 (thesis: FAITHFUL).

An illustrator's reconstruction of ``studio/millennium-poincare/ref/reference.png`` (an AI
poster, 1122 x 1402 px): a dumbbell wireframe on the rising diagonal, spaced-caps title
top-left over a short rule and an italic statement, a flush-right corner caption with its
own short rule, red loops as the one loud accent.  The reconstruction keeps that vocabulary
and replaces the poster's fiction (loops politely shrinking on a body that never changes)
with the real Ricci flow of a real dumbbell 3-sphere, cut and capped once (encoding.md).

Reference measurements (px on 1122 x 1402; u = x/1122, v = y/1402 from the TOP):
    title "THE POINCARÉ / CONJECTURE"  x  75..399  y  75..139   u .067-.356 v .053-.099
        cap height 19 px (1.35 % of H)  -> 5.7 mm on A3 (encoding asked 8: 40 % oversize)
    short rule under the title         x  75..131  y 159         v .113  (≈ 16 mm on A3)
    statement, 3 italic lines          x  75..370  y 183..263    line pitch 30 px, cap ≈ 14 px
    corner caption, 4 lines flush-R    right edge x 1047 (u .933) y 70..141, pitch 22 px, cap 7 px
        + short rule                   y 168
    the body (all ink)                 x  64..1069 y 159..1179   u .057-.953 v .113-.841
    body axis                          big lobe lower-left -> small lobe upper-right, ≈ 44°
    red: 7 loops on the body + a filmstrip of 7 ellipses, bottom right (y 1060..1120)
    bottom captions                    y 1268..1331               v .905-.950

Layout fixes against the reference (each a correction, listed in NOTES.md):
    1. the diagonal steepens 44° -> 62° (encoding §5) and the body shrinks from 90 % of the
       width to ≈ 75 %, opening the upper-left quiet triangle the reference fills with lobe
    2. the filmstrip of shrinking ellipses (lie 1) is cut; its corner becomes the data footer
    3. "A loop contracts to a point" + leader line is cut (forbidden 13); the one red loop
       left is the loop that does NOT contract
    4. the wireframe survives only as the back half-shell of the surgery instant, seen past
       the cut face; the cut face carries the flow's isochrones (the reference's "contour"
       vocabulary made into time)
    5. the gold point becomes two red extinction points (no ochre pen: encoding §6)
    6. three bottom-edge captions collapse to one colophon (sources)

Pens (layer order light -> dark -> accent, one swap each):
    0  HAIR   black 0.1 (preview dimgray)  the body at the cut instant: back half-shell
    1  BLACK  black 0.3                    the space at each instant: halo, start line,
                                           keyline x2, the two nests
    2  TEXT   black 0.3 (own layer)        type
    3  RED    red 0.5                      the cut (two caps), two extinction points,
                                           SOLVED, the stuck loop

Entry point: ``poincare_faithful``.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from matplotlib.path import Path as MPath

from promptplot.generative.engine.kit import fill_disc
from promptplot.generative.engine.scene3d import Camera, Occupancy, Scene3D
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

HERE = Path(__file__).resolve().parent
ISO = HERE / "isochrones.npz"          # written by compute.py (exact time grid)
NPZ = HERE.parents[1] / "data" / "neckpinch.npz"   # the dossier run (2-D control numbers)

HAIR, BLACK, TEXT, RED = 0, 1, 2, 3
F_DRAW = 2200

# ===========================================================================
# the one mapping — sheet mm, y UP from the bottom edge (A3 portrait 297 x 420)
# ===========================================================================
S_MM = 62.0                   # mm per unit of the warping function (encoding: 55-62)
BETA = math.radians(40.0)     # axis tilt out of the picture plane (encoding: 40 ± 5)
PHI = math.radians(62.0)      # the axis on the sheet, rising to the upper right
O_CUT = (156.0, 199.0)        # sheet position of the cut point (the pinned neck)
FLOOR = 0.8                   # mm, one pen's minimum line gap (merge rule)
MIN_FRAG = 2.0                # mm, pause fragments shorter than this are culled
SAMPLE = 0.2                  # mm, resampling step for occlusion / merge tests

D_AX = (math.cos(PHI), math.sin(PHI))       # axis direction on the sheet, A -> B
N_AX = (-math.sin(PHI), math.cos(PHI))      # in-picture normal to the axis
CB, SB = math.cos(BETA), math.sin(BETA)
# 3-D frame: X, Y on the sheet, Z toward the viewer.  The A end leans toward the viewer.
#   a3 = (cosβ·d, −sinβ)   n3 = (n, 0)   m3 = (sinβ·d, cosβ)   (m3·Z > 0: front half)


def sec(z, rho):
    """(z, ρ) in the meridian plane (units) -> sheet mm.  Foreshortened along the axis only."""
    z = np.asarray(z, float)
    rho = np.asarray(rho, float)
    x = O_CUT[0] + S_MM * (z * CB * D_AX[0] + rho * N_AX[0])
    y = O_CUT[1] + S_MM * (z * CB * D_AX[1] + rho * N_AX[1])
    return x, y


def rev(z, rho, th):
    """Surface of revolution point (axis coordinate z, radius ρ, angle θ) -> sheet x, y, depth.
    θ = 0 / π lie on the meridian plane (+n / −n); sin θ > 0 is the front half."""
    z, rho, th = (np.asarray(v, float) for v in (z, rho, th))
    c, s = np.cos(th), np.sin(th)
    along = z * CB + rho * s * SB            # component along d on the sheet
    x = O_CUT[0] + S_MM * (along * D_AX[0] + rho * c * N_AX[0])
    y = O_CUT[1] + S_MM * (along * D_AX[1] + rho * c * N_AX[1])
    dep = S_MM * (-z * SB + rho * s * CB)
    return x, y, dep


# ===========================================================================
# data -> profiles in the key frame (neck pinned at z = 0)
# ===========================================================================
def embed(psi: np.ndarray, L: float) -> Tuple[np.ndarray, np.ndarray]:
    """(z, ρ) profile of the surface of revolution (identical to data/ricci_rot.embed)."""
    N = len(psi) - 1
    ds = L / N
    ps = np.gradient(psi, ds, edge_order=2)
    dz = np.sqrt(np.clip(1 - ps ** 2, 0, None))
    z = np.concatenate([[0.0], np.cumsum(0.5 * (dz[1:] + dz[:-1]) * ds)])
    return z, psi.copy()


def _neck(psi: np.ndarray) -> int:
    c = psi[3:-3]
    m = (c <= psi[2:-4]) & (c <= psi[4:-2])
    idx = np.nonzero(m)[0]
    return int(idx[np.argmin(c[idx])] + 3)


def _neck_z(z: np.ndarray, psi: np.ndarray) -> float:
    """z of the neck minimum, refined by a parabola through the three grid nodes."""
    i = _neck(psi)
    y0, y1, y2 = psi[i - 1], psi[i], psi[i + 1]
    den = y0 - 2 * y1 + y2
    off = 0.5 * (y0 - y2) / den if abs(den) > 1e-15 else 0.0
    return float(np.interp(i + off, np.arange(len(z)), z))


def _centroid(z: np.ndarray, psi: np.ndarray, L: float) -> float:
    """ψ²·ds-weighted axis centroid (the limit point of a shrinking round piece)."""
    s = np.linspace(0, L, len(psi))
    w = psi ** 2
    return float(np.trapezoid(z * w, s) / np.trapezoid(w, s))


@lru_cache(maxsize=1)
def profiles() -> Dict[str, dict]:
    d = np.load(ISO)
    names = [str(x) for x in d["names"]]
    out: Dict[str, dict] = {}
    rec = {k: (float(d["t_target"][i]), float(d["t_actual"][i]), d["psi"][i], float(d["L"][i]))
           for i, k in enumerate(names)}
    i_s = int(d["i_s"])
    # keyline: the cut is made at grid node i_s, so pin THAT node at z = 0
    _, _, pk, Lk = rec["key"]
    zk, rk = embed(pk, Lk)
    z_cut = float(zk[i_s])
    out["key"] = dict(t=float(d["t_s"]), z=zk - z_cut, r=rk, kind="key")
    # past lines + start line: neck minimum pinned at z = 0
    for k in ["start"] + [f"past{j}" for j in range(1, 6)]:
        tt, ta, p, L = rec[k]
        z, r = embed(p, L)
        out[k] = dict(t=tt, t_act=ta, z=z - _neck_z(z, p), r=r, kind="past")
    # pieces: ψ²ds-centroid held at its t_s position in the key frame
    zA0, rA0 = embed(rec["A0"][2], rec["A0"][3])
    cA = _centroid(zA0, rA0, rec["A0"][3]) - z_cut                 # pole A sits at −z_cut
    zB0, rB0 = embed(rec["B0"][2], rec["B0"][3])
    ZB = float(zk[-1]) - z_cut                                      # pole B in the key frame
    cB = ZB - _centroid(zB0, rB0, rec["B0"][3])
    for k in names:
        if k[0] in "AB" and k[1:].isdigit() and k[1:] != "0":
            tt, ta, p, L = rec[k]
            z, r = embed(p, L)
            c = _centroid(z, r, L)
            zf = (z - c + cA) if k[0] == "A" else (cB - (z - c))
            out[k] = dict(t=tt, t_act=ta, z=zf, r=r, kind=k[0], idx=int(k[1:]))
    out["_meta"] = dict(t_s=float(d["t_s"]), h=float(pk[i_s]), cA=cA, cB=cB,
                        T_A=float(d["T_ext_A"]), T_B=float(d["T_ext_B"]),
                        err=float(d["max_snap_err"]), neck0=float(np.min(rec["start"][2][50:-50])),
                        zA0=zA0 - z_cut, rA0=rA0, zB0=ZB - zB0, rB0=rB0)
    return out


def outline(pr: dict) -> np.ndarray:
    """Closed section outline (z, ±ρ) -> sheet polygon, upper side A->B, lower side back."""
    z, r = pr["z"], pr["r"]
    zz = np.concatenate([z, z[::-1][1:]])
    rr = np.concatenate([r, -r[::-1][1:]])
    x, y = sec(zz, rr)
    return np.column_stack([x, y])


# ===========================================================================
# line machinery: resample, occlude (cards), merge (Occupancy pause-resume)
# ===========================================================================
def resample(pts: np.ndarray, step: float = SAMPLE) -> np.ndarray:
    seg = np.hypot(*np.diff(pts, axis=0).T)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    n = max(2, int(math.ceil(s[-1] / step)) + 1)
    u = np.linspace(0, s[-1], n)
    return np.column_stack([np.interp(u, s, pts[:, 0]), np.interp(u, s, pts[:, 1])])


def _inside_any(pts: np.ndarray, paths: Sequence[MPath]) -> np.ndarray:
    m = np.zeros(len(pts), bool)
    for p in paths:
        m |= p.contains_points(pts)
    return m


def _edge(a, b, paths, a_in: bool) -> Pt:
    """Bisect the segment a-b to the card boundary (to 1e-4 mm)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    for _ in range(14):
        m = 0.5 * (a + b)
        if bool(_inside_any(m[None], paths)[0]) == a_in:
            a = m
        else:
            b = m
    return (float(0.5 * (a[0] + b[0])), float(0.5 * (a[1] + b[1])))


def occlude(pts: np.ndarray, paths: Sequence[MPath], closed: bool = False,
            keep_inside: bool = False) -> List[np.ndarray]:
    """Runs of a sampled line that lie OUTSIDE every card (or, ``keep_inside``, inside the
    union), ends landed on the card edge."""
    if not paths:
        return [pts]
    hid = _inside_any(pts, paths)
    if keep_inside:
        hid = ~hid
    if not hid.any():
        return [pts]
    runs, cur = [], []
    for i in range(len(pts)):
        if not hid[i]:
            if not cur and i > 0 and hid[i - 1]:
                cur.append(_edge(pts[i - 1], pts[i], paths, not keep_inside))
            cur.append(tuple(pts[i]))
        else:
            if cur:
                cur.append(_edge(pts[i - 1], pts[i], paths, keep_inside))
                runs.append(np.array(cur))
                cur = []
    if cur:
        runs.append(np.array(cur))
    if closed and len(runs) > 1 and not hid[0] and not hid[-1]:
        runs[0] = np.vstack([runs[-1], runs[0][1:]])
        runs.pop()
    return runs


def _plen(p: np.ndarray) -> float:
    return float(np.hypot(*np.diff(p, axis=0).T).sum()) if len(p) > 1 else 0.0


BRIDGE = 5.0    # mm: a clear gap shorter than this between two paused stretches stays paused


def _bridge(bad: np.ndarray, r: np.ndarray, gap: float) -> np.ndarray:
    """Morphological closing of the pause mask along the line: a line that is merged on both
    sides of a short clear stretch stays merged through it, so a merge band reads as ONE
    line, not a comb of crumbs (hysteresis on pause-resume)."""
    if not bad.any() or bad.all():
        return bad
    s = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(r, axis=0).T))])
    out = bad.copy()
    idx = np.nonzero(bad)[0]
    for a, b in zip(idx[:-1], idx[1:]):
        if b - a > 1 and s[b] - s[a] < gap:
            out[a:b] = True
    return out


def merge(runs: Sequence[np.ndarray], occ: Occupancy, sep_check: bool = True,
          per_run: bool = False) -> List[np.ndarray]:
    """Pause each run where it comes within FLOOR of an already drawn (higher-ranked) line,
    resume when clear, cull fragments < MIN_FRAG, then register what was kept.  ``per_run``
    registers after every run (a FAMILY given in rank order); otherwise the runs are the
    pieces of ONE line and are registered together."""
    kept: List[np.ndarray] = []
    for r in runs:
        n0 = len(kept)
        if sep_check:
            bad = np.array([occ.crowded(x, y) for x, y in r])
        else:
            bad = np.zeros(len(r), bool)
        bad = _bridge(bad, r, BRIDGE)
        cur: List[Pt] = []
        for i, (x, y) in enumerate(r):
            if bad[i]:
                if len(cur) > 1 and _plen(np.array(cur)) >= MIN_FRAG:
                    kept.append(np.array(cur))
                cur = []
            else:
                cur.append((x, y))
        if len(cur) > 1 and _plen(np.array(cur)) >= MIN_FRAG:
            kept.append(np.array(cur))
        if per_run:
            for k in kept[n0:]:
                for x, y in k:
                    occ.add(x, y)
    if not per_run:
        for k in kept:
            for x, y in k:
                occ.add(x, y)
    return kept


# ===========================================================================
# the section: halo (past), start line, keyline, the two nests
# ===========================================================================
@lru_cache(maxsize=1)
def build_section():
    P = profiles()
    meta = P["_meta"]
    past_keys = [f"past{j}" for j in range(1, 6)]            # latest first
    rings_A = sorted([k for k in P if k.startswith("A")], key=lambda k: P[k]["idx"])
    rings_B = sorted([k for k in P if k.startswith("B")], key=lambda k: P[k]["idx"])
    polys = {k: outline(P[k]) for k in ["key", "start"] + past_keys + rings_A + rings_B}
    mpaths = {k: MPath(v) for k, v in polys.items()}
    stats: Dict[str, float] = {}
    # --- time-occlusion: each line hidden under every LATER card ------------------------
    # later than a past line: the later past lines and the keyline (the rings lie inside
    # the keyline card; the ≤ 0.65 mm A overshoot is absorbed by the merge rule instead)
    vis: Dict[str, List[np.ndarray]] = {}
    order_past = ["start"] + past_keys[::-1]                  # earliest -> latest
    for i, k in enumerate(order_past):
        later = [mpaths[j] for j in order_past[i + 1:]] + [mpaths["key"]]
        pts = resample(polys[k])
        runs = occlude(pts, later, closed=True)
        vis[k] = runs
        stats[f"clip_{k}"] = 1.0 - sum(_plen(r) for r in runs) / _plen(pts)
    vis["key"] = [resample(polys["key"])]
    key_path = mpaths["key"]
    for k in rings_A + rings_B:
        pts = resample(polys[k])
        inside = key_path.contains_points(pts)
        stats[f"out_{k}"] = float((~inside).mean())
        # the future lies inside the keyline: where the centroid alignment lets a ring
        # overshoot the t_s outline at A's far pole (measured ≤ 1.73 mm on the sheet) the ring
        # is clipped to the keyline card, and the merge rule then folds it into the keyline
        vis[k] = [pts] if inside.all() else occlude(pts, [key_path], closed=True, keep_inside=True)
    # --- merge rule: rank by |t − t_s|, the two event lines above everything ----------
    rank = ["key", "start"]
    kmax = max(len(rings_A), len(past_keys), len(rings_B))
    for j in range(1, kmax + 1):
        for k in (f"past{j}", f"A{j}", f"B{j}"):
            if k in vis:
                rank.append(k)
    occ = Occupancy(FLOOR + 0.05)
    drawn: Dict[str, List[np.ndarray]] = {}
    for k in rank:
        drawn[k] = merge(vis[k], occ, sep_check=(k != "key"))
        before = sum(_plen(r) for r in vis[k])
        stats[f"merge_{k}"] = 1.0 - sum(_plen(r) for r in drawn[k]) / max(before, 1e-9)
    return dict(P=P, polys=polys, drawn=drawn, stats=stats, rings_A=rings_A, rings_B=rings_B,
                past=past_keys, meta=meta)


# ===========================================================================
# the body at the cut instant: back half-shell (Scene3D z-buffer), outside all cards
# ===========================================================================
@lru_cache(maxsize=1)
def build_shell():
    S = build_section()
    P = S["P"]
    key = P["key"]
    z, r = key["z"], key["r"]
    L = len(z)
    # z-buffer of the back half: a fine (s, θ) grid through the engine's rasterizer
    iz = np.linspace(0, L - 1, 161).astype(int)
    th = np.linspace(math.pi, 2 * math.pi, 73)
    ZZ, TT = np.meshgrid(z[iz], th, indexing="ij")
    RR = np.repeat(r[iz][:, None], len(th), 1)
    SX, SY, DEP = rev(ZZ, RR, TT)
    sc = Scene3D(None, None, camera=Camera(proj=lambda *a: a[:2], depth=lambda *a: a[2]),
                 fit="none", px=(520, 520), pad=2.0)
    sc.surface(SX, SY, DEP, pen=0, thin=None)      # rasterize; its own mesh is discarded
    cards = [MPath(v) for v in S["polys"].values()]

    def visible_runs(xs, ys, ds):
        pts = np.column_stack([xs, ys])
        ok = np.array([sc.visible(x, y, d) for x, y, d in zip(xs, ys, ds)])
        runs, cur = [], []
        for i in range(len(pts)):
            if ok[i]:
                cur.append(pts[i])
            elif cur:
                runs.append(np.array(cur))
                cur = []
        if cur:
            runs.append(np.array(cur))
        out = []
        for rr in runs:
            if len(rr) > 1:
                out += occlude(resample(rr), cards)
        return out

    s_arc = np.linspace(0, 1, L)
    lines_par, lines_mer, sil = [], [], []
    # parallels at equal Δs (each one a round 2-sphere of radius ψ)
    Ls = float(np.sum(np.hypot(np.diff(z), np.diff(r))))
    n_par = int(Ls / 0.075)
    sgrid = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(z), np.diff(r)))])
    tt = np.linspace(math.pi, 2 * math.pi, 241)
    for k in range(1, n_par):
        sk = Ls * k / n_par
        zk = float(np.interp(sk, sgrid, z))
        rk = float(np.interp(sk, sgrid, r))
        xs, ys, ds = rev(np.full_like(tt, zk), np.full_like(tt, rk), tt)
        lines_par += visible_runs(xs, ys, ds)
    # half-meridians every 15°
    zf = np.interp(np.linspace(0, Ls, 900), sgrid, z)
    rf = np.interp(np.linspace(0, Ls, 900), sgrid, r)
    for j in range(1, 12):
        a = math.pi + j * math.pi / 12
        xs, ys, ds = rev(zf, rf, np.full_like(zf, a))
        lines_mer += visible_runs(xs, ys, ds)
    # silhouette: normal ⟂ view  ->  sin θ = −(ρ'/z')·tanβ·(−1) on the back half
    zs = np.gradient(z)
    rs = np.gradient(r)
    with np.errstate(divide="ignore", invalid="ignore"):
        sv = -(rs / zs) * math.tan(BETA)
    for sign in (1, -1):
        seg_x, seg_y, seg_d = [], [], []
        pieces = []
        for i in range(L):
            if np.isfinite(sv[i]) and -1 <= sv[i] < 0:
                a = math.asin(sv[i])                     # in [−π/2, 0)
                thv = a if sign > 0 else math.pi - a     # cos θ > 0 / cos θ < 0
                x, y, dd = rev(z[i], r[i], thv)
                seg_x.append(float(x)); seg_y.append(float(y)); seg_d.append(float(dd))
            elif seg_x:
                pieces.append((seg_x, seg_y, seg_d))
                seg_x, seg_y, seg_d = [], [], []
        if seg_x:
            pieces.append((seg_x, seg_y, seg_d))
        for xs, ys, ds in pieces:
            if len(xs) > 1:
                sil += occlude(resample(np.column_stack([xs, ys])), cards)
    # crowd control per family (the ScreenThin idea on free lines): Occupancy, 0.8 mm
    occ_p = Occupancy(FLOOR + 0.05)
    occ_m = Occupancy(FLOOR + 0.05)
    sil_k = merge(sil, occ_p, sep_check=False)
    par_k = merge(lines_par, occ_p, per_run=True)
    for q in sil_k:
        for x, y in q:
            occ_m.add(x, y)
    mer_k = dashes(merge(lines_mer, occ_m, per_run=True), DASH_ON, DASH_OFF)
    return dict(par=par_k, mer=mer_k, sil=sil_k)


DASH_ON, DASH_OFF = 2.2, 1.5     # mm: the reference's dashed back meridians


def dashes(runs: Sequence[np.ndarray], on: float, off: float) -> List[np.ndarray]:
    """Cut runs into dashes by arc length (phase restarts per run)."""
    out: List[np.ndarray] = []
    for r in runs:
        rr = resample(r, 0.1)
        s = np.concatenate([[0.0], np.cumsum(np.hypot(*np.diff(rr, axis=0).T))])
        ph = np.mod(s, on + off) < on
        cur = []
        for i in range(len(rr)):
            if ph[i]:
                cur.append(rr[i])
            elif cur:
                if len(cur) > 3:
                    out.append(np.array(cur))
                cur = []
        if len(cur) > 3:
            out.append(np.array(cur))
    return out


# ===========================================================================
# red: the cut, the stuck loop, the extinction points
# ===========================================================================
def build_red():
    S = build_section()
    m = S["meta"]
    h = m["h"]
    ph = np.linspace(0, math.pi, 90)
    capA = np.column_stack(sec(h * np.sin(ph), h * np.cos(ph)))       # ")" A's cap, toward B
    capB = np.column_stack(sec(-h * np.sin(ph), h * np.cos(ph)))      # "(" B's cap, toward A
    # t = 0 neck geodesic (CSF parks a loop here): the parallel of radius neck0 at z = 0.
    r0 = m["neck0"]
    th = np.linspace(0, math.pi, 181)                                   # front half only
    lx, ly, _ = rev(np.zeros_like(th), np.full_like(th, r0), th)
    loop = np.column_stack([lx, ly])
    dots = [tuple(float(v) for v in sec(m["cA"], 0.0)), tuple(float(v) for v in sec(m["cB"], 0.0))]
    return dict(caps=[capA, capB[::-1]], loop=loop, dots=dots)


# ===========================================================================
# type
# ===========================================================================
def _small(strokes, y0: float, k: float = 0.52):
    return [[(x * k + 0.6, y * k + y0) for (x, y) in st] for st in strokes]


GLYPHS = dict(_GLYPHS)
GLYPHS.update({
    "É": _GLYPHS["E"] + [[(1.6, 6.9), (2.8, 7.9)]],
    "π": [[(0.2, 3.6), (0.8, 4.0), (3.8, 4.0)], [(1.4, 4.0), (1.2, 0.0)],
          [(2.9, 4.0), (2.9, 0.6), (3.3, 0.0), (3.8, 0.3)]],
    "Δ": [[(0, 0), (2, 6), (4, 0), (0, 0)]],
    "–": [[(0.4, 3), (3.6, 3)]],
    "—": [[(0.0, 3), (4.0, 3)]],
    "·": [[(1.8, 2.8), (2.2, 2.8)]],
})


def _adv(ch: str) -> float:
    if ch == " ":
        return 2.6
    st = GLYPHS.get(ch) or GLYPHS.get(ch.upper()) or []
    xs = [p[0] for s in st for p in s]
    if not xs:
        return 2.6
    sb = 0.55 if ch.islower() else 1.02
    return (max(xs) - min(xs)) + 2.0 * sb


def text_width(txt: str, h: float, track: float = 0.0) -> float:
    return sum(_adv(c) for c in txt) * h / 6.0 + track * max(0, len(txt) - 1)


def chain(runs: List[Poly], tol: float = 0.02) -> List[Poly]:
    runs = [list(r) for r in runs]
    out: List[Poly] = []
    while runs:
        cur = runs.pop(0)
        grown = True
        while grown:
            grown = False
            for i, r in enumerate(runs):
                if math.dist(cur[-1], r[0]) < tol:
                    cur += r[1:]
                elif math.dist(cur[-1], r[-1]) < tol:
                    cur += r[::-1][1:]
                elif math.dist(cur[0], r[-1]) < tol:
                    cur = r + cur[1:]
                elif math.dist(cur[0], r[0]) < tol:
                    cur = r[::-1] + cur[1:]
                else:
                    continue
                runs.pop(i)
                grown = True
                break
        out.append(cur)
    return out


def set_text(txt: str, x: float, y: float, h: float, track: float = 0.0,
             slant: float = 0.0) -> List[Poly]:
    """Left-baseline stroke text -> polylines.  ``slant`` shears (italic, the reference's
    statement voice)."""
    sc = h / 6.0
    runs: List[Poly] = []
    cx = x
    for ch in txt:
        st = GLYPHS.get(ch)
        if st is None:
            st = GLYPHS.get(ch.upper(), [])
        xs = [p[0] for s in st for p in s]
        x_off = -min(xs) + (0.55 if ch.islower() else 1.02) if xs else 0.0
        runs += chain([[(cx + (gx + x_off) * sc + slant * gy * sc, y + gy * sc) for gx, gy in s]
                       for s in st])
        cx += _adv(ch) * sc + track
    return runs


def set_right(txt: str, xr: float, y: float, h: float, track: float = 0.0) -> List[Poly]:
    return set_text(txt, xr - text_width(txt, h, track), y, h, track)


# ===========================================================================
# the plate
# ===========================================================================
def _sheet_stats():
    return build_section()["stats"]


def _order_runs(runs: List[np.ndarray]) -> List[np.ndarray]:
    """Greedy nearest-end order (with reversal) inside one region of one layer."""
    todo = [np.asarray(r) for r in runs if len(r) > 1]
    out: List[np.ndarray] = []
    cur = None
    while todo:
        if cur is None:
            i = int(np.argmin([min(r[0][0], r[-1][0]) for r in todo]))
            r = todo.pop(i)
        else:
            best, bi, rv = 1e18, 0, False
            for i, r in enumerate(todo):
                d0 = math.dist(cur, r[0])
                d1 = math.dist(cur, r[-1])
                if d0 < best:
                    best, bi, rv = d0, i, False
                if d1 < best:
                    best, bi, rv = d1, i, True
            r = todo.pop(bi)
            if rv:
                r = r[::-1]
        out.append(r)
        cur = tuple(r[-1])
    return out


def poincare_faithful(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    def pen(i: int) -> Optional[int]:
        return i if colors >= 4 else min(i, max(colors - 1, 0))

    S = build_section()
    SH = build_shell()
    R = build_red()
    out: List[GCodeCommand] = []

    def emit(runs, p):
        for q in runs:
            out.extend(_poly([tuple(map(float, v)) for v in q], color=pen(p), f=F_DRAW))

    # L0 hairline shell
    emit(_order_runs(SH["sil"] + SH["par"] + SH["mer"]), HAIR)
    # L1 black: start -> halo outer->inner -> keyline x2 -> B outer->inner -> A outer->inner
    d = S["drawn"]
    seq = ["start"] + [f"past{j}" for j in range(5, 0, -1)]
    emit(_order_runs(sum((d[k] for k in seq), [])), BLACK)
    emit(d["key"], BLACK)
    emit(d["key"], BLACK)
    for k in S["rings_B"]:
        emit(d[k], BLACK)
    for k in S["rings_A"]:
        emit(d[k], BLACK)
    # L2 type
    emit(build_text(), TEXT)
    # L3 red
    emit(R["caps"], RED)
    emit([R["loop"]], RED)
    for (x, y) in R["dots"]:
        out.extend(fill_disc(x, y, 0.8, spacing=0.4, pen=pen(RED), f=F_DRAW))
    emit(build_red_type(), RED)
    return out


# layout of type (reference-measured, see module docstring) — sheet mm, y up
X_L = 15.0
X_R = 282.0
TOP = 403.0
BASE = 17.0                       # shared bottom baseline: colophon + footer
X_F = 204.0                       # footer column, flush left


FOOTER = [
    ["EACH LINE: THE WHOLE SPACE AT", "ONE INSTANT, IN SECTION — EVERY", "CHORD A ROUND 2-SPHERE"],
    ["ONE LINE = Δt 0.01 OF ∂g/∂t = −2 Ric,", "COUNTED FROM THE CUT"],
    ["NECK 0.314 → 0.120 WHILE THE LOBE", "LOSES 12 % · CUT AND CAPPED", "AT t = 0.055"],
    ["SMALL PIECE VANISHES ROUND AT", "t = 0.117 · LARGE AT t = 0.387"],
    ["IN 2-D THE SAME NECK WOULD WIDEN", "(0.314 → 0.355): EACH RING IS", "SECRETLY A SPHERE"],
    ["RED RING: CURVE-SHORTENING PARKS", "A LOOP HERE, LENGTH 2π·0.314,", "FOREVER"],
]
H_FOOT, LEAD_FOOT, GAP_FOOT = 2.0, 4.0, 2.6


def build_text() -> List[Poly]:
    T: List[Poly] = []
    hT = 6.0
    T += set_text("THE POINCARÉ", X_L, TOP - hT, hT, track=3.4)
    T += set_text("CONJECTURE", X_L, TOP - hT - 9.5, hT, track=3.4)
    T.append([(X_L, TOP - 23.0), (X_L + 16.0, TOP - 23.0)])
    hs = 3.2
    y = TOP - 31.5
    for ln in ["Every closed, simply connected", "3-manifold is homeomorphic", "to the 3-sphere."]:
        T += set_text(ln, X_L, y, hs, track=0.35, slant=0.18)
        y -= 7.0
    # stamp: SOLVED (red, build_red_type) then two lines of credit
    y = Y_SOLVED - 7.0
    for ln in ["G. PERELMAN 2002–03 · RICCI FLOW WITH SURGERY,",
               "AFTER R. HAMILTON (1982) · CLAY PRIZE 18 MAR 2010, DECLINED"]:
        T += set_text(ln, X_L, y, 2.0, track=0.42)
        y -= 4.4
    # corner caption, flush right, 4 lines + short rule (reference: 7 px caps, 22 px pitch)
    yc = TOP - 2.5
    for ln in ["TO PROVE", "IT IS ONE SPHERE", "THE FLOW", "CUTS IT IN TWO"]:
        T += set_right(ln, X_R, yc, 2.2, track=1.1)
        yc -= 5.6
    T.append([(X_R - 11.0, yc + 1.6), (X_R, yc + 1.6)])
    # footer: bottom-up so its last baseline sits on BASE
    lines: List[Optional[str]] = []
    for blk in FOOTER:
        lines += blk + [None]
    lines.pop()
    y = BASE
    for ln in reversed(lines):
        if ln is None:
            y += GAP_FOOT
            continue
        T += set_text(ln, X_F, y, H_FOOT, track=0.36)
        y += LEAD_FOOT
    T.append([(X_F, y + 1.0), (X_F + 11.0, y + 1.0)])        # short rule, the series' mark
    # colophon, bottom-left on the shared baseline
    T += set_text("arXiv math/0211159 · 0303109 · 0307245 · ANGENENT–KNOPF 2004", X_L, BASE + 3.6,
                  1.8, track=0.3)
    T += set_text("ROTATIONALLY SYMMETRIC S³ · SURGERY AT NECK RADIUS h = 0.12", X_L, BASE,
                  1.8, track=0.3)
    return T


Y_SOLVED = TOP - 31.5 - 14.0 - 11.0


def build_red_type() -> List[Poly]:
    return set_text("SOLVED", X_L, Y_SOLVED, 4.2, track=2.6)
