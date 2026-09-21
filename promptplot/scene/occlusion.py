"""Hidden-line removal for authored scenes — two rules for two kinds of drawing.

``cover_walk`` is the pen rule (cubist, engraving): walk the scene FRONT to back,
subtract the union of covers already passed from each object's marks, then add
the object's own cover. An object never occludes itself; cover-less objects are
transparent. Exact, via ``geometry.Polygon`` — a hatch line stops ON the facet
edge in front of it.

``paint_walk`` is the brush rule (acrylic): later opaque strokes hide earlier
ones. Rasterise footprints back-to-front; a stroke whose every sample is already
under paint is dropped. The oracle culled 562 of 11,725 this way.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..generative.engine.geometry import (  # noqa: F401  (erode_ring re-exported)
    Point,
    Poly,
    Polygon,
    Rect,
    Region,
    Union,
    clip,
    erode_ring,
)
from .models import Mark, Scene, SceneObject

# roles that give way to label clearance; contours and labels themselves never do
_YIELDS_TO_LABELS = {"hatch", "construction", "flow"}


def _label_regions(objects: Sequence[SceneObject], pad: float) -> Optional[Region]:
    """One keep-out box per object that carries label marks (bbox + pad)."""
    boxes: List[Region] = []
    for o in objects:
        pts = [p for m in o.marks if m.role == "label" for p in m.points]
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        boxes.append(Rect(min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad))
    if not boxes:
        return None
    return boxes[0] if len(boxes) == 1 else Union(*boxes)


def _length(poly: Sequence[Point]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:]))


def cover_walk(
    scene: Scene,
    *,
    erode: float = 0.01,
    label_pad: float = 2.0,
    min_len: float = 0.55,
) -> List[Tuple[int, Mark, List[Poly]]]:
    """-> ``[(object_index, mark, visible_polylines)]`` in ORIGINAL (back-to-front)
    order. Visible polylines are in source units."""
    objects = scene.objects
    labels = _label_regions(objects, label_pad)
    covered: List[Region] = []
    visible: Dict[int, List[Tuple[Mark, List[Poly]]]] = {}

    for idx in range(len(objects) - 1, -1, -1):
        obj = objects[idx]
        occluder = None if not covered else (covered[0] if len(covered) == 1 else Union(*covered))
        kept: List[Tuple[Mark, List[Poly]]] = []
        for m in obj.marks:
            runs: List[Poly] = [list(m.points)]
            if occluder is not None:
                runs = [r for poly in runs for r in clip(poly, occluder, keep="outside")]
            if labels is not None and m.role in _YIELDS_TO_LABELS:
                runs = [r for poly in runs for r in clip(poly, labels, keep="outside")]
            runs = [r for r in runs if len(r) >= 2 and _length(r) >= min_len]
            if runs:
                kept.append((m, runs))
        visible[idx] = kept
        if obj.cover:
            covered.append(Polygon(erode_ring(obj.cover, erode)))

    out: List[Tuple[int, Mark, List[Poly]]] = []
    for idx in range(len(objects)):
        for m, runs in visible.get(idx, []):
            out.append((idx, m, runs))
    return out


def paint_walk(
    strokes: Sequence[Tuple[float, Poly]],
    *,
    cell: float = 0.5,
    sample: float = 0.5,
) -> List[bool]:
    """Keep-flags for ``strokes = [(width_mm, polyline_mm), ...]`` given in PAINT
    ORDER (first painted first). A stroke is dropped only when every sample along
    it is already covered by the footprints of strokes painted after it."""
    if not strokes:
        return []
    xs = [p[0] for _, poly in strokes for p in poly]
    ys = [p[1] for _, poly in strokes for p in poly]
    wmax = max(w for w, _ in strokes)
    x0, y0 = min(xs) - wmax, min(ys) - wmax
    W = int(math.ceil((max(xs) + wmax - x0) / cell)) + 2
    H = int(math.ceil((max(ys) + wmax - y0) / cell)) + 2
    covered = np.zeros((H, W), dtype=bool)
    keep = [True] * len(strokes)

    def samples(poly: Poly) -> List[Point]:
        out: List[Point] = [poly[0]]
        for a, b in zip(poly, poly[1:]):
            d = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(1, int(d / sample))
            for k in range(1, n + 1):
                t = k / n
                out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
        return out

    def paint(poly: Poly, width: float) -> None:
        r = max(1, int(round(width / 2.0 / cell)))
        yy, xx = np.ogrid[-r : r + 1, -r : r + 1]
        disc = (xx * xx + yy * yy) <= r * r
        for px, py in samples(poly):
            cx = int((px - x0) / cell)
            cy = int((py - y0) / cell)
            ya, yb = max(0, cy - r), min(H, cy + r + 1)
            xa, xb = max(0, cx - r), min(W, cx + r + 1)
            if ya >= yb or xa >= xb:
                continue
            sub = disc[(ya - (cy - r)) : (yb - (cy - r)), (xa - (cx - r)) : (xb - (cx - r))]
            covered[ya:yb, xa:xb] |= sub

    for i in range(len(strokes) - 1, -1, -1):
        w, poly = strokes[i]
        pts = samples(poly)
        hidden = all(
            covered[int((py - y0) / cell), int((px - x0) / cell)] for px, py in pts
        )
        keep[i] = not hidden
        paint(poly, w)
    return keep
