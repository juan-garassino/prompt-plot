"""Acceptance checks for orrery r04, measured on the EMITTED gcode.

    .venv/bin/python studio/orrery/rounds/r04/checks.py ~/Downloads/pp_orrery_iterate_vN.gcode

Prints: per-layer strokes / draw / travel / minutes (Leo model: F500 draw,
F1800 travel, 1 s dwell per pen lift and per pen drop), in-layer hops > 60 mm,
blue strokes < 8 mm, blue-to-glyph clearance, and per-band science numbers
(envelope on the 3 o'clock ray, % drawn, parallel < 0.8 mm share).
"""

from __future__ import annotations

import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import piece  # noqa: E402

LEO_DRAW, LEO_TRAVEL, DWELL = 500.0, 1800.0, 1.0


def parse(path):
    strokes = []  # (color, [pts])
    cur = None
    pos = (0.0, 0.0)
    col = None
    down = False
    for line in open(os.path.expanduser(path)):
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        m = re.search(r"color=(\d+)", line)
        if m:
            col = int(m.group(1))
        cmd = line.split()[0]
        xy = dict(re.findall(r"([XY])(-?[\d.]+)", line))
        if cmd == "M3":
            down = True
            cur = [pos]
            strokes.append((col, cur))
        elif cmd == "M5":
            down = False
        elif cmd in ("G0", "G1") and xy:
            pos = (float(xy.get("X", pos[0])), float(xy.get("Y", pos[1])))
            if cmd == "G1" and down and cur is not None:
                cur.append(pos)
    return [(c, np.array(p)) for c, p in strokes if len(p) >= 2]


def plen(p):
    return float(np.hypot(*np.diff(p, axis=0).T).sum())


def main(path):
    S = parse(path)
    names = {0: "blue keys", 1: "crimson query", 2: "black type"}
    print("layer | strokes | draw m | travel m | max hop | hops>60 | minutes")
    tot_min = 0.0
    order = []
    for c, _ in S:
        if not order or order[-1] != c:
            order.append(c)
    print("layer order in file:", order)
    prev_end = (0.0, 0.0)
    for c in sorted(set(k for k, _ in S)):
        L = [p for k, p in S if k == c]
        draw = sum(plen(p) for p in L)
        hops = [float(np.hypot(*(L[i + 1][0] - L[i][-1]))) for i in range(len(L) - 1)]
        approach = float(np.hypot(*(L[0][0] - np.array(prev_end))))
        prev_end = L[-1][-1]
        trav = sum(hops) + approach
        mins = draw / LEO_DRAW + trav / LEO_TRAVEL + 2 * DWELL * len(L) / 60.0
        tot_min += mins
        big = [h for h in hops if h > 60]
        for i, h in enumerate(hops):
            if h > 40:
                print(f"   hop {h:.1f} mm  stroke {i}->{i+1}: {L[i][-1].round(1)} -> {L[i+1][0].round(1)}")
        print(f"{names.get(c, c)} | {len(L)} | {draw/1000:.2f} | {trav/1000:.2f} | "
              f"{max(hops) if hops else 0:.1f} | {len(big)} | {mins:.1f}  (approach {approach:.0f} mm)")
    print(f"total minutes ~{tot_min:.1f} (+ 2 pen swaps)")

    blue = [p for k, p in S if k == 0]
    short = [plen(p) for p in blue if plen(p) < 8.0]
    print("blue strokes < 8 mm:", len(short), short[:5])

    # glyphs: every black stroke + crimson strokes shorter than 25 mm (the question)
    glyph = np.vstack([p for k, p in S if k == 2] + [p for k, p in S if k == 1 and plen(p) < 25])
    bpts = np.vstack([resample(p, 0.2) for p in blue])
    dmin = nearest(bpts, glyph, 4.0)
    print(f"blue-to-glyph min clearance: {dmin:.2f} mm")

    # science per band
    LY = piece.layout()
    bands = LY["bands"]
    crim = [p for k, p in S if k == 1]
    sun = max(crim, key=lambda p: len(p))
    cx = 0.5 * (sun[:, 0].min() + sun[:, 0].max())
    cy = 0.5 * (sun[:, 1].min() + sun[:, 1].max())
    print(f"sun centre ({cx:.2f}, {cy:.2f}) diameter {sun[:,0].max()-sun[:,0].min():.2f}")
    per = {b["j"]: [] for b in bands}
    for p in blue:
        r = np.hypot(p[:, 0] - cx, p[:, 1] - cy).mean()
        b = min(bands, key=lambda b: abs(r - (b["R"] + 0.5 * b["s"])))
        per[b["j"]].append(p)
    print("tok | d | turns*d | n | s mm | env(3 o'clock) | env full | %drawn/turn | parallel<0.8")
    envs = {}
    for b in bands:
        ps = per[b["j"]]
        # 3 o'clock ray crossings
        rs = []
        for p in ps:
            for a, q in zip(p[:-1], p[1:]):
                if (a[1] - cy) * (q[1] - cy) <= 0 and a[0] > cx and a[1] != q[1]:
                    t = (cy - a[1]) / (q[1] - a[1])
                    rs.append(a[0] + t * (q[0] - a[0]) - cx)
        env = max(rs) - min(rs) if rs else float("nan")
        envs[b["tok"]] = env
        pct = []
        for p in ps:
            th = np.unwrap(np.arctan2(p[:, 1] - cy, p[:, 0] - cx))
            pct.append(abs(th[-1] - th[0]) / (2 * math.pi) * 100)
        par = parallel_share([resample(p, 0.15) for p in ps]) if b["s"] > 0 else float("nan")
        print(f"{b['tok']:12s} | {b['d']:.4f} | {2*b['d']:.3f} | {b['n']} | {b['s']:.2f} | "
              f"{env:.2f} | {b['outer']-b['inner']:.2f} | "
              f"{', '.join(f'{x:.1f}' for x in pct)} | {par*100:.1f}%")
    miss = {k: v for k, v in envs.items() if k != "transformer"}
    print(f"envelope ratio on the 3 o'clock ray: {max(miss.values())/min(miss.values()):.2f}")
    gaps = [(bands[i]["tok"], bands[i + 1]["inner"] - bands[i]["outer"]) for i in range(len(bands) - 1)]
    print("gaps >= 4 mm:", [(t, round(g, 2)) for t, g in gaps if g >= 4.0])


def resample(p, step):
    seg = np.hypot(*np.diff(p, axis=0).T)
    s = np.r_[0, np.cumsum(seg)]
    n = max(2, int(s[-1] / step))
    u = np.linspace(0, s[-1], n)
    return np.c_[np.interp(u, s, p[:, 0]), np.interp(u, s, p[:, 1])]


def nearest(P, Q, cap):
    cell = cap
    grid = {}
    for i, (a, b) in enumerate(np.floor(Q / cell).astype(int)):
        grid.setdefault((a, b), []).append(i)
    best = cap
    for n, (a, b) in enumerate(np.floor(P / cell).astype(int)):
        cand = []
        for da in (-1, 0, 1):
            for db in (-1, 0, 1):
                cand += grid.get((a + da, b + db), [])
        if cand:
            d = np.hypot(*(Q[cand] - P[n]).T).min()
            best = min(best, float(d))
    return best


def parallel_share(S, dmin=0.8, ang=25.0):
    tans = [np.arctan2(*np.gradient(P, axis=0).T[::-1]) for P in S]
    hits = tot = 0
    for i, P in enumerate(S):
        others = [j for j in range(len(S)) if j != i]
        if not others:
            continue
        Q = np.vstack([S[j] for j in others])
        T = np.concatenate([tans[j] for j in others])
        grid = {}
        for n, (a, b) in enumerate(np.floor(Q / dmin).astype(int)):
            grid.setdefault((a, b), []).append(n)
        for n, (a, b) in enumerate(np.floor(P / dmin).astype(int)):
            tot += 1
            cand = []
            for da in (-1, 0, 1):
                for db in (-1, 0, 1):
                    cand += grid.get((a + da, b + db), [])
            if not cand:
                continue
            cand = np.array(cand)
            ok = cand[np.hypot(*(Q[cand] - P[n]).T) < dmin]
            if len(ok) and (np.abs((T[ok] - tans[i][n] + np.pi / 2) % np.pi - np.pi / 2)
                            < math.radians(ang)).any():
                hits += 1
    return hits / max(tot, 1)


if __name__ == "__main__":
    main(sys.argv[1])
