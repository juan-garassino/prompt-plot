"""CNN — THE REACH OF ONE UNIT (r05, thesis: wildcard · parent r03 · canon: radial data-viz §5).

One forward pass of a real trained CNN (Keras MobileNetV2, ImageNet weights, on
the scikit-image cat "chelsea", centre-crop 300² -> bicubic 224²; the SAME pass as
r02-r04, re-run by ``compute_reach.py`` to tap the gradient at all 20 depths and
cross-checked bit-exact against r03's ``maps.npz``). The question the plate
answers is the one a CNN is built on: HOW FAR DOES ONE UNIT SEE, AND WHO DECIDES?

The order is a DIAL, not a stack (lineage: Florence Nightingale's polar-area
"rose", 1858, read through the Bauhaus 1919-1933 radial timeline):

    angle  = time through the network = conv layers applied (0 -> 52), clockwise
             from 12 o'clock (the input) to 6 o'clock (Conv_1); a4 portrait, the
             dial's diameter on the left margin is the px scale
    radius = Chebyshev distance from the centre of the argmax CAM unit (4,3),
             in INPUT pixels (the one shared ruler), 0 -> 160 px (the farthest
             pixel of the picture is 159 px away; edges beyond sit on the rim)
    one sector per tapped depth (input, stem, block_0 … block_16, Conv_1)

In every sector (pen: cadetblue) the concentric arcs ARE the rings of that
layer's grid: ring pitch = that layer's stride, so the resolution coarsens
around the dial (2 px -> 32 px). Each arc's LENGTH is the ring's SHARE of the
gradient mass Σ|∂unit/∂A| (summed over the ring's units), relative to the
sector's largest ring — each sector is the effective receptive field's radial
mass profile drawn as a petal.

Pens, plot order: 0 cadetblue petals · 1 darkgoldenrod half-mass · 2 indianred
theoretical edge · 3 black furniture and type.

    red   = the exact theoretical receptive field edge on that layer: beyond it
            the gradient is 0.0 exactly (checked numerically in compute_reach).
    ochre = the ring inside which half the gradient mass lies (ERF r50).
    black = scale, rim, type.

Nothing is invented: every mark is read from ``reach.npz``.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import _poly, _runs_from_cmds_pens, _stroke_text, _text_width

HERE = Path(__file__).resolve().parent
DATA = np.load(HERE / "reach.npz")

Pt = Tuple[float, float]
Run = List[Pt]

# pens, in plotting order (light body first, type last)
BLUE, OCHRE, RED, BLACK = 0, 1, 2, 3

# ---- the ruler -------------------------------------------------------------
D_MAX = 160.0          # px on the radial axis: the farthest pixel of the picture is 159 px away
DUTY_MIN = 0.03        # rings below 3 % of their sector's densest ring stay blank
MIN_ARC = 0.7          # mm: shortest petal arc drawn
GUTTER_DEG = 1.1       # blank radial gutter between sectors
CLEAR = 0.9            # mm clearance kept between pens where marks meet
INPUT_SPAN = 3.0       # the input sector is given one block's width of "time"

STATS: Dict[str, float] = {}

SHORT = {"input": "IN", "stem": "S", "conv_1": "C1"}


# ---------------------------------------------------------------------------
# the science: rings, profiles, r50, theoretical edge
# ---------------------------------------------------------------------------


def unit_centre() -> Tuple[float, float]:
    """Input-pixel centre of the argmax unit's receptive field (row, col)."""
    names = [str(n) for n in DATA["names"]]
    k = names.index("conv_1")
    s, o = float(DATA["stride"][k]), float(DATA["off"][k])
    i, j = (int(v) for v in DATA["argmax"])
    return o + s * i, o + s * j


def taps() -> List[Dict]:
    """One record per tapped depth, computed from the raw gradient maps."""
    cr, cc = unit_centre()
    out = []
    names = [str(n) for n in DATA["names"]]
    prev_n = -INPUT_SPAN
    for k, name in enumerate(names):
        g = DATA["g_" + name].astype(float)
        N, s, o, nL = int(DATA["N"][k]), int(DATA["stride"][k]), float(DATA["off"][k]), int(DATA["nL"][k])
        r0, r1, c0, c1 = (int(v) for v in DATA["trf"][k])
        centres = o + s * np.arange(N)
        d = np.maximum(np.abs(centres[:, None] - cr), np.abs(centres[None, :] - cc))
        b = max(s, 2)                       # ring bin: the grid's own pitch, >= 2 px
        ring = np.floor((d + b - 1) / b).astype(int)
        nr = int(ring.max()) + 1
        dens = np.array([g[ring == q].mean() if (ring == q).any() else 0.0 for q in range(nr)])
        mass = np.array([g[ring == q].sum() for q in range(nr)])
        duty = mass / mass.max()            # the ring's SHARE of the gradient mass
        cm = np.cumsum(mass) / mass.sum()
        q50 = int(np.searchsorted(cm, 0.5))
        # continuous half-mass radius: ring q holds d in ((q-1)b, qb], so the
        # cumulative mass is exact at d = qb and is interpolated between rings
        if q50 == 0:
            r50x = 0.0
        else:
            c_lo, c_hi = cm[q50 - 1], cm[q50]
            r50x = ((q50 - 1) + (0.5 - c_lo) / (c_hi - c_lo)) * b
        # exact theoretical edge on this grid, in input px from the unit centre
        trf = max(cr - (o + s * r0), (o + s * r1) - cr, cc - (o + s * c0), (o + s * c1) - cc)
        zero_out = bool(DATA["zero_outside"][k])
        n_start = prev_n if name != "input" else -INPUT_SPAN
        n_end = nL if name != "input" else 0.0
        out.append(dict(name=name, N=N, stride=s, bin=b, nL=nL, n0=n_start, n1=n_end,
                        duty=duty, ring_px=np.arange(nr) * b, r50=q50 * b, r50x=r50x, trf=trf,
                        trf_edge=trf + b / 2.0, zero_out=zero_out,
                        maxnz=float(d[g > 0].max())))
        prev_n = n_end
    return out


# ---------------------------------------------------------------------------
# drawing helpers
# ---------------------------------------------------------------------------


class Dial:
    """Polar frame. Time runs CLOCKWISE from 12 o'clock (the input) to
    6 o'clock (Conv_1); the diameter lies on the sheet's left edge."""

    def __init__(self, hx: float, hy: float, R0: float, R1: float, n_lo: float, n_hi: float):
        self.hx, self.hy, self.R0, self.R1 = hx, hy, R0, R1
        self.k = (R1 - R0) / D_MAX
        self.n_lo, self.n_hi = n_lo, n_hi

    def R(self, d_px: float) -> float:
        return self.R0 + self.k * d_px

    def theta(self, n: float) -> float:
        return math.pi / 2.0 - math.pi * (n - self.n_lo) / (self.n_hi - self.n_lo)

    def xy(self, r: float, th: float) -> Pt:
        return (self.hx + r * math.cos(th), self.hy + r * math.sin(th))

    def arc(self, r: float, th0: float, th1: float, step: float = 0.45) -> Run:
        n = max(2, int(abs(th1 - th0) * r / step) + 1)
        return [self.xy(r, th0 + (th1 - th0) * i / (n - 1)) for i in range(n)]


def text_runs(text: str, x: float, y: float, h: float, pen: int, ang: float = 0.0,
              anchor: str = "left") -> List[Tuple[int, Run]]:
    """Single-stroke text, (x, y) = baseline anchor, rotated by ``ang`` rad."""
    w = _text_width(text, h)
    dx = {"left": 0.0, "centre": -w / 2.0, "right": -w}[anchor]
    runs = []
    for _, r in _runs_from_cmds_pens(_stroke_text(text, 0.0, 0.0, h, color=pen)):
        pts = []
        for px, py in r:
            px += dx
            pts.append((x + px * math.cos(ang) - py * math.sin(ang),
                        y + px * math.sin(ang) + py * math.cos(ang)))
        runs.append((pen, pts))
    return runs


def radial_label(dial: Dial, text: str, r: float, th: float, h: float) -> List[Tuple[int, Run]]:
    """Text centred on (r, th), baseline tangent to the circle, never upside down."""
    x, y = dial.xy(r, th)
    ang = th - math.pi / 2.0
    while ang <= -math.pi / 2.0:
        ang += math.pi
    while ang > math.pi / 2.0:
        ang -= math.pi
    w = _text_width(text, h)
    cx = x - (w / 2.0) * math.cos(ang) + (h / 2.0) * math.sin(ang)
    cy = y - (w / 2.0) * math.sin(ang) - (h / 2.0) * math.cos(ang)
    return text_runs(text, cx, cy, h, BLACK, ang=ang)


def dotted(dial: Dial, r: float, lo: float, hi: float, on: float = 0.7, period: float = 2.6) -> List[Run]:
    """Dotted arc at radius r over the angle interval [lo, hi], phase-locked to angle 0."""
    lo, hi = min(lo, hi), max(lo, hi)
    segs = []
    k = math.ceil(lo * r / period)
    while k * period + on <= hi * r:
        a = k * period / r
        segs.append(dial.arc(r, a, a + on / r, step=0.3))
        k += 1
    return segs


def run_len(r: Run) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(r, r[1:]))


def order_runs(runs: List[Run], start: Pt = (0.0, 0.0)) -> List[Run]:
    """Greedy nearest-neighbour order, reversing a run when its far end is nearer."""
    left = [list(r) for r in runs]
    out, cur = [], start
    while left:
        best, bi, rev = 1e18, 0, False
        for k, r in enumerate(left):
            d0 = (r[0][0] - cur[0]) ** 2 + (r[0][1] - cur[1]) ** 2
            d1 = (r[-1][0] - cur[0]) ** 2 + (r[-1][1] - cur[1]) ** 2
            if d0 < best:
                best, bi, rev = d0, k, False
            if d1 < best:
                best, bi, rev = d1, k, True
        r = left.pop(bi)
        out.append(r[::-1] if rev else r)
        cur = out[-1][-1]
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def cnn_reach_dial(rng, bounds, colors: int = 4, feed: int = 2200):
    """a4 PORTRAIT. rng unused: nothing on the sheet is random."""
    x0, y0, x1, y1 = bounds
    T = taps()
    dial = Dial(x0 + 13.0, (y0 + y1) / 2.0, R0=12.0, R1=117.0,
                n_lo=-INPUT_SPAN, n_hi=float(T[-1]["n1"]))
    gut = math.radians(GUTTER_DEG) / 2.0
    runs: List[Tuple[int, Run]] = []
    for t in T:                                   # clockwise: th0 > th1
        t["th0"] = dial.theta(t["n0"]) - gut
        t["th1"] = dial.theta(t["n1"]) + gut
        t["thc"] = (t["th0"] + t["th1"]) / 2.0

    # ---- blue: the petals (arc length = the ring's share of gradient mass) --
    # Where the ochre or red line steps radially through a gutter, a petal arc
    # on a ring crossed by that step keeps CLEAR mm away from it: the arc is
    # SHIFTED inside its sector (length kept); only if it cannot fit is it cut.
    steps = []                                    # (angle, r_lo, r_hi) of every radial step
    for i in range(len(T) - 1):
        thg = (T[i]["th1"] + T[i + 1]["th0"]) / 2.0
        for key in ("r50x", "trf_edge"):
            ra = dial.R(min(T[i][key], D_MAX))
            rb = dial.R(min(T[i + 1][key], D_MAX))
            if abs(ra - rb) > 1e-6:
                steps.append((thg, min(ra, rb) - CLEAR, max(ra, rb) + CLEAR))
    petal_half: Dict[Tuple[str, int], Tuple[float, float]] = {}
    yielded = shifted = cut = 0
    for t in T:
        half = (t["th0"] - t["th1"]) / 2.0
        r_o = dial.R(t["r50x"])
        for q, (dpx, u) in enumerate(zip(t["ring_px"], t["duty"])):
            if u < DUTY_MIN or dpx > D_MAX:
                continue
            r = dial.R(dpx)
            if abs(r - r_o) < CLEAR:
                yielded += 1                      # the ochre line takes this ring's place
                continue
            a = max(half * u, MIN_ARC / (2 * r))
            lo, hi = t["thc"] - a, t["thc"] + a
            lim_hi, lim_lo = t["th0"], t["th1"]       # never leave the sector
            for thg, r_lo, r_hi in steps:
                if r_lo <= r <= r_hi:
                    if t["thc"] < thg < t["th0"] + math.radians(GUTTER_DEG):
                        lim_hi = min(lim_hi, thg - CLEAR / r)
                    if t["th1"] - math.radians(GUTTER_DEG) < thg < t["thc"]:
                        lim_lo = max(lim_lo, thg + CLEAR / r)
            if hi > lim_hi + 1e-9 or lo < lim_lo - 1e-9:
                if hi - lo <= lim_hi - lim_lo:
                    d = (lim_hi - hi) if hi > lim_hi else (lim_lo - lo)
                    lo, hi = lo + d, hi + d
                    shifted += 1
                else:
                    full = (hi - lo) * r
                    lo, hi = max(lo, lim_lo), min(hi, lim_hi)
                    cut += 1
                    STATS["max_cut_mm"] = max(STATS.get("max_cut_mm", 0.0), full - (hi - lo) * r)
                    STATS["max_cut_frac"] = max(STATS.get("max_cut_frac", 0.0), 1 - (hi - lo) * r / full)
            if (hi - lo) * r < 0.3:
                continue
            petal_half[(t["name"], q)] = (lo, hi)
            runs.append((BLUE, dial.arc(r, hi, lo)))
    STATS.update(rings_yielded_to_ochre=yielded, arcs_shifted=shifted, arcs_cut=cut,
                 petal_arcs=len(petal_half))

    # ---- ochre: the half-mass radius, one line through every sector --------
    # ---- red:   the exact theoretical edge (on the rim = beyond the picture)
    for pen, key in ((OCHRE, "r50x"), (RED, "trf_edge")):
        line: Run = []
        for i, t in enumerate(T):
            r = dial.R(min(t[key], D_MAX))
            if line:
                rp = dial.R(min(T[i - 1][key], D_MAX))
                thg = (T[i - 1]["th1"] + t["th0"]) / 2.0
                if abs(rp - r) > 1e-6:
                    line += [dial.xy(rp, thg), dial.xy(r, thg)]
            line += dial.arc(r, t["th0"], t["th1"])
        runs.append((pen, line))

    runs += furniture(dial, T, bounds, petal_half)

    # ---- emit: one clean layer per pen, stated order, batchable ------------
    # Within a layer, runs are split into two ZONES (the dial, and the type
    # column on the right) and each zone is nearest-neighbour ordered on its
    # own, dial first, so no stroke-to-stroke travel crosses the sheet. The
    # legend swatch of each colour pen is drawn last in its layer.
    def zone(r: Run) -> int:
        mx = sum(q[0] for q in r) / len(r)
        my = sum(q[1] for q in r) / len(r)
        return 0 if math.hypot(mx - dial.hx, my - dial.hy) <= dial.R1 + 18.0 else 1

    by_pen: Dict[int, List[List[Run]]] = {}
    for pen, r in runs:
        if len(r) >= 2 and run_len(r) > 0.3:
            by_pen.setdefault(pen, [[], []])[zone(r)].append(r)
    cmds = []
    for pen in sorted(by_pen):
        p = pen if colors > 1 else None
        cur: Pt = (x0, y1) if pen != BLACK else (x0, y0)
        for zr in by_pen[pen]:
            for r in order_runs(zr, cur):
                cmds += _poly(r, color=p, f=feed)
                cur = r[-1]
    return cmds


def furniture(dial: Dial, T: List[Dict], bounds, petal_half) -> List[Tuple[int, Run]]:
    x0, y0, x1, y1 = bounds
    runs: List[Tuple[int, Run]] = []
    B = BLACK

    # rim: one fine tick per conv layer applied, long every 10
    Rr = dial.R1 + 2.5
    runs.append((B, dial.arc(Rr, dial.theta(0), dial.theta(dial.n_hi))))
    for n in range(0, int(dial.n_hi) + 1):
        th = dial.theta(n)
        L = 2.4 if n % 10 == 0 else 1.1
        runs.append((B, [dial.xy(Rr, th), dial.xy(Rr + L, th)]))
    for t in T:                                   # block ids outside the rim
        lab = SHORT[t["name"]] if t["name"] in SHORT else t["name"].split("_")[1]
        runs += radial_label(dial, lab, dial.R1 + 7.0, t["thc"], 1.5)

    # stage brackets: same-resolution sectors share one arc and one label
    Rs = dial.R1 + 11.5
    groups: List[List[Dict]] = []
    for t in T:
        if groups and groups[-1][0]["N"] == t["N"]:
            groups[-1].append(t)
        else:
            groups.append([t])
    for gp in groups:
        a0, a1 = gp[0]["th0"], gp[-1]["th1"]
        runs.append((B, dial.arc(Rs, a0, a1)))
        for a in (a0, a1):
            runs.append((B, [dial.xy(Rs, a), dial.xy(Rs - 1.4, a)]))
        runs += radial_label(dial, f"{gp[0]['N']}²", Rs + 3.2, (a0 + a1) / 2.0, 2.0)

    # graduated scale rings (dotted) at 64 and 128 px, only on blank paper
    for dpx in (64, 128):
        r = dial.R(dpx)
        for i, t in enumerate(T):
            spans = [(t["th1"], t["th0"])]
            if i + 1 < len(T):
                spans.append((T[i + 1]["th0"], t["th1"]))
            q = int(round(dpx / t["bin"]))
            if q * t["bin"] == dpx and (t["name"], q) in petal_half:
                plo, phi = petal_half[(t["name"], q)]
                plo, phi = plo - CLEAR / r, phi + CLEAR / r
                spans = [(lo, hi) for lo0, hi0 in spans
                         for lo, hi in ((lo0, min(hi0, plo)), (max(lo0, phi), hi0))
                         if hi > lo]
            for lo, hi in spans:
                runs += [(B, seg) for seg in dotted(dial, r, lo, hi)]

    # the diameter: radial scale in px, both halves, on the sheet's left edge
    xb = dial.hx - 1.2
    for side in (-1, 1):
        ya, yb = dial.hy + side * dial.R0, dial.hy + side * dial.R1
        runs.append((B, [(xb, ya), (xb, yb)]))
        for dpx in range(0, int(D_MAX) + 1, 16):
            yy = dial.hy + side * dial.R(dpx)
            L = 1.8 if dpx % 32 == 0 else 0.9
            runs.append((B, [(xb, yy), (xb - L, yy)]))
            if dpx % 32 == 0 and dpx > 0:
                runs += text_runs(str(dpx), xb - 2.6, yy - 0.8, 1.6, B, anchor="right")
    # hub: the unit itself
    runs.append((B, [(dial.hx - 1.0, dial.hy), (dial.hx + 1.0, dial.hy)]))
    runs.append((B, [(dial.hx, dial.hy - 1.0), (dial.hx, dial.hy + 1.0)]))

    # ---- type: one flush-left axis in the right column ----------------------
    tx = 112.0
    runs += text_runs("THE REACH", tx, y1 - 13.5, 8.0, B)
    runs += text_runs("OF ONE UNIT", tx, y1 - 26.0, 8.0, B)
    sub = ["IT COULD SEE THE WHOLE PICTURE.", "IT LOOKS AT A QUARTER OF IT."]
    for i, ln in enumerate(sub):
        runs += text_runs(ln, tx, y1 - 36.0 - i * 3.6, 2.0, B)

    notes = [
        (y1 - 58.0, ["INPUT: THE EDGE LIES AT", "245 PX, OFF THE PICTURE.",
                     "HALF THE PULL LIES", "WITHIN 56 PX: 25 % OF IT."]),
        ((y0 + y1) / 2.0 + 20.0, ["INPUT TO BLOCK 12: THE", "EDGE CLOSES 245 -> 112 PX,",
                                  "THE HALF-MASS RING", "ONLY 56 -> 43 PX."]),
        (y0 + 96.0, ["THE 7² BLOCKS DO THE", "REST: EDGE 112 -> 0 PX,",
                     "HALF-MASS 43 -> 0 PX.", "ONE CELL: UNIT (4,3)."]),
    ]
    nx = 158.0
    for yy, lines in notes:
        for i, ln in enumerate(lines):
            runs += text_runs(ln, nx, yy - i * 3.4, 1.5, B)

    # legend, bottom-right
    lx, ly = tx, y0 + 31.5
    rows = [
        (BLUE, "ARC LENGTH = RING'S SHARE OF |∂ UNIT / ∂ LAYER|"),
        (OCHRE, "HALF THE GRADIENT MASS LIES INSIDE"),
        (RED, "THEORETICAL EDGE: BEYOND IT ∂ = 0"),
    ]
    for i, (pen, txt) in enumerate(rows):
        yy = ly - i * 5.0
        runs.append((pen, [(lx, yy + 0.8), (lx + 6.0, yy + 0.8)]))
        runs += text_runs(txt, lx + 8.5, yy, 1.5, B)
    cap = ["ANGLE = CONV LAYERS APPLIED, CLOCKWISE 0 -> 52",
           "RADIUS = CHEBYSHEV PX FROM THE UNIT'S CENTRE",
           "RING PITCH = STRIDE · LONGEST RING OF A SECTOR = FULL",
           "MOBILENETV2 · CHELSEA, CENTRE-CROP · TIGER CAT 0.43"]
    for i, ln in enumerate(cap):
        runs += text_runs(ln, lx, ly - 15.0 - i * 3.4, 1.5, B)
    return runs
