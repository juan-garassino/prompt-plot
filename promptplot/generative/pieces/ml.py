"""ML pieces — neural networks & learning drawn as phenomena, not diagrams.

The "abstract neural representations for penplotters" series plus the earlier
ML compositions. Every function is a seeded composition
``(rng, bounds, colors=3, ...) -> List[GCodeCommand]``; the seed fine-tunes.
Style is applied at the lamina level.
"""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

from ...models import GCodeCommand
from ..rng import SeededRNG
from ..engine import Occupancy, PolarLOD, Scene3D, ScreenThin  # noqa: F401
from ..engine3d import _fit_out, _zbuf_terrain  # noqa: F401
from ..kit import (  # noqa: F401
    Bounds,
    BAUHAUS_PALETTE,
    BLUE,
    PINK,
    BLACK,
    _pen,
    fill_rect,
    fill_disc,
    fill_quarter,
    fill_ring,
    _runs_from_cmds,
    _cut,
    _clip_runs,
    _rect_keep,
    _fit_runs_cover,
    _emit_runs,
    circle,
    dotted_circle,
    plus_mark,
    crosshair_rules,
    swatch_bar,
    _spaced,
    type_block,
    scale_footer,
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

import io
import zipfile



# ---------------------------------------------------------------------------
# piece 04 — PARAMETER FIELD (Hinton diagram)
# ---------------------------------------------------------------------------


def _load_qkv(weights: str, block: int):
    import numpy as np

    buf = io.BytesIO(zipfile.ZipFile(weights).read("model.weights.h5"))
    import h5py

    f5 = h5py.File(buf, "r")
    base = "layers/transformer_encoder_block" + ("" if block == 0 else f"_{block}")

    def att(nm):
        Wm = np.array(f5[f"{base}/att/{nm}/vars/0"])
        return Wm.reshape(Wm.shape[0], -1)

    return [att("query_dense"), att("key_dense"), att("value_dense")]




# ---------------------------------------------------------------------------
# piece 03 — ATTENTION
# ---------------------------------------------------------------------------


def bauhaus_attention(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    tokens: int = 24,
    topk: int = 2,
    temp: float = 1.0,
    attn_npz: str = "",
    block: int = 5,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """A huge token ring cropped at three frame edges; the ring is rotated so
    the sink token lands on the left axis as one big solid blue disc, and the
    strongest chords into it run pink — a directional wedge of attention."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    out: List[GCodeCommand] = []
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    frame_keep = _rect_keep(bounds)

    A = None
    if attn_npz:
        try:
            import numpy as np

            A = np.load(attn_npz)["attn"][block][0]
            tokens = A.shape[-1]
        except Exception:
            A = None
    if A is None:
        A = _attention_matrix(rng, tokens, 0, temp, True, "", 0)

    col_mass = [sum(float(A[q][k]) for q in range(tokens)) for k in range(tokens)]
    sink = max(range(tokens), key=lambda k: col_mass[k])

    # ring center right of middle; radius huge so the ring crops at the frame;
    # phase rotated so the sink token sits on the left axis at mid-height
    ccx, ccy = x0 + 0.62 * W, y0 + 0.46 * H
    R = min(0.66 * H, 0.60 * W)
    phase = math.pi - 2 * math.pi * sink / tokens
    pos = [
        (
            ccx + R * math.cos(2 * math.pi * t / tokens + phase),
            ccy + R * math.sin(2 * math.pi * t / tokens + phase),
        )
        for t in range(tokens)
    ]
    sk = pos[sink]
    r_sink = min(10.0, sk[0] - x0 - 0.8, x1 - sk[0] - 0.8, sk[1] - y0 - 0.8, y1 - sk[1] - 0.8)
    r_sink = max(1.5, r_sink)

    out += dotted_circle(ccx, ccy, R, pen=black, bounds=bounds, f=feed)

    # chords into the sink, ranked: top 12 pink (top 3 of those triple-pass),
    # the next 12 thin black, the rest dropped — no fan flood
    into_sink = []
    plain = []
    for q in range(tokens):
        row = sorted(range(tokens), key=lambda k: -float(A[q][k]))[:topk]
        for k in row:
            if k == q or float(A[q][k]) < 0.03:
                continue
            if k == sink:
                into_sink.append((float(A[q][k]), q))
            else:
                plain.append((k, q))
    into_sink.sort(reverse=True)

    for k, q in plain:
        if q == sink:
            continue
        for seg in _clip_runs([[pos[k], pos[q]]], frame_keep):
            out += _poly(seg, color=black, f=feed)

    for rank, (_w, q) in enumerate(into_sink[:24]):
        xb, yb = pos[q]
        dx, dy = xb - sk[0], yb - sk[1]
        n = math.hypot(dx, dy) or 1.0
        ax_, ay_ = sk[0] + dx / n * (r_sink + 1.0), sk[1] + dy / n * (r_sink + 1.0)
        if rank < 12:
            passes = 3 if rank < 3 else 1
            for pp in range(passes):
                o = (pp - (passes - 1) / 2) * 0.32
                oxp, oyp = -dy / n * o, dx / n * o
                for seg in _clip_runs([[(ax_ + oxp, ay_ + oyp), (xb + oxp, yb + oyp)]], frame_keep):
                    out += _poly(seg, color=pink, f=feed)
        else:
            for seg in _clip_runs([[(ax_, ay_), (xb, yb)]], frame_keep):
                out += _poly(seg, color=black, f=feed)

    for t in range(tokens):
        if t == sink:
            continue
        px, py = pos[t]
        if x0 + 2.2 < px < x1 - 2.2 and y0 + 2.2 < py < y1 - 2.2:
            out += fill_disc(px, py, 1.4, spacing=0.45, pen=black, f=feed)
    out += fill_disc(sk[0], sk[1], r_sink, spacing=0.5, pen=blue, f=feed)

    # left axis: type over the sink, swatches, footer
    xT = x0 + 0.015 * W
    out += type_block(["ATTENTION"], xT, y1 - 7.0, height=2.8, pen=black, f=feed)
    out += swatch_bar(xT, y1 - 17.0, [black, blue, pink], size=3.2, f=feed)
    out += _stroke_text(_spaced("M 1:80"), xT, y0 + 2.0, 2.2, color=black, f=feed)
    return out




def bauhaus_weights(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    weights: str = "",
    block: int = 0,
    rows: int = 22,
    cols: int = 16,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """A true Hinton diagram in the Bauhaus language: Q | K | V panels on a
    strict grid, every weight a solid circle — radius by magnitude, blue
    positive, pink negative. Trained weights when a checkpoint is given."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    out: List[GCodeCommand] = []
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)

    panels = None
    if weights:
        try:
            panels = _load_qkv(weights, block)
        except Exception:
            panels = None
    if panels is None:
        panels = [
            np.array([[rng.random() * 2 - 1 for _ in range(48)] for _ in range(72)])
            for _ in range(3)
        ]

    gap = 0.045 * W
    pw = (W - 4 * gap) / 3.0
    pitch = min(pw / cols, (H * 0.62) / rows)
    ph = pitch * rows
    py_top = y1 - 0.14 * H
    labels = ["Q", "K", "V"]
    for pi, Wm in enumerate(panels):
        # block-mean downsample to rows x cols, signed
        R0, C0 = Wm.shape
        br, bc = max(1, R0 // rows), max(1, C0 // cols)
        M = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                blk = Wm[i * br : (i + 1) * br, j * bc : (j + 1) * bc]
                if blk.size:
                    # magnitude by |w| mean (doesn't cancel), sign by mean
                    M[i, j] = math.copysign(float(np.abs(blk).mean()), float(blk.mean()))
        norm = float(np.percentile(np.abs(M), 90)) or 1.0
        rx = x0 + gap + pi * (pw + gap) + (pw - pitch * cols) / 2.0
        for i in range(rows):
            cy_ = py_top - pitch * (i + 0.5)
            for j in range(cols):
                w = float(M[i, j])
                rr = min(1.0, abs(w) / norm) * pitch * 0.38
                if rr < 0.22:
                    continue
                cx_ = rx + pitch * (j + 0.5)
                pen = blue if w >= 0 else pink
                if rr < 0.55:
                    out += _poly([(cx_ - rr, cy_), (cx_ + rr, cy_)], color=pen, f=feed)
                else:
                    out += fill_disc(cx_, cy_, rr, spacing=0.42, pen=pen, f=feed)
        cap = labels[pi]
        out += _stroke_text(
            _spaced(cap), rx + pitch * cols / 2 - 2.0, py_top - ph - 6.5, 3.0, color=black, f=feed
        )
        if pi < 2:
            bx = x0 + gap + (pi + 1) * (pw + gap) - gap / 2
            out += _poly([(bx, py_top - ph), (bx, py_top)], color=black, f=feed)

    out += type_block(["PARAMETER", "FIELD"], x0 + 5.0, y0 + 16.5, pen=black, f=feed)
    out += swatch_bar(x1 - 8.0, y1 - 4.0, [black, blue, pink], f=feed)
    out += plus_mark(x1 - 9.0, y0 + 20.0, pen=black, f=feed)
    out += scale_footer(bounds, pen=black, f=feed)
    return out




# ---------------------------------------------------------------------------
# piece 05 — FORWARD PASS (perceptron)
# ---------------------------------------------------------------------------


# RETIRED (curation, no-schematics rule): a wiring diagram cannot be art. The
# 'forward pass' concept is superseded by the ml-01 space-warping piece. Kept
# for version history; deregistered from GENERATOR_REGISTRY.
def bauhaus_perceptron(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    layers: Sequence[int] = (6, 8, 8, 3),
    weights: str = "",
    feed: int = 2200,
) -> List[GCodeCommand]:
    """An MLP as constructivist art: neurons are solid discs, connections carry
    1-3 parallel passes by |w|, the winning forward path runs bold pink."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    out: List[GCodeCommand] = []
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)

    # weight matrices: slices of the real checkpoint when given, else seeded
    mats = []
    try:
        if weights:
            qkv = _load_qkv(weights, 0)
            src = qkv[0]
            for a, b in zip(layers, layers[1:]):
                mats.append(
                    [
                        [float(src[i % src.shape[0]][j % src.shape[1]]) for j in range(b)]
                        for i in range(a)
                    ]
                )
    except Exception:
        mats = []
    if not mats:
        for a, b in zip(layers, layers[1:]):
            mats.append([[rng.random() * 2 - 1 for _ in range(b)] for _ in range(a)])

    n_l = len(layers)
    lx = [x0 + W * (0.14 + 0.72 * i / (n_l - 1)) for i in range(n_l)]

    def ys(n):
        span = H * 0.62
        return [y0 + H * 0.52 - span / 2 + span * (j + 0.5) / n for j in range(n)]

    pos = [[(lx[i], y) for y in ys(n)] for i, n in enumerate(layers)]

    # bar behind the second hidden layer
    bx = lx[min(2, n_l - 1)]
    out += fill_rect(bx - 5.0, y0 + 0.5, bx + 5.0, y1 - 0.5, spacing=0.6, pen=black, f=feed)

    # winning path: greedy argmax |w| from a seeded input neuron
    path = [rng.randint(0, layers[0] - 1)]
    for li, M in enumerate(mats):
        row = M[path[-1]]
        path.append(max(range(len(row)), key=lambda j: abs(row[j])))

    for li, M in enumerate(mats):
        norm = max(abs(v) for row in M for v in row) or 1.0
        for i, row in enumerate(M):
            for j, w in enumerate(row):
                t = abs(w) / norm
                if t < 0.45:
                    continue
                (xa, ya), (xb, yb) = pos[li][i], pos[li + 1][j]
                on_path = path[li] == i and path[li + 1] == j
                pen = pink if on_path else black
                passes = 3 if on_path else (2 if t > 0.75 else 1)
                dx, dy = xb - xa, yb - ya
                n = math.hypot(dx, dy) or 1.0
                oxp, oyp = -dy / n * 0.3, dx / n * 0.3
                for pp in range(passes):
                    o = pp - (passes - 1) / 2
                    out += _poly(
                        [(xa + oxp * o, ya + oyp * o), (xb + oxp * o, yb + oyp * o)],
                        color=pen,
                        f=feed,
                    )

    for li, col in enumerate(pos):
        for j, (px, py) in enumerate(col):
            r = 2.0 + 1.6 * rng.random()
            if li == 0:
                out += fill_disc(px, py, r, spacing=0.5, pen=blue, f=feed)
            elif li == n_l - 1:
                out += fill_disc(px, py, r, spacing=0.5, pen=pink, f=feed)
            elif path[li] == j:
                out += fill_disc(px, py, r * 0.9, spacing=0.5, pen=black, f=feed)
            else:
                out += circle(px, py, r * 0.9, pen=black, f=feed)

    out += type_block(["FORWARD", "PASS"], x0 + 5.0, y1 - 6.0, pen=black, f=feed)
    out += swatch_bar(x0 + 5.0, y1 - 22.0, [black, blue, pink], f=feed)
    out += plus_mark(x1 - 9.0, y1 - 9.0, pen=black, f=feed)
    out += scale_footer(bounds, pen=black, f=feed)
    return out




# ---------------------------------------------------------------------------
# piece 06 — GRADIENT DESCENT  → reworked as WATERSHED (basin of attraction)
# ---------------------------------------------------------------------------


def bauhaus_gradient(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    n_seeds: int = 220,
    min_sep: float = 2.4,
    rk4_dt: float = 0.9,
    max_steps: int = 420,
    deep_depth: float = 1.0,
    shallow_depth: float = 0.55,
    settle_eps: float = 0.006,
    momentum: float = 0.9,
    fill_spacing: float = 0.5,
    sink_scale: float = 1.0,
    sink_spacing: float = 0.0,
    joint_gap: float = 2.4,
    braid_passes: int = 3,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """WATERSHED — gradient descent as a BASIN OF ATTRACTION. The whole
    parameter plane rains downhill (exact RK4 on an analytic 2-Gaussian loss)
    into two sinks; the separatrix is left as a knife of blank paper. Each
    streamline is black on the plateau and inks its last stretch in its
    destination's hue (blue = deep global well, pink = shallow local trap). One
    blue heavy-ball-momentum channel visibly OVERSHOOTS the deep sink and rings
    back — the optimizer, not decorative flow."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    fx0, fy0, fx1, fy1 = x0 + 6, y0 + 12, x1 - 6, y1 - 22
    fw, fh = fx1 - fx0, fy1 - fy0
    rect_keep = _rect_keep((fx0, fy0, fx1, fy1))
    typebox = lambda p: p[0] < fx0 + 0.34 * W and p[1] > fy1 - 0.16 * H
    keep = lambda p: rect_keep(p) and not typebox(p)

    def u2px(u):
        return fx0 + (u + 1) / 2 * fw

    def v2py(v):
        return fy0 + (v + 1) / 2 * fh

    # exact analytic loss: two negative Gaussians + a mild draining bowl
    gux, guy, sd = -0.34, -0.30, 0.42  # deep global well (lower-left)
    sux, svy, ss = 0.40, 0.34, 0.55  # shallow local trap (upper-right)

    def gradL(u, v):
        e1 = deep_depth * math.exp(-((u - gux) ** 2 + (v - guy) ** 2) / (2 * sd * sd))
        e2 = shallow_depth * math.exp(-((u - sux) ** 2 + (v - svy) ** 2) / (2 * ss * ss))
        gx = 0.24 * u + e1 * (u - gux) / (sd * sd) + e2 * (u - sux) / (ss * ss)
        gy = 0.24 * v + e1 * (v - guy) / (sd * sd) + e2 * (v - svy) / (ss * ss)
        return gx, gy

    def rhs(u, v):
        gx, gy = gradL(u, v)
        n = math.hypot(gx, gy) or 1e-9
        return -gx / n, -gy / n

    # locate the TWO true sinks by descent from a coarse lattice
    def descend(u, v):
        for _ in range(800):
            gx, gy = gradL(u, v)
            n = math.hypot(gx, gy)
            if n < settle_eps:
                break
            u -= 0.02 * gx
            v -= 0.02 * gy
        return u, v

    ends = [descend(-1 + 2 * i / 5, -1 + 2 * j / 5) for i in range(6) for j in range(6)]
    gc = [e for e in ends if (e[0] - gux) ** 2 + (e[1] - guy) ** 2 <= (e[0] - sux) ** 2 + (e[1] - svy) ** 2]
    sc = [e for e in ends if e not in gc]
    gsink = (sum(p[0] for p in gc) / len(gc), sum(p[1] for p in gc) / len(gc)) if gc else (gux, guy)
    ssink = (sum(p[0] for p in sc) / len(sc), sum(p[1] for p in sc) / len(sc)) if sc else (sux, svy)
    gpx, spx = (u2px(gsink[0]), v2py(gsink[1])), (u2px(ssink[0]), v2py(ssink[1]))
    rscale = max(0.6, min(1.0, min(fw, fh) / 160))
    deep_r, shallow_r = 13.0 * rscale * sink_scale, 5.0 * rscale * sink_scale

    # evenly-spaced streamlines (Jobard–Lefebvre, seed-based)
    cell = max(min_sep, 0.5)
    occ: dict = {}

    def gkey(px, py):
        return (int((px - fx0) / cell), int((py - fy0) / cell))

    def too_close(px, py):
        # exempt a capture radius near each sink so tributaries reach the rim
        if math.hypot(px - gpx[0], py - gpx[1]) < deep_r + 1.2 * min_sep:
            return False
        if math.hypot(px - spx[0], py - spx[1]) < shallow_r + 1.2 * min_sep:
            return False
        gk = gkey(px, py)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for qx, qy in occ.get((gk[0] + di, gk[1] + dj), []):
                    if (px - qx) ** 2 + (py - qy) ** 2 < min_sep * min_sep:
                        return True
        return False

    def register(pts):
        for px, py in pts:
            occ.setdefault(gkey(px, py), []).append((px, py))

    h = 0.02 * rk4_dt

    def trace(u, v):
        pts = [(u2px(u), v2py(v))]
        skey = None
        for _ in range(max_steps):
            gx, gy = gradL(u, v)
            if math.hypot(gx, gy) < settle_eps:
                break
            k1 = rhs(u, v)
            k2 = rhs(u + 0.5 * h * k1[0], v + 0.5 * h * k1[1])
            k3 = rhs(u + 0.5 * h * k2[0], v + 0.5 * h * k2[1])
            k4 = rhs(u + h * k3[0], v + h * k3[1])
            u += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            v += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            px, py = u2px(u), v2py(v)
            if math.hypot(px - gpx[0], py - gpx[1]) < deep_r + 0.6:
                skey = "b"
                break
            if math.hypot(px - spx[0], py - spx[1]) < shallow_r + 0.6:
                skey = "p"
                break
            if not keep((px, py)) or too_close(px, py):
                break
            pts.append((px, py))
        if skey is None:
            db = (pts[-1][0] - gpx[0]) ** 2 + (pts[-1][1] - gpx[1]) ** 2
            dp = (pts[-1][0] - spx[0]) ** 2 + (pts[-1][1] - spx[1]) ** 2
            skey = "b" if db <= dp else "p"
        return pts, skey

    grid_n = max(6, int(math.sqrt(n_seeds)))
    starts = []
    for i in range(grid_n):
        for j in range(grid_n):
            su = -1.05 + 2.1 * (i + 0.5) / grid_n + rng.uniform(-0.3, 0.3) * (2.1 / grid_n)
            sv = -1.05 + 2.1 * (j + 0.5) / grid_n + rng.uniform(-0.3, 0.3) * (2.1 / grid_n)
            starts.append((su, sv))
    rng.shuffle(starts)

    streams = []  # (pts, skey, start_uv)
    for su, sv in starts:
        p0 = (u2px(su), v2py(sv))
        if not keep(p0) or too_close(*p0):
            continue
        pts, skey = trace(su, sv)
        if len(pts) < 4:
            continue
        register(pts)
        streams.append((pts, skey, (su, sv)))

    # the hero: the blue-basin tributary starting farthest up-plateau
    hero_idx = -1
    best_d = -1.0
    for i, (pts, skey, st) in enumerate(streams):
        if skey == "b":
            d = (st[0] - gsink[0]) ** 2 + (st[1] - gsink[1]) ** 2
            if d > best_d:
                best_d, hero_idx = d, i

    # draw the field: black plateau, destination-hued last stretch.
    # NO OVERLAP joint: black ends joint_gap/2 BEFORE the cut and the colored
    # tail starts joint_gap/2 AFTER it, so round acrylic pen caps butt cleanly
    # instead of overpainting each other (feedback from the plotted 17×24).
    def _split_gap(pts, ncut, gap):
        acc = 0.0
        b_end = ncut
        while b_end > 1 and acc < gap / 2.0:
            acc += math.hypot(
                pts[b_end][0] - pts[b_end - 1][0], pts[b_end][1] - pts[b_end - 1][1]
            )
            b_end -= 1
        acc = 0.0
        t_start = ncut
        while t_start < len(pts) - 1 and acc < gap / 2.0:
            acc += math.hypot(
                pts[t_start + 1][0] - pts[t_start][0], pts[t_start + 1][1] - pts[t_start][1]
            )
            t_start += 1
        return b_end, t_start

    for i, (pts, skey, _st) in enumerate(streams):
        if i == hero_idx:
            continue
        ncut = max(1, int(len(pts) * 0.85))
        b_end, t_start = _split_gap(pts, ncut, joint_gap)
        out += _poly(pts[: b_end + 1], color=black, f=feed)
        tail = pts[t_start:]
        if len(tail) >= 2:
            out += _poly(tail, color=(blue if skey == "b" else pink), f=feed)

    # the OVERSHOOT braid — heavy-ball momentum into the deep sink
    def offset_poly(pts, d):
        n = len(pts)
        res = []
        for i, (px, py) in enumerate(pts):
            ax, ay = pts[max(0, i - 1)]
            bx, by = pts[min(n - 1, i + 1)]
            tx, ty = bx - ax, by - ay
            L = math.hypot(tx, ty) or 1.0
            res.append((px - ty / L * d, py + tx / L * d))
        return res

    if hero_idx >= 0:
        u, v = streams[hero_idx][2]
        vel = [0.0, 0.0]
        path = [(u2px(u), v2py(v))]
        spd = [0.0]
        left = False
        for _ in range(max_steps):
            gx, gy = gradL(u, v)
            vel[0] = momentum * vel[0] - 0.03 * gx
            vel[1] = momentum * vel[1] - 0.03 * gy
            u += vel[0]
            v += vel[1]
            px, py = u2px(u), v2py(v)
            if not keep((px, py)):
                break
            path.append((px, py))
            spd.append(math.hypot(vel[0], vel[1]))
            near = (u - gsink[0]) ** 2 + (v - gsink[1]) ** 2
            if near > 0.09:
                left = True
            if left and near < 0.02 and math.hypot(vel[0], vel[1]) < 0.006:
                break
        smax = max(spd) or 1.0
        # the descent line gets its OWN pen (distinct from the sink circles)
        # when a 5th pen is available; falls back to the basin hue otherwise
        braid_pen = _pen(4, colors) if colors >= 5 else blue
        out += _poly(path, color=braid_pen, f=feed)  # center pass always
        if braid_passes >= 3:
            # companion passes fake thickness for FINE pens only — at 2mm tips
            # they sit inside the tip width and just fight the crowding
            # guardrail (render with braid_passes=1 for acrylics)
            for d in (-0.38, 0.38):  # outer passes only on the fast opening reach
                seg = []
                for i, p in enumerate(path):
                    if spd[i] > 0.4 * smax:
                        seg.append(p)
                    elif len(seg) >= 2:
                        out += _poly(offset_poly(seg, d), color=braid_pen, f=feed)
                        seg = []
                    else:
                        seg = []
                if len(seg) >= 2:
                    out += _poly(offset_poly(seg, d), color=braid_pen, f=feed)

    # the sinks: hierarchy at 3m — CONCENTRIC rings (clean at 2mm tips), not
    # spirals; ``sink_spacing`` tightens the ring pitch independently of the
    # streamline separation (0 → same as fill_spacing)
    ring_pitch = sink_spacing if sink_spacing > 0 else fill_spacing

    def _concentric(cx_, cy_, r_max_, pen_):
        rr = ring_pitch
        cmds: List[GCodeCommand] = []
        while rr <= r_max_ + 1e-9:
            cmds += circle(cx_, cy_, rr, pen=pen_, f=feed)
            rr += ring_pitch
        return cmds

    # both sinks ringed by DOTTED circles in their own hue (feedback ④: blue dots
    # around the deep basin, mirroring the pink dots around the shallow one)
    out += dotted_circle(gpx[0], gpx[1], deep_r + 2.5, pen=blue, bounds=bounds, f=feed)
    out += _concentric(gpx[0], gpx[1], deep_r, blue)
    out += _concentric(spx[0], spx[1], shallow_r, pink)
    out += dotted_circle(spx[0], spx[1], shallow_r + 4, pen=pink, bounds=bounds, f=feed)

    # furniture on a shared left axis — type on its own LEGEND pen (mount 0.5/0.1
    # while the drawing runs 2mm acrylics); falls back to black when colors < 4
    legend = _pen(3, colors) if colors >= 4 else black
    xT = x0 + 0.02 * W
    out += type_block(["WATER", "SHED"], xT, y1 - 6.0, height=3.2, pen=legend, f=feed)
    out += _stroke_text(
        _spaced("EVERY START FINDS THE VALLEY"), xT, y1 - 20.0, 2.0, color=legend, f=feed
    )
    out += swatch_bar(x1 - 9.0, y1 - 4.0, [black, blue, pink], size=2.6, f=feed)
    sad = (u2px((gsink[0] + ssink[0]) / 2), v2py((gsink[1] + ssink[1]) / 2))
    out += plus_mark(sad[0], sad[1], s=1.4, pen=black, f=feed)
    out += scale_footer(bounds, text="DTH = -GRAD L . DT", pen=legend, height=2.4, f=feed)
    return out




def bauhaus_gradient_v1(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    levels: int = 14,
    steps: int = 70,
    lr: float = 0.22,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """RETIRED (kept for version history, deregistered). The original GRADIENT
    DESCENT: a two-bowl loss landscape as thin contour ellipses with a bold pink
    descent path + step dots. Superseded by the WATERSHED rework of
    ``bauhaus_gradient`` — flagged as textbook/schematic by the studio critics."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    out: List[GCodeCommand] = []
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    cx_, cy_ = x0 + 0.54 * W, y0 + 0.5 * H

    m1 = (cx_ - 0.16 * W, cy_ - 0.07 * H)  # global minimum
    m2 = (cx_ + 0.22 * W, cy_ + 0.13 * H)  # shallow second bowl

    def loss(px, py):
        d1 = ((px - m1[0]) / (0.30 * W)) ** 2 + ((py - m1[1]) / (0.26 * H)) ** 2
        d2 = ((px - m2[0]) / (0.20 * W)) ** 2 + ((py - m2[1]) / (0.18 * H)) ** 2
        return min(d1, 0.35 + 0.8 * d2)

    # marching-squares-lite: sample a grid, draw iso segments per cell
    nxg, nyg = 90, 62
    gx = [x0 + 4 + (W - 8) * i / (nxg - 1) for i in range(nxg)]
    gy = [y0 + 8 + (H - 16) * j / (nyg - 1) for j in range(nyg)]
    field = [[loss(px, py) for py in gy] for px in gx]
    vmax = 1.15
    for lv in range(1, levels + 1):
        iso = vmax * (lv / levels) ** 1.4
        for i in range(nxg - 1):
            for j in range(nyg - 1):
                quad = (field[i][j], field[i + 1][j], field[i + 1][j + 1], field[i][j + 1])
                pts_c = []
                corners = [
                    (gx[i], gy[j]),
                    (gx[i + 1], gy[j]),
                    (gx[i + 1], gy[j + 1]),
                    (gx[i], gy[j + 1]),
                ]
                for k in range(4):
                    a_, b_ = quad[k], quad[(k + 1) % 4]
                    if (a_ < iso) != (b_ < iso):
                        t = (iso - a_) / (b_ - a_)
                        pa, pb = corners[k], corners[(k + 1) % 4]
                        pts_c.append((pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t))
                if len(pts_c) >= 2:
                    out += _poly(pts_c[:2], color=black, f=feed)

    # descent path from a seeded start, bold pink with step dots
    px, py = x0 + W * rng.uniform(0.20, 0.30), y0 + H * rng.uniform(0.78, 0.88)
    path = [(px, py)]
    for _ in range(steps):
        e = 1.5
        gx_ = (loss(px + e, py) - loss(px - e, py)) / (2 * e)
        gy_ = (loss(px, py + e) - loss(px, py - e)) / (2 * e)
        px -= lr * W * gx_
        py -= lr * H * gy_
        path.append((px, py))
    for o in (-0.35, 0.0, 0.35):
        out += _poly([(p_[0], p_[1] + o) for p_ in path], color=pink, f=feed)
    for k, (sx, sy) in enumerate(path[:: max(1, steps // 14)]):
        out += fill_disc(sx, sy, 1.0, spacing=0.45, pen=pink, f=feed)
    out += fill_disc(m1[0], m1[1], 3.2, spacing=0.5, pen=blue, f=feed)
    out += dotted_circle(m2[0], m2[1], 6.0, pen=black, bounds=bounds, f=feed)

    out += type_block(["GRADIENT", "DESCENT"], x0 + 5.0, y1 - 6.0, pen=black, f=feed)
    out += swatch_bar(x0 + 5.0, y1 - 22.0, [black, blue, pink], f=feed)
    out += plus_mark(x1 - 9.0, y1 - 9.0, pen=black, f=feed)
    out += scale_footer(bounds, pen=black, f=feed)
    return out




# ---------------------------------------------------------------------------
# FORWARD PASS, rethought — the weight matrix as an Anni-Albers weave draft.
# A network layer IS a grid of connections = a loom. Warp (blue) = inputs,
# weft (pink) = outputs; at each crossing the thread on TOP is set by the real
# weight's SIGN, its FLOAT length by magnitude. Not a wiring diagram — a textile
# that happens to be the exact matrix.
# ---------------------------------------------------------------------------


def bauhaus_loom(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    weights: str = "",
    block: int = 0,
    n_warp: int = 52,
    n_weft: int = 34,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """FORWARD PASS as weaving: a real weight matrix woven as warp/weft threads,
    over/under by sign, float by magnitude. Bauhaus by lineage (the weaving
    workshop), true by construction (it is the matrix), lines by nature."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    Wm = None
    if weights:
        try:
            Wm = _load_qkv(weights, block)[0]  # query matrix
        except Exception:
            Wm = None
    if Wm is None:
        Wm = np.array([[rng.random() * 2 - 1 for _ in range(96)] for _ in range(96)])

    # block-mean downsample to n_warp x n_weft, keep sign + magnitude
    R0, C0 = Wm.shape
    br, bc = max(1, R0 // n_warp), max(1, C0 // n_weft)
    M = np.zeros((n_warp, n_weft))
    for i in range(n_warp):
        for j in range(n_weft):
            blk = Wm[i * br : (i + 1) * br, j * bc : (j + 1) * bc]
            if blk.size:
                M[i, j] = math.copysign(float(np.abs(blk).mean()), float(blk.mean()))
    # sort warp rows + weft cols by mean weight so same-sign regions CLUSTER —
    # a legitimate neuron reorder (permutation-invariant), revealing the block/
    # diagonal structure a trained matrix hides in arbitrary index order.
    ri = sorted(range(n_warp), key=lambda i: float(M[i].mean()))
    ci = sorted(range(n_weft), key=lambda j: float(M[:, j].mean()))
    M = M[np.ix_(ri, ci)]
    norm = float(np.percentile(np.abs(M), 92)) or 1.0

    # the tapestry fills the page (dominant mass); title band above, footer below
    mx0, mx1 = x0 + 6, x1 - 6
    my0, my1 = y0 + 16, y1 - 20
    dx = (mx1 - mx0) / (n_warp - 1)
    dy = (my1 - my0) / (n_weft - 1)
    gap = min(dx, dy) * 0.34  # the interlace gap: the under-thread ducks here

    def strong(w):
        return abs(w) / norm > 0.85  # heaviest floats get a second pass (sheen)

    # WARP threads (vertical, blue) — broken where the warp dips UNDER (w < 0)
    for i in range(n_warp):
        xi = mx0 + i * dx
        cuts = []
        for j in range(n_weft):
            if M[i, j] < 0:  # weft on top here -> warp ducks under
                yj = my0 + j * dy
                cuts.append((yj - gap, yj + gap))
        yptr = my0
        segs = []
        for a, b in cuts:
            if a > yptr:
                segs.append((yptr, a))
            yptr = max(yptr, b)
        if yptr < my1:
            segs.append((yptr, my1))
        for a, b in segs:
            out += _poly([(xi, a), (xi, b)], color=blue, f=feed)

    # WEFT threads (horizontal, pink) — broken where the weft dips UNDER (w >= 0)
    for j in range(n_weft):
        yj = my0 + j * dy
        cuts = []
        for i in range(n_warp):
            if M[i, j] >= 0:  # warp on top -> weft ducks under
                xi = mx0 + i * dx
                cuts.append((xi - gap, xi + gap))
        xptr = mx0
        segs = []
        for a, b in cuts:
            if a > xptr:
                segs.append((xptr, a))
            xptr = max(xptr, b)
        if xptr < mx1:
            segs.append((xptr, mx1))
        for a, b in segs:
            out += _poly([(a, yj), (b, yj)], color=pink, f=feed)
            if b - a > dx * 2.4:  # a long float catches the light -> doubled
                out += _poly([(a, yj + 0.25), (b, yj + 0.25)], color=pink, f=feed)

    # black selvage: the woven edge, framing the cloth (the only closed rects)
    out += _poly(
        [
            (mx0 - 2, my0 - 2),
            (mx1 + 2, my0 - 2),
            (mx1 + 2, my1 + 2),
            (mx0 - 2, my1 + 2),
            (mx0 - 2, my0 - 2),
        ],
        color=black,
        f=feed,
    )

    # type: title top-left over the cloth's head, spec footer
    out += type_block(["FORWARD PASS"], x0 + 4, y1 - 4, height=3.0, pen=black, f=feed)
    out += _stroke_text(_spaced("THE WEIGHTS, WOVEN"), x0 + 4, y1 - 11, 2.2, color=black, f=feed)
    out += swatch_bar(x1 - 8, y1 - 4, [black, blue, pink], size=1.8, f=feed)
    out += scale_footer(
        bounds, text="LAYER Q  52x34  WARP=IN WEFT=OUT", pen=black, height=2.2, f=feed
    )
    return out




# ---------------------------------------------------------------------------
# piece 08 — DECISION SURFACE (the network as its function, not its wiring)
# ---------------------------------------------------------------------------


def bauhaus_decision(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    weights: str = "",
    block: int = 0,
    hidden: int = 6,
    n_points: int = 120,
    margin: float = 0.22,
    boundary_passes: int = 3,
    grid: int = 140,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """DECISION SURFACE — a neural network drawn as its decision FUNCTION, not
    its wiring. A small readout f(u,v)=Σ aᵢ·tanh(Wᵢ·[u,v]+bᵢ) scores the input
    plane; the bold black knife is the EXACT iso-0 contour (marching squares),
    flanked by ±margin shoulders and the hidden-unit hyperplane creases the cut
    visibly kinks on (the fingerprint of composition — no neuron drawn). Every
    dot is coloured by the TRUE sign of f: blue = class +1, pink = class −1.
    Trained query directions drive the readout when a checkpoint is given."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    # bands: title on top, field in the middle, footer below → the corner→corner
    # cut lives in the field and never fights the type.
    title_h, foot_h = 24.0, 12.0
    fx0, fx1 = x0 + 6.0, x1 - 6.0
    fy0, fy1 = y0 + foot_h, y1 - title_h
    fw, fh = fx1 - fx0, fy1 - fy0
    keep = _rect_keep((fx0, fy0, fx1, fy1))

    def px2u(px: float) -> float:
        return (px - fx0) / fw * 2.0 - 1.0

    def py2v(py: float) -> float:
        return (py - fy0) / fh * 2.0 - 1.0

    def u2px(u: float) -> float:
        return fx0 + (u + 1.0) / 2.0 * fw

    def v2py(v: float) -> float:
        return fy0 + (v + 1.0) / 2.0 * fh

    # ---- the readout f(u,v) = Σ aᵢ tanh(Wᵢ·[u,v] + bᵢ) --------------------
    Wq = None
    if weights:
        try:
            Wq = _load_qkv(weights, block)[0]  # trained query matrix (~96×96)
        except Exception:
            Wq = None

    def build_field(attempt: int):
        """Return (W1, b1, a). Real path rotates which trained columns feed the
        2D readout; fallback re-draws seeded gaussians at a shrinking scale."""
        if Wq is not None:
            C = Wq.shape[1]
            c = (attempt * 2) % max(1, C - 3)
            W1 = np.array(Wq[:hidden, c : c + 2], dtype=float)
            b1 = np.array([float(Wq[i, (c + 2) % C]) for i in range(hidden)])
            a = np.array(
                [
                    float(np.linalg.norm(Wq[i, :hidden]))
                    * (1.0 if float(Wq[i].mean()) >= 0 else -1.0)
                    for i in range(hidden)
                ]
            )
        else:
            sc = 1.6 * (0.82**attempt)
            W1 = np.array([[rng.gauss(0, sc) for _ in range(2)] for _ in range(hidden)])
            b1 = np.array([rng.gauss(0, 0.55) for _ in range(hidden)])
            a = np.array([rng.gauss(0, 1.0) for _ in range(hidden)])
        # normalise input scale so tanh isn't saturated flat
        s = float(np.abs(W1).mean()) or 1.0
        W1 = W1 / s * 1.7
        return W1, b1, a

    def eval_grid(W1, b1, a, us, vs):
        U, V = np.meshgrid(us, vs)  # (ny, nx) → F[j][i], j indexes vs/ys
        F = np.zeros_like(U)
        for i in range(hidden):
            F += a[i] * np.tanh(W1[i, 0] * U + W1[i, 1] * V + b1[i])
        return F

    def chains_at(F_list, xs, ys, iso, minlen=6):
        segs = _marching_squares(F_list, xs, ys, iso)
        return [c for c in _chain_segments(segs) if len(c) >= minlen]

    def span(ch):
        xs_ = [p[0] for p in ch]
        ys_ = [p[1] for p in ch]
        return math.hypot(max(xs_) - min(xs_), max(ys_) - min(ys_))

    # ---- boundary-quality gate: pick the cleanest single folded knife -------
    cxs = [fx0 + i * (fw / 44) for i in range(45)]
    cys = [fy0 + j * (fh / 44) for j in range(45)]
    cus = np.array([px2u(x) for x in cxs])
    cvs = np.array([py2v(y) for y in cys])
    best = None
    for attempt in range(8):
        W1, b1, a = build_field(attempt)
        Fc = eval_grid(W1, b1, a, cus, cvs).tolist()
        chs = chains_at(Fc, cxs, cys, 0.0)
        if not chs:
            continue
        dom = max(chs, key=span)

        def diag_score(ch):
            xs_ = [p[0] for p in ch]
            ys_ = [p[1] for p in ch]
            dx, dy = max(xs_) - min(xs_), max(ys_) - min(ys_)
            aspect = min(dx, dy) / (max(dx, dy) + 1e-9)  # 1 → true diagonal
            return span(ch) * (0.35 + 0.65 * aspect)

        # fewest components, then the longest chain that best spans the diagonal
        score = (len(chs), -diag_score(dom))
        if best is None or score < best[0]:
            best = (score, (W1, b1, a))
    if best is None:
        W1, b1, a = build_field(0)
    else:
        W1, b1, a = best[1]

    # ---- fine field, reused for boundary + both margins --------------------
    xs = [fx0 + i * (fw / grid) for i in range(grid + 1)]
    ys = [fy0 + j * (fh / grid) for j in range(grid + 1)]
    us = np.array([px2u(x) for x in xs])
    vs = np.array([py2v(y) for y in ys])
    Fnp = eval_grid(W1, b1, a, us, vs)
    # normalise field magnitude so `margin` is a consistent fraction of the
    # range whatever the weight source (the iso-0 cut is scale-invariant, so
    # only the shoulders + point classification depend on this).
    fscale = float(np.percentile(np.abs(Fnp), 88)) or 1.0
    a = a / fscale
    F_list = (Fnp / fscale).tolist()

    def offset_poly(pts, d):
        n = len(pts)
        res = []
        for i, (px, py) in enumerate(pts):
            ax, ay = pts[max(0, i - 1)]
            bx, by = pts[min(n - 1, i + 1)]
            tx, ty = bx - ax, by - ay
            L = math.hypot(tx, ty) or 1.0
            res.append((px - ty / L * d, py + tx / L * d))
        return res

    # ---- MARGIN SHOULDERS first (thin, so the knife overprints them) -------
    for iso in (margin, -margin):
        for ch in chains_at(F_list, xs, ys, iso):
            for r in _clip_runs([ch], keep):
                out += _poly(r, color=black, f=feed)

    # ---- THE DECISION CUT: iso-0, the hero. The curve is already piecewise-
    # bent (a NETWORK's boundary, not one perceptron's straight line); drawn as
    # a solid multi-line knife. Secondary components stay a single quiet stroke.
    b_chains = sorted(chains_at(F_list, xs, ys, 0.0), key=span, reverse=True)
    for ci, ch in enumerate(b_chains):
        for r in _clip_runs([ch], keep):
            if len(r) < 2:
                continue
            offs = [-0.5, -0.25, 0.0, 0.25, 0.5] if ci == 0 else [0.0]
            for d in offs:
                out += _poly(offset_poly(r, d) if d else r, color=black, f=feed)

    # ---- POINT CLOUDS labelled by the true sign of f ----------------------
    def fval(u, v):
        return sum(
            float(a[i]) * math.tanh(float(W1[i, 0]) * u + float(W1[i, 1]) * v + float(b1[i]))
            for i in range(hidden)
        )

    def dot(cx, cy, r, pen):
        turns = max(1, int(r / 0.55))
        n = max(10, int(r * 16))
        pts = []
        for k in range(n + 1):
            t = k / n
            ang = 2 * math.pi * turns * t
            pts.append((cx + r * t * math.cos(ang), cy + r * t * math.sin(ang)))
        return _poly(pts, color=pen, f=feed)

    # 1:2 blue:pink mass — pink is the dense, loud field. A CLEAR corridor
    # (|f|<0.7·margin) hugs the cut; a few big "support vector" discs sit on the
    # shoulders (0.7·margin ≤ |f| < 1.5·margin); the rest is the small field.
    n_blue = n_points // 3
    n_pink = n_points - n_blue
    want = {"b": n_blue, "p": n_pink}
    got = {"b": [], "p": []}
    sup = {"b": 0, "p": 0}
    SUPMAX = 5
    typebox = lambda px, py: px < fx0 + 0.30 * fw and py > fy1 - 0.14 * fh
    tries = 0
    while (len(got["b"]) < n_blue or len(got["p"]) < n_pink) and tries < 12000:
        tries += 1
        px = rng.uniform(fx0 + 2, fx1 - 2)
        py = rng.uniform(fy0 + 2, fy1 - 2)
        if typebox(px, py):
            continue
        val = fval(px2u(px), py2v(py))
        key = "b" if val >= 0 else "p"
        if len(got[key]) >= want[key]:
            continue
        av = abs(val)
        if av < 0.7 * margin:  # the spine corridor stays a clean void
            continue
        if av < 1.5 * margin:  # support shoulder — a few big discs only
            if sup[key] >= SUPMAX:
                continue
            sup[key] += 1
            got[key].append((px, py, True))
        else:
            got[key].append((px, py, False))
    for px, py, is_sup in got["b"]:
        out += dot(px, py, 2.1 if is_sup else 1.0, blue)
    for px, py, is_sup in got["p"]:
        out += dot(px, py, 2.1 if is_sup else 1.0, pink)

    # ---- FURNITURE on a shared left axis ----------------------------------
    xT = x0 + 0.02 * W
    out += type_block(["DECISION", "SURFACE"], xT, y1 - 5.0, height=3.2, pen=black, f=feed)
    out += _stroke_text(
        _spaced("THE CUT THROUGH INPUT SPACE"), xT, y1 - 19.0, 2.0, color=black, f=feed
    )
    out += swatch_bar(x1 - 9.0, y1 - 4.0, [black, blue, pink], size=2.6, f=feed)
    out += plus_mark(fx1 - 0.16 * fw, fy0 + 0.12 * fh, s=1.4, pen=black, f=feed)
    out += scale_footer(bounds, text="F(X)=SIGN(W.X+B)", pen=black, height=2.4, f=feed)
    return out




# ---------------------------------------------------------------------------
# piece 10 — THE LONG NOW (LSTM cell state as one modulated memory band)
# ---------------------------------------------------------------------------


def bauhaus_conveyor(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    weights: str = "",
    block: int = 0,
    steps: int = 64,
    forget_events: int = 2,
    write_events: int = 4,
    band_max_frac: float = 0.20,
    full_pitch: float = 0.9,
    void_pitch: float = 5.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """THE LONG NOW — an LSTM's memory carried through time. The exact cell
    update cₜ = fₜ·cₜ₋₁ + iₜ·gₜ runs across `steps`; the black conveyor band's
    thickness AND ink density are |cₜ| (dense = strong memory, near-void where it
    decays). Forget gates pinch the band to a thread; pink write-stitches inject
    new information into one selvage; a thin blue ghost shows the prior value
    being overwritten. Time is the horizontal axis."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    dt = (0.78 * W) / steps
    A = band_max_frac * H
    yb = y0 + 0.46 * H
    xL = x0 + 0.20 * W

    # gate schedule — the fallback runs the SAME true recurrence as a real ckpt
    f = [0.80 + 0.19 * rng.fbm(t * 0.11, 7.3) for t in range(steps)]
    ig = [(0.15 + 0.10 * rng.fbm(t * 0.09, 2.1)) * (2.0 * rng.fbm(t * 0.07, 9.9) - 1.0) for t in range(steps)]

    def scatter(nev):
        idx = []
        for k in range(nev):
            base = (k + 1) / (nev + 1)
            idx.append(int(min(steps - 2, max(1, (base + rng.uniform(-0.05, 0.05)) * steps))))
        return sorted(set(idx))

    forgets = scatter(forget_events)
    writes = scatter(write_events)
    for t in forgets:
        f[t] = 0.06  # a scripted pinch-to-thread
    deepest = forgets[len(forgets) // 2] if forgets else 0
    for w in writes:
        ig[w] = rng.choice([-1, 1]) * 0.9  # a strong signed injection
    # the write just after the deepest forget is the loudest (cause & effect)
    after = min([w for w in writes if w > deepest], default=None)
    if after is not None:
        ig[after] = math.copysign(1.15, ig[after])

    c = 0.0
    c_now, c_prev = [], []
    for t in range(steps):
        c_prev.append(c)
        c = f[t] * c + ig[t]
        c_now.append(c)
    cmax = max(1e-6, max(abs(v) for v in c_now))
    h = [max(0.6, A * abs(v) / cmax) for v in c_now]

    xc = [xL + (t + 0.5) * dt for t in range(steps)]

    # body — aligned horizontal striations clipped to the tube envelope: the
    # number of lines at each column IS |cₜ|, so the ribbon swells with memory
    # and collapses toward the baseline through a forget (density = tone).
    nlev = int(A / full_pitch) + 1
    for k in range(nlev + 1):
        off = k * full_pitch
        if off > A + 1e-6:
            break
        for sgn in ((1, -1) if k > 0 else (1,)):
            run: List[Tuple[float, float]] = []
            for t in range(steps):
                if h[t] >= off:
                    run.append((xc[t], yb + sgn * off))
                elif len(run) >= 2:
                    out += _poly(run, color=black, f=feed)
                    run = []
                else:
                    run = []
            if len(run) >= 2:
                out += _poly(run, color=black, f=feed)

    # smooth tube selvages (the rounded memory ribbon) + through-baseline
    out += _poly([(xc[t], yb + h[t]) for t in range(steps)], color=black, f=feed)
    out += _poly([(xc[t], yb - h[t]) for t in range(steps)], color=black, f=feed)
    out += _poly([(xL, yb), (xc[-1], yb)], color=black, f=feed)

    # blue prior-memory ghost in a clear lane below the band
    yg = yb - A - 4.0
    out += _poly([(xc[t], yg - A * 0.35 * abs(c_prev[t]) / cmax) for t in range(steps)], color=blue, f=feed)

    # pink write-stitches into one selvage (sign of c picks top/bottom)
    for w in writes:
        top = c_now[w] >= 0
        y_from = yb + h[w] if top else yb - h[w]
        length = min(0.9 * h[w], A * abs(ig[w]) / cmax * 1.4)
        length *= 1.3 if w == after else 1.0
        y_to = y_from - length if top else y_from + length
        out += _poly([(xc[w], y_from), (xc[w], y_to)], color=pink, f=feed)

    # forget anchor — the singularity of forgetting, on the baseline
    out += plus_mark(xc[deepest], yb, s=1.4, pen=black, f=feed)

    xT = x0 + 0.02 * W
    out += type_block(["THE LONG", "NOW"], xT, yb + 0.24 * H, height=3.2, pen=black, f=feed)
    out += _stroke_text(_spaced("FORGET . WRITE . CARRY"), xT, yb + 0.10 * H, 2.0, color=black, f=feed)
    out += swatch_bar(xT, yb - 0.02 * H, [black, blue, pink], size=2.6, f=feed)
    real = bool(weights)
    out += scale_footer(
        bounds,
        text=("GATES REAL RECURRENCE EXACT" if real else "GATES SYNTHETIC RECURRENCE EXACT"),
        pen=black,
        height=2.2,
        f=feed,
    )
    return out




# ---------------------------------------------------------------------------
# piece 11 — SETTLING (the perceptron boundary as a rotating sweep of errors)
# ---------------------------------------------------------------------------


def bauhaus_settling(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    weights: str = "",
    block: int = 0,
    n_points: int = 90,
    margin_gap: float = 0.14,
    eta: float = 1.0,
    max_epochs: int = 40,
    ghost_lines: int = 16,
    final_passes: int = 3,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """SETTLING — a perceptron's decision boundary drawn as MOTION: the line
    that its own errors pushed into place. Real online Rosenblatt updates on a
    seeded separable cloud leave a fan of successive boundary positions (black,
    ghosting from wild to settled); the converged cut is the loud pink knife; the
    2-3 misclassified points that rotated the boundary most are the scarce large
    discs — the CAUSE of the cut. Time here is the learning."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, pink, black = _pen(BLUE, colors), _pen(PINK, colors), _pen(BLACK, colors)
    out: List[GCodeCommand] = []

    fx0, fy0, fx1, fy1 = x0 + 0.24 * W, y0 + 8, x1 - 6, y1 - 8
    fw, fh = fx1 - fx0, fy1 - fy0
    fieldkeep = _rect_keep((fx0, fy0, fx1, fy1))

    def dx2px(x):
        return fx0 + (x + 1) / 2 * fw

    def dy2py(y):
        return fy0 + (y + 1) / 2 * fh

    def make_data(phi, theta):
        ws = (math.cos(phi), math.sin(phi))
        pts, lab = [], []
        tries = 0
        while len(pts) < n_points and tries < n_points * 25:
            tries += 1
            x = (rng.uniform(-1, 1), rng.uniform(-1, 1))
            s = ws[0] * x[0] + ws[1] * x[1] - theta
            if abs(s) < margin_gap:
                continue
            pts.append(x)
            lab.append(1 if s > 0 else -1)
        return pts, lab

    def train(pts, lab):
        w = [0.0, 0.0]
        b = 0.0
        hist = []
        for _ in range(max_epochs):
            updated = False
            for x, y in zip(pts, lab):
                if (1 if (w[0] * x[0] + w[1] * x[1] + b) > 0 else -1) != y:
                    w[0] += eta * y * x[0]
                    w[1] += eta * y * x[1]
                    b += eta * y
                    hist.append((w[0], w[1], b, x, y))
                    updated = True
            if not updated:
                break
        return w, b, hist

    # resample until the trajectory is long enough to read as a sweep
    best = None
    for _ in range(20):
        phi = rng.uniform(0.35, 0.75) * math.pi
        theta = rng.uniform(-0.15, 0.15)
        pts, lab = make_data(phi, theta)
        w, b, hist = train(pts, lab)
        if best is None or len(hist) > len(best[4]):
            best = (pts, lab, w, b, hist)
        if len(hist) >= ghost_lines:
            break
    pts, lab, wf, bf, hist = best

    def boundary_seg(wx, wy, bb):
        n2 = wx * wx + wy * wy
        if n2 < 1e-9:
            return [(fx0, fy0), (fx0, fy0)]
        ox, oy = -bb * wx / n2, -bb * wy / n2
        dx, dy = -wy, wx
        dl = math.hypot(dx, dy) or 1.0
        dx, dy = dx / dl, dy / dl
        L, N = 4.0, 48  # densify so _clip_runs keeps the in-rect portion
        p0 = (ox - L * dx, oy - L * dy)
        p1 = (ox + L * dx, oy + L * dy)
        return [
            (dx2px(p0[0] + (p1[0] - p0[0]) * t / N), dy2py(p0[1] + (p1[1] - p0[1]) * t / N))
            for t in range(N + 1)
        ]

    def offset_poly(p, d):
        n = len(p)
        res = []
        for i, (px, py) in enumerate(p):
            ax, ay = p[max(0, i - 1)]
            bx, by = p[min(n - 1, i + 1)]
            tx, ty = bx - ax, by - ay
            ln = math.hypot(tx, ty) or 1.0
            res.append((px - ty / ln * d, py + tx / ln * d))
        return res

    # thinned scatter — quiet context so the sweep dominates
    keepn = max(10, int(0.6 * len(pts)))
    for (x, y) in list(zip(pts, lab))[:keepn]:
        px, py = dx2px(x[0]), dy2py(x[1])
        if y > 0:
            out += fill_disc(px, py, 0.8, spacing=0.5, pen=blue, f=feed)
        else:
            out += circle(px, py, 0.9, pen=pink, f=feed)

    # the fan of past-guess boundaries — subsample by EVEN ANGLE of the normal
    # so it reads as one clean rotating sweep (a fan closing), not random sticks.
    ang_all = [math.atan2(h[1], h[0]) for h in hist]
    order = sorted(range(len(hist)), key=lambda i: ang_all[i])
    if len(order) <= ghost_lines:
        sel = order
    else:
        sel = [order[int(round(k * (len(order) - 1) / (ghost_lines - 1)))] for k in range(ghost_lines)]
    final_ang = math.atan2(wf[1], wf[0])
    for si in sel:
        wx, wy, bb, _, _ = hist[si]
        near = abs(math.atan2(math.sin(ang_all[si] - final_ang), math.cos(ang_all[si] - final_ang)))
        for r in _clip_runs([boundary_seg(wx, wy, bb)], fieldkeep):
            out += _poly(r, color=black, f=feed)
            if near < 0.12:  # the ghosts nearest the settled angle gain weight
                out += _poly(offset_poly(r, 0.3), color=black, f=feed)

    # the hero: the converged cut, a bold pink knife that dominates at 3m
    for r in _clip_runs([boundary_seg(wf[0], wf[1], bf)], fieldkeep):
        for d in (-0.7, -0.42, -0.14, 0.14, 0.42, 0.7):
            out += _poly(offset_poly(r, d), color=pink, f=feed)

    # the scarce accent — the culprit points that rotated the boundary most
    def angdiff(a, b):
        return math.atan2(math.sin(a - b), math.cos(a - b))

    angs = [math.atan2(h[1], h[0]) for h in hist]
    rot = [0.0] + [abs(angdiff(angs[i], angs[i - 1])) for i in range(1, len(hist))]
    top = sorted(range(len(hist)), key=lambda i: -rot[i])[:3]
    for i in top:
        _, _, _, cx, cy = hist[i]
        px, py = dx2px(cx[0]), dy2py(cx[1])
        _, _, _, _, yv = hist[i]
        out += fill_disc(px, py, 2.2, spacing=0.5, pen=(blue if yv > 0 else pink), f=feed)
        out += circle(px, py, 3.0, pen=black, f=feed)
    if top:
        _, _, _, c0, _ = hist[top[0]]
        out += plus_mark(dx2px(c0[0]), dy2py(c0[1]), s=1.2, pen=black, f=feed)

    xT = x0 + 0.02 * W
    out += type_block(["SETTLING"], xT, y1 - 6.0, height=3.2, pen=black, f=feed)
    out += _stroke_text(_spaced("THE LINE THAT ERRORS BUILT"), xT, y1 - 20.0, 2.0, color=black, f=feed)
    out += swatch_bar(xT, y1 - 26.0, [black, blue, pink], size=3.0, f=feed)
    out += scale_footer(bounds, text=f"W += Y X   {len(hist)} UPDATES", pen=black, height=2.4, f=feed)
    return out




# ---------------------------------------------------------------------------
# piece 12 — RELEVANCE TERRAIN (transformer Q·K score field as a sheared relief)
# ---------------------------------------------------------------------------


def bauhaus_relevance_v1(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
    nu: int = 48,
    nv: int = 48,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """ATTENTION AS TOPOGRAPHY — a transformer's attention as a vertical stack of
    5 hidden-line terrain stages (from-scratch 3D pen-plotter engine): the CANVAS
    GRID where Q (red, from the left) and K (blue, from above) meet; QKᵀ where
    their landscapes MERGE into raw similarity cones (red = query side, blue = key
    side); SOFTMAX as smooth probability contours; V the semantic terrain (green);
    OUTPUT = V pulled upward by attention. Colour-coded blue/red/green/black; best
    plotted with 4 pens. Droplines tie the query·key anchors through every stage."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, red, green, blk = 0, 1, 2, 3  # render with dodgerblue/crimson/forestgreen/black
    out: List[GCodeCommand] = []

    cx = x0 + 0.52 * W
    SXX, SXZ = 0.30 * W, 0.16 * W
    SYX, SYZ, SYY = 0.055 * H, -0.065 * H, 0.085 * H

    def proj(wx, wy, wz, cyL):
        return (cx + wx * SXX + wz * SXZ, cyL + wx * SYX + wz * SYZ - wy * SYY)

    def dep(wx, wy, wz):
        return -wz + 0.05 * wy

    peaks = [(-0.52, 0.14, 1.0), (0.03, -0.22, 0.80), (0.52, 0.30, 0.92)]

    def f_qkt(wx, wz):
        z = 0.06 * (rng.fbm(wx * 7.0 + 3.1, wz * 7.0 + 6.7) - 0.5) * 2
        for px, py, a in peaks:
            z += 1.5 * a * math.exp(-((wx - px) ** 2 + (wz - py) ** 2) / (2 * 0.028))
        return z

    def f_smooth(wx, wz):
        z = 0.0
        for px, py, a in peaks:
            z += a * math.exp(-((wx - px) ** 2 + (wz - py) ** 2) / (2 * 0.16))
        return z

    def f_v(wx, wz):
        return 0.42 * (math.sin(2.2 * wx + 0.4) * math.cos(1.9 * wz) + 0.5 * math.sin(3.0 * wz + 1.1))

    def f_out(wx, wz):
        z = f_v(wx, wz)
        for px, py, a in peaks:
            z += 1.3 * a * math.exp(-((wx - px) ** 2 + (wz - py) ** 2) / (2 * 0.028))
        return z

    cy_top, cy_bot = y1 - 0.16 * H, y0 + 0.17 * H
    step = (cy_top - cy_bot) / 4.0
    cyL = [cy_top - k * step for k in range(5)]

    # ---- z-buffered terrain (self hidden-line) with optional per-vertex colour
    def render_terrain(cyc, hfun, hscale, pen=blk, penfn=None):
        SX = np.zeros((nu + 1, nv + 1))
        SY = np.zeros((nu + 1, nv + 1))
        DE = np.zeros((nu + 1, nv + 1))
        PV = np.full((nu + 1, nv + 1), pen)
        for i in range(nu + 1):
            wx = -1 + 2 * i / nu
            for j in range(nv + 1):
                wz = -1 + 2 * j / nv
                wy = hfun(wx, wz) * hscale
                p = proj(wx, wy, wz, cyc)
                SX[i, j], SY[i, j], DE[i, j] = p[0], p[1], dep(wx, wy, wz)
                if penfn is not None:
                    PV[i, j] = penfn(wx, wz)
        _zbuf_terrain(out, SX, SY, DE, feed=feed, PENV=PV)

    def near_anchor(wx, wz, r=0.24):
        for k, (px, py, _a) in enumerate(peaks):
            if math.hypot(wx - px, wz - py) < r:
                return k
        return -1

    # ---- 1. CANVAS GRID (flat) + Q (red, left) & K (blue, top) arrows ----
    c0 = cyL[0]
    gc = 16
    for i in range(gc + 1):
        wx = -1 + 2 * i / gc
        out += _poly([proj(wx, 0, -1 + 2 * j / gc, c0) for j in range(gc + 1)], color=blk, f=feed)
    for j in range(gc + 1):
        wz = -1 + 2 * j / gc
        out += _poly([proj(-1 + 2 * i / gc, 0, wz, c0) for i in range(gc + 1)], color=blk, f=feed)
    uxm = math.hypot(SXX, SYX)
    uxx, uxy = SXX / uxm, SYX / uxm
    uym = math.hypot(SXZ, SYZ)
    uyx, uyy = SXZ / uym, SYZ / uym

    def arrow(e, dx, dy, pen, ln=20.0):
        s = (e[0] - ln * dx, e[1] - ln * dy)
        out.extend(_poly([s, e], color=pen, f=feed))
        px, py = -dy, dx
        out.extend(_poly([(e[0] - 4 * dx + 1.5 * px, e[1] - 4 * dy + 1.5 * py), e,
                          (e[0] - 4 * dx - 1.5 * px, e[1] - 4 * dy - 1.5 * py)], color=pen, f=feed))

    for t in range(5):
        wz = -0.8 + 1.6 * t / 4
        e = proj(-1, 0, wz, c0)
        arrow((e[0] - 3 * uxx, e[1] - 3 * uxy), uxx, uxy, red)
    for t in range(6):
        wx = -0.8 + 1.6 * t / 5
        e = proj(wx, 0, 1, c0)
        arrow((e[0] + 3 * uyx, e[1] + 3 * uyy), -uyx, -uyy, blue)
    out += _stroke_text(_spaced("Q QUERIES"), proj(-1, 0, -0.9, c0)[0] - 26, c0 + 0.10 * H, 1.7, color=red, f=feed)
    out += _stroke_text(_spaced("K KEYS"), proj(0, 0, 1, c0)[0] + 4, c0 + 0.14 * H, 1.7, color=blue, f=feed)

    # ---- 2. QKT — Q(red) & K(blue) landscapes MERGE into similarity cones --
    def qk_pen(wx, wz):
        k = near_anchor(wx, wz, 0.26)
        if k < 0:
            return blk
        return red if k % 2 == 0 else blue  # query-side red, key-side blue

    render_terrain(cyL[1], f_qkt, 0.9, pen=blk, penfn=qk_pen)

    # ---- 3. SOFTMAX probability contours ---------------------------------
    c2 = cyL[2]
    gN = 90
    xs = [-1 + 2 * i / gN for i in range(gN + 1)]
    ys = [-1 + 2 * j / gN for j in range(gN + 1)]
    F = [[f_smooth(xs[i], ys[j]) for i in range(gN + 1)] for j in range(gN + 1)]
    fmax = max(max(r) for r in F)
    for lv in range(1, 11):
        iso = fmax * lv / 11.0
        for ch in _chain_segments(_marching_squares(F, xs, ys, iso)):
            if len(ch) < 4:
                continue
            out += _poly([proj(wx, iso * 0.6, wz, c2) for (wx, wz) in ch], color=blk, f=feed)

    # ---- 4. V — the semantic terrain (green) -----------------------------
    render_terrain(cyL[3], f_v, 0.9, pen=green)

    # ---- 5. OUTPUT — V pulled up by attention (peaks tinted) -------------
    def o_pen(wx, wz):
        return green if near_anchor(wx, wz, 0.20) >= 0 else blk

    render_terrain(cyL[4], f_out, 0.62, pen=blk, penfn=o_pen)

    # ---- droplines tying the 3 anchors through every stage --------------
    for px, py, _a in peaks:
        sx = cx + px * SXX + py * SXZ
        yt = proj(px, 0, py, cyL[0])[1]
        yb = proj(px, f_out(px, py) * 0.62, py, cyL[4])[1]
        yv, ye = min(yt, yb), max(yt, yb)
        k = 0
        while yv < ye:
            if k % 2 == 0:
                out += _poly([(sx, yv), (sx, min(ye, yv + 3.0))], color=blk, f=feed)
            yv += 5.0
            k += 1

    # ---- numbered stages (left) + stage labels (right) ------------------
    xL = x0 + 0.015 * W
    stages = [
        ("1", "THE CANVAS GRID", "Q AND K MEET", blk),
        ("2", "THE INTERSECTION", "S = QK T", red),
        ("3", "SOFTMAX", "A = SOFTMAX S", blk),
        ("4", "VALUES V", "SEMANTIC TERRAIN", green),
        ("5", "OUTPUT", "O = A V", blk),
    ]
    for k, (num, title, rlab, rc) in enumerate(stages):
        out += _stroke_text(num, xL, cyL[k] + 4, 3.0, color=blk, f=feed)
        out += _stroke_text(_spaced(title), xL + 6, cyL[k] + 4, 1.9, color=blk, f=feed)
        out += _stroke_text(_spaced(rlab), x1 - 0.16 * W, cyL[k], 1.7, color=rc, f=feed)

    out += type_block(["ATTENTION AS"], xL, y1 - 5.0, height=3.4, pen=blk, underline=False, f=feed)
    out += _stroke_text(_spaced("TOPOGRAPHY"), xL, y1 - 12.0, 3.0, color=blk, f=feed)
    out += _stroke_text(_spaced("QUERIES SHAPE CONTENT THROUGH CONTEXT"), xL, y1 - 18.0, 1.7, color=blk, f=feed)
    return out




# ---------------------------------------------------------------------------
# piece 13 — MEMORY IN TIME (LSTM as a vertical figure-8 of information loops)
# ---------------------------------------------------------------------------


def bauhaus_memory_v1(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    loops: int = 40,
    half: int = 130,
    precess: float = 0.5,
    grow: float = 1.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """MEMORY IN TIME — an LSTM as a figure-8 of PRECESSING loops. The recurrence
    loops back every step (REMEMBER c_t above, FORGET c_{t-1} below, meeting at the
    hollow carried-state waist), but each iteration lands slightly ROTATED by the
    transformation it underwent — a helix / logarithmic spiral of nested loops,
    not one static 8. Gate leaders mark the input/forget/output gates. Black + red."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)  # PINK slot rendered crimson
    out: List[GCodeCommand] = []

    cx, cyw = x0 + 0.48 * W, y0 + 0.50 * H
    ru, rl, wx = 0.135 * H, 0.175 * H, 1.55  # top REMEMBER lobe, bigger FORGET lobe

    def rot(px, py, ph):
        c, s = math.cos(ph), math.sin(ph)
        return (px * c - py * s, px * s + py * c)

    # faint background orbits (the iterations echoing) + a light starfield
    for e in range(3):
        ea, eb = (0.34 + 0.05 * e) * W, (0.40 + 0.05 * e) * H
        erot = rng.uniform(-0.3, 0.3)
        seg = []
        for k in range(241):
            a = 2 * math.pi * k / 240
            ox, oy = rot(ea * 0.5 * math.cos(a), eb * 0.5 * math.sin(a), erot)
            if k % 6 < 3:
                seg.append((cx + ox, cyw + oy))
            elif len(seg) >= 2:
                out += _poly(seg, color=black, f=feed)
                seg = []
            else:
                seg = []
        if len(seg) >= 2:
            out += _poly(seg, color=black, f=feed)
    for _ in range(26):
        sxp, syp = rng.uniform(x0 + 4, x1 - 4), rng.uniform(y0 + 4, y1 - 4)
        out += _dot(sxp, syp, rng.uniform(0.3, 0.9), color=black, f=feed)

    # the precessing figure-8 family — each loop a rounded double-circle, rotated
    for i in range(loops):
        t = i / (loops - 1)
        sc = (0.26 + 0.74 * t) * (grow ** i)
        ph = precess * t  # monotonic precession: the swept helix of iterations
        jr = 1.0 + 0.04 * rng.gauss(0, 1)  # subtle per-iteration transformation
        pts = []
        for k in range(half + 1):  # upper lobe — REMEMBER
            a = 2 * math.pi * k / half
            ox, oy = rot(wx * ru * sc * jr * math.sin(a), ru * sc * (1 - math.cos(a)), ph)
            pts.append((cx + ox, cyw + oy))
        for k in range(half + 1):  # lower lobe — FORGET (bigger)
            a = 2 * math.pi * k / half
            ox, oy = rot(wx * rl * sc * jr * math.sin(a), -rl * sc * (1 - math.cos(a)), ph)
            pts.append((cx + ox, cyw + oy))
        pen = accent if (i % 3 == 0 or i >= loops - 2) else black
        out += _poly(pts, color=pen, f=feed)

    # the central line carries THREE points the helix connects: INPUT → LATENT → OUTPUT
    top_node, bot_node = cyw + 1.98 * ru, cyw - 1.98 * rl
    aT, aB = top_node + 11, bot_node - 11
    out += _poly([(cx, aB), (cx, aT)], color=black, f=feed)
    out += _poly([(cx - 1.6, aT - 4), (cx, aT), (cx + 1.6, aT - 4)], color=black, f=feed)
    out += _poly([(cx - 1.6, aB + 4), (cx, aB), (cx + 1.6, aB + 4)], color=black, f=feed)
    out += fill_disc(cx, top_node, 1.9, spacing=0.5, pen=black, f=feed)  # OUTPUT point
    out += fill_disc(cx, bot_node, 1.9, spacing=0.5, pen=black, f=feed)  # INPUT point
    out += circle(cx, cyw, 2.6, pen=accent, f=feed)  # LATENT — the carried state
    out += _stroke_text(_spaced("OUTPUT"), cx + 6, aT - 1.2, 2.3, color=black, f=feed)
    out += _stroke_text(_spaced("INPUT"), cx + 6, aB - 1.2, 2.3, color=black, f=feed)
    out += _stroke_text(_spaced("LATENT"), cx + 6, cyw - 1.2, 2.2, color=accent, f=feed)

    # lobe descriptions
    out += _stroke_text(_spaced("REMEMBER"), cx - 13, cyw + ru * 0.95, 2.2, color=black, f=feed)
    out += _stroke_text(_spaced("C T"), cx - 4, cyw + ru * 0.95 - 5.2, 1.9, color=black, f=feed)
    out += _stroke_text(_spaced("FORGET"), cx - 11, cyw - rl * 0.98, 2.2, color=black, f=feed)
    out += _stroke_text(_spaced("C T-1"), cx - 6, cyw - rl * 0.98 - 5.2, 1.9, color=black, f=feed)

    # gate leaders (dot on an outer loop → dashed leader → label)
    def leader(px, py, lx, ly, l1, l2):
        out.extend(_dot(px, py, 1.4, color=black, f=feed))
        n = 7
        for s in range(0, n, 2):
            a = (px + (lx - px) * s / n, py + (ly - py) * s / n)
            b = (px + (lx - px) * (s + 1) / n, py + (ly - py) * (s + 1) / n)
            out.extend(_poly([a, b], color=black, f=feed))
        out.extend(_stroke_text(_spaced(l1), lx - 0.14 * W, ly + 2.2, 2.0, color=black, f=feed))
        out.extend(_stroke_text(_spaced(l2), lx - 0.14 * W, ly - 2.4, 1.8, color=black, f=feed))

    og = rot(-wx * ru, ru, precess * 0.5)
    ig = rot(wx * ru, ru * 0.4, precess * 0.5)
    fg = rot(-wx * rl, -rl, precess * 0.5)
    leader(cx + og[0], cyw + og[1], x0 + 0.14 * W, cyw + 0.22 * H, "OUTPUT GATE", "O T")
    leader(cx + ig[0], cyw + ig[1], x1 - 0.05 * W, cyw + 0.02 * H, "INPUT GATE", "I T")
    leader(cx + fg[0], cyw + fg[1], x0 + 0.13 * W, cyw - 0.18 * H, "FORGET GATE", "F T")

    # small series label
    out += _stroke_text(_spaced("LSTM   MEMORY IN TIME"), x0 + 0.03 * W, y0 + 8.0, 2.0, color=black, f=feed)
    return out




# ---------------------------------------------------------------------------
# piece 14 — LOCALITY IN SPACE (CNN as stacked wireframe feature-map terrains)
# ---------------------------------------------------------------------------


def bauhaus_locality_v1(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    layers: int = 4,
    nx: int = 38,
    ny: int = 38,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """LOCALITY IN SPACE — a CNN as a stack of feature-map TERRAINS, rendered by
    the shared 3D pen-plotter engine (z-buffer hidden-line, so each surface reads
    solid). The layers VARY with depth: a nearly-flat fine PIXEL grid, small-bump
    LOW-level, rounded-hill MID-level, up to a few big smooth HIGH-level peaks
    (the tallest in red). A red receptive-field window is tracked up the stack."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)  # PINK slot → crimson
    out: List[GCodeCommand] = []

    LW, DX, DY = 0.52 * W, 0.27 * W, 0.075 * H
    base_x = x0 + 0.11 * W
    base_y0 = y0 + 0.15 * H
    gap = 0.185 * H
    freqs = [9.0, 6.0, 3.6, 2.2, 1.8]
    amps = [0.004, 0.030, 0.078, 0.150, 0.170]

    def layer_z(i):
        fr = freqs[min(i, len(freqs) - 1)]
        Z = [[rng.fbm(iu / nx * fr + i * 11.3, jv / ny * fr + i * 5.7) for jv in range(ny + 1)] for iu in range(nx + 1)]
        lo = min(min(r) for r in Z)
        hi = max(max(r) for r in Z)
        rr = (hi - lo) or 1.0
        return [[(Z[iu][jv] - lo) / rr for jv in range(ny + 1)] for iu in range(nx + 1)]

    def proj(i, u, v, z):
        zh = amps[min(i, len(amps) - 1)] * H
        return (base_x + u * LW + v * DX, base_y0 + i * gap + v * DY + z * zh)

    import numpy as np

    centers = []
    for i in range(layers):
        Z = layer_z(i)
        top = i == layers - 1
        pun = pvn = 0.5
        if top:  # tallest peak → red
            bi = bj = 0
            bz = -1e9
            for iu in range(nx + 1):
                for jv in range(ny + 1):
                    if Z[iu][jv] > bz:
                        bz, bi, bj = Z[iu][jv], iu, jv
            pun, pvn = bi / nx, bj / ny
        SX = np.zeros((nx + 1, ny + 1))
        SY = np.zeros((nx + 1, ny + 1))
        DEP = np.zeros((nx + 1, ny + 1))
        PENV = np.full((nx + 1, ny + 1), black if black is not None else 0)
        for iu in range(nx + 1):
            u = iu / nx
            for jv in range(ny + 1):
                v = jv / ny
                z = Z[iu][jv]
                p = proj(i, u, v, z)
                SX[iu, jv], SY[iu, jv] = p[0], p[1]
                DEP[iu, jv] = -v + 0.2 * z
                if top and math.hypot(u - pun, v - pvn) < 0.20:
                    PENV[iu, jv] = accent if accent is not None else 0
        _zbuf_terrain(out, SX, SY, DEP, feed=feed, PENV=PENV, PXW=220, PXH=170)

        # receptive-field window (red), larger toward the input (bottom)
        uc, vc = 0.52, 0.46
        hw = 0.13 - i * 0.02
        zc = Z[int(uc * nx)][int(vc * ny)]
        sq = [
            proj(i, uc - hw, vc - hw, zc),
            proj(i, uc + hw, vc - hw, zc),
            proj(i, uc + hw, vc + hw, zc),
            proj(i, uc - hw, vc + hw, zc),
            proj(i, uc - hw, vc - hw, zc),
        ]
        out += _poly(sq, color=accent, f=feed)
        centers.append(proj(i, uc, vc, zc))

    # right-edge layer labels
    lbls = ["PIXELS", "LOW-LEVEL", "MID-LEVEL", "HIGH-LEVEL"]
    for i in range(layers):
        p = proj(i, 1.0, 0.5, 0.5)
        out += _stroke_text(_spaced(lbls[min(i, 3)]), p[0] + 5, p[1], 1.6, color=black, f=feed)

    # dashed red connectors up the receptive-field column
    for i in range(layers - 1):
        a, b = centers[i], centers[i + 1]
        n = 9
        for s in range(0, n, 2):
            p0 = (a[0] + (b[0] - a[0]) * s / n, a[1] + (b[1] - a[1]) * s / n)
            p1 = (a[0] + (b[0] - a[0]) * (s + 1) / n, a[1] + (b[1] - a[1]) * (s + 1) / n)
            out += _poly([p0, p1], color=accent, f=feed)

    # left depth arrow: PIXELS (bottom) ↔ HIGH-ORDER FEATURES (top)
    ax = x0 + 0.05 * W
    ay0, ay1 = base_y0, base_y0 + (layers - 1) * gap + 0.10 * H
    out += _poly([(ax, ay0), (ax, ay1)], color=black, f=feed)
    out += _poly([(ax - 1.4, ay1 - 3), (ax, ay1), (ax + 1.4, ay1 - 3)], color=black, f=feed)
    out += _poly([(ax - 1.4, ay0 + 3), (ax, ay0), (ax + 1.4, ay0 + 3)], color=black, f=feed)
    out += _stroke_text(_spaced("PIXELS"), ax - 2, ay0 - 5, 1.9, color=black, f=feed)
    out += _stroke_text(_spaced("HIGH-ORDER"), ax - 2, ay1 + 6.5, 1.9, color=black, f=feed)
    out += _stroke_text(_spaced("FEATURES"), ax - 2, ay1 + 2.0, 1.9, color=black, f=feed)

    # title + caption
    xT = x0 + 0.03 * W
    out += type_block(["CNN"], xT, y1 - 6.0, height=4.2, pen=black, underline=False, f=feed)
    out += _stroke_text(_spaced("LOCALITY IN SPACE"), xT, y1 - 16.0, 2.4, color=black, f=feed)
    cxp = x0 + 0.58 * W
    out += _stroke_text(_spaced("SMALL WINDOWS"), cxp, y0 + 20.0, 1.9, color=black, f=feed)
    out += _stroke_text(_spaced("DEEPER PATTERNS"), cxp, y0 + 15.0, 1.9, color=black, f=feed)
    out += _stroke_text(_spaced("A LARGER PICTURE"), cxp, y0 + 10.0, 1.9, color=black, f=feed)

    # bottom mini-diagram: receptive field shrinking grid → window → cell
    mgx, mgy, celln, cs = x0 + 0.10 * W, y0 + 10.0, 6, 2.2
    stages = [(celln, 3), (celln, 2), (celln, 1)]
    sx = mgx
    for si, (gn, winr) in enumerate(stages):
        for r in range(gn + 1):
            out += _poly([(sx, mgy + r * cs), (sx + gn * cs, mgy + r * cs)], color=black, f=feed)
        for c in range(gn + 1):
            out += _poly([(sx + c * cs, mgy), (sx + c * cs, mgy + gn * cs)], color=black, f=feed)
        cc = gn / 2.0
        out += _poly(
            [
                (sx + (cc - winr) * cs, mgy + (cc - winr) * cs),
                (sx + (cc + winr) * cs, mgy + (cc - winr) * cs),
                (sx + (cc + winr) * cs, mgy + (cc + winr) * cs),
                (sx + (cc - winr) * cs, mgy + (cc + winr) * cs),
                (sx + (cc - winr) * cs, mgy + (cc - winr) * cs),
            ],
            color=accent,
            f=feed,
        )
        nxt = sx + gn * cs + 5
        if si < len(stages) - 1:
            out += _poly([(sx + gn * cs + 1, mgy + gn * cs / 2), (nxt - 1, mgy + gn * cs / 2)], color=black, f=feed)
        sx = nxt + 4
    return out




# ---------------------------------------------------------------------------
# piece 15 — NONLINEAR TRANSFORMATION (MLP as a warped hourglass manifold)
# ---------------------------------------------------------------------------


def bauhaus_manifold(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    nu: int = 44,
    nv: int = 168,
    petals: int = 3,
    fold: float = 1.05,
    twist: float = 1.2,
    nstream: int = 52,
    stream_sep: float = 2.2,
    mesh_weave: float = 0.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """NONLINEAR TRANSFORMATION — an MLP as a folded petal-saddle, now a SHORT
    declaration on the Scene3D engine: the surface renders with native polar
    LOD (spider-web pole), depth-aware screen thinning in both families and
    optional mesh weave; streamlines flow INPUT→OUTPUT with pause-resume crowd
    control, cross-registered against the red fold-ridges; labels reserve
    halos; the whole composition fill-fits the page. 3 pens: surface+planes
    on the fine slot 0, red ridges/flow on 1, the rest black on 2."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    surface_pen = _pen(BLUE, colors)
    accent = _pen(PINK, colors)
    black = _pen(BLACK, colors)
    scene = Scene3D(
        rng, bounds, feed=feed, tip=0.5, px=(240, 320), pad=4.0, fit="fill", fit_pad=4.0
    )
    out = scene.out

    # ---- 3D world → isometric screen -------------------------------------
    cx0, cy0 = x0 + 0.50 * W, y0 + 0.50 * H
    a, cd, bwy = 0.29 * W, 0.070 * H, 0.195 * H
    Hy = 1.30

    def proj(wx, wy, wz):
        return (cx0 + (wx - wz) * a, cy0 + wy * bwy - (wx + wz) * cd)

    def depth(wx, wy, wz):
        return (wx + wz) + 0.12 * wy

    def surf(r, th):
        return fold * ((r ** 1.1) * math.cos(petals * th) + 0.20 * (r ** 2) * math.cos(2 * petals * th))

    # ---- surface grid ------------------------------------------------------
    SX = np.zeros((nu + 1, nv + 1))
    SY = np.zeros((nu + 1, nv + 1))
    DEP = np.zeros((nu + 1, nv + 1))
    for i in range(nu + 1):
        r = i / nu
        for j in range(nv + 1):
            th = 2 * math.pi * j / nv
            wx, wz = r * math.cos(th), r * math.sin(th)
            wy = surf(r, th)
            sx, sy = proj(wx, wy, wz)
            SX[i, j], SY[i, j], DEP[i, j] = sx, sy, depth(wx, wy, wz)

    scene.prime_scale(SX, SY)
    occ = scene.occupancy(stream_sep)

    # ---- text labels reserve halos up front --------------------------------
    xT = x0 + 0.02 * W
    wmax = _text_width(_spaced("LINEAR TRANSFORM"), 1.7)
    rx = min(x1 - 0.205 * W, x1 - wmax - 2.0)
    ci = proj(0.0, Hy, 0.0)
    co = proj(0.0, -Hy, 0.0)
    scene.halo_labels(
        [
            (_spaced("MLP"), xT, y1 - 8.0, 3.6, black),
            (_spaced("NONLINEAR TRANSFORMATION"), xT, y1 - 15.0, 2.0, black),
            (_spaced("INPUT SPACE"), ci[0] - 0.10 * W, ci[1] + 14.0, 2.3, black),
            (_spaced("OUTPUT SPACE"), co[0] - 0.10 * W, co[1] - 8.0, 2.3, black),
            (_spaced("LINEAR TRANSFORM"), rx, cy0 + 0.30 * H, 1.7, black),
            (_spaced("NONLINEAR"), rx, cy0 + 0.02 * H, 1.7, accent),
            (_spaced("ACTIVATION"), rx, cy0 - 0.03 * H, 1.7, accent),
            (_spaced("LINEAR TRANSFORM"), rx, cy0 - 0.30 * H, 1.7, black),
        ]
    )

    # ---- the fold, one declaration ------------------------------------------
    ridge_every = max(1, nv // petals)
    lod = PolarLOD(
        ridge_every=ridge_every,
        ridge_half=nv // (2 * petals),
        ridge_register=occ,
    )
    PENS = np.full((nu + 1, nv + 1), surface_pen if surface_pen is not None else 0)
    for j in range(nv + 1):
        if lod.is_ridge(j):
            PENS[:, j] = accent if accent is not None else 0
    thin = ScreenThin(gap_mm=0.8, far_mult=2.0, weave=mesh_weave)
    scene.surface(SX, SY, DEP, pens=PENS, lod=lod, thin=thin)

    # ---- streamlines: INPUT plane → fold → OUTPUT plane (engine crowd control)
    streams = []
    for s_i in range(nstream):
        th0 = 2 * math.pi * s_i / nstream
        r0 = 0.6 + 0.4 * rng.random()
        pen = accent if s_i % 4 == 0 else black
        line = []
        STEPS = 74
        for k in range(STEPS + 1):
            sfr = k / STEPS
            wy_lin = Hy - 2 * Hy * sfr
            rr = r0 * (0.42 + 0.58 * abs(2 * sfr - 1))
            th = th0 + twist * sfr
            blend = math.exp(-((sfr - 0.5) / 0.22) ** 2)
            wy = wy_lin * (1 - blend) + surf(min(1.0, rr), th) * blend
            wx, wz = rr * math.cos(th), rr * math.sin(th)
            sx, sy = proj(wx, wy, wz)
            line.append((sx, sy, depth(wx, wy, wz), pen))
        streams.append(line)
    scene.lines(streams, occupancy=occ, warmup=6, min_kept=6)

    # ---- INPUT / OUTPUT planes: dot lattice + frame -------------------------
    def plane(wy):
        g = 11
        for ia in range(g):
            for ib in range(g):
                gu, gv = -1.15 + 2.3 * ia / (g - 1), -1.15 + 2.3 * ib / (g - 1)
                sx, sy = proj(gu, wy, gv)
                if scene._blocked(sx, sy):
                    continue
                out.extend(_dot(sx, sy, 0.45, color=surface_pen, f=feed))
        corners = [(-1.15, -1.15), (1.15, -1.15), (1.15, 1.15), (-1.15, 1.15), (-1.15, -1.15)]
        scene.poly([proj(gu, wy, gv) for gu, gv in corners], pen=surface_pen)

    plane(Hy)
    plane(-Hy)
    for dl in range(10):  # dashed droplines through the ambient volume
        gu = -1.0 + 2.0 * rng.random()
        gv = -1.0 + 2.0 * rng.random()
        seg = [proj(gu, Hy - 2 * Hy * k / 20, gv) for k in range(0, 21, 2)]
        for k in range(0, len(seg) - 1, 2):
            scene.poly([seg[k], seg[k + 1]], pen=black)

    return scene.render()




# ---------------------------------------------------------------------------
# LSTM — MEMORY IN TIME (descending cell-state helix; studio rework)
# ---------------------------------------------------------------------------


def bauhaus_memory(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    loops: int = 40,
    half: int = 130,
    precess: float = 0.5,
    grow: float = 1.0,
    sep: float = 2.0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """MEMORY IN TIME — an LSTM as a figure-8 of PRECESSING loops (REMEMBER c_t
    above, FORGET c_{t-1} below, meeting at the carried-state waist), each
    iteration landing slightly rotated. Crowd control is ENGINE-NATIVE: the loop
    family renders through Scene3D.lines(pause_resume), so the waist and the
    bunched lobe rims self-limit to the paper's capacity instead of piling into
    ink. Labels reserve halos; gate leaders and the INPUT→LATENT→OUTPUT axis
    stay structural. Black + red."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)
    scene = Scene3D(rng, bounds, feed=feed, fit="rescue", tip=0.5)
    out = scene.out

    cx, cyw = x0 + 0.48 * W, y0 + 0.50 * H
    ru, rl, wx = 0.135 * H, 0.175 * H, 1.55  # top REMEMBER lobe, bigger FORGET lobe

    def rot(px, py, ph):
        c, s2 = math.cos(ph), math.sin(ph)
        return (px * c - py * s2, px * s2 + py * c)

    # labels FIRST so their halos carve through loops, orbits and stars
    scene.halo_labels(
        [
            (_spaced("OUTPUT"), cx + 6, cyw + 1.98 * ru + 9.8, 2.3, black),
            (_spaced("INPUT"), cx + 6, cyw - 1.98 * rl - 12.2, 2.3, black),
            (_spaced("LATENT"), cx + 6, cyw - 1.2, 2.2, accent),
            (_spaced("REMEMBER"), cx - 13, cyw + ru * 0.95, 2.2, black),
            (_spaced("C T"), cx - 4, cyw + ru * 0.95 - 5.2, 1.9, black),
            (_spaced("FORGET"), cx - 11, cyw - rl * 0.98, 2.2, black),
            (_spaced("C T-1"), cx - 6, cyw - rl * 0.98 - 5.2, 1.9, black),
        ]
    )

    # faint background orbits (dashed) + a light starfield
    for e in range(3):
        ea, eb = (0.34 + 0.05 * e) * W, (0.40 + 0.05 * e) * H
        erot = rng.uniform(-0.3, 0.3)
        seg = []
        for k in range(241):
            a = 2 * math.pi * k / 240
            ox, oy = rot(ea * 0.5 * math.cos(a), eb * 0.5 * math.sin(a), erot)
            if k % 6 < 3:
                seg.append((cx + ox, cyw + oy))
            elif len(seg) >= 2:
                scene.poly(seg, pen=black)
                seg = []
            else:
                seg = []
        if len(seg) >= 2:
            scene.poly(seg, pen=black)
    for _ in range(26):
        sxp, syp = rng.uniform(x0 + 4, x1 - 4), rng.uniform(y0 + 4, y1 - 4)
        out += _dot(sxp, syp, rng.uniform(0.3, 0.9), color=black, f=feed)

    # the precessing figure-8 family — ENGINE crowd control (outermost first so
    # the big envelope loops own their rims; inner iterations pause through
    # saturated stretches and resume where space opens)
    family = []
    for i in range(loops):
        t = i / (loops - 1)
        sc = (0.26 + 0.74 * t) * (grow ** i)
        ph = precess * t
        jr = 1.0 + 0.04 * rng.gauss(0, 1)
        pts = []
        for k in range(half + 1):  # upper lobe — REMEMBER
            a = 2 * math.pi * k / half
            ox, oy = rot(wx * ru * sc * jr * math.sin(a), ru * sc * (1 - math.cos(a)), ph)
            pts.append((cx + ox, cyw + oy))
        for k in range(half + 1):  # lower lobe — FORGET (bigger)
            a = 2 * math.pi * k / half
            ox, oy = rot(wx * rl * sc * jr * math.sin(a), -rl * sc * (1 - math.cos(a)), ph)
            pts.append((cx + ox, cyw + oy))
        pen = accent if (i % 3 == 0 or i >= loops - 2) else black
        family.append([(px, py, 0.0, pen) for (px, py) in pts])
    scene.lines(reversed(family), sep_mm=sep, warmup=0, min_kept=12)

    # the central axis: INPUT → LATENT → OUTPUT
    top_node, bot_node = cyw + 1.98 * ru, cyw - 1.98 * rl
    aT, aB = top_node + 11, bot_node - 11
    scene.poly([(cx, aB), (cx, aT)], pen=black)
    scene.poly([(cx - 1.6, aT - 4), (cx, aT), (cx + 1.6, aT - 4)], pen=black)
    scene.poly([(cx - 1.6, aB + 4), (cx, aB), (cx + 1.6, aB + 4)], pen=black)
    out += fill_disc(cx, top_node, 1.9, spacing=0.5, pen=black, f=feed)
    out += fill_disc(cx, bot_node, 1.9, spacing=0.5, pen=black, f=feed)
    out += circle(cx, cyw, 2.6, pen=accent, f=feed)  # LATENT — the carried state

    # gate leaders (dot on an outer loop → dashed leader → label)
    def leader(px, py, lx, ly, l1, l2):
        out.extend(_dot(px, py, 1.4, color=black, f=feed))
        n = 7
        for s2 in range(0, n, 2):
            a = (px + (lx - px) * s2 / n, py + (ly - py) * s2 / n)
            b = (px + (lx - px) * (s2 + 1) / n, py + (ly - py) * (s2 + 1) / n)
            scene.poly([a, b], pen=black)
        out.extend(_stroke_text(_spaced(l1), lx - 0.14 * W, ly + 2.2, 2.0, color=black, f=feed))
        out.extend(_stroke_text(_spaced(l2), lx - 0.14 * W, ly - 2.4, 1.8, color=black, f=feed))

    og = rot(-wx * ru, ru, precess * 0.5)
    ig = rot(wx * ru, ru * 0.4, precess * 0.5)
    fg = rot(-wx * rl, -rl, precess * 0.5)
    leader(cx + og[0], cyw + og[1], x0 + 0.14 * W, cyw + 0.22 * H, "OUTPUT GATE", "O T")
    leader(cx + ig[0], cyw + ig[1], x1 - 0.05 * W, cyw + 0.02 * H, "INPUT GATE", "I T")
    leader(cx + fg[0], cyw + fg[1], x0 + 0.13 * W, cyw - 0.18 * H, "FORGET GATE", "F T")

    out += _stroke_text(_spaced("LSTM   MEMORY IN TIME"), x0 + 0.03 * W, y0 + 8.0, 2.0, color=black, f=feed)
    return scene.render()




# ---------------------------------------------------------------------------
# CNN — FROM PIXELS TO MEANING (rising valley + receptive-field frustum; rework)
# ---------------------------------------------------------------------------


def bauhaus_locality(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 2,
    layers: int = 5,
    nx: int = 42,
    ny: int = 42,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """FROM PIXELS TO MEANING — a CNN as a rising valley of feature terrains
    (hidden-line occluded), each layer changing MORPHOLOGY with depth via a
    depth-varying box-blur: crunchy PIXELS → smooth OBJECT peaks. One crimson
    RECEPTIVE-FIELD frustum climbs from a small input patch to the tallest
    high-level peak — the single thread of data being abstracted. Diagonal
    recession so 'resolution down / abstraction up' is the reading axis."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)
    # Scene3D renders the terrains with native anti-crowding; `out` aliases the
    # scene buffer so every append keeps its historical draw order.
    scene = Scene3D(rng, bounds, feed=feed, px=(230, 180), fit="rescue")
    out = scene.out

    LW, DX, DY = 0.50 * W, 0.24 * W, 0.065 * H
    gap, STAGGER_X = 0.150 * H, 0.045 * W
    base_x, base_y0 = x0 + 0.085 * W, y0 + 0.135 * H
    freqs = [11.0, 6.5, 3.8, 2.4, 1.6]
    amps = [0.004, 0.028, 0.075, 0.140, 0.190]
    uc, vc = 0.46, 0.42

    def proj(i, u, v, z):
        return (base_x + u * LW + v * DX + i * STAGGER_X, base_y0 + i * gap + v * DY + z * amps[min(i, 4)] * H)

    def dep(i, v, z):
        return -v + 0.28 * z + 0.6 * i

    def box_blur(Z):
        B = Z.copy()
        B[1:-1, 1:-1] = 0.2 * (Z[1:-1, 1:-1] + Z[:-2, 1:-1] + Z[2:, 1:-1] + Z[1:-1, :-2] + Z[1:-1, 2:])
        return B

    def layer_z(i):
        fr = freqs[min(i, 4)]
        Z = np.array([[rng.fbm(iu / nx * fr + i * 11.3, jv / ny * fr + i * 5.7) for jv in range(ny + 1)] for iu in range(nx + 1)])
        for _ in range(i):
            Z = box_blur(Z)
        lo, hi = float(Z.min()), float(Z.max())
        return (Z - lo) / ((hi - lo) or 1.0)

    Zs = []
    for i in range(layers):
        Z = layer_z(i)
        top = i == layers - 1
        pun = pvn = 0.5
        if top:
            bi, bj = np.unravel_index(int(np.argmax(Z)), Z.shape)
            gg = np.array([[math.exp(-(((iu - bi) ** 2 + (jv - bj) ** 2) / (2 * (0.28 * nx) ** 2))) for jv in range(ny + 1)] for iu in range(nx + 1)])
            Z = Z * (0.35 + 0.65 * gg)
            Z = (Z - float(Z.min())) / ((float(Z.max()) - float(Z.min())) or 1.0)
            pun, pvn = bi / nx, bj / ny
        Zs.append(Z)
        SX = np.zeros((nx + 1, ny + 1))
        SY = np.zeros((nx + 1, ny + 1))
        DEP = np.zeros((nx + 1, ny + 1))
        PENV = np.full((nx + 1, ny + 1), black if black is not None else 0)
        for iu in range(nx + 1):
            u = iu / nx
            for jv in range(ny + 1):
                v = jv / ny
                z = Z[iu, jv]
                p = proj(i, u, v, z)
                SX[iu, jv], SY[iu, jv], DEP[iu, jv] = p[0], p[1], dep(i, v, z)
                if top and math.hypot(u - pun, v - pvn) < 0.16:
                    PENV[iu, jv] = accent if accent is not None else 0
        scene.surface(SX, SY, DEP, pens=PENV)

    # top-layer object contours (faint black, skip the crimson cap)
    top = layers - 1
    Zt = Zs[top]
    xs = [proj(top, iu / nx, 0.5, 0)[0] for iu in range(nx + 1)]
    ys = [proj(top, 0.5, jv / ny, 0)[1] for jv in range(ny + 1)]
    # (contours drawn in surface space below via marching squares over index grid)
    F = [[float(Zt[iu, jv]) for iu in range(nx + 1)] for jv in range(ny + 1)]
    gi = list(range(nx + 1))
    gj = list(range(ny + 1))
    bi2, bj2 = np.unravel_index(int(np.argmax(Zt)), Zt.shape)
    for lv in range(1, 6):
        iso = 0.45 + 0.5 * lv / 6.0
        for ch in _chain_segments(_marching_squares(F, gi, gj, iso)):
            if len(ch) < 5:
                continue
            pts = []
            for (ii, jj) in ch:
                if math.hypot(ii / nx - pun, jj / ny - pvn) < 0.16:
                    continue
                z = Zt[int(min(nx, max(0, ii)))][int(min(ny, max(0, jj)))]
                pts.append(proj(top, ii / nx, jj / ny, z))
            if len(pts) >= 2:
                out += _poly(pts, color=black, f=feed)

    # receptive-field frustum (crimson): growing draped window + 4 rails + centre dots
    def surf_z(i, u, v):
        return float(Zs[i][int(min(nx, max(0, round(u * nx))))][int(min(ny, max(0, round(v * ny))))])

    def _dashed(pts, dash=1.8, gap=3.6, pen=None):
        """Sparse dashes along a polyline (arc-length walk) — a whisper, not a wire."""
        cmds: List[GCodeCommand] = []
        on, acc = True, 0.0
        cur = [pts[0]]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
            seg = math.hypot(xb - xa, yb - ya)
            t = 0.0
            while t < seg:
                limit = (dash if on else gap) - acc
                step = min(limit, seg - t)
                t += step
                acc += step
                px, py = xa + (xb - xa) * t / seg, ya + (yb - ya) * t / seg
                if acc >= (dash if on else gap) - 1e-9:
                    if on:
                        cur.append((px, py))
                        if len(cur) >= 2:
                            cmds += _poly(cur, color=pen, f=feed)
                    cur = [(px, py)]
                    on, acc = not on, 0.0
                elif on:
                    cur.append((px, py))
        if on and len(cur) >= 2:
            cmds += _poly(cur, color=pen, f=feed)
        return cmds

    corner_paths = [[], [], [], []]
    for i in range(layers):
        hw = 0.045 + 0.052 * i
        cs = [(uc - hw, vc - hw), (uc + hw, vc - hw), (uc + hw, vc + hw), (uc - hw, vc + hw)]
        sq = [proj(i, cu, cv, surf_z(i, cu, cv)) for (cu, cv) in cs]
        out += _poly(sq + [sq[0]], color=accent, f=feed)
        for k, (cu, cv) in enumerate(cs):
            corner_paths[k].append(proj(i, cu, cv, surf_z(i, cu, cv)))
        out += _dot(*proj(i, uc, vc, surf_z(i, uc, vc)), 1.1, color=accent, f=feed)
    # receptive-field rails as sparse dashes — present but quiet (plot feedback:
    # the solid red wires dominated the terrains)
    for path in corner_paths:
        out += _dashed(path, pen=accent)

    # left abstraction/resolution axis (one honest rule, not a schematic)
    ax = x0 + 0.05 * W
    ay0, ay1 = base_y0, base_y0 + (layers - 1) * gap + 0.12 * H
    out += _poly([(ax, ay0), (ax, ay1)], color=black, f=feed)
    out += _poly([(ax - 1.4, ay1 - 3), (ax, ay1), (ax + 1.4, ay1 - 3)], color=black, f=feed)
    out += _poly([(ax - 1.4, ay0 + 3), (ax, ay0), (ax + 1.4, ay0 + 3)], color=black, f=feed)
    out += _stroke_text(_spaced("MORE ABSTRACTION"), ax - 2, ay1 + 4, 1.7, color=black, f=feed)
    out += _stroke_text(_spaced("SPATIAL RESOLUTION"), ax - 2, ay0 - 5, 1.7, color=black, f=feed)

    lbls = ["PIXELS", "EDGES", "TEXTURES", "PARTS", "OBJECTS"]
    for i in range(layers):
        p = proj(i, 1.0, 0.5, 0.5)
        out += _stroke_text(_spaced(lbls[min(i, 4)]), p[0] + 5, p[1], 1.6, color=black, f=feed)

    xT = x0 + 0.03 * W
    out += type_block(["CNN"], xT, y1 - 6.0, height=4.2, pen=black, underline=False, f=feed)
    out += _stroke_text(_spaced("FROM PIXELS TO MEANING"), xT, y1 - 16.0, 2.4, color=black, f=feed)
    out += scale_footer(bounds, text="M 1:80", pen=black, height=2.4, f=feed)
    return scene.render()




# ---------------------------------------------------------------------------
# TRANSFORMER — ATTENTION AS TOPOGRAPHY (single-query basin; studio rework)
# ---------------------------------------------------------------------------


def bauhaus_relevance(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
    tokens: int = 28,
    n_keys: int = 34,
    nu: int = 56,
    nv: int = 56,
    head: int = 0,
    tau: float = 0.55,
    sigma_k: float = 0.10,
    sigma_q: float = 0.30,
    basin_depth: float = 1.8,
    lean: float = 0.28,
    topk: int = 5,
    weights: str = "",
    block: int = 0,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """ATTENTION AS TOPOGRAPHY — the mechanism as a tight ISOMETRIC diamond
    stack: 1 QUERY + KEY SPACES (one shared sheet, Q and K as two red wells) ·
    2 DOT PRODUCT (the similarity landscape: black central peak flanked by red
    Q/K peaks, red swoop arrows falling in) · 3 SOFTMAX (contour rings
    tightening to the winner) · 4 VALUES (a full red rolling terrain) ·
    5 OUTPUT (green attended terrain, one dominant contextualized peak).
    Dashed anchor droplines tie the Q and K sites through every stage. Driven
    by a real attention row (checkpoint/GPT-2 via ``weights``)."""
    import numpy as np

    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blue, red, green, blk = 0, 1, 2, 3
    scene = Scene3D(rng, bounds, feed=feed, px=(230, 210), fit="rescue")
    out = scene.out
    ns = max(26, nu // 2)

    # real attention row → relative Q/K energy
    S = np.asarray(
        _attention_matrix(rng, tokens, head, temp=tau, causal=False, weights=weights, block=block, return_scores=True),
        dtype=float,
    )
    S = (S - S.min()) / (S.max() - S.min() + 1e-9)
    qi = int(np.argmax(S.max(axis=1)))
    w = np.exp(S[qi] / tau)
    w = w / w.sum()
    k_amp = 0.75 + 0.5 * float(max(w))  # K side scaled by the winning weight

    qw, kw = (-0.46, -0.12), (0.50, 0.16)  # Q and K sites (shared sheet coords)
    mid = ((qw[0] + kw[0]) / 2.0, (qw[1] + kw[1]) / 2.0)

    # ---- the diamond iso stack ------------------------------------------
    cx = x0 + 0.50 * W
    A, CD, HY = 0.205 * W, 0.050 * H, 0.055 * H
    n_stage = 5
    cy_top, cy_bot = y1 - 0.170 * H, y0 + 0.115 * H
    stepy = (cy_top - cy_bot) / (n_stage - 1)
    cyL = [cy_top - k * stepy for k in range(n_stage)]

    def mk_sheet(cyc, hfun, hscale, penfn=None, pen=blk):
        SX = np.zeros((ns + 1, ns + 1))
        SY = np.zeros((ns + 1, ns + 1))
        DE = np.zeros((ns + 1, ns + 1))
        PV = np.full((ns + 1, ns + 1), pen)
        for i in range(ns + 1):
            wx = -1 + 2 * i / ns
            for j in range(ns + 1):
                wz = -1 + 2 * j / ns
                wy = hfun(wx, wz) * hscale
                SX[i, j] = cx + (wx - wz) * A
                SY[i, j] = cyc + wy * HY - (wx + wz) * CD
                DE[i, j] = (wx + wz) + 0.12 * wy
                if penfn is not None:
                    PV[i, j] = penfn(wx, wz)
        scene.surface(SX, SY, DE, pens=PV)

    def at(cyc, wx, wz, wy=0.0, hs=0.0):
        return (cx + (wx - wz) * A, cyc + wy * hs * HY - (wx + wz) * CD)

    def g2(wx, wz, c, sig):
        return math.exp(-(((wx - c[0]) ** 2 + (wz - c[1]) ** 2) / (2 * sig * sig)))

    # ---- fields ----------------------------------------------------------
    def s1(wx, wz):  # two wells in a flat sheet
        return -0.95 * g2(wx, wz, qw, 0.17) - 0.95 * g2(wx, wz, kw, 0.17)

    def s2(wx, wz):  # similarity landscape
        return (
            1.05 * g2(wx, wz, mid, 0.20)
            + 0.62 * g2(wx, wz, qw, 0.16)
            + 0.62 * k_amp * g2(wx, wz, kw, 0.16)
            + 0.10 * rng.fbm(wx * 2.0 + 3.7, wz * 2.0 + 8.1)
        )

    def s_attn(wx, wz):  # sharpened winner
        return math.exp((s2(wx, wz) - 1.0) / max(0.15, tau * 0.55))

    def s4(wx, wz):  # V: rolling content terrain
        return (
            0.40 * (math.sin(2.3 * wx + 0.5) * math.cos(1.8 * wz) + 0.5 * math.sin(2.8 * wz + 1.2))
            + 0.42 * rng.fbm(wx * 1.7 + 5.5, wz * 1.7 + 2.2)
            + 0.30
        )

    def s5(wx, wz):  # attended output: V pulled up where attention mass sits
        return 0.35 * s4(wx, wz) + 1.05 * s_attn(wx, wz) * (0.4 + 0.6 * s4(wx, wz))

    # ---- halo labels (stage numbers left, formulas right, sub-notes) ------
    Lx = x0 + 0.020 * W
    Rx = x1 - 0.235 * W
    scene.halo_labels(
        [
            ("1", Lx, cyL[0] + 0.035 * H, 2.6, blk),
            (_spaced("QUERY + KEY SPACES"), Lx + 6, cyL[0] + 0.035 * H, 1.7, blk),
            (_spaced("Q QUERIES"), cx - 0.33 * W, cyL[0] + 0.065 * H, 1.7, red),
            (_spaced("K KEYS"), cx + 0.21 * W, cyL[0] + 0.065 * H, 1.7, red),
            ("2", Lx, cyL[1] + 0.035 * H, 2.6, blk),
            (_spaced("DOT PRODUCT"), Lx + 6, cyL[1] + 0.035 * H, 1.7, blk),
            (_spaced("Q . K T"), Rx, cyL[1] + 0.045 * H, 1.8, blk),
            (_spaced("SIMILARITY"), Rx, cyL[1] - 0.030 * H, 1.4, blk),
            (_spaced("LANDSCAPE"), Rx, cyL[1] - 0.048 * H, 1.4, blk),
            ("3", Lx, cyL[2] + 0.030 * H, 2.6, blk),
            (_spaced("SOFTMAX"), Lx + 6, cyL[2] + 0.030 * H, 1.7, blk),
            (_spaced("SOFTMAX QK T"), Rx, cyL[2] + 0.040 * H, 1.8, blk),
            (_spaced("NORMALIZED"), Rx, cyL[2] + 0.020 * H, 1.4, blk),
            (_spaced("ATTENTION WEIGHTS"), Rx, cyL[2] + 0.002 * H, 1.4, blk),
            ("4", Lx, cyL[3] + 0.030 * H, 2.6, blk),
            (_spaced("VALUES V"), Lx + 6, cyL[3] + 0.030 * H, 1.7, blk),
            (_spaced("V VALUES"), Rx, cyL[3] + 0.040 * H, 1.8, red),
            (_spaced("CONTENT TO"), Rx, cyL[3] - 0.030 * H, 1.4, blk),
            (_spaced("BE MIXED"), Rx, cyL[3] - 0.048 * H, 1.4, blk),
            ("5", Lx, cyL[4] + 0.030 * H, 2.6, blk),
            (_spaced("OUTPUT"), Lx + 6, cyL[4] + 0.030 * H, 1.7, blk),
            (_spaced("SOFTMAX QK T V"), Rx, cyL[4] + 0.040 * H, 1.8, blk),
            (_spaced("ATTENDED OUTPUT"), Rx, cyL[4] + 0.020 * H, 1.4, green),
            (_spaced("TOKENS"), cx + 0.26 * W, cyL[0] + 0.028 * H, 1.3, blk),
            (_spaced("DIMENSIONS"), cx + 0.27 * W, cyL[0] - 0.020 * H, 1.3, blk),
        ]
    )

    # ---- stage 1: shared sheet with the two wells
    def pen1(wx, wz):
        return red if (g2(wx, wz, qw, 0.17) > 0.30 or g2(wx, wz, kw, 0.17) > 0.30) else blk

    mk_sheet(cyL[0], s1, 0.9, penfn=pen1)

    # red swoop arrows: wells → the similarity peaks
    def swoop(p0, p1, bend, pen):
        mx, my = (p0[0] + p1[0]) / 2 + bend, (p0[1] + p1[1]) / 2
        pts = []
        for t in range(21):
            u = t / 20.0
            x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u * u * p1[0]
            y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u * u * p1[1]
            pts.append((x, y))
        scene.poly(pts, pen=pen)
        ux, uy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        L = math.hypot(ux, uy) or 1.0
        ux, uy = ux / L, uy / L
        nxv, nyv = -uy, ux
        b = pts[-1]
        scene.poly([(b[0] - (ux + nxv * 0.5) * 2.6, b[1] - (uy + nyv * 0.5) * 2.6), b,
                    (b[0] - (ux - nxv * 0.5) * 2.6, b[1] - (uy - nyv * 0.5) * 2.6)], pen=pen)

    swoop(at(cyL[0], *qw), at(cyL[1], qw[0] * 0.7, qw[1] * 0.7), -9.0, red)
    swoop(at(cyL[0], *kw), at(cyL[1], kw[0] * 0.7, kw[1] * 0.7), 9.0, red)

    # ---- stage 2: similarity landscape (red side peaks, black centre)
    def pen2(wx, wz):
        side = max(g2(wx, wz, qw, 0.16), k_amp * g2(wx, wz, kw, 0.16))
        return red if side > 0.42 and g2(wx, wz, mid, 0.20) < 0.55 else blk

    mk_sheet(cyL[1], s2, 0.85, penfn=pen2)

    # ---- stage 3: softmax rings tightening to the winner
    gN = 64
    xs = [-1 + 2 * i / gN for i in range(gN + 1)]
    zs = [-1 + 2 * j / gN for j in range(gN + 1)]
    P = [[s_attn(xs[i], zs[j]) for i in range(gN + 1)] for j in range(gN + 1)]
    pmax = max(max(row) for row in P) or 1.0
    for lv in range(1, 10):
        iso = (lv / 10.0) ** 1.6 * pmax
        for ch in _chain_segments(_marching_squares(P, xs, zs, iso)):
            if len(ch) < 5:
                continue
            pts = [at(cyL[2], wx, wz) for (wx, wz) in ch]
            scene.poly(pts, pen=blk)
    # sheet border diamond
    br = [at(cyL[2], -1, -1), at(cyL[2], 1, -1), at(cyL[2], 1, 1), at(cyL[2], -1, 1), at(cyL[2], -1, -1)]
    scene.poly(br, pen=blk)

    # blue dashed arrows: weights falling onto V
    for wxa in (-0.5, -0.15, 0.2, 0.55):
        p0 = at(cyL[2], wxa, 0.1)
        p1 = at(cyL[3], wxa, 0.1)
        n = 8
        for q in range(0, n, 2):
            a = (p0[0], p0[1] + (p1[1] - p0[1]) * q / n)
            b = (p0[0], p0[1] + (p1[1] - p0[1]) * (q + 1) / n)
            scene.poly([a, b], pen=blue)
        scene.poly([(p1[0] - 1.4, p1[1] + 2.6), p1, (p1[0] + 1.4, p1[1] + 2.6)], pen=blue)

    # ---- stage 4: VALUES — full red rolling terrain
    mk_sheet(cyL[3], s4, 0.75, pen=red)

    # ---- stage 5: OUTPUT — green attended terrain
    mk_sheet(cyL[4], s5, 0.80, pen=green)

    # dashed anchor droplines through the whole stack (Q site and K site)
    for site in (qw, kw):
        for k in range(n_stage - 1):
            p0 = at(cyL[k], *site)
            p1 = at(cyL[k + 1], *site)
            n = 9
            for q in range(0, n, 2):
                a = (p0[0], p0[1] + (p1[1] - p0[1]) * q / n)
                b = (p0[0], p0[1] + (p1[1] - p0[1]) * (q + 1) / n)
                scene.poly([a, b], pen=blk)

    # ---- title
    out += _stroke_text(_spaced("ATTENTION AS TOPOGRAPHY"), x0 + 0.13 * W, y1 - 0.035 * H, 3.0, color=blk, f=feed)
    out += _stroke_text(_spaced("QUERIES SHAPE CONTENT THROUGH CONTEXT"), x0 + 0.17 * W, y1 - 0.062 * H, 1.6, color=blk, f=feed)
    out += scale_footer(bounds, text="A = SOFTMAX(QK T)  Z = AV", pen=blk, height=2.4, f=feed)
    return scene.render()




# ---------------------------------------------------------------------------
# LSTM — GATED MEMORY DYNAMICS (gate mandala flavor: cell-state hub, four gate
# discs, log-spiral bundles; sibling of bauhaus_memory's figure-8)
# ---------------------------------------------------------------------------


def lstm_gates(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    bundle: int = 14,
    orbits: int = 3,
    sep: float = 1.6,
    feed: int = 2200,
) -> List[GCodeCommand]:
    """GATED MEMORY DYNAMICS — the LSTM as a gate mandala: the CELL STATE hub
    with four gate discs (FORGET, INPUT, CANDIDATE, OUTPUT), each holding a
    0→1 slider; LOGARITHMIC-SPIRAL bundles stream between hub and gates
    (memory flowing through gates), crowd-controlled natively by the engine so
    bundles tighten at the rims without knotting. Dashed orbits + time axes.
    Black + crimson; sibling flavor of the figure-8 ``bauhaus_memory``."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    accent, black = _pen(PINK, colors), _pen(BLACK, colors)
    scene = Scene3D(rng, bounds, feed=feed, fit="rescue", tip=0.5)
    out = scene.out

    cx, cy = x0 + 0.50 * W, y0 + 0.545 * H
    r_cell = 0.085 * W
    r_gate = 0.075 * W
    D = 0.335 * W  # hub→gate distance
    gates = [
        ("FORGET GATE", math.radians(133), 0.15),
        ("INPUT GATE", math.radians(42), 0.85),
        ("CANDIDATE", math.radians(215), 0.75),
        ("OUTPUT GATE", math.radians(300), 0.9),
    ]

    # labels first: halos carve through bundles and orbits
    labels = [
        (_spaced("CELL STATE"), cx - 0.088 * W, cy + 2.2, 1.9, black),
        (_spaced("MEMORY IN TIME"), cx - 0.082 * W, cy - 5.4, 1.4, black),
        (_spaced("C T-1"), x0 + 0.035 * W, cy + 2.4, 1.8, black),
        (_spaced("C T"), x1 - 0.075 * W, cy + 2.4, 1.8, black),
        (_spaced("TIME"), cx + 3.0, y1 - 0.045 * H, 1.8, black),
        (_spaced("H T   OUTPUT"), cx + 3.0, y0 + 0.075 * H, 1.8, black),
    ]
    for name, ang, _v in gates:
        gx, gy = cx + D * math.cos(ang), cy + D * math.sin(ang)
        labels.append((_spaced(name), gx - 0.066 * W, gy + 3.4, 1.5, black))
    scene.halo_labels(labels)

    # dashed orbit circles + scattered nodes
    for e in range(orbits):
        orad = D * (0.72 + 0.34 * e) + rng.uniform(-3, 3)
        seg = []
        for k in range(301):
            a = 2 * math.pi * k / 300
            px, py = cx + orad * math.cos(a), cy + orad * math.sin(a)
            if not (x0 + 3 < px < x1 - 3 and y0 + 3 < py < y1 - 3):
                if len(seg) >= 2:
                    scene.poly(seg, pen=black)
                seg = []
                continue
            if k % 8 < 4:
                seg.append((px, py))
            elif len(seg) >= 2:
                scene.poly(seg, pen=black)
                seg = []
            else:
                seg = []
        if len(seg) >= 2:
            scene.poly(seg, pen=black)
    for _ in range(10):
        a = rng.uniform(0, 2 * math.pi)
        orad = D * rng.uniform(0.7, 1.05)
        px, py = cx + orad * math.cos(a), cy + orad * math.sin(a)
        if x0 + 4 < px < x1 - 4 and y0 + 4 < py < y1 - 4:
            out += circle(px, py, rng.uniform(0.8, 1.5), pen=black, f=feed)

    # LOG-SPIRAL bundles hub↔gate (the memory flow), engine crowd control
    family = []
    for gi, (_name, ang, _v) in enumerate(gates):
        for k in range(bundle):
            t = k / max(1, bundle - 1)
            sweep = (1.1 + 2.0 * t) * (1 if k % 2 == 0 else -1)
            r0 = r_cell * (1.02 + 0.06 * rng.random())
            r1 = D - r_gate * (1.0 + 0.25 * t)
            b = math.log(max(1e-6, r1 / r0)) / sweep
            th0 = ang - sweep
            pts = []
            NPT = 64
            for q in range(NPT + 1):
                u = q / NPT
                th = th0 + sweep * u
                r = r0 * math.exp(b * sweep * u)
                pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
            pen = accent if k % 4 == 0 else black
            family.append([(px, py, 0.0, pen) for (px, py) in pts])
    scene.lines(family, sep_mm=sep, warmup=2, min_kept=10)

    # axes: c_{t-1} -> c_t horizontal, TIME up, h_t down from output side
    scene.poly([(x0 + 0.10 * W, cy), (x1 - 0.10 * W, cy)], pen=black)
    scene.poly([(x1 - 0.10 * W - 3, cy + 1.6), (x1 - 0.10 * W, cy), (x1 - 0.10 * W - 3, cy - 1.6)], pen=black)
    scene.poly([(cx, y0 + 0.06 * H), (cx, y1 - 0.05 * H)], pen=black)
    scene.poly([(cx - 1.6, y1 - 0.05 * H - 3), (cx, y1 - 0.05 * H), (cx + 1.6, y1 - 0.05 * H - 3)], pen=black)
    scene.poly([(cx - 1.6, y0 + 0.06 * H + 3), (cx, y0 + 0.06 * H), (cx + 1.6, y0 + 0.06 * H + 3)], pen=black)

    # the hub disc + plus mark
    out += circle(cx, cy, r_cell, pen=black, f=feed)
    out += circle(cx, cy, r_cell + 1.6, pen=black, f=feed)
    out += _poly([(cx - 2.2, cy - 9.0), (cx + 2.2, cy - 9.0)], color=black, f=feed)
    out += _poly([(cx, cy - 9.0 - 2.2), (cx, cy - 9.0 + 2.2)], color=black, f=feed)

    # gate discs: double circle + 0—1 slider with a red dot at the gate value
    for _name, ang, val in gates:
        gx, gy = cx + D * math.cos(ang), cy + D * math.sin(ang)
        out += circle(gx, gy, r_gate, pen=black, f=feed)
        out += circle(gx, gy, r_gate + 1.5, pen=black, f=feed)
        sx0, sx1 = gx - r_gate * 0.55, gx + r_gate * 0.55
        sy = gy - r_gate * 0.34
        scene.poly([(sx0, sy), (sx1, sy)], pen=black)
        for q in range(4):
            qx = sx0 + (sx1 - sx0) * q / 3
            out += circle(qx, sy + 1.8, 1.1, pen=black, f=feed)
        dotx = sx0 + (sx1 - sx0) * val
        out += fill_disc(dotx, sy + 1.8, 1.1, spacing=0.4, pen=accent, f=feed)
        out += _stroke_text("0", sx0 - 1.0, sy - 4.6, 1.3, color=black, f=feed)
        out += _stroke_text("1", sx1 - 0.5, sy - 4.6, 1.3, color=black, f=feed)

    # title + margin micro-texts
    out += type_block(["LSTM"], x0 + 0.38 * W, y0 + 0.045 * H, height=4.6, pen=black, underline=False, f=feed)
    out += _stroke_text(_spaced("GATED MEMORY DYNAMICS"), x0 + 0.27 * W, y0 + 0.018 * H, 2.0, color=black, f=feed)
    micro = [
        (("SEQUENCES", "CREATE", "MEMORY"), x0 + 0.03 * W, y1 - 0.045 * H),
        (("PAST", "PRESENT", "FUTURE"), x1 - 0.16 * W, y1 - 0.045 * H),
        (("RECURSION", "CREATES", "PERSISTENCE"), x0 + 0.03 * W, y0 + 0.16 * H),
        (("A SMALL", "MECHANISM", "A LONG MEMORY"), x1 - 0.19 * W, y0 + 0.16 * H),
    ]
    for lines_, mx, my in micro:
        for li, txt in enumerate(lines_):
            out += _stroke_text(_spaced(txt), mx, my - li * 3.4, 1.3, color=black, f=feed)
    return scene.render()
