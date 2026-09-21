"""VOICING — the rank of pipes a reaction cuts for itself (round 02).

CARRIER: a rank of flue organ pipes, built exactly.

    Every pipe is cut to EIGHT wavelengths of the pattern wrapped around it;
    the red ladder up its front is cut from sqrt(D).

Why this carrier and not a relief, a deck of panels or an S(q) plot (round 01
was all three, and the rubric now calls that the SCIENTIFIC FIGURE failure): an
organ pipe is the one everyday object whose whole job is to take BROADBAND NOISE
in at the mouth and put ONE WAVELENGTH out, with the wavelength set by the pipe
and not by the wind.  That is the Gray-Scott statement, structurally, not by
analogy of appearance:

    wind sheet at the mouth (turbulent, scaleless)   = the seeded noise
    the chiff that starts the pipe speaking          = the germ
    the pipe's cut length                            = the selected wavelength
    the skin the pattern is wrapped on               = the field that grew
    how hard you blow                                = the germ's size

An organ builder cuts a pipe to length to get a note.  Here the reaction cuts
its own pipes, and the rank is what it cut.  A rank of pipes IS a spectrum, so
the S(q) inset of round 01 has no reason to exist and is gone; the three plates
of round 01 are gone; the relief is gone.  Nothing on the sheet is a plot.

THE EXPERIMENT IS THE SKYLINE.  Five pipes, a crossed design:

    D 0.4   |  GERM 8   D 1.0   GERM 50  |   D 2.0
    germ 20 |  --------- all D 1.0 ------|   germ 20

The three middle pipes share D and differ in germ by a factor of six: they come
out the SAME HEIGHT, a flat plateau, over three wildly different red germ blocks
on the chest.  The two outer pipes share the germ and differ in D: they step
down and up.  Read the skyline and you have read the result.

THE FALSIFICATION IS ON THE PIPE.  The black stripes wrapped on each body are
the MEASURED field.  The red ladder is the PREDICTION: eight rungs at
lambda(D 1.0) * sqrt(D / D 1.0).  On the reference pipe the eighth rung lands on
the cut.  On the others it misses by the measurement error - about 2 % over
eight wavelengths, a millimetre and a half.  If sqrt(D) were wrong the ladder
would not fit the pipe, and you would see it without reading a number.

The physics is unchanged from round 01 and still exact: Gray-Scott
(du/dt = Du lap u - u v^2 + F(1-u), dv/dt = Dv lap v + u v^2 - (F+k) v),
explicit Euler, 5-point periodic Laplacian, one shared noise realization, and
lambda measured as N / q* with q* the intensity-weighted first moment of the
radial structure factor.  The domain is periodic in both directions - a torus -
so wrapping it round a cylinder is not a liberty, it is the literal topology of
the simulation; the pattern closes on itself with no seam.

Pens: black = every pipe, every stripe, the chest, the wind, all type.
red = what was PUT IN and what was PREDICTED, and nothing else: the germ blocks
on the chest and the sqrt(D) ladders on the pipes.  Diameters follow the organ
builder's scaling rule (d ~ L^0.72, Toepfer); only LENGTH is data - stated on
the sheet.
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
    _text_width,
    plus_mark,
    swatch_bar,
)

Bounds = Tuple[float, float, float, float]

INK = 0  # black — pipes, stripes, chest, wind, type
RED = 1  # crimson — what was put in (germ) and what was predicted (sqrt D)

# ------------------------------------------------- the one axonometric basis
# Chosen once for a tall standing object: verticals unforeshortened, the ground
# plane raked.  A pipe that must be smaller shrinks its world FOOTPRINT.
A_ISO = 0.500  # screen mm per world unit of (wx - wz)
CD_ISO = 0.260  # screen mm per world unit of (wx + wz), downward
WY_ISO = 1.000  # screen mm per world mm of height

_SQ2 = math.sqrt(2.0)


def _proj(wx: float, wy: float, wz: float) -> Tuple[float, float]:
    return ((wx - wz) * A_ISO, wy * WY_ISO - (wx + wz) * CD_ISO)


def _dep(wx: float, wy: float, wz: float) -> float:
    return (wx + wz) + 0.12 * wy


# ---------------------------------------------------------------- the solver
def _gray_scott(F: float, k: float, du: float, dv: float, dt: float, steps: int, u0, v0):
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
        T *= u
        u += cu * L - dtf * T + (dtf * Ff) * (1.0 - u)
        np.add(np.roll(v, 1, 0), np.roll(v, -1, 0), out=L)
        L += np.roll(v, 1, 1)
        L += np.roll(v, -1, 1)
        L -= 4.0 * v
        v += cv * L + dtf * T - (dtf * (Ff + kf)) * v
    return v


def _lambda_cells(v) -> float:
    """N / q*, with q* the intensity-weighted first moment of S(q) over the
    peak band.  A bare argmax jitters a whole bin between noise realizations."""
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
    qs = max(float((np.arange(lo, hi) * w).sum() / max(w.sum(), 1e-12)), 1e-6)
    return n / qs


# ------------------------------------------------------------------ contours
def _decimate(pts: Sequence[Tuple[float, float]], d: float):
    out = [pts[0]]
    for p in pts[1:-1]:
        if (p[0] - out[-1][0]) ** 2 + (p[1] - out[-1][1]) ** 2 >= d * d:
            out.append(p)
    out.append(pts[-1])
    return out


def _isolines(field, xs, ys, iso: float, min_pts: int, dec: float):
    segs = _marching_squares(field, xs, ys, iso)
    return [_decimate(c, dec) for c in _chain_segments(segs) if len(c) >= min_pts]


# ------------------------------------------------------------------- regions
def _poly_region(corners) -> Region:
    """Convex screen polygon as an intersection of half-planes (inside <= 0)."""
    reg: Optional[Region] = None
    n = len(corners)
    cx = sum(p[0] for p in corners) / n
    cy = sum(p[1] for p in corners) / n
    for i in range(n):
        ax, ay = corners[i]
        bx, by = corners[(i + 1) % n]
        nx, ny = by - ay, ax - bx
        c = -(nx * ax + ny * ay)
        if nx * cx + ny * cy + c > 0:
            nx, ny, c = -nx, -ny, -c
        hp = HalfPlane(nx, ny, c)
        reg = hp if reg is None else (reg & hp)
    return reg


# --------------------------------------------------------------------- piece
def studio_pipe_rank(
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
    noise: float = 0.02,
    iso_frac: float = 0.46,
    mm_per_cell: float = 1.10,
    germ_scale: float = 0.5,
    waves: int = 8,
    germ_ref: int = 10,
    germ_lo: int = 4,
    germ_hi: int = 25,
    n_theta: int = 84,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """VOICING — five pipes a reaction cut for itself.

    Each pipe's speaking length is eight measured wavelengths of the field
    wrapped around its body; the red ladder up its front is eight PREDICTED
    wavelengths from sqrt(D).  Three pipes share D and differ in germ by 6x and
    come out the same height; two share the germ and differ in D and do not.
    """
    import numpy as np

    x0, y0, x1, y1 = bounds
    ink, red = INK % colors, RED % colors
    type_pen = (3 % colors) if colors >= 4 else ink

    # ------------------------------------------------------------ the physics
    rs = np.random.RandomState(rng.randint(0, 10**6))
    nz = rs.normal(0.0, noise, (n, n)).astype(np.float32)  # ONE wind, shared
    cy_, cx_ = int(n * 0.415), int(n * 0.455)  # off-centre: no imposed symmetry

    def seeded(half: int):
        u = np.ones((n, n), np.float32)
        v = np.zeros((n, n), np.float32)
        u[cy_ - half : cy_ + half, cx_ - half : cx_ + half] = 0.50
        v[cy_ - half : cy_ + half, cx_ - half : cx_ + half] = 0.25
        return u + nz, v - nz

    # the crossed design, left to right along the rank: (scale, germ half, tag)
    plan = [
        (0.4, germ_ref, "D 0.4", "%d" % (2 * germ_ref)),
        (1.0, germ_lo, "G %d" % (2 * germ_lo), "%d" % (2 * germ_lo)),
        (1.0, germ_ref, "D 1.0", "%d" % (2 * germ_ref)),
        (1.0, germ_hi, "G %d" % (2 * germ_hi), "%d" % (2 * germ_hi)),
        (2.0, germ_ref, "D 2.0", "%d" % (2 * germ_ref)),
    ]
    REF = 2  # the reference pipe: D 1.0, germ 20
    NP = len(plan)

    fields, lams = [], []
    for s, half, _t, _g in plan:
        u0, v0 = seeded(half)
        v = _gray_scott(F, k, du * s, dv * s, dt, steps, u0, v0)
        fields.append(v)
        lams.append(_lambda_cells(v))
    lam_pred = [lams[REF] * math.sqrt(s / plan[REF][0]) for s, _h, _t, _g in plan]

    # ------------------------------------------------------------- the scene
    scene = Scene3D(rng, bounds, feed=feed, tip=0.35, px=(300, 300), pad=4.0, fit="none")
    out = scene.out
    paper = Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)

    # --- the chest's own frame: E1 runs ALONG the rank (nearly horizontal on
    #     screen, each step slightly nearer), E2 runs toward the viewer (straight
    #     down the screen).  Everything that lies on the chest is placed in it.
    E1 = (1.0, -0.85)
    E2 = (1.0, 1.0)
    CHEST_Y = y0 + 60.0  # screen y of the chest's BACK edge, where the pipes stand
    E1_SX = (E1[0] - E1[1]) * A_ISO  # 0.925 mm right per unit
    DEPTH = 64.0  # chest depth in E2 units -> 0.52 * DEPTH mm of screen
    TH_CHEST = 13.0

    def ground(a: float, b: float, h: float = 0.0) -> Tuple[float, float]:
        wx = a * E1[0] + b * E2[0]
        wz = a * E1[1] + b * E2[1]
        px, py = _proj(wx, h, wz)
        return px + x0, py + CHEST_Y

    # --- rank geometry -------------------------------------------------------
    # screen widths follow the organ builder's scaling (d ~ L^0.72, Toepfer);
    # only LENGTH is data.
    wid = [24.0 * (L / lams[REF]) ** 0.72 for L in lams]
    body = [waves * L * mm_per_cell for L in lams]  # speaking length
    rad = [w / (2.0 * A_ISO * _SQ2) for w in wid]  # world radius

    FOOT, CUT, TOE = 13.0, 6.0, 0.46
    gap = 3.5
    a_of: List[float] = []
    xc = 50.0 + wid[0] / 2.0
    for i, w in enumerate(wid):
        if i:
            xc += wid[i - 1] / 2.0 + gap + w / 2.0
        a_of.append(xc / E1_SX)

    def pipe_pt(i: int, th: float, h: float, rr: Optional[float] = None) -> Tuple[float, float]:
        a = a_of[i]
        r = rad[i] if rr is None else rr
        wx = a * E1[0] + r * math.cos(th)
        wz = a * E1[1] + r * math.sin(th)
        px, py = _proj(wx, h, wz)
        return px + x0, py + CHEST_Y

    # --- occluders: a projected vertical cylinder is convex (ellipse + segment)
    def silhouette(i: int) -> List[Tuple[float, float]]:
        hb, ht = FOOT + CUT, FOOT + CUT + body[i]
        pts = [pipe_pt(i, math.pi * 0.75 + math.pi * j / 24.0, ht) for j in range(25)]
        pts += [pipe_pt(i, -math.pi / 4.0 + math.pi * j / 24.0, 0.0) for j in range(25)]
        return pts

    sils = [_poly_region(silhouette(i)) for i in range(NP)]
    order = sorted(range(NP), key=lambda i: a_of[i] * (E1[0] + E1[1]))  # far -> near

    def emit(pts, pen: int, nearer: Sequence[int] = ()) -> None:
        runs = [list(pts)]
        for j in nearer:
            nxt = []
            for r in runs:
                nxt.extend(clip(r, sils[j], keep="outside"))
            runs = nxt
        for r in runs:
            for rr in clip(r, paper, keep="inside"):
                scene.poly(rr, pen=pen)

    # ------------------------------------------------------------------ type
    lam_txt = ["%.1f" % L for L in lams]
    err = max(abs(lams[i] / lam_pred[i] - 1.0) for i in range(NP)) * 100.0
    A_LO, A_HI = -40.0 / E1_SX, 215.0 / E1_SX
    front_y = ground(a_of[0], DEPTH)[1]

    labels = [
        (_spaced("VOICING"), x0 + 1.0, y1 - 11.0, 9.0, type_pen),
        (_spaced("THE RANK A REACTION CUTS FOR ITSELF"), x0 + 1.0, y1 - 18.8, 2.6, type_pen),
        (_spaced("EVERY PIPE IS EIGHT WAVELENGTHS OF THE"), x0 + 1.0, y1 - 24.8, 1.9, type_pen),
        (_spaced("PATTERN WRAPPED ROUND IT. THE LADDER"), x0 + 1.0, y1 - 29.0, 1.9, type_pen),
        (_spaced("IS CUT FROM SQRT D."), x0 + 1.0, y1 - 33.2, 1.9, type_pen),
        (_spaced("ONE WIND"), x0 + 1.0, front_y + 21.0, 2.6, type_pen),
        (_spaced("NO PITCH IN IT"), x0 + 1.0, front_y + 16.6, 1.7, type_pen),
        (_spaced("RED WENT IN"), x0 + 1.0, front_y + 11.0, 1.7, type_pen),
        (_spaced("BLACK CAME OUT"), x0 + 1.0, front_y + 7.4, 1.7, type_pen),
    ]
    par = [
        "GRAY-SCOTT",
        "DU %.2f  DV %.2f" % (du, dv),
        "F %.3f" % F,
        "K %.3f" % k,
        "GRID %d  PBC" % n,
        "DT %.2f" % dt,
        "STEPS %d" % steps,
        "LAMBDA FROM S Q",
        "LADDER MISS %.0f PCT" % (err + 0.5),
        "TOEPFER SCALING",
        "LENGTH IS DATA",
        "GERMS AT HALF SCALE",
    ]
    py = y0 + 236.0
    for ln in par:
        labels.append((_spaced(ln), x0 + 1.0, py, 1.6, type_pen))
        py -= 4.1
    # nameplates, engraved on the chest's front face under each pipe
    for i, (_s, _h, tag, gtag) in enumerate(plan):
        cxp = a_of[i] * E1_SX + x0
        labels.append(
            (_spaced(tag), cxp - _text_width(_spaced(tag), 1.7) / 2.0,
             front_y - 3.8, 1.7, type_pen)
        )
        labels.append(
            (_spaced(lam_txt[i]), cxp - _text_width(_spaced(lam_txt[i]), 1.5) / 2.0,
             front_y - 8.0, 1.5, type_pen)
        )
    scene.halo_labels(labels)

    # ------------------------------------------------------------- the chest
    emit([ground(A_LO, 0.0), ground(A_HI, 0.0)], ink)  # back edge
    emit([ground(A_LO, DEPTH), ground(A_HI, DEPTH)], ink)  # front top edge
    emit(
        [ground(A_LO, DEPTH, -TH_CHEST), ground(A_HI, DEPTH, -TH_CHEST)], ink
    )  # front bottom edge

    # --- the wind: the shared noise realization at its own zero level, coarse-
    #     grained so the dust is plottable.  White noise is isotropic, so laying
    #     it along the chest is not a distortion.  Every pipe breathes it.
    step = 4.0 * mm_per_cell
    a_s = [A_LO + step * j / E1_SX for j in range(int((A_HI - A_LO) * E1_SX / step) + 1)]
    b_s = [30.0 - step * j for j in range(7)][::-1]
    Wn = [[float(nz[int(b / mm_per_cell) % n, int(a * E1_SX / mm_per_cell) % n]) for a in a_s]
          for b in b_s]
    for ch in _isolines(Wn, a_s, b_s, 0.0, 4, 1.4 / E1_SX):
        emit([ground(a, b) for a, b in ch], ink, order)

    # --- the germs: what was PUT IN, at true scale, in red, on the chest in
    #     front of its pipe (an E2 offset moves straight down the screen).
    GB = 46.0
    for i, (_s, half, _t, _g) in enumerate(plan):
        g = 2 * half * mm_per_cell * germ_scale
        wx = a_of[i] * E1[0] + GB * E2[0]
        wz = a_of[i] * E1[1] + GB * E2[1]
        sq = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
        ring = []
        for dx_, dz_ in sq + [sq[0]]:
            px, py = _proj(wx + dx_ * g, 0.0, wz + dz_ * g)
            ring.append((px + x0, py + CHEST_Y))
        emit(ring, red, order)
        # serpentine fill: a germ is a MASS of reagent, not a frame
        hz = wz - g / 2.0
        flip = False
        while hz <= wz + g / 2.0 + 1e-9:
            row = [(wx - g / 2.0, hz), (wx + g / 2.0, hz)]
            if flip:
                row.reverse()
            pts = []
            for qx, qz in row:
                px, py = _proj(qx, 0.0, qz)
                pts.append((px + x0, py + CHEST_Y))
            emit(pts, red, order)
            flip = not flip
            hz += 5.0

    # ------------------------------------------------------------- the pipes
    for rank_i, i in enumerate(order):
        nearer = order[rank_i + 1 :]
        r = rad[i]
        hb, ht = FOOT + CUT, FOOT + CUT + body[i]
        TL, TR = -math.pi / 4.0, 3.0 * math.pi / 4.0  # the visible front half

        def arc(h, rr, t0=TL, t1=TR, m=24):
            return [pipe_pt(i, t0 + (t1 - t0) * j / m, h, rr) for j in range(m + 1)]

        # foot: a true cone, toe on the chest, flaring to the mouth line
        rt = r * TOE
        for th in (TL, TR):
            emit([pipe_pt(i, th, 0.0, rt), pipe_pt(i, th, FOOT, r)], ink, nearer)
        emit(arc(0.0, rt), ink, nearer)
        emit(arc(0.0, rt, TR, TR + math.pi), ink, nearer)  # toe seated on the chest
        emit(arc(FOOT, r), ink, nearer)

        # mouth: lower lip at the foot line, upper lip at the cut-up, languid
        mw = 0.78
        lip = arc(FOOT, r, math.pi / 4 - mw / 2, math.pi / 4 + mw / 2, 10)
        up = arc(FOOT + CUT, r, math.pi / 4 - mw / 2, math.pi / 4 + mw / 2, 10)
        emit(lip, ink, nearer)
        emit(up, ink, nearer)
        emit([lip[0], up[0]], ink, nearer)
        emit([lip[-1], up[-1]], ink, nearer)
        emit([pipe_pt(i, math.pi / 4, FOOT), pipe_pt(i, math.pi / 4, FOOT + CUT * 0.40)],
             ink, nearer)

        # body silhouette + the open bore at the top
        for th in (TL, TR):
            emit([pipe_pt(i, th, hb), pipe_pt(i, th, ht)], ink, nearer)
        emit(arc(ht, r, TL, TR, 26), ink, nearer)
        emit(arc(ht, r, TR, TR + math.pi, 26), ink, nearer)

        # --- the wrap: THE FIELD, on the pipe's skin.  The domain is a torus,
        #     so the pattern closes round the cylinder with no seam.
        V = fields[i]
        nh = max(8, int(body[i] / mm_per_cell))
        th_g = [TL + (TR - TL) * a / n_theta for a in range(n_theta + 1)]
        h_g = [hb + (ht - hb) * b / nh for b in range(nh + 1)]
        uu = np.array([r * (t - TL) / mm_per_cell for t in th_g])
        ww = np.array([(h - hb) / mm_per_cell for h in h_g])
        U0, W0 = np.floor(uu).astype(int), np.floor(ww).astype(int)
        fu, fw = uu - U0, ww - W0
        Fg = (
            V[np.ix_(W0 % n, U0 % n)] * (1 - fw)[:, None] * (1 - fu)[None, :]
            + V[np.ix_(W0 % n, (U0 + 1) % n)] * (1 - fw)[:, None] * fu[None, :]
            + V[np.ix_((W0 + 1) % n, U0 % n)] * fw[:, None] * (1 - fu)[None, :]
            + V[np.ix_((W0 + 1) % n, (U0 + 1) % n)] * fw[:, None] * fu[None, :]
        )
        lo, hi = float(V.min()), float(V.max())
        for ch in _isolines(Fg.tolist(), th_g, h_g, lo + (hi - lo) * iso_frac, 5, 0.014):
            emit([pipe_pt(i, t, h) for t, h in ch], ink, nearer)

        # --- the ladder: eight PREDICTED wavelengths from sqrt(D), in red, up
        #     the near meridian.  On the reference pipe the last rung lands on
        #     the cut; elsewhere it misses by the measurement error.
        for j in range(1, waves + 1):
            hj = hb + j * lam_pred[i] * mm_per_cell
            if hj > ht + 4.0:
                break
            rung = arc(hj, r, math.pi / 4 - 0.34, math.pi / 4 + 0.34, 8)
            emit(rung, red, nearer)
            if j == waves:
                emit([(p[0] + 0.30, p[1]) for p in rung], red, nearer)

    # ------------------------------------------------------------- furniture
    out.extend(swatch_bar(x1 - 5.0, y1 - 2.0, [ink, red], size=2.4, f=feed))
    out.extend(plus_mark(x0 + 2.0, y1 - 2.0, s=1.6, pen=ink, f=feed))
    out.extend(plus_mark(x1 - 2.0, y0 + 2.0, s=1.6, pen=ink, f=feed))
    return scene.render()
