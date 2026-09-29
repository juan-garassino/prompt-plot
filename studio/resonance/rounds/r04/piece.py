"""ATTENTION AS RESONANCE — ONE FIELD (resonance r04, thesis ``one-field``, parent r01).

The plate IS the interference figure.  Two coherent point sources, Q (crimson)
and K (blue); their field is blown up past the sheet and cropped at the top and
both side edges.  It stops on ONE horizontal cut — the screen of Young's
experiment — and the edge it stops on is the softmax of the interference term
along that cut, the only heavy line on the sheet.  No box, arrow, packet row or
gradient label survives from r01.

The one drawing rule (exact, and the whole plate is made of it)
--------------------------------------------------------------
* CRIMSON / BLUE — each wave's own Huygens crests r_s = (m - phi_s/2pi) L, drawn
  only where the two crest families cross at more than 25 deg (the r01 guard's
  parallel test, promoted to a regime boundary): the only place a pen can hold
  them apart.  By the inscribed-angle theorem that region is two discs through Q
  and K — the knot.
* BLACK — everywhere else the two families run within 25 deg of parallel and a
  pen would merge them, so the plate draws what they add up to: the crests of
  the SUM psi (arg psi = 0), only where the time-averaged intensity
  I = A_Q^2 + A_K^2 + 2 A_Q A_K cos(dPhase) clears one level I_th.  Where they
  cancel (the nodal hyperbolae) the sheet is bare paper.  I_th is absolute, so
  the rays taper as the wave spreads (1/r intensity) — tone drives duty, the
  crest pitch never changes.
* THE HEAVY LINE — softmax of the cross-term along the cut (below).

FOLDING THE PACKETS INTO THE SOURCES.  The r01 Q and K rows are wave packets
q_i(xi), k_j(xi) (carrier x Gaussian), xi measured from each block's node
column toward the centre.  Their dot products are overlap integrals

    S_ij = int q_i k_j dxi  =  (1/pi) Re int_0^inf Qhat(w) Khat*(w) dw   (Parseval)

The plate draws the best-matching pair by cosine (Q4, K4: cos 0.748).  Both
sources radiate at the RESONANT carrier w0 = argmax |Qhat Khat| — where the two
spectra overlap, i.e. where the dot product is made — with amplitude and phase
equal to each packet's Fourier coefficient there:  a_s e^{i phi_s} = shat(w0).
One shared wavelength is what makes the interference stationary (resonance);
the packets survive as a_Q/a_K and dphi = phi_Q - phi_K.

THE SUM CRESTS, in closed form.  With h = r_Q - r_K, s = r_Q + r_K and band j
(k h + dphi = 2 pi j + delta, |delta| < pi):
    psi = e^{i(k s/2 + phibar + pi j)} [(A_Q + A_K) cos(delta/2) + i (A_Q - A_K) sin(delta/2)]
so the crest n is  s = 2 (2 pi n - pi j - phibar - eps) / k,
eps = atan2((A_Q - A_K) sin(delta/2), (A_Q + A_K) cos(delta/2)),  solved by fixed
point along each hyperbola and mapped back to the sheet by two-circle
intersection.  Measured |arg psi| on the drawn crests < 1e-4 rad.

THE CUT.  On the screen y = y_s the cross-term of |psi|^2 is
    2 Re(psi_Q psi_K*) = 2 |psi_Q||psi_K| cos(k (r_Q - r_K) + dphi),
a dot product of two phasors whose angle is the path-phase difference — a
rotary-position score whose relative position is r_Q - r_K.  The heavy line is
    a(x) = softmax_x(beta * c(x)),   c(x) = cos(k (r_Q - r_K) + dphi) * r0 / sqrt(r_Q r_K)
over a row of keys every 0.25 mm; beta = |q||k|/sqrt(d_k) is the one chosen
number.  Its peaks sit on the antinodal hyperbolae because it is the same
equation — the black rays land on the peaks.

Deterministic: ``rng`` is accepted for the contract and never used.
"""

from __future__ import annotations

import math
from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import (  # noqa: F401
    _GLYPHS,
    _offset_polyline,
    _poly,
    _stroke_text,
    _text_width,
    fill_disc,
    giant_type,
)
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

# pens — the resonance family grammar (crimson = Q, blue = K, black = the figure)
Q_PEN, K_PEN, BLACK, TYPE = 0, 1, 2, 3


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return min(idx, colors - 1)


# ---------------------------------------------------------------------------
# 1. the r01 packets (reference pixels) and the fold into two sources
# ---------------------------------------------------------------------------

Packet = Tuple[float, float, float, float, float]  # centre, sigma, lambda, amp, phase

# verbatim from studio/resonance/rounds/r01/piece.py
Q_PACKETS: List[List[Packet]] = [
    [(225.0, 26.0, 12.0, 40.0, 0.0), (289.0, 10.0, 9.5, 17.0, 1.2), (160.0, 12.0, 7.5, 5.0, 0.4)],
    [(168.0, 23.0, 11.0, 34.0, 0.0), (306.0, 14.0, 11.0, 21.0, 0.6), (240.0, 10.0, 7.5, 4.0, 0.0)],
    [(252.0, 35.0, 18.0, 43.0, 0.0), (332.0, 12.0, 8.5, 13.0, 0.9), (192.0, 15.0, 9.0, 10.0, 0.3)],
    [(190.0, 25.0, 13.0, 29.0, 0.0), (331.0, 10.0, 9.5, 16.0, 0.5), (262.0, 10.0, 7.5, 5.0, 0.0)],
    [(243.0, 29.0, 12.0, 43.0, 0.0), (163.0, 11.0, 8.0, 6.0, 0.0)],
]
K_PACKETS: List[List[Packet]] = [
    [(950.0, 26.0, 12.0, 40.0, 0.0), (858.0, 10.0, 9.0, 16.0, 0.7), (1000.0, 11.0, 7.5, 6.0, 0.2)],
    [(944.0, 24.0, 11.0, 33.0, 0.0), (795.0, 13.0, 10.0, 20.0, 0.4), (880.0, 10.0, 7.5, 4.0, 0.0)],
    [(858.0, 33.0, 17.0, 41.0, 0.0), (962.0, 14.0, 8.5, 13.0, 1.1), (1000.0, 10.0, 7.0, 6.0, 0.5)],
    [(932.0, 25.0, 12.0, 33.0, 0.0), (790.0, 10.0, 9.0, 15.0, 0.9), (862.0, 10.0, 7.5, 5.0, 0.0)],
    [(884.0, 28.0, 11.0, 43.0, 0.0), (985.0, 11.0, 8.0, 6.0, 0.3)],
]
Q_HOME, K_HOME = 109.0, 1013.0   # the node columns; xi runs from here toward the centre


def _packet_signal(packets: Sequence[Packet], home: float, side: int, xi: np.ndarray) -> np.ndarray:
    """A packet row as a signal of xi = distance from its node column toward
    the centre.  K rows run right-to-left, so their phase flips sign."""
    v = np.zeros_like(xi)
    for c, sg, lam, amp, ph in packets:
        xc = (c - home) if side > 0 else (home - c)
        t = (xi - xc) / sg
        v += amp * np.exp(-t * t) * np.cos(2 * np.pi * (xi - xc) / lam + side * ph)
    return v


def fold_packets() -> dict:
    """Score matrix, best pair, resonant carrier, source amplitudes and phases."""
    dxi = 0.25
    xi = np.arange(0.0, 700.0, dxi)
    Q = [_packet_signal(p, Q_HOME, +1, xi) for p in Q_PACKETS]
    K = [_packet_signal(p, K_HOME, -1, xi) for p in K_PACKETS]
    S = np.array([[float(np.sum(q * k) * dxi) for k in K] for q in Q])
    qn = np.array([math.sqrt(float(np.sum(q * q) * dxi)) for q in Q])
    kn = np.array([math.sqrt(float(np.sum(k * k) * dxi)) for k in K])
    C = S / np.outer(qn, kn)
    i, j = np.unravel_index(int(np.argmax(C)), C.shape)
    ws = np.linspace(0.2, 1.2, 2001)
    E = np.exp(-1j * np.outer(ws, xi))
    Qh = E @ Q[i] * dxi
    Kh = E @ K[j] * dxi
    b = int(np.argmax(np.abs(Qh * Kh)))
    # Parseval: S_ij = (1/pi) Re int_0^inf Qhat Khat* dw  (real signals)
    pars = float(np.real(Qh * np.conj(Kh)).sum() * (ws[1] - ws[0]) / math.pi)
    return {
        "S": S, "C": C, "i": int(i), "j": int(j),
        "w0": float(ws[b]), "lam0_px": 2 * math.pi / float(ws[b]),
        "aQ": float(abs(Qh[b])), "aK": float(abs(Kh[b])),
        "phiQ": float(np.angle(Qh[b])), "phiK": float(np.angle(Kh[b])),
        "parseval": pars,
    }


# ---------------------------------------------------------------------------
# 2. masks along a polyline, with exact edges (vectorised bisection)
# ---------------------------------------------------------------------------

MaskFn = Callable[[np.ndarray, np.ndarray], np.ndarray]


def _mask_runs(P: np.ndarray, keep: MaskFn, min_len: float = 2.0) -> List[np.ndarray]:
    """Split polyline P (n, 2) into the runs where ``keep`` holds.  Every run
    end is bisected onto the mask boundary (20 halvings, < 1 um), so a crest
    stops ON the band edge, the screen curve or a halo, never a sample short."""
    if len(P) < 2:
        return []
    m = keep(P[:, 0], P[:, 1])
    tr = np.nonzero(m[:-1] != m[1:])[0]
    edge = {}
    if len(tr):
        a = P[tr].copy()
        b = P[tr + 1].copy()
        ain = m[tr]                       # which end is inside
        for _ in range(20):
            mid = (a + b) / 2
            mk = keep(mid[:, 0], mid[:, 1])
            same = mk == ain
            a[same] = mid[same]
            b[~same] = mid[~same]
        for t, q in zip(tr.tolist(), a):
            edge[t] = q
    # slice the kept stretches between transitions (vectorised bookkeeping)
    runs: List[np.ndarray] = []
    starts = [0] + (tr + 1).tolist()
    ends = tr.tolist() + [len(P) - 1]
    for st, en in zip(starts, ends):
        if not m[st]:
            continue
        body = P[st:en + 1]
        pre = [edge[st - 1]] if (st - 1) in edge else []
        post = [edge[en]] if en in edge else []
        runs.append(np.vstack(pre + [body] + post) if (pre or post) else body)
    out = []
    for r in runs:
        if len(r) >= 2 and float(np.hypot(*np.diff(r, axis=0).T).sum()) >= min_len:
            out.append(r)
    return out


def _decimate(P: np.ndarray, step: float = 0.3) -> np.ndarray:
    """Resample to vertices about ``step`` apart along the arc (ends kept)."""
    seg = np.hypot(*np.diff(P, axis=0).T)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    if cum[-1] <= step:
        return P[[0, -1]]
    idx = np.unique(np.searchsorted(cum, np.arange(0.0, cum[-1], step)))
    idx = np.unique(np.concatenate([idx, [len(P) - 1]]))
    return P[idx]


def _order(runs: List[np.ndarray], start: Pt = (0.0, 0.0)) -> List[np.ndarray]:
    """Greedy nearest-neighbour WITH reversal, so each layer streams as one
    spatial walk.  postprocess re-runs a no-reversal nearest-neighbour on the
    result; every choice here already minimised over both ends, so that pass
    reproduces this order."""
    if not runs:
        return []
    S = np.array([r[0] for r in runs])
    E = np.array([r[-1] for r in runs])
    alive = np.ones(len(runs), bool)
    pos = np.array(start, float)
    out: List[np.ndarray] = []
    for _ in range(len(runs)):
        ds = np.hypot(*(S - pos).T)
        de = np.hypot(*(E - pos).T)
        ds[~alive] = np.inf
        de[~alive] = np.inf
        i_s, i_e = int(np.argmin(ds)), int(np.argmin(de))
        if ds[i_s] <= de[i_e]:
            i, run = i_s, runs[i_s]
        else:
            i, run = i_e, runs[i_e][::-1]
        alive[i] = False
        out.append(run)
        pos = run[-1]
    return out


def _emit(run: np.ndarray, pen, f: int = 2600) -> List[GCodeCommand]:
    return _poly([(float(x), float(y)) for x, y in run], color=pen, f=f)


# ---------------------------------------------------------------------------
# 3. the plate
# ---------------------------------------------------------------------------

LAYOUT = {
    "L": 3.4,          # crest pitch, mm — one resonant wavelength for both sources
    "N": 6,            # d = N * L, whole wavelengths (the approved r01 construction)
    "mid_u": 0.30,     # pair midpoint, fraction of drawable width
    "mid_v": 0.82,     # pair midpoint, fraction of drawable height (from bottom)
    "tilt": 28.0,      # pair axis, degrees from horizontal (K upper-right of Q)
    "screen_v": 0.25,  # the cut, fraction of drawable height (from bottom)
    "peak_h": 44.0,    # tallest softmax peak, mm
    "beta": 6.0,       # |q||k| / sqrt(d_k): the inverse temperature
    "heavy": 3,        # passes in the heavy line
    "title_h": 6.5,    # title cap height, mm
    "title_w": 0.5,    # title stroke weight, mm (giant_type band)
    "colo_h": 2.2,     # colophon cap height, mm
    "fade_c": 0.4,     # band threshold cos(dPhase) at the screen below the pair
    "c_min": -0.6,     # never draw closer to a node than this (nodes stay paper)
}

LAST_RUNS: dict = {}   # diagnostics of the last call (read by the NOTES measurements)

PAR_COS = 0.906   # cos 25 deg — the r01 guard's parallel test, now a regime boundary


def attention_one_field(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    """Deterministic: ``rng`` is accepted for the contract; nothing is random."""
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    P = LAYOUT
    fold = fold_packets()

    L = P["L"]
    k = 2 * math.pi / L
    d = P["N"] * L
    mx, my = x0 + P["mid_u"] * W, y0 + P["mid_v"] * H
    ta = math.radians(P["tilt"])
    u = np.array([math.cos(ta), math.sin(ta)])        # Q -> K
    nrm = np.array([-u[1], u[0]])
    Qs = np.array([mx, my]) - u * d / 2
    Ks = np.array([mx, my]) + u * d / 2
    phiQ, phiK = fold["phiQ"], fold["phiK"]
    an = max(fold["aQ"], fold["aK"])
    aQ, aK = fold["aQ"] / an, fold["aK"] / an
    dphi = phiQ - phiK
    phibar = (phiQ + phiK) / 2
    dstar = math.acos(P["c_min"])                      # widest band ever drawn

    # ---- the cut: softmax of the cross-term along the screen ------------
    ys = y0 + P["screen_v"] * H
    xs = np.arange(x0, x1 + 1e-9, 0.25)
    rQ = np.hypot(xs - Qs[0], ys - Qs[1])
    rK = np.hypot(xs - Ks[0], ys - Ks[1])
    r0 = float(my - ys)
    c = np.cos(k * (rQ - rK) + dphi) * np.sqrt(r0 * r0 / (rQ * rK))
    logit = P["beta"] * c
    a = np.exp(logit - logit.max())
    a /= a.sum()
    h = P["peak_h"] * a / a.max()
    curve_y = ys + h

    halos: List[Tuple[float, float, float, float]] = []

    def inside(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        ok = (X >= x0) & (X <= x1) & (Y <= y1) & (Y >= np.interp(X, xs, curve_y))
        for hx0, hy0, hx1, hy1 in halos:
            ok &= ~((X >= hx0) & (X <= hx1) & (Y >= hy0) & (Y <= hy1))
        return ok

    def geom(X, Y):
        ax_, ay_ = X - Qs[0], Y - Qs[1]
        bx_, by_ = X - Ks[0], Y - Ks[1]
        ra, rb = np.hypot(ax_, ay_) + 1e-9, np.hypot(bx_, by_) + 1e-9
        cosang = np.abs(ax_ * bx_ + ay_ * by_) / (ra * rb)
        cosd = np.cos(k * (ra - rb) + dphi)
        return cosang >= PAR_COS, cosd, ra, rb

    # The bright fringe is drawn where the time-averaged intensity
    #   I = A_Q^2 + A_K^2 + 2 A_Q A_K cos(dPhase),  A_s = a_s / sqrt(r_s)
    # clears one absolute level I_th — so the rays taper as the wave spreads.
    # I_th is fixed by asking for cos(dPhase) >= fade_c at the screen point
    # straight below the pair.  Nodes are always paper (cos >= c_min floor).
    fq, fk = math.hypot(mx - Qs[0], ys - Qs[1]), math.hypot(mx - Ks[0], ys - Ks[1])
    AQf, AKf = aQ / math.sqrt(fq), aK / math.sqrt(fk)
    I_th = AQf ** 2 + AKf ** 2 + 2 * AQf * AKf * P["fade_c"]

    def c_needed(ra, rb):
        AQ_, AK_ = aQ / np.sqrt(ra), aK / np.sqrt(rb)
        return np.clip((I_th - AQ_ ** 2 - AK_ ** 2) / (2 * AQ_ * AK_), P["c_min"], 2.0)

    def keep_colour(X, Y):
        par = geom(X, Y)[0]
        return inside(X, Y) & ~par

    def keep_black(X, Y):
        par, cosd, ra, rb = geom(X, Y)
        return inside(X, Y) & par & (cosd >= c_needed(ra, rb))

    qp, kp, bk, tp = (_pen(Q_PEN, colors), _pen(K_PEN, colors),
                      _pen(BLACK, colors), _pen(TYPE, colors))

    # ---- labels: Q and K beside their sources, with halos ---------------
    lab_h = 5.0
    lab_w = _text_width("Q", lab_h)
    q_lab = (Qs[0] - 3.2 - lab_w, Qs[1] - lab_h / 2)
    k_lab = (Ks[0] + 3.2, Ks[1] - lab_h / 2)
    for lx, ly in (q_lab, k_lab):
        halos.append((lx - 1.2, ly - 1.2, lx + lab_w + 1.2, ly + lab_h + 1.2))

    corners = np.array([(x0, y0), (x1, y0), (x0, y1), (x1, y1)])
    strokes = {qp: [], kp: [], bk: []}

    # ---- colour: each wave's own crests, where the two disagree ----------
    for src, phi, pen in ((Qs, phiQ, qp), (Ks, phiK, kp)):
        rmax = float(np.max(np.hypot(*(corners - src).T)))
        flip = False
        for m in range(1, int(rmax / L) + 3):
            r = (m - phi / (2 * math.pi)) * L
            if r <= 0.3 or r > rmax:
                continue
            n = max(64, int(2 * math.pi * r / 0.3))
            t = np.linspace(0.0, 2 * math.pi, n + 1)
            ring = np.stack([src[0] + r * np.cos(t), src[1] + r * np.sin(t)], 1)
            if flip:
                ring = ring[::-1]
            flip = not flip
            for run in _mask_runs(ring, keep_colour):
                strokes[pen].append(run)

    # ---- black: crests of the SUM, where the two agree --------------------
    # In agreement band j (k h + dphi = 2 pi j + delta, |delta| <= dstar) the
    # crest of psi is s = r_Q + r_K = 2 (2 pi n - pi j - phibar - eps) / k with
    # eps = atan2((A_Q - A_K) sin(delta/2), (A_Q + A_K) cos(delta/2)) — exact,
    # solved by fixed point along each hyperbola h = r_Q - r_K.
    smax = float(np.max(np.hypot(*(corners - Qs).T) + np.hypot(*(corners - Ks).T)))
    jlo = int(math.floor((-k * d + dphi - dstar) / (2 * math.pi)))
    jhi = int(math.ceil((k * d + dphi + dstar) / (2 * math.pi)))
    for j in range(jlo, jhi + 1):
        hlo = max(-d, (2 * math.pi * j - dstar - dphi) / k)
        hhi = min(d, (2 * math.pi * j + dstar - dphi) / k)
        if hhi <= hlo:
            continue
        hh = np.linspace(hlo, hhi, 1400)
        delta = k * hh + dphi - 2 * math.pi * j
        nlo = int(math.floor((k * d / 2 + math.pi * j + phibar - 1) / (2 * math.pi)))
        nhi = int(math.ceil((k * smax / 2 + math.pi * j + phibar + 1) / (2 * math.pi)))
        for n in range(nlo, nhi + 1):
            eps = np.zeros_like(hh)
            for _ in range(4):
                s = 2 * (2 * math.pi * n - math.pi * j - phibar - eps) / k
                rq = np.maximum((s + hh) / 2, 1e-6)
                rk = np.maximum((s - hh) / 2, 1e-6)
                AQ, AK = aQ / np.sqrt(rq), aK / np.sqrt(rk)
                eps = np.arctan2((AQ - AK) * np.sin(delta / 2), (AQ + AK) * np.cos(delta / 2))
            s = 2 * (2 * math.pi * n - math.pi * j - phibar - eps) / k
            rq, rk = (s + hh) / 2, (s - hh) / 2
            along = (s * hh + d * d) / (2 * d)
            b2 = rq * rq - along * along
            ok = (rq > 0) & (rk > 0) & (b2 > 0)
            if ok.sum() < 2:
                continue
            for sgn in (1.0, -1.0):
                bb = sgn * np.sqrt(np.where(ok, b2, 0.0))
                pts = Qs[None, :] + along[:, None] * u[None, :] + bb[:, None] * nrm[None, :]
                # split where the hyperbola leaves the valid range
                idx = np.nonzero(ok)[0]
                breaks = np.nonzero(np.diff(idx) > 1)[0]
                for seg in np.split(idx, breaks + 1):
                    if len(seg) < 2:
                        continue
                    for run in _mask_runs(pts[seg], keep_black):
                        strokes[bk].append(_decimate(run))

    LAST_RUNS.clear()
    LAST_RUNS.update({"Q": strokes[qp], "K": strokes[kp], "SUM": strokes[bk],
                      "fold": fold, "Qs": Qs, "Ks": Ks, "xs": xs, "a": a, "ys": ys})
    out: List[GCodeCommand] = []
    for pen in (qp, kp, bk):
        for run in _order(strokes[pen]):
            out += _emit(run, pen)
    # the two sources
    out += fill_disc(float(Qs[0]), float(Qs[1]), 1.1, spacing=0.3, pen=qp)
    out += fill_disc(float(Ks[0]), float(Ks[1]), 1.1, spacing=0.3, pen=kp)
    out += giant_type("Q", q_lab[0], q_lab[1], lab_h, pen=qp, weight=0.3, tip=0.3)
    out += giant_type("K", k_lab[0], k_lab[1], lab_h, pen=kp, weight=0.3, tip=0.3)

    # ---- the heavy line ----------------------------------------------------
    curve = [(float(x), float(y)) for x, y in zip(xs[::2], curve_y[::2])]
    for p in range(P["heavy"]):
        off = -0.33 * p
        pas = _offset_polyline(curve, off) if off else curve
        out += _poly(pas if p % 2 == 0 else pas[::-1], color=bk, f=2200)   # serpentine passes

    # ---- type (own layer) --------------------------------------------------
    # Swiss block, flush left on the sheet edge x0: title, then two colophon
    # lines whose every number is computed above.
    th = P["title_h"]
    ch = P["colo_h"]
    base = y0 + 1.0
    qi, kj = fold["i"], fold["j"]
    l1 = ("q \u00b7 k = |q| |k| cos(2\u03a0(rQ \u2212 rK)/\u03bb %s %.2f)"
          % ("+" if dphi >= 0 else "\u2212", abs(dphi)))
    l2 = ("Q%d \u00b7 K%d   cos %.3f   \u03bb %.1f mm   d = %d\u03bb   \u03b2 %g   after Thomas Young, 1807"
          % (qi + 1, kj + 1, float(fold["C"][qi, kj]), L, P["N"], P["beta"]))
    out += _stroke_text(l2, x0, base, ch, color=tp, f=2200)
    out += _stroke_text(l1, x0, base + ch * 2.1, ch, color=tp, f=2200)
    out += giant_type("ATTENTION AS RESONANCE", x0, base + ch * 2.1 + ch * 2.6, th,
                      pen=tp, weight=P["title_w"], tip=0.25)
    return out
