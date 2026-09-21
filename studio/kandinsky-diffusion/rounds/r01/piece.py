"""DIFFUSION — the corrected Kandinsky recreation.

ABSTRACT ORDER (one line): *one straight chord in, a nest of concentric orbits
out* — the forward kernel is closed form so it is a single ruled line, the
reverse chain is the SAME operator applied again and again so it is a stack of
orbits around the prior, one orbit per step, and every orbit's texture is that
step's signal-to-noise.

The reference plate (``ref/reference.png``) is recreated in composition and
colour and CORRECTED in mechanism.  Full audit in NOTES.md; the corrections
that are visible on the sheet:

  * the denoiser is not a box passed through once — it is a LOOP, drawn as 26
    concentric orbits around the prior, labelled with the real step count;
  * forward and reverse are not mirror twins — the forward is ONE straight
    chord (q(x_t|x_0) is closed form, any t in one shot), the reverse is a
    countable ladder of discrete orbits;
  * the noise end is isotropic — a circular Gaussian ball, one pen, no ribbon,
    no preferred direction, no leftover palette;
  * the dissolve is not linear — everything on the sheet is keyed to the exact
    cosine schedule, which barely moves early and collapses late and fast;
  * provenance dies at a SCALE-DEPENDENT time — coarse structure keeps its
    colour long after fine detail has gone black;
  * the last reverse step injects no noise, so the outermost orbit is the only
    exact circle in the stack.

Exact mappings (each stated once, used everywhere):

    orbit index k        = one denoising step (26 drawn, stride 38 of T = 1000)
    orbit DUTY (inked
      fraction of the
      circumference)     = abar_t, the signal's share of the state variance
    orbit WOBBLE split   = sqrt(abar_t) * signal + sqrt(1 - abar_t) * noise,
                           i.e. the DDPM state equation on the radius
    colour anywhere      = provenance, and it exists only where SNR > 1
    melt dot RADIUS      = the feature scale l it stands for
    melt dot POSITION    = an honest draw from q(x_u | x_0) at its own u
    ruler tick spacing   = the schedule (even timesteps, placed by sqrt(abar))
    descending squares   = sigma_t of the injected noise; the fourth is absent
                           because the final step injects none

Style canon: BAUHAUS / Kandinsky colour-block (STYLES.md §1) on cream, five
pens.  Flat by canon and by subject — declared, per rubric dimension 7: the one
depth cue used is occlusion (the orbit stack knocks out what crosses it).

Contract: kandinsky_diffusion(rng, bounds, colors=5) -> list[GCodeCommand]
"""

from __future__ import annotations

import logging
import math
from typing import Callable, List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.engine import kit
from promptplot.generative.engine.kit import _poly, _stroke_text, _text_width

logger = logging.getLogger(__name__)

Pt = Tuple[float, float]
Bounds = Tuple[float, float, float, float]

# ---------------------------------------------------------------------------
# pens — Kandinsky primaries on cream
# ---------------------------------------------------------------------------
BLACK, RED, BLUE, GOLD, GREEN = 0, 1, 2, 3, 4


def _pens(colors: int) -> List[Optional[int]]:
    if colors <= 1:
        return [None] * 5
    return [i % colors for i in range(5)]


# ---------------------------------------------------------------------------
# the schedule — cosine (Nichol & Dhariwal 2021), used exactly
# ---------------------------------------------------------------------------
_S = 0.008
T_STEPS = 1000
N_ORBITS = 26


def _f(u: float) -> float:
    return math.cos(0.5 * math.pi * (u + _S) / (1.0 + _S)) ** 2


_F0 = _f(0.0)


def abar(u: float) -> float:
    """abar_t for normalised time u = t/T, normalised so abar(0) = 1."""
    u = 0.0 if u < 0.0 else (1.0 if u > 1.0 else u)
    return max(0.0, min(1.0, _f(u) / _F0))


def u_at_abar(a: float) -> float:
    """Inverse of :func:`abar` — the u at which abar takes the value ``a``."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if abar(mid) > a:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def sigma_post(u_t: float, u_prev: float) -> float:
    """Posterior sd sigma_t of the ancestral sampler's injected noise."""
    a_t, a_p = abar(u_t), abar(u_prev)
    if a_t >= a_p or a_t <= 0.0:
        return 0.0
    alpha = a_t / a_p
    beta = 1.0 - alpha
    return math.sqrt(max(0.0, beta * (1.0 - a_p) / (1.0 - a_t)))


# u where the state is half signal, half noise: SNR = abar/(1-abar) = 1
U_SNR1 = u_at_abar(0.5)


# ---------------------------------------------------------------------------
# small geometry helpers (no engine edits — everything local)
# ---------------------------------------------------------------------------


def _pip(poly: Sequence[Pt]) -> Callable[[Pt], bool]:
    """Point-in-polygon predicate for a closed ring of vertices."""
    pts = list(poly)

    def keep(p: Pt) -> bool:
        x, y = p
        inside = False
        n = len(pts)
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            if (y0 > y) != (y1 > y):
                xx = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                if xx > x:
                    inside = not inside
        return inside

    return keep


def _hatch(
    poly: Sequence[Pt],
    angle_deg: float,
    pitch: float,
    pen: Optional[int],
    f: int = 2100,
) -> List[GCodeCommand]:
    """Parallel-line fill of a polygon at a chosen angle and pitch."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    cx, cy = 0.5 * (min(xs) + max(xs)), 0.5 * (min(ys) + max(ys))
    half = 0.5 * math.hypot(max(xs) - min(xs), max(ys) - min(ys)) + pitch
    a = math.radians(angle_deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    runs = []
    k = -int(half / pitch) - 1
    while k * pitch <= half:
        off = k * pitch
        p0 = (cx + nx * off - dx * half, cy + ny * off - dy * half)
        p1 = (cx + nx * off + dx * half, cy + ny * off + dy * half)
        runs.append([p0, p1])
        k += 1
    return kit._emit_runs(kit._clip_runs(runs, _pip(poly)), pen, f=f)


def _outline(poly: Sequence[Pt], pen: Optional[int], f: int = 2100) -> List[GCodeCommand]:
    return _poly(list(poly) + [poly[0]], color=pen, f=f)


def _checker(
    rect: Bounds, nx: int, ny: int, pen: Optional[int], pitch: float = 0.62
) -> List[GCodeCommand]:
    """Checkerboard: alternate cells solid, the rest blank paper."""
    x0, y0, x1, y1 = rect
    cw, ch = (x1 - x0) / nx, (y1 - y0) / ny
    out: List[GCodeCommand] = []
    for j in range(ny):
        for i in range(nx):
            if (i + j) % 2:
                continue
            out += kit.fill_rect(
                x0 + i * cw, y0 + j * ch, x0 + (i + 1) * cw, y0 + (j + 1) * ch,
                spacing=pitch, pen=pen,
            )
    return out


def _clip_out_annulus(
    cmds: Sequence[GCodeCommand], c: Pt, r_in: float, r_out: float
) -> List[GCodeCommand]:
    """Knock a ring-shaped hole out of a command list (occlusion by the stack)."""

    def keep(p: Pt) -> bool:
        d = math.hypot(p[0] - c[0], p[1] - c[1])
        return d <= r_in or d >= r_out

    out: List[GCodeCommand] = []
    for pen, run in kit._runs_from_cmds_pens(cmds):
        out += kit._emit_runs(kit._clip_runs([run], keep), pen)
    return out


def _clip_rect(cmds: Sequence[GCodeCommand], rect: Bounds) -> List[GCodeCommand]:
    keep = kit._rect_keep(rect)
    out: List[GCodeCommand] = []
    for pen, run in kit._runs_from_cmds_pens(cmds):
        out += kit._emit_runs(kit._clip_runs([run], keep), pen)
    return out


# ---------------------------------------------------------------------------
# the data composition — ONE grammar, two draws
# ---------------------------------------------------------------------------
# Both end compositions come from this generator with different rng streams:
# same plane multiset, same module grid, different arrangement.  That is what
# "same distribution, different sample" means, and it is why the right-hand
# block must not be a copy of the left-hand one.

_PLANE_KINDS = ("vbar", "hbar", "checker", "disc", "rings", "wedge", "quarter")


def _composition(
    rng, rect: Bounds, P: Sequence[Optional[int]], cols: int = 3, rows: int = 5
) -> List[GCodeCommand]:
    """A Kandinsky colour-block draw: planes on a module grid, each plane a
    DIFFERENT line-fill (the texture assignment is the design decision the
    Kandinsky set asks for, not a default 45-degree hatch everywhere)."""
    x0, y0, x1, y1 = rect
    cw, rh = (x1 - x0) / cols, (y1 - y0) / rows
    cells = [(i, j) for j in range(rows) for i in range(cols)]

    # a fixed multiset of planes -> the two draws share a distribution
    bag = list(_PLANE_KINDS) + ["vbar", "hbar", "checker", "rings"]
    rng.shuffle(bag)
    rng.shuffle(cells)

    out: List[GCodeCommand] = []
    used: List[Tuple[int, int, int, int]] = []

    def free(i, j, w, h) -> bool:
        if i + w > cols or j + h > rows:
            return False
        for (ui, uj, uw, uh) in used:
            if i < ui + uw and ui < i + w and j < uj + uh and uj < j + h:
                return False
        return True

    for kind in bag:
        w, h = (1, 1)
        if kind in ("vbar", "rings"):
            w, h = 1, 2
        elif kind == "hbar":
            w, h = 2, 1
        elif kind == "disc":
            w, h = 1, 1
        placed = False
        for (i, j) in cells:
            for (ww, hh) in ((w, h), (1, 1)):
                if free(i, j, ww, hh):
                    used.append((i, j, ww, hh))
                    bx0 = x0 + i * cw + 0.9
                    by0 = y0 + j * rh + 0.9
                    bx1 = x0 + (i + ww) * cw - 0.9
                    by1 = y0 + (j + hh) * rh - 0.9
                    out += _plane(rng, kind, (bx0, by0, bx1, by1), P)
                    placed = True
                    break
            if placed:
                break

    # the composition's own black structure: two rules and one heavy diagonal
    out += _poly([(x0, y0 + rh * 2), (x1, y0 + rh * 2)], color=P[BLACK], f=2000)
    out += _poly([(x0 + cw, y0), (x0 + cw, y1)], color=P[BLACK], f=2000)
    for d in (-0.32, 0.0, 0.32):
        out += _poly(
            [(x0 - 3 + d, y1 + 6), (x1 + 3 + d, y0 - 6)], color=P[BLACK], f=1800
        )
    return out


def _plane(rng, kind: str, r: Bounds, P: Sequence[Optional[int]]) -> List[GCodeCommand]:
    """One flat Kandinsky plane, rendered as a deliberately chosen line-fill."""
    x0, y0, x1, y1 = r
    w, h = x1 - x0, y1 - y0
    cx, cy = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    if kind == "vbar":
        # crimson mass -> VERTICAL hatch (the fill runs with the bar)
        return _hatch([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], 90.0, 0.85, P[RED])
    if kind == "hbar":
        # green mass -> HORIZONTAL serpentine (one long stroke, cheap ink)
        return kit.fill_rect(x0, y0, x1, y1, spacing=0.85, pen=P[GREEN])
    if kind == "checker":
        return _checker((x0, y0, x1, y1), 3, 3, P[BLACK])
    if kind == "disc":
        # gold -> Archimedean SPIRAL fill
        rr = 0.44 * min(w, h)
        return kit.fill_disc(cx, cy, rr, spacing=0.8, pen=P[GOLD])
    if kind == "rings":
        # blue -> CONCENTRIC rings, the Bauhaus target
        rr = 0.44 * min(w, h)
        return kit.concentric_disc(cx, cy, rr, rings=max(3, int(rr / 1.5)), pen=P[BLUE])
    if kind == "wedge":
        # blue triangle -> DIAGONAL hatch, cross-grain to everything else
        tri = [(x0, y0), (x1, y0), (x0 + 0.5 * w, y1)]
        return _hatch(tri, -38.0, 1.0, P[BLUE]) + _outline(tri, P[BLACK])
    # quarter: crimson quarter-disc as concentric ARCS
    a0 = 0.5 * math.pi * rng.randint(0, 3)
    return kit.fill_quarter(cx, cy, 0.49 * min(w, h) * 1.6, a0, spacing=0.85, pen=P[RED])


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def kandinsky_diffusion(rng, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    P = _pens(colors)
    out: List[GCodeCommand] = []

    # ---- the frame's shared grid -------------------------------------------
    Y_TOP_RULE = y0 + 0.872 * H          # the top rule every corner mark sits on
    Y_BAND_TOP = y0 + 0.800 * H
    Y_BAND_BOT = y0 + 0.185 * H
    Y_RAIL = y0 + 0.130 * H              # the schedule ruler
    CX = x0 + 0.622 * W                  # mandala axis — also the title's stop
    CY = y0 + 0.487 * H
    R_OUT = 0.285 * min(W * 1.36, H * 1.36)
    R_CORE = 0.285 * R_OUT
    C = (CX, CY)
    SIG = R_CORE / 2.55                  # 1 sigma of the prior, in mm

    # ---- 1. the data composition x_0 (left) --------------------------------
    A = (x0 + 0.010 * W, Y_BAND_BOT + 0.055 * H, x0 + 0.238 * W, Y_BAND_TOP)
    block_a = _composition(rng, A, P, cols=3, rows=5)
    out += block_a

    # ---- 2. the forward melt -----------------------------------------------
    # Every dot is a genuine draw x_u = c + sqrt(abar)*(x_0 - c)
    #                                 + sqrt(1-abar)*sigma*eps at its own u.
    # No layout offset, no ribbon: the equation alone puts the dots where they
    # are, which is why the cloud is a comet and not the reference's S-curve.
    src: List[Tuple[float, float, Optional[int]]] = []
    for pen, run in kit._runs_from_cmds_pens(block_a):
        for p in run[::3]:
            src.append((p[0], p[1], pen))
    rng.shuffle(src)

    L_REF = 2.0        # the reference feature scale of the colour-death rule
    melt: List[GCodeCommand] = []
    n_dots = 560
    for i in range(n_dots):
        px, py, pen = src[i % len(src)]
        u = rng.random()
        s, n = math.sqrt(abar(u)), math.sqrt(1.0 - abar(u))
        qx = CX + s * (px - CX) + n * SIG * rng.gauss(0.0, 1.0)
        qy = CY + s * (py - CY) + n * SIG * rng.gauss(0.0, 1.0)
        if not (x0 + 1 < qx < x1 - 1 and Y_BAND_BOT - 4 < qy < Y_BAND_TOP + 6):
            continue
        d = math.hypot(qx - CX, qy - CY)
        if R_CORE - 0.5 < d < R_OUT + 1.2:      # occluded by the orbit stack
            continue
        # feature scale this dot stands for -> log-uniform over [0.55, 7.2] mm
        ell = 0.55 * (7.2 / 0.55) ** (i / max(1, n_dots - 1))
        # provenance survives while sqrt(abar)*l > sqrt(1-abar)*L_REF
        keeps_colour = s * ell > n * L_REF
        pn = pen if keeps_colour else P[BLACK]
        if ell > 2.4:
            melt += kit.fill_disc(qx, qy, 0.5 * ell, spacing=0.72, pen=pn)
        elif ell > 1.1:
            melt += kit.circle(qx, qy, 0.5 * ell, pen=pn, n=18)
        else:
            melt += kit.circle(qx, qy, max(0.26, 0.5 * ell), pen=pn, n=9)
    out += melt

    # the closed-form chords: q(x_t | x_0) needs no iteration, so the forward
    # process is drawn as STRAIGHT RULES converging on the prior — five thin
    # ones stopped at the rim, and one heavy black chord driven all the way in.
    for k in range(5):
        ax = A[0] + (A[2] - A[0]) * (0.08 + 0.21 * k)
        ay = A[1] + (A[3] - A[1]) * (0.94 - 0.2 * k)
        dx, dy = CX - ax, CY - ay
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        t = 0.0
        seg: List[Pt] = []
        while t < L - R_OUT - 1.5:
            seg.append((ax + ux * t, ay + uy * t))
            t += 2.6
            seg.append((ax + ux * t, ay + uy * t))
            out += _poly(seg[-2:], color=P[BLACK], f=2200)
            t += 2.2
    hx = A[0] + 0.12 * (A[2] - A[0])
    hy = Y_BAND_TOP + 0.030 * H
    for d in (-0.34, 0.0, 0.34):
        out += _poly([(hx + d, hy), (CX + d, CY)], color=P[BLACK], f=1700)

    # ---- 3. the reverse loop: 26 orbits around the prior --------------------
    pitch = (R_OUT - R_CORE) / N_ORBITS
    stride = T_STEPS // N_ORBITS
    amp = 0.33 * pitch
    # the structure being recovered: one fixed low-frequency target, identical
    # for every orbit, because every step is refining the SAME sample
    sig_h = [(3, rng.uniform(0, 2 * math.pi), 1.0),
             (5, rng.uniform(0, 2 * math.pi), 0.62),
             (8, rng.uniform(0, 2 * math.pi), 0.38)]
    sig_norm = sum(a for _, _, a in sig_h)

    def signal(th: float) -> float:
        return sum(a * math.sin(m * th + ph) for m, ph, a in sig_h) / sig_norm

    orbit_cmds: List[GCodeCommand] = []
    r_snr1 = R_CORE
    for k in range(N_ORBITS):
        u = 1.0 - k / (N_ORBITS - 1)                    # ring 0 = t = T
        u_prev = 1.0 - (k - 1) / (N_ORBITS - 1) if k else 1.0
        ab = abar(u)
        s, nz = math.sqrt(ab), math.sqrt(1.0 - ab)
        r_k = R_CORE + (k + 1) * pitch
        last = k == N_ORBITS - 1
        sg = 0.0 if last else sigma_post(u, u_prev)     # final step injects none
        nh = [(m, rng.uniform(0, 2 * math.pi)) for m in (13, 19, 27)]
        duty = ab                                       # inked share = signal share
        if ab >= 0.5 and r_snr1 == R_CORE:
            r_snr1 = r_k
        pen = P[RED] if (abs(ab - 0.5) < 0.5 / (N_ORBITS - 1)) else P[BLACK]
        passes = 2 if (pen == P[RED] or last) else 1

        seg: List[Pt] = []
        N = 720
        for q in range(N + 1):
            th = 2 * math.pi * q / N
            wob = amp * (s * signal(th)
                         + nz * sum(math.sin(m * th + ph) for m, ph in nh) / 3.0
                         + 0.9 * sg * math.sin(41 * th + 0.7))
            rr = r_k + wob
            on = ((q * 1.0 / N * 17.0) % 1.0) < max(0.03, min(1.0, duty))
            if on:
                seg.append((CX + rr * math.cos(th), CY + rr * math.sin(th)))
            else:
                if len(seg) >= 2:
                    for _ in range(passes):
                        orbit_cmds += _poly(seg, color=pen, f=2300)
                seg = []
        if len(seg) >= 2:
            for _ in range(passes):
                orbit_cmds += _poly(seg, color=pen, f=2300)
    out += orbit_cmds

    # the prior: an ISOTROPIC Gaussian ball.  One pen, circular level sets, no
    # orientation and no memory of either composition's palette.
    for _ in range(130):
        gx, gy = rng.gauss(0.0, SIG), rng.gauss(0.0, SIG)
        if math.hypot(gx, gy) > R_CORE - 1.6:
            continue
        out += kit.circle(CX + gx, CY + gy, 0.3, pen=P[BLACK], n=8)
    for m in (1, 2):
        out += kit.dotted_circle(CX, CY, m * SIG, pen=P[BLACK])
    out += kit.circle(CX, CY, R_CORE, pen=P[GOLD], n=140)

    # ---- 4. colour lives only outside the SNR = 1 orbit ---------------------
    # Three Kandinsky planes laid over the stack, each knocked out inside the
    # half-information radius: below SNR = 1 the state has no identity to show.
    def outside_snr1(p: Pt) -> bool:
        d = math.hypot(p[0] - CX, p[1] - CY)
        return r_snr1 + 0.8 <= d <= R_OUT + 0.4

    planes: List[GCodeCommand] = []
    tri_b = [(CX - 0.10 * R_OUT, CY + 1.30 * R_OUT),
             (CX + 0.92 * R_OUT, CY - 0.30 * R_OUT),
             (CX - 0.86 * R_OUT, CY - 0.62 * R_OUT)]
    planes += _hatch(tri_b, 62.0, 3.1, P[BLUE])
    tri_r = [(CX - 1.22 * R_OUT, CY + 0.52 * R_OUT),
             (CX + 0.30 * R_OUT, CY + 1.02 * R_OUT),
             (CX + 0.04 * R_OUT, CY - 1.16 * R_OUT)]
    planes += _hatch(tri_r, -24.0, 3.4, P[RED])
    quad = [(CX, CY), (CX + 1.15 * R_OUT, CY),
            (CX + 1.15 * R_OUT, CY - 1.15 * R_OUT), (CX, CY - 1.15 * R_OUT)]
    planes += _hatch(quad, 8.0, 3.6, P[GREEN])
    out += _clip_keep(planes, outside_snr1)

    # ---- 5. the sample x_0' (right, cropped at the frame) -------------------
    B = (x1 - 0.212 * W, Y_BAND_BOT + 0.075 * H, x1 + 0.030 * W, Y_BAND_TOP - 0.02 * H)
    block_b = _composition(rng, B, P, cols=3, rows=5)
    block_b = _clip_out_annulus(block_b, C, R_CORE, R_OUT + 0.6)
    out += _clip_rect(block_b, (x0, y0, x1, y1))

    # ---- 6. bottom rail: the schedule as a RULER, not a plot ----------------
    RX0, RX1 = x0 + 0.318 * W, x1 - 0.010 * W
    out += _poly([(RX0, Y_RAIL), (RX1, Y_RAIL)], color=P[BLACK], f=2000)
    for j in range(N_ORBITS + 1):
        u = j / N_ORBITS
        px = RX0 + (RX1 - RX0) * (1.0 - math.sqrt(abar(u)))
        big = abs(abar(u) - 0.5) < 0.5 / N_ORBITS
        out += _poly([(px, Y_RAIL), (px, Y_RAIL + (3.4 if big else 1.9))],
                     color=P[RED] if big else P[BLACK], f=2000)
    px = RX0 + (RX1 - RX0) * (1.0 - math.sqrt(abar(U_SNR1)))
    out += _poly([(px, Y_RAIL - 2.6), (px, Y_RAIL)], color=P[RED], f=2000)
    out += _stroke_text("S N R  1", px + 1.4, Y_RAIL - 4.6, 2.3, color=P[RED])
    out += _stroke_text("t = 0", RX0, Y_RAIL + 5.0, 2.6, color=P[BLACK])
    lab = "t = T = 1 0 0 0"
    out += _stroke_text(lab, RX1 - _text_width(lab, 2.6), Y_RAIL + 5.0, 2.6, color=P[BLACK])
    out += _stroke_text("√ᾱₜ", 0.5 * (RX0 + RX1) - 4.0, Y_RAIL + 5.0, 3.0, color=P[BLACK])

    cap_y = Y_RAIL - 9.0
    out += _stroke_text("q ( xₜ | x₀ )   O N E   S T E P ,   C L O S E D   F O R M",
                        RX0, cap_y, 2.6, color=P[BLACK])
    cap2 = "p θ ( · )   × 1 0 0 0   S T E P S   ·   ε θ   I N S I D E   E A C H"
    out += _stroke_text(cap2, RX1 - _text_width(cap2, 2.6), cap_y - 5.6, 2.6, color=P[BLACK])

    # ---- 7. bottom-left corner: the prior's sigma key -----------------------
    kx, ky = x0 + 0.012 * W, y0 + 0.012 * H
    for m in (1, 2, 3):
        arc = [(kx + m * SIG * math.cos(a * math.pi / 40),
                ky + m * SIG * math.sin(a * math.pi / 40)) for a in range(21)]
        out += _poly(arc, color=P[BLUE], f=2200)
    out += _poly([(kx, ky), (kx + 3.4 * SIG, ky)], color=P[BLACK], f=2000)
    out += _poly([(kx, ky), (kx, ky + 3.4 * SIG)], color=P[BLACK], f=2000)
    out += _stroke_text("1 σ   2 σ   3 σ", kx + 1.5, ky + 3.4 * SIG + 1.6, 2.4, color=P[BLACK])
    out += _stroke_text("𝒩 ( 0 , I )", kx + 1.5, ky + 3.4 * SIG + 6.4, 2.8, color=P[BLACK])

    # ---- 8. title + top furniture ------------------------------------------
    th = 0.072 * H
    tx = x0 + 0.062 * W
    out += kit.giant_type("DIFFUSION", tx, Y_TOP_RULE + 0.010 * H, th,
                          pen=P[BLACK], weight=0.95, tip=0.5)
    # the Kandinsky chevron mark that opens the reference's title
    out += _poly([(tx - 0.048 * W, Y_TOP_RULE + th * 1.28),
                  (tx - 0.028 * W, Y_TOP_RULE + th * 0.62),
                  (tx - 0.048 * W, Y_TOP_RULE - 0.004 * H)], color=P[BLACK], f=2000)
    out += _poly([(tx - 0.030 * W, Y_TOP_RULE + th * 1.28),
                  (tx - 0.030 * W, Y_TOP_RULE - 0.004 * H)], color=P[BLACK], f=2000)
    eq = "xₜ = √ᾱₜ x₀ + √ ( 1 − ᾱₜ ) ε"
    out += _stroke_text(eq, tx, Y_TOP_RULE - 0.030 * H, 3.0, color=P[BLACK])

    trx0 = tx + kit.giant_type_width("DIFFUSION", th) + 0.028 * W
    out += _poly([(trx0, Y_TOP_RULE), (x1, Y_TOP_RULE)], color=P[BLACK], f=2000)
    # two discs on the rule: the two end samples.  Same law, different draw —
    # the plate is NOT a round trip, and this is where that is said.
    dgx = trx0 + 0.055 * W
    out += kit.fill_disc(dgx, Y_TOP_RULE + 0.026 * H, 0.020 * H, spacing=0.7, pen=P[GOLD])
    out += kit.fill_disc(dgx + 0.072 * W, Y_TOP_RULE + 0.026 * H, 0.020 * H,
                         spacing=0.7, pen=P[BLUE])
    out += _stroke_text("≠", dgx + 0.033 * W, Y_TOP_RULE + 0.020 * H, 4.2, color=P[BLACK])
    out += _stroke_text("S A M E  L A W  ·  D I F F E R E N T  D R A W",
                        dgx - 0.010 * W, Y_TOP_RULE + 0.052 * H, 2.4, color=P[BLACK])

    # the vertical rule on the mandala axis, carrying sigma_t as squares that
    # shrink to nothing — the fourth is missing because the last step is noiseless
    out += _poly([(CX, Y_TOP_RULE), (CX, CY + R_OUT + 0.9)], color=P[BLACK], f=2000)
    for i, uu in enumerate((0.92, 0.64, 0.36)):
        sg = sigma_post(uu, min(1.0, uu + 1.0 / N_ORBITS))
        side = 1.1 + 5.4 * sg
        yy = Y_TOP_RULE - 0.028 * H - i * 0.042 * H
        out += kit.fill_rect(CX - side / 2, yy - side, CX + side / 2, yy,
                             spacing=0.6, pen=P[BLACK])
    out += _stroke_text("σₜ", CX + 2.6, Y_TOP_RULE - 0.052 * H, 2.6, color=P[BLACK])

    # top-right corner mark, locked to the top rule and the stack's right rim
    qx_ = CX + R_OUT
    out += _poly([(qx_, Y_TOP_RULE - 0.014 * H), (qx_, y1)], color=P[BLACK], f=2000)
    out += _poly([(qx_ - 0.030 * W, y1 - 0.022 * H), (x1, y1 - 0.022 * H)],
                 color=P[BLACK], f=2000)
    out += kit.fill_rect(x1 - 0.026 * W, y1 - 0.016 * H, x1 - 0.008 * W, y1 - 0.002 * H,
                         spacing=0.6, pen=P[RED])

    out += kit.scale_footer((x0, y0, x1, y1), "26 OF T=1000  ·  STRIDE 38",
                            pen=P[BLACK], height=2.4)

    # ---- bounds guard -------------------------------------------------------
    out = _clip_rect(out, (x0, y0, x1, y1))
    logger.info(
        "kandinsky_diffusion: %d cmds  SNR1 at u=%.3f (r=%.1fmm)  stride %d",
        len(out), U_SNR1, r_snr1, stride,
    )
    return out


def _clip_keep(cmds: Sequence[GCodeCommand], keep) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for pen, run in kit._runs_from_cmds_pens(cmds):
        out += kit._emit_runs(kit._clip_runs([run], keep), pen)
    return out
