"""RIEMANN HYPOTHESIS — Millennium plate 1, r01 (thesis: FAITHFUL).

An illustrator's reconstruction of ``studio/millennium-riemann/ref/reference.png``
(1024x1536 AI poster), with its architecture MEASURED and its four lies corrected
(encoding.md §5F).  The reference's streamline "field" becomes the X-RAY of ζ
(Arias de Reyna 2003): the two zero sets Re ζ(s) = 0 and Im ζ(s) = 0, computed with
mpmath on a 0.05-unit grid (``compute_faithful.py`` -> ``data/xray_faithful.json``).
Nothing in the field is drawn by hand; every meeting of the two families above or
below the real axis is a nontrivial zero, and those alone are red.

Reference measurements (px on the 1024x1536 raster; u = x/1024, v = y/1536 from TOP):
    title "RIEMANN / HYPOTHESIS"   x  35..325  y  30..112     u .034-.317  v .020-.073
    short rule under title         x  35.. 86  y 137          v .089
    statement (2 lines caps)       x  35..272  y 160..193     v .104-.126  (cap 10 px)
    red critical line              x 512.5     y  41..1371    u .5005      v .027-.893
    23 blue rings on the line      rows 121..645 and 822..1241 (evenly laddered, down to t~1)
    real axis (arrowed)            y 728                      v .474
    |ζ| colour bar                 x  45.. 70  y 862..1102    (cut: lie 8)
    "DETAIL NEAR ZEROS" inset      x 739..935  y 872..1162    (cut: its "32.0" is false)
    "Primes:" number line          y 1405, numerals y 1440    v .915 / .938
    tagline, centred bottom        y 1491                     v .971
    ink, left half vs right half   0.99 : 1  (the reference is a left-right mirror: lie 1)

Layout fixes against the reference (each one is a correction, listed in NOTES.md):
    1. top-bottom mirror only (conjugate symmetry); the right half is ζ's own silence
    2. the critical line is not drawn: two red register ticks outside the field
    3. 20 red crossings at the true ±γ_n; the column is empty for |t| < 14.1347
    4. axes, arrows, colour bar, inset: cut; the real axis survives as the hairline it is
    5. all type moves to the right void, flush-left on ζ's own ruling grid t = kπ/ln 2
    6. "ζ(s)=0 ⇔ Re s=½" becomes "ζ(ρ)=0, 0<Re ρ<1 ⇒ Re ρ=½ ?"
    7. the "Primes:" dotted line becomes ψ₁₀₀(x) − x: a cliff at every prime AND prime power

Pens (``colors=4``), layer order light -> dark, red last:
    0  B · HAIRLINE  black 0.1   Im ζ = 0, the real axis included
    1  A · BLACK     black 0.3   Re ζ = 0
    2  TEXT          black 0.3   (same pen as A, own layer, no swap) type + ψ footer
    3  RED           red 0.5     the nontrivial zeros ρ_n, and the two register ticks

Entry point: ``riemann_faithful``.
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Circle, Rect, clip
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "data"

HAIR, BLACK, TEXT, RED = 0, 1, 2, 3
F_DRAW = 2200

# ===========================================================================
# the one mapping (encoding §4 / §5F) — sheet mm, y UP from the bottom edge
# ===========================================================================
SHEET_W, SHEET_H = 297.0, 420.0
S_MM = 3.0            # mm per complex-plane unit, BOTH axes (isotropic: every X is 90°)
X0 = 148.5            # sheet x of σ = ½  (the sheet centre, where the reference put its red line)
Y_AXIS = 210.0        # sheet y of t = 0
T_CROP = 51.37        # mid-gap between γ10 = 49.774 and γ11 = 52.970 -> 20 crossings
FIELD_X = (15.0, 282.0)
R_RED = 2.0           # mm: red substitution radius (0.38 x min gap γ9-γ10 = 5.31 mm)
JOINT = 0.2           # mm: red overlaps its black/hairline continuation by this much
SPLIT_MM = 300.0      # strokes longer than this split at their tip (batch boundary)
RDP_TOL = 0.02        # mm: polyline decimation, far below the 0.1 mm nib


def to_sheet(sig: float, t: float) -> Pt:
    return (X0 + S_MM * (sig - 0.5), Y_AXIS + S_MM * t)


FIELD_Y = (Y_AXIS - S_MM * T_CROP, Y_AXIS + S_MM * T_CROP)   # 55.89 .. 364.11


# ===========================================================================
# data
# ===========================================================================
@lru_cache(maxsize=1)
def _xray() -> Dict[str, list]:
    return json.loads((DATA / "xray_faithful.json").read_text())


@lru_cache(maxsize=1)
def _zeros() -> List[float]:
    return [z["gamma"] for z in json.loads((DATA / "zeros.json").read_text())["zeros"]]


def _rdp(pts: np.ndarray, tol: float) -> np.ndarray:
    """Ramer-Douglas-Peucker, iterative. Deviation <= tol (mm), endpoints kept."""
    n = len(pts)
    if n < 3:
        return pts
    keep = np.zeros(n, bool)
    keep[0] = keep[-1] = True
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = pts[i], pts[j]
        d = b - a
        L = math.hypot(d[0], d[1])
        seg = pts[i + 1:j] - a
        if L < 1e-12:
            dist = np.hypot(seg[:, 0], seg[:, 1])
        else:
            dist = np.abs(seg[:, 0] * d[1] - seg[:, 1] * d[0]) / L
        k = int(np.argmax(dist))
        if dist[k] > tol:
            m = i + 1 + k
            keep[m] = True
            stack.append((i, m))
            stack.append((m, j))
    return pts[keep]


def _plen(p: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))


def _field_polys(key: str) -> List[Poly]:
    """Map a zero set to sheet mm and crop it EXACTLY to the field rectangle."""
    frame = Rect(FIELD_X[0], FIELD_Y[0], FIELD_X[1], FIELD_Y[1])
    out: List[Poly] = []
    for raw in _xray()[key]:
        a = np.asarray(raw, float)
        sheet = np.column_stack([X0 + S_MM * (a[:, 0] - 0.5), Y_AXIS + S_MM * a[:, 1]])
        sheet = _rdp(sheet, RDP_TOL)
        for piece in clip([tuple(p) for p in sheet], frame, keep="inside"):
            if _plen(piece) > 0.5:
                out.append(piece)
    return out


def _nearest(poly: Poly, c: Pt) -> Tuple[float, int]:
    """Exact point-to-polyline distance (to SEGMENTS, not vertices) and the segment index."""
    a = np.asarray(poly, float)
    p0, p1 = a[:-1], a[1:]
    d = p1 - p0
    L2 = np.maximum((d ** 2).sum(1), 1e-18)
    u = np.clip(((c[0] - p0[:, 0]) * d[:, 0] + (c[1] - p0[:, 1]) * d[:, 1]) / L2, 0.0, 1.0)
    q = p0 + d * u[:, None]
    dist = np.hypot(q[:, 0] - c[0], q[:, 1] - c[1])
    k = int(np.argmin(dist))
    return float(dist[k]), k


# ===========================================================================
# the X-ray, with the red substitution at every ρ_n (encoding §4 "red crossing")
# ===========================================================================
def build_field():
    A = _field_polys("re0")
    B = _field_polys("im0")
    gam = [g for g in _zeros() if g < T_CROP]
    centres = [to_sheet(0.5, s * g) for g in gam for s in (1, -1)]
    red: List[Poly] = []
    report = []
    for fam in (A, B):
        for c in centres:
            # the branch THROUGH ρ: the polyline that passes nearest the exact centre
            dists = [_nearest(p, c)[0] for p in fam]
            i = int(np.argmin(dists))
            report.append(dists[i])
            p = fam.pop(i)
            inner = clip(p, Circle(c[0], c[1], R_RED), keep="inside")
            # keep only the inside piece that actually passes through the centre
            inner.sort(key=lambda q: _nearest(q, c)[0])
            red.append(inner[0])
            fam.extend(clip(p, Circle(c[0], c[1], R_RED - JOINT), keep="outside"))
    return A, B, red, centres, max(report)


def _split_long(polys: List[Poly]) -> List[Poly]:
    """Split any stroke longer than SPLIT_MM at the vertex nearest the column (its tip),
    so every stroke can be a batch boundary (DESIGN_RUBRIC § PLOTTABLE)."""
    out: List[Poly] = []
    work = list(polys)
    while work:
        p = work.pop()
        if _plen(p) <= SPLIT_MM or len(p) < 4:
            out.append(p)
            continue
        xs = [q[0] for q in p]
        k = int(np.argmax(xs[1:-1])) + 1
        if k <= 1 or k >= len(p) - 2:
            k = len(p) // 2
        work.append(p[: k + 1])
        work.append(p[k:])
    return out


def _order(polys: List[Poly]) -> List[Poly]:
    """Bottom -> top by the y of the left end, alternating direction (boustrophedon)."""
    def key(p):
        a, b = p[0], p[-1]
        return min((a, b), key=lambda q: q[0])[1]
    ps = sorted(polys, key=key)
    out = []
    for i, p in enumerate(ps):
        left_first = p[0][0] <= p[-1][0]
        want_left = i % 2 == 0
        out.append(p if left_first == want_left else p[::-1])
    return out


# ===========================================================================
# type — the house stroke font plus the glyphs this plate needs (authored here)
# ===========================================================================
def _small(strokes, y0: float, k: float = 0.52):
    return [[(x * k + 0.6, y * k + y0) for (x, y) in st] for st in strokes]


GLYPHS = dict(_GLYPHS)
GLYPHS.update({
    # ζ: top bar, spine sweeping down-left, belly along the baseline, descender hook
    "ζ": [[(0.9, 6.0), (3.2, 6.0), (2.2, 5.0), (1.2, 3.8), (0.6, 2.6), (0.5, 1.5), (0.9, 0.6),
           (1.8, 0.15), (2.7, 0.0), (3.2, -0.5), (3.1, -1.2), (2.5, -1.6)]],
    # ρ: descending stem into a round bowl
    "ρ": [[(0.6, -1.6), (0.6, 2.0), (0.8, 3.1), (1.4, 3.8), (2.2, 4.0), (2.9, 3.6), (3.3, 2.8),
           (3.3, 1.2), (2.9, 0.4), (2.2, 0.0), (1.4, 0.1), (0.7, 0.7)]],
    # ψ: cup on a long stem
    "ψ": [[(0.3, 4.0), (0.35, 2.3), (0.8, 0.9), (1.8, 0.3), (2.8, 0.9), (3.25, 2.3), (3.3, 4.0)],
          [(1.8, 5.8), (1.8, -1.6)]],
    # γ
    "γ": [[(0.3, 4.0), (0.9, 3.8), (1.9, 0.2)],
          [(3.5, 4.0), (1.9, 0.2), (1.6, -1.0), (1.9, -1.6), (2.2, -1.0), (1.9, 0.2)]],
    "½": [[(0.3, 4.9), (0.9, 5.6), (0.9, 3.2)], [(3.6, 5.9), (0.4, 0.1)],
          [(2.0, 2.5), (2.5, 2.9), (3.2, 2.9), (3.6, 2.5), (3.6, 2.0), (2.0, 0.2), (3.8, 0.2)]],
    "⇒": [[(0.3, 3.9), (2.9, 3.9)], [(0.3, 2.1), (2.9, 2.1)], [(2.1, 5.0), (3.8, 3.0), (2.1, 1.0)]],
    "–": [[(0.4, 3), (3.6, 3)]],
    "?": [[(0.6, 4.7), (1.3, 5.6), (2.5, 5.9), (3.4, 5.2), (3.4, 4.1), (2.0, 3.0), (2.0, 1.7)],
          [(1.8, 0.1), (2.2, 0.1)]],
    "·": [[(1.8, 2.8), (2.2, 2.8)]],
    "—": [[(0.0, 3), (4.0, 3)]],
})
GLYPHS["⁻"] = _small(GLYPHS["−"], 3.1)
GLYPHS["ˢ"] = _small(GLYPHS["s"], 3.1)
GLYPHS["ₙ"] = _small(GLYPHS["n"], -1.3)
GLYPHS["⁰"] = _small(GLYPHS["0"], 3.1)


def _adv(ch: str) -> float:
    """Proportional advance in 4x6 cell units (the house rule: caps 1.02, lowercase 0.55)."""
    if ch == " ":
        return 2.6
    st = GLYPHS.get(ch) or GLYPHS.get(ch.upper()) or []
    xs = [p[0] for s in st for p in s]
    if not xs:
        return 2.6
    sb = 0.55 if ch.islower() else 1.02
    return (max(xs) - min(xs)) + 2.0 * sb


def text_width(txt: str, h: float, track: float = 0.0) -> float:
    return sum(_adv(c) for c in txt) * h / 6.0 + track * max(0, len(txt) - 1)


def set_text(txt: str, x: float, y: float, h: float, track: float = 0.0) -> List[Poly]:
    """Left-baseline stroke text -> polylines (so the layer can be ordered and batched)."""
    sc = h / 6.0
    runs: List[Poly] = []
    cx = x
    for ch in txt:
        st = GLYPHS.get(ch)
        if st is None:
            st = GLYPHS.get(ch.upper(), [])
        xs = [p[0] for s in st for p in s]
        x_off = -min(xs) + (0.55 if ch.islower() else 1.02) if xs else 0.0
        runs += chain([[(cx + (gx + x_off) * sc, y + gy * sc) for gx, gy in s] for s in st])
        cx += _adv(ch) * sc + track
    return runs


def heavy(runs: List[Poly], weight: float, tip: float = 0.3) -> List[Poly]:
    """Weight a hairline glyph run into parallel passes (display type as mass)."""
    if weight <= 0:
        return runs
    n = max(2, int(round(weight / tip)) + 1)
    out = []
    for r in runs:
        # the passes of one glyph stroke are ONE pen-down run: pass k+1 is drawn back along
        # pass k, linked by a weight/(n-1) step inside the stroke's own band (fewer pen cycles)
        band: Poly = []
        for k in range(n):
            d = -weight / 2 + weight * k / (n - 1)
            q = _offset(r, d)
            band += q if k % 2 == 0 else q[::-1]
        out.append(band)
    return out


def chain(runs: List[Poly], tol: float = 0.02) -> List[Poly]:
    """Join runs whose ends meet (either direction) so a glyph is as few pen-downs as it can be."""
    runs = [list(r) for r in runs]
    out: List[Poly] = []
    while runs:
        cur = runs.pop(0)
        grown = True
        while grown:
            grown = False
            for i, r in enumerate(runs):
                if math.dist(cur[-1], r[0]) < tol:
                    cur += r[1:]
                elif math.dist(cur[-1], r[-1]) < tol:
                    cur += r[::-1][1:]
                elif math.dist(cur[0], r[-1]) < tol:
                    cur = r + cur[1:]
                elif math.dist(cur[0], r[0]) < tol:
                    cur = r[::-1] + cur[1:]
                else:
                    continue
                runs.pop(i)
                grown = True
                break
        out.append(cur)
    return out


def _offset(pts: Poly, d: float) -> Poly:
    n = len(pts)
    if n < 2 or abs(d) < 1e-9:
        return list(pts)
    out = []
    for i, (px, py) in enumerate(pts):
        nx = ny = 0.0
        for a, b in ((i - 1, i), (i, i + 1)):
            if a < 0 or b >= n:
                continue
            dx, dy = pts[b][0] - pts[a][0], pts[b][1] - pts[a][1]
            L = math.hypot(dx, dy)
            if L > 1e-9:
                nx -= dy / L
                ny += dx / L
        L = math.hypot(nx, ny)
        out.append((px + d * nx / L, py + d * ny / L) if L > 1e-9 else (px, py))
    return out


# ===========================================================================
# footer — the explicit formula, ψ_100(x) − x (dossier §1, check #10)
# ===========================================================================
PSI_X = (1.5, 32.5)
PSI_BAND = (24.0, 41.0)      # sheet y of the curve's band


def psi_curve(n_zeros: int = 100):
    g = np.asarray(_zeros()[:n_zeros])
    rho = 0.5 + 1j * g
    x = np.exp(np.linspace(math.log(PSI_X[0]), math.log(PSI_X[1]), 9000))
    xr = x[:, None] ** rho[None, :]
    wave = -2.0 * np.real(xr / rho[None, :]).sum(1)
    y = wave - math.log(2 * math.pi) - 0.5 * np.log(1 - x ** -2.0)
    return x, y      # this IS ψ_N(x) − x


def footer():
    x, y = psi_curve()
    kx = (FIELD_X[1] - FIELD_X[0]) / (PSI_X[1] - PSI_X[0])
    lo, hi = float(y.min()), float(y.max())
    ky = (PSI_BAND[1] - PSI_BAND[0]) / (hi - lo)
    pts = np.column_stack([FIELD_X[0] + kx * (x - PSI_X[0]), PSI_BAND[0] + ky * (y - lo)])
    curve = [tuple(p) for p in _rdp(pts, RDP_TOL)]
    stats = {"lo": lo, "hi": hi, "mm_per_unit_x": kx, "mm_per_unit_y": ky,
             "psi_10_5": float(np.interp(10.5, x, y) + 10.5)}
    runs: List[Poly] = [curve]
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    powers = [4, 8, 9, 16, 25, 27, 32]
    for n in primes + powers:
        h = 2.2 if n in primes else 1.6
        s = str(n)
        cx = FIELD_X[0] + kx * (n - PSI_X[0])
        runs += set_text(s, cx - text_width(s, h) / 2, 16.0, h)
    return runs, stats


# ===========================================================================
# the plate
# ===========================================================================
def _ruling_heights(B: List[Poly], x_at: float) -> List[float]:
    ys = []
    for p in B:
        for a, b in zip(p, p[1:]):
            if (a[0] - x_at) * (b[0] - x_at) <= 0 and a[0] != b[0]:
                t = (x_at - a[0]) / (b[0] - a[0])
                ys.append(a[1] + t * (b[1] - a[1]))
    return sorted(ys)


def build_text(B: List[Poly]):
    T: List[Poly] = []
    # --- title band (reference: title top-left, short rule, statement) ---------
    T += heavy(set_text("RIEMANN HYPOTHESIS", 15.0, 395.0, 8.0, track=1.6), 0.6, tip=0.2)
    T.append([(15.0, 389.0), (21.0, 389.0)])
    T += set_text("ALL NONTRIVIAL ZEROS LIE ON THE CRITICAL LINE RE S = ½.",
                  15.0, 381.0, 2.5, track=0.55)
    # --- corner caption, top right, on the text column ------------------------
    XC = 190.0
    T += set_text("MILLENNIUM PRIZE PROBLEMS  1 / 7", XC, 399.0, 2.2, track=0.45)
    T += set_text("CLAY MATHEMATICS INSTITUTE, 2000", XC, 394.0, 2.2, track=0.45)

    # --- right void: type sits BETWEEN ζ's own rulings t = kπ/ln 2 --------------
    rul = _ruling_heights(B, XC - 2.0)
    up = [y for y in rul if y > Y_AXIS + 1]
    dn = [y for y in rul if y < Y_AXIS - 1][::-1]

    def band(ys, k):          # the k-th band away from the axis: (lower ruling, upper ruling)
        a, b = ys[k], ys[k + 1]
        return (min(a, b), max(a, b))

    def block(lines, bnd, h, lead, track):
        lo, hi = bnd
        tot = h + lead * (len(lines) - 1)
        y = (lo + hi) / 2 + tot / 2 - h
        out = []
        for ln in lines:
            out += set_text(ln, XC, y, h, track)
            y -= lead
        return out

    # upper cluster: the claim and its object; lower cluster: the instruction (LeWitt's
    # wall label, one instruction per band) and the status.  The bands next to the real
    # axis stay empty on purpose: the widest silence sits beside the zero-free stretch.
    T += block(["THE ZEROS CHOOSE THE SEAM OF", "A PICTURE THAT IS NOT SYMMETRIC."],
               band(up, len(up) - 3), 2.5, 4.6, 0.5)
    T += block(["ζ(s) = Σ n⁻ˢ = Π (1 − p⁻ˢ)⁻¹"], band(up, len(up) - 5), 3.0, 0, 0.25)
    T += block(["ζ(ρ) = 0,  0 < Re ρ < 1   ⇒   Re ρ = ½ ?"], band(up, len(up) - 6), 3.0, 0, 0.25)
    T += block(["BLACK: EVERY POINT WHERE RE ζ(S) = 0."], band(dn, len(dn) - 7), 2.2, 0, 0.45)
    T += block(["HAIRLINE: EVERY POINT WHERE IM ζ(S) = 0."], band(dn, len(dn) - 6), 2.2, 0, 0.45)
    T += block(["RED: WHERE BOTH ARE. A ZERO OF ζ."], band(dn, len(dn) - 5), 2.2, 0, 0.45)
    T += block(["VERIFIED TO T = 3·10¹²,", "PLATT–TRUDGIAN 2021. NOT PROVED."],
               band(dn, len(dn) - 3), 2.2, 4.2, 0.45)
    # --- footer ---------------------------------------------------------------
    T += set_text("ψ(x) − x FROM THE FIRST 100 ZEROS: A CLIFF OF LN P AT EVERY PRIME "
                  "AND PRIME POWER", 15.0, 45.0, 2.2, track=0.45)
    fr, stats = footer()
    T += fr
    return T, stats, rul


def riemann_faithful(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    def pen(i: int) -> Optional[int]:
        return i if colors >= 4 else min(i, max(colors - 1, 0))

    A, B, red, centres, _ = build_field()
    # red register ticks, outside the field, where Re s = ½ meets the crops
    red_ticks = [[(X0, FIELD_Y[1] + 2.0), (X0, FIELD_Y[1] + 7.0)],
                 [(X0, FIELD_Y[0] - 7.0), (X0, FIELD_Y[0] - 2.0)]]
    T, _, _ = build_text(B)

    out: List[GCodeCommand] = []
    for p in _order(_split_long(B)):
        out += _poly(p, color=pen(HAIR), f=F_DRAW)
    for p in _order(_split_long(A)):
        out += _poly(p, color=pen(BLACK), f=F_DRAW)
    for p in T:
        out += _poly(p, color=pen(TEXT), f=F_DRAW)
    for p in sorted(red + red_ticks, key=lambda q: q[0][1]):
        out += _poly(p, color=pen(RED), f=F_DRAW)
    return out
