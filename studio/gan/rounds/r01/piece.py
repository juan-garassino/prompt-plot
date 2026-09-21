"""GAN — THE ADVERSARIAL MINIMAX DUEL.  Studio candidate, round 01.

Contract (promptplot/studio/loop.py:_render_code_payload):

    minimax_duel(rng: SeededRNG, bounds, colors: int = 3) -> list[GCodeCommand]

WHAT IS ACTUALLY COMPUTED
-------------------------
The Dirac-GAN (Mescheder/Geiger/Nowozin 2018, *Which Training Methods for GANs
do actually Converge?*) — the smallest GAN that still has the whole pathology:

    real data   x ~ delta_0                 (a point mass at the origin)
    generator   p_theta = delta_theta        (one parameter: where the fake sits)
    discriminator D_psi(x) = psi * x         (one parameter: the slope)
    objective   V(theta, psi) = f(psi*theta) + f(0),   f(t) = -log(1 + e^-t)

V depends on the two players ONLY through the product s = psi*theta, so the
minimax objective is an EXACT saddle: a hyperbolic surface, high where the
discriminator wins (s > 0) and plunging where the generator wins (s < 0).  That
surface IS the arena drawn here — no illustration, the height of every mesh
vertex is f(psi*theta).

Simultaneous gradient descent-ascent on it:

    theta <- theta - h * psi * f'(s)        (generator descends)
    psi   <- psi   + h * theta * f'(s)      (discriminator ascends)

with f'(s) = sigmoid(-s).  Two exact facts drive the whole composition:

  * CONTINUOUS TIME CONSERVES theta^2 + psi^2 exactly
    (d/dt (theta^2+psi^2) = 2*theta*(-psi*g) + 2*psi*(theta*g) = 0):
    the honest game is a CLOSED ORBIT — it never converges, it circles.
  * THE DISCRETE STEP GROWS THE RADIUS BY EXACTLY sqrt(1 + h^2 g^2):
    r_{n+1}^2 = (theta - h psi g)^2 + (psi + h theta g)^2 = (1 + h^2 g^2) r_n^2.
    Training does not merely fail to converge — it provably spirals OUT.

The unique Nash equilibrium (0, 0) is therefore never reached, from any start.
It is drawn as the only thing on the sheet made of pure paper: a circular hole
in the surface itself.

Each iteration is drawn as its two players' moves separately — a horizontal
leg (the generator changing theta) and a vertical leg (the discriminator
changing psi), whose corner is the counterfactual "if only one had moved".
Their sum is exactly the simultaneous update, so the staircase is the scheme,
not a stylisation of it.  Leg length is |h*psi*g| / |h*theta*g|, so the ink
density IS the gradient magnitude: long confident flights where the players
disagree, a bunched crawl along the saturated diagonals where f'(s) -> 0 and
the generator's gradient vanishes (Goodfellow 2014's saturating loss).
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import PolarLOD, Scene3D, ScreenThin
from promptplot.generative.kit import (
    BLACK,
    BLUE,
    PINK,
    _dot,
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    plus_mark,
    scale_footer,
    swatch_bar,
    type_block,
)

Bounds = Tuple[float, float, float, float]


# ---------------------------------------------------------------------------
# the mathematics (exact; no numpy needed for the scalar path)
# ---------------------------------------------------------------------------


def _sigmoid(t: float) -> float:
    if t >= 0.0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def _V(s: float) -> float:
    """f(s) = -log(1 + e^-s): the Dirac-GAN objective as a function of psi*theta."""
    return -math.log1p(math.exp(-s)) if s > -35.0 else s


def _grad_mag(s: float) -> float:
    """f'(s) = sigmoid(-s) — the shared gradient magnitude of BOTH players."""
    return _sigmoid(-s)


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def minimax_duel(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    step: float = 0.26,           # h — the shared learning rate of both players
    r_start: float = 0.74,        # initial ||(theta, psi)||
    r_arena: float = 3.30,        # radius of the drawn objective surface
    r_void: float = 0.60,         # radius of the equilibrium hole (blank paper)
    max_iters: int = 900,
    nr: int = 42,                 # surface rings
    na: int = 128,                # surface angular samples (multiple of 8)
    z_gain: float = 0.44,         # vertical relief of the saddle
    ax: float = 1.00,             # axonometric: theta-axis spread
    az: float = 0.62,             # axonometric: psi-axis spread
    cx_: float = 0.30,            # axonometric: theta-axis drop
    cz_: float = 0.52,            # axonometric: psi-axis drop
    anchor: Tuple[float, float] = (0.56, 0.40),
    fill: float = 1.02,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """NO FIXED POINT — the adversarial game as the only landscape that has an
    equilibrium and never reaches it.  The huge saddle is the EXACT Dirac-GAN
    objective V = f(psi*theta); the staircase riding it is a real run of
    simultaneous gradient descent-ascent, each iteration split into the
    generator's move (pink, along theta) and the discriminator's answer (blue,
    along psi).  Continuous time would close the dotted orbit forever; the
    discrete scheme multiplies the radius by sqrt(1+h^2 f'^2) every step and
    escapes the arena.  The Nash point is a hole in the surface: the one place
    on the sheet made of paper."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    pinkp, bluep, black = _pen(PINK, colors), _pen(BLUE, colors), _pen(BLACK, colors)
    legend = _pen(3, colors) if colors >= 4 else black

    scene = Scene3D(rng, bounds, feed=feed, fit="none", tip=0.5, px=(300, 270), pad=2.0)

    # ---- raw axonometric camera (unit scale; fitted to the sheet below) ----
    def raw(th: float, ps: float, z: float) -> Tuple[float, float, float]:
        sx = ax * th - az * ps
        sy = z_gain * z - (cx_ * th + cz_ * ps)
        dep = (cx_ * th + cz_ * ps) + 0.12 * z_gain * z
        return sx, sy, dep

    # ---- the objective surface: an annulus around the unreachable point ----
    RR = np.linspace(r_void, r_arena, nr + 1)[:, None]
    AA = np.linspace(0.0, 2.0 * math.pi, na + 1)[None, :]
    TH = RR * np.cos(AA)
    PS = RR * np.sin(AA)
    S = TH * PS
    Z = -np.logaddexp(0.0, -S)                       # f(s), stable
    RX = ax * TH - az * PS
    RY = z_gain * Z - (cx_ * TH + cz_ * PS)
    DEP = (cx_ * TH + cz_ * PS) + 0.12 * z_gain * Z

    # ---- fit the arena into an off-centre field, leaving the top-left quiet
    bw = float(RX.max() - RX.min()) or 1.0
    bh = float(RY.max() - RY.min()) or 1.0
    fx0, fy0, fx1, fy1 = x0 + 3.0, y0 + 15.0, x1 - 3.0, y1 - 26.0
    k = fill * min((fx1 - fx0) / bw, (fy1 - fy0) / bh)
    CX = fx0 + anchor[0] * (fx1 - fx0) - k * (RX.min() + RX.max()) / 2.0
    CY = fy0 + anchor[1] * (fy1 - fy0) - k * (RY.min() + RY.max()) / 2.0

    def T(rx: float, ry: float) -> Tuple[float, float]:
        return CX + k * rx, CY + k * ry

    def P(th: float, ps: float, lift: float = 0.0) -> Tuple[float, float, float]:
        """World (theta, psi) -> paper (sx, sy, depth), draped on the surface."""
        z = _V(th * ps) + lift
        rx, ry, dep = raw(th, ps, z)
        sx, sy = T(rx, ry)
        return sx, sy, dep

    SX = CX + k * RX
    SY = CY + k * RY

    inside = lambda sx, sy: x0 + 1.0 <= sx <= x1 - 1.0 and y0 + 1.0 <= sy <= y1 - 1.0

    # ---- the run: simultaneous gradient descent-ascent, legs kept apart ----
    a0 = 0.62 + rng.uniform(-0.55, 0.55)
    th, ps = r_start * math.cos(a0), r_start * math.sin(a0)
    steps: List[Tuple[float, float, float, float, float]] = []  # th,ps,dth,dps,g
    for _ in range(max_iters):
        s = th * ps
        g = _grad_mag(s)
        dth = -step * ps * g
        dps = step * th * g
        steps.append((th, ps, dth, dps, g))
        th, ps = th + dth, ps + dps
        if math.hypot(th, ps) > r_arena - 0.12:
            break
    n_steps = len(steps)
    r_end = math.hypot(steps[-1][0] + steps[-1][2], steps[-1][1] + steps[-1][3])

    # ---- labels first: their halos carve the mesh and the staircase --------
    tip_th = (r_arena + 0.55) * math.cos(0.0)
    lab_th = T(*raw(tip_th, 0.0, _V(0.0))[:2])
    lab_ps = T(*raw(0.0, r_arena + 0.55, _V(0.0))[:2])
    eq = P(0.0, 0.0)
    xT = x0 + 0.018 * W
    scene.halo_labels(
        [
            (_spaced("G  THETA"), lab_th[0] - 0.055 * W, lab_th[1] - 1.0, 2.0, legend),
            (_spaced("D  PSI"), lab_ps[0] - 0.02 * W, lab_ps[1] - 1.0, 2.0, legend),
            (_spaced("EQUILIBRIUM"), eq[0] - 0.085 * W, eq[1] - 0.052 * H, 1.9, legend),
            (_spaced("NEVER REACHED"), eq[0] - 0.085 * W, eq[1] - 0.052 * H - 4.2, 1.6, legend),
        ]
    )

    # ---- the arena: hidden-line saddle, spider-web polar meshing ----------
    lod = PolarLOD(
        levels=((16, 0.0), (8, 0.20), (4, 0.42), (2, 0.64), (1, 0.82)),
        ring_start=1,
        ring_skip_inner=0.22,
        ridge_every=na // 4,
        ridge_half=na // 8,
    )
    scene.surface(
        SX,
        SY,
        np.where(
            (SX > x0 + 1.0) & (SX < x1 - 1.0) & (SY > y0 + 1.0) & (SY < y1 - 1.0),
            DEP,
            Scene3D.HIDE,
        ),
        pen=black,
        thin=ScreenThin(gap_mm=1.05, far_mult=1.9, weave=0.55),
        lod=lod,
    )

    # ---- the void rim: the exact circle of the hole, on the surface -------
    rim = []
    for kk in range(181):
        a = 2.0 * math.pi * kk / 180.0
        sx, sy, dp = P(r_void * math.cos(a), r_void * math.sin(a), 0.02)
        rim.append((sx, sy, dp if inside(sx, sy) else Scene3D.HIDE, black))
    scene.lines([rim], mode="over")

    # ---- the conserved orbit: what continuous time would do forever ------
    r_c = math.hypot(steps[int(0.52 * n_steps)][0], steps[int(0.52 * n_steps)][1])
    orbit = []
    for kk in range(721):
        a = 2.0 * math.pi * kk / 720.0
        sx, sy, dp = P(r_c * math.cos(a), r_c * math.sin(a), 0.03)
        on = (kk % 8) < 4 and inside(sx, sy)
        orbit.append((sx, sy, dp if on else Scene3D.HIDE, black))
    scene.lines([orbit], mode="over")

    # ---- the duel: every iteration as two perpendicular player moves -----
    def leg(a_th, a_ps, b_th, b_ps, pen):
        n = max(3, int(12 * math.hypot(b_th - a_th, b_ps - a_ps) / max(0.02, step)))
        out_s = []
        for kk in range(n + 1):
            t = kk / n
            sx, sy, dp = P(a_th + (b_th - a_th) * t, a_ps + (b_ps - a_ps) * t, 0.05)
            out_s.append((sx, sy, dp if inside(sx, sy) else Scene3D.HIDE, pen))
        return out_s

    occ = scene.occupancy(0.85)
    family = []
    corners = []
    for (t0, p0, dth, dps, g) in steps:
        family.append(leg(t0, p0, t0 + dth, p0, pinkp))       # GENERATOR moves
        family.append(leg(t0 + dth, p0, t0 + dth, p0 + dps, bluep))  # DISCRIMINATOR answers
        if math.hypot(dth, dps) > 0.14:
            corners.append((t0 + dth, p0))
    scene.lines(family, occupancy=occ, warmup=0, min_kept=2)

    for ct, cp in corners:
        sx, sy, dp = P(ct, cp, 0.06)
        if inside(sx, sy) and scene.visible(sx, sy, dp):
            scene.emit(_dot(sx, sy, 0.55, color=black, f=feed))

    # ---- the equilibrium itself: a mark on bare paper --------------------
    scene.emit(plus_mark(eq[0], eq[1], s=1.8, pen=pinkp, f=feed))

    out = scene.render()

    # ---- furniture: shared left axis, the quiet top-left corner ----------
    out += type_block(["NO FIXED", "POINT"], xT, y1 - 5.0, height=3.4, pen=legend, f=feed)
    out += _stroke_text(
        _spaced("NEITHER PLAYER EVER ARRIVES"), xT, y1 - 21.0, 2.0, color=legend, f=feed
    )
    out += _stroke_text(
        _spaced(f"{n_steps} STEPS   R {r_start:.2f} TO {r_end:.2f}"),
        xT,
        y0 + 9.0,
        1.8,
        color=legend,
        f=feed,
    )
    out += _stroke_text(
        _spaced("G MOVES THETA   D MOVES PSI"), xT, y0 + 4.0, 1.8, color=legend, f=feed
    )
    out += swatch_bar(x1 - 8.5, y1 - 4.0, [black, pinkp, bluep], size=2.6, f=feed)
    out += scale_footer(bounds, text="MIN G MAX D V D G", pen=legend, height=2.4, f=feed)
    return out
