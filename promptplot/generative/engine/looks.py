"""Seeded LOOK effects — aesthetic transforms applied to any generator's
commands before merge/postprocess. Deterministic from the SeededRNG."""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from ...models import GCodeCommand
from ..rng import SeededRNG

Bounds = Tuple[float, float, float, float]


def anaglyph_layers(
    commands: List[GCodeCommand],
    rng: SeededRNG,
    offset: Tuple[float, float] = (1.6, 0.9),
    layers: int = 2,
    glitch_bands: int = 0,
    band_shift: float = 4.0,
    bounds: Optional[Bounds] = None,
) -> List[GCodeCommand]:
    """Duplicate a drawing into offset pen layers — 3D-anaglyph / glitch effect.

    Each layer is the full drawing shifted by a fraction of ``offset`` (mm) and
    tagged with its own pen (layer 0 → pen 0, classic red/cyan). With
    ``glitch_bands`` > 0, seeded horizontal bands tear sideways by up to
    ``band_shift`` mm with alternating sign per layer — the glitchy scanline rip.
    """
    layers = max(2, layers)
    ox, oy = offset

    bands: List[Tuple[float, float, float]] = []
    if glitch_bands > 0:
        ys = [c.y for c in commands if c.y is not None]
        if ys:
            ylo, yhi = min(ys), max(ys)
            span = max(1e-6, yhi - ylo)
            for _ in range(glitch_bands):
                b0 = ylo + rng.uniform(0.05, 0.85) * span
                bh = span * rng.uniform(0.03, 0.10)
                shift = band_shift * rng.uniform(0.4, 1.0) * rng.choice([-1.0, 1.0])
                bands.append((b0, b0 + bh, shift))

    def clampx(v: float) -> float:
        if bounds is None:
            return round(v, 2)
        return round(min(max(v, bounds[0]), bounds[2]), 2)

    def clampy(v: float) -> float:
        if bounds is None:
            return round(v, 2)
        return round(min(max(v, bounds[1]), bounds[3]), 2)

    out: List[GCodeCommand] = []
    for L in range(layers):
        frac = L - (layers - 1) / 2.0
        dx, dy = ox * frac, oy * frac
        sign = 1.0 if L % 2 == 0 else -1.0
        for c in commands:
            nc = c.model_copy()
            if nc.x is not None:
                gx = 0.0
                if bands and nc.y is not None:
                    for b0, b1, shift in bands:
                        if b0 <= nc.y <= b1:
                            gx += shift * sign
                nc.x = clampx(nc.x + dx + gx)
            if nc.y is not None:
                nc.y = clampy(nc.y + dy)
            if nc.command in ("M3", "G1"):
                nc.color = L
            out.append(nc)
    return out


def echo_layers(
    commands: List[GCodeCommand],
    rng: SeededRNG,
    copies: int = 3,
    offset: float = 1.6,
    wobble: float = 0.9,
    wobble_scale: float = 0.05,
    step: float = 3.0,
    bounds: Optional[Bounds] = None,
) -> List[GCodeCommand]:
    """Hand-traced echo: the whole drawing redrawn ``copies`` times, one pen per
    copy, each with its own drift direction and a low-frequency hand wobble —
    the posca-marker misregistered-multiples look. Long segments are resampled
    at ``step`` mm so straight lines wave too.
    """
    copies = max(2, copies)

    def clampp(x: float, y: float):
        if bounds is None:
            return (round(x, 2), round(y, 2))
        return (
            round(min(max(x, bounds[0]), bounds[2]), 2),
            round(min(max(y, bounds[1]), bounds[3]), 2),
        )

    out: List[GCodeCommand] = []
    for L in range(copies):
        ang = rng.uniform(0.0, 2.0 * math.pi)
        dxd, dyd = math.cos(ang) * offset, math.sin(ang) * offset
        ph1 = rng.uniform(0.0, 400.0)
        ph2 = rng.uniform(0.0, 400.0)

        def warp(x: float, y: float):
            n1 = rng.noise2d(x * wobble_scale + ph1, y * wobble_scale + ph1)
            n2 = rng.noise2d(x * wobble_scale + ph2 + 61.7, y * wobble_scale + ph2 + 61.7)
            return clampp(
                x + dxd + (n1 - 0.5) * 2.0 * wobble,
                y + dyd + (n2 - 0.5) * 2.0 * wobble,
            )

        last = None
        for c in commands:
            if c.command == "G1" and c.x is not None and last is not None:
                seg = math.hypot(c.x - last[0], c.y - last[1])
                ns = max(1, int(seg / step))
                for k in range(1, ns + 1):
                    g = c.model_copy()
                    g.x, g.y = warp(
                        last[0] + (c.x - last[0]) * k / ns,
                        last[1] + (c.y - last[1]) * k / ns,
                    )
                    g.color = L
                    out.append(g)
                last = (c.x, c.y)
            else:
                nc = c.model_copy()
                if c.x is not None:
                    last = (c.x, c.y)
                    if nc.command in ("G0", "G1"):
                        nc.x, nc.y = warp(c.x, c.y)
                    if nc.command == "G1":
                        nc.color = L
                if nc.command == "M3":
                    nc.color = L
                out.append(nc)
    return out


def dash_rain(
    commands: List[GCodeCommand],
    rng: SeededRNG,
    bounds: Bounds,
    near: float = 10.0,
    near_pen: int = 1,
    far_pen: int = 2,
    dash: float = 3.2,
    pitch: float = 2.4,
    clearance: float = 2.0,
    coverage: float = 0.9,
    cell: float = 1.0,
    feed: int = 1500,
) -> List[GCodeCommand]:
    """Graffiti 'dash rain': short vertical dashes fill the negative space and
    never touch the drawing — ``near_pen`` inside the ``near`` mm halo hugging
    the ink, ``far_pen`` beyond it (sticker-style speed-line background).
    """
    from collections import deque

    x0, y0, x1, y1 = bounds
    W = max(1, int((x1 - x0) / cell) + 1)
    H = max(1, int((y1 - y0) / cell) + 1)

    def cix(x: float) -> int:
        return min(W - 1, max(0, int((x - x0) / cell)))

    def ciy(y: float) -> int:
        return min(H - 1, max(0, int((y - y0) / cell)))

    INF = 1 << 30
    dist = [[INF] * H for _ in range(W)]
    dq: deque = deque()
    last = None
    for c in commands:
        if c.x is None:
            continue
        if c.command == "G1" and last is not None:
            seg = math.hypot(c.x - last[0], c.y - last[1])
            ns = max(1, int(seg / (cell * 0.5)))
            for k in range(ns + 1):
                ix = cix(last[0] + (c.x - last[0]) * k / ns)
                iy = ciy(last[1] + (c.y - last[1]) * k / ns)
                if dist[ix][iy]:
                    dist[ix][iy] = 0
                    dq.append((ix, iy))
        last = (c.x, c.y)
    while dq:  # multi-source BFS: cell distance to the nearest ink
        ix, iy = dq.popleft()
        nd = dist[ix][iy] + 1
        for ddx, ddy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jx, jy = ix + ddx, iy + ddy
            if 0 <= jx < W and 0 <= jy < H and dist[jx][jy] > nd:
                dist[jx][jy] = nd
                dq.append((jx, jy))

    def dmm(x: float, y: float) -> float:
        return dist[cix(x)][ciy(y)] * cell

    out = list(commands)
    xcol = x0 + pitch * 0.5
    while xcol < x1 - 0.3:
        yv = y0 + rng.uniform(0.0, dash * 1.6)
        while yv < y1 - 0.5:
            dlen = dash * rng.uniform(0.7, 1.3)
            ytop = min(y1 - 0.2, yv + dlen)
            xd = xcol + rng.uniform(-0.25, 0.25) * pitch
            keep = rng.random() < coverage
            band = near + rng.uniform(-2.0, 2.0)
            if keep:
                dmin, yy = INF * 1.0, yv
                while yy <= ytop:
                    dmin = min(dmin, dmm(xd, yy))
                    yy += cell * 0.8
                if dmin >= clearance:
                    pen = near_pen if dmm(xd, (yv + ytop) / 2.0) < band else far_pen
                    out.append(GCodeCommand(command="G0", x=round(xd, 2), y=round(ytop, 2)))
                    out.append(GCodeCommand(command="M3", s=1000, color=pen))
                    out.append(
                        GCodeCommand(command="G1", x=round(xd, 2), y=round(yv, 2), f=feed, color=pen)
                    )
                    out.append(GCodeCommand(command="M5"))
            yv = ytop + dash * rng.uniform(0.6, 1.4)
        xcol += pitch
    return out


def glitch_slice(
    commands: List[GCodeCommand],
    rng: SeededRNG,
    bounds: Bounds,
    bands: int = 7,
    max_shift: float = 6.0,
    copies: int = 2,
    copy_offset: float = 1.8,
    dashes: int = 26,
    dash_len: float = 14.0,
    dash_pen: Optional[List[int]] = None,
    feed: int = 1500,
) -> List[GCodeCommand]:
    """Rick-style horizontal glitch: the drawing is duplicated into ``copies``
    offset pen layers (chromatic-shift outline), then seeded horizontal bands
    tear each layer sideways, and colored horizontal speed-dashes shoot out from
    the drawing's silhouette edges within those bands.

    Pen mapping: layer L → pen L. Speed-dashes cycle ``dash_pen`` (default the
    copy pens), so they read as the same red/blue chromatic streaks.
    """
    copies = max(1, copies)
    x0, y0, x1, y1 = bounds
    span = max(1e-6, y1 - y0)

    # seeded tear bands: (y_lo, y_hi, shift_mm)
    band_list: List[Tuple[float, float, float]] = []
    for _ in range(max(0, bands)):
        b0 = y0 + rng.uniform(0.04, 0.9) * span
        bh = span * rng.uniform(0.015, 0.06)
        sh = max_shift * rng.uniform(0.3, 1.0) * rng.choice([-1.0, 1.0])
        band_list.append((b0, b0 + bh, sh))

    def shift_at(y: float) -> float:
        for b0, b1, sh in band_list:
            if b0 <= y <= b1:
                return sh
        return 0.0

    def clampx(v: float) -> float:
        return round(min(max(v, x0), x1), 2)

    out: List[GCodeCommand] = []
    # --- offset + torn outline copies
    for L in range(copies):
        frac = L - (copies - 1) / 2.0
        dx = copy_offset * frac
        for c in commands:
            nc = c.model_copy()
            if nc.x is not None:
                nc.x = clampx(nc.x + dx + shift_at(nc.y))
            if nc.command in ("M3", "G1"):
                nc.color = L
            out.append(nc)

    # --- silhouette scan: for each band, find drawing's x-extent per scanline
    #     and shoot horizontal dashes outward from the left/right edges
    pens = dash_pen if dash_pen else list(range(copies))
    verts = [(c.x, c.y) for c in commands if c.x is not None and c.command == "G1"]
    di = 0
    for bi, (b0, b1, sh) in enumerate(band_list):
        for _ in range(max(0, dashes) // max(1, len(band_list)) + 1):
            yv = rng.uniform(b0, b1 + (b1 - b0) * 2.0)
            near = [vx for vx, vy in verts if abs(vy - yv) < 3.0]
            if not near:
                continue
            side = rng.choice([-1.0, 1.0])
            edge = (min(near) if side < 0 else max(near)) + sh
            dl = dash_len * rng.uniform(0.5, 1.3)
            xa = clampx(edge)
            xb = clampx(edge + side * dl)
            if abs(xb - xa) < 1.5:
                continue
            pen = pens[di % len(pens)]
            di += 1
            out.append(GCodeCommand(command="G0", x=xa, y=round(yv, 2)))
            out.append(GCodeCommand(command="M3", s=1000, color=pen))
            out.append(GCodeCommand(command="G1", x=xb, y=round(yv, 2), f=feed, color=pen))
            out.append(GCodeCommand(command="M5"))
    return out


