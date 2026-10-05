"""DIFFUSION AS TOPOGRAPHY — exact recreation of studio/diffusion-topography/ref/reference.png.

This is a REPRODUCTION, not a design.  Every element is authored in REFERENCE
PIXEL SPACE (1448 x 1086, origin top-left, y down) transcribed off a gridded
crop of the plate, then mapped once onto the drawable area.  Fidelity is the
only score; nothing here is invented.

Four pens: 0 blue (data blob + forward flow), 1 ochre (noise tangle + reverse
flow + the two red rule marks), 2 green (sample terrain), 3 black (score field,
type, furniture, dots).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import (
    _chain_segments,
    _dot,
    _marching_squares,
    _poly,
    tone_dots,
)
from promptplot.generative.engine.policies import enforce_line_spacing
from promptplot.generative.generators import _GLYPHS
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

REFW, REFH = 1448.0, 1086.0
FEED = 2000
MINGAP = 0.8  # mm — the plate's line-spacing floor

BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3


# ---------------------------------------------------------------------------
# The shared font (_GLYPHS) now carries full lowercase, so all of this plate's
# type is set from it. These FOUR characters are the only ones the reference
# needs that the shared font still lacks -- reported upstream for central
# addition; same 4x6 cell, ascender 6 / x-height 4 / descender -1.6.
# ---------------------------------------------------------------------------
_EXTRA = {
    "\u03b5": [[(3.2, 3.6), (2.3, 4), (0.95, 3.85), (0.4, 3.15), (1.0, 2.35), (2.25, 2.1),
                (1.0, 1.9), (0.35, 1.1), (0.9, 0.15), (2.3, 0.05), (3.2, 0.6)]],
    "\u03b8": [[(1.9, 6), (1.0, 5.2), (0.7, 3.0), (1.0, 0.8), (1.9, 0), (2.8, 0.8), (3.1, 3.0),
                (2.8, 5.2), (1.9, 6)], [(0.78, 3.0), (3.02, 3.0)]],
    "^": [[(1.0, 4.9), (1.9, 6.0), (2.8, 4.9)]],
    "_": [[(0.2, -0.7), (3.6, -0.7)]],
    "|": [[(1.85, -0.5), (1.85, 4.8)]],
}


def _glyph(ch: str):
    if ch in _GLYPHS:
        return _GLYPHS[ch]
    if ch in _EXTRA:
        return _EXTRA[ch]
    return _GLYPHS.get(ch.upper(), [])


# ---------------------------------------------------------------------------
# reference-pixel -> mm mapping (aspect preserved to within 6%)
# ---------------------------------------------------------------------------
class Ref:
    def __init__(self, bounds: Bounds):
        x0, y0, x1, y1 = bounds
        w, h = x1 - x0, y1 - y0
        self.sy = h / REFH
        self.sx = min(w / REFW, self.sy * 1.06)
        self.ox = x0 + (w - REFW * self.sx) / 2.0
        self.oy = y0 + (h - REFH * self.sy) / 2.0

    def p(self, px: float, py: float) -> Tuple[float, float]:
        return (self.ox + px * self.sx, self.oy + (REFH - py) * self.sy)

    def mm(self, v_px: float) -> float:
        return v_px * self.sy


# ---------------------------------------------------------------------------
# curve + stroke helpers (all take reference pixels, emit mm)
# ---------------------------------------------------------------------------
def _catmull(pts: Sequence[Tuple[float, float]], per_seg: int = 14):
    if len(pts) < 3:
        return list(pts)
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(len(P) - 3):
        p0, p1, p2, p3 = P[i], P[i + 1], P[i + 2], P[i + 3]
        for k in range(per_seg):
            t = k / per_seg
            t2, t3 = t * t, t * t * t
            out.append((
                0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t
                       + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
                0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t
                       + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3),
            ))
    out.append(tuple(pts[-1]))
    return out


def _dash_split(pts_mm, on: float, off: float):
    """Split a polyline (mm) into dashes of length `on` separated by `off`."""
    runs, cur, phase, pen_on = [], [], 0.0, True
    if len(pts_mm) < 2:
        return runs
    cur = [pts_mm[0]]
    for a, b in zip(pts_mm, pts_mm[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        t = 0.0
        while t < seg - 1e-9:
            want = (on if pen_on else off) - phase
            step = min(want, seg - t)
            t += step
            phase += step
            q = (a[0] + (b[0] - a[0]) * t / seg, a[1] + (b[1] - a[1]) * t / seg)
            if pen_on:
                cur.append(q)
            if phase >= (on if pen_on else off) - 1e-9:
                if pen_on and len(cur) >= 2:
                    runs.append(cur)
                pen_on = not pen_on
                phase = 0.0
                cur = [q] if pen_on else []
    if pen_on and len(cur) >= 2:
        runs.append(cur)
    return runs


class Plate:
    def __init__(self, ref: Ref, colors: int):
        self.r = ref
        self.colors = colors
        self.out: List[GCodeCommand] = []

    def px(self, mm: float) -> float:
        """millimetres expressed in reference pixels."""
        return mm / self.r.sy

    def mark(self) -> int:
        return len(self.out)

    def guard(self, start: int, min_dist: float = 0.85) -> None:
        """Hard minimum-separation floor on everything emitted since ``mark()``.
        Contour bundles, stacked terrain profiles and nested ellipses all crowd
        where the field is steep; this thins them instead of letting them flood."""
        seg = self.out[start:]
        del self.out[start:]
        self.out.extend(enforce_line_spacing(seg, min_dist, resample=0.35, min_run=1.2))

    def pen(self, idx: int) -> Optional[int]:
        return idx % self.colors if self.colors > 1 else None

    # --- emit ------------------------------------------------------------
    def line_px(self, pts_px, pen, dash=None, feed=FEED, closed=False):
        pts = [self.r.p(x, y) for x, y in pts_px]
        if closed and pts and pts[0] != pts[-1]:
            pts.append(pts[0])
        if dash is None:
            self.out += _poly(pts, color=self.pen(pen), f=feed)
        else:
            for run in _dash_split(pts, dash[0], dash[1]):
                self.out += _poly(run, color=self.pen(pen), f=feed)

    def curve_px(self, ctrl_px, pen, dash=None, per_seg=14, feed=FEED):
        self.line_px(_catmull(ctrl_px, per_seg), pen, dash=dash, feed=feed)

    def rule(self, x0, y0, x1, y1, pen=BLACK, dash=None):
        self.line_px([(x0, y0), (x1, y1)], pen, dash=dash)

    def ring_px(self, cx, cy, r_px, pen, dash=None, n=64):
        pts = [(cx + r_px * math.cos(2 * math.pi * k / n),
                cy + r_px * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
        self.line_px(pts, pen, dash=dash)

    def arc_px(self, cx, cy, r_px, a0_deg, a1_deg, pen, dash=None, rx=None, ry=None):
        rx = r_px if rx is None else rx
        ry = r_px if ry is None else ry
        n = max(24, int(abs(a1_deg - a0_deg) * 1.2))
        pts = []
        for k in range(n + 1):
            a = math.radians(a0_deg + (a1_deg - a0_deg) * k / n)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        self.line_px(pts, pen, dash=dash)

    def dot(self, cx, cy, r_px, pen=BLACK, filled=True):
        """Solid dot: nested rings at 0.42mm (dot fill is a solid feature, not a
        line field — the 0.8mm floor governs parallel line work)."""
        c = self.r.p(cx, cy)
        rr = self.r.mm(r_px)
        p = self.pen(pen)
        if not filled:
            self.ring_px(cx, cy, r_px, pen)
            return
        if rr <= 0.42:
            self.out += _dot(c[0], c[1], max(0.18, rr), color=p)
            return
        # archimedean spiral fill, then a clean outline
        turns = max(2, int(rr / 0.42))
        n = turns * 26
        pts = []
        for k in range(n + 1):
            t = k / n
            a = 2 * math.pi * turns * t
            pts.append((c[0] + rr * t * math.cos(a), c[1] + rr * t * math.sin(a)))
        self.out += _poly(pts, color=p, f=1600)
        if r_px >= 4.5:
            self.ring_px(cx, cy, r_px, pen, n=40)

    def sq(self, x0, y0, x1, y1, pen=BLACK, spacing=0.42):
        a = self.r.p(x0, y1)
        b = self.r.p(x1, y0)
        pts, y, flip = [], min(a[1], b[1]), False
        top = max(a[1], b[1])
        xa, xb = min(a[0], b[0]), max(a[0], b[0])
        while y <= top + 1e-9:
            row = [(xa, y), (xb, y)]
            pts.extend(reversed(row) if flip else row)
            flip = not flip
            y += spacing
        self.out += _poly(pts, color=self.pen(pen), f=1600)

    # --- type ------------------------------------------------------------
    def text(self, parts, x_px, base_px, h_px, pen=BLACK, track=1.7):
        """parts: str, or list of (str, 'n'|'sub'|'sup'). h_px = cap/ascender height."""
        if isinstance(parts, str):
            parts = [(parts, "n")]
        cx = x_px
        for s, mode in parts:
            k = 0.66 if mode in ("sub", "sup") else 1.0
            hb = h_px * k
            u = hb / 6.0                       # glyph unit in ref px
            dy = {"n": 0.0, "sub": h_px * 0.20, "sup": -h_px * 0.42}[mode]
            adv = 5.6 * u * track
            for ch in s:
                for stroke in _glyph(ch):
                    pts = [(cx + gx * u, base_px + dy - gy * u) for gx, gy in stroke]
                    self.line_px(pts, pen)
                cx += adv
        return cx

    def text_w(self, parts, h_px, track=1.7):
        if isinstance(parts, str):
            parts = [(parts, "n")]
        w = 0.0
        for s, mode in parts:
            k = 0.66 if mode in ("sub", "sup") else 1.0
            w += len(s) * 5.6 * (h_px * k / 6.0) * track
        return w


# ---------------------------------------------------------------------------
# scalar fields + contouring
# ---------------------------------------------------------------------------
def _mix(X, Y, peaks):
    F = np.zeros_like(X)
    for cx, cy, sx, sy, w in peaks:
        F += w * np.exp(-(((X - cx) / sx) ** 2 + ((Y - cy) / sy) ** 2) / 2.0)
    return F


def _even_levels(F, cell, f_lo, f_hi, step_px, max_levels=80, pct=0.82):
    """Iso levels spaced by real DISTANCE, not by value.

    Evenly-spaced iso VALUES bunch wherever the field is steep, which is how a
    contour bundle ends up below the pen-tip gap and floods. Stepping by
    ``level += distance * median|grad F|`` along each contour instead puts the
    rings a fixed number of millimetres apart wherever they run, so the whole
    field can stay CONTINUOUS (no thinning, no chopped dashes).
    The step uses a HIGH PERCENTILE of |grad F| along the level, not the median:
    the gap between two rings is narrowest where the field is steepest, so sizing
    by the median leaves the steep stretches far under the pen-tip gap while the
    flat ones are fine. Sizing by the 82nd percentile makes the TIGHTEST stretch
    the design gap, which is what a plotter actually needs.
    ``step_px`` may be a float or a callable ``k -> float``.
    """
    gy, gx = np.gradient(F, cell, cell)
    G = np.hypot(gx, gy)
    rng_f = f_hi - f_lo
    levels: List[float] = []
    v = f_lo
    while v < f_hi and len(levels) < max_levels:
        levels.append(v)
        g = 0.0
        for wfrac in (0.004, 0.009, 0.02, 0.05, 0.12):
            band = np.abs(F - v) < wfrac * rng_f
            if int(band.sum()) >= 24:
                g = float(np.quantile(G[band], pct))
                break
        if g <= 1e-12:
            break
        st = step_px(len(levels) - 1) if callable(step_px) else step_px
        v += st * g
    return levels


def _contours(plate: Plate, peaks, box, cell, levels, pen, dashed=None,
              dash=(1.1, 1.0), min_len_px=6.0, smooth=True, field=None):
    x0, y0, x1, y1 = box
    xs = np.arange(x0, x1 + cell, cell)
    ys = np.arange(y0, y1 + cell, cell)
    if field is None:
        X, Y = np.meshgrid(xs, ys)
        field = _mix(X, Y, peaks)
    xl, yl = list(xs), list(ys)
    Fl = field.tolist()
    n = 0
    for li, iso in enumerate(levels):
        segs = _marching_squares(Fl, xl, yl, iso)
        if not segs:
            continue
        is_dash = dashed(li) if callable(dashed) else False
        for chain in _chain_segments(segs):
            if len(chain) < 3:
                continue
            ln = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(chain, chain[1:]))
            if ln < min_len_px:
                continue
            pts = _catmull(chain, per_seg=2) if smooth else chain
            plate.line_px(pts, pen, dash=(dash if is_dash else None))
            n += 1
    return n


# ---------------------------------------------------------------------------
# THE PLATE
# ---------------------------------------------------------------------------
def diffusion_topography(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    ref = Ref(bounds)
    P = Plate(ref, colors)

    _furniture(P, rng)
    _data_blob(P, rng)
    _noise_tangle(P, rng)
    _score_field(P, rng)
    _schedule(P, rng)
    _sample_terrain(P, rng)
    _flows(P, rng)
    _type(P)
    return P.out


# ------------------------------------------------------------------ data x_0
def _data_blob(P: Plate, rng: SeededRNG) -> None:
    # lobes transcribed off the plate; tight sigmas so the notches between them
    # survive into the outline -- the concavities are the whole character.
    peaks = [
        (242, 84, 34, 29, 0.66),
        (150, 112, 29, 27, 0.62),
        (104, 178, 26, 30, 0.60),
        (156, 250, 28, 26, 0.60),
        (214, 272, 29, 25, 0.62),
        (266, 252, 28, 25, 0.56),
        (288, 152, 25, 28, 0.50),
        (198, 170, 54, 52, 1.05),
    ]
    box, cell = (55, 15, 335, 325), 1.9
    xs = np.arange(box[0], box[2] + cell, cell)
    ys = np.arange(box[1], box[3] + cell, cell)
    X, Y = np.meshgrid(xs, ys)
    F = _mix(X, Y, peaks)
    fmax = float(F.max())
    levels = _even_levels(F, cell, 0.255 * fmax, 0.988 * fmax, P.px(0.92))
    # solid outline, a stipple band just inside it, solid rings from there in
    mk = P.mark()
    _contours(P, peaks, box, cell, levels, BLUE, field=F,
              dashed=lambda li: 1 <= li <= 2, dash=(0.55, 1.05), min_len_px=12.0)
    P.guard(mk, 0.70)
    for cx, cy, r in [(137, 152, 5.2), (205, 141, 5.4), (196, 178, 6.2), (219, 177, 4.6)]:
        P.dot(cx, cy, r, BLACK)
    P.line_px([(137, 152), (200, 150), (262, 148)], BLACK)
    P.line_px([(196, 178), (250, 168), (300, 160)], BLACK)


# ----------------------------------------------------------------- noise x_T
def _noise_tangle(P: Plate, rng: SeededRNG) -> None:
    cx0, cy0 = 1116, 174
    n_loops = 36
    for i in range(n_loops):
        # jittered centre, biased toward the core
        rr = 80 * (rng.random() ** 0.55)
        ang = rng.uniform(0, 2 * math.pi)
        cx = cx0 + rr * math.cos(ang) * 1.12
        cy = cy0 + rr * math.sin(ang) * 0.80
        R = 28 + 108 * (rng.random() ** 1.05)
        asp = rng.uniform(0.30, 1.0)
        rot = rng.uniform(0, math.pi)
        h1, h2, h3 = rng.uniform(0.06, 0.26), rng.uniform(0.04, 0.20), rng.uniform(0.02, 0.14)
        p1, p2, p3 = rng.uniform(0, 6.3), rng.uniform(0, 6.3), rng.uniform(0, 6.3)
        pts = []
        for k in range(97):
            t = 2 * math.pi * k / 96
            rad = R * (1 + h1 * math.sin(2 * t + p1) + h2 * math.sin(3 * t + p2)
                       + h3 * math.sin(5 * t + p3))
            ux, uy = rad * math.cos(t), rad * asp * math.sin(t)
            pts.append((cx + ux * math.cos(rot) - uy * math.sin(rot),
                        cy + ux * math.sin(rot) + uy * math.cos(rot)))
        dash = (1.3, 1.1) if i % 5 == 4 else None
        P.line_px(pts, OCHRE, dash=dash)
    # black dots inside + the thin black lines fanning off the big one
    P.dot(1085, 152, 4.6, BLACK)
    P.dot(1150, 180, 7.4, BLACK)
    P.dot(1097, 240, 4.6, BLACK)
    P.dot(1020, 205, 4.4, BLACK)
    P.ring_px(1020, 205, 6.4, OCHRE)
    P.curve_px([(1150, 180), (1090, 190), (1020, 205)], BLACK)
    P.curve_px([(1150, 180), (1100, 215), (1050, 248), (1010, 262)], BLACK)
    P.curve_px([(1150, 180), (1122, 212), (1097, 240)], BLACK)


# --------------------------------------------------------- score eps(x_t, t)
def _score_field(P: Plate, rng: SeededRNG) -> None:
    # one narrow dominant peak plus heavy near satellites -> the level sets bulge
    # toward each satellite and the contours come out star-lobed, as on the plate.
    peaks = [
        (658, 447, 36, 34, 1.00),
        (668, 378, 42, 36, 0.48),
        (728, 412, 42, 36, 0.48),
        (738, 494, 44, 38, 0.44),
        (692, 536, 42, 38, 0.44),
        (606, 516, 42, 38, 0.42),
        (576, 432, 42, 38, 0.46),
        (604, 380, 40, 34, 0.38),
        (806, 452, 52, 44, 0.22),
        (516, 492, 48, 42, 0.20),
        (704, 598, 50, 42, 0.18),
        (650, 306, 50, 42, 0.18),
        (852, 388, 46, 40, 0.13),
    ]
    box, cell = (420, 240, 930, 650), 2.0
    xs = np.arange(box[0], box[2] + cell, cell)
    ys = np.arange(box[1], box[3] + cell, cell)
    X, Y = np.meshgrid(xs, ys)
    F = _mix(X, Y, peaks)
    fmax = float(F.max())
    # outer contours sparse (2.6 mm), the nest around the peak tight (0.95 mm)
    levels = _even_levels(F, cell, 0.030 * fmax, 0.988 * fmax,
                          lambda k: P.px(2.1 if k < 7 else 0.92))
    _contours(P, peaks, box, cell, levels, BLACK, field=F,
              dashed=lambda li: li < 7, dash=(1.9, 1.7), min_len_px=16.0)
    for cx, cy, r in [(658, 447, 6.6), (611, 447, 6.0), (700, 462, 5.2), (733, 373, 6.0),
                      (790, 392, 6.0), (778, 512, 6.0)]:
        P.dot(cx, cy, r, BLACK)


# ------------------------------------------------------------------ schedule
def _schedule(P: Plate, rng: SeededRNG) -> None:
    # the flat ellipse and its nested companions
    P.arc_px(678, 670, 0, 0, 360, BLACK, rx=178, ry=37)
    for rx, ry in [(156, 32), (132, 27), (110, 22.5), (90, 18), (70, 13.5), (52, 9)]:
        P.arc_px(700, 670, 0, 0, 360, BLACK, rx=rx, ry=ry)
    # tonal mass toward t = T -- tone_dots: tone drives the PROBABILITY a cell
    # is inked, never the spacing, so this cannot crowd into a black mass.
    a_mm = P.r.p(604, 646)
    b_mm = P.r.p(822, 694)
    region = (min(a_mm[0], b_mm[0]), min(a_mm[1], b_mm[1]),
              max(a_mm[0], b_mm[0]), max(a_mm[1], b_mm[1]))

    def _tone(xm, ym):
        px = (xm - P.r.ox) / P.r.sx
        py = REFH - (ym - P.r.oy) / P.r.sy
        ex, ey = (px - 728) / 98.0, (py - 670) / 24.0
        d = ex * ex + ey * ey
        if d > 1.0:
            return 0.0
        edge = min(1.0, (1.0 - d) * 3.0)                 # soft ellipse edge
        ramp = max(0.0, min(1.0, (px - 648) / 158.0)) ** 1.25
        return edge * (0.10 + 0.90 * ramp)

    P.out += tone_dots(region, _tone, rng, pen=P.pen(BLACK), cell=1.0, jitter=0.55, r=0.3)

    # the graduated dot row
    P.ring_px(528, 670, 4.4, BLACK)
    P.ring_px(573, 670, 4.4, BLACK)
    for x in (548, 558, 566):
        P.dot(x, 670, 1.5, BLACK)
    x = 585
    r = 1.7
    while x < 672:
        P.dot(x, 670, r, BLACK)
        x += 8.6
        r += 0.16
    P.dot(680, 670, 8.4, BLACK)
    x = 694
    while x < 792:
        P.dot(x, 670, 3.0, BLACK)
        x += 11.0
    P.dot(802, 670, 7.6, BLACK)
    P.dot(835, 670, 5.4, BLACK)
    # tick marks the schedule sits on
    P.rule(683, 636, 683, 706, BLACK, dash=(1.6, 1.4))
    P.rule(706, 640, 706, 702, BLACK, dash=(1.2, 1.6))
    P.rule(730, 644, 730, 698, BLACK, dash=(1.2, 1.6))


# ---------------------------------------------------------- sample x-hat_0
def _sample_terrain(P: Plate, rng: SeededRNG) -> None:
    X0, X1 = 796, 1292
    rows, dy, amp, base = 24, 5.2, 64.0, 902.0
    ns = 300
    bumps = [
        (0.43, 0.72, 0.030, 0.38, 1.05),
        (0.59, 0.64, 0.032, 0.36, 1.00),
        (0.51, 0.50, 0.040, 0.40, 0.56),
        (0.30, 0.52, 0.070, 0.44, 0.58),
        (0.72, 0.48, 0.060, 0.42, 0.52),
        (0.16, 0.42, 0.075, 0.44, 0.34),
        (0.84, 0.34, 0.070, 0.38, 0.20),
        (0.38, 0.26, 0.060, 0.34, 0.34),
        (0.665, 0.80, 0.026, 0.26, 0.44),
        (0.24, 0.10, 0.095, 0.34, -0.72),
        (0.56, 0.06, 0.085, 0.30, -0.80),
        (0.70, 0.14, 0.085, 0.32, -0.56),
        (0.12, 0.18, 0.095, 0.36, -0.36),
        (0.88, 0.20, 0.080, 0.36, -0.40),
    ]

    def z(u, t):
        v = 0.0
        for bu, bt, su, st, w in bumps:
            v += w * math.exp(-(((u - bu) / su) ** 2 + ((t - bt) / st) ** 2) / 2.0)
        v += 0.055 * math.sin(u * 27.0 + t * 5.0) * math.exp(-((t - 0.4) / 0.4) ** 2)
        # taper at the ends so the terrain dies into blank paper
        v *= math.exp(-((u - 0.5) / 0.52) ** 4)
        return v

    eps = 0.76 / P.r.sy
    horizon = [1e9] * ns
    for j in range(rows):
        t = j / (rows - 1.0)
        run: List[Tuple[float, float]] = []
        pen = BLACK if j < 3 else GREEN
        for i in range(ns):
            u = i / (ns - 1.0)
            x = X0 + u * (X1 - X0)
            w = 0.12 + 0.88 * math.exp(-((u - 0.5) / 0.50) ** 4)
            y = base - j * dy * w - amp * z(u, t)
            if y < horizon[i] - eps:
                run.append((x, y))
            else:
                if len(run) >= 2:
                    P.line_px(run, pen)
                run = []
            horizon[i] = min(horizon[i], y)
        if len(run) >= 2:
            P.line_px(run, pen)
    for cx, cy, r in [(1013, 822, 5.6), (1037, 858, 6.2), (1127, 895, 6.2)]:
        P.dot(cx, cy, r, BLACK)


# --------------------------------------------------------------------- flows
def _flows(P: Plate, rng: SeededRNG) -> None:
    D = (2.6, 2.3)
    # forward q(x_t | x_0) — blue, blob -> score
    P.curve_px([(200, 170), (268, 193), (335, 222), (412, 272), (490, 325),
                (545, 352), (587, 378), (602, 412), (588, 445)], BLUE)
    P.curve_px([(207, 145), (300, 152), (400, 180), (490, 222), (560, 268),
                (610, 320), (626, 378), (612, 425), (590, 447)], BLUE)
    P.curve_px([(250, 148), (312, 142), (372, 140), (450, 152), (520, 178), (580, 215),
                (626, 266), (646, 320), (640, 376), (620, 416)], BLUE, dash=D)
    P.curve_px([(255, 168), (330, 190), (410, 218), (480, 248), (540, 282),
                (582, 320), (602, 362), (598, 402)], BLUE, dash=D)
    P.curve_px([(250, 268), (330, 318), (420, 364), (510, 390), (580, 384),
                (626, 360), (650, 324)], BLUE, dash=D)
    for cx, cy, r in [(335, 222, 4.6), (490, 325, 4.4), (587, 378, 5.2),
                      (560, 192, 3.6), (370, 140, 3.6)]:
        P.dot(cx, cy, r, BLUE)
    P.dot(588, 445, 5.4, BLACK)
    # the long blue dashed sweep down-left
    P.curve_px([(582, 514), (520, 546), (440, 576), (360, 600), (300, 618),
                (252, 602), (238, 588)], BLUE, dash=D)
    P.curve_px([(576, 532), (510, 564), (430, 594), (355, 616), (300, 630),
                (254, 614), (241, 599)], BLUE, dash=D)
    P.curve_px([(568, 550), (500, 582), (420, 610), (350, 630), (303, 640),
                (259, 624), (246, 610)], BLUE, dash=D)
    P.dot(490, 596, 4.0, BLUE)

    # reverse p(x_{t-1} | x_t) — ochre, tangle -> score -> sample
    P.curve_px([(1150, 185), (1075, 212), (995, 245), (925, 275), (888, 297),
                (850, 335), (822, 382), (812, 428), (820, 458), (804, 476),
                (786, 472)], OCHRE)
    P.curve_px([(1148, 192), (1060, 252), (980, 322), (920, 392), (880, 460),
                (862, 520), (868, 580), (900, 640), (958, 690), (1018, 742),
                (1052, 792)], OCHRE)
    P.curve_px([(1158, 180), (1092, 266), (1042, 350), (1012, 440), (1012, 520),
                (1032, 600), (1060, 662), (1078, 722), (1082, 776)], OCHRE)
    P.curve_px([(1115, 165), (1030, 195), (958, 208), (900, 240), (850, 290),
                (812, 350), (796, 410), (802, 456)], OCHRE, dash=D)
    P.curve_px([(1182, 240), (1122, 290), (1062, 340), (1012, 400), (976, 460),
                (956, 520), (952, 580), (968, 640), (1002, 700), (1042, 762)],
               OCHRE, dash=D)
    P.curve_px([(1206, 256), (1160, 322), (1120, 392), (1090, 462), (1076, 532),
                (1076, 602), (1086, 672), (1096, 732), (1090, 782)], OCHRE, dash=D)
    P.curve_px([(760, 530), (810, 556), (856, 576), (940, 606), (1026, 628),
                (1080, 640)], OCHRE, dash=(1.9, 1.9))
    for cx, cy, r, filled in [(888, 297, 4.6, True), (958, 208, 4.2, False),
                              (820, 458, 4.2, False), (836, 484, 4.2, True),
                              (795, 526, 4.0, True), (856, 576, 4.2, False),
                              (1026, 628, 4.4, True), (1067, 578, 4.2, False),
                              (1082, 776, 4.4, True), (1052, 792, 3.6, True)]:
        P.dot(cx, cy, r, OCHRE, filled=filled)


# ----------------------------------------------------------------- furniture
def _furniture(P: Plate, rng: SeededRNG) -> None:
    dot = (0.7, 2.4)      # dotted
    dsh = (2.6, 2.4)      # dashed
    ddt = (4.5, 2.0)      # dash-dot-ish (long dash)

    # --- upper left
    P.dot(41, 52, 2.4)
    P.rule(41, 20, 41, 104, BLACK, dash=dot)
    P.rule(19, 152, 64, 152)
    P.dot(41, 152, 5.6)
    P.dot(81, 238, 6.4)
    P.rule(41, 118, 41, 205, BLACK, dash=dot)
    P.rule(63, 286, 63, 432, OCHRE, dash=(4.0, 3.2))   # the two red rule marks
    P.rule(57, 300, 57, 348, OCHRE, dash=(3.0, 3.0))
    P.rule(37, 358, 172, 358)
    P.rule(107, 302, 107, 360)
    P.ring_px(128, 390, 3.8, BLACK)
    P.dot(123, 428, 3.2)

    # --- left middle
    P.dot(173, 573, 4.6)
    for k, r in enumerate([3.0, 2.6, 2.2, 2.6]):
        P.dot(71, 618 + 13 * k, r)
    P.rule(71, 668, 71, 742, BLACK, dash=dot)
    P.arc_px(205, 650, 72, 55, 305, BLACK)
    P.rule(186, 636, 246, 636)
    P.rule(210, 540, 210, 734)
    P.dot(210, 637, 7.4)
    P.rule(363, 530, 363, 652, BLACK, dash=ddt)
    P.rule(422, 528, 422, 736, BLACK, dash=dot)

    # --- lower left
    P.arc_px(420, 880, 115, 180, 270, BLACK)
    P.rule(422, 752, 422, 798)
    P.rule(422, 769, 474, 769)
    P.dot(495, 838, 3.4)
    P.rule(278, 1010, 384, 1010)

    # --- upper middle
    P.rule(578, 12, 578, 122, BLACK, dash=dot)
    P.rule(628, 14, 628, 202, BLACK, dash=ddt)
    P.dot(630, 148, 6.0)
    P.curve_px([(556, 74), (600, 49), (652, 43), (702, 73), (762, 133),
                (832, 190), (906, 250)], BLACK, dash=dsh)
    P.line_px([(610, 326), (610, 242)], BLACK)
    P.line_px([(606, 250), (610, 240), (614, 250)], BLACK)
    P.dot(665, 268, 4.2)

    # --- centre spine
    P.rule(683, 266, 683, 560, BLACK, dash=ddt)
    P.rule(683, 590, 683, 1030, BLACK, dash=(5.5, 4.0))
    P.dot(683, 580, 5.2)
    P.dot(683, 608, 6.6)
    P.dot(683, 799, 11.0)
    P.dot(683, 908, 3.8)
    P.rule(648, 937, 722, 937)
    P.dot(683, 1013, 8.0)
    for x in (662, 712, 727):
        P.rule(x, 558, x, 644, BLACK, dash=dot)
    P.line_px([(606, 634), (585, 657)], BLACK)
    P.line_px([(585, 657), (592, 650)], BLACK)
    P.line_px([(585, 657), (594, 656)], BLACK)

    # --- around the score field
    P.rule(690, 470, 786, 470, BLACK, dash=ddt)
    P.rule(728, 418, 728, 502)
    P.rule(915, 348, 915, 472, BLACK, dash=dot)
    P.rule(895, 390, 938, 390)
    P.rule(898, 442, 942, 442)

    # --- upper right
    P.rule(752, 130, 792, 130)
    P.rule(792, 130, 792, 195)
    P.line_px([(752, 130), (760, 126)], BLACK)
    P.line_px([(752, 130), (760, 134)], BLACK)
    P.dot(994, 112, 3.6)
    P.dot(955, 288, 5.4)
    P.rule(1400, 133, 1400, 192)
    P.rule(1362, 240, 1414, 240)
    P.rule(1398, 218, 1398, 262)
    P.rule(1250, 238, 1292, 238)
    P.rule(1250, 238, 1250, 252)
    P.arc_px(1770, 573, 462, 142.7, 221.7, BLACK)

    # --- right / lower right
    P.dot(1370, 500, 3.6)
    P.rule(1073, 758, 1145, 758)
    P.rule(1105, 758, 1105, 1012)
    P.rule(1105, 833, 1137, 833)
    P.dot(1330, 995, 3.4)
    P.rule(862, 700, 862, 986, BLACK, dash=ddt)
    P.rule(800, 782, 930, 782, BLACK, dash=dot)
    P.dot(888, 858, 5.2)
    P.dot(835, 845, 5.2)
    P.curve_px([(868, 762), (880, 832), (902, 902), (942, 956), (996, 988),
                (1046, 972)], BLACK, dash=dsh)
    P.rule(1317, 872, 1334, 872)
    P.rule(1317, 872, 1317, 888)
    P.rule(1290, 898, 1327, 898)
    P.rule(1290, 912, 1327, 912)
    P.rule(1290, 898, 1290, 912)
    P.rule(1327, 898, 1327, 912)
    P.dot(1300, 893, 5.4)
    P.rule(1390, 855, 1408, 855)
    P.rule(1403, 858, 1403, 932, BLACK, dash=dot)
    P.sq(1147, 1006, 1159, 1022)
    P.rule(1175, 1023, 1403, 1023)


# ---------------------------------------------------------------------- type
def _type(P: Plate) -> None:
    """All type set from the shared font. Sizes/positions measured off the plate:
    label ascender 14 px, formula 13 px, caption cap 11 px, title cap 15 px."""
    H, HF, HS, HT = 14.0, 13.0, 11.0, 15.0
    TL, TF, TC, TT = 1.14, 1.10, 1.22, 1.38

    P.text("data", 85, 62, H, BLACK, track=TL)
    P.text([("x", "n"), ("_", "n"), ("0", "n")], 86, 90, HF, BLACK, track=TF)

    P.text("noise", 1330, 76, H, BLACK, track=TL)
    P.text([("x", "n"), ("T", "sub")], 1364, 102, HF, BLACK, track=TF)

    P.text("score", 752, 292, H, BLACK, track=TL)
    P.text([("\u03b5", "n"), ("\u03b8", "sub"), ("(x", "n"), ("t", "sub"),
            (", t)", "n")], 756, 320, HF, BLACK, track=TF)

    P.text("forward", 338, 308, H, BLACK, track=TL)
    P.text([("q(x", "n"), ("t", "sub"), (" | x", "n"), ("0", "sub"), (")", "n")],
           341, 336, HF, BLACK, track=TF)

    P.text("reverse", 1091, 478, H, BLACK, track=TL)
    P.text([("p", "n"), ("\u03b8", "sub"), ("(x", "n"), ("t-1", "sub"), (" | x", "n"),
            ("t", "sub"), (")", "n")], 1097, 506, HF, BLACK, track=TF)

    P.text("sample", 1190, 796, H, BLACK, track=TL)
    P.text([("x", "n")], 1213, 826, HF, BLACK, track=TF)
    P.text([("^", "n")], 1213, 826, HF, BLACK, track=TF)
    P.text([("0", "sub")], 1226, 826, HF, BLACK, track=TF)

    P.text([("t = 0", "n")], 478, 675, 10.5, BLACK, track=0.80)
    P.text([("t = T", "n")], 854, 675, 10.5, BLACK, track=0.80)
    P.text("schedule", 660, 743, 12.0, BLACK, track=0.86)

    # title block, lower left
    P.text("DIFFUSION", 45, 871, HT, BLACK, track=TT)
    P.text("AS", 45, 899, HT, BLACK, track=TT)
    P.text("TOPOGRAPHY", 45, 928, HT, BLACK, track=TT)
    P.rule(45, 963, 158, 963)
    P.text("FROM NOISE", 45, 990, HS, BLACK, track=TC)
    P.text("TO STRUCTURE", 45, 1011, HS, BLACK, track=TC)

    # colophon, lower right (right-aligned on x = 1400)
    for txt, base in (("GENERATIVE", 975), ("FIELDS", 990), ("IN CONTINUOUS TIME", 1009)):
        w = P.text_w(txt, HS, track=TC)
        P.text(txt, 1400 - w, base, HS, BLACK, track=TC)
