"""SUPERPOSITION r02 — the real GPT-2 forward pass behind the plate.

(IO, tokeniser and forward pass adapted from studio/orrery/rounds/r02/mechanism.py.)

Run once (needs network or a local copy of GPT-2 small's ``model.safetensors``);
it writes ``head.npz`` beside this file, and ``piece.py`` reads only that.

    .venv/bin/python studio/orrery/rounds/r02/mechanism.py [--weights PATH] [--scan]

Everything here is plain numpy, no torch:

* GPT-2's byte-level BPE (vocab.json + merges.txt) tokenises the sentence;
* the safetensors file is parsed by hand (8-byte header length, JSON header,
  raw little-endian f32) and only the tensors a layer needs are read, by
  HTTP range request when no local file is given;
* the residual stream is run forward block by block (LN -> causal MHA ->
  residual -> LN -> gelu MLP -> residual) up to the chosen layer, and that
  layer's per-head Q, K, V, A = softmax(QK^T/8 + causal mask), Z = A V are kept.

Proof it is GPT-2 and not a lookalike: every attention map of layers 0..L
computed here is compared against ``~/.promptplot/attn_gpt2.npz`` (the stack
HuggingFace's torch model produced for the same sentence,
``scripts/extract_gpt2_attention.py``). The max abs difference is printed and
stored.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import urllib.request
from functools import lru_cache

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://huggingface.co/openai-community/gpt2/resolve/main/"
TEXT = "The pen plotter drew a black hole while the transformer watched itself think."
CACHED = os.path.expanduser("~/.promptplot/attn_gpt2.npz")
D, NH, HD = 768, 12, 64


# --------------------------------------------------------------------------- io
def _get(url: str, rng: tuple[int, int] | None = None) -> bytes:
    req = urllib.request.Request(url)
    if rng is not None:
        req.add_header("Range", f"bytes={rng[0]}-{rng[1] - 1}")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


class Weights:
    def __init__(self, path: str | None, aux_dir: str | None) -> None:
        self.path = path
        self.aux = aux_dir
        if path:
            with open(path, "rb") as f:
                n = struct.unpack("<Q", f.read(8))[0]
                self.header = json.loads(f.read(n))
        else:
            n = struct.unpack("<Q", _get(BASE + "model.safetensors", (0, 8)))[0]
            self.header = json.loads(_get(BASE + "model.safetensors", (8, 8 + n)))
        self.base = 8 + n

    def aux_file(self, name: str) -> bytes:
        if self.aux and os.path.exists(os.path.join(self.aux, name)):
            with open(os.path.join(self.aux, name), "rb") as f:
                return f.read()
        return _get(BASE + name)

    def raw(self, a: int, b: int) -> bytes:
        if self.path:
            with open(self.path, "rb") as f:
                f.seek(self.base + a)
                return f.read(b - a)
        return _get(BASE + "model.safetensors", (self.base + a, self.base + b))

    def t(self, name: str) -> np.ndarray:
        h = self.header[name]
        assert h["dtype"] == "F32"
        a, b = h["data_offsets"]
        return np.frombuffer(self.raw(a, b), dtype="<f4").reshape(h["shape"]).astype(np.float64)

    def rows(self, name: str, idx) -> np.ndarray:
        """Individual rows of a 2-D tensor (wte is 154 MB; we need 15 rows)."""
        h = self.header[name]
        a, _ = h["data_offsets"]
        w = h["shape"][1]
        out = []
        for i in idx:
            s = a + int(i) * w * 4
            out.append(np.frombuffer(self.raw(s, s + w * 4), dtype="<f4"))
        return np.stack(out).astype(np.float64)


# ------------------------------------------------------------------ tokeniser
def _bytes_to_unicode() -> dict:
    bs = list(range(ord("!"), ord("~") + 1)) + list(range(ord("¡"), ord("¬") + 1)) + list(
        range(ord("®"), ord("ÿ") + 1)
    )
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, map(chr, cs)))


def tokenize(text: str, W: Weights) -> tuple[list[int], list[str]]:
    enc = json.loads(W.aux_file("vocab.json"))
    merges = W.aux_file("merges.txt").decode("utf-8").split("\n")[1:]
    ranks = {tuple(m.split()): i for i, m in enumerate(merges) if m.strip()}
    b2u = _bytes_to_unicode()
    pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?[A-Za-z]+| ?[0-9]+| ?[^\sA-Za-z0-9]+|\s+(?!\S)|\s+""")

    @lru_cache(None)
    def bpe(tok: str) -> tuple:
        word = tuple(tok)
        while len(word) > 1:
            pairs = [(ranks.get((word[i], word[i + 1]), 1e18), i) for i in range(len(word) - 1)]
            r, i = min(pairs)
            if r == 1e18:
                break
            a, b = word[i], word[i + 1]
            new, j = [], 0
            while j < len(word):
                if j < len(word) - 1 and word[j] == a and word[j + 1] == b:
                    new.append(a + b)
                    j += 2
                else:
                    new.append(word[j])
                    j += 1
            word = tuple(new)
        return word

    ids, toks = [], []
    for m in pat.findall(text):
        u = "".join(b2u[b] for b in m.encode("utf-8"))
        for piece in bpe(u):
            ids.append(enc[piece])
            toks.append(piece.replace("Ġ", " "))
    return ids, toks


# ------------------------------------------------------------------- forward
def _ln(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return (x - mu) / np.sqrt(var + eps) * g + b


def _gelu(x):
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))


def _attn(x, W: Weights, L: int):
    T = x.shape[0]
    h = _ln(x, W.t(f"h.{L}.ln_1.weight"), W.t(f"h.{L}.ln_1.bias"))
    qkv = h @ W.t(f"h.{L}.attn.c_attn.weight") + W.t(f"h.{L}.attn.c_attn.bias")
    q, k, v = np.split(qkv, 3, axis=-1)
    q = q.reshape(T, NH, HD).transpose(1, 0, 2)
    k = k.reshape(T, NH, HD).transpose(1, 0, 2)
    v = v.reshape(T, NH, HD).transpose(1, 0, 2)
    S = q @ k.transpose(0, 2, 1) / np.sqrt(HD)
    mask = np.tril(np.ones((T, T), bool))
    S = np.where(mask, S, -1e10)
    S = S - S.max(-1, keepdims=True)
    A = np.exp(S)
    A /= A.sum(-1, keepdims=True)
    Z = A @ v
    return q, k, v, A, Z


def forward(W: Weights, ids: list[int], upto: int):
    x = W.rows("wte.weight", ids) + W.rows("wpe.weight", range(len(ids)))
    per_layer = []
    for L in range(upto + 1):
        q, k, v, A, Z = _attn(x, W, L)
        per_layer.append((q, k, v, A, Z))
        if L == upto:
            break
        T = x.shape[0]
        a = Z.transpose(1, 0, 2).reshape(T, D) @ W.t(f"h.{L}.attn.c_proj.weight") + W.t(
            f"h.{L}.attn.c_proj.bias"
        )
        x = x + a
        h = _ln(x, W.t(f"h.{L}.ln_2.weight"), W.t(f"h.{L}.ln_2.bias"))
        m = _gelu(h @ W.t(f"h.{L}.mlp.c_fc.weight") + W.t(f"h.{L}.mlp.c_fc.bias"))
        x = x + m @ W.t(f"h.{L}.mlp.c_proj.weight") + W.t(f"h.{L}.mlp.c_proj.bias")
    return per_layer


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", default=None, help="local GPT-2 small model.safetensors")
    ap.add_argument("--aux", default=None, help="dir holding vocab.json + merges.txt")
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--head", type=int, required=True)
    ap.add_argument("--dump", default=None, help="also save every layer/head (for the scan)")
    args = ap.parse_args()

    W = Weights(args.weights, args.aux)
    ids, toks = tokenize(TEXT, W)
    print("tokens", len(toks), toks)
    upto = 11 if args.dump else args.layer
    layers = forward(W, ids, upto)

    ref = np.load(CACHED)["attn"] if os.path.exists(CACHED) else None
    err = []
    if ref is not None:
        for L, (_, _, _, A, _) in enumerate(layers):
            err.append(float(np.abs(A - ref[L]).max()))
        print("max |A_numpy - A_torch| per layer:", ["%.1e" % e for e in err])
    if args.dump:
        np.savez_compressed(
            args.dump, tokens=np.array(toks),
            Q=np.stack([l[0] for l in layers]), K=np.stack([l[1] for l in layers]),
            V=np.stack([l[2] for l in layers]), A=np.stack([l[3] for l in layers]),
            Z=np.stack([l[4] for l in layers]))
        print("dumped", args.dump)

    L, h = args.layer, args.head
    q, k, v, A, Z = layers[L]
    out = os.path.join(HERE, "head.npz")
    np.savez_compressed(
        out,
        tokens=np.array(toks),
        ids=np.array(ids),
        layer=L,
        head=h,
        Q=q[h].astype(np.float64),
        K=k[h].astype(np.float64),
        V=v[h].astype(np.float64),
        A=A[h].astype(np.float64),
        Z=Z[h].astype(np.float64),
        check_err=np.array(err, dtype=np.float64),
    )
    print("saved", out)


if __name__ == "__main__":
    main()
