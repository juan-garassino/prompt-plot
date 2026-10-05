# millennium-p-vs-np r02 — abstract · parent: none · 2026-09-29

**Lineage:** Manfred Mohr, *Cubic Limit* (1973–75) and the hypercube works from 1977 (the curator
should verify the catalogue number of the sheet cited). The order taken is a hypercube read by a
rule, where every mark is a selected edge and the rule IS the image. Here the cube is {0,1}²⁰ and
the rule is "halve it at every ring; draw only what is not yet refuted".
**ORDER:** RADIAL + NESTED. **Canon:** RADIAL DATA-VIZ (5) on the series' SWISS sheet (3).
**Declared flat:** the measure coordinate (angle = share of 2²⁰) is exact only on an undistorted
plane.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-p-vs-np/rounds/r02/piece.py \
  --fn pvsnp_needle_radius --seed 7 --paper a3 --margin 15 \
  --palette dimgray,black,black,crimson --out gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3.png
```
- PNG: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3.png`. Pen 0 is previewed in dimgray. It is
  a black 0.1 nib.
- **Physical-width preview** (judge weight on this one): `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3_phys.png`.
  It is made by `render_truewidth.py` (this round), which draws each pen at its nib width on cream
  and prints per-layer stats.
- GCODE: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3.gcode`
- Seed 7. The piece uses no randomness. Seed 11 gives byte-identical gcode below the header
  (checked with diff).
- Tree dump: `rounds/r02/tree.json` (8,047 nodes, from `data/search.py --json`). The piece does
  not read it. It re-runs `data/search.py`'s own `load`/`build` on the CNF at import.

## Mandate responses

| id | mandate | status |
|---|---|---|
| — | No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exists for this slug, so there are no open J*/A*/S* rows. The binding brief is encoding.md §4, §5A, §9 and §11 plus the curator note. | n/a |
| curator | the search tree must be a REAL search, the one verified certificate path in red, checking = linear verification of that certificate | FIXED. Every edge is a node of chronological backtracking on SATLIB uf20-03, computed at import. The red is the model's own root-to-rim path on the same stem/fork/branch geometry (it substitutes for the black and is never drawn over it). The 91 red ticks are the 91 clause evaluations of the certificate. |
| curator | one clean layer per meaningful pen, stated order, strokes batchable, minutes per layer | FIXED. The layers are 0 hair → 1 black → 2 text → 3 red, each contiguous in the gcode (checked). The longest stroke is the red path at 287 mm. Minutes per layer are in the Plot budget below. |
| curator | thousands of tiny node circles must earn their pen cycles | FIXED. There is not one node mark on the sheet. A line that stops is the conflict. The only short strokes are the 91 ticks, one clause each. |
| curator | name the LINEAGE | FIXED (Mohr, see above). |
| enc §11.1 | ONE RED RADIUS at 348.6° ± 0.5°, swings to 9 o'clock first, continues collinear to within 5 mm of the top margin | FIXED. It crosses the rim at 348.628° (the depth-20 node centre). The first fork goes to 270°, then 315°, 337.5°, 348.75°, 343.125° … The tip is at (97.83, 400.45), 4.55 mm under the 405 margin. |
| enc §11.2 | no end inside ring 5; 7 ends at ring 6 every 22.5° from 194°; 14 lines cross the rim | FIXED, from the data. The depth-6 conflicts are at 194.1, 216.6, 239.1, 261.6, 284.1, 306.6 and 329.1°. The ring-crossing counts match the encoding table exactly (see below). |
| enc §11.3 | exactly one black rim contact in the right half (≈169.5°), wedge empty | FIXED. The black rim contacts are at 169.5, 227.1, 235.5, 249.6, 258.0, 280.5, 303.0, 317.1, 325.5, 332.6, 334.0, 336.8 and 339.6°. Only preorder ≤ 7,812 is drawn, so the wedge from 348.628° to 360° holds only the red (and the rim hairline). |
| enc §11.4 | 91 ticks, even pitch, 41/36/14 lengths, 14 side-alternating groups, no arrow/dot; 43,658 vs 91 captioned | FIXED. There are 91 ticks at a 1.35 mm pitch. Histogram {1: 41, 2: 36, 3: 14}. The 14 groups are sorted by closing variable. FINDING says "43,658 CLAUSE TESTS" and CHECKING says "91 CLAUSES, 273 LOOKUPS". |
| enc §11.5 | gcode, 4 layers in order, 2 swaps, ≥ 0.8 mm, weight change at ring 8 captioned, no type on the disc | FIXED. The key says: "BLACK: EVERY NODE OF THE SEARCH TO X8. HAIRLINE: EACH X8 SUB-TREE AS ONE LINE, AS DEEP AS ITS DEEPEST NODE." The spacing audit is below. Type stays ≥ 14 mm from the rim everywhere. |
| enc §9 | forbidden list | Checked item by item. There are no merges, no node marks, no invented branching, one red line, 91 ticks, no arrows/frames/legend box, nothing in the void, no "exponential is necessary" claim, no clock numerals (only "11:37" in a caption), no rotation or mirror, no chords, and no black in the wedge. The title is the largest type. |

## What changed from parent (no parent — the self-rounds)

- **v1.** Built the §5A sheet from the live search. Hub (148.5, 148.5), R 128, pitch 6.4. The
  exact tree runs node for node to x8 in 0.3, with 139 aggregate hairlines, the rim and 12 hour
  ticks. One red stroke goes from the hub to r = 257, plus 91 ticks. Type is set in the left
  column, right of the tip, and in the two spandrels.
- **v2.** The data block had a machine-wrapped break ("91 / CLAUSES"). I rewrote it as authored
  lines and set it on the 3.2 mm caption grid. Its **last baseline sits on y = 282, the top end
  of the 12 o'clock hour tick**, so the column and the dial's time scale share one horizontal.
  Added the tick key under the certificate: "TICK LENGTH: LITERALS MADE TRUE, 1 2 3 · SIDE:
  CLOSING VARIABLE." Without it, the two channels on the comb had no reading.
- **v3.** The spandrel captions are now bottom-aligned on the margin (y = 15). That is the line
  the 6 o'clock tick ends on, so the three tick ends at 3, 6 and 9 o'clock and both captions
  stand on the sheet's edges. Top registrations are the title cap-top at 400, the CHECKING cap-top
  at 400 and the red tip at 400.5.
- Considered and rejected: double-passing the red, as Riemann does for its zeros. The encoding
  says the red wins by colour, not mass. The comb of 91 ticks already gives the needle body at
  3 m, and offsetting a path with 90° stem/fork corners and sub-0.2 mm deep-ring jogs would pinch.

## Measurements / computations (all printed by `python piece.py` or recomputed from it)

- Instance: SATLIB uf20-03, sha256 `23bbf1db…3f62`, 20 vars, 91 clauses, m/n 4.55.
- Search: 8,047 nodes, 4,023 conflicts, 1 model. The model is `11110111111010011101`
  (k = 1,015,453) at preorder 7,812. The refuted mass is 1,048,575 + 1 = 2²⁰.
- Drawn [A]: preorder 1..7,812. **Clause tests to the model are 43,658** (45,088 over the whole
  tree), under the rule that a clause is tested at every node whose depth equals its largest
  variable.
- Red rim angle 348.62829° (the model's interval starts at 348.62812°). Red path 287.2 mm and
  ticks 216.5 mm.
- Lines crossing ring d (aggregates + red):

  | d | 9 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | lines | 140 | 140 | 125 | 99 | 95 | 72 | 42 | 29 | 19 | **14** |

  This is identical to the encoding's table.
- Verification: 91 clauses, 273 lookups, true-literal histogram 41/36/14. Closing-variable groups
  (x6…x20): 1,3,1,2,3,4,5,4,8,13,7,12,10,18.
- **Spacing audit** (scratch script: every stroke is sampled at 0.1 mm and every pair of distinct
  strokes closer than 0.8 mm is flagged, ignoring points within 1.3 mm of a stroke endpoint,
  i.e. designed stem/fork joints and tick bases). **0 violations**, except the red crossing the
  rim hairline, which is a designed crossing.
  - Exact spokes are ≥ 1.178 mm apart at r = 7.5 p, and aggregates ≥ 1.257 mm at r = 51.2.
  - The red is **1.5 mm** from the nearest hairline past ring 8.5. The encoding estimated 1.77,
    measured at a larger radius.
  - The ticks sit at a 1.35 mm pitch.

## Plot budget (A3 portrait, Leo F600 ≈ 10 mm/s, ≈ 2.5 s per pen cycle)

| order | layer | pen | strokes | draw | travel | est. |
|---|---|---|---|---|---|---|
| 1 | HAIR: 139 aggregates, 12 hour ticks, 4 rim quadrants | black 0.1 | 155 | 7.53 m | 2.27 m | ≈ 23 min |
| 2 | BLACK: exact tree to x8, DFS polylines | black 0.3 | 226 | 2.69 m | 2.52 m | ≈ 18 min |
| 3 | TEXT: title (5 chained passes), captions | black 0.3 (no swap) | 910 | 3.14 m | 2.77 m | ≈ 48 min |
| 4 | RED: 1 path+needle stroke, 91 ticks | red 0.5 | 92 | 0.50 m | 0.21 m | ≈ 5 min |
| | **total** | 3 physical pens, 2 swaps | 1,383 | 13.86 m | 7.8 m in-layer (8.86 m with inter-layer park) | **≈ 94 min** |

- Commands: 16,669. `preview --score` gives grade A, efficiency 0.63.
- The postprocess optimiser reorders strokes within each colour, so batch boundaries are whatever
  it emits. No stroke is longer than 287 mm.
- A3 is the design sheet. **A5 (Leo) is not a scale-down**: the depth-8 spokes would fall to
  0.59 mm. Confirm with Juan that Leo takes A3 before the plot job. Trace the frame first, always.

## Self-critique (seven rubric dimensions)

1. **Hierarchy: 7.** The dial dominates, the red hand plus comb is the clear second, and the
   title the third. The 0.1 corona that carries the "eaten haystack" silhouette will be faint
   at 3 m. What reads from across the room is a lacy black hub, a thin circle and the red.
2. **Grid & alignment: 8.** There is one flush-left axis at x = 15, and the title ink ends on
   x = 88. The data block's last baseline is on the 12 o'clock tick top (282). The spandrels
   stand on the 15 margin with the 6 o'clock tick. Three things register at y ≈ 400. The
   CHECKING caption's x = 110 is taken from the encoding, not from a line on the sheet.
3. **Tension & asymmetry: 6.** The hub is centred by necessity (declared). The tension comes
   from the 11.4° red diagonal rising 124 mm out of the disc, the lopsided corona (long left,
   short right) and the empty upper right.
4. **Negative space: 8.** There are three silences, each one a truth: the refuted mass inside
   the rim, the 11.4° wedge after the needle, and the upper-right quiet.
5. **Craft for pen: 8.** The audit is clean, there are no node marks or floods, and the layers
   are contiguous. The text layer is the expensive one (910 pen cycles, ≈ 48 min).
6. **Concept legibility: 7.** One red radius reaches the rim, the needle is pulled out and
   notched 91 times, and the hand stops at 11:37. The mapping lands. The risk is that the dial
   reads as a radial dendrogram, a figure.
7. **Depth: 6.** Flat by declaration. Weight carries the only "depth": 0.3 exact, 0.1 aggregate.

**Single worst thing:** at 3 m the dial risks reading as a well-made radial dendrogram rather
than a Mohr-hard object. The hub's 0.3 lines are lace, not mass, and the 0.1 corona that makes
the lopsided carving legible almost vanishes at distance.

## Engine requests

- None required. `render_candidate.py` cannot preview nib widths, so this round carries its own
  `render_truewidth.py`, as Riemann r01 does. A shared `--pen-widths` flag on the render script
  would retire these copies.
