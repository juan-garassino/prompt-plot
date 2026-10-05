# THE LONG WAY BACK (DIFFUSION — forward, network, reverse) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/diffusion_passes` |
| current render | `gallery/studio/diffusion_passes/current/pp_diffusion_passes_abstract_v2.png` (THE LONG WAY BACK — **approved**) |
| | `gallery/studio/diffusion_passes/current/pp_diffusion_passes_faithful_v11.png` (reference recreation) |
| | `gallery/studio/diffusion_passes/current/pp_diffusion_passes_mechanism_v7.png` (real DDPM on a Gaussian mixture) |
| source | abstract: `studio/diffusion-passes/rounds/r03/piece_v2_APPROVED.py::diffusion_passes` (frozen; `r03/piece.py` holds unapproved v3–v5) · faithful: `studio/diffusion-passes/rounds/r01/piece.py::diffusion_passes` · mechanism: `studio/diffusion-passes/rounds/r02/piece.py::diffusion_passes` |
| reference | `studio/diffusion-passes/ref/reference.png` (1512×1043) |
| paper · pens | a3 landscape, cream · 0 black = t = 0 data / structure / type / chord · 1 dodgerblue · 2 mediumpurple · 3 palevioletred · 4 crimson = a continuous **t-ramp** (black → blue → purple → pink → crimson); crimson ends at the prior |
| status | abstract v2 **PROMOTED** ("this is also supper good", 2026-09-20) — frozen · faithful v11 and mechanism v7 unreviewed · 25 renders on disk |

## In one line
Diffusion drawn as **a lattice-with-defects wrapped into a ring of time that fails to close** — the arc coordinate is t, the crystal melts to an isotropic bullseye at the antipode and recrystallises back to the seam at a 37.4° grain tilt, and one straight chord (the closed-form forward jump) crosses the void one way only. The faithful and mechanism variants keep the reference's **three laminar registers** (noising row, U-Net bowtie, denoising row) with colour as t; the mechanism's states are real DDPM particles.

## Lede
Diffusion drawn as **a ring of time that does not close**: an ordered crystal melts into noise along one arc and is rebuilt, slightly rotated, along the other.

## On the sheet
A wide ring takes up most of the sheet. Its texture runs from a black ruled lattice through blue, purple and pink to crimson scatter, with a small crimson bullseye of pure noise at the lower right. The return arc is stitched and tilted. One straight diagonal chord crosses the ring, and large stroke type stacks down the left.

## The science
The forward half follows the standard recipe for adding noise step by step: fine detail dies first, and each pen change marks a level where noise overtakes what is left of the picture. The chord is the shortcut that jumps straight to pure noise in one step. The return arc's tilt means a new picture, not the original. The learned network is not drawn.

## What is on the sheet

### abstract v2 — THE LONG WAY BACK
**The ring (dominant, u 0.33–0.89, v 0.09–0.91; ≈0.57 sheet width, centre ≈ u 0.61, v 0.50).** An annular band ~50 mm thick whose texture changes continuously around its circumference:
- **Forward half, clockwise from the seam (upper-left → top → right → lower-right)**: starts at the seam (u≈0.38, v≈0.26) as a clean **black ruled lattice** — warped quadrilateral cells with continuous row lines — sweeping up to the top (u≈0.60, v≈0.11). At the top it turns **blue**: cells break into irregular polygons with loose dashes inside (u 0.60–0.78, v 0.10–0.35); then **purple** scattered short strokes down the right side (u 0.76–0.86, v 0.35–0.55); **pink** (v 0.55–0.65); **crimson** fragments narrowing toward the bottleneck.
- **The prior** at u≈0.81, v≈0.71: a crimson bullseye of 9 concentric circles (≈17.8 mm, ≈0.04 sheet width) ringed by dotted circles — the smallest object and the only true circle on the sheet.
- **Reverse half, continuing clockwise from the prior (bottom → left → back up to the seam)**: crimson scatter (u 0.68–0.80, v 0.72–0.85), pink and purple scattered dashes along the bottom (u 0.52–0.72, v 0.80–0.91), **blue stitched cells** — every bond a separate dash — up the lower-left (u 0.36–0.56, v 0.55–0.90), and finally a **black stitched lattice** of short parallel dash pairs at a visibly rotated grain (u 0.34–0.52, v 0.26–0.56) that meets the ruled forward lattice at the seam and does not fit.
- **The chord**: a single straight diagonal (≈ −37°) from the top-left (u≈0.19, v≈0.045, dashed) to the lower-right (u≈0.97, v≈0.88, dashed). Inside the ring it is ink: a **heavy black keyline bar** at the seam (u 0.38–0.48, v 0.26–0.34 — the grain boundary), then three parallel solid lines converging to the prior (u 0.48–0.81), the last ~26 mm drawn as a fat mass landing in the bullseye's centre.
- **`ONE EVALUATION`** in large spaced caps set *along* the chord on its lower-left side, from the seam (u≈0.46, v≈0.33) to u≈0.72, v≈0.62.
- **Void labels**: `FORWARD   q ( x t | x 0 )` / `RULED. ONE EVALUATION.` (u 0.60–0.73, v 0.31–0.33); `t 0.  DATA.` / `GRAIN BOUNDARY   θ 37.4 DEG` (u 0.51–0.67, v 0.40–0.42 — the chord's `E` letters run through `BOUNDARY`); `REVERSE   p θ ( x t-1 | x t )` / `STITCHED. 512 EVALUATIONS.` (u 0.52–0.68, v 0.62–0.64); crimson `t T.  N ( 0 , I )` / `ISOTROPIC. THE ONLY` / `TRUE CIRCLE HERE.` (u 0.69–0.83, v 0.73–0.76), overlapping crimson ring dashes.

**Type column (Constructivist, flush-left at u≈0.036).**
- `D I F F U S I O N` spaced small caps, v≈0.065.
- `THE` / `LONG` / `WAY` / `BACK` — giant stroke type, ~24 mm caps, u 0.036–0.25, v 0.10–0.51.
- `A RING OF TIME THAT DOES NOT CLOSE` (v≈0.54).
- `DOWN THE CHORD IN ONE EVALUATION. / BACK ROUND THE ARC IN 512 STEPS. / THE SCHEDULE IS SYMMETRIC ABOUT THE / AXIS. THE SAMPLE IS NOT.` (v 0.58–0.64).
- `COSINE SCHEDULE  s 0.008   T 512 / LATTICE a 9.0 MM   SIGMA 3.57 MM / RESOLVED WHILE SNR ABOVE (2 SIGMA / L)^2 / SNR = ABAR / (1 - ABAR)` (v 0.67–0.71).
- Table (v 0.74–0.79): `L = a/3  DIES u 0.247  ABAR 0.850`, `L = a  DIES u 0.570  ABAR 0.386`, `L = 2a  DIES u 0.758  ABAR 0.136`, `L = 3a  DIES u 0.834  ABAR 0.065`.
- `GRAIN TILT  θ 37.4 DEG / ONE STEP MOVES AN ATOM 0.22 MM / THE CRYSTAL IS 254 MM ACROSS / THE PRIOR IS 17.8 MM ACROSS` (v 0.81–0.85).
- A five-swatch pen ramp with `t 0` … `t T` (v≈0.885); `P E N  P L O T T E R` with a rule (v≈0.935); one plus mark at the bottom-left corner.

### faithful v11 — three registers after the reference
- **Top register, forward (v 0.10–0.38)**: `forward process (noising)` over a long dashed → arrow (u 0.25–0.78, v 0.10–0.12), `q(xₜ | x₀) = N(√ᾱₜ x₀, (1 − ᾱₜ) I)`. Six states on one row (v 0.19–0.30), each ≈0.08 wide, separated by `•••`: `x₀` black trefoil contour nest with a centre dot; `x_t1` blue nest wobbling; `x_t2` purple nest breaking to dashes; `x_t3` pink mostly dots; `x_t4` crimson dot cloud with a few dashed arcs; `x_T` black isotropic dot cloud. Captions `data distribution p_data(x)` and `isotropic noise N(0, I)`. A full-width axis arrow `t = 0` … `increasing noise` … `t = T` at v≈0.38. Dashed vertical brackets at both ends of the row.
- **Middle register, U-Net (v 0.40–0.67)**: `U-Net ε_θ(xₜ, t)` / `predicts noise (or v, or x0)` / `skip connections` stacked at centre (v 0.40–0.44). A horizontal **bowtie of contour lines** (u 0.26–0.66, v 0.49–0.67): a tall blue mouth at left, purple bulges, a pinched waist at centre with small pink bulges, a tall crimson mouth at right. Four nested dashed skip arcs with arrowheads arch over the top (apex v≈0.43). Left: crimson dot cloud `x_t` / `noisy sample` (u 0.10–0.22) with → arrow; right: black trefoil nest `ε̂` / `predicted noise` (u 0.72–0.77) with → arrow in; loss formula `ℒ = E_{t,x0,ε}[‖ε − ε_θ(xₜ, t)‖²]` behind a vertical rule at u≈0.87, v 0.52.
- **Bottom register, reverse (v 0.68–0.93)**: `reverse process (denoising)` over a dashed ← arrow, `p_θ(x_{t−1} | xₜ) = N(μ_θ(xₜ, t), σₜ² I)`. Six states: `x₀` a **different** black nest — four-lobed star, `x_t1` blue four-lobed nest, … `x_T` black cloud; captions `generated sample x ~ p_θ(x)` and `sample from N(0, I)`.
- **Furniture**: `DIFFUSION` / `probabilistic generative modeling` top-left; right keyword stacks `noise / schedules / score matching / denoising / generative sampling` (u 0.87–0.93, v 0.10–0.21) and `latent diffusion / text conditioning / classifier-free guidance / high-dimensional data / iterative refinement` (u 0.87–0.95, v 0.80–0.88); plus marks at top-centre, left edge (v≈0.58) and bottom-centre; small filled squares on the right margin; dashed quarter-arcs; `P E N  P L O T T E R` with rule bottom-left.

### mechanism v7 — real DDPM particles
- Same three-register layout and furniture; title `D I F F U S I O N` in bold spaced caps; type throughout in spaced stroke caps.
- **States are particle renders**: `x0` is five separate contoured blobs (a small cluster of dotted nests) rather than one rose; `xt1`…`xt4` show the same blobs dissolving into dotted arcs and scatter; `xT` an isotropic black dot cloud. Under each: `t = 0 / sqrt at 1.000`, `t = 220 / sqrt at 0.938`, `t = 350 / sqrt at 0.848`, `t = 480 / sqrt at 0.725`, `t = 670 / sqrt at 0.492`, `t = 1000 / sqrt at 4.9e-05`, colour-matched.
- **U-Net as a stepped laminar bundle** (u 0.23–0.77, v 0.46–0.67): ~30 parallel horizontal lines that step inward at each resolution — `32^2 128ch` (blue, tallest), `16^2 256ch`, `8^2 256ch` (purple), `4^2 256ch` (pink waist) — and step back out through crimson; dashed skip arcs with arrowheads over the top. Input `xt` / `noisy sample` / `t = 350` in purple at left; `c` / `predicted noise` a small black contour blob at right; `L = E ( c - ce(xt, t) )^2 = 1.332 measured`.
- **Bottom register** runs `x0 xt1 xt2 xt3 xt4 xT` left→right under a ← arrow; its x0 is a near-identical five-blob cluster. Footer: `cosine schedule   T = 1000   n = 40000 particles   exact score   DDPM ancestral`.

## The science it encodes
DDPM: the forward process `xₜ = √ᾱₜ x₀ + √(1−ᾱₜ) ε` destroys structure analytically; a learned denoiser (U-Net, ε-prediction) makes the reverse chain possible; the reverse chain is a different sample of the same law.
- **abstract** (`r03/NOTES.md`): cosine schedule (s = 0.008, T = 512); sites transported by the real DDPM map with isotropic 2-D noise in the local frame; a scale ℓ is drawn while `SNR = ᾱ/(1−ᾱ) > (2σ/ℓ)²`, so structure dies late and fast at measured crossings (u 0.247 / 0.570 / 0.758 / 0.834), and each pen change is exactly one such threshold. The two arcs are mirror images about the chord (equal t at equal offset). Reverse = a rotated lattice (grain tilt 37.4°) = "a different sample". Forward is **ruled** (continuous rows, one pass, cheap); reverse is **stitched** (every bond a dash, every atom an oriented step, expensive). The U-Net is deliberately not drawn — the learned part is the asymmetry: a chord on the forward side, none on the reverse. Canon: Russian Constructivism (chord = diagonal thrust, display type as mass).
- **faithful** (`r01/NOTES.md`): hand-authored progressive perturbation of a rose nest; pen at any x in the bowtie matches the state column above it.
- **mechanism** (`r02/piece.py` docstring): a 6-component Gaussian-mixture data law, cosine schedule T = 1000, one fixed ε per particle across the top row (one coupling evolving), an **exact Bayes-optimal** denoiser from the closed-form mixture score (not a learned net), and a real 1000-step DDPM ancestral reverse chain from fresh noise; each state is a binned KDE of its own particles. Visible check: the bottom x0 is a new particle draw of the same five blobs — honest, but it reads as "the same picture", not "a different sample".

## How it got here
- **faithful**: v5 → v9 → v11 are refinements of one layout (reference recreation); the bowtie and trefoil/star x₀ pair arrived by v5.
- **mechanism**: v5 already had the stepped U-Net bundle and real particles (states were small uniform clouds); v7 replaced them with KDE-contoured blobs and measured `sqrt at` labels.
- **abstract**: v1 had 146 bounds violations, captions overrunning the ring, a diffuse melt with no focus. **v2** (approved): the prior redrawn as its own level sets (the bullseye), a 112 mm budgeted type column, ring labels moved into the void, `ONE EVALUATION` set along the chord, 0 violations. v3–v5 exist in `r03/piece.py` as unapproved proposals (v4: smaller ring 242 mm, lattice a 7.0, smaller type, a `NO CHORD HERE` label). Juan on v2: **"this is also supper good."** — "A ring of time that does not close: the chord is the closed-form forward jump, the arc is 512 reverse steps."

## Keep — what works

### abstract v2
- **The ring + chord as one Constructivist diagonal**: the chord runs corner-to-corner (u 0.19 → 0.97) and simultaneously is the forward jump, the mirror axis and the driving diagonal; its fat landing in the prior makes the bullseye the focal point despite being 0.04 wide.
- **Scale contrast**: 254 mm crystal vs 17.8 mm prior vs 24 mm display type — three decisive sizes.
- **Ruled vs stitched** at the seam (u 0.34–0.52, v 0.26–0.56): continuous black grid above the keyline, crooked dash-pairs below it — "cheap vs crawled" readable without text.
- **The heavy grain-boundary bar** at the seam — the defect has mass.
- **Colour symmetric about the chord while geometry is not** — the eye reads "same schedule, different sample" at once.
- **The giant `THE LONG WAY BACK` column** at u 0.036–0.25 flush on one grid line, with the measured table below it.
- Crimson is scarce (0.83 m of 13.4 m) and spent only on the melt.

### faithful v11
- Column registration between top and bottom rows (six states on the same u in both rows).
- The bowtie's colour matches the state above each x.
- Bottom x₀ is a different shape (four-lobed star vs trefoil) — the "different sample" claim is visible.

### mechanism v7
- The **stepped laminar U-Net bundle** with resolution/channel labels — the bottleneck is a count of lines, not a picture.
- Measured `sqrt at` values under every state in the state's own pen.
- `L = … = 1.332 measured` — the loss is a real number.

## Weak — what doesn't

### abstract v2
- [space] The chord's `ONE EVALUATION` letters run through `GRAIN BOUNDARY θ 37.4 DEG` (u≈0.55–0.60, v≈0.41) and the first letters (`O`, `N`) sit on the stitched lattice at the seam — type colliding with type and with geometry.
- [space] The crimson caption `ISOTROPIC. THE ONLY / TRUE CIRCLE HERE.` (u 0.69–0.83, v 0.73–0.76) is overprinted by the ring's crimson dashes.
- [craft] The right half of the ring (blue → pink, u 0.60–0.88) is loose scatter of short dashes with little structure; at 1 m the melt looks like noise *drawn* rather than a lattice melting — the "late and fast" collapse is not legible as a boundary.
- [hierarchy] Three void labels float in the ring's interior at similar size with no shared axis.
- [concept] The seam mismatch (the punchline) is partly hidden under the heavy keyline bar; the 37.4° tilt of the black reverse lattice is visible but the forward lattice at the seam is also curved, so "crooked" is not obvious.
- [depth] Flat; Constructivism permits it but the flatness is not declared on the sheet or in the notes.

### faithful v11
- [concept] It is the reference: three registers, arrows, formulas, a U-Net bowtie with skip arcs — a textbook schematic (§ 6 ≤ 3).
- [hierarchy] Twelve states + bowtie + clouds all at one scale; nothing dominates.
- [grid] Keyword stacks, filled squares, plus marks and quarter-arcs scattered in corners — the furniture checklist.
- [craft] The noise states (x_t3, x_t4, x_T) are unstructured stipple — tone by random dots, not by duty.

### mechanism v7
- [concept] Same schematic layout as the faithful; the real computation does not change the read.
- [concept] The bottom row's x0 is visually the same five-blob cluster as the top x0 — the "different sample" claim does not land.
- [craft] Spaced stroke caps at ~1.5 mm for all labels; the dotted particle blobs at x0 read as smudges at 3 m.
- [tension] Symmetric registers, centred U-Net.

## Next versions
- **clean-seam** (abstract) — Branch v6 from `r03/piece.py` (not the frozen file). Keep ring, chord, prior and type column exactly. Move `ONE EVALUATION` to the chord's upper-right side between u 0.50 and 0.75 so it touches nothing, gather the three void labels onto one axis parallel to the chord, and set the crimson prior caption outside the ring (u≈0.86–0.97, v≈0.74) clear of the dashes. Make the seam mismatch the loudest thing: stop the keyline bar short so the ruled rows and the tilted stitched rows visibly meet at an angle for ~20 mm. Same argument, zero collisions.
- **two-crystals** (mechanism × abstract) — Drive the approved ring with r02's real particles: the forward arc's sites are the actual DDPM coupling, the reverse arc is the actual ancestral chain from fresh noise, and the recrystallised lattice's tilt is *measured* from the generated sample's principal axis rather than chosen. The punchline angle becomes a result.
- **melt-front** (lens) — Zoom into the forward half only: the lattice across the full sheet width (cropped at three edges), melting left→right with each scale's death line drawn as one crisp vertical boundary at its measured u (0.247 / 0.570 / 0.758 / 0.834), pen changing exactly there. The "late and fast" collapse becomes the whole plate; the chord reappears as a single diagonal jumping from the left edge to the fog.
- **If only iterating:**
  1. Re-set `ONE EVALUATION` on the upper-right side of the chord (between u 0.50 and 0.75) so no letter touches `GRAIN BOUNDARY` or the stitched lattice.
  2. Move the crimson `t T. N(0, I) / ISOTROPIC…` caption outside the ring to the right of the bullseye (u≥0.86), 5 mm clear of every crimson dash.
  3. Shorten the heavy grain-boundary bar to the first 40 % of its length so ~20 mm of the seam shows the ruled and stitched lattices meeting at their 37.4° mismatch.
