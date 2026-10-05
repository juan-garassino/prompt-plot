"""Gcode audit for r02: per-layer draw/travel, strokes, longest stroke, minutes at Leo F600
(+2.5 s per lift/drop), and the minimum gap between DIFFERENT strokes of the line layer
(identical retraced strokes -- the keyline x2 -- count once).

    .venv/bin/python studio/millennium-poincare/rounds/r02/audit.py file.gcode
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict

import numpy as np


def strokes(path):
    out = defaultdict(list)
    pos, cur, col = (0.0, 0.0), None, None
    travel = defaultdict(float)
    last_end = {}
    for ln in open(path):
        c = re.match(r"(G[01]|M3|M5)", ln)
        if not c:
            continue
        c = c.group(1)
        m = re.search(r"color=(\d+)", ln)
        if c == "M3":
            col = int(m.group(1)) if m else col
            cur = [pos]
            continue
        if c == "M5":
            if cur and len(cur) > 1:
                out[col].append(np.array(cur))
            cur = None
            continue
        xs, ys = re.search(r"X([-\d.]+)", ln), re.search(r"Y([-\d.]+)", ln)
        if not xs:
            continue
        p = (float(xs.group(1)), float(ys.group(1)))
        if c == "G1" and cur is not None:
            cur.append(p)
        elif c == "G0":
            if col is not None:
                travel[col] += float(np.hypot(p[0] - pos[0], p[1] - pos[1]))
        pos = p
    return out, travel


def dense(a, step=0.2):
    seg = np.hypot(*np.diff(a, axis=0).T)
    s = np.concatenate([[0], np.cumsum(seg)])
    u = np.linspace(0, s[-1], max(2, int(s[-1] / step) + 1))
    return np.column_stack([np.interp(u, s, a[:, 0]), np.interp(u, s, a[:, 1])])


def min_gap(strk, sep=0.8, cell=1.0):
    uniq, seen = [], set()
    for a in strk:
        key = a.round(3).tobytes()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(a)
    P, I = [], []
    for i, a in enumerate(uniq):
        d = dense(a)
        P.append(d)
        I.append(np.full(len(d), i))
    P, I = np.vstack(P), np.concatenate(I)
    grid = defaultdict(list)
    ij = np.floor(P / cell).astype(int)
    for k, (a, b) in enumerate(ij):
        grid[(a, b)].append(k)
    best, nbad = 1e9, 0
    where = None
    for k, (a, b) in enumerate(ij):
        cand = []
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                cand += grid.get((a + da, b + db), [])
        cand = np.array(cand)
        cand = cand[I[cand] != I[k]]
        if not len(cand):
            continue
        d = np.hypot(*(P[cand] - P[k]).T)
        j = int(np.argmin(d))
        if d[j] < best:
            best, where = float(d[j]), tuple(P[k].round(1))
        nbad += int((d < sep).any())
    return best, where, nbad, len(uniq)


if __name__ == "__main__":
    S, T = strokes(sys.argv[1])
    tot = 0.0
    for col in sorted(S):
        L = sum(float(np.hypot(*np.diff(a, axis=0).T).sum()) for a in S[col])
        lmax = max(float(np.hypot(*np.diff(a, axis=0).T).sum()) for a in S[col])
        mins = L / 10.0 / 60.0 + len(S[col]) * 2.5 / 60.0 + T[col] / 50.0 / 60.0
        tot += mins
        print(f"layer {col}: strokes {len(S[col])}  draw {L / 1000:.2f} m  travel {T[col] / 1000:.2f} m  "
              f"longest {lmax:.0f} mm  ~{mins:.1f} min")
    print(f"total ~{tot:.1f} min (F600 draw = 10 mm/s, 2.5 s per lift/drop, travel 50 mm/s)")
    b, w, n, u = min_gap(S[0])
    print(f"layer 0 min gap between different strokes: {b:.3f} mm at {w}; samples under 0.8: {n}; unique strokes {u}")
