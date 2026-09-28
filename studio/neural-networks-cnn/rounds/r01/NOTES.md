# neural-networks-cnn r01 — pooling-cascade (abstract) · parent: promptplot/generative/pieces/ml.py::bauhaus_locality · 2026-09-28

lineage: Vera Molnár, *(Dés)Ordres* (1974). The order taken from it is a strict lattice of concentric squares where each cell's ring count is its own value. Here the ring count is the activation, and the lattice pitch doubles from card to card.

## Render
```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-cnn/rounds/r01/piece.py \
  --fn pooling_cascade --seed 7 --paper a4 --palette black,crimson,black \
  --out ~/Downloads/pp_neural_networks_cnn_pooling-cascade_v11.png
```
- final: `~/Downloads/pp_neural_networks_cnn_pooling-cascade_v11.png` + `.gcode`, seed 7
- seed variants: v12 (seed 3) and v13 (seed 11). The seed only moves the probabilistic pixel ticks and the one-ring 2-px cells, and all three read the same.
- iteration trail: v1–v10 (same prefix), all kept

Files: `piece.py` (composition), `net.py` (the real CNN and the receptive-field bookkeeping), `input_48x64.npy` (the cached input array; `net.build_input()` rebuilds it from the parent gcode).

## Mandate responses
No `LEDGER.md` or `FEEDBACK.md` exists for this slug, so there are no open J*/A*/S* rows. The table below answers the "Weak" list in DESCRIPTION.md as the working mandates.

| id | mandate (DESCRIPTION § Weak) | status |
|---|---|---|
| W1 | straight black chords across the crimson cap | FIXED: there are no contours. The crimson top cell is its own concentric-ring cell, and no black stroke enters it. |
| W2 | crimson not occluded, and the top window is 4 straight corners | FIXED: every crimson stroke goes through the same exact `geometry.clip` occlusion as the black. Footprints hide under the cards above them. Rails are hidden beneath each card and reappear below its front edge. Footprints are exact lattice rectangles on flat cards, so nothing needs to drape. |
| W3 | PIXELS floods; EDGES crumbs | FIXED: pixel ticks are 2.3 mm apart along u and 1.06 mm along v. Rings are held 0.9 mm apart at a fixed pitch and activation sets the ring COUNT (duty), never the spacing. Cell gutters are ≥ 0.95 mm, and there is a 0.95 mm keep-out on both sides of every crimson line. A ring that the keep-out would cut is left out whole, never broken. |
| W4 | travel ≈ draw, floating debris | PARTLY FIXED: there is no debris. Travel is 6.7 m against 9.3 m of draw (ratio 1.38, was 1.01). Most of the air is the ~1,000 isolated pixel ticks. |
| W5 | textbook diagram / NO SCHEMATICS | ARGUED: no layer is named, there is no axis, no arrow and no "PIXELS…OBJECTS" labels. The only per-card text is its cell pitch (1 2 4 8 16), and it grows with the pitch. But a stack of feature maps with a receptive-field funnel is still the genre of the AlexNet/Zeiler–Fergus figure. See the self-critique. |
| W6 | centred column, no diagonal, nothing crops | PARTLY FIXED: the cards drift 8 mm right per level while the crimson funnel runs down-left, so there are two opposed diagonals. Type masses sit on the counter-diagonal (CNN top-right, 16 bottom-left). Nothing crops at the frame. |
| W7 | metronomic gaps, leftover bottom band | FIXED: the gap between cards is 30 mm + k·(receptive-field growth across that stage), giving 32.2 / 37.4 / 38.4 / 48.9 mm, so the rhythm is data. The bottom band holds the colophon on the numeral axis. |
| W8 | five equal smudges | PARTLY FIXED: the marks change species with depth (pixel ticks → one-ring cells → Molnár targets of up to 7 rings), and the one crimson 7-ring target is the loudest mark. The cards themselves are equal in size by necessity, because every map covers the same image extent. |
| W9 | ragged labels, no shared edge, lost colon | FIXED: the numerals and colophon are flush-left on one axis (x0 + 6). The title is flush-left on one axis 5 mm right of card 0's back corner. No `M 1:80` footer. |
| W10 | depth inverted | ARGUED: occlusion carries the depth. Cards are opaque, each has a 1.6 mm front and right face, and the nearer card hides the one below. The nearest card (the input) is the lightest because the input is sparse ink. |

## What changed from parent
- **New order (nested / tessellated) replaces the laminar noise terrains.** The plate has five flat, opaque square-lattice cards in one shared axonometric basis. The input is at the top, nearest the eye, and each pooled map falls beneath it. Every card covers the same image extent, so the cell pitch doubles card to card (1, 2, 4, 8, 16 input px). The halving lattice IS the depth.
- **The data is real.** A fixed CNN runs on one real image, and the hand-seeded fbm is gone. The image is the ink of the parent plate itself (`pp_cnn_dashes.gcode`, rasterised). The new plate is literally the old one pooled into one unit.
- **Crimson carries only the receptive field:** the argmax top unit, its exact dependency footprint on every map below it, and dotted projection rails joining the corners. Where a footprint side lies on the image boundary it is drawn ON the card edge and replaces the black edge.
- **Type is data or colophon:** per-card pitch numerals growing with pitch, "CNN" at the size of the largest numeral, and a five-line colophon. The axis and all layer names are gone.
- The composition flipped to a cascade that falls down the sheet (pixels at the top, the one cell at the bottom), opposite to the parent's rising valley.

## Measurements / computations
Input: the parent gcode's G1 strokes, rasterised at 8 px/mm with a 0.35 mm stroke, over the window x 20–190, y 40–267 mm (aspect 0.749). Area-averaged to 48 × 64 and normalised by its 99th percentile (0.734). 43 % of pixels are non-zero and the mean darkness is 0.179.

Network (`net.py`; all convs are zero-'same' padded, all pools are 2×2 stride 2):

| map | op | shape | min / max / mean |
|---|---|---|---|
| P0 | input | 48×64 | 0 / 1 / 0.179 |
| P1 | \|Sobel\| → pool | 24×32 | 0 / 4.26 / 1.08 |
| P2 | Gabor 5×5 ×4 orientations (σ 1.3, λ 3.6, zero-mean), ReLU, winning orientation → pool | 12×16 | 0 / 8.74 / 2.59 |
| P3 | binomial 3×3 → pool | 6×8 | 0.99 / 5.49 / 2.95 |
| P4 | centre-surround 3×3, ReLU → pool | 3×4 | 0.05 / 3.88 / 1.31 |

- C2 winning-orientation counts (0°, 45°, 90°, 135°): 293 / 123 / 232 / 120.
- The winner is the P4 argmax unit (u 0, v 3), the front-left cell, with value 3.877. The runner-up is 2.147.
- Receptive field by recurrence r += (k−1)·j: 1 → 4 → 14 → 26 → 50 px. The frame gap uses the growth per stage, 3 / 10 / 12 / 24.
- Exact footprints (index boxes, clipped at the grid):

  | map | u range | v range | size | size in input px |
  |---|---|---|---|---|
  | P3 | 0–2 | 5–7 | 3×3 | 24×24 |
  | P2 | 0–6 | 9–15 | 7×7 | 28 |
  | P1 | 0–15 | 16–31 | 16×16 | 32 |
  | P0 | 0–32 | 31–63 | 33×33 | 33 |

  The field would be 50 px unclipped, but it is cut by the image corner.
- **Verification:** 8 trials randomising every input pixel OUTSIDE the P0 footprint left the top unit unchanged, with max |Δ| = 0.0. Randomising pixels inside it moved the unit by up to 2.03. The footprint is exact.
- "Where the old plate flooded": the winner's own 16×16 input region holds 5.9 % fully-inked pixels, against 1.1 % image-wide (5.4×). That region is the parent's solid-black PIXELS slab.
- Geometry in one shared basis: screen = origin + u·(2.3, 0) + w·(0.36, 1.0) mm, where w = 64 − v.
  - Card drift is +8 mm per level. Parallel side edges of successive cards sit 20–26 mm apart; at the v3 drift of −11 they were 1.1 mm apart.
  - Card pad is 0.6 mm and card thickness is 1.6 mm.
  - Ring pitch is 0.9 mm perpendicular in screen, which is 0.41 u-units and 0.9 v-units.
  - Ring capacity per cell: 1 at 2 px, 1–2 at 4 px, 3 at 8 px, 7 at 16 px.
  - Tone is (a / p99.5)^γ with γ = 0.55 for pixels and 0.8 for the rest.

## Plot budget
- Draw 9.29 m, travel 6.73 m (ratio 1.38), 11,157 commands, 1,621 pen lifts.
- 3 pens: 0 black lattices and cards, 1 crimson receptive field, 2 black type.
- Bounds are clean inside the 10–200 × 10–287 drawable area. The ink sits at x 16–199, y 18–280.
- Estimated time is 437 s at F2200. On Leo at F600 draw with G4 P1.0 dwells: ~16 min ink + ~3 min travel + ~54 min of lift/drop dwells ≈ **75 min**. The dwell count is driven by the pixel ticks.
- Scorer: grade A, dominant issue "efficiency".

## Self-critique (rubric, honest)
1. **Hierarchy 6.** The crimson 7-ring target at the funnel's foot is the unambiguous focal mark, and the growing numerals give a second read. The five cards are still similar masses at 3 m, and the input card is a pale dash field, not a mass.
2. **Grid & alignment 7.** There is one numeral/colophon axis and one title axis, and each numeral sits on its card's front edge. The title axis is 5 mm off card 0's corner, not on it.
3. **Tension 6.** The right-drifting cards and the left-leaning crimson funnel are two real diagonals. Nothing crops at the frame, and the stack is still a column.
4. **Negative space 7.** The left numeral gutter, the top-right title wedge and the bottom-right corner are all shaped by the drift. The big blank P4 card is honest data (a sparse centre-surround map).
5. **Craft 7.** No floods, every spacing is ≥ 0.9 mm, and no pen shares a stroke with another. Crimson replaces the black card edge where they would coincide. Travel is high because the ticks are isolated.
6. **Concept 5.** The mapping is exact and stated ("cell pitch is stride, crimson footprint is exact receptive field"), and the self-referential input is a real joke. But the silhouette is still the feature-map-stack figure every CNN paper draws. The abstract order is present, and the genre is not escaped.
7. **Depth 7.** Opaque cards with thickness, exact hidden-line occlusion of black and crimson alike, and rails that pass behind cards.

**The single worst thing:** at arm's length it still reads as "the CNN diagram", a pyramid of feature maps with a receptive-field cone, only more exact. The second is that the input card (dashes of the old plate) is too thin to carry the "pixels" end of the story.

## Engine requests
- `kit.tone_dots` draws in screen space and cannot sit on a projected lattice. A `tone_dots_on_basis(basis, grid, tone)` variant (one mark per lattice cell, projected) would have let the pixel card use the kit directly. For now it is hand-placed with the same duty rule: one tick per cell, inked with probability = tone.
- A "rail halo" primitive: a Region built from a dotted polyline with a clearance, so front-of-card rails can clear black marks without a hand-built quad union. Here it is done locally with `geometry.Polygon` quads plus `Union`.
