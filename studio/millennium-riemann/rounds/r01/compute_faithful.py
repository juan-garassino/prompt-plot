"""X-ray data for the FAITHFUL window (encoding §10). Needs mpmath (not in .venv):

    uv pip install --python .venv/bin/python --target <scratch>/mplib mpmath
    PYTHONPATH=<scratch>/mplib .venv/bin/python studio/millennium-riemann/rounds/r01/compute_faithful.py <scratch>

Grid: sigma in [-46, 47] step 0.05; t on HALF-STEP rows 0.025 + 0.05k up to 54.025, then mirrored
t -> -t by conjugate symmetry (zeta(conj s) = conj zeta(s)), so the real axis falls BETWEEN grid
rows: marching squares traces the real axis (Im zeta = 0) as a genuine line, the Re zeta = 0 curves
pass straight through it at the trivial zeros as single strokes, and s = 1 is never evaluated.
Writes studio/millennium-riemann/data/xray_faithful.json (new file, never overwrites).
"""
from __future__ import annotations

import json
import sys
from multiprocessing import Pool
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "data" / "xray_faithful.json"
S = np.round(np.arange(-46.0, 47.0 + 1e-9, 0.05), 4)
T = np.round(0.025 + 0.05 * np.arange(0, 1081), 4)


def _row(t: float) -> np.ndarray:
    return np.array([mp.fp.zeta(complex(s, t)) for s in S], dtype=complex)


def main() -> None:
    scratch = Path(sys.argv[1])
    raw = scratch / "zeta_faithful_grid.npy"
    if raw.exists():
        Z = np.load(raw)
    else:
        with Pool(8) as p:
            Z = np.array(p.map(_row, T, chunksize=4))
        np.save(raw, Z)
    Zf = np.vstack([np.conj(Z[::-1]), Z])          # t from -54.025 .. 54.025
    Tf = np.concatenate([-T[::-1], T])
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    X, Y = np.meshgrid(S, Tf)
    re0 = plt.contour(X, Y, Zf.real, [0]).allsegs[0]
    im0 = plt.contour(X, Y, Zf.imag, [0]).allsegs[0]
    rnd = lambda ps: [np.round(p, 4).tolist() for p in ps if len(p) > 1]
    if OUT.exists():
        raise SystemExit(f"{OUT} exists — refusing to overwrite")
    OUT.write_text(json.dumps(
        {"window": {"sigma": [-46, 47], "t": [-54.025, 54.025], "grid_step": 0.05,
                    "t_rows": "half-step (0.025 + 0.05k), mirrored by conjugate symmetry"},
         "source": "mpmath.fp.zeta, matplotlib marching squares, level 0",
         "re0": rnd(re0), "im0": rnd(im0)}))
    print("re0", len(re0), "im0", len(im0), "->", OUT)


if __name__ == "__main__":
    main()
