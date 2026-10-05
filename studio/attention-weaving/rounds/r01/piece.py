"""ATTENTION AS WEAVING — faithful recreation, r01.

Reproduction of ``studio/attention-weaving/ref/reference.png`` (1122x1402, ratio
0.800 -> custom paper ``--paper 24x30`` portrait) with the brief's explicit
licence to fix the reference's crowding.

THE ORDER (rubric dim. 6): **INTERLACING**, then **PLYING**.  Nothing here is a
picture of a loom and nothing is a plot.  Two claims, both exact:

1.  ``sign(S[i, j])`` where ``S = QK^T / sqrt(d)`` decides who floats at every
    Q-K crossing.  Positive similarity passes OVER.  That is the whole rule and
    it is the same rule ``bauhaus_loom`` uses (sign -> over/under), applied to
    the score matrix instead of a weight matrix.
2.  Below the waist the sheet is a **3-ply rope**: ply Q, ply K, ply V wind
    about a common spine with angle ``theta_P(s) = theta0_P + Omega(s)``, and
    the projected depth ``R(s)*sin(theta_P)`` decides over/under.  That is real
    3D, so every rope crossing is physically consistent.

STRAND BOOK-KEEPING.  36 filaments.  Each is ONE polyline from its entry tick
at a sheet margin to its exit tick at the right margin — it changes pen (it is
Q, then Z), it never starts or stops in the middle of the sheet.  12 Q + 12 K
enter top-left / top-right, pass the waist, and are joined below it by 12 V
entering mid-left; 36 leave bottom-right.  ``_strand_audit()`` asserts this.

THE WAIST.  The bead block IS the attention matrix ``A = softmax(S)`` drawn as
a Hinton grid, 12 rows (queries) x 12 columns (keys), bead AREA proportional to
the weight, so **every row sums to one** — that is what softmax normalises and
it is why the rows are visibly peaked (one or two heavy beads, a tail of light
ones).  Column j is strung on K-strand j: ``A[i, j]`` is how much query i
attends to key j, so it belongs on key j's filament.  The 24 Q/K filaments run
dead vertical through the 28.8 x 29.0 mm block at 1.25 mm pitch and BREAK
around every bead — the beads are the only thing on the sheet in front of
everything else.  140 of the 144 weights clear the 0.16 mm radius floor.

MEASURED (seed 7, 240x300 mm sheet).  2535 crossings: 1964 filament-filament,
each of which gives the loser exactly one break (800 of them Q-K, decided by
the score's sign), plus 543 scaffold breaks; 28 scaffold-over-scaffold
crossings are left alone because the scaffold is all dotted anyway.
36 filaments in at a margin, 36 out — ``_strand_audit`` asserts it, and the
``AUDIT`` dict carries the numbers out of a run.

DE-CROWDING (the licence).  Against the reference:
  1. the waist is 28.8 mm wide, not the reference's 13.6 mm.  24 filaments
     through a 13.6 mm throat is 0.57 mm pitch, under the pen floor; this
     throat is 1.25 mm.  It still reads narrow — 29 mm against a 170 mm weave.
  2. ``Q . K^T`` moves up from v=0.189 to v=0.140, into the lens the two
     bundles' upper edges actually leave clear.  In the reference it grazes
     both bundles.
  3. the ``Q`` label drops 4.5 mm off the bottom Q filament.
  4. the exit reed is 45.5 mm of 1.30 mm dents (ref: ~40 mm for ~28), and the
     filaments stop 2 mm short of it so it reads as a reed and not a fringe.
  5. the scaffold is cut out of every type box; in the reference the top
     compass circle runs straight through the title.

Pens (``colors=5``): 0 black · 1 crimson Q · 2 dodgerblue K · 3 goldenrod V ·
4 darkgreen Z=AV.  Cream paper.  Fine tips: the rope's crossing zones run a
10th-percentile clearance of 0.77 mm, sized for a 0.3 mm liner.

Entry point: ``attention_weaving``.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.geometry import Circle, Rect, Region, Union, clip
from promptplot.generative.engine.kit import fill_disc
from promptplot.generative.generators import _dot, _glyph_advance, _poly, _stroke_text
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

BLACK, RED, BLUE, OCHRE, GREEN = 0, 1, 2, 3, 4

F_DRAW = 2200
STEP = 0.80  # mm — polyline resample pitch (also the crossing-detector's floor)

# ---- strand counts.  Everything downstream is derived from these. ----------
N_Q = 12
N_K = 12
N_V = 12
N_OUT = N_Q + N_K + N_V  # 36 — must equal the exit tick count

# ---- the waist ------------------------------------------------------------
THROAT_PITCH = 1.25  # mm between adjacent filaments at the waist
N_SLOT = N_Q + N_K  # 24 filaments through the throat
BLOCK_CX = 120.0
BLOCK_CY = 156.0
BLOCK_HH = 14.5  # half-height of the bead block
BEAD_RMAX = 1.15
BEAD_CUT = 0.72  # mm of clear paper a bead opens in the filament under it

# ---- crossing occlusion ---------------------------------------------------
GAP_STRAND = 0.55  # mm, half-gap at a perpendicular crossing
GAP_SCAFFOLD = 1.55
GAP_MAX = 2.40

# filled in by every run so the round can be audited without re-deriving it
AUDIT: Dict[str, float] = {}
SIN_FLOOR = 0.34  # shallow crossings widen the gap, but only up to GAP_MAX:
# uncapped, a 10-degree crossing opened a 5 mm hole and the weave turned into
# a field of dashes.  1.9 mm is two pen widths of clear paper, which is all an
# over/under needs to read.


# ===========================================================================
# tiny helpers
# ===========================================================================
def _pen(idx: int, colors: int) -> Optional[int]:
    return None if colors <= 1 else idx % colors


def _catmull(ctrl: Sequence[Pt], per: int = 26) -> np.ndarray:
    """Uniform Catmull-Rom through every control point (ends duplicated).

    Returns ``((len(ctrl)-1)*per + 1, 2)``; control point ``m`` is exactly at
    sample ``m*per``, which is what lets a bundle be truncated ON a knot.
    """
    p = [ctrl[0]] + list(ctrl) + [ctrl[-1]]
    out: List[Pt] = []
    for i in range(len(p) - 3):
        p0, p1, p2, p3 = (np.array(p[i + k], dtype=float) for k in range(4))
        for k in range(per):
            t = k / per
            t2, t3 = t * t, t * t * t
            q = 0.5 * (
                (2 * p1)
                + (-p0 + p2) * t
                + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                + (-p0 + 3 * p1 - 3 * p2 + p3) * t3
            )
            out.append((float(q[0]), float(q[1])))
    out.append(tuple(map(float, ctrl[-1])))
    return np.asarray(out, dtype=float)


def _arclen(pts: np.ndarray) -> np.ndarray:
    d = np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1]))
    return np.concatenate([[0.0], np.cumsum(d)])


def _resample(pts: np.ndarray, step: float = STEP) -> np.ndarray:
    """Uniform arclength resample."""
    s = _arclen(pts)
    if s[-1] < 1e-6:
        return pts[:1]
    n = max(2, int(round(s[-1] / step)) + 1)
    t = np.linspace(0.0, s[-1], n)
    return np.stack([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])], axis=1)


def _tracked(
    text: str,
    x: float,
    y: float,
    h: float,
    track: float,
    pen: Optional[int],
    word: float = 0.0,
    f: int = F_DRAW,
) -> List[GCodeCommand]:
    """Letter-spaced type.  The stroke font has no tracking parameter, so the
    glyphs are placed one at a time — this is the only way to get the
    reference's wide-spaced caps without doubling the cap height.  ``word``
    adds extra width to the space, so word gaps stay bigger than letter gaps
    however wide the tracking gets."""
    out: List[GCodeCommand] = []
    cx = x
    for ch in text:
        if ch != " ":
            out += _stroke_text(ch, cx, y, h, color=pen, f=f, proportional=True)
        cx += _glyph_advance(ch) * h / 6.0 + track + (word if ch == " " else 0.0)
    return out


def _tracked_w(text: str, h: float, track: float, word: float = 0.0) -> float:
    return (
        sum(
            _glyph_advance(c) * h / 6.0 + track + (word if c == " " else 0.0) for c in text
        )
        - track
    )


def _dash(poly: Poly, on: float = 1.05, off: float = 1.65) -> List[Poly]:
    """Split a polyline into dashes by arclength (the scaffold's dotted look)."""
    if len(poly) < 2:
        return []
    pts = np.asarray(poly, dtype=float)
    s = _arclen(pts)
    total = float(s[-1])
    runs: List[Poly] = []
    pos = 0.0
    while pos < total:
        a, b = pos, min(total, pos + on)
        if b - a > 0.25:
            t = np.linspace(a, b, max(2, int((b - a) / 0.4) + 1))
            runs.append(
                list(zip(np.interp(t, s, pts[:, 0]).tolist(), np.interp(t, s, pts[:, 1]).tolist()))
            )
        pos = b + off
    return runs


# ===========================================================================
# ribbons — a bundle is a ribbon of filaments, not N independent curves
# ===========================================================================
# A station is (x, y, normal-angle-deg, half-width-mm, sag).  The ribbon's
# normal rotates from vertical at the margin (filaments stacked in a column of
# ticks) to horizontal at the funnel (filaments spread left-to-right), which is
# what turns a vertical reed into a horizontal throat WITHOUT any filament in a
# bundle crossing another one in that bundle.
#
# ``sag`` bends the reed into a parabola (``+sag*hw*lam^2`` in y).  Without it
# the funnel mouth is a dead-straight horizontal bar and the bundle collapses
# onto one scanline — v1's worst flaw, a flat-bottomed mushroom.  With it the
# mouth is an arc and the filaments arrive at the throat from every height.
Station = Tuple[float, float, float, float, float]


def _ribbon(stations: Sequence[Station], per: int = 26):
    pos = _catmull([(s[0], s[1]) for s in stations], per)
    n = len(pos)
    ang = np.empty(n)
    hw = np.empty(n)
    sag = np.empty(n)
    for i in range(len(stations) - 1):
        a0, a1 = stations[i][2], stations[i + 1][2]
        w0, w1 = stations[i][3], stations[i + 1][3]
        g0, g1 = stations[i][4], stations[i + 1][4]
        for k in range(per + (1 if i == len(stations) - 2 else 0)):
            t = k / per
            e = t * t * (3 - 2 * t)  # smoothstep so the ribbon does not kink
            ang[i * per + k] = a0 + (a1 - a0) * e
            hw[i * per + k] = w0 + (w1 - w0) * e
            sag[i * per + k] = g0 + (g1 - g0) * e
    u = np.linspace(0.0, 1.0, n)
    return pos, np.radians(ang), hw, sag, u


def _ribbon_strand(rib, lam: float, wob_amp: float, wob_f: float, wob_ph: float):
    """One filament on a ribbon, riding a shared travelling wave.

    ``wob`` is a coherent wave (one frequency, a fixed phase step between
    neighbours) windowed to zero at both ends, so the bundle undulates without
    any two filaments in it swapping places: adjacent-filament clearance stays
    >= 1.4 mm everywhere.  Depth is the wave's quadrature — the bundle is a
    shallow helix, which is what gives V something to be in front of / behind.
    """
    pos, ang, hw, sag, u = rib
    win = np.sin(np.pi * u) ** 0.7
    th = 2 * math.pi * (wob_f * u) + wob_ph
    off = lam + wob_amp * win * np.sin(th)
    x = pos[:, 0] + off * hw * np.cos(ang)
    y = pos[:, 1] + off * hw * np.sin(ang) + sag * hw * off * off
    dep = 2.6 * win * np.cos(th)
    return np.stack([x, y], axis=1), dep


# ===========================================================================
# the rope — 3 plies winding a common spine
# ===========================================================================
class Rope:
    """theta_P(s) = theta0_P + Omega(s); lateral = R cos theta + lam*w,
    depth = R sin theta.  A ply is a flat band of filaments that slides
    sinusoidally across the rope; the bands cross each other, never
    themselves, and the band that is in front (sin theta > 0) wins."""

    SPINE: Sequence[Pt] = (
        (120.0, 141.5),
        (120.8, 129.0),
        (118.8, 114.0),
        (116.0, 98.0),
        (115.2, 85.0),
        (119.2, 72.0),
        (131.0, 62.0),
        (152.0, 55.8),
        (170.0, 55.4),
        (187.0, 51.6),
        (203.0, 54.2),
        (216.0, 52.4),
    )
    # Omega is pinned to 720 deg at S_FAN, and that is not decoration: three
    # plies at 0/90/180 project to lat = -R, 0, +R exactly there, which is the
    # ONE phase where all three bands are disjoint.  Hand the exit fan over at
    # any other phase and two plies are superimposed as the blend freezes, so
    # their filaments sit on top of each other going the same way.
    S_OM = (0.00, 0.10, 0.28, 0.46, 0.60, 0.74, 0.88, 1.00)
    D_OM = (14.0, 80.0, 205.0, 340.0, 470.0, 600.0, 720.0, 720.0)
    S_R = (0.00, 0.06, 0.14, 0.30, 0.44, 0.56, 0.68, 0.80, 0.90, 1.00)
    D_R = (7.0, 8.2, 12.5, 16.0, 17.5, 15.5, 16.8, 17.5, 18.0, 18.2)
    D_W = (10.6, 9.2, 5.8, 5.5, 5.5, 5.3, 5.5, 5.9, 6.4, 6.9)

    THETA0 = {"Q": 180.0, "K": 0.0, "V": 90.0}
    S_SEP = 0.12  # flat throat line -> plies
    S_FAN = 0.88  # plies -> flat exit fan
    FAN_PITCH = 1.30

    def __init__(self, n: int = 620):
        dense = _catmull(self.SPINE, 40)
        self.C = _resample(dense, _arclen(dense)[-1] / (n - 1))[:n]
        n = len(self.C)
        self.s = np.linspace(0.0, 1.0, n)
        d = np.gradient(self.C, axis=0)
        L = np.hypot(d[:, 0], d[:, 1])
        L[L < 1e-9] = 1.0
        self.dl = float(np.median(L))  # mm of spine per sample
        T = d / L[:, None]
        self.N = np.stack([-T[:, 1], T[:, 0]], axis=1)  # T=(0,-1) -> N=(1,0)
        self.Om = np.radians(np.interp(self.s, self.S_OM, self.D_OM))
        self.R = np.interp(self.s, self.S_R, self.D_R)
        self.W = np.interp(self.s, self.S_R, self.D_W)
        self._fan_rank: Dict[Tuple[str, int], int] = {}

    # -- raw ply placement, before the two end blends -----------------------
    def _raw(self, ply: str, lam: float):
        """A ply is a flat band of filaments whose centre slides across the
        rope at lateral speed ``v = |d lat / dl|``.  A band of fixed SAME-s
        width therefore has its own filaments crowd together by exactly
        ``1/sqrt(1+v^2)`` when it sweeps — the filaments run oblique to the
        cross-section, so their PERPENDICULAR pitch is not the pitch you set.
        That, not the ply crossings, is what put 20% of the rope under 0.8 mm
        in v7.  Widening the band by ``sqrt(1+v^2)`` cancels it exactly and is
        also what a physical ply does: constant apparent thickness."""
        th = np.radians(self.THETA0[ply]) + self.Om
        c = self.R * np.cos(th)
        v = np.abs(np.gradient(c) / self.dl)
        # capped at 1.6: measured v peaks near 1.2 here, so 1.6 covers the
        # whole compensation, while a looser cap fattens the bands until the
        # three plies overlap permanently and the braid reads as one ribbon.
        k = np.clip(np.sqrt(1.0 + v * v), 1.0, 1.60)
        return c + lam * self.W * k, self.R * np.sin(th)

    def set_fan_order(self, members: Sequence[Tuple[str, int, float]]) -> None:
        """Rank the 36 filaments by their lateral position at S_FAN and hand
        them the exit fan in that order — the fan therefore introduces ZERO
        crossings, and the reed at the right margin is a clean comb."""
        k = int(np.argmin(np.abs(self.s - self.S_FAN)))
        vals = [(self._raw(p, lam)[0][k], (p, i)) for p, i, lam in members]
        for r, (_, key) in enumerate(sorted(vals)):
            self._fan_rank[key] = r

    def path(self, ply: str, idx: int, lam: float, slot: Optional[int], s0: float = 0.0):
        """Filament positions + depth over s in [s0, 1]."""
        lat, dep = self._raw(ply, lam)
        if slot is not None:  # Q/K leave the waist as a flat line of slots
            flat = (slot - (N_SLOT - 1) / 2.0) * THROAT_PITCH
            t = np.clip(self.s / self.S_SEP, 0.0, 1.0)
            b = t * t * (3 - 2 * t)
            lat = flat * (1 - b) + lat * b
        # The exit fan FREEZES the plying at S_FAN before blending to the comb.
        # If the plies keep turning under the blend their order keeps swapping,
        # and the fan — which is ordered by lat AT S_FAN — then has to undo
        # those swaps: v2's reed was a thicket of shallow grazing crossings
        # instead of a clean comb.  Frozen, the blend is monotone, so the fan
        # introduces exactly zero crossings.
        kf = int(np.argmin(np.abs(self.s - self.S_FAN)))
        q = np.clip((self.s - (self.S_FAN - 0.05)) / 0.05, 0.0, 1.0)
        q = q * q * (3 - 2 * q)  # smooth, or the freeze itself is a kink
        lat = lat * (1 - q) + lat[kf] * q
        dep = dep * (1 - q) + dep[kf] * q
        rank = self._fan_rank[(ply, idx)]
        fan = (rank - (N_OUT - 1) / 2.0) * self.FAN_PITCH
        t = np.clip((self.s - self.S_FAN) / (1.0 - self.S_FAN), 0.0, 1.0)
        b = t * t * (3 - 2 * t)
        lat = lat * (1 - b) + fan * b
        dep = dep * (1 - b)
        P = self.C + lat[:, None] * self.N
        m = self.s >= s0 - 1e-9
        return P[m], dep[m]

    def at(self, ply: str, lam: float, s: float) -> Pt:
        k = int(np.argmin(np.abs(self.s - s)))
        lat, _ = self._raw(ply, lam)
        p = self.C[k] + lat[k] * self.N[k]
        return (float(p[0]), float(p[1]))

    def s_nearest(self, pt: Pt) -> float:
        d = np.hypot(self.C[:, 0] - pt[0], self.C[:, 1] - pt[1])
        return float(self.s[int(np.argmin(d))])


# ===========================================================================
# strands
# ===========================================================================
class Strand:
    __slots__ = ("pts", "pen", "dep", "weave", "fam", "idx", "arc", "cuts", "kind")

    def __init__(self, pts, pen, dep, weave, fam, idx, kind="strand"):
        self.pts = np.asarray(pts, dtype=float)
        self.pen = np.asarray(pen, dtype=int)
        self.dep = np.asarray(dep, dtype=float)
        self.weave = np.asarray(weave, dtype=bool)
        self.fam = fam
        self.idx = idx
        self.kind = kind
        self.arc = _arclen(self.pts)
        self.cuts: List[Tuple[float, float]] = []


def _join(parts: Sequence[Tuple[np.ndarray, np.ndarray, int, bool]]):
    """Concatenate (points, depth, pen, weave-flag) segments, dropping the
    duplicated junction point so the filament stays ONE polyline."""
    P, D, PE, WV = [], [], [], []
    for k, (pts, dep, pen, wv) in enumerate(parts):
        pts = np.asarray(pts, dtype=float)
        dep = np.asarray(dep, dtype=float)
        if k:
            pts, dep = pts[1:], dep[1:]
        P.append(pts)
        D.append(dep)
        PE.append(np.full(len(pts), pen, dtype=int))
        WV.append(np.full(len(pts), wv, dtype=bool))
    return (
        np.concatenate(P),
        np.concatenate(D),
        np.concatenate(PE),
        np.concatenate(WV),
    )


def _reseam(pts, dep, pen, wv, step: float = STEP):
    """Uniform resample of a filament, carrying its per-point channels."""
    s = _arclen(pts)
    n = max(2, int(round(s[-1] / step)) + 1)
    t = np.linspace(0.0, s[-1], n)
    P = np.stack([np.interp(t, s, pts[:, 0]), np.interp(t, s, pts[:, 1])], axis=1)
    D = np.interp(t, s, dep)
    PE = np.rint(np.interp(t, s, pen.astype(float))).astype(int)
    WV = np.interp(t, s, wv.astype(float)) > 0.5
    return P, D, PE, WV


# ===========================================================================
# crossing resolution — the piece's central problem
# ===========================================================================
def _resolve(strands: Sequence[Strand], S: np.ndarray) -> int:
    """Find every crossing between filaments and give the LOSER an arclength
    gap.  Buckets are one cell wide, each segment lives in the bucket of its
    midpoint, and only 5 of the 9 neighbour offsets are visited, so every pair
    is tested exactly once.

    The winner:
      * anything beats scaffold (the drafting geometry passes behind);
      * a Q-K crossing inside the weave is decided by ``sign(S[i, j])``;
      * everything else by projected depth.
    """
    P0, P1, SID, PIX = [], [], [], []
    for si, st in enumerate(strands):
        if len(st.pts) < 2:
            continue
        P0.append(st.pts[:-1])
        P1.append(st.pts[1:])
        SID.append(np.full(len(st.pts) - 1, si))
        PIX.append(np.arange(len(st.pts) - 1))
    P0 = np.concatenate(P0)
    P1 = np.concatenate(P1)
    SID = np.concatenate(SID)
    PIX = np.concatenate(PIX)

    cell = 2.6
    mid = (P0 + P1) * 0.5
    key = np.floor(mid / cell).astype(np.int64)
    buckets: Dict[Tuple[int, int], List[int]] = defaultdict(list)
    for i in range(len(mid)):
        buckets[(int(key[i, 0]), int(key[i, 1]))].append(i)
    for k in buckets:
        buckets[k] = np.asarray(buckets[k], dtype=np.int64)

    NEIGH = ((0, 0), (1, 0), (0, 1), (1, 1), (-1, 1))
    hits: List[Tuple[int, int, float, float, float]] = []
    for (kx, ky), idx in buckets.items():
        for dx, dy in NEIGH:
            other = buckets.get((kx + dx, ky + dy))
            if other is None:
                continue
            if dx == 0 and dy == 0:
                if len(idx) < 2:
                    continue
                a, b = np.triu_indices(len(idx), 1)
                A, B = idx[a], idx[b]
            else:
                A = np.repeat(idx, len(other))
                B = np.tile(other, len(idx))
            m = SID[A] != SID[B]
            if not m.any():
                continue
            A, B = A[m], B[m]
            r = P1[A] - P0[A]
            sv = P1[B] - P0[B]
            den = r[:, 0] * sv[:, 1] - r[:, 1] * sv[:, 0]
            ok = np.abs(den) > 1e-12
            if not ok.any():
                continue
            A, B, r, sv, den = A[ok], B[ok], r[ok], sv[ok], den[ok]
            qp = P0[B] - P0[A]
            t = (qp[:, 0] * sv[:, 1] - qp[:, 1] * sv[:, 0]) / den
            u = (qp[:, 0] * r[:, 1] - qp[:, 1] * r[:, 0]) / den
            g = (t >= 0) & (t <= 1) & (u >= 0) & (u <= 1)
            if not g.any():
                continue
            A, B, t, u, r, sv = A[g], B[g], t[g], u[g], r[g], sv[g]
            lr = np.hypot(r[:, 0], r[:, 1])
            ls = np.hypot(sv[:, 0], sv[:, 1])
            sin = np.abs(r[:, 0] * sv[:, 1] - r[:, 1] * sv[:, 0]) / np.maximum(lr * ls, 1e-9)
            for a_, b_, t_, u_, sn in zip(A, B, t, u, sin):
                hits.append((int(a_), int(b_), float(t_), float(u_), float(sn)))

    for a, b, t, u, sn in hits:
        sa, sb = strands[SID[a]], strands[SID[b]]
        ia, ib = PIX[a], PIX[b]
        la = sa.arc[ia] + t * (sa.arc[ia + 1] - sa.arc[ia])
        lb = sb.arc[ib] + u * (sb.arc[ib + 1] - sb.arc[ib])

        scaf_a, scaf_b = sa.kind == "scaffold", sb.kind == "scaffold"
        if scaf_a != scaf_b:
            loser, lo, base = (sa, la, GAP_SCAFFOLD) if scaf_a else (sb, lb, GAP_SCAFFOLD)
            loser.cuts.append((lo, min(GAP_MAX + 1.2, base / max(sn, SIN_FLOOR))))
            continue
        if scaf_a and scaf_b:
            continue  # scaffold over scaffold: leave it, it is all dotted

        a_over: bool
        if {sa.fam, sb.fam} == {"Q", "K"} and sa.weave[ia] and sb.weave[ib]:
            q, k = (sa, sb) if sa.fam == "Q" else (sb, sa)
            q_over = S[q.idx, k.idx] > 0.0
            a_over = q_over if sa.fam == "Q" else (not q_over)
        else:
            da = sa.dep[ia] + t * (sa.dep[ia + 1] - sa.dep[ia])
            db = sb.dep[ib] + u * (sb.dep[ib + 1] - sb.dep[ib])
            if abs(da - db) < 1e-6:
                a_over = sa.idx < sb.idx
            else:
                a_over = da > db
        g = min(GAP_MAX, GAP_STRAND / max(sn, SIN_FLOOR))
        AUDIT["x_" + "".join(sorted((sa.fam, sb.fam)))] = (
            AUDIT.get("x_" + "".join(sorted((sa.fam, sb.fam))), 0) + 1
        )
        if a_over:
            sb.cuts.append((lb, g))
        else:
            sa.cuts.append((la, g))
    return len(hits)


def _runs(st: Strand) -> List[Tuple[Poly, int]]:
    """Apply the accumulated gaps, then split by pen.  Returns drawable runs."""
    total = float(st.arc[-1])
    keep: List[Tuple[float, float]] = []
    if st.cuts:
        ivs = sorted((max(0.0, c - g), min(total, c + g)) for c, g in st.cuts)
        merged: List[List[float]] = []
        for a, b in ivs:
            if merged and a <= merged[-1][1] + 1e-9:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        prev = 0.0
        for a, b in merged:
            if a - prev > 0.55:
                keep.append((prev, a))
            prev = b
        if total - prev > 0.55:
            keep.append((prev, total))
    else:
        keep = [(0.0, total)]

    out: List[Tuple[Poly, int]] = []
    for a, b in keep:
        i0 = int(np.searchsorted(st.arc, a, "left"))
        i1 = int(np.searchsorted(st.arc, b, "right"))
        idx = list(range(max(1, i0), min(len(st.arc) - 1, i1) + 1))
        pa = _interp_at(st, a)
        pb = _interp_at(st, b)
        pts = [pa] + [tuple(st.pts[i]) for i in idx if a < st.arc[i] < b] + [pb]
        pens = [st.pen[min(len(st.pen) - 1, i0)]] + [
            st.pen[i] for i in idx if a < st.arc[i] < b
        ] + [st.pen[min(len(st.pen) - 1, i1)]]
        cur: Poly = [pts[0]]
        cp = pens[0]
        for p, q in zip(pts[1:], pens[1:]):
            cur.append(p)
            if q != cp:
                if len(cur) >= 2:
                    out.append((list(cur), int(cp)))
                cur = [p]
                cp = q
        if len(cur) >= 2:
            out.append((cur, int(cp)))
    return out


def _interp_at(st: Strand, l: float) -> Pt:
    x = float(np.interp(l, st.arc, st.pts[:, 0]))
    y = float(np.interp(l, st.arc, st.pts[:, 1]))
    return (x, y)


# ===========================================================================
# the piece
# ===========================================================================
def attention_weaving(rng: SeededRNG, bounds: Bounds, colors: int = 5) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    PB, PR, PK, PV, PZ = (_pen(i, colors) for i in (BLACK, RED, BLUE, OCHRE, GREEN))
    out: List[GCodeCommand] = []

    # ---- composition frame: reference ratio 0.800, letterboxed in the sheet
    fw = (x1 - x0) - 8.0
    fh = min((y1 - y0) - 8.0, fw / 0.800)
    fw = min(fw, fh * 0.800)
    fx = x0 + ((x1 - x0) - fw) / 2.0
    ftop = y1 - ((y1 - y0) - fh) / 2.0

    def U(u: float) -> float:
        return fx + u * fw

    def Vv(v: float) -> float:
        return ftop - v * fh

    # =======================================================================
    # the numbers: Q, K, the scores, the attention matrix
    # =======================================================================
    d = 8
    Qm = np.array([[rng.gauss(0, 1) for _ in range(d)] for _ in range(N_Q)])
    Km = np.array([[rng.gauss(0, 1) for _ in range(d)] for _ in range(N_K)])
    S = (Qm @ Km.T) / math.sqrt(d)
    E = np.exp(S - S.max(axis=1, keepdims=True))
    A = E / E.sum(axis=1, keepdims=True)  # each ROW sums to 1 — that is softmax

    # =======================================================================
    # slots at the waist
    # =======================================================================
    def slot_x(k: int) -> float:
        return BLOCK_CX + (k - (N_SLOT - 1) / 2.0) * THROAT_PITCH

    q_slot = [2 * (N_Q - 1 - i) for i in range(N_Q)]  # Q_0 (highest) -> rightmost
    k_slot = [2 * (N_K - 1 - j) + 1 for j in range(N_K)]  # K_0 (highest) -> leftmost
    lam_q = [1.0 - 2.0 * i / (N_Q - 1) for i in range(N_Q)]
    lam_k = [1.0 - 2.0 * j / (N_K - 1) for j in range(N_K)]
    lam_v = [1.0 - 2.0 * i / (N_V - 1) for i in range(N_V)]

    block_top, block_bot = BLOCK_CY + BLOCK_HH, BLOCK_CY - BLOCK_HH
    hw_throat = (slot_x(q_slot[0]) - slot_x(q_slot[-1])) / 2.0
    cx_q = (slot_x(q_slot[0]) + slot_x(q_slot[-1])) / 2.0
    cx_k = (slot_x(k_slot[0]) + slot_x(k_slot[-1])) / 2.0

    # =======================================================================
    # the two upper ribbons.  Normal rotates 90deg -> 0deg: a vertical reed at
    # the margin becomes a horizontal funnel mouth, and because Q_0 sits at
    # lam=+1 it ends up at the RIGHT of the mouth while K_0 (also lam=+1, but
    # the K ribbon's normal points the other way) ends up at the LEFT.  The
    # two bundles are therefore forced to pass completely through each other.
    # =======================================================================
    q_st: List[Station] = [
        (U(0.047), Vv(0.140), 90.0, 21.0, 0.00),
        (U(0.165), Vv(0.174), 78.0, 23.0, 0.03),
        (U(0.297), Vv(0.210), 62.0, 28.0, 0.06),
        (U(0.452), Vv(0.264), 32.0, 36.0, 0.12),
        (U(0.538), Vv(0.320), 14.0, 31.0, 0.20),
        (U(0.530), Vv(0.360), 5.0, 23.0, 0.11),
        (U(0.512), Vv(0.395), 1.0, 17.0, 0.03),
        (cx_q, block_top, 0.0, hw_throat, 0.0),
    ]
    k_st: List[Station] = [
        (2 * BLOCK_CX - s[0], s[1], 180.0 - s[2], s[3], s[4]) for s in q_st[:-1]
    ] + [(cx_k, block_top, 180.0, hw_throat, 0.0)]

    v_st: List[Station] = [
        (U(0.047), Vv(0.632), 90.0, 22.0, 0.00),
        (U(0.150), Vv(0.641), 88.0, 22.0, 0.02),
        (U(0.270), Vv(0.663), 82.0, 21.5, 0.05),
        (U(0.380), Vv(0.696), 66.0, 19.0, 0.12),
        (U(0.455), Vv(0.729), 44.0, 14.5, 0.18),
        (U(0.492), Vv(0.752), 26.0, 10.5, 0.14),
    ]

    rib_q, rib_k, rib_v = _ribbon(q_st), _ribbon(k_st), _ribbon(v_st)

    # coherent travelling wave: one frequency, fixed phase step between
    # neighbours, amplitude chosen so no two filaments in a bundle swap.
    WOB_A, WOB_F, WOB_D = 0.25, 1.35, 0.55

    rope = Rope()
    s_join = rope.s_nearest((U(0.500), Vv(0.747)))

    members = (
        [("Q", i, lam_q[i]) for i in range(N_Q)]
        + [("K", j, lam_k[j]) for j in range(N_K)]
        + [("V", i, lam_v[i]) for i in range(N_V)]
    )
    rope.set_fan_order(members)

    strands: List[Strand] = []

    # ---- Q and K ----------------------------------------------------------
    for fam, rib, lams, slots, pen0, pen_block in (
        ("Q", rib_q, lam_q, q_slot, PR, PR),
        ("K", rib_k, lam_k, k_slot, PK, PK),
    ):
        for i, lam in enumerate(lams):
            pre, dpre = _ribbon_strand(rib, lam, WOB_A, WOB_F, WOB_D * i)
            sx = slot_x(slots[i])
            nblk = max(2, int(round((block_top - block_bot) / STEP)) + 1)
            blk = np.stack(
                [np.full(nblk, sx), np.linspace(block_top, block_bot, nblk)], axis=1
            )
            rp, rdep = rope.path(fam, i, lam, slots[i])
            pts, dep, pen, wv = _join(
                [
                    (pre, dpre, pen0, True),
                    (blk, np.zeros(nblk), pen_block, False),
                    (rp, rdep, PZ, False),
                ]
            )
            pts, dep, pen, wv = _reseam(pts, dep, pen, wv)
            strands.append(Strand(pts, pen, dep, wv, fam, i))

    # ---- V: free ribbon, then bridged onto its ply --------------------------
    for i, lam in enumerate(lam_v):
        free, dfree = _ribbon_strand(rib_v, lam, WOB_A, WOB_F, WOB_D * (i + 0.5))
        anchor = rope.at("V", lam, s_join)
        ahead = rope.at("V", lam, min(1.0, s_join + 0.035))
        ctrl = [tuple(p) for p in free[:: max(1, len(free) // 9)]] + [tuple(free[-1])]
        ctrl = ctrl + [anchor, ahead]
        per = 26
        bridged = _catmull(ctrl, per)[: (len(ctrl) - 2) * per + 1]  # stop ON the anchor
        rp, rdep = rope.path("V", i, lam, None, s0=s_join)
        rp = np.vstack([np.asarray([anchor]), rp[1:]]) if len(rp) else np.asarray([anchor])
        dbr = np.interp(
            np.linspace(0, 1, len(bridged)), np.linspace(0, 1, len(dfree)), dfree
        )
        pts, dep, pen, wv = _join(
            [(bridged, dbr, PV, False), (rp, rdep, PZ, False)]
        )
        pts, dep, pen, wv = _reseam(pts, dep, pen, wv)
        strands.append(Strand(pts, pen, dep, wv, "V", i))

    _strand_audit(strands, bounds)

    # =======================================================================
    # type layout, computed HERE so the scaffold can be cut out of the type
    # boxes.  In v2 the top compass circle ran clean through the title and it
    # printed as "ATTENTION--AS--WEAVING".
    # =======================================================================
    title = "ATTENTION AS WEAVING"
    th, tword = 5.2, 3.4
    ttrack = (fw * 0.560 - _tracked_w(title, th, 0.0, tword)) / (len(title) - 1)
    tw = _tracked_w(title, th, ttrack, tword)

    lh, lab = 6.0, "Q · K"
    labw = _tracked_w(lab, lh, 1.0)
    sup_h = lh * 0.55
    lw = labw + 0.8 + _glyph_advance("T") * sup_h / 6.0
    lx, ly = U(0.5) - lw / 2.0, Vv(0.140)
    sup_x, sup_y = lx + labw + 0.8, ly + lh * 0.52

    sm_x, sm_y, sm_h = BLOCK_CX + 19.5, BLOCK_CY - 1.0, 2.8

    TYPE: List[Tuple[str, float, float, float, float, Optional[int], float]] = [
        (title, U(0.5) - tw / 2.0, Vv(0.054), th, ttrack, PB, tword),
        (lab, lx, ly, lh, 1.0, PB, 0.0),
        ("Q", U(0.062), Vv(0.268), 5.6, 0.0, PR, 0.0),
        ("K", U(0.905), Vv(0.318), 5.6, 0.0, PK, 0.0),
        ("V", U(0.126), Vv(0.523), 5.6, 0.0, PV, 0.0),
        ("Z = AV", U(0.762), Vv(0.752), 5.6, 1.0, PZ, 0.0),
        ("softmax", sm_x, sm_y, sm_h, 0.35, PB, 0.0),
    ]
    type_boxes: List[Region] = [
        Rect(bx - 2.2, by - bh * 0.40, bx + _tracked_w(bt, bh, btr, bw) + 2.2, by + bh + 2.2)
        for bt, bx, by, bh, btr, _bp, bw in TYPE
    ]
    type_boxes.append(Rect(sup_x - 1.0, sup_y - 0.6, sup_x + sup_h + 1.6, sup_y + sup_h + 1.6))
    TYPE_MASK = Union(*type_boxes)

    # =======================================================================
    # scaffold — compass circles + bead-strung rules, all dotted, all BEHIND
    # =======================================================================
    scaffold: List[Strand] = []

    def add_scaffold(poly: np.ndarray) -> None:
        poly = _resample(np.asarray(poly, dtype=float), STEP)
        for sub in clip([(float(p[0]), float(p[1])) for p in poly], TYPE_MASK, "outside"):
            arr = np.asarray(sub, dtype=float)
            m = (
                (arr[:, 0] > x0 + 1.0)
                & (arr[:, 0] < x1 - 1.0)
                & (arr[:, 1] > y0 + 1.0)
                & (arr[:, 1] < y1 - 1.0)
            )
            run: List[Pt] = []
            for p, ok in zip(arr, m):
                if ok:
                    run.append((float(p[0]), float(p[1])))
                else:
                    if len(run) >= 3:
                        scaffold.append(_scaf(run))
                    run = []
            if len(run) >= 3:
                scaffold.append(_scaf(run))

    def _scaf(run: Sequence[Pt]) -> Strand:
        n = len(run)
        return Strand(
            np.asarray(run, dtype=float),
            np.full(n, PB if PB is not None else 0),
            np.full(n, -1e6),
            np.zeros(n, dtype=bool),
            "SCAF",
            len(scaffold),
            kind="scaffold",
        )

    COMPASS = (
        (U(0.500), Vv(0.185), 37.0),
        (U(0.500), Vv(0.185), 23.5),
        (BLOCK_CX, BLOCK_CY, 25.0),
        (BLOCK_CX, BLOCK_CY, 46.0),
        (U(0.400), Vv(0.610), 33.0),
        (U(0.465), Vv(0.790), 28.0),
        (U(0.640), Vv(0.855), 34.0),
        (U(0.745), Vv(0.300), 18.5),
        (U(0.255), Vv(0.300), 18.5),
    )
    for ccx, ccy, cr in COMPASS:
        a = np.linspace(0, 2 * math.pi, max(64, int(cr * 5)))
        add_scaffold(np.stack([ccx + cr * np.cos(a), ccy + cr * np.sin(a)], axis=1))

    RULES = (
        (U(0.125), 0.055, 0.395),
        (U(0.218), 0.085, 0.330),
        (U(0.500), 0.095, 0.415),
        (U(0.561), 0.470, 0.760),
        (U(0.766), 0.520, 0.800),
        (U(0.913), 0.060, 0.330),
        (U(0.330), 0.560, 0.830),
        (U(0.908), 0.735, 0.988),
    )
    bead_rule: List[Tuple[float, float, float]] = []
    for rx, v_a, v_b in RULES:
        ya, yb = Vv(v_a), Vv(v_b)
        add_scaffold(np.stack([np.full(40, rx), np.linspace(ya, yb, 40)], axis=1))
        for _ in range(rng.randint(2, 5)):
            t = rng.random()
            bead_rule.append((rx, ya + (yb - ya) * t, 0.42 + rng.random() * 0.70))

    # the waist's horizontal dotted rule — broken for the `softmax` label, so
    # the label sits in clear paper instead of on top of the rule
    lab_x0 = sm_x
    lab_x1 = sm_x + _tracked_w("softmax", sm_h, 0.35)
    for a, b in ((U(0.300), lab_x0 - 1.8), (lab_x1 + 1.8, U(0.700))):
        add_scaffold(np.stack([np.linspace(a, b, 40), np.full(40, BLOCK_CY)], axis=1))

    # =======================================================================
    # marks that are IN FRONT: the beads and the solid registration dots.
    # Anything solid cuts the filaments under it (geometry.Circle, so the
    # filament stops exactly on the disc, not on a sample).
    # =======================================================================
    solid: List[Tuple[float, float, float, Optional[int], float]] = []  # +cut radius
    hollow: List[Tuple[float, float, float, Optional[int]]] = []

    # --- the attention matrix, strung on the K filaments -------------------
    # The beads open BEAD_CUT of clear paper in whatever runs under them.  At
    # 0.42 (v2) the waist read as a barcode with dots on it; at 0.72 the
    # verticals are reduced to short ties between beads and the bead grid is
    # what the eye gets, which is the point of the waist.
    amax = float(A.max())
    row_y = [BLOCK_CY + ((N_Q - 1) / 2.0 - r) * (2 * BLOCK_HH / N_Q) for r in range(N_Q)]
    for r in range(N_Q):
        for c in range(N_K):
            rad = BEAD_RMAX * math.sqrt(A[r, c] / amax)
            if rad < 0.16:
                continue
            solid.append((slot_x(k_slot[c]), row_y[r], rad, PB, BEAD_CUT))

    # --- registration marks riding the filaments ---------------------------
    # No two marks may touch.  Two 3 mm open circles landing 1 mm apart is not
    # an overlap anyone would defend, it is the rng running out of room.
    placed: List[Tuple[float, float, float]] = []

    def free(px: float, py: float, r: float) -> bool:
        return all(
            math.hypot(px - qx, py - qy) > r + qr + 1.6 for qx, qy, qr in placed
        )

    for _ in range(96):
        st = strands[rng.randint(0, len(strands) - 1)]
        k = rng.randint(6, len(st.pts) - 7)
        px, py = float(st.pts[k, 0]), float(st.pts[k, 1])
        if abs(px - BLOCK_CX) < 18 and abs(py - BLOCK_CY) < 19:
            continue
        pen = int(st.pen[k])
        if TYPE_MASK.contains(px, py):
            continue
        if rng.random() < 0.52:
            r = 1.4 + rng.random() * 2.8
            if not free(px, py, r):
                continue
            hollow.append((px, py, r, pen))
        else:
            r = 0.42 + rng.random() * 0.85
            if not free(px, py, r):
                continue
            solid.append((px, py, r, pen, 0.42))
        placed.append((px, py, r))
    for rx, ry, rr in bead_rule:
        if not TYPE_MASK.contains(rx, ry):
            solid.append((rx, ry, rr, PB, 0.42))
    for _ in range(16):
        fx_, fy_ = U(0.08 + rng.random() * 0.84), Vv(0.10 + rng.random() * 0.82)
        fr_ = 0.30 + rng.random() * 0.45
        if not TYPE_MASK.contains(fx_, fy_) and free(fx_, fy_, fr_):
            solid.append((fx_, fy_, fr_, PB, 0.42))
            placed.append((fx_, fy_, fr_))

    # =======================================================================
    # resolve every crossing, then emit
    # =======================================================================
    allpaths = strands + scaffold
    AUDIT.clear()
    n_cross = _resolve(allpaths, S)
    AUDIT["crossings_total"] = n_cross
    AUDIT["breaks_total"] = sum(len(p.cuts) for p in allpaths)
    AUDIT["filaments"] = len(strands)
    AUDIT["entered"] = sum(1 for t in strands if t.pts[0, 0] < x0 + 30 or t.pts[0, 0] > x1 - 30)
    AUDIT["exited"] = sum(1 for t in strands if t.pts[-1, 0] > x1 - 30)
    AUDIT["beads"] = sum(1 for c in solid if c[4] == BEAD_CUT)

    cut_regions = [Circle(cx, cy, r + cut) for cx, cy, r, _, cut in solid]

    def emit_runs(st: Strand, dashed: bool) -> None:
        for poly, pen in _runs(st):
            near = [
                c
                for c in cut_regions
                if _bbox_near(poly, c.cx, c.cy, c.r)
            ]
            pieces = clip(poly, Union(*near), keep="outside") if near else [poly]
            for pc in pieces:
                if dashed:
                    for dsh in _dash(pc):
                        out.extend(_poly(dsh, color=pen, f=F_DRAW))
                elif len(pc) >= 2:
                    out.extend(_poly(pc, color=pen, f=F_DRAW))

    for st in scaffold:
        emit_runs(st, dashed=True)
    for st in strands:
        emit_runs(st, dashed=False)

    # ---- the solid marks --------------------------------------------------
    for cx, cy, r, pen, _cut in solid:
        if r < 0.55:
            out.extend(_dot(cx, cy, max(0.22, r * 0.8), color=pen))
        else:
            out.extend(fill_disc(cx, cy, r, spacing=0.34, pen=pen, f=F_DRAW))
    for cx, cy, r, pen in hollow:
        a = np.linspace(0, 2 * math.pi, 48)
        out.extend(
            _poly(list(zip(cx + r * np.cos(a), cy + r * np.sin(a))), color=pen, f=F_DRAW)
        )

    # =======================================================================
    # the reeds: one tick per filament, at the margin it enters or leaves by
    # =======================================================================
    def reed_h(
        xa: float, xb: float, ys: Sequence[float], pen: Optional[int], alt: float = 1.0
    ) -> None:
        # a real reed alternates dent lengths; 36 equal ticks at 1.3 mm read as
        # one solid black bar, which is what v4's exit looked like
        for k, yy in enumerate(sorted(ys)):
            w = (xb - xa) * (1.0 if k % 2 == 0 else alt)
            out.extend(_poly([(xb - w, yy), (xb, yy)], color=pen, f=F_DRAW))

    reed_h(U(0.014), U(0.038), [float(s.pts[0, 1]) for s in strands[:N_Q]], PR)
    reed_h(
        U(0.962),
        U(0.986),
        [float(s.pts[0, 1]) for s in strands[N_Q : N_Q + N_K]],
        PK,
    )
    reed_h(U(0.014), U(0.038), [float(s.pts[0, 1]) for s in strands[N_Q + N_K :]], PV)
    # the exit reed stands clear of the filament ends (they stop at x=214.5) so
    # it reads as a reed and not as a fringe on the end of the rope
    reed_h(U(0.958), U(0.986), [float(s.pts[-1, 1]) for s in strands], PZ, alt=0.52)

    # =======================================================================
    # type
    # =======================================================================
    for bt, bx, by, bh, btr, bp, bw in TYPE:
        out += _tracked(bt, bx, by, bh, btr, bp, word=bw)
    out += _stroke_text("T", sup_x, sup_y, sup_h, color=PB, f=F_DRAW, proportional=True)

    return out


def _bbox_near(poly: Sequence[Pt], cx: float, cy: float, r: float) -> bool:
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return (
        min(xs) - r <= cx <= max(xs) + r and min(ys) - r <= cy <= max(ys) + r
    )


def _strand_audit(strands: Sequence[Strand], bounds: Bounds) -> None:
    """Strand count in == strand count out, and nothing born or killed inside
    the sheet.  This is the brief's hard requirement, so it is an assertion and
    not a comment."""
    x0, y0, x1, y1 = bounds
    assert len(strands) == N_OUT, f"{len(strands)} filaments, expected {N_OUT}"
    n_in = sum(1 for s in strands if s.pts[0, 0] < x0 + 30 or s.pts[0, 0] > x1 - 30)
    n_out = sum(1 for s in strands if s.pts[-1, 0] > x1 - 30)
    assert n_in == N_OUT, f"{n_in} filaments enter at a margin, expected {N_OUT}"
    assert n_out == N_OUT, f"{n_out} filaments leave at a margin, expected {N_OUT}"
    for s in strands:
        assert len(s.pts) > 40, f"{s.fam}{s.idx} is a stub"
