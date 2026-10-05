"""How a MARK is made, per material — the layer the engine lacked.

``scene3d`` decides where a surface goes, ``kit`` supplies furniture, ``geometry``
clips exactly, ``policies`` de-crowd. None of them said what KIND of stroke a
thing gets. This module does, one grammar per material:

* **cubist planes** — ``hatch_polygon`` + the physical clearance rules
  (``physical_spacing``, ``physical_inset``, ``shadow_cross``).
* **skin, cloth** — ``surface_grid``: a warped (u,v) net whose rows break into
  dashes by an authored tone (``cut_tone``); cross family only in shadow.
* **hair, metal, flowing surfaces** — ``flow_family``: tracks interpolated between
  two authored guides, with a travelling highlight.
* **painterly** — ``brush_family``: neighbouring centerlines around one guide.
  (Image-field strokes and palette quantisation arrive with the acrylic phase.)

Algorithms and constants are those of the reference reconstructions
(``gallery/references/oracles/``), reimplemented on the exact ``geometry``
Regions — no shapely. All coordinates are in whatever units the caller uses;
the compiler maps to mm. Everything returns plain polylines (``List[Poly]``);
the caller decides pen, width and stage.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, NamedTuple, Optional, Sequence, Tuple, Union as _U

import numpy as np

from .geometry import (
    EPS,
    Point,
    Poly,
    Polygon,
    Region,
    Union,
    clip,
    erode_ring,
    offset,
    polyline_length,
    resample_by_arclength,
)

ToneFn = Callable[[np.ndarray, np.ndarray], np.ndarray]

# --------------------------------------------------------------------------- #
# cubist planes                                                               #
# --------------------------------------------------------------------------- #


def hatch_polygon(
    ring: Sequence[Point],
    spacing: float,
    angle_deg: float = 0.0,
    inset: float = 0.0,
    *,
    min_len: float = 1.7,
    phase_lock: bool = True,
) -> List[Poly]:
    """Parallel fill lines clipped EXACTLY to a polygon.

    ``phase_lock`` anchors the line grid to the global origin (not the shape's
    bbox), so two adjacent facets hatched at the same angle and spacing have
    collinear lines — they read as one surface with a fold, not two textures.
    ``inset`` pulls the lines in from the edge (see ``physical_inset``).
    """
    pts = [tuple(p) for p in ring]
    if inset > 0:
        pts = erode_ring(pts, inset)
    if len(pts) < 3:
        return []
    region = Polygon(pts)
    a = math.radians(angle_deg)
    ux, uy = math.cos(a), math.sin(a)  # along the line
    vx, vy = -uy, ux  # across the lines
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    corners = [(xs[0], ys[0]), (xs[0], ys[1]), (xs[1], ys[0]), (xs[1], ys[1])] if False else [
        (min(xs), min(ys)), (min(xs), max(ys)), (max(xs), min(ys)), (max(xs), max(ys))
    ]
    du = [c[0] * ux + c[1] * uy for c in corners]
    dv = [c[0] * vx + c[1] * vy for c in corners]
    u0, u1 = min(du) - 5.0, max(du) + 5.0
    v0, v1 = min(dv), max(dv)
    start = math.floor(v0 / spacing) * spacing if phase_lock else v0 + spacing * 0.5
    out: List[Poly] = []
    d = start
    while d <= v1 + EPS:
        p0 = (vx * d + ux * u0, vy * d + uy * u0)
        p1 = (vx * d + ux * u1, vy * d + uy * u1)
        for run in clip([p0, p1], region, keep="inside"):
            if polyline_length(run) >= min_len:
                out.append(run)
        d += spacing
    return out


def physical_spacing(spacing: float, nib_fine_mm: float, page_scale: float, density: float = 1.0) -> float:
    """Hatch spacing in source units, floored so two neighbouring lines keep paper
    between them: never closer than 2.4 × the finest nib (1 nib of ink, 1.4 of
    white). ``density`` scales the AUTHORED spacing; it cannot beat the floor."""
    return max(spacing / max(density, 1e-9), nib_fine_mm * 2.4 / page_scale)


def physical_inset(inset: float, nib_border_mm: float, nib_fine_mm: float, page_scale: float) -> float:
    """Hatch inset from the bounding contour, in source units: half the outline's
    ink, half the hatch's own ink, plus 0.035 mm of guaranteed white paper, so a
    hatch line never fuses with the edge that bounds it."""
    return max(inset, (0.5 * nib_border_mm + 0.5 * nib_fine_mm + 0.035) / page_scale)


def shadow_cross(rule: Dict) -> Dict:
    """The second family a shadow plane gets: +67° (an oblique lozenge reads as
    tone; a square grid reads as a grid) and 1.5× sparser."""
    r = dict(rule)
    r["angle"] = rule.get("angle", 0.0) + 67.0
    r["spacing"] = rule["spacing"] * 1.5
    return r


# --------------------------------------------------------------------------- #
# tone → marks                                                                #
# --------------------------------------------------------------------------- #


def _tone_array(tone, n: int, pts: Poly) -> np.ndarray:
    if callable(tone):
        xs = np.array([p[0] for p in pts], dtype=float)
        ys = np.array([p[1] for p in pts], dtype=float)
        return np.clip(np.asarray(tone(xs, ys), dtype=float), 0.0, 1.0)
    return np.clip(np.broadcast_to(np.asarray(tone, dtype=float), (n,)), 0.0, 1.0)


def cut_tone(
    poly: Poly,
    tone,
    *,
    period: float = 6.0,
    phase: float = 0.0,
    continuous_at: float = 0.71,
    min_len: float = 0.66,
    min_samples: int = 2,
) -> List[Poly]:
    """Tone → a duty cycle of visible stroke intervals, along ARC LENGTH.

    Spatial PWM: within each ``period`` the first ``period·duty`` is inked, with
    ``duty = (tone − 0.06) / 0.65`` (so tone 0.71 is a solid line), nothing at all
    below tone 0.13, and ``phase`` shifting where the gaps fall so adjacent lines
    are staggered. ``tone`` may be a scalar, a per-point array, or ``f(xs, ys)``.
    Returns real separate polylines — no dash arrays, no opacity.
    """
    pts = [tuple(p) for p in poly]
    n = len(pts)
    if n < 2:
        return []
    seg = np.hypot(
        np.diff([p[0] for p in pts]), np.diff([p[1] for p in pts])
    )
    d = np.concatenate([[0.0], np.cumsum(seg)])
    t = _tone_array(tone, n, pts)
    duty = np.clip((t - 0.06) / 0.65, 0.0, 1.0)
    active = (((d + phase) % period) < period * duty) | (t >= continuous_at)
    active &= t > 0.13
    return _chunks(pts, active, min_len=min_len, min_samples=min_samples)


def _chunks(pts: Poly, good: np.ndarray, *, min_len: float, min_samples: int) -> List[Poly]:
    """Run-length extraction over a boolean mask, with sample-count and physical
    length floors so no dotty crumbs are emitted."""
    g = np.concatenate([[False], good.astype(bool), [False]]).astype(np.int8)
    changes = np.flatnonzero(np.diff(g))
    out: List[Poly] = []
    for a, b in zip(changes[0::2], changes[1::2]):
        if b - a < min_samples:
            continue
        q = pts[a:b]
        if polyline_length(q) >= min_len:
            out.append(list(q))
    return out


def gauss_tone(base: float, lobes: Sequence[Tuple[float, float, float, float, float]]) -> ToneFn:
    """The authored tone-function form: ``base + Σ aᵢ·G(u,v; xᵢ,yᵢ,sxᵢ,syᵢ)``.

    Each lobe is ``(amplitude, x, y, sx, sy)`` in normalised surface coordinates;
    positive amplitude = shadow, negative = lit plane or highlight. A narrow ``sx``
    with a tall ``sy`` makes the vertical shadow rail down one side of a limb.
    """
    lobes = [tuple(map(float, l)) for l in lobes]

    def f(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        u = np.asarray(u, dtype=float)
        v = np.asarray(v, dtype=float)
        acc = np.full(np.broadcast(u, v).shape, float(base))
        for a, x, y, sx, sy in lobes:
            acc = acc + a * np.exp(-0.5 * (((u - x) / sx) ** 2 + ((v - y) / sy) ** 2))
        return acc

    return f


# --------------------------------------------------------------------------- #
# hair, metal, flowing surfaces                                               #
# --------------------------------------------------------------------------- #


class FlowFamily(NamedTuple):
    tracks: List[Poly]  # the interpolated family (possibly broken by the highlight)
    rims: List[Poly]  # two heavy edge strokes when dark_edge=True, else []
    count: int  # how many tracks the width admitted


def _clip_many(runs: List[Poly], region: Optional[Region], min_len: float) -> List[Poly]:
    if region is None:
        return [r for r in runs if polyline_length(r) >= min_len]
    out: List[Poly] = []
    for r in runs:
        for piece in clip(r, region, keep="inside"):
            if polyline_length(piece) >= min_len:
                out.append(piece)
    return out


def flow_family(
    guide_a: Sequence[Point],
    guide_b: Sequence[Point],
    spacing: float,
    region: Optional[Region] = None,
    *,
    highlight: bool = False,
    dark_edge: bool = False,
    pitch: float = 1.0,
    u_range: Tuple[float, float] = (0.03, 0.97),
    n_max: int = 180,
    min_len: float = 0.7,
    count: Optional[int] = None,
) -> FlowFamily:
    """Two authored guide curves → a coherent family of tracks between them.

    Both guides are resampled to the same N (≈ one sample per ``pitch`` units of
    the longer guide), so they correspond point-for-point by fraction of length.
    The track count comes from the **76th percentile of the perpendicular width**
    divided by ``spacing`` — a lobe that pinches to a point at its tips keeps the
    density its fat part deserves while the tips simply converge. Tracks sit at
    ``u ∈ linspace(0.03, 0.97, n)``, never on the guides themselves.

    ``highlight`` cuts a narrow Gaussian notch (σ = 2.6 % of track length) whose
    position drifts sinusoidally across the family — shine as a real gap that
    travels, not a grey. ``dark_edge`` adds two rim strokes hugging the guides.
    """
    La, Lb = polyline_length(guide_a), polyline_length(guide_b)
    nn = max(40, int(max(La, Lb) / max(pitch, 1e-9)))
    a = np.array(resample_by_arclength(guide_a, n=nn), dtype=float)
    b = np.array(resample_by_arclength(guide_b, n=nn), dtype=float)

    centre = (a + b) / 2.0
    tangent = np.gradient(centre, axis=0)
    tl = np.hypot(tangent[:, 0], tangent[:, 1])
    tl[tl < EPS] = 1.0
    tangent = tangent / tl[:, None]
    delta = b - a
    widths = np.abs(delta[:, 0] * tangent[:, 1] - delta[:, 1] * tangent[:, 0])
    if count is not None:
        n = max(1, int(count))  # caller decides (brush_family); the width rule is bypassed
    else:
        n = int(np.percentile(widths, 76) / max(spacing, 1e-9))
        n = max(2, min(n_max, n))

    v = np.linspace(0.0, 1.0, nn)
    tracks: List[Poly] = []
    for j, u in enumerate(np.linspace(u_range[0], u_range[1], n)):
        p = (1.0 - u) * a + u * b
        poly = [tuple(q) for q in p]
        if highlight:
            center = 0.34 + 0.055 * math.sin(2.8 * u + 0.4)
            shine = np.exp(-0.5 * ((v - center) / 0.026) ** 2)
            tone = np.clip(0.93 - 1.00 * shine, 0.0, 1.0)
            runs = cut_tone(poly, tone, period=4.0, phase=j * 0.91, min_len=min_len)
        else:
            runs = [poly]
        tracks.extend(_clip_many(runs, region, min_len))

    rims: List[Poly] = []
    if dark_edge:
        for f in (0.025, 0.975):
            p = (1.0 - f) * a + f * b
            rims.extend(_clip_many([[tuple(q) for q in p]], region, min_len))
    return FlowFamily(tracks, rims, n)


def brush_family(
    guide: Sequence[Point],
    n: int,
    spread: float,
    region: Optional[Region] = None,
    *,
    pitch: float = 1.0,
) -> List[Poly]:
    """Painterly: ``n`` neighbouring centerlines around ONE authored guide, spread
    ``spread`` units across, via smooth normal offsets. This is ``flow_family``
    between the two offset rails of the guide."""
    if n <= 1:
        return _clip_many([[tuple(p) for p in guide]], region, 0.0)
    ra = offset(list(guide), -spread / 2.0)
    rb = offset(list(guide), +spread / 2.0)
    fam = flow_family(ra, rb, spread / max(n - 1, 1), region, pitch=pitch, u_range=(0.0, 1.0), count=n)
    return fam.tracks


# --------------------------------------------------------------------------- #
# skin, cloth                                                                 #
# --------------------------------------------------------------------------- #


class SurfaceGrid(NamedTuple):
    rows: List[Poly]  # the primary warped-row family
    cross: List[Poly]  # the oblique family, present only in shadow


def _ellipse_ring(xa: float, ya: float, xb: float, yb: float, n: int = 32) -> List[Point]:
    cx, cy = (xa + xb) / 2.0, (ya + yb) / 2.0
    rx, ry = abs(xb - xa) / 2.0, abs(yb - ya) / 2.0
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


def surface_grid(
    ring: Sequence[Point],
    tone: ToneFn,
    *,
    row_spacing: float = 2.7,
    bend: float = 8.0,
    slope: float = 0.0,
    protect: Sequence[Tuple[float, float, float, float]] = (),
    cross: bool = True,
    mode: str = "skin",
    erode: float = 0.7,
    pitch: float = 0.38,
    min_len: float = 0.66,
) -> SurfaceGrid:
    """A curved (u,v) net over a form, its rows broken to dashes by an authored tone.

    The warp is a bilinear box map plus one sinusoidal bulge
    ``bend·sin(πu)·sin(πv)`` (peaks at the centre, vanishes on every edge — what
    makes a face read convex; negative bend = concave) and a linear shear
    ``slope·(u − 0.5)``. Rows go through ``cut_tone`` with the golden-ratio phase
    ``j · 0.381966 · period`` so highlight gaps never line up into a seam. The
    oblique cross family (slope 0.88 in uv, 1.30× sparser) is admitted only where
    ``(tone − 0.40)·2.7 > 0`` — genuine shadow — and ramps in fast. ``protect`` boxes
    ``(xa, ya, xb, yb)`` become elliptical holes: eyes and lips stay open.

    ``tone(u, v)`` takes and returns numpy arrays over normalised surface coords.
    """
    pts = [tuple(p) for p in ring]
    inner = erode_ring(pts, erode) if erode > 0 else pts
    if len(inner) < 3:
        return SurfaceGrid([], [])
    region: Region = Polygon(inner)
    holes = [Polygon(_ellipse_ring(*box)) for box in protect]
    if holes:
        region = region & ~(holes[0] if len(holes) == 1 else Union(*holes))

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, y0 = min(xs), min(ys)
    bw, bh = (max(xs) - x0) or 1.0, (max(ys) - y0) or 1.0

    def warp(u: np.ndarray, v: np.ndarray) -> Poly:
        x = x0 + u * bw
        y = y0 + v * bh + bend * np.sin(np.pi * u) * np.sin(np.pi * v) + slope * (u - 0.5)
        return list(zip(x.tolist(), y.tolist()))

    us = np.linspace(-0.08, 1.08, max(100, int(bw / pitch)))
    period = 5.7 if mode == "skin" else 8.3

    rows: List[Poly] = []
    for j, vv in enumerate(np.arange(-0.08, 1.09, row_spacing / bh)):
        v = np.full_like(us, vv)
        p = warp(us, v)
        tv = np.clip(tone(us, v), 0.0, 1.0)
        runs = cut_tone(p, tv, period=period, phase=j * 0.381966 * 5.7, min_len=min_len)
        rows.extend(_clip_many(runs, region, min_len))

    crossed: List[Poly] = []
    if cross:
        for j, b in enumerate(np.arange(-1.0, 1.1, row_spacing * 1.30 / bh)):
            v = b + us * 0.88
            p = warp(us, v)
            tv = np.clip((tone(us, v) - 0.40) * 2.7, 0.0, 1.0)
            tv[(v < -0.07) | (v > 1.07)] = 0.0
            runs = cut_tone(p, tv, period=7.2, phase=j * 2.41, continuous_at=0.81, min_len=min_len)
            crossed.extend(_clip_many(runs, region, min_len))
    return SurfaceGrid(rows, crossed)


# --------------------------------------------------------------------------- #
# painterly: the image as a field of colour + orientation                     #
# --------------------------------------------------------------------------- #


class ImageGrid(NamedTuple):
    """A reference image resampled onto a paper-space cell grid.

    ``rgb[j, i]`` is the cell's colour in 0..1 (row j is paper-UP, so j=0 is the
    bottom); ``tone[j, i]`` its darkness; ``tangent(i, j)`` the local contour
    direction (radians) and ``coherence(i, j)`` how organised the structure is
    (1 = a clear edge, 0 = flat). Cell (i, j) covers paper
    ``x0 + i·cell .. x0 + (i+1)·cell``, same for y.
    """

    gw: int
    gh: int
    x0: float
    y0: float
    cell: float
    rgb: np.ndarray
    tone: np.ndarray
    tangent: Callable[[int, int], float]
    coherence: Callable[[int, int], float]

    def cell_of(self, x: float, y: float) -> Tuple[int, int]:
        i = int((x - self.x0) / self.cell)
        j = int((y - self.y0) / self.cell)
        return min(self.gw - 1, max(0, i)), min(self.gh - 1, max(0, j))

    def rgb_at(self, x: float, y: float) -> Tuple[float, float, float]:
        i, j = self.cell_of(x, y)
        return tuple(float(v) for v in self.rgb[j, i])

    def tangent_at(self, x: float, y: float) -> float:
        return self.tangent(*self.cell_of(x, y))

    def coherence_at(self, x: float, y: float) -> float:
        return self.coherence(*self.cell_of(x, y))


def load_image_grid(path: str, bounds: Tuple[float, float, float, float], cell: float = 2.0) -> ImageGrid:
    """Cover-fit a reference image onto ``bounds`` (auto-rotating to match the
    paper's orientation, centre-cropping overflow — the house image-fit rule) and
    return colour + tone + a structure-tensor orientation field per cell.

    This is the painterly grammar's substrate: colour is SAMPLED here then
    quantised; strokes FOLLOW the tangent field. Nothing here is a tracing — the
    designer still authors the guides and decides what is drawn.
    """
    try:
        from PIL import Image
    except ImportError:  # pragma: no cover
        raise RuntimeError("Pillow required for image input: pip install -e '.[vision]'")
    from ..generators import _image_orientation_grid

    x0, y0, x1, y1 = bounds
    bw, bh = x1 - x0, y1 - y0
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    if (iw >= ih) != (bw >= bh):
        img = img.transpose(Image.ROTATE_90)
        iw, ih = ih, iw
    sc = max(bw / iw, bh / ih)
    crop_w, crop_h = min(iw, bw / sc), min(ih, bh / sc)
    left, top = (iw - crop_w) / 2.0, (ih - crop_h) / 2.0
    img = img.crop((int(left), int(top), int(left + crop_w), int(top + crop_h)))
    gw, gh = max(2, int(bw / cell)), max(2, int(bh / cell))
    small = np.asarray(img.resize((gw, gh)), dtype=float) / 255.0  # (gh, gw, 3), image y down
    rgb = small[::-1, :, :].copy()  # flip to paper-up rows
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    tone = 1.0 - lum

    def tone_fn(i: int, j: int) -> float:
        return float(tone[j, i])

    tangent, coherence = _image_orientation_grid(gw, gh, tone_fn)
    return ImageGrid(gw, gh, x0, y0, cell, rgb, tone, tangent, coherence)


def quantize_palette(rgb: np.ndarray, k: int = 10) -> List[Tuple[float, float, float]]:
    """Median-cut quantisation of an (N,3) or (H,W,3) 0..1 colour array to ``k``
    representative colours, sorted dark → light. Deterministic; no sklearn."""
    pts = np.asarray(rgb, dtype=float).reshape(-1, 3)
    if len(pts) == 0:
        return []
    boxes = [pts]
    while len(boxes) < k:
        # split the box with the largest colour range along its widest channel
        spans = [b.max(axis=0) - b.min(axis=0) if len(b) > 1 else np.zeros(3) for b in boxes]
        idx = int(np.argmax([s.max() for s in spans]))
        b = boxes[idx]
        if len(b) < 2 or spans[idx].max() < 1e-6:
            break
        ch = int(np.argmax(spans[idx]))
        order = np.argsort(b[:, ch], kind="stable")
        b = b[order]
        mid = len(b) // 2
        boxes[idx : idx + 1] = [b[:mid], b[mid:]]
    pal = [tuple(float(v) for v in b.mean(axis=0)) for b in boxes if len(b)]
    pal.sort(key=lambda c: 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2])
    return pal


def snap_color(rgb: Tuple[float, float, float], palette: Sequence[Tuple[float, float, float]]) -> int:
    """Index of the nearest palette colour (Euclidean in RGB; good enough for a
    ten-paint plate, and cheap)."""
    p = np.asarray(palette, dtype=float)
    d = ((p - np.asarray(rgb, dtype=float)) ** 2).sum(axis=1)
    return int(np.argmin(d))


def flow_strokes(
    grid: ImageGrid,
    region: Optional[Region],
    rng,
    *,
    length: float = 6.0,
    step: float = 0.8,
    density: float = 0.35,
    coherence_min: float = 0.15,
    jitter: float = 0.45,
    palette: Optional[Sequence[Tuple[float, float, float]]] = None,
    pitch: Optional[float] = None,
    brush_mm: Optional[float] = None,
    overlap: float = 0.85,
) -> List[Tuple[Poly, Optional[int]]]:
    """Short curved strokes riding the image's orientation field.

    Two seeding regimes:

    * **scatter** (default) — seeds on the image's own cell grid at ``density``
      per cell. Marks sit ON the picture where it has structure; paper shows
      between them. Good for an accent layer over paint that is already there.
    * **coverage** — pass ``brush_mm`` (or an explicit ``pitch``) and the seeds
      go on a lattice of pitch ``brush_mm · overlap``, EVERY cell, so adjacent
      footprints touch and the passes tile the sheet with no bare paper. This is
      what an underpainting is: you are covering a ground, not decorating one.
      ``coherence_min`` is ignored here — flat regions need paint too, they just
      take the field's smoothed direction.

    Each stroke is traced ``length``/2 either way along the tangent. Returns
    ``(polyline, palette_index)``, the index being the sampled colour snapped to
    ``palette``. Direction and colour come from the image; WHERE strokes are laid
    at all remains the designer's call (pass a ``region``).
    """
    out: List[Tuple[Poly, Optional[int]]] = []
    half = max(1, int((length / 2.0) / step))
    covering = pitch is not None or brush_mm is not None
    if covering:
        p = pitch if pitch is not None else float(brush_mm) * overlap
        p = max(p, 1e-6)
        nx_cells = max(1, int(math.ceil(grid.gw * grid.cell / p)))
        ny_cells = max(1, int(math.ceil(grid.gh * grid.cell / p)))
        seeds = (
            (grid.x0 + (i + 0.5) * p, grid.y0 + (j + 0.5) * p)
            for j in range(ny_cells)
            for i in range(nx_cells)
        )
        jit = jitter * p
    else:
        seeds = (
            (grid.x0 + (i + 0.5) * grid.cell, grid.y0 + (j + 0.5) * grid.cell)
            for j in range(grid.gh)
            for i in range(grid.gw)
        )
        jit = jitter * grid.cell

    for cx, cy in seeds:
        if not covering:
            if rng.random() > density:
                continue
            i, j = grid.cell_of(cx, cy)
            if grid.coherence(i, j) < coherence_min:
                continue
        sx = cx + (rng.random() - 0.5) * 2 * jit
        sy = cy + (rng.random() - 0.5) * 2 * jit
        if region is not None and not region.contains(sx, sy):
            continue
        fwd: List[Point] = []
        back: List[Point] = []
        for sign, acc in ((1.0, fwd), (-1.0, back)):
            x, y = sx, sy
            for _ in range(half):
                a = grid.tangent_at(x, y)
                nx, ny = x + sign * step * math.cos(a), y + sign * step * math.sin(a)
                if region is not None and not region.contains(nx, ny):
                    break
                acc.append((nx, ny))
                x, y = nx, ny
        poly = list(reversed(back)) + [(sx, sy)] + fwd
        if len(poly) < 2:
            continue
        idx = snap_color(grid.rgb_at(sx, sy), palette) if palette else None
        out.append((poly, idx))
    return out


# --------------------------------------------------------------------------- #
# de-crowding for hatch families                                              #
# --------------------------------------------------------------------------- #


def suppress_parallel(
    paths: Sequence[Poly],
    *,
    min_dist: float = 1.55,
    align: float = 0.93,
    sample: float = 0.75,
    min_run_pts: int = 3,
    min_run_len: float = 3.0,
) -> List[Poly]:
    """Drop the parts of a hatch stroke that run too close AND nearly parallel to
    a stroke already kept (|cos θ| > ``align`` ≈ within 21°). Crossing strokes may
    pass arbitrarily close — that is a crosshatch, not a blot. Longest strokes
    claim space first. Grid-hash neighbour lookup; no scipy."""
    if not paths:
        return []
    cell = max(min_dist, 1e-6)
    grid: Dict[Tuple[int, int], List[Tuple[float, float, float, float]]] = {}

    def key(x: float, y: float) -> Tuple[int, int]:
        return (int(math.floor(x / cell)), int(math.floor(y / cell)))

    def near(x: float, y: float):
        kx, ky = key(x, y)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for item in grid.get((kx + dx, ky + dy), ()):
                    yield item

    kept: List[Poly] = []
    for poly in sorted(paths, key=lambda p: -polyline_length(p)):
        pts = resample_by_arclength(poly, step=sample)
        if len(pts) < 2:
            continue
        arr = np.array(pts, dtype=float)
        tang = np.gradient(arr, axis=0)
        tl = np.hypot(tang[:, 0], tang[:, 1])
        tl[tl < EPS] = 1.0
        tang = tang / tl[:, None]
        good = np.ones(len(pts), dtype=bool)
        for i, (x, y) in enumerate(pts):
            for qx, qy, tx, ty in near(x, y):
                if math.hypot(qx - x, qy - y) < min_dist and abs(tang[i, 0] * tx + tang[i, 1] * ty) > align:
                    good[i] = False
                    break
        for run in _chunks(pts, good, min_len=min_run_len, min_samples=min_run_pts):
            kept.append(run)
            rr = np.array(run, dtype=float)
            rt = np.gradient(rr, axis=0)
            rl = np.hypot(rt[:, 0], rt[:, 1])
            rl[rl < EPS] = 1.0
            rt = rt / rl[:, None]
            for (x, y), (tx, ty) in zip(run, rt):
                grid.setdefault(key(x, y), []).append((x, y, float(tx), float(ty)))
    return kept
