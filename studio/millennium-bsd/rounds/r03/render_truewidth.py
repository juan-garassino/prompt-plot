"""True-width raster of this plate's gcode (pens at their physical nib widths).

usage: render_truewidth.py file.gcode out.png [x0 y0 x1 y1 [px_per_mm]]
"""
import re
import sys

from PIL import Image, ImageDraw

g, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(float, sys.argv[3:7]) if len(sys.argv) > 6 else (0, 0, 297, 420)
k = float(sys.argv[7]) if len(sys.argv) > 7 else 6
W = {0: 0.1, 1: 0.3, 2: 0.3, 3: 0.5, 4: 0.7}
C = {0: (30, 30, 30), 1: (0, 0, 0), 2: (0, 0, 0), 3: (0, 0, 0), 4: (196, 150, 40)}
im = Image.new("RGB", (int((x1 - x0) * k), int((y1 - y0) * k)), (244, 239, 228))
d = ImageDraw.Draw(im)
pos, col, segs = (0, 0), 0, []
for ln in open(g):
    m = re.match(r"(G[01])", ln)
    if not m:
        continue
    cm = re.search(r"color=(\d+)", ln)
    xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
    if not xs:
        continue
    p = (float(xs.group(1)), float(ys.group(1)))
    if m.group(1) == "G1":
        if cm:
            col = int(cm.group(1))
        segs.append((pos, p, col))
    pos = p
f = lambda q: ((q[0] - x0) * k, (y1 - q[1]) * k)  # noqa: E731
for a, b, c in sorted(segs, key=lambda s: s[2]):
    w = max(1, round(W.get(c, .3) * k))
    d.line([f(a), f(b)], fill=C.get(c, (0, 0, 0)), width=w)
    if w > 2:
        r = w / 2
        for q in (f(a), f(b)):
            d.ellipse([q[0] - r, q[1] - r, q[0] + r, q[1] + r], fill=C.get(c, (0, 0, 0)))
im.save(out)
