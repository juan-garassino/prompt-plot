"""Compat shim — the 2D design kit moved to ``generative.engine.kit``.

Copies EVERY public and underscore name so historical imports keep working
(single def-site stays in engine.kit).
"""

import sys as _sys

from .engine import kit as _kit_mod

_this = _sys.modules[__name__]
for _n in dir(_kit_mod):
    if not _n.startswith("__"):
        setattr(_this, _n, getattr(_kit_mod, _n))
