# neural-networks-cnn r02 — one-valley (mechanism) · parent: `promptplot/generative/pieces/ml.py::bauhaus_locality` (render `gallery/neural-networks/cnn/promoted/pp_cnn_dashes.png`) · 2026-09-28

Lineage: **Georg Nees, *Schotter* (c. 1968)**, order → disorder down the sheet. Here the data
provides both ends: raster noise at the foot, one peak at the head. Read top-down it is
Schotter's gradient.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-cnn/rounds/r02/piece.py \
  --fn cnn_one_valley --seed 7 --paper a4 --palette black,crimson \
  --out ~/Downloads/pp_neural_networks_cnn_one-valley_v12.png
```

- Final: `~/Downloads/pp_neural_networks_cnn_one-valley_v12.png` + `.gcode` (identical to v11 apart from the header timestamp)
- a4 portrait, drawable 10–200 × 10–287 mm, cream. Pens: 0 black, 1 crimson.
- The seed does nothing, because the piece has no randomness at all: every coordinate comes from the network. Seeds 2, 7 and 11 give byte-identical output (sha1 `65596811b611`, 24,142 raw commands).
- Files in this round: `piece.py` (the plate), `compute_maps.py` (the torch forward/backward pass, run once), `maps.npz` (374 KB, the cached arrays the plate reads).

## Mandate responses

There is no LEDGER.md or FEEDBACK.md for this slug, so no J/A/S mandates are open. The work order was the one-valley brief plus the DESCRIPTION's Weak list. Each item is answered below.

| id | mandate (DESCRIPTION.md) | status |
|---|---|---|
| brief-1 | Layer i = a real activation map at conv depth i, from a real image; ONE computation | **FIXED**. One forward pass of trained MobileNetV2 (ImageNet) on one photo. Every terrain is a stage of that pass (see Measurements). |
| brief-2 | Top peak sits where the object actually is | **FIXED**. Top = ReLU(CAM − mean) for the top-1 class. Its argmax, unit (4,3), is on the cat's muzzle. |
| brief-3 | Crimson frustum = computed receptive field of that argmax unit | **FIXED**. On each lower layer the crimson ring is the effective-RF ellipse (gradient of the unit, 50.0 % of mass). Rails join the ring extremes up to the unit's cell. |
| brief-4 | Drop the axis and per-layer labels; one title | **FIXED**. There is one title block (FROM / PIXELS / TO / MEANING) and one data line (`MOBILENETV2 . IMAGENET . P(TIGER CAT) = 0.43`). |
| brief-5 | Strong diagonal cropping the top-right; PIXELS gets the whole bottom width | **PARTLY**. The stack climbs bottom-left → top-right and the top layer crops at the right frame. PIXELS runs off the left frame and spans 10–198 mm. The summit sits 19 mm under the top frame: the crop is on the right edge, not the corner, because cropping the summit would cut the crimson apex. |
| brief-6 | Fix occlusion: crimson through the z-buffer | **FIXED**. ERF rings and summit isolines are drawn against their own layer's z-buffer. Rails are tested against both the layer they leave (hidden behind its ridges) and the layer they enter (hidden under it). |
| brief-7 | Fix flooding: row thinning on the near edge | **FIXED**. Row and column strides are chosen per layer so the nominal paper pitch is ≥ 1.5 mm; pause-resume occupancy (0.9 mm) handles local folds. Measured crowding is in Measurements. |
| W-craft-1 | Straight black chords across the crimson cap | **FIXED**. The top isolines are split per sample by pen (black outside the unit's cell, crimson inside), so no chord crosses the cap. |
| W-craft-2 | Crimson not occluded; 4-corner window becomes straight chords | **FIXED**. Every crimson mark is sampled densely along the surface and draped, so none is a 4-corner polygon. |
| W-craft-3 | PIXELS floods; EDGES crumbs | **FIXED / partly**. PIXELS is 32 scanlines at a 1.30 mm nominal pitch, with 0.0 mm of sustained crowding. The a56 and a28 meshes still break into short runs behind their own spikes. That is real occlusion of real data, but it reads as crumb. |
| W-craft-4 | Travel ≈ draw; floating debris | **PARTLY**. 122 black runs under 1.2 mm are dropped, and no mesh overhangs its unit hull. Travel is still 12.6 m against 15.3 m of draw. |
| W-concept | Textbook stacked-layers diagram, seeded noise, order asserted by labels | **PARTLY**. No labels and no noise; the terrains compose because they are one pass. Stacked slabs are still the silhouette of the Zeiler–Fergus figure. |
| W-tension | Centred column, 0.04 W stagger | **FIXED**. The stagger is now 0.08–0.12 W per layer, the bottom crops left and the top crops right. |
| W-space | Leftover bottom band; metronomic gaps | **PARTLY**. The bottom band is gone (PIXELS starts 5 mm above the frame), and the quiet zone is the left strip under the title, shaped by the stair. Gaps are "6 mm clear on the real silhouettes", so they vary with the data (4.0–10 mm) but are not composed. |
| W-hierarchy | Five similar grey smudges | **FIXED for the top**. The summit is 66 mm tall with a crimson cap. The four lower slabs are still close in weight to each other. |
| W-grid | Ragged labels, near-miss edges, colon lost | **FIXED**. Title, caption and the PIXELS crop share x = x0. The layer labels are gone. `=` renders (the font has `:` now, but it is not used). |
| W-depth | Far layers heavier than near, inverted cue | **ARGUED**. Weight now follows the data: raster at the foot, sparse unit cage at the head. There is no atmospheric falloff; hidden lines and the rails passing behind surfaces carry the depth. |

## What changed from parent

- **One computation instead of five noises.** The parent seeded fbm per layer and blurred it. r02 runs a trained CNN once and draws its stages. Morphology still coarsens up the stack, and the data does that by itself: a56 is bristly, a14 shows the two eyes and the nose as three hills, and the top is one mountain.
- **Mesh line = a row of units.** Line pitch is the stride: 224 px → 56 → 28 → 14 → 7. PIXELS is drawn as a raster (scanlines only). Every other layer is a unit-line lattice, stride-thinned only where the paper pitch would fall under 1.5 mm.
- **The frustum points the right way.** The parent's window grew upward. The dependency cone of one top unit is wide at the input and ends on one cell, so the rails now converge upward onto the unit.
- **Composition.** The labelled axis and the five labels are gone. PIXELS spans the full bottom width and crops left. The stack climbs a diagonal and the top layer crops at the right frame. A Swiss-weight title block (6 mm, 0.5 mm weight) sits in the top-left quiet zone, flush with the frame and the PIXELS crop.
- **The one loud accent** is the crimson cap: 9 isoline arcs inside the argmax unit's 1/7 × 1/7 cell, on a 66 mm peak.

## Measurements / computations

**Network**
- Keras `mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224.h5`, re-implemented in torch functional form with Keras padding (`correct_pad`: right/bottom +1 before every stride-2 3×3).
- Input: skimage `chelsea.png` (451×300), centre-cropped to 300², bicubic to 224², scaled `x/127.5 − 1`.
- Top-5: tiger_cat 0.4290 · Egyptian_cat 0.2512 · tabby 0.1775 · lynx 0.0053 · window_screen 0.0018. Three cat classes on top is the correctness check for the port; a broken port does not produce cats.
- **CAM identity check:** mean(CAM) + bias = 8.349988448 against logit 8.349988448, exact to double precision. That holds because MobileNetV2's head is GAP + dense.
- CAM range −0.71 … 18.28, mean 8.28. Argmax is unit (row 4, col 3), centre (u, v) = (0.500, 0.643).

**Terrains (height = the value named, min–max normalised per layer)**

| layer | array | raw range | drawn as |
|---|---|---|---|
| PIXELS | input luminance 224² | 0.015–0.725 | 32 scanlines (7-px band means), 224 samples each |
| a56 | ‖block_2 out‖₂, 24 ch | 10.5–61.6 | 20 rows (stride 3) × 56 cols |
| a28 | ‖block_5 out‖₂, 32 ch | 16.2–51.9 | 15 rows (stride 2) × 28 cols |
| a14 | ‖block_12 out‖₂, 96 ch | 27.4–77.2 | 14 × 14 |
| top | ReLU(CAM − mean) | 0–10.0 | 7 × 7 unit lines + 17 isolines (gradient-stepped, 2.2 mm plan spacing, floor 0.06) |

**Receptive field of unit (4,3)**
- **Theoretical RF**, by exact interval propagation through all 52 conv layers (raw, before clipping): input rows −86…404, cols −118…372 (it covers the whole image); a56 −20…98; a28 −8…46; a14 rows 2…16, cols 0…14.
- **Numerical cross-check:** the gradient on a14 is non-zero on exactly 85.7 % of units (168/196 = 12 rows × 14). That matches the theoretical RF rows 2–13 after clipping.
- **Effective RF** (Luo et al. 2016): Σ_c |∂unit/∂A_c| at every captured layer. The crimson ellipse is its second-moment ellipse, scaled by bisection to hold exactly half the mass:

| layer | ERF centre (u, v) | radius in σ | mass held |
|---|---|---|---|
| PIXELS | (0.531, 0.643) | 1.248 | 0.500 |
| a56 | (0.519, 0.627) | 1.243 | 0.500 |
| a28 | (0.512, 0.619) | 1.248 | 0.503 |
| a14 | (0.506, 0.625) | 1.201 | 0.501 |

In normalised image space the ERF keeps nearly the same size at every depth (σ ≈ 0.22–0.24 of the image). The funnel on paper comes from the footprints shrinking, and the rails end on the one 1/7 cell. A pure Gaussian would hold 50 % at 1.177 σ; the ERF needs about 1.24 σ, so it is slightly heavier-tailed than Gaussian.

**Spacing, measured on the gcode.** Crowding here means parallel neighbours (|cos| > 0.93) of the same pen running side by side under 0.8 mm for at least 2.4 mm:

| band | ink | crowded length |
|---|---|---|
| PIXELS | 3.73 m | 0.0 mm |
| a56 | 3.80 m | 4.8 mm (0.13 %) |
| a28 | 1.72 m | 2.4 mm (0.14 %) |
| a14 | 1.35 m | 8.4 mm (0.62 %) |
| top | 1.67 m | 30.9 mm (1.85 %, isolines near the flat foot) |

Nominal pitches: PIXELS 1.30 mm · a56 1.86 / 1.80 mm · a28 2.20 / 3.19 · a14 2.05 / 5.96 · top 5.24 / 15.2 (rows / depth-running columns).

**Placement.** Each layer's origin is solved so its lower silhouette clears the previous layer's upper silhouette by 6 mm, column by column. Resulting origins (mm): (2.4, 10.7), (25.2, 59.8), (44.2, 101.5), (59.4, 147.7), (63.2, 187.4).

## Plot budget

- Draw 15.28 m · travel 12.57 m (0.82 × draw) · 26,641 commands · 1,248 pen lifts · 2 pens (one swap).
- Estimated 12.7 min at the render's F2200. At Leo's F600 with 1 s dwells, expect about 25 min of draw plus about 40 min of lift dwells and travel: roughly 65–70 min.
- Ink stays within x 10–200, y 10–286.2. The right edge is the deliberate crop at the drawable boundary.

## Self-critique (rubric, honest)

| dimension | score | why |
|---|---|---|
| Hierarchy | 7 | The 66 mm peak with its crimson cap wins at 3 m and the title block is second. The four lower slabs are near-equal in weight to each other. |
| Grid & alignment | 7 | Title, caption and PIXELS crop share x0; the top layer crops at the right frame. The layer left edges form a data-driven staircase, not a ruled one. |
| Tension & asymmetry | 7 | A working diagonal with crops on both sides. The top-right corner itself is not cut. |
| Negative space | 6 | The left strip under the title is shaped by the stair. Inter-layer gaps come from a formula, not a composition, and the bottom margin is thin. |
| Craft for pen | 7 | Pitches are measured and crowding is ≤ 1.85 % per band. a56 and a28 break into short runs behind their own spikes, and their crimson ERF rings are chopped the same way. Travel is high. |
| Concept legibility | 6 | This is a real single computation with no labels, and the morphology gradient plus the converging crimson carry it. The silhouette is still "stacked feature maps". The cat is invisible, so the joke (a 43 %-confident tiger cat that is actually a tabby) lives only in the caption. |
| Depth | 7 | True hidden lines within each layer, and rails pass behind and under surfaces. No atmospheric falloff. |

**Single worst thing:** the lower four slabs are equal-weight parallelograms stacked with near-uniform gaps. The plate still has the Zeiler–Fergus silhouette, and the thesis is carried by the crimson thread and the data rather than by the form.

## Engine requests

1. `Scene3D.field(SX, SY, DEP)`: rasterise the active z-buffer without drawing a mesh. I called the private `scene._rasterize` so I could draw scanlines only (PIXELS), strided unit lines and densely sampled isolines against the same buffer. `surface()` always draws both grid families at every vertex.
2. Multi-buffer visibility, e.g. `scene.visible_in(field_id, …)` or saving and restoring an active field. Rails between two layers must pass both layers' buffers. I did it by recording public `visible()` flags against layer i, then drawing against layer i+1.
3. `lines(mode="pause_resume")` takes one occupancy for everything drawn in the call. A mesh wants one occupancy per family, so that crossings never read as crowding. Today that needs two calls.
