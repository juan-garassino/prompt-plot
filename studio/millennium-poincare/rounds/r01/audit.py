"""Audit a faithful gcode: per-layer draw/travel/strokes/minutes, bounds, and the minimum
gap between DIFFERENT strokes of one layer (away from stroke ends, where lines land on a
card edge by design).  usage: audit.py file.gcode"""
import re
import sys

import numpy as np

strokes, cur, col, pos, down = [], None, None, (0.0, 0.0), False
travel = {}
for ln in open(sys.argv[1]):
    c = re.search(r"color=(\d+)", ln)
    if ln.startswith("M3"):
        down, col = True, int(c.group(1)) if c else col
        cur = [pos]
        continue
    if ln.startswith("M5"):
        if cur and len(cur) > 1:
            strokes.append((col, np.array(cur)))
        down, cur = False, None
        continue
    x = re.search(r"X([-\d.]+)", ln)
    y = re.search(r"Y([-\d.]+)", ln)
    if not x:
        continue
    p = (float(x.group(1)), float(y.group(1)))
    if ln.startswith("G1") and down:
        cur.append(p)
    elif ln.startswith("G0"):
        travel[col] = travel.get(col, 0.0) + float(np.hypot(p[0] - pos[0], p[1] - pos[1]))
    pos = p

allp = np.vstack([s for _, s in strokes])
print(f"bounds x {allp[:,0].min():.1f}..{allp[:,0].max():.1f}  y {allp[:,1].min():.1f}..{allp[:,1].max():.1f}")
tot_min = 0
for pen in sorted({c for c, _ in strokes}):
    S = [s for c, s in strokes if c == pen]
    L = sum(float(np.hypot(*np.diff(s, axis=0).T).sum()) for s in S)
    longest = max(float(np.hypot(*np.diff(s, axis=0).T).sum()) for s in S)
    mins = L / 10 / 60 + len(S) * 2.5 / 60 + travel.get(pen, 0) / 33 / 60
    tot_min += mins
    # min gap between different strokes, samples >= 1.5 mm from either stroke end
    pts, ids = [], []
    first = {}
    for k, s in enumerate(S):
        key = s.tobytes()
        sid = first.setdefault(key, k)           # an identical retrace shares its id
        seg = np.hypot(*np.diff(s, axis=0).T)
        cs = np.concatenate([[0], np.cumsum(seg)])
        u = np.arange(0, cs[-1], 0.2)
        q = np.column_stack([np.interp(u, cs, s[:, 0]), np.interp(u, cs, s[:, 1])])
        tg = np.gradient(q, axis=0) if len(q) > 2 else np.tile([1.0, 0.0], (len(q), 1))
        tg /= np.maximum(np.hypot(*tg.T), 1e-9)[:, None]
        keep = (u > 1.5) & (u < cs[-1] - 1.5)
        pts.append(np.hstack([q, tg])[keep]); ids.append(np.full(keep.sum(), sid))
    if not sum(len(q) for q in pts):
        print(f"pen {pen}: draw {L/1000:.2f} m  strokes {len(S)}  ≈ {mins:.1f} min")
        continue
    PT = np.vstack(pts); P = PT[:, :2]; T = PT[:, 2:]; I = np.concatenate(ids)
    cell = {}
    for i, (x, y) in enumerate(P):
        cell.setdefault((int(x // 1), int(y // 1)), []).append(i)
    gmin, where = 9e9, (0, 0)
    for (cx, cy), idx in cell.items():
        nb = [j for dx in (-1, 0, 1) for dy in (-1, 0, 1) for j in cell.get((cx + dx, cy + dy), [])]
        A = P[idx]; B = P[nb]
        d = np.hypot(A[:, None, 0] - B[None, :, 0], A[:, None, 1] - B[None, :, 1])
        same = I[idx][:, None] == I[nb][None, :]
        par = np.abs(T[idx] @ T[nb].T) > 0.94          # near-parallel runs only (crossings allowed)
        same |= ~par
        # identical retrace (keyline pass 2) is not a gap
        d[same | (d < 0.02)] = 9e9
        m = d.min()
        if m < gmin:
            gmin, where = m, tuple(A[np.unravel_index(d.argmin(), d.shape)[0]])
    print(f"pen {pen}: draw {L/1000:.2f} m  strokes {len(S)}  longest {longest:.0f} mm  "
          f"travel {travel.get(pen,0)/1000:.2f} m  ≈ {mins:.1f} min  min gap {gmin:.2f} mm at "
          f"({where[0]:.1f},{where[1]:.1f})")
print(f"total ≈ {tot_min:.0f} min (F600 draw, 2.5 s per lift+drop, travel 33 mm/s)")
