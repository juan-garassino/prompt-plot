"""Scene3D — the stateful 3D diagram builder (raster core + native policies).

The z-buffer hidden-line renderer extracted from the pieces: surface quads
rasterize into a depth buffer, then only the VISIBLE parts of each mesh line
are drawn, so near folds occlude far ones and surfaces read as solid form.

ANTI-CROWDING IS NATIVE (house law): ``surface()`` defaults to a depth-aware
screen-space thinning derived from the pen ``tip`` width, so meshes can never
pile into black patches — pass ``thin=None`` for the exact/legacy mode (the
``engine3d._zbuf_terrain`` compat wrapper does exactly that).

Engine operators are RNG-FREE: randomness stays in piece code so extraction
never shuffles seeded output.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

from ...models import GCodeCommand
from ..generators import _poly

HIDE = -1e19  # sample sentinel: silently breaks the current run


@dataclass
class Iso:
    """Isometric camera: proj (wx,wy,wz)→(sx,sy) and view depth (larger=nearer)."""

    cx: float
    cy: float
    a: float  # x−z spread
    wy: float  # vertical gain
    cd: float  # depth drop
    depth_wy: float = 0.12

    def proj(self, wx: float, wy: float, wz: float) -> Tuple[float, float]:
        return (self.cx + (wx - wz) * self.a, self.cy + wy * self.wy - (wx + wz) * self.cd)

    def depth(self, wx: float, wy: float, wz: float) -> float:
        return (wx + wz) + self.depth_wy * wy


@dataclass
class Camera:
    """Escape hatch: any pair of proj/depth callables (sheared layer cameras…)."""

    proj: Callable[[float, float, float], Tuple[float, float]]
    depth: Callable[[float, float, float], float]


@dataclass
class ScreenThin:
    """Depth-aware minimum line gap for grid surfaces, in PAPER mm.

    Where mesh lines stack tighter than ``gap_mm`` on the page (steep folds,
    foreshortened faces), samples drop locally in BOTH grid families; the far
    half of the surface (view depth below median) uses ``far_mult``× the floor
    — atmospheric perspective. ``weave`` > 0 alternates ring/radial leadership
    in checkerboard patches (the yielding family's floor × weave).
    """

    gap_mm: float = 0.8
    far_mult: float = 2.0
    weave: float = 0.0
    weave_blocks: Optional[Tuple[int, int]] = None


class Scene3D:
    HIDE = HIDE

    def __init__(
        self,
        rng=None,
        bounds: Optional[Tuple[float, float, float, float]] = None,
        *,
        camera=None,
        feed: int = 2200,
        tip: float = 0.5,
        px: Tuple[int, int] = (210, 160),
        pad: float = 3.0,
        fit: str = "rescue",  # "rescue" | "fill" | "none"
        fit_pad: float = 4.0,
    ):
        self.rng = rng
        self.bounds = bounds
        self.camera = camera
        self.feed = feed
        self.tip = tip
        self.pxw, self.pxh = px
        self.pad = pad
        self.fit = fit
        self.fit_pad = fit_pad
        self.out: List[GCodeCommand] = []
        self._labels: List[tuple] = []
        self._boxes: List[Tuple[float, float, float, float]] = []
        self._mm_scale: Optional[float] = None
        # active depth field (fresh per surface()/ribbon() call)
        self._zb = None
        self._sxmin = self._sxmax = self._symin = self._symax = 0.0
        self._bias = 0.0

    # ------------------------------------------------------------------ mm
    def mm(self, v: float) -> float:
        """Convert paper-mm to the scene's pre-fit units (identity unless the
        scene will be fill-scaled; then the first surface's extents estimate
        the eventual fit factor — the manifold idiom)."""
        return v / self._scale()

    def _scale(self) -> float:
        if self._mm_scale is None:
            return 1.0
        return self._mm_scale

    def _estimate_scale(self, SX, SY) -> None:
        if self.fit != "fill" or self.bounds is None or self._mm_scale is not None:
            return
        x0, y0, x1, y1 = self.bounds
        pw = float(SX.max() - SX.min()) or 1.0
        ph = float(SY.max() - SY.min()) or 1.0
        w, h = x1 - x0, y1 - y0
        s = min((w - 2 * self.fit_pad) / pw, (h - 2 * self.fit_pad) / ph)
        self._mm_scale = s if s > 0 else 1.0

    # ------------------------------------------------------------ raster core
    def _rasterize(self, SX, SY, DEP) -> None:
        """Fresh z-buffer from a (R+1,C+1) grid — becomes the active field."""
        import numpy as np

        R, C = SX.shape[0] - 1, SX.shape[1] - 1
        self._sxmin, self._sxmax = float(SX.min()) - self.pad, float(SX.max()) + self.pad
        self._symin, self._symax = float(SY.min()) - self.pad, float(SY.max()) + self.pad
        zb = np.full((self.pxh, self.pxw), -1e18)
        PX = (SX - self._sxmin) / (self._sxmax - self._sxmin) * (self.pxw - 1)
        PY = (SY - self._symin) / (self._symax - self._symin) * (self.pxh - 1)
        dspan = float(DEP.max() - DEP.min()) or 1.0
        self._bias = 0.02 * dspan
        pxw, pxh = self.pxw, self.pxh

        def tri(p0, p1, p2, d0, d1, d2):
            minx = int(max(0, math.floor(min(p0[0], p1[0], p2[0]))))
            maxx = int(min(pxw - 1, math.ceil(max(p0[0], p1[0], p2[0]))))
            miny = int(max(0, math.floor(min(p0[1], p1[1], p2[1]))))
            maxy = int(min(pxh - 1, math.ceil(max(p0[1], p1[1], p2[1]))))
            if maxx < minx or maxy < miny:
                return
            den = (p1[1] - p2[1]) * (p0[0] - p2[0]) + (p2[0] - p1[0]) * (p0[1] - p2[1])
            if abs(den) < 1e-9:
                return
            X, Y = np.meshgrid(np.arange(minx, maxx + 1), np.arange(miny, maxy + 1))
            aa = ((p1[1] - p2[1]) * (X - p2[0]) + (p2[0] - p1[0]) * (Y - p2[1])) / den
            bb = ((p2[1] - p0[1]) * (X - p2[0]) + (p0[0] - p2[0]) * (Y - p2[1])) / den
            cc = 1 - aa - bb
            ins = (aa >= -1e-4) & (bb >= -1e-4) & (cc >= -1e-4)
            d = aa * d0 + bb * d1 + cc * d2
            sub = zb[miny : maxy + 1, minx : maxx + 1]
            m = ins & (d > sub)
            sub[m] = d[m]

        for i in range(R):
            for j in range(C):
                tri(
                    (PX[i, j], PY[i, j]),
                    (PX[i + 1, j], PY[i + 1, j]),
                    (PX[i + 1, j + 1], PY[i + 1, j + 1]),
                    DEP[i, j],
                    DEP[i + 1, j],
                    DEP[i + 1, j + 1],
                )
                tri(
                    (PX[i, j], PY[i, j]),
                    (PX[i + 1, j + 1], PY[i + 1, j + 1]),
                    (PX[i, j + 1], PY[i, j + 1]),
                    DEP[i, j],
                    DEP[i + 1, j + 1],
                    DEP[i, j + 1],
                )
        self._zb = zb

    def visible(self, sx: float, sy: float, dep: float) -> bool:
        """Is a point visible against the ACTIVE depth field? (off-buffer or
        no field → visible: nothing occludes it)."""
        if self._zb is None:
            return True
        px = int((sx - self._sxmin) / (self._sxmax - self._sxmin) * (self.pxw - 1))
        py = int((sy - self._symin) / (self._symax - self._symin) * (self.pxh - 1))
        if px < 0 or px >= self.pxw or py < 0 or py >= self.pxh:
            return True
        return dep >= self._zb[py, px] - self._bias

    def _blocked(self, sx: float, sy: float) -> bool:
        for bx0, by0, bx1, by1 in self._boxes:
            if bx0 <= sx <= bx1 and by0 <= sy <= by1:
                return True
        return False

    def _emit_runs(self, samples: Sequence[tuple], feed: Optional[int] = None) -> None:
        """samples: (sx, sy, dep, pen). Draw the visible runs against the
        active field, splitting on occlusion, HIDE sentinels, halo boxes and
        pen changes (a pen change starts the new run at the current sample —
        the historical `_zbuf_terrain` behavior, preserved)."""
        feed = self.feed if feed is None else feed
        run: List[Tuple[float, float]] = []
        cur = None
        for sx, sy, dep, pen in samples:
            ok = dep != HIDE and self.visible(sx, sy, dep) and not self._blocked(sx, sy)
            if ok:
                if cur is None or pen == cur:
                    run.append((sx, sy))
                    cur = pen
                else:
                    if len(run) >= 2:
                        self.out.extend(_poly(run, color=cur, f=feed))
                    run, cur = [(sx, sy)], pen
            else:
                if len(run) >= 2:
                    self.out.extend(_poly(run, color=cur, f=feed))
                run, cur = [], None
        if len(run) >= 2:
            self.out.extend(_poly(run, color=cur, f=feed))

    # ---------------------------------------------------------------- surface
    def surface(
        self,
        SX,
        SY,
        DEP,
        *,
        pen: Optional[int] = None,
        pens=None,
        thin="auto",
        feed: Optional[int] = None,
    ) -> "Scene3D":
        """Rasterize a grid surface (fresh field) and draw its mesh lines with
        hidden-line occlusion. ``thin="auto"`` (default) applies the native
        anti-crowding ScreenThin derived from ``tip``; ``thin=None`` is the
        exact/legacy mode (every grid line drawn, occlusion only)."""
        import numpy as np

        self._estimate_scale(SX, SY)
        self._rasterize(SX, SY, DEP)
        R, C = SX.shape[0] - 1, SX.shape[1] - 1

        cfg = ScreenThin(gap_mm=1.6 * self.tip) if thin == "auto" else thin
        if cfg is None:
            for i in range(R + 1):
                self._emit_runs(
                    [
                        (SX[i, j], SY[i, j], DEP[i, j], int(pens[i, j]) if pens is not None else pen)
                        for j in range(C + 1)
                    ],
                    feed,
                )
            for j in range(C + 1):
                self._emit_runs(
                    [
                        (SX[i, j], SY[i, j], DEP[i, j], int(pens[i, j]) if pens is not None else pen)
                        for i in range(R + 1)
                    ],
                    feed,
                )
            return self

        # native anti-crowding: local screen-gap floor per family, depth-aware
        gap_pre = self.mm(cfg.gap_mm)
        dep_med = float(np.median(DEP))
        wbi, wbj = cfg.weave_blocks or (max(1, R // 4), max(1, C // 8))

        def gap2(i, j, family):
            g = gap_pre * (cfg.far_mult if DEP[i, j] < dep_med else 1.0)
            if cfg.weave > 0:
                rows_lead = ((i // wbi) + (j // wbj)) % 2 == 0
                leads = rows_lead if family == "row" else not rows_lead
                if not leads:
                    g *= cfg.weave
            return g * g

        def pen_at(i, j):
            return int(pens[i, j]) if pens is not None else pen

        last_row = [None] * (C + 1)  # memory for the row family, per column
        last_col = [None] * (R + 1)  # memory for the col family, per row
        for i in range(R + 1):
            samples = []
            for j in range(C + 1):
                sx, sy, dp = SX[i, j], SY[i, j], DEP[i, j]
                lk = last_row[j]
                if lk is not None and (sx - lk[0]) ** 2 + (sy - lk[1]) ** 2 < gap2(i, j, "row"):
                    samples.append((sx, sy, HIDE, pen_at(i, j)))
                else:
                    samples.append((sx, sy, dp, pen_at(i, j)))
                    last_row[j] = (sx, sy)
            self._emit_runs(samples, feed)
        for j in range(C + 1):
            samples = []
            for i in range(R + 1):
                sx, sy, dp = SX[i, j], SY[i, j], DEP[i, j]
                lk = last_col[i]
                if lk is not None and (sx - lk[0]) ** 2 + (sy - lk[1]) ** 2 < gap2(i, j, "col"):
                    samples.append((sx, sy, HIDE, pen_at(i, j)))
                else:
                    samples.append((sx, sy, dp, pen_at(i, j)))
                    last_col[i] = (sx, sy)
            self._emit_runs(samples, feed)
        return self

    # ------------------------------------------------------------- strokes
    def poly(self, pts, *, pen=None, feed: Optional[int] = None, halos: bool = True) -> "Scene3D":
        """A plain polyline (no occlusion), split around halo boxes."""
        feed = self.feed if feed is None else feed
        if not halos or not self._boxes:
            self.out.extend(_poly(pts, color=pen, f=feed))
            return self
        run: List[Tuple[float, float]] = []
        for p in pts:
            if self._blocked(p[0], p[1]):
                if len(run) >= 2:
                    self.out.extend(_poly(run, color=pen, f=feed))
                run = []
            else:
                run.append(p)
        if len(run) >= 2:
            self.out.extend(_poly(run, color=pen, f=feed))
        return self

    def emit(self, cmds: Sequence[GCodeCommand]) -> "Scene3D":
        """Pass-through for kit furniture / piece-specific commands."""
        self.out.extend(cmds)
        return self

    # -------------------------------------------------------------- labels
    def halo_labels(self, labels, *, pad_x: float = 1.4, pad_y: Tuple[float, float] = (0.5, 1.35)) -> "Scene3D":
        """Reserve halo boxes NOW (mesh/strokes skip them); glyphs draw at
        render() so they sit on top. labels: (text, x, y, height, pen)."""
        from ..generators import _text_width

        for text, lx, ly, lh, pen in labels:
            w = _text_width(text, lh)
            self._boxes.append((lx - pad_x, ly - pad_y[0] * lh, lx + w + pad_x, ly + pad_y[1] * lh))
            self._labels.append((text, lx, ly, lh, pen))
        return self

    # -------------------------------------------------------------- render
    def render(self) -> List[GCodeCommand]:
        from ..generators import _stroke_text

        for text, lx, ly, lh, pen in self._labels:
            self.out.extend(_stroke_text(text, lx, ly, lh, color=pen, f=self.feed))
        if self.fit == "none" or self.bounds is None:
            return self.out
        if self.fit == "rescue":
            from ..engine3d import _fit_out

            return _fit_out(self.out, self.bounds, inset=self.fit_pad)
        # fit == "fill": always scale + centre into the drawable (manifold idiom)
        xs = [c.x for c in self.out if c.x is not None]
        ys = [c.y for c in self.out if c.y is not None]
        if not xs:
            return self.out
        x0, y0, x1, y1 = self.bounds
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        bw, bh = (bx1 - bx0) or 1.0, (by1 - by0) or 1.0
        s = min((x1 - x0 - 2 * self.fit_pad) / bw, (y1 - y0 - 2 * self.fit_pad) / bh)
        ox = x0 + ((x1 - x0) - bw * s) / 2.0 - bx0 * s
        oy = y0 + ((y1 - y0) - bh * s) / 2.0 - by0 * s
        for c in self.out:
            if c.x is not None:
                c.x = round(c.x * s + ox, 3)
            if c.y is not None:
                c.y = round(c.y * s + oy, 3)
        return self.out
