"""CRITICAL — the 2D Ising phase transition, drawn as DOMAIN WALLS.

One rule (neighbours prefer to agree, H = -J sum_<ij> s_i s_j) contains no
length scale, yet at exactly one temperature — Tc = 2/ln(1+sqrt2) = 2.269185,
Onsager 1944 — the correlation length diverges and structure appears at EVERY
size at once. The drawable object is not the spins (a grid of filled squares is
not line work); it is the dual-lattice WALL between disagreeing neighbours:
closed, nested, wandering curves. Their statistics ARE the transition.

The simulation is real and seeded: Wolff single-cluster
(P_add = 1 - exp(-2 beta J)) interleaved with checkerboard Metropolis sweeps,
periodic boundaries, wrap bonds simply not drawn (the sheet is a window onto the
torus). Domains are exact 4-connected components of equal spin.

TWO exact rules turn the physics into pen weight, and they are the piece:

1. LINE WEIGHT = the SCALE of the domain the wall encloses. Passes are keyed to
   min(|A|, |B|) over the two domains a wall separates: 1 pass below `tier_lo`
   sites, 2 up to `tier_hi`, 3 above. At Tc every rung is occupied at once —
   that is scale invariance, drawn, not asserted.
2. RED = the top rung: a wall whose SMALLER domain still covers `red_frac` of
   the lattice. At Tc in the symmetric sector that is a single enormous fractal
   interface between the two coexisting phases; it is the only long-range
   object on the sheet.

Two honesty notes that the sheet itself carries:
  * At Tc a FINITE lattice fluctuates between a magnetised and a symmetric
    configuration. The hero is drawn from the symmetric sector: `sector_draws`
    decorrelated Wolff samples are taken from the one seeded chain and the least
    magnetised is kept. That is a declared restriction of the ensemble, not a
    different physics.
  * 2D Ising SPIN clusters stay large well above Tc (their percolation point is
    Tc itself), so "a big domain" is NOT by itself a critical signature and the
    sheet never claims it is. The critical statement is carried by the weight
    ladder, by the exact Onsager wall density printed in the footer, and by the
    order-parameter knee in the footer chart.

Entry point: ``ising_critical``.
"""

from __future__ import annotations

import math
import random as _random
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine import geometry as geo
from promptplot.generative.engine.kit import _chain_segments, _poly, _stroke_text, _text_width
from promptplot.generative.engine.scene3d import Scene3D
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Point = Tuple[float, float]

TC = 2.0 / math.log(1.0 + math.sqrt(2.0))  # 2.269185...
ONSAGER_WALL_FRAC = (1.0 - 1.0 / math.sqrt(2.0)) / 2.0  # 0.146447: exact at Tc

BLACK, RED = 0, 1


def _pen(idx: int, colors: int) -> Optional[int]:
    return idx % colors if colors > 1 else None


def _spaced(t: str) -> str:
    return " ".join(t)


def _m_exact(tr: float) -> float:
    """Onsager/Yang spontaneous magnetisation, T in units of Tc."""
    if tr >= 1.0:
        return 0.0
    k = math.sinh(2.0 / (tr * TC))
    v = 1.0 - k ** -4
    return v ** 0.125 if v > 0 else 0.0


# ---------------------------------------------------------------------------
# the real simulation
# ---------------------------------------------------------------------------
def _metropolis(s: "np.ndarray", T: float, npr, sweeps: int) -> "np.ndarray":
    """Checkerboard Metropolis: same-colour sites are conditionally independent
    given the other sublattice, so the sublattice update is exact and vectorises."""
    ii, jj = np.indices(s.shape)
    par = (ii + jj) % 2
    for _ in range(sweeps):
        for p in (0, 1):
            nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
            dE = 2.0 * s * nb
            acc = (dE <= 0) | (npr.random(s.shape) < np.exp(-np.minimum(dE, 40.0) / T))
            s = np.where((par == p) & acc, -s, s)
    return s


def _wolff(flat: List[int], L: int, T: float, pyr, n_clusters: int) -> None:
    """Wolff single-cluster, in place on a flat list (fast inner loop).
    P_add = 1 - exp(-2 beta J), J = 1 — what defeats critical slowing down at Tc,
    where Metropolis alone needs tau ~ L^2.17 sweeps to decorrelate."""
    p_add = 1.0 - math.exp(-2.0 / T)
    rnd = pyr.random
    rri = pyr.randrange
    N = L * L
    for _ in range(n_clusters):
        seed = rri(N)
        old = flat[seed]
        flat[seed] = -old
        stack = [seed]
        while stack:
            c = stack.pop()
            i, j = divmod(c, L)
            for nb in (
                ((i + 1) % L) * L + j,
                ((i - 1) % L) * L + j,
                i * L + ((j + 1) % L),
                i * L + ((j - 1) % L),
            ):
                if flat[nb] == old and rnd() < p_add:
                    flat[nb] = -old
                    stack.append(nb)


def _simulate(
    rng: SeededRNG,
    L: int,
    T: float,
    wolff: int,
    sweeps: int,
    sector_draws: int = 0,
    sector_stride: int = 12,
    diag: Optional[Dict[str, float]] = None,
) -> List[int]:
    """One seeded, equilibrated configuration as a flat list of +-1.
    ``sector_draws`` > 0 keeps the least magnetised of that many decorrelated
    samples from the same chain — the declared symmetric-sector restriction."""
    key = (rng.seed * 7919 + int(round(T * 1e6))) & 0xFFFFFFFF
    npr = np.random.default_rng(key)
    pyr = _random.Random(key ^ 0x9E3779B9)
    s = np.where(npr.random((L, L)) < 0.5, 1, -1).astype(np.int8)
    s = _metropolis(s, T, npr, sweeps)
    flat = [int(v) for v in s.ravel()]
    _wolff(flat, L, T, pyr, wolff)
    if sector_draws <= 0:
        return flat
    best: Optional[Tuple[float, List[int]]] = None
    acc = 0.0
    for _ in range(sector_draws):
        _wolff(flat, L, T, pyr, sector_stride)
        mag = abs(sum(flat)) / float(L * L)
        acc += _bond_wall_fraction(flat, L)  # UNRESTRICTED chain mean
        if best is None or mag < best[0]:
            best = (mag, list(flat))
    if diag is not None:
        diag["chain_wall_frac"] = acc / sector_draws
    return best[1] if best else flat


def _bond_wall_fraction(flat: Sequence[int], L: int) -> float:
    """Fraction of the 2 L^2 bonds that are unsatisfied — the internal energy.
    Onsager: exactly (1 - 1/sqrt2)/2 = 0.146447 at Tc, for the FULL ensemble."""
    n = 0
    for i in range(L):
        row = i * L
        for j in range(L):
            a = row + j
            if flat[a] != flat[row + (j + 1) % L]:
                n += 1
            if flat[a] != flat[((i + 1) % L) * L + j]:
                n += 1
    return n / float(2 * L * L)


def _clusters(flat: Sequence[int], L: int) -> Tuple[List[int], List[int]]:
    """Exact 4-connected same-spin components, periodic boundaries."""
    N = L * L
    lab = [-1] * N
    sizes: List[int] = []
    for start in range(N):
        if lab[start] >= 0:
            continue
        cid = len(sizes)
        sp = flat[start]
        lab[start] = cid
        stack = [start]
        cnt = 0
        while stack:
            c = stack.pop()
            cnt += 1
            i, j = divmod(c, L)
            for nb in (
                ((i + 1) % L) * L + j,
                ((i - 1) % L) * L + j,
                i * L + ((j + 1) % L),
                i * L + ((j - 1) % L),
            ):
                if lab[nb] < 0 and flat[nb] == sp:
                    lab[nb] = cid
                    stack.append(nb)
        sizes.append(cnt)
    return lab, sizes


def _wall_tiers(flat, lab, sizes, L: int, tier_lo: int, tier_hi: int, tier_red: int):
    """Dual-lattice walls in unit-square coords, bucketed by the SCALE of the
    domain they enclose. Wrap bonds are not drawn. Keys: 1, 2, 3 = pen passes,
    'red' = the top rung. Also returns the unsatisfied-bond fraction."""
    c = 1.0 / L
    out: Dict[object, List[Tuple[Point, Point]]] = {"red": [], 1: [], 2: [], 3: []}
    nb_total = 0
    nb_wall = 0

    def bucket(la: int, lb: int):
        sa, sb = sizes[la], sizes[lb]
        mn = sa if sa < sb else sb
        if mn >= tier_red:
            return "red"
        return 1 if mn < tier_lo else (2 if mn < tier_hi else 3)

    for i in range(L):
        row = i * L
        for j in range(L):
            a = row + j
            for b, seg in (
                (row + (j + 1) % L, (((j + 1) * c, i * c), ((j + 1) * c, (i + 1) * c))),
                (((i + 1) % L) * L + j, ((j * c, (i + 1) * c), ((j + 1) * c, (i + 1) * c))),
            ):
                nb_total += 1
                if flat[a] == flat[b]:
                    continue
                nb_wall += 1
                if b == row + (j + 1) % L and j + 1 >= L:
                    continue  # wrap bond: counted, never drawn
                if b == ((i + 1) % L) * L + j and i + 1 >= L:
                    continue
                out[bucket(lab[a], lab[b])].append(seg)
    return out, nb_wall / float(nb_total)


# ---------------------------------------------------------------------------
# ONE axonometric basis for the whole scene
# ---------------------------------------------------------------------------
class _Axo:
    """proj(wx, wy, wz) -> screen. Every plate is a unit square in the world
    x-z plane; +y is up. Plates differ only in world FOOTPRINT and position,
    never in a, cd, wy — so nothing can interpenetrate by accident and the
    deck's spacing is derived from its real projected extent."""

    def __init__(self, ox: float, oy: float, a: float, cd: float, wy: float):
        self.ox, self.oy, self.a, self.cd, self.wy = ox, oy, a, cd, wy

    def p(self, wx: float, wy: float, wz: float) -> Point:
        return (self.ox + self.a * (wx - wz), self.oy + self.wy * wy - self.cd * (wx + wz))


def _convex_region(pts: Sequence[Point], grow: float = 0.0) -> geo.Region:
    """A convex polygon as an intersection of half-planes, inflated by ``grow``."""
    pl = list(pts)
    n = len(pl)
    area = 0.5 * sum(
        pl[i][0] * pl[(i + 1) % n][1] - pl[(i + 1) % n][0] * pl[i][1] for i in range(n)
    )
    if area < 0:
        pl = pl[::-1]
    halves = []
    for k in range(n):
        p, q = pl[k], pl[(k + 1) % n]
        dx, dy = q[0] - p[0], q[1] - p[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = dy / ln, -dx / ln  # outward normal for CCW
        halves.append(geo.HalfPlane(nx, ny, -(nx * p[0] + ny * p[1]) - grow))
    return geo.Intersect(*halves)


def _hull(pts: Sequence[Point]) -> List[int]:
    """Andrew monotone chain -> hull vertex indices, CCW."""
    idx = sorted(range(len(pts)), key=lambda i: (pts[i][0], pts[i][1]))

    def cross(o, a, b):
        return (pts[a][0] - pts[o][0]) * (pts[b][1] - pts[o][1]) - (pts[a][1] - pts[o][1]) * (
            pts[b][0] - pts[o][0]
        )

    lower: List[int] = []
    for i in idx:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], i) <= 0:
            lower.pop()
        lower.append(i)
    upper: List[int] = []
    for i in reversed(idx):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], i) <= 0:
            upper.pop()
        upper.append(i)
    return lower[:-1] + upper[:-1]


def _dashes(p0: Point, p1: Point, dash: float = 1.2, gap: float = 1.8) -> List[List[Point]]:
    """House law: projection lines are DOTTED. Never arrows."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    if ln < 1e-6:
        return []
    ux, uy = dx / ln, dy / ln
    out: List[List[Point]] = []
    t = 0.0
    while t < ln:
        e = min(ln, t + dash)
        out.append([(p0[0] + ux * t, p0[1] + uy * t), (p0[0] + ux * e, p0[1] + uy * e)])
        t = e + gap
    return out


def _poly_len(pts: Sequence[Point]) -> float:
    return sum(
        math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        for i in range(len(pts) - 1)
    )


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def ising_critical(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    L: int = 128,
    L_card: int = 24,
    red_frac: float = 0.030,
    tier_lo: int = 10,
    tier_hi: int = 120,
    wolff: int = 90,
    sweeps: int = 16,
    sector_draws: int = 16,
    card_wolff: int = 400,
    card_sweeps: int = 200,
    pass_gap: float = 0.24,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """CRITICAL — order at every scale. A real seeded Wolff/Metropolis run at
    Tc fills a huge square cropped at two paper edges; every wall's line weight
    is keyed to the size of the domain it encloses, and the top rung — the
    interface between the two coexisting macroscopic phases — runs red. Below
    left, five axonometric plates on one shared basis step toward the viewer
    across T/Tc = 0.75 … 1.80, the Tc plate left EMPTY and blown up into the
    hero along dotted projection lines."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    black, red = _pen(BLACK, colors), _pen(RED, colors)

    sc = Scene3D(rng, bounds, feed=feed, tip=0.5, fit="none")
    stats: Dict[str, object] = {}

    # ---------------------------------------------------------------- layout
    edge = 0.6  # keeps the widest (3-pass) stroke inside the drawable area
    hs = 0.72 * W  # hero side
    hx1, hy1 = x1 - edge, y1 - edge  # flush right + top => cropped at two frame edges
    hx0, hy0 = hx1 - hs, hy1 - hs

    temps = [0.75, 0.90, 1.00, 1.20, 1.80]
    ghost_k = 2
    d = 0.88  # world step between plates (they overlap by ~12%)
    zr = 0.72  # world offset of the temperature axis, in front of the plates
    span = 4 * d + 1.0 + (0.65 + zr)  # the deck's REAL projected extent, in units of a
    a = 0.695 * W / span
    cd = 0.55 * a  # depth drop — ONE basis for the whole scene
    deck_top = hy0 - 30.0
    axo = _Axo(ox=x0 + 2.0 + a * (0.65 + zr), oy=deck_top - cd, a=a, cd=cd, wy=1.6 * a)

    # ------------------------------------------------------------- the hero
    diag: Dict[str, float] = {}
    flat = _simulate(
        rng, L, TC, wolff=wolff, sweeps=sweeps, sector_draws=sector_draws, diag=diag
    )
    lab, sizes = _clusters(flat, L)
    tiers, wall_frac = _wall_tiers(
        flat, lab, sizes, L, tier_lo, tier_hi, int(red_frac * L * L)
    )
    stats.update(
        hero_m=abs(sum(flat)) / float(L * L),
        hero_clusters=len(sizes),
        hero_top=[round(s / float(L * L), 3) for s in sorted(sizes, reverse=True)[:4]],
        wall_frac=wall_frac,
        tier_counts={k: len(v) for k, v in tiers.items()},
    )

    def to_page(uv: Point) -> Point:
        return (hx0 + uv[0] * hs, hy0 + uv[1] * hs)


    # --------------------------------------------------------- type (halos)
    sc.halo_labels(
        [
            (_spaced("CRITICAL"), x0 + 2.0, y1 - 27.0, 8.4, black),
            (_spaced("DOMAIN WALLS AT EVERY SCALE"), x0 + 2.0, y1 - 38.0, 2.6, black),
            (_spaced("ONE RULE   NO LENGTH SCALE"), x0 + 2.0, y1 - 45.4, 2.6, black),
        ],
        pad_x=2.2,
        pad_y=(0.9, 1.7),
    )

    # -------------------------------- hero walls: weight = the enclosed scale
    for key, passes, pen in ((1, 1, black), (2, 2, black), (3, 3, black), ("red", 2, red)):
        segs = tiers[key]
        if not segs:
            continue
        for ch in _chain_segments([(to_page(s[0]), to_page(s[1])) for s in segs], tol=1e-2):
            if len(ch) < 2:
                continue
            for p in range(passes):
                off = (p - (passes - 1) / 2.0) * pass_gap
                sc.poly(geo.offset(ch, off) if off else ch, pen=pen, halos=True)

    # the hero's two FREE edges (the other two are the crop) carry corner
    # brackets: the blow-up needs something to land on and they lock the field
    # to the page grid.
    arm = 15.0
    sc.emit(_poly([(hx0, hy0 + arm), (hx0, hy0), (hx0 + arm, hy0)], color=black, f=feed))
    sc.emit(_poly([(hx1 - arm, hy0), (hx1, hy0)], color=black, f=feed))

    # ------------------------------------------------------------- the deck
    def plate(k: int) -> List[Point]:
        cx = k * d
        return [
            axo.p(cx - 0.5, 0.0, -0.5),
            axo.p(cx + 0.5, 0.0, -0.5),
            axo.p(cx + 0.5, 0.0, 0.5),
            axo.p(cx - 0.5, 0.0, 0.5),
        ]

    regions = [_convex_region(plate(k), grow=1.0) for k in range(len(temps))]

    def occlude(poly: List[Point], k: int) -> List[List[Point]]:
        runs = [poly]
        for kk in range(k + 1, len(temps)):  # only NEARER plates occlude
            nxt: List[List[Point]] = []
            for r in runs:
                nxt.extend(geo.clip(r, regions[kk], keep="outside"))
            runs = nxt
        return runs

    # the deck is ONE pen: at L = 24 a 3 pct domain is 17 sites, which is not
    # macroscopic in any meaningful sense, so the red rung is the hero's alone.
    card_stats: List[Optional[Tuple[float, int]]] = []
    for k, tr in enumerate(temps):
        outline = plate(k)
        if k == ghost_k:
            card_stats.append(None)
            for p, q in zip(outline, outline[1:] + outline[:1]):
                for dsh in _dashes(p, q, dash=1.6, gap=1.4):
                    for run in occlude(dsh, k):
                        sc.poly(run, pen=red, halos=False)
            continue

        cflat = _simulate(rng, L_card, tr * TC, wolff=card_wolff, sweeps=card_sweeps)
        clab, csizes = _clusters(cflat, L_card)
        ct, cwf = _wall_tiers(cflat, clab, csizes, L_card, 4, 40, 10 ** 9)
        card_stats.append((abs(sum(cflat)) / float(L_card * L_card), cwf))

        cx = k * d

        def to_plate(uv: Point, cx=cx) -> Point:
            return axo.p(cx + uv[0] - 0.5, 0.0, uv[1] - 0.5)

        for key, passes in ((1, 1), (2, 1), (3, 2)):
            if not ct[key]:
                continue
            for ch in _chain_segments(
                [(to_plate(s[0]), to_plate(s[1])) for s in ct[key]], tol=1e-2
            ):
                if len(ch) < 2:
                    continue
                for run in occlude(ch, k):
                    if _poly_len(run) <= 0.8:
                        continue
                    for p in range(passes):
                        off = (p - (passes - 1) / 2.0) * pass_gap
                        sc.poly(geo.offset(run, off) if off else run, pen=black, halos=False)
        for p, q in zip(outline, outline[1:] + outline[:1]):
            for run in occlude([p, q], k):
                sc.poly(run, pen=black, halos=False)

    # ------------------------------ the temperature axis, in the same basis
    ax_a = axo.p(-0.65, 0.0, zr)
    ax_b = axo.p(4 * d + 0.65, 0.0, zr)
    sc.poly([ax_a, ax_b], pen=black, halos=False)
    for k, tr in enumerate(temps):
        t0 = axo.p(k * d, 0.0, zr)
        t1 = axo.p(k * d, 0.0, zr + (0.34 if k == ghost_k else 0.17))
        sc.poly([t0, t1], pen=red if k == ghost_k else black, halos=False)
        lbl = f"{tr:.2f}"
        sc.emit(
            _stroke_text(
                lbl,
                t1[0] - _text_width(lbl, 2.2) / 2.0,
                t1[1] - 3.9,
                2.2,
                color=red if k == ghost_k else black,
                f=feed,
            )
        )
    sc.emit(
        _stroke_text("T IN UNITS OF TC", x0 + 2.0, deck_top + 5.0, 2.2, color=black, f=feed)
    )

    # --------------------------- the blow-up: dotted projection, never arrows
    # the frustum springs from the hero's BOTTOM edge — the edge that faces the
    # deck — so the two rays open instead of crossing the field.
    ghost = plate(ghost_k)
    hero_box = [(hx0, hy0), (hx1, hy0), (hx1, hy1), (hx0, hy1)]
    pts = ghost + [(hx0, hy0), (hx1, hy0)]
    tag = [0] * 4 + [1, 1]
    hull = _hull(pts)
    blockers = regions + [_convex_region(hero_box, grow=0.0)]
    for n in range(len(hull)):
        i, j = hull[n], hull[(n + 1) % len(hull)]
        if tag[i] == tag[j]:
            continue
        for dsh in _dashes(pts[i], pts[j], dash=1.4, gap=2.1):
            runs = [dsh]
            for reg in blockers:
                nxt: List[List[Point]] = []
                for r in runs:
                    nxt.extend(geo.clip(r, reg, keep="outside"))
                runs = nxt
            for r in runs:
                if _poly_len(r) > 0.35:
                    sc.poly(r, pen=black, halos=False)

    # ------------------------------------------------------------ the footer
    fx, fy = x0 + 4.0, y0 + 32.0
    lines = [
        f"WOLFF AND METROPOLIS   L {L}   PBC   SEED {rng.seed}   SYMMETRIC SECTOR",
        "TC 2.269185   ONSAGER 1944   EXACT",
        f"UNSATISFIED BONDS   CHAIN {diag.get('chain_wall_frac', wall_frac):.4f}"
        f"   ONSAGER {ONSAGER_WALL_FRAC:.4f}",
        f"THIS CONFIGURATION   M {stats['hero_m']:.3f}   {stats['hero_clusters']} DOMAINS",
        "LINE WEIGHT   THE SIZE OF THE DOMAIN THE WALL ENCLOSES",
        f"RED   BOTH DOMAINS OVER {red_frac * 100:.0f} PCT OF THE LATTICE",
    ]
    for n, ln in enumerate(lines):
        sc.emit(_stroke_text(ln, fx, fy - n * 5.6, 2.3, color=black, f=feed))
    sc.emit(_poly([(fx, fy + 4.6), (fx + 118.0, fy + 4.6)], color=black, f=feed))

    # ------------- micro-chart: the exact order parameter, with a knee at Tc
    gx0, gy0 = x1 - 46.0, y0 + 9.0
    gw, gh = 42.0, 33.0
    tlo, thi = 0.55, 1.95

    def gp(tr: float, mv: float) -> Point:
        return (gx0 + (tr - tlo) / (thi - tlo) * gw, gy0 + mv * gh)

    sc.emit(_poly([gp(tlo, 0.0), gp(thi, 0.0)], color=black, f=feed))
    sc.emit(_poly([gp(tlo, 0.0), gp(tlo, 1.08)], color=black, f=feed))
    curve = [gp(tlo + (1.0 - tlo) * i / 60.0, _m_exact(tlo + (1.0 - tlo) * i / 60.0)) for i in range(61)]
    sc.emit(_poly(curve, color=black, f=feed))
    sc.emit(_poly([gp(1.0, 0.0), gp(thi, 0.0)], color=black, f=feed))
    for dsh in _dashes(gp(1.0, 0.0), gp(1.0, 1.06), dash=1.4, gap=1.2):
        sc.poly(dsh, pen=red, halos=False)
    for k, tr in enumerate(temps):
        cs = card_stats[k]
        if cs is None:
            continue
        p = gp(tr, cs[0])
        sc.emit(_poly([(p[0] - 1.0, p[1]), (p[0] + 1.0, p[1])], color=black, f=feed))
        sc.emit(_poly([(p[0], p[1] - 1.0), (p[0], p[1] + 1.0)], color=black, f=feed))
    sc.emit(_stroke_text("ORDER PARAMETER", gx0, gy0 + gh + 6.4, 2.2, color=black, f=feed))
    sc.emit(_stroke_text("EXACT   PLATES L 24", gx0, gy0 + gh + 2.4, 2.1, color=black, f=feed))
    sc.emit(_stroke_text("0.55", gx0 - 2.0, gy0 - 3.9, 2.0, color=black, f=feed))
    sc.emit(_stroke_text("1.95", gx0 + gw - 6.0, gy0 - 3.9, 2.0, color=black, f=feed))

    out = sc.render()
    ising_critical.stats = stats  # type: ignore[attr-defined]
    ising_critical.card_stats = card_stats  # type: ignore[attr-defined]
    return out
