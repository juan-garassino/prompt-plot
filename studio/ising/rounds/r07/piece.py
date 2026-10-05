"""CRITICAL — COOLING STRIP (r07 iterate, parent r05). The Ising transition as a PLACE.

One lattice, 212 x 129, whose temperature ramps linearly across the sheet,
T/Tc = 0.70 at the left edge to 2.30 at the right. Local equilibrium in a
gradient is an ordinary Boltzmann ensemble with position-dependent couplings,
P(s) ~ exp(sum K_ij s_i s_j), K_ij = J / T(x_ij), sampled exactly by
checkerboard Metropolis + Wolff (P_add = 1 - exp(-2 K_ij)). Top and bottom wrap,
the LEFT edge is held up by a fixed reservoir column (the cold wall), the right
edge is free. The drawn objects are the Fortuin-Kasteleyn (Coniglio-Klein)
droplets of the last sampled state (one seeded Swendsen-Wang bond draw). The
droplet bonded to the held-up wall is the ordered sea: its density IS the
magnetisation M (P(x connected to the + wall) = <s_x>_+ in the FK
representation), and its hull is pinned to Tc (gradient percolation).

r07 — r05's sheet (coast, ruled sea, rungs 13/30/50/155 grown inward at
0.35 mm, CRITICAL spine, exact thermometer, pens black / crimson / grey), with
the Schotter dissolve given its ENDING by physics:
  * the ramp's hot end runs to T_max = 2.30 Tc at the same fixed cut 13: the
    smallest T_max whose last 25 mm column holds <= 3 outlines and a >= 60 mm
    mark-free run on seeds 7, 3 and 13 (census.py). The sea + coast stays
    49-61 mm wide, so the cut never had to move. The expected outline count
    per 20 mm column falls strictly to the edge (ensemble_r07.py, 40 chains);
    one configuration is Poisson about it;
  * the field is 129 rows (was 137) at r05's pitch: the footer gets its air
    from the field, never from smaller type;
  * every black and grey stroke is cut back >= 0.85 mm short of the outermost
    crimson pass (the coast itself never moves); rules run serpentine;
  * no knots: an inner pass on a 1-site neck, or any inner-pass segment that
    runs within 0.34 mm of other ink, is dropped;
  * the colophon unpacks FK and says where weight and count peak, measured on
    the outlines actually drawn.

Entry point: ``ising_cooling_strip_r07``.
"""

from __future__ import annotations

import logging
import math
import random as _random
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine import geometry as geo
from promptplot.generative.engine.kit import (
    _GLYPHS,
    _offset_polyline,
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
BLACK, RED, GREY = 0, 1, 2


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
# r05: traced hull loops that know their inside, and inward weight passes
# ---------------------------------------------------------------------------
EKey = Tuple[str, int, int]


def seg_key(p: Point, q: Point, NY: int) -> EKey:
    """Canonical key of a unit dual-lattice edge on the cylinder:
    ('v', x, y) spans x, [y, y+1]; ('h', x, y) spans [x, x+1], y; y mod NY."""
    x0, y0 = int(round(p[0])), int(round(p[1]))
    x1, y1 = int(round(q[0])), int(round(q[1]))
    if x0 == x1:
        return ("v", x0, min(y0, y1) % NY)
    return ("h", min(x0, x1), y0 % NY)


def _trace_loops(edges):
    """edges: (start, end, n, cell) with the cluster on the n side. Returns the
    closed walks. At a diagonal pinch the walk turns TOWARD the interior, so the
    two cells meeting at a corner get separate loops and the inward offset of
    the corner stays inside its own cell."""
    outm: Dict[Point, List[int]] = {}
    for k, (s, _e, _n, _c) in enumerate(edges):
        outm.setdefault(s, []).append(k)
    used = [False] * len(edges)
    loops = []
    for k0 in range(len(edges)):
        if used[k0]:
            continue
        loop, k = [], k0
        while True:
            used[k] = True
            loop.append(edges[k])
            _s, e, n, _c = edges[k]
            alln = outm.get(e, [])
            pref = None
            if len(alln) == 1:
                pref = alln[0]
            else:
                for m in alln:
                    sm, em = edges[m][0], edges[m][1]
                    if (em[0] - sm[0], em[1] - sm[1]) == n:
                        pref = m
            if pref == k0:
                break  # closed
            if pref is None or used[pref]:
                rest = [m for m in alln if not used[m]]
                if not rest:
                    break
                pref = rest[0]
            k = pref
        loops.append(loop)
    return loops


def droplet_loops(root, fsea, NY: int, NX: int, cut: int):
    """Every free FK droplet of >= `cut` sites as traced hull loops in UNWRAPPED
    lattice coords (x = column, y = row from the top, may leave [0, NY) where a
    droplet straddles the seam). Hull = edges between the droplet and its
    4-connected exterior; enclosed holes are excluded (same set as r04)."""
    members: Dict[int, List[int]] = {}
    for c in range(NX * NY):
        if not fsea[c]:
            members.setdefault(root[c], []).append(c)
    out = []
    for rt, cells in members.items():
        n = len(cells)
        if n < cut:
            continue
        cset = set(cells)
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
        grid = np.zeros((H, W), np.int8)
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
        edges = []
        for ui, j in pts:
            a, b = ui - r0, j - c0
            if ext[a, b + 1]:
                edges.append(((j + 1, ui + 1), (j + 1, ui), (-1, 0), (ui, j)))
            if ext[a, b - 1]:
                edges.append(((j, ui), (j, ui + 1), (1, 0), (ui, j)))
            if ext[a + 1, b]:
                edges.append(((j, ui + 1), (j + 1, ui + 1), (0, -1), (ui, j)))
            if ext[a - 1, b]:
                edges.append(((j + 1, ui), (j, ui), (0, 1), (ui, j)))
        xs = [p[1] + 0.5 for p in pts]
        out.append({
            "size": n,
            "root": rt,
            "loops": _trace_loops(edges),
            "cx": sum(xs) / n,
            "w": max(p[1] for p in pts) - min(p[1] for p in pts) + 1,
            "h": max(p[0] for p in pts) - min(p[0] for p in pts) + 1,
        })
    return out


def _far_key(n, cell, NY: int) -> EKey:
    """The lattice line on the far side of the edge's own cell (one site in)."""
    ui, j = cell
    if n == (-1, 0):
        return ("v", j, ui % NY)
    if n == (1, 0):
        return ("v", j + 1, ui % NY)
    if n == (0, -1):
        return ("h", j, ui % NY)
    return ("h", j, (ui + 1) % NY)


def _offset_loop(loop, t: float, page, closed: bool) -> List[Point]:
    """Exact rectilinear miter offset of a traced loop by t mm toward the
    interior. Vertex k sits between edge k-1 and edge k; the page flips y."""
    m = len(loop)
    pts = []
    for k in range(m + (0 if closed else 1)):
        if k < m:
            V = page(*loop[k][0])
            na = loop[k - 1][2] if (closed or k > 0) else loop[k][2]
            nb = loop[k][2]
        else:
            V = page(*loop[m - 1][1])
            na = nb = loop[m - 1][2]
        ax, ay = na[0], -na[1]
        bx, by = nb[0], -nb[1]
        if na == nb:
            pts.append((V[0] + t * ax, V[1] + t * ay))
        else:
            pts.append((V[0] + t * (ax + bx), V[1] + t * (ay + by)))
    if closed:
        pts.append(pts[0])
    return pts


def _runs(pts: List[Point], keep: List[bool], closed: bool) -> List[List[Point]]:
    """Split an offset loop (segment k = pts[k] -> pts[k+1]) into runs of kept
    segments; a fully kept closed loop stays one closed polyline."""
    m = len(keep)
    if all(keep):
        return [pts]
    if closed:
        s = next(k for k in range(m) if not keep[k])
        order = [(s + 1 + k) % m for k in range(m)]
    else:
        order = list(range(m))
    runs, cur = [], []
    for k in order:
        if keep[k]:
            if not cur:
                cur = [pts[k]]
            cur.append(pts[k + 1])
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def _clip_y(pts: List[Point], ylo: float, yhi: float) -> List[List[Point]]:
    runs, cur = [], []
    eps = 1e-6
    for a, b in zip(pts, pts[1:]):
        (ax, ay), (bx, by) = a, b
        t0, t1 = 0.0, 1.0
        dy = by - ay
        if abs(dy) < 1e-12:
            if ay < ylo - eps or ay > yhi + eps:
                t0, t1 = 1.0, 0.0
        else:
            ta, tb = (ylo - ay) / dy, (yhi - ay) / dy
            t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
        if t1 < t0 + 1e-9:
            if cur:
                runs.append(cur)
                cur = []
            continue
        pa = (ax + (bx - ax) * t0, ay + dy * t0)
        pb = (ax + (bx - ax) * t1, ay + dy * t1)
        if cur and abs(cur[-1][0] - pa[0]) < 1e-6 and abs(cur[-1][1] - pa[1]) < 1e-6:
            cur.append(pb)
        else:
            if cur:
                runs.append(cur)
            cur = [pa, pb]
    if cur:
        runs.append(cur)
    return runs


def _simplify(pts: List[Point]) -> List[Point]:
    """Drop collinear interior vertices (all strokes here are axis-parallel)."""
    if len(pts) < 3:
        return pts
    out = [pts[0]]
    for k in range(1, len(pts) - 1):
        a, b, c = out[-1], pts[k], pts[k + 1]
        if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) > 1e-9:
            out.append(b)
    out.append(pts[-1])
    return out


def _title_glyph(ch: str, x: float, y: float, height: float, pen, weight: float,
                 tip: float, angle: float, f: int) -> List[GCodeCommand]:
    """giant_type for one glyph, except that a stroke is split at any vertex
    turning by more than 120 deg before its weight passes are offset. The
    kit's averaged-normal offset collapses at a sharp apex, which is why r05's
    `A` diagonals thinned to a hairline (A21). Every other glyph is identical."""
    sc_ = height / 6.0
    passes = max(1, int(round(weight / max(tip, 0.05))) + 1) if weight > 0 else 1
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))

    def place(gx: float, gy: float) -> Point:
        lx, ly = gx * sc_, gy * sc_
        return (x + lx * ca - ly * sa, y + lx * sa + ly * ca)

    out: List[GCodeCommand] = []
    for stroke in _GLYPHS.get(ch, []):
        pts = [place(gx, gy) for gx, gy in stroke]
        parts, cur = [], [pts[0]]
        for k in range(1, len(pts)):
            cur.append(pts[k])
            if k < len(pts) - 1:
                ux, uy = pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]
                vx, vy = pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]
                c = (ux * vx + uy * vy) / max(1e-12, math.hypot(ux, uy) * math.hypot(vx, vy))
                if c < math.cos(math.radians(120.0)):
                    parts.append(cur)
                    cur = [pts[k]]
        parts.append(cur)
        for part in parts:
            for k in range(passes):
                d = -weight / 2.0 + weight * k / (passes - 1) if passes > 1 else 0.0
                out += _poly(_offset_polyline(part, d) if d else part, color=pen, f=f)
    return out


# ---------------------------------------------------------------------------
# r07: the coast is where everything stops
# ---------------------------------------------------------------------------
class _RectIndex:
    """Axis-aligned keep-out rectangles with a coarse grid hash."""

    def __init__(self, rects: List[Tuple[float, float, float, float]], cell: float = 4.0):
        self.rects, self.cell = rects, cell
        self.grid: Dict[Tuple[int, int], List[int]] = {}
        for k, (xa, ya, xb, yb) in enumerate(rects):
            for gx in range(int(math.floor(xa / cell)), int(math.floor(xb / cell)) + 1):
                for gy in range(int(math.floor(ya / cell)), int(math.floor(yb / cell)) + 1):
                    self.grid.setdefault((gx, gy), []).append(k)

    def near(self, xa: float, ya: float, xb: float, yb: float) -> set:
        c = self.cell
        out: set = set()
        for gx in range(int(math.floor(xa / c)), int(math.floor(xb / c)) + 1):
            for gy in range(int(math.floor(ya / c)), int(math.floor(yb / c)) + 1):
                out.update(self.grid.get((gx, gy), ()))
        return out


def _plen(pts: List[Point]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _cut_away(pts: List[Point], idx: _RectIndex, min_len: float) -> List[List[Point]]:
    """Remove from an axis-parallel polyline every part strictly inside a
    keep-out rectangle (exact interval subtraction; a closed loop whose first
    and last surviving pieces meet is re-joined). Pieces shorter than
    `min_len` are dropped rather than left as dots."""
    eps = 1e-7
    pieces: List[List[Point]] = []
    cur: List[Point] = []

    def push(P0: Point, P1: Point) -> None:
        nonlocal cur
        if cur and abs(cur[-1][0] - P0[0]) < 1e-6 and abs(cur[-1][1] - P0[1]) < 1e-6:
            cur.append(P1)
        else:
            if cur:
                pieces.append(cur)
            cur = [P0, P1]

    for a, b in zip(pts, pts[1:]):
        hor = abs(a[1] - b[1]) < 1e-9
        ver = abs(a[0] - b[0]) < 1e-9
        if not (hor or ver):  # never happens here; keep it untouched
            push(a, b)
            continue
        c = a[1] if hor else a[0]
        s0, s1 = (a[0], b[0]) if hor else (a[1], b[1])
        lo, hi = min(s0, s1), max(s0, s1)
        rem = []
        for k in idx.near(min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])):
            xa, ya, xb, yb = idx.rects[k]
            if hor and ya + eps < c < yb - eps:
                rem.append((xa, xb))
            elif ver and xa + eps < c < xb - eps:
                rem.append((ya, yb))
        keep = [(lo, hi)]
        for r0, r1 in rem:
            nxt = []
            for k0, k1 in keep:
                if r1 <= k0 or r0 >= k1:
                    nxt.append((k0, k1))
                    continue
                if r0 > k0:
                    nxt.append((k0, r0))
                if r1 < k1:
                    nxt.append((r1, k1))
            keep = nxt
        keep = [(k0, k1) for k0, k1 in keep if k1 - k0 > 1e-6]
        fwd = s1 >= s0
        for k0, k1 in sorted(keep, reverse=not fwd):
            u0, u1 = (k0, k1) if fwd else (k1, k0)
            push((u0, c) if hor else (c, u0), (u1, c) if hor else (c, u1))
    if cur:
        pieces.append(cur)
    if (len(pieces) > 1 and abs(pieces[-1][-1][0] - pieces[0][0][0]) < 1e-6
            and abs(pieces[-1][-1][1] - pieces[0][0][1]) < 1e-6):
        pieces[0] = pieces[-1] + pieces[0][1:]
        pieces.pop()
    return [_simplify(pc) for pc in pieces if _plen(pc) >= min_len]


def _unknot(strokes, min_gap: float, min_ov: float = 0.05):
    """Drop every inner-pass SEGMENT that runs parallel within `min_gap` of any
    other inked segment (over > `min_ov` mm): the heavier pass yields, equal
    passes both yield. This is what a 1-site neck or a concave-corner miter
    turns into a knot. Returns (strokes, n_segments_dropped)."""
    segs = []  # (stroke k, seg j, pass, a, b)
    for k, (_c, p, pts) in enumerate(strokes):
        for j, (a, b) in enumerate(zip(pts, pts[1:])):
            segs.append((k, j, p, a, b))
    cell = 2.0
    grid: Dict[Tuple[int, int], List[int]] = {}
    for n, (_k, _j, _p, a, b) in enumerate(segs):
        for gx in range(int(min(a[0], b[0]) // cell), int(max(a[0], b[0]) // cell) + 1):
            for gy in range(int(min(a[1], b[1]) // cell), int(max(a[1], b[1]) // cell) + 1):
                grid.setdefault((gx, gy), []).append(n)
    drop = set()
    for n, (k, j, p, a, b) in enumerate(segs):
        if p == 0:
            continue
        hor = abs(a[1] - b[1]) < 1e-9
        near = set()
        for gx in range(int((min(a[0], b[0]) - min_gap) // cell),
                        int((max(a[0], b[0]) + min_gap) // cell) + 1):
            for gy in range(int((min(a[1], b[1]) - min_gap) // cell),
                            int((max(a[1], b[1]) + min_gap) // cell) + 1):
                near.update(grid.get((gx, gy), ()))
        for m in near:
            if m == n:
                continue
            k2, j2, p2, c, d = segs[m]
            if p2 > p:
                continue  # that one yields instead
            if hor and abs(c[1] - d[1]) < 1e-9:
                gap = abs(a[1] - c[1])
                ov = min(max(a[0], b[0]), max(c[0], d[0])) - max(min(a[0], b[0]), min(c[0], d[0]))
            elif not hor and abs(c[0] - d[0]) < 1e-9:
                gap = abs(a[0] - c[0])
                ov = min(max(a[1], b[1]), max(c[1], d[1])) - max(min(a[1], b[1]), min(c[1], d[1]))
            else:
                continue
            if 1e-6 < gap < min_gap and ov > min_ov:
                drop.add((k, j))
                break
    out = []
    for k, (c, p, pts) in enumerate(strokes):
        cur = []
        for j, (a, b) in enumerate(zip(pts, pts[1:])):
            if (k, j) in drop:
                if len(cur) >= 2:
                    out.append((c, p, cur))
                cur = []
                continue
            if not cur:
                cur = [a]
            cur.append(b)
        if len(cur) >= 2:
            out.append((c, p, cur))
    return out, len(drop)


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def ising_cooling_strip_r07(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    nx: int = 212,
    ny: int = 129,
    t_lo: float = 0.70,
    t_hi: float = 2.30,
    sweeps: int = 40,
    wolff: int = 1500,
    rounds: int = 8,
    cut: int = 13,
    seam_cut: int = 30,
    tier_lo: int = 30,
    tier_mid: int = 50,
    tier_hi: int = 155,
    pass_gap: float = 0.35,
    coast_gap: float = 0.15,
    coast_clear: float = 0.85,
    screen: int = 3,
    band: float = 11.6,
    title_cap: float = 18.0,
    title_gap: float = 3.2,
    type_h: float = 1.8,
    line_pitch: float = 4.0,
    foot_lift: float = 3.2,
    foot_air: float = 5.0,
    place_cap: float = 5.2,
    hot_tick: float = 1.60,
    loop_start: str = "low",
    feed: int = 2000,
) -> List[GCodeCommand]:
    """COOLING STRIP r07 — r05's lattice, rungs, coast and spine; the ramp's hot
    end extended to where heat is finer than the fixed cut, so the right edge
    is bare paper by physics. Every black/grey stroke stops >= `coast_clear`
    short of the crimson coast; the field is shorter so the footer breathes."""
    x0, y0, x1, y1 = bounds
    black, red = _pen(BLACK, colors), _pen(RED, colors)
    grey = _pen(GREY, colors) if colors > 2 else black  # hairline rung pen
    sc = Scene3D(rng, bounds, feed=feed, tip=0.5, fit="none")
    NX, NY = nx, ny

    # ------------------------------------------------------------- layout
    # one left axis tx: CRITICAL's cap line and the colophon. The type strip is
    # a 5-line grid `line_pitch` apart whose last baseline sits `foot_lift`
    # above the bottom margin; the field keeps >= `foot_air` of bare paper above
    # the first cap line. NY (rows) is what shortens the field; the display
    # pitch stays r05's (set by the width).
    tx = 15.0 if x0 < 15.0 else x0 + 5.0
    t_weight = 0.6
    edge = 0.4
    fx0 = tx + title_cap + t_weight + title_gap
    fx1 = x1 - edge
    fy1 = y1 - band
    base = y0 + foot_lift
    strip_top = base + 4 * line_pitch + type_h + foot_air
    pitch = min((fx1 - fx0) / NX, (fy1 - strip_top) / NY)
    fx1 = fx0 + NX * pitch
    fy0 = fy1 - NY * pitch

    def page(u: float, v: float) -> Point:
        return (fx0 + u * pitch, fy1 - v * pitch)

    def x_of(tr: float) -> float:
        return fx0 + (tr - t_lo) / (t_hi - t_lo) * NX * pitch

    # ------------------------------------------------------------- physics
    flat, sim, diag = simulate(rng, NY, NX, t_lo, t_hi, sweeps, wolff, rounds)
    key = (rng.seed * 7919 + 17) & 0xFFFFFFFF
    root, fsz = fk_clusters(flat, sim, key, None)
    big0 = max(range(len(fsz)), key=lambda r: fsz[r])

    def drawn_r04(r: int) -> bool:  # the seam rule stays r04's
        return r != big0 and fsz[r] >= seam_cut

    def seam_cost(b: int) -> int:
        a, c = ((b - 1) % NY) * NX, b * NX
        return sum(drawn_r04(root[a + j]) + drawn_r04(root[c + j]) for j in range(NX))

    fsea, fout = fk_sea_outside(root, fsz, NY, NX)
    h0, s0 = hull_edges(fsea, fout, NY, NX), seam_hull_edges(fsea, fout, NY, NX)
    costs = [seam_cost(b) for b in range(NY)]
    cross = [seam_crossings(h0, s0, NY, b) for b in range(NY)]
    roll = min(range(NY), key=lambda b: (cross[b], costs[b], b))
    root = [root[((c // NX + roll) % NY) * NX + c % NX] for c in range(NX * NY)]
    fsea, fout = fk_sea_outside(root, fsz, NY, NX)
    shore_all = hull_edges(fsea, fout, NY, NX)
    shore, shore_dropped, shore_comps = largest_component(
        shore_all, NY, seam_hull_edges(fsea, fout, NY, NX)
    )
    red_keys = {seg_key(p, q, NY) for p, q in shore}

    # ------------------------------------------------ free droplets, by rung
    def rung(n: int) -> int:
        if n < tier_lo:
            return 0
        return 1 if n < tier_mid else (2 if n < tier_hi else 3)

    clusters = droplet_loops(root, fsea, NY, NX, cut)
    owners: Dict[EKey, Tuple[int, int, int]] = {}
    cl_keys: List[set] = []
    for idx, cl in enumerate(clusters):
        r, n = rung(cl["size"]), cl["size"]
        ks = set()
        for loop in cl["loops"]:
            for s, e, _n, _c in loop:
                k = seg_key(s, e, NY)
                ks.add(k)
                if k not in owners or (r, n) > owners[k][:2]:
                    owners[k] = (r, n, idx)
        cl_keys.append(ks)
    inked = red_keys | set(owners)

    # the sea as a line-screen, every `screen`-th row, ON the lattice line under
    # the row, yielding where a drawn hull/coast already inks that line
    screen_runs: List[Tuple[int, int, int]] = []
    rule_keys = set()
    yielded = 0
    for i in range(screen // 2, NY, screen):
        j = 0
        while j < NX:
            held = fsea[i * NX + j]
            free_line = ("h", j, (i + 1) % NY) not in inked
            if held and not free_line:
                yielded += 1
            if held and free_line:
                k = j
                while (
                    k + 1 < NX
                    and fsea[i * NX + k + 1]
                    and ("h", k + 1, (i + 1) % NY) not in inked
                ):
                    k += 1
                screen_runs.append((i, j, k + 1))
                for jj in range(j, k + 1):
                    rule_keys.add(("h", jj, (i + 1) % NY))
                j = k + 1
            else:
                j += 1

    # hull passes (r05), plus r07's neck rule: on an edge whose own cell is the
    # whole width of the droplet (the far line is this droplet's hull too),
    # pass p survives only if both sides' passes keep >= pass_gap between them,
    # 2 p gap + gap <= pitch; and an inner-pass segment that the miter turns
    # backwards or shrinks under 0.4 mm is dropped (no knots).
    strokes: List[Tuple[int, int, List[Point]]] = []  # (cluster idx, pass, pts)
    stroke_pen: List[Optional[int]] = []
    thinned = 0
    corner_cut = 0
    neck_cut = 0
    clear = 0.8

    def _lat_page(u: float, v: float) -> Point:
        return (u, -v)

    def _crowds(a: Point, b: Point, idx: int) -> bool:
        (ax, ay), (bx, by) = a, b
        if abs(ay - by) < 1e-9:
            kind, c, lo, hi = "h", -ay, min(ax, bx), max(ax, bx)
        else:
            kind, c, lo, hi = "v", ax, min(-ay, -by), max(-ay, -by)
        for L in {math.floor(c), math.ceil(c)}:
            d = abs(c - L) * pitch
            if d < 1e-6 or d >= clear + coast_gap:
                continue
            for j in range(math.floor(lo) - 1, math.ceil(hi) + 1):
                if min(hi, j + 1) - max(lo, j) <= 0.3 / pitch:
                    continue
                k = (kind, j, L % NY) if kind == "h" else (kind, L, j % NY)
                if k in red_keys:
                    if d < clear + coast_gap:
                        return True
                elif d < clear and (k in rule_keys or (k in owners and owners[k][2] != idx)):
                    return True
        return False

    neck_max = max(0, int(math.floor((pitch - pass_gap) / (2.0 * pass_gap) + 1e-9)))
    for idx, cl in enumerate(clusters):
        r = rung(cl["size"])
        for loop in cl["loops"]:
            closed = loop[0][0] == loop[-1][1]
            keys = [seg_key(s, e, NY) for s, e, _n, _c in loop]
            own = [(k not in red_keys) and owners[k][2] == idx for k in keys]
            inner, narrow = [], []
            for (s, e, n, c), k, o in zip(loop, keys, own):
                fk = _far_key(n, c, NY)
                ok = o and fk not in red_keys and fk not in rule_keys and (
                    fk not in owners or owners[fk][2] == idx
                )
                if o and r > 1 and not ok:
                    thinned += 1
                inner.append(ok)
                narrow.append(fk in cl_keys[idx])
            for p in range(max(r, 1)):
                keep = own if p == 0 else list(inner)
                if p > 0:
                    if p > neck_max:
                        for k in range(len(keep)):
                            if keep[k] and narrow[k]:
                                keep[k] = False
                                neck_cut += 1
                    if not any(keep):
                        continue
                    lat = _offset_loop(loop, p * pass_gap / pitch, _lat_page, closed)
                    for k in range(len(keep)):
                        if not keep[k]:
                            continue
                        (sx, sy), (ex, ey) = _lat_page(*loop[k][0]), _lat_page(*loop[k][1])
                        (ax, ay), (bx, by) = lat[k], lat[k + 1]
                        if ((bx - ax) * (ex - sx) + (by - ay) * (ey - sy) <= 0
                                or math.hypot(bx - ax, by - ay) * pitch < 0.4):
                            keep[k] = False
                            neck_cut += 1
                        elif _crowds(lat[k], lat[k + 1], idx):
                            keep[k] = False
                            corner_cut += 1
                    if not any(keep):
                        continue
                pts = _offset_loop(loop, p * pass_gap, page, closed)
                for run in _runs(pts, keep, closed):
                    for shift in (0.0, NY * pitch, -NY * pitch):
                        moved = [(x, y + shift) for x, y in run]
                        for piece in _clip_y(moved, fy0, fy1):
                            if len(piece) >= 2:
                                strokes.append((idx, p, _simplify(piece)))
                                stroke_pen.append(grey if r == 0 else black)

    # no knots: an inner pass never runs closer than pass_gap to other ink
    tagged = [(c, p, pts, pn) for (c, p, pts), pn in zip(strokes, stroke_pen)]
    un, knot_cut = _unknot([(c, p, pts) for c, p, pts, _pn in tagged], pass_gap - 0.01)
    pen_of_cluster = {c: pn for c, _p, _pts, pn in tagged}
    strokes = [(c, p, [tuple(v) for v in pts]) for c, p, pts in un]
    stroke_pen = [pen_of_cluster[c] for c, _p, _pts in strokes]

    # ---------------------------------------- the coast is where it stops
    # keep-out: every crimson unit edge grown by (coast_gap + coast_clear) on
    # all sides; black and grey strokes are cut back to its boundary, so each
    # ends >= coast_clear short of the outermost crimson pass. The coast
    # itself is never moved.
    ko = coast_gap + coast_clear
    shore_mm = [(page(*p), page(*q)) for p, q in shore]
    rects = [
        (min(a[0], b[0]) - ko, min(a[1], b[1]) - ko, max(a[0], b[0]) + ko, max(a[1], b[1]) + ko)
        for a, b in shore_mm
    ]
    kidx = _RectIndex(rects)
    min_piece = 0.8      # a rule survives down to 0.8 mm (it is one held cell)
    min_hull_piece = 1.5  # a trimmed outline shorter than this is debris, not a wall
    cut_strokes: List[Tuple[int, int, List[Point]]] = []
    cut_pens: List[Optional[int]] = []
    trimmed = 0
    for (cidx, p, pts), spen in zip(strokes, stroke_pen):
        parts = _cut_away(pts, kidx, min_hull_piece)
        if len(parts) != 1 or abs(_plen(parts[0]) - _plen(pts)) > 1e-6:
            trimmed += 1
        for q in parts:
            cut_strokes.append((cidx, p, q))
            cut_pens.append(spen)
    strokes, stroke_pen = cut_strokes, cut_pens
    if loop_start != "traced":  # where a closed outline begins (plot order only)
        rot = []
        for c, p, q in strokes:
            if len(q) > 3 and abs(q[0][0] - q[-1][0]) < 1e-6 and abs(q[0][1] - q[-1][1]) < 1e-6:
                ring = q[:-1]
                if loop_start == "left":
                    k = min(range(len(ring)), key=lambda i: (ring[i][0], ring[i][1]))
                else:  # "low"
                    k = min(range(len(ring)), key=lambda i: (ring[i][1], ring[i][0]))
                q = ring[k:] + ring[:k] + [ring[k]]
            rot.append((c, p, q))
        strokes = rot

    # the rules: serpentine (alternate rows run right-to-left so the pen's next
    # start is the row below, not the far wall), then cut back from the coast
    rule_polys: List[List[Point]] = []
    rows_seen: Dict[int, int] = {}
    for i, j0, j1 in screen_runs:
        rows_seen.setdefault(i, len(rows_seen))
    rules_trimmed = 0
    for i, j0, j1 in screen_runs:
        (ax, ay), (bx, _by) = page(j0, i + 1.0), page(j1, i + 1.0)
        seg = [(ax, ay), (bx, ay)]
        parts = _cut_away(seg, kidx, min_piece)
        if len(parts) != 1 or abs(_plen(parts[0]) - _plen(seg)) > 1e-6:
            rules_trimmed += 1
        for q in parts:
            rule_polys.append(q[::-1] if rows_seen[i] % 2 else q)

    # ------------------------------------------------------------ statistics
    sx = [0.5 * (p[0] + q[0]) for p, q in shore if p[0] == q[0]]
    x_mean = sum(sx) / max(1, len(sx))
    x_std = math.sqrt(sum((v - x_mean) ** 2 for v in sx) / max(1, len(sx)))
    cols = [j for j in range(NX) if sim.tr_at(j + 0.5) < 0.80]
    rrows = list(range(screen // 2, NY, screen))
    held_all = sum(fsea[i * NX + j] for i in range(NY) for j in cols) / float(NY * len(cols))
    held_rule = sum(fsea[i * NX + j] for i in rrows for j in cols) / float(len(rrows) * len(cols))
    # the density measured on the INK: drawn rule length on every ruled row,
    # over the 0.70-0.80 columns (each column is one pitch of rule line)
    xa_band, xb_band = page(min(cols), 0)[0], page(max(cols) + 1, 0)[0]
    ink_len = 0.0
    for q in rule_polys:
        lo, hi = min(q[0][0], q[-1][0]), max(q[0][0], q[-1][0])
        ink_len += max(0.0, min(hi, xb_band) - max(lo, xa_band))
    ink_rule = ink_len / ((xb_band - xa_band) * len(rrows))
    m_ex = sum(onsager_m(sim.Kv[j]) for j in cols) / len(cols)

    # census of the DRAWN outlines by T band (the key's bounds)
    bands_T = [(1.00, 1.15), (1.15, 1.35), (1.35, 1.55), (1.55, 1.80)]
    if t_hi > 1.80 + 1e-9:
        bands_T.append((1.80, t_hi))
    drawn_idx = sorted({c for c, _p, _q in strokes})
    band_stats = []
    for lo, hi in bands_T:
        sel = [clusters[c] for c in drawn_idx if lo <= sim.tr_at(clusters[c]["cx"]) < hi]
        band_stats.append({
            "T": (lo, hi),
            "count": len(sel),
            "mean_sites": round(sum(c["size"] for c in sel) / max(1, len(sel)), 2),
            "black_share": round(sum(c["size"] >= tier_lo for c in sel) / max(1, len(sel)), 2),
        })
    w_peak = max(range(len(band_stats)), key=lambda b: band_stats[b]["mean_sites"])
    n_peak = max(range(len(band_stats)), key=lambda b: band_stats[b]["count"])
    if w_peak == 0 and n_peak > 0:
        peak_line = "WEIGHT PEAKS AT TC   COUNT PEAKS PAST IT"
    elif w_peak == 0 and n_peak == 0:
        peak_line = "WEIGHT AND COUNT BOTH PEAK AT TC"
    else:
        peak_line = "OUTLINE WEIGHT PEAKS PAST TC"

    # A18 on the ink: 20 mm columns anchored on the field's right edge (the last
    # one 25 mm), outlines counted by centroid; the last column's marks and its
    # longest mark-free vertical run are measured on every drawn stroke
    col_edges = [fx1, fx1 - 25.0]
    while col_edges[-1] - 20.0 > fx0:
        col_edges.append(col_edges[-1] - 20.0)
    col_edges.append(fx0)
    col_list = list(zip(col_edges[1:], col_edges[:-1]))  # [0] = last column
    col_cnt = [0] * len(col_list)
    for c in drawn_idx:
        xm = fx0 + clusters[c]["cx"] * pitch
        for k, (a, b) in enumerate(col_list):
            if a <= xm < b or (k == 0 and xm >= b):
                col_cnt[k] += 1
                break
    last_x = fx1 - 25.0
    last_marks = len({c for c, _p, q in strokes if max(pt[0] for pt in q) > last_x})
    ys = []
    all_ink = [q for _c, _p, q in strokes] + rule_polys + [
        [a, b] for a, b in shore_mm
    ]
    for q in all_ink:
        for a, b in zip(q, q[1:]):
            if max(a[0], b[0]) > last_x:
                ys.append((min(a[1], b[1]), max(a[1], b[1])))
    ys.sort()
    gaps, cur_top = [], fy0
    for lo, hi in ys:
        if lo > cur_top:
            gaps.append(lo - cur_top)
        cur_top = max(cur_top, hi)
    gaps.append(fy1 - cur_top)
    x13 = x_of(1.30)
    k13 = next(k for k, (a, b) in enumerate(col_list) if a <= x13 < b)
    k182 = next(k for k, (a, b) in enumerate(col_list) if a <= 182.0 < b)
    per_rung = {0: 0, 1: 0, 2: 0, 3: 0}
    for c in drawn_idx:
        per_rung[rung(clusters[c]["size"])] += 1
    stats = {
        "pitch": pitch,
        "field": (fx0, fy0, fx1, fy1),
        "seam_roll_rows": roll,
        "seam_crossings": cross[roll],
        "sea_frac": sum(fsea) / float(NX * NY),
        "shore_edges": len(shore),
        "shore_dropped_edges": shore_dropped,
        "shore_components_before": shore_comps,
        "shore_T": sim.tr_at(x_mean),
        "shore_T_std": (t_hi - t_lo) * x_std / NX,
        "shore_T_range": (sim.tr_at(min(sx)), sim.tr_at(max(sx))),
        "sea_to_coast_mm": x_mean * pitch,
        "energy_rms_band": diag["rms"],
        "wolff_frozen": diag["wolff_frozen"],
        "droplets_drawn": len(drawn_idx),
        "droplets_per_rung": per_rung,
        "edges_thinned": thinned,
        "corner_segments_cut": corner_cut,
        "neck_segments_cut": neck_cut,
        "knot_segments_cut": knot_cut,
        "strokes_trimmed_at_coast": trimmed,
        "rules_trimmed_at_coast": rules_trimmed,
        "rule_cells_yielded": yielded,
        "held_070_080_rule_rows": held_rule,
        "held_070_080_all_rows": held_all,
        "ink_070_080_rule_rows": ink_rule,
        "onsager_m_070_080": m_ex,
        "bands": band_stats,
        "peak_line": peak_line,
        "cols_left_to_right": col_cnt[::-1],
        "cols_from_T1.3": col_cnt[k13::-1],
        "cols_from_x182": col_cnt[k182::-1],
        "last_col_marks": last_marks,
        "last_col_free_run_mm": max(gaps),
        "largest": sorted((c["size"] for c in clusters), reverse=True)[:6],
    }

    # ---------------------------------------------------------- the marks
    for q in rule_polys:  # the ordered sea
        sc.poly(q, pen=black, halos=False)
    for (_idx, _p, pts), spen in zip(strokes, stroke_pen):
        sc.poly(pts, pen=spen, halos=False)
    sc.poly([(fx0, fy0), (fx0, fy1)], pen=black, halos=False)  # the cold wall
    for ch in _chain_segments(shore_mm, tol=1e-3):
        if len(ch) < 2:
            continue
        for k in range(3):
            off = (k - 1) * coast_gap
            sc.poly(_simplify(_closed_offset(ch, off)), pen=red, halos=False)

    # --------------------------------------------- the thermometer, on top
    ry = fy1 + 2.2
    sc.emit(_poly([(fx0, ry), (fx1, ry)], color=black, f=feed))
    steps = int(round((t_hi - t_lo) / 0.05))
    label_tops = []
    for k in range(steps + 1):
        tr = t_lo + k * 0.05
        x = x_of(tr)
        major = abs((tr * 10) - round(tr * 10)) < 1e-6
        is_tc = abs(tr - 1.0) < 1e-6
        ln = 3.2 if is_tc else (1.8 if major else 0.9)
        sc.emit(_poly([(x, ry), (x, ry + ln)], color=red if is_tc else black, f=feed))
        if is_tc or (major and round(tr * 10) % 2 == 0 and abs(tr - 1.0) > 0.15):
            lbl = f"{tr:.2f}"
            h = 2.2
            lx = min(max(x - _text_width(lbl, h) / 2.0, fx0), fx1 - _text_width(lbl, h))
            sc.emit(_stroke_text(lbl, lx, ry + ln + 1.2, h, color=red if is_tc else black, f=feed))
            label_tops.append(ry + ln + 1.2 + h)
    x_tc = x_of(1.0)
    stats["ruler_label_clear_mm"] = y1 - max(label_tops)

    # ------------------------------------------------ the title (weighted)
    t_h = title_cap
    sc_t = t_h / 6.0
    glyph_w = 4.0 * sc_t
    word = "CRITICAL"
    adv = (fy1 - fy0 - glyph_w) / (len(word) - 1)
    t_x = tx + t_h + t_weight / 2.0
    for k, ch in enumerate(word):
        sc.emit(_title_glyph(ch, t_x, fy0 + k * adv, t_h, black, t_weight, 0.3, 90.0, feed))
    stats["title"] = (tx, fy0, t_x + t_weight / 2.0, fy0 + (len(word) - 1) * adv + glyph_w)

    # --------------------------------------------------- the type strip
    # a 5-line grid; three blocks, each hung under what it explains: the sea on
    # the left axis, Tc on the red tick, the hot side on the `hot_tick` tick.
    def bl(k: int) -> float:
        return base + (4 - k) * line_pitch

    block_sea = [
        "RULED   THE HELD FK CLUSTER",
        "EVERY 3RD ROW   LEFT EDGE HELD UP",
        "RULE DENSITY IS THE MAGNETISATION M",
        f"UNDER 0.80 TC   AS DRAWN {ink_rule:.3f}",
        f"ONSAGER M {m_ex:.3f}",
    ]
    block_tc = [
        f"RED  HELD CLUSTER HULL  MEAN {stats['shore_T']:.2f} TC",
        "TC 2.269185   ONSAGER 1944   EXACT",
        peak_line,
    ]
    if cut < tier_lo:
        key_line = (f"GREY {cut}-{tier_lo - 1}   1 PASS {tier_lo}-{tier_mid - 1}   2 PASSES"
                    f" {tier_mid}-{tier_hi - 1}   3 PASSES {tier_hi}+")
        grey_head = f"GREY {cut}-{tier_lo - 1}"
    else:
        key_line = (f"1 PASS {cut}-{tier_mid - 1}   2 PASSES {tier_mid}-{tier_hi - 1}"
                    f"   3 PASSES {tier_hi}+")
        grey_head = None
    block_hot = [
        f"2D ISING  {NX} X {NY}  SEED {rng.seed}   T OVER TC {t_lo:.2f} TO {t_hi:.2f}",
        "FK  SPINS BONDED WITH PROB 1-EXP(-2J/T)   TOP AND BOTTOM WRAP",
        "OUTLINED   FREE FK CLUSTERS BY SITE COUNT",
        key_line,
        f"BLANK   DISORDER FINER THAN {cut} SITES",
    ]
    for k, ln in enumerate(block_sea):
        sc.emit(_stroke_text(ln, tx, bl(k), type_h, color=black, f=feed))
    for k, ln in enumerate(block_tc):
        sc.emit(_stroke_text(ln, x_tc, bl(k), type_h, color=black, f=feed))
    sc.emit(giant_type("TC IS A PLACE", x_tc, base, place_cap, pen=black, weight=0.3,
                       tip=0.3, f=feed))
    bx = x_of(hot_tick)
    for k, ln in enumerate(block_hot):
        if grey_head and ln.startswith(grey_head):
            sc.emit(_stroke_text(grey_head, bx, bl(k), type_h, color=grey, f=feed))
            rest = ln[len(grey_head):]
            sc.emit(_stroke_text(rest, bx + _text_width(grey_head, type_h), bl(k), type_h,
                                 color=black, f=feed))
        else:
            sc.emit(_stroke_text(ln, bx, bl(k), type_h, color=black, f=feed))
    stats["type"] = {
        "sea_right": tx + max(_text_width(ln, type_h) for ln in block_sea),
        "tc_left": x_tc,
        "tc_right": x_tc + max([_text_width(ln, type_h) for ln in block_tc]
                               + [giant_type_width("TC IS A PLACE", place_cap)]),
        "hot_left": bx,
        "hot_right": bx + max(_text_width(ln, type_h) for ln in block_hot),
        "first_cap_top": bl(0) + type_h,
        "air_above_footer": fy0 - (bl(0) + type_h),
        "last_baseline_above_margin": base - y0,
        "clear_above_place": bl(len(block_tc) - 1) - (base + place_cap + 0.15),
    }

    out_cmds = sc.render()
    logging.getLogger(__name__).info("r07 stats %s", stats)
    ising_cooling_strip_r07.stats = stats  # type: ignore[attr-defined]
    ising_cooling_strip_r07.strokes = strokes  # type: ignore[attr-defined]
    ising_cooling_strip_r07.stroke_pen = stroke_pen  # type: ignore[attr-defined]
    ising_cooling_strip_r07.rules = rule_polys  # type: ignore[attr-defined]
    ising_cooling_strip_r07.shore_mm = shore_mm  # type: ignore[attr-defined]
    ising_cooling_strip_r07.clusters = clusters  # type: ignore[attr-defined]
    return out_cmds
