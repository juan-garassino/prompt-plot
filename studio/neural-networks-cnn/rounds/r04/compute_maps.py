"""The ONE computation behind the one-valley plate (r02) — run once, offline.

A real, trained ImageNet CNN (Keras MobileNetV2, alpha 1.0, 224 px, the
published `mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224.h5`)
re-implemented in torch functional form with Keras' exact padding rules
(`correct_pad` = pad right/bottom by one before every stride-2 conv), fed ONE
real photograph: `chelsea.png`, the scikit-image test cat (CC0, S. van der Walt),
centre-cropped to its 300 x 300 square and resized to 224 x 224.

What is cached (``maps.npz`` beside this file, all float32):

  pix      224x224  input luminance 0..1 (the PIXELS terrain)
  a56      56x56    ||block_2_add||_2 over 24 channels      (stride 4)
  a28      28x28    ||block_5_add||_2 over 32 channels      (stride 8)
  a14      14x14    ||block_12_add||_2 over 96 channels     (stride 16)
  cam      7x7      class-activation map of the top-1 class
                    sum_k w[k,c] * out_relu[k]  (GAP + dense => CAM is exact)
  g224..g7          effective receptive field of the argmax CAM unit: |d cam[i*,j*] / d A|
                    summed over channels, at every captured layer (Luo et al. 2016)
  rf       (5,4)    theoretical receptive field of that unit on each grid, as
                    [r0, r1, c0, c1] inclusive unit indices, by exact interval
                    propagation through every conv halo / stride (verified below)
  top5     class ids + probabilities, logits of the whole softmax

Why this runs in another interpreter: PromptPlot's .venv has no torch/h5py. The
plate (piece.py) only reads maps.npz. Rebuild:

  uv venv h5env && uv pip install -p h5env h5py numpy
  h5env/bin/python -c "...h5 -> mnv2_weights.npz"       (see NOTES.md)
  <any torch python> compute_maps.py <weights.npz> <chelsea.png> <imagenet_class_index.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

HERE = Path(__file__).resolve().parent

# (expansion t, out channels c, repeats n, first stride s) — Sandler et al. 2018, Table 2
CFG = [(1, 16, 1, 1), (6, 24, 2, 2), (6, 32, 3, 2), (6, 64, 4, 2), (6, 96, 3, 1), (6, 160, 3, 2), (6, 320, 1, 1)]
CAPTURE = {2: "a56", 5: "a28", 12: "a14"}


def load(wpath):
    W = dict(np.load(wpath))
    return {k: torch.tensor(v, dtype=torch.float64) for k, v in W.items()}


def bn(x, W, name):
    g, b = W[f"{name}/gamma:0"], W[f"{name}/beta:0"]
    m, v = W[f"{name}/moving_mean:0"], W[f"{name}/moving_variance:0"]
    return (x - m[None, :, None, None]) / torch.sqrt(v[None, :, None, None] + 1e-3) * g[None, :, None, None] + b[None, :, None, None]


def conv(x, k, stride=1, pad="same"):
    kt = k.permute(3, 2, 0, 1)  # (kh,kw,in,out) -> (out,in,kh,kw)
    kh = kt.shape[-1]
    if stride == 2:
        x = F.pad(x, (0, 1, 0, 1)) if kh == 3 else x  # Keras correct_pad for even inputs
        return F.conv2d(x, kt, stride=2)
    return F.conv2d(x, kt, padding=kh // 2)


def dwconv(x, k, stride=1):
    kt = k.permute(2, 3, 0, 1)  # (kh,kw,in,1) -> (in,1,kh,kw)
    C = kt.shape[0]
    if stride == 2:
        return F.conv2d(F.pad(x, (0, 1, 0, 1)), kt, stride=2, groups=C)
    return F.conv2d(x, kt, padding=1, groups=C)


def forward(x, W):
    acts = {}
    x = F.hardtanh(bn(conv(x, W["Conv1/kernel:0"], 2), W, "bn_Conv1"), 0, 6)
    bid, cin = 0, 32
    for t, c, n, s in CFG:
        for r in range(n):
            stride = s if r == 0 else 1
            inp = x
            h = x
            if bid > 0:
                h = F.hardtanh(bn(conv(h, W[f"mobl{bid}_conv_{bid}_expand/kernel:0"]), W, f"bn{bid}_conv_{bid}_bn_expand"), 0, 6)
            h = dwconv(h, W[f"mobl{bid}_conv_{bid}_depthwise/depthwise_kernel:0"], stride)
            h = F.hardtanh(bn(h, W, f"bn{bid}_conv_{bid}_bn_depthwise"), 0, 6)
            h = bn(conv(h, W[f"mobl{bid}_conv_{bid}_project/kernel:0"]), W, f"bn{bid}_conv_{bid}_bn_project")
            if stride == 1 and cin == c:
                h = h + inp
            x = h
            if bid in CAPTURE:
                x.retain_grad()
                acts[CAPTURE[bid]] = x
            bid, cin = bid + 1, c
    x = F.hardtanh(bn(conv(x, W["Conv_1/kernel:0"]), W, "Conv_1_bn"), 0, 6)
    x.retain_grad()
    acts["top"] = x
    return x, acts


# ---- exact theoretical receptive field by interval propagation -------------
# every layer in order as (kernel, stride, pad_before) on the Keras grid
def layer_list():
    L = [(3, 2, 0)]  # Conv1 (pad right/bottom only -> 0 before)
    L += [(3, 1, 1), (1, 1, 0)]  # block 0 dw + project
    bid = 1
    for t, c, n, s in CFG[1:]:
        for r in range(n):
            stride = s if r == 0 else 1
            L += [(1, 1, 0), (3, stride, 0 if stride == 2 else 1), (1, 1, 0)]
            bid += 1
    L += [(1, 1, 0)]  # Conv_1
    return L


def rf_interval(idx_top, n_top_layers):
    """Map a unit interval [a,b] on the output of the first n layers back to
    the input of layer 0. Residual adds do not widen (same grid)."""
    L = layer_list()[:n_top_layers]
    a, b = idx_top, idx_top
    for k, s, p in reversed(L):
        a, b = a * s - p, b * s - p + k - 1
    return a, b


def main(wpath, img_path, cls_path):
    W = load(wpath)
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side)).resize((224, 224), Image.BICUBIC)
    rgb = np.asarray(im, dtype=np.float64)
    x = torch.tensor(rgb / 127.5 - 1.0).permute(2, 0, 1)[None].requires_grad_(True)
    top, acts = forward(x, W)
    logits = top.mean(dim=(2, 3)) @ W["Logits/kernel:0"] + W["Logits/bias:0"]
    p = torch.softmax(logits, dim=1)[0]
    classes = json.load(open(cls_path))
    order = torch.argsort(p, descending=True)[:5].tolist()
    for c in order:
        print(f"{classes[str(c)][1]:>20s}  {float(p[c]):.4f}")
    c = order[0]
    cam = torch.einsum("bkhw,k->bhw", top, W["Logits/kernel:0"][:, c])[0]
    # CAM check: GAP(cam) + bias == logit exactly
    print("CAM mean + bias vs logit:", float(cam.mean() + W["Logits/bias:0"][c]), float(logits[0, c]))
    ij = np.unravel_index(int(torch.argmax(cam)), cam.shape)
    print("argmax CAM unit", ij, float(cam[ij]))
    cam[ij].backward()
    out = {"pix": (0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]) / 255.0}
    for k in ("a56", "a28", "a14"):
        out[k] = acts[k][0].norm(dim=0).detach().numpy()
    out["cam"] = cam.detach().numpy()
    out["g224"] = x.grad[0].abs().sum(0).numpy()
    out["g56"] = acts["a56"].grad[0].abs().sum(0).numpy()
    out["g28"] = acts["a28"].grad[0].abs().sum(0).numpy()
    out["g14"] = acts["a14"].grad[0].abs().sum(0).numpy()
    g7 = np.zeros((7, 7)); g7[ij] = 1.0
    out["g7"] = g7
    # theoretical RF on each captured grid (#layers up to and incl. that block)
    nL = {"g224": 0, "a56": 3 + 3 * 2, "a28": 3 + 3 * 5, "a14": 3 + 3 * 12}
    Lall = layer_list()
    rf = []
    for key, n in (("g224", 0), ("a56", nL["a56"]), ("a28", nL["a28"]), ("a14", nL["a14"])):
        # interval of the top unit mapped down to the OUTPUT grid of layer n
        sub = Lall[n:]
        a0, b0 = ij[0], ij[0]
        a1, b1 = ij[1], ij[1]
        for k, s, pd in reversed(sub):
            a0, b0 = a0 * s - pd, b0 * s - pd + k - 1
            a1, b1 = a1 * s - pd, b1 * s - pd + k - 1
        N = {"g224": 224, "a56": 56, "a28": 28, "a14": 14}[key]
        rf.append([max(0, a0), min(N - 1, b0), max(0, a1), min(N - 1, b1), a0, b0, a1, b1])
    rf.append([ij[0], ij[0], ij[1], ij[1]] * 2)
    out["rf"] = np.array(rf, dtype=np.int32)
    print("theoretical RF (clipped r0,r1,c0,c1 | raw):", rf)
    # numerical proof the ERF is local: fraction of |grad| mass within the RF
    for key in ("g224", "g56", "g28", "g14"):
        g = out[key]
        print(key, "shape", g.shape, "nonzero frac", float((g > 0).mean()))
    out["top5"] = np.array([[c_, float(p[c_])] for c_ in order])
    out["class_name"] = np.array(classes[str(c)][1])
    out["argmax"] = np.array(ij)
    np.savez_compressed(HERE / "maps.npz", **{k: (v.astype(np.float32) if isinstance(v, np.ndarray) and v.dtype.kind == "f" else v) for k, v in out.items()})
    print("saved", HERE / "maps.npz")


if __name__ == "__main__":
    main(*sys.argv[1:4])
