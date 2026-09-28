# GAN — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/gan_plate` |
| current render | `gallery/studio/gan_plate/current/pp_gan_plate_v2.png` |
| source | `studio/gan-plate/rounds/r01/piece.py::gan_plate` |
| reference | `studio/gan-plate/ref/reference.png` |
| paper · pens | a4 landscape (297×210 mm) · 0 crimson, 1 dodgerblue, 2 goldenrod, 3 olive = one stage-blob each + matching flow curve + kernel tile · 4 black = black stage-blobs, real-data blob, latent stipple, all type, furniture (crosses, dashed arcs, verticals), most flow curves |
| status | unreviewed (no feedback on file) · 2 renders on disk (v1 trial, v2 current) |

## In one line
A GAN drawn as a **laminar** left-to-right pipeline — latent cloud → five generator blobs → x̂ → five discriminator blobs → a fork to D(x̂)/D(x) — a measured reproduction of a reference schematic in which each "layer" is a 3-lobed contour blob whose knot is threaded by coloured flow curves.

## What is on the sheet
- **The main row (dominant mass).** A horizontal chain of 11 lobed blobs threaded on flow curves across v≈0.30–0.46, u≈0.07–0.86.
  - Far left, the **latent cloud**: a round stipple of ~300 black dots, ~0.07 of sheet width, centred u≈0.08, v≈0.40. Above it `z ~ p(z)` (u≈0.08–0.12, v≈0.27) with a dotted vertical tick below, beneath it `latent space` (v≈0.48).
  - **Generator stages**: five blobs at u≈0.21, 0.26, 0.32, 0.37, 0.42 on v≈0.37, colours crimson · black · blue · gold · black, each ~0.05 of sheet width and ~0.17 of sheet height. Every blob is three-lobed with its dominant lobe pointing straight UP (a tall tulip/blade), filled with concentric dashed rings that follow the outline and tighten to a black knot.
  - **x̂** (generated sample): a crimson blob, slightly larger and lower, at u≈0.49, v≈0.39; `x̂` label above (u≈0.50, v≈0.26); `generated` / `sample` below (u≈0.47–0.52, v≈0.49–0.52).
  - **Discriminator stages**: five blobs at u≈0.62, 0.68, 0.73, 0.78, 0.84 on v≈0.40, colours blue · black · gold · black · olive, same construction.
  - **Flow**: between consecutive knots, 3–5 curves (solid black, dashed crimson/blue, solid gold/black) weave as sinusoidal lenses that pinch at each knot. Right of the olive blob a black bracket forks to `D(x̂)` / `fake` (u≈0.93–0.96, v≈0.37–0.40) and `D(x)` / `real` (v≈0.48–0.51) with a black vertical bar between (u≈0.93, v≈0.41–0.47).
- **Real data (second mass).** A large black 3-lobed blob, ~0.11 of sheet width, centred u≈0.20, v≈0.57, knot at its right. `x ~ p_data (x)` at u≈0.08–0.19, v≈0.56 and `real data` beneath (u≈0.09–0.12, v≈0.62). From its knot a bundle of 6 curves (black solid/dashed, blue, gold) sweeps right and up in an S to meet the first discriminator knot at u≈0.62, v≈0.40, passing under the x̂ blob.
- **Headings.** `Generator  G` (u≈0.19–0.25, v≈0.19) with `z → x̂` beneath (v≈0.21); `Discriminator  D` (u≈0.63–0.69, v≈0.19) with `x → [0 .1]` beneath (the comma of `[0,1]` renders as a period). Row captions `nonlinear transformation` / `in latent space` (u≈0.19–0.28, v≈0.50–0.52) and `nonlinear decision function` (u≈0.63–0.72, v≈0.52).
- **Losses.** `L_D = − [log D(x) + log(1 − D(x̂))]` and `L_G = − log D(x̂)` at u≈0.64–0.81, v≈0.60–0.63; the opening bracket collides with the `l` of `log`.
- **Kernel strip.** `kernels / filters` (u≈0.13–0.21, v≈0.69), then five columns at u≈0.15, 0.19, 0.23, 0.27, 0.31 (each ~0.03 of sheet width), colours crimson · black · blue · gold · olive: a 3×3 grid tile over a square containing a small blob. The grid cells hold scattered tiny marks that render as asterisks and little "c" hooks rather than weight dots. A short dash under each column (where the reference has a dot). `3 × 3 kernels (example set)` at v≈0.86.
- **Title and corners.** `GAN` (spaced caps, u≈0.05–0.11, v≈0.07) with a rule under it, then `generative` / `adversarial` / `networks` (v≈0.13–0.16). Top-right text block `adversarial` / `learning` / `representation` / `synthesis` (u≈0.88–0.96, v≈0.12–0.14) over a rule, and a small open square at u≈0.92, v≈0.21. Bottom-right block `local patterns` / `hierarchical features` / `global structure` / `realistic samples` (u≈0.87–0.95, v≈0.83–0.86). `PEN PLOTTER` + rule at u≈0.05–0.19, v≈0.90.
- **Furniture.** Plus crosses at u≈0.44 v≈0.12, u≈0.46 v≈0.63, u≈0.65 v≈0.88, and a large L-cross at u≈0.05, v≈0.70. Dashed semicircle arcs at u≈0.18–0.26 v≈0.10–0.16 (top-left), u≈0.55–0.63 v≈0.12–0.16 (top-centre), u≈0.38–0.44 v≈0.67–0.75 (lower centre), u≈0.83–0.87 v≈0.62–0.66 (right). Dotted horizontal runs and dashed vertical ticks scattered at stage boundaries (u≈0.16, 0.37, 0.56, 0.62, 0.81, 0.95).
- **Quiet zones.** Lower-right quadrant u≈0.50–0.85, v≈0.68–0.95 is open paper broken only by one arc and one cross.

## The science it encodes
Per `studio/gan-plate/rounds/r01/NOTES.md`: "Exact recreation of `studio/gan-plate/ref/reference.png`. Reproduction, not design." Nothing is computed from a GAN; every position is a pixel probe of the reference mapped affinely onto the drawable area. What is engineered is the mark: `_blob` rings are iso-lines of a normalised radius on a conical cusp, gated perpendicular to the contour at a 0.8 mm floor (flooded necks fell from 37 % to 19 % of ink), per-angle ring survival, golden-ratio bead phase, a polar-LOD spoke fan at the core. The losses printed are the standard GAN non-saturating losses; the kernel tiles and the corner word lists are decoration carried over from the reference. The "flow" between stages carries no data.

## How it got here
- **v1** (trial): blobs broader with lobes mostly sideways, each knot showing a visible radial spoke fan; latent cloud a sparse starburst; kernel cells each one small glyph + centre dot; real-data bundle leaves its blob as a wide fan.
- **v2** (current): blobs taller with a dominant upward lobe (so every stage reads as a tulip/blade — the thing the notes say to avoid, "lobes never point straight up"), spoke fans gone, rings denser and dashed; latent cloud a dense round stipple (closer to the reference); kernel cells filled with scattered marks; real-data blob larger and the bundle rerouted under x̂ to clear the caption. Gained reference fidelity in the stipple and bundle routing; lost the knot fans and the compact lobe orientation.
- No feedback from Juan on file.

## Keep — what works
- The single left-to-right rhythm of tangent blobs pinched by flow lenses at every knot (v≈0.37–0.40) — the one strong visual order on the sheet.
- Colour sequencing across the row (crimson · black · blue · gold · black | blue · black · gold · black · olive) — colours alternate with black so no hue clumps.
- The real-data bundle's long S from u≈0.20 v≈0.57 up to the first discriminator knot — the only diagonal on the plate and it gives the row a second entry point.
- Perpendicular-gated ring spacing inside blobs — no blob floods even at the knot.
- The measured, reference-exact layout method (`Ref` affine map) — reusable for any faithful round.

## Weak — what doesn't
- [concept] It is a textbook schematic: labelled stages, arrows (`z → x̂`, `x → [0 .1]`), loss equations, a legend of kernels. By § 6 NO SCHEMATICS it fails outright; the adversarial game (two players pulling against each other) is not shown anywhere — the plate reads as one feed-forward pipe.
- [hierarchy] Eleven blobs of the same size at one height; the real-data blob is the only larger mass and it sits off the row. At 3 m nothing dominates.
- [craft] Kernel cells fill with asterisk/"c" glyph marks (u≈0.15–0.31, v≈0.73–0.78) instead of weight dots; under-column dots render as dashes; `[0 .1]` for `[0,1]`; the `[` of `L_D` collides with `log`.
- [grid] Furniture checklist: crosses, arcs, dotted runs and dashed verticals are scattered at reference pixel positions with no shared line; the top-right square (u≈0.92, v≈0.21) and the L-cross (u≈0.05, v≈0.70) float.
- [craft] Upward blade lobes on every stage (v≈0.28–0.35) — the orientation the notes explicitly identify as wrong under the vertical stretch.
- [space] The lower-right quadrant is empty because the reference is, not because it was composed; the kernel strip and the formulas are two unrelated islands.
- [depth] Entirely flat and undeclared: blobs, flows and tiles sit on one plane with no occlusion except flows passing "behind" blobs.
- [tension] Symmetric horizontal band across the centre with even margins — the "subject floating dead-centre" failure mode.

## Next versions
1. **faithful-v3** (faithful) — Finish the reproduction honestly: rotate every blob so a lobe runs horizontally (0/120/240 or 60/180/300), restore the knot spoke fans from v1, render kernel weights as sized dots (`_dot` radius = weight) with dots, not dashes, under each column, fix `[0,1]` and the `L_D` bracket, and add the reference's missing thin vertical centre divider with its two dots. Scores higher on craft and fidelity; stays a schematic by design.
2. **tug-of-war-interference** (abstract) — Drop the pipe. Transpose to INTERFERING: the generator's five blobs and the discriminator's five blobs become two ring-sources on one axis whose contour families interfere; the x̂ knot sits where the two families' rings are tangent, and the real-data blob's rings pull the discriminator source. The kept element is the lobed-ring mark and the colour sequence; what changes is that the two players visibly act on the same field. Beats v2 on concept and hierarchy.
3. **real-vs-fake-lens** (lens) — One giant real-data blob (0.45 of width, cropping the left edge) and one giant x̂ blob overlapping it at right, rings of both in their own pens; where rings coincide the discriminator is fooled. The generator/discriminator stage chains shrink to two thin strips of small blobs feeding each from above and below. Turns the plate into two masses with a readable overlap instead of eleven equal tokens.

**If only iterating:**
- Re-orient every stage blob so no lobe points straight up (dominant lobe at 0° or 180°); test: no blob is taller than 1.4× its width.
- Replace kernel-cell glyph marks with one filled dot per cell sized by a weight, and turn the five under-column dashes into dots; test: the tiles read as 3×3 weight matrices at 1 m.
- Put crosses, arcs and the top-right square on the stage-boundary verticals (u≈0.16, 0.56, 0.95) so every furniture element shares an axis with a stage; test: each piece of furniture aligns to a row or column line within 1 mm.
