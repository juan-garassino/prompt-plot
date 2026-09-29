"""Round-local render wrapper: the r03 plate at Leo's plot settings (mandate A2).

Same contract and pipeline as ``scripts/render_candidate.py`` (piece -> merge_chunks
-> preview + gcode), but the config is set for the plot, not the house default:
``pen.feed_rate = 600`` and ``pen_up_delay = pen_down_delay = 1.0`` (G4 P1.0 after
every M3/M5).  The piece itself emits F600 on every G1.  Writes, beside ``--out``:
the .gcode, and a ``_phys.png`` true-width raster (0.1 / 0.3 / 0.3 / 0.5 nibs on cream).
Then it re-reads the gcode it just wrote and prints the per-layer budget from it:
strokes, draw and travel length, the F values present, the G4 dwell total, minutes.

Nothing under ``promptplot/`` is edited.

usage:
    .venv/bin/python studio/millennium-p-vs-np/rounds/r03/render_plot.py \
        --out ~/Downloads/pp_millennium_p_vs_np_iterate_v1.png
"""
from __future__ import annotations

import argparse
import importlib.util
import math
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO))

FEED = 600
DWELL = 1.0
PALETTE = ["dimgray", "black", "black", "crimson"]
SERVO_S = 0.5      # assumed servo travel per lift or drop, on top of the dwell
RAPID_MM_S = 10.0  # travel costed at the draw speed (conservative: Leo's G0 is slowed too)


def layer_budget(gpath: Path) -> None:
    rows, order = {}, []
    col, down, pos, prev_end = 0, False, (0.0, 0.0), None
    feeds: Counter = Counter()
    for ln in gpath.read_text().splitlines():
        m = re.match(r"(G0|G1|G4|M3|M5)\b", ln)
        if not m:
            continue
        c = m.group(1)
        cm = re.search(r"color=(\d+)", ln)
        if c == "M3":
            col = int(cm.group(1)) if cm else col
            if col not in rows:
                rows[col] = {"strokes": 0, "draw": 0.0, "travel": 0.0, "dwell": 0.0, "g4": 0}
                order.append(col)
                prev_end = None
            rows[col]["strokes"] += 1
            if prev_end is not None:
                rows[col]["travel"] += math.dist(prev_end, pos)
            down = True
            continue
        if c == "M5":
            if down:
                prev_end = pos
            down = False
            continue
        if c == "G4":
            pm = re.search(r"P([\d.]+)", ln)
            if pm and col in rows:
                rows[col]["dwell"] += float(pm.group(1))
                rows[col]["g4"] += 1
            continue
        xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
        if not xs:
            continue
        p = (float(xs.group(1)), float(ys.group(1)))
        if c == "G1":
            fm = re.search(r"F(\d+)", ln)
            feeds[fm.group(1) if fm else "none"] += 1
            if down and col in rows:
                rows[col]["draw"] += math.dist(pos, p)
        pos = p
    print("layer order", order, "(contiguous)" if len(order) == len(set(order)) else "(RE-ENTERED)")
    print("G1 feed values:", dict(feeds))
    tot = 0.0
    for c in order:
        r = rows[c]
        mins = ((r["draw"] + r["travel"]) / RAPID_MM_S + r["dwell"] + 2 * SERVO_S * r["strokes"]) / 60
        tot += mins
        print(f"pen {c}: {r['strokes']} strokes, draw {r['draw']/1000:.2f} m, travel "
              f"{r['travel']/1000:.2f} m, {r['g4']} G4 = {r['dwell']:.0f} s dwell, ~{mins:.1f} min")
    print(f"total ~{tot:.1f} min (+ 2 pen swaps)")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--fn", default="pvsnp_needle_radius")
    a = ap.parse_args()

    from promptplot.config import PaperConfig, get_config
    from promptplot.generative.rng import SeededRNG
    from promptplot.orchestrate import merge_chunks
    from promptplot.visualizer import GCodeVisualizer

    config = get_config()
    config.paper = PaperConfig.from_size("a3", "portrait", margin=15.0)
    config.color.enabled = True
    config.color.palette = list(PALETTE)
    config.pen.feed_rate = FEED
    config.pen.pen_up_delay = DWELL
    config.pen.pen_down_delay = DWELL

    spec = importlib.util.spec_from_file_location("pvsnp_r03", HERE / "piece.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["pvsnp_r03"] = mod
    spec.loader.exec_module(mod)
    cmds = getattr(mod, a.fn)(SeededRNG(a.seed), config.paper.get_drawable_area(),
                              colors=len(PALETTE))
    program = merge_chunks([cmds], config)

    out = Path(a.out).expanduser()
    GCodeVisualizer(config).preview(program, str(out))
    gpath = out.with_suffix(".gcode")
    head = "\n".join([
        "; promptplot render (round-local wrapper: F600, G4 P1.0 pen dwells)",
        f"; piece     {HERE / 'piece.py'}",
        f"; function  {a.fn}",
        f"; seed      {a.seed}",
        "; paper     a3 portrait, margin 15",
        f"; pens      {','.join(PALETTE)}",
        f"; feed      F{FEED} draw · dwell G4 P{DWELL}",
        f"; rendered  {datetime.now().isoformat(timespec='seconds')}",
        f"; commands  {len(program.commands)}",
        "",
    ])
    gpath.write_text(head + program.to_gcode())
    print(len(program.commands), "commands ->", out, gpath)
    phys = out.with_name(out.stem + "_phys.png")
    subprocess.run([sys.executable, str(HERE / "render_truewidth.py"), str(gpath), str(phys)],
                   check=True, stdout=subprocess.DEVNULL)
    print("phys ->", phys)
    layer_budget(gpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
