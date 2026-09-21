"""TRANSFORMER ATTENTION AS MASS REDISTRIBUTION — recreation, r01.

A faithful recreation of the reference plate (A4 portrait, cream):

    Q  five hatched density plots, upper-left, red
    K  five mirrored density plots, upper-right, blue
    A  the softmax matrix, dead centre, black
    V  five concentric-ring value discs, lower-left, ochre
    Z  Z = AV, lower-right, green

...with TWO elements deliberately redesigned (see NOTES.md):

  1. the softmax grid, which in the reference is a 5x5 dot lattice with
     decorative warped curves threading it — a mesh, not a matrix; and
  2. the Z vector, which in the reference is a green vortex of swept curves —
     an ornament, not a weighted sum.

Everything numeric here is real. Each Q / K distribution is a 3-component
Gaussian mixture; sampling it at d_k = 8 equally spaced points gives that
token's vector; the vectors are standardised (LayerNorm), S = QK^T / sqrt(d_k),
and A = softmax(S) row-wise. The SAME numbers drive the curves you see, the
matrix in the middle and the composition of Z. Nothing is drawn by eye.

Contract: mass_redistribution(rng, bounds, colors=5) -> list[GCodeCommand].
Nothing under promptplot/ is modified.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import (
    _dot,
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    circle,
    fill_disc,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# pen slots — index 0 red, 1 blue, 2 ochre, 3 green, 4 black
RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

N = 5  # tokens
D_K = 8  # key dimension — the sqrt(d_k) in the formula is this number

F_DRAW = 2200
F_FINE = 1800


# ---------------------------------------------------------------------------
# the numbers
# ---------------------------------------------------------------------------


def _mixture(rng: SeededRNG) -> Tuple[Tuple[float, float, float], ...]:
    """One token's density: a shoulder, a dominant mode, a trailing mode."""
    return (
        (rng.uniform(0.30, 0.52), rng.uniform(0.11, 0.24), rng.uniform(0.030, 0.048)),
        (1.0, rng.uniform(0.32, 0.50), rng.uniform(0.038, 0.062)),
        (rng.uniform(0.24, 0.58), rng.uniform(0.56, 0.74), rng.uniform(0.032, 0.052)),
    )


def _density(mix: Sequence[Tuple[float, float, float]], t: float) -> float:
    return sum(w * math.exp(-0.5 * ((t - mu) / sd) ** 2) for w, mu, sd in mix)


def _vector(mix: Sequence[Tuple[float, float, float]]) -> List[float]:
    """Sample the density at d_k points, then standardise (LayerNorm)."""
    v = [_density(mix, (m + 0.5) / D_K) for m in range(D_K)]
    mu = sum(v) / D_K
    sd = math.sqrt(sum((x - mu) ** 2 for x in v) / D_K) + 1e-9
    return [(x - mu) / sd for x in v]


def _softmax(row: Sequence[float]) -> List[float]:
    m = max(row)
    e = [math.exp(x - m) for x in row]
    s = sum(e)
    return [x / s for x in e]


def _attention(rng: SeededRNG):
    q_mix = [_mixture(rng) for _ in range(N)]
    k_mix = [_mixture(rng) for _ in range(N)]
    q = [_vector(m) for m in q_mix]
    k = [_vector(m) for m in k_mix]
    scores = [[sum(a * b for a, b in zip(qi, kj)) / math.sqrt(D_K) for kj in k] for qi in q]
    attn = [_softmax(r) for r in scores]
    return q_mix, k_mix, scores, attn


# ---------------------------------------------------------------------------
# curve helpers
# ---------------------------------------------------------------------------


def _bez(p0: Pt, c1: Pt, c2: Pt, p3: Pt, n: int = 38) -> List[Pt]:
    pts = []
    for s in range(n + 1):
        t = s / n
        u = 1.0 - t
        a, b, c, d = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
        pts.append(
            (
                a * p0[0] + b * c1[0] + c * c2[0] + d * p3[0],
                a * p0[1] + b * c1[1] + c * c2[1] + d * p3[1],
            )
        )
    return pts


def _arc(cx: float, cy: float, r: float, a0: float, a1: float, step: float = 0.7) -> List[Pt]:
    span = abs(a1 - a0)
    n = max(3, int(span * r / step))
    return [
        (cx + r * math.cos(a0 + (a1 - a0) * s / n), cy + r * math.sin(a0 + (a1 - a0) * s / n))
        for s in range(n + 1)
    ]


def _dotted_line(p0: Pt, p1: Pt, pen: Optional[int], dash: float = 0.7, gap: float = 1.6):
    """A dotted rule — the plate's background furniture idiom."""
    out: List[GCodeCommand] = []
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy)
    if L < 1e-6:
        return out
    ux, uy = dx / L, dy / L
    s = 0.0
    while s < L:
        e = min(L, s + dash)
        out += _poly(
            [(p0[0] + ux * s, p0[1] + uy * s), (p0[0] + ux * e, p0[1] + uy * e)],
            color=pen,
            f=F_FINE,
        )
        s = e + gap
    return out


def _dotted_ring(
    cx: float, cy: float, r: float, pen: Optional[int], bounds: Bounds,
    dash: float = 0.3, gap: float = 3.4,
) -> List[GCodeCommand]:
    """Faint background orbit — dots of a FIXED arc length, so a 80mm circle
    reads as dotted and not as a dashed rule (kit.dotted_circle divides the
    circumference, which coarsens badly at poster radii)."""
    out: List[GCodeCommand] = []
    step = dash + gap
    n = max(8, int(2 * math.pi * r / step))
    da = dash / r
    for k in range(n):
        a = 2 * math.pi * k / n
        p0 = (cx + r * math.cos(a), cy + r * math.sin(a))
        p1 = (cx + r * math.cos(a + da), cy + r * math.sin(a + da))
        if all(bounds[0] + 0.5 < p[0] < bounds[2] - 0.5
               and bounds[1] + 0.5 < p[1] < bounds[3] - 0.5 for p in (p0, p1)):
            out += _poly([p0, p1], color=pen, f=F_FINE)
    return out


def _mark(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """A small SOLID dot — two nested rings plus a chord, cheap and round."""
    out = circle(x, y, r, pen=pen, f=F_FINE, n=12)
    if r > 0.34:
        out += circle(x, y, r * 0.5, pen=pen, f=F_FINE, n=8)
    out += _poly([(x - r, y), (x + r, y)], color=pen, f=F_FINE)
    return out


def _spaced_text(text: str, x: float, y: float, h: float, pen: Optional[int]):
    return _stroke_text(_spaced(text), x, y, h, color=pen, f=F_FINE)


def _spaced_width(text: str, h: float) -> float:
    return _text_width(_spaced(text), h)


# ---------------------------------------------------------------------------
# Q / K — hatched density plots
# ---------------------------------------------------------------------------


def _distribution_plot(
    mix,
    x0: float,
    x1: float,
    base: float,
    amp: float,
    pen: Optional[int],
    dot_at_left: bool,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    n = 118
    peak = max(_density(mix, s / n) for s in range(n + 1)) or 1.0
    curve = [
        (x0 + (x1 - x0) * s / n, base + amp * _density(mix, s / n) / peak) for s in range(n + 1)
    ]

    # baseline
    out += _poly([(x0, base), (x1, base)], color=pen, f=F_DRAW)
    # vertical hatch under the density
    step = 0.9
    xx = x0 + step * 0.5
    while xx <= x1 - 0.2:
        t = (xx - x0) / (x1 - x0)
        h = amp * _density(mix, t) / peak
        if h > 0.45:
            out += _poly([(xx, base + 0.05), (xx, base + h)], color=pen, f=F_FINE)
        xx += step
    # the density itself, drawn over its own hatch
    out += _poly(curve, color=pen, f=F_DRAW)
    # terminal dot on the baseline
    dx = x0 if dot_at_left else x1
    out += fill_disc(dx, base, 1.15, spacing=0.4, pen=pen, f=F_FINE)
    return out


# ---------------------------------------------------------------------------
# V — concentric-ring value discs
# ---------------------------------------------------------------------------

# one texture per value vector; the SAME texture reappears inside Z, which is
# how the eye reads which v_j landed in which output.
V_STYLE = ("rings", "dots", "spokes", "dots", "rings")
V_PITCH = (1.55, 1.30, 0.0, 1.10, 1.75)


def _ring_texture(
    cx: float,
    cy: float,
    r_in: float,
    r_out: float,
    a0: float,
    a1: float,
    style: str,
    pitch: float,
    pen: Optional[int],
) -> List[GCodeCommand]:
    """The wedge/annulus texture of one value vector."""
    out: List[GCodeCommand] = []
    if style == "spokes":
        span = a1 - a0
        n = max(1, int(span / 0.165))
        for s in range(n + 1):
            a = a0 + span * s / n
            out += _poly(
                [
                    (cx + r_in * math.cos(a), cy + r_in * math.sin(a)),
                    (cx + r_out * math.cos(a), cy + r_out * math.sin(a)),
                ],
                color=pen,
                f=F_FINE,
            )
        return out

    rr = r_in + pitch
    while rr <= r_out - 0.15:
        if style == "dots":
            span = a1 - a0
            n = max(2, int(span * rr / 1.25))
            for s in range(n):
                a = a0 + span * (s + 0.5) / n
                out += _dot(cx + rr * math.cos(a), cy + rr * math.sin(a), 0.22, color=pen, f=F_FINE)
        else:
            out += _poly(_arc(cx, cy, rr, a0, a1), color=pen, f=F_FINE)
        rr += pitch
    return out


def _value_disc(cx: float, cy: float, r: float, j: int, pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += circle(cx, cy, r, pen=pen, f=F_DRAW, n=80)
    out += _ring_texture(
        cx, cy, 0.9, r, 0.0, 2 * math.pi, V_STYLE[j], V_PITCH[j] or 1.4, pen
    )
    out += fill_disc(cx, cy, 1.25, spacing=0.4, pen=pen, f=F_FINE)
    return out


# ---------------------------------------------------------------------------
# REDESIGN 1 — the softmax matrix
#
# The reference draws a 5x5 dot lattice with warped curves behind it: it reads
# as a mesh with decoration, and says nothing about what softmax DOES. Here the
# same rectangle is a real matrix plate, in two registers per row.
#
#   LOWER register — the matrix proper. Row i is a query, column j a key, and
#   the cell holds a hatched bar of height A[i,j]. A dotted rule at 1/n crosses
#   every row: a bar above it is mass TAKEN, a bar below it mass GIVEN UP.
#
#   UPPER register — the unit rail. The same width as the grid, cut at the
#   cumulative sums, so its five segments have widths A[i,0..4]. Every row's
#   rail is exactly the same length: that IS the row summing to one, drawn.
#
#   BETWEEN them — the transport map. A short line runs from each cell's centre
#   (where the key sits on the uniform lattice) to the centre of the segment
#   that key was given on the rail. The lines lean left and right by exactly the
#   amount softmax moved. Mass being reallocated from keys to queries is then
#   not a metaphor in the title, it is the slope of twenty-five line segments.
# ---------------------------------------------------------------------------


def _softmax_matrix(
    attn,
    gx0: float,
    gy0: float,
    gx1: float,
    gy1: float,
    pen: Optional[int],
):
    cw = (gx1 - gx0) / N
    lane = (gy1 - gy0) / N
    a_max = max(max(r) for r in attn)

    h_bar = 4.2  # bar height at A = a_max, mm
    d_hub = 5.0  # where the transport lines leave the uniform lattice
    d_rail = 9.0  # the unit rail
    tick = 1.3  # rail subdivision ticks, hanging DOWN off the rail

    out: List[GCodeCommand] = []
    left_ports: List[Pt] = []
    right_ports: List[Pt] = []
    exit_ports: List[Pt] = []
    bottom_ports: List[Pt] = []

    # dashed frame (kept from the reference)
    fx0, fy0, fx1, fy1 = gx0 - 3.0, gy0 - 3.0, gx1 + 3.0, gy1 + 3.0
    for a, b in (
        ((fx0, fy0), (fx1, fy0)),
        ((fx1, fy0), (fx1, fy1)),
        ((fx1, fy1), (fx0, fy1)),
        ((fx0, fy1), (fx0, fy0)),
    ):
        out += _dotted_line(a, b, pen, dash=1.5, gap=1.3)

    # key columns — the lattice that makes it read as a matrix
    for j in range(N + 1):
        x = gx0 + j * cw
        out += _dotted_line((x, gy0), (x, gy1), pen, dash=0.6, gap=1.5)
    for j in range(N):
        bottom_ports.append((gx0 + (j + 0.5) * cw, gy0))

    for i in range(N):
        base = gy1 - (i + 1) * lane + lane * 0.09
        out += _poly([(gx0, base), (gx1, base)], color=pen, f=F_FINE)

        # uniform share 1/N — the line mass is redistributed AROUND
        y_uni = base + h_bar * (1.0 / N) / a_max
        out += _dotted_line((gx0, y_uni), (gx1, y_uni), pen, dash=0.5, gap=1.0)

        # --- lower register: the cells ------------------------------------
        for j in range(N):
            a = attn[i][j]
            x_l = gx0 + j * cw + 0.8
            x_r = gx0 + (j + 1) * cw - 0.8
            h = h_bar * a / a_max
            h = max(h, 0.22)
            out += _poly(
                [(x_l, base), (x_l, base + h), (x_r, base + h), (x_r, base)],
                color=pen,
                f=F_DRAW,
            )
            xx = x_l + 0.8
            while xx < x_r - 0.2 and h > 0.5:
                out += _poly([(xx, base + 0.05), (xx, base + h - 0.05)], color=pen, f=F_FINE)
                xx += 0.8

        # --- upper register: the unit rail, cut at the cumulative sums -----
        y_rail = base + d_rail
        for dy in (0.0, 0.26):
            out += _poly([(gx0, y_rail + dy), (gx1, y_rail + dy)], color=pen, f=F_DRAW)
        cum = 0.0
        mids: List[float] = []
        edges = [gx0]
        for j in range(N):
            mids.append(gx0 + (cum + attn[i][j] * 0.5) * (gx1 - gx0))
            cum += attn[i][j]
            edges.append(gx0 + min(cum, 1.0) * (gx1 - gx0))
        for e in edges:
            for dx in (-0.11, 0.11):
                out += _poly([(e + dx, y_rail - tick), (e + dx, y_rail + 0.26)],
                             color=pen, f=F_DRAW)

        # --- between them: the transport map ------------------------------
        # from the key's seat on the UNIFORM lattice to the middle of the
        # segment softmax actually granted it. The lean of the line is the move.
        y_hub = base + d_hub
        for j in range(N):
            cell_cx = gx0 + (j + 0.5) * cw
            out += circle(cell_cx, y_hub, 0.42, pen=pen, f=F_FINE, n=10)
            out += _poly(
                [(cell_cx, y_hub + 0.42), (mids[j], y_rail - tick - 0.35)],
                color=pen,
                f=F_FINE,
            )
            out += _poly(
                [(mids[j] - 0.35, y_rail - tick - 0.35), (mids[j] + 0.35, y_rail - tick - 0.35)],
                color=pen,
                f=F_FINE,
            )

        # unity cap: the row's whole mass, leaving to become z_i
        out += _poly([(gx1, y_rail), (gx1 + 2.6, y_rail)], color=pen, f=F_DRAW)
        out += fill_disc(gx1 + 2.6, y_rail, 0.85, spacing=0.38, pen=pen, f=F_FINE)

        left_ports.append((gx0, base + lane * 0.30))
        right_ports.append((gx1, base + lane * 0.30))
        exit_ports.append((gx1 + 2.6, y_rail))

    return out, left_ports, right_ports, bottom_ports, exit_ports


# ---------------------------------------------------------------------------
# REDESIGN 2 — Z = AV
#
# The reference draws a green vortex: pretty, and unrelated to the arithmetic.
# Here each output z_i is a DISC OF UNIT AREA cut into five wedges. Wedge j
# subtends exactly A[i,j] * 2*pi and is filled with value vector v_j's OWN
# texture — the same rings / dots / spokes drawn in the V column. So each output
# is literally the five values, each present in proportion to its attention
# weight, and the wedges close the circle because the row sums to one. A small
# five-tick recipe bar under every disc repeats row i of the matrix, so a reader
# can walk a weight from the grid to the wedge that carries it.
# ---------------------------------------------------------------------------


def _output_disc(
    cx: float, cy: float, r: float, weights: Sequence[float], pen: Optional[int]
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += circle(cx, cy, r, pen=pen, f=F_DRAW, n=96)

    a = math.pi / 2.0  # start at twelve o'clock, run clockwise
    for j, w in enumerate(weights):
        span = w * 2 * math.pi
        a1 = a - span
        if span > 0.06:
            out += _poly(
                [(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], color=pen, f=F_FINE
            )
            out += _ring_texture(
                cx, cy, 1.6, r, min(a, a1), max(a, a1), V_STYLE[j], V_PITCH[j] or 1.4, pen
            )
        else:
            # a sliver of mass still gets its boundary, so nothing is lost
            out += _poly(
                [(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))], color=pen, f=F_FINE
            )
        a = a1
    out += fill_disc(cx, cy, 1.5, spacing=0.42, pen=pen, f=F_FINE)

    # recipe bar: row i of A, repeated under the disc
    bw = r * 1.15
    bx = cx - bw / 2.0
    by = cy - r - 3.4
    out += _poly([(bx, by), (bx + bw, by)], color=pen, f=F_FINE)
    a_ref = max(weights)
    for j, w in enumerate(weights):
        x = bx + bw * (j + 0.5) / N
        out += _poly([(x, by), (x, by + 3.0 * w / a_ref)], color=pen, f=F_FINE)
    return out


# ---------------------------------------------------------------------------
# the formula
# ---------------------------------------------------------------------------


def _formula(cx: float, cy: float, pen: Optional[int]) -> List[GCodeCommand]:
    """A = softmax( QK^T / sqrt(d_k) ), set as a real fraction."""
    h = 4.2
    hs = 2.5  # super/subscript
    out: List[GCodeCommand] = []

    w_a = _text_width("A", h)
    w_eq = _text_width("=", h)
    w_sm = _text_width("softmax", h * 0.95)
    num_w = _text_width("QK", h) + _text_width("T", hs)
    rad_w = 3.0
    den_w = rad_w + _text_width("d", h) + _text_width("k", hs) - 1.0
    bar_w = max(num_w, den_w) + 3.2
    paren_w = 2.6

    total = w_a + 2.0 + w_eq + 2.0 + w_sm + 1.6 + paren_w + 1.2 + bar_w + 1.2 + paren_w
    x = cx - total / 2.0

    out += _stroke_text("A", x, cy - h / 2.0, h, color=pen, f=F_FINE)
    x += w_a + 2.0
    out += _stroke_text("=", x, cy - h / 2.0, h, color=pen, f=F_FINE)
    x += w_eq + 2.0
    out += _stroke_text("softmax", x, cy - h * 0.30, h * 0.95, color=pen, f=F_FINE)
    x += w_sm + 1.6

    # tall parentheses as circular arcs
    ph = 7.4
    pr = ph / math.sin(0.62)
    out += _poly(
        _arc(x + paren_w + pr - 0.4, cy, pr, math.pi - 0.62, math.pi + 0.62), color=pen, f=F_FINE
    )
    x += paren_w + 1.2

    bar_y = cy
    out += _poly([(x, bar_y), (x + bar_w, bar_y)], color=pen, f=F_DRAW)

    # numerator QK^T
    nx = x + (bar_w - num_w) / 2.0
    out += _stroke_text("QK", nx, bar_y + 1.5, h, color=pen, f=F_FINE)
    out += _stroke_text(
        "T", nx + _text_width("QK", h) - 0.4, bar_y + 1.5 + h * 0.62, hs, color=pen, f=F_FINE
    )

    # denominator sqrt(d_k): radical + D + subscript K
    dx = x + (bar_w - den_w) / 2.0
    dy = bar_y - 1.6 - h
    w_d = _text_width("d", h)
    out += _poly(
        [(dx, dy + h * 0.45), (dx + 0.9, dy + h * 0.10), (dx + 1.9, dy + h * 1.14),
         (dx + rad_w + w_d - 0.4, dy + h * 1.14)],
        color=pen,
        f=F_FINE,
    )
    out += _stroke_text("d", dx + rad_w, dy, h, color=pen, f=F_FINE)
    out += _stroke_text(
        "k", dx + rad_w + w_d - 1.3, dy - 0.9, hs, color=pen, f=F_FINE
    )

    x += bar_w + 1.2
    out += _poly(_arc(x - pr + 0.4 + paren_w, cy, pr, -0.62, 0.62), color=pen, f=F_FINE)
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def mass_redistribution(
    rng: SeededRNG, bounds: Bounds, colors: int = 5
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    P_RED = _pen(RED, colors)
    P_BLU = _pen(BLUE, colors)
    P_OCH = _pen(OCHRE, colors)
    P_GRN = _pen(GREEN, colors)
    P_BLK = _pen(BLACK, colors)

    q_mix, k_mix, _scores, attn = _attention(rng)
    out: List[GCodeCommand] = []

    # ---------------- background furniture (drawn first, reads as behind) ----
    big = [
        (35.0, 250.0, 58.0),
        (168.0, 214.0, 62.0),
        (104.0, 152.0, 80.0),
        (46.0, 96.0, 56.0),
        (176.0, 58.0, 52.0),
        (112.0, 38.0, 62.0),
    ]
    for cx, cy, r in big:
        out += _dotted_ring(cx, cy, r, P_BLK, bounds)

    out += _dotted_line((106.0, y1 - 2.0), (106.0, y0 + 2.0), P_BLK, dash=0.4, gap=3.2)
    for vx, va, vb in ((43.0, 262.0, 178.0), (54.0, 252.0, 186.0), (158.0, 236.0, 150.0),
                       (174.0, 246.0, 120.0), (27.0, 142.0, 34.0), (197.0, 214.0, 96.0)):
        out += _dotted_line((vx, va), (vx, vb), P_BLK, dash=0.4, gap=3.2)
    out += _dotted_line((17.0, 27.5), (92.0, 27.5), P_BLK, dash=0.4, gap=3.0)

    for _ in range(18):
        px = rng.uniform(x0 + 4, x1 - 4)
        py = rng.uniform(y0 + 4, y1 - 4)
        if rng.random() < 0.28:
            out += circle(px, py, rng.uniform(0.7, 1.2), pen=P_BLK, f=F_FINE, n=16)
        else:
            out += _mark(px, py, rng.uniform(0.22, 0.45), P_BLK)

    # ---------------- type ---------------------------------------------------
    t1, t2 = "TRANSFORMER ATTENTION", "AS MASS REDISTRIBUTION"
    out += _spaced_text(t1, 198.0 - _spaced_width(t1, 3.5), 277.0, 3.5, P_BLK)
    out += _spaced_text(t2, 198.0 - _spaced_width(t2, 2.4), 270.0, 2.4, P_BLK)

    fx = 17.0
    for k, word in enumerate(("ALIGN", "TRANSPORT", "COMPOSE")):
        if k:
            out += _mark(fx + 1.4, 22.9, 0.42, P_BLK)
            fx += 4.6
        out += _spaced_text(word, fx, 22.0, 2.4, P_BLK)
        fx += _spaced_width(word, 2.4) + 1.2

    # ---------------- Q ------------------------------------------------------
    qx0, qx1, q_amp = 18.0, 54.0, 12.5
    q_base = [247.0, 232.0, 217.0, 202.0, 187.0]
    out += _stroke_text("Q", 18.5, 255.0, 9.5, color=P_RED, f=F_DRAW)
    for i in range(N):
        out += _distribution_plot(q_mix[i], qx0, qx1, q_base[i], q_amp, P_RED, True)

    # ---------------- K ------------------------------------------------------
    kx0, kx1, k_amp = 155.0, 191.0, 12.5
    k_base = [224.0, 207.0, 190.0, 173.0, 156.0]
    out += _stroke_text("K", 178.0, 239.0, 9.5, color=P_BLU, f=F_DRAW)
    for j in range(N):
        out += _distribution_plot(k_mix[j], kx0, kx1, k_base[j], k_amp, P_BLU, False)

    # ---------------- A (redesign 1) -----------------------------------------
    gx0, gy0, gx1, gy1 = 84.0, 160.0, 128.0, 214.0
    grid, l_ports, r_ports, b_ports, z_ports = _softmax_matrix(attn, gx0, gy0, gx1, gy1, P_BLK)
    out += grid
    cap = "ROW SUM = 1"
    out += _spaced_text(cap, 106.0 - _spaced_width(cap, 1.9) / 2.0, 218.5, 1.9, P_BLK)
    out += _formula(107.0, 234.0, P_BLK)

    # ---------------- V ------------------------------------------------------
    vx, v_r = 41.0, 6.6
    v_cy = [131.0, 113.0, 94.0, 75.0, 56.0]
    out += _stroke_text("V", 21.0, 139.5, 9.5, color=P_OCH, f=F_DRAW)
    out += _poly([(27.0, v_cy[0] + 4.0), (27.0, v_cy[-1] - 4.0)], color=P_OCH, f=F_FINE)
    for j in range(N):
        cy = v_cy[j]
        out += _value_disc(vx, cy, v_r, j, P_OCH)
        out += fill_disc(27.0, cy, 1.0, spacing=0.4, pen=P_OCH, f=F_FINE)
        out += _poly([(27.0, cy), (vx - v_r - 0.4, cy)], color=P_OCH, f=F_FINE)
        out += _poly([(vx + v_r + 0.4, cy), (52.0, cy)], color=P_OCH, f=F_FINE)
        out += _mark(52.0, cy, 0.62, P_OCH)

    # ---------------- Z (redesign 2) -----------------------------------------
    z_c = [(132.0, 96.0), (156.0, 88.0), (178.0, 76.0), (189.0, 51.0), (172.0, 29.0)]
    z_r = 9.8
    zl = "Z = AV"
    out += _stroke_text(zl, 153.0, 108.5, 7.4, color=P_GRN, f=F_DRAW)
    for i in range(N):
        out += _output_disc(z_c[i][0], z_c[i][1], z_r, attn[i], P_GRN)
    for _ in range(18):
        a = rng.uniform(0, 2 * math.pi)
        rr = rng.uniform(14.0, 30.0)
        k = rng.randint(0, N - 1)
        px, py = z_c[k][0] + rr * math.cos(a), z_c[k][1] + rr * math.sin(a)
        if x0 + 3 < px < x1 - 3 and y0 + 3 < py < y1 - 3:
            out += _mark(px, py, rng.uniform(0.32, 0.75), P_GRN)

    # ---------------- connector bundles --------------------------------------
    # red: every query distribution into every matrix row
    for i in range(N):
        src = (qx1, q_base[i])
        for t in range(N):
            tgt = l_ports[t]
            for s in range(2):
                o = (s - 0.5) * 1.5
                out += _poly(
                    _bez(
                        (src[0], src[1] + o * 0.8),
                        (src[0] + 13.0, src[1] + o * 2.4),
                        (tgt[0] - 13.0, tgt[1] + o * 2.0),
                        (tgt[0] - 0.4, tgt[1] + o),
                        34,
                    ),
                    color=P_RED,
                    f=F_FINE,
                )

    # blue: every key distribution into every matrix row
    for j in range(N):
        src = (kx0, k_base[j])
        for t in range(N):
            tgt = r_ports[t]
            for s in range(2):
                o = (s - 0.5) * 1.5
                out += _poly(
                    _bez(
                        (src[0], src[1] + o * 0.8),
                        (src[0] - 12.0, src[1] + o * 2.4),
                        (tgt[0] + 12.0, tgt[1] + o * 2.0),
                        (tgt[0] + 0.4, tgt[1] + o),
                        34,
                    ),
                    color=P_BLU,
                    f=F_FINE,
                )

    # ochre: value v_j into its own column port (columns ARE keys)
    for j in range(N):
        cy = v_cy[j]
        tgt = b_ports[j]
        for s in range(7):
            u = (s / 6.0 - 0.5)
            a = u * 1.15
            sp = (vx + (v_r + 1.2) * math.cos(a), cy + (v_r + 1.2) * math.sin(a))
            out += _poly(
                _bez(
                    sp,
                    (sp[0] + 34.0 + u * 6.0, sp[1] + u * 9.0),
                    (tgt[0] - 4.0 + u * 9.0, tgt[1] - 34.0 - u * 12.0),
                    (tgt[0] + u * 1.6, tgt[1] - 0.4),
                    40,
                ),
                color=P_OCH,
                f=F_FINE,
            )

    # green: the unity tick of row i sweeps out to output disc z_i
    for i in range(N):
        src = z_ports[i]
        cx, cy = z_c[i]
        for s in range(5):
            u = (s / 4.0 - 0.5)
            a = math.pi * 0.86 + u * 0.55
            tp = (cx + (z_r + 1.1) * math.cos(a), cy + (z_r + 1.1) * math.sin(a))
            out += _poly(
                _bez(
                    (src[0] + 0.6, src[1] + u * 1.1),
                    (src[0] + 6.5 + 2.9 * i + u * 2.2, src[1] - 23.0 - u * 6.0),
                    (tp[0] - 32.0 + u * 8.0, tp[1] + 33.0 + u * 10.0),
                    tp,
                    40,
                ),
                color=P_GRN,
                f=F_FINE,
            )

    return out
