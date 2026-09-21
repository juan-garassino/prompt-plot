"""THE LONG WAY BACK — diffusion as a ring of time that fails to close.

ABSTRACT ORDER (one line): *an annular crystal whose arc coordinate IS diffusion
time — it melts to an isotropic fog at the antipode and recrystallises back to
the seam, where it cannot meet itself because the grain came back at a different
angle.*  One straight chord crosses the void from seam to melt: the closed-form
forward jump, the only shortcut on the sheet, and it goes one way only.

No registers, no plot, no bowtie, no picture of a thing.  The mechanism supplies
every number; the order supplies the form:

    angle          = t          (arc-offset from the seam, both ways, so the
                                 two arcs are MIRRORS about the chord and the
                                 reversibility is the plate's own symmetry)
    radial offset  = the one data coordinate, transported by
                     x_t = sqrt(abar_t) * x_0 + sqrt(1 - abar_t) * sigma * eps
    pen            = t, switching EXACTLY where a structural scale stops being
                     resolved (four scales a/3, a, 2a, 3a -> four boundaries)
    chord          = q(x_t | x_0): one evaluation.  Three lines collapsing to
                     one as they cross the void: information going away.
    bullseye       = the prior's level sets.  Perfect circles because N(0, I)
                     is isotropic; the only true circle on the sheet.
    seam mismatch  = the reverse trajectory is a DIFFERENT SAMPLE.

Style canon: RUSSIAN CONSTRUCTIVISM (STYLES.md §8) — one aggressive diagonal
(the chord, which is also the time-mirror axis), display type as mass on a
single flush-left column plus one line set along the diagonal, a heavy black
keyline at the defect, one scarce loud accent (crimson, spent only on the melt).

Contract: diffusion_passes(rng, bounds, colors=3) -> list[GCodeCommand]
"""

from __future__ import annotations

import logging
import math
from typing import Dict, List, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.engine import kit
from promptplot.generative.engine.kit import _dot, _poly, _stroke_text, _text_width

logger = logging.getLogger(__name__)

Pt = Tuple[float, float]

# --------------------------------------------------------------------------
# the schedule — cosine (Nichol & Dhariwal), used exactly, nothing eyeballed
# --------------------------------------------------------------------------

_S = 0.008


def _abar(u: float) -> float:
    """abar_t for normalised time u = t/T."""
    u = 0.0 if u < 0.0 else (1.0 if u > 1.0 else u)
    return math.cos(0.5 * math.pi * (u + _S) / (1.0 + _S)) ** 2


def _u_at(ab: float) -> float:
    """Inverse of _abar."""
    ab = 0.0 if ab < 0.0 else (1.0 if ab > 1.0 else ab)
    return (1.0 + _S) * (2.0 / math.pi) * math.acos(math.sqrt(ab)) - _S


def _u_of_scale(ell: float, sigma: float) -> float:
    """The u at which structure of size ``ell`` stops being resolved.

    One criterion, applied everywhere: a feature of size ell survives while the
    surviving signal exceeds two standard deviations of the injected noise,
    sqrt(abar)*ell > 2*sqrt(1-abar)*sigma, i.e. while SNR = abar/(1-abar) is
    above (2*sigma/ell)^2.  Every pen boundary and every structural death on
    this plate is one crossing of that inequality — which is why the decay is
    late and fast at each scale instead of linear by eye.
    """
    snr = (2.0 * sigma / ell) ** 2
    return _u_at(snr / (1.0 + snr))


PSI_DEG = 37.4          # grain tilt of the recrystallised half. The whole
                        # "not a rewind" argument is this one angle.
PHI_SEAM_DEG = 143.0    # seam upper-left; the melt is diametrically opposite
N_STEPS = 512           # denoising steps the reverse arc stands for


def _pen_ramp(colors: int) -> List[int]:
    return [i % max(1, colors) for i in range(5)]


def diffusion_passes(rng, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    SC = min((x1 - x0) / 400.0, (y1 - y0) / 277.0)

    A = 9.0 * SC                     # lattice constant
    H = 3.0 * A                      # band half-width (= 3a, the coarse scale)
    SIGMA = A / 2.522                # noise scale; sets the whole ladder
    R = 100.0 * SC                   # centreline radius
    CX = x0 + 0.630 * (x1 - x0)
    CY = y0 + 0.490 * (y1 - y0)
    L = math.pi * R                  # arc length of one half-ring
    PHI = math.radians(PHI_SEAM_DEG)
    PSI = math.radians(PSI_DEG)

    ramp = _pen_ramp(colors)
    K = ramp[0]
    ACCENT = ramp[4]

    u_edges = [
        _u_of_scale(A / 3.0, SIGMA),   # the fine hatch inside a cell
        _u_of_scale(A, SIGMA),         # the cell itself / the bonds
        _u_of_scale(2.0 * A, SIGMA),   # the row pair
        _u_of_scale(3.0 * A, SIGMA),   # the band — confinement itself
    ]

    def pen_of(u: float) -> int:
        k = 0
        for i, e in enumerate(u_edges):
            if u >= e:
                k = i + 1
        return ramp[k]

    out: List[GCodeCommand] = []

    # ------------------------------------------------------------------
    # the ring
    # ------------------------------------------------------------------

    def place(tt: float, rr: float, side: int) -> Pt:
        phi = PHI + side * (tt / R)
        rad = R + rr
        return (CX + rad * math.cos(phi), CY + rad * math.sin(phi))

    def transport(tl: float, rl: float, side: int) -> Pt:
        """DDPM transport of one nominal lattice coordinate.

        The arc coordinate IS time, so the map contracts + noises the radial
        coordinate and adds the SAME isotropic noise to the in-cell tangential
        deviation (which is zero at t=0).  Both axes therefore receive noise of
        equal scale, which is what makes the end state isotropic; and the rows
        collapse onto the centreline as sqrt(abar), which is what pinches the
        band into a filament at the bottleneck.
        """
        u = tl / L
        ab = _abar(u)
        sa, na = math.sqrt(ab), math.sqrt(1.0 - ab)
        rr = sa * rl + na * SIGMA * rng.gauss(0.0, 1.0)
        tt = tl + na * SIGMA * rng.gauss(0.0, 1.0)
        return place(tt, rr, side)

    def build(side: int, psi: float):
        cp, sp = math.cos(psi), math.sin(psi)
        span = int(L / A) + 16
        sites: Dict[Tuple[int, int], dict] = {}
        for m in range(-span, span + 1):
            for n in range(-span, span + 1):
                tl = A * (m * cp + n * sp)
                rl = A * (-m * sp + n * cp)
                if tl < -1e-9 or tl > L or abs(rl) > H + 1e-9:
                    continue
                u = tl / L
                sites[(m, n)] = {"u": u, "ab": _abar(u),
                                 "p": transport(tl, rl, side)}
        cells = [(m, n) for (m, n) in sites
                 if all((m + dm, n + dn) in sites
                        for dm, dn in ((1, 0), (0, 1), (1, 1)))]
        return sites, cells

    def bond_alive(a: dict, b: dict) -> bool:
        """Survives while the two atoms stay within 1.45x the CURRENT lattice
        constant sqrt(abar_t)*a.  That threshold goes to zero, so no bond can
        survive t=T, and the breaking is granular — one bond at a time, which
        is what melting looks like."""
        ab = 0.5 * (a["ab"] + b["ab"])
        tau = 1.45 * math.sqrt(ab) * A
        dx = a["p"][0] - b["p"][0]
        dy = a["p"][1] - b["p"][1]
        return dx * dx + dy * dy < tau * tau

    def lerp(p: Pt, q: Pt, f: float) -> Pt:
        return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)

    def dash(p: Pt, q: Pt, frac: float, pen: int) -> List[GCodeCommand]:
        a = 0.5 - frac / 2.0
        return _poly([lerp(p, q, a), lerp(p, q, 1.0 - a)], color=pen, f=2200)

    stats = {}

    def emit_side(side: int, psi: float, stitched: bool, tag: str):
        sites, cells = build(side, psi)
        o: List[GCodeCommand] = []
        alive: Dict[Tuple[Tuple[int, int], int], bool] = {}
        for key, s in sites.items():
            m, n = key
            for d, (dm, dn) in enumerate(((1, 0), (0, 1))):
                t = sites.get((m + dm, n + dn))
                alive[(key, d)] = bool(t) and bond_alive(s, t)

        # rows — continuous on the forward side, stitched on the reverse
        for key in sites:
            m, n = key
            if (m - 1, n) in sites and alive.get(((m - 1, n), 0)):
                continue
            run, k = [key], key
            while alive.get((k, 0)):
                k = (k[0] + 1, k[1])
                run.append(k)
            if len(run) < 2:
                continue
            if stitched:
                for i in range(len(run) - 1):
                    a, b = sites[run[i]], sites[run[i + 1]]
                    o += dash(a["p"], b["p"], 0.56,
                              pen_of(0.5 * (a["u"] + b["u"])))
            else:
                cur = [sites[run[0]]["p"]]
                cur_pen = pen_of(sites[run[0]]["u"])
                for i in range(1, len(run)):
                    s = sites[run[i]]
                    p = pen_of(s["u"])
                    cur.append(s["p"])
                    if p != cur_pen:
                        o += _poly(cur, color=cur_pen, f=2200)
                        cur, cur_pen = [s["p"]], p
                if len(cur) >= 2:
                    o += _poly(cur, color=cur_pen, f=2200)

        # radial bonds
        for key, s in sites.items():
            if not alive.get((key, 1)):
                continue
            t = sites[(key[0], key[1] + 1)]
            pen = pen_of(0.5 * (s["u"] + t["u"]))
            o += (dash(s["p"], t["p"], 0.56, pen) if stitched
                  else _poly([s["p"], t["p"]], color=pen, f=2200))

        # the fine hatch, while the a/3 scale is still resolved
        n_hatch = 0
        for (m, n) in cells:
            c00, c10 = sites[(m, n)], sites[(m + 1, n)]
            c01, c11 = sites[(m, n + 1)], sites[(m + 1, n + 1)]
            u = 0.25 * (c00["u"] + c10["u"] + c01["u"] + c11["u"])
            if u >= u_edges[0]:
                continue
            if not (alive.get(((m, n), 0)) and alive.get(((m, n), 1))):
                continue
            pen = pen_of(u)
            n_hatch += 1
            for fr in (1.0 / 3.0, 2.0 / 3.0):
                a = lerp(c00["p"], c01["p"], fr)
                b = lerp(c10["p"], c11["p"], fr)
                o += (dash(a, b, 0.60, pen) if stitched
                      else _poly([a, b], color=pen, f=2200))

        # atoms — the hatch's material, freed when the a/3 scale dies.
        # Particle number is conserved; only the order is lost.
        cp, sp = math.cos(psi), math.sin(psi)
        n_atom = 0
        for (m, n) in cells:
            u_c = 0.25 * (sites[(m, n)]["u"] + sites[(m + 1, n)]["u"]
                          + sites[(m, n + 1)]["u"] + sites[(m + 1, n + 1)]["u"])
            if u_c < u_edges[0]:
                continue
            pen = pen_of(u_c)
            for fm, fn in ((0.27, 0.44), (0.56, 0.21), (0.73, 0.71)):
                tl = A * ((m + fm) * cp + (n + fn) * sp)
                rl = A * (-(m + fm) * sp + (n + fn) * cp)
                if tl < 0.0 or tl > L:
                    continue
                px, py = transport(tl, rl, side)
                n_atom += 1
                if stitched:
                    # one drawn step's displacement: the reverse fog is made of
                    # tiny oriented steps, the forward fog of free points
                    th = rng.uniform(0.0, 2.0 * math.pi)
                    ln = 0.66 * SC
                    o += _poly([(px - ln * math.cos(th), py - ln * math.sin(th)),
                                (px + ln * math.cos(th), py + ln * math.sin(th))],
                               color=pen, f=2200)
                else:
                    o += _dot(px, py, r=0.55 * SC, color=pen, f=1800)

        # unbound sites become free points
        n_free = 0
        for key, s in sites.items():
            m, n = key
            if (alive.get((key, 0)) or alive.get((key, 1))
                    or alive.get(((m - 1, n), 0)) or alive.get(((m, n - 1), 1))):
                continue
            n_free += 1
            o += _dot(s["p"][0], s["p"][1], r=0.55 * SC,
                      color=pen_of(s["u"]), f=1800)

        n_bond = sum(1 for v in alive.values() if v)
        stats[tag] = dict(sites=len(sites), cells=len(cells), bonds=n_bond,
                          hatch=n_hatch, atoms=n_atom, free=n_free)
        return o

    out += emit_side(-1, 0.0, False, "forward")   # ruled, ring-aligned grain
    out += emit_side(+1, PSI, True, "reverse")    # stitched, tilted grain

    # ------------------------------------------------------------------
    # the chord — q(x_t | x_0).  Three lines collapsing to one.
    # ------------------------------------------------------------------
    er = (math.cos(PHI), math.sin(PHI))
    perp = (-er[1], er[0])
    p_seam = (CX + (R + H) * er[0], CY + (R + H) * er[1])
    p_melt = (CX - R * er[0], CY - R * er[1])
    spread = 2.8 * SC
    for k in (-1, 0, 1):
        a = (p_seam[0] + k * spread * perp[0], p_seam[1] + k * spread * perp[1])
        out += _poly([a, p_melt], color=K, f=2200)
    # the last 26 mm arrives as mass: the jump landing in the prior
    hl = 26.0 * SC
    hv = (p_melt[0] - p_seam[0], p_melt[1] - p_seam[1])
    hn = math.hypot(*hv)
    hd = (hv[0] / hn, hv[1] / hn)
    out += kit.fat_outline([(p_melt[0] - hd[0] * hl, p_melt[1] - hd[1] * hl),
                            p_melt], width=1.7 * SC, pen=K, tip=0.5)

    # the mirror axis, continued to the sheet edge as a fine dashed rule
    def axis_run(p: Pt, d: Pt, length: float, pen: int, on=2.8, off=2.8):
        s, o2 = 0.0, []
        on, off = on * SC, off * SC
        while s < length:
            e = min(length, s + on)
            o2 += _poly([(p[0] + d[0] * s, p[1] + d[1] * s),
                         (p[0] + d[0] * e, p[1] + d[1] * e)], color=pen, f=2200)
            s = e + off
        return o2

    def to_edge(p: Pt, d: Pt) -> float:
        best = 1e9
        for lim, c in ((x0 + 3, 0), (x1 - 3, 0), (y0 + 3, 1), (y1 - 3, 1)):
            if abs(d[c]) < 1e-9:
                continue
            s = (lim - p[c]) / d[c]
            if 0.0 < s < best:
                best = s
        return 0.0 if best > 1e8 else best

    out += axis_run(p_seam, er, to_edge(p_seam, er), K)
    d2 = (-er[0], -er[1])
    far = (p_melt[0] + d2[0] * 14.0 * SC, p_melt[1] + d2[1] * 14.0 * SC)
    out += axis_run(far, d2, to_edge(far, d2), K)

    # ------------------------------------------------------------------
    # the defect: where the two crystals meet and do not fit
    # ------------------------------------------------------------------
    out += kit.fat_outline([(CX + (R - H) * er[0], CY + (R - H) * er[1]),
                            (CX + (R + H) * er[0], CY + (R + H) * er[1])],
                           width=2.4 * SC, pen=K, tip=0.5)

    # ------------------------------------------------------------------
    # the bottleneck.  N(0, I) drawn as its own level sets: perfect circles,
    # because isotropic, at 0.5 sigma pitch out to 2.5 sigma.  The smallest
    # object on the sheet and the only true circle on it.
    # ------------------------------------------------------------------
    r_prior = 2.5 * SIGMA
    out += kit.concentric_disc(p_melt[0], p_melt[1], r_prior, rings=9,
                               pen=ACCENT, seg=64)
    out += kit.dotted_circle(p_melt[0], p_melt[1], 3.4 * SIGMA, pen=ACCENT,
                             bounds=bounds)

    # ------------------------------------------------------------------
    # type — Constructivism: one flush-left column + one line on the diagonal
    # ------------------------------------------------------------------
    TX = x0 + 6.0 * SC
    COLW = 112.0 * SC                       # hard width budget for the column

    def col(lines: Sequence[str], ty: float, hh: float, lead: float,
            pen: int, spaced: bool = False) -> List[GCodeCommand]:
        o2, yy = [], ty
        for ln in lines:
            if ln:
                t = " ".join(ln) if spaced else ln
                w = _text_width(t, hh)
                if w > COLW + 0.5:
                    logger.warning("column overflow %.1f mm: %r", w, ln)
                o2 += _stroke_text(t, TX, yy, hh, color=pen, f=2200)
            yy -= lead
        return o2

    out += col(["DIFFUSION"], y1 - 11.0 * SC, 3.0 * SC, 0.0, K, spaced=True)
    for i, word in enumerate(("THE", "LONG", "WAY", "BACK")):
        out += kit.giant_type(word, TX, y1 - (43.0 + 32.0 * i) * SC, 24.0 * SC,
                              pen=K, weight=1.1 * SC, tip=0.5)

    out += col(["A RING OF TIME THAT DOES NOT CLOSE",
                "",
                "DOWN THE CHORD IN ONE EVALUATION.",
                "BACK ROUND THE ARC IN 512 STEPS.",
                "THE SCHEDULE IS SYMMETRIC ABOUT THE",
                "AXIS. THE SAMPLE IS NOT."],
               y1 - 152.0 * SC, 3.1 * SC, 5.6 * SC, K)

    ab_e = [_abar(u) for u in u_edges]
    out += col(["COSINE SCHEDULE  s 0.008   T 512",
                "LATTICE a %.1f MM    SIGMA %.2f MM" % (A / SC, SIGMA / SC),
                "RESOLVED WHILE SNR ABOVE (2 SIGMA / L)^2",
                "SNR = ABAR / (1 - ABAR)",
                "",
                "L = a/3    DIES u %.3f    ABAR %.3f" % (u_edges[0], ab_e[0]),
                "L = a      DIES u %.3f    ABAR %.3f" % (u_edges[1], ab_e[1]),
                "L = 2a     DIES u %.3f    ABAR %.3f" % (u_edges[2], ab_e[2]),
                "L = 3a     DIES u %.3f    ABAR %.3f" % (u_edges[3], ab_e[3]),
                "",
                "GRAIN TILT  θ %.1f DEG" % PSI_DEG,
                "ONE STEP MOVES AN ATOM 0.22 MM",
                "THE CRYSTAL IS %.0f MM ACROSS" % (2.0 * (R + H) / SC),
                "THE PRIOR IS %.1f MM ACROSS" % (2.0 * r_prior / SC)],
               y0 + 86.0 * SC, 2.4 * SC, 4.1 * SC, K)

    # pen ramp legend — the ramp is a VARIABLE here, so it needs a scale
    ly = y0 + 22.0 * SC
    for i, p in enumerate(ramp):
        out += kit.fill_rect(TX + i * 7.4 * SC, ly, TX + i * 7.4 * SC + 5.4 * SC,
                             ly + 3.2 * SC, spacing=0.55, pen=p, f=2200)
    out += _stroke_text("t 0", TX, ly - 4.4 * SC, 2.4 * SC, color=K, f=2200)
    out += _stroke_text("t T", TX + 4 * 7.4 * SC, ly - 4.4 * SC, 2.4 * SC,
                        color=K, f=2200)

    out += _stroke_text(" ".join("PEN PLOTTER"), TX, y0 + 8.0 * SC, 3.2 * SC,
                        color=K, f=2200)
    out += _poly([(TX + 62.0 * SC, y0 + 9.6 * SC),
                  (TX + 86.0 * SC, y0 + 9.6 * SC)], color=K, f=2200)

    # ------------------------------------------------------------------
    # tags inside the void — the chord divides it, so each half is labelled
    # ------------------------------------------------------------------
    def tag(lines: Sequence[str], tx: float, ty: float, pen: int,
            hh: float = 2.6, lead: float = 4.3) -> List[GCodeCommand]:
        o2, yy = [], ty
        for ln in lines:
            o2 += _stroke_text(ln, tx, yy, hh * SC, color=pen, f=2200)
            yy -= lead * SC
        return o2

    def vp(dx: float, dy: float) -> Pt:
        return (CX + dx * SC, CY + dy * SC)

    p = vp(-14.0, 56.0)
    out += tag(["FORWARD   q ( x t | x 0 )", "RULED. ONE EVALUATION."],
               p[0], p[1], K)
    p = vp(-62.0, -36.0)
    out += tag(["REVERSE   p θ ( x t-1 | x t )", "STITCHED. 512 EVALUATIONS."],
               p[0], p[1], K)
    p = vp(-66.0, 30.0)
    out += tag(["t 0.  DATA.", "GRAIN BOUNDARY  θ 37.4 DEG"], p[0], p[1], K)
    p = vp(26.0, -70.0)
    out += tag(["t T.  N ( 0 , I )", "ISOTROPIC. THE ONLY", "TRUE CIRCLE HERE."],
               p[0], p[1], ACCENT)

    # the one line of display type on the diagonal — Constructivism's axis
    ang = math.degrees(math.atan2(hd[1], hd[0]))
    anc = (p_seam[0] + hd[0] * 30.0 * SC + perp[0] * 7.0 * SC,
           p_seam[1] + hd[1] * 30.0 * SC + perp[1] * 7.0 * SC)
    out += kit.giant_type("ONE EVALUATION", anc[0], anc[1], 6.6 * SC,
                          pen=K, angle=ang, spaced=True)

    # registration marks on the column's grid line
    for yy in (y1 - 4.0 * SC, y0 + 4.0 * SC):
        out += kit.plus_mark(TX, yy, 2.2 * SC, pen=K)

    # ------------------------------------------------------------------
    # report
    # ------------------------------------------------------------------
    xs = [c.x for c in out if c.x is not None]
    ys = [c.y for c in out if c.y is not None]
    draw = 0.0
    px = py = None
    for c in out:
        if c.x is None or c.y is None:
            continue
        if c.command == "G1" and px is not None:
            draw += math.hypot(c.x - px, c.y - py)
        px, py = c.x, c.y
    logger.info("diffusion_passes: u edges %s", ["%.3f" % u for u in u_edges])
    for k, v in stats.items():
        logger.info("  %-8s %s", k, v)
    logger.info("  extent x %.1f..%.1f  y %.1f..%.1f  (bounds %.0f..%.0f / %.0f..%.0f)",
                min(xs), max(xs), min(ys), max(ys), x0, x1, y0, y1)
    logger.info("  draw %.2f m   strokes %d", draw / 1000.0,
                sum(1 for c in out if c.command == "M3"))
    return out
