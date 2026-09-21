"""CLI package.

Re-exports ``cli`` and ``main`` so the ``promptplot.cli:main`` entry point and
``from promptplot.cli import cli`` keep working. Importing the command modules
registers their commands on the shared ``cli`` group.
"""

from ._group import cli, main, console, logger, _get_config

# Import command modules for their registration side effects.
from . import generate  # noqa: F401  (registers generate/plot/score/preview)
from . import draw  # noqa: F401  (registers draw)
from . import art  # noqa: F401  (registers art — seeded generative)
from . import import_cmd  # noqa: F401  (registers import — SVG/DXF)
from . import manage
from . import plot_cmd  # registers plot — frame trace + per-layer guardrailed streaming  # noqa: F401  (registers config/plotter/interactive/ui/library)
from . import agent  # noqa: F401  (registers agent — agentic controller)
from . import studio  # noqa: F401  (registers studio — briefs + design loop)
from . import plate  # noqa: F401  (registers plate — lamina composition)
from . import scene_cmd  # noqa: F401  (registers scene — authored Scene JSON validate/render)

__all__ = ["cli", "main"]
