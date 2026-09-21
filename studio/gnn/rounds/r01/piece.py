"""GNN — REACH: a node's receptive field drawn as terrain, message passing as collapse.

Studio candidate, round r01 (brief: ``studio/nets/gnn.md``).

Contract (promptplot/studio/loop.py:_render_code_payload):
    studio_gnn(rng: SeededRNG, bounds, colors: int = 3) -> list[GCodeCommand]

Everything on the sheet is COMPUTED, not illustrated:
  * a seeded small-world geometric graph (Poisson-disk cloud + kNN + long-range
    shortcut rewires, forced connected);
  * exact BFS hop distance d(v) from one root;
  * the continuous hop field  f(p) = min_v [ d(v) + |p - p_v| / L ]  — the lower
    envelope of unit cones, whose level sets ARE the k-hop receptive fields;
  * exact mean-aggregation dynamics  h^(k) = D^-1 (A+I) h^(k-1)  on the same
    graph, whose row-stochastic operator drives every node to one consensus
    value (oversmoothing), at the empirically measured rate |lambda_2|.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

from promptplot.generative.engine import Scene3D, ScreenThin
from promptplot.generative.kit import (
    Bounds,
    _catmull_subdivide,
    _chain_segments,
    _dot,
    _marching_squares,
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    circle,
    fill_disc,
    scale_footer,
    swatch_bar,
    type_block,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

BLACK, RED, BLUE = 0, 1, 2


# ---------------------------------------------------------------------------
# the graph (seeded, exact)
# ---------------------------------------------------------------------------
def _poisson_cloud(rng: SeededRNG, n: int, sep: float) -> List[Tuple[float, float]]:
    """Dart-thrown blue-noise cloud in [-1,1]^2 — organic, never a lattice."""
    cell = sep / math.sqrt(2.0)
    grid: Dict[Tuple[int, int], List[Tuple[float, float]]] = {}
    pts: List[Tuple[float, float]] = []
    for _ in range(80 * n):
        if len(pts) >= n:
            break
        p = (rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0))
        ci, cj = int((p[0] + 1.0) / cell), int((p[1] + 1.0) / cell)
        ok = True
        for di in (-2, -1, 0, 1, 2):
            for dj in (-2, -1, 0, 1, 2):
                for q in grid.get((ci + di, cj + dj), ()):
                    if (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 < sep * sep:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            pts.append(p)
            grid.setdefault((ci, cj), []).append(p)
    return pts


def _adjacency(pts: Sequence[Tuple[float, float]], knn: int) -> Dict[int, set]:
    adj: Dict[int, set] = {i: set() for i in range(len(pts))}
    for i, p in enumerate(pts):
        order = sorted(
            range(len(pts)), key=lambda j: (pts[j][0] - p[0]) ** 2 + (pts[j][1] - p[1]) ** 2
        )
        for j in order[1 : knn + 1]:
            adj[i].add(j)
            adj[j].add(i)
    return adj


def _components(adj: Dict[int, set]) -> List[List[int]]:
    seen, comps = set(), []
    for s in adj:
        if s in seen:
            continue
        stack, comp = [s], []
        seen.add(s)
        while stack:
            v = stack.pop()
            comp.append(v)
            for u in adj[v]:
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
        comps.append(comp)
    return comps


def _connect(pts, adj) -> None:
    """Weld stragglers onto the giant component (nearest pair) — exact."""
    comps = sorted(_components(adj), key=len, reverse=True)
    main = set(comps[0])
    for comp in comps[1:]:
        best = min(
            ((i, j) for i in comp for j in main),
            key=lambda e: (pts[e[0]][0] - pts[e[1]][0]) ** 2 + (pts[e[0]][1] - pts[e[1]][1]) ** 2,
        )
        adj[best[0]].add(best[1])
        adj[best[1]].add(best[0])
        main |= set(comp)


def _shortcuts(rng, pts, adj, k: int, min_span: float) -> List[Tuple[int, int]]:
    """Watts-Strogatz long-range rewires: the edges that make a graph small-world."""
    cands = [
        (i, j)
        for i in range(len(pts))
        for j in range(i + 1, len(pts))
        if math.dist(pts[i], pts[j]) > min_span
    ]
    rng.shuffle(cands)
    picked: List[Tuple[int, int]] = []
    for i, j in cands:
        if len(picked) >= k:
            break
        if any(min(math.dist(pts[i], pts[a]), math.dist(pts[j], pts[b])) < 0.5 for a, b in picked):
            continue
        picked.append((i, j))
        adj[i].add(j)
        adj[j].add(i)
    return picked


def _bfs(adj: Dict[int, set], root: int) -> List[float]:
    d = [math.inf] * len(adj)
    d[root] = 0.0
    frontier = [root]
    while frontier:
        nxt = []
        for v in frontier:
            for u in adj[v]:
                if d[u] == math.inf:
                    d[u] = d[v] + 1.0
                    nxt.append(u)
        frontier = nxt
    return d


def _smooth(adj: Dict[int, set], h0: List[float], layers: int) -> List[List[float]]:
    """h^(k) = D^-1 (A+I) h^(k-1) — mean aggregation, exactly."""
    hist = [list(h0)]
    for _ in range(layers):
        prev = hist[-1]
        hist.append([(prev[v] + sum(prev[u] for u in adj[v])) / (len(adj[v]) + 1) for v in range(len(adj))])
    return hist


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def studio_gnn(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_nodes: int = 150,
    node_sep: float = 0.112,
    knn: int = 3,
    n_shortcut: int = 3,
    span: float = 1.05,
    hops_red: int = 3,
    layers: int = 12,
    n_traj: int = 34,
    grid: int = 78,
    cgrid: int = 150,
    gamma: float = 1.35,
    lift: float = 0.40,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """REACH — a GNN's receptive field is not a disc, it is an ARCHIPELAGO.

    Hero: the exact hop-distance field of a seeded small-world graph, rendered
    as hidden-line terrain (root = summit, height falls one hop per terrace).
    The red terraces are the 1/2/3-hop receptive field of a normal 3-layer GNN
    — ragged, and broken into ISLANDS wherever a long-range shortcut teleports
    the message across the sheet. Footer: the same graph's mean-aggregation
    states over 12 layers, collapsing into one consensus line (oversmoothing).
    """
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    black, red, blue = _pen(BLACK, colors), _pen(RED, colors), _pen(BLUE, colors)
    tpen = _pen(3, colors) if colors >= 4 else black

    # ---- graph ------------------------------------------------------------
    pts = _poisson_cloud(rng, n_nodes, node_sep)
    adj = _adjacency(pts, knn)
    _connect(pts, adj)
    shorts = _shortcuts(rng, pts, adj, n_shortcut, span)
    root = min(range(len(pts)), key=lambda i: math.dist(pts[i], (0.46, 0.18)))
    hop = _bfs(adj, root)
    L = sorted(math.dist(pts[i], pts[j]) for i in adj for j in adj[i] if j > i)
    L = L[len(L) // 2]  # median edge length = one hop of reach

    # ---- the continuous hop field f(p) = min_v [ d(v) + |p-p_v| / L ] -------
    P = np.array(pts)
    D = np.array(hop, dtype=float)

    def field(GX, GZ):
        F = np.full(GX.shape, 1e18)
        for (px, pz), dv in zip(P, D):
            np.minimum(F, dv + np.sqrt((GX - px) ** 2 + (GZ - pz) ** 2) / L, out=F)
        return F

    gx = np.linspace(-1.06, 1.06, grid + 1)
    GX, GZ = np.meshgrid(gx, gx)
    FS = field(GX, GZ)
    fcap = float(FS.max())

    def hgt(f):
        return max(0.0, (1.0 - f / fcap)) ** gamma

    # ---- camera: hero band, peak right-of-centre ---------------------------
    hy0, hy1 = y0 + 0.315 * H, y0 + 0.995 * H
    hh = hy1 - hy0
    cx, cy = x0 + 0.50 * W, hy0 + 0.38 * hh
    aa, cd, bwy = 0.240 * W, 0.112 * hh, 0.335 * hh

    def proj(wx, wy, wz):
        return (cx + (wx - wz) * aa, cy + wy * bwy - (wx + wz) * cd)

    def dep(wx, wy, wz):
        return (wx + wz) + 0.12 * wy

    scene = Scene3D(rng, bounds, feed=feed, tip=0.5, px=(300, 300), pad=3.0, fit="rescue")

    HH = np.maximum(0.0, 1.0 - FS / fcap) ** gamma
    SX = cx + (GX - GZ) * aa
    SY = cy + HH * bwy - (GX + GZ) * cd
    DEP = (GX + GZ) + 0.12 * HH

    # ---- type reserves its halos BEFORE any geometry (house law) -----------
    xT = x0 + 0.02 * W
    rp = proj(pts[root][0], hgt(0.0), pts[root][1])
    isl = max(shorts, key=lambda e: hop[e[0]] + hop[e[1]]) if shorts else None
    ip = proj(pts[isl[1]][0], hgt(hop[isl[1]]), pts[isl[1]][1]) if isl else (cx, cy)
    by0, by1 = y0 + 0.108 * H, y0 + 0.222 * H
    bx0, bx1 = xT, x0 + 0.93 * W
    scene.halo_labels(
        [
            (_spaced("REACH"), xT, y1 - 7.0, 4.6, tpen),
            (_spaced("GNN . MESSAGE PASSING"), xT, y1 - 14.5, 2.0, tpen),
            (_spaced("THREE HOPS TO SEE . TWELVE TO FORGET"), xT, y1 - 19.6, 2.0, tpen),
            (_spaced("ROOT"), rp[0] + 4.0, rp[1] + 3.2, 2.2, tpen),
            (_spaced("ARCHIPELAGO"), ip[0] - 6.0, ip[1] + 5.0, 2.2, tpen),
            (_spaced("RECEPTIVE FIELD . 3 HOPS"), xT, hy0 + 0.035 * hh, 2.0, tpen),
            (_spaced("OVERSMOOTHING"), xT, by1 + 4.2, 2.6, tpen),
            (_spaced("K 0"), bx0, by0 - 5.0, 1.8, tpen),
            (_spaced("K 12"), bx1 - _text_width(_spaced("K 12"), 1.8), by0 - 5.0, 1.8, tpen),
        ]
    )

    # ---- the terrain: ONE declaration --------------------------------------
    scene.surface(SX, SY, DEP, pen=black, thin=ScreenThin(gap_mm=0.95, far_mult=2.4))

    # ---- hop terraces = level sets of f (marching squares, draped exactly) --
    cx_ = np.linspace(-1.06, 1.06, cgrid + 1)
    CGX, CGZ = np.meshgrid(cx_, cx_)
    FC = field(CGX, CGZ).tolist()
    xs = list(cx_)
    nlev = max(2, int(fcap - 0.6))
    for lev in range(1, nlev + 1):
        wy = hgt(float(lev))
        chains = _chain_segments(_marching_squares(FC, xs, xs, float(lev)))
        pen = red if lev <= hops_red else black
        fam = []
        for ch in chains:
            if len(ch) < 6:
                continue
            fam.append([(*proj(u, wy, v), dep(u, wy, v), pen) for u, v in ch])
        scene.lines(fam, mode="over")

    # ---- nodes on the surface (size = degree; hidden where the land hides) --
    for i, (u, v) in enumerate(pts):
        wy = hgt(hop[i])
        sx, sy = proj(u, wy, v)
        if not scene.visible(sx, sy, dep(u, wy, v)) or scene._blocked(sx, sy):
            continue
        scene.emit(_dot(sx, sy, 0.32 + 0.085 * min(6, len(adj[i])), color=black, f=feed))

    # ---- the shortcuts: red arcs LEAPING the landscape ---------------------
    for i, j in shorts:
        h_i, h_j = hgt(hop[i]), hgt(hop[j])
        arc = []
        for s in range(61):
            t = s / 60.0
            u = pts[i][0] + (pts[j][0] - pts[i][0]) * t
            v = pts[i][1] + (pts[j][1] - pts[i][1]) * t
            wy = h_i + (h_j - h_i) * t + lift * math.sin(math.pi * t)
            arc.append((*proj(u, wy, v), dep(u, wy, v), red))
        scene.lines([arc], mode="over")

    # ---- the root: the single loudest mark ---------------------------------
    scene.emit(fill_disc(rp[0], rp[1], 2.5, spacing=0.45, pen=red, f=feed))
    scene.emit(circle(rp[0], rp[1], 4.4, pen=red, f=feed))

    # ---- OVERSMOOTHING: mean aggregation collapses every state -------------
    N = len(pts)
    raw = [math.sin(2.3 * pts[i][0]) * math.cos(1.9 * pts[i][1]) for i in range(N)]
    lo, hi = min(raw), max(raw)
    h0 = [2.0 * (r - lo) / (hi - lo) - 1.0 for r in raw]
    hist = _smooth(adj, h0, layers)
    spread = [max(h) - min(h) for h in hist]
    lam = spread[-1] / spread[-2] if spread[-2] > 1e-12 else 0.0

    rank = sorted(range(N), key=lambda v: h0[v])
    keep = [rank[round(t * (N - 1) / (n_traj - 1))] for t in range(n_traj)]
    ymid, yamp = (by0 + by1) / 2.0, (by1 - by0) / 2.0
    for v in keep:
        pth = [
            (bx0 + (bx1 - bx0) * k / layers, ymid + yamp * hist[k][v] / spread[0] * 2.0)
            for k in range(layers + 1)
        ]
        smooth, _ = _catmull_subdivide(pth, subdiv=4)
        scene.poly(smooth, pen=blue)
    cons = ymid + yamp * hist[-1][keep[0]] / spread[0] * 2.0
    scene.emit(_dot(bx1 + 1.6, cons, 1.1, color=red, f=feed))

    # ---- furniture + footer, all on the shared left/right axes -------------
    scene.emit(
        _stroke_text(
            _spaced("LAMBDA2 %.2f . SPREAD PER LAYER" % lam),
            bx0,
            by1 + 10.0,
            1.8,
            color=tpen,
            f=feed,
        )
    )
    scene.emit(
        _stroke_text(
            _spaced("H K . MEAN OF H K-1 OVER N V PLUS V"), xT, y0 + 2.5, 2.0, color=tpen, f=feed
        )
    )
    scene.emit(swatch_bar(x1 - 8.0, by1 + 12.0, [black, red, blue], size=2.4, f=feed))
    scene.emit(
        scale_footer(
            bounds, text="%d NODES . %d HOPS" % (N, int(max(hop))), pen=tpen, height=2.0, f=feed
        )
    )
    return scene.render()
