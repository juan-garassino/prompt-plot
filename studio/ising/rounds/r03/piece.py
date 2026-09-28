"""COASTLINE — the 2D Ising model at Tc, full bleed, drawn only as its walls.

Round r03 of `ising` (thesis COASTLINE, parent r01). The deck, the chart and the
footer are gone. One real critical configuration fills the sheet, and the whole
design is the WEIGHT LADDER:

    every wall is weighted by log8 of the domain it encloses
    (min(|A|, |B|) over the two domains it separates)

        1 .. 7 sites     -> DUST: one pen touch at the domain's centroid
        8 .. 63          -> 1 pass
        64 .. 511        -> 2 passes
        512 .. 4095      -> 3 passes
        4096 and over    -> 4 passes, CRIMSON  (8^4 sites)

Kandinsky's point / line / plane: a domain below the ruler is a POINT, every
other domain is a LINE whose weight is the PLANE it encloses. At Tc the rungs
are populated in a power law (1217 / 109 / 9 / 1 / 2 on seed 7). The crimson
rung is the macroscopic interface — in the symmetric sector the wall between
the two coexisting phases.

The twist is Mandelbrot's (1967): HOW LONG IS THE COAST. The crimson wall is
walked with Richardson dividers at 1, 4 and 16 lattice steps; the lengths
disagree, the 16-step walk is drawn DOTTED over the coast, and the slope of
log L against log ruler gives the dimension, printed beside the exact 11/8 of
a critical Ising spin-cluster boundary (SLE kappa 3).

Composition lever: translation is a symmetry of the torus, so the sheet may cut
it open anywhere. The widest red-free bay is found (toroidal chessboard
distance) and the torus is rolled to put it at ``bay_uv``.

Physics (all real, all seeded through the passed SeededRNG): J = 1, zero field,
a RECTANGULAR periodic Lx x Ly lattice whose aspect is the sheet's, at
Tc = 2/ln(1+sqrt2). Checkerboard Metropolis burn-in, then Wolff single-cluster
(P_add = 1 - exp(-2 beta J)). Domains = exact 4-connected components with PBC.
Wrap bonds are counted, never drawn — the sheet IS the torus, cut open.

Entry point: ``ising_coastline``.
"""

from __future__ import annotations

import math
import random as _random
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine import geometry as geo
from promptplot.generative.engine.kit import (
    _chain_segments,
    _poly,
    _stroke_text,
    _text_width,
    giant_type,
)
from promptplot.generative.engine.scene3d import Scene3D
from promptplot.generative.generators import _dot
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Point = Tuple[float, float]

TC = 2.0 / math.log(1.0 + math.sqrt(2.0))  # 2.269185...
ONSAGER_WALL_FRAC = (1.0 - 1.0 / math.sqrt(2.0)) / 2.0  # 0.146447 exact at Tc
D_HULL_EXACT = 11.0 / 8.0  # critical Ising spin-cluster boundary, SLE kappa = 3

BLACK, RED = 0, 1


def _pen(idx: int, colors: int) -> Optional[int]:
    return idx % colors if colors > 1 else None


def _spaced(t: str) -> str:
    return " ".join(t)


# ---------------------------------------------------------------------------
# the real simulation — rectangular torus, rows = y, cols = x
# ---------------------------------------------------------------------------
def _nbrs(c: int, Lx: int, Ly: int):
    i, j = divmod(c, Lx)
    return (
        ((i + 1) % Ly) * Lx + j,
        ((i - 1) % Ly) * Lx + j,
        i * Lx + (j + 1) % Lx,
        i * Lx + (j - 1) % Lx,
    )


def _metropolis(s: "np.ndarray", T: float, npr, sweeps: int) -> "np.ndarray":
    """Checkerboard Metropolis — same-colour sites are conditionally independent
    given the other sublattice (needs even Lx, Ly), so the update is exact."""
    ii, jj = np.indices(s.shape)
    par = (ii + jj) % 2
    for _ in range(sweeps):
        for p in (0, 1):
            nb = np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1)
            dE = 2.0 * s * nb
            acc = (dE <= 0) | (npr.random(s.shape) < np.exp(-np.minimum(dE, 40.0) / T))
            s = np.where((par == p) & acc, -s, s)
    return s


def _wolff(flat: List[int], Lx: int, Ly: int, T: float, pyr, n_clusters: int) -> int:
    """Wolff single-cluster in place. Returns total sites flipped."""
    p_add = 1.0 - math.exp(-2.0 / T)
    rnd = pyr.random
    rri = pyr.randrange
    N = Lx * Ly
    flipped = 0
    for _ in range(n_clusters):
        seed = rri(N)
        old = flat[seed]
        flat[seed] = -old
        stack = [seed]
        flipped += 1
        while stack:
            c = stack.pop()
            i, j = divmod(c, Lx)
            for nb in (
                ((i + 1) % Ly) * Lx + j,
                ((i - 1) % Ly) * Lx + j,
                i * Lx + (j + 1) % Lx,
                i * Lx + (j - 1) % Lx,
            ):
                if flat[nb] == old and rnd() < p_add:
                    flat[nb] = -old
                    stack.append(nb)
                    flipped += 1
    return flipped


def _bond_wall_fraction(flat: Sequence[int], Lx: int, Ly: int) -> float:
    """Unsatisfied fraction of the 2 N bonds. Onsager: 0.146447 at Tc."""
    a = np.asarray(flat, dtype=np.int8).reshape(Ly, Lx)
    n = int((a != np.roll(a, 1, 0)).sum() + (a != np.roll(a, 1, 1)).sum())
    return n / float(2 * Lx * Ly)


def _simulate(rng: SeededRNG, Lx: int, Ly: int, T: float, wolff: int, sweeps: int,
              sector_draws: int, sector_stride: int, diag: Dict[str, float]) -> List[int]:
    key = (rng.seed * 7919 + int(round(T * 1e6))) & 0xFFFFFFFF
    npr = np.random.default_rng(key)
    pyr = _random.Random(key ^ 0x9E3779B9)
    s = np.where(npr.random((Ly, Lx)) < 0.5, 1, -1).astype(np.int8)
    s = _metropolis(s, T, npr, sweeps)
    flat = [int(v) for v in s.ravel()]
    diag["burn_flipped"] = _wolff(flat, Lx, Ly, T, pyr, wolff) / float(Lx * Ly)
    best: Optional[Tuple[float, List[int]]] = None
    acc, mags = 0.0, []
    for _ in range(sector_draws):
        _wolff(flat, Lx, Ly, T, pyr, sector_stride)
        mag = abs(sum(flat)) / float(Lx * Ly)
        mags.append(mag)
        acc += _bond_wall_fraction(flat, Lx, Ly)  # UNRESTRICTED chain mean
        if best is None or mag < best[0]:
            best = (mag, list(flat))
    diag["chain_wall_frac"] = acc / max(1, sector_draws)
    diag["chain_mags"] = mags  # type: ignore[assignment]
    return best[1] if best else flat


def _clusters(flat: Sequence[int], Lx: int, Ly: int) -> Tuple[List[int], List[int]]:
    """Exact 4-connected same-spin components, periodic boundaries."""
    N = Lx * Ly
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
            for nb in _nbrs(c, Lx, Ly):
                if lab[nb] < 0 and flat[nb] == sp:
                    lab[nb] = cid
                    stack.append(nb)
        sizes.append(cnt)
    return lab, sizes


def _rung(mn: int, ladder: Sequence[int]) -> int:
    """0 = singleton (dot), 1..3 = black passes, 4 = crimson."""
    r = 0
    for t in ladder:
        if mn >= t:
            r += 1
    return r


def _walls(flat, lab, sizes, Lx: int, Ly: int, ladder: Sequence[int]):
    """Dual-lattice walls in LATTICE units (x = col, y = row), bucketed by rung
    of min(|A|,|B|). Wrap bonds are not drawn."""
    out: Dict[int, List[Tuple[Point, Point]]] = {1: [], 2: [], 3: [], 4: []}
    for i in range(Ly):
        row = i * Lx
        for j in range(Lx):
            a = row + j
            if j + 1 < Lx:
                b = a + 1
                if flat[a] != flat[b]:
                    sa, sb = sizes[lab[a]], sizes[lab[b]]
                    r = _rung(sa if sa < sb else sb, ladder)
                    if r:
                        out[r].append(((j + 1.0, i), (j + 1.0, i + 1.0)))
            if i + 1 < Ly:
                b = a + Lx
                if flat[a] != flat[b]:
                    sa, sb = sizes[lab[a]], sizes[lab[b]]
                    r = _rung(sa if sa < sb else sb, ladder)
                    if r:
                        out[r].append(((j, i + 1.0), (j + 1.0, i + 1.0)))
    return out


def _box_count(segs: Sequence[Tuple[Point, Point]], sizes: Sequence[int]) -> List[int]:
    """Boxes of side b (lattice units) touched by the wall set, b in sizes."""
    mids = [((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5) for a, b in segs]
    res = []
    for bs in sizes:
        res.append(len({(int(mx // bs), int(my // bs)) for mx, my in mids}))
    return res


def _widest_bay(flat, lab, sizes, Lx: int, Ly: int, red_min: int):
    """Centre (row, col) and radius of the largest red-free square on the
    torus: chessboard distance to the nearest site touching a crimson wall,
    by repeated toroidal dilation."""
    a = np.asarray(flat, dtype=np.int8).reshape(Ly, Lx)
    S = np.asarray(sizes)[np.asarray(lab)].reshape(Ly, Lx)
    red = np.zeros((Ly, Lx), dtype=bool)
    for ax in (0, 1):
        b = np.roll(a, -1, axis=ax)
        Sb = np.roll(S, -1, axis=ax)
        m = (a != b) & (np.minimum(S, Sb) >= red_min)
        red |= m
        red |= np.roll(m, 1, axis=ax)
    if not red.any():
        return (Ly // 2, Lx // 2), 0
    dist = np.zeros((Ly, Lx), dtype=np.int32)
    cur = red.copy()
    k = 0
    while not cur.all():
        k += 1
        nxt = cur.copy()
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                nxt |= np.roll(cur, (di, dj), axis=(0, 1))
        dist[nxt & ~cur] = k
        cur = nxt
    i, j = np.unravel_index(int(np.argmax(dist)), dist.shape)
    return (int(i), int(j)), int(dist[i, j])


def _dust_centroids(lab, sizes, Lx: int, Ly: int, below: int) -> List[Point]:
    """Centroid (lattice units, torus-unwrapped about the first site) of every
    domain smaller than ``below`` sites, in scan order."""
    acc: Dict[int, List[float]] = {}
    for c, d in enumerate(lab):
        if sizes[d] >= below:
            continue
        i, j = divmod(c, Lx)
        a = acc.get(d)
        if a is None:
            acc[d] = [j + 0.5, i + 0.5, 1.0, j + 0.5, i + 0.5]
            continue
        x, y = j + 0.5, i + 0.5
        x += Lx * round((a[3] - x) / Lx)
        y += Ly * round((a[4] - y) / Ly)
        a[0] += x
        a[1] += y
        a[2] += 1.0
    out = []
    for a in acc.values():
        out.append(((a[0] / a[2]) % Lx, (a[1] / a[2]) % Ly))
    return out


def _sandbox_dim(segs, Lx: int, Ly: int, radii=(4, 8, 16)):
    """Mass-radius (sandbox) dimension of a wall set: mean number of wall
    edges within Chebyshev radius R of a wall edge, M(R) ~ R^D. Centres are
    every 5th edge at least max(R) from the sheet edge (no randomness)."""
    if not segs:
        return float("nan"), []
    mids = np.array([((a[0] + b[0]) * 0.5, (a[1] + b[1]) * 0.5) for a, b in segs])
    R = max(radii)
    ok = (mids[:, 0] > R) & (mids[:, 0] < Lx - R) & (mids[:, 1] > R) & (mids[:, 1] < Ly - R)
    cen = mids[ok][::5]
    M = []
    for r in radii:
        M.append(float(np.mean([(np.max(np.abs(mids - c), axis=1) <= r).sum() for c in cen])))
    D = float(np.polyfit(np.log(radii), np.log(M), 1)[0])
    return D, [round(m, 1) for m in M]


def _divider(poly: Sequence[Point], r: float) -> Tuple[List[Point], float]:
    """Richardson/Mandelbrot divider walk: step a pair of dividers of opening
    ``r`` along the polyline. Returns the nodes and the length n*r + tail."""
    if len(poly) < 2:
        return [], 0.0
    nodes = [poly[0]]
    cur = poly[0]
    k = 1
    while k < len(poly):
        # first vertex at distance >= r from cur
        while k < len(poly) and math.hypot(poly[k][0] - cur[0], poly[k][1] - cur[1]) < r:
            k += 1
        if k >= len(poly):
            break
        a, b = poly[k - 1], poly[k]
        dx, dy = b[0] - a[0], b[1] - a[1]
        fx, fy = a[0] - cur[0], a[1] - cur[1]
        A = dx * dx + dy * dy
        B = 2 * (fx * dx + fy * dy)
        C = fx * fx + fy * fy - r * r
        disc = max(0.0, B * B - 4 * A * C)
        t = (-B + math.sqrt(disc)) / (2 * A) if A > 0 else 1.0
        t = min(1.0, max(0.0, t))
        cur = (a[0] + t * dx, a[1] + t * dy)
        nodes.append(cur)
        poly = [cur] + list(poly[k:])
        k = 1
    tail = math.hypot(poly[-1][0] - cur[0], poly[-1][1] - cur[1])
    return nodes, (len(nodes) - 1) * r + tail


def _dashes(p0: Point, p1: Point, dash: float = 1.2, gap: float = 1.8) -> List[List[Point]]:
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


def _ring(c: Point, r: float, n: int = 10) -> List[Point]:
    return [(c[0] + r * math.cos(2 * math.pi * k / n), c[1] + r * math.sin(2 * math.pi * k / n))
            for k in range(n + 1)]


def _slope(xs: Sequence[float], ys: Sequence[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    return sxy / sxx


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def ising_coastline(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    Lx: int = 176,
    ladder: Tuple[int, int, int, int] = (8, 64, 512, 4096),
    wolff: int = 160,
    sweeps: int = 16,
    sector_draws: int = 16,
    sector_stride: int = 14,
    band: float = 17.0,
    gaps: Tuple[float, float, float] = (0.26, 0.24, 0.21),
    dot_r: float = 0.22,
    show_ruler: bool = True,
    title_w: float = 0.26,
    bay_uv: Optional[Tuple[float, float]] = (0.30, 0.34),
    ruler_sites: float = 16.0,
    node_r: float = 0.55,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """HOW LONG IS THE COAST — a full-bleed critical Ising configuration whose
    wall weight is log16 of the enclosed domain; the crimson 4-pass rung is the
    macroscopic interface, box-counted at three rulers in the colophon."""
    x0, y0, x1, y1 = bounds
    black, red = _pen(BLACK, colors), _pen(RED, colors)
    sc = Scene3D(rng, bounds, feed=feed, tip=0.5, fit="none")

    # ------------------------------------------------------------ layout
    edge = 0.7  # the 4-pass stroke stays inside the drawable area
    fx0, fx1 = x0 + edge, x1 - edge
    pitch = (fx1 - fx0) / Lx
    Ly = int((y1 - edge - (y0 + band)) / pitch) // 2 * 2  # even: checkerboard exact
    fy1 = y1 - edge
    fy0 = fy1 - Ly * pitch

    def page(p: Point) -> Point:  # lattice (col, row) -> mm; row 0 at the top
        return (fx0 + p[0] * pitch, fy1 - p[1] * pitch)

    # --------------------------------------------------------- the physics
    diag: Dict[str, float] = {}
    flat = _simulate(rng, Lx, Ly, TC, wolff, sweeps, sector_draws, sector_stride, diag)
    lab, sizes = _clusters(flat, Lx, Ly)
    # TRANSLATION IS A SYMMETRY of the torus: where the sheet cuts it open is
    # a free choice, and it is the composition lever. Find the widest bay the
    # crimson interface leaves (largest red-free disc, toroidal chessboard
    # distance) and roll the torus so that bay sits at ``bay_uv``.
    roll = (0, 0)
    bay_r = 0
    if bay_uv is not None:
        (bi, bj), bay_r = _widest_bay(flat, lab, sizes, Lx, Ly, ladder[-1])
        ti, tj = int(bay_uv[1] * Ly), int(bay_uv[0] * Lx)
        roll = ((ti - bi) % Ly, (tj - bj) % Lx)
        a2 = np.roll(np.asarray(flat, dtype=np.int8).reshape(Ly, Lx), roll, axis=(0, 1))
        flat = [int(v) for v in a2.ravel()]
        lab, sizes = _clusters(flat, Lx, Ly)
    walls = _walls(flat, lab, sizes, Lx, Ly, ladder)
    N = Lx * Ly
    dust = _dust_centroids(lab, sizes, Lx, Ly, ladder[0])

    # the coast measured three ways. PRINTED: Richardson dividers (the literal
    # coastline method) at 1/4/16 steps, dimension from the 2..16 slope.
    # DIAGNOSTIC only (stats + NOTES): box counting and the sandbox estimate.
    rulers = [1, 4, 16]
    nb = _box_count(walls[4], rulers) if walls[4] else [0, 0, 0]
    nb[0] = len(walls[4])  # ruler = one lattice step: the drawn length itself
    D, sand = _sandbox_dim(walls[4], Lx, Ly, radii=(4, 8, 16))
    coast = [c for c in _chain_segments(walls[4], tol=1e-3) if len(c) >= 2]
    div_len = {}
    div_nodes: Dict[float, List[List[Point]]] = {}
    for rr in (1.0, 2.0, 4.0, 8.0, 16.0):
        tot, nl = 0.0, []
        for c in coast:
            nodes, ln = _divider(c, rr)
            tot += ln
            nl.append(nodes)
        div_len[rr] = tot
        div_nodes[rr] = nl
    D_div = 1.0 - _slope([math.log(k) for k in (2.0, 4.0, 8.0, 16.0)],
                         [math.log(div_len[k]) for k in (2.0, 4.0, 8.0, 16.0)])
    top = sorted(sizes, reverse=True)
    stats = dict(
        Lx=Lx, Ly=Ly, N=N, pitch=pitch,
        m=abs(sum(flat)) / float(N),
        roll=roll, bay_radius_sites=bay_r,
        domains=len(sizes),
        top=[round(s / float(N), 4) for s in top[:5]],
        dust=len(dust),
        singletons=sum(1 for v in sizes if v == 1),
        sandbox=sand,
        rung_domains=[sum(1 for s in sizes if _rung(s, ladder) == r) for r in range(5)],
        rung_segs={r: len(v) for r, v in walls.items()},
        wall_frac_this=_bond_wall_fraction(flat, Lx, Ly),
        wall_frac_chain=diag["chain_wall_frac"],
        chain_mags=[round(v, 3) for v in diag["chain_mags"]],  # type: ignore[arg-type]
        burn_flipped=diag["burn_flipped"],
        box_counts=dict(zip(rulers, nb)),
        coast_chains=len(coast),
        coast_chain_lens=sorted((len(c) - 1 for c in coast), reverse=True)[:8],
        divider_len_sites={k: round(v, 1) for k, v in div_len.items()},
        D_divider=D_div,
        rung_sizes=[
            sorted((v for v in sizes if _rung(v, ladder) == r), reverse=True)[:6]
            for r in (2, 3, 4)
        ],
        D_sandbox=D,
        D_box=-_slope([math.log(b) for b in rulers[1:]] + [0.0],
                      [math.log(max(1, n)) for n in nb[1:]] + [math.log(max(1, nb[0]))]),
    )

    # ----------------------------------------------------------- the walls
    offs = {
        1: [0.0],
        2: [-gaps[0] / 2, gaps[0] / 2],
        3: [-gaps[1], 0.0, gaps[1]],
        4: [-1.5 * gaps[2], -0.5 * gaps[2], 0.5 * gaps[2], 1.5 * gaps[2]],
    }
    for r in (1, 2, 3, 4):
        pen = red if r == 4 else black
        segs = [(page(a), page(b)) for a, b in walls[r]]
        for ch in _chain_segments(segs, tol=1e-2):
            if len(ch) < 2:
                continue
            for o in offs[r]:
                sc.poly(geo.offset(ch, o) if o else ch, pen=pen, halos=False)

    # the ruler: the 16-site divider walk laid over the coast, DOTTED (house
    # law: construction is dotted, never arrows). It cuts every fjord narrower
    # than the ruler — that is where the missing metres went.
    if show_ruler:
        for nodes in div_nodes[ruler_sites]:
            if len(nodes) < 3:  # a stub cut by the frame: counted, not drawn
                continue
            pg = [page(q) for q in nodes]
            for p0, p1 in zip(pg, pg[1:]):
                for d in _dashes(p0, p1, dash=0.9, gap=1.5):
                    sc.poly(d, pen=black, halos=False)
            for q in pg:
                sc.emit(_poly(_ring(q, node_r), color=black, f=feed))

    # dust: every domain below the first rung is ONE pen touch at its centroid
    for cx, cy in dust:
        px, py = page((cx, cy))
        sc.emit(_dot(px, py, r=dot_r, color=black, f=feed))

    # ------------------------------------------------------------- the type
    # one left edge (fx0) for everything; the band under the field is the
    # sheet's only quiet zone.
    th = 4.2
    title = _spaced("HOW LONG IS THE COAST")
    ty = fy0 - 5.0 - th
    # the title is set on the 2-pass rung of the ladder: type is a wall too
    sc.emit(giant_type(title, fx0, ty, th, pen=black, weight=title_w, tip=title_w, f=feed))
    rl = [1.0, 4.0, ruler_sites]
    Lm = [div_len[k] * pitch / 1000.0 for k in rl]
    l1 = (
        f"{Lm[0]:.2f} M WITH A {rl[0] * pitch:.1f} MM RULER   "
        f"{Lm[1]:.2f} M WITH {rl[1] * pitch:.1f} MM   "
        f"{Lm[2]:.2f} M WITH {rl[2] * pitch:.0f} MM DOTTED   "
        f"DIMENSION {D_div:.2f}   EXACT 11 OVER 8"
    )
    l2 = (
        f"ISING AT TC   {Lx} X {Ly} TORUS   SEED {rng.seed}   "
        f"BONDS {diag['chain_wall_frac']:.4f}  ONSAGER {ONSAGER_WALL_FRAC:.4f}   "
        f"WEIGHT   LOG 8 OF THE DOMAIN ENCLOSED   RED   4096 SITES UP"
    )
    ch_ = min(1.8, (fx1 - fx0) / max(_text_width(l1, 1.0), _text_width(l2, 1.0)))
    sc.emit(_stroke_text(l1, fx0, ty - 5.2, ch_, color=black, f=feed))
    sc.emit(_stroke_text(l2, fx0, ty - 9.2, ch_, color=black, f=feed))
    stats["title_w"] = _text_width(title, th)
    stats["caption_h"] = ch_
    stats["lengths_m"] = Lm

    out = sc.render()
    ising_coastline.stats = stats  # type: ignore[attr-defined]
    return out
