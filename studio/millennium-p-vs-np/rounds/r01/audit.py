"""Audit a render of the faithful P vs NP plate against encoding §10/§11.

    .venv/bin/python studio/millennium-p-vs-np/rounds/r01/audit.py ~/Downloads/pp_..._vN.gcode
"""
from __future__ import annotations

import collections
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import piece as P  # noqa: E402

NAMES = {0: "HAIR 0.1", 1: "BLACK 0.3", 2: "TEXT 0.3", 3: "RED 0.5"}
F_MM_S = 10.0      # Leo F600 ~ 10 mm/s draw
TRAVEL_MM_S = 33.0  # G0 at the slowed Leo travel (G1 F2000)
CYCLE_S = 2.5      # one lift + drop with dwells


def parse(path):
    strokes = []            # (colour, [pts])
    order = []
    travel = collections.Counter()
    pos, down, col, cur = (0.0, 0.0), False, 0, None
    for ln in open(path):
        m = re.match(r"(G[01]|M3|M5)", ln)
        if not m:
            continue
        c = m.group(1)
        cm = re.search(r"color=(\d+)", ln)
        if c == "M3":
            down = True
            col = int(cm.group(1)) if cm else col
            cur = [pos]
            strokes.append((col, cur))
            if not order or order[-1] != col:
                order.append(col)
            continue
        if c == "M5":
            down = False
            continue
        xs = re.search(r"X([-\d.]+)", ln)
        ys = re.search(r"Y([-\d.]+)", ln)
        if not xs:
            continue
        p = (float(xs.group(1)), float(ys.group(1)))
        if c == "G1" and down:
            cur.append(p)
        elif c == "G0":
            travel[col] += math.dist(pos, p)
        pos = p
    return strokes, order, travel


def main():
    g = Path(sys.argv[1]).expanduser()
    strokes, order, travel = parse(g)
    print("layer order in gcode:", [NAMES[c] for c in order], "swaps(physical):",
          "2 (0.1 -> 0.3 -> [text same pen] -> red)")
    tot = 0.0
    for c in sorted(NAMES):
        ss = [s for cc, s in strokes if cc == c]
        L = sum(math.dist(a, b) for s in ss for a, b in zip(s, s[1:]))
        mins = L / F_MM_S / 60 + len(ss) * CYCLE_S / 60 + travel[c] / TRAVEL_MM_S / 60
        tot += mins
        print(f"  {NAMES[c]:10s} draw {L/1000:6.2f} m  travel {travel[c]/1000:5.2f} m  "
              f"strokes {len(ss):4d}  ~{mins:5.1f} min")
    print(f"  total ~{tot:.0f} min")
    xs = [p[0] for _, s in strokes for p in s]
    ys = [p[1] for _, s in strokes for p in s]
    print("ink bbox", min(xs), max(xs), min(ys), max(ys))

    black, hair, red, st = P.build_search()
    # --- §11.1 / 11.2 / 11.3 --------------------------------------------------------------
    rx = red[0][-1][0]
    print("red strokes", len(red), "red end", red[0][-1], "(want x 273.6 +- 0.5, y 100)")
    ends = collections.Counter(round(p[-1][1], 3) for p in hair)
    row20 = [p[0][0] for p in hair if abs(p[-1][1] - P.y_of(20)) < 1e-6]
    print("lines reaching row 20:", len(row20) + 1, "(black", len(row20), "+ red)")
    print("black reaching row 20 left of centre:", [round(x, 2) for x in row20 if x < 148.5])
    print("row-6 conflict ends:", len(st["row6_ends"]), [round(x, 1) for _, x in st["row6_ends"]])
    ends_at = collections.Counter()
    for p in black:
        ends_at[round(p[-1][1], 2)] += 1
    print("black run ends by y:", dict(sorted(ends_at.items(), reverse=True)))
    # --- spacing: nearest vertical neighbour at each row ---------------------------------
    worst = 9e9
    for d in range(1, 21):
        y = P.y_of(d) + 0.5
        cross = []
        for w, polys in ((0.3, black), (0.1, hair), (0.5, red)):
            for p in polys:
                for a, b in zip(p, p[1:]):
                    if abs(a[0] - b[0]) < 1e-9 and min(a[1], b[1]) <= y <= max(a[1], b[1]):
                        cross.append((a[0], w))
        cross.sort()
        for (x1, w1), (x2, w2) in zip(cross, cross[1:]):
            clear = (x2 - x1) - (w1 + w2) / 2
            worst = min(worst, x2 - x1)
    print("min centre-to-centre between verticals (all rows):", round(worst, 3), "mm")
    hx = sorted(p[0][0] for p in hair)
    near = min(abs(x - rx) for x in hx)
    print("red to nearest hairline below row 7:", round(near, 3), "mm (centre-centre)")
    rule, ticks, cst = P.build_check(P.x_of(0, 0), rx)
    print("ticks", len(ticks), "pitch", round(cst["pitch"], 4), "hist", cst["hist"],
          "groups", len(cst["groups"]), "chain", round(rule[0][0], 2), "->", round(rule[1][0], 2))
    pet, pc = P.build_petersen()
    print("petersen", pc)


if __name__ == "__main__":
    main()
