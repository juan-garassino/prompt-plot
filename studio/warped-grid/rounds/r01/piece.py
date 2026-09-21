"""WARPED GRID — exact recreation of studio/warped-grid/ref/reference.png.

Attention as a plate: Q and K spiral-contour clusters feed a warped Q.K^T
lattice, softmax lifts it into the A surface, V joins, Z = AV closes.

Every position in this module is expressed in REFERENCE PIXELS of the
1086x1448 plate and mapped to millimetres once, by ``_Sheet``.  That is the
only way the labels stayed the right size: measured off the raster, never
judged by eye.

Contract:  warped_grid(rng, bounds, colors=5) -> list[GCodeCommand]
Pens: 0 red (Q) · 1 blue (K) · 2 ochre (V) · 3 green (Z) · 4 black (frame).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.engine import kit
from promptplot.generative.engine.kit import (
    _catmull_subdivide,
    _chain_segments,
    _dot,
    _marching_squares,
    _poly,
    _stroke_text,
    _text_width,
)
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

REF_W, REF_H = 1086.0, 1448.0

RED, BLUE, OCHRE, GREEN, BLACK = 0, 1, 2, 3, 4

FEED = 2100


# ---------------------------------------------------------------------------
# sheet mapping: reference pixels -> millimetres
# ---------------------------------------------------------------------------


class _Sheet:
    """Cover-free FIT of the 3:4 reference plate into the drawable area."""

    def __init__(self, bounds: Bounds, colors: int = 5) -> None:
        self.colors = max(1, int(colors))
        x0, y0, x1, y1 = bounds
        self.s = min((x1 - x0) / REF_W, (y1 - y0) / REF_H)
        self.ox = x0 + ((x1 - x0) - REF_W * self.s) / 2.0
        self.oy = y1 - ((y1 - y0) - REF_H * self.s) / 2.0
        self.mm = 1.0 / self.s  # reference pixels per millimetre

    def p(self, px: float, py: float) -> Pt:
        return (self.ox + px * self.s, self.oy - py * self.s)

    def pen(self, idx: Optional[int]) -> Optional[int]:
        """Fold a plate pen index onto however many pens the caller has."""
        if idx is None or self.colors <= 1:
            return None
        return idx % self.colors

    def poly(self, pts: Sequence[Pt], pen: Optional[int], f: int = FEED) -> List[GCodeCommand]:
        if len(pts) < 2:
            return []
        return _poly([self.p(x, y) for x, y in pts], color=self.pen(pen), f=f)

    def dot(self, px: float, py: float, r_px: float, pen: Optional[int]) -> List[GCodeCommand]:
        """A filled dot of radius ``r_px`` reference pixels."""
        r = r_px * self.s
        if r <= 0.22:
            return _dot(*self.p(px, py), r=max(0.16, r), color=self.pen(pen), f=1400)
        return kit.fill_disc(*self.p(px, py), r=r, spacing=0.22, pen=self.pen(pen), f=1600)

    def ring(self, px: float, py: float, r_px: float, pen: Optional[int], n: int = 64):
        return kit.circle(*self.p(px, py), r=r_px * self.s, pen=self.pen(pen), f=FEED, n=n)

    def text(
        self,
        s: str,
        px: float,
        py: float,
        cap_px: float,
        pen: Optional[int],
        anchor: str = "left",
    ) -> List[GCodeCommand]:
        """Single-stroke text; (px, py) is the LEFT BASELINE in reference px."""
        h = cap_px * self.s
        w = _text_width(s, h, proportional=True)
        x, y = self.p(px, py)
        if anchor == "center":
            x -= w / 2.0
        elif anchor == "right":
            x -= w
        return _stroke_text(s, x, y, h, color=self.pen(pen), f=2300, proportional=True)

    def text_width_px(self, s: str, cap_px: float) -> float:
        return _text_width(s, cap_px * self.s, proportional=True) * self.mm


# ---------------------------------------------------------------------------
# small drawing helpers (all in reference pixels)
# ---------------------------------------------------------------------------


def _resample(pts: Sequence[Pt], step: float) -> List[Pt]:
    """Resample a polyline to an even arc-length step."""
    if len(pts) < 2:
        return list(pts)
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d < 1e-9:
            continue
        t = step - acc
        while t <= d:
            out.append((a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d))
            t += step
        acc = (acc + d) % step
    out.append(pts[-1])
    return out


def _dashes(pts: Sequence[Pt], on: float, off: float) -> List[List[Pt]]:
    """Split a polyline into dashes of ``on`` px separated by ``off`` px."""
    segs: List[List[Pt]] = []
    cur: List[Pt] = []
    run = 0.0
    drawing = True
    for a, b in zip(pts, pts[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if d < 1e-9:
            continue
        t = 0.0
        while t < d:
            lim = (on if drawing else off) - run
            take = min(lim, d - t)
            p0 = (a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d)
            t += take
            p1 = (a[0] + (b[0] - a[0]) * t / d, a[1] + (b[1] - a[1]) * t / d)
            if drawing:
                if not cur:
                    cur = [p0]
                cur.append(p1)
            run += take
            if run >= (on if drawing else off) - 1e-9:
                if drawing and len(cur) >= 2:
                    segs.append(cur)
                cur = []
                drawing = not drawing
                run = 0.0
    if drawing and len(cur) >= 2:
        segs.append(cur)
    return segs


# Every label's footprint, padded.  House law: an overlap has to be one you
# would defend out loud.  A dashed halo crossing a letterform is never that --
# it is the halo running out of room -- so the halo yields and the type keeps
# its air.  Deliberate overlaps (the V sweeps crossing into the A plane, the
# crowding at the lattice pinch) are NOT listed here and stay.
_TYPE_KEEPOUT: Tuple[Tuple[float, float, float, float], ...] = (
    (78.0, 70.0, 142.0, 146.0),      # Q
    (942.0, 84.0, 1008.0, 150.0),    # K
    (933.0, 898.0, 994.0, 962.0),    # V
    (264.0, 806.0, 314.0, 856.0),    # A
    (135.0, 1142.0, 275.0, 1202.0),  # Z = AV
    (43.0, 328.0, 112.0, 354.0),     # (n x d) under Q
    (969.0, 343.0, 1044.0, 369.0),   # (n x d) under K
    (701.0, 675.0, 770.0, 701.0),    # (n x n) beside the lattice
    (243.0, 862.0, 316.0, 888.0),    # (n x n) beside A
    (980.0, 1101.0, 1050.0, 1127.0), # (n x d) under V
    (154.0, 1200.0, 224.0, 1226.0),  # (n x d) under Z
    (498.0, 412.0, 592.0, 460.0),    # Q . K^T
    (486.0, 732.0, 594.0, 762.0),    # softmax
    (988.0, 168.0, 1036.0, 342.0),   # K bracket + dot column
    (978.0, 966.0, 1030.0, 1098.0),  # V bracket + dot column
    (48.0, 172.0, 68.0, 288.0),      # Q dot column
)


def _clear_of_type(pts: Sequence[Pt]) -> bool:
    for x, y in pts:
        for x0, y0, x1, y1 in _TYPE_KEEPOUT:
            if x0 <= x <= x1 and y0 <= y <= y1:
                return False
    return True


def _smooth(ctrl: Sequence[Pt], subdiv: int = 12) -> List[Pt]:
    pts, _ = _catmull_subdivide(list(ctrl), None, subdiv=subdiv)
    return pts


def _arrow(sh: _Sheet, tail: Pt, tip: Pt, pen: Optional[int], head: float = 11.0,
           ctrl: Optional[Sequence[Pt]] = None) -> List[GCodeCommand]:
    """Straight (or catmull-guided) arrow with a solid V head, reference px."""
    path = _smooth([tail] + list(ctrl) + [tip]) if ctrl else [tail, tip]
    out = sh.poly(path, pen)
    ax, ay = path[-2]
    bx, by = path[-1]
    ang = math.atan2(by - ay, bx - ax)
    for sgn in (+1, -1):
        a = ang + math.pi + sgn * 0.30
        out += sh.poly([(bx, by), (bx + head * math.cos(a), by + head * math.sin(a))], pen)
    a1 = ang + math.pi + 0.30
    a2 = ang + math.pi - 0.30
    out += sh.poly(
        [
            (bx + head * math.cos(a1) * 0.62, by + head * math.sin(a1) * 0.62),
            (bx + head * math.cos(a2) * 0.62, by + head * math.sin(a2) * 0.62),
        ],
        pen,
    )
    return out


def _bracket(sh: _Sheet, x: float, y0: float, y1: float, side: int, pen: int,
             serif: float = 16.0) -> List[GCodeCommand]:
    """A square bracket. side=+1 opens right ('['), side=-1 opens left (']')."""
    return sh.poly(
        [(x + side * serif, y0), (x, y0), (x, y1), (x + side * serif, y1)], pen
    )


def _dot_column(sh: _Sheet, x: float, y0: float, y1: float, n: int, r: float,
                pen: int) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for k in range(n):
        out += sh.dot(x, y0 + (y1 - y0) * k / (n - 1), r, pen)
    return out


# ---------------------------------------------------------------------------
# contour engine — "conical" log-cusps, rings a fixed distance apart
# ---------------------------------------------------------------------------


def _cusp_profile(r: float, rmax: float, g0: float, slope: float) -> float:
    """Height profile whose ARITHMETIC contours sit ``g0 + slope*r`` apart.

    A Gaussian spreads its rings exactly at the summit; a pure exponential
    cusp spreads them exponentially outward.  Integrating 1/(g0 + slope*r)
    gives a cusp that keeps the innermost gap at ``g0`` (the pen-safety floor)
    and lets it open only gently outward, which is what the plate shows.
    """
    if r >= rmax:
        return 0.0
    return (math.log(g0 + slope * rmax) - math.log(g0 + slope * r)) / slope


def _field(peaks: Sequence[Tuple[float, float, float, float]], x0: float, y0: float,
           x1: float, y1: float, cell: float, g0: float, slope: float):
    """Sample sum-of-cusps on a grid.  peaks = (x, y, rmax, amp)."""
    nx = int((x1 - x0) / cell) + 1
    ny = int((y1 - y0) / cell) + 1
    xs = [x0 + i * cell for i in range(nx)]
    ys = [y0 + j * cell for j in range(ny)]
    F = [[0.0] * nx for _ in range(ny)]
    for px, py, rmax, amp in peaks:
        i0 = max(0, int((px - rmax - x0) / cell))
        i1 = min(nx - 1, int((px + rmax - x0) / cell) + 1)
        j0 = max(0, int((py - rmax - y0) / cell))
        j1 = min(ny - 1, int((py + rmax - y0) / cell) + 1)
        for j in range(j0, j1 + 1):
            dy = ys[j] - py
            row = F[j]
            for i in range(i0, i1 + 1):
                dx = xs[i] - px
                r = math.sqrt(dx * dx + dy * dy)
                if r < rmax:
                    row[i] += amp * _cusp_profile(r, rmax, g0, slope)
    return F, xs, ys


def _contours(F, xs, ys, levels: Sequence[float], min_len: int = 5) -> List[List[Pt]]:
    out: List[List[Pt]] = []
    for lv in levels:
        for chain in _chain_segments(_marching_squares(F, xs, ys, lv)):
            if len(chain) >= min_len:
                out.append(chain)
    return out


def _cusp_radius(level: float, amp: float, rmax: float, g0: float, slope: float) -> float:
    """Invert the cusp profile: radius of the iso-``level`` ring around one peak."""
    if amp <= 0 or level <= 0:
        return -1.0
    lg = math.log(g0 + slope * rmax) - slope * level / amp
    r = (math.exp(lg) - g0) / slope
    return r if 0.0 <= r < rmax else -1.0


def _nest_eyes(
    peaks: Sequence[Tuple[float, float, float, float]],
    levels: Sequence[float],
    g0: float,
    slope: float,
) -> Tuple[List[Tuple[float, float, float]], List[float]]:
    """Exact circles for the DENSE EYE of every cusp, plus a switch radius.

    Marching squares cannot resolve a ring whose radius is a couple of grid
    cells, which is exactly the part of a spiral nest that carries the plate:
    the tight centre.  Near its own summit each cusp is isolated, so the ring
    IS a circle and can be emitted exactly.  Returns (circles, switch_radii);
    contour chains smaller than the switch radius are dropped in favour of
    these.
    """
    switch: List[float] = []
    base: List[float] = []
    for i, (xi, yi, ri, _ai) in enumerate(peaks):
        dmin = min(
            (math.hypot(xi - xj, yi - yj) for j, (xj, yj, _, _) in enumerate(peaks) if j != i),
            default=ri * 2.0,
        )
        switch.append(min(0.46 * dmin, 0.60 * ri))
        base.append(
            sum(
                aj * _cusp_profile(math.hypot(xi - xj, yi - yj), rj, g0, slope)
                for j, (xj, yj, rj, aj) in enumerate(peaks)
                if j != i
            )
        )
    circles: List[Tuple[float, float, float, float]] = []
    for lv in levels:
        for i, (xi, yi, ri, ai) in enumerate(peaks):
            r = _cusp_radius(lv - base[i], ai, ri, g0, slope)
            if 0.0 < r <= switch[i]:
                circles.append((xi, yi, r, lv))
    return circles, switch


def _too_small(chain: Sequence[Pt], peaks, switch: Sequence[float]) -> bool:
    """True when a contour chain is an eye ring the analytic pass already owns."""
    cx = sum(p[0] for p in chain) / len(chain)
    cy = sum(p[1] for p in chain) / len(chain)
    rad = max(math.hypot(p[0] - cx, p[1] - cy) for p in chain)
    best, bi = 1e18, 0
    for i, (xi, yi, _, _) in enumerate(peaks):
        d = math.hypot(cx - xi, cy - yi)
        if d < best:
            best, bi = d, i
    return rad <= switch[bi] * 1.02


def _nest_levels(F, cell: float, g0_px: float, amp_max: float,
                 quantile: float = 0.82) -> List[float]:
    """Iso-values by GRADIENT (kit.even_contour_levels), floored for pen safety.

    even_contour_levels keeps the rings a fixed distance apart instead of
    letting them bunch wherever the field is steep.  The floor is exact for
    this profile: |dF/dr| = amp/(g0 + slope*r), so a level step of ``amp_max``
    puts the innermost ring of the tallest cusp exactly ``g0`` apart -- the
    pen-spacing minimum -- and every ring further out is wider still.
    """
    lv = kit.even_contour_levels(F, spacing=g0_px, quantile=quantile, n_max=80, cell=cell)
    safe = max(amp_max, 1e-6)
    if len(lv) >= 2 and (lv[1] - lv[0]) >= safe:
        return lv
    hi = max(max(row) for row in F)
    n = max(1, int(hi / safe))
    return [safe * (k + 0.5) for k in range(n)]


# ---------------------------------------------------------------------------
# Q / K / V cluster
# ---------------------------------------------------------------------------


def _cluster(
    sh: _Sheet,
    pen: int,
    nests: Sequence[Tuple[float, float, float, float]],
    box: Tuple[float, float, float, float],
    links: Sequence[Sequence[Pt]],
    fans: Sequence[Tuple[int, Pt, float, int]],
    node_r: float = 5.6,
) -> List[GCodeCommand]:
    """Spiral-contour nests + linking curves + fan + dashed halo."""
    out: List[GCodeCommand] = []
    g0 = 0.88 * sh.mm          # innermost ring gap, px
    slope = 0.042

    x0, y0, x1, y1 = box
    cell = 0.82 * sh.mm
    F, xs, ys = _field(nests, x0, y0, x1, y1, cell, g0, slope)
    amp_max = max(a for _, _, _, a in nests)
    levels = _nest_levels(F, cell, g0, amp_max)[1:]
    circles, switch = _nest_eyes(nests, levels, g0, slope)
    for chain in _contours(F, xs, ys, levels):
        if _too_small(chain, nests, switch):
            continue
        out += sh.poly(_smooth(chain, 3) if len(chain) >= 4 else chain, pen, f=2300)
    for cxp, cyp, r, _lv in circles:
        out += sh.ring(cxp, cyp, r, pen, n=max(20, min(96, int(r * 2.4))))

    # linking curves through scattered nodes
    nodes: List[Pt] = []
    for ctrl in links:
        out += sh.poly(_smooth(ctrl, 14), pen, f=2200)
        nodes.extend(ctrl[1:-1])

    # fans: a bundle of curves leaving a nest centre and re-converging
    # Fans leave the eye on a short ARC, not from one point: six strokes
    # sharing an origin stack inside the pen width for their first few
    # millimetres.  The eye's dot covers the gap, so it still reads as
    # emerging from the centre, which is what the plate shows.
    for idx, tip, spread, count in fans:
        cx, cy, _, _ = nests[idx]
        dx, dy = tip[0] - cx, tip[1] - cy
        L = max(1.0, math.hypot(dx, dy))
        ux, uy = dx / L, dy / L
        r0 = 3.0 * sh.mm
        for k in range(count):
            t = (k / (count - 1.0)) - 0.5 if count > 1 else 0.0
            sx = cx + ux * r0 - uy * t * spread * 0.34
            sy = cy + uy * r0 + ux * t * spread * 0.34
            mx = (cx + tip[0]) / 2.0 + t * spread * uy
            my = (cy + tip[1]) / 2.0 - t * spread * ux
            out += sh.poly(
                _smooth(
                    [
                        (sx, sy),
                        (sx + (mx - sx) * 0.34, sy + (my - sy) * 0.34),
                        (mx, my),
                        (tip[0] - (tip[0] - mx) * 0.24, tip[1] - (tip[1] - my) * 0.24),
                        tip,
                    ],
                    12,
                ),
                pen,
                f=2200,
            )

    # Dashed halo. Taking it from an INFLATED copy of the same field (rather
    # than a hand-drawn oval) makes it follow the cluster's own lobed
    # silhouette, which is what the plate does, and guarantees it clears the
    # contours by a constant margin instead of grazing them somewhere.
    if levels:
        hF, hxs, hys = _field(
            [(px, py, rmax * 1.42, amp) for px, py, rmax, amp in nests],
            x0, y0, x1, y1, cell * 2.4, g0, slope,
        )
        for chain in _contours(hF, hxs, hys, [levels[0] * 0.34], min_len=30):
            for seg in _dashes(_resample(_smooth(chain, 4), 2.4), 4.0, 9.0):
                if _clear_of_type(seg):
                    out += sh.poly(seg, BLACK, f=2500)

    # nest centres, then the link nodes
    # The eye's dot has to fit INSIDE the innermost analytic ring; sized up to
    # "look right" it swallows two rings and the nest loses its spiral.
    for px, py, _, amp in nests:
        out += sh.dot(px, py, node_r * (0.62 + 0.20 * amp), pen)
    for nx, ny in nodes:
        out += sh.dot(nx, ny, node_r * 0.72, pen)
    return out


# ---------------------------------------------------------------------------
# the hero: warped Q.K^T lattice
# ---------------------------------------------------------------------------

LAT_X0, LAT_X1 = 420.0, 663.0
LAT_Y0, LAT_Y1 = 462.0, 693.0
LAT_N = 12  # cells; 13 nodes each way

_LAT_AX = 2.10      # horizontal distances count for more -> a weaker sideways pull
_LAT_RC = math.hypot(_LAT_AX, 1.0)   # corner radius: the map's fixed circle
_LAT_P = 1.45       # power-law exponent - 1
_LAT_FLOOR = 0.24   # residual scale, so the innermost ring of nodes cannot merge


def _lens(a: float, b: float) -> Tuple[float, float]:
    """The central pinch: a power-law radial compression on a stretched metric.

    r' = rc*(r/rc)^p pulls every point toward the centre by a fraction that
    grows all the way in, which is what makes the whole sheet read as ONE
    deformed fabric rather than two rigid halves either side of a waist -- the
    failure mode of any lens with a narrow window.  Two corrections earn their
    keep against the measured plate: the metric stretches x by ``_LAT_AX`` (on
    the reference the top and bottom rows dive far more than the outer columns
    slide, so the pull is not isotropic), and a residual ``_LAT_FLOOR`` keeps
    the innermost nodes ~0.8 mm apart instead of collapsing onto the centre.
    The corner circle r = rc is fixed, so the frame stays put and the
    deformation is visibly interior.
    """
    r = math.hypot(_LAT_AX * a, b)
    if r < 1e-9:
        return 0.0, 0.0
    f = (1.0 - _LAT_FLOOR) * (min(r, _LAT_RC) / _LAT_RC) ** _LAT_P + _LAT_FLOOR
    f = min(1.0, f)
    # Damp the sideways pull on the top/bottom rows and the vertical pull on
    # the outer columns.  Without this the radial map drags the top row's
    # nodes together as well as down and the edge closes to a V; on the plate
    # it stays a broad U with its own spacing intact.
    fx = f + (1.0 - f) * min(1.0, b * b) * 0.85
    fy = f + (1.0 - f) * min(1.0, a * a) * 0.75
    return a * fx, b * fy


def _lat_pt(u: float, v: float) -> Pt:
    """u, v in [-1, 1] -> warped reference-pixel position."""
    a, b = _lens(u, v)
    cx = (LAT_X0 + LAT_X1) / 2.0
    cy = (LAT_Y0 + LAT_Y1) / 2.0
    return (cx + a * (LAT_X1 - LAT_X0) / 2.0, cy + b * (LAT_Y1 - LAT_Y0) / 2.0)


def _lattice(sh: _Sheet) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    cy = (LAT_Y0 + LAT_Y1) / 2.0

    # Ghost rows: the UNDISTORTED row heights, as short rules in the margin
    # either side of the field.  The plate draws them at 25% grey straight
    # across; one pen cannot, and dashing them across the field turned the
    # whole lattice into a striped background -- crowding, not composition.
    # Kept where they read as a datum and nothing else has to share the space.
    for j in range(LAT_N + 1):
        v = -1.0 + 2.0 * j / LAT_N
        y = cy + v * (LAT_Y1 - LAT_Y0) / 2.0
        out += sh.poly([(LAT_X0 - 15.0, y), (LAT_X0 - 3.0, y)], BLACK, f=2600)
        out += sh.poly([(LAT_X1 + 3.0, y), (LAT_X1 + 14.0, y)], BLACK, f=2600)

    steps = 84
    for i in range(LAT_N + 1):  # columns
        u = -1.0 + 2.0 * i / LAT_N
        out += sh.poly(
            [_lat_pt(u, -1.0 + 2.0 * k / steps) for k in range(steps + 1)], BLACK, f=2200
        )
    for j in range(LAT_N + 1):  # rows
        v = -1.0 + 2.0 * j / LAT_N
        out += sh.poly(
            [_lat_pt(-1.0 + 2.0 * k / steps, v) for k in range(steps + 1)], BLACK, f=2200
        )

    # nodes: radius follows the local cell size, so the core cannot blob
    h = 1.0 / LAT_N
    for j in range(LAT_N + 1):
        v = -1.0 + 2.0 * j / LAT_N
        for i in range(LAT_N + 1):
            u = -1.0 + 2.0 * i / LAT_N
            p = _lat_pt(u, v)
            pu = _lat_pt(min(1.0, u + h), v)
            pv = _lat_pt(u, min(1.0, v + h))
            d = 0.5 * (math.hypot(pu[0] - p[0], pu[1] - p[1])
                       + math.hypot(pv[0] - p[0], pv[1] - p[1]))
            r = min(4.3, max(1.15, 0.24 * d))
            out += sh.dot(p[0], p[1], r, BLACK)

    # brackets with a node on each, plus the loose node outside the right one
    for x, side in ((397.0, +1), (686.0, -1)):
        out += _bracket(sh, x, LAT_Y0 - 3.0, LAT_Y1 + 3.0, side, BLACK, serif=13.0)
        out += sh.dot(x, cy, 4.0, BLACK)
    out += sh.dot(697.0, cy, 4.0, BLACK)
    return out


# ---------------------------------------------------------------------------
# the A surface — a perspective ground plane carrying five contour peaks
# ---------------------------------------------------------------------------

A_BACK_Y, A_FRONT_Y = 805.0, 946.0
A_BACK_HW, A_FRONT_HW = 170.0, 254.0
A_CX = 542.0
A_ROWS, A_COLS = 5, 12
A_K = 1.18  # row-gap growth toward the viewer
A_DEPTH = 380.0  # world depth of the plane


def _a_v_of(t: float) -> float:
    """t in [0, 1] (back -> front) -> normalised screen depth."""
    return (A_K ** (A_ROWS * t) - 1.0) / (A_K ** A_ROWS - 1.0)


def _a_t_of(v: float) -> float:
    return math.log(1.0 + v * (A_K ** A_ROWS - 1.0)) / (A_ROWS * math.log(A_K))


def _a_ground(U: float, V: float) -> Pt:
    """World (U across, V back->front) -> screen reference px, on the plane."""
    t = V / A_DEPTH
    v = _a_v_of(t)
    y = A_BACK_Y + (A_FRONT_Y - A_BACK_Y) * v
    hw = A_BACK_HW + (A_FRONT_HW - A_BACK_HW) * v
    return (A_CX + (U / A_FRONT_HW) * hw, y)


A_PEAKS = [
    # (U, V, world radius, screen height)
    (-192.8, 286.9, 72.0, 42.0),
    (-127.5, 139.8, 92.0, 56.0),
    (1.0, 277.8, 110.0, 68.0),
    (93.2, 127.3, 76.0, 40.0),
    (194.8, 277.8, 72.0, 44.0),
]


def _a_surface(sh: _Sheet) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []

    # plane grid
    for j in range(A_ROWS + 1):
        V = A_DEPTH * j / A_ROWS
        p0 = _a_ground(-A_FRONT_HW, V)
        p1 = _a_ground(A_FRONT_HW, V)
        out += sh.poly([p0, p1], BLACK, f=2500)
    for i in range(A_COLS + 1):
        U = -A_FRONT_HW + 2.0 * A_FRONT_HW * i / A_COLS
        out += sh.poly(
            [_a_ground(U, A_DEPTH * k / 24.0) for k in range(25)], BLACK, f=2500
        )
    for j in range(A_ROWS + 1):
        V = A_DEPTH * j / A_ROWS
        for i in range(A_COLS + 1):
            U = -A_FRONT_HW + 2.0 * A_FRONT_HW * i / A_COLS
            out += sh.dot(*_a_ground(U, V), 2.4, BLACK)

    # contour field on the ground, drawn lifted by its own height
    g0 = 1.02 * sh.mm
    slope = 0.048
    peaks = [(U, V, R, h) for U, V, R, h in A_PEAKS]
    pk = [(U, V, R, h / _cusp_profile(0.0, R, g0, slope)) for U, V, R, h in peaks]
    cell = 1.25 * sh.mm
    F, xs, ys = _field(pk, -A_FRONT_HW - 40, -40.0, A_FRONT_HW + 40, A_DEPTH + 40, cell,
                       g0, slope)
    amp_max = max(a for *_, a in pk)
    levels = _nest_levels(F, cell, g0, amp_max)
    circles, switch = _nest_eyes(pk, levels, g0, slope)
    for lv in levels:
        for chain in _chain_segments(_marching_squares(F, xs, ys, lv)):
            if len(chain) < 5 or _too_small(chain, pk, switch):
                continue
            pts = [
                (_a_ground(U, V)[0], _a_ground(U, V)[1] - lv)
                for U, V in _smooth(chain, 3)
            ]
            out += sh.poly(pts, BLACK, f=2300)
    for U, V, r, lv in circles:
        n = max(22, min(90, int(r * 1.6)))
        pts = []
        for k in range(n + 1):
            a = 2.0 * math.pi * k / n
            gx, gy = _a_ground(U + r * math.cos(a), V + r * math.sin(a))
            pts.append((gx, gy - lv))
        out += sh.poly(pts, BLACK, f=2300)

    # apex needles
    for U, V, _R, h in A_PEAKS:
        gx, gy = _a_ground(U, V)
        out += sh.poly([(gx, gy - h), (gx, gy - h - 16.0)], BLACK)
        out += sh.dot(gx, gy - h - 16.0, 2.4, BLACK)
        out += sh.dot(gx, gy - h, 4.2, BLACK)
    return out


# ---------------------------------------------------------------------------
# Z = AV — the stacked wave landscape
# ---------------------------------------------------------------------------

Z_L, Z_R = 118.0, 666.0
Z_YL, Z_YR = 1314.0, 1273.0
Z_PEAK_X = 382.0


def _z_bump(x: float, c: float, w: float) -> float:
    return math.exp(-((x - c) / w) ** 2)


def _z_main(x: float) -> float:
    """The single tall central peak, normalised to 1."""
    return _z_bump(x, Z_PEAK_X, 46.0)


def _z_lobes(x: float) -> float:
    """The surrounding wave landscape, normalised to ~1 at its tallest lobe."""
    return (
        1.00 * _z_bump(x, 219.0, 44.0)
        + 0.94 * _z_bump(x, 535.0, 44.0)
        + 0.46 * _z_bump(x, 156.0, 27.0)
        + 0.40 * _z_bump(x, 628.0, 29.0)
        + 0.20 * _z_bump(x, 300.0, 30.0)
        + 0.19 * _z_bump(x, 458.0, 30.0)
    )


def _z_y(x: float, a: float) -> float:
    """y of the profile whose amplitude fraction is ``a``, at abscissa ``x``."""
    t = (x - Z_L) / (Z_R - Z_L)
    base = Z_YL + (Z_YR - Z_YL) * t
    taper = math.sin(math.pi * max(0.0, min(1.0, t))) ** 0.45
    return base - taper * a * (40.0 + 78.0 * _z_main(x) + 58.0 * _z_lobes(x))


def _z_stack(sh: _Sheet) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    # The peak and the side lobes get SEPARATE amplitude ramps.  With one ramp
    # the lobes of neighbouring profiles land within a pen width of each other
    # and the left half of the landscape fills in solid; ramping them apart
    # keeps every profile readable at ~0.8 mm, which is the whole point of the
    # stack.
    # ``amp_floor`` is what keeps the stack readable in the VALLEYS.  Scale
    # the shape alone and every profile collapses onto the base line wherever
    # the landscape is flat -- 0.2 mm apart, a solid green bar.  A constant
    # per-profile lift (tapering to nothing at the two anchors, where the
    # plate does converge them) holds ~0.65 mm there, which is what the
    # reference itself runs.
    n = 15
    amp_top, amp_lobe, amp_floor = 78.0, 58.0, 40.0
    steps = 210
    for k in range(n):
        u = k / (n - 1.0)
        a = -0.45 + 1.45 * u                    # the lower third mirrors below the base
        pts: List[Pt] = []
        for m in range(steps + 1):
            t = m / steps
            x = Z_L + (Z_R - Z_L) * t
            base = Z_YL + (Z_YR - Z_YL) * t
            taper = math.sin(math.pi * t) ** 0.45
            y = base - taper * a * (
                amp_floor + amp_top * _z_main(x) + amp_lobe * _z_lobes(x)
            )
            pts.append((x, y))
        out += sh.poly(pts, GREEN, f=2200)

    # tails and their terminals
    out += sh.poly([(55.0, Z_YL), (Z_L, Z_YL)], GREEN)
    out += sh.ring(Z_L, Z_YL, 7.0, GREEN, n=36)
    out += sh.poly([(Z_R, Z_YR), (712.0, Z_YR)], GREEN)
    out += sh.ring(Z_R, Z_YR, 7.0, GREEN, n=36)
    out += sh.dot(712.0, Z_YR, 3.4, GREEN)

    # Ring nodes sit ON a profile, never near one: a marker floating a
    # millimetre off the curve it is marking is the collision the house law
    # is about.
    for px, frac in ((219.0, 1.00), (300.0, 0.78), (162.0, 0.62),
                     (535.0, 1.00), (612.0, 0.74), (456.0, 0.58)):
        out += sh.ring(px, _z_y(px, frac), 5.2, GREEN, n=28)

    # central axis with its graduated dot column
    out += sh.poly([(Z_PEAK_X, 1196.0), (Z_PEAK_X, 1403.0)], GREEN)
    for k in range(26):
        t = k / 25.0
        y = 1196.0 + (1396.0 - 1196.0) * t
        r = 2.0 + 3.4 * math.exp(-((t - 0.02) / 0.22) ** 2) + 2.6 * max(0.0, t - 0.86) * 6
        out += sh.dot(Z_PEAK_X, y, min(5.6, r), GREEN)
    out += sh.dot(Z_PEAK_X, 1403.0, 2.2, BLACK)

    # the plate's two big dashed arcs, set behind the landscape
    for cxp, cyp, rr, a0, a1 in ((276.0, 1292.0, 122.0, -145.0, 118.0),
                                 (492.0, 1288.0, 130.0, 55.0, 330.0)):
        arc = [
            (cxp + rr * math.cos(math.radians(a)), cyp + rr * math.sin(math.radians(a)))
            for a in [a0 + (a1 - a0) * k / 160.0 for k in range(161)]
        ]
        for seg in _dashes(arc, 5.0, 7.0):
            if _clear_of_type(seg):
                out += sh.poly(seg, BLACK, f=2500)
    return out


# ---------------------------------------------------------------------------
# furniture
# ---------------------------------------------------------------------------


def _furniture(sh: _Sheet) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []

    # mid-left: two overlapping circles on dashed crosshair rules
    for seg in _dashes([(65.0, 578.0), (268.0, 578.0)], 7.0, 5.0):
        out += sh.poly(seg, BLACK)
    for seg in _dashes([(159.0, 468.0), (159.0, 685.0)], 7.0, 5.0):
        out += sh.poly(seg, BLACK)
    out += sh.ring(159.0, 566.0, 45.0, BLACK)
    out += sh.ring(159.0, 601.0, 45.0, BLACK)

    # mid-right: dot lattice + a crosshair circle
    for j in range(4):
        for i in range(4):
            if (i, j) in ((3, 3),):
                continue
            out += sh.dot(814.0 + i * 21.0, 540.0 + j * 25.0, 2.1, BLACK)
    out += sh.ring(956.0, 566.0, 36.0, BLACK)
    for seg in _dashes([(895.0, 566.0), (1016.0, 566.0)], 8.0, 5.0):
        out += sh.poly(seg, BLACK)
    for seg in _dashes([(956.0, 492.0), (956.0, 639.0)], 8.0, 5.0):
        out += sh.poly(seg, BLACK)

    # upper-right of A: a stack of five profile lines + a dot column
    for k in range(6):
        y = 742.0 + k * 21.5
        amp = 40.0 * (1.0 - k / 5.5) ** 1.5
        pts = [
            (862.0 + 150.0 * m / 60.0,
             y - amp * math.exp(-((862.0 + 150.0 * m / 60.0 - 941.0) / 15.0) ** 2))
            for m in range(61)
        ]
        out += sh.poly(pts, BLACK, f=2400)
    for k in range(7):
        out += sh.dot(836.0, 762.0 + k * 13.6, 1.5 + 0.22 * k, BLACK)

    # lower-left: graduated dot rule, and a small ringed axis
    out += sh.poly([(112.0, 1003.0), (160.0, 1003.0)], BLACK)
    for k, r in enumerate((3.4, 3.3, 3.1, 2.6, 1.9, 1.3)):
        out += sh.dot(165.0 + k * 16.0, 1003.0, r, BLACK)
    out += sh.poly([(83.0, 989.0), (83.0, 1089.0)], BLACK)
    out += sh.ring(83.0, 1050.0, 17.0, BLACK, n=40)

    # lower-right: three shrinking circles on a dash-dot rule, plus a dot rule
    for cxp, r in ((903.0, 21.0), (939.0, 18.5), (966.0, 15.5)):
        out += sh.ring(cxp, 1328.0, r, BLACK, n=56)
    for seg in _dashes([(923.0, 1326.0), (1033.0, 1326.0)], 13.0, 7.0):
        out += sh.poly(seg, BLACK)
    out += sh.poly([(952.0, 1318.0), (952.0, 1334.0)], BLACK)
    out += sh.poly([(794.0, 1368.0), (957.0, 1368.0)], BLACK)
    for px, r in ((794.0, 3.4), (915.0, 2.8), (957.0, 1.4)):
        out += sh.dot(px, 1368.0, r, BLACK)
    return out


# ---------------------------------------------------------------------------
# type
# ---------------------------------------------------------------------------


def _shape_label(sh: _Sheet, s: str, px: float, py: float, pen: int = BLACK):
    """A '(n x d)' shape annotation, left baseline at (px, py).

    Cap height is set from the MEASURED footprint on the plate (54 px wide,
    14 px tall), not from how big it looks: this font is wider per cap than
    the reference's, so matching the height alone overruns by ~40%.
    """
    return sh.text(s, px, py, 12.2, pen)


def _labels(sh: _Sheet) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    out += sh.text("Q", 93.0, 121.0, 33.0, RED)
    out += sh.text("K", 958.0, 132.0, 32.0, BLUE)
    out += sh.text("A", 274.0, 847.0, 32.0, BLACK)
    out += sh.text("V", 949.0, 946.0, 32.0, OCHRE)
    out += sh.text("Z = AV", 151.0, 1186.0, 24.0, GREEN)

    out += _shape_label(sh, "(n x d)", 49.0, 346.0)
    out += _shape_label(sh, "(n x d)", 975.0, 361.0)
    out += _shape_label(sh, "(n x n)", 707.0, 693.0)
    out += _shape_label(sh, "(n x n)", 249.0, 880.0)
    out += _shape_label(sh, "(n x d)", 986.0, 1119.0)
    out += _shape_label(sh, "(n x d)", 160.0, 1218.0)

    # Q . K^T  -- the plate's one composite label: 77 px wide, 33 px cap.
    out += sh.text("Q", 505.0, 452.0, 28.0, BLACK)
    out += sh.dot(538.5, 442.0, 2.3, BLACK)
    out += sh.text("K", 543.0, 452.0, 28.0, BLACK)
    out += sh.text("T", 571.5, 439.0, 14.0, BLACK)

    out += sh.text("softmax", 492.0, 755.0, 16.2, BLACK)
    return out


# ---------------------------------------------------------------------------
# piece
# ---------------------------------------------------------------------------


def warped_grid(rng, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    """The plate. ``rng`` is accepted for the studio contract and unused: this
    is an exact recreation, so every position is measured, none is sampled."""
    del rng
    sh = _Sheet(bounds, colors)
    out: List[GCodeCommand] = []

    # ---- Q -----------------------------------------------------------------
    q_nests = [
        (158.0, 220.0, 98.0, 1.00),
        (266.0, 131.0, 70.0, 0.84),
        (397.0, 268.0, 68.0, 0.82),
        (261.0, 325.0, 70.0, 0.84),
    ]
    q_links = [
        [(74.0, 306.0), (150.0, 372.0), (238.0, 408.0), (330.0, 392.0), (416.0, 344.0),
         (502.0, 300.0)],
        [(96.0, 152.0), (180.0, 98.0), (282.0, 72.0), (372.0, 98.0), (432.0, 162.0),
         (472.0, 242.0), (500.0, 330.0)],
        [(112.0, 254.0), (196.0, 236.0), (286.0, 246.0), (368.0, 262.0), (444.0, 268.0),
         (516.0, 240.0)],
        [(122.0, 392.0), (204.0, 348.0), (270.0, 326.0), (344.0, 318.0), (412.0, 300.0),
         (486.0, 266.0)],
        [(268.0, 128.0), (344.0, 122.0), (406.0, 148.0), (454.0, 194.0), (482.0, 254.0),
         (492.0, 322.0)],
        [(78.0, 246.0), (124.0, 178.0), (198.0, 138.0), (272.0, 132.0), (334.0, 154.0),
         (380.0, 200.0)],
        [(214.0, 408.0), (302.0, 402.0), (378.0, 370.0), (434.0, 320.0), (470.0, 260.0)],
        [(140.0, 116.0), (212.0, 86.0), (302.0, 86.0), (378.0, 116.0), (432.0, 166.0)],
    ]
    out += _cluster(
        sh, RED, q_nests, (40.0, 28.0, 560.0, 448.0), q_links,
        fans=((0, (523.0, 398.0), 88.0, 6), (2, (523.0, 398.0), 40.0, 4)),
    )
    out += _arrow(sh, (498.0, 352.0), (525.0, 408.0), RED, head=13.0,
                  ctrl=[(516.0, 380.0)])
    out += _dot_column(sh, 57.0, 180.0, 279.0, 6, 4.6, RED)
    out += sh.poly([(55.0, 297.0), (55.0, 315.0), (87.0, 315.0)], BLACK)
    out += sh.dot(94.0, 315.0, 2.0, BLACK)

    # ---- K -----------------------------------------------------------------
    k_nests = [
        (694.0, 220.0, 94.0, 1.00),
        (807.0, 143.0, 68.0, 0.84),
        (908.0, 268.0, 86.0, 0.94),
        (824.0, 366.0, 68.0, 0.84),
    ]
    k_links = [
        [(588.0, 254.0), (650.0, 318.0), (730.0, 346.0), (812.0, 332.0), (886.0, 300.0),
         (948.0, 254.0)],
        [(590.0, 206.0), (664.0, 160.0), (748.0, 144.0), (826.0, 168.0), (886.0, 218.0),
         (936.0, 288.0)],
        [(608.0, 300.0), (684.0, 262.0), (762.0, 256.0), (840.0, 276.0), (912.0, 266.0),
         (956.0, 226.0)],
        [(730.0, 92.0), (812.0, 70.0), (888.0, 104.0), (930.0, 176.0), (940.0, 248.0),
         (918.0, 328.0)],
        [(630.0, 348.0), (706.0, 394.0), (790.0, 410.0), (862.0, 382.0), (912.0, 330.0)],
        [(684.0, 296.0), (756.0, 326.0), (818.0, 364.0), (868.0, 410.0)],
        [(618.0, 156.0), (682.0, 108.0), (756.0, 100.0), (818.0, 132.0), (860.0, 184.0)],
        [(700.0, 428.0), (782.0, 434.0), (856.0, 410.0), (908.0, 358.0)],
    ]
    out += _cluster(
        sh, BLUE, k_nests, (540.0, 28.0, 1010.0, 470.0), k_links,
        fans=((0, (568.0, 400.0), 74.0, 6), (2, (700.0, 330.0), 46.0, 4)),
    )
    out += _arrow(sh, (600.0, 350.0), (566.0, 408.0), BLUE, head=13.0,
                  ctrl=[(572.0, 382.0)])
    out += _dot_column(sh, 1024.0, 180.0, 279.0, 6, 4.6, BLUE)
    out += _bracket(sh, 995.0, 175.0, 335.0, +1, BLACK, serif=15.0)
    out += sh.ring(681.0, 72.0, 7.0, BLUE, n=32)
    out += sh.poly([(831.0, 446.0), (845.0, 446.0)], BLUE)
    out += sh.poly([(838.0, 439.0), (838.0, 453.0)], BLUE)

    # ---- centre lattice ----------------------------------------------------
    out += _lattice(sh)
    out += _arrow(sh, (542.0, 700.0), (542.0, 729.0), BLACK, head=10.0)
    out += sh.poly([(542.0, 762.0), (542.0, 812.0)], BLACK)
    # the two little grey pointers that lead the eye into the lattice
    out += _arrow(sh, (622.0, 432.0), (700.0, 382.0), BLACK, head=9.0,
                  ctrl=[(652.0, 444.0), (684.0, 424.0)])
    out += _arrow(sh, (700.0, 466.0), (700.0, 404.0), BLACK, head=9.0)

    # ---- A -----------------------------------------------------------------
    out += _a_surface(sh)

    # ---- V -----------------------------------------------------------------
    v_nests = [
        (886.0, 1000.0, 92.0, 1.00),
        (773.0, 1074.0, 74.0, 0.88),
        (856.0, 1138.0, 72.0, 0.86),
    ]
    v_links = [
        [(654.0, 1034.0), (720.0, 1010.0), (792.0, 986.0), (858.0, 970.0), (926.0, 958.0),
         (966.0, 984.0)],
        [(640.0, 1070.0), (710.0, 1056.0), (778.0, 1072.0), (846.0, 1092.0), (918.0, 1074.0),
         (958.0, 1036.0)],
        [(648.0, 1124.0), (724.0, 1136.0), (792.0, 1160.0), (860.0, 1176.0), (930.0, 1152.0),
         (958.0, 1104.0)],
        [(686.0, 1090.0), (760.0, 1110.0), (820.0, 1142.0), (878.0, 1172.0), (938.0, 1178.0)],
        [(894.0, 994.0), (936.0, 1034.0), (950.0, 1090.0), (932.0, 1148.0), (886.0, 1188.0)],
        [(636.0, 1000.0), (700.0, 960.0), (782.0, 942.0), (858.0, 950.0), (924.0, 984.0)],
    ]
    out += _cluster(
        sh, OCHRE, v_nests, (588.0, 884.0, 1002.0, 1236.0), v_links,
        fans=((0, (700.0, 1112.0), 54.0, 6),),
    )
    out += _dot_column(sh, 1016.0, 980.0, 1080.0, 6, 4.6, OCHRE)
    out += _bracket(sh, 985.0, 973.0, 1091.0, +1, BLACK, serif=15.0)

    # ---- V -> A front edge, and A -> Z droplines ---------------------------
    for k in range(5):
        y_v = 1004.0 + k * 40.0
        x_end = 562.0 + k * 5.0
        out += sh.poly(
            _smooth([(846.0, y_v), (742.0, y_v + 6.0), (664.0, y_v - 14.0),
                     (614.0, 996.0 + k * 6.0), (x_end + 8.0, 962.0),
                     (x_end, 946.0)], 10),
            OCHRE, f=2300,
        )
        out += sh.dot(742.0, y_v + 6.0, 4.0, OCHRE)
    out += sh.ring(582.0, 946.0, 4.4, OCHRE, n=24)
    out += sh.ring(544.0, 946.0, 4.4, BLACK, n=24)

    # ---- Z -----------------------------------------------------------------
    out += _z_stack(sh)
    drops = ((503.0, 382.0), (523.0, 398.0), (544.0, 414.0), (562.0, 430.0))
    for x0p, xtip in drops:
        out += sh.poly([(x0p, 946.0), (x0p, 1096.0)], BLACK, f=2400)
        out += _arrow(
            sh, (x0p, 1096.0), (xtip, 1186.0), BLACK, head=10.0,
            ctrl=[(x0p, 1128.0), (xtip, 1158.0)],
        )

    # ---- furniture + type --------------------------------------------------
    out += _furniture(sh)
    out += _labels(sh)
    return out
