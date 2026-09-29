"""Write the r04 PLATE gcode with the piece's stream order kept, and report the Leo budget.

``scripts/render_candidate.py`` runs the full postprocess pipeline, whose per-colour
nearest-START pass re-orders strokes from (0, 0) and cannot reverse them — it undoes the
piece's serpentine, reversal-aware order and leaves long straggler hops.  This script runs the
same pipeline stages MINUS that one reorder (arcs, bounds, pen safety, pen dwells), so the
gcode streams exactly in the order ``piece._order`` built: pens in index order (light ->
dark), each layer once, each layer a serpentine sweep of 30 mm cells.

    .venv/bin/python studio/resonance-backprop/rounds/r04/plate.py \
        --out ~/Downloads/pp_res_backprop_iterate_vN_plate.gcode [--png]

Budget model = studio/PLOT_JOBS.md (the plate job's ETA): draw at F500, travel at
2000 mm/min, 2.0 s per pen cycle, 90 s per pen swap, 20 s per re-zero check.
"""

from __future__ import annotations

import argparse
import importlib.util
import logging
import math
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))

logger = logging.getLogger(__name__)

F_DRAW = 500.0          # mm/min, the plate job's draw cap
F_TRAVEL = 2000.0       # mm/min
S_CYCLE = 2.0           # s per pen cycle (lift + drop + dwells)
S_SWAP = 90.0           # s per pen swap
S_REZERO = 20.0         # s per re-zero check
BATCH = 400             # strokes per batch (plot plate --batch-strokes 400)
HOP_MAX = 80.0          # mm: no in-layer travel longer than this except layer entry


def load_piece():
    spec = importlib.util.spec_from_file_location("r04_piece", HERE / "piece.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["r04_piece"] = mod
    spec.loader.exec_module(mod)
    return mod


def layer_stats(program):
    """Per colour layer: strokes (pen cycles), draw, travel, hops, batch regions."""
    layers = {}
    order = []
    pos = (0.0, 0.0)
    cur = None
    for c in program.commands:
        if c.command == "M3" and c.color is not None:
            cur = c.color
            if cur not in layers:
                layers[cur] = {"strokes": 0, "draw": 0.0, "travel": 0.0, "hops": [], "starts": [],
                               "entry": None, "boxes": []}
                order.append(cur)
            L = layers[cur]
            L["strokes"] += 1
            L["starts"].append(pos)
        if c.command in ("G0", "G1") and c.x is not None:
            nxt = (c.x, c.y if c.y is not None else pos[1])
            d = math.hypot(nxt[0] - pos[0], nxt[1] - pos[1])
            if c.command == "G1" and cur is not None:
                layers[cur]["draw"] += d
            elif c.command == "G0":
                # attribute a travel to the layer of the NEXT stroke
                layers.setdefault("_pending", 0.0)
                layers["_pending"] += d
                layers.setdefault("_hop", 0.0)
                layers["_hop"] += d
            pos = nxt
        if c.command == "M3" and c.color is not None:
            L = layers[cur]
            L["travel"] += layers.pop("_pending", 0.0)
            hop = layers.pop("_hop", 0.0)
            if L["strokes"] == 1:
                L["entry"] = hop
            else:
                L["hops"].append(hop)
    layers.pop("_pending", None)
    layers.pop("_hop", None)
    return order, layers


def stroke_boxes(program):
    """Per layer, the bbox of each stroke's drawn points, in stroke order."""
    boxes = {}
    cur = None
    pts = []
    for c in program.commands:
        if c.command == "M3" and c.color is not None:
            cur = c.color
            pts = []
        elif c.command == "G1" and c.x is not None and cur is not None:
            pts.append((c.x, c.y))
        elif c.command == "M5" and cur is not None and pts:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            boxes.setdefault(cur, []).append((min(xs), min(ys), max(xs), max(ys)))
            pts = []
    return boxes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="plate gcode path")
    ap.add_argument("--png", action="store_true", help="also write a preview PNG beside it")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from promptplot.config import PaperConfig, get_config
    from promptplot.generative.rng import SeededRNG
    from promptplot.models import GCodeCommand, GCodeProgram
    from promptplot.postprocess import (approximate_arcs, ensure_pen_safety, insert_pen_dwells,
                                        validate_bounds)

    piece = load_piece()
    config = get_config()
    config.paper = PaperConfig.from_size("a4", "portrait")
    config.color.enabled = True
    config.color.palette = piece.PALETTE.split(",")
    bounds = config.paper.get_drawable_area()

    cmds = piece.attention_as_resonance(SeededRNG(args.seed), bounds, colors=5)
    prog = GCodeProgram(commands=[GCodeCommand(command="M5")] + cmds + [GCodeCommand(command="M5")])
    prog = approximate_arcs(prog)
    prog, violations = validate_bounds(prog, config.paper, config.bounds.mode)
    prog = GCodeProgram(commands=ensure_pen_safety(prog.commands, config.pen))
    prog.commands.append(GCodeCommand(command="G0", x=0.0, y=0.0))
    prog = insert_pen_dwells(prog, config.pen)

    out = Path(args.out).expanduser()
    head = "\n".join([
        "; promptplot PLATE (stream order kept: pens light->dark, serpentine cells per layer)",
        f"; piece     {HERE / 'piece.py'} (plate.py)",
        "; function  attention_as_resonance",
        f"; seed      {args.seed}",
        "; paper     a4 portrait",
        f"; pens      {piece.PALETTE}",
        "; colors    5",
        f"; rendered  {datetime.now().isoformat(timespec='seconds')}",
        f"; commands  {len(prog.commands)}",
        "",
    ])
    out.write_text(head + prog.to_gcode())
    logger.info("plate gcode -> %s (%d commands, %d bounds violations)", out, len(prog.commands),
                len(violations))
    if args.png:
        from promptplot.visualizer import GCodeVisualizer
        GCodeVisualizer(config).preview(prog, str(out.with_suffix(".png")))

    order, layers = layer_stats(prog)
    boxes = stroke_boxes(prog)
    names = piece.PALETTE.split(",")
    print("\n| layer | pen | cycles | draw m | travel m | entry mm | max hop mm | hops>80 | min |")
    print("|---|---|---|---|---|---|---|---|---|")
    T = {"cyc": 0, "draw": 0.0, "trav": 0.0, "min": 0.0}
    for i, k in enumerate(order):
        L = layers[k]
        mins = (L["draw"] / F_DRAW + L["travel"] / F_TRAVEL + L["strokes"] * S_CYCLE / 60.0
                + S_SWAP / 60.0)
        big = [h for h in L["hops"] if h > HOP_MAX]
        print(f"| {i + 1} | {k} {names[k]} | {L['strokes']} | {L['draw'] / 1000:.2f} | "
              f"{L['travel'] / 1000:.2f} | {L['entry']:.0f} | {max(L['hops'] or [0]):.1f} | "
              f"{len(big)} | {mins:.1f} |")
        T["cyc"] += L["strokes"]
        T["draw"] += L["draw"]
        T["trav"] += L["travel"]
        T["min"] += mins
    print(f"| total | 5 pens | {T['cyc']} | {T['draw'] / 1000:.2f} | {T['trav'] / 1000:.2f} | | | | "
          f"{T['min']:.1f} ({T['min'] / 60:.2f} h) |")
    print(f"\ntravel / draw = {T['trav'] / T['draw'] * 100:.0f} %")
    print("\nbatches (--strokes S:E, 400 per batch) with the sheet region each covers (mm):")
    for k in order:
        bx = boxes[k]
        n = len(bx)
        for s in range(0, n, BATCH):
            e = min(n, s + BATCH)
            sub = bx[s:e]
            x0 = min(b[0] for b in sub)
            y0 = min(b[1] for b in sub)
            x1 = max(b[2] for b in sub)
            y1 = max(b[3] for b in sub)
            print(f"  layer {k} {names[k]:12s} {s}:{e}  x {x0:5.1f}-{x1:5.1f}  y {y0:5.1f}-{y1:5.1f}"
                  f"  ({x1 - x0:.0f} x {y1 - y0:.0f})")
    print("\nSTATS", piece.STATS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
