"""Compat shim — the exact 2D diagram ops moved to ``generative.engine.geometry``."""

from .engine.geometry import *  # noqa: F401,F403
from .engine.geometry import (  # noqa: F401
    Band,
    Circle,
    Complement,
    HalfPlane,
    Intersect,
    Rect,
    Region,
    Union,
    clip,
    offset,
    trim_to,
)
