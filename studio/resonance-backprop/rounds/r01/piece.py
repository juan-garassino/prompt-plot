"""ATTENTION AS RESONANCE (forward + backward) — exact recreation of
``studio/resonance-backprop/ref/reference.png``.

REPRODUCTION, not design.  Every coordinate below was measured off the
reference raster (1122 x 1402 px) — colour-segmented row scans for the axis
rows, ASCII pixel maps for the node columns, ink-bbox probes for the type —
and mapped through ONE uniform width-fit, so the layout is carried verbatim and
only the mark-making is translated into pen strokes.

What is REUSED (do not reinvent it)
-----------------------------------
* ``interference`` — the APPROVED two-source construction from the sibling
  plate ``studio/resonance/rounds/r01/piece.py`` (and its port in
  ``studio/resonance-clean``): Huygens crest ridges r_s = m*L with a source
  separation of an exact whole number of wavelengths (d = 35*L), so crest m of
  one family meets crest 35-m of the other ON the axis instead of beating
  against it.  Crests 1-21 solid, 22-51 dotted for the tonal fade.  Its
  crossing-safe anti-crowding guard (``_Guard``) is ported verbatim: a point is
  dropped only when a neighbouring stroke runs within 0.82 mm AND within 25
  degrees of parallel, so genuine crossings survive.  A level set of
  cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2) was tried on the sibling and thrown
  out — it draws every fringe twice and closes into a lattice of blobs.
  Only the frame is re-fitted here: this reference's figure sits at
  (560, 448) and is WIDER and FLATTER (d = 352 px, clip 345 x 132) because the
  backward band had to be made room for.
* ``packet_curves`` / ``draw_packet`` — the wave-packet helper (carrier x
  gaussian envelope, envelope outlined as a dotted trace that lifts off the
  axis) from the same sibling.
* ``_spline``, ``rdotted``, ``rdisc``, ``rcircle``, ``rdot_run``, ``radical``,
  ``tracked_type`` — the sibling's mark vocabulary.

What is NEW here
----------------
* the whole layout: five-row Q/K at y = 171..348, V as FOUR ochre rows at
  mid-LEFT, Z at y = 819 with "Z = AV" set BELOW it;
* the subtitle line, the four corner registration crosses;
* the two vertical rails at the far left ("forward pass" running down the upper
  half, "backward pass" running up the lower half) — the structural idea of
  the plate;
* the entire BACKWARD band (y 940..1300): dL/dZ, dL/dA, dL/dQ, dL/dK, dL/dV,
  every connector DASHED and carrying an ARROWHEAD.  Arrowheads are correct
  here and nowhere else on these plates: they mark gradient direction, not
  projection.

Type
----
The shared stroke font (promptplot.generative.generators._GLYPHS) now carries
lowercase, so "softmax", "forward pass", "backward pass" and "d_k" set
correctly, and ``proportional=True`` gives per-glyph advances.  Two maths signs
are NOT in it and are drawn as bespoke geometry, exactly as the sibling draws
its radical: the partial-derivative sign (``_PARTIAL``) and the radical
(``radical``).  They should be added centrally.  Serif/italic is a known
permanent gap — the reference's fractions are italic serif, ours are upright
single-stroke.

Pens (render palette crimson,dodgerblue,goldenrod,forestgreen,black):
    0 red · 1 blue · 2 ochre · 3 green · 4 black

Entry point: ``attention_as_resonance``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import _dot, _poly, circle, fill_disc, giant_type
from promptplot.generative.generators import _glyph_advance
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

# --- reference frame -------------------------------------------------------
# content box = the four corner registration crosses, measured on the raster
REF_X0, REF_Y0, REF_X1, REF_Y1 = 17.0, 17.0, 1105.0, 1385.0

_S = 1.0  # mm per reference px (set by _fit)
_OX = 0.0
_OY = 0.0
_BX0 = 0.0
_BX1 = 0.0


def _fit(bounds: Bounds) -> None:
    """Uniform width-fit of the reference content box into the drawable area."""
    global _S, _OX, _OY, _BX0, _BX1
    x0, y0, x1, y1 = bounds
    _BX0, _BX1 = x0, x1
    _S = (x1 - x0) / (REF_X1 - REF_X0)
    h = (REF_Y1 - REF_Y0) * _S
    _OX = x0
    _OY = y1 - (y1 - y0 - h) / 2.0


def P(rx: float, ry: float) -> Pt:
    """Reference px (y down) -> sheet mm (y up)."""
    return (_OX + (rx - REF_X0) * _S, _OY - (ry - REF_Y0) * _S)


def L(d: float) -> float:
    return d * _S


def PP(pts: Sequence[Pt]) -> List[Pt]:
    return [P(x, y) for x, y in pts]


# ---------------------------------------------------------------------------
# mark-making primitives (arguments in REFERENCE px unless noted)
# ---------------------------------------------------------------------------


def rpoly(ref_pts: Sequence[Pt], pen: Optional[int], f: int = 2000) -> List[GCodeCommand]:
    return _poly(PP(ref_pts), color=pen, f=f)


def rdot(rx: float, ry: float, rr: float, pen: Optional[int]) -> List[GCodeCommand]:
    x, y = P(rx, ry)
    return _dot(x, y, max(0.1, L(rr)), color=pen)


def rcircle(rx: float, ry: float, rr: float, pen: Optional[int], n: int = 0) -> List[GCodeCommand]:
    x, y = P(rx, ry)
    r = L(rr)
    if n <= 0:
        n = max(16, int(2 * math.pi * r / 0.55))
    return circle(x, y, r, pen=pen, n=n)


def rdisc(rx: float, ry: float, rr: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid node dot."""
    x, y = P(rx, ry)
    r = L(rr)
    if r <= 0.32:
        return _dot(x, y, max(r, 0.14), color=pen)
    return fill_disc(x, y, r, spacing=0.45, pen=pen)


def rdotted(
    ref_pts: Sequence[Pt],
    pen: Optional[int],
    dash: float = 0.55,
    gap: float = 1.35,
    f: int = 2000,
) -> List[GCodeCommand]:
    """Dotted polyline: dash/gap measured in mm along the mapped path."""
    pts = PP(ref_pts)
    out: List[GCodeCommand] = []
    if len(pts) < 2:
        return out
    period = dash + gap
    t = 0.0
    cur: List[Pt] = []
    step = 0.30
    for i in range(1, len(pts)):
        ax, ay = pts[i - 1]
        bx, by = pts[i]
        d = math.hypot(bx - ax, by - ay)
        if d < 1e-9:
            continue
        n = max(1, int(d / step))
        for j in range(1, n + 1):
            u = j / n
            px, py = ax + (bx - ax) * u, ay + (by - ay) * u
            t += d / n
            if (t % period) < dash:
                cur.append((px, py))
            else:
                if len(cur) >= 2:
                    out += _poly(cur, color=pen, f=f)
                cur = []
    if len(cur) >= 2:
        out += _poly(cur, color=pen, f=f)
    return out


def rdot_run(xs: Sequence[float], ry: float, rr: float, pen: Optional[int]) -> List[GCodeCommand]:
    """The reference's '....' axis continuations: round filled dots, not dashes."""
    out: List[GCodeCommand] = []
    for x in xs:
        out += rdisc(x, ry, rr, pen)
    return out


def _spline(way: Sequence[Pt], n_per: int = 40) -> List[Pt]:
    """Catmull-Rom through waypoints — for the long swooping convergence fans."""
    pts = list(way)
    ext = [pts[0]] + pts + [pts[-1]]
    out: List[Pt] = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        for j in range(n_per):
            t = j / n_per
            t2, t3 = t * t, t * t * t
            out.append(
                (
                    0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                           + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                           + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                    0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                           + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                           + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3),
                )
            )
    out.append(pts[-1])
    return out


def arrowhead(rx: float, ry: float, ang: float, size: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid triangular arrowhead, tip at (rx, ry), pointing along ``ang``
    (degrees measured in REFERENCE space, 0 = +x, 90 = down).

    This is the ONE place on these plates where an arrowhead is correct: in the
    backward band it marks gradient direction, not projection.
    """
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux                      # unit normal
    half = size * 0.40
    tip = (rx, ry)
    b1 = (rx - ux * size + px * half, ry - uy * size + py * half)
    b2 = (rx - ux * size - px * half, ry - uy * size - py * half)
    out = rpoly([tip, b1, b2, tip], pen, f=1600)
    # hatch the interior so it reads solid at plot scale
    n = max(2, int(L(size) / 0.34))
    for i in range(1, n):
        t = i / n
        ax = rx - ux * size * t
        ay = ry - uy * size * t
        hw = half * t
        out += rpoly([(ax + px * hw, ay + py * hw), (ax - px * hw, ay - py * hw)], pen, f=1600)
    return out


def cross(rx: float, ry: float, arm: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Corner registration cross."""
    return rpoly([(rx - arm, ry), (rx + arm, ry)], pen) + rpoly([(rx, ry - arm), (rx, ry + arm)], pen)


# ---------------------------------------------------------------------------
# the wave packet — carrier x gaussian envelope on an axis.
# lobes: (centre_px, sigma_px, amp_px, period_px, phase)
# ---------------------------------------------------------------------------


def packet_curves(
    y: float,
    xa: float,
    xb: float,
    lobes: Sequence[Tuple[float, float, float, float, float]],
) -> Tuple[List[Pt], List[Pt], List[Pt]]:
    """Return (wave, envelope_upper, envelope_lower) in reference px."""
    tmin = min(l[3] for l in lobes)
    step = max(0.45, tmin / 10.0)
    n = max(80, int((xb - xa) / step))
    wave: List[Pt] = []
    up: List[Pt] = []
    dn: List[Pt] = []
    for i in range(n + 1):
        x = xa + (xb - xa) * i / n
        e = 0.0
        v = 0.0
        for c, sg, a, per, ph in lobes:
            g = a * math.exp(-0.5 * ((x - c) / sg) ** 2)
            e += g
            v += g * math.sin(2 * math.pi * (x - c) / per + ph)
        wave.append((x, y + v))
        up.append((x, y + e))
        dn.append((x, y - e))
    return wave, up, dn


def _trim(pts: Sequence[Pt], y: float, floor_px: float) -> List[List[Pt]]:
    """Split an envelope trace into runs where it stands clear of the axis."""
    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    for x, yy in pts:
        if abs(yy - y) >= floor_px:
            cur.append((x, yy))
        else:
            if len(cur) >= 3:
                runs.append(cur)
            cur = []
    if len(cur) >= 3:
        runs.append(cur)
    return runs


def draw_packet(
    y: float,
    xa: float,
    xb: float,
    lobes: Sequence[Tuple[float, float, float, float, float]],
    pen: Optional[int],
    envelope: bool = True,
    env_floor: float = 0.0,
) -> List[GCodeCommand]:
    wave, up, dn = packet_curves(y, xa, xb, lobes)
    out = rpoly(wave, pen, f=1800)
    if envelope:
        amax = sum(l[2] for l in lobes)
        floor = env_floor or max(2.0, amax * 0.10)
        for run in _trim(up, y, floor) + _trim(dn, y, floor):
            out += rdotted(run, pen, dash=0.9, gap=0.95)
    return out


def node(rx: float, ry: float, rr: float, filled: bool, pen: Optional[int]) -> List[GCodeCommand]:
    return rdisc(rx, ry, rr, pen) if filled else rcircle(rx, ry, rr, pen, n=30)


# ---------------------------------------------------------------------------
# type
# ---------------------------------------------------------------------------

# The partial-derivative sign is NOT in the shared stroke font. Drawn here as
# bespoke geometry on the font's own 4x6 / baseline-0 grid, exactly as the
# sibling plate draws its radical. It belongs in the central font.
_PARTIAL: List[List[Pt]] = [
    [(1.3, 0.0), (0.4, 0.9), (0.4, 2.3), (1.3, 3.2), (2.5, 3.2), (3.3, 2.3),
     (3.3, 0.9), (2.5, 0.0), (1.3, 0.0)],
    [(3.3, 1.6), (3.3, 3.7), (2.9, 4.9), (2.0, 5.8), (0.8, 6.0)],
]
_PARTIAL_ADV = 4.9


def _adv(ch: str) -> float:
    return _PARTIAL_ADV if ch == "@" else _glyph_advance(ch)


def math_width(text: str, cap: float, track: float = 1.0) -> float:
    """Width in REFERENCE px of a proportional maths run ('@' = partial sign)."""
    return sum(_adv(c) for c in text) * (cap / 6.0) * track


def math_text(
    text: str,
    rx: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    track: float = 1.0,
    weight: float = 0.0,
    center: bool = False,
) -> List[GCodeCommand]:
    """Proportional maths type in reference px; '@' renders the partial sign."""
    h = L(cap)
    sc = h / 6.0
    if center:
        rx -= math_width(text, cap, track) / 2.0
    x, y = P(rx, baseline)
    out: List[GCodeCommand] = []
    for ch in text:
        if ch == "@":
            for st in _PARTIAL:
                out += _poly([(x + gx * sc, y + gy * sc) for gx, gy in st], color=pen, f=2200)
                if weight > 0:
                    out += _poly([(x + gx * sc + weight, y + gy * sc) for gx, gy in st],
                                 color=pen, f=2200)
        else:
            out += giant_type(ch, x, y, h, pen=pen, weight=weight, tip=0.26)
        x += _adv(ch) * sc * track
    return out


def frac(
    num: str,
    den: str,
    cx: float,
    rule_y: float,
    cap: float,
    pen: Optional[int],
    track: float = 1.0,
    weight: float = 0.0,
    gap: float = 5.0,
) -> List[GCodeCommand]:
    """A stacked fraction: numerator over a rule over denominator (ref px)."""
    wn = math_width(num, cap, track)
    wd = math_width(den, cap, track)
    half = max(wn, wd) / 2.0 + 3.0
    out = rpoly([(cx - half, rule_y), (cx + half, rule_y)], pen)
    out += math_text(num, cx, rule_y - gap, cap, pen, track=track, weight=weight, center=True)
    out += math_text(den, cx, rule_y + gap + cap, cap, pen, track=track, weight=weight,
                     center=True)
    return out


def tracked_type(
    text: str,
    cx: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    track: float = 1.33,
    weight: float = 0.0,
) -> List[GCodeCommand]:
    """Centred display type with reference letter-spacing (cap heights in ref px)."""
    h = L(cap)
    adv = h * track
    chars = list(text)
    width = adv * (len(chars) - 1) + h * 0.667
    x0 = P(cx, baseline)[0] - width / 2.0
    _, ybl = P(cx, baseline)
    out: List[GCodeCommand] = []
    for i, ch in enumerate(chars):
        if ch == " ":
            continue
        out += giant_type(ch, x0 + adv * i, ybl, h, pen=pen, weight=weight, tip=0.26)
    return out


def left_type(
    text: str, rx: float, baseline: float, cap: float, pen: Optional[int],
    track: float = 1.15, weight: float = 0.0,
) -> List[GCodeCommand]:
    h = L(cap)
    adv = h * track
    x, y = P(rx, baseline)
    out: List[GCodeCommand] = []
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        out += giant_type(ch, x + adv * i, y, h, pen=pen, weight=weight, tip=0.26)
    return out


def rail_type(
    text: str, rx: float, ry_bottom: float, cap: float, pen: Optional[int], track: float = 1.16,
) -> List[GCodeCommand]:
    """Rotated rail label: reads BOTTOM-TO-TOP with the glyph tops pointing left
    (angle = +90 deg in sheet mm), which is how the reference sets both rails.
    ``rx`` is the baseline column, ``ry_bottom`` the first glyph's origin."""
    h = L(cap)
    sc = h / 6.0
    x, y = P(rx, ry_bottom)
    out: List[GCodeCommand] = []
    for ch in text:
        if ch != " ":
            out += giant_type(ch, x, y, h, pen=pen, tip=0.26, angle=90.0)
        y += _adv(ch) * sc * track
    return out


def radical(rx: float, ry: float, cap: float, span: float, pen: Optional[int]) -> List[GCodeCommand]:
    """A drawn square-root sign (not in the stroke font)."""
    h = cap
    pts = [
        (rx, ry - 0.42 * h),
        (rx + 0.20 * h, ry - 0.30 * h),
        (rx + 0.45 * h, ry - 1.05 * h),
        (rx + span, ry - 1.05 * h),
    ]
    return rpoly(pts, pen)


# ---------------------------------------------------------------------------
# frame: corner crosses, title, subtitle, the two rails
# ---------------------------------------------------------------------------

CENTRE = 561.0


def _mirror(x: float) -> float:
    return 2 * CENTRE - x


def frame_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for cx, cy in ((38.0, 37.0), (1085.0, 37.0), (38.0, 1365.0), (1085.0, 1365.0)):
        out += cross(cx, cy, 20.0, pen)
    # the dotted tick that drops out of each corner cross toward the plate
    for cx in (38.0, 1085.0):
        out += rdotted([(cx, 56.0), (cx, 96.0)], pen, dash=0.5, gap=1.5)
        out += rdisc(cx, 102.0, 2.6, pen)
        out += rdotted([(cx, 1305.0), (cx, 1345.0)], pen, dash=0.5, gap=1.5)
        out += rdisc(cx, 1295.0, 2.6, pen)
    return out


def title_block(pen: Optional[int]) -> List[GCodeCommand]:
    out = tracked_type("ATTENTION AS RESONANCE", 568.0, 47.0, 20.0, pen, track=1.47)
    out += rpoly([(498.0, 66.0), (624.0, 66.0)], pen)
    out += rdisc(561.0, 66.0, 3.4, pen)
    # subtitle: three runs separated by mid-dots
    out += tracked_type("frequency interference", 393.0, 93.0, 11.0, pen, track=0.96)
    out += rdisc(527.0, 89.0, 2.4, pen)
    out += tracked_type("selection", 591.5, 93.0, 11.0, pen, track=0.94)
    out += rdisc(657.5, 89.0, 2.4, pen)
    out += tracked_type("backpropagation", 762.5, 93.0, 11.0, pen, track=1.01)
    return out


RAIL_X = 37.5


def rails_block(pen: Optional[int]) -> List[GCodeCommand]:
    """The two vertical rails that frame the plate: forward pass runs DOWN the
    upper half, backward pass runs UP the lower half."""
    out: List[GCodeCommand] = []
    # --- forward pass: T-bar at the top, arrow pointing DOWN ---------------
    out += rpoly([(RAIL_X - 11.0, 165.0), (RAIL_X + 11.0, 165.0)], pen)
    out += rpoly([(RAIL_X, 165.0), (RAIL_X, 318.0)], pen)
    out += rpoly([(RAIL_X, 483.0), (RAIL_X, 568.0)], pen)
    out += arrowhead(RAIL_X, 581.0, 90.0, 13.0, pen)
    out += rail_type("forward pass", 46.0, 478.0, 15.0, pen)
    # --- backward pass: arrow pointing UP, T-bar at the bottom ------------
    out += arrowhead(RAIL_X, 908.0, -90.0, 13.0, pen)
    out += rpoly([(RAIL_X, 921.0), (RAIL_X, 1013.0)], pen)
    out += rpoly([(RAIL_X, 1187.0), (RAIL_X, 1289.0)], pen)
    out += rpoly([(RAIL_X - 11.0, 1289.0), (RAIL_X + 11.0, 1289.0)], pen)
    out += rail_type("backward pass", 46.0, 1184.0, 15.0, pen)
    return out


# ---------------------------------------------------------------------------
# FORWARD — Q and K
# ---------------------------------------------------------------------------

Q_HOME = 127.0
Q_STUB = 113.0          # the axis runs a little past the home node
Q_MID = 301.0           # the second aligned node column

# (y, far_x, home_filled, mid_marker, tail_dot_x, lobes, ghost_lobes)
Q_ROWS = [
    (
        171.0, 301.0, False, "open", None,
        [(228.0, 29.0, 40.0, 11.4, 0.0), (172.0, 11.0, 6.0, 8.4, 1.1)],
        [(238.0, 26.0, 26.0, 21.0, 2.0)],
    ),
    (
        215.0, 352.0, True, "open", 352.0,
        [(196.0, 23.0, 32.0, 9.6, 0.4), (324.0, 13.0, 15.0, 9.0, 2.2)],
        [(206.0, 22.0, 18.0, 16.0, 1.4)],
    ),
    (
        260.0, 388.0, False, "open", None,
        [(250.0, 31.0, 40.0, 14.6, 0.7), (196.0, 15.0, 10.0, 9.6, 0.2),
         (330.0, 15.0, 14.0, 10.2, 1.5)],
        [(240.0, 25.0, 22.0, 19.0, 2.6)],
    ),
    (
        305.0, 357.0, True, "open", 357.0,
        [(206.0, 26.0, 30.0, 9.8, 0.9), (330.0, 12.0, 13.0, 9.4, 0.3)],
        [(214.0, 23.0, 17.0, 15.5, 0.8)],
    ),
    (
        348.0, 305.0, False, None, None,
        [(240.0, 30.0, 38.0, 10.8, 0.5), (176.0, 12.0, 6.0, 8.2, 2.0)],
        [(246.0, 26.0, 24.0, 17.5, 1.2)],
    ),
]
Q_VERTS = [(127.0, 134.0, 402.0), (189.0, 118.0, 210.0), (301.0, 128.0, 424.0),
           (352.0, 196.0, 330.0), (388.0, 204.0, 392.0)]

# K is NOT a literal mirror in the reference; it carries its own packet table.
K_LOBES = [
    ([(892.0, 28.0, 38.0, 11.0, 0.5), (952.0, 12.0, 8.0, 8.6, 1.6)],
     [(884.0, 26.0, 25.0, 20.0, 0.6)]),
    ([(922.0, 24.0, 33.0, 9.4, 1.2), (798.0, 13.0, 14.0, 9.2, 0.3)],
     [(914.0, 22.0, 18.0, 16.4, 2.1)]),
    ([(870.0, 31.0, 40.0, 15.0, 0.2), (930.0, 15.0, 11.0, 9.8, 1.4),
      (792.0, 14.0, 13.0, 10.0, 2.3)],
     [(880.0, 25.0, 22.0, 18.5, 0.9)]),
    ([(916.0, 26.0, 29.0, 10.2, 2.0), (790.0, 12.0, 13.0, 9.0, 1.0)],
     [(908.0, 23.0, 17.0, 15.0, 0.4)]),
    ([(880.0, 30.0, 39.0, 11.2, 1.5), (946.0, 12.0, 6.0, 8.4, 0.7)],
     [(874.0, 26.0, 24.0, 18.0, 2.4)]),
]


def qk_block(pen: Optional[int], mirror: bool) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []

    def mx(x: float) -> float:
        return _mirror(x) if mirror else x

    for i, (y, far, home_filled, mid, tail, lobes, ghosts) in enumerate(Q_ROWS):
        if mirror:
            lobes, ghosts = K_LOBES[i]
        out += rdot_run([mx(v) for v in (87.0, 96.0, 105.0)], y, 2.0, pen)
        out += rpoly([(mx(Q_STUB), y), (mx(far), y)], pen)
        out += node(mx(Q_HOME), y, 4.6, home_filled, pen)
        if mid is not None:
            out += rcircle(mx(Q_MID), y, 5.2, pen, n=30)
        if far != Q_MID:
            out += rcircle(mx(far), y, 5.2, pen, n=30)
        if tail is not None:
            out += rdisc(mx(tail + 8.0), y, 2.6, pen)
        xa = min(l[0] - 3.1 * l[1] for l in lobes)
        xb = max(l[0] + 3.1 * l[1] for l in lobes)
        out += draw_packet(y, min(xa, xb), max(xa, xb), lobes, pen)
        if ghosts:
            gxa = min(l[0] - 3.0 * l[1] for l in ghosts)
            gxb = max(l[0] + 3.0 * l[1] for l in ghosts)
            gw, _, _ = packet_curves(y, gxa, gxb, ghosts)
            out += rdotted(gw, pen, dash=0.45, gap=0.95)

    for x, y0, y1 in Q_VERTS:
        out += rdotted([(mx(x), y0), (mx(x), y1)], pen, dash=0.5, gap=1.25)

    if mirror:
        out += left_type("K", 990.0, 138.0, 30.0, pen, track=1.1, weight=0.34)
    else:
        out += left_type("Q", 108.0, 138.0, 30.0, pen, track=1.1, weight=0.34)
    return out


def fraction_block(pen: Optional[int]) -> List[GCodeCommand]:
    """Q . K^T over a rule over sqrt(d_k) — a true stacked fraction."""
    out: List[GCodeCommand] = []
    cap = 24.0
    h = L(cap)
    x, y = P(525.0, 226.0)
    out += giant_type("Q", x, y, h, pen=pen, weight=0.2, tip=0.26)
    out += rdisc(556.0, 217.0, 2.6, pen)
    x2, _ = P(567.0, 226.0)
    out += giant_type("K", x2, y, h, pen=pen, weight=0.2, tip=0.26)
    x3, y3 = P(589.0, 212.0)
    out += giant_type("T", x3, y3, h * 0.58, pen=pen, weight=0.1, tip=0.26)
    out += rpoly([(520.0, 236.0), (600.0, 236.0)], pen)
    out += radical(522.0, 266.0, 22.0, 40.0, pen)
    xd, yd = P(539.0, 266.0)
    out += giant_type("d", xd, yd, L(19.0), pen=pen, weight=0.14, tip=0.26)
    xk, yk = P(555.0, 271.0)
    out += giant_type("k", xk, yk, L(12.0), pen=pen, weight=0.08, tip=0.26)
    # the central spine above and below the fraction
    out += rdotted([(561.0, 148.0), (561.0, 196.0)], pen, dash=0.6, gap=1.5)
    out += rdotted([(561.0, 278.0), (561.0, 326.0)], pen, dash=0.6, gap=1.5)
    return out


# ---------------------------------------------------------------------------
# THE HERO — two-source interference.
# Construction ported verbatim from the APPROVED sibling plate,
# studio/resonance/rounds/r01/piece.py :: _interference (Huygens crest ridges).
# Only the frame is re-fitted: this reference's figure is wider and flatter.
# ---------------------------------------------------------------------------

IF_CX, IF_CY = 560.0, 448.0
IF_D = 352.0
SRC_L, SRC_R = IF_CX - IF_D / 2, IF_CX + IF_D / 2
DROPS = [383.0, 433.0, 475.0, 512.0, 560.0, 608.0, 643.0, 689.0, 735.0]


class _Guard:
    """Anti-crowding that keeps the crossings.

    Two crest families run TANGENT to one another along the axis of a two-source
    diagram, the one place a pen cannot resolve them. A plain occupancy grid
    also deletes the CROSSINGS, which are the whole point, so this rejects a
    point only when a nearby point of another stroke is within ``sep`` AND its
    tangent is within 25 degrees of parallel. Real crossings pass through.
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


def interference(pen: Optional[int], rng: SeededRNG) -> List[GCodeCommand]:
    """The hero, computed as a real two-source field.

    Huygens construction: a crest of the wave from source s is the locus
    r_s = m * L. Drawing both crest families is exactly cos(k r1) = 1 and
    cos(k r2) = 1 with k = 2 pi / L -- the RIDGE lines of the instantaneous
    superposition A = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2), rather than a
    level set of it (a level set draws every fringe twice and closes into a
    lattice of blobs).

    The families cross on the hyperbolae r1 - r2 = const; between the sources
    those crossings pack into the fine vertical comb, and the lens-shaped cells
    they cut near the midpoint are what reads as a third ring system. The
    separation is an exact whole number of wavelengths (d = 35 L) so the two
    families meet ON the axis instead of beating against it.
    """
    bk = pen
    out: List[GCodeCommand] = []

    # d = 59 * L here (not the sibling's 35): the property that matters is that
    # the separation is a WHOLE number of wavelengths, so crest m of one family
    # meets crest 59-m of the other ON the axis. 59 is what keeps the fringe
    # pitch at the reference's ~1.0 mm now that d has grown to 352 px.
    n_lam = 59
    lam = IF_D / n_lam                      # 5.97 ref px = 0.99 mm on A4
    R_BULL = 9.0 * lam                      # the solid bullseye around a source
    LENS_A, LENS_B = 100.0, 40.0            # the solid comb at the midpoint
    a_out, b_out = 300.0, 98.0              # the dotted field
    sid = 0
    guard = _Guard(0.82)

    def ring(cx: float, r: float, dense: bool = True):
        n = max(56, int(r * (2.0 if dense else 1.05)))
        return [
            (cx + r * math.cos(2 * math.pi * t / n), IF_CY + r * math.sin(2 * math.pi * t / n))
            for t in range(n + 1)
        ]

    def in_lens(px: float, py: float) -> bool:
        return ((px - IF_CX) / LENS_A) ** 2 + ((py - IF_CY) / LENS_B) ** 2 <= 1.0

    def in_bull(px: float, py: float, pad: float = 0.0) -> bool:
        return (math.hypot(px - SRC_L, py - IF_CY) <= R_BULL + pad
                or math.hypot(px - SRC_R, py - IF_CY) <= R_BULL + pad)

    def emit(pts, keep, dotted: bool):
        """Emit the run of a crest that passes ``keep``.  Solid runs also go
        through the parallel-crowding guard."""
        nonlocal sid
        sid += 1
        res: List[GCodeCommand] = []
        run: List[Pt] = []
        for j, (px, py) in enumerate(pts):
            ok = keep(px, py)
            if ok and not dotted:
                qx, qy = pts[min(j + 1, len(pts) - 1)]
                mx_, my_ = P(px, py)
                nx_, ny_ = P(qx, qy)
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
                    res += (rdotted(run, bk, dash=1.45, gap=0.75) if dotted
                            else rpoly(run, bk, f=2600))
                run = []
        if len(run) >= 4:
            res += (rdotted(run, bk, dash=1.45, gap=0.75) if dotted
                    else rpoly(run, bk, f=2600))
        return res

    for sx in (SRC_L, SRC_R):
        # 1. the SOLID bullseye: the near field, where 1/sqrt(r) makes this
        #    source's term dominate and the field reads as clean rings.
        for m in range(1, 10):
            out += emit(ring(sx, m * lam), lambda px, py: True, False)
        # 2. the SOLID comb at the midpoint: the same crests, carried on into
        #    the lens-shaped cells the two families cut out of each other.
        for m in range(10, 51):
            out += emit(ring(sx, m * lam), in_lens, False)
        # 3. the DOTTED tonal field, everywhere else inside the big oval.
        for m in range(10, 64, 3):
            out += emit(
                ring(sx, m * lam, dense=False),
                lambda px, py: (((px - IF_CX) / a_out) ** 2 + ((py - IF_CY) / b_out) ** 2 <= 1.0
                                and not in_bull(px, py, 5.0) and not in_lens(px, py)),
                True,
            )

    # --- outer sparse dotted ellipses around each source -------------------
    for sx in (SRC_L, SRC_R):
        for a in (188.0, 248.0):
            b = a * 0.34
            rr = [
                (sx + a * math.cos(2 * math.pi * t / 240),
                 IF_CY + b * math.sin(2 * math.pi * t / 240))
                for t in range(241)
            ]
            rr = [q for q in rr
                  if _BX0 + 2 < P(*q)[0] < _BX1 - 2 and not in_bull(q[0], q[1], 10.0)]
            if len(rr) > 6:
                out += rdotted(rr, bk, dash=0.55, gap=1.15)

    # --- the horizontal axis through the figure ---------------------------
    out += rpoly([(300.0, IF_CY), (820.0, IF_CY)], bk)
    for sgn in (1, -1):
        base = IF_CX - sgn * 259.0
        out += rcircle(base, IF_CY, 5.0, bk, n=30)
        for j in range(3):
            out += rdisc(base - sgn * (16.0 + 16.0 * j), IF_CY, 2.2, bk)
        out += rdisc(IF_CX - sgn * 243.0, IF_CY, 3.0, bk)
        out += rdisc(IF_CX - sgn * 227.0, IF_CY, 3.2, bk)
    out += rdisc(IF_CX, IF_CY, 4.6, bk)
    out += rdisc(SRC_L, IF_CY, 4.4, bk)
    out += rdisc(SRC_R, IF_CY, 4.4, bk)

    # --- the beaded dot columns that hang off each dropline ---------------
    k = 2 * math.pi / lam

    def field(px, py):
        d1 = math.hypot(px - SRC_L, py - IF_CY) + 4.0
        d2 = math.hypot(px - SRC_R, py - IF_CY) + 4.0
        return math.cos(k * d1) / math.sqrt(d1) + math.cos(k * d2) / math.sqrt(d2)

    placed: List[Tuple[float, float, float]] = []

    def place(px, py, r):
        if r < 0.7 or not (_BX0 + 3 < P(px, py)[0] < _BX1 - 3):
            return []
        for qx, qy, qr in placed:
            if math.hypot(px - qx, py - qy) < (r + qr) * 1.3 + 4.0:
                return []
        placed.append((px, py, r))
        return rdisc(px, py, r, bk)

    for cx in DROPS:
        heavy = cx in (SRC_L, IF_CX, SRC_R)
        for j in range(-5, 6):
            if j:
                r = (1.3 if heavy else 0.9) + (2.8 if heavy else 1.9) * math.exp(-abs(j) / 3.0)
                out += place(cx, IF_CY + 22.0 * j, r)
    for _ in range(10):
        px = IF_CX + rng.uniform(-300.0, 300.0)
        py = IF_CY + rng.uniform(-120.0, 120.0)
        out += place(px, py, min(3.4, 0.9 + 14.0 * abs(field(px, py))))

    # --- vertical dotted droplines, up and down ---------------------------
    for j, x in enumerate(DROPS):
        top = 330.0 if x in (383.0, 560.0, 735.0) else 356.0
        out += rdotted([(x, top), (x, IF_CY - 6.0)], bk, dash=0.5, gap=1.7)
        out += rdisc(x, top - 8.0, 2.0, bk)
        bot = 664.0 if j % 2 == 0 else 640.0
        out += rdotted([(x, IF_CY + 6.0), (x, bot)], bk, dash=0.5, gap=1.7)
    out += rcircle(IF_CX, 372.0, 4.6, bk, n=28)
    out += rcircle(IF_CX, 524.0, 4.6, bk, n=28)
    return out


# ---------------------------------------------------------------------------
# FORWARD — softmax row, V, Z
# ---------------------------------------------------------------------------

SOFT_Y = 687.0
# (x, height, width, apex marker)
SOFT_PEAKS = [
    (383.0, 26.0, 5.6, "open"),
    (475.0, 55.0, 5.4, "open"),
    (560.0, 62.0, 5.2, "fill"),
    (643.0, 60.0, 5.4, "open"),
    (735.0, 34.0, 5.8, "open"),
]
SOFT_GHOSTS = [(433.0, 20.0), (512.0, 17.0), (609.0, 22.0), (689.0, 18.0)]
SOFT_BASE = [
    (383.0, "open"), (433.0, "open"), (475.0, "open"), (512.0, "dot"), (560.0, "open"),
    (609.0, "open"), (643.0, "open"), (689.0, "dot"), (735.0, "open"),
]


def _soft_y(x: float) -> float:
    v = 0.0
    for c, h, w, _m in SOFT_PEAKS:
        v += h / (1.0 + ((x - c) / w) ** 2) ** 1.5
    return SOFT_Y - v


def softmax_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += rpoly([(350.0, SOFT_Y), (770.0, SOFT_Y)], pen)
    out += rdot_run([307.0, 317.0, 327.0, 340.0], SOFT_Y, 2.2, pen)
    out += rdot_run([780.0, 790.0, 800.0, 811.0], SOFT_Y, 2.2, pen)

    n = 780
    curve = [(350.0 + (770.0 - 350.0) * i / n, 0.0) for i in range(n + 1)]
    out += rpoly([(x, _soft_y(x)) for x, _ in curve], pen, f=1800)

    ghost = []
    for i in range(460):
        x = 360.0 + (760.0 - 360.0) * i / 459
        v = 0.0
        for c, h in SOFT_GHOSTS:
            v += h / (1.0 + ((x - c) / 6.2) ** 2) ** 1.5
        ghost.append((x, SOFT_Y - v))
    out += rdotted(ghost, pen, dash=0.4, gap=1.5)

    for c, h, _w, mark in SOFT_PEAKS:
        out += rpoly([(c, SOFT_Y), (c, SOFT_Y - h + 4.0)], pen)
        out += node(c, SOFT_Y - h - 6.0, 5.2, mark == "fill", pen)
    for x, kind in SOFT_BASE:
        if kind == "open":
            out += rcircle(x, SOFT_Y, 5.2, pen, n=28)
        else:
            out += rdisc(x, SOFT_Y, 2.8, pen)

    out += _a_formula(pen)
    return out


def _a_formula(pen: Optional[int]) -> List[GCodeCommand]:
    """A = softmax(QK^T / sqrt(d_k)) — token x-positions traced off the raster."""
    y = 604.0
    cap = 19.0
    h = L(cap)
    sc = h / 6.0
    out: List[GCodeCommand] = []

    def tok(text: str, rx: float, ry: float, hh: float, w: float = 0.12, track: float = 1.06):
        x, ym = P(rx, ry)
        for ch in text:
            out.extend(giant_type(ch, x, ym, hh, pen=pen, weight=w, tip=0.26))
            x += _adv(ch) * (hh / 6.0) * track

    tok("A", 425.0, y, h, 0.16)
    tok("=", 450.0, y, h, 0.12)
    tok("softmax", 477.0, y, h, 0.1, track=1.0)
    tok("(", 564.0, y, h, 0.1)
    tok("QK", 575.0, y, h, 0.14, track=1.08)
    tok("T", 622.0, y - cap * 0.56, h * 0.58, 0.08)
    tok("/", 637.0, y, h, 0.1)
    out += radical(656.0, y, 17.0, 26.0, pen)
    tok("d", 666.0, y, h * 0.94, 0.12)
    tok("k", 680.0, y + cap * 0.20, h * 0.60, 0.06)
    tok(")", 692.0, y, h, 0.1)
    return out


V_L, V_R = 97.0, 240.0
V_ROWS = [
    (669.0, False, [(178.0, 24.0, 26.0, 8.4, 0.2)], [(160.0, 20.0, 14.0, 15.0, 1.0)]),
    (702.0, False, [(166.0, 22.0, 22.0, 7.6, 1.1)], [(150.0, 18.0, 12.0, 13.5, 0.4)]),
    (734.0, True, [(184.0, 23.0, 24.0, 9.6, 0.6), (140.0, 14.0, 10.0, 7.4, 2.0)],
     [(170.0, 20.0, 13.0, 16.0, 2.2)]),
    (766.0, False, [(160.0, 24.0, 22.0, 7.8, 0.9)], [(146.0, 19.0, 12.0, 14.0, 0.7)]),
]


def v_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for y, left_fill, lobes, ghosts in V_ROWS:
        out += rdot_run([54.0, 63.0, 72.0], y, 2.0, pen)
        out += rpoly([(81.0, y), (237.0, y)], pen)
        out += node(V_L, y, 4.4, left_fill, pen)
        out += rcircle(V_R, y, 5.0, pen, n=28)
        out += rdot_run([250.0, 259.0, 268.0], y, 2.0, pen)
        xa = min(l[0] - 3.1 * l[1] for l in lobes)
        xb = max(l[0] + 3.1 * l[1] for l in lobes)
        out += draw_packet(y, xa, xb, lobes, pen)
        gxa = min(l[0] - 3.0 * l[1] for l in ghosts)
        gxb = max(l[0] + 3.0 * l[1] for l in ghosts)
        gw, _, _ = packet_curves(y, gxa, gxb, ghosts)
        out += rdotted(gw, pen, dash=0.45, gap=0.95)
    for x in (V_L, V_R):
        out += rdotted([(x, 640.0), (x, 792.0)], pen, dash=0.5, gap=1.25)
    out += left_type("V", 92.0, 640.0, 28.0, pen, track=1.1, weight=0.34)
    return out


Z_Y = 819.0
Z_LOBES = [
    (560.0, 46.0, 70.0, 12.6, 0.0),
    (492.0, 26.0, 15.0, 10.4, 1.3),
    (628.0, 26.0, 15.0, 10.4, 2.4),
    (452.0, 20.0, 9.0, 8.4, 0.6),
    (668.0, 20.0, 9.0, 8.4, 2.9),
]


def z_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += rdotted([(207.0, Z_Y), (250.0, Z_Y)], pen, dash=0.6, gap=1.4)
    out += rpoly([(250.0, Z_Y), (872.0, Z_Y)], pen)
    out += rdot_run([166.0, 177.0, 188.0], Z_Y, 2.2, pen)
    out += rdisc(201.0, Z_Y, 3.0, pen)
    out += rdot_run([931.0, 942.0, 954.0], Z_Y, 2.4, pen)
    out += rdotted([(880.0, Z_Y), (922.0, Z_Y)], pen, dash=0.6, gap=1.4)
    out += draw_packet(Z_Y, 420.0, 700.0, Z_LOBES, pen, env_floor=3.0)

    # a second, narrower envelope inside
    _, up2, dn2 = packet_curves(Z_Y, 430.0, 692.0, [(560.0, 32.0, 46.0, 9.4, 0.0)])
    for run in _trim(up2, Z_Y, 4.0) + _trim(dn2, Z_Y, 4.0):
        out += rdotted(run, pen, dash=0.85, gap=1.05)

    for x in (277.0, 845.0):
        out += rcircle(x, Z_Y, 5.6, pen, n=30)
    out += rcircle(560.0, Z_Y, 6.4, pen, n=32)
    # the two side "eyes"
    for x in (443.0, 675.0):
        for a, b in ((9.0, 15.0), (4.2, 7.0)):
            ring = [
                (x + a * math.cos(2 * math.pi * i / 56), Z_Y + b * math.sin(2 * math.pi * i / 56))
                for i in range(57)
            ]
            out += rpoly(ring, pen)
        out += rpoly([(x, Z_Y - 19.0), (x, Z_Y + 19.0)], pen)
    out += rdisc(560.0, 733.0, 4.4, pen)
    out += tracked_type("Z = AV", 561.0, 913.0, 22.0, pen, track=0.90, weight=0.28)
    return out


# ---------------------------------------------------------------------------
# forward convergence fans
# ---------------------------------------------------------------------------

# Q -> the interference: the reference's red curves leave each Q row, sweep
# right, then WATERFALL down a descending chain of dots to the figure's axis.
Q_FAN = [
    [(312, 171), (372, 180), (404, 220), (410, 272), (400, 322), (390, 356)],
    [(364, 216), (412, 232), (430, 276), (424, 322), (406, 362), (396, 384)],
    [(400, 262), (438, 288), (446, 326), (432, 366), (410, 398), (398, 412)],
    [(368, 306), (410, 334), (418, 368), (404, 400), (382, 424), (370, 434)],
    [(316, 349), (352, 382), (358, 408), (346, 428), (328, 440), (318, 444)],
    [(250, 372), (276, 404), (282, 424), (300, 436), (318, 442), (328, 444)],
    [(192, 388), (206, 414), (232, 430), (270, 440), (300, 445), (316, 446)],
    [(150, 420), (176, 434), (214, 442), (256, 447), (288, 448), (302, 448)],
]

# softmax -> V : on this plate V sits at mid-LEFT, so the ochre feed runs BACK
A_FAN = [
    [(383, 700), (356, 726), (320, 748), (280, 762), (252, 766), (240, 768)],
    [(433, 700), (394, 728), (342, 748), (294, 756), (258, 750), (244, 744)],
    [(475, 700), (430, 724), (370, 738), (314, 734), (270, 720), (246, 710)],
    [(512, 700), (464, 718), (398, 726), (332, 716), (280, 698), (250, 684)],
    [(560, 700), (508, 714), (436, 714), (358, 700), (292, 680), (250, 670)],
    [(609, 700), (552, 712), (474, 708), (388, 690), (306, 670), (254, 662)],
]

# V and the softmax tail -> Z
V_FAN = [
    [(252, 664), (330, 668), (416, 690), (490, 730), (534, 776), (548, 806)],
    [(252, 700), (340, 708), (432, 730), (506, 766), (546, 794), (556, 810)],
    [(252, 734), (352, 748), (446, 768), (516, 792), (552, 806), (562, 812)],
    [(252, 768), (360, 784), (456, 798), (522, 808), (556, 814), (566, 816)],
]
Z_FAN = [
    [(643, 700), (700, 722), (756, 754), (786, 786), (788, 806), (778, 816)],
    [(689, 700), (756, 726), (812, 762), (840, 792), (838, 810), (824, 818)],
    [(735, 700), (810, 730), (866, 770), (888, 798), (880, 812), (864, 818)],
]


def fan(ways, pen: Optional[int], endcap: float = 0.0,
        dots: Sequence[float] = ()) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for way in ways:
        pts = _spline(way, n_per=30)
        out += rdotted(pts, pen, dash=0.85, gap=1.15)
        if endcap:
            out += rdisc(pts[-1][0], pts[-1][1], endcap, pen)
            for u in dots:
                q = pts[int(len(pts) * u)]
                out += rdisc(q[0], q[1], endcap * 0.75, pen)
    return out


# ---------------------------------------------------------------------------
# BACKWARD BAND — the real addition.  Every connector here is DASHED and
# carries an ARROWHEAD: on this plate an arrowhead means gradient direction.
# ---------------------------------------------------------------------------

DZ_Y = 1060.0
DZ_LOBES = [
    (560.0, 34.0, 52.0, 10.4, 0.0),
    (505.0, 20.0, 12.0, 8.8, 1.3),
    (616.0, 20.0, 12.0, 8.8, 2.4),
]

DA_Y = 1268.0
DA_PEAKS = [
    (451.0, 58.0, 6.6, "open"),
    (512.0, 48.0, 4.4, None),
    (560.0, 56.0, 5.0, "fill"),
    (608.0, 48.0, 4.4, None),
    (672.0, 60.0, 6.8, "open"),
]
DA_BASE = [451.0, 485.0, 512.0, 560.0, 608.0, 637.0, 672.0]

DQ_ROWS = [1210.0, 1243.0, 1281.0]
DQ_L, DQ_R = 122.0, 295.0
DQ_LOBES = [
    [(232.0, 25.0, 30.0, 9.6, 0.3), (172.0, 12.0, 8.0, 7.6, 1.4)],
    [(206.0, 22.0, 22.0, 8.2, 1.2), (268.0, 13.0, 12.0, 8.0, 0.5)],
    [(228.0, 26.0, 30.0, 10.4, 2.0), (176.0, 12.0, 7.0, 7.4, 0.8)],
]
DK_LOBES = [
    [(898.0, 25.0, 30.0, 9.2, 1.1), (956.0, 12.0, 8.0, 7.4, 0.2)],
    [(916.0, 22.0, 22.0, 8.6, 0.4), (846.0, 13.0, 12.0, 7.8, 1.7)],
    [(896.0, 26.0, 30.0, 10.0, 2.3), (954.0, 12.0, 7.0, 7.2, 1.0)],
]

DV_ROWS = [1025.0, 1060.0]
DV_L, DV_R = 889.0, 1002.0
DV_LOBES = [
    [(938.0, 19.0, 22.0, 7.4, 0.4)],
    [(950.0, 20.0, 24.0, 7.8, 1.6)],
]


def _dz_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += frac("@L", "@Z", 561.0, 970.0, 20.0, pen, track=1.02, weight=0.12, gap=4.0)
    out += rdisc(561.0, 1002.0, 4.0, pen)
    out += rdotted([(561.0, 1010.0), (561.0, 1040.0)], pen, dash=0.5, gap=1.4)
    out += rpoly([(441.0, DZ_Y), (684.0, DZ_Y)], pen)
    out += rcircle(451.0, DZ_Y, 5.4, pen, n=30)
    out += rcircle(672.0, DZ_Y, 5.4, pen, n=30)
    out += draw_packet(DZ_Y, 470.0, 650.0, DZ_LOBES, pen, env_floor=3.0)
    _, up2, dn2 = packet_curves(DZ_Y, 478.0, 644.0, [(560.0, 26.0, 34.0, 8.6, 0.0)])
    for run in _trim(up2, DZ_Y, 4.0) + _trim(dn2, DZ_Y, 4.0):
        out += rdotted(run, pen, dash=0.85, gap=1.05)
    return out


def _da_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += frac("@L", "@A", 561.0, 1169.0, 20.0, pen, track=1.02, weight=0.12, gap=4.0)

    def cy(x: float) -> float:
        v = 0.0
        for c, h, w, _m in DA_PEAKS:
            v += h / (1.0 + ((x - c) / w) ** 2) ** 1.5
        return DA_Y - v

    out += rpoly([(399.0, DA_Y), (738.0, DA_Y)], pen)
    out += rdot_run([349.0, 358.0, 367.0, 378.0], DA_Y, 2.2, pen)
    out += rdot_run([748.0, 757.0, 766.0, 777.0], DA_Y, 2.2, pen)
    n = 640
    out += rpoly([(399.0 + (738.0 - 399.0) * i / n,
                   cy(399.0 + (738.0 - 399.0) * i / n)) for i in range(n + 1)], pen, f=1800)
    ghost = []
    for i in range(420):
        x = 405.0 + (732.0 - 405.0) * i / 419
        v = 0.0
        for c, h in ((485.0, 20.0), (537.0, 16.0), (585.0, 16.0), (637.0, 20.0)):
            v += h / (1.0 + ((x - c) / 6.0) ** 2) ** 1.5
        ghost.append((x, DA_Y - v))
    out += rdotted(ghost, pen, dash=0.4, gap=1.5)
    for c, h, _w, mark in DA_PEAKS:
        out += rpoly([(c, DA_Y), (c, DA_Y - h + 4.0)], pen)
        if mark:
            out += node(c, DA_Y - h - 4.0, 5.2, mark == "fill", pen)
    for x in DA_BASE:
        out += rcircle(x, DA_Y, 5.2, pen, n=28) if x != 560.0 else rdisc(x, DA_Y, 4.0, pen)
    # droplines up out of the peak row toward dL/dZ
    for x in (451.0, 485.0, 512.0, 560.0, 608.0, 637.0, 672.0):
        out += rdotted([(x, DA_Y - 8.0), (x, 1300.0)], pen, dash=0.5, gap=1.6)
    for x, y0 in ((451.0, 1100.0), (560.0, 1112.0), (672.0, 1100.0)):
        out += rdotted([(x, y0), (x, DA_Y - 66.0)], pen, dash=0.5, gap=1.6)
        out += rdisc(x, y0 - 8.0, 3.0, pen)
    out += rdisc(561.0, 1320.0, 3.0, pen)
    return out


def _dqk_block(pen: Optional[int], mirror: bool) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []

    def mx(x: float) -> float:
        return _mirror(x) if mirror else x

    lobes_tbl = DK_LOBES if mirror else DQ_LOBES
    for i, y in enumerate(DQ_ROWS):
        out += rdot_run([mx(v) for v in (84.0, 95.0, 107.0)], y, 2.0, pen)
        out += rpoly([(mx(114.0), y), (mx(DQ_R + 5.0), y)], pen)
        out += rcircle(mx(DQ_L), y, 5.0, pen, n=28)
        out += rcircle(mx(DQ_R), y, 5.0, pen, n=28)
        lb = lobes_tbl[i] if mirror else [(mx(c), s, a, p, ph) for c, s, a, p, ph in lobes_tbl[i]]
        xa = min(l[0] - 3.1 * l[1] for l in lb)
        xb = max(l[0] + 3.1 * l[1] for l in lb)
        out += draw_packet(y, xa, xb, lb, pen)
    for x in (DQ_L, DQ_R):
        out += rdotted([(mx(x), 1186.0), (mx(x), 1304.0)], pen, dash=0.5, gap=1.25)
    out += frac("@L", "@Q" if not mirror else "@K", mx(91.0), 1169.0, 19.0, pen,
                track=1.02, weight=0.12, gap=4.0)
    return out


def _dv_block(pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for i, y in enumerate(DV_ROWS):
        out += rpoly([(881.0, y), (1010.0, y)], pen)
        out += rcircle(DV_L, y, 5.0, pen, n=28)
        out += rcircle(DV_R, y, 5.0, pen, n=28)
        out += rdot_run([1018.0, 1028.0, 1038.0], y, 2.2, pen)
        lb = DV_LOBES[i]
        xa = min(l[0] - 3.1 * l[1] for l in lb)
        xb = max(l[0] + 3.1 * l[1] for l in lb)
        out += draw_packet(y, xa, xb, lb, pen)
    for x in (DV_L, DV_R):
        out += rdotted([(x, 998.0), (x, 1090.0)], pen, dash=0.5, gap=1.25)
    out += frac("@L", "@V", 1081.0, 1042.0, 18.0, pen, track=1.02, weight=0.12, gap=4.0)
    # the gradient path back from V into Z: two opposing heads, as the reference
    out += rdotted(_spline([(881, 1025), (840, 1032), (800, 1048), (760, 1058), (700, 1060)]),
                   pen, dash=0.6, gap=1.5)
    out += rdotted([(700.0, DZ_Y), (874.0, DZ_Y)], pen, dash=0.6, gap=1.5)
    out += arrowhead(766.0, 1060.0, 0.0, 10.0, pen)
    out += arrowhead(832.0, 1060.0, 180.0, 10.0, pen)
    return out


# backward fans: (waypoints, arrowhead index along the spline, head angle)
DZ_FAN = [
    ([(512, 1030), (466, 1010), (414, 1002), (370, 1010), (340, 1026)], 180.0),
    ([(500, 1044), (452, 1024), (400, 1016), (356, 1024), (326, 1040)], 180.0),
    ([(486, 1056), (436, 1052), (392, 1058), (350, 1072), (322, 1086)], 175.0),
    ([(490, 1070), (440, 1082), (396, 1098), (356, 1118), (334, 1134)], 150.0),
    ([(500, 1080), (452, 1102), (410, 1126), (374, 1152), (352, 1170)], 140.0),
    ([(608, 1030), (654, 1010), (706, 1002), (750, 1010), (780, 1026)], 0.0),
    ([(620, 1044), (668, 1024), (720, 1016), (764, 1024), (794, 1040)], 0.0),
    ([(634, 1056), (684, 1052), (728, 1058), (770, 1072), (798, 1086)], 5.0),
    ([(630, 1070), (680, 1082), (724, 1098), (764, 1118), (786, 1134)], 30.0),
    ([(620, 1080), (668, 1102), (710, 1126), (746, 1152), (768, 1170)], 40.0),
]

DA_FAN = [
    ([(451, 1202), (436, 1176), (428, 1152), (424, 1132), (426, 1118)], -80.0),
    ([(470, 1200), (446, 1178), (430, 1160), (420, 1152)], 205.0),
    ([(478, 1232), (450, 1214), (430, 1198), (418, 1190)], 210.0),
    ([(492, 1252), (458, 1240), (432, 1224), (416, 1212)], 215.0),
    ([(672, 1202), (688, 1176), (696, 1152), (700, 1132), (698, 1118)], -100.0),
    ([(652, 1200), (676, 1178), (692, 1160), (702, 1152)], -25.0),
    ([(646, 1232), (674, 1214), (694, 1198), (706, 1190)], -30.0),
    ([(632, 1252), (666, 1240), (692, 1224), (708, 1212)], -35.0),
]

DQ_FAN = [
    ([(386, 1180), (322, 1152), (260, 1136), (204, 1132), (162, 1136)], 185.0),
    ([(392, 1200), (330, 1172), (270, 1152), (210, 1144), (166, 1144)], 185.0),
    ([(398, 1226), (340, 1196), (280, 1172), (230, 1158), (196, 1154)], 190.0),
    ([(392, 1252), (330, 1236), (266, 1208), (212, 1184), (172, 1178)], 200.0),
    ([(372, 1268), (318, 1264), (258, 1246), (208, 1220), (176, 1202)], 205.0),
    ([(360, 1282), (312, 1290), (256, 1288), (204, 1278), (168, 1268)], 195.0),
]


def backward_fans(colors_map) -> List[GCodeCommand]:
    green, black, red, blue, ochre = colors_map
    out: List[GCodeCommand] = []
    for way, ang in DZ_FAN:
        pts = _spline(way, n_per=28)
        out += rdotted(pts, green, dash=0.8, gap=1.5)
        out += arrowhead(pts[-1][0], pts[-1][1], ang, 10.0, green)
    for way, ang in DA_FAN:
        pts = _spline(way, n_per=28)
        out += rdotted(pts, black, dash=0.8, gap=1.5)
        out += arrowhead(pts[-1][0], pts[-1][1], ang, 10.0, black)
    for way, ang in DQ_FAN:
        pts = _spline(way, n_per=28)
        out += rdotted(pts, red, dash=0.8, gap=1.5)
        out += arrowhead(pts[-1][0], pts[-1][1], ang, 10.0, red)
        mway = [(_mirror(a), b) for a, b in way]
        mpts = _spline(mway, n_per=28)
        out += rdotted(mpts, blue, dash=0.8, gap=1.5)
        out += arrowhead(mpts[-1][0], mpts[-1][1], 180.0 - ang, 10.0, blue)
    # the long returns that climb out of the backward band into the forward half
    out += rdotted(_spline([(451, 1046), (420, 1010), (392, 970), (386, 930), (392, 900)]),
                   green, dash=0.8, gap=1.5)
    out += arrowhead(392.0, 894.0, -90.0, 10.0, green)
    out += rdotted(_spline([(672, 1046), (704, 1010), (730, 970), (736, 930), (730, 900)]),
                   green, dash=0.8, gap=1.5)
    out += arrowhead(730.0, 894.0, -80.0, 10.0, green)
    # blue / red long sweeps across the band
    out += rdotted(_spline([(700, 1046), (790, 1054), (872, 1078), (924, 1104), (952, 1132)]),
                   blue, dash=0.8, gap=1.5)
    out += arrowhead(952.0, 1132.0, 45.0, 10.0, blue)
    out += rdotted(_spline([(420, 1046), (330, 1054), (248, 1078), (196, 1104), (168, 1132)]),
                   red, dash=0.8, gap=1.5)
    out += arrowhead(168.0, 1132.0, 135.0, 10.0, red)
    return out


# ---------------------------------------------------------------------------


def attention_as_resonance(
    rng: SeededRNG, bounds: Bounds, colors: int = 5
) -> List[GCodeCommand]:
    _fit(bounds)

    def p(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    red, blue, ochre, green, black = (p(RED), p(BLUE), p(OCHRE), p(GREEN), p(BLACK))

    out: List[GCodeCommand] = []
    # frame
    out += frame_block(black)
    out += title_block(black)
    out += rails_block(black)
    # forward
    out += qk_block(red, False)
    out += qk_block(blue, True)
    out += fraction_block(black)
    out += fan(Q_FAN, red, endcap=4.0, dots=(0.70, 0.86))
    out += fan([[(_mirror(a), b) for a, b in way] for way in Q_FAN], blue,
               endcap=4.0, dots=(0.70, 0.86))
    out += interference(black, rng)
    out += softmax_block(black)
    out += fan(A_FAN, ochre)
    out += v_block(ochre)
    out += fan(V_FAN, ochre)
    out += fan(Z_FAN, ochre)
    out += z_block(green)
    # backward
    out += _dz_block(green)
    out += _da_block(black)
    out += _dqk_block(red, False)
    out += _dqk_block(blue, True)
    out += _dv_block(ochre)
    out += backward_fans((green, black, red, blue, ochre))
    return out
