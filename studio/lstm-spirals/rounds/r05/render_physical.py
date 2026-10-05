"""Re-render an emitted r05 gcode at PHYSICAL pen widths on cream paper.

    .venv/bin/python studio/lstm-spirals/rounds/r05/render_physical.py <in>.gcode <out>.png

render_candidate.py draws every pen at one width, so the declared hierarchy
(grey 0.3 < crimson 0.5 = black 0.5 > type 0.3) is invisible there. This reads
the same gcode back (no geometry is recomputed) and draws each colour layer at
its nib width.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

from promptplot.config import PaperConfig, get_config  # noqa: E402
from promptplot.pipeline import FilePipeline  # noqa: E402
from promptplot.visualizer import GCodeVisualizer  # noqa: E402

PENS = {0: 0.3, 1: 0.5, 2: 0.5, 3: 0.3}
PALETTE = ["#9a9a9a", "crimson", "black", "black"]


def main() -> int:
    src, dst = Path(sys.argv[1]).expanduser(), Path(sys.argv[2]).expanduser()
    config = get_config()
    program = FilePipeline(config).load_gcode_file(str(src))
    config.paper = PaperConfig.from_size("a4", "portrait")
    config.color.enabled = True
    config.color.palette = PALETTE
    config.visualization.paper_color = "cream"
    GCodeVisualizer(config).preview(program, str(dst), palette=PALETTE, pen_widths=PENS)
    print(dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
