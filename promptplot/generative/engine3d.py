"""engine3d — the from-scratch 3D pen-plotter engine.

A numpy z-buffer hidden-line renderer for line-native 3D on a plotter: surface
quads are rasterized into a depth buffer, then only the VISIBLE parts of each
mesh line are drawn, so near ridges/folds occlude far mesh and surfaces read as
solid form. Pieces build (SX, SY, DEP) screen/depth arrays with their own
isometric ``proj``/``dep`` closures and call :func:`_zbuf_terrain`.
"""

from __future__ import annotations

import math
from typing import List, Optional

from ..models import GCodeCommand
from .generators import _poly



def _zbuf_terrain(out, SX, SY, DEP, feed=2200, PENV=None, pen=None, PXW=210, PXH=160):
    """Shared 3D hidden-line terrain engine (compat wrapper).

    The raster core now lives in :class:`engine.scene3d.Scene3D`; this wrapper
    runs it in EXACT/legacy mode (``thin=None`` — every grid line drawn,
    occlusion only) and appends to ``out``, byte-compatible with the historic
    implementation. New pieces should build a ``Scene3D`` directly and get the
    native anti-crowding defaults."""
    from .engine.scene3d import Scene3D

    scene = Scene3D(bounds=None, feed=feed, px=(PXW, PXH), pad=3.0, fit="none")
    scene.surface(SX, SY, DEP, pen=pen, pens=PENV, thin=None)
    out.extend(scene.out)



def _fit_out(out, bounds, inset=4.0):
    """Safety net: if the emitted geometry spills the drawable, uniformly
    shrink + centre ALL commands so the whole composition lands on paper."""
    xs = [c.x for c in out if c.x is not None]
    ys = [c.y for c in out if c.y is not None]
    if not xs:
        return out
    x0, y0, x1, y1 = bounds
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    if bx0 >= x0 and bx1 <= x1 and by0 >= y0 and by1 <= y1:
        return out
    tw, th = (x1 - x0 - 2 * inset), (y1 - y0 - 2 * inset)
    s = min(tw / max(1e-6, bx1 - bx0), th / max(1e-6, by1 - by0), 1.0)
    cxs, cys = (bx0 + bx1) / 2, (by0 + by1) / 2
    tcx, tcy = (x0 + x1) / 2, (y0 + y1) / 2
    fitted = []
    for c in out:
        nx = tcx + (c.x - cxs) * s if c.x is not None else None
        ny = tcy + (c.y - cys) * s if c.y is not None else None
        fitted.append(c.model_copy(update={"x": (round(nx, 3) if nx is not None else None),
                                           "y": (round(ny, 3) if ny is not None else None)}))
    return fitted

