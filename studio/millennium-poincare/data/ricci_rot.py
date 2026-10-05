"""Rotationally symmetric Ricci flow on S^{n+1}  (n=2 -> the 3-sphere), arc-length gauge.

Metric  g = ds^2 + psi(s,t)^2 g_{S^n},  s in [0, L(t)],  psi(0)=psi(L)=0.
Ricci flow dg/dt = -2 Ric, in a fixed coordinate x (Angenent & Knopf, Math. Res. Lett.
11 (2004) 493-518, eq. for the warped product):

    psi_t|_x = psi_ss - (n-1)(1 - psi_s^2)/psi        d(ds)/dt = n (psi_ss/psi) ds

Rewritten on the normalised arc-length grid xi = s/L in [0,1] (removes the degenerate
phi-equation and its pole instability):

    psi_t|_xi = psi_ss - (n-1)(1-psi_s^2)/psi - psi_s Q(s) + psi_s xi L_t,
    Q(s) = int_0^s n psi_ss/psi ds',   L_t = Q(L).

n=1 is 2-D Ricci flow on S^2 (the pinching term vanishes); n=2 is the 3-manifold case.
Pure numpy, explicit, adaptive dt. Validated on the round sphere: r^2 = r0^2 - 2 n t.
"""
from __future__ import annotations

import numpy as np

POLE_FIT = 4  # nodes next to each pole whose psi_ss/psi comes from an even fit


def _d(psi, L):
    N = len(psi) - 1
    ds = L / N
    ps = np.gradient(psi, ds, edge_order=2)
    pss = np.empty_like(psi)
    pss[1:-1] = (psi[2:] - 2 * psi[1:-1] + psi[:-2]) / ds**2
    pss[0] = pss[-1] = 0.0  # unused at the poles (psi=0 there)
    return ds, ps, pss


def rhs(psi, L, n):
    N = len(psi) - 1
    ds, ps, pss = _d(psi, L)
    p = psi[1:-1]
    q = np.empty_like(psi)
    q[1:-1] = n * pss[1:-1] / p
    # psi_ss/psi is smooth and EVEN about each pole but ill-conditioned next to it
    # (0/0); replace the first M nodes by an even fit c0 + c2 s^2 from nodes M..M+3.
    M = POLE_FIT
    k = np.arange(M, M + 4, dtype=float)
    A = np.stack([np.ones_like(k), (k * ds) ** 2], 1)
    P = np.linalg.pinv(A)
    near = (np.arange(0, M) * ds) ** 2
    cl = P @ q[M:M + 4]
    cr = P @ q[N - M - 3:N - M + 1][::-1]
    q[:M] = cl[0] + cl[1] * near
    q[N - M + 1:] = (cr[0] + cr[1] * near)[::-1]
    Q = np.concatenate([[0.0], np.cumsum(0.5 * (q[1:] + q[:-1]) * ds)])
    Lt = Q[-1]
    xi = np.linspace(0, 1, N + 1)
    dpsi = np.zeros_like(psi)
    dpsi[1:-1] = (pss[1:-1] - (n - 1) * (1 - ps[1:-1] ** 2) / p
                  - ps[1:-1] * Q[1:-1] + ps[1:-1] * xi[1:-1] * Lt)
    return dpsi, Lt, ds


def step(psi, L, n, cfl=0.2):
    dpsi, Lt, ds = rhs(psi, L, n)
    pmin = np.min(psi[1:-1])
    dt = cfl * min(ds * ds, pmin * pmin)
    return psi + dt * dpsi, L + dt * Lt, dt


def scalar_curvature(psi, L, n):
    ds, ps, pss = _d(psi, L)
    p = psi[1:-1]
    return -2 * n * pss[1:-1] / p + n * (n - 1) * (1 - ps[1:-1] ** 2) / p**2


def embed(psi, L):
    """(z, rho) profile of the surface of revolution drawn for it (needs |psi_s|<=1)."""
    N = len(psi) - 1
    ds, ps, _ = _d(psi, L)
    dz = np.sqrt(np.clip(1 - ps**2, 0, None))
    z = np.concatenate([[0.0], np.cumsum(0.5 * (dz[1:] + dz[:-1]) * ds)])
    return z, psi.copy()


def resample(psi, L, N):
    s_old = np.linspace(0, L, len(psi))
    s_new = np.linspace(0, L, N + 1)
    return np.interp(s_new, s_old, psi)


if __name__ == "__main__":
    for n in (1, 2):
        N = 200
        xi = np.linspace(0, 1, N + 1)
        L = np.pi
        psi = np.sin(np.pi * xi)
        t = 0.0
        T = 1.0 / (2 * n)
        while t < 0.75 * T:
            psi, L, dt = step(psi, L, n)
            t += dt
        r = np.max(psi)
        print(f"n={n}: t={t:.5f}  r^2={r*r:.6f}  exact 1-2nt={1-2*n*t:.6f}  L/r={L/r:.6f}")
