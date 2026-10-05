"""ATTENTION AS INTERFERENCE — exact recreation of ``ref/reference.png``.

Reproduction, not design.  Every landmark is a pixel coordinate measured off
the 1122x1402 reference raster and mapped into the drawable area, so the plate
is paper-size agnostic.  Text is never sized by eye: each block is scaled to
the width its widest line occupies in the reference.

Five pens: 0 red (Q), 1 blue (K), 2 ochre (V), 3 green (Z), 4 black.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine import kit
from promptplot.generative.engine.kit import (  # noqa: F401
    _catmull_subdivide,
    _dot,
    _poly,
    _stroke_text,
    _text_width,
)
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

REF_W, REF_H = 1122.0, 1402.0
AXIS_PX = 561.0


# ---------------------------------------------------------------------------
# reference-pixel -> millimetre mapping
# ---------------------------------------------------------------------------


class Sheet:
    """Maps reference-raster pixels onto the drawable area.

    ``l`` is the ISOTROPIC length scale -- shapes keep the shape they have in
    the reference.  ``ly`` is the vertical POSITION scale, which differs
    because the reference is 0.800 aspect and A4 is 0.686: the layout stretches
    to fill the sheet, the geometry does not distort.
    """

    def __init__(self, bounds: Bounds) -> None:
        self.x0, self.y0, self.x1, self.y1 = bounds
        self.mx = (self.x1 - self.x0) / REF_W
        self.my = (self.y1 - self.y0) / REF_H

    def p(self, px: float, py: float) -> Pt:
        return (self.x0 + px * self.mx, self.y1 - py * self.my)

    def l(self, px: float) -> float:
        return px * self.mx

    def ly(self, px: float) -> float:
        return px * self.my


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------


def _blob(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    if r <= 0.42:
        return _dot(x, y, r=max(r, 0.22), color=pen)
    return kit.fill_disc(x, y, r, spacing=0.38, pen=pen)


def _ringdot(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    return kit.circle(x, y, r, pen=pen, n=18) + _dot(x, y, r=0.22, color=pen)


def _dash(pts: Sequence[Pt], pen: Optional[int], on: float = 2.0, off: float = 1.6,
          f: int = 2200) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    run: List[Pt] = []
    s = 0.0
    period = on + off
    for i in range(len(pts) - 1):
        ax, ay = pts[i]
        bx, by = pts[i + 1]
        seg = math.hypot(bx - ax, by - ay)
        if seg < 1e-9:
            continue
        steps = max(1, int(seg / 0.45))
        for k in range(steps):
            t0, t1 = k / steps, (k + 1) / steps
            on_now = ((s + seg * (t0 + t1) / 2.0) % period) < on
            pa = (ax + (bx - ax) * t0, ay + (by - ay) * t0)
            pb = (ax + (bx - ax) * t1, ay + (by - ay) * t1)
            if on_now:
                if not run:
                    run.append(pa)
                run.append(pb)
            elif run:
                out += _poly(run, color=pen, f=f)
                run = []
        s += seg
    if len(run) >= 2:
        out += _poly(run, color=pen, f=f)
    return out


def _ellipse_pts(cx: float, cy: float, rx: float, ry: float, n: int = 160,
                 a0: float = 0.0, a1: float = 2 * math.pi) -> List[Pt]:
    return [
        (cx + rx * math.cos(a0 + (a1 - a0) * k / n), cy + ry * math.sin(a0 + (a1 - a0) * k / n))
        for k in range(n + 1)
    ]


def _smooth(ctrl: Sequence[Pt], subdiv: int = 12) -> List[Pt]:
    pts, _ = _catmull_subdivide(list(ctrl), None, subdiv)
    return pts


# ---------------------------------------------------------------------------
# type
# ---------------------------------------------------------------------------


def _fit_cap(text: str, width: float, spaced: bool = False, guess: float = 4.0) -> float:
    """Cap height that makes ``text`` exactly ``width`` mm wide.

    Every text size on this plate is set by a width measured off the reference
    raster, never by eye -- annotation blocks read "about right" at 30% too big.
    """
    s = " ".join(text) if spaced else text
    w = _text_width(s, guess, proportional=True)
    return guess * width / w if w > 1e-6 else guess


def _txt(text: str, x: float, baseline: float, cap: float, pen: Optional[int],
         spaced: bool = False, center: bool = False, f: int = 2400) -> List[GCodeCommand]:
    s = " ".join(text) if spaced else text
    if center:
        x -= _text_width(s, cap, proportional=True) / 2.0
    return _stroke_text(s, x, baseline, cap, color=pen, f=f, proportional=True)


def _block(S: "Sheet", lines: Sequence[str], x_px: float, base_px: float, pitch_px: float,
           width_px: float, pen: Optional[int], spaced: bool = False) -> List[GCodeCommand]:
    widest = max(lines, key=lambda s: _text_width(" ".join(s) if spaced else s, 4.0, True))
    cap = _fit_cap(widest, S.l(width_px), spaced)
    x = S.p(x_px, 0)[0]
    out: List[GCodeCommand] = []
    for i, ln in enumerate(lines):
        out += _txt(ln, x, S.p(0, base_px)[1] - S.l(pitch_px) * i, cap, pen, spaced=spaced)
    return out


# ---------------------------------------------------------------------------
# Q / K / V clusters — spiral nests linked by tangential curve bundles
# ---------------------------------------------------------------------------


def _spiral_nest(cx: float, cy: float, r_out: float, pitch: float, pen: Optional[int],
                 r_in: float, sense: float) -> List[GCodeCommand]:
    """One continuous spiral from ``r_out`` in to the eye at constant radial pitch.

    Constant PITCH (mm per turn), not constant angular step, so consecutive
    rings sit a fixed distance apart however tight the eye gets and the nest
    can never flood into a solid disc.
    """
    turns = max(1.0, (r_out - r_in) / pitch)
    steps = max(60, int(turns * 64))
    pts = []
    for k in range(steps + 1):
        t = k / steps
        r = r_out - (r_out - r_in) * t
        a = sense * 2 * math.pi * turns * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return _poly(pts, color=pen, f=2200)


class ClusterSpec:
    """foci / links / streams / orbits / dots, all in reference pixels."""

    def __init__(self, foci, links, streams, orbits, arcs, dots_on, pen, clip):
        self.foci = foci        # (px, py, r_out_px, pitch_px, sense)
        self.links = links      # (i, a_from, j, a_to, n, bow_px, spread_deg)
        self.streams = streams  # (i, a_deg, span_deg, spine_px, n, spread_px)
        self.orbits = orbits    # (px, py, rx, ry, rot_deg, dashed)
        self.arcs = arcs        # (px, py, r_px, a0_deg, a1_deg) solid sweeping arcs
        self.dots_on = dots_on
        self.pen = pen
        self.clip = clip        # (x0, y0, x1, y1) in px — nothing escapes this


def _wrap_clamp(a: float, lim: float) -> float:
    a = (a + math.pi) % (2 * math.pi) - math.pi
    return max(-lim, min(lim, a))


def _tangent_launch(a: float, sense: float, lead: float = 0.55) -> float:
    """Heading of a curve peeling off a nest: tangential, leaning outward."""
    return a + sense * (math.pi / 2.0 - lead)


def _arc_curve(p0: Pt, h0: float, p1: Pt, h1: float, bow: float,
               subdiv: int = 12) -> List[Pt]:
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    span = math.hypot(dx, dy) or 1.0
    # A tangent that points away from the chord makes the spline double back,
    # which is exactly the cusp that spiked the first linking bundles.  Clamp
    # both headings into a cone about the chord instead.
    chord = math.atan2(dy, dx)
    h0 = chord + _wrap_clamp(h0 - chord, math.radians(74))
    h1 = chord + _wrap_clamp(h1 - chord, math.radians(74))
    ux, uy = dx / span, dy / span
    c1 = (p0[0] + math.cos(h0) * span * 0.34, p0[1] + math.sin(h0) * span * 0.34)
    c2 = (p1[0] - math.cos(h1) * span * 0.34, p1[1] - math.sin(h1) * span * 0.34)
    mid = ((p0[0] + p1[0]) / 2 - uy * bow, (p0[1] + p1[1]) / 2 + ux * bow)
    return _smooth([p0, c1, mid, c2, p1], subdiv=subdiv)


def _offset_spine(spine: Sequence[Pt], amount: float, power: float = 0.28) -> List[Pt]:
    """Copy a spine displaced sideways, the displacement tapering to 0 at its end.

    This is how a BUNDLE is built here rather than by integrating a field: the
    curves are guaranteed to converge exactly on the node and to stay inside
    the cluster, which an ODE will not promise.
    """
    m = len(spine) - 1
    out: List[Pt] = []
    for i, (px, py) in enumerate(spine):
        j0, j1 = max(i - 1, 0), min(i + 1, m)
        dx, dy = spine[j1][0] - spine[j0][0], spine[j1][1] - spine[j0][1]
        L = math.hypot(dx, dy) or 1.0
        taper = (1.0 - i / m) ** power
        out.append((px - dy / L * amount * taper, py + dx / L * amount * taper))
    return out


def _clip_runs(runs, box) -> List[List[Pt]]:
    x0, y0, x1, y1 = box
    out: List[List[Pt]] = []
    for run in runs:
        cur: List[Pt] = []
        for p in run:
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                cur.append(p)
            elif len(cur) >= 2:
                out.append(cur)
                cur = []
            else:
                cur = []
        if len(cur) >= 2:
            out.append(cur)
    return out


# Reserved type boxes, in reference pixels.  OVERLAP IS A DECISION: every
# annotation on this plate owns an allocated rectangle and the geometry is cut
# out of it, so no block is ever legible-by-luck in a gap between curves.
KEEPOUT: List[Tuple[float, float, float, float]] = [
    (228, 14, 864, 78),        # title
    (294, 62, 800, 106),       # subtitle
    (30, 138, 94, 224),        # Q / query
    (30, 226, 94, 318),        # what you are looking for
    (73, 416, 125, 524),       # emit query field into token space
    (1034, 122, 1082, 224),    # K / key
    (1028, 226, 1104, 318),    # what is available in context
    (976, 416, 1049, 508),     # receptive key field across tokens
    (488, 312, 668, 388),      # Q.K^T / sqrt(d_k)
    (850, 523, 948, 620),      # alignment creates an interference pattern
    (417, 647, 705, 724),      # A = softmax(...)
    (184, 712, 268, 748),      # weights
    (186, 754, 315, 830),      # normalize into a probability distribution
    (845, 738, 946, 816),      # each token receives an attention weight
    (1025, 806, 1067, 850),    # V
    (1025, 852, 1082, 878),    # value
    (1025, 884, 1106, 922),    # the content / to be mixed
    (950, 1106, 1042, 1166),   # weighted readout from values
    (159, 1205, 279, 1280),    # a synthesized representation ...
    (502, 1297, 620, 1352),    # Z = AV
    (445, 1352, 676, 1380),    # contextualized output
    (52, 1312, 167, 1384),     # TRANSFORMERS TURN ...
    (996, 1318, 1092, 1384),   # SAME INFORMATION ...
]


def _keepout_boxes(S: Sheet) -> List[Bounds]:
    out = []
    for x0, y0, x1, y1 in KEEPOUT:
        a = S.p(x0, y1)
        b = S.p(x1, y0)
        out.append((a[0], a[1], b[0], b[1]))
    return out


def _reserve(runs, boxes) -> List[List[Pt]]:
    """Cut every run out of the reserved type boxes."""
    out: List[List[Pt]] = []
    for run in runs:
        cur: List[Pt] = []
        for px, py in run:
            inside = any(x0 <= px <= x1 and y0 <= py <= y1 for x0, y0, x1, y1 in boxes)
            if inside:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
            else:
                cur.append((px, py))
        if len(cur) >= 2:
            out.append(cur)
    return out


def _emit(runs, pen, boxes, f: int = 2200) -> List[GCodeCommand]:
    cmds: List[GCodeCommand] = []
    for run in _reserve(runs, boxes):
        cmds += _poly(run, color=pen, f=f)
    return cmds


def _cluster(S: Sheet, spec: ClusterSpec, rng, colors: int) -> List[GCodeCommand]:
    pen = kit._pen(spec.pen, colors)
    out: List[GCodeCommand] = []
    cx0, cy0 = S.p(spec.clip[0], spec.clip[3])
    cx1, cy1 = S.p(spec.clip[2], spec.clip[1])
    box = (cx0, cy0, cx1, cy1)

    orbit_runs = []
    for px, py, rx, ry, rot, dashed in spec.orbits:
        cx, cy = S.p(px, py)
        a = math.radians(rot)
        orbit_runs.append([
            (cx + ex * math.cos(a) - ey * math.sin(a), cy + ex * math.sin(a) + ey * math.cos(a))
            for ex, ey in _ellipse_pts(0.0, 0.0, S.l(rx), S.l(ry) * (S.my / S.mx), n=220)])
    boxes = _keepout_boxes(S)
    for run in _reserve(_clip_runs(orbit_runs, box), boxes):
        out += _dash(run, pen, on=0.35, off=2.0)

    curves: List[List[Pt]] = []

    for px, py, r, a0, a1 in spec.arcs:
        cx, cy = S.p(px, py)
        curves.append(_ellipse_pts(cx, cy, S.l(r), S.l(r) * (S.my / S.mx), n=140,
                                   a0=math.radians(a0), a1=math.radians(a1)))

    for i, a_f, j, a_t, n, bow, spread in spec.links:
        fi, fj = spec.foci[i], spec.foci[j]
        pi_, pj_ = S.p(fi[0], fi[1]), S.p(fj[0], fj[1])
        for k in range(n):
            t = (k / (n - 1.0)) if n > 1 else 0.5
            as_ = math.radians(a_f + (t - 0.5) * spread)
            at_ = math.radians(a_t - (t - 0.5) * spread)
            r0 = S.l(fi[2]) * (1.0 + 0.10 * k)
            r1 = S.l(fj[2]) * (1.0 + 0.10 * (n - 1 - k))
            p0 = (pi_[0] + r0 * math.cos(as_), pi_[1] + r0 * math.sin(as_))
            p1 = (pj_[0] + r1 * math.cos(at_), pj_[1] + r1 * math.sin(at_))
            curves.append(_arc_curve(p0, _tangent_launch(as_, fi[4]), p1,
                                     _tangent_launch(at_, -fj[4]) + math.pi,
                                     S.l(bow) * (0.4 + t)))

    for i, a_deg, span, spine_px, n, spread in spec.streams:
        fi = spec.foci[i]
        fx, fy = S.p(fi[0], fi[1])
        spine = [S.p(*q) for q in spine_px]
        for k in range(n):
            t = (k / (n - 1.0)) if n > 1 else 0.5
            as_ = math.radians(a_deg + (t - 0.5) * span)
            r0 = S.l(fi[2]) * (0.12 + 0.80 * t)
            p0 = (fx + r0 * math.cos(as_), fy + r0 * math.sin(as_))
            off = _offset_spine(spine, S.l(spread) * (t - 0.5))
            w0 = off[0]
            base = math.atan2(w0[1] - p0[1], w0[0] - p0[0])
            # tangential curl off the nest, but never pointing away from the
            # bundle it is joining -- that is what produced sawtooth spikes
            h0 = base + _wrap_clamp(_tangent_launch(as_, fi[4], lead=1.25) - base,
                                    math.radians(34))
            reach = 0.40 * math.hypot(w0[0] - p0[0], w0[1] - p0[1])
            lead = (p0[0] + math.cos(h0) * reach, p0[1] + math.sin(h0) * reach)
            curves.append(_smooth([p0, lead] + off, subdiv=10))

    out += _emit(_clip_runs(curves, box), pen, boxes)

    for px, py, r_out, pitch, sense in spec.foci:
        cx, cy = S.p(px, py)
        out += _spiral_nest(cx, cy, S.l(r_out), S.l(pitch), pen, S.l(3.0), sense)
        out += _blob(cx, cy, S.l(4.0), pen)

    for px, py, r in spec.dots_on:
        if any(x0 <= px <= x1 and y0 <= py <= y1 for x0, y0, x1, y1 in KEEPOUT):
            continue
        cx, cy = S.p(px, py)
        out += _blob(cx, cy, S.l(r), pen)
    return out


# ---------------------------------------------------------------------------
# the woven interference lattice
# ---------------------------------------------------------------------------

LAT_TOP = 387.0
LAT_DEPTH = 214.0
LAT_X0, LAT_X1 = 369.0, 753.0
LAT_G = 268.0          # sideways "acceleration" that bends every column
LAT_FAN = 52.0        # half-angle of the fan leaving each node, degrees
LAT_COLS = 16
LAT_ROWS = [437.0 + 16.8 * k for k in range(9)]


def _column(S: Sheet, node_px: Pt, vx: float, sign: float) -> List[Pt]:
    """One lattice column as a parabola: launched from the node, bent sideways.

    The reference's weave is TWO of these families, one per node, bent towards
    each other — which is why the outer columns make a U (out, vertex, back)
    and the inner ones race across.  A pair of straight fans cannot do that.
    """
    nx, ny = node_px
    pts: List[Pt] = []
    steps = 70
    for k in range(steps + 1):
        t = k / steps
        dx = sign * (vx * t + 0.5 * LAT_G * t * t)
        pts.append((nx + S.l(dx), ny - S.ly(LAT_DEPTH) * t))
    return pts


def _lattice(S: Sheet, colors: int) -> List[GCodeCommand]:
    blk = kit._pen(BLACK, colors)
    red = kit._pen(RED, colors)
    blu = kit._pen(BLUE, colors)
    out: List[GCodeCommand] = []

    nodeL = S.p(488, LAT_TOP)
    nodeR = S.p(639, LAT_TOP)
    axis_x = S.p(AXIS_PX, 0)[0]
    box = (S.p(LAT_X0, 0)[0], S.p(0, 640)[1], S.p(LAT_X1, 0)[0], S.p(0, LAT_TOP)[1])

    vxs = [LAT_DEPTH * math.tan(math.radians(-LAT_FAN + 2 * LAT_FAN * k / (LAT_COLS - 1.0)))
           for k in range(LAT_COLS)]

    runs = []
    for node, sign, tint in ((nodeL, 1.0, red), (nodeR, -1.0, blu)):
        for idx, vx in enumerate(vxs):
            runs.append((_column(S, node, vx, sign), tint, idx))

    boxes = _keepout_boxes(S)
    for run, tint, idx in runs:
        for piece in _clip_runs([run], box):
            if idx < 7:                     # outermost columns carry the cluster colour
                cut = max(2, int(len(piece) * 0.34))
                out += _emit([piece[: cut + 1]], tint, boxes)
                out += _emit([piece[cut:]], blk, boxes)
            else:
                out += _emit([piece], blk, boxes)

    # token rows: full width, horizontal at the margins, sagging under the weave
    for i, ry in enumerate(LAT_ROWS):
        sag = S.ly(5.0 + 1.6 * i)
        pts = []
        steps = 96
        for k in range(steps + 1):
            u = k / steps
            x_px = LAT_X0 + (LAT_X1 - LAT_X0) * u
            pts.append((S.p(x_px, 0)[0], S.p(0, ry)[1] - sag * math.sin(math.pi * u) ** 1.6))
        out += _emit([pts], blk, boxes)

    def grid_dots(node, sign, tint):
        cmds: List[GCodeCommand] = []
        for k in range(2, 8):
            run = _column(S, node, vxs[k], sign)
            for ry in LAT_ROWS:
                y = S.p(0, ry)[1]
                hit = None
                for i in range(len(run) - 1):
                    if (run[i][1] - y) * (run[i + 1][1] - y) <= 0:
                        d0, d1 = abs(run[i][1] - y), abs(run[i + 1][1] - y)
                        fr = d0 / (d0 + d1 + 1e-9)
                        hit = (run[i][0] + (run[i + 1][0] - run[i][0]) * fr, y)
                        break
                if hit is None or not (box[0] <= hit[0] <= box[2]):
                    continue
                if abs(hit[0] - axis_x) < S.l(44):
                    continue
                tinted = ry < 505 and k >= 4
                cmds += _blob(hit[0], hit[1], S.l(4.0 if k < 4 else 3.4),
                              tint if tinted else blk)
        return cmds

    out += grid_dots(nodeL, 1.0, red)
    out += grid_dots(nodeR, -1.0, blu)

    for k in range(20):
        cx, cy = S.p(AXIS_PX, 400 + k * (222.0 / 19.0))
        out += _ringdot(cx, cy, S.l(3.4), blk)

    ay = S.p(0, 487)[1]
    out += _dash([(S.p(215, 0)[0], ay), (S.p(905, 0)[0], ay)], blk, on=2.4, off=2.2)
    for px in (271, 854):
        out += _ringdot(S.p(px, 0)[0], ay, S.l(4.0), blk)

    for px in (420, 702):
        cx, cy = S.p(px, 468)
        out += _dash(_ellipse_pts(cx, cy, S.l(132), S.l(132) * (S.my / S.mx), n=220),
                     blk, on=1.1, off=3.6)
    return out


# ---------------------------------------------------------------------------
# the softmax weights disc
# ---------------------------------------------------------------------------

DISC_BASE = 807.0
DISC_AMP = 72.0        # apex height above the base plane, px
DISC_SIG = 79.5        # fitted from the ring-extreme locus in the reference
DISC_EXP = 1.554
DISC_FLAT = 0.35
DISC_RMAX = 186.0
DISC_RDOT = 206.0


def _disc_h(S: Sheet, r_mm: float) -> float:
    r_px = r_mm / S.mx
    return S.ly(DISC_AMP) * math.exp(-((r_px / DISC_SIG) ** DISC_EXP))


def _disc(S: Sheet, colors: int) -> List[GCodeCommand]:
    blk = kit._pen(BLACK, colors)
    out: List[GCodeCommand] = []
    cx, base = S.p(AXIS_PX, DISC_BASE)
    rmax = S.l(DISC_RMAX)

    # radii stepped so the ring EXTREMES (the cone flank) stay a fixed distance
    # apart -- even radii would bunch the flank and leave the rim sparse.
    radii: List[float] = []
    r = S.l(5.0)
    while r < rmax:
        radii.append(r)
        eps = S.l(0.6)
        slope = abs(_disc_h(S, r + eps) - _disc_h(S, r)) / eps
        dr = 1.70 / math.hypot(1.0, slope)
        r += min(max(dr, 1.35), 2.6)
    vs = S.my / S.mx
    for r in radii:
        out += _poly(_ellipse_pts(cx, base + _disc_h(S, r), r, r * DISC_FLAT * vs, n=120),
                     color=blk, f=2200)

    rd = S.l(DISC_RDOT)
    out += _dash(_ellipse_pts(cx, base + _disc_h(S, rd), rd, rd * DISC_FLAT * vs, n=240),
                 blk, on=1.0, off=1.9)

    out += _ringdot(cx, base + S.ly(DISC_AMP), S.l(4.0), blk)

    out += _poly([(S.p(320, 0)[0], base), (S.p(806, 0)[0], base)], color=blk, f=2200)
    for px in (330, 372, 414, 458, 503, 619, 664, 708, 750, 792):
        out += _blob(S.p(px, 0)[0], base, S.l(3.4), blk)

    drop_y = S.p(0, 894)[1]
    for px in (516, 538, 561, 584, 607):
        x = S.p(px, 0)[0]
        r_here = max(abs(x - cx), S.l(3))
        top = base + _disc_h(S, r_here) - r_here * DISC_FLAT * vs
        out += _poly([(x, top), (x, drop_y + S.l(5))], color=blk, f=2200)
        out += _ringdot(x, drop_y, S.l(4.2), blk)
    return out


# ---------------------------------------------------------------------------
# Z = AV — the contextualised output surface
# ---------------------------------------------------------------------------

Z_AXIS = 1195.0
Z_HALF = 205.0
Z_DEPTH = 250.0
Z_FLAT = 0.26
Z_AMP = 60.0
Z_SIG = 56.0
Z_MOAT = 20.0
Z_MOAT_R = 120.0
Z_MOAT_W = 55.0
Z_ROWS = 25
Z_SQUASH = 0.40       # the bump runs further in depth than across
Z_RIDGE = 18.0        # the outer ring that opens the butterfly wings
Z_RIDGE_R = 128.0
Z_RIDGE_W = 34.0


def _zsurface(S: Sheet, colors: int) -> List[GCodeCommand]:
    grn = kit._pen(GREEN, colors)
    blk = kit._pen(BLACK, colors)
    out: List[GCodeCommand] = []
    cx, ay = S.p(AXIS_PX, Z_AXIS)
    half = S.l(Z_HALF)

    def hh(r_px: float) -> float:
        return (S.ly(Z_AMP) * math.exp(-((r_px / Z_SIG) ** 2))
                - S.ly(Z_MOAT) * math.exp(-(((r_px - Z_MOAT_R) / Z_MOAT_W) ** 2))
                + S.ly(Z_RIDGE) * math.exp(-(((r_px - Z_RIDGE_R) / Z_RIDGE_W) ** 2)))

    vs = S.my / S.mx
    for rr, fl in ((0.95, 0.60), (0.72, 0.76)):
        out += _dash(_ellipse_pts(cx, ay, half * rr, half * rr * fl * vs, n=240),
                     blk, on=0.45, off=2.8)

    for j in range(Z_ROWS):
        d = (j / (Z_ROWS - 1.0) - 0.5) * 2.0 * Z_DEPTH
        pts: List[Pt] = []
        steps = 220
        for k in range(steps + 1):
            x_px = (-Z_HALF + 2 * Z_HALF * (k / steps))
            w = (1.0 - (x_px / Z_HALF) ** 2) ** 0.75
            r = math.hypot(x_px, d * Z_SQUASH)
            pts.append((cx + S.l(x_px), ay + w * (S.ly(d) * Z_FLAT + hh(r))))
        out += _poly(pts, color=grn, f=2200)

    # The reference's summit is a closed NEST, not a stack of open humps: the
    # row family alone can only fold, so the peak is also drawn as iso-height
    # rings of the same surface -- the two families share hh(), so the rings sit
    # exactly on the folds instead of floating over them.
    nest_y = ay + S.ly(34.0)
    rr = S.l(9.0)
    while rr < S.l(88.0):
        out += _poly(_ellipse_pts(cx, nest_y, rr, rr * 0.45 * vs, n=110), color=grn, f=2200)
        rr += S.l(8.5)
    out += _ringdot(cx, nest_y, S.l(4.0), grn)

    out += _poly([(S.p(228, 0)[0], ay), (S.p(893, 0)[0], ay)], color=blk, f=2200)
    for px in (228, 300, 892):
        out += _blob(S.p(px, 0)[0], ay, S.l(3.0), blk)
    for px in (386, 424, 698, 736):
        out += _blob(S.p(px, 0)[0], ay, S.l(3.6), grn)

    out += _poly([(cx, S.p(0, 1030)[1]), (cx, S.p(0, 1298)[1])], color=grn, f=2200)
    for py in (1034, 1090, 1113, 1160, 1206, 1237, 1266, 1287):
        out += _ringdot(cx, S.p(0, py)[1], S.l(3.6), grn)
    return out


# ---------------------------------------------------------------------------
# formulas — the stroke font has no radical, so it is drawn as geometry
# ---------------------------------------------------------------------------


def _radical(x: float, baseline: float, cap: float, w: float,
             pen: Optional[int]) -> List[GCodeCommand]:
    return _poly(
        [(x, baseline + cap * 0.44), (x + cap * 0.20, baseline + cap * 0.12),
         (x + cap * 0.44, baseline + cap * 1.22), (x + w, baseline + cap * 1.22)],
        color=pen, f=2400,
    )


def _qk_parts(cap: float) -> List[Tuple[str, str, float]]:
    """(kind, payload, width) for ``Q . K^T / sqrt(d_k)``."""
    sub = cap * 0.62
    return [
        ("t", "Q", _text_width("Q", cap, True)),
        ("d", "", cap * 0.52),
        ("t", "K", _text_width("K", cap, True)),
        ("s", "T", _text_width("T", sub, True)),
        ("t", "/", _text_width("/", cap, True)),
        ("r", "", cap * 0.44),
        ("t", "d", _text_width("d", cap, True)),
        ("b", "k", _text_width("k", sub, True)),
        ("g", "", cap * 0.16),
    ]


def _lay(parts, x: float, baseline: float, cap: float, pen: Optional[int],
         rad_from: int) -> List[GCodeCommand]:
    sub = cap * 0.62
    out: List[GCodeCommand] = []
    rad_w = sum(w for _, _, w in parts[rad_from:])
    for i, (kind, payload, w) in enumerate(parts):
        if kind == "t":
            out += _txt(payload, x, baseline, cap, pen)
        elif kind == "s":
            out += _txt(payload, x, baseline + cap * 0.58, sub, pen)
        elif kind == "b":
            out += _txt(payload, x, baseline - cap * 0.22, sub, pen)
        elif kind == "d":
            out += _dot(x + w * 0.5, baseline + cap * 0.34, r=0.26, color=pen)
        elif kind == "r":
            out += _radical(x, baseline, cap, rad_w, pen)
        x += w
    return out


def _qk_formula(S: Sheet, cx_px: float, base_px: float, width_px: float,
                pen: Optional[int]) -> List[GCodeCommand]:
    cap = 4.0
    parts = _qk_parts(cap)
    cap *= S.l(width_px) / sum(w for _, _, w in parts)
    parts = _qk_parts(cap)
    total = sum(w for _, _, w in parts)
    return _lay(parts, S.p(cx_px, 0)[0] - total / 2.0, S.p(0, base_px)[1], cap, pen, 5)


def _softmax_formula(S: Sheet, cx_px: float, base_px: float, width_px: float,
                     pen: Optional[int]) -> List[GCodeCommand]:
    def build(cap):
        sub = cap * 0.62
        return ([("t", "A = softmax(", _text_width("A = softmax(", cap, True)),
                 ("t", "QK", _text_width("QK", cap, True)),
                 ("s", "T", _text_width("T", sub, True)),
                 ("t", "/", _text_width("/", cap, True)),
                 ("r", "", cap * 0.44),
                 ("t", "d", _text_width("d", cap, True)),
                 ("b", "k", _text_width("k", sub, True)),
                 ("g", "", cap * 0.16),
                 ("t", ")", _text_width(")", cap, True))])
    cap = 4.0
    parts = build(cap)
    cap *= S.l(width_px) / sum(w for _, _, w in parts)
    parts = build(cap)
    total = sum(w for _, _, w in parts)
    # the radical spans only d_k, not the trailing bracket
    out: List[GCodeCommand] = []
    x = S.p(cx_px, 0)[0] - total / 2.0
    baseline = S.p(0, base_px)[1]
    rad_w = sum(w for _, _, w in parts[4:8])
    sub = cap * 0.62
    for kind, payload, w in parts:
        if kind == "t":
            out += _txt(payload, x, baseline, cap, pen)
        elif kind == "s":
            out += _txt(payload, x, baseline + cap * 0.58, sub, pen)
        elif kind == "b":
            out += _txt(payload, x, baseline - cap * 0.22, sub, pen)
        elif kind == "r":
            out += _radical(x, baseline, cap, rad_w, pen)
        x += w
    return out


# ---------------------------------------------------------------------------
# furniture + annotation
# ---------------------------------------------------------------------------


def _furniture(S: Sheet, colors: int) -> List[GCodeCommand]:
    blk = kit._pen(BLACK, colors)
    out: List[GCodeCommand] = []

    def cross(px, py, vh, hw, frac):
        cx, cy = S.p(px, py)
        out.extend(_poly([(cx, cy + S.ly(vh) / 2), (cx, cy - S.ly(vh) / 2)], color=blk))
        yb = cy + S.ly(vh) / 2 - S.ly(vh) * frac
        out.extend(_poly([(cx - S.l(hw) / 2, yb), (cx + S.l(hw) / 2, yb)], color=blk))

    cross(53, 60, 38, 24, 0.36)
    cross(1068, 60, 38, 24, 0.36)
    # the foot marks sit CLEAR of the footer type: a corner rule that runs
    # through a word is a collision, not a composition
    cross(48, 1315, 32, 30, 0.20)
    cross(1074, 1315, 32, 30, 0.20)

    for px in (53.5, 1067.5):
        x, _ = S.p(px, 0)
        out += _poly([(x, S.p(0, 366)[1]), (x, S.p(0, 560)[1])], color=blk)
        out += kit.plus_mark(x, S.p(0, 570)[1], s=S.l(9), pen=blk)
        out += _poly([(x, S.p(0, 606)[1]), (x, S.p(0, 758)[1])], color=blk)
        for py in (690, 714, 738):
            cy = S.p(0, py)[1]
            out += kit.circle(x, cy, S.l(15), pen=blk, n=52)
            out += _dot(x, cy, r=0.24, color=blk)
        out += _poly([(x, S.p(0, 972)[1]), (x, S.p(0, 1012)[1])], color=blk)
        out += kit.plus_mark(x, S.p(0, 1022)[1], s=S.l(9), pen=blk)
    return out


def _titles(S: Sheet, colors: int) -> List[GCodeCommand]:
    blk = kit._pen(BLACK, colors)
    red = kit._pen(RED, colors)
    blu = kit._pen(BLUE, colors)
    och = kit._pen(OCHRE, colors)
    grn = kit._pen(GREEN, colors)
    out: List[GCodeCommand] = []

    out += _txt("ATTENTION AS INTERFERENCE", S.p(546, 0)[0], S.p(0, 69)[1],
                _fit_cap("ATTENTION AS INTERFERENCE", S.l(618), True), blk,
                spaced=True, center=True)
    out += _txt("alignment selects and mixes context", S.p(547, 0)[0], S.p(0, 85)[1],
                _fit_cap("alignment selects and mixes context", S.l(488), True), blk,
                spaced=True, center=True)

    cap_big = S.l(32)

    out += _txt("Q", S.p(48, 0)[0], S.p(0, 181)[1], cap_big, red)
    out += _txt("query", S.p(38, 0)[0], S.p(0, 212)[1], _fit_cap("query", S.l(44)), red)
    out += _block(S, ["what", "you", "are", "looking", "for"], 38, 243, 16.3, 48, blk)
    out += _block(S, ["emit", "query", "field", "into", "token", "space"], 81, 435, 16.6, 36, blk)

    out += _txt("K", S.p(1042, 0)[0], S.p(0, 185)[1], cap_big, blu)
    out += _txt("key", S.p(1043, 0)[0], S.p(0, 213)[1], _fit_cap("key", S.l(28)), blu)
    out += _block(S, ["what", "is", "available", "in", "context"], 1036, 243, 16.3, 60, blk)
    out += _block(S, ["receptive", "key", "field", "across", "tokens"], 984, 434, 16.3, 57, blk)

    out += _txt("V", S.p(1031, 0)[0], S.p(0, 845)[1], cap_big, och)
    out += _txt("value", S.p(1031, 0)[0], S.p(0, 870)[1], _fit_cap("value", S.l(44)), och)
    out += _block(S, ["the content", "to be mixed"], 1031, 900, 16.3, 68, blk)
    out += _block(S, ["weighted", "readout", "from values"], 956, 1127, 16.3, 79, blk)

    out += _block(S, ["alignment", "creates", "an", "interference", "pattern"],
                  858, 545, 16.3, 82, blk)
    out += _txt("weights", S.p(192, 0)[0], S.p(0, 737)[1], _fit_cap("weights", S.l(68)), blk)
    out += _block(S, ["normalize", "into", "a probability", "distribution"],
                  194, 771, 16.3, 115, blk)
    out += _block(S, ["each token", "receives", "an attention", "weight"],
                  853, 755, 16.3, 85, blk)
    out += _block(S, ["a synthesized", "representation", "from relevant", "context"],
                  167, 1222, 16.3, 104, blk)

    out += _qk_formula(S, 578, 366, 163, blk)
    out += _softmax_formula(S, 561, 700, 272, blk)
    out += _txt("Z = AV", S.p(561, 0)[0], S.p(0, 1340)[1], _fit_cap("Z = AV", S.l(102)),
                grn, center=True)
    out += _txt("contextualized output", S.p(561, 0)[0], S.p(0, 1372)[1],
                _fit_cap("contextualized output", S.l(215), True), blk,
                spaced=True, center=True)

    out += _block(S, ["TRANSFORMERS", "TURN", "ALIGNMENT", "INTO", "MEANING"],
                  56, 1322, 14.0, 97, blk, spaced=True)
    out += _poly([(S.p(112, 0)[0], S.p(0, 1374)[1]), (S.p(152, 0)[0], S.p(0, 1374)[1])], color=blk)
    out += _block(S, ["SAME", "INFORMATION", "DIFFRENT", "INTERFERENCE"],
                  1001, 1328, 14.0, 84, blk, spaced=True)
    out += _poly([(S.p(1000, 0)[0], S.p(0, 1374)[1]), (S.p(1042, 0)[0], S.p(0, 1374)[1])],
                 color=blk)

    ax, _ = S.p(AXIS_PX, 0)
    out += _poly([(ax, S.p(0, 105)[1]), (ax, S.p(0, 323)[1])], color=blk)
    out += _ringdot(ax, S.p(0, 178)[1], S.l(4.2), blk)
    out += _poly([(ax, S.p(0, 375)[1]), (ax, S.p(0, 648)[1])], color=blk)
    ay = S.p(0, 648)[1]
    out += _poly([(ax - S.l(6), ay + S.ly(14)), (ax, ay), (ax + S.l(6), ay + S.ly(14))], color=blk)
    out += _poly([(ax, S.p(0, 709)[1]), (ax, S.p(0, 1030)[1])], color=blk)
    return out


# ---------------------------------------------------------------------------
# cluster data (reference pixels)
# ---------------------------------------------------------------------------

Q_SPEC = ClusterSpec(
    foci=[(190, 166, 75, 7.6, 1.0), (168, 315, 58, 6.6, 1.0),
          (283, 272, 20, 4.4, -1.0), (316, 387, 15, 4.0, 1.0)],
    links=[],
    streams=[
        (0, -16, 124, [(296, 178), (372, 218), (428, 282), (464, 340), (488, 387)], 12, 268),
        (1, -18, 116, [(248, 344), (330, 376), (402, 392), (452, 392), (488, 387)], 8, 168),
    ],
    orbits=[(190, 166, 96, 96, 0, True), (190, 166, 124, 124, 0, True),
            (196, 172, 152, 134, -12, True), (168, 315, 80, 80, 0, True),
            (168, 315, 104, 104, 0, True), (283, 272, 40, 40, 0, True),
            (250, 300, 156, 126, -20, True)],
    arcs=[(258, 210, 118, 50, 330), (232, 330, 130, -40, 120),
          (330, 250, 150, 95, 250), (200, 250, 190, -70, 60)],
    dots_on=[(160, 92, 4.6), (249, 100, 4.0), (302, 74, 4.4), (330, 82, 3.4),
             (245, 148, 3.4), (110, 190, 3.2), (249, 194, 4.2),
             (283, 226, 4.0), (352, 202, 4.0), (373, 224, 4.6),
             (247, 251, 3.6), (137, 254, 4.2), (89, 300, 4.0),
             (128, 358, 4.0), (205, 331, 4.0), (285, 314, 3.4), (340, 300, 4.0),
             (163, 416, 4.2), (238, 410, 4.0), (277, 385, 3.6),
             (330, 404, 4.6), (300, 452, 3.6), (355, 440, 3.4), (420, 292, 4.6)],
    pen=RED, clip=(96, 70, 492, 474),
)

K_SPEC = ClusterSpec(
    foci=[(969, 151, 62, 6.8, -1.0), (797, 265, 62, 6.8, -1.0),
          (945, 352, 58, 6.6, -1.0), (838, 378, 20, 4.4, 1.0)],
    links=[],
    streams=[
        (1, 196, -124, [(746, 292), (696, 322), (664, 352), (646, 372), (639, 387)], 12, -258),
        (2, 198, -116, [(866, 392), (784, 412), (702, 404), (657, 394), (639, 387)], 8, -164),
    ],
    orbits=[(969, 151, 90, 90, 0, True), (969, 151, 118, 118, 0, True),
            (797, 265, 84, 84, 0, True), (797, 265, 110, 110, 0, True),
            (945, 352, 84, 84, 0, True), (880, 300, 158, 130, 18, True)],
    arcs=[(886, 200, 120, -150, 130), (900, 330, 128, 60, 220),
          (800, 270, 150, -70, 110), (940, 260, 170, 120, 300)],
    dots_on=[(905, 95, 4.0), (966, 88, 3.4), (1011, 116, 3.4), (838, 148, 4.2),
             (893, 175, 4.0), (900, 196, 3.8), (906, 220, 3.6), (1006, 205, 3.6),
             (1030, 158, 3.2), (740, 190, 4.0), (712, 236, 3.6), (752, 268, 3.4),
             (920, 268, 3.6), (960, 250, 3.4), (846, 300, 3.8), (870, 322, 3.4),
             (738, 331, 3.6), (781, 348, 3.4), (856, 402, 3.6), (918, 412, 3.4),
             (958, 430, 3.6), (874, 452, 3.4), (700, 420, 4.0), (770, 444, 3.4),
             (816, 476, 3.4), (676, 300, 4.0)],
    pen=BLUE, clip=(634, 70, 1040, 500),
)

V_SPEC = ClusterSpec(
    foci=[(963, 888, 56, 6.4, -1.0), (853, 970, 40, 5.6, -1.0),
          (965, 1043, 58, 6.6, -1.0), (878, 1055, 22, 4.6, 1.0)],
    links=[],
    streams=[
        (1, 194, -126, [(826, 978), (798, 990), (776, 997), (766, 1000)], 9, -176),
        (0, 228, -120, [(888, 932), (830, 966), (788, 990), (766, 1000)], 8, -152),
    ],
    orbits=[(963, 888, 78, 78, 0, True), (963, 888, 100, 100, 0, True),
            (853, 970, 58, 58, 0, True), (965, 1043, 80, 80, 0, True),
            (915, 970, 154, 126, 12, True)],
    arcs=[(910, 930, 96, -160, 150), (920, 1010, 104, 30, 230),
          (963, 965, 120, 60, 300), (876, 1010, 96, -120, 120)],
    dots_on=[(955, 843, 4.0), (876, 902, 3.6), (798, 924, 3.8),
             (905, 940, 3.4), (1006, 952, 3.6), (1011, 930, 3.2),
             (833, 1010, 3.4), (908, 1006, 3.2), (952, 984, 3.2),
             (770, 1082, 3.6), (786, 1104, 3.6), (858, 1096, 3.4), (944, 1090, 3.6),
             (986, 1076, 3.2), (1012, 1006, 3.2), (900, 1130, 3.4)],
    pen=OCHRE, clip=(742, 802, 1082, 1106),
)


def _readout(S: Sheet, colors: int) -> List[GCodeCommand]:
    """Weights -> V, and weights -> Z: the swoop out of the disc droplines."""
    blk = kit._pen(BLACK, colors)
    och = kit._pen(OCHRE, colors)
    grn = kit._pen(GREEN, colors)
    out: List[GCodeCommand] = []
    drop_y = S.p(0, 894)[1]

    # the ochre read-out column the V field drains into
    col_px = [(766, 940 + 24 * k) for k in range(7)]
    for k, (qx, qy) in enumerate(col_px):
        out += _ringdot(S.p(qx, qy)[0], S.p(qx, qy)[1], S.l(3.4), och)

    starts = [(607, och), (584, och), (561, blk), (584, och), (607, och), (561, och), (584, och)]
    for k, (px, pen) in enumerate(starts):
        p0 = (S.p(px, 0)[0], drop_y)
        p1 = S.p(*col_px[k])
        mid = S.p(640 + 12 * k, 918 + 14 * k)
        out += _poly(_smooth([p0, mid, p1], subdiv=14), color=pen, f=2200)

    for px in (516, 538):
        p0 = (S.p(px, 0)[0], drop_y)
        out += _dash(_smooth([p0, S.p(px - 4, 970), S.p(px - 10, 1046)], subdiv=12),
                     blk, on=2.0, off=2.0)
    for k, px in enumerate((561, 584, 607)):
        p0 = (S.p(px, 0)[0], drop_y)
        p1 = S.p(561 + (k - 1) * 16, 1036)
        out += _poly(_smooth([p0, S.p(px + (k - 1) * 10, 975), p1], subdiv=14),
                     color=grn if k != 2 else blk, f=2200)
    return out


# ---------------------------------------------------------------------------


def attention_interference(rng, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    S = Sheet(bounds)
    out: List[GCodeCommand] = []
    out += _furniture(S, colors)
    out += _cluster(S, Q_SPEC, rng, colors)
    out += _cluster(S, K_SPEC, rng, colors)
    out += _lattice(S, colors)
    out += _disc(S, colors)
    out += _readout(S, colors)
    out += _cluster(S, V_SPEC, rng, colors)
    out += _zsurface(S, colors)
    out += _titles(S, colors)
    return out
