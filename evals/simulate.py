"""Toolpath simulator used by the eval harness.

Walks a GCode command list the way a pen plotter would (M3 = pen down,
M5 = pen up, G0 = rapid, G1 = feed move) and records every inked segment,
every travel move and every safety violation. It is deliberately independent
of ``promptplot.postprocess`` so it can judge that code instead of trusting it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from promptplot.models import GCodeCommand

Point = tuple[float, float]
# (x0, y0, x1, y1, color) with endpoints rounded and sorted so a segment drawn
# in either direction gets the same key.
SegKey = tuple[float, float, float, float, int]

EPS = 1e-3  # mm tolerance for bounds checks
ROUND = 2  # decimals used when matching segments (0.01 mm)


def seg_key(a: Point, b: Point, color: int = 0) -> SegKey | None:
    """Canonical, direction-free key for a segment; ``None`` for zero length."""
    pa = (round(a[0], ROUND), round(a[1], ROUND))
    pb = (round(b[0], ROUND), round(b[1], ROUND))
    if pa == pb:
        return None
    lo, hi = sorted((pa, pb))
    return (lo[0], lo[1], hi[0], hi[1], color)


def seg_len(k: SegKey) -> float:
    return math.hypot(k[2] - k[0], k[3] - k[1])


@dataclass
class SimResult:
    ink: dict[SegKey, int] = field(default_factory=dict)  # segment -> times drawn
    ink_order: list[SegKey] = field(default_factory=list)
    draw_mm: float = 0.0
    travel_mm: float = 0.0
    pen_lifts: int = 0  # down -> up transitions
    g0_pen_down: int = 0  # rapid moves with the pen down (drags ink)
    g1_pen_up: int = 0  # feed moves with the pen up (lost ink)
    out_of_bounds: int = 0  # inked segment endpoints outside the drawable area
    starts_pen_up: bool = True
    ends_pen_up: bool = True
    color_switches: int = 0  # colour changes along the inked order
    colors: list[int] = field(default_factory=list)


def simulate(
    commands: list[GCodeCommand],
    drawable: tuple[float, float, float, float] | None = None,
    start: Point = (0.0, 0.0),
    g1_is_ink: bool = False,
) -> SimResult:
    """Simulate ``commands`` and return ink/travel/safety statistics.

    ``g1_is_ink=True`` treats every G1 as ink regardless of M3/M5. That is the
    project's pen convention (G1 = draw) and is how the *intended* drawing of a
    raw, possibly malformed LLM response is reconstructed for reference.
    """
    r = SimResult()
    x, y = start
    down = False
    first_motion = True
    last_color: int | None = None
    for cmd in commands:
        c = cmd.command
        if c == "M3":
            down = True
            continue
        if c == "M5":
            if down:
                r.pen_lifts += 1
            down = False
            continue
        if c not in ("G0", "G1", "G2", "G3"):
            continue
        if c in ("G2", "G3"):
            # GCodeCommand has no I/J/R fields, so the arc centre is already lost
            # at parse time; score it as its chord, like approximate_arcs does.
            c = "G1"
        nx = cmd.x if cmd.x is not None else x
        ny = cmd.y if cmd.y is not None else y
        if (nx, ny) == (x, y):
            continue
        if first_motion:
            r.starts_pen_up = not down
            first_motion = False
        inked = (c == "G1" and (down or g1_is_ink)) or (c == "G0" and down and not g1_is_ink)
        if c == "G0" and down:
            r.g0_pen_down += 1
        if c == "G1" and not down:
            r.g1_pen_up += 1
        d = math.hypot(nx - x, ny - y)
        if inked:
            color = cmd.color if cmd.color is not None else 0
            k = seg_key((x, y), (nx, ny), color)
            if k is not None:
                r.ink[k] = r.ink.get(k, 0) + 1
                r.ink_order.append(k)
                r.draw_mm += d
                if last_color is not None and color != last_color:
                    r.color_switches += 1
                last_color = color
                if color not in r.colors:
                    r.colors.append(color)
            if drawable is not None:
                x0, y0, x1, y1 = drawable
                for px, py in ((x, y), (nx, ny)):
                    if not (x0 - EPS <= px <= x1 + EPS and y0 - EPS <= py <= y1 + EPS):
                        r.out_of_bounds += 1
        else:
            r.travel_mm += d
        x, y = nx, ny
    r.ends_pen_up = not down
    return r


CELL = 0.5  # mm raster used to compare ink coverage


def ink_cells(ink: dict[SegKey, int], drawable=None) -> set[tuple[int, int, int]]:
    """Rasterise inked segments into ``(i, j, color)`` cells of ``CELL`` mm.

    Comparing coverage rather than exact segments makes the fidelity check
    indifferent to stroke order, stroke direction and subdivision (arc
    approximation, stroke merging). With ``drawable`` the segment endpoints are
    clamped into it first, mirroring the pipeline's default ``clamp`` bounds mode.
    """
    cells: set[tuple[int, int, int]] = set()
    for ax, ay, bx, by, col in ink:
        if drawable is not None:
            # clamp mode moves endpoints, so the segment between them stays straight
            x0, y0, x1, y1 = drawable
            ax, ay = min(max(ax, x0), x1), min(max(ay, y0), y1)
            bx, by = min(max(bx, x0), x1), min(max(by, y0), y1)
        n = max(1, int(math.ceil(math.hypot(bx - ax, by - ay) / (CELL / 2))))
        for i in range(n + 1):
            t = i / n
            px, py = ax + (bx - ax) * t, ay + (by - ay) * t
            cells.add((int(math.floor(px / CELL)), int(math.floor(py / CELL)), col))
    return cells


def _uncovered(a: set[tuple[int, int, int]], b: set[tuple[int, int, int]]) -> int:
    """Cells of ``a`` with no cell of ``b`` (same colour) within one cell."""
    n = 0
    for i, j, c in a:
        if not any((i + di, j + dj, c) in b for di in (-1, 0, 1) for dj in (-1, 0, 1)):
            n += 1
    return n


def ink_diff(ref_cells, got_cells) -> tuple[float, float]:
    """Return approximate ``(missing_mm, spurious_mm)`` of ink vs the reference.

    Colour is part of the cell key, so ink drawn with the wrong pen counts as
    both missing (right pen) and spurious (wrong pen).
    """
    return _uncovered(ref_cells, got_cells) * CELL, _uncovered(got_cells, ref_cells) * CELL


def layer_pen_down_leaks(layers) -> int:
    """Count pen-down events a colour layer performs without inking anything.

    When a layer ends with an ``M3`` that belongs to the *next* colour's first
    stroke, the plotter lowers the current pen at the next colour's start point
    (a stray dot in the wrong colour) before the swap pause.
    """
    leaks = 0
    for _color, cmds in layers:
        pending = False
        for cmd in cmds:
            if cmd.command == "M3":
                pending = True
            elif cmd.command == "G1" and pending:
                pending = False
            elif cmd.command == "M5":
                pending = False
        if pending:
            leaks += 1
    return leaks


def layer_mixed_colors(layers) -> int:
    """Count layers that contain inked G1s of more than one colour."""
    bad = 0
    for _color, cmds in layers:
        cols = {c.color for c in cmds if c.command == "G1" and c.color is not None}
        if len(cols) > 1:
            bad += 1
    return bad
