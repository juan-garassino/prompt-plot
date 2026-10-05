"""YANG-MILLS MASS GAP — r02, thesis ABSTRACT.  Plate 4 of the MILLENNIUM series.

Lineage: Wassily Kandinsky, *Punkt und Linie zu Flaeche* (Bauhausbuch 9, 1926).
Order taken: POINT / LINE / PLANE as the three elements with weight and
direction.  Here that triad is not a metaphor: the joint spectrum of (H, |P|)
of pure SU(3) Yang-Mills, drawn in the half-plane p >= 0 with one scale on
both axes, has exactly three components and each has that dimension:

    POINT  the vacuum Omega              (E, p) = (0, 0)             dim 0
    LINES  one-glueball mass shells      E = sqrt(p^2 + M_i^2)       dim 1
    PLANE  the two-glueball continuum    E >= sqrt(p^2 + (2 Delta)^2) dim 2

and between the point and the first line there is NOTHING (the mass gap).

Every mark is computed from ``../../data/glueball_spectrum.json``
(Athenodorou-Teper 2020, continuum limit, M/sqrt(sigma)); M/Delta is derived
here, not typed in.  Nothing on the sheet is an axis, tick or legend.

Design sheet: A3 portrait, mm, y UP from the bottom edge, drawable [15,282]x
[15,405].  The whole design is uniformly fitted to ``bounds``; PHYSICAL
quantities (strata pitch 1.0 mm, rim inset 0.29 mm, caps >= 1.8 mm, disc
>= 2.2 mm) are held in real millimetres on any paper, so the strata count is
recomputed, never the pitch scaled.

Layout (abstract thesis, encoding 5A with two stated departures): the J^PC
names sit in the p < 0 column at the VERTICES (rest masses), not at a right
tag column, so no name ever enters the lens' extension; and with the tag
column gone every line, the rim, the strata and the red shell crop AT the
right frame (p = 2.42).

Pens / layers, plotted in index order (light -> dark, red last):
    0 GHOST     grey 0.1   the light cone E = p: asymptote only, no state on it
    1 PLANE     black 0.2  the continuum strata
    2 TEXT      black 0.2  (same pen, own layer)  title, statement, tags, captions
    3 SPECTRUM  black 0.3  vacuum point, five shells, threshold rim
    4 RED       red 0.5    Delta: the 0++ shell + the heavy Delta bar + Delta glyph

Entry point: ``yang_mills_point_line_plane``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.generators import _GLYPHS, _glyph_advance, _poly
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
# and is MERGED into the rim (declared on the sheet).
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
X_STOP = X_RIGHT  # shells, rim, strata and the red shell all crop AT the frame (p = 2.42)
X_COL = 36.0  # the p < 0 column: names flush-RIGHT here, 4 mm off the spine
Y_PLANE_TOP = 370.0  # the plane is cropped here (E = 3.20)

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
# type: own tiny setter on the house stroke font, with an authored Delta
# (the font has none), superscripts and tracking.
# ===========================================================================
SUP = 0.6  # superscript size, raised by 0.6 cap


def _delta_glyph(x: float, y: float, cap: float) -> Tuple[List[Run], float]:
    w = cap * 0.86
    return [[(x, y), (x + w / 2, y + cap), (x + w, y), (x, y)]], w + cap * 0.28


def _star_glyph(x: float, y: float, cap: float) -> Tuple[List[Run], float]:
    """An authored six-armed asterisk: the font's '*' shrinks to a '+' at
    superscript size, which made 0++* read as 0+++."""
    r = cap * 0.5
    cx, cy = x + r, y + r
    runs = []
    for k in range(3):
        a = math.pi / 2 + k * math.pi / 3
        runs.append([(cx - r * math.cos(a), cy - r * math.sin(a)),
                     (cx + r * math.cos(a), cy + r * math.sin(a))])
    return runs, 2 * r + cap * 0.3


def set_text(
    segs,
    x: float,
    y: float,
    cap: float,
    track: float = 0.0,
    proportional: bool = False,
) -> Tuple[List[Run], float]:
    """Typeset ``segs`` (a str, or a list of (str, 'n'|'sup')) at left baseline.

    Returns (runs, advance width).  'Δ' is drawn as an authored triangle.
    """
    if isinstance(segs, str):
        segs = [(segs, "n")]
    runs: List[Run] = []
    cx = x
    for txt, mode in segs:
        h = cap * (SUP if mode == "sup" else 1.0)
        base = y + (cap * 0.6 if mode == "sup" else 0.0)
        sc = h / 6.0
        for ch in txt:
            if ch == "Δ":
                rr, adv = _delta_glyph(cx, base, h)
                runs += rr
                cx += adv + track
                continue
            if ch == "*" and mode == "sup":
                rr, adv = _star_glyph(cx, base + h * 0.05, h * 0.8)
                runs += rr
                cx += adv + track
                continue
            strokes = _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
            for st in strokes:
                runs.append([(cx + gx * sc, base + gy * sc) for gx, gy in st])
            cx += (_glyph_advance(ch) * sc if proportional else 5.6 * sc) + track
    return runs, cx - x - (track if segs else 0.0)


def text_width(segs, cap, track=0.0, proportional=False) -> float:
    return set_text(segs, 0.0, 0.0, cap, track, proportional)[1]


def wrap(text: str, cap: float, track: float, maxw: float) -> List[str]:
    """Greedy word wrap on the monospace setter (never shrinks the type)."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if cur and text_width(trial, cap, track) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def fit_lines(lines: Sequence[str], cap: float, track: float, maxw: float) -> List[str]:
    """Keep the AUTHORED breaks; a line too wide for ``maxw`` is split into the
    fewest balanced lines (minimise the longest) -- never a one-word widow."""
    out: List[str] = []
    for ln in lines:
        if text_width(ln, cap, track) <= maxw:
            out.append(ln)
            continue
        words = ln.split(" ")
        best = None
        for n in (2, 3):
            if n > len(words):
                break
            import itertools

            for cuts in itertools.combinations(range(1, len(words)), n - 1):
                idx = (0,) + cuts + (len(words),)
                parts = [" ".join(words[a:b]) for a, b in zip(idx, idx[1:])]
                mw = max(text_width(q, cap, track) for q in parts)
                if mw <= maxw and (best is None or mw < best[0]):
                    best = (mw, parts)
            if best:
                break
        out += best[1] if best else wrap(ln, cap, track, maxw)
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


def dashed(a: Pt, b: Pt, dash: float, gap: float, start_gap: float = 0.0) -> List[Run]:
    ax, ay = a
    bx, by = b
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    out, t = [], start_gap
    while t < L - 0.5:
        t1 = min(L, t + dash)
        out.append([(ax + ux * t, ay + uy * t), (ax + ux * t1, ay + uy * t1)])
        t = t1 + gap
    return out


def disc_spiral(cx: float, cy: float, r: float, pitch: float) -> Run:
    turns = max(2, int(math.ceil(r / pitch)))
    n = turns * 36
    pts = []
    for i in range(n + 1):
        t = i / n
        a = 2 * math.pi * turns * t
        pts.append((cx + r * t * math.cos(a), cy + r * t * math.sin(a)))
    # close on the rim so the edge is a clean circle
    for i in range(1, 37):
        a = 2 * math.pi * turns + 2 * math.pi * i / 36
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ===========================================================================
# pens
# ===========================================================================
LAYERS = ("ghost", "plane", "text", "spectrum", "red")


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


# ===========================================================================
# the plate
# ===========================================================================
def build_layers(fit: Fit) -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}
    ph = fit.phys

    # ---- POINT: the vacuum, one solid disc (spectrum pen 0.3) -------------
    r_disc = max(1.5, ph(1.1))  # >= 2.2 mm physical diameter
    L["spectrum"].append(disc_spiral(X_AX, Y_VAC, r_disc, ph(0.24)))

    # ---- GHOST: the light cone E = p, the one driving diagonal ------------
    # from the disc edge to the right frame; dashes, never a state.
    y_exit = Y_VAC + (X_RIGHT - X_AX)  # 45 deg exactly
    L["ghost"] += dashed(
        (X_AX, Y_VAC), (X_RIGHT, y_exit), dash=9.0, gap=3.0, start_gap=r_disc + ph(0.8)
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
    y = Y_PLANE_TOP
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
    # vertex, then out along the shell.  Two flanking passes thicken the bar.
    y_bar0 = Y_VAC + r_disc + ph(0.15 + 0.25 + 0.15)  # clear of the black disc
    red_shell = hyperbola(GROUND[2], 0.0, P_STOP)
    off = ph(0.4)
    # ONE pen-down: up the right pass, down the left pass, up the centre and
    # out along 0++ to the frame.  The 0.4 mm jogs hide inside the 1.3 mm bar,
    # and a single stroke leaves the travel optimiser nothing to scatter.
    red_bar = [
        [(X_AX + off, y_bar0), (X_AX + off, ey(1.0) - ph(0.4)),
         (X_AX - off, ey(1.0)), (X_AX - off, y_bar0),
         (X_AX, y_bar0)] + red_shell,
    ]

    # red Delta glyph: in the p < 0 column (outside the half-section, so
    # outside the lens), flush-right on the name column, mid-gap
    g_cap = 10.0
    g_w = g_cap * 0.86
    gy = (Y_VAC + ey(1.0)) / 2.0 - g_cap / 2.0
    # stroke order: glyph, then the bar passes, then the long stroke out to
    # the frame -- no sheet-crossing travel inside the layer
    L["red"] += _delta_glyph(X_COL - g_w, gy, g_cap)[0] + red_bar

    # ---- TEXT -------------------------------------------------------------
    # built in buckets, emitted in a travel-short order: caption (bottom
    # right) -> colophon (bottom left) -> names up the staff -> statement -> title
    T: Dict[str, List[Run]] = {k: [] for k in ("cap", "colo", "tags", "stmt", "title")}
    # J^PC names sit at the VERTICES, i.e. at p = 0, where E is the rest mass
    # itself: a staff of names in the p < 0 column, flush-right on X_COL.
    cap_tag = max(2.2, ph(1.8))
    tag_items = [(GROUND[0], GROUND[2])] + [
        (s[0] + ("*" if s[1] == "ex1" else ""), s[2]) for s in shells
    ]
    tag_items.append(("2Δ", THRESH))
    placed: List[Tuple[float, float, float]] = []  # (x_right, y0, y1)
    for lab, m in tag_items:
        segs = [("2", "n"), ("Δ", "n")] if lab == "2Δ" else jpc(lab)
        w = text_width(segs, cap_tag)
        base = ey(m) - cap_tag / 2.0
        xr = X_COL
        # stagger leftward only if a name would collide with the one below
        # (never on A3; can happen on A5/A6 where the caps are held at 1.8 mm)
        for (pxr, py0, py1) in placed:
            if base < py1 + ph(0.5) and abs(pxr - xr) < 1e-9:
                xr = pxr - w - ph(1.5)
        runs, _ = set_text(segs, xr - w, base, cap_tag)
        T["tags"] += runs
        placed.append((xr, base, base + cap_tag * 1.25))

    # title + statement, flush-left on the spine, above the plane
    cap_t = max(6.0, ph(1.8))
    title_runs, _ = set_text("YANG-MILLS  MASS GAP", X_AX, 397.0, cap_t, track=cap_t * 0.30)
    # display weight: three passes of the 0.2 nib at 0.18 mm -> a 0.56 mm
    # stroke, chained out-back-out into ONE pen-down per glyph stroke (the
    # 0.18 mm joins vanish inside the stroke width) -> 1/3 of the pen cycles
    for r in title_runs:
        a = _offset_polyline(r, ph(-0.18))
        c = _offset_polyline(r, ph(0.18))
        T["title"].append(a + list(r)[::-1] + c)
    # statement: one line on A3; word-wrapped (never shrunk under 1.8 mm) on
    # small paper, wrapping DOWNWARD toward the plane but never into it
    cap_s = max(2.4, ph(1.8))
    tr_s = cap_s * 0.12
    stmt = wrap(
        "THE LIGHT CONE HOLDS ONLY ITS TIP, THE VACUUM. THEN NOTHING, UP TO Δ.",
        cap_s, tr_s, X_RIGHT - X_AX,
    )
    lead_s = cap_s * 1.8
    for i, ln in enumerate(stmt):
        T["stmt"] += set_text(ln, X_AX, 384.0 - i * lead_s, cap_s, track=tr_s)[0]
    assert 384.0 - (len(stmt) - 1) * lead_s - cap_s * 0.3 > Y_PLANE_TOP + ph(2.0), "statement hits plane"

    # colophon: flush-left on the outer margin, under the vacuum
    cap_c = max(1.8, ph(1.8))
    tr_c = cap_c * 0.08
    lead = cap_c * 1.85
    colo = fit_lines(["CLAY PROBLEM: PROVE THE THEORY EXISTS ON R⁴", "AND THAT Δ > 0. OPEN."],
                     cap_c, tr_c, (X_RIGHT - SHEET[0]) * 0.42)
    yb = 18.0 + lead * (len(colo) - 1)
    colo_top, colo_right = yb + cap_c, SHEET[0]
    for ln in colo:
        runs, w = set_text(ln, SHEET[0], yb, cap_c, track=tr_c)
        T["colo"] += runs
        colo_right = max(colo_right, SHEET[0] + w)
        yb -= lead

    # corner caption: flush-right on the frame, in the far corner of the
    # spacelike void (below the cone).  Shares the colophon's bottom baseline
    # when they fit side by side; otherwise it stacks up INTO the void.
    cap_w = (X_RIGHT - SHEET[0]) * 0.55
    cap_lines = [
        [(ln, "n")]
        for ln in fit_lines(
            ["PURE SU(3) GAUGE THEORY.",
             "HEIGHT ENERGY, WIDTH MOMENTUM, ONE SCALE.",
             "MASSES: LATTICE, ATHENODOROU-TEPER 2020."],
            cap_c, tr_c, cap_w)
    ]
    last = [("2", "n"), ("++*", "sup"), (" SITS ON 2Δ, STATES ABOVE 2Δ OMITTED.", "n")]
    if text_width(last, cap_c, track=tr_c) <= cap_w:
        cap_lines.append(last)
    else:
        cap_lines += [[("2", "n"), ("++*", "sup"), (" SITS ON 2Δ,", "n")],
                      [("STATES ABOVE 2Δ OMITTED.", "n")]]
    widths = [text_width(sg, cap_c, track=tr_c) for sg in cap_lines]
    y0 = 18.0
    if X_RIGHT - max(widths) < colo_right + 10.0:
        y0 = colo_top + lead
    yb = y0 + lead * (len(cap_lines) - 1)
    for segs, w in zip(cap_lines, widths):
        x0 = X_RIGHT - w
        # the block lives below the ghost cone, in the spacelike field
        assert yb + cap_c < Y_VAC + (x0 - X_AX) - 6.0, "caption crosses the cone"
        T["cap"] += set_text(segs, x0, yb, cap_c, track=tr_c)[0]
        yb -= lead

    for k in ("cap", "colo", "tags", "stmt", "title"):
        L["text"] += T[k]
    return L


def yang_mills_point_line_plane(rng: SeededRNG, bounds, colors: int = 5) -> List[GCodeCommand]:
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
