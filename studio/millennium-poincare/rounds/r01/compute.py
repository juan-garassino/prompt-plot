"""Isochrones for millennium-poincare r01 — the neckpinch solver re-run with snapshots at
EXACTLY the encoding's time grid (t = 0, t_s - 0.01k, t_s + 0.01k), not the npz's 0.005 grid.

    .venv/bin/python -W ignore studio/millennium-poincare/rounds/r01/compute.py

A copy of data/run_neckpinch.py's NECKPINCH -> SURGERY -> EXTINCTION path (the 2-D control
is not re-run; its numbers are read from data/neckpinch.npz for the footer). Same grid
(N = 400), same adaptive step, same surgery rule (cut when the neck reaches h = 0.12, cap
with round hemispheres), deterministic. Snapshot rule: every solver state is kept, and the
state whose time is NEAREST each target is the snapshot — no interpolation at all. The
largest |t_snap - t_target| is written to the output and must be < 1e-4.

Writes isochrones.npz beside this file.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data")
sys.path.insert(0, DATA)
import dumbbell as D  # noqa: E402
from ricci_rot import step  # noqa: E402
from run_neckpinch import H_SURGERY, N, cap, neck_index  # noqa: E402

DT = 0.01


def main():
    psi, L, _ = D.initial_profile(N)
    n = 2
    t = 0.0
    pre = [(0.0, psi.copy(), L)]
    while True:
        psi, L, dt = step(psi, L, n)
        t += dt
        pre.append((t, psi.copy(), L))
        i = neck_index(psi)
        if psi[i] <= H_SURGERY:
            break
    t_s, psi_s, L_s = t, psi.copy(), L
    i_s = neck_index(psi_s)
    pre_dt = np.diff([p[0] for p in pre])
    snaps = {"start": (0.0, 0.0, pre[0][1], pre[0][2]), "key": (t_s, t_s, psi_s, L_s)}
    tp = np.array([p[0] for p in pre])
    for k in range(1, 6):
        tt = t_s - DT * k
        j = int(np.argmin(np.abs(tp - tt)))
        snaps[f"past{k}"] = (tt, tp[j], pre[j][1], pre[j][2])
    # surgery: identical to run_neckpinch.main
    ds = L_s / N
    s_cut = i_s * ds
    left, Ll = cap(psi_s[: i_s + 1], s_cut, psi_s[i_s])
    right, Lr = cap(psi_s[i_s:][::-1], L_s - s_cut, psi_s[i_s])
    snaps["A0"] = (t_s, t_s, left.copy(), Ll)
    snaps["B0"] = (t_s, t_s, right.copy(), Lr)
    ext = {}
    maxdt = {}
    for tag, (p, Lp) in (("A", (left, Ll)), ("B", (right, Lr))):
        t = t_s
        k = 1
        prev = (t, p.copy(), Lp)
        hist = []
        while np.max(p) > 0.06:
            p, Lp, dt = step(p, Lp, n)
            t += dt
            hist.append((t, np.max(p)))
            tt = t_s + DT * k
            if t >= tt:
                pick = (t, p, Lp) if abs(t - tt) <= abs(prev[0] - tt) else prev
                snaps[f"{tag}{k}"] = (tt, pick[0], pick[1].copy(), pick[2])
                k += 1
            prev = (t, p.copy(), Lp)
            maxdt[tag] = max(maxdt.get(tag, 0.0), dt)
        h = np.array(hist)
        tail = h[h[:, 1] < 0.12]
        sl, ic = np.polyfit(tail[:, 0], tail[:, 1] ** 2, 1)
        ext[tag] = (-ic / sl, sl)
        # drop any ring at or after extinction (none expected: the loop stops at psi_max 0.06)
        for kk in list(snaps):
            if kk.startswith(tag) and kk[1:].isdigit() and snaps[kk][0] >= ext[tag][0]:
                del snaps[kk]
    names = list(snaps)
    err = max(abs(snaps[k][0] - snaps[k][1]) for k in names)
    np.savez(
        os.path.join(HERE, "isochrones.npz"),
        names=np.array(names),
        t_target=np.array([snaps[k][0] for k in names]),
        t_actual=np.array([snaps[k][1] for k in names]),
        L=np.array([snaps[k][3] for k in names]),
        psi=np.stack([np.interp(np.linspace(0, 1, 401), np.linspace(0, 1, len(snaps[k][2])),
                                snaps[k][2]) for k in names]),
        t_s=t_s, i_s=i_s, T_ext_A=ext["A"][0], T_ext_B=ext["B"][0],
        slope_A=ext["A"][1], slope_B=ext["B"][1], max_snap_err=err,
    )
    print(f"t_s = {t_s:.7f} (npz 0.0546465)   neck at t_s = {psi_s[i_s]:.5f}")
    print(f"pre-surgery solver dt: max {pre_dt.max():.2e}; post A/B max dt {maxdt}")
    print(f"T_ext A = {ext['A'][0]:.5f} (slope {ext['A'][1]:.3f})  B = {ext['B'][0]:.5f} "
          f"(slope {ext['B'][1]:.3f})")
    na = sum(1 for k in names if k[0] == "A" and k[1:].isdigit() and k != "A0")
    nb = sum(1 for k in names if k[0] == "B" and k[1:].isdigit() and k != "B0")
    print(f"rings: A {na}  B {nb}   max |t_snap - t_target| = {err:.2e}")


if __name__ == "__main__":
    main()
