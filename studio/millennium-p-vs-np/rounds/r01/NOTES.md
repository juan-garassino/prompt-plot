# millennium-p-vs-np r01 — faithful · parent: none · 2026-09-29

lineage: Manfred Mohr, *Cubic Limit* (1973–75) and the n-dimensional hypercube works that
followed it from 1977 (curator: verify the catalogue number of a specific sheet). The order taken
is a hypercube read by a rule, with every mark a selected edge. Here the cube is the 20-cube of
assignments and the rule is "halve it at every row, and draw only what is not yet refuted". Mohr's
vocabulary is orthogonal: every edge is a vertical stem, a horizontal fork bar or a vertical drop.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-p-vs-np/rounds/r01/piece.py \
  --fn p_vs_np_faithful --seed 7 --paper a3 --margin 15 \
  --palette "dimgray,black,black,crimson" \
  --out gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.png
```

- final PNG: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.png`. This is the standard preview, so every
  pen is drawn at one width. Pen 0 is shown in dimgray to stand in for the 0.1 nib.
- true-width companion: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6_truewidth.png` (pens at 0.1 / 0.3 / 0.3 /
  0.5 mm, made with `rounds/r01/render_truewidth.py`). The stats box in the standard preview covers the title,
  so judge the type on this one.
- GCODE: `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.gcode`
- seed 7. The piece uses no randomness. Seeds 3, 7 and 11 give byte-identical gcode bodies
  (md5 `c1890d57…` at v5).
- data: `rounds/r01/tree.json`, from `data/search.py --json` and written into the round, never into
  `data/`. The Petersen tree is computed inside `piece.py`, rebuilding `hamilton.py`'s graph the same
  way. **Deviation:** the encoding asked for a new `data/petersen_tree.py`, but I kept all my writes
  inside my round. The counts match `hamilton.py` exactly: 274 / 48 / 24 / 0.
- audit: `.venv/bin/python studio/millennium-p-vs-np/rounds/r01/audit.py <gcode>`

## Mandate responses

There is no FEEDBACK.md, LEDGER.md or DESCRIPTION.md for this slug, so there are no open J/A/S rows. The
binding briefs are the curator note and encoding §9/§11. Each is answered below.

| id | mandate | status |
|---|---|---|
| CUR-1 | interpret the reference, never trace it | FIXED. Only the reference's layout was measured (table below). Every mark in the field is a node of the real search or an exact aggregate of one. |
| CUR-2 | a REAL search, with the one verified certificate path in red | FIXED. Chronological backtracking on SATLIB uf20-03: 8,047 nodes, 4,023 conflict leaves, 1 model. The red is recomputed from the model bits `11110111111010011101`: root → row 20, exact at every depth. |
| CUR-3 | the checking side is the linear verification of that certificate | FIXED. The chain has 91 red ticks, one per clause, and each tick's length is the number of true literals (41/36/14). It is ordered by closing variable, with the side alternating by group (14 groups). |
| CUR-4 | one clean layer per meaningful pen, stated order, batchable, minutes per layer | FIXED. See Plot budget. The order is 0.1 → 0.3 → text (same pen) → red, which is 2 swaps. |
| CUR-5 | tiny node circles must earn their cycles | FIXED. There are no node marks at all. The only short strokes are the 91 red ticks, and each one is a clause. |
| CUR-6 | name the lineage | FIXED (Mohr, above and in HANDOFF). |
| §11.1 | ONE RED RADIUS: ends at x = 273.6 ± 0.5 | FIXED. The red is one stroke that ends at (273.566, 100.0). |
| §11.2 | carving: nothing ends inside row 5, 8 first ends at row 6, 15 lines at row 20 | FIXED. There are 8 row-6 ends, at x 158.9 … 275.7 (all x1 = TRUE). 15 lines reach row 20: 14 black and the red. |
| §11.3 | lopsided: exactly one black line reaches row 20 in the left half, at x ≈ 140 | FIXED. The only one is at x = 141.2 (sector 60). |
| §11.4 | 91 ticks, even pitch, 41/36/14, 14 groups, no arrow, no second red element; captions give 45,088 against 91 and name the method | FIXED. There are 91 ticks at pitch 1.3744 with 14 groups. The captions read "CHECKING: 91 CLAUSES, 273 LOOKUPS" and "FINDING: BACKTRACKING X1..X20, FALSE FIRST — 8,047 NODES, 45,088 CLAUSE TESTS". **Deviation:** the pitch is 1.3744 instead of 1.35, because the chain now spans exactly from the START axis (x = 148.5) to the SOLUTION axis (x = 273.57). The clear gap is 0.87 mm with the 0.5 nib. |
| §11.5 | gcode, 4 layers in order, 2 swaps, ≥ 0.8 mm, weight change at row 7 captioned, no type in the field, Petersen zero red, no boxes/circles | FIXED. The minimum vertical centre-to-centre is 2.086 mm (a clear gap of 1.78 mm at 0.3). The weight changes at y = 262.5, and the FINDING caption says why. The nearest type to the field is SOLUTION, 6.2 mm below row 20. |
| §9 | forbidden list | Honoured. The tree never merges, and there are no node marks, invented twigs, arrows, frames, axes, tone, clock furniture or giant glyphs. There is one red path plus the verification chain. The captions say "THIS SEARCH, NOT THE PROBLEM" and never say exponential or ≠. |
| §5F | the right column is flush-left at x = 190 | CHANGED to x = 181.875, the crown stem of node (x1 = T, x2 = F), so the column shares an axis with the tree. Its baselines 377/372 sit on the statement's two baselines. |
| §5F | method line full width at baseline 20 | CHANGED. It became a 4-line FINDING caption in the right column, under CHECKING, on the same baselines (33.5 … 23.6) as the NO caption on the left. Full width at 1.8 mm, it ran to two cramped lines that collided with the Petersen caption (v1). |

## What changed from the reference (layout fixes)

The reference was measured on its 1024×1536 raster (u = x/W, v = y/H from the top):

| reference element | measured | faithful r01 |
|---|---|---|
| title "P vs NP" | u .038–.288, v .021–.059 | `P VS NP`, 10 mm caps with 1.2 mm weight (5 linked passes), flush-left x = 15, baseline 392 |
| statement, 4 spaced-caps lines, left | v .090–.145 | Clay's sentence in 2 lines of 2.5 mm caps at baselines 377/372, plus a 1.8 mm instance line (SATLIB UF20-03 … 2²⁰ = 1,048,576 CANDIDATES. ONE SATISFIES ALL 91.) |
| P = {…} / NP = {…} left, italic quote top right | v .174–.262 / u .749–.967 | one right column: series caption, then P / NP / "P IS INSIDE NP. EQUAL? OPEN." |
| START with a red circle, centred | u .467–.532, v .014–.022 | `START` label only, centred on the root x = 148.5. No circle. |
| tree: a lattice that merges, bushy and uniform to the bottom | u .03–.97 | the real tree, which never merges: stem / bar / drop on x = 15 + 267 m. Complete to row 5, pruned from row 6, one survivor at row 20. |
| blue waypoint rings on the thread | 9 rings | cut (lie 9) |
| red thread wanders about the centre, ends at u .50 | x 448–612 px | the true path. It steps right (215.3, 248.6, 265.3, 273.7, 269.5 …) and ends at x = 273.57, **96.8 % of the width**. |
| SOLUTION with a red circle | u .447–.556, v .90 | `SOLUTION` label only, flush-right at x = 282 under the red's end |
| Hamiltonian inset box + FINDING toy tree, "typically exponential" | two boxes | the Petersen NO search: all 274 nodes, zero red, "LEAF ORDER, NOT TO MEASURE". The "typically exponential" claim is cut. |
| CHECKING: 5 nodes with an arrow, "polynomial in the size of the solution" | box | 91 red ticks, no arrow, "THE TESTS ALONG THE RED ALONE" |
| "SAME PROBLEM. DIFFERENT WORLDS?" | v .95 | cut. The FINDING caption takes its place, ending "THIS SEARCH, NOT THE PROBLEM: UNIT PROPAGATION NEEDS 87 NODES." |

Self-rounds:
- v1 was the encoding's §5F as written.
- v2 regrouped the bottom band into two captions on shared baselines and moved the instance line up to the title band.
- v3 tightened the title from `P  VS  NP` (it read as three loose letters) and made it heavier. The chain was re-spanned START axis → SOLUTION axis.
- v4 moved the definitions column onto a crown stem and added the audit.
- v5 authored a single-stroke sans `I`, which cut about 120 pen cycles, and made `·` visible.
- v6 rewrapped the NO caption to four full lines with no orphan.

## Measurements / computations

- Search (`data/search.py`, sha256 of the CNF is `23bbf1db…`):
  - generated per depth: `[1,2,4,8,16,32,64,112,224,288,504,860,1136,1284,986,996,726,346,276,106,76]`
  - conflicts per depth: `[0,0,0,0,0,0,8,0,80,36,74,292,494,791,488,633,553,208,223,68,75]`
  - the model is found at preorder 7,812 of 8,047
  - DPLL on the same instance takes 87 nodes
- Aggregate below row 7: 112 depth-7 sub-trees, each drawn as one hairline from row 7 down to its deepest row. 111 are drawn, because the red substitutes for sector 123. The deepest rows by sector are in `piece.deepest_below()`. 15 sectors reach row 20 (k₇ = 60, 80, 83, 88, 91, 99, 107, 112, 115, 118, 119, 120, 123, 126, 127).
- Sectors 124 and 125 do not exist: node 111110 is a depth-6 conflict. Its stub ends at row 6 at x = 275.7, directly right of the red. The nearest black to the red's right past row 7 is sector 126 at x = 278.9.
- Red geometry: node x at d = 1…7 is 215.25, 248.63, 265.31, 273.66, 269.48, 271.57, 272.61, converging to 273.566.
- Verification: the true-literal histogram is {1: 41, 2: 36, 3: 14}. The closing-variable groups are x6, x8…x20 (14 groups). There are 273 literal lookups.
- Petersen: 72 leaves at 1.1 mm (x 15.0–93.1) and 10 levels at 5 mm (y 85 → 40).
- Spacing:
  - vertical neighbours at every row are ≥ 2.086 mm centre-to-centre
  - red to the nearest hairline is ≥ 2.08 mm (at row 7)
  - chain ticks are 1.374 mm apart
  - Petersen drops are 1.1 mm apart (0.8 mm clear at 0.3)
- Ink bbox: 15.0–281.7 × 23.4–402.6. Bounds are clean.

## Plot budget (A3 portrait, Leo F600 ≈ 10 mm/s, 2.5 s per pen cycle, travel ≈ 33 mm/s)

| order | layer | pen | draw | travel | strokes | ≈ min |
|---|---|---|---|---|---|---|
| 1 | HAIR: the aggregated search below row 7 | black 0.1 | 10.84 m | 2.98 m | 111 | 24 |
| 2 | BLACK: rows 0–7 node for node + Petersen | black 0.3 | 4.35 m | 4.52 m | 191 | 18 |
| 3 | TEXT (same pen, own layer, no swap) | black 0.3 | 3.95 m | 3.70 m | 1,055 | 52 |
| 4 | RED: the certificate path (1 stroke) + rule + 91 ticks | red 0.5 | 0.73 m | 0.83 m | 93 | 6 |

- Total ≈ 100 min, 2 physical swaps, 11,816 commands.
- Batching:
  - Every tree stroke is a vertical line or a DFS polyline ≤ ~430 mm, so any stroke is a batch boundary.
  - The Petersen tree is spatially separate: 72 runs in the lower-left.
- The text layer is the cost: about 1,055 pen cycles is ~44 min of dwell. The pipeline's nearest-neighbour reorder
  (`merge_chunks`) overrides the authored left→right order inside each layer.
- **Confirm with Juan that Leo takes A3.** An A5 edition is a re-layout, not a scale-down (encoding §10).

## Self-critique (rubric, honest)

1. **Hierarchy: 8.** The black crown dominates at 3 m. The red thread, the one colour, stepping to the right edge, is the second read. The pale curtain and the red comb are third.
2. **Grid & alignment: 8.** Everything shares a small set of lines:
   - x = 15 carries the title, statement, instance, curtain, Petersen and NO caption.
   - x = 148.5 carries START, the root and the left end of the chain and FINDING.
   - x = 273.57 carries the red's end, SOLUTION and the chain's right end.
   - The definitions column stands on a crown stem.
   - The two bottom captions share baselines.
3. **Tension & asymmetry: 7.** The root is centred by the measure, but the red runs to 96.8 % of the width. The curtain is short on the left and long on the right, and the lower-left is carved away.
4. **Negative space: 7.** The carved lower-left is real (refuted space), and so are the empty 12.5 mm row bands in the crown. The gap between the Petersen tree and the chain is leftover rather than shaped.
5. **Craft for pen: 8.** Spacing is ≥ 2.08 mm in the field, and there are no fills and no ink on ink. Weight carries a truth: 0.3 means exact, 0.1 means aggregate. The text layer is heavy on pen cycles.
6. **Concept legibility: 7.** "A huge pruned search, one red thread that reaches the bottom only at the far right, and a short counted comb" lands without the caption. At rows 0–5, though, the crown is a complete binary bracket, so the upper half reads as a tournament bracket or dendrogram, which is a figure-like form, until the carving starts at row 6.
7. **Depth: flat by declaration** (Swiss sheet plus the exact measure coordinate: any tilt would make equal shares unequal). The depth cue is weight: 0.3 exact over 0.1 aggregate.

**Single worst thing:** the upper crown. Rows 0–5 are the complete binary bracket, because no clause closes before x6. This is true, but it is visually the most generic part of the sheet, a textbook dendrogram occupying the top 90 mm, and it takes the eye before the carving does. A rework could compress rows 0–5 (radius as any monotone function of depth is allowed by the dossier, so a stepped row pitch is legal) and give the pruned rows 6–20 the height.

## Engine requests

- `render_candidate.py --pen-widths` so the standard preview draws a 0.1 hairline thinner than a 0.3. Riemann
  r01 asked for the same thing. This round reuses its local true-width rasteriser.
- A flag on `merge_chunks` / `reorder_by_color` to keep the authored stroke order inside a layer, so batch order
  is guaranteed rather than nearest-neighbour.
- Stroke-font candidates for `_GLYPHS`: `?` (authored here) and a single-stroke sans `I`. The house `I` has
  serifs and costs 3 pen-downs per letter.
