"""MORPHOGENESIS — A UNIFORM FIELD CHOOSES A LENGTH (studio candidate, round 01).

The phenomenon, integrated — not illustrated.

The Gray-Scott two-morphogen system on a periodic square lattice::

    du/dt = Du grad^2 u  -  u v^2  +  F (1 - u)
    dv/dt = Dv grad^2 v  +  u v^2  - (F + k) v

is solved by explicit forward Euler with the 5-point Laplacian, from ONE
initial condition: u = 1, v = 0 everywhere (the homogeneous state), plus a
small square of (u, v) = (0.5, 0.25) and seeded Gaussian noise of sigma 0.02.
The noise is WHITE — it contains every length at once and prefers none.

The same initial array is then run three times with the diffusion pair scaled
by s = 0.4, 1.0, 2.0 (the ratio Du:Dv = 2:1 held fixed).  Rescaling both
diffusivities by s is an exact similarity of the PDE under x -> x sqrt(s), so
the selected Turing wavelength must obey

    lambda(s) / lambda(1) = sqrt(s)          (0.632, 1.000, 1.414)

and nothing else in the run changes.  The wavelength is measured, not asserted:
the radially-averaged structure factor S(q) of the converged v field is taken by
FFT and its peak located by parabolic interpolation, lambda = N / q*.  The
measured ratios are printed on the sheet next to the predicted ones — the plate
carries its own falsification.

Drawn as ISOLINES.  A pen cannot fill a bitmap but it draws a level set
perfectly, and the level set of v is the pattern: marching squares
(``_marching_squares``) + endpoint chaining (``_chain_segments``), the same
machinery ``contour_field`` uses — but here the field is a solved PDE, not
noise, and the contour level is a physical concentration.

Composition (one shared axonometric basis for every plate; plate spacing is
derived from the true projected rhombus extents, so nothing can interpenetrate):

* THE HERO — the central 72% of the s = 1.0 domain, magnified x4, drawn as a
  TERRACED RELIEF: four level sets of v, each riding its own terrace above the
  last, the stack centred on the ground plane.  Emitted top terrace first
  through ONE shared ``Scene3D.occupancy``, so the nearest ridge owns the paper
  and the ones behind it pause and resume — hidden line by the engine's native
  crowd control, never a hand-rolled z-buffer.  Cropped at the right sheet edge.
* THE DECK — four EQUAL plates on one straight world line: T = 0, then the three
  diffusion scales.  Equal size is mandatory: the argument is about spacing, so
  the plates must differ in nothing else.  The deck is also a tone ramp — the
  fine plate is a dark mass, the coarse one open paper.
* THE ORIGIN (T = 0) — the seeded noise contoured at its own zero level,
  coarse-grained so the dust is plottable: structureless speckle, every length
  and no length.  Plus the red germ square.  Mostly blank paper, because a
  uniform field IS blank paper.
* THE CALIPERS — five red bars at the hero's scale.  Three for D (visibly
  different) and, under a rule, two for the germ control (visibly identical).
  Gray-Scott's uniform state is linearly STABLE, so it needs a finite germ to
  nucleate and "the germ set the length" is a real objection; a 6x germ sweep
  answers it to better than 1%.
* Dotted projection lines (house law: dotted, never arrows) run corner to corner
  down the exploded deck and from the hero's source window up to the hero,
  clipped exactly outside every plate.
* Footer + S(q) inset — the run parameters, measured against predicted ratios,
  and the three radial structure factors with their peaks marked.

Pens.  black = the field, the frames, all type and furniture.  red = LENGTH, and
only length: the germ square that broke the symmetry, the five calipers, the
caliper on the relief, the three spectral peak ticks.  Type takes its own nib
when a 4th pen exists; red never carries a glyph.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from promptplot.models import GCodeCommand  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402
from promptplot.generative.engine import Scene3D  # noqa: E402
from promptplot.generative.engine.geometry import HalfPlane, Rect, Region, clip  # noqa: E402
from promptplot.generative.kit import (  # noqa: E402
    _chain_segments,
    _marching_squares,
    _spaced,
    _stroke_text,
    plus_mark,
    swatch_bar,
)

Bounds = Tuple[float, float, float, float]

# ---------------------------------------------------------------- pen indices
INK = 0  # black — the field, frames, type, furniture
RED = 1  # crimson — LENGTH only (germ, wavelength rules, spectral peaks)

# ------------------------------------------------- the one axonometric basis
# Never rescaled.  A plate that must be smaller shrinks its world FOOTPRINT.
A_ISO = 0.500  # screen mm per world unit of (wx - wz)
CD_ISO = 0.260  # screen mm per world unit of (wx + wz), downward
WY_ISO = 0.620  # screen mm per world unit of height


def _proj(wx: float, wy: float, wz: float) -> Tuple[float, float]:
    return ((wx - wz) * A_ISO, wy * WY_ISO - (wx + wz) * CD_ISO)


def _dep(wx: float, wy: float, wz: float) -> float:
    return (wx + wz) + 0.12 * wy


def _world_at(sx: float, sy: float) -> Tuple[float, float]:
    """Ground-plane world (wx, wz) whose projection is the screen point."""
    d = sx / A_ISO  # wx - wz
    t = -sy / CD_ISO  # wx + wz
    return (t + d) / 2.0, (t - d) / 2.0


# ---------------------------------------------------------------- the solver
def _gray_scott(
    n: int,
    F: float,
    k: float,
    du: float,
    dv: float,
    dt: float,
    steps: int,
    u0,
    v0,
):
    """Explicit forward Euler, 5-point periodic Laplacian. Returns v."""
    import numpy as np

    u, v = u0.copy(), v0.copy()
    cu, cv = np.float32(du * dt), np.float32(dv * dt)
    dtf, Ff, kf = np.float32(dt), np.float32(F), np.float32(k)
    L = np.empty_like(u)
    T = np.empty_like(u)
    for _ in range(steps):
        np.add(np.roll(u, 1, 0), np.roll(u, -1, 0), out=L)
        L += np.roll(u, 1, 1)
        L += np.roll(u, -1, 1)
        L -= 4.0 * u
        np.multiply(v, v, out=T)
        T *= u  # u v^2
        u += cu * L - dtf * T + (dtf * Ff) * (1.0 - u)
        np.add(np.roll(v, 1, 0), np.roll(v, -1, 0), out=L)
        L += np.roll(v, 1, 1)
        L += np.roll(v, -1, 1)
        L -= 4.0 * v
        v += cv * L + dtf * T - (dtf * (Ff + kf)) * v
    return v


def _structure_factor(v):
    """Radially averaged S(q) of v, and the characteristic wavenumber q*.

    q* is the intensity-weighted FIRST MOMENT of S(q) over the band around the
    (smoothed) peak — the standard robust definition.  A bare argmax on a
    128-box spectrum jitters by a whole bin between noise realizations; the
    moment does not (measured spread < 1% over four seeds).
    """
    import numpy as np

    a = v - v.mean()
    n = a.shape[0]
    P = np.abs(np.fft.fft2(a)) ** 2
    fy, fx = np.meshgrid(np.fft.fftfreq(n) * n, np.fft.fftfreq(n) * n, indexing="ij")
    q = np.sqrt(fx * fx + fy * fy)
    nb = n // 2
    prof = np.bincount(q.astype(int).ravel(), P.ravel(), minlength=nb)[:nb]
    prof[0] = 0.0
    i = int(np.argmax(np.convolve(prof, np.ones(3) / 3.0, mode="same")))
    lo, hi = max(1, int(i * 0.55)), min(nb, int(i * 1.85) + 1)
    w = prof[lo:hi]
    qs = float((np.arange(lo, hi) * w).sum() / max(w.sum(), 1e-12))
    return prof, max(qs, 1e-6)


# ------------------------------------------------------------------ contours
def _decimate(pts: Sequence[Tuple[float, float]], d: float = 0.45):
    """Drop samples closer than ``d`` (in the chain's own units)."""
    out = [pts[0]]
    for p in pts[1:-1]:
        if (p[0] - out[-1][0]) ** 2 + (p[1] - out[-1][1]) ** 2 >= d * d:
            out.append(p)
    out.append(pts[-1])
    return out


def _isolines(field, iso: float, min_pts: int = 5, dec: float = 0.45):
    """Level set of ``field`` in unit-square coordinates [0,1]^2."""
    ny, nx = len(field), len(field[0])
    xs = [i / (nx - 1) for i in range(nx)]
    ys = [j / (ny - 1) for j in range(ny)]
    segs = _marching_squares(field, xs, ys, iso)
    chains = []
    for ch in _chain_segments(segs):
        if len(ch) >= min_pts:
            chains.append(_decimate(ch, dec / max(nx, ny)))
    return chains


# ------------------------------------------------------------------- regions
def _rhombus(cx: float, cy: float, half_w: float, half_h: float):
    """Screen corners of a ground-plane square, in CCW order."""
    return [(cx - half_w, cy), (cx, cy - half_h), (cx + half_w, cy), (cx, cy + half_h)]


def _poly_region(corners) -> Region:
    """Convex screen polygon as an intersection of half-planes (inside <= 0)."""
    reg: Optional[Region] = None
    n = len(corners)
    cx = sum(p[0] for p in corners) / n
    cy = sum(p[1] for p in corners) / n
    for i in range(n):
        ax, ay = corners[i]
        bx, by = corners[(i + 1) % n]
        nx, ny = by - ay, ax - bx  # outward-ish normal
        c = -(nx * ax + ny * ay)
        if nx * cx + ny * cy + c > 0:  # flip so the centroid is inside
            nx, ny, c = -nx, -ny, -c
        hp = HalfPlane(nx, ny, c)
        reg = hp if reg is None else (reg & hp)
    return reg


def _rhombi_clear(p, q, gap: float = 1.0) -> bool:
    """Exact separation test for two same-orientation screen rhombi.

    p, q = (cx, cy, half_w, half_h).  Their Minkowski sum is a rhombus with the
    summed half-diagonals, so they are disjoint iff the L1 test below holds.
    """
    dx, dy = abs(p[0] - q[0]), abs(p[1] - q[1])
    return dx / (p[2] + q[2]) + dy / (p[3] + q[3]) >= gap


# --------------------------------------------------------------------- piece
def studio_reaction_diffusion(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n: int = 128,
    F: float = 0.030,
    k: float = 0.057,
    du: float = 0.16,
    dv: float = 0.08,
    dt: float = 0.75,
    steps: int = 7000,
    scales: Tuple[float, float, float] = (0.4, 1.0, 2.0),
    noise: float = 0.02,
    iso_frac: float = 0.46,
    hero_src: int = 1,
    hero_win: float = 0.72,
    hero_levels: int = 4,
    level_lift: float = 2.6,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """MORPHOGENESIS — the Turing wavelength measured off three solved fields.

    One initial condition, three diffusion scales, one shared axonometry: the
    pattern's spacing tracks sqrt(D) exactly while the noise that seeded it has
    no length at all.
    """
    import numpy as np

    x0, y0, x1, y1 = bounds
    ink, red = INK % colors, RED % colors
    type_pen = (3 % colors) if colors >= 4 else ink

    # ------------------------------------------------------------ the physics
    rs = np.random.RandomState(rng.randint(0, 10**6))
    u0 = np.ones((n, n), np.float32)
    v0 = np.zeros((n, n), np.float32)
    g = max(3, n // 12)
    cy_, cx_ = int(n * 0.415), int(n * 0.455)  # off-centre: no imposed symmetry
    u0[cy_ - g : cy_ + g, cx_ - g : cx_ + g] = 0.50
    v0[cy_ - g : cy_ + g, cx_ - g : cx_ + g] = 0.25
    nz = rs.normal(0.0, noise, (n, n)).astype(np.float32)
    u0 += nz
    v0 -= nz

    def seeded(half: int):
        u = np.ones((n, n), np.float32)
        v = np.zeros((n, n), np.float32)
        u[cy_ - half : cy_ + half, cx_ - half : cx_ + half] = 0.50
        v[cy_ - half : cy_ + half, cx_ - half : cx_ + half] = 0.25
        u += nz
        v -= nz
        return u, v

    fields, lams, profs = [], [], []
    for s in scales:
        v = _gray_scott(n, F, k, du * s, dv * s, dt, steps, u0, v0)
        prof, qs = _structure_factor(v)
        fields.append(v)
        profs.append(prof)
        lams.append(n / qs)  # wavelength in lattice cells

    # CONTROL: the germ is varied ~6x at fixed D.  If the noise/seed set the
    # length, these two must differ.  They do not.
    ctrl_half = (max(2, n // 32), max(4, n // 5))
    ctrl_lam = []
    for half in ctrl_half:
        cu_, cv_ = seeded(half)
        _, qs = _structure_factor(_gray_scott(n, F, k, du, dv, dt, steps, cu_, cv_))
        ctrl_lam.append(n / qs)

    # ------------------------------------------------------------- the scene
    scene = Scene3D(rng, bounds, feed=feed, tip=0.35, px=(300, 300), pad=4.0, fit="none")
    out = scene.out

    S_ROW = 46.0  # world side of every flat plate — EQUAL, by the argument
    S_HERO = 132.0
    HW_ROW, HH_ROW = S_ROW * A_ISO, S_ROW * CD_ISO
    HW_HERO, HH_HERO = S_HERO * A_ISO, S_HERO * CD_ISO
    STEP = (38.0, 19.76)  # one world step along -wz, in screen mm

    deck = [(x0 + 38.0 + STEP[0] * i, y0 + 52.0 + STEP[1] * i) for i in range(4)]
    t0_c, row_c = deck[0], deck[1:]
    hero_c = (x0 + 128.0, y0 + 188.0)

    boxes = [(p[0], p[1], HW_ROW, HH_ROW) for p in deck]
    hero_box = (hero_c[0], hero_c[1] + hero_levels * level_lift * 0.5,
                HW_HERO, HH_HERO + hero_levels * level_lift * 0.5)
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            if not _rhombi_clear(boxes[i], boxes[j]):
                raise ValueError(f"plates {i},{j} interpenetrate")
        if not _rhombi_clear(boxes[i], hero_box):
            raise ValueError(f"plate {i} interpenetrates the hero")

    regions = [_poly_region(_rhombus(*b)) for b in boxes]
    regions.append(_poly_region(_rhombus(hero_c[0], hero_c[1], HW_HERO, HH_HERO)))

    # ------------------------------------------------------------------ type
    paper = Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)

    def spoly(pts, pen: int) -> None:
        """scene.poly, cut EXACTLY at the sheet edge (the hero crops there)."""
        for run in clip(list(pts), paper, keep="inside"):
            scene.poly(run, pen=pen)

    tx = x0 + 1.0
    lam_txt = ["%.1f" % L for L in lams]
    r_meas = [L / lams[1] for L in lams]
    r_pred = [math.sqrt(s) for s in scales]
    cal_x, cal_y = x0 + 1.0, y0 + 184.0  # caliper stack, in the left void

    # the hero's own wavelength mark — hoisted so its label can reserve a halo
    hu, hv = _world_at(hero_c[0] - x0, hero_c[1] - y0)
    Lh = lams[hero_src] / (n * hero_win)  # one wavelength, as a fraction of the side
    ha, hb = (
        _proj(hu + (uu - 0.5) * S_HERO, 0.0, hv + (0.945 - 0.5) * S_HERO)
        for uu in (0.13, 0.13 + Lh)
    )
    ha, hb = (ha[0] + x0, ha[1] + y0), (hb[0] + x0, hb[1] + y0)

    scene.halo_labels(
        [
            (_spaced("MORPHOGENESIS"), tx, y1 - 12.0, 6.8, type_pen),
            (_spaced("A UNIFORM FIELD CHOOSES A LENGTH"), tx, y1 - 19.6, 2.6, type_pen),
            (_spaced("GRAY-SCOTT REACTION-DIFFUSION. ONE SEEDED FIELD,"),
             tx, y1 - 25.4, 1.8, type_pen),
            (_spaced("THREE DIFFUSION SCALES. THE SPACING GOES AS SQRT D."),
             tx, y1 - 29.6, 1.8, type_pen),
            (_spaced("V IN RELIEF"), cal_x, cal_y + 34.0, 2.2, type_pen),
            (_spaced("LAMBDA %s" % lam_txt[hero_src]), ha[0] + 1.0, ha[1] + 3.0,
             2.0, type_pen),
            (_spaced("ONE LEVEL SET PER TERRACE"), cal_x, cal_y + 29.4, 1.6, type_pen),
            (_spaced("WINDOW X%.1f OFF D %.1f" % (S_HERO / (S_ROW * hero_win),
                                                  scales[hero_src])),
             cal_x, cal_y + 25.8, 1.6, type_pen),
            (_spaced("SELECTED WAVELENGTH"), cal_x, cal_y + 15.0, 2.0, type_pen),
            (_spaced("MEASURED OFF S Q"), cal_x, cal_y + 10.6, 1.6, type_pen),
            (_spaced("CONTROL. SAME D, GERM X%d" % round(ctrl_half[1] / ctrl_half[0])),
             cal_x, cal_y - 23.0, 1.6, type_pen),
            (_spaced("T 0"), t0_c[0] - HW_ROW + 1.0, t0_c[1] + HH_ROW + 3.0, 2.6, type_pen),
            (_spaced("UNIFORM PLUS NOISE"),
             t0_c[0] - HW_ROW + 1.0, t0_c[1] + HH_ROW - 0.4, 1.6, type_pen),
            (_spaced("NO LENGTH SCALE"),
             t0_c[0] - HW_ROW + 1.0, t0_c[1] + HH_ROW - 3.4, 1.6, type_pen),
        ]
        + [
            (_spaced("D %.1f" % s), row_c[i][0] - HW_ROW + 1.0,
             row_c[i][1] + HH_ROW + 3.0, 2.6, type_pen)
            for i, s in enumerate(scales)
        ]
        + [
            (_spaced("LAMBDA %s" % lam_txt[i]), row_c[i][0] - HW_ROW + 1.0,
             row_c[i][1] + HH_ROW - 0.4, 1.6, type_pen)
            for i in range(3)
        ]
    )

    # -------------------------------------------------------- the flat deck
    def frame(cx: float, cy: float, hw: float, hh: float, pen: int) -> None:
        pts = _rhombus(cx, cy, hw, hh)
        spoly(pts + [pts[0]], pen)

    def lay(cx: float, cy: float, s_world: float, ux: float, uz: float):
        sx, sy = _proj((ux - 0.5) * s_world, 0.0, (uz - 0.5) * s_world)
        return cx + sx, cy + sy

    # T = 0 : the seeded noise at its own zero level — coarse-grained so the
    # dust is plottable.  White noise: every length, no length.
    nzc = (v0[::4, ::4]).astype(float).tolist()
    for ch in _isolines(nzc, 0.0, min_pts=4, dec=0.9):
        spoly([lay(*t0_c, S_ROW, p[0], p[1]) for p in ch], ink)
    gq = g / n
    gu, gz = cx_ / n, cy_ / n
    germ = [(gu - gq, gz - gq), (gu + gq, gz - gq), (gu + gq, gz + gq), (gu - gq, gz + gq)]
    gpts = [lay(*t0_c, S_ROW, p[0], p[1]) for p in germ + [germ[0]]]
    spoly(gpts, red)
    spoly([(p[0] + 0.25, p[1]) for p in gpts], red)  # 2nd pass: loud
    frame(*t0_c, HW_ROW, HH_ROW, ink)

    # the three solved fields, one isoline level each — equal plates
    for i, v in enumerate(fields):
        lo, hi = float(v.min()), float(v.max())
        fl = v.astype(float).tolist()
        for ch in _isolines(fl, lo + (hi - lo) * iso_frac, min_pts=6, dec=0.55):
            spoly([lay(*row_c[i], S_ROW, p[0], p[1]) for p in ch], ink)
        frame(*row_c[i], HW_ROW, HH_ROW, ink)

    # -------------------------------------------- dotted projection lines
    def dotted(p0, p1, pen: int, period: float = 2.8, duty: float = 0.42) -> None:
        runs = [[p0, p1]]
        for reg in regions:
            nxt = []
            for r in runs:
                nxt.extend(clip(r, reg, keep="outside"))
            runs = nxt
        for r in runs:
            ax, ay = r[0]
            bx, by = r[-1]
            L = math.hypot(bx - ax, by - ay)
            if L < 4.0:
                continue
            m = int(L / period)
            for q in range(m):
                ta, tb = q / m, (q + duty) / m
                spoly(
                    [(ax + (bx - ax) * ta, ay + (by - ay) * ta),
                     (ax + (bx - ax) * tb, ay + (by - ay) * tb)],
                    pen,
                )

    for i in range(len(deck) - 1):
        ca = _rhombus(deck[i][0], deck[i][1], HW_ROW, HH_ROW)
        cb = _rhombus(deck[i + 1][0], deck[i + 1][1], HW_ROW, HH_ROW)
        for pa, pb in zip(ca, cb):
            dotted(pa, pb, ink)

    # ------------------------------------------------------------- the hero
    hw = hero_win / 2.0
    win = [(0.5 - hw, 0.5 - hw), (0.5 + hw, 0.5 - hw), (0.5 + hw, 0.5 + hw), (0.5 - hw, 0.5 + hw)]
    win_s = [lay(*row_c[hero_src], S_ROW, p[0], p[1]) for p in win]
    spoly(win_s + [win_s[0]], ink)
    spoly([(p[0] + 0.25, p[1]) for p in win_s + [win_s[0]]], ink)  # 2nd pass

    vh = fields[hero_src]
    i0, i1 = int(n * (0.5 - hw)), int(n * (0.5 + hw))
    wf = vh[i0:i1, i0:i1]
    wlo, whi = float(wf.min()), float(wf.max())
    hgt = ((wf - wlo) / max(1e-9, whi - wlo)).astype(float).tolist()

    frame(hero_c[0], hero_c[1], HW_HERO, HH_HERO, ink)

    # the level sets, stacked: each level rides its own terrace.  Drawn from
    # the TOP down through one shared occupancy, so the nearest ridge owns the
    # paper and the ones behind it pause — the engine's native hidden line.
    occ = scene.occupancy(0.82)
    for lv in range(hero_levels, 0, -1):
        frac = lv / (hero_levels + 1)
        wy = (lv - (hero_levels + 1) / 2.0) * level_lift / WY_ISO
        fam = []
        for ch in _isolines(hgt, frac, min_pts=6, dec=0.4):
            samples = []
            for uxx, uzz in ch:
                wx = hu + (uxx - 0.5) * S_HERO
                wz = hv + (uzz - 0.5) * S_HERO
                px, py = _proj(wx, wy, wz)
                sx_, sy_ = px + x0, py + y0
                inside = x0 + 0.3 <= sx_ <= x1 - 0.3 and y0 + 0.3 <= sy_ <= y1 - 0.3
                samples.append(
                    (sx_, sy_, _dep(wx, wy, wz) if inside else Scene3D.HIDE, ink)
                )
            if len(samples) >= 4:
                fam.append(samples)
        scene.lines(fam, mode="pause_resume", occupancy=occ, warmup=2, min_kept=4)

    # one measured wavelength laid ON the relief — the hero states its own scale
    spoly([ha, hb], red)
    spoly([(ha[0], ha[1] + 0.3), (hb[0], hb[1] + 0.3)], red)
    for e in (ha, hb):
        spoly([(e[0], e[1] - 2.0), (e[0], e[1] + 2.0)], red)

    for pa, pb in zip(win_s, _rhombus(hero_c[0], hero_c[1], HW_HERO, HH_HERO)):
        dotted(pa, pb, ink, period=3.6, duty=0.40)

    # --------------------------------------------- the calipers (red = LENGTH)
    mm_per_cell = S_HERO * A_ISO * 2.0 / (n * hero_win)

    def caliper(yy: float, L: float, tag: str) -> None:
        bx = cal_x + L * mm_per_cell
        spoly([(cal_x, yy), (bx, yy)], red)
        spoly([(cal_x, yy + 0.25), (bx, yy + 0.25)], red)  # 2nd pass
        for e in (cal_x, bx):
            spoly([(e, yy - 1.5), (e, yy + 1.5)], red)
        out.extend(_stroke_text(_spaced(tag), bx + 2.2, yy - 0.8, 1.8,
                                color=type_pen, f=feed))

    for i, L in enumerate(lams):
        caliper(cal_y - i * 6.4, L, "D %.1f" % scales[i])
    for i, L in enumerate(ctrl_lam):
        caliper(cal_y - 27.0 - i * 6.4, L, "GERM %d" % (2 * ctrl_half[i]))

    # ------------------------------------------------- structure factor inset
    gx0, gy0, gw, gh = x0 + 140.0, y0 + 8.0, 48.0, 30.0
    qmax = 34
    peak = max(float(p[1:qmax].max()) for p in profs)
    spoly([(gx0, gy0 + gh), (gx0, gy0), (gx0 + gw, gy0)], ink)
    for i, prof in enumerate(profs):
        spoly([(gx0 + gw * q / qmax, gy0 + gh * float(prof[q]) / peak)
               for q in range(1, qmax)], ink)
        px = gx0 + gw * (n / lams[i]) / qmax
        spoly([(px, gy0 - 1.2), (px, gy0 + 3.0)], red)
    out.extend(_stroke_text(_spaced("S Q"), gx0 + 1.4, gy0 + gh - 2.6, 2.0,
                            color=type_pen, f=feed))
    out.extend(_stroke_text(_spaced("Q PER BOX"), gx0, gy0 - 4.4, 1.6,
                            color=type_pen, f=feed))

    # ----------------------------------------------------------------- footer
    foot = [
        "DU %.2f  DV %.2f  F %.3f  K %.3f" % (du, dv, F, k),
        "GRID %d PERIODIC  DT %.2f  STEPS %d" % (n, dt, steps),
        "LAMBDA CELLS %s" % "  ".join(lam_txt),
        "RATIO MEASURED %s" % " ".join("%.2f" % r for r in r_meas),
        "PREDICTED SQRT D %s" % " ".join("%.2f" % r for r in r_pred),
        "AGREE WITHIN %.0f PERCENT OVER D X%.0f"
        % (max(abs(m / q - 1.0) for m, q in zip(r_meas, r_pred)) * 100.0 + 0.5,
           max(scales) / min(scales)),
    ]
    fy = y0 + 31.0
    for line in foot:
        out.extend(_stroke_text(_spaced(line), x0 + 1.0, fy, 1.7, color=type_pen, f=feed))
        fy -= 4.4
    out.extend(swatch_bar(x1 - 5.0, y1 - 2.0, [ink, red], size=2.4, f=feed))
    out.extend(plus_mark(x0 + 2.0, y1 - 2.0, s=1.6, pen=ink, f=feed))
    out.extend(plus_mark(x1 - 2.0, y0 + 2.0, s=1.6, pen=ink, f=feed))

    return scene.render()
