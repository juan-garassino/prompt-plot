"""THE REACH OF ONE UNIT — the computation behind r05 (wildcard), run once, offline.

The SAME forward pass as r02/r03/r04 (Keras MobileNetV2 alpha 1.0 / 224, ImageNet
weights, re-implemented in torch functional form with Keras' `correct_pad`; the
scikit-image cat "chelsea", centre-crop 300² -> bicubic 224²). What is new: the
gradient of the argmax CAM unit is captured at EVERY depth of the network, not
four, so the plate can draw the receptive field as a time series.

depths (20): input · Conv1 stem · block_0 … block_16 · Conv_1 (out_relu)
per depth:   G_d = Σ_c |∂ cam[i*,j*] / ∂A_d|        (Luo et al. 2016, ERF)
             stride_d, centre offset_d (input px of unit 0's RF centre),
             the exact theoretical RF of the unit on that grid (interval
             propagation through every conv halo and stride), and a numerical
             check that G_d is exactly 0 outside it.

Run (PromptPlot's .venv has no torch):
  <torch python> compute_reach.py <mnv2_weights.npz> <chelsea.png> <imagenet_class_index.json>
Writes reach.npz beside this file. The plate only reads reach.npz.
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
CFG = [(1, 16, 1, 1), (6, 24, 2, 2), (6, 32, 3, 2), (6, 64, 4, 2), (6, 96, 3, 1), (6, 160, 3, 2), (6, 320, 1, 1)]


def bn(x, W, name):
    g, b = W[f"{name}/gamma:0"], W[f"{name}/beta:0"]
    m, v = W[f"{name}/moving_mean:0"], W[f"{name}/moving_variance:0"]
    return (x - m[None, :, None, None]) / torch.sqrt(v[None, :, None, None] + 1e-3) * g[None, :, None, None] + b[None, :, None, None]


def conv(x, k, stride=1):
    kt = k.permute(3, 2, 0, 1)
    kh = kt.shape[-1]
    if stride == 2:
        x = F.pad(x, (0, 1, 0, 1)) if kh == 3 else x
        return F.conv2d(x, kt, stride=2)
    return F.conv2d(x, kt, padding=kh // 2)


def dwconv(x, k, stride=1):
    kt = k.permute(2, 3, 0, 1)
    C = kt.shape[0]
    if stride == 2:
        return F.conv2d(F.pad(x, (0, 1, 0, 1)), kt, stride=2, groups=C)
    return F.conv2d(x, kt, padding=1, groups=C)


def forward(x, W):
    """Returns top activation and the list of (name, tensor, n_conv_layers_so_far)."""
    taps = []
    x = F.hardtanh(bn(conv(x, W["Conv1/kernel:0"], 2), W, "bn_Conv1"), 0, 6)
    x.retain_grad()
    taps.append(("stem", x, 1))
    nL = 1
    bid, cin = 0, 32
    for t, c, n, s in CFG:
        for r in range(n):
            stride = s if r == 0 else 1
            inp = x
            h = x
            if bid > 0:
                h = F.hardtanh(bn(conv(h, W[f"mobl{bid}_conv_{bid}_expand/kernel:0"]), W, f"bn{bid}_conv_{bid}_bn_expand"), 0, 6)
                nL += 1
            h = dwconv(h, W[f"mobl{bid}_conv_{bid}_depthwise/depthwise_kernel:0"], stride)
            h = F.hardtanh(bn(h, W, f"bn{bid}_conv_{bid}_bn_depthwise"), 0, 6)
            h = bn(conv(h, W[f"mobl{bid}_conv_{bid}_project/kernel:0"]), W, f"bn{bid}_conv_{bid}_bn_project")
            nL += 2
            if stride == 1 and cin == c:
                h = h + inp
            x = h
            x.retain_grad()
            taps.append((f"block_{bid}", x, nL))
            bid, cin = bid + 1, c
    x = F.hardtanh(bn(conv(x, W["Conv_1/kernel:0"]), W, "Conv_1_bn"), 0, 6)
    nL += 1
    x.retain_grad()
    taps.append(("conv_1", x, nL))
    return x, taps


def layer_list():
    L = [(3, 2, 0)]
    L += [(3, 1, 1), (1, 1, 0)]
    for t, c, n, s in CFG[1:]:
        for r in range(n):
            stride = s if r == 0 else 1
            L += [(1, 1, 0), (3, stride, 0 if stride == 2 else 1), (1, 1, 0)]
    L += [(1, 1, 0)]
    return L


def back(a, b, layers):
    for k, s, p in reversed(layers):
        a, b = a * s - p, b * s - p + k - 1
    return a, b


def main(wpath, img_path, cls_path):
    W = {k: torch.tensor(v, dtype=torch.float64) for k, v in dict(np.load(wpath)).items()}
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2, (w - side) // 2 + side, (h - side) // 2 + side)).resize((224, 224), Image.BICUBIC)
    rgb = np.asarray(im, dtype=np.float64)
    x = torch.tensor(rgb / 127.5 - 1.0).permute(2, 0, 1)[None].requires_grad_(True)
    top, taps = forward(x, W)
    logits = top.mean(dim=(2, 3)) @ W["Logits/kernel:0"] + W["Logits/bias:0"]
    p = torch.softmax(logits, dim=1)[0]
    classes = json.load(open(cls_path))
    order = torch.argsort(p, descending=True)[:5].tolist()
    c = order[0]
    cam = torch.einsum("bkhw,k->bhw", top, W["Logits/kernel:0"][:, c])[0]
    ij = np.unravel_index(int(torch.argmax(cam)), cam.shape)
    print("top-1", classes[str(c)][1], float(p[c]), "argmax", ij, float(cam[ij]))
    cam[ij].backward()

    L = layer_list()
    out = {"names": [], "N": [], "stride": [], "off": [], "nL": [], "trf": [], "zero_outside": []}
    grads = {}
    # input + taps
    entries = [("input", x, 0)] + [(n, t, k) for n, t, k in taps]
    for name, t, n in entries:
        g = t.grad[0].abs().sum(0).numpy()
        N = g.shape[0]
        # unit 0's RF on the input and the stride of this grid
        a0, b0 = back(0, 0, L[:n])
        a1, _ = back(1, 1, L[:n])
        stride = a1 - a0
        off = (a0 + b0) / 2.0
        # exact theoretical RF of the top unit on this grid
        r0, r1 = back(ij[0], ij[0], L[n:])
        c0, c1 = back(ij[1], ij[1], L[n:])
        mask = np.zeros_like(g, dtype=bool)
        mask[max(0, r0):min(N, r1 + 1), max(0, c0):min(N, c1 + 1)] = True
        zero_out = bool(np.all(g[~mask] == 0.0))
        grads[name] = g.astype(np.float32)
        out["names"].append(name)
        out["N"].append(N)
        out["stride"].append(stride)
        out["off"].append(off)
        out["nL"].append(n)
        out["trf"].append([r0, r1, c0, c1])
        out["zero_outside"].append(zero_out)
        print(f"{name:>9s} N={N:3d} stride={stride:2d} off={off:5.1f} nL={n:2d} TRF rows[{r0},{r1}] cols[{c0},{c1}] "
              f"zero-outside={zero_out} nonzero={float((g > 0).mean()):.3f}")
    # cross-check with r03's cached arrays
    cam_np = cam.detach().numpy()
    save = {f"g_{k}": v for k, v in grads.items()}
    save.update({
        "names": np.array(out["names"]), "N": np.array(out["N"]), "stride": np.array(out["stride"]),
        "off": np.array(out["off"]), "nL": np.array(out["nL"]), "trf": np.array(out["trf"]),
        "zero_outside": np.array(out["zero_outside"]), "cam": cam_np.astype(np.float32),
        "argmax": np.array(ij), "top5": np.array([[c_, float(p[c_])] for c_ in order]),
        "top5_names": np.array([classes[str(c_)][1] for c_ in order]),
    })
    np.savez_compressed(HERE / "reach.npz", **save)
    print("saved", HERE / "reach.npz")


if __name__ == "__main__":
    main(*sys.argv[1:4])
