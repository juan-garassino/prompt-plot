"""Gcode audit for millennium-hodge r02 (abstract).  Reads the rendered gcode and
checks the plate-level claims a science critic can re-run:

  1. every GOLD / BLUE stroke is straight (all points collinear within 0.01 mm)
  2. same-colour near-parallel spacing: minimum distance between two DIFFERENT
     strokes of one colour where they run within 21 deg of each other
     (|cos| > 0.93), excluding the X band (its own 5 passes are one mark)
  3. ink in the eye: no stroke of any colour enters the see-through channel
  4. per-layer draw length, strokes, and Leo time at F600 + 2.5 s/pen cycle

usage: .venv/bin/python studio/millennium-hodge/rounds/r02/audit.py <file.gcode>
(A3 design sheet only: checks 2-3 assume the A3 coordinates; check 4 holds on any paper)
"""
from __future__ import annotations

import importlib.util
import math
import re
import sys
from pathlib import Path

import numpy as np


def load(path):
    strokes, cur, col, pos = [], None, None, (0.0, 0.0)
    for ln in open(path):
        body = ln.split(";", 1)[0].strip()
        m = re.search(r"color=(\d+)", ln)
        if body.startswith("M3"):
            cur, col = [pos], int(m.group(1)) if m else col
        elif body.startswith("M5"):
            if cur and len(cur) > 1:
                strokes.append((col, np.array(cur)))
            cur = None
        elif body.startswith(("G0", "G1")):
            x = re.search(r"X([-\d.]+)", body)
            y = re.search(r"Y([-\d.]+)", body)
            pos = (float(x.group(1)) if x else pos[0], float(y.group(1)) if y else pos[1])
            if body.startswith("G1") and cur is not None:
                cur.append(pos)
    return strokes


def _seg_dist(q, a, b):
    ab = b - a
    t = np.clip(((q - a) @ ab) / max(ab @ ab, 1e-12), 0, 1)
    return float(np.linalg.norm(a + t * ab - q))


def main(path):
    st = load(path)
    spec = importlib.util.spec_from_file_location("pc", Path(__file__).with_name("piece.py"))
    m = importlib.util.module_from_spec(spec); sys.modules["pc"] = m; spec.loader.exec_module(m)
    view = m.View(**m.VIEW)
    xa = view.proj(m.string_A(view.a0, [-m.H, m.H]))
    xb = view.proj(m.string_B(view.a0, [-m.H, m.H]))
    m.hodge_circle_is_two_lines(None, (15, 15, 282, 405), 4)  # fills STATS (A3 design = paper)
    rb = m.STATS["rebus_box"]
    band = set()
    for k, (c, p) in enumerate(st):
        if c not in (0, 1, 2):
            continue
        in_rebus = all(rb[0] - 1 <= x <= rb[2] + 1 and rb[1] - 1 <= y <= rb[3] + 1 for x, y in p)
        on_x = c in (0, 1) and len(p) == 2 and all(
            min(_seg_dist(q, *xa), _seg_dist(q, *xb)) < 0.35 for q in p)
        if in_rebus or on_x:
            band.add(k)
    names = {0: "GOLD", 1: "BLUE", 2: "GREEN", 3: "TEXT"}
    # 1. straightness
    worst = 0.0
    for c, p in st:
        if c in (0, 1) and len(p) > 2:
            a, b = p[0], p[-1]
            d = (b - a) / max(np.linalg.norm(b - a), 1e-9)
            r = np.abs((p - a) @ np.array([-d[1], d[0]]))
            worst = max(worst, float(r.max()))
    n_multi = sum(1 for c, p in st if c in (0, 1) and len(p) > 2)
    print(f"1. straight: {n_multi} gold/blue strokes with >2 points; worst deviation {worst:.4f} mm")
    # pieces of ONE string (a paused-and-resumed string) are collinear: not a pair
    lines = {}
    for k, (c, p) in enumerate(st):
        if len(p) == 2:
            d = (p[1] - p[0]) / max(np.linalg.norm(p[1] - p[0]), 1e-9)
            nrm = np.array([-d[1], d[0]])
            lines[k] = (nrm, float(nrm @ p[0]))

    def same_line(i, j):
        if i not in lines or j not in lines:
            return False
        (n1, o1), (n2, o2) = lines[i], lines[j]
        dot = float(n1 @ n2)
        return abs(dot) > 0.99999 and abs(o1 - np.sign(dot) * o2) < 0.03

    # 2. near-parallel same-colour spacing (sampled at 0.25 mm)
    for c in (0, 1, 2):
        pts, tan, sid = [], [], []
        for k, (cc, p) in enumerate(st):
            if cc != c:
                continue
            for a, b in zip(p[:-1], p[1:]):
                L = float(np.linalg.norm(b - a))
                if L < 1e-9:
                    continue
                n = max(2, int(L / 0.25))
                t = np.linspace(0, 1, n)[:, None]
                pts.append(a + t * (b - a))
                tan.append(np.repeat(((b - a) / L)[None], n, 0))
                sid.append(np.full(n, k))
        P = np.concatenate(pts); T = np.concatenate(tan); S = np.concatenate(sid)
        cell = 1.0
        keys = np.floor(P / cell).astype(int)
        grid = {}
        for i, kk in enumerate(map(tuple, keys)):
            grid.setdefault(kk, []).append(i)
        dmin, where = 9.9, None
        # the X / rebus bands: strokes that have a parallel twin within 0.35 mm are band passes
        for i in range(0, len(P), 3):
            kx, ky = keys[i]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for j in grid.get((kx + dx, ky + dy), ()):
                        if S[j] == S[i] or (S[j] in band and S[i] in band) or same_line(S[i], S[j]):
                            continue
                        d = float(np.hypot(*(P[j] - P[i])))
                        if d < dmin and abs(float(T[i] @ T[j])) > 0.93:
                            dmin, where = d, tuple(np.round(P[i], 1))
        print(f"2. {names[c]}: min near-parallel gap between strokes (X / rebus band passes are one mark) "
              f"{dmin:.2f} mm at {where}")
    # 3. the eye: a sample is IN the eye if its sight-line, and those of its
    # four 0.3 mm neighbours, miss the clipped surface, near the throat.
    ink, where = 0, []
    for c, p in st:
        for a_, b_ in zip(p[:-1], p[1:]):
            n = max(2, int(np.linalg.norm(b_ - a_) / 0.2))
            q = a_ + np.linspace(0, 1, n)[:, None] * (b_ - a_)
            ok = view.sees_through(q[:, 0], q[:, 1]) & (np.hypot(q[:, 0] - view.cx, q[:, 1] - view.cy) < 70)
            for dx, dy in ((0.3, 0), (-0.3, 0), (0, 0.3), (0, -0.3)):
                ok &= view.sees_through(q[:, 0] + dx, q[:, 1] + dy)
            if ok.any():
                ink += int(ok.sum()); where.append((c, tuple(np.round(q[ok][0], 1))))
    X, Y = np.meshgrid(np.arange(view.cx - 70, view.cx + 70, 0.25), np.arange(view.cy - 70, view.cy + 70, 0.25))
    eye = view.sees_through(X, Y)
    seed = np.zeros_like(eye); seed[eye.shape[0] // 2, eye.shape[1] // 2] = True
    while True:
        nn = seed.copy()
        nn[1:] |= seed[:-1]; nn[:-1] |= seed[1:]; nn[:, 1:] |= seed[:, :-1]; nn[:, :-1] |= seed[:, 1:]
        nn &= eye
        if (nn == seed).all():
            break
        seed = nn
    pts = np.stack([X[seed], Y[seed]], 1)
    c0 = pts.mean(0); u, sv, vt = np.linalg.svd(pts - c0, full_matrices=False)
    pr = (pts - c0) @ vt.T
    print(f"3. eye: area {seed.sum() * 0.0625:.0f} mm^2, long {np.ptp(pr[:, 0]):.1f} x thick "
          f"{np.ptp(pr[:, 1]):.1f} mm; ink samples >0.3 mm inside the eye: {ink} {where[:6]}")
    # 4. budget
    tot = 0.0
    for c in (0, 1, 2, 3):
        L = sum(float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum()) for cc, p in st if cc == c)
        n = sum(1 for cc, p in st if cc == c)
        mins = (L / 10.0 + n * 2.5) / 60.0
        tot += mins
        print(f"4. {names[c]}: draw {L / 1000:.2f} m, {n} strokes, ~{mins:.1f} min")
    print(f"   total ~{tot:.0f} min")


if __name__ == "__main__":
    main(sys.argv[1])
