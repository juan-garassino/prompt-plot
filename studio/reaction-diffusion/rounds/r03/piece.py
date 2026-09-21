"""RULED — a page that ruled itself (round 03).

ORDER: **LATTICE-WITH-DEFECTS.** Stratified laminae at one pitch, packed edge to
edge, with dislocations where a line ends mid-sheet. Nothing is depicted. There
is no object in the plate that is not the mechanism.

    Everything IMPOSED sits on the module. Everything that GREW ignores it.

THE TWIST. What the viewer already holds: ruled paper — lines at a spacing some
stationer chose, running the way the stationer chose. Substitute the mechanism
and exactly one thing breaks: the spacing is still dictated, the DIRECTION is
not. A Turing field's power sits on a circle in Fourier space — one radius,
every angle — so it has a pitch and no grain. This page ruled itself, kept
perfect pitch, and has no idea which way is across. RULED, both ways.

CANON: SWISS / INTERNATIONAL TYPOGRAPHIC. Chosen because its order is the
argument's opposite number: the strictest grid in the canon hosting a lattice
that will not obey a grid. Module documented in the code (6 x 12 over the
drawable), flush-left display type at poster scale with real weight, red and
black only, radical negative space, a hard module crop, zero ornament. The
tension IS the composition: every red element snaps to a module intersection,
and not one black line does.

THE MECHANISM, exactly. Gray-Scott on one lattice:

    du/dt = Du(x) lap u  -  u v^2  +  F (1 - u)
    dv/dt = Dv(x) lap v  +  u v^2  - (F + k) v

explicit forward Euler, 5-point Laplacian, periodic in y, zero-flux in x. Both
diffusivities are ramped GEOMETRICALLY along x by a factor of ~4.3 across the
sheet, holding Du:Dv, F, k, dt and the seeded noise fixed. Scaling both
diffusivities by s is an exact similarity of the PDE under x -> x sqrt(s), so
the pitch must follow sqrt(D) — locally, wherever D varies slowly compared to
the pitch itself (it changes by under 5 % per wavelength here, printed on the
sheet). Nothing imposes a length: D has units of length^2/time, not length.

WHAT THE RED DOES. Five red calipers, each cut to the PREDICTED local
wavelength, lie on the ruling at five module intersections. They grow left to
right as sqrt(D). If sqrt(D) were wrong they would not span one line pair, and
you would see it without reading a number. Two red squares are the GERMS at
true scale, seeded on the same module column so they sit at the same D, one 6
cells across and one 38: the ruling that grew out of each has the same pitch.
Six times the seed, same spacing — the control, drawn.

Pens: black = the ruling, all type. red = everything imposed — the two germs
and the five predictions. Two pens, one swap.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List, Sequence, Tuple

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from promptplot.models import GCodeCommand  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402
from promptplot.generative.engine import Scene3D  # noqa: E402
from promptplot.generative.engine.geometry import Rect, clip  # noqa: E402
from promptplot.generative.kit import (  # noqa: E402
    _chain_segments,
    _marching_squares,
    _spaced,
    _stroke_text,
    _text_width,
    giant_type,
    giant_type_width,
)

Bounds = Tuple[float, float, float, float]

INK = 0  # black — the ruling, the type
RED = 1  # crimson — everything imposed: the germs, the predictions


# ---------------------------------------------------------------- the solver
def _gray_scott_ramped(F, k, DU, DV, dt, steps, u0, v0):
    """Explicit Euler. Periodic in y (axis 0), ZERO-FLUX in x (axis 1), because
    the diffusivity ramps along x and a periodic seam would be a discontinuity.
    DU, DV are per-column arrays already multiplied by dt."""
    import numpy as np

    u, v = u0.copy(), v0.copy()
    dtf, Ff, kf = np.float32(dt), np.float32(F), np.float32(k)
    du_, dv_ = DU[None, :], DV[None, :]

    def lap(a, out):
        np.add(np.roll(a, 1, 0), np.roll(a, -1, 0), out=out)  # y periodic
        out[:, 1:] += a[:, :-1]
        out[:, 0] += a[:, 0]  # zero flux
        out[:, :-1] += a[:, 1:]
        out[:, -1] += a[:, -1]  # zero flux
        out -= 4.0 * a
        return out

    L = np.empty_like(u)
    T = np.empty_like(u)
    for _ in range(steps):
        np.multiply(v, v, out=T)
        T *= u
        u += du_ * lap(u, L) - dtf * T + (dtf * Ff) * (1.0 - u)
        v += dv_ * lap(v, L) + dtf * T - (dtf * (Ff + kf)) * v
    return v


def _lambda_cells(win):
    """N / q*, q* = intensity-weighted first moment of S(q) over the peak band."""
    import numpy as np

    a = win - win.mean()
    n = min(a.shape)
    a = a[:n, :n]
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


# --------------------------------------------------------------------- piece
def studio_ruled(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    mm_per_cell: float = 1.0,
    F: float = 0.030,
    k: float = 0.057,
    du: float = 0.16,
    dv: float = 0.08,
    dt: float = 0.75,
    steps: int = 6200,
    s_lo: float = 0.25,
    s_hi: float = 2.00,
    noise: float = 0.02,
    iso_frac: float = 0.46,
    cols: int = 6,
    rows: int = 12,
    band_rows: int = 8,
    germ_lo: int = 3,
    germ_hi: int = 19,
    title: str = "RULED",
    feed: int = 2000,
) -> List[GCodeCommand]:
    """RULED — a page that ruled itself: perfect pitch, no direction.

    One Gray-Scott field on a diffusivity ramp. The pitch follows sqrt(D) and
    nothing else; the five red calipers are cut from that prediction, the two
    red germs differ 6x and change nothing. Swiss: everything imposed snaps to
    the module, the ruling never does.
    """
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    ink, red = INK % colors, RED % colors

    # ------------------------------------------------------- the Swiss module
    C = W / cols  # column module
    R = H / rows  # row module
    BAND = band_rows * R  # the ruling is cropped on a module line
    field_top = y0 + BAND

    def mod(ci: float, ri: float) -> Tuple[float, float]:
        return x0 + ci * C, y0 + ri * R

    # ------------------------------------------------------------ the physics
    nx = int(W / mm_per_cell)
    ny = int(BAND / mm_per_cell)
    # geometric ramp in x: lambda ~ sqrt(D), so a geometric D gives a geometric
    # pitch.  D has units length^2/time — no LENGTH is imposed anywhere.
    xs = np.arange(nx) / max(1, nx - 1)
    S = (s_lo * (s_hi / s_lo) ** xs).astype(np.float32)
    DU = (du * S * dt).astype(np.float32)
    DV = (dv * S * dt).astype(np.float32)

    rs = np.random.RandomState(rng.randint(0, 10**6))
    nz = rs.normal(0.0, noise, (ny, nx)).astype(np.float32)
    u0 = np.ones((ny, nx), np.float32) + nz
    v0 = np.zeros((ny, nx), np.float32) - nz

    # germs, ALL on module intersections.  The control pair shares a module
    # COLUMN, so it shares D exactly; their sizes differ 6x.
    germs = [
        (2.0, 6.0, germ_lo),  # control A — 6 cells
        (2.0, 2.0, germ_hi),  # control B — 38 cells, same column, same D
        (4.0, 4.5, 10),
        (5.0, 7.0, 10),
        (0.6, 4.0, 10),
    ]
    germ_xy = []
    for ci, ri, half in germs:
        gx, gy = mod(ci, ri)
        j = int((gx - x0) / mm_per_cell)
        i = int((gy - y0) / mm_per_cell)
        u0[max(0, i - half) : i + half, max(0, j - half) : j + half] = 0.50
        v0[max(0, i - half) : i + half, max(0, j - half) : j + half] = 0.25
        germ_xy.append((gx, gy, half))

    V = _gray_scott_ramped(F, k, DU, DV, dt, steps, u0, v0)

    # ---------------------------------------------------------- measurement
    # five stations on module intersections, left to right and stepping down:
    # a local window round each gives the MEASURED pitch there.
    stations = [(0.75, 6.4), (1.85, 5.2), (2.95, 4.0), (4.05, 2.8), (5.15, 1.6)]
    win = 48
    lam_meas, lam_pred, st_xy = [], [], []
    for ci, ri in stations:
        sx, sy = mod(ci, ri)
        j = int((sx - x0) / mm_per_cell)
        i = int((sy - y0) / mm_per_cell)
        j0 = min(max(0, j - win // 2), nx - win)
        i0 = min(max(0, i - win // 2), ny - win)
        lam_meas.append(_lambda_cells(V[i0 : i0 + win, j0 : j0 + win]) * mm_per_cell)
        st_xy.append((sx, sy, j))
    ref = len(stations) // 2
    for _n, (_c, _r) in enumerate(stations):
        lam_pred.append(lam_meas[ref] * math.sqrt(S[st_xy[_n][2]] / S[st_xy[ref][2]]))
    agree = max(abs(m / p - 1.0) for m, p in zip(lam_meas, lam_pred)) * 100.0
    # how fast D changes per wavelength — the adiabatic condition, measured
    grad = (math.log(s_hi / s_lo) / W) * 0.5 * lam_meas[ref] * 100.0
    # the control: pitch in the grain grown from each of the two germs
    ctrl = []
    for gi in (0, 1):
        gx, gy, _h = germ_xy[gi]
        j = int((gx - x0) / mm_per_cell)
        i = int((gy - y0) / mm_per_cell)
        j0 = min(max(0, j - win // 2), nx - win)
        i0 = min(max(0, i - win // 2), ny - win)
        ctrl.append(_lambda_cells(V[i0 : i0 + win, j0 : j0 + win]) * mm_per_cell)

    # ------------------------------------------------------------- the scene
    scene = Scene3D(rng, bounds, feed=feed, tip=0.35, px=(300, 300), pad=4.0, fit="none")
    out = scene.out
    paper = Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)

    def spoly(pts, pen: int) -> None:
        for run in clip(list(pts), paper, keep="inside"):
            scene.poly(run, pen=pen)

    # ------------------------------------------------------------------ type
    # Swiss: flush left on the module, ONE huge element, hairline everything else.
    gh = 34.0
    while giant_type_width(title, gh) > W - 2.0 and gh > 8.0:
        gh -= 0.5
    ty = y1 - gh - 4.0
    cap = [
        (_spaced("A PAGE THAT RULED ITSELF"), x0, ty - 7.6, 3.4, ink),
        (_spaced("THE SPACING IS DICTATED. THE DIRECTION IS NOT."), x0, ty - 13.4, 2.1, ink),
        (_spaced("RED IS IMPOSED AND SITS ON THE MODULE."), x0, ty - 20.6, 2.1, ink),
        (_spaced("BLACK GREW AND IGNORES IT."), x0, ty - 25.2, 2.1, ink),
        (_spaced("SWISS   LATTICE WITH DEFECTS"), x0, y0 + 3.0, 2.1, ink),
        (
            _spaced("PITCH FOLLOWS SQRT D"),
            x1 - _text_width(_spaced("PITCH FOLLOWS SQRT D"), 2.1),
            y0 + 3.0,
            2.1,
            ink,
        ),
    ]
    par = [
        "GRAY-SCOTT  DU %.2f  DV %.2f  F %.3f  K %.3f" % (du, dv, F, k),
        "D RAMPED X%.1f ALONG X  DT %.2f  STEPS %d" % (s_hi / s_lo, dt, steps),
        "D CHANGES %.0f PCT PER WAVELENGTH" % grad,
        "PITCH %s MM" % "  ".join("%.1f" % L for L in lam_meas),
        "RED IS SQRT D  AGREES WITHIN %.0f PCT" % (agree + 0.5),
        "GERMS %d AND %d CELLS SAME D  PITCH %.1f AND %.1f"
        % (2 * germ_lo, 2 * germ_hi, ctrl[0], ctrl[1]),
        "MODULE %d X %d" % (cols, rows),
    ]
    py = ty - 34.0
    for ln in par:
        cap.append((_spaced(ln), x0, py, 1.8, ink))
        py -= 4.4
    scene.halo_labels(cap)

    # ------------------------------------------------------------- the ruling
    # isolines of v: the laminae.  Cropped hard on the band's module line.
    fx = [x0 + j * mm_per_cell for j in range(nx)]
    fy = [y0 + i * mm_per_cell for i in range(ny)]
    lo, hi = float(V.min()), float(V.max())
    segs = _marching_squares(V.astype(float).tolist(), fx, fy, lo + (hi - lo) * iso_frac)
    for ch in _chain_segments(segs):
        if len(ch) >= 6:
            spoly(_decimate(ch, 0.5), ink)
    # the crop is a Swiss decision, so it is a drawn line
    spoly([(x0, field_top), (x1, field_top)], ink)

    # ------------------------------------------------ red: everything imposed
    # the germs, at TRUE scale, on their module intersections
    for gx, gy, half in germ_xy[:2]:
        g = 2 * half * mm_per_cell
        ring = [
            (gx - g / 2, gy - g / 2),
            (gx + g / 2, gy - g / 2),
            (gx + g / 2, gy + g / 2),
            (gx - g / 2, gy + g / 2),
        ]
        spoly(ring + [ring[0]], red)
        spoly([(q[0] + 0.30, q[1]) for q in ring + [ring[0]]], red)  # 2nd pass
        spoly([(gx - g / 2, gy), (gx + g / 2, gy)], red)  # centre cross
        spoly([(gx, gy - g / 2), (gx, gy + g / 2)], red)

    # the five calipers: one PREDICTED wavelength each, lying on the ruling
    for idx, (sx, sy, _j) in enumerate(st_xy):
        L = lam_pred[idx]
        spoly([(sx, sy), (sx + L, sy)], red)
        spoly([(sx, sy + 0.30), (sx + L, sy + 0.30)], red)
        for e in (sx, sx + L):
            spoly([(e, sy - 3.0), (e, sy + 3.0)], red)
            spoly([(e + 0.30, sy - 3.0), (e + 0.30, sy + 3.0)], red)

    # ---------------------------------------------------- the one huge element
    out.extend(giant_type(title, x0, ty, gh, pen=ink, weight=2.6, tip=0.42, f=feed))
    for t_, lx_, ly_, lh_, pen_ in cap[-2:]:
        out.extend(_stroke_text(t_, lx_, ly_, lh_, color=pen_, f=feed))
    return scene.render()
