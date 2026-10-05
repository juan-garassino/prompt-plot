"""The real CNN — one honest forward pass and one honest backward pass, numpy only.

Nothing here is decorative. Every array this module returns is the arithmetic
result of the layer above it, and ``piece.py`` draws those arrays and nothing
else. ``summary()`` prints the statistics that make the claim checkable.

Shapes (all deterministic from the seed):

    X       24x24            radial double-chirp input
    W1      4 x 5 x 5        zero-mean Gabor wave filters
    A1      4 x 20 x 20      valid cross-correlation  X * W1
    R1      4 x 20 x 20      max(0, A1);  M1 = A1 > 0
    P1      4 x 10 x 10      2x2 max-pool + argmax routing
    W2      6 x 4 x 3 x 3    second-stage filters
    A2      6 x 8 x 8        valid cross-correlation  P1 * W2
    R2/M2   6 x 8 x 8        max(0, A2)
    P2      6 x 4 x 4        2x2 max-pool + argmax routing
    a       96               flatten(P2)
    Wc      96 x 6           linear classifier
    z, p    6                logits, softmax
    L       scalar           cross-entropy against one-hot target t

    dz      6                p - y
    dWc     96 x 6           outer(a, dz)
    da      96               Wc @ dz
    dP2     6 x 4 x 4
    dR2     6 x 8 x 8        unpool: one cell per 2x2 window (argmax only)
    dA2     6 x 8 x 8        dR2 * M2
    dW2     6 x 4 x 3 x 3
    dP1     4 x 10 x 10      full convolution with flipped W2
    dR1     4 x 20 x 20      unpool: one cell per 2x2 window (argmax only)
    dA1     4 x 20 x 20      dR1 * M1          <- the ReLU gate, visibly
    dW1     4 x 5 x 5        correlate(X, dA1)
    dX      24 x 24          full convolution with flipped W1
"""

from __future__ import annotations

import math
from typing import Dict

import numpy as np

NX = 24          # input side
K1 = 5           # conv-1 kernel side
C1 = 4           # conv-1 channels
K2 = 3           # conv-2 kernel side
C2 = 6           # conv-2 channels
NCLASS = 6
LOGIT_GAIN = 2.05   # LSUV-style init scale: z is normalised to this std


# ---------------------------------------------------------------------------
# primitive ops (all written out, no framework)
# ---------------------------------------------------------------------------
def corr2d(img: np.ndarray, ker: np.ndarray) -> np.ndarray:
    """Valid 2-D cross-correlation of a single plane with a single kernel."""
    kh, kw = ker.shape
    oh, ow = img.shape[0] - kh + 1, img.shape[1] - kw + 1
    out = np.zeros((oh, ow))
    for a in range(kh):
        for b in range(kw):
            out += ker[a, b] * img[a:a + oh, b:b + ow]
    return out


def full_conv2d(sig: np.ndarray, ker: np.ndarray) -> np.ndarray:
    """Full convolution (zero-padded, kernel flipped) — the adjoint of corr2d."""
    kh, kw = ker.shape
    pad = np.zeros((sig.shape[0] + 2 * (kh - 1), sig.shape[1] + 2 * (kw - 1)))
    pad[kh - 1:kh - 1 + sig.shape[0], kw - 1:kw - 1 + sig.shape[1]] = sig
    return corr2d(pad, ker[::-1, ::-1])


def maxpool2(x: np.ndarray):
    """2x2 max-pool a (C, H, W) stack. Returns (pooled, argmax offsets)."""
    c, h, w = x.shape
    blocks = x.reshape(c, h // 2, 2, w // 2, 2).transpose(0, 1, 3, 2, 4).reshape(c, h // 2, w // 2, 4)
    idx = blocks.argmax(axis=3)
    return blocks.max(axis=3), idx


def unpool2(g: np.ndarray, idx: np.ndarray, shape) -> np.ndarray:
    """Scatter each pooled gradient back to the ONE cell that won its window."""
    out = np.zeros(shape)
    c, ph, pw = g.shape
    for k in range(c):
        for j in range(ph):
            for i in range(pw):
                o = int(idx[k, j, i])
                out[k, 2 * j + o // 2, 2 * i + o % 2] = g[k, j, i]
    return out


def softmax(z: np.ndarray) -> np.ndarray:
    e = np.exp(z - z.max())
    return e / e.sum()


# ---------------------------------------------------------------------------
# the pass
# ---------------------------------------------------------------------------
def _input_plate() -> np.ndarray:
    """A radial double-chirp: concentric ripples whose frequency grows outward.

    Deterministic (no rng): it is the fixed stimulus the plate is a readout of.
    """
    t = (np.arange(NX) + 0.5) / NX * 2.0 - 1.0
    Xg, Yg = np.meshgrid(t, t)
    r1 = np.hypot(Xg + 0.10, Yg - 0.06)
    r2 = np.hypot(Xg - 0.62, Yg + 0.55)
    f = np.cos(2 * math.pi * (1.15 * r1 + 2.35 * r1 * r1)) * np.exp(-1.15 * r1 * r1)
    f += 0.55 * np.cos(2 * math.pi * (2.05 * r2)) * np.exp(-2.6 * r2 * r2)
    return f - f.mean()


def _gabor_bank() -> np.ndarray:
    """4 zero-mean oriented wave filters — 'kernels as wave filters', literally."""
    u = np.arange(K1) - (K1 - 1) / 2.0
    U, V = np.meshgrid(u, u)
    out = np.zeros((C1, K1, K1))
    for c in range(C1):
        th = math.pi * c / C1
        env = np.exp(-(U ** 2 + V ** 2) / (2 * 1.45 ** 2))
        wave = np.cos(2 * math.pi * 0.235 * (U * math.cos(th) + V * math.sin(th)) + 0.0)
        k = env * wave
        k -= k.mean()
        out[c] = k / np.abs(k).max()
    return out


def build(seed: int = 7) -> Dict[str, np.ndarray]:
    g = np.random.default_rng(seed)

    X = _input_plate()
    W1 = _gabor_bank()

    # ---- forward ----------------------------------------------------------
    A1 = np.stack([corr2d(X, W1[c]) for c in range(C1)])
    M1 = (A1 > 0).astype(float)
    R1 = A1 * M1
    P1, ix1 = maxpool2(R1)

    W2 = g.normal(0.0, 1.0, (C2, C1, K2, K2))
    W2 /= np.sqrt((W2 ** 2).sum(axis=(1, 2, 3)))[:, None, None, None]
    A2 = np.stack([sum(corr2d(P1[c], W2[k, c]) for c in range(C1)) for k in range(C2)])
    M2 = (A2 > 0).astype(float)
    R2 = A2 * M2
    P2, ix2 = maxpool2(R2)

    a = P2.reshape(-1)
    Wc_raw = g.normal(0.0, 1.0, (a.size, NCLASS))
    z_raw = a @ Wc_raw
    gain = LOGIT_GAIN / float(z_raw.std())          # init scale, fixed once
    Wc = Wc_raw * gain
    z = a @ Wc
    p = softmax(z)

    order = np.argsort(p)[::-1]
    win = int(order[0])
    target = int(order[1])                           # the plate draws a WRONG pass
    y = np.zeros(NCLASS)
    y[target] = 1.0
    L = float(-math.log(p[target]))

    # ---- backward ---------------------------------------------------------
    dz = p - y
    dWc = np.outer(a, dz)
    da = Wc @ dz
    dP2 = da.reshape(P2.shape)
    dR2 = unpool2(dP2, ix2, R2.shape)
    dA2 = dR2 * M2

    dW2 = np.zeros_like(W2)
    for k in range(C2):
        for c in range(C1):
            dW2[k, c] = corr2d(P1[c], dA2[k])
    dP1 = np.zeros_like(P1)
    for c in range(C1):
        dP1[c] = sum(full_conv2d(dA2[k], W2[k, c]) for k in range(C2))

    dR1 = unpool2(dP1, ix1, R1.shape)
    dA1 = dR1 * M1
    dW1 = np.stack([corr2d(X, dA1[c]) for c in range(C1)])
    dX = sum(full_conv2d(dA1[c], W1[c]) for c in range(C1))

    return dict(
        X=X, W1=W1, A1=A1, M1=M1, R1=R1, P1=P1, ix1=ix1,
        W2=W2, A2=A2, M2=M2, R2=R2, P2=P2, ix2=ix2,
        a=a, Wc=Wc, z=z, p=p, y=y, L=L, win=win, target=target,
        dz=dz, dWc=dWc, da=da, dP2=dP2, dR2=dR2, dA2=dA2,
        dW2=dW2, dP1=dP1, dR1=dR1, dA1=dA1, dW1=dW1, dX=dX,
    )


# ---------------------------------------------------------------------------
# provenance
# ---------------------------------------------------------------------------
def summary(n: Dict[str, np.ndarray]) -> str:
    """Human-checkable statistics for every array the plate draws."""
    L: list[str] = []
    w = L.append

    def st(name, A, extra=""):
        A = np.asarray(A)
        w(f"  {name:<10} {str(A.shape):<14} min {A.min():+9.4f}  max {A.max():+9.4f}  "
          f"mean {A.mean():+9.4f}  |.|sum {np.abs(A).sum():10.4f}  {extra}")

    w("FORWARD")
    st("X", n["X"])
    st("W1", n["W1"], f"per-kernel mean {np.round(n['W1'].mean(axis=(1,2)), 12).tolist()}")
    st("A1", n["A1"])
    st("R1", n["R1"], f"alive {int(n['M1'].sum())}/{n['M1'].size} = {n['M1'].mean():.3f}")
    st("P1", n["P1"])
    st("A2", n["A2"])
    st("P2", n["P2"], f"alive2 {int(n['M2'].sum())}/{n['M2'].size} = {n['M2'].mean():.3f}")
    st("z", n["z"])
    p = n["p"]
    w(f"  p          {np.round(p, 4).tolist()}   sum {p.sum():.6f}   "
      f"argmax {n['win']}  target {n['target']}  L = -log p[t] = {n['L']:.4f}")

    w("BACKWARD")
    dz = n["dz"]
    w(f"  dz = p - y {np.round(dz, 4).tolist()}   sum {dz.sum():+.2e} (must be ~0)")
    st("dWc", n["dWc"])
    st("dP2", n["dP2"])
    st("dR2", n["dR2"], f"nonzero {int((n['dR2'] != 0).sum())}/{n['dR2'].size} "
                        f"(unpool -> 1 per 2x2 window)")
    st("dA2", n["dA2"], f"nonzero {int((n['dA2'] != 0).sum())} after ReLU mask")
    st("dP1", n["dP1"])
    st("dR1", n["dR1"], f"nonzero {int((n['dR1'] != 0).sum())}/{n['dR1'].size} "
                        f"= {(n['dR1'] != 0).mean():.3f}")
    st("dA1", n["dA1"], f"nonzero {int((n['dA1'] != 0).sum())}  "
                        f"killed by the mask {int((n['dR1'] != 0).sum()) - int((n['dA1'] != 0).sum())}")
    st("dW1", n["dW1"])
    st("dX", n["dX"])

    w("GRADIENT CHECK (central differences, eps = 1e-5)")
    for line in _gradcheck():
        w("  " + line)
    return "\n".join(L)


def _gradcheck(seed: int = 7, eps: float = 1e-5) -> list:
    """Finite-difference check of dW1, dWc and dX against the analytic values."""
    base = build(seed)
    W1, Wc, X = base["W1"], base["Wc"], base["X"]
    target = base["target"]

    def loss(X_, W1_, Wc_):
        A1 = np.stack([corr2d(X_, W1_[c]) for c in range(C1)])
        R1 = np.maximum(A1, 0.0)
        P1, _ = maxpool2(R1)
        A2 = np.stack([sum(corr2d(P1[c], base["W2"][k, c]) for c in range(C1))
                       for k in range(C2)])
        P2, _ = maxpool2(np.maximum(A2, 0.0))
        pp = softmax(P2.reshape(-1) @ Wc_)
        return float(-math.log(pp[target]))

    out = []
    for name, arr, idx in (("dW1", W1, (1, 2, 3)), ("dWc", Wc, (40, 2)), ("dX", X, (11, 9))):
        A = arr.copy()
        A[idx] += eps
        lo_hi = loss(*( (A, W1, Wc) if name == "dX" else
                        (X, A, Wc) if name == "dW1" else (X, W1, A) ))
        A = arr.copy()
        A[idx] -= eps
        lo_lo = loss(*( (A, W1, Wc) if name == "dX" else
                        (X, A, Wc) if name == "dW1" else (X, W1, A) ))
        num = (lo_hi - lo_lo) / (2 * eps)
        ana = float(base[name][idx])
        rel = abs(num - ana) / max(1e-12, abs(num) + abs(ana))
        out.append(f"{name}{list(idx)}: analytic {ana:+.6f}  numeric {num:+.6f}  rel.err {rel:.2e}")
    return out


if __name__ == "__main__":
    print(summary(build(7)))
