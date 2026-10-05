"""ATTENTION AS RESONANCE — r06 "iterate" (parent r10 = r01/v13 + Juan's continuous dots).

v13 is the design (Juan, 2026-09-28: "the original was much more beautiful — we
just needed the dot lines to be more continuous, not to remove the waves").  So
every element, every position and all six pens are r10's, which are r01's, which
were traced off ``studio/resonance/ref/attention-as-resonance.png``
(1122 x 1402 px).  What this round changes is HOW marks are made and HOW the
sheet streams:

* **Stroke IR** (from r05).  Every helper registers geometry on the sheet — solid
  ``Stroke``s, dotted ``DotPath``s and dot ``texture``s — and nothing becomes
  G-code until three sheet passes have run: halos, the dot resolver, the tour.
* **Two dot classes.**  DOTTED LINES (fans, guides, droplines, leaders, rails,
  ghost lanes, halo ellipses, backward runs, return curves) are round dots at a
  1.0 mm end-anchored pitch (r10's).  TEXTURES (the crest fade m = 22..51 that
  forms the stipple caps; the |A| spoke field and the 60 scatter marks) keep
  v13's own mark positions — one round dot per v13 mark, never re-pitched.
* **The dot resolver** (sheet pass).  A dot is placed only where it is VISIBLE:
  not within 0.55 mm of same-pen solid ink, not within 0.6 mm of another
  same-pen dot, not in a label halo, not on a node.  Where two same-pen dotted
  paths run within 2 mm, the later path is PHASE-LOCKED to the earlier one (its
  dots anchor on the projections of the earlier path's dots).  A dot that falls
  on ink is slid <= 0.35 mm along its own path into the nearest clear gap, so a
  dropline crossing the crest net puts its dots BETWEEN crests.
* **The tour** (sheet pass).  Each pen is ordered by a reversal- and
  rotation-aware nearest-neighbour walk from (0, 0), and each stroke is emitted
  already oriented.  ``postprocess.reorder_by_color`` runs a plain nearest-start
  walk; on a stroke set oriented this way it provably reproduces the same order
  (every step's chosen start is the nearest of ALL remaining ends), so the
  order computed here is the order Leo draws.
* r05's non-destructive craft: label halos, node keep-outs, the carrier IS the
  axis (no co-incident duplicate ink), fused weighted type, round solid dots
  (touch / loop / spiral), the dL stack at 10 mm pitch / 3 mm clear air.
* Collisions fixed without deleting: V rows occluded (a lower packet hides under
  the upper row's envelope), the word ``router`` haloed, the three Z taps end ON
  their dL return curves, every softmax -> Z link and V's connector end ON Z's
  axis (kept gold: a_j V_j flowing into Z).

Pens — palette index = stream order, light -> dark:
0 goldenrod V · 1 dodgerblue K · 2 forestgreen Z · 3 crimson Q ·
4 darkviolet MoE / Y / their gradients · 5 black field, softmax, type, dL/dA.

Lineage: Thomas Young, *Lectures on Natural Philosophy* (1807), Plate XX
Fig. 267 — interfering: two concentric crest families, the result is where they
cross.

The maths (v13, unchanged)
--------------------------
WAVE PACKET  f(x) = SUM A_i exp(-((x-c_i)/s_i)^2) cos(2 pi (x-c_i)/L_i + p_i),
envelope env(x) = SUM A_i exp(-((x-c_i)/s_i)^2).
INTERFERENCE  ridge lines of A = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2): crest
loci r_s = m L, d = 35 L, crests 1..21 solid, 22..51 the dotted fade, parallel
guard 0.82 mm / 25 deg.

Entry point: ``attention_resonance_iterate``.
"""

from __future__ import annotations

import math
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, Union, clip
from promptplot.generative.kit import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

REF_W, REF_H = 1122.0, 1402.0

# pen slots in STREAM order (light -> dark); the family grammar is by colour
OCHRE, BLUE, GREEN, RED, PURPLE, BLACK = 0, 1, 2, 3, 4, 5
PALETTE = "goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black"

PEN_MM = 0.35            # the nib the plate is drawn for
DOT_PITCH = 1.0          # dotted LINES: centre-to-centre, end-anchored (r10, J1)
DOT_INK_R = 0.275        # every dot is one loop of r = 0.10 -> inked disc of r 0.275
LOCK_DIST = 2.0          # same-pen paths closer than this are phase-locked
CLEAR_INK = 0.55         # dot centre to same-pen solid centreline (0.1 mm of paper)
CLEAR_DOT = 0.60         # dot centre to another same-pen dot centre
SNAP = 0.35              # how far a dot may slide along its path into a gap
NODE_PAD = 0.55          # clear paper a dot keeps from any node
HALO_PAD = 0.9           # clear paper around every label
ENV_RHYTHM = (1.3, 2.4)  # envelope dash / period mm (v13 period 2.4; dash out of the dot range)
AXIS_ENV_MM = 0.25       # the axis is drawn under a packet where env >= this

RES = 0.1                # resolver raster, mm per cell


class Stroke(NamedTuple):
    pts: List[Pt]
    pen: Optional[int]
    kind: str        # "type" | "line" | "disc" | "dash" | "dot"
    f: int


class DotPath(NamedTuple):
    pts: List[Pt]           # polyline, mm
    pen: Optional[int]
    name: str
    prio: int               # resolver order (lower first)
    anchors: Tuple[Pt, ...]  # points (on the path) that must carry a dot
    corners: bool           # every interior vertex carries a dot


# ---------------------------------------------------------------------------
# the sheet: mapping + registries
# ---------------------------------------------------------------------------


class _Map:
    """Reference pixels -> sheet millimetres, plus everything registered on the sheet."""

    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.sx = (x1 - x0) / REF_W
        self.sy = (y1 - y0) / REF_H
        self.halos: List[Tuple[float, float, float, float]] = []
        self.nodes: List[Tuple[float, float, float]] = []
        self.strokes: List[Stroke] = []
        self.field: List[Tuple[float, float, float]] = []   # (cx, cy, r) mm, v13's dot field
        self.paths: List[DotPath] = []
        self.textures: List[Tuple[str, Optional[int], List[Pt]]] = []
        self.stats: Dict[str, float] = {}

    def p(self, px: float, py: float) -> Pt:
        return (self.x0 + px * self.sx, self.y1 - py * self.sy)

    def s(self, v: float) -> float:
        return v * self.sx

    def halo(self, strokes: Sequence[Stroke], pad: float = HALO_PAD) -> None:
        xs = [x for st in strokes for x, _ in st.pts]
        ys = [y for st in strokes for _, y in st.pts]
        if xs:
            self.halos.append((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))

    # registration ---------------------------------------------------------
    def add(self, strokes: Sequence[Stroke]) -> List[Stroke]:
        self.strokes.extend(strokes)
        return list(strokes)

    def dotline(self, pts: Sequence[Pt], pen, name: str, prio: int = 5,
                anchors: Sequence[Pt] = (), corners: bool = False) -> None:
        pts = [p for p in pts if p is not None]
        if len(pts) >= 2:
            self.paths.append(DotPath(list(pts), pen, name, prio, tuple(anchors), corners))

    def dotline_px(self, pts_px, pen, name: str, prio: int = 5, anchors_px=(),
                   corners: bool = False) -> None:
        self.dotline([self.p(x, y) for x, y in pts_px], pen, name, prio,
                     [self.p(x, y) for x, y in anchors_px], corners)

    def texture(self, pts: Sequence[Pt], pen, name: str) -> None:
        self.textures.append((name, pen, list(pts)))


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# stroke primitives (mm)
# ---------------------------------------------------------------------------


def _S(pts: Sequence[Pt], pen, kind: str = "line", f: int = 2000) -> List[Stroke]:
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    return [Stroke(list(pts), pen, kind, f)]


def _disc_mm(cx: float, cy: float, r: float, pen, kind: str = "disc") -> List[Stroke]:
    """A round solid dot of inked radius ``r`` for a PEN_MM nib, one pen-down.
    touch (r <= nib/2 + 0.08) · one loop (r <= nib) · spiral at 0.25 mm pitch."""
    h = PEN_MM / 2.0
    if r <= h + 0.08:
        return _S([(cx - 0.03, cy), (cx + 0.03, cy)], pen, kind, 1200)
    if r <= 2 * h:
        rr = r - h
        return _S([(cx + rr * math.cos(2 * math.pi * k / 10), cy + rr * math.sin(2 * math.pi * k / 10))
                   for k in range(11)], pen, kind, 1200)
    turns = max(2, int(math.ceil((r - h) / 0.25)) + 1)
    n = turns * 24
    pts = []
    for k in range(n + 1):
        t = k / n
        rr = (r - h) * (1.0 - t)
        a = 2 * math.pi * turns * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _S(pts, pen, kind, 1600)


def _dot_mark(cx: float, cy: float, pen) -> List[Stroke]:
    """THE dot of every dotted line and texture: one fixed round mark."""
    return _disc_mm(cx, cy, DOT_INK_R, pen, "dot")


def _circle_mm(cx: float, cy: float, r: float, pen, n: int = 40) -> List[Stroke]:
    return _S([(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
               for k in range(n + 1)], pen, "line", 2000)


def _cum(pts: Sequence[Pt]) -> List[float]:
    c = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        c.append(c[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return c


def _at(pts, cum, s: float) -> Pt:
    lo, hi = 0, len(cum) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cum[mid] <= s:
            lo = mid
        else:
            hi = mid
    seg = cum[hi] - cum[lo]
    t = 0.0 if seg < 1e-12 else (s - cum[lo]) / seg
    a, b = pts[lo], pts[hi]
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _sub(pts, cum, a: float, b: float) -> List[Pt]:
    out = [_at(pts, cum, a)]
    for p, s in zip(pts, cum):
        if a < s < b:
            out.append(p)
    out.append(_at(pts, cum, b))
    return out


def _dashed_mm(pts: Sequence[Pt], rhythm: Tuple[float, float], pen) -> List[Stroke]:
    """Dashes spread evenly: n = round(len / period), each centred in its slot —
    no stub at either end.  Used only for the packet envelope."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    cum = _cum(pts)
    L = cum[-1]
    dash, period = rhythm
    if L < dash:
        return []
    n = max(1, int(round(L / period)))
    p = L / n
    out: List[Stroke] = []
    for k in range(n):
        c = (k + 0.5) * p
        out += _S(_sub(pts, cum, max(0.0, c - dash / 2), min(L, c + dash / 2)), pen, "dash", 2000)
    return out


def _line(M: _Map, pts_px, pen, f: int = 2000) -> List[Stroke]:
    return M.add(_S([M.p(x, y) for x, y in pts_px], pen, "line", f))


def _ocirc(M: _Map, px: float, py: float, r_px: float, pen, n: int = 40) -> List[Stroke]:
    cx, cy = M.p(px, py)
    M.nodes.append((cx, cy, M.s(r_px) + NODE_PAD))
    return M.add(_circle_mm(cx, cy, M.s(r_px), pen, n=n))


def _fdot(M: _Map, px: float, py: float, r_px: float, pen) -> List[Stroke]:
    cx, cy = M.p(px, py)
    r = M.s(r_px)
    if r >= 0.4:
        M.nodes.append((cx, cy, r + NODE_PAD))
    return M.add(_disc_mm(cx, cy, r, pen))


def _lead_dots(M: _Map, x_from: float, step: float, n: int, y: float, r: float, pen):
    for k in range(n):
        _fdot(M, x_from + step * k, y, r, pen)


def _bez(p0, c1, c2, p1, n: int = 64):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append((u * u * u * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * p1[0],
                    u * u * u * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * p1[1]))
    return out


def _arrow(M: _Map, px: float, py: float, direction: int, size_px: float, pen) -> List[Stroke]:
    """v13's solid arrowhead (the dL band keeps its arrowheads, J2) drawn as ONE
    pen-down: the outline, then a boustrophedon fill that only ever moves inside
    the triangle.  v13 drew it as 1 + 5 separate strokes."""
    cx, cy = M.p(px, py)
    L = M.s(size_px)
    hb = L * 0.62
    d = direction
    path = [(cx, cy), (cx - d * L, cy + hb), (cx - d * L, cy - hb), (cx, cy)]
    n = max(2, int(hb * 2 / 0.25))
    for i in range(1, n):
        yy = -hb + 2 * hb * i / n
        # v13 filled from (1 - |y|/hb) L, i.e. from the back edge to the back
        # edge at the axis: the head plotted with a notch.  The slanted edge
        # is at |y|/hb * L from the tip.
        xe = cx - d * L * (abs(yy) / hb)
        xb = cx - d * L
        path += [(xe, cy + yy), (xb, cy + yy)] if i % 2 else [(xb, cy + yy), (xe, cy + yy)]
    return M.add(_S(path, pen, "line", 1600))


# ---------------------------------------------------------------------------
# type — r01's letterforms; weight fused into one pen-down (r05)
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
    "@": [  # partial derivative
        [(1.3, 0.0), (0.4, 0.9), (0.4, 2.3), (1.3, 3.2), (2.5, 3.2), (3.3, 2.3), (3.3, 0.9), (2.5, 0.0), (1.3, 0.0)],
        [(3.3, 1.6), (3.3, 3.7), (2.9, 4.9), (2.0, 5.8), (0.8, 6.0)],
    ],
    "#": [[(0.0, 3.2), (0.7, 2.7), (1.6, 0.0), (2.8, 6.0), (5.4, 6.0)]],  # radical
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


def _weighted(pts: List[Pt], w: float) -> List[Pt]:
    """r01's weight offsets chained into ONE pen-down, passes <= 0.28 mm apart."""
    if w <= 0:
        return pts
    n = max(1, int(math.ceil(w / 0.28)))
    m = max(1, int(math.ceil(0.9 * w / 0.28)))
    offs = [(w * k / n, 0.0) for k in range(n + 1)] + [(w * 0.5, 0.9 * w * j / m) for j in range(1, m + 1)]
    path: List[Pt] = []
    for i, (ox, oy) in enumerate(offs):
        seq = [(x + ox, y + oy) for x, y in pts]
        path += seq if i % 2 == 0 else seq[::-1]
    return path


def _type(M: _Map, text: str, px: float, py: float, h_px: float, pen, tracking: float = 1.0,
          center: bool = False, weight: float = 0.0, f: int = 2200,
          halo: bool = True, register: bool = True) -> List[Stroke]:
    ax, ay = M.p(px, py)
    h = M.s(h_px)
    sc = h / 6.0
    adv = _ADV * sc * tracking
    if center:
        ax -= _tw(text, h, tracking) / 2.0
    out: List[Stroke] = []
    cx = ax
    for ch in text:
        if ch == ".":
            out += _disc_mm(cx + 2.0 * sc, ay + 0.25 * sc, max(0.28 * sc, 0.2), pen, "type")
        elif ch == "~":  # middle dot
            out += _disc_mm(cx + 2.0 * sc, ay + 2.6 * sc, max(0.55 * sc, 0.32), pen, "type")
        else:
            for st in _strokes(ch):
                pts = [(cx + gx * sc, ay + gy * sc) for gx, gy in st]
                out += _S(_weighted(pts, weight), pen, "type", f)
        cx += adv
    if halo:
        M.halo(out)
    if register:
        M.add(out)
    return out


def _frac(M: _Map, num: str, den: str, px: float, py: float, h_px: float, pen,
          tracking: float = 1.0, gap_px: float = 4.2) -> List[Stroke]:
    h = M.s(h_px)
    half = max(_tw(num, h, tracking), _tw(den, h, tracking)) / 2.0 + M.s(2.0)
    rx, ry = M.p(px, py)
    out: List[Stroke] = []
    out += _S([(rx - half, ry), (rx + half, ry)], pen, "type", 2000)
    out += _type(M, num, px, py - h_px * 0.42 - gap_px, h_px, pen, tracking=tracking,
                 center=True, halo=False, register=False)
    out += _type(M, den, px, py + h_px * 1.02 + gap_px, h_px, pen, tracking=tracking,
                 center=True, halo=False, register=False)
    M.halo(out)
    return M.add(out)


# ---------------------------------------------------------------------------
# the wave packet
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


def _runs(pts, keep) -> List[List]:
    out, cur = [], []
    for p, k in zip(pts, keep):
        if k:
            cur.append(p)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def wave_packet(M: _Map, x0: float, x1: float, y: float, packets: Sequence[Packet], pen,
                envelope: bool = True, ghost: bool = False, occ=None,
                name: str = "packet") -> None:
    """One row: the carrier node to node (the carrier IS the axis where the
    packet has decayed), the straight axis only UNDER the packet (so v13's axis
    still runs through every packet, but no ink is laid twice), and the dashed
    envelope above and below, split into its own runs (no chords).

    ``occ(x, y_px) -> bool`` hides points behind a row in front (V rows)."""
    lam_min = min(p[2] for p in packets)
    step = max(lam_min / 14.0, 0.18)
    n = int((x1 - x0) / step) + 1
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    curve = [(x, y - _pk_value(x, packets)) for x in xs]
    if ghost:
        M.dotline_px(curve, pen, name + ":ghost", prio=6)
        return
    vis = [True] * len(curve) if occ is None else [not occ(x, yy) for x, yy in curve]
    for run in _runs(curve, vis):
        _line(M, run, pen, f=2400)
    # the axis under the packet
    thr = AXIS_ENV_MM / M.sy
    under = [_pk_env(x, packets) >= thr for x in xs]
    for run in _runs(list(zip(xs, [y] * len(xs))), under):
        if len(run) >= 2:
            pts = [run[0], run[-1]]
            if occ is not None and (occ(*pts[0]) or occ(*pts[1])):
                continue
            _line(M, pts, pen)
    if envelope:
        for sgn in (-1.0, 1.0):
            env = [(x, y + sgn * _pk_env(x, packets)) for x in xs]
            keep = [abs(yy - y) > 3.2 and (occ is None or not occ(x, yy)) for x, yy in env]
            for r in _runs(env, keep):
                if len(r) > 3:
                    M.add(_dashed_mm([M.p(a, b) for a, b in r], ENV_RHYTHM, pen))


# ---------------------------------------------------------------------------
# layout constants — r01 / r10 (reference pixels)
# ---------------------------------------------------------------------------

TITLE_Y = 52.0
RULE_Y = 74.0

QK_ROWS = [164.0, 223.0, 282.0, 339.0, 396.0]
Q_HOME = 109.0
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
    (109.0, 128.0, 412.0),
    (207.0, 100.0, 300.0),
    (287.0, 108.0, 352.0),
    (315.0, 162.0, 420.0),
    (356.0, 212.0, 402.0),
    (389.0, 262.0, 432.0),
]

IF_CX, IF_CY = 561.0, 611.0
IF_D = 250.0
SRC_L, SRC_R = IF_CX - IF_D / 2, IF_CX + IF_D / 2

SOFT_BASE = 886.0
SOFT_PEAKS = [
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
V_PACKS: List[List[Packet]] = [
    [(903.0, 32.0, 12.5, 28.0, 0.0), (800.0, 17.0, 9.0, 12.0, 0.5)],
    [(862.0, 27.0, 11.5, 25.0, 0.0), (778.0, 15.0, 8.5, 13.0, 0.8)],
    [(878.0, 25.0, 14.0, 22.0, 0.0), (790.0, 14.0, 9.5, 11.0, 0.3)],
]
V_OCC_GAP_MM = 0.6    # a lower V row stops this far below the upper row's envelope

MOE_Y = 1073.0
ROUTER_X, NODE2_X = 527.0, 884.0
LANE_L, LANE_R = 611.0, 789.0
LANE_YS = [1010.0, 1044.0, 1073.0, 1103.0, 1148.0]
Z_L, Z_R = 110.0, ROUTER_X - 14.0          # Z's axis, px (28.6 .. 96.9 mm)

# softmax -> Z links now end ON Z's axis (S1a).  Three of them land where the
# Z taps leave the axis below, so a_j V_j visibly runs through Z into dL.
LINK_ENDS = [336.0, 356.0, 377.0, 396.0, 415.0, 430.0]
V_CONN_END = 466.0
V_CHANNEL_Y = 910.0      # the clear run between the softmax baseline (886) and the MoE header (929+)

# dL stack re-spaced (r05, critic-confirmed): 10 mm pitch, 3 mm clear air
BACK_ROWS = [1170.0, 1218.0, 1266.0, 1314.0, 1362.0]
BACK_H = 11.5
BACK_GAP = 3.0
BACK_COL = 282.0
TAPS = [(336.0, RED), (377.0, BLUE), (415.0, OCHRE)]


# ---------------------------------------------------------------------------
# sections
# ---------------------------------------------------------------------------


def _title(M: _Map, colors: int) -> None:
    bk = _pen(BLACK, colors)
    _type(M, "ATTENTION AS RESONANCE", 561.0, TITLE_Y, 20.0, bk, tracking=1.72, center=True,
          weight=0.24)
    M.add(_S([M.p(492.0, RULE_Y), M.p(630.0, RULE_Y)], bk, "type"))
    _fdot(M, 561.0, RULE_Y, 2.4, bk)


def _qk_block(M: _Map, colors: int, side: int, pen) -> None:
    def mx(x: float) -> float:
        return x if side > 0 else REF_W - x

    home = Q_HOME if side > 0 else K_HOME
    filled = Q_HOME_FILLED if side > 0 else K_HOME_FILLED
    tag = "Q" if side > 0 else "K"

    for i, y in enumerate(QK_ROWS):
        if side > 0:
            far, circ, tail = Q_ROWS[i][0], Q_ROWS[i][1], Q_ROWS[i][3]
            pk = Q_PACKETS[i]
        else:
            far, circ, tail = K_ROWS[i]
            pk = K_PACKETS[i]
        lo, hi = (home, far) if side > 0 else (far, home)
        wave_packet(M, lo, hi, y, pk, pen, name=f"{tag}{i}")
        if filled[i]:
            _fdot(M, home, y, 4.6, pen)
        else:
            _ocirc(M, home, y, 4.8, pen)
        if circ is not None:
            _ocirc(M, circ, y, 5.4, pen)
        if tail is not None:
            _fdot(M, tail, y, 3.4, pen)
        _lead_dots(M, home - side * 21.0, -side * 12.0, 4, y, 2.4, pen)

    for x, yt, yb in Q_VERTS:
        M.dotline_px([(mx(x), yt), (mx(x), yb)], pen, f"{tag}:guide", prio=3)
        _fdot(M, mx(x), yt - 6.0, 2.2, pen)

    lx = 92.0 if side > 0 else REF_W - 133.0
    _type(M, tag, lx, 124.0, 38.0, pen, weight=0.46)

    # the convergence fans — the plate's one gesture (resolved first)
    for i, y in enumerate(QK_ROWS):
        end_x = Q_ROWS[i][0] if side > 0 else REF_W - K_ROWS[i][0]
        x_start = mx(end_x + 12.0)
        tx = mx(408.0 + 15.0 * i)
        ty = 446.0 + 26.0 * i
        c1 = (mx(end_x + 86.0 + 16.0 * i), y + 10.0)
        c2 = (mx(492.0 + 6.0 * i), 352.0 + 20.0 * i)
        M.dotline_px(_bez((x_start, y), c1, c2, (tx, ty)), pen, f"{tag}:fan{i}a", prio=0)
        _fdot(M, tx, ty, 3.0, pen)
        c1b = (mx(end_x + 128.0 + 20.0 * i), y + 18.0)
        c2b = (mx(524.0 + 8.0 * i), 366.0 + 20.0 * i)
        tx2, ty2 = mx(386.0 + 13.0 * i), 470.0 + 24.0 * i
        M.dotline_px(_bez((x_start, y + 6.0), c1b, c2b, (tx2, ty2)), pen, f"{tag}:fan{i}b", prio=0)
        _fdot(M, tx2, ty2, 2.2, pen)


def _centre_fraction(M: _Map, colors: int) -> None:
    bk = _pen(BLACK, colors)
    for j in range(3):
        _fdot(M, 561.0, 332.0 + 11.0 * j, 1.7, bk)
    h = 23.0
    num = "Q~K"
    tr = 1.16
    wn_px = _tw(num, M.s(h), tr) / M.sx
    nx = 561.0 - 5.0
    g: List[Stroke] = []
    g += _type(M, num, nx, 392.0, h, bk, tracking=tr, center=True, weight=0.2, halo=False, register=False)
    g += _type(M, "T", nx + wn_px / 2.0 + 1.5, 381.0, 12.5, bk, weight=0.16, halo=False, register=False)
    g += _S([M.p(507.0, 404.0), M.p(616.0, 404.0)], bk, "type")
    g += _type(M, "#d", 529.0, 434.0, 21.0, bk, tracking=1.0, weight=0.16, halo=False, register=False)
    g += _type(M, "k", 568.0, 438.0, 12.0, bk, weight=0.14, halo=False, register=False)
    M.halo(g, pad=1.6)
    M.add(g)


class _Guard:
    """Parallel-crowding guard, mm (r01 verbatim)."""

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
        self.g.setdefault((int(x / self.sep), int(y / self.sep)), []).append((x, y, ux, uy, sid))


def _v13_marks(pts: Sequence[Pt], dash: float, gap: float, step: float = 0.13) -> List[Pt]:
    """Where r01's ``_dash_mm`` put each mark (one centre per micro-dash) — the
    TEXTURE positions this round keeps, one round dot per v13 mark."""
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
    marks, run = [], []
    for x, y, ss in samples:
        if (ss % period) < dash:
            run.append((x, y))
        else:
            if run:
                marks.append(run)
            run = []
    if run:
        marks.append(run)
    return [(sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r)) for r in marks]


LAM = IF_D / 35.0     # 7.14 ref px = 1.21 mm across, 1.41 mm down
R_SOLID = 21          # v13


def _interference(M: _Map, rng: SeededRNG, colors: int) -> None:
    """v13's hero, construction and emission order verbatim."""
    bk = _pen(BLACK, colors)
    lam = LAM
    a_out, b_out = 272.0, 158.0
    guard = _Guard(0.82)
    sid = 0

    def ring(cx: float, cy: float, r: float):
        n = max(64, int(r * 2.6))
        return [(cx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n))
                for t in range(n + 1)]

    fade: List[Pt] = []

    def emit_clipped(pts, dotted: bool = False, keep_out=None):
        nonlocal sid
        sid += 1
        aa, bb = (a_out, b_out) if dotted else (a_out * 0.80, 126.0)
        run = []

        def flush(run):
            if len(run) >= 4:
                if dotted:
                    fade.extend(_v13_marks([M.p(x, y) for x, y in run], 0.42, 1.8))
                else:
                    _line(M, run, bk, f=2600)

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
                flush(run)
                run = []
        flush(run)

    for sx in (SRC_L, SRC_R):
        other = SRC_R if sx == SRC_L else SRC_L
        for m in range(1, R_SOLID + 1):
            emit_clipped(ring(sx, IF_CY, m * lam))
        for m in range(R_SOLID + 1, 52):
            emit_clipped(ring(sx, IF_CY, m * lam), dotted=True,
                         keep_out=(other, IF_CY, R_SOLID * lam + 6.0))
    M.texture(fade, bk, "crest-fade")
    M.stats["fade_v13_marks"] = len(fade)

    # --- the halo ellipses: each kept stretch its own arc, ending ON the keep-out
    reach = R_SOLID * lam + 8.0

    def keep(sx, a, b, t):
        q = (sx + a * math.cos(t), IF_CY + b * math.sin(t))
        xm = M.p(*q)[0]
        return (M.x0 + 2 < xm < M.x1 - 2
                and min(math.hypot(q[0] - SRC_L, q[1] - IF_CY),
                        math.hypot(q[0] - SRC_R, q[1] - IF_CY)) > reach)

    n_arcs = 0
    for sx in (SRC_L, SRC_R):
        for a in (152.0, 190.0, 232.0):
            b = a * 0.60
            N = 1440
            ts = [2 * math.pi * k / N for k in range(N)]
            ks = [keep(sx, a, b, t) for t in ts]
            if not any(ks):
                continue                      # a = 152 lies wholly inside the crest reach (as in v13)
            k0 = ks.index(False)               # start the scan on a gap: arcs never split at t = 0
            order = list(range(k0, N)) + list(range(0, k0))
            arcs, cur = [], []
            for k in order:
                if ks[k]:
                    cur.append(k)
                elif cur:
                    arcs.append(cur)
                    cur = []
            if cur:
                arcs.append(cur)
            for arc in arcs:
                def edge(t_in, t_out):
                    for _ in range(40):
                        tm = 0.5 * (t_in + t_out)
                        if keep(sx, a, b, tm):
                            t_in = tm
                        else:
                            t_out = tm
                    return t_in
                dt = 2 * math.pi / N
                t_first = ts[arc[0]]
                t_last = ts[arc[-1]]
                if t_last < t_first:
                    t_last += 2 * math.pi
                ta = edge(t_first, t_first - dt)
                tb = edge(t_last, t_last + dt)
                m = max(8, int((tb - ta) / math.radians(0.5)))
                pts = [(sx + a * math.cos(ta + (tb - ta) * i / m), IF_CY + b * math.sin(ta + (tb - ta) * i / m))
                       for i in range(m + 1)]
                M.dotline_px(pts, bk, f"halo-ellipse a={a:.0f}", prio=4)
                n_arcs += 1
    M.stats["halo_arcs"] = n_arcs

    # --- the horizontal axis through the figure ---------------------------
    M.add(_S([M.p(300.0, IF_CY), M.p(822.0, IF_CY)], bk))
    for sgn in (1, -1):
        base = IF_CX - sgn * 334.0
        _ocirc(M, base, IF_CY, 5.0, bk)
        for j in range(4):
            _fdot(M, base - sgn * (17.0 + 17.0 * j), IF_CY, 2.3, bk)
        _fdot(M, IF_CX - sgn * 305.0, IF_CY, 3.2, bk)
        _fdot(M, IF_CX - sgn * 266.0, IF_CY, 3.4, bk)
        cxx = IF_CX - sgn * 203.0
        _ocirc(M, cxx, IF_CY, 6.2, bk)
        _fdot(M, cxx, IF_CY, 2.2, bk)
    _fdot(M, IF_CX, IF_CY, 5.0, bk)
    _fdot(M, SRC_L, IF_CY, 4.8, bk)
    _fdot(M, SRC_R, IF_CY, 4.8, bk)

    # --- the dot field (v13's positions, sizes and seeded scatter) ---------
    k = 2 * math.pi / lam

    def field(px, py):
        d1 = math.hypot(px - SRC_L, py - IF_CY) + 4.0
        d2 = math.hypot(px - SRC_R, py - IF_CY) + 4.0
        return math.cos(k * d1) / math.sqrt(d1) + math.cos(k * d2) / math.sqrt(d2)

    placed: List[Tuple[float, float, float]] = []

    def place(px, py, r):
        if r < 0.7 or not (M.x0 + 3 < M.p(px, py)[0] < M.x1 - 3):
            return
        for qx, qy, qr in placed:
            if math.hypot(px - qx, py - qy) < (r + qr) * 1.3 + 4.0:
                return
        placed.append((px, py, r))
        cx, cy = M.p(px, py)
        M.field.append((cx, cy, M.s(r)))

    for cx in (SRC_L, IF_CX, SRC_R):
        for j in range(-6, 7):
            if j:
                place(cx, IF_CY + 24.0 * j, 1.7 + 4.2 * math.exp(-abs(j) / 3.4))
    for sx in (SRC_L, SRC_R):
        for t in range(12):
            th = 2 * math.pi * t / 12 + 0.09
            for rr in (46.0, 84.0, 122.0, 160.0, 198.0):
                px = sx + rr * math.cos(th)
                py = IF_CY + rr * 0.62 * math.sin(th)
                place(px, py, 1.1 + 22.0 * abs(field(px, py)))
    for _ in range(60):
        px = IF_CX + rng.uniform(-228.0, 228.0)
        py = IF_CY + rng.uniform(-145.0, 145.0)
        place(px, py, 0.9 + 16.0 * abs(field(px, py)))
    M.stats["field_v13"] = len(M.field)

    # --- vertical dotted droplines ----------------------------------------
    drops = [434.0, 477.0, 516.0, 561.0, 613.0, 652.0, 691.0]
    for j, x in enumerate(drops):
        top = 462.0 if x in (434.0, 561.0, 691.0) else 496.0
        M.dotline_px([(x, top), (x, IF_CY - 6.0)], bk, "hero:drop-up", prio=5)
        _fdot(M, x, top - 8.0, 2.0, bk)
        bot = 832.0 if j % 2 == 0 else 806.0
        M.dotline_px([(x, IF_CY + 6.0), (x, bot)], bk, "hero:drop-down", prio=5)
    _ocirc(M, IF_CX, 486.0, 4.8, bk)
    _ocirc(M, IF_CX, 716.0, 4.8, bk)


def _softmax(M: _Map, colors: int) -> None:
    bk = _pen(BLACK, colors)
    x0, x1 = 313.0, 806.0

    def curve_y(x: float) -> float:
        v = 0.0
        for cx, h, _m in SOFT_PEAKS:
            v += h / (1.0 + ((x - cx) / 9.5) ** 2) ** 1.6
        return SOFT_BASE - v

    n = int((x1 - x0) / 0.7)
    _line(M, [(x0 + k * (x1 - x0) / n, curve_y(x0 + k * (x1 - x0) / n)) for k in range(n + 1)], bk, f=2400)
    for cx, h in SOFT_GHOSTS:
        gp = [(cx - 26.0 + t * 0.9,
               SOFT_BASE - h / (1.0 + ((cx - 26.0 + t * 0.9 - cx) / 8.0) ** 2) ** 1.6) for t in range(59)]
        M.dotline_px(gp, bk, "softmax:ghost", prio=6)
    for cx, h, m in SOFT_PEAKS:
        _line(M, [(cx, SOFT_BASE), (cx, SOFT_BASE - h + 2.0)], bk)
        if m == "o":
            _ocirc(M, cx, SOFT_BASE - h - 3.0, 5.0, bk)
        elif m == "f":
            _fdot(M, cx, SOFT_BASE - h - 3.0, 4.4, bk)
    for x, kind in [
        (321.0, "f"), (391.0, "f"), (434.0, "o"), (475.0, "o"), (516.0, "f"),
        (559.0, "o"), (601.0, "o"), (645.0, "o"), (686.0, "o"), (724.0, "f"), (799.0, "f"),
    ]:
        if kind == "o":
            _ocirc(M, x, SOFT_BASE, 4.4, bk)
        else:
            _fdot(M, x, SOFT_BASE, 3.2, bk)
    _lead_dots(M, 303.0, -14.0, 3, SOFT_BASE, 2.4, bk)
    _lead_dots(M, 818.0, 14.0, 3, SOFT_BASE, 2.4, bk)
    _type(M, "softmax", 561.0, 786.0, 20.0, bk, tracking=1.16, center=True, weight=0.16)


def _v_occluder(i: int, M: _Map):
    """Row i hides where it rises into row i-1's envelope (+0.6 mm): the upper
    packet is in front.  None for the top row."""
    if i == 0:
        return None
    y_up, pk_up = V_ROWS[i - 1], V_PACKS[i - 1]
    gap = V_OCC_GAP_MM / M.sy

    def occ(x: float, yy: float) -> bool:
        return yy < y_up + _pk_env(x, pk_up) + gap

    return occ


def _v_block(M: _Map, colors: int) -> None:
    oc = _pen(OCHRE, colors)
    for i, y in enumerate(V_ROWS):
        wave_packet(M, V_L, V_R, y, V_PACKS[i], oc, occ=_v_occluder(i, M), name=f"V{i}")
        if i == 2:
            _fdot(M, V_L, y, 4.4, oc)
        else:
            _ocirc(M, V_L, y, 4.8, oc)
        _ocirc(M, V_R, y, 4.8, oc)
        _lead_dots(M, V_R + 24.0, 14.0, 4, y, 2.4, oc)
        M.dotline_px([(688.0, y), (V_L - 8.0, y)], oc, "V:feed", prio=6)
        _fdot(M, 684.0, y, 2.2, oc)
    _type(M, "V", 1022.0, 748.0, 34.0, oc, weight=0.46)
    # softmax -> Z: a_j V_j into Z.  Same launch as v13, re-aimed onto Z's axis.
    for i, x in enumerate([391.0, 434.0, 475.0, 516.0, 559.0, 601.0]):
        end = LINK_ENDS[i]
        off = end - x
        pts = _bez((x, SOFT_BASE + 8.0), (x - 4.0, 960.0), (x + 0.62 * off, 1010.0), (end, MOE_Y))
        M.dotline_px(pts, oc, f"link{i}->Z", prio=2)
    # V's connector: v13 sent it to the MoE gather node; it now ends on Z's axis,
    # running the quiet channel between softmax and the MoE header.
    y = V_CHANNEL_Y
    conn = (_bez((975.0 + 22.0, V_ROWS[2]), (1050.0, 845.0), (1052.0, y), (960.0, y), n=40)
            + [(960.0 - 10.0 * k, y) for k in range(1, 35)]
            + _bez((620.0, y), (524.0, y), (462.0, 975.0), (V_CONN_END, MOE_Y), n=48)[1:])
    M.dotline_px(conn, oc, "V->Z", prio=2)


def _moe_row(M: _Map, colors: int) -> None:
    gr = _pen(GREEN, colors)
    pu = _pen(PURPLE, colors)
    bk = _pen(BLACK, colors)

    zp: List[Packet] = [
        (277.0, 47.0, 13.5, 68.0, 0.0),
        (178.0, 13.0, 8.5, 15.0, 0.4),
        (443.0, 13.0, 8.5, 14.0, 0.9),
        (352.0, 9.0, 7.5, 8.0, 0.2),
    ]
    wave_packet(M, Z_L, Z_R, MOE_Y, zp, gr, name="Z")
    _ocirc(M, 110.0, MOE_Y, 4.8, gr)
    for x in (178.0, 315.0, 443.0, 490.0):
        _ocirc(M, x, MOE_Y, 4.4, gr)
    _lead_dots(M, 88.0, -13.0, 4, MOE_Y, 2.4, gr)
    _fdot(M, 277.0, MOE_Y - 72.0, 4.6, gr)
    _fdot(M, 277.0, MOE_Y + 72.0, 4.6, gr)
    _type(M, "Z = AV", 100.0, 1018.0, 30.0, gr, tracking=0.98, weight=0.42)

    _type(M, "MoE", 706.0, 948.0, 22.0, bk, tracking=1.02, center=True, weight=0.2)
    for a, b in ((618.0, 668.0), (746.0, 796.0)):
        M.add(_S([M.p(a, 941.0), M.p(b, 941.0)], bk, "type"))
    _type(M, "experts", 714.0, 976.0, 15.0, pu, tracking=1.1, center=True)
    _type(M, "top-2", 848.0, 999.0, 15.0, pu, tracking=1.1, center=True)
    _type(M, "router", 529.0, 1049.0, 15.0, pu, tracking=1.1, center=True)

    for nx in (ROUTER_X, NODE2_X):
        _ocirc(M, nx, MOE_Y, 12.5, pu)
        _ocirc(M, nx, MOE_Y, 8.0, pu)
        _fdot(M, nx, MOE_Y, 3.4, pu)

    lane_pk: List[List[Packet]] = [
        [(700.0, 23.0, 8.0, 24.0, 0.0), (743.0, 12.0, 6.6, 11.0, 0.7)],
        [(700.0, 20.0, 7.6, 10.0, 0.0)],
        [(700.0, 20.0, 7.6, 10.0, 0.4)],
        [(700.0, 20.0, 7.6, 10.0, 0.8)],
        [(706.0, 27.0, 8.0, 27.0, 0.0), (752.0, 13.0, 6.8, 12.0, 0.5)],
    ]
    for i, y in enumerate(LANE_YS):
        if i in (0, 4):
            wave_packet(M, LANE_L, LANE_R, y, lane_pk[i], pu, name=f"expert{i}")
            _ocirc(M, LANE_L, y, 5.6, pu)
            _ocirc(M, LANE_R, y, 5.6, pu)
            _line(M, _bez((ROUTER_X + 13.0, MOE_Y), (ROUTER_X + 58.0, MOE_Y),
                          (LANE_L - 42.0, y), (LANE_L - 6.0, y)), pu)
            _line(M, _bez((LANE_R + 6.0, y), (LANE_R + 42.0, y),
                          (NODE2_X - 50.0, MOE_Y), (NODE2_X - 13.0, MOE_Y)), pu)
            _fdot(M, LANE_L - 24.0, y, 3.0, pu)
            _fdot(M, LANE_R + 26.0, y, 3.0, pu)
        else:
            M.dotline_px([(LANE_L, y), (LANE_L + 52.0, y)], pu, "ghost:rail", prio=5)
            M.dotline_px([(LANE_R - 52.0, y), (LANE_R, y)], pu, "ghost:rail", prio=5)
            wave_packet(M, LANE_L + 8.0, LANE_R - 8.0, y, lane_pk[i], pu, envelope=False, ghost=True,
                        name=f"expert{i}")
            _ocirc(M, LANE_L, y, 5.0, pu, n=28)
            _ocirc(M, LANE_R, y, 5.0, pu, n=28)
            M.dotline_px(_bez((ROUTER_X + 13.0, MOE_Y), (ROUTER_X + 54.0, MOE_Y),
                              (LANE_L - 40.0, y), (LANE_L - 6.0, y)), pu, "ghost:fork", prio=5)
            M.dotline_px(_bez((LANE_R + 6.0, y), (LANE_R + 40.0, y),
                              (NODE2_X - 48.0, MOE_Y), (NODE2_X - 13.0, MOE_Y)), pu, "ghost:join", prio=5)

    yp: List[Packet] = [(978.0, 31.0, 11.0, 40.0, 0.0), (1030.0, 11.0, 7.5, 11.0, 0.6)]
    wave_packet(M, NODE2_X + 14.0, 1052.0, MOE_Y, yp, pu, name="Y")
    _ocirc(M, 1052.0, MOE_Y, 4.8, pu)
    _lead_dots(M, 1072.0, 13.0, 3, MOE_Y, 2.4, pu)
    _type(M, "Y", 1020.0, 1030.0, 30.0, pu, weight=0.46)


def _bez_x_hit(p0, c1, c2, p1, x: float) -> Tuple[float, float]:
    """Point on the cubic where it first reaches ``x`` (bisection on t)."""
    pts = _bez(p0, c1, c2, p1, n=2000)
    for a, b in zip(pts[:-1], pts[1:]):
        if (a[0] - x) * (b[0] - x) <= 0 and a[0] != b[0]:
            t = (x - a[0]) / (b[0] - a[0])
            return (x, a[1] + (b[1] - a[1]) * t)
    raise ValueError("curve never reaches x")


def _backward(M: _Map, colors: int) -> None:
    pens = [_pen(RED, colors), _pen(BLUE, colors), _pen(OCHRE, colors),
            _pen(BLACK, colors), _pen(GREEN, colors)]
    dens = ["Q", "K", "V", "A", "Z"]
    curves = []
    for i, y in enumerate(BACK_ROWS):
        pn = pens[i]
        _frac(M, "@L", "@" + dens[i], 62.0, y, BACK_H, pn, tracking=1.02, gap_px=BACK_GAP)
        _arrow(M, 104.0, y, -1, 8.5, pn)
        M.dotline_px([(118.0, y), (BACK_COL - 7.0, y)], pn, f"back:{dens[i]}", prio=1)
        _ocirc(M, BACK_COL, y, 4.6, pn)
        tx = 500.0 + 58.0 * i
        ty = 1010.0 - 14.0 * i
        bz = ((BACK_COL + 7.0, y), (BACK_COL + 120.0 + 20.0 * i, y), (tx - 120.0, ty + 90.0), (tx, ty))
        curves.append(bz)

    # the Z taps are the start of the dL return curves (the reference draws them
    # as one line): each tap now runs from Z's axis down ONTO its curve, and the
    # curve carries a dot exactly at the junction.
    #
    # A tap is a dead-end branch, and Leo's stroke order is a nearest-neighbour
    # walk, so two local spacings decide whether the pen draws the branch in
    # passing or has to come back for it across the sheet.  They are set here,
    # inside J1's pitch band: the tap's first dot sits 0.8 mm above the junction
    # J (the curve's next is 1.1 mm on), so the walk turns up the tap; and on
    # the curve dot Q nearest the tap's cap, where the walk re-enters the curve,
    # the step back towards J is 0.85 mm and the step on is 1.15 mm, so it
    # finishes the stretch below Q first and leaves the curve at its far end.
    junction = {}
    for (xx, pidx), bz in zip(TAPS, curves[:3]):
        junction[pidx] = _bez_x_hit(*bz, xx)
    for i, bz in enumerate(curves):
        pn = pens[i]
        pidx = [RED, BLUE, OCHRE, BLACK, GREEN][i]
        pts = [M.p(*q) for q in _bez(*bz, n=2000)]
        anchors: List[Pt] = []
        if pidx in junction:
            cum = _cum(pts)
            xx = dict((b, a) for a, b in TAPS)[pidx]
            jm = M.p(*junction[pidx])
            cap = M.p(xx, MOE_Y + 22.0)
            sJ = cum[int(np.argmin([math.dist(q, jm) for q in pts]))]
            sQ = cum[int(np.argmin([math.dist(q, cap) for q in pts]))]
            back = -1.0 if sQ > sJ else 1.0
            anchors = [jm, _at(pts, cum, sJ - back * 1.1),
                       _at(pts, cum, sQ), _at(pts, cum, sQ + back * 0.85), _at(pts, cum, sQ - back * 1.15)]
        M.dotline(pts, pn, f"return:{dens[i]}", prio=1, anchors=anchors)
    for xx, pidx in TAPS:
        pn = _pen(pidx, colors)
        jx, jy = junction[pidx]
        jm = M.p(jx, jy)
        M.dotline([M.p(xx, MOE_Y + 26.0), jm], pn, "tap", prio=2,
                  anchors=[jm, (jm[0], jm[1] + 0.8)])
        _fdot(M, xx, MOE_Y + 22.0, 2.2, pn)

    M.dotline_px([(BACK_COL, MOE_Y + 66.0), (BACK_COL, BACK_ROWS[-1] + 10.0)],
                 _pen(GREEN, colors), "back:column", prio=3)

    pu = _pen(PURPLE, colors)
    for name, y in [("Y", 1191.0), ("experts", 1265.0), ("router", 1321.0)]:
        h = 14.0 if len(name) < 4 else 11.5
        _frac(M, "@L", "@" + name, 1052.0, y, h, pu, tracking=1.0)
        _arrow(M, 1006.0, y, 1, 8.5, pu)
    M.dotline_px(_bez((940.0, 1120.0), (985.0, 1150.0), (958.0, 1178.0), (994.0, 1191.0)), pu,
                 "skeleton:Y", prio=5)
    # v13's seven skeleton segments walked as three paths, a dot on every corner
    M.dotline_px([(796.0, 1175.0), (796.0, 1265.0), (977.0, 1265.0), (994.0, 1265.0)], pu,
                 "skeleton:experts", prio=5, corners=True)
    M.dotline_px([(718.0, 1175.0), (718.0, 1321.0), (977.0, 1321.0), (994.0, 1321.0)], pu,
                 "skeleton:router", prio=5, corners=True)
    M.dotline_px([(977.0, 1265.0), (977.0, 1321.0)], pu, "skeleton:bridge", prio=5)
    for nx, ny in ((718.0, 1238.0), (796.0, 1238.0), (718.0, 1291.0), (718.0, 1321.0),
                   (977.0, 1265.0), (977.0, 1321.0)):
        _ocirc(M, nx, ny, 4.2, pu, n=28)


# ---------------------------------------------------------------------------
# sheet pass 1: halos (r05)
# ---------------------------------------------------------------------------


def _length(pts: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def _apply_halos(strokes: List[Stroke], M: _Map) -> List[Stroke]:
    """Clip every non-type stroke out of every label box (exact Region clip);
    a small mark that touches a box is dropped whole; a short dash on a node is
    dropped (it would vanish into the node)."""
    boxes = M.halos
    out: List[Stroke] = []
    for st in strokes:
        if st.kind == "type":
            out.append(st)
            continue
        if st.kind == "dash" and any(
                math.hypot(x - nx, y - ny) < nr for x, y in st.pts[:: max(1, len(st.pts) - 1)]
                for nx, ny, nr in M.nodes):
            continue
        xs = [p[0] for p in st.pts]
        ys = [p[1] for p in st.pts]
        bx0, by0, bx1, by1 = min(xs), min(ys), max(xs), max(ys)
        hit = [b for b in boxes if not (bx1 < b[0] or bx0 > b[2] or by1 < b[1] or by0 > b[3])]
        if not hit:
            out.append(st)
            continue
        if max(bx1 - bx0, by1 - by0) < 3.0:
            continue
        region = Union(*[Rect(*b) for b in hit])
        for run in clip(st.pts, region, keep="outside"):
            if _length(run) >= 0.3:
                out.append(Stroke(run, st.pen, st.kind, st.f))
    return out


# ---------------------------------------------------------------------------
# sheet pass 2: the dot resolver
# ---------------------------------------------------------------------------


_MASKS: Dict = {}


class _Raster:
    """Boolean occupancy on the sheet at RES mm."""

    def __init__(self, W: float = 215.0, H: float = 300.0) -> None:
        self.nx, self.ny = int(W / RES) + 1, int(H / RES) + 1
        self.a = np.zeros((self.ny, self.nx), dtype=bool)

    def _idx(self, x, y):
        return (np.clip(np.rint(np.asarray(y) / RES).astype(int), 0, self.ny - 1),
                np.clip(np.rint(np.asarray(x) / RES).astype(int), 0, self.nx - 1))

    def stamp(self, pts: np.ndarray, radius: float) -> None:
        """Mark every cell within ``radius`` of any point (vectorised over points)."""
        pts = np.asarray(pts, dtype=float).reshape(-1, 2)
        if len(pts) == 0:
            return
        iy, ix = self._idx(pts[:, 0], pts[:, 1])
        R = int(math.ceil(radius / RES))
        for dy in range(-R, R + 1):
            for dx in range(-R, R + 1):
                if (dx * dx + dy * dy) * RES * RES <= radius * radius + 1e-12:
                    self.a[np.clip(iy + dy, 0, self.ny - 1), np.clip(ix + dx, 0, self.nx - 1)] = True

    def stamp1(self, x: float, y: float, radius: float) -> None:
        """One disc, by slice (fast path for placing a single dot)."""
        R = int(math.ceil(radius / RES))
        key = (R, radius)
        mask = _MASKS.get(key)
        if mask is None:
            yy, xx = np.mgrid[-R:R + 1, -R:R + 1]
            mask = (xx * xx + yy * yy) * RES * RES <= radius * radius + 1e-12
            _MASKS[key] = mask
        cy, cx = int(round(y / RES)), int(round(x / RES))
        y0, y1, x0, x1 = cy - R, cy + R + 1, cx - R, cx + R + 1
        if y0 < 0 or x0 < 0 or y1 > self.ny or x1 > self.nx:
            self.stamp(np.asarray([[x, y]]), radius)
            return
        self.a[y0:y1, x0:x1] |= mask

    def box(self, x0, y0, x1, y1) -> None:
        iy0, ix0 = self._idx(x0, y0)
        iy1, ix1 = self._idx(x1, y1)
        self.a[int(iy0):int(iy1) + 1, int(ix0):int(ix1) + 1] = True

    def hit(self, x, y):
        iy, ix = self._idx(x, y)
        return self.a[iy, ix]


def _resample(pts: Sequence[Pt], step: float) -> np.ndarray:
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(1, int(math.ceil(L / step)))
        for k in range(1, n + 1):
            out.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    return np.asarray(out, dtype=float)


def _resolve_dots(M: _Map, solid: List[Stroke]) -> List[Stroke]:
    """Place every dot of every dotted line and texture where it is VISIBLE."""
    pens = sorted({st.pen for st in solid} | {p.pen for p in M.paths} | {t[1] for t in M.textures},
                  key=lambda v: -1 if v is None else v)
    ink = {p: _Raster() for p in pens}
    dots = {p: _Raster() for p in pens}
    block = _Raster()
    for b in M.halos:
        block.box(*b)
    for cx, cy, r in M.nodes:
        block.stamp1(cx, cy, r + 0.08)     # +0.08: the raster rounds by <= 0.07 mm

    # the v13 field dots are solid discs; a small one swallowed by a crest line
    # is an invisible cycle and is not drawn
    line_ink = {p: _Raster() for p in pens}
    for p in pens:
        pts = [_resample(st.pts, RES) for st in solid if st.pen == p and st.kind in ("line", "type", "dash")]
        if pts:
            line_ink[p].stamp(np.concatenate(pts), 0.0)
    field_kept: List[Stroke] = []
    swallowed = in_label = slid = 0
    for cx, cy, r in M.field:
        pen = _pen_of_field(M)
        if any(b[0] <= cx <= b[2] and b[1] <= cy <= b[3] for b in M.halos):
            in_label += 1
            continue
        if r <= 0.35 and (line_ink[pen].hit(cx, cy) or _ring_hits(line_ink[pen], cx, cy, r + 0.2)):
            # a small field dot a crest line would swallow: slide it (<= 0.6 mm)
            # into the gap between crests, where it reads as a dot again
            spot = None
            for rad in (0.15, 0.3, 0.45, 0.6):
                for a in np.linspace(0, 2 * math.pi, 16, endpoint=False):
                    qx, qy = cx + rad * math.cos(a), cy + rad * math.sin(a)
                    if not (line_ink[pen].hit(qx, qy) or _ring_hits(line_ink[pen], qx, qy, r + 0.2)):
                        spot = (qx, qy)
                        break
                if spot:
                    break
            if spot is None:
                swallowed += 1
                continue
            cx, cy = spot
            slid += 1
        field_kept += _disc_mm(cx, cy, r, pen, "disc")
    M.stats["field_slid"] = slid
    M.stats["field_kept"] = len(field_kept)
    M.stats["field_swallowed"] = swallowed
    M.stats["field_in_label"] = in_label
    solid = solid + field_kept

    for p in pens:
        pts = [_resample(st.pts, RES) for st in solid if st.pen == p]
        if pts:
            ink[p].stamp(np.concatenate(pts), CLEAR_INK + 0.05)

    locked: Dict[Optional[int], List[Pt]] = {p: [] for p in pens}   # line dots, for phase-lock
    out: List[Stroke] = []

    grid: Dict[Optional[int], Dict[Tuple[int, int], List[Pt]]] = {p: {} for p in pens}

    def free(pen, xs, ys):
        ok = ~(block.hit(xs, ys) | ink[pen].hit(xs, ys))
        # dot-to-dot clearance is checked EXACTLY (the raster rounds by <= 0.07 mm)
        cx, cy = int(math.floor(float(np.mean(xs)))), int(math.floor(float(np.mean(ys))))
        near = [q for dx in (-1, 0, 1) for dy in (-1, 0, 1) for q in grid[pen].get((cx + dx, cy + dy), ())]
        if near:
            q = np.asarray(near)
            d = np.hypot(np.asarray(xs)[:, None] - q[None, :, 0], np.asarray(ys)[:, None] - q[None, :, 1])
            ok &= d.min(axis=1) >= CLEAR_DOT
        return ok

    def put(pen, x, y, line: bool):
        grid[pen].setdefault((int(math.floor(x)), int(math.floor(y))), []).append((x, y))
        dots[pen].stamp1(x, y, CLEAR_DOT)
        if line:
            locked[pen].append((x, y))
        out.extend(_dot_mark(x, y, pen))

    # TEXTURES first: v13's own positions, never re-pitched.  A mark that would
    # be invisible where v13 put it slides <= 0.6 mm to the nearest clear spot.
    offs = [(0.0, 0.0)] + [(rad * math.cos(a), rad * math.sin(a))
                           for rad in (0.15, 0.3, 0.45, 0.6)
                           for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    for name, pen, pts in M.textures:
        kept = moved = 0
        for x, y in pts:
            for ox, oy in offs:
                if free(pen, np.asarray([x + ox]), np.asarray([y + oy]))[0]:
                    put(pen, x + ox, y + oy, line=False)
                    kept += 1
                    moved += (ox, oy) != (0.0, 0.0)
                    break
        M.stats[f"texture:{name}"] = kept
        M.stats[f"texture:{name}:slid"] = moved

    # DOTTED LINES: anchors (ends, corners, junctions, phase-lock) + 1 mm fill,
    # each dot slid <= SNAP into the nearest clear gap on its own path
    n_line = n_lock = n_drop = 0
    for path in sorted(M.paths, key=lambda p: p.prio):
        pen = path.pen
        pts = path.pts
        cum = _cum(pts)
        L = cum[-1]
        if L < 0.3:
            continue
        ss = np.linspace(0.0, L, max(2, int(L / 0.05) + 1))
        xy = np.asarray([_at(pts, cum, s) for s in ss])
        anchors = [0.0, L]
        if path.corners:
            anchors += cum[1:-1]
        fixed = set()
        for ax, ay in path.anchors:
            a = float(ss[int(np.argmin(np.hypot(xy[:, 0] - ax, xy[:, 1] - ay)))])
            anchors.append(a)
            fixed.add(a)
        # phase-lock: projections of earlier same-pen line dots within LOCK_DIST
        near = locked[pen]
        if near:
            arr = np.asarray(near)
            bx0, by0 = xy.min(axis=0) - LOCK_DIST
            bx1, by1 = xy.max(axis=0) + LOCK_DIST
            sel = arr[(arr[:, 0] >= bx0) & (arr[:, 0] <= bx1) & (arr[:, 1] >= by0) & (arr[:, 1] <= by1)]
            if len(sel):
                sub = xy[::4]
                ssub = ss[::4]
                d = np.hypot(sub[:, None, 0] - sel[None, :, 0], sub[:, None, 1] - sel[None, :, 1])
                j = np.argmin(d, axis=0)
                dm = d[j, np.arange(len(sel))]
                for jj, dd in zip(j, dm):
                    if dd < LOCK_DIST:
                        anchors.append(float(ssub[jj]))
                        n_lock += 1
        anchors.sort()
        merged: List[float] = []
        for a in anchors:
            if merged and a - merged[-1] < 0.5:
                prev = merged[-1]
                if prev in fixed or prev in (0.0, L):
                    continue                   # hard anchors win
                merged[-1] = a if (a in fixed or a == L) else 0.5 * (prev + a)
            else:
                merged.append(a)
        cands: List[float] = []
        for a, b in zip(merged[:-1], merged[1:]):
            n = max(1, int(round((b - a) / DOT_PITCH)))
            cands += [a + (b - a) * k / n for k in range(n)]
        cands.append(merged[-1])
        for c in cands:
            lo = int(np.searchsorted(ss, c - SNAP))
            hi = int(np.searchsorted(ss, c + SNAP, side="right"))
            win = np.arange(lo, max(lo + 1, hi))
            win = win[win < len(ss)]
            if c in fixed:                    # a junction dot is shared, never slid
                win = np.asarray([int(np.argmin(np.abs(ss - c)))])
                x, y = xy[win[0]]
                if not block.hit(x, y) and _clear_of(grid[pen], x, y):
                    put(pen, float(x), float(y), line=True)
                    n_line += 1
                else:
                    n_drop += 1
                continue
            ok = free(pen, xy[win, 0], xy[win, 1])
            if not ok.any():
                n_drop += 1
                continue
            best = win[ok][int(np.argmin(np.abs(ss[win[ok]] - c)))]
            put(pen, float(xy[best, 0]), float(xy[best, 1]), line=True)
            n_line += 1
    M.stats["line_dots"] = n_line
    M.stats["line_dots_dropped"] = n_drop
    M.stats["lock_anchors"] = n_lock
    return solid + out


def _clear_of(g, x: float, y: float) -> bool:
    cx, cy = int(math.floor(x)), int(math.floor(y))
    return all(math.hypot(x - qx, y - qy) >= CLEAR_DOT
               for dx in (-1, 0, 1) for dy in (-1, 0, 1) for qx, qy in g.get((cx + dx, cy + dy), ()))


def _pen_of_field(M: _Map):
    return M._field_pen


def _ring_hits(r: _Raster, cx: float, cy: float, rad: float) -> bool:
    """Does line ink pass within ``rad`` of (cx, cy)?  (probed on two rings)"""
    th = np.linspace(0, 2 * math.pi, 16, endpoint=False)
    return bool(r.hit(cx + rad * np.cos(th), cy + rad * np.sin(th)).any()
                or r.hit(cx + 0.5 * rad * np.cos(th), cy + 0.5 * rad * np.sin(th)).any())


# ---------------------------------------------------------------------------
# sheet pass 3: the tour
# ---------------------------------------------------------------------------


def _round_pts(pts: Sequence[Pt]) -> List[Pt]:
    return [(round(x, 2), round(y, 2)) for x, y in pts]


HOP_CAP = 80.0   # mm: no consecutive in-layer travel should exceed this (A4)


def _greedy_oriented(strokes: List[Stroke]) -> List[Stroke]:
    """Nearest-neighbour walk from (0, 0) that may enter an open stroke at either
    end and a closed loop at any vertex; every stroke comes back ORIENTED."""
    items = []
    cx, ci, cv = [], [], []
    for k, st in enumerate(strokes):
        pts = _round_pts(st.pts)
        closed = len(pts) > 3 and pts[0] == pts[-1]
        items.append((st, pts, closed))
        if closed and st.kind != "dot":
            for v in range(len(pts) - 1):
                cx.append(pts[v])
                ci.append(k)
                cv.append(v)
        else:
            cx.append(pts[0])
            ci.append(k)
            cv.append(0)
            if not closed:
                cx.append(pts[-1])
                ci.append(k)
                cv.append(-1)
    Px = np.asarray([p[0] for p in cx])
    Py = np.asarray([p[1] for p in cx])
    I = np.asarray(ci)
    V = np.asarray(cv)
    span: Dict[int, List[int]] = {}
    for j, k in enumerate(ci):
        span.setdefault(k, [j, j])[1] = j
    pos = (0.0, 0.0)
    out: List[Stroke] = []
    for _ in range(len(items)):
        j = int(np.argmin((Px - pos[0]) ** 2 + (Py - pos[1]) ** 2))
        k = int(I[j])
        st, pts, closed = items[k]
        v = int(V[j])
        if closed and st.kind != "dot":
            pts = pts[v:-1] + pts[:v] + [pts[v]]
        elif v == -1:
            pts = pts[::-1]
        lo, hi = span[k]
        Px[lo:hi + 1] = 1e9
        Py[lo:hi + 1] = 1e9
        out.append(Stroke(pts, st.pen, st.kind, st.f))
        pos = pts[-1]
    return out


class _EngineWalk:
    """``postprocess.optimize_stroke_order`` re-implemented exactly (nearest
    START from the last END, from (0, 0), ties to the lowest index), vectorised
    and prefix-cached so an orientation change is re-walked only from the first
    step it can affect."""

    def __init__(self, S: np.ndarray, E: np.ndarray) -> None:
        self.S, self.E = S.copy(), E.copy()
        self.order, self.hop = self.walk(self.S, self.E, 0, None, None)

    @staticmethod
    def walk(S, E, k0, order0, hop0):
        n = len(S)
        order = np.empty(n, dtype=int)
        hop = np.empty(n)
        Sx, Sy = S[:, 0].copy(), S[:, 1].copy()
        if k0:
            order[:k0] = order0[:k0]
            hop[:k0] = hop0[:k0]
            used = order0[:k0]
            Sx[used] = 1e9
            Sy[used] = 1e9
            pos = E[order0[k0 - 1]]
        else:
            pos = (0.0, 0.0)
        for k in range(k0, n):
            d = (Sx - pos[0]) ** 2 + (Sy - pos[1]) ** 2
            j = int(np.argmin(d))
            order[k] = j
            hop[k] = math.sqrt(d[j])
            Sx[j] = 1e9
            Sy[j] = 1e9
            pos = E[j]
        return order, hop

    @staticmethod
    def cost(hop) -> float:
        h = hop[1:]                       # hop[0] is the swap approach, not in-layer
        if len(h) == 0:
            return 0.0
        return 1e4 * float(np.maximum(0.0, h - HOP_CAP).sum()) + 20.0 * float(h.max()) + float(h.sum())

    def try_variant(self, i: int, s_new, e_new) -> bool:
        """Re-orient stroke i; keep it only if the engine's walk gets cheaper."""
        order, hop = self.order, self.hop
        n = len(order)
        rank = np.empty(n, dtype=int)
        rank[order] = np.arange(n)
        ki = int(rank[i])
        posx = np.concatenate([[0.0], self.E[order[:-1], 0]])
        posy = np.concatenate([[0.0], self.E[order[:-1], 1]])
        d_new = np.sqrt((posx[:ki] - s_new[0]) ** 2 + (posy[:ki] - s_new[1]) ** 2)
        earlier = np.nonzero(d_new <= hop[:ki] + 1e-9)[0]
        k0 = int(earlier[0]) if len(earlier) else ki
        S2, E2 = self.S.copy(), self.E.copy()
        S2[i], E2[i] = s_new, e_new
        o2, h2 = self.walk(S2, E2, k0, order, hop)
        if self.cost(h2) < self.cost(hop) - 1e-9:
            self.S, self.E, self.order, self.hop = S2, E2, o2, h2
            return True
        return False


def _tour(strokes: List[Stroke], rounds: int = 3) -> List[Stroke]:
    """Order one pen for Leo.

    1. a reversal- and rotation-aware nearest-neighbour walk orients every
       stroke;
    2. a local search re-orients open strokes (flip) and closed loops (4 entry
       points) against the ENGINE's own walk — ``postprocess.reorder_by_color``
       re-derives stroke order by nearest start and never reverses, so the only
       lever a piece has is which end each stroke starts at;
    3. strokes are emitted in exactly the order that walk produces, so the
       gcode's order is this order (checked: the walk of the emitted list is the
       identity)."""
    base = _greedy_oriented(strokes)
    pts = [list(st.pts) for st in base]
    S = np.asarray([p[0] for p in pts], dtype=float)
    E = np.asarray([p[-1] for p in pts], dtype=float)
    ew = _EngineWalk(S, E)
    variants: List[Tuple[int, List[List[Pt]]]] = []
    for i, st in enumerate(base):
        if st.kind == "dot":
            continue
        p = pts[i]
        closed = len(p) > 3 and p[0] == p[-1]
        if closed:
            if _length(p) > 3.0:
                m = len(p) - 1
                variants.append((i, [p[v:-1] + p[:v] + [p[v]] for v in (m // 4, m // 2, 3 * m // 4)]))
        elif math.dist(p[0], p[-1]) > 2.0:
            variants.append((i, [p[::-1]]))
    for _ in range(rounds):
        changed = 0
        for i, alts in variants:
            for alt in alts:
                if ew.try_variant(i, alt[0], alt[-1]):
                    pts[i] = alt
                    changed += 1
        if not changed:
            break
    # dot steering: a dot is a 0.1 mm loop, so where it starts is free to
    # +-0.1 mm.  Next to a long hop that is enough to break the near-ties that
    # decide which way the walk runs along a dotted line after entering it
    # mid-way (the Z tap -> return curve dead end).
    for _ in range(rounds):
        changed = 0
        order, hop = ew.order, ew.hop
        hot = set()
        for k in np.nonzero(hop[1:] > 5.0)[0] + 1:
            for q in (ew.E[order[k - 1]], ew.S[order[k]]):
                near = np.nonzero(np.hypot(ew.S[:, 0] - q[0], ew.S[:, 1] - q[1]) < 3.0)[0]
                hot.update(int(j) for j in near if base[j].kind == "dot")
        for i in sorted(hot):
            p = pts[i]
            m = len(p) - 1
            for v in (m // 4, m // 2, 3 * m // 4):
                alt = p[v:-1] + p[:v] + [p[v]]
                if ew.try_variant(i, alt[0], alt[-1]):
                    pts[i] = alt
                    p = alt
                    changed += 1
        # the direction a dotted line is walked after a mid-way entry is decided
        # by B's two chain neighbours; lean B and the wanted neighbour towards
        # each other and the other neighbour away (0.4 mm of leverage in all)
        order, hop = ew.order, ew.hop
        for k in np.nonzero(hop[1:] > 5.0)[0] + 1:
            b = int(ew.order[k])
            if base[b].kind != "dot":
                continue
            c = ew.S[b]
            d = np.hypot(ew.S[:, 0] - c[0], ew.S[:, 1] - c[1])
            d[b] = np.inf
            nbr = [int(j) for j in np.argsort(d)[:6] if base[int(j)].kind == "dot" and d[int(j)] < 1.6]
            if len(nbr) < 2:
                continue
            n1 = nbr[0]
            n2 = next((j for j in nbr[1:] if np.dot(ew.S[j] - c, ew.S[n1] - c) < 0), None)
            if n2 is None:
                continue
            for want, other in ((n1, n2), (n2, n1)):
                trial = {}
                for idx, toward, sign in ((b, ew.S[want], 1), (want, c, 1), (other, c, -1)):
                    q = pts[idx]
                    m = len(q) - 1
                    score = [sign * -math.dist(q[v], toward) for v in range(m)]
                    v = int(np.argmax(score))
                    trial[idx] = q[v:-1] + q[:v] + [q[v]]
                S2, E2 = ew.S.copy(), ew.E.copy()
                for idx, q in trial.items():
                    S2[idx], E2[idx] = q[0], q[-1]
                o2, h2 = ew.walk(S2, E2, 0, None, None)
                if ew.cost(h2) < ew.cost(ew.hop) - 1e-9:
                    ew.S, ew.E, ew.order, ew.hop = S2, E2, o2, h2
                    for i2, q2 in trial.items():
                        pts[i2] = q2
                    changed += 1
                    break
        if not changed:
            break
    return [Stroke(pts[j], base[j].pen, base[j].kind, base[j].f) for j in ew.order]


# ---------------------------------------------------------------------------
# build + entry point
# ---------------------------------------------------------------------------


def build_sheet(rng: SeededRNG, bounds: Bounds, colors: int = 6) -> Tuple[Dict[Optional[int], List[Stroke]], _Map]:
    M = _Map(bounds)
    M._field_pen = _pen(BLACK, colors)
    _title(M, colors)
    _qk_block(M, colors, +1, _pen(RED, colors))
    _qk_block(M, colors, -1, _pen(BLUE, colors))
    _centre_fraction(M, colors)
    _interference(M, rng, colors)
    _softmax(M, colors)
    _v_block(M, colors)
    _moe_row(M, colors)
    _backward(M, colors)
    solid = _apply_halos(M.strokes, M)
    allst = _resolve_dots(M, solid)
    by_pen: Dict[Optional[int], List[Stroke]] = {}
    for st in allst:
        by_pen.setdefault(st.pen, []).append(st)
    return {p: _tour(v) for p, v in by_pen.items()}, M


def attention_resonance_iterate(rng: SeededRNG, bounds: Bounds, colors: int = 6) -> List[GCodeCommand]:
    """v13 kept whole, dotted continuously, streamed as a batched Leo job."""
    tours, _ = build_sheet(rng, bounds, colors)
    out: List[GCodeCommand] = []
    for pen in sorted(tours, key=lambda v: -1 if v is None else v):
        for st in tours[pen]:
            out += _poly(st.pts, color=st.pen, f=st.f)
    return out
