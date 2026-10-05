"""GAN — THE FIXED POINT REPELS, woven.  Studio candidate, round 07 (iterate).

parent: r05 (encoding rev 1, Red Meander proper).  Built to `studio/gan/encoding.md`
revision 1.1 (appended this round):

  * PER-STEP FACE.  Ribbon cell k (z_k -> z_{k+1}) is warp-on-top iff
    psi_k * theta_k > 0 — the sign the move z_k -> z_{k+1} was computed from
    (f'(psi_k theta_k)).  Not per crossing.  The quarter seams leave the axes and
    sit on the radial line through each lap's first post-axis iterate.
  * RIM SHIFT.  The ribbon is SHIFTED outward at the hole, never clipped: on
    every ray it spans [lo, lo + 0.2 rho] with lo = max(0.9 rho, rho_min), where
    rho_min = r0 + 1.0 mm is the smallest radius whose thread ink keeps 0.5 mm of
    paper to the dashed circle's ink (0.25 cap + 0.5 paper + 0.25 dash half-width).
  * WEIGHT BY MEMBERSHIP.  Double pass exactly over the ribbon crossings of a
    float (per crossing, +-p/2), single pass over its ground crossings.
  * MID-PITCH WINDOW.  The cloth's cut edges fall half-way between threads.
  * RE-CROP (A21).  51.1 mm/unit, equilibrium (66, 100), window x 10.0-197.6,
    y 38.4-254.0: every lap clears each edge by >= 6 mm, or is cut through, or
    keeps >= 8.4 mm inside AND loses >= 8.4 mm outside (no graze).  Found by a
    full scan of scale x centre; checked in `stats['crops']`.
  * TIES + BASKET.  Tie-downs only where a float would bridge the channel onto
    the next lap ("bridge"); 2/2 basket phase (1, 1) puts the block edges off
    both axes.  Ground over-share 49.96 %.
  * TYPE on the cloth's edges: title (118 mm), tagline and footer flush on the
    window's left cut edge x = 10.0; legend and brief flush on its right, 197.6.

Contract:  gan_meander_step(rng, bounds, colors=3) -> list[GCodeCommand]

WHAT IS COMPUTED (exact, unchanged since r01)
---------------------------------------------
Dirac-GAN (Mescheder, Geiger, Nowozin 2018): V(theta, psi) = f(psi*theta) + f(0),
f(t) = -log(1 + e^-t), f'(s) = sigmoid(-s).  Simultaneous GDA, one shared h:

    theta' = theta - h * psi   * f'(s)      (G descends)
    psi'   = psi   + h * theta * f'(s)      (D ascends)

The equilibrium theta = psi = 0 exists (Jacobian +-0.5i, a centre); the h -> 0
flow circles at r0; each discrete step multiplies r by sqrt(1 + h^2 f'^2) > 1,
so the fixed point REPELS.
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


def _chain_glyph(strokes, tol: float = 1e-6):
    """Join a glyph's strokes end to end where they share an endpoint, so one
    pen-down draws what the font split into several.  Same ink, fewer lifts."""
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


def _text(s: str, x: float, y: float, hgt: float, pen: int, f: int,
          track: float = 1.0) -> List[GCodeCommand]:
    sc = hgt / 6.0
    out: List[GCodeCommand] = []
    cx = x
    for ch in s:
        strokes = _LOCAL.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        for st in _chain_glyph(strokes):
            out += _poly([(cx + gx * sc, y + gy * sc) for gx, gy in st], color=pen, f=f)
        cx += ADV * sc * track
    return out


def _ink_width(s: str, hgt: float, track: float = 1.0) -> float:
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
    """The chord polygon of the run, as a band of width 2*beta*rho about it,
    SHIFTED outward (never clipped) where it would enter rho < rho_min.

    Iterates are in mm relative to the equilibrium.  Their polar angle is
    strictly increasing (every step turns by atan(h f') > 0), so a direction
    at unwrapped angle A meets the chord polygon exactly once per lap."""

    def __init__(self, pts_mm: List[Tuple[float, float]], beta: float, rho_min: float):
        self.P = pts_mm
        self.beta = beta
        self.rho_min = rho_min
        ang = [math.atan2(pts_mm[0][1], pts_mm[0][0])]
        for (x0, y0), (x1, y1) in zip(pts_mm, pts_mm[1:]):
            d = math.atan2(x0 * y1 - y0 * x1, x0 * x1 + y0 * y1)
            ang.append(ang[-1] + d)
        self.A = ang

    def span(self, rc: float) -> Tuple[float, float]:
        lo = max((1 - self.beta) * rc, self.rho_min)
        return lo, lo + 2 * self.beta * rc

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
        """(lap, cell k, centre rho) if (x, y) lies in the ribbon, else None."""
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
            lo, hi = self.span(rc)
            if lo <= rho <= hi:
                return m - m0, k, rc
            if lo > rho:
                break
        return None


def _runs(flags: List[bool]) -> int:
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def gan_meander_step(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    step: float = 0.26,            # h, the shared learning rate
    r_start: float = 0.74,         # ||(theta, psi)|| at step 0: the flow circle
    max_iters: int = 9000,
    scale_mm: float = 51.1,        # mm per world unit
    centre: Tuple[float, float] = (66.0, 100.0),   # equilibrium, paper mm
    window_y: Tuple[float, float] = (37.3, 256.0),  # limits; edges snap to mid-pitch inside
    pitch: float = 2.8,            # the reed
    beta: float = 0.10,            # ribbon width = 2 beta rho
    gap: float = 2.4,              # under-gap along the thread
    hole_clear: float = 1.0,       # rho_min = r0 + hole_clear (0.25 + 0.5 paper + 0.25)
    min_ink: float = 2.5,          # shortest inked piece
    pass_sep: float = 0.4,
    basket_phase: Tuple[int, int] = (1, 1),  # 2/2 block edges off both axes
    tie_mode: str = "bridge",       # all | pair | bridge | none
    title_w: float = 118.0,        # title ink width (A22: <= 120)
    title_top: float = 284.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE FIXED POINT REPELS — Red Meander proper, one face per training step:
    a basket-woven cloth in which the Dirac-GAN's simultaneous-GDA run is the
    region where the player who was winning AT THAT STEP floats on top,
    unwinding away from a hole of bare paper that holds the equilibrium."""
    x0, y0, x1, y1 = bounds
    WARP = 0 % max(1, colors)      # dodgerblue, plotted first
    WEFT = 1 % max(1, colors)      # crimson
    TYPE = 2 % max(1, colors)      # black, last
    k = scale_mm
    p = pitch
    ex, ey = centre
    r0mm = r_start * k
    R_HOLE = r0mm + hole_clear

    # ---- the window: cut edges at mid-pitch (half-way between two threads) --
    def snap(c, lo, hi):
        return (c + math.ceil((lo - c) / p - 1e-9) * p, c + math.floor((hi - c) / p + 1e-9) * p)

    wx0, wx1 = snap(ex, x0, x1)
    wy0, wy1 = snap(ey, *window_y)

    # ---- the run, far enough that the ribbon covers every window corner ----
    r_far = max(math.hypot(cx - ex, cy - ey) for cx in (wx0, wx1) for cy in (wy0, wy1))
    a0 = 0.62 + rng.uniform(-0.55, 0.55)
    states, grads = dirac_gan_run(step, r_start, a0, r_far / k / (1 - beta) * 1.05, max_iters)
    Z = [(t * k, s * k) for t, s in states]
    rib = Ribbon(Z, beta, R_HOLE)
    face_warp = [zx * zy > 0 for zx, zy in Z]        # cell k: psi_k theta_k > 0 -> D on top

    def in_win(x: float, y: float) -> bool:
        return wx0 <= x <= wx1 and wy0 <= y <= wy1

    n_exit = next(n for n, (zx, zy) in enumerate(Z) if not in_win(ex + zx, ey + zy))
    r_exit = math.hypot(*states[n_exit])
    exit_pt = (ex + Z[n_exit][0], ey + Z[n_exit][1])

    # ---- the reed ------------------------------------------------------------
    I = [i for i in range(-200, 200) if wx0 < ex + (i + 0.5) * p < wx1]
    J = [j for j in range(-200, 200) if wy0 < ey + (j + 0.5) * p < wy1]
    XI = {i: ex + (i + 0.5) * p for i in I}
    YJ = {j: ey + (j + 0.5) * p for j in J}
    bx, by = basket_phase

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
                warp_over[(i, j)] = face_warp[loc[1]]      # the face of the owning step
            else:
                warp_over[(i, j)] = ((i + bx) // 2 + (j + by) // 2) % 2 == 0

    # ---- tie-downs: a float ENDS by going under (r05).  At the first ground
    # crossing beyond each end of a ribbon float the floating thread goes under;
    # where a warp float and a weft float both claim it, the basket stands.
    want: Dict[Tuple[int, int], set] = {}
    for is_warp, lines, other in ((True, I, J), (False, J, I)):
        for a in lines:
            seq = [((a, b) if is_warp else (b, a)) for b in other]
            for q, key in enumerate(seq):
                if key not in in_rib or warp_over.get(key) != is_warp:
                    continue
                for d in (-1, 1):
                    nb = q + d
                    if not 0 <= nb < len(seq):
                        continue
                    kk = seq[nb]
                    if kk not in warp_over or kk in in_rib:
                        continue
                    if tie_mode == "none":
                        continue
                    if tie_mode in ("bridge", "pair"):
                        # tie only if the basket run of this thread would carry
                        # the float across the channel onto another float
                        t = nb
                        while (0 <= t < len(seq) and seq[t] in warp_over
                               and seq[t] not in in_rib and warp_over[seq[t]] == is_warp):
                            t += d
                        if t == nb:
                            continue
                        bridges = (0 <= t < len(seq) and seq[t] in in_rib
                                   and warp_over.get(seq[t]) == is_warp)
                        if not bridges and not (tie_mode == "pair" and abs(t - nb) >= 2):
                            continue
                    want.setdefault(kk, set()).add(not is_warp)
    n_ties = 0
    tie_dir = {"to_weft": 0, "to_warp": 0, "conflict": 0}
    for kk, vals in want.items():
        if len(vals) == 1:
            v = next(iter(vals))
            if warp_over[kk] != v:
                n_ties += 1
                tie_dir["to_warp" if v else "to_weft"] += 1
            warp_over[kk] = v
        else:
            tie_dir["conflict"] += 1

    # ---- threads: extent minus an under-gap at every under crossing --------
    def extents(c_rel: float, lo: float, hi: float, c0: float):
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
                overs = [(q, key, key in in_rib) for q, ov, key in cs if ov and a <= q <= b]
                out.append(dict(a=a, b=b, overs=overs))
        return out

    # ---- no empty crossing: where the over-thread's piece is too short to ink
    # (hole rim, cut edge), the other thread takes the crossing.  Ground only;
    # a ribbon crossing keeps its step's face (checked below: 0 left over).
    # If neither thread alone can ink it (both truncated by the hole), the
    # thread whose next crossing AWAY from the hole is ground also takes that
    # neighbour, so its piece is long enough.
    flipped = []
    extended = []
    tried: Dict[Tuple[int, int], int] = {}
    for _it in range(12):
        warps = {i: thread_pieces(True, i) for i in I}
        wefts = {j: thread_pieces(False, j) for j in J}
        inked = {key for thr in list(warps.values()) + list(wefts.values())
                 for pc in thr for _q, key, _r in pc["overs"]}
        empty = [kk for kk in warp_over if kk not in inked]
        fix = [kk for kk in empty if kk not in in_rib]
        if not fix:
            break
        for kk in fix:
            n = tried.get(kk, 0)
            tried[kk] = n + 1
            if n == 0:
                warp_over[kk] = not warp_over[kk]
                flipped.append(kk)
                continue
            i, j = kk
            best = None
            for is_w in (True, False):
                nb = (i, j + 1) if is_w else (i + 1, j)
                nb2 = (i, j - 1) if is_w else (i - 1, j)
                far = max((nb, nb2), key=lambda t: math.hypot(
                    XI.get(t[0], 1e9) - ex, YJ.get(t[1], 1e9) - ey)
                    if t[0] in XI and t[1] in YJ else -1)
                if far in warp_over and far not in in_rib:
                    best = (is_w, far)
                    break
            if best is not None:
                is_w, far = best
                warp_over[kk] = is_w
                warp_over[far] = is_w
                extended.append((kk, far))
    empty_rib = [kk for kk in empty if kk in in_rib]
    empty_all = empty

    # ---- emit: reed order, boustrophedon.  Weight by membership: out-and-back
    # (double pass) exactly over the float's ribbon crossings, +- p/2 ----------
    out: List[GCodeCommand] = []
    pendowns = {WARP: 0, WEFT: 0, TYPE: 0}
    draw_len = {WARP: 0.0, WEFT: 0.0, TYPE: 0.0}
    dbl_keys = set()
    o = pass_sep / 2

    def parts_of(pc):
        a, b = pc["a"], pc["b"]
        ivs = []
        cur = None
        for q, key, r in sorted(pc["overs"]):
            if r:
                if cur is not None and q - cur[1] < 1.01 * p:
                    cur[1] = q
                else:
                    cur = [q, q]
                    ivs.append(cur)
                dbl_keys.add(key)
            else:
                cur = None
        dd = []
        for s0, s1 in ivs:
            d0, d1 = max(a, s0 - p / 2), min(b, s1 + p / 2)
            if d0 - a < p / 2:
                d0 = a
            if b - d1 < p / 2:
                d1 = b
            dd.append((d0, d1))
        parts = []
        pos = a
        for d0, d1 in dd:
            if d0 > pos + 1e-9:
                parts.append((pos, d0, False))
            parts.append((d0, d1, True))
            pos = d1
        if b > pos + 1e-9:
            parts.append((pos, b, False))
        return parts

    def lay(pen: int, is_warp: bool, c: float, pc, forward: bool):
        parts = parts_of(pc)
        if not forward:
            parts = [(t1, t0, d) for t0, t1, d in reversed(parts)]
        # the out-and-back closes at the far end: put a double part there
        if not parts[-1][2] and parts[0][2]:
            parts = [(t1, t0, d) for t0, t1, d in reversed(parts)]
        strokes = []
        path = []
        for t0, t1, d in parts:
            off = -o if d else 0.0
            path += [(t0, c + off), (t1, c + off)]
        backs = [(t0, t1) for t0, t1, d in parts if d]
        if parts[-1][2]:
            t0, t1 = backs.pop()
            path += [(t1, c + o), (t0, c + o)]
        strokes.append(path)
        for t0, t1 in backs:
            strokes.append([(t1, c + o), (t0, c + o)])
        cmds = []
        for st in strokes:
            clean = [st[0]] + [q for prev, q in zip(st, st[1:]) if math.dist(prev, q) > 1e-9]
            pts = [(t, v) for v, t in clean] if is_warp else clean
            pendowns[pen] += 1
            draw_len[pen] += sum(math.dist(u, v) for u, v in zip(pts, pts[1:]))
            cmds += _poly(pts, color=pen, f=feed)
        return cmds

    for q, i in enumerate(I):
        fwd = q % 2 == 0
        pcs = warps[i] if fwd else list(reversed(warps[i]))
        for pc in pcs:
            out += lay(WARP, True, XI[i], pc, fwd)
    for q, j in enumerate(J):
        fwd = q % 2 == 0
        pcs = wefts[j] if fwd else list(reversed(wefts[j]))
        for pc in pcs:
            out += lay(WEFT, False, YJ[j], pc, fwd)

    # ---- the h -> 0 flow: the full dashed circle at r0, a dash starts at z_0 -
    n_d = int(2 * math.pi * r0mm / 4.5)
    on = 2.5 / r0mm
    circle = []
    for m in range(n_d):
        a = a0 + 2 * math.pi * m / n_d
        pts = [(ex + r0mm * math.cos(a + on * t / 3), ey + r0mm * math.sin(a + on * t / 3))
               for t in range(4)]
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
    boxes = {}

    def put(s, x, y, hgt, track=1.0, tag=None):
        nonlocal type_cmds
        type_cmds += _text(s, x, y, hgt, TYPE, feed, track)
        if tag:
            xl = x + _left_ink(s, hgt)
            boxes[tag] = (xl, y, xl + _ink_width(s, hgt, track), y + hgt)

    def centred(s, cx, y, hgt, track=1.0, tag=None):
        put(s, cx - _ink_width(s, hgt, track) / 2 - _left_ink(s, hgt), y, hgt, track, tag)

    def right(s, xr, y, hgt, track=1.0, tag=None):
        put(s, xr - _ink_width(s, hgt, track) - _left_ink(s, hgt), y, hgt, track, tag)

    # label group 1: the equilibrium, both lines under the +
    TL = 2.1
    centred("NASH EQUILIBRIUM", ex, ey - arm - 3.0 - TL, TL, tag="nash")
    centred("θ = ψ = 0", ex, ey - arm - 6.4 - 2 * TL, TL, tag="zero")
    # label group 2: where the run starts, on the rim beside z_0
    zx0, zy0 = ex + Z[0][0], ey + Z[0][1]
    right("STEP 0", zx0 - 2.4, zy0 - TL / 2, TL, tag="step0")
    right("h → 0: THE FLOW CIRCLES", zx0 - 2.4, zy0 - TL / 2 - 4.2, 2.0, tag="flow")

    # ---- title: flush x0, <= 120 mm, cap-tops at title_top ----------------
    title = "THE FIXED POINT REPELS"
    tw_w = 0.3
    lo_t = _glyph_extent(title[0])[0]
    hi_t = _glyph_extent(title[-1])[1]
    span_units = (len(title) - 1) * ADV + hi_t - lo_t
    th = (title_w - tw_w) / span_units * 6.0
    sc_t = th / 6.0
    xT = wx0 + tw_w / 2 - lo_t * sc_t
    yT = title_top - th - tw_w / 2
    type_cmds += giant_type(title, xT, yT, th, pen=TYPE, weight=tw_w, tip=0.3, f=feed)
    sub = " ".join("NEITHER PLAYER EVER ARRIVES")
    y_sub = yT - 7.0
    put(sub, wx0 - _left_ink(sub, 2.4), y_sub, 2.4, tag="sub")

    # ---- footer: 4 lines, 1.7 mm caps, baselines 23.6 / 19.4 / 15.2 / 11.0 ---
    # left column flush on the cloth's left cut edge, right column flush on its
    # right cut edge (wx0 / wx1 are the window, so type and cloth share edges)
    TF, TR = 1.7, 1.18
    yF = [23.6, 19.4, 15.2, 11.0]
    foot = [
        f"H {step:.2f} · STEP 0 ON THE CIRCLE R {r_start:.2f} · EACH LAP ABOUT 1.5 × WIDER",
        f"STEP {n_exit}  R {r_exit:.2f}  LEAVES THE CLOTH",
        "BASKET: STATES THE RUN NEVER CROSSES · INSIDE THE CIRCLE: CLOSER THAN THE START",
        "WARP ON TOP: D SPOTS THE FAKE AT THAT STEP (ψθ > 0) · "
        "WEFT ON TOP: G FOOLS D AT THAT STEP (ψθ < 0)",
    ]
    for q, (s, yb) in enumerate(zip(foot, yF)):
        put(s, wx0 - _left_ink(s, TF), yb, TF, TR, tag=f"foot{q}")
    brief = "MIN G MAX D V(D,G)"
    right(brief, wx1, yF[2], TF, TR, tag="brief")
    legend = ["WEFT  G  MOVES θ", "WARP  D  MOVES ψ"]
    lw = max(_ink_width(s, TF, TR) for s in legend)
    xL = wx1 - lw
    for q, (s, yb) in enumerate(zip(legend, yF[:2])):
        right(s, wx1, yb, TF, TR, tag=f"legend{q}")
    fl = 3 * p - gap                     # a real float over two crossings, 6.0 mm
    sw = []
    cyw = yF[0] + TF / 2                 # weft swatch on line 1's midline
    xs1 = xL - 3.5
    sw += _poly([(xs1 - fl, cyw - o), (xs1, cyw - o), (xs1, cyw + o), (xs1 - fl, cyw + o)],
                color=WEFT, f=feed)
    xv = xs1 - fl / 2                    # warp swatch centred on line 2's midline
    ytop = yF[1] + TF / 2 + fl / 2
    sw += _poly([(xv - o, ytop), (xv - o, ytop - fl), (xv + o, ytop - fl), (xv + o, ytop)],
                color=WARP, f=feed)
    boxes["sw_warp"] = (xv - o, ytop - fl, xv + o, ytop)
    boxes["sw_weft"] = (xs1 - fl, cyw - o, xs1, cyw + o)
    pendowns[WEFT] += 1
    pendowns[WARP] += 1
    draw_len[WEFT] += 2 * fl + 2 * o
    draw_len[WARP] += 2 * fl + 2 * o
    for c in type_cmds:
        if c.command == "M3":
            pendowns[TYPE] += 1

    out += sw + circle + plus + type_cmds

    # =======================================================================
    # checks (printed into NOTES)
    # =======================================================================
    rib_keys = list(in_rib)
    face_ok = sum(1 for kk in rib_keys if warp_over[kk] == face_warp[in_rib[kk][1]])
    percross_agree = sum(1 for (i, j) in rib_keys
                         if warp_over[(i, j)] == ((XI[i] - ex) * (YJ[j] - ey) > 0))
    ground = [kk for kk in warp_over if kk not in in_rib]
    g_over = sum(1 for kk in ground if warp_over[kk])
    rib_single = [kk for kk in rib_keys if kk not in dbl_keys]
    ground_double = [kk for kk in ground if kk in dbl_keys]
    all_pieces = [(True, i, pc) for i in I for pc in warps[i]] + \
                 [(False, j, pc) for j in J for pc in wefts[j]]
    min_piece = min(pc["b"] - pc["a"] for _w, _i, pc in all_pieces)
    min_gap = float("inf")
    for thr in list(warps.values()) + list(wefts.values()):
        for a, b in zip(thr, thr[1:]):
            min_gap = min(min_gap, b["a"] - a["b"])
    r_min = float("inf")
    for is_w, idx, pc in all_pieces:
        c = (XI[idx] - ex) if is_w else (YJ[idx] - ey)
        c0 = ey if is_w else ex
        for t in (pc["a"], pc["b"], min(max(c0, pc["a"]), pc["b"])):
            r_min = min(r_min, math.hypot(c, t - c0))

    # S10: every in-frame iterate has a double-pass ribbon crossing within one pitch
    rib_pts = [(XI[i] - ex, YJ[j] - ey) for (i, j) in rib_keys if (i, j) in dbl_keys]
    in_frame = [n for n, (zx, zy) in enumerate(Z) if in_win(ex + zx, ey + zy)]
    iter_d = {}
    for n in in_frame:
        zx, zy = Z[n]
        iter_d[n] = min(math.hypot(zx - px, zy - py) for px, py in rib_pts
                        if abs(zx - px) < 6 and abs(zy - py) < 6) if any(
            abs(zx - px) < 6 and abs(zy - py) < 6 for px, py in rib_pts) else 99.0
    iter_far = {n: round(d, 2) for n, d in iter_d.items() if d > p}

    # A20: seams — each lap's face change, and the straightedge on the axes
    seams = []
    for n in range(1, len(Z)):
        if face_warp[n] != face_warp[n - 1] and n - 1 < len(Z) - 1:
            zx, zy = Z[n]
            if abs(zx) < abs(zy):
                ax, off = ("N" if zy > 0 else "S"), zx
            else:
                ax, off = ("E" if zx > 0 else "W"), zy
            seams.append((ax, n, round(off, 2), round(math.hypot(zx, zy), 1),
                          in_win(ex + zx, ey + zy)))
    tol = 0.6

    def edge_rows(is_warp_line: bool, half: int, floats_only: bool):
        """rows (wefts for x = ex, warps for y = ey) whose piece END lies on the
        axis line, in the given half; returns the longest consecutive run."""
        if is_warp_line:     # straightedge x = ex; weft ends
            rows = [j for j in J if (YJ[j] - ey) * half > 0]
            flags = []
            for j in rows:
                hit = any((abs(pc["a"] - ex) < tol or abs(pc["b"] - ex) < tol)
                          and (not floats_only or any(r for _q, _k, r in pc["overs"]))
                          for pc in wefts[j])
                flags.append(hit)
        else:                # straightedge y = ey; warp ends
            rows = [i for i in I if (XI[i] - ex) * half > 0]
            flags = []
            for i in rows:
                hit = any((abs(pc["a"] - ey) < tol or abs(pc["b"] - ey) < tol)
                          and (not floats_only or any(r for _q, _k, r in pc["overs"]))
                          for pc in warps[i])
                flags.append(hit)
        return _runs(flags), sum(flags)

    straightedge = {
        "x=ex N": edge_rows(True, +1, True), "x=ex S": edge_rows(True, -1, True),
        "y=ey E": edge_rows(False, +1, True), "y=ey W": edge_rows(False, -1, True),
    }

    # ribbon span + channels on 8 rays, lap by lap (with the rim shift)
    rays = {}
    for deg in range(0, 360, 45):
        A = math.radians(deg)
        row = []
        while A <= rib.A[-1]:
            if A >= rib.A[0]:
                rc, _k = rib.centre_rho(A)
                lo, hi = rib.span(rc)
                row.append((round(rc, 1), round(lo, 1), round(hi, 1)))
            A += 2 * math.pi
        rays[deg] = row
    chan = {deg: [round(b[1] - a[2], 1) for a, b in zip(r, r[1:])] for deg, r in rays.items()}
    chan_ratio = {deg: [round((b[1] - a[2]) / a[0], 3) for a, b in zip(r, r[1:])]
                  for deg, r in rays.items()}
    lam0 = math.sqrt(1 + step ** 2 * 0.25)

    # A21: every lap either CLEARS each window edge by >= 6 mm, or the edge cuts
    # it: then the part left inside (edge -> inner boundary, at its narrowest)
    # must be >= 3 pitches, and the part cut off (outer boundary past the edge)
    # also >= 3 pitches, so the edge crops THROUGH the lap and never grazes it.
    crops = {}
    n_laps = int((rib.A[-1] - rib.A[0]) / (2 * math.pi)) + 1
    edges = {"L": (0, -1, wx0), "R": (0, +1, wx1), "B": (1, -1, wy0), "T": (1, +1, wy1)}
    rng_other = {0: (wy0, wy1), 1: (wx0, wx1)}
    for m in range(n_laps):
        Aa = rib.A[0] + 2 * math.pi * m
        Ab = min(Aa + 2 * math.pi, rib.A[-1])
        if Aa >= rib.A[-1]:
            break
        inner, outer = [], []
        nA = 1440
        for q in range(nA + 1):
            A = Aa + (Ab - Aa) * q / nA
            rc, _k = rib.centre_rho(A)
            lo, hi = rib.span(rc)
            c, s_ = math.cos(A), math.sin(A)
            inner.append((ex + lo * c, ey + lo * s_))
            outer.append((ex + hi * c, ey + hi * s_))
        row = {}
        for name, (ax, sgn, pos) in edges.items():
            oa = 1 - ax
            olo, ohi = rng_other[ax]
            ins = [pt[ax] * sgn for pt in inner if olo <= pt[oa] <= ohi]
            outs = [pt[ax] * sgn for pt in outer if olo <= pt[oa] <= ohi]
            if not outs:
                row[name] = ("absent",)
                continue
            out_max = max(outs) - pos * sgn          # > 0: outer boundary past the edge
            in_max = (max(ins) - pos * sgn) if ins else float("inf")
            if out_max <= 0:
                row[name] = ("clear", round(-out_max, 1))
            elif in_max >= 0:
                row[name] = ("through",)
            else:
                row[name] = ("cut", round(-in_max, 1), round(out_max, 1))
        # is the lap inside the window at all?
        vis = any(wx0 <= x <= wx1 and wy0 <= y <= wy1 for x, y in inner + outer)
        if vis:
            crops[m] = row
    crop_fail = []
    for m, row in crops.items():
        for name, v in row.items():
            if v[0] == "clear" and v[1] < 6.0:
                crop_fail.append((m, name, v))
            if v[0] == "cut" and (v[1] < 3 * p or v[2] < 3 * p):
                crop_fail.append((m, name, v))

    # floats riding an edge: the outermost thread on each side, longest inked piece
    edge_float = {}
    for name, is_w, idx in (("L", True, I[0]), ("R", True, I[-1]),
                            ("B", False, J[0]), ("T", False, J[-1])):
        thr = warps[idx] if is_w else wefts[idx]
        dist = (XI[idx] - wx0 if name == "L" else wx1 - XI[idx]) if is_w else \
               (YJ[idx] - wy0 if name == "B" else wy1 - YJ[idx])
        edge_float[name] = (round(dist, 2), round(max((pc["b"] - pc["a"]) for pc in thr), 1))

    gan_meander_step.stats = dict(  # type: ignore[attr-defined]
        a0=a0, n_ties=n_ties, n_states=len(states), n_exit=n_exit, r_exit=r_exit,
        exit_pt=exit_pt, lam0=lam0, window=(wx0, wx1, wy0, wy1), R_hole=R_HOLE, r0mm=r0mm,
        warps=len(I), wefts=len(J), crossings=len(warp_over), in_ribbon=len(rib_keys),
        face_ok=face_ok, percross_agree=percross_agree,
        ground=len(ground), ground_warp_over=g_over, tie_sites=len(want), tie_dir=tie_dir, flipped=flipped, extended=extended, empty_all=empty_all,
        empty_ribbon=empty_rib, rib_single=rib_single, ground_double=ground_double,
        pieces=len(all_pieces), min_piece=min_piece, min_gap=min_gap, r_min=r_min,
        in_frame=len(in_frame), iter_far=iter_far,
        iter_max_d=max(iter_d.values()) if iter_d else None,
        seams=seams, straightedge=straightedge,
        rays=rays, channels=chan, channel_ratio=chan_ratio,
        pendowns=pendowns, draw_len=draw_len, title_h=th, boxes=boxes,
        z0=(zx0, zy0), crops=crops, crop_fail=crop_fail, edge_float=edge_float,
    )
    gan_meander_step._debug = dict(in_rib=in_rib, dbl=dbl_keys, warp_over=warp_over,
                                   warps=warps, wefts=wefts, XI=XI, YJ=YJ, Z=Z)
    return out
