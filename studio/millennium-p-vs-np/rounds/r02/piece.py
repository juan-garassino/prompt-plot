"""P VS NP -- r02, thesis ABSTRACT.  Plate 2 of the MILLENNIUM series.

THE NEEDLE IS A RADIUS.  The complete backtracking search of one real 3-SAT
instance (SATLIB uf20-91 / uf20-03.cnf: 20 variables, 91 clauses, exactly one
model), drawn in its exact MEASURE layout: a node (b1..bd) owns the angular
interval [k/2^d, (k+1)/2^d) of one turn, so its arc IS its share of the 2^20
candidate assignments.  Radius is depth (one ring per variable fixed).  With
x1..x20 in order and False first, depth-first preorder runs in increasing
angle: search TIME is ANGLE, a clock hand sweeping clockwise from 12.

Lineage: Manfred Mohr, *Cubic Limit* (1973-75) and the hypercube works from
1977 -- a hypercube read by a rule, every mark a selected edge, the rule IS the
image.  Here the cube is the 20-cube {0,1}^20 and the rule is "halve it at every
ring; draw only what is not yet refuted".

ORDER: RADIAL + NESTED.  Canon: RADIAL DATA-VIZ (5) set on the series' SWISS
sheet (3).  Flat by declaration: equal shares of the haystack are equal only on
an undistorted plane.

Every mark is computed here, at import, by running ``data/search.py``'s own
``load``/``build`` on the CNF (8,047 nodes; the dial draws preorder 1..7,812,
i.e. the search up to and including the model).  Nothing is placed by eye and
the plate uses no randomness.

Design sheet: A3 portrait, mm, y UP, drawable [15,282] x [15,405], uniformly
fitted to ``bounds``.  Hub (148.5, 148.5), R = 128, ring pitch 6.4 mm.

Pens / layers, plotted in index order (light -> dark, red last):
    0 HAIR   black 0.1   one line per depth-8 sub-tree (exact aggregate), rim, 12 hour ticks
    1 BLACK  black 0.3   the search node for node, depths 0..8
    2 TEXT   black 0.3   (same pen, own layer, no swap)
    3 RED    red 0.5     the certificate: its search path + the needle pulled out + 91 clause ticks

Entry point: ``pvsnp_needle_radius``.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.engine.kit import _offset_polyline
from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Pt = Tuple[float, float]
Run = List[Pt]

HERE = Path(__file__).resolve().parent
_SEARCH = HERE.parents[1] / "data" / "search.py"

# ===========================================================================
# the data: run the dossier's own search on the CNF (stdlib, deterministic)
# ===========================================================================
_spec = importlib.util.spec_from_file_location("pvsnp_search", _SEARCH)
_S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_S)

N = 20
CLAUSES = _S.load(_S.CNF)
ALL_NODES = _S.build(CLAUSES)  # preorder [(bits tuple, conflict)]
MODEL = next(p for p, bad in ALL_NODES if len(p) == N and not bad)
MODEL_PRE = [p for p, _ in ALL_NODES].index(MODEL)  # 0-based -> 7811
NODES = ALL_NODES[: MODEL_PRE + 1]  # [A]: the search up to the needle
CONFLICT = {p: bad for p, bad in NODES}
ON_PATH = {MODEL[:d] for d in range(N + 1)}


def k_of(p: Sequence[bool]) -> int:
    return int("".join("1" if b else "0" for b in p), 2) if p else 0


def theta(p: Sequence[bool]) -> float:
    """Node centre angle, degrees, 0 at 12 o'clock, clockwise."""
    return 360.0 * (k_of(p) + 0.5) / 2 ** len(p)


def children(p) -> List[tuple]:
    return [c for c in (p + (False,), p + (True,)) if c in CONFLICT]


# ===========================================================================
# the design sheet (A3 portrait, mm, y up) -- encoding 5A
# ===========================================================================
SHEET = (15.0, 15.0, 282.0, 405.0)
HX, HY = 148.5, 148.5
R = 128.0
PITCH = R / N  # 6.4 mm per variable
EXACT_D = 8  # node-for-node to depth 8 (sibling spokes >= 1.178 mm at r = 7.5 p)
TICK_R = (129.5, 133.5)  # hour ticks
NEEDLE_R = 257.0  # the needle pulled out
CHK_R0, CHK_PITCH = 134.0, 1.35  # 91 clause ticks
TICK_LEN = {1: 1.5, 2: 2.75, 3: 4.0}
ARC_STEP = 0.25  # mm, arc chord


def pol(r: float, th: float) -> Pt:
    a = math.radians(th)
    return (HX + r * math.sin(a), HY + r * math.cos(a))


def arc(r: float, t0: float, t1: float) -> Run:
    if r <= 0 or abs(t1 - t0) < 1e-12:
        return [pol(r, t0)]
    n = max(1, int(math.ceil(abs(math.radians(t1 - t0)) * r / ARC_STEP)))
    return [pol(r, t0 + (t1 - t0) * i / n) for i in range(n + 1)]


class Fit:
    def __init__(self, bounds):
        bx0, by0, bx1, by1 = bounds
        w, h = SHEET[2] - SHEET[0], SHEET[3] - SHEET[1]
        self.k = min((bx1 - bx0) / w, (by1 - by0) / h)
        self.ox = bx0 + ((bx1 - bx0) - w * self.k) / 2.0 - SHEET[0] * self.k
        self.oy = by0 + ((by1 - by0) - h * self.k) / 2.0 - SHEET[1] * self.k

    def run(self, r: Sequence[Pt]) -> Run:
        return [(self.ox + x * self.k, self.oy + y * self.k) for x, y in r]


def length(r: Sequence[Pt]) -> float:
    return sum(math.dist(r[i], r[i + 1]) for i in range(len(r) - 1))


# ===========================================================================
# the tree as edge pieces: STEM (radial stub, half a pitch past the ring),
# FORK (arc at r_d + p/2 from the parent's angle to the child's), BRANCH
# (the child's spoke out to its ring).  Pieces are emitted in DFS order and
# chained into pen-down polylines wherever one ends where the next begins.
# ===========================================================================
def pieces(max_d: int):
    """Yield (tag, run) in preorder for every edge from depth d to d+1, d < max_d.
    tag 'red' for the certificate's own edges (substituted, never double-inked)."""
    out: List[Tuple[str, Run]] = []

    def rec(p):
        d = len(p)
        if d >= max_d or CONFLICT[p]:
            return
        kids = children(p)
        if not kids:
            return
        r0, rf, r1 = d * PITCH, (d + 0.5) * PITCH, (d + 1) * PITCH
        tp = theta(p)
        out.append(("red" if p in ON_PATH else "black", [pol(r0, tp), pol(rf, tp)]))
        for c in kids:
            tc = theta(c)
            run = arc(rf, tp, tc) + [pol(r1, tc)]
            out.append(("red" if c in ON_PATH else "black", run))
            rec(c)

    rec(())
    return out


def chain(pcs: List[Tuple[str, Run]], tag: str) -> List[Run]:
    runs: List[Run] = []
    for t, r in pcs:
        if t != tag:
            continue
        if runs and math.dist(runs[-1][-1], r[0]) < 1e-9:
            runs[-1] += r[1:]
        else:
            runs.append(list(r))
    return [r for r in runs if length(r) > 1e-6]


# ===========================================================================
# type: the house stroke font, 4 x 6 cell; '?' and the em dash authored
# ===========================================================================
_EXTRA = {
    "?": [[(0.2, 4.7), (0.8, 5.7), (2.0, 6.0), (3.2, 5.7), (3.8, 4.8), (3.6, 3.9),
           (2.7, 3.2), (2.0, 2.6), (2.0, 1.7)],
          [(1.7, 0), (2.3, 0), (2.3, 0.5), (1.7, 0.5), (1.7, 0)]],
    "—": [[(0.0, 3.0), (5.6, 3.0)]],
}
ADV = 5.6


def set_text(txt: str, x: float, y: float, cap: float, track: float = 0.0) -> Tuple[List[Run], float]:
    runs: List[Run] = []
    sc = cap / 6.0
    cx = x
    for ch in txt:
        strokes = _EXTRA.get(ch) or _GLYPHS.get(ch) or _GLYPHS.get(ch.upper()) or []
        for st in strokes:
            runs.append([(cx + gx * sc, y + gy * sc) for gx, gy in st])
        cx += ADV * sc + track
    return runs, (cx - x - track) if txt else 0.0


def ink_width(txt: str, cap: float, track: float = 0.0) -> float:
    """Advance width minus the trailing side-bearing of a 4-cell glyph."""
    return set_text(txt, 0.0, 0.0, cap, track)[1] - (ADV - 4.0) * cap / 6.0


def wrap(txt: str, cap: float, track: float, maxw: float) -> List[str]:
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if ink_width(t, cap, track) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def split_corners(r: Run, max_turn: float = 50.0) -> List[Run]:
    out, cur = [], [r[0]]
    for i in range(1, len(r) - 1):
        cur.append(r[i])
        a = math.atan2(r[i][1] - r[i - 1][1], r[i][0] - r[i - 1][0])
        b = math.atan2(r[i + 1][1] - r[i][1], r[i + 1][0] - r[i][0])
        if abs((math.degrees(b - a) + 180.0) % 360.0 - 180.0) > max_turn:
            out.append(cur)
            cur = [r[i]]
    cur.append(r[-1])
    out.append(cur)
    return out


# ===========================================================================
# pens
# ===========================================================================
LAYERS = ("hair", "black", "text", "red")


def _pen_map(colors: int) -> Dict[str, Optional[int]]:
    if colors >= 4:
        return {"hair": 0, "black": 1, "text": 2, "red": 3}
    if colors == 3:
        return {"hair": 0, "black": 1, "text": 1, "red": 2}
    if colors == 2:
        return {"hair": 0, "black": 0, "text": 0, "red": 1}
    return {k: None for k in LAYERS}


# ===========================================================================
# the plate
# ===========================================================================
REPORT: Dict[str, object] = {}


def clause_tests(nodes) -> int:
    by_max: Dict[int, int] = {}
    for c in CLAUSES:
        m = max(abs(l) for l in c)
        by_max[m] = by_max.get(m, 0) + 1
    return sum(by_max.get(len(p), 0) for p, _ in nodes if p)


def subtree_depth() -> Dict[tuple, int]:
    """Deepest depth reached below every depth-EXACT_D node (drawn nodes only)."""
    deep: Dict[tuple, int] = {}
    for p, _ in NODES:
        if len(p) >= EXACT_D:
            a = p[:EXACT_D]
            deep[a] = max(deep.get(a, EXACT_D), len(p))
    return deep


def build_layers() -> Dict[str, List[Run]]:
    L: Dict[str, List[Run]] = {k: [] for k in LAYERS}

    # ---- BLACK: exact, node for node, depths 0..8 ---------------------------
    pcs = pieces(EXACT_D)
    L["black"] = chain(pcs, "black")

    # ---- HAIR: one line per depth-8 sub-tree, ring 8 -> its deepest ring ---
    deep = subtree_depth()
    agg = []
    for a, dmax in deep.items():
        if a in ON_PATH or CONFLICT[a] or dmax == EXACT_D:
            continue
        agg.append((theta(a), dmax))
    agg.sort()
    REPORT["aggregate_lines"] = len(agg)
    REPORT["rim_contacts_black"] = [round(t, 1) for t, d in agg if d == N]
    hair_items: List[Tuple[float, Run]] = []
    for t, dmax in agg:
        hair_items.append((t, [pol(EXACT_D * PITCH, t), pol(dmax * PITCH, t)]))
    for h in range(12):  # hour ticks: 1/12 of the sweep each
        hair_items.append((h * 30.0 - 1e-6, [pol(TICK_R[0], h * 30.0), pol(TICK_R[1], h * 30.0)]))
    # clockwise from 12; radial lines boustrophedon so consecutive strokes are close
    hair_items.sort(key=lambda it: it[0])
    hair = []
    for i, (_, r) in enumerate(hair_items):
        hair.append(r if i % 2 == 0 else r[::-1])
    for q in range(4):  # the rim, ring 20: 4 quadrant arcs, last
        hair.append(arc(R, q * 90.0, (q + 1) * 90.0))
    L["hair"] = hair

    # ---- RED: the certificate's own search path, then the needle -----------
    all_pcs = pieces(N)
    red_path: Run = []
    for t, r in all_pcs:
        if t == "red":
            red_path = red_path + (r[1:] if red_path else r)
    t20 = theta(MODEL)
    red_path += [pol(NEEDLE_R, t20)]
    REPORT["red_rim_angle"] = t20
    REPORT["red_tip"] = pol(NEEDLE_R, t20)
    red = [red_path]

    # the 91 clause checks along the needle, grouped by closing variable
    order = sorted(range(len(CLAUSES)), key=lambda i: (max(abs(l) for l in CLAUSES[i]), i))
    groups = sorted({max(abs(l) for l in c) for c in CLAUSES})
    a = math.radians(t20)
    u = (math.sin(a), math.cos(a))  # along the needle
    nrm = (-u[1], u[0])  # left normal
    ntrue = []
    ticks: List[Run] = []
    for j, i in enumerate(order):
        c = CLAUSES[i]
        nt = sum(1 for l in c if MODEL[abs(l) - 1] == (l > 0))
        assert nt >= 1  # the certificate satisfies every clause
        ntrue.append(nt)
        g = groups.index(max(abs(l) for l in c))
        side = 1.0 if g % 2 == 0 else -1.0
        r = CHK_R0 + CHK_PITCH * (j + 0.5)
        base = pol(r, t20)
        tip = (base[0] + side * nrm[0] * TICK_LEN[nt], base[1] + side * nrm[1] * TICK_LEN[nt])
        ticks.append([base, tip] if j % 2 == 0 else [tip, base])
    red += ticks
    REPORT["ticks"] = len(ticks)
    REPORT["tick_hist"] = {k: ntrue.count(k) for k in (1, 2, 3)}
    REPORT["groups"] = len(groups)
    L["red"] = red

    REPORT["clause_tests_to_model"] = clause_tests(NODES)
    REPORT["clause_tests_all"] = clause_tests(ALL_NODES)
    REPORT["depth6_conflicts"] = [round(theta(p), 1) for p, b in NODES if b and len(p) == 6]

    # ---- TEXT --------------------------------------------------------------
    L["text"] = build_text()
    return L


def _heavy(runs: List[Run], offs=(-0.36, -0.18, 0.0, 0.18, 0.36)) -> List[Run]:
    out = []
    for r in (q for r0 in runs for q in split_corners(r0)):
        ch: Run = []
        for j, d in enumerate(offs):
            q = _offset_polyline(r, d) if d else list(r)
            ch += q if j % 2 == 0 else q[::-1]
        out.append(ch)
    return out


def build_text() -> List[Run]:
    T: List[Run] = []
    X_L = SHEET[0]
    COL_R = 88.0  # left column right edge, >= 10 mm clear of the red

    # title: display weight (5 chained passes of the 0.3 nib), tracking solved
    # so the ink ends on COL_R
    cap_t, ttl = 10.0, "P VS NP"
    w0 = ink_width(ttl, cap_t)
    tr_t = ((COL_R - 0.36) - (X_L + 0.36) - w0) / (len(ttl) - 1)
    T += _heavy(set_text(ttl, X_L + 0.36, 390.0, cap_t, tr_t)[0])

    cap_s, tr_s = 2.5, 0.3
    for i, ln in enumerate(["IF AN ANSWER IS EASY", "TO CHECK, IS IT EASY", "TO FIND?"]):
        assert X_L + ink_width(ln, cap_s, tr_s) <= COL_R
        T += set_text(ln, X_L, 372.0 - i * 4.4, cap_s, tr_s)[0]

    cap_c, tr_c, lead = 1.8, 0.18, 3.2

    def block(txt_lines, x, y_bottom, maxw, right=False):
        """Wrapped caption whose LAST baseline sits on ``y_bottom``."""
        nonlocal T
        n = sum(len(wrap(para, cap_c, tr_c, maxw)) for para in txt_lines)
        y = y_bottom + (n - 1) * lead
        for para in txt_lines:
            for ln in wrap(para, cap_c, tr_c, maxw):
                w = ink_width(ln, cap_c, tr_c)
                x0 = x - w if right else x
                T += set_text(ln, x0, y, cap_c, tr_c)[0]
                y -= lead
        return y

    # data block on the 3.2 mm caption grid; its LAST baseline sits on the top
    # end of the 12 o'clock hour tick (y = HY + 133.5 = 282): the column and
    # the dial's time scale share one horizontal
    data = ["SATLIB UF20-03 · 20 VARIABLES,",
            "91 CLAUSES, M/N = 4.55.",
            "1,048,576 CANDIDATES. ONE FITS ALL 91.",
            "",
            "BLACK: EVERY NODE OF THE SEARCH TO X8.",
            "HAIRLINE: EACH X8 SUB-TREE AS ONE LINE,",
            "AS DEEP AS ITS DEEPEST NODE.",
            "A LINE THAT STOPS IS A REFUTATION."]
    y_last = HY + TICK_R[1]
    for i, ln in enumerate(data):
        assert X_L + ink_width(ln, cap_c, tr_c) <= COL_R, ln
        T += set_text(ln, X_L, y_last + (len(data) - 1 - i) * lead, cap_c, tr_c)[0]

    # the checking caption, right of the needle's tip
    cap_k, tr_k = 2.0, 0.2
    T += set_text("CHECKING: THE NEEDLE PULLED OUT — 91 CLAUSES, 273 LOOKUPS.",
                  110.0, 398.0, cap_k, tr_k)[0]
    cert = " ".join(str(i + 1) if b else "−" + str(i + 1) for i, b in enumerate(MODEL))
    T += set_text(cert, 110.0, 393.6, cap_k, tr_k)[0]
    T += set_text("TICK LENGTH: LITERALS MADE TRUE, 1 2 3 · SIDE: CLOSING VARIABLE.",
                  110.0, 389.6, cap_c, tr_c)[0]

    tests = REPORT.get("clause_tests_to_model", 0)
    # the two spandrel captions stand on the bottom margin (y = 15), the line the
    # 6 o'clock hour tick ends on: dial and type share the sheet's edges
    block([f"FINDING: BACKTRACKING X1..X20, FALSE FIRST, CLOCKWISE FROM 12. "
           f"{MODEL_PRE + 1:,} NODES, {tests:,} CLAUSE TESTS. FOUND AT 11:37."],
          X_L, SHEET[1], 62.0 - X_L)
    block(["THIS SEARCH, NOT THE PROBLEM: UNIT PROPAGATION FINDS THE SAME NEEDLE "
           "IN 87 NODES. A SHORTCUT FOR EVERY CASE? OPEN."],
          SHEET[2], SHEET[1], SHEET[2] - 235.0, right=True)
    return T


def pvsnp_needle_radius(rng: SeededRNG, bounds, colors: int = 4) -> List[GCodeCommand]:
    """The whole search of uf20-03 as a dial; the needle is one red radius.

    Deterministic: every mark is exact data; ``rng`` is accepted for the
    contract and deliberately unused.
    """
    _ = rng
    fit = Fit(bounds)
    L = build_layers()
    pens = _pen_map(colors)
    out: List[GCodeCommand] = []
    for layer in LAYERS:
        f = 1500 if layer == "red" else 2000
        for r in L[layer]:
            out += _poly(fit.run(r), color=pens[layer], f=f)
    return out


if __name__ == "__main__":
    L = build_layers()
    for k, v in L.items():
        print(k, len(v), "strokes", round(sum(length(r) for r in v) / 1000, 3), "m")
    for k, v in REPORT.items():
        print(k, v)
