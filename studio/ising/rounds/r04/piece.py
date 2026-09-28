"""CRITICAL — COOLING STRIP (r04 iterate). The Ising transition as a PLACE on the sheet.

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

Encodings (r04 — parent r02; sampler, lattice, ramp and reservoir unchanged):
  * ruled line-screen = the held FK cluster (the ordered sea), one rule every
    `screen` lattice rows, laid ON the lattice line under its row and broken
    wherever a non-held cell interrupts; where a drawn hull already inks that
    line the rule yields to it;
  * crimson, 3 passes = that cluster's hull seen from the hot edge (4-connected
    outside: diagonally pinched pockets are lakes, so the coast is ONE line);
  * black = the closed dual-lattice HULL of every free FK cluster of >= `cut`
    sites (the r01/r03 wall-loop vocabulary; no primal-lattice bond sticks),
    1/2/3 passes for `cut`..`tier_mid`-1 / ..`tier_hi`-1 / `tier_hi` and up,
    on EVERY edge of the cluster (a shared edge takes the heavier rung, an
    edge that is also coast is crimson);
  * nothing at all for clusters under `cut` sites (singletons included): the
    hot end is bare paper because the clusters there are small;
  * the y seam (the strip is a cylinder) is placed where the coast crosses it
    once and it cuts the fewest drawn hulls — a pure display translation.

The type lives in the ordered sea: CRITICAL runs up it (cap line on the left
axis), the key sits in the gaps of the ruling below it.

Entry point: ``ising_cooling_strip_iterate``.
"""

from __future__ import annotations

import logging
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
    OUTSIDE = the 4-connected non-sea region reachable from the hot edge; the
    sea/outside edges are the droplet's hull. r04: 4-connected (r02 used 8), so
    a pocket that touches the outside only through a diagonal pinch is a lake,
    not coast — that is what put a stray 2-site crimson loop on r02."""
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
        nbs = [((i + 1) % NY) * NX + j, ((i - 1) % NY) * NX + j]
        if j + 1 < NX:
            nbs.append(c + 1)
        if j > 0:
            nbs.append(c - 1)
        for nb in nbs:
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


def _ekey(p: Point, q: Point) -> Tuple[int, int, int, int]:
    a = (int(round(p[0])), int(round(p[1])))
    b = (int(round(q[0])), int(round(q[1])))
    return a + b if a <= b else b + a


def seam_hull_edges(sea, out, NY: int, NX: int) -> List[Tuple[Point, Point]]:
    """The hull edges ON the y seam (between row NY-1 and row 0): real coast,
    never drawn (they would lie on the frame), used only for connectivity."""
    segs: List[Tuple[Point, Point]] = []
    for j in range(NX):
        a, b = (NY - 1) * NX + j, j
        if (sea[a] and out[b]) or (out[a] and sea[b]):
            segs.append(((j, NY), (j + 1, NY)))
    return segs


def largest_component(segs: Sequence[Tuple[Point, Point]], NY: int, connectors=()):
    """Keep the edge set's largest vertex-connected component ON THE CYLINDER
    (v taken mod NY; undrawn seam `connectors` join across the seam). Returns
    (kept, n_dropped_edges, n_components). A guard: with the 4-connected
    outside there should be exactly one component."""
    par: Dict[Tuple[int, int], Tuple[int, int]] = {}

    def vk(p: Point) -> Tuple[int, int]:
        return (int(round(p[0])), int(round(p[1])) % NY)

    def find(a):
        par.setdefault(a, a)
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    for p, q in list(segs) + list(connectors):
        ra, rb = find(vk(p)), find(vk(q))
        if ra != rb:
            par[ra] = rb
    comp: Dict[Tuple[int, int], List[Tuple[Point, Point]]] = {}
    for p, q in segs:
        comp.setdefault(find(vk(p)), []).append((p, q))
    best = max(comp.values(), key=len)
    return best, len(segs) - len(best), len(comp)


def seam_crossings(segs: Sequence[Tuple[Point, Point]], seam: Sequence[Tuple[Point, Point]],
                   NY: int, b: int) -> int:
    """How many times the hull (drawn edges + seam edges, on the cylinder)
    crosses the horizontal lattice line v = b."""
    horiz = set()
    up: Dict[int, int] = {}
    dn: Dict[int, int] = {}
    for p, q in list(segs) + list(seam):
        (u0, v0), (u1, v1) = p, q
        v0, v1 = int(round(v0)) % NY, int(round(v1)) % NY
        u0, u1 = int(round(u0)), int(round(u1))
        if v0 == v1:
            if v0 == b % NY:
                horiz.add(min(u0, u1))
        else:  # vertical edge between rows: touches line b at one end
            lo, hi = (v0, v1) if (v1 - v0) % NY == 1 else (v1, v0)
            if hi == b % NY:
                up[u0] = up.get(u0, 0) + 1
            if lo == b % NY:
                dn[u0] = dn.get(u0, 0) + 1
    seen = set()
    n = 0
    for u in sorted(set(up) | set(dn) | horiz | {h + 1 for h in horiz}):
        if u in seen:
            continue
        a = u
        while a - 1 in horiz:
            a -= 1
        z = a
        while z in horiz:
            z += 1
        run = range(a, z + 1)
        seen.update(run)
        n += min(sum(up.get(k, 0) for k in run), sum(dn.get(k, 0) for k in run))
    return n


def droplet_hulls(root, fsz, fsea, NY: int, NX: int, cut: int):
    """The closed dual-lattice HULL of every free FK droplet of >= `cut` sites:
    the edges between a droplet site and the droplet's 4-connected exterior
    (enclosed holes excluded), in lattice units (u = column, v = row from the
    top). Rows are unwrapped across the y seam for the flood, then folded back;
    edges between two droplet sites across the seam do not exist, so a droplet
    cut by the seam stays open at the frame, exactly like the crimson hull."""
    members: Dict[int, List[int]] = {}
    for c in range(NX * NY):
        if not fsea[c]:
            members.setdefault(root[c], []).append(c)
    out: List[Tuple[int, List[Tuple[Point, Point]], List[int]]] = []
    for rt, cells in members.items():
        n = len(cells)
        if n < cut:
            continue
        cset = set(cells)
        # unwrap rows by BFS over the droplet's own 4-neighbour sites
        urow: Dict[int, int] = {cells[0]: cells[0] // NX}
        stack = [cells[0]]
        while stack:
            c = stack.pop()
            i, j = divmod(c, NX)
            ui = urow[c]
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                jj = j + dj
                if jj < 0 or jj >= NX:
                    continue
                nb = ((i + di) % NY) * NX + jj
                if nb in cset and nb not in urow:
                    urow[nb] = ui + di
                    stack.append(nb)
        pts = [(urow[c], c % NX) for c in cells]
        r0 = min(p[0] for p in pts) - 1
        c0 = min(p[1] for p in pts) - 1
        H = max(p[0] for p in pts) - r0 + 2
        W = max(p[1] for p in pts) - c0 + 2
        grid = np.zeros((H, W), np.int8)  # 1 = droplet
        for ui, j in pts:
            grid[ui - r0, j - c0] = 1
        ext = np.zeros((H, W), bool)
        st = [(a, b) for a in range(H) for b in (0, W - 1)] + [
            (a, b) for a in (0, H - 1) for b in range(W)
        ]
        for a, b in st:
            ext[a, b] = True
        while st:
            a, b = st.pop()
            for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                aa, bb = a + da, b + db
                if 0 <= aa < H and 0 <= bb < W and not ext[aa, bb] and not grid[aa, bb]:
                    ext[aa, bb] = True
                    st.append((aa, bb))
        segs: List[Tuple[Point, Point]] = []
        for ui, j in pts:
            a, b = ui - r0, j - c0
            i = ui % NY
            if ext[a, b + 1]:
                segs.append(((j + 1, i), (j + 1, i + 1)))
            if ext[a, b - 1]:
                segs.append(((j, i), (j, i + 1)))
            if ext[a + 1, b]:
                segs.append(((j, i + 1), (j + 1, i + 1)))
            if ext[a - 1, b]:
                segs.append(((j, i), (j + 1, i)))
        out.append((n, segs, cells))
    return out


def onsager_m(K: float) -> float:
    """Spontaneous magnetisation (Onsager 1949, Yang 1952); 0 above Tc."""
    s = math.sinh(2.0 * K)
    return (1.0 - s ** -4) ** 0.125 if s > 1.0 else 0.0


def _closed_offset(ch: List[Point], d: float) -> List[Point]:
    """Offset a polyline; a closed loop gets a proper miter at its seam vertex."""
    if not d:
        return ch
    closed = len(ch) > 3 and math.hypot(ch[0][0] - ch[-1][0], ch[0][1] - ch[-1][1]) < 1e-6
    if not closed:
        return geo.offset(ch, d)
    ext = [ch[-2]] + list(ch) + [ch[1]]
    o = geo.offset(ext, d)[1:-1]
    o[-1] = o[0]
    return o


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def ising_cooling_strip_iterate(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    pitch: float = 1.3,
    t_lo: float = 0.70,
    t_hi: float = 1.80,
    sweeps: int = 40,
    wolff: int = 1500,
    rounds: int = 8,
    cut: int = 30,
    tier_mid: int = 50,
    tier_hi: int = 155,
    pass_gap: float = 0.15,
    screen: int = 3,
    band: float = 11.0,
    title_cap: float = 18.0,
    feed: int = 2000,
) -> List[GCodeCommand]:
    """COOLING STRIP r04 — one lattice, T/Tc 0.70 (left) to 1.80 (right); the
    ordered sea's FK hull runs crimson where the transition happens, and every
    free FK cluster of >= `cut` sites is drawn as its closed hull outline."""
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
    # (unchanged from r02: sampler, lattice, ramp, reservoir coupling, FK draw)
    flat, sim, diag = simulate(rng, NY, NX, t_lo, t_hi, sweeps, wolff, rounds)
    key = (rng.seed * 7919 + 17) & 0xFFFFFFFF
    root, fsz = fk_clusters(flat, sim, key, None)
    # The strip is periodic in y, so WHERE the seam falls is a free display
    # choice (translation invariance is exact; the configuration and its FK
    # draw are untouched). Put the seam where it cuts the fewest drawn hulls:
    # a hull cut by the seam hangs off the frame as open stubs.
    big0 = max(range(len(fsz)), key=lambda r: fsz[r])

    def drawn(r: int) -> bool:
        return r != big0 and fsz[r] >= cut

    def seam_cost(b: int) -> int:
        """Drawn-droplet sites touching the seam between rows b-1 and b."""
        a, c = ((b - 1) % NY) * NX, b * NX
        return sum(drawn(root[a + j]) + drawn(root[c + j]) for j in range(NX))

    fsea, fout = fk_sea_outside(root, fsz, NY, NX)
    h0, s0 = hull_edges(fsea, fout, NY, NX), seam_hull_edges(fsea, fout, NY, NX)
    costs = [seam_cost(b) for b in range(NY)]
    cross = [seam_crossings(h0, s0, NY, b) for b in range(NY)]
    # the crimson coast must cross the seam once (one polyline, top to bottom);
    # among those rows, the seam that touches the fewest drawn droplets
    roll = min(range(NY), key=lambda b: (cross[b], costs[b], b))
    root = [root[((c // NX + roll) % NY) * NX + c % NX] for c in range(NX * NY)]
    fsea, fout = fk_sea_outside(root, fsz, NY, NX)
    shore_all = hull_edges(fsea, fout, NY, NX)
    shore, shore_dropped, shore_comps = largest_component(
        shore_all, NY, seam_hull_edges(fsea, fout, NY, NX)
    )
    red_keys = {_ekey(p, q) for p, q in shore}

    # every free droplet >= cut: its closed hull, weighted by its size. An edge
    # shared by two drawn droplets carries the heavier rung (never under-inked);
    # an edge that is also frontier is drawn crimson only (the cut never
    # deletes coast).
    def rung(n: int) -> int:
        return 1 if n < tier_mid else (2 if n < tier_hi else 3)

    hulls = droplet_hulls(root, fsz, fsea, NY, NX, cut)
    edges: Dict[Tuple[int, int, int, int], Tuple[Tuple[Point, Point], int]] = {}
    per_rung = {1: 0, 2: 0, 3: 0}
    shared_red = 0
    for n, segs, _cells in hulls:
        r = rung(n)
        per_rung[r] += 1
        for p, q in segs:
            k = _ekey(p, q)
            if k in red_keys:
                shared_red += 1
                continue
            if k not in edges or edges[k][1] < r:
                edges[k] = ((p, q), r)
    buckets: Dict[int, List[Tuple[Point, Point]]] = {1: [], 2: [], 3: []}
    for seg, r in edges.values():
        buckets[r].append(seg)

    # the sea as a line-screen: every `screen`-th row, runs of held-droplet
    # cells. r04: the rule of row i lies ON the lattice line under that row
    # (v = i + 1), not through the cell centres — so every horizontal hull
    # edge is either ON a rule or a full pitch (1.3 mm) from it, never the
    # 0.65 mm r02 left between a rule and a coast step. Where a drawn hull
    # edge already inks that line, the rule yields to it (same line, no
    # overdraw): the row's ruled coverage is still exactly its held cells.
    inked = red_keys | set(edges)
    screen_runs: List[Tuple[int, int, int]] = []  # (row, j0, j1 exclusive)
    yielded = 0
    for i in range(screen // 2, NY, screen):
        j = 0
        while j < NX:
            ok = fsea[i * NX + j] and _ekey((j, i + 1), (j + 1, i + 1)) not in inked
            if fsea[i * NX + j] and not ok:
                yielded += 1
            if ok:
                k = j
                while (
                    k + 1 < NX
                    and fsea[i * NX + k + 1]
                    and _ekey((k + 1, i + 1), (k + 2, i + 1)) not in inked
                ):
                    k += 1
                screen_runs.append((i, j, k + 1))
                j = k + 1
            else:
                j += 1
    sx = [0.5 * (p[0] + q[0]) for p, q in shore if p[0] == q[0]]  # vertical hull edges
    x_mean = sum(sx) / max(1, len(sx))
    x_std = math.sqrt(sum((v - x_mean) ** 2 for v in sx) / max(1, len(sx)))
    # S3: the sea's density IS the order parameter. Held fraction over the
    # columns with T/Tc in [0.70, 0.80) vs the Onsager-Yang m(T) there.
    cols = [j for j in range(NX) if sim.tr_at(j + 0.5) < 0.80]
    held_all = sum(fsea[i * NX + j] for i in range(NY) for j in cols) / float(NY * len(cols))
    rrows = list(range(screen // 2, NY, screen))
    held = sum(fsea[i * NX + j] for i in rrows for j in cols) / float(len(rrows) * len(cols))
    m_ex = sum(onsager_m(sim.Kv[j]) for j in cols) / len(cols)
    sizes_free = sorted((n for n, _, _ in hulls), reverse=True)
    stats = {
        "NX": NX,
        "NY": NY,
        "seam_roll_rows": roll,
        "seam_cost": costs[roll],
        "seam_cost_unrolled": costs[0],
        "seam_crossings": cross[roll],
        "rule_cells_yielded_to_hull": yielded,
        "seam_crossings_unrolled": cross[0],
        "sea_frac": sum(fsea) / float(NX * NY),
        "shore_edges": len(shore),
        "shore_dropped_edges": shore_dropped,
        "shore_components_before": shore_comps,
        "shore_T": sim.tr_at(x_mean),
        "shore_T_std": (t_hi - t_lo) * x_std / NX,
        "shore_T_min": sim.tr_at(min(sx)) if sx else 0.0,
        "shore_T_max": sim.tr_at(max(sx)) if sx else 0.0,
        "shore_x_mm": fx0 + x_mean * pitch,
        "energy_rms_band": diag["rms"],
        "energy_rms_col": diag["rms_col"],
        "wolff_frozen": diag["wolff_frozen"],
        "droplets_per_rung": per_rung,
        "edges_per_rung": {k: len(v) for k, v in buckets.items()},
        "edges_given_to_red": shared_red,
        "drawn_droplet_sizes": sizes_free[:10],
        "held_frac_070_080_rule_rows": held,
        "held_frac_070_080_all_rows": held_all,
        "onsager_m_070_080": m_ex,
    }

    # ---------------------------------------------------------------- type
    # One stroke mono everywhere. Horizontal type sits in the gaps of the
    # sea's ruling (pitch R = screen * pitch); the title runs UP the sea,
    # cap line on the left axis.
    R = screen * pitch
    rule_rows = list(range(screen // 2, NY, screen))

    def rule_y(k: int) -> float:
        return fy1 - (rule_rows[k] + 1.0) * pitch

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

    tx = 15.0 if x0 < 15.0 else x0 + 5.0  # the one left axis
    clear = 4.0  # type never comes nearer the shore than this

    def in_gap(k: int, h: float) -> float:
        """Baseline for type of height h centred in the gap under rule k."""
        return rule_y(k + 1) + (R - h) / 2.0

    lines: List[Tuple[str, float]] = [
        ("TC IS A PLACE", 2.2),
        (f"2D ISING   {NX} X {NY}   SEED {rng.seed}", 1.8),
        (f"T OVER TC  {t_lo:.2f} TO {t_hi:.2f}  ALONG X", 1.8),
        ("LEFT EDGE HELD UP   TOP WRAPS", 1.8),
        ("RULED   THE HELD FK CLUSTER", 1.8),
        (f"UNDER 0.80 TC  {held:.3f}  ONSAGER M {m_ex:.3f}", 1.8),
        (f"RED   ITS HULL   MEAN {stats['shore_T']:.2f} TC", 1.8),
        ("FREE FK CLUSTERS   1  2  3 PASSES", 1.8),
        (f"SITES  {cut} TO {tier_mid - 1}  {tier_mid} TO {tier_hi - 1}  {tier_hi} UP", 1.8),
        (f"SINGLE SPINS NOT DRAWN  NOR UNDER {cut}", 1.8),
    ]
    last = len(rule_rows) - 2  # the lowest full gap
    first = last - len(lines) + 1
    labels = []
    min_h = 9.9
    for n, (ln, h) in enumerate(lines):
        yb = in_gap(first + n, h)
        room = reach(yb - 0.5, yb + h + 0.5) - clear - tx
        h = min(h, room / (_text_width(ln, 1.0) + 1e-9))
        min_h = min(min_h, h)
        labels.append((ln, tx, in_gap(first + n, h), h, black))
    stats["key_min_h"] = min_h
    sc.halo_labels(labels, pad_x=1.2, pad_y=(0.25, 1.25))

    # title: CRITICAL runs up the ordered sea (reading bottom to top), cap line
    # flush on the left axis, from just above the key to the top of the field.
    t_weight = 0.6
    t_h = title_cap
    t_len = giant_type_width("CRITICAL", t_h) - (5.6 - 4.0) * t_h / 6.0
    t_y0 = rule_y(first - 1) + 2.5
    t_y1 = fy1 - 1.5
    if t_y0 + t_len > t_y1:  # shrink only if the sea is too short
        t_h = t_h * (t_y1 - t_y0) / t_len
        t_len = t_y1 - t_y0
    t_x = tx + t_h + t_weight / 2.0  # anchor = baseline; cap line lands on tx
    stats["title_h"] = t_h
    stats["title_len"] = t_len
    # the title's slot in the ruling: rules are removed from the cold wall to
    # 1.6 mm right of the baseline, so no stub is left between wall and C.
    slot = (fx0 - 1.0, t_y0 - 1.6, t_x + t_weight / 2.0 + 1.6, t_y0 + t_len + 1.6)
    sc._boxes.append(slot)

    # ---------------------------------------------------------- the marks
    queue: List[Tuple[List[Point], Optional[int], bool]] = []

    def draw(segs, passes, pen, halos=True):
        for ch in _chain_segments([(page(*p), page(*q)) for p, q in segs], tol=1e-3):
            if len(ch) < 2:
                continue
            for k in range(passes):
                off = (k - (passes - 1) / 2.0) * pass_gap
                queue.append((_closed_offset(ch, off), pen, halos))

    stubs = 0
    for i, j0, j1 in screen_runs:  # the ordered sea: one straight rule per run
        (ax, ay), (bx, _by) = page(j0, i + 1.0), page(j1, i + 1.0)
        if slot[1] <= ay <= slot[3]:
            ax = max(ax, slot[2])
            if bx - ax < 4.0:  # never leave a crumb beside the title
                stubs += 1
                continue
        queue.append(([(ax, ay), (bx, ay)], black, True))
    stats["title_stubs_dropped"] = stubs
    for r in (1, 2, 3):
        draw(buckets[r], r, black)
    draw(shore, 3, red, halos=False)  # nothing is allowed to cut the shore

    for pts, pen, halos in queue:
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
    sc.emit(
        giant_type(
            "CRITICAL", t_x, t_y0, t_h, pen=black, weight=t_weight, tip=0.3, angle=90.0, f=feed
        )
    )

    out_cmds = sc.render()
    logging.getLogger(__name__).info("r04 stats %s", stats)
    ising_cooling_strip_iterate.stats = stats  # type: ignore[attr-defined]
    ising_cooling_strip_iterate.diag = diag  # type: ignore[attr-defined]
    return out_cmds
