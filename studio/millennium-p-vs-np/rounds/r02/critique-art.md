# Art critique — millennium-p-vs-np r02 [A] · canon: RADIAL DATA-VIZ (5) on the SWISS series sheet (3), a stated hybrid · 2026-09-29
render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3.png (+ `_phys.png`; gcode parsed for every measurement below)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 8 | Three clear levels. The dial is the mass, the red needle is the loud scarce accent, and the 10 mm title is the only large type. The 0.3 core against the 0.1 fringe gives the dial a readable dark heart at r 35–51. |
| 2 | grid & alignment | 8 | The left column is flush at x=15 from the title down to the instance block. The instance block's foot (y 282.0) sits on the top of the 12 o'clock tick. The needle caption's cap line (y 400.4) meets the title's. Weak spot: the two bottom spandrels are corner furniture (rubric failure mode 2). |
| 3 | tension & asymmetry | 8 | The centred dial is declared and forced by the width. The needle's 11.4° lean into the empty upper right carries the tension, and so does the carved right half (one rim contact on the right against 12 on the left, a crescent of paper inside the right rim). |
| 4 | negative space | 7 | The upper-right quiet (167×105 mm) is earned. Nothing else breathes, though. The dial's ticks sit on the 3, 6 and 9 o'clock margins. Two 5-line blocks of 1.8 mm caps are wedged into the leftover bottom corners, so the bottom 40 mm is the most crowded strip on the sheet while the top half is empty. Canon 5 asks for the outer margin to breathe. |
| 5 | craft for pen | 8 | Spacing is clean: aggregate starts ≥1.248 mm, ring-8 spokes ≥1.18 mm, red ticks 1.345–1.357 pitch (0.85 mm clear at 0.5 nib). No floods or knots. The 1.8 mm type holds open counters at true 0.3 width. 4 layers, 2 physical swaps. Docked because the gcode draws at **F2000/F1500 with 0.2 s dwells** while HANDOFF states F600 (Leo needs F600 and ~1.0 s dwells). The black layer also travels 2.52 m for 2.69 m of ink: it is not batched clockwise from 12 as §10 asks (it starts at 224°). |
| 6 | concept legibility | 8 | Not a schematic, not a figure. The order reads: a halving tree swept clockwise, most of it stopping, one red radius escaping the disc as a notched rule. Held back from 9 because the find-vs-check contrast, the thesis in numbers, is split: 43,658 sits in 1.8 mm prose in the bottom-left corner and 91 in the top-right caption, about 380 mm apart. §2 promises "the two counts sit side by side". |
| 7 | depth & dimensionality | 8 | Flatness is declared (measure coordinate). Depth is carried by three honest weights (0.3 exact / 0.1 aggregate / 0.5 red), and the needle literally leaves the disc's plane. |

avg **7.86** · min **7** · **VERDICT: FAIL** (avg < 8)

## Reads at a glance
At 3 m: a spiky black wheel pressed into the foot of the sheet, with one red notched needle drawn out of it up to the top edge, where the title sits.

## Acceptance checks (encoding §11, [A])

1. **ONE RED RADIUS: PASS.**
   - Rim crossing at 348.628°, at (123.26, 273.99).
   - Path node angles are 270 / 315 / 337.49 / 348.76 / 343.12°, then 345.9 / 347.3 / 348.05° converging.
   - The needle is straight and collinear to r=257.0 (348.629°). It ends at y=400.45, 4.55 mm under the top margin.
   - Only one red line exists: 1 path plus 91 ticks, no other red.
2. **THE CARVING: PASS.**
   - No refutation ends inside ring 5. The black stubs below ring 6 end exactly where the red takes over, at 180 / 270 / 315 / 337.5 / 343.1°.
   - 7 ring-6 ends, at 194.1, 216.6, 239.1, 261.6, 284.1, 306.6 and 329.1°.
   - Crossing counts match the table: 139 black + red at rings 9–12, then 124/98/94/71/41/28/18/13.
   - 13 black rim contacts + the red = 14. Refuted areas are bare paper.
3. **LOPSIDED, AND THE WEDGE: PASS.**
   - Rim contacts: 169.5, 227.1, 235.5, 249.6, 258.0, 280.5, 303.0, 317.1, 325.5, 332.6, 334.0, 336.8 and 339.6°. Only 169.5° is in the right half.
   - Zero black points in 348.63°→360°.
4. **CHECKING IS THE RED, AND IT COUNTS: PASS.**
   - 91 ticks at pitch 1.35 ± 0.006, lengths 1.5 / 2.75 / 4.0 = 41 / 36 / 14, in 14 side-alternating groups.
   - No arrow, no dot.
   - The captions carry 43,658 and 91 and name the method. They pass as captions, but they are not juxtaposed; see the mandates.
5. **PLOTTABLE AND CLEAN: PASS.**
   - The gcode sits beside the png, with layers 0→1→2→3 and 2 physical swaps (1 and 2 share a pen).
   - Minimum spacing is ≥0.8 mm.
   - All 139 aggregates start at exactly r=51.2 (ring 8), and the legend states why.
   - The nearest type is r=150.3 from the hub, outside the tick ring (133.5).

AUTHORING §6 (reference = interpretation brief; the dial is a legitimate re-reading of the reference's START→SOLUTION tree):

1. Forms recognisable without fills: PASS.
2. Shadow lines follow the surface: n/a, no hatch.
3. Double-edged strokes: PASS, none.
4. Blackest regions intended: PASS. Rings 5–8 are the exact node-for-node search.
5. Labels at true width: PASS. 1.8 mm caps at 0.3 keep their counters.
6. Thick-pen knots: PASS. The red 0.5 ticks keep 0.85 mm clear, and the red crosses the rim cleanly.
7. Empty travel / tiny marks: PARTIAL. Black-layer travel ≈ its ink (2.52 m / 2.69 m). The type layer is 910 strokes, about half the plot time.

Lost from the reference and worth keeping: the reference juxtaposes FINDING and CHECKING as a pair. The abstract dropped that pairing.

## Biggest weakness
The plate states its thesis in ink (black mass versus one red line) but not in its numbers, and it has run out of room at the bottom. The comparison that makes this P vs NP rather than "a search tree" is 43,658 tests to find against 91 to check. That comparison is split between the two far corners in 1.8 mm prose. Meanwhile the dial is jammed against three margins, with type stuffed into the leftover bottom corners, while the whole upper half sits empty.

## Mandates

1. **Pair the two counts at display size in the left column.**
   - Set `43,658` and `91` together as one flush-left unit at x=15, between the statement (foot ≈ y 363) and the instance block (top y 306), e.g. baseline ≈ y 335–345.
   - Numerals at 4–5 mm caps (below the 10 mm title), each with a 1.8 mm label beneath: `CLAUSE TESTS TO FIND (THIS SEARCH)` / `TO CHECK THE NEEDLE`.
   - Remove 43,658 from the bottom-left prose.
   - Test: both numbers are within 25 mm of each other, cap height ≥ 4 mm, and nothing crosses x = 88.
2. **Empty the bottom corners.**
   - Move the FINDING spandrel's method line and the whole "THIS SEARCH, NOT THE PROBLEM … OPEN." block into the left-column stack. They belong under the counts pair from mandate 1, between y 306 and the pair, or in the free band y ≈ 262–280 left of x = 60 if they fit without touching the rim.
   - The dial then sits alone on the bottom margin, with its 6 o'clock tick the only mark below y = 60.
   - Test: no type below y = 260, and every type block except the needle caption starts at x = 15.
3. **Plot parameters and batching match the HANDOFF.**
   - The gcode must draw at F600 with ≥1.0 s pen dwells (Leo drags ink at F2000 / 0.2 s).
   - Layers 0 and 1 must stream clockwise from 0° in depth-4 sector batches, as §10 states. Today the black layer starts at 224° and travels 2.52 m for 2.69 m of ink.
   - Test: `grep -c F2000` = 0, the first black stroke starts in [0°, 22.5°), black-layer travel < 1.5 m, and the HANDOFF time estimate is recomputed from the real feed.

## Follow-up on open mandates
No LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists for this slug, and HANDOFF gives compare-to: none. r01 is the parallel faithful thesis, not this plate's parent. No open A*/J* mandates to track.

| id | status | evidence |
|---|---|---|
| — | — | none open |

## Regressions vs compare-to
None assessable: this is a new plate with no parent render and no DESCRIPTION § Keep items.
