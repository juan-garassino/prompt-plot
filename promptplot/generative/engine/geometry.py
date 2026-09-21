"""Computational-geometry 'diagram ops' for the generative engine.

A small, dependency-free 2D toolkit so pieces COMPOSE diagrams with exact
clip / trim / offset against regions, instead of hand-rolling per-piece
sample-and-snap conditionals (the `hidden = ... or ...` pattern that produced
staggered, grazing ring-ends).

API vocabulary modelled on FreeCAD (studied 2026-09-15):
  - Draft workbench: Offset, Trimex (trim/extend), Split, Join  →  offset(), clip()/trim_to()
  - Part workbench 2D boolean: cut / common / section (OpenCASCADE) →  Region &/|/~ and clip(keep=)
FreeCAD's OCCT kernel is too heavy to embed; this mirrors the *concepts* with
exact segment↔boundary intersection maths (so a curve clipped at a line stops
precisely ON it — no sampling stagger). Regions compose with Union/Intersect/
Complement; ``clip(poly, region, keep='outside'|'inside')`` is the workhorse.
Shapely can back arbitrary-polygon booleans later behind the same API.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple

Point = Tuple[float, float]
Poly = List[Point]
Interval = Tuple[float, float]

EPS = 1e-9


# ---------------------------------------------------------------------------
# interval algebra over a segment parameter t in [0, 1]
# ---------------------------------------------------------------------------
def _union(ivs: Sequence[Interval]) -> List[Interval]:
    ivs = sorted((a, b) for a, b in ivs if b - a > EPS)
    out: List[Interval] = []
    for a, b in ivs:
        if out and a <= out[-1][1] + EPS:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _intersect(sets: Sequence[List[Interval]]) -> List[Interval]:
    cur: List[Interval] = [(0.0, 1.0)]
    for ivs in sets:
        nxt: List[Interval] = []
        for a, b in cur:
            for c, d in ivs:
                lo, hi = max(a, c), min(b, d)
                if hi - lo > EPS:
                    nxt.append((lo, hi))
        cur = nxt
    return cur


def _complement(ivs: Sequence[Interval]) -> List[Interval]:
    ivs = _union(ivs)
    out: List[Interval] = []
    prev = 0.0
    for a, b in ivs:
        if a - prev > EPS:
            out.append((prev, a))
        prev = b
    if 1.0 - prev > EPS:
        out.append((prev, 1.0))
    return out


# ---------------------------------------------------------------------------
# regions — each returns the t-intervals of a segment that lie INSIDE it
# ---------------------------------------------------------------------------
class Region:
    def inside_intervals(self, p0: Point, p1: Point) -> List[Interval]:
        raise NotImplementedError

    def contains(self, x: float, y: float) -> bool:
        raise NotImplementedError

    def __or__(self, o: "Region") -> "Region":
        return Union(self, o)

    def __and__(self, o: "Region") -> "Region":
        return Intersect(self, o)

    def __invert__(self) -> "Region":
        return Complement(self)


class Circle(Region):
    def __init__(self, cx: float, cy: float, r: float):
        self.cx, self.cy, self.r = cx, cy, r

    def contains(self, x, y):
        return (x - self.cx) ** 2 + (y - self.cy) ** 2 <= self.r * self.r + EPS

    def inside_intervals(self, p0, p1):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        fx, fy = p0[0] - self.cx, p0[1] - self.cy
        a = dx * dx + dy * dy
        if a < EPS:
            return [(0.0, 1.0)] if self.contains(*p0) else []
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - self.r * self.r
        disc = b * b - 4 * a * c
        if disc <= 0:
            return [(0.0, 1.0)] if self.contains(*p0) else []
        s = math.sqrt(disc)
        t1, t2 = (-b - s) / (2 * a), (-b + s) / (2 * a)
        lo, hi = max(0.0, min(t1, t2)), min(1.0, max(t1, t2))
        return [(lo, hi)] if hi - lo > EPS else []


class HalfPlane(Region):
    """Inside where ``nx*x + ny*y + c <= 0``."""

    def __init__(self, nx: float, ny: float, c: float):
        self.nx, self.ny, self.c = nx, ny, c

    def _f(self, x, y):
        return self.nx * x + self.ny * y + self.c

    def contains(self, x, y):
        return self._f(x, y) <= EPS

    def inside_intervals(self, p0, p1):
        f0, f1 = self._f(*p0), self._f(*p1)
        d = f1 - f0
        if abs(d) < EPS:  # constant along the segment
            return [(0.0, 1.0)] if f0 <= EPS else []
        t = -f0 / d  # parameter where f crosses 0
        if d > 0:  # f increasing → inside (f<=0) for t <= t*
            hi = max(0.0, min(1.0, t))
            return [(0.0, hi)] if hi > EPS else []
        # f decreasing → inside for t >= t*
        lo = max(0.0, min(1.0, t))
        return [(lo, 1.0)] if lo < 1.0 - EPS else []


def Band(axis: str, lo: float, hi: float) -> Region:
    """Axis-aligned slab lo <= coord <= hi (``axis`` = 'x' or 'y')."""
    if axis == "x":
        return HalfPlane(-1.0, 0.0, lo) & HalfPlane(1.0, 0.0, -hi)
    return HalfPlane(0.0, -1.0, lo) & HalfPlane(0.0, 1.0, -hi)


def Rect(x0: float, y0: float, x1: float, y1: float) -> Region:
    return Band("x", x0, x1) & Band("y", y0, y1)


class Polygon(Region):
    """Arbitrary simple polygon (concave allowed), given as its vertex ring.

    ``contains`` is even-odd ray casting; ``inside_intervals`` finds every exact
    segment↔edge crossing and toggles inside/outside between them, so a polyline
    clipped against a facet stops precisely ON the facet edge. This is what makes
    scene ``cover`` occlusion exact without shapely: we only ever clip LINES
    against areas, never merge areas, so a Union of Polygons is enough.

    Edges are half-open (``0 <= u < 1``) so a crossing exactly at a shared vertex
    is counted once, not twice.
    """

    def __init__(self, pts: Sequence[Point]):
        ring = [tuple(p) for p in pts]
        if len(ring) >= 2 and (
            abs(ring[0][0] - ring[-1][0]) < 1e-9 and abs(ring[0][1] - ring[-1][1]) < 1e-9
        ):
            ring = ring[:-1]
        if len(ring) < 3:
            raise ValueError("Polygon needs at least 3 distinct vertices")
        self.pts: List[Point] = ring
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        self.bbox = (min(xs), min(ys), max(xs), max(ys))

    def _edges(self):
        n = len(self.pts)
        for i in range(n):
            yield self.pts[i], self.pts[(i + 1) % n]

    def contains(self, x, y):
        bx0, by0, bx1, by1 = self.bbox
        if x < bx0 - EPS or x > bx1 + EPS or y < by0 - EPS or y > by1 + EPS:
            return False
        inside = False
        for (ax, ay), (bx, by) in self._edges():
            # half-open in y so a ray through a vertex toggles exactly once
            if (ay > y) != (by > y):
                t = (y - ay) / (by - ay)
                if ax + t * (bx - ax) > x:
                    inside = not inside
        return inside

    def inside_intervals(self, p0, p1):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        if abs(dx) < EPS and abs(dy) < EPS:
            return [(0.0, 1.0)] if self.contains(*p0) else []
        # quick reject: segment bbox vs polygon bbox
        sx0, sx1 = min(p0[0], p1[0]), max(p0[0], p1[0])
        sy0, sy1 = min(p0[1], p1[1]), max(p0[1], p1[1])
        bx0, by0, bx1, by1 = self.bbox
        if sx1 < bx0 - EPS or sx0 > bx1 + EPS or sy1 < by0 - EPS or sy0 > by1 + EPS:
            return []
        ts: List[float] = []
        for (ax, ay), (bx, by) in self._edges():
            ex, ey = bx - ax, by - ay
            den = dx * ey - dy * ex
            if abs(den) < EPS:
                continue  # parallel; collinear overlap handled by endpoint tests
            qx, qy = ax - p0[0], ay - p0[1]
            t = (qx * ey - qy * ex) / den
            u = (qx * dy - qy * dx) / den
            if -EPS <= u < 1.0 - EPS and EPS < t < 1.0 - EPS:
                ts.append(t)
        ts.sort()
        inside = self.contains(*p0)
        out: List[Interval] = []
        prev = 0.0
        for t in ts:
            if inside and t - prev > EPS:
                out.append((prev, t))
            inside = not inside
            prev = t
        if inside and 1.0 - prev > EPS:
            out.append((prev, 1.0))
        return _union(out)


class Union(Region):
    def __init__(self, *rs: Region):
        self.rs = rs

    def contains(self, x, y):
        return any(r.contains(x, y) for r in self.rs)

    def inside_intervals(self, p0, p1):
        return _union([iv for r in self.rs for iv in r.inside_intervals(p0, p1)])


class Intersect(Region):
    def __init__(self, *rs: Region):
        self.rs = rs

    def contains(self, x, y):
        return all(r.contains(x, y) for r in self.rs)

    def inside_intervals(self, p0, p1):
        return _intersect([r.inside_intervals(p0, p1) for r in self.rs])


class Complement(Region):
    def __init__(self, r: Region):
        self.r = r

    def contains(self, x, y):
        return not self.r.contains(x, y)

    def inside_intervals(self, p0, p1):
        return _complement(self.r.inside_intervals(p0, p1))


# ---------------------------------------------------------------------------
# ops
# ---------------------------------------------------------------------------
def _at(p0: Point, p1: Point, t: float) -> Point:
    return (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)


def clip(poly: Poly, region: Region, keep: str = "outside") -> List[Poly]:
    """Split ``poly`` at exact region-boundary crossings; return the sub-polylines
    on the kept side (``keep`` = 'outside' | 'inside'). No sampling — a curve
    clipped at a line/circle stops exactly on it."""
    if len(poly) < 2:
        return []
    runs: List[Poly] = []
    cur: Poly = []
    for p0, p1 in zip(poly, poly[1:]):
        ins = region.inside_intervals(p0, p1)
        keep_ivs = ins if keep == "inside" else _complement(ins)
        for t0, t1 in keep_ivs:
            a, b = _at(p0, p1, t0), _at(p0, p1, t1)
            if cur and t0 <= EPS and abs(cur[-1][0] - a[0]) < 1e-6 and abs(cur[-1][1] - a[1]) < 1e-6:
                cur.append(b)
            else:
                if len(cur) >= 2:
                    runs.append(cur)
                cur = [a, b]
        # if the kept part doesn't run to the end of this segment, the polyline
        # leaves the kept side here → close the current run
        if not keep_ivs or keep_ivs[-1][1] < 1.0 - EPS:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def trim_to(poly: Poly, region: Region) -> List[Poly]:
    """FreeCAD-Trimex-like: keep the parts of ``poly`` OUTSIDE ``region`` (i.e.
    stop the curve exactly at the region boundary)."""
    return clip(poly, region, keep="outside")


def bezier_flatten(ctrl: Sequence[Point], max_seg: float = 2.0) -> Poly:
    """Flatten a quadratic (3 pts) or cubic (4 pts) Bezier into a polyline.

    Step count is ``max(8, ceil(control_polygon_length / max_seg))`` — the rule
    the oracle drawings were flattened with, so a re-import reproduces their
    sampling. Returns both endpoints.
    """
    n = len(ctrl)
    if n not in (3, 4):
        raise ValueError("bezier_flatten expects 3 (quadratic) or 4 (cubic) control points")
    hull = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(ctrl, ctrl[1:]))
    steps = max(8, int(math.ceil(hull / max(max_seg, 1e-9))))
    out: Poly = []
    for k in range(steps + 1):
        t = k / steps
        s = 1.0 - t
        if n == 3:
            (x0, y0), (x1, y1), (x2, y2) = ctrl
            x = s * s * x0 + 2 * s * t * x1 + t * t * x2
            y = s * s * y0 + 2 * s * t * y1 + t * t * y2
        else:
            (x0, y0), (x1, y1), (x2, y2), (x3, y3) = ctrl
            x = s * s * s * x0 + 3 * s * s * t * x1 + 3 * s * t * t * x2 + t * t * t * x3
            y = s * s * s * y0 + 3 * s * s * t * y1 + 3 * s * t * t * y2 + t * t * t * y3
        out.append((x, y))
    return out


def polyline_length(poly: Sequence[Point]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:]))


def resample_by_arclength(poly: Sequence[Point], step: float = 0.0, n: int = 0) -> Poly:
    """Resample a polyline at uniform arc-length spacing.

    Give ``step`` (mm between samples) OR ``n`` (exact sample count). Both
    endpoints are kept. Two guides resampled with the same ``n`` correspond
    point-for-point by fraction of their own length — the correspondence
    ``flow_family`` interpolates between.
    """
    pts = [tuple(p) for p in poly]
    if len(pts) < 2:
        return list(pts)
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(seg)
    if total < EPS:
        return [pts[0], pts[-1]] if n <= 2 else [pts[0]] * n
    if n <= 0:
        if step <= 0:
            raise ValueError("resample_by_arclength needs step > 0 or n > 0")
        n = max(2, int(math.ceil(total / step)) + 1)
    out: Poly = []
    cum = 0.0
    j = 0
    for k in range(n):
        target = total * k / (n - 1)
        while j < len(seg) - 1 and cum + seg[j] < target - EPS:
            cum += seg[j]
            j += 1
        d = seg[j] if seg[j] > EPS else 1.0
        t = min(1.0, max(0.0, (target - cum) / d))
        out.append(_at(pts[j], pts[j + 1], t))
    out[-1] = pts[-1]
    return out


def signed_area(ring: Sequence[Point]) -> float:
    a = 0.0
    n = len(ring)
    for i in range(n):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return a / 2.0


def erode_ring(
    ring: Sequence[Point],
    d: float,
    *,
    miter: bool = True,
    prune_folds: bool = False,
    miter_limit: float = 2.0,
) -> List[Point]:
    """Offset a closed ring INWARD by ``d`` whichever way it winds. Negative ``d``
    grows it.

    ``miter=True`` (default) moves each EDGE exactly ``d`` — right for polygons
    with real corners (covers, facets, panels). For a densely sampled SMOOTH
    curve there are no true corners, and the bisector correction only amplifies
    sampling noise into spikes: pass ``miter=False`` for a plain per-point normal
    offset, which is the exact offset of a smooth curve.

    ``prune_folds`` drops points whose local direction reversed against the
    source — the loops that appear once ``d`` exceeds the curve's inner radius of
    curvature (a clover's valleys long before its lobes). Without it a nest of
    offsets turns into a star.
    """
    pts = [tuple(p) for p in ring]
    if len(pts) >= 2 and abs(pts[0][0] - pts[-1][0]) < 1e-9 and abs(pts[0][1] - pts[-1][1]) < 1e-9:
        pts = pts[:-1]
    n = len(pts)
    if n < 3 or d == 0:
        return pts
    inward = 1.0 if signed_area(pts) > 0 else -1.0  # CCW: left normal points inward
    out: List[Point] = []
    for i in range(n):
        (ax, ay), (bx, by), (cx, cy) = pts[i - 1], pts[i], pts[(i + 1) % n]
        n1 = (-(by - ay), bx - ax)
        n2 = (-(cy - by), cx - bx)
        L1 = math.hypot(*n1) or 1.0
        L2 = math.hypot(*n2) or 1.0
        u1 = (n1[0] / L1, n1[1] / L1)
        u2 = (n2[0] / L2, n2[1] / L2)
        bx_, by_ = u1[0] + u2[0], u1[1] + u2[1]
        L = math.hypot(bx_, by_)
        if L < 1e-9:  # 180° hairpin: no meaningful bisector, fall back to one normal
            bx_, by_, L = u1[0], u1[1], 1.0
        bx_, by_ = bx_ / L, by_ / L
        if miter:
            cos_half = bx_ * u1[0] + by_ * u1[1]
            k = inward * d / max(1.0 / miter_limit, cos_half)
        else:
            k = inward * d
        out.append((bx + k * bx_, by + k * by_))

    if prune_folds and len(out) > 8:
        keep: List[Point] = []
        for i in range(len(out)):
            sx = pts[(i + 1) % n][0] - pts[i - 1][0]
            sy = pts[(i + 1) % n][1] - pts[i - 1][1]
            ox = out[(i + 1) % len(out)][0] - out[i - 1][0]
            oy = out[(i + 1) % len(out)][1] - out[i - 1][1]
            if sx * ox + sy * oy > 0:  # direction preserved → not inside a fold
                keep.append(out[i])
        out = keep
    return out


def smooth_ring(ring: Sequence[Point], passes: int = 2, w: float = 0.5) -> List[Point]:
    """Laplacian smoothing of a closed ring: ``p ← (1-w)·p + w·(prev+next)/2``.

    Run after a fold-pruning offset — deleting the folded points leaves a sharp
    seam where the ring closes over the gap, and that seam is a spike. A couple
    of passes removes it and barely moves the rest of the curve."""
    pts = [tuple(p) for p in ring]
    n = len(pts)
    if n < 4 or passes <= 0:
        return pts
    for _ in range(passes):
        nxt: List[Point] = []
        for i in range(n):
            ax, ay = pts[i - 1]
            bx, by = pts[i]
            cx, cy = pts[(i + 1) % n]
            nxt.append(
                (bx * (1 - w) + w * (ax + cx) / 2.0, by * (1 - w) + w * (ay + cy) / 2.0)
            )
        pts = nxt
    return pts


def offset(poly: Poly, d: float) -> Poly:
    """Parallel offset by ``d`` mm (miter joins). +d = left of travel direction."""
    if len(poly) < 2:
        return list(poly)
    seg_n: List[Point] = []
    for p0, p1 in zip(poly, poly[1:]):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy) or 1.0
        seg_n.append((-dy / L, dx / L))
    out: Poly = []
    for i, p in enumerate(poly):
        if i == 0:
            nx, ny = seg_n[0]
        elif i == len(poly) - 1:
            nx, ny = seg_n[-1]
        else:
            nx, ny = seg_n[i - 1][0] + seg_n[i][0], seg_n[i - 1][1] + seg_n[i][1]
            L = math.hypot(nx, ny) or 1.0
            nx, ny = nx / L, ny / L
        out.append((p[0] + nx * d, p[1] + ny * d))
    return out
