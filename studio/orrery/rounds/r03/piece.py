"""ORRERY r03 — RESONANT ORBITS.  parent: r01 (the engraved orrery recreation).

One real attention row drawn as an ORBITAL order. GPT-2 small, layer 4, head 3,
the sentence "The pen plotter drew a black hole while the transformer watched
itself think." The query is ``itself`` (token 12); causal masking leaves it 13
keys (tokens 0..12, itself included).

The mechanism is the geometry
-----------------------------
Every key is a body on a near-circular orbit about the query (the crimson sun).
Its distance from the query breathes κ_j times per revolution:

    r_j(θ) = R_j + A·cos(κ_j (θ − θ0)),   θ ∈ [θ0, θ0 + 2πN]

An orbit closes iff the ratio of its radial to its orbital frequency is a whole
number (Bertrand's condition): otherwise the apsides precess and, given time,
the orbit fills its annulus. κ_j = n_j + δ_j, where n_j is the whole number of
lobes that fits the ring (layout) and δ_j is the key's miss (data):

    δ_j = (s* − s_j) / (N · max_k(s* − s_k)),      s_j = q·k_j / √d_head

s* is the best key's scaled dot product. Softmax is blind to a shared shift, so
the dot-product SHORTFALL to the best key is the only part of q·k attention can
see; that shortfall is the detuning, exactly (s* − s_j = ln a* − ln a_j, read off
the stored softmax row with no approximation). N = 4, max shortfall = 4.710, so
δ_j = (s* − s_j) / 18.84.

* δ = 0 (the argmax key, ``transformer``): κ is whole, the orbit closes after
  one turn and its remaining N−1 turns retrace it. The plate lays those N
  retraces 0.25 mm apart, so the same ink becomes one heavy line.
* δ > 0: each turn the apsides slip by δ of a lobe. After N turns the key has
  laid N offset strands across its annulus: a rope whose twist is its
  dot-product shortfall. The worst key (``drew``) slips a full lobe.

Every key orbits for the same N turns, so every key gets the same ink; resonance
only decides whether that ink lands in one place or spreads.

Layout (declared, not data): ring radius = token position (the first token
innermost, the newest outermost, like growth rings); all bodies start in
conjunction on the 6 o'clock ray, which is the spine the sentence is set on.

Pens: 0 blue = keys (every orbit) · 1 crimson = the query (sun + conjunction
spine) · 2 black = type.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

from promptplot.generative.engine.geometry import Rect, clip, polyline_length, resample_by_arclength
from promptplot.generative.engine.kit import _offset_polyline, fill_disc, giant_type
from promptplot.generative.generators import _poly, _stroke_text, _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Poly = List[Pt]

# --- the data -------------------------------------------------------------
# ~/.promptplot/attn_gpt2.npz  attn[4, 3, 12, :13]  (layer 4, head 3, query 12)
# extracted by scripts/extract_gpt2_attention.py with its default sentence.
TOKENS = ["The", "pen", "plot", "ter", "drew", "a", "black", "hole", "while", "the",
          "transformer", "watched", "itself"]
ATTN = [0.114244, 0.0582645, 0.0312548, 0.0139284, 0.00501897, 0.00604155, 0.0105259,
        0.0625073, 0.015139, 0.0521766, 0.557199, 0.0618485, 0.0118518]
NPZ = "~/.promptplot/attn_gpt2.npz"
LAYER, HEAD, QUERY = 4, 3, 12

BLUE, CRIMSON, BLACK = 0, 1, 2

# --- the orbit law ----------------------------------------------------------
# sheet layout, mm (A4 portrait, drawable 10..200 x 10..287)
LAYOUT = dict(cx=70.0, cy=172.0, R0=15.0, P=7.5, A=2.6, lobe=16.0)

TURNS = 4  # N: every key orbits the query for the same number of turns
RETRACE_GAP = 0.25  # mm between the locked key's N coincident passes


def logit_gaps() -> List[float]:
    """s* − s_j for every key, from the softmax row (ln a* − ln a_j)."""
    s = [math.log(a) for a in ATTN]
    top = max(s)
    return [top - v for v in s]


def detunings(turns: int = TURNS) -> List[float]:
    g = logit_gaps()
    gmax = max(g)
    return [gj / (gmax * turns) for gj in g]


def check_against_npz() -> bool:
    """True when the hard-coded row matches the npz on disk (if present)."""
    import os

    path = os.path.expanduser(NPZ)
    if not os.path.exists(path):
        return False
    import numpy as np

    row = np.load(path)["attn"][LAYER, HEAD, QUERY, : QUERY + 1]
    return bool(np.allclose(row, ATTN, rtol=1e-4, atol=1e-7))


# --- geometry ---------------------------------------------------------------
def _rdp(pts: Sequence[Pt], tol: float) -> Poly:
    """Douglas–Peucker: drop vertices within ``tol`` mm of the chord (G-code size)."""
    if len(pts) < 3:
        return list(pts)
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = math.hypot(dx, dy) or 1e-12
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * (px - ax) - dx * (py - ay)) / L
            if d > best:
                best, bi = d, i
        if best > tol:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [p for p, k in zip(pts, keep) if k]


def orbit_trace(c: Pt, R: float, A: float, kappa: float, turns: float, theta0: float) -> Poly:
    """A near-circular orbit about the query: r(θ) = R + A·cos(κ(θ − θ0)).

    κ = radial frequency / orbital frequency. The orbit closes iff κ is whole
    (the apsides return to the same place every turn); otherwise the apsides
    precess by 2π(κ − ⌊κ⌋)/κ per turn and the orbit fills its annulus. Starts at
    apoapsis on the conjunction ray θ0."""
    import numpy as np

    steps = int(turns * 2 * math.pi * (R + A) * (1 + A * kappa / R) / 0.1) + 8
    th = theta0 + 2 * math.pi * turns * np.linspace(0.0, 1.0, steps + 1)
    rr = R + A * np.cos(kappa * (th - theta0))
    pts = list(zip((c[0] + rr * np.cos(th)).tolist(), (c[1] + rr * np.sin(th)).tolist()))
    return _rdp(resample_by_arclength(pts, step=0.25), 0.02)


Box = Tuple[float, float, float, float]


def _knock(polys: Sequence[Poly], boxes: Sequence[Box], frame: Box, min_len: float) -> List[Poly]:
    """Clip to the frame and knock out the type halos with the exact geometry
    kernel (runs stop ON the box edge), then drop crumbs. Only the segments
    whose bbox touches a box are sent to the exact clipper, so a 3 m trace with
    15 halos stays fast and untouched stretches are never split."""
    regions = [Rect(*b) for b in boxes]
    fx0, fy0, fx1, fy1 = frame
    freg = Rect(*frame)
    out: List[Poly] = []

    def flush(run: Poly):
        if len(run) >= 2 and polyline_length(run) >= min_len:
            out.append(run)

    for p in polys:
        run: Poly = []
        for a, b in zip(p, p[1:]):
            sx0, sx1 = min(a[0], b[0]), max(a[0], b[0])
            sy0, sy1 = min(a[1], b[1]), max(a[1], b[1])
            hit = [reg for reg, (bx0, by0, bx1, by1) in zip(regions, boxes)
                   if sx1 >= bx0 and sx0 <= bx1 and sy1 >= by0 and sy0 <= by1]
            inside_frame = sx0 >= fx0 and sx1 <= fx1 and sy0 >= fy0 and sy1 <= fy1
            if not hit and inside_frame:
                if not run:
                    run = [a]
                run.append(b)
                continue
            pieces = clip([a, b], freg, keep="inside")
            for reg in hit:
                pieces = [q for pc in pieces for q in clip(pc, reg, keep="outside")]
            if not pieces:
                flush(run)
                run = []
                continue
            for k, pc in enumerate(pieces):
                starts_at_a = abs(pc[0][0] - a[0]) < 1e-9 and abs(pc[0][1] - a[1]) < 1e-9
                if k == 0 and starts_at_a and run:
                    run.extend(pc[1:])
                else:
                    flush(run)
                    run = list(pc)
            last = pieces[-1][-1]
            if abs(last[0] - b[0]) > 1e-9 or abs(last[1] - b[1]) > 1e-9:
                flush(run)
                run = []
        flush(run)
    return out


def _halo(text: str, x: float, y: float, h: float, pad: float = 1.2) -> Box:
    w = _text_width(text, h)
    return (x - pad, y - 0.45 * h - pad * 0.6, x + w + pad, y + h + pad * 0.6)


CAPTION = [
    "thirteen keys, one query, four turns each. an orbit closes only",
    "if it breathes a whole number of times per turn. each key misses",
    "by its dot-product shortfall to the best key.",
]
LAW = [
    "kappa = n + (s* - s) / 18.84       s = q.k / 8",
    "gpt-2 small   layer 4   head 3   query 12 of 15",
]

# the stroke font has no '?': a hook and a dot on its 4 x 6 grid
_QMARK = [[(0.6, 4.6), (1.3, 5.7), (2.7, 5.7), (3.4, 4.8), (3.4, 4.0), (2.0, 2.9), (2.0, 1.7)],
          [(1.7, 0.0), (2.3, 0.0), (2.3, 0.5), (1.7, 0.5), (1.7, 0.0)]]


def _question(text: str, x: float, y: float, h: float, pen: int) -> List[GCodeCommand]:
    out = _stroke_text(text, x, y, h, color=pen)
    qx = x + _text_width(text, h)
    sc = h / 6.0
    for st in _QMARK:
        out += _poly([(qx + gx * sc, y + gy * sc) for gx, gy in st], color=pen)
    return out


# --- the plate ----------------------------------------------------------------
def orrery_resonant_orbits(rng: SeededRNG, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    frame = (x0, y0, x1, y1)
    cx, cy = LAYOUT["cx"], LAYOUT["cy"]
    R0, P, r, lam = LAYOUT["R0"], LAYOUT["P"], LAYOUT["A"], LAYOUT["lobe"]
    theta0 = -math.pi / 2  # conjunction on the 6 o'clock ray
    dl = detunings()
    out: List[GCodeCommand] = []

    # type first (as geometry), so the orbits can be knocked out around it
    lh, nh = 2.6, 2.0
    labels, weights = [], []
    for j, tok in enumerate(TOKENS):
        R = R0 + j * P
        yb = cy - R - 0.45 * lh
        labels.append((tok, cx + 2.4, yb, lh))
        wtxt = f"{ATTN[j]:.3f}"[1:]
        weights.append((wtxt, cx - 2.4 - _text_width(wtxt, nh), yb + 0.2, nh))
    holes = [_halo(t, x, y, h) for t, x, y, h in labels + weights]
    spine_bot = cy - R0 - (len(TOKENS) - 1) * P - 5.0
    holes.append((cx - 1.1, spine_bot, cx + 1.1, cy - 6.0))

    # 0 blue — the keys, inner ring first, each ring in trace order
    for j in range(len(TOKENS)):
        R = R0 + j * P
        n = max(3, round(2 * math.pi * R / lam))
        if dl[j] == 0.0:
            base = orbit_trace((cx, cy), R, r, float(n), 1.0, theta0)
            passes = [
                _offset_polyline(base, (k - (TURNS - 1) / 2.0) * RETRACE_GAP)
                for k in range(TURNS)
            ]
        else:
            passes = [orbit_trace((cx, cy), R, r, n + dl[j], float(TURNS), theta0)]
        for run in _knock(passes, holes, frame, 4.0):
            out += _poly(run, color=BLUE, f=2200)

    # 1 crimson — the query: sun, conjunction spine, and its question
    out += fill_disc(cx, cy, 5.0, spacing=0.45, pen=CRIMSON)
    out += _poly([(cx, cy - 6.8), (cx, spine_bot)], color=CRIMSON)
    tx = cx + 2.4
    ty = spine_bot - 11.0
    out += _question("what does itself refer to", tx, ty - 7.5, 3.0, CRIMSON)

    # 2 black — type
    for t, x, y, h in labels + weights:
        out += _stroke_text(t, x, y, h, color=BLACK)
    out += giant_type("RESONANT ORBITS", tx, ty, 6.5, pen=BLACK, weight=0.5, tip=0.25)
    yy = ty - 13.0
    for line in CAPTION:
        out += _stroke_text(line, tx, yy, 1.9, color=BLACK)
        yy -= 3.6
    yy -= 1.6
    for line in LAW:
        out += _stroke_text(line, tx, yy, 1.9, color=BLACK)
        yy -= 3.6
    return out
