# CNN — FORWARD AND BACKWARD
*the whole pass, both directions, as one spectral plate*

**Reference:** `studio/cnn-passes/ref/reference.png`
**Status:** to build. New family — NOT a rework of `studio/convolutions/`, which
recreates a different poster entirely. Do not read that piece for layout.

## Essence

A CNN drawn as **two stacked registers of the same pipeline**: activations flowing
left→right on top, gradients flowing right→left underneath. The plate's subject is
not the architecture — it is the *symmetry between the two passes*. Every forward
stage has a gradient twin directly below it, on the same column.

## What the reference does

**Top register — forward pass (activations), arrow →**
- Input plate `X` (`H×W×C`) at far left: a square of concentric dotted ripples.
- Six labelled stages across the sheet, two-line labels in lowercase:
  `convolution (kernels as wave filters)` · `feature maps (frequency responses)` ·
  `non-linearity (ReLU)` · `pooling (downsample)` · `deeper layers (more abstract
  spectra)` · `classifier (linear + softmax)`.
- Each stage is a **stack of 3–4 tilted parallelogram planes** in a shallow shared
  axonometric, each plane line-filled with a different texture: concentric contours,
  wave trains, ripple interference. Depth by overlap and occlusion, never by tone.
- Between stages, **bundles of dotted flow curves** fan out of one stack and pinch
  into the next. Blue marks the highlighted channel; black the rest.
- Tensor shapes sit under each stage in small mono type: `A¹ H×W×C′`, `R¹ H×W×C′`,
  `P¹ H/2×W/2×C′`, `A^L H/2^L×W/2^L×C^L`, `W^c C^L×K`.
- A kernel-swatch row under the convolution stage: `W¹ k×k×C×C′`, three small
  patterned squares.
- Far right: a tall narrow vertical bar (classifier weight matrix, filled with tiny
  glyph marks) fanning to a column of circles `p₁ p₂ p₃ ⋮ p_K` under `softmax`, one
  highlighted blue.
- A `···` ellipsis between pooling and deeper layers — the plate admits it skips.

**Bottom register — backward pass (gradients), arrow ←**
- The exact same columns, mirrored in meaning: `∂L/∂x`, `∂L/∂(conv) (filter
  gradients)`, `∂L/∂A¹`, `∂L/∂(ReLU) (mask)`, `∂L/∂P¹ (unpool)`, `∂L/∂A^L`,
  `∂L/∂z`, `∂L/∂W^c (classifier gradients)`.
- Flow bundles in **red**, running right→left.
- `∂L/∂W¹` gradient swatches under the conv column.
- Far right: red nodes fanning to a column of small squares of varying line density
  — the per-class gradient tiles.

**Bottom legend strip** — five cells divided by thin vertical rules:
1. `convolution = local correlation (in frequency domain)` — grid `*` wave `=` wave
2. `non-linearity (ReLU)` — axes, red kinked line, `y = max(0, x)`
3. `pooling (e.g. 2 × 2)` — 4×4 grid → arrow → 2×2 grid
4. `softmax` — fan of curves into a dot column, `σ(z)`
5. `loss (e.g. cross-entropy)` — `L = − Σᵢ yᵢ log pᵢ`

Registration crosses at all four corners. `C N N` in spaced caps, bottom right.

## What must be TRUE

The mechanism carries the style, per `DESIGN_RUBRIC.md`. At minimum:
- **Column registration is the whole idea** — a forward stage and its gradient twin
  share an x-position exactly. If that breaks, the plate says nothing.
- ReLU's backward is a **mask**: the gradient plane must be visibly *gated* — regions
  the forward pass zeroed are blank paper below, not decorated.
- Pooling downsamples and unpooling **scatters back to one cell per window** — the
  gradient plane is sparser than its forward twin, and visibly so.
- Spatial dimensions shrink left→right while channel count grows. Plane stacks get
  smaller and deeper across the sheet.
- Softmax output is a **normalised** distribution — one clear winner, the rest small.

## Pens

`black` structure/type/furniture · `blue` the highlighted forward channel ·
`red` the backward pass · cream paper as the fourth colour.
