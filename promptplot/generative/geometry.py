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
