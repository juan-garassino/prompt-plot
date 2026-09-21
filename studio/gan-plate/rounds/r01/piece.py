"""GAN plate — exact recreation.

Every position in this file is a measurement taken off
``studio/gan-plate/ref/reference.png`` (1510 x 1041 px) with a pixel probe, not
an eyeball estimate.  ``_P`` maps reference pixels onto the drawable area, so
the whole layout is one affine map away from the raster and can be stacked back
against it.

The plate's core primitive is a LOBED BLOB: a 3-lobed closed outline filled
with concentric rings that follow its own boundary and tighten into a knot at
the centre.  ``_blob`` builds one; every stage of the diagram is a call to it.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.generative.kit import (
    _GLYPHS,
    _dot,
    _glyph_advance,
    _poly,
    _stroke_text,
    circle,
    tone_dots,
)
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

# reference raster size -- every literal below is in these pixels
REF_W, REF_H = 1510.0, 1041.0

RED, BLUE, YEL, OLV, BLK = 0, 1, 2, 3, 4

MIN_SEP = 0.8  # mm -- floor on line spacing for every field/ring/hatch
# A deliberately SOLID mark (a knot, a kernel weight dot, a node) is filled at
# the pen tip instead: one pass, no overlap, and it is the only place on the
# plate where lines sit closer than MIN_SEP. Everything else obeys MIN_SEP.
TIP = 0.5


# ---------------------------------------------------------------------------
# reference-pixel space
# ---------------------------------------------------------------------------


class Ref:
    """Affine map reference-pixel -> sheet millimetres."""

    def __init__(self, bounds: Bounds) -> None:
        x0, y0, x1, y1 = bounds
        self.x0, self.y0, self.x1, self.y1 = bounds
        self.sx = (x1 - x0) / REF_W
        self.sy = (y1 - y0) / REF_H

    def p(self, px: float, py: float) -> Tuple[float, float]:
        return (self.x0 + px * self.sx, self.y1 - py * self.sy)

    def lx(self, px: float) -> float:
        return px * self.sx

    def ly(self, py: float) -> float:
        return py * self.sy


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return min(idx, colors - 1)


# ---------------------------------------------------------------------------
# type -- fitted to the reference's measured ink box, never guessed
# ---------------------------------------------------------------------------


def _spaced(text: str) -> str:
    return " ".join(text)


def _ink_extent(text: str) -> Tuple[float, float, float]:
    """(first ink x, last ink x, total advance) in 4x6 glyph units."""
    cx = 0.0
    lo = hi = None
    for ch in text:
        st = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        for stroke in st:
            for gx, _gy in stroke:
                v = cx + gx
                lo = v if lo is None else min(lo, v)
                hi = v if hi is None else max(hi, v)
        cx += _glyph_advance(ch)
    if lo is None:
        return 0.0, 0.0, cx
    return lo, hi, cx


def _fit_height(text: str, width_px: float, spaced: bool = True) -> float:
    """Cap height (in reference px) that makes ``text`` exactly ``width_px`` wide.

    Labels on sibling plates kept "looking right" at 30% oversize; fitting the
    measured ink box instead of judging the size removes the whole class of
    error.
    """
    lo, hi, _ = _ink_extent(_spaced(text) if spaced else text)
    span = hi - lo
    if span <= 0:
        return 6.0
    return 6.0 * width_px / span


class Type:
    """Stroke type placed by reference pixel, sized by measured ink width."""

    def __init__(self, ref: Ref) -> None:
        self.ref = ref

    def draw(
        self,
        text: str,
        px: float,
        baseline_py: float,
        h_px: float,
        pen: Optional[int],
        spaced: bool = True,
        f: int = 2400,
    ) -> List[GCodeCommand]:
        s = _spaced(text) if spaced else text
        lo, _hi, _ = _ink_extent(s)
        h_mm = self.ref.ly(h_px)
        sc = h_mm / 6.0
        x_mm, y_mm = self.ref.p(px, baseline_py)
        # pull the leading side bearing off so px really is the first ink column
        return _stroke_text(s, x_mm - lo * sc, y_mm, h_mm, color=pen, f=f, proportional=True)

    def block(
        self,
        lines: Sequence[str],
        px: float,
        first_baseline_py: float,
        pitch_py: float,
        width_px: float,
        pen: Optional[int],
        spaced: bool = True,
    ) -> List[GCodeCommand]:
        """A left-aligned stack sized from its WIDEST line's measured width."""
        widest = max(lines, key=lambda s: _ink_extent(_spaced(s) if spaced else s)[1])
        h = _fit_height(widest, width_px, spaced)
        out: List[GCodeCommand] = []
        for i, ln in enumerate(lines):
            out += self.draw(ln, px, first_baseline_py + i * pitch_py, h, pen, spaced)
        return out

    def width_px(self, text: str, h_px: float, spaced: bool = True) -> float:
        lo, hi, _ = _ink_extent(_spaced(text) if spaced else text)
        return (hi - lo) * h_px / 6.0


# ---------------------------------------------------------------------------
# THE LOBED BLOB
# ---------------------------------------------------------------------------


def _lobe_factor(th: float, harm: Sequence[Tuple[int, float, float]]) -> float:
    v = 1.0
    for k, amp, ph in harm:
        v += amp * math.cos(k * th + ph)
    return max(0.22, v)


def _blob_harmonics(rng, lobes: int = 3, upright: bool = False) -> List[Tuple[int, float, float]]:
    """A three-lobed organic outline: one dominant harmonic plus wobble.

    ``upright`` is kept only for callers that want the old behaviour; the plate
    uses the measured arrangement instead (see below).
    """
    # Never let a lobe point straight up or straight down. Under the 2:1
    # vertical stretch a lobe on the vertical axis is drawn out into a blade,
    # which is exactly what the first three rounds produced; on the reference
    # every blob sits in one of two mirrored arrangements -- lobes at 0/120/240
    # or at 60/180/300 -- so one lobe always runs horizontally and stays
    # compact under the stretch.
    phi = (0.0 if rng.random() < 0.5 else math.pi / 3.0) + (rng.random() - 0.5) * 0.55
    return [
        (lobes, 0.235 + 0.05 * rng.random(), phi),
        (2, 0.055 + 0.035 * rng.random(), rng.random() * 2 * math.pi),
        (5, 0.022 + 0.018 * rng.random(), rng.random() * 2 * math.pi),
    ]


def _extent(harm, rx: float, ry: float, n: int = 240) -> Tuple[float, float]:
    """Half-extents (x, y) the outline actually reaches, for collision control."""
    mx = my = 0.0
    for k in range(n):
        th = 2 * math.pi * k / n
        s = _lobe_factor(th, harm)
        mx = max(mx, abs(s * rx * math.cos(th)))
        my = max(my, abs(s * ry * math.sin(th)))
    return mx, my


def _dash_polyline(
    pts: Sequence[Tuple[float, float]],
    dash: float,
    gap: float,
    phase: float,
    pen: Optional[int],
    f: int = 2400,
) -> List[GCodeCommand]:
    """Walk a polyline by arc length, emitting dashes. Phase shifts the pattern.

    Rotating the phase ring by ring is what turns a nest of contours into the
    reference's woven/beaded texture instead of a solid flood -- and it halves
    the ink.
    """
    out: List[GCodeCommand] = []
    period = dash + gap
    s = phase % period
    run: List[Tuple[float, float]] = []
    if s < dash:
        run = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        if seg < 1e-9:
            continue
        t = 0.0
        while t < seg - 1e-9:
            cur = s % period
            if cur < dash:
                step = min(seg - t, dash - cur)
            else:
                step = min(seg - t, period - cur)
            # a zero-length step stalls the walk forever when `cur` lands
            # exactly on a dash boundary; always advance by something.
            step = max(step, 1e-6)
            t2 = min(t + step, seg)
            p2 = (a[0] + (b[0] - a[0]) * t2 / seg, a[1] + (b[1] - a[1]) * t2 / seg)
            if cur < dash:
                if not run:
                    run = [(a[0] + (b[0] - a[0]) * t / seg, a[1] + (b[1] - a[1]) * t / seg)]
                run.append(p2)
            else:
                if len(run) >= 2:
                    out += _poly(run, color=pen, f=f)
                run = []
            s += step
            t = t2
    if len(run) >= 2:
        out += _poly(run, color=pen, f=f)
    return out


def _blob(
    rng,
    cx: float,
    cy: float,
    rx: float,
    ry: float,
    pen: Optional[int],
    *,
    harm: Sequence[Tuple[int, float, float]],
    sigma: float = 0.40,
    n_rings: int = 30,
    pitch: float = MIN_SEP,
    dash: float = 1.15,
    gap: float = 0.7,
    bead_n: int = 28,
    bead_duty: float = 0.72,
    bead_step: float = 0.618,
    core_u: float = 0.26,
    knot_r: float = 0.9,
    spoke_levels: int = 4,
    base_spokes: int = 7,
    outline: bool = True,
    ring_pen: Optional[int] = None,
    n_theta: int = 190,
    f: int = 2400,
) -> List[GCodeCommand]:
    """One lobed blob: outline + boundary-following rings + a converging knot.

    Ring levels come from a CONICAL cusp ``exp(-u/sigma)`` sampled at evenly
    spaced iso-values, so the rings tighten toward the centre and open toward
    the rim (a Gaussian would do the opposite and spread exactly where the knot
    has to be dense).  ``u`` is the NORMALISED radius |P-C| / R(theta), so every
    iso-line is a scaled copy of the outline -- the rings follow the boundary
    by construction.

    Radial spacing is then enforced against ``pitch``: inner rings are dropped
    until every gap clears the pen floor, and the leftover core is carried by a
    polar-LOD spoke fan that doubles outward, so nothing crowds at the cusp.
    """
    ring_pen = pen if ring_pen is None else ring_pen
    bead_ang = 2 * math.pi / bead_n
    ths = [2 * math.pi * k / n_theta for k in range(n_theta + 1)]
    shape = [_lobe_factor(t, harm) for t in ths]

    def pt(u: float, i: int) -> Tuple[float, float]:
        rfac = u * shape[i]
        return (cx + rfac * rx * math.cos(ths[i]), cy + rfac * ry * math.sin(ths[i]))

    # radial distance from the cusp to the outline, per angle (mm)
    radial = [
        math.hypot(shape[i] * rx * math.cos(ths[i]), shape[i] * ry * math.sin(ths[i]))
        for i in range(n_theta + 1)
    ]

    # PERPENDICULAR step per unit of u, per angle.
    #
    # Rings are scaled copies of the outline, so stepping u by du moves each
    # point du*|V| ALONG THE RADIUS -- but two contours are only du*|V . n| apart
    # measured across them. Wherever the boundary runs steeply (every neck), the
    # radius is far from the normal and the true gap is a fraction of the radial
    # one. Gating on the radial step is how a nest that looks correctly spaced
    # floods solid in the necks; this is the same "choose levels by GRADIENT,
    # not by value" rule that `kit.even_contour_levels` exists for, written out
    # for an analytic family of contours.
    perp: List[float] = []
    for i in range(n_theta + 1):
        a, bb = (i - 1) % n_theta, (i + 1) % n_theta
        pa, pb = pt(1.0, a), pt(1.0, bb)
        tx, ty = pb[0] - pa[0], pb[1] - pa[1]
        tl = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / tl, tx / tl
        vx = shape[i] * rx * math.cos(ths[i])
        vy = shape[i] * ry * math.sin(ths[i])
        perp.append(max(1e-6, abs(vx * nx + vy * ny)))

    # --- iso-values of the conical cusp, evenly spaced -> even ring spacing ---
    f_out = math.exp(-1.0 / sigma)
    f_in = math.exp(-0.06 / sigma)
    levels: List[float] = []
    for k in range(n_rings):
        fk = f_out + (f_in - f_out) * (k + 0.5) / n_rings
        levels.append(-sigma * math.log(fk))  # descending u

    out: List[GCodeCommand] = []
    if outline:
        out += _poly([pt(1.0, i) for i in range(n_theta + 1)], color=pen, f=f)

    # --- per-ANGLE spacing, not one global gate ------------------------------
    # Gating a whole ring on the narrowest neck deletes the ring everywhere,
    # which is how twelve ring-filled blobs turn into twelve empty outlines.
    # Instead every angle carries its own last-drawn level: a ring survives on
    # the fat lobes, where there is room, and simply stops existing across the
    # necks, where there is not. Nothing is ever drawn closer than `pitch`.
    last_u = [1.0] * (n_theta + 1)
    for k, u in enumerate(levels):
        if u <= core_u:
            break
        ok = [(last_u[i] - u) * perp[i] >= pitch for i in range(n_theta)]
        if not any(ok):
            continue
        # start the walk at a gap so a ring that wraps 0/2pi is one run, not two
        start = 0
        if all(ok):
            start = 0
        else:
            start = next(i for i in range(n_theta) if not ok[i])
        # Beads are cut by ANGLE, not by arc length: a fixed angular period with
        # a per-ring phase drift is what makes the dashes line up into the
        # reference's radial/spiral weave, and it shortens the beads toward the
        # centre exactly as the raster does instead of over-inking the core.
        run: List[Tuple[float, float]] = []
        ph = k * bead_step * bead_ang
        for j in range(n_theta + 1):
            i = (start + j) % n_theta
            on = ok[i] and j < n_theta and ((ths[i] + ph) % bead_ang) < bead_ang * bead_duty
            if ok[i] and j < n_theta:
                last_u[i] = u
            if on:
                run.append(pt(u, i))
            else:
                if len(run) >= 2:
                    out += _poly(run, color=ring_pen, f=f)
                run = []
        if len(run) >= 2:
            out += _poly(run, color=ring_pen, f=f)
    # --- the core is a polar-LOD GLOW, not more rings ------------------------
    # The reference's knot is not a fill and not a nest: it is a fan of fine
    # lines converging on the cusp, which is the only structure that can get
    # darker and darker toward a point without ever crowding. Level L carries
    # base*2^L spokes and starts at exactly the radius where that many spokes
    # are still `pitch` apart (pitch*n / 2pi), so the angular gap is bounded by
    # construction and the finest levels simply fall off the end of the blob.
    for lvl in range(spoke_levels):
        n = base_spokes * (2**lvl)
        r0 = max(knot_r + pitch * 0.6, pitch * n / (2 * math.pi))
        for j in range(n):
            if lvl > 0 and j % 2 == 0:
                continue  # even indices already drawn by the coarser level
            a = 2 * math.pi * j / n
            idx = int(round(a / (2 * math.pi) * n_theta)) % n_theta
            # Run each spoke out to wherever the rings actually stopped at this
            # angle, not to a fixed core radius. On a fat lobe the rings reach
            # the core and the spoke is short; across a neck the rings ran out
            # early and the spoke carries the whole gap. Spokes are radial and
            # rings are tangential, so the two never crowd each other.
            r1 = radial[idx] * max(core_u, last_u[idx]) - pitch * 0.5
            if r1 - r0 < pitch:
                continue
            ca, sa = math.cos(a), math.sin(a)
            ux, uy = shape[idx] * rx * ca, shape[idx] * ry * sa
            ul = math.hypot(ux, uy) or 1.0
            ux, uy = ux / ul, uy / ul
            out += _poly(
                [(cx + ux * r0, cy + uy * r0), (cx + ux * r1, cy + uy * r1)], color=ring_pen, f=f
            )

    # --- the knot itself: a small tight spiral, the only truly dense ink ------
    turns = max(2, int(round(knot_r / TIP)))
    n = turns * 26
    spiral = []
    for k in range(n + 1):
        t = k / n
        a = 2 * math.pi * turns * t
        rr = knot_r * t
        spiral.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    out += _poly(spiral, color=pen, f=f)
    return out


# ---------------------------------------------------------------------------
# curves
# ---------------------------------------------------------------------------


def _bezier(p0, p1, p2, p3, n: int = 64) -> List[Tuple[float, float]]:
    pts = []
    for k in range(n + 1):
        t = k / n
        m = 1 - t
        x = m**3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t**3 * p3[0]
        y = m**3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def _arc(cx, cy, r, a0, a1, n: int = 90) -> List[Tuple[float, float]]:
    return [
        (cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n))
        for k in range(n + 1)
    ]


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------

# knot centres, measured off the raster (densest-ink probe)
G_KNOTS = [(284, 373), (374, 373), (461, 373), (545, 373), (628, 373)]
G_PENS = [RED, BLK, BLUE, YEL, BLK]
D_KNOTS = [(957, 398), (1041, 397), (1131, 398), (1209, 397), (1305, 398)]
D_PENS = [BLUE, BLK, YEL, BLK, OLV]
XHAT = (737, 388)
REAL = (266, 594)

KERN_X = [177, 281, 385, 490, 594]  # tile left edges, pitch 104.2, width 73
KERN_PEN = [RED, BLK, BLUE, YEL, OLV]


def gan_plate(rng, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    R = Ref(bounds)
    T = Type(R)
    P = R.p
    out: List[GCodeCommand] = []

    red = _pen(RED, colors)
    blue = _pen(BLUE, colors)
    yel = _pen(YEL, colors)
    olv = _pen(OLV, colors)
    blk = _pen(BLK, colors)
    PENS = [red, blue, yel, olv, blk]

    def line(a, b, pen=None, f=2400):
        return _poly([P(*a), P(*b)], color=pen, f=f)

    def dashed(pts_px, pen, dash=5.0, gap=4.0, phase=0.0, f=2400):
        pts = [P(*q) for q in pts_px]
        return _dash_polyline(pts, R.lx(dash), R.lx(gap), R.lx(phase), pen, f=f)

    def plus(px, py, arm, pen):
        return line((px - arm, py), (px + arm, py), pen) + line(
            (px, py - arm), (px, py + arm), pen
        )

    # =====================================================================
    # 1. blobs  (built here, EMITTED after the flow curves so the curves read
    #    as passing behind the stages, the way the reference stacks them)
    #
    # Each blob is sized by the half-extent its OUTLINE actually reaches, not by
    # a nominal radius: the lobe harmonic swings the radius by +-45%, so setting
    # a radius and hoping is exactly how neighbours end up colliding.
    #
    # The row pitch IS the blob width. Measured off the raster, consecutive
    # stages are tangent -- blob 1 ends at x=331, blob 2 begins at x=330 -- so
    # the stages touch at their single widest point and nowhere else. That is
    # the decision: one repeating rhythm, no stage crowding into the next, and
    # no leftover slack either.
    # =====================================================================
    def blob_at(kx, ky, hw_px, hh_px, pen, *, rings=30, sigma=0.40, knot=0.95,
                lv=7, bs=10, upright=False, dash=1.15, gap=0.7, beads=28, core=0.26):
        cx, cy = P(kx, ky)
        harm = _blob_harmonics(rng, upright=upright)
        ex, ey = _extent(harm, 1.0, 1.0)
        return _blob(
            rng,
            cx,
            cy,
            R.lx(hw_px) / ex,
            R.ly(hh_px) / ey,
            pen,
            harm=harm,
            sigma=sigma,
            n_rings=rings,
            knot_r=knot,
            spoke_levels=lv,
            base_spokes=bs,
            dash=dash,
            gap=gap,
            bead_n=beads,
            core_u=core,
            n_theta=260,
        )

    # Measured on the raster: consecutive stages interlock by 4 px (0.7 mm) --
    # blob 1 ends at x=331, blob 2 begins at x=330. One constant, everywhere,
    # so the row reads as a single chain and never as five things that ran out
    # of room. Anything wider than this and the necks would start colliding.
    INTERLOCK_PX = 8.0
    g_hw = min(b[0] - a[0] for a, b in zip(G_KNOTS, G_KNOTS[1:])) / 2.0 + INTERLOCK_PX / 2.0
    d_hw = min(b[0] - a[0] for a, b in zip(D_KNOTS, D_KNOTS[1:])) / 2.0 + INTERLOCK_PX / 2.0

    blobs: List[GCodeCommand] = []
    for (kx, ky), pi in zip(G_KNOTS, G_PENS):
        blobs += blob_at(kx, ky, g_hw, 92, PENS[pi], rings=150)
    for (kx, ky), pi in zip(D_KNOTS, D_PENS):
        blobs += blob_at(kx, ky, d_hw, 92, PENS[pi], rings=150)
    blobs += blob_at(*XHAT, 57, 100, red, rings=170, knot=1.1)
    blobs += blob_at(*REAL, 87, 96, blk, rings=220, sigma=0.36, knot=1.5, lv=8, bs=8,
                     beads=34, core=0.22)

    # =====================================================================
    # 2. latent space: stipple cloud + dot column
    # =====================================================================
    lx0, ly0 = P(17, 461)
    lx1, ly1 = P(133, 335)
    core = P(70, 396)
    sigma_mm = R.lx(21.0)

    def tone(x, y):
        # a CONICAL cusp, same law as the blob rings: exp(-r/sigma) is dense at
        # the point and fades smoothly, where a Gaussian would sit flat across
        # the middle and then fall off a cliff.
        d = math.hypot(x - core[0], y - core[1])
        return min(1.0, 1.55 * math.exp(-d / sigma_mm))

    out += tone_dots(
        (min(lx0, lx1), min(ly0, ly1), max(lx0, lx1), max(ly0, ly1)),
        tone,
        rng,
        pen=blk,
        cell=MIN_SEP,
        jitter=0.6,
        r=0.15,
    )
    # the cusp has its own converging fan, polar-LOD like the blobs: 9 long
    # lines from close in, 18 shorter ones further out, so the core darkens
    # toward the point without ever crowding.
    for lvl, n in ((0, 9), (1, 18)):
        for j in range(n):
            if lvl and j % 2 == 0:
                continue
            a = 2 * math.pi * j / n
            r0 = max(R.lx(3.0), MIN_SEP * n / (2 * math.pi))
            r1 = R.lx(16.0 + 10.0 * rng.random())
            if r1 - r0 < MIN_SEP:
                continue
            out += _poly(
                [
                    (core[0] + r0 * math.cos(a), core[1] + r0 * math.sin(a)),
                    (core[0] + r1 * math.cos(a), core[1] + r1 * math.sin(a)),
                ],
                color=blk,
                f=2400,
            )
    for k in range(7):
        a = math.radians(-26 + 9.0 * k)
        r0, r1 = R.lx(4.0), R.lx(30.0 + 14.0 * rng.random())
        out += _poly(
            [
                (core[0] + r0 * math.cos(a), core[1] + r0 * math.sin(a)),
                (core[0] + r1 * math.cos(a), core[1] + r1 * math.sin(a)),
            ],
            color=blk,
            f=2400,
        )
    out += _fill_dot(core[0], core[1], R.lx(4.0), blk)
    for py in (287, 304.5, 322, 340):
        x, y = P(69, py)
        out += _fill_dot(x, y, 0.62, blk)

    # =====================================================================
    # 3. flow curves
    # =====================================================================
    def flow(a, b, bow, pen, dash=None, tight=0.42):
        """Smooth curve from a to b bowing `bow` px perpendicular at mid-span."""
        dx = b[0] - a[0]
        c1 = (a[0] + dx * tight, a[1] + bow * 0.9)
        c2 = (b[0] - dx * tight, b[1] + bow * 0.9)
        pts = [P(*q) for q in _bezier(a, c1, c2, b, 70)]
        if dash:
            return _dash_polyline(pts, R.lx(dash[0]), R.lx(dash[1]), 0.0, pen)
        return _poly(pts, color=pen, f=2400)

    # latent -> G1
    for i, (bow, pen, dsh) in enumerate(
        [
            (-58, red, (7, 5)),
            (-30, blk, None),
            (-8, blue, (6, 5)),
            (14, blk, None),
            (36, red, (7, 5)),
            (58, blue, (6, 5)),
        ]
    ):
        out += flow((104, 399), G_KNOTS[0], bow, pen, dsh)

    # inside the generator row
    link_bows = [
        [(-40, blk, None), (-16, blue, None), (6, blk, (6, 5)), (26, yel, None), (46, blk, None)],
        [(-44, blue, None), (-18, blk, None), (8, blk, None), (30, yel, (6, 5)), (50, blk, None)],
        [(-38, blk, None), (-12, yel, None), (10, blue, None), (32, blk, None), (52, blk, (5, 4))],
        [(-42, blk, None), (-14, blk, None), (10, yel, None), (30, blue, (6, 5)), (50, blk, None)],
    ]
    for i in range(4):
        for bow, pen, dsh in link_bows[i]:
            out += flow(G_KNOTS[i], G_KNOTS[i + 1], bow, pen, dsh)
    for bow, pen, dsh in [
        (-46, blk, None),
        (-20, blk, None),
        (4, red, None),
        (26, blk, (6, 5)),
        (48, yel, None),
    ]:
        out += flow(G_KNOTS[4], XHAT, bow, pen, dsh)

    # x-hat -> discriminator
    for bow, pen, dsh in [
        (-62, blk, None),
        (-30, red, (7, 5)),
        (-6, blk, None),
        (22, yel, None),
        (48, blk, (6, 5)),
        (74, blk, None),
    ]:
        out += flow(XHAT, D_KNOTS[0], bow, pen, dsh)

    # inside the discriminator row
    dlink = [
        [(-40, blk, None), (-14, blue, None), (8, blk, (6, 5)), (30, yel, None), (50, blk, None)],
        [(-42, blk, None), (-16, yel, None), (6, blk, None), (28, blue, (6, 5)), (48, blk, None)],
        [(-38, blk, None), (-12, blk, None), (10, yel, None), (32, blk, None), (52, blk, (5, 4))],
        [(-40, blk, None), (-14, blk, None), (10, olv, None), (32, blk, (6, 5)), (50, blk, None)],
    ]
    for i in range(4):
        for bow, pen, dsh in dlink[i]:
            out += flow(D_KNOTS[i], D_KNOTS[i + 1], bow, pen, dsh)

    # real data -> discriminator: the long bundle that runs BENEATH the whole
    # generator row before it climbs. The control points are placed low and far
    # right on purpose -- a symmetric bow would cut straight through x-hat.
    def long_flow(bow, lift, pen, dsh=None):
        a, b = REAL, D_KNOTS[0]
        c1 = (a[0] + 250, a[1] + bow)
        c2 = (915 + lift * 0.32, 612 + lift * 0.72)
        pts = [P(*q) for q in _bezier(a, c1, c2, b, 110)]
        if dsh:
            return _dash_polyline(pts, R.lx(dsh[0]), R.lx(dsh[1]), 0.0, pen)
        return _poly(pts, color=pen, f=2400)

    for bow, lift, pen, dsh in [
        (-62, -34, blk, (9, 6)),
        (-44, -26, blk, None),
        (-20, 0, blue, None),
        (2, 26, blk, (7, 6)),
        (24, 52, yel, None),
        (48, 78, blk, None),
        (72, 104, blk, (8, 6)),
    ]:
        out += long_flow(bow, lift, pen, dsh)

    # the stages themselves go down on top of the flow bundle
    out += blobs

    # =====================================================================
    # 4. right edge outputs
    # =====================================================================
    node = (1352, 396)
    out += _poly([P(*q) for q in _bezier(P(*D_KNOTS[4]), P(1330, 397), P(1342, 396), P(*node))],
                 color=blk, f=2400)
    out += _poly(
        [P(*q) for q in _bezier(node, (1385, 392), (1398, 340), (1428, 332))], color=blk, f=2400
    )
    out += _poly(
        [P(*q) for q in _bezier(node, (1385, 402), (1396, 480), (1425, 489))], color=blk, f=2400
    )
    for q, r in ((node, 0.62), ((1428, 332), 0.62), ((1425, 489), 0.62)):
        x, y = P(*q)
        out += _dot(x, y, r=r, color=blk)
    out += line((1432, 366), (1432, 451), blk)

    # =====================================================================
    # 5. type
    # =====================================================================
    # title
    out += T.draw("GAN", 30, 49, _fit_height("GAN", 92), blk)
    out += line((30, 65.5), (68, 65.5), blk)
    out += T.block(["generative", "adversarial", "networks"], 29, 102, 21, 135, blk)
    # upper right
    out += T.block(
        ["adversarial", "learning", "representation", "synthesis"], 1364, 57, 15, 122, blk
    )
    out += line((1365, 121), (1418, 121), blk)

    # stage headings
    h_gen = _fit_height("Generator", 123)
    out += T.draw("Generator", 338, 208, h_gen, blk)
    out += T.draw("G", 489, 208, 17, blk, spaced=False)
    out += T.draw("Discriminator", 995, 208, _fit_height("Discriminator", 179), blk)
    out += T.draw("D", 1201, 208, 17, blk, spaced=False)

    # subtitles with arrows
    def arrow(x0, x1, y, pen, head=4.0):
        c = line((x0, y), (x1, y), pen)
        c += line((x1 - head, y - head * 0.62), (x1, y), pen)
        c += line((x1 - head, y + head * 0.62), (x1, y), pen)
        return c

    def hat(px, py, w, pen):
        return _poly([P(px - w, py), P(px, py - w * 0.85), P(px + w, py)], color=pen, f=2400)

    out += T.draw("z", 385, 241, 11, blk, spaced=False)
    out += arrow(400, 428, 236, blk)
    out += T.draw("x", 440, 241, 11, blk, spaced=False)
    out += hat(445.5, 227, 5.0, blk)

    out += T.draw("x", 1049, 247, 11, blk, spaced=False)
    out += arrow(1066, 1094, 241, blk)
    # [0,1]
    out += _poly([P(1112, 228), P(1107, 228), P(1107, 248), P(1112, 248)], color=blk, f=2400)
    out += T.draw("0,1", 1113, 247, 11, blk, spaced=True)
    out += _poly([P(1156, 228), P(1161, 228), P(1161, 248), P(1156, 248)], color=blk, f=2400)

    # z ~ p(z)
    out += T.draw("z", 33, 276, 21, blk, spaced=False)
    out += T.draw("~", 55, 276, 21, blk, spaced=False)
    out += T.draw("p(z)", 78, 278, 21, blk, spaced=False)
    out += T.draw("latent space", 29, 470, _fit_height("latent space", 110), blk)

    # x ~ p_data(x)
    out += T.draw("x", 24, 586, 21, blk, spaced=False)
    out += T.draw("~", 45, 586, 21, blk, spaced=False)
    out += T.draw("p", 66, 588, 21, blk, spaced=False)
    out += T.draw("data", 79, 592, 11, blk, spaced=False)
    out += T.draw("(x)", 119, 588, 21, blk, spaced=False)
    out += T.draw("real data", 60, 644, _fit_height("real data", 78), blk)

    # generator / discriminator captions
    out += T.block(
        ["nonlinear transformation", "in latent space"], 334, 485, 23, 230, blk
    )
    out += T.draw("nonlinear decision function", 999, 518, _fit_height("nonlinear decision function", 254), blk)

    # x-hat label + caption
    out += T.draw("x", 752, 280, 14, blk, spaced=False)
    out += hat(758, 262, 6.0, blk)
    out += T.block(["generated", "sample"], 712, 495, 23, 80, blk)

    # D(x-hat) / D(x)
    out += T.draw("D(x)", 1438, 318, 16, blk, spaced=False)
    out += hat(1465, 296, 5.0, blk)
    out += T.draw("fake", 1450, 336, _fit_height("fake", 32), blk)
    out += T.draw("D(x)", 1425, 500, 16, blk, spaced=False)
    out += T.draw("real", 1450, 518, _fit_height("real", 31), blk)

    # loss block
    out += _loss_block(R, T, blk)

    # kernels
    out += T.draw("kernels / filters", 178, 736, _fit_height("kernels / filters", 197), blk)
    # The stroke font has no MULTIPLICATION sign, so the caption is set in two
    # runs with the cross drawn into the gap -- a lowercase x standing in for
    # it is the kind of substitution that shows up immediately at plate size.
    h33 = _fit_height("3 x 3 kernels (example set)", 230)
    out += T.draw("3", 302, 954, h33, blk)
    out += T.draw("3 kernels (example set)", 335, 954, h33, blk)
    mx, my = 322.0, 949.0
    d33 = h33 * 0.30
    out += _poly([P(mx - d33, my - d33), P(mx + d33, my + d33)], color=blk, f=2400)
    out += _poly([P(mx - d33, my + d33), P(mx + d33, my - d33)], color=blk, f=2400)

    # bottom rules
    out += T.draw("PEN PLOTTER", 31, 998, _fit_height("PEN PLOTTER", 213), blk)
    out += line((262, 991), (327, 991), blk)
    out += T.block(
        ["local patterns", "hierarchical features", "global structure", "realistic samples"],
        1329,
        913,
        15,
        158,
        blk,
    )

    # =====================================================================
    # 6. kernel tiles
    # =====================================================================
    out += _kernel_tiles(rng, R, PENS)

    # =====================================================================
    # 7. furniture
    # =====================================================================
    out += _furniture(R, blk, dashed, line, plus)
    return out


# ---------------------------------------------------------------------------


def _loss_block(R: Ref, T: Type, blk) -> List[GCodeCommand]:
    """L_D = -[log D(x) + log(1 - D(x-hat))]   /   L_G = - log D(x-hat)."""
    out: List[GCodeCommand] = []
    P = R.p
    H = 13.0
    SUB = 8.0

    def brk(px, py0, py1, right=False, w=5.0):
        d = -w if not right else w
        return _poly(
            [P(px - d, py0), P(px, py0), P(px, py1), P(px - d, py1)], color=blk, f=2400
        )

    # line 1 baseline 611
    y = 611
    out += T.draw("L", 981, y, H, blk, spaced=False)
    out += T.draw("D", 991, y + 4, SUB, blk, spaced=False)
    out += T.draw("=", 1010, y, H, blk, spaced=False)
    out += _poly([P(1030, y - 5), P(1040, y - 5)], color=blk, f=2400)  # minus
    out += brk(1053, y - 12, y + 4)
    out += T.draw("log", 1056, y, H, blk, spaced=False)
    out += T.draw("D(x)", 1084, y, H, blk, spaced=False)
    out += T.draw("+", 1131, y, H, blk, spaced=False)
    out += T.draw("log(1", 1150, y, H, blk, spaced=False)
    out += _poly([P(1198, y - 5), P(1208, y - 5)], color=blk, f=2400)  # minus
    out += T.draw("D(x))", 1215, y, H, blk, spaced=False)
    out += _poly([P(1264, y - 12), P(1269, y - 12), P(1269, y + 4), P(1264, y + 4)],
                 color=blk, f=2400)
    out += _poly([P(1235, y - 18), P(1240, y - 23), P(1245, y - 18)], color=blk, f=2400)  # hat

    # line 2 baseline 655
    y = 655
    out += T.draw("L", 981, y, H, blk, spaced=False)
    out += T.draw("G", 991, y + 4, SUB, blk, spaced=False)
    out += T.draw("=", 1010, y, H, blk, spaced=False)
    out += _poly([P(1031, y - 5), P(1041, y - 5)], color=blk, f=2400)
    out += T.draw("log", 1052, y, H, blk, spaced=False)
    out += T.draw("D(x)", 1081, y, H, blk, spaced=False)
    out += _poly([P(1101, y - 18), P(1106, y - 23), P(1111, y - 18)], color=blk, f=2400)
    return out


def _kernel_tiles(rng, R: Ref, PENS) -> List[GCodeCommand]:
    """Five 3x3 kernel tiles over five mini-blob tiles, measured off the raster."""
    out: List[GCodeCommand] = []
    P = R.p
    W = 73.0
    TOP_Y0, TOP_Y1 = 748.0, 822.0
    BOT_Y0, BOT_Y1 = 831.0, 902.0

    for t, (x0, pi) in enumerate(zip(KERN_X, KERN_PEN)):
        pen = PENS[pi] if len(PENS) > pi else None
        x1 = x0 + W
        # --- top tile: border + 3x3 rule grid + tinted grounds + dots --------
        out += _poly(
            [P(x0, TOP_Y0), P(x1, TOP_Y0), P(x1, TOP_Y1), P(x0, TOP_Y1), P(x0, TOP_Y0)],
            color=PENS[BLK],
            f=2400,
        )
        cw = W / 3.0
        chh = (TOP_Y1 - TOP_Y0) / 3.0
        for k in (1, 2):
            out += _poly([P(x0 + k * cw, TOP_Y0), P(x0 + k * cw, TOP_Y1)], color=PENS[BLK], f=2400)
            out += _poly(
                [P(x0, TOP_Y0 + k * chh), P(x1, TOP_Y0 + k * chh)], color=PENS[BLK], f=2400
            )
        for j in range(3):
            for i in range(3):
                # kernel weight: strong in the middle, decaying outward
                w = math.exp(-((i - 1) ** 2 + (j - 1) ** 2) / 1.7) * (0.62 + 0.38 * rng.random())
                gx0, gy0 = x0 + i * cw + 2.0, TOP_Y0 + j * chh + 2.0
                gx1, gy1 = x0 + (i + 1) * cw - 2.0, TOP_Y0 + (j + 1) * chh - 2.0
                a = P(gx0, gy1)
                b = P(gx1, gy0)
                # ground tint: a sparse even stipple. Tone drives PROBABILITY,
                # never spacing, and it is capped well under 1 so the cell reads
                # as a wash behind the dot rather than competing with it.
                if w > 0.55:
                    out += tone_dots(
                        (a[0], a[1], b[0], b[1]),
                        lambda _x, _y, _w=w: 0.08 + _w * 0.16,
                        rng,
                        pen=pen,
                        cell=MIN_SEP * 1.35,
                        jitter=0.35,
                        r=0.15,
                    )
                cx, cy = P(x0 + (i + 0.5) * cw, TOP_Y0 + (j + 0.5) * chh)
                out += _fill_dot(cx, cy, R.lx(2.1 + 3.4 * w), pen)
        # --- bottom tile: border + a mini blob ------------------------------
        out += _poly(
            [P(x0, BOT_Y0), P(x1, BOT_Y0), P(x1, BOT_Y1), P(x0, BOT_Y1), P(x0, BOT_Y0)],
            color=PENS[BLK],
            f=2400,
        )
        cx, cy = P(x0 + W / 2.0, (BOT_Y0 + BOT_Y1) / 2.0)
        harm = _blob_harmonics(rng)
        ex, ey = _extent(harm, 1.0, 1.0)
        out += _blob(
            rng,
            cx,
            cy,
            R.lx(27.0) / ex,
            R.ly(26.0) / ey,
            pen,
            harm=harm,
            sigma=0.40,
            n_rings=130,
            knot_r=0.5,
            spoke_levels=4,
            base_spokes=6,
            core_u=0.24,
            dash=0.9,
            gap=0.6,
            n_theta=150,
        )
        dx, dy = P(x0 + W / 2.0, 917.0)
        out += _fill_dot(dx, dy, 0.62, PENS[BLK])
    return out


def _fill_dot(cx: float, cy: float, r: float, pen) -> List[GCodeCommand]:
    """A solid dot: one short spiral, capped so it cannot pool."""
    if r < 0.32:
        return circle(cx, cy, max(0.16, r), pen=pen, n=8)
    turns = max(1, int(round(r / TIP)))
    n = turns * 26
    pts = []
    for k in range(n + 1):
        t = k / n
        a = 2 * math.pi * turns * t
        rr = r * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _poly(pts, color=pen, f=2400)


def _furniture(R: Ref, blk, dashed, line, plus) -> List[GCodeCommand]:
    """Plus marks, rules, dashed arcs, the open square, isolated dots."""
    out: List[GCodeCommand] = []
    P = R.p

    # dashed quarter arcs (circle fits from the raster)
    for cx, cy, r, a0, a1 in [
        (404, 147, 110, 180, 0),
        (898, 145, 80, 108, -6),
        (1187, 250, 116, 46, 3),
        (880, 839, 127, 100, 17),
        (1414, 703, 118, 144, 98),
    ]:
        pts = [
            (cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / 120)),
             cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / 120)))
            for k in range(121)
        ]
        out += dashed(pts, blk, dash=7.0, gap=6.0)

    # vertical rules (solid and dashed)
    out += line((556, 93), (556, 183), blk)
    out += line((1432, 366), (1432, 451), blk)
    out += line((33, 704), (33, 790), blk)
    out += line((29, 744), (117, 744), blk)
    for px, py0, py1 in [
        (242, 209, 325),
        (353, 266, 317),
        (431, 268, 315),
        (509, 281, 312),
        (648, 236, 287),
        (662, 463, 550),
        (827, 236, 342),
        (827, 414, 668),
        (931, 512, 675),
        (1250, 209, 382),
        (1303, 237, 307),
        (1477, 534, 765),
        (952, 285, 316),
        (1019, 295, 329),
        (1095, 285, 335),
        (1173, 291, 334),
    ]:
        out += dashed([(px, py0), (px, py1)], blk, dash=5.0, gap=5.0)

    # dotted horizontal rules
    for py, px0, px1 in [(149, 470, 557), (151, 968, 1147), (366, 1250, 1296), (751, 1056, 1219)]:
        out += dashed([(px0, py), (px1, py)], blk, dash=2.0, gap=5.0)

    # plus marks
    out += plus(657, 88, 25, blk)
    out += plus(693, 675, 16, blk)
    out += plus(994, 961, 44, blk)

    # open square
    out += _poly(
        [P(1419, 184), P(1442, 184), P(1442, 209), P(1419, 209), P(1419, 184)], color=blk, f=2400
    )

    # diagonal tick with a terminal dot, upper left
    out += line((211, 180), (250, 134), blk)
    x, y = P(210, 181)
    out += _dot(x, y, r=0.72, color=blk)

    # isolated dots of several sizes
    for px, py, r in [
        (753, 97, 0.72),
        (171, 597, 0.62),
        (199, 611, 0.45),
        (88, 894, 0.62),
        (1306, 726, 0.62),
        (1438, 838, 0.55),
        (755, 947, 0.62),
        (214, 786, 0.45),
        (190, 786, 0.45),
    ]:
        x, y = P(px, py)
        out += _dot(x, y, r=r, color=blk)
    return out
