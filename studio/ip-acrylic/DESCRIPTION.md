# ATTENTION AS RESONANCE (Van Gogh acrylic oracle import) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/ip_acrylic` |
| current render | `gallery/studio/ip_acrylic/current/ip_acrylic_oracle.png` (paired gcode `ip_acrylic_oracle.gcode`: 110.2 m draw, 113.9 m travel, 702,569 commands, 11,163 pen cycles, 32 colour layers, bbox x 8.1–288.6 × y 34.8–385.4 mm) |
| source | **Nothing in PromptPlot generates it.** The plate is the oracle SVG `gallery/references/oracles/attention_acrylic_source/output/attention_acrylic_brushpaths.svg` (11,163 centerline paths, 32 layers, mm viewBox; `_centerlines.svg` has identical geometry) run through the SVG importer. The oracle package ships `render_attention_acrylic.py` + `scene_attention_acrylic.json` + `paint_plan.json` + `paint_order.csv`, but its README says the original generator was never saved: the package replays the final strokes, it does not re-derive them. The native rebuild is briefed, **not built**: `studio/reconstructions/acrylic-repro.md`, reference `studio/reconstructions/acrylic-repro/ref/reference.png`. |
| paper · pens | A3 portrait (297 × 420), white. The oracle paint plan: 10 paints (01 ink navy #172c38 · 02 ultramarine · 03 cobalt · 04 teal · 05 forest · 06 vermilion · 07 orange · 08 ochre · 09 yellow · 10 ivory #fff0b3) × 3 brushes (4 mm underpainting · 1.8 mm body · 0.9 mm accents) = 30 passes, plus 2 "optional lettering" passes at 0.45 mm. That makes 32 layers. **The preview shows none of this.** Every pass is a thin line in the matplotlib 10-colour cycle, so navy shows black, ultramarine red, cobalt blue, teal green, forest purple, vermilion orange, and so on. |
| status | unreviewed (no feedback) · 1 render + 1 gcode on disk |

## In one line
The transformer block as a **Van Gogh starry night of flow-to-attractor brush fields**: Q and K are two spiral suns, their arcs meet over a score slab and pour through an `A = softmax(...)` burst into the `Z = AV` river, W₁ / σ(·) / W₂ are a budding tree, a whirlpool and a fork, and `H = Z' + X` is the road looping home. Every mark is one brush centerline laid in three stages.

## What is on the sheet
Observed on the preview. The legend covers the whole upper-right third (u 0.61–0.98, v 0.03–0.52), so the K sun, the right-hand cypresses and the upper-right sky are not visible in this render.

- **Overall.** A rectangular full-bleed "canvas" at u 0.03–0.97, v 0.08–0.92, packed edge to edge with short curved coloured strokes (flow strokes riding an orientation field). There is no bare paper inside it. It is cut straight on all four sides.
- **Q sun (upper-left, u 0.05–0.35, v 0.08–0.25).** A large spiral of orange (vermilion 1.8 / 4 mm) and cyan strokes wound around a small eye, with the red lettering `Q` at its centre (u 0.24, v 0.17).
- **Title.** `ATTENTION AS RESONANCE` in black 0.45 mm lettering across u 0.36–0.62+, v 0.11–0.13, partly under the legend.
- **Score formula.** `Q·Kᵀ / √d_K` in red lettering at u 0.46–0.55, v 0.19–0.24, sitting in an ivory/yellow halo of concentric strokes.
- **Small whirls.** A green one at u 0.40, v 0.18 and another at u 0.60, v 0.18.
- **The score slab.** A parallelogram band of horizontal eddies (u 0.13–0.68, v 0.24–0.33) with small closed ovals. It reads only as a hard horizontal crease at v ≈ 0.33 (its bottom edge, u 0.13–0.68) and a straight diagonal left edge from (u 0.13, v 0.33) up to (u 0.38, v 0.24). The board of the oracle preview is not recognisable here.
- **Left cypresses.** Tall flame-shaped clusters of dark navy strokes rising from u 0.05–0.25, v 0.12–0.50, the darkest mass on the sheet. A second group sits at u 0.27–0.35, v 0.37–0.45 below the slab corner.
- **Softmax burst (centre).** `A = SOFTMAX(Q·K / √d_K)` in red lettering at u 0.41–0.62, v 0.38–0.40, on a fan of ochre/yellow strokes radiating up and out from a trunk.
- **V.** Red `V` at u 0.12, v 0.44 inside a broad teal/cyan river sweeping in from the left edge (v 0.40–0.50) toward the centre.
- **Z = AV.** Red lettering at u 0.46–0.54, v 0.51, on the yellow trunk where the V river and the burst merge.
- **Lower band (FFN, v 0.55–0.72):**
  - `W₁` at u 0.28, v 0.63 among a cluster of small yellow ring-buds (u 0.18–0.40, v 0.56–0.70).
  - `σ ()` at u 0.48, v 0.63, between two stacked spiral whirlpools (u 0.50, v 0.61 and v 0.70).
  - `W₂` at u 0.66, v 0.63.
  - `Z' = FFN(Z)` at u 0.77–0.87, v 0.64 on an ivory halo.
  - Tall dark navy cypress flames stand between them (u 0.55–0.65, v 0.55–0.73) and on the right (u 0.73–0.83, v 0.57–0.64).
- **The road / residual.** A wide S-shaped band of long parallel cyan and pink strokes enters left at v ≈ 0.55, sweeps right under the FFN, loops at the right edge (u 0.95, v 0.65) and returns along the bottom (v 0.78–0.84). `H = Z' + X` sits in it at u 0.46–0.57, v 0.82.
- **Bottom strip (v 0.84–0.92).** Hills of mixed purple/ochre strokes and dark bushes, cut flat at v 0.92.
- **Below the canvas (v 0.92–0.98)** and above it (v 0.02–0.08): blank paper.

## The science it encodes
Allegory, no computation. Colour is "time of night and heat of attention" (acrylic-repro brief). Q, K and V are three light sources, the score is where their arcs meet, softmax is a burst of light, `Z = AV` is the river it pours into, and the FFN is a tree (W₁ expansion), a whirlpool (σ nonlinearity) and a forking stream (W₂). The residual is the road home.

Oracle numbers (`paint_plan.json`):
- 11,045 paint strokes + 118 lettering strokes;
- 562 fully hidden strokes culled;
- 109.74 m painted, 97.71 m travel after in-pass ordering;
- stages ≈ 1,660 underpainting / 2,880 body / 6,500 accents.

Our import shows 110.2 m draw but **113.9 m travel**, so some of the oracle's ordering was lost on import.

**How faithful it is to the reference** (`studio/reconstructions/acrylic-repro/ref/reference.png`):
- Kept: the oracle keeps the Q/K suns, the cypresses, the burst, the river, the FFN trio and the looping road.
- Added: a perspective **score slab** that the reference does not have.
- Lost: the reference's stars and the village.

The oracle's own footprint preview (`gallery/references/oracles/attention_acrylic_art_preview.png`) reads convincingly as a painted Van Gogh pastiche. **This render does not.** At hairline width with category colours it reads as a coloured-line scribble, and the underpainting's 4 mm masses vanish.

## How it got here
One render, a straight import of the oracle's final SVG. There is no PromptPlot iteration and no upstream history (the generator was lost; the package only replays it). No Juan feedback recorded.

## Keep — what works
- **One centerline per mark, with a brush width.** Never two edges around a blob. This is the painterly MATERIAL GRAMMAR row, and the right model for the brush hardware.
- **Three stages with later-covers-earlier culling** (underpainting 4 mm → body 1.8 mm → accents 0.9 mm), and 562 hidden strokes discarded before plotting.
- **Flow structure.** Two spiral attractors up top, a burst in the centre, a river trunk, and a looping road. The whole sheet is organised by a few authored flow guides, which is a genuine flow-to-attractor order.
- **The equation chain on light.** Each formula sits on an ivory/yellow halo on the main flow, in reading order down the sheet: `Q·Kᵀ/√d` → `A = softmax` → `Z = AV` → `W₁ σ W₂ Z'` → `H = Z' + X`.
- **Dark cypresses as vertical counterweights** to the horizontal river and road.

## Weak — what doesn't
- [craft] The preview is not the drawing. With no brush footprints and fake colours, the plate cannot be judged: AUTHORING question 1 (forms recognisable) fails here only because of the preview. Re-render at footprint with the real hexes before any critique round.
- [craft] It cannot be plotted on this machine as delivered:
  - 32 layers = 30 paint/brush swaps plus lettering;
  - 11,163 pen cycles, 110 m of paint, 114 m of travel;
  - no dip/reload or drying encoded (the oracle's own note).

  The brush hardware path (`BrushConfig.charge_positions`, paint dips) exists but has never run a 30-pass job.
- [space] It is full-bleed to the four straight cuts, with no bare paper inside the canvas. That is the canon (Van Gogh is all-over), but on a pen plate it means no quiet zone. The only rest is the blank margins, which read as leftover rather than shaped.
- [concept] NO SCHEMATICS / illustration. It is a landscape (cypresses, hills, a road) with equations lettered onto it. The labels, not the forms, carry the mechanism. Remove the lettering and nothing says "attention".
- [grid] The score slab is a hard perspective parallelogram dropped into a painterly field. In this render it survives only as a straight crease at v 0.33 and a diagonal, a foreign ruled edge that reads as an import seam.
- [hierarchy] Lettering at 0.45 mm red is the only high-contrast element. The Q sun and softmax burst compete at similar scale and there is no 3 m read. In the oracle's footprint preview the burst dominates, so this may partly be the preview.
- [craft] Travel after import (113.9 m) exceeds the oracle's optimised 97.7 m. Pass ordering or path direction was not preserved.

## Next versions
1. **native paint** (faithful) — Build `acrylic-repro` as an authored `Scene` in `occlusion: paint`, stages `[underpainting, body, accents]`, widths `[4.0, 1.8, 0.9]`:
   - Author ~6 flow guides: the Q spiral, the K spiral, the burst, the river, the road, and the σ whirlpool.
   - `brush_family` around each guide for underpainting and body; `flow_strokes` on the reference's orientation field for accents.
   - Colour sampled and snapped with `quantize_palette` to the oracle's 10 hexes.

   Judge against the oracle's footprint preview and numbers (~11k strokes, ~110 m, stage ratio ≈ 15 / 26 / 59 %). It is the generator the oracle lost, rebuilt on our engine.
2. **four paints, two brushes** (craft) — Make it a real plot:
   - Collapse to 4 paints (navy, cobalt, yellow, vermilion) × 2 brushes (4 mm masses, 1.2 mm flow) = 8 passes via `--max-paints`.
   - Drop the score slab.
   - Cap strokes at ~3,500 with reload counts.
   - Leave one shaped ivory void (the softmax burst as bare paper, not yellow paint) as the quiet zone and the light source.

   Fewer, fatter marks read more like acrylic than 11k thin ones.
3. **suns that attend** (mechanism) — Keep the Van Gogh order and let flow carry data:
   - The Q and K spirals get one arm per head, with arm tightness = that head's attention entropy.
   - The softmax burst's rays = the actual top-k weights of one GPT-2 row (stroke count ∝ weight).
   - The river's width along its course = ‖Z‖ per token.

   Strip the landscape furniture (village, hills) that carries nothing.

**If only iterating:**
- Re-render the gcode with brush footprints (4 / 1.8 / 0.9 / 0.45 mm) and the paint plan's hex colours, with the legend outside the canvas. The K sun and top-right sky must be visible and the underpainting must read as solid masses.
- Re-import preserving the oracle's per-pass stroke order so travel is ≤ 98 m, and verify that the 562 culled strokes stay culled.
- Remove the score slab's straight edges (or paint them as a flow band), so no ruled crease crosses the field at v ≈ 0.33.
