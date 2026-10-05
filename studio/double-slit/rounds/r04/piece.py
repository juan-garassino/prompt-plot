"""THE DOUBLE SLIT — r04.

ORDER: **INTERFERING — a lattice with defects.**
CANON: **PSYCHEDELIC (1960s)** — continuous warp.

One regular system and nothing else: a ruling in which EVERY RULE CARRIES THE
SAME PROBABILITY.  Rule k lies where the cumulative probability first reaches
(k+1/2)/N, so no rule is longer, heavier or taller than any other and POSITION
is the only thing that carries information.  The ruling is laid down twice at a
small angular offset, so the two families beat against one another physically on
the paper -- the canon's optical vibration and the mechanism's interference are
the same order, and the buzz is finest exactly where the light is brightest.

Two commensurate lattices cancel inside that one ruling:

    the FRINGE lattice   -- quantum zeros at  u = (m + 1/2)/3
    the ENVELOPE lattice -- aperture zeros at u = m,   with d = 3a

so the third order falls on an envelope zero and is annihilated.  Both cancel by
leaving the paper bare.  The cross term is drawn NOWHERE: the rules it takes out
of a channel are the rules it piles into the bands, and the count never changes.

ONE continuous displacement field drives the ruling AND the letterforms; its
amplitude at every height is the exact coherence envelope 2|psi1||psi2|, so the
sheet melts hardest where the two amplitudes overlap most and lies flat where
they cannot interfere at all.

Amplitudes: exact Rayleigh-Sommerfeld aperture integral, 96-node Gauss-Legendre.

Entry point: ``double_slit_vibration``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

import numpy as np

from promptplot.models import GCodeCommand
from promptplot.generative.engine import Scene3D
from promptplot.generative.kit import (
    _clip_runs,
    _poly,
    _rect_keep,
    _runs_from_cmds,
    _spaced,
    _stroke_text,
    _text_width,
    giant_type,
    giant_type_width,
)
from promptplot.generative.rng import SeededRNG

Bounds = Tuple[float, float, float, float]

LAMBDA = 633e-9
SLIT_A = 100e-6
SLIT_D = 300e-6            # d = 3a  ->  the third order is annihilated
DIST_L = 2.000
_K = 2.0 * math.pi / LAMBDA
UMAX = 1.06


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


def _fields(u):
    """-> |psi1+psi2|^2 and the coherence envelope 2|psi1||psi2| (the exact
    amplitude of the cross term)."""
    nodes, wts = np.polynomial.legendre.leggauss(96)
    x = _x_of_u(np.atleast_1d(u))
    p1 = _psi(x, -0.5 * SLIT_D, nodes, wts)
    p2 = _psi(x, +0.5 * SLIT_D, nodes, wts)
    return np.abs(p1 + p2) ** 2, 2.0 * np.abs(p1) * np.abs(p2)


def _equal_probability_rules(I, U, n: int):
    """The one and only mapping: every rule carries 1/n of the probability."""
    c = np.concatenate([[0.0], np.cumsum(0.5 * (I[1:] + I[:-1]) * np.diff(U))])
    c /= c[-1]
    return np.interp((np.arange(n) + 0.5) / n, c, U)


# --------------------------------------------------------------------------
# a spatial hash, so the ruling can be knocked out of the letterforms
# --------------------------------------------------------------------------
class _Mask:
    def __init__(self, radius: float):
        self.r = radius
        self.cell = max(1e-6, radius)
        self.g: Dict[Tuple[int, int], List[Tuple[float, float]]] = {}

    def add_run(self, pts: Sequence[Tuple[float, float]], step: float = 0.8):
        prev = None
        for p in pts:
            if prev is not None:
                d = math.hypot(p[0] - prev[0], p[1] - prev[1])
                for i in range(1, max(1, int(d / step))):
                    t = i * step / d
                    self._add((prev[0] + (p[0] - prev[0]) * t, prev[1] + (p[1] - prev[1]) * t))
            self._add(p)
            prev = p

    def _add(self, p):
        self.g.setdefault((int(p[0] / self.cell), int(p[1] / self.cell)), []).append(p)

    def hit(self, x: float, y: float) -> bool:
        ci, cj = int(x / self.cell), int(y / self.cell)
        rr = self.r * self.r
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for qx, qy in self.g.get((ci + di, cj + dj), ()):
                    if (qx - x) ** 2 + (qy - y) ** 2 < rr:
                        return True
        return False


# --------------------------------------------------------------------------
# the piece
# --------------------------------------------------------------------------
def double_slit_vibration(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
    rules: int = 42,
    beta: float = 7.0,        # degrees: the angular offset that makes the buzz
    melt: float = 30.0,       # mm: the displacement field's full amplitude
    cycles: float = 1.15,     # periods of the displacement across the sheet
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE DOUBLE SLIT, psychedelic: one equal-probability ruling laid down
    twice at a small angle so it beats against itself, melted by the exact
    coherence envelope, with the cancellation lattices left as bare paper."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BLK = 0
    RED = 1 % colors if colors > 1 else 0
    GRN = 2 % colors if colors > 2 else RED

    scene = Scene3D(bounds=bounds, feed=feed, fit="none")
    out = scene.out

    # ---- the computation -------------------------------------------------
    U = np.linspace(-UMAX, UMAX, 40001)
    IQ, ENV = _fields(U)
    ur = _equal_probability_rules(IQ, U, rules)
    env = ENV / ENV.max()

    au = H / (2.0 * UMAX)                      # mm per unit u -- u runs UP
    pcx, pcy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)

    def y_of(u: float) -> float:
        return y0 + (u + UMAX) * au

    def u_of(y: float) -> float:
        return (y - y0) / au - UMAX

    def warp(px: float, py: float) -> Tuple[float, float]:
        """THE displacement field: amplitude = the exact coherence envelope at
        this height, shape = one and a bit periods across the sheet.  It moves
        the ruling and the letterforms alike."""
        e = float(np.interp(u_of(py), U, env))
        return (px, py + melt * e * math.sin(2 * math.pi * cycles * (px - x0) / W + 0.75))

    def spin(pts, sgn: float):
        a = math.radians(beta) * sgn
        ca, sa = math.cos(a), math.sin(a)
        return [
            (pcx + (px - pcx) * ca - (py - pcy) * sa, pcy + (px - pcx) * sa + (py - pcy) * ca)
            for px, py in pts
        ]

    # ---- the letterforms, cut by the lattices they lie on -----------------
    gaps = np.diff(ur)
    wide = float(np.mean(gaps)) * 2.6           # a channel, not a spacing
    voids = [(ur[i], ur[i + 1]) for i in range(len(ur) - 1) if gaps[i] > wide]
    voids = [(-UMAX, ur[0])] + voids + [(ur[-1], UMAX)]

    def lit(p) -> bool:
        u = u_of(p[1])
        return not any(a + 0.004 < u < b - 0.004 for a, b in voids)

    head = ("ONE AND", "ONE MAKE", "NONE")
    heights = [min(52.0, (0.93 * W) / max(1e-6, giant_type_width(t, 1.0))) for t in head]
    glyph_runs: List[List[Tuple[float, float]]] = []
    ytop = y0 + 0.875 * H
    for t, h in zip(head, heights):
        base = ytop - h
        raw = giant_type(t, x0 + 0.028 * W, base, h, pen=BLK,
                         weight=max(1.7, h * 0.075), tip=0.5, f=feed)
        for run in _clip_runs(_runs_from_cmds(raw), lit):
            glyph_runs.append([warp(*p) for p in run])
        ytop = base - 5.0

    # knock the ruling out of the letterforms so the type reads as mass
    mask = _Mask(1.9)
    for run in glyph_runs:
        mask.add_run(run)

    # ---- the ruling: two families of the SAME exact lattice, ±beta --------
    nx = 64
    for sgn, pen in ((-1.0, RED), (1.0, GRN)):
        for u in ur:
            pts = [warp(x0 + W * i / nx, y_of(u)) for i in range(nx + 1)]
            pts = spin(pts, sgn)
            run: List[Tuple[float, float]] = []
            def flush(rr):
                if len(rr) < 2:
                    return
                if math.hypot(rr[-1][0] - rr[0][0], rr[-1][1] - rr[0][1]) < 3.0:
                    return
                for r in _clip_runs([rr], _rect_keep(bounds, 0.6)):
                    scene.poly(r, pen=pen)

            for p in pts:
                if mask.hit(p[0], p[1]):
                    flush(run)
                    run = []
                else:
                    run.append(p)
            flush(run)

    # ---- the type, on the same field --------------------------------------
    for run in glyph_runs:
        for r in _clip_runs([run], _rect_keep(bounds, 0.6)):
            scene.poly(r, pen=BLK)

    # ---- the record, small, on the same field -----------------------------
    def small(text: str, lx: float, ly: float, h: float, pen=BLK):
        t = _spaced(text)
        while h > 1.05 and _text_width(t, h) > (x1 - 3.0) - lx:
            h -= 0.05
        for run in _runs_from_cmds(_stroke_text(t, lx, ly, h, color=pen, f=feed)):
            for r in _clip_runs([[warp(*p) for p in run]], _rect_keep(bounds, 0.6)):
                scene.poly(r, pen=pen)

    small("THE DOUBLE SLIT", x0 + 0.028 * W, y1 - 11.0, 4.6)
    for i, ln in enumerate(
        (
            "LAMBDA 633 NM   SLIT 100 UM   SEPARATION 300 UM   SCREEN 2.000 M",
            "EVERY RULE IS ONE FORTY-SECOND OF THE PROBABILITY.  D = 3A, SO THE",
            "THIRD ORDER FALLS ON AN ENVELOPE ZERO.  AMPLITUDES: THE EXACT",
            "RAYLEIGH-SOMMERFELD APERTURE INTEGRAL, 96-NODE GAUSS-LEGENDRE.",
        )
    ):
        small(ln, x0 + 0.035 * W, y0 + 16.0 - 3.6 * i, 1.7)
    return scene.render()
