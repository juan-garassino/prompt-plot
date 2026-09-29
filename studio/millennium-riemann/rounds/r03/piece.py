"""RIEMANN HYPOTHESIS -- r03 (iterate, parent r02, thesis ABSTRACT).  Plate 1 of the
MILLENNIUM series.  r03 = r02 polish: ONE one-way red pass per arm; key / foot
numerals / type registration; series caption.  The field is r02's, unchanged.

Lineage: Sol LeWitt, *Wall Drawing #46* (1970) -- "vertical lines, not straight,
not touching, covering the wall evenly" (wording: curator to verify against the
catalogue raisonne).  Order taken: an INSTRUCTION executed exactly, whose text
could redraw the wall.  Here zeta writes the two instructions:

    BLACK     every point where Re zeta(s) = 0
    HAIRLINE  every point where Im zeta(s) = 0
    RED       where both are, above the real line (rho_n = 1/2 + i gamma_n)

Their lines are not straight and never touch -- except at the zeros, and every
touch above the real axis stands in one column that nobody draws (Re s = 1/2).

ORDER: INTERLACED / LAMINAR.  Canon: SWISS sheet (flat by nature -- declared:
conformality, the 90 deg at every red cross, survives only on a flat isotropic
plane) carrying a conceptual instruction drawing.

Every curve is the level-0 set of the real zeta function, read from
``xray_abstract.json`` (this round; computed by ``compute_abstract.py`` --
Euler-Maclaurin + functional equation, 1.6e-13 max rel. error and 100 % sign
agreement vs mpmath on 4000 points; contourpy marching squares, grid 0.05 u).
Every red centre is a gamma_n read from ``../../data/zeros.json`` (mpmath
zetazero).  Nothing is placed by eye; the plate uses no randomness.

Design sheet: A3 portrait, mm, y UP from the bottom edge, drawable
[15,282] x [15,405], uniformly fitted to ``bounds``.  One scale on both axes:
x = 180 + 3.45 (sigma - 1/2),  y = 32 + 3.45 t,  window sigma in [-47.33, 30.07],
t in [0, 97.35] (the mid-gap between gamma_28 and gamma_29), 28 zeros.

Pens / layers, plotted in index order (light -> dark, red last):
    0 HAIRLINE  black 0.1   Im zeta = 0, the real axis included
    1 BLACK     black 0.3   Re zeta = 0
    2 TEXT      black 0.3   (same pen, own layer, no swap) title, instructions, captions
    3 RED       red 0.5     the nontrivial zeros: both branches through rho_n, r = 1.6 mm,
                            ONE one-way pass per arm (r03)

Entry point: ``riemann_two_instructions``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Rect, clip
from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

HERE = Path(__file__).resolve().parent
_XRAY = HERE.parent / "r02" / "xray_abstract.json"  # r02 field, read-only, unchanged
_ZEROS = HERE.parents[1] / "data" / "zeros.json"

# ===========================================================================
# the design sheet (A3 portrait, mm, y up) -- encoding 5A
# ===========================================================================
SHEET = (15.0, 15.0, 282.0, 405.0)
S = 3.45  # mm per unit, BOTH axes
X0 = 180.0  # sigma = 1/2  (the 62 % line; never drawn)
Y_AX = 32.0  # t = 0, the real axis = the field's bottom edge
X_L, X_R = SHEET[0], SHEET[2]
T_TOP = 97.35  # mid-gap gamma_28 = 95.871 / gamma_29 = 98.831
Y_TOP = Y_AX + S * T_TOP  # 367.86
R_RED = 1.6  # red cross radius, mm (0.38 x the tightest gap, 4.21 mm)
RED_OVER = 0.2  # red runs 0.2 mm past the circle to cover the black joint
RULE = S * math.pi / math.log(2.0)  # 15.637 mm: t = k pi / ln 2, the right-field rulings
X_TXT = 206.0  # text column, flush-left (sigma = 8.04, rulings flat to < 0.15 mm)
SIMPLIFY = 0.02  # RDP tolerance, mm -- far below the 0.17 mm marching-squares grid


def sx(sig: float) -> float:
    return X0 + S * (sig - 0.5)


def ty(t: float) -> float:
    return Y_AX + S * t


def _load() -> Tuple[List[np.ndarray], List[np.ndarray], List[float]]:
    d = json.loads(_XRAY.read_text())
    z = json.loads(_ZEROS.read_text())
    gam = [float(q["gamma"]) for q in z["zeros"] if float(q["gamma"]) < T_TOP]
    return ([np.asarray(p, float) for p in d["re0"]],
            [np.asarray(p, float) for p in d["im0"]], gam)


RE0, IM0, GAMMAS = _load()
assert len(GAMMAS) == 28 and abs(GAMMAS[0] - 14.134725) < 1e-6


# ===========================================================================
# design -> sheet transform
# ===========================================================================
class Fit:
    def __init__(self, bounds):
        bx0, by0, bx1, by1 = bounds
        w, h = SHEET[2] - SHEET[0], SHEET[3] - SHEET[1]
        self.k = min((bx1 - bx0) / w, (by1 - by0) / h)
        self.ox = bx0 + ((bx1 - bx0) - w * self.k) / 2.0 - SHEET[0] * self.k
        self.oy = by0 + ((by1 - by0) - h * self.k) / 2.0 - SHEET[1] * self.k

    def run(self, r: Sequence[Pt]) -> Run:
        return [(self.ox + x * self.k, self.oy + y * self.k) for x, y in r]


# ===========================================================================
# polyline utilities
# ===========================================================================
def rdp(pts: np.ndarray, eps: float) -> np.ndarray:
    """Ramer-Douglas-Peucker (iterative).  Drops only vertices within ``eps`` of
    the chord -- collinear marching-squares steps; no vertex is moved."""
    n = len(pts)
    if n < 3:
        return pts
    keep = np.zeros(n, bool)
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        p, q = pts[a], pts[b]
        seg = pts[a + 1:b]
        d = q - p
        L = math.hypot(d[0], d[1])
        if L < 1e-12:
            dist = np.hypot(seg[:, 0] - p[0], seg[:, 1] - p[1])
        else:
            dist = np.abs(d[0] * (seg[:, 1] - p[1]) - d[1] * (seg[:, 0] - p[0])) / L
        i = int(np.argmax(dist))
        if dist[i] > eps:
            m = a + 1 + i
            keep[m] = True
            stack += [(a, m), (m, b)]
    return pts[keep]


def length(r: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(r, r[1:]))


def to_sheet(p: np.ndarray) -> np.ndarray:
    return np.column_stack([X0 + S * (p[:, 0] - 0.5), Y_AX + S * p[:, 1]])


def drop_axis_trace(p: np.ndarray) -> List[np.ndarray]:
    """The contour of Im zeta traces the real axis itself between the two
    half-step rows (exactly at t = 0 by conjugate symmetry).  That trace is
    replaced by ONE exact hairline, so remove runs lying on t = 0."""
    on = p[:, 1] <= 1e-9
    out, cur = [], []
    for i in range(len(p)):
        if on[i] and i + 1 < len(p) and on[i + 1]:
            if len(cur) >= 2:
                cur.append(p[i])
                out.append(np.array(cur))
            cur = []
            continue
        cur.append(p[i])
    if len(cur) >= 2:
        out.append(np.array(cur))
    return out


FIELD = Rect(X_L, Y_AX, X_R, Y_TOP)


def field_runs(lines: List[np.ndarray]) -> List[np.ndarray]:
    """sheet mm, cropped exactly at the frame (left/right), the real axis and the
    top crop; RDP-thinned below pen resolution."""
    out = []
    for p in lines:
        for q in drop_axis_trace(p):
            m = to_sheet(q)
            for r in clip([tuple(v) for v in m], FIELD, keep="inside"):
                a = rdp(np.asarray(r), SIMPLIFY)
                if len(a) >= 2 and length(a.tolist()) > 0.3:
                    out.append(a)
    return out


# ===========================================================================
# red substitution: the two branches THROUGH rho_n, inside radius r
# ===========================================================================
def _walk(p: np.ndarray, i0: int, c: np.ndarray, R: float, step: int) -> Tuple[int, np.ndarray]:
    """From vertex i0 (inside R) walk in direction ``step`` until the curve leaves
    the circle of radius R about c; return (last inside index, exact exit point)
    or (end index, end point) if the curve ends inside."""
    i = i0
    while 0 <= i + step < len(p):
        j = i + step
        if np.hypot(*(p[j] - c)) >= R:
            a, b = p[i], p[j]
            d = b - a
            f = a - c
            A = d @ d
            B = 2 * f @ d
            C = f @ f - R * R
            u = (-B + math.sqrt(max(B * B - 4 * A * C, 0.0))) / (2 * A)
            return i, a + u * d
        i = j
    return i, p[i]


def substitute(runs: List[np.ndarray], c: np.ndarray) -> Tuple[List[np.ndarray], np.ndarray, float]:
    """Find the run passing through c; cut it at radius R_RED (black keeps the
    outside) and return the red sub-curve out to R_RED + RED_OVER.  Every other
    run -- and every other passage of this run through the circle -- is left
    untouched.  Returns (new runs, red polyline, miss distance mm)."""
    best, bi, bk = 1e9, -1, -1
    for k, p in enumerate(runs):
        # distance to segments, not just vertices
        a, b = p[:-1], p[1:]
        ab = b - a
        L2 = np.maximum((ab ** 2).sum(1), 1e-18)
        u = np.clip(((c - a) * ab).sum(1) / L2, 0, 1)
        proj = a + ab * u[:, None]
        ds = np.hypot(proj[:, 0] - c[0], proj[:, 1] - c[1])
        j = int(np.argmin(ds))
        if ds[j] < best:
            best, bk, bi = float(ds[j]), k, j
    p = runs[bk]
    # insert the exact foot point so the walk starts ON the curve at the zero
    a, b = p[bi], p[bi + 1]
    ab = b - a
    u = float(np.clip(((c - a) @ ab) / max(ab @ ab, 1e-18), 0, 1))
    foot = a + u * ab
    q = np.vstack([p[: bi + 1], foot[None], p[bi + 1:]])
    i0 = bi + 1
    # black: split out [entry(R), exit(R)] of THIS passage
    lo_i, lo_pt = _walk(q, i0, c, R_RED, -1)
    hi_i, hi_pt = _walk(q, i0, c, R_RED, +1)
    new = [r for k, r in enumerate(runs) if k != bk]
    left = np.vstack([q[:lo_i], lo_pt[None]]) if lo_i > 0 else None
    right = np.vstack([hi_pt[None], q[hi_i + 1:]]) if hi_i < len(q) - 1 else None
    for piece in (left, right):
        if piece is not None and len(piece) >= 2 and length(piece.tolist()) > 0.3:
            new.append(piece)
    # red: [entry(R+over), exit(R+over)], the true curve through the zero
    R2 = R_RED + RED_OVER
    rlo_i, rlo_pt = _walk(q, i0, c, R2, -1)
    rhi_i, rhi_pt = _walk(q, i0, c, R2, +1)
    red = np.vstack([rlo_pt[None], q[rlo_i: rhi_i + 1], rhi_pt[None]])
    return new, red, best


def arm_angle(red: np.ndarray, c: np.ndarray) -> float:
    """direction of a red branch at the centre, degrees in (-90, 90]."""
    d = np.hypot(red[:, 0] - c[0], red[:, 1] - c[1])
    j = int(np.argmin(d))
    a, b = red[max(j - 3, 0)], red[min(j + 3, len(red) - 1)]
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    while ang <= -90:
        ang += 180
    while ang > 90:
        ang -= 180
    return ang


# ===========================================================================
# type: the house stroke font, 4 x 6 cell; zeta authored (the font has none)
# ===========================================================================
_ZETA = [[(0.6, 6.0), (3.6, 6.0), (2.5, 4.9), (1.2, 3.5), (0.4, 2.2), (0.35, 1.1),
          (1.0, 0.35), (2.3, 0.1), (3.2, -0.25), (3.4, -0.9), (2.9, -1.6)]]
ADV = 5.6  # font advance per character, cell units


def chain_glyph(strokes: List[List[Pt]]) -> List[List[Pt]]:
    """Join a glyph's strokes wherever two share an endpoint (flipping as
    needed) -> fewer pen-downs, nothing retraced, the ink is identical except
    that a shared corner is inked once instead of twice."""
    rest = [list(st) for st in strokes]
    out: List[List[Pt]] = []
    eq = lambda a, b: abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9
    while rest:
        cur = rest.pop(0)
        grown = True
        while grown:
            grown = False
            for i, st in enumerate(rest):
                if eq(cur[-1], st[0]):
                    cur += st[1:]
                elif eq(cur[-1], st[-1]):
                    cur += st[::-1][1:]
                elif eq(cur[0], st[-1]):
                    cur = st[:-1] + cur
                elif eq(cur[0], st[0]):
                    cur = st[::-1][:-1] + cur
                else:
                    continue
                rest.pop(i)
                grown = True
                break
        out.append(cur)
    return out


def set_text(txt: str, x: float, y: float, cap: float, track: float = 0.0,
             chain: bool = True) -> Tuple[List[Run], float]:
    runs: List[Run] = []
    sc = cap / 6.0
    cx = x
    for ch in txt:
        strokes = _ZETA if ch == "ζ" else (_GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or [])
        if chain:
            strokes = chain_glyph([[tuple(v) for v in st] for st in strokes])
        for st in strokes:
            runs.append([(cx + gx * sc, y + gy * sc) for gx, gy in st])
        cx += ADV * sc + track
    return runs, (cx - x - track) if txt else 0.0


def text_width(txt: str, cap: float, track: float = 0.0) -> float:
    return set_text(txt, 0.0, 0.0, cap, track)[1]


def split_corners(r: Run, max_turn: float = 50.0) -> List[Run]:
    """Split a glyph stroke at sharp corners (turn > ``max_turn`` deg) so each
    part can be thickened by parallel offsets without the averaged-normal
    pinch at the corner (which made N and M diagonals read thin)."""
    out, cur = [], [r[0]]
    for i in range(1, len(r) - 1):
        cur.append(r[i])
        a = math.atan2(r[i][1] - r[i - 1][1], r[i][0] - r[i - 1][0])
        b = math.atan2(r[i + 1][1] - r[i][1], r[i + 1][0] - r[i][0])
        turn = abs((math.degrees(b - a) + 180.0) % 360.0 - 180.0)
        if turn > max_turn:
            out.append(cur)
            cur = [r[i]]
    cur.append(r[-1])
    out.append(cur)
    return out


def ink_box(runs: List[Run]) -> Tuple[float, float, float, float]:
    xs = [x for r in runs for x, _ in r]
    ys = [y for r in runs for _, y in r]
    return min(xs), min(ys), max(xs), max(ys)


def solve_track(txt: str, x0: float, x_end: float, cap: float) -> float:
    """tracking such that the ink of the LAST glyph ends exactly on x_end"""
    sc = cap / 6.0
    last = _ZETA if txt[-1] == "ζ" else _GLYPHS.get(txt[-1])
    gmax = max(gx for st in last for gx, _ in st)
    return (x_end - x0 - (len(txt) - 1) * ADV * sc - gmax * sc) / (len(txt) - 1)


def _dense(r: Sequence[Pt], step: float = 0.05) -> np.ndarray:
    p = np.asarray(r, float)
    out = [p[:1]]
    for a, b in zip(p[:-1], p[1:]):
        n = max(1, int(math.ceil(math.hypot(*(b - a)) / step)))
        u = np.linspace(0, 1, n + 1)[1:, None]
        out.append(a + u * (b - a))
    return np.vstack(out)


def min_clearance(runs: List[Run], field: List[np.ndarray]) -> float:
    """min distance (mm, centreline) from any glyph point to any field line"""
    g = np.vstack([_dense(r) for r in runs])
    x0, y0 = g.min(0) - 6.0
    x1, y1 = g.max(0) + 6.0
    best = 1e9
    for f in field:
        if f[:, 0].max() < x0 or f[:, 0].min() > x1 or f[:, 1].max() < y0 or f[:, 1].min() > y1:
            continue
        q = _dense(f.tolist())
        q = q[(q[:, 0] > x0) & (q[:, 0] < x1) & (q[:, 1] > y0) & (q[:, 1] < y1)]
        if len(q):
            d = np.sqrt(((g[:, None, :] - q[None, :, :]) ** 2).sum(-1)).min()
            best = min(best, float(d))
    return best


def ruling_span(field: List[np.ndarray], xa: float, xb: float, mid: float) -> Tuple[float, float]:
    """highest field-line point below ``mid`` and lowest above it, over x in [xa, xb]"""
    lo, hi = -1e9, 1e9
    for f in field:
        q = _dense(f.tolist(), 0.2)
        q = q[(q[:, 0] >= xa) & (q[:, 0] <= xb)]
        if len(q):
            below = q[q[:, 1] < mid, 1]
            above = q[q[:, 1] >= mid, 1]
            if len(below):
                lo = max(lo, float(below.max()))
            if len(above):
                hi = min(hi, float(above.min()))
    return lo, hi


# ===========================================================================
# pens
# ===========================================================================
LAYERS = ("hair", "black", "text", "red")


def _pen_map(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 4:
        return {"hair": 0, "black": 1, "text": 2, "red": 3}
    if colors == 3:
        return {"hair": 0, "black": 1, "text": 1, "red": 2}
    if colors == 2:
        return {"hair": 0, "black": 0, "text": 0, "red": 1}
    return {k: None for k in LAYERS}


# ===========================================================================
# layer ordering for batched streaming: bottom -> top, nearest end next
# ===========================================================================
def order_runs(runs: List[Run]) -> List[Run]:
    rest = [list(r) for r in runs]
    rest.sort(key=lambda r: min(r[0][1], r[-1][1]))
    out: List[Run] = []
    pos = (X_L, Y_AX)
    while rest:
        best, bi, flip = 1e18, 0, False
        for i, r in enumerate(rest[:40]):  # look-ahead window keeps it bottom-up
            for fl, e in ((False, r[0]), (True, r[-1])):
                d = (e[0] - pos[0]) ** 2 + (e[1] - pos[1]) ** 2
                if d < best:
                    best, bi, flip = d, i, fl
        r = rest.pop(bi)
        r = r[::-1] if flip else r
        out.append(r)
        pos = r[-1]
    return out


def split_long(r: np.ndarray, max_mm: float = 300.0) -> List[np.ndarray]:
    """A tongue longer than ``max_mm`` splits at its U-tip (max x vertex) so no
    single pen-down is longer than a batch boundary allows."""
    if length(r.tolist()) <= max_mm:
        return [r]
    j = int(np.argmax(r[:, 0]))
    if j in (0, len(r) - 1):
        j = len(r) // 2
    return [r[: j + 1], r[j:]]


# ===========================================================================
# the plate
# ===========================================================================
REPORT: Dict[str, object] = {}


def build_layers() -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}
    A = field_runs(RE0)
    B = field_runs(IM0)

    # ---- RED: substitution at the 28 zeros --------------------------------
    red_runs, misses, angles = [], [], []
    for g in GAMMAS:
        c = np.array([X0, ty(g)])
        A, ra, ma = substitute(A, c)
        B, rb, mb = substitute(B, c)
        misses += [ma, mb]
        aa, ab = arm_angle(ra, c), arm_angle(rb, c)
        angles.append((g, aa, ab))
        # r03: ONE one-way pass of the red nib per arm, on the true curve (r02's
        # out-and-back pair inked every arm point twice and the centre 4x)
        for arm in (ra.tolist(), rb.tolist()):
            red_runs.append(arm)
    REPORT["red_centre_miss_mm_max"] = max(misses)
    REPORT["arm_angles"] = angles

    # ---- HAIRLINE: Im zeta = 0 + the exact real axis ----------------------
    hair = [[(X_L, Y_AX), (X_R, Y_AX)]] + [r.tolist() for r in B]
    L["hair"] = order_runs(hair)
    # ---- BLACK: Re zeta = 0 -----------------------------------------------
    blk: List[Run] = []
    for r in A:
        blk += [q.tolist() for q in split_long(r)]
    L["black"] = order_runs(blk)
    L["red"] = order_runs(red_runs)

    # ---- TEXT ---------------------------------------------------------------
    T: List[Run] = []
    # title: display weight = five passes of the 0.3 nib 0.18 mm apart (a ~1.0 mm
    # stroke: type as MASS, the plate's clear second), chained out-back-out into
    # ONE pen-down per glyph stroke.  Set 0.36 mm in from the frame so the outer
    # pass lands on the margin, not over it.
    # tracking is SOLVED so the last glyph's outer pass ends exactly on x = X0:
    # the title spans the comb and its end registers the undrawn column from
    # above, outside the field (no mark is made on sigma = 1/2 itself)
    cap_t = 8.0
    ttl = "RIEMANN HYPOTHESIS"
    ink_w = (len(ttl) - 1) * ADV * cap_t / 6.0 + 4.0 * cap_t / 6.0  # last glyph ink = 4 cells
    tr_t = ((X0 - 0.36) - (X_L + 0.36) - ink_w) / (len(ttl) - 1)
    title, _ = set_text(ttl, X_L + 0.36, 395.0, cap_t, track=tr_t, chain=False)
    # r03: the corner-split pieces of one glyph stroke are chained back into ONE
    # pen-down; the hop between pieces lies within 0.36 mm of the corner vertex,
    # i.e. inside the glyph's own ~1 mm mass (52 -> 31 title pen cycles)
    for r0 in title:
        chain: Run = []
        for r in split_corners(r0):
            offs = [-0.36, -0.18, 0.0, 0.18, 0.36]
            if chain:
                a, b = _offset_polyline(r, offs[0])[0], _offset_polyline(r, offs[-1])[0]
                e = chain[-1]
                if math.hypot(b[0] - e[0], b[1] - e[1]) < math.hypot(a[0] - e[0], a[1] - e[1]):
                    offs = offs[::-1]
            for j, d in enumerate(offs):
                q = _offset_polyline(r, d) if d else list(r)
                chain += q if j % 2 == 0 else q[::-1]
        T.append(chain)
    # the statement: tracking SOLVED (as the title's) so the last glyph's ink
    # ends on x = X0 -- both lines of the head register the undrawn column
    cap_s = 2.5
    stmt = "EVERY CROSSING ABOVE THE REAL LINE STANDS ON RE S = 1/2."
    tr_s = solve_track(stmt, X_L, X0, cap_s)
    T += set_text(stmt, X_L, 384.0, cap_s, track=tr_s)[0]
    REPORT["statement_track_mm"] = tr_s

    # the series caption (r01's, text only): flush-left on X_TXT, its cap line on
    # the title's outer cap line (395 + 8 + 0.36)
    cap_k = 2.2
    tr_k = cap_k * 0.1
    y_cap = 395.0 + 8.0 + 0.36
    for i, ln in enumerate(["MILLENNIUM PRIZE PROBLEMS  1 / 7", "CLAY MATHEMATICS INSTITUTE, 2000"]):
        assert X_TXT + text_width(ln, cap_k, tr_k) <= X_R, ln
        T += set_text(ln, X_TXT, y_cap - cap_k - i * cap_k * 1.8, cap_k, tr_k)[0]

    # the wall label: one instruction per ruling band, flush-left on X_TXT.
    # r03: each block's INK box (descenders included) is centred between the
    # ACTUAL rulings measured over the label's x-span, and every glyph is
    # checked >= 2.5 mm from every field line (r02 missed by 0.25 mm on the
    # zeta descender at k = 20).
    cap_i = 2.2
    tr_i = cap_i * 0.1
    lead = cap_i * 1.6
    maxw = X_R - X_TXT
    label = [
        (20, ["1  BLACK", "EVERY POINT WHERE THE REAL", "PART OF ζ(S) IS ZERO."]),
        (19, ["2  HAIRLINE", "EVERY POINT WHERE THE IMAGINARY", "PART OF ζ(S) IS ZERO."]),
        (18, ["3  RED", "WHERE BOTH ARE,", "ABOVE THE REAL LINE."]),
    ]
    field = [np.asarray(r, float) for r in L["hair"] + L["black"]]
    clear = {}
    for k, lines in label:
        blk_runs: List[Run] = []
        for i, ln in enumerate(lines):
            assert text_width(ln, cap_i, tr_i) <= maxw, ln
            blk_runs += set_text(ln, X_TXT, -i * lead, cap_i, tr_i)[0]
        bx0, by0, bx1, by1 = ink_box(blk_runs)
        mid = Y_AX + (k + 0.5) * RULE
        y_lo, y_hi = ruling_span(field, bx0 - 1.0, bx1 + 1.0, mid)
        dy = (y_lo + y_hi) / 2.0 - (by0 + by1) / 2.0
        blk_runs = [[(x, y + dy) for x, y in r] for r in blk_runs]
        d = min_clearance(blk_runs, field)
        clear[k] = (round(y_lo, 3), round(y_hi, 3), round(d, 3))
        assert d >= 2.5, f"wall label k={k} is {d:.2f} mm from a ruling"
        T += blk_runs
    REPORT["label_clearance"] = clear

    # the three true feet under the baseline: -4, -2 (trivial zeros) and 1 (the
    # pole).  They anchor sigma = 1/2 without drawing it: 180 = sx(1/2).
    cap_n = 1.6
    feet = []
    for num, sig in (("−4", -4.0), ("−2", -2.0), ("1", 1.0)):
        rr, _ = set_text(num, 0.0, 0.0, cap_n, 0.0)
        bx0, by0, bx1, by1 = ink_box(rr)
        ox = sx(sig) - (bx0 + bx1) / 2.0
        oy = 28.0 - cap_n / 2.0
        rr = [[(x + ox, y + oy) for x, y in r] for r in rr]
        assert all(abs(x - X0) > 0.5 for r in rr for x, _ in r), "numeral on the column"
        feet.append((num, round(sx(sig), 3), round(min_clearance(rr, field), 3)))
        T += rr
    REPORT["feet"] = feet

    # bottom band, below the real axis, on the same two flush-left axes as
    # everything else: x = 15 (under the comb) and x = X_TXT (the right column)
    cap_c = 2.2
    tr_c = cap_c * 0.1
    lead_c = cap_c * 1.8
    y1 = 23.0
    for i, ln in enumerate(["UPPER HALF-PLANE, 0 ≤ T ≤ 97.35. 28 ZEROS.",
                            "ONE SCALE ON BOTH AXES: 3.45 MM PER UNIT."]):
        T += set_text(ln, X_L, y1 - i * lead_c, cap_c, tr_c)[0]
    REPORT["bl_caption_right_mm"] = X_L + max(
        text_width(t, cap_c, tr_c) for t in ["UPPER HALF-PLANE, 0 ≤ T ≤ 97.35. 28 ZEROS.",
                                            "ONE SCALE ON BOTH AXES: 3.45 MM PER UNIT."])
    for i, ln in enumerate(["VERIFIED TO T = 3·10¹²", "(PLATT-TRUDGIAN 2021).", "NOT PROVED."]):
        assert text_width(ln, cap_c, tr_c) <= X_R - X_TXT
        T += set_text(ln, X_TXT, y1 - i * lead_c, cap_c, tr_c)[0]
    assert y1 - 2 * lead_c >= SHEET[1] - 1e-9
    L["text"] = order_runs(T)  # r03: bottom-up nearest-end order, like the field layers
    return L


def riemann_two_instructions(rng: SeededRNG, bounds, colors: int = 4) -> List[GCodeCommand]:
    """The X-ray of zeta as a LeWitt instruction drawing.

    Deterministic: every mark is exact data; ``rng`` is accepted for the
    contract and deliberately unused (nothing on the sheet is random).
    """
    _ = rng
    fit = Fit(bounds)
    L = build_layers()
    pens = _pen_map(colors)
    out: List[GCodeCommand] = []
    for layer in LAYERS:
        f = 1500 if layer == "red" else 2000
        for r in L[layer]:
            out += _poly(fit.run(r), color=pens[layer], f=f)
    return out


if __name__ == "__main__":  # quick self-report
    L = build_layers()
    for k, v in L.items():
        print(k, len(v), "strokes", round(sum(length(r) for r in v) / 1000, 2), "m")
    print("red miss", REPORT["red_centre_miss_mm_max"])
    for k in ("statement_track_mm", "label_clearance", "feet", "bl_caption_right_mm"):
        print(k, REPORT[k])
    for g, aa, ab in REPORT["arm_angles"][:6]:
        print(f"gamma {g:.4f}: A {aa:+.1f}  B {ab:+.1f}  diff {abs(aa - ab):.1f}")
