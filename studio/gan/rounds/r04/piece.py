"""GAN — THE FIXED POINT REPELS, woven.  Studio candidate, round 04 (iterate).

parent: r03 (gan_darn, the two-players-interlaced darn).  MERGE from r02: the
complete h -> 0 gradient-flow circle.  Everything else is r03's order re-laid
under three checkable rules.

Contract:  gan_repels(rng, bounds, colors=3) -> list[GCodeCommand]

WHAT IS COMPUTED (exact, unchanged from r01/r03)
------------------------------------------------
The Dirac-GAN (Mescheder, Geiger, Nowozin 2018).  Real data delta_0, generator
delta_theta, discriminator D_psi(x) = psi*x, objective
V(theta, psi) = f(psi*theta) + f(0),  f(t) = -log(1 + e^-t),  f'(s) = sigmoid(-s).
Simultaneous gradient descent-ascent, one shared step h (both updates use the
OLD state):

    theta' = theta - h * psi   * f'(s)      (generator descends)
    psi'   = psi   + h * theta * f'(s)      (discriminator ascends)

The Nash equilibrium theta = psi = 0 EXISTS (Jacobian eigenvalues +-0.5i, a
centre).  Continuous time (h -> 0) conserves theta^2 + psi^2: the flow circles
it forever at r0.  The discrete step multiplies r^2 by 1 + h^2 f'(s)^2 > 1, so
the fixed point REPELS: the run spirals out and never arrives.

THE ORDER: A WOVEN TAPE, LAID UNDER THREE RULES
-----------------------------------------------
Every step is split into its two players' moves: G's move changes theta
(horizontal, WEFT, crimson), D's move changes psi (vertical, WARP, blue).
Within one quadrant theta and psi are both monotone, so the steps group into
RUNS: consecutive steps with the same leader (sign of s = psi*theta), closed as
soon as the leader's summed move reaches `min_mm`.

  1. THE HOLE IS EXACT.  A run from state a to state b is drawn as the L of its
     two summed moves, taking the corner of larger radius (the outward L).
     Every thread is laid on the OUTWARD side of its leg, `clear_mm` off it, so
     no thread falls inside r0.
  2. ONE TAPE, ONE WIDTH.  Each leg carries a band `tape_mm` wide on its
     outward side, and the convex corner of every L is filled by a TURN square,
     so the tape is one piece of constant width from the hole to the frame.
  3. A FLOAT ALONG THE TAPE IS THE LEG IT CLAIMS.  The thread that runs ALONG
     a leg spans exactly that leg: weft on a G band spans the theta the run
     moved, warp on a D band the psi.  Runs meet end to end in a row, so a float
     is always one consecutive stretch of its player's moves, summed (the fit
     is in stats: slope 1, intercept 0).  The other family crosses each band
     ACROSS (and the turn squares) and carries the tape's width, not a move.
     At every crossing the leader's thread is on top (sign of psi*theta): the
     over-thread is continuous, drawn out and back, and rides in pairs (two
     dents of every three on the 1.8 mm reed); the under-thread breaks into
     2.6 mm dashes in the third dent.  Nothing under `min_mm` is laid.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.generators import _GLYPHS
from promptplot.generative.kit import (
    _poly,
    _spaced,
    _text_width,
    giant_type,
    giant_type_width,
    plus_mark,
)

Bounds = Tuple[float, float, float, float]

# psi is missing from the shared stroke font and its theta sits at x-height,
# which reads as a dot at label size: both drawn locally at cap height.
_PSI = [
    [(0.6, 5.4), (0.6, 3.8), (0.95, 2.8), (1.5, 2.3), (2.0, 2.2), (2.5, 2.3),
     (3.05, 2.8), (3.4, 3.8), (3.4, 5.4)],
    [(2.0, 6.0), (2.0, 0.0)],
]
_THETA = [
    [(2.0 + 1.5 * math.sin(2 * math.pi * q / 24), 3.0 + 3.0 * math.cos(2 * math.pi * q / 24))
     for q in range(25)],
    [(0.5, 3.0), (3.5, 3.0)],
]
_LOCAL = {"ψ": _PSI, "θ": _THETA}


def _text(s: str, x: float, y: float, hgt: float, pen: int, f: int) -> List[GCodeCommand]:
    """Single-stroke text on the house font, plus a local psi."""
    sc = hgt / 6.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in s:
        strokes = _LOCAL.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        for st in strokes:
            out += _poly([(cx + gx * sc, y + gy * sc) for gx, gy in st], color=pen, f=f)
        cx += 5.6 * sc
    return out


# ---------------------------------------------------------------------------
# the mathematics (exact)
# ---------------------------------------------------------------------------


def _sigmoid(t: float) -> float:
    if t >= 0.0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def dirac_gan_run(h: float, r_start: float, a0: float, stop, max_iters: int):
    """Simultaneous GDA on the Dirac-GAN.  Returns the states (theta, psi),
    n+1 of them for n steps, and the f'(s) of each step."""
    th, ps = r_start * math.cos(a0), r_start * math.sin(a0)
    states = [(th, ps)]
    grads = []
    for _ in range(max_iters):
        g = _sigmoid(-(th * ps))
        th, ps = th - h * ps * g, ps + h * th * g
        states.append((th, ps))
        grads.append(g)
        if stop(th, ps):
            break
    return states, grads


def build_runs(states, k: float, min_mm: float):
    """Group steps into runs: same quadrant, same leader (sign psi*theta at the
    step's start), closed once the LEADER's summed move reaches min_mm."""
    runs: List[dict] = []
    cur: Optional[dict] = None
    for n in range(len(states) - 1):
        (t0, p0), (t1, p1) = states[n], states[n + 1]
        lead = "D" if t0 * p0 > 0 else "G"
        q = (t0 >= 0.0, p0 >= 0.0)
        over = abs(p1 - p0) if lead == "D" else abs(t1 - t0)
        if cur is not None and cur["lead"] == lead and cur["q"] == q and cur["over"] * k < min_mm:
            cur["b"] = n + 1
            cur["over"] += over
        else:
            if cur is not None:
                runs.append(cur)
            cur = dict(a=n, b=n + 1, lead=lead, q=q, over=over)
    if cur is not None:
        runs.append(cur)
    # a short remainder at the end of a quadrant joins the run before it
    merged: List[dict] = []
    for r in runs:
        if merged and r["over"] * k < min_mm and merged[-1]["lead"] == r["lead"] \
                and merged[-1]["q"] == r["q"] and merged[-1]["b"] == r["a"]:
            merged[-1]["b"] = r["b"]
            merged[-1]["over"] += r["over"]
        else:
            merged.append(r)
    for r in merged:
        (ta, pa), (tb, pb) = states[r["a"]], states[r["b"]]
        # the outward L: of the two corners, the one of larger radius
        if math.hypot(tb, pa) >= math.hypot(ta, pb):
            r["gy"], r["dx"] = pa, tb          # G first: G leg at psi_a, D leg at theta_b
        else:
            r["gy"], r["dx"] = pb, ta          # D first
        r["t"] = (ta, tb)
        r["p"] = (pa, pb)
    return merged


# ---------------------------------------------------------------------------
# interval helpers
# ---------------------------------------------------------------------------


def _merge(iv):
    """Union of (a, b, tags) intervals; touching intervals join, tags pool."""
    out = []
    for a, b, tags in sorted(iv, key=lambda t: t[0]):
        if out and a <= out[-1][1] + 1e-6:
            out[-1] = (out[-1][0], max(out[-1][1], b), out[-1][2] | tags)
        else:
            out.append((a, b, set(tags)))
    return out


def _cut(a: float, b: float, cuts: Sequence[Tuple[float, float]]):
    out, p = [], a
    for c0, c1 in sorted(cuts):
        if c1 <= p or c0 >= b:
            continue
        if c0 > p:
            out.append((p, c0))
        p = max(p, c1)
    if b > p:
        out.append((p, b))
    return out


def _cloth_keep(segs, win, rad: float, min_area: float, min_segs: int = 4,
                res: float = 0.5) -> List[bool]:
    """Which axis-aligned thread segments belong to a piece of cloth with body.
    segs: ('w', y, xa, xb) horizontal or ('v', x, ya, yb) vertical, in mm.
    Rasterised at `res` mm, each thread dilated by `rad` mm, 4-connected."""
    import numpy as np

    wx0, wy0, wx1, wy1 = win
    nx, ny = int((wx1 - wx0) / res) + 3, int((wy1 - wy0) / res) + 3
    R = max(1, int(round(rad / res)))
    occ = np.zeros((ny, nx), dtype=bool)
    cells_of = []
    for kind, pos, a, b in segs:
        n = max(2, int((b - a) / res) + 2)
        first = None
        for t in range(n + 1):
            u = a + (b - a) * t / n
            px, py = (u, pos) if kind == "w" else (pos, u)
            cx = min(max(int(round((px - wx0) / res)) + 1, 0), nx - 1)
            cy = min(max(int(round((py - wy0) / res)) + 1, 0), ny - 1)
            first = first or (cy, cx)
            occ[max(0, cy - R):cy + R + 1, max(0, cx - R):cx + R + 1] = True
        cells_of.append(first)
    lab = -np.ones((ny, nx), dtype=np.int64)
    area = []
    for sy in range(ny):
        for sx in range(nx):
            if not occ[sy, sx] or lab[sy, sx] >= 0:
                continue
            L = len(area)
            lab[sy, sx] = L
            stack, n_c = [(sy, sx)], 0
            while stack:
                cy, cx = stack.pop()
                n_c += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = cy + dy, cx + dx
                    if 0 <= yy < ny and 0 <= xx < nx and occ[yy, xx] and lab[yy, xx] < 0:
                        lab[yy, xx] = L
                        stack.append((yy, xx))
            area.append(n_c * res * res)
    comp = [int(lab[cy, cx]) for cy, cx in cells_of]
    count: Dict[int, int] = {}
    for c in comp:
        count[c] = count.get(c, 0) + 1
    # cloth has body AND more than a couple of threads: a lone thread at a crop is fringe
    return [area[c] >= min_area and count[c] >= min_segs for c in comp]


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def gan_repels(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    step: float = 0.26,           # h, the shared learning rate (r01's value)
    r_start: float = 0.74,        # ||(theta, psi)|| at step 0: the flow circle
    max_iters: int = 6000,
    scale_mm: float = 52.0,       # mm per world unit
    centre_mm: Tuple[float, float] = (68.0, 107.0),  # equilibrium, mm from the drawable corner
    dent_mm: float = 1.8,         # the reed, phase-locked to the equilibrium
    tape_mm: float = 9.0,         # tape width, one for every leg (5 dents)
    clear_mm: float = 1.5,        # the tape starts this far outward of its leg
    min_mm: float = 2.5,          # float / dash floor, and the run-closing length
    gap_mm: float = 0.5,          # half-gap where the under-thread ducks
    gutter_mm: float = 12.0,      # type <-> thread, top and bottom
    min_on_frac: float = 0.45,    # a tape mostly off the window is not laid
    min_threads: int = 4,         # threads of a tape that must land in the window
    min_piece_mm2: float = 60.0,   # a piece of cloth smaller than this is debris
    over_passes: int = 2,         # the thread on top is drawn out and back: weight = who leads
    over_sep: float = 0.3,
    title_h: float = 8.4,
    title_weight: float = 0.9,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE FIXED POINT REPELS — the Dirac-GAN's exact simultaneous-GDA run as
    one woven tape: G's summed moves are weft, D's are warp, the leader's
    thread on top, every float the run it claims.  The equilibrium is a hole
    of bare paper with one crimson +, ringed by the h -> 0 flow circle."""
    x0, y0, x1, y1 = bounds
    TYPE = 0
    WEFT = 1 % max(1, colors)
    WARP = 2 % max(1, colors)
    k = scale_mm
    P = dent_mm

    # ---- type bands first: the window for the cloth is what they leave ----
    TH_S, TH_F, LP = 2.4, 1.7, 4.2
    yT = y1 - title_h
    ySub = yT - 4.0 - TH_S
    NF = 4
    yF = [y0 + 1.0 + LP * (NF - 1 - q) for q in range(NF)]   # footer baselines, top first
    win = (x0, yF[0] + TH_F + gutter_mm, x1, ySub - gutter_mm)
    wx0, wy0, wx1, wy1 = win

    ex, ey = x0 + centre_mm[0], y0 + centre_mm[1]

    def X(t: float) -> float:
        return ex + k * t

    def Y(p: float) -> float:
        return ey + k * p

    reach = (tape_mm + clear_mm) / k
    r_far = max(math.hypot(cx - ex, cy - ey) for cx in (wx0, wx1) for cy in (wy0, wy1)) / k

    def gone(th: float, ps: float) -> bool:
        return math.hypot(th, ps) > r_far + reach + 0.05

    a0 = 0.62 + rng.uniform(-0.55, 0.55)
    states, grads = dirac_gan_run(step, r_start, a0, gone, max_iters)
    runs = build_runs(states, k, min_mm)

    def in_win(t: float, p: float) -> bool:
        return wx0 <= X(t) <= wx1 and wy0 <= Y(p) <= wy1

    n_edge = next((n for n, (t, p) in enumerate(states) if not in_win(t, p)), len(states) - 1)
    r_edge = math.hypot(*states[n_edge])

    # ---- lay each run as a tape on the reed --------------------------------
    # A run's outward L has a G leg (horizontal, at psi = gy) and a D leg
    # (vertical, at theta = dx) meeting at the convex corner K = (dx, gy).  The
    # tape is c + T outward of the L.  Three kinds of thread fill it:
    #   ALONG  — the thread that runs along a leg spans EXACTLY that leg:
    #            weft on the G leg's band, warp on the D leg's band;
    #   ACROSS — the other family crosses each leg's band: its width;
    #   TURN   — the corner square outward of K, where the tape turns.
    # Along-threads have priority; across/turn threads fill what is left.
    def frac_on(ax, ay, bx, by):
        full = max(1e-9, (bx - ax) * (by - ay))
        cw = max(0.0, min(bx, wx1) - max(ax, wx0))
        ch = max(0.0, min(by, wy1) - max(ay, wy0))
        return cw * ch / full

    def dents(lo, hi, c0):
        return range(math.ceil((lo - c0) / P - 1e-9), math.floor((hi - c0) / P + 1e-9) + 1)

    along_r: Dict[int, list] = {}
    fill_r: Dict[int, list] = {}
    along_c: Dict[int, list] = {}
    fill_c: Dict[int, list] = {}
    n_dropped_tape = 0
    CT = clear_mm + tape_mm
    for ri, r in enumerate(runs):
        (ta, tb), (pa, pb) = r["t"], r["p"]
        gy, dx = r["gy"], r["dx"]
        sy = 1.0 if (gy if gy != 0 else pb) > 0 else -1.0
        sx = 1.0 if (dx if dx != 0 else tb) > 0 else -1.0
        gxa, gxb = sorted((X(ta), X(tb)))           # the G leg's theta extent (mm)
        dya, dyb = sorted((Y(pa), Y(pb)))           # the D leg's psi extent (mm)
        Gy, Dx = Y(gy), X(dx)
        hy = sorted((Gy + sy * clear_mm, Gy + sy * CT))   # the G leg's band (rows)
        vx = sorted((Dx + sx * clear_mm, Dx + sx * CT))   # the D leg's band (cols)
        kx = sorted((Dx, Dx + sx * CT))                   # the turn square
        ky = sorted((Gy, Gy + sy * CT))
        # a tape is laid only if most of it lands in the window AND at least
        # `min_threads` of its threads do: one or two threads left at a crop
        # are a fringe, not cloth
        h_ok = (gxb - gxa > 1e-9 and frac_on(gxa, hy[0], gxb, hy[1]) >= min_on_frac
                and len([j for j in dents(hy[0], hy[1], ey) if wy0 <= ey + j * P <= wy1]) >= min_threads)
        v_ok = (dyb - dya > 1e-9 and frac_on(vx[0], dya, vx[1], dyb) >= min_on_frac
                and len([i for i in dents(vx[0], vx[1], ex) if wx0 <= ex + i * P <= wx1]) >= min_threads)
        n_dropped_tape += (gxb - gxa > 1e-9 and not h_ok) + (dyb - dya > 1e-9 and not v_ok)
        if h_ok:
            for j in dents(hy[0], hy[1], ey):
                along_r.setdefault(j, []).append((gxa, gxb, {ri}))
            for i in dents(gxa, gxb, ex):
                fill_c.setdefault(i, []).append((hy[0], hy[1], set()))
        if v_ok:
            for i in dents(vx[0], vx[1], ex):
                along_c.setdefault(i, []).append((dya, dyb, {ri}))
            for j in dents(dya, dyb, ey):
                fill_r.setdefault(j, []).append((vx[0], vx[1], set()))
        if h_ok or v_ok:
            for j in dents(max(ky[0], hy[0]), min(ky[1], hy[1]), ey):
                fill_r.setdefault(j, []).append((kx[0], kx[1], set()))
            for i in dents(max(kx[0], vx[0]), min(kx[1], vx[1]), ex):
                fill_c.setdefault(i, []).append((ky[0], ky[1], set()))

    # ---- threads: along first, fill in what is left; split on the axis
    # (the seam where the leader changes), clipped to the window ------------
    SEAM = 0.6

    def pieces(along, fill, axis_c, lo, hi):
        out = []
        for idx in set(along) | set(fill):
            al = _merge(along.get(idx, []))
            fl = []
            for a, b, _t in _merge(fill.get(idx, [])):
                for fa, fb in _cut(a, b, [(p - SEAM, q + SEAM) for p, q, _ in al]):
                    fl.append((fa, fb, set()))
            for kind, ivs in (("along", al), ("fill", fl)):
                for a, b, tags in ivs:
                    for sa, sb in ((a, min(b, axis_c - SEAM)), (max(a, axis_c + SEAM), b)):
                        if sb - sa <= 0:
                            continue
                        axis_cut = (sa != a) or (sb != b)
                        ca, cb = max(sa, lo), min(sb, hi)
                        if cb - ca <= 0:
                            continue
                        out.append(dict(i=idx, a=ca, b=cb, runs=tags, kind=kind,
                                        clip=(ca != sa or cb != sb), axis=axis_cut))
        return out

    weft = [w for w in pieces(along_r, fill_r, ex, wx0, wx1) if wy0 <= ey + w["i"] * P <= wy1]
    warp = [w for w in pieces(along_c, fill_c, ey, wy0, wy1) if wx0 <= ex + w["i"] * P <= wx1]
    for w in weft:
        w["pos"] = ey + w["i"] * P
        side = 1.0 if (w["a"] + w["b"]) / 2 > ex else -1.0
        w["over"] = side * (w["pos"] - ey) < 0          # psi*theta < 0: G ahead, weft on top
    for w in warp:
        w["pos"] = ex + w["i"] * P
        side = 1.0 if (w["a"] + w["b"]) / 2 > ey else -1.0
        w["over"] = side * (w["pos"] - ex) > 0          # psi*theta > 0: D ahead, warp on top

    # The over-threads ride in PAIRS (two dents of every three): the third dent
    # is the window where the under-thread shows, 3.6 mm between pairs, so an
    # under-dash is 3.6 - 2*gap long.  The under-threads use every dent.
    def paired(w):
        return w["i"] % 3 != 2

    over_w = [w for w in weft if w["over"] and paired(w) and w["b"] - w["a"] >= min_mm]
    over_v = [w for w in warp if w["over"] and paired(w) and w["b"] - w["a"] >= min_mm]

    def under_dashes(under, over_other):
        # the under-thread ducks at every over-thread, and also across the
        # seam gap where an over-thread changes run (it is still under there)
        dashes = []
        for u in under:
            cuts = [(o["pos"] - gap_mm, o["pos"] + gap_mm) for o in over_other
                    if u["a"] - gap_mm < o["pos"] < u["b"] + gap_mm
                    and o["a"] - 2 * SEAM - 0.05 <= u["pos"] <= o["b"] + 2 * SEAM + 0.05]
            n_cuts[0] += len(cuts)
            for a, b in _cut(u["a"], u["b"], cuts):
                if b - a >= min_mm:
                    dashes.append((u["i"], u["pos"], a, b))
        return dashes

    n_cuts = [0]

    dash_w = under_dashes([w for w in weft if not w["over"]], over_v)
    dash_v = under_dashes([w for w in warp if not w["over"]], over_w)

    # ---- crop hygiene, second pass: a scrap of cloth the frame has shaved
    # off a tape (a corner of one tape, a few stray threads) is debris, not a
    # crop.  Threads are rasterised on a 1 mm grid, dilated by one dent so a
    # tape's threads join, and a piece of cloth smaller than `min_piece_mm2`
    # is not laid.
    segs = ([("w", w["pos"], w["a"], w["b"]) for w in over_w]
            + [("v", w["pos"], w["a"], w["b"]) for w in over_v]
            + [("w", yy, a, b) for _i, yy, a, b in dash_w]
            + [("v", xx, a, b) for _i, xx, a, b in dash_v])
    keep = _cloth_keep(segs, win, rad=1.0, min_area=min_piece_mm2)
    nw, nv = len(over_w), len(over_v)
    nd = len(dash_w)
    n_scrap = len(segs) - sum(keep)
    over_w = [w for q, w in enumerate(over_w) if keep[q]]
    over_v = [w for q, w in enumerate(over_v) if keep[nw + q]]
    dash_w = [d for q, d in enumerate(dash_w) if keep[nw + nv + q]]
    dash_v = [d for q, d in enumerate(dash_v) if keep[nw + nv + nd + q]]

    # ---- emit.  Each line runs in the direction of its dent's parity, so the
    # optimiser snakes through a tape instead of flying back to one side.
    out: List[GCodeCommand] = []

    def line(pen, horiz, pos, a, b, idx, passes=1):
        if idx % 2:
            a, b = b, a
        seq = [(a, pos), (b, pos)]
        if passes == 2:        # the thread on top: out and back, over_sep apart
            seq = [(a, pos - over_sep / 2), (b, pos - over_sep / 2),
                   (b, pos + over_sep / 2), (a, pos + over_sep / 2)]
        pts = seq if horiz else [(q, t) for t, q in seq]
        return _poly(pts, color=pen, f=feed)

    for w in over_w:
        out += line(WEFT, True, w["pos"], w["a"], w["b"], w["i"], over_passes)
    for w in over_v:
        out += line(WARP, False, w["pos"], w["a"], w["b"], w["i"], over_passes)
    for i, yy, a, b in dash_w:
        out += line(WEFT, True, yy, a, b, i)
    for i, xx, a, b in dash_v:
        out += line(WARP, False, xx, a, b, i)

    # ---- float = leg: the fit, over-floats the frame and seam did not cut --
    def leg_mm(ri: int, fam: str) -> float:
        r = runs[ri]
        return k * abs(r["t"][1] - r["t"][0]) if fam == "G" else k * abs(r["p"][1] - r["p"][0])

    fit = []
    for fam, group in (("G", over_w), ("D", over_v)):
        for w in group:
            if w["clip"] or w["axis"] or w["kind"] != "along":
                continue
            fit.append((sum(leg_mm(ri, fam) for ri in w["runs"]), w["b"] - w["a"], len(w["runs"])))
    if len(fit) >= 2:
        mx = sum(p for p, _m, _n in fit) / len(fit)
        my = sum(m for _p, m, _n in fit) / len(fit)
        sxx = sum((p - mx) ** 2 for p, _m, _n in fit)
        slope = sum((p - mx) * (m - my) for p, m, _n in fit) / max(sxx, 1e-12)
        icpt = my - slope * mx
        max_res = max(abs(m - p) for p, m, _n in fit)
    else:
        slope = icpt = max_res = float("nan")

    # ---- min thread radius (the hole) ---------------------------------------
    def rad(px, py):
        return math.hypot(px - ex, py - ey)

    r_min = float("inf")
    for w in over_w:
        for xx in (w["a"], w["b"], min(max(ex, w["a"]), w["b"])):
            r_min = min(r_min, rad(xx, w["pos"]))
    for w in over_v:
        for yy in (w["a"], w["b"], min(max(ey, w["a"]), w["b"])):
            r_min = min(r_min, rad(w["pos"], yy))
    for _i, yy, a, b in dash_w:
        for xx in (a, b, min(max(ex, a), b)):
            r_min = min(r_min, rad(xx, yy))
    for _i, xx, a, b in dash_v:
        for yy in (a, b, min(max(ey, a), b)):
            r_min = min(r_min, rad(xx, yy))

    # ---- the h -> 0 flow: the full circle at r0, through the start point ---
    rc = r_start * k
    circ = 2 * math.pi * rc
    n_d = int(circ / 4.5)
    on = 2.5 / rc
    for m in range(n_d):
        a = a0 + 2 * math.pi * m / n_d
        pts = [(ex + rc * math.cos(a + on * t / 6), ey + rc * math.sin(a + on * t / 6)) for t in range(7)]
        out += _poly(pts, color=TYPE, f=feed)

    # ---- the equilibrium: bare paper, one crimson + ------------------------
    out += plus_mark(ex, ey, s=1.8, pen=WEFT, f=feed)
    TL = 2.1
    lab1, lab2 = "NASH EQUILIBRIUM", "θ = ψ = 0"
    out += _text(lab1, ex - _text_width(lab1, TL) / 2, ey + 5.0, TL, TYPE, feed)
    out += _text(lab2, ex - _text_width(lab2, TL) / 2, ey - 5.0 - TL, TL, TYPE, feed)
    lab3 = "h → 0: THE FLOW CIRCLES"
    out += _text(lab3, ex - _text_width(lab3, TL) / 2, ey - 0.75 * rc, TL, TYPE, feed)

    # ---- type: own pen, plotted last -----------------------------------------
    title = "THE FIXED POINT REPELS"
    sub = _spaced("NEITHER PLAYER EVER ARRIVES")
    xT = x0 + 0.5
    out += giant_type(title, xT, yT, title_h, pen=TYPE, weight=title_weight, tip=0.3, f=feed)
    out += _text(sub, xT, ySub, TH_S, TYPE, feed)
    foot = [
        _spaced(f"H {step:.2f}   STEP 0 ON THE CIRCLE R {r_start:.2f}"),
        _spaced(f"STEP {n_edge}  R {r_edge:.2f}  LEAVES THE SHEET"),
        _spaced("ON TOP: WARP IF PSI THETA > 0, WEFT IF < 0"),
        _spaced("ALONG THE TAPE: A FLOAT = ITS PLAYER'S RUN OF MOVES, SUMMED"),
    ]
    for t, yb in zip(foot, yF):
        out += _text(t, xT, yb, TH_F, TYPE, feed)
    legend = [
        (WEFT, _spaced("WEFT  G  MOVES THETA"), True),
        (WARP, _spaced("WARP  D  MOVES PSI"), False),
    ]
    leg_w = max(_text_width(t, TH_F) for _p, t, _h in legend)
    xL = x1 - leg_w
    for (pen, label, horiz), yb in zip(legend, yF[:2]):
        # a real sample of each thread as it lies on top: an over-pair, double pass
        cy = yb + TH_F / 2.0
        for q in (-0.9, 0.9):
            if horiz:
                out += line(pen, True, cy + q, xL - 9.0, xL - 3.0, 0, over_passes)
            else:
                out += line(pen, False, xL - 6.0 + q, cy - 1.3, cy + 1.3, 0, over_passes)
        out += _text(label, xL, yb, TH_F, TYPE, feed)

    gan_repels.stats = dict(  # type: ignore[attr-defined]
        a0=a0, n_states=len(states), n_runs=len(runs), n_edge=n_edge, r_edge=r_edge,
        over_weft=len(over_w), over_warp=len(over_v), dash_weft=len(dash_w), dash_warp=len(dash_v),
        dropped_tapes=n_dropped_tape, fit_n=len(fit), slope=slope, intercept=icpt,
        max_res=max_res, n_scrap=n_scrap, n_crossings=n_cuts[0],
        fill_over_mm=sorted(round(w['b'] - w['a'], 2) for w in over_w + over_v if w['kind'] == 'fill'), r_min_mm=r_min, r0_mm=rc, window=win, centre=(ex, ey),
        fit=fit,
    )
    return out
