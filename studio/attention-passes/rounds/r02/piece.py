"""ATTENTION — FORWARD AND BACKWARD  (round 02: TRUE MECHANISM)

Every mark is a real number out of `mechanism.py`.  The plate follows ONE
query — row 12 of GPT-2 layer 1 head 0 — all the way out and all the way
back.

  * `similarity` IS the recovered QK^T/sqrt(d) score matrix, and its
    triangular silhouette is the causal mask, not a design choice.
  * between `similarity` and `softmax` each strand is drawn as a ribbon
    whose width at every x is the probability that score would carry at
    softmax temperature tau(x), annealed from tau -> inf (all thirteen
    scores equal: no distribution yet) down to tau = 1 (the real row).
    Strands are dropped as their ribbon falls under the pen.  That taper
    IS the information being destroyed, and it is exact.
  * `softmax` carries the real normalised row: teeth to the RIGHT, summing
    to 1.000000.  The other fourteen rows of the same head are the quiet
    teeth to the LEFT.
  * the backward register is the real gradient — dL/dV = A^T dL/dZ,
    dL/dA = dL/dZ V^T, the softmax Jacobian, dL/dQ, dL/dK — verified
    against central finite differences (NOTES.md).  The backward comb is
    the SAME row, mirrored: V's gradient is the attention re-applied.

ORDER: a convergent flow through a WAIST, run twice in opposite directions.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import (
    _chain_segments,
    _dot,
    _marching_squares,
    _poly,
    _stroke_text,
    _text_width,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("attn_mechanism", _HERE / "mechanism.py")
mechanism = importlib.util.module_from_spec(_spec)
sys.modules["attn_mechanism"] = mechanism  # dataclass needs the module registered
_spec.loader.exec_module(mechanism)

# pen slots for --palette black,dodgerblue,crimson
BLACK, BLUE, RED = 0, 1, 2
TIP = 0.30  # mm, the pen's own width; nothing is finer than this


def _pen(i: int, colors: int) -> Optional[int]:
    return i % colors if colors > 1 else None


# ---------------------------------------------------------------------------
# geometry helpers
# ---------------------------------------------------------------------------


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 30) -> List[Pt]:
    out = []
    for k in range(n + 1):
        t = k / n
        m = 1.0 - t
        out.append(
            (
                m ** 3 * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t ** 3 * p3[0],
                m ** 3 * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t ** 3 * p3[1],
            )
        )
    return out


def _resample(pts: Sequence[Pt], pitch: float) -> List[Pt]:
    out: List[Pt] = []
    if len(pts) < 2:
        return out
    carry = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        seg = math.hypot(dx, dy)
        if seg < 1e-9:
            continue
        ux, uy = dx / seg, dy / seg
        s = carry
        while s < seg:
            out.append((a[0] + ux * s, a[1] + uy * s))
            s += pitch
        carry = s - seg
    return out


def _dotted(pts: Sequence[Pt], r: float, pen: Optional[int], pitch: float) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for p in _resample(pts, pitch):
        out += _dot(p[0], p[1], max(TIP * 0.5, r), color=pen)
    return out


def _dash(pts: Sequence[Pt], pen: Optional[int], on: float = 1.2, off: float = 1.5,
          f: int = 2100) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    run: List[Pt] = []
    acc, drawing = 0.0, True
    for a, b in zip(pts[:-1], pts[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if drawing:
            if not run:
                run.append(a)
            run.append(b)
            if acc >= on:
                out += _poly(run, color=pen, f=f)
                run, acc, drawing = [], 0.0, False
        elif acc >= off:
            acc, drawing = 0.0, True
    if len(run) >= 2:
        out += _poly(run, color=pen, f=f)
    return out


def _through(s0: Pt, neck: Pt, d0: Pt, o: float, n: int = 40) -> List[Pt]:
    """One strand of a sheaf: out of the source, through a common neck at
    offset ``o``, then out again to the destination.  Every bundle on the
    plate necks, because the plate's order is flow through a waist."""
    nk_ = (neck[0], neck[1] + o)
    a = _bez(s0, (s0[0] + 0.58 * (nk_[0] - s0[0]), s0[1]),
             (nk_[0] - 0.30 * (nk_[0] - s0[0]), nk_[1]), nk_, n=n // 2)
    b = _bez(nk_, (nk_[0] + 0.30 * (d0[0] - nk_[0]), nk_[1]),
             (d0[0] - 0.52 * (d0[0] - nk_[0]), d0[1]), d0, n=n // 2)
    return a + b[1:]


def _tan(pts: Sequence[Pt], f: float) -> Pt:
    i = max(1, min(len(pts) - 1, int(len(pts) * f)))
    dx, dy = pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]
    L = math.hypot(dx, dy) or 1.0
    return (dx / L, dy / L)


def _arrow_on(pts: Sequence[Pt], f: float, size: float, pen: Optional[int]) -> List[GCodeCommand]:
    """Small solid triangle at fraction f of the path, pointing BACKWARDS."""
    i = max(1, min(len(pts) - 1, int(len(pts) * f)))
    p = pts[i]
    tx, ty = _tan(pts, f)
    ux, uy = -tx, -ty
    nx, ny = -uy, ux
    tip = (p[0] + ux * size, p[1] + uy * size)
    a = (p[0] - ux * size * 0.30 + nx * size * 0.50, p[1] - uy * size * 0.30 + ny * size * 0.50)
    b = (p[0] - ux * size * 0.30 - nx * size * 0.50, p[1] - uy * size * 0.30 - ny * size * 0.50)
    out = _poly([tip, a, b, tip], color=pen, f=1400)
    for k in (0.32, 0.66):
        m = (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)
        out += _poly([tip, m], color=pen, f=1400)
    return out


def _sq(x: float, y: float, s: float, pen: Optional[int]) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    n = max(2, int(round(2 * s / (TIP * 0.80))))
    for k in range(n + 1):
        yy = y - s + 2 * s * k / n
        out += _poly([(x - s, yy), (x + s, yy)], color=pen, f=1400)
    return out


def _vrule(x: float, ya: float, yb: float, pen: Optional[int],
           period: float = 3.0, duty: float = 0.38) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    y = ya
    while y < yb:
        out += _poly([(x, y), (x, min(yb, y + period * duty))], color=pen, f=2200)
        y += period
    return out


def _cross(x: float, y: float, s: float, pen: Optional[int]) -> List[GCodeCommand]:
    return _poly([(x - s, y), (x + s, y)], color=pen, f=2000) + _poly(
        [(x, y - s), (x, y + s)], color=pen, f=2000
    )


def _text(s: str, x: float, y: float, h: float, pen: Optional[int],
          spaced: bool = False) -> List[GCodeCommand]:
    return _stroke_text(" ".join(s) if spaced else s, x, y, h, color=pen, f=2300)


def _tw(s: str, h: float, spaced: bool = False) -> float:
    return _text_width(" ".join(s) if spaced else s, h)


def _frac(num: str, den: str, x: float, y: float, h: float,
          pen: Optional[int]) -> List[GCodeCommand]:
    """A stacked fraction, as the reference sets the gradient labels."""
    w = max(_tw(num, h), _tw(den, h))
    out = _text(num, x + (w - _tw(num, h)) / 2, y + h * 0.42, h, pen)
    out += _poly([(x - 0.4, y - h * 0.10), (x + w + 0.4, y - h * 0.10)], color=pen, f=2200)
    out += _text(den, x + (w - _tw(den, h)) / 2, y - h * 1.52, h, pen)
    return out


# ---------------------------------------------------------------------------
# the three wells — three genuinely different KINDS of field
# ---------------------------------------------------------------------------


def _grid(box: Bounds, nx: int, ny: int):
    x0, y0, x1, y1 = box
    return ([x0 + (x1 - x0) * i / (nx - 1) for i in range(nx)],
            [y0 + (y1 - y0) * j / (ny - 1) for j in range(ny)])


def _contours(F, xs, ys, levels, pen, pitch, r_of, min_len=2.6) -> List[GCodeCommand]:
    out: List[GCodeCommand] = []
    for lv in levels:
        segs = _marching_squares(F, xs, ys, lv)
        if not segs:
            continue
        for chain in _chain_segments(segs):
            if len(chain) < 3:
                continue
            L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(chain[:-1], chain[1:]))
            if L < min_len:
                continue
            out += _dotted(chain, r_of(lv), pen, pitch)
    return out


def _ladder(F, n: int, sym: bool, lo_frac: float = 0.10) -> List[float]:
    """Geometric level ladder: constant ring pitch instead of flooding."""
    a = float(np.max(np.abs(F)))
    if a <= 0:
        return []
    lo = a * lo_frac
    ks = [lo * (a / lo) ** (k / (n - 1)) for k in range(n)]
    return ([-k for k in ks] + ks) if sym else ks


def _well_dipole(box: Bounds, u: Pt, pen, pitch: float, rmax: float, n: int = 7):
    """Q — a DIRECTION.  Level sets of the real query functional p -> q.p on
    the token cloud: two opposed lobes pinched at the node.  The only signed
    well, because a direction is the only signed thing here."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    xs, ys = _grid(box, 120, 74)
    ux, uy = u
    X = (np.array(xs)[None, :] - cx) / rx
    Y = (np.array(ys)[:, None] - cy) / ry
    F = (X * ux + Y * uy) * np.exp(-(X * X + Y * Y) * 1.55)
    lv = _ladder(F, n, sym=True, lo_frac=0.13)
    a = max(abs(v) for v in lv) if lv else 1.0
    out = _contours(F, xs, ys, lv, pen, pitch,
                    lambda v: TIP * 0.55 + rmax * (abs(v) / a) ** 0.85)
    return out, (cx, cy)


def _well_modes(box: Bounds, pts, wts, pen, pitch: float, rmax: float, n: int = 8):
    """K — a FIELD OF MANY.  The real projected key vectors as a kernel sum:
    one lumpy envelope outside, separate islands inside."""
    x0, y0, x1, y1 = box
    xs, ys = _grid(box, 128, 80)
    sig = 0.078 * (x1 - x0)
    X = np.array(xs)[None, :]
    Y = np.array(ys)[:, None]
    F = np.zeros((len(ys), len(xs)))
    for (px, py), w in zip(pts, wts):
        F += w * np.exp(-((X - px) ** 2 + (Y - py) ** 2) / (2 * sig * sig))
    lv = _ladder(F, n, sym=False, lo_frac=0.14)
    a = max(lv) if lv else 1.0
    out = _contours(F, xs, ys, lv, pen, pitch, lambda v: TIP * 0.55 + rmax * (v / a) ** 0.85)
    return out, pts[int(np.argmax(wts))]


def _well_strata(box: Bounds, rows, tilt, pen, pitch: float, rmax: float, n: int = 6):
    """V — CONTENT IN LAYERS.  One lamina per token; its height is the real
    scalar content of that token's value vector, tilted by the second
    channel.  Level sets are near-parallel strata: neither a point nor a
    direction, which is the whole reason V is a different kind of thing."""
    x0, y0, x1, y1 = box
    xs, ys = _grid(box, 112, 96)
    m = len(rows)
    ycen = [y0 + (y1 - y0) * (j + 0.5) / m for j in range(m)]
    X = np.array(xs)[None, :]
    Y = np.array(ys)[:, None]
    sig = (y1 - y0) / m * 1.25
    u = (X - (x0 + x1) / 2) / ((x1 - x0) / 2)
    F = np.zeros((len(ys), len(xs)))
    Wt = np.zeros((len(ys), len(xs))) + 1e-9
    for j in range(m):
        k = np.exp(-((Y - ycen[j]) ** 2) / (2 * sig * sig)) + 0.0 * u
        F += k * (rows[j] + tilt[j] * u)
        Wt += k
    F = F / Wt
    lv = _ladder(F, n, sym=True, lo_frac=0.085)
    a = max(abs(v) for v in lv) if lv else 1.0
    out = _contours(F, xs, ys, lv, pen, pitch,
                    lambda v: TIP * 0.55 + rmax * (abs(v) / a) ** 0.85, min_len=9.0)
    return out, ((x0 + x1) / 2, ycen[int(np.argmax(np.abs(rows)))])


def _anneal(logits: np.ndarray, tau: float) -> np.ndarray:
    z = logits / tau
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def _blob(x: float, y: float, r: float, pen: Optional[int]) -> List[GCodeCommand]:
    """A round filled dot, as ONE spiral stroke.  `_dot` draws a horizontal
    line of length 2r, which at lattice scale reads as a dash and destroyed
    the score matrix in rounds 1-3; a lattice of dots of varying SIZE only
    works if the marks are actually round."""
    r = max(TIP * 0.5, r)
    if r <= TIP * 0.62:
        return _poly([(x - r, y), (x + r, y)], color=pen, f=1500)
    pitch = TIP * 0.62
    turns = r / pitch
    n = max(12, int(turns * 22))
    pts = []
    for k in range(n + 1):
        t = k / n
        rr = r * t
        a = 2 * math.pi * turns * t
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    pts.append((x + r, y))
    return _poly(pts, color=pen, f=1500)


def attention_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    blk, blu, red = _pen(BLACK, colors), _pen(BLUE, colors), _pen(RED, colors)

    M = mechanism.build(seed=rng.randint(1, 99991))
    A, S, dS, dV = M.A, M.S, M.dS, M.dV
    T = A.shape[0]
    q = M.row
    nk = q + 1
    row = A[q, :nk]
    logits = S[q, :nk]

    # --- real 2D projections ------------------------------------------------
    QK = np.vstack([M.Q, M.K])
    QK = QK - QK.mean(axis=0, keepdims=True)
    B = np.linalg.svd(QK, full_matrices=False)[2][:2].T
    Kp, dKp = M.K @ B, M.dK @ B
    qv = M.Q[q] @ B
    qv = qv / (np.linalg.norm(qv) + 1e-12)
    dqv = M.dQ[q] @ B
    dqv = dqv / (np.linalg.norm(dqv) + 1e-12)
    Vb = np.linalg.svd(M.V - M.V.mean(0, keepdims=True), full_matrices=False)[2][:2].T
    Vs, dVs = M.V @ Vb, dV @ Vb

    # --- stations -----------------------------------------------------------
    x_lab = x0 + 0.028 * W
    x_sim = x0 + 0.470 * W
    x_sft = x0 + 0.645 * W
    x_wv = x0 + 0.802 * W
    x_Z = x0 + 0.952 * W

    fb0, fb1 = y0 + 0.470 * H, y0 + 0.962 * H
    bb0, bb1 = y0 + 0.092 * H, y0 + 0.372 * H
    y_axis = y0 + 0.040 * H
    RF = (0.155, 0.500, 0.845)          # V, K, Q — shared by both registers
    IV, IK, IQ = 0, 1, 2

    def frow(k):
        return fb0 + (fb1 - fb0) * RF[k]

    def brow(k):
        return bb0 + (bb1 - bb0) * RF[k]

    out: List[GCodeCommand] = []

    # ======================================================================
    # 1. FURNITURE
    # ======================================================================
    for x, lab in ((x_sim, "similarity"), (x_sft, "softmax"), (x_wv, "weighted values")):
        out += _vrule(x, bb0 - 0.030 * H, fb1 + 0.010 * H, blk)
        out += _text(lab, x - _tw(lab, 2.4, True) / 2, fb1 + 0.024 * H, 2.4, blk, spaced=True)

    cs = 0.012 * W
    for (cx, cy) in ((x0 + 0.020 * W, fb1 + 0.014 * H), (x1 - 0.020 * W, fb1 + 0.014 * H),
                     (x0 + 0.020 * W, y_axis - 0.016 * H), (x1 - 0.020 * W, y_axis - 0.016 * H)):
        out += _cross(cx, cy, cs, blk)

    mid = (x0 + x1) / 2
    fwd_t, bwd_t = "forward pass", "backward pass"
    fx = x0 + 0.145 * W
    bx_ = x1 - 0.145 * W - _tw(bwd_t, 2.4, True)
    out += _poly([(x0 + 0.042 * W, y_axis), (fx - 3.0, y_axis)], color=blk, f=2200)
    out += _text(fwd_t, fx, y_axis - 1.2, 2.4, blk, spaced=True)
    out += _poly([(fx + _tw(fwd_t, 2.4, True) + 3.0, y_axis), (mid - 0.040 * W, y_axis)],
                 color=blk, f=2200)
    out += _arrow_on([(mid - 0.055 * W, y_axis), (mid - 0.040 * W, y_axis)], 1.0, 2.0, blk)
    out += _poly([(mid + 0.040 * W, y_axis), (bx_ - 3.0, y_axis)], color=blk, f=2200)
    out += _arrow_on([(mid + 0.055 * W, y_axis), (mid + 0.040 * W, y_axis)], 1.0, 2.0, blk)
    out += _text(bwd_t, bx_, y_axis - 1.2, 2.4, blk, spaced=True)
    out += _poly([(bx_ + _tw(bwd_t, 2.4, True) + 3.0, y_axis), (x1 - 0.042 * W, y_axis)],
                 color=blk, f=2200)
    out += _blob(mid, y_axis, 1.05, blk)

    # ======================================================================
    # 2. REGISTRATION SPINES
    # ======================================================================
    for k, pen in ((IV, red), (IK, blk), (IQ, blu)):
        sx = x0 + 0.0060 * W + 0.0052 * W * k
        out += _vrule(sx, brow(k), frow(k), pen, period=2.4, duty=0.26)
        for yy in (brow(k), frow(k)):
            out += _poly([(sx - 1.6, yy), (sx + 1.6, yy)], color=pen, f=2000)

    # ======================================================================
    # 3. WELLS
    # ======================================================================
    def kern_pts(P, box, pad=(0.15, 0.72, 0.17, 0.66)):
        ax, ay = P[:, 0], P[:, 1]
        ax = (ax - ax.min()) / (np.ptp(ax) + 1e-12)
        ay = (ay - ay.min()) / (np.ptp(ay) + 1e-12)
        return [(box[0] + pad[0] * (box[2] - box[0]) + pad[1] * (box[2] - box[0]) * float(a),
                 box[1] + pad[2] * (box[3] - box[1]) + pad[3] * (box[3] - box[1]) * float(b))
                for a, b in zip(ax, ay)]

    def norm_w(v, lo=0.42):
        v = np.asarray(v, float)
        return lo + (1 - lo) * (v - v.min()) / (np.ptp(v) + 1e-12)

    hf = (fb1 - fb0) * 0.148
    hb = (bb1 - bb0) * 0.140
    XQ = (x0 + 0.120 * W, x0 + 0.300 * W)
    XK = (x0 + 0.074 * W, x0 + 0.322 * W)
    XV = (x0 + 0.098 * W, x0 + 0.312 * W)

    wells = {}
    for reg, rowf, hh, sc in ((0, frow, hf, 1.0), (1, brow, hb, 0.80)):
        bQ = (XQ[0], rowf(IQ) - hh, XQ[1], rowf(IQ) + hh)
        bK = (XK[0], rowf(IK) - hh, XK[1], rowf(IK) + hh)
        bV = (XV[0], rowf(IV) - hh, XV[1], rowf(IV) + hh)
        uq = (float(qv[0]), float(qv[1])) if reg == 0 else (float(dqv[0]), float(dqv[1]))
        cq, nq = _well_dipole(bQ, uq, blu, 2.15, 0.60 * sc, n=6)
        Kmat = Kp if reg == 0 else dKp
        Kw = norm_w(np.linalg.norm(M.K if reg == 0 else M.dK, axis=1))
        ck, nkp = _well_modes(bK, kern_pts(Kmat, bK), Kw, blk, 2.10, 0.56 * sc, n=7)
        Vr = (Vs if reg == 0 else dVs)[:, 0]
        Vt = (Vs if reg == 0 else dVs)[:, 1]
        Vr = Vr / (np.abs(Vr).max() + 1e-12)
        Vt = 0.55 * Vt / (np.abs(Vt).max() + 1e-12)
        cv, nv = _well_strata(bV, list(Vr), list(Vt), red, 1.95, 0.58 * sc, n=7)
        out += cq + ck + cv
        kpts = kern_pts(Kmat, bK)
        vext = np.abs(Vr) / (np.abs(Vr).max() + 1e-12)
        vlam = [(bV[0] + (bV[2] - bV[0]) * (0.52 + 0.46 * float(vext[j])),
                 bV[1] + (bV[3] - bV[1]) * (j + 0.5) / T) for j in range(T)]
        wells[(reg, IQ)] = (bQ, nq, [nq] * T)
        wells[(reg, IK)] = (bK, nkp, kpts)
        wells[(reg, IV)] = (bV, nv, vlam)

    node = {}
    for reg in (0, 1):
        for k, pen in ((IV, red), (IK, blk), (IQ, blu)):
            box, n_, srcs = wells[(reg, k)]
            out += _sq(n_[0], n_[1], 1.45 if reg == 0 else 1.25, pen)
            node[(reg, k)] = n_
            node[(reg, k, "src")] = srcs

    out += _text("Q", x_lab, frow(IQ) - 3.4, 9.5, blu)
    out += _text("K", x_lab, frow(IK) - 3.4, 9.5, blk)
    out += _text("V", x_lab, frow(IV) - 3.4, 9.5, red)
    for k, name, pen in ((IV, "V", red), (IK, "K", blk), (IQ, "Q", blu)):
        out += _frac("∂L", "∂" + name, x_lab, brow(k), 3.9, pen)

    # ======================================================================
    # 4. SIMILARITY — the real score matrix.  Query indexes the COLUMNS,
    #    key indexes the ROWS, so the key axis is the SAME vertical axis all
    #    the way to Z and the whole plate flows left to right.  The causal
    #    mask leaves the lower-left triangle empty; that void is real.
    # ======================================================================
    lw, lh = 0.118 * W, 0.292 * H
    lcy = fb0 + 0.500 * (fb1 - fb0)
    lpx, lpy = lw / (T - 1), lh / (T - 1)

    def lx(i):
        return x_sim - lw / 2 + lpx * i

    def lyk(j):
        return lcy + lh / 2 - lpy * j

    smax = float(np.abs(S[M.mask]).max())
    for i in range(T):
        for j in range(i + 1):
            r = TIP * 0.52 + 1.10 * (abs(S[i, j]) / smax) ** 0.66
            out += _blob(lx(i), lyk(j), r, blu if i == q else blk)
    # Q selects a column: mark it
    cxr = lx(q) - lpx * 0.50
    out += _poly([(cxr, lyk(0) + 5.0), (cxr, lyk(q) - 4.0)], color=blu, f=2200)
    for yy in (lyk(0) + 5.0, lyk(q) - 4.0):
        out += _poly([(cxr, yy), (lx(q) + lpx * 0.42, yy)], color=blu, f=2200)

    # ======================================================================
    # 5. SOFTMAX — the real normalised row.  Teeth RIGHT = the focus
    #    distribution (sums to 1.000000); teeth LEFT = the other fourteen
    #    rows of the same head, quiet.
    # ======================================================================
    ch = 0.150 * H
    ccy = lcy
    kp = ch / (T - 1)

    def ky(j):
        return ccy + ch / 2 - kp * j

    TOOTH = 0.112 * W
    BACKT = 0.034 * W
    brush = [i for i in range(T) if i != q]
    for n_, i in enumerate(brush):
        lane = kp * (0.30 if n_ % 2 == 0 else -0.30)
        dy = lane + (n_ // 2 - 3.25) * (kp * 0.062)
        for j in range(i + 1):
            L = BACKT * float(A[i, j])
            if L < TIP:
                continue
            out += _poly([(x_sft, ky(j) + dy), (x_sft + L, ky(j) + dy)], color=blk, f=2200)

    tip_x = []
    for j in range(nk):
        a = float(row[j])
        yy, L = ky(j), TOOTH * a
        passes = 1 + (a > 0.02) + (a > 0.06) + (a > 0.12) + 2 * (a > 0.30)
        for p_ in range(passes):
            off = (p_ - (passes - 1) / 2) * 0.36
            out += _poly([(x_sft, yy + off), (x_sft + max(L, TIP), yy + off)], color=blu, f=2000)
        out += _blob(x_sft, yy, TIP * 0.55 + 1.35 * math.sqrt(a), blu)
        tip_x.append(x_sft + max(L, TIP))
    jmax = int(np.argmax(row))
    out += _text("a = 0.5024", x_sft + 2.6, ky(0) + 5.6, 2.4, blu)
    out += _poly([(x_sft + 1.0, ky(0) + 4.6), (tip_x[jmax], ky(0) + 4.6)], color=blu, f=2200)

    # ======================================================================
    # 6. THE WAIST — softmax annealed from tau = 30 to tau = 1.  A strand's
    #    ribbon half-width at every x is the probability that score carries
    #    at that temperature, so the thirteen equal ribbons that leave the
    #    lattice arrive as one fat strand and twelve hairlines.  Edges are
    #    dropped where the ribbon closes under the pen: that is the
    #    information being destroyed, and it is exact.
    # ======================================================================
    HALF_MAX = kp * 0.58          # capped so the winner cannot swallow its
    TAU_HI = 30.0                 # neighbours; the reading is the CLOSING
    span = x_sft - lx(q)
    for j in range(nk):
        src = (lx(q) + 2.4, lyk(j))
        dst = (x_sft - 0.6, ky(j))
        base = _bez(src, (src[0] + span * 0.48, src[1]),
                    (dst[0] - span * 0.48, dst[1]), dst, n=34)
        n = len(base)
        wj = [float(_anneal(logits, max(1.0, math.exp(math.log(TAU_HI) * (1.0 - t / (n - 1)))))[j])
              for t in range(n)]
        w0 = 1.0 / nk
        halves = [min(HALF_MAX, HALF_MAX * w / w0) for w in wj]
        out += _poly(base, color=blk, f=2200)
        for off in (-1.0, 1.0):
            pts = []
            for t, (px_, py_) in enumerate(base):
                if halves[t] < TIP * 0.75:
                    break
                pts.append((px_, py_ + halves[t] * off))
            if len(pts) >= 3:
                out += _poly(pts, color=blk, f=2200)

    # ======================================================================
    # 7. Q SELECTS A COLUMN (it drops onto column 12 from above);
    #    K LANDS ON THE CAUSAL DIAGONAL (key j first exists at token j).
    # ======================================================================
    nq = node[(0, IQ)]
    thr = (lx(q), lyk(0) + 5.2)
    NQR = 7
    for k in range(NQR):
        o = (k - (NQR - 1) / 2) / ((NQR - 1) / 2)
        s0 = (nq[0], nq[1] + o * 5.0)
        dst = (thr[0] + o * 2.6, thr[1])
        out += _poly(_bez(s0, (s0[0] + 0.34 * (dst[0] - s0[0]), s0[1] + o * 6.0),
                          (dst[0] - 0.34 * (dst[0] - s0[0]), dst[1] + 6.0 + o * 3.0),
                          dst, n=30), color=blu, f=2200)
    out += _poly([(thr[0] - 3.4, thr[1]), (thr[0] + 3.4, thr[1])], color=blu, f=2200)

    # K: every key leaves its OWN kernel, so the projection's ordering shows
    # as a braid near the well; the strands settle onto their rows early and
    # run clean into the causal diagonal.
    ksrc = node[(0, IK, "src")]
    kneck = (lx(0) - 0.150 * W, lcy)
    for j in range(T):
        o = (j - (T - 1) / 2) * 0.55
        dst = (lx(j) - lpx * 0.55, lyk(j))
        out += _poly(_through(ksrc[j], kneck, dst, o, n=40), color=blk, f=2200)

    # ======================================================================
    # 8. V BYPASSES THE SCORE — V never meets Q or K.  It sweeps under both
    #    earlier stations and only joins the flow at the softmax axis.
    # ======================================================================
    wh = 0.104 * H
    wkp = wh / (T - 1)

    def wy(j):
        return ccy + wh / 2 - wkp * j

    vsrc = node[(0, IV, "src")]
    dip = fb0 + 0.016 * H
    for j in range(T):
        a = float(A[q, j]) if j < nk else 0.0
        s0 = vsrc[j]
        dst = (x_wv - 0.8, wy(j))
        vneck = (0.44 * s0[0] + 0.56 * dst[0], dip)
        pts = _through(s0, vneck, dst, (j - (T - 1) / 2) * 0.48, n=44)
        for p_ in range(1 + (a > 0.30)):
            out += _poly([(px_, py_ + 0.32 * p_) for px_, py_ in pts], color=red, f=2200)

    # ======================================================================
    # 9. WEIGHTED VALUES -> Z.  Ink passes are the attention weight: Z is a
    #    convex combination and the strand widths say so.
    # ======================================================================
    zn = (x_Z, ccy)
    for j in range(nk):
        a = float(row[j])
        src = (tip_x[j] + 1.4, ky(j))
        dst = (x_wv - 0.8, wy(j))
        pts = _bez(src, (src[0] + 0.50 * (dst[0] - src[0]), src[1]),
                   (dst[0] - 0.42 * (dst[0] - src[0]), dst[1]), dst, n=26)
        passes = 1 + (a > 0.10) + (a > 0.30)
        for p_ in range(passes):
            out += _poly([(ax, ay + 0.32 * (p_ - (passes - 1) / 2)) for ax, ay in pts],
                         color=blu, f=2200)
    for j in range(nk):
        a = float(row[j])
        out += _blob(x_wv, wy(j), TIP * 0.55 + 0.90 * math.sqrt(a), red)
        src = (x_wv + 1.0, wy(j))
        pts = _bez(src, (src[0] + 0.52 * (zn[0] - src[0]), src[1]),
                   (zn[0] - 0.30 * (zn[0] - src[0]), zn[1]), zn, n=30)
        passes = 1 + (a > 0.04) + (a > 0.10) + (a > 0.30)
        for p_ in range(passes):
            out += _poly([(ax, ay + 0.34 * (p_ - (passes - 1) / 2)) for ax, ay in pts],
                         color=red, f=2200)
    out += _sq(zn[0], zn[1], 1.9, blk)
    out += _text("Z", zn[0] + 4.2, zn[1] - 3.0, 9.0, blk)
    out += _poly([(zn[0] + 4.6, zn[1] + 11.0), (zn[0] + 4.6, zn[1] + 26.0)], color=blk, f=2200)

    # ======================================================================
    # 10. BACKWARD REGISTER — the same stations, the arrows reversed
    # ======================================================================
    dzn = (x_Z, brow(IK))
    out += _sq(dzn[0], dzn[1], 1.6, blk)
    out += _frac("∂L", "∂Z", dzn[0] + 4.2, dzn[1], 4.2, blk)

    bch = (bb1 - bb0) * 0.58
    bccy = (bb0 + bb1) / 2
    bkp = bch / (T - 1)

    def bky(j):
        return bccy + bch / 2 - bkp * j

    BT = 0.070 * W
    for j in range(nk):
        a = float(row[j])
        yy = bky(j)
        passes = 1 + (a > 0.04) + (a > 0.10) + (a > 0.30)
        for p_ in range(passes):
            off = (p_ - (passes - 1) / 2) * 0.32
            out += _poly([(x_sft - max(BT * a, TIP), yy + off), (x_sft, yy + off)],
                         color=red, f=2000)
        out += _blob(x_sft, yy, TIP * 0.55 + 0.90 * math.sqrt(a), red)

    for j in range(nk):
        a = float(row[j])
        dst = (x_sft + 0.8, bky(j))
        pts = _bez(dzn, (dzn[0] - 0.48 * (dzn[0] - x_wv), dzn[1]),
                   (dst[0] + 0.54 * (x_wv - dst[0]), dst[1]), dst, n=32)
        passes = 1 + (a > 0.10) + (a > 0.30)
        for p_ in range(passes):
            out += _poly([(bx2, by2 + 0.30 * (p_ - (passes - 1) / 2)) for bx2, by2 in pts],
                         color=red, f=2200)
        out += _arrow_on(pts, 0.62, 1.8, red)

    dvsrc = node[(1, IV, "src")]
    for j in range(nk):
        a = float(row[j])
        ndv = dvsrc[j]
        src = (x_sft - max(BT * a, TIP) - 1.0, bky(j))
        dvneck = (0.46 * src[0] + 0.54 * ndv[0], bb0 + 0.012 * H)
        pts = _through(src, dvneck, ndv, (j - (nk - 1) / 2) * 0.42, n=40)
        for p_ in range(1 + (a > 0.30)):
            out += _poly([(px_, py_ + 0.30 * p_) for px_, py_ in pts], color=red, f=2200)
        out += _arrow_on(pts, 0.40, 1.7, red)

    # dL/dS: the same triangle, signed — blob = positive, tick = negative
    blw, blh = 0.104 * W, (bb1 - bb0) * 0.86
    blcy = bccy
    bpx, bpy = blw / (T - 1), blh / (T - 1)

    def blx(i):
        return x_sim - blw / 2 + bpx * i

    def blyk(j):
        return blcy + blh / 2 - bpy * j

    # gradients span orders of magnitude, so the ladder is set by the 92nd
    # percentile, not the max: one outlier otherwise crushes the whole field
    dsm = float(np.percentile(np.abs(dS[M.mask]), 92)) or 1.0
    for i in range(T):
        for j in range(i + 1):
            v = float(dS[i, j])
            m_ = min(1.25, abs(v) / dsm)
            pen = blu if i == q else blk
            if v >= 0:
                out += _blob(blx(i), blyk(j), TIP * 0.52 + 0.88 * m_ ** 0.62, pen)
            else:
                h_ = 0.55 + 1.15 * m_ ** 0.62
                out += _poly([(blx(i), blyk(j) - h_), (blx(i), blyk(j) + h_)],
                             color=pen, f=1800)

    # softmax Jacobian: the comb back into the focus column
    for j in range(nk):
        src = (x_sft - max(BT * float(row[j]), TIP) - 1.0, bky(j))
        dst = (blx(q) + bpx * 0.5, blyk(j))
        pts = _bez(src, (src[0] - 0.50 * (src[0] - dst[0]), src[1]),
                   (dst[0] + 0.50 * (src[0] - dst[0]), dst[1]), dst, n=26)
        out += _poly(pts, color=blu, f=2200)
        out += _arrow_on(pts, 0.52, 1.7, blu)

    # dL/dS -> dL/dQ (off the column) and -> dL/dK (off the causal diagonal)
    dqn = node[(1, IQ)]
    bthr = (blx(q) + 1.0, blyk(0) + 5.6)
    for j in range(nk):
        o = (j - (nk - 1) / 2) / ((nk - 1) / 2)
        src = (blx(q) + bpx * 0.36, blyk(j))
        d_ = (bthr[0] + o * 5.2, bthr[1])
        out += _poly(_bez(src, (src[0] + 4.0 + (nk - j) * 0.85, src[1]),
                          (d_[0] + 3.0 + abs(o) * 5.0, d_[1] - 5.0 - (nk - j) * 0.5),
                          d_, n=24), color=blu, f=2200)
    out += _poly([(bthr[0] - 6.0, bthr[1]), (bthr[0] + 6.0, bthr[1])], color=blu, f=2200)
    NBR = 7
    for k in range(NBR):
        o = (k - (NBR - 1) / 2) / ((NBR - 1) / 2)
        s0 = (bthr[0] + o * 2.4, bthr[1])
        d_ = (dqn[0], dqn[1] + o * 4.2)
        pts = _bez(s0, (s0[0] - 0.34 * (s0[0] - d_[0]), s0[1] + 5.0 + o * 2.0),
                   (d_[0] + 0.34 * (s0[0] - d_[0]), d_[1] + o * 5.0), d_, n=30)
        out += _poly(pts, color=blu, f=2200)
        out += _arrow_on(pts, 0.48, 1.7, blu)
    dksrc = node[(1, IK, "src")]
    for j in range(T):
        dkn = dksrc[j]
        src = (blx(j) - bpx * 0.55, blyk(j))
        dkneck = (blx(0) - 0.130 * W, blcy)
        pts = _through(src, dkneck, dkn, (j - (T - 1) / 2) * 0.42, n=40)
        out += _poly(pts, color=blk, f=2200)
        out += _arrow_on(pts, 0.50, 1.6, blk)

    # ======================================================================
    # 11. TYPE IN THE QUIET BAND between the registers
    # ======================================================================
    gy = (bb1 + fb0) / 2
    tx = x0 + 0.042 * W
    out += _poly([(tx - 3.2, gy + 8.2), (tx - 3.2, gy - 7.4)], color=blk, f=2200)
    out += _text("sum a = 1.000000   max a = 0.5024 at key 11", tx, gy + 5.4, 2.3, blu)
    out += _text("softmax keeps the order and destroys the scale", tx, gy + 1.0, 2.3, blk)
    out += _text("∂L/∂V = A' ∂L/∂Z    the same weights, transposed", tx, gy - 3.4, 2.3, red)

    rt = "backpropagate"
    rw = _tw(rt, 2.4, True)
    rx = x_Z + 2.0 - rw
    out += _text(rt, rx, gy + 2.4, 2.4, blk, spaced=True)
    out += _text("gradients", rx + rw - _tw("gradients", 2.4, True), gy - 2.0, 2.4,
                 blk, spaced=True)
    out += _poly([(rx + rw + 2.6, gy + 6.6), (rx + rw + 2.6, gy - 4.2)], color=blk, f=2200)

    prov = "gpt2  layer 1  head 0  query 12  |  15 tokens  |  d = 64"
    out += _text(prov, x0 + 0.042 * W, y_axis - 6.0, 1.9, blk)

    return out
