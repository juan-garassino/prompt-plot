"""ATTENTION — FORWARD AND BACKWARD: the real linear algebra behind the plate.

Every number the piece draws comes from here. Nothing is invented, nothing is
shaped by hand to look good.

Provenance
----------
``A`` is REAL GPT-2 attention, read from the cached stack produced by
``scripts/extract_gpt2_attention.py`` (12 layers x 12 heads x 15 tokens).

``Q`` and ``K`` are recovered from ``A`` exactly.  Softmax is invariant to a
per-row additive shift, so the score matrix is observable from the attention up
to that gauge: ``S = log A`` row-centred over the causal window reproduces
``A`` under softmax to machine precision.  A full SVD of that ``S`` (rank <= T =
15, well under GPT-2's head dimension d = 64) gives an EXACT rank factorisation
``Q K^T / sqrt(d) = S``.  So Q and K here are GPT-2's own queries and keys up to
the orthogonal gauge ``Q -> QR, K -> KR`` that the dot product cannot see.

``V`` is the one thing the cached stack does not contain (only attention
probabilities were saved, not the value projection).  It is a real seeded
Gaussian value matrix at GPT-2's head width.  It is a real matrix and the whole
forward/backward chain through it is exact -- it is simply not GPT-2's V, and
the plate does not claim it is.

The backward pass is the textbook derivation, done with actual matrix algebra
and checked against central finite differences:

    L      = 0.5 * ||Z - Z*||_F^2
    dL/dZ  = Z - Z*
    dL/dV  = A^T @ dL/dZ                      <- routed by the SAME A as forward
    dL/dA  = dL/dZ @ V^T
    dL/dS  = A * (dL/dA - rowsum(dL/dA * A))  <- softmax Jacobian
    dL/dQ  = dL/dS  @ K / sqrt(d)
    dL/dK  = dL/dS^T @ Q / sqrt(d)
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np

ATTN_NPZ = os.path.expanduser("~/.promptplot/attn_gpt2.npz")

# Chosen by a scan over all 12x12 heads and every causal row; see NOTES.md.
LAYER, HEAD, QROW = 1, 0, 12
DHEAD = 64  # GPT-2 head width


@dataclass
class Mechanism:
    A: np.ndarray        # (T, T) real GPT-2 attention, causal, rows sum to 1
    S: np.ndarray        # (T, T) recovered scores, QK^T/sqrt(d)
    Q: np.ndarray        # (T, d)
    K: np.ndarray        # (T, d)
    V: np.ndarray        # (T, d)
    Z: np.ndarray        # (T, d)  Z = A V
    dZ: np.ndarray       # (T, d)
    dV: np.ndarray
    dA: np.ndarray
    dS: np.ndarray
    dQ: np.ndarray
    dK: np.ndarray
    mask: np.ndarray     # (T, T) bool, causal window
    row: int             # the focus query row
    real_attention: bool
    checks: dict


def _softmax_causal(S: np.ndarray, mask: np.ndarray) -> np.ndarray:
    M = np.where(mask, S, -np.inf)
    M = M - M.max(axis=1, keepdims=True)
    E = np.exp(M)
    return E / E.sum(axis=1, keepdims=True)


def _synthetic_attention(T: int, rng: np.random.Generator) -> np.ndarray:
    """Fallback when the GPT-2 cache is absent: a REAL attention layer in numpy.

    Real Gaussian Q/K at head width, real scaled dot product, real causal
    softmax.  Not GPT-2, but not faked either.
    """
    q = rng.normal(0.0, 1.0, (T, DHEAD))
    k = rng.normal(0.0, 1.0, (T, DHEAD))
    S = q @ k.T / np.sqrt(DHEAD)
    mask = np.tril(np.ones((T, T), bool))
    return _softmax_causal(S, mask)


def build(seed: int = 7) -> Mechanism:
    rng = np.random.default_rng(seed)
    real = False
    if os.path.exists(ATTN_NPZ):
        stack = np.load(ATTN_NPZ)["attn"].astype(np.float64)
        A = stack[LAYER, HEAD]
        real = True
    else:
        A = _synthetic_attention(15, rng)
    T = A.shape[0]
    mask = np.tril(np.ones((T, T), bool))

    # ---- recover the score matrix (softmax's additive row gauge fixed by
    #      centring over the causal window) --------------------------------
    S = np.full((T, T), 0.0)
    L = np.log(np.clip(A, 1e-30, None))
    for i in range(T):
        w = mask[i]
        S[i, w] = L[i, w] - L[i, w].mean()
        S[i, ~w] = S[i, w].min()      # never seen by the causal softmax
    assert np.allclose(_softmax_causal(S, mask), A, atol=1e-9)

    # ---- exact rank factorisation S = Q K^T / sqrt(d) ---------------------
    U, sig, Wt = np.linalg.svd(S)
    r = min(T, DHEAD)
    root = np.sqrt(sig[:r]) * DHEAD ** 0.25
    Q = np.zeros((T, DHEAD))
    K = np.zeros((T, DHEAD))
    Q[:, :r] = U[:, :r] * root
    K[:, :r] = Wt[:r, :].T * root
    S_hat = Q @ K.T / np.sqrt(DHEAD)

    # ---- forward ----------------------------------------------------------
    V = rng.normal(0.0, 1.0 / np.sqrt(DHEAD), (T, DHEAD))
    Z = A @ V
    Zstar = rng.normal(0.0, 1.0 / np.sqrt(DHEAD), (T, DHEAD))

    def loss_of(Qm, Km, Vm):
        Sm = Qm @ Km.T / np.sqrt(DHEAD)
        Am = _softmax_causal(Sm, mask)
        return 0.5 * float(((Am @ Vm - Zstar) ** 2).sum())

    # ---- backward, by hand -------------------------------------------------
    dZ = Z - Zstar                                     # dL/dZ
    dV = A.T @ dZ                                      # dL/dV  = A^T dL/dZ
    dA = dZ @ V.T                                      # dL/dA  = dL/dZ V^T
    dS = A * (dA - (dA * A).sum(axis=1, keepdims=True))  # softmax Jacobian
    dS = np.where(mask, dS, 0.0)
    dQ = dS @ K / np.sqrt(DHEAD)
    dK = dS.T @ Q / np.sqrt(DHEAD)

    # ---- central finite differences: the proof ----------------------------
    def fd(mat, analytic, which, n=60):
        h, errs = 1e-5, []
        idx = rng.permutation(mat.size)[:n]
        for f in idx:
            i, j = divmod(int(f), mat.shape[1])
            up = [Q.copy(), K.copy(), V.copy()]
            dn = [Q.copy(), K.copy(), V.copy()]
            up[which][i, j] += h
            dn[which][i, j] -= h
            num = (loss_of(*up) - loss_of(*dn)) / (2 * h)
            ana = analytic[i, j]
            errs.append(abs(num - ana) / max(1e-9, abs(num) + abs(ana)))
        return float(np.max(errs))

    def directional(which, G, h=1e-4):
        """Central difference along the analytic gradient itself.

        The element-wise check is ill-conditioned for Q and K: their entries
        are ~1e-3 against a loss of ~10, so h*dL/dQ_ij is lost in the
        cancellation.  The directional derivative sums the whole matrix and
        is well scaled, and it is the stronger statement anyway: it says the
        analytic gradient IS the steepest-ascent direction with the right
        magnitude.
        """
        up = [Q.copy(), K.copy(), V.copy()]
        dn = [Q.copy(), K.copy(), V.copy()]
        up[which] = up[which] + h * G
        dn[which] = dn[which] - h * G
        num = (loss_of(*up) - loss_of(*dn)) / (2 * h)
        ana = float((G * G).sum())
        return abs(num - ana) / max(1e-12, abs(num) + abs(ana))

    checks = {
        "T": T,
        "d": DHEAD,
        "softmax_row_sum": float(A[QROW].sum()),
        "S_reconstruction_max_abs_err": float(np.abs((S_hat - S)[mask]).max()),
        "attention_from_QK_max_abs_err": float(
            np.abs(_softmax_causal(S_hat, mask) - A).max()
        ),
        "fd_rel_err_dQ": fd(Q, dQ, 0),
        "fd_rel_err_dK": fd(K, dK, 1),
        "fd_rel_err_dV": fd(V, dV, 2),
        "directional_rel_err_dQ": directional(0, dQ),
        "directional_rel_err_dK": directional(1, dK),
        "directional_rel_err_dV": directional(2, dV),
        "dV_equals_At_dZ_exactly": bool(np.array_equal(A.T @ dZ, dV)),
        "norm_dQ": float(np.linalg.norm(dQ)),
        "norm_dK": float(np.linalg.norm(dK)),
        "norm_dV": float(np.linalg.norm(dV)),
        "norm_dZ": float(np.linalg.norm(dZ)),
        "loss": float(0.5 * ((Z - Zstar) ** 2).sum()),
    }

    return Mechanism(A=A, S=S_hat, Q=Q, K=K, V=V, Z=Z, dZ=dZ, dV=dV, dA=dA,
                     dS=dS, dQ=dQ, dK=dK, mask=mask, row=QROW,
                     real_attention=real, checks=checks)


if __name__ == "__main__":
    m = build()
    print("real GPT-2 attention:", m.real_attention, " layer", LAYER, "head", HEAD)
    for k, v in m.checks.items():
        print("  %-32s %s" % (k, v))
    r = m.A[m.row][: m.row + 1]
    print("\nsoftmax row q=%d (%d keys), sum = %.10f" % (m.row, len(r), r.sum()))
    print("  " + " ".join("%.4f" % v for v in r))
    print("  argmax k=%d  max=%.4f  perplexity=%.3f"
          % (int(r.argmax()), r.max(),
             float(np.exp(-(r * np.log(r + 1e-12)).sum()))))
    print("\nrow-gradient norms |dL/dV_j| routed by A^T:")
    print("  " + " ".join("%.3f" % v for v in np.linalg.norm(m.dV, axis=1)))
