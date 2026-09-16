"""Compat shim — effects split into ``engine.looks`` (aesthetics) and
``engine.policies`` (guardrails). Single def-sites live there."""

from .engine.looks import (  # noqa: F401
    anaglyph_layers,
    dash_rain,
    echo_layers,
    glitch_slice,
)
from .engine.policies import (  # noqa: F401
    enforce_line_spacing,
    focal_void,
    limit_ink_density,
    occlude_crossings,
)
