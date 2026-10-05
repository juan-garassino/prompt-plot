"""THE DOUBLE SLIT — r03.

ORDER: **INTERFERING — a lattice with defects.**

Not a relief of |psi|^2 (r01: a scientific figure) and not an object with the
mechanism hung on it (r02: an illustration).  The plate is one regular system
and nothing else: a ruling in which EVERY RULE CARRIES THE SAME PROBABILITY.
Rule k stands where the cumulative probability first reaches (k+1/2)/N, so the
rules' own spacing is the pattern and no rule is longer, taller or heavier than
any other -- position is the only thing that carries information.

Two commensurate lattices live inside that one ruling, and their superposition
is the whole composition:

    the FRINGE lattice   -- zeros of the quantum law at  u = (m + 1/2)/3
    the ENVELOPE lattice -- zeros of each aperture at    u = m

with d = 3a exactly, so the third fringe maximum falls on the first envelope
zero and is annihilated.  Both lattices cancel by leaving the paper bare: six
narrow channels where the cross term is negative, and two wide ones at the ends
where the two lattices coincide and an entire order is missing.  The cross term
is drawn NOWHERE.  The blank paper is the conserved quantity -- the rules taken
out of a channel are the rules piled into the bands beside it, and the count
never changes.

Amplitudes: exact Rayleigh-Sommerfeld aperture integral, 96-node Gauss-Legendre.

Entry point: ``double_slit_lattice``.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

import numpy as np

from promptplot.models import GCodeCommand
from promptplot.generative.engine import Scene3D
from promptplot.generative.kit import (
    _clip_runs,
    _poly,
    _rect_keep,
    _spaced,
    _stroke_text,
    _text_width,
)
from promptplot.generative.rng import SeededRNG

Bounds = Tuple[float, float, float, float]

LAMBDA = 633e-9
SLIT_A = 100e-6
SLIT_D = 300e-6          # d = 3a  ->  the third order is annihilated
DIST_L = 2.000
_K = 2.0 * math.pi / LAMBDA
UMAX = 1.06              # a hair past the first envelope zeros, so the two
                         # wide end channels are visibly bounded


# --------------------------------------------------------------------------
# exact physics
# --------------------------------------------------------------------------
def _x_of_u(u):
    s = np.asarray(u, dtype=float) * LAMBDA / SLIT_A
    return DIST_L * s / np.sqrt(1.0 - s * s)


def _psi(x, xc: float, nodes, wts):
    """Rayleigh-Sommerfeld amplitude of ONE slit, Gauss-Legendre over the
    aperture.  r-L is formed as (x-x')^2/(r+L): k*r ~ 2e7 rad, so subtracting
    would throw away eight digits of phase."""
    xp = xc + 0.5 * SLIT_A * nodes
    dx = np.asarray(x)[:, None] - xp[None, :]
    r = np.sqrt(DIST_L * DIST_L + dx * dx)
    rml = dx * dx / (r + DIST_L)
    integ = np.exp(1j * _K * rml) * (DIST_L / r) / np.sqrt(r)
    return 0.5 * SLIT_A * (integ * wts[None, :]).sum(axis=1)


def _intensities(u):
    nodes, wts = np.polynomial.legendre.leggauss(96)
    x = _x_of_u(np.atleast_1d(u))
    p1 = _psi(x, -0.5 * SLIT_D, nodes, wts)
    p2 = _psi(x, +0.5 * SLIT_D, nodes, wts)
    return np.abs(p1 + p2) ** 2, np.abs(p1) ** 2 + np.abs(p2) ** 2


def _equal_probability_rules(I, U, n: int):
    """The one and only mapping: every rule carries 1/n of the probability."""
    c = np.concatenate([[0.0], np.cumsum(0.5 * (I[1:] + I[:-1]) * np.diff(U))])
    c /= c[-1]
    return np.interp((np.arange(n) + 0.5) / n, c, U)


# --------------------------------------------------------------------------
# the piece
# --------------------------------------------------------------------------
def double_slit_lattice(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    rules: int = 44,
    front: float = 50.0,     # the slab's face, mm
    depth_x: float = 66.0,   # ONE shared oblique depth step for the whole plate
    depth_y: float = 52.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE DOUBLE SLIT as a lattice with defects: one ruling, every rule worth
    the same probability, cut by the two commensurate cancellation lattices."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BLK = 0
    RED = 1 % colors if colors > 1 else 0

    scene = Scene3D(bounds=bounds, feed=feed, fit="rescue", fit_pad=2.0)
    out = scene.out

    # ---- the computation -------------------------------------------------
    U = np.linspace(-UMAX, UMAX, 40001)
    IQ, _IC = _intensities(U)
    ur = _equal_probability_rules(IQ, U, rules)

    # ---- one shared oblique basis ---------------------------------------
    xa = x0 + 0.030 * W
    xb = xa + 0.645 * W
    ax = 0.5 * (xb - xa)
    cx = 0.5 * (xa + xb)
    yf = y0 + 0.140 * H                 # foot of the face
    yt = yf + front                     # face meets the plan

    def face(u: float, t: float) -> Tuple[float, float]:
        return (cx + u * ax, yf + t * front)

    def plan(u: float, t: float) -> Tuple[float, float]:
        return (cx + u * ax + t * depth_x, yt + t * depth_y)

    # ---- the slab: face + plan, both bleeding off the sheet --------------
    slab = []
    e = 0.40                            # the ruled sheet runs past the data
    slab.append([face(-1 - e, 0.0), face(1 + e, 0.0)])
    slab.append([face(-1 - e, 1.0), face(1 + e, 1.0)])
    slab.append([plan(-1 - e, 1.0), plan(1 + e, 1.0)])
    slab.append([face(-1 - e, 0.0), face(-1 - e, 1.0), plan(-1 - e, 1.0)])
    slab.append([face(1 + e, 0.0), face(1 + e, 1.0), plan(1 + e, 1.0)])
    for run in _clip_runs(slab, _rect_keep(bounds, inset=0.6)):
        scene.poly(run, pen=BLK)

    # ---- the ruling: identical rules, position is the only information ----
    outer = float(np.max(np.abs(ur)))
    for u in ur:
        pen = RED if abs(abs(u) - outer) < 1e-9 else BLK
        scene.poly([face(u, 0.0), face(u, 1.0)], pen=pen)          # the face
        scene.poly([plan(u, 0.0), plan(u, 1.0)], pen=pen)          # the plan

    # ---- the second lattice, marked where it annihilates an order --------
    def dotted(p0, p1, pen, dash=1.4, gp=3.0):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        t = 0.0
        while t < L:
            ee = min(L, t + dash)
            scene.poly([(p0[0] + ux * t, p0[1] + uy * t),
                        (p0[0] + ux * ee, p0[1] + uy * ee)], pen=pen)
            t = ee + gp

    for uz in (-1.0, 1.0):
        dotted(plan(uz, 0.06), plan(uz, 0.94), RED)

    # ---- type -------------------------------------------------------------
    def line(text, lx, ly, h, pen=BLK, passes=1, maxw=None, floor=1.15):
        t = _spaced(text)
        lim = (x1 - 2.0) - lx if maxw is None else maxw
        while h > floor and _text_width(t, h) > lim:
            h -= 0.05
        for k in range(passes):
            out.extend(_stroke_text(t, lx + 0.15 * k, ly, h, color=pen, f=feed))

    line("THE DOUBLE SLIT", x0, y1 - 11.0, 10.5, passes=2, maxw=0.72 * W)
    line("EVERY RULE IS WORTH THE SAME", x0, y1 - 22.5, 3.2, maxw=0.72 * W)
    for i, ln in enumerate(
        (
            "FORTY-FOUR RULES, EACH ONE FORTY-FOURTH OF THE PROBABILITY.",
            "NOTHING IS TALLER OR HEAVIER THAN ANYTHING ELSE; ONLY WHERE",
            "THE RULES STAND CARRIES INFORMATION.  THE CROSS TERM IS DRAWN",
            "NOWHERE -- THE RULES IT TAKES OUT OF A CHANNEL ARE THE RULES",
            "IT PILES INTO THE BANDS, AND THE COUNT NEVER CHANGES.",
        )
    ):
        line(ln, x0 + 0.735 * W, y1 - 12.0 - 4.3 * i, 1.9, maxw=0.255 * W)
    line("RED  THE LAST RULE, AND WHERE THE", x0 + 0.735 * W, y1 - 37.5, 1.9,
         pen=RED, maxw=0.255 * W)
    line("THIRD ORDER SHOULD HAVE STOOD.", x0 + 0.735 * W, y1 - 41.8, 1.9,
         pen=RED, maxw=0.255 * W)

    col = (
        (
            "LAMBDA 633 NM   SLIT 100 UM",
            "SEPARATION 300 UM",
            "SCREEN DISTANCE 2.000 M",
            "AMPLITUDES: THE EXACT",
            "RAYLEIGH-SOMMERFELD APERTURE",
            "INTEGRAL, 96-NODE GAUSS-",
            "LEGENDRE, NO FAR-FIELD",
            "APPROXIMATION.",
        ),
        (
            "TWO COMMENSURATE LATTICES:",
            "THE QUANTUM ZEROS AT U =",
            "(M+1/2)/3 AND THE APERTURE",
            "ZEROS AT U = M, WITH D = 3A,",
            "SO THE THIRD ORDER FALLS ON",
            "AN ENVELOPE ZERO AND IS",
            "ANNIHILATED.  U = A SIN THETA",
            "OVER LAMBDA.",
        ),
    )
    for c, lines in enumerate(col):
        for i, ln in enumerate(lines):
            line(ln, x0 + c * 0.255 * W, y0 + 22.0 - 2.9 * i, 1.6,
                 maxw=0.235 * W, floor=1.05)
    return scene.render()
