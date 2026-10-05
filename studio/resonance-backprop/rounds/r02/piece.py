"""ATTENTION AS RESONANCE — THE FOLD (resonance-backprop r02, thesis ``the fold``).

The mirror is the whole plate.  Above one horizontal line, the forward pass:
two coherent point sources, Q (crimson) and K (blue), each drawn as its own
family of Huygens crest circles.  Below it, the backward pass: the same two
waves reflected in the line.  Nothing else is on the sheet except the line
itself (green: Z, where the loss is read), the attention weights strung on it
as goldenrod beads (V), and the left rail with its two words.

The twist is the colours.  Below the line the crimson and blue have changed
places, because that is what the gradient of a resonance does:

    s = Re(q . conj(k))            (the dot product of two phasors)
    dL/dq = C . k                  dL/dk = conj(C) . q

The gradient that arrives at Q is K's wave, and the gradient that arrives at K
is Q's wave, time-reversed (conjugated).  So the source sitting under Q radiates
BLUE and the source sitting under K radiates CRIMSON: colour says whose wave it
is, position says whose gradient it is.

The maths (every number below is computed in this file, nothing traced)
------------------------------------------------------------------------
PACKETS -> SOURCES.  The five Q rows and five K rows of the parent plate (r01,
measured off the reference) are real signals q_i(xi), k_j(xi), xi measured from
each block's node column toward the centre.  Their dot products are overlap
integrals S_ij.  The pair with the highest cosine is taken (Q row 1, K row 5,
cos 0.908), and each is folded into ONE complex amplitude, its Fourier
coefficient at the resonant carrier w0 = argmax_w |Qhat(w) Khat(w)| — the
family's construction (resonance r04), re-derived from this plate's packets.
Parseval is checked to 1e-8.

THE FIELD.  psi_s(x) = a_s e^{i(k r_s + phi_s)} / sqrt(r_s).  Crest loci are
circles r = (m - phi_s / 2 pi) L.  The sources sit an exact whole number of
wavelengths apart (d = N L, the approved family construction).

THE HEAD.  Keys are tokens strung along the fold at x_j.  Each token's score is
the resonance of the two waves arriving there,

    s_j = beta . Re( q G_Q(x_j) . conj(k G_K(x_j)) ) / S0,   G = e^{ikr}/sqrt(r)

a = softmax(s).  Values v_j are the parent plate's third V packet row sampled
at the tokens; Z = sum a_j v_j; the loss asks the head to retrieve the loudest
value, L = (Z - max v)^2 / 2.

THE BACKWARD PASS.  dL/dZ = Z - z*, dL/dv_j = a_j dL/dZ, dL/da_j = v_j dL/dZ,
g_j = dL/ds_j = a_j (dL/da_j - sum a dL/da).  With Wirtinger gradients
(dL/dRe + i dL/dIm), exactly:

    dL/dq = C k,   dL/dk = conj(C) q,   C = (beta/S0) sum_j g_j conj(G_Qj) G_Kj

(checked against central finite differences in ``_fd_check``, rel. err 1e-8).
Below the fold each gradient radiates from its source's mirror image.  |C| is
the one scalar the loss contributes to every gradient; the lower half is
drawn normalised by it, so what the drawing shows is arg C: every lower ring
slips by arg C / 2 pi of a wavelength, in opposite senses on the two sides
(C against conj C), and the moire bands break where they cross the line.

V IS THE ONE TENSOR THE FOLD MAPS ONTO ITSELF.  dL/dv_j = a_j dL/dZ has
attention's own shape, so the forward read and the backward write of every
value are the same size: a bead, which is its own mirror image.

Lineage: Sol LeWitt, *Arcs, Circles & Grids* (1972) — families of concentric
arcs from fixed points, superimposed by a stated rule.  The rule here is the
chain rule: reflect, swap, conjugate.

Pens (render palette goldenrod,dodgerblue,crimson,forestgreen,black — the index
IS the stream order, light to dark):
    0 goldenrod  V: attention beads (= dL/dV)
    1 blue       K's wave: K above, dL/dQ below-left
    2 crimson    Q's wave: Q above, dL/dK below-right
    3 green      Z: the fold, where the loss is read
    4 black      the rail and its two words

Entry point: ``resonance_the_fold``.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import _poly, giant_type
from promptplot.generative.generators import _text_width
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]

V_PEN, K_PEN, Q_PEN, Z_PEN, INK = 0, 1, 2, 3, 4


def _pen(idx: int, colors: int) -> Optional[int]:
    if colors <= 1:
        return None
    return min(idx, colors - 1)


# ---------------------------------------------------------------------------
# 1. the parent's packets (r01, measured off the reference, reference px)
# ---------------------------------------------------------------------------

Lobe = Tuple[float, float, float, float, float]  # centre, sigma, amp, period, phase

Q_HOME = 127.0
K_HOME = 2 * 561.0 - Q_HOME        # r01 mirrors the node column about x = 561
Q_LOBES: List[List[Lobe]] = [
    [(228.0, 29.0, 40.0, 11.4, 0.0), (172.0, 11.0, 6.0, 8.4, 1.1)],
    [(196.0, 23.0, 32.0, 9.6, 0.4), (324.0, 13.0, 15.0, 9.0, 2.2)],
    [(250.0, 31.0, 40.0, 14.6, 0.7), (196.0, 15.0, 10.0, 9.6, 0.2),
     (330.0, 15.0, 14.0, 10.2, 1.5)],
    [(206.0, 26.0, 30.0, 9.8, 0.9), (330.0, 12.0, 13.0, 9.4, 0.3)],
    [(240.0, 30.0, 38.0, 10.8, 0.5), (176.0, 12.0, 6.0, 8.2, 2.0)],
]
K_LOBES: List[List[Lobe]] = [
    [(892.0, 28.0, 38.0, 11.0, 0.5), (952.0, 12.0, 8.0, 8.6, 1.6)],
    [(922.0, 24.0, 33.0, 9.4, 1.2), (798.0, 13.0, 14.0, 9.2, 0.3)],
    [(870.0, 31.0, 40.0, 15.0, 0.2), (930.0, 15.0, 11.0, 9.8, 1.4),
     (792.0, 14.0, 13.0, 10.0, 2.3)],
    [(916.0, 26.0, 29.0, 10.2, 2.0), (790.0, 12.0, 13.0, 9.0, 1.0)],
    [(880.0, 30.0, 39.0, 11.2, 1.5), (946.0, 12.0, 6.0, 8.4, 0.7)],
]
# r01's third V row (the one with the filled home node)
V_LOBES: List[Lobe] = [(184.0, 23.0, 24.0, 9.6, 0.6), (140.0, 14.0, 10.0, 7.4, 2.0)]


def _packet(lobes: Sequence[Lobe], x: np.ndarray) -> np.ndarray:
    """r01's packet: sum of gaussian-enveloped sine carriers."""
    v = np.zeros_like(x)
    for c, sg, a, per, ph in lobes:
        v += a * np.exp(-0.5 * ((x - c) / sg) ** 2) * np.sin(2 * np.pi * (x - c) / per + ph)
    return v


def fold_packets() -> Dict[str, object]:
    """Score matrix, best pair, resonant carrier, source phasors."""
    dxi = 0.25
    xi = np.arange(0.0, 500.0, dxi)
    Q = [_packet(l, Q_HOME + xi) for l in Q_LOBES]
    K = [_packet(l, K_HOME - xi) for l in K_LOBES]     # K rows run right to left
    S = np.array([[float(np.sum(q * k) * dxi) for k in K] for q in Q])
    qn = np.array([math.sqrt(float(np.sum(q * q) * dxi)) for q in Q])
    kn = np.array([math.sqrt(float(np.sum(k * k) * dxi)) for k in K])
    cos = S / np.outer(qn, kn)
    i, j = np.unravel_index(int(np.argmax(cos)), cos.shape)
    ws = np.linspace(0.2, 1.2, 4001)
    E = np.exp(-1j * np.outer(ws, xi))
    Qh = E @ Q[i] * dxi
    Kh = E @ K[j] * dxi
    b = int(np.argmax(np.abs(Qh * Kh)))
    parseval = float(np.real(Qh * np.conj(Kh)).sum() * (ws[1] - ws[0]) / math.pi)
    return {
        "cos": cos, "i": int(i), "j": int(j), "S": float(S[i, j]), "parseval": parseval,
        "w0": float(ws[b]), "lam_px": 2 * math.pi / float(ws[b]),
        "q": complex(Qh[b]), "k": complex(Kh[b]),
    }


# ---------------------------------------------------------------------------
# 2. layout (fractions of the drawable area; the plate is paper-agnostic)
# ---------------------------------------------------------------------------

LAYOUT = {
    "L": 3.0,          # crest pitch, mm: the one resonant wavelength
    "N": 30,           # d = N L: whole wavelengths between the sources
    "q_u": 0.22,       # Q, fraction of drawable width
    "q_h": 9.0,        # Q's height above the fold, mm (its image the same below)
    "tilt": 36.0,      # the Q->K axis, degrees above horizontal
    "fold_v": 0.50,    # the fold, fraction of drawable height from the bottom
    "reach": 88.0,     # radius where the larger forward wave falls to threshold, mm
    "rail_dx": 5.0,    # rail inset from the drawable left edge, mm
    "field_gap": 6.0,  # field clip right of the rail, mm
    "tok": 4.0,        # token pitch along the fold, mm
    "bead": 1.7,       # largest bead radius, mm (< tok/2: beads never touch)
    "bead_min": 0.8,   # smaller beads would sit inside the fold's ink band
    "beta": 6.0,       # inverse temperature of the softmax
    "rail_h": 2.6,     # rail type cap height, mm
    "fold_passes": 3,  # the fold line weight
    "pass_dr": 0.25,   # offset of a crest's extra ink passes, mm
}


# ---------------------------------------------------------------------------
# 3. the head: forward, backward, gradient check
# ---------------------------------------------------------------------------

def _green(r: np.ndarray, lam: float) -> np.ndarray:
    return np.exp(1j * (2 * math.pi / lam) * r) / np.sqrt(r)


def head(q: complex, k: complex, xs: np.ndarray, yF: float, Qp: Pt, Kp: Pt,
         lam: float, beta: float) -> Dict[str, object]:
    GQ = _green(np.hypot(xs - Qp[0], Qp[1] - yF), lam)
    GK = _green(np.hypot(xs - Kp[0], Kp[1] - yF), lam)
    w = GQ * np.conj(k * GK)
    S0 = float(np.max(np.abs(q * w)))
    s = beta * np.real(q * w) / S0
    a = np.exp(s - s.max())
    a /= a.sum()
    xv0 = min(c - 3.1 * sg for c, sg, *_ in V_LOBES)
    xv1 = max(c + 3.1 * sg for c, sg, *_ in V_LOBES)
    v = _packet(V_LOBES, np.linspace(xv0, xv1, len(xs)))
    v = v / float(np.max(np.abs(v)))
    Z = float(np.sum(a * v))
    zstar = float(np.max(v))
    dZ = Z - zstar
    loss = 0.5 * dZ * dZ
    dv = a * dZ
    da = v * dZ
    g = a * (da - float(np.sum(a * da)))
    C = complex(np.sum(g * (beta / S0) * np.conj(GQ) * GK))

    def L_of(qq: complex, kk: complex) -> float:
        w_ = GQ * np.conj(kk * GK)
        s_ = beta * np.real(qq * w_) / S0
        a_ = np.exp(s_ - s_.max())
        a_ /= a_.sum()
        return 0.5 * (float(np.sum(a_ * v)) - zstar) ** 2

    return {"a": a, "s": s, "v": v, "Z": Z, "zstar": zstar, "loss": loss, "dZ": dZ,
            "dv": dv, "g": g, "C": C, "dq": C * k, "dk": C.conjugate() * q,
            "S0": S0, "L_of": L_of}


def _fd_check(h: Dict[str, object], q: complex, k: complex) -> Tuple[float, float]:
    """Central finite differences of L against the closed-form C k, conj(C) q."""
    L_of = h["L_of"]
    e = 1e-4 * abs(q)
    fq = ((L_of(q + e, k) - L_of(q - e, k)) + 1j * (L_of(q + 1j * e, k) - L_of(q - 1j * e, k))) / (2 * e)
    fk = ((L_of(q, k + e) - L_of(q, k - e)) + 1j * (L_of(q, k + 1j * e) - L_of(q, k - 1j * e))) / (2 * e)
    return abs(fq - h["dq"]) / abs(h["dq"]), abs(fk - h["dk"]) / abs(h["dk"])


# ---------------------------------------------------------------------------
# 4. exact arc clipping
# ---------------------------------------------------------------------------

TAU = 2 * math.pi
Interval = Tuple[float, float]


def _cos_set(alpha: float, kappa: float) -> Optional[List[Interval]]:
    """{t : cos(t - alpha) >= kappa} on [0, 2pi).  None = everything."""
    if kappa <= -1.0:
        return None
    if kappa >= 1.0:
        return []
    b = math.acos(kappa)
    s = (alpha - b) % TAU
    e = s + 2 * b
    if e <= TAU:
        return [(s, e)]
    return [(s, TAU), (0.0, e - TAU)]


def _intersect(A: List[Interval], B: List[Interval]) -> List[Interval]:
    out = []
    for a0, a1 in A:
        for b0, b1 in B:
            lo, hi = max(a0, b0), min(a1, b1)
            if hi > lo:
                out.append((lo, hi))
    return sorted(out)


def arc_intervals(cx: float, cy: float, r: float,
                  planes: Sequence[Tuple[float, float, float]],
                  holes: Sequence[Tuple[float, float, float]]) -> List[Interval]:
    """Angular intervals of the circle (cx, cy, r) that satisfy every
    half-plane n.p >= b (n unit) and lie outside every hole (x, y, rho).
    Closed-form, so a crest stops exactly ON the fold, the frame or a halo."""
    I: List[Interval] = [(0.0, TAU)]
    for nx, ny, b in planes:
        S = _cos_set(math.atan2(ny, nx), (b - (nx * cx + ny * cy)) / r)
        if S is not None:
            I = _intersect(I, S)
        if not I:
            return []
    for hx, hy, rho in holes:
        dx, dy = cx - hx, cy - hy
        D = math.hypot(dx, dy)
        if D < 1e-9:
            if r <= rho:
                return []
            continue
        # |c + r u - h|^2 >= rho^2  <=>  (c-h).u >= (rho^2 - D^2 - r^2) / (2r)
        S = _cos_set(math.atan2(dy, dx), (rho * rho - D * D - r * r) / (2 * r * D))
        if S is not None:
            I = _intersect(I, S)
        if not I:
            return []
    # join the wrap so a ring that survives across angle 0 stays one stroke
    if len(I) >= 2 and I[0][0] <= 1e-12 and I[-1][1] >= TAU - 1e-12:
        first = I.pop(0)
        last = I.pop()
        I.append((last[0], last[1] + first[1]))
    return I


# ---------------------------------------------------------------------------
# 5. crossing-safe anti-crowding (the family's _Guard, 0.82 mm / 25 deg)
# ---------------------------------------------------------------------------

class _Guard:
    """Drop a point only when another stroke runs within ``sep`` AND within
    25 degrees of parallel, so every genuine crossing survives."""

    def __init__(self, sep: float = 0.82) -> None:
        self.sep = sep
        self.s2 = sep * sep
        self.g: dict = {}

    def ok(self, x: float, y: float, ux: float, uy: float, sid: int) -> bool:
        cx, cy = int(x // self.sep), int(y // self.sep)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for qx, qy, qu, qv, qs in self.g.get((cx + dx, cy + dy), ()):
                    if qs == sid or abs(ux * qu + uy * qv) < 0.906:
                        continue
                    if (qx - x) ** 2 + (qy - y) ** 2 < self.s2:
                        return False
        return True

    def add(self, x: float, y: float, ux: float, uy: float, sid: int) -> None:
        self.g.setdefault((int(x // self.sep), int(y // self.sep)), []).append(
            (x, y, ux, uy, sid))

    def add_line(self, pts: Sequence[Pt], sid: int, step: float = 0.3) -> None:
        for (ax, ay), (bx, by) in zip(pts[:-1], pts[1:]):
            d = math.hypot(bx - ax, by - ay)
            if d < 1e-9:
                continue
            ux, uy = (bx - ax) / d, (by - ay) / d
            n = max(1, int(d / step))
            for t in range(n + 1):
                self.add(ax + (bx - ax) * t / n, ay + (by - ay) * t / n, ux, uy, sid)


# ---------------------------------------------------------------------------
# 6. marks
# ---------------------------------------------------------------------------

def _arc_pts(cx: float, cy: float, r: float, t0: float, t1: float, step: float) -> List[Pt]:
    n = max(2, int(math.ceil((t1 - t0) * r / step)))
    return [(cx + r * math.cos(t0 + (t1 - t0) * i / n), cy + r * math.sin(t0 + (t1 - t0) * i / n))
            for i in range(n + 1)]


def _len(pts: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts[:-1], pts[1:]))


def _decimate(pts: List[Pt], r: float) -> List[Pt]:
    """Keep vertices at the chord step that holds a 0.01 mm sagitta on radius r."""
    step = min(1.5, max(0.25, math.sqrt(8.0 * r * 0.01)))
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= step:
            out.append(b)
            acc = 0.0
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def _inside(px: float, py: float, planes, holes) -> bool:
    for nx, ny, b in planes:
        if nx * px + ny * py < b:
            return False
    for hx, hy, rho in holes:
        if (px - hx) ** 2 + (py - hy) ** 2 < rho * rho:
            return False
    return True


def _weighted(cur: List[Pt], cx: float, cy: float, r: float, amp: float,
              planes, holes, dr: float) -> List[Pt]:
    """One crest run with its WEIGHT from the field: ink passes = floor(a / theta),
    where a / theta = sqrt(R / r) is the wave's amplitude on this crest in units
    of the reach threshold (1 pass at the rim, 2 inside R/4, 3 inside R/9).
    The extra passes sit dr off the crest and are chained back and forth into
    ONE pen-down, so weight costs draw length, never a pen cycle."""
    n = max(1, min(3, int(amp)))
    base = _decimate(cur, r)
    out = list(base)
    fwd = False
    for k in range(1, n):
        rr = r + (dr if k == 1 else -dr)
        sc = rr / r
        lane = [(cx + (x - cx) * sc, cy + (y - cy) * sc) for x, y in base]
        lane = [p for p in lane if _inside(p[0], p[1], planes, holes)]
        if len(lane) < 2:
            continue
        out += lane if fwd else lane[::-1]
        fwd = not fwd
    return out


def disc(cx: float, cy: float, r: float, pen: Optional[int], pitch: float = 0.3) -> List[Pt]:
    """A solid disc as ONE pen-down: an inward spiral closed by its rim."""
    turns = max(1, int(math.ceil(r / pitch)))
    n = turns * 36
    pts = [(cx + r * math.cos(TAU * i / 48), cy + r * math.sin(TAU * i / 48)) for i in range(49)]
    for i in range(n + 1):
        t = i / n
        rr = r * (1 - t)
        a = TAU * turns * t
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


def _order(runs: List[List[Pt]], start: Pt) -> List[List[Pt]]:
    """Greedy nearest-neighbour WITH reversal: each layer streams as one walk."""
    if not runs:
        return []
    S = np.array([r[0] for r in runs])
    E = np.array([r[-1] for r in runs])
    alive = np.ones(len(runs), bool)
    pos = np.array(start, float)
    out: List[List[Pt]] = []
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
        out.append(list(run))
        pos = np.array(run[-1])
    return out


# ---------------------------------------------------------------------------
# 7. the plate
# ---------------------------------------------------------------------------

def build(bounds: Bounds, lay: Optional[dict] = None) -> Dict[str, object]:
    """Everything the plate draws, as mm polylines per semantic pen, plus the
    numbers (for NOTES)."""
    P = dict(LAYOUT)
    if lay:
        P.update(lay)
    x0, y0, x1, y1 = bounds
    W, H = x1 - x0, y1 - y0
    lam = P["L"]
    d = P["N"] * lam
    yF = y0 + P["fold_v"] * H
    tl = math.radians(P["tilt"])
    xQ, yQ = x0 + P["q_u"] * W, yF + P["q_h"]
    xK, yK = xQ + d * math.cos(tl), yQ + d * math.sin(tl)
    rail_x = x0 + P["rail_dx"]
    fx0 = rail_x + P["field_gap"]

    fp = fold_packets()
    q, k = fp["q"], fp["k"]

    # tokens along the fold
    n_tok = int((x1 - fx0) // P["tok"])
    off = (x1 - fx0 - (n_tok - 1) * P["tok"]) / 2
    xs = fx0 + off + P["tok"] * np.arange(n_tok)
    hd = head(q, k, xs, yF, (xQ, yQ), (xK, yK), lam, P["beta"])
    fd = _fd_check(hd, q, k)
    C = hd["C"]

    # the four sources: (x, y, phasor, pen, half)
    # reach R = (a / theta)^2, theta fixed by the larger forward amplitude
    amax = max(abs(q), abs(k))
    theta = amax / math.sqrt(P["reach"])
    dq_n, dk_n = hd["dq"] / abs(C), hd["dk"] / abs(C)
    sources = [
        ("Q", xQ, yQ, q, Q_PEN, +1),
        ("K", xK, yK, k, K_PEN, +1),
        ("dL/dQ", xQ, 2 * yF - yQ, dq_n, K_PEN, -1),     # Q's gradient is K's wave
        ("dL/dK", xK, 2 * yF - yK, dk_n, Q_PEN, -1),     # K's gradient is Q's wave, conjugated
    ]

    # beads: V, radius from attention (area ~ a_j)
    amax_tok = float(np.max(hd["a"]))
    beads = []
    for x, a in zip(xs, hd["a"]):
        r = P["bead"] * math.sqrt(a / amax_tok)
        if r >= P["bead_min"]:
            beads.append((float(x), yF, r))

    src_r = 0.9
    holes = [(bx, by, br + 0.5) for bx, by, br in beads]
    holes += [(sx, sy, src_r + 0.6) for _, sx, sy, *_ in sources]

    guard = _Guard(0.82)
    fold_pts = [(rail_x, yF), (x1, yF)]
    guard.add_line(fold_pts, sid=-1)

    # crest runs, emitted interleaved by m so no family always wins the guard
    fam_rings = []
    for name, sx, sy, ph, pen, half in sources:
        R = (abs(ph) / theta) ** 2
        phi = math.atan2(ph.imag, ph.real)
        planes = [(1.0, 0.0, fx0), (-1.0, 0.0, -x1), (0.0, 1.0, y0), (0.0, -1.0, -y1),
                  (0.0, float(half), half * yF)]
        rings = []
        m = 0
        while True:
            m += 1
            r = (m - phi / TAU) * lam
            if r > R:
                break
            if r < 2.0:
                continue
            rings.append(r)
        fam_rings.append((name, sx, sy, pen, planes, rings, R, phi))

    runs: Dict[int, List[List[Pt]]] = {V_PEN: [], K_PEN: [], Q_PEN: [], Z_PEN: [], INK: []}
    sid = 0
    stats = {"guard_dropped": 0, "crest_pts": 0}
    maxm = max(len(f[5]) for f in fam_rings)
    for mi in range(maxm):
        for name, sx, sy, pen, planes, rings, R, phi in fam_rings:
            if mi >= len(rings):
                continue
            r = rings[mi]
            for t0, t1 in arc_intervals(sx, sy, r, planes, holes):
                sid += 1
                pts = _arc_pts(sx, sy, r, t0, t1, 0.3)
                cur: List[Pt] = []
                for j, (px, py) in enumerate(pts):
                    qx, qy = pts[min(j + 1, len(pts) - 1)] if j + 1 < len(pts) else pts[j - 1]
                    du, dv = qx - px, qy - py
                    dn = math.hypot(du, dv) or 1.0
                    du, dv = du / dn, dv / dn
                    stats["crest_pts"] += 1
                    if guard.ok(px, py, du, dv, sid):
                        guard.add(px, py, du, dv, sid)
                        cur.append((px, py))
                    else:
                        stats["guard_dropped"] += 1
                        if len(cur) >= 2 and _len(cur) >= 1.5:
                            runs[pen].append(_weighted(cur, sx, sy, r, math.sqrt(R / r),
                                                       planes, holes, P["pass_dr"]))
                        cur = []
                if len(cur) >= 2 and _len(cur) >= 1.5:
                    runs[pen].append(_weighted(cur, sx, sy, r, math.sqrt(R / r),
                                               planes, holes, P["pass_dr"]))

    # sources: solid discs in their wave's colour
    for name, sx, sy, ph, pen, half in sources:
        runs[pen].append(disc(sx, sy, src_r, pen))

    # V beads
    for bx, by, br in beads:
        runs[V_PEN].append(disc(bx, by, br, V_PEN))

    # the fold (Z): passes 0.35 mm apart, alternating direction
    zline: List[Pt] = []
    for p in range(P["fold_passes"]):
        dy = (p - (P["fold_passes"] - 1) / 2) * 0.3
        seg = [(rail_x, yF + dy), (x1, yF + dy)]
        zline += seg if p % 2 == 0 else seg[::-1]
    runs[Z_PEN].append(zline)          # one pen-down, boustrophedon

    # the rail and its two words (black), reading top to bottom
    th = P["rail_h"]
    words = [("forward pass", (yF + y1) / 2), ("backward pass", (y0 + yF) / 2)]
    type_cmds: List[GCodeCommand] = []
    gaps = []
    for text, yc in words:
        wlen = _text_width(text, th, proportional=True)
        ytop = yc + wlen / 2
        type_cmds += giant_type(text, rail_x - th / 2, ytop, th, pen=INK, tip=0.2, weight=0.2,
                                angle=-90.0, proportional=True)
        gaps.append((yc - wlen / 2 - 1.6, ytop + 1.6))
    rail_segs = []
    ys = [y1] + [v for g in sorted(gaps, reverse=True) for v in (g[1], g[0])] + [y0]
    for a_, b_ in zip(ys[0::2], ys[1::2]):
        if a_ - b_ > 0.5:
            rail_segs.append([(rail_x, a_), (rail_x, b_)])
    runs[INK] += rail_segs

    return {
        "runs": runs, "type": type_cmds, "fp": fp, "head": hd, "fd": fd, "stats": stats,
        "geom": {"xQ": xQ, "yQ": yQ, "xK": xK, "yK": yK, "yF": yF, "d": d, "lam": lam,
                 "rail_x": rail_x, "fx0": fx0, "theta": theta},
        "families": [(f[0], f[3], f[6], f[7], len(f[5])) for f in fam_rings],
        "beads": beads, "xs": xs,
    }


def resonance_the_fold(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    """THE FOLD: attention's forward field above one line, its gradient below,
    the two waves swapped by the chain rule.  Seed-independent: every mark is
    computed, none sampled."""
    B = build(bounds)
    out: List[GCodeCommand] = []
    pos: Pt = (0.0, 0.0)
    for pen in (V_PEN, K_PEN, Q_PEN, Z_PEN, INK):
        ordered = _order(B["runs"][pen], pos)
        for run in ordered:
            out += _poly(run, color=_pen(pen, colors), f=2600)
        if pen == INK:
            out += [c.model_copy(update={"color": _pen(INK, colors)}) if c.color is not None else c
                    for c in B["type"]]
        if ordered:
            pos = ordered[-1][-1]
    return out
