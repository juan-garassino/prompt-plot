"""ATTENTION AS RESONANCE (FFN) -- THE SQUASH.  resonance-ffn r02, parent r01.

The FFN fan made the plate.  One streamline bundle crosses the sheet: it is
born on the left as the bright fringes of the Q/K two-source field, is pushed
through tanh in the middle (the outer lines are crushed against the +-1
asymptotes and end there), and fans out on the right.  Below it the SAME
bundle carries the gradient back.  Right of the gate the two are identical;
left of it every backward line reaches back toward Q and K only as far as
tanh'(u) lets its gradient through, so the ends of the lower fan trace
tanh' = 1 - tanh^2 itself: the notch is drawn by absence.

Everything drawn is computed here; nothing is traced, nothing is random.

THE FIELD.  Two coherent in-phase point sources, Q (crimson) and K (blue), on
one vertical line, d = N_LAM * LAM apart (a whole number of wavelengths, the
family's invariant).  Their crests are the Huygens circles r_s = m LAM.

THE FRINGES = THE STREAMLINES.  The bright fringes of a two-source field are
the loci  r_Q - r_K = m LAM  -- hyperbolae with foci Q and K,

    (y - yc)^2 / a^2 - (x - xs)^2 / b^2 = 1,   a = |m| LAM / 2,  b^2 = (d/2)^2 - a^2

They pass through every point where a Q crest crosses a K crest (crest i of Q
meets crest j of K on fringe m = j - i), and far from the pair they straighten
into rays at sin(theta_m) = m LAM / d.  Where Q and K resonate is drawn as a
FAN of lines.  (``self_check`` verifies r_Q - r_K = m LAM along every drawn
fringe.)

THE FFN (one hidden unit, applied to every fringe).  A fringe's offset from
the axis at the throat, X_FLAT, is its pre-activation:

    u_m = W1 * y_m(X_FLAT) / Y0 + B1        (B1 != 0: the squash is lopsided)
    h_m = tanh(u_m)                          throat height = B_TH * h_m
    o_m = W2 * h_m + B2                      the right fan: a linear map, i.e. rays

Between the gate and the throat each line eases from its fringe onto B_TH*h_m.

THE BACKWARD PASS.  L = sum_m o_m (a linear readout: every line receives the
same dL/do = 1), so  dL/dh_m = W2  and  dL/du_m = W2 (1 - h_m^2).  The share
of the gradient that crosses the tanh is 1 - h_m^2 (checked against a central
finite difference in ``self_check``).  Drawn: the backward bundle is the
forward geometry; a backward line's green part reaches (1 - h_m^2) of the way
from the gate back to the field's edge.  The gradient's own sources are drawn
with round(M_RING * mean(1 - h^2)) crest circles: the share that got back.

CROWDING (engine Occupancy, 0.8 mm).  A ``_Guard`` over the engine's
``Occupancy`` grid pauses a sample that runs within 0.8 mm of, and within 25
deg of parallel to, an earlier one (crossings survive).  Lines go centre-out,
so tanh's crushed outer lines are the ones that pause; inside the squash a
paused line stays paused (``lock``), so it ENDS rather than flickering.  Crest
circles are guarded the same way against each other and then block the fan,
so the fan is born at the edge of the field.

DOTS.  One mark, one pitch, family-wide: a round dot (a closed loop of radius
0.15 mm, inked ~0.65 mm across by a 0.35 nib) every DOT_PITCH = 1.0 mm,
end-anchored.  Used only for the +-1 asymptotes -- a dotted line is a line that
is approached and never reached.

Lineage: Bridget Riley, *Current* (1964) -- one family of lines whose spacing
alone makes the surface move.  Here the spacing is tanh'.

Pens (index = stream order, light -> dark; each pen one clean layer):
    0 dodgerblue   K: its crest circles (and dL/dK's)
    1 crimson      Q: its crest circles (and dL/dQ's)
    2 forestgreen  Z: the fringe fan up to the gate; dL/dZ left of the gate
    3 darkviolet   the FFN: squash, throat, right fan (forward and backward)
    4 black        the +-1 asymptotes (dotted), their two labels, the title

Entry point: ``resonance_ffn_squash``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.engine.scene3d import HIDE, Occupancy, Scene3D
from promptplot.generative.generators import _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

BLUE, RED, GREEN, VIOLET, BLACK = 0, 1, 2, 3, 4
PALETTE = "dodgerblue,crimson,forestgreen,darkviolet,black"

# --- physical ---------------------------------------------------------------
PEN_MM = 0.35            # the nib the plate is drawn for (0.3-0.4 mm fineliner)
SEP = 0.8                # line-spacing floor (house law)
DOT_PITCH = 1.0          # the family's continuous-dot pitch, centre to centre
STEP = 0.3               # streamline sample step, mm

# --- the field (sheet mm, y up) -----------------------------------------------
LAM = 1.2                # crest pitch
N_LAM = 37               # d = N_LAM * LAM  (whole number of wavelengths)
D_SRC = N_LAM * LAM      # 44.4 mm between Q and K
M_RING = 21              # crest circles drawn per source (r <= 25.2 mm)
M_FRINGE = 24            # fringes |m| <= M_FRINGE (asymptote <= 40.5 deg)

# --- the FFN -------------------------------------------------------------------
Y0 = 18.0                # mm of gate offset per unit of pre-activation
W1, B1 = 1.0, 0.28
W2, B2 = 1.0, 0.0
B_TH = 24.0              # throat half-height = the +-1 asymptote, mm
FAN_GAIN = 0.78          # right fan opens to (1 + FAN_GAIN) x the throat at the frame


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return idx % colors


# ---------------------------------------------------------------------------
# the model (pure maths; layout-free apart from the gate position)
# ---------------------------------------------------------------------------


def fringe_offset(m: int, x: float, xs: float) -> float:
    """Signed offset (mm, + = toward Q = up) of bright fringe m at abscissa x.

    r_Q - r_K = m LAM: positive m is nearer K, i.e. BELOW the axis."""
    if m == 0:
        return 0.0
    a = abs(m) * LAM / 2.0
    c = D_SRC / 2.0
    b = math.sqrt(c * c - a * a)
    y = a * math.sqrt(1.0 + ((x - xs) / b) ** 2)
    return -y if m > 0 else y


class Squash:
    """The forward and backward numbers for every fringe m."""

    def __init__(self, xs: float, x_throat: float) -> None:
        self.ms = list(range(-M_FRINGE, M_FRINGE + 1))
        self.off: Dict[int, float] = {}
        self.u: Dict[int, float] = {}
        self.h: Dict[int, float] = {}
        self.o: Dict[int, float] = {}
        self.g_o: Dict[int, float] = {}
        self.g_h: Dict[int, float] = {}
        self.g_u: Dict[int, float] = {}
        for m in self.ms:
            off = fringe_offset(m, x_throat, xs)
            u = W1 * off / Y0 + B1
            h = math.tanh(u)
            o = W2 * h + B2
            self.off[m], self.u[m], self.h[m], self.o[m] = off, u, h, o
            # L = sum_m o_m  (a linear readout: every line receives the same dL/do)
            self.g_o[m] = 1.0
            self.g_h[m] = W2
            self.g_u[m] = W2 * (1.0 - h * h)
        # the share of the gradient that gets back through the tanh
        self.survival = sum(1.0 - self.h[m] ** 2 for m in self.ms) / len(self.ms)
        self.n_back_rings = max(1, int(round(M_RING * self.survival)))


def self_check(bounds: Bounds = (10.0, 10.0, 200.0, 287.0)) -> Dict[str, float]:
    """The numbers NOTES.md quotes: fringe geometry and gradient, verified."""
    L = Layout(bounds)
    S = Squash(L.xs, L.xf)
    qy, ky = D_SRC / 2.0, -D_SRC / 2.0
    worst = 0.0
    for m in S.ms:
        for k in range(0, 400):
            x = L.xs + 0.5 * k
            y = fringe_offset(m, x, L.xs)
            rq = math.hypot(x - L.xs, y - qy)
            rk = math.hypot(x - L.xs, y - ky)
            worst = max(worst, abs((rq - rk) - m * LAM))
    fd = 0.0
    eps = 1e-6
    for m in S.ms:
        u = S.u[m]
        num = (W2 * math.tanh(u + eps) - W2 * math.tanh(u - eps)) / (2 * eps)
        fd = max(fd, abs(num - S.g_u[m]))
    crushed = [m for m in S.ms if B_TH * (1.0 - abs(S.h[m])) < SEP]
    return {
        "fringe_max_err_mm": worst,
        "grad_fd_max_err": fd,
        "survival": S.survival,
        "n_back_rings": S.n_back_rings,
        "u_min": min(S.u.values()), "u_max": max(S.u.values()),
        "lines": len(S.ms),
        "within_sep_of_rail": len(crushed),
        "gap_to_rail_top_mm": min(B_TH * (1 - S.h[m]) for m in S.ms),
        "gap_to_rail_bottom_mm": min(B_TH * (1 + S.h[m]) for m in S.ms),
    }


# ---------------------------------------------------------------------------
# small geometry helpers
# ---------------------------------------------------------------------------


def _dots(pts: Sequence[Pt], pen, pitch: float = DOT_PITCH) -> List[GCodeCommand]:
    """A continuous dotted line: round pen touches at a constant arclength
    pitch, END-ANCHORED (n = round(L / pitch) intervals, n + 1 dots)."""
    pts = [p for p in pts if p is not None]
    if len(pts) < 2:
        return []
    cum = [0.0]
    for a, b in zip(pts[:-1], pts[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    L = cum[-1]
    n = max(1, int(round(L / pitch)))
    out: List[GCodeCommand] = []
    j = 0
    for k in range(n + 1):
        s = L * k / n
        while j < len(cum) - 2 and cum[j + 1] < s:
            j += 1
        seg = cum[j + 1] - cum[j]
        t = 0.0 if seg < 1e-12 else (s - cum[j]) / seg
        x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * t
        y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * t
        out += _dot_mark(x, y, pen)
    return out


DOT_R = 0.15   # loop radius: with a 0.35 nib the inked dot is ~0.65 mm across


def _dot_mark(x: float, y: float, pen) -> List[GCodeCommand]:
    """One round dot, one pen-down: a closed loop of radius DOT_R (< nib/2, so
    the hole closes and the nib inks a solid round dot)."""
    return _poly([(x + DOT_R * math.cos(2 * math.pi * k / 8),
                   y + DOT_R * math.sin(2 * math.pi * k / 8)) for k in range(9)],
                 color=pen, f=1200)


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


class Layout:
    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        W, H = x1 - x0, y1 - y0
        self.xs = x0 + 0.075 * W            # the source line (Q over K)
        self.xg = x0 + 0.40 * W             # the gate: where Z enters the FFN
        self.xf = x0 + 0.56 * W             # squash complete: the throat
        self.xo = x0 + 0.70 * W             # the right fan begins
        self.xa = x0 + 0.4                  # lines run frame to frame
        self.xb = x1 - 0.4
        self.yc = y0 + 0.70 * H             # forward axis
        self.yb = y0 + 0.262 * H            # backward axis

    def grow(self, x: float) -> float:
        """Right-fan opening: 0 up to xo, then a C1 start into straight rays
        (a linear map draws rays), FAN_GAIN at the frame."""
        if x <= self.xo:
            return 0.0
        xi = (x - self.xo) / (self.xb - self.xo)
        return FAN_GAIN * (math.sqrt(xi * xi + 0.04) - 0.2) / (math.sqrt(1.04) - 0.2)


def _ease(L: Layout, x: float) -> float:
    """0 at the gate -> 1 at the throat; starts at full rate (the squash grabs
    the lines at once), arrives with zero slope (C1 into the throat)."""
    t = min(max((x - L.xg) / (L.xf - L.xg), 0.0), 1.0)
    return 1.0 - (1.0 - t) * (1.0 - t)


def fwd_offset(L: Layout, S: Squash, m: int, x: float) -> float:
    """Left of the gate: the fringe.  Gate -> throat: the fringe pulled onto
    B_TH * h_m = B_TH * tanh(u_m).  Throat: B_TH * h_m.  Right: the linear fan."""
    if x < L.xg:
        return fringe_offset(m, x, L.xs)
    if x < L.xf:
        s = _ease(L, x)
        return (1.0 - s) * fringe_offset(m, x, L.xs) + s * B_TH * S.h[m]
    return B_TH * S.h[m] * (1.0 + L.grow(x))


class _Guard:
    """Crowd control on top of the engine's ``Occupancy`` grid: a sample is
    crowded if an earlier sample lies within SEP AND runs within 25 degrees of
    parallel (crossings survive -- they plot fine); entries registered with no
    direction (the crest field) block everything."""

    def __init__(self, sep: float = SEP) -> None:
        self.occ = Occupancy(sep)
        self.dirs: Dict[Tuple[float, float], List[Optional[Tuple[float, float]]]] = {}

    def add(self, x: float, y: float, d: Optional[Tuple[float, float]] = None) -> None:
        self.occ.add(x, y)
        self.dirs.setdefault((x, y), []).append(d)

    def crowded(self, x: float, y: float, d: Tuple[float, float]) -> bool:
        occ = self.occ
        ci, cj = occ._cell(x, y)
        s2 = occ.sep * occ.sep
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for qx, qy in occ._grid.get((ci + di, cj + dj), ()):
                    if (qx - x) ** 2 + (qy - y) ** 2 >= s2:
                        continue
                    for qd in self.dirs.get((qx, qy), ()):
                        if qd is None or abs(qd[0] * d[0] + qd[1] * d[1]) > 0.906:
                            return True
        return False


MIN_RUN = 8.0   # mm: a resumed stretch shorter than this is not worth a pen cycle


def _family(scene: Scene3D, guard: _Guard, lines, lock: Optional[Tuple[float, float]] = None,
            feed: Optional[int] = None, min_run: Optional[float] = None) -> List[Pt]:
    """Pause-and-resume a family against ``guard`` (first come, first served).

    ``lock`` = (xa, xb): inside this stretch a paused line STAYS paused (a line
    crushed onto the rail does not flicker back in dashes).  Resumed stretches
    shorter than MIN_RUN are dropped.  Returns every kept point."""
    kept: List[Pt] = []
    for m, line in lines:
        n = len(line)
        keep = []
        dirs = []
        # walk in the x-increasing sense for the lock rule, whatever the stroke direction
        idx = list(range(n)) if line[0][0] <= line[-1][0] else list(range(n))[::-1]
        for i in range(n):
            x, y, pen, gap = line[i]
            a = line[max(0, i - 1)]
            b = line[min(n - 1, i + 1)]
            dx, dy = b[0] - a[0], b[1] - a[1]
            dn = math.hypot(dx, dy) or 1.0
            dirs.append((dx / dn, dy / dn))
            keep.append(False)
        locked = False
        for i in idx:
            x, y, pen, gap = line[i]
            crowded = guard.crowded(x, y, dirs[i])
            ok = (not gap) and not crowded
            if lock is not None and lock[0] <= x <= lock[1]:
                if crowded:
                    locked = True
                if locked:
                    ok = False
            else:
                locked = False
            keep[i] = ok
        i = 0
        while i < n:
            if not keep[i]:
                i += 1
                continue
            j = i
            length = 0.0
            while j + 1 < n and keep[j + 1] and line[j + 1][2] == line[i][2]:
                length += math.hypot(line[j + 1][0] - line[j][0], line[j + 1][1] - line[j][1])
                j += 1
            if length < (MIN_RUN if min_run is None else min_run):
                for k in range(i, j + 1):
                    keep[k] = False
            i = j + 1
        for i, (x, y, pen, gap) in enumerate(line):
            if keep[i]:
                guard.add(x, y, dirs[i])
                kept.append((x, y))
        scene.lines([[(x, y, 0.0 if keep[i] else HIDE, pen)
                      for i, (x, y, pen, gap) in enumerate(line)]], mode="over", feed=feed)
    return kept


def _bundle(L: Layout, S: Squash, colors: int, offset, yaxis: float, reach=None):
    """``reach(m)`` (backward only): the x left of which line m is not drawn."""
    gr, vi = _pen(GREEN, colors), _pen(VIOLET, colors)
    n = int((L.xb - L.xa) / STEP)
    order = sorted(S.ms, key=lambda m: (abs(m), m))     # centre-out: inner lines win
    lines = []
    for idx, m in enumerate(order):
        samples = []
        for k in range(n + 1):
            x = L.xa + k * STEP
            y = yaxis + offset(L, S, m, x)
            pen = gr if x < L.xg else vi
            # the gate: a hairline of blank paper where Z hands over to the FFN
            gap = abs(x - L.xg) < 0.45 or (reach is not None and x < reach(m))
            samples.append((x, y, pen, gap))
        if idx % 2 == 1:
            samples = samples[::-1]     # boustrophedon: neighbours alternate
        lines.append((m, samples))
    return lines


def _rail_pts(L: Layout, sgn: float, yaxis: float) -> List[Pt]:
    xa = L.xg + 0.62 * (L.xf - L.xg)
    n = int((L.xb - xa) / 0.5)
    return [(xa + (L.xb - xa) * k / n,
             yaxis + sgn * B_TH * (1.0 + L.grow(xa + (L.xb - xa) * k / n))) for k in range(n + 1)]


def _rings(scene: Scene3D, guard: _Guard, L: Layout, yaxis: float, count: int, colors: int):
    """Q's and K's crest circles, interleaved by m.  Between the sources the
    two families run tangent (a Q crest's foot on a K crest's crown); a ring
    pauses where it would run within SEP of, and parallel to, one already
    drawn (the family's crest guard), so the lens reads as crossings, not mud.
    Every kept point then blocks the fan (``guard``)."""
    rg = _Guard()
    lines = []
    for m in range(1, count + 1):
        for sy, slot in ((yaxis + D_SRC / 2.0, RED), (yaxis - D_SRC / 2.0, BLUE)):
            r = m * LAM
            nn = max(48, int(2 * math.pi * r / 0.45))
            pen = _pen(slot, colors)
            pts = []
            for k in range(nn + 1):
                x = L.xs + r * math.cos(2 * math.pi * k / nn)
                y = sy + r * math.sin(2 * math.pi * k / nn)
                pts.append((x, y, pen, not (L.xa <= x <= L.xb)))
            lines.append((m, pts))
    for x, y in _family(scene, rg, lines, feed=2200, min_run=2.0):
        guard.add(x, y, None)


def build(bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    L = Layout(bounds)
    S = Squash(L.xs, L.xf)
    scene = Scene3D(None, bounds, fit="none", tip=PEN_MM)
    gf, gb = _Guard(), _Guard()

    # 1. the field: crest circles of Q and K, clipped to the sheet; they block
    #    the fan, so the fringes are born at the field's edge.  Below, the
    #    gradient's sources: the same circles, as many as the share of the
    #    gradient that survives the tanh (mean of 1 - h^2 over the fringes).
    _rings(scene, gf, L, L.yc, M_RING, colors)
    _rings(scene, gb, L, L.yb, S.n_back_rings, colors)

    # 2. the +-1 asymptotes (dotted) register first: crushed lines pause under them
    bk = _pen(BLACK, colors)
    for sgn in (1.0, -1.0):
        pts = _rail_pts(L, sgn, L.yc)
        for i, (x, y) in enumerate(pts):
            gf.add(x, y, None)
        scene.emit(_dots(pts, bk))

    # 3. the bundles
    _family(scene, gf, _bundle(L, S, colors, fwd_offset, L.yc), lock=(L.xg, L.xo))

    # Backward: right of the gate the bundle IS the forward one (dL/do = 1 on
    # every line, dL/dh = W2).  Left of the gate each line reaches back toward
    # the sources only as far as its share of the gradient carries it:
    # reach = tanh'(u_m) = 1 - h_m^2 of the way from the gate to the field's
    # edge.  The line ENDS trace tanh' itself -- the notch is drawn by absence.
    x_edge = L.xs + S.n_back_rings * LAM + 2.0

    def reach(m: int) -> float:
        return L.xg - (1.0 - S.h[m] ** 2) * (L.xg - x_edge)

    _family(scene, gb, _bundle(L, S, colors, fwd_offset, L.yb, reach=reach), lock=(L.xg, L.xo))

    # 4. type, on its own pen: the title bottom-left in the quiet quadrant
    h = 3.0
    title = "ATTENTION AS RESONANCE"
    scene.halo_labels([(title, L.x0 + 2.0, L.y0 + 9.0, h, bk),
                       ("FFN · THE SQUASH", L.x0 + 2.0, L.y0 + 3.5, 2.2, bk),
                       # the asymptotes, named once, on the flat of the throat
                       ("+1", L.xf - 4.0, L.yc + B_TH + 1.6, 2.2, bk),
                       ("−1", L.xf - 4.0, L.yc - B_TH - 3.8, 2.2, bk)])
    return scene.render()


def resonance_ffn_squash(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    """Deterministic: every number is computed from the constants above; ``rng``
    is kept for the contract (nothing on this plate is random)."""
    return build(bounds, colors)
