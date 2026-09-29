"""SUMS TO ONE — r08 (wildcard) of `attention-weaving`. No parent geometry.

THE ORDER: CONTINUOUS WARP (Psychedelic canon, STYLES.md §9).

A softmax row is a partition of one: 16 non-negative shares that add up to
exactly 1. A line of JUSTIFIED TYPE is the same object — letters that share out
one fixed measure between them, flush at both margins. So:

  every LINE of the sheet  = one query's softmax row  (22 queries -> 22 lines)
  every LETTER on a line   = one key, the phrase S O F T M A X S U M S T O O N E
                             is the 16 keys in index order (k0 = S ... k15 = E)
  a letter's WIDTH          = a_ij x the measure (exact at the line's centre)
  a letter's OUTLINES       = floor(16 a_ij): one ring per full 1/16 it receives
  crimson / green           = a_ij >= 1/16 / a_ij < 1/16  (complementary pair)
  a line's HEIGHT           = k (4 - H_i bits), strictly: the more peaked the query,
                             the taller its line
  BETWEEN line centres      = the query slerps to the next one and the widths
                             are the REAL softmax of that intermediate query,
                             so the letter edges are continuous curves: one
                             displacement field (the attention CDF of the
                             query at height y) warps every glyph on the sheet.

Because every row sums to one, every line is justified: the first letter's
left edge and the last letter's right edge are pinned to the measure on all
22 lines and everywhere between them. If the softmax leaked mass, the right
margin would be ragged. That is the plate's one joke: attention is typesetting.

The numbers are the plate's truth (encoding.md §4a): seed 7, d = 16, Q_i, K_j
~ unit N(0, I), five keys tilted toward Q11, T bisected to a_max = 0.190.

CANON: Psychedelic (Wes Wilson / Moscoso), declared flat.
LINEAGE: Wes Wilson, Fillmore poster for The Association (1966): lettering
         stretched to fill a field, one warp through every letter.
Contract: attention_weaving_wildcard(rng, bounds, colors=3)
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine.kit import _pen, _poly, _stroke_text, _text_width

Bounds = Tuple[float, float, float, float]
Poly = List[Tuple[float, float]]

# pen slots — palette: black, crimson, forestgreen
BLACK, HOT, COLD = 0, 1, 2

PHRASE = "SOFTMAXSUMSTOONE"          # key j <-> PHRASE[j]

LAST_STATS: dict = {}


# ---------------------------------------------------------------------------
# the numbers
# ---------------------------------------------------------------------------
def _softmax(s, temp):
    import numpy as np
    z = s / temp
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def _numbers(rng: SeededRNG, n_q: int = 22, n_k: int = 16, d: int = 16):
    import numpy as np

    def _unit(n: int = d):
        v = [rng.gauss() for _ in range(n)]
        s = math.sqrt(sum(t * t for t in v)) or 1.0
        return [t / s for t in v]

    Qv = [_unit() for _ in range(n_q)]
    Kv = [_unit() for _ in range(n_k)]
    Vv = [_unit(38)[:d] for _ in range(n_k)]      # drawn to keep the stream identical
    P = n_q // 2
    for j, w_ in ((5, 0.90), (11, 0.70), (2, 0.54), (14, 0.40), (8, 0.30)):
        Kv[j] = [w_ * Qv[P][t] + math.sqrt(1 - w_ * w_) * Kv[j][t] for t in range(d)]
        n_ = math.sqrt(sum(t * t for t in Kv[j])) or 1.0
        Kv[j] = [t / n_ for t in Kv[j]]
    Q = np.array(Qv)
    K = np.array(Kv)
    V = np.array(Vv)
    S = math.sqrt(d) * Q @ K.T
    lo, hi = 0.05, 30.0
    for _ in range(64):
        mid = 0.5 * (lo + hi)
        if _softmax(S[P], mid).max() > 0.190:
            lo = mid
        else:
            hi = mid
    T = 0.5 * (lo + hi)
    A = _softmax(S, T)
    return Q, K, V, S, T, A, P


def _seriate(A, pin: int, pin_pos: int) -> List[int]:
    """Row order minimising the L1 jump between neighbouring rows (so the warp
    between lines is gentle), with query `pin` fixed at slot `pin_pos`.
    Greedy from both sides of the pin, then 2-opt on the free slots."""
    import numpy as np
    n = A.shape[0]
    D = np.abs(A[:, None, :] - A[None, :, :]).sum(-1)
    free = set(range(n)) - {pin}
    order = [pin]
    # grow alternately up and down from the pin
    up, dn = pin_pos, n - 1 - pin_pos
    while free:
        if up > 0 and (dn == 0 or up >= dn):
            end = order[0]
            j = min(free, key=lambda k: D[end, k])
            order.insert(0, j)
            up -= 1
        else:
            end = order[-1]
            j = min(free, key=lambda k: D[end, k])
            order.append(j)
            dn -= 1
        free.discard(j)

    def cost(o):
        return sum(D[o[i], o[i + 1]] for i in range(len(o) - 1))

    best = cost(order)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for k in range(i + 1, n):
                if i <= pin_pos <= k:
                    continue           # never move the pin
                o = order[:i] + order[i:k + 1][::-1] + order[k + 1:]
                c = cost(o)
                if c < best - 1e-12:
                    order, best, improved = o, c, True
    return order


# ---------------------------------------------------------------------------
# bespoke psychedelic letterforms, unit box (u right, v up), fill the box
# ---------------------------------------------------------------------------
def _sarc(cx, cy, rx, ry, a0, a1, e=2.6, n=40) -> Poly:
    out = []
    for k in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * k / n)
        c, s = math.cos(a), math.sin(a)
        out.append((cx + rx * math.copysign(abs(c) ** (2 / e), c),
                    cy + ry * math.copysign(abs(s) ** (2 / e), s)))
    return out


def _glyph(ch: str) -> List[Poly]:
    if ch == "O":
        return [_sarc(0.5, 0.5, 0.5, 0.5, 90, 450, n=96)]
    if ch == "S":
        top = _sarc(0.5, 0.75, 0.5, 0.25, 20, 270, n=48)
        bot = _sarc(0.5, 0.25, 0.5, 0.25, 90, -160, n=48)
        return [top + bot[1:]]
    if ch == "F":
        return [[(1, 1), (0, 1), (0, 0)], [(0, 0.55), (0.78, 0.55)]]
    if ch == "T":
        return [[(0, 1), (1, 1)], [(0.5, 1), (0.5, 0)]]
    if ch == "M":
        return [[(0, 0), (0, 1), (0.5, 0.32), (1, 1), (1, 0)]]
    if ch == "A":
        arch = _sarc(0.5, 0.5, 0.5, 0.5, 180, 0, n=48)
        return [[(0, 0)] + arch + [(1, 0)], [(0, 0.40), (1, 0.40)]]
    if ch == "X":
        return [[(0, 0), (1, 1)], [(0, 1), (1, 0)]]
    if ch == "U":
        cup = _sarc(0.5, 0.5, 0.5, 0.5, 180, 360, n=48)
        return [[(0, 1)] + cup + [(1, 1)]]
    if ch == "N":
        return [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    if ch == "E":
        return [[(1, 1), (0, 1), (0, 0), (1, 0)], [(0, 0.5), (0.8, 0.5)]]
    raise KeyError(ch)


def _plen(poly: Poly) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:]))


def _densify(poly: Poly, step: float) -> Poly:
    out = [poly[0]]
    for (xa, ya), (xb, yb) in zip(poly, poly[1:]):
        L = math.hypot(xb - xa, yb - ya)
        n = max(1, int(math.ceil(L / step)))
        for k in range(1, n + 1):
            out.append((xa + (xb - xa) * k / n, ya + (yb - ya) * k / n))
    return out


def _rdp(poly: Poly, tol: float) -> Poly:
    """Ramer-Douglas-Peucker, iterative."""
    import numpy as np
    if len(poly) < 3:
        return list(poly)
    P = np.asarray(poly, float)
    keep = np.zeros(len(P), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(P) - 1)]
    while stack:
        i, k = stack.pop()
        if k <= i + 1:
            continue
        a, b = P[i], P[k]
        ab = b - a
        L = math.hypot(ab[0], ab[1])
        seg = P[i + 1:k]
        if L < 1e-12:
            dd = np.hypot(seg[:, 0] - a[0], seg[:, 1] - a[1])
        else:
            dd = np.abs(ab[0] * (seg[:, 1] - a[1]) - ab[1] * (seg[:, 0] - a[0])) / L
        m = int(np.argmax(dd))
        if dd[m] > tol:
            j = i + 1 + m
            keep[j] = True
            stack += [(i, j), (j, k)]
    return [tuple(map(float, q)) for q in P[keep]]


def _seg_dist(X, Y, segs):
    """min distance from grid points to a set of segments (numpy)."""
    import numpy as np
    best = np.full(X.shape, np.inf)
    P = np.stack([X.ravel(), Y.ravel()], 1)
    for (ax, ay, bx, by) in segs:
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        if L2 < 1e-12:
            d = np.hypot(P[:, 0] - ax, P[:, 1] - ay)
        else:
            t = ((P[:, 0] - ax) * dx + (P[:, 1] - ay) * dy) / L2
            t = np.clip(t, 0.0, 1.0)
            d = np.hypot(P[:, 0] - (ax + t * dx), P[:, 1] - (ay + t * dy))
        best = np.minimum(best, d.reshape(X.shape))
    return best


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------
def attention_weaving_wildcard(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    pitch: float = 0.9,          # ring pitch (mm), > pen tip
    hero_slot: int = 7,          # which line (from the top) carries query 11
    measure: float = 158.0,      # the justified measure (mm), flush left
    block_bottom: float = 22.0,  # mm above the bottom margin where the block ends
    uni_gap: float = 4.0,        # paper between the block and the uniform key line
    uni_h: float = 8.0,          # the uniform key line's glyph height
    gutter: float = 10.0,        # measure -> caption column
    h0: float = 0.0,             # line-height floor (mm); 0 = height strictly prop. to bits
    ease: bool = True,           # smoothstep the slerp parameter between line centres
    CLR: float = 0.5,            # ink-to-cell-edge clearance along the edge normal (mm)
    lead: float = 0.55,          # vertical paper between a line's ink and its edge
    side: float = 0.05,          # side bearing as a fraction of the cell width
    feed: int = 2200,
) -> List[GCodeCommand]:
    import numpy as np
    import contourpy

    x0, y0, x1, y1 = bounds
    W = measure                       # THE ONE: the measure every line is set to
    xm1 = x0 + W
    k_blk = _pen(BLACK, colors)
    k_hot = _pen(HOT, colors)
    k_cold = _pen(COLD, colors)
    LAST_STATS.clear()

    Q, K, V, S, T, A, P = _numbers(rng)
    n_q, n_k = A.shape
    d = Q.shape[1]
    Hbits = -(A * np.log2(A)).sum(1)
    info = math.log2(n_k) - Hbits                     # bits of focus per query

    order = _seriate(A, P, hero_slot)                  # top -> bottom
    # ---- line heights: h0 + k * bits, filling the block exactly -------------
    top, bot = y1, y0 + block_bottom
    Hblk = top - bot
    kbits = (Hblk - n_q * h0) / float(info.sum())
    heights = [h0 + kbits * info[q] for q in order]
    edges_y = [top]
    for h in heights:
        edges_y.append(edges_y[-1] - h)
    centres = [0.5 * (edges_y[r] + edges_y[r + 1]) for r in range(n_q)]

    # ---- the warp: query at height y (slerp between line centres) ---------
    def q_at(y: float):
        if y >= centres[0]:
            return Q[order[0]]
        if y <= centres[-1]:
            return Q[order[-1]]
        r = 0
        while not (centres[r] >= y >= centres[r + 1]):
            r += 1
        f = (centres[r] - y) / (centres[r] - centres[r + 1])
        if ease:
            f = f * f * (3.0 - 2.0 * f)
        a, b = Q[order[r]], Q[order[r + 1]]
        om = math.acos(max(-1.0, min(1.0, float(a @ b))))
        if om < 1e-9:
            return a
        return (math.sin((1 - f) * om) * a + math.sin(f * om) * b) / math.sin(om)

    ys = np.arange(bot - 1.0, top + 1.0, 0.05)
    ys = np.unique(np.concatenate([ys, np.array(centres)]))   # centres sit ON the grid
    qs = np.array([q_at(float(y)) for y in ys])
    Ays = _softmax(math.sqrt(d) * qs @ K.T, T)            # (ny, 16), rows sum to 1
    cum = np.concatenate([np.zeros((len(ys), 1)), np.cumsum(Ays, 1)], 1)
    bx = x0 + W * cum                                      # (ny, 17) letter edges

    # measured: at each line centre the cell edges ARE that query's cumulative row
    _cerr = 0.0
    for r_, q_ in enumerate(order):
        exact = x0 + W * np.concatenate([[0.0], np.cumsum(A[q_])])
        got = np.array([np.interp(centres[r_], ys, bx[:, j_]) for j_ in range(n_k + 1)])
        _cerr = max(_cerr, float(np.abs(got - exact).max()))
    LAST_STATS["centre_edge_err_mm"] = _cerr
    LAST_STATS["right_edge_err_mm"] = float(np.abs(bx[:, -1] - xm1).max())

    # ---- letter cells, eroded so ink never crosses a slanted edge -----------
    # Every ink point of letter j at height y keeps >= CLR (measured along the
    # normal of the local cell edge) from that edge. A ring of radius R around
    # the skeleton reaches R above/below the skeleton point, so the skeleton's
    # cell at y is the tightest cell over the window y +- R.
    dy_s = 0.05                                            # nominal grid step
    slope = np.gradient(bx, ys, axis=0)                  # dx/dy of each edge
    sec = np.sqrt(1.0 + slope * slope)
    Lc = bx[:, :-1] + CLR * sec[:, :-1]
    Rc = bx[:, 1:] - CLR * sec[:, 1:]
    Lc[:, 0] = x0                                          # flush to the measure
    Rc[:, -1] = xm1

    _ero: Dict[float, Tuple[object, object]] = {}

    def eroded(R: float):
        if R in _ero:
            return _ero[R]
        k = int(math.ceil(R / dy_s)) + 1        # +1: the inserted centre samples
        Lm, Rm = Lc.copy(), Rc.copy()
        for o in range(1, k + 1):
            Lm[o:] = np.maximum(Lm[o:], Lc[:-o])
            Lm[:-o] = np.maximum(Lm[:-o], Lc[o:])
            Rm[o:] = np.minimum(Rm[o:], Rc[:-o])
            Rm[:-o] = np.minimum(Rm[:-o], Rc[o:])
        _ero[R] = (Lm, Rm)
        return _ero[R]

    # ---- letters -----------------------------------------------------------
    hot_polys: List[Poly] = []
    cold_polys: List[Poly] = []
    owner_hot: List[int] = []
    owner_cold: List[int] = []
    rings_per: Dict[int, int] = {}
    min_glyph_h = 1e9
    min_glyph_w = 1e9
    uid = 0
    for r, q in enumerate(order):
        yt, yb = edges_y[r], edges_y[r + 1]
        for j in range(n_k):
            uid += 1
            a = float(A[q, j])
            n = int(math.floor(a * n_k + 1e-12))          # one ring per 1/16
            rings_per[n] = rings_per.get(n, 0) + 1
            R = n * pitch
            pv = R + lead
            gy0, gy1 = yb + pv, yt - pv
            min_glyph_h = min(min_glyph_h, gy1 - gy0)
            Lm, Rm = eroded(R)
            Lj, Rj = Lm[:, j], Rm[:, j]

            def warp(u: float, v: float) -> Tuple[float, float]:
                y = gy0 + v * (gy1 - gy0)
                L = float(np.interp(y, ys, Lj)) + R
                Rr = float(np.interp(y, ys, Rj)) - R
                w = Rr - L
                sb = side * max(0.0, w) if 0 < j < n_k - 1 else 0.0
                if j == 0:
                    sb_l, sb_r = 0.0, side * max(0.0, w)
                elif j == n_k - 1:
                    sb_l, sb_r = side * max(0.0, w), 0.0
                else:
                    sb_l = sb_r = sb
                # where the eroded cell has closed (w < 0) the letter is squeezed
                # out of existence at this height: flag it, the stroke breaks
                return (L + sb_l + u * max(0.0, w - sb_l - sb_r), y, w >= 0.0)

            wmid = float(np.interp(0.5 * (gy0 + gy1), ys, Rj - Lj)) - 2 * R
            min_glyph_w = min(min_glyph_w, wmid)
            skel = []
            for st in _glyph(PHRASE[j]):
                st = _densify(st, 0.02)
                # adaptive: where the warp is steep a 0.02 step in the glyph
                # can jump millimetres on paper, and the chord would cut across
                # the cell edge. Bisect until every physical step <= 0.25 mm.
                pts = [warp(*st[0])]
                for (ua, va), (ub, vb) in zip(st, st[1:]):
                    stack = [((ua, va), (ub, vb), pts[-1], warp(ub, vb), 0)]
                    seq = []
                    while stack:
                        (pa_u, pb_u, pa, pb, dep) = stack.pop()
                        if dep < 10 and math.hypot(pb[0] - pa[0], pb[1] - pa[1]) > 0.25:
                            mu = ((pa_u[0] + pb_u[0]) / 2, (pa_u[1] + pb_u[1]) / 2)
                            pm = warp(*mu)
                            stack.append((mu, pb_u, pm, pb, dep + 1))
                            stack.append((pa_u, mu, pa, pm, dep + 1))
                        else:
                            seq.append(pb)
                    pts.extend(seq)
                run: Poly = []
                for (px_, py_, ok_) in pts:
                    if ok_:
                        run.append((px_, py_))
                    else:
                        if len(run) >= 2:
                            skel.append(run)
                        run = []
                if len(run) >= 2:
                    skel.append(run)
                skel = [s_ for s_ in skel if _plen(s_) >= 0.6]
            if n == 0:
                cold_polys.extend(skel)
                owner_cold.extend([uid] * len(skel))
                continue
            # rings: level sets of the distance to the warped skeleton at
            # m * pitch (m = 1..n), plus the skeleton itself
            hot_polys.extend(skel)
            owner_hot.extend([uid] * len(skel))
            xs_ = [p[0] for s_ in skel for p in s_]
            ys_ = [p[1] for s_ in skel for p in s_]
            pad = R + 1.0
            res = 0.08
            gx = np.arange(min(xs_) - pad, max(xs_) + pad, res)
            gyy = np.arange(min(ys_) - pad, max(ys_) + pad, res)
            X, Y = np.meshgrid(gx, gyy)
            segs = []
            for s_ in skel:
                s2 = s_[::6] + [s_[-1]]
                for pa, pb in zip(s2, s2[1:]):
                    segs.append((pa[0], pa[1], pb[0], pb[1]))
            D = _seg_dist(X, Y, segs)
            gen = contourpy.contour_generator(x=gx, y=gyy, z=D, line_type="Separate")
            for m in range(1, n + 1):
                for ln in gen.lines(m * pitch):
                    if len(ln) >= 3:
                        hot_polys.append([(float(p[0]), float(p[1])) for p in ln])
                        owner_hot.append(uid)

    # ---- measured: closest approach between inks of DIFFERENT letters -------
    def _min_between(polys, owners, step=0.25):
        pts, own = [], []
        for pl, o in zip(polys, owners):
            for q_ in _densify(pl, step):
                pts.append(q_)
                own.append(o)
        P_ = np.asarray(pts)
        O_ = np.asarray(own)
        cell = 1.5
        keys = np.floor(P_ / cell).astype(int)
        buckets: Dict[Tuple[int, int], List[int]] = {}
        for idx, (kx, ky) in enumerate(keys):
            buckets.setdefault((int(kx), int(ky)), []).append(idx)
        best, where = 1e9, None
        for (kx, ky), ids in buckets.items():
            near = []
            for ox in (-1, 0, 1):
                for oy in (-1, 0, 1):
                    near += buckets.get((kx + ox, ky + oy), [])
            a_ = np.asarray(ids)
            b_ = np.asarray(near)
            D_ = np.hypot(P_[a_, None, 0] - P_[None, b_, 0], P_[a_, None, 1] - P_[None, b_, 1])
            D_[O_[a_][:, None] == O_[b_][None, :]] = 1e9
            m_ = float(D_.min())
            if m_ < best:
                best = m_
                ii = np.unravel_index(int(np.argmin(D_)), D_.shape)
                where = (tuple(round(float(v), 1) for v in P_[a_[ii[0]]]),
                         tuple(round(float(v), 1) for v in P_[b_[ii[1]]]),
                         int(O_[a_[ii[0]]]), int(O_[b_[ii[1]]]))
        return best, where

    out: List[GCodeCommand] = []
    hot_polys = [_rdp(p, 0.025) for p in hot_polys]
    cold_polys = [_rdp(p, 0.025) for p in cold_polys]
    for p in hot_polys:
        out += _poly(p, color=k_hot, f=feed)
    for p in cold_polys:
        out += _poly(p, color=k_cold, f=feed)

    # ---- the uniform line: the 16 keys at exactly 1/16 each (H = 4 bits) -----
    # By the height rule a query that knew nothing would get ZERO height, so
    # this line is not one of the 22: it is the key, set in black on the text
    # layer, where every letter's cell is the same 1/16 of the measure.
    u_top, u_bot = bot - uni_gap, bot - uni_gap - uni_h
    cw = W / n_k
    for j in range(n_k):
        l_ = x0 + j * cw + (0.0 if j == 0 else side * cw)
        r_ = x0 + (j + 1) * cw - (0.0 if j == n_k - 1 else side * cw)
        for st in _glyph(PHRASE[j]):
            st = _densify(st, 0.05)
            out += _poly(_rdp([(l_ + u * (r_ - l_), u_bot + v * (u_top - u_bot))
                               for (u, v) in st], 0.02), color=k_blk, f=feed)
    # key indices under the uniform line
    for j in range(n_k):
        lab = "k%d" % j
        cx_ = x0 + (j + 0.5) * cw
        out += _stroke_text(lab, cx_ - 0.5 * _text_width(lab, 1.8), u_bot - 4.2, 1.8,
                            color=k_blk)

    # ---- caption ---------------------------------------------------------------
    fh = 2.2
    n1 = rings_per.get(1, 0)
    n2 = rings_per.get(2, 0)
    n3 = rings_per.get(3, 0)
    nh = n1 + n2 + n3
    order_txt = " ".join(str(q) for q in order)
    head = "SUMS TO ONE"
    lines = [
        "EACH LINE IS ONE QUERY'S",
        "SOFTMAX ROW.  EACH LETTER",
        "IS A KEY, k0...k15 BELOW,",
        "AND ITS CELL IS a OF THE",
        "LINE.  EVERY ROW SUMS TO 1",
        "SO EVERY LINE IS JUSTIFIED.",
        "",
        "ONE OUTLINE PER WHOLE 1/16.",
        "CRIMSON a ≥ 1/16  %d/%d" % (nh, n_q * n_k),
        "LINE HEIGHT %.1f MM/BIT" % kbits,
        "OF 4 - H.  BETWEEN LINES",
        "THE QUERY SLERPS.",
        "",
        "A = SOFTMAX(QKᵀ/T)  T %.3f" % T,
        "22 × 16  d 16  SEED %s" % getattr(rng, "seed", "?"),
        "LINES TOP DOWN = QUERIES",
    ]
    ot = [str(q) for q in order]
    row_, rows_ = "", []
    for t_ in ot:
        cand = (row_ + " " + t_).strip()
        if len(cand) > 26:
            rows_.append(row_)
            row_ = t_
        else:
            row_ = cand
    rows_.append(row_)
    lines += rows_ + ["BELOW: EVERY a = 1/16"]
    fh = 2.0
    lead_c = 3.5
    xc = xm1 + gutter
    yy = u_bot - 4.2 + lead_c * (len(lines) - 1)
    LAST_STATS["caption_top"] = yy + 4.0 + 5.0
    out += _stroke_text(head, xc, yy + 4.0 + 2.2, 5.0, color=k_blk)
    for t in lines:
        if t:
            out += _stroke_text(t, xc, yy, fh, color=k_blk)
        yy -= lead_c
    LAST_STATS["caption_right"] = max(xc + _text_width(t, fh) for t in lines)
    LAST_STATS["head_right"] = xc + _text_width(head, 5.0)

    LAST_STATS.update(
        T=T, order=order, heights=heights, kbits=kbits, rings=rings_per,
        min_glyph_h=min_glyph_h, min_glyph_w=min_glyph_w,
        min_between_letters=_min_between(hot_polys + cold_polys, owner_hot + owner_cold),
        row_sum_err=float(np.abs(A.sum(1) - 1).max()),
        warp_sum_err=float(np.abs(Ays.sum(1) - 1).max()),
    )
    return out
