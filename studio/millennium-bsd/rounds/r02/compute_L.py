"""Tabulate L(E,s) for 37a1 on [0, 2] (401 samples) -> l_samples.json (this round).

    .venv/bin/python studio/millennium-bsd/rounds/r02/compute_L.py

Uses the dossier's smoothed approximate functional equation with root number -1
(studio/millennium-bsd/data/lfun_lib.py; L'(1) = 0.3059997738 vs LMFDB
0.30599977383405). s = 0 is the trivial zero, taken as exactly 0.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "data"))
from lfun_lib import Lfun, upper_gamma  # noqa: E402

E = Lfun("37a1")
s = [2.0 * i / 400 for i in range(401)]
L = [0.0 if t == 0.0 else E.L(t, -1) for t in s]
Lp = float(2 * (E.A / E.n * upper_gamma(0.0, E.x)).sum())
out = {"curve": "37a1", "root_number": -1, "Lprime_1": Lp,
       "crossing_deg_equal_scale": math.degrees(math.atan(Lp)),
       "s": s, "L": L}
(HERE / "l_samples.json").write_text(json.dumps(out, indent=0))
print("L'(1) =", Lp, " L(1) =", L[200], " min", min(L), "at s", s[L.index(min(L))], " L(2) =", L[-1])
