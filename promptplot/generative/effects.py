"""Seeded post-effects applied to generated command lists.

Effects transform a raw ``List[GCodeCommand]`` before merge/postprocess, so they
work with ANY generator. Deterministic: all randomness comes from the SeededRNG.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from ..models import GCodeCommand
from .rng import SeededRNG

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


def focal_void(
    commands: List[GCodeCommand],
    r: float = 12.0,
    cx: Optional[float] = None,
    cy: Optional[float] = None,
    keep: int = 1,
    rim: bool = False,
    rim_pen: Optional[int] = None,
    min_len: float = 1.5,
) -> List[GCodeCommand]:
    """ENGINE ARTISTIC POLICY — the convergence clearing. Where many strokes
    converge into an unreadable knot (helix waists, spiral centers, mesh folds),
    carve a disc of BLANK PAPER: every stroke stops exactly ON the circle
    (exact clip, no stagger), and the ``keep`` strokes that pass closest to the
    centre survive whole — the hero lines that thread the void. The eye
    completes the rest. House aesthetic: negative space over pileup (WATERSHED
    separatrix, black-hole shadow, LSTM gate).

    ``cx``/``cy`` default to the densest drawn spot (auto-detected). ``rim``
    draws the clearing circle itself (``rim_pen``) as a quiet boundary.
    """
    from .geometry import Circle as _Circle, clip as _clip

    # ---- split into strokes (pen-preserving)
    strokes: List[dict] = []
    cur: Optional[dict] = None
    pos = None
    passthrough: List[GCodeCommand] = []
    for c in commands:
        if c.command == "M3":
            cur = {"m3": c, "pts": [pos] if pos else [], "g1": []}
        elif c.command == "M5":
            if cur is not None:
                strokes.append(cur)
                cur = None
        elif cur is not None and c.command == "G1" and c.x is not None:
            cur["g1"].append(c)
            cur["pts"].append((c.x, c.y))
        elif cur is None:
            passthrough.append(c)
        if c.x is not None:
            pos = (c.x, c.y)

    # ---- auto-locate the knot: densest 3mm cell of drawn points
    if cx is None or cy is None:
        from collections import Counter

        cell = 3.0
        density: Counter = Counter()
        for s in strokes:
            for px, py in s["pts"]:
                density[(int(px / cell), int(py / cell))] += 1
        if not density:
            return commands
        (ci, cj), _ = density.most_common(1)[0]
        cx, cy = (ci + 0.5) * cell, (cj + 0.5) * cell

    void = _Circle(cx, cy, r)

    # ---- heroes: the `keep` strokes passing closest to the centre
    # (distance to SEGMENTS, not vertices — a sparse straight line through the
    # centre has no vertex near it)
    def min_d2(s):
        pts = s["pts"]
        best = 1e18
        if len(pts) == 1:
            px, py = pts[0]
            return (px - cx) ** 2 + (py - cy) ** 2
        for p0, p1 in zip(pts, pts[1:]):
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            l2 = dx * dx + dy * dy
            if l2 < 1e-12:
                qx, qy = p0
            else:
                t = max(0.0, min(1.0, ((cx - p0[0]) * dx + (cy - p0[1]) * dy) / l2))
                qx, qy = p0[0] + t * dx, p0[1] + t * dy
            d2 = (qx - cx) ** 2 + (qy - cy) ** 2
            if d2 < best:
                best = d2
        return best

    crossing = [si for si, s in enumerate(strokes) if min_d2(s) < r * r]
    heroes = set(sorted(crossing, key=lambda si: min_d2(strokes[si]))[: max(0, keep)])

    out: List[GCodeCommand] = list(passthrough)
    for si, s in enumerate(strokes):
        pts = s["pts"]
        if len(pts) < 2:
            continue
        template = s["g1"][0] if s["g1"] else None

        def _emit(sub):
            out.append(GCodeCommand(command="G0", x=round(sub[0][0], 2), y=round(sub[0][1], 2)))
            out.append(s["m3"].model_copy())
            for x, y in sub[1:]:
                g = template.model_copy() if template else GCodeCommand(command="G1", f=1500)
                g.x, g.y = round(x, 2), round(y, 2)
                out.append(g)
            out.append(GCodeCommand(command="M5"))

        if si in heroes or si not in crossing:
            _emit(pts)  # untouched: heroes and strokes that never enter the void
            continue
        for sub in _clip(pts, void, keep="outside"):
            total = sum(
                math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(sub, sub[1:])
            )
            if len(sub) >= 2 and total >= min_len:
                _emit(sub)

    if rim:
        ring = [
            (cx + r * math.cos(2 * math.pi * k / 120), cy + r * math.sin(2 * math.pi * k / 120))
            for k in range(121)
        ]
        out.append(GCodeCommand(command="G0", x=round(ring[0][0], 2), y=round(ring[0][1], 2)))
        out.append(GCodeCommand(command="M3", s=1000, color=rim_pen))
        for x, y in ring[1:]:
            out.append(GCodeCommand(command="G1", x=round(x, 2), y=round(y, 2), f=1500, color=rim_pen))
        out.append(GCodeCommand(command="M5"))
    return out


def occlude_crossings(
    commands: List[GCodeCommand],
    gap: float = 1.0,
    min_len: float = 0.7,
    priority: Optional[List[int]] = None,
    mode: str = "priority",
) -> List[GCodeCommand]:
    """Simulated opacity at pen crossings — layered paint-marker look instead
    of muddy ink-on-ink. Same-pen crossings are always left alone.

    ``mode='priority'``: wherever a lower-priority pen crosses a higher one,
    cut a ``gap`` mm break in the lower stroke. ``priority`` lists pen indices
    topmost-first; default is higher pen index on top (drawn later = on top).

    ``mode='weave'``: no fixed winner — along each stroke, successive crossings
    alternate over/under (textile weave: sometimes this line breaks, sometimes
    the other one does). Deterministic: parity of the crossing sequence along
    the lower-indexed stroke decides.
    """
    # ---- split into strokes, remembering pen + polyline
    strokes: List[dict] = []
    cur: Optional[dict] = None
    pos = None
    prefix: List[GCodeCommand] = []
    for c in commands:
        if c.command == "M3":
            cur = {"m3": c, "pts": [pos] if pos else [], "g1": []}
        elif c.command == "M5":
            if cur is not None:
                strokes.append(cur)
                cur = None
        elif cur is not None and c.command == "G1" and c.x is not None:
            cur["g1"].append(c)
            cur["pts"].append((c.x, c.y))
        elif cur is None:
            prefix.append(c)
        if c.x is not None:
            pos = (c.x, c.y)

    def pen_of(s):
        col = s["m3"].color
        if col is None and s["g1"]:
            col = s["g1"][0].color
        return col if col is not None else 0

    order = {p: i for i, p in enumerate(priority)} if priority else None

    def rank(pen):  # smaller = more on top
        if order is not None:
            return order.get(pen, len(order))
        return -pen

    # ---- per-stroke cumulative arc lengths + spatial hash of segments
    CELL = 4.0
    grid: dict = {}
    seglist = []
    cum: List[List[float]] = []
    for si, s in enumerate(strokes):
        pts = s["pts"]
        c = [0.0]
        for a, b in zip(pts, pts[1:]):
            c.append(c[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        cum.append(c)
        for k in range(len(pts) - 1):
            (xa, ya), (xb, yb) = pts[k], pts[k + 1]
            gi = len(seglist)
            seglist.append((xa, ya, xb, yb, si, k))
            for cx in range(int(min(xa, xb) / CELL), int(max(xa, xb) / CELL) + 1):
                for cy in range(int(min(ya, yb) / CELL), int(max(ya, yb) / CELL) + 1):
                    grid.setdefault((cx, cy), []).append(gi)

    # ---- find ALL different-pen crossings once, with arc positions on BOTH
    # strokes: records (si, arc_i, sj, arc_j) with si < sj
    records = []
    seen_pairs = set()
    for gi, (xa, ya, xb, yb, si, k) in enumerate(seglist):
        dx, dy = xb - xa, yb - ya
        for cx in range(int(min(xa, xb) / CELL), int(max(xa, xb) / CELL) + 1):
            for cy in range(int(min(ya, yb) / CELL), int(max(ya, yb) / CELL) + 1):
                for gj in grid.get((cx, cy), ()):
                    if gj <= gi or (gi, gj) in seen_pairs:
                        continue
                    seen_pairs.add((gi, gj))
                    (ox, oy, px, py, sj, kj) = seglist[gj]
                    if sj == si or pen_of(strokes[sj]) == pen_of(strokes[si]):
                        continue
                    ex, ey = px - ox, py - oy
                    den = dx * ey - dy * ex
                    if abs(den) < 1e-12:
                        continue
                    t = ((ox - xa) * ey - (oy - ya) * ex) / den
                    u = ((ox - xa) * dy - (oy - ya) * dx) / den
                    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
                        seg_i = math.hypot(dx, dy)
                        seg_j = math.hypot(ex, ey)
                        records.append(
                            (si, cum[si][k] + t * seg_i, sj, cum[sj][kj] + u * seg_j)
                        )

    # ---- decide the loser of every crossing → cut positions per stroke
    cut_at: dict = {}
    if mode == "weave":
        # alternate over/under along the lower-indexed (driver) stroke
        records.sort(key=lambda r: (r[0], r[1]))
        parity: dict = {}
        for si, arc_i, sj, arc_j in records:
            n = parity.get(si, 0)
            parity[si] = n + 1
            if n % 2 == 0:
                cut_at.setdefault(sj, []).append(arc_j)  # driver goes over
            else:
                cut_at.setdefault(si, []).append(arc_i)  # driver goes under
    else:
        for si, arc_i, sj, arc_j in records:
            ri, rj = rank(pen_of(strokes[si])), rank(pen_of(strokes[sj]))
            if ri == rj:
                continue
            if ri < rj:  # si on top → sj yields
                cut_at.setdefault(sj, []).append(arc_j)
            else:
                cut_at.setdefault(si, []).append(arc_i)

    # ---- rebuild: cut gap-intervals out of losing strokes
    out: List[GCodeCommand] = list(prefix)
    for si, s in enumerate(strokes):
        pts = s["pts"]
        cuts = cut_at.get(si, [])
        total = cum[si][-1] if cum[si] else 0.0
        if not cuts:
            out.append(GCodeCommand(command="G0", x=pts[0][0], y=pts[0][1]))
            out.append(s["m3"].model_copy())
            out.extend(g.model_copy() for g in s["g1"])
            out.append(GCodeCommand(command="M5"))
            continue
        # merge cut intervals along arc length
        iv = sorted((c - gap / 2.0, c + gap / 2.0) for c in cuts)
        merged = [list(iv[0])]
        for lo, hi in iv[1:]:
            if lo <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], hi)
            else:
                merged.append([lo, hi])
        keep = []
        at = 0.0
        for lo, hi in merged:
            if lo > at:
                keep.append((at, min(lo, total)))
            at = max(at, hi)
        if at < total:
            keep.append((at, total))

        def point_at(sd):
            acc = 0.0
            for k in range(len(pts) - 1):
                (xa, ya), (xb, yb) = pts[k], pts[k + 1]
                L = math.hypot(xb - xa, yb - ya)
                if acc + L >= sd or k == len(pts) - 2:
                    f = 0.0 if L == 0 else min(1.0, max(0.0, (sd - acc) / L))
                    return (xa + (xb - xa) * f, ya + (yb - ya) * f, k)
                acc += L
            return (pts[-1][0], pts[-1][1], len(pts) - 2)

        template = s["g1"][0] if s["g1"] else None
        for lo, hi in keep:
            if hi - lo < min_len:
                continue
            x0_, y0_, k0 = point_at(lo)
            x1_, y1_, k1 = point_at(hi)
            sub = [(x0_, y0_)] + [pts[k] for k in range(k0 + 1, k1 + 1)] + [(x1_, y1_)]
            out.append(GCodeCommand(command="G0", x=round(sub[0][0], 2), y=round(sub[0][1], 2)))
            out.append(s["m3"].model_copy())
            for x, y in sub[1:]:
                g = template.model_copy() if template else GCodeCommand(command="G1", f=1500)
                g.x, g.y = round(x, 2), round(y, 2)
                out.append(g)
            out.append(GCodeCommand(command="M5"))
    return out


def enforce_line_spacing(
    commands: List[GCodeCommand],
    min_dist: float,
    resample: float = 0.5,
    lookback_mm: Optional[float] = None,
    min_run: float = 1.5,
    short_exempt: float = 10.0,
) -> List[GCodeCommand]:
    """Minimum line-separation guardrail: thin strokes so no drawn point lands
    within ``min_dist`` mm of an EARLIER drawn point (from another stroke, or a
    far-back part of the same stroke). Stops crowded parallel / converging lines
    merging into a solid black patch — the attractor / harmonograph / dense-mesh
    saturation problem. Distinct from ``limit_ink_density`` (which caps repeated
    passes over the same spot); this enforces a real gap between neighbours.

    ``min_dist`` should be ~1.5–2× the pen tip so adjacent lines keep white
    between them. ``lookback_mm`` (default ``3*min_dist``) is how much of the
    current stroke's own recent trail is exempt, so a line never rejects itself.
    """
    if min_dist <= 0:
        return commands

    if lookback_mm is None:
        lookback_mm = 3.0 * min_dist
    lookback = max(2, int(lookback_mm / max(0.1, resample)))
    cell = min_dist
    r2 = min_dist * min_dist
    grid: dict = {}
    counter = 0

    def occupied(x, y, cur_idx):
        ci, cj = int(x / cell), int(y / cell)
        for a in (ci - 1, ci, ci + 1):
            for b in (cj - 1, cj, cj + 1):
                for px, py, idx in grid.get((a, b), ()):
                    if cur_idx - idx <= lookback:
                        continue  # local trail of the current line — not a violation
                    if (px - x) ** 2 + (py - y) ** 2 < r2:
                        return True
        return False

    # split into strokes (mirror limit_ink_density's parsing)
    out: List[GCodeCommand] = []
    i = 0
    n = len(commands)
    while i < n:
        c = commands[i]
        if c.command != "M3":
            out.append(c)
            i += 1
            continue
        m3 = c
        start = None
        if out and out[-1].command == "G0" and out[-1].x is not None:
            start = (out[-1].x, out[-1].y)
            out.pop()
        j = i + 1
        g1s = []
        while j < n and commands[j].command == "G1":
            g1s.append(commands[j])
            j += 1
        if j < n and commands[j].command == "M5":
            j += 1
        template = g1s[0] if g1s else None
        path = ([start] if start else []) + [(g.x, g.y) for g in g1s if g.x is not None]

        # SHORT strokes (glyphs, ticks, dots, dashes) are exempt from thinning —
        # letter joints legitimately touch and must never be eaten — but they
        # still claim their space so long lines yield to text, not through it.
        path_len = sum(
            math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(path, path[1:])
        )
        if path_len < short_exempt:
            if start is not None:
                out.append(GCodeCommand(command="G0", x=start[0], y=start[1]))
            out.append(m3.model_copy())
            out.extend(g.model_copy() for g in g1s)
            out.append(GCodeCommand(command="M5"))
            for (xa, ya), (xb, yb) in zip(path, path[1:]):
                seg = math.hypot(xb - xa, yb - ya)
                ns = max(1, int(seg / resample))
                for k in range(ns + 1):
                    px = xa + (xb - xa) * k / ns
                    py = ya + (yb - ya) * k / ns
                    grid.setdefault((int(px / cell), int(py / cell)), []).append(
                        (px, py, counter)
                    )
                    counter += 1
            i = j
            continue

        # resample and keep runs of points that clear the min-distance
        runs = []
        cur: list = []
        for (xa, ya), (xb, yb) in zip(path, path[1:]):
            seg = math.hypot(xb - xa, yb - ya)
            ns = max(1, int(seg / resample))
            for k in range(1, ns + 1):
                px = xa + (xb - xa) * k / ns
                py = ya + (yb - ya) * k / ns
                if occupied(px, py, counter):
                    if len(cur) >= 2:
                        runs.append(cur)
                    cur = []
                    continue
                grid.setdefault((int(px / cell), int(py / cell)), []).append((px, py, counter))
                counter += 1
                cur.append((px, py))
        if len(cur) >= 2:
            runs.append(cur)

        for r in runs:
            total = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(r, r[1:]))
            if total < min_run:
                continue
            out.append(GCodeCommand(command="G0", x=round(r[0][0], 2), y=round(r[0][1], 2)))
            out.append(m3.model_copy())
            for x, y in r[1:]:
                g = template.model_copy() if template else GCodeCommand(command="G1", f=1500)
                g.x, g.y = round(x, 2), round(y, 2)
                out.append(g)
            out.append(GCodeCommand(command="M5"))
        i = j
    return out


def limit_ink_density(
    commands: List[GCodeCommand],
    cell: float = 1.0,
    max_passes: int = 8,
    min_run: float = 2.0,
    decimate: float = 2.0,
) -> List[GCodeCommand]:
    """Cap how many times the pen may pass over any ``cell``-mm spot.

    A deterministic post-process applicable to ANY generator's output: strokes
    are re-sampled and split wherever a cell has already been inked
    ``max_passes`` times, so dense knots (attractor/harmonograph convergence
    zones, interference pileups) thin out instead of chewing through the paper.
    """
    counts: dict = {}

    def cell_of(x, y):
        return (int(x / cell), int(y / cell))

    out: List[GCodeCommand] = []
    i = 0
    n = len(commands)
    while i < n:
        c = commands[i]
        if c.command != "M3":
            out.append(c)
            i += 1
            continue
        m3 = c
        # stroke start = trailing G0 we already emitted
        start = None
        if out and out[-1].command == "G0" and out[-1].x is not None:
            start = (out[-1].x, out[-1].y)
            out.pop()
        j = i + 1
        g1s = []
        while j < n and commands[j].command == "G1":
            g1s.append(commands[j])
            j += 1
        if j < n and commands[j].command == "M5":
            j += 1
        template = g1s[0] if g1s else None
        path = ([start] if start else []) + [(g.x, g.y) for g in g1s if g.x is not None]

        # never densify beyond the stroke's native vertex spacing
        path_len = sum(
            math.hypot(bpt[0] - apt[0], bpt[1] - apt[1]) for apt, bpt in zip(path, path[1:])
        )
        dec = max(decimate, 0.95 * path_len / max(1, len(path) - 1))

        runs = []
        cur: list = []
        prev_cell = None
        for (xa, ya), (xb, yb) in zip(path, path[1:]):
            seg_len = math.hypot(xb - xa, yb - ya)
            ns = max(1, int(seg_len / 0.4))
            for k in range(1, ns + 1):
                px = xa + (xb - xa) * k / ns
                py = ya + (yb - ya) * k / ns
                cl = cell_of(px, py)
                if cl != prev_cell:
                    prev_cell = cl
                    cnt = counts.get(cl, 0)
                    if cnt >= max_passes:
                        if len(cur) >= 2:
                            runs.append(cur)
                        cur = []
                        continue
                    counts[cl] = cnt + 1
                cur.append((px, py)) if cur else cur.extend([(px, py)])
        if len(cur) >= 2:
            runs.append(cur)

        for r in runs:
            # decimate resampled points back to a plottable polyline
            slim = [r[0]]
            for pnt in r[1:-1]:
                if math.hypot(pnt[0] - slim[-1][0], pnt[1] - slim[-1][1]) >= dec:
                    slim.append(pnt)
            slim.append(r[-1])
            total_len = sum(
                math.hypot(bpt[0] - apt[0], bpt[1] - apt[1]) for apt, bpt in zip(slim, slim[1:])
            )
            if len(slim) < 2 or total_len < min_run:
                continue
            out.append(GCodeCommand(command="G0", x=round(slim[0][0], 2), y=round(slim[0][1], 2)))
            out.append(m3.model_copy())
            for pnt in slim[1:]:
                g = template.model_copy() if template else GCodeCommand(command="G1", f=1500)
                g.x = round(pnt[0], 2)
                g.y = round(pnt[1], 2)
                out.append(g)
            out.append(GCodeCommand(command="M5"))
        i = j
    return out
