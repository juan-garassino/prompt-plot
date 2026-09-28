"""CRITICAL — COOLING STRIP. The Ising transition as a PLACE on the sheet.

r01 showed Tc as one configuration plus a deck of five temperature plates and an
order-parameter chart: a scientific figure. This round replaces all of that with
ONE lattice whose temperature ramps linearly across the sheet, T/Tc = 0.70 at the
left edge to 1.80 at the right. Local equilibrium in a gradient is an ordinary
equilibrium ensemble with position-dependent couplings,

    P(s) ~ exp( sum_<ij> K_ij s_i s_j ),   K_ij = J / T(x_ij),

so it is sampled EXACTLY by the same two algorithms as r01 with a per-bond
coupling: checkerboard Metropolis (local field sum_j K_ij s_j) and Wolff with
P_add = 1 - exp(-2 K_ij) per bond (Fortuin-Kasteleyn works for any ferromagnetic
coupling set). Boundary conditions: the top and bottom wrap (the sheet is a
window onto a cylinder, wrap bonds never drawn); the LEFT edge is held "up" by a
fixed reservoir column (the cold wall, drawn as the one straight rule); the right
edge is free. A Wolff cluster that bonds to the reservoir is frozen (the FK
cluster connected to fixed spins cannot flip) — the growth is aborted, which is
the exact Swendsen-Wang rule restricted to the seed's cluster.

What the sheet then shows is physics, not a choice. The frontier is drawn from
the FORTUIN-KASTELEYN (Coniglio-Klein) droplets of the sampled configuration —
one seeded Swendsen-Wang bond draw, p = 1 - exp(-2 K_ij) on satisfied bonds —
because FK droplets percolate EXACTLY at Tc, so the hull of the droplet held by
the cold wall is pinned to the Tc column (gradient percolation, Sapoval, Rosso &
Gouyet 1985). The SPIN-domain shore is not: spin clusters stay large above Tc
and measured shores sit at 1.23-1.45 Tc. That measurement is why this plate
draws droplets, not domain walls (r01's encoding). No symmetric-sector
selection is needed: the gradient forces a frontier in EVERY configuration.

Encodings (one line each):
  * ruled line-screen = the held droplet (the ordered sea), one rule every
    `screen` lattice rows, broken wherever a non-sea cell (a lake) interrupts;
  * crimson, 3 passes = that droplet's hull seen from the hot edge;
  * black sticks = the occupied FK bonds of every free droplet larger than
    `dot_max`, 1/2/3 passes by droplet size (< tier_lo, < tier_hi, above);
  * a dot = one free droplet of 2..`dot_max` sites, at its centroid; a
    singleton (an uncorrelated spin) draws nothing;
  * the ink therefore peaks just past Tc (mean droplet size = susceptibility)
    and thins toward both ends;
  * the sampler is checked against Onsager's exact nearest-neighbour
    correlation column by column (colophon: RMS over 20 bands).

The type lives in the ordered sea, set in the gaps of its ruling.

Entry point: ``ising_cooling_strip``.
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
    giant_type_width,
)
from promptplot.generative.engine.scene3d import Scene3D
from promptplot.generative.generators import _dot
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Point = Tuple[float, float]

TC = 2.0 / math.log(1.0 + math.sqrt(2.0))  # 2.269185... Onsager 1944
BLACK, RED = 0, 1


def _pen(idx: int, colors: int) -> Optional[int]:
    return idx % colors if colors > 1 else None


# ---------------------------------------------------------------------------
# exact reference: Onsager's nearest-neighbour correlation <s_i s_j>(K)
# ---------------------------------------------------------------------------
def _agm(a: float, b: float) -> float:
    for _ in range(60):
        a, b = 0.5 * (a + b), math.sqrt(a * b)
    return a


def onsager_nn(K: float) -> float:
    """<s_i s_j> for the isotropic square lattice at coupling K = J/T (Onsager).
    u/J = -2 <ss> = -coth 2K [1 + (2/pi)(2 tanh^2 2K - 1) K1(k)],
    k = 2 sinh 2K / cosh^2 2K. At Kc it is exactly 1/sqrt2."""
    k = 2.0 * math.sinh(2.0 * K) / math.cosh(2.0 * K) ** 2
    kp = math.sqrt(max(1.0 - k * k, 1e-300))
    K1 = math.pi / (2.0 * _agm(1.0, kp))
    t2 = math.tanh(2.0 * K) ** 2
    return 0.5 / math.tanh(2.0 * K) * (1.0 + (2.0 / math.pi) * (2.0 * t2 - 1.0) * K1)


# ---------------------------------------------------------------------------
# the real simulation: Ising on an NY x NX strip with a temperature ramp
# ---------------------------------------------------------------------------
class GradientIsing:
    """Couplings: vertical bonds in column j carry K(x_j + 1/2); the horizontal
    bond j <-> j+1 carries K(x_{j+1}); the reservoir bond (ghost column -1,
    fixed +1) carries K(0). T(x) = Tc (t_lo + (t_hi - t_lo) x / NX)."""

    def __init__(self, NY: int, NX: int, t_lo: float, t_hi: float, key: int):
        self.NY, self.NX, self.t_lo, self.t_hi = NY, NX, t_lo, t_hi
        self.Kv = [1.0 / self.T(j + 0.5) for j in range(NX)]
        self.Kh = [1.0 / self.T(j + 1.0) for j in range(NX - 1)] + [0.0]
        self.K0 = 1.0 / self.T(0.0)
        self.pv = [1.0 - math.exp(-2.0 * k) for k in self.Kv]
        self.ph = [1.0 - math.exp(-2.0 * k) for k in self.Kh]
        self.p0 = 1.0 - math.exp(-2.0 * self.K0)
        self.npr = np.random.default_rng(key)
        self.pyr = _random.Random(key ^ 0x9E3779B9)
        self.wolff_tried = 0
        self.wolff_frozen = 0

    def T(self, x: float) -> float:
        return TC * (self.t_lo + (self.t_hi - self.t_lo) * x / self.NX)

    def tr_at(self, x: float) -> float:
        return self.T(x) / TC

    def metropolis(self, s: "np.ndarray", sweeps: int) -> "np.ndarray":
        NY, NX = self.NY, self.NX
        KV = np.asarray(self.Kv)[None, :]
        KHR = np.asarray(self.Kh)[None, :]
        KHL = np.asarray([self.K0] + self.Kh[:-1])[None, :]
        ii, jj = np.indices((NY, NX))
        par = (ii + jj) % 2
        up = np.ones((NY, 1), np.int8)
        free = np.zeros((NY, 1), np.int8)
        for _ in range(sweeps):
            for p in (0, 1):
                left = np.concatenate([up, s[:, :-1]], 1)
                right = np.concatenate([s[:, 1:], free], 1)
                h = KV * (np.roll(s, 1, 0) + np.roll(s, -1, 0)) + KHL * left + KHR * right
                dE = 2.0 * s * h
                acc = (dE <= 0) | (self.npr.random(s.shape) < np.exp(-np.minimum(dE, 40.0)))
                s = np.where((par == p) & acc, -s, s).astype(np.int8)
        return s

    def wolff(self, flat: List[int], n: int) -> None:
        NY, NX = self.NY, self.NX
        N = NY * NX
        rnd, rri = self.pyr.random, self.pyr.randrange
        pv, ph, p0 = self.pv, self.ph, self.p0
        for _ in range(n):
            self.wolff_tried += 1
            seed = rri(N)
            old = flat[seed]
            inc = {seed}
            stack = [seed]
            frozen = False
            while stack:
                c = stack.pop()
                i, j = divmod(c, NX)
                if j == 0 and old == 1 and rnd() < p0:
                    frozen = True  # bonded to the held-up reservoir
                    break
                cand = [(((i + 1) % NY) * NX + j, pv[j]), (((i - 1) % NY) * NX + j, pv[j])]
                if j + 1 < NX:
                    cand.append((c + 1, ph[j]))
                if j > 0:
                    cand.append((c - 1, ph[j - 1]))
                for nb, pa in cand:
                    if nb not in inc and flat[nb] == old and rnd() < pa:
                        inc.add(nb)
                        stack.append(nb)
            if frozen:
                self.wolff_frozen += 1
                continue
            for c in inc:
                flat[c] = -old


def simulate(
    rng: SeededRNG, NY: int, NX: int, t_lo: float, t_hi: float, sweeps: int, wolff: int,
    rounds: int, start: str = "up", samples: int = 6,
) -> Tuple[List[int], GradientIsing, Dict[str, object]]:
    key = (rng.seed * 7919 + NX * 131 + NY) & 0xFFFFFFFF
    sim = GradientIsing(NY, NX, t_lo, t_hi, key)
    if start == "up":
        s = np.ones((NY, NX), np.int8)
    else:
        s = np.where(sim.npr.random((NY, NX)) < 0.5, 1, -1).astype(np.int8)
    for _ in range(rounds):  # burn-in
        s = sim.metropolis(s, sweeps)
        flat = [int(v) for v in s.ravel()]
        sim.wolff(flat, wolff)
        s = np.asarray(flat, np.int8).reshape(NY, NX)
    # production: `samples` further decorrelated states; the column energy is
    # averaged over them (vertical bonds only: they carry exactly the column's
    # K, so the comparison with Onsager is clean). The LAST state is drawn.
    corr = np.zeros(NX)
    for k in range(samples):
        if k:
            s = sim.metropolis(s, 10)
            flat = [int(v) for v in s.ravel()]
            sim.wolff(flat, wolff // 2)
            s = np.asarray(flat, np.int8).reshape(NY, NX)
        corr += (s.astype(np.int32) * np.roll(s, 1, 0)).mean(0)
    corr /= samples
    flat = [int(v) for v in s.ravel()]
    exact = np.asarray([onsager_nn(sim.Kv[j]) for j in range(NX)])
    band = max(1, NX // 20)  # 20 bands of ~10 columns
    nb = NX // band
    cb = corr[: nb * band].reshape(nb, band).mean(1)
    eb = exact[: nb * band].reshape(nb, band).mean(1)
    diag: Dict[str, object] = {
        "corr": corr,
        "exact": exact,
        "band_sim": cb,
        "band_exact": eb,
        "band_T": [sim.tr_at((b + 0.5) * band) for b in range(nb)],
        "rms_col": float(np.sqrt(np.mean((corr - exact) ** 2))),
        "rms": float(np.sqrt(np.mean((cb - eb) ** 2))),
        "wolff_frozen": sim.wolff_frozen / max(1, sim.wolff_tried),
        "m_col": s.mean(0),
    }
    return flat, sim, diag


# ---------------------------------------------------------------------------
# domains, the sea, its shore
# ---------------------------------------------------------------------------
def domains(flat: Sequence[int], NY: int, NX: int) -> Tuple[List[int], List[int]]:
    """Exact 4-connected same-spin components; wraps in y, open in x."""
    N = NY * NX
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
            i, j = divmod(c, NX)
            nbs = [((i + 1) % NY) * NX + j, ((i - 1) % NY) * NX + j]
            if j + 1 < NX:
                nbs.append(c + 1)
            if j > 0:
                nbs.append(c - 1)
            for nb in nbs:
                if lab[nb] < 0 and flat[nb] == sp:
                    lab[nb] = cid
                    stack.append(nb)
        sizes.append(cnt)
    return lab, sizes


def sea_and_outside(flat, lab, NY: int, NX: int) -> Tuple[set, List[bool]]:
    """The SEA = the up-domain(s) touching the held-up cold wall. OUTSIDE = the
    8-connected complement of the sea reachable from the hot (free) edge: its
    boundary with the sea is the hull — lakes enclosed by the sea are excluded."""
    sea = {lab[i * NX] for i in range(NY) if flat[i * NX] == 1}
    N = NY * NX
    out = [False] * N
    stack = []
    for i in range(NY):
        c = i * NX + NX - 1
        if lab[c] not in sea:
            out[c] = True
            stack.append(c)
    while stack:
        c = stack.pop()
        i, j = divmod(c, NX)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                jj = j + dj
                if jj < 0 or jj >= NX:
                    continue
                nb = ((i + di) % NY) * NX + jj
                if not out[nb] and lab[nb] not in sea:
                    out[nb] = True
                    stack.append(nb)
    return sea, out


def fk_clusters(flat, sim: "GradientIsing", key: int, bonds: Optional[list] = None):
    """Fortuin-Kasteleyn (Coniglio-Klein) droplets of THIS configuration: each
    satisfied bond is occupied with p = 1 - exp(-2 K_ij), exactly the Swendsen-
    Wang bond draw, seeded. Sites bonded to the held-up reservoir join cluster
    of the virtual node N (size reported as the whole lattice). Returns
    (root per site, size per root). Unlike spin domains, FK droplets are small
    on BOTH sides of Tc and their mean size is the susceptibility — it peaks at
    the transition."""
    NY, NX = sim.NY, sim.NX
    N = NY * NX
    par = list(range(N + 1))

    def find(a: int) -> int:
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb

    r = _random.Random(key ^ 0x5F3759DF).random
    for i in range(NY):
        for j in range(NX):
            a = i * NX + j
            if j == 0 and flat[a] == 1 and r() < sim.p0:
                union(a, N)
            if j + 1 < NX and flat[a] == flat[a + 1] and r() < sim.ph[j]:
                union(a, a + 1)
                if bonds is not None:
                    bonds.append((a, a + 1))
            b = ((i + 1) % NY) * NX + j
            if flat[a] == flat[b] and r() < sim.pv[j]:
                union(a, b)
                if bonds is not None and i + 1 < NY:  # wrap bonds: real, not drawn
                    bonds.append((a, b))
    root = [find(a) for a in range(N)]
    size = [0] * (N + 1)
    for rt in root:
        size[rt] += 1
    size[find(N)] = N  # the reservoir droplet is macroscopic by construction
    return root, size


def fk_sea_outside(root, size, NY: int, NX: int) -> Tuple[List[bool], List[bool]]:
    """The FK SEA = sites in the droplet bonded to the held-up reservoir.
    OUTSIDE = the 8-connected non-sea region reachable from the hot edge; the
    sea/outside edges are the droplet's hull (lakes enclosed by it excluded)."""
    N = NY * NX
    big = max(range(len(size)), key=lambda r: size[r])  # the reservoir root (size N)
    sea = [root[c] == big for c in range(N)]
    out = [False] * N
    stack = []
    for i in range(NY):
        c = i * NX + NX - 1
        if not sea[c]:
            out[c] = True
            stack.append(c)
    while stack:
        c = stack.pop()
        i, j = divmod(c, NX)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                jj = j + dj
                if (di == 0 and dj == 0) or jj < 0 or jj >= NX:
                    continue
                nb = ((i + di) % NY) * NX + jj
                if not out[nb] and not sea[nb]:
                    out[nb] = True
                    stack.append(nb)
    return sea, out


def hull_edges(sea, out, NY: int, NX: int) -> List[Tuple[Point, Point]]:
    segs: List[Tuple[Point, Point]] = []
    for i in range(NY):
        for j in range(NX):
            a = i * NX + j
            if j + 1 < NX and ((sea[a] and out[a + 1]) or (out[a] and sea[a + 1])):
                segs.append(((j + 1, i), (j + 1, i + 1)))
            if i + 1 < NY:
                b = a + NX
                if (sea[a] and out[b]) or (out[a] and sea[b]):
                    segs.append(((j, i + 1), (j + 1, i + 1)))
    return segs


def _poly_len(pts: Sequence[Point]) -> float:
    return sum(
        math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        for i in range(len(pts) - 1)
    )


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def ising_cooling_strip(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    pitch: float = 1.3,
    t_lo: float = 0.70,
    t_hi: float = 1.80,
    sweeps: int = 40,
    wolff: int = 1500,
    rounds: int = 8,
    tier_lo: int = 40,
    tier_hi: int = 400,
    pass_gap: float = 0.22,
    screen: int = 3,
    dot_max: int = 9,
    dot_r: float = 0.2,
    band: float = 11.0,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """COOLING STRIP — one lattice, T/Tc 0.70 (left) to 1.80 (right); the ordered
    sea's shore runs crimson across the strip where the transition happens."""
    x0, y0, x1, y1 = bounds
    black, red = _pen(BLACK, colors), _pen(RED, colors)
    sc = Scene3D(rng, bounds, feed=feed, tip=0.5, fit="none")

    # ------------------------------------------------------------- layout
    edge = 0.4  # keeps the widest pass inside the drawable
    fx0 = x0 + edge
    fx1 = x1 - edge
    fy0 = y0 + edge
    fy1 = y1 - band  # the thermometer band lives above the field
    NX = int((fx1 - fx0) // pitch)
    NY = int((fy1 - fy0) // pitch)
    fx1 = fx0 + NX * pitch  # the field is an exact multiple of the lattice
    fy0 = fy1 - NY * pitch

    def page(u: float, v: float) -> Point:
        # cell coords (column u, row v from the top) -> mm
        return (fx0 + u * pitch, fy1 - v * pitch)

    # ------------------------------------------------------------- physics
    flat, sim, diag = simulate(rng, NY, NX, t_lo, t_hi, sweeps, wolff, rounds)
    lab, sizes = domains(flat, NY, NX)
    key = (rng.seed * 7919 + 17) & 0xFFFFFFFF
    bonds: List[Tuple[int, int]] = []
    fk = fk_clusters(flat, sim, key, bonds)
    root, fsz = fk
    fsea, fout = fk_sea_outside(root, fsz, NY, NX)
    shore = hull_edges(fsea, fout, NY, NX)
    # the droplets: every occupied FK bond outside the held droplet, bucketed by
    # the size of the droplet it belongs to (pen passes 1 / 2 / 3)
    # small droplets (2 .. dot_max sites) collapse to ONE dot at their centroid
    # (tone = droplet count, never spacing); singletons draw nothing (an
    # uncorrelated spin); larger droplets draw their real bond graph.
    buckets: Dict[int, List[Tuple[Point, Point]]] = {1: [], 2: [], 3: []}
    for a, b in bonds:
        if fsea[a]:
            continue
        n = fsz[root[a]]
        if n <= dot_max:
            continue
        ia, ja = divmod(a, NX)
        ib, jb = divmod(b, NX)
        seg = ((ja + 0.5, ia + 0.5), (jb + 0.5, ib + 0.5))
        buckets[1 if n < tier_lo else (2 if n < tier_hi else 3)].append(seg)
    members: Dict[int, List[int]] = {}
    for c in range(NX * NY):
        if not fsea[c] and 2 <= fsz[root[c]] <= dot_max:
            members.setdefault(root[c], []).append(c)
    dots: List[Point] = []
    for cells in members.values():
        i0, _ = divmod(cells[0], NX)
        su = sv = 0.0
        for c in cells:
            i, j = divmod(c, NX)
            di = (i - i0 + NY // 2) % NY - NY // 2  # unwrap across the seam
            su += j + 0.5
            sv += i0 + di + 0.5
        v = (sv / len(cells)) % NY
        dots.append((su / len(cells), v))
    # the sea as a line-screen: every `screen`-th row, runs of held-droplet cells
    screen_runs: List[Tuple[Point, Point]] = []
    for i in range(screen // 2, NY, screen):
        j = 0
        while j < NX:
            if fsea[i * NX + j]:
                k = j
                while k + 1 < NX and fsea[i * NX + k + 1]:
                    k += 1
                screen_runs.append(((j, i + 0.5), (k + 1, i + 0.5)))
                j = k + 1
            else:
                j += 1
    sx = [0.5 * (p[0] + q[0]) for p, q in shore if p[0] == q[0]]  # vertical hull edges
    x_mean = sum(sx) / max(1, len(sx))
    x_std = math.sqrt(sum((v - x_mean) ** 2 for v in sx) / max(1, len(sx)))
    stats = {
        "NX": NX,
        "NY": NY,
        "sea_frac": sum(fsea) / float(NX * NY),
        "spin_domains": len(sizes),
        "shore_edges": len(shore),
        "shore_T": sim.tr_at(x_mean),
        "shore_T_std": (t_hi - t_lo) * x_std / NX,
        "shore_T_min": sim.tr_at(min(sx)) if sx else 0.0,
        "shore_T_max": sim.tr_at(max(sx)) if sx else 0.0,
        "shore_x_mm": fx0 + x_mean * pitch,
        "energy_rms_band": diag["rms"],
        "energy_rms_col": diag["rms_col"],
        "wolff_frozen": diag["wolff_frozen"],
        "tiers": {k: len(v) for k, v in buckets.items()},
        "screen_runs": len(screen_runs),
        "dots": len(dots),
        "droplet_sizes_top": sorted(
            {fsz[r] for r in set(root) if fsz[r] < NX * NY}, reverse=True
        )[:5],
    }
    # for the record: the SPIN-domain shore (the up-domain touching the cold
    # wall) sits well past Tc — spin clusters stay large above Tc, which is why
    # the drawn frontier is the FK droplet's, not the spin domain's.
    ssea, sout = sea_and_outside(flat, lab, NY, NX)
    ssx = [
        j + 1.0
        for i in range(NY)
        for j in range(NX - 1)
        if (lab[i * NX + j] in ssea and sout[i * NX + j + 1])
        or (lab[i * NX + j + 1] in ssea and sout[i * NX + j])
    ]
    stats["spin_shore_T"] = sim.tr_at(sum(ssx) / max(1, len(ssx)))

    # ---------------------------------------------------------------- type
    # One stroke mono everywhere. The words live IN the ordered sea and are set
    # on its ruling: every line of type sits in a gap between two screen rules
    # (pitch R = screen * pitch), so type and lattice share one vertical grid.
    R = screen * pitch
    rule_rows = list(range(screen // 2, NY, screen))

    def rule_y(k: int) -> float:
        return fy1 - (rule_rows[k] + 0.5) * pitch

    def reach(ya: float, yb: float) -> float:
        """Leftmost page-x of the hot-connected outside over the rows spanning
        page-y [ya, yb] — the type must stop short of the shore there."""
        v0 = max(0, int((fy1 - yb) / pitch) - 1)
        v1 = min(NY - 1, int((fy1 - ya) / pitch) + 1)
        best = NX
        for i in range(v0, v1 + 1):
            row = i * NX
            for j in range(NX):
                if fout[row + j]:
                    best = min(best, j)
                    break
        return fx0 + best * pitch

    tx = fx0 + 5.0
    clear = 4.0  # type never comes nearer the shore than this
    # title: three ruling gaps tall, between rules 1 and 4, with the same
    # 1.3 mm clearance to the rule above and below; the two rules it spans are
    # cut (halo), the ones that frame it are not.
    title_base = rule_y(4) + 1.3
    title_h = 3.0 * R - 2.6
    room = reach(title_base - 1.0, title_base + title_h + 1.0) - clear - tx
    title_h = min(title_h, room / (giant_type_width("CRITICAL", 1.0) + 1e-9))
    title_w = giant_type_width("CRITICAL", title_h)
    sc._boxes.append(
        (tx - 1.6, title_base - 0.6, tx + title_w + 1.6, title_base + title_h + 0.6)
    )
    stats["title_h"] = title_h

    def in_gap(k: int, h: float) -> float:
        """Baseline for type of height h centred in the gap under rule k."""
        return rule_y(k + 1) + (R - h) / 2.0

    labels = []
    sub_h = 2.2
    labels.append(("TC IS A PLACE", tx, in_gap(5, sub_h), sub_h, black))
    colo = [
        f"2D ISING   {NX} X {NY}   SEED {rng.seed}",
        "WOLFF AND METROPOLIS",
        f"T OVER TC  {t_lo:.2f} TO {t_hi:.2f}  ALONG X",
        "LEFT EDGE HELD UP   TOP WRAPS",
        "RULED   THE HELD DROPLET",
        f"RED   ITS EDGE   MEAN {stats['shore_T']:.2f} TC",
        "BONDS   THE FREE DROPLETS",
        f"ENERGY VS ONSAGER   RMS {diag['rms']:.3f}",
    ]
    last = len(rule_rows) - 2  # the lowest full gap
    first = last - len(colo) + 1
    col_h = 1.8
    for n, ln in enumerate(colo):
        yb = in_gap(first + n, col_h)
        room = reach(yb - 0.5, yb + col_h + 0.5) - clear - tx
        col_h = min(col_h, room / (_text_width(ln, 1.0) + 1e-9))
    stats["colophon_h"] = col_h
    for n, ln in enumerate(colo):
        labels.append((ln, tx, in_gap(first + n, col_h), col_h, black))
    sc.halo_labels(labels, pad_x=1.2, pad_y=(0.25, 1.25))

    # ---------------------------------------------------------- the marks
    # Marks are queued then emitted in one pass (the pipeline's own stroke
    # optimiser orders them; a hand-sorted serpentine measured no travel gain).
    queue: List[Tuple[List[Point], Optional[int], bool, bool]] = []  # pts, pen, halos, is_dot

    def draw(segs, passes, pen, halos=True):
        for ch in _chain_segments([(page(*p), page(*q)) for p, q in segs], tol=1e-3):
            if len(ch) < 2:
                continue
            for k in range(passes):
                off = (k - (passes - 1) / 2.0) * pass_gap
                queue.append((geo.offset(ch, off) if off else ch, pen, halos, False))

    for seg in screen_runs:  # the ordered sea: one straight rule per run
        queue.append(([page(*seg[0]), page(*seg[1])], black, True, False))
    for key, passes in ((1, 1), (2, 2), (3, 3)):
        draw(buckets[key], passes, black)
    for u, v in dots:
        px, py = page(u, v)
        if not sc._blocked(px, py):
            queue.append(([(px, py)], black, False, True))
    draw(shore, 3, red, halos=False)  # nothing is allowed to cut the shore

    for pts, pen, halos, is_dot in queue:
        if is_dot:
            sc.emit(_dot(pts[0][0], pts[0][1], r=dot_r, color=pen, f=feed))
        else:
            sc.poly(pts, pen=pen, halos=halos)

    # ------------------------------------ the cold wall: the one straight rule
    sc.poly([(fx0, fy0), (fx0, fy1)], pen=black, halos=False)

    # --------------------------------------------- the thermometer, on top
    ry = fy1 + 2.2
    sc.emit(_poly([(fx0, ry), (fx1, ry)], color=black, f=feed))
    steps = int(round((t_hi - t_lo) / 0.05))
    for k in range(steps + 1):
        tr = t_lo + k * 0.05
        x = fx0 + (tr - t_lo) / (t_hi - t_lo) * NX * pitch
        major = abs((tr * 10) - round(tr * 10)) < 1e-6
        is_tc = abs(tr - 1.0) < 1e-6
        ln = 3.2 if is_tc else (1.8 if major else 0.9)
        sc.emit(_poly([(x, ry), (x, ry + ln)], color=red if is_tc else black, f=feed))
        if is_tc or (major and round(tr * 10) % 2 == 0 and abs(tr - 1.0) > 0.15):
            lbl = f"{tr:.2f}"
            h = 2.2
            lx = min(max(x - _text_width(lbl, h) / 2.0, fx0), fx1 - _text_width(lbl, h))
            sc.emit(_stroke_text(lbl, lx, ry + ln + 1.2, h, color=red if is_tc else black, f=feed))

    # ------------------------------------------------ the title (weighted)
    sc.emit(giant_type("CRITICAL", tx, title_base, title_h, pen=black, weight=0.6, tip=0.3, f=feed))

    out_cmds = sc.render()
    ising_cooling_strip.stats = stats  # type: ignore[attr-defined]
    ising_cooling_strip.diag = diag  # type: ignore[attr-defined]
    return out_cmds
