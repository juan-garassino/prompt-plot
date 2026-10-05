# Science critique — neural-networks-cnn r05 · machine learning (convolutional networks, receptive fields) · 2026-09-29
render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.png (+ .gcode: 16,432 cmds; pen0 teal 442 polylines 1,327.8 mm · pen1 gold 2 polylines 166.1 mm · pen2 red 2 polylines 410.1 mm · pen3 black 1,149 polylines 3,612.5 mm)

Process note (S6, still open): there is still no `dossier.md` or `encoding.md` for this slug, so there are no §7 check numbers and no §4 lies list. The checks below come from the HANDOFF claims and an **independent recompute**: a fresh TF 2.16.2 MobileNetV2/ImageNet in a throwaway uv env, run on skimage `chelsea` (centre-crop 300², PIL bicubic to 224²), with Σ_c|∂CAM_tiger_cat(4,3)/∂A| tapped at all 20 depths (block outputs; `_add` where one exists). I did not read `reach.npz` until after the recompute, and used it only for the comparison. The lies list is the standard CNN/ERF set from r02/r03, plus one new item. Sheet coordinates are in mm, y up, hub at (23, 148.5), with r_mm = 12 + 0.65625·px.

## Check numbers
| quantity | dossier / HANDOFF | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| top-1, p | tiger_cat 0.429 | tiger_cat 0.42900 · Egyptian 0.251 · tabby 0.178 | caption "TIGER CAT 0.43", "CENTRE-CROP" | OK |
| CAM argmax / unit RF centre | (4,3) / (row 159, col 127) | (4,3). With 5 stride-2 layers padded right/bottom only, the centre is 32·i+31, giving (159, 127). Farthest pixel is 159 px (Chebyshev) | "UNIT (4,3)" in note 3 | OK |
| gradients at 20 depths | as npz | corr 1.000000 at every depth vs reach.npz, max rel. diff ≤ 4.9e-4 | — | OK |
| layers applied nL | 0,1,3,6…51,52 | Conv1 = 1, expanded_conv = 2, blocks 1–16 = 3 each, Conv_1 = 1, giving 52 | wedge sweeps: S 3.30°, block_0 6.50°, blocks 9.8–9.9° (3.27°/layer). IN is a nominal 9.25° wedge for 0 layers, so the angle axis starts at θ 9.8°, not at 12 o'clock | OK (IN width not disclosed) |
| TRF edge (Chebyshev, input px) | IN 245 · b12 112 · b16 0 | 245/244/242/240/236/232/224/216/208/192/176/160/144/128/112/96/64/32/0/0 | red line in polar: 160 (rim) for θ 0.5–108.0, then 152 / 136 / 120 / 112 / 80 / 48 / 16 / 16. That is edge + ½ stride (block 10: 144+8, 13: 96+16, 16: 0+16). Every non-arc red segment is a radial riser on a gutter ray, and red never rises | values OK. **Line ≠ note**: note 3 says "112 → 0" but the line reads 120 → 16 |
| gradient 0 outside TRF | yes, all depths | 0 non-zero cells outside TRF at every depth. Input gradient is non-zero on 100 % of pixels ("COULD SEE THE WHOLE PICTURE" is true) | legend "BEYOND IT ∂ = 0" | OK |
| half-mass radius (gold) | IN 56 · b12 43 · b16 0 | 56.1 / 55.3 / 55.7 / 54.3 / 54.4 / 51.7 / 51.2 / 51.1 / 46.7 / 46.0 / 45.5 / 44.8 / 44.3 / 43.6 / 43.0 / 33.6 / 25.5 / 14.2 / 0 / 0 | gold in polar: identical to 0.1 px, per wedge, with radial risers only | OK |
| "56 PX · 25 % OF IT" | 113² = 25.4 % | Chebyshev ≤ 56 holds 49.8 % of the mass in 25.4 % of the area | note 1 | OK |
| ring pitch = stride | yes (input binned 2 px) | 2/2/2/4/4/8/8/8/16…/32 | teal radii: IN, S and 0 step 2; blocks 1–2 step 4; 3–5 step 8; 6–12 step 16; 13–15 step 32 | OK (input 2-px bin not on sheet) |
| arc sweep = ring share / max share | yes | per-ring shares | blocks 3–5 and 8–12: every ring > 3 % matches to ≤ 0.002. **Exceptions:** ring-0 arcs are floored at 3.34° (0.70 mm, frac 0.383) whatever their share (b3 0.032, b6 0.071, b13 0.158); input rings 2–10 are floored the same way (r2: 0.065 → 0.347); the longest ring in b13–15 is drawn at 0.883, not 1.0; rings under ~3 % are dropped (IN 158/160, b0 158, b9/b10 144) | **PARTIAL** |
| longest ring = full wedge | legend says so | argmax rings: IN 58, S 56, b0 60, b6 **48**, b13–15 **32**, b16/C1 **0** (100 %) | IN 56 (0.906), S 54/56, b0 56 (0.942) and **b6's max ring 48** have no arc: they are deleted where the gold runs. **b16 and conv_1 wedges (θ 166.9–179.4) carry no teal at all.** b13–15 have no full arc (0.883) | **FAIL** |
| resolution brackets | 224/112/56/28/14/7 | IN / S,0 / 1,2 / 3–5 / 6–12 / 13–C1 | brackets read exactly that | OK |
| px scale | 0.656 mm/px, 160 = rim | — | diameter ticks at 0,16…160 px land at y 136.5 ± k·10.5 mm to 0.1 px. Dotted rings at 64.0 and 128.0 px | OK |

## Lies list
| item | status |
|---|---|
| ERF drawn as decorative, not computed | clean. Every teal ring and gold step is the recomputed gradient mass to ≤ 0.002 / 0.1 px |
| ring about the wrong unit | clean. The centre (159, 127) is recomputed from the padding |
| ERF confused with TRF | clean. Red = TRF, gold/teal = ERF, and the sheet states the gap (245 vs 56) |
| feature-map resolution misdrawn | clean. Ring pitch = stride, and the brackets are correct. Soft: the input's 2-px binning is unstated |
| data truncated / omitted | **VIOLATED.** The gold's knockout deletes whole rings: b6's longest ring (48 px, share-max 1.0, θ 68.7–78.5, r 43.5 mm), IN 56, S 54/56, b0 56. b16 and conv_1 show no teal, although their entire mass is ring 0. Rings < ~3 % of the max are silently dropped |
| scale manipulated | **VIOLATED (soft).** A 0.70 mm floor on ring-0 and inner input arcs inflates them 2.4–5.5×. The b13–15 max ring is shortened to 0.883, so ring 32 (1.0) reads almost equal to ring 64 (0.84 / 0.74) |
| quantities unlabeled / mislabelled | **VIOLATED (soft).** The legend says "ARC LENGTH", but the channel is sweep fraction, and ink length is share × radius (12 → 117 mm, up to 9.75×). The red line's +½-stride convention is unstated and contradicts note 3 (line 120/16 vs "112 → 0"). Red is clamped to the rim for IN–block 9 (true edges 245–160), and only IN is disclosed |
| NEW: ring share read as sensitivity | **VIOLATED (legibility).** Per-pixel |∂| peaks at the unit (input density ring 0 = 1.00, 60 px = 0.30, 96 px = 0.12), but perimeter weighting makes the petal fattest at 58 px. Ink-median radius is 72 px vs true half-mass 56 (IN), and 64 vs 33.6 (b13). A stranger reads a doughnut, "looks around itself", when the ERF is centre-peaked |

## Scores
truth 8 · fidelity 6 · legibility 7 · VERDICT: FAIL

The science is exactly right. The gradients reproduce to correlation 1.000000. TRF edges, half-mass radii, 49.8 % in 25.4 %, p = 0.429 and the 0-outside-TRF property all recompute. The red and gold are clean polar steps: every riser is radial, and red is monotone. Truth takes a point off because the drawn red contradicts note 3 and the legend's "longest ring = full" is false in 6 of 20 wedges.

Fidelity fails. The gold's knockout deletes the very rings that carry the most mass, including b6's maximum and the whole "one cell" endpoint (b16, C1). A floor inflates the hub arcs, and the red and gold use different conventions: red uses the cell-footprint edge, gold interpolates cell centres. At b15 that puts gold at 14.2 px, where no cell lies, with 10 % of the mass at 0 px and 90 % at 32 px.

Legibility: TRF ≫ ERF lands for a scientist. For a stranger, the perimeter-weighted petals put the "pull" 16–30 px further out than it is, and the subtitle "IT LOOKS AT A QUARTER OF IT" overclaims. Half the pull lies outside that quarter.

Note for the art critic's mandate 1: the red and gold are already arc-plus-radial-riser steps. Measured in polar, 0 of 7 red risers and 0 of 19 gold risers are off-ray, and red never rises from wedge 9 to C1. The "sawtooth" is the Cartesian look of 10° arcs with radial risers in the lower-left quadrant, not diagonal segments.

## Mandates
1. **Teal omits and inflates data (teal petals, θ 0–179.4°).**
   - *Measured.* No arc at: b6 ring 48 px (share-max 1.0; expected full 8.72° arc at r 43.5 mm, θ 69.3–78.0), IN 56 (0.906), S 54/56, b0 56 (0.942). Nothing at all in b16/C1 (θ 166.9–179.4). The expected arc there is full-wedge at the ring-0 radius (12 mm), 100 % share.
   - *Also measured.* b13–15 max ring drawn at 7.70° (0.883), not 8.72°. Ring-0 arcs are all 3.34° (0.383) against expected 0.032–0.158. Input r2 is 0.347 against 0.065.
   - *Expected.* Every ring at its exact sweep fraction. The gold must never delete a ring: trim the teal ≤ 1.2 mm either side of the gold instead of dropping it, or carry the gold on the gutter. Either no floor, or a disclosed dot glyph for sub-0.7 mm arcs. A stated cut-off for rings < 3 %.
2. **Channel label and the share-vs-density misread (legend line 1 at x 112, y 41; subtitle at y 247–257).**
   - *Measured.* Ink length ∝ share × (12 + 0.656·r). The ink-median radius is 72 px (IN), 64 px (b12) and 64 px (b13), against half-mass 56 / 43 / 33.6. Per-pixel sensitivity peaks at the unit (1.00 at 0 px → 0.30 at 60 px), yet the petal peaks at 58 px.
   - *Expected.* Relabel "ARC SWEEP = RING'S SHARE", and either add the per-pixel falloff (e.g. a mean-|∂| tick per ring) or state "RINGS GROW WITH RADIUS; SENSITIVITY PEAKS AT THE CENTRE".
   - Rewrite the subtitle to what was measured: "HALF ITS PULL FALLS IN A QUARTER OF IT" (49.8 % in 25.4 %).
3. **Red and gold use mismatched conventions, and the notes disagree with the line (red/gold, θ 108–179.4; notes at x 157, y 102–165).**
   - *Measured.* Red sits at edge + ½ stride: b12 120 (note: 112), b13–15 112/80/48 (true 96/64/32), b16/C1 16 (note: "0 px"). Gold interpolates cell centres: b15 = 14.2 px, where no cell lies. Red is clamped at 160 on 11 wedges (IN–b9) whose true edges are 245–160, and only IN's clamp is disclosed.
   - *Expected.* One convention for both lines, matching the notes. The simplest is cell centres: red b12 = 112, b16 = 0. Add a clamp glyph at the rim on IN–b9 with "EDGE ≥ 160 PX".
   - Disclose IN's nominal wedge width (0 layers, drawn 9.25°) and the input's 2-px ring binning in the caption.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S2 (caption decodes the stack) | **FIXED** (in the new encoding) | caption maps angle = conv layers 0→52, radius = Chebyshev px, ring pitch = stride. Resolution brackets 224²…7² sit over exactly the right wedges. The quantity is named (\|∂ UNIT / ∂ LAYER\|). "CENTRE-CROP" is present |
| S6 (no dossier/encoding) | **NOT FIXED** (process) | neither file exists |
| S7 (preprocessing behind p) | **FIXED** (headline) | "CENTRE-CROP" printed. Bicubic is unstated, and p varies 0.375–0.463 with the resize kernel (r02), so the value is reproducible only with the HANDOFF |
| S8 (7² CAM plane hides half its cells) | **SUPERSEDED** | the CAM plane is no longer drawn. Only unit (4,3)'s gradient is plotted. The runner-up (3,3) = 6.86 no longer appears on the sheet in any form. That is not a lie under this encoding, but it is no longer shown |
| S4, S5 | n/a | dropped with the r01 line |
| regressions | **one (data completeness)** | r03 held "every drawn map is its data, nothing clipped or omitted" after S1. r05 omits b6's maximum ring and all of b16/C1's teal (mandate 1). Every numeric truth that held in r03 (argmax, map data, ERF regions) still holds |
