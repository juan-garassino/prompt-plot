"""NAVIER-STOKES — r02, thesis ABSTRACT.  Plate 3 of the MILLENNIUM series.

Lineage: Bridget Riley, *Blaze 1* (1962, National Galleries of Scotland) — "although
it appears to be a spiral, Blaze 1 is formed from a succession of concentric
circles".  Order taken: ONE LINE FAMILY AT CONSTANT SPACING WHOSE CURVATURE DRIFT
ALONE MAKES THE SURFACE TURN.  The plate answers her literally: in the plane a
vortex really IS concentric circles (Lamb-Oseen, black); the spiral the eye wants
exists only in space (Burgers, blue), where the fluid leaves through the page.

Abstract order: RADIAL flow-to-an-attractor that is not a sink (blue) against
NESTED rings (black), the radial form repeated as a SELF-SIMILAR ladder that
converges on one empty point (red).

Every mark is computed, nothing is tuned by eye:

  blue   exact Burgers-vortex streamlines, closed form
             theta(s) = theta0 + (Re/8pi) [ (1 - e^-s)/s + E1(s) ],  s = r^2/delta^2
         seeded ONCE in delta-units (d_sep = 2.4 mm / 20 mm): 192 rim arms in
         halving order with Jobard-Lefebvre termination (per-arm d_test drawn
         from the rng in [0.70, 0.95] d_sep), then J-L infill.  Every stroke is
         a rotated arc of the one master curve, so every point lies exactly on
         a streamline.  Re_Gamma = Gamma/nu = 100, delta0 = 20 mm, R_out = 4 delta.
  ladder rung n = rung 0 scaled by 2^-n about its own centre (NS scaling
         u_lambda = lambda u(lambda x, lambda^2 t)); centres on the similarity
         orbit "scale 1/2 about L" with |C_n - C_n+1| = 1.20 (R_n + R_n+1)
         (rim gaps 24, 12, 6, 3 mm, and 1.5 mm to the red ring).
         A 0.8 mm cull on the FINAL mm geometry (longest first, shortened from
         its inner end) is the only thing that differs between rungs.
  black  Lamb-Oseen psi-isolines psi = (Gamma/4pi)[ln s + E1(s)], same Gamma,
         r_c = delta0, at EQUAL delta-psi (ring gap = speed), tightest 1.5 mm,
         20 rings out to 2 r_c.
  red    the empty ring around L: radius |C5 - L| + R5, it encloses every rung
         the pen cannot draw.  Plus the one open clause of the status stamp
         (the dated claim itself is black type).

Design sheet: A3 portrait, mm, y UP, drawable [15,282] x [15,405].  The design is
uniformly mapped to ``bounds``; the 0.8 mm floor, the 1.5 mm ring gap and type
minimums are held in REAL millimetres on the target paper.

Pens / layers, plotted in index order:
    0 BLUE   0.3  space: flow that leaves the plane (3D)   hero, rung 1, rungs 2-4
    1 BLACK  0.1  the plane: proved smooth (2D)            20 rings, inner -> outer
    2 BLACK  0.3  type (same ink, own layer)
    3 RED    0.5  the open question                        empty ring + 'WITHOUT A PUSH: OPEN'

Entry point: ``navier_stokes_blaze``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import giant_type
from promptplot.generative.generators import _poly, _stroke_text, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

# ===========================================================================
# the physics  (delta = 1, nu = 1)
# ===========================================================================
RE = 100.0                 # Re_Gamma = Gamma / nu
R_OUT = 4.0                # truncation radius, delta-units
R_MIN = 0.02               # table floor, delta-units (J-L terminates far above it)
DELTA0 = 20.0              # hero core scale on the A3 design sheet, mm (in [12.8, 25.6))
D_SEP = 2.4 / DELTA0       # J-L separation, delta-units  (0.109 delta)
D_TEST = D_SEP * 2.0 / 3.0 # J-L termination, delta-units
H_ARC = 0.010              # master-curve arc step, delta-units (0.22 mm on the hero)
LAMBDA = 2.0               # NS scaling ratio between rungs
N_RUNGS = 5                # rungs 0..4 drawn; rung 5 (0.69 mm core) is under the floor
ORBIT_K = 1.20             # |C_n - C_{n+1}| = ORBIT_K (R_n + R_{n+1}); rim gaps 0.2 (R_n + R_n+1)
FLOOR_MM = 0.8             # physical pen floor, real mm
RING_GAP_MM = 1.5          # tightest Lamb-Oseen ring gap, real mm
EULER_GAMMA = 0.5772156649015329
RIM_LEVELS = 5
# rim arms = base * 2^5, the base chosen so the PERPENDICULAR rim spacing
# (arc spacing * sin 64 deg at 4 delta) clears the widest per-arm d_test
# (0.95 d_sep): every arm of the finest level can start.  delta0 = 20 mm:
# base 6, 192 arms, rim arc spacing 2.62 mm.
RIM_BASE = int(2 * math.pi * R_OUT / (1.08 * D_SEP) / 2 ** RIM_LEVELS)
DT_LO, DT_HI = 0.70, 0.95       # per-arm termination band, in d_sep
RIM_MIN = 3.0                # shortest rim arm, in d_sep of arc (no stubs)
INFILL_MIN = 8.0             # shortest infill stroke, in d_sep of arc


def e1(s: np.ndarray) -> np.ndarray:
    """Exponential integral E1(s) = int_{ln s}^inf exp(-e^u) du, by cumulative
    trapezoid on a fine log grid (numpy only).  E1(1) = 0.2193839344."""
    s = np.asarray(s, dtype=float)
    lo = math.log(max(float(s.min()), 1e-12)) - 0.01
    u = np.linspace(lo, math.log(60.0), 400001)
    f = np.exp(-np.exp(u))
    du = u[1] - u[0]
    # tail[i] = int_{u_i}^{u_end} f du
    seg = 0.5 * (f[1:] + f[:-1]) * du
    tail = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    return np.interp(np.log(s), u, tail)


def burgers_theta(r: np.ndarray) -> np.ndarray:
    """Closed-form swirl angle of a Burgers streamline at radius r (delta-units),
    up to the arm's constant theta0.  Increases inward (counter-clockwise)."""
    s = np.asarray(r, dtype=float) ** 2
    return RE / (8.0 * math.pi) * ((1.0 - np.exp(-s)) / s + e1(s))


def dtheta_dlnr(r: float) -> float:
    return -RE * (1.0 - math.exp(-r * r)) / (4.0 * math.pi * r * r)


def master_curve(r_out: float = R_OUT, r_min: float = R_MIN, h: float = H_ARC):
    """Radii of the master streamline from r_out inward, spaced ~h in ARC length,
    with the exact closed-form theta at each radius."""
    rs = [r_out]
    r = r_out
    while r > r_min:
        g = dtheta_dlnr(r)
        dl = h / (r * math.sqrt(1.0 + g * g))
        r = r * math.exp(-dl)
        rs.append(r)
    rs = np.array(rs)
    return rs, burgers_theta(rs)


# ===========================================================================
# Jobard-Lefebvre on the planar Burgers field, run ONCE in delta-units
# ===========================================================================
class _Grid:
    def __init__(self, cell: float):
        self.cell = cell
        self.g: Dict[Tuple[int, int], list] = {}

    def key(self, x, y):
        return (int(math.floor(x / self.cell)), int(math.floor(y / self.cell)))

    def add(self, x, y, sid, k):
        self.g.setdefault(self.key(x, y), []).append((x, y, sid, k))

    def near(self, x, y, d, sid=-1, k=0.0, excl=0.0) -> bool:
        ci, cj = self.key(x, y)
        d2 = d * d
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for (qx, qy, qs, qk) in self.g.get((ci + di, cj + dj), ()):
                    if qs == sid and abs(qk - k) < excl:
                        continue
                    if (qx - x) ** 2 + (qy - y) ** 2 < d2:
                        return True
        return False


def jobard_lefebvre(rs: np.ndarray, th: np.ndarray, rng: Optional[SeededRNG] = None):
    """Evenly spaced streamlines of the Burgers plan-view field.

    Every stroke is the master curve rotated by theta0 and restricted to an
    index interval, so every point lies EXACTLY on a streamline.  Returns a list
    of (theta0, i_out, i_in, seed) with the stroke running rim -> eye."""
    grid = _Grid(D_SEP)
    excl = 3.0 * D_TEST / H_ARC          # own-stroke exclusion, in table indices
    n = len(rs)
    lnr = np.log(rs)

    def pt(theta0, i):
        a = theta0 + th[i]
        return rs[i] * math.cos(a), rs[i] * math.sin(a)

    def trace(theta0, i_seed_frac, sid, dt=D_TEST):
        """walk outward (decreasing index) and inward (increasing index) from a
        fractional seed index; stop at D_TEST from anything placed, or from the
        stroke's own points further than `excl` along it."""
        own = _Grid(D_SEP)
        i_hi = int(math.floor(i_seed_frac))  # last table index with r >= r_seed
        out_idx: List[int] = []
        in_idx: List[int] = []
        # inward
        for i in range(i_hi + 1, n):
            x, y = pt(theta0, i)
            if grid.near(x, y, dt) or own.near(x, y, D_TEST, 0, i, excl):
                break
            own.add(x, y, 0, i)
            in_idx.append(i)
        # outward
        for i in range(i_hi, -1, -1):
            x, y = pt(theta0, i)
            if grid.near(x, y, dt) or own.near(x, y, D_TEST, 0, i, excl):
                break
            own.add(x, y, 0, i)
            out_idx.append(i)
        if not out_idx and not in_idx:
            return None
        i_out = out_idx[-1] if out_idx else in_idx[0]
        i_in = in_idx[-1] if in_idx else out_idx[0]
        return i_out, i_in

    strokes = []

    def place(theta0, i_seed_frac, min_len, dt=D_TEST):
        res = trace(theta0, i_seed_frac, len(strokes), dt)
        if res is None:
            return None
        i_out, i_in = res
        if i_in - i_out < min_len:
            return None
        sid = len(strokes)
        for i in range(i_out, i_in + 1):
            px, py = pt(theta0, i)
            grid.add(px, py, sid, i)
        strokes.append((theta0, i_out, i_in))
        return sid

    # 1) RIM ARMS.  N = 7 * 2^5 arms whose rim spacing is ~d_sep, placed in
    #    halving order (7 base arms, then every level's bisectors, bit-reversed),
    #    each traced inward until it meets D_TEST.  Later levels therefore stop
    #    earlier as the flow converges: the arm count halves toward the eye.
    base_n, levels = RIM_BASE, RIM_LEVELS
    n_arms = base_n * 2 ** levels
    order: List[int] = []
    seen = set()
    for lev in range(levels + 1):
        step = 2 ** (levels - lev)
        for j in range(0, n_arms, step):
            if j not in seen:
                seen.add(j)
                order.append(j)
    th_rim = th[0]
    for j in order:
        theta0 = 2 * math.pi * j / n_arms - th_rim
        # Termination DITHER (a pen decision, not physics): in an axisymmetric
        # flow every arm of one level would die at the same radius and the
        # stroke ends would draw a RING inside the spiral - exactly the figure
        # this plate reserves for the plane.  Each arm draws its own d_test in
        # [0.70, 0.95] d_sep, so the ends scatter over a band.  The lower bound
        # sits just above J-L's 2/3 so rung 1 (d_sep 1.2 mm) clears 0.8 mm
        # WITHOUT culling - rungs 0 and 1 stay exact congruent copies.
        u = rng.random() if rng is not None else ((j * 0.6180339887) % 1.0)
        place(theta0, 0.0, int(RIM_MIN * D_SEP / H_ARC),
              dt=D_SEP * (DT_LO + (DT_HI - DT_LO) * u))
    STATS["rim_arms_placed"] = len(strokes)
    # 2) INFILL.  Classic Jobard-Lefebvre seeding off every placed line, but a
    #    stroke is kept only if it is long (>= INFILL_MIN d_sep of arc) - Riley
    #    lines, never stubs.
    min_len = int(INFILL_MIN * D_SEP / H_ARC)

    def try_seed(x, y):
        r = math.hypot(x, y)
        if not (rs[-1] < r < rs[0]):
            return None
        if grid.near(x, y, D_SEP):
            return None
        j = float(np.interp(-math.log(r), -lnr, np.arange(n)))
        th_r = float(burgers_theta(np.array([r]))[0])
        return place(math.atan2(y, x) - th_r, j, min_len)

    q = 0
    stride = max(1, int(round(D_SEP / 3.0 / H_ARC)))
    while q < len(strokes):
        theta0, i_out, i_in = strokes[q]
        q += 1
        for i in range(i_out, i_in + 1, stride):
            i0, i1 = max(i_out, i - 1), min(i_in, i + 1)
            if i1 == i0:
                continue
            ax, ay = pt(theta0, i0)
            bx, by = pt(theta0, i1)
            tx, ty = bx - ax, by - ay
            tl = math.hypot(tx, ty) or 1.0
            nx, ny = -ty / tl, tx / tl
            cx, cy = pt(theta0, i)
            for sgn in (1.0, -1.0):
                try_seed(cx + sgn * D_SEP * nx, cy + sgn * D_SEP * ny)
    return strokes, pt


# ===========================================================================
# Lamb-Oseen rings at equal delta-psi
# ===========================================================================
def lamb_oseen_rings(r_c: float, r_max: float, gap_mm: float) -> Tuple[List[float], float]:
    """Radii (mm) of psi-isolines at equal delta-psi, psi~ = ln s + E1(s),
    with delta-psi chosen so the tightest gap equals gap_mm exactly."""
    rr = np.linspace(1e-4, r_max * 1.05, 200001)
    s = (rr / r_c) ** 2
    psi = np.log(s) + e1(s) + EULER_GAMMA          # psi(0) = 0
    psi_max = float(np.interp(r_max, rr, psi))

    def radii(dpsi):
        levels = np.arange(dpsi, psi_max + 1e-12, dpsi)
        return np.interp(levels, psi, rr)

    lo, hi = 1e-4, 2.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        rad = radii(mid)
        g = float(np.diff(rad).min()) if len(rad) > 1 else 1e9
        if g < gap_mm:
            lo = mid
        else:
            hi = mid
    rad = radii(hi)
    return [float(v) for v in rad], hi


# ===========================================================================
# geometry helpers (real mm)
# ===========================================================================
def _clip_rect(run: Run, x0, y0, x1, y1) -> List[Run]:
    """Split a polyline at the rectangle; exact boundary crossings."""
    def inside(p):
        return x0 <= p[0] <= x1 and y0 <= p[1] <= y1

    def cross(a, b):
        # parameter where segment a->b leaves/enters the rect (Liang-Barsky)
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        for p, qv in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if p == 0:
                if qv < 0:
                    return None
                continue
            t = qv / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
        if t0 > t1:
            return None
        return t0, t1

    out: List[Run] = []
    cur: Run = []
    for i, p in enumerate(run):
        if inside(p):
            if not cur and i > 0:
                c = cross(run[i - 1], p)
                if c:
                    a = run[i - 1]
                    cur.append((a[0] + c[0] * (p[0] - a[0]), a[1] + c[0] * (p[1] - a[1])))
            cur.append(p)
        else:
            if cur:
                c = cross(run[i - 1], p)
                if c:
                    a = run[i - 1]
                    cur.append((a[0] + c[1] * (p[0] - a[0]), a[1] + c[1] * (p[1] - a[1])))
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    return [r for r in out if len(r) >= 2]


def _length(run: Run) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(run, run[1:]))


def _resample(run: Run, step: float) -> Run:
    if len(run) < 2:
        return list(run)
    out = [run[0]]
    carry = 0.0
    for a, b in zip(run, run[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg <= 0:
            continue
        t = step - carry
        while t < seg:
            out.append((a[0] + (b[0] - a[0]) * t / seg, a[1] + (b[1] - a[1]) * t / seg))
            t += step
        carry = seg - (t - step)
    if out[-1] != run[-1]:
        out.append(run[-1])
    return out


def _decimate(run: Run, step: float) -> Run:
    """Keep a SUBSET of the exact vertices, >= step apart (endpoints kept)."""
    out = [run[0]]
    for p in run[1:-1]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= step:
            out.append(p)
    out.append(run[-1])
    return out


def _truncate(run: Run, arc: float) -> Run:
    out = [run[0]]
    acc = 0.0
    for p0, p1 in zip(run, run[1:]):
        seg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        if acc + seg >= arc:
            t = (arc - acc) / seg if seg > 0 else 0.0
            out.append((p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1])))
            return out
        out.append(p1)
        acc += seg
    return out


def cull_floor(runs: Sequence[Run], floor: float, step: float = 0.1) -> Tuple[List[Run], dict]:
    """The pen floor, on the FINAL mm geometry.  Longest first; each stroke
    (ordered rim -> eye) is shortened from its inner end until it clears every
    kept stroke - and its own earlier wraps - by `floor`.  Never resumes."""
    order = sorted(range(len(runs)), key=lambda i: -_length(runs[i]))
    grid = _Grid(floor)
    kept: Dict[int, Run] = {}
    excl = 1.5 * floor / step    # own points nearer than 1.5 floor ALONG the stroke
    trimmed = removed = 0
    for sid in order:
        pts = _resample(runs[sid], step)
        keep: Run = []
        own = _Grid(floor)
        for k, (x, y) in enumerate(pts):
            if grid.near(x, y, floor) or own.near(x, y, floor, 0, k, excl):
                break
            own.add(x, y, 0, k)
            keep.append((x, y))
        if len(keep) < len(pts):
            trimmed += 1
        if _length(keep) < 3.0 * floor:
            removed += 1
            continue
        for k, (x, y) in enumerate(keep):
            grid.add(x, y, sid, k)
        # emit the ORIGINAL vertices (exact streamline points) up to the cut,
        # not the 0.1 mm check samples
        kept[sid] = _truncate(runs[sid], _length(keep)) if len(keep) < len(pts) else list(runs[sid])
    res = [kept[i] for i in range(len(runs)) if i in kept]
    return res, {"in": len(runs), "trimmed": trimmed, "removed": removed, "out": len(res)}


def _circle(cx, cy, r, a0=0.0, n=None) -> Run:
    n = n or max(48, int(2 * math.pi * r / 0.35))
    return [(cx + r * math.cos(a0 + 2 * math.pi * k / n),
             cy + r * math.sin(a0 + 2 * math.pi * k / n)) for k in range(n + 1)]


# ===========================================================================
# the plate
# ===========================================================================
STATS: dict = {}


def navier_stokes_blaze(rng: SeededRNG, bounds, colors: int = 4,
                        c0: Tuple[float, float] = (62.0, 272.0),
                        l_dir: Tuple[float, float] = (202.0, -238.0),
                        disc: Tuple[float, float] = (228.0, 295.0)) -> List[GCodeCommand]:
    """Rings in the plane, a spiral in space, and the ladder that would have to
    finish.  All randomness would go through `rng`; the plate uses none (J-L seed
    order is fixed: rim, theta = 0, sweeping counter-clockwise)."""
    bx0, by0, bx1, by1 = bounds
    # design sheet (A3 drawable) -> real mm, uniform
    DX0, DY0, DW, DH = 15.0, 15.0, 267.0, 390.0
    k = min((bx1 - bx0) / DW, (by1 - by0) / DH)
    ox = bx0 + ((bx1 - bx0) - DW * k) / 2.0
    oy = by0 + ((by1 - by0) - DH * k) / 2.0

    def M(x, y):
        return (ox + (x - DX0) * k, oy + (y - DY0) * k)

    def P(v):   # pen index, folded onto the available pens
        return v if colors > v else min(v, colors - 1)

    PEN_BLUE, PEN_RING, PEN_TYPE, PEN_RED = P(0), P(1), P(2), P(3)
    out: List[GCodeCommand] = []

    # ---------------------------------------------------------------- blue
    rs, th = master_curve()
    strokes, pt = jobard_lefebvre(rs, th, rng)
    base = []  # delta-unit strokes, rim -> eye
    for theta0, i_out, i_in in strokes:
        base.append([pt(theta0, i) for i in range(i_out, i_in + 1)])
    STATS["jl_strokes"] = len(base)
    STATS["jl_eye_delta"] = min(math.hypot(*s[-1]) for s in base)

    ux, uy = l_dir
    ul = math.hypot(ux, uy)
    ux, uy = ux / ul, uy / ul
    chain = ORBIT_K * 3.0 * R_OUT * DELTA0            # |C0 - L| (design mm)
    L = (c0[0] + chain * ux, c0[1] + chain * uy)
    STATS["chain_mm"] = chain
    STATS["L_design"] = L
    rung_runs: List[List[Run]] = []
    rung_meta = []
    for n in range(N_RUNGS):
        sc = LAMBDA ** (-n)
        cx = L[0] + (c0[0] - L[0]) * sc
        cy = L[1] + (c0[1] - L[1]) * sc
        dn = DELTA0 * sc                              # design mm per delta
        rc = M(cx, cy)
        runs: List[Run] = []
        for s in base:
            run = [(rc[0] + p[0] * dn * k, rc[1] + p[1] * dn * k) for p in s]
            runs += _clip_rect(run, bx0 + 0.05, by0 + 0.05, bx1 - 0.05, by1 - 0.05)
        # cull 0.03 mm above the floor so the decimated chords still clear it
        runs, st = cull_floor(runs, FLOOR_MM + 0.03)
        runs = [_decimate(r, 0.2) for r in runs]
        # stroke order: angular sweep of the outer end around the rung centre
        runs.sort(key=lambda r: (math.atan2(r[0][1] - rc[1], r[0][0] - rc[0])) % (2 * math.pi))
        rung_runs.append(runs)
        rung_meta.append({"n": n, "centre_mm": rc, "delta_mm": dn * k,
                          "R_mm": R_OUT * dn * k, **st,
                          "draw_mm": sum(_length(r) for r in runs)})
    STATS["rungs"] = rung_meta
    for runs in rung_runs:
        for r in runs:
            out += _poly(r, color=PEN_BLUE, f=600)

    # ---------------------------------------------------------------- black rings
    r_c = DELTA0 * k
    radii, dpsi = lamb_oseen_rings(r_c, 2.0 * r_c, RING_GAP_MM)
    dcx, dcy = M(*disc)
    golden = math.pi * (3.0 - math.sqrt(5.0))
    for i, rr in enumerate(radii):                    # inner -> outer
        out += _poly(_circle(dcx, dcy, rr, a0=i * golden), color=PEN_RING, f=600)
    gaps = np.diff(radii)
    STATS["rings"] = {"n": len(radii), "inner_mm": radii[0], "outer_mm": radii[-1],
                      "dpsi": dpsi, "min_gap_mm": float(gaps.min()),
                      "r_at_min_gap_over_rc": float((radii[int(gaps.argmin())]
                                                     + radii[int(gaps.argmin()) + 1]) / 2 / r_c),
                      "outer_gap_mm": float(gaps[-1])}

    # ---------------------------------------------------------------- red ring
    c5 = (L[0] + (c0[0] - L[0]) * LAMBDA ** -5, L[1] + (c0[1] - L[1]) * LAMBDA ** -5)
    R5 = R_OUT * DELTA0 * LAMBDA ** -5
    rho = (math.hypot(c5[0] - L[0], c5[1] - L[1]) + R5) * k
    Lm = M(*L)
    red_runs = [_circle(Lm[0], Lm[1], rho, a0=0.0), _circle(Lm[0], Lm[1], rho, a0=math.pi)]
    STATS["red_ring"] = {"centre_mm": Lm, "radius_mm": rho}

    # ---------------------------------------------------------------- type
    T: List[GCodeCommand] = []
    th_ = lambda h: max(1.8, h * k)                 # physical type floor

    def text(s, x, y, h, right=False, pen=PEN_TYPE):
        hh = th_(h)
        X, Y = M(x, y)
        if right:
            X -= _text_width(s, hh)
        return _stroke_text(s, X, Y, hh, color=pen, f=600)

    def stack(lines, x, y_top, h, lead=1.9, right=False, pen=PEN_TYPE):
        o = []
        for i, s in enumerate(lines):
            o += text(s, x, y_top - i * h * lead, h, right=right, pen=pen)
        return o

    # title + statement, top-left on x = 15; the title runs the full measure
    # 15 -> 282 (24 spaced advances + one glyph = 138.4 glyph units)
    title = "NAVIER-STOKES"
    sc_t = (DW * k) / (24 * 5.6 + 4.0)
    tx, ty = M(15.0, 386.0)
    T += giant_type(title, tx, ty, 6.0 * sc_t, pen=PEN_TYPE, weight=0.9 * k,
                    tip=0.45 * k, spaced=True, f=600)   # 3 passes on any paper
    T += text("FLAT, A WHIRLPOOL IS ONLY RINGS. THE SPIRAL IS THE THIRD DIMENSION,"
              " AND IT CAN KEEP SHRINKING.", 15.0, 373.0, 2.8)
    STATS["type_layout"] = "see NOTES"
    CAP = 2.3
    # ring disc (top-right, right-aligned on x = 282)
    T += stack(["IN THE PLANE: RINGS", "THE EYE ONLY OPENS",
                "PROVED SMOOTH"], 282.0, 360.0, CAP, right=True)
    # hero, tucked under its own cropped arc on x = 15
    T += stack(["IN SPACE: A SPIRAL", "SEEN DOWN THE STRETCHING AXIS",
                "THE FLUID LEAVES THROUGH THE PAGE"], 15.0, 180.0, CAP)
    # ladder, in the pocket right of rung 1
    T += stack(["THE SAME SOLUTION", "AT 1/2, 1/4, 1/8, 1/16",
                "NS SCALING: COPIES,", "NOT ONE INSTANT"], 282.0, 170.0, CAP, right=True)
    # the limit point + the status: right-aligned on x = 232, just left of
    # the red ring (left tangent 236.9) and under rung 4 (lowest 61)
    XL = 232.0
    T += stack(["IF THE LADDER FINISHES, IT FINISHES HERE,",
                "IN 4/3 OF THE FIRST RUNG'S TIME.",
                "THE PEN STOPS AT 0.8 MM FIRST."], XL, 50.0, CAP, right=True)
    # notes corner, bottom-left on x = 15
    T += stack(["BURGERS 1948 / LAMB-OSEEN / RE = %d / CORE %d MM" % (RE, round(DELTA0 * k)),
                "IN 2D, ENERGY RUNS TO LARGER SCALES (KRAICHNAN 1967)"], 15.0, 19.4, 2.0)
    out += T

    # ---------------------------------------------------------------- red last
    R: List[GCodeCommand] = []
    for r in red_runs:
        R += _poly(r, color=PEN_RED, f=600)
    # the status: the dated claim in black type, only the OPEN clause in red
    # (red is the open question - in space the ring, in time this line)
    T2 = stack(["CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH",
                "FORCED CASE NOT YET VERIFIED \u00b7 CLAY: NO AWARD"], XL, 35.0, CAP,
               lead=1.7, right=True, pen=PEN_TYPE)
    R += stack(["WITHOUT A PUSH: OPEN"], XL, 35.0 - 2 * CAP * 1.7, CAP,
               right=True, pen=PEN_RED)
    out += T2
    out += R
    return out
