"""ATTENTION AS RESONANCE (FFN) — r04 · iterate · parent r01 (v9).

r01/v9 is THE DESIGN (Juan, 2026-09-28: "the original was much more beautiful — we
just needed the dot lines to be more continuous").  This round keeps v9's
composition, every element and all six pens exactly where r01 draws them, and
changes only HOW MARKS ARE MADE and HOW THE SHEET STREAMS.

What changed from r01, and nothing else
---------------------------------------
1. A stroke IR.  Every section of r01 (transcribed below with r01's reference-pixel
   coordinates, packet tables and crest maths untouched) now appends ``Mark``s to a
   ``Sheet`` instead of writing G-code.  The whole plate exists as geometry before a
   single command is emitted, so non-destructive passes can run over it:
     * label halos — dots clipped out of every label box + 0.9 mm;
     * node keep-outs — no dot within 0.55 mm of a node circle / disc;
     * no invisible dots — no dot within 0.30 mm of same-pen ink, no two same-pen
       dots within 0.60 mm (co-incident);
     * the carrier is the axis — a row's straight axis is not redrawn where the
       carrier already lies on it (envelope < 0.15 mm);
     * fused marks — type weight passes, arrowheads and discs are one pen-down.
2. Two dot classes.
     * Dotted LINES (fans, leaders, droplines, ochre falls, continuations, halo
       ellipses, envelope outlines, arrow shafts) take THE family dot: one closed
       loop of radius DOT_R = 0.15 mm at DOT_PITCH = 1.0 mm centre to centre, end-
       anchored (n = round(L / pitch), n + 1 dots) — resonance r10's constants.
     * TEXTURES (the hero's and the twin's stipple caps = the dotted crest fade,
       and the scattered field dots) keep r01's mark count and positions: each r01
       micro-dash becomes one round dot at its own centre, never re-pitched.
   Every former ``_fdot`` is a round mark by radius (a loop, or r01's spiral disc),
   never a ``-`` tick.
3. Halo ellipses are cut into their real arcs, each stopping ON the curve at the
   crest keep-out (found by bisection), joined through the parameter seam — no flat
   chords, no stub.
4. Collisions fixed without deleting: the FFN bracket's right leg re-aimed onto the
   project|Y pinch node, ``FFN`` lifted 2 mm, the prime of ``nonlinearity′`` set
   against its word, ``∂L/∂A`` given 1.5 mm of clear air.
5. Streaming: each pen is one layer, ordered greedy nearest-END with reversal from
   the machine origin on the G-code's own 0.01 mm coordinates, so the post-
   processor's nearest-START pass reproduces the order exactly (verified stroke
   for stroke).  ``_polish`` then repairs stragglers by flipping stroke
   directions — the one variable the post-processor keeps — re-simulating its
   pass each time.  Stream light -> dark with ``--layers 2,1,3,0,4,5``.
6. Converging dotted lines never braid: ``_lay_trains`` phase-locks a dotted line
   to an earlier same-pen line running within 2 mm (dots side by side), and a line
   that closes to under 0.9 mm at one of its ends stops early on a dot.

Lineage: Charles Csuri & James Shaffer, *Sine Curve Man* (1967) — a form and its
function-mapped copy on one plotter sheet: the forward FFN row and its transposed
backward row, the hero field and its 0.39-scale ∂L/∂A copy.  Depth: flat —
reproduction of a flat plate diagram.

Pens (family indices, kept): 0 crimson Q · 1 dodgerblue K · 2 goldenrod V ·
3 forestgreen Z · 4 darkviolet FFN/Y · 5 black field, softmax, type, bracket.

Entry point: ``attention_as_resonance_ffn_iterate``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import _GLYPHS, _glyph_advance, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

REF_W, REF_H = 1122.0, 1402.0

# palette slots — crimson, dodgerblue, goldenrod, forestgreen, darkviolet, black
RED, BLUE, OCHRE, GREEN, PURPLE, BLACK = 0, 1, 2, 3, 4, 5
STREAM_LAYERS = (OCHRE, BLUE, GREEN, RED, PURPLE, BLACK)    # light -> dark

PEN_MM = 0.35            # the nib the plate is drawn for (0.3-0.4 mm fineliner)

# THE family dot (shared with resonance r10 / resonance-backprop).
DOT_PITCH = 1.0          # mm, centre to centre, end-anchored
DOT_R = 0.15             # mm, radius of the closed loop the pen draws

HALO_PAD = 0.9           # mm of clear paper round every label (dots only)
NODE_KEEP = 0.55         # mm of clear paper round every node, for dots
INK_KEEP = 0.30          # a dot centre this close to same-pen ink is invisible
COINCIDENT = 0.60        # two same-pen dots this close are one dot
AXIS_TOL = 0.15          # mm: where the envelope is below this the carrier IS the axis


# ---------------------------------------------------------------------------
# sheet mapping (r01, unchanged)
# ---------------------------------------------------------------------------


class _Map:
    """Reference pixels -> sheet millimetres."""

    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.sx = (x1 - x0) / REF_W
        self.sy = (y1 - y0) / REF_H

    def p(self, px: float, py: float) -> Pt:
        return (self.x0 + px * self.sx, self.y1 - py * self.sy)

    def s(self, v: float) -> float:
        """Uniform length (mm) for a reference-pixel length."""
        return v * self.sx


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# the stroke IR
# ---------------------------------------------------------------------------


class Mark:
    """One pen-down.  kind: line | axis | type | node | dash | dot | tex.

    ``dot`` is a family dot on a dotted LINE (``train`` = which line, ``seq`` =
    its index along it); ``tex`` is a texture mark (stipple or scatter)."""

    __slots__ = ("pts", "pen", "kind", "f", "c", "r", "train", "seq", "y")

    def __init__(self, pts, pen, kind="line", f=2000, c=None, r=0.0, train=-1, seq=0, y=None):
        self.pts = pts
        self.pen = pen
        self.kind = kind
        self.f = f
        self.c = c
        self.r = r
        self.train = train
        self.seq = seq
        self.y = y


class Sheet:
    def __init__(self, M: _Map, colors: int) -> None:
        self.M = M
        self.colors = colors
        self.marks: List[Mark] = []
        self.boxes: List[Tuple[float, float, float, float]] = []   # already padded
        self.carriers: List[tuple] = []
        self.trains: Dict[int, dict] = {}
        self.log: Dict[str, int] = {}
        self.stream: Dict[object, dict] = {}

    def add(self, m: Mark) -> None:
        self.marks.append(m)

    def box(self, pts: Sequence[Pt], pad: float = HALO_PAD) -> None:
        if not pts:
            return
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.boxes.append((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))


def _loop(cx: float, cy: float, r: float, n: int = 8) -> List[Pt]:
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
            for k in range(n + 1)]


def _S(SH: Sheet, pts: Sequence[Pt], pen, kind: str = "line", f: int = 2000, y=None) -> None:
    pts = [p for p in pts if p is not None]
    if len(pts) >= 2:
        SH.add(Mark(list(pts), pen, kind, f, y=y))


def _line(SH: Sheet, pts, pen=None, f: int = 2000, kind: str = "line") -> None:
    _S(SH, [SH.M.p(x, y) for x, y in pts], pen, kind, f)


def _round(SH: Sheet, cx: float, cy: float, r: float, pen, kind: str = "node") -> None:
    """A round mark of radius r (mm), ONE pen-down, never a tick.

    r <= 0.32: a closed loop of radius r - 0.12 (floor 0.06) — a pen touch that
    inks a round dot of about r.  Larger: r01's spiral disc (kit.fill_disc
    geometry, spacing 0.3), so every disc on v9 keeps its size and weight."""
    if r <= 0.32:
        rl = max(0.06, r - 0.12)
        pts = _loop(cx, cy, rl, 10)
        f = 1200
    else:
        turns = max(2, int(r / 0.3))
        n = turns * 30
        pts = []
        for k in range(n + 1):
            t = k / n
            rr = r * t
            a = 2 * math.pi * turns * t
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        f = 2200
    SH.add(Mark(pts, pen, kind, f, c=(cx, cy), r=r))


def _fdot(SH: Sheet, px: float, py: float, r_px: float, pen=None, kind: str = "node") -> None:
    cx, cy = SH.M.p(px, py)
    _round(SH, cx, cy, max(SH.M.s(r_px), 0.14), pen, kind)


def _ocirc(SH: Sheet, px: float, py: float, r_px: float, pen=None, n: int = 40) -> None:
    cx, cy = SH.M.p(px, py)
    r = SH.M.s(r_px)
    SH.add(Mark(_loop(cx, cy, r, n), pen, "node", 2200, c=(cx, cy), r=r))


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


def _the_dot(SH: Sheet, cx: float, cy: float, pen, train: int = -1, seq: int = 0,
             kind: str = "dot") -> None:
    """THE dot: a closed loop of radius DOT_R, one pen-down, always the same."""
    SH.add(Mark(_loop(cx, cy, DOT_R, 8), pen, kind, 1200, c=(cx, cy), r=DOT_R,
                train=train, seq=seq))


def _dotline(SH: Sheet, pts: Sequence[Pt], pen, tag: str = "") -> int:
    """Register a dotted LINE (mm).  Its dots are laid later, by ``_lay_trains``,
    once every other dotted line on the sheet is known (phase-locking needs them)."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return -1
    tid = len(SH.trains)
    SH.trains[tid] = dict(pen=pen, tag=tag, path=list(pts), length=_cum(pts)[-1])
    return tid


LOCK = 2.0               # mm: same-pen trains closer than this, near-parallel, are phase-locked
MERGE = 0.9              # mm: closer than this they are one line — the later one ends early
PARALLEL = 0.8           # |cos| above which two trains run together


def _lay_trains(SH: Sheet) -> None:
    """Lay the family dots on every registered dotted line.

    Free stretches: DOT_PITCH, end-anchored (n = round(L / pitch), n + 1 dots).
    Where a line runs within LOCK of an earlier same-pen line and near-parallel,
    its dots are PHASE-LOCKED — placed at the projections of the earlier line's
    dots — so the two read as two dotted lines side by side instead of braiding
    into noise.  Where it closes to under MERGE at one of its ENDS (a converging
    bundle), it ENDS EARLY on a dot; no path is deleted."""
    stats = {"locked": 0, "trimmed_mm": 0.0, "trains": 0}
    acc: Dict[object, Dict[Tuple[int, int], List[tuple]]] = {}   # pen -> grid of accepted dots
    CELL = 2.0
    for tid, tr in SH.trains.items():
        pen, path = tr["pen"], tr["path"]
        cum = _cum(path)
        L = cum[-1]
        stats["trains"] += 1
        if L < 0.5:
            x, y = path[0]
            _the_dot(SH, x, y, pen, tid, 0)
            continue
        # dense resample for projection
        n_s = max(2, int(L / 0.1))
        ss = [L * i / n_s for i in range(n_s + 1)]
        P = [_at(path, cum, s) for s in ss]
        grid = acc.setdefault(pen, {})
        anchors: List[Tuple[float, float]] = []      # (s, separation)
        seen = set()
        for i, (x, y) in enumerate(P):
            a = P[max(i - 1, 0)]
            b = P[min(i + 1, n_s)]
            tx, ty = b[0] - a[0], b[1] - a[1]
            tn = math.hypot(tx, ty) or 1.0
            tx, ty = tx / tn, ty / tn
            gx, gy = int(x // CELL), int(y // CELL)
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    for (qx, qy, ux, uy, key) in grid.get((gx + di, gy + dj), ()):
                        d = math.hypot(qx - x, qy - y)
                        if d >= LOCK or abs(tx * ux + ty * uy) < PARALLEL:
                            continue
                        # the projection foot: the sample where the dot is nearest
                        if key in seen:
                            continue
                        best_i, best_d = i, d
                        for j in range(max(0, i - 30), min(n_s, i + 30) + 1):
                            dj_ = math.hypot(qx - P[j][0], qy - P[j][1])
                            if dj_ < best_d:
                                best_i, best_d = j, dj_
                        seen.add(key)
                        anchors.append((ss[best_i], best_d))
        s0, s1 = 0.0, L
        merge = sorted(s for s, d in anchors if d < MERGE)
        if merge:
            # contiguous merge zone touching an end -> end early on a dot
            tail = [s for s in merge if s > L - 3.0]
            if tail:
                zone = [s for s in merge if s >= min(tail) - 1.6]
                lo = min(zone)
                while True:
                    near = [s for s in merge if lo - 1.6 <= s < lo]
                    if not near:
                        break
                    lo = min(near)
                s1 = max(0.0, lo - DOT_PITCH)
            head = [s for s in merge if s < 3.0]
            if head:
                hi = max(head)
                while True:
                    near = [s for s in merge if hi < s <= hi + 1.6]
                    if not near:
                        break
                    hi = max(near)
                s0 = min(s1, hi + DOT_PITCH)
        stats["trimmed_mm"] += (L - s1) + s0
        # nearest neighbour wins: accept anchors by increasing separation, never
        # two within 0.7 mm of arclength, the two end dots always first
        kept: List[float] = [s0, s1] if s1 - s0 >= 0.7 else [s0]
        for s, d in sorted(anchors, key=lambda a: a[1]):
            if s0 + 0.35 < s < s1 - 0.35 and all(abs(s - k) >= 0.7 for k in kept):
                kept.append(s)
        kept.sort()
        stats["locked"] += len(kept) - 2
        dots: List[float] = []
        for a_, b_ in zip(kept[:-1], kept[1:]):
            n = max(1, int(round((b_ - a_) / DOT_PITCH)))
            dots += [a_ + (b_ - a_) * k / n for k in range(n)]
        dots.append(kept[-1])
        if s1 - s0 < 0.5:
            dots = [s0]
        for k, s in enumerate(dots):
            x, y = _at(path, cum, s)
            _the_dot(SH, x, y, pen, tid, k)
            a = _at(path, cum, max(0.0, s - 0.3))
            b = _at(path, cum, min(L, s + 0.3))
            ux, uy = b[0] - a[0], b[1] - a[1]
            un = math.hypot(ux, uy) or 1.0
            grid.setdefault((int(x // CELL), int(y // CELL)), []).append(
                (x, y, ux / un, uy / un, (tid, k)))
    SH.log.update({k: round(v, 1) if isinstance(v, float) else v for k, v in stats.items()})


def _texline(SH: Sheet, pts: Sequence[Pt], dash: float, gap: float, pen,
             step: float = 0.20) -> None:
    """A TEXTURE: r01's own micro-dash sampling (step 0.20 mm), each dash
    replaced by ONE round dot at its centre — r01's mark count and positions."""
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
    run: List[Pt] = []
    for x, y, ss in samples + [(None, None, None)]:
        if ss is not None and (ss % period) < dash:
            run.append((x, y))
            continue
        if run:
            mx_, my_ = run[len(run) // 2]
            _the_dot(SH, mx_, my_, pen, kind="tex")
        run = []


def _longdash(SH: Sheet, pts: Sequence[Pt], dash: float, gap: float, pen,
              step: float = 0.20) -> None:
    """r01's real dashes (only the 2.6 mm axis into the ∂L/∂A figure)."""
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
    run: List[Pt] = []
    for x, y, ss in samples + [(None, None, None)]:
        if ss is not None and (ss % period) < dash:
            run.append((x, y))
            continue
        if len(run) >= 2:
            _S(SH, run, pen, "dash", 2000)
        run = []


def _dash_mm(SH: Sheet, pts, dash: float, gap: float, pen=None, cls: str = "line",
             tag: str = "") -> None:
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return
    if cls == "tex":
        _texline(SH, pts, dash, gap, pen)
    elif dash > 1.2:
        _longdash(SH, pts, dash, gap, pen)
    else:
        _dotline(SH, pts, pen, tag)


def _dash(SH: Sheet, pts, dash: float = 0.45, gap: float = 1.55, pen=None, cls: str = "line",
          tag: str = "") -> None:
    """Dotted path given in REFERENCE PIXELS."""
    _dash_mm(SH, [SH.M.p(x, y) for x, y in pts], dash, gap, pen, cls, tag)


def _lead_dots(SH: Sheet, x_from: float, step: float, n: int, y: float, r: float, pen=None):
    """The '· · · ·' axis continuation, now a family dotted line over r01's span."""
    _dotline(SH, [SH.M.p(x_from, y), SH.M.p(x_from + step * (n - 1), y)], pen, "lead")


def _bez(p0, c1, c2, p1, n: int = 64):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        x = u * u * u * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * p1[0]
        y = u * u * u * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * p1[1]
        out.append((x, y))
    return out


def _arrow(SH: Sheet, px: float, py: float, direction: int, size_px: float = 8.0, pen=None):
    """r01's solid arrowhead — outline + fill lines at 0.32 mm — as ONE pen-down.

    r01's fill ran from the BASE to where the far edge would be mirrored, so its
    centre line had zero length and v9's heads plotted hollow; the fill now spans
    base to slanted edge at every height, which is the solid head r01 describes."""
    cx, cy = SH.M.p(px, py)
    L = SH.M.s(size_px)
    hb = L * 0.62
    path = [(cx, cy), (cx - direction * L, cy + hb), (cx - direction * L, cy - hb), (cx, cy)]
    n = max(2, int(hb * 2 / 0.32))
    for i in range(1, n):
        t = i / n
        yy = -hb + 2 * hb * t
        frac = abs(yy) / hb        # r01 had 1 - |yy|/hb: the fill ran the wrong way
        a = (cx - direction * L * frac, cy + yy)
        b = (cx - direction * L, cy + yy)
        path += [a, b] if i % 2 else [b, a]
    SH.add(Mark(path, pen, "node", 1600, c=(cx - direction * L * 0.45, cy), r=hb))


# ---------------------------------------------------------------------------
# type — r01's shared single-stroke font, weight passes FUSED into one pen-down
# ---------------------------------------------------------------------------

PARTIAL = "∂"


def _units(ch: str) -> float:
    return _glyph_advance(ch)


def _strokes(ch: str):
    st = _GLYPHS.get(ch)
    if st is None:
        st = _GLYPHS.get(ch.upper(), [])
    return st


def _tw(text: str, h_mm: float, tracking: float = 1.0) -> float:
    return sum(_units(c) for c in text) * (h_mm / 6.0) * tracking


def _fused(base: List[Pt], weight: float) -> List[Pt]:
    """r01's weight passes (0,0), (w,0), (w/2, 0.9w) chained serpentine."""
    if weight <= 0:
        return base
    path: List[Pt] = []
    for i, (ox, oy) in enumerate(((0.0, 0.0), (weight, 0.0), (weight * 0.5, weight * 0.9))):
        seq = [(x + ox, y + oy) for x, y in base]
        path += seq if i % 2 == 0 else seq[::-1]
    return path


def _type(SH: Sheet, text: str, px: float, py: float, h_px: float, pen=None,
          tracking: float = 1.0, center: bool = False, weight: float = 0.0, f: int = 2200,
          halo: Optional[float] = HALO_PAD) -> List[Pt]:
    """(px, py) = LEFT BASELINE in reference pixels; glyphs built in mm."""
    M = SH.M
    ax, ay = M.p(px, py)
    h = M.s(h_px)
    sc = h / 6.0
    if center:
        ax -= _tw(text, h, tracking) / 2.0
    allp: List[Pt] = []
    cx = ax
    for ch in text:
        if ch == "~":  # the centred multiplication dot
            ccx, ccy, rr = cx + 1.8 * sc, ay + 2.6 * sc, max(0.55 * sc, 0.32)
            _round(SH, ccx, ccy, rr, pen, "type")
            allp += [(ccx - rr, ccy - rr), (ccx + rr, ccy + rr)]
        else:
            for st in _strokes(ch):
                base = [(cx + gx * sc, ay + gy * sc) for gx, gy in st]
                path = _fused(base, weight)
                _S(SH, path, pen, "type", f)
                allp += path
        cx += _units(ch) * sc * tracking
    if halo is not None:
        SH.box(allp, halo)
    return allp


def _type_sup(SH: Sheet, word: str, sup: str, cx_px: float, py: float, h_px: float, pen=None,
              tracking: float = 1.0, sup_scale: float = 0.62, sup_rise: float = 0.52):
    """word + a raised, smaller mark (the transpose T) — r01 layout."""
    M = SH.M
    h = M.s(h_px)
    w_word = _tw(word, h, tracking)
    w_sup = _tw(sup, h * sup_scale, tracking)
    total_px = (w_word + w_sup + M.s(1.2)) / M.sx
    left = cx_px - total_px / 2.0
    allp = _type(SH, word, left, py, h_px, pen=pen, tracking=tracking, halo=None)
    sx = left + (w_word + M.s(1.2)) / M.sx
    allp += _type(SH, sup, sx, py - h_px * sup_rise, h_px * sup_scale, pen=pen,
                  tracking=tracking, halo=None)
    SH.box(allp)


def _type_prime(SH: Sheet, word: str, cx_px: float, py: float, h_px: float, pen=None,
                tracking: float = 1.0):
    """word + the derivative PRIME, attached (A5): a short raised stroke set
    0.35 mm after the last glyph's ink, from cap height down 0.6 x-height —
    r01 set a ' glyph at 0.72 scale 0.95 mm off the word, where it floated."""
    M = SH.M
    h = M.s(h_px)
    sc = h / 6.0
    last = word[-1]
    ink_r = max(gx for st in _strokes(last) for gx, _ in st)
    w_word = _tw(word, h, tracking) - (_units(last) - ink_r) * sc * tracking
    gap, pw = 0.50, 0.22
    total = w_word + gap + pw
    left_mm = M.p(cx_px, py)[0] - total / 2.0
    left_px = (left_mm - M.x0) / M.sx
    allp = _type(SH, word, left_px, py, h_px, pen=pen, tracking=tracking, halo=None)
    _, by = M.p(0.0, py)
    x0 = left_mm + w_word + gap
    prime = [(x0 + pw, by + 6.0 * sc), (x0, by + 4.1 * sc)]
    _S(SH, prime, pen, "type", 2200)
    allp += prime
    SH.box(allp)


def _frac(SH: Sheet, num: str, den: str, px: float, py: float, h_px: float, pen=None,
          tracking: float = 1.0, gap_px: float = 4.2, halo: float = HALO_PAD):
    """numerator, rule, denominator — centred on ``px``, rule at ``py`` (r01)."""
    M = SH.M
    h = M.s(h_px)
    wn = _tw(num, h, tracking)
    wd = _tw(den, h, tracking)
    half = max(wn, wd) / 2.0 + M.s(2.0)
    rx, ry = M.p(px, py)
    rule = [(rx - half, ry), (rx + half, ry)]
    _S(SH, rule, pen, "type", 2000)
    allp = list(rule)
    allp += _type(SH, num, px, py - h_px * 0.42 - gap_px, h_px, pen=pen, tracking=tracking,
                  center=True, halo=None)
    allp += _type(SH, den, px, py + h_px * 1.02 + gap_px, h_px, pen=pen, tracking=tracking,
                  center=True, halo=None)
    SH.box(allp, halo)


# ---------------------------------------------------------------------------
# the wave packet (APPROVED, from the sibling) — carrier + dotted envelope
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


def wave_packet(SH: Sheet, x0: float, x1: float, y: float, packets: Sequence[Packet],
                pen=None, envelope: bool = True, env_lift: float = 3.2,
                ext: Optional[Tuple[float, float]] = None):
    """Carrier x Gaussian envelope on an axis, the envelope outlined above and
    below (r01).  ``ext`` = the axis span the carrier is extended to: the axis
    ends are drawn BY the carrier, so the straight axis is only redrawn where
    the packet actually leaves it (see ``_dedupe_axes``)."""
    M = SH.M
    lam_min = min(p[2] for p in packets)
    step = max(lam_min / 11.0, 0.22)
    n = int((x1 - x0) / step) + 1
    xs = [x0 + k * step for k in range(n + 1)]

    curve = [(x, y - _pk_value(x, packets)) for x in xs]
    if ext is not None:
        curve = [(ext[0], y)] + curve + [(ext[1], y)]
    _line(SH, curve, pen=pen, f=2400)
    lo, hi = (ext if ext is not None else (x0, xs[-1]))
    ymm = M.p(0.0, y)[1]
    SH.carriers.append((pen, ymm, M.p(lo, y)[0], M.p(hi, y)[0], list(packets)))

    if envelope:
        for sgn in (-1.0, 1.0):
            env = [(x, y + sgn * _pk_env(x, packets)) for x in xs]
            # r01 filtered the list and joined the survivors, which drew a chord
            # across every quiet stretch; the envelope is now cut into its runs.
            run: List[Pt] = []
            for x, yy in env + [(None, None)]:
                if x is not None and abs(yy - y) > env_lift:
                    run.append((x, yy))
                    continue
                if len(run) > 3:
                    _dash(SH, run, 0.85, 1.55, pen=pen, tag="env")
                run = []


def _axis(SH: Sheet, xa: float, xb: float, y: float, pen) -> None:
    a, b = SH.M.p(xa, y), SH.M.p(xb, y)
    SH.add(Mark([a, b], pen, "axis", 2000, y=a[1]))


# ---------------------------------------------------------------------------
# layout constants, traced off the reference (reference pixels) — r01
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

IF_CX, IF_CY = 561.0, 611.0
IF_D = 250.0
SRC_L, SRC_R = IF_CX - IF_D / 2, IF_CX + IF_D / 2

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

V_ROWS = [919.0, 944.0, 971.0, 999.0, 1027.0]
V_L = 725.0
V_R = [976.0, 991.0, 991.0, 991.0, 991.0]

FWD_Y = 1129.0
Z_START = 245.0
FFN_N0 = 722.0
FFN_N1 = 825.0
FFN_N2 = 900.0
FFN_N3 = 1000.0
Y_END = 1032.0

BACK_Y = 1272.0
BACK_ROWS = [
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

IF2_CX, IF2_CY = 465.5, BACK_Y
IF2_D = 97.0
SRC2_L, SRC2_R = IF2_CX - IF2_D / 2, IF2_CX + IF2_D / 2


# ---------------------------------------------------------------------------
# sections — upper half (r01)
# ---------------------------------------------------------------------------


def _title(SH: Sheet):
    bk = _pen(BLACK, SH.colors)
    M = SH.M
    _type(SH, "ATTENTION AS RESONANCE", 545.0, TITLE_Y, 16.0, pen=bk,
          tracking=1.645, center=True, weight=0.22)
    ax, ay = M.p(490.0, RULE_Y)
    bx, _ = M.p(615.0, RULE_Y)
    _S(SH, [(ax, ay), (bx, ay)], bk)
    _fdot(SH, 552.0, RULE_Y, 2.4, pen=bk)


def _qk_block(SH: Sheet, side: int, pen):
    """side = +1 Q (left block), -1 K (right, mirrored) — r01."""

    def mx(x: float) -> float:
        return x if side > 0 else REF_W - x

    home = Q_HOME if side > 0 else K_HOME
    filled = Q_HOME_FILLED if side > 0 else K_HOME_FILLED

    for i, y in enumerate(QK_ROWS):
        if side > 0:
            far, circ, tail = Q_ROWS[i][0], Q_ROWS[i][1], Q_ROWS[i][3]
            pk = Q_PACKETS[i]
        else:
            far, circ, tail = K_ROWS[i]
            pk = K_PACKETS[i]
        lo, hi = (home, far) if side > 0 else (far, home)

        _axis(SH, lo, hi, y, pen)
        wave_packet(SH, lo + 2.0, hi - 2.0, y, pk, pen=pen, ext=(lo, hi))
        if filled[i]:
            _fdot(SH, home, y, 4.6, pen=pen)
        else:
            _ocirc(SH, home, y, 4.8, pen=pen)
        if circ is not None:
            _ocirc(SH, circ, y, 5.4, pen=pen)
        if tail is not None:
            _fdot(SH, tail, y, 3.4, pen=pen)
        _lead_dots(SH, home - side * 21.0, -side * 12.0, 4, y, 2.4, pen=pen)

    for x, yt, yb in Q_VERTS:
        _dash(SH, [(mx(x), yt), (mx(x), yb)], dash=0.5, gap=1.7, pen=pen, tag="vert")
        _fdot(SH, mx(x), yt - 6.0, 2.2, pen=pen)

    if side > 0:
        _type(SH, "Q", 97.0, 126.0, 30.0, pen=pen, tracking=0.90, weight=0.44)
    else:
        _type(SH, "K", 1002.0, 124.0, 28.0, pen=pen, tracking=0.92, weight=0.44)

    for i, y in enumerate(QK_ROWS):
        end_x = Q_ROWS[i][0] if side > 0 else REF_W - K_ROWS[i][0]
        x_start = mx(end_x + 12.0)
        tx = mx(408.0 + 15.0 * i)
        ty = 446.0 + 26.0 * i
        c1 = (mx(end_x + 86.0 + 16.0 * i), y + 10.0)
        c2 = (mx(492.0 + 6.0 * i), 352.0 + 20.0 * i)
        _dash(SH, _bez((x_start, y), c1, c2, (tx, ty)), dash=0.5, gap=1.85, pen=pen,
              tag=f"fanA{i}")
        _fdot(SH, tx, ty, 3.0, pen=pen)
        c1b = (mx(end_x + 128.0 + 20.0 * i), y + 18.0)
        c2b = (mx(524.0 + 8.0 * i), 366.0 + 20.0 * i)
        tx2, ty2 = mx(386.0 + 13.0 * i), 470.0 + 24.0 * i
        _dash(SH, _bez((x_start, y + 6.0), c1b, c2b, (tx2, ty2)), dash=0.45, gap=2.1, pen=pen,
              tag=f"fanB{i}")
        _fdot(SH, tx2, ty2, 2.2, pen=pen)


def _centre_fraction(SH: Sheet):
    """Q . K^T over a rule over sqrt(d_k) — r01."""
    bk = _pen(BLACK, SH.colors)
    M = SH.M
    for j in range(3):
        _fdot(SH, 561.0, 332.0 + 11.0 * j, 1.7, pen=bk)

    h = 23.0
    hm = M.s(h)
    num = "Q~K"
    tr = 1.16
    wn_px = _tw(num, hm, tr) / M.sx
    nx = 561.0 - 4.0
    allp = _type(SH, num, nx, 392.0, h, pen=bk, tracking=tr, center=True, weight=0.2, halo=None)
    allp += _type(SH, "T", nx + wn_px / 2.0 + 1.5, 381.0, 12.5, pen=bk, weight=0.16, halo=None)

    ax, ay = M.p(507.0, 404.0)
    bx, _ = M.p(616.0, 404.0)
    _S(SH, [(ax, ay), (bx, ay)], bk, "type")
    allp += [(ax, ay), (bx, ay)]
    allp += _radical(SH, "d", 528.0, 434.0, 21.0, pen=bk, weight=0.16, tail_px=11.0)
    allp += _type(SH, "k", 564.0, 437.0, 12.0, pen=bk, weight=0.14, halo=None)
    SH.box(allp)


def _radical(SH: Sheet, radicand: str, px: float, py: float, h_px: float, pen=None,
             weight: float = 0.0, tail_px: float = 0.0) -> List[Pt]:
    """The radical sign, COMPOSED (r01), weight passes fused."""
    M = SH.M
    ax, ay = M.p(px, py)
    sc = M.s(h_px) / 6.0
    w = _tw(radicand, M.s(h_px), 1.0) + M.s(tail_px)
    tick = [(ax + gx * sc, ay + gy * sc) for gx, gy in
            [(0.0, 3.2), (0.7, 2.7), (1.6, 0.0), (2.8, 6.0)]]
    tick.append((ax + 3.4 * sc + w, ay + 6.0 * sc))     # the overbar continues the tick
    path = _fused(tick, weight)
    _S(SH, path, pen, "type", 2200)
    return path + _type(SH, radicand, px + 3.9 * sc / M.sx, py, h_px, pen=pen, weight=weight,
                        halo=None)


class _Guard:
    """Parallel-crowding guard, in MILLIMETRES (r01, unchanged)."""

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


def _crest_field(SH: Sheet, cx: float, cy: float, d: float, n_lam: int, m_solid: int,
                 m_max: int, a_out: float, b_out: float, b_solid: float, pen):
    """The APPROVED Huygens crest construction (r01, byte-identical maths).  The
    dotted crest fade (m > m_solid) is the TEXTURE: one round dot per r01 dash."""
    M = SH.M
    lam = d / n_lam
    sl, sr = cx - d / 2, cx + d / 2
    guard = _Guard(0.82)
    sid = 0

    def ring(sx: float, r: float):
        n = max(60, int(r * 2.1))
        return [
            (sx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n))
            for t in range(n + 1)
        ]

    def emit(run, dotted):
        if dotted:
            _dash(SH, run, dash=0.42, gap=1.8, pen=pen, cls="tex")
        else:
            _line(SH, run, pen=pen, f=2600)

    def emit_clipped(pts, dotted: bool = False, keep_out=None):
        nonlocal sid
        sid += 1
        aa, bb = (a_out, b_out) if dotted else (a_out * 0.80, b_solid)
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
                    emit(run, dotted)
                run = []
        if len(run) >= 4:
            emit(run, dotted)

    for sx in (sl, sr):
        other = sr if sx == sl else sl
        for m in range(1, m_solid + 1):
            emit_clipped(ring(sx, m * lam))
        for m in range(m_solid + 1, m_max):
            emit_clipped(ring(sx, m * lam), dotted=True,
                         keep_out=(other, cy, m_solid * lam + d * 0.024))


def _halo_ellipse(SH: Sheet, sx: float, cy: float, a: float, b: float, N: int, keep, pen):
    """One dotted halo ellipse (reference px), cut into its REAL arcs.

    r01 filtered the sample list and joined the survivors, so every removed
    stretch became a straight dotted chord (y ≈ 191 / 140 mm) and the parameter
    seam at the right-hand vertex became a vertical stub.  Here every arc stops
    ON the curve at the keep-out (bisection on the parameter), and the arc that
    crosses the seam is joined through it."""

    def P(t):
        return (sx + a * math.cos(t), cy + b * math.sin(t))

    ts = [2 * math.pi * k / N for k in range(N)]
    ok = [keep(P(t)) for t in ts]
    if all(ok):
        _dotline(SH, [SH.M.p(*P(2 * math.pi * k / N)) for k in range(N + 1)], pen, "halo")
        return
    if not any(ok):
        return

    def edge(t_in, t_out):
        for _ in range(30):
            tm = 0.5 * (t_in + t_out)
            if keep(P(tm)):
                t_in = tm
            else:
                t_out = tm
        return t_in

    # start the walk at a dropped sample so no arc is split by the seam
    k0 = ok.index(False)
    runs: List[List[float]] = []
    cur: Optional[List[float]] = None
    for j in range(1, N + 1):
        k = (k0 + j) % N
        t = ts[k] + (2 * math.pi if k0 + j >= N else 0.0)
        if ok[k]:
            if cur is None:
                cur = [edge(t, t - 2 * math.pi / N)]
            cur.append(t)
        elif cur is not None:
            cur.append(edge(cur[-1], t))
            runs.append(cur)
            cur = None
    for run in runs:
        dense = []
        for a_, b_ in zip(run[:-1], run[1:]):
            m = max(1, int(abs(b_ - a_) / (2 * math.pi / 720)))
            dense += [a_ + (b_ - a_) * i / m for i in range(m)]
        dense.append(run[-1])
        _dotline(SH, [SH.M.p(*P(t)) for t in dense], pen, "halo")


def _interference(SH: Sheet, rng: SeededRNG):
    """The hero, computed as a real two-source field (r01)."""
    M = SH.M
    bk = _pen(BLACK, SH.colors)

    n_lam = 35
    lam = IF_D / n_lam
    _crest_field(SH, IF_CX, IF_CY, IF_D, n_lam, 21, 52, 272.0, 158.0, 126.0, bk)

    # --- outer dotted halo ellipses around each source (arcs, not chords) ---
    def keep(q):
        return (M.x0 + 2 < M.p(*q)[0] < M.x1 - 2
                and min(math.hypot(q[0] - SRC_L, q[1] - IF_CY),
                        math.hypot(q[0] - SRC_R, q[1] - IF_CY)) > 21 * lam + 8.0)

    for sx in (SRC_L, SRC_R):
        for a in (152.0, 190.0, 232.0):
            _halo_ellipse(SH, sx, IF_CY, a, a * 0.60, 240, keep, bk)

    # --- the horizontal axis through the figure ---------------------------
    ax, ay = M.p(300.0, IF_CY)
    bx, _ = M.p(822.0, IF_CY)
    _S(SH, [(ax, ay), (bx, ay)], bk)
    for sgn in (1, -1):
        base = IF_CX - sgn * 334.0
        _ocirc(SH, base, IF_CY, 5.0, pen=bk)
        for j in range(4):
            _fdot(SH, base - sgn * (17.0 + 17.0 * j), IF_CY, 2.3, pen=bk)
        _fdot(SH, IF_CX - sgn * 305.0, IF_CY, 3.2, pen=bk)
        _fdot(SH, IF_CX - sgn * 266.0, IF_CY, 3.4, pen=bk)
        cxx = IF_CX - sgn * 203.0
        _ocirc(SH, cxx, IF_CY, 6.2, pen=bk)
        _fdot(SH, cxx, IF_CY, 2.2, pen=bk)
    _fdot(SH, IF_CX, IF_CY, 5.0, pen=bk)
    _fdot(SH, SRC_L, IF_CY, 4.8, pen=bk)
    _fdot(SH, SRC_R, IF_CY, 4.8, pen=bk)

    # --- the dot field (TEXTURE: r01's positions and radii) ----------------
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
        _fdot(SH, px, py, r, pen=bk, kind="tex")

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

    # --- vertical dotted droplines, up and down ---------------------------
    drops = [434.0, 477.0, 516.0, 561.0, 613.0, 652.0, 691.0]
    for j, x in enumerate(drops):
        top = 462.0 if x in (434.0, 561.0, 691.0) else 496.0
        _dash(SH, [(x, top), (x, IF_CY - 6.0)], dash=0.5, gap=1.7, pen=bk, tag="drop")
        _fdot(SH, x, top - 8.0, 2.0, pen=bk)
        bot = 812.0 if j % 2 == 0 else 788.0
        _dash(SH, [(x, IF_CY + 6.0), (x, bot)], dash=0.5, gap=1.7, pen=bk, tag="drop")
    _ocirc(SH, IF_CX, 486.0, 4.8, pen=bk)
    _ocirc(SH, IF_CX, 716.0, 4.8, pen=bk)


def _softmax(SH: Sheet):
    bk = _pen(BLACK, SH.colors)
    x0, x1 = 313.0, 806.0

    def curve_y(x: float) -> float:
        v = 0.0
        for cx, h, _m in SOFT_PEAKS:
            v += h / (1.0 + ((x - cx) / 9.5) ** 2) ** 1.6
        return SOFT_BASE - v

    n = int((x1 - x0) / 0.7)
    pts = [(x0 + k * (x1 - x0) / n, 0.0) for k in range(n + 1)]
    pts = [(x, curve_y(x)) for x, _ in pts]
    _line(SH, pts, pen=bk, f=2400)

    for cx, h in SOFT_GHOSTS:
        gp = [
            (cx - 26.0 + t * 0.9,
             SOFT_BASE - h / (1.0 + ((cx - 26.0 + t * 0.9 - cx) / 8.0) ** 2) ** 1.6)
            for t in range(59)
        ]
        _dash(SH, gp, dash=0.42, gap=1.5, pen=bk, tag="ghost")

    for cx, h, m in SOFT_PEAKS:
        _line(SH, [(cx, SOFT_BASE), (cx, SOFT_BASE - h + 2.0)], pen=bk)
        if m == "o":
            _ocirc(SH, cx, SOFT_BASE - h - 3.0, 5.0, pen=bk)
        elif m == "f":
            _fdot(SH, cx, SOFT_BASE - h - 3.0, 4.4, pen=bk)

    for x, kind in [
        (322.0, "f"), (391.0, "f"), (434.0, "o"), (475.0, "o"), (516.0, "f"),
        (559.0, "o"), (605.0, "o"), (645.0, "o"), (685.0, "o"), (726.0, "f"), (798.0, "f"),
    ]:
        if kind == "o":
            _ocirc(SH, x, SOFT_BASE, 4.4, pen=bk)
        else:
            _fdot(SH, x, SOFT_BASE, 3.2, pen=bk)

    _lead_dots(SH, 311.0, -11.0, 4, SOFT_BASE, 2.3, pen=bk)
    _lead_dots(SH, 813.0, 13.5, 4, SOFT_BASE, 2.3, pen=bk)

    _type(SH, "softmax", 562.0, 782.0, 16.0, pen=bk, tracking=1.173, center=True, weight=0.14)


def _v_block(SH: Sheet):
    """V — FIVE ochre rows at mid-right (r01)."""
    oc = _pen(OCHRE, SH.colors)
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
        _axis(SH, V_L, xr, y, oc)
        wave_packet(SH, V_L + 2.0, xr - 2.0, y, packs[i], pen=oc, ext=(V_L, xr))
        _ocirc(SH, V_L, y, 4.8, pen=oc)
        if i == 2:
            _fdot(SH, V_L, y, 2.2, pen=oc)
        if i == 3:
            _fdot(SH, xr, y, 4.4, pen=oc)
        else:
            _ocirc(SH, xr, y, 4.8, pen=oc)
        _lead_dots(SH, 1036.0, 10.5, 4, y, 2.2, pen=oc)
        if i in (0, 2):
            _fdot(SH, 703.0, y, 2.4, pen=oc)
        if i == 1:
            _fdot(SH, 691.0, y, 3.4, pen=oc)

    _dash(SH, [(V_L, V_ROWS[0] - 20.0), (V_L, V_ROWS[-1] + 26.0)],
          dash=0.5, gap=1.7, pen=oc, tag="vcol")
    _dash(SH, [(991.0, V_ROWS[0] + 6.0), (991.0, V_ROWS[-1] + 30.0)],
          dash=0.5, gap=1.7, pen=oc, tag="vcol")

    _type(SH, "V", 1021.0, 897.0, 24.0, pen=oc, tracking=0.99, weight=0.38)

    # --- softmax -> V : long ochre feeds swinging in from the left ---------
    for i, sx in enumerate([391.0, 434.0, 475.0, 516.0, 559.0, 601.0]):
        ty = V_ROWS[min(i, 4)]
        pts = _bez((sx, SOFT_BASE + 8.0), (sx + 10.0, SOFT_BASE + 60.0),
                   (V_L - 150.0 + 6.0 * i, ty), (V_L - 22.0, ty))
        _dash(SH, pts, dash=0.45, gap=1.9, pen=oc, tag=f"feed{i}")

    # --- V -> Z : the ochre bundle sweeping down-left under the V block ----
    for i, y in enumerate(V_ROWS):
        pts = _bez((V_L - 4.0, y + 6.0), (V_L - 96.0, y + 34.0),
                   (700.0 - 10.0 * i, 1036.0 + 8.0 * i), (652.0 - 18.0 * i, 1100.0 + 5.0 * i))
        _dash(SH, pts, dash=0.45, gap=2.0, pen=oc, tag=f"vz{i}")


# ---------------------------------------------------------------------------
# the FFN fan (r01)
# ---------------------------------------------------------------------------


FAN_STATS: Dict[str, int] = {}


def _ffn_fan(SH: Sheet, xa: float, xb: float, y: float, amp: float, pen,
             derivative: bool = False, n: int = 5):
    """A bundle of streamlines pinched to a point at both nodes (r01, unchanged):
    forward tanh-saturated dome, backward the same family with an ABSOLUTE notch."""
    M = SH.M
    span = xb - xa
    steps = 170
    LIFT = 0.44 / M.sx
    dip = 0.26 * amp if derivative else 0.0
    lines = 0

    def family(u: float, p: float) -> float:
        s = math.sin(math.pi * min(max(u, 0.0), 1.0))
        if s <= 0.0:
            return 0.0
        v = s ** p
        if derivative:
            return v
        c = 1.75
        return math.tanh(c * v) / math.tanh(c)

    def notch(u: float) -> float:
        return dip * math.exp(-((u - 0.5) / 0.078) ** 2)

    for k in range(1, n + 1):
        frac = k / n
        a = amp * frac ** 0.72
        p = 2.55 - 0.16 * k + (0.85 if derivative else 0.0)
        skew = 0.035 * (1.0 - frac)
        for sgn in (1.0, -1.0):
            run: List[Pt] = []
            drew = False
            for t in range(steps + 1):
                u = t / steps
                uu = min(max(u + skew * math.sin(2 * math.pi * u), 0.0), 1.0)
                off = a * family(uu, p) - notch(u)
                if off < LIFT:
                    if len(run) > 3:
                        _line(SH, run, pen=pen, f=2500)
                        drew = True
                    run = []
                    continue
                run.append((xa + u * span, y + sgn * off))
            if len(run) > 3:
                _line(SH, run, pen=pen, f=2500)
                drew = True
            lines += int(drew)
    FAN_STATS["backward" if derivative else "forward"] = lines

    for sgn in (1.0, -1.0):
        pts = [
            (xa + (t / 120) * span,
             y + sgn * (amp * 1.28 * family(t / 120, 2.15) - notch(t / 120) * 0.6))
            for t in range(121)
        ]
        _dash(SH, pts, dash=0.45, gap=1.9, pen=pen, tag="fanarc")


# ---------------------------------------------------------------------------
# the forward row: Z = AV | FFN | Y
# ---------------------------------------------------------------------------


def _forward_row(SH: Sheet):
    c = SH.colors
    gr, pu, bk, oc = _pen(GREEN, c), _pen(PURPLE, c), _pen(BLACK, c), _pen(OCHRE, c)
    M = SH.M
    y = FWD_Y

    zp: List[Packet] = [
        (508.0, 46.0, 13.5, 72.0, 0.0),
        (400.0, 13.0, 8.5, 15.0, 0.4),
        (612.0, 13.0, 8.5, 14.0, 0.9),
        (455.0, 9.0, 7.5, 8.0, 0.2),
        (352.0, 11.0, 8.0, 6.0, 0.1),
    ]
    _axis(SH, Z_START, FFN_N0, y, gr)
    wave_packet(SH, Z_START + 2.0, FFN_N0 - 4.0, y, zp, pen=gr, ext=(Z_START, FFN_N0))
    _fdot(SH, Z_START, y, 4.2, pen=gr)
    _lead_dots(SH, Z_START - 21.0, -10.5, 5, y, 2.3, pen=gr)
    for x in (322.0, 508.0, 686.0):
        _ocirc(SH, x, y, 4.6, pen=gr)
    for x in (387.0, 620.0):
        _ocirc(SH, x, y, 6.4, pen=gr)
        _ocirc(SH, x, y, 3.2, pen=gr, n=26)
    _ocirc(SH, 634.0, y, 3.0, pen=gr, n=24)
    _fdot(SH, 508.0, y - 76.0, 4.4, pen=gr)
    _fdot(SH, 508.0, y + 76.0, 4.4, pen=gr)
    _dash(SH, [(508.0, y - 70.0), (508.0, y + 70.0)], dash=0.5, gap=1.8, pen=gr, tag="zvert")
    _type(SH, "Z = AV", 362.0, 1068.0, 22.0, pen=gr, tracking=1.203, weight=0.38)

    # ---- the FFN bracket (A5: right leg re-aimed onto the project|Y node,
    #      `FFN` lifted 2 mm clear of the bar) -------------------------------
    lift_px = 2.0 / M.sy
    # legs AIMED at the pinch nodes N0 (722, 1129) and N3 (1000, 1129), stopping
    # 11 px (2.2 mm) below the bar — r01's right leg (972,1077)->(983,1098) ended
    # on project's crest.
    leg = 11.0 / 52.0
    _line(SH, [(733.0 - 11.0 * leg, 1088.0), (733.0, 1077.0), (846.0, 1077.0)], pen=bk)
    _fdot(SH, 850.0, 1077.0, 2.2, pen=bk)
    _type(SH, "FFN", 876.0, 1075.0 - lift_px, 14.0, pen=bk, tracking=0.85, center=True,
          weight=0.16)
    _fdot(SH, 899.0, 1077.0, 2.2, pen=bk)
    _line(SH, [(905.0, 1077.0), (989.0, 1077.0), (989.0 + 11.0 * leg, 1088.0)], pen=bk)

    # ---- the purple spine ------------------------------------------------
    _axis(SH, FFN_N0, Y_END, y, pu)
    _fdot(SH, FFN_N0, y, 4.6, pen=gr)
    for nx in (FFN_N1, FFN_N2, FFN_N3):
        _fdot(SH, nx, y, 4.4, pen=pu)
    _ocirc(SH, Y_END, y, 5.4, pen=pu)
    _lead_dots(SH, 1052.0, 15.0, 4, y, 2.4, pen=pu)

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
    wave_packet(SH, FFN_N0 + 5.0, FFN_N1 - 4.0, y, expand, pen=pu, ext=(FFN_N0, FFN_N1))
    _ffn_fan(SH, FFN_N1, FFN_N2, y, 44.0, pu, derivative=False)
    wave_packet(SH, FFN_N2 + 4.0, FFN_N3 - 3.0, y, project, pen=pu, ext=(FFN_N2, FFN_N3))

    for name, cx, tr in (("expand", 764.5, 0.89), ("nonlinearity", 873.0, 0.97),
                         ("project", 968.0, 0.85)):
        _type(SH, name, cx, 1187.0, 12.0, pen=bk, tracking=tr, center=True)

    for nx in (FFN_N1, FFN_N2):
        _dash(SH, [(nx, 1086.0), (nx, 1172.0)], dash=0.6, gap=2.2, pen=bk, tag="stage")
    _dash(SH, [(FFN_N3, 1092.0), (FFN_N3, 1162.0)], dash=0.55, gap=2.0, pen=pu, tag="stage")

    _type(SH, "Y", 1052.0, 1107.0, 23.0, pen=pu, tracking=0.86, weight=0.40)

    _dash(SH, _bez((996.0, V_ROWS[0]), (1075.0, 960.0), (1055.0, 1030.0), (1010.0, 1062.0)),
          dash=0.45, gap=1.9, pen=oc, tag="ventry")


# ---------------------------------------------------------------------------
# the backward row — ONE line along the bottom (r01)
# ---------------------------------------------------------------------------


def _small_interference(SH: Sheet, rng: SeededRNG):
    """∂L/∂A — the hero figure again, at 0.39 scale, same construction (r01)."""
    bk = _pen(BLACK, SH.colors)
    M = SH.M
    n_lam = 14
    lam = IF2_D / n_lam
    _crest_field(SH, IF2_CX, IF2_CY, IF2_D, n_lam, 8, 21, 105.5, 61.0, 48.5, bk)

    def keep(q):
        return min(math.hypot(q[0] - SRC2_L, q[1] - IF2_CY),
                   math.hypot(q[0] - SRC2_R, q[1] - IF2_CY)) > 8 * lam + 3.0

    for sx in (SRC2_L, SRC2_R):
        for a in (62.0, 78.0):
            _halo_ellipse(SH, sx, IF2_CY, a, a * 0.60, 200, keep, bk)

    k = 2 * math.pi / lam

    def field(px, py):
        d1 = math.hypot(px - SRC2_L, py - IF2_CY) + 3.0
        d2 = math.hypot(px - SRC2_R, py - IF2_CY) + 3.0
        return math.cos(k * d1) / math.sqrt(d1) + math.cos(k * d2) / math.sqrt(d2)

    placed: List[Tuple[float, float, float]] = []

    def place(px, py, r):
        if r < 0.7:
            return
        for qx, qy, qr in placed:
            if math.hypot(px - qx, py - qy) < (r + qr) * 1.3 + 2.5:
                return
        placed.append((px, py, r))
        _fdot(SH, px, py, r, pen=bk, kind="tex")

    for _ in range(46):
        px = IF2_CX + rng.uniform(-88.0, 88.0)
        py = IF2_CY + rng.uniform(-52.0, 52.0)
        if ((px - IF2_CX) / 92.0) ** 2 + ((py - IF2_CY) / 54.0) ** 2 > 1.0:
            continue
        place(px, py, 0.7 + 8.0 * abs(field(px, py)))

    for x, yt, yb in ((417.0, 1231.0, 1325.0), (458.0, 1218.0, 1305.0),
                      (514.0, 1207.0, 1338.0)):
        _dash(SH, [(x, yt), (x, yb)], dash=0.6, gap=2.1, pen=bk, tag="drop2")

    # A5: 1.5 mm of clear air under the twin — the label moves down 0.8 mm and
    # its halo is widened to 1.5 mm, so no crest-fade dot sits against it.
    _frac(SH, "∂L", "∂A", 462.0, 1352.0 + 0.8 / M.sy, 13.0, pen=bk, tracking=1.02,
          halo=1.5)


def _backward(SH: Sheet, rng: SeededRNG):
    c = SH.colors
    pens = {RED: _pen(RED, c), BLUE: _pen(BLUE, c), OCHRE: _pen(OCHRE, c)}
    bk, gr, pu = _pen(BLACK, c), _pen(GREEN, c), _pen(PURPLE, c)

    for i, (y, slot, xl, xr, label, _open) in enumerate(BACK_ROWS):
        pn = pens[slot]
        _axis(SH, xl, xr, y, pn)
        wave_packet(SH, xl + 3.0, xr - 3.0, y, BACK_PACKETS[i], pen=pn, env_lift=2.4,
                    ext=(xl, xr))
        _ocirc(SH, xl, y, 4.7, pen=pn)
        _ocirc(SH, xr, y, 4.7, pen=pn)
        if label is not None:
            _frac(SH, "∂L", PARTIAL + label, 47.0, y, 14.0, pen=pn, tracking=1.02)
            _arrow(SH, 75.0, y, -1, 9.0, pen=pn)
            _dash(SH, [(88.0, y), (xl - 7.0, y)], dash=0.5, gap=1.0, pen=pn, tag="shaft")
        else:
            _fdot(SH, 112.0, y, 2.2, pen=pn)
            _dash(SH, [(120.0, y), (xl - 7.0, y)], dash=0.5, gap=1.0, pen=pn, tag="shaft")

    for x, yt, yb, slot in ((112.0, 1206.0, 1240.0, RED), (112.0, 1272.0, 1303.0, BLUE),
                            (112.0, 1334.0, 1366.0, OCHRE),
                            (143.0, 1178.0, 1238.0, RED), (143.0, 1250.0, 1301.0, BLUE),
                            (232.0, 1178.0, 1206.0, RED), (232.0, 1206.0, 1248.0, RED),
                            (276.0, 1206.0, 1240.0, RED), (276.0, 1272.0, 1303.0, BLUE),
                            (276.0, 1334.0, 1368.0, OCHRE)):
        _dash(SH, [(x, yt), (x, yb)], dash=0.5, gap=1.8, pen=pens[slot], tag="bcol")

    fans = [
        (240.0, 1206.0, RED, 417.0, 1231.0),
        (284.0, 1238.0, RED, 417.0, 1233.0),
        (284.0, 1272.0, BLUE, 419.0, 1236.0),
        (284.0, 1301.0, BLUE, 421.0, 1240.0),
        (284.0, 1334.0, OCHRE, 424.0, 1248.0),
    ]
    for j, (sx, sy, slot, ex, ey) in enumerate(fans):
        pts = _bez((sx, sy), (sx + 105.0, sy + 4.0), (ex - 95.0, ey + 58.0), (ex, ey))
        _dash(SH, pts, dash=0.45, gap=1.9, pen=pens[slot], tag=f"ret{j}")
    _fdot(SH, 417.0, 1231.0, 3.2, pen=pens[RED])

    _small_interference(SH, rng)

    _dash(SH, [(286.0, BACK_Y), (330.0, BACK_Y)], dash=0.5, gap=1.9, pen=_pen(BLUE, c),
          tag="axisin")
    _dash(SH, [(330.0, BACK_Y), (585.0, BACK_Y)], dash=2.6, gap=2.0, pen=bk)
    for x, r in ((363.0, 3.6), (377.0, 2.2), (389.0, 2.2), (554.0, 2.6),
                 (566.0, 2.0), (578.0, 3.4)):
        _fdot(SH, x, BACK_Y, r, pen=bk)
    _fdot(SH, SRC2_L, BACK_Y, 4.6, pen=bk)
    _fdot(SH, IF2_CX - 7.5, BACK_Y, 3.4, pen=bk)
    _fdot(SH, SRC2_R, BACK_Y, 4.6, pen=bk)
    _ocirc(SH, SRC2_R, BACK_Y, 6.2, pen=bk)

    zp: List[Packet] = [
        (662.0, 22.0, 11.0, 34.0, 0.0),
        (630.0, 10.0, 7.5, 9.0, 0.4),
        (692.0, 10.0, 7.5, 8.0, 0.8),
    ]
    _arrow(SH, 590.0, BACK_Y, -1, 9.5, pen=gr)
    _dash(SH, [(601.0, BACK_Y), (618.0, BACK_Y)], dash=0.5, gap=1.1, pen=gr, tag="shaft")
    _axis(SH, 618.0, 706.0, BACK_Y, gr)
    wave_packet(SH, 620.0, 704.0, BACK_Y, zp, pen=gr, env_lift=2.4, ext=(618.0, 706.0))
    _arrow(SH, 706.0, BACK_Y, -1, 9.5, pen=gr)
    _dash(SH, [(717.0, BACK_Y), (733.0, BACK_Y)], dash=0.5, gap=1.1, pen=gr, tag="shaft")
    _frac(SH, "∂L", "∂Z", 665.0, 1342.0, 13.0, pen=gr, tracking=1.02)

    _axis(SH, 737.0, 1016.0, BACK_Y, pu)
    for nx in (737.0, 828.0, 930.0, 1016.0):
        _fdot(SH, nx, BACK_Y, 4.4, pen=pu)
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
    wave_packet(SH, 740.0, 824.0, BACK_Y, proj_t, pen=pu, env_lift=2.4, ext=(737.0, 828.0))
    _ffn_fan(SH, 828.0, 930.0, BACK_Y, 42.0, pu, derivative=True)
    wave_packet(SH, 934.0, 1013.0, BACK_Y, exp_t, pen=pu, env_lift=2.4, ext=(930.0, 1016.0))
    for nx in (828.0, 930.0):
        _dash(SH, [(nx, 1238.0), (nx, 1308.0)], dash=0.6, gap=2.2, pen=bk, tag="stage")

    _type_sup(SH, "project", "T", 782.0, 1334.0, 12.0, pen=bk, tracking=0.85)
    _type_prime(SH, "nonlinearity", 880.0, 1334.0, 12.0, pen=bk, tracking=0.95)
    _type_sup(SH, "expand", "T", 973.0, 1334.0, 12.0, pen=bk, tracking=0.85)

    _arrow(SH, 1029.0, BACK_Y, -1, 9.5, pen=pu)
    _dash(SH, [(1040.0, BACK_Y), (1060.0, BACK_Y)], dash=0.5, gap=1.1, pen=pu, tag="shaft")
    _frac(SH, "∂L", "∂Y", 1086.0, 1270.0, 14.0, pen=pu, tracking=1.02)

    _dash(SH, _bez((FFN_N0, FWD_Y + 6.0), (712.0, 1180.0), (676.0, 1200.0), (655.0, 1233.0)),
          dash=0.5, gap=1.9, pen=gr, tag="dropZ")
    _dash(SH, _bez((Y_END, FWD_Y + 8.0), (1040.0, 1170.0), (1024.0, 1196.0), (1011.0, 1232.0)),
          dash=0.5, gap=1.9, pen=pu, tag="dropY")
    _fdot(SH, 1011.0, 1233.0, 2.6, pen=pu)


# ---------------------------------------------------------------------------
# the non-destructive passes
# ---------------------------------------------------------------------------


def _dedupe_axes(SH: Sheet) -> None:
    """The carrier IS the axis: drop the straight axis only where a same-pen
    carrier on the same line already lies on it (envelope < AXIS_TOL)."""
    M = SH.M
    out: List[Mark] = []
    for m in SH.marks:
        if m.kind != "axis":
            out.append(m)
            continue
        (xa, y), (xb, _) = m.pts
        if xa > xb:
            xa, xb = xb, xa
        cs = [c for c in SH.carriers if c[0] == m.pen and abs(c[1] - y) < 1e-6]
        step = 0.05
        n = max(1, int((xb - xa) / step))
        keep_run: List[float] = []
        pieces: List[Tuple[float, float]] = []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            px = (x - M.x0) / M.sx
            covered = any(c[2] - 1e-6 <= x <= c[3] + 1e-6 and _pk_env(px, c[4]) * M.sy < AXIS_TOL
                          for c in cs)
            if not covered:
                keep_run.append(x)
            elif keep_run:
                pieces.append((keep_run[0], keep_run[-1]))
                keep_run = []
        if keep_run:
            pieces.append((keep_run[0], keep_run[-1]))
        for a, b in pieces:
            if b - a >= 0.2:
                out.append(Mark([(a, y), (b, y)], m.pen, "line", m.f))
    SH.marks = out


class _SegGrid:
    def __init__(self, cell: float = 1.0) -> None:
        self.cell = cell
        self.g: Dict[Tuple[int, int], List[tuple]] = {}

    def add_poly(self, pts: Sequence[Pt], key) -> None:
        c = self.cell
        for a, b in zip(pts[:-1], pts[1:]):
            x0, x1 = sorted((a[0], b[0]))
            y0, y1 = sorted((a[1], b[1]))
            for i in range(int(x0 // c), int(x1 // c) + 1):
                for j in range(int(y0 // c), int(y1 // c) + 1):
                    self.g.setdefault((i, j), []).append((a, b, key))

    def near(self, x: float, y: float, r: float, key) -> bool:
        c = self.cell
        r2 = r * r
        for i in range(int((x - r) // c), int((x + r) // c) + 1):
            for j in range(int((y - r) // c), int((y + r) // c) + 1):
                for a, b, k in self.g.get((i, j), ()):
                    if k != key:
                        continue
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    L2 = dx * dx + dy * dy
                    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((x - a[0]) * dx + (y - a[1]) * dy) / L2))
                    qx, qy = a[0] + t * dx - x, a[1] + t * dy - y
                    if qx * qx + qy * qy < r2:
                        return True
        return False


def _clean_dots(SH: Sheet) -> None:
    """No invisible dots.  A dot (family or texture stipple) is dropped only when
    it could not be seen as its own mark anyway: inside a label halo, on a node,
    within INK_KEEP of same-pen ink, or co-incident with a same-pen dot."""
    ink = _SegGrid(1.0)
    nodes: List[Tuple[float, float, float]] = []
    for m in SH.marks:
        if m.kind in ("line", "type", "dash", "node"):
            ink.add_poly(m.pts, m.pen)
        if m.kind == "node" and m.c is not None:
            nodes.append((m.c[0], m.c[1], m.r))
        if m.kind == "tex" and m.r > 0.3:          # scatter discs are obstacles too
            nodes.append((m.c[0], m.c[1], m.r))
    ncell = 3.0
    ngrid: Dict[Tuple[int, int], List[tuple]] = {}
    for n in nodes:
        ngrid.setdefault((int(n[0] // ncell), int(n[1] // ncell)), []).append(n)

    def on_node(x, y):
        gi, gj = int(x // ncell), int(y // ncell)
        for i in (gi - 1, gi, gi + 1):
            for j in (gj - 1, gj, gj + 1):
                for nx, ny, nr in ngrid.get((i, j), ()):
                    if math.hypot(x - nx, y - ny) < nr + NODE_KEEP + DOT_R:
                        return True
        return False

    def in_box(x, y):
        for b in SH.boxes:
            if b[0] - DOT_R <= x <= b[2] + DOT_R and b[1] - DOT_R <= y <= b[3] + DOT_R:
                return True
        return False

    placed: Dict[Tuple[int, int, object], List[Pt]] = {}

    def coincident(x, y, pen, lim=COINCIDENT):
        gi, gj = int(x // 1.0), int(y // 1.0)
        for i in (gi - 1, gi, gi + 1):
            for j in (gj - 1, gj, gj + 1):
                for qx, qy in placed.get((i, j, pen), ()):
                    if (qx - x) ** 2 + (qy - y) ** 2 < lim ** 2:
                        return True
        return False

    log = {"halo": 0, "node": 0, "ink": 0, "coincident": 0,
           "tex_halo": 0, "tex_coincident": 0}
    out: List[Mark] = [m for m in SH.marks if m.kind not in ("dot", "tex")]
    # TEXTURES first: they keep r01's count and positions.  A texture mark is
    # dropped only under a label (the halo pass) or when it lands on another
    # texture mark (< 0.35 mm: one dot).  A stipple or scatter dot on a crest
    # line is NOT invisible — a 0.65 mm dot on a 0.35 mm line reads as a bead,
    # which is how the reference sets its field dots on the rings.
    for m in (m for m in SH.marks if m.kind == "tex"):
        x, y = m.c
        if in_box(x, y):
            log["tex_halo"] += 1
            continue
        if m.r <= 0.3 and coincident(x, y, m.pen, 0.35):
            log["tex_coincident"] += 1
            continue
        placed.setdefault((int(x // 1.0), int(y // 1.0), m.pen), []).append((x, y))
        out.append(m)
    # then the family dots of the dotted LINES
    for m in (m for m in SH.marks if m.kind == "dot"):
        x, y = m.c
        if in_box(x, y):
            log["halo"] += 1
            continue
        if on_node(x, y):
            log["node"] += 1
            continue
        if ink.near(x, y, INK_KEEP, m.pen):
            log["ink"] += 1
            continue
        if coincident(x, y, m.pen):
            log["coincident"] += 1
            continue
        placed.setdefault((int(x // 1.0), int(y // 1.0), m.pen), []).append((x, y))
        out.append(m)
    SH.log.update(log)
    SH.marks = out


# ---------------------------------------------------------------------------
# ordering and emission
# ---------------------------------------------------------------------------


def _order(marks: List[Mark]) -> List[Mark]:
    """Per pen, one clean layer: greedy nearest-END from the machine origin
    (0, 0), a stroke may be drawn in either direction.  The post-processor's
    per-colour nearest-START pass then reproduces this order exactly (each
    chosen start is the nearest endpoint of all that remain, hence the nearest
    start), so the file streams in the order computed here."""
    by_pen: Dict[Optional[int], List[Mark]] = {}
    for m in marks:
        by_pen.setdefault(m.pen, []).append(m)
    out: List[Mark] = []
    for pen in sorted(by_pen, key=lambda p: -1 if p is None else p):
        todo = by_pen[pen]
        cell = 4.0
        grid: Dict[Tuple[int, int], List[int]] = {}
        for i, m in enumerate(todo):
            for q in (m.pts[0], m.pts[-1]):
                grid.setdefault((int(q[0] // cell), int(q[1] // cell)), []).append(i)
        used = [False] * len(todo)
        cx, cy = 0.0, 0.0
        for _ in range(len(todo)):
            best, bd, brev = -1, 1e18, False
            ring = 0
            gx, gy = int(cx // cell), int(cy // cell)
            while best < 0 or (ring - 1) * cell < math.sqrt(bd):
                for i_ in range(gx - ring, gx + ring + 1):
                    for j_ in range(gy - ring, gy + ring + 1):
                        if max(abs(i_ - gx), abs(j_ - gy)) != ring:
                            continue
                        for i in grid.get((i_, j_), ()):
                            if used[i]:
                                continue
                            m = todo[i]
                            for rev, q in ((False, m.pts[0]), (True, m.pts[-1])):
                                dd = (q[0] - cx) ** 2 + (q[1] - cy) ** 2
                                if dd < bd:
                                    best, bd, brev = i, dd, rev
                ring += 1
                if ring > 200:
                    break
            used[best] = True
            m = todo[best]
            if brev:
                m.pts = m.pts[::-1]
            out.append(m)
            cx, cy = m.pts[-1]
    return out


HOP_MAX = 80.0           # mm: the longest in-layer travel a batch may carry


def _greedy_by_start(S: List[Pt], E: List[Pt]) -> Tuple[List[int], List[float]]:
    """EXACTLY the post-processor's pass (postprocess.optimize_stroke_order):
    from (0, 0), repeatedly the remaining stroke whose START is nearest (first
    index wins a tie).  Returns the visiting order and each travel hop."""
    n = len(S)
    used = [False] * n
    order: List[int] = []
    hops: List[float] = []
    cell = 4.0
    grid: Dict[Tuple[int, int], List[int]] = {}
    for i, (x, y) in enumerate(S):
        grid.setdefault((int(x // cell), int(y // cell)), []).append(i)
    cx = cy = 0.0
    for _ in range(n):
        gx, gy = int(cx // cell), int(cy // cell)
        best, bd, ring = -1, 1e18, 0
        while best < 0 or (ring - 1) * cell < math.sqrt(bd):
            for i_ in range(gx - ring, gx + ring + 1):
                for j_ in range(gy - ring, gy + ring + 1):
                    if max(abs(i_ - gx), abs(j_ - gy)) != ring:
                        continue
                    for i in grid.get((i_, j_), ()):
                        if used[i]:
                            continue
                        dd = (S[i][0] - cx) ** 2 + (S[i][1] - cy) ** 2
                        if dd < bd or (dd == bd and i < best):
                            best, bd = i, dd
            ring += 1
            if ring > 400:
                break
        used[best] = True
        order.append(best)
        hops.append(math.sqrt(bd))
        cx, cy = E[best]
    return order, hops


def _regions(ms: List[Mark], link: float = HOP_MAX) -> int:
    """How many ink regions a pen has, linked at ``link`` mm: a layer spread over
    k regions must make k - 1 hops longer than ``link`` whatever the order."""
    cells = sorted({(int(p[0] // 4.0), int(p[1] // 4.0)) for m in ms for p in (m.pts[0], m.pts[-1])})
    parent = list(range(len(cells)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    lim = (link - 8.0) / 4.0
    for i, a in enumerate(cells):
        for j in range(i + 1, len(cells)):
            b = cells[j]
            if math.hypot(a[0] - b[0], a[1] - b[1]) <= lim:
                parent[find(i)] = find(j)
    return len({find(i) for i in range(len(cells))})


def _polish(ms: List[Mark], budget: int = 150) -> Tuple[List[Mark], dict]:
    """Straggler repair that the post-processor cannot undo.

    The file order is whatever greedy-by-start makes of the strokes, so the
    only free variable is each stroke's DIRECTION.  Where the walk leaves a
    straggler behind (an in-layer hop > HOP_MAX that the pen's regions do not
    force), flip strokes near the hop, re-simulate the post-processor, keep a
    flip that lowers  sum(max(0, hop - HOP_MAX)) * 50 + travel."""
    S = [m.pts[0] for m in ms]
    E = [m.pts[-1] for m in ms]
    flip = [False] * len(ms)

    def cur():
        return ([E[i] if flip[i] else S[i] for i in range(len(ms))],
                [S[i] if flip[i] else E[i] for i in range(len(ms))])

    def cost(h):
        long_ = [x for x in h[1:] if x > HOP_MAX]
        return len(long_) * 1e6 + sum(x - HOP_MAX for x in long_) * 50.0 + sum(h)

    s, e = cur()
    order, hops = _greedy_by_start(s, e)
    need = _regions(ms) - 1
    best = cost(hops)
    flippable = [i for i in range(len(ms))
                 if math.hypot(S[i][0] - E[i][0], S[i][1] - E[i][1]) > 0.5]
    evals = 0
    while evals < budget:
        long_ = [k for k in range(1, len(hops)) if hops[k] > HOP_MAX]
        if len(long_) <= need:
            break
        pts: List[Pt] = []
        for k in long_:
            pts += [s[order[k]], e[order[k - 1]]]
        dist = {c: min(math.hypot(S[c][0] - p[0], S[c][1] - p[1]) for p in pts)
                for c in flippable}
        cands = sorted((c for c in flippable if dist[c] < 25.0), key=dist.get)
        pick = None
        for c in cands:              # first improvement, nearest the hop first
            if evals >= budget:
                break
            evals += 1
            flip[c] = not flip[c]
            s2, e2 = cur()
            o2, h2 = _greedy_by_start(s2, e2)
            v = cost(h2)
            flip[c] = not flip[c]
            if v < best - 1e-6:
                best, pick, keep = v, c, (s2, e2, o2, h2)
                break
        if pick is None:
            break
        flip[pick] = not flip[pick]
        s, e, order, hops = keep
    out = []
    for i in order:
        m = ms[i]
        if flip[i]:
            m.pts = m.pts[::-1]
        out.append(m)
    info = dict(regions=need + 1, evals=evals, flips=sum(flip),
                long=[round(h) for h in hops[1:] if h > HOP_MAX], travel=round(sum(hops)))
    return out, info


def build_sheet(rng: SeededRNG, bounds: Bounds, colors: int = 6) -> Sheet:
    SH = Sheet(_Map(bounds), colors)
    _title(SH)
    _qk_block(SH, +1, _pen(RED, colors))
    _qk_block(SH, -1, _pen(BLUE, colors))
    _centre_fraction(SH)
    _interference(SH, rng)
    _softmax(SH)
    _v_block(SH)
    _forward_row(SH)
    _backward(SH, rng)
    _lay_trains(SH)
    _dedupe_axes(SH)
    _clean_dots(SH)
    # the G-code carries 0.01 mm (kit._r); order on exactly those numbers, or a
    # near-tie resolves differently in the post-processor and the walk diverges
    for m in SH.marks:
        m.pts = [(round(x, 2), round(y, 2)) for x, y in m.pts]
    ordered = _order(SH.marks)
    SH.marks = []
    SH.stream = {}
    for pen in sorted({m.pen for m in ordered}, key=lambda p: -1 if p is None else p):
        ms, info = _polish([m for m in ordered if m.pen == pen])
        SH.marks += ms
        SH.stream[pen] = info
    return SH


def attention_as_resonance_ffn_iterate(
    rng: SeededRNG, bounds: Bounds, colors: int = 6
) -> List[GCodeCommand]:
    SH = build_sheet(rng, bounds, colors)
    out: List[GCodeCommand] = []
    for m in SH.marks:
        out += _poly(m.pts, color=m.pen, f=m.f)
    return out
