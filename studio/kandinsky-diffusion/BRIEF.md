# DIFFUSION — KANDINSKY
**Reference:** `studio/kandinsky-diffusion/ref/reference.png` (1448×1086, ratio 1.333
→ paper `32x24` cm = 320×240 mm, or a4 landscape).
**Read first:** `studio/KANDINSKY_SET.md` — the shared idiom AND the technical audit.
**Status:** to build.

Same subject as `studio/diffusion-passes/` (which holds an APPROVED piece, "THE LONG
WAY BACK" — `rounds/r03/piece_v2_APPROVED.py`). That one is the technical idiom; this
is the Kandinsky one. Read it so you do not repeat it.

## What the reference does
A left-to-right band: a dense Bauhaus composition at the left (the data sample —
stacked rectangles, quadrants, a circle, checkerboard, black diagonals) → a **dissolving
field of dots** of many sizes and colours → a central **circular mandala** (the
denoiser: concentric rings, a yellow core, overlaid translucent triangles, heavy black
diagonals cutting through) → a second dot field → a second Bauhaus composition at the
right (the generated sample). Captions on ruled arrows beneath: `forward process` ·
`noise` · `denoiser` · `reverse process` · `sample`. Corner furniture: small
quadrant-and-rule motifs, a yellow and a blue disc on a rule at the top.

## What must be TRUE (and where the reference is suspect)
- The right-hand composition must be **of the same family as the left but NOT a copy** —
  it is a different sample from the same distribution.
- **Sampling is iterative.** The reference reads as one pass through a denoiser box.
  Find a way to make the loop legible — the brief's note on iteration applies.
- The dot field must decay at the real `√ᾱ_t` rate — late and fast, not linear.
- The noise end must be **isotropic**: no residual structure, no preferred direction,
  no leftover colour ordering.

## Pens
Kandinsky primaries: `black` structure/rules/type · `red` · `blue` · `yellow` ·
`green`. Cream paper. Five pens; colour separation must do real work.
