"""ORBITAL RESONANCE — THE CONSONANT PIPES ARE MISSING (studio candidate, r02).

CARRIER: an ORGAN RANK — a row of flue pipes standing in a rack board.

    A pipe's speaking length IS the asteroid's orbital period, and a pipe is
    missing exactly where its interval with Jupiter's pipe is a small whole
    number ratio.

That mapping is an identity, not a resemblance: an organ rank is built on
length ∝ 1/frequency ∝ period (it is why stops are named 8', 4', 2') and a
mean-motion resonance IS a small-integer frequency ratio — the same arithmetic
that makes an octave makes a Kirkwood gap. The consonances with Jupiter are the
2:1 octave, the 7:3, the 5:2 octave-and-major-third and the 3:1 twelfth, and at
those four lengths the rack board is drilled and empty.

The numbers are the same physics as r01 and are unchanged: 96 test particles on
a uniform comb in semimajor axis, velocity-Verlet in the planar circular
restricted three-body problem (Sun + Jupiter, mu = 9.5388e-4), 300 Jupiter
years; the boxcar-averaged osculating semimajor axis gives each orbit's
LIBRATION WIDTH, which decides whether its pipe stands and how far its speaking
length wanders. The four crimson ghost pipes are placed by arithmetic alone
(Kepler III, a = a_J (q/p)^(2/3)) and land in sockets the integration emptied.

Contract: resonance_rank(rng, bounds, colors=3) -> list[GCodeCommand].
Nothing under promptplot/ is modified.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.engine import Scene3D
from promptplot.generative.engine.kit import _poly, _spaced, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# --- physical constants -----------------------------------------------------
MU = 9.5388e-4  # m_J / (M_sun + m_J)
AJ_AU = 5.2028  # Jupiter semimajor axis, AU
TJ_YR = 11.862  # Jupiter's period, years
GM_S = 1.0 - MU

# interior mean-motion resonances = the consonances with Jupiter's pipe
RESONANCES: Tuple[Tuple[int, int], ...] = ((3, 1), (5, 2), (7, 3), (2, 1))
INTERVAL: Dict[Tuple[int, int], str] = {
    (2, 1): "OCTAVE",
    (7, 3): "SEPTIMAL TENTH",
    (5, 2): "MAJOR TENTH",
    (3, 1): "TWELFTH",
}


def res_axis(p: int, q: int) -> float:
    """Kepler III: n/n_J = p/q  =>  a = a_J (q/p)^(2/3).  Arithmetic only."""
    return AJ_AU * (q / p) ** (2.0 / 3.0)


def period_ratio(a_au: float) -> float:
    """T / T_J — and therefore, in a rank, pipe length / Jupiter's pipe."""
    return (a_au / AJ_AU) ** 1.5


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
def _dots(pts: Sequence[Pt], on: float = 0.9, period: float = 2.4) -> List[List[Pt]]:
    """Dotted rendering of a polyline: the piece's word for UNCERTAIN or ABSENT."""
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


def _split(seg: Tuple[Pt, Pt], spans: Sequence[Tuple[float, float]]) -> List[List[Pt]]:
    """Cut a horizontal segment where standing pipes occlude it (hidden line)."""
    (ax, ay), (bx, by) = seg
    lo, hi = min(ax, bx), max(ax, bx)
    cuts = sorted((max(lo, s), min(hi, e)) for s, e in spans if e > lo and s < hi)
    runs: List[List[Pt]] = []
    x = lo
    for s, e in cuts:
        if s > x:
            runs.append([(x, ay), (s, by)])
        x = max(x, e)
    if x < hi:
        runs.append([(x, ay), (hi, by)])
    return [r for r in runs if abs(r[1][0] - r[0][0]) > 0.35]


def _fit(text: str, max_w: float, h: float) -> float:
    w = _text_width(text, h)
    return h if w <= max_w else h * max_w / w


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
def resonance_rank(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_pipes: int = 96,
    a_lo: float = 2.26,
    a_hi: float = 3.34,
    ecc: float = 0.18,
    jup_periods: float = 300.0,
    dt: float = 0.02,
    sample_every: int = 10,
    wander_drop: float = 0.0197,
    excess_drop: float = 2.4,
    bg_window: float = 0.22,
    rim_gain: float = 6.0,
    shear: float = 0.30,
    rise: float = 0.50,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """ORBITAL RESONANCE as an ORGAN RANK — pipe length is orbital period, and
    the pipes at small whole-number intervals with Jupiter are missing from the
    rack. Black = the rank that stands, crimson = the four consonant pipes that
    do not, and the drilled empty sockets are the Kirkwood gaps."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    PIPE = 0
    GHOST = 1 % colors if colors > 1 else None
    TYPE = 2 % colors if colors > 1 else None

    # ---- integrate the comb (one particle per pipe socket) -----------------
    a_au = np.linspace(a_lo, a_hi, n_pipes)
    pom = rng.np.uniform(0.0, 2 * math.pi, n_pipes)
    m0 = rng.np.uniform(0.0, 2 * math.pi, n_pipes)
    dts, A = _integrate(
        a_au, ecc, pom, m0, t_end=jup_periods * 2 * math.pi, dt=dt, sample_every=sample_every
    )
    amean, width = _libration(a_au, dts, A)

    bg = np.array([np.nanmedian(width[np.abs(a_au - a_au[j]) < bg_window]) for j in range(n_pipes)])
    with np.errstate(invalid="ignore", divide="ignore"):
        excess = width / bg
        # absolute wander (AU of mean-motion excursion) OR resonance excess over
        # the local non-resonant background; either one and the pipe never stood
        w = np.fmax(width / wander_drop, (excess - 1.0) / (excess_drop - 1.0))
    drop = ~np.isfinite(w) | (w >= 1.0)
    for j in range(n_pipes):  # a socket enclosed by empties is inside the separatrix
        if not drop[j] and drop[max(0, j - 3) : j].any() and drop[j + 1 : j + 4].any():
            drop[j] = True

    # ---- ONE axonometric basis for the whole plate -------------------------
    # u along the rank, w up, v into depth. Nothing on this sheet is projected
    # any other way; a smaller element shrinks its world footprint, never shear.
    def P(u: float, wv: float, v: float) -> Pt:
        return (x0 + u + shear * v, y0 + wv + rise * v)

    V_CHEST = 0.110 * H
    V_RACK = 0.072 * H
    V_PIPE = 0.5 * V_CHEST
    # the boards are the widest thing on the sheet, so the rank's pitch is set
    # from what is left after the axonometric depth-shear, never the other way
    u_span = W - shear * V_CHEST - 1.0
    pitch = u_span / (n_pipes + 1.6)
    r_body = min(0.36 * pitch, 0.5 * (pitch - 0.85))  # keep >= 0.85 mm of paper
    w_chest = 0.055 * H
    w_mouth = w_chest + 0.090 * H  # every mouth on one line (organ practice)
    w_rack = w_mouth + 0.074 * H
    cut_up = 0.020 * H
    w_top_max = 0.725 * H

    def u_of(a: float) -> float:
        return 0.8 * pitch + (a - a_lo) / (a_hi - a_lo) * (n_pipes - 1) * pitch

    # speaking length IS the period: ONE length scale for the whole rank
    LKW = (w_top_max - w_mouth) / period_ratio(a_hi)

    def w_top(a: float) -> float:
        return w_mouth + LKW * period_ratio(a)

    scene = Scene3D(rng, bounds, feed=feed, fit="none")
    labels: List[Tuple[str, float, float, float, Optional[int]]] = []
    ratio_marks: List[Tuple[str, float, float, float, Optional[int]]] = []

    # ---- type first: every board line and pipe knocks out around it --------
    ty = y1 - 0.085 * H
    h1 = _fit(_spaced("RESONANCE"), 0.40 * W, 0.105 * H)
    labels.append((_spaced("ORBITAL"), x0, ty, h1, TYPE))
    labels.append((_spaced("RESONANCE"), x0, ty - 1.5 * h1, h1, TYPE))
    sub = ty - 1.5 * h1 - 0.042 * H
    for k, line in enumerate(
        (
            "A PIPE IS ITS ORBIT. LENGTH IS PERIOD.",
            "THE CONSONANCES WITH JUPITER ARE MISSING.",
        )
    ):
        t = _spaced(line)
        labels.append((t, x0, sub - k * 0.026 * H, _fit(t, 0.40 * W, 0.0165 * H), TYPE))

    for p, q in RESONANCES:  # each ratio rides its own ghost, following the rake
        ar = res_axis(p, q)
        if not (a_lo < ar < a_hi):
            continue
        gx = P(u_of(ar), 0.0, V_PIPE)[0]
        gtop = P(0.0, w_top(ar), V_PIPE)[1]
        txt = _spaced("%d:%d" % (p, q))
        lh = 0.019 * H
        lx = min(max(x0, gx - _text_width(txt, lh) / 2), x1 - _text_width(txt, lh))
        labels.append((txt, lx, gtop + 0.022 * H, lh, TYPE))
        ratio_marks.append((txt, lx, gtop + 0.022 * H, lh, TYPE))

    # the interval names read as one block, not four floating captions
    for k, pair in enumerate((((3, 1), (5, 2)), ((7, 3), (2, 1)))):
        line = "   ".join("%d:%d %s" % (p, q, INTERVAL[(p, q)]) for p, q in pair)
        t = _spaced(line)
        th = _fit(t, 0.40 * W, 0.0125 * H)
        labels.append((t, x0, sub - (2 + k) * 0.022 * H, th, GHOST))
        ratio_marks.append((t, x0, sub - (2 + k) * 0.022 * H, th, GHOST))

    kw = _spaced("KIRKWOOD 1866")
    hkw = _fit(kw, 0.22 * W, 0.0165 * H)
    labels.append((kw, x1 - _text_width(kw, hkw), y1 - 0.030 * H, hkw, TYPE))
    stop = _spaced("MAIN BELT  %d SOCKETS  %d SPEAKING" % (n_pipes, int((~drop).sum())))
    hst = _fit(stop, 0.34 * W, 0.0155 * H)
    labels.append((stop, x1 - _text_width(stop, hst), y1 - 0.052 * H, hst, TYPE))

    for k, line in enumerate(
        (
            "CIRCULAR RESTRICTED 3-BODY. MU 9.5388E-4. VERLET DT 0.02. 300 JUPITER YEARS.",
            "DOTTED COLLAR IS THE LIBRATION OF THE SPEAKING LENGTH, MAGNIFIED 6 TIMES.",
            "CRIMSON GHOSTS PLACED BY ARITHMETIC ALONE. SUN AND JUPITER ONLY.",
        )
    ):
        t = _spaced(line)
        labels.append((t, x0, y0 + 0.030 * H - k * 0.0155 * H, _fit(t, 0.62 * W, 0.0115 * H), TYPE))

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

    # ---- geometry helpers in the shared basis ------------------------------
    def ring(uc: float, wv: float, rr: float, n: int = 16, arc: str = "all") -> List[Pt]:
        pts: List[Pt] = []
        for k in range(n + 1):
            ang = math.pi + 2 * math.pi * k / n
            if arc == "back" and math.sin(ang) < -0.02:
                continue
            pts.append(P(uc + rr * math.cos(ang), wv, V_PIPE + rr * math.sin(ang)))
        return pts

    u_end = u_of(a_hi) + 0.8 * pitch
    spans = [
        (P(u_of(amean[j]), 0.0, V_PIPE)[0] - r_body, P(u_of(amean[j]), 0.0, V_PIPE)[0] + r_body)
        for j in range(n_pipes)
        if not drop[j] and math.isfinite(amean[j])
    ]

    def board(wv: float, depth: float, thick: float, pen):
        fl, fr = P(0, wv, 0.0), P(u_end, wv, 0.0)
        bl, br = P(0, wv, depth), P(u_end, wv, depth)
        scene.poly([(fl[0], fl[1] - thick), fl, fr, (fr[0], fr[1] - thick)], pen=pen)
        scene.poly([(fl[0], fl[1] - thick), (fr[0], fr[1] - thick)], pen=pen)
        for seg in _split((bl, br), spans):  # back edge: the rank stands in front
            scene.poly(seg, pen=pen)
        scene.poly([fl, bl], pen=pen)
        scene.poly([fr, br], pen=pen)

    board(w_chest, V_CHEST, 0.030 * H, PIPE)
    board(w_rack, V_RACK, 0.014 * H, PIPE)

    # every socket is drilled, whether or not a pipe was ever put in it
    for j in range(n_pipes):
        uc = u_of(a_au[j])
        standing = (not drop[j]) and math.isfinite(amean[j])
        scene.poly(ring(uc, w_rack, r_body * 1.10, arc="back" if standing else "all"), pen=PIPE)
        if not standing:  # the toe hole shows through the empty socket
            scene.poly(ring(uc, w_chest, r_body * 0.40, n=12), pen=PIPE)

    # ---- the rank: ONE outline stroke per pipe (foot, body, rim, body, foot)
    def draw_pipe(uc: float, wt: float, collar: float, pen, ghost: bool):
        outline = (
            [P(uc - 0.30 * r_body, w_chest, V_PIPE), P(uc - r_body, w_mouth, V_PIPE)]
            + ring(uc, wt, r_body)
            + [P(uc + r_body, w_mouth, V_PIPE), P(uc + 0.30 * r_body, w_chest, V_PIPE)]
        )
        # the left body line must climb to the rim's left lip, and the right one
        # descend from it: the ring already starts and ends at angle pi (left).
        outline = (
            outline[:2] + [P(uc - r_body, wt, V_PIPE)] + outline[2:-2] + [P(uc + r_body, wt, V_PIPE)] + outline[-2:]
        )
        mouth = [
            P(uc - 0.80 * r_body, w_mouth, V_PIPE),
            P(uc + 0.80 * r_body, w_mouth, V_PIPE),
            P(uc + 0.80 * r_body, w_mouth + cut_up, V_PIPE),
            P(uc + 0.38 * r_body, w_mouth + cut_up * 1.42, V_PIPE),
            P(uc - 0.38 * r_body, w_mouth + cut_up * 1.42, V_PIPE),
            P(uc - 0.80 * r_body, w_mouth + cut_up, V_PIPE),
            P(uc - 0.80 * r_body, w_mouth, V_PIPE),
        ]
        if ghost:
            for part in (outline, mouth):
                for seg in _dots(part, on=1.8, period=3.0):
                    scene.poly(seg, pen=pen)
                    scene.poly([(px + 0.16, py) for px, py in seg], pen=pen)  # 2nd pass
            return
        scene.poly(outline, pen=pen)
        scene.poly(mouth, pen=pen)
        cx = P(uc, 0.0, V_PIPE)[0]
        ytop, ymouth = P(0, wt, V_PIPE)[1], P(0, w_mouth, V_PIPE)[1]
        scene.poly(  # one shading line: a cylinder, not a slot
            [(cx + 0.50 * r_body, ymouth + cut_up * 1.8), (cx + 0.50 * r_body, ytop - 1.2)], pen=pen
        )
        if collar > 1.2:  # the speaking length does not hold still
            for sx in (cx - r_body, cx + r_body):
                for seg in _dots(
                    [(sx, ytop - collar / 2), (sx, ytop + collar / 2)], on=0.6, period=1.7
                ):
                    scene.poly(seg, pen=pen)

    for j in range(n_pipes):
        if drop[j] or not math.isfinite(amean[j]):
            continue
        a_j = float(amean[j])
        wt = w_top(a_j)
        collar = min(0.12 * H, rim_gain * 1.5 * (wt - w_mouth) * float(width[j]) / a_j)
        draw_pipe(u_of(a_j), wt, collar, PIPE, ghost=False)

    # ---- CRIMSON: the four pipes the integers say should stand here --------
    for p, q in RESONANCES:
        ar = res_axis(p, q)
        if a_lo < ar < a_hi:
            draw_pipe(u_of(ar), w_top(ar), 0.0, GHOST, ghost=True)

    out = scene.render()
    for txt, lx, ly, lh, pen in ratio_marks:
        out.extend(_colons(txt, lx, ly, lh, pen, feed))
    return out
