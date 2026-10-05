"""CONVOLUTIONS — r02 · real-kernel (mechanism) · parent r01.

Same plate as r01 — same layout, same spine, same gutters, same measured type —
but NOTHING on it is decoration any more.  Every ring, disc and contour is a
real computed array:

* **X** — the input field.  A trefoil outline; X(p) = distance to the boundary
  (|grad X| = 1, so the drawn rings are its level sets at exactly one pitch)
  plus a bounded fbm wobble.  The network SAMPLES X on a 1.5 mm pixel lattice.
* **The strip** — five real 5x5 kernels, a five-layer stack
  ``Y = relu(K5 * relu(K4 * relu(K3 * relu(K2 * relu(K1 * X)))))``:
  blur (Gaussian, sigma 1 px) · ridge (negated Laplacian-of-Gaussian) · blur ·
  ridge · blur (sigma 1.3 px).  Each tile draws its kernel as signed Ben-Day
  discs: disc AREA = |w| / max|w|, crimson = positive tap, blue = negative tap.
* **Y** — the output of that stack on that X, drawn at the SAME scale on the same
  lattice, translated to the right.  A ridge detector on a distance field fires
  on the medial axis, and the medial axis of a trefoil whose lobes point
  up-left, up-right and down is the letter Y.  The output IS its own label.
* **Feature maps** — the single-layer pre-activations ``K_i * X`` of three bank
  kernels (Sobel-x edge, Gaussian blur, 0-degree Gabor) on the same X; crimson
  contours are positive response, blue dashed contours negative.
* **Kernel bank** — the nine 5x5 kernels the strip and the maps are drawn from
  (edge / blur / Gabor rows), same Ben-Day encoding; the three used by the maps
  carry a double keyline.
* **Receptive field** — the stack's own receptive field against depth: the
  dashed TRIANGLE is the theoretical field (+-2 px per 5x5 layer, 21 px after
  five), the solid nest is the effective field — contours of the Gaussian whose
  variance is the exact sum of the five |K| variances — and the dot rows are
  the exact composite |K5 * ... * K1| marginal at each layer (Ben-Day area).

Every overlap that remains is one of r01's two defended cases (connectors pass
behind the tiles; the kernel window knocks the X rings out).

Pens (``colors=4``): 0 black = X, type, keylines · 1 crimson = positive weight /
positive response · 2 blue = negative weight / negative response · 3 olive =
activation after sigma (Y, the links between layers, the output fan).

Entry point: ``convolutions_real_kernel``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, Region, Union, clip
from promptplot.generative.engine.kit import circle
from promptplot.generative.engine.policies import enforce_line_spacing
from promptplot.generative.engine.scene3d import Occupancy
from promptplot.generative.generators import (
    _chain_segments,
    _glyph_advance,
    _poly,
    _stroke_text,
    _text_width,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, RED, BLUE, OLIVE = 0, 1, 2, 3
POS, NEG, ACT = RED, BLUE, OLIVE

F_DRAW = 2200
MIN_PITCH = 0.85  # mm — plotting floor; no ring family may go under this


# ===========================================================================
# measured layout  (normalised sheet coords; v = 0 TOP) — inherited from r01,
# where every number was measured off the reference raster.
# ===========================================================================
FRAME_INSET = 3.0  # mm inside the drawable area

# --- header -------------------------------------------------------------
TITLE_CAP = 3.0
TITLE_W = 47.0
TITLE_V = 0.010  # cap TOP
RULE_V = 0.048
SUB_CAP = 2.5
SUB_V = (0.070, 0.0922, 0.1144)
SUB_W = 46.0
UR_CAP = 1.85
UR_V = (0.010, 0.0265, 0.043, 0.0595)
UR_RULE_V = 0.082
UR_W = 22.0

CELL_GAP = 3.2  # inside the kernel bank AND the feature-map strip

# --- flow band ----------------------------------------------------------
# X and Y share one box height: Y is X's output on the SAME lattice, so it is
# drawn at the same scale and the same height, only translated.
BX_U = (0.000, 0.168)
BX_V = (0.170, 0.470)
BY_U = (0.832, 1.000)
BY_V = BX_V

TILE_W = 18.5
TILE_H = 22.5
TILE_GAP = 8.0
N_TILES = 5
STRIP_CU = 0.500
TILE_TOP_V = 0.303

GUTTER_V = (0.538, 0.615)

# --- lower band ---------------------------------------------------------
BASE_V = 0.925
CAP_BASE_V = 0.9605
LOWER_TOP_V = 0.615

ZONE_CELL_W = 20.0
KB_CELL_H = 16.87
FM_CELL_H = 22.6
CONE_HALF = 33.0

# --- the network --------------------------------------------------------
PIXEL = 1.5  # mm per input pixel on the sheet
FINE = 0.375  # mm field grid;  PIXEL / FINE = 4 = the tap dilation on that grid
PAD = 17.0  # mm of zero padding around X: > the stack's 10 px half-field
TAPS = np.arange(-2, 3)


# ===========================================================================
# frame mapping
# ===========================================================================
class Frame:
    def __init__(self, bounds: Bounds, inset: float = FRAME_INSET):
        x0, y0, x1, y1 = bounds
        self.x0, self.y0 = x0 + inset, y0 + inset
        self.x1, self.y1 = x1 - inset, y1 - inset
        self.w = self.x1 - self.x0
        self.h = self.y1 - self.y0

    def u(self, u: float) -> float:
        return self.x0 + u * self.w

    def v(self, v: float) -> float:
        return self.y1 - v * self.h

    def p(self, u: float, v: float) -> Pt:
        return (self.u(u), self.v(v))


# ===========================================================================
# type
# ===========================================================================
def _tracked(
    text: str,
    x: float,
    baseline: float,
    cap: float,
    pen: Optional[int],
    target_w: Optional[float] = None,
    f: int = 2300,
) -> Tuple[List[GCodeCommand], float]:
    """Proportional stroke type with uniform letter-tracking to hit ``target_w``.

    Cap height stays at the MEASURED value and the extra width is spent on
    tracking, instead of scaling the glyphs up (which is how recreation labels
    end up 30% oversized)."""
    sc = cap / 6.0
    nat = _text_width(text, cap, proportional=True)
    extra = 0.0
    if target_w is not None and len(text) > 1:
        extra = (target_w - nat) / (len(text) - 1)
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        out += _stroke_text(ch, cx, baseline, cap, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * sc + extra
    return out, (cx - extra - x) if len(text) > 1 else nat


def _tracked_w(text: str, cap: float, target_w: Optional[float]) -> float:
    if target_w is not None:
        return target_w
    return _text_width(text, cap, proportional=True)


def _text_at(
    text: str,
    baseline: float,
    cap: float,
    pen: Optional[int],
    left: Optional[float] = None,
    centre: Optional[float] = None,
    right: Optional[float] = None,
    target_w: Optional[float] = None,
) -> List[GCodeCommand]:
    w = _tracked_w(text, cap, target_w)
    if left is not None:
        x = left
    elif centre is not None:
        x = centre - w / 2.0
    else:
        x = (right or 0.0) - w
    return _tracked(text, x, baseline, cap, pen, target_w)[0]


# ===========================================================================
# contouring — numpy-prefiltered marching squares, chained with the house
# `_chain_segments`.  Only cells the level actually crosses are visited, which
# is what makes four render rounds affordable.
# ===========================================================================
_MS_TABLE = {
    1: ((3, 0),),
    2: ((0, 1),),
    3: ((3, 1),),
    4: ((1, 2),),
    5: ((3, 2), (0, 1)),
    6: ((0, 2),),
    7: ((3, 2),),
    8: ((2, 3),),
    9: ((0, 2),),
    10: ((0, 3), (1, 2)),
    11: ((1, 2),),
    12: ((1, 3),),
    13: ((0, 1),),
    14: ((0, 3),),
}


def _iso_chains(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, iso: float) -> List[Poly]:
    """Iso-contour of F[j, i] (j indexes ys) as chained polylines."""
    v0 = F[:-1, :-1]
    v1 = F[:-1, 1:]
    v2 = F[1:, 1:]
    v3 = F[1:, :-1]
    case = (
        (v0 > iso).astype(np.uint8)
        | ((v1 > iso).astype(np.uint8) << 1)
        | ((v2 > iso).astype(np.uint8) << 2)
        | ((v3 > iso).astype(np.uint8) << 3)
    )
    jj, ii = np.nonzero((case != 0) & (case != 15))
    if len(jj) == 0:
        return []
    segs = []
    for j, i in zip(jj.tolist(), ii.tolist()):
        xa, xb = float(xs[i]), float(xs[i + 1])
        ya, yb = float(ys[j]), float(ys[j + 1])
        a, b, c, d = float(v0[j, i]), float(v1[j, i]), float(v2[j, i]), float(v3[j, i])

        def lerp(pa, pb, va, vb):
            t = (iso - va) / (vb - va) if vb != va else 0.5
            return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))

        e = (
            lerp((xa, ya), (xb, ya), a, b),
            lerp((xb, ya), (xb, yb), b, c),
            lerp((xb, yb), (xa, yb), c, d),
            lerp((xa, yb), (xa, ya), d, a),
        )
        for p, q in _MS_TABLE[int(case[j, i])]:
            segs.append((e[p], e[q]))
    return [list(ch) for ch in _chain_segments(segs)]


# ===========================================================================
# outlines + distance fields
# ===========================================================================
def _amoeba(harmonics: Sequence[Tuple[int, float, float]], n: int = 300) -> Poly:
    """Closed radial blob r(theta) = 1 + sum a_k cos(k theta + phi_k), unit scale.

    A DOMINANT k = 3 term is the whole trick.  A near-convex blob's distance
    field has one long medial ridge, so its rings come out as a plain onion;
    a trefoil with waists deep enough to pinch (a_3 ~ 0.46) has a Y-shaped
    medial axis, and the rings split into the reference's three fingerprint
    eyes.  The smaller harmonics only break the symmetry.
    """
    pts: Poly = []
    for k in range(n):
        t = 2 * math.pi * k / n
        r = 1.0
        for kk, a, ph in harmonics:
            r += a * math.cos(kk * t + ph)
        pts.append((r * math.cos(t), r * math.sin(t)))
    return pts


def _fit_poly(poly: Poly, box: Bounds) -> Poly:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    x0, y0, x1, y1 = box
    sx = (x1 - x0) / (max(xs) - min(xs))
    sy = (y1 - y0) / (max(ys) - min(ys))
    return [(x0 + (p[0] - min(xs)) * sx, y0 + (p[1] - min(ys)) * sy) for p in poly]


def _dist_field(poly: Poly, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Distance to the boundary, positive INSIDE, 0 outside. |grad| = 1 inside."""
    P = np.asarray(poly, float)
    A = P
    B = np.roll(P, -1, axis=0)
    d = np.full(X.shape, 1e9)
    inside = np.zeros(X.shape, bool)
    for (ax, ay), (bx, by) in zip(A, B):
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        if L2 > 1e-12:
            t = np.clip(((X - ax) * vx + (Y - ay) * vy) / L2, 0.0, 1.0)
            d = np.minimum(d, np.hypot(X - (ax + t * vx), Y - (ay + t * vy)))
        if (ay > Y).any() or (by > Y).any():
            cond = (ay > Y) != (by > Y)
            if cond.any():
                xint = np.where(
                    abs(by - ay) > 1e-12, ax + (Y - ay) * vx / (by - ay + 1e-30), ax
                )
                inside ^= cond & (X < xint)
    return np.where(inside, d, 0.0)


def _grid(box: Bounds, step: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    x0, y0, x1, y1 = box
    xs = np.arange(x0, x1 + step, step)
    ys = np.arange(y0, y1 + step, step)
    X, Y = np.meshgrid(xs, ys)
    return xs, ys, X, Y


def _cone_levels(peak: float, sigma: float, pitch: float, n: int, base: float = 0.0):
    """Level ladder for a CONICAL field that gives a uniform RADIAL pitch.

    For ``F = a exp(-r/sigma)`` the ring at level ``F_k`` sits at
    ``r_k = sigma ln(a/F_k)``, so a ladder of UNIFORM LEVEL STEPS puts the
    radii at ``sigma ln((k+1)/k)`` apart — 0.69*sigma for the first gap and
    ``sigma/k`` near the summit.  At 16 levels on a sigma = 5.4 mm cusp the
    innermost gap is 0.33 mm, well under the 0.85 mm plotting floor, and the
    eye floods.  A GEOMETRIC ladder, ``F_k = a exp(-k pitch / sigma)``, puts
    the rings at exactly ``pitch`` apart everywhere, which is the whole reason
    the field is conical in the first place.
    """
    return [base + peak * math.exp(-k * pitch / sigma) for k in range(1, n + 1)]


def _cusps(X: np.ndarray, Y: np.ndarray, cusps: Sequence[Tuple[float, float, float, float]]):
    """sum a * exp(-r/sigma) — CONICAL, so uniform levels give uniform ring pitch."""
    F = np.zeros(X.shape)
    for cx, cy, sig, amp in cusps:
        F += amp * np.exp(-np.hypot(X - cx, Y - cy) / sig)
    return F


def _fbm_grid(rng: SeededRNG, X: np.ndarray, Y: np.ndarray, scale: float, oct_: int = 3):
    Z = np.zeros(X.shape)
    amp, frq = 1.0, 1.0
    norm = 0.0
    for _ in range(oct_):
        ox, oy = rng.uniform(-40, 40), rng.uniform(-40, 40)
        Z += amp * _value_noise(X * scale * frq + ox, Y * scale * frq + oy)
        norm += amp
        amp *= 0.5
        frq *= 2.0
    return Z / norm


def _value_noise(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    i0, j0 = np.floor(U).astype(int), np.floor(V).astype(int)
    fu, fv = U - i0, V - j0
    su = fu * fu * (3 - 2 * fu)
    sv = fv * fv * (3 - 2 * fv)

    def h(a, b):
        n = (a * 374761393 + b * 668265263) & 0xFFFFFFFF
        n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFFFF) / 0xFFFFFF

    a00, a10 = h(i0, j0), h(i0 + 1, j0)
    a01, a11 = h(i0, j0 + 1), h(i0 + 1, j0 + 1)
    return (a00 * (1 - su) + a10 * su) * (1 - sv) + (a01 * (1 - su) + a11 * su) * sv


# ===========================================================================
# stroke helpers
# ===========================================================================
def _dash(poly: Poly, on: float = 2.2, off: float = 1.9, phase: float = 0.0) -> List[Poly]:
    """Split a polyline into dashes of ``on`` mm separated by ``off`` mm.

    The phase is carried as an explicit on/off state with a remaining length,
    never as ``arclength % period``: the modulo form lands epsilon below the
    switch point once float error accumulates, the step collapses to ~1e-16 and
    the walk never terminates.
    """
    out: List[Poly] = []
    cur: Poly = []
    period = on + off
    s = phase % period if period > 0 else 0.0
    drawing = s < on
    rem = (on - s) if drawing else (period - s)
    for p, q in zip(poly, poly[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        seg = math.hypot(dx, dy)
        if seg < 1e-12:
            continue
        t = 0.0
        while t < seg - 1e-12:
            step = min(rem, seg - t)
            if drawing:
                a = (p[0] + dx * t / seg, p[1] + dy * t / seg)
                t2 = t + step
                b = (p[0] + dx * t2 / seg, p[1] + dy * t2 / seg)
                if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
                    cur.append(b)
                else:
                    if len(cur) >= 2:
                        out.append(cur)
                    cur = [a, b]
            else:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
            t += step
            rem -= step
            if rem <= 1e-12:
                drawing = not drawing
                rem = on if drawing else off
    if len(cur) >= 2:
        out.append(cur)
    return out


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 64) -> Poly:
    out: Poly = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        out.append(
            (
                m**3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t**3 * p3[0],
                m**3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t**3 * p3[1],
            )
        )
    return out


def _ellipse(cx: float, cy: float, rx: float, ry: float, rot: float = 0.0, n: int = 220) -> Poly:
    ca, sa = math.cos(rot), math.sin(rot)
    out: Poly = []
    for k in range(n + 1):
        t = 2 * math.pi * k / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        out.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return out


def _emit(polys: Sequence[Poly], pen: Optional[int], f: int = F_DRAW) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        if len(p) >= 2:
            out += _poly(p, color=pen, f=f)
    return out


def _guard_spacing(cmds: List[GCodeCommand], min_dist: float = 0.80) -> List[GCodeCommand]:
    """``enforce_line_spacing`` + re-emit, so every stroke keeps a leading G0.

    The policy rebuilds strokes and can drop the ``G0`` that positions one; the
    merged program then starts that stroke from the machine origin, which shows
    up as a stray point at (0, 0) and a bounds violation.  Re-emitting from the
    thinned runs is cheap and makes the guard safe to use anywhere.
    """
    thinned = enforce_line_spacing(cmds, min_dist=min_dist, resample=0.40)
    runs: List[Poly] = []
    cur: Poly = []
    pen: Optional[int] = None
    for c in thinned:
        if c.command == "G0" and c.x is not None:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [(c.x, c.y)]
        elif c.command == "M3":
            pen = c.color if c.color is not None else pen
        elif c.command == "G1" and c.x is not None:
            cur.append((c.x, c.y))
            if c.color is not None:
                pen = c.color
        elif c.command == "M5":
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return _emit(runs, pen)


def _clip_out(polys: Sequence[Poly], region: Region) -> List[Poly]:
    out: List[Poly] = []
    for p in polys:
        out.extend(clip(p, region, keep="outside"))
    return out


def _clip_in(polys: Sequence[Poly], box: Bounds) -> List[Poly]:
    """Keep the parts of each polyline INSIDE an axis-aligned box.

    A dedicated Liang-Barsky clip rather than ``geometry.clip``: the tiles,
    kernel cells and feature maps between them clip a few thousand contour
    chains, and the general Region machinery costs four half-plane calls per
    segment. ``geometry.clip`` is still used where the region is not a plain
    box (the strip knockout) and exactness at the boundary matters.
    """
    x0, y0, x1, y1 = box
    out: List[Poly] = []
    for poly in polys:
        cur: Poly = []
        for p, q in zip(poly, poly[1:]):
            t0, t1 = 0.0, 1.0
            dx, dy = q[0] - p[0], q[1] - p[1]
            ok = True
            for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
                if pp == 0.0:
                    if qq < 0.0:
                        ok = False
                        break
                    continue
                r = qq / pp
                if pp < 0.0:
                    if r > t1:
                        ok = False
                        break
                    if r > t0:
                        t0 = r
                else:
                    if r < t0:
                        ok = False
                        break
                    if r < t1:
                        t1 = r
            if not ok:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
                continue
            a = (p[0] + dx * t0, p[1] + dy * t0)
            b = (p[0] + dx * t1, p[1] + dy * t1)
            if cur and abs(cur[-1][0] - a[0]) < 1e-9 and abs(cur[-1][1] - a[1]) < 1e-9:
                cur.append(b)
            else:
                if len(cur) >= 2:
                    out.append(cur)
                cur = [a, b]
            if t1 < 1.0 - 1e-12:
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
        if len(cur) >= 2:
            out.append(cur)
    return out


def _rect(x0: float, y0: float, x1: float, y1: float) -> Poly:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def _disc(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Solid dot as a tight spiral — small enough that a spiral cannot flood."""
    turns = max(3, int(r / 0.20))
    n = turns * 22
    pts = [
        (
            x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            y + r * (k / n) * math.sin(2 * math.pi * turns * k / n),
        )
        for k in range(n + 1)
    ]
    pts.append((x + r, y))
    return _poly(pts, color=pen, f=1600) + circle(x, y, r, pen=pen, f=1600, n=26)


def _label_slot(
    outline: Poly, box: Bounds, side: int, cap: float, w: float, clear: float = 3.0
) -> Tuple[float, float]:
    """Find a baseline for a display label beside a blob, with real clearance.

    Scans candidate heights over the blob's middle third and returns the one
    where the gap between the blob's silhouette and the box edge is largest,
    so the label always lands on paper.
    """
    x0, y0, x1, y1 = box
    best = None
    for k in range(24):
        v = 0.20 + 0.60 * k / 23.0
        py = y1 - v * (y1 - y0)
        band = [p[0] for p in outline if abs(p[1] - py) < cap * 0.75]
        if not band:
            continue
        gap = (min(band) - x0) if side < 0 else (x1 - max(band))
        if best is None or gap > best[0]:
            best = (gap, py, min(band) if side < 0 else max(band))
    if best is None:
        return (x0, (y0 + y1) / 2.0)
    gap, py, edge = best
    lx = (edge - w - clear) if side < 0 else (edge + clear)
    lx = min(max(lx, x0 - w - clear - 1.0), x1 + clear + 1.0)
    return (lx, py - cap * 0.5)


def _pt_in_poly(px: float, py: float, poly: Poly) -> bool:
    inside = False
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        if (ay > py) != (by > py):
            if px < ax + (py - ay) * (bx - ax) / (by - ay + 1e-30):
                inside = not inside
    return inside



# ===========================================================================
# THE NETWORK — real kernels, real correlation, real ReLU
# ===========================================================================
_GX, _GY = np.meshgrid(TAPS, TAPS)  # tap offsets in pixels; row index = y


def k_gauss(s: float) -> np.ndarray:
    """Gaussian blur, 5x5, normalised to sum 1 (an averaging kernel)."""
    k = np.exp(-(_GX**2 + _GY**2) / (2.0 * s * s))
    return k / k.sum()


def k_ridge(s: float) -> np.ndarray:
    """Negated Laplacian-of-Gaussian, 5x5, made exactly zero-sum.

    Centre positive, surround negative: it annihilates any linear ramp, so on
    a distance field (a ramp almost everywhere) it answers only where the
    field bends — positive on the medial ridge, negative on the outline kink.
    """
    r2 = _GX**2 + _GY**2
    k = -(r2 - 2.0 * s * s) / s**4 * np.exp(-r2 / (2.0 * s * s))
    k = k - k.mean()
    return k / np.abs(k).max()


def k_sobel_x() -> np.ndarray:
    """5x5 Sobel: binomial smoothing across, central difference along x."""
    return np.outer([1, 4, 6, 4, 1], [-1, -2, 0, 2, 1]) / 96.0


def k_sobel_y() -> np.ndarray:
    return k_sobel_x().T.copy()


def k_gabor(theta: float, lam: float = 3.2, s: float = 1.1, gam: float = 0.6) -> np.ndarray:
    """Even (cosine) Gabor, zero-mean.  ``theta`` = direction of the carrier,
    so theta = 0 has vertical stripes and detects VERTICAL ridges."""
    xr = _GX * math.cos(theta) + _GY * math.sin(theta)
    yr = -_GX * math.sin(theta) + _GY * math.cos(theta)
    k = np.exp(-(xr**2 + (gam * yr) ** 2) / (2.0 * s * s)) * np.cos(2.0 * math.pi * xr / lam)
    k = k - k.mean()
    return k / np.abs(k).max()


# the bank, row-major: edge / blur / Gabor
BANK: List[Tuple[str, np.ndarray]] = [
    ("sobel x", k_sobel_x()),
    ("sobel y", k_sobel_y()),
    ("ridge", k_ridge(1.0)),
    ("blur .7", k_gauss(0.7)),
    ("blur 1", k_gauss(1.0)),
    ("blur 1.3", k_gauss(1.3)),
    ("gabor 0", k_gabor(0.0)),
    ("gabor 60", k_gabor(math.pi / 3.0)),
    ("gabor 120", k_gabor(2.0 * math.pi / 3.0)),
]
STACK = (4, 2, 4, 2, 5)  # blur, ridge, blur, ridge, blur 1.3  -> Y
STACK_NAMES = ("blur", "ridge", "blur", "ridge", "blur")
MAPS = (0, 4, 6)  # sobel x, blur 1, gabor 0  -> the three feature maps
MAP_NAMES = ("edge", "blur", "gabor")


def correlate(F: np.ndarray, K: np.ndarray, dil: int) -> np.ndarray:
    """2-D cross-correlation (what a conv layer computes), zero padding, 'same'.

    ``dil`` is the tap spacing on the field grid.  With PIXEL = dil * FINE the
    fine-grid result is the union of dil^2 interleaved real CNNs on shifted
    1.5 mm lattices — every value is exactly what a stride-1 CNN computes at
    that output position; nothing is interpolated.
    """
    n = K.shape[0] // 2
    Fp = np.pad(F, n * dil)
    out = np.zeros_like(F)
    h, w = F.shape
    for j in range(-n, n + 1):
        for i in range(-n, n + 1):
            wgt = float(K[j + n, i + n])
            if wgt == 0.0:
                continue
            oy, ox = n * dil + j * dil, n * dil + i * dil
            out += wgt * Fp[oy : oy + h, ox : ox + w]
    return out


class Net:
    """X, the five-layer stack's activations, the three map pre-activations."""

    def __init__(self, rng: SeededRNG, outline: Poly, box: Bounds, pitch: float):
        x0, y0, x1, y1 = box
        self.box = box
        self.dil = int(round(PIXEL / FINE))
        self.xs = np.arange(x0 - PAD, x1 + PAD + FINE * 0.5, FINE)
        self.ys = np.arange(y0 - PAD, y1 + PAD + FINE * 0.5, FINE)
        Xg, Yg = np.meshgrid(self.xs, self.ys)
        D = _dist_field(outline, Xg, Yg)
        self.D = D
        # hand-drawn wobble, bounded so the worst-case ring pitch stays legal;
        # it is PART of X, so the network sees exactly the rings that are drawn
        wob = (_fbm_grid(rng, Xg, Yg, 1.0 / 13.0, 3) - 0.5) * 2.0 * (0.30 * pitch)
        self.X = np.where(D > 0, np.maximum(D + wob, 0.0), 0.0)

        self.acts = [self.X]
        self.pre = []
        A = self.X
        for idx in STACK:
            Z = correlate(A, BANK[idx][1], self.dil)
            self.pre.append(Z)
            A = np.maximum(Z, 0.0)
            self.acts.append(A)
        self.Y = A
        self.maps = [correlate(self.X, BANK[i][1], self.dil) for i in MAPS]

    # -- the checkable statistics, printed into NOTES.md -------------------
    def stats(self) -> Dict[str, object]:
        out: Dict[str, object] = {}
        out["grid"] = self.X.shape
        out["layer_max"] = [float(a.max()) for a in self.acts]
        live = self.D > 0
        out["relu_killed"] = [
            float((z[live] < 0).mean()) for z in self.pre
        ]
        # Y against the medial axis of X: the axis is where |grad D| collapses
        gy, gx = np.gradient(self.D, FINE)
        g = np.hypot(gx, gy)
        axis = (self.D > 2.0) & (g < 0.75)
        ay, ax = np.nonzero(axis)
        top = self.Y >= 0.6 * self.Y.max()
        ty, tx = np.nonzero(top)
        if len(ax) and len(tx):
            A = np.stack([self.xs[ax], self.ys[ay]], 1)
            T = np.stack([self.xs[tx], self.ys[ty]], 1)
            d = np.array([np.min(np.hypot(*(A - t).T)) for t in T[:: max(1, len(T) // 800)]])
            out["y_to_axis_median_mm"] = float(np.median(d))
            out["y_to_axis_p95_mm"] = float(np.percentile(d, 95))
            # and the other way: the share of the axis Y covers
            Ts = T[:: max(1, len(T) // 1500)]
            dA = np.array([np.min(np.hypot(*(Ts - a).T)) for a in A[:: max(1, len(A) // 800)]])
            out["axis_covered_within_2mm"] = float((dA < 2.0).mean())
        out["map_ranges"] = [(float(m.min()), float(m.max())) for m in self.maps]
        return out


def erf_profile() -> Tuple[List[np.ndarray], List[float]]:
    """The exact composite |K| field of the stack, one layer back at a time.

    C_0 = delta (the output pixel); C_d = C_{d-1} (*) |K_(6-d)| / sum|K|.
    Returns the x-marginals and the exact variances (variances of convolved
    distributions add, so this is not a fit)."""
    C = np.ones((1, 1))
    margs = [np.ones(1)]
    var = [0.0]
    for idx in reversed(STACK):
        K = np.abs(BANK[idx][1])
        K = K / K.sum()
        h, w = C.shape
        N = np.zeros((h + 4, w + 4))
        for j in range(5):
            for i in range(5):
                N[j : j + h, i : i + w] += K[j, i] * C
        C = N
        m = C.sum(0)
        xs = np.arange(len(m)) - (len(m) - 1) / 2.0
        margs.append(m)
        var.append(float((m * xs * xs).sum()))
    return margs, var


# ===========================================================================
# drawing helpers for the computed fields
# ===========================================================================
def _solid_disc(x: float, y: float, r: float, pen: Optional[int], pitch: float = 0.34):
    """Filled Ben-Day disc: spiral at ``pitch`` + a closing circle."""
    if r < 0.12:
        return []
    if r <= pitch:
        return circle(x, y, r, pen=pen, f=1600, n=14)
    turns = max(1, int(r / pitch))
    n = turns * 22
    pts = [
        (
            x + r * (k / n) * math.cos(2 * math.pi * turns * k / n),
            y + r * (k / n) * math.sin(2 * math.pi * turns * k / n),
        )
        for k in range(n + 1)
    ]
    return _poly(pts, color=pen, f=1600) + circle(x, y, r, pen=pen, f=1600, n=max(14, int(r * 18)))


def _benday_kernel(
    box: Bounds, K: np.ndarray, r_frac: float = 0.42, keyline: int = 1
) -> List[GCodeCommand]:
    """A 5x5 kernel as signed Ben-Day discs.  AREA = |w| / max|w|, pen = sign.
    Zero taps keep a black lattice point, so the 5x5 grid always reads."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    p = min(w, h) / 5.25
    r_max = r_frac * p
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    m = float(np.abs(K).max())
    out: List[GCodeCommand] = []
    for j in range(5):
        for i in range(5):
            wt = float(K[j, i])
            px = cx + (i - 2) * p
            py = cy + (j - 2) * p  # row index = +y (sheet y is up)
            r = r_max * math.sqrt(abs(wt) / m)
            if r >= 0.16:
                out += _solid_disc(px, py, r, POS if wt > 0 else NEG)
            else:
                out += circle(px, py, 0.12, pen=BLACK, f=1600, n=8)
    # the second keyline goes INSIDE: outside it broke the u = 0 edge the
    # kernel bank shares with the title, X and the crosshair
    for k in range(keyline):
        d = 0.55 * k
        out += _emit([_rect(x0 + d, y0 + d, x1 - d, y1 - d)], BLACK, f=1800)
    return out


def _grad_step(F: np.ndarray, cell: float, spacing: float, mask: np.ndarray, q: float = 0.82):
    """Level step that puts contours ``spacing`` apart where the field is
    steep (82nd percentile of |grad F| inside ``mask``) — the house rule."""
    gy, gx = np.gradient(F, cell)
    g = np.hypot(gx, gy)[mask]
    if g.size == 0:
        return 0.0
    return spacing * float(np.quantile(g, q))


def _affine(polys: Sequence[Poly], s: float, ox: float, oy: float, bx: float, by: float):
    return [[(ox + (x - bx) * s, oy + (y - by) * s) for x, y in p] for p in polys]


def _translate(polys: Sequence[Poly], dx: float, dy: float) -> List[Poly]:
    return [[(x + dx, y + dy) for x, y in p] for p in polys]


# ===========================================================================
# 1. X — the input field, drawn as its own level sets
# ===========================================================================
def _draw_x(net: Net, outline: Poly, pen: int, pitch: float, knock: Optional[Region]):
    F = net.X
    polys: List[Poly] = []
    dashed: List[Poly] = []
    k = 1
    while k * pitch < float(F.max()):
        chains = _iso_chains(F, net.xs, net.ys, k * pitch)
        if knock is not None:
            chains = _clip_out(chains, knock)
        if k == 2:
            for ch in chains:
                dashed += _dash(ch, 3.4, 1.5, phase=1.7)
        else:
            polys += chains
        k += 1
    out = _guard_spacing(_emit(polys, pen) + _emit(dashed, pen), 0.80)
    ring = outline + [outline[0]]
    parts = _clip_out([ring], knock) if knock is not None else [ring]
    out += _emit(parts, pen)
    out += _emit(_translate(parts, 0.28, 0.0), pen)
    return out


# ===========================================================================
# 2. Y — the stack's output on the same lattice
# ===========================================================================
def _draw_y(net: Net, dx: float, pen: int, spacing: float = 0.95):
    F = net.Y
    top = float(F.max())
    # Y is a TUBE with a bell-shaped cross-section, so neither uniform
    # levels (bunch on the flanks) nor the gradient rule (sparse on the crest
    # and the foot) give an even fingerprint.  Read the profile across the
    # stem instead — the row through the stem's mid-height, walked out from
    # the crest on both sides and averaged — and take the levels the field
    # actually has at 1, 2, 3 ... x ``spacing`` mm from the crest.  Every
    # ring then sits ``spacing`` apart across the stem; elsewhere the
    # Occupancy pause holds the floor.
    x0, y0, x1, y1 = net.box
    jrow = int(np.argmin(np.abs(net.ys - (y0 + 0.25 * (y1 - y0)))))
    row = F[jrow]
    ic = int(np.argmax(row))
    nmax = min(ic, len(row) - 1 - ic)
    prof = 0.5 * (row[ic - np.arange(nmax + 1)] + row[ic + np.arange(nmax + 1)])
    dist = np.arange(nmax + 1) * FINE
    levels = []
    k = 1
    while True:
        dmm = (k - 0.5) * spacing
        if dmm > dist[-1]:
            break
        lv = float(np.interp(dmm, dist, prof))
        if lv < 0.03 * top:
            break
        levels.append(lv)
        k += 1
    levels = sorted(levels)  # outermost (lowest) first: it is the boundary
    Y_PROFILE.update({"row_y": float(net.ys[jrow]), "crest": float(prof[0]),
                      "levels": levels})
    polys: List[Poly] = []
    outer: List[Poly] = []
    for n, lv in enumerate(levels):
        ch = _translate(_drop_slivers(_iso_chains(F, net.xs, net.ys, lv)), dx, 0.0)
        if n == 0:
            outer = ch
        else:
            polys += ch
    # the outer ring is the boundary and is drawn double; it seeds the
    # occupancy grid so no inner ring may crowd it
    polys = _pause_resume([outer, polys], MIN_PITCH)[1]
    Y_POLYS[:] = outer + polys
    out = _emit(polys, pen)
    out += _emit(outer, pen)
    out += _emit(_translate(outer, 0.28, 0.0), pen)
    return out, outer, levels


# ===========================================================================
# 3. the feature maps — contours of K_i * X, signed
# ===========================================================================
def _draw_map(net: Net, which: int, cell: Bounds, spacing: float = 0.95):
    P = net.maps[which]
    bx0, by0, bx1, by1 = net.box
    mp = 1.5
    bx0, by0, bx1, by1 = bx0 - mp, by0 - mp, bx1 + mp, by1 + mp
    cx0, cy0, cx1, cy1 = cell
    s = min((cx1 - cx0) / (bx1 - bx0), (cy1 - cy0) / (by1 - by0))
    ox = (cx0 + cx1) / 2.0 - (bx1 - bx0) * s / 2.0
    oy = (cy0 + cy1) / 2.0 - (by1 - by0) * s / 2.0
    keep = (cx0 + 0.3, cy0 + 0.3, cx1 - 0.3, cy1 - 0.3)
    big = float(np.abs(P).max())
    step = _grad_step(P, FINE, spacing / s, np.abs(P) > 0.01 * big, q=MAP_Q)

    def ladder(step: float):
        pos: List[Poly] = []
        neg: List[Poly] = []
        lv = step * 0.75
        while lv < float(P.max()):
            pos += _drop_slivers(_iso_chains(P, net.xs, net.ys, lv), MIN_PITCH / s)
            lv += step
        lv = -step * 0.75
        while lv > float(P.min()):
            neg += _drop_slivers(_iso_chains(P, net.xs, net.ys, lv), MIN_PITCH / s)
            lv -= step
        pos = _clip_in(_affine(pos, s, ox, oy, bx0, by0), keep)
        neg = _clip_in(_affine(neg, s, ox, oy, bx0, by0), keep)
        return pos, neg

    # Gradient-rule ladder, then the engine's Occupancy grid pauses any
    # contour where it comes within MIN_PITCH of an earlier one and resumes
    # once clear.  Contours converge only locally (the Sobel response is a
    # near-step at the medial axis; the Gabor tube pinches at the junction),
    # so a local pause keeps the ladder dense everywhere else — widening the
    # step globally to satisfy those few spots left one contour per map.
    # The ladder starts at +-0.75 step so the two sign families stand 1.5
    # steps apart across the zero line.
    pos, neg = ladder(step)
    pos, neg = _pause_resume([pos, neg], MIN_PITCH)
    nd: List[Poly] = []
    for c in neg:
        nd += _dash(c, 1.3, 0.9)
    # no spacing guard here: on these 0.39x thumbnails it ate every curved
    # stretch.  The ladder is built from the gradient instead, and the real
    # minimum gap is MEASURED (see measure_gaps) and reported in NOTES.md.
    out = _emit(pos, POS, f=2500)
    out += _emit(nd, NEG, f=2500)
    MAP_POLYS.append((pos, neg))
    out += _emit([_rect(cx0, cy0, cx1, cy1)], BLACK, f=1800)
    return out, step, s


# ===========================================================================
# 4. the receptive field of the stack, against depth
# ===========================================================================
def _erf_cone(apex: Pt, base_y: float, half: float) -> Tuple[List[GCodeCommand], Dict]:
    margs, var = erf_profile()
    L = len(STACK)
    ax, ay = apex
    H = ay - base_y
    ppx = half / (2.0 * L)  # mm per pixel: the triangle reaches 2L px at the base
    out: List[GCodeCommand] = []

    def row_y(d: float) -> float:
        return ay - d / L * H

    # --- the Ben-Day rows: exact composite marginal at each layer --------
    r_row = 0.36 * ppx
    dots: List[Tuple[float, float, float]] = []
    for d in range(0, L + 1):
        m = margs[d]
        mx = float(m.max())
        half_n = (len(m) - 1) // 2
        for i, val in enumerate(m):
            px = ax + (i - half_n) * ppx
            r = r_row * math.sqrt(float(val) / mx) if d > 0 else 1.25
            dots.append((px, row_y(d), max(r, 0.14)))
    knock = Union(*[_Circle(x, y, r + 0.55) for x, y, r in dots if r > 0.3])

    # --- theoretical field: the dashed triangle ---------------------------
    env = [(ax - half, base_y), (ax, ay), (ax + half, base_y)]
    out += _emit(_dash(env, 3.0, 2.6), BLACK, f=2400)

    # --- effective field: central-mass quantile curves ------------------
    # At every integer depth the half-width holding q of the influence is
    # read EXACTLY off the composite marginal (pixels as unit bins, CDF
    # piecewise linear).  Between rows the width rides the exact sigma(s)
    # (variance interpolated linearly, which is exact for a continuous
    # diffusion), so each curve passes through its measured value at all
    # six rows and grows like sqrt(depth) between them.
    sig = [math.sqrt(1.0 / 12.0 + v) for v in var]
    widths: Dict[float, List[float]] = {}
    for q in ERF_QUANTILES:
        wq = []
        for d in range(L + 1):
            wq.append(_central_halfwidth(margs[d], q))
        widths[q] = wq
    fams: List[List[Poly]] = []
    for q in ERF_QUANTILES:
        ratio = [w / s for w, s in zip(widths[q], sig)]
        fam: List[Poly] = []
        for sgn in (-1.0, 1.0):
            pts: Poly = []
            for k in range(0, 241):
                sd = L * k / 240.0
                sg = math.sqrt(1.0 / 12.0 + float(np.interp(sd, np.arange(L + 1), var)))
                w = float(np.interp(sd, np.arange(L + 1), ratio)) * sg
                pts.append((ax + sgn * w * ppx, row_y(sd)))
            fam.append(pts)
        fam = _clip_out(_clip_out(fam, knock), _Circle(ax, ay, 3.0))
        fams.append(fam)
    # the dashed triangle joins the occupancy grid first, so the 95 % curve
    # yields to it where the two nearly coincide near the apex
    fams = _pause_resume([[env]] + fams, MIN_PITCH)[1:]
    curves = [c for f in fams for c in f]
    for q, fam in zip(ERF_QUANTILES, fams):
        if q >= 0.95:  # the outermost share rides dashed, like the envelope
            dd: List[Poly] = []
            for c in fam:
                dd += _dash(c, 2.0, 1.4)
            out += _emit(dd, BLACK, f=2500)
        else:
            out += _emit(fam, BLACK, f=2500)
    CONE_POLYS.extend(curves)

    for x, y, r in dots:
        out += _solid_disc(x, y, r, BLACK)

    # RF width in pixels, at the right end of each row
    for d in range(1, L + 1):
        n_px = len(margs[d])
        tx = ax + (n_px - 1) / 2.0 * ppx + 2.2
        out += _text_at(str(n_px), row_y(d) - 0.8, 1.6, BLACK, left=tx)

    info = {
        "var_px2": var,
        "sigma_px": [math.sqrt(1.0 / 12.0 + v) for v in var],
        "rf_px": [len(m) for m in margs],
        "quantile_halfwidth_px": {str(q): widths[q] for q in ERF_QUANTILES},
        "ppx": ppx,
    }
    return out, info


ERF_QUANTILES = (0.5, 0.8, 0.95)
MAP_Q = 0.6
Y_Q = 0.55
MAP_POLYS: List[Tuple[List[Poly], List[Poly]]] = []
CONE_POLYS: List[Poly] = []


def _central_halfwidth(m: np.ndarray, q: float) -> float:
    """Half-width w (px) with mass q inside [-w, w]; pixels are unit bins."""
    m = np.asarray(m, float) / float(np.sum(m))
    n = len(m)
    c = (n - 1) / 2.0
    edges = np.arange(n + 1) - 0.5 - c  # bin edges, centred
    cdf = np.concatenate([[0.0], np.cumsum(m)])
    lo = float(np.interp((1.0 - q) / 2.0, cdf, edges))
    hi = float(np.interp((1.0 + q) / 2.0, cdf, edges))
    return (hi - lo) / 2.0


def _thumb(net: Net, layer: int, box: Bounds, fracs=(0.08, 0.5)) -> List[GCodeCommand]:
    """Activation after layer ``layer``: contours at fixed fractions of its
    own max, mapped into ``box`` (same framing as the feature maps)."""
    A = net.acts[layer]
    bx0, by0, bx1, by1 = net.box
    mp = 1.5
    bx0, by0, bx1, by1 = bx0 - mp, by0 - mp, bx1 + mp, by1 + mp
    cx0, cy0, cx1, cy1 = box
    s = min((cx1 - cx0) / (bx1 - bx0), (cy1 - cy0) / (by1 - by0))
    ox = (cx0 + cx1) / 2.0 - (bx1 - bx0) * s / 2.0
    oy = (cy0 + cy1) / 2.0 - (by1 - by0) * s / 2.0
    top = float(A.max())
    polys: List[Poly] = []
    for f in fracs:
        polys += _drop_slivers(_iso_chains(A, net.xs, net.ys, f * top), MIN_PITCH / s)
    polys = _affine(polys, s, ox, oy, bx0, by0)
    polys = _pause_resume([polys], MIN_PITCH)[0]
    THUMB_POLYS.append(polys)
    return _emit(polys, ACT, f=2500)


THUMB_POLYS: List[List[Poly]] = []
Y_POLYS: List[Poly] = []
Y_PROFILE: Dict[str, object] = {}


def _drop_slivers(chains: Sequence[Poly], min_w: float = MIN_PITCH) -> List[Poly]:
    """Drop closed contour islands thinner than ``min_w``.

    Near a crest a level set can close as a sliver whose two sides stand
    0.3 mm apart; the Occupancy grid cannot see that (a polyline never
    crowds itself), so it is caught here by its mean width 2A / P."""
    out: List[Poly] = []
    for c in chains:
        if len(c) > 3 and math.hypot(c[0][0] - c[-1][0], c[0][1] - c[-1][1]) < 1e-6:
            A = 0.0
            Pm = 0.0
            for a, b in zip(c, c[1:]):
                A += a[0] * b[1] - b[0] * a[1]
                Pm += math.hypot(b[0] - a[0], b[1] - a[1])
            if Pm > 0 and 2.0 * abs(A / 2.0) / Pm < min_w:
                continue
        out.append(c)
    return out


def _pause_resume(families: Sequence[Sequence[Poly]], sep: float, step: float = 0.2,
                  min_run: float = 0.9) -> List[List[Poly]]:
    """Engine-native crowd control (``scene3d.Occupancy``) for 2-D contour
    families: walk every polyline in order, lift the pen wherever it comes
    within ``sep`` of an EARLIER polyline, resume when clear.  A polyline's
    own points join the grid only after it is finished, so it never rejects
    itself.  Families share one grid (both inks land on one sheet)."""
    occ = Occupancy(sep)
    out: List[List[Poly]] = []
    for fam in families:
        kept: List[Poly] = []
        for poly in fam:
            dense: Poly = []
            for a, b in zip(poly, poly[1:]):
                L = math.hypot(b[0] - a[0], b[1] - a[1])
                n = max(1, int(math.ceil(L / step)))
                for t in range(n):
                    dense.append((a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n))
            if poly:
                dense.append(poly[-1])
            runs: List[Poly] = []
            cur: Poly = []
            for q in dense:
                if occ.crowded(*q):
                    if len(cur) >= 2:
                        runs.append(cur)
                    cur = []
                else:
                    cur.append(q)
            if len(cur) >= 2:
                runs.append(cur)
            for r in runs:
                if sum(math.hypot(r[i + 1][0] - r[i][0], r[i + 1][1] - r[i][1])
                       for i in range(len(r) - 1)) >= min_run:
                    kept.append(r)
            for q in dense:
                occ.add(*q)
        out.append(kept)
    return out


def measure_gaps(polys: Sequence[Poly], step: float = 0.3) -> Tuple[float, float]:
    """Min and median nearest-neighbour distance between DIFFERENT polylines
    (resampled at ``step``) — the checkable spacing number for NOTES.md.

    A curve cut by a knockout (or split by the chainer) becomes several
    polylines whose ends touch; points within 0.9 mm of a chain end are not
    counted, since those junctions are not gaps."""
    pts = []
    ids = []
    for k, p in enumerate(polys):
        for a, b in zip(p, p[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(1, int(L / step))
            for t in range(n):
                pts.append((a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n))
                ids.append(k)
    if len(pts) < 2 or len(set(ids)) < 2:
        return (float("nan"), float("nan"))
    P = np.asarray(pts)
    I = np.asarray(ids)
    ends = np.asarray([p[0] for p in polys if len(p) > 1] + [p[-1] for p in polys if len(p) > 1])
    best = np.full(len(P), np.inf)
    for c0 in range(0, len(P), 700):
        blk = P[c0 : c0 + 700]
        d = np.hypot(blk[:, None, 0] - P[None, :, 0], blk[:, None, 1] - P[None, :, 1])
        d[I[c0 : c0 + 700][:, None] == I[None, :]] = np.inf
        best[c0 : c0 + 700] = d.min(1)
        de = np.hypot(blk[:, None, 0] - ends[None, :, 0], blk[:, None, 1] - ends[None, :, 1])
        best[c0 : c0 + 700][de.min(1) < 0.9] = np.inf
    fin = best[np.isfinite(best)]
    if fin.size == 0:
        return (float("nan"), float("nan"))
    return (float(fin.min()), float(np.median(fin)))


def _Circle(cx: float, cy: float, r: float) -> Region:
    from promptplot.generative.engine.geometry import Circle

    return Circle(cx, cy, r)


# ===========================================================================
# the plate
# ===========================================================================
LAST_STATS: Dict[str, object] = {}


def convolutions_real_kernel(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    fr = Frame(bounds)
    out: List[GCodeCommand] = []
    U, V = fr.u, fr.v
    MAP_POLYS.clear()
    CONE_POLYS.clear()
    THUMB_POLYS.clear()

    strip_w = N_TILES * TILE_W + (N_TILES - 1) * TILE_GAP
    strip_x0 = U(STRIP_CU) - strip_w / 2.0
    tile_top = V(TILE_TOP_V)
    tile_bot = tile_top - TILE_H
    tile_cy = (tile_top + tile_bot) / 2.0
    tiles: List[Bounds] = []
    for k in range(N_TILES):
        tx0 = strip_x0 + k * (TILE_W + TILE_GAP)
        tiles.append((tx0, tile_bot, tx0 + TILE_W, tile_top))

    base_y = V(BASE_V)
    lower_top = V(LOWER_TOP_V)
    cap_base = V(CAP_BASE_V)
    zone_w = 3 * ZONE_CELL_W + 2 * CELL_GAP
    kb_x0 = U(0.0)
    kb_h = 3 * KB_CELL_H + 2 * CELL_GAP
    kb_y1 = base_y + kb_h
    fm_x1 = U(1.0)
    fm_x0 = fm_x1 - zone_w
    cone_x = U(0.5)

    # ---------------- 1. header --------------------------------------------
    out += _text_at("CONVOLUTIONS", V(TITLE_V) - TITLE_CAP, TITLE_CAP, BLACK,
                    left=U(0.0), target_w=TITLE_W)
    out += _emit([[(U(0.0), V(RULE_V)), (U(0.0) + 7.6, V(RULE_V))]], BLACK, f=1800)
    for line, vv in zip(("local patterns", "global structures", "continuous perception"), SUB_V):
        out += _text_at(line, V(vv) - SUB_CAP, SUB_CAP, BLACK, left=U(0.0), target_w=SUB_W)
    # the corner note now states the network's ACTUAL hyper-parameters
    ur_left = U(1.0) - UR_W
    for line, vv in zip(("stride 1", "padding 2", "dilation 1", "channels 1"), UR_V):
        out += _text_at(line, V(vv) - UR_CAP, UR_CAP, BLACK, left=ur_left, target_w=UR_W)
    out += _emit([[(ur_left, V(UR_RULE_V)), (ur_left + 10.3, V(UR_RULE_V))]], BLACK, f=1800)

    # ---------------- 2. X, the network, Y ---------------------------------
    bx_box = (U(BX_U[0]), V(BX_V[1]), U(BX_U[1]), V(BX_V[0]))
    by_box = (U(BY_U[0]), V(BY_V[1]), U(BY_U[1]), V(BY_V[0]))
    dx_y = by_box[0] - bx_box[0]
    # k = 3 peaks at 30 / 150 / 270 deg: lobes up-right, up-left, down, so the
    # medial axis — what a ridge detector finds — is an upright Y.  The small
    # k = 1, 2 terms only break the symmetry; a k = 5 term (r01) would sprout
    # extra skeleton spurs and the Y would grow whiskers.
    x_out = _fit_poly(_amoeba(X_HARMONICS), bx_box)
    pitch = 0.95
    net = Net(rng, x_out, bx_box, pitch)

    # the kernel's real footprint on X: 5 x 5 taps at the pixel pitch,
    # placed inside the right rim of the stem at the strip's height
    band = [p for p in x_out if abs(p[1] - (tile_cy + 3.0)) < 3.0]
    xr = max(p[0] for p in band)
    win_c = (xr - 6.0, tile_cy + 3.0)
    wh = 2.5 * PIXEL
    win = (win_c[0] - wh, win_c[1] - wh, win_c[0] + wh, win_c[1] + wh)
    win_knock = Rect(win[0] - 0.8, win[1] - 0.8, win[2] + 0.8, win[3] + 0.8)

    out += _draw_x(net, x_out, BLACK, pitch, win_knock)
    for j in range(5):
        for i in range(5):
            out += circle(win_c[0] + (i - 2) * PIXEL, win_c[1] + (j - 2) * PIXEL, 0.22,
                          pen=BLACK, f=1600, n=8)
    out += _emit([_rect(*win)], BLACK, f=1800)

    y_cmds, y_outer, y_levels = _draw_y(net, dx_y, ACT, 0.95)
    out += y_cmds
    lp = [p for ch in y_outer for p in ch if abs(p[1] - tile_cy) < 4.0]
    y_hub = min(lp, key=lambda p: p[0]) if lp else (by_box[0] + 4.0, tile_cy)
    out += _solid_disc(y_hub[0], y_hub[1], 1.3, ACT)

    xl, xb = _label_slot(x_out, bx_box, side=-1, cap=3.95, w=4.6, clear=3.0)
    out += _text_at("X", xb, 3.95, BLACK, left=xl)

    # crosshair captions: input x under X (r01), output y mirrored under Y
    cr_x = U(0.026)
    cr_y = V(0.508)
    out += _emit([[(cr_x, V(0.478)), (cr_x, V(0.534))]], BLACK, f=2200)
    out += _emit([[(U(0.0), cr_y), (U(0.128), cr_y)]], BLACK, f=2200)
    out += _text_at("input x", V(0.4955), 2.5, BLACK, left=U(0.052), target_w=17.0)
    cr_x2 = U(0.974)
    out += _emit([[(cr_x2, V(0.478)), (cr_x2, V(0.534))]], BLACK, f=2200)
    out += _emit([[(U(0.872), cr_y), (U(1.0), cr_y)]], BLACK, f=2200)
    out += _text_at("output y", V(0.4955), 2.5, BLACK, right=U(0.948), target_w=19.4)

    # ---------------- 3. the strip -----------------------------------------
    label_boxes = Union(
        Rect(tiles[2][0] - 3.0, V(0.262) - 1.2, tiles[2][2] + 3.0, V(0.262) + 5.6),
        Rect(tiles[3][2] - 2.5, V(0.262) - 1.2, tiles[4][0] + 2.5, V(0.262) + 5.6),
    )
    tile_regions = Union(
        *[Rect(t[0] - 1.1, t[1] - 1.1, t[2] + 1.1, t[3] + 1.1) for t in tiles],
        label_boxes,
        win_knock,
    )

    conn: List[Tuple[Poly, int, bool]] = []
    t0 = tiles[0]
    n_in = 10
    for k in range(n_in):
        sy = win[1] + (k + 0.5) * (win[3] - win[1]) / n_in
        fy = t0[1] + (k + 0.5) * (t0[3] - t0[1]) / n_in
        sag = (k / (n_in - 1.0) - 0.5) * 30.0
        curve = _bez(
            (win[2], sy),
            (win[2] + 16.0, sy + sag * 0.9),
            (t0[0] - 20.0, fy + sag * 0.55),
            (t0[0] + TILE_W * 0.5, fy),
            76,
        )
        conn.append((curve, BLACK, k in (1, 4, 8)))
    t4 = tiles[-1]
    for k in range(6):
        fy = t4[1] + (k + 0.5) * (t4[3] - t4[1]) / 6.0
        sag = (k / 5.0 - 0.5) * 18.0
        curve = _bez(
            (t4[2] - TILE_W * 0.5, fy),
            (t4[2] + 20.0, fy + sag),
            (y_hub[0] - 22.0, y_hub[1] + sag * 0.5),
            y_hub,
            72,
        )
        conn.append((curve, ACT, k == 3))
    for k in range(N_TILES - 1):
        a, b = tiles[k], tiles[k + 1]
        for m in range(3):
            ya = a[1] + (m + 0.7) * (a[3] - a[1]) / 3.5
            yb = b[1] + (m + 0.7) * (b[3] - b[1]) / 3.5
            curve = _bez((a[2] - 2.0, ya), (a[2] + TILE_GAP * 0.45, ya),
                         (b[0] - TILE_GAP * 0.45, yb), (b[0] + 2.0, yb), 34)
            conn.append((curve, ACT, False))
    for curve, pen, dashed in conn:
        parts = _clip_out([curve], tile_regions)
        if dashed:
            dd: List[Poly] = []
            for p in parts:
                dd += _dash(p, 2.4, 2.0)
            parts = dd
        out += _emit(parts, pen, f=2400)

    # each tile: its kernel; its name above; UNDER it, the activation that
    # layer leaves behind — trefoil to Y, one real step at a time
    for k, t in enumerate(tiles):
        out += _benday_kernel(t, BANK[STACK[k]][1])
        out += _text_at(STACK_NAMES[k], t[3] + 1.9, NAME_CAP, BLACK, centre=(t[0] + t[2]) / 2.0)
        th = (t[0], t[1] - THUMB_GAP - THUMB_H, t[2], t[1] - THUMB_GAP)
        out += _thumb(net, k + 1, th)

    out += _text_at("K ∗ X", V(0.262), 3.95, BLACK, centre=(tiles[2][0] + tiles[2][2]) / 2.0,
                    target_w=15.2)
    out += _text_at("σ(·)", V(0.262), 3.95, BLACK, centre=(tiles[3][2] + tiles[4][0]) / 2.0)

    # ---------------- 4. kernel bank ---------------------------------------
    for j in range(3):
        for i in range(3):
            idx = j * 3 + i
            cx0 = kb_x0 + i * (ZONE_CELL_W + CELL_GAP)
            cy1 = kb_y1 - j * (KB_CELL_H + CELL_GAP)
            out += _benday_kernel((cx0, cy1 - KB_CELL_H, cx0 + ZONE_CELL_W, cy1), BANK[idx][1],
                                  keyline=2 if idx in MAPS else 1)
    out += _text_at("kernel bank", cap_base, 2.5, BLACK, centre=kb_x0 + zone_w / 2.0, target_w=24.5)

    # ---------------- 5. receptive field -----------------------------------
    cone_cmds, cone_info = _erf_cone((cone_x, lower_top), base_y, CONE_HALF)
    out += cone_cmds
    out += _text_at("receptive field", cap_base, 2.5, BLACK, centre=cone_x, target_w=31.2)

    # ---------------- 6. feature maps --------------------------------------
    map_info = []
    for k in range(3):
        cx0 = fm_x0 + k * (ZONE_CELL_W + CELL_GAP)
        cell = (cx0, base_y, cx0 + ZONE_CELL_W, base_y + FM_CELL_H)
        cmds, step, s = _draw_map(net, k, cell)
        out += cmds
        out += _text_at(MAP_NAMES[k], base_y + FM_CELL_H + 1.8, 1.85, BLACK,
                        centre=cx0 + ZONE_CELL_W / 2.0)
        map_info.append({"step": step, "scale": s})
    out += _text_at("feature maps", cap_base, 2.5, BLACK, centre=fm_x0 + zone_w / 2.0, target_w=28.6)

    # ---------------- 7. the spine -----------------------------------------
    for v_lo, v_hi in ((0.000, 0.232), (GUTTER_V[0] + 0.004, LOWER_TOP_V - 0.028)):
        out += _emit(_dash([(U(0.5), V(v_lo)), (U(0.5), V(v_hi))], 3.0, 3.4), BLACK, f=2400)

    LAST_STATS.clear()
    LAST_STATS.update(net.stats())
    LAST_STATS["cone"] = cone_info
    LAST_STATS["maps"] = map_info
    LAST_STATS["y_levels"] = len(y_levels)
    LAST_STATS["y_profile"] = dict(Y_PROFILE)
    LAST_STATS["window"] = win
    LAST_STATS["gaps_maps"] = [(measure_gaps(p), measure_gaps(n), measure_gaps(p + n)) for p, n in MAP_POLYS]
    LAST_STATS["gaps_cone"] = measure_gaps(CONE_POLYS)
    LAST_STATS["gaps_y"] = measure_gaps(Y_POLYS)
    LAST_STATS["gaps_thumbs"] = [measure_gaps(t) for t in THUMB_POLYS]
    return out


NAME_CAP = 2.5
THUMB_GAP = 2.2
THUMB_H = 15.5

X_HARMONICS = ((3, 0.40, -math.pi / 2.0), (2, 0.14, 0.9), (1, 0.10, -0.9))
