"""LSTM — MEMORY STRATA.  studio/lstm-spirals r04 (thesis: memory-strata, parent r01).

A real, trained 8-cell character LSTM (weights in ``lstm_weights.json``, trained by
``train_lstm.py`` beside this file) reads one proverb, once, at render time:

    THE PALEST INK IS BETTER THAN THE BEST MEMORY

and the plate draws what its two memories did while reading it.

ORDER: NESTED, on one field. Both families live on the level sets of ONE complex
potential -- a pair of point vortices on the vertical axis,

    F(z) = c_b log(z - z_b) + c_r log(z - z_r),     rho = Re F,  sigma = Im F,

whose closed orbits (rho = const) are Cassini-like ovals: small ones round either
eye, large ones round both, the two regimes split by the separatrix through the
saddle between the eyes.

  * RED  = the cell state c_t. ONE continuous line that grows outward from the red
    eye like a tree's rings. Every character turns it half a loop round the red
    eye (a fixed angle of the potential, ``pi * c_r``) while it climbs at a pitch
    of ``S * carry_t`` mm per loop, where ``carry_t = |f_t * c_{t-1}| / |c_{t-1}|``
    is the fraction of the cell the forget gate carried across that character
    (floored at the pen's 0.9 mm). Its last characters leave the red lobe and
    wrap the whole field: long memory holds the short.
  * BLACK = the hidden state h_t = o_t * tanh(c_t). One comet per character, born
    at that character on the rim of the black lobe, falling toward the black eye
    along the same field plus a sink (``d rho / d sigma = -mu``), sweeping
    ``RMS(h_t)`` of one full turn. tanh keeps every |h| below 1 -- so no comet can
    ever close its turn. Comets are laid newest first; an older comet dies where
    it first runs within 1 mm of a newer one (the newer hidden state overwrites
    it) -- the engine's Occupancy grid decides, and the comet is cut, not resumed.

No randomness: the sheet is fully determined by the trained weights and the
proverb, so every seed gives the same plate.

Contract: ``lstm_memory_strata(rng, bounds, colors=3) -> list[GCodeCommand]``.
Pens (layer order = index order): 0 crimson = the cell-state line · 1 black = the
hidden-state comets · 2 black fine = the input text and the colophon.
"""

from __future__ import annotations

import cmath
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.engine import Scene3D
from promptplot.generative.engine.kit import Bounds, _pen, _poly, _stroke_text, _text_width, giant_type
from promptplot.generative.engine.geometry import erode_ring, signed_area, smooth_ring
from promptplot.generative.generators import _GLYPHS

HERE = Path(__file__).resolve().parent
TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------------------
# the LSTM -- the real forward pass of the trained weights
# ---------------------------------------------------------------------------


def run_lstm(path: Path = HERE / "lstm_weights.json") -> Dict[str, object]:
    """Forward pass over ``"." + target`` (the start token, then the proverb).
    Returns per-step gates and states, plus the two scalars the plate draws."""
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
        carry = float(np.linalg.norm(f * c)) / nc if nc > 1e-9 else 0.0
        rows.append(
            dict(
                ch=ch,
                carry=carry,
                h_rms=float(np.sqrt(np.mean(h_new * h_new))),
                h_max=float(np.max(np.abs(h_new))),
                f_mean=float(np.mean(f)),
                c_norm=float(np.linalg.norm(c_new)),
            )
        )
        h, c = h_new, c_new
    return dict(text=d["target"], rows=rows, hidden=H,
                loss=d.get("target_loss_nats_per_char"), acc=d.get("target_next_char_accuracy"))


# ---------------------------------------------------------------------------
# the field -- exact complex potential of two point vortices, with continuation
# ---------------------------------------------------------------------------


class VortexPair:
    """F(z) = c_b log(z - z_b) + c_r log(z - z_r).  Level sets of rho = Re F are
    the closed orbits of the pure vortex pair; lines of constant rho + mu*sigma
    are the orbits of the same pair plus a sink (spiral inflow of pitch mu)."""

    def __init__(self, zb: complex, zr: complex, cb: float, cr: float):
        self.zb, self.zr, self.cb, self.cr = zb, zr, cb, cr
        self.saddle = (cb * zr + cr * zb) / (cb + cr)  # F'(z) = 0
        self.rho_s = self.rho(self.saddle)

    def rho(self, z: complex) -> float:
        return self.cb * math.log(abs(z - self.zb)) + self.cr * math.log(abs(z - self.zr))

    def dF(self, z: complex) -> complex:
        return self.cb / (z - self.zb) + self.cr / (z - self.zr)


class Tracker:
    """Walks a curve given in (rho, sigma) and returns z, keeping the two
    arguments UNWRAPPED so sigma = c_b*theta_b + c_r*theta_r stays continuous
    (the multi-valued log is followed branch by branch, never jumped)."""

    def __init__(self, field: VortexPair, z0: complex):
        self.f = field
        self.z = z0
        self.tb = cmath.phase(z0 - field.zb)
        self.tr = cmath.phase(z0 - field.zr)

    @property
    def sigma(self) -> float:
        return self.f.cb * self.tb + self.f.cr * self.tr

    def _move(self, zn: complex) -> None:
        """Accept a new point, advancing both unwrapped arguments."""
        for attr, zc in (("tb", self.f.zb), ("tr", self.f.zr)):
            d = cmath.phase(zn - zc) - cmath.phase(self.z - zc)
            d = (d + math.pi) % TWO_PI - math.pi
            setattr(self, attr, getattr(self, attr) + d)
        self.z = zn

    def goto(self, rho_t: float, sig_t: float, max_dz: float = 0.5) -> complex:
        """Newton continuation to the point with the given (rho, sigma), cut into
        sub-steps no longer than ``max_dz`` mm so no branch is ever skipped."""
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


def _plen(samples) -> float:
    return sum(math.hypot(samples[i][0] - samples[i - 1][0], samples[i][1] - samples[i - 1][1])
               for i in range(1, len(samples)))


def red_line(F: "VortexPair", rows, stratum_mm: float, floor_mm: float, phase: float,
             turn: float = 1.0, r_start: float = 4.0) -> List[List[complex]]:
    """The cell state as ONE line, growing outward from the red eye.

    Every character turns it through the same angle of the potential,
    ``turn * 2*pi*c_r`` (turn=0.5: half a loop round the red eye, or
    c_r/(2(c_b+c_r)) of a loop round both), while it climbs outward at
    PITCH = S * carry_t mm per loop, floored at the pen's
    resolution. The pitch is held at the loop's tightest point (max |F'| over
    the last full loop), so no two loops come closer than the pitch.
    Returns one polyline per character (the pen may lift between them; the
    joints coincide, so the line is continuous on paper)."""
    z_start = F.zr + r_start * cmath.exp(1j * phase)
    tr = Tracker(F, z_start)
    rho = F.rho(z_start)
    sig = tr.sigma
    turns: List[List[complex]] = []
    hist: List[Tuple[float, float]] = [(sig, F.cr / r_start)]  # (sigma, |F'|)
    span = TWO_PI * F.cr * turn
    for row in rows:
        pitch = max(floor_mm, stratum_mm * row["carry"])
        loop = TWO_PI * (F.cr if rho < F.rho_s else (F.cb + F.cr))
        g = max(v for sg_, v in hist if sg_ <= sig + loop + 1e-9)
        d_rho = pitch * g * span / loop
        # adaptive step: at most 0.4 mm of paper per sample, whatever |F'| is
        # (it vanishes at the saddle, where a fixed sigma step would facet)
        dw = abs(complex(d_rho, span))
        pts = [tr.z]
        u = 0.0
        while u < 1.0 - 1e-12:
            du = min(0.02 / (span / TWO_PI), 0.4 * abs(F.dF(tr.z)) / dw, 1.0 - u)
            u += max(du, 1e-5)
            u = min(u, 1.0)
            z = tr.goto(rho + d_rho * u, sig - span * u)
            pts.append(z)
            hist.append((sig - span * u, abs(F.dF(z))))
        rho += d_rho
        sig -= span
        hist = [(sg_, v) for sg_, v in hist if sg_ <= sig + TWO_PI * (F.cb + F.cr) + 1e-9]
        turns.append(pts)
    return turns


# ---------------------------------------------------------------------------
# type on a curve
# ---------------------------------------------------------------------------


def glyph_on_curve(ch: str, p: complex, tangent: float, h: float) -> List[List[Tuple[float, float]]]:
    """One glyph centred on ``p``, baseline along ``tangent`` (radians), glyph up
    = the tangent rotated +90deg.  Returns polylines."""
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
# the plate
# ---------------------------------------------------------------------------


def lstm_memory_strata(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 3,
    feed: int = 2200,
    c_black: float = 1.30,
    c_red: float = 1.00,
    stratum_mm: float = 1.8,
    floor_mm: float = 0.9,
    comet_mu: float = 0.45,
    letter_h: float = 3.2,
    gap_saddle_mm: float = 5.0,
    birth_mm: float = 1.2,
    newest_first: bool = True,
    turn_per_char: float = 0.5,
    col_gap: float = 9.0,
    text_clear: float = 2.2,
    red_stroke_mm: float = 280.0,
    comet_sep_mm: float = 1.0,
    start_phase: float = -math.pi / 2,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    W, Hh = x1 - x0, y1 - y0
    RED = _pen(0, colors)
    INK = _pen(1, colors)
    TYPE = _pen(2, colors)

    net = run_lstm()
    rows = net["rows"]
    text = net["text"]

    scene = Scene3D(rng, bounds, feed=feed, fit="none", tip=0.5)
    out = scene.out

    # ---- the field --------------------------------------------------------
    cx = x0 + 0.36 * W
    zb = complex(cx, y0 + 0.79 * Hh)  # black eye (hidden state)
    zr = complex(cx, y0 + 0.155 * Hh)  # red eye (cell state)
    F = VortexPair(zb, zr, c_black, c_red)

    # ---- RED: the cell state, one continuous line ---------------------------
    red_turns = red_line(F, rows, stratum_mm, floor_mm, start_phase, turn=turn_per_char)

    # emitted as strokes of <= red_stroke_mm: long enough that the pen-lift
    # joints do not stack into a seam, short enough that every stroke is a
    # clean batch boundary on Leo (the joints coincide: one line on paper)
    run: List[Tuple[float, float]] = []
    run_len = 0.0
    for pts in red_turns:
        seg = [(p.real, p.imag) for p in pts]
        if run:
            seg = seg[1:]
        for q in seg:
            if run:
                run_len += math.hypot(q[0] - run[-1][0], q[1] - run[-1][1])
            run.append(q)
            if run_len >= red_stroke_mm:
                scene.poly(run, pen=RED)
                run, run_len = [q], 0.0
    if len(run) >= 2:
        scene.poly(run, pen=RED)

    # ---- the separatrix: the orbit through the saddle, traced by rays ------
    def lobe(zc: complex, phi0: float, n: int = 1440) -> List[complex]:
        """The lobe of the separatrix round eye ``zc``: along each ray from the
        eye, the FIRST radius where rho reaches rho_s (march, then bisect).
        Clockwise, starting at the ray ``phi0`` (the one through the saddle)."""
        ring = []
        for k in range(n):
            phi = phi0 - TWO_PI * k / n
            e = cmath.exp(1j * phi)
            r_lo, r = 0.5, 0.5
            while r < 400.0 and F.rho(zc + r * e) < F.rho_s - 1e-3:
                r_lo, r = r, r + 0.5
            lo_, hi_ = r_lo, r
            for _ in range(40):
                m = 0.5 * (lo_ + hi_)
                if F.rho(zc + m * e) < F.rho_s - 1e-3:
                    lo_ = m
                else:
                    hi_ = m
            ring.append(zc + lo_ * e)
        return ring

    phi_down = cmath.phase(F.saddle - zb)
    sep_b = lobe(zb, phi_down)

    # ---- the rim of the black lobe, where the input is written -------------
    # the separatrix offset INWARD by the letter height + clearance (a true
    # physical offset, so the text follows the lobe right down to the saddle)
    rim_pts = erode_ring([(q.real, q.imag) for q in sep_b], letter_h + text_clear, miter=False,
                         prune_folds=True)
    rim_pts = smooth_ring(rim_pts, passes=6)
    rim = [complex(px, py) for px, py in rim_pts]
    # keep clockwise order starting nearest the saddle
    if signed_area(rim_pts) > 0:
        rim = rim[::-1]
    i0 = min(range(len(rim)), key=lambda i: abs(rim[i] - F.saddle))
    rim = rim[i0:] + rim[:i0] + [rim[i0]]
    acc = [0.0]
    for a_, b_ in zip(rim, rim[1:]):
        acc.append(acc[-1] + abs(b_ - a_))
    L = acc[-1]
    T = len(text)

    def rim_at(arc):
        j = max(1, min(len(acc) - 1, int(np.searchsorted(acc, arc))))
        a0, a1 = acc[j - 1], acc[j]
        u = 0.0 if a1 <= a0 else (arc - a0) / (a1 - a0)
        z = rim[j - 1] + (rim[j] - rim[j - 1]) * u
        tz = rim[min(len(rim) - 1, j + 2)] - rim[max(0, j - 3)]
        return z, math.atan2(tz.imag, tz.real)

    gap_mm = gap_saddle_mm
    step_arc = (L - 2.0 * gap_mm) / (T - 1)
    letters = []
    for t, ch in enumerate(text):
        z, tan = rim_at(gap_mm + t * step_arc)
        letters.append((ch, z, tan))

    # glyphs: clockwise travel => tangent points "forward"; glyph up = outward
    type_polys: List[List[Tuple[float, float]]] = []
    for ch, z, tan in letters:
        if ch == " ":
            continue
        type_polys += glyph_on_curve(ch, z, tan, letter_h)

    # ---- BLACK: one comet per character, newest first ----------------------
    occ = scene.occupancy(comet_sep_mm)
    comet_len = []
    for t in (reversed(range(T)) if newest_first else range(T)):
        ch, z_l, tan = letters[t]
        row = rows[t + 1]  # rows[0] is the start token
        sweep = TWO_PI * F.cb * row["h_rms"]
        inward = complex(math.cos(tan - math.pi / 2), math.sin(tan - math.pi / 2))
        z_birth = z_l + birth_mm * inward
        ct = Tracker(F, z_birth)
        rho0, sg0 = F.rho(z_birth), ct.sigma
        n = max(20, int(sweep / 0.01))
        samples = []
        for s_ in range(n + 1):
            dsg = sweep * s_ / n
            z = ct.goto(rho0 - comet_mu * dsg, sg0 - dsg)
            samples.append((z.real, z.imag, 0.0, INK))
        # a comet DIES where it first runs within the pen floor of a newer
        # one (the newer hidden state overwrites it) -- the engine's Occupancy
        # grid decides; the comet is cut there, never resumed
        cut = len(samples)
        for i, q in enumerate(samples):
            if i > 0 and occ.crowded(q[0], q[1]):
                cut = i
                break
        kept = samples[:cut]
        full = _plen(samples)
        drawn = _plen(kept)
        comet_len.append((text[t], row["h_rms"], full, drawn))
        if len(kept) >= 2:
            scene.lines([kept], mode="over")
            for q in kept:
                occ.add(q[0], q[1])

    # ---- the title: a spine on the right margin, read bottom-up ------------
    # set so its INKED length spans the figure exactly, red coil to red crown
    title = "LONG SHORT-TERM MEMORY"
    ys = [z.imag for turn_ in red_turns for z in turn_]
    fig_lo, fig_hi = min(ys), max(ys)
    n_ch = len(title)
    t_h = (fig_hi - fig_lo) / ((n_ch - 1) * 5.6 / 6.0 + 4.0 / 6.0)
    t_y0 = fig_lo
    out.extend(giant_type(title, x1 - 0.6, t_y0, t_h, pen=TYPE, angle=90.0, f=feed))

    # ---- colophon: in the waist void, centred on the saddle's height ---------
    col_h = 1.6
    lead = 3.3
    lines = [
        "AN 8-CELL LSTM,",
        "TRAINED ON TWELVE",
        "SAYINGS, READS",
        "THIS ONE ONCE.",
        "",
        "cₜ ONE LINE,",
        "   HALF A TURN",
        "   PER LETTER.",
        "hₜ ONE STROKE",
        "   PER LETTER,",
        "   NEVER A TURN.",
    ]
    col_x = x1 - t_h - 0.6 - col_gap - max(_text_width(ln, col_h) for ln in lines)
    ly = F.saddle.imag + 0.5 * lead * (len(lines) - 1)
    for ln in lines:
        if ln:
            out.extend(_stroke_text(ln, col_x, ly, col_h, color=TYPE, f=feed))
        ly -= lead

    # ---- type layer ---------------------------------------------------------
    for pl in type_polys:
        out.extend(_poly(pl, color=TYPE, f=feed))

    lstm_memory_strata.stats = dict(comets=comet_len, red_turns=red_turns, rows=rows)
    return scene.render()
