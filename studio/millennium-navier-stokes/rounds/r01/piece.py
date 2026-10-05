"""NAVIER-STOKES — faithful reconstruction, r01.  Millennium plate 3.

RINGS IN THE PLANE, A SPIRAL IN SPACE.  Every blue line is an exact streamline of
the Burgers vortex (Burgers 1948, an exact 3D Navier-Stokes solution) seen down
its stretching axis; the black disc is the exact 2D vortex (Lamb-Oseen), whose
streamlines can only be closed circles; the blue ladder is the SAME Burgers
solution under the Navier-Stokes scaling u -> 2u(2x, 4t), at 1, 1/2, 1/4, 1/8,
1/16; the empty red ring is where that ladder would have to finish, and it
encloses everything the 0.8 mm pen floor cannot draw.

Lineage: Bridget Riley, *Blaze 1* (1962).  Order taken: one line family at
constant spacing whose curvature drift alone makes the surface turn -- Riley's
concentric circles that the eye reads as a spiral; here the circles are the
plane and the spiral is real only in the third dimension.

FAITHFUL thesis: an illustrator's reconstruction of ``ref/reference.png``
(1122 x 1402 px, AI poster).  Measured off the raster (colour masks, row/column
scans, least-squares circle fit), in normalised reference (u right, v DOWN):

    frame rule        px x 28..1093, y 32..1368  (u .025-.974, v .023-.976)
    title caps        u .053-.409, v .058-.074 (cap 23 px = 1.64 % H)
    statement         v .086-.099 (italic lowercase)
    hero eye          (432, 562) px  -> u .385, v .401
    red circle        centre (834, 530), r 11 px -> u .743, v .378
    eddy lobe         4 eddies (865,260) (985,375) (980,535) (945,610) px
    zoom inset        circle centre (858, 981) r 182 px -> u .765 v .700,
                      R = 0.163 W  (the "X" saddle = the Burgers side view)
    corner captions   cap 6 px (0.43 % H), line pitch 14.5 px, a 20 px rule
                      below: TR u .896-.949 v .058-.099, L u .067-.111 v .667-.711,
                      BR u .892-.948 v .908-.957

Design space: A3 portrait in mm, y UP, drawable frame [15, 282] x [15, 405].
The whole sheet maps uniformly onto the passed bounds; the pen floors (0.8 mm,
the 2.4 mm streamline spacing, cap heights) are held in PAPER millimetres.

Pens (colors >= 4), plotting order light -> dark, accent last:
    0 BLUE   0.3  space: the 3D Burgers streamlines (hero + rungs 1-4)
    1 BLACK  0.1  the plane: 22 Lamb-Oseen rings; the side view (r^2 z = C) + axis
    2 BLACK  0.3  type (own layer)
    3 RED    0.5  the empty ring at the ladder's limit + the dated status stamp

Entry point: ``navier_stokes_faithful``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.scene3d import PolarLOD
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

# ---------------------------------------------------------------------------
# physics constants (stated in NOTES)
# ---------------------------------------------------------------------------
RE = 100.0            # Re_Gamma = Gamma / nu
DELTA0 = 22.0         # hero core scale delta_0, mm on A3
R_UNITS = 4.0         # every rung truncated at R_out = 4 delta
D_SEP = 2.4           # J-L separation in the hero, paper mm (Riley spacing)
D_TEST = 1.7          # arm termination spacing in the hero, paper mm (rung 1 = 0.85 >= floor)
FLOOR = 0.8           # pen floor, paper mm
CULL_MARGIN = 0.02    # cull at 0.82 so gcode rounding + chord sampling stay >= 0.80
LAMBDA = 2.0          # NS scaling ratio between rungs
N_RUNGS = 5           # rungs 0..4 drawn; rung 5 (delta 0.69 mm) is under the floor
N_ARMS = 256          # equal angular shares of the inflow at the rim
ORBIT_K_OVER_M = 2.2  # |C0 - L| = 1.5 * (k/m) * R0 ; k/m = 2.2 -> red ring clears rung 4
DPHI = math.radians(-20.0)  # similarity-orbit rotation per rung (faithful curl)
LO_DPSI = 0.09        # Lamb-Oseen ring step in f = ln s + E1(s)  (psi / (Gamma/4pi))
LO_R = 44.0           # ring disc radius = 2 r_c, r_c = delta_0
ST_DPSI = 0.20        # Stokes stream-function step for the side view (delta^3 units)
EL_RHO = 35.0         # side-view window radius, mm (same scale as the plan)

# design frame (A3 portrait)
FX0, FY0, FX1, FY1 = 15.0, 15.0, 282.0, 405.0

# layout (design mm)
C0 = (72.0, 262.0)          # hero centre (reference eye u .385 moved left: see NOTES)
L_PT = (250.0, 44.0)        # where the ladder would finish
DISC_C = (228.0, 297.0)     # 2D ring disc (where the reference's eddy lobe was)
EL_C = (72.0, 110.0)        # side view centre, on the hero's vertical

_EULER = 0.5772156649015329

STATS: Dict[str, object] = {}


# ---------------------------------------------------------------------------
# exact special functions
# ---------------------------------------------------------------------------
def E1(x) -> np.ndarray:
    """Exponential integral E1: power series below 1.5, Lentz continued fraction
    above.  Checked E1(1) = 0.2193839344, E1(2) = 0.0489005107."""
    x = np.atleast_1d(np.asarray(x, float))
    out = np.empty_like(x)
    lo = x <= 1.5
    xl = x[lo]
    s = np.zeros_like(xl)
    term = np.ones_like(xl)
    for k in range(1, 60):
        term = term * (-xl) / k
        s = s + term / k
    out[lo] = -_EULER - np.log(xl) - s
    xh = x[~lo]
    if xh.size:
        b = xh + 1.0
        c = np.full_like(xh, 1e300)
        d = 1.0 / b
        h = d.copy()
        for i in range(1, 200):
            a = -float(i * i)
            b = b + 2.0
            d = 1.0 / (a * d + b)
            c = b + a / c
            h = h * (c * d)
        out[~lo] = h * np.exp(-xh)
    return out


def burgers_theta(r) -> np.ndarray:
    """Closed-form Burgers streamline angle, delta = 1:
    theta(s) = (Re/8pi) [ (1 - e^-s)/s + E1(s) ],  s = r^2."""
    s = np.atleast_1d(np.asarray(r, float)) ** 2
    return (RE / (8.0 * math.pi)) * ((1.0 - np.exp(-s)) / s + E1(s))


def lamb_oseen_f(r_over_rc) -> np.ndarray:
    """Lamb-Oseen stream function / (Gamma/4pi) = ln s + E1(s), s = (r/r_c)^2."""
    s = np.atleast_1d(np.asarray(r_over_rc, float)) ** 2
    return np.log(s) + E1(s)


# ---------------------------------------------------------------------------
# Jobard-Lefebvre on the exact Burgers plan-view field (delta units)
# ---------------------------------------------------------------------------
def _canonical(r_out: float, r_min: float, h: float):
    """One exact streamline sampled at arclength ~h, rim -> eye.  Every other
    streamline of the axisymmetric field is this curve rotated."""
    rs = [r_out]
    r = r_out
    while r > r_min:
        rt = RE * (1.0 - math.exp(-r * r)) / (4.0 * math.pi * r * r)  # |r dtheta/dr|
        r -= h / math.sqrt(1.0 + rt * rt)
        rs.append(max(r, r_min))
    rs_a = np.array(rs)
    return rs_a, burgers_theta(rs_a)


def jobard_lefebvre(r_out: float, d_sep: float, d_test: float, h: float, r_min: float = 0.02):
    """Evenly spaced exact streamlines.  Seeds at +-d_sep off placed lines,
    traced both ways; a line terminates when it comes within d_test of any
    other line, or of its own earlier wrap.  Returns [(radius_idx array,
    rotation psi)] per streamline, rim -> eye, plus the canonical curve."""
    rs, th = _canonical(r_out, r_min, h)
    n = len(rs)
    lk = int(4.0 * d_test / h) + 1
    cell = d_test
    grid: dict = {}
    t2 = d_test * d_test
    s2 = d_sep * d_sep
    csep = int(math.ceil(d_sep / cell))

    def key(x, y):
        return (int(math.floor(x / cell)), int(math.floor(y / cell)))

    def near(x, y, sid, j):
        ci, cj = key(x, y)
        for a in (ci - 1, ci, ci + 1):
            for b in (cj - 1, cj, cj + 1):
                for px, py, ps, pj in grid.get((a, b), ()):
                    if ps == sid and abs(pj - j) <= lk:
                        continue
                    if (px - x) ** 2 + (py - y) ** 2 < t2:
                        return True
        return False

    def near_sep(x, y):
        ci, cj = key(x, y)
        for a in range(ci - csep, ci + csep + 1):
            for b in range(cj - csep, cj + csep + 1):
                for px, py, _, _ in grid.get((a, b), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < s2:
                        return True
        return False

    def trace(js, psi, sid):
        local: dict = {}
        inward = []
        for j in range(js, n):
            a = th[j] + psi
            x, y = rs[j] * math.cos(a), rs[j] * math.sin(a)
            if near(x, y, sid, j):
                break
            ci, cj = key(x, y)
            bad = False
            for aa in (ci - 1, ci, ci + 1):
                for bb in (cj - 1, cj, cj + 1):
                    for px, py, pj in local.get((aa, bb), ()):
                        if abs(pj - j) > lk and (px - x) ** 2 + (py - y) ** 2 < t2:
                            bad = True
                            break
            if bad:
                break
            local.setdefault((ci, cj), []).append((x, y, j))
            inward.append((j, x, y))
        outward = []
        for j in range(js - 1, -1, -1):
            a = th[j] + psi
            x, y = rs[j] * math.cos(a), rs[j] * math.sin(a)
            if near(x, y, sid, j):
                break
            outward.append((j, x, y))
        return list(reversed(outward)) + inward

    def register(pts, sid):
        for j, x, y in pts:
            grid.setdefault(key(x, y), []).append((x, y, sid, j))

    streams = []
    psis = []
    first = trace(0, -th[0], 0)  # rim, theta = 0
    register(first, 0)
    streams.append(first)
    psis.append(-th[0])
    step = max(1, int(0.5 * d_sep / h))
    q = [0]
    qi = 0
    min_len = 3.0 * d_sep
    while qi < len(q):
        s = streams[q[qi]]
        qi += 1
        for k in range(0, len(s), step):
            _, x, y = s[k]
            k1, k2 = max(0, k - 1), min(len(s) - 1, k + 1)
            tx, ty = s[k2][1] - s[k1][1], s[k2][2] - s[k1][2]
            tl = math.hypot(tx, ty)
            if tl == 0.0:
                continue
            nx, ny = -ty / tl, tx / tl
            for sg in (1.0, -1.0):
                sx, sy = x + sg * d_sep * nx, y + sg * d_sep * ny
                r = math.hypot(sx, sy)
                if r >= r_out or r <= 3.0 * d_sep:
                    continue
                if near_sep(sx, sy):
                    continue
                js = int(np.searchsorted(-rs, -r))
                js = min(max(js, 0), n - 1)
                psi = math.atan2(sy, sx) - th[js]
                sid = len(streams)
                pts = trace(js, psi, sid)
                if len(pts) * h < min_len:
                    continue
                register(pts, sid)
                streams.append(pts)
                psis.append(psi)
                q.append(sid)
    return streams, rs, th


def polar_arms(r_out: float, n_arms: int, d_test: float, h: float, r_min: float = 0.02):
    """N exact streamlines as equal angular shares of the axisymmetric inflow,
    thinned toward the eye by the engine's PolarLOD (halving levels).  The
    level radii are not tuned: arms with 2-adic valuation k die at the radius
    r_k where the N/2^k surviving arms' perpendicular spacing
    2 pi r sin(beta(r)) / (N/2^k) falls to d_test; arm 0 runs on to the
    self-wrap eye (its point comes within d_test of its own outer wrap).
    All in delta units.  Returns (streams rim->eye, level table, eye radius)."""
    rs, th = _canonical(r_out, r_min, h)
    ur = 2.0 * rs                                       # |u_r|, nu = 1, delta = 1
    vt = RE * (1.0 - np.exp(-rs * rs)) / (2.0 * math.pi * rs)
    g = 2.0 * math.pi * rs * ur / np.hypot(ur, vt)      # 2 pi r sin(beta), increasing in r
    kmax = int(round(math.log2(n_arms)))
    # self-wrap eye of the last arm: first sample whose outer wrap (theta - 2pi)
    # lies closer than d_test (measured as perpendicular gap along the radius)
    r_wrap = np.interp(th - 2.0 * math.pi, th, rs, left=np.nan)  # th increases inward
    cosb = vt / np.hypot(ur, vt)
    gap = (r_wrap - rs) * cosb
    bad = np.nonzero(np.nan_to_num(gap, nan=1e9) < d_test)[0]
    j_eye = int(bad[0]) if bad.size else len(rs) - 1
    levels = [(n_arms, rs[j_eye] / r_out)]
    for k in range(kmax - 1, -1, -1):
        m = n_arms // (2 ** k)                          # arms alive at this level
        # arms with valuation k die where m arms reach d_test
        rk = float(np.interp(d_test * m, g[::-1], rs[::-1]))
        levels.append((2 ** k, min(1.0, rk / r_out)))
    lod = PolarLOD(levels=tuple(levels))
    R = 100000
    streams = []
    for j in range(n_arms):
        rstop = lod.start_index(j, R) / R * r_out
        jj = int(np.searchsorted(-rs, -rstop))
        if jj < 2:
            continue
        psi = 2.0 * math.pi * j / n_arms - th[0]
        a = th[:jj] + psi
        streams.append(list(zip(rs[:jj] * np.cos(a), rs[:jj] * np.sin(a))))
    return streams, levels, float(rs[j_eye])


# ---------------------------------------------------------------------------
# small geometry helpers (design / paper mm)
# ---------------------------------------------------------------------------
def _resample(pts: Poly, step: float) -> Poly:
    if len(pts) < 2:
        return list(pts)
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= step:
            out.append(b)
            acc = 0.0
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def _length(pts: Poly) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _clip_rect(pts: Poly, x0: float, y0: float, x1: float, y1: float) -> List[Poly]:
    """Split a polyline where it leaves the rectangle (vertex test, dense input),
    interpolating the exit point onto the edge."""
    def inside(p):
        return x0 <= p[0] <= x1 and y0 <= p[1] <= y1

    def edge_pt(a, b):
        lo, hi = 0.0, 1.0
        for _ in range(30):
            m = 0.5 * (lo + hi)
            p = (a[0] + (b[0] - a[0]) * m, a[1] + (b[1] - a[1]) * m)
            if inside(p) == inside(a):
                lo = m
            else:
                hi = m
        return (a[0] + (b[0] - a[0]) * hi, a[1] + (b[1] - a[1]) * hi) if not inside(a) else \
            (a[0] + (b[0] - a[0]) * lo, a[1] + (b[1] - a[1]) * lo)

    runs: List[Poly] = []
    cur: Poly = []
    for i, p in enumerate(pts):
        if inside(p):
            if not cur and i > 0:
                cur.append(edge_pt(pts[i - 1], p))
            cur.append(p)
        else:
            if cur:
                cur.append(edge_pt(pts[i - 1], p))
                runs.append(cur)
                cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) >= 2]


class _Occ:
    """Floor grid for the cull pass (paper mm)."""

    def __init__(self, sep: float):
        self.sep = sep
        self.g: dict = {}

    def k(self, x, y):
        return (int(math.floor(x / self.sep)), int(math.floor(y / self.sep)))

    def hit(self, x, y) -> bool:
        ci, cj = self.k(x, y)
        s2 = self.sep * self.sep
        for a in (ci - 1, ci, ci + 1):
            for b in (cj - 1, cj, cj + 1):
                for px, py in self.g.get((a, b), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < s2:
                        return True
        return False

    def add(self, pts: Poly):
        for x, y in pts:
            self.g.setdefault(self.k(x, y), []).append((x, y))


def cull_to_floor(strokes: List[Poly], floor: float, sample: float = 0.2) -> Tuple[List[Poly], int, int]:
    """Longest first; each stroke is shortened from its INNER end (strokes run
    rim -> eye) at the first point closer than ``floor`` to a kept stroke or to
    its own earlier wrap.  Returns (kept, n_shortened, n_dropped)."""
    order = sorted(range(len(strokes)), key=lambda i: -_length(strokes[i]))
    occ = _Occ(floor)
    kept: Dict[int, Poly] = {}
    shortened = dropped = 0
    look = int(3.0 * floor / sample) + 1
    for i in order:
        pts = _resample_dense(strokes[i], sample)
        own = _Occ(floor)
        own_q: List[Pt] = []
        keep: Poly = []
        for p in pts:
            if occ.hit(*p):
                break
            if len(own_q) > look:
                own.add([own_q[-look - 1]])
            if own.hit(*p):
                break
            own_q.append(p)
            keep.append(p)
        if len(keep) < len(pts):
            shortened += 1
        if _length(keep) < 2.0 * floor:
            dropped += 1
            continue
        occ.add(keep)
        kept[i] = keep
    return [kept[i] for i in range(len(strokes)) if i in kept], shortened, dropped


def _resample_dense(pts: Poly, step: float) -> Poly:
    """Uniform arclength resample (inserts points)."""
    out: Poly = [pts[0]]
    carry = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg == 0.0:
            continue
        t = step - carry
        while t <= seg:
            out.append((a[0] + (b[0] - a[0]) * t / seg, a[1] + (b[1] - a[1]) * t / seg))
            t += step
        carry = seg - (t - step)
    if math.hypot(out[-1][0] - pts[-1][0], out[-1][1] - pts[-1][1]) > 1e-6:
        out.append(pts[-1])
    return out


# ---------------------------------------------------------------------------
# type (single-stroke font, proportional, tracked)
# ---------------------------------------------------------------------------
_EXTRA = {
    "δ": [[(2.4, 4.0), (1.1, 4.0), (0.3, 3.1), (0.3, 0.9), (1.1, 0.0), (2.4, 0.0), (3.2, 0.9),
           (3.2, 3.1), (2.4, 4.0), (1.0, 5.1), (1.3, 6.0), (3.0, 6.0)]],
    "ω": [[(0.9, 4.0), (0.3, 3.0), (0.3, 0.9), (0.9, 0.0), (1.5, 0.0), (1.75, 0.6), (1.75, 2.2)],
          [(1.75, 0.6), (2.0, 0.0), (2.6, 0.0), (3.2, 0.9), (3.2, 3.0), (2.6, 4.0)]],
    "Γ": [[(0.0, 0.0), (0.0, 6.0), (3.6, 6.0)]],
}
_SB = 0.8
_SPACE = 3.0
_GC: dict = {}


def _glyph(ch: str):
    if ch in _GC:
        return _GC[ch]
    if ch == " ":
        res = ([], _SPACE)
    else:
        strokes = _EXTRA.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        if ch == "0":
            strokes = strokes[:1]  # no slash
        xs = [p[0] for st in strokes for p in st]
        if not xs:
            res = ([], _SPACE)
        else:
            x0 = min(xs)
            sb = 0.45 if ch.islower() else _SB
            res = ([[(gx - x0 + sb, gy) for gx, gy in st] for st in strokes], max(xs) - x0 + 2 * sb)
    _GC[ch] = res
    return res


def text_width(s: str, cap: float, track: float = 0.0) -> float:
    return sum(_glyph(c)[1] for c in s) * cap / 6.0 + track * cap * max(0, len(s) - 1)


def text(s: str, x: float, y: float, cap: float, track: float = 0.0, align: str = "left") -> List[Poly]:
    if align == "right":
        x -= text_width(s, cap, track)
    elif align == "center":
        x -= 0.5 * text_width(s, cap, track)
    sc = cap / 6.0
    out: List[Poly] = []
    cx = x
    for ch in s:
        strokes, adv = _glyph(ch)
        for st in strokes:
            out.append([(cx + gx * sc, y + gy * sc) for gx, gy in st])
        cx += adv * sc + track * cap
    return out


def text_box(s: str, x: float, y: float, cap: float, track: float = 0.0, align: str = "left"):
    w = text_width(s, cap, track)
    if align == "right":
        x -= w
    elif align == "center":
        x -= 0.5 * w
    return (x, y - 0.3 * cap, x + w, y + 1.1 * cap)


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------
def orbit_centres(r0: float) -> Tuple[List[Pt], float, float]:
    """Rung centres on the similarity orbit 'scale 1/2, rotate DPHI about L'.
    |C0 - L| is fixed by the red-ring clearance; C0 is then placed on the ray
    from L towards the chosen hero centre."""
    dist = 1.5 * ORBIT_K_OVER_M * r0
    vx, vy = C0[0] - L_PT[0], C0[1] - L_PT[1]
    vl = math.hypot(vx, vy)
    vx, vy = vx / vl * dist, vy / vl * dist
    cs = []
    for n in range(N_RUNGS + 1):
        f = (1.0 / LAMBDA) ** n
        a = n * DPHI
        cx = L_PT[0] + f * (vx * math.cos(a) - vy * math.sin(a))
        cy = L_PT[1] + f * (vx * math.sin(a) + vy * math.cos(a))
        cs.append((cx, cy))
    ring_r = math.hypot(cs[N_RUNGS][0] - L_PT[0], cs[N_RUNGS][1] - L_PT[1]) + r0 / LAMBDA ** N_RUNGS
    return cs, ring_r, dist


def build(scale: float) -> Dict[str, List[Poly]]:
    """All geometry in DESIGN mm (A3 frame).  ``scale`` = paper mm per design mm,
    used only to hold the physical floors in paper millimetres."""
    L: Dict[str, List[Poly]] = {"blue": [], "hair": [], "type": [], "red": []}

    d0_paper = DELTA0 * scale
    r0 = R_UNITS * DELTA0
    # --- J-L once, in delta units (paper floors / paper delta_0)
    unit, levels, r_eye = polar_arms(R_UNITS, N_ARMS, D_TEST / d0_paper, 0.2 / d0_paper)
    STATS["arms"] = len(unit)
    STATS["lod_levels_mm"] = [(m, round(f * R_UNITS * DELTA0, 2)) for m, f in levels]
    STATS["eye_r_mm_hero"] = r_eye * DELTA0

    cs, ring_r, dist = orbit_centres(r0)
    STATS["orbit_centres"] = [(round(c[0], 2), round(c[1], 2)) for c in cs]
    STATS["ring_r"] = ring_r
    STATS["orbit_dist"] = dist

    rung_stats = []
    for n in range(N_RUNGS):
        dn = DELTA0 / LAMBDA ** n
        cx, cy = cs[n]
        strokes: List[Poly] = []
        for s in unit:
            pts = [(cx + x * dn, cy + y * dn) for x, y in s]
            pts = _resample(pts, 0.25 / scale)
            if n == 0:
                strokes += _clip_rect(pts, FX0, FY0, FX1, FY1)
            else:
                strokes.append(pts)
        # cull at the pen floor on PAPER geometry
        paper = [[(x * scale, y * scale) for x, y in s] for s in strokes]
        kept, sh, dr = cull_to_floor(paper, FLOOR + CULL_MARGIN)
        kept = [[(x / scale, y / scale) for x, y in s] for s in kept]
        kept.sort(key=lambda s: math.atan2(s[0][1] - cy, s[0][0] - cx) % (2 * math.pi))
        L["blue"] += kept
        rung_stats.append(
            dict(n=n, delta_mm=dn, R_mm=R_UNITS * dn, strokes_in=len(strokes), kept=len(kept),
                 shortened=sh, dropped=dr, length_mm=sum(_length(s) for s in kept) * scale,
                 uncut_mm=sum(_length(s) for s in strokes) * scale)
        )
    STATS["rungs"] = rung_stats

    # --- the empty red ring at L (two passes, slightly offset radii)
    for rr in (ring_r, ring_r - 0.35 / scale):  # 2nd pass inward: keeps the 0.8 mm to rung 4
        m = max(48, int(2 * math.pi * rr / 0.5))
        L["red"].append([(L_PT[0] + rr * math.cos(2 * math.pi * i / m),
                          L_PT[1] + rr * math.sin(2 * math.pi * i / m)) for i in range(m + 1)])

    # --- 2D Lamb-Oseen rings at equal delta-psi, r_c = delta_0, out to 2 r_c
    rc = DELTA0
    rr = np.linspace(0.005, LO_R / rc, 400001)
    ff = lamb_oseen_f(rr)
    lv = lamb_oseen_f(np.array([LO_R / rc]))[0] - LO_DPSI * np.arange(0, 400)
    lv = lv[lv > ff[0]]
    radii = np.interp(lv, ff, rr) * rc
    STATS["rings"] = dict(n=len(radii), inner=float(radii[-1]), outer=float(radii[0]),
                          min_gap=float((-np.diff(radii)).min()),
                          min_gap_at=float(radii[1:][np.argmin(-np.diff(radii))]),
                          outer_gap=float(radii[0] - radii[1]))
    for rad in radii[::-1]:  # inner -> outer
        m = max(40, int(2 * math.pi * rad / 0.5))
        a0 = 0.0
        L["hair"].append([(DISC_C[0] + rad * math.cos(a0 + 2 * math.pi * i / m),
                           DISC_C[1] + rad * math.sin(a0 + 2 * math.pi * i / m)) for i in range(m + 1)])

    hx = cs[0][0]  # the shared vertical: hero eye, projection line, side-view axis
    # --- side view: meridional streamlines r^2 |z| = C (Stokes psi = alpha r^2 z / 2),
    #     equal delta-psi, same scale as the plan, clipped to a disc window
    rho = EL_RHO / DELTA0
    cmax = 0.0
    tt = np.linspace(0.0, math.pi / 2, 2001)
    cmax = float(np.max((rho * np.cos(tt)) ** 2 * rho * np.sin(tt)))
    levels = []
    c = 0.5 * ST_DPSI
    while c < cmax:
        levels.append(c)
        c += ST_DPSI
    STATS["side_levels"] = len(levels)
    for cval in levels:
        # r from the axis side out to the window: z = c / r^2 ; keep inside disc
        rgrid = np.geomspace(1e-3, rho, 6000)
        z = cval / rgrid ** 2
        ok = rgrid ** 2 + z ** 2 <= rho * rho
        idx = np.nonzero(ok)[0]
        if idx.size < 2:
            continue
        # the inside part is one contiguous interval (hyperbola crosses the circle twice)
        seg_r, seg_z = rgrid[idx], z[idx]
        # densify the ends onto the circle by bisection
        branch = list(zip(seg_r, seg_z))
        branch = _resample(branch, 0.25 / DELTA0)
        for sx in (1, -1):
            for sz in (1, -1):
                # draw outward-flowing direction: from far-r end (inflow) to axis end (outflow)
                pts = [(hx + sx * r * DELTA0, EL_C[1] + sz * zz * DELTA0) for r, zz in branch[::-1]]
                L["hair"].append(pts)
    # the vortex line (the axis): solid inside the window
    L["hair"].append([(hx, EL_C[1] - EL_RHO), (hx, EL_C[1] + EL_RHO)])
    # ONE dotted projection line: hero rim -> side-view window, on the shared vertical
    y_top = cs[0][1] - r0 - 3.0
    y_bot = EL_C[1] + EL_RHO + 3.0
    y = y_top
    while y > y_bot:
        L["hair"].append([(hx, y), (hx, y - 0.35)])
        y -= 2.0
    STATS["dotted_span"] = (y_bot, y_top)
    return L


def _layout_type(L: Dict[str, List[Poly]], cs: List[Pt], ring_r: float) -> None:
    T = L["type"]
    hx, hy0 = cs[0]
    r0 = R_UNITS * DELTA0
    # title + statement, top-left on the frame
    T += text("NAVIER-STOKES", FX0, 386.0, 8.0, track=0.42)
    T += text("NAVIER-STOKES", FX0 + 0.3, 386.0, 8.0, track=0.42)  # second pass: weight
    T += text("flat, a whirlpool is only rings  /  the spiral is the third dimension",
              FX0, 374.0, 3.2, track=0.06)
    # top-right corner caption (reference "MOTION CONNECTS SCALES")
    y = 374.0  # first line on the statement's baseline
    for w in ("SAME EQUATIONS", "EVERY SCALE"):
        T += text(w, FX1, y, 1.9, track=0.55, align="right")
        y -= 4.4
    T.append([(FX1 - 6.0, y + 1.4), (FX1, y + 1.4)])
    # hero caption: right of the dotted projection line, under the hero's rim
    x = hx + 6.0
    y = hy0 - r0 - 9.0
    for ln in ("IN SPACE: A SPIRAL", "SEEN DOWN THE STRETCHING AXIS", "FLUID LEAVES THROUGH THE PAGE"):
        T += text(ln, x, y, 2.2, track=0.3)
        y -= 4.6
    # disc caption: under the disc, right-aligned on the frame
    y = DISC_C[1] - LO_R - 7.0
    for ln in ("IN THE PLANE: RINGS",
               "NO STRETCHING  (ω·∇)u = 0  ·  PROVED SMOOTH",
               "THE EYE ONLY OPENS:  t ×4  →  EYE ×2"):
        T += text(ln, FX1, y, 2.2, track=0.3, align="right")
        y -= 4.6
    # side-view caption: under the side-view window, on the frame's left edge
    y = EL_C[1] - EL_RHO - 7.0
    for ln in ("SIDE VIEW:  r²z = CONST  ·  SWIRL OMITTED",
               "IN FROM THE PLANE, OUT ALONG THE AXIS"):
        T += text(ln, FX0, y, 2.2, track=0.3)
        y -= 4.6
    # ladder caption: left of rung 2, right-aligned
    x = cs[2][0] - R_UNITS * DELTA0 / 4 - 6.0
    y = cs[2][1] + 4.6
    for ln in ("LARGE SCALES TO SMALLER ONES",
               "THE SAME SOLUTION AT 1/2, 1/4, 1/8, 1/16",
               "u → λu(λx, λ²t)  ·  COPIES, NOT ONE INSTANT"):
        T += text(ln, x, y, 2.2, track=0.3, align="right")
        y -= 4.6
    # at L
    x = L_PT[0] - ring_r - 5.0
    y = L_PT[1] + 2.0
    for ln in ("IF THE LADDER FINISHES, IT FINISHES HERE, BY 4/3 T0",
               "THE PEN STOPS AT 0.8 MM FIRST"):
        T += text(ln, x, y, 2.2, track=0.3, align="right")
        y -= 4.6
    # notes corner, bottom-left, on the stamp's baselines
    y = FY0 + 6.6
    for ln in ("BURGERS 1948 · LAMB-OSEEN · Re = 100 · δ0 = 22 MM",
               "IN 2D, ENERGY RUNS TO LARGER SCALES (KRAICHNAN 1967)"):
        T += text(ln, FX0, y, 1.9, track=0.3)
        y -= 4.6


def _stamp(L: Dict[str, List[Poly]], ring_r: float) -> None:
    y = FY0 + 6.6
    for ln in ("CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH (UNVERIFIED)",
               "WITHOUT A PUSH: OPEN"):
        L["red"] += text(ln, FX1, y, 2.2, track=0.3, align="right")
        y -= 4.6


def _pens(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 4:
        return {"blue": 0, "hair": 1, "type": 2, "red": 3}
    if colors == 3:
        return {"blue": 0, "hair": 1, "type": 1, "red": 2}
    if colors == 2:
        return {"blue": 0, "hair": 1, "type": 1, "red": 1}
    return {"blue": None, "hair": None, "type": None, "red": None}


def navier_stokes_faithful(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    """Millennium plate 3, faithful thesis.  Deterministic: no randomness is used
    (every mark is an exact streamline, ring or level set); ``rng`` is accepted
    for the contract."""
    bx0, by0, bx1, by1 = bounds
    fw, fh = FX1 - FX0, FY1 - FY0
    scale = min((bx1 - bx0) / fw, (by1 - by0) / fh)
    ox = bx0 + 0.5 * ((bx1 - bx0) - fw * scale) - FX0 * scale
    oy = by0 + 0.5 * ((by1 - by0) - fh * scale) - FY0 * scale

    L = build(scale)
    cs, ring_r, _ = orbit_centres(R_UNITS * DELTA0)
    _layout_type(L, cs, ring_r)
    _stamp(L, ring_r)

    pens = _pens(colors)
    out: List[GCodeCommand] = []
    feeds = {"blue": 1500, "hair": 1500, "type": 1800, "red": 1200}
    for name in ("blue", "hair", "type", "red"):
        for pl in L[name]:
            pts = [(ox + x * scale, oy + y * scale) for x, y in pl]
            out += _poly(pts, color=pens[name], f=feeds[name])
    STATS["layers"] = {k: (len(v), sum(_length(p) for p in v) * scale) for k, v in L.items()}
    return out


if __name__ == "__main__":  # quick stats
    import json
    cmds = navier_stokes_faithful(SeededRNG(7), (15, 15, 282, 405), 4)
    print(json.dumps(STATS, indent=1, default=float))
