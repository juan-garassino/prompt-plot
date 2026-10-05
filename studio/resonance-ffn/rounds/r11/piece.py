"""ATTENTION AS RESONANCE (FFN) — exact recreation of ``studio/resonance-ffn/ref/reference.png``.

REPRODUCTION, not design.  Every element, its position and its marker vocabulary
are traced off the reference (1122 x 1402 px), mapped into the drawable area and
drawn with pen-plottable geometry.

Relationship to the sibling plate
---------------------------------
``studio/resonance/rounds/r01/piece.py`` is the SAME plate with an MoE band where
this one has an FFN band.  Its coordinate map, its wave-packet primitive and its
``_interference`` figure are APPROVED and are reused here wholesale — the maths
below is quoted from it because it is the same maths, not a re-derivation.

What is new in this plate: the FFN band (three purple stages between pinch
nodes), the second, smaller interference figure under ``@L/@A``, and the single
bottom backward ROW that carries the transposed stages in reverse order.

Two coordinate systems
----------------------
* REFERENCE PIXELS — everything is laid out in the reference image's own pixel
  space, origin top-left.  ``_Map.p`` maps a reference pixel to sheet mm (x
  stretched to the drawable width, y to its height).
* MILLIMETRES — letterforms, circles, discs and arrowheads are built in mm at a
  UNIFORM scale (``_Map.s``) so glyphs and rings never shear when the reference
  aspect (0.800) is fitted to A4 portrait's drawable (0.686).

The maths
---------
WAVE PACKET (the plate's core primitive — Q, K, V, Z, the three FFN stages, Y
and every backward row):

    f(x)   = SUM_i A_i * exp(-((x - c_i)/s_i)^2) * cos(2*pi*(x - c_i)/L_i + p_i)
    env(x) = SUM_i A_i * exp(-((x - c_i)/s_i)^2)

carrier x Gaussian envelope; ``env`` is outlined above and below the axis.  Rows
carry 2-3 superposed packets, which is what produces the small ripple where two
Gaussian tails overlap.

INTERFERENCE FIGURE (the hero, and its small sibling under @L/@A) — a real
two-source field, not faked.  The instantaneous superposition of two point
sources is

    A(x, y) = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2),      k = 2*pi/L

and what the reference draws are its RIDGE lines — the wave crests, cos(k r_s)
= 1, i.e. the Huygens loci r_s = m L.  (A level set of A is the wrong object: it
draws every fringe twice and closes into a lattice of blobs.)  Each family is a
set of concentric circles about its own source; the two families cross on the
hyperbolae r1 - r2 = const.  The separation is a whole number of wavelengths
(d = 35 L for the hero, d = 14 L for the small one) so crest m of one family
meets crest n-m of the other exactly ON the axis rather than beating against it.

A parallel-crowding guard (``_Guard``) drops a crest point only where another
stroke runs within 0.82 mm of it AND within 25 degrees of parallel, so genuine
crossings survive and only unplottable tangency crowding is removed.

THE FFN FAN (new here).  The middle stage is not a packet — it is a bundle of
streamlines pinched to a point at both nodes:

    forward  (nonlinearity):  g(u) = tanh(c sin(pi u)^p) / tanh(c)     -- saturating,
                                                                         flat-topped
    backward (nonlinearity'): g(u) = sin(pi u)^p * (1 - d exp(-((u-1/2)/w)^2))

i.e. the derivative of the forward shape: a notch at the centre splits the single
plateau into the twin peaks the reference draws.  That is the whole difference in
character between the two bands and it is why the middle stage reads differently
from its neighbours.

Pens (6): 0 red · 1 blue · 2 ochre · 3 green · 4 purple · 5 black.

Entry point: ``attention_as_resonance_ffn``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import (  # noqa: F401
    _GLYPHS,
    _dot,
    _glyph_advance,
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


# Juan, 2026-09-28, on the resonance family: "the original was much more beautiful — we just
# needed the dot lines to be more continuous, not to remove the waves". The only change in
# this round: a dot-sized mark (dash <= DOT_MAX) becomes one round dot, laid at an even
# arclength pitch with a dot on both ends. Longer dashes and everything else are unchanged.
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
    out = []
    si = 0
    for k in range(n + 1):
        target = total * k / n
        while si < len(segs) - 1 and segs[si][2] + segs[si][3] < target:
            si += 1
        a, b, s0, L = segs[si]
        t = min(1.0, max(0.0, (target - s0) / L))
        out += _dot(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, DOT_R, color=pen)
    return out


def _dash_mm(pts, dash: float, gap: float, pen=None, f: int = 2000, step: float = 0.20):
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


def _fdot_mm(cx: float, cy: float, r: float, pen=None):
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
        out += _poly(
            [(cx - direction * L * frac, cy + yy), (cx - direction * L, cy + yy)],
            color=pen,
            f=1600,
        )
    return out


# ---------------------------------------------------------------------------
# type — the SHARED single-stroke font (now 78 glyphs incl. lowercase), used
# with per-glyph proportional advances.  Only two glyphs are built locally:
# the partial-derivative and the radical, which the shared font does not carry.
# ---------------------------------------------------------------------------

# The partial derivative is a SHARED glyph now (U+2202) and is used as the
# character.  The radical is deliberately NOT a glyph: its overbar has to
# stretch to whatever it covers, so ``_radical`` composes it (tick + rule +
# radicand) instead.  Nothing else on this plate needs a local letterform.
_EXTRA: Dict[str, List[List[Tuple[float, float]]]] = {}

PARTIAL = "\u2202"


def _units(ch: str) -> float:
    """Natural advance for one glyph, in the font's 4x6 cell units."""
    return _glyph_advance(ch)


def _strokes(ch: str):
    st = _GLYPHS.get(ch)
    if st is None:
        st = _GLYPHS.get(ch.upper(), [])
    return st


def _tw(text: str, h_mm: float, tracking: float = 1.0) -> float:
    return sum(_units(c) for c in text) * (h_mm / 6.0) * tracking


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
    the glyphs themselves are built in mm at uniform scale so they never shear.
    Advances are PROPORTIONAL (per-glyph), which is what lets lowercase words
    like ``softmax`` / ``nonlinearity`` set at a believable colour."""
    ax, ay = M.p(px, py)
    h = M.s(h_px)
    sc = h / 6.0
    if center:
        ax -= _tw(text, h, tracking) / 2.0
    out: List[GCodeCommand] = []
    cx = ax
    for ch in text:
        if ch == "~":  # the centred multiplication dot
            out += _fdot_mm(cx + 1.8 * sc, ay + 2.6 * sc, max(0.55 * sc, 0.32), pen)
        else:
            offs = [(0.0, 0.0)]
            if weight > 0:
                offs = [(0.0, 0.0), (weight, 0.0), (weight * 0.5, weight * 0.9)]
            for ox, oy in offs:
                for st in _strokes(ch):
                    out += _poly(
                        [(cx + gx * sc + ox, ay + gy * sc + oy) for gx, gy in st],
                        color=pen,
                        f=f,
                    )
        cx += _units(ch) * sc * tracking
    return out


def _type_sup(
    M: _Map,
    word: str,
    sup: str,
    cx_px: float,
    py: float,
    h_px: float,
    pen=None,
    tracking: float = 1.0,
    sup_scale: float = 0.62,
    sup_rise: float = 0.52,
):
    """word + a raised, smaller mark (the transpose T, the derivative prime).

    The superscript is LAYOUT, not a glyph: the same font, smaller and lifted."""
    h = M.s(h_px)
    w_word = _tw(word, h, tracking)
    w_sup = _tw(sup, h * sup_scale, tracking)
    total_px = (w_word + w_sup + M.s(1.2)) / M.sx
    left = cx_px - total_px / 2.0
    out = _type(M, word, left, py, h_px, pen=pen, tracking=tracking)
    sx = left + (w_word + M.s(1.2)) / M.sx
    out += _type(
        M, sup, sx, py - h_px * sup_rise, h_px * sup_scale, pen=pen, tracking=tracking
    )
    return out


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
    out += _type(
        M, num, px, py - h_px * 0.42 - gap_px, h_px, pen=pen, tracking=tracking, center=True
    )
    out += _type(
        M, den, px, py + h_px * 1.02 + gap_px, h_px, pen=pen, tracking=tracking, center=True
    )
    return out


# ---------------------------------------------------------------------------
# the wave packet — the plate's core primitive (APPROVED, from the sibling)
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
    env_lift: float = 3.2,
):
    """Carrier x Gaussian envelope on an axis line, with the envelope itself
    outlined above and below."""
    lam_min = min(p[2] for p in packets)
    step = max(lam_min / 11.0, 0.22)
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
            env = [(x, y + sgn * _pk_env(x, packets)) for x in xs]
            env = [(x, yy) for x, yy in env if abs(yy - y) > env_lift]
            if len(env) > 3:
                out += _dash_mm([M.p(a, b) for a, b in env], 0.85, 1.55, pen=pen)
    return out


# ---------------------------------------------------------------------------
# layout constants, traced off the reference (reference pixels)
# ---------------------------------------------------------------------------

TITLE_Y = 48.0
RULE_Y = 75.0

QK_ROWS = [164.0, 221.0, 282.0, 339.0, 396.0]
Q_HOME = 108.0
K_HOME = REF_W - Q_HOME

Q_ROWS = [
    (312.0, 287.0, False, 312.0),
    (356.0, 287.0, False, 356.0),
    (389.0, 389.0, False, None),
    (357.0, None, False, 357.0),
    (325.0, 325.0, False, None),
]
Q_HOME_FILLED = [False, True, False, True, False]

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

Q_VERTS = [
    (108.0, 128.0, 412.0),
    (207.0, 100.0, 300.0),
    (287.0, 108.0, 352.0),
    (315.0, 162.0, 420.0),
    (356.0, 212.0, 402.0),
    (389.0, 262.0, 432.0),
]

# --- the hero interference figure -----------------------------------------
IF_CX, IF_CY = 561.0, 611.0
IF_D = 250.0
SRC_L, SRC_R = IF_CX - IF_D / 2, IF_CX + IF_D / 2

# --- softmax band ----------------------------------------------------------
SOFT_BASE = 864.0
SOFT_PEAKS = [
    (391.0, 38.0, "o"),
    (475.0, 67.0, "f"),
    (516.0, 21.0, None),
    (559.0, 51.0, "f"),
    (645.0, 67.0, "o"),
    (726.0, 34.0, "o"),
]
SOFT_GHOSTS = [(433.0, 22.0), (601.0, 26.0), (686.0, 22.0)]

# --- V block (FIVE ochre rows, mid-right) ----------------------------------
V_ROWS = [919.0, 944.0, 971.0, 999.0, 1027.0]
V_L = 725.0
V_R = [976.0, 991.0, 991.0, 991.0, 991.0]

# --- the forward row: Z = AV | FFN | Y --------------------------------------
FWD_Y = 1129.0
Z_START = 245.0
FFN_N0 = 722.0      # the green->purple junction
FFN_N1 = 825.0      # expand | nonlinearity
FFN_N2 = 900.0      # nonlinearity | project
FFN_N3 = 1000.0     # project | Y
Y_END = 1032.0

# --- the backward ROW (one line) + the left stack ---------------------------
BACK_Y = 1272.0
BACK_ROWS = [
    # y, pen-slot, x_left, x_right, arrow+label, open-left
    (1206.0, RED, 112.0, 232.0, "Q", True),
    (1238.0, RED, 143.0, 276.0, None, True),
    (1272.0, BLUE, 112.0, 276.0, "K", True),
    (1301.0, BLUE, 143.0, 276.0, None, True),
    (1334.0, OCHRE, 112.0, 276.0, "V", True),
]
BACK_PACKETS: List[List[Packet]] = [
    [(180.0, 20.0, 10.5, 23.0, 0.0), (148.0, 9.0, 7.0, 7.0, 0.4), (214.0, 9.0, 7.0, 6.0, 0.9)],
    [(218.0, 19.0, 10.0, 20.0, 0.0), (185.0, 9.0, 7.0, 7.0, 0.3), (254.0, 8.0, 6.5, 5.0, 0.8)],
    [(190.0, 21.0, 10.5, 29.0, 0.0), (150.0, 9.0, 7.0, 7.0, 0.5), (228.0, 9.0, 7.0, 8.0, 0.2)],
    [(228.0, 21.0, 10.5, 27.0, 0.0), (188.0, 9.0, 7.0, 7.0, 0.6), (262.0, 8.0, 6.5, 5.0, 0.1)],
    [(186.0, 20.0, 10.0, 31.0, 0.0), (150.0, 9.0, 7.0, 8.0, 0.3), (222.0, 9.0, 7.0, 7.0, 0.7)],
]

# --- the small interference figure under @L/@A ------------------------------
IF2_CX, IF2_CY = 465.5, BACK_Y
IF2_D = 97.0
SRC2_L, SRC2_R = IF2_CX - IF2_D / 2, IF2_CX + IF2_D / 2


# ---------------------------------------------------------------------------
# sections — upper half (reused verbatim from the approved sibling)
# ---------------------------------------------------------------------------


def _title(M: _Map, colors: int):
    bk = _pen(BLACK, colors)
    out = _type(
        M, "ATTENTION AS RESONANCE", 545.0, TITLE_Y, 16.0, pen=bk,
        tracking=1.645, center=True, weight=0.22,
    )
    ax, ay = M.p(490.0, RULE_Y)
    bx, _ = M.p(615.0, RULE_Y)
    out += _poly([(ax, ay), (bx, ay)], color=bk, f=2000)
    out += _fdot(M, 552.0, RULE_Y, 2.4, pen=bk)
    return out


def _qk_block(M: _Map, colors: int, side: int, pen):
    """side = +1 Q (left block, continuations leftward), -1 K (right, mirrored).

    Q and K are NOT a literal mirror of one another; each block carries its own
    traced row geometry and its own packet parameters."""

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

    if side > 0:
        out += _type(M, "Q", 97.0, 126.0, 30.0, pen=pen, tracking=0.90, weight=0.44)
    else:
        out += _type(M, "K", 1002.0, 124.0, 28.0, pen=pen, tracking=0.92, weight=0.44)

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
    nx = 561.0 - 4.0
    out += _type(M, num, nx, 392.0, h, pen=bk, tracking=tr, center=True, weight=0.2)
    out += _type(M, "T", nx + wn_px / 2.0 + 1.5, 381.0, 12.5, pen=bk, weight=0.16)

    ax, ay = M.p(507.0, 404.0)
    bx, _ = M.p(616.0, 404.0)
    out += _poly([(ax, ay), (bx, ay)], color=bk, f=2000)

    out += _radical(M, "d", 528.0, 434.0, 21.0, pen=bk, weight=0.16, tail_px=11.0)
    out += _type(M, "k", 564.0, 437.0, 12.0, pen=bk, weight=0.14)
    return out


def _radical(
    M: _Map,
    radicand: str,
    px: float,
    py: float,
    h_px: float,
    pen=None,
    weight: float = 0.0,
    tail_px: float = 0.0,
):
    """The radical sign, COMPOSED rather than drawn from a glyph.

    A fixed glyph cannot work: the overbar has to reach the end of whatever it
    covers, and here that is ``d`` plus its subscript.  (px, py) is the left
    baseline of the tick."""
    ax, ay = M.p(px, py)
    sc = M.s(h_px) / 6.0
    w = _tw(radicand, M.s(h_px), 1.0) + M.s(tail_px)
    tick = [(0.0, 3.2), (0.7, 2.7), (1.6, 0.0), (2.8, 6.0)]
    out: List[GCodeCommand] = []
    offs = [(0.0, 0.0)]
    if weight > 0:
        offs = [(0.0, 0.0), (weight, 0.0), (weight * 0.5, weight * 0.9)]
    for ox, oy in offs:
        out += _poly([(ax + gx * sc + ox, ay + gy * sc + oy) for gx, gy in tick],
                     color=pen, f=2200)
        out += _poly([(ax + 2.8 * sc + ox, ay + 6.0 * sc + oy),
                      (ax + 3.4 * sc + w + ox, ay + 6.0 * sc + oy)], color=pen, f=2200)
    out += _type(M, radicand, px + 3.9 * sc / M.sx, py, h_px, pen=pen, weight=weight)
    return out


class _Guard:
    """Parallel-crowding guard, in MILLIMETRES.

    Two crest families inevitably run TANGENT to one another along the axis of a
    two-source diagram, which is the one place a pen cannot resolve them.  A
    plain occupancy grid also deletes the CROSSINGS, which are the whole point,
    so this one rejects a point only when a nearby point of another stroke is
    within ``sep`` AND its tangent is within 25 degrees of parallel."""

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
            (x, y, ux, uy, sid)
        )


def _crest_field(
    M: _Map,
    cx: float,
    cy: float,
    d: float,
    n_lam: int,
    m_solid: int,
    m_max: int,
    a_out: float,
    b_out: float,
    b_solid: float,
    pen,
):
    """The APPROVED Huygens crest construction, parameterised so the hero figure
    and its small @L/@A sibling are literally the same object at two scales."""
    lam = d / n_lam
    sl, sr = cx - d / 2, cx + d / 2
    guard = _Guard(0.82)
    out: List[GCodeCommand] = []
    sid = 0

    def ring(sx: float, r: float):
        n = max(60, int(r * 2.1))
        return [
            (sx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n))
            for t in range(n + 1)
        ]

    def emit_clipped(pts, dotted: bool = False, keep_out=None):
        nonlocal sid
        sid += 1
        aa, bb = (a_out, b_out) if dotted else (a_out * 0.80, b_solid)
        res: List[GCodeCommand] = []
        run = []
        for j, (px, py) in enumerate(pts):
            ok = ((px - cx) / aa) ** 2 + ((py - cy) / bb) ** 2 <= 1.0
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
                    res += (_dash(M, run, dash=0.42, gap=1.8, pen=pen) if dotted
                            else _line(M, run, pen=pen, f=2600))
                run = []
        if len(run) >= 4:
            res += (_dash(M, run, dash=0.42, gap=1.8, pen=pen) if dotted
                    else _line(M, run, pen=pen, f=2600))
        return res

    for sx in (sl, sr):
        other = sr if sx == sl else sl
        for m in range(1, m_solid + 1):
            out += emit_clipped(ring(sx, m * lam))
        for m in range(m_solid + 1, m_max):
            out += emit_clipped(
                ring(sx, m * lam), dotted=True,
                keep_out=(other, cy, m_solid * lam + d * 0.024),
            )
    return out


def _interference(M: _Map, rng: SeededRNG, colors: int):
    """The hero, computed as a real two-source field (APPROVED — see module docstring)."""
    bk = _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    n_lam = 35
    lam = IF_D / n_lam
    out += _crest_field(M, IF_CX, IF_CY, IF_D, n_lam, 21, 52, 272.0, 158.0, 126.0, bk)

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
        bot = 812.0 if j % 2 == 0 else 788.0
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

    for cx, h in SOFT_GHOSTS:
        gp = [
            (cx - 26.0 + t * 0.9,
             SOFT_BASE - h / (1.0 + ((cx - 26.0 + t * 0.9 - cx) / 8.0) ** 2) ** 1.6)
            for t in range(59)
        ]
        out += _dash(M, gp, dash=0.42, gap=1.5, pen=bk)

    for cx, h, m in SOFT_PEAKS:
        out += _line(M, [(cx, SOFT_BASE), (cx, SOFT_BASE - h + 2.0)], pen=bk)
        if m == "o":
            out += _ocirc(M, cx, SOFT_BASE - h - 3.0, 5.0, pen=bk)
        elif m == "f":
            out += _fdot(M, cx, SOFT_BASE - h - 3.0, 4.4, pen=bk)

    for x, kind in [
        (322.0, "f"), (391.0, "f"), (434.0, "o"), (475.0, "o"), (516.0, "f"),
        (559.0, "o"), (605.0, "o"), (645.0, "o"), (685.0, "o"), (726.0, "f"), (798.0, "f"),
    ]:
        if kind == "o":
            out += _ocirc(M, x, SOFT_BASE, 4.4, pen=bk)
        else:
            out += _fdot(M, x, SOFT_BASE, 3.2, pen=bk)

    out += _lead_dots(M, 311.0, -11.0, 4, SOFT_BASE, 2.3, pen=bk)
    out += _lead_dots(M, 813.0, 13.5, 4, SOFT_BASE, 2.3, pen=bk)

    out += _type(M, "softmax", 562.0, 782.0, 16.0, pen=bk, tracking=1.173, center=True,
                 weight=0.14)
    return out


def _v_block(M: _Map, colors: int):
    """V — FIVE ochre rows at mid-right, fed from the softmax band and feeding Z."""
    oc = _pen(OCHRE, colors)
    out: List[GCodeCommand] = []
    packs: List[List[Packet]] = [
        [(898.0, 30.0, 12.0, 36.0, 0.0), (800.0, 16.0, 9.0, 11.0, 0.5),
         (950.0, 12.0, 8.0, 9.0, 0.9)],
        [(880.0, 30.0, 11.5, 34.0, 0.0), (790.0, 14.0, 8.5, 12.0, 0.8),
         (945.0, 11.0, 7.5, 8.0, 0.2)],
        [(900.0, 26.0, 15.0, 28.0, 0.0), (812.0, 14.0, 9.5, 10.0, 0.3),
         (960.0, 10.0, 8.0, 7.0, 0.6)],
        [(862.0, 28.0, 11.0, 32.0, 0.0), (940.0, 12.0, 8.0, 9.0, 0.4),
         (792.0, 12.0, 8.0, 8.0, 0.1)],
        [(890.0, 28.0, 11.5, 34.0, 0.0), (960.0, 13.0, 8.0, 10.0, 0.7),
         (802.0, 11.0, 7.5, 7.0, 0.3)],
    ]
    for i, y in enumerate(V_ROWS):
        xr = V_R[i]
        out += _line(M, [(V_L, y), (xr, y)], pen=oc)
        out += wave_packet(M, V_L + 2.0, xr - 2.0, y, packs[i], pen=oc)
        out += _ocirc(M, V_L, y, 4.8, pen=oc)
        if i == 2:
            out += _fdot(M, V_L, y, 2.2, pen=oc)
        if i == 3:
            out += _fdot(M, xr, y, 4.4, pen=oc)
        else:
            out += _ocirc(M, xr, y, 4.8, pen=oc)
        out += _lead_dots(M, 1036.0, 10.5, 4, y, 2.2, pen=oc)
        if i in (0, 2):
            out += _fdot(M, 703.0, y, 2.4, pen=oc)
        if i == 1:
            out += _fdot(M, 691.0, y, 3.4, pen=oc)

    # the two ochre dotted columns that tie the five rows together
    out += _dash(M, [(V_L, V_ROWS[0] - 20.0), (V_L, V_ROWS[-1] + 26.0)],
                 dash=0.5, gap=1.7, pen=oc)
    out += _dash(M, [(991.0, V_ROWS[0] + 6.0), (991.0, V_ROWS[-1] + 30.0)],
                 dash=0.5, gap=1.7, pen=oc)

    out += _type(M, "V", 1021.0, 897.0, 24.0, pen=oc, tracking=0.99, weight=0.38)

    # --- softmax -> V : long ochre feeds swinging in from the left ---------
    for i, sx in enumerate([391.0, 434.0, 475.0, 516.0, 559.0, 601.0]):
        ty = V_ROWS[min(i, 4)]
        pts = _bez((sx, SOFT_BASE + 8.0), (sx + 10.0, SOFT_BASE + 60.0),
                   (V_L - 150.0 + 6.0 * i, ty), (V_L - 22.0, ty))
        out += _dash(M, pts, dash=0.45, gap=1.9, pen=oc)

    # --- V -> Z : the ochre bundle sweeping down-left under the V block ----
    for i, y in enumerate(V_ROWS):
        pts = _bez((V_L - 4.0, y + 6.0), (V_L - 96.0, y + 34.0),
                   (700.0 - 10.0 * i, 1036.0 + 8.0 * i), (652.0 - 18.0 * i, 1100.0 + 5.0 * i))
        out += _dash(M, pts, dash=0.45, gap=2.0, pen=oc)
    return out


# ---------------------------------------------------------------------------
# the FFN fan — the middle stage of each band
# ---------------------------------------------------------------------------


def _ffn_fan(
    M: _Map,
    xa: float,
    xb: float,
    y: float,
    amp: float,
    pen,
    derivative: bool = False,
    n: int = 5,
):
    """A bundle of streamlines pinched to a point at both nodes.

        offset_k(u) = a_k * sin(pi u)^p_k              -- the family
                      - D * exp(-((u - 1/2)/w)^2)      -- the notch (backward only)

    Forward the family is mildly saturated (``tanh``), so each streamline has
    the flat top of a squashing nonlinearity.  Backward the SAME family carries
    a notch at the centre: that is the derivative, and it is what turns one
    plateau into the twin peaks the reference draws.

    The notch is an ABSOLUTE dip, the same for every streamline — a dip
    proportional to ``a_k`` pulls the outer lines down past the inner ones,
    which both crosses the family and closes the bundle below one pen width.
    """
    span = xb - xa
    out: List[GCodeCommand] = []
    steps = 170
    LIFT = 0.44 / M.sx          # 0.44 mm, in reference px
    dip = 0.26 * amp if derivative else 0.0

    def family(u: float, p: float) -> float:
        s = math.sin(math.pi * min(max(u, 0.0), 1.0))
        if s <= 0.0:
            return 0.0
        v = s ** p
        if derivative:
            return v
        c = 1.75                       # a MILD saturation: a rounded flat top
        return math.tanh(c * v) / math.tanh(c)

    def notch(u: float) -> float:
        return dip * math.exp(-((u - 0.5) / 0.078) ** 2)

    for k in range(1, n + 1):
        frac = k / n
        a = amp * frac ** 0.72
        p = 2.55 - 0.16 * k + (0.85 if derivative else 0.0)
        skew = 0.035 * (1.0 - frac)
        for sgn in (1.0, -1.0):
            run: List[Tuple[float, float]] = []
            for t in range(steps + 1):
                u = t / steps
                uu = min(max(u + skew * math.sin(2 * math.pi * u), 0.0), 1.0)
                off = a * family(uu, p) - notch(u)
                # Every streamline converges on the node, so near it the whole
                # bundle (and the spine) would be redrawn inside one pen width.
                # Lift off at LIFT and let the node disc close the figure.
                if off < LIFT:
                    if len(run) > 3:
                        out += _line(M, run, pen=pen, f=2500)
                    run = []
                    continue
                run.append((xa + u * span, y + sgn * off))
            if len(run) > 3:
                out += _line(M, run, pen=pen, f=2500)

    # the faint dotted arc just outside the bundle
    for sgn in (1.0, -1.0):
        pts = [
            (xa + (t / 120) * span,
             y + sgn * (amp * 1.28 * family(t / 120, 2.15) - notch(t / 120) * 0.6))
            for t in range(121)
        ]
        out += _dash(M, pts, dash=0.45, gap=1.9, pen=pen)

    return out


# ---------------------------------------------------------------------------
# the forward row: Z = AV | FFN | Y
# ---------------------------------------------------------------------------


def _forward_row(M: _Map, colors: int):
    gr = _pen(GREEN, colors)
    pu = _pen(PURPLE, colors)
    bk = _pen(BLACK, colors)
    oc = _pen(OCHRE, colors)
    out: List[GCodeCommand] = []
    y = FWD_Y

    # ---- Z = AV ---------------------------------------------------------
    zp: List[Packet] = [
        (508.0, 46.0, 13.5, 72.0, 0.0),
        (400.0, 13.0, 8.5, 15.0, 0.4),
        (612.0, 13.0, 8.5, 14.0, 0.9),
        (455.0, 9.0, 7.5, 8.0, 0.2),
        (352.0, 11.0, 8.0, 6.0, 0.1),
    ]
    out += _line(M, [(Z_START, y), (FFN_N0, y)], pen=gr)
    out += wave_packet(M, Z_START + 2.0, FFN_N0 - 4.0, y, zp, pen=gr)
    out += _fdot(M, Z_START, y, 4.2, pen=gr)
    out += _lead_dots(M, Z_START - 21.0, -10.5, 5, y, 2.3, pen=gr)
    for x in (322.0, 508.0, 686.0):
        out += _ocirc(M, x, y, 4.6, pen=gr)
    for x in (387.0, 620.0):
        out += _ocirc(M, x, y, 6.4, pen=gr)
        out += _ocirc(M, x, y, 3.2, pen=gr, n=26)
    out += _ocirc(M, 634.0, y, 3.0, pen=gr, n=24)
    out += _fdot(M, 508.0, y - 76.0, 4.4, pen=gr)
    out += _fdot(M, 508.0, y + 76.0, 4.4, pen=gr)
    out += _dash(M, [(508.0, y - 70.0), (508.0, y + 70.0)], dash=0.5, gap=1.8, pen=gr)
    out += _type(M, "Z = AV", 362.0, 1068.0, 22.0, pen=gr, tracking=1.203, weight=0.38)

    # ---- the FFN bracket -------------------------------------------------
    out += _line(M, [(723.0, 1098.0), (733.0, 1077.0), (846.0, 1077.0)], pen=bk)
    out += _fdot(M, 850.0, 1077.0, 2.2, pen=bk)
    out += _type(M, "FFN", 876.0, 1075.0, 14.0, pen=bk, tracking=0.85, center=True,
                 weight=0.16)
    out += _fdot(M, 899.0, 1077.0, 2.2, pen=bk)
    out += _line(M, [(905.0, 1077.0), (972.0, 1077.0), (983.0, 1098.0)], pen=bk)

    # ---- the purple spine ------------------------------------------------
    out += _line(M, [(FFN_N0, y), (Y_END, y)], pen=pu)
    out += _fdot(M, FFN_N0, y, 4.6, pen=gr)          # the green->purple junction
    for nx in (FFN_N1, FFN_N2, FFN_N3):
        out += _fdot(M, nx, y, 4.4, pen=pu)
    out += _ocirc(M, Y_END, y, 5.4, pen=pu)
    out += _lead_dots(M, 1052.0, 15.0, 4, y, 2.4, pen=pu)

    # ---- the three stages ------------------------------------------------
    expand: List[Packet] = [
        (772.0, 20.0, 11.0, 42.0, 0.0),
        (745.0, 11.0, 7.5, 14.0, 0.5),
        (803.0, 8.0, 6.5, 9.0, 0.9),
    ]
    project: List[Packet] = [
        (976.0, 17.0, 10.0, 40.0, 0.0),
        (947.0, 12.0, 7.5, 12.0, 0.4),
        (1004.0, 7.0, 6.0, 7.0, 0.8),
    ]
    out += wave_packet(M, FFN_N0 + 5.0, FFN_N1 - 4.0, y, expand, pen=pu)
    out += _ffn_fan(M, FFN_N1, FFN_N2, y, 44.0, pu, derivative=False)
    out += wave_packet(M, FFN_N2 + 4.0, FFN_N3 - 3.0, y, project, pen=pu)

    # ---- the stage names -------------------------------------------------
    for name, cx, tr in (("expand", 764.5, 0.89), ("nonlinearity", 873.0, 0.97),
                         ("project", 968.0, 0.85)):
        out += _type(M, name, cx, 1187.0, 12.0, pen=bk, tracking=tr, center=True)

    # ---- the dotted columns that tie the stages to their names -----------
    for nx in (FFN_N1, FFN_N2):
        out += _dash(M, [(nx, 1086.0), (nx, 1172.0)], dash=0.6, gap=2.2, pen=bk)
    out += _dash(M, [(FFN_N3, 1092.0), (FFN_N3, 1162.0)], dash=0.55, gap=2.0, pen=pu)

    # ---- Y ---------------------------------------------------------------
    out += _type(M, "Y", 1052.0, 1107.0, 23.0, pen=pu, tracking=0.86, weight=0.40)

    # ---- V -> the FFN entry ---------------------------------------------
    out += _dash(M, _bez((996.0, V_ROWS[0]), (1075.0, 960.0), (1055.0, 1030.0),
                         (1010.0, 1062.0)), dash=0.45, gap=1.9, pen=oc)
    return out


# ---------------------------------------------------------------------------
# the backward row — ONE line along the bottom
# ---------------------------------------------------------------------------


def _small_interference(M: _Map, rng: SeededRNG, colors: int):
    """@L/@A — the hero figure again, at 0.39 scale, same construction."""
    bk = _pen(BLACK, colors)
    out: List[GCodeCommand] = []
    # the hero's proportions exactly: m_solid/n_lam = 0.60, a/d = 1.09,
    # b/d = 0.63, b_solid/d = 0.50 -- the same object at 0.39 scale.
    n_lam = 14
    lam = IF2_D / n_lam
    out += _crest_field(M, IF2_CX, IF2_CY, IF2_D, n_lam, 8, 21,
                        105.5, 61.0, 48.5, bk)

    for sx in (SRC2_L, SRC2_R):
        for a in (62.0, 78.0):
            b = a * 0.60
            rr = [
                (sx + a * math.cos(2 * math.pi * t / 200),
                 IF2_CY + b * math.sin(2 * math.pi * t / 200))
                for t in range(201)
            ]
            rr = [q for q in rr
                  if min(math.hypot(q[0] - SRC2_L, q[1] - IF2_CY),
                         math.hypot(q[0] - SRC2_R, q[1] - IF2_CY)) > 8 * lam + 3.0]
            if len(rr) > 6:
                out += _dash(M, rr, dash=0.42, gap=1.9, pen=bk)

    k = 2 * math.pi / lam

    def field(px, py):
        d1 = math.hypot(px - SRC2_L, py - IF2_CY) + 3.0
        d2 = math.hypot(px - SRC2_R, py - IF2_CY) + 3.0
        return math.cos(k * d1) / math.sqrt(d1) + math.cos(k * d2) / math.sqrt(d2)

    placed: List[Tuple[float, float, float]] = []

    def place(px, py, r):
        if r < 0.7:
            return []
        for qx, qy, qr in placed:
            if math.hypot(px - qx, py - qy) < (r + qr) * 1.3 + 2.5:
                return []
        placed.append((px, py, r))
        return _fdot(M, px, py, r, pen=bk)

    for _ in range(46):
        px = IF2_CX + rng.uniform(-88.0, 88.0)
        py = IF2_CY + rng.uniform(-52.0, 52.0)
        if ((px - IF2_CX) / 92.0) ** 2 + ((py - IF2_CY) / 54.0) ** 2 > 1.0:
            continue
        out += place(px, py, 0.7 + 8.0 * abs(field(px, py)))

    # the three dotted droplines through the figure
    for x, yt, yb in ((417.0, 1231.0, 1325.0), (458.0, 1218.0, 1305.0),
                      (514.0, 1207.0, 1338.0)):
        out += _dash(M, [(x, yt), (x, yb)], dash=0.6, gap=2.1, pen=bk)

    out += _frac(M, "\u2202L", "\u2202A", 462.0, 1352.0, 13.0, pen=bk, tracking=1.02)
    return out


def _backward(M: _Map, rng: SeededRNG, colors: int):
    out: List[GCodeCommand] = []
    pens = {RED: _pen(RED, colors), BLUE: _pen(BLUE, colors), OCHRE: _pen(OCHRE, colors)}
    bk = _pen(BLACK, colors)
    gr = _pen(GREEN, colors)
    pu = _pen(PURPLE, colors)

    # ---- the left stack: @L/@Q @L/@K @L/@V, five rows --------------------
    for i, (y, slot, xl, xr, label, _open) in enumerate(BACK_ROWS):
        pn = pens[slot]
        out += _line(M, [(xl, y), (xr, y)], pen=pn)
        out += wave_packet(M, xl + 3.0, xr - 3.0, y, BACK_PACKETS[i], pen=pn,
                           env_lift=2.4)
        out += _ocirc(M, xl, y, 4.7, pen=pn)
        out += _ocirc(M, xr, y, 4.7, pen=pn)
        if label is not None:
            out += _frac(M, "\u2202L", PARTIAL + label, 47.0, y, 14.0, pen=pn, tracking=1.02)
            out += _arrow(M, 75.0, y, -1, 9.0, pen=pn)
            out += _dash(M, [(88.0, y), (xl - 7.0, y)], dash=0.5, gap=1.0, pen=pn)
        else:
            out += _fdot(M, 112.0, y, 2.2, pen=pn)
            out += _dash(M, [(120.0, y), (xl - 7.0, y)], dash=0.5, gap=1.0, pen=pn)

    # the dotted columns down the stack
    for x, yt, yb, slot in ((112.0, 1206.0, 1240.0, RED), (112.0, 1272.0, 1303.0, BLUE),
                            (112.0, 1334.0, 1366.0, OCHRE),
                            (143.0, 1178.0, 1238.0, RED), (143.0, 1250.0, 1301.0, BLUE),
                            (232.0, 1178.0, 1206.0, RED), (232.0, 1206.0, 1248.0, RED),
                            (276.0, 1206.0, 1240.0, RED), (276.0, 1272.0, 1303.0, BLUE),
                            (276.0, 1334.0, 1368.0, OCHRE)):
        out += _dash(M, [(x, yt), (x, yb)], dash=0.5, gap=1.8, pen=pens[slot])

    # the return fans: every row sweeps right and up into the @L/@A figure
    fans = [
        (240.0, 1206.0, RED, 417.0, 1231.0),
        (284.0, 1238.0, RED, 417.0, 1233.0),
        (284.0, 1272.0, BLUE, 419.0, 1236.0),
        (284.0, 1301.0, BLUE, 421.0, 1240.0),
        (284.0, 1334.0, OCHRE, 424.0, 1248.0),
    ]
    for sx, sy, slot, ex, ey in fans:
        pts = _bez((sx, sy), (sx + 105.0, sy + 4.0), (ex - 95.0, ey + 58.0), (ex, ey))
        out += _dash(M, pts, dash=0.45, gap=1.9, pen=pens[slot])
    out += _fdot(M, 417.0, 1231.0, 3.2, pen=pens[RED])

    # ---- @L/@A : the small interference figure ---------------------------
    out += _small_interference(M, rng, colors)

    # the black axis running into it from the left
    out += _dash(M, [(286.0, BACK_Y), (330.0, BACK_Y)], dash=0.5, gap=1.9,
                 pen=_pen(BLUE, colors))
    out += _dash(M, [(330.0, BACK_Y), (585.0, BACK_Y)], dash=2.6, gap=2.0, pen=bk)
    for x, r in ((363.0, 3.6), (377.0, 2.2), (389.0, 2.2), (554.0, 2.6),
                 (566.0, 2.0), (578.0, 3.4)):
        out += _fdot(M, x, BACK_Y, r, pen=bk)
    out += _fdot(M, SRC2_L, BACK_Y, 4.6, pen=bk)
    out += _fdot(M, IF2_CX - 7.5, BACK_Y, 3.4, pen=bk)
    out += _fdot(M, SRC2_R, BACK_Y, 4.6, pen=bk)
    out += _ocirc(M, SRC2_R, BACK_Y, 6.2, pen=bk)

    # ---- @L/@Z : the green stretch --------------------------------------
    zp: List[Packet] = [
        (662.0, 22.0, 11.0, 34.0, 0.0),
        (630.0, 10.0, 7.5, 9.0, 0.4),
        (692.0, 10.0, 7.5, 8.0, 0.8),
    ]
    out += _arrow(M, 590.0, BACK_Y, -1, 9.5, pen=gr)
    out += _dash(M, [(601.0, BACK_Y), (618.0, BACK_Y)], dash=0.5, gap=1.1, pen=gr)
    out += _line(M, [(618.0, BACK_Y), (706.0, BACK_Y)], pen=gr)
    out += wave_packet(M, 620.0, 704.0, BACK_Y, zp, pen=gr, env_lift=2.4)
    out += _arrow(M, 706.0, BACK_Y, -1, 9.5, pen=gr)
    out += _dash(M, [(717.0, BACK_Y), (733.0, BACK_Y)], dash=0.5, gap=1.1, pen=gr)
    out += _frac(M, "\u2202L", "\u2202Z", 665.0, 1342.0, 13.0, pen=gr, tracking=1.02)

    # ---- the purple mirror of the FFN, transposed and REVERSED -----------
    out += _line(M, [(737.0, BACK_Y), (1016.0, BACK_Y)], pen=pu)
    for nx in (737.0, 828.0, 930.0, 1016.0):
        out += _fdot(M, nx, BACK_Y, 4.4, pen=pu)
    proj_t: List[Packet] = [
        (782.0, 18.0, 10.5, 38.0, 0.0),
        (756.0, 10.0, 7.0, 12.0, 0.5),
        (810.0, 8.0, 6.5, 8.0, 0.9),
    ]
    exp_t: List[Packet] = [
        (976.0, 17.0, 10.0, 36.0, 0.0),
        (948.0, 10.0, 7.0, 11.0, 0.3),
        (1004.0, 7.0, 6.0, 7.0, 0.7),
    ]
    out += wave_packet(M, 740.0, 824.0, BACK_Y, proj_t, pen=pu, env_lift=2.4)
    out += _ffn_fan(M, 828.0, 930.0, BACK_Y, 42.0, pu, derivative=True)
    out += wave_packet(M, 934.0, 1013.0, BACK_Y, exp_t, pen=pu, env_lift=2.4)
    for nx in (828.0, 930.0):
        out += _dash(M, [(nx, 1238.0), (nx, 1308.0)], dash=0.6, gap=2.2, pen=bk)

    # THE POINT OF THE ROW: the three stages read backwards, transposed.
    out += _type_sup(M, "project", "T", 782.0, 1334.0, 12.0, pen=bk, tracking=0.85)
    out += _type_sup(M, "nonlinearity", "'", 880.0, 1334.0, 12.0, pen=bk, tracking=0.95,
                     sup_scale=0.72, sup_rise=0.42)
    out += _type_sup(M, "expand", "T", 973.0, 1334.0, 12.0, pen=bk, tracking=0.85)

    # ---- @L/@Y ----------------------------------------------------------
    out += _arrow(M, 1029.0, BACK_Y, -1, 9.5, pen=pu)
    out += _dash(M, [(1040.0, BACK_Y), (1060.0, BACK_Y)], dash=0.5, gap=1.1, pen=pu)
    out += _frac(M, "\u2202L", "\u2202Y", 1086.0, 1270.0, 14.0, pen=pu, tracking=1.02)

    # ---- the two links from the forward row down into the backward row ---
    out += _dash(M, _bez((FFN_N0, FWD_Y + 6.0), (712.0, 1180.0),
                         (676.0, 1200.0), (655.0, 1233.0)),
                 dash=0.5, gap=1.9, pen=gr)
    out += _dash(M, _bez((Y_END, FWD_Y + 8.0), (1040.0, 1170.0),
                         (1024.0, 1196.0), (1011.0, 1232.0)),
                 dash=0.5, gap=1.9, pen=pu)
    out += _fdot(M, 1011.0, 1233.0, 2.6, pen=pu)
    return out


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------


def attention_as_resonance_ffn(
    rng: SeededRNG, bounds: Bounds, colors: int = 6
) -> List[GCodeCommand]:
    M = _Map(bounds)
    out: List[GCodeCommand] = []
    out += _title(M, colors)
    out += _qk_block(M, colors, +1, _pen(RED, colors))
    out += _qk_block(M, colors, -1, _pen(BLUE, colors))
    out += _centre_fraction(M, colors)
    out += _interference(M, rng, colors)
    out += _softmax(M, colors)
    out += _v_block(M, colors)
    out += _forward_row(M, colors)
    out += _backward(M, rng, colors)
    return out
