"""ORBITAL RESONANCE — LATTICE WITH DEFECTS (studio candidate, r03).

ORDER: LATTICE WITH DEFECTS. Not a plot of the belt, not a picture of anything.

    A site's position in the lattice IS its measured semimajor axis, and a
    column is vacant exactly where the period is commensurate with Jupiter's.

One column per orbit, one row per strobe of Jupiter's period. A uniform comb of
test orbits is a perfect lattice; commensurability forbids specific members, so
the lattice carries VACANCY CHANNELS running through it in the time direction,
and around each channel the remaining sites RELAX — every neighbouring column
snakes by exactly the libration the integration measured, at true lattice scale,
with no gain applied. That relaxation field decaying away from each defect is
the whole mechanism: where periods lock, the site cannot hold its place.

The physics is r01's, unchanged: 96 test particles on a uniform comb in
semimajor axis, velocity-Verlet in the planar circular restricted three-body
problem (Sun + Jupiter, mu = 9.5388e-4), 300 Jupiter years, the boxcar-averaged
osculating semimajor axis giving each orbit's libration width. The four crimson
threads are placed by arithmetic alone (Kepler III, a = a_J (q/p)^(2/3)) and run
down the middle of channels the integration emptied.

Contract: resonance_lattice(rng, bounds, colors=3) -> list[GCodeCommand].
Nothing under promptplot/ is modified.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine import HIDE, Scene3D, ScreenThin
from promptplot.generative.engine.kit import _poly, _spaced, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

MU = 9.5388e-4  # m_J / (M_sun + m_J)
AJ_AU = 5.2028  # Jupiter semimajor axis, AU
GM_S = 1.0 - MU

RESONANCES: Tuple[Tuple[int, int], ...] = ((3, 1), (5, 2), (7, 3), (2, 1))


def res_axis(p: int, q: int) -> float:
    """Kepler III: n/n_J = p/q  =>  a = a_J (q/p)^(2/3).  Arithmetic only."""
    return AJ_AU * (q / p) ** (2.0 / 3.0)


# ---------------------------------------------------------------------------
# dynamics (identical to r01 — the numbers this plate stands on)
# ---------------------------------------------------------------------------
def _integrate(a_au, ecc, pom, m0, t_end: float, dt: float, sample_every: int):
    """Velocity-Verlet in the barycentric inertial frame, Jupiter prescribed on a
    circular orbit. Returns (sample dt, A) with A[k, j] = osculating a of j."""
    import numpy as np

    a0 = a_au / AJ_AU
    E = m0 + ecc * np.sin(m0)  # Kepler's equation, Newton
    for _ in range(40):
        E = E - (E - ecc * np.sin(E) - m0) / (1.0 - ecc * np.cos(E))
    xo = a0 * (np.cos(E) - ecc)
    yo = a0 * np.sqrt(1.0 - ecc * ecc) * np.sin(E)
    n = np.sqrt(GM_S / a0**3)
    rr = a0 * (1.0 - ecc * np.cos(E))
    vxo = -n * a0 * a0 / rr * np.sin(E)
    vyo = n * a0 * a0 / rr * np.sqrt(1.0 - ecc * ecc) * np.cos(E)
    c, s = np.cos(pom), np.sin(pom)
    hx, hy = c * xo - s * yo, s * xo + c * yo
    hvx, hvy = c * vxo - s * vyo, s * vxo + c * vyo

    x, y = hx - MU, hy
    vx, vy = hvx, hvy - MU

    def acc(x, y, t):
        ct, st = math.cos(t), math.sin(t)
        dx1, dy1 = x + MU * ct, y + MU * st
        dx2, dy2 = x - (1 - MU) * ct, y - (1 - MU) * st
        r1 = np.sqrt(dx1 * dx1 + dy1 * dy1)
        r2 = np.sqrt(dx2 * dx2 + dy2 * dy2)
        f1 = -(1 - MU) / (r1 * r1 * r1)
        f2 = -MU / (r2 * r2 * r2)
        return f1 * dx1 + f2 * dx2, f1 * dy1 + f2 * dy2

    ax, ay = acc(x, y, 0.0)
    nsteps = int(t_end / dt)
    A = np.zeros((nsteps // sample_every + 1, len(a_au)))
    k = 0
    for i in range(nsteps):
        x = x + vx * dt + 0.5 * ax * dt * dt
        y = y + vy * dt + 0.5 * ay * dt * dt
        t = (i + 1) * dt
        nax, nay = acc(x, y, t)
        vx = vx + 0.5 * (ax + nax) * dt
        vy = vy + 0.5 * (ay + nay) * dt
        ax, ay = nax, nay
        if i % sample_every == 0:
            ct, st = math.cos(t), math.sin(t)
            dx, dy = x + MU * ct, y + MU * st
            dvx, dvy = vx - MU * st, vy + MU * ct
            r1 = np.sqrt(dx * dx + dy * dy)
            inv_a = 2.0 / r1 - (dvx * dvx + dvy * dvy) / GM_S  # vis-viva
            safe = inv_a > 1e-6
            A[k] = np.where(safe, 1.0 / np.where(safe, inv_a, 1.0), np.nan)
            k += 1
    return dt * sample_every, A[:k]


def _mean_series(a_au, dts: float, A):
    """Boxcar the osculating a over one orbital period -> the MEAN semimajor axis
    series (AU) and each orbit's libration width (max - min)."""
    import numpy as np

    n = len(a_au)
    per = 2.0 * math.pi * (a_au / AJ_AU) ** 1.5
    S = np.full(A.shape, np.nan)
    width = np.full(n, np.nan)
    for j in range(n):
        col = A[:, j]
        if not np.all(np.isfinite(col)):
            continue
        w = max(3, int(round(per[j] / dts)))
        sm = np.convolve(col, np.ones(w) / w, mode="same") * AJ_AU
        S[:, j] = sm
        trim = sm[w : len(sm) - w]
        width[j] = float(trim.max() - trim.min()) if trim.size else np.nan
    return S, width


def _fit(text: str, max_w: float, h: float) -> float:
    w = _text_width(text, h)
    return h if w <= max_w else h * max_w / w


def _dots(pts: Sequence[Pt], on: float = 1.4, period: float = 3.2) -> List[List[Pt]]:
    out: List[List[Pt]] = []
    acc = 0.0
    cur: List[Pt] = [pts[0]]
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if (acc % period) <= on:
            if not cur:
                cur = [a]
            cur.append(b)
        else:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


def _colons(text: str, x: float, y: float, h: float, pen, f: int) -> List[GCodeCommand]:
    """The stroke font has no ':' glyph — it advances but draws nothing."""
    sc, adv = h / 6.0, 5.6 * h / 6.0
    out: List[GCodeCommand] = []
    for i, ch in enumerate(text):
        if ch != ":":
            continue
        gx = x + i * adv + 1.9 * sc
        for gy in (1.6 * sc, 4.0 * sc):
            out += _poly([(gx, y + gy), (gx + 0.45 * sc, y + gy)], color=pen, f=f)
    return out


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def resonance_lattice(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_cols: int = 96,
    n_rows: int = 46,
    a_lo: float = 2.26,
    a_hi: float = 3.34,
    ecc: float = 0.18,
    jup_periods: float = 300.0,
    row_step: float = 3.0,
    row_start: float = 24.0,
    dt: float = 0.02,
    sample_every: int = 10,
    wander_drop: float = 0.0197,
    excess_drop: float = 2.4,
    bg_window: float = 0.22,
    shear: float = 0.62,
    rise: float = 0.78,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """ORBITAL RESONANCE as a LATTICE WITH DEFECTS — a site's place in the
    lattice is its measured semimajor axis, the commensurate columns are vacant,
    and the relaxation around each vacancy is the libration, at true scale."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    LAT = 0
    ARITH = 1 % colors if colors > 1 else None
    TYPE = 2 % colors if colors > 1 else None

    # ---- the comb, integrated ---------------------------------------------
    a_au = np.linspace(a_lo, a_hi, n_cols)
    pom = rng.np.uniform(0.0, 2 * math.pi, n_cols)
    m0 = rng.np.uniform(0.0, 2 * math.pi, n_cols)
    dts, A = _integrate(
        a_au, ecc, pom, m0, t_end=jup_periods * 2 * math.pi, dt=dt, sample_every=sample_every
    )
    S, width = _mean_series(a_au, dts, A)

    bg = np.array([np.nanmedian(width[np.abs(a_au - a_au[j]) < bg_window]) for j in range(n_cols)])
    with np.errstate(invalid="ignore", divide="ignore"):
        excess = width / bg
        w = np.fmax(width / wander_drop, (excess - 1.0) / (excess_drop - 1.0))
    vacant = ~np.isfinite(w) | (w >= 1.0)
    for j in range(n_cols):  # a site enclosed by vacancies lies inside the separatrix
        if not vacant[j] and vacant[max(0, j - 3) : j].any() and vacant[j + 1 : j + 4].any():
            vacant[j] = True

    # ---- ONE basis for the whole plate: u across the lattice, v into depth --
    v_span = 0.620 * H / rise
    u_span = W - shear * v_span - 3.0
    ox, oy = x0 + 1.5, y0 + 0.085 * H

    def site(u: float, v: float) -> Pt:
        return (ox + u + shear * v, oy + rise * v)

    def u_of(a: float) -> float:
        return (a - a_lo) / (a_hi - a_lo) * u_span

    rows = [int(round(((row_start + k * row_step) * 2 * math.pi) / dts)) for k in range(n_rows)]
    rows = [min(r, S.shape[0] - 1) for r in rows]

    SX = np.zeros((n_rows, n_cols))
    SY = np.zeros((n_rows, n_cols))
    DEP = np.zeros((n_rows, n_cols))
    for k, ridx in enumerate(rows):
        v = k * (v_span / (n_rows - 1))
        for j in range(n_cols):
            a_kj = S[ridx, j]
            if vacant[j] or not math.isfinite(a_kj):
                SX[k, j], SY[k, j] = site(u_of(a_au[j]), v)
                DEP[k, j] = HIDE  # the site is forbidden: no mark, ever
                continue
            SX[k, j], SY[k, j] = site(u_of(float(a_kj)), v)
            DEP[k, j] = -k  # row 0 is nearest; the lattice recedes into time

    scene = Scene3D(rng, bounds, feed=feed, fit="none", px=(260, 200), tip=0.45)

    # ---- type reserved first: the lattice knocks out around it -------------
    labels: List[Tuple[str, float, float, float, Optional[int]]] = []
    ratio_marks: List[Tuple[str, float, float, float, Optional[int]]] = []
    ty = y1 - 0.055 * H
    h1 = _fit(_spaced("RESONANCE"), 0.36 * W, 0.085 * H)
    labels.append((_spaced("ORBITAL"), x0, ty, h1, TYPE))
    labels.append((_spaced("RESONANCE"), x0, ty - 1.5 * h1, h1, TYPE))
    sub = ty - 1.5 * h1 - 0.038 * H
    for k, line in enumerate(
        (
            "A SITE IS ITS ORBIT. ITS PLACE IS ITS SEMIMAJOR AXIS.",
            "COMMENSURABLE COLUMNS ARE FORBIDDEN. THE REST RELAX.",
        )
    ):
        t = _spaced(line)
        labels.append((t, x0, sub - k * 0.024 * H, _fit(t, 0.38 * W, 0.0145 * H), TYPE))

    for p, q in RESONANCES:  # each ratio at the far head of its own channel
        ar = res_axis(p, q)
        if not (a_lo < ar < a_hi):
            continue
        hx, hy = site(u_of(ar), v_span)
        txt = _spaced("%d:%d" % (p, q))
        lh = 0.021 * H
        lx = min(max(x0, hx - _text_width(txt, lh) / 2), x1 - _text_width(txt, lh))
        labels.append((txt, lx, hy + 0.017 * H, lh, TYPE))
        ratio_marks.append((txt, lx, hy + 0.017 * H, lh, TYPE))

    foot = [
        "CIRCULAR RESTRICTED 3-BODY. MU 9.5388E-4. VERLET DT 0.02. 300 JUPITER YEARS.",
        "ROWS ARE STROBES OF JUPITER. RELAXATION DRAWN AT TRUE LATTICE SCALE.",
        "CRIMSON THREADS PLACED BY ARITHMETIC ALONE. SUN AND JUPITER ONLY.",
    ]
    for k, line in enumerate(foot):
        t = _spaced(line)
        th = _fit(t, 0.52 * W, 0.0115 * H)
        labels.append((t, x1 - _text_width(t, th), y0 + 0.030 * H - k * 0.0155 * H, th, TYPE))
    occ = _spaced("%d OF %d SITES OCCUPIED" % (int((~vacant).sum()), n_cols))
    ho = _fit(occ, 0.30 * W, 0.0165 * H)
    labels.append((occ, x1 - _text_width(occ, ho), y1 - 0.030 * H, ho, TYPE))
    kirk = _spaced("KIRKWOOD 1866")
    hk = _fit(kirk, 0.24 * W, 0.0165 * H)
    labels.append((kirk, x1 - _text_width(kirk, hk), y1 - 0.052 * H, hk, TYPE))

    def _inside(lab) -> bool:
        txt, lx, ly, lh, _p = lab
        return (
            lx >= x0 - 0.01
            and lx + _text_width(txt, lh) <= x1 + 0.01
            and ly >= y0
            and ly + 1.12 * lh <= y1
        )

    labels = [lab for lab in labels if _inside(lab)]
    ratio_marks = [lab for lab in ratio_marks if _inside(lab)]
    scene.halo_labels(labels, pad_x=1.4, pad_y=(0.5, 1.35))

    # ---- THE LATTICE: one declaration. Both line families, native crowd
    #      control, HIDE opening the vacancy channels.
    scene.surface(SX, SY, DEP, pen=LAT, thin=None)

    # ---- CRIMSON: the forbidden set, straight down its own channel ---------
    for p, q in RESONANCES:
        ar = res_axis(p, q)
        if not (a_lo < ar < a_hi):
            continue
        for seg in _dots([site(u_of(ar), 0.0), site(u_of(ar), v_span)]):
            scene.poly(seg, pen=ARITH)
            scene.poly([(px + 0.15, py) for px, py in seg], pen=ARITH)  # 2nd pass

    out = scene.render()
    for txt, lx, ly, lh, pen in ratio_marks:
        out.extend(_colons(txt, lx, ly, lh, pen, feed))
    return out
