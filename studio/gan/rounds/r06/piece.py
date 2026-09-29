"""GAN — THE FIXED POINT REPELS, as a boogie-woogie.  Studio candidate r06 (wildcard).

parent: r04 in name only.  Nothing of r01-r04's composition or code is reused
except the exact Dirac-GAN run (the same h, r0, seed -> a0) and the title.

Contract:  gan_boogie(rng, bounds, colors=4) -> list[GCodeCommand]

WHAT IS COMPUTED (exact)
------------------------
The Dirac-GAN (Mescheder, Geiger, Nowozin 2018).  Real data delta_0, generator
delta_theta, discriminator D_psi(x) = psi*x, V(theta, psi) = f(psi*theta) + f(0),
f(t) = -log(1 + e^-t), f'(s) = sigmoid(-s).  Simultaneous gradient
descent-ascent, both players from the OLD state:

    theta' = theta - h * psi   * f'(s)
    psi'   = psi   + h * theta * f'(s)

The equilibrium theta = psi = 0 exists (Jacobian +-0.5i, a centre).  The flow
(h -> 0) keeps theta^2 + psi^2: it crosses every axis at r0 forever.  The
discrete step multiplies r^2 by 1 + h^2 f'(s)^2 > 1: the run spirals OUT.

When psi*theta > 0 the discriminator is ahead (D spots the fake): f' -> 0 as
|s| grows, both moves shrink, and play CRAWLS.  When psi*theta < 0 the
generator is ahead (G fools D): f' -> 1 and play STRIDES.  Measured on this
run: every quarter-turn G leads takes 7-11 steps; the quarter-turns D leads
take 10, 15, 15, 18, 23, 36, 79, 315 steps.

THE ORDER: ORTHOGONAL SUBDIVISION  (De Stijl, Mondrian's Broadway Boogie Woogie)
---------------------------------------------------------------------------------
No diagonal, no curve.  The run is squared:

  1. THE LANE.  A square spiral of constant width.  Each side sits exactly where
     the run crossed that axis (its crossing radius, measured on the chord), so
     the lane widens its turn by the run's own lap ratio (~1.51).  Before the
     first crossing the lane sits on the flow square (r0).
  2. THE BEATS.  Every step lands on the lane where the ray from the
     equilibrium through that iterate meets it.  The lane is cut into square
     cells; a cell where a step landed is BLUE if D was ahead (psi*theta > 0) or
     RED if G was ahead (psi*theta < 0); a cell the run passed over without a
     step is YELLOW.  Crawl therefore reads as solid blue runs, strides as
     single red beats on yellow.
  3. THE BLACK SQUARE.  The flow's own squared orbit: half-side r0 (every axis
     crossing of the h -> 0 orbit is at r0).  Inside it: bare paper and one
     black + (the Nash equilibrium, exists, repels).
  4. THE WHIRL.  Each lane side is continued by a black rule outward until it
     meets the next lap's lane: the rule is the side's own coordinate, carried
     across the channel, so every white block's depth is the growth of the run
     over one lap on that side.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.models import GCodeCommand
from promptplot.generative.rng import SeededRNG
from promptplot.generative.generators import _poly

Bounds = Tuple[float, float, float, float]
Rect = Tuple[float, float, float, float]

# ---------------------------------------------------------------------------
# An orthogonal alphabet (van Doesburg, 1919): every glyph is horizontal and
# vertical strokes on a 4 x 6 lattice.  One definition serves both the display
# title (lattice points become filled blocks) and the captions (strokes).
# ---------------------------------------------------------------------------

_O = [(0, 0), (0, 6), (4, 6), (4, 0), (0, 0)]
GLYPHS: Dict[str, List[List[Tuple[float, float]]]] = {
    "A": [[(0, 0), (0, 6), (4, 6), (4, 0)], [(0, 3), (4, 3)]],
    "B": [[(0, 0), (0, 6), (3, 6), (3, 3)], [(0, 3), (4, 3), (4, 0), (0, 0)]],
    "C": [[(4, 6), (0, 6), (0, 0), (4, 0)]],
    "D": [[(0, 0), (0, 6), (3, 6), (3, 5), (4, 5), (4, 0), (0, 0)]],
    "E": [[(4, 6), (0, 6), (0, 0), (4, 0)], [(0, 3), (3, 3)]],
    "F": [[(4, 6), (0, 6), (0, 0)], [(0, 3), (3, 3)]],
    "G": [[(4, 6), (0, 6), (0, 0), (4, 0), (4, 3), (2, 3)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "I": [[(1, 6), (3, 6)], [(2, 6), (2, 0)], [(1, 0), (3, 0)]],
    "J": [[(4, 6), (4, 0), (0, 0), (0, 2)]],
    "K": [[(0, 0), (0, 6)], [(0, 3), (2, 3), (2, 5), (4, 5), (4, 6)],
          [(2, 3), (2, 1), (4, 1), (4, 0)]],
    "L": [[(0, 6), (0, 0), (4, 0)]],
    "M": [[(0, 0), (0, 6), (4, 6), (4, 0)], [(2, 6), (2, 3)]],
    "N": [[(0, 0), (0, 6), (2, 6), (2, 0), (4, 0), (4, 6)]],
    "O": [_O],
    "P": [[(0, 0), (0, 6), (4, 6), (4, 3), (0, 3)]],
    "Q": [_O, [(3, 0), (3, -1), (4, -1)]],
    "R": [[(0, 0), (0, 6), (4, 6), (4, 3), (0, 3)], [(2, 3), (2, 1), (4, 1), (4, 0)]],
    "S": [[(4, 6), (0, 6), (0, 3), (4, 3), (4, 0), (0, 0)]],
    "T": [[(0, 6), (4, 6)], [(2, 6), (2, 0)]],
    "U": [[(0, 6), (0, 0), (4, 0), (4, 6)]],
    "V": [[(0, 6), (0, 2), (1, 2), (1, 0), (3, 0), (3, 2), (4, 2), (4, 6)]],
    "W": [[(0, 6), (0, 0), (4, 0), (4, 6)], [(2, 0), (2, 3)]],
    "X": [[(0, 6), (0, 4), (4, 4), (4, 6)], [(0, 0), (0, 2), (4, 2), (4, 0)],
          [(2, 2), (2, 4)]],
    "Y": [[(0, 6), (0, 3), (4, 3), (4, 6)], [(2, 3), (2, 0)]],
    "Z": [[(0, 6), (4, 6), (4, 3), (0, 3), (0, 0), (4, 0)]],
    "0": [_O, [(2, 2), (2, 4)]],
    "1": [[(1, 6), (2, 6), (2, 0)], [(1, 0), (3, 0)]],
    "2": [[(0, 6), (4, 6), (4, 3), (0, 3), (0, 0), (4, 0)]],
    "3": [[(0, 6), (4, 6), (4, 0), (0, 0)], [(1, 3), (4, 3)]],
    "4": [[(0, 6), (0, 3), (4, 3)], [(3, 6), (3, 0)]],
    "5": [[(4, 6), (0, 6), (0, 3), (4, 3), (4, 0), (0, 0)]],
    "6": [[(4, 6), (0, 6), (0, 0), (4, 0), (4, 3), (0, 3)]],
    "7": [[(0, 6), (4, 6), (4, 0)]],
    "8": [_O, [(0, 3), (4, 3)]],
    "9": [[(4, 3), (0, 3), (0, 6), (4, 6), (4, 0), (0, 0)]],
    ".": [[(1.6, 0), (2.4, 0)]],
    ",": [[(2, 0.6), (2, -1)]],
    "·": [[(1.6, 3), (2.4, 3)]],
    ":": [[(1.6, 1), (2.4, 1)], [(1.6, 5), (2.4, 5)]],
    "=": [[(0, 2), (4, 2)], [(0, 4), (4, 4)]],
    "-": [[(1, 3), (3, 3)]],
    "+": [[(0, 3), (4, 3)], [(2, 1), (2, 5)]],
    "(": [[(3, 6), (2, 6), (2, 0), (3, 0)]],
    ")": [[(1, 6), (2, 6), (2, 0), (1, 0)]],
}
ADV = 6.0      # advance in lattice units (glyph 4 wide + 2)
SPACE = 4.0


def text_width(s: str, u: float) -> float:
    w = 0.0
    for ch in s:
        w += SPACE * u if ch == " " else ADV * u
    return w - 2 * u if s and s[-1] != " " else w


def stroke_text(s: str, x: float, y: float, u: float, pen, f: int) -> List[GCodeCommand]:
    """Caption type: the lattice strokes, one pass, cap height 6u."""
    out: List[GCodeCommand] = []
    cx = x
    for ch in s:
        if ch == " ":
            cx += SPACE * u
            continue
        for st in GLYPHS.get(ch, []):
            out += _poly([(cx + gx * u, y + gy * u) for gx, gy in st], color=pen, f=f)
        cx += ADV * u
    return out


def _glyph_cells(ch: str) -> set:
    cells = set()
    for st in GLYPHS.get(ch, []):
        for (ax, ay), (bx, by) in zip(st, st[1:]):
            if ax == bx:
                for j in range(int(min(ay, by)), int(max(ay, by)) + 1):
                    cells.add((int(ax), j))
            else:
                for i in range(int(min(ax, bx)), int(max(ax, bx)) + 1):
                    cells.add((i, int(ay)))
    return cells


def block_text_width(s: str, c: float) -> float:
    # a glyph is 5 blocks wide, advance 6 blocks, space 3 blocks
    w = 0.0
    for ch in s:
        w += 3 * c if ch == " " else 6 * c
    return w - c


def block_text(s: str, x: float, y: float, c: float, pen, f: int,
               pitch: float) -> List[GCodeCommand]:
    """Display type: every lattice point is a c x c block; each glyph is merged
    into maximal rectangles and each rectangle filled as one serpentine."""
    out: List[GCodeCommand] = []
    cx = x
    for ch in s:
        if ch == " ":
            cx += 3 * c
            continue
        cells = _glyph_cells(ch)
        rows: Dict[int, List[Tuple[int, int]]] = {}
        for j in range(7):
            xs = sorted(i for i, jj in cells if jj == j)
            runs = []
            for i in xs:
                if runs and runs[-1][1] == i - 1:
                    runs[-1][1] = i
                else:
                    runs.append([i, i])
            rows[j] = [tuple(r) for r in runs]
        # merge identical runs down the rows into rectangles
        open_: Dict[Tuple[int, int], int] = {}
        rects = []
        for j in range(8):
            cur = set(rows.get(j, []))
            for r in list(open_):
                if r not in cur:
                    rects.append((r[0], open_[r], r[1], j - 1))
                    del open_[r]
            for r in cur:
                if r not in open_:
                    open_[r] = j
        for i0, j0, i1, j1 in rects:
            X0, Y0 = cx + i0 * c, y + j0 * c
            X1, Y1 = cx + (i1 + 1) * c, y + (j1 + 1) * c
            out += serpentine((X0, Y0, X1, Y1), pitch, pen, f, inset=max(0.2, (c - pitch) / 2))
        cx += 6 * c
    return out


# ---------------------------------------------------------------------------
# fills and rules
# ---------------------------------------------------------------------------


def serpentine(r: Rect, pitch: float, pen, f: int, inset: float = 0.25,
               along: Optional[str] = None) -> List[GCodeCommand]:
    """Fill a rectangle with parallel lines along its long side (or `along`),
    one pen-down.  Lines sit `inset` inside the edge (half the tip)."""
    x0, y0, x1, y1 = r
    x0, y0, x1, y1 = x0 + inset, y0 + inset, x1 - inset, y1 - inset
    if x1 - x0 < 0.3 or y1 - y0 < 0.3:
        return []
    horiz = (x1 - x0) >= (y1 - y0) if along is None else along == "x"
    pts = []
    if horiz:
        n = max(1, int(math.floor((y1 - y0) / pitch + 1e-9)))
        step = (y1 - y0) / n
        for k in range(n + 1):
            y = y0 + k * step
            row = [(x0, y), (x1, y)]
            pts += row[::-1] if k % 2 else row
    else:
        n = max(1, int(math.floor((x1 - x0) / pitch + 1e-9)))
        step = (x1 - x0) / n
        for k in range(n + 1):
            x = x0 + k * step
            col = [(x, y0), (x, y1)]
            pts += col[::-1] if k % 2 else col
    return _poly(pts, color=pen, f=f)


def clip_rect(r: Rect, w: Rect) -> Optional[Rect]:
    a = (max(r[0], w[0]), max(r[1], w[1]), min(r[2], w[2]), min(r[3], w[3]))
    if a[2] - a[0] <= 1e-6 or a[3] - a[1] <= 1e-6:
        return None
    return a


def clip_seg(p, q, w: Rect):
    """Axis-aligned segment clipped to window."""
    (ax, ay), (bx, by) = p, q
    if ax == bx:
        if not (w[0] <= ax <= w[2]):
            return None
        lo, hi = max(min(ay, by), w[1]), min(max(ay, by), w[3])
        return ((ax, lo), (ax, hi)) if hi - lo > 0.5 else None
    if not (w[1] <= ay <= w[3]):
        return None
    lo, hi = max(min(ax, bx), w[0]), min(max(ax, bx), w[2])
    return ((lo, ay), (hi, ay)) if hi - lo > 0.5 else None


def rule(p, q, passes: int, sep: float, pen, f: int) -> List[GCodeCommand]:
    """A black rule of `passes` parallel strokes, drawn out and back."""
    (ax, ay), (bx, by) = p, q
    out: List[GCodeCommand] = []
    pts = []
    for k in range(passes):
        o = (k - (passes - 1) / 2) * sep
        if ax == bx:
            seg = [(ax + o, ay), (bx + o, by)]
        else:
            seg = [(ax, ay + o), (bx, by + o)]
        pts += seg[::-1] if k % 2 else seg
    out += _poly(pts, color=pen, f=f)
    return out


# ---------------------------------------------------------------------------
# the mathematics (exact)
# ---------------------------------------------------------------------------


def _sigmoid(t: float) -> float:
    if t >= 0.0:
        return 1.0 / (1.0 + math.exp(-t))
    e = math.exp(t)
    return e / (1.0 + e)


def dirac_gan_run(h: float, r_start: float, a0: float, r_stop: float, max_iters: int):
    th, ps = r_start * math.cos(a0), r_start * math.sin(a0)
    states = [(th, ps)]
    for _ in range(max_iters):
        g = _sigmoid(-(th * ps))
        th, ps = th - h * ps * g, ps + h * th * g
        states.append((th, ps))
        if math.hypot(th, ps) > r_stop:
            break
    return states


def axis_crossings(states):
    """Every chord that changes sign of theta or psi: (step index k of the
    chord z_k -> z_k+1, side E/N/W/S, crossing radius on the chord)."""
    out = []
    for k in range(len(states) - 1):
        (t0, p0), (t1, p1) = states[k], states[k + 1]
        if (p0 >= 0) != (p1 >= 0):
            u = p0 / (p0 - p1)
            x = t0 + u * (t1 - t0)
            out.append((k, "E" if x > 0 else "W", abs(x)))
        if (t0 >= 0) != (t1 >= 0):
            u = t0 / (t0 - t1)
            y = p0 + u * (p1 - p0)
            out.append((k, "N" if y > 0 else "S", abs(y)))
    return out


# ---------------------------------------------------------------------------
# the piece
# ---------------------------------------------------------------------------


def gan_boogie(
    rng: SeededRNG,
    bounds: Bounds,
    colors: int = 4,
    step: float = 0.26,            # h
    r_start: float = 0.74,         # r0: step 0 and the flow square
    scale_mm: float = 38.0,        # mm per world unit
    centre_mm: Tuple[float, float] = (78.0, 141.0),  # the equilibrium, absolute mm
    lane_mm: float = 6.5,          # lane width = beat cell size
    lane_gap: float = 1.0,         # lane inner edge off the crossing line / the black square
    fill_pitch: float = 0.8,       # serpentine pitch (house floor 0.8 mm)
    cell_gap: float = 0.8,         # paper between cells of different colour
    rule_sep: float = 0.45,
    title_block: float = 1.55,
    cap_u: float = 0.38,           # caption lattice unit (cap = 6u)
    gutter: float = 12.0,
    whirl: bool = False,         # r06 v2: the pinwheel rules read as stubs; off
    feed: int = 2200,
    report: Optional[dict] = None,
) -> List[GCodeCommand]:
    x0, y0, x1, y1 = bounds
    # pens, in plot order light -> dark (the colour sequence is sorted by index)
    YEL, RED, BLU, BLK = (0, 1, 2, 3) if colors >= 4 else (0, 1 % colors, 2 % colors, 0)
    s = scale_mm
    w = lane_mm

    # ---- the run -----------------------------------------------------------
    a0 = 0.62 + rng.uniform(-0.55, 0.55)            # seed 7 -> 0.42622 (as r02-r04)
    states = dirac_gan_run(step, r_start, a0, 6.0, 4000)   # the sheet is left long before
    cross = axis_crossings(states)

    # ---- type bands, then the window ----------------------------------------
    title = "THE FIXED POINT REPELS"
    c = (x1 - x0) / block_text_width(title, 1.0)
    title_h = 7 * c
    title_y = y1 - title_h                              # cap-tops on the top margin line
    tag_u = 0.55
    tag = "NEITHER PLAYER EVER ARRIVES"
    tag_y = title_y - 4.0 - 6 * tag_u
    win_top = tag_y - gutter
    cap_lines = 5
    lead = 6 * cap_u + 2.6
    foot_top = y0 + (cap_lines - 1) * lead + 6 * cap_u
    win_bot = foot_top + gutter
    W: Rect = (x0, win_bot, x1, win_top)
    cx, cy = centre_mm

    def P(th, ps):
        return (cx + s * th, cy + s * ps)

    # ---- the squared spiral: side coordinates (mm from the centre) -----------
    # side sequence starts on the flow square's E side (step 0 lies at a0 in Q1)
    g0 = lane_gap
    r0mm = r_start * s
    sides: List[Tuple[str, float, int]] = [("E", r0mm, -1)]   # (side, crossing radius mm, chord k)
    for k, sd, R in cross:
        sides.append((sd, R * s, k))
    # centreline coordinate of each side's lane
    def lane_c(R):
        return R + g0 + w / 2.0

    sign = {"E": (1, 0), "N": (0, 1), "W": (-1, 0), "S": (0, -1)}
    # vertices: corner between side i and side i+1
    verts = []
    for i in range(len(sides) - 1):
        a, b = sides[i], sides[i + 1]
        ca, cb = lane_c(a[1]), lane_c(b[1])
        va, vb = sign[a[0]], sign[b[0]]
        vx = va[0] * ca if va[0] else vb[0] * cb
        vy = va[1] * ca if va[1] else vb[1] * cb
        verts.append((vx, vy))
    # start point: the ray through z_0 on the first (E) side
    t0, p0 = states[0]
    start = (lane_c(r0mm), lane_c(r0mm) * p0 / t0)
    poly = [start] + verts                          # lane centreline, mm relative to centre

    # unwrapped angle of each vertex and of each iterate
    def unwrap(seq):
        out, prev, acc = [], None, 0.0
        for x, y in seq:
            a = math.atan2(y, x)
            if prev is not None:
                d = a - prev
                while d > math.pi:
                    d -= 2 * math.pi
                while d < -math.pi:
                    d += 2 * math.pi
                acc += d
            else:
                acc = a
            out.append(acc)
            prev = a
        return out

    vang = unwrap(poly)
    sang = unwrap(states)

    # land each step on the lane: ray from the centre at the iterate's angle
    landings: List[Tuple[int, int, float]] = []    # (segment index, step k, along-mm)
    seg_i = 0
    for k, A in enumerate(sang):
        while seg_i < len(poly) - 2 and A > vang[seg_i + 1]:
            seg_i += 1
        if A < vang[seg_i] - 1e-9 or A > vang[seg_i + 1] + 1e-9:
            continue
        (ax, ay), (bx, by) = poly[seg_i], poly[seg_i + 1]
        dx, dy = math.cos(A), math.sin(A)
        if ax == bx:          # vertical side x = ax
            y = ax * dy / dx
            along = abs(y - ay)
        else:
            x = ay * dx / dy
            along = abs(x - ax)
        landings.append((seg_i, k, along))

    # ---- cells -------------------------------------------------------------
    # segment i runs poly[i] -> poly[i+1]; its lane rectangle covers the
    # centreline from poly[i] (+w/2, past the previous corner square) to
    # poly[i+1] (+w/2, owning the corner square it arrives at).
    cmds: List[GCodeCommand] = []
    stats = dict(cells=0, yellow=0, red=0, blue=0, steps_landed=0, steps_in_window=0)
    first_exit = None
    in_window_steps = set()
    seg_cells: List[List[dict]] = []
    for i in range(len(poly) - 1):
        (ax, ay), (bx, by) = poly[i], poly[i + 1]
        L = math.hypot(bx - ax, by - ay)
        start_off = 0.0 if i == 0 else w / 2.0
        end_off = L + w / 2.0
        span = end_off - start_off
        n = max(1, int(round(span / w)))
        cl = span / n
        ux, uy = (bx - ax) / L, (by - ay) / L
        cells = []
        for j in range(n):
            s0, s1 = start_off + j * cl, start_off + (j + 1) * cl
            cells.append(dict(s0=s0, s1=s1, steps=[]))
        for si, k, along in landings:
            if si != i:
                continue
            j = min(n - 1, max(0, int((along - start_off) // cl)))
            cells[j]["steps"].append(k)
        for cell in cells:
            ks = cell["steps"]
            if ks:
                nd = sum(1 for k in ks if states[k][0] * states[k][1] > 0)
                cell["col"] = BLU if nd * 2 >= len(ks) and nd > 0 else RED
                if nd * 2 == len(ks):
                    th, ps = states[ks[0]]
                    cell["col"] = BLU if th * ps > 0 else RED
            else:
                cell["col"] = YEL
            for k in ks:
                stats["mixed"] = stats.get("mixed", 0) + (
                    (states[k][0] * states[k][1] > 0) != (cell["col"] == BLU))
            # rectangle in mm
            px0, py0 = ax + ux * cell["s0"], ay + uy * cell["s0"]
            px1, py1 = ax + ux * cell["s1"], ay + uy * cell["s1"]
            if ux == 0:
                rr = (ax - w / 2, min(py0, py1), ax + w / 2, max(py0, py1))
            else:
                rr = (min(px0, px1), ay - w / 2, max(px0, px1), ay + w / 2)
            cell["rect"] = (rr[0] + cx, rr[1] + cy, rr[2] + cx, rr[3] + cy)
            cell["u"] = (ux, uy)
        seg_cells.append(cells)

    # merge consecutive same-colour cells into runs; paper between colours
    lane_rects: List[Tuple[Rect, int]] = []
    for i, cells in enumerate(seg_cells):
        runs = []
        for cell in cells:
            if runs and runs[-1]["col"] == cell["col"]:
                runs[-1]["cells"].append(cell)
            else:
                runs.append(dict(col=cell["col"], cells=[cell]))
        for r in runs:
            rs = [cc["rect"] for cc in r["cells"]]
            rect = (min(q[0] for q in rs), min(q[1] for q in rs),
                    max(q[2] for q in rs), max(q[3] for q in rs))
            ux, uy = r["cells"][0]["u"]
            hg = cell_gap / 2.0
            if ux != 0:
                rect = (rect[0] + hg, rect[1], rect[2] - hg, rect[3])
            else:
                rect = (rect[0], rect[1] + hg, rect[2], rect[3] - hg)
            cr = clip_rect(rect, W)
            if cr is None:
                continue
            along_len = (cr[2] - cr[0]) if ux != 0 else (cr[3] - cr[1])
            if along_len < 2.5:
                continue
            lane_rects.append((cr, r["col"]))
            stats["cells"] += len(r["cells"])
            key = {YEL: "yellow", RED: "red", BLU: "blue"}[r["col"]]
            stats[key] += len(r["cells"])
            for cc in r["cells"]:
                inside = clip_rect(cc["rect"], W)
                for k in cc["steps"]:
                    if inside is not None:
                        in_window_steps.add(k)
                    elif first_exit is None:
                        first_exit = k
            cmds += serpentine(cr, fill_pitch, r["col"], feed,
                               along="x" if ux != 0 else "y")

    # first step whose landing is off the sheet
    landed = sorted(set(k for _, k, _ in landings))
    for k in landed:
        if k not in in_window_steps:
            first_exit = k
            break

    # ---- the whirl: each side's line carried outward to the next lap --------
    # side i's lane (at coordinate c_i) is continued past its end corner, along
    # the same line, until it meets the outer edge region of the lane 4 sides later.
    black: List[GCodeCommand] = []
    for i in range(len(poly) - 1 if whirl else 0):
        (ax, ay), (bx, by) = poly[i], poly[i + 1]
        L = math.hypot(bx - ax, by - ay)
        ux, uy = (bx - ax) / L, (by - ay) / L
        # the side 3 segments later is parallel to the side one lap on (i+4
        # in `sides` terms) - the rule runs from this lane's end corner along
        # u until it reaches the lane of segment i+3 (the next lap's perpendicular side)
        if i + 5 >= len(poly):
            continue
        (qx, qy) = poly[i + 5]
        e = (bx + ux * (w / 2 + 1.0), by + uy * (w / 2 + 1.0))
        if ux != 0:
            end = (qx - ux * (w / 2 + 1.0), by)
        else:
            end = (bx, qy - uy * (w / 2 + 1.0))
        if (end[0] - e[0]) * ux + (end[1] - e[1]) * uy < 1.0:
            continue
        seg = clip_seg((e[0] + cx, e[1] + cy), (end[0] + cx, end[1] + cy), W)
        if seg:
            lap = i // 4
            black += rule(seg[0], seg[1], min(4, 2 + lap // 2), rule_sep, BLK, feed)

    # ---- the flow square and the + ---------------------------------------
    hs = r0mm
    sq = [(cx - hs, cy - hs), (cx + hs, cy - hs), (cx + hs, cy + hs), (cx - hs, cy + hs)]
    for k in range(3):
        o = -(k * rule_sep)          # grows inward: outer edge exactly at r0
        pts = [(cx - hs - o, cy - hs - o), (cx + hs + o, cy - hs - o),
               (cx + hs + o, cy + hs + o), (cx - hs - o, cy + hs + o),
               (cx - hs - o, cy - hs - o)]
        black += _poly(pts, color=BLK, f=feed)
    arm = 4.0
    for k in range(3):
        o = (k - 1) * 0.35
        black += _poly([(cx - arm, cy + o), (cx + arm, cy + o)], color=BLK, f=feed)
        black += _poly([(cx + o, cy - arm), (cx + o, cy + arm)], color=BLK, f=feed)
    lu = 0.36
    l1 = "NASH EQUILIBRIUM"
    l2 = "THETA = PSI = 0"
    black += stroke_text(l1, cx - text_width(l1, lu) / 2, cy + arm + 3.0, lu, BLK, feed)
    black += stroke_text(l2, cx - text_width(l2, lu) / 2, cy - arm - 3.0 - 6 * lu, lu, BLK, feed)

    s0 = "STEP 0"
    sy = cy + start[1] - 3 * lu
    # keep clear of the two equilibrium labels (they sit arm+3 .. arm+3+6lu off the +)
    band = (cy + arm + 3.0 - 6 * lu - 1.5, cy + arm + 3.0 + 6 * lu + 1.5)
    if band[0] < sy < band[1] or band[0] < sy + 6 * lu < band[1]:
        sy = band[1] + 0.5
    black += stroke_text(s0, cx + hs - 2.5 - text_width(s0, lu), sy, lu, BLK, feed)

    # ---- title, tagline --------------------------------------------------
    black += block_text(title, x0, title_y, c, BLK, feed, pitch=0.8)
    black += stroke_text(tag, x0, tag_y, tag_u, BLK, feed)

    # ---- footer ----------------------------------------------------------
    r_exit = math.hypot(*states[first_exit]) if first_exit is not None else float("nan")
    col2 = cx + r0mm                      # right column hangs from the black square's right edge
    sw = 6 * cap_u
    key = [
        ("A STEP, D AHEAD: D SPOTS THE FAKE", BLU),
        ("A STEP, G AHEAD: G FOOLS D", RED),
        ("PASSED OVER WITHOUT A STEP", YEL),
        ("H TO 0: EVERY AXIS AT R 0.74, FOREVER", BLK),
        ("NASH EQUILIBRIUM: IT EXISTS, IT REPELS", "+"),
    ]
    rule_lines = [
        "DIRAC-GAN · SIMULTANEOUS STEPS · H 0.26",
        "AHEAD: D IF PSI·THETA ABOVE 0, ELSE G",
        "A SIDE: WHERE THE RUN CROSSED AN AXIS",
        "A STEP LANDS ON ITS OWN RAY FROM THE +",
        f"STEP {first_exit} R {r_exit:.2f}: FIRST BEAT OFF THE SHEET",
    ]
    for n, (t, col) in enumerate(key):
        yb = y0 + (cap_lines - 1 - n) * lead
        r = (x0, yb, x0 + 2 * sw, yb + sw)
        if col == "+":
            m = x0 + sw
            black += _poly([(m - sw / 2, yb + sw / 2), (m + sw / 2, yb + sw / 2)], color=BLK, f=feed)
            black += _poly([(m, yb), (m, yb + sw)], color=BLK, f=feed)
        elif col == BLK:
            black += rule((x0, yb + sw / 2), (x0 + 2 * sw, yb + sw / 2), 3, rule_sep, BLK, feed)
        else:
            cmds += serpentine(r, fill_pitch, col, feed, along="x")
        black += stroke_text(t, x0 + 2 * sw + 2.5, yb, cap_u, BLK, feed)
    for n, t in enumerate(rule_lines):
        yb = y0 + (cap_lines - 1 - n) * lead
        black += stroke_text(t, col2, yb, cap_u, BLK, feed)
    ann = "MIN G MAX D V(D,G)"
    black += stroke_text(ann, x1 - text_width(ann, tag_u), tag_y, tag_u, BLK, feed)

    if report is not None:
        report.update(stats)
        report.update(dict(
            a0=a0, n_states=len(states), first_exit=first_exit, r_exit=r_exit,
            window=W, centre=(cx, cy), title_block=c, crossings=[(k, sd, R) for k, sd, R in cross],
            n_landed=len(landed), n_in_window=len(in_window_steps),
        ))
    return cmds + black
