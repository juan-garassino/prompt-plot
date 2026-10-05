"""Train the small LSTM whose gates drive r03 (forget-gate-vortex).

Run once, offline; the trained weights are baked into piece.py as constants and
piece.py re-runs the FORWARD pass live on its own sequence.  numpy only, exact
BPTT (checked against central differences below), Adam.

Task — THE ANALOG LATCH: remember the VALUE that arrived at the last WRITE.
  x_t = [v_t ~ U(-0.8, 0.8), write_t in {0,1}]    (a write at t=0 always)
  y_t = v at the most recent write <= t
A value arrives on EVERY step (distractors).  The values are analog, so a
bistable h-feedback loop cannot hold them (with {-1,+1} bits a 3-unit net
solved the task that way, f ~ 0.3-0.8, and never used the forget gate);
the only solution is to hold the cell (f ~ 1, i ~ 0) between writes and to
flush + rewrite it (f -> 0, i -> 1) on a write.  That is what the plate draws.

    .venv/bin/python studio/lstm-spirals/rounds/r03/train_lstm.py
"""
from __future__ import annotations

import sys

import numpy as np

import os
H, D, T, B = int(os.environ.get("LSTM_H", 1)), 2, int(os.environ.get("LSTM_T", 30)), 128
STEPS, LR, SEED = 8000, 0.01, 20260928
P_WRITE = 0.2


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def batch(rng, n=B, t_len=T):
    bits = rng.uniform(-0.8, 0.8, size=(n, t_len))
    wr = (rng.random((n, t_len)) < P_WRITE).astype(float)
    wr[:, 0] = 1.0
    y = np.zeros((n, t_len))
    cur = bits[:, 0].copy()
    for t in range(t_len):
        cur = np.where(wr[:, t] > 0, bits[:, t], cur)
        y[:, t] = cur
    return np.stack([bits, wr], -1), y


def forward(P, X):
    W, b, V, d = P["W"], P["b"], P["V"], P["d"]
    n, t_len, _ = X.shape
    h = np.zeros((n, H))
    c = np.zeros((n, H))
    cache = []
    ys = np.zeros((n, t_len))
    for t in range(t_len):
        xh = np.concatenate([X[:, t], h], 1)
        z = xh @ W + b
        i, f, o = sig(z[:, :H]), sig(z[:, H:2 * H]), sig(z[:, 2 * H:3 * H])
        g = np.tanh(z[:, 3 * H:])
        cp = c
        c = f * cp + i * g
        tc = np.tanh(c)
        h = o * tc
        ys[:, t] = h @ V + d[0]
        cache.append((xh, i, f, o, g, cp, c, tc, h))
    return ys, cache


def loss_grad(P, X, Y):
    n, t_len, _ = X.shape
    ys, cache = forward(P, X)
    err = ys - Y
    loss = float((err ** 2).mean())
    G = {k: np.zeros_like(v) for k, v in P.items()}
    dh_n = np.zeros((n, H))
    dc_n = np.zeros((n, H))
    for t in reversed(range(t_len)):
        xh, i, f, o, g, cp, c, tc, h = cache[t]
        dy = 2 * err[:, t] / (n * t_len)
        G["V"] += h.T @ dy
        G["d"] += dy.sum()
        dh = dy[:, None] * P["V"][None] + dh_n
        do = dh * tc
        dc = dh * o * (1 - tc ** 2) + dc_n
        df, di, dg = dc * cp, dc * g, dc * i
        dz = np.concatenate([di * i * (1 - i), df * f * (1 - f),
                             do * o * (1 - o), dg * (1 - g ** 2)], 1)
        G["W"] += xh.T @ dz
        G["b"] += dz.sum(0)
        dxh = dz @ P["W"].T
        dh_n = dxh[:, D:]
        dc_n = dc * f
    return loss, G, ys


def grad_check(P, rng):
    X, Y = batch(rng, n=4, t_len=6)
    _, G, _ = loss_grad(P, X, Y)
    worst = 0.0
    for k in P:
        flat = P[k].reshape(-1)
        for j in range(min(flat.size, 12)):
            old = flat[j]
            flat[j] = old + 1e-5
            lp, _, _ = loss_grad(P, X, Y)
            flat[j] = old - 1e-5
            lm, _, _ = loss_grad(P, X, Y)
            flat[j] = old
            num = (lp - lm) / 2e-5
            ana = G[k].reshape(-1)[j]
            worst = max(worst, abs(num - ana) / max(1e-8, abs(num) + abs(ana)))
    return worst


def train():
    rng = np.random.default_rng(SEED)
    P = {"W": rng.normal(0, 0.4, (D + H, 4 * H)), "b": np.zeros(4 * H),
         "V": rng.normal(0, 0.4, H), "d": np.zeros(1)}
    P["b"][H:2 * H] = 1.0  # forget bias 1 (Jozefowicz et al. 2015)
    print(f"BPTT grad-check max rel err at init: {grad_check(P, np.random.default_rng(1)):.2e}")
    m = {k: np.zeros_like(v) for k, v in P.items()}
    s = {k: np.zeros_like(v) for k, v in P.items()}
    for step in range(1, STEPS + 1):
        X, Y = batch(rng)
        loss, G, ys = loss_grad(P, X, Y)
        for k in P:
            m[k] = 0.9 * m[k] + 0.1 * G[k]
            s[k] = 0.999 * s[k] + 0.001 * G[k] ** 2
            P[k] -= LR * (m[k] / (1 - 0.9 ** step)) / (np.sqrt(s[k] / (1 - 0.999 ** step)) + 1e-8)
        if step % 1000 == 0:
            print(f"step {step:5d}  mse {loss:.5f}")
    return P


if __name__ == "__main__":
    P = train()
    for t_len in (20, 40):
        Xh, Yh = batch(np.random.default_rng(SEED + 1), n=2000, t_len=t_len)
        ys, _ = forward(P, Xh)
        print(f"held-out (2000 seqs, T={t_len}) mse {float(((ys - Yh) ** 2).mean()):.5f}"
              f"  (predict-zero baseline {float((Yh ** 2).mean()):.4f})")
    np.set_printoptions(precision=5, suppress=True, linewidth=140)
    np.savez(sys.argv[1] if len(sys.argv) > 1 else "/dev/null", **P)
    for k, v in P.items():
        print(k, "=", repr(np.round(v, 5).tolist()))
