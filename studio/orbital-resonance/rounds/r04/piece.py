"""COMPOSITION WITH RED YELLOW BLUE AND NOTHING (studio candidate, r04).

ORDER: ORTHOGONAL SUBDIVISION.  CANON: DE STIJL.

    The sheet is period-space. Vertical rules cut it at the measured edges of
    the forbidden bands; horizontal rules stack those bands by the ORDER of the
    resonance; and the colour is painted on the emptiness.

Nothing is depicted and nothing is plotted. The subdivision IS the data:

  * x  — semimajor axis, 2.26 to 3.34 AU, one linear scale across the sheet.
  * a vertical rule stands at every measured boundary of a forbidden band, and
    its WEIGHT is that band's libration width: the 2:1 is a bar, the 7:3 a hair.
  * horizontal rules stratify the sheet by resonance ORDER |p-q| — first order
    at the foot, fourth at the top — and a stratum's HEIGHT is that order's
    measured strength. Block area is therefore width x strength: the phase
    space the resonance takes out of the belt.
  * RED is first order (2:1), BLUE second (3:1), YELLOW third (5:2). The 7:3 is
    fourth order and too weak to paint: it gets rules and no colour, which is
    the measurement, not a design choice.

The joke is the title, and the punchline is the physics: in this composition
the coloured blocks are the NOTHING. Every white rectangle is full of
asteroids; every painted one is swept. Kepler's integers carve holes in a belt
they never touch, and the emptiness is the evidence.

The physics is r01's, unchanged: 96 test particles on a uniform comb in
semimajor axis, velocity-Verlet in the planar circular restricted three-body
problem (Sun + Jupiter, mu = 9.5388e-4), 300 Jupiter years, the boxcar-averaged
osculating semimajor axis giving each orbit's libration width. Band edges come
from that integration; the ratios and their order come from arithmetic alone.

Contract: composition_with_nothing(rng, bounds, colors=4) -> list[GCodeCommand].
Nothing under promptplot/ is modified.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from promptplot.generative.engine.kit import (
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    fill_rect,
    giant_type,
    giant_type_width,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

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


def _libration(a_au, dts: float, A):
    """Boxcar the osculating a over one orbital period -> libration width (AU)."""
    import numpy as np

    n = len(a_au)
    per = 2.0 * math.pi * (a_au / AJ_AU) ** 1.5
    width = np.full(n, np.nan)
    for j in range(n):
        col = A[:, j]
        if not np.all(np.isfinite(col)):
            continue
        w = max(3, int(round(per[j] / dts)))
        sm = np.convolve(col, np.ones(w) / w, mode="valid") * AJ_AU
        width[j] = float(sm.max() - sm.min())
    return width


def _fit(text: str, max_w: float, h: float, spaced: bool = False) -> float:
    w = giant_type_width(text, h, spaced)
    return h if w <= max_w else h * max_w / w


def _colons(text: str, x: float, y: float, h: float, pen, f: int) -> List[GCodeCommand]:
    """The stroke font has no ':' glyph — it advances but draws nothing."""
    sc, adv = h / 6.0, 5.6 * h / 6.0
    out: List[GCodeCommand] = []
    for i, ch in enumerate(text):
        if ch != ":":
            continue
        gx = x + i * adv + 1.9 * sc
        for gy in (1.4 * sc, 4.2 * sc):
            out += _poly(
                [(gx, y + gy), (gx + 0.8 * sc, y + gy)], color=pen, f=f
            )
            out += _poly(
                [(gx, y + gy + 0.35 * sc), (gx + 0.8 * sc, y + gy + 0.35 * sc)], color=pen, f=f
            )
    return out


def _rule_v(x: float, ya: float, yb: float, w: float, pen, f: int) -> List[GCodeCommand]:
    """A vertical black rule of real WEIGHT — a serpentine band, not a hairline."""
    return fill_rect(x - w / 2, ya, x + w / 2, yb, spacing=0.42, pen=pen, f=f)


def _rule_h(y: float, xa: float, xb: float, w: float, pen, f: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    k = max(2, int(round(w / 0.42)) + 1)
    for i in range(k):
        yy = y - w / 2 + w * i / (k - 1)
        out += _poly([(xa, yy), (xb, yy)], color=pen, f=f)
    return out


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def composition_with_nothing(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
    n_cols: int = 240,
    a_lo: float = 2.26,
    a_hi: float = 3.34,
    ecc: float = 0.18,
    jup_periods: float = 300.0,
    dt: float = 0.02,
    sample_every: int = 10,
    wander_drop: float = 0.0197,
    excess_drop: float = 2.4,
    bg_window: float = 0.22,
    field_frac: float = 0.635,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """COMPOSITION WITH RED YELLOW BLUE AND NOTHING — De Stijl orthogonal
    subdivision of period-space, where the painted blocks are the swept bands
    and every white rectangle is full of asteroids."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BLACK = 0
    RED = 1 % colors
    YELLOW = 2 % colors
    BLUE = 3 % colors
    ORDER_PEN: Dict[int, Optional[int]] = {1: RED, 2: BLUE, 3: YELLOW, 4: None}

    # ---- the comb, integrated ---------------------------------------------
    a_au = np.linspace(a_lo, a_hi, n_cols)
    pom = rng.np.uniform(0.0, 2 * math.pi, n_cols)
    m0 = rng.np.uniform(0.0, 2 * math.pi, n_cols)
    dts, A = _integrate(
        a_au, ecc, pom, m0, t_end=jup_periods * 2 * math.pi, dt=dt, sample_every=sample_every
    )
    width = _libration(a_au, dts, A)
    bg = np.array([np.nanmedian(width[np.abs(a_au - a_au[j]) < bg_window]) for j in range(n_cols)])
    with np.errstate(invalid="ignore", divide="ignore"):
        excess = width / bg
        w = np.fmax(width / wander_drop, (excess - 1.0) / (excess_drop - 1.0))
    vacant = ~np.isfinite(w) | (w >= 1.0)
    close = max(1, int(round(0.014 / ((a_hi - a_lo) / (n_cols - 1)))))  # 0.014 AU
    for j in range(n_cols):  # a lane enclosed by vacancies is inside the separatrix
        if (
            not vacant[j]
            and vacant[max(0, j - close) : j].any()
            and vacant[j + 1 : j + 1 + close].any()
        ):
            vacant[j] = True

    # ---- contiguous forbidden bands, named by the integers that make them ---
    pitch = (a_hi - a_lo) / (n_cols - 1)
    bands: List[dict] = []
    j = 0
    while j < n_cols:
        if not vacant[j]:
            j += 1
            continue
        k = j
        while k + 1 < n_cols and vacant[k + 1]:
            k += 1
        lo = max(a_lo, a_au[j] - pitch / 2)
        hi = min(a_hi, a_au[k] + pitch / 2)
        strength = float(np.nanmax(width[j : k + 1]))
        named = None
        for p, q in RESONANCES:
            if lo - 1.5 * pitch <= res_axis(p, q) <= hi + 1.5 * pitch:
                named = (p, q)
                break
        bands.append({"lo": lo, "hi": hi, "s": strength, "pq": named})
        j = k + 1
    smax = max(b["s"] for b in bands) if bands else 1.0

    def X(a: float) -> float:
        return x0 + (a - a_lo) / (a_hi - a_lo) * W

    # ---- strata: one per resonance order, height = that order's strength ---
    named = [b for b in bands if b["pq"] is not None]
    named.sort(key=lambda b: b["pq"][0] - b["pq"][1])  # first order at the foot
    tot = sum(b["s"] for b in named) or 1.0
    y_field = y0 + field_frac * H
    cuts = [y0]
    for b in named:
        cuts.append(cuts[-1] + (y_field - y0) * b["s"] / tot)
    for i, b in enumerate(named):
        b["ya"], b["yb"] = cuts[i], cuts[i + 1]

    out: List[GCodeCommand] = []

    # ---- the paint: colour goes on the emptiness ---------------------------
    for b in named:
        pen = ORDER_PEN.get(b["pq"][0] - b["pq"][1])
        if pen is None:
            continue
        out += fill_rect(X(b["lo"]), b["ya"], X(b["hi"]), b["yb"], spacing=0.62, pen=pen, f=feed)

    # ---- the armature: only horizontal and vertical black rules ------------
    # vertical rules stop at the field line; ONE runs the full height — the
    # strongest band's inner edge, which is where the belt itself stops
    full = max(named, key=lambda b: b["s"])["lo"] if named else None
    for b in bands:
        rw = 0.85 + 3.0 * (b["s"] / smax)
        for a in (b["lo"], b["hi"]):
            top = y1 if (full is not None and abs(a - full) < 1e-9) else y_field
            out += _rule_v(min(max(X(a), x0 + rw / 2), x1 - rw / 2), y0, top, rw, BLACK, feed)
    for i, b in enumerate(named):  # horizontal rules at the stratum boundaries
        if i == 0:
            continue
        out += _rule_h(b["ya"], x0, x1, 0.85 + 2.0 * (b["s"] / smax), BLACK, feed)
    out += _rule_h(y_field, x0, x1, 2.6, BLACK, feed)  # field / title division

    # ---- type as MASS, flush into the top band ----------------------------
    title = ("COMPOSITION WITH RED", "YELLOW BLUE AND NOTHING")
    th = min(
        _fit(title[0], 0.94 * W, 0.115 * H),
        _fit(title[1], 0.94 * W, 0.115 * H),
    )
    ty = y1 - 0.055 * H - th
    pad = 0.018 * W
    for i, line in enumerate(title):
        out += giant_type(
            line, x0 + pad, ty - i * 1.42 * th, th, pen=BLACK, weight=0.085 * th, f=feed
        )
    sub = _spaced("KIRKWOOD 1866.  MU 9.5388E-4.  VERLET.  300 JUPITER YEARS.")
    sh = min(0.0165 * H, 0.42 * W / max(1e-6, _text_width(sub, 1.0)))
    out += _stroke_text(sub, x0 + pad, y_field + 0.030 * H, sh, color=BLACK, f=feed)

    # ---- each block says which integers took it ---------------------------
    for b in named:
        p, q = b["pq"]
        txt = "%d:%d" % (p, q)
        lh = 0.040 * H
        bw = X(b["hi"]) - X(b["lo"])
        lx = X(b["hi"]) + 0.012 * W
        ly = b["ya"] + (b["yb"] - b["ya"]) / 2 - lh / 2
        if lx + giant_type_width(txt, lh) > x1 - 0.01 * W:
            lx = X(b["lo"]) - 0.012 * W - giant_type_width(txt, lh)
        if bw > giant_type_width(txt, lh) * 1.25 and b["yb"] - b["ya"] > lh * 2.2:
            lx = X(b["lo"]) + (bw - giant_type_width(txt, lh)) / 2
            ly = b["yb"] + 0.012 * H
        out += giant_type(txt, lx, ly, lh, pen=BLACK, weight=0.07 * lh, f=feed)
        out += _colons(txt, lx, ly, lh, BLACK, feed)

    swept = int(vacant.sum())
    tail = _spaced("%.1f PERCENT OF THE BELT SWEPT.  THE WHITE IS WHAT IS LEFT." % (100.0 * swept / n_cols,))
    tw = min(0.0155 * H, 0.46 * W / max(1e-6, _text_width(tail, 1.0)))
    out += _stroke_text(
        tail, x1 - pad - _text_width(tail, tw), y_field + 0.030 * H, tw, color=BLACK, f=feed
    )
    return out
