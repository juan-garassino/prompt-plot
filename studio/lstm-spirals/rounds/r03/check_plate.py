"""Re-measure the rendered plate against the computation (r03, forget-gate-vortex).

    .venv/bin/python studio/lstm-spirals/rounds/r03/check_plate.py <render>.gcode [seed]

1. the LSTM run on the plate's sequence (gates per step)
2. per annulus: the angle every DRAWN segment makes with its orbit, median vs
   the designed atan(kappa_t) — the gate is read back off the ink
3. single-centre law: integrating one line through a lone screened vortex,
   radius ratio after one full turn vs k_t
4. spacing: fraction of drawn samples within 0.8 mm of another stroke that
   are NEAR-PARALLEL (the flood failure), vs crossings
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path
from statistics import median

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

import piece as P  # noqa: E402
from promptplot.config import PaperConfig  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402


def strokes(path):
    out, cur, col, down = [], [], None, False
    for line in open(path):
        m = re.search(r"color=(\d+)", line)
        cmd = line.split(";")[0].strip()
        if cmd.startswith("M3"):
            down, col, cur = True, int(m.group(1)) if m else col, []
        elif cmd.startswith("M5"):
            if down and len(cur) > 1:
                out.append((col, cur))
            down = False
        elif cmd.startswith("G0"):
            mx, my = re.search(r"X(-?[\d.]+)", cmd), re.search(r"Y(-?[\d.]+)", cmd)
            if mx and my:
                cur = [(float(mx.group(1)), float(my.group(1)))]
        elif cmd.startswith("G1") and down:
            mx, my = re.search(r"X(-?[\d.]+)", cmd), re.search(r"Y(-?[\d.]+)", cmd)
            cur.append((float(mx.group(1)), float(my.group(1))))
    return out


def main():
    gpath = sys.argv[1]
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    bounds = PaperConfig.from_size("a4", "portrait").get_drawable_area()
    run, pair, black, red, F, _ = P.build_plate(SeededRNG(seed), bounds, 3)

    print("## 1. the trained cell on the plate's sequence")
    print("t  write  x_t     i      f      o      g       c       y")
    for t, s in enumerate(run):
        print(f"{t + 1:<2} {int(s['w'])}      {s['v']:+.2f}  {s['i']:.4f} {s['f']:.4f} {s['o']:.4f} "
              f"{s['g']:+.3f}  {s['c']:+.4f} {s['y']:+.3f}")

    print("\n## 2. drawn angle to the orbit, per annulus (degrees)")
    S = strokes(gpath)
    acc = {}
    for col, pts in S:
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < 0.3:
                continue
            mx, my = 0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])
            li, t = F.where(mx, my)
            if li < 0 or t >= (black if li == 0 else red).n:
                continue
            gx, gy = pair.grad(mx, my)
            tx, ty = -gy, gx
            n = math.hypot(tx, ty)
            if n < 1e-12:
                continue
            c = abs((b[0] - a[0]) * tx + (b[1] - a[1]) * ty) / (L * n)
            ang = math.degrees(math.acos(min(1.0, c)))
            acc.setdefault((li, t, col), []).append(ang)
    for (li, t, col), v in sorted(acc.items()):
        lobe = black if li == 0 else red
        if len(v) < 20 or col is None:
            continue
        want = math.degrees(math.atan(lobe.kappa[t]))
        print(f"{'black' if li == 0 else 'red  '} t={t + 1:<2} pen {col}: designed {want:6.2f}  "
              f"drawn median {median(v):6.2f}  (n={len(v)})")

    print("\n## 3. single-centre law: radius ratio per turn vs k_t (RK4, 0.05 mm step)")
    for k in (red.keeps[0], red.keeps[1], black.keeps[0], black.keeps[1]):
        kap = -math.log(k) / (2 * math.pi)

        def vel(x, y):
            r = math.hypot(x, y)
            u = r / (r * r + 4.0) * math.exp(-r / P._LAMBDA)
            vx, vy = u * (-y / r) - kap * u * (x / r), u * (x / r) - kap * u * (y / r)
            n = math.hypot(vx, vy)
            return vx / n, vy / n

        x, y, th, h = 40.0, 0.0, 0.0, 0.05
        while True:
            k1 = vel(x, y)
            k2 = vel(x + 0.5 * h * k1[0], y + 0.5 * h * k1[1])
            k3 = vel(x + 0.5 * h * k2[0], y + 0.5 * h * k2[1])
            k4 = vel(x + h * k3[0], y + h * k3[1])
            nx = x + h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
            ny = y + h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6
            dth = (math.atan2(ny, nx) - math.atan2(y, x) + math.pi) % (2 * math.pi) - math.pi
            if th + dth >= 2 * math.pi:  # interpolate to exactly one turn
                a = (2 * math.pi - th) / dth
                x, y = x + a * (nx - x), y + a * (ny - y)
                break
            x, y, th = nx, ny, th + dth
        print(f"k = {k:.6f}: r after one turn / r = {math.hypot(x, y) / 40.0:.6f}")

    print("\n## 4. spacing")
    samples = []
    for si, (col, pts) in enumerate(S):
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = max(1, int(L / 0.4))
            for j in range(n):
                q = j / n
                samples.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q,
                                (b[0] - a[0]) / (L or 1), (b[1] - a[1]) / (L or 1), si))
    grid = {}
    for k, s in enumerate(samples):
        grid.setdefault((int(s[0] / 0.8), int(s[1] / 0.8)), []).append(k)
    close = par = side = 0
    worst = 9.0
    for s in samples:
        if s[1] > 255.0 and s[0] < 75.0:  # the weighted title: passes are 0.35 mm apart BY DESIGN
            continue
        ci, cj = int(s[0] / 0.8), int(s[1] / 0.8)
        hit = None
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for k in grid.get((ci + di, cj + dj), ()):
                    o = samples[k]
                    if o[4] == s[4]:
                        continue
                    d = math.hypot(o[0] - s[0], o[1] - s[1])
                    if d < 0.8 and (hit is None or d < hit[0]):
                        hit = (d, o)
        if hit:
            close += 1
            o = hit[1]
            if abs(s[2] * o[2] + s[3] * o[3]) > 0.94:
                par += 1
                perp = abs((o[0] - s[0]) * s[3] - (o[1] - s[1]) * s[2])
                if perp > 0.2:  # side by side, not a collinear continuation
                    side += 1
                    worst = min(worst, perp)
    n = len(samples)
    print(f"samples {n} (title excluded); within 0.8 mm of another stroke {100 * close / n:.2f}%; "
          f"near-parallel {100 * par / n:.2f}%; of those SIDE BY SIDE (perp > 0.2 mm, the flood "
          f"failure) {100 * side / n:.2f}%, min perp {worst:.2f} mm")


if __name__ == "__main__":
    main()
