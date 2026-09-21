"""MIXTURE OF EXPERTS — candidate r01.

SPARSE ROUTING: the router's partition of input space, computed exactly, and
the traffic that actually lands on it. See NOTES.md for the maths.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import HIDE, Iso, Scene3D
from promptplot.generative.kit import (
    BLACK,
    BLUE,
    PINK,
    Bounds,
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    plus_mark,
    scale_footer,
    swatch_bar,
    type_block,
)

_SQUARE = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]


def _clip_hp(poly: Sequence[Tuple[float, float]], ax: float, ay: float, c: float):
    """Sutherland-Hodgman: keep the part of a convex polygon where
    ``ax*x + ay*y + c >= 0``. Exact — the cut lands ON the line."""
    if len(poly) < 3:
        return []
    out: List[Tuple[float, float]] = []
    n = len(poly)
    for k in range(n):
        p, q = poly[k], poly[(k + 1) % n]
        fp = ax * p[0] + ay * p[1] + c
        fq = ax * q[0] + ay * q[1] + c
        if fp >= 0.0:
            out.append(p)
        if (fp >= 0.0) != (fq >= 0.0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out if len(out) >= 3 else []


def _area(poly) -> float:
    a = 0.0
    n = len(poly)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        a += x0 * y1 - x1 * y0
    return abs(a) * 0.5


def studio_moe(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_experts: int = 16,
    topk: int = 2,
    n_tokens: int = 900,
    collapse_rounds: int = 9,
    eta: float = 0.62,
    terraces: int = 8,
    grid: int = 108,
    dot_sep: float = 1.05,
    tip: float = 0.5,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """SPARSE ROUTING — conditional computation drawn as a mostly-blank plate.

    A real linear gate ``l_i(x) = w_i.x + b_i`` over a 2-D token space with
    N=16 experts.  argmax over affine functions is EXACT convex geometry: each
    expert owns a polygonal cell (an intersection of half-planes, solved here
    by Sutherland-Hodgman clipping, no sampling).  The height field is the
    ROUTING MARGIN ``D(x) = l_(1) - l_(2)`` — zero exactly on the cell walls,
    rising to an apex inside each cell — so the plate is a landscape of faceted
    confidence tents separated by valleys of indecision.  Every terrace ring is
    the exact level set ``{l_i - l_j >= t, all j}``, another half-plane clip.

    The imbalance is SIMULATED, not assumed: starting from an unbiased gate the
    piece runs the un-regularised rich-get-richer dynamic
    ``b_i += eta (f_i - 1/N)`` — the positive feedback that load-balancing
    losses exist to suppress — until the router has collapsed.  Most experts
    end with no territory at all and are simply absent from the drawing; of
    those that survive, most get no tokens.  The red marks are the tokens
    themselves, each sitting on the terrain at its own routing margin, so the
    load is not encoded, it IS the ink.  Inside the dominant cell, dotted blue
    walls subdivide it by each token's SECOND expert (k=2).  Everything else is
    cream paper: sparsity is the absence of drawing."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, red, blk = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    legend = _pen(3, colors) if colors >= 4 else blk
    N = n_experts

    # ---------------------------------------------------------------- the gate
    Wx: List[float] = []
    Wy: List[float] = []
    B: List[float] = []
    for i in range(N):
        ang = 2 * math.pi * (i + 0.55 * rng.random()) / N
        rad = 0.70 + 0.95 * rng.random()
        Wx.append(rad * math.cos(ang))
        Wy.append(rad * math.sin(ang))
        B.append(0.08 * rng.gauss(0.0, 1.0))

    # -------------------------------------------------------------- the tokens
    mus = [(-0.34, 0.36), (0.46, -0.10), (-0.02, -0.58)]
    sgs = [0.31, 0.23, 0.18]
    wts = [0.46, 0.34, 0.20]
    toks: List[Tuple[float, float]] = []
    guard = 0
    while len(toks) < n_tokens and guard < 80 * n_tokens:
        guard += 1
        c = rng.choices([0, 1, 2], weights=wts, k=1)[0]
        u = mus[c][0] + rng.gauss(0.0, sgs[c])
        v = mus[c][1] + rng.gauss(0.0, sgs[c])
        if -0.97 < u < 0.97 and -0.97 < v < 0.97:
            toks.append((u, v))

    def rank(u: float, v: float):
        ls = sorted(((Wx[i] * u + Wy[i] * v + B[i], i) for i in range(N)), reverse=True)
        return ls

    # ---- ROUTING COLLAPSE: the un-regularised rich-get-richer feedback loop
    for _ in range(collapse_rounds):
        cnt = [0] * N
        for u, v in toks:
            for _lg, i in rank(u, v)[:topk]:
                cnt[i] += 1
        tot = float(len(toks) * topk) or 1.0
        for i in range(N):
            B[i] += eta * (cnt[i] / tot - 1.0 / N)

    # final routing statistics (what the footer reports)
    top1 = [0] * N
    topk_cnt = [0] * N
    tok_rank: List[Tuple[int, int, float]] = []
    for u, v in toks:
        ls = rank(u, v)
        top1[ls[0][1]] += 1
        for _lg, i in ls[:topk]:
            topk_cnt[i] += 1
        tok_rank.append((ls[0][1], ls[1][1], ls[0][0] - ls[1][0]))

    # ------------------------------------------------- exact routing geometry
    def region(i: int, t: float, drop: int = -1):
        """{x in [-1,1]^2 : l_i(x) - l_j(x) >= t for every j (minus `drop`)} —
        exact intersection of half-planes.  t = 0 gives expert i's cell; t > 0
        gives its margin terrace; dropping j gives 'i wins if j abstains'."""
        poly = list(_SQUARE)
        for j in range(N):
            if j == i or j == drop:
                continue
            poly = _clip_hp(poly, Wx[i] - Wx[j], Wy[i] - Wy[j], B[i] - B[j] - t)
            if not poly:
                return []
        return poly

    cells = [region(i, 0.0) for i in range(N)]
    live = [i for i in range(N) if cells[i] and _area(cells[i]) > 4e-3]

    def apex(i: int):
        """The point of maximum routing margin inside cell i (bisection on the
        terrace level until the terrace shrinks to a point)."""
        hi = 0.05
        while region(i, hi) and hi < 16.0:
            hi *= 2.0
        lo = 0.0
        for _ in range(28):
            mid = 0.5 * (lo + hi)
            if region(i, mid):
                lo = mid
            else:
                hi = mid
        p = region(i, lo)
        if not p:
            return None
        return (sum(q[0] for q in p) / len(p), sum(q[1] for q in p) / len(p), lo)

    apexes = {i: apex(i) for i in live}
    apexes = {i: a for i, a in apexes.items() if a is not None}
    hero = max(live, key=lambda i: top1[i]) if live else 0
    dmax = max((a[2] for a in apexes.values()), default=1.0) or 1.0

    def margin(u: float, v: float) -> float:
        ls = rank(u, v)
        return ls[0][0] - ls[1][0]

    # ------------------------------------------------------- camera + scene
    #  left corner inside the plate, right corner CROPPED at the margin
    a_sp = 0.235 * W
    cx = x0 + 0.655 * W
    cy = y0 + 0.560 * H
    cd = 0.098 * H
    hy = 0.150 * H / dmax  # mm per margin unit
    iso = Iso(cx=cx, cy=cy, a=a_sp, wy=hy, cd=cd, depth_wy=0.30)
    scene = Scene3D(rng, bounds, feed=feed, tip=tip, px=(260, 240), fit="rescue")

    cx0, cy0, cx1, cy1 = x0 + 1.5, y0 + 0.155 * H, x1 - 1.5, y1 - 0.085 * H

    def keep(sx: float, sy: float) -> bool:
        return cx0 <= sx <= cx1 and cy0 <= sy <= cy1

    def S(u: float, v: float, m: float):
        return iso.proj(u, m, v), iso.depth(u, m, v)

    # ---- the depth field: rasterise the margin terrain, then drop its mesh.
    # (engine gap: Scene3D has no rasterise-only entry point — see NOTES.md)
    G = grid
    SX = np.zeros((G + 1, G + 1))
    SY = np.zeros((G + 1, G + 1))
    DE = np.zeros((G + 1, G + 1))
    for ii in range(G + 1):
        u = -1.0 + 2.0 * ii / G
        for jj in range(G + 1):
            v = -1.0 + 2.0 * jj / G
            m = margin(u, v)
            (sx, sy), dp = S(u, v, m)
            SX[ii, jj], SY[ii, jj], DE[ii, jj] = sx, sy, dp
    _n0 = len(scene.out)
    scene.surface(SX, SY, DE, pen=blk, thin=None)
    del scene.out[_n0:]

    # --------------------------------------------------------------- sampling
    def edge_samples(poly, t: float, pen, step: float = 1.1, dash: int = 0):
        """Densify a closed polygon at height t into (sx, sy, dep, pen)
        samples.  dash > 0 turns it into a dotted projection line."""
        pts = list(poly) + [poly[0]]
        sm: List[Tuple[float, float, float, Optional[int]]] = []
        k = 0
        for q in range(len(pts) - 1):
            (u0, v0), (u1, v1) = pts[q], pts[q + 1]
            (ax_, ay_), _ = S(u0, v0, t)
            (bx_, by_), _ = S(u1, v1, t)
            n = max(2, int(math.hypot(bx_ - ax_, by_ - ay_) / step))
            for mstep in range(n + 1):
                f = mstep / n
                uu, vv = u0 + (u1 - u0) * f, v0 + (v1 - v0) * f
                (sx, sy), dp = S(uu, vv, t)
                on = True if dash <= 0 else (k % (2 * dash)) < dash
                sm.append((sx, sy, dp if (on and keep(sx, sy)) else HIDE, pen))
                k += 1
        return sm

    def seg_samples(p0, p1, pen, step: float = 1.0, dash: int = 0):
        (ax_, ay_), _ = S(*p0)
        (bx_, by_), _ = S(*p1)
        n = max(2, int(math.hypot(bx_ - ax_, by_ - ay_) / step))
        sm = []
        for mstep in range(n + 1):
            f = mstep / n
            uu = p0[0] + (p1[0] - p0[0]) * f
            vv = p0[1] + (p1[1] - p0[1]) * f
            tt = p0[2] + (p1[2] - p0[2]) * f
            (sx, sy), dp = S(uu, vv, tt)
            on = True if dash <= 0 else (mstep % (2 * dash)) < dash
            sm.append((sx, sy, dp if (on and keep(sx, sy)) else HIDE, pen))
        return sm

    # ---------------------------------------------- 1. the walls (t = 0)
    occ = scene.occupancy(1.15)
    walls = [edge_samples(cells[i], 0.0, blk) for i in live]
    scene.lines(walls, mode="pause_resume", occupancy=occ, warmup=3, min_kept=5)

    # ---------------------------------------------- 2. the margin terraces
    dt = dmax / max(2, terraces)
    fam = []
    for step_k in range(1, terraces + 1):
        t = step_k * dt
        for i in live:
            poly = region(i, t)
            if poly and _area(poly) > 1e-4:
                fam.append(edge_samples(poly, t, blk))
    scene.lines(fam, mode="pause_resume", occupancy=occ, warmup=3, min_kept=6)

    # ---------------------------------------------- 3. the block-diagram skirt
    skirt = []
    for fixed in (1.0, -1.0):
        rail = []
        drop = []
        n = 120
        for q in range(n + 1):
            w_ = -1.0 + 2.0 * q / n
            u, v = (fixed, w_) if fixed > 0 else (w_, fixed)
            m = margin(u, v)
            (sx, sy), dp = S(u, v, m)
            rail.append((sx, sy, dp if keep(sx, sy) else HIDE, blk))
            (bx_, by_), bd = S(u, v, -0.28 * dmax)
            drop.append((bx_, by_, bd if keep(bx_, by_) else HIDE, blk))
        skirt.append(rail)
        skirt.append(drop)
    for cor in ((1.0, 1.0), (1.0, -1.0), (-1.0, 1.0)):
        skirt.append(
            seg_samples(
                (cor[0], cor[1], margin(*cor)), (cor[0], cor[1], -0.28 * dmax), blk, dash=2
            )
        )
    scene.lines(skirt, mode="over")

    # ---------------------------------------------- 4. k = 2 inside the hero
    seen = set()
    partner = []
    for j in range(N):
        if j == hero:
            continue
        sub = region(hero, 0.0, drop=j)
        if not sub or _area(sub) < 6e-3:
            continue
        sub = _clip_hp(sub, Wx[j] - Wx[hero], Wy[j] - Wy[hero], B[j] - B[hero])
        if not sub or _area(sub) < 6e-3:
            continue
        pts = list(sub) + [sub[0]]
        for q in range(len(pts) - 1):
            key = tuple(sorted((tuple(round(c, 4) for c in pts[q]),
                                tuple(round(c, 4) for c in pts[q + 1]))))
            if key in seen:
                continue
            seen.add(key)
            p0, p1 = pts[q], pts[q + 1]
            partner.append(
                seg_samples((p0[0], p0[1], 0.0), (p1[0], p1[1], 0.0), blue, step=0.9, dash=2)
            )
    scene.lines(partner, mode="over")

    # ---------------------------------------------- 5. the traffic (the tokens)
    tocc = scene.occupancy(dot_sep)
    dots = []
    for (u, v), (w1, _w2, dm) in zip(toks, tok_rank):
        (sx, sy), dp = S(u, v, dm)
        if not keep(sx, sy) or tocc.crowded(sx, sy):
            continue
        tocc.add(sx, sy)
        dots.append([(sx - 0.34, sy, dp, red), (sx + 0.34, sy, dp, red)])
    scene.lines(dots, mode="over")

    # ---------------------------------------------- 6. axonometric droplines
    drops = []
    for i in sorted(live, key=lambda k: -top1[k]):
        ap = apexes.get(i)
        if ap is None:
            continue
        drops.append(seg_samples((ap[0], ap[1], ap[2]), (ap[0], ap[1], 0.0), blk, dash=2))
    scene.lines(drops, mode="over")

    # -------------------------------------------------------------- the type
    xT = x0 + 0.020 * W
    (hx, hy_s), _ = S(*apexes[hero][:2], apexes[hero][2])
    scene.halo_labels(
        [
            (_spaced("E%02d" % hero), hx + 2.4, hy_s + 1.6, 2.2, legend),
            (
                _spaced("%d%% OF TOKENS" % round(100.0 * topk_cnt[hero] / len(toks))),
                hx + 2.4,
                hy_s - 2.2,
                1.5,
                legend,
            ),
        ]
    )

    out = scene.out
    out += type_block(["SPARSE", "ROUTING"], xT, y1 - 5.0, height=5.4, pen=legend, f=feed)
    out += _stroke_text(
        _spaced("SIXTEEN EXPERTS . TWO FIRE . THE REST IS PAPER"),
        xT,
        y1 - 26.0,
        1.9,
        color=legend,
        f=feed,
    )

    # the load strip — the honest detail, on the type axis
    n_live = len(live)
    n_dead = N - n_live
    bw, gap, hmax = 1.7, 1.5, 11.0
    yb = y0 + 0.118 * H
    fmax = max(topk_cnt) / float(len(toks)) or 1.0
    for i in range(N):
        fi = topk_cnt[i] / float(len(toks))
        bx = xT + i * (bw + gap)
        hgt = max(0.5, hmax * fi / fmax)
        pen_i = red if i == hero else blk
        for pss in range(2 if i == hero else 1):
            off = 0.0 if pss == 0 else 0.45
            out += _poly([(bx + off, yb), (bx + off, yb + hgt)], color=pen_i, f=feed)
            out += _poly([(bx + bw - off, yb), (bx + bw - off, yb + hgt)], color=pen_i, f=feed)
        if fi < 1e-9:
            out += _poly([(bx - 0.3, yb - 0.9), (bx + bw + 0.3, yb - 0.9)], color=blk, f=feed)
    out += _poly([(xT, yb), (xT + N * (bw + gap) - gap, yb)], color=legend, f=feed)
    out += _stroke_text(
        _spaced("LOAD PER EXPERT   K = %d" % topk), xT, yb - 5.2, 1.5, color=legend, f=feed
    )
    out += _stroke_text(
        _spaced(
            "%d OF %d HOLD TERRITORY . %d NEVER FIRE . TOP EXPERT %d%%"
            % (n_live, N, n_dead, round(100.0 * topk_cnt[hero] / len(toks)))
        ),
        xT,
        yb - 9.6,
        1.5,
        color=legend,
        f=feed,
    )
    out += swatch_bar(x1 - 9.0, y1 - 4.0, [blk, red, blue], size=2.6, f=feed)
    out += plus_mark(xT + 1.2, y1 - 32.0, s=1.4, pen=blk, f=feed)
    out += scale_footer(bounds, text="Y = SUM GI(X) EI(X)", pen=legend, height=2.4, f=feed)
    return scene.render()
