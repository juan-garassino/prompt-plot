"""THE POINCARE CONJECTURE -- r03 (iterate; parent r02, thesis ABSTRACT).  Plate 6 of the
MILLENNIUM series.

r03 = the surgery instant as the spine: the t_s keyline alone on its own black 0.5 layer,
single pass, inside a bare 2.5 mm moat (every other line pauses in it); the keyline yields to
the red caps at the waist (0.8 mm cream edge to edge); a paused ring stays paused for the
whole crowded arc (no stroke < 15 mm on the line layer); relative-race footer.  The flow
data, the 62 mm/u scale, the 62 deg axis, the cut at (165, 200) and both type columns are
the parent's, unchanged.

Lineage: Vera Molnar, *(Des)Ordres* (1974) -- nested closed figures whose deviation from
the ideal form is measured ring by ring.  Order taken (not the look): here the deviation
(a pear with a cap) is removed by Ricci flow until each nest is round and vanishes.

ORDER: BRANCHING NEST -> two FLOW-TO-ATTRACTOR nests, stacked by time-occlusion.
Mapping in one line: each closed line is the whole space at one instant, drawn in meridian
section; one line = dt 0.01 of Ricci time counted from the cut; past lines lie outside the
keyline, future lines inside it; red circle = the cut, red points = where a piece vanishes.

Every line is a solver output: ``snapshots.npz`` written by ``run_snapshots.py`` (this
round; a copy of data/run_neckpinch.py that lands exactly on t = 0 and t_s + 0.01 k,
max |t_snap - t_target| = 0).  Embedding (z, rho) by data/ricci_rot.embed.  Alignment:
pre-surgery the neck minimum is pinned at the cut; post-surgery each piece's psi^2 ds
centroid is held at its t_s position.  Nothing is placed by eye; no randomness.

FLAT BY DECLARATION: the meridian plane is the only place the profile embeds honestly,
so depth is spent on TIME through the occlusion stack (terraced mounds), not on a view.

Design sheet: A3 portrait, mm, y UP, drawable [15,282] x [15,405], fitted to ``bounds``.

Pens / layers, plotted in index order (lines 0.3 -> keyline 0.5 -> type -> red):
    0 LINES  black 0.3   the space at each instant: start line, past halo, 33 + 6 rings
    1 KEY    black 0.5   the surgery instant t_s, ONE pass, paused where the red caps run
    2 TEXT   black 0.3   title, statement, captions, footer (same pen as layer 0)
    3 RED    red 0.5     the events of the proof: the cut (two caps), two extinction
                         points, the word SOLVED

Entry point: ``poincare_two_nests``.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from matplotlib.path import Path as MPath

from promptplot.generative.engine.geometry import resample_by_arclength
from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.engine.scene3d import Occupancy
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

HERE = Path(__file__).resolve().parent
_SNAP = HERE / "snapshots.npz"
_DATA = HERE.parents[1] / "data"


def _load_mod(name: str):
    spec = importlib.util.spec_from_file_location(f"_poincare_{name}", _DATA / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_RR = _load_mod("ricci_rot")

# ===========================================================================
# the design sheet (A3 portrait, mm, y up) -- encoding section 5
# ===========================================================================
SHEET = (15.0, 15.0, 282.0, 405.0)
X_L, Y_B, X_R, Y_T = SHEET
S_MM = 62.0  # mm per unit of the (z, rho) half-plane, both directions
AXIS_DEG = 62.0  # the axis of revolution rises toward the upper right (not drawn)
CUT = (165.0, 200.0)  # sheet position of the cut (neck minimum at t_s)
COL = 205.0  # the right text column: corner caption + footer, flush-left
SEP = 0.85  # merge floor, mm (0.8 governs; 0.05 margin for sample-to-sample tests)
STEP = 0.25  # resampling step for occupancy tests, mm
MIN_FRAG = 15.0  # r03: no line-layer stroke shorter than this (whole rings excepted), mm
RESUME_SEP = 1.2  # a paused line resumes only this far clear, mm
MOAT = 3.05  # r03 A1: bare moat about the keyline centre-line, mm (>= 2.5; 3.0 + sampling margin)
MOAT_RESUME = 3.4  # a line paused in the moat resumes only this far out, mm
TWIN = 1.5  # r03 A2: a SHORT broken stretch (< TWIN_LEN) running this close to kept ink
TWIN_FRAC = 0.6  # over most of its length is a twin of that line, not a line: it merges
TWIN_LEN = 30.0  # mm (= 2 x MIN_FRAG); longer stretches are lines and are never touched
KEY_NIB = 0.5
LINE_NIB = 0.3
RED_CLEAR = 0.8  # r03 A3: cream between red and black ink edges, mm
DOT_R = 0.95  # extinction point radius (ink edge), mm: Ø1.9
RED_NIB = 0.5

E_AX = (math.cos(math.radians(AXIS_DEG)), math.sin(math.radians(AXIS_DEG)))
N_AX = (-E_AX[1], E_AX[0])


def to_sheet(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return np.column_stack([CUT[0] + S_MM * (u * E_AX[0] + v * N_AX[0]),
                            CUT[1] + S_MM * (u * E_AX[1] + v * N_AX[1])])


# ===========================================================================
# data: the isochrones, aligned
# ===========================================================================
REPORT: Dict[str, object] = {}


def _neck_z(z: np.ndarray, psi: np.ndarray) -> float:
    """z of the neck minimum, parabola through the 5 nodes around the discrete min."""
    c = psi[3:-3]
    m = (c <= psi[2:-4]) & (c <= psi[4:-2])
    idx = np.nonzero(m)[0]
    i = int(idx[np.argmin(c[idx])] + 3)
    a, b, _ = np.polyfit(z[i - 2:i + 3], psi[i - 2:i + 3], 2)
    return float(-b / (2 * a))


def _centroid(z: np.ndarray, psi: np.ndarray, L: float) -> float:
    s = np.linspace(0, L, len(psi))
    w = psi ** 2
    return float(np.trapezoid(z * w, s) / np.trapezoid(w, s))


class Iso:
    """one isochrone: the outline (u, +-rho) of the space at time t."""

    def __init__(self, kind: str, k: int, t: float, u: np.ndarray, rho: np.ndarray):
        self.kind, self.k, self.t = kind, k, t
        self.u, self.rho = u, rho

    def ring_uv(self) -> Tuple[np.ndarray, np.ndarray]:
        u = np.concatenate([self.u, self.u[::-1][1:]])
        v = np.concatenate([self.rho, -self.rho[::-1][1:]])
        return u, v


def load_isochrones() -> Tuple[List[Iso], Dict[str, float]]:
    d = np.load(_SNAP)
    tags = [str(x) for x in d["tag"]]
    T, Ls, P = d["t"], d["L"], d["psi"]
    info = {k: float(d[k]) for k in ("t_s", "h_cut", "T_ext_A", "T_ext_B", "s_cut")}
    ts = info["t_s"]
    emb = [_RR.embed(P[j], Ls[j]) for j in range(len(tags))]
    j_key = tags.index("key")
    zk, rk = emb[j_key]
    zn_key = _neck_z(zk, rk)
    isos: List[Iso] = []
    growth = {}
    for j, tg in enumerate(tags):
        z, r = emb[j]
        if tg in ("start", "halo", "key"):
            u = z - _neck_z(z, r)
            k = int(round((ts - T[j]) / 0.01)) if tg == "halo" else 0
            isos.append(Iso(tg, k, float(T[j]), u, r))
            growth[tg if tg != "halo" else f"halo{k}"] = float(z[-1] - z[0])
    # post-surgery frames
    jA0, jB0 = tags.index("A0"), tags.index("B0")
    zA0, rA0 = emb[jA0]
    uA0 = zA0 - zn_key
    cA = _centroid(uA0, rA0, Ls[jA0])
    zB0, rB0 = emb[jB0]
    uB_pole = zk[-1] - zn_key
    cB = uB_pole - _centroid(zB0, rB0, Ls[jB0])
    info.update(cA=cA, cB=cB, u_cut=float(zk[int(round(info["s_cut"] / (Ls[j_key] / (len(rk) - 1))))] - zn_key))
    info["capA_tip_ts"] = float(uA0[-1])
    info["capB_tip_ts"] = float(uB_pole - zB0[-1])
    for j, tg in enumerate(tags):
        if tg not in ("A", "B"):
            continue
        z, r = emb[j]
        zc = _centroid(z, r, Ls[j])
        k = int(round((T[j] - ts) / 0.01))
        if tg == "A":
            u = z - zc + cA
            info[f"capA_tip_{k}"] = float(u[-1])
        else:
            u = cB - (z - zc)
            info[f"capB_tip_{k}"] = float(u[-1])
        isos.append(Iso(tg, k, float(T[j]), u, r))
    info["pole_to_pole"] = growth
    REPORT["info"] = info
    return isos, info


def race_numbers() -> Dict[str, float]:
    """relative radius loss t = 0 -> t_s, read straight off the solver snapshots:
    neck = the interior minimum of psi, large/small lobe = the two interior maxima."""
    d = np.load(_SNAP)
    tags = [str(x) for x in d["tag"]]
    out = {}
    prof = {}
    for tg in ("start", "key"):
        psi = d["psi"][tags.index(tg)]
        c = psi[1:-1]
        mx = np.nonzero((c >= psi[:-2]) & (c >= psi[2:]))[0] + 1
        mn = np.nonzero((c <= psi[:-2]) & (c <= psi[2:]))[0] + 1
        lob = sorted(float(psi[i]) for i in mx)
        prof[tg] = (float(psi[mn].min()), lob[0], lob[-1])
    (n0, s0, l0), (n1, s1, l1) = prof["start"], prof["key"]
    out.update(neck=100 * (1 - n1 / n0), small=100 * (1 - s1 / s0), large=100 * (1 - l1 / l0),
               neck0=n0, neck1=n1, small0=s0, small1=s1, large0=l0, large1=l1)
    return out


# ===========================================================================
# polyline helpers
# ===========================================================================
def plen(r: Sequence[Pt]) -> float:
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(r, r[1:]))


def dense(r: Sequence[Pt], step: float = STEP) -> Run:
    return [tuple(p) for p in resample_by_arclength(list(r), step=step)]


def rotate_closed(ring: np.ndarray, start: int) -> np.ndarray:
    """re-seat a closed ring (first == last) so it starts at vertex ``start``."""
    body = ring[:-1]
    body = np.roll(body, -start, axis=0)
    return np.vstack([body, body[:1]])


# ===========================================================================
# the line system: occlusion (time cards) + merge (rank by |t - t_s|)
# ===========================================================================
class Line:
    def __init__(self, iso: Iso, ring_mm: np.ndarray):
        self.iso = iso
        self.ring = ring_mm  # closed, sheet mm
        self.runs: List[Run] = [ring_mm.tolist()]
        self.drawn: List[Run] = []
        self.occluded_frac = 0.0

    @property
    def rank(self) -> Tuple[int, float, int]:
        k = self.iso.kind
        if k in ("key", "start"):
            return (0, 0.0 if k == "key" else 1.0, 0)
        order = {"halo": 0, "B": 1, "A": 2}[k]
        return (1, self.iso.k, order)


def build_lines(isos: List[Iso]) -> List[Line]:
    lines = []
    for it in isos:
        u, v = it.ring_uv()
        mm = to_sheet(u, v)
        # start every closed line at its far pole from the cut (the A/B pole
        # nearest the viewer's reading start), so a stroke never begins in the waist
        far = int(np.argmin(u)) if it.kind in ("A", "start", "halo", "key") else int(np.argmax(u))
        ring = rotate_closed(mm, far)
        ring = np.asarray(resample_by_arclength([tuple(p) for p in ring], step=0.5))
        lines.append(Line(it, ring))
    return lines


def occlude(lines: List[Line]) -> None:
    """Time-occlusion: every isochrone is an opaque card; later cards lie on top.
    A line is drawn only where no later card covers it.  Exceptions (stated):
    the KEYLINE is never occluded (sacred event line); future rings are
    occluded only by later rings of their own piece (the two pieces are
    disjoint); past lines by later past lines + the keyline."""
    by_kind: Dict[str, List[Line]] = {}
    for ln in lines:
        by_kind.setdefault(ln.iso.kind, []).append(ln)
    key = by_kind["key"][0]
    past = sorted(by_kind["start"] + by_kind["halo"], key=lambda l: l.iso.t)
    for i, ln in enumerate(past):
        later = [q for q in past[i + 1:]] + [key]
        _clip_against(ln, later)
    for kind in ("A", "B"):
        fut = sorted(by_kind[kind], key=lambda l: l.iso.t)
        for i, ln in enumerate(fut):
            _clip_against(ln, fut[i + 1:])


def _seg_cross(a: np.ndarray, b: np.ndarray, ring: np.ndarray) -> Optional[float]:
    """smallest parameter t in (0,1] where segment a->b crosses the closed ring
    (vectorised over the ring's edges); exact line-line intersection."""
    p, q = ring[:-1], ring[1:]
    d = b - a
    e = q - p
    den = d[0] * e[:, 1] - d[1] * e[:, 0]
    ok = np.abs(den) > 1e-12
    w = p - a
    t = np.where(ok, (w[:, 0] * e[:, 1] - w[:, 1] * e[:, 0]) / np.where(ok, den, 1), -1)
    s = np.where(ok, (w[:, 0] * d[1] - w[:, 1] * d[0]) / np.where(ok, den, 1), -1)
    m = ok & (t >= -1e-9) & (t <= 1 + 1e-9) & (s >= -1e-9) & (s < 1 + 1e-9)
    if not m.any():
        return None
    return float(np.clip(t[m].min(), 0.0, 1.0))


def _clip_against(ln: Line, later: List[Line]) -> None:
    """exact clip of a closed ring against the union of later cards: vertices are
    classified by point-in-polygon; every in/out transition is cut exactly ON
    the covering card's edge (segment-edge intersection)."""
    ring = ln.ring
    L0 = plen(ring.tolist())
    pts = ring[:-1]
    ins = np.zeros(len(pts), bool)
    owner = np.full(len(pts), -1)
    cards = []
    for q in later:
        m = MPath(q.ring).contains_points(pts)
        if m.any():
            owner[m & ~ins] = len(cards)
            ins |= m
            cards.append(q.ring)
    if not ins.any():
        ln.occluded_frac = 0.0
        return
    if ins.all():
        ln.runs, ln.occluded_frac = [], 1.0
        return
    n = len(pts)
    s0 = int(np.argmin(ins))  # an outside vertex: open the ring there
    idx = [(s0 + i) % n for i in range(n + 1)]
    runs: List[Run] = []
    cur: Run = []
    for a_i, b_i in zip(idx, idx[1:]):
        A, B = pts[a_i], pts[b_i]
        if not ins[a_i]:
            if not cur:
                cur = [tuple(A)]
            if ins[b_i]:
                t = min([c for c in (_seg_cross(A, B, cards[j]) for j in range(len(cards))) if c is not None],
                        default=1.0)
                cur.append(tuple(A + t * (B - A)))
                runs.append(cur)
                cur = []
            else:
                cur.append(tuple(B))
        elif not ins[b_i]:
            ts = [c for c in (_seg_cross(B, A, cards[j]) for j in range(len(cards))) if c is not None]
            t = min(ts, default=1.0)
            cur = [tuple(B + t * (A - B)), tuple(B)]
    if cur and len(cur) >= 2:
        runs.append(cur)
    ln.runs = [r for r in runs if len(r) >= 2]
    ln.occluded_frac = 1.0 - sum(plen(r) for r in ln.runs) / L0


def merge(lines: List[Line], occ: Occupancy, occ_hi: Optional[Occupancy] = None) -> None:
    """Rank by |t - t_s| (the keyline first, then the start line, then by k).

    r03 rule, three clauses:
      * MOAT (A1): the keyline is drawn whole (its own layer); every other line
        pauses wherever it comes within MOAT of the keyline centre-line and
        resumes only at MOAT_RESUME (two engine Occupancy grids fed the keyline).
      * FLOOR: a line pauses within SEP of any higher-ranked drawn line and
        resumes at RESUME_SEP (hysteresis, as r02).
      * ARC (A2): after pausing, a drawn stretch shorter than MIN_FRAG is not a
        line, it is a stutter: it is dropped, so a ring that pauses on a crowded
        rim arc stays paused for the whole arc.  Whole rings are exempt.
      * TWIN (A2): a stretch shorter than TWIN_LEN that runs within TWIN of
        kept ink over > TWIN_FRAC of its length is that line's twin, not a
        line: it merges (in practice only t_s-0.05's last 16 mm beside t = 0).
    Only the kept ink is added to the occupancy grids, so the next-ranked line
    sees exactly what is on paper (the merge reads as the surviving line)."""
    key = next(l for l in lines if l.iso.kind == "key")
    moat, moat_hi = Occupancy(MOAT), Occupancy(MOAT_RESUME)
    for r in key.runs:
        for x, y in dense(r, 0.2):
            moat.add(x, y)
            moat_hi.add(x, y)
    REPORT["frags_dropped"] = 0
    REPORT["twins_dropped"] = []
    twin = Occupancy(TWIN)
    for ln in sorted(lines, key=lambda l: l.rank):
        sacred = ln.iso.kind == "key"
        ring_len = plen(ln.ring.tolist())
        out: List[Run] = []
        for r in ln.runs:
            if plen(r) < 1e-6:
                continue
            smp = dense(r)
            if sacred:
                keep = [True] * len(smp)
            else:
                keep, paused = [], False
                for x, y in smp:
                    if not paused and (occ.crowded(x, y) or moat.crowded(x, y)):
                        paused = True
                    elif paused and not ((occ_hi or occ).crowded(x, y) or moat_hi.crowded(x, y)):
                        paused = False
                    keep.append(not paused)
            cur: Run = []
            for p, kk in zip(smp, keep):
                if kk:
                    cur.append(p)
                else:
                    if len(cur) >= 2:
                        out.append(cur)
                    cur = []
            if len(cur) >= 2:
                out.append(cur)
        # stitch the two ends of a closed line whose run wraps the seam
        out = _stitch(out)
        if not sacred:
            whole = len(out) == 1 and abs(plen(out[0]) - ring_len) < 1.0
            if not whole:
                n0 = len(out)
                out = [r for r in out if plen(r) >= MIN_FRAG]
                REPORT["frags_dropped"] += n0 - len(out)
                kept = []
                for r in out:
                    fr = float(np.mean([twin.crowded(x, y) for x, y in r]))
                    REPORT.setdefault("twin_frac", []).append((ln.iso.kind, ln.iso.k, round(plen(r), 1), round(fr, 2)))
                    if plen(r) < TWIN_LEN and fr > TWIN_FRAC:
                        REPORT["twins_dropped"].append((ln.iso.kind, ln.iso.k, round(plen(r), 1), round(fr, 2)))
                    else:
                        kept.append(r)
                out = kept
        for r in out:
            for x, y in r:
                twin.add(x, y)
                occ.add(x, y)
                if occ_hi is not None:
                    occ_hi.add(x, y)
        ln.drawn = out


def _stitch(runs: List[Run]) -> List[Run]:
    if len(runs) >= 2:
        a, b = runs[-1], runs[0]
        if math.hypot(a[-1][0] - b[0][0], a[-1][1] - b[0][1]) < 1e-6:
            return [a + b[1:]] + runs[1:-1]
    return runs


# ===========================================================================
# type: the house stroke font (4 x 6 cell) + authored glyphs the font lacks
# ===========================================================================
EXTRA = {
    "É": _GLYPHS["E"] + [[(1.5, 6.8), (2.7, 7.9)]],
    "Δ": [[(0.0, 0.0), (2.0, 6.0), (4.0, 0.0), (0.0, 0.0)]],
    "π": [[(0.0, 4.0), (4.0, 4.0)], [(1.1, 4.0), (1.1, 0.0)], [(2.9, 4.0), (2.9, 0.7), (3.5, 0.0)]],
    "ψ": [[(0.0, 4.0), (0.0, 2.3), (0.6, 1.3), (2.0, 0.9), (3.4, 1.3), (4.0, 2.3), (4.0, 4.0)],
          [(2.0, 5.4), (2.0, -1.6)]],
    "–": [[(0.3, 3.0), (3.7, 3.0)]],
}


def _strokes(ch: str):
    if ch == "\u00a0":
        return []
    if ch in EXTRA:
        return EXTRA[ch]
    g = _GLYPHS.get(ch)
    if g is None:
        g = _GLYPHS.get(ch.upper())
    if g is None and ch not in " \u00a0":
        raise KeyError(f"glyph missing: {ch!r}")
    return g or []


def _metrics(ch: str, prop: bool) -> Tuple[float, float]:
    """(x shift, advance) in cell units.  Monospace = the font's 5.6 cell.
    Proportional is measured here from the glyph's own ink: the engine's
    _glyph_advance returns a width but _stroke_text draws the glyph at its
    un-normalised offset, so a narrow 'i' (ink at x = 1.8, advance 1.1)
    lands on its neighbour (engine request in NOTES)."""
    if not prop:
        return 0.0, 5.6
    if ch in " \u00a0":
        return 0.0, 2.6
    st = _strokes(ch)
    xs = [p[0] for s in st for p in s]
    x0, x1 = min(xs), max(xs)
    b = 0.95 if (ch.islower() or ch in ",.;:") else 1.25
    return -x0 + b / 2.0, (x1 - x0) + b


def set_text(txt: str, x: float, y: float, cap: float, track: float = 0.0,
             prop: bool = False) -> Tuple[List[Run], float]:
    runs: List[Run] = []
    sc = cap / 6.0
    cx = x
    for ch in txt:
        dx, adv = _metrics(ch, prop)
        for st in _strokes(ch):
            runs.append([(cx + (gx + dx) * sc, y + gy * sc) for gx, gy in st])
        cx += adv * sc + track
    return runs, (cx - x - track) if txt else 0.0


def text_width(txt: str, cap: float, track: float = 0.0, prop: bool = False) -> float:
    return set_text(txt, 0.0, 0.0, cap, track, prop)[1]


def split_corners(r: Run, max_turn: float = 50.0) -> List[Run]:
    out, cur = [], [r[0]]
    for i in range(1, len(r) - 1):
        cur.append(r[i])
        a = math.atan2(r[i][1] - r[i - 1][1], r[i][0] - r[i - 1][0])
        b = math.atan2(r[i + 1][1] - r[i][1], r[i + 1][0] - r[i][0])
        turn = abs((math.degrees(b - a) + 180.0) % 360.0 - 180.0)
        if turn > max_turn:
            out.append(cur)
            cur = [r[i]]
    cur.append(r[-1])
    out.append(cur)
    return out


def heavy(runs: List[Run], offsets: Sequence[float]) -> List[Run]:
    """display weight: parallel passes chained out-back-out into one pen-down."""
    out = []
    for r in (q for r0 in runs for q in split_corners(r0)):
        if len(r) < 2:
            continue
        chain: Run = []
        for j, d in enumerate(offsets):
            q = _offset_polyline(r, d) if d else list(r)
            chain += q if j % 2 == 0 else q[::-1]
        out.append(chain)
    return out


def wrap(text: str, cap: float, track: float, width: float) -> List[str]:
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, cap, track) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ===========================================================================
# red: the cut, the two extinction points
# ===========================================================================
def cap_arcs(h: float, u_cut: float) -> List[Run]:
    """A's cap ')' (bulges toward B, u >= u_cut) and B's cap '(' (u <= u_cut):
    radius h, centre on the cut; each semicircle ends ON the keyline."""
    out = []
    for sgn in (+1, -1):
        a = np.linspace(-math.pi / 2, math.pi / 2, 90)
        u = u_cut + sgn * h * np.cos(a)
        v = h * np.sin(a)
        out.append(to_sheet(u, v).tolist())
    return out


def solid_dot(cx: float, cy: float, r_ink: float, nib: float = RED_NIB, pitch: float = 0.4) -> Run:
    """one pen-down: outer circle at the ink radius, then an Archimedean spiral in."""
    rc = r_ink - nib / 2.0
    pts: Run = []
    for a in np.linspace(0, 2 * math.pi, 40):
        pts.append((cx + rc * math.cos(a), cy + rc * math.sin(a)))
    turns = rc / pitch
    for a in np.linspace(0, 2 * math.pi * turns, int(40 * turns) + 2):
        r = rc * (1 - a / (2 * math.pi * turns))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def yield_keyline(kr: Run, info: Dict[str, float]) -> List[Run]:
    """A3: at the waist the heavy line yields to the red.  The caps are one circle
    of radius h about the cut (centre-line); the keyline pauses wherever its
    centre-line runs within RED_CLEAR + half of both nibs of that circle, i.e.
    where the caps replace the neck.  Returns the keyline as strokes, each
    re-seated so no stroke starts inside the waist."""
    cc = to_sheet(np.array([info["u_cut"]]), np.array([0.0]))[0]
    R = info["h_cut"] * S_MM
    lim = RED_CLEAR + RED_NIB / 2.0 + KEY_NIB / 2.0 + 0.02
    smp = np.asarray(dense(kr, 0.1))
    d = np.abs(np.hypot(smp[:, 0] - cc[0], smp[:, 1] - cc[1]) - R)
    keep = d >= lim
    runs: List[Run] = []
    cur: Run = []
    for p, k in zip(smp.tolist(), keep):
        if k:
            cur.append(tuple(p))
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    runs = _stitch(runs)
    # pause lengths per flank (arc length of keyline removed), and the gap chord
    gaps = []
    i = 0
    n = len(keep)
    seg = np.hypot(*np.diff(smp, axis=0).T)
    while i < n:
        if not keep[i]:
            j = i
            while j < n and not keep[j]:
                j += 1
            a0, a1 = smp[max(i - 1, 0)], smp[min(j, n - 1)]
            gaps.append((float(seg[max(i - 1, 0):min(j, n - 1)].sum()), float(np.hypot(*(a1 - a0))),
                         tuple(np.round(smp[(i + j) // 2], 2))))
            i = j
        else:
            i += 1
    REPORT["key_gaps"] = gaps
    REPORT["key_red_lim"] = lim
    return [dense(r, 0.5) for r in runs]


# ===========================================================================
# ordering for batched streaming
# ===========================================================================
def chain_order(runs: List[Run], start: Pt) -> List[Run]:
    rest = [list(r) for r in runs]
    out: List[Run] = []
    pos = start
    while rest:
        best, bi, flip = 1e18, 0, False
        for i, r in enumerate(rest):
            for fl, e in ((False, r[0]), (True, r[-1])):
                dd = (e[0] - pos[0]) ** 2 + (e[1] - pos[1]) ** 2
                if dd < best:
                    best, bi, flip = dd, i, fl
        r = rest.pop(bi)
        r = r[::-1] if flip else r
        out.append(r)
        pos = r[-1]
    return out


# ===========================================================================
# the plate
# ===========================================================================
LAYERS = ("lines", "key", "text", "red")
BOXES: List[Tuple[float, float, float, float]] = []


def _pen_map(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 4:
        return {"lines": 0, "key": 1, "text": 2, "red": 3}
    if colors == 3:
        return {"lines": 0, "key": 1, "text": 0, "red": 2}
    if colors == 2:
        return {"lines": 0, "key": 0, "text": 0, "red": 1}
    return {k: None for k in LAYERS}


def build_layers() -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}
    isos, info = load_isochrones()
    lines = build_lines(isos)
    occlude(lines)
    occ = Occupancy(SEP)
    merge(lines, occ, Occupancy(RESUME_SEP))
    REPORT["lines"] = lines

    # ---- LINES layer, stated stroke order ----------------------------------
    def of(kind):
        return sorted([l for l in lines if l.iso.kind == kind], key=lambda l: l.iso.t)

    key = of("key")[0]
    seq: List[Run] = []
    pos = (X_L, Y_B)
    for ln in of("start") + of("halo"):
        rr = chain_order(ln.drawn, pos)
        seq += rr
        pos = rr[-1][-1] if rr else pos
    L["key"] = yield_keyline(key.drawn[0], info)
    for ln in of("B") + of("A"):
        rr = chain_order(ln.drawn, pos)
        seq += rr
        pos = rr[-1][-1] if rr else pos
    L["lines"] = seq

    # ---- RED ----------------------------------------------------------------
    h = info["h_cut"]
    red = cap_arcs(h, info["u_cut"])
    pA = to_sheet(np.array([info["cA"]]), np.array([0.0]))[0]
    pB = to_sheet(np.array([info["cB"]]), np.array([0.0]))[0]
    red.append(solid_dot(pA[0], pA[1], DOT_R))
    red.append(solid_dot(pB[0], pB[1], DOT_R))
    REPORT["dots"] = (tuple(pA), tuple(pB))

    # ---- the race, every number from snapshots.npz (S1) ----------------------
    rc = race_numbers()
    REPORT["race"] = rc
    RACE = (f"NECK −{rc['neck']:.0f}\u00a0% · SMALL LOBE −{rc['small']:.0f}\u00a0% · LARGE LOBE "
            f"−{rc['large']:.0f}\u00a0% · CUT AND CAPPED AT t\u00a0=\u00a0{info['t_s']:.3f}")

    # ---- TEXT ---------------------------------------------------------------
    T: List[Run] = []
    R: List[Run] = []
    BOXES.clear()

    def put(txt, x, y, cap, track=0.0, prop=False, right=False, dest=None, weight=None):
        w = text_width(txt, cap, track, prop)
        x0 = x - w if right else x
        runs, _ = set_text(txt, x0, y, cap, track, prop)
        if weight:
            runs = heavy(runs, weight)
        (dest if dest is not None else T).extend(runs)
        BOXES.append((x0 - 1.0, y - 0.35 * cap - 1.0, x0 + w + 1.0, y + 1.35 * cap + 1.0))
        return w

    cap_t = 8.0
    tr_t = 3.2
    wt = (-0.3, -0.1, 0.1, 0.3)
    yt = Y_T - cap_t * 7.9 / 6.0 - 0.4  # the acute on É is the top of the ink
    put("THE POINCARÉ", X_L + 0.4, yt, cap_t, tr_t, weight=wt)
    put("CONJECTURE", X_L + 0.4, yt - cap_t - 7.0, cap_t, tr_t, weight=wt)
    y = yt - cap_t - 7.0 - 14.0
    cap_s = 3.5
    Y_STMT = y
    for ln in ("Every closed, simply connected 3-manifold", "is homeomorphic to the 3-sphere."):
        put(ln, X_L, y, cap_s, 0.25, prop=True)
        y -= cap_s * 2.0
    y -= 5.0
    cap_st = 4.2
    wsol = put("SOLVED", X_L + 0.2, y, cap_st, cap_st * 0.35, dest=R, weight=(-0.2, 0.0, 0.2))
    cap_c = 2.2
    tr_c = cap_c * 0.12
    put("G. PERELMAN 2002–03", X_L + wsol + 5.0, y, cap_c, tr_c)
    y -= cap_c * 2.0
    for ln in ("RICCI FLOW WITH SURGERY, AFTER R. HAMILTON (1982)",
               "FIELDS MEDAL 2006, CLAY PRIZE 18 MAR 2010: BOTH DECLINED"):
        put(ln, X_L + wsol + 5.0, y, cap_c, tr_c)
        y -= cap_c * 2.0
    REPORT["title_block_bottom"] = y

    # top-right corner caption, flush right
    cap_k = 2.5
    # both corner lines share the footer's flush-left axis x = COL; tracking is
    # solved so the longer line ends exactly on the right margin
    c1, c2 = "TO PROVE IT IS ONE SPHERE", "THE FLOW CUTS IT IN TWO"
    ink1 = text_width(c1, cap_k) - (5.6 - 4.0) * cap_k / 6.0
    tr_k = ((X_R - COL) - ink1) / (len(c1) - 1)
    put(c1, COL, Y_T - cap_k, cap_k, tr_k)
    put(c2, COL, Y_T - cap_k - 6.0, cap_k, tr_k)

    # the series caption (A4): same x = COL column, its two baselines registered
    # on the statement's two baselines; one tracking, solved so the longer line
    # ends on the right margin
    cap_m = 2.2
    s1, s2 = "MILLENNIUM PRIZE PROBLEMS 6 / 7", "CLAY MATHEMATICS INSTITUTE, 2000"
    lng = max((s1, s2), key=lambda q: text_width(q, cap_m))
    ink_l = text_width(lng, cap_m) - (5.6 - 4.0) * cap_m / 6.0
    tr_m = ((X_R - COL) - ink_l) / (len(lng) - 1)
    REPORT["series_track"] = tr_m
    for i, ln in enumerate((s1, s2)):
        put(ln, COL, Y_STMT - i * 3.5 * 2.0, cap_m, tr_m)

    # footer: lower right, flush-left column
    fx0 = COL
    fw = X_R - fx0
    foot = [
        "EACH LINE: THE WHOLE SPACE AT ONE INSTANT, IN SECTION — EVERY CHORD A ROUND 2-SPHERE",
        "OUTSIDE THE HEAVY LINE: BEFORE THE\u00a0CUT · INSIDE: AFTER",
        "ONE LINE = Δt\u00a00.01 OF ∂g/∂t\u00a0=\u00a0−2\u00a0Ric, COUNTED FROM THE\u00a0CUT."
        " OUTERMOST LINE: t\u00a0=\u00a00 (OFF THE\u00a0GRID)",
        RACE,
        "SMALL PIECE VANISHES ROUND AT t\u00a0=\u00a00.117, LARGE AT t\u00a0=\u00a00.387",
        "IN 2-D THE SAME NECK WOULD WIDEN (0.314 → 0.355): EACH RING IS SECRETLY A SPHERE",
    ]
    colo = ["arXiv math/0211159 · 0303109 · 0307245", "ANGENENT–KNOPF 2004 · ROTATIONALLY SYMMETRIC, h = 0.12"]
    lead = cap_c * 1.8
    flines: List[str] = []
    for i, para in enumerate(foot):
        flines += wrap(para.replace("—", "-"), cap_c, tr_c, fw)
        flines.append("")
    cap_o = 1.8
    olines: List[str] = []
    for para in colo:
        olines += wrap(para, cap_o, cap_o * 0.12, fw)
    ytop = Y_B + len(olines) * cap_o * 1.8 + 4.0 + len(flines) * lead
    y = ytop
    for ln in flines:
        y -= lead
        if ln:
            put(ln, fx0, y, cap_c, tr_c)
    y -= 1.0
    for ln in olines:
        y -= cap_o * 1.8
        put(ln, fx0, y, cap_o, cap_o * 0.12)
    REPORT["footer_top"] = ytop

    L["text"] = T
    L["red"] = red + R
    # clearance: every text box against every drawn line sample
    allp = np.array([p for r in L["lines"] for p in r])
    clr = []
    for (x0, y0, x1, y1) in BOXES:
        dx = np.maximum(np.maximum(x0 - allp[:, 0], allp[:, 0] - x1), 0)
        dy = np.maximum(np.maximum(y0 - allp[:, 1], allp[:, 1] - y1), 0)
        clr.append(float(np.hypot(dx, dy).min()))
    REPORT["text_clearance_min"] = min(clr)
    cc = to_sheet(np.array([info["u_cut"]]), np.array([0.0]))[0]
    rr = np.hypot(allp[:, 0] - cc[0], allp[:, 1] - cc[1])
    # keyline excluded (tangent by construction): nearest non-keyline ink to the cut circle
    nk = np.array([p for ln in lines if ln.iso.kind in ("A", "B", "halo", "start") for r in ln.drawn for p in r])
    REPORT["cut_circle_bare_mm"] = float(np.hypot(nk[:, 0] - cc[0], nk[:, 1] - cc[1]).min() - h * S_MM - RED_NIB / 2 - 0.15)
    for nm, pp in (("A", pA), ("B", pB)):
        REPORT[f"dot_bare_{nm}_mm"] = float(np.hypot(allp[:, 0] - pp[0], allp[:, 1] - pp[1]).min() - DOT_R - 0.15)
    REPORT["cut_diam_over_A_width"] = (2 * h) / (2 * float(max(i.rho.max() for i in isos if i.kind == "key")))
    REPORT["ink_bbox"] = (allp[:, 0].min(), allp[:, 1].min(), allp[:, 0].max(), allp[:, 1].max())
    return L


def poincare_two_nests(rng: SeededRNG, bounds, colors: int = 3) -> List[GCodeCommand]:
    """Neckpinch -> surgery -> extinction as one branching nest of isochrones.

    Deterministic: every mark is solver output; ``rng`` is accepted for the
    contract and deliberately unused."""
    _ = rng
    bx0, by0, bx1, by1 = bounds
    w, hh = X_R - X_L, Y_T - Y_B
    k = min((bx1 - bx0) / w, (by1 - by0) / hh)
    ox = bx0 + ((bx1 - bx0) - w * k) / 2.0 - X_L * k
    oy = by0 + ((by1 - by0) - hh * k) / 2.0 - Y_B * k
    L = build_layers()
    pens = _pen_map(colors)
    out: List[GCodeCommand] = []
    for layer in LAYERS:
        f = 1500 if layer in ("red", "key") else 2000
        for r in L[layer]:
            out += _poly([(ox + x * k, oy + y * k) for x, y in r], color=pens[layer], f=f)
    return out


if __name__ == "__main__":
    import time

    t0 = time.time()
    L = build_layers()
    print(f"built in {time.time() - t0:.1f}s")
    for k, v in L.items():
        print(k, len(v), "strokes", round(sum(plen(r) for r in v) / 1000, 3), "m")
    info = REPORT["info"]
    for k, v in info.items():
        print(k, v)
    for ln in REPORT["lines"]:
        a = np.asarray(ln.ring)
        print(f"{ln.iso.kind:5s} k={ln.iso.k:2d} t={ln.iso.t:.4f} occl={ln.occluded_frac:.3f} "
              f"frags={len(ln.drawn):2d} drawn={sum(plen(r) for r in ln.drawn):7.1f} "
              f"x[{a[:, 0].min():.0f},{a[:, 0].max():.0f}] y[{a[:, 1].min():.0f},{a[:, 1].max():.0f}]")
    print({k: REPORT[k] for k in ("cut_circle_bare_mm", "dot_bare_A_mm", "dot_bare_B_mm", "cut_diam_over_A_width")})
    print("clearance", REPORT["text_clearance_min"], "bbox", REPORT["ink_bbox"])
    print("dots", REPORT["dots"], "footer_top", REPORT["footer_top"], "title bottom", REPORT["title_block_bottom"])
    print("race", REPORT["race"])
    print("key gaps (arc mm, chord mm, mid)", REPORT["key_gaps"], "lim", REPORT["key_red_lim"])
    print("twins dropped", REPORT["twins_dropped"])
    print("short stretches twin frac", [q for q in REPORT["twin_frac"] if q[2] < 40])
    print("frags dropped", REPORT["frags_dropped"], "series track", REPORT["series_track"])
    print("line strokes < 15 mm:", sorted(round(plen(r), 1) for r in L["lines"] if plen(r) < 15))
