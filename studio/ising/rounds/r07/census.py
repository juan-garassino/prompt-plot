"""r07 census: for a given T_max (and NY), re-sample the r05 chain and measure
A18 on the lattice before drawing anything.

usage: .venv/bin/python studio/ising/rounds/r07/census.py T_MAX [NY] [CUT] [seeds...]

Columns are anchored on the field's right edge: col 0 = the last 25 mm, then
20 mm columns leftwards. A hull is counted in the column holding its centroid;
a column's MARKS are hulls with any edge inside it (for the <= 3 test).
"""
from __future__ import annotations

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))

import numpy as np  # noqa: E402

import piece as P  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402

PITCH = 249.8 / 212


def census(seed: int, t_hi: float, NY: int = 137, NX: int = 212, cut: int = 13, t_lo=0.70):
    rng = SeededRNG(seed)
    t0 = time.time()
    flat, sim, diag = P.simulate(rng, NY, NX, t_lo, t_hi, 40, 1500, 8)
    key = (rng.seed * 7919 + 17) & 0xFFFFFFFF
    root, fsz = P.fk_clusters(flat, sim, key, None)
    fsea, fout = P.fk_sea_outside(root, fsz, NY, NX)
    shore = P.hull_edges(fsea, fout, NY, NX)
    sx = [p[0] for p, q in shore if p[0] == q[0]]
    coast_mean = sim.tr_at(sum(sx) / len(sx))
    coast_max = sim.tr_at(max(sx))
    cl = P.droplet_loops(root, fsea, NY, NX, cut)
    W = NX * PITCH
    xr = lambda u: u * PITCH  # field-relative mm
    # column edges, right-anchored
    edges = [W, W - 25.0]
    while edges[-1] - 20.0 > 0:
        edges.append(edges[-1] - 20.0)
    edges.append(0.0)
    cols = list(zip(edges[1:], edges[:-1]))  # col 0 = last
    cnt = [0] * len(cols)
    marks0 = 0
    ink = np.zeros((NY, NX), bool)  # cell rows touched by any hull edge (lattice)
    for c in cl:
        x = xr(c["cx"])
        for k, (a, b) in enumerate(cols):
            if a <= x < b or (k == 0 and x >= b):
                cnt[k] += 1
                break
        xs = []
        for loop in c["loops"]:
            for s, e, _n, _c in loop:
                xs += [s[0], e[0]]
                for (u, v) in (s, e):
                    uu = min(NX - 1, max(0, int(u) - (1 if u == NX else 0)))
                    ink[int(v) % NY, min(NX - 1, int(u))] = True
                    ink[int(v) % NY, max(0, int(u) - 1)] = True
        if max(xs) * PITCH > W - 25.0:
            marks0 += 1
    # mark-free vertical run in the last 25 mm (full width)
    c0 = int(math.floor((W - 25.0) / PITCH))
    free_rows = ~ink[:, c0:].any(1)
    best = run = 0
    for f in np.concatenate([free_rows, free_rows]):  # wraps
        run = run + 1 if f else 0
        best = max(best, run)
    best = min(best, NY)
    free_mm = best * PITCH
    # from the column holding T=1.3 to the edge
    x13 = (1.3 - t_lo) / (t_hi - t_lo) * W
    k13 = next(k for k, (a, b) in enumerate(cols) if a <= x13 < b)
    seq = cnt[k13::-1]
    strict = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
    # band census (A14 bands scale with the axis: fixed T bounds)
    bands = [(1.00, 1.15), (1.15, 1.35), (1.35, 1.55), (1.55, 1.80)]
    extra = []
    tb = 1.80
    while tb < t_hi - 1e-9:
        nb = min(t_hi, tb + 0.35)
        extra.append((tb, nb))
        tb = nb
    bs = []
    for lo, hi in bands + extra:
        sel = [c for c in cl if lo <= sim.tr_at(c["cx"]) < hi]
        bs.append((lo, hi, len(sel), round(sum(c["size"] for c in sel) / max(1, len(sel)), 1)))
    sea_w = (coast_mean - t_lo) / (t_hi - t_lo) * W
    return {
        "seed": seed, "t_hi": t_hi, "NY": NY, "cut": cut, "secs": round(time.time() - t0, 1),
        "coast_mean": round(coast_mean, 3), "coast_max": round(coast_max, 3),
        "sea_to_coast_mm": round(sea_w, 1),
        "sea_to_coastmax_mm": round((coast_max - t_lo) / (t_hi - t_lo) * W, 1),
        "cols_left_to_right": cnt[::-1], "seq_from_1.3": seq, "strict": strict,
        "last_marks": marks0, "last_free_run_mm": round(free_mm, 1), "bands": bs,
        "rms": round(diag["rms"], 4),
    }


if __name__ == "__main__":
    t_hi = float(sys.argv[1])
    NY = int(sys.argv[2]) if len(sys.argv) > 2 else 137
    cut = int(sys.argv[3]) if len(sys.argv) > 3 else 13
    seeds = [int(a) for a in sys.argv[4:]] or [7, 3, 13]
    for s in seeds:
        print(census(s, t_hi, NY, cut=cut), flush=True)
