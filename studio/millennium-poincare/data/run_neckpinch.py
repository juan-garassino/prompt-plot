"""NECKPINCH -> SURGERY -> EXTINCTION for the dumbbell 3-sphere, plus the 2-D control.

    .venv/bin/python studio/millennium-poincare/data/run_neckpinch.py

Writes neckpinch.npz next to this file: profiles psi(s) at equal time steps (pre-surgery,
and for each post-surgery piece) plus the scalar diagnostics quoted in dossier.md section 7.
Deterministic (no randomness). Pure numpy.
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dumbbell as D  # noqa: E402
from ricci_rot import _d, scalar_curvature, step  # noqa: E402

N = 400
N_POST = 400            # grid for the post-surgery pieces (smooth, nearly round)
H_SURGERY = 0.12          # surgery scale: cut when the neck radius reaches this
H_PROBE = 0.05            # an un-cut branch continues to here to measure the pinch rate
DT_SNAP = 0.005           # isochrone spacing in Ricci-flow time


def neck_index(psi):
    c = psi[3:-3]
    m = (c <= psi[2:-4]) & (c <= psi[4:-2])
    if not m.any():
        return None
    idx = np.nonzero(m)[0]
    return int(idx[np.argmin(c[idx])] + 3)


def volume(psi, L, n):
    """vol of S^{n+1} warped product: |S^n| * int psi^n ds  (|S^2| = 4 pi)"""
    s = np.linspace(0, L, len(psi))
    omega = {1: 2 * np.pi, 2: 4 * np.pi}[n]
    return omega * np.trapezoid(psi**n, s)


def cap(psi_side, L_side, h):
    """Glue a round hemisphere cap of radius h at the cut end (psi=h, psi_s~0)."""
    s = np.linspace(0, L_side, len(psi_side))
    sc = np.linspace(0, np.pi * h / 2, 200)[1:]
    psi_c = h * np.cos(sc / h)
    s_all = np.concatenate([s, L_side + sc])
    p_all = np.concatenate([psi_side, psi_c])
    Lnew = s_all[-1]
    return np.interp(np.linspace(0, Lnew, N_POST + 1), s_all, p_all), Lnew


def run_to_extinction(psi, L, n, t0, tag, snaps):
    t = t0
    next_snap = (np.floor(t0 / DT_SNAP) + 1) * DT_SNAP
    hist = []
    while np.max(psi) > 0.06:
        psi, L, dt = step(psi, L, n)
        t += dt
        hist.append((t, np.max(psi), L))
        if t >= next_snap:
            snaps.append((tag, t, psi.copy(), L))
            next_snap += DT_SNAP
    h = np.array(hist)
    # extinction: fit psi_max^2 = 4 (T - t)-type line on the last stretch, extrapolate
    tail = h[h[:, 1] < 0.12]
    slope, icpt = np.polyfit(tail[:, 0], tail[:, 1] ** 2, 1)
    T = -icpt / slope
    return T, slope, h


def main():
    out = {}
    snaps = []
    psi, L, _ = D.initial_profile(N)
    n = 2
    t = 0.0
    R0 = scalar_curvature(psi, L, n)
    i = neck_index(psi)
    out.update(L0=L, neck0=psi[i], lobeA0=psi[:i].max(), lobeB0=psi[i:].max(),
               Rmin0=R0[8:-8].min(), vol0=volume(psi, L, n))
    snaps.append(("pre", 0.0, psi.copy(), L))
    next_snap = DT_SNAP
    th = []
    surg = None
    while True:
        psi, L, dt = step(psi, L, n)
        t += dt
        i = neck_index(psi)
        th.append((t, psi[i], psi[:i].max(), psi[i:].max(), L))
        if surg is None and t >= next_snap:
            snaps.append(("pre", t, psi.copy(), L))
            next_snap += DT_SNAP
        if surg is None and psi[i] <= H_SURGERY:
            surg = (t, psi.copy(), L, i)
            snaps.append(("surgery", t, psi.copy(), L))
        if psi[i] <= H_PROBE:
            break
    th = np.array(th)
    # pinch time: psi_min^2 vs t is asymptotically linear with slope -2(n-1) = -2
    near = th[th[:, 1] < 0.09]
    slope, icpt = np.polyfit(near[:, 0], near[:, 1] ** 2, 1)
    t, psi, L, i = surg
    k = np.argmin(np.abs(th[:, 0] - t))
    out.update(t_surgery=t, T_pinch_extrap=-icpt / slope, neck_sq_slope=slope,
               lobeA_at_surgery=th[k, 2], lobeB_at_surgery=th[k, 3], L_at_surgery=L)
    print("pre-surgery done", flush=True)
    ds = L / N
    s_cut = i * ds
    left, Ll = cap(psi[: i + 1], s_cut, psi[i])
    right, Lr = cap(psi[i:][::-1], L - s_cut, psi[i])
    TA, slA, hA = run_to_extinction(left, Ll, n, t, "A", snaps)
    print("piece A done", TA, flush=True)
    TB, slB, hB = run_to_extinction(right, Lr, n, t, "B", snaps)
    print("piece B done", TB, flush=True)
    # roundness at psi_max ~ 0.10:  L/psi_max -> pi for a round S^3
    def roundness(h):
        k = np.argmin(np.abs(h[:, 1] - 0.10))
        return h[k, 2] / h[k, 1]
    out.update(T_ext_A=TA, slope_ext_A=slA, T_ext_B=TB, slope_ext_B=slB,
               roundA=roundness(hA), roundB=roundness(hB))
    # ---- 2-D control: same profile, n = 1 (Ricci flow of the surface itself) ----
    psi1, L1, _ = D.initial_profile(N_POST)
    s1 = np.linspace(0, L1, N_POST + 1)
    area0 = 2 * np.pi * np.trapezoid(psi1, s1)
    t1 = 0.0
    ratio_hist = []
    while np.max(psi1) > 0.3:
        psi1, L1, dt = step(psi1, L1, 1)
        t1 += dt
        j = neck_index(psi1)
        ratio_hist.append((t1, (psi1[j] / psi1.max()) if j else 1.0,
                           2 * np.pi * np.trapezoid(psi1, np.linspace(0, L1, N_POST + 1))))
    rh = np.array(ratio_hist)
    gone = rh[rh[:, 1] >= 1.0]
    out.update(area0_2d=area0, T_ext_2d_exact=area0 / (8 * np.pi),
               area_slope_2d=np.polyfit(rh[:, 0], rh[:, 2], 1)[0],
               t_neck_gone_2d=gone[0, 0] if len(gone) else np.nan,
               min_ratio_2d=rh[:, 1].min())
    for k, v in out.items():
        print(f"{k:>18s} = {v:.6g}")
    np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "neckpinch.npz"),
             snap_tag=np.array([s[0] for s in snaps]), snap_t=np.array([s[1] for s in snaps]),
             snap_L=np.array([s[3] for s in snaps]), snap_psi=np.stack([s[2] for s in snaps]),
             neck_hist=th, **{k: np.float64(v) for k, v in out.items()})


if __name__ == "__main__":
    main()
