"""DIFFUSION — FORWARD, NETWORK, REVERSE.  Three registers, one real process.

Every state on this sheet is a REAL sample from a REAL DDPM, computed in numpy
here.  Nothing is drawn "as if" noised.

    data law      p0 = a 6-component Gaussian mixture (one core + five lobes),
                  standardised to unit per-dimension variance so the process is
                  genuinely variance-preserving.
    schedule      COSINE (Nichol & Dhariwal 2021), s = 0.008, T = 1000:
                      abar(t) = cos^2( ((t/T)+s)/(1+s) * pi/2 ) / f(0)
    forward       x_t = sqrt(abar_t) x0 + sqrt(1-abar_t) eps,  eps ~ N(0, I).
                  One fixed eps per particle across the whole row, so the top
                  register is ONE coupling evolving, not six unrelated draws.
    denoiser      p_t of a Gaussian mixture is EXACTLY a Gaussian mixture, so the
                  score  grad log p_t  is available in closed form and
                      eps_theta(x,t) = -sqrt(1-abar_t) * grad log p_t(x)
                  is the EXACT Bayes-optimal denoiser for this data law.  Not a
                  learned net, but not a stand-in either: it is the function the
                  U-Net is trained to approximate.
    reverse       real DDPM ancestral sampling from FRESH noise (an independent
                  numpy SeedSequence stream), all 1000 steps:
                      x_{t-1} = 1/sqrt(a_t) ( x_t - (1-a_t)/sqrt(1-abar_t) eps )
                                + sqrt(betatilde_t) z
                  The bottom register is therefore a DIFFERENT sample from the
                  same family, not the top row played backwards.

EVERY MARK IN A STATE COMES OUT OF TWO MEASURED FIELDS.  Each state's own
particles are run through a binned Gaussian KDE (one bandwidth for the whole
sheet, so the columns are comparable), giving

        p_hat_t(x)                            the estimated density
        F(x) = log p_hat_t(x) - log q_h(x)    its excess over the prior,

where q_h is the prior SEEN THROUGH THE SAME KERNEL, N(0, (1+h^2) I).  Then:

    * SHAPE       the rings are level sets of p_hat_t.  Those ARE "the data
                  manifold's level sets": one lobed nest that splits into
                  separate eyes only high up, where the modes separate.  Levels
                  are chosen by AREA INVERSION so the ring pitch on paper is
                  constant (DESIGN_RUBRIC craft law -- see _pitch_levels).
    * EXTENT      the outermost ring is the contour that just ENCLOSES everything
                  detectable, {F > floor}, where ``floor`` is measured by running
                  an equal-sized sample of PURE PRIOR NOISE through the same
                  estimator.  So the nest's diameter is a measurement, and it
                  shrinks to nothing on its own: x_T has no rings because there
                  is nothing left to detect.
    * INK         dash duty varies ALONG each ring as clip(F / (0.38 F_REF)): a
                  contour is solid where the state is measurably denser than the
                  prior and frays in the gaps.  Once a dash would carry less than
                  one pen tip of ink it becomes a dot -- so contours become dashes
                  become stipple, and the PEN decides where, not a taste
                  parameter.
    * RELIEF      each ring stands at a height set by its own density level, on a
                  scale fixed once from x0 and shared by every cell, so the mound
                  visibly FLATTENS along the row as the peak density falls.
    * PARTICLES   a particle is inked individually only OUTSIDE the nest, where no
                  contour covers it.  The same 420 indices at every t, so one
                  particle can be followed across the whole row.

DEPTH IS DECLARED: the states are a shear relief of a real surface, hidden-line
tested; the skip arcs pass over the bowtie.  The three registers themselves are
a flat band structure, which is what a sequence wants.

U-NET.  Real DDPM/CIFAR-10 configuration (Ho et al. 2020): resolutions
32/16/8/4 with 128/256/256/256 channels.  ONE DRAWN LINE PER FEATURE-MAP ROW, at
constant pitch, so the envelope height IS the spatial resolution and the bowtie's
8x contraction is the real 32 -> 4 downsample; adjacent rows MERGE IN PAIRS at
each stride-2 step, because that is what a stride-2 convolution does.  Each
level's x-extent is proportional to its channel count (128 : 256 : 256 : 256).
Skips join genuinely mirrored levels and carry channels/128 parallel dashed
strands.

COLOUR IS THE TIME AXIS.  black / blue / purple / pink / crimson.  Both
endpoints -- the data law and the prior -- are black, because both are fixed
structure; the four transit states carry the ramp.  Colour therefore reads as
IN TRANSIT.  The same ramp runs left to right through the U-Net as network
depth, so encoder blue sits under forward blue and decoder crimson under
forward crimson.

Column registration is by t: column k is the SAME abar_t in both rows.  (The
reference plate indexes the bottom row by reverse-step count, which breaks the
top/bottom correspondence; the brief asks for the correspondence, so the labels
follow t.)
"""

from __future__ import annotations

import bisect
import math
from typing import List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import (
    _dot,
    giant_type,
    _poly,
    _spaced,
    _stroke_text,
    _text_width,
    fill_rect,
    plus_mark,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]

# ---------------------------------------------------------------------- schedule
T_STEPS = 1000
COS_S = 0.008

# --------------------------------------------------------------------- estimator
N_PART = 40000          # particles per state (both rows, same estimator).
                        # The estimator's detection floor falls as 1/sqrt(n),
                        # and it is the floor that decides how many rings each
                        # state keeps -- at n = 12000 the floor ate everything
                        # past column 3 (measured: 11/8/6/3/1/0 rings).
N_STIPPLE = 420         # of those, the ones actually inked -- FIXED indices, so
                        # the same particle can be followed across the whole row
KDE_GRID = 160          # binned-KDE / marching-squares grid per state
WIN = 2.45              # cell half-window in data standard deviations

# ------------------------------------------------------------------------ inking
RING_MM = 0.95          # contour pitch on paper (pen tip 0.5)
DASH_MM = 3.2           # dash period
TIP_MM = 0.5            # pen tip; a dash thinner than this becomes a dot
DUTY_REF = 0.30         # a ring is SOLID above this fraction of the data law
                        # peak contrast, and dies where the state becomes
                        # indistinguishable from the prior (F = 0).

# ----------------------------------------------------------------- U-Net (DDPM)
UNET_RES = (32, 16, 8, 4)
UNET_CH = (128, 256, 256, 256)

_TINY = 1e-300

# marching-squares case table: edge pairs (0 bottom, 1 right, 2 top, 3 left)
_MS = {
    1: ((3, 0),), 2: ((0, 1),), 3: ((3, 1),), 4: ((1, 2),),
    5: ((3, 0), (1, 2)), 6: ((0, 2),), 7: ((3, 2),), 8: ((2, 3),),
    9: ((2, 0),), 10: ((0, 1), (2, 3)), 11: ((2, 1),), 12: ((1, 3),),
    13: ((1, 0),), 14: ((0, 3),),
}


# ===========================================================================
# schedule
# ===========================================================================
def _schedule():
    """Cosine schedule, exactly as published: form abar from the cosine, take
    beta_t = 1 - abar_t/abar_{t-1} CLIPPED AT 0.999, then rebuild abar as the
    cumulative product of alpha = 1 - beta.

    The clip is not cosmetic.  The raw cosine gives abar_T = 0 exactly, and an
    ancestral step then divides by sqrt(alpha_T) = 0: the reverse chain blows up
    to ~1e4 (measured before this fix).  Clipping keeps alpha_T = 0.001 and the
    chain finite, and abar_T = 3e-6 is still isotropic noise to any measurement."""
    t = np.arange(T_STEPS + 1, dtype=float)
    f = np.cos(((t / T_STEPS) + COS_S) / (1.0 + COS_S) * (math.pi / 2.0)) ** 2
    raw = f / f[0]
    beta = np.zeros(T_STEPS + 1)
    beta[1:] = np.clip(1.0 - raw[1:] / raw[:-1], 0.0, 0.999)
    alpha = 1.0 - beta
    ab = np.cumprod(alpha)
    ab[0] = 1.0
    return ab, alpha, beta


# ===========================================================================
# data law: a lobed Gaussian mixture, standardised to unit variance per dim
# ===========================================================================
def _data_law(rng: SeededRNG):
    """(w, mu, Sig) of the data mixture.  Irregular on purpose -- a 5-fold
    symmetric rose is student work (DESIGN_RUBRIC dim 3)."""
    gen = np.random.default_rng([rng.seed, 101])
    n_lobe = 5
    w = np.empty(n_lobe + 1)
    mu = np.zeros((n_lobe + 1, 2))
    Sig = np.zeros((n_lobe + 1, 2, 2))

    # core
    # A HEAVY, BROAD CORE is structural, not decorative: it is what lifts the
    # saddles between the lobes above the prior, so the outer level sets close
    # into ONE lobed nest instead of five separate islands.
    w[0] = 0.36
    s_core = 0.50
    Sig[0] = np.diag([s_core ** 2, (s_core * 0.82) ** 2])

    base = gen.uniform(0, 2 * math.pi)
    for k in range(n_lobe):
        a = base + 2 * math.pi * k / n_lobe + gen.uniform(-0.28, 0.28)
        r = 0.95 * gen.uniform(0.80, 1.22)
        s_rad = 0.32 * gen.uniform(0.80, 1.20)
        s_tan = 0.22 * gen.uniform(0.82, 1.20)
        w[k + 1] = 0.128 * gen.uniform(0.72, 1.28)
        mu[k + 1] = (r * math.cos(a), r * math.sin(a))
        R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
        Sig[k + 1] = R @ np.diag([s_rad ** 2, s_tan ** 2]) @ R.T
    w /= w.sum()

    # standardise: zero mean, unit variance per dimension (variance-preserving
    # diffusion is only variance-preserving if the data has unit variance)
    m = (w[:, None] * mu).sum(0)
    mu -= m
    cov = (w[:, None, None] * (Sig + mu[:, :, None] * mu[:, None, :])).sum(0)
    sc = math.sqrt(0.5 * (cov[0, 0] + cov[1, 1]))
    mu /= sc
    Sig /= sc * sc
    return w, mu, Sig


def _sample_data(w, mu, Sig, n, gen) -> np.ndarray:
    idx = gen.choice(len(w), size=n, p=w)
    L = np.linalg.cholesky(Sig)                      # (K,2,2)
    z = gen.standard_normal((n, 2))
    return mu[idx] + np.einsum("nij,nj->ni", L[idx], z)


def _marginal(P, w, mu, Sig, ab: float) -> np.ndarray:
    """EXACT p_t on points P: a Gaussian convolved with a Gaussian mixture is a
    Gaussian mixture.  P (n,2) -> (n,)."""
    sa = math.sqrt(ab)
    C = ab * Sig + (1.0 - ab) * np.eye(2)            # (K,2,2)
    d = P[None, :, :] - sa * mu[:, None, :]          # (K,n,2)
    Ci = np.linalg.inv(C)
    det = np.linalg.det(C)
    q = np.einsum("kni,kij,knj->kn", d, Ci, d)
    return (w[:, None] / (2 * math.pi * np.sqrt(det))[:, None] * np.exp(-0.5 * q)).sum(0)


def _eps_theta(P, w, mu, Sig, ab: float) -> np.ndarray:
    """EXACT Bayes-optimal noise prediction for this data law.

    Written out in 2D closed form rather than via einsum: the reverse chain runs
    T = 1000 ancestral steps on 12000 particles, and the (K,n,2) temporaries of
    the general form cost ten times as much memory traffic as the (K,n) ones."""
    sa = math.sqrt(ab)
    C = ab * Sig + (1.0 - ab) * np.eye(2)
    det = C[:, 0, 0] * C[:, 1, 1] - C[:, 0, 1] * C[:, 1, 0]
    i00, i01 = C[:, 1, 1] / det, -C[:, 0, 1] / det
    i10, i11 = -C[:, 1, 0] / det, C[:, 0, 0] / det
    dx = P[:, 0][None, :] - (sa * mu[:, 0])[:, None]
    dy = P[:, 1][None, :] - (sa * mu[:, 1])[:, None]
    ax = i00[:, None] * dx + i01[:, None] * dy
    ay = i10[:, None] * dx + i11[:, None] * dy
    comp = (w / (2 * math.pi * np.sqrt(det)))[:, None] * np.exp(-0.5 * (ax * dx + ay * dy))
    r = comp / (comp.sum(0) + _TINY)                 # responsibilities (K,n)
    score = np.stack([-(r * ax).sum(0), -(r * ay).sum(0)], 1)   # grad log p_t
    return -math.sqrt(max(1.0 - ab, 1e-12)) * score


# ===========================================================================
# estimator: binned Gaussian KDE + gradient-stepped contour levels
# ===========================================================================
def _kde(P: np.ndarray, h: float, ng: int, win: float):
    """Binned Gaussian KDE.  Binning + a separable Gaussian applied as two
    matrix products -- exact on the bin grid, and O(ng^3) instead of O(n*ng^2),
    so the particle count is free."""
    edges = np.linspace(-win, win, ng + 1)
    xs = 0.5 * (edges[:-1] + edges[1:])
    H, _, _ = np.histogram2d(P[:, 1], P[:, 0], bins=[edges, edges])   # [j=y, i=x]
    d = xs[:, None] - xs[None, :]
    K = np.exp(-0.5 * (d / h) ** 2)
    dens = K @ H @ K.T
    cell = xs[1] - xs[0]
    dens /= (2 * math.pi * h * h) * len(P) / (cell * cell) * (cell * cell)
    dens /= max(dens.sum() * cell * cell, 1e-30)     # normalise to a density
    return dens, xs


def _log_null(xs: np.ndarray, h: float) -> np.ndarray:
    """log of the PRIOR AS THIS ESTIMATOR SEES IT.

    A Gaussian KDE of bandwidth h inflates the estimate's covariance by h^2, so
    comparing p_hat against a bare N(0, I) makes an oversmoothed estimate look
    FATTER than the prior and the contrast F blows up in the tails instead of
    vanishing (measured: F_max rose from 1.10 to 1.77 over the last three
    columns, i.e. the row un-collapsed).  The correct null is N(0, (1+h^2) I) --
    the prior run through the same kernel."""
    v = 1.0 + h * h
    r2 = xs[None, :] ** 2 + xs[:, None] ** 2
    return -math.log(2 * math.pi * v) - r2 / (2.0 * v)


def _noise_floor(n: int, h: float, ng: int, win: float, gen, reps: int = 5) -> float:
    """The contrast a sample of PURE PRIOR NOISE produces through this exact
    estimator -- the detection floor.

    A finite KDE always fluctuates, so F = log p_hat - log null is never exactly
    zero even when the state IS the prior; drawing rings down to F = 0 therefore
    fills the last columns with contoured sampling noise (measured on v1: x_T
    came out as a dotted rectangle filling the frame).  Calibrate against the
    null instead: run n draws from N(0, I) through the same bandwidth and take
    the peak contrast.  Structure below that is not structure."""
    peak = 0.0
    for _ in range(reps):
        Z = gen.standard_normal((n, 2))
        d, xs = _kde(Z, h, ng, win)
        peak = max(peak, float(np.max(np.log(np.maximum(d, _TINY)) - _log_null(xs, h))))
    return peak


def _pitch_levels(G: np.ndarray, cell: float, pitch: float, r_out: float):
    """Levels of ``G`` whose RINGS sit exactly ``pitch`` apart on the page,
    starting from the one that encloses an equivalent radius of ``r_out``.

    DESIGN_RUBRIC's craft law is that contour PITCH, not contour value, must be
    constant -- otherwise the nest floods where the field is steep.  The kit's
    gradient-quantile version of that rule is calibrated on |grad G| and is the
    wrong tool here: on a log-density the 82nd-percentile gradient is set by the
    lobe walls and by estimator noise, and sizing the step by it yields ONE ring
    for the whole nest (measured).

    So invert the AREA instead: A(L) is the area enclosed above level L and the
    equivalent radius is sqrt(A/pi).  Pick the levels whose equivalent radii
    differ by exactly ``pitch``.  Same law, computed on the geometry it is
    actually about, and robust to estimator noise because an area is an
    integral."""
    gmax = float(G.max())
    if gmax <= 0 or r_out < pitch:
        return []
    L = np.linspace(0.0, gmax, 400)
    area = (G[None, :, :] > L[:, None, None]).sum(axis=(1, 2)) * cell * cell
    req = np.sqrt(np.maximum(area, 0.0) / math.pi)   # decreasing in L
    out = []
    k = 0
    while True:
        r = r_out - k * pitch
        if r < pitch * 0.8 or k > 60:
            break
        i = int(np.searchsorted(-req, -r))
        i = min(max(i, 1), len(L) - 1)
        r0, r1 = float(req[i - 1]), float(req[i])
        t = 0.0 if r0 == r1 else (r0 - r) / (r0 - r1)
        out.append(float(L[i - 1] + (L[i] - L[i - 1]) * t))
        k += 1
    return out


def _iso_runs(F: np.ndarray, xs: np.ndarray, iso: float):
    """Vectorised marching squares -> chained polylines."""
    v0, v1 = F[:-1, :-1], F[:-1, 1:]
    v2, v3 = F[1:, 1:], F[1:, :-1]
    case = ((v0 > iso).astype(np.uint8) | ((v1 > iso).astype(np.uint8) << 1)
            | ((v2 > iso).astype(np.uint8) << 2) | ((v3 > iso).astype(np.uint8) << 3))
    if not case.any():
        return []
    shp = case.shape
    X0 = np.broadcast_to(xs[:-1][None, :], shp)
    X1 = np.broadcast_to(xs[1:][None, :], shp)
    Y0 = np.broadcast_to(xs[:-1][:, None], shp)
    Y1 = np.broadcast_to(xs[1:][:, None], shp)

    def lp(a, b, va, vb):
        den = np.where(vb == va, 1e-30, vb - va)
        return a + (b - a) * ((iso - va) / den)

    EX = (lp(X0, X1, v0, v1), X1, lp(X0, X1, v3, v2), X0)
    EY = (Y0, lp(Y0, Y1, v1, v2), Y1, lp(Y0, Y1, v0, v3))

    segs = []
    for c, pairs in _MS.items():
        sel = case == c
        if not sel.any():
            continue
        for ea, eb in pairs:
            ax, ay = EX[ea][sel], EY[ea][sel]
            bx, by = EX[eb][sel], EY[eb][sel]
            segs.extend(zip(zip(ax.tolist(), ay.tolist()), zip(bx.tolist(), by.tolist())))
    return _chain(segs)


def _chain(segs, tol: float = 1e-7):
    """Join segments into polylines by exact endpoint matching."""
    def key(p):
        return (round(p[0] / tol), round(p[1] / tol))

    adj: dict = {}
    for i, (a, b) in enumerate(segs):
        adj.setdefault(key(a), []).append((i, 0))
        adj.setdefault(key(b), []).append((i, 1))
    used = [False] * len(segs)
    out = []
    for s in range(len(segs)):
        if used[s]:
            continue
        used[s] = True
        chain = [segs[s][0], segs[s][1]]
        for end in (1, 0):
            while True:
                p = chain[-1] if end else chain[0]
                nxt = None
                for i, side in adj.get(key(p), ()):
                    if not used[i]:
                        nxt = (i, side)
                        break
                if nxt is None:
                    break
                i, side = nxt
                used[i] = True
                other = segs[i][1 - side]
                if end:
                    chain.append(other)
                else:
                    chain.insert(0, other)
        if len(chain) >= 3:
            out.append(chain)
    return out


# ===========================================================================
# inking helpers
# ===========================================================================
def _arclen(pts):
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    return cum


def _at(pts, cum, s):
    i = bisect.bisect_right(cum, s)
    if i <= 0:
        return pts[0]
    if i >= len(pts):
        return pts[-1]
    seg = cum[i] - cum[i - 1]
    t = 0.0 if seg <= 0 else (s - cum[i - 1]) / seg
    return (pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t,
            pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t)


def _slice(pts, cum, a, b):
    out = [_at(pts, cum, a)]
    i = bisect.bisect_right(cum, a)
    while i < len(pts) and cum[i] < b:
        out.append(pts[i])
        i += 1
    out.append(_at(pts, cum, b))
    return out


def _dashed(pts, duty, pen, period: float = DASH_MM, f: int = 2100):
    """Ink a polyline at a given duty: solid -> dashed -> (once a dash would
    carry less than one pen tip of ink) a single dot -> nothing.  The pen's
    physical tip width decides where dashes become stipple; no taste parameter
    does.

    ``duty`` may be a single number OR one value per point.  Per-point is the
    normal case here: a density contour runs through both a lobe and the gap
    beside it, so the SAME ring is solid where the state is dense against the
    prior and frays where it is not.  A single average duty per ring was tried
    and is wrong -- the average is dragged to zero by the gaps, where the excess
    is negative, and the whole nest disappears (measured)."""
    if len(pts) < 2:
        return []
    seq = not isinstance(duty, (int, float))
    if not seq:
        if duty >= 0.98:
            return _poly(pts, color=pen, f=f)
        if duty <= 0.035:
            return []
    cum = _arclen(pts)
    L = cum[-1]
    if L < 0.4:
        return []
    out: List[GCodeCommand] = []
    k = 0
    while k * period < L:
        a = k * period
        if seq:
            d = duty[min(bisect.bisect_right(cum, a), len(duty) - 1)]
        else:
            d = duty
        if d <= 0.035:
            k += 1
            continue
        on = d * period
        if on < TIP_MM * 0.9:              # a dash shorter than the tip IS a dot
            px, py = _at(pts, cum, min(L, a + period * 0.5))
            out += _dot(px, py, r=0.3, color=pen)
            k += 1
            continue
        sub = _slice(pts, cum, a, min(L, a + on))
        if len(sub) >= 2:
            out += _poly(sub, color=pen, f=f)
        k += 1
    return out


def _dashed_line(a, b, pen, on: float = 2.2, off: float = 2.0, f: int = 2100):
    ax, ay = a
    bx, by = b
    L = math.hypot(bx - ax, by - ay)
    if L < 1e-9:
        return []
    out: List[GCodeCommand] = []
    s = 0.0
    while s < L:
        e = min(L, s + on)
        out += _poly([(ax + (bx - ax) * s / L, ay + (by - ay) * s / L),
                      (ax + (bx - ax) * e / L, ay + (by - ay) * e / L)], color=pen, f=f)
        s = e + off
    return out


def _arrow(x, y, dx, dy, pen, head: float = 2.0, f: int = 2100):
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx / L, dy / L
    out = _poly([(x, y), (x + dx, y + dy)], color=pen, f=f)
    tx, ty = x + dx, y + dy
    for sgn in (1, -1):
        px, py = -uy * sgn, ux * sgn
        out += _poly([(tx, ty), (tx - ux * head + px * head * 0.5,
                                 ty - uy * head + py * head * 0.5)], color=pen, f=f)
    return out


def _txt(s: str, x: float, y: float, h: float, pen, anchor: str = "l",
         spaced: bool = False, f: int = 2300):
    t = _spaced(s) if spaced else s
    w = _text_width(t, h)
    if anchor == "c":
        x -= w / 2.0
    elif anchor == "r":
        x -= w
    return _stroke_text(t, x, y, h, color=pen, f=f)


def _txt_w(s: str, h: float, spaced: bool = False) -> float:
    return _text_width(_spaced(s) if spaced else s, h)


# ===========================================================================
# a state cell: the relief of F = log p_hat_t - log N(0, I)
# ===========================================================================
def _state_cell(P: np.ndarray, stip: np.ndarray, cx: float, cy: float, half: float,
                lift: float, f_ref: float, pen, h_kde: float, floor: float = 0.0,
                relief: Tuple[float, float] = (0.0, 1.0), ng: int = KDE_GRID):
    """Draw one state.  Returns (commands, F_max, (rings, inked particles)).

    TWO fields, each doing the job it is actually right for:

      p_hat_t   the estimated density.  Its level sets ARE "the data manifold's
                level sets" -- one connected, lobed nest, splitting into separate
                eyes only at the high levels where the modes separate.  This is
                the RING GEOMETRY.
      F         log p_hat_t - log(prior through the same kernel): the excess over
                noise.  This is the MEASUREMENT -- what is detectable, how solid
                the ink is, and how high the relief stands.

    Contouring F itself was tried and is geometrically impossible for this
    subject: a variance-preserving diffusion keeps Var(x_t) = I at every t, so
    p_t and the prior have the SAME covariance and {p_t > prior} is necessarily
    several disjoint islands around the modes -- never the single lobed nest the
    plate needs (measured: 5 chains at every outer level, for every data law
    tried).  Density for shape, ratio for truth."""
    dens, xs = _kde(P, h_kde, ng, WIN)
    F = np.log(np.maximum(dens, _TINY)) - _log_null(xs, h_kde)
    fmax = float(F.max())

    mmu = half / WIN                       # mm per data sigma
    cell = float(xs[1] - xs[0])
    out: List[GCodeCommand] = []

    # THE NEST'S OUTER RING is the density contour that just ENCLOSES everything
    # detectable: L0 = the 5th percentile of p_hat over {F > floor}.  (The
    # detected set's own equivalent radius was tried and badly under-sizes the
    # nest -- it is the union of a few narrow lobe-ellipses, so its AREA is a
    # fraction of the form's extent and the nests came out tiny.)  So the nest's
    # diameter is a measurement, and it shrinks to nothing on its own as the
    # schedule destroys the contrast.
    det = F > floor
    if int(det.sum()) < 24:
        L0, r_out = float(dens.max()) * 2.0, 0.0
    else:
        L0 = float(np.quantile(dens[det], 0.01))
        r_out = math.sqrt(float((dens > L0).sum()) * cell * cell / math.pi)

    # --- hidden-line test for the shear relief (viewer in front = small world y)
    dlo, dhi = relief
    Dn = np.clip((np.log(np.maximum(dens, _TINY)) - dlo) / max(dhi - dlo, 1e-9), 0.0, 1.0)
    SY = xs[:, None] + (lift / mmu) * Dn
    run = np.maximum.accumulate(SY, axis=0)
    vis = SY >= run - 1e-9

    def _ij(wx, wy):
        return (int((wx + WIN) / (2 * WIN) * ng), int((wy + WIN) / (2 * WIN) * ng))

    def visible(wx, wy) -> bool:
        i, j = _ij(wx, wy)
        if i < 0 or j < 0 or i >= ng or j >= ng:
            return True
        return bool(vis[j, i])

    def field(wx, wy) -> float:
        i, j = _ij(wx, wy)
        if i < 0 or j < 0 or i >= ng or j >= ng:
            return -9.0
        return float(F[j, i])

    # --- rings.  A ring shorter than the perimeter of one smoothing kernel is
    # an artefact of the estimator, not a level set, so it is dropped.
    levels = _pitch_levels(dens, cell, RING_MM / mmu, r_out)
    min_per = math.pi * h_kde
    n_rings = 0
    for lv in levels:
        # RING HEIGHT: the ring is a level set of the density, so its height on
        # the shear relief is constant along it -- the nest stacks as one clean
        # mound.  The scale (dlo, dhi) is fixed once from the t = 0 state and
        # shared by every cell, so the mound FLATTENS across the row exactly as
        # the peak density falls.  Height varying along the ring was tried and
        # shears the rings into loose ribbons; a level set has one height.
        z = lift * max(0.0, min(1.0, (math.log(max(lv, _TINY)) - dlo) / max(dhi - dlo, 1e-9)))
        drawn = False
        for chain in _iso_runs(dens, xs, lv):
            per = sum(math.hypot(chain[i][0] - chain[i - 1][0], chain[i][1] - chain[i - 1][1])
                      for i in range(1, len(chain)))
            if per < min_per:
                continue
            drawn = True
            pts, dut = [], []
            for wx, wy in chain:
                if not visible(wx, wy):
                    if len(pts) >= 2:
                        out += _dashed(pts, dut, pen)
                    pts, dut = [], []
                    continue
                pts.append((cx + wx * mmu, cy + wy * mmu + z))
                # DASH DUTY varies ALONG the ring: a density contour runs through
                # a lobe and then through the gap beside it, so the same ring is
                # solid where the state is measurably denser than the prior and
                # frays where it is not.  This is the only channel carrying the
                # schedule pointwise, and it is what makes the nests break up.
                dut.append(max(0.0, min(1.0, field(wx, wy) / (DUTY_REF * f_ref))))
            if len(pts) >= 2:
                out += _dashed(pts, dut, pen)
        if drawn:
            n_rings += 1

    # --- the particles themselves, and ONLY where no ring covers them: outside
    # the nest's outer contour.  Inside it the contours ARE the particles, and
    # stippling over them just buries the structure (measured on v2).  So x0 is
    # a clean nest with a faint outer speckle and x_T, which has no nest at all,
    # shows every particle -- the reference's whole progression out of one rule.
    # Same 420 indices at every t, so a particle can be followed along the row.
    n_dots = 0
    for wx, wy in stip:
        if abs(wx) > WIN * 0.995 or abs(wy) > WIN * 0.995:
            continue
        i, j = _ij(wx, wy)
        if 0 <= i < ng and 0 <= j < ng and dens[j, i] >= L0:
            continue
        if not visible(wx, wy):
            continue
        out += _dot(cx + wx * mmu, cy + wy * mmu, r=0.32, color=pen)
        n_dots += 1
    return out, fmax, (n_rings, n_dots)


# ===========================================================================
# the U-Net bowtie
# ===========================================================================
def _bowtie(u0: float, u1: float, cy: float, halfh: float, pens, blk):
    """One drawn line per feature-map row, constant pitch: envelope height IS
    the spatial resolution, rows MERGE IN PAIRS at each stride-2 step, and each
    level's x-extent is proportional to its channel count."""
    res = list(UNET_RES)
    ch = list(UNET_CH)
    seq_res = res + res[-2::-1]                     # 32 16 8 4 8 16 32
    seq_ch = ch + ch[-2::-1]
    pitch = 2.0 * halfh / res[0]
    trans = 13.0
    unit = (u1 - u0 - trans * (len(seq_res) - 1)) / float(sum(seq_ch))
    plate = [c * unit for c in seq_ch]

    spans = []
    x = u0
    for k, L in enumerate(plate):
        spans.append((x, x + L))
        x += L + (trans if k < len(plate) - 1 else 0.0)

    def ys(r):
        return [(i + 0.5 - r / 2.0) * pitch for i in range(r)]

    def pen_at(xx):
        d = (xx - u0) / max(u1 - u0, 1e-9)
        return pens[min(3, max(0, int(d * 4.0)))]

    out: List[GCodeCommand] = []
    # plateaus
    for (a, b), r in zip(spans, seq_res):
        for y in ys(r):
            n = max(2, int((b - a) / 2.0))
            pts, cur = [], None
            for k in range(n + 1):
                xx = a + (b - a) * k / n
                p = pen_at(xx)
                if cur is None:
                    cur = p
                if p != cur:
                    if len(pts) >= 2:
                        out += _poly(pts, color=cur, f=2100)
                    pts, cur = [pts[-1]] if pts else [], p
                pts.append((xx, cy + y))
            if len(pts) >= 2:
                out += _poly(pts, color=cur, f=2100)
    # transitions: merge in pairs going in, split going out
    for k in range(len(spans) - 1):
        a = spans[k][1]
        b = spans[k + 1][0]
        ra, rb = seq_res[k], seq_res[k + 1]
        ya, yb = ys(ra), ys(rb)
        for i in range(ra):
            j = i // 2 if rb < ra else min(rb - 1, i * 2 if rb > ra else i)
            if rb > ra:                              # split: source i -> 2i, 2i+1
                targets = [2 * i, 2 * i + 1]
            else:
                targets = [j]
            for tgt in targets:
                pts = []
                n = 16
                for m in range(n + 1):
                    u = m / n
                    s = u * u * (3 - 2 * u)
                    xx = a + (b - a) * u
                    yy = ya[i] + (yb[tgt] - ya[i]) * s
                    pts.append((xx, cy + yy))
                out += _poly(pts, color=pen_at((a + b) / 2), f=2100)
    return out, spans, pitch


# ===========================================================================
# THE PLATE
# ===========================================================================
def diffusion_passes(rng: SeededRNG, bounds: Bounds, colors: int = 3) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    S = min((x1 - x0) / 400.0, (y1 - y0) / 277.0)
    OX = x0 + ((x1 - x0) - 400.0 * S) / 2.0
    OY = y0 + ((y1 - y0) - 277.0 * S) / 2.0

    def X(u):
        return OX + u * S

    def Y(v):
        return OY + v * S

    def M(v):                                        # a design-space length in mm
        return v * S

    if colors >= 5:
        BLK, BLU, PUR, PNK, CRM = 0, 1, 2, 3, 4
    elif colors == 4:
        BLK, BLU, PUR, PNK, CRM = 0, 1, 2, 3, 3
    elif colors == 3:
        BLK, BLU, PUR, PNK, CRM = 0, 1, 1, 2, 2
    elif colors == 2:
        BLK, BLU, PUR, PNK, CRM = 0, 1, 1, 1, 1
    else:
        BLK = BLU = PUR = PNK = CRM = None
    RAMP = [BLU, PUR, PNK, CRM]
    COLPEN = [BLK, BLU, PUR, PNK, CRM, BLK]

    # ------------------------------------------------------------- the process
    ab, alpha, beta = _schedule()
    w, mu, Sig = _data_law(rng)

    gen_f = np.random.default_rng([rng.seed, 11])    # forward stream
    gen_r = np.random.default_rng([rng.seed, 977])   # reverse stream -- independent
    gen_s = np.random.default_rng([rng.seed, 5])

    x_data = _sample_data(w, mu, Sig, N_PART, gen_f)
    eps_f = gen_f.standard_normal((N_PART, 2))       # ONE fixed coupling

    # choose the displayed t by EQUAL STEPS OF SURVIVING CONTRAST, measured on
    # the exact marginal: the t values then come out unevenly spaced, which is
    # precisely the schedule's late-and-fast collapse made readable.
    gq = np.linspace(-WIN, WIN, 96)
    GX, GY = np.meshgrid(gq, gq)
    GP = np.stack([GX.ravel(), GY.ravel()], 1)
    lq = -math.log(2 * math.pi) - 0.5 * (GP ** 2).sum(1)

    def contrast(t: int) -> float:
        p = _marginal(GP, w, mu, Sig, float(ab[t]))
        return float(np.max(np.log(np.maximum(p, _TINY)) - lq))

    probe_t = list(range(0, T_STEPS + 1, 10))
    probe_c = np.array([contrast(t) for t in probe_t])
    c0 = probe_c[0]
    targets = [0.78, 0.56, 0.35, 0.16]
    t_show = [0]
    for tg in targets:
        k = int(np.argmin(np.abs(probe_c - tg * c0)))
        t_show.append(probe_t[k])
    t_show.append(T_STEPS)

    abs_show = [float(ab[t]) for t in t_show]
    sa = [math.sqrt(a) for a in abs_show]

    # forward states
    fwd = [sa[k] * x_data + math.sqrt(max(1.0 - abs_show[k], 0.0)) * eps_f
           for k in range(6)]

    # reverse: real DDPM ancestral sampling from FRESH noise, all T steps
    x = gen_r.standard_normal((N_PART, 2))
    rev_snap = {T_STEPS: x.copy()}
    want = set(t_show)
    for t in range(T_STEPS, 0, -1):
        abt = float(ab[t])
        abp = float(ab[t - 1])
        e = _eps_theta(x, w, mu, Sig, abt)
        at = float(alpha[t])
        bt = float(beta[t])
        x = (x - bt / math.sqrt(max(1.0 - abt, 1e-12)) * e) / math.sqrt(max(at, 1e-12))
        if t > 1:
            var = (1.0 - abp) / max(1.0 - abt, 1e-12) * bt
            x = x + math.sqrt(max(var, 0.0)) * gen_r.standard_normal((N_PART, 2))
        if (t - 1) in want:
            rev_snap[t - 1] = x.copy()
    rev = [rev_snap[t] for t in t_show]

    stip_idx = gen_s.choice(N_PART, size=N_STIPPLE, replace=False)

    # ONE BANDWIDTH FOR THE WHOLE SHEET: 0.75 x the narrowest feature of the
    # data law (the smallest sd in the mixture), floored at 2 grid cells.  A
    # per-t bandwidth was tried first and is wrong twice over -- it makes the
    # columns incomparable (a change in the picture could be the estimator
    # rather than the process), and by t4 it had grown to 0.71, smoothing the
    # state broader than the prior so the contrast rose again instead of dying.
    cell_w = 2.0 * WIN / KDE_GRID
    H_KDE = max(2.0 * cell_w, 0.75 * math.sqrt(float(np.linalg.eigvalsh(Sig).min())))
    FLOOR = _noise_floor(N_PART, H_KDE, KDE_GRID, WIN,
                         np.random.default_rng([rng.seed, 4242]))

    # ------------------------------------------------------------------ layout
    RU0, RU1 = 12.0, 334.0
    PITCH = (RU1 - RU0) / 6.0
    CU = [RU0 + PITCH * (k + 0.5) for k in range(6)]
    MID = (RU0 + RU1) / 2.0

    TOP_CV, TOP_LIFT = 210.0, 5.5
    BOT_CV, BOT_LIFT = 36.8, 4.6
    HWU = 20.5

    out: List[GCodeCommand] = []

    # F_REF: the peak contrast of the data law itself, fixed once and shared by
    # every cell on the sheet -- so the mounds are on ONE scale and the flattening
    # across the row is the schedule, not a per-cell rescale.
    d0, xs0 = _kde(fwd[0], H_KDE, KDE_GRID, WIN)
    F0 = np.log(np.maximum(d0, _TINY)) - _log_null(xs0, H_KDE)
    F_REF = float(F0.max())
    # RELIEF SCALE, fixed once from the data law and shared by every cell: from
    # the density of x0's outermost ring up to its peak.  Because the scale is
    # shared, the mound visibly FLATTENS along the row -- that flattening is the
    # peak density falling, not a per-cell rescale.
    RELIEF = (math.log(max(float(np.quantile(d0[F0 > FLOOR], 0.01)), _TINY)),
              math.log(float(d0.max())))

    diag = {"t": t_show, "abar": abs_show, "sqrt_abar": sa, "F_REF": F_REF,
            "h": H_KDE, "floor": FLOOR, "fmax_fwd": [], "fmax_rev": [],
            "rings_fwd": [], "rings_rev": []}

    # ============================================================ REGISTER 1
    for k in range(6):
        cmds, fm, nr = _state_cell(fwd[k], fwd[k][stip_idx], X(CU[k]), Y(TOP_CV),
                                   M(HWU), M(TOP_LIFT), F_REF, COLPEN[k], H_KDE,
                                   floor=FLOOR, relief=RELIEF)
        out += cmds
        diag["fmax_fwd"].append(fm)
        diag["rings_fwd"].append(nr)

    # ============================================================ REGISTER 3
    for k in range(6):
        cmds, fm, nr = _state_cell(rev[k], rev[k][stip_idx], X(CU[k]), Y(BOT_CV),
                                   M(HWU * 0.82), M(BOT_LIFT), F_REF, COLPEN[k], H_KDE,
                                   floor=FLOOR, relief=RELIEF)
        out += cmds
        diag["fmax_rev"].append(fm)
        diag["rings_rev"].append(nr)

    # ============================================================ REGISTER 2
    BU0, BU1, BCV, BHH = 82.0, 298.0, 119.0, 27.0
    bow, spans, pitch = _bowtie(BU0, BU1, BCV, BHH, RAMP, BLK)
    bow_mm = [GCodeCommand(command=c.command, x=None if c.x is None else X(c.x),
                           y=None if c.y is None else Y(c.y), z=c.z, f=c.f, s=c.s,
                           color=c.color) for c in bow]
    out += bow_mm

    # skip connections: mirrored levels, channels/128 parallel dashed strands
    n_lv = len(UNET_RES)
    arc_pen = BLK
    for lv in range(n_lv - 1):
        ea = spans[lv]
        da = spans[len(spans) - 1 - lv]
        xa = 0.5 * (ea[0] + ea[1])
        xb = 0.5 * (da[0] + da[1])
        top_a = BCV + UNET_RES[lv] * pitch / 2.0
        top_b = top_a
        peak = BHH + 2.0 + (n_lv - 2 - lv) * 3.2
        strands = max(1, UNET_CH[lv] // 128)
        for sidx in range(strands):
            off = (sidx - (strands - 1) / 2.0) * 1.1
            pts = []
            n = 76
            for m in range(n + 1):
                u = m / n
                xx = xa + (xb - xa) * u
                bump = math.sin(math.pi * u)
                yy = (top_a + (top_b - top_a) * u) + bump * (peak - (top_a - BCV)) + off * bump
                pts.append((X(xx), Y(BCV + yy - BCV)))
            acc = 0.0
            run = []
            for i in range(1, len(pts)):
                seg = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
                if (acc // M(3.4)) % 2 == 0:
                    if not run:
                        run = [pts[i - 1]]
                    run.append(pts[i])
                else:
                    if len(run) >= 2:
                        out += _poly(run, color=arc_pen, f=2100)
                    run = []
                acc += seg
            if len(run) >= 2:
                out += _poly(run, color=arc_pen, f=2100)
        # little down-arrows onto the decoder side
        out += _arrow(X(xb), Y(BCV + peak * 0.42), 0.0, -M(3.0), arc_pen, head=M(1.6))

    # x_t entering (a real state, at the t of column 4) and eps-hat leaving
    t_in = t_show[2]
    a_in = abs_show[2]
    x_in = fwd[2]
    cmds, _, _ = _state_cell(x_in, x_in[stip_idx], X(44.0), Y(BCV), M(15.0), M(5.0),
                             F_REF, COLPEN[2], H_KDE, floor=FLOOR, relief=RELIEF)
    out += cmds
    eps_hat = _eps_theta(x_in, w, mu, Sig, a_in)
    cmds, _, _ = _state_cell(eps_hat, eps_hat[stip_idx], X(320.0), Y(BCV), M(14.0),
                             M(5.0), F_REF, BLK, H_KDE, floor=FLOOR, relief=RELIEF)
    out += cmds
    loss = float(np.mean(((eps_f - eps_hat) ** 2).sum(1)))
    eig = np.linalg.eigvalsh(np.cov(eps_hat.T))
    diag["loss"] = loss
    diag["eps_hat_cov_eig"] = eig.tolist()
    diag["t_in"] = t_in

    out += _arrow(X(62.0), Y(BCV), M(15.0), 0.0, BLK, head=M(2.0))
    out += _arrow(X(300.0), Y(BCV), M(4.0), 0.0, BLK, head=M(2.0))

    # ============================================================ TYPE
    # -- title block
    out += giant_type("DIFFUSION", X(12.0), Y(265.0), M(5.0), pen=BLK,
                      weight=M(0.55), tip=M(0.45), spaced=True)
    for i, ln in enumerate(("probabilistic", "generative", "modeling")):
        out += _txt(ln, X(12.0), Y(257.0 - 4.5 * i), M(2.2), BLK, spaced=True)

    # -- forward header
    out += _txt("forward process (noising)", X(MID), Y(265.0), M(2.6), BLK, "c", True)
    out += _dashed_line((X(118.0), Y(259.0)), (X(318.0), Y(259.0)), BLK,
                        on=M(3.2), off=M(2.6))
    out += _arrow(X(318.0), Y(259.0), M(4.0), 0.0, BLK, head=M(2.0))
    out += _txt("q(xt | x0)  =  N( sqrt(at) x0 ,  (1 - at) I )", X(MID), Y(250.0),
                M(2.8), BLK, "c")

    lbl = ["x0", "xt1", "xt2", "xt3", "xt4", "xT"]
    for k in range(6):
        out += _txt(lbl[k], X(CU[k]), Y(242.0), M(3.0), COLPEN[k], "c")
        out += _txt("t = %d" % t_show[k], X(CU[k]), Y(185.0), M(2.0), BLK, "c")
        val = ("%.3f" % sa[k]) if sa[k] >= 1e-3 else ("%.1e" % sa[k])
        out += _txt("sqrt at " + val, X(CU[k]), Y(181.0), M(2.0), COLPEN[k], "c")
        if k < 5:
            gx = 0.5 * (CU[k] + CU[k + 1])
            for d in (-1, 0, 1):
                out += _dot(X(gx + d * 2.0), Y(TOP_CV + 3.0), r=0.3, color=BLK)

    out += _txt("data distribution", X(CU[0]), Y(175.0), M(2.1), BLK, "c")
    out += _txt("p data(x)", X(CU[0]), Y(171.0), M(2.1), BLK, "c")
    out += _txt("isotropic noise", X(CU[5]), Y(175.0), M(2.1), BLK, "c")
    out += _txt("N(0, I)", X(CU[5]), Y(171.0), M(2.1), BLK, "c")

    # -- the t axis, stated once, serving BOTH rows (they register by t)
    out += _poly([(X(34.0), Y(166.0)), (X(308.0), Y(166.0))], color=BLK, f=2200)
    out += _arrow(X(308.0), Y(166.0), M(4.0), 0.0, BLK, head=M(2.0))
    out += _txt("t = 0", X(12.0), Y(164.5), M(2.2), BLK, spaced=True)
    out += _txt("t = T", X(318.0), Y(164.5), M(2.2), BLK, spaced=True)
    out += _txt("increasing noise", X(MID), Y(168.0), M(2.1), BLK, "c", True)

    # -- U-Net
    out += _txt("U-Net  εθ(xt, t)", X(12.0), Y(152.0), M(3.6), BLK, spaced=True)
    out += _txt("predicts noise (or v, or x0)", X(12.0), Y(145.5), M(2.2), BLK)
    out += _txt("skip connections", X(189.0), Y(137.0), M(2.1), BLK, "c", True)
    out += _txt("xt", X(44.0), Y(BCV + 17.0), M(3.0), COLPEN[2], "c")
    out += _txt("noisy sample", X(44.0), Y(BCV - 19.0), M(2.1), BLK, "c")
    out += _txt("t = %d" % t_in, X(44.0), Y(BCV - 23.0), M(2.1), COLPEN[2], "c")
    out += _txt("ε", X(320.0), Y(BCV + 16.0), M(3.0), BLK, "c")
    out += _txt("predicted noise", X(320.0), Y(BCV - 18.0), M(2.1), BLK, "c")

    # level readout: the real DDPM configuration the bowtie is drawn from, each
    # tag centred under its own encoder plateau, all on one baseline
    for lv in range(len(UNET_RES)):
        a, b = spans[lv]
        xc = 0.5 * (a + b)
        yv = BCV - UNET_RES[lv] * pitch / 2.0 - 4.2
        pn = RAMP[min(3, int((xc - BU0) / (BU1 - BU0) * 4))]
        out += _txt("%d^2 %dch" % (UNET_RES[lv], UNET_CH[lv]), X(xc), Y(yv),
                    M(1.95), pn, "c")

    # loss, with the value actually measured on this sheet
    out += _poly([(X(338.0), Y(BCV + 9.0)), (X(338.0), Y(BCV - 9.0))], color=BLK, f=2200)
    out += _txt("L = E ( ε - εθ(xt, t) )^2", X(342.0), Y(BCV + 1.5), M(2.2), BLK)
    out += _txt("= %.3f  measured" % loss, X(342.0), Y(BCV - 3.6), M(2.0), BLK)

    # -- reverse header
    out += _txt("reverse process (denoising)", X(MID), Y(82.0), M(2.6), BLK, "c", True)
    out += _dashed_line((X(318.0), Y(76.0)), (X(122.0), Y(76.0)), BLK,
                        on=M(3.2), off=M(2.6))
    out += _arrow(X(122.0), Y(76.0), -M(4.0), 0.0, BLK, head=M(2.0))
    out += _txt("pθ(xt-1 | xt)  =  N( muθ(xt, t) ,  σt^2 I )", X(MID), Y(68.0),
                M(2.6), BLK, "c")

    for k in range(6):
        out += _txt(lbl[k], X(CU[k]), Y(61.5), M(2.6), COLPEN[k], "c")
        if k < 5:
            gx = 0.5 * (CU[k] + CU[k + 1])
            for d in (-1, 0, 1):
                out += _dot(X(gx + d * 2.0), Y(BOT_CV + 2.0), r=0.3, color=BLK)

    out += _txt("generated sample", X(CU[0]), Y(15.5), M(2.1), BLK, "c")
    out += _txt("x ~ pθ(x)", X(CU[0]), Y(11.5), M(2.1), BLK, "c")
    out += _txt("sample from", X(CU[5]), Y(15.5), M(2.1), BLK, "c")
    out += _txt("N(0, I)", X(CU[5]), Y(11.5), M(2.1), BLK, "c")

    # ============================================================ FURNITURE
    out += _stroke_text(_spaced("PEN PLOTTER"), X(12.0), Y(4.0), M(3.2), color=BLK, f=2400)
    rule = _txt_w("PEN PLOTTER", M(3.2), spaced=True)
    out += _poly([(X(12.0) + rule + M(4.0), Y(5.6)),
                  (X(12.0) + rule + M(16.0), Y(5.6))], color=BLK, f=2200)

    out += _txt("cosine schedule   T = 1000   n = %d particles   exact score   "
                "DDPM ancestral" % N_PART, X(334.0), Y(5.6), M(1.95), BLK, "r")

    stack_a = ("noise", "schedules", "score matching", "denoising", "generative sampling")
    for i, ln in enumerate(stack_a):
        out += _txt(ln, X(344.0), Y(270.0 - 4.5 * i), M(2.1), BLK)
    stack_b = ("latent diffusion", "text conditioning", "classifier-free guidance",
               "high-dimensional data", "iterative refinement")
    for i, ln in enumerate(stack_b):
        out += _txt(ln, X(344.0), Y(46.0 - 4.5 * i), M(2.1), BLK)

    out += plus_mark(X(344.0), Y(166.0), M(3.0), pen=BLK)
    out += plus_mark(X(12.0), Y(119.0), M(3.0), pen=BLK)
    out += plus_mark(X(173.0), Y(274.0), M(2.6), pen=BLK)
    for u, v in ((12.0, 242.0), (344.0, 242.0), (344.0, 61.5), (12.0, 61.5)):
        out += fill_rect(X(u), Y(v), X(u + 1.6), Y(v + 1.6), spacing=M(0.5), pen=BLK)

    # dashed quarter arcs -- placed in the two genuinely empty pockets of the
    # right margin, not dropped into corners the type already occupies
    for ccx, ccy, r, a0 in ((394.0, 240.0, 17.0, math.pi),
                            (394.0, 96.0, 17.0, math.pi / 2)):
        pts = [(X(ccx + r * math.cos(a0 + math.pi / 2 * t / 40)),
                Y(ccy + r * math.sin(a0 + math.pi / 2 * t / 40))) for t in range(41)]
        acc = 0.0
        run = []
        for i in range(1, len(pts)):
            seg = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
            if (acc // M(2.1)) % 2 == 0:
                if not run:
                    run = [pts[i - 1]]
                run.append(pts[i])
            else:
                if len(run) >= 2:
                    out += _poly(run, color=BLK, f=2200)
                run = []
            acc += seg
        if len(run) >= 2:
            out += _poly(run, color=BLK, f=2200)

    # ---------------------------------------------------------------- diagnostics
    iso = np.linalg.eigvalsh(np.cov(fwd[5].T))
    diag["xT_cov_eig"] = iso.tolist()
    diag["xT_iso_ratio"] = float(iso.max() / iso.min())
    diag["abar_T"] = float(ab[T_STEPS])
    diag["beta_1"] = float(beta[1])
    diag["beta_T"] = float(beta[T_STEPS])
    diag["rev_x0_mean"] = np.mean(rev[0], 0).tolist()
    diag["rev_x0_cov"] = np.cov(rev[0].T).tolist()
    diag["fwd_x0_mean"] = np.mean(fwd[0], 0).tolist()
    diag["fwd_x0_cov"] = np.cov(fwd[0].T).tolist()
    # independence of the two streams: the correlation between the forward x_T
    # draws and the reverse chain's starting noise, particle by particle
    diag["stream_corr"] = float(abs(np.corrcoef(fwd[5][:, 0], rev_snap[T_STEPS][:, 0])[0, 1]))
    diffusion_passes.diag = diag
    return out


if __name__ == "__main__":
    import json
    import time

    from promptplot.config import PaperConfig, get_config

    cfg = get_config()
    cfg.paper = PaperConfig.from_size("a3", "landscape")
    t0 = time.time()
    cmds = diffusion_passes(SeededRNG(7), cfg.paper.get_drawable_area(), colors=5)
    print("commands", len(cmds), "in %.1fs" % (time.time() - t0))
    print(json.dumps(diffusion_passes.diag, indent=1, default=float))
