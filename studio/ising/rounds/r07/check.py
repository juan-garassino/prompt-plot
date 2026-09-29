"""r07 acceptance checks measured on the INK.

usage: .venv/bin/python studio/ising/rounds/r07/check.py file.gcode

Reads the rendered gcode (pen-down G1 polylines per colour layer) and reports:
  A19  crimson x (black|grey) crossings (proper or touching), and the minimum
       distance from any black/grey vertex or segment to the crimson ink
  A9   minimum centre distance between parallel black/grey/red segments that
       overlap > 0.3 mm, split into  same-stroke-family (pass offsets / knots)
       and all pairs; pairs under 0.34 mm are listed as potential knots
  A2   draw, travel, ratio, longest travel per layer, pen-downs per layer
"""
from __future__ import annotations

import math
import re
import sys
from collections import defaultdict


def parse(path):
    layers = defaultdict(list)  # colour -> list of polylines
    travel = defaultdict(list)
    color = 0
    pos = (0.0, 0.0)
    cur = None
    pen = False
    for line in open(path):
        m = re.search(r"color=(\d+)", line)
        if m:
            color = int(m.group(1))
        s = line.split(";")[0].strip()
        if not s:
            continue
        w = s.split()
        if w[0] == "M3":
            pen = True
            cur = [pos]
        elif w[0] == "M5":
            if cur and len(cur) > 1:
                layers[color].append(cur)
            cur = None
            pen = False
        elif w[0] in ("G0", "G1"):
            x = y = None
            for t in w[1:]:
                if t[0] == "X":
                    x = float(t[1:])
                if t[0] == "Y":
                    y = float(t[1:])
            if x is None and y is None:
                continue
            np_ = (x if x is not None else pos[0], y if y is not None else pos[1])
            if w[0] == "G1" and pen and cur is not None:
                cur.append(np_)
            elif w[0] == "G0" or not pen:
                travel[color].append(math.hypot(np_[0] - pos[0], np_[1] - pos[1]))
            pos = np_
    return layers, travel


def segs(polys):
    out = []
    for k, p in enumerate(polys):
        for a, b in zip(p, p[1:]):
            if math.hypot(b[0] - a[0], b[1] - a[1]) > 1e-9:
                out.append((a, b, k))
    return out


def seg_dist(a, b, c, d):
    def pd(p, a, b):
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        t = 0.0 if L == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L))
        return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)

    if intersects(a, b, c, d):
        return 0.0
    return min(pd(a, c, d), pd(b, c, d), pd(c, a, b), pd(d, a, b))


def intersects(a, b, c, d):
    def o(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)

    def on(p, q, r):
        return min(p[0], r[0]) - 1e-9 <= q[0] <= max(p[0], r[0]) + 1e-9 and \
            min(p[1], r[1]) - 1e-9 <= q[1] <= max(p[1], r[1]) + 1e-9

    o1, o2, o3, o4 = o(a, b, c), o(a, b, d), o(c, d, a), o(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return (o1 == 0 and on(a, c, b)) or (o2 == 0 and on(a, d, b)) or \
        (o3 == 0 and on(c, a, d)) or (o4 == 0 and on(c, b, d))


class Grid:
    def __init__(self, ss, cell=3.0):
        self.c = cell
        self.g = defaultdict(list)
        for i, (a, b, _k) in enumerate(ss):
            for gx in range(int(min(a[0], b[0]) // cell), int(max(a[0], b[0]) // cell) + 1):
                for gy in range(int(min(a[1], b[1]) // cell), int(max(a[1], b[1]) // cell) + 1):
                    self.g[(gx, gy)].append(i)

    def near(self, a, b, pad):
        c = self.c
        out = set()
        for gx in range(int((min(a[0], b[0]) - pad) // c), int((max(a[0], b[0]) + pad) // c) + 1):
            for gy in range(int((min(a[1], b[1]) - pad) // c), int((max(a[1], b[1]) + pad) // c) + 1):
                out.update(self.g.get((gx, gy), ()))
        return out


def parallel_gap(s1, s2):
    (a, b, _), (c, d, _) = s1, s2
    h1, h2 = abs(a[1] - b[1]) < 1e-9, abs(c[1] - d[1]) < 1e-9
    v1, v2 = abs(a[0] - b[0]) < 1e-9, abs(c[0] - d[0]) < 1e-9
    if h1 and h2:
        ov = min(max(a[0], b[0]), max(c[0], d[0])) - max(min(a[0], b[0]), min(c[0], d[0]))
        return abs(a[1] - c[1]), ov
    if v1 and v2:
        ov = min(max(a[1], b[1]), max(c[1], d[1])) - max(min(a[1], b[1]), min(c[1], d[1]))
        return abs(a[0] - c[0]), ov
    return None, 0.0


def main(path, field_x0=36.0, field_y1=188.45, field_y0=36.3):
    layers, travel = parse(path)
    red = segs(layers.get(1, []))
    rg = Grid(red)
    report = {}
    for col, name in ((0, "black"), (2, "grey")):
        ss = segs(layers.get(col, []))
        cross = 0
        dmin = 1e9
        where = None
        for a, b, _k in ss:
            if max(a[0], b[0]) < field_x0 or min(a[1], b[1]) > field_y1:
                continue
            for i in rg.near(a, b, 1.5):
                c, d, _ = red[i]
                dd = seg_dist(a, b, c, d)
                if dd == 0.0:
                    cross += 1
                if dd < dmin:
                    dmin, where = dd, (round(a[0], 1), round(a[1], 1))
        report[name] = {"crossings_with_red": cross, "min_dist_to_red_mm": round(dmin, 3),
                        "at": where}
    # A9 + knots over black+grey+red, field only
    allp = []
    for col in (0, 1, 2):
        for p in layers.get(col, []):
            allp.append((col, p))
    ss = []
    for k, (col, p) in enumerate(allp):
        for a, b in zip(p, p[1:]):
            if min(a[0], b[0]) >= field_x0 and field_y0 <= min(a[1], b[1]) and max(a[1], b[1]) <= field_y1 and math.hypot(b[0] - a[0], b[1] - a[1]) > 1e-9:
                ss.append((a, b, k))
    g = Grid(ss)
    knots = []
    diff_min = 1e9
    for i, s in enumerate(ss):
        for j in g.near(s[0], s[1], 1.0):
            if j <= i:
                continue
            t = ss[j]
            gap, ov = parallel_gap(s, t)
            if gap is None or ov <= 0.3 or gap < 1e-6:
                continue
            if allp[s[2]][0] == 1 and allp[t[2]][0] == 1:
                continue  # the coast's own +-0.15 mm passes
            if s[2] != t[2]:
                diff_min = min(diff_min, gap)
            if gap < 0.34:
                knots.append((round(gap, 3), round(s[0][0], 1), round(s[0][1], 1), s[2] == t[2]))
    report["parallel_min_between_strokes_mm"] = round(diff_min, 3)
    report["pairs_under_0.34mm"] = len(knots)
    report["pairs_under_0.34mm_examples"] = sorted(knots)[:8]
    # A2
    tot_d = tot_t = 0.0
    for col in sorted(set(layers) | set(travel)):
        d = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for p in layers.get(col, [])
                for a, b in zip(p, p[1:]))
        t = travel.get(col, [])
        tot_d += d
        tot_t += sum(t)
        report[f"layer{col}"] = {"draw_m": round(d / 1000, 2), "travel_m": round(sum(t) / 1000, 2),
                                 "pen_downs": len(layers.get(col, [])),
                                 "longest_travel_mm": round(max(t, default=0), 1)}
    report["draw_m"] = round(tot_d / 1000, 2)
    report["travel_m"] = round(tot_t / 1000, 2)
    report["travel_ratio"] = round(tot_t / tot_d, 3)
    for k, v in report.items():
        print(k, v)


if __name__ == "__main__":
    main(sys.argv[1])
