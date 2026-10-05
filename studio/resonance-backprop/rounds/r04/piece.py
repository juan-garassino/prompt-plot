"""ATTENTION AS RESONANCE (forward + backward) — resonance-backprop r04 (iterate, parent r01).

Juan, 2026-09-28, on ``pp_res_backprop_v5.png``: "the original was much more beautiful — we
just needed the dot lines to be more continuous, not to remove the waves".  So this round is
r01, element for element, with two changes and nothing else:

1. **v5's tonal field in place of v8's dashed oval.**  v5's gcode was overwritten by v8's, so
   the field was re-measured off the v5 PNG (mm axes printed on it) — see NOTES.md
   § Measurements.  Measured, in reference px:
     * dotted crest arcs  r_s = m * lam,  m = 10, 13, ... 73 (22 rings per source), clipped to
       the ellipse (560, 448; a 352, b 128), outside the bullseye pad (R_BULL + 5) and the
       comb lens (100 x 40);
     * dotted halo ellipses: three per source, centred ON each source, a = 196, 245.5, 300,
       b = 0.40 a;
     * the "scatter": r01's own 10 seeded field-weighted discs (same draws, same positions)
       plus the beaded dropline columns.  v5's grey band is the dotted crest arcs, not a
       scatter.
2. **How marks are made and how the sheet streams.**
     * Every dotted LINE (fans, leaders, droplines, guides, halos, crest arcs, envelopes,
       ghost waves) is one round dot every DOT_PITCH = 1.0 mm, END-ANCHORED
       (n = round(len / pitch) intervals, n + 1 dots) — resonance r10's DOT_PITCH / DOT_R /
       DOT_MAX with r03's end-anchored ``_dotted``.  The dot is a closed 8-gon of radius
       DOT_R (0.30 mm across; 0.65 mm of ink at a 0.35 mm nib): round, one fixed size, never
       a dash.
     * Same-pen dotted paths closer than 2 mm and within 25 deg of parallel are PHASE-LOCKED:
       the later path's dots are placed opposite the earlier path's dots (anchors), and the
       stretches between anchors are filled end-anchored at the same pitch.
     * TEXTURES (the 10 scatter discs, the beaded columns) keep r01's count and positions,
       one round dot or one solid disc per mark by radius; never re-pitched.
     * A dot is dropped only if it would be invisible: < 0.3 mm of paper between it and
       other same-pen ink, centre inside a label box + 0.9 mm (exact ``geometry`` Rect/Union),
       on a node, or a co-incident duplicate.  The black field dots (crest arcs, halos) also
       yield 0.4 mm of paper to every other pen's ink and fan path, so the field sits BEHIND
       the Q/K/V fans and never crosses them (A7).
     * Multi-pass glyphs and arrowheads are chained into one pen-down.
     * Two sub-millimetre mark moves, both so a mark reads at a 0.35 mm nib: packet envelopes
       stand ENV_LIFT = 0.8 mm off the crest tips (on the tips 60 % of their dots were
       invisible), and the i/j tittle of small type is lifted to leave 0.3 mm of paper.
     * Pens are indexed in STREAM order, light -> dark (goldenrod, dodgerblue, forestgreen,
       crimson, black); each layer is ordered as a serpentine sweep of 30 mm cells with a
       reversal-aware nearest-end walk inside each cell, so every 400-stroke batch is one
       region of the sheet.  ``plate.py`` writes the plate gcode with that order kept (the
       render pipeline's nearest-start pass would undo it).

The hero (d = 59 L, bullseyes m 1-9, comb m 10-50 in the lens, ``_Guard`` 0.82 mm / 25 deg),
every packet, fan, dropline, arrowhead, fraction, the rail, title, subtitle and crosses are
r01's code and coordinates unchanged.

Lineage: Hermann von Helmholtz, *On the Sensations of Tone* (1863) — the wave-composition
figures, where rows of partial waves are drawn one above another on shared axes and summed
into a compound wave below them.  The ORDER it lends: stacked partials -> one sum.  Q and K
rows are partials, their interference is the sum, A selects, Z = AV is the compound wave, and
the backward band re-reads the same stack upward.  Flat: a reproduction of a flat plate
diagram; depth is not claimed.

Pens (render palette goldenrod,dodgerblue,forestgreen,crimson,black):
    0 ochre = V, dL/dV · 1 blue = K, dL/dK · 2 green = Z, dL/dZ · 3 crimson = Q, dL/dQ ·
    4 black = the field, softmax, dL/dA, rail, type, crosses

Entry point: ``attention_as_resonance``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, Union
from promptplot.generative.engine.kit import _GLYPHS, _offset_polyline, _poly
from promptplot.generative.generators import _glyph_advance
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# Pen slots in STREAM order, light -> dark.  The family grammar is by COLOUR (Q crimson,
# K blue, V goldenrod, Z green, black), so only the indices moved from r01.
OCHRE, BLUE, GREEN, RED, BLACK = 0, 1, 2, 3, 4
PALETTE = "goldenrod,dodgerblue,forestgreen,crimson,black"

# --- the dot (shared with resonance r10 and resonance-ffn) -------------------
PEN_MM = 0.35            # the nib the plate is judged at (0.3-0.4 mm fineliner)
DOT_PITCH = 1.0          # mm, centre to centre, end-anchored
DOT_R = 0.15             # the dot: a closed 8-gon of this radius (0.30 mm across)
DOT_MAX = 0.6            # r10: a dash this short was always meant as a dot.  In r01 every
                         # rdotted dash is a dotted LINE, so every one of them becomes dots
DOT_INK = DOT_R + PEN_MM / 2.0   # 0.325 mm: ink radius of one dot
HALO_PAD = 0.9           # mm of clear paper around every label
GAP_SAME = 0.3           # a dot with less paper than this to same-pen ink is invisible
GAP_FIELD = 0.4          # the black field yields this much paper to every other pen
GAP_NODE = 0.2           # a dot this close to a node's ink sits ON the node
LOCK_DIST = 2.0          # same-pen dotted paths closer than this are phase-locked ...
LOCK_COS = math.cos(math.radians(25.0))   # ... when within 25 deg of parallel
CELL_MM = 30.0           # stream-order cell (serpentine sweep)
ENV_LIFT = 0.8           # mm: packet envelopes stand this far off the crest tips

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
# MARKS.  r01 emitted GCodeCommands straight from each primitive; r04 emits MARKS (what the
# thing is: a line, a node, a texture mark, a type stroke, a dotted PATH still to be dotted),
# so the sheet pass can dot, cull, phase-lock and order them with the whole plate in view.
# Arguments in REFERENCE px unless noted; Mark coordinates are sheet mm.
# ---------------------------------------------------------------------------


class Mark:
    __slots__ = ("kind", "pen", "pts", "c", "r", "label", "role", "pid")

    def __init__(self, kind: str, pen: Optional[int], pts: List[Pt], c: Optional[Pt] = None,
                 r: float = 0.0, label: int = -1, role: str = "", pid: int = -1) -> None:
        self.kind = kind      # line | node | tex | type | arrow | path | dot
        self.pen = pen
        self.pts = pts
        self.c = c
        self.r = r
        self.label = label
        self.role = role      # path roles: fan | field | drop | guide | env | ghost
        self.pid = pid


_IDS = {"label": 0, "pid": 0}


def _new(key: str) -> int:
    _IDS[key] += 1
    return _IDS[key]


def _octagon(cx: float, cy: float, r: float = DOT_R) -> List[Pt]:
    return [(cx + r * math.cos(2 * math.pi * k / 8), cy + r * math.sin(2 * math.pi * k / 8))
            for k in range(9)]


def _spiral(cx: float, cy: float, r: float, spacing: float) -> List[Pt]:
    """kit.fill_disc's Archimedean spiral (same turns rule), as points."""
    turns = max(2, int(r / spacing))
    n = turns * 30
    return [(cx + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
             cy + r * (k / n) * math.sin(2 * math.pi * turns * k / n)) for k in range(n + 1)]


def rpoly(ref_pts: Sequence[Pt], pen: Optional[int], f: int = 2000,
          kind: str = "line") -> List[Mark]:
    pts = PP(ref_pts)
    if len(pts) < 2:
        return []
    return [Mark(kind, pen, pts, label=_new("label") if kind == "type" else -1)]


def rcircle(rx: float, ry: float, rr: float, pen: Optional[int], n: int = 0) -> List[Mark]:
    x, y = P(rx, ry)
    r = L(rr)
    if n <= 0:
        n = max(16, int(2 * math.pi * r / 0.55))
    ring = [(x + r * math.cos(2 * math.pi * k / n), y + r * math.sin(2 * math.pi * k / n))
            for k in range(n + 1)]
    return [Mark("node", pen, ring, c=(x, y), r=r + PEN_MM / 2.0)]


def rdisc(rx: float, ry: float, rr: float, pen: Optional[int], role: str = "node") -> List[Mark]:
    """A solid round mark by radius (r01's classes): r <= 0.32 mm becomes ONE round dot (r01
    drew it as a 2r hairline tick, i.e. a micro-dash); above that the same spiral disc r01
    drew with kit.fill_disc, at a 0.30 mm pitch (under the nib, so it inks solid; r01's
    0.45 mm left a visible spiral).  ``role='tex'`` marks the texture class (scatter, beads)."""
    x, y = P(rx, ry)
    r = L(rr)
    kind = "tex" if role == "tex" else "node"
    if r <= 0.32:
        return [Mark(kind, pen, _octagon(x, y), c=(x, y), r=DOT_INK, role=role)]
    return [Mark(kind, pen, _spiral(x, y, r, 0.30), c=(x, y), r=r + PEN_MM / 2.0, role=role)]


def rdotted(ref_pts: Sequence[Pt], pen: Optional[int], dash: float = 0.55, gap: float = 1.35,
            f: int = 2000, role: str = "guide") -> List[Mark]:
    """A dotted LINE.  r01's dash/gap are ignored on purpose: every dotted line on the plate
    becomes the family dot at DOT_PITCH, placed in the sheet pass (``_realize``)."""
    pts = PP(ref_pts)
    if len(pts) < 2:
        return []
    return [Mark("path", pen, pts, role=role, pid=_new("pid"))]


def rdot_run(xs: Sequence[float], ry: float, rr: float, pen: Optional[int]) -> List[Mark]:
    """The reference's '....' axis continuations: round filled dots, not dashes."""
    out: List[Mark] = []
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


def arrowhead(rx: float, ry: float, ang: float, size: float, pen: Optional[int]) -> List[Mark]:
    """Solid triangular arrowhead, tip at (rx, ry), pointing along ``ang`` (degrees in
    REFERENCE space, 0 = +x, 90 = down).  r01's outline + interior hatch, CHAINED into one
    pen-down: each hatch line starts on the edge where the last one ended, so every
    connector runs inside the inked triangle.

    This is the ONE place on these plates where an arrowhead is correct: in the backward
    band it marks gradient direction, not projection (A12, argued and accepted)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    half = size * 0.40
    tip = (rx, ry)
    b1 = (rx - ux * size + px * half, ry - uy * size + py * half)
    b2 = (rx - ux * size - px * half, ry - uy * size - py * half)
    path = [tip, b1, b2, tip]
    n = max(2, int(L(size) / 0.34))
    for i in range(1, n):
        t = i / n
        ax, ay = rx - ux * size * t, ry - uy * size * t
        hw = half * t
        e1, e2 = (ax + px * hw, ay + py * hw), (ax - px * hw, ay - py * hw)
        path += [e1, e2] if i % 2 else [e2, e1]
    pts = PP(path)
    return [Mark("arrow", pen, pts, c=P(rx - ux * size * 0.5, ry - uy * size * 0.5),
                 r=L(size) * 0.55)]


def cross(rx: float, ry: float, arm: float, pen: Optional[int]) -> List[Mark]:
    """Corner registration cross."""
    return rpoly([(rx - arm, ry), (rx + arm, ry)], pen) + rpoly([(rx, ry - arm), (rx, ry + arm)], pen)


def giant_type(text: str, x: float, y: float, height: float, pen: Optional[int] = None,
               weight: float = 0.0, tip: float = 0.55, angle: float = 0.0,
               f: int = 2200) -> List[Mark]:
    """kit.giant_type, same glyphs, same passes, same advance — but each glyph stroke's
    parallel passes are CHAINED into one pen-down (boustrophedon: pass k+1 starts where pass
    k ended, 0.26 mm across, inside the stroke band).  One label box per call."""
    sc = height / 6.0
    adv = 5.6 * sc
    passes = max(1, int(round(weight / max(tip, 0.05))) + 1) if weight > 0 else 1
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    lab = _new("label")

    def place(gx, gy, cursor):
        lx, ly = cursor - x + gx * sc, gy * sc
        return (x + lx * ca - ly * sa, y + lx * sa + ly * ca)

    out: List[Mark] = []
    cx = x
    for ch in text:
        strokes = _GLYPHS.get(ch)
        if strokes is None:
            strokes = _GLYPHS.get(ch.upper(), [])
        for stroke in strokes:
            if ch in "ij" and min(gy for _, gy in stroke) >= 4.9:
                # the tittle: at small caps it sits 1 glyph unit (0.32 mm at the subtitle
                # size) above the stem and fuses into it at a 0.35 mm nib ('i' reads 'l').
                # Keep it a dot, lifted just enough to leave GAP_SAME of paper (A11).
                gap = 1.0 * sc - PEN_MM
                lift = max(0.0, GAP_SAME - gap) / sc
                gx = sum(q[0] for q in stroke) / len(stroke)
                gy = 5.0 + lift + DOT_R / sc
                tx, ty = place(gx, gy, cx)
                out.append(Mark("type", pen, _octagon(tx, ty, max(DOT_R, 0.35 * sc)), label=lab))
                continue
            pts = [place(gx, gy, cx) for gx, gy in stroke]
            if passes == 1:
                chain = pts
            else:
                chain = []
                for k in range(passes):
                    d = -weight / 2.0 + weight * k / (passes - 1)
                    seq = _offset_polyline(pts, d)
                    chain += seq if k % 2 == 0 else seq[::-1]
            if len(chain) >= 2:
                out.append(Mark("type", pen, chain, label=lab))
        cx += adv
    return out


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
        # r04: the envelope stands ENV_LIFT mm off the crest tips it bounds.  Drawn exactly on
        # the tips (r01), 60 % of its dots sat within 0.3 mm of a crest and were invisible;
        # lifted 0.8 mm (inside J2's 1 mm), the dotted outline reads as its own line.
        off = ENV_LIFT / _S
        for run in _trim(up, y, floor):
            out += rdotted([(x, yy + off) for x, yy in run], pen, role="env")
        for run in _trim(dn, y, floor):
            out += rdotted([(x, yy - off) for x, yy in run], pen, role="env")
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
            lab = _new("label")
            for st in _PARTIAL:
                seq = [(x + gx * sc, y + gy * sc) for gx, gy in st]
                if weight > 0:   # r01's second pass, chained back along the stroke: one pen-down
                    seq = seq + [(px + weight, py) for px, py in seq][::-1]
                out.append(Mark("type", pen, seq, label=lab))
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
    return rpoly(pts, pen, kind="type")


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
            out += rdotted(gw, pen, dash=0.45, gap=0.95, role="ghost")

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


# v5's tonal field, MEASURED off gallery/studio/res_backprop/current/pp_res_backprop_v5.png
# (NOTES.md § Measurements).  Reference px, the plate's own frame.
V5_CREST_M = range(10, 74, 3)          # 22 dotted crest rings per source, m = 10 .. 73
V5_CLIP_A, V5_CLIP_B = 352.0, 128.0    # the crest arcs live inside this ellipse at (IF_CX, IF_CY)
V5_HALO_A = (196.0, 245.5, 300.0)      # three dotted halo ellipses centred on EACH source
V5_HALO_K = 0.40                       # b = 0.40 a


def interference(pen: Optional[int], rng: SeededRNG) -> List[Mark]:
    """The hero, computed as a real two-source field.

    Huygens construction: a crest of the wave from source s is the locus r_s = m * L.
    Drawing both crest families is exactly cos(k r1) = 1 and cos(k r2) = 1 with
    k = 2 pi / L -- the RIDGE lines of A = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2).

    r01's solid construction (bullseyes m 1-9, the comb m 10-50 inside the lens, both through
    the crossing-safe ``_Guard``) is unchanged, stroke for stroke.  What changed is the TONE
    around it: v8's dashed crest oval is gone and v5's field is back, measured — dotted crest
    arcs m = 10..73 step 3 inside the (352 x 128) ellipse, plus three dotted halo ellipses per
    source — every one of them a dotted LINE at the family pitch.
    """
    bk = pen
    out: List[Mark] = []

    n_lam = 59
    lam = IF_D / n_lam                      # 5.97 ref px = 1.04 mm on A4
    R_BULL = 9.0 * lam
    LENS_A, LENS_B = 100.0, 40.0
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
        nonlocal sid
        sid += 1
        res: List[Mark] = []
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
                    res += (rdotted(run, bk, role="field") if dotted else rpoly(run, bk, f=2600))
                run = []
        if len(run) >= 4:
            res += (rdotted(run, bk, role="field") if dotted else rpoly(run, bk, f=2600))
        return res

    def in_clip(px: float, py: float) -> bool:
        return ((px - IF_CX) / V5_CLIP_A) ** 2 + ((py - IF_CY) / V5_CLIP_B) ** 2 <= 1.0

    for sx in (SRC_L, SRC_R):
        # 1. the SOLID bullseye (r01, unchanged)
        for m in range(1, 10):
            out += emit(ring(sx, m * lam), lambda px, py: True, False)
        # 2. the SOLID comb in the lens (r01, unchanged)
        for m in range(10, 51):
            out += emit(ring(sx, m * lam), in_lens, False)
        # 3. v5's DOTTED crest arcs (measured): m = 10..73 step 3 inside the clip ellipse
        for m in V5_CREST_M:
            out += emit(
                ring(sx, m * lam, dense=False),
                lambda px, py: in_clip(px, py) and not in_bull(px, py, 5.0) and not in_lens(px, py),
                True,
            )

    # --- v5's dotted halo ellipses: three per source, centred on the source (measured) ------
    for sx in (SRC_L, SRC_R):
        for a in V5_HALO_A:
            b = a * V5_HALO_K
            rr = [
                (sx + a * math.cos(2 * math.pi * t / 240),
                 IF_CY + b * math.sin(2 * math.pi * t / 240))
                for t in range(241)
            ]
            runs: List[List[Pt]] = []
            cur: List[Pt] = []
            for q in rr:
                if (_BX0 + 2 < P(*q)[0] < _BX1 - 2 and not in_bull(q[0], q[1], 10.0)
                        and not in_lens(q[0], q[1])):
                    cur.append(q)
                else:
                    if len(cur) > 3:
                        runs.append(cur)
                    cur = []
            if len(cur) > 3:
                runs.append(cur)
            for run in runs:
                out += rdotted(run, bk, role="field")

    # --- the horizontal axis through the figure (r01) ----------------------
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

    # --- TEXTURE: the beaded dot columns and r01's 10 seeded scatter discs (r01, unchanged
    #     positions and radii; each one round dot or one solid disc) ----------
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
        return rdisc(px, py, r, bk, role="tex")

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

    # --- vertical dotted droplines, up and down (r01) ------------------------
    for j, x in enumerate(DROPS):
        top = 330.0 if x in (383.0, 560.0, 735.0) else 356.0
        out += rdotted([(x, top), (x, IF_CY - 6.0)], bk, role="drop")
        out += rdisc(x, top - 8.0, 2.0, bk)
        bot = 664.0 if j % 2 == 0 else 640.0
        out += rdotted([(x, IF_CY + 6.0), (x, bot)], bk, role="drop")
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
    out += rdotted(ghost, pen, dash=0.4, gap=1.5, role="ghost")

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
        out += rdotted(gw, pen, dash=0.45, gap=0.95, role="ghost")
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
        out += rdotted(run, pen, dash=0.85, gap=1.05, role="env")

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
        out += rdotted(pts, pen, dash=0.85, gap=1.15, role="fan")
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
        out += rdotted(run, pen, dash=0.85, gap=1.05, role="env")
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
    out += rdotted(ghost, pen, dash=0.4, gap=1.5, role="ghost")
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
                   pen, dash=0.6, gap=1.5, role="fan")
    out += rdotted([(700.0, DZ_Y), (874.0, DZ_Y)], pen, dash=0.6, gap=1.5, role="fan")
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
        out += rdotted(pts, green, dash=0.8, gap=1.5, role="fan")
        out += arrowhead(pts[-1][0], pts[-1][1], ang, 10.0, green)
    for way, ang in DA_FAN:
        pts = _spline(way, n_per=28)
        out += rdotted(pts, black, dash=0.8, gap=1.5, role="fan")
        out += arrowhead(pts[-1][0], pts[-1][1], ang, 10.0, black)
    for way, ang in DQ_FAN:
        pts = _spline(way, n_per=28)
        out += rdotted(pts, red, dash=0.8, gap=1.5, role="fan")
        out += arrowhead(pts[-1][0], pts[-1][1], ang, 10.0, red)
        mway = [(_mirror(a), b) for a, b in way]
        mpts = _spline(mway, n_per=28)
        out += rdotted(mpts, blue, dash=0.8, gap=1.5, role="fan")
        out += arrowhead(mpts[-1][0], mpts[-1][1], 180.0 - ang, 10.0, blue)
    # the long returns that climb out of the backward band into the forward half
    out += rdotted(_spline([(451, 1046), (420, 1010), (392, 970), (386, 930), (392, 900)]),
                   green, dash=0.8, gap=1.5, role="fan")
    out += arrowhead(392.0, 894.0, -90.0, 10.0, green)
    out += rdotted(_spline([(672, 1046), (704, 1010), (730, 970), (736, 930), (730, 900)]),
                   green, dash=0.8, gap=1.5, role="fan")
    out += arrowhead(730.0, 894.0, -80.0, 10.0, green)
    # blue / red long sweeps across the band
    out += rdotted(_spline([(700, 1046), (790, 1054), (872, 1078), (924, 1104), (952, 1132)]),
                   blue, dash=0.8, gap=1.5, role="fan")
    out += arrowhead(952.0, 1132.0, 45.0, 10.0, blue)
    out += rdotted(_spline([(420, 1046), (330, 1054), (248, 1078), (196, 1104), (168, 1132)]),
                   red, dash=0.8, gap=1.5, role="fan")
    out += arrowhead(168.0, 1132.0, 135.0, 10.0, red)
    return out



# ---------------------------------------------------------------------------
# SHEET PASS 1 — realise every dotted PATH as family dots, dropping only invisible ones.
# ---------------------------------------------------------------------------

STATS: Dict[str, int] = {}


class _SegGrid:
    """Ink centrelines with their half-width, bucketed on a 1 mm grid, for 'how much paper is
    left between this dot and that ink' queries."""

    def __init__(self, cell: float = 1.0) -> None:
        self.cell = cell
        self.g: Dict[Tuple[int, int], List[int]] = {}
        self.segs: List[Tuple[float, float, float, float, float]] = []

    def add_poly(self, pts: Sequence[Pt], hw: float) -> None:
        if len(pts) == 1:
            self._add(pts[0], pts[0], hw)
        for a, b in zip(pts[:-1], pts[1:]):
            self._add(a, b, hw)

    def _add(self, a: Pt, b: Pt, hw: float) -> None:
        i = len(self.segs)
        self.segs.append((a[0], a[1], b[0], b[1], hw))
        c = self.cell
        for gx in range(int(math.floor((min(a[0], b[0]) - hw) / c)),
                        int(math.floor((max(a[0], b[0]) + hw) / c)) + 1):
            for gy in range(int(math.floor((min(a[1], b[1]) - hw) / c)),
                            int(math.floor((max(a[1], b[1]) + hw) / c)) + 1):
                self.g.setdefault((gx, gy), []).append(i)

    def gap(self, x: float, y: float, reach: float) -> float:
        """Paper between (x, y) and the nearest ink edge (negative = inside ink)."""
        c = self.cell
        best = 1e9
        seen = set()
        for gx in range(int(math.floor((x - reach) / c)), int(math.floor((x + reach) / c)) + 1):
            for gy in range(int(math.floor((y - reach) / c)), int(math.floor((y + reach) / c)) + 1):
                for i in self.g.get((gx, gy), ()):
                    if i in seen:
                        continue
                    seen.add(i)
                    ax, ay, bx, by, hw = self.segs[i]
                    dx, dy = bx - ax, by - ay
                    L2 = dx * dx + dy * dy
                    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / L2))
                    d = math.hypot(x - ax - t * dx, y - ay - t * dy) - hw
                    if d < best:
                        best = d
        return best


class _DotGrid:
    def __init__(self, cell: float = 1.0) -> None:
        self.cell = cell
        self.g: Dict[Tuple[int, int], List[Tuple[float, float, float, float, int]]] = {}

    def add(self, x: float, y: float, tx: float, ty: float, pid: int) -> None:
        self.g.setdefault((int(math.floor(x / self.cell)), int(math.floor(y / self.cell))),
                          []).append((x, y, tx, ty, pid))

    def near(self, x: float, y: float, reach: float):
        c = self.cell
        for gx in range(int(math.floor((x - reach) / c)), int(math.floor((x + reach) / c)) + 1):
            for gy in range(int(math.floor((y - reach) / c)), int(math.floor((y + reach) / c)) + 1):
                for d in self.g.get((gx, gy), ()):
                    if (d[0] - x) ** 2 + (d[1] - y) ** 2 <= reach * reach:
                        yield d


def _resample(pts: Sequence[Pt], step: float = 0.25) -> Tuple[np.ndarray, np.ndarray]:
    a = np.asarray(pts, float)
    seg = np.hypot(*np.diff(a, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    L_ = cum[-1]
    n = max(2, int(math.ceil(L_ / step)) + 1)
    s = np.linspace(0.0, L_, n)
    xy = np.stack([np.interp(s, cum, a[:, 0]), np.interp(s, cum, a[:, 1])], axis=1)
    return xy, s


def _dot_positions(pts: Sequence[Pt], pen, pid: int, dots: "_DotGrid", blocked=None
                   ) -> List[Tuple[float, float, float, float]]:
    """End-anchored dots every DOT_PITCH along ``pts``; where an already-dotted same-pen path
    runs within LOCK_DIST and within 25 deg of parallel, its dots become ANCHORS (this path's
    dots sit opposite them) and the stretches between anchors are filled end-anchored.

    The path is first TRIMMED at both ends past whatever it runs into (a node, an arrowhead,
    a label box, same-pen ink), so the end anchors land on the first and last VISIBLE
    positions: a leader ends one clean gap short of its arrowhead, with a dot."""
    xy, s = _resample(pts)
    if blocked is not None:
        i0, i1 = 0, len(s) - 1
        while i0 <= i1 and blocked(xy[i0, 0], xy[i0, 1]):
            i0 += 1
        while i1 >= i0 and blocked(xy[i1, 0], xy[i1, 1]):
            i1 -= 1
        if i1 < i0:
            return []
        xy, s = xy[i0:i1 + 1], s[i0:i1 + 1] - s[i0]
        if len(s) < 2:
            return [(float(xy[0, 0]), float(xy[0, 1]), 1.0, 0.0)]
    L_ = float(s[-1])
    tang = np.gradient(xy, axis=0)
    tn = np.hypot(tang[:, 0], tang[:, 1])
    tn[tn < 1e-12] = 1.0
    tang = tang / tn[:, None]
    if L_ < 0.6:
        i = len(s) // 2
        return [(xy[i, 0], xy[i, 1], tang[i, 0], tang[i, 1])]
    anchors: List[float] = []
    cand = {}
    for i in range(0, len(s), 4):
        for d in dots.near(xy[i, 0], xy[i, 1], LOCK_DIST):
            if d[4] != pid:
                cand[(round(d[0], 4), round(d[1], 4))] = d
    for d in cand.values():
        dd = np.hypot(xy[:, 0] - d[0], xy[:, 1] - d[1])
        i = int(np.argmin(dd))
        if dd[i] > LOCK_DIST:
            continue
        if abs(tang[i, 0] * d[2] + tang[i, 1] * d[3]) < LOCK_COS:
            continue
        anchors.append(float(s[i]))
    anchors = sorted(a for a in anchors if 0.5 < a < L_ - 0.5)
    bps = [0.0]
    for a in anchors:
        if a - bps[-1] >= 0.6:
            bps.append(a)
    if L_ - bps[-1] < 0.6 and len(bps) > 1:
        bps.pop()
    bps.append(L_)
    ss: List[float] = []
    for a, b in zip(bps[:-1], bps[1:]):
        n = max(1, int(round((b - a) / DOT_PITCH)))
        ss += [a + (b - a) * j / n for j in range(n)]
    ss.append(L_)
    out = []
    for v in ss:
        i = min(len(s) - 1, int(np.searchsorted(s, v)))
        x = float(np.interp(v, s, xy[:, 0]))
        y = float(np.interp(v, s, xy[:, 1]))
        out.append((x, y, float(tang[i, 0]), float(tang[i, 1])))
    STATS["anchored_paths"] = STATS.get("anchored_paths", 0) + (1 if anchors else 0)
    return out


def _realize(marks: List[Mark]) -> List[Mark]:
    solid = [m for m in marks if m.kind != "path"]
    paths = [m for m in marks if m.kind == "path"]
    pens = sorted({m.pen for m in marks}, key=lambda p: (p is None, p))

    same: Dict[Optional[int], _SegGrid] = {p: _SegGrid() for p in pens}
    other: Dict[Optional[int], _SegGrid] = {p: _SegGrid() for p in pens}
    for m in solid:
        same[m.pen].add_poly(m.pts, PEN_MM / 2.0)
        for p in pens:
            if p != m.pen:
                other[p].add_poly(m.pts, PEN_MM / 2.0)
    for m in paths:   # the field yields to every other pen's leaders, as centrelines
        for p in pens:
            if p != m.pen:
                other[p].add_poly(m.pts, DOT_INK)

    nodes = [m for m in solid if m.kind in ("node", "tex", "arrow")]
    node_g: Dict[Tuple[int, int], List[Mark]] = {}
    for m in nodes:
        rr = m.r + DOT_INK + GAP_NODE
        for gx in range(int(math.floor((m.c[0] - rr) / 2.0)), int(math.floor((m.c[0] + rr) / 2.0)) + 1):
            for gy in range(int(math.floor((m.c[1] - rr) / 2.0)), int(math.floor((m.c[1] + rr) / 2.0)) + 1):
                node_g.setdefault((gx, gy), []).append(m)

    # label boxes: exact geometry Rect / Union, one box per type run + HALO_PAD
    by_label: Dict[int, List[Pt]] = {}
    for m in solid:
        if m.kind == "type":
            by_label.setdefault(m.label, []).extend(m.pts)
    boxes = []
    for pts in by_label.values():
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        boxes.append((min(xs) - HALO_PAD, min(ys) - HALO_PAD, max(xs) + HALO_PAD, max(ys) + HALO_PAD))
    labels = Union(*[Rect(*b) for b in boxes]) if boxes else None
    box_g: Dict[Tuple[int, int], List[int]] = {}
    for i, b in enumerate(boxes):
        for gx in range(int(b[0] // 5), int(b[2] // 5) + 1):
            for gy in range(int(b[1] // 5), int(b[3] // 5) + 1):
                box_g.setdefault((gx, gy), []).append(i)

    def in_label(x: float, y: float) -> bool:
        hit = box_g.get((int(x // 5), int(y // 5)))
        if not hit:
            return False
        return Union(*[labels.rs[i] for i in hit]).contains(x, y)

    def on_node(x: float, y: float) -> bool:
        for m in node_g.get((int(math.floor(x / 2.0)), int(math.floor(y / 2.0))), ()):
            if math.hypot(x - m.c[0], y - m.c[1]) < m.r + DOT_INK + GAP_NODE:
                return True
        return False

    dots: Dict[Optional[int], _DotGrid] = {p: _DotGrid() for p in pens}
    out: List[Mark] = list(solid)
    order = sorted(range(len(paths)), key=lambda i: (paths[i].role == "field", i))
    for k in ("dots_kept", "drop_label", "drop_node", "drop_ink", "drop_dup", "drop_field"):
        STATS[k] = 0
    for i in order:
        m = paths[i]

        def blocked(x: float, y: float, m=m) -> bool:
            return ((labels is not None and in_label(x, y)) or on_node(x, y)
                    or same[m.pen].gap(x, y, 1.2) - DOT_INK < GAP_SAME)

        for x, y, tx, ty in _dot_positions(m.pts, m.pen, m.pid, dots[m.pen], blocked):
            if labels is not None and in_label(x, y):
                STATS["drop_label"] += 1
                STATS["drop_label_" + m.role] = STATS.get("drop_label_" + m.role, 0) + 1
                continue
            if on_node(x, y):
                STATS["drop_node"] += 1
                STATS["drop_node_" + m.role] = STATS.get("drop_node_" + m.role, 0) + 1
                continue
            if same[m.pen].gap(x, y, 1.2) - DOT_INK < GAP_SAME:
                STATS["drop_ink"] += 1
                STATS["drop_ink_" + m.role] = STATS.get("drop_ink_" + m.role, 0) + 1
                continue
            if any(d[4] != m.pid for d in dots[m.pen].near(x, y, 2 * DOT_INK)):
                STATS["drop_dup"] += 1
                STATS["drop_dup_" + m.role] = STATS.get("drop_dup_" + m.role, 0) + 1
                continue
            if m.role == "field" and other[m.pen].gap(x, y, 1.5) - DOT_INK < GAP_FIELD:
                STATS["drop_field"] += 1
                STATS["drop_field_" + m.role] = STATS.get("drop_field_" + m.role, 0) + 1
                continue
            dots[m.pen].add(x, y, tx, ty, m.pid)
            out.append(Mark("dot", m.pen, _octagon(x, y), c=(x, y), r=DOT_INK, role=m.role,
                            pid=m.pid))
            STATS["dots_kept"] += 1
            STATS["dots_" + m.role] = STATS.get("dots_" + m.role, 0) + 1
    return out


# ---------------------------------------------------------------------------
# SHEET PASS 2 — stream order.  Per pen (pens in index order = light -> dark): a serpentine
# sweep of CELL_MM cells, bottom row first (the head parks at (0, 0), bottom-left), with a
# reversal-aware nearest-end walk inside each cell.  So consecutive strokes are neighbours
# and any 400-stroke batch is one contiguous region of the sheet.
# ---------------------------------------------------------------------------


def _order(marks: List[Mark]) -> List[Mark]:
    by_pen: Dict[Optional[int], List[Mark]] = {}
    for m in marks:
        by_pen.setdefault(m.pen, []).append(m)
    out: List[Mark] = []
    pos = np.array([0.0, 0.0])
    for pen in sorted(by_pen, key=lambda p: (p is None, p)):
        items = by_pen[pen]
        cells: Dict[Tuple[int, int], List[Mark]] = {}
        for m in items:
            xs = [p[0] for p in m.pts]
            ys = [p[1] for p in m.pts]
            cx, cy = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0
            cells.setdefault((int(cy // CELL_MM), int(cx // CELL_MM)), []).append(m)
        rows = sorted({r for r, _ in cells})

        def seq():
            # serpentine, but each row is entered from whichever end is nearer the head
            for r in rows:
                cols = sorted(c for rr, c in cells if rr == r)
                left = (cols[0] + 0.5) * CELL_MM
                right = (cols[-1] + 0.5) * CELL_MM
                if abs(pos[0] - right) < abs(pos[0] - left):
                    cols = cols[::-1]
                for c in cols:
                    yield (r, c)

        for key in seq():
            rest = cells[key]
            p0 = np.array([m.pts[0] for m in rest])
            p1 = np.array([m.pts[-1] for m in rest])
            alive = np.ones(len(rest), bool)
            for _ in range(len(rest)):
                d0 = np.hypot(*(p0 - pos).T)
                d1 = np.hypot(*(p1 - pos).T)
                d0[~alive] = np.inf
                d1[~alive] = np.inf
                i0, i1 = int(np.argmin(d0)), int(np.argmin(d1))
                if d0[i0] <= d1[i1]:
                    m = rest[i0]
                    alive[i0] = False
                else:
                    m = rest[i1]
                    alive[i1] = False
                    m = Mark(m.kind, m.pen, m.pts[::-1], m.c, m.r, m.label, m.role, m.pid)
                out.append(m)
                pos = np.array(m.pts[-1])
    return out


def _emit(marks: Sequence[Mark]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for m in marks:
        out += _poly(m.pts, color=m.pen, f=1200 if m.kind == "dot" else 2000)
    return out


# ---------------------------------------------------------------------------


def build_marks(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[Mark]:
    """r01's plate, block for block, in r01's order — as marks."""
    _fit(bounds)
    _IDS["label"] = 0
    _IDS["pid"] = 0

    def p(i: int) -> Optional[int]:
        return i % colors if colors > 1 else None

    red, blue, ochre, green, black = (p(RED), p(BLUE), p(OCHRE), p(GREEN), p(BLACK))

    out: List[Mark] = []
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


def plate_marks(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[Mark]:
    STATS.clear()
    return _order(_realize(build_marks(rng, bounds, colors)))


def attention_as_resonance(
    rng: SeededRNG, bounds: Bounds, colors: int = 5
) -> List[GCodeCommand]:
    return _emit(plate_marks(rng, bounds, colors))
