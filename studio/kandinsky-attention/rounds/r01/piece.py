"""ATTENTION AS RESONANCE — the corrected recreation.

Kandinsky/Bauhaus colour-block idiom, but the mechanism underneath is real
scaled dot-product attention taken from GPT-2 small (layer 4, head 7), not a
decorative stand-in.  See NOTES.md for the audit of the reference's technical
errors and what was drawn instead.

The abstract ORDER is APPORTIONMENT: every query is handed exactly one unit of
attention and must spend all of it.  On this sheet that unit is EIGHT RINGS per
grid row and ONE BAR LENGTH per output row.  Rows are all equally loud; only the
spending differs.  The first query has nothing to spend it on but itself, and
the empty upper-right triangle is what no query is allowed to buy.
"""

from __future__ import annotations

import math
import os
from typing import List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.engine.kit import (
    circle,
    fat_outline,
    fill_disc,
    fill_rect,
    giant_type,
    _dot,
    _poly,
    _stroke_text,
    _text_width,
)

Bounds = Tuple[float, float, float, float]

# ---------------------------------------------------------------------------
# pens.  Render with --palette black,crimson,dodgerblue,goldenrod,forestgreen
# ---------------------------------------------------------------------------
BLACK, RED, BLUE, GOLD, GREEN = 0, 1, 2, 3, 4

# ---------------------------------------------------------------------------
# THE DATA.  GPT-2 small, layer 4, head 7, first 8 query rows.
#
# Source: ~/.promptplot/attn_gpt2.npz, attn[4, 7], shape (12, 12, 15, 15),
# produced by scripts/extract_gpt2_attention.py on
#   "The pen plotter drew a black hole while the transformer watched itself think."
#
# The 8x8 crop is EXACT, not a sample: GPT-2 is a causal decoder, so row q has
# support only on keys j <= q.  Rows 0..7 therefore live entirely inside columns
# 0..7 and each still sums to 1.  Verified against the file: the upper triangle
# of every one of the 144 heads is exactly 0.0, and every row sums to 1.
#
# Head 4/7 was chosen because it shows both behaviours a reader needs to see at
# once: a hard attention sink on k0 (rows 0-2) and a self/previous-token
# diagonal (rows 3-7).  The literal below is the fallback when the npz is
# absent; the numbers are byte-identical to the file.
# ---------------------------------------------------------------------------
LAYER, HEAD, N = 4, 7, 8
D_K = 64  # 768 model dim / 12 heads -> sqrt(d_k) = 8

A_LITERAL: List[List[float]] = [
    [1.000000, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.959080, 0.040920, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.589180, 0.108296, 0.302524, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.286658, 0.016626, 0.119473, 0.577242, 0.0, 0.0, 0.0, 0.0],
    [0.037658, 0.000593, 0.044546, 0.218612, 0.698591, 0.0, 0.0, 0.0],
    [0.129849, 0.006410, 0.013317, 0.015959, 0.364844, 0.469622, 0.0, 0.0],
    [0.126464, 0.028717, 0.003263, 0.004431, 0.055571, 0.229968, 0.551587, 0.0],
    [0.296590, 0.014573, 0.010744, 0.014312, 0.048976, 0.023164, 0.104275, 0.487365],
]


def _load_attention() -> List[List[float]]:
    """Real GPT-2 attention from disk, falling back to the embedded literal."""
    path = os.path.expanduser("~/.promptplot/attn_gpt2.npz")
    try:
        import numpy as np

        M = np.load(path)["attn"][LAYER, HEAD, :N, :N].astype(float)
        rows = [[float(v) for v in M[i]] for i in range(N)]
        # a row must still sum to 1 after the causal crop, or the crop was wrong
        for r in rows:
            assert abs(sum(r) - 1.0) < 1e-4
        return rows
    except Exception:
        return [list(r) for r in A_LITERAL]


# ---------------------------------------------------------------------------
# exact numbers derived from A
# ---------------------------------------------------------------------------
RINGS_PER_ROW = 8  # the ration: one unit of attention == 8 rings


def _apportion(w: Sequence[float], total: int) -> List[int]:
    """Largest-remainder apportionment so the counts sum to ``total`` EXACTLY.

    Rounding each weight independently does not sum to the budget, and a grid
    whose rows carry different amounts of ink is exactly the reference's error
    (attention that does not sum to one).  Hamilton's method fixes the row sum
    by construction.
    """
    raw = [x * total for x in w]
    base = [int(math.floor(v)) for v in raw]
    short = total - sum(base)
    order = sorted(range(len(w)), key=lambda k: (-(raw[k] - base[k]), k))
    for k in order[:short]:
        base[k] += 1
    return base


def _entropy_bits(row: Sequence[float]) -> float:
    return float(sum(-p * math.log2(p) for p in row if p > 0.0))


# ---------------------------------------------------------------------------
# tiny drawing helpers (design space; everything is transformed at the end)
# ---------------------------------------------------------------------------


def _rect(x0, y0, x1, y1, pen, f=2200) -> List[GCodeCommand]:
    return _poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], color=pen, f=f)


def _seg(x0, y0, x1, y1, pen, f=2200) -> List[GCodeCommand]:
    return _poly([(x0, y0), (x1, y1)], color=pen, f=f)


def _dotted_seg(x0, y0, x1, y1, pen, on=1.2, off=1.4, f=2200) -> List[GCodeCommand]:
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1e-6:
        return []
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    out: List[GCodeCommand] = []
    t = 0.0
    while t < L:
        t2 = min(L, t + on)
        out += _poly([(x0 + ux * t, y0 + uy * t), (x0 + ux * t2, y0 + uy * t2)], color=pen, f=f)
        t = t2 + off
    return out


def _text(s, x, y, h, pen, spaced=False, f=2400) -> List[GCodeCommand]:
    if spaced:
        s = " ".join(s)
    return _stroke_text(s, x, y, h, color=pen, f=f)


def _tw(s, h, spaced=False) -> float:
    return _text_width(" ".join(s) if spaced else s, h)


# ---------------------------------------------------------------------------
# THE EIGHT VALUE TEXTURES.
# Kandinsky's flat colour planes have no pen equivalent, so each value row v_j
# gets its own LINE-FILL, and the texture is that row's identity.  Z = AV is
# then literally drawn: an output bar is the textures mixed in the softmax
# proportions.  Pitches are all >= 0.9 mm.
# ---------------------------------------------------------------------------
TEXTURE_NAMES = [
    "horizontal", "vertical", "rise 45", "fall 45",
    "cross", "dot lattice", "dashed rows", "wave",
]


def _clip_h(y, x0, x1):
    return (x0, y, x1, y)


def _texture(x0, y0, x1, y1, kind, pen, f=2400) -> List[GCodeCommand]:
    """Line-fill a rectangle with texture ``kind`` (0..7)."""
    out: List[GCodeCommand] = []
    w, h = x1 - x0, y1 - y0
    if w <= 0.05 or h <= 0.05:
        return out
    k = kind % 8
    if k == 0:  # horizontal
        y = y0 + 0.5
        while y <= y1 - 0.4:
            out += _poly([(x0, y), (x1, y)], color=pen, f=f)
            y += 1.0
    elif k == 1:  # vertical
        x = x0 + 0.5
        while x <= x1 - 0.3:
            out += _poly([(x, y0), (x, y1)], color=pen, f=f)
            x += 1.0
    elif k in (2, 3, 4):  # diagonals / cross
        pitch = 1.15 if k != 4 else 2.0
        dirs = [1] if k == 2 else ([-1] if k == 3 else [1, -1])
        for d in dirs:
            c = -h - 2.0
            while c <= w + h + 2.0:
                # line: y = d*(x - x0) + y0 + c  -> clip to the rect
                pts = []
                for xx in (x0, x1):
                    yy = d * (xx - x0) + y0 + c
                    pts.append((xx, yy))
                (ax, ay), (bx, by) = pts
                # clip in y
                if ay > by:
                    (ax, ay), (bx, by) = (bx, by), (ax, ay)
                if by < y0 or ay > y1:
                    c += pitch
                    continue
                if ay < y0:
                    t = (y0 - ay) / (by - ay)
                    ax, ay = ax + (bx - ax) * t, y0
                if by > y1:
                    t = (y1 - ay) / (by - ay)
                    bx, by = ax + (bx - ax) * t, y1
                if math.hypot(bx - ax, by - ay) > 0.25:
                    out += _poly([(ax, ay), (bx, by)], color=pen, f=f)
                c += pitch
    elif k == 5:  # dot lattice
        step = 1.5
        y = y0 + 0.75
        row = 0
        while y <= y1 - 0.3:
            x = x0 + 0.5 + (0.75 if row % 2 else 0.0)
            while x <= x1 - 0.2:
                out += circle(x, y, 0.3, pen=pen, f=f, n=8)
                x += step
            y += step
            row += 1
    elif k == 6:  # dashed rows
        y = y0 + 0.6
        row = 0
        while y <= y1 - 0.4:
            x = x0 + (0.9 if row % 2 else 0.0)
            while x < x1 - 0.2:
                out += _poly([(x, y), (min(x1, x + 1.3), y)], color=pen, f=f)
                x += 2.3
            y += 1.15
            row += 1
    else:  # wave
        y = y0 + 0.6
        while y <= y1 - 0.4:
            pts = []
            steps = max(4, int(w / 0.45))
            for m in range(steps + 1):
                xx = x0 + w * m / steps
                pts.append((xx, y + 0.34 * math.sin(2 * math.pi * (xx - x0) / 3.2)))
            out += _poly(pts, color=pen, f=f)
            y += 1.15
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------

# design sheet: 240 x 300 mm, live area 14..226 x 14..286
SX0, SY0, SW, SH = 10.0, 10.0, 220.0, 280.0

GX0, GY1, CELL = 42.0, 250.0, 19.0          # grid: top-left corner, cell pitch
GX1, GY0 = GX0 + N * CELL, GY1 - N * CELL   # 42..194, 98..250
PITCH = 0.9                                 # ring pitch, mm
BAR_X0, BAR_L = 66.0, 110.0                 # the unit bar
BAR_TOP, BAR_DY, BAR_H = 72.0, 7.3, 5.0
MIN_SEG = 1.8                               # a segment narrower than this gets no texture
MIN_TICK = 0.6                              # ...and narrower than this, no boundary tick


def _cell_box(i: int, j: int) -> Tuple[float, float, float, float]:
    x0 = GX0 + j * CELL
    y1 = GY1 - i * CELL
    return x0, y1 - CELL, x0 + CELL, y1


def kandinsky_attention(rng, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    A = _load_attention()
    ent = [_entropy_bits(r) for r in A]
    colmass = [sum(A[i][j] for i in range(N)) for j in range(N)]
    argmax = [max(range(N), key=lambda j: A[i][j]) for i in range(N)]
    shares = [_apportion(A[i], RINGS_PER_ROW) for i in range(N)]

    def P(idx: int) -> Optional[int]:
        return (idx % colors) if colors and colors > 1 else None

    K_, R_, B_, G_, Z_ = P(BLACK), P(RED), P(BLUE), P(GOLD), P(GREEN)
    out: List[GCodeCommand] = []

    # -- title band -------------------------------------------------------
    out += giant_type("ATTENTION AS RESONANCE", 14.0, 278.0, 5.0,
                      pen=K_, weight=0.55, tip=0.5, spaced=True)
    out += fat_outline([(14.0, 272.0), (226.0, 272.0)], width=1.3, pen=K_, tip=0.5)

    # -- K axis: one disc per key, AREA = the mass that key receives ------
    # sum over the 8 query rows of A[i][j].  Total over all columns is exactly
    # N, so the discs partition eight units of received attention.  k0 is the
    # attention sink and it looks like one.
    mmax = max(colmass)
    for j in range(N):
        cx = GX0 + (j + 0.5) * CELL
        r = 6.4 * math.sqrt(colmass[j] / mmax)
        if r > 0.6:
            out += fill_disc(cx, 259.0, r, spacing=0.75, pen=B_)
        else:
            out += circle(cx, 259.0, max(r, 0.45), pen=B_)
        lbl = f"k{j}"
        out += _text(lbl, cx - _tw(lbl, 2.0) / 2.0, 267.5, 2.0, B_)
    out += giant_type("K", 200.0, 253.0, 10.0, pen=B_, weight=0.7, tip=0.5)
    out += _text("received mass", 200.0, 248.0, 2.0, B_)

    # -- Q axis: one bar per query, LENGTH = H(A_i) in bits ---------------
    out += giant_type("Q", 16.0, 253.0, 10.0, pen=R_, weight=0.7, tip=0.5)
    out += _text("bits of doubt", 16.0, 248.0, 2.0, R_)
    for b in (1, 2):
        x = 40.0 - b * 10.0
        out += _dotted_seg(x, GY0 - 1.0, x, GY1, K_, on=0.8, off=2.2)
    out += _text("2", 20.0 - 1.2, 94.0, 2.0, K_)
    out += _text("1", 30.0 - 1.2, 94.0, 2.0, K_)
    out += _text("0", 40.0 - 1.2, 94.0, 2.0, K_)
    out += _text("H bits", 20.0, 89.0, 2.2, K_)
    for i in range(N):
        cy = GY1 - (i + 0.5) * CELL
        lbl = f"q{i}"
        out += _text(lbl, 14.0, cy - 1.0, 2.4, R_)
        L = 10.0 * ent[i]
        if L > 0.4:
            out += fill_rect(40.0 - L, cy - 1.4, 40.0, cy + 1.4, spacing=0.62, pen=R_)
        else:
            out += _poly([(40.0, cy - 1.6), (40.0, cy + 1.6)], color=R_, f=2200)

    # -- the grid, clipped to the causal region ---------------------------
    for k in range(N + 1):  # horizontal rules
        y = GY1 - k * CELL
        x_end = GX0 + min(k + 1, N) * CELL
        out += _poly([(GX0, y), (x_end, y)], color=K_, f=2200)
    for j in range(N + 1):  # vertical rules
        x = GX0 + j * CELL
        y_top = GY1 - max(j - 1, 0) * CELL
        out += _poly([(x, y_top), (x, GY0)], color=K_, f=2200)

    # lattice nodes, inside the causal region only
    for k in range(N + 1):
        y = GY1 - k * CELL
        for j in range(min(k + 1, N) + 1):
            out += fill_disc(GX0 + j * CELL, y, 0.62, spacing=0.5, pen=K_)

    # -- the mask staircase: the heavy diagonal, and it is a STAIRCASE ----
    stair: List[Tuple[float, float]] = [(GX0 + CELL, GY1)]
    for i in range(N):
        x = GX0 + (i + 1) * CELL
        y_bot = GY1 - (i + 1) * CELL
        stair.append((x, y_bot))
        if i < N - 1:
            stair.append((x + CELL, y_bot))
    out += fat_outline(stair, width=1.4, pen=K_, tip=0.5)

    # -- the resonance cells ---------------------------------------------
    # ring count  = that cell's apportioned share of the row's EIGHT rings
    # centre disc = the exact weight, area-proportional, so sub-quantum
    #               weights are still present on the sheet
    for i in range(N):
        for j in range(i + 1):
            x0, y0, x1, y1 = _cell_box(i, j)
            cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
            w = A[i][j]
            n_rings = shares[i][j]
            rd = 1.7 * math.sqrt(max(w, 0.0))
            if rd >= 0.42:
                out += fill_disc(cx, cy, rd, spacing=0.62, pen=K_)
            else:
                out += circle(cx, cy, 0.35, pen=K_, n=10)
            r = max(rd, 0.5) + PITCH
            for _ in range(n_rings):
                out += circle(cx, cy, r, pen=K_, n=max(28, int(r * 9)))
                r += PITCH

    # q0's score is unidentifiable: with one visible key softmax returns 1
    # whatever the score was.  Mark it.
    x0, y0, x1, y1 = _cell_box(0, 0)
    out += _poly([(x0 + 2.2, y0 + 2.2), (x1 - 2.2, y1 - 2.2)], color=K_, f=2200)
    out += _poly([(x0 + 2.2, y1 - 2.2), (x1 - 2.2, y0 + 2.2)], color=K_, f=2200)

    # -- the selection path: argmax of each row, in the query pen ---------
    for i in range(N):
        x0, y0, x1, y1 = _cell_box(i, argmax[i])
        out += fat_outline(
            [(x0 + 1.3, y0 + 1.3), (x1 - 1.3, y0 + 1.3), (x1 - 1.3, y1 - 1.3),
             (x0 + 1.3, y1 - 1.3), (x0 + 1.3, y0 + 1.3)],
            width=1.0, pen=R_, tip=0.5)

    # -- the void: label, mask law, and the unit ring ---------------------
    out += _text("S = QK", 100.0, 240.0, 4.0, K_)
    out += _text("T", 100.0 + _tw("S = QK", 4.0), 242.6, 2.4, K_)
    tx = 100.0 + _tw("S = QK", 4.0) + _tw("T", 2.4) + 1.4
    out += _text("/", tx, 240.0, 4.0, K_)
    out += _text("d", tx + _tw("/", 4.0) + 3.0, 240.0, 4.0, K_)
    out += _text("k", tx + _tw("/", 4.0) + 3.0 + _tw("d", 4.0), 238.6, 2.4, K_)
    out += _poly([(tx + _tw("/", 4.0) + 1.2, 240.4),
                  (tx + _tw("/", 4.0) + 2.4, 239.0),
                  (tx + _tw("/", 4.0) + 3.0, 244.2),
                  (tx + _tw("/", 4.0) + 3.0 + _tw("d", 4.0) + 2.2, 244.2)],
                 color=K_, f=2200)
    out += _text("j > i", 100.0, 232.0, 3.0, K_)
    out += _text("masked to minus infinity", 100.0, 226.0, 2.2, K_)
    out += _text("every row : eight rings", 112.0, 218.0, 2.6, K_)
    out += _text("apportioned by weight", 112.0, 213.0, 2.6, K_)

    # the unit ring: circumference == one bar length.  Sectors are row q7.
    ur = BAR_L / (2.0 * math.pi)
    ucx, ucy = 150.0, 198.0
    acc = 0.0
    for j in range(N):
        w = A[7][j]
        if w <= 0.0:
            continue
        a0 = math.pi / 2.0 - 2.0 * math.pi * acc
        a1 = math.pi / 2.0 - 2.0 * math.pi * (acc + w)
        pts = []
        steps = max(3, int(abs(a1 - a0) * ur / 0.5))
        for m in range(steps + 1):
            a = a0 + (a1 - a0) * m / steps
            pts.append((ucx + ur * math.cos(a), ucy + ur * math.sin(a)))
        if j == argmax[7]:
            out += fat_outline(pts, width=1.2, pen=R_, tip=0.5)
        else:
            out += _poly(pts, color=K_, f=2200)
        out += _poly([(ucx + (ur - 2.4) * math.cos(a0), ucy + (ur - 2.4) * math.sin(a0)),
                      (ucx + (ur + 2.4) * math.cos(a0), ucy + (ur + 2.4) * math.sin(a0))],
                     color=K_, f=2200)
        acc += w
    out += _text("q7", ucx - 2.4, ucy - 1.0, 3.0, R_)
    out += _text("one unit", 132.0, 176.0, 2.4, K_)

    # -- V: eight values, eight textures ----------------------------------
    out += giant_type("V", 18.0, 78.0, 12.0, pen=G_, weight=0.75, tip=0.5)
    out += _text("eight values", 18.0, 72.0, 2.2, G_)
    out += _text("eight textures", 18.0, 68.0, 2.2, G_)
    sw_w, sw_h, sw_p = 13.0, 9.0, 15.0
    for j in range(N):
        sx = 66.0 + j * sw_p
        out += _texture(sx, 82.0, sx + sw_w, 82.0 + sw_h, j, G_)
        out += _rect(sx, 82.0, sx + sw_w, 82.0 + sw_h, G_)
        lbl = f"v{j}"
        out += _text(lbl, sx + sw_w / 2.0 - _tw(lbl, 2.2) / 2.0, 78.0, 2.2, G_)
    out += _text("A = softmax ( S )", 66.0, 93.5, 2.8, K_)
    out += _text("one distribution per query, not one curve per sheet",
                 66.0 + _tw("A = softmax ( S )", 2.8) + 4.0, 93.5, 2.2, K_)

    # -- Z = AV: eight unit bars, the textures mixed ----------------------
    out += giant_type("Z", 188.0, 40.0, 12.0, pen=Z_, weight=0.75, tip=0.5)
    out += _text("= AV", 200.0, 42.0, 3.4, Z_)
    out += _text("one row", 188.0, 34.0, 2.2, Z_)
    out += _text("per query", 188.0, 30.0, 2.2, Z_)
    for i in range(N):
        yt = BAR_TOP - i * BAR_DY
        yb = yt - BAR_H
        lbl = f"z{i}"
        out += _text(lbl, 52.0, yt - BAR_H + 1.2, 2.4, Z_)
        acc = 0.0
        for j in range(N):
            w = A[i][j]
            if w <= 0.0:
                continue
            xa = BAR_X0 + BAR_L * acc
            xb = BAR_X0 + BAR_L * (acc + w)
            if xb - xa >= MIN_SEG:
                out += _texture(xa + 0.25, yb + 0.25, xb - 0.25, yt - 0.25, j, G_)
            if acc > 0.0 and (xb - xa) >= MIN_TICK:
                out += _poly([(xa, yb), (xa, yt)], color=Z_, f=2200)
            acc += w
        out += _rect(BAR_X0, yb, BAR_X0 + BAR_L, yt, Z_)
    # every bar is the same length.  say why.
    out += _poly([(BAR_X0, 14.6), (BAR_X0 + BAR_L, 14.6)], color=K_, f=2200)
    out += _poly([(BAR_X0, 13.4), (BAR_X0, 15.8)], color=K_, f=2200)
    out += _poly([(BAR_X0 + BAR_L, 13.4), (BAR_X0 + BAR_L, 15.8)], color=K_, f=2200)
    out += _text("one unit of attention . every bar is this long", BAR_X0, 17.4, 2.2, K_)

    # -- provenance footer ------------------------------------------------
    for k, line in enumerate([
        "gpt-2 small",
        f"layer {LAYER} head {HEAD}",
        f"d k {D_K}   root d k 8",
        f"n {N} queries {N} keys",
    ]):
        out += _text(line, 188.0, 24.0 - k * 4.2, 2.2, K_)

    # -- fit the design sheet into the real drawable area -----------------
    bx0, by0, bx1, by1 = bounds
    s = min((bx1 - bx0) / SW, (by1 - by0) / SH)
    ox = bx0 + ((bx1 - bx0) - SW * s) / 2.0 - SX0 * s
    oy = by0 + ((by1 - by0) - SH * s) / 2.0 - SY0 * s
    if abs(s - 1.0) > 1e-9 or abs(ox) > 1e-9 or abs(oy) > 1e-9:
        for c in out:
            if c.x is not None:
                c.x = round(ox + c.x * s, 3)
            if c.y is not None:
                c.y = round(oy + c.y * s, 3)
    return out
