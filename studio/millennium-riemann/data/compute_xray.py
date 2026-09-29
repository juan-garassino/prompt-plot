"""Exact data for millennium-riemann (dossier §3). Needs mpmath, which is NOT in .venv:

    uv pip install --python .venv/bin/python --target /tmp/mplib mpmath
    PYTHONPATH=/tmp/mplib .venv/bin/python studio/millennium-riemann/data/compute_xray.py

Writes, next to this file:
  zeros.json          first 100 nontrivial zeros rho_n = 1/2 + i*gamma_n (mpmath.zetazero, 20 digits),
                      |zeta'(rho)|, arg zeta'(rho) in degrees, and the Gram / half-Gram points to t=102
  xray_contours.json  the X-RAY (Arias de Reyna 2003): polylines of Re zeta = 0 ("re0") and
                      Im zeta = 0 ("im0") on sigma in [-16, 12], t in [0, 102], complex-plane units.
                      Lower half-plane = mirror t -> -t (zeta(conj s) = conj zeta(s)); the real axis
                      itself (t = 0, s != 1) is also an Im zeta = 0 line and is NOT in the polylines.
"""
from __future__ import annotations

import json
from multiprocessing import Pool
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).parent
S = np.round(np.arange(-16.0, 12.0 + 1e-9, 0.05), 4)
T = np.round(np.arange(0.0, 102.0 + 1e-9, 0.05), 4)


def _row(t: float) -> list[complex]:
    return [complex("nan") if (s == 1.0 and t == 0.0) else mp.fp.zeta(complex(s, t)) for s in S]


def main() -> None:
    mp.mp.dps = 20
    zeros = []
    for n in range(1, 101):
        r = mp.zetazero(n)
        d = mp.zeta(r, derivative=1)
        zeros.append({"n": n, "gamma": float(r.imag), "gamma_str": mp.nstr(r.imag, 15),
                      "abs_dzeta": float(abs(d)), "arg_dzeta_deg": float(mp.degrees(mp.arg(d)))})
    gram = [float(mp.grampoint(n)) for n in range(-1, 40) if mp.grampoint(n) < 102]
    half = []
    for n in range(-1, 40):
        g = float(mp.findroot(lambda t: mp.siegeltheta(t) - (n + 0.5) * mp.pi, float(mp.grampoint(n)) + 1))
        if g < 102:
            half.append(g)
    (HERE / "zeros.json").write_text(json.dumps(
        {"source": "mpmath.zetazero (Odlyzko/LMFDB-consistent), dps=20", "zeros": zeros,
         "gram_points_theta_eq_n_pi": gram, "half_gram_theta_eq_n_plus_half_pi": half}, indent=1))

    with Pool(8) as p:
        Z = np.array(p.map(_row, T))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    X, Y = np.meshgrid(S, T)
    re0 = plt.contour(X, Y, Z.real, [0]).allsegs[0]
    im0 = plt.contour(X, Y, Z.imag, [0]).allsegs[0]
    rnd = lambda ps: [np.round(p, 4).tolist() for p in ps if len(p) > 1]
    (HERE / "xray_contours.json").write_text(json.dumps(
        {"window": {"sigma": [-16, 12], "t": [0, 102], "grid_step": 0.05},
         "re0": rnd(re0), "im0": rnd(im0)}))
    print("zeros", len(zeros), "re0", len(re0), "im0", len(im0))


if __name__ == "__main__":
    main()
