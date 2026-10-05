"""A vectorised numpy zeta(s) for the X-ray grid -- validated against mpmath (see compute_abstract.py).

Why: the studio machine was running ~390 load when this round was built; mpmath.fp.zeta at
~1 ms per point would have taken hours for the 3.1 M-point abstract grid. This is the textbook
method, not an approximation of convenience:

  Re s >= 1/2 : Euler-Maclaurin summation,  N = 100 terms, M = 24 Bernoulli corrections
                zeta(s) = sum_{n<N} n^-s + N^(1-s)/(s-1) + N^-s/2
                          + sum_k B_2k/(2k)! * s(s+1)...(s+2k-2) * N^(-s-2k+1)
  Re s <  1/2 : the functional equation zeta(s) = chi(s) zeta(1-s),
                chi(s) = 2^s pi^(s-1) sin(pi s/2) Gamma(1-s), evaluated in logs;
                log Gamma by Stirling (12 terms) after shifting Re z >= 25.
Error vs mpmath (dps 30) on 4000 random points of the window is printed by compute_abstract.py.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np


def _bernoulli(n: int) -> list:
    A = [Fraction(0)] * (n + 1)
    B = []
    for m in range(n + 1):
        A[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
        B.append(A[0])  # B_m (B_1 = +1/2 convention, unused)
    return B


_B = _bernoulli(60)
_M = 24
_N = 100
_EM = [float(_B[2 * k] / math.factorial(2 * k)) for k in range(1, _M + 1)]
_ST = [float(_B[2 * k] / (2 * k * (2 * k - 1))) for k in range(1, 13)]


def _zeta_right(s: np.ndarray) -> np.ndarray:
    """Euler-Maclaurin, valid for Re s >= 1/2 (and far beyond)."""
    s = np.asarray(s, dtype=complex)
    out = np.zeros_like(s)
    for n in range(1, _N):
        out += np.exp(-s * math.log(n))
    lnN = math.log(_N)
    Ns = np.exp(-s * lnN)  # N^-s
    out += _N * Ns / (s - 1.0) + 0.5 * Ns
    poch = s.copy()  # s(s+1)...(s+2k-2), k = 1
    Npow = Ns / _N  # N^(-s-1)
    for k in range(1, _M + 1):
        out += _EM[k - 1] * poch * Npow
        poch = poch * (s + 2 * k - 1) * (s + 2 * k)
        Npow = Npow / (_N * _N)
    return out


def _loggamma(z: np.ndarray) -> np.ndarray:
    """log Gamma(z) up to a multiple of 2 pi i (irrelevant: it is exponentiated)."""
    z = np.asarray(z, dtype=complex)
    shift = np.zeros_like(z)
    w = z.copy()
    for _ in range(40):
        m = w.real < 25.0
        if not m.any():
            break
        shift[m] += np.log(w[m])
        w[m] = w[m] + 1.0
    lg = (w - 0.5) * np.log(w) - w + 0.5 * math.log(2 * math.pi)
    wi = 1.0 / w
    w2 = wi * wi
    p = wi.copy()
    for c in _ST:
        lg += c * p
        p = p * w2
    return lg - shift


def zeta(s: np.ndarray) -> np.ndarray:
    s = np.asarray(s, dtype=complex)
    out = np.empty_like(s)
    r = s.real >= 0.5
    if r.any():
        out[r] = _zeta_right(s[r])
    l = ~r
    if l.any():
        sl = s[l]
        logchi = (sl * math.log(2.0) + (sl - 1.0) * math.log(math.pi)
                  + np.log(np.sin(math.pi * sl / 2.0)) + _loggamma(1.0 - sl))
        out[l] = np.exp(logchi) * _zeta_right(1.0 - sl)
    return out
