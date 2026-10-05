"""THE DOUBLE SLIT — WHAT THE CROSS TERM TAKES AWAY  (candidate, round r01).

Two laws for the same apparatus, computed from the SAME pair of complex
amplitudes and drawn in ONE shared axonometric basis:

    I_quantum(x)   = |psi1 + psi2|^2        paths indistinguishable
    I_classical(x) = |psi1|^2 + |psi2|^2    which-path known
    difference     = 2 Re(psi1 psi2*)       the cross term -- DRAWN NOWHERE

The amplitudes are the exact Rayleigh-Sommerfeld (Fresnel-Kirchhoff) aperture
integral evaluated by Gauss-Legendre quadrature -- no far-field approximation,
no analytic sinc/cos stand-in anywhere in the drawn geometry.  The far-field
closed form is used only as a verification oracle (see NOTES.md).

Entry point: ``double_slit_cross_term``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.models import GCodeCommand
from promptplot.generative.engine import Scene3D, ScreenThin
from promptplot.generative.kit import _spaced, _stroke_text, _text_width
from promptplot.generative.rng import SeededRNG

Bounds = Tuple[float, float, float, float]

# --------------------------------------------------------------------------
# the apparatus (stated, not cited -- an optical bench anyone can build)
# --------------------------------------------------------------------------
LAMBDA = 633e-9       # m   HeNe line, one quantum at a time
SLIT_A = 100e-6       # m   slit width
SLIT_D = 300e-6       # m   centre-to-centre separation  (d/a = 3 exactly ->
DIST_L = 2.000        # m   screen distance               the 3rd order is MISSING)
_K = 2.0 * math.pi / LAMBDA

UMAX = 1.00           # crop in envelope units u = a sin(theta)/lambda
                      # (u = +-1 are the first envelope zeros)


# --------------------------------------------------------------------------
# exact physics
# --------------------------------------------------------------------------
def _x_of_u(u: float | np.ndarray):
    """Screen position for u = a sin(theta)/lambda.  sin(theta) exact, no
    small-angle step: x = L sin / sqrt(1 - sin^2)."""
    s = np.asarray(u) * LAMBDA / SLIT_A
    return DIST_L * s / np.sqrt(1.0 - s * s)


def _psi(x, xc: float, nodes, wts):
    """Rayleigh-Sommerfeld amplitude of ONE slit of width SLIT_A centred at xc.

        psi(x) = INT exp(i k (r-L)) (L/r) r^(-1/2) dx' ,  r = sqrt(L^2+(x-x')^2)

    The common piston phase exp(ikL) is divided out (it cancels in every
    intensity) and r-L is formed as (x-x')^2/(r+L) so no significant digits are
    lost to cancellation at k*r ~ 2e7 rad.  Gauss-Legendre over the aperture.
    """
    xp = xc + 0.5 * SLIT_A * nodes                      # (M,)
    dx = np.asarray(x)[:, None] - xp[None, :]           # (N, M)
    r = np.sqrt(DIST_L * DIST_L + dx * dx)
    rml = dx * dx / (r + DIST_L)
    integ = np.exp(1j * _K * rml) * (DIST_L / r) / np.sqrt(r)
    return 0.5 * SLIT_A * (integ * wts[None, :]).sum(axis=1)


def _intensities(u):
    """-> (I_quantum, I_classical) on the u grid, both in the SAME units."""
    nodes, wts = np.polynomial.legendre.leggauss(96)
    x = _x_of_u(np.atleast_1d(u))
    p1 = _psi(x, -0.5 * SLIT_D, nodes, wts)
    p2 = _psi(x, +0.5 * SLIT_D, nodes, wts)
    iq = np.abs(p1 + p2) ** 2
    ic = np.abs(p1) ** 2 + np.abs(p2) ** 2
    return iq, ic


def _iq_scalar(u: float) -> float:
    return float(_intensities(np.array([u]))[0][0])


def _golden_min(f, a: float, b: float, tol: float = 1e-10) -> float:
    """Golden-section minimiser -- the nulls are FOUND in the computed
    intensity, never assumed from the cos^2 formula."""
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = f(c), f(d)
    while b - a > tol:
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(d)
    return 0.5 * (a + b)


def _find_nulls() -> List[float]:
    """Zeros of |psi1+psi2|^2 inside the crop, by minimisation of the computed
    intensity (bracketed a third of a fringe either side of the seed)."""
    period = SLIT_A / SLIT_D                     # fringe period in u units
    out: List[float] = []
    m = 0
    while True:
        seed = (m + 0.5) * period
        if seed > UMAX:
            break
        w = 0.33 * period
        out.append(_golden_min(_iq_scalar, seed - w, seed + w))
        m += 1
    return [-v for v in reversed(out)] + out


# --------------------------------------------------------------------------
# drawing helpers
# --------------------------------------------------------------------------
def _dotted(scene: Scene3D, p0, p1, pen, dash: float = 1.5, gap: float = 1.9) -> None:
    """A dotted PROJECTION line (house law: never an arrow)."""
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    if L < 1e-6:
        return
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    t = 0.0
    while t < L:
        e = min(L, t + dash)
        scene.poly([(p0[0] + ux * t, p0[1] + uy * t), (p0[0] + ux * e, p0[1] + uy * e)], pen=pen)
        t = e + gap


# --------------------------------------------------------------------------
# the piece
# --------------------------------------------------------------------------
def double_slit_cross_term(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    nu: int = 460,
    nv_hero: int = 7,
    nv_dune: int = 3,
    ax: float = 68.0,          # mm per unit u        -- HORIZONTAL (the screen axis)
    dx: float = 14.0,           # mm per unit depth    -- shared oblique recession
    dy: float = 22.0,          # ... (dx, dy) is ONE basis vector for the whole scene
    gain: float = 66.0,        # mm per unit probability density -- VERTICAL, shared
    z_hero: float = 1.00,      # world FOOTPRINT of the dominant plate (depth)
    z_dune: float = 0.34,      # ... of the subordinate plate; projection unchanged
    fore: float = 0.30,        # how far the crimson ground rules step forward
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE DOUBLE SLIT -- two laws, one computation, the difference left blank.

    Lower plate (dominant): |psi1+psi2|^2, a corrugated relief whose front rim
    dives to the ground line at every forbidden position.  Upper plate: the same
    two amplitudes with the cross term switched off, |psi1|^2+|psi2|^2 -- a
    smooth dune that never touches ground.  Crimson rules the zero set of the
    quantum law on BOTH plates; the crimson plumb standing on each rule measures
    what interference took away.  On the comb that plumb has zero length, so
    nothing is drawn: the difference is the paper.

    Cabinet-oblique axonometry -- ONE basis for the whole scene: u -> (ax, 0),
    probability -> (0, gain), depth -> (dx, dy).  A plate that must be smaller
    shrinks its world footprint (z_dune), never the projection constants.
    """
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BLK = 0
    RED = 1 % colors if colors > 1 else 0
    WY = gain

    scene = Scene3D(bounds=bounds, feed=feed, px=(560, 420), fit="rescue", fit_pad=3.0, tip=0.45)

    # ---- the computation ------------------------------------------------
    nulls = _find_nulls()
    U = np.linspace(-UMAX, UMAX, nu + 1)
    pitch = U[1] - U[0]
    red_cols = set()
    for un in nulls:                       # seat TWO mesh columns on each null
        j = int(np.argmin(np.abs(U - un)))
        j = max(1, min(nu - 1, j))
        U[j], U[j + 1] = un - 0.20 * pitch, un + 0.20 * pitch
        red_cols.add(j)
        red_cols.add(j + 1)
    IQ, IC = _intensities(U)
    norm = float(IQ.max())
    HQ, HC = IQ / norm, IC / norm          # ONE normalisation for both laws

    # ---- shared oblique basis (never rescaled per plate) ------------------
    cx = x0 + 0.475 * W

    def P(cy: float, u: float, h: float, z: float) -> Tuple[float, float]:
        return (cx + u * ax + z * dx, cy + h * WY + z * dy)

    # plate spacing derived from the REAL projected extent, so whatever the
    # parameters do the stages cannot interpenetrate.
    up_hero = WY * float(HQ.max()) + dy * z_hero
    up_dune = WY * float(HC.max()) + dy * z_dune
    dn = fore * dy
    cy_dune = y1 - 82.0 - up_dune
    cy_hero = cy_dune - dn - 12.0 - up_hero

    def plate(cy: float, Z: float, nv: int, Hh, thin) -> None:
        ZV = np.linspace(0.0, Z, nv + 1)
        SX = cx + U[None, :] * ax + ZV[:, None] * dx
        SY = cy + Hh[None, :] * WY + ZV[:, None] * dy
        DE = -ZV[:, None] + 0.0 * Hh[None, :]
        scene.surface(SX, SY, DE, pen=BLK, thin=thin)

    # ---- type first: halos are reserved BEFORE any mesh is drawn ---------
    scene.halo_labels(
        [
            ("2", x0 + 0.5, cy_hero + up_hero - 10.0, 7.0, BLK),
            (_spaced("INTERFERENCE"), x0 + 9.0, cy_hero + up_hero - 7.0, 2.8, BLK),
            (_spaced("PSI1 + PSI2  ALL SQUARED"), x0 + 9.0, cy_hero + up_hero - 12.4, 1.75, BLK),
            (_spaced("PATHS INDISTINGUISHABLE"), x0 + 9.0, cy_hero + up_hero - 16.6, 1.75, BLK),
            ("1", x0 + 0.5, cy_dune + up_dune - 9.0, 7.0, BLK),
            (_spaced("WHICH PATH"), x0 + 9.0, cy_dune + up_dune - 6.0, 2.8, BLK),
            (_spaced("PSI1 SQ  +  PSI2 SQ"), x0 + 9.0, cy_dune + up_dune - 11.4, 1.75, BLK),
            (_spaced("PATHS DISTINGUISHED"), x0 + 9.0, cy_dune + up_dune - 15.6, 1.75, BLK),
        ]
    )

    _tom = _spaced("THIRD ORDER MISSING")
    scene.halo_labels(
        [(_tom, x1 - _text_width(_tom, 1.6) - 1.5, cy_hero + up_hero + 4.0, 1.6, BLK)]
    )

    # ---- plate 1 (subordinate): which-path, shallow footprint -----------
    plate(cy_dune, z_dune, nv_dune, HC, ScreenThin(gap_mm=3.0, far_mult=1.25))
    # ---- plate 2 (dominant): interference, deep footprint ---------------
    plate(cy_hero, z_hero, nv_hero, HQ, ScreenThin(gap_mm=3.0, far_mult=1.25))

    # ---- ground line + front rim (nothing can occlude z = 0) -------------
    for cy, Hh, w in ((cy_dune, HC, 1), (cy_hero, HQ, 2)):
        g0, g1 = P(cy, -UMAX, 0.0, 0.0), P(cy, UMAX, 0.0, 0.0)
        scene.poly([(g0[0] - 7.0, g0[1]), (g1[0] + 9.0, g1[1])], pen=BLK)
        rim = [P(cy, float(U[j]), float(Hh[j]), 0.0) for j in range(len(U))]
        for k in range(w):                                  # line weight by passes
            scene.poly([(px, py + 0.13 * k) for px, py in rim], pen=BLK)

    # ---- crimson: the zero set of the quantum law, on both plates --------
    gap_lo, gap_hi = cy_dune - dn + 1.5, cy_hero + up_hero - 1.5
    for un in nulls:
        h_q = float(np.interp(un, U, HQ))
        h_c = float(np.interp(un, U, HC))
        for cy, hv in ((cy_dune, h_c), (cy_hero, h_q)):
            a0 = P(cy, un, 0.0, 0.0)
            scene.poly([a0, P(cy, un, 0.0, -fore)], pen=RED)   # forbidden, on the floor
            if hv * WY > 1.6:            # SOLID plumb = the height interference deleted
                top = P(cy, un, hv, 0.0)
                scene.poly([a0, top], pen=RED)
                scene.poly([(top[0] - 1.6, top[1]), (top[0] + 1.6, top[1])], pen=RED)
        _dotted(scene, (cx + un * ax, gap_lo), (cx + un * ax, gap_hi), RED, dash=1.0, gap=2.9)
    for uf in (-1.0, 0.0, 1.0):        # shared structure: envelope zeros + axis
        _dotted(scene, (cx + uf * ax, gap_lo), (cx + uf * ax, gap_hi), BLK, dash=0.9, gap=3.6)

    out = scene.out

    # ---- type ------------------------------------------------------------
    def line(text, lx, ly, h, pen=BLK, passes=1, maxw=None, floor=1.25):
        t = _spaced(text)
        lim = (x1 - 2.0) - lx if maxw is None else maxw
        while h > floor and _text_width(t, h) > lim:
            h -= 0.05
        for k in range(passes):
            out.extend(_stroke_text(t, lx + 0.15 * k, ly, h, color=pen, f=feed))

    # giant flush-left word stack: the Swiss HUGE element, cropped to a notch
    line("THE", x0, y1 - 9.0, 3.2)
    line("DOUBLE", x0, y1 - 22.0, 10.0, passes=2, maxw=0.62 * W)
    line("SLIT", x0, y1 - 35.0, 10.0, passes=2, maxw=0.62 * W)
    for i, ln in enumerate(("INTERFERENCE", "REDISTRIBUTES", "IT DOES NOT", "CREATE")):
        line(ln, x0 + 0.545 * W, y1 - 28.0 - 5.2 * i, 2.8)
    for i, ln in enumerate(
        (
            "THE CROSS TERM 2 RE (PSI1 PSI2*) IS DRAWN",
            "NOWHERE: IT IS THE PAPER BETWEEN THE RIDGES.",
            "ITS SUM OVER THE SCREEN IS EXACTLY ZERO.",
        )
    ):
        line(ln, x0, y1 - 48.0 - 4.8 * i, 2.3, maxw=0.62 * W)
    line("RED  WHERE THE PARTICLE NEVER LANDS.", x0, y1 - 65.0, 2.2, pen=RED, maxw=0.70 * W)
    line("EACH PLUMB IS WHAT INTERFERENCE TOOK.", x0, y1 - 70.0, 2.2, pen=RED, maxw=0.70 * W)

    # ---- data footer: three fine columns on the module -------------------
    col = (
        (
            "LAMBDA 633 NM",
            "SLIT WIDTH 100 UM",
            "SEPARATION 300 UM",
            "SCREEN 2.000 M",
            "HEIGHT = PROBABILITY",
            "ONE SCALE BOTH PLATES",
        ),
        (
            "AMPLITUDES: EXACT",
            "RAYLEIGH-SOMMERFELD",
            "APERTURE INTEGRAL BY",
            "96-NODE GAUSS-",
            "LEGENDRE, NO FAR-",
            "FIELD APPROXIMATION",
        ),
        (
            "D = 3A SO THE THIRD",
            "ORDER FALLS ON THE",
            "ENVELOPE ZERO AND IS",
            "MISSING. NOT A",
            "BIPRISM: THE ENVELOPE",
            "IS REAL. ZEROS FOUND",
        ),
    )
    for c, lines in enumerate(col):
        for i, ln in enumerate(lines):
            line(ln, x0 + c * 0.335 * W, y0 + 18.0 - 2.95 * i, 1.55, maxw=0.305 * W, floor=1.05)
    return scene.render()
