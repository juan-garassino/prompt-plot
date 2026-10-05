"""r03 acceptance audit, read off the GCODE (not the piece's own numbers).

usage: audit.py r03.gcode r02.gcode

1. tree and red layers (pens 0, 1, 3) identical to r02: the multiset of pen-down
   strokes, coordinates to the gcode's 3 decimals (stroke order may differ);
2. type (pen 2): min distance to any red sample (path + 91 ticks) >= 10 mm,
   min distance to the hub >= R + 14 = 142 mm, nothing below y = 260;
3. type blocks start at x = 15 and stay <= 88, except the needle caption (y > 385, x >= 110);
4. the upper-right quiet [115, 282] x [285, 385] holds no ink at all;
5. feed: every G1 at F600; every dwell G4 P1.
"""
from __future__ import annotations

import math
import re
import sys
from collections import Counter

HUB, R = (148.5, 148.5), 128.0


def strokes(path):
    out, cur, col, down, pos = [], None, 0, False, None
    feeds, dwells = Counter(), Counter()
    for ln in open(path):
        m = re.match(r"(G0|G1|G4|M3|M5)\b", ln)
        if not m:
            continue
        c = m.group(1)
        if c == "G4":
            dwells[re.search(r"P([\d.]+)", ln).group(1)] += 1
            continue
        if c == "M3":
            cm = re.search(r"color=(\d+)", ln)
            col = int(cm.group(1)) if cm else col
            down, cur = True, [col, [pos]]
            out.append(cur)
            continue
        if c == "M5":
            down = False
            continue
        xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
        if not xs:
            continue
        pos = (float(xs.group(1)), float(ys.group(1)))
        if c == "G1":
            fm = re.search(r"F(\d+)", ln)
            feeds[fm.group(1) if fm else "-"] += 1
            if down:
                cur[1].append(pos)
    return [s for s in out if len(s[1]) > 1], feeds, dwells


def canon(pts):
    t = tuple((round(x, 3), round(y, 3)) for x, y in pts)
    return min(t, t[::-1])


def samples(pts, step=0.1):
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        n = max(1, int(math.dist(a, b) / step))
        for k in range(n + 1):
            yield (a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)


def main():
    new, feeds, dwells = strokes(sys.argv[1])
    old, _, _ = strokes(sys.argv[2])
    ok = True
    for pen in (0, 1, 3):
        a = Counter(canon(p) for c, p in new if c == pen)
        b = Counter(canon(p) for c, p in old if c == pen)
        same = a == b
        ok &= same
        print(f"1. pen {pen}: {sum(a.values())} strokes vs r02 {sum(b.values())} -> "
              f"{'IDENTICAL' if same else 'DIFFERENT'}")

    red = [q for c, p in new if c == 3 for q in samples(p, 0.2)]
    text = [(p, list(samples(p, 0.1))) for c, p in new if c == 2]
    tpts = [q for _, s in text for q in s]
    # bucket red for a fast nearest search
    grid = {}
    for q in red:
        grid.setdefault((int(q[0] // 5), int(q[1] // 5)), []).append(q)

    def dred(q):
        gx, gy = int(q[0] // 5), int(q[1] // 5)
        best = 1e9
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                for r in grid.get((gx + dx, gy + dy), ()):
                    best = min(best, math.dist(q, r))
        return best

    d_red = min(dred(q) for q in tpts)
    d_hub = min(math.dist(q, HUB) for q in tpts)
    y_min = min(q[1] for q in tpts)
    print(f"2. type->red min {d_red:.2f} mm (>= 10) {'PASS' if d_red >= 10 else 'FAIL'}")
    print(f"   type->hub min {d_hub:.2f} mm (>= {R + 14:.0f}) {'PASS' if d_hub >= R + 14 else 'FAIL'}")
    print(f"   type lowest y {y_min:.2f} (>= 260) {'PASS' if y_min >= 260 else 'FAIL'}")
    ok &= d_red >= 10 and d_hub >= R + 14 and y_min >= 260

    left = [q for q in tpts if q[1] <= 385.0 or q[0] < 110]
    x0, x1 = min(q[0] for q in left), max(q[0] for q in left)
    cap = [q for q in tpts if q[1] > 385.0 and q[0] >= 110]
    print(f"3. left stack ink x [{x0:.2f}, {x1:.2f}] (15..88) {'PASS' if x0 >= 14.99 and x1 <= 88 else 'FAIL'};"
          f" needle caption x from {min(q[0] for q in cap):.2f}")
    ok &= x0 >= 14.99 and x1 <= 88

    quiet = [q for c, p in new if c != 3 for q in samples(p, 0.5) if 115 <= q[0] <= 282 and 285 <= q[1] <= 385]
    print(f"4. upper-right quiet [115,282]x[285,385], all pens but the needle: {len(quiet)} ink samples {'PASS' if not quiet else 'FAIL'}")
    ok &= not quiet
    below60 = Counter(c for c, p in new for q in p if q[1] < 60)
    print(f"   pens with ink below y 60: {dict(below60)} (dial hair/black only)")

    print(f"5. G1 feeds {dict(feeds)}; dwells {dict(dwells)}")
    ok &= set(feeds) == {"600"}
    print("ALL PASS" if ok else "SOMETHING FAILED")


if __name__ == "__main__":
    main()
