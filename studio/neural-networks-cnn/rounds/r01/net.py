"""The real computation behind the pooling-cascade plate (r01).

A fixed, hand-specified CNN run on ONE real image: the ink of the previous
version of this very plate (``gallery/neural-networks/cnn/promoted/
pp_cnn_dashes.gcode``), rasterised and area-averaged to 48 x 64 pixels.  The
array is cached beside this file as ``input_48x64.npy`` so the plate does not
depend on the (gitignored) gallery at render time; ``build_input()`` rebuilds it.

Architecture (every conv is 'same'-padded, every pool is 2x2 stride 2):

    P0  48x64   input darkness (ink coverage 0..1)
    C1  |Sobel| (3x3 gx, gy -> magnitude)        -> P1 = maxpool  24x32
    C2  Gabor bank 5x5, 4 orientations, rectified,
        the winning orientation per unit          -> P2 = maxpool  12x16
    C3  3x3 binomial (energy integration)         -> P3 = maxpool   6x8
    C4  3x3 centre-surround, rectified            -> P4 = maxpool   3x4

Pitch in input pixels: 1, 2, 4, 8, 16 -- each layer's cell pitch is the
previous one times the stride.  ``receptive_footprints`` propagates one top
unit's dependency interval down through every conv (k-1)/2 halo and every pool
window, clipped to the grid: that is the EXACT set of units it can see.
``verify_footprint`` proves it numerically (perturbing anything outside the P0
footprint leaves the top unit bit-identical).
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

HERE = Path(__file__).resolve().parent
INPUT_NPY = HERE / "input_48x64.npy"
PARENT_GCODE = HERE.parents[3] / "gallery/neural-networks/cnn/promoted/pp_cnn_dashes.gcode"

NX, NY = 48, 64                      # input columns (u), rows (v)
CROP = (20.0, 40.0, 190.0, 267.0)    # mm window on the parent sheet (x0, y0, x1, y1), 0.749 aspect


# ---------------------------------------------------------------------------
# input
# ---------------------------------------------------------------------------


def build_input(px_per_mm: float = 8.0) -> np.ndarray:
    """Rasterise the parent plate's G1 strokes and area-average to NX x NY."""
    from PIL import Image, ImageDraw

    x0, y0, x1, y1 = CROP
    Wp, Hp = int((x1 - x0) * px_per_mm), int((y1 - y0) * px_per_mm)
    im = Image.new("L", (Wp, Hp), 0)
    dr = ImageDraw.Draw(im)
    pen_down, cur = False, None
    num = re.compile(r"([XY])(-?\d+\.?\d*)")
    for line in PARENT_GCODE.read_text().splitlines():
        line = line.split(";")[0].strip()
        if not line:
            continue
        if line.startswith("M3"):
            pen_down = True
            continue
        if line.startswith("M5"):
            pen_down = False
            continue
        if line.startswith(("G0", "G1")):
            d = dict((k, float(v)) for k, v in num.findall(line))
            nxt = (d.get("X", cur[0] if cur else 0.0), d.get("Y", cur[1] if cur else 0.0))
            if line.startswith("G1") and pen_down and cur is not None:
                a = ((cur[0] - x0) * px_per_mm, (y1 - cur[1]) * px_per_mm)
                b = ((nxt[0] - x0) * px_per_mm, (y1 - nxt[1]) * px_per_mm)
                dr.line([a, b], fill=255, width=max(1, int(round(0.35 * px_per_mm))))
            cur = nxt
    A = np.asarray(im, dtype=float) / 255.0          # rows top->bottom
    by, bx = Hp // NY, Wp // NX
    A = A[: by * NY, : bx * NX].reshape(NY, by, NX, bx).mean(axis=(1, 3))
    return A.T.copy()                                 # [u, v] with v = 0 at the TOP of the parent


def load_input() -> np.ndarray:
    if INPUT_NPY.exists():
        return np.load(INPUT_NPY)
    A = build_input()
    np.save(INPUT_NPY, A)
    return A


# ---------------------------------------------------------------------------
# the network
# ---------------------------------------------------------------------------


def conv_same(X: np.ndarray, K: np.ndarray) -> np.ndarray:
    """True 2-D correlation with zero 'same' padding (odd kernels)."""
    k = K.shape[0]
    p = k // 2
    Xp = np.pad(X, p)
    out = np.zeros_like(X)
    for di in range(k):
        for dj in range(k):
            out += K[di, dj] * Xp[di : di + X.shape[0], dj : dj + X.shape[1]]
    return out


def maxpool2(X: np.ndarray) -> np.ndarray:
    a, b = X.shape
    return X[: a // 2 * 2, : b // 2 * 2].reshape(a // 2, 2, b // 2, 2).max(axis=(1, 3))


SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float)
SOBEL_Y = SOBEL_X.T
BINOM3 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], float) / 16.0
CSURR3 = (np.full((3, 3), -1.0) + 9.0 * np.eye(3)[1][:, None] * np.eye(3)[1][None, :]) / 8.0


def gabor5(theta: float, sigma: float = 1.3, lam: float = 3.6) -> np.ndarray:
    r = np.arange(-2, 3, dtype=float)
    U, V = np.meshgrid(r, r, indexing="ij")
    xr = U * math.cos(theta) + V * math.sin(theta)
    yr = -U * math.sin(theta) + V * math.cos(theta)
    g = np.exp(-(xr ** 2 + yr ** 2) / (2 * sigma ** 2)) * np.cos(2 * math.pi * xr / lam)
    return g - g.mean()


GABORS = [gabor5(t) for t in (0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4)]

# (kind, kernel size) per stage, in order, for receptive-field bookkeeping
STAGES = [("conv", 3), ("pool", 2), ("conv", 5), ("pool", 2), ("conv", 3), ("pool", 2), ("conv", 3), ("pool", 2)]


def forward(P0: np.ndarray) -> Dict[str, np.ndarray]:
    C1 = np.hypot(conv_same(P0, SOBEL_X), conv_same(P0, SOBEL_Y))
    P1 = maxpool2(C1)
    resp = np.stack([np.maximum(conv_same(P1, G), 0.0) for G in GABORS])
    C2 = resp.max(axis=0)
    P2 = maxpool2(C2)
    C3 = conv_same(P2, BINOM3)
    P3 = maxpool2(C3)
    C4 = np.maximum(conv_same(P3, CSURR3), 0.0)
    P4 = maxpool2(C4)
    return {
        "P0": P0, "C1": C1, "P1": P1, "C2": C2, "P2": P2, "C3": C3, "P3": P3, "C4": C4, "P4": P4,
        "orient": resp.argmax(axis=0),
    }


def receptive_footprints(top_ij: Tuple[int, int], shapes: List[Tuple[int, int]]):
    """Index box [lo, hi] (inclusive, per axis) of every P_l unit the top unit
    depends on.  ``shapes`` = [P0 shape, ..., P4 shape]."""
    boxes = {len(shapes) - 1: [(top_ij[0], top_ij[0]), (top_ij[1], top_ij[1])]}
    box = boxes[len(shapes) - 1]
    lvl = len(shapes) - 1
    for kind, k in reversed(STAGES):
        if kind == "pool":
            # pool output a..b  <-  conv units 2a .. 2b+1 (same shape as P_{lvl-1})
            n = shapes[lvl - 1]
            box = [(2 * lo, min(n[ax] - 1, 2 * hi + 1)) for ax, (lo, hi) in enumerate(box)]
        else:
            p = k // 2
            n = shapes[lvl - 1]
            box = [(max(0, lo - p), min(n[ax] - 1, hi + p)) for ax, (lo, hi) in enumerate(box)]
            lvl -= 1
            boxes[lvl] = box
    return boxes


def verify_footprint(P0: np.ndarray, top_ij, box0, trials: int = 6, seed: int = 11):
    """Randomise every input pixel OUTSIDE the footprint: the top unit must not move.
    Randomise pixels INSIDE: it must (in general) move.  Returns (max |d| outside,
    max |d| inside)."""
    rs = np.random.default_rng(seed)
    base = forward(P0)["P4"][top_ij]
    mask = np.zeros_like(P0, bool)
    (u0, u1), (v0, v1) = box0
    mask[u0 : u1 + 1, v0 : v1 + 1] = True
    d_out = d_in = 0.0
    for _ in range(trials):
        X = P0.copy()
        X[~mask] = rs.random(int((~mask).sum()))
        d_out = max(d_out, abs(forward(X)["P4"][top_ij] - base))
        Y = P0.copy()
        Y[mask] = rs.random(int(mask.sum()))
        d_in = max(d_in, abs(forward(Y)["P4"][top_ij] - base))
    return d_out, d_in
