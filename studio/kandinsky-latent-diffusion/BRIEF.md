# LATENT DIFFUSION — KANDINSKY
**Reference:** `studio/kandinsky-latent-diffusion/ref/reference.png` (1536×1024,
ratio 1.500 → paper `36x24` cm = 360×240 mm, or a3 landscape).
**Read first:** `studio/KANDINSKY_SET.md` — the shared idiom AND the technical audit.
**Status:** to build.

Same subject as `studio/stable-diffusion/` (three agents are building that one now in
the fine technical idiom, from a different reference). This is the Kandinsky take.
Check `studio/stable-diffusion/BRIEF.md` for the subject's "what must be TRUE" list —
it applies here too — then build a different composition.

## What the reference does
The full latent-diffusion architecture, annotated like a textbook plate:
- `x` (a Kandinsky composition) → **encoder ℰ** (a flat trapezoid/prism) → `z₀`.
  Captioned `encoder ℰ (pretrained, frozen)`, `x ↦ z₀`, `z₀ ∈ ℝ^{h×w×d}`.
- **Top row, forward diffusion**: `z₀ z₁ z₂ … z_t … z_T` as small circular discs,
  each split into coloured quadrants, progressively dissolving into a black dot cloud.
  Captioned `q(z_t | z_{t−1})` and `z_t = √ᾱ_t z₀ + √(1−ᾱ_t) ε`, `ε ~ 𝒩(0, I)`.
- **Centre**: a big **U-NET** as a bowtie of flat colour blocks, `ε_θ(z_t, t, c)`, with
  a **CROSS ATTENTION** ring at its waist, `t` / `time embedding` entering from above,
  and `skip connections` bracketed underneath.
- **Lower left**: `y` (a second Kandinsky composition, the prompt) → **τ_θ** → `c`,
  feeding the U-Net's waist on a bundle of coloured curves.
- **Right**: `ε̂_t` → a circulation arc back round (`REVERSE DIFFUSION (DENOISING)`,
  `p_θ(z_{t−1} | z_t, c)`, `repeat for t = T,…,0`) → `z₀` → **decoder 𝒟** → `x̃`.
- Bottom-right **legend**: latent state / operation / conditioning signal /
  information flow / skip connection / timestep / noise.
- `WASSILY KANDINSKY INSPIRATION` bottom left; a centred quoted line at the bottom.

## What must be TRUE (and where the reference is suspect)
- **The two `z₀`s are not the same `z₀`.** The encoder's latent and the sampler's
  output share a label in the reference. They are different tensors; the round trip is
  lossy. Same for `x` vs `x̃`. Draw and label the difference.
- **Cross-attention is not only at the bottleneck** in a real U-Net — it is applied at
  several resolutions. Decide what to draw and justify it.
- **Latent must be visibly smaller / lower-detail than pixel space.** That asymmetry
  is the entire reason latent diffusion exists.
- The `repeat for t = T,…,0` loop must read as a loop, not a single arc.
- The forward row decays at the real `√ᾱ_t` rate; `z_T` is isotropic.

## Pens
`black` structure, type, legend · `red` · `blue` · `yellow` · `green`. Cream paper.
Colour should still encode *which space a thing lives in* where it can.
