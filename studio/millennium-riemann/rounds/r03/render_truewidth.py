"""True-width raster of a gcode for crop inspection (round nib: polylines drawn with
curved joints + round end caps, 4x supersampled).  r01's script, rebuilt for r03.

usage: render_truewidth.py file.gcode out.png x0 y0 x1 y1 [pxmm]
"""
import re
import sys

from PIL import Image, ImageDraw

g, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(float, sys.argv[3:7])
k_out = float(sys.argv[7]) if len(sys.argv) > 7 else 12
SS = 4
k = k_out * SS
W = {0: 0.1, 1: 0.3, 2: 0.3, 3: 0.5}
C = {0: (40, 40, 40), 1: (0, 0, 0), 2: (0, 0, 0), 3: (210, 20, 50)}
strokes = []  # (colour, [pts])
pos = (0.0, 0.0)
cur = None
col = 0
for ln in open(g):
    m = re.match(r"(G[01])", ln)
    if not m:
        continue
    cm = re.search(r"color=(\d+)", ln)
    xs = re.search(r"X([-\d.]+)", ln)
    ys = re.search(r"Y([-\d.]+)", ln)
    if not xs or not ys:
        continue
    p = (float(xs.group(1)), float(ys.group(1)))
    if m.group(1) == "G1":
        if cm:
            col = int(cm.group(1))
        if cur is None:
            cur = (col, [pos])
            strokes.append(cur)
        cur[1].append(p)
    else:
        cur = None
    pos = p
im = Image.new("RGB", (int((x1 - x0) * k), int((y1 - y0) * k)), (244, 239, 228))
d = ImageDraw.Draw(im)


def f(q):
    return ((q[0] - x0) * k, (y1 - q[1]) * k)


for c, pts in sorted(strokes, key=lambda s: s[0]):
    w = W.get(c, 0.3) * k
    colr = C.get(c, (0, 0, 0))
    P = [f(q) for q in pts]
    d.line(P, fill=colr, width=max(1, round(w)), joint="curve")
    for cx, cy in (P[0], P[-1]):
        d.ellipse([cx - w / 2, cy - w / 2, cx + w / 2, cy + w / 2], fill=colr)
im = im.resize((int((x1 - x0) * k_out), int((y1 - y0) * k_out)), Image.LANCZOS)
im.save(out)
