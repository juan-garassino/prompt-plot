"""L(E,s) for 37a1 on s in [0,2] -> lcurve.json (this round's own data file).

    .venv/bin/python studio/millennium-bsd/rounds/r01/compute_l.py

Uses studio/millennium-bsd/data/lfun_lib.py (smoothed series, root number -1),
the dossier's verified evaluator. ~0.5 s per sample; 241 samples + 61 near s=1.
L(0) is set to exactly 0 (trivial zero: 1/Gamma(0) = 0).
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "data"))
from lfun_lib import Lfun  # noqa: E402

_E = None


def _L(s: float) -> float:
    global _E
    if _E is None:
        _E = Lfun("37a1")
    return 0.0 if s == 0.0 else float(_E.L(s, -1))


def main() -> None:
    s = sorted(set(np.round(np.linspace(0.0, 2.0, 241), 10).tolist()
                   + np.round(np.linspace(0.85, 1.15, 61), 10).tolist()))
    with ProcessPoolExecutor() as ex:
        v = list(ex.map(_L, s, chunksize=4))
    E = Lfun("37a1")
    d = (E.L(1.0005, -1) - E.L(0.9995, -1)) / 0.001
    out = {"curve": "37a1", "root_number": -1, "s": s, "L": v,
           "L_prime_1_fd": d, "source": "data/lfun_lib.py Lfun('37a1').L(s,-1)"}
    (HERE / "lcurve.json").write_text(json.dumps(out, indent=1))
    print(len(s), "samples; min", min(v), "L(2)", v[-1], "L'(1)", d)


if __name__ == "__main__":
    main()
