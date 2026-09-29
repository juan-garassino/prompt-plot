"""ORRERY r04 — RESONANT ORBITS, the miss takes space.  parent: r03.

One real attention row drawn as an ORBITAL order. GPT-2 small, layer 4, head 3,
the sentence "The pen plotter drew a black hole while the transformer watched
itself think." The query is `` itself`` (position 12); causal masking leaves it
13 keys (positions 0..12). Tokens, ids and the row are read from r02's
``gpt2_head.npz`` (own numpy forward, byte-level BPE ids, matched to
HuggingFace's torch stack at <= 2.3e-6).

The orbit law (kept from r03)
----------------------------
Every key is a body on a near-circular orbit about the query (the crimson sun),
breathing kappa_j times per revolution; turn k (k = 0, 1) is

    r(theta) = R_j + k*s_j + A*cos(kappa_j*(theta - theta0))

An orbit closes iff kappa is whole (Bertrand). kappa_j = n_j + d_j, n_j = the
whole number of lobes that fits the ring (layout), d_j = the key's miss (data):

    d_j = (s* - s_j) / 11.77,   s_j = q.k_j / 8,   11.77 = 2.5 x max_j (s* - s_j)

so the worst key (``drew``) slips 0.4 of a lobe per turn and is still 0.8 of a
lobe out after the two turns every key is given: TURNS x d_max = 0.8 < 1. The
shortfall s* - s_j = ln a* - ln a_j exactly (softmax is shift-invariant).

New in r04: the miss takes space
--------------------------------
A key that misses lays its second turn ``s_j`` further out:

    s_j = S0 + C*(d_j - d_min)      one affine map, anchored at ``The`` (d_min)

S0 = 1.3 mm is the floor that keeps the tightest key's two strands >= 0.8 mm apart
everywhere (breathing slope and phase slip included); C = 12.7 mm per lobe makes
the widest band 3.6x the tightest. The closing key has d = 0: its turns coincide
and are drawn as 3 passes 0.35 mm apart (weight, not data), set in 4.2 mm of
bare paper either side. The step between turns happens at conjunction, inside
the label slot, where no ink is drawn. The radius the bands do not use is shared
equally between the ordinary gaps (layout()).

The slot: two chord lines either side of the token column (the left one
vertical, the right one the least-loss straight line that keeps 2.1 mm clear of
every word). Every turn starts on one chord and ends on the other; turns
alternate direction, so the pipeline's nearest-neighbour reorder walks the blue
layer ring to ring down the slot. Type is planned the same way (plan_walk).

Pens (layer order, light to dark): 0 blue = keys · 1 crimson = the query (sun,
spine, question) · 2 black = type.
"""

from __future__ import annotations

import math
import os
from typing import Dict, List, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import (
    HalfPlane,
    clip,
    polyline_length,
)
from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Poly = List[Pt]

HERE = os.path.dirname(os.path.abspath(__file__))
NPZ = os.path.join(HERE, "..", "r02", "gpt2_head.npz")
QUERY = 12

BLUE, CRIMSON, BLACK = 0, 1, 2

# --- the law's constants (declared on the sheet) ------------------------------
TURNS = 2  # every key orbits the query twice
D_MAX = 0.4  # the worst key slips 0.4 lobe per turn -> TURNS * D_MAX = 0.8 < 1
AMP = 0.5  # A: constant breathing amplitude, mm (no data)
LOBE = 7.0  # target lobe length along the ring, mm (layout: sets n_j)
S0 = 1.3  # floor drift of the tightest key, mm
S_RATIO = 3.6  # widest / tightest band: s(d_max) / s(d_min)
R_OUT = 91.3  # outer envelope of the disc, mm; the gap between bands is solved from it
MOAT = 4.2  # bare paper either side of the closing orbit, mm
R_IN = 15.0  # inner envelope of the first band, mm
RETRACE = 0.35  # offset between the closing orbit's 3 passes, mm
SUN_R, SUN_PITCH = 9.8, 0.85

# type
TOK_H, W_H, SINK_H = 2.2, 1.8, 1.6
COL = 1.8  # tokens start / weights end this far from the spine
HALO = 2.1  # blue keeps this far from every glyph (>= 2 mm)
SWEEP_W = 1.2  # type is walked as a sweep: strokes whose leading x is within this of the front


def load_row():
    d = np.load(NPZ)
    toks = [str(t).strip() for t in d["tokens"][: QUERY + 1]]
    row = d["A"][QUERY, : QUERY + 1].astype(float)
    ids = [int(i) for i in d["ids"][: QUERY + 1]]
    return toks, row, ids, float(np.max(d["check_err"]))


def law() -> Dict:
    toks, row, ids, err = load_row()
    gaps = np.log(row.max()) - np.log(row)
    D = gaps.max() / D_MAX
    dl = gaps / D
    dmin = min(x for x in dl if x > 0)
    C = (S_RATIO - 1.0) * S0 / (dl.max() - dmin)
    return dict(toks=toks, row=row, ids=ids, err=err, gaps=gaps, D=D, dl=dl, dmin=dmin, C=C)


def _stack(L: Dict, gap: float) -> List[Dict]:
    bands = []
    R = R_IN + AMP
    for j, tok in enumerate(L["toks"]):
        d = float(L["dl"][j])
        if d == 0.0:
            R += MOAT - gap
            Rc = R + RETRACE
            n = round(2 * math.pi * Rc / LOBE)
            bands.append(dict(j=j, tok=tok, R=Rc, s=0.0, n=n, kappa=float(n), d=0.0,
                              inner=Rc - RETRACE - AMP, outer=Rc + RETRACE + AMP))
            R = Rc + RETRACE + AMP + MOAT + AMP
            continue
        s = S0 + L["C"] * (d - L["dmin"])
        n = round(2 * math.pi * R / LOBE)
        bands.append(dict(j=j, tok=tok, R=R, s=s, n=n, kappa=n + d, d=d,
                          inner=R - AMP, outer=R + s + AMP))
        R = R + s + AMP + gap + AMP
    return bands


def layout() -> Dict:
    """Radial budget: the bands take what the law gives them; the bare paper
    left over inside R_OUT is shared equally between the 10 ordinary gaps (the
    two gaps flanking the closing orbit are the fixed MOAT)."""
    L = law()
    lo, hi = 0.0, 10.0
    for _ in range(60):
        g = 0.5 * (lo + hi)
        if _stack(L, g)[-1]["outer"] > R_OUT:
            hi = g
        else:
            lo = g
    bands = _stack(L, lo)
    return dict(law=L, bands=bands, r_out=bands[-1]["outer"], gap=lo)


# --- geometry -------------------------------------------------------------------
def turn_trace(c: Pt, R: float, kappa: float, k: int, theta0: float) -> Poly:
    """Turn k of the orbit, theta in [theta0 + 2pi k, theta0 + 2pi (k+1)]."""
    steps = int(2 * math.pi * (R + AMP) / 0.12) + 8
    th = theta0 + 2 * math.pi * (k + np.linspace(0.0, 1.0, steps + 1))
    rr = R + AMP * np.cos(kappa * (th - theta0))
    return list(zip((c[0] + rr * np.cos(th)).tolist(), (c[1] + rr * np.sin(th)).tolist()))


def _rdp(pts: Sequence[Pt], tol: float) -> Poly:
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
        Ln = math.hypot(dx, dy) or 1e-12
        best, bi = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            dd = abs(dy * (px - ax) - dx * (py - ay)) / Ln
            if dd > best:
                best, bi = dd, i
        if best > tol:
            keep[bi] = True
            stack.append((a, bi))
            stack.append((bi, b))
    return [p for p, k in zip(pts, keep) if k]


# local glyph overrides: the font's zero carries a slash (reads as "Ø" in a
# column of weights), its full stop is a 0.6-unit speck, and it has no '?'.
_LOCAL = {
    "0": [[(1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 1), (3, 0), (1, 0)]],
    ".": [[(0.0, 0.0), (0.9, 0.0), (0.9, 0.9), (0.0, 0.9), (0.0, 0.0)]],
    "?": [[(0.0, 4.6), (0.7, 5.7), (2.1, 5.7), (2.8, 4.8), (2.8, 4.0), (1.4, 2.9), (1.4, 1.7)],
          [(1.1, 0.0), (1.7, 0.0), (1.7, 0.6), (1.1, 0.6), (1.1, 0.0)]],
}


def _glyph(ch: str):
    if ch in _LOCAL:
        return _LOCAL[ch]
    g = _GLYPHS.get(ch)
    if g is None:
        g = _GLYPHS.get(ch.upper(), [])
    return g


def ptext(text: str, x: float, y: float, h: float, weight: float = 0.0,
          tip: float = 0.25) -> List[Poly]:
    """Proportional stroke text with each glyph's INK left-aligned.

    ``_stroke_text(proportional=True)`` advances by ink width but still places
    the glyph at its cell origin, so a centred glyph (``i``, ``l``) lands on its
    neighbour ("itself" plots as "tself"). This shifts every glyph by its own
    ink minimum first. ``weight`` > 0 thickens strokes with parallel passes.
    """
    sc = h / 6.0
    out: List[Poly] = []
    cur = x
    passes = max(1, int(round(weight / tip)) + 1) if weight > 0 else 1
    for ch in text:
        g = _glyph(ch)
        xs = [p[0] for st in g for p in st]
        if not xs:
            cur += 2.6 * sc
            continue
        sb = 0.55 if ch.islower() else 0.9
        x0 = min(xs)
        for st in g:
            pts = [(cur + (gx - x0 + sb) * sc, y + gy * sc) for gx, gy in st]
            if passes == 1:
                out.append(pts)
            else:
                for k in range(passes):
                    d = -weight / 2.0 + weight * k / (passes - 1)
                    out.append(_offset_polyline(pts, d))
        cur += (max(xs) - x0 + 2 * sb) * sc
    return out


def ptext_width(text: str, h: float) -> float:
    sc = h / 6.0
    w = 0.0
    for ch in text:
        g = _glyph(ch)
        xs = [p[0] for st in g for p in st]
        sb = 0.55 if ch.islower() else 0.9
        w += (2.6 if not xs else max(xs) - min(xs) + 2 * sb) * sc
    return w


def _pbox(polys: Sequence[Poly]):
    xs = [p[0] for pl in polys for p in pl]
    ys = [p[1] for pl in polys for p in pl]
    return (min(xs), min(ys), max(xs), max(ys))


QUESTION = "where does this head look from itself?"
TITLE = "RESONANT ORBITS"
CAP_H = 1.9
CAP_PITCHES = (4.2, 4.4, 4.6, 4.8)
CAP_WIDTHS = (80.0, 84.0, 88.0)


def caption_paragraphs(L: Dict) -> List[str]:
    """The caption. A '~' is a non-breaking space: formulas never wrap."""
    D, gmax = L["D"], float(L["gaps"].max())
    return [t.replace("~", "\u00a0") for t in [
        "13 keys, 1 query, 2 turns each. an orbit closes only if it breathes a whole "
        "number of times per turn: kappa~=~n~+~d is whole only where d~=~0.",
        f"d~=~(s*~-~s)~/~{D:.2f}, s~=~q.k~/~8, and {D:.2f}~=~2.5~x the widest shortfall "
        f"(drew, {gmax:.2f}): after two turns the worst key is still 0.8 of a lobe out, "
        "so no miss can close.",
        f"a key that misses lays its second turn {S0:.1f}~+~{L['C']:.1f}~(d~-~{L['dmin']:.3f})~mm "
        "further out: the width of its band is its miss. the closing orbit is drawn as "
        f"3 passes {RETRACE:.2f}~mm apart: weight, not data.",
        "gpt-2 small, layer 4, head 3, query itself (12 of 15). the strongest of 144 heads "
        "for itself~>~transformer (next .416, mean .053). 106 of 144 heads look hardest "
        "at The, the position-0 sink.",
    ]]


def wrap(text: str, h: float, width: float) -> List[str]:
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if cur and ptext_width(t, h) > width:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


def _emit(polys: Sequence[Poly], pen: int, f: int = 2200) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for pl in polys:
        out += _poly(pl, color=pen, f=f)
    return out


def nn_walk(polys: Sequence[Poly]) -> List[int]:
    """Exactly the pipeline's per-colour walk (postprocess.optimize_stroke_order):
    start at (0, 0), always take the stroke whose START is nearest, never
    reverse a stroke, ties to the lowest index."""
    starts = np.array([p[0] for p in polys])
    ends = np.array([p[-1] for p in polys])
    left = list(range(len(polys)))
    pos = np.zeros(2)
    order = []
    while left:
        d = np.hypot(*(starts[left] - pos).T)
        i = left[int(np.argmin(d))]
        left.remove(i)
        order.append(i)
        pos = ends[i]
    return order


def plan_walk(blocks: Sequence[Sequence[Poly]]) -> Tuple[List[Poly], int]:
    """Order and orient strokes so the pipeline's greedy walk (``nn_walk``:
    from (0, 0), always the stroke with the nearest START, no reversal) visits
    the blocks one after another and never leaves a straggler behind.

    Inside a block the walk is greedy over both ends of every remaining stroke
    of that block. Every stroke not yet drawn waits with its start on its TOP
    end (so type on the line above presents its far side), and any stroke
    whose start would steal a step is flipped when its other end can wait
    further away without stealing an earlier step. Returns the strokes in walk
    order and the number of steps that could not be secured."""
    # plan on the coordinates the gcode will carry (_poly rounds to 0.01 mm),
    # and treat anything within TIE of the chosen distance as a rival
    items = [(bi, [(round(x, 2), round(y, 2)) for x, y in p]) for bi, blk in enumerate(blocks)
             for p in blk]
    n = len(items)
    TIE = 0.05
    E = np.array([[p[0], p[-1]] for _, p in items])  # (n, 2 ends, xy)
    blk = np.array([bi for bi, _ in items])
    flip = E[:, 1, 1] > E[:, 0, 1]  # wait with the start on the top end
    done = np.zeros(n, dtype=bool)
    banned = np.zeros((n, 2), dtype=bool)  # this end would have stolen a past step
    order: List[int] = []
    misses = 0
    pos = np.zeros(2)
    xmin = np.array([min(p_[0] for p_ in p) for _, p in items])
    xmax = np.array([max(p_[0] for p_ in p) for _, p in items])
    for bi in range(len(blocks)):
        idx = np.where(blk == bi)[0]
        # sweep the block away from the side the pen enters on
        sgn = 1.0 if abs(pos[0] - xmin[idx].min()) <= abs(pos[0] - xmax[idx].max()) else -1.0
        u = np.where(sgn > 0, xmin, -xmax)
        # entering a block: every stroke in it now waits with its start on the
        # end the sweep reaches first (the lower end of an upright stroke)
        for i in idx[~done[idx]]:
            (xa, ya), (xb, yb) = E[i]
            want_b = (yb < ya) if abs(xa - xb) < 0.3 else (sgn * xb < sgn * xa)
            if not banned[i, int(want_b)]:
                flip[i] = want_b
        while not np.all(done[idx]):
            left = idx[~done[idx]]
            cand = left[u[left] <= u[left].min() + SWEEP_W]
            d = np.hypot(E[cand, :, 0] - pos[0], E[cand, :, 1] - pos[1])  # (m, 2)
            if d.min() > 8.0:
                # entering from afar: take the block's nearest end, so the long
                # approach does not rule out ends the sweep will need later
                cand = left
                d = np.hypot(E[cand, :, 0] - pos[0], E[cand, :, 1] - pos[1])
            flat = int(np.argmin(d + 1e6 * banned[cand]))
            i, f = int(cand[flat // 2]), bool(flat % 2)
            r = float(d[flat // 2, flat % 2])
            rest = np.where(~done)[0]
            rest = rest[rest != i]
            if len(rest):
                dr = np.hypot(E[rest, :, 0] - pos[0], E[rest, :, 1] - pos[1])
                fi = flip[rest].astype(int)
                cur = dr[np.arange(len(rest)), fi]
                oth = dr[np.arange(len(rest)), 1 - fi]
                steal = cur <= r + TIE
                can = steal & (oth > r + TIE) & ~banned[rest, 1 - fi]
                flip[rest[can]] = ~flip[rest[can]]
                thieves = rest[steal & ~can]
                if len(thieves):
                    # cannot be pushed away: the walk WILL take it now, so plan it
                    misses += len(thieves)
                    # ... as it lies now: the walk takes a stroke by its current start
                    st = np.where(flip[thieves, None], E[thieves, 1], E[thieves, 0])
                    dt = np.hypot(st[:, 0] - pos[0], st[:, 1] - pos[1])
                    k = int(np.argmin(dt))
                    i, f, r = int(thieves[k]), bool(flip[thieves[k]]), float(dt[k])
            flip[i] = f
            done[i] = True
            rest = np.where(~done)[0]
            if len(rest):
                banned[rest] |= np.hypot(E[rest, :, 0] - pos[0], E[rest, :, 1] - pos[1]) <= r + TIE
            order.append(i)
            pos = E[i, 0] if flip[i] else E[i, 1]
    out = [items[i][1][::-1] if flip[i] else items[i][1] for i in order]
    return out, misses


# --- the plate --------------------------------------------------------------------
def orrery_resonant_iterate(rng: SeededRNG, bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    LY = layout()
    L = LY["law"]
    bands = LY["bands"]
    r_out = LY["r_out"]
    cx = 0.5 * (x0 + x1)
    cy = y1 - 4.0 - r_out
    theta0 = -math.pi / 2  # conjunction on the 6 o'clock ray
    c = (cx, cy)

    # ---- type as geometry first (the slot is cut from it) ---------------------
    rows = []  # (band, token polys, weight polys)
    for b in bands:
        yc = cy - (b["R"] + 0.5 * b["s"])
        yb = yc - 0.5 * TOK_H * 4.0 / 6.0
        tok = ptext(b["tok"], cx + COL, yb, TOK_H)
        wtxt = f"{L['row'][b['j']]:.3f}"[1:]
        wgt = ptext(wtxt, cx - COL - ptext_width(wtxt, W_H), yb, W_H)
        rows.append((b, tok, wgt))
    tb = _pbox(rows[0][1])
    sink = ptext("sink", cx + COL, tb[3] + 1.2, SINK_H)

    boxes_l = [_pbox(w) for _, _, w in rows]
    boxes_r = [_pbox(t) for _, t, _ in rows] + [_pbox(sink)]
    xl = min(bx[0] for bx in boxes_l + boxes_r) - HALO  # left chord, vertical
    # right chord: the straight line x = cx + a + m*(cy - y) that keeps HALO right
    # of every token box and costs the rings the least angle
    best = None
    for m in np.linspace(0.0, 0.4, 161):
        a = max(max(bx[2] + HALO - cx - m * (cy - bx[1]), bx[2] + HALO - cx - m * (cy - bx[3]))
                for bx in boxes_r)
        loss = sum(math.asin(min(1.0, (a + m * rr) / rr)) for rr in
                   (b["R"] + 0.5 * b["s"] for b in bands))
        if best is None or loss < best[0]:
            best = (loss, a, m)
    _, ra, rm = best
    # slot = {x >= xl} & {x <= cx + ra + rm*(cy - y)} & {y <= cy}
    slot = (HalfPlane(-1.0, 0.0, xl) & HalfPlane(1.0, rm, -(cx + ra + rm * cy))
            & HalfPlane(0.0, 1.0, -cy))

    # ---- 0 blue: the keys, outermost first, alternating direction -------------
    strokes: List[Poly] = []
    for b in reversed(bands):
        if b["s"] == 0.0:
            base = turn_trace(c, b["R"], b["kappa"], 0, theta0)
            turns = [_offset_polyline(base, o) for o in (RETRACE, 0.0, -RETRACE)]
        else:
            turns = [turn_trace(c, b["R"] + k * b["s"], b["kappa"], k, theta0) for k in (1, 0)]
        for t in turns:
            pieces = [p for p in clip(t, slot, keep="outside") if polyline_length(p) >= 8.0]
            pieces.sort(key=polyline_length, reverse=True)
            strokes.append(_rdp(pieces[0], 0.02))
    blue: List[GCodeCommand] = []
    for i, p in enumerate(strokes):
        # stroke 0 starts on the LEFT chord (nearest the origin), then alternate
        starts_left = abs(p[0][0] - xl) < abs(p[-1][0] - xl)
        if starts_left != (i % 2 == 0):
            p = p[::-1]
        blue += _poly(p, color=BLUE, f=2200)

    # ---- the type block hangs off the spine and sits on the bottom margin -----
    # The pipeline walks each pen greedily from the sheet origin (nearest stroke
    # START next, no reversal). Type is where that walk strays, so the caption
    # measure and leading are chosen from a few candidates by the longest hop of
    # the walk the pipeline will actually take (see plan_walk / nn_walk).
    text = " ".join(caption_paragraphs(L))
    tx = cx + COL
    # the title runs from the word column to the disc's right edge, exactly
    title_h = 6.5 * (cx + r_out - tx) / ptext_width(TITLE, 6.5)
    best = None
    for pitch in CAP_PITCHES:
        for cap_w in CAP_WIDTHS:
            lines = wrap(text, CAP_H, cap_w)
            y_title = y0 + 4.5 + (len(lines) - 1) * pitch + 9.5
            walk: List[List[Poly]] = [ptext(ln, tx, y_title - 9.5 - k * pitch, CAP_H)
                                      for k, ln in enumerate(lines)][::-1]  # bottom first
            walk.append(ptext(TITLE, tx, y_title, title_h, weight=0.5, tip=0.25))
            # up the token column to the sink mark, then down the weights
            walk += [t for _, t, _ in reversed(rows)] + [sink] + [w for _, _, w in rows]
            chain, _ = plan_walk(walk)
            o = nn_walk(chain)
            hop = max(math.dist(chain[a_][-1], chain[b_][0]) for a_, b_ in zip(o, o[1:]))
            if best is None or hop < best[0] - 1e-9:
                best = (hop, y_title, [chain[k] for k in o])
    _, y_title, chain = best

    # ---- 1 crimson: question -> spine -> sun, one walk -----------------------
    qh = 3.0
    q = ptext(QUESTION, cx - COL - ptext_width(QUESTION, qh), y_title, qh)
    spine = [(cx, y_title - 3.0), (cx, cy - SUN_R - 1.3)]
    turns_sun = SUN_R / SUN_PITCH
    m_pts = int(turns_sun * 90)
    sun = []
    for k in range(m_pts + 1):
        t = k / m_pts
        rr = SUN_R * (1 - t)
        a = -math.pi / 2 + 2 * math.pi * turns_sun * t
        sun.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    crimson = _emit(plan_walk([q, [spine], [sun]])[0], CRIMSON)

    # ---- 2 black: caption (bottom up) -> title -> column (bottom up) ----------
    black = _emit(chain, BLACK)
    return blue + crimson + black
