"""Curve-shortening flow (CSF) checks — the 1-D model of Ricci flow.

    .venv/bin/python studio/millennium-poincare/data/csf.py

(1) Plane: X_t = kappa N. For ANY embedded closed curve dA/dt = -int kappa ds = -2 pi
    exactly (turning number 1), so extinction T = A0 / (2 pi) (Gage-Hamilton 1986,
    Grayson 1987). Discretisation: arclength-uniform polygon, X_t = X_ss, remeshed.
(2) Surface of revolution ds^2 + psi(s)^2 dtheta^2 (the drawn dumbbell, static): a parallel
    at s has geodesic curvature psi_s/psi, so CSF moves it by ds/dt = -psi_s/psi, i.e.
    gradient descent on log psi. Closed-geodesic parallels = critical points of psi.
(3) Gauss-Bonnet on that surface: int_{pole}^{s} K dA = 2 pi (1 - psi_s(s)).
"""
from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dumbbell as D  # noqa: E402


def polygon_area(P):
    x, y = P[:, 0], P[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def remesh(P, M):
    Q = np.vstack([P, P[:1]])
    seg = np.hypot(*np.diff(Q, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    u = np.linspace(0, s[-1], M + 1)[:-1]
    return np.stack([np.interp(u, s, Q[:, 0]), np.interp(u, s, Q[:, 1])], 1), s[-1]


def csf_plane(P, M=400, stop_area=0.02, snap_dA=None):
    P, Ltot = remesh(P, M)
    t = 0.0
    hist = [(0.0, polygon_area(P), Ltot)]
    snaps = [(0.0, P.copy())]
    A0 = hist[0][1]
    next_A = A0 - snap_dA if snap_dA else None
    while hist[-1][1] > stop_area:
        h = Ltot / M
        dt = 0.2 * h * h
        lap = (np.roll(P, -1, 0) - 2 * P + np.roll(P, 1, 0)) / (h * h)
        P = P + dt * lap
        t += dt
        P, Ltot = remesh(P, M)
        M = max(64, min(M, int(Ltot / 0.004)))  # keep resolution sane as it shrinks
        A = polygon_area(P)
        hist.append((t, A, Ltot))
        if next_A is not None and A <= next_A:
            snaps.append((t, P.copy()))
            next_A -= snap_dA
    return np.array(hist), snaps


def parallels_on_dumbbell(N=2000):
    psi, L, _ = D.initial_profile(N)
    s = np.linspace(0, L, N + 1)
    ps = np.gradient(psi, s)
    crit = [k for k in range(2, N - 1) if (ps[k - 1] > 0) != (ps[k] > 0)]
    kinds = ["max" if ps[k - 1] > 0 else "min" for k in crit]
    return psi, L, s, ps, crit, kinds


if __name__ == "__main__":
    th = np.linspace(0, 2 * np.pi, 800, endpoint=False)
    r = 1 + 0.30 * np.cos(3 * th) + 0.15 * np.sin(5 * th)
    P0 = np.stack([r * np.cos(th), r * np.sin(th)], 1)
    hist, _ = csf_plane(P0, M=400)
    A0 = hist[0, 1]
    mid = hist[(hist[:, 1] < 0.8 * A0) & (hist[:, 1] > 0.2 * A0)]
    rate = np.polyfit(mid[:, 0], mid[:, 1], 1)[0]
    T = hist[-1, 0] + hist[-1, 1] / (2 * np.pi)
    iso = 4 * np.pi * hist[:, 1] / hist[:, 2] ** 2    # isoperimetric ratio, 1 = circle
    k_end = np.argmin(np.abs(hist[:, 1] - 0.05 * A0))
    print(f"plane: A0={A0:.6f}  dA/dt={rate:.5f} (-2pi={-2*np.pi:.5f})  "
          f"T_ext={T:.5f}  A0/2pi={A0/(2*np.pi):.5f}")
    print(f"plane: isoperimetric 4piA/L^2: start {iso[0]:.4f} -> at 5% area {iso[k_end]:.4f}")

    psi, L, s, ps, crit, kinds = parallels_on_dumbbell()
    for k, kd in zip(crit, kinds):
        print(f"dumbbell closed-geodesic parallel: s={s[k]:.4f} psi={psi[k]:.4f} ({kd} of psi"
              f" -> {'UNSTABLE' if kd=='max' else 'STABLE: CSF basin sink'})")
    # Gauss-Bonnet: total curvature pole -> each geodesic parallel
    K = -np.gradient(ps, s) / np.where(psi > 1e-9, psi, np.nan)
    dA = 2 * np.pi * psi
    for k in crit:
        tot = np.nansum((K * dA)[1:k] * np.diff(s)[: k - 1])
        print(f"  int K dA pole->s={s[k]:.3f} = {tot:.4f}   (2pi = {2*np.pi:.4f})")
    tot_all = np.nansum((K * dA)[1:-1] * np.diff(s)[1:])
    print(f"  int K dA whole surface = {tot_all:.4f}   (4pi = {4*np.pi:.4f})")
    # a parallel just on the neck side of the big equator flows to the neck and stops
    eq, nk = crit[0], crit[1]
    sp = s[eq] + 0.05
    t = 0.0
    dt = 1e-4
    for _ in range(200000):
        v = -np.interp(sp, s, ps) / np.interp(sp, s, psi)
        sp += dt * v
        t += dt
    print(f"parallel started at s={s[eq]+0.05:.3f}: after t={t:.1f} sits at s={sp:.4f} "
          f"(neck s={s[nk]:.4f}), length {2*np.pi*np.interp(sp, s, psi):.4f} "
          f"= 2pi*psi_neck {2*np.pi*psi[nk]:.4f} — never contracts")
    # a parallel on the pole side shrinks to the pole in finite time
    sp = s[eq] - 0.05
    t = 0.0
    while sp > 0.01:
        v = -np.interp(sp, s, ps) / np.interp(sp, s, psi)
        sp += 1e-5 * v
        t += 1e-5
    print(f"parallel started at s={s[eq]-0.05:.3f} (pole side): reaches the pole at t~{t:.4f}")
