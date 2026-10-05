# convolutions r06 — wildcard (Memphis Group canon) · parent: r04 (lineage only, nothing reused) · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r06/piece.py \
  --fn convolutions_memphis --seed 7 --paper a4 --orientation landscape \
  --palette darkorange,crimson,dodgerblue,black \
  --out gallery/studio/convolutions/trials/pp_convolutions_wildcard_v22.png
```
- final PNG: `gallery/studio/convolutions/trials/pp_convolutions_wildcard_v22.png`
- final GCODE: `gallery/studio/convolutions/trials/pp_convolutions_wildcard_v22.gcode`
- seed 7. `v23` is a re-render of the same code to check determinism: its gcode is byte-identical to v22 apart from the timestamp line.
- Other seeds tried: `v20_s3` and `v20_s11`. The seed picks X, so it changes the whole plate. Seed 7 wins because it gives the cleanest lone Gabor stamps in the triangle (three bars each), a legible fuse gradient in the square, and a solid-red crowd at the focus. s11 has a small orange solid, but its triangle stamps are fragmentary. s3 has the weakest triangle.
- This round was relaunched. An earlier, interrupted pass of this same thesis left `piece.py` and renders v1–v10 in this round directory. v11–v22 continue that work, and nothing from r01–r05 was used.

## Mandate responses
The wildcard retires r04's lattice, head, key and title, so most open mandates attach to objects that no longer exist. Each one is still answered below.

| id | mandate | response |
|---|---|---|
| A12 | Title: multi-pass strokes separate, `I` spacing, N diagonals | FIXED in kind. The title is built per SEGMENT (`_fat_glyph`): every straight segment is its own serpentine band of the same width, so the N and V diagonals are as fat as the stems. Glyphs are set on their ink boxes, which evens the spacing |
| A16 | Kill the heart and the leftover quadrant; crop at the frame; no empty region > 80×80 mm; key and title on one left axis | ARGUED / partly FIXED. There is no contour mass left to read as a heart. Nothing on the sheet is figurative: a disc, a square and a triangle are Memphis primitives, and the confetti is X. The disc bleeds off the left and bottom frame and the laminate grid bleeds off the right and bottom, so cropping at the frame is done with intent. The one open zone (x 100–175, y 140–200 mm, about 75×60) is the quiet zone, and it holds sparse impulses. NOT done: key and title on one left axis. The key sits on the laminate grid (grid column 2), because a Memphis key belongs to the ground, not to the title |
| A17 | The head is a lifted card: shadow ≥ 3 mm on right and bottom, 45° hatch at ≈ 0.9, fattest keyline | FIXED as a system. All three cards are lifted: a 3.4 mm cast shadow on the right and bottom, 45° hatch at 0.9 mm pitch, and a 4-pass 1.05 mm keyline, which is the heaviest line on the sheet after the title. The maps and grid behind a card stop at its shadow's outer edge, not at a hairline offset |
| A18 | Head collars ∝ \|w\| | ARGUED (N/A). There is no head and no collar. Kernel identity is carried by the true impulse response: each lone confetti prints K itself, at 1:1 |
| A19 | Layer order light → dark; legend swatches last; max consecutive travel < 120 mm | PARTLY FIXED. The stream order is orange → crimson → blue → black (light → dark, black last, which also lands the confetti on top). Max consecutive travel is 24.9, 85.4, 69.0 and 123.2 mm per pen; only black misses the bar, by 3 mm, on one jump between two sparse chips (127.9,167.1) → (235.9,107.9). The piece chains strokes itself and puts key strokes last (`_sequence`, greedy + 2-opt), but `render_candidate` → `merge_chunks` → `reorder_by_color` re-chains every layer from (0,0) with plain nearest-neighbour, so the key lands mid-layer (black strokes 389–820 of 997). See Engine requests. The colour swatch was removed from the key, and all key icons are black |
| A20 | Honest lineage | FIXED. Lineage: Sottsass, *Bacterio* laminate (1978): one motif stamped at scattered points. That order IS `Y = K ∗ X` with X a sum of impulses, and the plate uses it literally, since every coloured mark is a stamp or a sum of stamps |
| S5 | No dossier/encoding for this slug | DEFERRED (process; not the designer's job). The binding encoding is in the piece header and the key: X = impulses, line Y = 0.35, solid Y > 1.25, grid = λ |
| S8 | The key tells the truth and says what was found | FIXED for this encoding. The key has 5 rows, each checkable: "one impulse of X (x = 1)"; "line K ∗ X = 0.35"; "solid K ∗ X > 1.25 : only a sum"; "(one impulse alone peaks at 1)"; "grid 12 mm = λ of K1, K2". The finding sits in the subtitle ("every squiggle is a sum") and is proved by the solid. There is no zero code, because no level is drawn at zero |
| S9 | Head hides outputs that prove window overlap | ARGUED (N/A). No inputs are hidden (every line stops 1 mm off every triangle, and triangles draw last). Card overlaps hide parts of maps, which is declared depth. Each card is a window, so the hidden part of a map is still computed; it is just not shown |

## What changed from parent
Nothing was carried over. r01–r05 are all one field or pipeline, read in (i, j) or along a flow. r06 answers with a different ORDER:
- **Superposition, stamped.** X is a confetti scatter. The feature maps are printed on three Memphis cards (disc, square, triangle), stacked with cast shadows over a gridded laminate slab. A card is a window onto `K ∗ X` at its true position.
- **Crowd → solitude.** X's hard-core radius grows with distance from ONE crowd focus at the disc/square overlap, so each card runs from fused squiggles to lone stamps. Lone stamps are the kernel itself: three bars for a Gabor, a ring for the blur. Crowds sum.
- **The proof is loud.** Where stamps add past what any single impulse can reach (Y > 1.25, while a lone peak is 1), the squiggle goes SOLID along its own bars. This is the plate's accent mass: bold red bars at the crowd focus.
- Grid pitch = λ, so the ground is a ruler for the Gabor bars. The key is a block of whole grid cells knocked out of the laminate.
- Moves in this relaunch pass (v11 → v22):
  1. Density moved from a linear ramp (the whole disc was a crowd) to a radial focus.
  2. Added the sum-only solid, then inset it to the pen floor.
  3. Confetti kept off keylines, so no chopped keylines.
  4. Triangle pulled off the right frame and aligned to the title's top line.
  5. Strict grid with the key knocked out on grid lines.
  6. Captions carry σ.
  7. Key rewritten and all its icons made black.

## Measurements / computations
Verification script: X was recovered from the black triangles in the GCODE, then Y was recomputed and checked at every coloured vertex.
- **X:** 97 impulses. The positions recovered from the gcode match the piece's X to 0.006 mm.
  - Nearest-neighbour distance: min 7.4, median 14.1, max 43.4 mm.
  - By distance from the focus: 0–50 mm has 50 impulses (median NN 9.8); 50–100 mm has 28 (19.0); 100–150 mm has 12 (32.0); beyond 150 mm has 7 (37.8).
- **Kernels:** each single-impulse peak K(0,0) = 1.0000 exactly (K1, K2, K3). Gabor: λ 12 mm, σ 9.6 mm, support cut at 4.2σ. Blur: σ 3.6 mm, support cut at 4.5σ. The evaluation grid is 0.4 mm and the sum is direct over all impulses on the sheet.
- **Every coloured vertex is explained**, recomputed from the recovered X:
  - K1 (crimson): 8305 vertices. 6672 lie on Y = 0.35 ± 0.02 and 1633 lie in the solid (Y ≥ 1.25). 0 unexplained. Y on vertices spans 0.342–2.887.
  - K2 (blue): 1783 vertices, all on 0.35 ± 0.02 (0.347–0.354).
  - K3 (orange): 1259 vertices. 1241 lie on 0.35 and 18 in the solid. 0 unexplained.
- **Who stands alone** (Y at the impulse within ±0.1 of 1): K1 43/97, K2 42/97, K3 86/97. Y at the impulses spans:
  - K1: −1.58 to 2.63. Gabor stamps interfere, so a crowd can also cancel.
  - K2: −1.02 to 2.74.
  - K3: 1.00 to 1.27.
- **Sum-only region Y > 1.25**, whole sheet:
  - K1: 1072 mm², of which 1039 mm² is drawn as solid after the inset.
  - K2: 768 mm², none of it inside the triangle, so the triangle shows lone stamps only.
  - K3: 12 mm², almost all under chip halos.
  - Max Y: K1 2.91, K2 3.09, K3 1.30.
- **Spacing** (measured on the contours at 0.1 mm sampling):
  - Solid edge to the 0.35 line: min 0.81 mm (K1) and 0.83 mm (K2). It was 0.55 mm before the `SOLID_INSET` = 1.0 mm first-order inset.
  - Distinct 0.35 contours: min 2.78 mm (K1), 2.82 mm (K2), 1.65 mm (K3).
  - Solid hatch pitch is 0.80 mm and shadow hatch 0.9 mm. Grid pitch is 12 mm = λ.
- **Layout:**
  - A4 landscape; drawable area 10–287 × 10–200 mm.
  - Disc: centre (79.3, 80.3), r 79.8, bleeding left and bottom.
  - Square: 70.3 mm side, rotated 18°, centred (145.7, 80.3).
  - Triangle: top edge on y 196.2, the title's top line; apex (235.8, 59.4).
  - Laminate slab from (170.7, 82.2) off to the right and bottom frame.
  - Key block: grid columns 2–9 × rows 3–6 = x 194.7–278.7, y 10.2–46.2. Text rows sit every λ/2 = 6 mm.
  - Title: caps fitted to the 0.45 W title box (≤ 13 mm), weight 1.2 mm, at the top-left.

## Plot budget
The final gcode has 20,276 commands, 4 pens and 997 pen lifts. Longest travel is 281 mm, and it is the inter-layer park. Per layer (within-layer travel):

| pen | meaning | draw | travel | strokes | max hop |
|---|---|---|---|---|---|
| 0 darkorange | Y3 = blur ∗ X | 0.39 m | 0.17 m | 13 | 24.9 mm |
| 1 crimson | Y1 = Gabor 30° ∗ X | 2.86 m | 1.30 m | 242 | 85.4 mm |
| 2 dodgerblue | Y2 = Gabor 120° ∗ X | 0.52 m | 0.32 m | 25 | 69.0 mm |
| 3 black | X confetti, keylines, shadows, grid, type | 10.58 m | 3.71 m | 717 | 123.2 mm |

- Total: draw 14.35 m, travel 6.45 m.
- Time: about 15 min at F2200 (preview estimate 567 s). At Leo's safe settings (F600 draw, 1 s dwells) it is about 60 min: orange ~2, crimson ~10, blue ~2, black ~45.
- Stream order: orange → crimson → blue → black. Light goes first so the black confetti lands on top of every map.
- Nib: 0.3–0.5 mm fineliners. The 0.8 mm solid pitch inks as a solid bar at 0.5 mm.
- Score: `preview --score` gives grade A. Efficiency 0.78 is the dominant issue.

## Self-critique
Scores are 1–10, harsh.
1. **Hierarchy 7.** The disc dominates at 3 m, the triangle is clearly second, and the square sits on top at the focus. The solid red bars make a loud accent exactly where the stack overlaps. The title is fat and competes a little with the disc.
2. **Grid & alignment 7.**
   - The title's top line is shared with the triangle's top edge.
   - The key sits on grid lines, with text rows at λ/2.
   - The laminate edge meets the triangle.
   - The subtitle and captions are hairline, so they do not pick up any grid.
3. **Tension & asymmetry 8.** There is no symmetry: the disc bleeds off the lower-left, the triangle is inverted top-right, the square is rotated 18° over the seam, and the crowd focus sits off-centre.
4. **Negative space 7.** The quiet top-middle zone and the triangle's sparse lower half make the crowd read louder. The lower-left of the square holds a crowd with no orange line inside it, because the blur saturates. This is true, but it reads as missing.
5. **Craft for pen 7.**
   - Spacing is ≥ 0.8 mm everywhere I measured.
   - Keylines are clean.
   - Confetti stays off the keylines.
   - One black hop is 123 mm.
   - About 700 black pen cycles, mostly confetti fills and hatch.
6. **Concept legibility 8.** Lone triangle → ring or three bars, crowd → fused squiggles, crowd → solid. The Memphis joke lands: the laminate's squiggles are caused by its confetti. The caption confirms, and the solid PROVES it (only a sum passes 1).
7. **Depth 7.** Declared: stacked cards with hatched cast shadows over a laminate slab, and confetti thrown over everything.

**Single worst thing:** the orange card's crowd corner. Where impulses crowd, the blur's 0.35 region swallows the whole crowd, so about 15 triangles in the square's lower-left sit on bare card with no orange mark near them. The level-set boundary runs mostly outside the card. It is correct, but it reads as "the map forgot these". The sum-solid for blur (12 mm²) is hidden under the chip halos, so it cannot rescue it.

## Engine requests
- `render_candidate.py` / `merge_chunks` → `reorder_by_color` → `optimize_stroke_order` always re-chains each colour layer with plain nearest-neighbour from (0,0), with no stroke reversal. A piece cannot keep its own order: this plate's greedy + 2-opt order with the legend last is discarded, so "legend swatches last" (A19) cannot be guaranteed from a piece. Please add either a `preserve_order` flag on the pipeline or a 2-opt with reversal inside `optimize_stroke_order`.
