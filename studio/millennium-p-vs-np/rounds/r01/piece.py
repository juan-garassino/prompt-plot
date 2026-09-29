"""P VS NP — Millennium plate 2, r01 (thesis: FAITHFUL).

An illustrator's reconstruction of ``studio/millennium-p-vs-np/ref/reference.png`` (a 1024x1536
AI poster), its architecture MEASURED and its lies corrected (encoding.md §5F).  The reference's
START -> SOLUTION search tree is replaced by the REAL one: chronological backtracking on SATLIB
``uf20-03.cnf`` (20 variables, 91 clauses), x1..x20 in order, False first -- 8,047 nodes,
4,023 conflict leaves, exactly one model.  Every mark in the field is one of those nodes or an
exact aggregate of them; the one red thread is the certificate's own search path; the red comb at
the foot is its verification, 91 clause checks.

Reference measurements (px on the 1024x1536 raster; u = x/1024, v = y/1536 from the TOP):
    title "P vs NP"              x  39..295  y   33..  90   u .038-.288  v .021-.059
    short rule under title       x  36.. 84  y  112         v .073
    statement, 4 lines caps      x  36..299  y  138.. 222   v .090-.145
    P = {...} / NP = {...}       x  34..309  y  268.. 402   v .174-.262
    italic quote, top right      x 767..990  y   43.. 162   u .749-.967
    Hamiltonian inset (box)      x 804..998  y  228.. 419   caption y 439..499
    START label                  x 478..545  y   21..  34   u .467-.532  (centred on the sheet)
    red thread x at v .04/.20/.46/.51/.66/.77/.86  -> 507 / 586 / 461 / 609 / 448 / 512 / 512 px
                                 (wanders about the centre, u .44-.60, ends at u .50)
    SOLUTION label               x 458..569  y 1380..1393   u .447-.556  v .898-.907
    FINDING box (toy tree)       x  35..291  y 1201..1414
    CHECKING box (5 nodes, arrow) x 735..989 y 1201..1414
    tagline                      x 326..712  y 1460..1469   "SAME PROBLEM. DIFFERENT WORLDS?"
    ink by band: the tree fills u .03-.97, v .02-.92, uniform and bushy to the bottom.

Layout fixes against the reference (every one listed in NOTES.md):
    1. the tree never merges: stem / fork bar / drop on the exact measure x = 15 + 267 m
    2. no node marks, no blue waypoints, no START/SOLUTION circles: a line that stops is a conflict
    3. the red thread is where the data puts it: x = 273.57 mm, 96.84 % of the width
    4. the bushy uniform fan becomes the real carving: complete to row 5, pruned from row 6
    5. the Hamiltonian inset + FINDING toy tree -> the Petersen NO search, complete, zero red
    6. the 5-node CHECKING chain with an arrow -> 91 red ticks, one per clause, no arrow
    7. boxes, quote block and tagline cut; defs set in a right column on the title's grid

Pens (``colors=4``), layer order light -> dark, red last (2 physical swaps):
    0  HAIR   black 0.1   the search below row 7, one line per depth-7 sub-tree (exact aggregate)
    1  BLACK  black 0.3   the search rows 0-7 node for node + the Petersen NO tree
    2  TEXT   black 0.3   (same pen as BLACK, own layer, no swap) all type
    3  RED    red 0.5     the certificate: its search path (root -> row 20) and its 91 checks

Lineage: Manfred Mohr, *Cubic Limit* (1973-75) and the hypercube works from 1977 -- a hypercube
read by a rule, every mark a selected edge.  Here: the 20-cube of assignments, halved at every
row, drawn only where not yet refuted.

Entry point: ``p_vs_np_faithful``.
"""

from __future__ import annotations

import collections
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from promptplot.generative.generators import _GLYPHS, _poly
from promptplot.generative.rng import SeededRNG
from promptplot.models import GCodeCommand

Bounds = Tuple[float, float, float, float]
Pt = Tuple[float, float]
Poly = List[Pt]

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "data"

HAIR, BLACK, TEXT, RED = 0, 1, 2, 3
F_DRAW = 2200

# ===========================================================================
# the one mapping (encoding §4 / §5F) -- sheet mm, y UP from the bottom edge, A3 portrait
# ===========================================================================
SHEET_W, SHEET_H = 297.0, 420.0
X_L, X_R = 15.0, 282.0
FIELD_W = X_R - X_L          # 267: x = 15 + 267 m, m = (k + 1/2) / 2^d
Y_ROOT, ROW = 350.0, 12.5    # y_d = 350 - 12.5 d; row 20 at y = 100
N_VARS = 20
EXACT_DEPTH = 7              # 0.3 node for node to row 7, 0.1 aggregate below (2.086 mm floor)


def x_of(k: int, d: int) -> float:
    return X_L + FIELD_W * (k + 0.5) / 2 ** d


def y_of(d: int) -> float:
    return Y_ROOT - ROW * d


# ===========================================================================
# data -- the real search (data/search.py --json, written into this round)
# ===========================================================================
@lru_cache(maxsize=1)
def tree() -> Dict[str, object]:
    path = HERE / "tree.json"
    if path.exists():
        raw = json.loads(path.read_text())
        nodes = [(n["bits"], n["conflict"]) for n in raw["nodes_preorder"]]
        model_k = raw["model"]
    else:  # recompute from the CNF with the dossier's own script (deterministic, stdlib)
        import importlib.util
        spec = importlib.util.spec_from_file_location("pnp_search", DATA / "search.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        built = mod.build(mod.load(DATA / "uf20-03.cnf"))
        nodes = [("".join("1" if b else "0" for b in p), bad) for p, bad in built]
        model_k = next(int(b, 2) for b, bad in nodes if len(b) == N_VARS and not bad)
    conflict = {b: bad for b, bad in nodes}
    model = format(model_k, "020b")
    return {"nodes": nodes, "conflict": conflict, "model": model}


def children(bits: str) -> List[str]:
    """Generated children in False-first order (both are generated for a live node)."""
    c = tree()["conflict"]
    return [bits + v for v in "01" if bits + v in c]


@lru_cache(maxsize=1)
def deepest_below() -> Dict[str, int]:
    """For every depth-7 node: the depth of the deepest node in its sub-tree (exact aggregate)."""
    deep: Dict[str, int] = collections.defaultdict(int)
    for b, _ in tree()["nodes"]:
        if len(b) >= EXACT_DEPTH:
            s = b[:EXACT_DEPTH]
            deep[s] = max(deep[s], len(b))
    return dict(deep)


@lru_cache(maxsize=1)
def clauses() -> List[List[int]]:
    out = []
    for line in (DATA / "uf20-03.cnf").read_text().splitlines():
        s = line.split()
        if not s or s[0] in ("c", "p"):
            continue
        if s[0] == "%":
            break
        lits = [int(x) for x in s if x != "0"]
        if lits:
            out.append(lits)
    return out


# ===========================================================================
# the search tree: stem / fork bar / drop (encoding §4 "edge geometry")
# ===========================================================================
class Chain:
    """Collect segments in DFS order; a segment that starts where the last one ended extends the
    current pen-down run, anything else starts a new one (so the tree plots as long DFS strokes)."""

    def __init__(self) -> None:
        self.runs: List[Poly] = []

    def seg(self, a: Pt, b: Pt) -> None:
        if abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9:
            return
        if self.runs and math.dist(self.runs[-1][-1], a) < 1e-6:
            last = self.runs[-1]
            # collinear continuation: replace the end point instead of adding a vertex
            if len(last) >= 2:
                p, q = last[-2], last[-1]
                if abs((q[0] - p[0]) * (b[1] - q[1]) - (q[1] - p[1]) * (b[0] - q[0])) < 1e-9 and \
                        (q[0] - p[0]) * (b[0] - q[0]) + (q[1] - p[1]) * (b[1] - q[1]) > 0:
                    last[-1] = b
                    return
            last.append(b)
        else:
            self.runs.append([a, b])


def build_search():
    """Black (rows 0-7, node for node), hairline (one line per depth-7 sub-tree) and red (the
    certificate's own path, root -> row 20, exact at every depth)."""
    model = tree()["model"]
    black, red = Chain(), Chain()
    stats = {"row6_ends": [], "black_segments": 0}

    def on_path(bits: str) -> bool:
        return model.startswith(bits)

    def visit(bits: str) -> None:
        d = len(bits)
        k = int(bits, 2) if bits else 0
        xp, yp = x_of(k, d), y_of(d)
        kids = children(bits) if (d < EXACT_DEPTH and not tree()["conflict"][bits]) else []
        if not kids:
            if tree()["conflict"][bits]:
                stats["row6_ends"].append((d, xp))
            return
        yb = yp - ROW / 2
        (red if on_path(bits) else black).seg((xp, yp), (xp, yb))          # stem
        for c in kids:
            xc = x_of(int(c, 2), d + 1)
            ch = red if on_path(c) else black
            ch.seg((xp, yb), (xc, yb))                                       # fork (half bar)
            ch.seg((xc, yb), (xc, y_of(d + 1)))                               # drop
            visit(c)

    visit("")
    # below row 7 the red keeps its exact geometry (stem, half-bar, drop at every depth)
    for d in range(EXACT_DEPTH, N_VARS):
        p, c = model[:d], model[:d + 1]
        xp, xc = x_of(int(p, 2), d), x_of(int(c, 2), d + 1)
        yb = y_of(d) - ROW / 2
        red.seg((xp, y_of(d)), (xp, yb))
        red.seg((xp, yb), (xc, yb))
        red.seg((xc, yb), (xc, y_of(d + 1)))

    hair: List[Poly] = []
    reach20 = []
    for s, dmax in sorted(deepest_below().items(), key=lambda kv: int(kv[0], 2)):
        x = x_of(int(s, 2), EXACT_DEPTH)
        if dmax == N_VARS:
            reach20.append(x)
        if on_path(s):
            continue                     # the red substitutes for sector 123's aggregate
        hair.append([(x, y_of(EXACT_DEPTH)), (x, y_of(dmax))])
    stats["reach20_x"] = reach20
    return black.runs, hair, red.runs, stats


# ===========================================================================
# the NO companion: the Petersen graph's complete Hamiltonian search (dossier §2c)
# ===========================================================================
def petersen() -> Dict[int, List[int]]:
    """Same construction as data/hamilton.py: outer 5-cycle, inner pentagram, 5 spokes."""
    adj: Dict[int, set] = {i: set() for i in range(10)}
    for i in range(5):
        for a, b in [(i, (i + 1) % 5), (5 + i, 5 + (i + 2) % 5), (i, 5 + i)]:
            adj[a].add(b)
            adj[b].add(a)
    return {k: sorted(v) for k, v in adj.items()}


def petersen_tree():
    """Every simple path from vertex 0, as a nested tree. Returns (root, counts)."""
    g = petersen()
    counts = collections.Counter()

    def rec(path: List[int]):
        counts["nodes"] += 1
        kids = [w for w in g[path[-1]] if w not in path]
        if len(path) == len(g):
            counts["ham_paths"] += 1
            counts["closing"] += path[0] in g[path[-1]]
        elif not kids:
            counts["dead"] += 1
        return {"depth": len(path) - 1, "kids": [rec(path + [w]) for w in kids]}

    root = rec([0])
    return root, dict(counts)


PET_X0, PET_PITCH = 15.0, 1.1        # 72 leaves at 1.1 mm (0.3 nib: 0.8 mm clear)
PET_Y0, PET_ROW = 85.0, 5.0          # depth 0 at y 85, depth 9 at y 40


def build_petersen():
    root, counts = petersen_tree()
    leaf_i = [0]

    def place(n):                     # leaf-order tidy layout (makes NO measure claim)
        if not n["kids"]:
            n["x"] = PET_X0 + PET_PITCH * leaf_i[0]
            leaf_i[0] += 1
        else:
            for c in n["kids"]:
                place(c)
            n["x"] = (n["kids"][0]["x"] + n["kids"][-1]["x"]) / 2
    place(root)
    ch = Chain()

    def draw(n):
        if not n["kids"]:
            return
        y = PET_Y0 - PET_ROW * n["depth"]
        yb = y - PET_ROW / 2
        ch.seg((n["x"], y), (n["x"], yb))
        kids = n["kids"]
        for i, c in enumerate(kids):
            if i == 0 or i == len(kids) - 1:
                ch.seg((n["x"], yb), (c["x"], yb))
            ch.seg((c["x"], yb), (c["x"], y - PET_ROW))
            draw(c)
    draw(root)
    counts["leaves"] = leaf_i[0]
    return ch.runs, counts


# ===========================================================================
# the verification: 91 red ticks, one per clause (encoding §4 "91 red ticks")
# ===========================================================================
CHAIN_Y = 62.0
TICK_PITCH = 1.35
TICK_LEN = {1: 1.5, 2: 2.75, 3: 4.0}


def build_check(x_left: float, x_right: float):
    model = tree()["model"]
    val = {i + 1: model[i] == "1" for i in range(N_VARS)}
    cl = clauses()
    order = sorted(range(len(cl)), key=lambda i: (max(abs(l) for l in cl[i]), i))
    n = len(order)
    pitch = (x_right - x_left) / n     # the chain spans the START axis -> the SOLUTION axis
    ticks: List[Poly] = []
    groups = []
    hist = collections.Counter()
    for j, i in enumerate(order):
        c = cl[i]
        ntrue = sum(1 for l in c if val[abs(l)] == (l > 0))
        assert ntrue >= 1, "the certificate must satisfy every clause"
        hist[ntrue] += 1
        g = max(abs(l) for l in c)
        if not groups or groups[-1] != g:
            groups.append(g)
        side = 1 if len(groups) % 2 == 1 else -1
        x = x_left + pitch * (j + 0.5)
        L = TICK_LEN[ntrue]
        ticks.append([(x, CHAIN_Y), (x, CHAIN_Y + side * L)])
    rule = [(x_left, CHAIN_Y), (x_right, CHAIN_Y)]
    return rule, ticks, {"n": n, "hist": dict(hist), "groups": groups, "x_left": x_left,
                         "pitch": pitch}


# ===========================================================================
# type -- the house stroke font plus the few glyphs this plate needs (authored here)
# ===========================================================================
GLYPHS = dict(_GLYPHS)
GLYPHS.update({
    "?": [[(0.6, 4.7), (1.3, 5.6), (2.5, 5.9), (3.4, 5.2), (3.4, 4.1), (2.0, 3.0), (2.0, 1.7)],
          [(1.8, 0.1), (2.2, 0.1)]],
    "–": [[(0.4, 3), (3.6, 3)]],
    "—": [[(0.0, 3), (4.0, 3)]],
    # sans I: one pen-down instead of three (the text layer is priced in pen cycles)
    "I": [[(2.0, 6.0), (2.0, 0.0)]],
    "·": [[(1.7, 2.6), (2.3, 2.6), (2.3, 3.1), (1.7, 3.1), (1.7, 2.6)]],
})


def _adv(ch: str) -> float:
    if ch == " ":
        return 2.6
    st = GLYPHS.get(ch) or GLYPHS.get(ch.upper()) or []
    xs = [p[0] for s in st for p in s]
    if not xs:
        return 2.6
    sb = 0.55 if ch.islower() else 1.02
    return (max(xs) - min(xs)) + 2.0 * sb


def text_width(txt: str, h: float, track: float = 0.0) -> float:
    return sum(_adv(c) for c in txt) * h / 6.0 + track * max(0, len(txt) - 1)


def chain(runs: List[Poly], tol: float = 0.02) -> List[Poly]:
    runs = [list(r) for r in runs]
    out: List[Poly] = []
    while runs:
        cur = runs.pop(0)
        grown = True
        while grown:
            grown = False
            for i, r in enumerate(runs):
                if math.dist(cur[-1], r[0]) < tol:
                    cur += r[1:]
                elif math.dist(cur[-1], r[-1]) < tol:
                    cur += r[::-1][1:]
                elif math.dist(cur[0], r[-1]) < tol:
                    cur = r + cur[1:]
                elif math.dist(cur[0], r[0]) < tol:
                    cur = r[::-1] + cur[1:]
                else:
                    continue
                runs.pop(i)
                grown = True
                break
        out.append(cur)
    return out


def set_text(txt: str, x: float, y: float, h: float, track: float = 0.0) -> List[Poly]:
    sc = h / 6.0
    runs: List[Poly] = []
    cx = x
    for ch in txt:
        st = GLYPHS.get(ch)
        if st is None:
            st = GLYPHS.get(ch.upper(), [])
        xs = [p[0] for s in st for p in s]
        x_off = -min(xs) + (0.55 if ch.islower() else 1.02) if xs else 0.0
        runs += chain([[(cx + (gx + x_off) * sc, y + gy * sc) for gx, gy in s] for s in st])
        cx += _adv(ch) * sc + track
    return runs


def set_right(txt: str, x_right: float, y: float, h: float, track: float = 0.0) -> List[Poly]:
    return set_text(txt, x_right - text_width(txt, h, track), y, h, track)


def set_centre(txt: str, xc: float, y: float, h: float, track: float = 0.0) -> List[Poly]:
    return set_text(txt, xc - text_width(txt, h, track) / 2, y, h, track)


def _offset(pts: Poly, d: float) -> Poly:
    n = len(pts)
    if n < 2 or abs(d) < 1e-9:
        return list(pts)
    out = []
    for i, (px, py) in enumerate(pts):
        nx = ny = 0.0
        for a, b in ((i - 1, i), (i, i + 1)):
            if a < 0 or b >= n:
                continue
            dx, dy = pts[b][0] - pts[a][0], pts[b][1] - pts[a][1]
            L = math.hypot(dx, dy)
            if L > 1e-9:
                nx -= dy / L
                ny += dx / L
        L = math.hypot(nx, ny)
        out.append((px + d * nx / L, py + d * ny / L) if L > 1e-9 else (px, py))
    return out


def heavy(runs: List[Poly], weight: float, tip: float = 0.3) -> List[Poly]:
    """Display weight: parallel passes of one glyph stroke linked into ONE pen-down run."""
    n = max(2, int(round(weight / tip)) + 1)
    out = []
    for r in runs:
        band: Poly = []
        for k in range(n):
            d = -weight / 2 + weight * k / (n - 1)
            q = _offset(r, d)
            band += q if k % 2 == 0 else q[::-1]
        out.append(band)
    return out


def wrap(txt: str, width: float, h: float, track: float) -> List[str]:
    lines, cur = [], ""
    for w in txt.split(" "):
        t = (cur + " " + w).strip()
        if cur and text_width(t, h, track) > width:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def block(txt: str, x: float, y_top_base: float, width: float, h: float, lead: float,
          track: float, align: str = "left") -> Tuple[List[Poly], float]:
    out: List[Poly] = []
    y = y_top_base
    for ln in wrap(txt, width, h, track):
        if align == "right":
            out += set_right(ln, x + width, y, h, track)
        else:
            out += set_text(ln, x, y, h, track)
        y -= lead
    return out, y + lead


# ===========================================================================
# the plate
# ===========================================================================
CAP_S = 1.8          # small caps (captions, labels)
TRK_S = 0.36
CAPTION_Y, CAP_LEAD = 33.5, 3.3


def build_text(red_end_x: float, check_stats) -> List[Poly]:
    T: List[Poly] = []
    # --- title band: flush-left on the field's left edge -----------------------------------
    T += heavy(set_text("P VS NP", X_L, 392.0, 10.0, track=1.8), 1.2)
    T += set_text("IF IT IS EASY TO CHECK THAT A SOLUTION IS CORRECT,", X_L, 377.0, 2.5, 0.5)
    T += set_text("IS IT ALSO EASY TO FIND ONE?", X_L, 372.0, 2.5, 0.5)
    T += set_text("SATLIB UF20-03: 20 VARIABLES, 91 CLAUSES OF 3.", X_L, 364.0, CAP_S, TRK_S)
    T += set_text("2²⁰ = 1,048,576 CANDIDATES. ONE SATISFIES ALL 91.", X_L, 360.2, CAP_S, TRK_S)
    # --- right column: series caption + definitions (baselines on the statement's grid) -----
    XC = x_of(0b10, 2)          # 181.875: the column stands on the crown stem of node (x1=T, x2=F)
    T += set_text("MILLENNIUM PRIZE PROBLEMS  2 / 7", XC, 400.0, 2.0, 0.4)
    T += set_text("CLAY MATHEMATICS INSTITUTE, 2000", XC, 395.5, 2.0, 0.4)
    T += set_text("P: ANSWERS FOUND IN POLYNOMIAL TIME.", XC, 387.0, 2.0, 0.4)
    T += set_text("NP: ANSWERS CHECKED IN POLYNOMIAL", XC, 382.0, 2.0, 0.4)
    T += set_text("TIME, GIVEN A CERTIFICATE.", XC, 377.0, 2.0, 0.4)
    T += set_text("P IS INSIDE NP. EQUAL? OPEN.", XC, 372.0, 2.0, 0.4)
    # --- the tree's two ends ------------------------------------------------------------------
    T += set_centre("START", x_of(0, 0), 355.0, CAP_S, TRK_S)
    T += set_right("SOLUTION", X_R, 92.0, CAP_S, TRK_S)
    # --- bottom band, right column: CHECKING over FINDING --------------------------------------
    xl = check_stats["x_left"]
    T += set_text("1 2 3 4 −5 6 7 8 9 10 11 −12 13 −14 −15 16 17 18 −19 20", xl, 72.0, 2.0, 0.3)
    T += set_text("CHECKING: 91 CLAUSES, 273 LOOKUPS — THE TESTS ALONG THE RED ALONE.",
                  xl, 50.0, CAP_S, TRK_S)
    t, _ = block("FINDING: BACKTRACKING X1..X20, FALSE FIRST — 8,047 NODES, 45,088 CLAUSE TESTS. "
                 "ROWS 0–7 NODE FOR NODE, BELOW ROW 7 ONE HAIRLINE PER SUB-TREE, AS DEEP AS ITS "
                 "DEEPEST NODE. THIS SEARCH, NOT THE PROBLEM: UNIT PROPAGATION NEEDS 87 NODES.", xl, CAPTION_Y, X_R - xl, CAP_S, CAP_LEAD, TRK_S)
    T += t
    # --- bottom band, left column: the NO companion caption (same baselines) -----------------
    t, _ = block("NO HAS NO CERTIFICATE. PETERSEN GRAPH: DOES A HAMILTONIAN CYCLE EXIST? THE "
                 "SEARCH FROM ONE VERTEX, ALL 274 NODES: NOTHING RED. LEAF ORDER, NOT TO MEASURE.",
                 X_L, CAPTION_Y, 79.0,
                 CAP_S, CAP_LEAD, TRK_S)
    T += t
    return T


def p_vs_np_faithful(rng: SeededRNG, bounds: Bounds, colors: int = 4) -> List[GCodeCommand]:
    def pen(i: int) -> Optional[int]:
        return i if colors >= 4 else min(i, max(colors - 1, 0))

    black, hair, red, st = build_search()
    pet, _ = build_petersen()
    red_end_x = red[-1][-1][0]
    rule, ticks, cst = build_check(x_of(0, 0), red_end_x)
    T = build_text(red_end_x, cst)

    out: List[GCodeCommand] = []
    for i, p in enumerate(sorted(hair, key=lambda q: q[0][0])):
        out += _poly(p if i % 2 == 0 else p[::-1], color=pen(HAIR), f=F_DRAW)
    for p in black + pet:
        out += _poly(p, color=pen(BLACK), f=F_DRAW)
    for p in T:
        out += _poly(p, color=pen(TEXT), f=F_DRAW)
    for p in red + [rule] + ticks:
        out += _poly(p, color=pen(RED), f=F_DRAW)
    return out
