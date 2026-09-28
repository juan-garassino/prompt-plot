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
``promptplot plot plate FILE``      → a whole multi-pen plate as ONE resumable
                                      job (``promptplot/plotjob.py``): frame,
                                      per-layer park + swap wait, pen-up
                                      approach, batches, re-zero checks, job
                                      file after every batch, ``--resume ID``
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


@plot_group.command(name="plate")
@click.argument("filepath", required=False)
@click.option("--layers", default=None, help="Colour indices in plotting order, e.g. 0,2,3 (default: file order)")
@click.option("--batch-strokes", "batch_strokes", default=400, type=int, help="Strokes per batch — the stop/resume granularity (0 = whole layer)")
@click.option("--rezero-every", "rezero_every", default=2000, type=int, help="Park at (0,0) and wait for an origin check every N strokes (0 = never)")
@click.option("--max-feed", "max_feed", default=500.0, type=float, help="Cap every draw feed, mm/min (0 = the file's feeds)")
@click.option("--min-dwell", "min_dwell", default=1.0, type=float, help="Floor every G4 pen dwell, s (0 = the file's dwells)")
@click.option("--resume", "resume_id", default=None, help="Resume a saved job (see --jobs)")
@click.option("--retrace", is_flag=True, help="On --resume, trace the pen-up frame again first")
@click.option("--jobs", "list_jobs", is_flag=True, help="List saved plate jobs and exit")
@click.option("--port", default=None, help="Serial port")
@click.option("--paper", default="a4:landscape", help="WxH (mm or cm) or size:orientation")
@click.option("--margin", default=15.0, type=float, help="Drawable margin (mm)")
@click.option("--timeout", default=60.0, type=float, help="Serial ack timeout (s)")
@click.option("--dry-run", "dry_run", is_flag=True, help="Plan + rehearse on the simulator, no hardware")
def plot_plate(filepath, layers, batch_strokes, rezero_every, max_feed, min_dwell, resume_id,
               retrace, list_jobs, port, paper, margin, timeout, dry_run):
    """Plot a whole multi-pen plate as ONE resumable job: frame trace, then per
    layer park + pen swap (Enter), pen-up approach, batches, re-zero checks.
    Ctrl-C once = pause after the current batch; twice = stop now (pen up, park)."""
    import signal

    from .. import plotjob as pj

    store = pj.JobStore()
    if list_jobs:
        rows = store.list()
        if not rows:
            console.print("no saved plate jobs")
        for r in rows:
            ov = (r.get("progress") or {}).get("overall") or [0, 0]
            console.print(f"  {r['id']}  {r['state']:<15} {ov[0]}/{ov[1]} strokes  "
                          f"eta {r.get('eta_min')} min  {r['target']}")
        return

    config = _get_config()
    if port:
        config.serial.port = port
    try:
        if resume_id:
            job = store.load(resume_id)
            if job.state == pj.JobState.DONE.value:
                raise pj.PlotRefused(f"{job.id} is already done")
            if filepath and Path(filepath).resolve() != Path(job.path):
                raise pj.PlotRefused(f"{job.id} plots {job.path}, not {filepath}")
            console.print(f"[bold]resuming {job.id}[/bold] on {job.paper} (the job's paper) at "
                          f"layer {job.cursor['unit'] + 1}, stroke {job.cursor['stroke']}")
        else:
            if not filepath:
                raise click.UsageError("give a gcode file, or --resume JOB_ID")
            job = pj.new_job(
                Path(filepath), paper=paper, margin=margin,
                layers=[int(v) for v in layers.split(",")] if layers else None,
                batch_strokes=batch_strokes, rezero_every=rezero_every,
                max_feed=max_feed, min_dwell=min_dwell)
            job.id = store.unique_id(job.id)
        plan = pj.plan_for_job(job)
    except pj.PlotRefused as e:
        raise SystemExit(f"refused: {e}") from None

    console.print(f"[bold]plate[/bold] {job.path}  paper {job.paper} margin {job.margin:g}")
    for i, L in enumerate(plan.layers):
        console.print(f"  layer {i + 1}: colour {L.color}  {L.strokes} strokes  "
                      f"~{sum(L.seconds) / 60:.0f} min")
    est = plan.remaining_seconds(job.cursor["unit"], job.cursor["stroke"], job.rezero_every,
                                 swap_pending=not resume_id) / 60.0
    console.print(f"  bounds ok · batches of {job.batch_strokes or 'whole layer'} · re-zero every "
                  f"{job.rezero_every or 'never'} · feed ≤ {job.max_feed:g} · dwell ≥ "
                  f"{job.min_dwell:g}s · ETA ~{est:.0f} min "
                  f"(F{pj.LEO_TRAVEL_MM_MIN:g} travel, {pj.SWAP_S:g}s per pen swap)")

    if dry_run:
        from ..plotter import SimulatedPlotter

        sim = SimulatedPlotter(command_delay=0)
        ctl = pj.AutoContinueControl()

        async def _sim():
            await sim.connect()
            return sim

        runner = pj.PlateJobRunner(job, plan, connect=_sim, control=ctl, store=None,
                                   trace_frame=True, resuming=bool(resume_id))
        asyncio.run(runner.run())
        drawn = sum(1 for seg in sim.lines if seg[4])
        console.print(f"[cyan]dry-run:[/cyan] {len(sim.collected)} commands, {drawn} inked "
                      f"segments, waits: {', '.join(ctl.waits) or 'none'} → {job.state}")
        return

    ctl = pj.KeypressControl(prompt=console.print)
    presses = {"n": 0}

    def _on_sigint(_sig, _frm):
        presses["n"] += 1
        if presses["n"] == 1:
            ctl.request_pause()
            console.print("\n[yellow]pause requested — stopping after this batch "
                          "(Ctrl-C again = stop now)[/yellow]")
        else:
            ctl.request_stop()
            console.print("\n[red]stop requested — lifting the pen and parking[/red]")

    async def _connect():
        from ..plotter import SerialPlotter

        p = SerialPlotter(port=config.serial.port, baud_rate=config.serial.baud_rate,
                          timeout=timeout, enable_heartbeat=False)
        if not await p.connect():
            raise RuntimeError(f"could not connect to {config.serial.port}")
        return p

    runner = pj.PlateJobRunner(
        job, plan, connect=_connect, control=ctl, store=store,
        trace_frame=retrace or not resume_id,
        framed=bool(resume_id and job.framed),
        resuming=bool(resume_id),
        say=lambda m: console.print(f"  {m}"))
    old = signal.signal(signal.SIGINT, _on_sigint)
    try:
        asyncio.run(runner.run())
    finally:
        signal.signal(signal.SIGINT, old)
    colour = "green" if job.state == pj.JobState.DONE.value else "yellow"
    console.print(f"[{colour}]{job.id}: {job.state}[/{colour}] — {job.message}")
    if job.state != pj.JobState.DONE.value:
        console.print(f"  resume: promptplot plot plate --resume {job.id}")
