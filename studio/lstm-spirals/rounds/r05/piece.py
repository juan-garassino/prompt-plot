"""LSTM — THE READOUT.  studio/lstm-spirals r05 (thesis: iterate, parent r04).

A real, trained 8-cell character LSTM (``lstm_weights.json``, trained by
``train_lstm.py`` beside this file) reads one proverb, once, at render time:

    THE PALEST INK IS BETTER THAN THE BEST MEMORY

and the plate draws its two memories and the gate that joins them.

The field is ONE complex potential, a pair of point vortices on one vertical axis,

    F(z) = c_b log(z - z_b) + c_r log(z - z_r),     rho = Re F,  sigma = Im F,

black (hidden state) above, red (cell state) below, a saddle between them.

  * RED  = the cell state c_t: ONE continuous line coiling outward from the red
    eye, exactly HALF A TURN PER LETTER (45 half-turns). The coil is isotropic
    (constant-shape, circular about the eye) and its ring gap is affine in the
    mean forget gate:  gap_t = G0 + K * fbar_t  (mm, unclamped).
  * BLACK = the hidden state h_t: one comet per letter, born at its letter on
    the black lobe's rim, falling toward the black eye and sweeping RMS(h_t) of
    a turn (tanh < 1: none closes). A newer comet cuts an older one where it
    comes within 1 mm. The comet's ROOT -- the stretch before its one 1 mm
    break -- is RMS(h_t) x ROOT_MM (8 mm) long and is never cut (every root is
    reserved before any comet is laid), so the true value survives the cut.
  * GREY = the output gate o_t, the readout h_t = o_t * tanh(c_t): one thread per
    letter from that letter's half-turn on the red coil to that letter's comet
    birth. Each thread leaves along the potential's orthogonal sigma-line (right
    angles to the rings, splitting at the saddle with the field), steps out along
    the lane metric's normal to its own lane (right angles to the lanes it
    crosses), rides that lane round the lobes -- lanes stack by destination and
    peel off letter by letter -- and dives in along the black sigma-line to its
    letter. All 45 pass the saddle's horizontal, 22 west and 23 east of it.
    Dashed: an integer number of ~8 mm periods, inked fraction = mean o_t.

Pen job: every layer is ordered here against a replica of the pipeline's
per-colour nearest neighbour on the emitted 0.01 mm grid -- red chunks seamed
due north of the eye (chain order, 0 mm between chunks), comets alternating
in/out round the rim, grey dashes and type repaired of stranded islands.

No randomness: weights + proverb determine the sheet; every seed is identical.

Contract: ``lstm_readout(rng, bounds, colors=4) -> list[GCodeCommand]``.
Pens (layer order = index order, light -> dark): 0 grey = output gate threads ·
1 crimson = cell-state line · 2 black = hidden-state comets · 3 black fine = type.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from statistics import median

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine.kit import Bounds, _pen, _poly, _stroke_text, _text_width, giant_type
from promptplot.generative.engine.geometry import erode_ring, signed_area, smooth_ring
from promptplot.generative.engine.scene3d import Occupancy
from promptplot.generative.generators import _GLYPHS

HERE = Path(__file__).resolve().parent
TWO_PI = 2.0 * math.pi

# the drawn mappings (also written into trace.json)
G0_MM = 0.8  # ring gap floor term
K_MM = 0.8  # ring gap per unit mean forget gate
ROOT_MM = 8.0  # comet root length per unit RMS(h)
DASH_MM = 8.0  # nominal thread dash period
R0_MM = 6.0  # the bare red eye
FAST = bool(__import__("os").environ.get("PP_FAST"))  # dev only: skip the pen-job search


# ---------------------------------------------------------------------------
# the LSTM -- the real forward pass of the trained weights
# ---------------------------------------------------------------------------


def run_lstm(path: Path = HERE / "lstm_weights.json") -> Dict[str, object]:
    """Forward pass over ``"." + target``. rows[0] is the start token."""
    d = json.loads(path.read_text())
    W, b = np.array(d["W"]), np.array(d["b"])
    H, vocab = int(d["hidden"]), d["vocab"]
    V = len(vocab)
    text = "." + d["target"]

    def sig(z):
        return 1.0 / (1.0 + np.exp(-z))

    h, c = np.zeros(H), np.zeros(H)
    rows = []
    for ch in text:
        x = np.zeros(V)
        x[vocab.index(ch)] = 1.0
        a = W @ np.concatenate([x, h]) + b
        i, f, o = sig(a[:H]), sig(a[H : 2 * H]), sig(a[2 * H : 3 * H])
        g = np.tanh(a[3 * H :])
        c_new = f * c + i * g
        h_new = o * np.tanh(c_new)
        nc = float(np.linalg.norm(c))
        rows.append(
            dict(
                ch=ch,
                i=i.tolist(), f=f.tolist(), o=o.tolist(), g=g.tolist(),
                c=c_new.tolist(), h=h_new.tolist(),
                f_mean=float(np.mean(f)), o_mean=float(np.mean(o)), i_mean=float(np.mean(i)),
                carry=float(np.linalg.norm(f * c)) / nc if nc > 1e-9 else 0.0,
                h_rms=float(np.sqrt(np.mean(h_new * h_new))),
                h_max=float(np.max(np.abs(h_new))),
                c_norm=float(np.linalg.norm(c_new)),
            )
        )
        h, c = h_new, c_new
    # retention: fraction of a write at step s still in cell j at step t is
    # prod_{u=s+1..t} f_u[j]. Horizon of a write = steps until even the most
    # retentive cell holds < 10 % of it.
    F = np.array([r["f"] for r in rows])  # (T+1, H)
    horizons = []
    for s in range(1, len(rows)):
        keep = np.ones(H)
        n = 0
        for t in range(s + 1, len(rows)):
            keep = keep * F[t]
            n += 1
            if keep.max() < 0.10:
                break
        else:
            n = None  # survives to the end of the sentence
        horizons.append(n)
    return dict(text=d["target"], rows=rows, hidden=H, horizons=horizons,
                loss=d.get("target_loss_nats_per_char"), acc=d.get("target_next_char_accuracy"))


# ---------------------------------------------------------------------------
# the field
# ---------------------------------------------------------------------------


class VortexPair:
    """F(z) = c_b log(z - z_b) + c_r log(z - z_r)."""

    def __init__(self, zb: complex, zr: complex, cb: float, cr: float):
        self.zb, self.zr, self.cb, self.cr = zb, zr, cb, cr
        self.saddle = (cb * zr + cr * zb) / (cb + cr)  # F'(z) = 0
        self.rho_s = self.rho(self.saddle)

    def rho(self, z: complex) -> float:
        return self.cb * math.log(abs(z - self.zb)) + self.cr * math.log(abs(z - self.zr))

    def dF(self, z: complex) -> complex:
        return self.cb / (z - self.zb) + self.cr / (z - self.zr)

    def grad(self, z: complex) -> complex:
        """grad rho as a complex number (= conj F')."""
        return self.dF(z).conjugate()

    def sig_ext(self, z: complex) -> float:
        """sigma, with both arguments cut straight DOWN from their eye: continuous
        all round the outside of the figure except below the red eye."""
        ab = math.atan2(z.imag - self.zb.imag, z.real - self.zb.real)
        ar = math.atan2(z.imag - self.zr.imag, z.real - self.zr.real)
        if ab < -math.pi / 2:
            ab += TWO_PI
        if ar < -math.pi / 2:
            ar += TWO_PI
        return self.cb * ab + self.cr * ar

    def u(self, z: complex) -> float:
        """first-order distance past the separatrix: (rho - rho_s) / |grad rho|."""
        return (self.rho(z) - self.rho_s) / max(1e-12, abs(self.dF(z)))


class Tracker:
    """Walks a curve given in (rho, sigma), arguments UNWRAPPED (from r04)."""

    def __init__(self, field: VortexPair, z0: complex):
        self.f = field
        self.z = z0
        self.tb = cmath.phase(z0 - field.zb)
        self.tr = cmath.phase(z0 - field.zr)

    @property
    def sigma(self) -> float:
        return self.f.cb * self.tb + self.f.cr * self.tr

    def _move(self, zn: complex) -> None:
        for attr, zc in (("tb", self.f.zb), ("tr", self.f.zr)):
            d = cmath.phase(zn - zc) - cmath.phase(self.z - zc)
            d = (d + math.pi) % TWO_PI - math.pi
            setattr(self, attr, getattr(self, attr) + d)
        self.z = zn

    def goto(self, rho_t: float, sig_t: float, max_dz: float = 0.5) -> complex:
        rho_c, sig_c = self.f.rho(self.z), self.sigma
        dw = complex(rho_t - rho_c, sig_t - sig_c)
        est = abs(dw / self.f.dF(self.z))
        n = max(1, int(math.ceil(est / max_dz)))
        for k in range(1, n + 1):
            tr_ = rho_c + (rho_t - rho_c) * k / n
            ts_ = sig_c + (sig_t - sig_c) * k / n
            for _it in range(6):
                res = complex(tr_ - self.f.rho(self.z), ts_ - self.sigma)
                step = res / self.f.dF(self.z)
                if abs(step) > max_dz:
                    step *= max_dz / abs(step)
                self._move(self.z + step)
                if abs(step) < 1e-9:
                    break
        return self.z


def _plen(pts) -> float:
    return sum(abs(pts[i] - pts[i - 1]) for i in range(1, len(pts)))


def _cut_at(pts: List[complex], length: float) -> Tuple[List[complex], List[complex]]:
    """Split a polyline at arc length ``length`` (the cut point is shared)."""
    acc = 0.0
    for i in range(1, len(pts)):
        seg = abs(pts[i] - pts[i - 1])
        if acc + seg >= length:
            u = (length - acc) / seg if seg > 0 else 0.0
            q = pts[i - 1] + (pts[i] - pts[i - 1]) * u
            return pts[:i] + [q], [q] + pts[i:]
        acc += seg
    return list(pts), [pts[-1]]


def _resample(pts: List[complex], step: float) -> List[complex]:
    out = [pts[0]]
    acc = 0.0
    for a, b in zip(pts, pts[1:]):
        seg = abs(b - a)
        if seg == 0:
            continue
        while acc + seg >= step:
            u = (step - acc) / seg
            a = a + (b - a) * u
            seg = abs(b - a)
            out.append(a)
            acc = 0.0
        acc += seg
    if abs(out[-1] - pts[-1]) > 1e-6:
        out.append(pts[-1])
    return out


def _cmd_strokes(cmds: List[GCodeCommand]) -> List[List[complex]]:
    """Commands (G0, M3, G1..., M5) back to polylines."""
    out, cur, pos, down = [], [], 0j, False
    for c in cmds:
        if c.command == "G0" and c.x is not None:
            pos = complex(c.x, c.y)
        elif c.command == "M3":
            down, cur = True, [pos]
        elif c.command == "G1" and down and c.x is not None:
            pos = complex(c.x, c.y)
            cur.append(pos)
        elif c.command == "M5":
            if down and len(cur) > 1:
                out.append(cur)
            down = False
    return out


def _q2(pts: List[complex]) -> List[complex]:
    """Round to the emitted gcode's 0.01 mm grid, so the pen-job simulation
    sees exactly what the pipeline's nearest-neighbour will see (greedy
    ordering flips on sub-0.01 mm ties)."""
    return [complex(round(z.real, 2), round(z.imag, 2)) for z in pts]


def _arc_slice(pts: List[complex], a: float, b: float) -> List[complex]:
    """The piece of a polyline between arc lengths a and b."""
    _, tail = _cut_at(pts, a)
    head, _ = _cut_at(tail, b - a)
    return head


# ---------------------------------------------------------------------------
# tracing on the field
# ---------------------------------------------------------------------------


def sigma_line(F: VortexPair, z: complex, stop, h: float = 0.25, maxn: int = 40000) -> List[complex]:
    """Walk +grad rho (an orthogonal sigma-line, outward) until stop(z)."""
    def d(q):
        v = F.grad(q)
        return v / abs(v)

    pts = [z]
    for _ in range(maxn):
        k1 = d(z)
        k2 = d(z + 0.5 * h * k1)
        k3 = d(z + 0.5 * h * k2)
        k4 = d(z + h * k3)
        zn = z + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if stop(zn):
            lo, hi = z, zn
            for _ in range(30):
                m = 0.5 * (lo + hi)
                if stop(m):
                    hi = m
                else:
                    lo = m
            pts.append(hi)
            return pts
        z = zn
        pts.append(z)
    raise RuntimeError("sigma-line did not reach its lane")


def normal_line(gfun, z: complex, stop, h: float = 0.25, maxn: int = 20000) -> List[complex]:
    """Walk along +grad of a scalar field (the lane-metric's normal) until stop."""
    pts = [z]
    for _ in range(maxn):
        g1 = gfun(z)
        zn = z + h * g1 / abs(g1)
        if stop(zn):
            lo, hi = z, zn
            for _ in range(30):
                m = 0.5 * (lo + hi)
                if stop(m):
                    hi = m
                else:
                    lo = m
            pts.append(hi)
            return pts
        z = zn
        pts.append(z)
    raise RuntimeError("normal line did not reach its lane")


def level_trace(phi, z: complex, sense: int, stop, h: float = 0.3, maxn: int = 6000) -> List[complex]:
    """Follow phi = 0 (phi increasing outward); sense +1 = clockwise."""
    e = 0.02

    def gphi(q):
        return complex(phi(q + e) - phi(q - e), phi(q + 1j * e) - phi(q - 1j * e)) / (2 * e)

    pts = [z]
    for _ in range(maxn):
        gz = gphi(z)
        zn = z + h * sense * (-1j) * gz / abs(gz)
        for _it in range(3):
            gn = gphi(zn)
            zn = zn - phi(zn) * gn / abs(gn) ** 2
        z = zn
        pts.append(z)
        if stop(z):
            return pts
    raise RuntimeError("lane ran away")


def fillet(pl: List[complex], ci: int, r: float) -> List[complex]:
    """Round the corner at index ci with a quadratic Bezier cut back r mm."""
    c = pl[ci]
    i = ci
    while i > 0 and abs(pl[i] - c) < r:
        i -= 1
    j = ci
    while j < len(pl) - 1 and abs(pl[j] - c) < r:
        j += 1
    a, b = pl[i], pl[j]
    n = max(6, int((abs(c - a) + abs(b - c)) / 0.3))
    arc = [(1 - u) ** 2 * a + 2 * (1 - u) * u * c + u * u * b for u in (k / n for k in range(n + 1))]
    return pl[:i] + arc + pl[j + 1 :]


# ---------------------------------------------------------------------------
# the silhouette and its exact offsets (the wraps)
# ---------------------------------------------------------------------------


class Silhouette:
    """The ink seen from a centre: per angular bin, the farthest ink point.

    ``radius(psi, d)`` is the far edge, along the ray at angle ``psi``, of the
    ink dilated by a disk of radius ``d`` -- the exact outward offset of the
    figure's star-shaped hull. Two levels d1 < d2 are therefore exactly
    d2 - d1 apart in EVERY direction: this is what makes the wraps isotropic.
    """

    def __init__(self, zc: complex, pts, nbins: int = 3600, blur_mm: float = 0.0):
        P = np.asarray(list(pts), complex) - zc
        rad = np.abs(P)
        b = (((np.angle(P) + math.pi) / TWO_PI) * nbins).astype(int) % nbins
        best = np.full(nbins, -1.0)
        np.maximum.at(best, b, rad)
        self.zc = zc
        self.lift = 0.0
        if blur_mm <= 0:
            keep = rad >= best[b] - 1e-9
            self.S = P[keep]
        else:
            # the farthest radius per bin, blurred over blur_mm of arc: takes
            # the raster staircase out of a closed hull (moves it < 0.1 mm)
            ok = best > 0
            idx = np.arange(nbins)
            best = np.interp(idx, idx[ok], best[ok], period=nbins)
            dpsi = TWO_PI / nbins
            sm = np.empty(nbins)
            for i in range(nbins):
                sg = max(1.0, blur_mm / max(best[i], 1.0) / dpsi)
                k = np.arange(-int(3 * sg), int(3 * sg) + 1)
                wt = np.exp(-0.5 * (k / sg) ** 2)
                sm[i] = float((best[(i + k) % nbins] * wt).sum() / wt.sum())
            psi = -math.pi + (idx + 0.5) * dpsi
            # lift the blurred outline by the most it dipped, so it never
            # passes inside the hull it smooths
            self.lift = float(np.max(best - sm))
            self.S = (sm + self.lift) * np.exp(1j * psi)
        self.rS = np.abs(self.S)

    def radius(self, psi, d) -> np.ndarray:
        psi = np.atleast_1d(np.asarray(psi, float))
        d = np.broadcast_to(np.asarray(d, float), psi.shape)
        out = np.empty_like(psi)
        for a in range(0, len(psi), 600):
            e = np.exp(-1j * psi[a:a + 600])[:, None]
            q = self.S[None, :] * e  # rotate so the ray is the +x axis
            proj, perp = q.real, np.abs(q.imag)
            dd = d[a:a + 600][:, None]
            reach = np.where((perp <= dd) & (proj > 0), proj + np.sqrt(np.maximum(0.0, dd * dd - perp * perp)), -np.inf)
            out[a:a + 600] = reach.max(axis=1)
        return out

    def point(self, psi, d) -> np.ndarray:
        psi = np.atleast_1d(np.asarray(psi, float))
        return self.zc + self.radius(psi, d) * np.exp(1j * psi)


def closed_hull(pts, rho: float, res: float = 0.25) -> np.ndarray:
    """Boundary points of the morphological CLOSING of the ink by a disk of
    radius rho (dilate, then erode): the figure's outline with every concavity
    narrower than 2*rho filled with a rho fillet -- the lanes' V at the waist
    becomes a round waist, the step where the crown lanes end becomes a ramp.
    Raster at ``res`` mm; the offsets taken from it are smooth for d >> res."""
    P = np.asarray(list(pts), complex)
    pad = rho + 3.0
    x0_, y0_ = P.real.min() - pad, P.imag.min() - pad
    nx = int((P.real.max() + pad - x0_) / res) + 1
    ny = int((P.imag.max() + pad - y0_) / res) + 1
    img = np.zeros((ny, nx))
    ix = np.clip(((P.real - x0_) / res).round().astype(int), 0, nx - 1)
    iy = np.clip(((P.imag - y0_) / res).round().astype(int), 0, ny - 1)
    img[iy, ix] = 1.0
    k = int(math.ceil(rho / res))
    yy, xx = np.mgrid[-k:k + 1, -k:k + 1]
    disk = ((xx * xx + yy * yy) * res * res <= rho * rho).astype(float)
    sh = (ny + 2 * k + 1, nx + 2 * k + 1)
    Kf = np.fft.rfft2(disk, sh)

    def conv(a):
        return np.fft.irfft2(np.fft.rfft2(a, sh) * Kf, sh)[k:k + ny, k:k + nx]

    dil = conv(img) > 0.5
    closed = ~(conv((~dil).astype(float)) > 0.5)
    inner = closed.copy()
    inner[1:-1, 1:-1] &= closed[:-2, 1:-1] & closed[2:, 1:-1] & closed[1:-1, :-2] & closed[1:-1, 2:]
    by, bx = np.nonzero(closed & ~inner)
    return (x0_ + bx * res) + 1j * (y0_ + by * res)


def ray_hit(sil: Silhouette, level: float, z0: complex, alpha, t_lo: float, t_hi: float = 260.0) -> np.ndarray:
    """Distance along the rays from z0 at angles ``alpha`` to the offset curve
    ``level`` of ``sil`` (bisection; z0 is inside)."""
    alpha = np.atleast_1d(np.asarray(alpha, float))
    lo = np.full(alpha.shape, t_lo)
    hi = np.full(alpha.shape, t_hi)
    e = np.exp(1j * alpha)
    for _ in range(40):
        m = 0.5 * (lo + hi)
        w = z0 + m * e - sil.zc
        outside = np.abs(w) > sil.radius(np.angle(w), level)
        hi = np.where(outside, m, hi)
        lo = np.where(outside, lo, m)
    return 0.5 * (lo + hi)


def seg_cross(pl: np.ndarray, a: complex, b: complex):
    """First crossing of segment a->b with polyline pl (complex array):
    (point, index of pl segment) or None."""
    P, Q = pl[:-1], pl[1:]
    d1 = b - a
    d2 = Q - P
    den = (d1.conjugate() * d2).imag
    ok = np.abs(den) > 1e-12
    w = P - a
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (w.conjugate() * d2).imag / den
        u = (w.conjugate() * d1).imag / den
    hit = ok & (t >= 0) & (t <= 1) & (u >= 0) & (u <= 1)
    if not hit.any():
        return None
    k = int(np.argmin(np.where(hit, t, np.inf)))
    return a + d1 * t[k], k


def walk_to(pl: np.ndarray, z: complex, direction, h: float = 0.25, maxn: int = 4000) -> List[complex]:
    """Walk from z along the unit field ``direction`` until crossing polyline pl."""
    pts = [z]
    for _ in range(maxn):
        k1 = direction(z)
        k2 = direction(z + 0.5 * h * k1)
        zn = z + h * k2
        c = seg_cross(pl, z, zn)
        if c is not None:
            pts.append(c[0])
            return pts
        z = zn
        pts.append(z)
    raise RuntimeError("walk did not reach its wrap")


# ---------------------------------------------------------------------------
# the plate geometry (shared with check_plate.py)
# ---------------------------------------------------------------------------


def build(
    bounds: Bounds,
    c_black: float = 1.15,
    c_red: float = 1.0,
    axis_u: float = 0.39,
    red_v: float = 0.175,
    black_v: float = 0.775,
    letter_h: float = 3.0,
    text_clear: float = 2.2,
    gap_saddle_mm: float = 7.0,
    start_gap_steps: float = 1.0,
    crown_centre: float = 39.0,
    birth_mm: float = 1.2,
    comet_mu: float = 0.45,
    comet_sep_mm: float = 1.0,
    lane_d0: float = 1.6,
    lane_sep: float = 1.1,
    lane_gauss: float = 7.0,
    waist_hold: float = 22.0,
    disk_margin: float = 2.0,
    soft: float = 2.0,
    spoke_sep: float = 1.05,
    spoke_eps: float = 0.05,
    fillet_mm: float = 2.5,
    spoke_fillet_mm: float = 1.8,
    wrap_clear: float = 1.6,
    handoff_hug_deg: float = 50.0,
    handoff_ramp_deg: float = 60.0,
    hull_close_mm: float = 22.0,
    hull_blur_mm: float = 6.0,
    entry_step: float = 1.6,
    wrap_step: float = 0.4,
) -> Dict[str, object]:
    x0, y0, x1, y1 = bounds
    W, Hh = x1 - x0, y1 - y0
    net = run_lstm()
    rows = net["rows"][1:]  # one row per letter (rows[0] is the start token)
    text = net["text"]
    T = len(text)
    # the letters the cell still HOLDS when the sentence ends (a write held
    # above 10 % in its most retentive cell): exactly the trailing run that
    # never fades. They wrap both eyes; the letter before them hands the line
    # out; every earlier letter coils the red eye.
    held = [t for t in range(T) if net["horizons"][t] is None]
    K_WRAP = held[0]  # first wrap letter (34: 'B')
    assert held == list(range(K_WRAP, T)), held
    K_HAND = K_WRAP - 1  # the hand-off (33: the space before BEST)
    wraps_ids = list(range(K_WRAP, T))

    cx = x0 + axis_u * W
    zb = complex(cx, y0 + black_v * Hh)
    zr = complex(cx, y0 + red_v * Hh)
    F = VortexPair(zb, zr, c_black, c_red)
    zs = F.saddle

    # ---- RED coil: half a turn per letter, clockwise from the west ---------
    # half-turn t runs from angle th_t to th_t - pi about the red eye; radius
    # grows by gap_t / 2 over it (so one full turn apart = the gap of that
    # stretch). Even t take the TOP half (W -> N -> E), odd t the BOTTOM half.
    gaps = [G0_MM + K_MM * r["f_mean"] for r in rows]
    halves = []  # per coil letter: (theta0, r0, dr)
    r, th = R0_MM, math.pi
    for t in range(K_HAND):
        halves.append((th, r, gaps[t] / 2.0))
        r += gaps[t] / 2.0
        th -= math.pi
    R_end = r  # the coil ends due EAST of the red eye (K_HAND is odd)

    def coil_pts(t: int, step: float = 0.3) -> List[complex]:
        th0, ra, dr = halves[t]
        n = max(8, int(math.pi * (ra + dr) / step))
        n += n % 2  # even, so the middle sample of a top half is due north
        return [zr + (ra + dr * j / n) * cmath.exp(1j * (th0 - math.pi * j / n)) for j in range(n + 1)]

    def coil_point(t: int, a: float) -> complex:
        th0, ra, dr = halves[t]
        while a > th0:
            a -= TWO_PI
        while a < th0 - math.pi:
            a += TWO_PI
        return zr + (ra + dr * (th0 - a) / math.pi) * cmath.exp(1j * a)

    # ---- the separatrix lobes (rays from each eye, bisected) ----------------
    def lobe(zc: complex, phi0: float, n: int = 1440) -> List[complex]:
        ring = []
        for k in range(n):
            phi = phi0 - TWO_PI * k / n
            e = cmath.exp(1j * phi)
            r_lo, rr = 0.5, 0.5
            while rr < 400.0 and F.rho(zc + rr * e) < F.rho_s - 1e-3:
                r_lo, rr = rr, rr + 0.5
            lo_, hi_ = r_lo, rr
            for _ in range(40):
                m = 0.5 * (lo_ + hi_)
                if F.rho(zc + m * e) < F.rho_s - 1e-3:
                    lo_ = m
                else:
                    hi_ = m
            ring.append(zc + lo_ * e)
        return ring

    sep_b = lobe(zb, cmath.phase(zs - zb))

    # ---- the rim of the black lobe, where the input is written -------------
    rim_pts = erode_ring([(q.real, q.imag) for q in sep_b], letter_h + text_clear, miter=False,
                         prune_folds=True)
    rim_pts = smooth_ring(rim_pts, passes=6)
    rim = [complex(px, py) for px, py in rim_pts]
    if signed_area(rim_pts) > 0:
        rim = rim[::-1]
    i0 = min(range(len(rim)), key=lambda i: abs(rim[i] - zs))
    rim = rim[i0:] + rim[:i0] + [rim[i0]]
    acc = [0.0]
    for a_, b_ in zip(rim, rim[1:]):
        acc.append(acc[-1] + abs(b_ - a_))
    L_rim = acc[-1]

    def rim_at(arc):
        j = max(1, min(len(acc) - 1, int(np.searchsorted(acc, arc))))
        a0, a1 = acc[j - 1], acc[j]
        uu = 0.0 if a1 <= a0 else (arc - a0) / (a1 - a0)
        z = rim[j - 1] + (rim[j] - rim[j - 1]) * uu
        tz = rim[min(len(rim) - 1, j + 2)] - rim[max(0, j - 3)]
        return z, math.atan2(tz.imag, tz.real)

    # the proverb runs clockwise once round the rim as a ring inscription:
    # the letters the cell still holds ("BEST MEMORY") crown the lobe, the
    # sentence begins after a one-step gap at the crown's right end, and the
    # saddle is skipped. Every letter is one step apart.
    U = L_rim - 2.0 * gap_saddle_mm
    step_arc = U / (T + start_gap_steps)
    i_top = max(range(len(rim) - 1), key=lambda i: rim[i].imag)
    u_top = acc[i_top] - gap_saddle_mm
    glyph_w = letter_h * 4.0 / 6.0
    behind = glyph_w / 2.0 + 1.2  # the thread lands 1.2 mm behind its glyph
    letters, births = [], []
    for t, ch in enumerate(text):
        u = (u_top + (t + T + start_gap_steps - crown_centre) * step_arc) % U
        s = gap_saddle_mm + u
        z, tan = rim_at(s)
        letters.append(dict(ch=ch, z=z, tan=tan, s=s))
        zb_, tanb = rim_at(s - behind)
        inward = complex(math.cos(tanb - math.pi / 2), math.sin(tanb - math.pi / 2))
        births.append(zb_ + birth_mm * inward)
    s_top = acc[i_top]

    # ---- the lane metric: first-order distance past the separatrix, soft-
    # merged with the coil disk so no lane runs inside the red ----------------
    R_disk = R_end + disk_margin

    def dist8(z: complex, e: float = 0.05) -> float:
        u0 = F.u(z)
        gu = complex(F.u(z + e) - F.u(z - e), F.u(z + 1j * e) - F.u(z - 1j * e)) / (2 * e)
        return u0 / max(1e-9, abs(gu)) ** (0.5 ** 0.5)

    def D(z: complex) -> float:
        a = dist8(z) / soft
        b = (abs(z - zr) - R_disk) / soft
        m = min(a, b)
        return soft * (m - math.log(math.exp(m - a) + math.exp(m - b)))

    def gradD(z: complex, e: float = 0.02) -> complex:
        return complex(D(z + e) - D(z - e), D(z + 1j * e) - D(z - 1j * e)) / (2 * e)

    zs0 = sigma_line(F, zr - 1.0, lambda q: D(q) >= lane_d0)[-1]
    base = level_trace(lambda q: D(q) - lane_d0, zs0, +1,
                       lambda q, st=[0]: (st.__setitem__(0, st[0] + 1) or st[0] > 60) and abs(q - zs0) < 0.45,
                       h=0.4, maxn=20000)
    sig = np.array([F.sig_ext(z) for z in base])
    j = int(np.where(np.abs(np.diff(sig)) > 1.0)[0][0]) + 1
    base = base[j:] + base[:j]
    sig = np.concatenate([sig[j:], sig[:j]])
    s_arc = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(np.array(base))))])
    base_np = np.array(base)
    SIG_R, S_R = sig[::-1].copy(), s_arc[::-1].copy()

    def s_of(sg: float) -> float:
        return float(np.interp(sg, SIG_R, S_R))

    def base_at(s: float) -> complex:
        k = int(np.clip(np.searchsorted(s_arc, s), 1, len(base) - 1))
        a, b_ = s_arc[k - 1], s_arc[k]
        return base[k - 1] + (base[k] - base[k - 1]) * ((s - a) / (b_ - a) if b_ > a else 0.0)

    sig_Lw = F.cb * 1.5 * math.pi + F.cr * 0.5 * math.pi  # the waist, left of the saddle
    sig_Rw = -F.cb * 0.5 * math.pi + F.cr * 0.5 * math.pi  # ... and right
    s_Lw, s_Rw = s_of(sig_Lw), s_of(sig_Rw)

    # ---- thread kinds, sides, ranks ---------------------------------------
    # coil  : a coil letter; spoke out of its half-turn, lane, dive
    # lane  : the hand-off and the wrap letters on BOTTOM half-wraps; lands on
    #         its wrap near a half-wrap end, lane, dive (the outermost lanes)
    # dive  : wrap letters on TOP half-wraps, which pass right over the crown
    kind = {}
    for t in range(T):
        if t < K_HAND:
            kind[t] = "coil"
        elif t == K_HAND or (t - K_WRAP) % 2 == 1:
            kind[t] = "lane"
        else:
            kind[t] = "dive"
    side = ["L" if letters[t]["s"] < s_top else "R" for t in range(T)]
    side[K_HAND] = "L"  # the hand-off ends west of the red eye
    laned = [t for t in range(T) if kind[t] != "dive"]
    rank: Dict[int, int] = {}
    for sd in "LR":
        ids = [t for t in laned if side[t] == sd]
        key = (lambda t: letters[t]["s"]) if sd == "L" else (lambda t: L_rim - letters[t]["s"])
        for i, t in enumerate(sorted(ids, key=key)):
            rank[t] = i

    theta: Dict[int, float] = {}
    for sd in "LR":
        for par in (0, 1):
            ids = sorted([t for t in range(K_HAND) if side[t] == sd and t % 2 == par], key=lambda t: rank[t])
            a0, dirn = {("L", 0): (math.pi / 2, 1), ("L", 1): (math.pi, 1),
                        ("R", 0): (math.pi / 2, -1), ("R", 1): (0.0, -1)}[(sd, par)]
            placed: List[Tuple[float, float]] = []
            a = a0 + dirn * spoke_eps
            for t in ids:
                rt = halves[t][1] + halves[t][2] / 2
                while not all(abs(a - ap) * max(rt, rp) >= spoke_sep for ap, rp in placed):
                    a += dirn * 0.002
                placed.append((a, rt))
                theta[t] = a

    thr: Dict[int, dict] = {}
    for t in range(K_HAND):
        A = coil_point(t, theta[t])
        sp = sigma_line(F, A, lambda q: D(q) >= lane_d0)
        en = sigma_line(F, births[t], lambda q: D(q) >= lane_d0)
        thr[t] = dict(A=A, sp=sp, en=en, sA=s_of(F.sig_ext(sp[-1])), sB=s_of(F.sig_ext(en[-1])))
    for t in range(K_HAND, T):
        en = sigma_line(F, births[t], lambda q: D(q) >= lane_d0)
        thr[t] = dict(en=en, sB=s_of(F.sig_ext(en[-1])))

    # left wrap-lane entries: just BELOW due west of the red eye (the hand-off
    # ends due west; bottom half-wraps end there too). Inner lanes enter first.
    iw = int(np.argmin(np.where(base_np.real < zr.real,
                                np.abs(np.angle((base_np - zr) * cmath.exp(-1j * math.pi))), np.inf)))
    s_w = float(s_arc[iw])
    left_wrap = sorted([t for t in laned if kind[t] == "lane" and side[t] == "L"], key=lambda t: rank[t])
    for i, t in enumerate(left_wrap):
        thr[t]["sA"] = s_w - entry_step * (len(left_wrap) - i) - 1.0

    grid = np.arange(0.0, s_arc[-1] + 0.1, 0.2)
    sg_ = lane_gauss / 0.2
    kx = np.arange(-int(4 * sg_), int(4 * sg_) + 1)
    ker = np.exp(-0.5 * (kx / sg_) ** 2)
    ker /= ker.sum()

    def smooth(a):
        n = len(kx) // 2
        return np.convolve(np.pad(a, n, mode="edge"), ker, mode="same")[n:-n]

    def stack(sd: str, ids_ready: List[int]) -> Dict[int, np.ndarray]:
        s_w_ = s_Lw if sd == "L" else s_Rw
        ids = sorted([t for t in ids_ready if side[t] == sd], key=lambda t: rank[t])
        win = np.abs(grid - s_w_) <= waist_hold
        act = {}
        for t in ids:
            lo_, hi_ = sorted((thr[t]["sA"], thr[t]["sB"]))
            pad = 1.5 * lane_gauss
            a_ = (grid >= lo_ - pad) & (grid <= hi_ + pad)
            if a_[win].any():
                a_ = a_ | win
            act[t] = a_.astype(float)
        out = {}
        for i, t in enumerate(ids):
            cnt = np.zeros_like(grid)
            for tj in ids[:i]:
                cnt += act[tj]
            out[t] = lane_d0 + lane_sep * smooth(cnt)
        return out

    lanes: Dict[int, dict] = {}

    def trace_lane(t: int, dkt: np.ndarray) -> None:
        th_ = thr[t]

        def phi(q, dkt=dkt):
            return D(q) - float(np.interp(s_of(F.sig_ext(q)), grid, dkt))

        if kind[t] == "coil":
            sp = th_["sp"] + normal_line(gradD, th_["sp"][-1], lambda q: phi(q) >= 0)[1:]
        else:  # the slot at the entry: out from the base lane along the normal
            sp = normal_line(gradD, base_at(th_["sA"]), lambda q: phi(q) >= 0)
            sp = [sp[-1]]
        en = th_["en"] + sigma_line(F, th_["en"][-1], lambda q: phi(q) >= 0)[1:]
        Q = en[-1]
        sense = +1 if side[t] == "L" else -1
        lane = level_trace(phi, sp[-1], sense, lambda q, Q=Q: abs(q - Q) < 0.35, h=0.3)
        pl = sp + lane[1:] + [Q] + en[::-1][1:]
        cq = len(sp) + len(lane) - 1
        pl = fillet(pl, cq, fillet_mm)
        if kind[t] == "coil":
            ci = len(sp) - 1
            pl = fillet(pl, ci, min(spoke_fillet_mm, 0.35 * _plen(lane)))
        lanes[t] = dict(pl=pl, slot=sp[-1])

    # pass 1: every lane that does not depend on where the wraps start
    first = [t for t in laned if not (kind[t] == "lane" and side[t] == "R")]
    dkL = stack("L", first)
    dkR = stack("R", first)
    for t in first:
        trace_lane(t, dkL[t] if side[t] == "L" else dkR[t])

    # ---- BLACK: one comet per letter, newest first; root gauge never cut ----
    paths = {}
    for t in range(T):
        row = rows[t]
        sweep = TWO_PI * F.cb * row["h_rms"]
        z_birth = births[t]
        ct = Tracker(F, z_birth)
        rho0, sg0 = F.rho(z_birth), ct.sigma
        n = max(20, int(sweep / 0.01))
        full = [ct.goto(rho0 - comet_mu * sweep * s_ / n, sg0 - sweep * s_ / n) for s_ in range(n + 1)]
        root, rest = _cut_at(full, ROOT_MM * row["h_rms"])
        _gap, rest = _cut_at(rest, 1.0)
        paths[t] = (full, root, rest)
    occ = Occupancy(comet_sep_mm)
    for t in range(T):
        for q in paths[t][1]:
            occ.add(q.real, q.imag)
    comets: Dict[int, dict] = {}
    for t in reversed(range(T)):
        full, root, rest = paths[t]
        cut = len(rest)
        for i, q in enumerate(rest):
            if i > 0 and occ.crowded(q.real, q.imag):
                cut = i
                break
        kept = rest[:cut]
        for q in kept:
            occ.add(q.real, q.imag)
        comets[t] = dict(root=root, rest=kept if len(kept) >= 2 else [], full_len=_plen(full),
                         drawn_len=_plen(root) + 1.0 + (_plen(kept) if len(kept) >= 2 else 0.0),
                         root_len=_plen(root), sweep_turn=rows[t]["h_rms"])

    # ---- the silhouette the wraps are offsets of ---------------------------
    def glyph_ink():
        out = []
        for L_ in letters:
            if L_["ch"] != " ":
                for gl in glyph_on_curve(L_["ch"], L_["z"], L_["tan"], letter_h):
                    out.extend(complex(px, py) for px, py in gl)
        return out

    def ink_points():
        pts = [zr + (R_end + 0.3) * cmath.exp(1j * k * TWO_PI / 720) for k in range(720)]
        for t, ln in lanes.items():
            pts.extend(_resample(ln["pl"], 0.5))
        for t in range(T):
            pts.extend(thr[t]["en"])
            pts.extend(comets[t]["root"])
            pts.extend(comets[t]["rest"])
        pts.extend(glyph_ink())
        return pts

    def handoff_and_wraps(sil: Silhouette):
        """The hand-off (half a turn about the red eye, E -> S -> W, peeling off
        the coil onto the first offset level) and the wraps (half a turn about
        the saddle per letter, the level growing by gap/2 over each)."""
        g_h = gaps[K_HAND]
        n = 900
        al = -math.pi * np.arange(n + 1) / n
        r_c = R_end + (g_h / 2.0) * (-al / math.pi)
        r_t = ray_hit(sil, wrap_clear, zr, al, R_end)
        # it runs on as the coil's next ring (inside the right-hand lanes,
        # crossing only their spokes, at right angles), peels off under the
        # coil where no thread runs, and is on the first offset level before
        # the left-hand lanes begin
        u = np.clip((-al - math.radians(handoff_hug_deg)) / math.radians(handoff_ramp_deg), 0.0, 1.0)
        w = u * u * (3 - 2 * u)
        r_h = (1 - w) * r_c + w * np.maximum(r_t, r_c)
        hand = list(zr + r_h * np.exp(1j * al))
        Pw = hand[-1]
        psi_w = cmath.phase(Pw - zs)
        wr = {}
        lev = wrap_clear
        psi0 = psi_w
        for k in wraps_ids:
            rr = float(sil.radius(psi0, lev)[0])
            m = max(60, int(math.pi * rr / wrap_step))
            ps = psi0 - math.pi * np.arange(m + 1) / m
            lv = lev + (gaps[k] / 2.0) * np.arange(m + 1) / m
            wr[k] = dict(pts=list(sil.point(ps, lv)), psi0=psi0, lev0=lev, lev1=lev + gaps[k] / 2.0)
            lev += gaps[k] / 2.0
            psi0 -= math.pi
        return hand, psi_w, wr

    sil = Silhouette(zs, closed_hull(ink_points(), hull_close_mm), blur_mm=hull_blur_mm)
    _hand, psi_w, _wr = handoff_and_wraps(sil)

    # right wrap-lane entries: just after the bottom half-wraps START, i.e.
    # just clockwise of psi_w - pi about the saddle (on the lobe's right flank)
    psi_e = psi_w - math.pi
    ang_s = np.angle((base_np - zs) * cmath.exp(-1j * psi_e))
    cand = np.where((np.abs(ang_s) < math.radians(1.0)) & (base_np.real > zs.real))[0]
    ie = int(cand[np.argmax(np.abs(base_np[cand] - zs))])
    s_e = float(s_arc[ie])
    right_wrap = sorted([t for t in laned if kind[t] == "lane" and side[t] == "R"], key=lambda t: rank[t])
    for i, t in enumerate(right_wrap):
        thr[t]["sA"] = s_e + entry_step * (len(right_wrap) - i) + 1.0
    dkR = stack("R", first + right_wrap)
    for t in right_wrap:
        trace_lane(t, dkR[t])

    # pass 2: the silhouette of ALL the ink, then the red line's outer part
    sil = Silhouette(zs, closed_hull(ink_points(), hull_close_mm), blur_mm=hull_blur_mm)
    hand, psi_w2, wr = handoff_and_wraps(sil)

    # ---- connectors (lane letters) and dives (top half-wrap letters) --------
    def unit_grad(z):
        g = gradD(z)
        return g / abs(g)

    def unit_sigma(z):
        g = F.grad(z)
        return g / abs(g)

    threads: Dict[int, List[complex]] = {}
    for t in range(T):
        if kind[t] == "coil":
            threads[t] = _resample(lanes[t]["pl"], 0.4)
        elif kind[t] == "lane":
            target = np.array(hand if t == K_HAND else wr[t]["pts"])
            conn = walk_to(target, lanes[t]["slot"], unit_grad)
            pl = fillet(conn[::-1] + lanes[t]["pl"][1:], len(conn) - 1, fillet_mm)
            threads[t] = _resample(pl, 0.4)
        else:
            en = thr[t]["en"]
            dive = walk_to(np.array(wr[t]["pts"]), en[-1], unit_sigma)
            threads[t] = _resample(dive[::-1] + en[::-1][1:], 0.4)

    return dict(net=net, rows=rows, text=text, T=T, F=F, zb=zb, zr=zr, zs=zs, halves=halves, gaps=gaps,
                R_end=R_end, coil_pts=coil_pts, letters=letters, births=births, threads=threads,
                theta=theta, side=side, rank=rank, kind=kind, comets=comets, letter_h=letter_h,
                sep_b=sep_b, D=D, s_Lw=s_Lw, s_Rw=s_Rw, hand=hand, wraps=wr, psi_w=psi_w2, psi_w1=psi_w,
                K_HAND=K_HAND, K_WRAP=K_WRAP, sil=sil, wrap_clear=wrap_clear,
                handoff_level_from_deg=handoff_hug_deg + handoff_ramp_deg, handoff_hug_deg=handoff_hug_deg)


# ---------------------------------------------------------------------------
# type on a curve
# ---------------------------------------------------------------------------


def glyph_on_curve(ch: str, p: complex, tangent: float, h: float) -> List[List[Tuple[float, float]]]:
    strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
    sc = h / 6.0
    ca, sa = math.cos(tangent), math.sin(tangent)
    out = []
    for st in strokes:
        pts = []
        for gx, gy in st:
            lx, ly = (gx - 2.0) * sc, gy * sc
            pts.append((p.real + lx * ca - ly * sa, p.imag + lx * sa + ly * ca))
        out.append(pts)
    return out


# ---------------------------------------------------------------------------
# pen-job ordering: replicate the pipeline's per-colour nearest neighbour
# ---------------------------------------------------------------------------


def nn_order(strokes: List[List[complex]], start: complex = 0j) -> Tuple[List[int], float, float]:
    """postprocess.optimize_stroke_order: from (0,0), repeatedly take the stroke
    whose START is nearest. Returns (order, travel, max hop)."""
    S = np.array([s[0] for s in strokes])
    E = np.array([s[-1] for s in strokes])
    left = np.ones(len(strokes), bool)
    pos = start
    order, travel, worst = [], 0.0, 0.0
    for _ in range(len(strokes)):
        d = np.abs(S - pos)
        d[~left] = np.inf
        i = int(np.argmin(d))
        if order:  # the entry hop from the previous layer is not in-layer travel
            travel += float(d[i])
            worst = max(worst, float(d[i]))
        order.append(i)
        left[i] = False
        pos = E[i]
    return order, travel, worst


def orient_for_nn(groups: List[List[List[complex]]], rounds: int = 6, hop_cap: float = 45.0,
                  init: List[bool] = None) -> List[bool]:
    """Pick a direction per group (a comet = root + rest; a thread = its dashes)
    so the pipeline's greedy NN gives the least travel with the smallest worst
    hop. Deterministic local search."""
    flip = list(init) if init is not None else [False] * len(groups)

    def strokes_of(fl):
        out = []
        for g, f in zip(groups, fl):
            if f:
                out.extend([s[::-1] for s in g[::-1]])
            else:
                out.extend(g)
        return out

    def cost(fl):
        order, tr, worst = nn_order(strokes_of(fl))
        return tr + 25.0 * max(0.0, worst - hop_cap) + 0.5 * worst

    best = cost(flip)
    n = len(groups)
    moves = [(i,) for i in range(n)] + [(i, i + 1) for i in range(n - 1)] + [(i, i + 2) for i in range(n - 2)]
    for _ in range(rounds):
        improved = False
        for mv in moves:
            for i in mv:
                flip[i] = not flip[i]
            c = cost(flip)
            if c < best - 1e-9:
                best, improved = c, True
            else:
                for i in mv:
                    flip[i] = not flip[i]
        if not improved:
            break
    return flip


def best_orientation(groups, inits, hop_cap: float = 45.0) -> List[bool]:
    """orient_for_nn from several deterministic starts; keep the one with the
    smallest worst hop (then the least travel)."""
    best, key = None, None
    for init in inits:
        fl = orient_for_nn(groups, init=init, hop_cap=hop_cap)
        st = []
        for g, f in zip(groups, fl):
            st.extend([s[::-1] for s in g[::-1]] if f else g)
        _, tr, worst = nn_order(st)
        k = (max(0.0, worst - hop_cap), tr)
        if key is None or k < key:
            best, key = fl, k
    return best


def repair_islands(strokes: List[List[complex]], cap: float = 45.0, rounds: int = 40,
                   reach: float = 8.0) -> List[List[complex]]:
    """Greedy NN strands 'islands' (strokes it skipped) and pays for them with
    long hops at the end. Flip single strokes near each long hop's target
    (and near where the island was passed) until no hop exceeds ``cap`` or
    no flip helps. Deterministic."""
    st = [list(s) for s in strokes]

    def cost(order_tr_w):
        order, tr, _ = order_tr_w
        E = [st[i][-1] for i in order]
        S_ = [st[i][0] for i in order]
        over = sum(max(0.0, abs(S_[k + 1] - E[k]) - cap) for k in range(len(order) - 1))
        return 25.0 * over + tr

    cur = nn_order(st)
    best = cost(cur)
    starts = np.array([s[0] for s in st])
    for _ in range(rounds):
        order = cur[0]
        long_targets = [order[k + 1] for k in range(len(order) - 1)
                        if abs(st[order[k + 1]][0] - st[order[k]][-1]) > cap]
        if not long_targets:
            break
        improved = False
        for tgt in long_targets:
            c = st[tgt][0]
            near = np.where(np.abs(starts - c) < reach)[0].tolist()
            for i in [tgt] + [j for j in near if j != tgt]:
                st[i] = st[i][::-1]
                trial = nn_order(st)
                k = cost(trial)
                if k < best - 1e-9:
                    best, cur, improved = k, trial, True
                    starts[i] = st[i][0]
                    break
                st[i] = st[i][::-1]
            if improved:
                break
        if not improved:
            break
    return st


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def lstm_readout(rng: SeededRNG, bounds: Bounds, colors: int = 4, feed: int = 2200,
                 red_chunk_mm: float = 560.0, **kw) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    GREY, RED, INK, TYPE = (_pen(i, colors) for i in range(4))
    geo = build(bounds, **kw)
    F, zr, T, text, rows = geo["F"], geo["zr"], geo["T"], geo["text"], geo["rows"]
    out: List[GCodeCommand] = []

    def poly(pts, pen):
        out.extend(_poly([(z.real, z.imag) for z in pts], color=pen, f=feed))

    # ---- 0 GREY: the output gate threads, dashed at duty = mean o_t --------
    dash_groups = []
    for t in range(T):
        pl = geo["threads"][t]
        L = _plen(pl)
        duty = rows[t]["o_mean"]
        n = max(1, int(round((L - duty * DASH_MM) / DASH_MM)))
        P = L / (n + duty)  # an integer number of periods, inked at both ends
        dash_groups.append([_q2(_arc_slice(pl, k * P, k * P + duty * P)) for k in range(n + 1)])
    flip = [False] * len(dash_groups) if FAST else orient_for_nn(dash_groups)
    grey_strokes = []
    for g, f in zip(dash_groups, flip):
        grey_strokes.extend([s[::-1] for s in g[::-1]] if f else g)
    for d_ in (grey_strokes if FAST else repair_islands(grey_strokes)):
        poly(d_, GREY)
    geo["grey_flip"] = flip

    # ---- 1 RED: the cell state, ONE line: the coil, the hand-off, the wraps.
    # Cut into chunks at the NORTH point of an open (above-median gap) top
    # half, so the pipeline's nearest-neighbour streams it in chain order:
    # every seam start is farther from (0,0) than the eye is, and each chunk
    # starts exactly where the last one ended -------------------------------
    zs = geo["zs"]
    line: List[complex] = []
    north_at: Dict[int, int] = {}
    stretch_at: Dict[int, Tuple[int, int]] = {}
    for t in range(geo["K_HAND"]):
        pts = geo["coil_pts"](t)
        base_i = len(line) - 1 if line else 0
        if t % 2 == 0:  # top half: W -> N -> E; its middle sample is due north
            north_at[t] = base_i + (len(pts) - 1) // 2
        line.extend(pts[1:] if line else pts)
        stretch_at[t] = (base_i, len(line) - 1)
    base_i = len(line) - 1
    line.extend(geo["hand"][1:])
    stretch_at[geo["K_HAND"]] = (base_i, len(line) - 1)
    for k, wk in geo["wraps"].items():
        pts = wk["pts"]
        base_i = len(line) - 1
        if (k - geo["K_WRAP"]) % 2 == 0:  # a top half-wrap: over the crown
            ps = np.angle((np.array(pts) - zs) * cmath.exp(-0.5j * math.pi))
            north_at[k] = base_i + int(np.argmin(np.abs(ps)))
        line.extend(pts[1:])
        stretch_at[k] = (base_i, len(line) - 1)
    med = float(np.median(geo["gaps"]))
    seams, last = [], 0
    cum = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(np.array(line))))])
    for t in sorted(north_at):
        i = north_at[t]
        if geo["gaps"][t] >= med and cum[i] - cum[last] >= red_chunk_mm and cum[-1] - cum[i] > 150.0:
            seams.append(i)
            last = i
    chunks = []
    prev = 0
    for i in seams + [len(line) - 1]:
        chunks.append(line[prev : i + 1])
        prev = i
    for ch in chunks:
        poly(ch, RED)
    geo["red_chunks"] = chunks
    geo["red_line"] = line
    geo["stretch_at"] = stretch_at

    # ---- 2 BLACK: comets (root, break, rest), oriented for NN -------------
    # comets alternate in / out around the ring (tip_k is ~2 mm from tip_k+1:
    # a newer comet cuts its neighbour where they converge), so the greedy
    # NN walks birth -> tip -> tip -> birth -> birth ... round the rim
    groups, init = [], []
    for t in range(T):
        cm = geo["comets"][t]
        groups.append([_q2(cm["root"])] + ([_q2(cm["rest"])] if cm["rest"] else []))
        init.append(t % 2 == 1)
    inits = [init, [not v for v in init], [False] * len(groups), [True] * len(groups)]
    geo["comet_groups"], geo["comet_inits"] = groups, inits
    cflip = init if FAST else best_orientation(groups, inits, hop_cap=30.0)
    for g, f in zip(groups, cflip):
        for s_ in (([s[::-1] for s in g[::-1]]) if f else g):
            poly(s_, INK)
    geo["comet_flip"] = cflip

    # ---- 3 TYPE: the proverb on the rim, the spine title, the colophon -----
    tcmds: List[GCodeCommand] = []
    for L_ in geo["letters"]:
        if L_["ch"] == " ":
            continue
        for pl in glyph_on_curve(L_["ch"], L_["z"], L_["tan"], geo["letter_h"]):
            tcmds.extend(_poly(pl, color=TYPE, f=feed))

    red_np = np.array(line)
    fig_lo = float(red_np.imag.min())
    fig_hi = float(red_np.imag.max())
    title = "LONG SHORT-TERM MEMORY"
    n_ch = len(title)
    t_h = (fig_hi - fig_lo) / ((n_ch - 1) * 5.6 / 6.0 + 4.0 / 6.0)
    tcmds.extend(giant_type(title, x1 - 0.6, fig_lo, t_h, pen=TYPE, angle=90.0, f=feed))

    hz = [h for h in geo["net"]["horizons"] if h is not None]
    n_wrap = len(geo["wraps"])
    col_h, lead = 1.5, 2.9
    lines = [
        "AN 8-CELL LSTM,",
        "TRAINED ON TWELVE",
        "SAYINGS, READS THIS",
        "ONE ONCE.",
        "",
        "cₜ ONE RED LINE, HALF",
        "   A TURN A LETTER:",
        "   %d ROUND ITS OWN EYE" % (geo["K_HAND"] + 1),
        "   (THE %dTH LEAVES IT)," % (geo["K_HAND"] + 1),
        "   %d ROUND BOTH EYES." % n_wrap,
        "   RING GAP (MM) =",
        "   0.8+0.8·MEAN fₜ",
        "",
        "hₜ ONE STROKE A",
        "   LETTER, RMS(hₜ)",
        "   OF A TURN. NEWER",
        "   CUTS OLDER. ROOT",
        "   = 8 MM × RMS.",
        "",
        "oₜ ONE GREY THREAD",
        "   A LETTER, FROM ITS",
        "   HALF-TURN TO ITS",
        "   STROKE:",
        "   hₜ = oₜ·tanh(cₜ).",
        "   INKED = MEAN oₜ.",
        "",
        "A WRITE FADES BELOW",
        "10 %% WITHIN %d" % max(hz),
        "LETTERS. AT THE END",
        "THE CELL HOLDS ONLY",
        "THE %d THAT WRAP" % n_wrap,
        "BOTH: BEST MEMORY.",
    ]
    low = red_np[red_np.imag < geo["zs"].imag]
    col_x = float(low.real.max()) + 0.0
    ly = geo["zs"].imag
    for ln in lines:
        if ln:
            tcmds.extend(_stroke_text(ln, col_x, ly, col_h, color=TYPE, f=feed))
        ly -= lead
    geo["colophon"] = dict(x=col_x, y_top=geo["zs"].imag, width=max(_text_width(l_, col_h) for l_ in lines),
                           title_x=x1 - 0.6 - t_h, fig_lo=fig_lo, fig_hi=fig_hi)

    # the type layer is collected, then ordered like the others (ring ->
    # colophon -> spine with no stranded glyph strokes)
    tstrokes = [_q2(p) for p in _cmd_strokes(tcmds)]
    geo["tstrokes"] = tstrokes
    for pl in (tstrokes if FAST else repair_islands(tstrokes, cap=45.0)):
        out.extend(_poly([(z.real, z.imag) for z in pl], color=TYPE, f=feed))

    lstm_readout.geo = geo
    return out


# ---------------------------------------------------------------------------
# the checkable trace
# ---------------------------------------------------------------------------


def write_trace(path: Path = HERE / "trace.json", paper: str = "a4", orientation: str = "portrait") -> dict:
    """Every per-step quantity the plate draws, with written definitions."""
    from promptplot.config import PaperConfig

    bounds = PaperConfig.from_size(paper, orientation).get_drawable_area()
    lstm_readout(SeededRNG(7), bounds, colors=4)
    geo = lstm_readout.geo
    net = geo["net"]
    # what each write still holds at the END of the sentence, in its most
    # retentive cell (prod of the later forget gates)
    Fg = np.array([rw["f"] for rw in net["rows"]])  # (T+1, H), rows[0] = start token
    held_end = [float(np.prod(Fg[t + 2:], axis=0).max()) if t + 2 < len(Fg) else 1.0 for t in range(geo["T"])]
    line = np.array(geo["red_line"])
    cum = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(line)))])
    K_HAND, K_WRAP = geo["K_HAND"], geo["K_WRAP"]
    steps = []
    for t in range(geo["T"]):
        r = geo["rows"][t]
        cm = geo["comets"][t]
        th = geo["threads"][t]
        i0, i1 = geo["stretch_at"][t]
        if t < K_HAND:
            red = dict(kind="coil", centre="red_eye", sweep_rad=math.pi, theta0_rad=geo["halves"][t][0],
                       r0_mm=geo["halves"][t][1], dr_mm=geo["halves"][t][2],
                       half="top" if t % 2 == 0 else "bottom")
        elif t == K_HAND:
            red = dict(kind="handoff", centre="red_eye", sweep_rad=math.pi, theta0_rad=0.0,
                       r0_mm=geo["R_end"], note="E -> S -> W about the red eye; peels from the coil onto the "
                       "first offset level of the figure's hull (its radial growth is NOT gap-mapped)")
        else:
            wk = geo["wraps"][t]
            red = dict(kind="wrap", centre="saddle", sweep_rad=math.pi, psi0_rad=wk["psi0"],
                       level0_mm=wk["lev0"], level1_mm=wk["lev1"],
                       half="top (over the crown)" if (t - K_WRAP) % 2 == 0 else "bottom (under the coil)")
        red.update(arc_mm=[float(cum[i0]), float(cum[i1])])
        steps.append(dict(
            t=t + 1, ch=r["ch"],
            i=r["i"], f=r["f"], o=r["o"], g=r["g"], c=r["c"], h=r["h"],
            i_mean=r["i_mean"], f_mean=r["f_mean"], o_mean=r["o_mean"],
            carry=r["carry"], c_norm=r["c_norm"], h_rms=r["h_rms"], h_max=r["h_max"],
            gap_mm=geo["gaps"][t],
            red_stretch=red,
            thread_kind=geo["kind"][t],
            thread_start=[th[0].real, th[0].imag], thread_len_mm=_plen(th),
            thread_path=[[round(z.real, 2), round(z.imag, 2)] for z in _resample(th, 1.0)],
            thread_side=geo["side"][t], thread_rank=geo["rank"].get(t),
            birth=[geo["births"][t].real, geo["births"][t].imag],
            letter=[geo["letters"][t]["z"].real, geo["letters"][t]["z"].imag],
            comet_root_mm=cm["root_len"], comet_full_mm=cm["full_len"], comet_drawn_mm=cm["drawn_len"],
            comet_drawn_turn=cm["sweep_turn"] * cm["drawn_len"] / cm["full_len"],
            comet_uncut=bool(cm["drawn_len"] >= cm["full_len"] - 0.05),
            retention_horizon_steps=net["horizons"][t],
            held_at_end=held_end[t],
        ))
    hz = [h for h in net["horizons"] if h is not None]
    data = dict(
        sequence=net["text"], T=geo["T"], hidden=net["hidden"],
        model=dict(weights="lstm_weights.json", gate_order="i,f,o,g", input="[x_onehot; h_prev]",
                   start_token=".", target_loss_nats_per_char=net["loss"], target_next_char_accuracy=net["acc"]),
        definitions=dict(
            f_mean="mean over the 8 cells of the forget gate f_t",
            o_mean="mean over the 8 cells of the output gate o_t",
            carry="|f_t * c_{t-1}| / |c_{t-1}|: fraction of the cell-state norm the forget gate carries across letter t (reported, not drawn)",
            h_rms="sqrt(mean_j h_t[j]^2), h_t = o_t * tanh(c_t)",
            gap_mm="G0_mm + K_mm * f_mean. Coil letters: radial growth of the red coil per FULL turn during half-turn t (the half-turn grows by gap/2). Wrap letters: growth of the offset level per full wrap (the half-wrap raises it by gap/2). The hand-off letter's gap is computed but not drawn",
            red_stretch="letter t owns exactly pi radians of the one red line. Coil letters and the hand-off: about the red eye (clockwise; even t top half W->N->E, odd t bottom half E->S->W). Wrap letters: about the saddle, from psi0 clockwise by pi, on the figure's hull offset at a level rising level0 -> level1",
            wrap_rule="a letter wraps both eyes iff its write is still held at the end of the sentence: held_at_end >= 0.10. That is exactly 'BEST MEMORY' (t = 35..45)",
            held_at_end="max over the 8 cells of prod_{u>t} f_u[j]: the fraction of letter t's write still in the cell after the last letter",
            hull="the figure's outline: the morphological closing (disk %.0f mm) of all grey, black and type ink plus the coil disk, seen from the saddle (star-shaped); a level-d wrap is its exact outward offset by d" % 22.0,
            thread="grey polyline from a point ON letter t's red stretch to comet t's birth. kind coil: a sigma-line spoke out of its half-turn, a lane, a dive; kind lane: lands on its half-wrap (or the hand-off) near a half-wrap end, a lane, a dive; kind dive: straight in along the black sigma-line from its half-wrap over the crown. Dashes: integer number of periods of ~dash_mm, inked fraction = o_mean",
            comet="black: sweeps h_rms of a turn of the black vortex (sigma span 2*pi*c_b*h_rms) with inflow d(rho)/d(sigma) = -mu; newest first; an older comet is cut where it comes within 1 mm of a newer one",
            comet_root="the comet's first stroke, before its 1 mm break: length = root_mm * h_rms, never cut",
            retention_horizon_steps="steps after letter t until the most retentive cell keeps < 10 % of letter t's write (prod of f over the following steps); null = survives the sentence",
        ),
        mapping=dict(G0_mm=G0_MM, K_mm=K_MM, root_mm=ROOT_MM, dash_mm=DASH_MM, r0_mm=R0_MM,
                     wrap_clear_mm=geo["wrap_clear"] + geo["sil"].lift,
                     handoff_level_from_deg=geo["handoff_level_from_deg"], handoff_hug_deg=geo["handoff_hug_deg"]),
        horizon=dict(max=max(hz), median=float(median(hz)) if hz else None,
                     survivors=sum(h is None for h in net["horizons"]),
                     held_at_end=[net["text"][t] for t in range(geo["T"]) if held_end[t] >= 0.10]),
        geometry=dict(red_eye=[geo["zr"].real, geo["zr"].imag], black_eye=[geo["zb"].real, geo["zb"].imag],
                      saddle=[geo["zs"].real, geo["zs"].imag], c_black=geo["F"].cb, c_red=geo["F"].cr,
                      R_end_mm=geo["R_end"], K_hand=K_HAND + 1, first_wrap=K_WRAP + 1, psi_w_rad=geo["psi_w"],
                      red_len_mm=float(cum[-1])),
        steps=steps,
    )
    path.write_text(json.dumps(data, indent=1))
    return data


if __name__ == "__main__":
    d = write_trace()
    print("trace.json:", d["T"], "steps; horizon", d["horizon"])
