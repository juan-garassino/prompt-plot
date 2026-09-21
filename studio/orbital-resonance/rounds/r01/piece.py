"""ORBITAL RESONANCE — SMALL INTEGERS EMPTY THE BELT (studio candidate, r01).

The asteroid belt seen from above, drawn as real orbits. A uniform comb of test
particles is integrated in the planar circular restricted three-body problem
(Sun + Jupiter, mu = 9.5388e-4) with velocity-Verlet; each particle's osculating
semimajor axis is boxcar-averaged over one orbital period and its LIBRATION WIDTH
(max - min of the mean a) is measured. An orbit that holds its lane is drawn as a
solid fine arc at its own semimajor axis; as the libration grows the arc's dashes
open up; past threshold it is not drawn at all. The voids that appear are the
Kirkwood gaps, and five dotted crimson arcs laid at a_J*(q/p)^(2/3) -- pure
arithmetic, no integration -- land inside them.

ONE radial scale governs every mark on the sheet: no second scale, no scale break
(the flat-view analogue of the house one-shared-axonometric-basis law).

Contract: orbital_resonance_belt(rng, bounds, colors=3) -> list[GCodeCommand].
Nothing under promptplot/ is modified.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine import Scene3D
from promptplot.generative.engine.kit import _poly, _spaced, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# --- physical constants -----------------------------------------------------
MU = 9.5388e-4  # m_J / (M_sun + m_J)
AJ_AU = 5.2028  # Jupiter semimajor axis, AU  (the ONE length unit)
GM_S = 1.0 - MU  # heliocentric GM in units where G(M_sun + m_J) = 1

# interior mean-motion resonances with Jupiter; p:q = asteroid orbits : Jupiter orbits
RESONANCES: Tuple[Tuple[int, int], ...] = ((4, 1), (3, 1), (5, 2), (7, 3), (2, 1))


def res_radius(p: int, q: int) -> float:
    """Kepler III: n/n_J = p/q  =>  a = a_J (q/p)^(2/3).  Arithmetic only."""
    return AJ_AU * (q / p) ** (2.0 / 3.0)


# ---------------------------------------------------------------------------
# dynamics
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

    # barycentric: Sun at -mu(cos t, sin t), Jupiter at (1-mu)(cos t, sin t)
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


def _libration(a_au, dts: float, A):
    """Boxcar the osculating a over one orbital period -> mean a and libration
    width (max - min), both in AU. NaN where the particle was lost."""
    import numpy as np

    n = len(a_au)
    per = 2.0 * math.pi * (a_au / AJ_AU) ** 1.5
    amean = np.full(n, np.nan)
    width = np.full(n, np.nan)
    for j in range(n):
        col = A[:, j]
        if not np.all(np.isfinite(col)):
            continue
        w = max(3, int(round(per[j] / dts)))
        sm = np.convolve(col, np.ones(w) / w, mode="valid") * AJ_AU
        amean[j] = float(sm.mean())
        width[j] = float(sm.max() - sm.min())
    return amean, width


# ---------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------
def _arc_runs(sun: Pt, radius: float, box: Bounds, step_mm: float = 1.6) -> List[List[Pt]]:
    """Polyline runs of the circle of ``radius`` about ``sun`` that lie in ``box``
    (the Sun is below the sheet, so only the upper half can be visible)."""
    sx, sy = sun
    bx0, by0, bx1, by1 = box
    dth = min(0.05, step_mm / max(1e-6, radius))
    th = -math.pi / 2
    runs: List[List[Pt]] = []
    cur: List[Pt] = []
    while th <= math.pi / 2 + 1e-9:
        px, py = sx + radius * math.sin(th), sy + radius * math.cos(th)
        if bx0 <= px <= bx1 and by0 <= py <= by1:
            cur.append((px, py))
        elif cur:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
        th += dth
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _dash(
    runs: Sequence[Sequence[Pt]], on: float, period: float, phase: float = 0.0
) -> List[List[Pt]]:
    """Fixed dash length, growing gap — the plotter's density ramp. period <= on
    passes through solid. ``phase`` de-registers neighbouring arcs."""
    if period <= on * 1.02:
        return [list(r) for r in runs]
    out: List[List[Pt]] = []
    for pts in runs:
        acc = phase
        cur: List[Pt] = [pts[0]] if (acc % period) <= on else []
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


def _arc_point(sun: Pt, radius: float, x: float) -> Optional[Pt]:
    """Point on the upper arc of ``radius`` about ``sun`` at abscissa ``x``."""
    dx = x - sun[0]
    if abs(dx) >= radius:
        return None
    return (x, sun[1] + math.sqrt(radius * radius - dx * dx))


def _fit(text: str, max_w: float, h: float) -> float:
    """Shrink a cap height so the string can never leave the drawable."""
    w = _text_width(text, h)
    return h if w <= max_w else h * max_w / w


def _colons(text: str, x: float, y: float, h: float, pen, f: int) -> List[GCodeCommand]:
    """The stroke font has no ':' glyph (it advances but draws nothing). Emit the
    two dots by hand so ratio labels read as ratios."""
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
def orbital_resonance_belt(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_orbits: int = 225,
    a_lo: float = 1.70,
    a_hi: float = 3.80,
    ecc: float = 0.18,
    jup_periods: float = 300.0,
    dt: float = 0.02,
    sample_every: int = 10,
    a_bottom: float = 1.32,
    a_top: float = 3.78,
    apex: float = -0.12,
    lane_drop: float = 2.1,
    excess_drop: float = 2.4,
    bg_window: float = 0.22,
    dash_on: float = 5.2,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """ORBITAL RESONANCE — a uniform comb of orbits, emptied at integer period
    ratios. Black = the integrated dynamics, crimson = the arithmetic, and the
    blank paper between them is the result."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BELT = 0
    ARITH = 1 % colors if colors > 1 else None
    TYPE = 2 % colors if colors > 1 else None

    # ---- ONE radial scale for the whole sheet ------------------------------
    S = H / (a_top - a_bottom)  # mm per AU
    sun = (x0 + apex * W, y0 - a_bottom * S)
    box = (x0 + 0.4, y0 + 0.4, x1 - 0.4, y1 - 0.4)

    # ---- integrate the comb ------------------------------------------------
    a_au = np.linspace(a_lo, a_hi, n_orbits)
    pom = rng.np.uniform(0.0, 2 * math.pi, n_orbits)  # longitude of perihelion
    m0 = rng.np.uniform(0.0, 2 * math.pi, n_orbits)  # mean anomaly at t = 0
    phase = rng.np.uniform(0.0, 40.0, n_orbits)  # dash phase, de-registers arcs
    dts, A = _integrate(
        a_au, ecc, pom, m0, t_end=jup_periods * 2 * math.pi, dt=dt, sample_every=sample_every
    )
    amean, width = _libration(a_au, dts, A)

    # ---- the two physical scales that decide whether an orbit is drawn -----
    pitch = (a_hi - a_lo) / (n_orbits - 1)  # AU between neighbouring lanes
    bg = np.array(
        [np.nanmedian(width[np.abs(a_au - a_au[j]) < bg_window]) for j in range(n_orbits)]
    )
    with np.errstate(invalid="ignore", divide="ignore"):
        excess = width / bg  # louder than its non-resonant neighbours?
        lanes = width / (lane_drop * pitch)  # how many lanes does it wander?
        res = np.clip((excess - 1.0) / (excess_drop - 1.0), 0.0, 2.0)
        w = np.fmax(lanes, res)  # drops the orbit
        # ink fades FASTER than the orbit dies, so every void arrives with a
        # visible shoulder of fraying arcs -- the gap edge is soft in nature too
        w_ink = np.fmax(0.45 * lanes, np.clip((excess - 1.0) / 0.7, 0.0, 2.0))
    drop = ~np.isfinite(w) | (w >= 1.0)

    # morphological closing: a lane enclosed by dropped lanes sits INSIDE a
    # separatrix (the stable island centre) and belongs to the resonance zone.
    closed = drop.copy()
    for j in range(n_orbits):
        if not drop[j] and drop[max(0, j - 4) : j].any() and drop[j + 1 : j + 5].any():
            closed[j] = True
    duty = np.clip(1.0 - 0.85 * np.nan_to_num(w_ink, nan=1.0), 0.20, 1.0)

    scene = Scene3D(rng, bounds, feed=feed, fit="none")
    labels: List[Tuple[str, float, float, float, Optional[int]]] = []
    ratio_marks: List[Tuple[str, float, float, float, Optional[int]]] = []

    # ---- type reserved FIRST so every arc knocks out around it -------------
    ty = y1 - 0.048 * H
    h1 = _fit(_spaced("RESONANCE"), 0.80 * W, 10.5)
    labels.append((_spaced("ORBITAL"), x0, ty, h1, TYPE))
    labels.append((_spaced("RESONANCE"), x0, ty - 1.52 * h1, h1, TYPE))
    sub_y = ty - 1.52 * h1 - 7.0
    for k, line in enumerate(
        (
            "A UNIFORM COMB OF %d ORBITS. %d JUPITER YEARS." % (n_orbits, int(jup_periods)),
            "SOLID HOLDS ITS LANE. DASHED LIBRATES. ABSENT IS SWEPT.",
            "BEYOND 3.1 AU NOTHING HOLDS ITS LANE. THAT IS THE 2:1.",
        )
    ):
        t = _spaced(line)
        labels.append((t, x0, sub_y - k * 4.3, _fit(t, 0.74 * W, 2.3), TYPE))
        if ":" in line:
            ratio_marks.append((t, x0, sub_y - k * 4.3, _fit(t, 0.74 * W, 2.3), TYPE))
    tcr = _spaced("CRIMSON. PREDICTED FROM THE INTEGERS ALONE.")
    labels.append((tcr, x0, sub_y - 3 * 4.3, _fit(tcr, 0.74 * W, 2.3), ARITH))
    kw = _spaced("KIRKWOOD 1866")
    hkw = _fit(kw, 0.30 * W, 2.3)
    labels.append((kw, x1 - _text_width(kw, hkw), ty + 0.55 * h1, hkw, TYPE))

    # gap labels: bare ratios, single line, staggered so they never stack and
    # small enough to sit INSIDE the void rather than punching a box in the belt
    for p, q in RESONANCES:
        txt = _spaced("%d:%d" % (p, q))
        tw = _text_width(txt, 3.2)
        pt = _arc_point(sun, res_radius(p, q) * S, x0 + tw / 2)
        if pt is None or not (y0 + 9 < pt[1] < y1 - 46):
            continue
        labels.append((txt, x0, pt[1] - 1.35, 3.2, TYPE))
        ratio_marks.append((txt, x0, pt[1] - 1.35, 3.2, TYPE))


    # radial scale: AU labels beside the ray (canon 5 requires the tick axis)
    ray = math.radians(28.0)
    ticks = (1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5)
    rnx, rny = math.cos(ray), -math.sin(ray)  # outward normal of the ray
    r_ray_hi = res_radius(2, 1) * S  # the scale ray terminates on the 2:1
    for au in (2.0, 2.5, 3.0, res_radius(2, 1)):
        r = au * S
        if r > r_ray_hi + 1e-6:
            continue
        px, py = sun[0] + r * math.sin(ray), sun[1] + r * math.cos(ray)
        t = _spaced("%.2f" % au)
        tw = _text_width(t, 2.1)
        lx, ly = px + 3.2 * rnx, py + 3.2 * rny - 1.0
        if lx + tw > x1 - 1.5:
            lx = px - 3.2 * rnx - tw
            ly = py - 3.2 * rny - 1.0
        if x0 < lx and lx + tw < x1 - 1 and y0 + 3 < ly < y1 - 34:
            labels.append((t, lx, ly, 2.1, TYPE))

    drawn = int((~closed & np.isfinite(amean)).sum())
    for k, line in enumerate(("CR3BP. MU 9.5388E-4. VERLET DT 0.02.",
                              "LIBRATION IS THE SPREAD OF MEAN A.")):
        t = _spaced(line)
        labels.append((t, x0, y0 + 6.0 - k * 3.6, _fit(t, 0.52 * W, 2.0), TYPE))
    for k, line in enumerate(("SUN AND JUPITER ONLY.",
                              "%d OF %d SURVIVE" % (drawn, n_orbits))):
        t = _spaced(line)
        ht = _fit(t, 0.34 * W, 2.0)
        labels.append((t, x1 - _text_width(t, ht), y0 + 6.0 - k * 3.6, ht, TYPE))
    # a label that cannot fit the drawable is dropped rather than clamped: the
    # piece must stay in bounds on any paper size, and the field is the subject.
    def _inside(lab) -> bool:
        txt, lx, ly, lh, _pen = lab
        return (
            lx >= x0 - 0.01
            and lx + _text_width(txt, lh) <= x1 + 0.01
            and ly >= y0
            and ly + 1.12 * lh <= y1
        )

    labels = [lab for lab in labels if _inside(lab)]
    ratio_marks = [lab for lab in ratio_marks if _inside(lab)]
    scene.halo_labels(labels, pad_x=1.5, pad_y=(0.5, 1.4))

    # ---- BLACK: the surviving orbits, one fine arc each ---------------------
    for j in range(n_orbits):
        if closed[j] or not math.isfinite(amean[j]):
            continue
        runs = _arc_runs(sun, amean[j] * S, box)
        if not runs:
            continue
        period = dash_on / max(1e-3, float(duty[j]))
        for seg in _dash(runs, dash_on, period, phase=float(phase[j])):
            scene.poly(seg, pen=BELT)

    # ---- CRIMSON: the arithmetic, dotted, laid over the dynamics ------------
    for p, q in RESONANCES:
        r = res_radius(p, q) * S
        for seg in _dash(_arc_runs(sun, r, box, step_mm=1.1), 1.4, 3.4):
            scene.poly(seg, pen=ARITH)

    # ---- the radial scale ray (dotted) + ticks, on the type layer -----------
    r_lo, r_hi = (a_bottom + 0.05) * S, res_radius(2, 1) * S
    ray_runs: List[List[Pt]] = []
    cur: List[Pt] = []
    rr = r_lo
    while rr <= r_hi:
        px, py = sun[0] + rr * math.sin(ray), sun[1] + rr * math.cos(ray)
        if box[0] <= px <= box[2] and box[1] <= py <= box[3]:
            cur.append((px, py))
        elif cur:
            ray_runs.append(cur)
            cur = []
        rr += 1.1
    if len(cur) >= 2:
        ray_runs.append(cur)
    for seg in _dash([r for r in ray_runs if len(r) >= 2], 1.0, 4.4):
        scene.poly(seg, pen=TYPE)
    for au in ticks:
        r = au * S
        if r > r_hi + 1e-6:
            continue
        px, py = sun[0] + r * math.sin(ray), sun[1] + r * math.cos(ray)
        if not (x0 + 1 < px < x1 - 1 and y0 + 1 < py < y1 - 1):
            continue
        tl = 3.2 if abs(au - round(au)) < 1e-9 or abs(au - 2.5) < 1e-9 else 1.7
        scene.poly([(px, py), (px + tl * rnx, py + tl * rny)], pen=TYPE)

    out = scene.render()
    for txt, lx, ly, lh, pen in ratio_marks:  # the missing ':' glyph, by hand
        out.extend(_colons(txt, lx, ly, lh, pen, feed))
    return out
