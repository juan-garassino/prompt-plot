"""LSTM — RECURSIVE MEMORY THROUGH TIME.

A recreation of the `studio/lstm-spirals/ref/reference.png` plate with ONE
correction: BOTH spiral centres sit exactly ON the central vertical axis, one
above the other, so the axis is the spine of the recursion (INPUT at the
bottom -> red cell-state spiral -> shared saddle -> black hidden-state spiral
-> OUTPUT at the top) rather than a rule laid over two off-axis vortices.

The two spiral families are NOT parametric spirals: they are streamlines of a
real 2-D vector field -- two spiral sinks (sink + vortex, 1/r falloff) placed
on the axis.  Equal strengths and equal circulation make the two contributions
cancel exactly at the midpoint, producing a genuine stagnation point on the
axis where the fields interleave; every bend in every line is the other
system's pull, which is what the reference's curves actually show.

Contract: ``lstm_spirals(rng, bounds, colors=2) -> list[GCodeCommand]``.
Pen 0 = black (hidden state h_t), pen 1 = red (cell state c_t).
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import Occupancy, Scene3D
from promptplot.generative.engine.kit import (
    Bounds,
    circle,
    _dot,
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    giant_type,
    plus_mark,
)

HIDE = Scene3D.HIDE

# ---------------------------------------------------------------------------
# the field
# ---------------------------------------------------------------------------

_SOFT2 = 4.0  # mm^2 softening: keeps the sink finite at its own centre

# x_t injection: a rightward drift decaying inward from the left edge.  Without
# it the left margin sits on the two sinks' symmetry line, where the radial
# parts cancel and the flow is purely vertical -- the INPUT SEQUENCE lines then
# slide down the edge instead of feeding the cell.  Weak enough (~4% of the
# local field at the centres) to leave both spirals and the saddle on the axis.
_DRIFT_U = 0.115
_DRIFT_L = 25.0


def _field(x, y, centres, drift=None):
    """Superposed spiral sinks (+ the input drift).  Each centre contributes
    ``(-m*d + g*rot90(d)) / (|d|^2 + s^2)`` -- a point sink plus a point vortex,
    whose single-centre streamlines are exact logarithmic spirals with pitch
    set by g/m.  Two of them interact, and that interaction is the drawing."""
    vx = vy = 0.0
    for px, py, m, g in centres:
        dx, dy = x - px, y - py
        r2 = dx * dx + dy * dy + _SOFT2
        vx += (-m * dx - g * dy) / r2
        vy += (-m * dy + g * dx) / r2
    if drift is not None:
        vx += _DRIFT_U * math.exp(-(x - drift) / _DRIFT_L)
    return vx, vy


def _unit(v):
    mag = math.hypot(v[0], v[1])
    if mag < 1e-12:
        return None
    return (v[0] / mag, v[1] / mag)


def _stream(
    x: float,
    y: float,
    centres,
    clip: Bounds,
    stops: Sequence[Tuple[float, float, float]],
    step: float = 0.85,
    max_steps: int = 620,
    drift: Optional[float] = None,
    ybar: Optional[Tuple[float, float]] = None,
) -> List[Tuple[float, float]]:
    """RK4 streamline on the NORMALISED field (constant arc-length samples, so
    occupancy spacing and dash phase are uniform).  Stops at the clip rect or
    when it reaches any (cx, cy, r) core."""
    pts = [(x, y)]
    cx0, cy0, cx1, cy1 = clip
    for _ in range(max_steps):
        k1 = _unit(_field(x, y, centres, drift))
        if k1 is None:
            break
        k2 = _unit(_field(x + 0.5 * step * k1[0], y + 0.5 * step * k1[1], centres, drift))
        if k2 is None:
            break
        k3 = _unit(_field(x + 0.5 * step * k2[0], y + 0.5 * step * k2[1], centres, drift))
        if k3 is None:
            break
        k4 = _unit(_field(x + step * k3[0], y + step * k3[1], centres, drift))
        if k4 is None:
            break
        x += step * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        y += step * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        if not (cx0 < x < cx1 and cy0 < y < cy1):
            break
        if ybar is not None and not (ybar[0] < y < ybar[1]):
            break  # a family never crosses past the far centre
        pts.append((x, y))
        hit = False
        for sx, sy, sr in stops:
            if (x - sx) ** 2 + (y - sy) ** 2 < sr * sr:
                hit = True
                break
        if hit:
            break
    return pts


# ---------------------------------------------------------------------------
# small drawing helpers (local: dash phase + chevrons the kit has no view on)
# ---------------------------------------------------------------------------


def _dash(pts: Sequence[Tuple[float, float]], on: float = 1.1, off: float = 1.9):
    """Split a polyline into dashes by arc length."""
    segs: List[List[Tuple[float, float]]] = []
    cur: List[Tuple[float, float]] = []
    trav = 0.0
    period = on + off
    for i, p in enumerate(pts):
        if i:
            trav += math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1])
        if (trav % period) < on:
            cur.append(p)
        else:
            if len(cur) >= 2:
                segs.append(cur)
            cur = []
    if len(cur) >= 2:
        segs.append(cur)
    return segs


def _arrow(x, y, dx, dy, size=1.9, pen=None, f=2200) -> List[GCodeCommand]:
    a = math.atan2(dy, dx)
    w = math.radians(148)
    return _poly(
        [
            (x + size * math.cos(a + w), y + size * math.sin(a + w)),
            (x, y),
            (x + size * math.cos(a - w), y + size * math.sin(a - w)),
        ],
        color=pen,
        f=f,
    )


def _filled_dot(x, y, r=0.55, pen=None, feed=2200):
    return circle(x, y, r, pen=pen, f=feed, n=14) + _dot(x, y, r=r * 0.55, color=pen, f=1200)


def _bez(p0, p1, p2, n: int = 40):
    out = []
    for k in range(n + 1):
        t = k / n
        u = 1 - t
        out.append(
            (
                u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1],
            )
        )
    return out


def _core_curl(cx, cy, r_out, pitch=1.0, turns_dir=1.0, pen=None, f=2200):
    """Archimedean curl at a spiral's heart: constant ``pitch`` mm between
    successive turns, so the densest spot on the plate is still pen-safe."""
    c = pitch / (2 * math.pi)
    th_end = r_out / c
    pts = []
    th = 1.2
    while th <= th_end:
        r = c * th
        pts.append((cx + r * math.cos(turns_dir * th), cy + r * math.sin(turns_dir * th)))
        th += 0.16
    return pts


# ---------------------------------------------------------------------------
# rich single-stroke type
# ---------------------------------------------------------------------------


def _rich(text, x, y, h, pen=None, feed=2200, track=0.0):
    """Single-stroke type with SUBSCRIPTS, letter tracking, and the two marks
    the shared font does not carry.  Returns ``(commands, width)``.

    Markup:  ``h_t``, ``c_{t-1}``  -> subscript (LAYOUT: the same glyphs at
    0.62x on a lowered baseline, not a new glyph table);
    ``@`` -> the Hadamard operator (a drawn circled dot, i.e. U+2299);
    ``^`` -> a tilde over the preceding glyph (c-tilde).
    U+2299 and the combining tilde are the only two characters this plate
    needs that _GLYPHS still lacks.
    """
    cmds: List[GCodeCommand] = []
    adv = 5.6 * h / 6.0 + track
    sub_h = 0.62 * h
    sub_adv = 5.6 * sub_h / 6.0 + track * 0.6
    px = x
    prev_x, prev_adv = x, adv
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "_" and i + 1 < n:
            i += 1
            if text[i] == "{":
                j = text.index("}", i)
                run, i = text[i + 1 : j], j + 1
            else:
                run, i = text[i], i + 1
            for c in run:
                cmds += _stroke_text(c, px, y - 0.27 * h, sub_h, color=pen, f=feed)
                px += sub_adv
            continue
        if ch == "@":
            r = 0.30 * h
            mx, my = px + adv * 0.45, y + 0.42 * h
            cmds += circle(mx, my, r, pen=pen, f=feed, n=20)
            cmds += _dot(mx, my, r=0.20 * h, color=pen, f=1200)
            px += adv
            i += 1
            continue
        if ch == "^":
            w = prev_adv * 0.52
            bx, ty = prev_x + prev_adv * 0.14, y + 1.00 * h
            cmds += _poly(
                [
                    (bx, ty),
                    (bx + 0.25 * w, ty + 0.15 * h),
                    (bx + 0.50 * w, ty),
                    (bx + 0.75 * w, ty - 0.15 * h),
                    (bx + w, ty),
                ],
                color=pen,
                f=feed,
            )
            i += 1
            continue
        cmds += _stroke_text(ch, px, y, h, color=pen, f=feed)
        prev_x, prev_adv = px, adv
        px += adv
        i += 1
    return cmds, px - x


def _rich_w(text, h, track=0.0):
    return _rich(text, 0.0, 0.0, h, track=track)[1]


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def lstm_spirals(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 2,
    sep: float = 0.95,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """LSTM — RECURSIVE MEMORY THROUGH TIME.  Two spiral-sink flow fields whose
    centres lie ON the plate's vertical axis: black hidden state h_t above, red
    cell state c_t below, meeting at a stagnation point on the axis."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    BK = _pen(0, colors)
    RD = _pen(1, colors)

    scene = Scene3D(rng, bounds, feed=feed, fit="none", tip=0.5)
    out = scene.out

    # ---- the spine -------------------------------------------------------
    cx = x0 + 0.5 * W
    y_top = y0 + 0.945 * H  # OUTPUT arrow tip
    y_bot = y0 + 0.190 * H  # INPUT arrow tip

    # BOTH centres exactly on the axis (the correction)
    yh = y0 + 0.662 * H  # hidden state h_t  (black)
    yc = y0 + 0.367 * H  # cell state c_t    (red)
    y_mid = 0.5 * (yh + yc)  # the stagnation point, also on the axis

    M, G = 1.0, 3.0  # sink / vortex strength -> log-spiral pitch
    C_H = (cx, yh, M, G)
    C_C = (cx, yc, M, G)
    centres = (C_H, C_C)

    r_core = 3.6
    stops = ((cx, yh, r_core), (cx, yc, r_core))
    clip = (x0 + 2.5, y0 + 0.205 * H, x1 - 2.5, y0 + 0.885 * H)

    # ---- labels first: their halos carve the field ------------------------
    # Reference type is MIXED CASE: caps for the structural labels, lowercase
    # (tracked) for the state names, true subscripts on every symbol.
    tt = 1.75  # caption cap height
    ts = 1.5  # small caption
    tk = 0.45  # tracking on the lowercase labels
    labels: List[tuple] = []
    rich: List[GCodeCommand] = []

    def place(text, x, y, h, pen, track=0.0):
        """Draw rich type AND reserve its halo box.  The box is reserved with a
        run of spaces (the space glyph draws nothing) so scene.render() emits no
        duplicate plain-text copy underneath."""
        cmds, w = _rich(text, x, y, h, pen, feed, track)
        k = max(1, int(math.ceil(w / (5.6 * h / 6.0))))
        labels.append((" " * k, x, y, h, pen))
        rich.extend(cmds)
        return w

    for txt, yy, hh, trk in (
        (_spaced("OUTPUT"), y_top - 6.0, tt, 0.0),
        ("h_t  /  y_t", y_top - 12.4, 2.7, 0.3),
    ):
        place(txt, cx - _rich_w(txt, hh, trk) / 2.0, yy, hh, BK, track=trk)
    for txt, yy, hh, trk in (
        (_spaced("INPUT"), y_bot - 7.0, tt, 0.0),
        ("x_t", y_bot - 13.8, 2.7, 0.3),
    ):
        place(txt, cx - _rich_w(txt, hh, trk) / 2.0, yy, hh, BK, track=trk)

    # dotted t-rings: radii + label angle, per field
    # eccentric orbits (ry = 0.78 rx): the reference's t-rings are wider than
    # tall, which is also what keeps the outer red one clear of the bottom band
    RY = 0.78
    rings_h = [(30.0, 186, "t = 1"), (41.0, 172, "t = 2"), (52.0, 158, "t = 3"), (63.0, 46, "t = T")]
    rings_c = [(30.0, 174, "t = 1"), (41.0, 194, "t = 2"), (52.0, 209, "t = 3"), (63.0, 316, "t = T")]
    for cyk, rings, pen in ((yh, rings_h, BK), (yc, rings_c, RD)):
        for r, adeg, txt in rings:
            a = math.radians(adeg)
            lx = cx + (r + 3.0) * math.cos(a)
            ly = cyk + RY * (r + 3.0) * math.sin(a)
            if math.cos(a) < 0:
                lx -= _rich_w(txt, ts)
            place(txt, lx, ly, ts, pen)
    place(". . .", cx + 72.0 * math.cos(math.radians(50)), yh + 72.0 * math.sin(math.radians(50)), 2.2, BK)
    place(". . .", cx + 63.0 * math.cos(math.radians(330)), yc + 63.0 * math.sin(math.radians(330)), 2.2, RD)

    # leader labels
    place(_spaced("OUTPUT GATE"), x0 + 3.0, y0 + 0.714 * H, tt, BK)
    place("o_t", x0 + 3.0, y0 + 0.690 * H, 2.6, BK)
    place(_spaced("INPUT GATE"), x0 + 3.0, y0 + 0.420 * H, tt, BK)
    place("i_t", x0 + 3.0, y0 + 0.396 * H, 2.6, BK)

    fg_x = x1 - 3.0 - _rich_w(_spaced("FORGET GATE"), tt)
    place(_spaced("FORGET GATE"), fg_x, y0 + 0.584 * H, tt, BK)
    place("f_t", fg_x + 6.0, y0 + 0.560 * H, 2.6, BK)

    hs_txt = "hidden state   h_t"
    hs_x = x1 - 3.0 - _rich_w(hs_txt, 2.2, tk)
    place(hs_txt, hs_x, y0 + 0.700 * H, 2.2, BK, track=tk)
    rich.extend(_filled_dot(hs_x + 2.0, y0 + 0.676 * H + 0.5, 0.55, BK, feed))
    place("hidden state flow", hs_x + 4.8, y0 + 0.676 * H, ts, BK)
    place("(short-term output)", hs_x + 4.8, y0 + 0.656 * H, ts, BK)

    cs_txt = "cell state   c_t"
    cs_x = x1 - 3.0 - _rich_w(cs_txt, 2.2, tk)
    place(cs_txt, cs_x, y0 + 0.372 * H, 2.2, RD, track=tk)
    rich.extend(_filled_dot(cs_x + 2.0, y0 + 0.348 * H + 0.5, 0.55, RD, feed))
    place("cell state flow", cs_x + 4.8, y0 + 0.348 * H, ts, RD)
    place("(long-term memory)", cs_x + 4.8, y0 + 0.328 * H, ts, RD)

    # input sequence block
    x_in = x0 + 11.0
    y_in_top = y0 + 0.560 * H
    y_in_bot = y0 + 0.468 * H
    place(_spaced("INPUT"), x0 + 3.0, y0 + 0.610 * H, tt, BK)
    place(_spaced("SEQUENCE"), x0 + 3.0, y0 + 0.590 * H, tt, BK)
    place("x_t", x0 + 5.0, y0 + 0.564 * H, 2.6, BK)

    scene.halo_labels(labels)

    # ---- streamline families --------------------------------------------
    # Solid families go FIRST: they are the plate's dominant read, so they get
    # first claim on the occupancy grid and stay long and continuous; the
    # dotted gate/information families fill what is left.
    occ = scene.occupancy(sep)
    x_drift = x0

    def emit_family(
        seeds,
        pen,
        own,
        other,
        dotted=False,
        arrow_every=3,
        step=0.85,
        ybar=None,
        arrows_per=2,
    ):
        """Integrate + hand to the engine's pause_resume crowd control.  The
        SAME Occupancy instance is queried first (crowded() does not mutate) so
        arrowheads only land on stretches the engine will actually keep."""
        n = 0
        for sx, sy in seeds:
            pts = _stream(
                sx,
                sy,
                centres,
                clip,
                ((own[0], own[1], r_core), (other[0], other[1], 8.0)),
                step=step,
                max_steps=int(560 * 0.85 / step),
                drift=x_drift,
                ybar=ybar,
            )
            if len(pts) < 12:
                continue
            samples = []
            for i, (px, py) in enumerate(pts):
                dep = HIDE if (dotted and (i % 3)) else 0.0
                samples.append((px, py, dep, pen))
            flags = [i > 6 and occ.crowded(q[0], q[1]) for i, q in enumerate(pts)]
            kept = [i for i, (f_, s_) in enumerate(zip(flags, samples)) if not f_ and s_[2] != HIDE]
            scene.lines([samples], occupancy=occ, warmup=6, min_kept=5)
            n += 1
            if not arrow_every or n % arrow_every or len(kept) < 26:
                continue
            fracs = (0.30, 0.68) if arrows_per == 2 else (0.48,)
            for frac in fracs:
                idx = kept[int(frac * (len(kept) - 1))]
                if idx < 2 or idx >= len(pts) - 2:
                    continue
                dx = pts[idx + 1][0] - pts[idx - 1][0]
                dy = pts[idx + 1][1] - pts[idx - 1][1]
                out.extend(_arrow(pts[idx][0], pts[idx][1], dx, dy, pen=pen, f=feed))

    def ring_seeds(cy_k, r, n, phase=0.0, jit=2.6, half=0):
        pts = []
        for k in range(n):
            a = phase + 2 * math.pi * k / n
            rr = r + rng.uniform(-jit, jit)
            px, py = cx + rr * math.cos(a), cy_k + rr * math.sin(a)
            if half > 0 and py < y_mid - 7.0:
                continue
            if half < 0 and py > y_mid + 7.0:
                continue
            pts.append((px, py))
        return pts

    # a family stops once it is well past the far centre -- keeps the two
    # colours interleaving in a band instead of interpenetrating completely
    bar_h = (yc - 9.0, clip[3])
    bar_c = (clip[1], yh + 9.0)

    for r, n, hf in ((64.0, 38, 1), (50.0, 32, 1), (37.0, 27, 0), (25.0, 20, 0)):
        emit_family(ring_seeds(yh, r, n, 0.07 * r, half=hf), BK, (cx, yh), (cx, yc), ybar=bar_h)
        emit_family(ring_seeds(yc, r, n, 0.11 * r, half=-hf), RD, (cx, yc), (cx, yh), ybar=bar_c)

    # input sequence -> the field (solid, carried by the x_t drift)
    n_in = 6
    in_pts = [(x_in, y_in_bot + (y_in_top - y_in_bot) * k / (n_in - 1)) for k in range(n_in)]
    emit_family(
        [(q[0] + 1.8, q[1]) for q in in_pts], BK, (cx, yh), (cx, yc), arrow_every=2, ybar=bar_h
    )

    # dotted: gate interactions (black) + information flow (red)
    for r, n, hf in ((73.0, 22, 1), (57.0, 19, 1), (43.0, 17, 0)):
        emit_family(
            ring_seeds(yh, r, n, 0.19 * r, half=hf), BK, (cx, yh), (cx, yc),
            dotted=True, arrow_every=4, step=0.55, ybar=bar_h, arrows_per=1,
        )
        emit_family(
            ring_seeds(yc, r, n, 0.23 * r, half=-hf), RD, (cx, yc), (cx, yh),
            dotted=True, arrow_every=4, step=0.55, ybar=bar_c, arrows_per=1,
        )
    emit_family(
        [(q[0] + 1.8, q[1] + 1.5) for q in in_pts], BK, (cx, yh), (cx, yc),
        dotted=True, arrow_every=0, step=0.55, ybar=bar_h,
    )

    # ---- cores ------------------------------------------------------------
    scene.poly(_core_curl(cx, yh, r_core + 0.4, pitch=1.0, turns_dir=1.0), pen=BK)
    scene.poly(_core_curl(cx, yc, r_core + 0.4, pitch=1.0, turns_dir=1.0), pen=RD)

    # ---- dotted t-rings ---------------------------------------------------
    # split into in-rect RUNS before dashing: filtering points and dashing the
    # remainder joins across the gap and draws a chord straight through the plate
    rcl = (x0 + 4.0, y0 + 0.176 * H + 3.5, x1 - 4.0, y1 - 15.0)
    for cy_k, rings, pen in ((yh, rings_h, BK), (yc, rings_c, RD)):
        for r, _a, _t in rings:
            run: List[Tuple[float, float]] = []
            for k in range(441):
                th = 2 * math.pi * k / 440
                px, py = cx + r * math.cos(th), cy_k + RY * r * math.sin(th)
                if rcl[0] < px < rcl[2] and rcl[1] < py < rcl[3]:
                    run.append((px, py))
                else:
                    for seg in _dash(run, on=1.0, off=1.6):
                        scene.poly(seg, pen=pen)
                    run = []
            for seg in _dash(run, on=1.0, off=1.6):
                scene.poly(seg, pen=pen)

    # ---- the axis ---------------------------------------------------------
    scene.poly([(cx, y_bot), (cx, y_top)], pen=BK)
    out.extend(_arrow(cx, y_top, 0, 1, size=3.2, pen=BK, f=feed))
    out.extend(_arrow(cx, y_bot, 0, -1, size=3.2, pen=BK, f=feed))

    # ---- input sequence dots + ellipsis ----------------------------------
    for px, py in in_pts:
        out.extend(_filled_dot(px, py, 0.7, BK, feed))
    for k in range(3):  # horizontal ellipsis beside the column, as in the reference
        out.extend(_filled_dot(x_in - 9.0 + 2.4 * k, y_mid - 0.5, 0.4, BK, feed))

    # ---- leaders ----------------------------------------------------------
    leaders = [
        ((x0 + 36.0, y0 + 0.705 * H), (cx - 58.0, y0 + 0.742 * H), (cx - 30.0, y0 + 0.700 * H), BK),
        ((x0 + 33.0, y0 + 0.424 * H), (cx - 56.0, y0 + 0.452 * H), (cx - 26.0, y0 + 0.512 * H), BK),
        ((fg_x - 3.0, y0 + 0.586 * H), (cx + 40.0, y0 + 0.598 * H), (cx + 14.0, y0 + 0.552 * H), BK),
        ((hs_x - 3.0, y0 + 0.690 * H), (cx + 44.0, y0 + 0.672 * H), (cx + 20.0, y0 + 0.634 * H), BK),
        ((cs_x - 3.0, y0 + 0.362 * H), (cx + 44.0, y0 + 0.380 * H), (cx + 20.0, y0 + 0.418 * H), RD),
    ]
    for p0, p1, p2, pen in leaders:
        for seg in _dash(_bez(p0, p1, p2, 140), on=2.0, off=1.7):
            scene.poly(seg, pen=pen)

    # ---- title block ------------------------------------------------------
    out.extend(giant_type("LSTM", x0 + 3.5, y1 - 13.0, 8.4, pen=BK, weight=0.0, spaced=True))
    ty = y1 - 19.5
    for ln in ("LONG SHORT-TERM MEMORY", "RECURSIVE MEMORY", "THROUGH TIME"):
        out.extend(_spaced_text(ln, x0 + 3.0, ty, 1.55, BK, feed))
        ty -= 3.4

    ry = y1 - 6.0
    for ln in ("MEMORY", "THROUGH", "RECURSION", "THROUGH", "TIME"):
        out.extend(_spaced_text(ln, x1 - 33.0, ry, 1.55, BK, feed))
        ry -= 3.4

    # ---- bottom band ------------------------------------------------------
    band_top = y0 + 0.176 * H
    band_bot = y0 + 0.062 * H
    col1, col2, col3 = x0 + 3.0, x0 + 0.578 * W, x0 + 0.858 * W
    for cxr in (col1, col2, col3):
        out.extend(_poly([(cxr, band_bot), (cxr, band_top)], color=BK, f=feed))

    out.extend(_spaced_text("LSTM EQUATIONS", col1 + 4.0, band_top - 2.0, 1.55, BK, feed))
    out.extend(_rich("c_t = f_t @ c_{t-1} + i_t @ c^_t", col1 + 6.0, band_top - 13.0, 2.7, BK, feed, 0.25)[0])
    out.extend(_rich("h_t = o_t @ tanh(c_t)", col1 + 6.0, band_top - 22.0, 2.7, BK, feed, 0.25)[0])

    out.extend(_spaced_text("FLOW LEGEND", col2 + 4.0, band_top - 2.0, 1.55, BK, feed))
    legend = [
        (BK, False, "hidden state flow (h_t)"),
        (RD, False, "cell state flow (c_t)"),
        (BK, True, "gate interactions"),
        (RD, True, "information flow"),
    ]
    ly = band_top - 9.0
    for pen, dotted, txt in legend:
        sx, ex = col2 + 5.0, col2 + 18.0
        if dotted:
            out.extend(_arrow(sx + 1.4, ly + 0.5, 1, 0, size=1.1, pen=pen, f=feed))
            for seg in _dash([(sx + 2.4 + 0.3 * k, ly + 0.5) for k in range(40)], on=0.5, off=1.1):
                out.extend(_poly(seg, color=pen, f=feed))
        else:
            out.extend(_filled_dot(sx, ly + 0.5, 0.55, pen, feed))
            out.extend(_poly([(sx + 2.4, ly + 0.5), (ex, ly + 0.5)], color=pen, f=feed))
        out.extend(_rich(txt, ex + 2.5, ly, 1.5, BK, feed)[0])
        ly -= 4.4

    ry = band_top - 2.0
    for ln in ("SAME STATE", "REPEATED T TIMES", "RECURSION", "CREATES MEMORY"):
        out.extend(_stroke(ln, col3 + 4.0, ry, 1.5, BK, feed))
        ry -= 3.3
    out.extend(_poly([(col3 + 4.0, ry - 0.6), (col3 + 9.0, ry - 0.6)], color=BK, f=feed))
    ry -= 4.4
    for ln in ("LSTM", "A DYNAMICAL", "MEMORY SYSTEM"):
        out.extend(_stroke(ln, col3 + 4.0, ry, 1.5, BK, feed))
        ry -= 3.3

    # ---- footer + registration -------------------------------------------
    foot = _spaced("MEMORY LIVES IN RECURSION")
    fw = _text_width(foot, 1.5)
    fx = cx - fw / 2.0
    fy = y0 + 4.0
    out.extend(_stroke(foot, fx, fy, 1.5, BK, feed))
    out.extend(_poly([(fx - 7.0, fy + 0.8), (fx - 3.0, fy + 0.8)], color=BK, f=feed))
    out.extend(_poly([(fx + fw + 3.0, fy + 0.8), (fx + fw + 7.0, fy + 0.8)], color=BK, f=feed))

    for px, py in ((x0 + 4, y0 + 4), (x1 - 4, y0 + 4), (x0 + 4, y1 - 4), (x1 - 4, y1 - 4)):
        out.extend(plus_mark(px, py, 3.2, pen=BK, f=feed))

    out.extend(rich)
    return scene.render()


# ---------------------------------------------------------------------------


def _stroke(text: str, x: float, y: float, h: float, pen, feed: int) -> List[GCodeCommand]:
    return _stroke_text(text, x, y, h, color=pen, f=feed)


def _spaced_text(text: str, x: float, y: float, h: float, pen, feed: int) -> List[GCodeCommand]:
    return _stroke(_spaced(text), x, y, h, pen, feed)
