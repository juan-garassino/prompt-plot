"""X-ray data for the ABSTRACT window (encoding §10, [A]).

    .venv/bin/python studio/millennium-riemann/rounds/r02/compute_abstract.py
    # optional cross-check against mpmath (not in .venv):
    PYTHONPATH=<scratch>/mplib .venv/bin/python studio/millennium-riemann/rounds/r02/compute_abstract.py --check

Grid: sigma in [-48, 31] step 0.05 (1581 columns); t on HALF-STEP rows 0.025 + 0.05k up to
98.025 (1961 rows), plus the conjugate row t = -0.025 (zeta(conj s) = conj zeta(s)), so the real
axis falls BETWEEN grid rows: s = 1 is never evaluated, and the Re zeta = 0 curves pass through the
axis at the trivial zeros cleanly (the piece crops at t = 0).
zeta: zeta_np.zeta (Euler-Maclaurin + functional equation, vectorised; see zeta_np.py), because
mpmath.fp.zeta at ~1 ms/point x 3.1 M points was hours on the shared machine. --check compares
4000 random window points with mpmath.zeta at dps 30 and prints the error and sign agreement.
Marching squares = contourpy (the engine under matplotlib.contour), level 0, no smoothing.
Writes xray_abstract.json NEXT TO THIS FILE (this round's own data; data/ is never touched).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from zeta_np import zeta  # noqa: E402

OUT = HERE / "xray_abstract.json"
S = np.round(np.arange(-48.0, 31.0 + 1e-9, 0.05), 4)
T = np.round(0.025 + 0.05 * np.arange(0, 1961), 4)


def check() -> dict:
    import mpmath as mp

    mp.mp.dps = 30
    rng = np.random.default_rng(1)
    s = rng.uniform(-48, 31, 4000) + 1j * rng.uniform(0.025, 98.025, 4000)
    z = zeta(s)
    ref = np.array([complex(mp.zeta(mp.mpc(x.real, x.imag))) for x in s])
    big = np.abs(ref) > 1e-8
    rel = np.abs(z - ref)[big] / np.abs(ref)[big]
    res = {"n": 4000, "max_rel_err": float(rel.max()), "median_rel_err": float(np.median(rel)),
           "sign_re_agree": float(np.mean(np.sign(z.real) == np.sign(ref.real))),
           "sign_im_agree": float(np.mean(np.sign(z.imag) == np.sign(ref.imag)))}
    print("check vs mpmath:", res, flush=True)
    return res


def main() -> None:
    chk = check() if "--check" in sys.argv else None
    t0 = time.time()
    X, Y = np.meshgrid(S, T)
    Z = np.empty(X.shape, dtype=complex)
    for i in range(0, len(T), 100):
        Z[i:i + 100] = zeta(X[i:i + 100] + 1j * Y[i:i + 100])
    print("grid", Z.shape, f"{time.time() - t0:.0f}s", flush=True)
    Zf = np.vstack([np.conj(Z[0:1]), Z])
    Tf = np.concatenate([[-0.025], T])
    import contourpy

    Xf, Yf = np.meshgrid(S, Tf)
    out = {}
    for key, F in (("re0", Zf.real), ("im0", Zf.imag)):
        lines = contourpy.contour_generator(Xf, Yf, F, line_type="Separate").lines(0.0)
        out[key] = [np.round(l, 4).tolist() for l in lines if len(l) > 1]
    OUT.write_text(json.dumps({
        "window": {"sigma": [-48, 31], "t": [-0.025, 98.025], "grid_step": 0.05,
                   "rows": "half-step 0.025+0.05k, plus conjugate row t=-0.025"},
        "method": "zeta_np.zeta (Euler-Maclaurin N=100 M=24 + functional equation) on the grid; "
                  "contourpy marching squares at level 0",
        "mpmath_check": chk, "re0": out["re0"], "im0": out["im0"]}))
    print("re0", len(out["re0"]), "im0", len(out["im0"]), "->", OUT)


if __name__ == "__main__":
    main()
