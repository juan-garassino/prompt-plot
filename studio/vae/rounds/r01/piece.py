"""VAE — LATENT BOTTLENECK (studio candidate, round 01).

The phenomenon, computed — not illustrated:

  A fixed saturating decoder ``g(z) = M tanh(z)`` (R2 -> R2) and a small set of
  data points on an open arc in data space.  Each datum gets a free diagonal
  Gaussian posterior ``q_i = N(mu_i, diag(sigma_i)^2)``.  We MAXIMIZE the exact
  ELBO with the reparameterization-trick estimator — the same fixed epsilon
  constellation that the drawing shows — by analytic gradient descent:

      F_i = 1/(2 gamma^2) * mean_s || x_i - g(mu_i + sigma_i . eps_s) ||^2
            + 1/2 sum_d ( sigma_id^2 + mu_id^2 - 1 - 2 ln sigma_id )

  dF/dz  = J(z)^T ( g(z) - x ) / gamma^2 ,  J(z) = M diag(1 - tanh(z)^2)
  dF/dmu = mean_s dF/dz + mu
  dF/dsig= mean_s (dF/dz . eps_s) + sigma - 1/sigma

  The converged (mu_i, sigma_i) ARE the drawing.  Nothing is placed by hand.

What it shows
  * The prior ``N(0,I)`` is drawn as its own energy surface: the paraboloid
    ``-log p(z) = 1/2 ||z||^2``.  Its rings are exact iso-KL contours in nats.
  * Every posterior is the SAME epsilon constellation, affinely copied by
    ``z = mu + sigma . eps``.  One master constellation sits on a flat
    ``N(0,I)`` target in the quiet zone; dotted correspondence lines tie three
    of its stars to the same three stars inside the hero cloud.
  * Where the decoder saturates the reconstruction term goes FLAT, so
    ``dF/dsigma = sigma - 1/sigma`` and sigma -> 1 exactly: the posterior
    relaxes to the prior and the channel carries ZERO bits.  That collapsed
    posterior is, by the arithmetic alone, the largest mass on the sheet — the
    hero.  Its red darts are the literal reparameterized samples.
  * The arc is open, so the chain of posteriors has a GAP: a wedge of bare
    paper the prior will happily sample from and no encoder ever visits.  The
    prior hole, left as blank paper.

Latent space under an isotropic prior is rotation invariant, so the display
rotation ``latent_rot_deg`` is a symmetry of the model, not a fudge.

Pens (nets/README.md colour law): black = structure (prior surface, type),
red = the active traced element (reparameterized samples + darts),
blue = the second perspective (the analytic posterior: sigma ellipses).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List, Optional, Tuple

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from promptplot.models import GCodeCommand  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402
from promptplot.generative.engine import PolarLOD, Scene3D, ScreenThin  # noqa: E402
from promptplot.generative.kit import (  # noqa: E402
    BLACK,
    BLUE,
    PINK,
    _dot,
    _pen,
    _spaced,
    _stroke_text,
    _text_width,
    dotted_circle,
    plus_mark,
    scale_footer,
    swatch_bar,
)

Bounds = Tuple[float, float, float, float]

# fixed decoder mixing matrix — the shear that makes the posteriors tilt
_M = ((1.18, 0.34), (-0.30, 0.96))


def studio_vae(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_post: int = 13,
    n_eps: int = 44,
    gamma: float = 0.21,
    arc_span: float = 236.0,
    arc_phase: float = -46.0,
    arc_r: float = 1.30,
    latent_rot_deg: float = 150.0,
    bowl_r: float = 3.2,
    bowl_gain: float = 0.42,
    steps: int = 900,
    lr: float = 0.055,
    dot_sep: float = 1.25,
    nr: int = 22,
    nth: int = 108,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """LATENT BOTTLENECK — a VAE's posteriors solved on the prior's energy bowl.

    The exact reparameterized ELBO is maximized by analytic gradient descent;
    the converged posteriors are stippled with the one epsilon constellation
    that trained them, the collapsed posterior (sigma -> 1, zero bits) becomes
    the hero mass, and the open arc leaves a wedge of prior with no posterior
    on it — blank paper as the hole.
    """
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, red, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    legend = _pen(3, colors) if colors >= 4 else black

    # ------------------------------------------------------------------ model
    M = np.array(_M, dtype=float)

    # the epsilon constellation: ONE seeded draw, centred + standardized so the
    # darts radiate from the true mean and the 1-sigma ellipse is honest.
    eps = np.array([[rng.gauss(), rng.gauss()] for _ in range(n_eps)])
    eps -= eps.mean(axis=0)
    eps /= eps.std(axis=0)

    # data: an OPEN elliptical arc in data space (the gap is the prior hole)
    th = np.radians(arc_phase + np.linspace(0.0, arc_span, n_post))
    X = np.stack([arc_r * np.cos(th), arc_r * 0.86 * np.sin(th)], axis=1)

    # init mu at the decoder's naive inverse, sigma at 0.5
    Minv = np.linalg.inv(M)
    mu = np.arctanh(np.clip(X @ Minv.T, -0.93, 0.93))
    rho = np.full((n_post, 2), math.log(0.5))

    g2 = gamma * gamma
    for k in range(steps):
        sig = np.exp(rho)
        z = mu[:, None, :] + sig[:, None, :] * eps[None, :, :]  # (N,S,2)
        t = np.tanh(z)
        resid = t @ M.T - X[:, None, :]  # g(z) - x
        dz = (1.0 - t * t) * (resid @ M) / g2  # J^T (g-x) / gamma^2
        dmu = dz.mean(axis=1) + mu
        dsig = (dz * eps[None, :, :]).mean(axis=1) + sig - 1.0 / sig
        step = lr * (1.0 - 0.6 * k / steps)
        mu -= step * dmu
        rho -= step * (dsig * sig)
        rho = np.clip(rho, -3.2, 0.06)

    sig = np.exp(rho)
    kl = 0.5 * (sig**2 + mu**2 - 1.0 - 2.0 * np.log(sig)).sum(axis=1)  # nats
    rate = float(kl.mean())
    hero = int(np.argmax(sig.prod(axis=1)))  # the widest posterior = fewest bits

    # display rotation (a symmetry of the isotropic prior)
    ca, sa = math.cos(math.radians(latent_rot_deg)), math.sin(math.radians(latent_rot_deg))
    R = np.array([[ca, -sa], [sa, ca]])
    mu = mu @ R.T
    epsR = eps @ R.T
    sigR = sig  # diagonal in the pre-rotation frame; rotate the axes instead
    AX = R @ np.diag([1.0, 0.0])  # unit axis 0 after rotation
    ax0 = R @ np.array([1.0, 0.0])
    ax1 = R @ np.array([0.0, 1.0])

    def zs_of(i: int) -> "np.ndarray":
        """The exact reparameterized samples of posterior i, display frame."""
        return mu[i][None, :] + (sig[i][None, :] * eps) @ R.T

    # ------------------------------------------------------------------ scene
    scene = Scene3D(rng, bounds, feed=feed, tip=0.5, px=(250, 340), pad=4.0, fit="rescue",
                    fit_pad=3.0)
    out = scene.out

    cx = x0 + 0.545 * W
    cy = y0 + 0.455 * H
    a = 0.415 * W / (bowl_r * math.sqrt(2.0))
    cd = 0.128 * H / (bowl_r * math.sqrt(2.0))
    bwy = 0.135 * H / (bowl_gain * 0.5 * bowl_r * bowl_r)

    def proj(wx: float, wy: float, wz: float) -> Tuple[float, float]:
        return (cx + (wx - wz) * a, cy + wy * bwy - (wx + wz) * cd)

    def depth(wx: float, wy: float, wz: float) -> float:
        return (wx + wz) + 0.12 * wy

    def energy(z0: float, z1: float) -> float:
        return bowl_gain * 0.5 * (z0 * z0 + z1 * z1)

    def lift(z0: float, z1: float):
        """latent point -> (sx, sy, dep); dep = HIDE beyond the bowl rim."""
        rr = math.hypot(z0, z1)
        wy = energy(z0, z1)
        sx, sy = proj(z0, wy, z1)
        if rr > bowl_r:
            return sx, sy, Scene3D.HIDE
        return sx, sy, depth(z0, wy, z1)

    # ------------------------------------------------- type (halos reserved first)
    xT = x0 + 0.024 * W
    epsx, epsy = x0 + 0.145 * W, y0 + 0.135 * H  # master N(0,I) target centre
    r_eps = 0.098 * W
    hz = zs_of(hero)
    hxy = proj(mu[hero][0], energy(*mu[hero]), mu[hero][1])

    scene.halo_labels(
        [
            (_spaced("LATENT"), xT, y1 - 7.0, 5.0, legend),
            (_spaced("BOTTLENECK"), xT, y1 - 15.4, 5.0, legend),
            (_spaced("THE CHANNEL IS AS WIDE AS THE NOISE ALLOWS"), xT, y1 - 21.6, 1.7, legend),
            (_spaced("Z  MU PLUS SIGMA TIMES EPSILON"), xT, y1 - 27.0, 1.7, red),
            (_spaced("N 0 I"), epsx - r_eps, epsy + r_eps + 5.6, 2.3, legend),
            (_spaced("ONE NOISE SET"), epsx - r_eps, epsy - r_eps - 5.0, 1.5, legend),
            (_spaced("COPIED EVERYWHERE"), epsx - r_eps, epsy - r_eps - 8.6, 1.5, legend),
            (_spaced("SIGMA %.2f" % float(sig[hero].max())), hxy[0] + 0.055 * W,
             hxy[1] + 0.075 * H, 2.1, blue),
            (_spaced("ZERO BITS"), hxy[0] + 0.055 * W, hxy[1] + 0.056 * H, 2.1, blue),
            (_spaced("PRIOR MASS"), x0 + 0.60 * W, y1 - 0.145 * H, 1.6, legend),
            (_spaced("NO POSTERIOR"), x0 + 0.60 * W, y1 - 0.163 * H, 1.6, legend),
        ]
    )

    # ------------------------------------------------------------- the prior bowl
    SX = np.zeros((nr + 1, nth + 1))
    SY = np.zeros((nr + 1, nth + 1))
    DEP = np.zeros((nr + 1, nth + 1))
    for i in range(nr + 1):
        rr = bowl_r * i / nr
        for j in range(nth + 1):
            aa = 2 * math.pi * j / nth
            wx, wz = rr * math.cos(aa), rr * math.sin(aa)
            wy = energy(wx, wz)
            SX[i, j], SY[i, j] = proj(wx, wy, wz)
            DEP[i, j] = depth(wx, wy, wz)

    lod = PolarLOD(
        levels=((12, 0.0), (6, 0.26), (3, 0.52), (1, 0.74)),
        ring_start=3,
        ring_skip_inner=0.32,
        ridge_every=nth // 4,
        ridge_half=nth // 8,
    )
    scene.surface(SX, SY, DEP, pen=black, lod=lod, thin=ScreenThin(gap_mm=1.15, far_mult=2.1))

    # ---------------------------------------------------------------- posteriors
    occ = scene.occupancy(dot_sep)
    order = sorted(range(n_post), key=lambda i: -float(sig[i].prod()))

    def ellipse(i: int, c: float):
        pts = []
        for k in range(97):
            tt = 2 * math.pi * k / 96
            d = (sig[i][0] * c * math.cos(tt)) * ax0 + (sig[i][1] * c * math.sin(tt)) * ax1
            sx, sy, dp = lift(mu[i][0] + d[0], mu[i][1] + d[1])
            pts.append((sx, sy, dp, blue))
        return pts

    for i in order:
        # the analytic posterior: 1-sigma solid, 2-sigma solid, 3-sigma for the hero
        scene.lines([ellipse(i, 1.0), ellipse(i, 2.0)], mode="over")
        if i == hero:
            scene.lines([ellipse(i, 3.0)], mode="over")
        # the realized samples: the SAME constellation, moved and stretched
        for z0, z1 in zs_of(i):
            sx, sy, dp = lift(z0, z1)
            if dp == Scene3D.HIDE or not scene.visible(sx, sy, dp) or scene._blocked(sx, sy):
                continue
            if occ.crowded(sx, sy):
                continue
            occ.add(sx, sy)
            out.extend(_dot(sx, sy, 0.42, color=red, f=feed))
        # the mean: a small cross, on the structural pen
        mx, my, mdep = lift(mu[i][0], mu[i][1])
        if mdep != Scene3D.HIDE and scene.visible(mx, my, mdep):
            out.extend(plus_mark(mx, my, s=1.15, pen=black, f=feed))

    # ------------------------------------------- the hero: reparameterization darts
    darts = []
    hmx, hmy, hmdep = lift(mu[hero][0], mu[hero][1])
    for z0, z1 in hz:
        sx, sy, dp = lift(z0, z1)
        if dp == Scene3D.HIDE:
            continue
        # leave the core as blank paper: the dart starts 34% out
        for u0, u1 in ((0.34, 0.94),):
            ax = hmx + (sx - hmx) * u0
            ay = hmy + (sy - hmy) * u0
            bx = hmx + (sx - hmx) * u1
            by = hmy + (sy - hmy) * u1
            darts.append([(ax, ay, hmdep, red), (bx, by, dp, red)])
    scene.lines(darts, mode="over")

    # ------------------------------------------------ the master N(0,I) constellation
    # exact chi-2 coverage radii for 2 dof: r = sqrt(-2 ln(1-p))
    for p in (0.50, 0.90, 0.99):
        rp = math.sqrt(-2.0 * math.log(1.0 - p))
        out.extend(dotted_circle(epsx, epsy, r_eps * rp / 3.0345, pen=blue, bounds=bounds, f=feed))
    occ_e = scene.occupancy(dot_sep)
    for ex, ey in epsR:
        sx, sy = epsx + ex * r_eps / 3.0345, epsy + ey * r_eps / 3.0345
        if scene._blocked(sx, sy) or occ_e.crowded(sx, sy):
            continue
        occ_e.add(sx, sy)
        out.extend(_dot(sx, sy, 0.42, color=red, f=feed))
    out.extend(plus_mark(epsx, epsy, s=1.15, pen=black, f=feed))

    # dotted correspondence lines: three named stars, same constellation, moved
    def dotted(p0, p1, pen):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        n = max(8, int(L / 3.6))
        for q in range(0, n, 2):
            aa = (p0[0] + (p1[0] - p0[0]) * q / n, p0[1] + (p1[1] - p0[1]) * q / n)
            bb = (p0[0] + (p1[0] - p0[0]) * (q + 0.5) / n, p0[1] + (p1[1] - p0[1]) * (q + 0.5) / n)
            scene.poly([aa, bb], pen=pen)

    picks = list(np.argsort(-np.hypot(eps[:, 0], eps[:, 1]))[:3])
    for idx in picks:
        sx, sy = epsx + epsR[idx][0] * r_eps / 3.0345, epsy + epsR[idx][1] * r_eps / 3.0345
        tx, ty, tdep = lift(hz[idx][0], hz[idx][1])
        if tdep == Scene3D.HIDE:
            continue
        dotted((sx, sy), (tx, ty), black)
        out.extend(_dot(tx, ty, 0.8, color=blue, f=feed))

    # ----------------------------------------------------------------- furniture
    # two iso-KL ring labels straight off the prior surface (nats = r^2 / 2)
    for rr, tag in ((1.0, "0.5 NATS"), (2.0, "2.0 NATS")):
        lx, ly = proj(-rr * 0.9239, energy(rr * 0.9239, rr * 0.3827), rr * 0.3827)
        out.extend(_stroke_text(_spaced(tag), lx - 12.0, ly + 1.4, 1.4, color=legend, f=feed))

    out.extend(swatch_bar(x1 - 8.4, y1 - 5.0, [black, red, blue], size=2.4, f=feed))
    out.extend(
        _stroke_text(
            _spaced("RATE %.2f NATS PER SAMPLE" % rate), xT, y0 + 4.2, 1.8, color=legend, f=feed
        )
    )
    out.extend(scale_footer(bounds, text="GAMMA %.2f" % gamma, pen=legend, height=1.8, f=feed))

    return scene.render()
