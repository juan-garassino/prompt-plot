"""The initial dumbbell 3-sphere: the warping profile psi(s) of an asymmetric peanut.

Drawn in the (z, rho) half-plane of its surface-of-revolution picture:

    rho(z) = sqrt(ELL^2 - z^2) * (ALPHA + BETA (z/ELL - ZETA_N)^2),   z in [-ELL, ELL]

sqrt(ELL^2 - z^2) is a round sphere (so both poles are smooth round caps); the quadratic
factor makes a waist at z = ZETA_N*ELL, offset so the left lobe is the larger. Chosen so
the initial metric has scalar curvature R > 0 everywhere and |psi_s| <= 1 (it embeds).
"""
from __future__ import annotations

import numpy as np

ELL = 2.0
ALPHA, BETA, ZETA_N = 0.16, 1.05, 0.18


def rho(z):
    return np.sqrt(np.clip(ELL**2 - z**2, 0, None)) * (ALPHA + BETA * (z / ELL - ZETA_N) ** 2)


def initial_profile(N=400, dense=400001):
    u = np.linspace(0, np.pi, dense)
    z = -ELL * np.cos(u)
    r = rho(z)
    r[0] = r[-1] = 0.0
    s = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(z), np.diff(r)))])
    L = s[-1]
    psi = np.interp(np.linspace(0, L, N + 1), s, r)
    return psi, L, (z, r)
