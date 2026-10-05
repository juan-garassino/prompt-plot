"""ATTENTION AS RESONANCE — exact recreation of studio/resonance-clean/ref/reference.png.

Reproduction, not design. Every coordinate below is measured off the reference
raster (1122 x 1402 px) and mapped through one uniform fit, so the layout is
carried verbatim; only the mark-making is translated into pen strokes.

The hero (the two-source interference figure) is the APPROVED construction from
the sibling plate studio/resonance/rounds/r01/piece.py :: _interference, ported
verbatim: Huygens crest ridges r_s = m*L with d = 35*L, plus its crossing-safe
anti-crowding guard. Do not reinvent it.

Pens (render palette crimson,dodgerblue,goldenrod,forestgreen,black):
    0 red · 1 blue · 2 ochre · 3 green · 4 black
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import _dot, _poly, circle, fill_disc, giant_type
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

# --- reference frame -------------------------------------------------------
# content box measured on the reference png
REF_X0, REF_Y0, REF_X1, REF_Y1 = 45.0, 25.0, 1085.0, 1340.0

_S = 1.0  # mm per reference px  (set by _fit)
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
# mark-making primitives (all arguments in REFERENCE px unless noted)
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
    return fill_disc(x, y, r, spacing=0.3, pen=pen)


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
    step = 0.22
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


def _spline(way: Sequence[Pt], n_per: int = 46) -> List[Pt]:
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


# ---------------------------------------------------------------------------
# THE wave-packet helper — carrier x gaussian envelope on an axis.
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
    step = max(0.35, tmin / 13.0)
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


def tracked_type(
    text: str,
    cx: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    track: float = 1.33,
    weight: float = 0.0,
) -> List[GCodeCommand]:
    """Centred display caps with reference letter-spacing (cap heights in ref px)."""
    h = L(cap)
    adv = h * track
    chars = [c for c in text]
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
# blocks
# ---------------------------------------------------------------------------

CENTRE = 557.0


def _mirror(x: float) -> float:
    return 2 * CENTRE - x


def title_block(pen: int) -> List[GCodeCommand]:
    out = tracked_type("ATTENTION AS RESONANCE", 546.0, 50.0, 19.0, pen, track=1.34, weight=0.0)
    out += rpoly([(490, 74), (616, 74)], pen)
    out += rdisc(557, 74, 3.4, pen)
    return out


# each row: (y, axis_x0, axis_x1, left_filled, right_x, right_filled, lobes, ghost_lobes)
Q_ROWS = [
    (
        163.0, 107.0, 287.0, False, 287.0, False,
        [(222.0, 30.0, 47.0, 19.5, 0.0), (168.0, 12.0, 7.0, 9.9, 1.1)],
        [(228.0, 26.0, 34.0, 29.8, 2.0)],
    ),
    (
        222.0, 107.0, 357.0, True, 357.0, True,
        [(190.0, 21.0, 30.0, 10.9, 0.4), (322.0, 15.0, 20.0, 15.6, 2.2)],
        [],
    ),
    (
        281.0, 107.0, 390.0, False, 390.0, False,
        [(252.0, 31.0, 34.0, 21.9, 0.7), (196.0, 16.0, 11.0, 12.8, 0.2),
         (325.0, 14.0, 9.0, 11.4, 1.5)],
        [(238.0, 24.0, 22.0, 15.6, 2.6)],
    ),
    (
        340.0, 107.0, 353.0, True, 353.0, False,
        [(191.0, 25.0, 29.0, 14.5, 0.9), (330.0, 12.0, 13.0, 11.9, 0.3)],
        [],
    ),
    (
        397.0, 107.0, 327.0, False, 327.0, False,
        [(232.0, 30.0, 41.0, 12.2, 0.5), (170.0, 12.0, 6.0, 9.2, 2.0)],
        [(236.0, 27.0, 26.0, 18.5, 1.2)],
    ),
]

Q_VERTS = [(107.0, 145.0, 432.0), (208.0, 95.0, 470.0), (287.0, 112.0, 420.0), (358.0, 185.0, 412.0)]


def qk_block(pen: int, mirror: bool, rng: SeededRNG) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []

    def mx(x: float) -> float:
        return _mirror(x) if mirror else x

    for y, ax0, ax1, lfill, rx, rfill, lobes, ghosts in Q_ROWS:
        # trailing dots off the far side
        out += rdot_run([mx(v) for v in (57.0, 69.0, 81.0, 92.0)], y, 2.3, pen)
        # axis
        out += rpoly([(mx(ax0), y), (mx(ax1), y)], pen)
        # nodes
        out += node(mx(ax0), y, 5.7, lfill, pen)
        out += node(mx(rx), y, 5.7, rfill, pen)
        # packets
        xa = mx(min(l[0] - 3.1 * l[1] for l in lobes))
        xb = mx(max(l[0] + 3.1 * l[1] for l in lobes))
        mlobes = [(mx(c), s, a, p, ph) for c, s, a, p, ph in lobes]
        out += draw_packet(y, min(xa, xb), max(xa, xb), mlobes, pen)
        if ghosts:
            gl = [(mx(c), s, a, p, ph) for c, s, a, p, ph in ghosts]
            gxa = mx(min(l[0] - 3.0 * l[1] for l in ghosts))
            gxb = mx(max(l[0] + 3.0 * l[1] for l in ghosts))
            gw, _, _ = packet_curves(y, min(gxa, gxb), max(gxa, gxb), gl)
            out += rdotted(gw, pen, dash=0.45, gap=0.95)

    for x, y0, y1 in Q_VERTS:
        out += rdotted([(mx(x), y0), (mx(x), y1)], pen, dash=0.5, gap=1.25)

    # the serif letter
    if mirror:
        out += left_type("K", 984.0, 128.0, 33.0, pen, track=1.1, weight=0.38)
    else:
        out += left_type("Q", 100.0, 128.0, 33.0, pen, track=1.1, weight=0.38)
    return out


def fraction_block(pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    cap = 26.0
    h = L(cap)
    # numerator  Q · K^T
    x, y = P(514.0, 390.0)
    out += giant_type("Q", x, y, h, pen=pen, weight=0.2, tip=0.26)
    out += rdisc(548.0, 381.0, 2.6, pen)
    x2, _ = P(560.0, 390.0)
    out += giant_type("K", x2, y, h, pen=pen, weight=0.2, tip=0.26)
    x3, y3 = P(586.0, 375.0)
    out += giant_type("T", x3, y3, h * 0.62, pen=pen, weight=0.12, tip=0.26)
    # rule
    out += rpoly([(508, 409), (601, 409)], pen)
    # denominator  sqrt(d_k)
    out += radical(516.0, 441.0, 24.0, 42.0, pen)
    xd, yd = P(534.0, 441.0)
    out += giant_type("d", xd, yd, L(20.0), pen=pen, weight=0.16, tip=0.26)
    xk, yk = P(552.0, 447.0)
    out += giant_type("k", xk, yk, L(13.0), pen=pen, weight=0.1, tip=0.26)
    return out


# ---------------------------------------------------------------------------
# THE HERO — two-source interference.
# Construction ported verbatim from the APPROVED sibling plate,
# studio/resonance/rounds/r01/piece.py :: _interference (Huygens crest ridges).
# ---------------------------------------------------------------------------

IF_CX, IF_CY = 561.0, 611.0
IF_D = 250.0
SRC_L, SRC_R = IF_CX - IF_D / 2, IF_CX + IF_D / 2


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

    n_lam = 35
    lam = IF_D / n_lam
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
        run: List[Pt] = []
        for j, (px, py) in enumerate(pts):
            ok = ((px - IF_CX) / aa) ** 2 + ((py - IF_CY) / bb) ** 2 <= 1.0
            if ok and keep_out is not None:
                ox, oy, orr = keep_out
                ok = math.hypot(px - ox, py - oy) > orr
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
                    res += (rdotted(run, bk, dash=0.42, gap=1.8) if dotted
                            else rpoly(run, bk, f=2600))
                run = []
        if len(run) >= 4:
            res += (rdotted(run, bk, dash=0.42, gap=1.8) if dotted
                    else rpoly(run, bk, f=2600))
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
                  if _BX0 + 2 < P(*q)[0] < _BX1 - 2
                  and min(math.hypot(q[0] - SRC_L, q[1] - IF_CY),
                          math.hypot(q[0] - SRC_R, q[1] - IF_CY)) > 21 * lam + 8.0]
            if len(rr) > 6:
                out += rdotted(rr, bk, dash=0.42, gap=1.9)

    # --- the horizontal axis through the figure ---------------------------
    out += rpoly([(300.0, IF_CY), (822.0, IF_CY)], bk)
    for sgn in (1, -1):
        base = IF_CX - sgn * 334.0
        out += rcircle(base, IF_CY, 5.0, bk, n=40)
        for j in range(4):
            out += rdisc(base - sgn * (17.0 + 17.0 * j), IF_CY, 2.3, bk)
        out += rdisc(IF_CX - sgn * 305.0, IF_CY, 3.2, bk)
        out += rdisc(IF_CX - sgn * 266.0, IF_CY, 3.4, bk)
        cxx = IF_CX - sgn * 203.0
        out += rcircle(cxx, IF_CY, 6.2, bk, n=40)
        out += rdisc(cxx, IF_CY, 2.2, bk)
    out += rdisc(IF_CX, IF_CY, 5.0, bk)
    out += rdisc(SRC_L, IF_CY, 4.8, bk)
    out += rdisc(SRC_R, IF_CY, 4.8, bk)

    # --- the dot field ----------------------------------------------------
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
        out += rdotted([(x, top), (x, IF_CY - 6.0)], bk, dash=0.5, gap=1.7)
        out += rdisc(x, top - 8.0, 2.0, bk)
        bot = 866.0 if j % 2 == 0 else 806.0
        out += rdotted([(x, IF_CY + 6.0), (x, bot)], bk, dash=0.5, gap=1.7)
    out += rcircle(IF_CX, 486.0, 4.8, bk, n=32)
    out += rcircle(IF_CX, 716.0, 4.8, bk, n=32)

    # the central spine, above the figure and on down through softmax, V and Z
    out += rdotted([(IF_CX, 330.0), (IF_CX, 452.0)], bk, dash=0.6, gap=1.5)
    out += rdotted([(IF_CX, 900.0), (IF_CX, 1345.0)], bk, dash=0.6, gap=1.5)
    return out


SOFT_Y = 893.0
SOFT_PEAKS = [
    (392.0, 45.0, 5.2, "open"),
    (476.0, 86.0, 5.6, "fill"),
    (517.0, 31.0, 4.2, None),
    (561.0, 62.0, 5.2, "fill"),
    (609.0, 20.0, 4.0, None),
    (646.0, 87.0, 5.6, "open"),
    (726.0, 42.0, 5.4, "open"),
]
SOFT_BASE_NODES = [
    (321.0, "dot"), (392.0, "dot"), (434.0, "open"), (476.0, "open"), (517.0, "dot"),
    (561.0, "open"), (609.0, "open"), (646.0, "open"), (686.0, "open"), (726.0, "dot"),
    (801.0, "dot"),
]


def _soft_y(x: float) -> float:
    v = 0.0
    for c, h, w, _m in SOFT_PEAKS:
        v += h / (1.0 + ((x - c) / w) ** 2) ** 1.5
    return SOFT_Y - v


def softmax_block(pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += rpoly([(321, SOFT_Y), (801, SOFT_Y)], pen)
    out += rdot_run([269, 283, 297, 311], SOFT_Y, 2.3, pen)
    out += rdot_run([812, 826, 840, 854], SOFT_Y, 2.3, pen)

    curve = []
    n = 900
    for i in range(n + 1):
        x = 321.0 + (801.0 - 321.0) * i / n
        curve.append((x, _soft_y(x)))
    out += rpoly(curve, pen, f=1800)

    # ghost distribution (fainter, dotted)
    ghost = []
    for i in range(500):
        x = 340.0 + (790.0 - 340.0) * i / 499
        v = 0.0
        for c, h in ((434.0, 22.0), (517.0, 18.0), (609.0, 26.0), (686.0, 20.0), (726.0, 14.0)):
            v += h / (1.0 + ((x - c) / 6.5) ** 2) ** 1.5
        ghost.append((x, SOFT_Y - v))
    out += rdotted(ghost, pen, dash=0.4, gap=1.5)

    for c, h, _w, mark in SOFT_PEAKS:
        if mark:
            out += rpoly([(c, SOFT_Y), (c, SOFT_Y - h + 5.0)], pen)
            out += node(c, SOFT_Y - h - 2.0, 5.6, mark == "fill", pen)
    for x, kind in SOFT_BASE_NODES:
        if kind == "open":
            out += rcircle(x, SOFT_Y, 5.6, pen, n=30)
        else:
            out += rdisc(x, SOFT_Y, 3.0, pen)

    out += tracked_type("softmax", 562.0, 782.0, 18.0, pen, track=0.80, weight=0.0)
    return out


V_ROWS = [
    (976.0, [(870.0, 38.0, 37.0, 12.7, 0.2)], True, False),
    (1017.0, [(800.0, 27.0, 31.0, 12.6, 1.1)], False, False),
    (1062.0, [(898.0, 30.0, 31.0, 25.5, 0.6), (840.0, 18.0, 14.0, 16.1, 2.0)], False, False),
    (1106.0, [(830.0, 31.0, 33.0, 13.5, 0.9)], False, True),
    (1150.0, [(912.0, 30.0, 35.0, 10.9, 0.4)], False, False),
]


def v_block(pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for y, lobes, big_left, right_fill in V_ROWS:
        out += rpoly([(726, y), (1018, y)], pen)
        out += rdot(702, y, 2.4, pen)
        out += node(726, y, 6.4 if big_left else 5.7, big_left, pen)
        out += node(993, y, 5.7, right_fill, pen)
        out += rdot_run([1037, 1048, 1059, 1070], y, 2.3, pen)
        xa = min(l[0] - 3.1 * l[1] for l in lobes)
        xb = max(l[0] + 3.1 * l[1] for l in lobes)
        out += draw_packet(y, xa, xb, lobes, pen)
    for x in (726.0, 993.0):
        out += rdotted([(x, 950), (x, 1172)], pen, dash=0.5, gap=1.25)
    out += left_type("V", 1020.0, 953.0, 30.0, pen, track=1.1, weight=0.38)
    return out


Z_Y = 1288.0
Z_LOBES = [
    (561.0, 58.0, 80.0, 15.3, 0.0),
    (470.0, 30.0, 16.0, 12.4, 1.3),
    (655.0, 30.0, 16.0, 12.4, 2.4),
    (397.0, 26.0, 12.0, 9.7, 0.6),
    (724.0, 26.0, 12.0, 9.7, 2.9),
]


def z_block(pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += rpoly([(221, Z_Y), (901, Z_Y)], pen)
    out += rdot_run([152, 173, 191, 209], Z_Y, 2.6, pen)
    out += rdot_run([925, 949, 973], Z_Y, 2.6, pen)
    out += draw_packet(Z_Y, 350.0, 775.0, Z_LOBES, pen, env_floor=3.0)

    # a second, narrower envelope inside
    _, up2, dn2 = packet_curves(Z_Y, 360.0, 765.0, [(561.0, 40.0, 52.0, 11.1, 0.0)])
    for run in _trim(up2, Z_Y, 4.0) + _trim(dn2, Z_Y, 4.0):
        out += rdotted(run, pen, dash=0.85, gap=1.05)

    out += rdisc(221, Z_Y, 4.2, pen)
    out += rdisc(901, Z_Y, 4.2, pen)
    for x in (317.0, 561.0, 804.0):
        out += rcircle(x, Z_Y, 6.4, pen, n=32)
    # the two side "eyes"
    for x in (397.0, 724.0):
        for a, b in ((10.0, 17.0), (4.6, 7.8)):
            ring = [
                (x + a * math.cos(2 * math.pi * i / 64), Z_Y + b * math.sin(2 * math.pi * i / 64))
                for i in range(65)
            ]
            out += rpoly(ring, pen)
        out += rpoly([(x, Z_Y - 21), (x, Z_Y + 21)], pen)
    out += rdisc(561, 1181, 5.0, pen)
    out += left_type("Z = AV", 355.0, 1208.0, 33.0, pen, track=1.02, weight=0.38)
    return out


# ---------------------------------------------------------------------------
# convergence fans
# ---------------------------------------------------------------------------

# each entry is a waypoint list (reference px) -> Catmull-Rom spline
Q_FAN = [
    [(298, 164), (400, 168), (476, 214), (508, 300), (493, 386), (466, 440)],
    [(360, 224), (446, 234), (498, 296), (508, 374), (478, 440), (452, 476)],
    [(392, 283), (466, 296), (500, 360), (492, 434), (452, 486), (428, 502)],
    [(356, 342), (440, 360), (468, 424), (444, 482), (404, 518), (380, 532)],
    [(330, 399), (400, 418), (420, 470), (398, 510), (368, 534), (354, 542)],
    [(268, 410), (300, 452), (296, 484), (316, 506), (338, 520), (350, 528)],
    [(196, 420), (206, 452), (238, 476), (278, 494), (308, 502), (322, 506)],
    [(156, 452), (188, 470), (228, 486), (268, 498), (300, 504), (314, 506)],
]

V_FAN = [
    [(392, 900), (398, 1006), (436, 1092), (532, 1140), (652, 1152), (708, 1154)],
    [(434, 900), (440, 1000), (478, 1080), (568, 1122), (668, 1132), (712, 1132)],
    [(476, 900), (482, 992), (520, 1062), (606, 1098), (682, 1104), (712, 1104)],
    [(517, 900), (523, 982), (558, 1042), (632, 1066), (692, 1066), (714, 1064)],
    [(561, 900), (566, 970), (598, 1018), (658, 1032), (700, 1026), (716, 1022)],
    [(609, 900), (613, 958), (640, 996), (684, 1002), (712, 994), (722, 990)],
    [(646, 900), (649, 946), (668, 974), (700, 978), (720, 972), (728, 968)],
]

Z_FAN = [
    [(756, 1166), (742, 1196), (706, 1216), (654, 1228), (606, 1232), (586, 1232)],
    [(818, 1170), (798, 1206), (756, 1230), (696, 1244), (648, 1248), (628, 1248)],
    [(880, 1174), (856, 1214), (810, 1242), (744, 1258), (690, 1262), (668, 1262)],
    [(942, 1178), (914, 1222), (862, 1254), (792, 1272), (734, 1276), (710, 1276)],
    [(992, 1184), (964, 1232), (908, 1266), (838, 1284), (780, 1288), (756, 1288)],
    [(1006, 1152), (996, 1190), (956, 1222), (896, 1244), (846, 1252), (824, 1254)],
]


def fan(ways, pen: int, endcap: float = 0.0, dots: Sequence[float] = ()) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for way in ways:
        pts = _spline(way, n_per=34)
        out += rdotted(pts, pen, dash=0.55, gap=1.5)
        if endcap:
            out += rdisc(pts[-1][0], pts[-1][1], endcap, pen)
            for u in dots:
                q = pts[int(len(pts) * u)]
                out += rdisc(q[0], q[1], endcap * 0.8, pen)
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
    out += title_block(black)
    out += qk_block(red, False, rng)
    out += qk_block(blue, True, rng)
    out += fraction_block(black)
    out += fan(Q_FAN, red, endcap=4.4, dots=(0.70, 0.85))
    out += fan([[(_mirror(a), b) for a, b in way] for way in Q_FAN], blue, endcap=4.4, dots=(0.70, 0.85))
    out += interference(black, rng)
    out += softmax_block(black)
    out += fan(V_FAN, ochre)
    out += v_block(ochre)
    out += fan(Z_FAN, ochre)
    out += z_block(green)
    return out
