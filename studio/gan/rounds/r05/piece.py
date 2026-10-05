"""GAN — THE FIXED POINT REPELS, woven.  Studio candidate, round 05 (iterate).

parent: r04 (run, hole, flow circle, title kept).  Built to `studio/gan/encoding.md`
revision 1: RED MEANDER PROPER.  The whole window is cloth; the run is not cut
out of paper, it is the region where one thread floats on top.

Contract:  gan_meander(rng, bounds, colors=3) -> list[GCodeCommand]

WHAT IS COMPUTED (exact, unchanged from r01/r04)
------------------------------------------------
Dirac-GAN (Mescheder, Geiger, Nowozin 2018): V(theta, psi) = f(psi*theta) + f(0),
f(t) = -log(1 + e^-t), f'(s) = sigmoid(-s).  Simultaneous GDA, one shared h:

    theta' = theta - h * psi   * f'(s)      (G descends)
    psi'   = psi   + h * theta * f'(s)      (D ascends)

The equilibrium theta = psi = 0 exists (Jacobian +-0.5i, a centre); the h -> 0
flow circles at r0; each discrete step multiplies r by sqrt(1 + h^2 f'^2) > 1,
so the fixed point REPELS.

THE ORDER: INTERLACING, FIGURE BY FLOAT
---------------------------------------
One reed, pitch p, phase-locked half a pitch off the equilibrium: warps (D,
vertical, psi) at x_i = ex + (i+1/2)p, wefts (G, horizontal, theta) at
y_j = ey + (j+1/2)p.  At every crossing exactly one thread is on top:

  * RIBBON — the chord polygon z_0 z_1 ... of the iterates, scaled about the
    equilibrium by s in [1-beta, 1+beta].  Cell k is the quad
    {s z_k + (1-s)... } = { s * Q : Q on chord z_k z_{k+1}, s in [0.9, 1.1] };
    neighbouring cells share a radial edge, so the ribbon is one seamless band.
    A crossing inside it: warp over iff psi*theta > 0 (D spots the fake),
    weft over iff psi*theta < 0 (G fools D), evaluated at the crossing.
  * GROUND — 2/2 basket (hopsack): warp over iff floor(i/2)+floor(j/2) is even.
  * HOLE — no crossing with rho < r0 + 1.5 mm is woven: bare paper.

A thread is drawn as its extent minus a gap g centred on every crossing where it
is UNDER.  A piece covering >= 3 over-crossings INSIDE THE RIBBON is drawn out
and back (double pass); everything else single.  No float claims a length.

Two build decisions beyond the encoding (both in NOTES.md):
  * TIE-DOWNS.  A ribbon float ends by going under: at the first ground crossing
    beyond each end of a float, the floating thread is set under.  Without it a
    basket over-pair fuses onto the float and eats the channel between laps.
  * REED 2.8 mm (encoding §6 fallback from 2.6): 2.6 broke the 15k-command and
    2,300 pen-down ceilings (16,008 cmds, 2,324 pen-downs).
"""

from __future__ import annotations

import bisect
import math
from typing import Dict, List, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.generators import _GLYPHS
from promptplot.generative.kit import _poly, giant_type

Bounds = Tuple[float, float, float, float]

# psi is missing from the shared stroke font and its theta sits at x-height:
# both drawn locally at cap height (from r04).
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
ADV = 5.6


def _glyph_extent(ch: str) -> Tuple[float, float]:
    strokes = _LOCAL.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
    xs = [gx for st in strokes for gx, _gy in st]
    return (min(xs), max(xs)) if xs else (0.0, 0.0)


def _text(s: str, x: float, y: float, hgt: float, pen: int, f: int,
          track: float = 1.0) -> List[GCodeCommand]:
    """Single-stroke text on the house font plus local psi/theta; `track`
    scales the advance (1 = the font's own 5.6 units)."""
    sc = hgt / 6.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in s:
        strokes = _LOCAL.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        for st in _chain_glyph(strokes):
            out += _poly([(cx + gx * sc, y + gy * sc) for gx, gy in st], color=pen, f=f)
        cx += ADV * sc * track
    return out


def _chain_glyph(strokes, tol: float = 1e-6):
    """Join a glyph's strokes end to end where they share an endpoint (either
    direction), so one pen-down draws what the font split into several.  The
    ink is identical; only the lifts go."""
    pool = [list(st) for st in strokes if len(st) >= 2]
    out = []
    while pool:
        cur = pool.pop(0)
        grown = True
        while grown:
            grown = False
            for q, st in enumerate(pool):
                for cand in (st, st[::-1]):
                    if math.dist(cur[-1], cand[0]) < tol:
                        cur = cur + cand[1:]
                    elif math.dist(cur[0], cand[-1]) < tol:
                        cur = cand[:-1] + cur
                    else:
                        continue
                    pool.pop(q)
                    grown = True
                    break
                if grown:
                    break
        out.append(cur)
    return out


def _ink_width(s: str, hgt: float, track: float = 1.0) -> float:
    """Visible width: from the first glyph's left ink to the last glyph's right ink."""
    sc = hgt / 6.0
    if not s:
        return 0.0
    lo = _glyph_extent(s[0])[0]
    hi = _glyph_extent(s[-1])[1]
    return ((len(s) - 1) * ADV * track + hi - lo) * sc


def _left_ink(s: str, hgt: float) -> float:
    return _glyph_extent(s[0])[0] * hgt / 6.0


# ---------------------------------------------------------------------------
# the mathematics (exact)
# ---------------------------------------------------------------------------


def _sigmoid(t: float) -> float:
    if t >= 0.0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def dirac_gan_run(h: float, r_start: float, a0: float, r_stop: float, max_iters: int):
    """Simultaneous GDA on the Dirac-GAN, until r > r_stop.  States and f'(s)."""
    th, ps = r_start * math.cos(a0), r_start * math.sin(a0)
    states = [(th, ps)]
    grads = []
    for _ in range(max_iters):
        g = _sigmoid(-(th * ps))
        th, ps = th - h * ps * g, ps + h * th * g
        states.append((th, ps))
        grads.append(g)
        if math.hypot(th, ps) > r_stop:
            break
    return states, grads


class Ribbon:
    """The chord polygon of the run, scaled about the equilibrium by [1-b, 1+b].

    Iterates are in mm relative to the equilibrium.  Their polar angle is
    strictly increasing (every step turns by atan(h f') > 0), so a direction
    at unwrapped angle A meets the chord polygon exactly once per lap."""

    def __init__(self, pts_mm: List[Tuple[float, float]], beta: float):
        self.P = pts_mm
        self.beta = beta
        ang = [math.atan2(pts_mm[0][1], pts_mm[0][0])]
        for (x0, y0), (x1, y1) in zip(pts_mm, pts_mm[1:]):
            d = math.atan2(x0 * y1 - y0 * x1, x0 * x1 + y0 * y1)
            ang.append(ang[-1] + d)
        self.A = ang

    def centre_rho(self, A: float):
        """Chord-polygon radius on the ray at unwrapped angle A, and its step k."""
        if A < self.A[0] or A > self.A[-1]:
            return None
        k = min(max(bisect.bisect_right(self.A, A) - 1, 0), len(self.P) - 2)
        (x0, y0), (x1, y1) = self.P[k], self.P[k + 1]
        ux, uy = math.cos(A), math.sin(A)
        dx, dy = x1 - x0, y1 - y0
        den = dx * uy - dy * ux
        if abs(den) < 1e-12:
            return math.hypot(x0, y0), k
        t = -(x0 * uy - y0 * ux) / den
        qx, qy = x0 + t * dx, y0 + t * dy
        return qx * ux + qy * uy, k

    def locate(self, x: float, y: float):
        """(lap, step k, centre rho) if (x, y) lies in the ribbon, else None."""
        rho = math.hypot(x, y)
        phi = math.atan2(y, x)
        m0 = math.floor((self.A[0] - phi) / (2 * math.pi))
        for m in range(m0, m0 + 40):
            A = phi + 2 * math.pi * m
            if A < self.A[0]:
                continue
            if A > self.A[-1]:
                break
            rc, k = self.centre_rho(A)
            if (1 - self.beta) * rc <= rho <= (1 + self.beta) * rc:
                return m - m0, k, rc
            if rc * (1 - self.beta) > rho:
                break
        return None


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def gan_meander(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    step: float = 0.26,            # h, the shared learning rate
    r_start: float = 0.74,         # ||(theta, psi)|| at step 0: the flow circle
    max_iters: int = 6000,
    scale_mm: float = 52.0,        # mm per world unit
    centre: Tuple[float, float] = (78.0, 113.0),   # equilibrium, paper mm
    window_y: Tuple[float, float] = (37.3, 251.5),  # the cloth's cut edge
    pitch: float = 2.8,            # the reed (encoding §6 fallback from 2.6: the plot ceilings)
    beta: float = 0.10,            # ribbon = chord polygon x [1-beta, 1+beta]
    gap: float = 2.4,              # under-gap along the thread
    hole_clear: float = 1.5,       # cloth starts this far outside the flow circle
    min_ink: float = 2.5,          # shortest inked piece
    double_min: int = 3,           # over-crossings for a double pass
    pass_sep: float = 0.4,
    title_top: float = 284.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE FIXED POINT REPELS — Red Meander proper: a basket-woven cloth in
    which the Dirac-GAN's simultaneous-GDA run is the region where the
    winning player's thread floats on top, unwinding away from a hole of bare
    paper that holds the equilibrium."""
    x0, y0, x1, y1 = bounds
    WARP = 0 % max(1, colors)      # dodgerblue, plotted first
    WEFT = 1 % max(1, colors)      # crimson
    TYPE = 2 % max(1, colors)      # black, last
    k = scale_mm
    p = pitch
    ex, ey = centre
    wx0, wx1 = x0, x1
    wy0, wy1 = window_y
    r0mm = r_start * k
    R_HOLE = r0mm + hole_clear

    # ---- the run, far enough that the ribbon covers every window corner ----
    r_far = max(math.hypot(cx - ex, cy - ey) for cx in (wx0, wx1) for cy in (wy0, wy1))
    a0 = 0.62 + rng.uniform(-0.55, 0.55)
    states, grads = dirac_gan_run(step, r_start, a0, r_far / k / (1 - beta) * 1.02, max_iters)
    Z = [(t * k, s * k) for t, s in states]
    rib = Ribbon(Z, beta)

    def in_win(x: float, y: float) -> bool:
        return wx0 <= x <= wx1 and wy0 <= y <= wy1

    n_exit = next(n for n, (zx, zy) in enumerate(Z) if not in_win(ex + zx, ey + zy))
    r_exit = math.hypot(*states[n_exit])

    # ---- the reed ------------------------------------------------------------
    I = [i for i in range(-200, 200) if wx0 <= ex + (i + 0.5) * p <= wx1]
    J = [j for j in range(-200, 200) if wy0 <= ey + (j + 0.5) * p <= wy1]
    XI = {i: ex + (i + 0.5) * p for i in I}
    YJ = {j: ey + (j + 0.5) * p for j in J}

    # ---- every crossing: woven? in the ribbon? who is on top? --------------
    warp_over: Dict[Tuple[int, int], bool] = {}
    in_rib: Dict[Tuple[int, int], Tuple[int, int, float]] = {}
    for i in I:
        dx = XI[i] - ex
        for j in J:
            dy = YJ[j] - ey
            if math.hypot(dx, dy) < R_HOLE:
                continue
            loc = rib.locate(dx, dy)
            if loc is not None:
                in_rib[(i, j)] = loc
                warp_over[(i, j)] = dx * dy > 0          # psi*theta > 0: D on top
            else:
                warp_over[(i, j)] = (i // 2 + j // 2) % 2 == 0

    # ---- tie-downs: a float ENDS by going under.  At the first ground crossing
    # beyond each end of a ribbon float, the floating thread goes under (the
    # basket may have had it over, which would fuse a basket pair onto the
    # float and eat the channel between laps).  Where a warp float and a weft
    # float would both need the same crossing, the basket rule stands.
    want: Dict[Tuple[int, int], set] = {}
    for is_warp, lines, other in ((True, I, J), (False, J, I)):
        for a in lines:
            seq = [((a, b) if is_warp else (b, a)) for b in other]
            for q, key in enumerate(seq):
                if key not in in_rib or warp_over.get(key) != is_warp:
                    continue
                for nb in (q - 1, q + 1):
                    if 0 <= nb < len(seq):
                        kk = seq[nb]
                        if kk in warp_over and kk not in in_rib:
                            want.setdefault(kk, set()).add(not is_warp)
    n_ties = 0
    for kk, vals in want.items():
        if len(vals) == 1:
            v = next(iter(vals))
            if warp_over[kk] != v:
                n_ties += 1
            warp_over[kk] = v

    # ---- threads: extent minus an under-gap at every under crossing --------
    def extents(c_rel: float, lo: float, hi: float, c0: float):
        """The thread's woven extent along its own axis: window minus hole."""
        if abs(c_rel) >= R_HOLE:
            return [(lo, hi)]
        h = math.sqrt(R_HOLE ** 2 - c_rel ** 2)
        return [(a, b) for a, b in ((lo, c0 - h), (c0 + h, hi)) if b - a > 0]

    def thread_pieces(is_warp: bool, idx: int):
        if is_warp:
            c_rel = XI[idx] - ex
            ext = extents(c_rel, wy0, wy1, ey)
            cross = [(YJ[j], warp_over.get((idx, j)), (idx, j)) for j in J]
        else:
            c_rel = YJ[idx] - ey
            ext = extents(c_rel, wx0, wx1, ex)
            cross = [(XI[i], (not warp_over[(i, idx)]) if (i, idx) in warp_over else None,
                      (i, idx)) for i in I]
        out = []
        for lo, hi in ext:
            cs = [(q, ov, key) for q, ov, key in cross if lo <= q <= hi and ov is not None]
            cuts = [(q - gap / 2, q + gap / 2) for q, ov, _ in cs if not ov]
            # a crossing just inside the hole is not woven, but both threads can
            # still reach it from the rim: neither may ink it
            cuts += [(q - gap / 2, q + gap / 2) for q, ov, _ in cross
                     if ov is None and lo - gap / 2 < q < hi + gap / 2]
            pos = lo
            segs = []
            for c0, c1 in sorted(cuts):
                if c0 > pos:
                    segs.append((pos, c0))
                pos = max(pos, c1)
            if hi > pos:
                segs.append((pos, hi))
            for a, b in segs:
                if b - a < min_ink:
                    continue
                # weight = on top INSIDE the ribbon: count the ribbon over-crossings
                n_over = sum(1 for q, ov, key in cs if ov and a <= q <= b and key in in_rib)
                keys = [key for q, ov, key in cs if ov and a <= q <= b]
                out.append(dict(a=a, b=b, n=n_over, keys=keys, rib=any(kk in in_rib for kk in keys)))
        return out

    warps = {i: thread_pieces(True, i) for i in I}
    wefts = {j: thread_pieces(False, j) for j in J}

    # ---- emit: reed order, boustrophedon; double pass out and back --------
    out: List[GCodeCommand] = []
    pendowns = {WARP: 0, WEFT: 0, TYPE: 0}
    draw_len = {WARP: 0.0, WEFT: 0.0, TYPE: 0.0}

    def lay(pen: int, is_warp: bool, c: float, a: float, b: float, n: int, forward: bool):
        if not forward:
            a, b = b, a
        if n >= double_min:
            o = pass_sep / 2
            seq = [(a, c - o), (b, c - o), (b, c + o), (a, c + o)]
            L = 2 * abs(b - a) + pass_sep
        else:
            seq = [(a, c), (b, c)]
            L = abs(b - a)
        pts = [(q, t) for t, q in seq] if is_warp else seq
        pendowns[pen] += 1
        draw_len[pen] += L
        return _poly(pts, color=pen, f=feed)

    for q, i in enumerate(I):
        fwd = q % 2 == 0
        pcs = warps[i] if fwd else list(reversed(warps[i]))
        for pc in pcs:
            out += lay(WARP, True, XI[i], pc["a"], pc["b"], pc["n"], fwd)
    for q, j in enumerate(J):
        fwd = q % 2 == 0
        pcs = wefts[j] if fwd else list(reversed(wefts[j]))
        for pc in pcs:
            out += lay(WEFT, False, YJ[j], pc["a"], pc["b"], pc["n"], fwd)

    # ---- the h -> 0 flow: the full dashed circle at r0 through step 0 -----
    n_d = int(2 * math.pi * r0mm / 4.5)
    on = 2.5 / r0mm
    circle = []
    for m in range(n_d):
        a = a0 + 2 * math.pi * m / n_d
        pts = [(ex + r0mm * math.cos(a + on * t / 6), ey + r0mm * math.sin(a + on * t / 6))
               for t in range(7)]
        circle += _poly(pts, color=TYPE, f=feed)
        pendowns[TYPE] += 1
        draw_len[TYPE] += 2.5

    # ---- the equilibrium: bare paper, one black +, three passes ----------
    arm = 3.5
    plus = []
    for d in (-0.25, 0.0, 0.25):
        plus += _poly([(ex - arm, ey + d), (ex + arm, ey + d)], color=TYPE, f=feed)
        plus += _poly([(ex + d, ey - arm), (ex + d, ey + arm)], color=TYPE, f=feed)
    pendowns[TYPE] += 6
    draw_len[TYPE] += 6 * 2 * arm

    type_cmds: List[GCodeCommand] = []

    def put(s, x, y, hgt, track=1.0):
        nonlocal type_cmds
        type_cmds += _text(s, x, y, hgt, TYPE, feed, track)

    def centred(s, cx, y, hgt, track=1.0):
        put(s, cx - _ink_width(s, hgt, track) / 2 - _left_ink(s, hgt), y, hgt, track)

    TL = 2.1
    centred("NASH EQUILIBRIUM", ex, ey + arm + 3.0, TL)
    centred("θ = ψ = 0", ex, ey - arm - 3.0 - TL, TL)
    centred("h → 0: THE FLOW CIRCLES", ex, ey - 0.72 * r0mm, 2.0)

    # ---- title: flush x0, ink ends exactly on x1, cap-tops at title_top ---
    title = "THE FIXED POINT REPELS"
    tw_w = 0.9
    # giant_type ink runs from x + lo*sc - w/2 to x + ((n-1)*ADV + hi)*sc + w/2
    lo_t = _glyph_extent(title[0])[0]
    hi_t = _glyph_extent(title[-1])[1]
    span_units = (len(title) - 1) * ADV + hi_t - lo_t
    th = (x1 - x0 - tw_w) / span_units * 6.0
    sc_t = th / 6.0
    xT = x0 + tw_w / 2 - lo_t * sc_t
    yT = title_top - th - tw_w / 2
    type_cmds += giant_type(title, xT, yT, th, pen=TYPE, weight=tw_w, tip=0.3, f=feed)
    sub = " ".join("NEITHER PLAYER EVER ARRIVES")
    put(sub, x0 - _left_ink(sub, 2.4), 263.5, 2.4)

    # ---- footer: 4 lines, 1.7 mm caps, baselines 11.0 / 15.2 / 19.4 / 23.6 --
    TF, TR = 1.7, 1.18
    yF = [23.6, 19.4, 15.2, 11.0]
    foot = [
        f"H {step:.2f} · STEP 0 ON THE CIRCLE R {r_start:.2f} · EACH LAP ABOUT 1.5 × WIDER",
        f"STEP {n_exit}  R {r_exit:.2f}  LEAVES THE CLOTH",
        "WARP ON TOP: D SPOTS THE FAKE (ψθ > 0) · WEFT ON TOP: G FOOLS D (ψθ < 0)",
        "BASKET: STATES THE RUN NEVER CROSSES · BARE PAPER: CLOSER THAN THE START",
    ]
    for s, yb in zip(foot, yF):
        put(s, x0 - _left_ink(s, TF), yb, TF, TR)
    brief = "MIN G MAX D V(D,G)"
    put(brief, x1 - _ink_width(brief, TF, TR) - _left_ink(brief, TF), yF[3], TF, TR)
    # legend flush right on x1, on footer baselines 1-2; a real 3-crossing float
    legend = ["WEFT  G  MOVES θ", "WARP  D  MOVES ψ"]
    lw = max(_ink_width(s, TF, TR) for s in legend)
    xL = x1 - lw
    for s, yb in zip(legend, yF[:2]):
        put(s, xL - _left_ink(s, TF) + (lw - _ink_width(s, TF, TR)), yb, TF, TR)
    fl = 4 * p - gap                     # a float over three crossings
    sw = []
    cyw = yF[0] + TF / 2
    xs1 = xL - 3.5
    sw += _poly([(xs1 - fl, cyw - 0.2), (xs1, cyw - 0.2), (xs1, cyw + 0.2), (xs1 - fl, cyw + 0.2)],
                color=WEFT, f=feed)
    # the warp sample hangs under the weft one in the same column, one reed
    # pitch below it: the two players as they meet in the cloth
    xv = xs1 - fl / 2
    ytop = cyw - p
    sw += _poly([(xv - 0.2, ytop), (xv - 0.2, ytop - fl),
                 (xv + 0.2, ytop - fl), (xv + 0.2, ytop)], color=WARP, f=feed)
    pendowns[WEFT] += 1
    pendowns[WARP] += 1
    draw_len[WEFT] += 2 * fl
    draw_len[WARP] += 2 * fl
    for c in type_cmds:
        if c.command == "M3":
            pendowns[TYPE] += 1

    out += sw + circle + plus + type_cmds

    # ---- checks ---------------------------------------------------------------
    rib_keys = list(in_rib)
    sign_ok = sum(1 for (i, j) in rib_keys
                  if warp_over[(i, j)] == ((XI[i] - ex) * (YJ[j] - ey) > 0))
    ground = [kk for kk in warp_over if kk not in in_rib]
    g_over = sum(1 for kk in ground if warp_over[kk])
    pure = [kk for kk in ground if kk not in want]
    pure_over = sum(1 for kk in pure if warp_over[kk])
    all_pieces = [(True, i, pc) for i in I for pc in warps[i]] + \
                 [(False, j, pc) for j in J for pc in wefts[j]]
    min_piece = min(pc["b"] - pc["a"] for _w, _i, pc in all_pieces)
    # visible paper along a thread between consecutive inked pieces
    min_gap = float("inf")
    for thr in list(warps.values()) + list(wefts.values()):
        for a, b in zip(thr, thr[1:]):
            min_gap = min(min_gap, b["a"] - a["b"])
    # min thread radius
    r_min = float("inf")
    for is_w, idx, pc in all_pieces:
        c = (XI[idx] - ex) if is_w else (YJ[idx] - ey)
        c0 = ey if is_w else ex
        for t in (pc["a"], pc["b"], min(max(c0, pc["a"]), pc["b"])):
            r_min = min(r_min, math.hypot(c, t - c0))
    # iterates in the window: on the ribbon centreline by construction; are they on cloth?
    in_frame = [n for n, (zx, zy) in enumerate(Z) if in_win(ex + zx, ey + zy)]
    in_hole = [n for n in in_frame if math.hypot(*Z[n]) < R_HOLE]
    # ribbon span on 8 rays: [0.9, 1.1] x chord radius, lap by lap
    rays = {}
    for deg in range(0, 360, 45):
        A = math.radians(deg)
        row = []
        while A <= rib.A[-1]:
            if A >= rib.A[0]:
                rc, _k = rib.centre_rho(A)
                row.append(round(rc, 1))
            A += 2 * math.pi
        rays[deg] = row
    chan = {deg: [round(0.9 * b - 1.1 * a, 1) for a, b in zip(r, r[1:])] for deg, r in rays.items()}
    chan_ratio = {deg: [round((0.9 * b - 1.1 * a) / a, 3) for a, b in zip(r, r[1:])]
                  for deg, r in rays.items()}
    lam0 = math.sqrt(1 + step ** 2 * 0.25)

    gan_meander.stats = dict(  # type: ignore[attr-defined]
        a0=a0, n_ties=n_ties, n_states=len(states), n_exit=n_exit, r_exit=r_exit, lam0=lam0,
        warps=len(I), wefts=len(J), crossings=len(warp_over), in_ribbon=len(rib_keys),
        sign_ok=sign_ok, ground=len(ground), ground_warp_over=g_over, basket_pure=len(pure), basket_pure_warp_over=pure_over, tie_sites=len(want),
        pieces=len(all_pieces), min_piece=min_piece, min_gap=min_gap, r_min=r_min,
        R_hole=R_HOLE, r0mm=r0mm, in_frame=len(in_frame), in_frame_in_hole=in_hole,
        rays=rays, channels=chan, channel_ratio=chan_ratio,
        pendowns=pendowns, draw_len=draw_len, title_h=th,
        doubles=sum(1 for _w, _i, pc in all_pieces if pc["n"] >= double_min),
    )
    return out
