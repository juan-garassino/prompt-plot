"""LSTM — THE FORGET GATE IS A DRAIN.   (lstm-spirals r03 · forget-gate-vortex)

Two spiral sinks on one vertical axis, as in r01 — but their pitch is no
longer a free parameter.  It is read, band by band, from the gates of a REAL
trained LSTM running over a real input sequence.

The one law of the plate:  ONE TURN OF A VORTEX = ONE TIME STEP.
A log-spiral whose radius shrinks by a factor k per revolution has pitch
    tan(psi) = -ln(k) / (2*pi)          (sink m over circulation g)
and a cell whose content is multiplied by f_t per step is exactly that spiral
with k = f_t.  So:

* RED (lower) vortex = the cell state c_t.  Annulus t (outermost = t=1, the
  eye = now) winds with k = f_t, the forget gate.  f ~ 1 draws a closed ring —
  the content goes round and nothing drains.  f -> 0 opens a drain.
* The pen of each red annulus is the term that WINS in
      c_t = f_t * c_{t-1} + i_t * g_t
  red where the keep coefficient f_t is larger, BLUE where the write
  coefficient i_t is larger — the band where the cell is overwritten.
* BLACK (upper) vortex = the hidden state h_t = o_t * tanh(c_t).  Its annuli
  wind with k = 1 - o_t: what the output gate does NOT let out.  The output gate
  is open on every step, so the black vortex drains every turn — it resets.

The network: a 1-unit LSTM trained here (numpy, exact BPTT, grad-checked; see
train_lstm.py) on the ANALOG LATCH — a value arrives on every step, y_t must be
the value at the most recent WRITE.  The forward pass below runs live on the
plate's own sequence; nothing about the gates is hand-set.

The field.  Two co-rotating SCREENED vortices on the axis (speed
u(r) = g r/(r^2+s^2) exp(-r/lambda)) give a stream function Psi whose level
sets are the ORBITS: closed rings round each centre inside a figure-eight
separatrix through a true saddle.  The drawn field is
    v = rot90(grad Psi) - kappa * grad Psi,   kappa_t = -ln(k_t) / 2pi
with kappa read from the annulus of orbits the point sits in.  So every drawn
line crosses its orbit at EXACTLY atan(kappa_t), everywhere, even beside the
saddle; for one centre alone d(ln r)/d(theta) = -kappa, i.e. the radius is
multiplied by k_t per turn, exactly, whatever u(r) is.  Annulus edges are
equal 1/T steps of distance along each centre's far ray (where orbits are
tightest), mapped to Psi levels.

Outside the eight is the arriving input: its pitch kappa_in is the plate's one
drawing constant (the input passes no gate before it arrives); each input line
is coloured by the basin it drains into.

LINEAGE: Marcel Duchamp, *Rotoreliefs* (1935) / *Anemic Cinema* (1926) — a disc
of rings that reads as a spiral once it turns; here one turn IS one tick.

Contract: ``lstm_forget_vortex(rng, bounds, colors=3) -> list[GCodeCommand]``.
Pens (= layer order, light -> dark): 0 blue = write (i_t wins) · 1 crimson =
keep (f_t wins) · 2 black = hidden state, axis, type.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import Scene3D
from promptplot.generative.generators import _GLYPHS
from promptplot.generative.engine.kit import Bounds, _pen, _stroke_text, _text_width, giant_type

# ---------------------------------------------------------------------------
# the network — weights from train_lstm.py (H=1, seed 20260928, 8000 Adam
# steps on T=30 sequences; held-out MSE 2e-5 at T=20 and T=40 against a
# predict-zero baseline of 0.21).  Rows: [x_value, x_write, h]; cols [i f o g].
# ---------------------------------------------------------------------------
_W = (
    (0.00425, -0.00262, 0.00195, -0.26844),
    (7.34955, -8.15534, -0.32605, -0.00212),
    (0.00846, 0.00903, -0.01386, -0.30586),
)
_B = (-6.35575, 6.85556, 4.10259, -0.00087)
_V, _D = -5.30308, -0.0117

T_STEPS = 12
WRITES = (0, 4, 9)  # 0-based steps carrying write=1 (a write at t=0 always)


def _sig(z: float) -> float:
    return 1.0 / (1.0 + math.exp(-z))


def lstm_run(values: Sequence[float], writes: Sequence[int]) -> List[Dict[str, float]]:
    """Forward pass of the trained cell.  Returns per-step i, f, o, g, c, h, y."""
    h = c = 0.0
    out = []
    for t, v in enumerate(values):
        x = (v, 1.0 if t in writes else 0.0, h)
        z = [sum(x[r] * _W[r][k] for r in range(3)) + _B[k] for k in range(4)]
        i, f, o, g = _sig(z[0]), _sig(z[1]), _sig(z[2]), math.tanh(z[3])
        c = f * c + i * g
        h = o * math.tanh(c)
        out.append(dict(v=v, w=x[1], i=i, f=f, o=o, g=g, c=c, h=h, y=_V * h + _D))
    return out


# ---------------------------------------------------------------------------
# the field
# ---------------------------------------------------------------------------
_S2 = 4.0  # mm^2 softening
_LAMBDA = 25.0  # mm, screening length

# A SCREENED vortex: azimuthal speed u(r) = g * r / (r^2 + s^2) * exp(-r / lambda)
# (a point vortex whose far field is cut off beyond lambda, as a quasi-
# geostrophic vortex is beyond its deformation radius).  Unscreened 1/r
# vortices make a lemniscate whose lobes reach only 0.41 x half the spacing
# past each centre — two slivers; screening gives two full lobes that still
# meet at a true saddle.  Psi1 = integral of u, tabulated once.
_DR = 0.05
_PSI_TAB: List[float] = [0.0]
for _k in range(1, int(900 / _DR) + 2):
    _r0, _r1 = (_k - 1) * _DR, _k * _DR
    _u0 = _r0 / (_r0 * _r0 + _S2) * math.exp(-_r0 / _LAMBDA)
    _u1 = _r1 / (_r1 * _r1 + _S2) * math.exp(-_r1 / _LAMBDA)
    _PSI_TAB.append(_PSI_TAB[-1] + 0.5 * (_u0 + _u1) * _DR)


def _psi1(r: float) -> float:
    q = r / _DR
    k = int(q)
    if k >= len(_PSI_TAB) - 1:
        return _PSI_TAB[-1]
    a = q - k
    return _PSI_TAB[k] * (1 - a) + _PSI_TAB[k + 1] * a


class Pair:
    """Two co-rotating screened vortices on the axis and the orbit geometry they
    make.  Psi = sum g_c * Psi1(r_c) is the stream function of the pure
    circulation: its level sets are the ORBITS (closed rings around one
    centre inside the figure-eight separatrix through the saddle).

    The drawn field is
        v = rot90(grad Psi) - kappa(orbit) * grad Psi
    so every streamline crosses its orbit at EXACTLY atan(kappa), everywhere,
    including beside the saddle.  kappa is set per annulus of orbits (one
    annulus per time step) by kappa_t = -ln(k_t) / 2pi: for one centre the
    radius is multiplied by k_t per revolution, exactly.  (Psi here is the
    SCREENED stream function, see _psi1, not the 1/r one.)
    """

    def __init__(self, cx, y_top, y_bot, g_top, g_bot):
        self.cx = cx
        self.c = ((cx, y_top, g_top), (cx, y_bot, g_bot))
        # the saddle: on the axis where the two circulations cancel
        lo, hi = y_bot + 1.0, y_top - 1.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            gy = self.grad(cx, mid)[1]
            if gy > 0:  # still below the saddle: the lower vortex dominates
                lo = mid
            else:
                hi = mid
        self.ys = 0.5 * (lo + hi)
        self.psi_s = self.psi(cx, self.ys)

    def psi(self, x, y):
        return sum(g * _psi1(math.hypot(x - px, y - py)) for px, py, g in self.c)

    def grad(self, x, y):
        gx = gy = 0.0
        for px, py, g in self.c:
            dx, dy = x - px, y - py
            q = dx * dx + dy * dy
            w = g * math.exp(-math.sqrt(q) / _LAMBDA) / (q + _S2)
            gx += w * dx
            gy += w * dy
        return gx, gy

    def far_point(self, top: bool) -> float:
        """Where the separatrix crosses the axis on the far side of a centre."""
        px, py, _ = self.c[0 if top else 1]
        sgn = 1.0 if top else -1.0
        lo, hi = 1.0, 400.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if self.psi(self.cx, py + sgn * mid) > self.psi_s:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)


class Lobe:
    """One lobe of the figure-eight: T annuli of orbits, outermost = t=1."""

    def __init__(self, pair: Pair, top: bool, r_eye: float, keeps, pens):
        self.P, self.top = pair, top
        self.x, self.y, self.g = pair.c[0 if top else 1]
        self.keeps, self.pens = list(keeps), list(pens)
        self.n = len(keeps)
        self.kappa = [-math.log(max(1e-9, k)) / (2 * math.pi) for k in keeps]
        self.r_far = pair.far_point(top)
        self.r_eye = r_eye
        sgn = 1.0 if top else -1.0
        # annulus edges: equal steps of distance along the FAR ray (where the
        # orbits are tightest), converted to Psi levels.  edges[0] = separatrix.
        self.edge_r = [self.r_far - (self.r_far - r_eye) * j / self.n for j in range(self.n + 1)]
        self.edges = [pair.psi(self.x, self.y + sgn * r) for r in self.edge_r]
        self.edges[0] = pair.psi_s
        self.sgn = sgn

    def inside(self, x, y) -> bool:
        if (y > self.P.ys) != self.top:
            return False
        return self.P.psi(x, y) < self.P.psi_s

    def band(self, x, y) -> int:
        """-1 = outside the lobe, n = in the eye, else the annulus index t."""
        if not self.inside(x, y):
            return -1
        ps = self.P.psi(x, y)
        for t in range(self.n):
            if ps >= self.edges[t + 1]:
                return t
        return self.n


class Field:
    """The whole plate's flow:  v = rot90(grad Psi) - kappa(x) grad Psi.

    kappa is read from where the point sits: annulus t of a lobe -> that
    lobe's kappa_t (a gate); outside the figure-eight -> ``kappa_in``, the
    pitch of the arriving input stream (the one drawing constant: the input
    passes no gate before it arrives)."""

    def __init__(self, pair: Pair, lobes: Sequence[Lobe], kappa_in: float):
        self.P, self.lobes, self.kappa_in = pair, list(lobes), kappa_in

    def where(self, x, y) -> Tuple[int, int]:
        """(lobe index or -1 = outside, annulus t; t == n means the eye)."""
        for li, L in enumerate(self.lobes):
            t = L.band(x, y)
            if t >= 0:
                return li, t
        return -1, -1

    def vel(self, x, y, sgn):
        li, t = self.where(x, y)
        if li < 0:
            k = self.kappa_in
        else:
            L = self.lobes[li]
            k = L.kappa[min(t, L.n - 1)]
        gx, gy = self.P.grad(x, y)
        vx, vy = -gy - k * gx, gx - k * gy
        n = math.hypot(vx, vy)
        if n < 1e-12:
            return None
        return sgn * vx / n, sgn * vy / n


def _trace(F: Field, x, y, sgn, ok, clip, turn_about=None, step=0.7, max_n=1600, gap=0.9):
    """RK4 on the normalised field (constant arc length).  ``ok(li, t)`` says
    whether the line may continue into region (li, t).  With ``turn_about``
    the line stops after one full turn about that point (a closed orbit)."""
    pts = [(x, y)]
    X0, Y0, X1, Y1 = clip
    swept = 0.0
    a0 = math.atan2(y - turn_about[1], x - turn_about[0]) if turn_about else 0.0
    for _ in range(max_n):
        k1 = F.vel(x, y, sgn)
        if k1 is None:
            break
        k2 = F.vel(x + 0.5 * step * k1[0], y + 0.5 * step * k1[1], sgn)
        if k2 is None:
            break
        k3 = F.vel(x + 0.5 * step * k2[0], y + 0.5 * step * k2[1], sgn)
        if k3 is None:
            break
        k4 = F.vel(x + step * k3[0], y + step * k3[1], sgn)
        if k4 is None:
            break
        x += step * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        y += step * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        if not (X0 < x < X1 and Y0 < y < Y1):
            break
        li, t = F.where(x, y)
        if not ok(li, t):
            break
        pts.append((x, y))
        if turn_about:
            a1 = math.atan2(y - turn_about[1], x - turn_about[0])
            swept += (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
            a0 = a1
            r = math.hypot(x - turn_about[0], y - turn_about[1])
            if abs(swept) >= 2 * math.pi - gap / max(r, 1.0):
                break
    return pts, swept


def _orbit(L: Lobe, r_far: float, step=0.8, n_max=2400):
    """The closed orbit (kappa = 0) through the far-ray point at distance r_far."""
    x, y = L.x, L.y + L.sgn * r_far
    pts = [(x, y)]
    a0 = math.atan2(y - L.y, x - L.x)
    swept = 0.0

    def v(px, py):
        gx, gy = L.P.grad(px, py)
        n = math.hypot(gx, gy) or 1e-12
        return -gy / n, gx / n

    for _ in range(n_max):
        k1 = v(x, y)
        k2 = v(x + 0.5 * step * k1[0], y + 0.5 * step * k1[1])
        k3 = v(x + 0.5 * step * k2[0], y + 0.5 * step * k2[1])
        k4 = v(x + step * k3[0], y + step * k3[1])
        x += step * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        y += step * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        a1 = math.atan2(y - L.y, x - L.x)
        swept += (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        a0 = a1
        pts.append((x, y))
        if abs(swept) >= 2 * math.pi:
            break
    return pts


def _outer_orbit(P: Pair, L: Lobe, r_far: float, step=0.9, n_max=3000):
    """A closed kappa=0 orbit OUTSIDE the figure-eight (it rings both centres),
    started on lobe L's far ray; one turn about the pair's midpoint."""
    mx, my = P.cx, 0.5 * (P.c[0][1] + P.c[1][1])
    x, y = L.x, L.y + L.sgn * r_far
    pts = [(x, y)]
    a0 = math.atan2(y - my, x - mx)
    swept = 0.0

    def v(px, py):
        gx, gy = P.grad(px, py)
        n = math.hypot(gx, gy) or 1e-12
        return -gy / n, gx / n

    for _ in range(n_max):
        k1 = v(x, y)
        k2 = v(x + 0.5 * step * k1[0], y + 0.5 * step * k1[1])
        k3 = v(x + 0.5 * step * k2[0], y + 0.5 * step * k2[1])
        k4 = v(x + step * k3[0], y + step * k3[1])
        x += step * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        y += step * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        a1 = math.atan2(y - my, x - mx)
        swept += (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        a0 = a1
        pts.append((x, y))
        if abs(swept) >= 2 * math.pi:
            break
    return pts


def _rich(text, x, y, h, pen=None, feed=2200):
    """Proportional single-stroke type with SUBSCRIPTS: ``f_t`` / ``c_{t-1}``
    set the run at 0.62x on a baseline lowered by 0.27h (r01's layout rule).
    Returns (commands, width)."""
    cmds: List[GCodeCommand] = []
    px = x
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "_" and i + 1 < n:
            i += 1
            if text[i] == "{":
                j = text.index("}", i)
                run, i = text[i + 1:j], j + 1
            else:
                run, i = text[i], i + 1
            sh = 0.62 * h
            px += 0.08 * h
            for c_ in run:
                ink = [q[0] for st in _GLYPHS.get(c_, []) for q in st]
                shift = (min(ink) - 0.55) * sh / 6.0 if ink else 0.0
                cmds += _stroke_text(c_, px - shift, y - 0.27 * h, sh, color=pen, f=feed)
                px += _text_width(c_, sh, proportional=True)
            px += 0.1 * h
            continue
        if ch == " ":  # the proportional space is too tight for tracked clauses
            px += 0.55 * h
            i += 1
            continue
        if ch.islower():
            # proportional advance, but the shared font draws each glyph at its
            # cell x, not at its ink: 'i' sits at x=1.8 with a 1.1 advance and
            # runs into the next glyph.  Shift the ink to the side bearing.
            ink = [q[0] for st in _GLYPHS.get(ch, []) for q in st]
            shift = (min(ink) - 0.55) * h / 6.0 if ink else 0.0
            cmds += _stroke_text(ch, px - shift, y, h, color=pen, f=feed)
            px += _text_width(ch, h, proportional=True)
        else:  # capitals on a fixed 0.84h pitch: the proportional I gaps ("DRA IN")
            cmds += _stroke_text(ch, px, y, h, color=pen, f=feed)
            px += 0.84 * h
        i += 1
    return cmds, px - x


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def build_plate(rng: SeededRNG, bounds: Bounds, colors: int = 3, spacing: float = 124.0,
                kappa_in: float = 0.55):
    """The computation and the geometry, without any drawing: run the trained
    cell on the plate's sequence, then lay out the two lobes.  Exposed so the
    checks in NOTES.md can re-measure the drawn plate against it."""
    x0, y0, x1, y1 = bounds
    W = x1 - x0
    BL, RD, BK = _pen(0, colors), _pen(1, colors), _pen(2, colors)
    values = [round(rng.uniform(-0.8, 0.8), 2) for _ in range(T_STEPS)]
    run = lstm_run(values, WRITES)
    f_keep = [s["f"] for s in run]
    o_keep = [1.0 - s["o"] for s in run]
    red_pens = [BL if s["i"] > s["f"] else RD for s in run]

    cx = x0 + 0.55 * W
    # size the figure-eight from its own separatrix: centres `spacing` apart,
    # then the whole eight is centred in the height left after the axis ends
    probe = Pair(cx, spacing, 0.0, 1.3, 1.0)
    f_top, f_bot = probe.far_point(True), probe.far_point(False)
    stub, lab = 8.0, 6.0  # axis stub beyond each lobe, then its label
    band_lo, band_hi = y0 + 14.0, y1  # the footer line owns the bottom 14 mm
    need = f_top + spacing + f_bot + 2 * (stub + lab)
    slack = (band_hi - band_lo) - need
    y_red = band_lo + 0.5 * slack + stub + lab + f_bot
    pair = Pair(cx, y_red + spacing, y_red, 1.3, 1.0)
    black = Lobe(pair, True, 7.0, o_keep, [BK] * T_STEPS)
    red = Lobe(pair, False, 2.5, f_keep, red_pens)
    return run, pair, black, red, Field(pair, (black, red), kappa_in), stub


def lstm_forget_vortex(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    sep: float = 0.95,
    kappa_in: float = 0.55,
    env: float = 14.0,
    spacing: float = 124.0,
    saddle_reach: float = 34.0,
    sep_h: float = 1.35,
    feed: int = 2200,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    BL = _pen(0, colors)  # write  (i_t wins)
    RD = _pen(1, colors)  # keep   (f_t wins)
    BK = _pen(2, colors)  # hidden state + structure

    run, pair, black, red, F, stub = build_plate(rng, bounds, colors, spacing, kappa_in)
    cx = pair.cx

    scene = Scene3D(rng, bounds, feed=feed, fit="none", tip=0.5)
    out = scene.out
    clip = (x0 + 0.5, y0 + 0.5, x1 - 0.5, y1 - 0.5)
    occ = scene.occupancy(sep)
    # the hidden state is drawn a step lighter: its lines keep sep_h from
    # EACH OTHER (a second engine Occupancy) and sep from everything else
    occ_h = scene.occupancy(sep_h)

    def pause_resume(pts, pen):
        """Rings and knurls: the engine's pause-and-resume crowd control."""
        if len(pts) >= 5:
            scene.lines([[(px, py, 0.0, pen) for px, py in pts]], occupancy=occ, warmup=2, min_kept=6)

    def until_crowded(pts, pen, warm=3, min_run=6):
        """Converging spirals: a line ENDS where it first meets owned space
        (Jobard-Lefebvre), queried on the engine Occupancy grids, so a sink
        thins itself instead of resuming into crumbs near its eye."""
        light = pen == BK
        cut = len(pts)
        for i in range(warm, len(pts)):
            if occ.crowded(*pts[i]) or (light and occ_h.crowded(*pts[i])):
                cut = i
                break
        if cut < min_run:
            return
        pause_resume(pts[:cut], pen)
        if light:
            for q in pts[:cut]:
                occ_h.add(*q)

    # ---- 1. red: the cell.  Hold annuli first (they own the paper), then
    #         the write annuli open their drains between them.
    same_pen = lambda pen: (lambda li, tt: li == 1 and tt < red.n and red.pens[tt] == pen)
    for t in reversed(range(T_STEPS)):
        if red.pens[t] != RD:
            continue
        r_o, r_i = red.edge_r[t], red.edge_r[t + 1]
        # closed orbits, seeded on the far ray where orbits are tightest; each
        # is integrated one full turn and closed (its drift per turn is
        # 2*pi*r*kappa = 0.04 mm at r = 40: the cell keeps everything)
        # ring pitch on the far ray is (r_o - r_i) / nr >= sep: the far ray is
        # where the orbits are tightest (|grad Psi| is largest there — measured:
        # every orbit's |grad Psi| peaks on the far ray), so pitch >= sep holds
        # all the way round every ring
        nr = max(1, int((r_o - r_i) / sep))
        for j in range(nr):
            rr = r_i + (j + 0.5) * (r_o - r_i) / nr
            sx, sy = red.x, red.y - rr
            if occ.crowded(sx, sy):
                continue
            ring, sw = _trace(F, sx, sy, 1.0, same_pen(RD), clip, turn_about=(red.x, red.y), gap=0.0)
            if abs(sw) >= 2 * math.pi - 1e-6:
                # closed: start the stroke at a seeded angle so the pen-down
                # points of the rings never stack into a seam on the far ray
                k = int(rng.uniform(0.0, 1.0) * (len(ring) - 1))
                ring = ring[k:] + ring[:k + 1]
            pause_resume(ring, RD)
    for t in reversed(range(T_STEPS)):
        if red.pens[t] == RD:
            continue
        r_o, r_i = red.edge_r[t], red.edge_r[t + 1]
        ok = same_pen(red.pens[t])
        for sx, sy in _orbit(red, 0.5 * (r_o + r_i))[::2]:
            if occ.crowded(sx, sy):
                continue
            fw, _ = _trace(F, sx, sy, 1.0, ok, clip)
            bw, _ = _trace(F, sx, sy, -1.0, ok, clip)
            pause_resume(list(reversed(bw))[:-1] + fw, red.pens[t])

    # ---- 2. the arriving input: a narrow band of orbits just outside the
    #         figure-eight.  It passes no gate yet (pitch = kappa_in, the one
    #         drawing constant); the saddle decides which memory it feeds, and
    #         its colour is the basin it drains into — BLACK into the hidden
    #         state, BLUE into the cell's first (write) annulus.
    psi_hi = pair.psi(red.x, red.y - red.r_far - env)

    def outer_ok(li, t, x=None, y=None):
        return li == -1

    def fwd_ok(li, t):
        return li == -1 or (li == 0 and t < black.n) or (li == 1 and t == 0)

    def in_env(px, py):
        return pair.psi(px, py) < psi_hi

    seeds = []
    for j in range(int(env / 1.6)):
        d = 0.8 + 1.6 * j
        for sx, sy in _outer_orbit(pair, red, red.r_far + d)[::3]:
            seeds.append((sx, sy))
    rng.shuffle(seeds)
    for sx, sy in seeds:
        if occ.crowded(sx, sy) or not in_env(sx, sy) or abs(sy - pair.ys) > saddle_reach:
            continue
        fw, _ = _trace(F, sx, sy, 1.0, fwd_ok, clip, max_n=900)
        bw, _ = _trace(F, sx, sy, -1.0, lambda li, t: li == -1, clip, max_n=400)
        bw = [q for q in bw if in_env(*q)]
        k = 0
        while k < len(bw) and in_env(*bw[k]):
            k += 1
        path = list(reversed(bw[:k]))[:-1] + fw
        li_end, _t = F.where(*fw[-1])
        if li_end == 1:
            until_crowded(path, red.pens[0], warm=2)
        elif li_end == 0:
            until_crowded(path, BK, warm=2)

    # ---- 3. black: the hidden state fills in from just inside the separatrix
    inside_black = lambda li, t: li == 0 and t < black.n
    for frac in (0.0,):
        orb = _orbit(black, black.r_far - frac * (black.r_far - black.r_eye) - 0.5)
        for sx, sy in orb[::2]:
            if occ.crowded(sx, sy) or occ_h.crowded(sx, sy):
                continue
            fw, _ = _trace(F, sx, sy, 1.0, inside_black, clip)
            until_crowded(fw, BK, warm=1, min_run=16)

    # ---- the spine: one axis through both eyes.  It is drawn only where no
    #      line owns the paper (queried on the engine Occupancy), and a run
    #      shorter than 5 mm is dropped, so it reads as the spine between and
    #      beyond the vortices, never as a comb through them.
    y_ax0, y_ax1 = red.y - red.r_far - stub, black.y + black.r_far + stub
    run: List[Tuple[float, float]] = []
    for k in range(int((y_ax1 - y_ax0) / 0.4) + 1):
        py = y_ax0 + 0.4 * k
        if occ.crowded(cx, py) or occ_h.crowded(cx, py):
            if len(run) > 10:
                scene.poly(run, pen=BK)
            run = []
        else:
            run.append((cx, py))
    if len(run) > 10:
        scene.poly(run, pen=BK)

    # ---- type ---------------------------------------------------------------
    def text(t, x, y, h, pen=BK):
        cmds, w = _rich(t, x, y, h, pen, feed)
        out.extend(cmds)
        return w

    tx = x0 + 2.0
    # the title is the plate's second mass: display type with real weight,
    # set flush-left on the same edge as the footer
    out.extend(giant_type("LSTM", tx, y1 - 19.0, 15.0, pen=BK, weight=1.05, tip=0.35, f=feed))
    text("THE FORGET GATE IS A DRAIN", tx + 0.3, y1 - 26.5, 2.6)
    w = _rich("h_t", 0, 0, 3.2)[1]
    text("h_t", cx - w / 2, y_ax1 + 2.5, 3.2)
    w = _rich("c_t", 0, 0, 3.2)[1]
    text("c_t", cx - w / 2, y_ax0 - 6.0, 3.2, RD)
    # the whole legend is ONE footer line; each clause is inked in the pen it
    # describes, so the key is also the swatch
    key = [("ONE TURN = ONE STEP  \u00b7  RIM = FIRST, EYE = NOW  \u00b7  ", BK),
           ("RED: f_t KEEPS", RD), ("  \u00b7  ", BK), ("BLUE: i_t WRITES", BL),
           ("  \u00b7  ", BK), ("BLACK: o_t LETS GO", BK)]
    kx = tx
    for t_, pen_ in key:
        kx += text(t_, kx, y0 + 2.0, 2.2, pen_)

    return scene.render()
