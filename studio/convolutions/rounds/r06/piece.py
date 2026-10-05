"""CONVOLUTIONS — r06 · wildcard · Memphis Group canon · parent r04 (by lineage only).

ORDER: SUPERPOSITION — one confetti field, stamped.  Nothing from r01–r05 is
reused: no lattice, no window, no wavefront, no pipeline, no blob.

LINEAGE: Ettore Sottsass, *Bacterio* laminate for Abet Laminati (1978), and
the Memphis confetti-on-grid surfaces.  The order it lends: ONE small motif
stamped at scattered points over a surface.  That is literally ``Y = K * X``
with X a scatter of impulses — read the other way, every squiggle on a Memphis
surface is a SUM.  Subtitle on the sheet: "every squiggle is a sum".

What every mark carries (all computed, nothing decorative):

* X — the input: ``X = sum_i delta(p - p_i)``, unit impulses at the confetti
  positions p_i.  A random-sequential-adsorption (hard-core) scatter whose
  exclusion radius grows (smoothstep) with distance from ONE crowd focus, from
  7 mm to 34 mm over 150 mm, so every card crosses from a crowd to solitude.
  Confetti never lands on a card keyline or the laminate edge.  Each impulse is
  one black triangle, drawn on top of everything: no input is ever hidden.
* K1, K2, K3 — the kernels a CNN's first layer is known to learn: two Gabors
  (bars at 30 and 120 deg, wavelength LAM = 12 mm, envelope SIG = 0.8 LAM) and
  one Gaussian blur (BLUR_SIG = 3.6 mm).  Each peaks at exactly 1 for a single
  impulse.
* Y_j = K_j * X — evaluated EXACTLY (direct sum over every impulse on the
  sheet, including those outside the card, no FFT) on a 0.4 mm grid.  Drawn in
  the kernel's pen as
    - the LINE ``Y = LEVEL`` (0.35): every impulse's stamp;
    - the SOLID ``Y > SUM_LEVEL`` (1.25): a single impulse peaks at 1, so only
      overlapping stamps adding up can reach it.  Filled along the kernel's
      own bars at 0.8 mm, inset so its edge stays >= 0.8 mm (measured) inside
      the 0.35 line.
  A card is a window onto its map at the true position (translation
  equivariance: the map is registered to the confetti above it).
* Ground grid: pitch = LAM, the Gabor wavelength — a ruler for the bars.  The
  strict Memphis ground: a laminate slab bleeding off right and bottom, the key
  a block of whole grid cells knocked out of it.
* Depth (declared): cards stacked disc < square < triangle, each with a
  4-pass keyline and a 3.4 mm 45-deg hatched cast shadow; a card and its
  shadow hide the maps and grid behind them.  X is never hidden: every line
  stops 1 mm off every confetti triangle.

Pens (palette order = streaming order, light -> dark so black lands last):
0 darkorange = Y3 (blur) · 1 crimson = Y1 (Gabor 30) · 2 dodgerblue = Y2
(Gabor 120) · 3 black = X confetti, card keylines + shadows, ground grid, type.

Entry point: ``convolutions_memphis``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import contourpy
import numpy as np

from promptplot.generative.engine.geometry import (Circle, Complement, Intersect, Polygon, Region,
                                                   Union, clip)
from promptplot.generative.engine.kit import giant_type
from promptplot.generative.generators import _poly, _stroke_text, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

ORANGE, RED, BLUE, BLACK = 0, 1, 2, 3
F = 2200

# --- the science ------------------------------------------------------------
LAM = 12.0          # Gabor wavelength (mm) == ground-grid pitch
SIG = 0.8 * LAM     # Gabor envelope sigma (mm): three bars per lone stamp
BLUR_SIG = 3.6      # Gaussian-blur sigma (mm)
LEVEL = 0.35        # the drawn level, as a fraction of one impulse's peak
SUM_LEVEL = 1.25    # second level: > 1 = a lone impulse's peak, so ONLY a sum reaches it
SOLID_INSET = 1.0   # the solid's edge keeps this far (mm) inside the Y = LEVEL line
FILL_PITCH = 0.8    # the solid inside Y > SUM_LEVEL: hatch pitch (mm), >= 0.8 floor
FILL_DEG = {"K1": 30.0, "K2": 120.0, "K3": 45.0}  # fill runs along each kernel's bars
GRID_H = 0.4        # evaluation grid (mm)
R_DENSE, R_SPARSE = 7.0, 34.0  # hard-core exclusion radius ramp (mm)

# --- the pen ----------------------------------------------------------------
CHIP_R = 1.3        # confetti triangle circumradius (mm)
CHIP_HALO = CHIP_R + 1.0
KEYLINE_W = 1.05    # card keyline band width (mm), 4 passes
SHADOW = (3.4, -3.4)
HATCH = 0.9
CARD_GAP = 1.1      # map lines stop this far inside the keyline centre

# --- the density ramp of X: hard-core radius grows with distance from ONE
# crowd focus (sheet u, v-down), smoothstep over RAMP_R mm, so every card
# crosses from crowd (stamps fuse) to solitude (stamps stand alone)
FOCUS_UV = (0.40, 0.80)
RAMP_R = 150.0

# --- type -------------------------------------------------------------------
CAPTIONS = ["K1  gabor, bars at 30 deg, σ 9.6",
            "K2  gabor, bars at 120 deg, σ 9.6",
            "K3  gaussian blur, σ 3.6"]
KEY_COLS = (2, 9)   # key block = grid columns 2..9 ...
KEY_ROWS = (3, 6)   # ... and grid rows 3..6 below the laminate edge
KEY_ROWS_TEXT = [
    ("chip", "one impulse of X  (x = 1)"),
    ("loop", "line  K * X = 0.35"),
    ("solid", "solid K * X > 1.25 : only a sum"),
    (None, "(one impulse alone peaks at 1)"),
    ("grid", "grid 12 mm = λ of K1, K2"),
]


# ---------------------------------------------------------------------------
# kernels
# ---------------------------------------------------------------------------
def gabor(dx: np.ndarray, dy: np.ndarray, bar_deg: float) -> np.ndarray:
    """Gabor with bars running at ``bar_deg``: carrier along the bar normal."""
    a = math.radians(bar_deg + 90.0)
    t = dx * math.cos(a) + dy * math.sin(a)
    return np.exp(-(dx * dx + dy * dy) / (2 * SIG * SIG)) * np.cos(2 * math.pi * t / LAM)


def blur(dx: np.ndarray, dy: np.ndarray) -> np.ndarray:
    """Gaussian blur, peak 1 (the all-positive smoothing kernel)."""
    return np.exp(-(dx * dx + dy * dy) / (2 * BLUR_SIG * BLUR_SIG))


KERNELS = [
    # (name, pen, fn, support radius mm)
    ("K1", RED, lambda dx, dy: gabor(dx, dy, 30.0), 4.2 * SIG),
    ("K2", BLUE, lambda dx, dy: gabor(dx, dy, 120.0), 4.2 * SIG),
    ("K3", ORANGE, blur, 4.5 * BLUR_SIG),
]


def convolve(pts: np.ndarray, kern, support: float, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    """Exact Y = K * sum_i delta(p - p_i) on the grid (xs, ys)."""
    Y = np.zeros((len(ys), len(xs)))
    x0, y0 = xs[0], ys[0]
    for px, py in pts:
        i0 = max(0, int((px - support - x0) / GRID_H))
        i1 = min(len(xs), int((px + support - x0) / GRID_H) + 2)
        j0 = max(0, int((py - support - y0) / GRID_H))
        j1 = min(len(ys), int((py + support - y0) / GRID_H) + 2)
        if i0 >= i1 or j0 >= j1:
            continue
        DX = xs[i0:i1][None, :] - px
        DY = ys[j0:j1][:, None] - py
        Y[j0:j1, i0:i1] += kern(DX, DY)
    return Y


# ---------------------------------------------------------------------------
# X: the confetti
# ---------------------------------------------------------------------------
def scatter(rng: SeededRNG, box: Bounds, ramp, keep_out: Sequence[Region]) -> np.ndarray:
    """Random sequential adsorption with a spatially varying hard-core radius."""
    x0, y0, x1, y1 = box
    acc: List[Tuple[float, float, float]] = []
    A = np.zeros((0, 3))
    misses = 0
    while misses < 4000:
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if any(r.contains(px + ox, py + oy) for r in keep_out for ox, oy in _PAD):
            misses += 1
            continue
        rp = ramp(px, py)
        if len(A):
            d = np.hypot(A[:, 0] - px, A[:, 1] - py)
            if np.any(d < np.minimum(A[:, 2], rp)):
                misses += 1
                continue
        acc.append((px, py, rp))
        A = np.array(acc)
        misses = 0
    return A[:, :2] if len(A) else np.zeros((0, 2))


_PAD = [(0.0, 0.0)] + [(CHIP_HALO * math.cos(k * math.pi / 4), CHIP_HALO * math.sin(k * math.pi / 4))
                       for k in range(8)]


def chip(px: float, py: float) -> List[GCodeCommand]:
    """One confetti triangle, upright, filled as one nested-triangle stroke."""
    pts: Poly = []
    r = CHIP_R
    while r > 0.15:
        for k in range(3):
            a = math.pi / 2 + k * 2 * math.pi / 3
            pts.append((px + r * math.cos(a), py + r * math.sin(a)))
        a = math.pi / 2
        pts.append((px + r * math.cos(a), py + r * math.sin(a)))
        r -= 0.38
    return _poly(pts, color=BLACK, f=F)


# ---------------------------------------------------------------------------
# cards
# ---------------------------------------------------------------------------
def _conv_offset(pts: Poly, d: float) -> Poly:
    """Mitred offset of a convex CCW polygon by d (outward positive)."""
    n = len(pts)
    lines = []
    for i in range(n):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % n]
        ex, ey = bx - ax, by - ay
        L = math.hypot(ex, ey)
        nx, ny = ey / L, -ex / L  # outward for CCW
        lines.append((ax + nx * d, ay + ny * d, ex, ey))
    out = []
    for i in range(n):
        ax, ay, ex, ey = lines[i - 1]
        bx, by, fx, fy = lines[i]
        den = ex * fy - ey * fx
        t = ((bx - ax) * fy - (by - ay) * fx) / den
        out.append((ax + t * ex, ay + t * ey))
    return out


class Card:
    def __init__(self, kind: str, geo, kernel: int, caption: str = "", edge: int = 0):
        self.kind = kind
        if kind == "poly":
            a2 = sum(geo[i][0] * geo[(i + 1) % len(geo)][1] - geo[(i + 1) % len(geo)][0] * geo[i][1]
                     for i in range(len(geo)))
            if a2 < 0:  # normalise to CCW: offsets and captions assume it
                geo = list(reversed(geo))
        self.geo = geo  # disc: (cx, cy, r) ; poly: CCW vertex list
        self.kernel = kernel
        self.caption = caption
        self.edge = edge  # poly: caption runs inside this edge (a -> b, CCW index)

    CAP_H = 2.4
    CAP_IN = 2.6  # caption baseline band starts this far inside the keyline

    def caption_frame(self) -> Tuple[Pt, float, Poly]:
        """(baseline start, angle deg, knockout box) for the card's own label."""
        h = self.CAP_H
        w = _text_width(self.caption, h)
        if self.kind == "disc":
            cx, cy, r = self.geo
            y = cy + r - self.CAP_IN - h - 12.0
            x = cx - w / 2
            box = [(x - 1.2, y - 1.4), (x + w + 1.2, y - 1.4), (x + w + 1.2, y + h + 1.4),
                   (x - 1.2, y + h + 1.4)]
            return (x, y), 0.0, box
        n = len(self.geo)
        a, b = self.geo[self.edge], self.geo[(self.edge + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ex, ey)
        dx, dy = -ex / L, -ey / L  # reading direction: interior falls below the text
        nx, ny = -ey / L, ex / L  # inward normal of a CCW edge
        off = self.CAP_IN + h
        start = (b[0] + dx * 7.0 + nx * off, b[1] + dy * 7.0 + ny * off)
        ang = math.degrees(math.atan2(dy, dx))
        ux, uy = -nx, -ny  # glyph "up"
        p0 = (start[0] - dx * 1.2 - ux * 1.4, start[1] - dy * 1.2 - uy * 1.4)
        box = [p0, (p0[0] + dx * (w + 2.4), p0[1] + dy * (w + 2.4)),
               (p0[0] + dx * (w + 2.4) + ux * (h + 2.8), p0[1] + dy * (w + 2.4) + uy * (h + 2.8)),
               (p0[0] + ux * (h + 2.8), p0[1] + uy * (h + 2.8))]
        return start, ang, box

    def region(self, d: float = 0.0, shift: Pt = (0.0, 0.0)) -> Region:
        sx, sy = shift
        if self.kind == "disc":
            cx, cy, r = self.geo
            return Circle(cx + sx, cy + sy, r + d)
        pts = _conv_offset(self.geo, d) if d else list(self.geo)
        return Polygon([(x + sx, y + sy) for x, y in pts])

    def ring(self, d: float = 0.0, shift: Pt = (0.0, 0.0)) -> Poly:
        sx, sy = shift
        if self.kind == "disc":
            cx, cy, r = self.geo
            n = 360
            return [(cx + sx + (r + d) * math.cos(2 * math.pi * k / n),
                     cy + sy + (r + d) * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
        pts = _conv_offset(self.geo, d) if d else list(self.geo)
        pts = [(x + sx, y + sy) for x, y in pts]
        return pts + [pts[0]]

    def hide(self) -> Region:
        """What this card (plus its cast shadow) hides of everything behind it."""
        g = KEYLINE_W / 2 + 0.9
        return Union(self.region(g), self.region(g, SHADOW))


# ---------------------------------------------------------------------------
# clipping helpers
# ---------------------------------------------------------------------------
def _bbox(poly: Poly) -> Bounds:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs), min(ys), max(xs), max(ys)


def _chips_near(chips: np.ndarray, bb: Bounds, pad: float) -> List[Region]:
    x0, y0, x1, y1 = bb
    m = (chips[:, 0] > x0 - pad) & (chips[:, 0] < x1 + pad) & (chips[:, 1] > y0 - pad) & (
        chips[:, 1] < y1 + pad)
    return [Circle(float(x), float(y), CHIP_HALO) for x, y in chips[m]]


def _split(poly: Poly, maxlen: int = 400) -> List[Poly]:
    """Cut long polylines so chip-halo clipping stays local and fast."""
    if len(poly) <= maxlen:
        return [poly]
    out = []
    for k in range(0, len(poly) - 1, maxlen):
        out.append(poly[k:k + maxlen + 1])
    return out


def _clip_all(polys: Sequence[Poly], keep_in: Optional[Region], hide: Sequence[Region],
              chips: np.ndarray, min_len: float = 0.8) -> List[Poly]:
    runs: List[Poly] = []
    for poly in polys:
        pieces = [poly]
        if keep_in is not None:
            pieces = [q for p in pieces for q in clip(p, keep_in, keep="inside")]
        for h in hide:
            pieces = [q for p in pieces for q in clip(p, h, keep="outside")]
        fin: List[Poly] = []
        for p in pieces:
            for s in _split(p):
                halos = _chips_near(chips, _bbox(s), CHIP_HALO + 0.5)
                if halos:
                    fin += clip(s, Union(*halos), keep="outside")
                else:
                    fin.append(s)
        runs += [p for p in fin if _plen(p) >= min_len]
    return _join(runs)


def _plen(p: Poly) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))


def _join(runs: List[Poly], tol: float = 1e-6) -> List[Poly]:
    out: List[Poly] = []
    for r in runs:
        if out and math.hypot(out[-1][-1][0] - r[0][0], out[-1][-1][1] - r[0][1]) < tol:
            out[-1] = out[-1] + r[1:]
        else:
            out.append(list(r))
    return out


def _emit(polys: Sequence[Poly], pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        out += _poly(p, color=pen, f=F)
    return out


def _band(ring: Poly, width: float, passes: int) -> List[Poly]:
    """Keyline band: ``passes`` parallel copies of a closed ring across ``width``."""
    from promptplot.generative.engine.kit import _offset_polyline
    out = []
    for k in range(passes):
        d = -width / 2 + width * k / (passes - 1)
        out.append(_offset_polyline(ring, d))
    return out


def _hatch(region: Region, bb: Bounds, pitch: float, deg: float = 45.0) -> List[Poly]:
    x0, y0, x1, y1 = bb
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = math.hypot(x1 - x0, y1 - y0) / 2 + 1
    out = []
    k = -int(R / pitch)
    flip = False
    while k * pitch <= R:
        off = k * pitch
        p0 = (cx - R * ca - off * sa, cy - R * sa + off * ca)
        p1 = (cx + R * ca - off * sa, cy + R * sa + off * ca)
        seg = [p0, p1] if not flip else [p1, p0]
        out += clip(seg, region, keep="inside")
        flip = not flip
        k += 1
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------
def _sum_fill(Y: np.ndarray, xs: np.ndarray, ys: np.ndarray, deg: float,
              pitch: float, step: float = 0.1) -> List[Poly]:
    """Parallel runs at ``pitch`` covering exactly {Y > 0} of the solid field: each line is
    sampled on the evaluation grid (bilinear) and cut where it crosses the
    level, the crossing refined linearly so the runs end ON the outline."""
    mask = Y > 0.0
    if not mask.any():
        return []
    jj, ii = np.nonzero(mask)
    x0, x1 = xs[ii.min()] - 1, xs[ii.max()] + 1
    y0, y1 = ys[jj.min()] - 1, ys[jj.max()] + 1
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    R = math.hypot(x1 - x0, y1 - y0) / 2
    t = np.arange(-R, R + step, step)
    h = xs[1] - xs[0]

    def sample(px: np.ndarray, py: np.ndarray) -> np.ndarray:
        fx = (px - xs[0]) / h
        fy = (py - ys[0]) / h
        i = np.clip(np.floor(fx).astype(int), 0, len(xs) - 2)
        j = np.clip(np.floor(fy).astype(int), 0, len(ys) - 2)
        ax, ay = fx - i, fy - j
        return ((1 - ax) * (1 - ay) * Y[j, i] + ax * (1 - ay) * Y[j, i + 1]
                + (1 - ax) * ay * Y[j + 1, i] + ax * ay * Y[j + 1, i + 1])

    out: List[Poly] = []
    k = -int(R / pitch)
    flip = False
    while k * pitch <= R:
        ox, oy = cx + nx * k * pitch, cy + ny * k * pitch
        px, py = ox + ux * t, oy + uy * t
        v = sample(px, py)
        pos = v > 0
        edges = np.nonzero(np.diff(pos.astype(int)))[0]
        runs = []
        start = None
        if pos[0]:
            start = 0.0
        for e in edges:
            f = e + v[e] / (v[e] - v[e + 1])  # fractional index of the crossing
            if pos[e + 1]:
                start = f
            elif start is not None:
                runs.append((start, f))
                start = None
        for s0, s1 in runs:
            if (s1 - s0) * step < 0.3:
                continue
            p0 = (ox + ux * (t[0] + s0 * step), oy + uy * (t[0] + s0 * step))
            p1 = (ox + ux * (t[0] + s1 * step), oy + uy * (t[0] + s1 * step))
            out.append([p1, p0] if flip else [p0, p1])
        flip = not flip
        k += 1
    return out


def _rot_rect(cx: float, cy: float, w: float, h: float, deg: float) -> Poly:
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    out = []
    for lx, ly in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        out.append((cx + lx * ca - ly * sa, cy + lx * sa + ly * ca))
    return out  # CCW


def build(bounds: Bounds, rng: SeededRNG) -> Dict:
    bx0, by0, bx1, by1 = bounds
    W, H = bx1 - bx0, by1 - by0

    def U(u: float) -> float:
        return bx0 + u * W

    def V(v: float) -> float:  # v measured DOWN from the top
        return by1 - v * H

    cards = [
        Card("disc", (U(0.25), V(0.63), 0.42 * H), 0, CAPTIONS[0]),
        Card("poly", _rot_rect(U(0.49), V(0.63), 0.37 * H, 0.37 * H, 18.0), 2, CAPTIONS[2], edge=2),
        Card("poly", [(U(0.60), V(0.02)), (U(0.955), V(0.02)), (U(0.815), V(0.74))], 1,
             CAPTIONS[1], edge=1),
    ]  # back -> front
    # the grid laminate: bleeds off the right and bottom frame
    gx0, gy1 = U(0.58), V(0.62)
    ground = (gx0, by0, bx1, gy1)
    # the key is a block of whole grid cells knocked out of the laminate:
    # columns 2..9, rows 3..6 below the slab edge (open at the bottom frame)
    key_box = (gx0 + KEY_COLS[0] * LAM, gy1 - KEY_ROWS[1] * LAM,
               gx0 + KEY_COLS[1] * LAM, gy1 - KEY_ROWS[0] * LAM)
    title_box = (U(0.02), V(0.15), U(0.47), V(0.02))
    keep_out = [Polygon(_rect_pts((title_box[0], title_box[1], title_box[2], by1), 1.5)),
                Polygon(_rect_pts(key_box, 0.0))]
    keep_out += [Polygon(c.caption_frame()[2]) for c in cards]
    # confetti never lands ON a keyline: a chip there would chop the band
    # into dashes.  (X is still whatever the scatter produced; the maps are
    # computed from exactly these chips.)
    g = KEYLINE_W / 2 + 0.6
    keep_out += [Intersect(c.region(g), Complement(c.region(-g))) for c in cards]
    keep_out += [Polygon(_rect_pts((gx0, by0 - 5, gx0, gy1), g)),
                 Polygon(_rect_pts((gx0, gy1, bx1 + 5, gy1), g))]

    def ramp(x: float, y: float) -> float:
        s = math.hypot(x - U(FOCUS_UV[0]), y - V(FOCUS_UV[1])) / RAMP_R
        s = min(1.0, s)
        s = s * s * (3 - 2 * s)
        return R_DENSE + (R_SPARSE - R_DENSE) * s

    chips = scatter(rng, (bx0 + 2, by0 + 2, bx1 - 2, by1 - 2), ramp, keep_out)
    xs = np.arange(bx0 - 2, bx1 + 2.001, GRID_H)
    ys = np.arange(by0 - 2, by1 + 2.001, GRID_H)
    frame = Polygon(_rect_pts(bounds, -0.5))
    return dict(cards=cards, chips=chips, xs=xs, ys=ys, title_box=title_box,
                key_box=key_box, frame=frame, ground=ground, U=U, V=V, ramp=ramp)


def _grid_lines(ground: Bounds, key: Bounds) -> List[Poly]:
    """The laminate grid at pitch LAM; the key block's interior is knocked out
    and its border IS four grid lines, so every cut ends on a grid node."""
    gx0, gy0, gx1, gy1 = ground
    kx0, ky0, kx1, ky1 = key
    eps = 1e-6
    out: List[Poly] = []
    x = gx0 + LAM
    while x <= gx1 + eps:
        if kx0 + eps < x < kx1 - eps:
            out.append([(x, gy1), (x, ky1)])
            if ky0 > gy0 + eps:
                out.append([(x, ky0), (x, gy0)])
        else:
            out.append([(x, gy1), (x, gy0)])
        x += LAM
    y = gy1 - LAM
    while y >= gy0 - eps:
        if ky0 + eps < y < ky1 - eps:
            out.append([(gx0, y), (kx0, y)])
            if kx1 < gx1 - eps:
                out.append([(kx1, y), (gx1, y)])
        else:
            out.append([(gx0, y), (gx1, y)])
        y -= LAM
    return out


def convolutions_memphis(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    M = build(bounds, rng)
    cards: List[Card] = M["cards"]
    chips: np.ndarray = M["chips"]
    xs, ys = M["xs"], M["ys"]
    frame: Region = M["frame"]
    out: List[GCodeCommand] = []
    type_hide = [Polygon(_rect_pts(M["title_box"], 1.0)),
                 Polygon(_rect_pts(M["key_box"], -0.01))]
    type_hide += [Polygon(c.caption_frame()[2]) for c in cards]
    M["fields"] = {}
    M["lines"] = {}

    # --- feature maps on their cards ------------------------------------
    for depth, card in enumerate(cards):
        name, pen, kern, sup = KERNELS[card.kernel]
        Y = convolve(chips, kern, sup, xs, ys)
        M["fields"][name] = Y
        gen = contourpy.contour_generator(xs, ys, Y, name="serial")
        # the solid: Y > SUM_LEVEL, inset so its edge stays >= SOLID_INSET from
        # the Y = LEVEL line (first-order distance (Y - LEVEL) / |grad Y|):
        # without the inset the two lines ran 0.55 mm apart on steep bars
        gy, gx = np.gradient(Y, GRID_H)
        S = np.minimum(Y - SUM_LEVEL, (Y - LEVEL) / np.maximum(np.hypot(gx, gy), 1e-9) - SOLID_INSET)
        M["solid"] = M.get("solid", {})
        M["solid"][name] = S
        sgen = contourpy.contour_generator(xs, ys, S, name="serial")
        lines = [[(float(x), float(y)) for x, y in ln] for ln in gen.lines(LEVEL)]
        lines += [[(float(x), float(y)) for x, y in ln] for ln in sgen.lines(0.0)]
        front = [c.hide() for c in cards[depth + 1:]]
        keep = Intersect(card.region(-(KEYLINE_W / 2 + CARD_GAP)), frame)
        runs = _clip_all(lines, keep, front + type_hide, chips)
        M["lines"][name] = runs
        out += _emit(runs, pen)
        # where only a SUM can reach (Y > SUM_LEVEL) the squiggle goes solid:
        # a fill along the kernel's own bar direction at FILL_PITCH
        fill = _sum_fill(S, xs, ys, FILL_DEG[name], FILL_PITCH)
        fill = _clip_all(fill, keep, front + type_hide, chips, min_len=0.4)
        M["fills"] = M.get("fills", {})
        M["fills"][name] = fill
        out += _emit(fill, pen)

    # --- card keylines + cast shadows (black) ------------------------------
    for depth, card in enumerate(cards):
        front = [c.hide() for c in cards[depth + 1:]]
        band = _band(card.ring(), KEYLINE_W, 4)
        out += _emit(_clip_all(band, frame, front + type_hide, chips), BLACK)
        sh_reg = card.region(0.0, SHADOW)
        bb = _bbox(card.ring(0.0, SHADOW))
        hat = _hatch(sh_reg, bb, HATCH)
        hide = [card.region(KEYLINE_W / 2 + 0.5)] + front + type_hide
        out += _emit(_clip_all(hat, frame, hide, chips), BLACK)

    # --- ground grid, pitch LAM, only on bare ground ----------------------
    card_hide = [c.hide() for c in cards]
    grid = _grid_lines(M["ground"], M["key_box"])
    out += _emit(_clip_all(grid, frame, card_hide + type_hide[:1] + type_hide[2:], chips), BLACK)
    gx0, gy0, gx1, gy1 = M["ground"]
    edge = [(gx0, gy0 - 5.0), (gx0, gy1), (gx1 + 5.0, gy1)]
    band = _band(edge, KEYLINE_W, 4)
    out += _emit(_clip_all(band, frame, card_hide + type_hide, chips), BLACK)

    # --- X: confetti, on top of everything ---------------------------------
    for px, py in chips:
        out += chip(float(px), float(py))

    # --- type ---------------------------------------------------------------
    out += _type(M)
    return _sequence(out, tail=M["key_box"])


def _strokes(cmds: Sequence[GCodeCommand]) -> List[Tuple[int, Poly]]:
    """Split a command list back into (pen, polyline) strokes."""
    res: List[Tuple[int, Poly]] = []
    start: Optional[Pt] = None
    cur: Optional[Poly] = None
    pen = 0
    for c in cmds:
        if c.command == "G0":
            start = (c.x, c.y)
        elif c.command == "M3":
            pen = c.color if c.color is not None else 0
            cur = [start]
        elif c.command == "G1" and cur is not None:
            cur.append((c.x, c.y))
        elif c.command == "M5" and cur is not None:
            if len(cur) > 1:
                res.append((pen, cur))
            cur = None
    return res


def _greedy(polys: List[Poly], pos: np.ndarray) -> List[Poly]:
    """Chain strokes nearest-end-first from ``pos``; a stroke may run backwards."""
    if not polys:
        return []
    S = np.array([p[0] for p in polys])
    E = np.array([p[-1] for p in polys])
    left = np.ones(len(polys), bool)
    order: List[Poly] = []
    for _ in range(len(polys)):
        ds = np.hypot(*(S - pos).T)
        de = np.hypot(*(E - pos).T)
        ds[~left] = np.inf
        de[~left] = np.inf
        i, j = int(np.argmin(ds)), int(np.argmin(de))
        if ds[i] <= de[j]:
            p = polys[i]
            left[i] = False
        else:
            p = list(reversed(polys[j]))
            left[j] = False
        order.append(p)
        pos = np.array(p[-1])
    return order


def _sequence(cmds: Sequence[GCodeCommand], tail: Optional[Bounds] = None) -> List[GCodeCommand]:
    """Pen layers in palette order (light -> dark, black last).  Inside a layer
    the strokes are chained greedily nearest-end-first and then 2-opted, so
    consecutive strokes are neighbours and every stroke end is a clean batch
    boundary.  Strokes that start inside ``tail`` (the key) are drawn LAST in
    their layer, so a legend swatch never sits mid-chain."""
    by_pen: Dict[int, Tuple[List[Poly], List[Poly]]] = {}
    for pen, pts in _strokes(cmds):
        body, key = by_pen.setdefault(pen, ([], []))
        x, y = pts[0]
        if tail is not None and tail[0] <= x <= tail[2] and tail[1] <= y <= tail[3]:
            key.append(pts)
        else:
            body.append(pts)
    out: List[GCodeCommand] = []
    pos = np.array([0.0, 0.0])
    for pen in sorted(by_pen):
        body, key = by_pen[pen]
        if key:
            # chain the body backwards from the key, so the body ENDS beside it
            kc = np.array([(tail[0] + tail[2]) / 2, (tail[1] + tail[3]) / 2])
            order = [list(reversed(p)) for p in reversed(_greedy(body, kc))]
            order = _two_opt(order, fixed_end=True)
        else:
            order = _two_opt(_greedy(body, pos))
        if order:
            pos = np.array(order[-1][-1])
        order += _greedy(key, pos)
        for p in order:
            out += _poly(p, color=pen, f=F)
        pos = np.array(order[-1][-1])
    return out


def _two_opt(seq: List[Poly], passes: int = 30, fixed_end: bool = False) -> List[Poly]:
    """2-opt on the travel between strokes: reversing a run of strokes also
    flips each stroke, so only the two boundary travels change."""
    seq = list(seq)
    n = len(seq)
    if n < 4:
        return seq
    for _ in range(passes):
        S = np.array([p[0] for p in seq])
        E = np.array([p[-1] for p in seq])
        improved = False
        for i in range(1, n - 1):
            # reverse seq[i..j]: travel E[i-1]->S[i] and E[j]->S[j+1] become
            # E[i-1]->E[j] and S[i]->S[j+1]
            j = np.arange(i + 1, n - 1 if fixed_end else n)
            if len(j) == 0:
                continue
            a = np.hypot(*(E[i - 1] - S[i]))
            has = j + 1 < n  # the stroke after the reversed run, if any
            nxt = S[np.minimum(j + 1, n - 1)]
            b = np.where(has, np.hypot(*(E[j] - nxt).T), 0.0)
            c = np.hypot(*(E[i - 1] - E[j]).T)
            d = np.where(has, np.hypot(*(S[i] - nxt).T), 0.0)
            gain = (a + b) - (c + d)
            k = int(np.argmax(gain))
            if gain[k] > 1e-6:
                jj = int(j[k])
                seq[i:jj + 1] = [list(reversed(p)) for p in reversed(seq[i:jj + 1])]
                S[i:jj + 1] = np.array([p[0] for p in seq[i:jj + 1]])
                E[i:jj + 1] = np.array([p[-1] for p in seq[i:jj + 1]])
                improved = True
        if not improved:
            break
    return seq


def _rect_pts(b: Bounds, pad: float) -> Poly:
    x0, y0, x1, y1 = b
    return [(x0 - pad, y0 - pad), (x1 + pad, y0 - pad), (x1 + pad, y1 + pad), (x0 - pad, y1 + pad)]


def _ink_box(ch: str) -> Tuple[float, float]:
    from promptplot.generative.generators import _GLYPHS

    xs = [pt[0] for stroke in _GLYPHS[ch] for pt in stroke] or [0.0, 2.0]
    return min(xs), max(xs)


def _fat_glyph(ch: str, x: float, y: float, h: float, weight: float, tip: float) -> List[GCodeCommand]:
    """One glyph, every straight SEGMENT thickened on its own as a serpentine band.

    Offsetting a whole glyph stroke along averaged normals pinches the band at
    sharp corners, which is why the N and V diagonals came out as hairlines next
    to fat stems (r03/r04 A12).  Per-segment bands have the same width at any
    angle."""
    from promptplot.generative.generators import _GLYPHS

    sc = h / 6.0
    n = max(2, int(round(weight / tip)) + 1)
    out: List[GCodeCommand] = []
    for stroke in _GLYPHS[ch]:
        pts = [(x + gx * sc, y + gy * sc) for gx, gy in stroke]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            L = math.hypot(bx - ax, by - ay)
            if L < 1e-6:
                continue
            nx, ny = -(by - ay) / L, (bx - ax) / L
            ux, uy = (bx - ax) / L, (by - ay) / L
            e = weight / 2  # square caps: extend so corners close
            band: Poly = []
            for k in range(n):
                d = -weight / 2 + weight * k / (n - 1)
                p0 = (ax - ux * e + nx * d, ay - uy * e + ny * d)
                p1 = (bx + ux * e + nx * d, by + uy * e + ny * d)
                band += [p0, p1] if k % 2 == 0 else [p1, p0]
            out += _poly(band, color=BLACK, f=F)
    return out


def _title(text: str, x: float, y: float, h: float, weight: float) -> Tuple[List[GCodeCommand], float]:
    """Display type set on each glyph's INK box (even optical spacing)."""
    sc = h / 6.0
    bearing = 1.6
    cmds: List[GCodeCommand] = []
    cx = x
    for ch in text:
        a, b = _ink_box(ch)
        if weight > 0:
            cmds += _fat_glyph(ch, cx - a * sc, y, h, weight, 0.3)
        cx += (b - a + bearing) * sc
    return cmds, cx - x - bearing * sc


def _type(M: Dict) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    tx0, ty0, tx1, ty1 = M["title_box"]
    # size the title to the title box width
    _, w1 = _title("CONVOLUTIONS", 0, 0, 1.0, 0.0)
    h = min(13.0, (tx1 - tx0) / w1)
    cmds, _ = _title("CONVOLUTIONS", tx0, ty1 - h, h, 1.2)
    out += cmds
    out += _stroke_text("every squiggle is a sum", tx0, ty0 + 0.5, 4.0, color=BLACK)
    # --- the key: rows every LAM/2 inside the knocked-out grid block -------
    kx0, ky0, kx1, ky1 = M["key_box"]
    th = 2.4
    tx = kx0 + LAM  # text column starts on the next grid line
    ix = kx0 + LAM / 2  # icon column centred in the first cell
    icons: List[GCodeCommand] = []
    for r, (icon, text) in enumerate(KEY_ROWS_TEXT):
        y = ky1 - LAM / 2 * (r + 1)
        out += _stroke_text(text, tx, y, th, color=BLACK)
        cy = y + th / 2
        if icon == "chip":
            icons += chip(ix, cy)
        elif icon in ("loop", "solid"):  # an outline stamp, or a solid one
            ring = [(ix + 3.6 * math.cos(2 * math.pi * t / 48),
                     cy + 1.6 * math.sin(2 * math.pi * t / 48)) for t in range(49)]
            icons += _poly(ring, color=BLACK, f=F)
            if icon == "solid":
                for yy in np.arange(-1.2, 1.21, 0.8):
                    xx = 3.6 * math.sqrt(max(0.0, 1 - (yy / 1.6) ** 2))
                    icons += _poly([(ix - xx, cy + yy), (ix + xx, cy + yy)], color=BLACK, f=F)
        elif icon == "grid":
            g = [[(ix - 2.5, cy - 3.0), (ix - 2.5, cy + 3.0)], [(ix + 2.5, cy - 3.0), (ix + 2.5, cy + 3.0)],
                 [(ix - 3.5, cy - 1.5), (ix + 3.5, cy - 1.5)], [(ix - 3.5, cy + 1.5), (ix + 3.5, cy + 1.5)]]
            icons += _emit(g, BLACK)
    for card in M["cards"]:
        (x, y), ang, _ = card.caption_frame()
        out += giant_type(card.caption, x, y, card.CAP_H, pen=BLACK, angle=ang)
    return icons + out
