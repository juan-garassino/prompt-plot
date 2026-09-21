"""Shared 2D design kit — style-neutral line primitives for every piece.

Fills (serpentine/spiral/arc), orbits, marks, swatch bars, spaced-caps
single-stroke type, run clipping/fitting utilities, and re-exports of the
low-level generators helpers so pieces have ONE import site. Style (palette,
furniture system) is chosen at the LAMINA level — see ``promptplot/lamina``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from ...models import GCodeCommand
from ..generators import (  # noqa: F401  (re-exported for pieces)
    _GLYPHS,
    _glyph_advance,
    _attention_matrix,
    _catmull_subdivide,
    _chain_segments,
    _dot,
    _limit_overdraw,
    _marching_squares,
    _poly,
    _stroke_text,
    _text_width,
)

Bounds = Tuple[float, float, float, float]

BAUHAUS_PALETTE = ["dodgerblue", "deeppink", "black"]
BLUE, PINK, BLACK = 0, 1, 2



def _pen(idx: int, colors: int) -> Optional[int]:
    return idx % colors if colors > 1 else None




# ---------------------------------------------------------------------------
# fills
# ---------------------------------------------------------------------------


def fill_rect(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    spacing: float = 0.55,
    pen: Optional[int] = None,
    f: int = 2200,
) -> List[GCodeCommand]:
    """Solid rectangle as one serpentine polyline."""
    pts = []
    y = y0
    flip = False
    while y <= y1 + 1e-9:
        row = [(x0, y), (x1, y)]
        pts.extend(reversed(row) if flip else row)
        flip = not flip
        y += spacing
    return _poly(pts, color=pen, f=f)




def fill_disc(
    cx: float, cy: float, r: float, spacing: float = 0.5, pen: Optional[int] = None, f: int = 2200
) -> List[GCodeCommand]:
    """Solid disc as one Archimedean spiral."""
    turns = max(2, int(r / spacing))
    n = turns * 30
    pts = []
    for k in range(n + 1):
        t = k / n
        rr = r * t
        a = 2 * math.pi * turns * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _poly(pts, color=pen, f=f)




def fill_quarter(
    cx: float,
    cy: float,
    r: float,
    a_start: float,
    spacing: float = 0.55,
    pen: Optional[int] = None,
    f: int = 2200,
) -> List[GCodeCommand]:
    """Solid quarter-disc as concentric arcs."""
    out: List[GCodeCommand] = []
    rr = r
    while rr > 0.3:
        arc = []
        a = a_start
        while a <= a_start + math.pi / 2 + 1e-6:
            arc.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
            a += 0.08
        out += _poly(arc, color=pen, f=f)
        rr -= spacing
    return out




def fill_ring(
    cx: float,
    cy: float,
    r0: float,
    r1: float,
    spacing: float = 0.55,
    pen: Optional[int] = None,
    f: int = 2200,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    rr = r0
    while rr <= r1 + 1e-9:
        ring = [
            (cx + rr * math.cos(2 * math.pi * k / 72), cy + rr * math.sin(2 * math.pi * k / 72))
            for k in range(73)
        ]
        out += _poly(ring, color=pen, f=f)
        rr += spacing
    return out




# ---------------------------------------------------------------------------
# geometry: runs, clipping (crop-at-frame + knockouts), cover-fit
# ---------------------------------------------------------------------------


def _runs_from_cmds(cmds: Sequence[GCodeCommand]) -> List[List[Tuple[float, float]]]:
    """Extract pen-down polylines from a command list."""
    runs: List[List[Tuple[float, float]]] = []
    cur: List[Tuple[float, float]] = []
    for c in cmds:
        if c.command == "G0":
            if len(cur) >= 2:
                runs.append(cur)
            cur = [(c.x, c.y)] if c.x is not None else []
        elif c.command == "G1" and c.x is not None:
            cur.append((c.x, c.y))
    if len(cur) >= 2:
        runs.append(cur)
    return runs




def _runs_from_cmds_pens(
    cmds: Sequence[GCodeCommand],
) -> List[Tuple[Optional[int], List[Tuple[float, float]]]]:
    """Like ``_runs_from_cmds`` but keeps each run's pen index.

    ``_runs_from_cmds`` drops ``GCodeCommand.color``, so a piece that round-trips
    commands -> runs -> commands (clipping a multi-pen composition, for example)
    silently collapses every pen onto one. Use this when the pen matters.
    """
    runs: List[Tuple[Optional[int], List[Tuple[float, float]]]] = []
    cur: List[Tuple[float, float]] = []
    pen: Optional[int] = None
    for c in cmds:
        if c.command == "G0":
            if len(cur) >= 2:
                runs.append((pen, cur))
            cur = [(c.x, c.y)] if c.x is not None else []
            pen = getattr(c, "color", None)
        elif c.command == "G1" and c.x is not None:
            if not cur:
                pen = getattr(c, "color", None)
            elif getattr(c, "color", None) is not None:
                pen = c.color
            cur.append((c.x, c.y))
    if len(cur) >= 2:
        runs.append((pen, cur))
    return runs


def _cut(inside, outside, keep, iters=14):
    """Bisect the crossing point between an inside and an outside point."""
    a, b = inside, outside
    for _ in range(iters):
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        if keep(m):
            a = m
        else:
            b = m
    return a




def _clip_runs(runs, keep) -> List[List[Tuple[float, float]]]:
    """Clip polylines to a boolean keep-region, cutting segments at the edge."""
    out: List[List[Tuple[float, float]]] = []
    for pts in runs:
        cur: List[Tuple[float, float]] = []
        for i, p in enumerate(pts):
            if i == 0:
                if keep(p):
                    cur.append(p)
                continue
            a = pts[i - 1]
            ka, kb = keep(a), keep(p)
            if ka and kb:
                if not cur:
                    cur = [a]
                cur.append(p)
            elif ka and not kb:
                if not cur:
                    cur = [a]
                cur.append(_cut(a, p, keep))
                if len(cur) >= 2:
                    out.append(cur)
                cur = []
            elif kb and not ka:
                cur = [_cut(p, a, keep), p]
        if len(cur) >= 2:
            out.append(cur)
    return out




def _rect_keep(region: Bounds, inset: float = 0.0):
    rx0, ry0, rx1, ry1 = region
    return lambda p: rx0 + inset <= p[0] <= rx1 - inset and ry0 + inset <= p[1] <= ry1 - inset




def _fit_runs_cover(runs, target: Bounds) -> List[List[Tuple[float, float]]]:
    """Uniform-scale + recenter runs so their bbox COVERS the target rect
    (overshoots on one axis — made for cropping at the frame)."""
    xs = [p[0] for r in runs for p in r]
    ys = [p[1] for r in runs for p in r]
    if not xs:
        return runs
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    tx0, ty0, tx1, ty1 = target
    s = max((tx1 - tx0) / max(1e-9, bx1 - bx0), (ty1 - ty0) / max(1e-9, by1 - by0))
    bcx, bcy = (bx0 + bx1) / 2, (by0 + by1) / 2
    tcx, tcy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
    return [[(tcx + (px - bcx) * s, tcy + (py - bcy) * s) for px, py in r] for r in runs]




def _emit_runs(runs, pen: Optional[int], f: int = 2200) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for r in runs:
        out += _poly(r, color=pen, f=f)
    return out





# ---------------------------------------------------------------------------
# furniture
# ---------------------------------------------------------------------------


def circle(
    cx: float, cy: float, r: float, pen: Optional[int] = None, f: int = 2200, n: int = 96
) -> List[GCodeCommand]:
    ring = [
        (cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n))
        for k in range(n + 1)
    ]
    return _poly(ring, color=pen, f=f)




def dotted_circle(
    cx: float,
    cy: float,
    r: float,
    pen: Optional[int] = None,
    bounds: Optional[Bounds] = None,
    f: int = 2200,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    seg: List[Tuple[float, float]] = []
    for k in range(241):
        a = 2 * math.pi * k / 240
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        ok = (k % 6) < 2
        if ok and bounds is not None:
            ok = bounds[0] + 0.5 < px < bounds[2] - 0.5 and bounds[1] + 0.5 < py < bounds[3] - 0.5
        if ok:
            seg.append((px, py))
        else:
            if len(seg) >= 2:
                out += _poly(seg, color=pen, f=f)
            seg = []
    if len(seg) >= 2:
        out += _poly(seg, color=pen, f=f)
    return out




def plus_mark(
    x: float, y: float, s: float = 1.0, pen: Optional[int] = None, f: int = 2200
) -> List[GCodeCommand]:
    return _poly([(x - s, y), (x + s, y)], color=pen, f=f) + _poly(
        [(x, y - s), (x, y + s)], color=pen, f=f
    )




def crosshair_rules(
    bounds: Bounds,
    xs: Sequence[float] = (),
    ys: Sequence[float] = (),
    pen: Optional[int] = None,
    f: int = 2200,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    out: List[GCodeCommand] = []
    for x in xs:
        out += _poly([(x, y0 + 0.5), (x, y1 - 0.5)], color=pen, f=f)
    for y in ys:
        out += _poly([(x0 + 0.5, y), (x1 - 0.5, y)], color=pen, f=f)
    return out




def swatch_bar(
    x: float,
    y_top: float,
    pens: Sequence[Optional[int]],
    size: float = 2.2,
    spacing: float = 0.5,
    f: int = 2200,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    y = y_top
    for pen in pens:
        out += fill_rect(x, y - size, x + size * 0.82, y, spacing=spacing, pen=pen, f=f)
        y -= size + 0.7
    return out




# ---------------------------------------------------------------------------
# type
# ---------------------------------------------------------------------------


def _spaced(text: str) -> str:
    return " ".join(text)




def type_block(
    lines: Sequence[str],
    x: float,
    y_top: float,
    height: float = 2.6,
    pen: Optional[int] = None,
    underline: bool = True,
    f: int = 2200,
) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    y = y_top
    for ln in lines:
        out += _stroke_text(_spaced(ln), x, y, height, color=pen, f=f)
        y -= height * 2.0
    if underline:
        out += _poly(
            [(x, y + height * 2.0 - 2.0), (x + 6.0, y + height * 2.0 - 2.0)], color=pen, f=f
        )
    return out




# ---------------------------------------------------------------------------
# style kit — the helpers STYLES.md has always required and nobody had built.
# Without these the only type tool was caption-sized `type_block` and the only
# marks were drafting furniture, so every piece defaulted to technical drawing.
# ---------------------------------------------------------------------------


def _offset_polyline(pts: Sequence[Tuple[float, float]], d: float) -> List[Tuple[float, float]]:
    """Offset a polyline by ``d`` along per-vertex averaged normals."""
    n = len(pts)
    if n < 2:
        return list(pts)
    out: List[Tuple[float, float]] = []
    for i, (px, py) in enumerate(pts):
        nxs, nys = 0.0, 0.0
        for a, b in ((i - 1, i), (i, i + 1)):
            if a < 0 or b >= n:
                continue
            dx, dy = pts[b][0] - pts[a][0], pts[b][1] - pts[a][1]
            L = math.hypot(dx, dy)
            if L < 1e-9:
                continue
            nxs -= dy / L
            nys += dx / L
        L = math.hypot(nxs, nys)
        if L < 1e-9:
            out.append((px, py))
        else:
            out.append((px + d * nxs / L, py + d * nys / L))
    return out


def giant_type(
    text: str,
    x: float,
    y: float,
    height: float,
    pen: Optional[int] = None,
    weight: float = 0.0,
    tip: float = 0.55,
    spaced: bool = False,
    angle: float = 0.0,
    proportional: bool = False,
    f: int = 2200,
) -> List[GCodeCommand]:
    """Display-scale stroke type with real WEIGHT — type as mass, not caption.

    The single-stroke font is a hairline at any size, which is why posters kept
    coming out as drafting sheets. ``weight`` (mm) thickens each glyph stroke
    into a band of parallel passes at ``tip`` spacing, so a Bauhaus or Swiss
    headline reads as a black shape from three metres.
    """
    sc = height / 6.0
    adv = 5.6 * sc
    passes = max(1, int(round(weight / max(tip, 0.05))) + 1) if weight > 0 else 1
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))

    def place(gx, gy, cursor):
        """Glyph coords -> sheet, rotated about the (x, y) anchor."""
        lx, ly = cursor - x + gx * sc, gy * sc
        return (x + lx * ca - ly * sa, y + lx * sa + ly * ca)

    out: List[GCodeCommand] = []
    cx = x
    for ch in (_spaced(text) if spaced else text):
        strokes = _GLYPHS.get(ch)
        if strokes is None:
            strokes = _GLYPHS.get(ch.upper(), [])
        for stroke in strokes:
            pts = [place(gx, gy, cx) for gx, gy in stroke]
            if passes == 1:
                out += _poly(pts, color=pen, f=f)
                continue
            for k in range(passes):
                d = -weight / 2.0 + weight * k / (passes - 1)
                out += _poly(_offset_polyline(pts, d), color=pen, f=f)
        cx += _glyph_advance(ch) * sc if proportional else adv
    return out


def giant_type_width(text: str, height: float, spaced: bool = False) -> float:
    return _text_width(_spaced(text) if spaced else text, height)


def concentric_disc(
    cx: float,
    cy: float,
    r: float,
    rings: int = 9,
    pen: Optional[int] = None,
    seg: int = 96,
    f: int = 2200,
) -> List[GCodeCommand]:
    """A circle of N evenly spaced rings — the Bauhaus poster disc."""
    out: List[GCodeCommand] = []
    for k in range(1, rings + 1):
        out += circle(cx, cy, r * k / rings, pen=pen, f=f, n=seg)
    return out


def benday_fill(
    region: Bounds,
    spacing: float = 3.0,
    r_max: float = 1.0,
    pen: Optional[int] = None,
    tone=None,
    stagger: bool = True,
    seg: int = 10,
    f: int = 2200,
) -> List[GCodeCommand]:
    """Pop-art Ben-Day lattice: a regular dot grid whose RADIUS carries tone.

    ``tone(x, y) -> 0..1`` scales each dot; omit it for a flat lattice. The grid
    stays strictly regular — mechanical reproduction is the point, so the dots
    must not wander.
    """
    x0, y0, x1, y1 = region
    out: List[GCodeCommand] = []
    row = 0
    yy = y0 + spacing * 0.5
    while yy <= y1:
        xx = x0 + spacing * 0.5 + (spacing * 0.5 if (stagger and row % 2) else 0.0)
        while xx <= x1:
            t = 1.0 if tone is None else max(0.0, min(1.0, tone(xx, yy)))
            r = r_max * math.sqrt(t)
            if r > 0.12:
                out += circle(xx, yy, r, pen=pen, f=f, n=seg)
            xx += spacing
        yy += spacing
        row += 1
    return out


def even_contour_levels(
    field: Sequence[Sequence[float]],
    spacing: float,
    quantile: float = 0.82,
    n_max: int = 80,
    cell: float = 1.0,
) -> List[float]:
    """Iso-values chosen so the resulting RINGS sit a fixed distance apart.

    Evenly spaced iso-VALUES bunch wherever the field is steep, so a contour
    nest either floods solid in the steep band or has to be thinned into crumbs
    afterwards. Stepping the level by ``spacing * quantile(|grad F|)`` instead
    puts rings a fixed number of millimetres apart wherever they run, which
    keeps every contour CONTINUOUS -- usually the dominant visual property of a
    contoured plate.

    The 82nd percentile rather than the median is load-bearing: the gap between
    rings is narrowest where the field is steepest, so the median under-sizes
    exactly the stretches that flood.

    ``cell`` is the grid pitch in the same units as ``spacing``.
    """
    ny = len(field)
    nx = len(field[0]) if ny else 0
    grads: List[float] = []
    for j in range(1, ny - 1):
        for i in range(1, nx - 1):
            gx = (field[j][i + 1] - field[j][i - 1]) / (2.0 * cell)
            gy = (field[j + 1][i] - field[j - 1][i]) / (2.0 * cell)
            grads.append(math.hypot(gx, gy))
    if not grads:
        return []
    grads.sort()
    q = grads[min(len(grads) - 1, int(quantile * len(grads)))]
    step = spacing * q
    if step <= 0:
        return []
    lo = min(min(row) for row in field)
    hi = max(max(row) for row in field)
    n = min(n_max, max(1, int((hi - lo) / step)))
    return [lo + step * (k + 0.5) for k in range(n)]


def tone_dots(
    region: Bounds,
    tone,
    rng,
    pen: Optional[int] = None,
    cell: float = 1.5,
    jitter: float = 0.42,
    r: float = 0.0,
    f: int = 2200,
) -> List[GCodeCommand]:
    """A tonal gradient as a DOT CLOUD that CANNOT crowd into a black mass.

    The usual way to stipple a gradient is to shrink the spacing as tone rises,
    and that always ends the same way: past a certain tone the spacing drops
    under the pen tip and the fill floods solid. Here tone controls the
    PROBABILITY that a cell is inked, never the spacing. One dot per cell at
    most, and the cell is never smaller than ``cell``, so peak density is
    bounded by construction at 1/cell² dots per mm² however dark the tone goes.

    ``tone(x, y) -> 0..1``. Keep ``cell`` at or above the pen tip.
    """
    x0, y0, x1, y1 = region
    out: List[GCodeCommand] = []
    ny = max(1, int((y1 - y0) / cell))
    nx = max(1, int((x1 - x0) / cell))
    for j in range(ny):
        for i in range(nx):
            cxx = x0 + (i + 0.5) * cell
            cyy = y0 + (j + 0.5) * cell
            t = max(0.0, min(1.0, tone(cxx, cyy)))
            if rng.random() > t:
                continue
            px = cxx + (rng.random() - 0.5) * cell * jitter
            py = cyy + (rng.random() - 0.5) * cell * jitter
            if r > 0.05:
                out += circle(px, py, r, pen=pen, f=f, n=8)
            else:
                out += _dot(px, py, color=pen, f=f)
    return out


def tone_hatch(
    region: Bounds,
    tone,
    pen: Optional[int] = None,
    spacing: float = 1.4,
    angle: float = 0.0,
    step: float = 0.8,
    f: int = 2200,
) -> List[GCodeCommand]:
    """A tonal gradient as PARALLEL LINES that cannot crowd.

    Same guarantee as ``tone_dots`` by the same trick: line spacing is FIXED at
    ``spacing``, and tone drives each line's dash duty instead. Dark reaches a
    solid run, light breaks to a dotted trace, and the lines never converge.
    """
    x0, y0, x1, y1 = region
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    diag = math.hypot(x1 - x0, y1 - y0)
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    out: List[GCodeCommand] = []
    n_lines = max(1, int(diag / spacing))
    for k in range(-n_lines // 2, n_lines // 2 + 1):
        off = k * spacing
        run: List[Tuple[float, float]] = []
        n_steps = max(2, int(diag / step))
        for m in range(n_steps + 1):
            t = -diag / 2.0 + diag * m / n_steps
            px = mx + t * ca - off * sa
            py = my + t * sa + off * ca
            inside = x0 <= px <= x1 and y0 <= py <= y1
            duty = max(0.0, min(1.0, tone(px, py))) if inside else 0.0
            on = inside and ((m % 4) / 4.0) < duty
            if on:
                run.append((px, py))
            elif len(run) >= 2:
                out += _poly(run, color=pen, f=f)
                run = []
            else:
                run = []
        if len(run) >= 2:
            out += _poly(run, color=pen, f=f)
    return out


def fat_outline(
    pts: Sequence[Tuple[float, float]],
    width: float = 1.6,
    pen: Optional[int] = None,
    tip: float = 0.55,
    f: int = 2200,
) -> List[GCodeCommand]:
    """A contour drawn as a BAND — the heavy pop/comic keyline."""
    passes = max(2, int(round(width / max(tip, 0.05))) + 1)
    out: List[GCodeCommand] = []
    for k in range(passes):
        d = -width / 2.0 + width * k / (passes - 1)
        out += _poly(_offset_polyline(pts, d), color=pen, f=f)
    return out


def squiggle(
    x: float,
    y: float,
    w: float,
    h: float = 3.0,
    waves: float = 3.0,
    pen: Optional[int] = None,
    n: int = 48,
    f: int = 2200,
) -> List[GCodeCommand]:
    """The Memphis squiggle — a sine run with a fat, confident amplitude."""
    pts = [
        (x + w * t / n, y + h * math.sin(2 * math.pi * waves * t / n))
        for t in range(n + 1)
    ]
    return _poly(pts, color=pen, f=f)


def confetti_field(
    region: Bounds,
    rng,
    count: int = 40,
    pens: Sequence[Optional[int]] = (0, 1, 2),
    scale: float = 6.0,
    f: int = 2200,
) -> List[GCodeCommand]:
    """Memphis confetti: squiggles, triangles, bars and dot-grids scattered at
    random over a strict ground. No two alike, none aligned to anything — the
    tension against the grid underneath is the entire point, so do NOT snap
    these to it.
    """
    x0, y0, x1, y1 = region
    out: List[GCodeCommand] = []
    for i in range(count):
        px = rng.uniform(x0, x1)
        py = rng.uniform(y0, y1)
        pen = pens[i % len(pens)]
        sz = scale * rng.uniform(0.55, 1.5)
        kind = i % 4
        if kind == 0:
            out += squiggle(px, py, sz * 1.6, sz * 0.32, waves=rng.uniform(2, 4), pen=pen, f=f)
        elif kind == 1:
            a = rng.uniform(0, 2 * math.pi)
            tri = [
                (px + sz * math.cos(a + k * 2 * math.pi / 3),
                 py + sz * math.sin(a + k * 2 * math.pi / 3))
                for k in range(4)
            ]
            out += _poly(tri, color=pen, f=f)
        elif kind == 2:
            out += fill_rect(px, py, px + sz * 1.7, py + sz * 0.42, spacing=0.7, pen=pen, f=f)
        else:
            step = max(1.1, sz * 0.38)
            gy = py
            while gy < py + sz:
                gx = px
                while gx < px + sz:
                    out += _dot(gx, gy, color=pen, f=f)
                    gx += step
                gy += step
    return out


def modular_grid(
    region: Bounds,
    cols: int = 6,
    rows: int = 8,
    gutter: float = 4.0,
    draw: bool = False,
    pen: Optional[int] = None,
    f: int = 2200,
) -> Tuple[List[List[Bounds]], List[GCodeCommand]]:
    """Swiss modular grid: returns the module rectangles to ALIGN to.

    The grid itself is normally invisible — the discipline is that every
    element snaps to it. Pass ``draw=True`` only while checking alignment.
    """
    x0, y0, x1, y1 = region
    cw = (x1 - x0 - gutter * (cols - 1)) / cols
    rh = (y1 - y0 - gutter * (rows - 1)) / rows
    mods: List[List[Bounds]] = []
    out: List[GCodeCommand] = []
    for r in range(rows):
        line: List[Bounds] = []
        for c in range(cols):
            mx0 = x0 + c * (cw + gutter)
            my1 = y1 - r * (rh + gutter)
            rect = (mx0, my1 - rh, mx0 + cw, my1)
            line.append(rect)
            if draw:
                out += _poly(
                    [(rect[0], rect[1]), (rect[2], rect[1]), (rect[2], rect[3]),
                     (rect[0], rect[3]), (rect[0], rect[1])], color=pen, f=f
                )
        mods.append(line)
    return mods, out


def scale_footer(
    bounds: Bounds,
    text: str = "M 1:80",
    pen: Optional[int] = None,
    height: float = 2.6,
    f: int = 2200,
) -> List[GCodeCommand]:
    x0, y0, x1, _y1 = bounds
    tw = _text_width(_spaced(text), height)
    return _stroke_text(_spaced(text), x1 - tw - 3.0, y0 + 3.0, height, color=pen, f=f)

