"""INTERFERENCE FIELD — superposition r03 (abstract thesis, parent r01).

One real attention head, GPT-2 small layer 5 head 5, reading a sentence that
comes back:  "Every wave that comes back meets itself." twice (16 tokens).

The plate keeps r01's vertical rhythm  K / Q -> field -> softmax -> V -> Z
but collapses the pipeline into the one element that carries it, the field:

* K ruler (blue, top) and Q ruler (red, left): the head's four principal
  key / query channels, i.e. the rank-1 factors of S = QK^T/8 from its SVD
  (S = sum_r q_r k_r^T; the four drawn modes hold 91 % of S's energy).  Each
  channel is a natural cubic spline through its 16 token values, so a curve
  passes EXACTLY through the data at every token tick.
* The field (black): the causal attention A = softmax(S + mask), every entry,
  blended onto the sheet with an isotropic Gaussian kernel (sigma in mm) and
  contoured on a Gaussian ladder: ring k is the level exp(-(k p)^2 / 2 s^2),
  so an eye of weight 1 has rings exactly p mm apart and an eye of weight a
  loses its innermost  sqrt(2 ln(1/a)) s / p  rings.  Ring count IS weight.
  The masked future (key > query) is blank paper, cut by the causal knife.
* The section (black): the field is cut through its last query row (row 15);
  the softmax row under it is that row's profile, sum_j A_15j k(u - u_j) with
  the field's own kernel, so each bell is exactly as wide as its eye above.
* V chords (ochre): each value vector v_j in the uncentred top-3 principal
  basis of V (78 % of its energy), written as a superposition of 3 Gaussian
  bumps with heights c_jr.  Uncentred so the sink's near-empty v_0 draws flat.
* Z (green): z = sum_j A_15j v_j.  The chord map is linear, so Z's chord is
  EXACTLY sum_j A_15j chord_j (drawn at 4x); the two connectors are dashed
  with duty = A_15j (a key under 6 % rounds to no dash at a 5 mm period).

Nothing here is random: the seed is unused (all data is the forward pass in
``gpt2_head.npz``, written by ``mechanism.py`` beside this file).
"""

from __future__ import annotations

import math
import os
from typing import Dict, List, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import HalfPlane, clip
from promptplot.generative.engine.kit import _GLYPHS, _poly, circle
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

HERE = os.path.dirname(os.path.abspath(__file__))

# pens, in plotting order (light -> dark; dark ink lands last)
OCHRE, BLUE, RED, GREEN, BLACK, TYPE = 0, 1, 2, 3, 4, 5

N_MODES = 4          # SVD modes drawn on each ruler
N_VPC = 3            # principal components in each V / Z glyph


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------


def _load() -> Dict[str, np.ndarray]:
    d = np.load(os.path.join(HERE, "gpt2_head.npz"))
    out = {k: d[k] for k in d.files}
    for k in "QKVAZ":
        out[k] = out[k].astype(np.float64)
    return out


def _cardinal(n: int, ts: np.ndarray) -> np.ndarray:
    """Natural cubic spline cardinal basis C[t, i]: sum_i C[t,i] y_i is the
    natural spline through (i, y_i), exact at every integer i."""
    A = np.zeros((n, n))
    A[0, 0] = A[-1, -1] = 1.0
    for i in range(1, n - 1):
        A[i, i - 1:i + 2] = [1.0, 4.0, 1.0]
    j = np.clip(np.floor(ts), 0, n - 2).astype(int)
    u = ts - j
    out = np.zeros((len(ts), n))
    for i in range(n):
        y = np.zeros(n)
        y[i] = 1.0
        rhs = np.zeros(n)
        rhs[1:-1] = 6.0 * (y[2:] - 2.0 * y[1:-1] + y[:-2])
        M = np.linalg.solve(A, rhs)
        out[:, i] = ((1 - u) * y[j] + u * y[j + 1]
                     + ((1 - u) ** 3 - (1 - u)) * M[j] / 6.0
                     + (u ** 3 - u) * M[j + 1] / 6.0)
    return out


# ---------------------------------------------------------------------------
# sheet layout (all mm; t measured DOWN from the drawable top)
# ---------------------------------------------------------------------------


class _Sheet:
    def __init__(self, bounds: Bounds, n: int):
        self.x0, self.y0, self.x1, self.y1 = bounds
        self.W, self.H = self.x1 - self.x0, self.y1 - self.y0
        self.n = n
        # field box: key axis across, query axis down
        self.uf0, self.uf1 = 36.0, self.W - 6.0
        self.tf0 = 38.0
        self.px = (self.uf1 - self.uf0) / n          # mm per key token
        self.py = self.px                              # square token cells: the knife is 45 deg
        self.tcut = self.ty(n - 1)                     # the section: last query row
        # rulers: one lane per SVD mode, mode 1 nearest the field
        self.lane = 6.2
        self.tk = [24.5 - r * self.lane for r in range(N_MODES)]
        self.uq = [21.6 - r * self.lane for r in range(N_MODES)]
        # coda
        self.ul = self.ux(0) - 13.0                    # shared left edge of the coda
        self.tsm = self.tcut + 21.0                    # softmax baseline
        self.tv = self.tsm + 23.0                      # V baseline
        self.tz = self.tv + 36.0                       # Z baseline

    # token coordinate -> sheet mm
    def ux(self, x: float) -> float:
        return self.uf0 + (x + 0.5) * self.px

    def ty(self, y: float) -> float:
        return self.tf0 + (y + 0.5) * self.py

    def P(self, u: float, t: float) -> Pt:
        return (self.x0 + u, self.y1 - t)

    def knife_pts(self) -> List[Pt]:
        """Causal boundary x = y + 1/2 (cell-inclusive: key <= query), from the
        top of the field to the section cut."""
        return [(self.ux(0.0), self.ty(-0.5)), (self.ux(self.n - 0.5), self.tcut)]

    def knife(self):
        (ua, ta), (ub, tb) = self.knife_pts()
        a = (ub - ua) / (tb - ta)
        # inside: u - ua - a (t - ta) <= 0
        return HalfPlane(1.0, -a, -ua + a * ta)


def _E(S: _Sheet, pts_ut: Sequence[Pt], pen: int, f: int = 1800) -> List[GCodeCommand]:
    return _poly([S.P(u, t) for u, t in pts_ut], color=pen, f=f)


def _dashed(S: _Sheet, pts_ut: Sequence[Pt], pen: int, period: float, duty: float,
            f: int = 1800) -> List[GCodeCommand]:
    """Dashes of length duty*period every period mm along a (u,t) polyline."""
    dash = duty * period
    if dash < 0.3:
        return []
    out: List[GCodeCommand] = []
    pts = np.asarray(pts_ut, float)
    seg = np.hypot(*np.diff(pts, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    L = cum[-1]
    s = 0.0
    while s + dash <= L + 1e-9:
        ss = np.linspace(s, s + dash, max(2, int(dash / 0.5) + 2))
        uu = np.interp(ss, cum, pts[:, 0])
        tt = np.interp(ss, cum, pts[:, 1])
        out += _E(S, list(zip(uu, tt)), pen, f)
        s += period
    return out


# ---------------------------------------------------------------------------
# the field
# ---------------------------------------------------------------------------


def _contour_lines(F: np.ndarray, xs: np.ndarray, ys: np.ndarray, level: float):
    try:
        import contourpy

        gen = contourpy.contour_generator(xs, ys, F, line_type="Separate")
        return [np.asarray(p) for p in gen.lines(level)]
    except ImportError:  # pragma: no cover - kit fallback
        from promptplot.generative.engine.kit import _chain_segments, _marching_squares

        segs = _marching_squares(F.tolist(), list(xs), list(ys), level)
        return [np.asarray(c) for c in _chain_segments(segs)]


def _field(S: _Sheet, A: np.ndarray, sigma: float, pitch: float, floor: float):
    """Kernel-blended causal attention, contoured on a Gaussian ladder.

    Returns (polylines in (u, t) mm, stats)."""
    n = S.n
    step = 0.2
    reach = sigma * math.sqrt(2.0 * math.log(1.0 / floor)) + 1.0
    us = np.arange(S.ux(0) - reach, S.uf1 + step, step)
    ts = np.arange(S.ty(0) - reach, S.tcut + step, step)
    # kernel in mm so eyes are round on paper whatever px / py are
    ku = np.exp(-0.5 * ((us[:, None] - np.array([S.ux(j) for j in range(n)])[None, :]) / sigma) ** 2)
    kt = np.exp(-0.5 * ((ts[:, None] - np.array([S.ty(i) for i in range(n)])[None, :]) / sigma) ** 2)
    FA = kt @ np.tril(A) @ ku.T                     # FA[t, u]
    kmax = int(math.floor(sigma * math.sqrt(2.0 * math.log(1.0 / floor)) / pitch))
    # ladder scaled to the TRUE maximum: summed neighbours lift the sink ridge
    # to ~1.12, and a ladder built for a peak of 1 pinched its crest rings to
    # 0.7 mm.  Against the max, every lower peak a has gaps >= pitch (r_k =
    # sqrt((k p)^2 - 2 s^2 ln(max/a)) spreads, never tightens).
    top = float(FA.max())
    kmax = int(math.floor(sigma * math.sqrt(2.0 * math.log(top / floor)) / pitch))
    levels = [top * math.exp(-((k * pitch) ** 2) / (2.0 * sigma ** 2)) for k in range(1, kmax + 1)]
    polys: List[List[Pt]] = []
    for lv in levels:
        for line in _contour_lines(FA, us, ts, lv):
            if len(line) < 2:
                continue
            for run in clip([tuple(p) for p in line], S.knife(), keep="inside"):
                if len(run) >= 2 and _plen(run) > 0.8:
                    polys.append(run)
    return polys, {"levels": len(levels), "kmax": kmax, "FA_max": float(FA.max()),
                   "grid": FA.shape}


def _plen(run: Sequence[Pt]) -> float:
    p = np.asarray(run)
    return float(np.hypot(*np.diff(p, axis=0).T).sum())


# ---------------------------------------------------------------------------
# rulers
# ---------------------------------------------------------------------------


def _modes(Q: np.ndarray, K: np.ndarray):
    Smat = Q @ K.T / 8.0
    U, s, Vt = np.linalg.svd(Smat)
    qm = U[:, :N_MODES] * np.sqrt(s[:N_MODES])
    km = Vt[:N_MODES].T * np.sqrt(s[:N_MODES])
    for r in range(N_MODES):                     # sign: key channel mostly positive
        if km[:, r].sum() < 0:
            qm[:, r] *= -1.0
            km[:, r] *= -1.0
    energy = float((s[:N_MODES] ** 2).sum() / (s ** 2).sum())
    return qm, km, s, energy


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# type: laid out from MEASURED glyph extents (the shared font's 'i' is drawn
# at x=1.8 but advances 1.1, so it collides with the next letter)
# ---------------------------------------------------------------------------


def _glyph_ext(ch: str):
    strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
    xs = [gx for st in strokes for gx, _ in st]
    if not xs:
        return strokes, 0.0, 0.0
    return strokes, min(xs), max(xs)


def _set_width(text: str, h: float, gap: float = 1.05, space: float = 2.6) -> float:
    sc = h / 6.0
    w = 0.0
    for ch in text:
        if ch == " ":
            w += space * sc
            continue
        _, lo, hi = _glyph_ext(ch)
        w += (hi - lo + gap) * sc
    return w - gap * sc


def _set(S: "_Sheet", text: str, u: float, t: float, h: float, pen: int,
         gap: float = 1.05, space: float = 2.6, f: int = 1500) -> List[GCodeCommand]:
    """(u, t) = left end of the baseline."""
    sc = h / 6.0
    out: List[GCodeCommand] = []
    cu = u
    for ch in text:
        if ch == " ":
            cu += space * sc
            continue
        strokes, lo, hi = _glyph_ext(ch)
        for st in strokes:
            out += _E(S, [(cu + (gx - lo) * sc, t - gy * sc) for gx, gy in st], pen, f)
        cu += (hi - lo + gap) * sc
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def _chord(coef: np.ndarray, s: np.ndarray, w: float) -> np.ndarray:
    """A value vector's principal coordinates as a superposition of Gaussian
    bumps, one per component, w apart (s and w in the same units)."""
    R = len(coef)
    offs = (np.arange(R) - (R - 1) / 2.0) * w
    return sum(coef[r] * np.exp(-0.5 * ((s - offs[r]) / (0.46 * w)) ** 2) for r in range(R))


def superposition_interference_field(rng: SeededRNG, bounds: Bounds, colors: int = 6,
                                     sigma: float = 4.2, pitch: float = 1.15,
                                     floor: float = 0.02) -> List[GCodeCommand]:
    D = _load()
    Q, K, V, A = D["Q"], D["K"], D["V"], D["A"]
    n = A.shape[0]
    S = _Sheet(bounds, n)
    out: List[GCodeCommand] = []

    def pen(p: int) -> int:
        return p if colors > p else p % max(1, colors)

    # ---------------- field (black)
    polys, _st = _field(S, A, sigma, pitch, floor)
    for run in polys:
        out += _E(S, run, pen(BLACK), 1700)
    out += _E(S, S.knife_pts(), pen(BLACK))                           # causal knife
    out += _E(S, [(S.ul, S.tcut), (S.uf1, S.tcut)], pen(BLACK))  # section

    # ---------------- rulers: one lane per mode
    qm, km, sv, energy = _modes(Q, K)
    ts_fine = np.linspace(0.0, n - 1.0, 16 * 24 + 1)
    C = _cardinal(n, ts_fine)
    amp = 3.2 / max(np.abs(qm).max(), np.abs(km).max())     # shared mm/unit
    for r in range(N_MODES):                 # serpentine: alternate lane direction
        kv = C @ km[:, r]
        kp = [(S.ux(x), S.tk[r] - amp * v) for x, v in zip(ts_fine, kv)]
        out += _E(S, kp if r % 2 == 0 else kp[::-1], pen(BLUE))
        qv = C @ qm[:, r]
        qp = [(S.uq[r] + amp * v, S.ty(y)) for y, v in zip(ts_fine, qv)]
        out += _E(S, qp if r % 2 == 0 else qp[::-1], pen(RED))
    a = A[n - 1]
    for j in range(n):                       # key ticks; attended keys ringed
        if a[j] >= 0.05:
            out += circle(*S.P(S.ux(j), S.tk[0] + 4.0), 0.9, pen=pen(BLUE), n=20)
        else:
            out += _E(S, [(S.ux(j), S.tk[0] + 3.4), (S.ux(j), S.tk[0] + 4.6)], pen(BLUE))
    for i in range(n):                       # query ticks; the read-out query ringed
        if i == n - 1:
            out += circle(*S.P(S.uq[0] + 4.0, S.ty(i)), 0.9, pen=pen(RED), n=20)
        else:
            out += _E(S, [(S.uq[0] + 3.4, S.ty(i)), (S.uq[0] + 4.6, S.ty(i))], pen(RED))

    # ---------------- softmax row: the section through row n-1 of A.  One
    # curve: sum_j A_15j * kernel(u - u_j), the field's own sigma, so each
    # attended key is a bell exactly as wide as its eye above.
    hs = 24.0                                   # mm per unit of attention
    us = np.linspace(S.ux(-0.5) - 2.0 * sigma, S.ux(n - 0.5), 700)
    prof = hs * (np.exp(-0.5 * ((us[:, None] - np.array([S.ux(j) for j in range(n)])[None, :])
                                / sigma) ** 2) @ a)
    runs, start = [], None
    for k in range(len(us)):
        on = prof[k] > 0.8
        if on and start is None:
            start = k
        if (not on or k == len(us) - 1) and start is not None:
            runs.append((start, k + (1 if on else 0)))
            start = None
    for lo, hi in runs:
        out += _E(S, [(u, S.tsm - h) for u, h in zip(us[lo:hi], prof[lo:hi])], pen(BLACK))
    out += _E(S, [(S.ul, S.tsm), (S.ux(n - 0.5), S.tsm)], pen(BLACK))
    for j in range(n):
        out += _E(S, [(S.ux(j), S.tsm), (S.ux(j), S.tsm + 1.2)], pen(BLACK))

    # ---------------- V chords and Z
    # uncentred principal basis of V, so a value that is nearly nothing (the
    # sink's v_0, |v_0| = 0.44 |v_8|) draws as nearly nothing
    _u, _s, vt_ = np.linalg.svd(V, full_matrices=False)
    basis = vt_[:N_VPC]
    for r in range(N_VPC):                              # sign: mean coordinate positive
        if (V @ basis[r]).sum() < 0:
            basis[r] = -basis[r]
    coef = V @ basis.T                                  # [n, N_VPC]
    zc = a @ coef                                       # exact: z's coordinates
    w = 0.27 * S.px                                     # bump pitch, mm
    half = (N_VPC - 1) / 2.0 * w + 2.6 * 0.46 * w
    gs = np.linspace(-half, half, 120)
    chords = np.stack([_chord(coef[j], gs, w) for j in range(n)])
    vamp = 9.0 / np.abs(chords).max()                  # mm per unit, shared by V and Z

    def trimmed(pts_c, k):
        vals = np.abs(pts_c)
        keep = np.nonzero(vals * k > 0.8)[0]
        return (keep[0], keep[-1] + 1) if len(keep) else (0, 0)

    out += _E(S, [(S.ul, S.tv), (S.ux(n - 0.5), S.tv)], pen(OCHRE))
    for j in range(n):
        lo, hi = trimmed(chords[j], vamp)
        if hi - lo >= 2:
            out += _E(S, [(S.ux(j) + g, S.tv - vamp * c)
                          for g, c in zip(gs[lo:hi], chords[j][lo:hi])], pen(OCHRE))
    zs = 4.0
    uz = S.uf1 - zs * half - 2.0
    order = np.argsort(-a)
    # (a nested A_8 v_8 partial inside z was tried and cut: it grazed z under 0.8 mm)
    zcurve = _chord(zc, gs, w)
    lo, hi = trimmed(zcurve, zs * vamp)
    out += _E(S, [(uz + zs * g, S.tz - zs * vamp * c)
                  for g, c in zip(gs[lo:hi], zcurve[lo:hi])], pen(GREEN))
    out += _E(S, [(uz - zs * half - 4.0, S.tz), (uz + zs * half + 4.0, S.tz)], pen(GREEN))

    # connectors V_j -> Z, dashed with duty = A_j
    ztop = S.tz - zs * vamp * max(0.0, zcurve.max()) - 2.5
    uzp = uz + zs * gs[int(np.argmax(zcurve))]          # land on z's crest
    drawn = [j for j in order if a[j] * 5.0 >= 0.3]
    for k, j in enumerate(sorted(drawn, key=lambda jj: S.ux(jj))):
        u0, t0 = S.ux(j), S.tv + 4.0
        u1 = uzp + (k - (len(drawn) - 1) / 2.0) * 3.2      # separate landing points
        run_t = 0.5 * (t0 + ztop)
        pts = _bez((u0, t0), (u0, run_t), (u1, run_t), (u1, ztop), 90)
        out += _dashed(S, pts, pen(OCHRE), period=5.0, duty=float(a[j]))

    # ---------------- caption (own layer)
    line = str(D["text"])
    first = line[: len(line) // 2].strip()
    cu, ct = S.ul, S.tz - 8.0
    for k in range(2):
        out += _set(S, first, cu, ct + k * 5.6, 3.0, pen(TYPE))
    out += _set(S, "GPT-2 small  layer 5  head 5    z = softmax(qKᵀ/8) V", cu, ct + 15.0, 1.9, pen(TYPE))
    return out


def _bez(p0: Pt, p1: Pt, p2: Pt, p3: Pt, n: int = 120) -> List[Pt]:
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1.0 - t
        pts.append((
            mt ** 3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t ** 3 * p3[0],
            mt ** 3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t ** 3 * p3[1],
        ))
    return pts
