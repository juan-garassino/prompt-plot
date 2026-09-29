"""The computation behind r06 (wildcard): 121 independent 2D Ising lattices, one per
temperature, each coarse-grained by iterated 3x3 majority rule (Kadanoff blocking).

Pure numpy, all randomness from one ``numpy.random.Generator`` seeded by the piece's
``SeededRNG``. The result is cached beside this file keyed by (seed, parameters)
because a full sample takes several minutes on this machine.

Temperature axis. The ray angle is linear in the Kramers-Wannier DUALITY variable

    u = K* - K,     exp(-2 K*) = tanh K,     K = J / T,

which is 0 exactly at Tc and flips sign under duality (T -> its dual temperature
maps u -> -u). So mirror rays about the zenith are exact Kramers-Wannier duals:
the plate's left/right symmetry is the model's self-duality, not a layout choice.

Exact Onsager results used for checks and for the crimson arch:
  * correlation length along an axis: xi^-1 = 2 u  (T > Tc),  4 |u|  (T < Tc)
    (amplitude ratio xi+/xi- = 2 at dual temperatures, exact);
  * internal energy per site  U = -coth 2K [1 + (2/pi)(2 tanh^2 2K - 1) K1(k)],
    k = 2 sinh 2K / cosh^2 2K;
  * spontaneous magnetisation m = (1 - sinh^-4 2K)^(1/8)  (T < Tc).

Sampler. Lattices with exact xi > XI_SW run vectorised Swendsen-Wang (FK bonds
p = 1 - exp(-2K) on satisfied bonds; clusters by hook-and-jump union on the bond
list; each cluster flipped with probability 1/2). The rest run vectorised
checkerboard Metropolis (their xi <= 3, so tau ~ xi^2.17 is a few sweeps). Cold
lattices start all-up, hot ones random. The cold sector is chosen UP: a cold
lattice whose final m < 0 is globally flipped (the Z2 symmetry, stated on the
sheet).
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
from pathlib import Path
from typing import Dict

import numpy as np

logger = logging.getLogger(__name__)

TC = 2.0 / math.log(1.0 + math.sqrt(2.0))  # 2.269185...
KC = 1.0 / TC

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- exact results


def dual_k(K: float) -> float:
    return -0.5 * math.log(math.tanh(K))


def u_of_k(K: float) -> float:
    return dual_k(K) - K


def k_of_u(u: float) -> float:
    """Invert u(K) = K* - K (strictly decreasing in K) by bisection."""
    lo, hi = 1e-4, 5.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if u_of_k(mid) > u:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def xi_exact(u: float) -> float:
    if u == 0:
        return math.inf
    return 1.0 / (2.0 * u) if u > 0 else 1.0 / (4.0 * -u)


def _ellipk(k: float) -> float:
    a, b = 1.0, math.sqrt(max(0.0, 1.0 - k * k))
    for _ in range(60):
        a, b = 0.5 * (a + b), math.sqrt(a * b)
    return math.pi / (2.0 * a)


def onsager_energy(K: float) -> float:
    """Internal energy per site, J = 1 (so -2 at T = 0)."""
    t2 = math.tanh(2 * K)
    kk = 2.0 * math.sinh(2 * K) / math.cosh(2 * K) ** 2
    kk = min(kk, 1.0 - 1e-15)
    return -(1.0 / t2) * (1.0 + (2.0 / math.pi) * (2.0 * t2 * t2 - 1.0) * _ellipk(kk))


def onsager_m(K: float) -> float:
    if K <= KC:
        return 0.0
    return (1.0 - math.sinh(2 * K) ** -4) ** 0.125


# ---------------------------------------------------------------- samplers


def _metropolis(s: np.ndarray, K: np.ndarray, sweeps: int, gen: np.random.Generator) -> None:
    """Vectorised checkerboard Metropolis over a stack of lattices (in place)."""
    M, L, _ = s.shape
    # L = 3^5 is ODD, so a 2-colour checkerboard is not an independent set across
    # the periodic seam. (i + 2j) mod 3 is: every neighbour differs by 1 or 2 mod 3,
    # and L divisible by 3 keeps it consistent across the wrap.
    assert L % 3 == 0
    ii, jj = np.indices((L, L))
    masks = [((ii + 2 * jj) % 3 == c) for c in (0, 1, 2)]
    # acceptance for dE = 2 s h, h in {-4,-2,0,2,4} -> dE/2 = s h in {-4..4}
    acc = np.exp(-2.0 * K[:, None] * np.array([-4, -2, 0, 2, 4])[None, :]).clip(max=1.0)
    acc = acc.astype(np.float32)
    for _ in range(sweeps):
        for mk in masks:
            h = (np.roll(s, 1, 1) + np.roll(s, -1, 1) + np.roll(s, 1, 2) + np.roll(s, -1, 2))
            sh = (s * h).astype(np.int64)  # in {-4,-2,0,2,4}
            p = np.take_along_axis(acc, ((sh + 4) // 2).reshape(M, -1), 1).reshape(M, L, L)
            flip = (gen.random((M, L, L), dtype=np.float32) < p) & mk[None]
            s[flip] *= -1


def _components(N: int, ei: np.ndarray, ej: np.ndarray) -> np.ndarray:
    f = np.arange(N, dtype=np.int64)
    while ei.size:
        ri, rj = f[ei], f[ej]
        act = ri != rj
        ei, ej, ri, rj = ei[act], ej[act], ri[act], rj[act]
        if not ei.size:
            break
        lo, hi = np.minimum(ri, rj), np.maximum(ri, rj)
        f[hi] = lo
        while True:
            g = f[f]
            if np.array_equal(g, f):
                break
            f = g
    return f


def _swendsen_wang(s: np.ndarray, K: np.ndarray, sweeps: int, gen: np.random.Generator) -> None:
    M, L, _ = s.shape
    N = M * L * L
    idx = np.arange(N, dtype=np.int64).reshape(M, L, L)
    nb = (np.arange(L) + 1) % L
    p = (1.0 - np.exp(-2.0 * K)).astype(np.float32)[:, None, None]
    for _ in range(sweeps):
        br = (s == s[:, :, nb]) & (gen.random(s.shape, dtype=np.float32) < p)
        bd = (s == s[:, nb, :]) & (gen.random(s.shape, dtype=np.float32) < p)
        ei = np.concatenate([idx[br], idx[bd]])
        ej = np.concatenate([idx[:, :, nb][br], idx[:, nb, :][bd]])
        root = _components(N, ei, ej)
        flip = gen.random(N, dtype=np.float32) < 0.5
        s *= np.where(flip[root], -1, 1).reshape(M, L, L).astype(np.int8)


def block_majority(s: np.ndarray) -> np.ndarray:
    """One Kadanoff step: 3x3 majority (odd block, never a tie). s: (M, L, L)."""
    M, L, _ = s.shape
    b = s.reshape(M, L // 3, 3, L // 3, 3).sum(axis=(2, 4), dtype=np.int32)
    return np.where(b > 0, 1, -1).astype(np.int8)


# ---------------------------------------------------------------- the sample


def sample(
    seed: int,
    n_rays: int = 121,
    u_max: float = 0.45,
    L: int = 243,
    levels: int = 4,
    xi_sw: float = 3.0,
    sw_sweeps: int = 90,
    met_sweeps: int = 120,
) -> Dict[str, np.ndarray]:
    params = dict(seed=seed, n_rays=n_rays, u_max=u_max, L=L, levels=levels,
                  xi_sw=xi_sw, sw_sweeps=sw_sweeps, met_sweeps=met_sweeps, v=4)
    key = hashlib.sha1(json.dumps(params, sort_keys=True).encode()).hexdigest()[:10]
    cache = HERE / f"cache_rg_s{seed}_{key}.npz"
    if cache.exists():
        d = np.load(cache)
        return {k: d[k] for k in d.files}

    gen = np.random.default_rng(seed)
    frac = np.linspace(-1.0, 1.0, n_rays)
    u = u_max * frac
    u[n_rays // 2] = 0.0
    K = np.array([k_of_u(x) for x in u])
    K[n_rays // 2] = KC
    xi = np.array([xi_exact(x) for x in u])

    s = np.empty((n_rays, L, L), dtype=np.int8)
    for j in range(n_rays):
        if u[j] < 0:
            s[j] = 1
        else:
            s[j] = np.where(gen.random((L, L)) < 0.5, 1, -1)
    near = xi > xi_sw
    far = ~near
    logger.info("rg sample: %d SW lattices, %d Metropolis lattices", near.sum(), far.sum())
    if far.any():
        sub = s[far]
        _metropolis(sub, K[far], met_sweeps, gen)
        s[far] = sub
    if near.any():
        sub = s[near]
        _metropolis(sub, K[near], 20, gen)
        _swendsen_wang(sub, K[near], sw_sweeps, gen)
        s[near] = sub

    # the cold sector is chosen UP
    m = s.reshape(n_rays, -1).mean(axis=1)
    flip = (u < 0) & (m < 0)
    s[flip] *= -1
    m = s.reshape(n_rays, -1).mean(axis=1)

    # energy per site: -(sum of right + down bond products) / N
    e = -(s * np.roll(s, -1, 2) + s * np.roll(s, -1, 1)).reshape(n_rays, -1).mean(axis=1)

    out: Dict[str, np.ndarray] = dict(u=u, K=K, xi=xi, m=m, e=e.astype(np.float64))
    lev = s
    for k in range(levels):
        out[f"lat{k}"] = np.packbits(lev.reshape(n_rays, -1) > 0, axis=1)
        out[f"shape{k}"] = np.array(lev.shape)
        out[f"mblk{k}"] = lev.reshape(n_rays, -1).mean(axis=1)
        if k < levels - 1:
            lev = block_majority(lev)
    np.savez_compressed(cache, **out)
    return out


def level_lattice(d: Dict[str, np.ndarray], k: int) -> np.ndarray:
    shp = tuple(int(x) for x in d[f"shape{k}"])
    n = shp[1] * shp[2]
    bits = np.unpackbits(d[f"lat{k}"], axis=1)[:, :n]
    return np.where(bits.reshape(shp) > 0, 1, -1).astype(np.int8)
