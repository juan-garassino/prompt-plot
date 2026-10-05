# Art critique — neural-networks-cnn r01 · canon: none declared (lineage: early computer art, Molnár *(Dés)Ordres*) · 2026-09-28
render: gallery/neural-networks/cnn/trials/pp_neural_networks_cnn_pooling-cascade_v11.png

No `encoding.md` or `BRIEF.md` in the slug. Judged against the HANDOFF thesis and lineage, `studio/nets/cnn.md` and DESIGN_RUBRIC. HANDOFF names no STYLES.md canon, so the plate is judged as a Molnár answer.

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 5 | At 3 m the dominant mass is "a stack of five slabs", and the busiest element is the dashed input card at the top. The crimson strongest unit (~40 × 17 mm, bottom-left) is the intended destination, but it is no bigger than the black ring cells beside it, so it reads as a third element at best. |
| 2 grid & alignment | 6 | The numerals 1/2/4/8/16 sit on each card's front-bottom edge and share a left axis with the footer (good). Title `CNN` floats at x≈165 on no card axis. The `FROM PIXELS` tracking runs to x≈200 and touches the drawable margin. Cells clipped by the card in front leave sliver rectangles poking out of the right card edges (card 2/4 junction, x≈140–150, y≈150–235). |
| 3 tension & asymmetry | 6 | The stair-step to the lower right gives a real diagonal, and the stride-scaled numerals ramp 1 → 16 in size, which is a nice move. The stack is still a centre column with no crop at the frame, and card gaps grow 33 → 58 mm with no visible reason. |
| 4 negative space | 5 | Most of card 16 is empty, but the emptiness reads as leftover because six ring cells are scattered with no rhythm. The right-hand dotted crimson rail runs on top of the hero cell's right edge (x≈98, y≈40–55): a collision, not an overlap anyone chose. The inner and outer rail pairs run 1–3 mm apart beside cards 2 and 4. The title is pressed against the frame. |
| 5 craft for pen | 6 | 3 pens, 9.3 m draw / 6.7 m travel, and no floods. Problems: (a) every card thickness is two lines ≈0.5 mm apart, under the 0.8 mm floor, so they will merge. (b) A black card-edge stub shows through at the hero cell's lower-left corner. (c) Clipped cell slivers at the occluded edges. (d) Pens 0 and 2 are both black, so one swap buys nothing. (e) The render is on white, but HANDOFF says cream. |
| 6 concept legibility | 3 | NO SCHEMATICS: oblique feature-map cards stacked in perspective, a dotted receptive-field frustum, stride numerals and a 5-line hyperparameter deck (`SOBEL 3 GABOR 5 … MAX-POOL 2X2 STRIDE 2`) make up the LeNet/AlexNet textbook figure. The Molnár rule (ring count = value) holds only on levels 8 and 16. Levels 1/2/4 are dashes and single rectangles, so the abstract order is a surface texture laid on a diagram, not the plate's form. The "input = the old plate's ink / strongest unit where it flooded" joke is the right kind of twist, but only the caption carries it. |
| 7 depth & dimensionality | 6 | Opaque cards occlude one another, which gives real stacking. But every card has the same weight, there is no falloff, and within a card everything is flat. |

avg **5.29** · min **3** · **VERDICT: FAIL**

## Reads at a glance
At 3 m a stranger sees "a CNN diagram from a paper": five tilted sheets stepping down to the right, with a red cone through them.

## Acceptance checks
(No encoding §11. These checks come from the HANDOFF thesis and lineage.)
- Cell pitch doubles per level (stride visible as pitch): **PASS**. Pitch runs from ≈2.3 mm through ≈5, 9 and 18 mm to ≈37 mm.
- Crimson footprint is the receptive field of the top unit, nested on every map: **PASS**. The footprints nest on every card and are clipped at the card 1 edge, consistent with the caption's "33 × 33 (50 unclipped)".
- Molnár rule "each cell's ring count its own value", applied uniformly: **FAIL**. Levels 1, 2 and 4 use dashes or single rectangles. Only 8 and 16 carry ring nests.
- Holds its own hung beside *(Dés)Ordres*: **FAIL**. Molnár is a flat, strict, face-on lattice with measured local breaks. This borrows her concentric square as texture inside a perspective diagram.
- No schematic (nets/cnn.md and DESCRIPTION's pooling-cascade spec: "nothing is labelled a layer; the halving lattice IS the depth"): **FAIL**. The layers are numbered, projected as cards, joined by a frustum and captioned with a hyperparameter deck.
- Plottable (≥0.8 mm, ≤4 pens, bounds clean): **PARTIAL**. Card-edge double lines are ≈0.5 mm apart, and the title touches the margin.

## Biggest weakness
The plate is still the textbook figure. Oblique cards plus a dotted frustum plus a stride caption is the exact apparatus that NO SCHEMATICS bans. The one abstract idea, a Molnár lattice whose cell nests carry values and whose pitch is the stride, is present but subordinate. It is painted onto the cards instead of being the whole sheet.

## Mandates
1. **Delete the projection and the frustum. Build the whole sheet as one face-on Molnár lattice.** Use five horizontal bands down the sheet, square cells, with pitch doubling band by band (≈2.3 → 37 mm), all sharing one left edge. No parallelogram cards, no card-thickness lines, no dotted crimson rails. Test: every line on the sheet is horizontal or vertical, and nothing on it is drawn in perspective.
2. **One cell rule on every band: a concentric-square nest whose ring count is that unit's value** (0 rings = bare paper), with rings ≥1.0 mm apart. The finest band may cap at 1 ring, but it must use the same glyph: no dashes, no plain rectangles. Crimson appears only on the strongest unit's nest and its footprint cells on each band. That nest must be the largest single mass on the sheet: ≥3× the area of any black nest and ≥55 mm on a side. Test: zoom any band and find only concentric squares; at 3 m the crimson nest is what you see first.
3. **Cut the type to one voice and one axis.** Keep `CNN` + one line, drop the 5-line hyperparameter deck to at most 2 lines (keep the "where the old plate flooded" line; it is the joke), and set title, numerals and caption flush-left on the lattice's left edge. The `FROM PIXELS TO MEANING` right end must sit ≥5 mm inside the margin (currently touching at x≈200). Test: all type left edges share one x, and no glyph is within 5 mm of the green frame.

## Follow-up on open mandates
No `LEDGER.md` or `FEEDBACK.md` exists for this slug, so there are no open A*/J* mandates. Checked against DESCRIPTION § "If only iterating" and § Next versions 1 (pooling-cascade), which this round claims to execute:
| id | status | evidence |
|---|---|---|
| iter-1 contour chords / crimson occlusion | FIXED | No contour chords. Crimson footprints are occluded by nearer cards, and the rails break at card edges. |
| iter-2 no rows < 0.8 mm, no debris | PARTIAL | No flood and no floating quads, but card-edge double lines are ≈0.5 mm apart and clipped cell slivers remain at occluded edges. |
| iter-3 remove labelled axis, diagonal that crops the frame | PARTIAL | The two-headed axis and word labels are gone, but numerals now label the layers. The diagonal exists but nothing crops at the frame. |
| NV-1 "nothing is labelled a layer; the halving lattice IS the depth" | NOT FIXED | The layers are numbered and still projected as stacked cards with a frustum. |
| NV-1 cells inked by tone from a real feature map | PARTIAL | Real maps are claimed (Sobel/Gabor/pool), but the glyph changes per level (dash, rectangle, nest) instead of using one tone rule. |

## Regressions vs compare-to (pp_cnn_dashes)
- **Reading direction inverted.** DESCRIPTION Keep says "single crimson summit at the top, the reading destination" and "rails fanning upward". Both are no longer true: the crimson destination is now bottom-left, jammed beside the caption deck, and the frustum narrows downward. The sheet now reads pixels-at-top, and the eye ends on the footer text instead of the accent.
- **Bottom band became a measured caption deck.** The parent's leftover bottom band is now filled with five lines of hyperparameters, which is the rubric's "scientific figure" failure mode, and in a heavier third type voice.
- **Paper tone lost.** The parent previews on cream; r01 previews on white, even though HANDOFF says cream.
- **Top-heavy mass.** The parent's weight sat in the terrains. Now the densest, busiest zone is the input card at the top-left, pulling the eye away from the crimson unit.
- Keep items still true: the fine-to-coarse gradient still reads (now as pitch, which is good); the rightward stagger is kept (≈8 mm per step); occlusion between layers is kept (cards are opaque).
- Improvements to bank: no flood, travel down from 17.7 m to 6.7 m, crimson occluded correctly, axis arrow gone.
