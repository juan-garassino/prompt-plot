"""Near-parallel centreline gap audit on a gcode (line layers only, text excluded).

usage: gapcheck.py file.gcode [--layers 0,1,3,4] [--floor 0.8] [--angle 10]
A violation is a run of >= 1 mm along stroke A whose samples lie < floor from a
DIFFERENT stroke B, with the two local directions within `angle` deg of parallel
(crossings and shallow butt-joins shorter than 1 mm are not parallel runs).
Prints the global minimum near-parallel gap and every violating pair.
"""
import math
import re
import sys
from collections import defaultdict

import numpy as np

g = sys.argv[1]
args = sys.argv[2:]
layers = {0, 1, 3, 4}
floor, ang_tol = 0.8, 10.0
for i, a in enumerate(args):
    if a == "--layers":
        layers = {int(x) for x in args[i + 1].split(",")}
    if a == "--floor":
        floor = float(args[i + 1])
    if a == "--angle":
        ang_tol = float(args[i + 1])

strokes, cur, col, pos, down = [], None, None, (0.0, 0.0), False
for ln in open(g):
    m = re.match(r"(G[01])", ln)
    if not m:
        continue
    xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
    cm = re.search(r"color=(\d+)", ln)
    if not xs:
        continue
    p = (float(xs.group(1)), float(ys.group(1)))
    if m.group(1) == "G1":
        if cm:
            col = int(cm.group(1))
        if not down:
            cur = [col, [pos]]
            strokes.append(cur)
        cur[1].append(p)
        down = True
    else:
        down = False
    pos = p

S = []  # samples: x, y, dx, dy, stroke id, seg ax, ay, bx, by, first-seg, last-seg
for sid, (c, pts) in enumerate(strokes):
    if c not in layers:
        continue
    nseg = len(pts) - 1
    for si, (a, b) in enumerate(zip(pts, pts[1:])):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        n = max(1, int(L / 0.2))
        for t in (np.arange(n + 1) / n if b == pts[-1] else np.arange(n) / n):  # r03 v7: sample each stroke END too, so a butt join reads as the touch it is
            S.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t,
                      (b[0] - a[0]) / L, (b[1] - a[1]) / L, sid,
                      a[0], a[1], b[0], b[1], si == 0, si == nseg - 1))
S = np.asarray(S)
cell = floor
grid = defaultdict(list)
keys = np.floor(S[:, :2] / cell).astype(int)
for i, (kx, ky) in enumerate(keys):
    grid[(kx, ky)].append(i)
cos_t = math.cos(math.radians(ang_tol))
best = 1e9
bad = defaultdict(list)  # (sidA, sidB) -> [(d, x, y)]
for i in range(len(S)):
    kx, ky = keys[i]
    x, y, dx, dy, sid = S[i, :5]
    for ox in (-1, 0, 1):
        for oy in (-1, 0, 1):
            for j in grid.get((kx + ox, ky + oy), ()):
                if S[j, 4] == sid:
                    continue
                # EXACT point-to-segment gap from A's sample to B's local segment,
                # counted only when the foot falls ON B's ink (r03 v7): a side-by-side
                # run is abeam of B; an end-to-end butt join (B continues where A
                # stops) has its foot past B's end, and is a touch, not a parallel run.
                ax_, ay_, bx_, by_ = S[j, 5], S[j, 6], S[j, 7], S[j, 8]
                vx, vy = bx_ - ax_, by_ - ay_
                L2 = vx * vx + vy * vy
                tt = ((x - ax_) * vx + (y - ay_) * vy) / L2
                if tt < 0.0 or tt > 1.0:  # foot off this segment (off B's ink, or the neighbour segment's case)
                    continue
                d = math.hypot(x - ax_ - tt * vx, y - ay_ - tt * vy)
                if d >= floor or d < 1e-6:
                    continue
                if abs(dx * S[j, 2] + dy * S[j, 3]) < cos_t:
                    continue
                bad[(int(sid), int(S[j, 4]))].append((d, x, y))
viol = []
for (a, b), v in bad.items():
    if a > b:
        continue
    if len(v) < 5:  # < 1 mm of run
        continue
    dmin = min(v)
    # true touches (a ray END on a curve, a butt join) come down to ~0: report separately
    viol.append((dmin[0], a, b, strokes[a][0], strokes[b][0], dmin[1], dmin[2], len(v)))
viol.sort()
meet = [v for v in viol if v[0] < 0.1]   # the two lines TOUCH: a ray END meeting a curve (a mark)
par = [v for v in viol if v >= (0.1,)]
print(f"{len(S)} samples, {len(strokes)} strokes")
print(f"near-parallel (<{ang_tol} deg) runs >= 1 mm with a centre gap under {floor} mm (lines that never touch): {len(par)}")
for v in par[:40]:
    print(f"  gap {v[0]:.3f} mm  strokes {v[1]}(pen {v[3]}) / {v[2]}(pen {v[4]})  at ({v[5]:.2f}, {v[6]:.2f})")
print(f"shallow MEETINGS (a line ends on / touches another at < {ang_tol} deg): {len(meet)}")
for v in meet[:40]:
    print(f"  touch {v[0]:.3f} mm  strokes {v[1]}(pen {v[3]}) / {v[2]}(pen {v[4]})  at ({v[5]:.2f}, {v[6]:.2f})")
