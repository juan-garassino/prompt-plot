"""CNN — POOLING CASCADE, r01 (thesis: pooling-cascade, abstract).

The convolution drawn as its own geometry and nothing else.  Five square
lattices fall down the sheet as opaque cards in one shared axonometric basis:
the input (48 x 64 px) at the top, nearest the eye, and each pooled map below
it with the cell pitch doubled -- 1, 2, 4, 8, 16 input pixels.  Every lattice
covers the same image extent, so the halving lattice IS the depth; no layer is
named.

Every mark is a real number from ``net.py``: a fixed CNN (|Sobel| -> pool ->
Gabor-5 bank -> pool -> binomial -> pool -> centre-surround -> pool) run on ONE
real image -- the ink of the previous version of this plate.  A cell's tone is
its activation, drawn as DUTY at a fixed ring pitch (Vera Molnar's concentric
squares: a cell fills from its edge inward, one ring per step of activation;
pixel cells hold only one mark, inked with probability = darkness).

The only crimson is the receptive field: the single strongest top unit, and
the exact footprint it depends on in every map below it (interval propagation
through every conv halo and pool window, verified by perturbation), joined
corner to corner by dotted projection lines that pass behind the cards.

Pens: 0 black = lattices + card edges · 1 crimson = receptive field ·
2 black = type (own layer).
Entry point: ``pooling_cascade``.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import net  # noqa: E402  (sibling module: the real computation)

from promptplot.generative.engine.geometry import Complement, Intersect, Polygon, Union, clip  # noqa: E402
from promptplot.generative.generators import _dot, _poly, _stroke_text, _text_width  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402
from promptplot.models import GCodeCommand  # noqa: E402

Pt = Tuple[float, float]
BLACK, RED, TYPE = 0, 1, 2
F = 2200
RING = 0.9          # mm — perpendicular screen pitch between nested rings (>= 0.8 floor)
TICK = 0.55        # mm — half-length of a pixel tick (a line-screen dash along u)
THICK = 1.6        # mm — card thickness (front + right risers)
HALO = 0.95        # mm — keep-out either side of a crimson footprint line
CARD_PAD = 0.6     # mm — card edge sits this far outside the lattice
CELL_GAP = 0.95     # mm — minimum screen gap between neighbouring cells' outer rings


def pooling_cascade(rng: SeededRNG, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    pen = lambda k: (k % colors) if colors > 1 else None  # noqa: E731
    black, red, typ = pen(BLACK), pen(RED), pen(TYPE if colors > 2 else BLACK)

    # ---------------- the computation ----------------
    raw = net.load_input()
    P0 = np.clip(raw / max(1e-9, float(np.percentile(raw, 99))), 0.0, 1.0)
    Fm = net.forward(P0)
    maps = [Fm["P0"], Fm["P1"], Fm["P2"], Fm["P3"], Fm["P4"]]
    shapes = [m.shape for m in maps]
    top = tuple(int(i) for i in np.unravel_index(int(np.argmax(maps[4])), maps[4].shape))
    boxes = net.receptive_footprints(top, shapes)
    L = len(maps)
    NX, NY = shapes[0]

    # ---------------- one shared axonometric basis ----------------
    # plate (u, w): u = input column, w = NY - v (depth; w = 0 is the image's
    # bottom row, nearest the eye).  screen = origin + u*A + w*(B, C)
    A, B, C = 2.3, 0.36, 1.0
    V_LEN = math.hypot(B, C)
    du_ring = RING * V_LEN / (A * C)     # plate-units per ring on the v-parallel edges
    dv_ring = RING / C                   # plate-units per ring on the u-parallel edges
    gap_u = CELL_GAP * V_LEN / (A * C)
    gap_v = CELL_GAP / C

    plate_w = NX * A + NY * B
    plate_h = NY * C
    # vertical explosion: step between cards = base + k * (growth of the receptive
    # field across that stage, in input px) -> the air grows where the field grows
    rf, r_, j_ = [1], 1, 1                # receptive field (input px) after each pool
    for kind, k in net.STAGES:
        r_ += (k - 1) * j_
        if kind == "pool":
            j_ *= 2
            rf.append(r_)
    growth = [rf[i + 1] - rf[i] for i in range(L - 1)]
    # Cards drift RIGHT as they fall.  With the skew B, a card's side edges sit
    # (DX + s*B) mm right of the card above's: kept >= 12 mm so no two parallel
    # edges ever run a millimetre apart (v3's double-line fault at DX = -11).
    DX = 8.0
    top_y = y1 - 8.0
    total_steps = (top_y - plate_h) - (y0 + 30.0)
    s0 = 30.0
    k = (total_steps - s0 * (L - 1)) / sum(growth)
    steps = [s0 + k * g for g in growth]
    origins = []
    ox, oy = x0 + 15.0, top_y - plate_h
    for l in range(L):
        origins.append((ox, oy))
        if l < L - 1:
            ox += DX
            oy -= steps[l]

    def P(l, u, v):
        """plate l, input-pixel coords (u right, v down the image) -> screen."""
        w = NY - v
        ox_, oy_ = origins[l]
        return (ox_ + u * A + w * B, oy_ + w * C)

    pad_u, pad_v = CARD_PAD * V_LEN / (A * C), CARD_PAD / C

    def card(l):
        """card corners: front-left, front-right, back-right, back-left (padded)"""
        return (P(l, -pad_u, NY + pad_v), P(l, NX + pad_u, NY + pad_v),
                P(l, NX + pad_u, -pad_v), P(l, -pad_u, -pad_v))

    def silhouette(l):
        """the card seen from above: top face + the THICK-mm front/right faces"""
        a, b, c, d = card(l)
        return [(a[0], a[1] - THICK), (b[0], b[1] - THICK), (c[0], c[1] - THICK), c, d, a]

    polys = [Polygon(silhouette(l)) for l in range(L)]

    def occluder(l):
        return Union(*polys[:l]) if l > 0 else None

    out: List[GCodeCommand] = []

    # receptive-field footprints (input px) and a HALO mm keep-out band around
    # each outline: black marks and card edges stop short of the crimson line,
    # so the two pens never share or crowd a stroke
    def fp_rect(l):
        pitch = 2 ** l
        (i0, i1), (j0, j1) = boxes[l]
        u0, u1, v0, v1 = i0 * pitch, (i1 + 1) * pitch, j0 * pitch, (j1 + 1) * pitch
        # a footprint side lying on the image boundary is drawn ON the card edge
        # (and replaces it), so it never runs a fraction of a mm inside it
        u0 = -pad_u if u0 <= 0 else u0
        v0 = -pad_v if v0 <= 0 else v0
        u1 = NX + pad_u if u1 >= NX else u1
        v1 = NY + pad_v if v1 >= NY else v1
        return u0, u1, v0, v1

    def rect_poly(l, u0, u1, v0, v1):
        return Polygon([P(l, u0, v1), P(l, u1, v1), P(l, u1, v0), P(l, u0, v0)])

    hal_u, hal_v = HALO * V_LEN / (A * C), HALO / C
    halos = []
    for l in range(L):
        if l == L - 1:
            halos.append(None)
            continue
        u0, u1, v0, v1 = fp_rect(l)
        halos.append(Intersect(
            rect_poly(l, u0 - hal_u, u1 + hal_u, v0 - hal_v, v1 + hal_v),
            Complement(rect_poly(l, u0 + hal_u, u1 - hal_u, v0 + hal_v, v1 - hal_v)),
        ))

    # the dotted rails hang in the air between cards, in FRONT of every card
    # below their upper end: black marks under a rail give way by HALO mm
    def fp_corners(l):
        if l == L - 1:     # the top cell: rails land on its outermost ring
            pt = 2 ** l
            cu_, cv_ = (top[0] + 0.5) * pt, (top[1] + 0.5) * pt
            hu_, hv_ = pt / 2 - gap_u / 2, pt / 2 - gap_v / 2
            return [P(l, cu_ - hu_, cv_ + hv_), P(l, cu_ + hu_, cv_ + hv_),
                    P(l, cu_ + hu_, cv_ - hv_), P(l, cu_ - hu_, cv_ - hv_)]
        u0, u1, v0, v1 = fp_rect(l)
        return [P(l, u0, v1), P(l, u1, v1), P(l, u1, v0), P(l, u0, v0)]

    rail_quads: List[List[Polygon]] = [[] for _ in range(L)]
    for l in range(L - 1):
        for c in range(4):
            p_, q_ = fp_corners(l)[c], fp_corners(l + 1)[c]
            dx_, dy_ = q_[0] - p_[0], q_[1] - p_[1]
            n_ = math.hypot(dx_, dy_) or 1.0
            ox_, oy_ = -dy_ / n_ * HALO, dx_ / n_ * HALO
            quad = Polygon([(p_[0] + ox_, p_[1] + oy_), (q_[0] + ox_, q_[1] + oy_),
                            (q_[0] - ox_, q_[1] - oy_), (p_[0] - ox_, p_[1] - oy_)])
            for m in range(l + 1, L):
                rail_quads[m].append(quad)

    def keep_out(l):
        rs = ([halos[l]] if halos[l] is not None else []) + rail_quads[l]
        return Union(*rs) if rs else None

    def emit(pts: Sequence[Pt], l_occ: int, color, halo=None):
        occ = occluder(l_occ)
        if halo is not None:
            occ = halo if occ is None else Union(occ, halo)
        runs = [list(pts)] if occ is None else clip(list(pts), occ, keep="outside")
        for run in runs:
            if len(run) >= 2:
                out.extend(_poly(run, color=color, f=F))

    # ---------------- the cards ----------------
    for l in range(L):
        M = maps[l]
        pitch = 2 ** l
        hi = float(np.percentile(M, 99.5)) or 1.0
        T = np.clip(M / hi, 0.0, 1.0) ** (0.55 if l == 0 else 0.8)
        # card edge + its thickness: the front and right faces drop THICK mm
        ca, cb, cc, cd = card(l)
        emit([ca, cb, cc, cd, ca], l, black, keep_out(l))
        a0, a1, a2 = ca, cb, cc
        dn = lambda q: (q[0], q[1] - THICK)  # noqa: E731
        emit([a0, dn(a0), dn(a1), dn(a2), a2], l, black, keep_out(l))
        emit([a1, dn(a1)], l, black, keep_out(l))
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                is_top = l == L - 1 and (i, j) == top
                col = red if is_top else black
                t = 1.0 if is_top else float(T[i, j])
                cu, cv = (i + 0.5) * pitch, (j + 0.5) * pitch
                hu = pitch / 2 - gap_u / 2
                hv = pitch / 2 - gap_v / 2
                if l < L - 1 and hv > 0.15:
                    # a cell beside a crimson footprint line shrinks (whole rings,
                    # smaller) instead of being cut by the keep-out band
                    fu0, fu1, fv0, fv1 = fp_rect(l)
                    if fv0 - pitch < cv < fv1 + pitch:
                        for e in (fu0, fu1):
                            if abs(cu - e) < pitch:
                                hu = min(hu, abs(cu - e) - 1.08 * hal_u)
                    if fu0 - pitch < cu < fu1 + pitch:
                        for e in (fv0, fv1):
                            if abs(cv - e) < pitch:
                                hv = min(hv, abs(cv - e) - 1.08 * hal_v)
                    if hu <= 0.12 or hv <= 0.12:
                        continue
                if hv <= 0.15:          # pixel cells: one tick, inked with probability = tone
                    if rng.random() < t:
                        x, y = P(l, cu, cv)
                        occ = occluder(l)
                        hid = occ is not None and occ.contains(x, y)
                        near = halos[l] is not None and any(
                            halos[l].contains(x + dx_, y) for dx_ in (-TICK, 0.0, TICK))
                        if not hid and not near:
                            out.extend(_dot(x, y, TICK, color=col, f=F))
                    continue
                # Molnar square: rings grow from the cell centre outward, a fixed
                # screen pitch apart; activation sets HOW MANY (duty), never the pitch
                cap = int(min(hv / dv_ring, hu / du_ring))
                if cap <= 1:
                    n = 1 if rng.random() < t else 0
                    cap = max(cap, 1)
                else:
                    n = int(round(t * cap))
                for kk in range(n):
                    f_ = (kk + 1) / cap
                    a_, b_ = hu * f_, hv * f_
                    ring = [P(l, cu - a_, cv + b_), P(l, cu + a_, cv + b_), P(l, cu + a_, cv - b_),
                            P(l, cu - a_, cv - b_), P(l, cu - a_, cv + b_)]
                    ko = None if is_top else keep_out(l)
                    if ko is not None and clip(ring, ko, keep="inside"):
                        continue          # a ring the rail/footprint would cut is omitted whole
                    emit(ring, l, col)

    # ---------------- receptive field (crimson) ----------------
    corners_by_level = []
    for l in range(L):
        cs = fp_corners(l)
        corners_by_level.append(cs)
        if l < L - 1:
            emit(cs + [cs[0]], l, red)

    def dotted(p, q, l_occ):
        n = max(1, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 1.6))
        for s in range(n + 1):
            t = s / n
            x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            occ = Union(*polys[: l_occ + 1])
            if not occ.contains(x, y):
                out.extend(_dot(x, y, 0.3, color=red, f=F))

    for l in range(L - 1):
        for c in range(4):
            dotted(corners_by_level[l][c], corners_by_level[l + 1][c], l)

    # ---------------- type (own pen) ----------------
    # the only per-card text is the card's cell pitch in input pixels: a column
    # flush-left on the margin, each numeral on its card's front edge, its size
    # growing with the pitch it names
    tx = x0 + 6.0
    for l in range(L):
        fy = origins[l][1]
        h = 2.6 * (1.42 ** l)
        out.extend(_stroke_text(str(2 ** l), tx, fy, h, color=typ, f=F))
    # title in the quiet top-right wedge, flush-left on one axis
    bx = card(0)[2][0] + 5.0
    # CNN set at the height of the largest numeral: the two type masses answer
    # each other across the sheet's diagonal
    big = 2.6 * (1.42 ** (L - 1))
    out.extend(_stroke_text("CNN", bx, top_y - big + 1.0, big, color=typ, f=F))
    out.extend(_stroke_text("F R O M   P I X E L S", bx, top_y - big - 7.0, 1.8, color=typ, f=F))
    out.extend(_stroke_text("T O   M E A N I N G", bx, top_y - big - 11.5, 1.8, color=typ, f=F))
    # colophon under the last card, flush-left on the numeral column
    (i0, i1), (j0, j1) = boxes[0]
    lines = [
        "INPUT  THE PREVIOUS PLATE  %d X %d PX" % (NX, NY),
        "SOBEL 3  GABOR 5  BINOMIAL 3  CENTRE-SURROUND 3",
        "MAX-POOL 2 X 2  STRIDE 2",
        "RECEPTIVE FIELD %d X %d PX  (%d UNCLIPPED)" % (i1 - i0 + 1, j1 - j0 + 1, rf[-1]),
        "STRONGEST UNIT  WHERE THE OLD PLATE FLOODED",
    ]
    cy = origins[-1][1] - 10.0
    for ln in lines:
        out.extend(_stroke_text(ln, tx, cy, 1.5, color=typ, f=F))
        cy -= 4.2
    return out
