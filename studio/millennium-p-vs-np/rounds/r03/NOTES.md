# millennium-p-vs-np r03 — iterate · parent: r02 · 2026-09-29

**Lineage:** unchanged from r02. Manfred Mohr, *Cubic Limit* (1973–75) and the hypercube works
from 1977: a hypercube read by a rule, where the rule IS the image. The catalogue number of a
specific sheet is still for the curator to verify.
**Canon:** RADIAL DATA-VIZ (5) on the SWISS series sheet (3). **ORDER:** RADIAL + NESTED.

## Render

```
.venv/bin/python studio/millennium-p-vs-np/rounds/r03/render_plot.py \
  --out gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.png
.venv/bin/python studio/millennium-p-vs-np/rounds/r03/audit.py \
  gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.gcode gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3.gcode
```
- `render_plot.py` is the round-local wrapper for A2. It uses the same pipeline as
  `scripts/render_candidate.py`, with A3 portrait, margin 15, palette
  dimgray,black,black,crimson. It sets `config.pen.feed_rate = 600` and
  `pen_up_delay = pen_down_delay = 1.0`. It writes the png, the gcode and a `_phys.png`
  true-width raster, then re-reads the gcode to print the per-layer budget.
- The piece emits F600 on every G1. Nothing under `promptplot/` is edited.
- The `fn` is `pvsnp_needle_radius`, with seed 7. The piece uses no randomness: the seed 11 gcode
  is byte-identical below the header (diffed).
- Final files:
  - PNG: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.png`
  - physical-width preview (judge on this one): `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3_phys.png`
  - GCODE: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.gcode`
- Self-rounds: v1 (first stack), v2 (the pair re-spaced as two units), v3 (the sans I set
  proportionally).

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | One left-column stack. The dial sits alone at the foot. 43,658 / 91 within 25 mm, cap ≥ 4 mm. No type below 260. Blocks at x = 15, ≤ 88, clear of the rim. Only the dial below y 60 | **FIXED.** Every word except the needle caption is one flush-left stack at x = 15, measured from the gcode ink: x 15.00–87.30. The stack is set bottom-up, and its last baseline sits on **y = 276.5, the rim's top tangent**. The lowest type is at y 276.50, and the minimum type-to-hub distance is 151.3 mm (the rim + 14 needs 142). Both bottom-corner blocks are gone. The only ink below y = 60 is dial (pen 0). The numerals are 4.5 mm caps (3 chained 0.3 passes). Their ink bottoms are at 355.9 (43,658, comma included) and 338.9 (91), so the two numerals are **≈ 17 mm apart**. 43,658 no longer appears in any prose. |
| S1 | DPLL at node 82. The clause-test convention stated beside 43,658 | **FIXED.** The line now reads "DPLL FINDS IT AT NODE 82." This is a find count on the same basis as "7,812 NODES … FOUND AT 11:37". The convention is the second line of the 43,658 label: "EACH CLAUSE TESTED AT ITS LAST VARIABLE". It sits directly beside the number, not in the method line two paragraphs down. That is where S1 asks for it; the SYNTH lists it with the method. The number 87 does not appear anywhere. |
| S2 | Key the dial in plain words. P / NP definitions. Retire "HAIRLINE: EACH X8 SUB-TREE" | **FIXED.** The key reads "THE DISC IS ALL 1,048,576 CANDIDATES. / EACH BRANCH'S ANGLE IS ITS EXACT SHARE. / BLANK PAPER IS REFUTED. / THIN LINE: ONE BRANCH'S DEEPEST REACH." The definitions are r01's text, merged and cut to two lines: "P: FOUND IN POLYNOMIAL TIME. / NP: CHECKED IN POLYNOMIAL TIME." Cut for strokes: "(1,048,575)" after REFUTED, "PAST RING 8," (the thin lines are visibly the outer ones) and r01's "given a certificate. P is inside NP. Equal? open.". The last clause is carried by the honest line "A SHORTCUT FOR EVERY CASE? OPEN.", and the certificate is the red, labelled "TO CHECK THE NEEDLE". |
| S3 | Caption the hour ticks: equal shares of candidates, reached clockwise, not equal time | **FIXED.** The caption reads "HOUR TICK: 1/12 OF THE CANDIDATES, / REACHED CLOCKWISE, NOT EQUAL TIME." "FOUND AT 11:37" is kept. |
| A2 | gcode at F600 with G4 P1.0 dwells via a round-local wrapper. Minutes recomputed from it | **FIXED.** The G1 feed values in the gcode are `{600: 10208}`; `grep -c F2000` = 0. There are 2,973 dwells, all `G4 P1`. The engine formats the float 1.0 as `P1`; Grbl reads it as 1 s, so this is the same dwell. Minutes are in the Plot budget, read off that gcode. |
| S4 | Type ≥ 10 mm from the red (r02 measured 6.2) | **FIXED.** The measured minimum is **10.74 mm**, over every type sample against every red sample, ticks included. r02's 6.2 mm was the CHECKING caption against the right-pointing top ticks, so the caption moves x 110 → **115**. The title's ink now ends at x 87.3 rather than 88, which clears the left-pointing ticks at y 400. |
| A3 | Black layer clockwise from 12 in depth-4 batches | **DEFERRED** (engine request, unchanged). `merge_chunks → reorder_by_color` replaces the authored order with nearest-neighbour. |
| S5, A4 | r01 mandates | dropped in LEDGER (r01 is not the parent). Nothing of r01's layout came across. |

## What changed from parent

- **Composition: the type now has one home.** r02 spread its words over four places: the left
  column, the top right, and the two bottom corners. r03 keeps two:
  - one flush-left column, reading top to bottom as a proof sheet: title → question → the thesis
    in numbers (43,658 over 91) → how to read the disc → what the instance is → how the search
    went → what this does not prove → what P and NP mean;
  - the needle caption at the top right, which stays because it captions the needle's tip.

  The dial now sits alone on the lower 260 mm of the sheet, and its foot and flanks are
  blank paper.
- **The stack stands on the rim's top tangent (y 276.5).** Column and disc share one horizontal.
  The column's top is still the title cap line at y 400, registered with the needle tip (400.45)
  and the CHECKING cap line (400.0).
- **The pair is the second level of the type hierarchy.** It is the only type between the title
  (10 mm) and the captions (1.8 mm) apart from the 2.5 mm question. Each count is a tight unit
  (numeral, 1.6 mm, label), and the two units are 5.8 mm apart. The reading 43,658 then 91 runs
  down the column like a subtraction.
- **Craft:**
  - The house `I` has 3 strokes (stem plus two serifs). This round uses r01's single-stroke sans
    `I`, set proportionally, so "BACKTRACKING" has no hole at the I. That cut about 80 pen cycles.
    `1` keeps its flag and foot, so `I` and `1` stay distinct.
  - The tick key was shortened to "TICK: TRUE LITERALS 1 2 3 · SIDE: LAST VARIABLE.", which uses
    the same "last variable" term as the 43,658 convention.
- **Unchanged:** the tree, the red, the ticks, the hour ticks and the rim. `audit.py` shows that
  pens 0, 1 and 3 are identical to r02's gcode as stroke multisets: 155 / 226 / 92 strokes, with
  coordinates equal to 3 decimals.

## Measurements / computations

Everything here comes from `audit.py`, which reads the r03 gcode against r02's gcode, and from
`python piece.py`.

**Science numbers.** All are live from `data/search.py` on uf20-03.
- Search: 8,047 nodes, with the model at preorder 7,812. 43,658 clause tests to the model
  (45,088 over the whole tree).
- Certificate: the red rim angle is 348.628°. There are 91 ticks, with lengths 41/36/14 by
  literals made true, in 14 groups.
- Tree: depth-6 conflicts at 194.1 … 329.1°, 139 aggregate hairlines, and 13 black rim contacts.

**Layout.**

| check | measured | required |
|---|---|---|
| type → red (path + ticks) | 10.74 mm | ≥ 10 |
| type → hub | 151.27 mm | ≥ 142 (R + 14) |
| type lowest y | 276.50 | ≥ 260 |
| left stack x | 15.00–87.30 | 15–88 |
| needle caption x from | 115.00 | clear of the red |
| upper-right quiet [115, 282] × [285, 385], non-red ink | 0 samples | empty |
| pair (ink bottoms) | 355.9 / 338.9 (Δ ≈ 17 mm), cap 4.5 | ≤ 25 mm, cap ≥ 4 |

Block extents on the sheet, in mm, y up:

| block | y |
|---|---|
| title | 389.7–400.4 |
| statement | 369.7–381.0 |
| 43,658 + label | 349.6–361.1 |
| 91 + label | 335.5–343.8 |
| key | 311.5–329.5 |
| instance | 303.5–308.7 |
| method | 295.5–300.7 |
| honest limit | 284.5–292.7 |
| P / NP | 276.5–281.5 |

Gaps: statement → pair 8.6 mm, 91 → next label 5.8 mm, key → pair 6.0 mm. The title → statement
gap is 8.7 mm.

## Plot budget (A3 portrait, from the r03 gcode)

The per-layer figures are read off the gcode. Time basis: (draw + travel) at 10 mm/s, plus the
real G4 dwell seconds, plus 0.5 s servo per lift and per drop.

| order | layer | pen | strokes | draw | travel | G4 | est. |
|---|---|---|---|---|---|---|---|
| 1 | HAIR: 139 aggregates, 12 hour ticks, rim | black 0.1 | 155 | 7.53 m | 2.27 m | 310 × 1 s | ≈ 24.1 min |
| 2 | BLACK: exact tree to x8 | black 0.3 | 226 | 2.69 m | 2.52 m | 452 × 1 s | ≈ 20.0 min |
| 3 | TEXT (same pen, own layer, no swap) | black 0.3 | 1,013 | 3.71 m | 2.68 m | 2,026 × 1 s | ≈ 61.3 min |
| 4 | RED: path + needle, 91 ticks | red 0.5 | 92 | 0.50 m | 0.21 m | 184 × 1 s | ≈ 5.8 min |
| | **total** | 3 physical pens, 2 swaps | 1,486 | 14.44 m | 7.68 m in-layer (8.74 m incl. park) | 2,972 s | **≈ 111 min** |

- Commands: 17,641. There are 0 G1 moves with the pen up. `preview --score` gives grade A,
  efficiency 0.65.
- The total is higher than r02's "≈ 94 min" because that figure costed 2.5 s per pen cycle at
  F600 while its gcode carried P0.2. This one is costed from the real 1 s dwells.
- TEXT is 1,013 strokes. That is +103 over r02's 910 and 13 over the ≈ 1,000 ceiling. It is
  the pen-cycle-bound layer: 34 of its 61 minutes are dwells.

## Self-critique (seven dimensions)

1. **Hierarchy: 8.** The dial comes first, the red needle second, then title, pair and
   captions. At 3 m the pair (43,658 / 91) is now the first thing read after the title, which
   is the thesis in numbers.
2. **Grid & alignment: 8.** There is one flush-left axis at x 15 from 400 to 276.5, and the stack
   foot sits on the rim tangent. The captions run on a 3.2 mm grid, with 1.6 mm paragraph
   breaks. The needle caption at x 115 is set by clearance, not by a line on the sheet.
3. **Tension & asymmetry: 7.** The dense upper-left column now weighs against the empty upper
   right, with the red diagonal between them. The bottom corners are empty, so the disc floats.
4. **Negative space: 8.** The bottom 40 mm is dial only. The upper-right quiet is intact, and so
   are the wedge and the refuted mass.
5. **Craft for pen: 7.** F600, 1 s dwells, contiguous layers and 0 pen-up G1. The type layer is
   still 55 % of the plot time.
6. **Concept legibility: 8.** The sheet now says what the disc is, what blank means, what a thin
   line is, what the ticks are, and what P and NP are.
7. **Depth: 6.** Flat by declaration, unchanged.

**Single worst thing:** the left column is now a dense 124 mm slab of 1.8 mm caps (17 caption
lines). It reads as one block at distance. It is also the most expensive thing on the sheet to
plot: 1,013 pen cycles and about 61 min for type, against about 50 min for all the geometry
together.

## Engine requests

- (carried) `render_candidate.py` needs `--feed` / `--dwell` flags, so plot-rate gcode does not
  need a per-round wrapper (this round's `render_plot.py`), and a `--pen-widths` flag for
  true-width previews.
- (carried, A3) `merge_chunks` / `reorder_by_color` needs a keep-authored-order flag.
- `GCodeCommand` formats `G4 p=1.0` as `G4 P1`. That is correct for Grbl, but a dwell-format
  test like `grep 'G4 P1.0'` misses it.
- The house `_GLYPHS["I"]` is 3 strokes. A single-stroke sans `I` with proportional advance,
  used series-wide, would save about 5–10 % of every type layer's pen cycles. It has now been
  authored locally twice (r01, r03).
