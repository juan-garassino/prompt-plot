# convolutions r02 — real-kernel (mechanism) · parent: r01 · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r02/piece.py \
  --fn convolutions_real_kernel --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson,dodgerblue,olive \
  --out gallery/studio/convolutions/current/pp_convolutions_real-kernel_v9.png
```

- final PNG: `gallery/studio/convolutions/current/pp_convolutions_real-kernel_v9.png`
- final GCODE: `gallery/studio/convolutions/current/pp_convolutions_real-kernel_v9.gcode`
- seed 7 (seeds 3 and 11 checked: `pp_convolutions_real-kernel_seed{3,11}_v7.png`; the seed only
  moves the X wobble, and the Y still comes out clean)
- self-rounds: v1…v9 on disk, none overwritten

## Mandate responses

`LEDGER.md` and `FEEDBACK.md` do not exist for this slug, so there are **no open J\*/A\*/S\*
mandates**. The brief was the `real-kernel` paragraph in DESCRIPTION.md § Next versions. Below it are
the DESCRIPTION "Weak" items and "If only iterating" fixes, answered as if they were mandates.

| id | mandate | status |
|---|---|---|
| brief | compute it: real kernels, real conv, true iso-contours; tiles = signed Ben-Day 5x5 | FIXED: all of it is computed (see Measurements) |
| W-concept-2 | nothing is computed; feature maps are not K*X | FIXED: maps = `K_i * X` for Sobel-x / Gaussian / Gabor-0, Y = output of the 5-layer stack |
| W-concept-4 | scatter dots, brackets, plus marks, hollow square carry no data | FIXED: every one deleted. The dots left on the sheet are kernel taps, pixel taps or ERF values |
| W-craft-5 | tile starbursts read as mud; crossed-dash scribble in X | FIXED: tiles are Ben-Day kernels (no rays); smudges/scribbles cut |
| W-craft-6 | dashed ellipse makes a `>` pointer at K | FIXED: the ellipses are cut (they carried no data) |
| W-space-7 | stride block jammed in corner; second spine cuts through Y | PARTLY: the second spine is deleted. The block stays on the u = 1 anchor, mirroring the title on u = 0, and it now states the real hyper-parameters (`stride 1 / padding 2 / dilation 1 / channels 1`) |
| W-concept-1 | pipeline schematic (§6) | ARGUED: the brief keeps the layout. The twist is new: the network's output IS the letter Y, which pulls it off the textbook figure |
| W-tension-3 | bilateral symmetry | DEFERRED: "same layout" brief; the `sliding-window` / `receptive-cone` siblings own this |
| W-hierarchy-8 | hairline type, no dominant | DEFERRED: layout thesis, not this one |
| W-depth-9 | undeclared flatness | ARGUED / DECLARED: the plate is flat on purpose (Pop Ben-Day kernels + contour maps). Depth comes only from connectors passing behind tiles |

## What changed from parent

- **The output became its own label.** X is re-harmonised so its lobes point up-left, up-right and down,
  with unequal lobe sizes so it reads as a blob and not a letter. A ridge detector on a distance field
  fires on the medial axis, and this trefoil's medial axis is an upright **Y**. The olive output on the
  right is literally the letter, so the "Y" glyph label is gone. It is replaced by an `output y`
  crosshair that mirrors `input x`.
- **Strip = a real 5-layer CNN.** Five 5x5 kernels (blur · ridge · blur · ridge · blur), each drawn as
  signed Ben-Day discs (area ∝ |w|/max|w|, crimson +, blue −), with names above the tiles.
- **New row under the strip: the activation after every layer** (olive thumbnails). You can watch the
  trefoil thin into the Y one real layer at a time. This is the "every ring on the right is caused by
  the rings on the left" proof, made visible.
- **The kernel's real footprint on X**: a 7.5 mm window holding 25 tap dots at the 1.5 mm pixel pitch.
  X's rings are knocked out under it, and the input fan leaves from its edge.
- **Kernel bank = the 9 real kernels** the plate draws from (edge / blur / Gabor rows). The three used
  by the feature maps carry an inner double keyline.
- **Receptive field rebuilt as the stack's real RF against depth.** The dashed triangle is the
  theoretical field (+-2 px per layer, labelled 5 · 9 · 13 · 17 · 21 px). The rows of dots are the
  exact composite |K| marginal at each layer (Ben-Day). The three curves are the exact 50 / 80 / 95 %
  central-mass half-widths (95 % dashed). The effective field is mostly the white inside the
  triangle, which is Luo et al.'s finding, drawn.
- **Pens re-meant**: sign, not identity. Crimson = positive weight or response, blue = negative,
  olive = post-σ activation, black = X and structure. The colour still travels left to right:
  black X → crimson/blue kernels → olive Y.
- Deleted: 5 dashed ellipses, 2 dashed over-arcs, ~34 scatter dots, 4 quarter brackets, 4 plus marks,
  2 squares, the tile droplines, the second spine, blob smudges, and the dots riding the connectors.
- Font gaps from r01 are fixed centrally (`σ`, `·`, `∗` are in the font now). `_sigma()` is deleted and
  the labels use real glyphs.

## Measurements / computations

**Network.** Pixel = 1.5 mm, field grid 0.375 mm, taps dilated ×4 on that grid. This is exact: the
fine result is the union of 16 interleaved stride-1 CNNs on shifted 1.5 mm lattices, with no
interpolation. Zero padding is 17 mm (> the 10 px half-field). The grid is 239×213. X = distance to
the boundary + fbm wobble (≤ 0.285 mm), clamped ≥ 0.

Kernels (rows printed top = +y):
```
blur σ1 (sum 1)      ridge = −LoG σ1, zero-sum, max 1        sobel x /96      gabor 0° λ3.2 σ1.1 γ0.6 zero-mean
.003 .013 .022 ...   -.075 -.145 -.157 -.145 -.075           -.010 -.021 0 .021 .010    -.113 -.180 .536 -.180 -.113
.013 .060 .098 ...   -.145 -.019  .290 -.019 -.145           -.042 -.083 0 .083 .042    -.156 -.261 .857 -.261 -.156
.022 .098 .162 ...   -.157  .290 1.000  .290 -.157           -.062 -.125 0 .125 .062    -.176 -.297 1.00 -.297 -.176
```
Stack = blur1 → ridge → blur1 → ridge → blur1.3, ReLU after each layer, no bias.

| layer | max activation | share of X's interior that ReLU zeroes |
|---|---|---|
| X | 12.71 | — |
| 1 blur | 11.44 | 0 % |
| 2 ridge | 2.62 | **43.7 %** |
| 3 blur | 2.09 | 0 % |
| 4 ridge | 1.58 | **68.3 %** |
| 5 blur = Y | 0.93 | 0 % |

**Y is X's medial axis (the check).** The axis = where the distance field's gradient magnitude
collapses below 0.75 with D > 2 mm. For the Y crest (Y ≥ 0.6 max), the median distance to the axis is
**0.75 mm** (p95 1.88 mm; the pixel is 1.5 mm). **91 %** of the axis lies within 2 mm of the crest.

**Receptive field (exact).** Composite |K| variances in px² by depth: 0, 1.270, 2.659, 3.584, 4.973,
5.897. So the effective σ goes 0.29 → 1.16 → 1.66 → 1.91 → 2.25 → 2.45 px, against a theoretical
half-width of 10 px at depth 5. The 50 / 80 / 95 % half-widths at depth 5 are 1.67 / 3.17 / 4.78 px,
so **95 % of the influence sits inside 48 % of the theoretical field**.

**Feature maps.** Map ranges: Sobel −2.03…+2.04, blur 0…11.44, Gabor −3.87…+7.28. The maps are drawn
at 0.388× the X scale. Ladders use the gradient rule at the 60th percentile, starting at ±0.75 step
(so the crimson and blue families stand 1.5 steps apart across the zero line). The engine `Occupancy`
grid pauses and resumes any contour that crowds an earlier one. Sliver islands (mean width 2A/P below
the floor) are dropped.

Measured minimum gaps between different polylines (0.3 mm resample, chain junctions excluded):

| family | min | median |
|---|---|---|
| X rings | guarded by `_guard_spacing` 0.80 (the r01 method, unchanged) | — |
| Y rings | 0.76 (tip of the stem eye, where one contour turns back on itself) | 0.97 |
| edge map (+ / − / both) | 0.88 / 0.90 / 0.88 | 1.70 / 2.30 / 1.70 |
| blur map | 0.86 | 0.91 |
| gabor map (+ / − / both) | 3.75 / 2.26 / 0.89 | — |
| RF curves | 1.68 | 3.85 |
| thumbnails 1/2/3 (4, 5 are single contours) | 1.35 / 0.90 / 0.88 | — |

**Y level ladder.** Levels come from the stem's cross-section profile, one level per 0.95 mm of
distance from the crest, which gives 6 levels. Uniform levels bunch on a bell-shaped flank, and the
gradient rule leaves the crest bare; both were tried in v2–v4 and rejected.

## Plot budget

| | |
|---|---|
| draw | 10.06 m (black 5.40 · crimson 2.25 · blue 0.89 · olive 1.56) |
| travel | 6.97 m |
| commands | 47,743 · 1,446 pen lifts |
| pens | 4 (3 swaps) |
| est. time | ~410 s at preview feed. On Leo at F600 plus dwells, expect well over an hour |
| ink bbox | inside the 13 mm frame (the reported X/Y 0 is the pipeline's final park move) |

Compared with r01: 54 % of the draw length and 38 % of the commands. The saving is the cut decoration
and the 25 whorls.

## Self-critique (rubric, honest)

| dim | score | why |
|---|---|---|
| Hierarchy | 6 | X (dense black) dominates, and the Y is a clear second. Hairline type still does no work |
| Grid & alignment | 8 | r01's anchors kept (u = 0 / 0.5 / 1, shared baselines). The double keyline was moved inside so the u = 0 edge stays exact |
| Tension & asymmetry | 4 | still the bilateral blob / strip / blob layout (the brief said keep it) |
| Negative space | 6 | the band above the strip is now a large unshaped quiet zone. It used to hold the decorative ellipses. It reads calm, not designed |
| Craft for pen | 8 | measured gaps ≥ 0.86 mm except one self-turning eye tip (0.76); discs spiral-filled at 0.34 mm |
| Concept legibility | 7 | X → five layers → the letter Y lands at a glance, and the thumbnails prove each step. It is still a pipeline figure |
| Depth | 5 | declared flat; only the connectors-behind-tiles overlap is left |

**Single worst thing:** the feature maps. They are real, but at 0.388× scale the edge and Gabor
maps hold only 1–2 contours per sign. The lower-right zone is the lightest, least legible part of
the sheet: at 1 m they read as squiggles in boxes. The next move is to crop each map to the part of
X its kernel responds to, instead of showing the whole blob at 0.39×.

## Engine requests

- `policies.enforce_line_spacing` (via r01's `_guard_spacing`) deletes the curved stretches of
  well-spaced contour rings when they are drawn at small scale: on the 20 mm feature maps it left
  only the straight runs. I worked around it locally with `scene3d.Occupancy` pause-resume, which
  behaves correctly. Worth a look.
- A native `pause_resume(polys, sep)` for plain 2-D polyline families (Occupancy is only exposed
  through `Scene3D.lines`). My `_pause_resume` is a 30-line copy of that pattern.
