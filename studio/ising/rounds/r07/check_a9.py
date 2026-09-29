"""r07 A9 on the drawn strokes, by OWNER: minimum centre distance between
parallel segments of different owners (free cluster id, 'rule', 'coast' with
its +-0.15 mm passes) overlapping by more than 0.3 mm.

usage: .venv/bin/python studio/ising/rounds/r07/check_a9.py SEED
"""
from __future__ import annotations

import importlib.util
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "../../../..")))
from promptplot.config import PaperConfig  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402

spec = importlib.util.spec_from_file_location("r07piece", os.path.join(HERE, "piece.py"))
m = importlib.util.module_from_spec(spec)
sys.modules["r07piece"] = m
spec.loader.exec_module(m)

seed = int(sys.argv[1])
paper = PaperConfig.from_size("a4", "landscape")
m.ising_cooling_strip_r07(SeededRNG(seed), paper.get_drawable_area(), colors=3)
f = m.ising_cooling_strip_r07
segs = []
for c, _p, q in f.strokes:
    for a, b in zip(q, q[1:]):
        segs.append((a, b, ("cl", c)))
for q in f.rules:
    for a, b in zip(q, q[1:]):
        segs.append((a, b, ("rule",)))
for a, b in f.shore_mm:
    for off in (-0.15, 0.0, 0.15):
        if abs(a[0] - b[0]) < 1e-9:
            segs.append(((a[0] + off, a[1]), (b[0] + off, b[1]), ("coast",)))
        else:
            segs.append(((a[0], a[1] + off), (b[0], b[1] + off), ("coast",)))
cell = 2.0
grid = defaultdict(list)
for i, (a, b, _o) in enumerate(segs):
    for gx in range(int(min(a[0], b[0]) // cell), int(max(a[0], b[0]) // cell) + 1):
        for gy in range(int(min(a[1], b[1]) // cell), int(max(a[1], b[1]) // cell) + 1):
            grid[(gx, gy)].append(i)
best = (9.0, None)
under = 0
for i, (a, b, o) in enumerate(segs):
    hor = abs(a[1] - b[1]) < 1e-9
    near = set()
    for gx in range(int((min(a[0], b[0]) - 1) // cell), int((max(a[0], b[0]) + 1) // cell) + 1):
        for gy in range(int((min(a[1], b[1]) - 1) // cell), int((max(a[1], b[1]) + 1) // cell) + 1):
            near.update(grid.get((gx, gy), ()))
    for j in near:
        if j <= i:
            continue
        c, d, o2 = segs[j]
        if o2 == o:
            continue
        if hor and abs(c[1] - d[1]) < 1e-9:
            gap = abs(a[1] - c[1])
            ov = min(max(a[0], b[0]), max(c[0], d[0])) - max(min(a[0], b[0]), min(c[0], d[0]))
        elif not hor and abs(c[0] - d[0]) < 1e-9:
            gap = abs(a[0] - c[0])
            ov = min(max(a[1], b[1]), max(c[1], d[1])) - max(min(a[1], b[1]), min(c[1], d[1]))
        else:
            continue
        if ov > 0.3 and gap < 3.0:
            if gap < 0.8 - 1e-6:
                under += 1
            if gap < best[0]:
                best = (gap, (o, o2, round(a[0], 1), round(a[1], 1)))
print("seed", seed, "A9 min centre distance between different owners:", round(best[0], 3),
      best[1], "pairs < 0.8 mm:", under)
