"""FORM FROM NOISE — diffusion drawn as the transport it actually is.

The phenomenon, not the apparatus: a variance-preserving diffusion model is a
DETERMINISTIC map from the Gaussian prior onto the data manifold.  For a
Gaussian-mixture data law that map is available in closed form, so the whole
plate is computed, never illustrated:

* forward marginal  p_t(x) = SUM_i w_i N(x ; sqrt(abar_t) mu_i , 1-abar_t+abar_t s0^2)
  is EXACT (a Gaussian mixture stays a Gaussian mixture under convolution),
  with the standard VP schedule beta(t) = 0.1 + t (20 - 0.1) of Song et al.
* the score  d/dx log p_t  is therefore exact too (responsibility-weighted),
* the probability-flow ODE  dx/dt = -0.5 beta(t) [ x + score(x,t) ]  is
  integrated with RK4 — that IS a deterministic DDIM/ODE sampler,
* the forward SDE  dx = -0.5 beta x dt + sqrt(beta) dW  is a real seeded
  Euler-Maruyama path (blue, jagged) against its exact +-2 sigma envelope.

THE DRAWING IS THE MESH.  The surface is the density landscape over
(x, log-SNR): a single broad prior hill at the back that shatters into three
needles at the front.  Its ROW lines are the time slices p_t; its COLUMN lines
ARE the sampler trajectories.  Nothing is overlaid on the terrain — the
wireframe and the mechanism are the same object.

Where two trajectories straddle a separatrix the mesh opens a canyon of blank
paper whose floor is inked red: the undecided region of noise space, the exact
knife-edge at which the sample changes its mind about which mode it will become.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

import numpy as np

from promptplot.generative.engine import Scene3D, ScreenThin
from promptplot.generative.kit import (
    _dot,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    plus_mark,
    scale_footer,
    swatch_bar,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

B_MIN, B_MAX = 0.1, 20.0  # VP-SDE linear schedule (Song et al. 2021 defaults)


def diffusion_transport(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    modes: Tuple[float, ...] = (-0.66, -0.05, 0.58),
    weights: Tuple[float, ...] = (0.22, 0.47, 0.31),
    sigma0: float = 0.10,
    t_end: float = 0.015,
    n_rows: int = 46,
    n_cols: int = 108,
    n_prior: int = 140,
    substeps: int = 4,
    canyon: float = 0.020,
    n_forward: int = 3,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """FORM FROM NOISE — the reverse diffusion process as an exact transport
    map from the Gaussian prior onto a three-mode data manifold."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blk = 0 if colors > 1 else None
    red = (1 % colors) if colors > 1 else None
    blu = (2 % colors) if colors > 1 else None
    txt = 3 if colors >= 4 else blk

    # ---------------------------------------------------------------- schedule
    def beta(t: float) -> float:
        return B_MIN + t * (B_MAX - B_MIN)

    def abar(t: float) -> float:
        return math.exp(-0.5 * B_MIN * t - 0.25 * (B_MAX - B_MIN) * t * t)

    def logsnr(t: float) -> float:
        a = min(abar(t), 1.0 - 1e-15)
        return math.log(a / (1.0 - a))

    def t_of_logsnr(lam: float) -> float:
        lo, hi = 1e-7, 1.0  # logsnr is strictly decreasing in t
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if logsnr(mid) > lam:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    def moments(t: float) -> Tuple[float, float]:
        a = abar(t)
        return math.sqrt(a), (1.0 - a) + a * sigma0 * sigma0

    def dens(u: float, t: float) -> float:
        s, v = moments(t)
        n = 1.0 / math.sqrt(2.0 * math.pi * v)
        return sum(w * n * math.exp(-((u - s * m) ** 2) / (2 * v)) for m, w in zip(modes, weights))

    def score(u: float, t: float) -> float:
        """d/du log p_t(u) — exact, responsibility weighted."""
        s, v = moments(t)
        num = 0.0
        den = 0.0
        for m, w in zip(modes, weights):
            e = w * math.exp(-((u - s * m) ** 2) / (2 * v))
            num += e * (s * m - u) / v
            den += e
        return num / den if den > 1e-300 else 0.0

    def flow(u: float, t: float) -> float:
        """probability-flow ODE right-hand side, du/dt."""
        return -0.5 * beta(t) * (u + score(u, t))

    # ------------------------------------------------------- the (x, logSNR) grid
    lam_far, lam_near = logsnr(1.0), logsnr(t_end)
    TS = [t_of_logsnr(lam_near + (lam_far - lam_near) * k / n_rows) for k in range(n_rows + 1)]
    TS[0], TS[-1] = t_end, 1.0  # k = 0 near (data), k = n_rows far (prior)

    def integrate(u_far: float) -> List[float]:
        """RK4 down the probability-flow ODE, one sample per row."""
        us = [0.0] * (n_rows + 1)
        u = u_far
        us[n_rows] = u
        for k in range(n_rows, 0, -1):
            ta, tb = TS[k], TS[k - 1]
            h = (tb - ta) / substeps
            t = ta
            for _ in range(substeps):
                k1 = flow(u, t)
                k2 = flow(u + 0.5 * h * k1, t + 0.5 * h)
                k3 = flow(u + 0.5 * h * k2, t + 0.5 * h)
                k4 = flow(u + h * k3, t + h)
                u += h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
                t += h
            us[k - 1] = u
        return us

    def arrival(u_far: float) -> int:
        u = integrate(u_far)[0]
        return min(range(len(modes)), key=lambda i: abs(u - modes[i]))

    # the separatrices: the exact noise values at which the sample changes mode
    seps: List[float] = []
    for i in range(len(modes) - 1):
        lo, hi = -3.0, 3.0
        while arrival(lo) > i:
            lo -= 1.0
        while arrival(hi) <= i:
            hi += 1.0
        for _ in range(46):
            mid = 0.5 * (lo + hi)
            if arrival(mid) <= i:
                lo = mid
            else:
                hi = mid
        seps.append(0.5 * (lo + hi))

    def phi(z: float) -> float:
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

    edges = [-1e9] + seps + [1e9]
    pushed = [phi(edges[i + 1]) - phi(edges[i]) for i in range(len(modes))]

    def valley(k: int, i: int, ul: float, ur: float) -> float:
        """The canyon floor: the density's local minimum (score = 0) between
        modes i and i+1 where the mixture is still multimodal; above the
        bifurcation it falls back to the straddling pair's midpoint."""
        t = TS[k]
        s, _v = moments(t)
        a, b = s * modes[i], s * modes[i + 1]
        if score(a, t) < 0.0 < score(b, t) or score(a, t) * score(b, t) > 0.0:
            return 0.5 * (ul + ur)
        for _ in range(40):
            mid = 0.5 * (a + b)
            if score(mid, t) > 0.0:
                a = mid
            else:
                b = mid
        return 0.5 * (a + b)

    # --------------------------------------------------------------- columns
    s_far, v_far = moments(1.0)
    u_far_max = max(abs(s_far * m) for m in modes) + 3.0 * math.sqrt(v_far)
    uni = [-u_far_max + 2.0 * u_far_max * j / n_cols for j in range(n_cols + 1)]
    special = [u for us in seps for u in (us - canyon, us, us + canyon)]
    uni = [u for u in uni if all(abs(u - s) > 1.35 * canyon for s in seps)]
    cols = sorted(uni + special)
    red_cols = {j for j, u in enumerate(cols) if any(abs(u - s) <= canyon + 1e-12 for s in seps)}
    mid_cols = {j: i for j, u in enumerate(cols) for i, s in enumerate(seps) if abs(u - s) < 1e-12}
    NC = len(cols) - 1

    U = [integrate(u) for u in cols]  # U[j][k] = x at row k of trajectory j
    for j, i in mid_cols.items():
        for k in range(n_rows + 1):
            U[j][k] = valley(k, i, U[j - 1][k], U[j + 1][k])

    # ------------------------------------------------------------ projection
    XS = 0.1480 * W  # paper mm per unit of data space x
    SKX = -0.075 * W  # the far edge slides left (oblique recession)
    cx = x0 + 0.532 * W
    cyN = y0 + 0.150 * H  # the near edge (t -> 0) baseline
    DY = 0.585 * H  # far edge rise
    pmax = max(dens(m, t_end) for m in modes)
    HY = 0.270 * H / pmax  # paper mm per unit of probability density

    def rho(k: int) -> float:
        return k / n_rows

    def sx(u: float, k: int) -> float:
        return cx + u * XS + rho(k) * SKX

    def sy(h: float, k: int) -> float:
        return cyN + rho(k) * DY + h * HY

    def dep(k: int) -> float:
        return 1.0 - rho(k)

    def drape(us: List[float], pen, kk: Optional[List[int]] = None):
        ks = kk if kk is not None else list(range(n_rows + 1))
        return [(sx(us[k], k), sy(dens(us[k], TS[k]), k), dep(k), pen) for k in ks]

    scene = Scene3D(rng, bounds, feed=feed, px=(260, 240), tip=0.5, fit="rescue", fit_pad=3.0)

    SXa = np.zeros((n_rows + 1, NC + 1))
    SYa = np.zeros((n_rows + 1, NC + 1))
    DEa = np.zeros((n_rows + 1, NC + 1))
    PVa = np.full((n_rows + 1, NC + 1), blk if blk is not None else 0)
    for k in range(n_rows + 1):
        for j in range(NC + 1):
            u = U[j][k]
            SXa[k, j] = sx(u, k)
            SYa[k, j] = sy(dens(u, TS[k]), k)
            DEa[k, j] = dep(k)
            if j in red_cols:
                PVa[k, j] = red if red is not None else 0

    # ------------------------------------------------------------ annotation
    sum_i = [int(np.argmax([dens(m, t_end) for m in modes]))]
    peak_x = [sx(m, 0) for m in modes]
    peak_y = [sy(dens(m, t_end), 0) for m in modes]
    far_top = sy(dens(0.0, 1.0), n_rows)
    Lx = x0 + 0.020 * W

    labels = [
        (_spaced("T 1.00  GAUSSIAN PRIOR"), Lx, far_top + 0.028 * H, 1.8, txt),
        (_spaced("N 0 1"), Lx, far_top + 0.012 * H, 1.5, txt),
        (
            _spaced("REVERSE  PROBABILITY FLOW ODE"),
            x1 - 0.365 * W,
            far_top - 0.055 * H,
            1.6,
            txt,
        ),
        (
            _spaced("EVERY COLUMN IS ONE SAMPLER PATH"),
            x1 - 0.365 * W,
            far_top - 0.073 * H,
            1.3,
            txt,
        ),
        (_spaced("FORWARD SDE"), x0 + 0.045 * W, cyN + 0.335 * H, 1.6, blu),
        (_spaced("NOISE DESTROYS"), x0 + 0.045 * W, cyN + 0.317 * H, 1.3, blu),
        (_spaced("SEPARATRIX"), sx(seps[-1], 6) + 0.020 * W, sy(0.0, 6) + 0.052 * H, 1.6, red),
        (
            _spaced("THE UNDECIDED PATH"),
            sx(seps[-1], 6) + 0.020 * W,
            sy(0.0, 6) + 0.034 * H,
            1.3,
            red,
        ),
        (_spaced("MODE IS CHOSEN AT T 0.12"), Lx, cyN + 0.395 * H, 1.3, txt),
    ]
    for i, m in enumerate(modes):
        labels.append((f"{pushed[i]:.2f}", peak_x[i] - 3.0, peak_y[i] + 0.012 * H, 2.0, txt))
    labels.append((_spaced("T 0.015  DATA MANIFOLD"), Lx, cyN - 0.030 * H, 1.8, txt))
    scene.halo_labels(labels)

    # ------------------------------------------------------------------ draw
    scene.surface(SXa, SYa, DEa, pens=PVa, thin=ScreenThin(gap_mm=0.9, far_mult=2.2))

    # the forward process: seeded Euler-Maruyama paths + the exact +-2 sigma cone
    x_src = modes[0]
    fwd: List[List[Tuple[float, float, float, object]]] = []
    for _p in range(n_forward):
        u = x_src
        us = [u]
        for k in range(n_rows):
            ta, tb = TS[k], TS[k + 1]
            h = (tb - ta) / substeps
            t = ta
            for _ in range(substeps):
                u += -0.5 * beta(t) * u * h + math.sqrt(beta(t) * h) * rng.gauss(0.0, 1.0)
                t += h
            us.append(u)
        fwd.append(drape(us, blu))
    for sgn in (-1.0, 1.0):
        env = []
        for k in range(n_rows + 1):
            s, _v = moments(TS[k])
            env.append(s * x_src + sgn * 2.0 * math.sqrt(1.0 - abar(TS[k])))
        pts = drape(env, blu)
        for q in range(0, len(pts) - 2, 3):  # dotted: the envelope is a statistic
            fwd.append(pts[q : q + 2])
    scene.lines(fwd, mode="over")

    # the prior: 140 real N(0,1) draws as a jittered stipple band on the plain
    hits = [0] * len(modes)
    for _i in range(n_prior):
        z = rng.gauss(0.0, 1.0)
        while abs(z) > 0.97 * u_far_max:
            z = rng.gauss(0.0, 1.0)
        hits[min(i for i in range(len(modes)) if z <= edges[i + 1])] += 1
        scene.emit(
            _dot(
                sx(z, n_rows),
                sy(dens(z, 1.0), n_rows) + 1.8 + 7.0 * rng.random(),
                r=0.45,
                color=blk,
                f=feed,
            )
        )
    for s in seps:  # the two knife points in noise space
        scene.emit(plus_mark(sx(s, n_rows), sy(dens(s, 1.0), n_rows) + 5.0, s=1.6, pen=red, f=feed))

    # axonometric registration: dotted droplines, never arrows
    base = sy(0.0, 0)
    for i in range(len(modes)):
        px, py = peak_x[i], peak_y[i]
        n = max(6, int((py - base) / 3.2))
        for q in range(n):
            a = base + (py - base) * q / n
            scene.poly([(px, a), (px, a + (py - base) * 0.45 / n)], pen=blk)
    scene.poly([(sx(-u_far_max * 0.33, 0), base), (sx(u_far_max * 0.33, 0), base)], pen=blk)

    out = scene.out
    out += _stroke_text(_spaced("FORM FROM NOISE"), Lx, y1 - 0.042 * H, 3.4, color=txt, f=feed)
    out += _stroke_text(
        _spaced("THE PRIOR ALREADY CONTAINS THE PICTURE"),
        Lx,
        y1 - 0.068 * H,
        1.7,
        color=txt,
        f=feed,
    )
    out += _stroke_text(
        _spaced(f"{n_prior} SAMPLES   {hits[0]} {hits[1]} {hits[2]}"),
        Lx,
        y0 + 0.052 * H,
        1.6,
        color=txt,
        f=feed,
    )
    out += _stroke_text(
        _spaced("VP SDE  BETA 0.1 - 20.0   RK4 ON THE PROBABILITY FLOW"),
        Lx,
        y0 + 0.030 * H,
        1.4,
        color=txt,
        f=feed,
    )
    out += swatch_bar(x1 - 8.5, y0 + 0.075 * H, [blk, red, blu], size=2.4, f=feed)
    out += scale_footer(bounds, text="PUSHFORWARD MASS", pen=txt, height=2.0, f=feed)
    return scene.render()
