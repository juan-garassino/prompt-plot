"""BIRCH AND SWINNERTON-DYER -- r02, thesis ABSTRACT.  Plate 7 of the MILLENNIUM series.

Lineage: François Morellet, *Répartition aléatoire de 40 000 carrés suivant les
chiffres pairs et impairs d'un annuaire de téléphone* (1961).  Order taken: a
number sequence's PARITY decides which of two families each mark joins, and the
maker adds no taste.  Here n odd puts nP on the closed oval and n even puts it on
the open branch; the root number eps = (-1)^rank = -1 forces L to cross zero.

Canon: ART DECO sheet (canon 2) carrying a Morellet system -- a stated hybrid.
Gold | black on cream.  FLAT BY DECLARATION: the 17.01 deg crossing and the
collinearity of every chord with P only hold on one isotropic flat plane.

ORDER: RADIAL seeded ORBITAL.  A pencil of lines through the one gold point
P = (0,0) of E: y^2 + y = x^3 - x (Cremona 37a1).  Chord k is the line through
P and kP; it meets E a third time at -(k+1)P.  Chords 1..60 therefore rule every
rational point +-1 .. +-61 (-P lies on the vertical through O and is correctly
unmarked).  The analysis is one line, L(E,s) on [0,2], laid on the curve's own
mirror y = -1/2 at the SAME mm scale, so its simple zero leans at 17.01 deg.

Everything is exact:
    orbit      Fractions, the chord-tangent law (computed at import, < 0.1 s)
    L(E,s)     smoothed approximate functional equation, eps = -1
               (studio/millennium-bsd/data/lfun_lib.py, checked vs LMFDB)
    E(R)       y = (-1 +- sqrt(4x^3 - 4x + 1)) / 2, tip-dense parametrisation
No randomness: ``rng`` is accepted for the contract and deliberately unused.

De-crowding is structural, in three stages along each chord (t = mm from P):
    hub LOD     chord k starts at max(7, gap / sin dtheta_kj) over lower chords j
                (gap 0.8; 1.05 against a heavy band; 1.35 for a heavy 2nd pass)
    egg lens    the egg is a curve through P, so it counts as a lower line: a
                hub->Q stretch never > 1.6 mm from the egg starts AT Q instead
                (chord 4), or is not drawn when Q is its far end (8, 24)
    clearance   engine ``suppress_parallel`` against E (<= 1.0 mm AND within
                8.1 deg of parallel): only chord 1, the tangent, which osculates
                the egg, loses ink (starts at 10.5 mm).  Ray ENDS on E are kept.

Design sheet: A3 portrait, mm, y UP from the bottom edge, drawable [15,282] x
[15,405], uniformly fitted to ``bounds``.  One scale on every axis:
    sheet_x = 30 + (x - e3) * 52      sheet_y = 200 + (y + 1/2) * 52
    L-curve:  (152.6 + 52 s, 200 + 52 L(E,s))

Pens / layers, plotted in index order (light -> dark, gold last):
    0 HAIR    black 0.1   fine chords k = 25..60; the s-axis
    1 CHORDS  black 0.3   medium chords k = 10..24 (1 pass), heavy k = 1..9 (2 passes)
    2 TEXT    black 0.3   (same pen, own layer, no swap) all type incl. the digit ziggurat
    3 CURVES  black 0.5   E(R) and L(E,s): the two objects of the conjecture
    4 GOLD    gold 0.7    P (concentric disc) and the crossing stretch s in [0.85, 1.15]

Entry point: ``bsd_zero_means_infinity``.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Circle, Rect, clip
from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.engine.material import suppress_parallel
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "data"

# ===========================================================================
# the curve and its orbit (exact)
# ===========================================================================
N_ORBIT = 61  # +-61: chords 1..60


def add(P, Q):
    """Group law on y^2 + y = x^3 - x (a1=a2=a6=0, a3=1, a4=-1). None = O."""
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


def _orbit() -> Dict[int, Tuple[Fr, Fr]]:
    P = (Fr(0), Fr(0))
    orb = {1: P}
    Q = P
    for n in range(2, N_ORBIT + 1):
        Q = add(Q, P)
        orb[n] = Q
    for n in range(1, N_ORBIT + 1):
        x, y = orb[n]
        assert y * y + y == x ** 3 - x
        orb[-n] = (x, -1 - y)
    return orb


ORB = _orbit()
assert ORB[6] == (6, 14) and ORB[8] == (Fr(21, 25), Fr(-69, 125))

# real roots of f(x) = 4x^3 - 4x + 1 (bisection to machine precision)


def _root(a: float, b: float) -> float:
    f = lambda x: 4 * x ** 3 - 4 * x + 1
    for _ in range(200):
        m = 0.5 * (a + b)
        if (f(a) < 0) == (f(m) < 0):
            a = m
        else:
            b = m
    return 0.5 * (a + b)


E3, E2, E1 = _root(-2, -1), _root(0, 0.5), _root(0.5, 1)
assert abs(E3 + 1.1071598716887676) < 1e-12

# ===========================================================================
# the design sheet (A3 portrait, mm, y up) -- encoding section 4/5
# ===========================================================================
SHEET = (15.0, 15.0, 282.0, 405.0)
S = 52.0
FIELD_TOP = 365.0
FIELD = Rect(15.0, 15.0, 282.0, FIELD_TOP)


def sx(x: float) -> float:
    return 30.0 + (x - E3) * S


def sy(y: float) -> float:
    return 200.0 + (y + 0.5) * S


PX, PY = sx(0.0), sy(0.0)  # the gold point (87.57, 226.0)
MIRROR = 200.0

# hub
DISC_R = 6.0  # 6 rings at 1.0 mm pitch (gold 0.7 nib)
DISC_RINGS = 6
EGG_BREAK = DISC_R + 0.8
HUB_R = 7.0  # chords 1..7 reach this circle
GAP_ONE = 0.8  # min ray spacing, mm
GAP_HEAVY = 1.35  # min centre spacing where a heavy (0.55 mm band) ray is involved
HEAVY_OFF = 0.25

# L(E,s)
S0_X = 152.6  # s = 0  (x_plane 1.25)
GOLD_S = (0.85, 1.15)
GOLD_HALF = 0.15

# type grid: every baseline on 28.2 + 4.2 k
LEAD = 4.2


def grid(k: int) -> float:
    return 28.2 + LEAD * k


# ===========================================================================
# polyline utils
# ===========================================================================
def length(r: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(r, r[1:]))


def rdp(pts: np.ndarray, eps: float) -> np.ndarray:
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


# ===========================================================================
# E(R): egg + branch
# ===========================================================================
def _f(x):
    return 4 * x ** 3 - 4 * x + 1


def egg_loop(n: int = 3000) -> np.ndarray:
    """Closed egg, tip-dense: x = e3 + (e2-e3)(1-cos u)/2 makes sqrt(f) smooth in u."""
    u = np.linspace(0.0, math.pi, n)
    x = E3 + (E2 - E3) * (1 - np.cos(u)) / 2.0
    r = np.sqrt(np.maximum(_f(x), 0.0)) / 2.0
    up = np.column_stack([x, -0.5 + r])
    lo = np.column_stack([x[::-1], -0.5 - r[::-1]])
    loop = np.vstack([up, lo[1:]])
    return np.column_stack([sx(loop[:, 0]), sy(loop[:, 1])])


def branch_arms(x_max: float = 9.0, n: int = 3000) -> List[np.ndarray]:
    w = np.linspace(0.0, math.sqrt(x_max - E1), n) ** 2
    x = E1 + w
    r = np.sqrt(np.maximum(_f(x), 0.0)) / 2.0
    arms = []
    for sgn in (1, -1):
        a = np.column_stack([sx(x), sy(-0.5 + sgn * r)])
        arms.append(a)
    return arms


def curve_runs() -> List[Run]:
    out: List[Run] = []
    loop = egg_loop()
    # start the closed loop at the vertex nearest P so the disc break leaves ONE stroke
    j = int(np.argmin(np.hypot(loop[:, 0] - PX, loop[:, 1] - PY)))
    loop = np.vstack([loop[j:], loop[1:j + 1]])
    for r in clip([tuple(p) for p in loop], Circle(PX, PY, EGG_BREAK), keep="outside"):
        a = rdp(np.asarray(r), 0.01)
        if length(a.tolist()) > 1.0:
            out.append([tuple(p) for p in a])
    for arm in branch_arms():
        for r in clip([tuple(p) for p in arm], FIELD, keep="inside"):
            a = rdp(np.asarray(r), 0.01)
            out.append([tuple(p) for p in a])
    return out


# ===========================================================================
# the pencil through P
# ===========================================================================
REPORT: Dict[str, object] = {}


def _dir_angle(k: int) -> float:
    """direction of chord k as a line angle in [0, 180) deg (sheet = plane, same scale)."""
    if k == 1:
        return 135.0  # tangent at P: y = -x
    q = ORB[k] if ORB[k] != ORB[1] else ORB[-(k + 1)]
    return math.degrees(math.atan2(float(q[1]), float(q[0]))) % 180.0


def chords() -> List[dict]:
    ang = {k: _dir_angle(k) for k in range(1, N_ORBIT)}
    out = []
    for k in range(1, N_ORBIT):
        a, b = ORB[k], ORB[-(k + 1)]
        # the three points are collinear with P (exact)
        assert k == 1 or a[0] * b[1] - a[1] * b[0] == 0
        # hub LOD, pairwise: chord k starts where it is GAP clear of every
        # lower-index chord j.  Against a heavy j the gap grows by that chord's
        # 0.25 mm band offset (0.8 -> 1.05), so a light ray never grazes a heavy
        # band; a heavy k's second pass keeps 1.35 (encoding section 10).
        heavy_k = k <= 9
        r1 = r2 = HUB_R
        dth = 180.0
        for j in range(1, k):
            d = min(abs(ang[k] - ang[j]), 180 - abs(ang[k] - ang[j]))
            dth = min(dth, d)
            sn = max(math.sin(math.radians(d)), 1e-9)
            g1 = GAP_ONE if (heavy_k or j > 9) else GAP_ONE + HEAVY_OFF
            r1 = max(r1, g1 / sn)
            r2 = max(r2, GAP_HEAVY / sn)
        th = math.radians(ang[k])
        u = (math.cos(th), math.sin(th))
        pts = []
        for p in (a, b):
            X, Y = sx(float(p[0])), sy(float(p[1]))
            t = (X - PX) * u[0] + (Y - PY) * u[1]
            comp = "egg" if float(p[0]) <= E2 + 1e-12 else "branch"
            pts.append((t, comp))
        tier = "heavy" if k <= 9 else ("medium" if k <= 24 else "fine")
        out.append(dict(k=k, ang=ang[k], dth=dth, r1=r1, r2=r2, u=u, pts=pts, tier=tier))
    return out


def _seg(u, t0, t1, off=0.0) -> Run:
    nx, ny = -u[1], u[0]
    return [(PX + u[0] * t0 + nx * off, PY + u[1] * t0 + ny * off),
            (PX + u[0] * t1 + nx * off, PY + u[1] * t1 + ny * off)]


def chord_pieces(c: dict, r: float) -> List[Tuple[float, float]]:
    """intervals of signed distance t along chord c that carry ink, hub hole r."""
    ts = [t for t, _ in c["pts"]]
    lo, hi = min(ts), max(ts)
    iv = []
    if lo < 0 < hi:  # Q -> P -> R
        if lo < -r:
            iv.append((lo, -r))
        if hi > r:
            iv.append((r, hi))
    elif hi <= 0:  # P at one end, both points on the negative side
        if lo < -r:
            iv.append((lo, -r))
    else:
        if hi > r:
            iv.append((r, hi))
    return iv


_GUARDS: List[Run] = []


def curve_guards() -> List[Run]:
    """E(R) as an OBSTACLE for the clearance pass: the egg loop run 1.5 times and
    both arms run far past the field, so each guard is longer than any chord and
    ``suppress_parallel`` (longest first) lets the curve claim its space before a
    chord is tested.  Never drawn."""
    if not _GUARDS:
        loop = egg_loop(1500)
        n = len(loop)
        _GUARDS.append([tuple(p) for p in np.vstack([loop, loop[1:n // 2]])])
        for arm in branch_arms(x_max=12.0, n=1500):
            keep = arm[(arm[:, 1] > -140.0) & (arm[:, 1] < 520.0)]
            _GUARDS.append([tuple(p) for p in keep])
    return _GUARDS


CLEAR = 1.0  # chord centreline >= 1.0 mm from E where they run parallel (0.5 + 0.3 nibs)
ALIGN = 0.99  # |cos| > 0.99: within 8.1 deg of parallel. Real crossings, even shallow ones, are kept.


def _t_of(c: dict, p: Pt) -> float:
    return (p[0] - PX) * c["u"][0] + (p[1] - PY) * c["u"][1]


def clear_of_curve(c: dict, iv: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Engine-native parallel suppression against the curve: drop the stretches
    of a chord that run within CLEAR of E AND within 21.6 deg of parallel to it
    (secants of a short arc hug the egg; crossings are kept, they may touch)."""
    out: List[Tuple[float, float]] = []
    guards = curve_guards()
    ends = [t for t, _ in c["pts"]]
    for (a, b) in iv:
        seg = _seg(c["u"], a, b)
        kept = suppress_parallel(guards + [seg], min_dist=CLEAR, align=ALIGN, sample=0.25,
                                 min_run_len=3.0)
        sub = sorted((min(_t_of(c, r[0]), _t_of(c, r[-1])),
                      max(_t_of(c, r[0]), _t_of(c, r[-1]))) for r in kept[len(guards):])
        if not sub:
            c.setdefault("dropped", []).append((a, b))
            continue
        # a ray END on E is a transversal meeting (the rational point's mark),
        # however shallow: it is restored.  Only the parallel run INSIDE the
        # chord -- the secant lying along the egg beside the hub -- stays cut.
        if a < sub[0][0] and any(abs(a - t) < 1e-6 for t in ends):
            sub[0] = (a, sub[0][1])
        if b > sub[-1][1] and any(abs(b - t) < 1e-6 for t in ends):
            sub[-1] = (sub[-1][0], b)
        # a break shorter than 3 mm reads as a pen fault, not as clearance: close it
        merged = [sub[0]]
        for lo, hi in sub[1:]:
            if lo - merged[-1][1] < 3.0:
                merged[-1] = (merged[-1][0], hi)
            else:
                merged.append((lo, hi))
        out += merged
    return out


LENS = 1.6  # mm: a hub->Q stretch never farther than this from the egg is a lens
_EGG: List[np.ndarray] = []


def lens_rule(c: dict, iv: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """The hub LOD, continued along the egg.  The egg is itself a curve through P
    (chord 1 is its tangent there), so it counts as a lower-index line.  If the
    stretch from the hub end of a piece to the egg point Q on it never gets more
    than LENS from the egg, it would only double the egg's line.  The ray then
    starts AT Q, on the curve, where its rational point is; if Q is the piece's
    far end the piece is not drawn (Q joins the points hidden by the hub LOD)."""
    if not _EGG:
        _EGG.append(egg_loop(4000))
    egg = _EGG[0]
    out = []
    for (a, b) in iv:
        h = a if abs(a) < abs(b) else b
        o = b if h == a else a
        new_h = h
        for t, comp in c["pts"]:
            if comp != "egg" or not (min(a, b) - 1e-6 <= t <= max(a, b) + 1e-6):
                continue
            ts = np.linspace(h, t, 200)
            q = np.column_stack([PX + c["u"][0] * ts, PY + c["u"][1] * ts])
            sep = np.hypot(q[:, None, 0] - egg[None, :, 0], q[:, None, 1] - egg[None, :, 1]).min(1)
            if sep.max() < LENS:
                new_h = t
                c.setdefault("lens", []).append((round(h, 1), round(t, 1), round(float(sep.max()), 2)))
        if abs(o - new_h) > 1.0:
            out.append((min(new_h, o), max(new_h, o)))
    return out


def chord_intervals(c: dict, r: float) -> List[Tuple[float, float]]:
    """hub LOD -> egg lens -> field crop -> curve clearance, as t-intervals."""
    iv = []
    for (a, b) in lens_rule(c, chord_pieces(c, r)):
        for q in clip(_seg(c["u"], a, b), FIELD, keep="inside"):
            t0, t1 = _t_of(c, q[0]), _t_of(c, q[-1])
            iv.append((min(t0, t1), max(t0, t1)))
    return clear_of_curve(c, iv)


def chord_runs(c: dict) -> List[Run]:
    """ink for one chord.  Heavy = out along pass 1, back along pass 2 (offset
    0.25 mm, its own hub hole, same curve clearance) -- one pen-down per piece."""
    iv1 = chord_intervals(c, c["r1"])
    c.setdefault("iv", iv1)
    out: List[Run] = [_seg(c["u"], a, b) for a, b in iv1]
    if c["tier"] != "heavy":
        return out
    heavy: List[Run] = []

    def outer_last(r):
        d0 = math.hypot(r[0][0] - PX, r[0][1] - PY)
        d1 = math.hypot(r[-1][0] - PX, r[-1][1] - PY)
        return r if d1 >= d0 else r[::-1]

    for (a, b), r1 in zip(iv1, out):
        mate = None
        for (a2, b2) in chord_pieces(c, c["r2"]):
            lo, hi = max(a, a2), min(b, b2)
            if hi - lo > 1.0:
                mate = _seg(c["u"], lo, hi, HEAVY_OFF)
        if mate is None:
            heavy.append(r1)
            continue
        # one pen-down: inner1 -> outer1 -> outer2 -> inner2
        heavy.append(list(outer_last(r1)) + list(outer_last(mate)[::-1]))
    return heavy


# ===========================================================================
# L(E,s) on [0, 2]
# ===========================================================================
def l_samples(n: int = 401) -> np.ndarray:
    """L(E,s) on [0,2].  Reads this round's l_samples.json (written by
    compute_L.py from the same lfun_lib call) when present -- identical numbers,
    ~60 s saved per render; recomputes live otherwise."""
    cache = HERE / "l_samples.json"
    if cache.exists():
        import json

        d = json.loads(cache.read_text())
        if len(d["s"]) == n:
            return np.column_stack([np.asarray(d["s"], float), np.asarray(d["L"], float)])
    sys.path.insert(0, str(DATA))
    try:
        from lfun_lib import Lfun  # noqa: E402
    finally:
        sys.path.pop(0)
    E = Lfun("37a1")
    s = np.linspace(0.0, 2.0, n)
    L = np.array([0.0 if t == 0.0 else E.L(float(t), -1) for t in s])
    return np.column_stack([s, L])


def l_sheet(sl: np.ndarray) -> np.ndarray:
    return np.column_stack([S0_X + S * sl[:, 0], MIRROR + S * sl[:, 1]])


def l_runs(sl: np.ndarray) -> Tuple[List[Run], List[Run], Dict[str, float]]:
    """black L (two runs, each reaching 0.3 mm under the gold) + gold band."""
    m = l_sheet(sl)
    s = sl[:, 0]
    g0, g1 = GOLD_S
    arc = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(m[:, 0]), np.diff(m[:, 1])))])
    A0 = float(np.interp(g0, s, arc))
    A1 = float(np.interp(g1, s, arc))

    def cut(a, b):
        xs = np.interp([a, b], arc, m[:, 0])
        ys = np.interp([a, b], arc, m[:, 1])
        inner = (arc > a) & (arc < b)
        pts = [(xs[0], ys[0])] + [tuple(p) for p in m[inner]] + [(xs[1], ys[1])]
        return pts

    black = [cut(0.0, A0 + 0.3), cut(A1 - 0.3, arc[-1])]
    g = cut(A0, A1)
    gold = [_offset_polyline(g, -GOLD_HALF) + _offset_polyline(g, GOLD_HALF)[::-1]]
    # crossing geometry
    i = int(np.argmin(np.abs(s - 1.0)))
    ang = math.degrees(math.atan2(m[i + 1, 1] - m[i - 1, 1], m[i + 1, 0] - m[i - 1, 0]))
    j = int(np.argmin(sl[:, 1]))
    rep = dict(gold_len=A1 - A0, cross_angle=ang, L_min=float(sl[j, 1]), s_min=float(s[j]),
               L2=float(sl[-1, 1]), L15=float(np.interp(1.5, s, sl[:, 1])),
               zero_x=float(np.interp(0.0, sl[150:250, 1], m[150:250, 0])))
    black = [[(float(x), float(y)) for x, y in r] for r in black]
    return black, gold, rep


# ===========================================================================
# type: the house stroke font, 4 x 6 cell; SHA authored (the font has none)
# ===========================================================================
_EXTRA = {
    "Ш": [[(0.0, 6.0), (0.0, 0.0), (4.0, 0.0), (4.0, 6.0)], [(2.0, 6.0), (2.0, 0.0)]],
}
ADV = 5.6


def set_text(txt: str, x: float, y: float, cap: float, track: float = 0.0) -> Tuple[List[Run], float]:
    runs: List[Run] = []
    sc = cap / 6.0
    cx = x
    for ch in txt:
        strokes = _EXTRA.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper())
        if strokes is None:
            raise KeyError(f"missing glyph {ch!r} in {txt!r}")
        for st in strokes:
            runs.append([(cx + gx * sc, y + gy * sc) for gx, gy in st])
        cx += ADV * sc + track
    return runs, (cx - x - track) if txt else 0.0


def ink_box(runs: List[Run]) -> Tuple[float, float, float, float]:
    xs = [p[0] for r in runs for p in r]
    ys = [p[1] for r in runs for p in r]
    return min(xs), min(ys), max(xs), max(ys)


def split_corners(r: Run, max_turn: float = 50.0) -> List[Run]:
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


def x_string(n: int) -> str:
    x = ORB[n][0]
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# ===========================================================================
# pens
# ===========================================================================
LAYERS = ("hair", "chords", "text", "curves", "gold")


def _pen_map(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 5:
        return {"hair": 0, "chords": 1, "text": 2, "curves": 3, "gold": 4}
    if colors == 4:
        return {"hair": 0, "chords": 1, "text": 1, "curves": 2, "gold": 3}
    if colors == 3:
        return {"hair": 0, "chords": 1, "text": 1, "curves": 1, "gold": 2}
    if colors == 2:
        return {"hair": 0, "chords": 0, "text": 0, "curves": 0, "gold": 1}
    return {k: None for k in LAYERS}


class Fit:
    def __init__(self, bounds):
        bx0, by0, bx1, by1 = bounds
        w, h = SHEET[2] - SHEET[0], SHEET[3] - SHEET[1]
        self.k = min((bx1 - bx0) / w, (by1 - by0) / h)
        self.ox = bx0 + ((bx1 - bx0) - w * self.k) / 2.0 - SHEET[0] * self.k
        self.oy = by0 + ((by1 - by0) - h * self.k) / 2.0 - SHEET[1] * self.k

    def run(self, r: Sequence[Pt]) -> Run:
        return [(self.ox + x * self.k, self.oy + y * self.k) for x, y in r]


def order_runs(runs: List[Run], start: Pt = (15.0, 15.0)) -> List[Run]:
    rest = [list(r) for r in runs]
    out: List[Run] = []
    pos = start
    while rest:
        best, bi, flip = 1e18, 0, False
        for i, r in enumerate(rest):
            for fl, e in ((False, r[0]), (True, r[-1])):
                d = (e[0] - pos[0]) ** 2 + (e[1] - pos[1]) ** 2
                if d < best:
                    best, bi, flip = d, i, fl
        r = rest.pop(bi)
        r = r[::-1] if flip else r
        out.append(r)
        pos = r[-1]
    return out


# ===========================================================================
# the plate
# ===========================================================================
def build_layers() -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}
    CH = chords()
    REPORT["chords"] = CH
    for c in CH:
        runs = chord_runs(c)
        L["hair" if c["tier"] == "fine" else "chords"] += runs

    sl = l_samples()
    REPORT["L"] = sl
    black_L, gold_L, lrep = l_runs(sl)
    REPORT.update(lrep)

    # s-axis: s in [0, 2] on the mirror, hairline
    L["hair"].append([(S0_X, MIRROR), (S0_X + 2 * S, MIRROR)])

    # curves: E(R) + L
    L["curves"] = curve_runs() + black_L

    # gold: the disc (6 rings) + the crossing band
    for i in range(1, DISC_RINGS + 1):
        rr = DISC_R * i / DISC_RINGS
        n = max(24, int(2 * math.pi * rr / 0.4))
        L["gold"].append([(PX + rr * math.cos(2 * math.pi * j / n),
                           PY + rr * math.sin(2 * math.pi * j / n)) for j in range(n + 1)])
    L["gold"] += gold_L

    L["text"] = build_text()
    for k in ("hair", "chords", "curves", "text"):
        L[k] = join_touching(order_runs(L[k]))
    return L


def join_touching(runs: List[Run], tol: float = 0.02) -> List[Run]:
    """Merge consecutive runs whose end meets the next run's start (glyph strokes
    sharing a vertex): the same ink, one pen cycle fewer each."""
    out: List[Run] = []
    for r in runs:
        if out and math.hypot(out[-1][-1][0] - r[0][0], out[-1][-1][1] - r[0][1]) < tol:
            out[-1] = out[-1] + list(r[1:])
        else:
            out.append(list(r))
    return out


def build_text() -> List[Run]:
    T: List[Run] = []
    boxes: Dict[str, Tuple[float, float, float, float]] = {}

    # ---- title: 8 mm spaced caps, display weight (5 passes, 0.18 mm) ------------
    # tracking SOLVED so the last glyph's outer pass ends on x = 256.6, the end of
    # the L-curve (s = 2): the title spans the sheet's two halves and registers
    # the analysis from above.
    cap_t = 8.0
    ttl = "BIRCH AND SWINNERTON-DYER"
    last_ink = max(p[0] for st in _GLYPHS["R"] for p in st) * cap_t / 6.0
    x_end = S0_X + 2 * S
    tr_t = ((x_end - 0.36) - (15.0 + 0.36) - (len(ttl) - 1) * ADV * cap_t / 6.0 - last_ink) / (len(ttl) - 1)
    title, _ = set_text(ttl, 15.0 + 0.36, grid(87), cap_t, track=tr_t)
    for r in (q for r0 in title for q in split_corners(r0)):
        chain: Run = []
        for j, d in enumerate((-0.36, -0.18, 0.0, 0.18, 0.36)):
            q = _offset_polyline(r, d) if d else list(r)
            chain += q if j % 2 == 0 else q[::-1]
        T.append(chain)
    REPORT["title_track"] = tr_t
    cap_s = 2.5
    st, _ = set_text("ONE POINT MAKES INFINITELY MANY. ITS L-FUNCTION CROSSES ZERO ONCE.",
                     15.0, grid(84), cap_s, track=cap_s * 0.12)
    T += st
    boxes["statement"] = ink_box(st)

    # ---- upper-left wall label: the Morellet instruction -----------------------
    cap_i = 1.8
    tr_i = cap_i * 0.1
    wall = [
        "1  EVERY LINE PASSES THROUGH",
        "   THE GOLD POINT P = (0,0).",
        "",
        "2  EVERY PLACE A LINE MEETS THE",
        "   CURVE IS A RATIONAL POINT.",
        "",
        "3  ODD MULTIPLES LAND ON THE OVAL,",
        "   EVEN ONES ON THE OPEN BRANCH.",
        "",
        "4  WEIGHT: HEAVY = SMALL NUMBERS.",
    ]
    wl: List[Run] = []
    for i, ln in enumerate(wall):
        if ln:
            wl += set_text(ln, 15.0, grid(79 - i), cap_i, tr_i)[0]
    T += wl
    boxes["wall"] = ink_box(wl)

    # ---- the digit ziggurat: x(nP), n = 1..30 -----------------------------------
    cap_z = 1.6
    adv_z = ADV * cap_z / 6.0  # 1.493 mm mono advance
    zg: List[Run] = []
    lens = []
    for n in range(1, 31):
        y = grid(29 - (n - 1))
        idx = f"{n:2d}"
        for i, ch in enumerate(idx):
            if ch != " ":
                zg += set_text(ch, 15.0 + i * adv_z, y, cap_z)[0]
        s = x_string(n)
        lens.append(len(s))
        zg += set_text(s, 22.0, y, cap_z)[0]
    T += zg
    boxes["ziggurat"] = ink_box(zg)
    REPORT["zig_lens"] = lens
    cz: List[Run] = []
    for i, ln in enumerate(["X(NP) EXACTLY. ITS DIGITS GROW AS", "N² × 0.0511: THE HEIGHT OF P."]):
        cz += set_text(ln, 22.0, grid(-1 - i), cap_z, 0.0)[0]
    T += cz
    boxes["zig_caption"] = ink_box(cz)

    # ---- at the crossing ------------------------------------------------------
    w = set_text("S = 1", 0, 0, 1.6)[1]
    sc, _ = set_text("S = 1", 204.6 - w / 2.0, grid(39), 1.6)
    T += sc
    boxes["s1"] = ink_box(sc)

    # ---- right column, bottom: the bridge + status -----------------------------
    cap_r = 1.8
    tr_r = cap_r * 0.1
    col = [
        "E : Y² + Y = X³ - X",
        "CREMONA 37A1 · RANK 1",
        "",
        "SLOPE AT THE CROSSING",
        "L'(E,1) = 0.30600",
        "= 5.98692 × 0.05111",
        "= REAL PERIOD × HEIGHT OF P",
        "(Ш = 1, C = 1, NO TORSION)",
        "",
        "ROOT NUMBER -1: THE COMPLETED",
        "L IS ODD ABOUT S = 1, SO IT",
        "CANNOT MISS ZERO.",
        "",
        "PROVED FOR THIS CURVE:",
        "GROSS-ZAGIER 1986,",
        "KOLYVAGIN 1988.",
        "OPEN IN GENERAL.",
    ]
    rc: List[Run] = []
    for i, ln in enumerate(col):
        if ln:
            rc += set_text(ln, 226.0, grid(14 - i), cap_r, tr_r)[0]  # last line on grid(-2): shared baseline with the ziggurat caption
    T += rc
    boxes["right"] = ink_box(rc)
    REPORT["boxes"] = boxes
    return T


def bsd_zero_means_infinity(rng: SeededRNG, bounds, colors: int = 5) -> List[GCodeCommand]:
    """E(Q) as one pencil through one gold point; L(E,s) crossing zero once, in gold.

    Deterministic: every mark is exact data; ``rng`` is accepted for the
    contract and deliberately unused (nothing on the sheet is random).
    """
    _ = rng
    fit = Fit(bounds)
    L = build_layers()
    pens = _pen_map(colors)
    out: List[GCodeCommand] = []
    for layer in LAYERS:
        for r in L[layer]:
            out += _poly(fit.run(r), color=pens[layer], f=600)
    return out


if __name__ == "__main__":
    L = build_layers()
    for k, v in L.items():
        print(f"{k:7s} {len(v):4d} strokes  {sum(length(r) for r in v) / 1000:.3f} m")
    for k in ("gold_len", "cross_angle", "L_min", "s_min", "L15", "L2", "zero_x", "title_track"):
        print(k, round(REPORT[k], 5))
    print("zig lens", REPORT["zig_lens"])
    for k, b in REPORT["boxes"].items():
        print(k, [round(v, 2) for v in b])
