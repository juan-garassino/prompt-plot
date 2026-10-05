# DIFFUSION AS TOPOGRAPHY — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/diffusion_topo` |
| current render | `gallery/studio/diffusion_topo/current/pp_diffusion_topo_v1.png` |
| source | `studio/diffusion-topography/rounds/r01/piece.py::diffusion_topography` |
| reference | `studio/diffusion-topography/ref/reference.png` (1448×1086) |
| paper · pens | a4 landscape, cream · 0 dodgerblue = data blob x₀ + forward flow · 1 goldenrod (ochre) = noise tangle x_T + reverse flow + two stand-in "red" rule marks · 2 forestgreen = sample terrain x̂₀ · 3 black = score field, schedule, type, furniture, dots |
| status | unreviewed (no FEEDBACK.md, no BRIEF.md) · 4 renders on disk (1 plate + 3 comparison tools: `flat`, `cmp` side-by-side with the reference, `overlay` 50/50 blend) |

## In one line
Diffusion drawn as **a constellation of four contoured fields joined by flow bundles** — data blob (blue) → score field (black nest) ← noise tangle (ochre) → sample terrain (green) — the reference poster reproduced element-for-element in reference pixel space.

## What is on the sheet
Positions normalised to the sheet (u → right, v → down). Four masses sit roughly at the corners of a diamond around a central score field, with scattered drafting furniture filling the gaps.

**1. Score field (dominant, centre-left, u 0.32–0.63, v 0.28–0.58).** A black nest of ~16 solid, continuous, slightly irregular closed contours around one eye at u≈0.46, v≈0.42 (solid core ≈0.15 sheet wide), wrapped by ~7 outer **dashed** contours that bulge into a star-lobed outline, the right lobe reaching u≈0.63. Seven black dots sit on the rings. A vertical dashed spine passes through it at u≈0.48; two black plus/crosshair marks sit *on* the right half of the nest (u≈0.50–0.53, v≈0.44–0.48); a short black arrow rises from its top-left (u≈0.43, v 0.28–0.33). Label `score` / `sθ(xt , t)` at u 0.52–0.57, v 0.31–0.33, set on top of the dashed contours (the ε glyph reads as an `s`).

**2. Schedule (under the score field, u 0.36–0.58, v 0.60–0.64).** A flat stack of ~7 nested black ellipses, eccentric toward the right, with a dense black dot scatter in the right half and a dotted axis `t = 0` … `t = T` through them; label `schedule` at u≈0.48, v≈0.66. The dashed spine continues below it with three spiral dots (v 0.72, 0.87, 0.96) and a plus mark (v≈0.84).

**3. Data blob x₀ (upper-left, u 0.09–0.25, v 0.08–0.30).** A blue amoeba of ~15 dotted/dashed concentric contours converging on two centres; label `data` / `x_0` at its top-left edge (u 0.10–0.14, v 0.09–0.12). Four black dots on it with short black vectors pointing right.
- **Forward flow**: from the blob, 2 solid + 3 dashed blue curves with small blue dots arc down-right into the score field (u 0.25–0.45, v 0.15–0.45); a second blue dashed bundle leaves from the lower-left (u≈0.20, v≈0.56) and rises into the score field's underside. Label `forward` / `q(xt | x0)` at u 0.26–0.34, v 0.31–0.33.

**4. Noise tangle x_T (upper-right, u 0.61–0.84, v 0.06–0.31).** A ball of ~36 wandering ochre closed loops, densest at a centre u≈0.76, v≈0.17, a few dashed; black dots with a fan of black lines from a big dot. Label `noise` / `xT` at u 0.88–0.91, v 0.12–0.14.
- **Reverse flow**: ochre solid and dashed curves with small ochre dots drop from the tangle to the score field's right lobe and down to the sample terrain (u 0.55–0.80, v 0.30–0.68). Label `reverse` / `pθ(xt-1 | xt)` at u 0.73–0.80, v 0.44–0.47.

**5. Sample terrain x̂₀ (lower-right, u 0.57–0.83, v 0.66–0.83).** ~20 green hidden-line ridgelines stacked in shallow perspective with two needle peaks at u≈0.68 and u≈0.71 (v≈0.66), tails collapsing to single lines left and right; three black ridgelines form its front edge and extend as a black wavy line to a small rectangle at u≈0.85. Five black dots on the surface. A vertical black rule with a T-cap (u≈0.74, v 0.67–0.88) and a vertical dashed line (u≈0.62) cut through it; a black dashed curve loops under it (u 0.61–0.70, v 0.80–0.85). Label `sample` / `x̂0` at u 0.78–0.82, v 0.70–0.73.

**6. Type.** `DIFFUSION` / `AS` / `TOPOGRAPHY` spaced caps at u 0.075–0.19, v 0.77–0.82; short rule; `FROM NOISE` / `TO STRUCTURE` (v 0.86–0.87). Bottom right, right-aligned to u≈0.92: `GENERATIVE` / `FIELDS` / `IN CONTINUOUS TIME` over a long rule (v 0.84–0.875), a stack of tiny marks at its left.

**7. Furniture (black unless noted).** A large C-arc with a crosshair and big dot at left (u 0.12–0.17, v 0.45–0.60); a tall arc at the right edge (u 0.87–0.92, v 0.30–0.60); a quarter-arc with a tick at lower-left-centre (u 0.24–0.32, v 0.60–0.72); a dashed arc over the top centre with a hooked right-angle marker (u 0.40–0.60, v 0.07–0.21); a crosshair rule at upper-left (u 0.07–0.14, v 0.34–0.40) beside two short ochre dashed verticals (the reference's red marks); dotted verticals, ~8 plus marks and ~15 loose dots.

## The science it encodes
From the `piece.py` docstring and `rounds/r01/NOTES.md`: **this is a reproduction, not a computation** — "fidelity is the only score; nothing here is invented". The four fields are authored Gaussian mixtures fitted by eye to the reference raster (8-term blob, 13-term score, 14 bump/trough terrain terms), not a diffusion model. The intended reading: forward process q destroys x₀ into x_T, the score field ε_θ(x_t, t) is what is learned, the reverse process p_θ rebuilds a sample x̂₀, the ellipse stack is the noise schedule over t. Genuine craft contribution: `_even_levels` steps contours by `distance × quantile_0.82(|∇F|)`, so rings sit a fixed physical distance apart and stay continuous (later adopted into the rubric as CONTOUR LEVELS BY GRADIENT). Measured overlap within 0.8 mm: blue 11.9 %, green 14.6 %, black 21.5 %, ochre **47.5 %** (the tangle's crossings, left unthinned on purpose).

## How it got here
One round of 14 internal iterations against a purpose-built comparison renderer (the three trials: `flat` = the plate re-drawn in reference pixel space, `cmp` = side-by-side with the reference, `overlay` = 50/50 blend). The first eight iterations flooded or crumbed the contours until gradient-stepped levels fixed them. Recorded gaps vs the reference: ~28 blob rings and ~40 terrain profiles in the raster vs 15–17 and 24 here (pen limit), no serif/italic type, `ε θ ^ _ |` glyphs supplied locally, red rule marks drawn in ochre, grey tonal weight replaced by dashes. No feedback from Juan.

## Keep — what works
- **Continuous gradient-stepped contours** in the score nest (u 0.40–0.55, v 0.33–0.52) and the blob — every ring unbroken at ~0.9 mm; the solid inner nest vs dashed outer lobes gives the score field a real near/far reading.
- **Four colours = four states**, each on its own mass: blue data, ochre noise, green sample, black learned field — a clean colour-to-meaning map.
- **The sample terrain's hidden-line ridgelines** with tails collapsing to single lines — the one element with genuine depth.
- **The noise tangle** reads as individual wandering loops, not a solid ball.
- **Diagonal reading**: blob (top-left) → score (centre) and tangle (top-right) → terrain (bottom-right) makes an X-shaped traffic through the centre, with the title quiet at bottom-left.

## Weak — what doesn't
- [concept] A node-and-link map of four labelled fields with arrows and a schedule inset — a science-figure schematic; nothing is computed, so the plate cannot even claim exactness.
- [space] Two plus/crosshair marks sit on the score nest's right half (u≈0.50–0.53, v≈0.44–0.48), the dashed spine runs through the nest and the schedule, and the `score` label is set on the dashed contours — collisions in the plate's focal element.
- [space] Blue forward curves cross the score field's dashed and solid rings (u 0.40–0.46, v 0.30–0.45); a vertical rule and a dashed line cut through the sample terrain (u≈0.62, 0.74).
- [concept] ~30 pieces of furniture (arcs, plus marks, dotted verticals, loose dots, the rectangle) carry no data.
- [hierarchy] Score field, tangle, blob and terrain are all ~0.15–0.25 sheet wide — four equal masses, no 3:1 dominant.
- [craft] The ochre tangle has 47.5 % of its ink within 0.8 mm of another stroke — on paper with a real pen this ball will saturate at its centre (u≈0.76, v≈0.17).
- [craft] The reference's crimson rule marks are faked in ochre, blurring the ochre = noise meaning.
- [grid] Labels sit at arbitrary offsets from their masses (`noise xT` floats 0.04 right of the tangle; `sample x̂0` beside the terrain's slope).

## Next versions
- **computed-fields** (mechanism) — Keep the four-field constellation but compute it: a 2-D Gaussian-mixture x₀, its exact forward marginals, the exact score, and a real probability-flow sampler; the blob is p₀'s level sets, the tangle is real Brownian paths, the score nest is |∇log p_t| contoured with the gradient-stepped ladder, the flows are actual trajectories, and the terrain is the sampled density. Delete all furniture. Same composition, now true.
- **one-field** (abstract) — Transpose to a single field that is contoured THREE times on one sheet: the same landscape drawn at t = 0 (tight blue nest, left third), t = 0.5 (black, half-melted rings, centre) and t = T (ochre loops, right third), laminated left→right with the rings of one stage flowing continuously into the next. The order is nested → dissolving; the viewer reads "form from noise" as one gradient of contour discipline, with no arrows at all.
- **terrain-hero** (lens) — Make the green sample terrain the dominant mass (0.7 sheet width, cropped at the bottom and right), its ridgelines drawn by the reverse sampler's actual rows, with the data blob and noise tangle reduced to small thumbnails on its horizon. Hierarchy and depth jump; the schematic network disappears.
- **If only iterating:**
  1. Remove the two plus/crosshair marks and the dashed spine from inside the score nest (u 0.40–0.63, v 0.28–0.58) and set `score / εθ(xt, t)` outside the outermost dashed contour.
  2. Cut the ochre tangle to ~20 loops or apply `limit_ink_density` at 0.5 mm so no spot at its centre (u≈0.76, v≈0.17) takes more than two passes.
  3. Delete the vertical T-rule and dashed line crossing the sample terrain (u≈0.62 and 0.74) and the loose furniture arcs at u 0.12–0.32, v 0.45–0.72, leaving that lower-left field as shaped empty paper under the title.
