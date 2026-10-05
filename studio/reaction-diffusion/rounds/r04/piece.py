"""BACTERIO — Sottsass drew it, Turing explained it (round 04).

ORDER: **SCATTERED PRIMITIVES ON A STRICT GROUND.**
CANON: **MEMPHIS GROUP** (Sottsass, Milan, 1980s).

THE JOKE, and it is true. Sottsass's *Bacterio* laminate — the black scattered
squiggle that Abet Laminati printed by the mile and Memphis glued to every
sideboard of the decade — is, structurally, a reaction-diffusion field: one
pitch, no direction, dislocations everywhere. Memphis spent a decade printing
Turing patterns on furniture. This plate is that laminate, except every squiggle
on it came out of the actual PDE, and the ground it is printed on is the
prediction it obeys.

    Red confetti went in. Black Bacterio came out. The green rules are spaced
    at the PREDICTED wavelength — one squiggle period per cell, all the way
    across, or the theory is wrong.

That is the whole plate. No relief, no parameter deck, no axis inset, no
calipers: the strict ground IS the ruler, and the confetti IS the seed set, so
the two things this studio would normally draw as a figure are already the two
halves of the Memphis order.

THE MECHANISM, exactly. Gray-Scott on one lattice, the whole sheet:

    du/dt = Du(x) lap u  -  u v^2  +  F (1 - u)
    dv/dt = Dv(x) lap v  +  u v^2  - (F + k) v

explicit forward Euler, 5-point Laplacian, periodic in y, zero-flux in x. Both
diffusivities ramp GEOMETRICALLY along x by 8x across the sheet with Du:Dv, F,
k, dt and the seeded noise held fixed. Scaling both diffusivities by s is an
exact similarity of the PDE under x -> x sqrt(s), so the pitch must follow
sqrt(D) wherever D varies slowly compared to the pitch itself. Nothing imposes a
length anywhere: D has units of length^2/time.

THE GROUND IS THE PREDICTION. One wavelength is measured, once, at the middle of
the sheet. Every green rule after that is placed by integrating dx / lambda(x)
with lambda(x) = lambda_mid * sqrt(D(x)/D_mid) — so the rules are pure theory,
spaced wider and wider to the right. The black field never saw them.

THE CONTROL IS THE CONFETTI. The germs are scattered where they like, in three
shapes and over a 6x size range, because a Memphis ground is violated by
confetti that obeys no alignment — and because a Gray-Scott germ is exactly
that: a finite blob dropped on a uniform state. Two of them sit at the same x,
hence the same D, at 6 and 38 cells across. The pitch that grew out of each is
the same. Six times the seed, one pitch.

Pens, four, as flat categories — the canon suspends the scarce-accent rule:
black = the field that grew. red = the germs, drawn at true scale exactly as
they were seeded. green = the ground, i.e. the prediction. blue = type and its
slab. Declared flat: Memphis is a flat canon and the depth here is layering —
the germs knock out of the field, the field runs over the ground.
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
    _text_width,
    fill_rect,
    giant_type,
    giant_type_width,
    squiggle,
)

Bounds = Tuple[float, float, float, float]

INK, RED, GRN, BLU = 0, 1, 2, 3


# ---------------------------------------------------------------- the solver
def _gray_scott_ramped(F, k, DU, DV, dt, steps, u0, v0):
    """Explicit Euler; periodic in y, zero-flux in x (the ramp lives in x, and a
    periodic seam there would be a discontinuity)."""
    import numpy as np

    u, v = u0.copy(), v0.copy()
    dtf, Ff, kf = np.float32(dt), np.float32(F), np.float32(k)
    du_, dv_ = DU[None, :], DV[None, :]

    def lap(a, out):
        np.add(np.roll(a, 1, 0), np.roll(a, -1, 0), out=out)
        out[:, 1:] += a[:, :-1]
        out[:, 0] += a[:, 0]
        out[:, :-1] += a[:, 1:]
        out[:, -1] += a[:, -1]
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


def _pitch_box(V, iso, mm_per_cell) -> float:
    """Local wavelength from level crossings along BOTH axes — orientation free.

    A locally uniaxial stripe field of wavelength L at angle t crosses a level
    2|cos t| / L times per unit length along x and 2|sin t| / L along y, so
    dx^2 + dy^2 = 4 / L^2 and L = 2 / sqrt(dx^2 + dy^2) whatever t is. That
    matters here: a ramp gives the stripes a local grain, and a one-axis count
    would read the grain instead of the pitch. Local in x, so it never averages
    over a range of D the way a windowed FFT does.
    """
    import numpy as np

    B = (V > iso).astype(np.int8)
    h, w = B.shape
    if h < 4 or w < 4:
        return float("nan")
    dy = np.abs(np.diff(B, axis=0)).sum() / (h * w * mm_per_cell)
    dx = np.abs(np.diff(B, axis=1)).sum() / (h * w * mm_per_cell)
    return 2.0 / math.sqrt(max(dx * dx + dy * dy, 1e-12))


def _decimate(pts: Sequence[Tuple[float, float]], d: float):
    out = [pts[0]]
    for p in pts[1:-1]:
        if (p[0] - out[-1][0]) ** 2 + (p[1] - out[-1][1]) ** 2 >= d * d:
            out.append(p)
    out.append(pts[-1])
    return out


# --------------------------------------------------------------------- piece
def studio_bacterio(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
    mm_per_cell: float = 1.0,
    F: float = 0.030,
    k: float = 0.057,
    du: float = 0.16,
    dv: float = 0.08,
    dt: float = 0.75,
    steps: int = 6000,
    s_lo: float = 0.30,
    s_hi: float = 2.00,
    noise: float = 0.02,
    iso_frac: float = 0.46,
    n_germ: int = 12,
    germ_lo: int = 3,
    germ_hi: int = 19,
    sky: float = 74.0,
    title: str = "BACTERIO",
    feed: int = 2000,
) -> List[GCodeCommand]:
    """BACTERIO — the Memphis laminate, solved.

    One Gray-Scott field on a diffusivity ramp fills the sheet; red confetti
    germs of three shapes over a 6x size range started it; the green ground is
    ruled at the PREDICTED wavelength so one squiggle period fits each cell all
    the way across. Four pens as flat categories, Memphis.
    """
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    ink, red = INK % colors, RED % colors
    grn = GRN % colors if colors >= 3 else ink
    blu = BLU % colors if colors >= 4 else ink

    # ------------------------------------------------------------ the physics
    nx, ny = int(W / mm_per_cell), int((H - sky) / mm_per_cell)
    S = (s_lo * (s_hi / s_lo) ** (np.arange(nx) / max(1, nx - 1))).astype(np.float32)
    DU = (du * S * dt).astype(np.float32)
    DV = (dv * S * dt).astype(np.float32)

    rs = np.random.RandomState(rng.randint(0, 10**6))
    nz = rs.normal(0.0, noise, (ny, nx)).astype(np.float32)
    u0 = np.ones((ny, nx), np.float32) + nz
    v0 = np.zeros((ny, nx), np.float32) - nz

    # --- the confetti: germs scattered where they like, three shapes, 6x sizes.
    #     Two are placed at the SAME x (hence the same D) at the extreme sizes:
    #     that pair is the control and it is drawn like all the others.
    GY0, GY1 = 14.0, H - sky - 14.0
    ctrl_x = 0.30 * W
    band = H - sky
    germs = [(ctrl_x, 0.22 * band, germ_lo, 0), (ctrl_x, 0.62 * band, germ_hi, 1)]
    for i in range(n_germ - 2):
        germs.append(
            (
                rng.uniform(0.04, 0.96) * W,
                rng.uniform(GY0, GY1),
                int(round(rng.uniform(germ_lo + 1, germ_hi - 2))),
                (i + 2) % 3,
            )
        )
    II, JJ = np.mgrid[0:ny, 0:nx]
    for gx, gy, half, shape in germs:
        j = int(gx / mm_per_cell)
        i = int(gy / mm_per_cell)
        if shape == 0:  # square
            m = (abs(JJ - j) <= half) & (abs(II - i) <= half)
        elif shape == 1:  # disc
            m = (JJ - j) ** 2 + (II - i) ** 2 <= half * half
        else:  # triangle
            m = (II - i >= -half) & (II - i <= half - 2 * abs(JJ - j))
        u0[m] = 0.50
        v0[m] = 0.25

    V = _gray_scott_ramped(F, k, DU, DV, dt, steps, u0, v0)

    # ------------------------------------------------- measure: ONE number, mid sheet
    lo_, hi_ = float(V.min()), float(V.max())
    iso = lo_ + (hi_ - lo_) * iso_frac
    strips = 13
    sw = nx // strips
    lam_strip = [
        _pitch_box(V[:, t * sw : (t + 1) * sw], iso, mm_per_cell) for t in range(strips)
    ]
    j_ref = nx // 2
    lam_ref = lam_strip[strips // 2]
    s_ref = float(S[j_ref])

    def lam_pred(mx: float) -> float:
        s = float(S[min(nx - 1, max(0, int(mx / mm_per_cell)))])
        return lam_ref * math.sqrt(s / s_ref)

    # agreement, strip by strip, across the whole sheet
    agree = (
        max(
            abs(lam_strip[t] / lam_pred((t + 0.5) * sw * mm_per_cell) - 1.0)
            for t in range(strips)
        )
        * 100.0
    )

    # the control: pitch inside the grain around each of the two extreme germs,
    # both at the same x and therefore the same D
    def pitch_box(gy: float, half_mm: float = 30.0) -> float:
        i0 = max(0, int((gy - half_mm) / mm_per_cell))
        i1 = min(ny, int((gy + half_mm) / mm_per_cell))
        j0 = max(0, int((ctrl_x - half_mm) / mm_per_cell))
        j1 = min(nx, int((ctrl_x + half_mm) / mm_per_cell))
        return _pitch_box(V[i0:i1, j0:j1], iso, mm_per_cell)

    ctrl = (pitch_box(0.22 * band), pitch_box(0.62 * band))
    sizes = sorted(2 * g[2] for g in germs)

    # ------------------------------------------------------------- the scene
    scene = Scene3D(rng, bounds, feed=feed, tip=0.35, px=(300, 300), pad=4.0, fit="none")
    out = scene.out
    paper = Rect(x0 + 0.3, y0 + 0.3, x1 - 0.3, y1 - 0.3)

    def spoly(pts, pen: int) -> None:
        for run in clip(list(pts), paper, keep="inside"):
            scene.poly(run, pen=pen)

    # ------------------------------------------------------------------ type
    gh = 27.0
    max_w = W - 9.0
    while giant_type_width(title, gh) > max_w and gh > 8.0:
        gh -= 0.5
    ty = y1 - gh - 3.0
    cap = [
        (_spaced("SOTTSASS DREW IT. TURING EXPLAINED IT."), x0, ty - 7.8, 2.5, blu),
        (_spaced("GREEN RULES ARE THE PREDICTION."), x0, ty - 14.6, 2.4, grn),
        (_spaced("COUNT THE SQUIGGLES BETWEEN THEM."), x0, ty - 19.4, 2.4, grn),
        (
            _spaced("%d SEEDS. %dX THE SIZE RANGE. ONE PITCH." % (n_germ, sizes[-1] // sizes[0])),
            x0,
            ty - 26.2,
            2.4,
            red,
        ),
        (
            _spaced("THE MEMPHIS LAMINATE IS A REACTION-DIFFUSION FIELD AND"),
            x0,
            ty - 33.4,
            1.8,
            ink,
        ),
        (_spaced("EVERY SQUIGGLE HERE CAME OUT OF THE ACTUAL PDE."), x0, ty - 37.4, 1.8, ink),
        (
            _spaced(
                "GRAY-SCOTT  DU %.2f  DV %.2f  F %.3f  K %.3f" % (du, dv, F, k)
            ),
            x0,
            ty - 43.4,
            1.7,
            ink,
        ),
        (
            _spaced(
                "D RAMPED X%.0f ALONG X.  DT %.2f.  STEPS %d." % (s_hi / s_lo, dt, steps)
            ),
            x0,
            ty - 47.4,
            1.7,
            ink,
        ),
        (
            _spaced(
                "PITCH %.1f MM MID SHEET. SQRT D HOLDS TO %.0f PCT."
                % (lam_ref, agree + 0.5)
            ),
            x0,
            ty - 51.4,
            1.7,
            ink,
        ),
        (
            _spaced(
                "SAME D, SEEDS %d AND %d CELLS, PITCH %.1f AND %.1f MM."
                % (2 * germ_lo, 2 * germ_hi, ctrl[0], ctrl[1])
            ),
            x0,
            ty - 55.4,
            1.7,
            ink,
        ),
    ]
    scene.halo_labels(cap)

    # --------------------------------------------- the ground: THE PREDICTION
    # rules placed by integrating dx / lambda(x) — pure theory, never measured
    xr, acc, rules = 0.0, 0.0, []
    while xr < W:
        step = 0.5
        acc += step / max(lam_pred(xr), 0.6)
        xr += step
        if acc >= 1.0:
            acc -= 1.0
            rules.append(xr)
    for rx in rules:
        spoly([(x0 + rx, y0), (x0 + rx, y1)], grn)
    spoly([(x0, y1 - sky), (x1, y1 - sky)], grn)

    # ------------------------------------------------------- BACTERIO, solved
    fx = [x0 + j * mm_per_cell for j in range(nx)]
    fy = [y0 + i * mm_per_cell for i in range(ny)]
    segs = _marching_squares(V.astype(float).tolist(), fx, fy, iso)
    for ch in _chain_segments(segs):
        if len(ch) >= 6:
            spoly(_decimate(ch, 0.5), ink)

    # ------------------------------------------------- the confetti that did it
    for gx, gy, half, shape in germs:
        g = half * mm_per_cell
        cx_, cy_ = x0 + gx, y0 + gy
        if shape == 0:
            ring = [
                (cx_ - g, cy_ - g),
                (cx_ + g, cy_ - g),
                (cx_ + g, cy_ + g),
                (cx_ - g, cy_ + g),
            ]
        elif shape == 1:
            ring = [
                (cx_ + g * math.cos(2 * math.pi * q / 40), cy_ + g * math.sin(2 * math.pi * q / 40))
                for q in range(40)
            ]
        else:
            ring = [(cx_ - g, cy_ - g), (cx_ + g, cy_ - g), (cx_, cy_ + g)]
        spoly(ring + [ring[0]], red)
        spoly([(q[0] + 0.30, q[1]) for q in ring + [ring[0]]], red)

    # ------------------------------------------------- the slab and the title
    out.extend(
        fill_rect(x0, ty - 5.4, x0 + W * 0.62, ty - 3.2, spacing=0.55, pen=blu, f=feed)
    )
    for c_ in giant_type(title, x0, ty, gh, pen=blu, weight=2.8, tip=0.45, f=feed):
        if c_.x is not None:
            c_.x = min(max(c_.x, x0), x1)
        if c_.y is not None:
            c_.y = min(max(c_.y, y0), y1)
        out.append(c_)
    out.extend(
        squiggle(x0 + W * 0.58, ty - 60.0, W * 0.38, 3.4, waves=3.0, pen=red, f=feed)
    )
    _ = _text_width
    return scene.render()
