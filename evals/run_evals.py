"""Offline eval harness: mocked LLM responses + seeded generators -> pipeline -> simulator.

Usage::

    python -m evals.run_evals                 # print the table
    python -m evals.run_evals --json out.json # also write per-case metrics

Every case goes through the production path that ``draw`` / ``art`` use after
the LLM call (``_validate_output`` -> ``expand_primitives`` -> ``run_pipeline``,
then ``split_color_layers`` for streaming) and the output is replayed in
``evals.simulate``. No network, API keys or plotter are needed; it runs in
well under a minute on CPU.

Metrics per case (lower is better unless noted):
  safety     G0 with pen down + G1 with pen up + inked points outside the
             drawable area + not starting/ending pen-up
  missing    mm of intended ink absent from the output
  spurious   mm of ink in the output that was not intended (drags, wrong pen)
  leaks      colour layers that lower the pen without drawing (stray dot)
  mixed      colour layers containing more than one pen's ink
  switches   colour changes along the drawing order beyond the minimum
  lifts      pen lifts (M5 after M3)
  travel     pen-up travel in mm
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

from promptplot.config import PromptPlotConfig
from promptplot.models import DrawProgram, GCodeProgram
from promptplot.orchestrate import split_color_layers
from promptplot.postprocess import run_pipeline
from promptplot.primitives import expand_primitives
from promptplot.workflow._shared import _validate_output

from . import simulate as sim

FIXTURES = Path(__file__).parent / "fixtures" / "llm_responses.json"
PALETTE = ["black", "red", "blue", "green"]

# Seeded generators: deterministic, no LLM. Kept small so the run stays fast.
GENERATOR_CASES = [
    {"name": "gen_truchet_2c", "generator": "truchet", "seed": 7, "colors": 2, "params": {}},
    {"name": "gen_maze", "generator": "maze", "seed": 3, "colors": 1, "params": {}},
    {"name": "gen_hitomezashi_2c", "generator": "hitomezashi", "seed": 11, "colors": 2,
     "params": {}},
    {"name": "gen_flow_field", "generator": "flow_field", "seed": 5, "colors": 1, "params": {}},
    {"name": "gen_wave_bands_3c", "generator": "wave_bands", "seed": 2, "colors": 3,
     "params": {}},
]


def _config(colors: int) -> PromptPlotConfig:
    cfg = PromptPlotConfig()
    cfg.paper.width, cfg.paper.height = 210.0, 297.0
    if colors > 1:
        cfg.color.enabled = True
        cfg.color.palette = PALETTE[:colors]
    return cfg


def _llm_program(response: str, cfg: PromptPlotConfig) -> GCodeProgram:
    """Parse a raw LLM reply the way the batch workflow does."""
    parsed = _validate_output(response)
    if isinstance(parsed, Exception):
        raise parsed
    if isinstance(parsed, DrawProgram):
        return expand_primitives(parsed, cfg.pen)
    if isinstance(parsed, GCodeProgram):
        return parsed
    return GCodeProgram(commands=[parsed])


def _gen_program(case: Dict[str, Any], cfg: PromptPlotConfig) -> GCodeProgram:
    from promptplot.generative.registry import run_generator

    cmds = run_generator(
        case["generator"], cfg.paper.get_drawable_area(), case["seed"],
        colors=case["colors"], params=case["params"],
    )
    return GCodeProgram(commands=cmds)


def evaluate_case(name: str, colors: int, build) -> Dict[str, Any]:
    """Run one case end-to-end and return its metrics (``error`` on failure)."""
    cfg = _config(colors)
    drawable = cfg.paper.get_drawable_area()
    row: Dict[str, Any] = {"case": name}
    try:
        raw = build(cfg)
    except Exception as e:  # a crash before the pipeline is itself a result
        row["error"] = f"{type(e).__name__}: {e}"[:160]
        return row
    out = run_pipeline(raw, cfg)
    ref = sim.simulate(raw.commands, g1_is_ink=True)
    before = sim.simulate(raw.commands)
    after = sim.simulate(out.commands, drawable=drawable)
    missing, spurious = sim.ink_diff(
        sim.ink_cells(ref.ink, drawable), sim.ink_cells(after.ink)
    )
    layers = split_color_layers(out) if colors > 1 else [(0, out.commands)]
    min_switches = max(0, len(after.colors) - 1)
    row.update(
        safety=after.g0_pen_down + after.g1_pen_up + after.out_of_bounds
        + (not after.starts_pen_up) + (not after.ends_pen_up),
        missing_mm=round(missing, 1),
        spurious_mm=round(spurious, 1),
        leaks=sim.layer_pen_down_leaks(layers) if colors > 1 else 0,
        mixed=sim.layer_mixed_colors(layers) if colors > 1 else 0,
        extra_switches=after.color_switches - min_switches,
        lifts_in=before.pen_lifts,
        lifts=after.pen_lifts,
        travel_in=round(before.travel_mm, 1),
        travel=round(after.travel_mm, 1),
        draw=round(after.draw_mm, 1),
    )
    return row


def run_all() -> List[Dict[str, Any]]:
    rows = []
    for case in json.loads(FIXTURES.read_text()):
        rows.append(evaluate_case(
            case["name"], case["colors"], lambda cfg, c=case: _llm_program(c["response"], cfg)
        ))
    for case in GENERATOR_CASES:
        rows.append(evaluate_case(
            case["name"], case["colors"], lambda cfg, c=case: _gen_program(c, cfg)
        ))
    return rows


def summarize(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate metrics across cases (errors counted separately)."""
    ok = [r for r in rows if "error" not in r]
    total = lambda k: round(sum(r[k] for r in ok), 1)  # noqa: E731
    return {
        "cases": len(rows),
        "errors": len(rows) - len(ok),
        "safety_violations": total("safety"),
        "missing_mm": total("missing_mm"),
        "spurious_mm": total("spurious_mm"),
        "layer_leaks": total("leaks"),
        "mixed_layers": total("mixed"),
        "extra_color_switches": total("extra_switches"),
        "pen_lifts": total("lifts"),
        "travel_mm": total("travel"),
    }


COLS = ["case", "safety", "missing_mm", "spurious_mm", "leaks", "mixed", "extra_switches",
        "lifts_in", "lifts", "travel_in", "travel"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", help="write per-case rows + summary to this path")
    args = ap.parse_args(argv)
    t0 = time.time()
    rows = run_all()
    summary = summarize(rows)
    print(" | ".join(COLS))
    for r in rows:
        if "error" in r:
            print(f"{r['case']} | ERROR {r['error']}")
        else:
            print(" | ".join(str(r[c]) for c in COLS))
    print()
    for k, v in summary.items():
        print(f"{k:>22}: {v}")
    print(f"{'seconds':>22}: {time.time() - t0:.1f}")
    if args.json:
        Path(args.json).write_text(json.dumps({"rows": rows, "summary": summary}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
