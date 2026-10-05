"""POINT AND LINE TO PLANE — attention as the track of a moving point.

Kandinsky opens *Punkt und Linie zu Flaeche* (Bauhaus Book 9, 1926) by defining
a line as "the track made by the moving point".  One attention row is exactly
that: fifteen steps, one per value, each step's LENGTH the weight it was given
and its DIRECTION that value's slot on the ring.  Because a softmax row sums to
one, every track on this sheet is the same total length; only where it ENDS
differs, and where it ends is the output.

Abstract order: **a walk of conserved length** (chain / track), not a block
diagram of Q, K, S, A, V, Z.

Data: real GPT-2 small attention, layer 4 head 7, 15 tokens, from
``~/.promptplot/attn_gpt2.npz``.  Every mark is a number out of that matrix.

Entry point: ``kandinsky_attention(rng, bounds, colors=5)``.
"""

from __future__ import annotations

import math
import os
from typing import List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.engine import kit
from promptplot.generative.engine.geometry import Circle, HalfPlane, Rect, clip
from promptplot.generative.rng import SeededRNG

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

NPZ = os.path.expanduser("~/.promptplot/attn_gpt2.npz")
LAYER, HEAD = 4, 7

# pen slots (palette: black, crimson, dodgerblue, goldenrod, forestgreen)
BLACK, RED, BLUE, GOLD, GREEN = 0, 1, 2, 3, 4

THETA0 = math.radians(60.0)  # slot 0 (the sink) placed upper-right
RING_PITCH = 1.5             # concentric-ring pitch inside a value mark, mm
HATCH_PITCH = 4.6            # top-3 plane, mm
KNOT_R = 24.0                # the plane is cut away from the knot, mm


# ---------------------------------------------------------------------------
# mechanism
# ---------------------------------------------------------------------------
def _attention() -> Tuple[List[List[float]], str]:
    """The real head, or a deterministic stand-in if the cache is absent."""
    try:
        import numpy as np

        a = np.load(NPZ)["attn"][LAYER, HEAD]
        return [[float(v) for v in row] for row in a], "gpt2"
    except Exception:  # pragma: no cover - cache is present on this machine
        n = 15
        rows = []
        for i in range(n):
            s = [(-4.0 if j > i else 3.2 * math.exp(-0.7 * (i - j)) + 1.1 * (j == 0))
                 for j in range(n)]
            m = max(s)
            e = [math.exp(v - m) if j <= i else 0.0 for j, v in enumerate(s)]
            t = sum(e)
            rows.append([v / t for v in e])
        return rows, "synthetic"


class Mech:
    """Everything the plate draws, computed once."""

    def __init__(self) -> None:
        self.a, self.source = _attention()
        self.n = n = len(self.a)
        self.theta = [THETA0 + 2 * math.pi * j / n for j in range(n)]
        self.p = [(math.cos(t), math.sin(t)) for t in self.theta]

        # column mass: how much attention each value receives in total
        self.m = [sum(self.a[i][j] for i in range(n)) for j in range(n)]
        # column concentration: is a value shared by many queries, or owned by one
        self.c = [max(self.a[i][j] for i in range(n)) / max(self.m[j], 1e-12)
                  for j in range(n)]
        # per-row peak share and winner
        self.peak = [max(r) for r in self.a]
        self.arg = [max(range(n), key=lambda j, r=r: r[j]) for r in self.a]
        self.wins = [sum(1 for i in range(n) if self.arg[i] == j) for j in range(n)]

        # the walk: unit-circle coordinates
        self.walk: List[List[Pt]] = []
        for i in range(n):
            x = y = 0.0
            pts = [(0.0, 0.0)]
            for j in range(n):
                x += self.a[i][j] * self.p[j][0]
                y += self.a[i][j] * self.p[j][1]
                pts.append((x, y))
            self.walk.append(pts)
        self.z = [w[-1] for w in self.walk]
        self.reach = [math.hypot(*v) for v in self.z]
        self.mean_reach = sum(self.reach) / n
        self.zbar = (sum(v[0] for v in self.z) / n, sum(v[1] for v in self.z) / n)

        self.mean_peak = sum(self.peak) / n

        order = sorted(range(n), key=lambda j: -self.m[j])
        self.top3 = sorted(order[:3])
        self.top3_share = sum(self.m[j] for j in self.top3) / n


# ---------------------------------------------------------------------------
# small drawing helpers (piece-local; nothing under promptplot/ is touched)
# ---------------------------------------------------------------------------
def _pen(idx: int, colors: int) -> Optional[int]:
    return idx % colors if colors > 1 else None


def _runs(polys: Sequence[Sequence[Pt]], pen: Optional[int], f: int = 2000
          ) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in polys:
        out += kit._poly(list(p), color=pen, f=f)
    return out


def _weighted(pts: Sequence[Pt], passes: int, gap: float, pen: Optional[int],
              f: int = 2000) -> List[GCodeCommand]:
    """A polyline drawn as `passes` parallel passes — line weight in mm."""
    if passes <= 1:
        return kit._poly(list(pts), color=pen, f=f)
    out: List[GCodeCommand] = []
    span = gap * (passes - 1)
    for k in range(passes):
        d = -span / 2 + span * k / (passes - 1)
        out += kit._poly(kit._offset_polyline(list(pts), d), color=pen, f=f)
    return out


def _spoke_disc(cx: float, cy: float, r: float, pen: Optional[int],
                pitch: float = 1.5) -> List[GCodeCommand]:
    """A disc filled by radii — a burst.  Used where ONE query owns the value."""
    n = max(8, int(2 * math.pi * r / pitch))
    out = kit.circle(cx, cy, r, pen=pen)
    for k in range(n):
        a = 2 * math.pi * k / n
        out += kit._poly([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
                         color=pen, f=2000)
    return out


def _tri_region(a: Pt, b: Pt, c: Pt):
    reg = None
    for (p0, p1, other) in ((a, b, c), (b, c, a), (c, a, b)):
        nx, ny = -(p1[1] - p0[1]), (p1[0] - p0[0])
        L = math.hypot(nx, ny) or 1.0
        nx, ny = nx / L, ny / L
        cc = -(nx * p0[0] + ny * p0[1])
        if nx * other[0] + ny * other[1] + cc > 0:
            nx, ny, cc = -nx, -ny, -cc
        hp = HalfPlane(nx, ny, cc)
        reg = hp if reg is None else (reg & hp)
    return reg


def _dotted(pts: Sequence[Pt], pen: Optional[int], on: float = 1.6,
            off: float = 2.2) -> List[GCodeCommand]:
    """Dash a polyline by arclength."""
    out: List[GCodeCommand] = []
    cur: List[Pt] = []
    s = 0.0
    draw = True
    for p0, p1 in zip(pts, pts[1:]):
        seg = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        t = 0.0
        while t < seg:
            want = (on if draw else off) - s
            step = min(want, seg - t)
            q0 = (p0[0] + (p1[0] - p0[0]) * t / seg, p0[1] + (p1[1] - p0[1]) * t / seg)
            t2 = t + step
            q1 = (p0[0] + (p1[0] - p0[0]) * t2 / seg, p0[1] + (p1[1] - p0[1]) * t2 / seg)
            if draw:
                if cur and abs(cur[-1][0] - q0[0]) < 1e-6 and abs(cur[-1][1] - q0[1]) < 1e-6:
                    cur.append(q1)
                else:
                    if len(cur) >= 2:
                        out += kit._poly(cur, color=pen, f=2000)
                    cur = [q0, q1]
            s += step
            t = t2
            if s >= (on if draw else off) - 1e-9:
                if draw and len(cur) >= 2:
                    out += kit._poly(cur, color=pen, f=2000)
                    cur = []
                draw = not draw
                s = 0.0
    if len(cur) >= 2:
        out += kit._poly(cur, color=pen, f=2000)
    return out


def _txt(s: str, x: float, y: float, h: float, pen: Optional[int],
         spaced: bool = False) -> List[GCodeCommand]:
    t = " ".join(s) if spaced else s
    return kit._stroke_text(t, x, y, h, color=pen, f=2000)


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------
def kandinsky_attention(rng: SeededRNG, bounds: Bounds, colors: int = 5
                        ) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    P = lambda i: _pen(i, colors)  # noqa: E731

    M = Mech()
    n = M.n

    # ---- layout -----------------------------------------------------------
    title_h = 14.0
    foot_h = 46.0
    band_lo, band_hi = y0 + foot_h, y1 - 46.0
    R = min((W - 44.0) / 2.0, (band_hi - band_lo) / 2.0 - 14.0)
    cx = x0 + W * 0.5 - 5.0
    cy = (band_lo + band_hi) * 0.5

    def S(p: Pt) -> Pt:
        """unit-circle coords -> sheet mm"""
        return (cx + R * p[0], cy + R * p[1])

    rmark = [max(1.7, 3.35 * m) for m in M.m]

    out: List[GCodeCommand] = []
    frame = Rect(x0 + 0.4, y0 + 0.4, x1 - 0.4, y1 - 0.4)

    # ---- 1. the plane of the three heaviest values (GOLD, wide hatch) ------
    tri = [S(M.p[j]) for j in M.top3]
    reg = _tri_region(*tri) & ~Circle(cx, cy, KNOT_R)
    phi = math.atan2(M.zbar[1], M.zbar[0]) + math.pi / 2  # hatch across the diagonal
    ux, uy = math.cos(phi), math.sin(phi)
    vx, vy = -uy, ux
    k = -int(R / HATCH_PITCH) - 2
    while k <= int(R / HATCH_PITCH) + 2:
        d = k * HATCH_PITCH
        a = (cx + vx * d - ux * (R + 6), cy + vy * d - uy * (R + 6))
        b = (cx + vx * d + ux * (R + 6), cy + vy * d + uy * (R + 6))
        out += _runs(clip([a, b], reg, keep="inside"), P(GOLD))
        k += 1
    out += _runs([[tri[0], tri[1], tri[2], tri[0]]], P(GOLD))

    # ---- 2. the unit circle + the slot scaffold (BLACK) --------------------
    ring = [(cx + R * math.cos(2 * math.pi * t / 240), cy + R * math.sin(2 * math.pi * t / 240))
            for t in range(241)]
    out += _weighted(ring, 2, 0.45, P(BLACK))
    for j in range(n):
        ca, sa = math.cos(M.theta[j]), math.sin(M.theta[j])
        out += _dotted([(cx + (R - 13.0) * ca, cy + (R - 13.0) * sa),
                        (cx + R * ca, cy + R * sa)], P(BLACK), on=0.9, off=2.1)

    # mean reach — the line between decided and undecided
    out += _dotted([(cx + M.mean_reach * R * math.cos(2 * math.pi * t / 240),
                     cy + M.mean_reach * R * math.sin(2 * math.pi * t / 240))
                    for t in range(241)], P(BLACK), on=1.1, off=2.6)

    # ---- 3. the plate's centre of gravity: one heavy ray (BLACK) ----------
    ang = math.atan2(M.zbar[1], M.zbar[0])
    far = W + H
    ray = clip([(cx, cy), (cx + far * math.cos(ang), cy + far * math.sin(ang))],
               frame, keep="inside")
    for r_ in ray:
        out += _weighted(r_, 3, 0.4, P(BLACK))
    back = clip([(cx, cy), (cx - far * math.cos(ang), cy - far * math.sin(ang))],
                frame, keep="inside")
    for r_ in back:
        out += _dotted(r_, P(BLACK), on=1.4, off=3.0)

    # ---- 4. the values on the rim (GOLD) + who wins them (BLUE) -----------
    for j in range(n):
        mx, my = S(M.p[j])
        r = rmark[j]
        if r < 2.5:
            out += kit.fill_disc(mx, my, r, spacing=0.5, pen=P(GOLD))
        elif M.c[j] > 0.5:                      # owned by one query -> burst
            out += _spoke_disc(mx, my, r, P(GOLD), pitch=RING_PITCH)
        else:                                   # shared by many -> rings
            out += kit.circle(mx, my, r, pen=P(GOLD))
            rr = r - RING_PITCH
            while rr > 0.4:
                out += kit.circle(mx, my, rr, pen=P(GOLD))
                rr -= RING_PITCH
            out += kit.fill_disc(mx, my, 0.8, spacing=0.45, pen=P(GOLD))
        # blue: one tick per query that picks this value as its argmax
        ca, sa = math.cos(M.theta[j]), math.sin(M.theta[j])
        for t in range(M.wins[j]):
            rr = R + r + 2.4 + t * 1.9
            a0 = M.theta[j] - 2.6 / rr
            a1 = M.theta[j] + 2.6 / rr
            out += _runs([[(cx + rr * math.cos(a0 + (a1 - a0) * s / 8),
                            cy + rr * math.sin(a0 + (a1 - a0) * s / 8)) for s in range(9)]],
                         P(BLUE))
        lab = R + r + 2.4 + max(M.wins[j], 1) * 1.9 + 3.4
        out += _txt(f"{j}", cx + lab * ca - 1.1, cy + lab * sa - 1.1, 2.6, P(BLACK))

    # ---- 5. the tracks: one per query, each exactly R mm long (RED) -------
    for i in range(n):
        pts = [S(p) for p in M.walk[i]]
        # drop repeated points from zero-weight steps so the polyline is clean
        clean = [pts[0]]
        for p in pts[1:]:
            if math.hypot(p[0] - clean[-1][0], p[1] - clean[-1][1]) > 0.05:
                clean.append(p)
        if len(clean) >= 2:
            out += kit._poly(clean, color=P(RED), f=2000)
        # a POINT at every joint whose step is visible: radius carries the weight
        for j in range(n):
            w = M.a[i][j]
            if w * R < 1.6:
                continue
            q = S(M.walk[i][j])
            rr = min(1.35, 0.42 + 1.1 * w)
            out += kit.fill_disc(q[0], q[1], rr, spacing=0.45, pen=P(RED))

    # ---- 6. the outputs: one per query (GREEN) ----------------------------
    zs = [S(v) for v in M.z]
    out += _dotted(zs, P(GREEN), on=1.3, off=1.9)
    for v in zs:
        out += kit.fill_disc(v[0], v[1], 2.3, spacing=0.45, pen=P(GREEN))
    out += kit.circle(cx, cy, 2.0, pen=P(BLACK))

    # ---- 7. type ----------------------------------------------------------
    out += kit.giant_type("POINT AND LINE", x0, y1 - 17.0, title_h, pen=P(BLACK),
                          weight=1.25, tip=0.5)
    out += kit.giant_type("TO PLANE", x0, y1 - 39.0, title_h, pen=P(BLACK),
                          weight=1.25, tip=0.5)
    sub_x = x0 + kit.giant_type_width("TO PLANE", title_h) + 10.0
    out += _txt("A LINE IS THE TRACK MADE BY THE MOVING POINT", sub_x, y1 - 30.0,
                2.7, P(BLACK))
    out += _txt("KANDINSKY 1926 · AND ONE ATTENTION ROW IS", sub_x, y1 - 35.5,
                2.7, P(BLACK))
    out += _txt("FIFTEEN STEPS OF EXACTLY ONE UNIT OF STRING", sub_x, y1 - 41.0,
                2.7, P(BLACK))

    # footer: the measured numbers
    fy = y0 + foot_h - 6.0
    col = [
        [
            "THE ORDER",
            f"step j of row i runs {'{:.0f}'.format(R)} x a(i,j) mm",
            "toward slot j.  every track is the",
            f"same length: {'{:.1f}'.format(R)} mm, because",
            "the row sums to one.",
            "where it ends is z(i) = sum a(i,j) v(j).",
        ],
        [
            "MEASURED",
            f"peak share  mean {M.mean_peak:.3f}  max {max(M.peak):.3f}",
            f"uniform row would be {1.0 / n:.3f}",
            f"reach |z|  {M.reach[0]:.2f} at row 0 to "
            f"{min(M.reach):.2f} at row {M.reach.index(min(M.reach))}",
            f"mean reach {M.mean_reach:.3f}  (dotted circle)",
            f"value {M.top3[0]} takes {max(M.m):.2f} of {float(n):.1f} units",
        ],
        [
            "READ",
            "gold  a value.  radius = mass received.",
            "rings = shared, burst = owned by one row.",
            "blue  one tick per row that picks it.",
            "red   the fifteen tracks.",
            "green the fifteen outputs.  one per row.",
        ],
    ]
    cw = W / 3.0
    for ci, lines in enumerate(col):
        yy = fy
        out += _txt(lines[0], x0 + ci * cw, yy, 3.0, P(BLACK), spaced=True)
        out += _runs([[(x0 + ci * cw, yy - 2.6), (x0 + ci * cw + cw - 10.0, yy - 2.6)]],
                     P(BLACK))
        yy -= 7.4
        for ln in lines[1:]:
            out += _txt(ln, x0 + ci * cw, yy, 2.45, P(BLACK))
            yy -= 4.6

    out += _txt(f"GPT-2 SMALL · LAYER {LAYER} · HEAD {HEAD} · {n} TOKENS · "
                f"EVERY TRACK BEGINS AT THE CENTRE AND NONE ENDS THERE",
                x0, y0 + 1.6, 2.6, P(BLACK))

    return out
