"""THE RECEDING HORIZON — SSM / Mamba (S6) selective state, drawn as a shadow.

The phenomenon, not the apparatus: a selective state-space model has no fixed
memory. Its discretisation step ``dt`` is a function of the input, so the model's
INTERNAL CLOCK races on novel tokens and stands still on predictable ones. The
memory horizon therefore RECEDES (grows one token per token) and is GUILLOTINED
to nothing whenever the selector fires.

Everything drawn is computed from one exact discretised recurrence (real diagonal
S6, zero-order hold):

    dt_t      = softplus(b + g * s_t)                     selective step
    Abar_tn   = exp(-a_n * dt_t)                          ZOH state transition
    Bbar_tn   = (1 - Abar_tn) / a_n * B_t                 ZOH input map
    h_tn      = Abar_tn * h_(t-1)n + Bbar_tn * u_t        the scan
    S_t       = sum_(r<=t) dt_r                           the model's own clock
    H(t)      = max{ l : a_slow * (S_t - S_(t-l)) <= 1 }  memory horizon, tokens

Three reads:
  3 m   — the SCAN: one axonometric corridor, the state h_tn over (time x
          channel), cropped at both frame edges because a sequence model has no
          first and no last token. The grain ramps across the channel axis: the
          timescales a_n are log-spaced, so slow swells sit at the back and fast
          chatter at the front. Red transverse seams where the selector fires.
  1 m   — the HORIZON: a hatched shadow below it. One tooth per token, its
          length EXACTLY the memory horizon in tokens, laid on the same world
          pitch as the time axis. Its silhouette is a sawtooth — 45 degree ramps
          (memory receding) cut to zero at every selection event.
  30 cm — the warped CLOCK RULE (one tick per unit of internal time, so ticks
          bunch where the clock races), the fast channel's stub horizon, the lag
          ruler, the dt stem chart, and the single longest reach in the 3rd pen.

Contract: ``fn(rng, bounds, colors=3) -> list[GCodeCommand]``.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import Scene3D, ScreenThin
from promptplot.generative.engine.geometry import Rect, clip
from promptplot.generative.engine.kit import (
    _pen,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    plus_mark,
    scale_footer,
    swatch_bar,
    type_block,
)

Bounds = Tuple[float, float, float, float]


def _softplus(z: float) -> float:
    return z + math.log1p(math.exp(-z)) if z > 0 else math.log1p(math.exp(z))


def _clip_cmds(cmds, rect: Bounds, feed: int) -> List[GCodeCommand]:
    """Crop every stroke at the frame with the engine's exact segment/boundary
    clipper (no sampling): the corridor and its shadow run off both edges, so
    the sequence reads as having neither a beginning nor an end."""
    region = Rect(*rect)
    out: List[GCodeCommand] = []
    run: List[Tuple[float, float]] = []
    pen: Optional[int] = None

    def flush() -> None:
        nonlocal run
        if len(run) >= 2:
            for piece in clip(run, region, keep="inside"):
                out.extend(_poly(piece, color=pen, f=feed))
        run = []

    for c in cmds:
        if c.command == "G0":
            flush()
            run = [(c.x, c.y)] if c.x is not None and c.y is not None else []
        elif c.command == "M3":
            pen = c.color
        elif c.command == "G1" and c.x is not None and c.y is not None:
            run.append((c.x, c.y))
            pen = c.color
    flush()
    return out


def receding_horizon(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    tokens: int = 88,
    channels: int = 40,
    a_slow: float = 0.150,
    a_fast: float = 2.600,
    chatter: float = 3.2,
    dt_bias: float = -1.55,
    dt_gain: float = 9.0,
    events: int = 5,
    span_x: float = 1.22,
    lean: float = 0.32,
    chan_span: float = 0.24,
    height_mm: float = 12.0,
    floor_mm: float = 56.0,
    anchor: float = 0.250,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE RECEDING HORIZON — a selective state space model (Mamba / S6) drawn
    as the shadow its own memory casts. One exact ZOH-discretised diagonal
    recurrence drives every mark: the corridor is the scanned state h_tn, the
    hatched shadow beneath it is the exact e^-1 memory horizon in tokens, and
    the sawtooth silhouette of that shadow IS selectivity — memory receding at
    one token per token, guillotined wherever the input-dependent step fires."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blk = _pen(0, colors)
    red = _pen(1, colors)
    hero = _pen(2, colors)
    legend = _pen(3, colors) if colors >= 4 else blk

    T, N = tokens, channels

    # ---------------------------------------------------------------- signal
    # TWO features per token, because a real S6 block reads DIFFERENT learned
    # linear projections of the same embedding:
    #   s_t  SALIENCE — a boundary/delimiter feature, ~0 inside a topic and ~1
    #                   at a topic switch. The learned Delta-head reads THIS.
    #   u_t  SIGNAL   — what the state integrates: a level per topic + a slow
    #                   swell + a mid wave + a large token-scale chatter. The
    #                   log-spaced timescales resolve it differently, and THAT
    #                   is the grain ramp across the corridor.
    cut = sorted(
        {
            int(min(T - 5, max(7, ((k + 1) / (events + 1) + rng.uniform(-0.05, 0.05)) * T)))
            for k in range(events)
        }
    )
    half = [
        t
        for t in sorted({int(min(T - 5, max(7, rng.uniform(0.08, 0.92) * T))) for _ in range(3)})
        if all(abs(t - cc) > 4 for cc in cut)
    ]
    sal = [0.02 + 0.11 * rng.fbm(t * 0.19 + 5.5, 13.0) for t in range(T)]
    for t in cut:
        sal[t] = 0.97  # a full topic boundary: the selector saturates
    for t in half:
        sal[t] = 0.55  # a half-salient token: a dent, not a guillotine
    dt = [_softplus(dt_bias + dt_gain * sal[t]) for t in range(T)]

    lvl = 0.0
    L = []
    for t in range(T):
        if t in cut:
            lvl += rng.choice([-1.0, 1.0]) * rng.uniform(0.6, 1.0)
        L.append(lvl)
    swell = [2 * rng.fbm(t * 0.035 + 2.2, 5.1) - 1 for t in range(T)]
    mid = [2 * rng.noise2d(t * 0.11 + 1.7, 3.3) - 1 for t in range(T)]
    chat = [2 * rng.noise2d(t * 0.55 + 9.1, 19.1) - 1 for t in range(T)]
    u = [L[t] + 0.75 * swell[t] + 0.85 * mid[t] + chatter * chat[t] for t in range(T)]
    mu = sum(u) / T
    u = [v - mu for v in u]  # the stream is mean-centred (LayerNorm, as always)
    B = [0.5 + 0.5 * math.tanh(1.2 * u[t]) for t in range(T)]  # B_t = s_B(x_t)

    # ------------------------------------------------------------- the scan
    a = np.asarray([a_slow * (a_fast / a_slow) ** (n / (N - 1)) for n in range(N)])
    Hs = np.zeros((T, N))
    h = np.zeros(N)
    for t in range(T):
        Abar = np.exp(-a * dt[t])
        Bbar = (1.0 - Abar) / a * B[t]
        h = Abar * h + Bbar * u[t]
        Hs[t] = h
    # the readout C is mean-centred and normalises the per-channel gains, so
    # what survives across the channel axis is the TIMESCALE, not the gain
    Hs = Hs - Hs.mean(axis=0)
    Z = Hs / (np.sqrt((Hs**2).mean(axis=0)) + 1e-9)
    Z = np.clip(Z / 1.9, -1.0, 1.0)

    # --------------------------------------------------------- the horizon
    S = []
    acc = 0.0
    for t in range(T):
        acc += dt[t]
        S.append(acc)

    def horizon(t: int, tgt: float) -> float:
        """Exact e^-1 memory horizon in TOKENS: the largest (fractional) lag l
        with a*(S_t - S_(t-l)) <= 1, i.e. the point where the accumulated
        selective decay has eaten one time-constant of the channel."""
        rem = tgt
        for k in range(1, t + 2):
            seg = dt[t - k + 1]
            if rem <= seg:
                return (k - 1) + rem / seg
            rem -= seg
        return float(t + 1)

    Hz = [horizon(t, 1.0 / a_slow) for t in range(T)]
    Hf = [horizon(t, 1.0 / a_fast) for t in range(T)]
    # a selection event is DERIVED, never scripted: one step erases the slowest
    # channel's memory outright  (a_slow * dt_t >= 1  <=>  H(t) < 1)
    fires = [t for t in range(T) if a_slow * dt[t] >= 1.0]
    t_star = max(range(T), key=lambda t: Hz[t])

    # ---------------------------------------------- ONE axonometric basis
    # A, CD and HY are fixed for the WHOLE scene; the floor plate shares them
    # exactly and is displaced by a pure -wy drop, so corresponding corners of
    # the corridor and its shadow stay in register (dotted projection lines
    # below prove it). A plate that must be smaller shrinks its world FOOTPRINT.
    A = span_x * W / (T - 1)  # screen mm per token along +wx
    CD = lean * A  # screen drop per unit of (wx + wz)
    HY = height_mm / 0.5  # wy in [-0.5, 0.5] -> +- height_mm
    cs = chan_span * W / ((N - 1) * A)  # channel pitch, measured IN TOKEN UNITS
    Zc = cs * (N - 1)
    Yf = floor_mm / HY
    cx = x0 - 0.5 * (span_x - 1.0) * W
    cy = y1 - anchor * H

    def P(wx: float, wy: float, wz: float) -> Tuple[float, float]:
        return (cx + (wx - wz) * A, cy + wy * HY - (wx + wz) * CD)

    def D(wx: float, wy: float, wz: float) -> float:
        return (wx + wz) + 0.12 * wy

    scene = Scene3D(rng, bounds, feed=feed, px=(900, 340), pad=3.0, fit="none", tip=0.5)

    # ------------------------------------------------------------- labels
    # type lives on its own pen and reserves its halos BEFORE any mesh is drawn
    CL = x0 + 0.018 * W
    CR = x0 + 0.55 * W
    p_slow = P(0.24 * T, 0.0, 0.0)
    p_fast = P(0.50 * T, 0.0, Zc)

    def LBL(text, lx, ly, th, pen):
        """Keep every glyph on the paper (the composition crops, the type never
        does)."""
        return (text, min(max(lx, x0 + 1.5), x1 - _text_width(text, th) - 1.5), ly, th, pen)

    t_fire = min(fires, key=lambda t: abs(t - 0.55 * T)) if fires else T // 2
    p_fire = P(t_fire, 0.0, 0.0)
    scene.halo_labels(
        [
            ("1", CR, y1 - 0.215 * H, 3.0, legend),
            (_spaced("THE SCAN"), CR + 7.0, y1 - 0.215 * H, 1.9, legend),
            (_spaced("STATE H T N"), CR + 7.0, y1 - 0.234 * H, 1.35, legend),
            (_spaced("%d CHANNELS . LOG SPACED A N" % N), CR + 7.0, y1 - 0.249 * H, 1.35, legend),
            LBL(_spaced("SLOW . A 0.15"), p_slow[0] + 3.0, p_slow[1] + height_mm + 5.0, 1.35, legend),
            LBL(_spaced("FAST . A 2.60"), p_fast[0] - 24.0, p_fast[1] - height_mm - 5.5, 1.35, legend),
            LBL(_spaced("SELECTION . DT FIRES"), p_fire[0], p_fire[1] + height_mm + 12.0, 1.6, red),
            LBL(_spaced("MEMORY CUT TO ZERO"), p_fire[0], p_fire[1] + height_mm + 7.0, 1.35, red),
            ("2", CL, y1 - 0.760 * H, 3.0, legend),
            (_spaced("THE HORIZON"), CL + 7.0, y1 - 0.760 * H, 1.9, legend),
            (_spaced("LAG . TOKENS BACK"), CL + 7.0, y1 - 0.779 * H, 1.35, legend),
            (_spaced("SAME PITCH AS TIME"), CL + 7.0, y1 - 0.794 * H, 1.35, legend),
            LBL(_spaced("INTERNAL CLOCK"), CL + 0.34 * W, y1 - 0.760 * H, 1.9, legend),
            LBL(_spaced("ONE TICK PER UNIT OF S"), CL + 0.34 * W, y1 - 0.779 * H, 1.35, legend),
            LBL(_spaced("TICKS BUNCH AS IT RACES"), CL + 0.34 * W, y1 - 0.794 * H, 1.35, legend),
            LBL(_spaced("REACH"), CL + 0.72 * W, y1 - 0.760 * H, 1.9, hero),
            LBL(
                _spaced("%d TOKENS BACK" % int(round(Hz[t_star]))),
                CL + 0.72 * W,
                y1 - 0.779 * H,
                1.35,
                hero,
            ),
            LBL(_spaced("DEEPEST MEMORY"), CL + 0.72 * W, y1 - 0.794 * H, 1.35, hero),
        ]
    )

    # -------------------------------------------------------- 1. the scan
    SX = np.zeros((T, N))
    SY = np.zeros((T, N))
    DE = np.zeros((T, N))
    for t in range(T):
        for n in range(N):
            wy = 0.5 * Z[t, n]
            SX[t, n], SY[t, n] = P(t, wy, n * cs)
            DE[t, n] = D(t, wy, n * cs)
    scene.surface(SX, SY, DE, pen=blk, thin=ScreenThin(gap_mm=0.95, far_mult=1.8))

    # the selection seams: the exact transverse profile at each firing token,
    # depth-tested against the same field so near ridges still occlude them
    scene.lines(
        [[(SX[t, n], SY[t, n], DE[t, n], red) for n in range(N)] for t in fires],
        mode="over",
    )
    # the nearest channel doubled: the front silhouette of the corridor
    scene.lines([[(SX[t, N - 1], SY[t, N - 1], DE[t, N - 1], blk) for t in range(T)]], mode="over")

    # ----------------------------------------------------- 2. the horizon
    # one tooth per token; its length is H(t) in TOKENS on the same world pitch
    # as the time axis. Parallel teeth ~1.6 mm apart = a hatched cast shadow.
    rule = [P(t, -Yf, 0.0) for t in range(T)]
    for t in range(T):
        # the tooth immediately BEFORE a guillotine is the last long memory
        scene.poly([rule[t], P(t, -Yf, Hz[t])], pen=(red if (t + 1) in fires else blk))
    # the receding silhouette, broken at every guillotine (no return stroke)
    seg: List[Tuple[float, float]] = []
    for t in range(T):
        if t in fires:
            if len(seg) >= 2:
                scene.poly(seg, pen=red)
            seg = []
        seg.append(P(t, -Yf, Hz[t]))
    if len(seg) >= 2:
        scene.poly(seg, pen=red)
    # the fastest channel's horizon: a stub curve hugging the rule
    scene.poly([P(t, -Yf, Hf[t]) for t in range(T)], pen=blk)

    # --------------------------------------------- the warped clock rule
    scene.poly([rule[0], rule[T - 1]], pen=blk)
    occ = scene.occupancy(0.9)  # engine-native crowd control for the tick burst
    k = 1
    while k < S[-1]:
        t = next((i for i in range(T) if S[i] >= k), None)
        if t is None:
            break
        s0 = S[t - 1] if t else 0.0  # exact fractional token of clock unit k
        tf = (t - 1) + (k - s0) / max(1e-9, dt[t]) if t else k / max(1e-9, dt[0])
        base_p = P(tf, -Yf, 0.0)
        if not occ.crowded(*base_p):
            occ.add(*base_p)
            scene.poly([base_p, P(tf, -Yf + (0.26 if k % 5 == 0 else 0.13), 0.0)], pen=blk)
        k += 1

    # ------------------------------------------- 3. the longest reach
    # a green segment running BACK along time from t*, exactly as long as the
    # tooth at t*: the drawing states its own scale twice, on two axes.
    back = t_star - Hz[t_star]
    for off in (-0.015, 0.015):
        scene.poly([P(back, -Yf - 0.20 + off, 0.0), P(t_star, -Yf - 0.20 + off, 0.0)], pen=hero)
    for e in (back, t_star):
        scene.poly([P(e, -Yf - 0.36, 0.0), P(e, -Yf - 0.07, 0.0)], pen=hero)

    # ------------------------------ dotted projection lines (never arrows)
    def projection(p0, p1, pen, dash=3.4, duty=0.48):
        L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        n = max(4, int(L / dash))
        for q in range(n):
            ta, tb = q / n, (q + duty) / n
            scene.poly(
                [
                    (p0[0] + (p1[0] - p0[0]) * ta, p0[1] + (p1[1] - p0[1]) * ta),
                    (p0[0] + (p1[0] - p0[0]) * tb, p0[1] + (p1[1] - p0[1]) * tb),
                ],
                pen=pen,
            )

    for t in fires:  # each selection seam tied to the pinch it causes
        projection(P(t, 0.5 * Z[t, 0] - 0.08, 0.0), P(t, -Yf + 0.08, 0.0), red)
    projection(P(t_star, 0.5 * Z[t_star, 0] - 0.08, 0.0), P(t_star, -Yf + 0.08, 0.0), hero)
    for wz in (0.0, Zc):  # the corridor's world edges dropped onto the plate
        for t in (0.0, float(T - 1)):
            projection(P(t, 0.0, wz), P(t, -Yf, wz), blk, dash=4.6, duty=0.40)

    # ------------------------------------------------------- the lag ruler
    t_r = int(T * 0.13)
    for lag in (5, 10, 15, 20):
        scene.poly([P(t_r, -Yf, lag), P(t_r - 1.0, -Yf, lag)], pen=blk)
    pr = P(t_r - 1.3, -Yf, 20.0)
    scene.emit(_stroke_text(_spaced("20"), pr[0] - 7.5, pr[1] - 0.8, 1.35, color=legend, f=feed))

    out = scene.render()

    # ------------------------------------------------------- dt stem chart
    # aligned to the SAME token x pitch as the corridor above it
    ybase = y0 + 0.055 * H
    xend = x1 - 0.20 * W
    dmax = max(dt) or 1.0
    out += _poly([(x0, ybase), (xend, ybase)], color=blk, f=feed)
    for t in range(T):
        sx = cx + t * A
        if not (x0 <= sx <= xend):
            continue
        out += _poly(
            [(sx, ybase), (sx, ybase + 16.0 * dt[t] / dmax)],
            color=(red if t in fires else blk),
            f=feed,
        )
    out += _stroke_text(
        _spaced("DT T . THE LEARNED STEP"), x0, ybase - 4.6, 1.5, color=legend, f=feed
    )
    out += _stroke_text(
        _spaced("SOFTPLUS OF A LINEAR READ OF X T"), x0, ybase - 8.0, 1.35, color=legend, f=feed
    )

    # ---------------------------------------------------------- furniture
    out += type_block(["THE RECEDING", "HORIZON"], CL, y1 - 6.0, height=6.0, pen=legend, f=feed)
    out += _stroke_text(
        _spaced("EVERY TOKEN CHOOSES HOW FAR BACK IT CAN SEE"),
        CL,
        y1 - 33.0,
        2.1,
        color=legend,
        f=feed,
    )
    out += _stroke_text(
        _spaced("SELECTIVE STATE SPACE . S6"), CL, y1 - 39.0, 1.5, color=legend, f=feed
    )
    out += swatch_bar(x1 - 9.0, y1 - 5.0, [blk, red, hero], size=2.8, f=feed)
    out += plus_mark(*P(t_star, -Yf, 0.0), s=1.5, pen=hero, f=feed)
    out += scale_footer(
        bounds, text="H T = EXP(-A DT T) H T-1 + B T X T", pen=legend, height=2.3, f=feed
    )

    return _clip_cmds(out, (x0, y0, x1, y1), feed)
