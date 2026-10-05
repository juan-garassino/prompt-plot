# neural-networks-cnn r05 — wildcard · parent: r03 (read only for what NOT to repeat) · 2026-09-29

**THE REACH OF ONE UNIT.** A deliberately different approach from r00–r04, which were a
stratified stack of terrains or oblique lattice cards. The order here is **RADIAL, a dial**:
time runs around it and distance runs outward. The plate asks a question about a CNN that the
terrain stack could not: how far does one unit reach into the picture, and which layers give
it that reach?

- **Canon:** RADIAL DATA-VIZ / INFORMATION ARCS (STYLES §5), as assigned. It is flat by nature,
  and the flatness is declared.
- **Lineage:** Florence Nightingale, *Diagram of the Causes of Mortality in the Army in the
  East* (the polar-area "rose", 1858), read through the Bauhaus 1919–1933 radial timeline (the
  §5 reference). The order it lends is **one wedge per period, with the datum as length inside
  the wedge**. Here the period is a depth and the datum is a ring's share of the gradient.
- **Not repeated:** no stack, no terrain, no hidden-line rows, no frustum, no cards.
- **Sibling check:** `cnn-passes` (THE MIRROR FORGETS, PROMOTE) uses **rings = layers**. This
  plate uses **angle = layers** and **rings = distance in input pixels**, so the two do not
  share an order.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-cnn/rounds/r05/piece.py \
  --fn cnn_reach_dial --seed 7 --paper a4 \
  --palette cadetblue,darkgoldenrod,indianred,black \
  --out gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.png
```

- Final: `gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.png` + `gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.gcode`.
- a4 **portrait**, drawable 10–200 × 10–287. Seed 7.
- The piece uses no randomness. Seeds 2, 7 and 11 give byte-identical gcode (sha1 `615c9283c672` at v8).
- Self-rounds v1–v13 are kept in `~/Downloads`. v1–v4 are landscape: a centred half-disc, which
  the rubric scores as student work. v5 onward is portrait, with the diameter on the left edge.
- Files: `piece.py` (the plate); `compute_reach.py` (the torch pass, run once);
  `reach.npz` (the cached arrays the plate reads).

## Mandate responses

Every open row of LEDGER.md is listed. Most were written against the terrain stack. For each
one I say whether its principle carries over to the dial, or why it does not apply.

| id | mandate | status |
|---|---|---|
| A1 | No schematics: no frustum, rails, card edges or apparatus | **FIXED** in the letter: there are no layers drawn as objects and nothing joins them. **ARGUED** in the spirit: §5 is a chart idiom, so the plate is a polar chart. That is the canon the curator assigned. The wedges are not boxes and there are no arrows. The only connectors are the ochre and red lines stepping through the gutters. |
| A2 | One mark grammar, pitch ≥ 1.0 mm, no run < 3 mm, < 12,000 commands | **PARTLY**. The grammar is fixed: every data mark is a concentric arc centred on the unit. The finest ring pitch is 1.31 mm, and the minimum same-pen parallel gap measured on the gcode is 0.89 mm. **Not met:** 16,432 commands (1,595 lifts), mostly from the stroke-font type that §5 makes mandatory. Petal arcs are floored at 0.7 mm, not 3 mm, because a short arc IS the datum (a ring with a small share). |
| A3 | Crimson scarce; each crimson mark one closed, occluded curve | **ARGUED, n/a**: the plate is flat, so there is no relief to occlude against. The spirit carries: red is ONE continuous polyline (the exact RF edge), ochre is one polyline, and each colour has one legend swatch. They never cross the blue. Measured minimum distance, any angle, to blue: ochre 0.91 mm, red 1.39 mm. |
| A4 | Top terrain solidity | **n/a** (no terrain). |
| A5 | Equal inter-layer gaps | **n/a**. The analogue holds: within each wedge the rings are evenly pitched at exactly that layer's stride (§5: "concentric and evenly pitched"). |
| A6 | Title cap ≥ 6 mm under the top margin; every edge ≥ 5 mm inside; no crop | **FIXED**. Ink bbox is x 14.99–193.57, y 16.15–281.5. The title cap top is at 281.5, which is 5.5 mm under y = 287. That is 0.5 mm short of the 6 mm ask, and I state it rather than hide it. Nothing is cropped. |
| A7 | One flush-left type axis; caption ≤ 3 lines | **ARGUED**. There are two axes, x = 112 (title, subtitle, legend, caption) and x = 158 (three data notes), plus a 4-line caption. §5 says "annotation is the point" and makes scale labels and legend mandatory. The type is set in a column, never in boxes. |
| A8 | No flood; nothing closer than 0.8 mm | **FIXED**. The minimum same-pen parallel gap is 0.89 mm, and 0 samples fall under 0.8 mm (script below). |
| A9 | A real diagonal / no centred column | **FIXED**. The half-disc sits hard on the left margin with its hub at x = 23, and the type column runs down the right. The data is also asymmetric: dense combs at 12 o'clock and collapse at 6. |
| A10 | One computation | **FIXED**. It is the same forward pass as r02–r04, now tapped at all 20 depths (next section). |
| A11 | Title double-stroke | **FIXED**. The title is drawn single-pass, with no offset passes, so there are no doubled parallels. |
| A12 | Preview on cream | **ARGUED (tooling)**: `render_candidate.py` has no paper-colour flag (engine request repeated). |
| A13 | Face-on Molnár lattice | dropped on the ledger. |
| A14 | Preserve the r02 summit mountain | **n/a on a wildcard**. The reading destination is the hub, the unit itself, where the ochre and red lines end at 6 o'clock. |
| A15 | Monotone Schotter gradient / resolution channel | **FIXED in its radial form**. Ring pitch rises strictly with stride around the dial: 1.31 (224², 112², binned at 2 px) → 2.63 (56²) → 5.25 (28²) → 10.5 (14²) → 21.0 mm (7²). Rings per wedge fall 78 → 39 → 20 → ≤10 → ≤4. |
| S1 | No data clipped; one basis | **FIXED, with one declared rule**. There is one polar basis at 0.656 mm/px. The radial axis stops at 160 px because the farthest pixel of the picture is 159 px from the unit. Theoretical edges beyond 160 px (input to block 9: 245 → 160 px) are drawn **on the rim**. The legend and note 1 say so, and note 1 prints 245. |
| S2 | Caption decodes the mapping | **FIXED**. The legend states each colour's meaning. The caption gives angle = conv layers applied (clockwise 0 → 52), radius = Chebyshev px from the unit's centre, ring pitch = stride, longest ring of a sector = full. The rim carries every block id and the resolution of each stage (224² … 7²). |
| S3 | Disclose every transform | **FIXED**. Arc length = the ring's share of Σ\|∂unit/∂A\|, normalised to the sector's largest ring (caption line 3). Input rings are binned at 2 px (see Measurements). |
| S6 | No dossier/encoding | **DEFERRED** (process; the translator's job). |
| S7 | Preprocessing for p = 0.43 | **FIXED**: "MOBILENETV2 · CHELSEA, CENTRE-CROP · TIGER CAT 0.43" is on the sheet. |
| S8 | CAM plane hides half its data | **n/a**. The CAM is used only to pick the argmax unit (4,3) and to define ∂unit. No CAM field is drawn. |

## What changed from parent (composition, not params)

- **Order: laminar stack → radial dial.** r03 drew five maps as five slabs. Here one unit is the
  hub, and the network's 52 conv layers wrap around it clockwise from 12 o'clock (the input) to
  6 o'clock (Conv_1). Each of the 20 tapped depths owns a wedge whose angular width equals its
  number of layers (a block is 3 layers). The input wedge is given one block's width.
- **The data is a petal per wedge.** Each concentric arc is one Chebyshev ring of that layer's
  grid around the unit's centre. Its length is that ring's share of the gradient mass, so each
  wedge is the effective receptive field's radial profile. With an empty centre (few units
  near d = 0) and a bulge at about 58 px, the wedges read as leaves.
- **Two lines tell the result:**
  - **Red** is the exact theoretical edge. It rides the rim (the whole picture is in reach) and
    then steps in, block by block, 112 → 80 → 48 → 16 px.
  - **Ochre** is the half-mass radius. It barely moves (56 → 43 px) until the 7² blocks, then
    collapses onto the cell.
- **Composition:** A4 portrait, with the diameter on the left margin as the px scale. The type
  column on the right follows the dial's time: the title and the input note beside 12 o'clock,
  the 14² note at 3, the 7² note and the legend beside 6.

## Measurements / computations

**The pass.** `compute_reach.py` uses Keras MobileNetV2 (α 1.0, 224) with ImageNet weights,
re-implemented in torch functional form with Keras `correct_pad`, run in float64. The input is
`chelsea.png`, centre-cropped 300² and bicubic-resized to 224². It was run once under
`009-mini-networks/.venv` (torch 2.2.2).

- Top-1: tiger_cat, p = 0.42900.
- Argmax CAM unit: (4,3), value 18.2825.
- **Cross-check against r03's `maps.npz`:** `g_input`, `g_block_2`, `g_block_5`, `g_block_12`
  and `cam` are bit-identical (max abs diff 0.0). It is the same pass.
- The unit's RF centre in input pixels, (row 159, col 127), follows from Keras' asymmetric
  padding (offset 31, stride 32).
- **Every depth:** G_d = Σ_c |∂cam(4,3)/∂A_d| is **exactly 0 outside** the theoretical RF
  interval (interval propagation through every conv halo and stride). This is checked
  numerically in `compute_reach.py`, and all 20 depths print `zero-outside=True`.

**Per depth.** Chebyshev distance, ring bin = max(stride, 2) px. r50 is the continuous
half-mass radius, interpolated between rings.

| depth | grid | stride | rings drawn | half-mass r50 (px) | theoretical edge (px) |
|---|---|---|---|---|---|
| input | 224² | 1 (binned 2) | 78 | 56.1 | 245 (rim) |
| stem | 112² | 2 | 78 | 55.3 | 244 (rim) |
| block_0 | 112² | 2 | 78 | 55.7 | 242 (rim) |
| block_1, 2 | 56² | 4 | 39 | 54.3, 54.4 | 240, 236 (rim) |
| block_3, 4, 5 | 28² | 8 | 20 | 51.7, 51.2, 51.1 | 232, 224, 216 (rim) |
| block_6 … 9 | 14² | 16 | 10–9 | 46.7 → 44.8 | 208 → 160 (rim) |
| block_10, 11, 12 | 14² | 16 | 9–8 | 44.3, 43.6, 43.0 | 144, 128, 112 |
| block_13 | 7² | 32 | 4 | 33.6 | 96 |
| block_14 | 7² | 32 | 3 | 25.6 | 64 |
| block_15 | 7² | 32 | 2 | 14.2 | 32 |
| block_16, Conv_1 | 7² | 32 | 1 | 0 | 0 |

Readings:
- **"A quarter of the picture":** the half-mass Chebyshev square at the input is 2·56 + 1 =
  113 px on a side. It lies wholly inside the 224² image (rows 103–215, cols 71–183), and
  113² / 224² = **25.4 %**. This agrees with r03's independent 50 %-ellipse figure (25.9 %).
- **"The 7² blocks do the rest":** from the input to block 12 the edge shrinks 245 → 112 px
  (−54 %), but the half-mass radius only shrinks 56.1 → 43.0 px (−23 %). The last five 7²
  layers carry both the edge and the half-mass radius from there down to 0.

**Geometry.**
- Hub at (23, 148.5). R0 = 12 mm (d = 0), R1 = 117 mm (d = 160 px), k = 0.656 mm/px.
- Wedge angle = 180° × layers / 55.
- Gutter between wedges 1.1°. The ochre and red radial steps run in the gutter centres.
- The graduated dotted rings at 64 and 128 px are drawn only on blank paper.

**Clearance rules** (from `STATS`):
- 7 blue rings within 0.9 mm of their wedge's ochre radius give way to it. The ochre line
  takes the ring's place.
- 3 petal arcs are **shifted** inside their wedge, length kept, to stay 0.9 mm off a radial
  step.
- 11 arcs could not shift and were **cut** by at most 0.58 mm, at most 28 % of one short arc
  near the hub.
- 441 petal arcs are drawn in all.

**Crowding** (measured on the v14 gcode; 0.3 mm samples; parallel means |cos| > 0.93; the
script is in the session scratchpad, not the repo):

| pair | minimum parallel gap | samples under 0.8 mm |
|---|---|---|
| blue vs blue | 0.89 mm | 0 |
| blue vs ochre | 0.92 mm | 0 |
| blue vs red | 9.0 mm (1.39 mm at any angle) | 0 |
| ochre vs red | 1.20 mm | 0 |

## Plot budget

- Draw 5.52 m · travel 5.96 m · **16,432 commands** · 1,595 pen lifts · **4 pens, 4 clean layers,
  one swap each**.
- Longest travel is 251 mm, a layer start, where the pen parks anyway.
- The engine's `reorder_by_color` sets the final stroke order within each colour. Inside a layer,
  the long hops are to and from that pen's legend swatch.

Stated order is light to dark, so black lands last:

| # | pen | meaning | draw | lifts | time on Leo |
|---|---|---|---|---|---|
| 0 | cadetblue | ERF petals | 1.33 m | 442 | ≈ 18 min |
| 1 | darkgoldenrod | half-mass line | 0.17 m | 2 | < 1 min |
| 2 | indianred | theoretical edge | 0.41 m | 2 | ≈ 1 min |
| 3 | black | scale, rim, labels, type | 3.61 m | 1,149 | ≈ 46 min |

- Leo settings assumed: F600 draw, 1 s dwells per lift and drop, G1 F2000 travel.
- **Total ≈ 66 min.** The preview estimate at F2200 is 5 min.

## Self-critique (rubric, honest)

1. **Hierarchy 7.** At 3 m the half-disc of fine blue arcs dominates, the red edge line is the
   loud second, and the title is third. The blue body is light: a fine cadetblue line against a
   single red line, so red sometimes out-shouts the data.
2. **Grid 7.** There are two type axes (112 / 158), and the diameter is the px scale. The block
   ids ride a fixed radius. The title cap is 5.5 mm under the margin, not 6.
3. **Tension 7.** A half-disc hard on the left margin against a right-hand type column is a
   real asymmetry. It is still a disc.
4. **Space 8.** The empty band between the half-mass line and the red rim (12 o'clock to
   3 o'clock) is the plate's point: "in reach, but not looked at". The quiet lower-left
   quadrant is where the field has collapsed.
5. **Craft 7.** Nothing is under 0.8 mm, and there is no ink-on-ink between pens. The cost is
   1,149 black lifts, mostly stroke-font type.
6. **Concept 6.** "It could see the whole picture. It looks at a quarter of it." lands, and the
   numbers are real and checkable. But it is openly a polar CHART (the assigned canon), and the
   rubric's NO-SCHEMATICS clause is where a critic will push.
7. **Depth 5, declared flat.** §5 is a flat canon. Line density carries some depth (the fine
   combs at 12 o'clock recede and the coarse rings at 6 come forward), but the plate is flat by
   decision.

**The single worst thing:** the plate reads as a very good data graphic rather than an image.
The petals in the fine wedges (224²/112²/56²) look like radial combs rather than leaves,
because those wedges are only 3–10° wide. The rose idea is fully visible only in the 14²/7²
half.

## Engine requests

- `render_candidate.py --paper-color cream` (repeated from r02/r03).
- A `kit.dotted_arc(cx, cy, r, a0, a1, on, period)` helper. The kit's `dotted_circle` is
  full-circle only, so this round's `dotted()` is local.
- A way for a piece to pin its within-colour stroke order (or a `start=` hint). Today
  `merge_chunks → reorder_by_color` re-orders it, so a piece cannot keep a legend swatch at
  the end of its layer.
