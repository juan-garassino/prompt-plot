"""YANG-MILLS MASS GAP — faithful reconstruction, r01.  Millennium plate 4.

THE EMPTY TIP.  The joint energy-momentum spectrum of pure SU(3) Yang-Mills in
the (p, E) plane, drawn exactly: one POINT (the vacuum, at the apex of the light
cone), six LINES (one-glueball mass shells E = sqrt(p^2 + M^2), M from
Athenodorou-Teper 2020, continuum limit), one PLANE (the two-glueball continuum,
everything above E = sqrt(p^2 + 4)).  The light cone E = |p| is drawn only as a
ghost dashed asymptote: no state lies on it.  Between the tip and the red 0++
shell there is nothing -- blank paper, the mass gap.

Lineage: Wassily Kandinsky, *Punkt und Linie zu Flaeche* (Bauhausbuch 9, 1926).
Order taken: point, line, plane as the three elements with weight and
direction; here they are the literal dimensions of the three spectral
components.

FAITHFUL thesis: an illustrator's reconstruction of ``ref/reference.png``
(1122 x 1402).  Measured off the raster (colour masks, row/column scans), in
normalised sheet (u right, v DOWN):

    red I-beam        u = 0.500 (bar), serifs u 0.487..0.513 (8.0 mm @A3)
                      v 0.4608 (top serif) .. 0.6940 (bottom) = 0.2332 H
                      = 97.9 mm on an A3 height -> s = 100 mm/Delta (enc. s)
    red Delta glyph   v 0.5678 .. 0.5877 = 0.0199 H = 8.4 mm tall @A3,
                      centred on the bar's midpoint (v 0.5774)
    bar break         v 0.5563 .. 0.5977 = +-8.7 mm about the glyph centre
    specimen cluster  v 0.017 .. 0.445, ink centroid (u 0.500, v 0.214)
    silent middle     v 0.445 .. 0.741 (0.296 H)
    vacuum band       v 0.741 .. 0.929, full width u 0.020 .. 0.979
    title             v 0.942 .. 0.954, u 0.407 .. 0.647, centred, lowercase

Design space: the A3 portrait sheet in mm, y measured UP from the bottom edge,
frame [15, 282] x [15, 405].  Everything is mapped uniformly onto the passed
bounds; physical quantities (strata pitch, rim inset, dash/gap, disc, caps)
are held in millimetres ON PAPER and divided by the fit scale.

Pens (colors >= 5), in plotting order, light -> dark, red last:
    0 GHOST     grey 0.1   light cone (asymptote, empty)
    1 PLANE     black 0.2  two-glueball continuum strata
    2 TEXT      black 0.2  title, statement, captions, J^PC tags (own layer)
    3 SPECTRUM  black 0.3  vacuum point, five shells, 2Delta rim
    4 RED       red 0.5    0++ shell, Delta measure, Delta glyph

Entry point: ``yang_mills_mass_gap_faithful``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

GHOST, PLANE, TEXT, SPECTRUM, RED = range(5)

# ---------------------------------------------------------------------------
# the data (AT2020, SU(3), continuum limit) -- read from the slug's data file
# ---------------------------------------------------------------------------

_DATA = Path(__file__).resolve().parents[2] / "data" / "glueball_spectrum.json"
_FALLBACK = [  # M/sqrt(sigma), same table, in case the json is not beside us
    ("0", "++", 3.405),
    ("2", "++", 4.894),
    ("0", "-+", 5.276),
    ("0", "++*", 5.855),
    ("1", "+-", 6.065),
    ("2", "-+", 6.32),
]


def _shells() -> List[Tuple[str, str, float]]:
    """(J, PC tag, M/Delta) for every state strictly below 2Delta except the
    2++* at 1.9935, which is merged into the threshold (0.65 mm below it at A3,
    under the 0.8 mm floor) -- declared in the caption."""
    try:
        d = json.loads(_DATA.read_text())
        delta = d["Delta_over_sqrt_sigma"][0]
        out = []
        for s in d["states"]:
            m = s["M_over_sqrt_sigma"] / delta
            if m >= 1.99:  # 2++* merged into the rim, embedded states omitted
                continue
            pc = s["JPC"][1:] + ("*" if s["level"] != "gs" else "")
            out.append((s["JPC"][0], pc, m))
        return out
    except (OSError, KeyError, ValueError):
        return [(j, pc, m / 3.405) for j, pc, m in _FALLBACK]


# ---------------------------------------------------------------------------
# layout (A3 design mm, y up) -- encoding.md 5F, corrected where measured
# ---------------------------------------------------------------------------

FRAME = (15.0, 15.0, 282.0, 405.0)
S = 100.0            # mm per Delta, both axes (the cone measures 45 deg)
X_AXIS = 122.0       # p = 0 (u 0.411: off-centre, the reference is dead-centred)
Y_VAC = 60.0         # E = 0
X_STOP = 266.0       # shells, rim and strata stop here; tag column beyond
X_TAG = 269.0
Y_PLANE_TOP = 370.0  # E = 3.10, straight implied crop, no drawn line

# physical constants (mm on paper)
PITCH_PLANE = 1.0            # strata pitch (>= 0.8, >= 2.4 x 0.2)
INSET_RIM = 0.5 * 0.3 + 0.5 * 0.2 + 0.035   # 0.285 -> strata stop ON the rim
DASH, GAP = 6.0, 4.0         # ghost cone
DISC_D = 3.0                 # vacuum, outer ink diameter
NIB = {GHOST: 0.1, PLANE: 0.2, TEXT: 0.2, SPECTRUM: 0.3, RED: 0.5}
CAP_MIN = 1.8

# measured from the reference (see module docstring)
DELTA_GLYPH_H = 0.0199 * 420.0     # 8.4 mm
BAR_BREAK = 0.0207 * 420.0         # 8.7 mm half-gap about the glyph centre

F_DRAW = 1800


class Sheet:
    """Uniform map from the A3 design frame onto the passed bounds."""

    def __init__(self, bounds: Bounds):
        bx0, by0, bx1, by1 = bounds
        fx0, fy0, fx1, fy1 = FRAME
        self.k = min((bx1 - bx0) / (fx1 - fx0), (by1 - by0) / (fy1 - fy0))
        self.ox = bx0 + 0.5 * ((bx1 - bx0) - self.k * (fx1 - fx0))
        self.oy = by0 + 0.5 * ((by1 - by0) - self.k * (fy1 - fy0))

    def pt(self, p: Pt) -> Pt:
        return (self.ox + self.k * (p[0] - FRAME[0]), self.oy + self.k * (p[1] - FRAME[1]))

    def phys(self, mm: float) -> float:
        """A physical length on paper, expressed in design units."""
        return mm / self.k

    def cap(self, design_cap: float) -> float:
        """Caps never fall under 1.8 mm on paper."""
        return max(design_cap, CAP_MIN / self.k)


def _pens(colors: int) -> Dict[int, Optional[int]]:
    if colors >= 5:
        return {i: i for i in range(5)}
    if colors == 4:
        return {GHOST: 0, PLANE: 1, TEXT: 1, SPECTRUM: 2, RED: 3}
    if colors == 3:
        return {GHOST: 0, PLANE: 1, TEXT: 1, SPECTRUM: 1, RED: 2}
    if colors == 2:
        return {GHOST: 0, PLANE: 0, TEXT: 0, SPECTRUM: 0, RED: 1}
    return {i: None for i in range(5)}


# ---------------------------------------------------------------------------
# physics -> design mm
# ---------------------------------------------------------------------------


def _x(p: float) -> float:
    return X_AXIS + S * p


def _y(E: float) -> float:
    return Y_VAC + S * E


def _p(x: float) -> float:
    return (x - X_AXIS) / S


def shell(M: float, x0: float, x1: float, step: float = 0.4) -> Poly:
    """E = sqrt(p^2 + M^2), exact, sampled every ~step mm of x (the curve's
    slope is < 1 on the sheet, so arc spacing is < 1.42 step)."""
    n = max(2, int(math.ceil((x1 - x0) / step)))
    out = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        p = _p(x)
        out.append((x, _y(math.sqrt(p * p + M * M))))
    return out


def _rim_y(x: float) -> float:
    p = _p(x)
    return _y(math.sqrt(p * p + 4.0))


def _rim_slope(x: float) -> float:
    p = _p(x)
    return p / math.sqrt(p * p + 4.0)


def _rim_cross(y: float, d: float, side: int) -> Optional[float]:
    """x on branch ``side`` (-1 left, +1 right) where a horizontal line at y
    sits exactly ``d`` (perpendicular, design units) above the rim."""

    def g(x: float) -> float:
        return y - _rim_y(x) - d * math.sqrt(1.0 + _rim_slope(x) ** 2)

    a, b = X_AXIS, X_AXIS + side * 400.0
    if g(a) < 0:
        return None  # stratum below the rim vertex
    for _ in range(60):
        m = 0.5 * (a + b)
        if g(m) > 0:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


# ---------------------------------------------------------------------------
# type: proportional, tracked, with authored Delta and superscripts
# ---------------------------------------------------------------------------

_DELTA = [[(0.0, 0.0), (2.0, 6.0), (4.0, 0.0), (0.0, 0.0)]]
# five-spoke asterisk: the font's six-spoke '*' reads as '+' at superscript
# size (v2 crop: "0++*" read "0+++")
_STAR = [
    [(2.0, 3.0), (2.0 + 2.0 * math.cos(a), 3.0 + 2.0 * math.sin(a))]
    for a in (math.pi / 2 + 2 * math.pi * i / 5 for i in range(5))
]
_SB = 0.75       # side bearing, cell units (caps-only text)
_SPACE = 3.2     # word space, cell units
_GCACHE: dict = {}


def _glyph(ch: str):
    """(strokes shifted so the ink starts at the side bearing, advance).

    The house proportional advance measures the ink but draws the glyph at
    its cell offset, so a comma (ink at x 1.8) sat a full bearing away from
    its word and a space after ')' vanished -- measured on the v1 crops.
    The zero loses its slash: on a plate about emptiness a slashed 0 reads
    as the empty-set sign next to J^PC tags.
    """
    if ch in _GCACHE:
        return _GCACHE[ch]
    if ch == " ":
        res = ([], _SPACE)
    else:
        if ch == "Δ":
            strokes = _DELTA
        elif ch == "*":
            strokes = _STAR
        else:
            strokes = _GLYPHS.get(ch)
            if strokes is None:
                strokes = _GLYPHS.get(ch.upper(), [])
            if ch == "0":
                strokes = strokes[:1]
        xs = [p[0] for st in strokes for p in st]
        if not xs:
            res = ([], _SPACE)
        else:
            x0 = min(xs)
            sh = [[(gx - x0 + _SB, gy) for gx, gy in st] for st in strokes]
            res = (sh, (max(xs) - x0) + 2 * _SB)
    _GCACHE[ch] = res
    return res


# a run is (text, "n" | "sup")
Run = Tuple[str, str]


def _runs_width(runs: Sequence[Run], cap: float, track: float) -> float:
    w = 0.0
    n = 0
    for txt, mode in runs:
        c = cap * (0.6 if mode == "sup" else 1.0)
        for ch in txt:
            w += _glyph(ch)[1] * c / 6.0
            n += 1
    return w + track * cap * max(0, n - 1)


def text_runs(
    runs: Sequence[Run], x: float, y: float, cap: float, track: float = 0.0, align: str = "left"
) -> List[Poly]:
    """Polylines (design units) for one line of runs; (x, y) = baseline anchor."""
    if align == "right":
        x -= _runs_width(runs, cap, track)
    out: List[Poly] = []
    cx = x
    for txt, mode in runs:
        c = cap * (0.6 if mode == "sup" else 1.0)
        base = y + (0.6 * cap if mode == "sup" else 0.0)
        sc = c / 6.0
        for ch in txt:
            strokes, adv = _glyph(ch)
            for st in strokes:
                out.append([(cx + gx * sc, base + gy * sc) for gx, gy in st])
            cx += adv * sc + track * cap
    return out


def text(s: str, x: float, y: float, cap: float, track: float = 0.0, align: str = "left"):
    return text_runs([(s, "n")], x, y, cap, track, align)


def text_width(s: str, cap: float, track: float = 0.0) -> float:
    return _runs_width([(s, "n")], cap, track)


def parse(markup: str) -> List[Run]:
    """'2^{++*} SITS' -> [('2','n'), ('++*','sup'), (' SITS','n')]."""
    out: List[Run] = []
    i = 0
    while i < len(markup):
        j = markup.find("^{", i)
        if j < 0:
            out.append((markup[i:], "n"))
            break
        if j > i:
            out.append((markup[i:j], "n"))
        k = markup.index("}", j)
        out.append((markup[j + 2:k], "sup"))
        i = k + 1
    return [r for r in out if r[0]]


def wrap(markup: str, cap: float, track: float, max_w: float) -> List[List[Run]]:
    """Greedy word wrap of a markup paragraph to ``max_w`` design units.
    A '|' marks the preferred break: used only when the whole does not fit,
    so a short tail never orphans (v8 A5: the statement left 'Δ.' alone)."""
    whole = markup.replace("|", "")
    if "|" in markup:
        if _runs_width(parse(whole), cap, track) <= max_w:
            return [parse(whole)]
        return [ln for part in markup.split("|") for ln in wrap(part.strip(), cap, track, max_w)]
    lines: List[str] = []
    cur = ""
    for w in markup.split(" "):
        trial = w if not cur else cur + " " + w
        if cur and _runs_width(parse(trial), cap, track) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return [parse(ln) for ln in lines]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def dashes(a: Pt, b: Pt, on: float, off: float, start: float = 0.0) -> List[Poly]:
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    out = []
    t = start
    while t < L - 0.5:
        t1 = min(L, t + on)
        out.append([(a[0] + ux * t, a[1] + uy * t), (a[0] + ux * t1, a[1] + uy * t1)])
        t = t1 + off
    return out


def spiral_disc(cx: float, cy: float, r: float, pitch: float) -> Poly:
    turns = max(2, int(math.ceil(r / pitch)))
    n = turns * 36
    pts = []
    for i in range(n + 1):
        t = i / n
        a = 2 * math.pi * turns * t
        pts.append((cx + r * t * math.cos(a), cy + r * t * math.sin(a)))
    for i in range(1, 37):  # close on the rim so the edge is round
        a = 2 * math.pi * turns + 2 * math.pi * i / 36
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _line_isect(p1: Pt, d1: Pt, p2: Pt, d2: Pt) -> Pt:
    den = d1[0] * d2[1] - d1[1] * d2[0]
    t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / den
    return (p1[0] + d1[0] * t, p1[1] + d1[1] * t)


def delta_glyph(cx: float, cy: float, h: float, w: float, heavy: int, off: float) -> List[Poly]:
    """The red Delta: one closed triangle plus ``heavy`` extra passes on the
    right leg, offset inward by ``off`` and trimmed exactly to the base and
    the left leg -- the Didone thick stroke of the reference's glyph."""
    A, B, C = (cx - w / 2, cy - h / 2), (cx, cy + h / 2), (cx + w / 2, cy - h / 2)
    out = [[A, B, C, A]]
    dx, dy = C[0] - B[0], C[1] - B[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L  # left normal of B->C
    # inward = toward the centroid
    gx, gy = (A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3
    if (gx - B[0]) * nx + (gy - B[1]) * ny < 0:
        nx, ny = -nx, -ny
    for i in range(1, heavy + 1):
        o = (B[0] + nx * off * i, B[1] + ny * off * i)
        top = _line_isect(o, (dx, dy), A, (B[0] - A[0], B[1] - A[1]))
        bot = _line_isect(o, (dx, dy), A, (C[0] - A[0], C[1] - A[1]))
        out.append([top, bot] if i % 2 else [bot, top])
    return out


# ---------------------------------------------------------------------------
# the plate
# ---------------------------------------------------------------------------


def build(sh: Sheet) -> Dict[int, List[Poly]]:
    """All marks in design units, by semantic layer."""
    L: Dict[int, List[Poly]] = {GHOST: [], PLANE: [], TEXT: [], SPECTRUM: [], RED: []}
    x0, y0, x1, y1 = FRAME
    shells = _shells()

    # -- POINT: the vacuum, one solid 3 mm disc (0.3 pen: rim at r - nib/2) ---
    r_ink = 0.5 * sh.phys(DISC_D)
    r_path = r_ink - 0.5 * sh.phys(NIB[SPECTRUM])
    L[SPECTRUM].append(spiral_disc(X_AXIS, Y_VAC, r_path, sh.phys(0.24)))

    # -- GHOST: the light cone, dashed, from the disc edge to the frame -------
    start = r_ink + sh.phys(0.8)
    apex = (X_AXIS, Y_VAC)
    left_end = (x0, Y_VAC + (X_AXIS - x0))      # exits the left edge
    right_end = (x1, Y_VAC + (x1 - X_AXIS))     # exits the right edge
    for end in (left_end, right_end):
        L[GHOST] += dashes(apex, end, sh.phys(DASH), sh.phys(GAP), start=start)

    # -- LINES: the discrete spectrum ----------------------------------------
    # one stroke per shell, bottom -> top, alternating direction (batchable:
    # no sheet-crossing travel between consecutive strokes)
    black = [M for _, _, M in shells if abs(M - 1.0) > 1e-9] + [2.0]  # + the rim
    for i, M in enumerate(sorted(black)):
        poly = shell(M, x0, X_STOP)
        L[SPECTRUM].append(poly if i % 2 else poly[::-1])
    L[RED].append(shell(1.0, x0, x1))  # the gap's edge runs frame to frame

    # -- PLANE: iso-energy strata from the rim up to the implied top ---------
    pitch = sh.phys(PITCH_PLANE)
    inset = sh.phys(INSET_RIM)
    y = Y_PLANE_TOP
    rows = []
    while y > _y(2.0):
        xl = _rim_cross(y, inset, -1)
        xr = _rim_cross(y, inset, +1)
        if xl is not None and xr is not None:
            a, b = max(x0, xl), min(X_STOP, xr)
            if b - a > sh.phys(1.0):
                rows.append((y, a, b))
        y -= pitch
    rows.reverse()  # bottom -> top, boustrophedon
    for i, (y, a, b) in enumerate(rows):
        L[PLANE].append([(a, y), (b, y)] if i % 2 == 0 else [(b, y), (a, y)])

    # -- RED: the Delta measure (I-beam without serifs: the stops are physics)
    y_glyph = _y(0.5)
    h = sh.phys(max(DELTA_GLYPH_H * sh.k, 4.0))
    brk = h / 2 + sh.phys(BAR_BREAK - DELTA_GLYPH_H / 2)
    red_start = Y_VAC + r_ink + sh.phys(0.5 * NIB[RED] + 0.15)
    L[RED].append([(X_AXIS, red_start), (X_AXIS, y_glyph - brk)])
    L[RED].append([(X_AXIS, y_glyph + brk), (X_AXIS, _y(1.0))])
    L[RED] += delta_glyph(X_AXIS, y_glyph, h, h * 1.07, heavy=2, off=sh.phys(0.4))

    # -- TEXT ------------------------------------------------------------------
    # Tags live in the tag column right of the stop. A black shell's tag is
    # centred on its line's end. The red 0++ does NOT stop: it is the lens's
    # upper edge and runs through the column to the frame, so the silence is
    # enclosed all the way out; its tag perches on it, baseline clear of the
    # curve by 0.6 mm at the tag's right end (the lens stays ink-free).
    # When the physical cap floor makes tags taller than their lines' spacing
    # (small papers) the stack is relaxed upward, order kept, >= 0.5 mm apart.
    tag_cap = sh.cap(TAG_CAP)
    tag_h = tag_cap * (0.6 + 0.6)  # superscript top = 0.6 cap raise + 0.6 cap
    tags = [(parse(f"{j}^{{{pc}}}"), M) for j, pc, M in shells] + [(parse("2Δ"), 2.0)]
    placed = []
    for runs, M in sorted(tags, key=lambda t: t[1]):
        if abs(M - 1.0) < 1e-9:
            xr = X_TAG + _runs_width(runs, tag_cap, 0.08)
            base = _y(math.sqrt(_p(xr) ** 2 + 1.0)) + sh.phys(0.6)
        else:
            base = _y(math.sqrt(_p(X_STOP) ** 2 + M * M)) - tag_cap / 2
            if placed:
                base = max(base, placed[-1][1] + tag_h + sh.phys(0.5))
        placed.append((runs, base))
    for runs, base in placed:
        L[TEXT] += text_runs(runs, X_TAG, base, tag_cap, 0.08)

    # title + statement, flush left on the frame, above the plane.
    # The title is tracked so it spans exactly the plane's width [x0, X_STOP]:
    # its right edge lands on the same vertical as every shell and stratum end.
    t_cap = sh.cap(TITLE_CAP)
    title = "YANG-MILLS  MASS GAP"
    nat = text_width(title, t_cap, 0.0)
    track = (X_STOP - x0 - nat) / (t_cap * (len(title) - 1))
    L[TEXT] += text(title, x0, TITLE_BASE, t_cap, track)
    s_cap = sh.cap(2.5)
    stmt = wrap(
        "THE LIGHT CONE HOLDS ONLY ITS TIP, THE VACUUM.| THEN NOTHING, UP TO Δ.",
        s_cap, 0.18, X_STOP - x0,
    )
    for i, runs in enumerate(stmt):
        L[TEXT] += text_runs(runs, x0, STMT_BASE - i * 2.0 * s_cap, s_cap, 0.18)

    # corner captions below the vacuum (E < 0: the spectral condition's
    # blank), both blocks bottom-aligned on the frame so the vacuum keeps a
    # silence of its own beneath it. Each block may use the half-frame on its
    # side of the axis minus a 10 mm gutter; small papers re-wrap.
    c_cap = sh.cap(1.8)
    lead = c_cap * 2.0
    left_w = X_AXIS - 10.0 - x0
    right_w = x1 - (X_AXIS + 10.0)
    left_par = [
        "PURE SU(3) GAUGE THEORY, NO QUARKS.",
        "HEIGHT IS ENERGY, WIDTH IS MOMENTUM, ONE SCALE.",
        "MASSES: LATTICE, ATHENODOROU-TEPER 2020.",
        "2^{++*} SITS ON 2Δ. STATES ABOVE 2Δ OMITTED.",
    ]
    right_par = ["CLAY PROBLEM: PROVE THE THEORY", "EXISTS ON ℝ^{4} AND Δ > 0.", "OPEN."]
    band_top = Y_VAC - 8.0 - c_cap  # highest caption baseline
    blocks = [
        ([ln for par in left_par for ln in wrap(par, c_cap, 0.12, left_w)], x0, "left"),
        ([ln for par in right_par for ln in wrap(par, c_cap, 0.12, right_w)], x1, "right"),
    ]
    if max(len(b[0]) for b in blocks) - 1 > (band_top - y0) / lead:
        # small paper: the corners cannot hold the text at a 1.8 mm cap, so
        # the captions run as ONE flush-left block under the whole frame
        # (still E < 0, still clear of the vacuum by >= 8 mm)
        # as run-in text: the line breaks of the corner layout are dropped
        run_in = " ".join(left_par + right_par)
        blocks = [(wrap(run_in, c_cap, 0.12, x1 - x0), x0, "left")]
        n = len(blocks[0][0])
        lead = max(c_cap * 1.6, min(lead, (band_top - y0) / max(1, n - 1)))
    for block, xa, al in blocks:
        n = len(block)
        for i, runs in enumerate(block):
            L[TEXT] += text_runs(runs, xa, y0 + (n - 1 - i) * lead, c_cap, 0.12, align=al)
    return L


TITLE_CAP = 8.0
TITLE_BASE = 397.0
STMT_BASE = 385.0
TAG_CAP = 2.2


def yang_mills_mass_gap_faithful(
    rng: SeededRNG, bounds: Bounds, colors: int = 5
) -> List[GCodeCommand]:
    """Millennium plate 4 -- the light cone with its tip cut out (faithful)."""
    del rng  # nothing on this sheet is random: every mark is the data
    sh = Sheet(bounds)
    pens = _pens(colors)
    layers = build(sh)
    out: List[GCodeCommand] = []
    for layer in (GHOST, PLANE, TEXT, SPECTRUM, RED):
        for poly in layers[layer]:
            out += _poly([sh.pt(p) for p in poly], color=pens[layer], f=F_DRAW)
    return out
