"""ATTENTION AS RESONANCE — exact recreation of ``studio/resonance/ref/attention-as-resonance.png``.

This is a REPRODUCTION, not a design.  Every element, its position and its
marker vocabulary are traced off the reference (1122 x 1402 px), mapped into
the drawable area, and drawn with pen-plottable geometry.

Two coordinate systems:

* REFERENCE PIXELS — everything in this file is laid out in the reference
  image's own pixel space, origin top-left.  ``_Map.p`` maps a reference pixel
  to sheet millimetres (x stretched to the drawable width, y to its height).
* MILLIMETRES — letterforms, circles, discs and arrowheads are built directly
  in mm at a UNIFORM scale (``_Map.s``) so glyphs and rings never shear when
  the reference aspect (0.800) is fitted to A4 portrait's drawable (0.686).

The maths
---------
WAVE PACKET (the plate's core primitive, used for Q, K, V, Z and Y):

    f(x) = SUM_i  A_i * exp(-((x - c_i)/s_i)^2) * cos(2*pi*(x - c_i)/L_i + p_i)
    env(x) = SUM_i A_i * exp(-((x - c_i)/s_i)^2)

carrier x Gaussian envelope; ``env`` is drawn as the faint outline above and
below the axis.  Rows carry 2-3 superposed packets, which is what produces the
small ripple where two Gaussian tails overlap.

INTERFERENCE FIGURE (the hero) — a real two-source field, not faked.  The
instantaneous superposition of two point sources is

    A(x, y) = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2),      k = 2*pi/L

and what the reference draws are its RIDGE lines — the wave crests, cos(k r_s)
= 1, i.e. the Huygens loci r_s = m L.  (A level set of A is the wrong object: it
draws every fringe twice and closes into a lattice of blobs, which is visibly
not the reference.)  Each family is therefore a set of concentric circles about
its own source; the two families cross on the hyperbolae r1 - r2 = const, which
is the interference.  Near a source the 1/sqrt(r) weight makes that term
dominate and the field reads as clean concentric rings; between the sources the
two families are tangent along the axis and cut the lens-shaped cells that read
as the fine vertical comb down the middle.  The separation is a whole number of
wavelengths (d = 35 L) so crest m of one family meets crest 35-m of the other
exactly ON the axis rather than beating against it.

A parallel-crowding guard (``_Guard``) drops a crest point only where another
stroke runs within 0.82 mm of it AND within 25 degrees of parallel, so genuine
crossings survive and only unplottable tangency crowding is removed.

Entry point: ``attention_as_resonance``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.kit import (  # noqa: F401
    _GLYPHS,
    _dot,
    _poly,
    circle,
    fill_disc,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

REF_W, REF_H = 1122.0, 1402.0

# palette slots — crimson, dodgerblue, goldenrod, forestgreen, darkviolet, black
RED, BLUE, OCHRE, GREEN, PURPLE, BLACK = 0, 1, 2, 3, 4, 5


# ---------------------------------------------------------------------------
# sheet mapping
# ---------------------------------------------------------------------------


class _Map:
    """Reference pixels -> sheet millimetres."""

    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.sx = (x1 - x0) / REF_W
        self.sy = (y1 - y0) / REF_H

    def p(self, px: float, py: float) -> Tuple[float, float]:
        return (self.x0 + px * self.sx, self.y1 - py * self.sy)

    def s(self, v: float) -> float:
        """Uniform length (mm) for a reference-pixel length."""
        return v * self.sx


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# emit helpers
# ---------------------------------------------------------------------------


def _line(M: _Map, pts: Sequence[Tuple[float, float]], pen=None, f: int = 2000):
    return _poly([M.p(x, y) for x, y in pts], color=pen, f=f)


# Juan, 2026-09-28: "the original was much more beautiful — we just needed the dot lines to be
# more continuous, not to remove the waves". v13 drew every "dot" as a 0.42 mm micro-dash with
# 1.8 mm of paper after it, which reads as a broken dash. The only change in this round: a
# dot-sized mark (dash <= DOT_MAX) becomes one round dot, laid at an even arclength pitch with
# a dot on both ends. Longer dashes and everything else are v13 untouched.
DOT_PITCH = 1.0   # mm, centre to centre
DOT_R = 0.15      # _dot is a 2r hairline tick: a round dot at tip scale
DOT_MAX = 0.6     # marks this short were meant as dots


def _dotted_mm(pts, pen=None):
    """Round dots at an even arclength pitch along a polyline in mm, both ends anchored."""
    segs, total = [], 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L > 1e-9:
            segs.append((a, b, total, L))
            total += L
    if not segs:
        return []
    n = max(1, round(total / DOT_PITCH))
    out: List[GCodeCommand] = []
    k, si = 0, 0
    while k <= n:
        target = total * k / n
        while si < len(segs) - 1 and segs[si][2] + segs[si][3] < target:
            si += 1
        a, b, s0, L = segs[si]
        t = min(1.0, max(0.0, (target - s0) / L))
        out += _dot(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, DOT_R, color=pen)
        k += 1
    return out


def _dash_mm(pts, dash: float, gap: float, pen=None, f: int = 2000, step: float = 0.13):
    """Dash/dot an arbitrary polyline given in MILLIMETRES."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    if dash <= DOT_MAX:
        return _dotted_mm(pts, pen=pen)
    samples = []
    s = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        n = max(1, int(L / step))
        for k in range(n):
            t = k / n
            samples.append((a[0] + dx * t, a[1] + dy * t, s + L * t))
        s += L
    samples.append((pts[-1][0], pts[-1][1], s))
    period = dash + gap
    out: List[GCodeCommand] = []
    run: List[Tuple[float, float]] = []
    for x, y, ss in samples:
        if (ss % period) < dash:
            run.append((x, y))
        else:
            if len(run) >= 2:
                out += _poly(run, color=pen, f=f)
            elif run:
                out += _dot(run[0][0], run[0][1], max(dash * 0.45, 0.16), color=pen)
            run = []
    if len(run) >= 2:
        out += _poly(run, color=pen, f=f)
    elif run:
        out += _dot(run[0][0], run[0][1], max(dash * 0.45, 0.16), color=pen)
    return out


def _dash(M: _Map, pts, dash: float = 0.45, gap: float = 1.55, pen=None, f: int = 2000):
    """Dotted/dashed path given in REFERENCE PIXELS."""
    return _dash_mm([M.p(x, y) for x, y in pts], dash, gap, pen=pen, f=f)


def _ocirc(M: _Map, px: float, py: float, r_px: float, pen=None, n: int = 40):
    cx, cy = M.p(px, py)
    return circle(cx, cy, M.s(r_px), pen=pen, n=n)


def _fdot(M: _Map, px: float, py: float, r_px: float, pen=None):
    cx, cy = M.p(px, py)
    r = M.s(r_px)
    if r <= 0.32:
        return _dot(cx, cy, max(r, 0.14), color=pen)
    return fill_disc(cx, cy, r, spacing=0.3, pen=pen)


def _lead_dots(M: _Map, x_from: float, step: float, n: int, y: float, r: float, pen=None):
    """The '· · · ·' axis continuation.  ``step`` may be negative (leftward)."""
    out: List[GCodeCommand] = []
    for k in range(n):
        out += _fdot(M, x_from + step * k, y, r, pen=pen)
    return out


def _bez(p0, c1, c2, p1, n: int = 64):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        x = u * u * u * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * p1[0]
        y = u * u * u * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * p1[1]
        out.append((x, y))
    return out


def _arrow(M: _Map, px: float, py: float, direction: int, size_px: float = 8.0, pen=None):
    """Solid triangular arrowhead; direction -1 points left, +1 points right."""
    cx, cy = M.p(px, py)
    L = M.s(size_px)
    hb = L * 0.62
    out: List[GCodeCommand] = []
    out += _poly(
        [(cx, cy), (cx - direction * L, cy + hb), (cx - direction * L, cy - hb), (cx, cy)],
        color=pen,
        f=1600,
    )
    n = max(2, int(hb * 2 / 0.32))
    for i in range(1, n):
        t = i / n
        yy = -hb + 2 * hb * t
        frac = 1.0 - abs(yy) / hb
        out += _poly([(cx - direction * L * frac, cy + yy), (cx - direction * L, cy + yy)],
                     color=pen, f=1600)
    return out


# ---------------------------------------------------------------------------
# type — the stock single-stroke caps plus a lowercase set and the two maths
# glyphs the plate needs (partial-derivative and radical).
# ---------------------------------------------------------------------------

_LOWER = {
    "a": [
        [(0.3, 3.4), (1.2, 4.0), (2.4, 4.0), (3.2, 3.3), (3.2, 0.0)],
        [(3.2, 2.0), (1.2, 2.0), (0.3, 1.3), (0.3, 0.7), (1.2, 0.0), (2.4, 0.0), (3.2, 0.7)],
    ],
    "b": [
        [(0.3, 6.0), (0.3, 0.0)],
        [(0.3, 0.9), (1.1, 0.0), (2.4, 0.0), (3.2, 0.9), (3.2, 3.1), (2.4, 4.0), (1.1, 4.0), (0.3, 3.1)],
    ],
    "c": [[(3.2, 3.3), (2.4, 4.0), (1.1, 4.0), (0.3, 3.1), (0.3, 0.9), (1.1, 0.0), (2.4, 0.0), (3.2, 0.7)]],
    "d": [
        [(3.2, 6.0), (3.2, 0.0)],
        [(3.2, 3.1), (2.4, 4.0), (1.1, 4.0), (0.3, 3.1), (0.3, 0.9), (1.1, 0.0), (2.4, 0.0), (3.2, 0.9)],
    ],
    "e": [
        [
            (0.3, 2.0), (3.3, 2.0), (3.3, 3.1), (2.4, 4.0), (1.1, 4.0), (0.3, 3.1),
            (0.3, 0.9), (1.1, 0.0), (2.6, 0.0), (3.3, 0.7),
        ]
    ],
    "f": [[(0.3, 4.0), (2.7, 4.0)], [(1.4, 0.0), (1.4, 5.2), (2.1, 6.0), (3.0, 6.0)]],
    "g": [
        [(3.2, 4.0), (3.2, -0.8), (2.5, -1.6), (1.2, -1.6), (0.5, -1.0)],
        [(3.2, 3.1), (2.4, 4.0), (1.1, 4.0), (0.3, 3.1), (0.3, 0.9), (1.1, 0.0), (2.4, 0.0), (3.2, 0.9)],
    ],
    "h": [[(0.3, 6.0), (0.3, 0.0)], [(0.3, 3.2), (1.2, 4.0), (2.4, 4.0), (3.2, 3.2), (3.2, 0.0)]],
    "i": [[(1.8, 0.0), (1.8, 4.0)], [(1.8, 5.0), (1.8, 5.7)]],
    "k": [[(0.4, 6.0), (0.4, 0.0)], [(3.2, 4.0), (0.4, 1.6)], [(1.5, 2.5), (3.2, 0.0)]],
    "l": [[(1.6, 6.0), (1.6, 0.8), (2.3, 0.0), (3.0, 0.0)]],
    "m": [
        [(0.3, 0.0), (0.3, 4.0)],
        [(0.3, 3.3), (0.9, 4.0), (1.5, 3.3), (1.5, 0.0)],
        [(1.5, 3.3), (2.2, 4.0), (3.1, 3.3), (3.1, 0.0)],
    ],
    "n": [[(0.3, 0.0), (0.3, 4.0)], [(0.3, 3.2), (1.2, 4.0), (2.4, 4.0), (3.2, 3.2), (3.2, 0.0)]],
    "o": [[(1.1, 0.0), (0.3, 0.9), (0.3, 3.1), (1.1, 4.0), (2.4, 4.0), (3.2, 3.1), (3.2, 0.9), (2.4, 0.0), (1.1, 0.0)]],
    "p": [
        [(0.3, -1.6), (0.3, 4.0)],
        [(0.3, 3.1), (1.1, 4.0), (2.4, 4.0), (3.2, 3.1), (3.2, 0.9), (2.4, 0.0), (1.1, 0.0), (0.3, 0.9)],
    ],
    "r": [[(0.4, 0.0), (0.4, 4.0)], [(0.4, 3.0), (1.3, 4.0), (2.8, 4.0)]],
    "s": [
        [
            (3.2, 3.4), (2.5, 4.0), (1.1, 4.0), (0.3, 3.4), (0.3, 2.7), (3.2, 1.5),
            (3.2, 0.7), (2.5, 0.0), (1.0, 0.0), (0.3, 0.6),
        ]
    ],
    "t": [[(1.3, 6.0), (1.3, 0.9), (2.0, 0.0), (3.0, 0.0)], [(0.3, 4.0), (2.6, 4.0)]],
    "u": [[(0.3, 4.0), (0.3, 0.9), (1.1, 0.0), (2.4, 0.0), (3.2, 0.9)], [(3.2, 4.0), (3.2, 0.0)]],
    "v": [[(0.3, 4.0), (1.75, 0.0), (3.2, 4.0)]],
    "w": [[(0.2, 4.0), (1.0, 0.0), (1.75, 2.8), (2.5, 0.0), (3.3, 4.0)]],
    "x": [[(0.3, 4.0), (3.2, 0.0)], [(0.3, 0.0), (3.2, 4.0)]],
    "y": [
        [(0.3, 4.0), (0.3, 1.0), (1.1, 0.0), (2.4, 0.0), (3.2, 1.0)],
        [(3.2, 4.0), (3.2, -0.8), (2.5, -1.6), (1.2, -1.6)],
    ],
    "z": [[(0.3, 4.0), (3.2, 4.0), (0.3, 0.0), (3.2, 0.0)]],
}

_EXTRA = {
    # partial derivative: a bowl with a tail sweeping up to the left
    "@": [
        [(1.3, 0.0), (0.4, 0.9), (0.4, 2.3), (1.3, 3.2), (2.5, 3.2), (3.3, 2.3), (3.3, 0.9), (2.5, 0.0), (1.3, 0.0)],
        [(3.3, 1.6), (3.3, 3.7), (2.9, 4.9), (2.0, 5.8), (0.8, 6.0)],
    ],
    # radical: the tick plus an overbar that runs to the right edge
    "#": [[(0.0, 3.2), (0.7, 2.7), (1.6, 0.0), (2.8, 6.0), (5.4, 6.0)]],
}

_ADV = 5.6


def _strokes(ch: str):
    if ch in _EXTRA:
        return _EXTRA[ch]
    if ch in _LOWER:
        return _LOWER[ch]
    return _GLYPHS.get(ch.upper(), [])


def _tw(text: str, h_mm: float, tracking: float = 1.0) -> float:
    return len(text) * _ADV * (h_mm / 6.0) * tracking


def _type(
    M: _Map,
    text: str,
    px: float,
    py: float,
    h_px: float,
    pen=None,
    tracking: float = 1.0,
    center: bool = False,
    weight: float = 0.0,
    f: int = 2200,
):
    """Single-stroke type.  (px, py) is the LEFT BASELINE in reference pixels;
    the glyphs themselves are built in mm at uniform scale so they never shear."""
    ax, ay = M.p(px, py)
    h = M.s(h_px)
    sc = h / 6.0
    adv = _ADV * sc * tracking
    if center:
        ax -= _tw(text, h, tracking) / 2.0
    out: List[GCodeCommand] = []
    cx = ax
    for ch in text:
        if ch == ".":
            out += _dot(cx + 2.0 * sc, ay + 0.25 * sc, max(0.28 * sc, 0.16), color=pen)
        elif ch == "~":  # middle dot
            out += _fdot_mm(cx + 2.0 * sc, ay + 2.6 * sc, max(0.55 * sc, 0.32), pen)
        else:
            offs = [(0.0, 0.0)]
            if weight > 0:
                offs = [(0.0, 0.0), (weight, 0.0), (weight * 0.5, weight * 0.9)]
            for ox, oy in offs:
                for st in _strokes(ch):
                    out += _poly([(cx + gx * sc + ox, ay + gy * sc + oy) for gx, gy in st],
                                 color=pen, f=f)
        cx += adv
    return out


def _fdot_mm(cx: float, cy: float, r: float, pen=None):
    if r <= 0.32:
        return _dot(cx, cy, max(r, 0.14), color=pen)
    return fill_disc(cx, cy, r, spacing=0.3, pen=pen)


def _frac(
    M: _Map,
    num: str,
    den: str,
    px: float,
    py: float,
    h_px: float,
    pen=None,
    tracking: float = 1.0,
    gap_px: float = 4.2,
):
    """A true fraction: numerator, rule, denominator — centred on ``px``,
    with the rule at ``py``."""
    h = M.s(h_px)
    wn = _tw(num, h, tracking)
    wd = _tw(den, h, tracking)
    half = max(wn, wd) / 2.0 + M.s(2.0)
    rx, ry = M.p(px, py)
    out: List[GCodeCommand] = []
    out += _poly([(rx - half, ry), (rx + half, ry)], color=pen, f=2000)
    out += _type(M, num, px, py - h_px * 0.42 - gap_px, h_px, pen=pen, tracking=tracking, center=True)
    out += _type(M, den, px, py + h_px * 1.02 + gap_px, h_px, pen=pen, tracking=tracking, center=True)
    return out


# ---------------------------------------------------------------------------
# the wave packet — the plate's core primitive
# ---------------------------------------------------------------------------

Packet = Tuple[float, float, float, float, float]  # centre, sigma, lambda, amp, phase


def _pk_value(x: float, packets: Sequence[Packet]) -> float:
    v = 0.0
    for c, sg, lam, amp, ph in packets:
        t = (x - c) / sg
        if abs(t) > 3.4:
            continue
        v += amp * math.exp(-t * t) * math.cos(2 * math.pi * (x - c) / lam + ph)
    return v


def _pk_env(x: float, packets: Sequence[Packet]) -> float:
    v = 0.0
    for c, sg, lam, amp, ph in packets:
        t = (x - c) / sg
        if abs(t) > 3.4:
            continue
        v += amp * math.exp(-t * t)
    return v


def wave_packet(
    M: _Map,
    x0: float,
    x1: float,
    y: float,
    packets: Sequence[Packet],
    pen=None,
    envelope: bool = True,
    ghost: bool = False,
):
    """The plate's core primitive: carrier x Gaussian envelope on an axis line,
    with the envelope itself outlined above and below."""
    lam_min = min(p[2] for p in packets)
    step = max(lam_min / 14.0, 0.18)
    n = int((x1 - x0) / step) + 1
    xs = [x0 + k * step for k in range(n + 1)]
    out: List[GCodeCommand] = []

    curve = [(x, y - _pk_value(x, packets)) for x in xs]
    if ghost:
        out += _dash(M, curve, dash=0.42, gap=1.35, pen=pen)
    else:
        out += _line(M, curve, pen=pen, f=2400)

    if envelope:
        for sgn in (-1.0, 1.0):
            # the outline hugs the carrier crests, as the reference's faint
            # envelope does; it lifts off the axis so it never doubles the rail
            env = [(x, y + sgn * _pk_env(x, packets)) for x in xs]
            env = [(x, yy) for x, yy in env if abs(yy - y) > 3.2]
            if len(env) > 3:
                out += _dash_mm([M.p(a, b) for a, b in env], 0.85, 1.55, pen=pen)
    return out


# ---------------------------------------------------------------------------
# layout constants, traced off the reference (reference pixels)
# ---------------------------------------------------------------------------

TITLE_Y = 52.0
RULE_Y = 74.0

QK_ROWS = [164.0, 223.0, 282.0, 339.0, 396.0]
Q_HOME = 109.0            # the aligned column of Q node circles
K_HOME = REF_W - Q_HOME   # 1013 — the aligned column of K node circles

# per Q row: (axis end x, node circle x or None, filled?, tail dot x or None)
Q_ROWS = [
    (312.0, 287.0, False, 312.0),
    (356.0, 287.0, False, 356.0),
    (389.0, 389.0, False, None),
    (357.0, None, False, 357.0),
    (325.0, 325.0, False, None),
]
Q_HOME_FILLED = [False, True, False, True, False]

# per K row: (axis start x, node circle x or None, tail dot x or None)
K_ROWS = [
    (814.0, 836.0, 814.0),
    (767.0, 836.0, 767.0),
    (734.0, 734.0, None),
    (770.0, None, 770.0),
    (796.0, 796.0, None),
]
K_HOME_FILLED = [False, True, False, True, False]

Q_PACKETS: List[List[Packet]] = [
    [(225.0, 26.0, 12.0, 40.0, 0.0), (289.0, 10.0, 9.5, 17.0, 1.2), (160.0, 12.0, 7.5, 5.0, 0.4)],
    [(168.0, 23.0, 11.0, 34.0, 0.0), (306.0, 14.0, 11.0, 21.0, 0.6), (240.0, 10.0, 7.5, 4.0, 0.0)],
    [(252.0, 35.0, 18.0, 43.0, 0.0), (332.0, 12.0, 8.5, 13.0, 0.9), (192.0, 15.0, 9.0, 10.0, 0.3)],
    [(190.0, 25.0, 13.0, 29.0, 0.0), (331.0, 10.0, 9.5, 16.0, 0.5), (262.0, 10.0, 7.5, 5.0, 0.0)],
    [(243.0, 29.0, 12.0, 43.0, 0.0), (163.0, 11.0, 8.0, 6.0, 0.0)],
]

K_PACKETS: List[List[Packet]] = [
    [(950.0, 26.0, 12.0, 40.0, 0.0), (858.0, 10.0, 9.0, 16.0, 0.7), (1000.0, 11.0, 7.5, 6.0, 0.2)],
    [(944.0, 24.0, 11.0, 33.0, 0.0), (795.0, 13.0, 10.0, 20.0, 0.4), (880.0, 10.0, 7.5, 4.0, 0.0)],
    [(858.0, 33.0, 17.0, 41.0, 0.0), (962.0, 14.0, 8.5, 13.0, 1.1), (1000.0, 10.0, 7.0, 6.0, 0.5)],
    [(932.0, 25.0, 12.0, 33.0, 0.0), (790.0, 10.0, 9.0, 15.0, 0.9), (862.0, 10.0, 7.5, 5.0, 0.0)],
    [(884.0, 28.0, 11.0, 43.0, 0.0), (985.0, 11.0, 8.0, 6.0, 0.3)],
]

Q_VERTS = [  # vertical dotted guides in the Q block: (x, y_top, y_bottom)
    (109.0, 128.0, 412.0),
    (207.0, 100.0, 300.0),
    (287.0, 108.0, 352.0),
    (315.0, 162.0, 420.0),
    (356.0, 212.0, 402.0),
    (389.0, 262.0, 432.0),
]

# interference figure
IF_CX, IF_CY = 561.0, 611.0
IF_D = 250.0
IF_LAM = IF_D / 23.0
SRC_L, SRC_R = IF_CX - IF_D / 2, IF_CX + IF_D / 2

SOFT_BASE = 886.0
SOFT_PEAKS = [  # x, height, apex marker ('o' open, 'f' filled, None)
    (391.0, 45.0, "o"),
    (475.0, 85.0, "f"),
    (516.0, 24.0, None),
    (559.0, 61.0, "f"),
    (645.0, 85.0, "o"),
    (724.0, 45.0, "o"),
]
SOFT_GHOSTS = [(433.0, 26.0), (601.0, 30.0), (686.0, 26.0)]

V_ROWS = [769.0, 805.0, 839.0]
V_L, V_R = 725.0, 975.0

MOE_Y = 1073.0
ROUTER_X, NODE2_X = 527.0, 884.0
LANE_L, LANE_R = 611.0, 789.0
LANE_YS = [1010.0, 1044.0, 1073.0, 1103.0, 1148.0]

BACK_ROWS = [1191.0, 1235.0, 1271.0, 1314.0, 1357.0]
BACK_COL = 282.0


# ---------------------------------------------------------------------------
# sections
# ---------------------------------------------------------------------------


def _title(M: _Map, colors: int):
    bk = _pen(BLACK, colors)
    out = _type(M, "ATTENTION AS RESONANCE", 561.0, TITLE_Y, 20.0, pen=bk,
                tracking=1.72, center=True, weight=0.24)
    ax, ay = M.p(492.0, RULE_Y)
    bx, _ = M.p(630.0, RULE_Y)
    out += _poly([(ax, ay), (bx, ay)], color=bk, f=2000)
    out += _fdot(M, 561.0, RULE_Y, 2.4, pen=bk)
    return out


def _qk_block(M: _Map, colors: int, side: int, pen):
    """side = +1 Q (left block, continuations leftward), -1 K (right, mirrored).

    Q and K are NOT a literal mirror of one another in the reference; each block
    carries its own traced row geometry and its own packet parameters.
    """

    def mx(x: float) -> float:
        return x if side > 0 else REF_W - x

    home = Q_HOME if side > 0 else K_HOME
    filled = Q_HOME_FILLED if side > 0 else K_HOME_FILLED
    out: List[GCodeCommand] = []

    for i, y in enumerate(QK_ROWS):
        if side > 0:
            far, circ, tail = Q_ROWS[i][0], Q_ROWS[i][1], Q_ROWS[i][3]
            pk = Q_PACKETS[i]
        else:
            far, circ, tail = K_ROWS[i]
            pk = K_PACKETS[i]
        lo, hi = (home, far) if side > 0 else (far, home)

        out += _line(M, [(lo, y), (hi, y)], pen=pen)
        out += wave_packet(M, lo + 2.0, hi - 2.0, y, pk, pen=pen)
        if filled[i]:
            out += _fdot(M, home, y, 4.6, pen=pen)
        else:
            out += _ocirc(M, home, y, 4.8, pen=pen)
        if circ is not None:
            out += _ocirc(M, circ, y, 5.4, pen=pen)
        if tail is not None:
            out += _fdot(M, tail, y, 3.4, pen=pen)
        out += _lead_dots(M, home - side * 21.0, -side * 12.0, 4, y, 2.4, pen=pen)

    for x, yt, yb in Q_VERTS:
        out += _dash(M, [(mx(x), yt), (mx(x), yb)], dash=0.5, gap=1.7, pen=pen)
        out += _fdot(M, mx(x), yt - 6.0, 2.2, pen=pen)

    lx = 92.0 if side > 0 else REF_W - 133.0
    out += _type(M, "Q" if side > 0 else "K", lx, 124.0, 38.0, pen=pen, weight=0.46)

    for i, y in enumerate(QK_ROWS):
        end_x = Q_ROWS[i][0] if side > 0 else REF_W - K_ROWS[i][0]
        x_start = mx(end_x + 12.0)
        tx = mx(408.0 + 15.0 * i)
        ty = 446.0 + 26.0 * i
        c1 = (mx(end_x + 86.0 + 16.0 * i), y + 10.0)
        c2 = (mx(492.0 + 6.0 * i), 352.0 + 20.0 * i)
        out += _dash(M, _bez((x_start, y), c1, c2, (tx, ty)), dash=0.5, gap=1.85, pen=pen)
        out += _fdot(M, tx, ty, 3.0, pen=pen)
        c1b = (mx(end_x + 128.0 + 20.0 * i), y + 18.0)
        c2b = (mx(524.0 + 8.0 * i), 366.0 + 20.0 * i)
        tx2, ty2 = mx(386.0 + 13.0 * i), 470.0 + 24.0 * i
        out += _dash(M, _bez((x_start, y + 6.0), c1b, c2b, (tx2, ty2)),
                     dash=0.45, gap=2.1, pen=pen)
        out += _fdot(M, tx2, ty2, 2.2, pen=pen)
    return out


def _centre_fraction(M: _Map, colors: int):
    """Q . K^T over a rule over sqrt(d_k) — a true stacked fraction."""
    bk = _pen(BLACK, colors)
    out: List[GCodeCommand] = []
    for j in range(3):
        out += _fdot(M, 561.0, 332.0 + 11.0 * j, 1.7, pen=bk)

    h = 23.0
    hm = M.s(h)
    num = "Q~K"
    tr = 1.16
    wn_px = _tw(num, hm, tr) / M.sx
    nx = 561.0 - 5.0
    out += _type(M, num, nx, 392.0, h, pen=bk, tracking=tr, center=True, weight=0.2)
    out += _type(M, "T", nx + wn_px / 2.0 + 1.5, 381.0, 12.5, pen=bk, weight=0.16)

    ax, ay = M.p(507.0, 404.0)
    bx, _ = M.p(616.0, 404.0)
    out += _poly([(ax, ay), (bx, ay)], color=bk, f=2000)

    out += _type(M, "#d", 529.0, 434.0, 21.0, pen=bk, tracking=1.0, weight=0.16)
    out += _type(M, "k", 568.0, 438.0, 12.0, pen=bk, weight=0.14)
    return out


class _Guard:
    """Parallel-crowding guard, in MILLIMETRES.

    Two crest families inevitably run TANGENT to one another along the axis of
    a two-source diagram, which is the one place a pen cannot resolve them.  A
    plain occupancy grid also deletes the CROSSINGS, which are the whole point,
    so this one rejects a point only when a nearby point of another stroke is
    within ``sep`` AND its tangent is within 25 degrees of parallel.  Crossings
    at any real angle pass straight through.
    """

    def __init__(self, sep: float = 0.82) -> None:
        self.sep = sep
        self.s2 = sep * sep
        self.g: dict = {}

    def ok(self, x: float, y: float, ux: float, uy: float, sid: int) -> bool:
        cx, cy = int(x / self.sep), int(y / self.sep)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for qx, qy, qu, qv, qs in self.g.get((cx + dx, cy + dy), ()):
                    if qs == sid or abs(ux * qu + uy * qv) < 0.906:
                        continue
                    if (qx - x) ** 2 + (qy - y) ** 2 < self.s2:
                        return False
        return True

    def add(self, x: float, y: float, ux: float, uy: float, sid: int) -> None:
        self.g.setdefault((int(x / self.sep), int(y / self.sep)), []).append(
            (x, y, ux, uy, sid))


def _interference(M: _Map, rng: SeededRNG, colors: int):
    """The hero, computed as a real two-source field.

    Huygens construction: a crest of the wave from source s is the locus
    r_s = m * L.  Drawing both crest families is exactly

        cos(k r1) = 1   and   cos(k r2) = 1,        k = 2 pi / L

    i.e. the ridge lines of the instantaneous superposition
    A(x, y) = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2), rather than a level set
    of it (a level set draws each fringe twice and closes into blobs).  The two
    families cross on the hyperbolae r1 - r2 = const; between the sources those
    crossings pack into the fine vertical comb, and the lens-shaped cells they
    cut near the midpoint are what reads as a third ring system.

    The separation is an exact whole number of wavelengths (d = 35 L) so the
    two families meet ON the axis instead of beating against it.
    """
    bk = _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    n_lam = 35
    lam = IF_D / n_lam                     # 7.14 ref px = 1.21 mm across, 1.41 mm down
    a_out, b_out = 272.0, 158.0
    sid = 0
    guard = _Guard(0.82)

    def ring(cx: float, cy: float, r: float):
        n = max(64, int(r * 2.6))
        return [
            (cx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n))
            for t in range(n + 1)
        ]

    def emit_clipped(pts, dotted: bool = False, keep_out=None):
        """Solid crests are clipped to a tighter lens than the dotted ones, so
        the field fades outward the way the reference's tone does."""
        nonlocal sid
        sid += 1
        aa, bb = (a_out, b_out) if dotted else (a_out * 0.80, 126.0)
        res: List[GCodeCommand] = []
        run = []
        for j, (px, py) in enumerate(pts):
            ok = ((px - IF_CX) / aa) ** 2 + ((py - IF_CY) / bb) ** 2 <= 1.0
            if ok and keep_out is not None:
                ox, oy, orr = keep_out
                ok = math.hypot(px - ox, py - oy) > orr
            if ok and not dotted:
                qx, qy = pts[min(j + 1, len(pts) - 1)]
                mx_, my_ = M.p(px, py)
                nx_, ny_ = M.p(qx, qy)
                du, dv = nx_ - mx_, ny_ - my_
                dn = math.hypot(du, dv) or 1.0
                du, dv = du / dn, dv / dn
                if guard.ok(mx_, my_, du, dv, sid):
                    guard.add(mx_, my_, du, dv, sid)
                else:
                    ok = False
            if ok:
                run.append((px, py))
            else:
                if len(run) >= 4:
                    res += (_dash(M, run, dash=0.42, gap=1.8, pen=bk) if dotted
                            else _line(M, run, pen=bk, f=2600))
                run = []
        if len(run) >= 4:
            res += (_dash(M, run, dash=0.42, gap=1.8, pen=bk) if dotted
                    else _line(M, run, pen=bk, f=2600))
        return res

    r_solid = 21
    for sx in (SRC_L, SRC_R):
        other = SRC_R if sx == SRC_L else SRC_L
        for m in range(1, r_solid + 1):              # solid crests
            out += emit_clipped(ring(sx, IF_CY, m * lam))
        for m in range(r_solid + 1, 52):             # the tonal fade-out
            out += emit_clipped(ring(sx, IF_CY, m * lam), dotted=True,
                                keep_out=(other, IF_CY, r_solid * lam + 6.0))

    # --- outer sparse dotted ellipses around each source -------------------
    for sx in (SRC_L, SRC_R):
        for a in (152.0, 190.0, 232.0):
            b = a * 0.60
            rr = [
                (sx + a * math.cos(2 * math.pi * t / 240),
                 IF_CY + b * math.sin(2 * math.pi * t / 240))
                for t in range(241)
            ]
            rr = [q for q in rr
                  if M.x0 + 2 < M.p(*q)[0] < M.x1 - 2
                  and min(math.hypot(q[0] - SRC_L, q[1] - IF_CY),
                          math.hypot(q[0] - SRC_R, q[1] - IF_CY)) > 21 * lam + 8.0]
            if len(rr) > 6:
                out += _dash(M, rr, dash=0.42, gap=1.9, pen=bk)

    # --- the horizontal axis through the figure ---------------------------
    ax, ay = M.p(300.0, IF_CY)
    bx, _ = M.p(822.0, IF_CY)
    out += _poly([(ax, ay), (bx, ay)], color=bk, f=2000)
    for sgn in (1, -1):
        base = IF_CX - sgn * 334.0
        out += _ocirc(M, base, IF_CY, 5.0, pen=bk)
        for j in range(4):
            out += _fdot(M, base - sgn * (17.0 + 17.0 * j), IF_CY, 2.3, pen=bk)
        out += _fdot(M, IF_CX - sgn * 305.0, IF_CY, 3.2, pen=bk)
        out += _fdot(M, IF_CX - sgn * 266.0, IF_CY, 3.4, pen=bk)
        cxx = IF_CX - sgn * 203.0
        out += _ocirc(M, cxx, IF_CY, 6.2, pen=bk)
        out += _fdot(M, cxx, IF_CY, 2.2, pen=bk)
    out += _fdot(M, IF_CX, IF_CY, 5.0, pen=bk)
    out += _fdot(M, SRC_L, IF_CY, 4.8, pen=bk)
    out += _fdot(M, SRC_R, IF_CY, 4.8, pen=bk)

    # --- the dot field ----------------------------------------------------
    k = 2 * math.pi / lam

    def field(px, py):
        d1 = math.hypot(px - SRC_L, py - IF_CY) + 4.0
        d2 = math.hypot(px - SRC_R, py - IF_CY) + 4.0
        return math.cos(k * d1) / math.sqrt(d1) + math.cos(k * d2) / math.sqrt(d2)

    placed: List[Tuple[float, float, float]] = []

    def place(px, py, r):
        if r < 0.7 or not (M.x0 + 3 < M.p(px, py)[0] < M.x1 - 3):
            return []
        for qx, qy, qr in placed:
            if math.hypot(px - qx, py - qy) < (r + qr) * 1.3 + 4.0:
                return []
        placed.append((px, py, r))
        return _fdot(M, px, py, r, pen=bk)

    for cx in (SRC_L, IF_CX, SRC_R):
        for j in range(-6, 7):
            if j:
                out += place(cx, IF_CY + 24.0 * j, 1.7 + 4.2 * math.exp(-abs(j) / 3.4))
    for sx in (SRC_L, SRC_R):
        for t in range(12):
            th = 2 * math.pi * t / 12 + 0.09
            for rr in (46.0, 84.0, 122.0, 160.0, 198.0):
                px = sx + rr * math.cos(th)
                py = IF_CY + rr * 0.62 * math.sin(th)
                out += place(px, py, 1.1 + 22.0 * abs(field(px, py)))
    for _ in range(60):
        px = IF_CX + rng.uniform(-228.0, 228.0)
        py = IF_CY + rng.uniform(-145.0, 145.0)
        out += place(px, py, 0.9 + 16.0 * abs(field(px, py)))

    # --- vertical dotted droplines, up and down ---------------------------
    drops = [434.0, 477.0, 516.0, 561.0, 613.0, 652.0, 691.0]
    for j, x in enumerate(drops):
        top = 462.0 if x in (434.0, 561.0, 691.0) else 496.0
        out += _dash(M, [(x, top), (x, IF_CY - 6.0)], dash=0.5, gap=1.7, pen=bk)
        out += _fdot(M, x, top - 8.0, 2.0, pen=bk)
        bot = 832.0 if j % 2 == 0 else 806.0
        out += _dash(M, [(x, IF_CY + 6.0), (x, bot)], dash=0.5, gap=1.7, pen=bk)
    out += _ocirc(M, IF_CX, 486.0, 4.8, pen=bk)
    out += _ocirc(M, IF_CX, 716.0, 4.8, pen=bk)
    return out


def _softmax(M: _Map, colors: int):
    bk = _pen(BLACK, colors)
    out: List[GCodeCommand] = []
    x0, x1 = 313.0, 806.0

    def curve_y(x: float) -> float:
        v = 0.0
        for cx, h, _m in SOFT_PEAKS:
            v += h / (1.0 + ((x - cx) / 9.5) ** 2) ** 1.6
        return SOFT_BASE - v

    n = int((x1 - x0) / 0.7)
    pts = [(x0 + k * (x1 - x0) / n, 0.0) for k in range(n + 1)]
    pts = [(x, curve_y(x)) for x, _ in pts]
    out += _line(M, pts, pen=bk, f=2400)

    # ghost peaks
    for cx, h in SOFT_GHOSTS:
        gp = [
            (cx - 26.0 + t * 0.9, SOFT_BASE - h / (1.0 + ((cx - 26.0 + t * 0.9 - cx) / 8.0) ** 2) ** 1.6)
            for t in range(59)
        ]
        out += _dash(M, gp, dash=0.42, gap=1.5, pen=bk)

    # stems + apex markers
    for cx, h, m in SOFT_PEAKS:
        out += _line(M, [(cx, SOFT_BASE), (cx, SOFT_BASE - h + 2.0)], pen=bk)
        if m == "o":
            out += _ocirc(M, cx, SOFT_BASE - h - 3.0, 5.0, pen=bk)
        elif m == "f":
            out += _fdot(M, cx, SOFT_BASE - h - 3.0, 4.4, pen=bk)

    # baseline markers
    for x, kind in [
        (321.0, "f"), (391.0, "f"), (434.0, "o"), (475.0, "o"), (516.0, "f"),
        (559.0, "o"), (601.0, "o"), (645.0, "o"), (686.0, "o"), (724.0, "f"), (799.0, "f"),
    ]:
        if kind == "o":
            out += _ocirc(M, x, SOFT_BASE, 4.4, pen=bk)
        else:
            out += _fdot(M, x, SOFT_BASE, 3.2, pen=bk)

    # '· · ·' both ends
    out += _lead_dots(M, 303.0, -14.0, 3, SOFT_BASE, 2.4, pen=bk)
    out += _lead_dots(M, 818.0, 14.0, 3, SOFT_BASE, 2.4, pen=bk)

    out += _type(M, "softmax", 561.0, 786.0, 20.0, pen=bk, tracking=1.16, center=True, weight=0.16)
    return out


def _v_block(M: _Map, colors: int):
    oc = _pen(OCHRE, colors)
    out: List[GCodeCommand] = []
    packs = [
        [(903.0, 32.0, 12.5, 28.0, 0.0), (800.0, 17.0, 9.0, 12.0, 0.5)],
        [(862.0, 27.0, 11.5, 25.0, 0.0), (778.0, 15.0, 8.5, 13.0, 0.8)],
        [(878.0, 25.0, 14.0, 22.0, 0.0), (790.0, 14.0, 9.5, 11.0, 0.3)],
    ]
    for i, y in enumerate(V_ROWS):
        out += _line(M, [(V_L, y), (V_R, y)], pen=oc)
        out += wave_packet(M, V_L + 2.0, V_R - 2.0, y, packs[i], pen=oc)
        if i == 2:
            out += _fdot(M, V_L, y, 4.4, pen=oc)
        else:
            out += _ocirc(M, V_L, y, 4.8, pen=oc)
        out += _ocirc(M, V_R, y, 4.8, pen=oc)
        out += _lead_dots(M, V_R + 24.0, 14.0, 4, y, 2.4, pen=oc)
        # dotted feed from the softmax band into the row
        out += _dash(M, [(688.0, y), (V_L - 8.0, y)], dash=0.5, gap=1.7, pen=oc)
        out += _fdot(M, 684.0, y, 2.2, pen=oc)
    out += _type(M, "V", 1022.0, 748.0, 34.0, pen=oc, weight=0.46)
    # ochre droplines from the softmax baseline down towards the MoE band
    for i, x in enumerate([391.0, 434.0, 475.0, 516.0, 559.0, 601.0]):
        pts = _bez((x, SOFT_BASE + 8.0), (x + 4.0, 960.0), (x + 46.0 + 9.0 * i, 1010.0), (x + 74.0 + 12.0 * i, 1080.0))
        out += _dash(M, pts, dash=0.45, gap=1.9, pen=oc)
    return out


def _moe_row(M: _Map, colors: int):
    gr = _pen(GREEN, colors)
    pu = _pen(PURPLE, colors)
    bk = _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    # ---- Z = AV ---------------------------------------------------------
    zp: List[Packet] = [
        (277.0, 47.0, 13.5, 68.0, 0.0),
        (178.0, 13.0, 8.5, 15.0, 0.4),
        (443.0, 13.0, 8.5, 14.0, 0.9),
        (352.0, 9.0, 7.5, 8.0, 0.2),
    ]
    out += _line(M, [(110.0, MOE_Y), (ROUTER_X - 14.0, MOE_Y)], pen=gr)
    out += wave_packet(M, 112.0, ROUTER_X - 18.0, MOE_Y, zp, pen=gr)
    out += _ocirc(M, 110.0, MOE_Y, 4.8, pen=gr)
    for x in (178.0, 315.0, 443.0, 490.0):
        out += _ocirc(M, x, MOE_Y, 4.4, pen=gr)
    out += _lead_dots(M, 88.0, -13.0, 4, MOE_Y, 2.4, pen=gr)
    out += _fdot(M, 277.0, MOE_Y - 72.0, 4.6, pen=gr)
    out += _fdot(M, 277.0, MOE_Y + 72.0, 4.6, pen=gr)
    out += _type(M, "Z = AV", 100.0, 1018.0, 30.0, pen=gr, tracking=0.98, weight=0.42)

    # ---- MoE header -----------------------------------------------------
    out += _type(M, "MoE", 706.0, 948.0, 22.0, pen=bk, tracking=1.02, center=True, weight=0.2)
    for a, b in ((618.0, 668.0), (746.0, 796.0)):
        p0, p1 = M.p(a, 941.0), M.p(b, 941.0)
        out += _poly([p0, p1], color=bk, f=2000)
    out += _type(M, "experts", 714.0, 976.0, 15.0, pen=pu, tracking=1.1, center=True)
    out += _type(M, "top-2", 848.0, 999.0, 15.0, pen=pu, tracking=1.1, center=True)
    out += _type(M, "router", 529.0, 1049.0, 15.0, pen=pu, tracking=1.1, center=True)

    # ---- router / gather nodes -----------------------------------------
    for nx in (ROUTER_X, NODE2_X):
        out += _ocirc(M, nx, MOE_Y, 12.5, pen=pu)
        out += _ocirc(M, nx, MOE_Y, 8.0, pen=pu)
        out += _fdot(M, nx, MOE_Y, 3.4, pen=pu)

    # ---- expert lanes ---------------------------------------------------
    lane_pk: List[List[Packet]] = [
        [(700.0, 23.0, 8.0, 24.0, 0.0), (743.0, 12.0, 6.6, 11.0, 0.7)],
        [(700.0, 20.0, 7.6, 10.0, 0.0)],
        [(700.0, 20.0, 7.6, 10.0, 0.4)],
        [(700.0, 20.0, 7.6, 10.0, 0.8)],
        [(706.0, 27.0, 8.0, 27.0, 0.0), (752.0, 13.0, 6.8, 12.0, 0.5)],
    ]
    for i, y in enumerate(LANE_YS):
        selected = i in (0, 4)
        if selected:
            out += _line(M, [(LANE_L, y), (LANE_R, y)], pen=pu)
            out += wave_packet(M, LANE_L + 4.0, LANE_R - 4.0, y, lane_pk[i], pen=pu)
            out += _ocirc(M, LANE_L, y, 5.6, pen=pu)
            out += _ocirc(M, LANE_R, y, 5.6, pen=pu)
            sgn = -1 if i == 0 else 1
            out += _line(M, _bez((ROUTER_X + 13.0, MOE_Y), (ROUTER_X + 58.0, MOE_Y),
                                 (LANE_L - 42.0, y), (LANE_L - 6.0, y)), pen=pu)
            out += _line(M, _bez((LANE_R + 6.0, y), (LANE_R + 42.0, y),
                                 (NODE2_X - 50.0, MOE_Y), (NODE2_X - 13.0, MOE_Y)), pen=pu)
            out += _fdot(M, LANE_L - 24.0, y + sgn * -12.0 * 0.0, 3.0, pen=pu)
            out += _fdot(M, LANE_R + 26.0, y, 3.0, pen=pu)
        else:
            out += _dash(M, [(LANE_L, y), (LANE_L + 52.0, y)], dash=0.4, gap=2.1, pen=pu)
            out += _dash(M, [(LANE_R - 52.0, y), (LANE_R, y)], dash=0.4, gap=2.1, pen=pu)
            out += wave_packet(M, LANE_L + 8.0, LANE_R - 8.0, y, lane_pk[i], pen=pu,
                               envelope=False, ghost=True)
            out += _ocirc(M, LANE_L, y, 5.0, pen=pu, n=28)
            out += _ocirc(M, LANE_R, y, 5.0, pen=pu, n=28)
            out += _dash(M, _bez((ROUTER_X + 13.0, MOE_Y), (ROUTER_X + 54.0, MOE_Y),
                                 (LANE_L - 40.0, y), (LANE_L - 6.0, y)), dash=0.45, gap=1.8, pen=pu)
            out += _dash(M, _bez((LANE_R + 6.0, y), (LANE_R + 40.0, y),
                                 (NODE2_X - 48.0, MOE_Y), (NODE2_X - 13.0, MOE_Y)), dash=0.45, gap=1.8, pen=pu)

    # ---- Y --------------------------------------------------------------
    yp: List[Packet] = [(978.0, 31.0, 11.0, 40.0, 0.0), (1030.0, 11.0, 7.5, 11.0, 0.6)]
    out += _line(M, [(NODE2_X + 14.0, MOE_Y), (1052.0, MOE_Y)], pen=pu)
    out += wave_packet(M, NODE2_X + 16.0, 1050.0, MOE_Y, yp, pen=pu)
    out += _ocirc(M, 1052.0, MOE_Y, 4.8, pen=pu)
    out += _lead_dots(M, 1072.0, 13.0, 3, MOE_Y, 2.4, pen=pu)
    out += _type(M, "Y", 1020.0, 1030.0, 30.0, pen=pu, weight=0.46)
    # V -> the gather node
    oc = _pen(OCHRE, colors)
    out += _dash(M, _bez((975.0 + 22.0, V_ROWS[2]), (1070.0, 900.0), (1010.0, 1010.0), (NODE2_X + 16.0, MOE_Y - 6.0)),
                 dash=0.45, gap=1.9, pen=oc)
    return out


def _backward(M: _Map, colors: int):
    out: List[GCodeCommand] = []
    pens = [_pen(RED, colors), _pen(BLUE, colors), _pen(OCHRE, colors),
            _pen(BLACK, colors), _pen(GREEN, colors)]
    dens = ["Q", "K", "V", "A", "Z"]
    for i, y in enumerate(BACK_ROWS):
        pn = pens[i]
        out += _frac(M, "@L", "@" + dens[i], 62.0, y, 14.0, pen=pn, tracking=1.02)
        out += _arrow(M, 104.0, y, -1, 8.5, pen=pn)
        out += _dash(M, [(118.0, y), (BACK_COL - 7.0, y)], dash=0.5, gap=1.7, pen=pn)
        out += _ocirc(M, BACK_COL, y, 4.6, pen=pn)
        # the return path up into the plate
        tx = 500.0 + 58.0 * i
        ty = 1010.0 - 14.0 * i
        out += _dash(M, _bez((BACK_COL + 7.0, y), (BACK_COL + 120.0 + 20.0 * i, y),
                             (tx - 120.0, ty + 90.0), (tx, ty)), dash=0.45, gap=1.9, pen=pn)

    # short coloured droplines falling out of the Z row, as in the reference
    for xx, pn, y_to in ((336.0, _pen(RED, colors), 1196.0),
                         (377.0, _pen(BLUE, colors), 1170.0),
                         (415.0, _pen(OCHRE, colors), 1150.0)):
        out += _dash(M, [(xx, MOE_Y + 26.0), (xx, y_to)], dash=0.5, gap=1.8, pen=pn)
        out += _fdot(M, xx, MOE_Y + 22.0, 2.2, pen=pn)

    # the vertical dotted column that ties Z's envelope to the whole stack
    out += _dash(M, [(BACK_COL, MOE_Y + 66.0), (BACK_COL, BACK_ROWS[-1] + 10.0)],
                 dash=0.5, gap=1.7, pen=_pen(GREEN, colors))

    # right-hand purple gradients
    pu = _pen(PURPLE, colors)
    labels = [("Y", 1191.0), ("experts", 1265.0), ("router", 1321.0)]
    for name, y in labels:
        h = 14.0 if len(name) < 4 else 11.5
        out += _frac(M, "@L", "@" + name, 1052.0, y, h, pen=pu, tracking=1.0)
        out += _arrow(M, 1006.0, y, 1, 8.5, pen=pu)
    # routing skeleton
    out += _dash(M, _bez((940.0, 1120.0), (985.0, 1150.0), (958.0, 1178.0), (994.0, 1191.0)),
                 dash=0.45, gap=1.8, pen=pu)
    out += _dash(M, [(718.0, 1175.0), (718.0, 1321.0)], dash=0.5, gap=1.7, pen=pu)
    out += _dash(M, [(796.0, 1175.0), (796.0, 1265.0)], dash=0.5, gap=1.7, pen=pu)
    out += _dash(M, [(796.0, 1265.0), (977.0, 1265.0)], dash=0.5, gap=1.7, pen=pu)
    out += _dash(M, [(718.0, 1321.0), (977.0, 1321.0)], dash=0.5, gap=1.7, pen=pu)
    out += _dash(M, [(977.0, 1265.0), (977.0, 1321.0)], dash=0.5, gap=1.7, pen=pu)
    out += _dash(M, [(977.0, 1265.0), (994.0, 1265.0)], dash=0.5, gap=1.7, pen=pu)
    out += _dash(M, [(977.0, 1321.0), (994.0, 1321.0)], dash=0.5, gap=1.7, pen=pu)
    for nx, ny in ((718.0, 1238.0), (796.0, 1238.0), (718.0, 1291.0), (718.0, 1321.0),
                   (977.0, 1265.0), (977.0, 1321.0)):
        out += _ocirc(M, nx, ny, 4.2, pen=pu, n=28)
    return out


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------


def attention_as_resonance(rng: SeededRNG, bounds: Bounds, colors: int = 6) -> List[GCodeCommand]:
    M = _Map(bounds)
    out: List[GCodeCommand] = []
    out += _title(M, colors)
    out += _qk_block(M, colors, +1, _pen(RED, colors))
    out += _qk_block(M, colors, -1, _pen(BLUE, colors))
    out += _centre_fraction(M, colors)
    out += _interference(M, rng, colors)
    out += _softmax(M, colors)
    out += _v_block(M, colors)
    out += _moe_row(M, colors)
    out += _backward(M, colors)
    return out
