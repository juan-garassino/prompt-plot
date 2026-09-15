"""plot command group — the physical-plotting playbook, first-class.

``promptplot plot FILE``            → legacy full-file plot (moved verbatim)
``promptplot plot frame``           → MANDATORY pen-up frame trace (paper edge
                                      with a hold after the first edge, then
                                      the margin rectangle) — always run this
                                      before inking
``promptplot plot layer FILE [C]``  → stream ONE colour layer (optionally a
                                      stroke range batch) with the streaming
                                      guardrails: pen-state enforcement, pen-up
                                      approach to the first stroke, 60s acks,
                                      park at exactly (0, 0)
"""

import asyncio
from pathlib import Path

import click

from ._group import cli, console, _get_config


class _DefaultFileGroup(click.Group):
    """`promptplot plot foo.gcode` keeps working: an unknown first token that
    is an existing file dispatches to the legacy ``file`` subcommand."""

    def resolve_command(self, ctx, args):
        if args and args[0] not in self.commands and Path(args[0]).exists():
            return "file", self.commands["file"], args
        return super().resolve_command(ctx, args)


@cli.group(cls=_DefaultFileGroup, name="plot")
def plot_group():
    """Physical plotting: frame trace, full files, per-layer batches."""


@plot_group.command(name="file")
@click.argument("filepath")
@click.option("--port", default=None, help="Serial port")
@click.option("--baud", default=115200, help="Baud rate")
@click.option("--simulate", is_flag=True, help="Simulation mode")
@click.option("--brush", is_flag=True, help="Enable brush/ink mode")
@click.option("--preview-only", is_flag=True, help="Preview without plotting")
@click.option("--output", "-o", default=None, help="Preview output path")
def plot_file(filepath, port, baud, simulate, brush, preview_only, output):
    """Plot a GCode file to the plotter (the historical `plot` command)."""
    config = _get_config()
    if port:
        config.serial.port = port
    if baud:
        config.serial.baud_rate = baud
    if brush:
        config.brush.enabled = True

    async def _run():
        from ..pipeline import FilePipeline
        from ..plotter import SimulatedPlotter, SerialPlotter

        pipeline = FilePipeline(config)
        plotter = None
        if not preview_only:
            if simulate:
                plotter = SimulatedPlotter()
            else:
                plotter = SerialPlotter(
                    port=config.serial.port,
                    baud_rate=config.serial.baud_rate,
                    timeout=config.serial.timeout,
                )
        processed, success, errors = await pipeline.process_file(
            filepath, plotter=plotter, preview_only=preview_only, output_path=output
        )
        if not preview_only:
            console.print(f"[bold]streamed[/bold] → {success} ok, {errors} errors")

    asyncio.run(_run())


def _parse_paper(paper: str, margin: float):
    """'297x210' (mm), '17x24' (cm), or 'a4:landscape' → (width, height)."""
    from ..config import PaperConfig

    if ":" in paper:
        size, orient = paper.split(":", 1)
        pc = PaperConfig.from_size(size, orientation=orient, margin=margin)
    else:
        pc = PaperConfig.from_size(paper, orientation="landscape", margin=margin)
    return pc.width, pc.height


@plot_group.command(name="frame")
@click.option("--paper", default="a4:landscape", help="WxH (mm or cm) or size:orientation")
@click.option("--margin", default=15.0, type=float, help="Drawable margin (mm)")
@click.option("--dwell", default=0.4, type=float, help="Corner dwell (s)")
@click.option("--hold", default=1.2, type=float, help="Pause between edge and margin loops (s)")
@click.option("--edge-hold", "edge_hold", default=3.0, type=float, help="Hold after the FIRST edge (s)")
@click.option("--port", default=None, help="Serial port")
@click.option("--timeout", default=60.0, type=float, help="Serial ack timeout (s)")
def plot_frame(paper, margin, dwell, hold, edge_hold, port, timeout):
    """MANDATORY pre-plot guardrail: pen-up trace of paper edge + margin."""
    config = _get_config()
    if port:
        config.serial.port = port
    width, height = _parse_paper(paper, margin)

    async def _run():
        from ..orchestrate import trace_frame_full
        from ..plotter import SerialPlotter

        p = SerialPlotter(
            port=config.serial.port,
            baud_rate=config.serial.baud_rate,
            timeout=timeout,
            enable_heartbeat=False,
        )
        if not await p.connect():
            raise SystemExit(f"could not connect to {config.serial.port}")
        await trace_frame_full(p, width, height, margin, dwell=dwell, hold=hold, edge_hold=edge_hold)
        await p.disconnect()
        console.print(f"[green]frame traced ({width:g}x{height:g}, margin {margin:g}) — head home[/green]")

    asyncio.run(_run())


@plot_group.command(name="layer")
@click.argument("filepath")
@click.argument("color", required=False, type=int)
@click.option("--list", "list_only", is_flag=True, help="List colour layers and stroke counts")
@click.option("--strokes", default=None, help="Stroke range S:E within the layer (batching)")
@click.option("--port", default=None, help="Serial port")
@click.option("--timeout", default=60.0, type=float, help="Serial ack timeout (s)")
@click.option("--park", default="0,0", help="Park position after the layer (default exactly 0,0)")
@click.option("--dry-run", "dry_run", is_flag=True, help="Show what would stream, no hardware")
def plot_layer(filepath, color, list_only, strokes, port, timeout, park, dry_run):
    """Stream ONE colour layer (optionally a stroke-range batch), guardrailed."""
    from ..orchestrate import split_color_layers, stroke_spans, slice_stroke_range, _first_drawn_point
    from ..pipeline import FilePipeline

    config = _get_config()
    if port:
        config.serial.port = port
    program = FilePipeline(config).load_gcode_file(filepath)
    layers = split_color_layers(program)

    console.print("[bold]layers:[/bold]")
    for c, cmds in layers:
        console.print(f"  color {c}: {len(stroke_spans(cmds))} strokes, {len(cmds)} cmds")
    if list_only or color is None:
        return

    bucket = next((cmds for c, cmds in layers if c == color), None)
    if bucket is None:
        raise SystemExit(f"no layer with color {color}")
    if strokes:
        s, e = (int(v) for v in strokes.split(":", 1))
        bucket = slice_stroke_range(bucket, s, e)
        console.print(f"  batch strokes {s}..{e} → {len(bucket)} cmds")
    fp = _first_drawn_point(bucket)
    if dry_run:
        console.print(f"[cyan]dry-run:[/cyan] {len(bucket)} cmds, first pen-down at {fp}")
        return

    px, py = (float(v) for v in park.split(",", 1))

    async def _run():
        from ..orchestrate import stream_chunk
        from ..plotter import SerialPlotter

        p = SerialPlotter(
            port=config.serial.port,
            baud_rate=config.serial.baud_rate,
            timeout=timeout,
            enable_heartbeat=False,
        )
        if not await p.connect():
            raise SystemExit(f"could not connect to {config.serial.port}")
        await p.send_command("M5")
        if fp is not None:  # pen-up approach: a layer can never drag from home
            await p.send_command(f"G0 X{fp[0]:.3f} Y{fp[1]:.3f}")
            await p.send_command("G4 P1.0")
        ok, err = await stream_chunk(bucket, p, verbose=False)
        await p.send_command("M5")
        await p.send_command("G4 P1.0")
        await p.send_command(f"G0 X{px:g} Y{py:g}")
        await p.disconnect()
        console.print(f"[bold]color {color}[/bold] → {ok} ok, {err} errors — parked ({px:g},{py:g})")

    asyncio.run(_run())
