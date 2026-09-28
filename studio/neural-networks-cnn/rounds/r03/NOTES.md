# neural-networks-cnn r03 — iterate · parent: r02 · 2026-09-28

Lineage: Georg Nees, *Schotter* (c. 1968). One element under one parameter. Here the element is a
hidden-line profile row, and the parameter is the map's resolution.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-cnn/rounds/r03/piece.py \
  --fn cnn_one_valley_rows --seed 7 --paper a4 --palette black,crimson \
  --out ~/Downloads/pp_neural_networks_cnn_iterate_v5.png
```

- Final: `~/Downloads/pp_neural_networks_cnn_iterate_v5.png` + `~/Downloads/pp_neural_networks_cnn_iterate_v5.gcode`
- Earlier self-rounds: v1–v4 in the same folder (kept).
- a4 portrait, drawable 10–200 × 10–287. Pens: 0 black, 1 crimson.
- The seed does nothing because the piece uses no randomness. Seeds 2, 7 and 11 give identical
  command streams (sha1 `e1014e0e27aa`, 8,453 raw commands).
- Files: `piece.py`; `maps.npz` and `compute_maps.py` are copied unchanged from r02. It is the same
  forward pass, not re-run.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | No schematics: no rails, no connector, nothing crimson between layers | **FIXED**. The dashed rails and all rail code are deleted. There are no drop-lines, no frame and no card edges. The funnel is carried only by the four ERF loops (widths ≈ 88 → 80 → 72 → 60 mm on paper) moving up and right onto the summit. |
| A2 | One mark grammar: horizontal hidden-line profile rows only, pitch ≥ 1.0 mm, no run < 3 mm, < 12,000 commands | **FIXED**. Every black mark on all five maps is a horizontal row at constant v, drawn against its own layer's z-buffer. There are no column lines, cross-mesh or ticks anywhere. Flat row pitch is 1.02 / 1.25 / 1.15 / 2.08 / 3.73 mm. The shortest run is 3.0 mm (82 black stubs under 3 mm are dropped). The final gcode has 9,826 commands. Caveat: pitch is not monotone between 56² and 28², explained under Measurements. |
| A3 | Crimson scarce; each is one closed, occluded curve; summit isolines wholly crimson; no pen switch mid-polyline | **FIXED**. Crimson is 13 polylines: 4 ERF loops, each ONE unbroken closed run (including blocks 5 and 12), plus 9 summit isolines. Each isoline is a closed level set lying wholly inside cell (4,3), drawn wholly in crimson; its back half is hidden by the peak itself. Black rows pen-up at the cap boundary (the region inside the lowest crimson level of cell (4,3)). No polyline changes pen. |
| A4 | Top terrain hidden-line regressed (far rows through the nearer hill) | **FIXED**. The top layer's z-buffer is its full field (97 v-samples), not just the 7 rows. Row 3's hill (value 0.69) is hidden behind the summit and shows only where it clears the spire's flanks. Rows 0–2 (mostly zero after the clip) vanish behind the row-4/5 hills. No black line crosses the interior of a nearer hill anywhere on the sheet. |
| A5 | Equal inter-layer gaps (≥ 10 mm) or a declared progression | **FIXED: equal**. Each layer is placed so its lowest drawn ink clears the layer below column by column by one constant G, and G is solved by bisection as the largest value that keeps the summit 3 mm under the inset line. G = 10.92 mm. Measured on the final ink envelopes: **10.9 / 10.9 / 10.8 / 10.9 mm**. |
| A6 | Title cap ≥ 6 mm below the top margin; every edge ≥ 5 mm inside, no crop | **FIXED**. Ink bbox is x 15.0–195.0, y 15.0–281.0, so every edge is 5 mm inside the frame and the title's ink top is exactly 6.0 mm under y = 287. Nothing is cropped: the frame clip was removed entirely. |
| A7 | Axis/labels gone; one flush-left type axis | **holds**. The title and three caption lines share x = 15.0, which is also the PIXELS front-left corner (x 15.0). |
| A8 | PIXELS no flood | **holds**. 38 rows at 1.02 mm. 0.5 % of PIXELS ink sits parallel within 0.7 mm of a neighbour (24.6 mm of 4.53 m). |
| A9 | Real diagonal | **holds, restated**. All five planes are right-flush at x = 195 (the inset line). The diagonal comes from left edges stepping in at 16.9 → 31.7 → 47.0 → 63.3 → 81.2 mm and from the loops walking up and right onto the spire. The title block sits top-left over an empty wedge (x 15–60, y 60–200). |
| A10 | One computation | **holds**. Same `maps.npz` as r02. |
| A11 | Title strokes doubled ≈ 0.6 mm apart | **PARTLY**. It was deferred to r04, but the fix was cheap: the two passes are now 0.8 mm apart (`weight = tip = 0.8`), so they read as inline type instead of merging. Where the font retraces a stroke (e.g. the arms of E, I) same-pen parallels under 0.7 mm remain: 241 mm of the title's 0.75 m. |
| A12 | Preview on cream | **ARGUED (tooling)**. `render_candidate.py` has no paper-colour flag. See Engine requests. |
| A13 | Face-on Molnár lattice | dropped on this line (ledger). |
| S1 | Top CAM plane whole, same basis, width ≤ 102.4 mm, monotone shrink | **FIXED**. All five planes use one basis: paper = (X + 0.5 D, 0.58 D + Z), with D = 0.45 × plane width. Plane widths are 146 / 134.5 / 123 / 111.5 / 100 mm (a constant 11.5 mm step), and front-row ink widths are 145 / 132 / 119 / 104 / 86 mm. The CAM plane spans x 88–195 and lies wholly inside. No polyline touches x = 200 (max x = 195.0). All 7 columns are drawn, including (1,6) = 0.26 and (4,6) = 0.27. |
| S2 | Resolutions as numerals, crimson key, ERF-vs-cell contrast | **FIXED**. Caption line 1: `224² 56² 28² 14² 7²: …`. Line 2: `CRIMSON: 50% OF ∂CAM(4,3) GRADIENT MASS`. Line 3: `~26% OF IMAGE VS CELL 1/49`. The printed number is **26**, not the synth's 27: the drawn 50 % ellipse on the input map covers 25.9 % of the image, computed in `piece.py` (`ERF_AREA`), both clipped and unclipped. The science critic's ≈ 27 % came from an independent TF recompute. |
| S3 | Disclose the ReLU(CAM − mean) transform | **FIXED (disclosed)**. Line 1 ends `7²:  CAM − MEAN, CLIPPED AT 0`. I kept the clip rather than drawing min-offset raw CAM because the DESCRIPTION Keep is "one smooth peak at the head". Raw CAM puts a runner-up at 0.76 of the peak and dissolves that singular read. The clipped zeros are visible as the two flat front rows of the top plane, so the disclosure has a mark on the sheet it explains. |
| S4, S5 | pooling-cascade items | dropped with that line (ledger). |
| S6 | No dossier/encoding | **DEFERRED** (process; the translator writes it). |
| S7 | Preprocessing word for p = 0.43 | **DEFERRED**. The caption is capped at 3 lines and every line is full. `P(TIGER CAT) = 0.43` stays on line 3 without "centre-crop, bicubic". |

## What changed from parent

- **One mark instead of four.** r02 drew PIXELS as scanlines, the middle maps as strided unit meshes
  and the top as mesh plus contours. Every map is now only horizontal profile rows, one per map row,
  stride-thinned only where the flat pitch would fall under 1.0 mm. Row count (38 / 28 / 28 / 14 / 7)
  and roughness carry the resolution. The sheet reads bottom to top as a dense raster that gradually
  becomes a Joy-Division ridgeline.
- **Apparatus deleted.** No rails. Crimson is now 4 loops and 1 summit.
- **The summit is the argmax unit's own hill.** With bicubic interpolation (r02), the peak's level
  sets close inside cell (4,3) only above 0.90 of the peak, because the (3,3) neighbour at 0.69
  pulls them north, and that leaves a 6 mm cap. So the 7×7 map is drawn as 49 unit hills: each unit
  is a cos² hill of radius one cell at exactly its own value, and the terrain is their p = 6 norm.
  Every row profile then peaks at its 7 unit values, and every level from 0.528 up closes inside
  the unit's own cell. The result is a 9-ring crimson spire that *is* unit (4,3). It is narrower
  than r02's cap (≈ 16 × 37 mm against 35 × 45), because the cell itself is only 100/7 = 14.3 mm.
- **Stack re-solved.** Right-flush on the inset line, constant-step widths, one constant gap,
  nothing cropped. The top plane moved from 140 mm wide (clipped) to 100 mm (whole).
- **Travel.** Runs are ordered nearest-neighbour per pen with reversal. Travel is 3.5 m against
  r02's 12.6 m.
- **Caption.** Three flush-left lines replace the one-line model credit (see S2/S3).

## Measurements / computations

Network and arrays: identical to r02 (MobileNetV2 Keras weights, `chelsea` centre-crop 300² →
bicubic 224²; top-1 tiger_cat 0.4290; argmax unit (4,3); CAM identity mean + bias = logit exact).

**Rows (flat pitch = 0.58 × 0.45 × width / N × stride)**

| map | width mm | N | stride | rows | flat pitch mm | samples/row | relief mm | black runs | median run | ink ≥ 10 mm runs |
|---|---|---|---|---|---|---|---|---|---|---|
| input luminance | 146.0 | 224 | 6 | 38 | 1.02 | 112 (2-px means) | 2 | 155 | 22.2 mm | 96 % |
| ‖block_2‖ | 134.5 | 56 | 2 | 28 | 1.25 | 111 (bicubic) | 3 | 127 | 15.6 mm | 92 % |
| ‖block_5‖ | 123.0 | 28 | 1 | 28 | 1.15 | 82 | 9 | 123 | 11.8 mm | 84 % |
| ‖block_12‖ | 111.5 | 14 | 1 | 14 | 2.08 | 79 | 16 | 35 | 19.5 mm | 97 % |
| ReLU(CAM − mean) | 100.0 | 7 | 1 | 7 | 3.73 | 97 | 68 | 9 | 16.5 mm | 97 % |

Pitch is not monotone from 56² to 28² (1.25 → 1.15). At 134.5 mm width, 56 rows would fall to
0.62 mm, so block_2 is thinned to every second row, and 28 rows of block_2 then sit on a slightly
larger plane than 28 rows of block_5. The alternative (thinning block_5 to 14 rows) would make it
look like block_12. So the row count ties at 28 and the difference sits in roughness along the
row (56 against 28 units across).

**Crimson (ERF of unit (4,3), Σ_c |∂unit/∂A_c|, second-moment ellipse holding 50 % of mass)**

| map | centre (u, v) | radius (σ) | mass held | area of map |
|---|---|---|---|---|
| input | (0.531, 0.643) | 1.248 | 0.500 | 25.9 % |
| 56² | (0.519, 0.627) | 1.243 | 0.500 | 25.6 % |
| 28² | (0.512, 0.619) | 1.248 | 0.503 | 24.8 % |
| 14² | (0.506, 0.625) | 1.201 | 0.501 | 19.8 % |

Each loop is drawn at the local crest height (the max of the drawn field within about 1.5 drawn row
pitches, smoothed over 31/721 of the loop) plus 0.8 mm. It is tested against its own layer's
z-buffer, so it hides only behind genuinely taller nearer relief. Result: 4 loops, 4 runs, no
break. The ellipses are the same as r02's (checked by the science critic to within 3 mm).

**Summit**: cell (4,3) boundary maximum of the unit-hill field = 0.508 of the peak. Isolines at
0.528 + k × (3.6 mm / 68 mm) up to 0.985 give 9 closed levels, all inside the cell. The spire's
ink top is 279 mm.

**Gaps**: G solved = 10.92 mm. Measured on the drawn ink column envelopes: 10.9 / 10.9 / 10.8 / 10.9 mm.

**Crowding** (same pen, parallel |cos| > 0.93, closer than 0.7 mm, other run; measured on the
gcode): PIXELS band 0.5 %, block_2 0.0 %, block_5 2.6 %, block_12 2.4 %, crimson 0.0 %.
Caption band 10.9 % and title 32 % come from the stroke font's own glyph geometry (1.5 mm caption
type; the title's double pass on retraced strokes).

## Plot budget

- Draw 13.28 m · travel 3.51 m (0.26 × draw) · **9,826 commands** · 675 pen lifts · 2 pens (one swap).
- The preview estimates 7.6 min at F2200. At Leo's F600 with 1 s dwells: about 22 min of draw,
  plus about 22 min of lift dwells and 2 min of slow travel, so **roughly 45–50 min**.

## Self-critique (rubric)

| dimension | score | why |
|---|---|---|
| Hierarchy | 6 | The crimson spire and the four loops lead, and the title block is second. The spire is narrower than r02's cap (the cell is 14 mm), and the four large crimson loops compete with it. At 3 m the heaviest mass is the bottom raster, not the summit. |
| Grid & alignment | 8 | One type axis at x 15 = PIXELS corner. Right-flush planes at x 195. Constant width step. Ink exactly 5 mm inside on every side, and the title 6 mm under the top. |
| Tension & asymmetry | 7 | The left-edge staircase and the loops walking right give a diagonal. It is weaker than r02's frame crops, which are now forbidden. |
| Negative space | 7 | Four equal 10.9 mm gaps, and an empty wedge under the title. The top plane floats in a lot of air because rows 0–2 are hidden or zero. |
| Craft for pen | 7 | Travel down 72 %, commands down 63 %, no stubs under 3 mm, loops unbroken. Block_5 is still the most broken layer (median run 11.8 mm). Title and caption type carry font-level crowding. |
| Concept legibility | 6 | One mark, one parameter, one pass, no apparatus, and the caption decodes it. The silhouette is still "stacked feature maps", and the top plane reads partly as a bell chart. |
| Depth | 7 | True hidden-line on every layer, including the top (A4). Loops hide behind real relief. No atmospheric falloff. |

**Single worst thing:** the top plane. Only 7 rows exist (as the rule requires) and rows 0–2 are
zero after the clip, hidden behind the row-4/5 hills. So the head reads as a few isolated bell
curves plus two flat ruler-like front rows under a narrow crimson spire. It is less of a
"landscape summit" than r02's peak, and the flat zero rows could be read as a baseline rule.

## Engine requests

1. `Scene3D.field(SX, SY, DEP)`: rasterise a z-buffer without drawing a mesh. Rows-only
   surfaces still need the private `scene._rasterize` (repeated from r02).
2. `scripts/render_candidate.py --paper-color cream` (and the same flag on `promptplot preview`):
   `VisualizationConfig.paper_color` exists but neither CLI exposes it (A12).
3. A `giant_type` option that de-duplicates retraced glyph strokes before offsetting passes, so
   inline/bold display type does not double-ink where the font retraces.
