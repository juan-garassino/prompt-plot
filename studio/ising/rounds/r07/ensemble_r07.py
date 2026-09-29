"""r07 ensemble for the PLATE geometry (212 x 129, T/Tc 0.70-2.30, cut 13):
what one configuration can and cannot promise about the A18 fade.

N independent chains (seeds 101..), each FK-drawn once, measured the way the
piece measures its own ink (columns right-anchored, last = 25 mm, outlines by
centroid; the art critic's run starts at x = 182 mm, the SYNTH's at T = 1.3).

usage: .venv/bin/python studio/ising/rounds/r07/ensemble_r07.py N
"""
from __future__ import annotations

import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import piece as P  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402

NX, NY, T_LO, T_HI, CUT = 212, 129, 0.70, 2.30, 13
PITCH = 249.8 / 212
W = NX * PITCH


def one(seed):
    rng = SeededRNG(seed)
    flat, sim, _ = P.simulate(rng, NY, NX, T_LO, T_HI, 40, 1500, 8)
    key = (rng.seed * 7919 + 17) & 0xFFFFFFFF
    root, fsz = P.fk_clusters(flat, sim, key, None)
    fsea, _fout = P.fk_sea_outside(root, fsz, NY, NX)
    cl = P.droplet_loops(root, fsea, NY, NX, CUT)
    edges = [W, W - 25.0]
    while edges[-1] - 20.0 > 0:
        edges.append(edges[-1] - 20.0)
    edges.append(0.0)
    cols = list(zip(edges[1:], edges[:-1]))
    cnt = [0] * len(cols)
    last = 0
    ink_rows = [False] * NY
    c0 = (W - 25.0) / PITCH
    for c in cl:
        x = c["cx"] * PITCH
        for k, (a, b) in enumerate(cols):
            if a <= x < b or (k == 0 and x >= b):
                cnt[k] += 1
                break
        hit = False
        for loop in c["loops"]:
            for s, e, _n, _c in loop:
                if max(s[0], e[0]) > c0:
                    hit = True
                    for v in (s[1], e[1]):
                        ink_rows[int(v) % NY] = True
                        ink_rows[(int(v) - 1) % NY] = True
        last += hit
    run = best = 0
    for f in [not r for r in ink_rows] * 2:
        run = run + 1 if f else 0
        best = max(best, run)
    x13 = (1.3 - T_LO) / (T_HI - T_LO) * W
    k13 = next(k for k, (a, b) in enumerate(cols) if a <= x13 < b)
    k182 = next(k for k, (a, b) in enumerate(cols) if a <= 182.0 - 36.8 < b)
    colsT = [j for j in range(NX) if sim.tr_at(j + 0.5) < 0.80]
    rows = list(range(1, NY, 3))
    dens = sum(fsea[i * NX + j] for i in rows for j in colsT) / (len(rows) * len(colsT))
    bands = [(1.00, 1.15), (1.15, 1.35), (1.35, 1.55), (1.55, 1.80), (1.80, 2.30)]
    bs = []
    for lo, hi in bands:
        sel = [c for c in cl if lo <= sim.tr_at(c["cx"]) < hi]
        bs.append((len(sel), sum(c["size"] for c in sel) / max(1, len(sel))))
    return {"seq13": cnt[k13::-1], "seq182": cnt[k182::-1], "last": last,
            "free_mm": min(best, NY) * PITCH, "dens": dens,
            "top": sum(c["size"] >= 155 for c in cl), "bands": bs}


def strict(s):
    return all(s[i] > s[i + 1] for i in range(len(s) - 1))


def strict_to_zero(s):  # strictly decreasing until it first reaches 0, then 0
    for i in range(len(s) - 1):
        if s[i] == 0:
            return all(v == 0 for v in s[i:])
        if not s[i] > s[i + 1]:
            return False
    return True


if __name__ == "__main__":
    N = int(sys.argv[1])
    with ProcessPoolExecutor(8) as ex:
        res = list(ex.map(one, [101 + k for k in range(N)]))
    n = len(res)
    out = {"N": n}
    for key in ("seq13", "seq182"):
        L = min(len(r[key]) for r in res)
        out[f"mean_{key}"] = [round(sum(r[key][i] for r in res) / n, 2) for i in range(L)]
        out[f"sd_{key}"] = [round(math.sqrt(sum((r[key][i] - out[f'mean_{key}'][i]) ** 2
                                               for r in res) / (n - 1)), 2) for i in range(L)]
        out[f"P_strict_{key}"] = round(sum(strict(r[key]) for r in res) / n, 3)
        out[f"P_strict_to_zero_{key}"] = round(sum(strict_to_zero(r[key]) for r in res) / n, 3)
    out["mean_last_marks"] = round(sum(r["last"] for r in res) / n, 2)
    out["P_last<=3"] = round(sum(r["last"] <= 3 for r in res) / n, 3)
    out["P_free>=60mm"] = round(sum(r["free_mm"] >= 60 for r in res) / n, 3)
    d = [r["dens"] for r in res]
    md = sum(d) / n
    out["held_070_080_mean"] = round(md, 4)
    out["held_070_080_sd"] = round(math.sqrt(sum((v - md) ** 2 for v in d) / (n - 1)), 4)
    out["P_top_rung>=1"] = round(sum(r["top"] >= 1 for r in res) / n, 3)
    out["mean_band_count"] = [round(sum(r["bands"][b][0] for r in res) / n, 1) for b in range(5)]
    out["mean_band_size"] = [round(sum(r["bands"][b][1] for r in res) / n, 1) for b in range(5)]
    out["P_count_peaks_past_Tc"] = round(sum(
        max(range(5), key=lambda b: r["bands"][b][0]) > 0 for r in res) / n, 3)
    out["P_weight_peaks_at_Tc"] = round(sum(
        max(range(5), key=lambda b: r["bands"][b][1]) == 0 for r in res) / n, 3)
    print(json.dumps(out, indent=1))
