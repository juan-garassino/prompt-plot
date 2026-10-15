"""
Post-processing pipeline for PromptPlot v3.0

Merged from:
- PromptPlot utils/gcode_optimizer.py: stroke extraction, reordering, pen safety
- drawStream gcode_architect.py: G4 dwell injection after pen commands
- drawStream gcode_crafter.py: brush reload sequences every N strokes

Pipeline order (critical — dwells MUST be last):
  1. ensure_pen_safety()      — fix pen state violations
  2. optimize_gcode_program() — reorder strokes to minimize travel
  3. insert_paint_dips()      — ink reload sequences (brush mode)
  4. insert_pen_dwells()      — G4 after every M3/M5
"""

import math
import logging
from typing import List, Tuple, Union

from .models import GCodeCommand, GCodeProgram
from .config import PenConfig, BrushConfig, PaperConfig, PromptPlotConfig
from .engine import PenState

_log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 0. Bounds Validation
# ---------------------------------------------------------------------------


def validate_bounds(
    program: GCodeProgram,
    paper: PaperConfig,
    mode: str = "clamp",
) -> Tuple[GCodeProgram, List[str]]:
    """Validate and optionally fix out-of-bounds coordinates.

    Args:
        program: The GCode program to validate.
        paper: Paper configuration with dimensions and margins.
        mode: "clamp" (fix coordinates), "reject" (remove commands), or "warn" (keep, log).

    Returns:
        Tuple of (possibly modified program, list of violation messages).
    """
    x0, y0, x1, y1 = paper.get_drawable_area()
    # G0 travel may reach corners (0,0); only G1 draw must stay inside margins.
    mx0, my0, mx1, my1 = 0.0, 0.0, paper.width, paper.height
    violations: List[str] = []
    new_commands: List[GCodeCommand] = []

    # A G0 whose next XY motion is a G1 is where the pen goes down, i.e. the
    # first inked point of a stroke. In clamp mode it must obey the drawable
    # area like the G1s, otherwise the stroke starts in the margin.
    stroke_start = [False] * len(program.commands)
    next_is_draw = False
    for i in range(len(program.commands) - 1, -1, -1):
        cmd = program.commands[i]
        if cmd.command in ("G0", "G1") and (cmd.x is not None or cmd.y is not None):
            stroke_start[i] = cmd.command == "G0" and next_is_draw
            next_is_draw = cmd.command == "G1"

    for i, cmd in enumerate(program.commands):
        out_of_bounds = False
        clamped_x = cmd.x
        clamped_y = cmd.y

        # Choose bounds per move type.
        if cmd.command == "G1" or (mode == "clamp" and stroke_start[i]):
            lx0, ly0, lx1, ly1 = x0, y0, x1, y1
        else:
            lx0, ly0, lx1, ly1 = mx0, my0, mx1, my1

        if cmd.x is not None:
            if cmd.x < lx0 or cmd.x > lx1:
                out_of_bounds = True
                violations.append(
                    f"Cmd {i} ({cmd.command}): X={cmd.x:.1f} outside [{lx0:.1f}, {lx1:.1f}]"
                )
                clamped_x = max(lx0, min(cmd.x, lx1))

        if cmd.y is not None:
            if cmd.y < ly0 or cmd.y > ly1:
                out_of_bounds = True
                violations.append(
                    f"Cmd {i} ({cmd.command}): Y={cmd.y:.1f} outside [{ly0:.1f}, {ly1:.1f}]"
                )
                clamped_y = max(ly0, min(cmd.y, ly1))

        if out_of_bounds:
            if mode == "clamp":
                new_commands.append(cmd.model_copy(update={"x": clamped_x, "y": clamped_y}))
            elif mode == "reject":
                _log.warning("Rejecting command %d: %s (out of bounds)", i, cmd.to_gcode())
                continue
            else:  # warn
                new_commands.append(cmd)
        else:
            new_commands.append(cmd)

    # Ensure we don't end up with empty program after rejection
    if not new_commands:
        new_commands = [GCodeCommand(command="M5"), GCodeCommand(command="G0", x=0, y=0)]

    metadata = {**(program.metadata or {})}
    if violations:
        metadata["bounds_violations"] = len(violations)
        metadata["bounds_mode"] = mode

    return GCodeProgram(commands=new_commands, metadata=metadata), violations


def validate_single_command(
    cmd: GCodeCommand,
    paper: PaperConfig,
    pen_is_down: Union[bool, "PenState"],
) -> tuple[GCodeCommand, list[str], list[GCodeCommand]]:
    """Validate and fix a single command for live streaming.

    Returns:
        (fixed_cmd, warnings, prefix_commands)
        prefix_commands: any pen safety commands to insert BEFORE this command
            (e.g., M5 before a G0 travel, M3 before a G1 draw)
    """
    # Normalize PenState to bool for internal logic
    if isinstance(pen_is_down, PenState):
        pen_is_down = pen_is_down.is_down

    warnings: list[str] = []
    prefix: list[GCodeCommand] = []

    # Clamp coordinates: G1 draw → drawable area; G0 travel → machine extents.
    x0, y0, x1, y1 = paper.get_drawable_area()
    if cmd.command == "G0":
        lx0, ly0, lx1, ly1 = 0.0, 0.0, paper.width, paper.height
    else:
        lx0, ly0, lx1, ly1 = x0, y0, x1, y1
    fixed_x = cmd.x
    fixed_y = cmd.y
    if cmd.x is not None and (cmd.x < lx0 or cmd.x > lx1):
        fixed_x = max(lx0, min(cmd.x, lx1))
        warnings.append(f"X={cmd.x:.1f} clamped to {fixed_x:.1f}")
    if cmd.y is not None and (cmd.y < ly0 or cmd.y > ly1):
        fixed_y = max(ly0, min(cmd.y, ly1))
        warnings.append(f"Y={cmd.y:.1f} clamped to {fixed_y:.1f}")

    if fixed_x != cmd.x or fixed_y != cmd.y:
        cmd = cmd.model_copy(update={"x": fixed_x, "y": fixed_y})

    # Pen safety: ensure pen is up before travel, down before draw
    if cmd.command == "G0" and pen_is_down:
        prefix.append(GCodeCommand(command="M5"))
        warnings.append("Inserted M5 before travel move")
    elif cmd.command == "G1" and not pen_is_down:
        s_val = 1000  # default; caller can override
        prefix.append(GCodeCommand(command="M3", s=s_val))
        warnings.append("Inserted M3 before draw move")

    return cmd, warnings, prefix


def validate_chunk(
    commands: List[GCodeCommand],
    prior_pen_state: "PenState",
    paper: PaperConfig,
) -> Tuple[List[GCodeCommand], List[str], "PenState"]:
    """Validate a sequence of commands, threading pen state and clamping bounds.

    Returns (fixed_commands, warnings, final_pen_state).
    """
    pen = PenState(prior_pen_state.state) if isinstance(prior_pen_state, PenState) else PenState()
    out: List[GCodeCommand] = []
    all_warnings: List[str] = []
    for cmd in commands:
        if cmd.command in ("M3", "M5"):
            out.append(cmd)
            if cmd.command == "M3":
                pen.set_down()
            else:
                pen.set_up()
            continue
        fixed, warns, prefix = validate_single_command(cmd, paper, pen)
        for p in prefix:
            out.append(p)
            if p.command == "M3":
                pen.set_down()
            elif p.command == "M5":
                pen.set_up()
        out.append(fixed)
        all_warnings.extend(warns)
    return out, all_warnings, pen


# ---------------------------------------------------------------------------
# 0.5 Arc Approximation (G2/G3 → G1 segments)
# ---------------------------------------------------------------------------


def approximate_arcs(program: GCodeProgram, segments_per_arc: int = 12) -> GCodeProgram:
    """Convert G2/G3 arc commands to short G1 line segments.

    If the LLM generates arc commands despite instructions, this converts
    them to linear approximations that all plotters can execute.
    """
    has_arcs = any(cmd.command in ("G2", "G3") for cmd in program.commands)
    if not has_arcs:
        return program

    new_commands: List[GCodeCommand] = []
    cx, cy = 0.0, 0.0  # current position

    for cmd in program.commands:
        if cmd.command not in ("G2", "G3"):
            # Track position
            if cmd.command in ("G0", "G1") and cmd.x is not None:
                cx = cmd.x
            if cmd.command in ("G0", "G1") and cmd.y is not None:
                cy = cmd.y
            new_commands.append(cmd)
            continue

        # Arc approximation
        ex = cmd.x if cmd.x is not None else cx
        ey = cmd.y if cmd.y is not None else cy
        feed = cmd.f or 2000

        # Simple linear interpolation for arc (chord approximation)
        # Without I/J center offsets we just interpolate from current to end
        for i in range(1, segments_per_arc + 1):
            t = i / segments_per_arc
            ix = cx + (ex - cx) * t
            iy = cy + (ey - cy) * t
            new_commands.append(GCodeCommand(command="G1", x=round(ix, 3), y=round(iy, 3), f=feed))

        cx, cy = ex, ey

    return GCodeProgram(
        commands=new_commands,
        metadata={**(program.metadata or {}), "arcs_approximated": True},
    )


# ---------------------------------------------------------------------------
# 1. Pen Safety
# ---------------------------------------------------------------------------


def ensure_pen_safety(
    commands: List[GCodeCommand], pen_config: PenConfig = None
) -> List[GCodeCommand]:
    """Enforce pen safety invariants on LLM-generated GCode.

    Uses pen_config.pen_down_s_value (default 1000) instead of hardcoded S100.
    """
    s_value = pen_config.pen_down_s_value if pen_config else 1000
    result: List[GCodeCommand] = []
    pen_state = PenState()

    if not commands or commands[0].command != "M5":
        result.append(GCodeCommand(command="M5"))

    for cmd in commands:
        if cmd.command == "M3":
            pen_state.set_down()
            result.append(cmd)
        elif cmd.command == "M5":
            pen_state.set_up()
            result.append(cmd)
        elif cmd.command == "G0":
            if pen_state.is_down:
                result.append(GCodeCommand(command="M5"))
                pen_state.set_up()
            result.append(cmd)
        elif cmd.command == "G1":
            if pen_state.is_up:
                result.append(GCodeCommand(command="M3", s=s_value))
                pen_state.set_down()
            result.append(cmd)
        else:
            result.append(cmd)

    if pen_state.is_down:
        result.append(GCodeCommand(command="M5"))

    last_g0 = None
    for cmd in reversed(result):
        if cmd.command == "G0":
            last_g0 = cmd
            break
    if last_g0 is None or (last_g0.x != 0.0 or last_g0.y != 0.0):
        result.append(GCodeCommand(command="G0", x=0.0, y=0.0))

    return result


# ---------------------------------------------------------------------------
# 2. Stroke Optimization (nearest-neighbor reorder)
# ---------------------------------------------------------------------------


def extract_strokes(commands: List[GCodeCommand]) -> List[List[GCodeCommand]]:
    """Extract individual strokes (G0 + M3 ... G1s ... M5) from a command list.

    Every stroke starts with a ``G0`` to the position the pen actually goes
    down at, so it can be reordered safely. That position is tracked from all
    preceding motion rather than taken from the last ``G0`` seen, because:

    - a Z-only ``G0`` (``G0 Z5``) between the XY travel and ``M3`` carries no
      XY, and
    - a stroke can start with ``M5``/``M3`` and no travel at all (the pen is
      re-lowered where the previous stroke ended).

    Using the last ``G0`` in either case made the reordered program draw a line
    from wherever the previous stroke ended to the first ``G1`` (ink that was
    never in the original drawing). Commands outside strokes (dwells, Z moves,
    comments) are dropped; the pipeline re-inserts dwells afterwards.
    """
    strokes: List[List[GCodeCommand]] = []
    current: List[GCodeCommand] = []
    pen_state = PenState()
    x, y = 0.0, 0.0

    for cmd in commands:
        if cmd.command == "M3":
            if pen_state.is_down and current:
                continue  # redundant M3 while already drawing — keep the stroke going
            pen_state.set_down()
            current = [GCodeCommand(command="G0", x=x, y=y), cmd]
        elif cmd.command == "M5":
            if current:
                current.append(cmd)
                strokes.append(current)
                current = []
            pen_state.set_up()
        elif cmd.command in ("G0", "G1"):
            if pen_state.is_down and cmd.command == "G1":
                current.append(cmd)
            if cmd.x is not None:
                x = cmd.x
            if cmd.y is not None:
                y = cmd.y

    if current:
        current.append(GCodeCommand(command="M5"))
        strokes.append(current)

    return strokes


def _stroke_points(stroke: List[GCodeCommand]) -> List[Tuple[float, float]]:
    """Resolved XY of the pen-down point followed by every G1 endpoint.

    Partial coordinates (``G1 X5`` with no Y) inherit the previous value, so
    the returned points are what the plotter actually visits.
    """
    pts: List[Tuple[float, float]] = []
    x = y = None
    for cmd in stroke:
        if cmd.command not in ("G0", "G1"):
            continue
        x = cmd.x if cmd.x is not None else x
        y = cmd.y if cmd.y is not None else y
        if x is None or y is None:
            continue
        if cmd.command == "G0":
            pts = [(x, y)]  # the last G0 before ink is the start
        else:
            pts.append((x, y))
    return pts or [(0.0, 0.0)]


def _stroke_start(stroke: List[GCodeCommand]) -> Tuple[float, float]:
    return _stroke_points(stroke)[0]


def _stroke_end(stroke: List[GCodeCommand]) -> Tuple[float, float]:
    return _stroke_points(stroke)[-1]


def _distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def _is_reversible(stroke: List[GCodeCommand]) -> bool:
    """True for the canonical ``[G0 X Y, M3, G1..., M5]`` shape with XY-only G1s."""
    return (
        len(stroke) >= 4
        and stroke[0].command == "G0"
        and stroke[0].x is not None
        and stroke[0].y is not None
        and stroke[1].command == "M3"
        and stroke[-1].command == "M5"
        and all(c.command == "G1" and c.z is None for c in stroke[2:-1])
    )


def reverse_stroke(stroke: List[GCodeCommand]) -> List[GCodeCommand]:
    """Return the same stroke drawn end-to-start (identical ink).

    Each G1 keeps the feed/colour/comment of the segment it now draws in the
    opposite direction. Non-canonical strokes are returned unchanged.
    """
    if not _is_reversible(stroke):
        return stroke
    pts = _stroke_points(stroke)
    g1s = stroke[2:-1]
    out = [stroke[0].model_copy(update={"x": pts[-1][0], "y": pts[-1][1]}), stroke[1]]
    for i in range(len(g1s) - 1, -1, -1):
        out.append(g1s[i].model_copy(update={"x": pts[i][0], "y": pts[i][1]}))
    out.append(stroke[-1])
    return out


def _order_travel(
    strokes: List[List[GCodeCommand]], start: Tuple[float, float] = (0.0, 0.0)
) -> float:
    """Pen-up travel (mm) needed to draw ``strokes`` in the given order."""
    total, pos = 0.0, start
    for s in strokes:
        pts = _stroke_points(s)
        total += _distance(pos, pts[0])
        pos = pts[-1]
    return total


def _nearest_neighbor(
    strokes: List[List[GCodeCommand]], start: Tuple[float, float], allow_reverse: bool
) -> List[List[GCodeCommand]]:
    """Greedy nearest-neighbour tour over stroke endpoints.

    Endpoints are bucketed in a uniform grid so each lookup scans only nearby
    cells (rings grow until no closer endpoint can exist). This keeps dense
    generator output (thousands of strokes) fast where a full O(n^2) scan was
    the cost. Ties break on (distance, stroke index, start-before-end), so the
    result is deterministic.
    """
    n = len(strokes)
    ends = []  # (stroke idx, use_reversed, point)
    for i, s in enumerate(strokes):
        pts = _stroke_points(s)
        ends.append((i, False, pts[0]))
        if allow_reverse and pts[-1] != pts[0] and _is_reversible(s):
            ends.append((i, True, pts[-1]))

    xs = [e[2][0] for e in ends]
    ys = [e[2][1] for e in ends]
    minx, miny = min(xs), min(ys)
    span = max(max(xs) - minx, max(ys) - miny, 1e-6)
    cell = max(span / max(1.0, math.sqrt(n)), 1e-6)
    grid: dict = {}
    for e in ends:
        key = (int((e[2][0] - minx) // cell), int((e[2][1] - miny) // cell))
        grid.setdefault(key, []).append(e)
    max_k = max(k for key in grid for k in key) + 1

    used = [False] * n
    ordered: List[List[GCodeCommand]] = []
    pos = start
    for _ in range(n):
        cx = int(math.floor((pos[0] - minx) / cell))
        cy = int(math.floor((pos[1] - miny) / cell))
        # rings needed to reach every occupied cell from (cx, cy)
        reach = max(abs(cx), abs(cy), abs(cx - max_k), abs(cy - max_k)) + 1
        best = None
        for r in range(reach + 1):
            for gx in range(cx - r, cx + r + 1):
                for gy in (range(cy - r, cy + r + 1) if gx in (cx - r, cx + r) else (cy - r, cy + r)):
                    bucket = grid.get((gx, gy))
                    if not bucket:
                        continue
                    live = [e for e in bucket if not used[e[0]]]
                    if len(live) != len(bucket):
                        grid[(gx, gy)] = live
                    for e in live:
                        cand = (_distance(pos, e[2]), e[0], e[1])
                        if best is None or cand < best:
                            best = cand
            # unseen cells are at least r*cell away
            if best is not None and best[0] <= r * cell:
                break
        _, idx, rev = best
        used[idx] = True
        stroke = reverse_stroke(strokes[idx]) if rev else strokes[idx]
        ordered.append(stroke)
        pos = _stroke_points(stroke)[-1]
    return ordered


def optimize_stroke_order(
    strokes: List[List[GCodeCommand]],
    start: Tuple[float, float] = (0.0, 0.0),
    allow_reverse: bool = True,
) -> List[List[GCodeCommand]]:
    """Reorder (and optionally reverse) strokes to cut pen-up travel.

    Nearest-neighbour from ``start``; a stroke may be drawn end-to-start when
    that endpoint is closer. Greedy NN can lose to an already well-ordered
    input (e.g. a maze emitted cell by cell), so the input order is kept
    whenever it needs no more travel. Ink is never changed, only its order and
    direction.
    """
    if len(strokes) <= 1:
        return strokes
    ordered = _nearest_neighbor(strokes, start, allow_reverse)
    if _order_travel(ordered, start) >= _order_travel(strokes, start):
        return strokes
    return ordered


def merge_contiguous_strokes(
    strokes: List[List[GCodeCommand]], tol: float = 1e-3
) -> List[List[GCodeCommand]]:
    """Join consecutive strokes where one starts where the previous ended.

    Drops the ``M5 / G0 / M3`` between them, so the pen stays down: fewer pen
    lifts and dwells with identical ink. Strokes of different colours are never
    joined.
    """
    if not strokes:
        return strokes
    merged = [list(strokes[0])]
    for s in strokes[1:]:
        prev = merged[-1]
        if (
            _is_reversible(s)
            and prev[-1].command == "M5"
            and _stroke_color(prev, -1) == _stroke_color(s, -1)
            and _distance(_stroke_end(prev), _stroke_start(s)) <= tol
        ):
            merged[-1] = prev[:-1] + s[2:]
        else:
            merged.append(list(s))
    return merged


def rebuild_program(strokes: List[List[GCodeCommand]]) -> List[GCodeCommand]:
    """Rebuild a full command list from ordered strokes.

    Strokes carry their G0 travel command as the first element, so no
    separate G0 is added here — the included G0 IS the repositioning move.
    """
    commands: List[GCodeCommand] = [GCodeCommand(command="M5")]
    for stroke in strokes:
        commands.extend(stroke)
    if not commands or commands[-1].command != "M5":
        commands.append(GCodeCommand(command="M5"))
    commands.append(GCodeCommand(command="G0", x=0.0, y=0.0))
    return commands


def optimize_gcode_program(program: GCodeProgram, merge: bool = True) -> GCodeProgram:
    """Optimize stroke order to minimize travel distance.

    With ``merge`` (default), strokes that end where the next one starts are
    joined so the pen is not lifted between them.
    """
    strokes = extract_strokes(program.commands)
    if len(strokes) <= 1:
        return program
    ordered = optimize_stroke_order(strokes)
    if merge:
        ordered = merge_contiguous_strokes(ordered)
    optimized = rebuild_program(ordered)
    return GCodeProgram(
        commands=optimized,
        metadata={
            **(program.metadata or {}),
            "optimized": True,
            "original_stroke_count": len(strokes),
            "optimization_method": "nearest_neighbor",
        },
    )


# ---------------------------------------------------------------------------
# 2b. Multi-color layering (group strokes by pen color)
# ---------------------------------------------------------------------------


def _stroke_color(stroke: List[GCodeCommand], default: int = 0) -> int:
    """Color index of a stroke, taken from its first colored M3/G1 command."""
    for c in stroke:
        if c.command in ("M3", "G1") and c.color is not None:
            return c.color
    return default


def group_strokes_by_color(commands, color_config):
    """Bucket strokes by pen color, preserving ascending color order.

    In ``round_robin`` mode, colors are assigned by stroke index
    (``strokes_before_swap`` strokes per color) instead of read from commands.
    Returns ``(buckets, color_sequence)``.
    """
    strokes = extract_strokes(commands)
    n_colors = max(1, len(color_config.palette))

    if color_config.assign_mode == "round_robin" and color_config.strokes_before_swap > 0:
        per = color_config.strokes_before_swap
        for i, stroke in enumerate(strokes):
            ci = (i // per) % n_colors
            for c in stroke:
                if c.command in ("M3", "G1"):
                    c.color = ci

    buckets: dict = {}
    for stroke in strokes:
        ci = _stroke_color(stroke, 0)
        buckets.setdefault(ci, []).append(stroke)
    color_sequence = sorted(buckets.keys())
    return buckets, color_sequence


def reorder_by_color(program: GCodeProgram, color_config, merge: bool = True) -> GCodeProgram:
    """Order the program by color layer, optimizing strokes WITHIN each color.

    All strokes of color 0 are emitted, then color 1, etc. Stroke reordering
    never crosses a color boundary. Streaming re-derives the layers by scanning
    each command's ``.color`` (robust to later dip/dwell insertion).
    """
    buckets, color_sequence = group_strokes_by_color(program.commands, color_config)
    if len(color_sequence) <= 1:
        # Single (or no) color — fall back to plain optimization.
        return optimize_gcode_program(program, merge=merge)

    commands: List[GCodeCommand] = [GCodeCommand(command="M5")]
    pos = (0.0, 0.0)
    for ci in color_sequence:
        ordered = optimize_stroke_order(buckets[ci], start=pos)
        if merge:
            ordered = merge_contiguous_strokes(ordered)
        for stroke in ordered:
            commands.extend(stroke)
        pos = _stroke_end(ordered[-1])
    if not commands or commands[-1].command != "M5":
        commands.append(GCodeCommand(command="M5"))
    commands.append(GCodeCommand(command="G0", x=0.0, y=0.0))

    return GCodeProgram(
        commands=commands,
        metadata={
            **(program.metadata or {}),
            "optimized": True,
            "optimization_method": "per_color_nearest_neighbor",
            "color_sequence": color_sequence,
            "palette": list(color_config.palette),
        },
    )


# ---------------------------------------------------------------------------
# 3. Brush / Paint Dip Insertion
# ---------------------------------------------------------------------------


def insert_paint_dips(program: GCodeProgram, brush_config: BrushConfig) -> GCodeProgram:
    """Insert ink reload sequences every N strokes.

    Sequence: M5 -> G0 to station -> G0 Z(dip_height) -> G4 hold -> G0 Z5 -> G4 drip -> resume
    """
    if not brush_config.enabled or brush_config.strokes_before_reload <= 0:
        return program

    commands: List[GCodeCommand] = []
    stroke_count = 0
    cx, cy = brush_config.charge_position
    fw = getattr(brush_config, "firmware", "grbl")
    dip_p = _dwell_p(brush_config.dip_duration, fw) or 0
    drip_p = _dwell_p(brush_config.drip_duration, fw) or 0

    for cmd in program.commands:
        if cmd.command == "M3":
            stroke_count += 1
            if stroke_count % brush_config.strokes_before_reload == 0:
                # Insert reload before this pen-down
                commands.append(GCodeCommand(command="M5"))
                commands.append(GCodeCommand(command="G0", x=cx, y=cy))
                commands.append(
                    GCodeCommand(
                        command="G0",
                        z=brush_config.dip_height,
                        comment="dip into ink",
                    )
                )
                commands.append(GCodeCommand(command="G4", p=dip_p, comment="hold in ink"))
                commands.append(GCodeCommand(command="G0", z=5.0, comment="lift"))
                commands.append(GCodeCommand(command="G4", p=drip_p, comment="drip"))
        commands.append(cmd)

    return GCodeProgram(
        commands=commands,
        metadata={
            **(program.metadata or {}),
            "brush_reloads": stroke_count // brush_config.strokes_before_reload,
        },
    )


# ---------------------------------------------------------------------------
# 4. Pen Dwell Injection (G4 after M3/M5)
# ---------------------------------------------------------------------------


def _dwell_p(seconds: float, firmware: str):
    """Return the right P value for G4 — Grbl reads seconds, Marlin reads ms."""
    if seconds <= 0:
        return None
    if firmware == "marlin":
        return int(seconds * 1000)
    return float(seconds)


def _dwell_p_values(pen_config: PenConfig):
    fw = getattr(pen_config, "firmware", "grbl")
    return _dwell_p(pen_config.pen_down_delay, fw), _dwell_p(pen_config.pen_up_delay, fw)


def insert_pen_dwells(program: GCodeProgram, pen_config: PenConfig) -> GCodeProgram:
    """Insert G4 dwell commands after every M3 and M5.

    Skips insertion when the corresponding delay is 0.
    """
    down_p, up_p = _dwell_p_values(pen_config)

    if not down_p and not up_p:
        return program

    commands: List[GCodeCommand] = []
    for cmd in program.commands:
        commands.append(cmd)
        if cmd.command == "M3" and down_p:
            commands.append(GCodeCommand(command="G4", p=down_p, comment="pen down dwell"))
        elif cmd.command == "M5" and up_p:
            commands.append(GCodeCommand(command="G4", p=up_p, comment="pen up dwell"))

    return GCodeProgram(
        commands=commands,
        metadata={**(program.metadata or {}), "dwells_inserted": True},
    )


# ---------------------------------------------------------------------------
# Full Pipeline
# ---------------------------------------------------------------------------


def run_pipeline(program: GCodeProgram, config: PromptPlotConfig) -> GCodeProgram:
    """Run the full post-processing pipeline in the correct order.

    Order:
    0. Bounds validation (clamp/reject/warn out-of-bounds coordinates)
    1. Pen safety (fix state violations, use configurable S-value)
    2. Stroke optimization (nearest-neighbor reorder)
    3. Paint dips (brush mode only)
    4. Pen dwells (G4 after M3/M5 — MUST be last)
    """
    # 0. Arc approximation (convert G2/G3 to G1 segments)
    program = approximate_arcs(program)

    # 0.5 Bounds validation
    if config.bounds.enforce:
        program, violations = validate_bounds(program, config.paper, config.bounds.mode)
        if violations:
            _log.info(
                "Bounds validation (%s mode): %d violations", config.bounds.mode, len(violations)
            )

    # 1. Pen safety
    safe_commands = ensure_pen_safety(program.commands, config.pen)
    program = GCodeProgram(commands=safe_commands, metadata=program.metadata)

    # 2. Optimize stroke order (per-color when multi-color layering is enabled,
    #    so strokes are grouped by pen and never reordered across a color)
    #    Merging contiguous strokes is skipped in brush mode, where each pen-down
    #    is a stroke that insert_paint_dips counts towards the next reload.
    merge = not config.brush.enabled
    if getattr(config, "color", None) is not None and config.color.enabled:
        program = reorder_by_color(program, config.color, merge=merge)
    else:
        program = optimize_gcode_program(program, merge=merge)

    # 3. Brush reload sequences
    if config.brush.enabled:
        program = insert_paint_dips(program, config.brush)

    # 4. Pen dwells (last!)
    program = insert_pen_dwells(program, config.pen)

    return program
