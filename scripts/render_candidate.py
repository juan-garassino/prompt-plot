"""Render a candidate studio piece to PNG (+ optional GCode).

Mirrors the contract in promptplot/studio/loop.py:_render_code_payload, so a piece
that renders here will render inside the studio design loop unchanged:

    def <fn>(rng: SeededRNG, bounds, colors: int = 3) -> list[GCodeCommand]

Usage:
    python scripts/render_candidate.py studio/<slug>/rounds/r01/piece.py \
        --fn my_piece --seed 7 --paper a4 --out ~/Downloads/pp_<slug>_v1.png
"""

from __future__ import annotations

import argparse
import importlib.util
import logging
from datetime import datetime
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

logger = logging.getLogger(__name__)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("piece", help="path to the candidate piece.py")
    ap.add_argument("--fn", required=True, help="function name inside the piece")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument(
        "--colors",
        type=int,
        default=None,
        help="pen count passed to the piece. Defaults to len(--palette): a fixed "
        "default silently folded 6-pen pieces onto 3 and destroyed the colour "
        "reading, which is never what the caller wanted.",
    )
    ap.add_argument("--paper", default="a4")
    ap.add_argument("--orientation", default="portrait", choices=["portrait", "landscape"])
    ap.add_argument("--out", required=True, help="PNG path")
    ap.add_argument(
        "--gcode",
        help="GCode path. Defaults to the PNG path with a .gcode suffix — a "
        "render with no GCode cannot be plotted, and 22 of 30 studio pieces "
        "ended up PNG-only because this was opt-in.",
    )
    ap.add_argument(
        "--palette",
        default="black,crimson,forestgreen,dodgerblue",
        help="comma-separated pen colours, index 0 first. Pieces address pens by "
        "index, so without this the config default (['black']) makes the "
        "visualizer fall back to its own cycle and every pen looks wrong.",
    )
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    from promptplot.config import PaperConfig, get_config
    from promptplot.generative.rng import SeededRNG
    from promptplot.orchestrate import merge_chunks
    from promptplot.visualizer import GCodeVisualizer

    config = get_config()
    config.paper = PaperConfig.from_size(args.paper, args.orientation)
    config.color.enabled = True
    config.color.palette = [c.strip() for c in args.palette.split(",") if c.strip()]

    piece_path = Path(args.piece).resolve()
    name = f"candidate_{args.fn}"
    spec = importlib.util.spec_from_file_location(name, piece_path)
    mod = importlib.util.module_from_spec(spec)
    # Register before exec: @dataclass resolves its annotations through
    # sys.modules[cls.__module__] and raises at import time if the module is
    # missing. Put the piece's own folder on the path too, so a round that
    # splits itself across files (piece.py + net.py) can import its sibling.
    sys.modules[name] = mod
    sys.path.insert(0, str(piece_path.parent))
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
    fn = getattr(mod, args.fn)

    n_colors = args.colors if args.colors is not None else len(config.color.palette)
    cmds = fn(SeededRNG(args.seed), config.paper.get_drawable_area(), colors=n_colors)
    program = merge_chunks([cmds], config)

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    GCodeVisualizer(config).preview(program, str(out))
    logger.info("%d commands -> %s", len(program.commands), out)

    gpath = Path(args.gcode).expanduser() if args.gcode else out.with_suffix(".gcode")
    gpath.parent.mkdir(parents=True, exist_ok=True)
    # Provenance header: raw M5/G0/G1 cannot be traced back to a piece, a seed
    # or a paper, which is what made the Downloads backlog unsortable.
    head = "\n".join(
        [
            "; promptplot render",
            f"; piece     {piece_path}",
            f"; function  {args.fn}",
            f"; seed      {args.seed}",
            f"; paper     {args.paper} {args.orientation}",
            f"; pens      {','.join(config.color.palette)}",
            f"; colors    {n_colors}",
            f"; rendered  {datetime.now().isoformat(timespec='seconds')}",
            f"; commands  {len(program.commands)}",
            "",
        ]
    )
    gpath.write_text(head + program.to_gcode())
    logger.info("gcode -> %s", gpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
