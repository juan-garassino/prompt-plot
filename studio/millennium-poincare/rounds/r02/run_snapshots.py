"""Copy of data/run_neckpinch.py for r02 (abstract): snapshots at EXACT target times.

    .venv/bin/python -W ignore studio/millennium-poincare/rounds/r02/run_snapshots.py

Encoding §4 (binding): isochrones at t = 0 and t_s + 0.01 k (Δt = 0.01 anchored at the
surgery instant t_s), never interpolated. The explicit solver of ricci_rot.py is used
unchanged; the ONLY difference from run_neckpinch.py is that a step which would overshoot
the next target time is shortened to land on it exactly (a shorter explicit step is always
inside the CFL bound). Pass 1 reproduces the reference step sequence to find t_s; pass 2
lands on every target, including t_s itself, where the surgery is done.

Writes snapshots.npz beside this file. Deterministic, pure numpy.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "..", "data")
sys.path.insert(0, DATA)
import dumbbell as D  # noqa: E402
from ricci_rot import rhs, step  # noqa: E402

N = 400
N_POST = 400
H_SURGERY = 0.12
DT_LINE = 0.01
N_HALO = 5


def neck_index(psi):
    c = psi[3:-3]
    m = (c <= psi[2:-4]) & (c <= psi[4:-2])
    if not m.any():
        return None
    idx = np.nonzero(m)[0]
    return int(idx[np.argmin(c[idx])] + 3)


def cap(psi_side, L_side, h):
    s = np.linspace(0, L_side, len(psi_side))
    sc = np.linspace(0, np.pi * h / 2, 200)[1:]
    psi_c = h * np.cos(sc / h)
    s_all = np.concatenate([s, L_side + sc])
    p_all = np.concatenate([psi_side, psi_c])
    Lnew = s_all[-1]
    return np.interp(np.linspace(0, Lnew, N_POST + 1), s_all, p_all), Lnew


def step_to(psi, L, n, t, t_target, cfl=0.2):
    """one explicit step, shortened if it would pass t_target (lands exactly)."""
    dpsi, Lt, ds = rhs(psi, L, n)
    pmin = np.min(psi[1:-1])
    dt = cfl * min(ds * ds, pmin * pmin)
    hit = False
    if t + dt >= t_target:
        dt = t_target - t
        hit = True
    return psi + dt * dpsi, L + dt * Lt, (t_target if hit else t + dt), hit


def pass1_ts():
    psi, L, _ = D.initial_profile(N)
    t = 0.0
    while True:
        psi, L, dt = step(psi, L, 2)
        t += dt
        i = neck_index(psi)
        if psi[i] <= H_SURGERY:
            return t


def main():
    ts = pass1_ts()
    print(f"pass1 t_s = {ts:.9f}", flush=True)
    snaps = []  # (tag, t_target, t_actual, psi, L)
    psi, L, _ = D.initial_profile(N)
    snaps.append(("start", 0.0, 0.0, psi.copy(), L))
    targets = [ts - DT_LINE * k for k in range(N_HALO, 0, -1)] + [ts]
    t = 0.0
    neck_track = []
    for tg in targets:
        hit = False
        while not hit:
            psi, L, t, hit = step_to(psi, L, 2, t, tg)
            i = neck_index(psi)
            neck_track.append((t, psi[i], psi[:i].max(), psi[i:].max(), L))
        tag = "key" if tg == ts else "halo"
        snaps.append((tag, tg, t, psi.copy(), L))
    i = neck_index(psi)
    ds = L / N
    s_cut = i * ds
    h = psi[i]
    left, Ll = cap(psi[: i + 1], s_cut, h)
    right, Lr = cap(psi[i:][::-1], L - s_cut, h)
    snaps.append(("A0", ts, ts, left.copy(), Ll))
    snaps.append(("B0", ts, ts, right.copy(), Lr))
    info = dict(t_s=ts, h_cut=h, s_cut=s_cut, L_key=L, i_cut=i)
    for tag, p, Lp in (("A", left, Ll), ("B", right, Lr)):
        t = ts
        k = 1
        hist = []
        tg = ts + DT_LINE * k
        while np.max(p) > 0.06:
            p, Lp, t, hit = step_to(p, Lp, 2, t, tg)
            hist.append((t, np.max(p), Lp))
            if hit:
                snaps.append((tag, tg, t, p.copy(), Lp))
                k += 1
                tg = ts + DT_LINE * k
        hh = np.array(hist)
        tail = hh[hh[:, 1] < 0.12]
        sl, ic = np.polyfit(tail[:, 0], tail[:, 1] ** 2, 1)
        T = -ic / sl
        # drop any snapshot after extinction or below the stop radius (none expected)
        info[f"T_ext_{tag}"] = T
        info[f"slope_{tag}"] = sl
        print(f"piece {tag}: T_ext = {T:.6f}  slope = {sl:.4f}  rings = {k - 1}", flush=True)
    for k, v in info.items():
        print(f"{k:>10s} = {v}")
    err = max(abs(s[1] - s[2]) for s in snaps)
    print("max |t_snap - t_target| =", err)
    np.savez(os.path.join(HERE, "snapshots.npz"),
             tag=np.array([s[0] for s in snaps]), t_target=np.array([s[1] for s in snaps]),
             t=np.array([s[2] for s in snaps]), L=np.array([s[4] for s in snaps]),
             psi=np.stack([s[3] for s in snaps]), neck_track=np.array(neck_track),
             **{k: np.float64(v) for k, v in info.items()})


if __name__ == "__main__":
    main()
