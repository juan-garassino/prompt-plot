"""CRITICAL -- r06 wildcard: THE SUNBURST. The Ising transition as a
renormalisation fan, in the Art Deco canon.

ORDER: RADIAL + NESTED (a stepped sunburst). Nothing from r01-r05 is kept: no single
configuration, no cooling strip, no domain walls, no FK hulls, no coast.

    angle  = temperature, linear in the Kramers-Wannier duality variable u = K* - K
             (zenith = Tc exactly; mirror rays are exact dual temperatures, so the
             Deco symmetry of the fan IS the model's self-duality);
    ray    = one independent equilibrium lattice (243 x 243, periodic) at that T;
    ring   = one Kadanoff blocking step, 3x3 majority rule, outward: block spins of
             size 1, 3, 9, 27 lattice spacings;
    dash   = one block spin of row 0 at that level (5 per ring), black = up,
             gold = down; its LENGTH is c_k(T) x cell pitch, where c_k is the
             measured nearest-neighbour block-spin correlation of the whole lattice
             at blocking level k (duty, never spacing). c_0 = -U/2 exactly.
    crimson arch = where the block size equals the EXACT Onsager correlation length
             xi(T) (xi^-1 = 2u above Tc, 4|u| below).
    crimson ray  = the Tc lattice, the one ray whose c_k does not flow.

Every ray flows to a fixed point as it goes out: cold rays to c = 1 (solid black,
T = 0), hot rays to c = 0 (paper, T = infinity), and the ray at Tc holds its
correlation ring after ring. The two fixed points sit in the cartouches.

Lineage: William Van Alen, the Chrysler Building crown (1930): a sunburst stacked in
stepped terraces, each terrace a step up in scale. Here each terrace is a
renormalisation step, and the sunburst only holds together below Tc.

Entry point: ``ising_rg_sunburst``. The sample (``ising_rg.sample``) is cached beside
this file per seed; a cold cache costs 8-14 minutes.
"""

from __future__ import annotations

import logging
import math
import os
import sys
from typing import List, Tuple

import numpy as np

from promptplot.generative.engine import kit
from promptplot.generative.engine.kit import _GLYPHS, _poly, _stroke_text, _text_width
from promptplot.generative.engine.policies import occlude_crossings
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ising_rg as RG  # noqa: E402

logger = logging.getLogger(__name__)

Pt = Tuple[float, float]

GOLD, BLACK, RED = 0, 1, 2  # layer order light -> dark -> jewel


def _arc(cx: float, cy: float, r: float, a0: float, a1: float, step: float = 0.6) -> List[Pt]:
    """Arc by angle-from-zenith a0 -> a1 (radians), chord <= step mm."""
    n = max(2, int(abs(a1 - a0) * r / step) + 1)
    return [(cx + r * math.sin(a), cy + r * math.cos(a))
            for a in np.linspace(a0, a1, n)]


def _ray_pt(cx, cy, th, r) -> Pt:
    return (cx + r * math.sin(th), cy + r * math.cos(th))


def _centered_text(text: str, cx: float, y: float, h: float, pen, spaced=False,
                   weight=0.0) -> List[GCodeCommand]:
    t = " ".join(text) if spaced else text
    w = _text_width(t, h)
    x = cx - w / 2.0 + (5.6 - 4.0) * h / 6.0 / 2.0  # centre the ink, not the advance
    if weight > 0:
        return kit.giant_type(t, x, y, h, pen=pen, weight=weight, tip=0.3)
    return _stroke_text(t, x, y, h, color=pen)


def _deco_type(text: str, cx: float, y: float, cap: float, pen, condense: float = 0.55,
               track: float = 1.0, stem: float = 0.0, tip: float = 0.3) -> List[GCodeCommand]:
    """Centred Deco display caps: condensed glyphs, wide tracking, and the Deco
    thick/thin contrast -- steep strokes (stems) carry ``stem`` mm of weight as
    parallel passes, horizontals and bowls stay hairline."""
    sy = cap / 6.0
    sx = sy * condense
    gw = 4.0 * sx
    adv = gw + track * cap
    total = len(text) * adv - track * cap
    x = cx - total / 2.0
    passes = max(1, int(round(stem / tip)) + 1) if stem > 0 else 1
    out: List[GCodeCommand] = []
    for ch in text:
        for stroke in _GLYPHS.get(ch, []):
            pts = [(x + gx * sx, y + gy * sy) for gx, gy in stroke]
            thin: List[Pt] = [pts[0]]
            for a, b in zip(pts, pts[1:]):
                steep = abs(b[1] - a[1]) > 2.0 * abs(b[0] - a[0])
                if steep and passes > 1:
                    if len(thin) > 1:
                        out += _poly(thin, color=pen)
                    for q in range(passes):
                        dx = -stem / 2.0 + stem * q / (passes - 1)
                        seg = [(a[0] + dx, a[1]), (b[0] + dx, b[1])]
                        out += _poly(seg if q % 2 == 0 else seg[::-1], color=pen)
                    thin = [b]
                else:
                    thin.append(b)
            if len(thin) > 1:
                out += _poly(thin, color=pen)
        x += adv
    return out


def block_correlation(s: np.ndarray) -> np.ndarray:
    """Nearest-neighbour block-spin correlation <s_i s_j> per lattice (both axes,
    periodic). s: (M, L, L) of +-1. Level 0 equals -U/2 (Onsager: sqrt2/2 at Tc)."""
    s = s.astype(np.float32)
    return 0.5 * ((s * np.roll(s, 1, 1)).mean((1, 2)) + (s * np.roll(s, 1, 2)).mean((1, 2)))


def _ziggurat(xa: float, xb: float, y0: float, h: float, steps: int = 3, inset: float = 4.0,
              rise: float = 2.6) -> List[Pt]:
    """Closed Deco stepped-arch outline (Chrysler window): a rectangle whose top
    steps up ``steps`` times, each step ``inset`` in from both sides."""
    left: List[Pt] = [(xa, y0), (xa, y0 + h)]
    y = y0 + h
    x = xa
    for _ in range(steps):
        x += inset
        left += [(x, y), (x, y + rise)]
        y += rise
    right = [(xa + xb - px, py) for px, py in reversed(left)]
    return left + right + [(xa, y0)]


def ising_rg_sunburst(
    rng: SeededRNG,
    bounds,
    colors: int = 3,
    n_cells: int = 5,
    r_sun: float = 36.0,
    r_out: float = 128.0,
    ring_gap: float = 3.4,
    merge_gap: float = 0.6,
    min_dash: float = 0.9,
    span_deg: float = 87.0,
    arch_passes: int = 2,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    cx = 0.5 * (x0 + x1)
    cy = y1 - 9.0 - r_out  # horizon: rim + dial numerals sit under the drawable top

    d = RG.sample(rng.seed)
    u = d["u"]
    K = d["K"]
    n_rays = len(u)
    jc = n_rays // 2
    levels = 4
    lat = [RG.level_lattice(d, k) for k in range(levels)]
    corr = np.stack([block_correlation(lat[k]) for k in range(levels)])  # (levels, rays)

    span = math.radians(span_deg)
    thetas = np.linspace(-span, span, n_rays)  # linear in u by construction
    band = (r_out - r_sun) / levels

    def pen(p):
        return p if colors > 1 else None

    out: List[GCodeCommand] = []

    # ------------------------------------------------------------- the rays
    # Ring k of ray j shows n_cells block spins (row 0 of blocking level k).
    # Each block spin is a dash CENTRED in its cell whose length is
    # c_k(T) x pitch -- the measured block-spin correlation at that step (duty,
    # never spacing). Colour is the block spin itself: black up, gold down.
    # Adjacent same-spin dashes whose gap would be under ``merge_gap`` are one
    # stroke (a fully correlated ring is a solid ray). Dashes under ``min_dash``
    # are not drawn (pen limit): correlation below min_dash / pitch reads paper.
    pitch = (band - ring_gap) / n_cells
    stats = {"black_mm": 0.0, "gold_mm": 0.0, "red_mm": 0.0, "dashes": 0, "dropped": 0}
    for j, th in enumerate(thetas):
        segs: List[Tuple[float, float, int]] = []
        for k in range(levels):
            row = lat[k][j, 0, :n_cells]
            c = max(0.0, float(corr[k, j]))
            dl = c * pitch
            a = r_sun + k * band + ring_gap / 2.0
            if dl < min_dash:
                stats["dropped"] += n_cells
                continue
            ring_segs: List[List[float]] = []
            for i in range(n_cells):
                mid = a + (i + 0.5) * pitch
                r0, r1 = mid - dl / 2.0, mid + dl / 2.0
                sp = int(row[i])
                if ring_segs and ring_segs[-1][2] == sp and r0 - ring_segs[-1][1] < merge_gap:
                    ring_segs[-1][1] = r1
                else:
                    ring_segs.append([r0, r1, sp])
            segs += [(s0, s1, sp) for s0, s1, sp in ring_segs]
        if j % 2:  # boustrophedon: odd rays walk inward
            segs = [(r1, r0, sp) for (r0, r1, sp) in reversed(segs)]
        for r0, r1, spin in segs:
            if j == jc:
                p, key = RED, "red_mm"
            else:
                p, key = (BLACK, "black_mm") if spin > 0 else (GOLD, "gold_mm")
            out += _poly([_ray_pt(cx, cy, th, r0), _ray_pt(cx, cy, th, r1)], color=pen(p))
            if j == jc:  # the one ray that never flows: a second pass, 0.3 mm over
                out += _poly([(cx + 0.3, cy + r1), (cx + 0.3, cy + r0)], color=pen(p))
            stats[key] += abs(r1 - r0)
            stats["dashes"] += 1

    # ------------------------------------------------------------- the arch
    # radius of a length scale s (lattice units): ring k is centred on s = 3^k
    def rho(s: float) -> float:
        return r_sun + band * (math.log(s, 3) + 0.5)

    u_max = float(np.max(np.abs(u)))
    arch: List[List[Pt]] = []
    for sgn in (-1, 1):
        pts: List[Pt] = []
        for th in np.linspace(sgn * 1e-4, sgn * span, 4000):
            uu = u_max * th / span
            r = rho(RG.xi_exact(uu))
            if r_sun <= r <= r_out:
                q = _ray_pt(cx, cy, th, r)
                if not pts or math.hypot(q[0] - pts[-1][0], q[1] - pts[-1][1]) >= 0.45:
                    pts.append(q)
        arch.append(pts)
    arch_cmds: List[GCodeCommand] = []
    for pts in arch:
        for pi in range(arch_passes):
            off = (pi - (arch_passes - 1) / 2.0) * 0.28
            arch_cmds += _poly(kit._offset_polyline(pts, off), color=pen(RED))
    out += arch_cmds

    # Tc tick at the zenith above the rim
    out += _poly([_ray_pt(cx, cy, 0.0, r_out + 1.0), (cx, cy + r_out + 2.6)], color=pen(RED))

    # ------------------------------------------------------------- the dial
    # Temperature numerals on the rim, placed on the exact duality angle of T:
    # the dial is non-linear in T (compressed near Tc) because the angle is u.
    u_max = float(np.max(np.abs(u)))
    dial_h = 2.0
    for tt in (0.7, 0.8, 0.9, 1.1, 1.25, 1.5):
        uu = RG.u_of_k(1.0 / (tt * RG.TC))
        th = span * uu / u_max
        # tick in the ring gap beyond the rim, numeral outside it
        out += _poly([_ray_pt(cx, cy, th, r_out + 1.2), _ray_pt(cx, cy, th, r_out + 3.0)],
                     color=pen(GOLD))
        lab = ("%.2f" % tt).rstrip("0").rstrip(".") if tt != 1.25 else "1.25"
        w = _text_width(lab, dial_h)
        px, py = _ray_pt(cx, cy, th, r_out + 4.6 + 0.5 * abs(math.sin(th)) * w)
        out += _stroke_text(lab, px - w / 2 + 0.2, py - dial_h / 2, dial_h, color=pen(GOLD))

    # ------------------------------------------------------------- the hub medallion
    # nested gold arcs (thick + thin, Deco) close the sun; inside it the exact Tc.
    for rr, npass in ((r_sun - 2.2, 2), (r_sun - 4.0, 1)):
        for q in range(npass):
            out += _poly(_arc(cx, cy, rr - 0.3 * q, -math.pi / 2, math.pi / 2)[:: 1 - 2 * (q % 2)],
                         color=pen(GOLD))

    # ------------------------------------------------------------- the fixed points
    # Two Deco cartouches flank the title: where the rays are going. T = 0: every
    # block agrees with its neighbours (c = 1), the fan closes solid. T = inf: no
    # block does (c = 0), and there is nothing to draw. The left fan is the rule
    # applied at c = 1, not a picture of data; the right one is honestly empty.
    cw, ch, cy0 = 38.0, 26.0, 12.0
    for side, (xa, lab) in enumerate(((x0 + 8.0, "T = 0   C = 1"),
                                      (x1 - 8.0 - cw, "T = INF   C = 0"))):
        xb = xa + cw
        for q, off in enumerate((0.0, 1.1)):
            zz = _ziggurat(xa + off, xb - off, cy0 + off, ch - 2.0 * off, inset=4.0, rise=2.6)
            out += _poly(zz if q == 0 else zz[::-1], color=pen(GOLD if q == 0 else BLACK))
        hx, hy = xa + cw / 2.0, cy0 + 8.4
        out += _poly(_arc(hx, hy, 3.6, -math.pi / 2, math.pi / 2), color=pen(GOLD))
        if side == 0:
            for a_ in np.linspace(-math.radians(84), math.radians(84), 29):
                out += _poly([_ray_pt(hx, hy, a_, 5.2), _ray_pt(hx, hy, a_, 15.5)],
                             color=pen(BLACK))
        out += _poly([(xa + 3.0, hy - 1.2), (xb - 3.0, hy - 1.2)], color=pen(BLACK))
        out += _deco_type(lab, hx, cy0 + 3.0, 1.8, pen(BLACK), condense=0.7, track=0.5)

    # ------------------------------------------------------------- horizon + type
    yh = cy - 2.2
    out += _poly([(cx - r_out, yh), (cx + r_out, yh)], color=pen(BLACK))

    # ring scale at both feet (the block size), set on the horizon under each ring
    for k in range(levels):
        rc = r_sun + (k + 0.5) * band
        lab = str(3 ** k)
        for sgn in (-1, 1):
            w = _text_width(lab, 2.2)
            out += _stroke_text(lab, cx + sgn * rc - w / 2 + 0.3, yh - 4.2, 2.2, color=pen(BLACK))
    out += _deco_type("BLOCK", cx, yh - 4.2, 2.2, pen(BLACK), condense=0.7, track=0.6)

    ttl_y = yh - 24.0
    out += _deco_type("CRITICAL", cx, ttl_y, 16.0, pen(BLACK), condense=0.5, track=0.62,
                      stem=0.9)
    out += _deco_type("EVERY RAY FLOWS TO A FIXED POINT  BUT ONE", cx, ttl_y - 6.0, 2.4,
                      pen(BLACK), condense=0.7, track=0.55)

    e_rms = float(np.sqrt(np.mean([(d["e"][j] - RG.onsager_energy(K[j])) ** 2
                                   for j in range(n_rays)])))
    t_lo, t_hi = 1.0 / (K[0] * RG.TC), 1.0 / (K[-1] * RG.TC)
    c_tc = corr[:, jc]
    lines = [
        "2D ISING  J 1  H 0  121 LATTICES 243 X 243  SWENDSEN WANG + METROPOLIS  SEED %d"
        % rng.seed,
        "RAY = ONE T  %.2f TO %.2f TC  ANGLE = K* - K  MIRROR RAYS ARE KRAMERS WANNIER DUALS"
        % (t_lo, t_hi),
        "RING = ONE 3 X 3 MAJORITY BLOCKING  DASH = ONE BLOCK SPIN  BLACK UP  GOLD DOWN",
        "DASH LENGTH = NEIGHBOUR CORRELATION  UNDER %.2f IS PAPER  RED ARCH = BLOCK SIZE = XI(T)"
        % (min_dash / pitch),
        "TC RAY %s  ONSAGER 0.7071  ALL RAYS VS ONSAGER RMS %.4f"
        % (" ".join("%.3f" % v for v in c_tc), e_rms / 2.0),
    ]
    for ln in lines:
        logger.info("colophon %.1f mm  %s", _text_width(ln, 1.7), ln)
    ly = ttl_y - 10.6
    for ln in lines:
        out += _centered_text(ln, cx, ly, 1.7, pen(BLACK))
        ly -= 3.4

    # the arch sits in a clean channel: lower pens break where they cross crimson
    out = occlude_crossings(out, gap=1.6, priority=[RED, BLACK, GOLD])
    out += _deco_type("TC", cx, cy + 14.0, 8.0, pen(RED), condense=0.55, track=0.55, stem=0.6)
    out += _deco_type("2.269185", cx, cy + 8.0, 2.4, pen(RED), condense=0.7, track=0.45)
    out += _deco_type("ONSAGER 1944 EXACT", cx, cy + 3.4, 1.6, pen(RED), condense=0.7,
                      track=0.45)
    logger.info("stats %s  corr Tc ray %s", stats, np.round(c_tc, 4))
    logger.info("pitch %.3f  paper under c %.3f  energy rms %.4f", pitch, min_dash / pitch, e_rms)
    return out
