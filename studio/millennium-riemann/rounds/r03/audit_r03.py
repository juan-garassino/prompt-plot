"""r03 audit: red single-pass overlap, right/left field ink, A-B minimum, type clearances.
usage: .venv/bin/python studio/millennium-riemann/rounds/r03/audit_r03.py"""
import importlib.util
import math
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location("p", Path(__file__).with_name("piece.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
L = P.build_layers()
NIB = 0.5


def dense(r, step=0.05):
    return P._dense(r, step)


# --- red: one-way strokes, overlap only at the centre ------------------------
red = [np.asarray(r) for r in L["red"]]
print("red strokes", len(red), "total m", round(sum(P.length(r.tolist()) for r in red) / 1000, 3))
cent = [np.array([P.X0, P.ty(g)]) for g in P.GAMMAS]
worst_self, worst_cross = 0.0, 0.0
retrace = 0
for c in cent:
    arms = [r for r in red if np.hypot(*(r.mean(0) - c)) < 3.0]
    assert len(arms) == 2, (c, len(arms))
    for a in arms:
        q = dense(a.tolist())
        s = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(q, axis=0).T))])
        D = np.hypot(q[:, None, 0] - q[None, :, 0], q[:, None, 1] - q[None, :, 1])
        S = np.abs(s[:, None] - s[None, :])
        bad = (D < NIB) & (S > 2 * NIB)  # the same arm comes back under its own nib
        worst_self = max(worst_self, float(S[bad].max()) if bad.any() else 0.0)
        retrace += int(bad.any())
    qa, qb = dense(arms[0].tolist()), dense(arms[1].tolist())
    D = np.hypot(qa[:, None, 0] - qb[None, :, 0], qa[:, None, 1] - qb[None, :, 1])
    near = qa[(D < NIB).any(1)]
    ext = float(np.hypot(*(near - c).T).max()) if len(near) else 0.0
    worst_cross = max(worst_cross, ext)
print("arms that re-enter their own nib:", retrace, "| worst:", round(worst_self, 3))
print("arm-vs-arm overlap reaches at most", round(worst_cross, 3), "mm from the centre (nib 0.5)")

# --- right/left ink, field layers only -----------------------------------------
def split_len(runs):
    lf = rt = 0.0
    for r in runs:
        q = dense(r, 0.1)
        m = (q[:-1] + q[1:]) / 2
        seg = np.hypot(*np.diff(q, axis=0).T)
        inf = (m[:, 1] >= P.Y_AX + 1e-6)
        lf += seg[(m[:, 0] < P.X0) & inf].sum()
        rt += seg[(m[:, 0] > P.X0) & inf].sum()
    return lf, rt


tl = tr = 0.0
for k in ("hair", "black", "red"):
    lf, rt = split_len(L[k])
    tl += lf
    tr += rt
    print(f"{k}: left {lf/1000:.2f} m right {rt/1000:.2f} m")
print(f"field right/left = {100*tr/tl:.2f} %  (axis excluded)")

# --- column never drawn: min |x-180| of hair/black away from red discs ---------
m = 1e9
for k in ("hair", "black"):
    for r in L[k]:
        q = dense(r, 0.05)
        d = np.abs(q[:, 0] - P.X0)
        m = min(m, float(d.min()))
print("hair/black closest approach to x=180 (crossings are the lone Gram lines, expected 0):", round(m, 3))
lo = min(float(np.asarray(r)[:, 1].min()) for r in L["red"])
print("lowest red y", round(lo, 2))
