"""r07: the A18 fade in EXPECTATION. N independent chains (seeds 101..) of the
r07 geometry (212 x NY, T/Tc 0.70-1.80), each FK-drawn once; per cut report the
mean hull count in the art critic's 20 mm columns (x >= 182 mm, last = 25 mm),
P(strict decrease), P(last column <= 3 marks), P(mark-free run >= 60 mm).

usage: .venv/bin/python studio/ising/rounds/r07/ensemble.py NY N cuts
"""
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import census_cut as C  # noqa: E402
import piece as P  # noqa: E402


def one(args):
    seed, NY, cuts = args
    sim, root, fsea = C.sample(seed, NY)
    cl_all = P.droplet_loops(root, fsea, NY, 212, min(cuts))
    out = {}
    for cut in cuts:
        out[cut] = C.evaluate(sim, root, fsea, cut, NY, cl_all=cl_all)
    return seed, out


if __name__ == "__main__":
    NY, N = int(sys.argv[1]), int(sys.argv[2])
    cuts = [int(c) for c in sys.argv[3].split(",")]
    with ProcessPoolExecutor(8) as ex:
        res = list(ex.map(one, [(101 + k, NY, cuts) for k in range(N)]))
    for cut in cuts:
        seqs = [r[cut]["seq"][1:] for _s, r in res]  # columns from x 182 (T 1.34)
        n = len(seqs)
        mean = [round(sum(s[k] for s in seqs) / n, 2) for k in range(len(seqs[0]))]
        strict = sum(all(s[i] > s[i + 1] for i in range(len(s) - 1)) for s in seqs) / n
        noninc = sum(all(s[i] >= s[i + 1] for i in range(len(s) - 1)) for s in seqs) / n
        last3 = sum(r[cut]["last_marks"] <= 3 for _s, r in res) / n
        free = sum(r[cut]["free_mm"] >= 60 for _s, r in res) / n
        lastm = round(sum(r[cut]["last_marks"] for _s, r in res) / n, 2)
        bands = sum(
            r[cut]["bands"][1][0] > r[cut]["bands"][2][0] > r[cut]["bands"][3][0]
            and r[cut]["bands"][1][1] > r[cut]["bands"][2][1] > r[cut]["bands"][3][1]
            for _s, r in res) / n
        print(json.dumps({"cut": cut, "N": n, "mean_cols_x182_to_edge": mean,
                          "P_strict": round(strict, 3), "P_noninc": round(noninc, 3),
                          "mean_last_marks": lastm, "P_last<=3": round(last3, 3),
                          "P_free>=60": round(free, 3), "P_A14_bands": round(bands, 3)}),
              flush=True)
