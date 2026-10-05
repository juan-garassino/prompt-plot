"""Per-layer plot budget from a gcode: draw m, strokes, travel, longest travel, minutes.

usage: layer_stats.py file.gcode
Time model (Leo): draw F600 = 10 mm/s, travel ~33 mm/s (G1 F2000 rapids), 2.0 s per
pen cycle (lift + drop dwells).  Also reports whether each colour layer is contiguous.
"""
import math
import re
import sys
from collections import OrderedDict

g = sys.argv[1]
pos, col, pen_down = (0.0, 0.0), None, False
L = OrderedDict()
seq = []
for ln in open(g):
    m = re.match(r"(G[01])", ln)
    if not m:
        continue
    xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
    cm = re.search(r"color=(\d+)", ln)
    if not xs:
        continue
    p = (float(xs.group(1)), float(ys.group(1)))
    d = math.hypot(p[0] - pos[0], p[1] - pos[1])
    if m.group(1) == "G1":
        c = int(cm.group(1)) if cm else col
        if c != col:
            seq.append(c)
        col = c
        s = L.setdefault(c, dict(draw=0.0, strokes=0, travel=0.0, maxtr=0.0, pending=0.0))
        if not pen_down:
            s["strokes"] += 1
            if s["strokes"] > 1:
                s["travel"] += s["pending"]
                s["maxtr"] = max(s["maxtr"], s["pending"])
        s["draw"] += d
        pen_down = True
    else:
        if pen_down and col is not None:
            L[col]["pending"] = 0.0
        if col is not None:
            L[col]["pending"] += d
        pen_down = False
    pos = p
tot = 0.0
for c, s in L.items():
    mins = (s["draw"] / 10 + s["travel"] / 33 + 2.0 * s["strokes"]) / 60
    tot += mins
    print(f"pen {c}: draw {s['draw']/1000:.2f} m  strokes {s['strokes']}  travel {s['travel']/1000:.2f} m"
          f"  longest intra-layer travel {s['maxtr']:.0f} mm  ~{mins:.0f} min")
print(f"total ~{tot:.0f} min; layer sequence {seq} (contiguous={len(seq) == len(set(seq))})")
