"""THE DOUBLE SLIT — r02.  CARRIER: A BEAD-COUNTING FRAME (an abacus).

TRANSPOSE, DON'T PLOT.  r01 drew two reliefs of |psi|^2 and was a scientific
figure.  Here the subject is carried by an ordinary made object whose whole
mechanism IS the conservation the physics asserts:

    an abacus cannot be made to show more by adding a bead.
    It can only move the beads it already has.

One tray, two wires, ONE set of beads.  Both wires carry the same 40 beads
because the two laws integrate to the same total; each bead is exactly one
fortieth of the probability, and bead k stands where the cumulative probability
first reaches (k+1/2)/40 — the inverse CDF, no free parameter.  The far wire is
strung by |psi1|^2+|psi2|^2, the near wire by |psi1+psi2|^2.  Where the quantum
law forbids arrival there is no bead, so the wire runs bare: the cross term is
drawn nowhere and the bare wire is the paper.

Bead diameter is not a style choice either — it is set so the brightest fringe
is EXACTLY full, beads touching, the wire packed solid.  Every other cluster is
therefore measured against a jammed one.

Amplitudes: exact Rayleigh-Sommerfeld aperture integral, 96-node Gauss-Legendre.

Entry point: ``double_slit_counting_frame``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

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

# --------------------------------------------------------------------------
# the apparatus (stated, not cited) -- d = 3a, so the third order is MISSING
# --------------------------------------------------------------------------
LAMBDA = 633e-9
SLIT_A = 100e-6
SLIT_D = 300e-6
DIST_L = 2.000
_K = 2.0 * math.pi / LAMBDA
UMAX = 1.00          # crop: the central envelope lobe, |a sin(theta)| <= lambda


# --------------------------------------------------------------------------
# exact physics (identical solver to r01)
# --------------------------------------------------------------------------
def _x_of_u(u):
    s = np.asarray(u, dtype=float) * LAMBDA / SLIT_A
    return DIST_L * s / np.sqrt(1.0 - s * s)


def _psi(x, xc: float, nodes, wts):
    """Rayleigh-Sommerfeld amplitude of ONE slit, Gauss-Legendre over the aperture.
    r-L is formed as (x-x')^2/(r+L): k*r ~ 2e7 rad, so subtracting would throw
    away eight digits of phase."""
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


def _quantiles(I, U, n: int):
    """Bead k stands where the cumulative probability first reaches (k+1/2)/n."""
    c = np.concatenate([[0.0], np.cumsum(0.5 * (I[1:] + I[:-1]) * np.diff(U))])
    c /= c[-1]
    q = (np.arange(n) + 0.5) / n
    return np.interp(q, c, U), c


# --------------------------------------------------------------------------
# jamming: beads are solid, they cannot pass through one another
# --------------------------------------------------------------------------
def _jam(pos: np.ndarray, sep: float) -> np.ndarray:
    """Push overlapping beads apart, keeping order, inside [-UMAX, UMAX].
    A physical constraint of the object, resolved deterministically: where the
    law asks for more probability than the wire can hold, the beads JAM."""
    p = np.array(pos, dtype=float)
    lo, hi = -UMAX + 0.5 * sep, UMAX - 0.5 * sep
    for _ in range(4000):
        moved = False
        for i in range(len(p) - 1):
            d = p[i + 1] - p[i]
            if d < sep - 1e-12:
                c = 0.5 * (p[i] + p[i + 1])
                p[i], p[i + 1] = c - 0.5 * sep, c + 0.5 * sep
                moved = True
        p[0] = max(p[0], lo)
        p[-1] = min(p[-1], hi)
        if not moved:
            break
    return p


# --------------------------------------------------------------------------
# the bead (a solid of revolution threaded on the wire)
# --------------------------------------------------------------------------
def _bead(px: float, py: float, half: float, rad: float, ez, pen, feed):
    """Soroban bead: lens silhouette (two circular arcs) + two latitude rings.
    ``half`` = half-length along the wire, ``rad`` = radius, ``ez`` = the
    projected depth direction (cabinet foreshortening already applied)."""
    out: List[GCodeCommand] = []
    R = (half * half + rad * rad) / (2.0 * rad)
    for sgn in (1.0, -1.0):
        cy0 = py + sgn * (rad - R)
        a0 = math.asin(max(-1.0, min(1.0, half / R)))
        pts = [
            (px + R * math.sin(-a0 + 2 * a0 * i / 18), cy0 + sgn * R * math.cos(-a0 + 2 * a0 * i / 18))
            for i in range(19)
        ]
        out += _poly(pts, color=pen, f=feed)
    ring = [
        (px + rad * math.sin(2 * math.pi * i / 28) * ez[0],
         py + rad * math.cos(2 * math.pi * i / 28) + rad * math.sin(2 * math.pi * i / 28) * ez[1])
        for i in range(29)
    ]
    out += _poly(ring, color=pen, f=feed)
    return out


def _frame_runs(fx0, fy0, fx1, fy1, ix0, iy0, ix1, iy1, tx, ty):
    """The bead frame as ONE solid, returned as polylines so the piece can crop
    it at the sheet edge: outer box (front face, the visible back edges, corner
    connectors) and the opening cut through it, with the reveal on the two
    inner faces the oblique step exposes."""
    def rect(a, b, c, d):
        return [(a, b), (c, b), (c, d), (a, d), (a, b)]

    runs = [rect(fx0, fy0, fx1, fy1), rect(ix0, iy0, ix1, iy1)]
    runs.append([(fx0 + tx, fy1 + ty), (fx1 + tx, fy1 + ty), (fx1 + tx, fy0 + ty)])
    runs.append([(ix0 + tx, iy0 + ty), (ix1 + tx, iy0 + ty)])
    runs.append([(ix0 + tx, iy0 + ty), (ix0 + tx, iy1 + ty)])
    for cxp, cyp in ((fx0, fy1), (fx1, fy1), (fx1, fy0), (ix0, iy0), (ix1, iy0), (ix0, iy1)):
        runs.append([(cxp, cyp), (cxp + tx, cyp + ty)])
    return runs


# --------------------------------------------------------------------------
# the piece
# --------------------------------------------------------------------------
def double_slit_counting_frame(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    beads: int = 24,
    gap: float = 62.0,       # mm between the two wires
    tx: float = 11.0,        # the ONE shared oblique depth step, used by the
    ty: float = 7.0,         # frame and by every bead's equator ring
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE DOUBLE SLIT as a bead-counting frame: the same twenty-four beads,
    strung twice.  Upper wire |psi1|^2+|psi2|^2, lower wire |psi1+psi2|^2.  A
    bead cannot be made, only moved; the bare wire is the cross term."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BLK = 0
    RED = 1 % colors if colors > 1 else 0

    scene = Scene3D(bounds=bounds, feed=feed, fit="rescue", fit_pad=2.0)
    out = scene.out

    # ---- the computation ------------------------------------------------
    U = np.linspace(-UMAX, UMAX, 20001)
    IQ, IC = _intensities(U)
    uq_raw, _ = _quantiles(IQ, U, beads)     # lower wire: interference
    uc_raw, _ = _quantiles(IC, U, beads)     # upper wire: which path
    nulls = [(k + 0.5) * SLIT_A / SLIT_D for k in range(3)]
    nulls = [-v for v in reversed(nulls)] + nulls

    # ---- the object ------------------------------------------------------
    # The frame is BIGGER than the sheet: its right stile and the whole oblique
    # back run off the page and are clipped there.  Every bead stays on.
    stile = 9.0
    ix0 = x0 + 0.145 * W
    ix1 = x1 - 0.048 * W
    ax = 0.5 * (ix1 - ix0)
    cx = 0.5 * (ix0 + ix1)
    fx0, fx1 = ix0 - stile, ix1 + stile
    fy1 = y1 - 0.160 * H
    fy0 = fy1 - (gap + 2.0 * stile + 30.0)
    iy0, iy1 = fy0 + stile, fy1 - stile
    y_lo = iy0 + 16.0                         # interference wire
    y_hi = y_lo + gap                         # which-path wire
    ez = (tx / math.hypot(tx, ty) * 0.55, ty / math.hypot(tx, ty) * 0.55)

    # Bead size is NOT a style choice.  It is the tightest spacing the WHICH-PATH
    # law asks for: that wire is exactly full where it is densest.  The quantum
    # law asks for tighter packing than that, so its beads JAM -- they pile up
    # against one another and spill out of the bright fringes.
    sep = float(np.min(np.diff(uc_raw)))
    half = 0.5 * sep * ax
    rad = half * 1.85
    uq = _jam(uq_raw, sep)
    uc = _jam(uc_raw, sep)

    # ---- type first: halos reserved before any geometry ------------------
    scene.halo_labels(
        [
            ("1", x0 + 1.0, y_hi - 3.0, 9.0, BLK),
            (_spaced("WHICH PATH"), ix0 + 2.0, y_hi + 11.5, 2.5, BLK),
            (_spaced("PSI1 SQUARED + PSI2 SQUARED"), ix0 + 2.0, y_hi + 6.6, 1.7, BLK),
            ("2", x0 + 1.0, y_lo - 3.0, 9.0, BLK),
            (_spaced("INTERFERENCE"), ix0 + 2.0, y_lo + 11.5, 2.5, BLK),
            (_spaced("PSI1 + PSI2  ALL SQUARED"), ix0 + 2.0, y_lo + 6.6, 1.7, BLK),
        ]
    )

    for run in _clip_runs(
        _frame_runs(fx0, fy0, fx1, fy1, ix0, iy0, ix1, iy1, tx, ty),
        _rect_keep(bounds, inset=0.6),
    ):
        scene.poly(run, pen=BLK)

    # ---- bare spans of the interference wire: what the cross term took ----
    def bare_spans(pos):
        s, lo = [], -UMAX
        for pp in pos:
            hi = pp - half / ax
            if (hi - lo) * ax > 2.4 * half:
                s.append((lo, hi))
            lo = pp + half / ax
        if (UMAX - lo) * ax > 2.4 * half:
            s.append((lo, UMAX))
        return s

    spans_q = bare_spans(uq)

    # ---- string both wires ------------------------------------------------
    for wy, pos, upper in ((y_hi, uc, True), (y_lo, uq, False)):
        prev = -UMAX
        for u in pos:                                   # the wire shows only
            a = cx + prev * ax                          # where no bead covers it
            b = cx + (u - half / ax) * ax
            if b - a > 0.2:
                scene.poly([(a, wy), (b, wy)], pen=BLK)
            prev = u + half / ax
        a, b = cx + prev * ax, cx + UMAX * ax
        if b - a > 0.2:
            scene.poly([(a, wy), (b, wy)], pen=BLK)
        for u in pos:
            red = upper and any(lo < u < hi for lo, hi in spans_q)
            out.extend(_bead(cx + u * ax, wy, half, rad, ez, RED if red else BLK, feed))

    # ---- dotted projection lines at the six exact zeros (never arrows) ----
    def dotted(p0, p1, pen, dash=1.3, gp=2.8):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        t = 0.0
        while t < L:
            e = min(L, t + dash)
            scene.poly([(p0[0] + ux * t, p0[1] + uy * t), (p0[0] + ux * e, p0[1] + uy * e)], pen=pen)
            t = e + gp

    for un in nulls:
        xz = cx + un * ax
        dotted((xz, y_lo + rad + 1.6), (xz, y_hi - rad - 1.6), RED)

    # ---- type -------------------------------------------------------------
    def line(text, lx, ly, h, pen=BLK, passes=1, maxw=None, floor=1.15):
        t = _spaced(text)
        lim = (x1 - 2.0) - lx if maxw is None else maxw
        while h > floor and _text_width(t, h) > lim:
            h -= 0.05
        for k in range(passes):
            out.extend(_stroke_text(t, lx + 0.15 * k, ly, h, color=pen, f=feed))

    line("THE DOUBLE SLIT", x0, y1 - 11.0, 10.0, passes=2, maxw=0.95 * W)
    line("TWENTY-FOUR BEADS  STRUNG TWICE  BY TWO LAWS", x0, y1 - 22.0, 3.2, maxw=0.95 * W)

    ny = fy0 - 12.0
    for i, ln in enumerate(
        (
            "AN ABACUS CANNOT BE MADE TO SHOW MORE BY ADDING A BEAD.",
            "IT CAN ONLY MOVE THE BEADS IT HAS.  EACH BEAD IS ONE",
            "TWENTY-FOURTH OF THE PROBABILITY, AND BOTH WIRES CARRY",
            "TWENTY-FOUR, BECAUSE THE TWO LAWS SUM ALIKE.",
        )
    ):
        line(ln, x0, ny - 4.9 * i, 2.3, maxw=0.44 * W)
    line("RED  BEADS THE QUANTUM LAW HAS NO ROOM FOR.", x0, ny - 24.0, 2.3, pen=RED, maxw=0.44 * W)

    col = (
        (
            "LAMBDA 633 NM   SLIT 100 UM",
            "SEPARATION 300 UM",
            "SCREEN DISTANCE 2.000 M",
            "D = 3A, SO THE THIRD ORDER",
            "FALLS ON THE ENVELOPE ZERO",
            "AND IS MISSING.",
        ),
        (
            "AMPLITUDES: THE EXACT RAYLEIGH-",
            "SOMMERFELD APERTURE INTEGRAL,",
            "96-NODE GAUSS-LEGENDRE, NO",
            "FAR-FIELD APPROXIMATION.  BEAD K",
            "STANDS WHERE THE CUMULATIVE",
            "PROBABILITY REACHES (K+1/2)/24.",
        ),
    )
    for c, lines in enumerate(col):
        for i, ln in enumerate(lines):
            line(ln, x0 + 0.50 * W + c * 0.255 * W, ny - 3.0 * i, 1.6, maxw=0.235 * W, floor=1.05)
    return scene.render()
