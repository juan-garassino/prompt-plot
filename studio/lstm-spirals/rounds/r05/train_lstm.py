"""Train the tiny character LSTM that `piece.py` runs forward at render time.

Offline, once, deterministic (numpy seed 20260928). Writes `lstm_weights.json`
beside this file. The plate then runs the REAL forward pass of these weights over
the proverb it draws -- nothing on the sheet is invented.

    .venv/bin/python studio/lstm-spirals/rounds/r04/train_lstm.py

Model: one LSTM layer, H hidden units, one-hot characters in, softmax out,
next-character prediction, full BPTT over whole lines (all lines in one masked batch), Adam. Standard gate
equations (the ones the plate is about):

    i = s(W_i [x, h] + b_i)   f = s(W_f [x, h] + b_f)   o = s(W_o [x, h] + b_o)
    g = tanh(W_g [x, h] + b_g)
    c_t = f * c_{t-1} + i * g          h_t = o * tanh(c_t)
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

VOCAB = " ABCDEFGHIJKLMNOPQRSTUVWXYZ."
TARGET = "THE PALEST INK IS BETTER THAN THE BEST MEMORY"

# A small corpus of sayings about memory and writing. The target proverb is in
# it on purpose: to predict "BEST" after the SECOND "THE " the cell has to still
# be carrying the fact that it is past "THAN" -- a long-range dependency the
# hidden state alone cannot hold.
CORPUS = [
    TARGET,
    "THE FAINTEST INK IS MORE POWERFUL THAN THE STRONGEST MEMORY",
    "THE BEST MEMORY IS NOT SO FIRM AS FADED INK",
    "WHAT IS WRITTEN REMAINS WHAT IS SPOKEN FLIES AWAY",
    "MEMORY IS THE TREASURY AND GUARDIAN OF ALL THINGS",
    "THE PEN IS THE TONGUE OF THE MIND",
    "TIME FLIES MEMORY FADES INK REMAINS",
    "THE PAST IS NEVER DEAD IT IS NOT EVEN PAST",
    "WHAT IS WELL WRITTEN IS NEVER FORGOTTEN",
    "THE PALEST INK OUTLASTS THE BRIGHTEST MIND",
    "A SHORT PENCIL IS BETTER THAN A LONG MEMORY",
    "THE MIND FORGETS WHAT THE HAND HAS WRITTEN LAST",
]

H = 8
V = len(VOCAB)
SEED = 20260928


def onehot(s):
    X = np.zeros((len(s), V))
    for t, ch in enumerate(s):
        X[t, VOCAB.index(ch)] = 1.0
    return X


def sig(z):
    return 1.0 / (1.0 + np.exp(-z))


def forward(P, X):
    """X: (T, V) or (T, B, V). Returns caches + logits (batched)."""
    W, b, Wy, by = P["W"], P["b"], P["Wy"], P["by"]
    if X.ndim == 2:
        X = X[:, None, :]
    T, B = X.shape[0], X.shape[1]
    h = np.zeros((B, H))
    c = np.zeros((B, H))
    cache = []
    logits = np.zeros((T, B, V))
    for t in range(T):
        z = np.concatenate([X[t], h], axis=1)
        a = z @ W.T + b
        i, f, o = sig(a[:, :H]), sig(a[:, H : 2 * H]), sig(a[:, 2 * H : 3 * H])
        g = np.tanh(a[:, 3 * H :])
        c_new = f * c + i * g
        tc = np.tanh(c_new)
        h_new = o * tc
        cache.append((z, i, f, o, g, c, c_new, tc, h_new))
        logits[t] = h_new @ Wy.T + by
        h, c = h_new, c_new
    return cache, logits


def loss_and_grads(P, X, Y, M=None):
    """Y: (T,) or (T, B) int targets; M: (T, B) mask (1 = real char)."""
    if X.ndim == 2:
        X, Y = X[:, None, :], Y[:, None]
    T, B = Y.shape
    if M is None:
        M = np.ones((T, B))
    cache, logits = forward(P, X)
    m = logits.max(2, keepdims=True)
    p = np.exp(logits - m)
    p /= p.sum(2, keepdims=True)
    tt, bb = np.meshgrid(np.arange(T), np.arange(B), indexing="ij")
    n = M.sum()
    loss = -np.sum(M * np.log(p[tt, bb, Y] + 1e-12)) / n
    dlog = p.copy()
    dlog[tt, bb, Y] -= 1.0
    dlog *= (M / n)[:, :, None]
    G = {k: np.zeros_like(v) for k, v in P.items()}
    dh_next = np.zeros((B, H))
    dc_next = np.zeros((B, H))
    for t in reversed(range(T)):
        z, i, f, o, g, c_prev, c_new, tc, h_new = cache[t]
        G["Wy"] += dlog[t].T @ h_new
        G["by"] += dlog[t].sum(0)
        dh = dlog[t] @ P["Wy"] + dh_next
        do = dh * tc
        dc = dh * o * (1 - tc * tc) + dc_next
        di = dc * g
        dg = dc * i
        df = dc * c_prev
        da = np.concatenate(
            [di * i * (1 - i), df * f * (1 - f), do * o * (1 - o), dg * (1 - g * g)], axis=1
        )
        G["W"] += da.T @ z
        G["b"] += da.sum(0)
        dz = da @ P["W"]
        dh_next = dz[:, V:]
        dc_next = dc * f
    return loss, G


def init(rng):
    s = 1.0 / math.sqrt(V + H)
    P = {
        "W": rng.normal(0, s, (4 * H, V + H)),
        "b": np.zeros(4 * H),
        "Wy": rng.normal(0, 1.0 / math.sqrt(H), (V, H)),
        "by": np.zeros(V),
    }
    P["b"][H : 2 * H] = 1.0  # forget-gate bias 1 (Gers et al.)
    return P


def gradcheck(P, X, Y, rng):
    _, G = loss_and_grads(P, X, Y)
    worst = 0.0
    for k in P:
        for _ in range(6):
            idx = tuple(rng.integers(0, n) for n in P[k].shape)
            old = P[k][idx]
            P[k][idx] = old + 1e-5
            lp, _ = loss_and_grads(P, X, Y)
            P[k][idx] = old - 1e-5
            lm, _ = loss_and_grads(P, X, Y)
            P[k][idx] = old
            num = (lp - lm) / 2e-5
            rel = abs(num - G[k][idx]) / max(1e-8, abs(num) + abs(G[k][idx]))
            worst = max(worst, rel)
    return worst


def main():
    rng = np.random.default_rng(SEED)
    P = init(rng)
    seqs = []
    for line in CORPUS:
        s = "." + line + "."
        seqs.append((onehot(s[:-1]), np.array([VOCAB.index(ch) for ch in s[1:]])))
    print("gradcheck worst rel err:", gradcheck(P, *seqs[0], rng))

    # one padded batch of every line; padding is masked out of the loss and
    # sits AFTER each line's end, so it never feeds back into a real step
    Tm = max(len(x) for x, _ in seqs)
    XB = np.zeros((Tm, len(seqs), V))
    YB = np.zeros((Tm, len(seqs)), dtype=int)
    MB = np.zeros((Tm, len(seqs)))
    for k, (x, y) in enumerate(seqs):
        XB[: len(x), k] = x
        YB[: len(y), k] = y
        MB[: len(y), k] = 1.0
    mom = {k: np.zeros_like(v) for k, v in P.items()}
    vel = {k: np.zeros_like(v) for k, v in P.items()}
    lr, b1, b2 = 0.02, 0.9, 0.999
    EPOCHS = 4000
    for step in range(1, EPOCHS + 1):
        loss, G = loss_and_grads(P, XB, YB, MB)
        for k in P:
            g = np.clip(G[k], -5, 5)
            mom[k] = b1 * mom[k] + (1 - b1) * g
            vel[k] = b2 * vel[k] + (1 - b2) * g * g
            mh = mom[k] / (1 - b1**step)
            vh = vel[k] / (1 - b2**step)
            P[k] -= lr * mh / (np.sqrt(vh) + 1e-8)
        if step % 250 == 0 or step == 1:
            print(f"step {step:5d}  corpus loss {loss:.3f} nats/char", flush=True)

    X, Y = seqs[0]
    cache, logits = forward(P, X)
    acc = float(np.mean(logits[:, 0].argmax(1) == Y))
    tloss, _ = loss_and_grads(P, X, Y)
    print(f"target proverb: loss {tloss:.3f} nats/char, next-char accuracy {acc:.3f}")
    out = {
        "vocab": VOCAB,
        "hidden": H,
        "target": TARGET,
        "corpus_lines": len(CORPUS),
        "seed": SEED,
        "adam_steps": EPOCHS,
        "target_loss_nats_per_char": round(float(tloss), 4),
        "target_next_char_accuracy": round(acc, 4),
        "W": np.round(P["W"], 6).tolist(),
        "b": np.round(P["b"], 6).tolist(),
        "Wy": np.round(P["Wy"], 6).tolist(),
        "by": np.round(P["by"], 6).tolist(),
    }
    (HERE / "lstm_weights.json").write_text(json.dumps(out))
    print("wrote", HERE / "lstm_weights.json")


if __name__ == "__main__":
    main()
