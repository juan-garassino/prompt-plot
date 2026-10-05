"""GAN — NO FIXED POINT, woven.  Studio candidate, round 03 (two-players-interlaced).

parent: r01 (minimax_duel, the Dirac-GAN saddle).  This round drops the 3D mesh
and transposes the same exact run to INTERLACING.

Contract:  gan_darn(rng, bounds, colors=3) -> list[GCodeCommand]

WHAT IS COMPUTED (unchanged from r01, exact)
--------------------------------------------
The Dirac-GAN (Mescheder, Geiger, Nowozin 2018).  Real data delta_0, generator
delta_theta, discriminator D_psi(x) = psi*x, objective
V(theta, psi) = f(psi*theta) + f(0),  f(t) = -log(1 + e^-t),  f'(s) = sigmoid(-s).
Simultaneous gradient descent-ascent with one shared step h:

    theta <- theta - h * psi   * f'(s)      (generator descends)
    psi   <- psi   + h * theta * f'(s)      (discriminator ascends)

Continuous time conserves theta^2 + psi^2 (a closed orbit, the dotted circle);
the discrete step multiplies the radius by sqrt(1 + h^2 f'(s)^2) every
iteration, so the run provably spirals OUT and never reaches the Nash point
(0, 0).

THE ORDER: INTERLACING (a darn that never closes its hole)
--------------------------------------------------------
Every iteration is split into its two players' moves.  The GENERATOR's move is
horizontal (it changes theta) and is laid as WEFT; the DISCRIMINATOR's answer
is vertical (it changes psi) and is laid as WARP.  Each move is a tape of the
loom's threads on one fixed lattice (the loom's reed), covering exactly the
extent of that leg, so:

  * FLOAT LENGTH = GRADIENT MAGNITUDE.  A leg is h*|psi|*f'(s) long (weft) or
    h*|theta|*f'(s) (warp); where the players disagree the threads float long
    and bare, where f'(s) -> 0 (saturation) the legs shrink below one reed
    pitch and the cloth becomes a dense check of short floats.
  * OVER / UNDER = SIGN OF s = psi*theta, i.e. who is ahead at that crossing:
    s > 0 the discriminator is winning (V > f(0)) and the warp rides on top;
    s < 0 the generator is winning and the weft rides on top.
  * THE HOLE: the run starts on the circle r0 and only ever moves outward, so
    inside r0 no thread ever crosses — the equilibrium is bare paper, a hole
    the darn was woven around and can never mend.  No fixed point.

THE SHEET IS A WINDOW ON THE CLOTH
----------------------------------
The run is iterated until it can never touch the sheet again; laps that leave
the frame come back in at the corners.  At large radius the run stalls in the
s > 0 quadrants (f'(s) ~ e^-s, the saturating-loss vanishing gradient): of the
3642 steps that touch the sheet (seed 7), 3568 are that crawl and only 74 are
the big stairs where the generator is ahead.  A move whose tape would land
mostly off the sheet, or inside the title block, is not laid at all, so every
edge of cloth on the sheet is a clean crop or a whole tape, never a sliver.

LINEAGE: Anni Albers, *Red Meander* (1954) — a figure carried entirely by the
interlacing, the meander made of which thread is on top.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.kit import (
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    giant_type,
    giant_type_width,
    plus_mark,
)

Bounds = Tuple[float, float, float, float]


# ---------------------------------------------------------------------------
# the mathematics (exact)
# ---------------------------------------------------------------------------


def _sigmoid(t: float) -> float:
    if t >= 0.0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def dirac_gan_run(
    h: float, r_start: float, a0: float, stop, max_iters: int
) -> List[Tuple[float, float, float, float, float]]:
    """Simultaneous GDA on the Dirac-GAN.  Returns (theta, psi, dtheta, dpsi, g).
    ``stop(theta, psi)`` ends the run (here: the thread has left the sheet)."""
    th, ps = r_start * math.cos(a0), r_start * math.sin(a0)
    steps = []
    for _ in range(max_iters):
        g = _sigmoid(-(th * ps))
        dth = -h * ps * g
        dps = h * th * g
        steps.append((th, ps, dth, dps, g))
        th, ps = th + dth, ps + dps
        if stop(th, ps):
            break
    return steps


# ---------------------------------------------------------------------------
# interval helpers
# ---------------------------------------------------------------------------


def _union(iv: Sequence[Tuple[float, float]]) -> List[Tuple[float, float]]:
    out: List[Tuple[float, float]] = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _covers(iv: Sequence[Tuple[float, float]], x: float) -> bool:
    for a, b in iv:
        if a <= x <= b:
            return True
    return False


def _subtract(
    runs: Sequence[Tuple[float, float]], cuts: Sequence[Tuple[float, float]], min_len: float
) -> List[Tuple[float, float]]:
    out = []
    cuts = sorted(cuts)
    for a, b in runs:
        p = a
        for c0, c1 in cuts:
            if c1 <= p or c0 >= b:
                continue
            if c0 > p:
                out.append((p, c0))
            p = max(p, c1)
        if b > p:
            out.append((p, b))
    return [(a, b) for a, b in out if b - a >= min_len]


def _cloth_pieces(cand, bounds, pitch_mm: float, min_side: float, min_area: float) -> List[int]:
    """Indices of thread segments that belong to a woven piece with body.

    Segments are rasterised on a 1 mm grid, dilated by one reed pitch so the
    threads of one tape join, then 4-connected components are labelled; a piece
    whose bounding box is thinner than ``min_side`` mm or whose area is below
    ``min_area`` mm^2 is dropped whole."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    nx, ny = int(x1 - x0) + 3, int(y1 - y0) + 3
    grid = -np.ones((ny, nx), dtype=np.int64)
    occ = np.zeros((ny, nx), dtype=bool)
    rad = max(1, int(math.ceil(pitch_mm / 2.0 + 0.2)))
    seg_cells = []
    for q, (_pen, (ax_, ay_), (bx_, by_)) in enumerate(cand):
        n = max(2, int(math.hypot(bx_ - ax_, by_ - ay_)) + 2)
        cells = set()
        for t in range(n + 1):
            u = t / n
            cx = int(round(ax_ + (bx_ - ax_) * u - x0)) + 1
            cy = int(round(ay_ + (by_ - ay_) * u - y0)) + 1
            cells.add((min(max(cy, 0), ny - 1), min(max(cx, 0), nx - 1)))
        seg_cells.append(cells)
        for cy, cx in cells:
            occ[max(0, cy - rad):cy + rad + 1, max(0, cx - rad):cx + rad + 1] = True
    label = 0
    comp_ok = {}
    for sy in range(ny):
        for sx in range(nx):
            if not occ[sy, sx] or grid[sy, sx] >= 0:
                continue
            stack = [(sy, sx)]
            grid[sy, sx] = label
            mnx = mxx = sx
            mny = mxy = sy
            area = 0
            while stack:
                cy, cx = stack.pop()
                area += 1
                mnx, mxx, mny, mxy = min(mnx, cx), max(mxx, cx), min(mny, cy), max(mxy, cy)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = cy + dy, cx + dx
                    if 0 <= yy < ny and 0 <= xx < nx and occ[yy, xx] and grid[yy, xx] < 0:
                        grid[yy, xx] = label
                        stack.append((yy, xx))
            side = min(mxx - mnx, mxy - mny) + 1 - 2 * rad
            comp_ok[label] = side >= min_side and area >= min_area
            label += 1
    keep = []
    for q, cells in enumerate(seg_cells):
        cy, cx = next(iter(cells))
        if comp_ok.get(int(grid[cy, cx]), False):
            keep.append(q)
    return keep


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def gan_darn(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    step: float = 0.26,          # h — shared learning rate (r01's value)
    r_start: float = 0.74,       # initial ||(theta, psi)||: the hole's radius
    max_iters: int = 6000,
    tape: float = 0.26,          # width of one move's tape, world units
    pitch_mm: float = 1.8,       # the reed: thread spacing on paper
    gap_mm: float = 0.5,         # half-gap where a thread ducks under
    scale_mm: float = 36.0,      # mm per world unit
    centre: Tuple[float, float] = (0.56, 0.485),  # equilibrium, fraction of bounds
    title_h: float = 9.0,        # display type height, mm
    title_weight: float = 0.9,   # display type stroke weight, mm
    title_clear: float = 5.0,
    min_piece_mm: float = 5.0,
    min_on_frac: float = 0.45,   # a move whose tape is mostly off the sheet is not laid   # a cropped piece thinner than this is debris    # the cloth stops this far short of the title block
    feed: int = 2200,
) -> List[GCodeCommand]:
    """NO FIXED POINT — the Dirac-GAN's exact run of simultaneous gradient
    descent-ascent woven as a darn: generator moves are weft, discriminator
    answers are warp, over/under by sign(psi*theta), float by gradient size.
    The darn winds outward and leaves the equilibrium a hole of bare paper."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    TYPE = 0
    WEFT = 1 % max(1, colors)
    WARP = 2 % max(1, colors)

    # ---- paper frame: world (theta, psi) -> mm ---------------------------
    ex = x0 + centre[0] * W
    ey = y0 + centre[1] * H
    k = scale_mm

    # The run is followed until it can never touch the sheet again: the sheet
    # is a window on the cloth, and a lap that leaves it may come back in.
    m_tape = (tape / 2.0) * k + 1.0
    r_far = max(math.hypot(cx - ex, cy - ey) for cx in (x0, x1) for cy in (y0, y1))

    def gone(th: float, ps: float) -> bool:
        return k * math.hypot(th, ps) > r_far + m_tape

    def on_sheet(th: float, ps: float) -> bool:
        sx, sy = ex + k * th, ey + k * ps
        return x0 - m_tape <= sx <= x1 + m_tape and y0 - m_tape <= sy <= y1 + m_tape

    # ---- the title block is laid first: the cloth is woven around it ----
    TH_T, TH_S, TH_F = title_h, 2.4, 1.8
    xT = x0 + 1.0
    yT = y1 - TH_T                                   # title baseline
    ySub = yT - 4.2 - TH_S                           # tagline baseline
    title = "NO FIXED POINT"
    sub = _spaced("NEITHER PLAYER EVER ARRIVES")
    tw = giant_type_width(title, TH_T)
    title_box = (x0 - 1.0, ySub - title_clear,
                 max(xT + tw, xT + _text_width(sub, TH_S)) + title_clear, y1 + 1.0)
    halos = [title_box]

    a0 = 0.62 + rng.uniform(-0.55, 0.55)
    steps_all = dirac_gan_run(step, r_start, a0, gone, max_iters)
    # keep the moves whose own path (not just the tape's fringe) crosses the
    # sheet: a tape that only grazes the frame would leave a sliver, not a crop
    def leg_on(st) -> bool:
        th, ps, dth, dps, _g = st
        pts = [(th + dth * t, ps) for t in (0.0, 0.5, 1.0)]
        pts += [(th + dth, ps + dps * t) for t in (0.5, 1.0)]
        return any(x0 <= ex + k * a <= x1 and y0 <= ey + k * b <= y1 for a, b in pts)

    def under_title(st) -> bool:
        # a move whose tape would reach into the title block is not laid at all,
        # so the cloth stops on whole tapes there instead of on cut threads
        th, ps, dth, dps, _g = st
        bx0, by0, bx1, by1 = title_box
        m = (tape / 2.0) * k
        for a_, b_ in ((th, ps), (th + dth, ps), (th + dth, ps + dps)):
            sx, sy = ex + k * a_, ey + k * b_
            if bx0 - m <= sx <= bx1 + m and by0 - m <= sy <= by1 + m:
                return True
        return False

    steps = [st for st in steps_all if leg_on(st) and not under_title(st)]
    n_steps = len(steps_all)
    # the step at which the thread first leaves the sheet, and the last one seen
    n_edge = next(
        (n for n, (th, ps, *_r) in enumerate(steps_all)
         if not (x0 <= ex + k * th <= x1 and y0 <= ey + k * ps <= y1)),
        n_steps,
    )
    r_edge = math.hypot(*steps_all[min(n_edge, n_steps - 1)][:2])
    n_last = max(n for n, st in enumerate(steps_all)
                 if on_sheet(st[0], st[1]) or on_sheet(st[0] + st[2], st[1] + st[3]))
    r_last = math.hypot(steps_all[n_last][0] + steps_all[n_last][2],
                        steps_all[n_last][1] + steps_all[n_last][3])
    r_end = r_last

    def P(th: float, ps: float) -> Tuple[float, float]:
        return ex + k * th, ey + k * ps

    # the reed: lattice lines phase-locked to the equilibrium
    p = pitch_mm / k                           # pitch in world units
    half = tape / 2.0

    # ---- lay every move as a tape on the reed ---------------------------
    weft_iv: Dict[int, List[Tuple[float, float]]] = {}   # row j -> theta intervals
    warp_iv: Dict[int, List[Tuple[float, float]]] = {}   # col i -> psi intervals
    def on_frac(ta: float, tb: float, pa: float, pb: float) -> float:
        """Fraction of a tape rectangle (world units) that lands on the sheet."""
        X0, X1 = ex + k * ta, ex + k * tb
        Y0, Y1 = ey + k * pa, ey + k * pb
        full = max(1e-9, (X1 - X0) * (Y1 - Y0))
        cw = max(0.0, min(X1, x1) - max(X0, x0))
        ch = max(0.0, min(Y1, y1) - max(Y0, y0))
        return cw * ch / full

    n_crop_drop = 0
    for th, ps, dth, dps, g in steps:
        # generator's move: horizontal, at psi = ps, theta from th to th+dth
        a, b = sorted((th, th + dth))
        if on_frac(a - half, b + half, ps - half, ps + half) < min_on_frac:
            n_crop_drop += 1          # the frame shaved this tape to a sliver
            a = None
        for j in ([] if a is None else range(math.ceil((ps - half) / p), math.floor((ps + half) / p) + 1)):
            weft_iv.setdefault(j, []).append((a - half, b + half))
        # discriminator's answer: vertical, at theta = th+dth, psi from ps to ps+dps
        tc = th + dth
        a, b = sorted((ps, ps + dps))
        if on_frac(tc - half, tc + half, a - half, b + half) < min_on_frac:
            n_crop_drop += 1
            continue
        for i in range(math.ceil((tc - half) / p), math.floor((tc + half) / p) + 1):
            warp_iv.setdefault(i, []).append((a - half, b + half))
    weft_iv = {j: _union(v) for j, v in weft_iv.items()}
    warp_iv = {i: _union(v) for i, v in warp_iv.items()}

    # ---- crossings: over/under by sign(psi*theta) -----------------------
    g_w = gap_mm / k
    weft_cuts: Dict[int, List[Tuple[float, float]]] = {}
    warp_cuts: Dict[int, List[Tuple[float, float]]] = {}
    n_cross = n_warp_over = 0
    for i, piv in warp_iv.items():
        th_i = i * p
        for a, b in piv:
            for j in range(math.ceil(a / p), math.floor(b / p) + 1):
                if j not in weft_iv or not _covers(weft_iv[j], th_i):
                    continue
                ps_j = j * p
                n_cross += 1
                if th_i * ps_j > 0.0:           # discriminator ahead: warp on top
                    n_warp_over += 1
                    weft_cuts.setdefault(j, []).append((th_i - g_w, th_i + g_w))
                else:                           # generator ahead: weft on top
                    warp_cuts.setdefault(i, []).append((ps_j - g_w, ps_j + g_w))

    out: List[GCodeCommand] = []

    # ---- type layout first: its boxes are halos the cloth is cut around ---
    foot = [
        _spaced(f"{n_last + 1} STEPS   H {step:.2f}"),
        _spaced(f"R {r_start:.2f} TO {r_last:.2f}"),
        _spaced("PSI THETA > 0  D AHEAD  WARP ON TOP"),
    ]
    yF = [y0 + 1.0 + (TH_F + 2.6) * (len(foot) - 1 - q) for q in range(len(foot))]
    fw = max(_text_width(t, TH_F) for t in foot)
    halos.append((xT - 2.0, y0 - 1.0, xT + fw + 2.0, yF[0] + TH_F + 2.0))
    legend = [
        (WEFT, _spaced("WEFT  G  MOVES THETA"), True),
        (WARP, _spaced("WARP  D  MOVES PSI"), False),
    ]
    leg_w = max(_text_width(t, TH_F) for _p, t, _h in legend)
    xL = x1 - leg_w - 1.0
    halos.append((xL - 10.0, y0 - 1.0, x1 + 1.0, yF[0] + TH_F + 2.0))

    def cut_h(y: float, a: float, b: float) -> List[Tuple[float, float]]:
        cuts = [(hx0, hx1) for hx0, hy0, hx1, hy1 in halos if hy0 <= y <= hy1]
        a, b = max(a, x0), min(b, x1)
        return _subtract([(a, b)], cuts, 0.35) if b > a else []

    def cut_v(x: float, a: float, b: float) -> List[Tuple[float, float]]:
        cuts = [(hy0, hy1) for hx0, hy0, hx1, hy1 in halos if hx0 <= x <= hx1]
        a, b = max(a, y0), min(b, y1)
        return _subtract([(a, b)], cuts, 0.35) if b > a else []

    cand: List[Tuple[int, Tuple[float, float], Tuple[float, float]]] = []
    # weft (generator) — horizontal threads
    for j in sorted(weft_iv):
        y = ey + k * j * p
        if not (y0 <= y <= y1):
            continue
        for r, (a, b) in enumerate(_subtract(weft_iv[j], weft_cuts.get(j, []), 0.35 / k)):
            for ca, cb in cut_h(y, ex + k * a, ex + k * b):
                cand.append((WEFT, (ca, y), (cb, y)) if r % 2 == 0 else (WEFT, (cb, y), (ca, y)))
    # warp (discriminator) — vertical threads
    for i in sorted(warp_iv):
        x = ex + k * i * p
        if not (x0 <= x <= x1):
            continue
        for r, (a, b) in enumerate(_subtract(warp_iv[i], warp_cuts.get(i, []), 0.35 / k)):
            for ca, cb in cut_v(x, ey + k * a, ey + k * b):
                cand.append((WARP, (x, ca), (x, cb)) if r % 2 == 0 else (WARP, (x, cb), (x, ca)))

    # ---- crop hygiene: a piece of cloth the frame has shaved to a sliver ------
    # (one or two threads, or a scrap) is not a crop, it is debris.  Label the
    # woven pieces on a 1 mm grid and keep only those with real body.
    keep_idx = _cloth_pieces(cand, bounds, pitch_mm, min_side=min_piece_mm,
                             min_area=min_piece_mm ** 2 * 2.0)
    thread_segs: List[Tuple[float, float, float, float]] = []
    n_scrap = len(cand) - len(keep_idx)
    for q in keep_idx:
        pen, pa, pb = cand[q]
        out += _poly([pa, pb], color=pen, f=feed)
        thread_segs.append((min(pa[0], pb[0]), min(pa[1], pb[1]),
                            max(pa[0], pb[0]), max(pa[1], pb[1])))

    def near_thread(px: float, py: float, d: float) -> bool:
        for ax_, ay_, bx_, by_ in thread_segs:
            if ay_ == by_:
                if abs(py - ay_) < d and ax_ - d <= px <= bx_ + d:
                    return True
            elif abs(px - ax_) < d and ay_ - d <= py <= by_ + d:
                return True
        return False

    # ---- the orbit continuous time would keep forever: dotted, at r0 -------
    ndot = int(2 * math.pi * r_start * k / 1.6)
    for m in range(ndot):
        a = 2 * math.pi * m / ndot
        cx_, cy_ = P(r_start * math.cos(a), r_start * math.sin(a))
        if not near_thread(cx_, cy_, 0.9):
            out += _poly([(cx_ - 0.15, cy_), (cx_ + 0.15, cy_)], color=TYPE, f=feed)

    # ---- the equilibrium: a mark on bare paper ----------------------------
    out += plus_mark(ex, ey, s=1.6, pen=TYPE, f=feed)

    # ---- type (own pen) ------------------------------------------------------
    out += giant_type(title, xT, yT, TH_T, pen=TYPE, weight=title_weight, tip=0.3, f=feed)
    out += _stroke_text(sub, xT, ySub, TH_S, color=TYPE, f=feed)
    for t, yb in zip(foot, yF):
        out += _stroke_text(t, xT, yb, TH_F, color=TYPE, f=feed)
    # legend: a real swatch of each thread in its own pen, then its meaning
    for (pen, label, horiz), yb in zip(legend, yF[:2]):
        if horiz:
            for q in range(2):
                yy = yb + 0.3 + q * 1.2
                out += _poly([(xL - 9.0, yy), (xL - 3.0, yy)], color=pen, f=feed)
        else:
            for q in range(4):
                xx = xL - 9.0 + q * 1.6
                out += _poly([(xx, yb), (xx, yb + TH_F)], color=pen, f=feed)
        out += _stroke_text(label, xL, yb, TH_F, color=TYPE, f=feed)
    gan_darn.stats = dict(  # type: ignore[attr-defined]
        n_steps=n_steps, n_last=n_last, n_edge=n_edge, r_edge=r_edge, r_end=r_end, n_cross=n_cross, n_warp_over=n_warp_over,
        rows=len(weft_iv), cols=len(warp_iv), n_scrap=n_scrap, n_crop_drop=n_crop_drop,
    )
    return out
