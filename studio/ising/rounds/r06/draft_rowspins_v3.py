"""CRITICAL — r06 wildcard: THE SUNBURST. The Ising transition as a renormalisation
fan, in the Art Deco canon.

ORDER: RADIAL + NESTED (a stepped sunburst). Nothing from r01-r05 is kept: no single
configuration, no cooling strip, no domain walls, no FK hulls, no coast.

    angle  = temperature, linear in the Kramers-Wannier duality variable u = K* - K
             (zenith = Tc exactly; mirror rays are exact dual temperatures, so the
             Deco symmetry of the fan IS the model's self-duality);
    ray    = one independent equilibrium lattice (243 x 243, periodic) at that T;
    ring   = one Kadanoff blocking step, 3x3 majority rule, outward: the four rings
             show block spins of size 1, 3, 9, 27 lattice spacings;
    dash   = one block spin read along row 0 of that level: 9 cells per ring,
             black = up, gold = down (both states are ink: Z2, neither is ground);
    crimson arch = where the block size equals the EXACT Onsager correlation length
             xi(T) (xi^-1 = 2u above Tc, 4|u| below): below the arch a ray still
             looks critical, above it the ray has decided. Its two flanks are mirror
             images offset by exactly log_3 2 of a ring (amplitude ratio 2, exact).

Every ray flows to a fixed point as it goes out: cold rays to solid black (T = 0,
the sunburst), hot rays to gold/black coin flips (T = infinity), and the one ray at
Tc keeps its texture at every ring -- the arch never closes over it.

Lineage: William Van Alen, the Chrysler Building crown (1930): one radiating
sunburst motif stacked in terraces, each terrace a step up in scale. Here each
terrace is a renormalisation step, and the sunburst only holds together below Tc.

Entry point: ``ising_rg_sunburst``.
"""

from __future__ import annotations

import logging
import math
import os
import sys
from typing import List, Optional, Sequence, Tuple

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


def ising_rg_sunburst(
    rng: SeededRNG,
    bounds,
    colors: int = 3,
    n_cells: int = 9,
    r_sun: float = 31.0,
    r_out: float = 133.0,
    ring_gap: float = 1.8,
    run_gap: float = 0.7,
    span_deg: float = 87.0,
    arch_passes: int = 2,
    down: str = "gold",
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    cx = 0.5 * (x0 + x1)
    cy = y1 - 3.0 - r_out  # horizon: fan top sits 3 mm under the drawable top

    d = RG.sample(rng.seed)
    u = d["u"]
    K = d["K"]
    n_rays = len(u)
    levels = 4
    lat = [RG.level_lattice(d, k) for k in range(levels)]

    span = math.radians(span_deg)
    thetas = np.linspace(-span, span, n_rays)  # linear in u by construction
    band = (r_out - r_sun) / levels

    def pen(p):
        return p if colors > 1 else None

    out: List[GCodeCommand] = []

    # ------------------------------------------------------------- the rays
    cell_len = (band - ring_gap) / n_cells
    stats = {"black_mm": 0.0, "gold_mm": 0.0, "dashes": 0}
    # Boustrophedon: even rays are drawn outward, odd rays inward, so each pen
    # layer walks the fan once with only short hops (plots in stroke batches).
    for j, th in enumerate(thetas):
        segs = []
        for k in range(levels):
            row = lat[k][j, 0, :n_cells]
            a = r_sun + k * band + ring_gap / 2.0
            c = 0
            while c < n_cells:
                e = c
                while e + 1 < n_cells and row[e + 1] == row[c]:
                    e += 1
                r0 = a + c * cell_len + (run_gap / 2.0 if c > 0 else 0.0)
                r1 = a + (e + 1) * cell_len - (run_gap / 2.0 if e < n_cells - 1 else 0.0)
                segs.append((r0, r1, int(row[c])))
                c = e + 1
        if j % 2:
            segs = [(r1, r0, sp) for (r0, r1, sp) in reversed(segs)]
        for r0, r1, spin in segs:
            if spin > 0 or down == "gold":
                p = BLACK if spin > 0 else GOLD
                out += _poly([_ray_pt(cx, cy, th, r0), _ray_pt(cx, cy, th, r1)],
                             color=pen(p))
                stats["black_mm" if spin > 0 else "gold_mm"] += abs(r1 - r0)
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

    ttl_y = yh - 26.0
    out += _deco_type("CRITICAL", cx, ttl_y, 16.0, pen(BLACK), condense=0.5, track=0.62,
                      stem=0.9)
    out += _deco_type("EVERY RAY FLOWS TO A FIXED POINT  BUT ONE", cx, ttl_y - 6.6, 2.4,
                      pen(BLACK), condense=0.7, track=0.55)

    e_rms = float(np.sqrt(np.mean([(d["e"][j] - RG.onsager_energy(K[j])) ** 2
                                   for j in range(n_rays)])))
    t_lo, t_hi = 1.0 / (K[0] * RG.TC), 1.0 / (K[-1] * RG.TC)
    lines = [
        "2D ISING  J 1  H 0  121 LATTICES 243 X 243 PERIODIC  SWENDSEN WANG + METROPOLIS  "
        "SEED %d  ENERGY VS ONSAGER RMS %.4f" % (rng.seed, e_rms),
        "RAY = ONE TEMPERATURE  %.2f TC LEFT  TC 2.269185 AT THE ZENITH  %.2f TC RIGHT  "
        "ANGLE = K* - K  MIRROR RAYS ARE KRAMERS WANNIER DUALS" % (t_lo, t_hi),
        "RING = ONE 3 X 3 MAJORITY BLOCKING  BLOCKS 1 3 9 27 OUTWARD  ROW 0 OF EACH  "
        "BLACK UP  GOLD DOWN  COLD SECTOR CHOSEN UP",
        "RED ARCH = BLOCK SIZE EQUALS XI(T)  ONSAGER 1944 EXACT  XI ABOVE TC / XI BELOW TC = 2",
    ]
    ly = ttl_y - 11.8
    for ln in lines:
        out += _centered_text(ln, cx, ly, 1.8, pen(BLACK))
        ly -= 3.9

    # the arch sits in a clean channel: lower pens break where they cross crimson
    out = occlude_crossings(out, gap=1.6, priority=[RED, BLACK, GOLD])
    out += _deco_type("TC", cx, cy + 24.0, 3.2, pen(RED), condense=0.7, track=0.5)
    logger.info("dashes %d", stats["dashes"])
    logger.info("rays black %.0f mm gold %.0f mm  energy rms %.4f", stats["black_mm"],
                stats["gold_mm"], e_rms)
    return out
