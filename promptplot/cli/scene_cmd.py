"""`promptplot scene` — compile an authored Scene JSON without an LLM in the loop.

This is the Claude-Code-in-conversation seat: author the Scene (see
studio/AUTHORING.md), then `promptplot scene render scene.json --out x.png`.
Same compiler, same pen plan, same preview as the in-app studio loop.
"""

from __future__ import annotations

import json
from pathlib import Path

import click

from ._group import cli, console, _get_config


@cli.group()
def scene():
    """Validate / render authored Scene JSON (promptplot.scene)."""


@scene.command("validate")
@click.argument("scene_json", type=click.Path(exists=True, dir_okay=False))
def scene_validate(scene_json):
    """Parse a Scene JSON and report objects, marks, inks, widths, stages."""
    from ..scene import Scene

    s = Scene.model_validate_json(Path(scene_json).read_text(encoding="utf-8"))
    n_marks = sum(len(o.marks) for o in s.objects)
    n_cover = sum(1 for o in s.objects if o.cover)
    console.print(f"[bold]{s.title or Path(scene_json).stem}[/bold]  canvas {s.canvas}  {s.paper} {s.orientation}")
    console.print(f"  objects {len(s.objects)} ({n_cover} with cover) · marks {n_marks}")
    console.print(f"  inks {list(s.inks)} · widths {s.widths_mm} mm · stages {s.stages} · occlusion {s.occlusion}")


@scene.command("render")
@click.argument("scene_json", type=click.Path(exists=True, dir_okay=False))
@click.option("--out", "out_png", default=None, help="Preview PNG (default: <stem>.png beside the input)")
@click.option("--gcode", "out_gcode", default=None, help="Save GCode here (default: <stem>.gcode beside --out)")
@click.option("--no-preview", is_flag=True, help="Skip the PNG")
@click.option("--simulate", is_flag=True, help="Stream to the simulated plotter")
@click.option("--port", default=None, help="Serial port (streams for real, layer by layer)")
def scene_render(scene_json, out_png, out_gcode, no_preview, simulate, port):
    """Compile a Scene JSON → colour-layered GCode + a preview at physical pen widths."""
    from ..scene import Scene, compile_to_program

    config = _get_config()
    src = Path(scene_json)
    s = Scene.model_validate_json(src.read_text(encoding="utf-8"))
    program, pen_plan = compile_to_program(s, config)
    passes = [p for p in pen_plan if "pen" in p]

    out_png = Path(out_png) if out_png else src.with_suffix(".png")
    out_gcode = Path(out_gcode) if out_gcode else out_png.with_suffix(".gcode")
    out_png.parent.mkdir(parents=True, exist_ok=True)

    out_gcode.write_text(program.to_gcode())
    (out_gcode.with_suffix(".pen_plan.json")).write_text(json.dumps(pen_plan, indent=2))
    console.print(f"[bold blue]scene[/bold blue]    → {s.title or src.stem}  ({len(s.objects)} objects)")
    console.print(f"[bold blue]commands[/bold blue] → {len(program.commands)}")
    for p in passes:
        console.print(f"  pen {p['pen']:2}  {p['stage']:14} {p['ink']:12} {p['hex']}  {p['width_mm']:g} mm  {p['strokes']} strokes")
    culled = [p for p in pen_plan if "culled_hidden_strokes" in p]
    if culled:
        console.print(f"  culled hidden strokes: {culled[0]['culled_hidden_strokes']}")
    console.print(f"[green]GCode saved to {out_gcode}[/green]")

    if not no_preview:
        try:
            from ..visualizer import GCodeVisualizer

            widths = {p["pen"]: float(p["width_mm"]) for p in passes}
            GCodeVisualizer(config).preview(program, str(out_png), pen_widths=widths)
            console.print(f"[green]Preview saved to {out_png}[/green]")
        except ImportError:
            console.print("[yellow]matplotlib not available — skipping preview[/yellow]")

    if simulate or port:
        import asyncio

        from ..orchestrate import stream_pen_layers
        from ..plotter import SerialPlotter, SimulatedPlotter

        config.color.pause_for_swap = not simulate
        if port:
            config.serial.port = port

        async def _run():
            if simulate:
                plotter = SimulatedPlotter()
                await plotter.connect()
            else:
                plotter = SerialPlotter(port=config.serial.port, baud_rate=config.serial.baud_rate)
                if not await plotter.connect():
                    console.print(f"[red]Could not connect to {config.serial.port}[/red]")
                    raise SystemExit(1)
            ok, err = await stream_pen_layers(program, plotter, config, verbose=False)
            if not simulate:
                await plotter.disconnect()
            console.print(f"[bold]streamed[/bold] → {ok} ok, {err} errors")

        asyncio.run(_run())
