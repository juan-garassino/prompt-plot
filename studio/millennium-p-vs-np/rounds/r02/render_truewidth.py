"""True-width raster of a plate gcode (each pen at its nib width, on cream) + per-layer stats.

usage: render_truewidth.py file.gcode out.png [x0 y0 x1 y1] [--px 8]
"""
from __future__ import annotations

import argparse
import math
import re

from PIL import Image, ImageDraw

W = {0: 0.1, 1: 0.3, 2: 0.3, 3: 0.5}
C = {0: (30, 30, 30), 1: (0, 0, 0), 2: (0, 0, 0), 3: (205, 18, 48)}


def parse(path):
    segs, pos, col, strokes = [], (0.0, 0.0), 0, []
    down = False
    for ln in open(path):
        m = re.match(r"(G0|G1|M3|M5)", ln)
        if not m:
            continue
        c = m.group(1)
        cm = re.search(r"color=(\d+)", ln)
        if c == "M3":
            down = True
            col = int(cm.group(1)) if cm else col
            strokes.append([col, [pos], pos])
            continue
        if c == "M5":
            down = False
            continue
        xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
        if not xs:
            continue
        p = (float(xs.group(1)), float(ys.group(1)))
        if c == "G1" and down:
            segs.append((pos, p, col))
            strokes[-1][1].append(p)
        pos = p
    return segs, strokes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gcode")
    ap.add_argument("out")
    ap.add_argument("box", nargs="*", type=float)
    ap.add_argument("--px", type=float, default=8.0)
    a = ap.parse_args()
    x0, y0, x1, y1 = a.box if a.box else (0, 0, 297, 420)
    k = a.px
    segs, strokes = parse(a.gcode)
    im = Image.new("RGB", (int((x1 - x0) * k), int((y1 - y0) * k)), (244, 239, 228))
    d = ImageDraw.Draw(im)
    f = lambda q: ((q[0] - x0) * k, (y1 - q[1]) * k)
    for p, q, c in sorted(segs, key=lambda s: s[2]):
        w = max(1, round(W.get(c, 0.3) * k))
        d.line([f(p), f(q)], fill=C.get(c, (0, 0, 0)), width=w)
        if w > 2:
            r = w / 2
            for e in (p, q):
                ex, ey = f(e)
                d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=C.get(c, (0, 0, 0)))
    im.save(a.out)
    if not a.box:
        # per-layer stats: strokes, draw m, travel m (within layer), order of layers
        order, stat = [], {}
        prev_end = None
        for col, pts, start in strokes:
            if col not in stat:
                order.append(col)
                stat[col] = [0, 0.0, 0.0]
                prev_end = None
            s = stat[col]
            s[0] += 1
            s[1] += sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
            if prev_end is not None:
                s[2] += math.dist(prev_end, pts[0])
            prev_end = pts[-1]
        print("layer order", order, "(contiguous)" if len(order) == len(set(order)) else "(RE-ENTERED)")
        for c in order:
            n, dr, tr = stat[c]
            mins = (dr + tr) / 10.0 / 60.0 + n * 2.5 / 60.0  # F600 draw + ~2.5 s per pen cycle
            print(f"pen {c}: {n} strokes, draw {dr/1000:.2f} m, travel {tr/1000:.2f} m, ~{mins:.1f} min")


if __name__ == "__main__":
    main()
