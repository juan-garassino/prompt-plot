"""The FORM vocabulary — the closed shapes technical plates are built from.

``material`` says how a mark is made on a surface; this says what the surfaces
ARE. The minimalist infographic idiom (GAN plate, latent-diffusion topography,
the science posters) is almost entirely four families:

* **rings** — a closed outline: lobed blob, hourglass, funnel, rounded rect.
* **nests** — that ring offset inward N times (``contour_nest``). This single op
  is what makes a blob read as a topographic mass, a funnel as a horn of
  contours, an hourglass as the U-Net butterfly.
* **dissolves** — a nest losing coherence: solid rings → broken rings → dotted
  rings → a scatter with no ring structure left. One parameter ``t`` walks it,
  which is exactly a diffusion forward process.
* **bursts / clouds** — radial rays and dot fields for latent spaces and samples.

Everything returns plain polylines in caller units, so a dot is just a very
short stroke — one type all the way through, and the compiler handles pens.
Rings are returned OPEN (first point not repeated); pass through ``close_ring``
when you want to draw the outline itself.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from .geometry import (
    EPS,
    Point,
    Poly,
    Region,
    erode_ring,
    polyline_length,
    resample_by_arclength,
    smooth_ring,
)
from .material import cut_tone

TAU = 2.0 * math.pi


def close_ring(ring: Sequence[Point]) -> Poly:
    """A ring as a drawable closed polyline (first point repeated at the end)."""
    pts = [tuple(p) for p in ring]
    if pts and pts[0] != pts[-1]:
        pts.append(pts[0])
    return pts


# --------------------------------------------------------------------------- #
# rings                                                                       #
# --------------------------------------------------------------------------- #


def lobed_ring(
    cx: float,
    cy: float,
    r: float,
    *,
    lobes: int = 4,
    amp: float = 0.34,
    phase: float = 0.0,
    squash: float = 1.0,
    wobble: float = 0.0,
    rng=None,
    n: int = 240,
) -> Poly:
    """A closed lobed blob: ``r(θ) = r·(1 + amp·cos(lobes·θ + phase))``.

    The clover/cross silhouette the plates use for a data distribution or a
    latent. ``squash`` scales y (an ellipse-ish blob), ``wobble`` adds a seeded
    low-frequency irregularity so two blobs of the same family are not clones.
    """
    w1 = w2 = 0.0
    p1 = p2 = 0.0
    if wobble and rng is not None:
        w1, w2 = wobble * rng.random(), wobble * 0.6 * rng.random()
        p1, p2 = rng.random() * TAU, rng.random() * TAU
    out: Poly = []
    for k in range(n):
        a = TAU * k / n
        rad = r * (1.0 + amp * math.cos(lobes * a + phase))
        if w1 or w2:
            rad *= 1.0 + w1 * math.cos(3 * a + p1) + w2 * math.cos(5 * a + p2)
        out.append((cx + rad * math.cos(a), cy + rad * math.sin(a) * squash))
    return out


def hourglass_ring(
    cx: float,
    cy: float,
    w: float,
    h: float,
    waist: float,
    *,
    power: float = 2.0,
    n: int = 200,
) -> Poly:
    """A bowtie/hourglass outline: full height ``h`` at the ends, pinched to
    ``waist`` at the centre, over width ``w``. ``power`` shapes the pinch (2 =
    parabolic; higher = a sharper throat). This nested is the U-Net butterfly."""
    half_w, half_h, half_waist = w / 2.0, h / 2.0, waist / 2.0

    def edge(x: float) -> float:
        u = min(1.0, abs(x) / max(half_w, EPS))
        return half_waist + (half_h - half_waist) * (u**power)

    m = max(8, n // 2)
    top = [(cx - half_w + w * k / m, cy + edge(-half_w + w * k / m)) for k in range(m + 1)]
    # the mirrored edge, right→left. Its ends are the OPPOSITE corners of the
    # top edge's ends, not duplicates — keep them or the ring loses both ends.
    bot = [(x, cy - (y - cy)) for x, y in reversed(top)]
    return top + bot


def funnel_ring(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    h0: float,
    h1: float,
    *,
    bow: float = 0.18,
    n: int = 120,
) -> Poly:
    """A horn/funnel: height ``h0`` at the mouth ``(x0,y0)`` narrowing to ``h1``
    at ``(x1,y1)``, with ``bow`` curving the sides outward. The encoder /
    decoder / conditioning towers are this nested."""
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux

    def side(t: float, sign: float) -> Point:
        px, py = x0 + dx * t, y0 + dy * t
        half = ((h0 + (h1 - h0) * t) / 2.0) * (1.0 + bow * math.sin(math.pi * t))
        return (px + sign * nx * half, py + sign * ny * half)

    top = [side(k / n, +1.0) for k in range(n + 1)]
    bot = [side(1.0 - k / n, -1.0) for k in range(n + 1)]  # both ends kept
    return top + bot


def rounded_rect_ring(x0: float, y0: float, x1: float, y1: float, r: float = 0.0, n: int = 8) -> Poly:
    """Panel frame, optionally with rounded corners."""
    if r <= 0:
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    r = min(r, (x1 - x0) / 2.0, (y1 - y0) / 2.0)
    out: Poly = []
    for cx, cy, a0 in (
        (x1 - r, y0 + r, -math.pi / 2),
        (x1 - r, y1 - r, 0.0),
        (x0 + r, y1 - r, math.pi / 2),
        (x0 + r, y0 + r, math.pi),
    ):
        for k in range(n + 1):
            a = a0 + (math.pi / 2) * k / n
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


# --------------------------------------------------------------------------- #
# nests                                                                       #
# --------------------------------------------------------------------------- #


def contour_nest(
    ring: Sequence[Point],
    n: int = 16,
    *,
    step: Optional[float] = None,
    inner: float = 0.85,
    min_len: float = 1.0,
) -> List[Poly]:
    """``n`` nested inward offsets of a closed ring — the workhorse.

    Give ``step`` (mm between contours) for a true topographic spacing, or leave
    it and ``inner`` sets how far in the innermost ring sits as a fraction of the
    shape's inradius estimate. Rings that collapse are dropped, so a lobed blob
    nests down to its core without producing knots.
    """
    base = [tuple(p) for p in ring]
    if len(base) < 3 or n < 1:
        return []
    smooth_probe = _is_smooth(base)
    if step is None:
        # How far can THIS shape actually be eroded? Not half its bbox, and not
        # even its inradius: a clover's valleys are concave with a small radius
        # of curvature, so they fold long before the lobes close. Measure it.
        step = (max_erode(base, smooth=smooth_probe) * inner) / max(n, 1)
    # A densely sampled curve (blob, funnel, hourglass) has no true corners, so a
    # miter join only amplifies sampling noise into spikes and offsetting past the
    # inner curvature makes folds. A cornered polygon (panel, facet) needs the
    # miter to keep its edges parallel. Decide from the geometry, not the caller.
    smooth = smooth_probe
    base_sign = 1.0 if _signed_area(base) > 0 else -1.0
    min_area = abs(_signed_area(base)) * 0.02
    out: List[Poly] = []
    for k in range(n):
        d = step * k
        r = base if d <= 0 else _eroded(base, d, smooth)
        # stop once the ring has collapsed or turned itself inside out
        if k and not _valid(r, base_sign, min_area):
            break
        if len(r) < 3:
            break
        closed = close_ring(r)
        if polyline_length(closed) < min_len:
            break
        # A ring INSIDE another cannot be longer than it. When the perimeter
        # starts growing, the offset has begun folding faster than pruning can
        # clean up and the rings would read as spikes — stop while it is honest.
        if out and polyline_length(closed) > polyline_length(out[-1]) * 1.02:
            break
        out.append(closed)
    return out


def radial_nest(
    ring: Sequence[Point],
    n: int = 16,
    *,
    inner: float = 0.10,
    centre: Optional[Point] = None,
    gamma: float = 1.0,
) -> List[Poly]:
    """``n`` self-similar contours scaled toward the shape's centre.

    The other nesting rule. ``contour_nest`` keeps a CONSTANT GAP between rings —
    right for a funnel or a panel, and what a topographic map means — but a
    concave outline can only be offset as far as its tightest valley, so a deep
    clover's rings all pile into a thin band near the rim and leave the middle
    hollow. Scaling about the centroid instead nests any star-shaped form all the
    way down, never folds, and is what a nested-blob mass actually looks like.

    ``gamma`` > 1 bunches the contours toward the rim, < 1 toward the centre.
    """
    base = [tuple(p) for p in ring]
    if len(base) < 3 or n < 1:
        return []
    if centre is None:
        cx = sum(p[0] for p in base) / len(base)
        cy = sum(p[1] for p in base) / len(base)
    else:
        cx, cy = centre
    out: List[Poly] = []
    for k in range(n):
        u = k / max(n - 1, 1)
        s = 1.0 - (1.0 - inner) * (u**gamma)
        out.append(close_ring([(cx + (x - cx) * s, cy + (y - cy) * s) for x, y in base]))
    return out


def _eroded(ring: Sequence[Point], d: float, smooth: bool, passes: int = 2) -> List[Point]:
    r = erode_ring(ring, d, miter=not smooth, prune_folds=smooth)
    return smooth_ring(r, passes=passes) if smooth else r


def _valid(ring: Sequence[Point], base_sign: float, min_area: float) -> bool:
    if len(ring) < 3:
        return False
    a = _signed_area(ring)
    return abs(a) >= min_area and (1.0 if a > 0 else -1.0) == base_sign


def max_erode(ring: Sequence[Point], *, smooth: Optional[bool] = None, iters: int = 14) -> float:
    """The largest inward offset this ring survives, by bisection.

    A concave region collapses at its tightest inner curvature, which no closed
    form gives you for an arbitrary authored outline — so probe it. Used to size
    a nest's step so every requested contour actually exists.
    """
    base = [tuple(p) for p in ring]
    if len(base) < 3:
        return 0.0
    if smooth is None:
        smooth = _is_smooth(base)
    base_sign = 1.0 if _signed_area(base) > 0 else -1.0
    min_area = abs(_signed_area(base)) * 0.02
    base_len = polyline_length(close_ring(base))
    xs = [p[0] for p in base]
    ys = [p[1] for p in base]
    hi = max(max(xs) - min(xs), max(ys) - min(ys))  # certainly too far
    lo = 0.0

    def ok(d: float) -> bool:
        r = _eroded(base, d, smooth)
        # valid AND still shorter than the source: a perimeter that has grown
        # back past the original is folding, not shrinking
        return _valid(r, base_sign, min_area) and polyline_length(close_ring(r)) <= base_len

    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if ok(mid):
            lo = mid
        else:
            hi = mid
    return lo


def _signed_area(ring: Sequence[Point]) -> float:
    a = 0.0
    n = len(ring)
    for i in range(n):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def _is_smooth(ring: Sequence[Point], corner_deg: float = 35.0) -> bool:
    """True when no vertex turns more than ``corner_deg`` — i.e. this is a
    sampled curve rather than a polygon with real corners."""
    pts = list(ring)
    n = len(pts)
    if n < 12:
        return False
    lim = math.cos(math.radians(180.0 - corner_deg))
    for i in range(n):
        ax, ay = pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]
        bx, by = pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1]
        la, lb = math.hypot(ax, ay), math.hypot(bx, by)
        if la < EPS or lb < EPS:
            continue
        if (ax * bx + ay * by) / (la * lb) < lim:
            return False
    return True


def _self_crossing(ring: Sequence[Point], sample: int = 48) -> bool:
    """Cheap fold detector: an eroded ring whose winding has collapsed."""
    pts = list(ring)
    if len(pts) < 8:
        return True
    step = max(1, len(pts) // sample)
    p = pts[::step]
    area = 0.0
    for a, b in zip(p, p[1:] + p[:1]):
        area += a[0] * b[1] - b[0] * a[1]
    return abs(area) < 1e-6


# --------------------------------------------------------------------------- #
# dissolve — a nest losing coherence                                          #
# --------------------------------------------------------------------------- #


def dissolve(
    nest: Sequence[Poly],
    t: float,
    rng,
    *,
    period: float = 5.0,
    scatter: float = 0.0,
    dot: float = 0.35,
    keep_outer: bool = False,
) -> List[Poly]:
    """A nest at ``t`` ∈ [0,1] of its way from solid contours to pure noise.

    ``t=0`` returns the nest untouched. Rising ``t`` first breaks each contour
    into dashes (via ``cut_tone``, so the breaks are real gaps at real spacing),
    then shortens them toward dots, then displaces them outward by ``scatter``
    until no ring structure survives. This is the diffusion forward process as a
    drawing op — and it is why ``x_T`` reads as isotropic rather than as a
    faded blob: by then every mark is a ``dot``-long stroke at a random angle.
    """
    t = max(0.0, min(1.0, t))
    if t <= EPS:
        return [list(p) for p in nest]
    out: List[Poly] = []
    tone = 1.0 - 0.92 * t  # 1 → solid, ~0.08 → almost nothing survives cut_tone
    for i, ring in enumerate(nest):
        if keep_outer and i == 0 and t < 0.75:
            out.append(list(ring))
            continue
        pieces = cut_tone(list(ring), tone, period=period, phase=rng.random() * period, min_len=dot * 0.8)
        for piece in pieces:
            if t > 0.45:  # past halfway, dashes shrink to dots
                shrink = (t - 0.45) / 0.55
                L = polyline_length(piece)
                target = L * (1.0 - shrink) + dot * shrink
                if target < L - EPS:
                    piece = resample_by_arclength(piece, n=max(2, int(target / dot) + 1))
                    piece = piece[: max(2, int(len(piece) * (target / max(L, EPS))) + 1)]
            if scatter > 0:
                a = rng.random() * TAU
                d = scatter * t * math.sqrt(rng.random())
                ox, oy = d * math.cos(a), d * math.sin(a)
                piece = [(x + ox, y + oy) for x, y in piece]
            if len(piece) >= 2:
                out.append(piece)
    return out


def dot_cloud(
    cx: float,
    cy: float,
    r: float,
    count: int,
    rng,
    *,
    dot: float = 0.35,
    falloff: float = 1.0,
    squash: float = 1.0,
) -> List[Poly]:
    """An isotropic scatter of dot-length strokes — a latent space, or the
    ``z_T`` end of a dissolve. ``falloff`` 0 = uniform disc, 1 = concentrated at
    the centre. Each dot is a short stroke at a random angle, so the field has no
    direction of its own."""
    out: List[Poly] = []
    for _ in range(count):
        a = rng.random() * TAU
        u = rng.random()
        rad = r * (u ** (0.5 + falloff))
        x, y = cx + rad * math.cos(a), cy + rad * math.sin(a) * squash
        th = rng.random() * TAU
        out.append([(x, y), (x + dot * math.cos(th), y + dot * math.sin(th))])
    return out


def radial_burst(
    cx: float,
    cy: float,
    r: float,
    rays: int,
    rng,
    *,
    inner: float = 0.06,
    dashed: bool = True,
    dash: float = 1.2,
    gap: float = 1.0,
    jitter: float = 0.12,
    region: Optional[Region] = None,
) -> List[Poly]:
    """Rays from a hot centre — the conv/feature panels and sample tiles.

    ``dashed`` breaks each ray into dashes that lengthen outward, which is what
    makes the centre read as dense and the rim as sparse without changing the ray
    count. ``region`` clips to a panel."""
    from .geometry import clip

    out: List[Poly] = []
    for k in range(rays):
        a = TAU * k / rays + (rng.random() - 0.5) * jitter * TAU / max(rays, 1)
        ux, uy = math.cos(a), math.sin(a)
        r0 = r * inner
        if not dashed:
            seg = [(cx + ux * r0, cy + uy * r0), (cx + ux * r, cy + uy * r)]
            out.extend(clip(seg, region, keep="inside") if region is not None else [seg])
            continue
        d = r0
        while d < r:
            grow = 0.4 + 1.6 * (d / max(r, EPS))  # dashes lengthen toward the rim
            L = dash * grow
            e = min(r, d + L)
            seg = [(cx + ux * d, cy + uy * d), (cx + ux * e, cy + uy * e)]
            if polyline_length(seg) > 0.15:
                out.extend(clip(seg, region, keep="inside") if region is not None else [seg])
            d = e + gap * grow
    return out


# --------------------------------------------------------------------------- #
# connectors                                                                  #
# --------------------------------------------------------------------------- #


def ribbon(
    p0: Point,
    p1: Point,
    n: int = 1,
    *,
    bow: float = 0.25,
    spread: float = 0.0,
    samples: int = 60,
    rng=None,
    wobble: float = 0.0,
) -> List[Poly]:
    """``n`` smooth curves from ``p0`` to ``p1``, bowed sideways by ``bow`` ×
    span and fanned across ``spread``. The flow bundles between stages."""
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    out: List[Poly] = []
    for i in range(n):
        f = 0.0 if n == 1 else (i / (n - 1) - 0.5)
        off = f * spread
        b = bow * L + (wobble * L * (rng.random() - 0.5) if (rng and wobble) else 0.0)
        cxp, cyp = (x0 + x1) / 2 + nx * b, (y0 + y1) / 2 + ny * b
        curve: Poly = []
        for k in range(samples + 1):
            t = k / samples
            s = 1 - t
            x = s * s * x0 + 2 * s * t * cxp + t * t * x1 + nx * off
            y = s * s * y0 + 2 * s * t * cyp + t * t * y1 + ny * off
            curve.append((x, y))
        out.append(curve)
    return out


# ---------------------------------------------------------------------------
# field_nest — the nesting rule that actually holds a constant gap
# ---------------------------------------------------------------------------
# ``contour_nest`` offsets the outline and ``radial_nest`` scales it. Both are
# wrong for a filled contour mass, in opposite ways:
#
#   contour_nest  holds the gap exactly, but an inward offset only exists as
#                 far as the tightest concave valley (``max_erode``): past that
#                 the rings fold, so a lobed shape keeps a hollow centre.
#   radial_nest   always reaches the centre, but the gap is NOT constant — it
#                 scales with the local radius. On a 4-lobe blob the measured
#                 gap runs 6.1 mm at a lobe tip against 3.3 mm in the valley,
#                 a 1.9x swing, and the inner rings close to nothing. That is
#                 what turns a mass into a solid black blot on paper.
#
# The distance field has neither failure. ``d`` = distance to the boundary has
# ``|grad d| = 1`` everywhere inside, so the level set at ``k*pitch`` is exactly
# ``pitch`` from the one at ``(k-1)*pitch`` — in every direction, all the way to
# the medial axis. Where the shape pinches, a level splits into two components
# on its own, which is the correct reading of a pinched mass rather than a bug.
#
# Ported from the technique proven in ``studio/convolutions`` (which hand-rolled
# it at the piece level); this is the engine home for it.


def _march_squares(F, xs, ys, iso: float) -> List[Poly]:
    """Iso-contour of ``F[j, i]`` (j indexes ys) as chained polylines."""
    import numpy as np

    table = {1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),),
             5: ((3, 2), (0, 1)), 6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),),
             9: ((0, 2),), 10: ((0, 3), (1, 2)), 11: ((1, 2),), 12: ((1, 3),),
             13: ((0, 1),), 14: ((0, 3),)}
    v0, v1 = F[:-1, :-1], F[:-1, 1:]
    v2, v3 = F[1:, 1:], F[1:, :-1]
    case = ((v0 > iso).astype(np.uint8)
            | ((v1 > iso).astype(np.uint8) << 1)
            | ((v2 > iso).astype(np.uint8) << 2)
            | ((v3 > iso).astype(np.uint8) << 3))
    jj, ii = np.nonzero((case != 0) & (case != 15))
    if len(jj) == 0:
        return []

    def lerp(pa, pb, va, vb):
        t = (iso - va) / (vb - va) if vb != va else 0.5
        return (pa[0] + t * (pb[0] - pa[0]), pa[1] + t * (pb[1] - pa[1]))

    segs: List[Tuple[Point, Point]] = []
    for j, i in zip(jj.tolist(), ii.tolist()):
        xa, xb = float(xs[i]), float(xs[i + 1])
        ya, yb = float(ys[j]), float(ys[j + 1])
        a, b, c, d = (float(v0[j, i]), float(v1[j, i]),
                      float(v2[j, i]), float(v3[j, i]))
        e = (lerp((xa, ya), (xb, ya), a, b), lerp((xb, ya), (xb, yb), b, c),
             lerp((xb, yb), (xa, yb), c, d), lerp((xa, yb), (xa, ya), d, a))
        for p, q in table[int(case[j, i])]:
            segs.append((e[p], e[q]))
    return _chain(segs)


def _chain(segs: Sequence[Tuple[Point, Point]], tol: float = 1e-6) -> List[Poly]:
    """Join loose segments end-to-end into the longest polylines they form."""
    def key(p: Point) -> Tuple[int, int]:
        return (round(p[0] / tol), round(p[1] / tol))

    ends: dict = {}
    for idx, (a, b) in enumerate(segs):
        ends.setdefault(key(a), []).append((idx, 0))
        ends.setdefault(key(b), []).append((idx, 1))

    used = [False] * len(segs)
    out: List[Poly] = []
    for start in range(len(segs)):
        if used[start]:
            continue
        used[start] = True
        a, b = segs[start]
        chain = [a, b]
        for direction in (1, 0):  # extend forward from b, then backward from a
            while True:
                tip = chain[-1] if direction else chain[0]
                nxt = None
                for idx, side in ends.get(key(tip), ()):
                    if not used[idx]:
                        nxt = (idx, side)
                        break
                if nxt is None:
                    break
                idx, side = nxt
                used[idx] = True
                other = segs[idx][1 - side]
                chain.append(other) if direction else chain.insert(0, other)
            chain.reverse() if direction else None
        if len(chain) >= 2:
            out.append([tuple(p) for p in chain])
    return out


def _distance_field(ring: Sequence[Point], X, Y):
    """Distance to the ring, positive INSIDE and 0 outside. ``|grad| = 1``."""
    import numpy as np

    P = np.asarray([tuple(p) for p in ring], float)
    A, B = P, np.roll(P, -1, axis=0)
    d = np.full(X.shape, 1e9)
    inside = np.zeros(X.shape, bool)
    for (ax, ay), (bx, by) in zip(A, B):
        vx, vy = bx - ax, by - ay
        L2 = vx * vx + vy * vy
        if L2 > 1e-12:
            t = np.clip(((X - ax) * vx + (Y - ay) * vy) / L2, 0.0, 1.0)
            d = np.minimum(d, np.hypot(X - (ax + t * vx), Y - (ay + t * vy)))
        cond = (ay > Y) != (by > Y)
        if cond.any():
            xint = np.where(abs(by - ay) > 1e-12,
                            ax + (Y - ay) * vx / (by - ay + 1e-30), ax)
            inside ^= cond & (X < xint)
    return np.where(inside, d, 0.0)


def field_nest(
    ring: Sequence[Point],
    *,
    pitch: float,
    n: Optional[int] = None,
    resolution: Optional[float] = None,
    min_len: float = 1.0,
    include_outline: bool = True,
) -> List[Poly]:
    """Nest ``ring`` inward as level sets of its distance field.

    Unlike ``contour_nest`` (folds past the tightest valley) and ``radial_nest``
    (gap scales with radius), the gap here is exactly ``pitch`` everywhere, all
    the way to the medial axis. A pinched shape splits into separate components
    where it should.

    ``pitch`` is a physical distance in caller units — set it above the pen tip
    or the mass fills solid. ``n`` caps the ring count; the default runs until
    the field is exhausted.
    """
    import numpy as np

    pts = [tuple(p) for p in ring]
    if len(pts) < 3 or pitch <= 0:
        return []
    xs_p = [p[0] for p in pts]
    ys_p = [p[1] for p in pts]
    x0, x1 = min(xs_p), max(xs_p)
    y0, y1 = min(ys_p), max(ys_p)
    step = resolution if resolution else max(pitch / 3.0, 1e-3)
    pad = step * 2
    xs = np.arange(x0 - pad, x1 + pad + step, step)
    ys = np.arange(y0 - pad, y1 + pad + step, step)
    X, Y = np.meshgrid(xs, ys)
    D = _distance_field(pts, X, Y)
    peak = float(D.max())
    if peak <= 0:
        return []

    levels = []
    k = 0 if include_outline else 1
    while True:
        lvl = k * pitch
        if lvl >= peak:
            break
        levels.append(lvl)
        k += 1
        if n is not None and len(levels) >= n:
            break

    out: List[Poly] = []
    for lvl in levels:
        # The 0 level sits on the boundary itself, where the field is exactly 0
        # outside too; nudge in so marching squares sees a crossing.
        iso = max(lvl, step * 0.25)
        for chain in _march_squares(D, xs, ys, iso):
            if polyline_length(chain) >= min_len:
                out.append(chain)
    return out
