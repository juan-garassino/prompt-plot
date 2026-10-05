"""True-width raster of a gcode for crop inspection. usage: raster.py file.gcode out.png x0 y0 x1 y1 [pxmm]"""
import sys, re
from PIL import Image, ImageDraw
g, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = map(float, sys.argv[3:7]); k = float(sys.argv[7]) if len(sys.argv) > 7 else 12
W = {0: 0.1, 1: 0.3, 2: 0.3, 3: 0.5}; C = {0: (95, 95, 95), 1: (0, 0, 0), 2: (0, 0, 0), 3: (210, 20, 50)}
im = Image.new("RGB", (int((x1 - x0) * k), int((y1 - y0) * k)), (244, 239, 228)); d = ImageDraw.Draw(im)
pos = (0, 0); down = False; col = 0
segs = []
for ln in open(g):
    m = re.match(r"(G[01]|M3|M5)", ln)
    if not m: continue
    c = m.group(1)
    cm = re.search(r"color=(\d+)", ln)
    if c == "M3": down = True; col = int(cm.group(1)) if cm else col; continue
    if c == "M5": down = False; continue
    xs = re.search(r"X([-\d.]+)", ln); ys = re.search(r"Y([-\d.]+)", ln)
    if not xs: continue
    p = (float(xs.group(1)), float(ys.group(1)))
    if c == "G1":
        if cm: col = int(cm.group(1))
        segs.append((pos, p, col))
    pos = p
for a, b, c in sorted(segs, key=lambda s: s[2]):
    f = lambda q: ((q[0] - x0) * k, (y1 - q[1]) * k)
    d.line([f(a), f(b)], fill=C.get(c, (0, 0, 0)), width=max(1, round(W.get(c, .3) * k)))
im.save(out)
