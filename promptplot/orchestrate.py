"""
Orchestration API for PromptPlot v3.0

Pure-function public API for the Claude Code controller: plan regions,
generate per region, validate, score, merge, stream — no global state.
"""

import asyncio
import json
import math
from typing import Any, Callable, List, Optional, Tuple

from .models import (
    GCodeCommand,
    GCodeProgram,
    DrawProgram,
    DrawCommand,
    Region,
    ChunkMetrics,
)
from .config import PromptPlotConfig
from .engine import PenState
from .postprocess import validate_chunk as _validate_chunk_pp, run_pipeline
from .scoring import score_chunk as _score_chunk_s
from .pipeline import load_and_continue as _load_and_continue
from .llm import build_region_worker_prompt
from .plotter import BasePlotter


def plan_regions(
    bounds: Tuple[float, float, float, float],
    strategy: str = "grid_2x2",
    composition_plan: Optional[Any] = None,
) -> List[Region]:
    """Partition a rectangular canvas into work regions."""
    x0, y0, x1, y1 = bounds
    w = x1 - x0
    h = y1 - y0

    if strategy == "composition_plan":
        if composition_plan is None or not hasattr(composition_plan, "regions"):
            raise ValueError("composition_plan strategy requires a plan with .regions")
        out: List[Region] = []
        for r in composition_plan.regions:
            rx0 = float(r.x)
            ry0 = float(r.y)
            rx1 = rx0 + float(r.width)
            ry1 = ry0 + float(r.height)
            density = getattr(r, "density", "medium")
            if density not in ("sparse", "medium", "dense", "saturated"):
                density = "medium"
            role = getattr(r, "role", "support")
            out.append(
                Region(
                    bounds=(rx0, ry0, rx1, ry1),
                    role=role,
                    target_density=density,
                    target_command_count=1500,
                    name=getattr(r, "name", None),
                )
            )
        return out

    if strategy == "grid_2x2" or strategy == "quadrant":
        mx = x0 + w / 2
        my = y0 + h / 2
        return [
            Region(bounds=(x0, my, mx, y1), role="support", name="top_left"),
            Region(bounds=(mx, my, x1, y1), role="support", name="top_right"),
            Region(bounds=(x0, y0, mx, my), role="support", name="bottom_left"),
            Region(bounds=(mx, y0, x1, my), role="support", name="bottom_right"),
        ]

    if strategy == "grid_3x3":
        dx = w / 3
        dy = h / 3
        regions: List[Region] = []
        for ix in range(3):
            for iy in range(3):
                rx0 = x0 + ix * dx
                ry0 = y0 + iy * dy
                role = "focal" if (ix == 1 and iy == 1) else "support"
                regions.append(
                    Region(
                        bounds=(rx0, ry0, rx0 + dx, ry0 + dy),
                        role=role,
                        name=f"cell_{ix}_{iy}",
                    )
                )
        return regions

    if strategy == "radial":
        cx = x0 + w / 2
        cy = y0 + h / 2
        r_outer = min(w, h) / 2
        r_inner = r_outer * 0.4
        center_half = r_inner
        regions: List[Region] = [
            Region(
                bounds=(cx - center_half, cy - center_half, cx + center_half, cy + center_half),
                role="focal",
                name="center",
            ),
        ]
        for i, (sx, sy, name) in enumerate(
            [
                (x0, cy, "left"),
                (cx, cy, "right"),
                (x0, y0, "bottom"),
                (x0, cy, "top"),
            ]
        ):
            pass
        # Surround: 4 quadrants minus the focal center
        mx = cx
        my = cy
        for bx0, by0, bx1, by1, nm in [
            (x0, my, mx, y1, "ring_tl"),
            (mx, my, x1, y1, "ring_tr"),
            (x0, y0, mx, my, "ring_bl"),
            (mx, y0, x1, my, "ring_br"),
        ]:
            regions.append(
                Region(
                    bounds=(bx0, by0, bx1, by1),
                    role="support",
                    name=nm,
                )
            )
        return regions

    raise ValueError(f"Unknown strategy: {strategy}")


def validate_chunk(
    commands: List[GCodeCommand],
    prior_pen_state: PenState,
    paper,
) -> Tuple[List[GCodeCommand], List[str], PenState]:
    return _validate_chunk_pp(commands, prior_pen_state, paper)


def score_chunk(commands: List[GCodeCommand], region: Region) -> ChunkMetrics:
    return _score_chunk_s(commands, region)


def load_and_continue(
    prior_gcode_path: str, new_commands: list, config: PromptPlotConfig
) -> GCodeProgram:
    return _load_and_continue(prior_gcode_path, new_commands, config)


def _clamp_to_region(cmd: GCodeCommand, region: Region) -> GCodeCommand:
    x0, y0, x1, y1 = region.bounds
    nx = cmd.x
    ny = cmd.y
    if nx is not None and (nx < x0 or nx > x1):
        nx = max(x0, min(nx, x1))
    if ny is not None and (ny < y0 or ny > y1):
        ny = max(y0, min(ny, y1))
    if nx != cmd.x or ny != cmd.y:
        return cmd.model_copy(update={"x": nx, "y": ny})
    return cmd


def _parse_worker_response(text: str, config: PromptPlotConfig) -> List[GCodeCommand]:
    """Parse worker LLM response into raw GCodeCommands (expanding primitives)."""
    s = text.strip()
    if "```" in s:
        # strip markdown fences
        if "```json" in s:
            s = s.split("```json", 1)[1]
        else:
            s = s.split("```", 1)[1]
        s = s.rsplit("```", 1)[0].strip()
    start = s.find("{")
    end = s.rfind("}") + 1
    if start < 0 or end <= start:
        return []
    data = json.loads(s[start:end])
    if "commands" not in data:
        return []

    has_structured = any(
        isinstance(c, dict) and c.get("command") in {"PRIMITIVE", "FREEFORM"}
        for c in data["commands"]
    )
    if has_structured:
        from .primitives import expand_primitives

        dp = DrawProgram(**data)
        gp = expand_primitives(dp, config.pen)
        return list(gp.commands)
    return [GCodeCommand(**c) for c in data["commands"]]


async def generate_region(
    prompt: str,
    region: Region,
    llm: Any,
    config: PromptPlotConfig,
    plan_context: Optional[str] = None,
) -> List[GCodeCommand]:
    """Single worker call constrained to region.bounds. Returns clamped commands."""
    worker_prompt = build_region_worker_prompt(prompt, region, config, plan_context=plan_context)
    try:
        response = await llm.acomplete(worker_prompt)
    except Exception as e:
        import logging

        logging.warning("region %s LLM call failed: %r", region.name, e)
        return []
    try:
        cmds = _parse_worker_response(response, config)
    except Exception as e:
        import logging

        logging.warning(
            "region %s parse failed: %r; head=%r", region.name, e, (response or "")[:300]
        )
        cmds = []
    if not cmds:
        import logging

        logging.warning(
            "region %s produced 0 commands; response head=%r", region.name, (response or "")[:300]
        )
    return [_clamp_to_region(c, region) for c in cmds]


def merge_chunks(
    chunks: List[List[GCodeCommand]],
    config: PromptPlotConfig,
) -> GCodeProgram:
    """Concat chunks with pen-up separators, then run the full postprocess pipeline."""
    merged: List[GCodeCommand] = [GCodeCommand(command="M5")]
    for chunk in chunks:
        if not chunk:
            continue
        if merged[-1].command != "M5":
            merged.append(GCodeCommand(command="M5"))
        merged.extend(chunk)
    if not merged or merged[-1].command != "M5":
        merged.append(GCodeCommand(command="M5"))
    program = GCodeProgram(commands=merged, metadata={"merged_chunks": len(chunks)})
    return run_pipeline(program, config)


class PauseSignal(Exception):
    """Raised when stream_chunk hands control back to the orchestrator."""


async def stream_chunk(
    commands: List[GCodeCommand],
    plotter: BasePlotter,
    on_pause: Optional[Callable[[int, int], Any]] = None,
    verbose: bool = False,
    enforce_pen_state: bool = True,
    settle_dwell: float = 0.3,
) -> Tuple[int, int]:
    """Stream a chunk to the plotter, then optionally invoke on_pause.

    GUARDRAIL (``enforce_pen_state``, on by default): the pen convention is
    ``G0`` = rapid travel (pen must be UP) and ``G1`` = draw (pen must be DOWN).
    This tracks pen state from ``M3``/``M5`` and, if a command would violate it,
    injects the missing lift/lower (plus a short ``settle_dwell``) BEFORE the
    move. So a travel can never be inked and a draw can never float — even if the
    upstream g-code forgot an ``M5``/``M3`` or mis-ordered a stroke. The pen
    convention is load-bearing: never emit ``G1`` for a pen-up move (use ``G0``),
    or the guardrail will (correctly) drop the pen onto it.
    """
    success = 0
    errors = 0
    total = len(commands)
    pen_down = False  # plotter homes/enters chunks pen-up

    async def _send(g: str) -> bool:
        if g == "COMPLETE":
            return True
        return await plotter.send_command(g)

    for i, cmd in enumerate(commands):
        gcode = cmd.to_gcode()
        if gcode == "COMPLETE":
            continue
        name = cmd.command
        if enforce_pen_state:
            if name == "G0" and cmd.x is not None and pen_down:
                # travel with pen down → lift + settle first
                await _send(GCodeCommand(command="M5").to_gcode())
                if settle_dwell > 0:
                    await _send(GCodeCommand(command="G4", p=settle_dwell).to_gcode())
                pen_down = False
            elif name == "G1" and cmd.x is not None and not pen_down:
                # draw with pen up → lower + settle first
                await _send(GCodeCommand(command="M3", s=1000).to_gcode())
                if settle_dwell > 0:
                    await _send(GCodeCommand(command="G4", p=settle_dwell).to_gcode())
                pen_down = True
        ok = await _send(gcode)
        if enforce_pen_state:
            if name == "M3":
                pen_down = True
            elif name == "M5":
                pen_down = False
        if ok:
            success += 1
        else:
            errors += 1
        if verbose:
            tag = "ok" if ok else "ERR"
            print(f"[{i+1:5d} / {total}]  {gcode:<44}  ->  {tag}", flush=True)
    if on_pause is not None:
        result = on_pause(success, errors)
        if asyncio.iscoroutine(result):
            await result
    return success, errors


def split_color_layers(program: GCodeProgram) -> List[Tuple[int, List[GCodeCommand]]]:
    """Split a program into contiguous same-color layers by scanning ``.color``.

    Non-drawing commands (M5, travel, dwells) with no color attach to the
    current layer. Returns ``[(color_index, commands), ...]`` in draw order.

    GUARDRAIL: on a colour switch, the trailing pen-up block (the M5 + G0/G1
    travel + dwells that reposition the head for the *next* colour's first
    stroke) is moved to the FRONT of the new layer. Without this, streaming a
    single layer on its own would begin with ``M3`` (pen down) at whatever
    position the head is parked at and drag a line to the first real stroke —
    the pen never gets a chance to travel there with the pen up. Keeping the
    repositioning travel attached to the layer it serves makes every layer
    safe to stream in isolation (per-pen swaps) through any code path.
    Concatenating the returned layers in order reproduces the input exactly.
    """
    def _is_penup_tail(cmd: GCodeCommand) -> bool:
        # travel / lift / dwell that carries no colour → belongs to the NEXT stroke
        return cmd.command in ("M5", "G0", "G4") or (
            cmd.command == "G1" and getattr(cmd, "color", None) is None
        )

    layers: List[Tuple[int, List[GCodeCommand]]] = []
    current_color: Optional[int] = None
    current: List[GCodeCommand] = []
    for cmd in program.commands:
        c = getattr(cmd, "color", None)
        if c is not None and c != current_color:
            if current and current_color is not None:
                # peel the trailing pen-up block into the incoming layer
                k = len(current)
                while k > 0 and _is_penup_tail(current[k - 1]):
                    k -= 1
                head, tail = current[:k], current[k:]
                layers.append((current_color, head))
                current = tail
            current_color = c
        current.append(cmd)
    if current:
        layers.append((current_color if current_color is not None else 0, current))
    return layers


def _first_drawn_point(
    cmds: List[GCodeCommand],
) -> Optional[Tuple[float, float]]:
    """Position where the pen first goes DOWN in ``cmds`` (the coordinate that
    precedes the first ``M3``). Returns None if the chunk never lowers the pen
    or has no positioning move — used to guarantee a pen-up travel before the
    first stroke so no layer can drag from the park/home position."""
    last_xy: Optional[Tuple[float, float]] = None
    for c in cmds:
        if c.command == "M3":
            return last_xy
        if c.x is not None:
            last_xy = (c.x, c.y)
    return None


async def trace_frame(plotter: BasePlotter, paper, laps: int = 1, dwell: float = 0.4) -> None:
    """Pen-UP tour of the drawable-area corners so the user can see the limits.

    A mandatory guardrail before physically plotting: leaves no marks (pen stays
    up), just moves the head around the perimeter of ``paper.get_drawable_area()``.
    """
    x0, y0, x1, y1 = paper.get_drawable_area()
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    await plotter.send_command("M5")  # ensure pen up for the whole trace
    for _ in range(max(1, laps)):
        for x, y in corners:
            await plotter.send_command(f"G0 X{x:.1f} Y{y:.1f}")
            if dwell > 0:
                await plotter.send_command(f"G4 P{dwell:g}")


async def _wait_for_keypress(message: str) -> None:
    """Block (without freezing the event loop) until the user presses Enter."""
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, input, message)
    except (EOFError, KeyboardInterrupt):
        pass


async def stream_pen_layers(
    program: GCodeProgram,
    plotter: BasePlotter,
    config: PromptPlotConfig,
    on_swap: Optional[Callable[[int, str], Any]] = None,
    verbose: bool = False,
) -> Tuple[int, int]:
    """Stream a multi-color program, pausing for a manual pen swap between layers.

    Between color layers the pen lifts, parks at ``config.color.park_position``,
    and (unless ``on_swap`` is provided) blocks for a keypress before the next
    color. Single-layer programs stream straight through.
    """
    layers = split_color_layers(program)
    color_cfg = getattr(config, "color", None)
    palette = list(color_cfg.palette) if color_cfg else ["black"]
    park = color_cfg.park_position if color_cfg else (0.0, 0.0)
    pause = color_cfg.pause_for_swap if color_cfg else True

    total_ok = 0
    total_err = 0
    for i, (color, cmds) in enumerate(layers):
        name = palette[color] if 0 <= color < len(palette) else f"color {color}"
        if i > 0:
            await plotter.send_command(GCodeCommand(command="M5").to_gcode())
            await plotter.send_command(
                GCodeCommand(command="G0", x=float(park[0]), y=float(park[1])).to_gcode()
            )
            if on_swap is not None:
                result = on_swap(color, name)
                if asyncio.iscoroutine(result):
                    await result
            elif pause:
                await _wait_for_keypress(f"  ↻ Swap to '{name}' pen, then press Enter...")
        # GUARDRAIL: never drop the pen before it has travelled to the first
        # stroke. Lift, then rapid pen-up to the layer's first drawn point so a
        # leading M3 can never drag a line from the park/home position.
        first_xy = _first_drawn_point(cmds)
        if first_xy is not None:
            await plotter.send_command(GCodeCommand(command="M5").to_gcode())
            await plotter.send_command(
                GCodeCommand(command="G0", x=float(first_xy[0]), y=float(first_xy[1])).to_gcode()
            )
        if verbose:
            print(f"── color layer {i + 1}/{len(layers)}: {name} ({len(cmds)} cmds) ──", flush=True)
        ok, err = await stream_chunk(cmds, plotter, verbose=verbose)
        total_ok += ok
        total_err += err
    return total_ok, total_err


async def compose_and_stream(
    blocks: List[Any],
    plotter: BasePlotter,
    config: PromptPlotConfig,
    verbose: bool = True,
) -> Tuple[GCodeProgram, int, int]:
    """Claude-Code-as-LLM path: hand-built blocks -> expand -> validate -> postprocess -> stream.

    No intermediate .gcode file. `blocks` is a list of either:
      - DrawProgram instances
      - dicts with a "commands" key (PRIMITIVE / FREEFORM / raw GCode dicts)
      - lists of GCodeCommand
    """
    from .primitives import expand_primitives

    chunks: List[List[GCodeCommand]] = []
    for b in blocks:
        if isinstance(b, DrawProgram):
            dp = b
        elif isinstance(b, dict):
            dp = DrawProgram(**b)
        elif isinstance(b, list):
            chunks.append(b)
            continue
        else:
            raise TypeError(f"unsupported block type: {type(b).__name__}")
        gp = expand_primitives(dp, config.pen)
        chunks.append(list(gp.commands))
    program = merge_chunks(chunks, config)
    success, errors = await plotter.stream_program(program, verbose=verbose)
    return program, success, errors
