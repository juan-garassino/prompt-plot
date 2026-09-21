# STABLE DIFFUSION AS TOPOGRAPHY
*encode down, noise across, denoise in a loop, decode back out*

**Reference:** `studio/stable-diffusion/ref/reference.png` (1672×941, ratio 1.78 —
very wide. Plot on custom paper `42x24` (cm → 420×240 mm, ratio 1.750), which fits
A3's long side. Do NOT force it onto A3 landscape at 1.414; the width is the format.)
**Status:** to build. New family.

**Distinct from `studio/diffusion-passes/`** (noising → U-Net → denoising, pixel
space) and from `studio/diffusion/` + `studio/diffusion-topography/` (vertical
stacked planes). What makes THIS one a different piece is the two things that make
Stable Diffusion "stable": **it works in a latent space** (so there is an encoder and
a decoder), and **it is conditioned** (so there is a text tower feeding the denoiser).
Read those other pieces only to avoid repeating them.

## Essence

Four movements on one wide sheet, and the composition is the dataflow:

1. **Down** — an image is compressed into a latent.
2. **Across** — that latent is destroyed by noise, left to right.
3. **In a loop** — a conditioned network walks it back, one step at a time, and the
   loop is drawn as a loop.
4. **Back out** — the recovered latent is decompressed into an image.

The plate's argument is that the expensive iteration happens in the *small* space:
the lobed blobs on the left and right are big, the latents are small, and the loop
lives entirely among the small things.

## What the reference does

**Left, upper — the encoder.** `x` as a red nest of concentric lobed contours →
a **horn**: a funnel of nested curves narrowing left-to-right → `z₀` as a smaller
**ochre** nest. The horn is the compression, drawn as a shape that literally narrows.

**Top row — the forward process.** `z₀ ··· z_t ··· z_T`, five or six states with `···`
between them, captioned `q(z_t | z_{t−1})` under a dotted arrow. Ochre contour nests
progressively dissolve: contours wobble, break to dashes, then to scattered dots,
ending in a black isotropic dot cloud at `z_T`. Thin dotted droplines fall from each
state down toward the network.

**Left, lower — the conditioning tower.** `y` as a **blue** lobed nest → a second
horn `τ_θ` → `c`, a small blue blob → a sheaf of **blue dashed** curves sweeping
right and up into the network's left flank. Dashed, because conditioning is a
different kind of input from the latent.

**Centre — the denoiser `ε_θ`.** A large **horizontal bowtie / hourglass** of dense
concentric contours: wide, pinching to a waist, wide again. `t` enters from the left
on a short solid arrow with a dot. This is the biggest, densest mass on the sheet.

**Under the centre — the sampling loop.** **Gold** arrowed curves sweeping around the
underside of the bowtie from right back to left, labelled `z_{t−1}` with `···` either
side. This is the only closed circulation on the plate and it must read as one.

**Right — the decoder.** `z₀` (ochre nest) → horn `D` → `x̃` as a red nest that
rhymes with `x` but is not identical to it.

**Furniture:** `STABLE DIFFUSION / AS TOPOGRAPHY` spaced caps top left;
`NOISE / CONDITION / DENOISE / GENERATE` bottom left;
`IMAGES / THROUGH / LATENT / LANDSCAPES` bottom right; registration crosses, long
dashed quarter-arcs sweeping through the corners, scattered dots and short rules.

## What must be TRUE

- **Latent is smaller than pixel.** `z` nests must be visibly smaller and lower-detail
  than `x` and `x̃`. If the latent reads the same size as the image, the entire
  argument for latent diffusion is gone.
- **The loop is a loop.** Sampling is iterative: the gold path must return to the
  network's input, not trail off. Drawn once, read as many passes (`···`).
- **Conditioning enters the denoiser, not the noise.** `c` feeds `ε_θ`, never the top
  row. The forward process is unconditional — that asymmetry is the point.
- `t` is an input to the network **alongside** `z_t` and `c` — three inputs, one output.
- The forward row follows the real schedule: structure barely moves early, collapses
  late and fast (`√ᾱ_t z₀ + √(1−ᾱ_t) ε`). `z_T` is isotropic with no residual lobes.
- `x̃ ≈ x` but **not equal** — the round trip is lossy. Draw the difference honestly;
  an exact copy would be a lie about autoencoders.

## Pens

`red` pixel space (x, x̃) · `ochre/gold` latent space (z, and the sampling loop) ·
`blue` conditioning (y, c) · `black` the networks, type and furniture · cream paper.
Colour here encodes **which space a thing lives in** — that is the plate's key.
