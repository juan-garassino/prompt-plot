"""ORRERY — ATTENTION.  EXACT RECREATION of ``studio/orrery/ref/reference.png``.

This is a reproduction, not a design.  Every coordinate below is measured off
the reference bitmap (1122 x 1402) and kept in *reference pixel space* — x right,
y DOWN, origin top-left — then mapped once, aspect-preserving, into the drawable
area by ``_Map``.  Angles are given the intuitive way: ``A`` degrees CCW from
east with +90 pointing visually UP the sheet.

Pens: 0 red (Q) · 1 blue (K) · 2 ochre (V) · 3 green (Z) · 4 black (centre +
furniture).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import circle, fill_disc
from promptplot.generative.generators import _dot, _poly, _stroke_text
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

REF_W, REF_H = 1122.0, 1402.0
RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

CENTRE = (560.0, 588.0)
Q_HUB = (202.0, 392.0)
K_HUB = (914.0, 298.0)
V_HUB = (947.5, 844.6)
Z_HUB = (560.5, 1159.0)

Cmds = List[GCodeCommand]
Pt = Tuple[float, float]


# ---------------------------------------------------------------------------
# reference-pixel space -> mm
# ---------------------------------------------------------------------------


class _Map:
    def __init__(self, bounds: Tuple[float, float, float, float]) -> None:
        x0, y0, x1, y1 = bounds
        bw, bh = x1 - x0, y1 - y0
        ar = REF_H / REF_W
        w = min(bw, bh / ar)
        h = w * ar
        self.ox = x0 + (bw - w) / 2.0
        self.oy = y0 + (bh - h) / 2.0
        self.k = w / REF_W  # mm per reference pixel
        self.w, self.h = w, h

    def xy(self, p: Pt) -> Pt:
        return (self.ox + p[0] * self.k, self.oy + (REF_H - p[1]) * self.k)

    def d(self, px: float) -> float:
        return px * self.k


def pol(c: Pt, r: float, a_deg: float) -> Pt:
    """Point at radius ``r``, angle ``a_deg`` CCW-from-east with +90 = up."""
    a = math.radians(a_deg)
    return (c[0] + r * math.cos(a), c[1] - r * math.sin(a))


def _arc(c: Pt, r: float, a0: float, a1: float, n: int = 0) -> List[Pt]:
    n = n or max(24, int(abs(a1 - a0) * r / 900.0 * 8) + 24)
    return [pol(c, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def _bez(p0: Pt, c1: Pt, c2: Pt, p3: Pt, n: int = 64) -> List[Pt]:
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append(
            (
                u**3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t**3 * p3[0],
                u**3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t**3 * p3[1],
            )
        )
    return out


# ---------------------------------------------------------------------------
# strokes
# ---------------------------------------------------------------------------


def _line(m: _Map, pts: Sequence[Pt], pen: Optional[int], f: int = 2200) -> Cmds:
    return _poly([m.xy(p) for p in pts], color=pen, f=f)


DOTTED = ((2.8, True), (11.7, False))
FINE_DOT = ((2.2, True), (9.8, False))
DASHDOT = ((15.0, True), (6.5, False), (2.0, True), (6.5, False))
DASH = ((9.0, True), (7.0, False))


def _dashed(
    m: _Map,
    pts: Sequence[Pt],
    pen: Optional[int],
    pattern=DOTTED,
    phase: float = 0.0,
    f: int = 2200,
) -> Cmds:
    """Walk a reference-space polyline, emitting only the inked spans."""
    out: Cmds = []
    seg: List[Pt] = []
    idx, left = 0, pattern[0][0]
    # advance the pattern by `phase`
    ph = phase
    while ph > 0:
        step = min(ph, left)
        left -= step
        ph -= step
        if left <= 1e-9:
            idx = (idx + 1) % len(pattern)
            left = pattern[idx][0]
    ink = pattern[idx][1]
    if ink:
        seg = [pts[0]]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        seglen = math.hypot(b[0] - a[0], b[1] - a[1])
        t = 0.0
        while t < seglen - 1e-9:
            step = min(left, seglen - t)
            t0, t1 = t / seglen, (t + step) / seglen
            p1 = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if ink:
                if not seg:
                    seg = [(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)]
                seg.append(p1)
            t += step
            left -= step
            if left <= 1e-9:
                if ink and len(seg) >= 2:
                    out += _line(m, seg, pen, f)
                seg = []
                idx = (idx + 1) % len(pattern)
                left = pattern[idx][0]
                ink = pattern[idx][1]
    if ink and len(seg) >= 2:
        out += _line(m, seg, pen, f)
    return out


def ring(m: _Map, c: Pt, r: float, pen: Optional[int], dotted=False, f: int = 2200) -> Cmds:
    if dotted:
        return _dashed(m, _arc(c, r, 0, 360), pen, DOTTED, f=f)
    X, Y = m.xy(c)
    return circle(X, Y, m.d(r), pen=pen, n=max(56, int(m.d(r) * 4.5)), f=f)


def node(m: _Map, p: Pt, d_px: float, pen: Optional[int], hollow: bool = False) -> Cmds:
    """A plotted dot: one serpentine fill + a crisp rim.  Serpentine (not a
    spiral) keeps a 1.5 mm dot to ~20 points instead of ~60."""
    X, Y = m.xy(p)
    R = m.d(d_px) / 2.0
    if hollow:
        return circle(X, Y, R, pen=pen, n=22, f=1800)
    if R <= 0.40:
        return _dot(X, Y, r=max(0.16, R), color=pen)
    sp = 0.32
    rows = max(2, int(2 * R / sp))
    pts: List[Pt] = []
    for i in range(rows + 1):
        yy = -R + 2 * R * i / rows
        w = math.sqrt(max(0.0, R * R - yy * yy))
        if w < 0.05:
            continue
        row = [(X - w, Y + yy), (X + w, Y + yy)]
        pts.extend(reversed(row) if i % 2 else row)
    out = _poly(pts, color=pen, f=1600)
    out += circle(X, Y, R, pen=pen, n=max(14, int(R * 10)), f=1600)
    return out


def star(m: _Map, c: Pt, pen: Optional[int] = BLACK, up: float = 60.0, dn: float = 46.0) -> Cmds:
    """Six-pointed engraver's star: long vertical, short horizontal + diagonals,
    small open circle at the crossing."""
    r0, r1, r2 = 5.0, 16.0, 13.0
    out: Cmds = []
    out += _line(m, [pol(c, r0, 90), pol(c, up, 90)], pen)
    out += _line(m, [pol(c, r0, -90), pol(c, dn, -90)], pen)
    for a in (0, 180):
        out += _line(m, [pol(c, r0, a), pol(c, r1, a)], pen)
    for a in (35, 145, 215, 325):
        out += _line(m, [pol(c, r0, a), pol(c, r2, a)], pen)
    out += ring(m, c, r0, pen)
    return out


def moon(m: _Map, c: Pt, r: float, phase: float, pen: Optional[int] = BLACK) -> Cmds:
    """Moon-phase disc: outline, terminator, and 45-deg hatching in the shadow.

    ``phase`` in (-1, 1): sign picks the shaded side, |phase| the terminator bulge.
    """
    out: Cmds = ring(m, c, r, pen)
    k = phase * r
    term = [(c[0] + k * math.sin(math.radians(t)), c[1] - r * math.cos(math.radians(t)))
            for t in range(0, 181, 6)]
    out += _line(m, term, pen)
    lit_right = phase > 0

    def inside(p: Pt) -> bool:
        if (p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 > r * r:
            return False
        dy = (p[1] - c[1]) / r
        xt = c[0] + k * math.sqrt(max(0.0, 1.0 - dy * dy))
        return p[0] > xt if lit_right else p[0] < xt

    step = m.d(1.0) and 0.0  # placeholder, spacing set below in px
    sp = 0.82 / m.k  # 0.82 mm between hatch lines
    d = -2 * r
    while d <= 2 * r:
        a = (c[0] - r + d, c[1] - r)
        b = (c[0] + r + d, c[1] + r)
        run: List[Pt] = []
        n = 48
        for i in range(n + 1):
            p = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
            if inside(p):
                run.append(p)
            else:
                if len(run) >= 2:
                    out += _line(m, run, pen, f=1800)
                run = []
        if len(run) >= 2:
            out += _line(m, run, pen, f=1800)
        d += sp
    return out


def _caps(
    m: _Map,
    text: str,
    cx: float,
    baseline: float,
    cap: float,
    span: float,
    pen: Optional[int],
    f: int = 2000,
) -> Cmds:
    """Letter-spaced caps fitted to a target span (reference px)."""
    glyph = cap * 4.0 / 6.0
    n = len(text)
    adv = (span - glyph) / max(1, n - 1)
    out: Cmds = []
    x = cx - span / 2.0
    for ch in text:
        X, Y = m.xy((x, baseline))
        out += _stroke_text(ch, X, Y, m.d(cap), color=pen, f=f)
        x += adv
    return out


def _word(m: _Map, text: str, cx: float, baseline: float, cap: float,
          pen: Optional[int], track: float = 1.0, f: int = 2000) -> Cmds:
    """Natural-advance word, centred on ``cx``."""
    adv = 5.6 * cap / 6.0 * track
    w = adv * (len(text) - 1) + cap * 4.0 / 6.0
    out: Cmds = []
    x = cx - w / 2.0
    for ch in text:
        X, Y = m.xy((x, baseline))
        out += _stroke_text(ch, X, Y, m.d(cap), color=pen, f=f)
        x += adv
    return out


def _bundle(
    m: _Map,
    hub: Pt,
    ends: Sequence[Tuple[float, float]],
    hub_dirs: Sequence[float],
    end_dirs: Sequence[float],
    pen: Optional[int],
    centre: Pt,
    bow: Sequence[float],
    rng: SeededRNG,
    dots: int = 2,
    f: int = 2000,
) -> Cmds:
    """Fan of cubic arcs from a hub to a spread of endpoints on another system.

    ``ends`` are (radius, angle) about ``centre``.  ``hub_dirs``/``end_dirs`` are
    departure / arrival headings in degrees; ``bow`` scales the handle lengths.
    """
    out: Cmds = []
    for i, (r, a) in enumerate(ends):
        p3 = pol(centre, r, a)
        L = math.hypot(p3[0] - hub[0], p3[1] - hub[1])
        c1 = pol(hub, L * bow[i], hub_dirs[i])
        c2 = pol(p3, L * bow[i] * 0.85, end_dirs[i])
        pts = _bez(hub, c1, c2, p3, 56)
        out += _line(m, pts, pen, f)
        for _ in range(dots):
            t = rng.uniform(0.18, 0.86)
            j = int(t * 56)
            out += node(m, pts[j], rng.uniform(4.0, 11.0), pen)
        out += node(m, p3, rng.uniform(6.0, 10.0), pen)
    return out


# ---------------------------------------------------------------------------
# the four planetary systems
# ---------------------------------------------------------------------------


def _system(
    m: _Map,
    hub: Pt,
    hub_r: float,
    radii: Sequence[float],
    ecc: Sequence[float],
    nodes: Sequence[Tuple[float, float, float]],
    pen: Optional[int],
    axis: Tuple[float, float],
    axis_dots: Tuple[float, float],
    dot_orbit: Optional[Tuple[float, float, float]] = None,
    hollow: Sequence[Tuple[float, float, float]] = (),
    rosette: Sequence[float] = (),
) -> Cmds:
    out: Cmds = []
    # faint inner rosette
    for r in rosette:
        out += _line(m, _arc(hub, r, 35, 325), pen, f=2400)
        out += _line(m, _arc(hub, r * 0.72, -20, 200), pen, f=2400)
    # orbits (mildly eccentric, drifting with radius — as in the reference)
    for r, e in zip(radii, ecc):
        out += ring(m, (hub[0] + e, hub[1]), r, pen)
    # vertical axis with its terminal dots, then the fine tail below
    out += _line(m, [(hub[0], axis[0]), (hub[0], axis[1])], pen, f=2400)
    out += node(m, (hub[0], axis_dots[0]), 8.5, pen)
    out += node(m, (hub[0], axis_dots[1]), 8.5, pen)
    if dot_orbit:
        r, a0, a1 = dot_orbit
        out += _dashed(m, _arc(hub, r, a0, a1), pen, DOTTED)
    for r, a, d in nodes:
        out += node(m, pol(hub, r, a), d, pen)
    for r, a, d in hollow:
        out += node(m, pol(hub, r, a), d, pen, hollow=True)
    # hub last so it sits on top of the fan
    out += node(m, hub, hub_r * 2, pen)
    return out


# ---------------------------------------------------------------------------
# piece
# ---------------------------------------------------------------------------


def orrery_attention(rng: SeededRNG, bounds, colors: int = 5) -> Cmds:
    m = _Map(bounds)

    def P(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    red, blue, ochre, green, black = P(RED), P(BLUE), P(OCHRE), P(GREEN), P(BLACK)
    out: Cmds = []

    # ---------------- furniture: corners, title, enclosing circle -----------
    for cx, cy in ((50.0, 39.0), (1070.0, 39.0)):
        out += _line(m, [(cx - 15, cy), (cx + 15, cy)], black)
        out += _line(m, [(cx, cy - 15), (cx, cy + 15)], black)
    for cx, cy in ((51.5, 1355.0), (1071.5, 1355.0)):
        out += _line(m, [(cx - 39, cy), (cx + 39, cy)], black)
        out += _line(m, [(cx, cy - 61), (cx, cy + 32)], black)
        out += ring(m, (cx, cy), 9.0, black)
    # bottom-centre diamond
    dx, dy, dr = 561.0, 1352.0, 12.0
    out += _line(m, [(dx, dy - dr), (dx + dr, dy), (dx, dy + dr), (dx - dr, dy), (dx, dy - dr)], black)
    out += _line(m, [(dx - 17, dy), (dx + 17, dy)], black)
    out += _line(m, [(dx, dy - 17), (dx, dy + 17)], black)

    out += _caps(m, "ATTENTION", 561.0, 56.0, 29.0, 359.0, black)
    out += _line(m, [(501.0, 89.0), (554.0, 89.0)], black)
    out += _line(m, [(568.0, 89.0), (621.0, 89.0)], black)
    out += ring(m, (561.0, 89.0), 7.0, black)
    out += _line(m, [(561.0, 79.0), (561.0, 99.0)], black)

    out += _dashed(m, _arc((575.6, 690.8), 504.9, 0, 360), black, DOTTED)
    out += _dashed(m, _arc(CENTRE, 340.0, -62, 242), black, DOTTED)
    out += _dashed(m, _arc(CENTRE, 353.0, 118, 242), black, FINE_DOT)

    out += _dashed(m, _arc((300.0, 700.0), 330.0, 20.0, 96.0), black, FINE_DOT)
    out += _dashed(m, _arc((820.0, 720.0), 330.0, 84.0, 168.0), black, FINE_DOT)
    out += _dashed(m, _arc((560.0, 300.0), 330.0, 200.0, 340.0), black, FINE_DOT)
    for fx, fy, fd in (
        (239.0, 1057.0, 6.0), (213.0, 757.0, 5.0), (293.0, 812.0, 4.0), (300.0, 448.0, 4.0),
        (688.0, 268.0, 4.5), (1020.0, 470.0, 4.0), (884.0, 1128.0, 5.0), (392.0, 1063.0, 4.0),
        (742.0, 1006.0, 4.5), (390.0, 305.0, 4.0),
    ):
        out += node(m, (fx, fy), fd, black)

    # long sight line from the lower-left moon up into the centre system
    out += _dashed(m, [(157.0, 889.0), (455.0, 710.0)], black, DASHDOT)
    out += node(m, (157.0, 889.0), 8.0, black)

    # moon-phase discs
    out += moon(m, (69.5, 719.0), 18.0, -0.30, black)
    out += moon(m, (118.0, 903.0), 22.0, 0.42, black)
    out += _dashed(m, _arc((118.0, 906.0), 44.0, 0, 360), black, DOTTED)
    out += moon(m, (805.0, 944.0), 11.0, 0.35, black)

    # stars
    out += star(m, (202.0, 209.0), black, up=44, dn=40)
    out += star(m, (915.0, 105.0), black, up=52, dn=46)
    out += star(m, (970.0, 677.0), black, up=44, dn=36)
    out += star(m, (947.0, 1238.0), black, up=86, dn=46)
    out += node(m, (947.0, 1152.0), 9.0, black)

    # lone open circle east of K, on the enclosing circle
    out += ring(m, (1057.0, 246.0), 13.0, black)
    out += ring(m, (567.0, 275.0), 9.0, black)

    # ---------------- plate axes -------------------------------------------
    out += _dashed(m, [(560.0, 160.0), (560.0, 528.0)], black, FINE_DOT)
    out += _dashed(m, [(560.0, 648.0), (560.0, 1055.0)], black, FINE_DOT)
    out += _dashed(m, [(560.5, 1262.0), (560.5, 1336.0)], black, FINE_DOT)
    out += _dashed(m, [(120.0, 588.0), (500.0, 588.0)], black, DASHDOT)
    out += _dashed(m, [(622.0, 588.0), (1002.0, 588.0)], black, DASHDOT)
    for x in (140.0, 208.0, 914.0, 986.0):
        out += node(m, (x, 588.0), 7.0, black)
    # the reference's row of nodes where the axis crosses the central orbits
    for rr, dd in ((110.0, 6.0), (140.0, 5.0), (178.0, 7.5), (208.0, 6.0), (241.0, 5.0)):
        out += node(m, (CENTRE[0] - rr, 588.0), dd, black)
        out += node(m, (CENTRE[0] + rr, 588.0), dd, black)
    out += moon(m, (324.0, 587.0), 8.0, -0.9, black)
    out += moon(m, (796.0, 587.0), 8.0, 0.9, black)

    # ---------------- the central system -----------------------------------
    rings_c = [
        (68.0, True), (78.0, True), (92.0, False), (110.0, False), (124.0, False), (132.0, True),
        (140.0, False), (150.0, True), (161.0, False), (170.0, True), (178.0, False),
        (190.0, True), (199.0, False), (208.0, False), (218.0, True), (231.0, False),
        (241.0, False),
    ]
    for i, (r, dot) in enumerate(rings_c):
        ex = rng.uniform(-5.0, 4.0) * (r / 241.0)
        ey = rng.uniform(-4.5, 4.5) * (r / 241.0)
        out += ring(m, (CENTRE[0] + ex, CENTRE[1] + ey), r, black, dotted=dot)

    # the one visibly heavy orbit — a second pass on the SAME path (no crowding)
    out += ring(m, CENTRE, 208.0, black)

    solid = [r for r, d in rings_c if not d]
    placed: List[Pt] = []
    for r in solid:
        # the reference thins the node field toward the middle and crowds the rim
        k = 2 + int(round(6.0 * (r - 92.0) / 149.0))
        for _ in range(rng.randint(max(2, k - 1), k + 2)):
            a = rng.uniform(0, 360)
            p = pol(CENTRE, r, a)
            if any(math.hypot(p[0] - q[0], p[1] - q[1]) < 15.0 for q in placed):
                continue
            placed.append(p)
            d = rng.choice([3.0, 3.5, 4.5, 5.0, 6.0, 7.0, 8.5, 10.0, 12.0, 15.0])
            out += node(m, p, d, black)
    for _ in range(5):
        r = rng.choice(solid)
        out += node(m, pol(CENTRE, r, rng.uniform(0, 360)), 9.0, black, hollow=True)
    # three short constellation links between neighbouring nodes
    for _ in range(3):
        i = rng.randint(0, len(placed) - 3)
        a, b = placed[i], placed[i + 1]
        if math.hypot(a[0] - b[0], a[1] - b[1]) < 90:
            out += _line(m, [a, ((a[0] + b[0]) / 2 + 6, (a[1] + b[1]) / 2 - 6), b], black)
    out += node(m, (559.0, 383.0), 15.0, black)

    # centre legend
    out += _word(m, "Q", 518.0, 568.0, 30.0, black, track=1.0)
    out += node(m, (546.0, 558.0), 4.5, black)
    out += _word(m, "K", 574.0, 568.0, 30.0, black, track=1.0)
    out += _word(m, "T", 597.0, 552.0, 14.0, black, track=1.0)
    out += _line(m, [(497.0, 588.0), (551.0, 588.0)], black)
    out += _line(m, [(569.0, 588.0), (623.0, 588.0)], black)
    out += ring(m, (560.0, 588.0), 8.0, black)
    out += _caps(m, "SOFTMAX", 560.0, 634.0, 16.0, 96.0, black)

    # ---------------- Q (red, upper left) ----------------------------------
    q_nodes = [
        (102.0, 164.9, 12.0), (113.0, 9.4, 10.0), (64.4, 131.9, 9.0), (83.2, 191.4, 10.0),
        (57.9, 39.0, 9.0), (65.3, 217.2, 7.0), (85.1, 303.5, 7.0), (93.0, 45.7, 5.0),
        (104.0, 223.8, 5.0), (84.3, 311.2, 4.0),
    ]
    out += _system(
        m, Q_HUB, 13.0,
        [29.0, 45.5, 62.0, 79.5, 102.0], [-1.5, -3.0, -4.0, -4.5, -5.0],
        q_nodes, red,
        axis=(281.0, 501.0), axis_dots=(281.0, 501.0),
        hollow=[(83.0, 123.7, 10.0)],
        rosette=[20.0],
    )
    out += _line(m, [(202.0, 501.0), (202.0, 588.0)], black, f=2400)
    out += _dashed(m, [(202.0, 281.0), (202.0, 222.0)], red, FINE_DOT)
    # Q's outlying dotted orbit, lower left
    out += _dashed(m, _bez((96.0, 424.0), (98.0, 470.0), (118.0, 530.0), (142.0, 554.0), 40),
                   red, DOTTED)
    out += node(m, (142.0, 554.0), 9.0, red)
    out += _word(m, "Q", 144.0, 276.0, 32.0, red)

    # ---------------- K (blue, upper right) --------------------------------
    k_nodes = [
        (102.5, -89.4, 11.0), (123.0, 140.9, 10.0), (79.6, -2.5, 10.0), (63.9, 55.2, 8.0),
        (63.2, 188.6, 8.0), (98.5, 228.3, 8.0), (126.8, 183.8, 6.0), (140.5, 89.6, 5.0),
        (61.8, 216.8, 6.0), (62.1, 232.9, 4.0), (121.6, 216.3, 3.5),
    ]
    out += _system(
        m, K_HUB, 13.5,
        [24.0, 43.0, 64.0, 86.0, 108.0], [-1.5, -3.0, -4.5, -5.5, -6.0],
        k_nodes, blue,
        axis=(158.0, 400.0), axis_dots=(158.0, 400.0),
        dot_orbit=(140.0, -118.0, 160.0),
        hollow=[(91.8, 69.6, 10.0)],
        rosette=[17.0],
    )
    out += _dashed(m, [(914.0, 158.0), (914.0, 78.0)], blue, FINE_DOT)
    out += _dashed(m, [(914.0, 400.0), (914.0, 462.0)], blue, FINE_DOT)
    out += _word(m, "K", 1038.0, 350.0, 30.0, blue)

    # ---------------- V (ochre, lower right) -------------------------------
    v_nodes = [
        (110.1, 174.3, 14.0), (92.3, -14.1, 12.0), (105.0, 90.3, 12.0), (81.1, 182.8, 11.0),
        (58.9, 220.2, 9.0), (122.5, -90.5, 7.0), (135.0, 90.2, 6.0), (97.6, 49.8, 5.0),
        (60.1, 135.7, 5.0), (80.4, 48.3, 4.0), (80.5, 271.1, 4.0),
    ]
    out += _system(
        m, V_HUB, 13.0,
        [27.0, 43.0, 58.5, 80.5, 104.0], [0.0, -1.0, -2.0, -3.0, -4.0],
        v_nodes, ochre,
        axis=(710.0, 1016.0), axis_dots=(710.0, 967.0),
        dot_orbit=(134.0, 20.0, 250.0),
        hollow=[(46.0, 96.0, 10.0), (62.0, 128.0, 8.0)],
        rosette=[18.0],
    )
    out += _word(m, "V", 1054.0, 812.0, 30.0, ochre)

    # ---------------- Z (green, bottom) ------------------------------------
    z_nodes = [(75.0, a, 7.0) for a in range(0, 360, 45)]
    out += _system(
        m, Z_HUB, 13.0,
        [25.0, 38.5, 50.0, 75.0], [0.0, 0.0, 0.0, 0.0],
        z_nodes, green,
        axis=(1084.0, 1234.0), axis_dots=(1084.0, 1234.0),
        dot_orbit=(95.0, 0.0, 360.0),
        rosette=[],
    )
    out += _line(m, [(442.0, 1157.0), (474.0, 1157.0)], black)
    out += _line(m, [(648.0, 1157.0), (680.0, 1157.0)], black)
    out += _word(m, "Z = AV", 560.0, 1299.0, 27.0, green, track=0.92)

    # ---------------- connector bundles ------------------------------------
    out += _bundle(
        m, Q_HUB,
        [(244.0, 127.0), (216.0, 140.0), (197.0, 152.0), (191.0, 162.0), (238.0, 171.0)],
        [14.0, -2.0, -18.0, -36.0, -54.0],
        [148.0, 156.0, 166.0, 176.0, 190.0],
        red, CENTRE,
        [0.46, 0.38, 0.34, 0.36, 0.44], rng, dots=2,
    )
    out += _bundle(
        m, K_HUB,
        [(250.0, 68.0), (229.0, 56.0), (212.0, 45.0), (205.0, 34.0), (221.0, 23.0), (245.0, 12.0)],
        [188.0, 201.0, 214.0, 227.0, 240.0, 252.0],
        [34.0, 25.0, 15.0, 4.0, -7.0, -19.0],
        blue, CENTRE,
        [0.42, 0.38, 0.35, 0.35, 0.38, 0.44], rng, dots=2,
    )
    out += _bundle(
        m, V_HUB,
        [(244.0, -20.0), (223.0, -31.0), (207.0, -42.0), (205.0, -53.0), (228.0, -64.0)],
        [130.0, 139.0, 148.0, 159.0, 172.0],
        [-52.0, -44.0, -36.0, -26.0, -14.0],
        ochre, CENTRE,
        [0.36, 0.33, 0.31, 0.33, 0.38], rng, dots=2,
    )
    # centre -> Z : sources on the centre's lower rings, long parallel waist
    for i, (r, a) in enumerate(
        [(241.0, 222.0), (231.0, 241.0), (208.0, 262.0), (219.0, 283.0), (242.0, 302.0)]
    ):
        p0 = pol(CENTRE, r, a)
        off = (i - 2) * 8.0
        c1 = (p0[0] * 0.32 + (Z_HUB[0] + off * 1.8) * 0.68, p0[1] + 150.0)
        c2 = (Z_HUB[0] + off * 2.0, Z_HUB[1] - 215.0)
        pts = _bez(p0, c1, c2, Z_HUB, 72)
        out += _line(m, pts, green, f=2000)
        for _ in range(2):
            out += node(m, pts[int(rng.uniform(0.25, 0.85) * 72)], rng.uniform(5.0, 11.0), green)
        out += node(m, p0, 8.0, green)

    return out
