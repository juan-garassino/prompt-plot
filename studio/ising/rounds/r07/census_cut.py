"""r07 census for the FALLBACK lever: T/Tc 0.70-1.80 kept, the single fixed
hull cut raised. One sample per (seed, NY) is cached; every cut is evaluated
on the same FK draw.

usage: .venv/bin/python studio/ising/rounds/r07/census_cut.py NY cut1,cut2,.. [seeds...]
"""
from __future__ import annotations

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "../../../..")))

import numpy as np  # noqa: E402

import piece as P  # noqa: E402
from promptplot.generative.rng import SeededRNG  # noqa: E402

PITCH = 249.8 / 212
SCR = os.environ.get("CENSUS_CACHE", HERE)


def sample(seed, NY, NX=212, t_lo=0.70, t_hi=1.80):
    fn = os.path.join(SCR, f"cache_s{seed}_ny{NY}_t{t_hi:.2f}.npz")
    rng = SeededRNG(seed)
    if os.path.exists(fn):
        flat = [int(v) for v in np.load(fn)["flat"]]
        sim = P.GradientIsing(NY, NX, t_lo, t_hi, 0)
    else:
        flat, sim, _ = P.simulate(rng, NY, NX, t_lo, t_hi, 40, 1500, 8)
        np.savez_compressed(fn, flat=np.asarray(flat, np.int8))
    key = (rng.seed * 7919 + 17) & 0xFFFFFFFF
    root, fsz = P.fk_clusters(flat, sim, key, None)
    fsea, fout = P.fk_sea_outside(root, fsz, NY, NX)
    return sim, root, fsea


def evaluate(sim, root, fsea, cut, NY, NX=212, t_lo=0.70, t_hi=1.80, cl_all=None):
    cl = [c for c in (cl_all or P.droplet_loops(root, fsea, NY, NX, cut)) if c["size"] >= cut]
    W = NX * PITCH
    edges = [W, W - 25.0]
    while edges[-1] - 20.0 > 0:
        edges.append(edges[-1] - 20.0)
    edges.append(0.0)
    cols = list(zip(edges[1:], edges[:-1]))
    cnt = [0] * len(cols)
    marks0 = 0
    c0 = int(math.floor((W - 25.0) / PITCH))
    ink_rows = np.zeros(NY, bool)
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
        marks0 += hit
    best = run = 0
    for f in np.concatenate([~ink_rows, ~ink_rows]):
        run = run + 1 if f else 0
        best = max(best, run)
    free_mm = min(best, NY) * PITCH
    x13 = (1.3 - t_lo) / (t_hi - t_lo) * W
    k13 = next(k for k, (a, b) in enumerate(cols) if a <= x13 < b)
    seq = cnt[k13::-1]
    strict = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
    bands = [(1.00, 1.15), (1.15, 1.35), (1.35, 1.55), (1.55, 1.80)]
    bs = []
    for lo, hi in bands:
        sel = [c for c in cl if lo <= sim.tr_at(c["cx"]) < hi]
        bs.append((len(sel), round(sum(c["size"] for c in sel) / max(1, len(sel)), 1)))
    return {"cut": cut, "seq": seq, "strict": strict, "last_marks": marks0,
            "free_mm": round(free_mm, 1), "bands": bs, "n": len(cl)}


if __name__ == "__main__":
    NY = int(sys.argv[1])
    cuts = [int(c) for c in sys.argv[2].split(",")]
    seeds = [int(a) for a in sys.argv[3:]] or [7, 3, 13]
    for s in seeds:
        sim, root, fsea = sample(s, NY)
        cl_all = P.droplet_loops(root, fsea, NY, 212, min(cuts))
        for cut in cuts:
            r = evaluate(sim, root, fsea, cut, NY, cl_all=cl_all)
            print("seed", s, "NY", NY, r, flush=True)
