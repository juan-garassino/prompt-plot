"""Train the tiny LSTM whose gates drive r02 (offline, run once; weights are
baked into piece.py as constants).  numpy only, exact BPTT, Adam.

Task — the LATCH ("remember the bit at the last WRITE"):
  inputs  x_t = [bit_t in {-1,+1}, write_t in {0,1}]
  target  y_t = bit at the most recent write step <= t   (a write at t=0 always)
Bits keep arriving on every step (distractors); only a write should change
the memory.  The trained cell has to hold (f ~ 1) between writes and let go
(f -> 0) on a write — which is exactly the mechanism the plate draws.

    .venv/bin/python studio/lstm-spirals/rounds/r02/train_lstm.py
"""
from __future__ import annotations

import numpy as np

H, D, T, B = 4, 2, 16, 128
STEPS, LR, SEED = 5000, 0.01, 20260928


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def batch(rng):
    bits = rng.choice([-1.0, 1.0], size=(B, T))
    wr = (rng.random((B, T)) < 0.18).astype(float)
    wr[:, 0] = 1.0
    y = np.zeros((B, T))
    cur = bits[:, 0].copy()
    for t in range(T):
        cur = np.where(wr[:, t] > 0, bits[:, t], cur)
        y[:, t] = cur
    return np.stack([bits, wr], -1), y


def forward(P, X):
    W, b, V, d = P["W"], P["b"], P["V"], P["d"]
    Bn, Tn, _ = X.shape
    h = np.zeros((Bn, H)); c = np.zeros((Bn, H))
    cache = []
    ys = np.zeros((Bn, Tn))
    for t in range(Tn):
        xh = np.concatenate([X[:, t], h], 1)
        z = xh @ W + b
        i, f, o = sig(z[:, :H]), sig(z[:, H:2*H]), sig(z[:, 2*H:3*H])
        g = np.tanh(z[:, 3*H:])
        cp = c
        c = f * cp + i * g
        tc = np.tanh(c)
        h = o * tc
        ys[:, t] = h @ V + d
        cache.append((xh, i, f, o, g, cp, c, tc, h))
    return ys, cache


def train():
    rng = np.random.default_rng(SEED)
    P = {"W": rng.normal(0, 0.4, (D + H, 4 * H)), "b": np.zeros(4 * H),
         "V": rng.normal(0, 0.4, H), "d": np.zeros(1)}
    P["b"][H:2*H] = 1.0  # forget-bias 1 (Jozefowicz et al. 2015)
    m = {k: np.zeros_like(v) for k, v in P.items()}
    s = {k: np.zeros_like(v) for k, v in P.items()}
    for step in range(1, STEPS + 1):
        X, Y = batch(rng)
        ys, cache = forward(P, X)
        err = ys - Y
        loss = float((err ** 2).mean())
        G = {k: np.zeros_like(v) for k, v in P.items()}
        dh_n = np.zeros((B, H)); dc_n = np.zeros((B, H))
        for t in reversed(range(T)):
            xh, i, f, o, g, cp, c, tc, h = cache[t]
            dy = 2 * err[:, t] / (B * T)
            G["V"] += h.T @ dy; G["d"] += dy.sum()
            dh = dy[:, None] * P["V"][None] + dh_n
            do = dh * tc
            dc = dh * o * (1 - tc ** 2) + dc_n
            df, di, dg = dc * cp, dc * g, dc * i
            dz = np.concatenate([di * i * (1 - i), df * f * (1 - f),
                                 do * o * (1 - o), dg * (1 - g ** 2)], 1)
            G["W"] += xh.T @ dz; G["b"] += dz.sum(0)
            dxh = dz @ P["W"].T
            dh_n = dxh[:, D:]; dc_n = dc * f
        for k in P:
            m[k] = 0.9 * m[k] + 0.1 * G[k]
            s[k] = 0.999 * s[k] + 0.001 * G[k] ** 2
            P[k] -= LR * (m[k] / (1 - 0.9 ** step)) / (np.sqrt(s[k] / (1 - 0.999 ** step)) + 1e-8)
        if step % 500 == 0:
            acc = float((np.sign(ys) == Y).mean())
            print(f"step {step:5d}  mse {loss:.4f}  sign-acc {acc:.4f}")
    return P


if __name__ == "__main__":
    P = train()
    # held-out check on fresh sequences at the training length
    Xh, Yh = batch(np.random.default_rng(SEED + 1))
    ys, _ = forward(P, Xh)
    print("held-out sign-acc", float((np.sign(ys) == Yh).mean()), "mse", float(((ys - Yh) ** 2).mean()))
    np.set_printoptions(precision=5, suppress=True)
    for k, v in P.items():
        print(k, "=", repr(np.round(v, 5).tolist()))
