"""BIRCH AND SWINNERTON-DYER — Millennium plate 7, r01 (thesis: FAITHFUL).

An illustrator's reconstruction of ``studio/millennium-bsd/ref/reference.png``
(1122x1402 AI poster), keeping its vocabulary (a cubic curve, a few chords through
labelled rational points drawn as small open circles, a gold accent, an L-function
beside it, the equation underneath) and correcting its six lies (dossier §4,
encoding §5 "Reference -> faithful mapping").  Nothing is traced: every mark is an
exact object of the curve 37a1, y^2 + y = x^3 - x.

Reference measurements (px on the 1122x1402 raster; u = x/W, v = y/H from TOP):
    title "BIRCH-SWINNERTON-DYER", centred   u .097-.900  v .133-.163  (cap 43 px = 3.1 % H)
    tagline "geometry meets analysis"        u .294-.700  v .180-.201
    gold rule + dot ornaments                v .216 and v .838             (cut: §9.11)
    "E : y^2 + y = x^3 - x"                  u .105-.357  v .293-.320
    figure band (curve + L graph)            u .029-.975  v .330-.720
    5 blue open circles, d = 12-14 px        u .093-.349  v .408-.659  (d = 1.2 % W)
    equation "rank(E(Q)) = ord L(E,s)"       u .287-.711  v .785-.812
    lower 16 % of the sheet                  blank
    gold threads from (1,1) to the zero      u .356-.772  v .216-.838      (cut: lie 6)

Layout / truth fixes (each listed in NOTES.md):
    1. two components: a closed egg and an open branch, 29.5 mm of bare mirror between
    2. the mirror is y = -1/2; it appears only as the s-axis, inside the branch's mouth
    3. every circle is a real multiple nP, |n| <= 30 (48 in the field; P itself is gold)
    4. the three chords are the pencil through P: y = 0, y = x and the tangent y = -x
    5. L(0) = 0, L < 0 on (0,1), a transversal crossing at s = 1 in gold, 17.01 deg
       on the curve's own mm scale; no V, no axes, no arrows, no ticks
    6. gold on exactly two things: the generator P and the crossing stretch
    7. title flush-left (series grammar), ornaments cut, equation kept

Pens (``colors=5``), light -> dark, gold last:
    0  HAIR    black 0.1   the two negation steps (dashed, a reflection in y = -1/2), the s-axis
    1  CHORDS  black 0.3   the three chords of the pencil + 47 open circles
    2  TEXT    black 0.3   (same pen, own layer, no swap) all type
    3  CURVES  black 0.5   E(R) and L(E,s): the two objects of the conjecture, one weight
    4  GOLD    gold 0.7    P and the crossing at s = 1, nothing else

Entry point: ``bsd_faithful``.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction as Fr
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

HAIR, CHORDS, TEXT, CURVES, GOLD = 0, 1, 2, 3, 4
F_DRAW = 2200

# ===========================================================================
# the one mapping (encoding §4) — sheet mm, y UP from the bottom edge, A3 portrait
# ===========================================================================
S = 52.0                                   # mm per unit, x, y, s and L alike
E3, E2, E1 = -1.1071598716887676, 0.26959443640544456, 0.8375654352833231
FIELD = (15.0, 15.0, 282.0, 365.0)        # x0, y0, x1, y1


def sx(x: float) -> float:
    return 30.0 + (x - E3) * S


def sy(y: float) -> float:
    return 200.0 + (y + 0.5) * S


def to_sheet(x: float, y: float) -> Pt:
    return (sx(x), sy(y))


S0_X = sx(1.25)                            # s = 0 on the sheet (152.57)
MIRROR_Y = sy(-0.5)                        # 200.0

R_DISC = 4.0          # gold disc radius (4 rings at 1.0 mm pitch)
GAP_DISC = 0.8        # ink stops this far outside the disc
R_OPEN = 0.8          # open circle radius (1.6 mm diameter)
GAP_OPEN = 0.3        # E and chords stop this far outside each circle
N_ORBIT = 30          # +-nP, n <= 30 (n = 31 brings a pair to 1.95 mm)
GOLD_S = (0.85, 1.15)
GOLD_OFF = 0.15       # the two gold passes sit +-0.15 mm off the curve (0.3 apart)
JOINT = 0.3           # black runs this far (mm) under each end of the gold stretch


# ===========================================================================
# the arithmetic — exact group law in Fractions (dossier §1)
# ===========================================================================
def add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1), (x2, y2) = P, Q
    if x1 == x2 and y1 + y2 + 1 == 0:
        return None
    lam = (3 * x1 * x1 - 1) / (2 * y1 + 1) if x1 == x2 else (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    return (x3, -(lam * x3 + y1 - lam * x1) - 1)


def neg(Q):
    return (Q[0], -1 - Q[1])


@lru_cache(maxsize=1)
def orbit() -> Dict[int, Tuple[Fr, Fr]]:
    P = (Fr(0), Fr(0))
    out: Dict[int, Tuple[Fr, Fr]] = {}
    Q = None
    for n in range(1, N_ORBIT + 1):
        Q = add(Q, P)
        out[n] = Q
        out[-n] = neg(Q)
    for x, y in out.values():
        assert y * y + y == x ** 3 - x, "off the curve"
    return out


def in_field(p: Pt, pad: float = 0.0) -> bool:
    return FIELD[0] + pad <= p[0] <= FIELD[2] - pad and FIELD[1] + pad <= p[1] <= FIELD[3] - pad


@lru_cache(maxsize=1)
def marked() -> Dict[int, Pt]:
    """Sheet position of every multiple in the field (P included)."""
    return {n: to_sheet(float(x), float(y)) for n, (x, y) in orbit().items()
            if in_field(to_sheet(float(x), float(y)))}


def fstr(q: Fr) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


# ===========================================================================
# the real locus E(R) — two components, nothing for e2 < x < e1 (dossier §1)
# ===========================================================================
def _yy(x: np.ndarray, sign: float) -> np.ndarray:
    f = np.maximum(4 * x ** 3 - 4 * x + 1, 0.0)
    return (-1.0 + sign * np.sqrt(f)) / 2.0


def egg() -> Poly:
    """Closed oval over [e3, e2]; x = e3 + (e2-e3)(1-cos t)/2 makes the vertical tips
    arclength-uniform (y ~ sqrt(x - e_i) ~ t)."""
    t = np.linspace(0.0, math.pi, 900)
    x = E3 + (E2 - E3) * (1 - np.cos(t)) / 2
    x[0], x[-1] = E3, E2
    up = np.column_stack([x, _yy(x, +1)])
    dn = np.column_stack([x[::-1], _yy(x[::-1], -1)])
    ring = np.vstack([up, dn[1:]])
    return [to_sheet(a, b) for a, b in ring]


def branch() -> List[Poly]:
    """Open branch, x = e1 + u^2 (arclength-uniform at the vertex); two arms from the
    vertex outward, each clipped exactly to the field."""
    u = np.linspace(0.0, math.sqrt(2.7 - E1), 1400)
    x = E1 + u ** 2
    arms = []
    for sign in (+1, -1):
        pts = [to_sheet(a, b) for a, b in zip(x, _yy(x, sign))]
        arms += clip(pts, Rect(*FIELD), keep="inside")
    return arms


# ===========================================================================
# the analysis — L(E,s) on [0, 2] (compute_l.py -> lcurve.json)
# ===========================================================================
@lru_cache(maxsize=1)
def lcurve() -> Tuple[np.ndarray, np.ndarray]:
    d = json.loads((HERE / "lcurve.json").read_text())
    return np.asarray(d["s"], float), np.asarray(d["L"], float)


def l_sheet(s: np.ndarray) -> np.ndarray:
    ss, LL = lcurve()
    return np.column_stack([S0_X + S * s, MIRROR_Y + S * np.interp(s, ss, LL)])


def l_runs():
    """Black before and after the gold stretch (each running JOINT mm under the gold),
    and the gold stretch itself as two offset passes, one pen-down."""
    ss, _ = lcurve()
    slope = 0.306
    ds = JOINT / (S * math.hypot(1.0, slope))
    a = np.concatenate([ss[ss < GOLD_S[0] + ds], [GOLD_S[0] + ds]])
    b = np.concatenate([[GOLD_S[1] - ds], ss[ss > GOLD_S[1] - ds]])
    black = [[tuple(p) for p in l_sheet(a)], [tuple(p) for p in l_sheet(b)]]
    g = np.concatenate([[GOLD_S[0]], ss[(ss > GOLD_S[0]) & (ss < GOLD_S[1])], [GOLD_S[1]]])
    mid = [tuple(p) for p in l_sheet(g)]
    gold = _offset(mid, +GOLD_OFF) + _offset(mid, -GOLD_OFF)[::-1]
    return black, [gold], mid


# ===========================================================================
# type — the house stroke font plus the glyphs this plate needs (authored here)
# ===========================================================================
def _small(strokes, y0: float, k: float = 0.52):
    return [[(x * k + 0.6, y * k + y0) for (x, y) in st] for st in strokes]


GLYPHS = dict(_GLYPHS)
GLYPHS.update({
    # double-struck Q: the house Q with an inner stem on the left (after the house ℝ)
    "ℚ": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0), (1, 0)],
          [(1.0, 0.0), (1.0, 6.0)], [(2.6, 1.4), (4.2, -0.4)]],
    # double-struck Z: the diagonal doubled by an exact parallel
    "ℤ": [[(0.4, 6.0), (3.6, 6.0), (0.4, 0.0), (3.6, 0.0)], [(2.7, 6.0), (0.4, 1.69)]],
    # Ш (Tate-Shafarevich)
    "Ш": [[(0.3, 6.0), (0.3, 0.0), (4.3, 0.0), (4.3, 6.0)], [(2.3, 0.0), (2.3, 6.0)]],
    "·": [[(1.8, 2.8), (2.2, 2.8)]],
    "–": [[(0.4, 3), (3.6, 3)]],
})
GLYPHS["ₛ"] = _small(GLYPHS["S"], -1.6, 0.55)
GLYPHS["₌"] = _small(GLYPHS["="], -1.6, 0.55)
GLYPHS["₁"] = _small(GLYPHS["1"], -1.6, 0.55)


def _adv(ch: str) -> float:
    """Proportional advance in 4x6 cell units (the house rule: caps 1.02, lowercase 0.55)."""
    if ch == " ":
        return 2.6
    st = GLYPHS.get(ch) or GLYPHS.get(ch.upper()) or []
    xs = [p[0] for s in st for p in s]
    if not xs:
        return 2.6
    sb = 0.55 if ch.islower() else 1.02
    if ch in "ₛ₌₁":
        sb = 0.25
    return (max(xs) - min(xs)) + 2.0 * sb


def text_width(txt: str, h: float, track: float = 0.0) -> float:
    return sum(_adv(c) for c in txt) * h / 6.0 + track * max(0, len(txt) - 1)


def set_text(txt: str, x: float, y: float, h: float, track: float = 0.0) -> List[Poly]:
    """Left-baseline stroke text -> polylines."""
    sc = h / 6.0
    runs: List[Poly] = []
    cx = x
    for ch in txt:
        st = GLYPHS.get(ch)
        if st is None:
            st = GLYPHS.get(ch.upper(), [])
        xs = [p[0] for s in st for p in s]
        sb = 0.25 if ch in "ₛ₌₁" else (0.55 if ch.islower() else 1.02)
        x_off = -min(xs) + sb if xs else 0.0
        runs += chain([[(cx + (gx + x_off) * sc, y + gy * sc) for gx, gy in s] for s in st])
        cx += _adv(ch) * sc + track
    return runs


def set_right(txt, x_right, y, h, track=0.0):
    return set_text(txt, x_right - text_width(txt, h, track), y, h, track)


def set_centre(txt, xc, y, h, track=0.0):
    return set_text(txt, xc - text_width(txt, h, track) / 2, y, h, track)


def heavy(runs: List[Poly], weight: float, tip: float = 0.3) -> List[Poly]:
    """Weight a hairline glyph run into parallel passes, linked into one pen-down."""
    if weight <= 0:
        return runs
    n = max(2, int(round(weight / tip)) + 1)
    out = []
    for r in runs:
        band: Poly = []
        for k in range(n):
            d = -weight / 2 + weight * k / (n - 1)
            q = _offset(r, d)
            band += q if k % 2 == 0 else q[::-1]
        out.append(band)
    return out


def chain(runs: List[Poly], tol: float = 0.02) -> List[Poly]:
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


def _offset(pts: Sequence[Pt], d: float) -> Poly:
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


def bbox(runs: Sequence[Poly]) -> Tuple[float, float, float, float]:
    xs = [p[0] for r in runs for p in r]
    ys = [p[1] for r in runs for p in r]
    return min(xs), min(ys), max(xs), max(ys)


# ===========================================================================
# small helpers
# ===========================================================================
def circle_poly(c: Pt, r: float, n: int = 28, phase: float = 0.0) -> Poly:
    return [(c[0] + r * math.cos(phase + 2 * math.pi * k / n),
             c[1] + r * math.sin(phase + 2 * math.pi * k / n)) for k in range(n + 1)]


def dashed(a: Pt, b: Pt, dash: float, gap: float) -> List[Poly]:
    L = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    n = max(1, int((L + gap) // (dash + gap)))
    rest = L - (n * dash + (n - 1) * gap)
    t = rest / 2
    out = []
    for _ in range(n):
        out.append([(a[0] + ux * t, a[1] + uy * t), (a[0] + ux * (t + dash), a[1] + uy * (t + dash))])
        t += dash + gap
    return out


def _plen(p: Sequence[Pt]) -> float:
    return sum(math.dist(a, b) for a, b in zip(p, p[1:]))


def cut_all(polys: Sequence[Poly], regions, min_len: float = 0.2) -> List[Poly]:
    out = list(polys)
    for reg in regions:
        nxt: List[Poly] = []
        for p in out:
            nxt += clip(p, reg, keep="outside")
        out = nxt
    return [p for p in out if _plen(p) > min_len]


# ===========================================================================
# the plate
# ===========================================================================
TANGENT_SEP = 0.9     # the tangent starts where it has left the egg by this much (mm)


def _tangent_start(p: Pt, q: Pt) -> Pt:
    """The tangent at P kisses the egg (separation ~ kappa t^2 / 2): within ~11 mm of P the
    two lines would run closer than the 0.8 mm floor.  The curve itself carries the contact;
    the tangent line begins where it has left the egg by TANGENT_SEP (bisection)."""
    eg = np.asarray(egg())
    u = np.subtract(q, p) / math.dist(p, q)
    sep = lambda t: float(np.min(np.hypot(*(eg - (np.asarray(p) + u * t)).T)))  # noqa: E731
    lo, hi = 0.0, 30.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sep(mid) < TANGENT_SEP else (lo, mid)
    return (p[0] + u[0] * hi, p[1] + u[1] * hi)


def construction():
    """The reference's construction, corrected: three chords of the pencil through P
    and two negation steps (encoding §4)."""
    O = orbit()
    pt = lambda n: to_sheet(float(O[n][0]), float(O[n][1]))  # noqa: E731
    chords = [
        [_tangent_start(pt(1), pt(-2)), pt(-2)],   # tangent at P: y = -x, meets E again at -2P
        [pt(-3), pt(2)],            # y = 0 :  -3P, P, 2P
        [pt(3), pt(-4)],            # y = x :   3P, P, -4P
    ]
    negations = [(pt(-2), pt(2)),   # x = 1 :  -2P -> 2P
                 (pt(-3), pt(3))]   # x = -1:  -3P -> 3P
    return chords, negations


# point labels: (n, text, anchor side, dx, dy) — every label sits off the curve and
# out of the gap e2 < x < e1; the side is the one away from P where that is free.
LABELS = [
    (1, "P (0,0)", "c", -1.0, 8.4),
    (2, "2P (1,0)", "l", 2.3, -0.9),
    (-2, "-2P (1,-1)", "l", 2.3, -0.9),
    (3, "3P (-1,-1)", "r", -1.4, -5.2),
    (-3, "-3P (-1,0)", "r", -2.6, 2.6),
    (-4, "-4P (2,2)", "l", 2.3, -0.9),
    (4, "4P (2,-3)", "l", 2.3, -0.9),
    (5, "5P (1/4,-5/8)", "r", -2.3, -0.9),
]
H_LABEL = 1.8


def build_labels():
    M = marked()
    runs: List[Poly] = []
    boxes = []
    for n, txt, side, dx, dy in LABELS:
        x, y = M[n]
        if side == "l":
            r = set_text(txt, x + dx, y + dy, H_LABEL, 0.25)
        elif side == "r":
            r = set_right(txt, x + dx, y + dy, H_LABEL, 0.25)
        else:
            r = set_centre(txt, x + dx, y + dy, H_LABEL, 0.25)
        runs += r
        boxes.append(bbox(r))
    return runs, boxes


XR = 215.0          # the analysis column: flush-left under the L-curve
EQ_Y = 121.8        # the equation's baseline (29 x 4.2)
E_Y = 314.0         # the curve's name, set just above the figure (as in the reference)
H_EQ = 5.5
H_SMALL = 1.8
LEAD = 4.2


def _count_circles() -> int:
    return sum(1 for n in marked() if n != 1)


def build_text():
    O = orbit()
    T: List[Poly] = []
    # --- title band (series grammar: spaced caps, flush-left, statement) -----------
    T += heavy(set_text("BIRCH AND SWINNERTON-DYER", 15.0, 395.0, 8.0, track=1.3), 0.6, tip=0.2)
    T += set_text("GEOMETRY MEETS ANALYSIS: THE RANK OF E(ℚ) IS", 15.0, 381.0, 2.5, track=0.55)
    T += set_text("THE ORDER OF THE ZERO OF L(E,S) AT S = 1.", 15.0, 381.0 - 1.8 * 2.5 - 1.3,
                  2.5, track=0.55)
    T += set_right("MILLENNIUM PRIZE PROBLEMS  7 / 7", 282.0, 381.0, 2.0, 0.4)
    T += set_right("CLAY MATHEMATICS INSTITUTE, 2000", 282.0, 376.5, 2.0, 0.4)

    # --- upper-left: the curve's name (the reference's label, kept) ----------------
    T += set_text("E : Y² + Y = X³ − X", 15.0, E_Y, 4.0, track=0.5)
    T += set_text("CREMONA 37A1  ·  CONDUCTOR 37  ·  E(ℚ) = ℤP", 15.0, E_Y - 7.5, H_SMALL, 0.35)
    key = ["ONE GENERATOR, P = (0,0), IN GOLD. EVERY OTHER",
           "RATIONAL POINT IS A MULTIPLE NP, BUILT BY LINES:",
           "THE LINE THROUGH P AND NP MEETS E ONCE MORE,",
           "AT -(N+1)P. REFLECT IN Y = -1/2 FOR (N+1)P.",
           f"OPEN CIRCLES: EVERY NP, N = -30 ... 30, ON THE SHEET ({_count_circles()}).",
           "ODD N FALL ON THE OVAL, EVEN N ON THE OPEN BRANCH."]
    y = E_Y - 20.0
    for ln in key:
        T += set_text(ln, 15.0, y, H_SMALL, 0.3)
        y -= LEAD

    # --- under the figure: the equation, then the orbit going on ---------------------
    eq_y = EQ_Y
    T += heavy(set_text("RANK E(ℚ) = ORD", 15.0, eq_y, H_EQ, 0.7), 0.35, tip=0.2)
    xo = 15.0 + text_width("RANK E(ℚ) = ORD", H_EQ, 0.7) + 0.7
    T += set_text("S=1", xo, eq_y - 2.8, 2.5, 0.3)
    xl = xo + text_width("S=1", 2.5, 0.3) + 2.6
    T += heavy(set_text("L(E,S)", xl, eq_y, H_EQ, 0.7), 0.35, tip=0.2)

    lines = []
    cur = ""
    for n in range(6, 15):
        x, yv = O[n]
        item = f"{n}P = ({fstr(x)}, {fstr(yv)})"
        if cur and text_width(cur + "    " + item, H_SMALL, 0.3) > 118:
            lines.append(cur)
            cur = item
        else:
            cur = item if not cur else cur + "    " + item
    lines.append(cur + "    ...")
    y = eq_y - 2 * LEAD - 1.0
    for ln in lines:
        T += set_text(ln, 15.0, y, H_SMALL, 0.3)
        y -= LEAD

    # --- at the crossing ---------------------------------------------------------------
    xc = S0_X + S * 1.0
    T += set_centre("S = 1", xc, 193.0, 1.6, 0.25)
    T += set_centre("0", S0_X, 193.0, 1.6, 0.25)
    T += set_centre("2", S0_X + 2 * S, 193.0, 1.6, 0.25)
    T += set_text("L(E,S)", S0_X + 2 * S + 2.0, MIRROR_Y + S * lcurve()[1][-1] + 1.5, 2.5, 0.4)

    # --- the analysis column: the caption, the bridge, the status ------------------------
    col = ["ONE CROSSING, NOT A TOUCH: ORDER 1.",
           "THE S-AXIS IS E'S MIRROR Y = -1/2.",
           "ONE SCALE FOR BOTH: 17.0 DEG AT S = 1.",
           "",
           "L'(E,1) = 0.30600",
           "        = 5.98692 × 0.05111",
           "        = REAL PERIOD × HEIGHT OF P",
           "(SHA = 1, TAMAGAWA = 1, NO TORSION)",
           "",
           "THE SLOPE OF THE GOLD CROSSING IS",
           "THE REAL PERIOD OF E TIMES THE",
           "HEIGHT OF P: HOW FAST THE DIGITS OF",
           "NP GROW: LOG H(X(NP)) ~ 0.0511 N².",
           "",
           "PROVED FOR THIS CURVE:",
           "GROSS-ZAGIER 1986, KOLYVAGIN 1988.",
           "OPEN IN GENERAL."]
    y = 180.0
    for ln in col:
        if ln:
            assert XR + text_width(ln, H_SMALL, 0.3) <= 282.0, ln
            T += set_text(ln, XR, y, H_SMALL, 0.3)
        y -= LEAD
    return T


def build_plate():
    M = marked()
    P = M[1]
    disc_keep = Circle(P[0], P[1], R_DISC + GAP_DISC)
    circ_keep = [Circle(c[0], c[1], R_OPEN + GAP_OPEN) for n, c in M.items() if n != 1]

    labels, lboxes = build_labels()
    halos = [Rect(b[0] - 1.0, b[1] - 1.0, b[2] + 1.0, b[3] + 1.0) for b in lboxes]

    chords, negs = construction()
    chord_runs = cut_all(chords, [disc_keep] + circ_keep + halos, min_len=1.5)
    circles = [circle_poly(c, R_OPEN) for n, c in M.items() if n != 1]

    hair: List[Poly] = []
    for a, b in negs:
        hair += dashed(a, b, 1.2, 1.2)
    hair = cut_all(hair, circ_keep + halos)
    hair.append([(S0_X, MIRROR_Y), (S0_X + 2 * S, MIRROR_Y)])      # s-axis, s in [0, 2]

    curves = cut_all([egg()] + branch(), [disc_keep] + circ_keep)
    l_black, l_gold, l_mid = l_runs()
    curves += l_black

    gold: List[Poly] = []
    for k in range(1, 5):
        gold.append(circle_poly(P, R_DISC * k / 4, n=16 + 8 * k))
    gold.append(circle_poly(P, 0.25, n=8))
    gold += l_gold

    text = build_text() + labels
    return dict(hair=hair, chords=chord_runs, circles=circles, text=text,
                curves=curves, gold=gold, l_mid=l_mid)


def _nn_order(polys: List[Poly], start: Pt = (15.0, 15.0)) -> List[Poly]:
    """Greedy nearest-end ordering (either direction) — short travels, batchable."""
    left = list(polys)
    out: List[Poly] = []
    cur = start
    while left:
        best = min(range(len(left)), key=lambda i: min(math.dist(cur, left[i][0]),
                                                      math.dist(cur, left[i][-1])))
        p = left.pop(best)
        if math.dist(cur, p[-1]) < math.dist(cur, p[0]):
            p = p[::-1]
        out.append(p)
        cur = p[-1]
    return out


def bsd_faithful(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    def pen(i: int) -> Optional[int]:
        return i if colors >= 5 else min(i, max(colors - 1, 0))

    L = build_plate()
    out: List[GCodeCommand] = []
    for p in _nn_order(L["hair"]):
        out += _poly(p, color=pen(HAIR), f=F_DRAW)
    for p in _nn_order(L["chords"] + L["circles"]):
        out += _poly(p, color=pen(CHORDS), f=F_DRAW)
    for p in L["text"]:
        out += _poly(p, color=pen(TEXT), f=F_DRAW)
    for p in _nn_order(L["curves"]):
        out += _poly(p, color=pen(CURVES), f=F_DRAW)
    for p in L["gold"]:
        out += _poly(p, color=pen(GOLD), f=F_DRAW)
    return out
