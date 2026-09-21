"""Shared import plumbing: polylines grouped by color/layer → color-tagged GCode.

An importer parses a file into a list of :class:`ImportedPath` (a polyline plus a
color string and a layer name). This module fits them onto the paper and turns
them into color-tagged GCode strokes for the normal color-layer pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from ..models import GCodeCommand

Point = Tuple[float, float]


@dataclass
class ImportedPath:
    points: List[Point]
    color: str = "black"  # stroke color (hex or name)
    layer: str = "default"  # source layer name


@dataclass
class ImportResult:
    paths: List[ImportedPath] = field(default_factory=list)
    y_down: bool = True  # SVG is y-down; DXF is y-up
    source: str = ""
    # Page geometry when the file declares it (SVG viewBox + physical width):
    # viewbox = (min_x, min_y, width, height) in user units, unit_scale = mm per
    # user unit. Both None when unknown. This is what lets ``fit=False`` be a
    # true mm-native passthrough instead of a recentred guess.
    viewbox: Optional[Tuple[float, float, float, float]] = None
    unit_scale: Optional[float] = None


def _bbox(paths: List[ImportedPath]) -> Tuple[float, float, float, float]:
    xs = [x for p in paths for x, _ in p.points]
    ys = [y for p in paths for _, y in p.points]
    return min(xs), min(ys), max(xs), max(ys)


def build_program_commands(
    result: ImportResult,
    config,
    fit: bool = True,
    group_by: str = "color",
) -> Tuple[List[GCodeCommand], List[str]]:
    """Fit imported paths onto the paper and emit color-tagged strokes.

    Returns ``(commands, palette)`` where palette[i] is the source color/layer
    name for pen index i. ``group_by`` is ``"color"`` or ``"layer"``.
    """
    paths = [p for p in result.paths if len(p.points) >= 2]
    if not paths:
        return [], []

    if not fit and result.viewbox is not None and result.unit_scale:
        # mm-native passthrough: the file declared its page, so honour it exactly.
        # Page origin → (0, 0) mm; y flipped within the page, not the ink bbox; no
        # recentring. A 297x420 viewBox lands at precisely [0,297]x[0,420].
        vx, vy, vw, vh = result.viewbox
        s = result.unit_scale

        def tx(x: float, y: float) -> Point:
            nx = (x - vx) * s
            ny = (vh - (y - vy)) * s if result.y_down else (y - vy) * s
            return round(nx, 3), round(ny, 3)

    else:
        minx, miny, maxx, maxy = _bbox(paths)
        src_w = max(maxx - minx, 1e-6)
        src_h = max(maxy - miny, 1e-6)

        dx0, dy0, dx1, dy1 = config.paper.get_drawable_area()
        dst_w = dx1 - dx0
        dst_h = dy1 - dy0

        if fit:
            scale = min(dst_w / src_w, dst_h / src_h)
        else:
            scale = 1.0
        # center the scaled drawing in the drawable area
        off_x = dx0 + (dst_w - src_w * scale) / 2.0
        off_y = dy0 + (dst_h - src_h * scale) / 2.0

        def tx(x: float, y: float) -> Point:
            nx = off_x + (x - minx) * scale
            # SVG y grows downward — flip so the drawing isn't mirrored top/bottom.
            if result.y_down:
                ny = off_y + (maxy - y) * scale
            else:
                ny = off_y + (y - miny) * scale
            return round(nx, 2), round(ny, 2)

    # Assign a pen index per distinct color/layer key, in first-seen order.
    palette: List[str] = []
    index_of: dict = {}
    for p in paths:
        key = p.color if group_by == "color" else p.layer
        if key not in index_of:
            index_of[key] = len(palette)
            palette.append(key)

    commands: List[GCodeCommand] = []
    for p in paths:
        key = p.color if group_by == "color" else p.layer
        ci = index_of[key]
        pts = [tx(x, y) for x, y in p.points]
        commands.append(GCodeCommand(command="G0", x=pts[0][0], y=pts[0][1]))
        commands.append(GCodeCommand(command="M3", s=1000, color=ci))
        for x, y in pts[1:]:
            commands.append(GCodeCommand(command="G1", x=x, y=y, f=config.pen.feed_rate, color=ci))
        commands.append(GCodeCommand(command="M5"))

    return commands, palette
