"""ATTENTION AS RESONANCE — r05 "benchmark-kept" (faithful; parent r01 = v13).

v13 kept as the family benchmark — same composition, same six pens, same hero —
re-cut for a real batched plot on Leo.  Every element, its position and its
marker vocabulary are still r01's, traced off
``studio/resonance/ref/attention-as-resonance.png`` (1122 x 1402 px).  What
changed is HOW each mark is made and in what order it streams:

* **Stroke IR.**  Every helper returns ``Stroke`` records (points in mm, pen,
  kind, feed) instead of G-code, so the whole sheet exists as geometry before a
  single command is emitted.  That is what makes the two sheet-level passes
  below possible.
* **Halos.**  Every label registers its glyph box (+0.9 mm); at the end every
  non-type stroke is clipped OUT of every box with the exact
  ``engine.geometry`` Region clip (Rect union, closed-form segment crossings),
  and a dot that touches a box is dropped whole.  Fans no longer run through
  ``Q.K^T / sqrt(d_k)``; droplines no longer pierce ``softmax``.
* **Dotted runs earn their cycles.**  One dot = one pen lift + drop (2 s of
  dwell on Leo).  Dots are distributed EVENLY along each run (n = round(len /
  pitch), the first and last half a pitch in from the ends, so a run never
  ends in a stub and never lands a dot on the node it feeds), and the pitch is
  set by ROLE and grows with distance from the hero:
  leader 2.8 mm < projection 3.2 mm < far rings 3.0 / 3.7 / 4.4 mm.
* **One stroke per row.**  The carrier IS the axis: r01 drew each packet row's
  axis line and then a carrier lying on it (29.5 mm of co-incident ink per row
  tail).  Now each row is one continuous carrier from node to node.
* **Weighted type in one pen-down.**  Display weight is still three offset
  passes, but chained into one stroke (forward, back, forward) instead of three.
* **Boustrophedon.**  Neighbouring runs alternate direction (fans, guides,
  droplines, upper/lower envelope), so the per-colour nearest-neighbour ordering
  in ``postprocess`` walks the sheet instead of hopping back across it.
* **Hero: same construction, drawn as ONE field.**  Same crest loci, same
  d = 35 L, same guard.  Crests now reach m = 28 (r01: 21) and are emitted
  interleaved by m, so the two families overlap across the whole central lens
  and their crossings build the dark core (r01 read as two bullseyes).
  Removed: the 60 seeded scatter marks, the dotted crest fade m = 22..51 (the
  "stipple caps") and the droplines' runs inside the crest lens.  Kept: the
  |A|-sampled spoke dots and node columns.
* **Ghost experts** are marked only at their carrier's extrema (one dot per
  crest/trough), not dotted along a 1.3 mm wave at 1.77 mm (which aliased).
* **No arrows** (house law): the gradient arrowheads become terminal discs.
* **Lineage**: Thomas Young, *Lectures on Natural Philosophy* (1807), Plate XX
  Fig. 267 — interference drawn as two concentric crest families whose
  crossings ARE the result, no tone.
* **Backward stack re-spaced**: fraction pitch 8.2 -> 9.5 mm with 2.7 mm clear
  air (r01: each denominator overlapped the next numerator).

Pens (layer order = palette index order = stream order, light -> dark so the
darkest ink always lands last and no light nib crosses wet dark ink):
0 goldenrod V · 1 dodgerblue K · 2 forestgreen Z · 3 crimson Q ·
4 darkviolet MoE/Y · 5 black interference, softmax, type.

The maths
---------
WAVE PACKET (Q, K, V, Z, the experts and Y):

    f(x)   = SUM_i A_i * exp(-((x - c_i)/s_i)^2) * cos(2*pi*(x - c_i)/L_i + p_i)
    env(x) = SUM_i A_i * exp(-((x - c_i)/s_i)^2)

INTERFERENCE (the hero): the ridge lines of
A(x, y) = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2), k = 2*pi/L, i.e. the Huygens
crest loci r_s = m L, m = 1..21 about each source; d = 35 L exactly so crest m
of one family meets crest 35-m of the other ON the axis.  ``_Guard`` drops a
crest point only where another crest runs within 0.82 mm AND within 25 degrees
of parallel, so crossings survive.

Entry point: ``attention_benchmark_kept``.
"""

from __future__ import annotations

import math
from typing import List, NamedTuple, Optional, Sequence, Tuple

from promptplot.generative.engine.geometry import Rect, Union, clip
from promptplot.generative.kit import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

REF_W, REF_H = 1122.0, 1402.0

# Pen slots in STREAM order (light -> dark).  The family grammar is by colour,
# not by slot: Q crimson, K blue, V goldenrod, Z green, MoE/Y violet, black.
OCHRE, BLUE, GREEN, RED, PURPLE, BLACK = 0, 1, 2, 3, 4, 5
PALETTE = "goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black"

PEN_MM = 0.35          # the nib this plate is drawn for (0.3-0.4 mm fineliner)

# dotted-run rhythm (dash length mm, pitch mm), by ROLE.
R_LEAD = (0.5, 2.8)    # short connectors: row feeds, block guides, backward runs
R_PROJ = (0.5, 3.6)    # projections: Q/K fans, hero droplines, return curves
R_REG = (0.45, 3.6)    # register guides of the Q/K blocks (furniture, drawn quiet)
R_FAR = [(0.45, 3.0), (0.45, 3.7), (0.45, 4.4)]   # the three far rings, outward
R_ENV = (1.2, 2.9)     # packet envelope outline

HALO_PAD = 0.9         # mm of clear paper around every label


class Stroke(NamedTuple):
    pts: List[Pt]
    pen: Optional[int]
    kind: str          # "type" | "line" | "dot"
    f: int


# ---------------------------------------------------------------------------
# sheet mapping
# ---------------------------------------------------------------------------


class _Map:
    """Reference pixels -> sheet millimetres, plus the sheet's halo registry."""

    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.sx = (x1 - x0) / REF_W
        self.sy = (y1 - y0) / REF_H
        self.halos: List[Tuple[float, float, float, float]] = []
        self.nodes: List[Tuple[float, float, float]] = []   # node keep-outs for dotted runs

    def p(self, px: float, py: float) -> Pt:
        return (self.x0 + px * self.sx, self.y1 - py * self.sy)

    def s(self, v: float) -> float:
        """Uniform length (mm) for a reference-pixel length."""
        return v * self.sx

    def halo(self, strokes: Sequence[Stroke], pad: float = HALO_PAD) -> None:
        xs = [x for st in strokes for x, _ in st.pts]
        ys = [y for st in strokes for _, y in st.pts]
        if xs:
            self.halos.append((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# stroke primitives (all in MILLIMETRES unless the name says px)
# ---------------------------------------------------------------------------


def _S(pts: Sequence[Pt], pen, kind: str = "line", f: int = 2000) -> List[Stroke]:
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    return [Stroke(list(pts), pen, kind, f)]


def _disc_mm(cx: float, cy: float, r: float, pen, kind: str = "dot") -> List[Stroke]:
    """A round dot of radius ``r`` built for a PEN_MM nib: one pen-down each.

    r <= nib/2 + 0.08: a touch (a 0.06 mm stroke) — the nib itself is the dot.
    small: one loop of radius r - nib/2, so the inked dot measures r.
    large: an Archimedean spiral at 0.3 mm pitch (solid under a 0.35 nib)."""
    h = PEN_MM / 2.0
    if r <= h + 0.08:
        return _S([(cx - 0.03, cy), (cx + 0.03, cy)], pen, kind, 1200)
    if r <= 2 * h:
        rr = r - h                          # loop radius <= nib/2: the hole closes
        return _S([(cx + rr * math.cos(2 * math.pi * k / 10), cy + rr * math.sin(2 * math.pi * k / 10))
                   for k in range(11)], pen, kind, 1200)
    turns = max(2, int(math.ceil((r - h) / 0.25)) + 1)   # spiral pitch < nib: solid
    n = turns * 24
    pts = []
    for k in range(n + 1):
        t = k / n
        rr = (r - h) * (1.0 - t)          # outside in: the spiral closes on the centre
        a = 2 * math.pi * turns * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _S(pts, pen, kind, 1600)


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


def _dotted_mm(pts: Sequence[Pt], rhythm: Tuple[float, float], pen, rev: bool = False,
               f: int = 2000) -> List[Stroke]:
    """A dotted run with its dots spread EVENLY: n = round(len / pitch) dashes,
    centred at (k + 1/2) * len / n — never a stub at an end, never a dot sitting
    on the node the run feeds.  ``rev`` draws it end -> start (boustrophedon)."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    if rev:
        pts = pts[::-1]
    cum = _cum(pts)
    L = cum[-1]
    dash, pitch = rhythm
    if L < 0.3:
        return []
    n = max(1, int(round(L / pitch)))
    p = L / n
    out: List[Stroke] = []
    for k in range(n):
        c = (k + 0.5) * p
        a, b = max(0.0, c - dash / 2), min(L, c + dash / 2)
        out += _S(_sub(pts, cum, a, b), pen, "line", f)
    return out


def _line(M: _Map, pts_px, pen, f: int = 2000) -> List[Stroke]:
    return _S([M.p(x, y) for x, y in pts_px], pen, "line", f)


def _dotted(M: _Map, pts_px, rhythm, pen, rev: bool = False) -> List[Stroke]:
    return _dotted_mm([M.p(x, y) for x, y in pts_px], rhythm, pen, rev=rev)


NODE_PAD = 0.55   # mm of clear paper a dotted run keeps from a node it passes


def _ocirc(M: _Map, px: float, py: float, r_px: float, pen, n: int = 40) -> List[Stroke]:
    cx, cy = M.p(px, py)
    M.nodes.append((cx, cy, M.s(r_px) + NODE_PAD))
    return _circle_mm(cx, cy, M.s(r_px), pen, n=n)


def _fdot(M: _Map, px: float, py: float, r_px: float, pen) -> List[Stroke]:
    cx, cy = M.p(px, py)
    r = M.s(r_px)
    if r >= 0.4:
        M.nodes.append((cx, cy, r + NODE_PAD))
    return _disc_mm(cx, cy, r, pen)


def _lead_dots(M: _Map, x_from: float, step: float, n: int, y: float, r: float, pen):
    """The '· · · ·' axis continuation.  ``step`` may be negative (leftward)."""
    out: List[Stroke] = []
    for k in range(n):
        out += _fdot(M, x_from + step * k, y, r, pen)
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


# ---------------------------------------------------------------------------
# type — the stock single-stroke caps plus the lowercase set and the two maths
# glyphs the plate needs (partial-derivative and radical); r01's letterforms.
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


def _weighted(pts: List[Pt], w: float) -> List[Pt]:
    """Offset passes of one glyph stroke (r01's weight: w across, 0.9 w up)
    chained into ONE pen-down, alternating direction.  Each join is a hop of
    <= 0.28 mm inside the stroke's own weight, so it vanishes into it."""
    if w <= 0:
        return pts
    # passes never more than 0.28 mm apart, so a 0.35 nib fuses them into one
    # solid stem (r01's 0.46 mm offsets drew hollow double outlines at 0.35)
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
          halo: bool = True) -> List[Stroke]:
    """Single-stroke type.  (px, py) is the LEFT BASELINE in reference pixels;
    glyphs are built in mm at uniform scale so they never shear.  Registers its
    box as a halo unless told not to."""
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
    return out


def _frac(M: _Map, num: str, den: str, px: float, py: float, h_px: float, pen,
          tracking: float = 1.0, gap_px: float = 4.2) -> List[Stroke]:
    """A true fraction: numerator, rule, denominator — centred on ``px``,
    with the rule at ``py``.  One halo for the whole fraction."""
    h = M.s(h_px)
    wn = _tw(num, h, tracking)
    wd = _tw(den, h, tracking)
    half = max(wn, wd) / 2.0 + M.s(2.0)
    rx, ry = M.p(px, py)
    out: List[Stroke] = []
    out += _S([(rx - half, ry), (rx + half, ry)], pen, "type", 2000)
    out += _type(M, num, px, py - h_px * 0.42 - gap_px, h_px, pen, tracking=tracking,
                 center=True, halo=False)
    out += _type(M, den, px, py + h_px * 1.02 + gap_px, h_px, pen, tracking=tracking,
                 center=True, halo=False)
    M.halo(out)
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


ENV_MIN_MM = 1.3   # the envelope outline is drawn only where it stands >= 1.3 mm off the axis


def wave_packet(M: _Map, x0: float, x1: float, y: float, packets: Sequence[Packet], pen,
                envelope: bool = True, ghost: bool = False, rev: bool = False) -> List[Stroke]:
    """One row = ONE carrier stroke from node to node (the carrier IS the axis
    where the envelope has decayed), plus the envelope outlined above and below
    as a dashed line — upper run one way, lower run back, so the pen walks."""
    lam_min = min(p[2] for p in packets)
    step = max(lam_min / 14.0, 0.18)
    n = int((x1 - x0) / step) + 1
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    if rev:
        xs = xs[::-1]
    out: List[Stroke] = []
    if ghost:
        # an unselected expert: only the carrier's EXTREMA are marked, one dot
        # at every crest and trough that stands >= 0.5 mm off the axis.  r01
        # dotted the whole carrier at 1.77 mm, which aliased a 1.3 mm wave into
        # a jumble and re-dotted the rails it overlapped.
        ex: List[Pt] = []
        for c, sg, lam, amp, ph in packets:
            k0 = int(math.floor((-3.0 * sg) / (lam / 2.0))) - 1
            for k in range(k0, -k0 + 2):
                x = c + lam * (k / 2.0 - ph / (2 * math.pi))
                if not (x0 <= x <= x1):
                    continue
                v = _pk_value(x, packets)
                if abs(v) * M.sy >= 0.5:
                    ex.append((x, y - v))
        for x, yy in sorted(ex, reverse=rev):
            out += _disc_mm(*M.p(x, yy), PEN_MM / 2.0, pen, "line")
        return out
    curve = [M.p(x, y - _pk_value(x, packets)) for x in xs]
    out += _S(curve, pen, "line", 2400)
    if envelope:
        thr = ENV_MIN_MM / M.sy
        for j, sgn in enumerate((-1.0, 1.0)):
            env = [(x, y + sgn * _pk_env(x, packets)) for x in xs]
            runs, cur = [], []
            for x, yy in env:
                if abs(yy - y) >= thr:
                    cur.append(M.p(x, yy))
                elif cur:
                    runs.append(cur)
                    cur = []
            if cur:
                runs.append(cur)
            for r in runs:
                if len(r) > 3:
                    out += _dotted_mm(r, R_ENV, pen, rev=(j == 1))
    return out


# ---------------------------------------------------------------------------
# layout constants, traced off the reference (reference pixels) — r01's
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

Q_VERTS = [  # vertical dotted guides in the Q block: (x, y_top, y_bottom)
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

MOE_Y = 1073.0
ROUTER_X, NODE2_X = 527.0, 884.0
LANE_L, LANE_R = 611.0, 789.0
LANE_YS = [1010.0, 1044.0, 1073.0, 1103.0, 1148.0]

# backward stack, RE-SPACED: pitch 41.5 -> 48 ref px (8.2 -> 9.5 mm on the sheet)
# at 11.5 px type with a 3.0 px num/den gap: 2.7 mm of clear paper between
# fractions, where r01's denominators overlapped the next numerator by 0.2 mm.
# The stack's foot stays where r01's was (15 mm above the paper edge).
BACK_ROWS = [1170.0, 1218.0, 1266.0, 1314.0, 1362.0]
BACK_H = 11.5
BACK_GAP = 3.0
BACK_COL = 282.0


# ---------------------------------------------------------------------------
# sections
# ---------------------------------------------------------------------------


def _title(M: _Map, colors: int) -> List[Stroke]:
    bk = _pen(BLACK, colors)
    out = _type(M, "ATTENTION AS RESONANCE", 561.0, TITLE_Y, 20.0, bk,
                tracking=1.72, center=True, weight=0.24)
    ax, ay = M.p(492.0, RULE_Y)
    bx, _ = M.p(630.0, RULE_Y)
    out += _S([(ax, ay), (bx, ay)], bk, "type")
    out += _fdot(M, 561.0, RULE_Y, 2.4, bk)
    return out


def _qk_block(M: _Map, colors: int, side: int, pen) -> List[Stroke]:
    """side = +1 Q (left block, continuations leftward), -1 K (right).  Each
    block carries its own traced rows and packets (r01 v7)."""

    def mx(x: float) -> float:
        return x if side > 0 else REF_W - x

    home = Q_HOME if side > 0 else K_HOME
    filled = Q_HOME_FILLED if side > 0 else K_HOME_FILLED
    out: List[Stroke] = []

    for i, y in enumerate(QK_ROWS):
        if side > 0:
            far, circ, tail = Q_ROWS[i][0], Q_ROWS[i][1], Q_ROWS[i][3]
            pk = Q_PACKETS[i]
        else:
            far, circ, tail = K_ROWS[i]
            pk = K_PACKETS[i]
        lo, hi = (home, far) if side > 0 else (far, home)
        # one stroke: the carrier runs node to node and IS the axis
        out += wave_packet(M, lo, hi, y, pk, pen, rev=(i % 2 == 1))
        if filled[i]:
            out += _fdot(M, home, y, 4.6, pen)
        else:
            out += _ocirc(M, home, y, 4.8, pen)
        if circ is not None:
            out += _ocirc(M, circ, y, 5.4, pen)
        if tail is not None:
            out += _fdot(M, tail, y, 3.4, pen)
        out += _lead_dots(M, home - side * 21.0, -side * 12.0, 4, y, 2.4, pen)

    for j, (x, yt, yb) in enumerate(Q_VERTS):
        out += _dotted(M, [(mx(x), yt), (mx(x), yb)], R_REG, pen, rev=(j % 2 == 1))
        out += _fdot(M, mx(x), yt - 6.0, 2.2, pen)

    lx = 92.0 if side > 0 else REF_W - 133.0
    out += _type(M, "Q" if side > 0 else "K", lx, 124.0, 38.0, pen, weight=0.46)

    # the convergence fans — the plate's one gesture.  Alternate direction so
    # the pen walks down one curve and back up the next.
    k = 0
    for i, y in enumerate(QK_ROWS):
        end_x = Q_ROWS[i][0] if side > 0 else REF_W - K_ROWS[i][0]
        x_start = mx(end_x + 12.0)
        tx = mx(408.0 + 15.0 * i)
        ty = 446.0 + 26.0 * i
        c1 = (mx(end_x + 86.0 + 16.0 * i), y + 10.0)
        c2 = (mx(492.0 + 6.0 * i), 352.0 + 20.0 * i)
        out += _dotted(M, _bez((x_start, y), c1, c2, (tx, ty)), R_PROJ, pen, rev=(k % 2 == 1))
        k += 1
        out += _fdot(M, tx, ty, 3.0, pen)
        c1b = (mx(end_x + 128.0 + 20.0 * i), y + 18.0)
        c2b = (mx(524.0 + 8.0 * i), 366.0 + 20.0 * i)
        tx2, ty2 = mx(386.0 + 13.0 * i), 470.0 + 24.0 * i
        out += _dotted(M, _bez((x_start, y + 6.0), c1b, c2b, (tx2, ty2)), R_PROJ, pen,
                       rev=(k % 2 == 1))
        k += 1
        out += _fdot(M, tx2, ty2, 2.2, pen)
    return out


def _centre_fraction(M: _Map, colors: int) -> List[Stroke]:
    """Q . K^T over a rule over sqrt(d_k) — a true stacked fraction."""
    bk = _pen(BLACK, colors)
    out: List[Stroke] = []
    for j in range(3):
        out += _fdot(M, 561.0, 332.0 + 11.0 * j, 1.7, bk)

    h = 23.0
    hm = M.s(h)
    num = "Q~K"
    tr = 1.16
    wn_px = _tw(num, hm, tr) / M.sx
    nx = 561.0 - 5.0
    glyphs: List[Stroke] = []
    glyphs += _type(M, num, nx, 392.0, h, bk, tracking=tr, center=True, weight=0.2, halo=False)
    glyphs += _type(M, "T", nx + wn_px / 2.0 + 1.5, 381.0, 12.5, bk, weight=0.16, halo=False)
    ax, ay = M.p(507.0, 404.0)
    bx, _ = M.p(616.0, 404.0)
    glyphs += _S([(ax, ay), (bx, ay)], bk, "type")
    glyphs += _type(M, "#d", 529.0, 434.0, 21.0, bk, tracking=1.0, weight=0.16, halo=False)
    glyphs += _type(M, "k", 568.0, 438.0, 12.0, bk, weight=0.14, halo=False)
    M.halo(glyphs, pad=1.6)
    return out + glyphs


class _Guard:
    """Parallel-crowding guard, in MILLIMETRES (r01, verbatim).

    Rejects a crest point only when a nearby point of ANOTHER stroke is within
    ``sep`` AND its tangent is within 25 degrees of parallel; crossings at any
    real angle pass straight through.
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


N_LAM = 35
LAM = IF_D / N_LAM          # 7.14 ref px = 1.21 mm across, 1.41 mm down
R_SOLID = 28     # r01: 21 — see _interference


def _interference(M: _Map, colors: int) -> List[Stroke]:
    """The hero: the Huygens crest loci r_s = m L of two sources, d = 35 L.
    r01's construction, guard and emission order verbatim — identical crests."""
    bk = _pen(BLACK, colors)
    out: List[Stroke] = []
    lam = LAM
    a_out = 272.0
    sid = 0
    guard = _Guard(0.82)

    def ring(cx: float, cy: float, r: float):
        n = max(64, int(r * 2.6))
        return [
            (cx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n))
            for t in range(n + 1)
        ]

    def emit_solid(pts):
        nonlocal sid
        sid += 1
        aa, bb = a_out * 0.80, 126.0
        res: List[Stroke] = []
        run = []
        for j, (px, py) in enumerate(pts):
            ok = ((px - IF_CX) / aa) ** 2 + ((py - IF_CY) / bb) ** 2 <= 1.0
            if ok:
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
                    res += _line(M, run, bk, f=2600)
                run = []
        if len(run) >= 4:
            res += _line(M, run, bk, f=2600)
        return res

    # Same loci, same d = 35 L, same guard.  Two changes, both to how much of the
    # field is drawn, not what it is:
    #  * crests reach m = 28 (r01: 21).  At 21 each family stopped 25 ref px past
    #    the midpoint, so the families overlapped in a 50 px sliver and the plate
    #    read as two bullseyes; at 28 they overlap across the whole central lens
    #    and their crossings build the dark interfering core the reference has.
    #  * emission interleaved by m (L1, R1, L2, R2 ...).  The guard keeps the
    #    first-drawn of two tangent crests; left-first made the left family win
    #    the whole overlap, interleaving lets each family win its own half.
    # r01's dotted crest fade m = 22..51 (the stipple caps) is cut.
    for m in range(1, R_SOLID + 1):
        for sx in (SRC_L, SRC_R):
            out += emit_solid(ring(sx, IF_CY, m * lam))

    # --- three far rings per source; dot pitch opens outward (tone = distance) --
    for sx in (SRC_L, SRC_R):
        for ia, a in enumerate((152.0, 190.0, 232.0)):
            b = a * 0.60
            rr = [
                (sx + a * math.cos(2 * math.pi * t / 240), IF_CY + b * math.sin(2 * math.pi * t / 240))
                for t in range(241)
            ]
            # a far ring stops where the solid crests are: inside the crest lens
            # AND within crest reach of a source (8 px of air)
            ok = [M.x0 + 2 < M.p(*q)[0] < M.x1 - 2
                  and not (((q[0] - IF_CX) / (a_out * 0.80 + 8.0)) ** 2
                           + ((q[1] - IF_CY) / (126.0 + 8.0)) ** 2 <= 1.0
                           and min(math.hypot(q[0] - SRC_L, q[1] - IF_CY),
                                   math.hypot(q[0] - SRC_R, q[1] - IF_CY)) <= R_SOLID * lam + 8.0)
                  for q in rr]
            runs, cur = [], []
            for q, o in zip(rr, ok):
                if o:
                    cur.append(q)
                elif cur:
                    runs.append(cur)
                    cur = []
            if cur:
                runs.append(cur)
            for r in runs:
                if len(r) > 6:
                    out += _dotted(M, r, R_FAR[ia], bk)

    # --- the horizontal axis through the figure ---------------------------
    ax, ay = M.p(300.0, IF_CY)
    bx, _ = M.p(822.0, IF_CY)
    out += _S([(ax, ay), (bx, ay)], bk)
    for sgn in (1, -1):
        base = IF_CX - sgn * 334.0
        out += _ocirc(M, base, IF_CY, 5.0, bk)
        for j in range(4):
            out += _fdot(M, base - sgn * (17.0 + 17.0 * j), IF_CY, 2.3, bk)
        out += _fdot(M, IF_CX - sgn * 305.0, IF_CY, 3.2, bk)
        out += _fdot(M, IF_CX - sgn * 266.0, IF_CY, 3.4, bk)
        cxx = IF_CX - sgn * 203.0
        out += _ocirc(M, cxx, IF_CY, 6.2, bk)
        out += _fdot(M, cxx, IF_CY, 2.2, bk)
    out += _fdot(M, IF_CX, IF_CY, 5.0, bk)
    out += _fdot(M, SRC_L, IF_CY, 4.8, bk)
    out += _fdot(M, SRC_R, IF_CY, 4.8, bk)

    # --- the dot field, sampled from the same A --------------------------
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
        return _fdot(M, px, py, r, bk)

    for cx in (SRC_L, IF_CX, SRC_R):
        for j in range(-6, 7):
            if j:
                out += place(cx, IF_CY + 24.0 * j, 1.7 + 4.2 * math.exp(-abs(j) / 3.4))
    for sx in (SRC_L, SRC_R):
        for t in range(12):
            th = 2 * math.pi * t / 12 + 0.09
            for rr_ in (46.0, 84.0, 122.0, 160.0, 198.0):
                px = sx + rr_ * math.cos(th)
                py = IF_CY + rr_ * 0.62 * math.sin(th)
                out += place(px, py, 1.1 + 22.0 * abs(field(px, py)))
    # r01 added 60 seeded scatter marks here — cut: they muddied the crest net.

    # --- vertical dotted droplines, up and down (boustrophedon) -----------
    # They stop at the solid-crest lens: inside it a dot lands between crest
    # lines 1.2 mm apart and reads as mud, not as a line (r01 ran them through).
    drops = [434.0, 477.0, 516.0, 561.0, 613.0, 652.0, 691.0]
    aa, bb = a_out * 0.80, 126.0
    for j, x in enumerate(drops):
        half = bb * math.sqrt(max(0.0, 1.0 - ((x - IF_CX) / aa) ** 2)) + 6.0
        top = 462.0 if x in (434.0, 561.0, 691.0) else 496.0
        if IF_CY - half - top > 8.0:
            out += _dotted(M, [(x, top), (x, IF_CY - half)], R_PROJ, bk, rev=(j % 2 == 1))
        out += _fdot(M, x, top - 8.0, 2.0, bk)
        bot = 832.0 if j % 2 == 0 else 806.0
        out += _dotted(M, [(x, IF_CY + half), (x, bot)], R_PROJ, bk, rev=(j % 2 == 0))
    out += _ocirc(M, IF_CX, 486.0, 4.8, bk)
    out += _ocirc(M, IF_CX, 716.0, 4.8, bk)
    return out


def _softmax(M: _Map, colors: int) -> List[Stroke]:
    bk = _pen(BLACK, colors)
    out: List[Stroke] = []
    x0, x1 = 313.0, 806.0

    def curve_y(x: float) -> float:
        v = 0.0
        for cx, h, _m in SOFT_PEAKS:
            v += h / (1.0 + ((x - cx) / 9.5) ** 2) ** 1.6
        return SOFT_BASE - v

    n = int((x1 - x0) / 0.7)
    out += _line(M, [(x0 + k * (x1 - x0) / n, curve_y(x0 + k * (x1 - x0) / n)) for k in range(n + 1)],
                 bk, f=2400)

    for cx, h in SOFT_GHOSTS:
        gp = [
            (cx - 26.0 + t * 0.9, SOFT_BASE - h / (1.0 + ((cx - 26.0 + t * 0.9 - cx) / 8.0) ** 2) ** 1.6)
            for t in range(59)
        ]
        out += _dotted(M, gp, (0.42, 1.9), bk)

    for cx, h, m in SOFT_PEAKS:
        out += _line(M, [(cx, SOFT_BASE), (cx, SOFT_BASE - h + 2.0)], bk)
        if m == "o":
            out += _ocirc(M, cx, SOFT_BASE - h - 3.0, 5.0, bk)
        elif m == "f":
            out += _fdot(M, cx, SOFT_BASE - h - 3.0, 4.4, bk)

    for x, kind in [
        (321.0, "f"), (391.0, "f"), (434.0, "o"), (475.0, "o"), (516.0, "f"),
        (559.0, "o"), (601.0, "o"), (645.0, "o"), (686.0, "o"), (724.0, "f"), (799.0, "f"),
    ]:
        if kind == "o":
            out += _ocirc(M, x, SOFT_BASE, 4.4, bk)
        else:
            out += _fdot(M, x, SOFT_BASE, 3.2, bk)

    out += _lead_dots(M, 303.0, -14.0, 3, SOFT_BASE, 2.4, bk)
    out += _lead_dots(M, 818.0, 14.0, 3, SOFT_BASE, 2.4, bk)
    out += _type(M, "softmax", 561.0, 786.0, 20.0, bk, tracking=1.16, center=True, weight=0.16)
    return out


def _v_block(M: _Map, colors: int) -> List[Stroke]:
    oc = _pen(OCHRE, colors)
    out: List[Stroke] = []
    packs = [
        [(903.0, 32.0, 12.5, 28.0, 0.0), (800.0, 17.0, 9.0, 12.0, 0.5)],
        [(862.0, 27.0, 11.5, 25.0, 0.0), (778.0, 15.0, 8.5, 13.0, 0.8)],
        [(878.0, 25.0, 14.0, 22.0, 0.0), (790.0, 14.0, 9.5, 11.0, 0.3)],
    ]
    for i, y in enumerate(V_ROWS):
        out += wave_packet(M, V_L, V_R, y, packs[i], oc, rev=(i % 2 == 1))
        if i == 2:
            out += _fdot(M, V_L, y, 4.4, oc)
        else:
            out += _ocirc(M, V_L, y, 4.8, oc)
        out += _ocirc(M, V_R, y, 4.8, oc)
        out += _lead_dots(M, V_R + 24.0, 14.0, 4, y, 2.4, oc)
        out += _dotted(M, [(688.0, y), (V_L - 8.0, y)], R_LEAD, oc)
        out += _fdot(M, 684.0, y, 2.2, oc)
    out += _type(M, "V", 1022.0, 748.0, 34.0, oc, weight=0.46)
    for i, x in enumerate([391.0, 434.0, 475.0, 516.0, 559.0, 601.0]):
        pts = _bez((x, SOFT_BASE + 8.0), (x + 4.0, 960.0), (x + 46.0 + 9.0 * i, 1010.0),
                   (x + 74.0 + 12.0 * i, 1080.0))
        out += _dotted(M, pts, R_PROJ, oc, rev=(i % 2 == 1))
    out += _dotted(M, _bez((975.0 + 22.0, V_ROWS[2]), (1070.0, 900.0), (1010.0, 1010.0),
                           (NODE2_X + 16.0, MOE_Y - 6.0)), R_PROJ, oc)
    return out


def _moe_row(M: _Map, colors: int) -> List[Stroke]:
    gr = _pen(GREEN, colors)
    pu = _pen(PURPLE, colors)
    bk = _pen(BLACK, colors)
    out: List[Stroke] = []

    # ---- Z = AV ---------------------------------------------------------
    zp: List[Packet] = [
        (277.0, 47.0, 13.5, 68.0, 0.0),
        (178.0, 13.0, 8.5, 15.0, 0.4),
        (443.0, 13.0, 8.5, 14.0, 0.9),
        (352.0, 9.0, 7.5, 8.0, 0.2),
    ]
    out += wave_packet(M, 110.0, ROUTER_X - 14.0, MOE_Y, zp, gr)
    out += _ocirc(M, 110.0, MOE_Y, 4.8, gr)
    for x in (178.0, 315.0, 443.0, 490.0):
        out += _ocirc(M, x, MOE_Y, 4.4, gr)
    out += _lead_dots(M, 88.0, -13.0, 4, MOE_Y, 2.4, gr)
    out += _fdot(M, 277.0, MOE_Y - 72.0, 4.6, gr)
    out += _fdot(M, 277.0, MOE_Y + 72.0, 4.6, gr)
    out += _type(M, "Z = AV", 90.0, 1018.0, 30.0, gr, tracking=0.98, weight=0.42)

    # ---- MoE header -----------------------------------------------------
    out += _type(M, "MoE", 706.0, 948.0, 22.0, bk, tracking=1.02, center=True, weight=0.2)
    for a, b in ((618.0, 668.0), (746.0, 796.0)):
        out += _S([M.p(a, 941.0), M.p(b, 941.0)], bk, "type")
    out += _type(M, "experts", 714.0, 976.0, 15.0, pu, tracking=1.1, center=True)
    out += _type(M, "top-2", 848.0, 999.0, 15.0, pu, tracking=1.1, center=True)
    out += _type(M, "router", 529.0, 1049.0, 15.0, pu, tracking=1.1, center=True)

    # ---- router / gather nodes -----------------------------------------
    for nx in (ROUTER_X, NODE2_X):
        out += _ocirc(M, nx, MOE_Y, 12.5, pu)
        out += _ocirc(M, nx, MOE_Y, 8.0, pu)
        out += _fdot(M, nx, MOE_Y, 3.4, pu)

    # ---- expert lanes ---------------------------------------------------
    lane_pk: List[List[Packet]] = [
        [(700.0, 23.0, 8.0, 24.0, 0.0), (743.0, 12.0, 6.6, 11.0, 0.7)],
        [(700.0, 20.0, 7.6, 10.0, 0.0)],
        [(700.0, 20.0, 7.6, 10.0, 0.4)],
        [(700.0, 20.0, 7.6, 10.0, 0.8)],
        [(706.0, 27.0, 8.0, 27.0, 0.0), (752.0, 13.0, 6.8, 12.0, 0.5)],
    ]
    for i, y in enumerate(LANE_YS):
        if i in (0, 4):   # top-2: the two selected experts, solid
            out += wave_packet(M, LANE_L, LANE_R, y, lane_pk[i], pu, rev=(i == 4))
            out += _ocirc(M, LANE_L, y, 5.6, pu)
            out += _ocirc(M, LANE_R, y, 5.6, pu)
            out += _line(M, _bez((ROUTER_X + 13.0, MOE_Y), (ROUTER_X + 58.0, MOE_Y),
                                 (LANE_L - 42.0, y), (LANE_L - 6.0, y)), pu)
            out += _line(M, _bez((LANE_R + 6.0, y), (LANE_R + 42.0, y),
                                 (NODE2_X - 50.0, MOE_Y), (NODE2_X - 13.0, MOE_Y)), pu)
            out += _fdot(M, LANE_L - 24.0, y, 3.0, pu)
            out += _fdot(M, LANE_R + 26.0, y, 3.0, pu)
        else:             # the three unselected experts: ghosts
            out += _dotted(M, [(LANE_L, y), (LANE_L + 52.0, y)], R_LEAD, pu)
            out += _dotted(M, [(LANE_R - 52.0, y), (LANE_R, y)], R_LEAD, pu)
            out += wave_packet(M, LANE_L + 8.0, LANE_R - 8.0, y, lane_pk[i], pu,
                               envelope=False, ghost=True)
            out += _ocirc(M, LANE_L, y, 5.0, pu, n=28)
            out += _ocirc(M, LANE_R, y, 5.0, pu, n=28)
            out += _dotted(M, _bez((ROUTER_X + 13.0, MOE_Y), (ROUTER_X + 54.0, MOE_Y),
                                   (LANE_L - 40.0, y), (LANE_L - 6.0, y)), R_LEAD, pu)
            out += _dotted(M, _bez((LANE_R + 6.0, y), (LANE_R + 40.0, y),
                                   (NODE2_X - 48.0, MOE_Y), (NODE2_X - 13.0, MOE_Y)), R_LEAD, pu)

    # ---- Y --------------------------------------------------------------
    yp: List[Packet] = [(978.0, 31.0, 11.0, 40.0, 0.0), (1030.0, 11.0, 7.5, 11.0, 0.6)]
    out += wave_packet(M, NODE2_X + 14.0, 1052.0, MOE_Y, yp, pu)
    out += _ocirc(M, 1052.0, MOE_Y, 4.8, pu)
    out += _lead_dots(M, 1072.0, 13.0, 3, MOE_Y, 2.4, pu)
    out += _type(M, "Y", 1020.0, 1030.0, 30.0, pu, weight=0.46)
    return out


TERM_GAP = 12.0   # ref px from a fraction's rule end to its terminal disc (2 mm)


def _frac_half_px(M: _Map, num: str, den: str, h_px: float, tracking: float) -> float:
    h = M.s(h_px)
    return (max(_tw(num, h, tracking), _tw(den, h, tracking)) / 2.0 + M.s(2.0)) / M.sx


def _backward(M: _Map, colors: int) -> List[Stroke]:
    out: List[Stroke] = []
    pens = [_pen(RED, colors), _pen(BLUE, colors), _pen(OCHRE, colors),
            _pen(BLACK, colors), _pen(GREEN, colors)]
    dens = ["Q", "K", "V", "A", "Z"]
    for i, y in enumerate(BACK_ROWS):
        pn = pens[i]
        out += _frac(M, "@L", "@" + dens[i], 62.0, y, BACK_H, pn, tracking=1.02, gap_px=BACK_GAP)
        tx0 = 62.0 + _frac_half_px(M, "@L", "@" + dens[i], BACK_H, 1.02) + TERM_GAP
        out += _fdot(M, tx0, y, 3.6, pn)             # terminal disc, not an arrowhead
        out += _dotted(M, [(tx0 + 9.0, y), (BACK_COL - 7.0, y)], R_LEAD, pn)
        out += _ocirc(M, BACK_COL, y, 4.6, pn)
        tx = 500.0 + 58.0 * i
        ty = 1010.0 - 14.0 * i
        out += _dotted(M, _bez((BACK_COL + 7.0, y), (BACK_COL + 120.0 + 20.0 * i, y),
                               (tx - 120.0, ty + 90.0), (tx, ty)), R_PROJ, pn, rev=True)

    for xx, pn, y_to in ((336.0, _pen(RED, colors), 1180.0),
                         (377.0, _pen(BLUE, colors), 1160.0),
                         (415.0, _pen(OCHRE, colors), 1145.0)):
        out += _dotted(M, [(xx, MOE_Y + 26.0), (xx, y_to)], R_LEAD, pn)
        out += _fdot(M, xx, MOE_Y + 22.0, 2.2, pn)

    out += _dotted(M, [(BACK_COL, MOE_Y + 84.0), (BACK_COL, BACK_ROWS[-1] - 7.0)], R_LEAD,
                   _pen(GREEN, colors))

    pu = _pen(PURPLE, colors)
    labels = [("Y", 1191.0), ("experts", 1265.0), ("router", 1321.0)]
    term = {}
    for name, y in labels:
        h = 14.0 if len(name) < 4 else 11.5
        out += _frac(M, "@L", "@" + name, 1052.0, y, h, pu, tracking=1.0)
        term[name] = 1052.0 - _frac_half_px(M, "@L", "@" + name, h, 1.0) - TERM_GAP
        out += _fdot(M, term[name], y, 3.6, pu)       # terminal disc, not an arrowhead
    out += _dotted(M, _bez((940.0, 1120.0), (985.0, 1150.0), (term["Y"] - 40.0, 1178.0),
                           (term["Y"] - 9.0, 1191.0)), R_LEAD, pu)
    # routing skeleton: one continuous dotted path per branch, walked in order
    out += _dotted(M, [(796.0, 1175.0), (796.0, 1265.0), (term["experts"] - 9.0, 1265.0)], R_LEAD, pu)
    out += _dotted(M, [(718.0, 1175.0), (718.0, 1321.0), (term["router"] - 9.0, 1321.0)], R_LEAD, pu)
    out += _dotted(M, [(977.0, 1270.0), (977.0, 1316.0)], R_LEAD, pu)
    for nx, ny in ((718.0, 1238.0), (796.0, 1238.0), (718.0, 1291.0), (718.0, 1321.0),
                   (977.0, 1265.0), (977.0, 1321.0)):
        out += _ocirc(M, nx, ny, 4.2, pu, n=28)
    return out


# ---------------------------------------------------------------------------
# sheet passes: halos, then emit
# ---------------------------------------------------------------------------


def _length(pts: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def _apply_halos(strokes: List[Stroke], M: _Map) -> List[Stroke]:
    """Clip every non-type stroke OUT of every label box (exact Region clip);
    a dot or small circle that touches a box is dropped whole."""
    boxes = M.halos
    out: List[Stroke] = []
    for st in strokes:
        if st.kind == "type":
            out.append(st)
            continue
        if st.kind == "line" and _length(st.pts) < 1.6 and any(
                math.hypot(x - nx, y - ny) < nr for x, y in st.pts[:: max(1, len(st.pts) - 1)]
                for nx, ny, nr in M.nodes):
            continue            # a dot/dash of a dotted run sitting on a node
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
            if sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(run[:-1], run[1:])) >= 0.3:
                out.append(Stroke(run, st.pen, st.kind, st.f))
    return out


def _emit(strokes: Sequence[Stroke]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for st in strokes:
        out += _poly(st.pts, color=st.pen, f=st.f)
    return out


def build_strokes(bounds: Bounds, colors: int = 6) -> Tuple[List[Stroke], _Map]:
    M = _Map(bounds)
    s: List[Stroke] = []
    # type-bearing sections first is not required: halos apply at the end
    s += _title(M, colors)
    s += _qk_block(M, colors, +1, _pen(RED, colors))
    s += _qk_block(M, colors, -1, _pen(BLUE, colors))
    s += _centre_fraction(M, colors)
    s += _interference(M, colors)
    s += _softmax(M, colors)
    s += _v_block(M, colors)
    s += _moe_row(M, colors)
    s += _backward(M, colors)
    return _apply_halos(s, M), M


def attention_benchmark_kept(rng: SeededRNG, bounds: Bounds, colors: int = 6) -> List[GCodeCommand]:
    """Deterministic: the r05 plate uses no randomness (r01's only random draw
    was the 60 scatter marks, now cut); ``rng`` is kept for the contract."""
    strokes, _ = build_strokes(bounds, colors)
    return _emit(strokes)
