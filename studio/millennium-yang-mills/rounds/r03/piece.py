"""YANG-MILLS MASS GAP -- r03, thesis ITERATE (parent r02, abstract).
Plate 4 of the MILLENNIUM series.

Lineage: Wassily Kandinsky, *Punkt und Linie zu Flaeche* (Bauhausbuch 9, 1926).
Order taken: POINT / LINE / PLANE as the three elements with weight and
direction.  Here that triad is not a metaphor: the joint spectrum of (H, |P|)
of pure SU(3) Yang-Mills, drawn in the half-plane p >= 0 with one scale on
both axes, has exactly three components and each has that dimension:

    POINT  the vacuum Omega              (E, p) = (0, 0)             dim 0
    LINES  one-glueball mass shells      E = sqrt(p^2 + M_i^2)       dim 1
    PLANE  the two-glueball continuum    E >= sqrt(p^2 + (2 Delta)^2) dim 2

and between the point and the first line there is NOTHING (the mass gap).

r03 = r02 with the chart furniture taken off the spine:
  * the point is a Kandinsky point: a solid disc of 9.5 mm, not the bar's foot;
  * every element (shells, rim, red 0++, strata, ghost cone) stops at ONE
    momentum crop x = 262 (p = 2.22), and the J^PC names sit flush-left at
    x = 265 in the gutter, each centred on its own line's end -- nothing is
    left on the spine that can read as a y-axis scale;
  * the statement carries the twist, the corner caption names the carriers;
  * superscripts are authored at >= 1.3 mm with a >= 0.8 mm sign gap.

Every mark is computed from ``../../data/glueball_spectrum.json``
(Athenodorou-Teper 2020, continuum limit, M/sqrt(sigma)); M/Delta is derived
here, not typed in.  Nothing on the sheet is an axis, tick or legend.

Design sheet: A3 portrait, mm, y UP from the bottom edge, drawable [15,282]x
[15,405].  The whole design is uniformly fitted to ``bounds``; PHYSICAL
quantities (strata pitch 1.0 mm, rim inset 0.29 mm, caps >= 1.8 mm, spiral
pitch 0.45 mm, dash 6/4 mm, superscripts >= 1.3 mm) are held in real
millimetres on any paper, so counts are recomputed, never pitches scaled.

Pens / layers, plotted in index order (light -> dark, red last):
    0 GHOST     grey 0.1   the light cone E = p: asymptote only, no state on it
    1 PLANE     black 0.2  the continuum strata
    2 TEXT      black 0.2  (same pen, own layer)  title, statement, tags, captions
    3 SPECTRUM  black 0.3  vacuum point, five shells, threshold rim
    4 RED       red 0.5    Delta: the 0++ shell + the heavy Delta bar + Delta glyph

Entry point: ``yang_mills_point_line_plane_r03``.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

# ===========================================================================
# the data  (read, never typed)
# ===========================================================================
_DATA = Path(__file__).resolve().parents[2] / "data" / "glueball_spectrum.json"


def _load_spectrum() -> Tuple[float, List[Tuple[str, str, float]]]:
    d = json.loads(_DATA.read_text())
    delta_sig = float(d["Delta_over_sqrt_sigma"][0])  # 3.405
    states = []
    for s in d["states"]:
        m = float(s["M_over_sqrt_sigma"]) / delta_sig
        states.append((s["JPC"], s["level"], m))
    return delta_sig, states


DELTA_SIG, STATES = _load_spectrum()
THRESH = float(json.loads(_DATA.read_text())["two_particle_threshold_over_Delta"])  # 2.0
# isolated shells strictly between Delta and 2 Delta, drawn black.  The 2++*
# (1.9935) lies 0.65 mm under the rim at s = 100 -- under the 0.8 mm floor --
# and is MERGED into the rim (declared on the sheet: "lies on 2 Delta within errors").
GROUND = [s for s in STATES if s[1] == "gs" and s[0] == "0++"][0]
BLACK_SHELLS = [
    s for s in STATES if 1.0 < s[2] < THRESH and (THRESH - s[2]) * 100.0 > 0.8
]
MERGED = [s for s in STATES if 1.0 < s[2] < THRESH and (THRESH - s[2]) * 100.0 <= 0.8]
assert abs(GROUND[2] - 1.0) < 1e-12
assert [round(s[2], 4) for s in BLACK_SHELLS] == [1.4373, 1.5495, 1.7195, 1.7812, 1.8561]

# ===========================================================================
# the design sheet (A3 portrait, mm, y up)
# ===========================================================================
SHEET = (15.0, 15.0, 282.0, 405.0)  # drawable frame of the design
S = 100.0  # mm per Delta, BOTH axes -> the cone is exactly 45 deg
X_AX = 40.0  # the spine p = 0 (never drawn; implied by every left end)
Y_VAC = 50.0  # E = 0
X_RIGHT = 282.0  # right frame
X_STOP = 262.0  # ONE momentum crop for every element (p = 2.22)
X_TAG = 265.0  # the gutter [265, 282]: names flush-left here
X_COL = 36.0  # the p < 0 column: the red Delta glyph flush-right here
Y_PLANE_TOP = 370.0  # the plane is cropped here (E = 3.20)
D_DISC = 9.5  # the vacuum point, ink diameter on the A3 design sheet (A1: 9-10 mm)

P_STOP = (X_STOP - X_AX) / S


def ex(p: float) -> float:
    return X_AX + S * p


def ey(E: float) -> float:
    return Y_VAC + S * E


def shell_E(p, m):
    return np.sqrt(np.asarray(p) ** 2 + m * m)


# ===========================================================================
# design -> sheet transform
# ===========================================================================
class Fit:
    def __init__(self, bounds):
        bx0, by0, bx1, by1 = bounds
        w, h = SHEET[2] - SHEET[0], SHEET[3] - SHEET[1]
        self.k = min((bx1 - bx0) / w, (by1 - by0) / h)
        self.ox = bx0 + ((bx1 - bx0) - w * self.k) / 2.0 - SHEET[0] * self.k
        self.oy = by0 + ((by1 - by0) - h * self.k) / 2.0 - SHEET[1] * self.k

    def pt(self, p: Pt) -> Pt:
        return (self.ox + p[0] * self.k, self.oy + p[1] * self.k)

    def run(self, r: Sequence[Pt]) -> Run:
        return [self.pt(p) for p in r]

    def phys(self, mm: float) -> float:
        """A physical length in mm -> design units."""
        return mm / self.k


# ===========================================================================
# type: own tiny setter on the house stroke font.  Authored here: the Delta
# (the font has none), the slashless zero (a slashed 0 reads as the empty set
# on a plate about emptiness -- r01), and the SUPERSCRIPT SIGNS: + - * drawn at
# a physical height >= 1.3 mm with a >= 0.8 mm gap between signs (S3), the *
# as a three-stroke star so 0++* never reads 0+++.
# ===========================================================================
SUP_RAISE = 0.6  # superscript baseline raised by 0.6 cap
SUP_MIN_MM = 1.30  # superscript sign height, physical
SIGN_GAP_MM = 1.00  # clear gap between the ink of adjacent superscript signs


class Type:
    """Holds the physical scale so superscripts keep their mm on any paper."""

    def __init__(self, fit: Fit):
        self.fit = fit

    def sup_h(self, cap: float) -> float:
        return max(cap * 0.6, self.fit.phys(SUP_MIN_MM))

    def _delta(self, x: float, y: float, cap: float) -> Tuple[List[Run], float]:
        w = cap * 0.86
        return [[(x, y), (x + w / 2, y + cap), (x + w, y), (x, y)]], w + cap * 0.28

    def _sign(self, ch: str, x: float, y: float, h: float) -> Tuple[List[Run], float]:
        """A superscript sign of ink box h x h, bottom-left at (x, y)."""
        gap = self.fit.phys(SIGN_GAP_MM)
        cx, cy, r = x + h / 2, y + h / 2, h / 2
        if ch == "+":
            runs = [[(cx, y), (cx, y + h)], [(x, cy), (x + h, cy)]]
        elif ch == "-":
            runs = [[(x, cy), (x + h, cy)]]
        else:  # '*': three strokes through the centre, 60 deg apart
            runs = []
            for k in range(3):
                a = math.pi / 2 + k * math.pi / 3
                runs.append([(cx - r * math.cos(a), cy - r * math.sin(a)),
                             (cx + r * math.cos(a), cy + r * math.sin(a))])
        return runs, h + gap

    def set(self, segs, x: float, y: float, cap: float, track: float = 0.0
            ) -> Tuple[List[Run], float]:
        """Typeset ``segs`` (a str, or a list of (str, 'n'|'sup')) at left baseline.

        Monospace on the house font (5.6 cell units); returns (runs, advance)."""
        if isinstance(segs, str):
            segs = [(segs, "n")]
        runs: List[Run] = []
        cx = x
        prev_sup = False
        for txt, mode in segs:
            if mode == "sup":
                h = self.sup_h(cap)
                base = y + cap * SUP_RAISE
                if not prev_sup:
                    cx += self.fit.phys(0.25)  # kern off the J digit
                for ch in txt:
                    rr, adv = self._sign(ch, cx, base, h)
                    runs += rr
                    cx += adv
                cx += -self.fit.phys(SIGN_GAP_MM) + cap * 0.35  # close the sup run
                prev_sup = True
                continue
            prev_sup = False
            sc = cap / 6.0
            for ch in txt:
                if ch == "Δ":
                    rr, adv = self._delta(cx, y, cap)
                    runs += rr
                    cx += adv + track
                    continue
                strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
                if ch == "0":
                    strokes = strokes[:1]  # slashless zero
                for st in strokes:
                    runs.append([(cx + gx * sc, y + gy * sc) for gx, gy in st])
                cx += 5.6 * sc + track
        return runs, cx - x

    def width(self, segs, cap, track=0.0) -> float:
        return self.set(segs, 0.0, 0.0, cap, track)[1]

    def wrap(self, text: str, cap: float, track: float, maxw: float) -> List[str]:
        lines, cur = [], ""
        for word in text.split(" "):
            trial = (cur + " " + word).strip()
            if cur and self.width(trial, cap, track) > maxw:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        if cur:
            lines.append(cur)
        return lines

    def fit_lines(self, lines: Sequence, cap: float, track: float, maxw: float) -> List:
        """Keep AUTHORED breaks; a line too wide is split into the fewest
        balanced lines (never a one-word widow).  Lines may be str or segs."""
        out: List = []
        for ln in lines:
            if self.width(ln, cap, track) <= maxw:
                out.append(ln)
                continue
            if not isinstance(ln, str):  # segs line: greedy wrap on words
                words: List[List[Tuple[str, str]]] = [[]]
                for txt, mode in ln:
                    if mode == "sup":
                        words[-1].append((txt, mode))
                        continue
                    parts = txt.split(" ")
                    for j, part in enumerate(parts):
                        if j > 0:
                            words.append([])
                        if part:
                            words[-1].append((part, mode))
                words = [w for w in words if w]
                cur: List[Tuple[str, str]] = []
                for w in words:
                    trial = cur + ([(" ", "n")] if cur else []) + w
                    if cur and self.width(trial, cap, track) > maxw:
                        out.append(cur)
                        cur = list(w)
                    else:
                        cur = trial
                if cur:
                    out.append(cur)
                continue
            words = ln.split(" ")
            best = None
            for n in (2, 3):
                if n > len(words):
                    break
                for cuts in itertools.combinations(range(1, len(words)), n - 1):
                    idx = (0,) + cuts + (len(words),)
                    parts = [" ".join(words[a:b]) for a, b in zip(idx, idx[1:])]
                    mw = max(self.width(q, cap, track) for q in parts)
                    if mw <= maxw and (best is None or mw < best[0]):
                        best = (mw, parts)
                if best:
                    break
            out += best[1] if best else self.wrap(ln, cap, track, maxw)
        return out


def jpc(label: str) -> List[Tuple[str, str]]:
    """'0++' -> J full size, PC (+ '*') as superscript."""
    return [(label[0], "n"), (label[1:], "sup")]


# ===========================================================================
# geometry
# ===========================================================================
def hyperbola(m: float, p0: float, p1: float, step_mm: float = 0.6) -> Run:
    """E = sqrt(p^2 + m^2) from p0 to p1, sampled at ~step_mm of arc."""
    n = max(8, int((p1 - p0) * S * 1.5 / step_mm))
    p = np.linspace(p0, p1, n + 1)
    E = shell_E(p, m)
    return [(ex(a), ey(b)) for a, b in zip(p, E)]


def rim_end_x(y: float, inset: float) -> Optional[float]:
    """x where a stratum at height y must end so that it stops `inset` mm
    (perpendicular) short of the rim E = sqrt(p^2 + 4).  None = no crossing."""
    E = (y - Y_VAC) / S
    x = None
    d = inset
    for _ in range(4):
        Ee = E - d / S
        if Ee <= THRESH:
            return None
        p = math.sqrt(Ee * Ee - THRESH * THRESH)
        slope = p / math.sqrt(p * p + THRESH * THRESH)  # dE/dp on the rim
        d = inset * math.sqrt(1.0 + slope * slope)  # vertical offset for a perp. inset
        x = ex(p)
    return x


def dashed(a: Pt, b: Pt, dash: float, gap: float, start_gap: float = 0.0,
           fit_end: bool = False) -> List[Run]:
    """Dashes from a (after start_gap) to b.  ``fit_end`` scales dash and gap
    by one common factor (~1 %) so a whole dash ends exactly ON b -- the
    ruling then stops at the same crop as every other element."""
    ax, ay = a
    bx, by = b
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    if fit_end:
        span = L - start_gap
        n = max(1, round((span + gap) / (dash + gap)))
        f = span / (n * dash + (n - 1) * gap)
        dash, gap = dash * f, gap * f
    out, t = [], start_gap
    while t < L - 0.5:
        t1 = min(L, t + dash)
        out.append([(ax + ux * t, ay + uy * t), (ax + ux * t1, ay + uy * t1)])
        t = t1 + gap
    return out


def disc_spiral(cx: float, cy: float, r: float, pitch: float) -> Run:
    """A solid point: an Archimedean spiral from the centre out to radius r at
    `pitch`, closed by one full circle on r so the edge is a clean round."""
    turns = max(2, int(r / pitch))  # floor: the realised pitch stays >= `pitch`
    pts = []
    n_per = 72
    n = turns * n_per
    for i in range(n + 1):
        t = i / n
        a = 2 * math.pi * turns * t
        pts.append((cx + r * t * math.cos(a), cy + r * t * math.sin(a)))
    for i in range(1, n_per + 1):
        a = 2 * math.pi * turns + 2 * math.pi * i / n_per
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ===========================================================================
# pens
# ===========================================================================
LAYERS = ("ghost", "plane", "text", "spectrum", "red")
NIB = {"ghost": 0.1, "plane": 0.2, "text": 0.2, "spectrum": 0.3, "red": 0.5}


def _pen_map(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 5:
        return {k: i for i, k in enumerate(LAYERS)}
    if colors == 4:
        return {"ghost": 0, "plane": 1, "text": 1, "spectrum": 2, "red": 3}
    if colors == 3:
        return {"ghost": 0, "plane": 1, "text": 1, "spectrum": 1, "red": 2}
    if colors == 2:
        return {"ghost": 0, "plane": 0, "text": 0, "spectrum": 0, "red": 1}
    return {k: None for k in LAYERS}


def _stack_tags(want: List[float], h: float, min_gap: float, floor: float) -> List[float]:
    """Centre heights for the gutter tags: as close to each line end as
    possible, kept in order with >= min_gap between blocks, never below
    `floor`.  A forward push, bottom to top, in order (no leaders).  On A3
    nothing moves (tightest pitch 3.8 mm > block 2.6 + 0.5 mm)."""
    c = list(want)
    pitch = h + min_gap
    c[0] = max(c[0], floor + h / 2)
    for i in range(1, len(c)):
        c[i] = max(c[i], c[i - 1] + pitch)
    return c


# ===========================================================================
# the plate
# ===========================================================================
def build_layers(fit: Fit) -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}
    ph = fit.phys
    ty = Type(fit)

    # ---- statement layout first: on small paper the physical 1.8 mm caps
    # wrap to more lines, and the plane's flat crop (E = 3.20 on A3) drops to
    # stay 2 mm clear of the last line.  The crop is a design line, not physics.
    cap_s = max(2.4, ph(1.8))
    tr_s = cap_s * 0.12
    stmt = ty.fit_lines(
        ["CLASSICAL YANG-MILLS WAVES RUN AT LIGHT SPEED, ON THE DASHED LINE.",
         "THE QUANTUM THEORY PUTS NO STATE THERE: NO MASSLESS GLUON, ONLY MASSIVE GLUEBALLS.",
         "THE CONE HOLDS ONLY ITS TIP, THE VACUUM. THEN NOTHING, UP TO Δ."],
        cap_s, tr_s, X_RIGHT - X_AX,
    )
    lead_s = cap_s * 1.8
    y_s0 = 388.0
    y_plane_top = min(Y_PLANE_TOP, y_s0 - (len(stmt) - 1) * lead_s - cap_s * 0.3 - ph(2.0))
    assert y_plane_top > ey(THRESH) + 60.0, "plane squeezed out"

    # ---- POINT: the vacuum, a Kandinsky point (spectrum pen 0.3) ----------
    # ink diameter 9.5 mm on A3; the spiral runs on the ink radius minus half
    # the nib, at 0.45 mm pitch -> reads solid, never floods (1 cycle).
    r_ink = D_DISC / 2.0
    L["spectrum"].append(disc_spiral(X_AX, Y_VAC, r_ink - ph(NIB["spectrum"] / 2), ph(0.45)))

    # ---- GHOST: the light cone E = p, the one driving diagonal ------------
    # from the disc edge to the momentum crop; 6 mm dash, 4 mm gap (encoding
    # s4), the first dash starting on the disc edge.
    L["ghost"] += dashed(
        (X_AX, Y_VAC), (X_STOP, Y_VAC + (X_STOP - X_AX)),
        dash=ph(6.0), gap=ph(4.0), start_gap=r_ink + ph(NIB["ghost"] / 2), fit_end=True,
    )

    # ---- LINES: five black shells + the threshold rim (spectrum pen) -------
    shells = sorted(BLACK_SHELLS, key=lambda s: s[2])
    for i, (lab, lev, m) in enumerate(shells):
        run = hyperbola(m, 0.0, P_STOP)
        L["spectrum"].append(run if i % 2 == 0 else run[::-1])
    rim = hyperbola(THRESH, 0.0, P_STOP)
    L["spectrum"].append(rim[::-1] if len(shells) % 2 else rim)

    # ---- PLANE: iso-energy strata above the rim ---------------------------
    pitch = ph(1.0)
    inset = ph(0.29)
    ys = []
    y = y_plane_top
    y_rim_v = ey(THRESH)
    while y > y_rim_v + inset:
        ys.append(y)
        y -= pitch
    ys = ys[::-1]  # bottom -> top
    for j, yy in enumerate(ys):
        xr = rim_end_x(yy, inset)
        xr = X_STOP if xr is None else min(xr, X_STOP)
        if xr - X_AX < 1.0:
            continue
        seg = [(X_AX, yy), (xr, yy)]
        L["plane"].append(seg if j % 2 == 0 else seg[::-1])

    # ---- RED: Delta.  The heavy bar (Kandinsky's line with weight) and the
    # 0++ shell as ONE stroke: up the spine from the disc edge to the 0++
    # vertex, then out along the shell to the crop.
    off = ph(0.4)
    # the red nib's round cap reaches 0.25 below the path end; the red ink
    # starts 0.05 mm above the disc's ink top -- on the edge, never on the black
    y_bar0 = Y_VAC + r_ink + ph(0.25 + 0.05)
    red_shell = hyperbola(GROUND[2], 0.0, P_STOP)
    red_bar = [
        [(X_AX + off, y_bar0), (X_AX + off, ey(1.0) - ph(0.4)),
         (X_AX - off, ey(1.0)), (X_AX - off, y_bar0),
         (X_AX, y_bar0)] + red_shell,
    ]
    # red Delta glyph: p < 0 column, flush-right on X_COL, mid-gap -- names the
    # red (the 0++ gets no tag at the crop: no room between lens and 2++)
    g_cap = 10.0
    g_w = g_cap * 0.86
    gy = (Y_VAC + ey(1.0)) / 2.0 - g_cap / 2.0
    L["red"] += ty._delta(X_COL - g_w, gy, g_cap)[0] + red_bar

    # ---- TEXT -------------------------------------------------------------
    T: Dict[str, List[Run]] = {k: [] for k in ("cap", "colo", "tags", "stmt", "title")}

    # J^PC tags in the gutter: flush-left at X_TAG, each centred on the height
    # at which its own line meets the crop.  0++ is named by the red Delta
    # glyph and the caption instead (the lens ceiling leaves no room).
    cap_tag = max(2.2, ph(1.8))
    tag_items = [(s[0] + ("*" if s[1] == "ex1" else ""), s[2]) for s in shells]
    tag_items.append(("2Δ", THRESH))
    blk_h = cap_tag * SUP_RAISE + ty.sup_h(cap_tag)  # ink block: baseline .. sup top
    want = [float(ey(math.sqrt(P_STOP ** 2 + m * m))) for _, m in tag_items]
    # nothing below the lens' continuation over the gutter (red at the far
    # edge of the widest tag) + 1 mm
    widths = [ty.width([("2", "n"), ("Δ", "n")] if lab == "2Δ" else jpc(lab), cap_tag)
              for lab, _ in tag_items]
    p_far = (X_TAG + max(widths) - X_AX) / S
    floor = ey(math.sqrt(p_far ** 2 + 1.0)) + ph(1.0)
    centres = _stack_tags(want, blk_h, ph(0.5), floor)
    TAG_LOG.clear()
    for (lab, m), c, w in zip(tag_items, centres, widths):
        segs = [("2", "n"), ("Δ", "n")] if lab == "2Δ" else jpc(lab)
        base = c - blk_h / 2.0 if lab != "2Δ" else c - cap_tag / 2.0
        runs, _ = ty.set(segs, X_TAG, base, cap_tag)
        T["tags"] += runs
        TAG_LOG.append((lab, c, ey(math.sqrt(P_STOP ** 2 + m * m)), base, w))

    # title + statement, flush-left on the spine, above the plane
    cap_t = max(6.0, ph(1.8))
    title_runs, _ = ty.set("YANG-MILLS  MASS GAP", X_AX, 397.0, cap_t, track=cap_t * 0.30)
    for r in title_runs:  # display weight: 3 passes of the 0.2 nib, one pen-down
        a = _offset_polyline(r, ph(-0.18))
        c = _offset_polyline(r, ph(0.18))
        T["title"].append(a + list(r)[::-1] + c)
    for i, ln in enumerate(stmt):
        T["stmt"] += ty.set(ln, X_AX, y_s0 - i * lead_s, cap_s, track=tr_s)[0]

    # colophon: flush-left on the outer margin, under the vacuum; ends with
    # the lineage
    cap_c = max(1.8, ph(1.8))
    tr_c = cap_c * 0.08
    lead = cap_c * 1.85
    # widen the measure (small paper) until the block clears the point by 2 mm
    for frac in (0.40, 0.50, 0.60, 0.75, 1.0):
        colo = ty.fit_lines(["CLAY PROBLEM: PROVE THE THEORY EXISTS ON R⁴",
                             "AND THAT Δ > 0. OPEN.",
                             "AFTER KANDINSKY, PUNKT UND LINIE ZU FLAECHE, 1926."],
                            cap_c, tr_c, (X_RIGHT - SHEET[0]) * frac)
        if 18.0 + lead * (len(colo) - 1) + cap_c < Y_VAC - r_ink - ph(2.0):
            break
    yb = 18.0 + lead * (len(colo) - 1)
    colo_top, colo_right = yb + cap_c, SHEET[0]
    for ln in colo:
        runs, w = ty.set(ln, SHEET[0], yb, cap_c, track=tr_c)
        T["colo"] += runs
        colo_right = max(colo_right, SHEET[0] + w)
        yb -= lead

    # corner caption: flush-right on the frame, in the far corner of the
    # spacelike void (below the cone).  It NAMES the carriers (S1).
    cap_w = (X_RIGHT - SHEET[0]) * 0.52
    cap_src = [
        "THE POINT: THE VACUUM.",
        "EACH LINE: ONE GLUEBALL, ITS MASS THE HEIGHT OF ITS LEFT END.",
        [("RED LINE: THE LIGHTEST GLUEBALL 0", "n"), ("++", "sup"), (", MASS Δ.", "n")],
        "RULED PLANE: EVERY PAIR OF GLUEBALLS, FROM EXACTLY 2Δ.",
        "HEIGHT ENERGY, WIDTH MOMENTUM, ONE SCALE. PURE SU(3).",
        "MASSES: LATTICE, ATHENODOROU-TEPER 2020.",
        [("2", "n"), ("++*", "sup"), (" LIES ON 2Δ WITHIN ERRORS. STATES ABOVE 2Δ OMITTED.", "n")],
    ]
    cap_lines = ty.fit_lines(cap_src, cap_c, tr_c, cap_w)
    widths = [ty.width(sg, cap_c, track=tr_c) for sg in cap_lines]
    y0 = 18.0
    if X_RIGHT - max(widths) < colo_right + 10.0:
        y0 = colo_top + lead
    lead_cap = lead * 1.08  # a touch more air: the superscripts ride high
    yb = y0 + lead_cap * (len(cap_lines) - 1)
    for segs, w in zip(cap_lines, widths):
        x0 = X_RIGHT - w
        assert yb + cap_c * 1.5 < Y_VAC + (x0 - X_AX) - 6.0, "caption crosses the cone"
        T["cap"] += ty.set(segs, x0, yb, cap_c, track=tr_c)[0]
        yb -= lead_cap

    for k in ("cap", "colo", "tags", "stmt", "title"):
        L["text"] += T[k]
    return L


TAG_LOG: List[Tuple[str, float, float, float, float]] = []


def yang_mills_point_line_plane_r03(rng: SeededRNG, bounds, colors: int = 5) -> List[GCodeCommand]:
    """POINT / LINE / PLANE: the joint (p, E) spectrum of pure SU(3) Yang-Mills.

    Deterministic: the plate is exact data; ``rng`` is accepted for the
    contract and deliberately unused (nothing on the sheet is random).
    """
    _ = rng
    fit = Fit(bounds)
    L = build_layers(fit)
    pens = _pen_map(colors)
    out: List[GCodeCommand] = []
    for layer in LAYERS:
        f = 1800 if layer in ("ghost", "red", "spectrum") else 2200
        for r in L[layer]:
            out += _poly(fit.run(r), color=pens[layer], f=f)
    return out
