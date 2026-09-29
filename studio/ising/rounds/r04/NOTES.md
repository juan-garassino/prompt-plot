# ising r04 — iterate (MERGE: r02 sheet + r03/r01 hull vocabulary) · parent: r02 · 2026-09-28

## Render
```
.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r04/piece.py \
  --fn ising_cooling_strip_iterate --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson --out gallery/studio/ising/current/pp_ising_r04_iterate_v5.png
```
Final: `gallery/studio/ising/current/pp_ising_r04_iterate_v5.png` / `.gcode`, seed 7 (the seed the r02 science critic verified).
Seed sweep (v4 geometry): `gallery/studio/ising/trials/pp_ising_r04_iterate_v4_s3.png`, `gallery/studio/ising/trials/pp_ising_r04_iterate_v4_s13.png`.
Iterations:
- v1: hull outlines, cut 30, vertical CRITICAL, key.
- v2: seam roll (unsafe: the frontier guard dropped 82 real coast edges, so it was fixed in v3).
- v3: the seam is chosen so the coast crosses it once, and the guard became cylinder-aware.
- v4: rules moved onto the lattice lines (this removed the 0.65 mm rule/coast parallels).
- v5: the S3 figure is measured on the ruled rows. Geometry is otherwise identical to v4.

## Mandate responses
| id | mandate | status |
|---|---|---|
| A2 | no isolated dots; crop x 230–270, y 20–60 has zero isolated marks and ≥ 50 % bare; travel ≤ 0.6 × draw | FIXED. Dots and singletons are gone: nothing is drawn for FK clusters under 30 sites. The crop is 98.1 % bare (0.5 mm raster) and holds no isolated mark. The only thing in it is part of the closed hull of one 30+ site island at x 235–248, y 40–55. On seeds 3 and 13 the crop is 100 % bare. Travel 6.27 m against draw 11.48 m is 0.547 × draw |
| A4 | a mark-free 60×80 mm rectangle on the hot side, ≥ 25 % bare | FIXED. 419 placements of a 60 × 80 mm mark-free rectangle exist with x ≥ 120, for example x 162–222, y 25.5–105.5. There are 276 placements at 80 × 60, for example x 207–287, y 59.5–119.5. About 45 % of the field (x > 160) carries only about 10 island outlines |
| A6 | canon + lineage in HANDOFF; declare flat | FIXED. HANDOFF carries `canon:`, `lineage:` and `declared: flat` |
| A9 | x 85–130, y 120–180: ≥ 0.8 mm clear between parallel strokes; no solid black cell > 2×2 mm | FIXED. Across the window, the smallest centre distance between the nearest passes of two different parallel edges is 1.08 mm, measured from the gcode. The design minimum is 1.3 − 2 × 0.15 = 1.0 mm for two 3-pass edges one site apart, and 0.82 mm clear at the preview's 0.18 mm stroke. There is no fused cell. It took two changes. (1) Hulls replace bond sticks. (2) The ruled sea's rules now lie ON lattice lines. r02's rules ran through cell centres, 0.65 mm from every horizontal coast step: the only sub-0.8 pairs left in v3 |
| A10 | CRITICAL cap ≥ 18 mm, 2–3 passes, flush-left x = 15 in the ruled sea, no rule stub < 4 mm left of the C | FIXED. The title is rotated 90° and runs up the sea (reading bottom to top). Cap is 18.0 mm, weight 0.6 mm = 3 passes. The ink bbox is x 15.00–33.60, y 56.0–185.9. The title slot removes rules from the cold wall to 1.6 mm right of the baseline, so there are no rule stubs at all left of the C. Rules that would leave a < 4 mm crumb right of the slot are dropped (32) |
| A11 | free droplets as closed dual-lattice wall loops | FIXED. Each FK cluster ≥ 30 sites is drawn as its closed hull: the edges between the cluster and its 4-connected exterior. Enclosed holes are excluded. The rows are unwrapped across the y seam for the flood. No primal-lattice bond is drawn |
| A12 | exactly one crimson polyline; remove the 2-site pinched loop at x 88–91, y 58–59 | FIXED. The hot-connected outside is now 4-connected, so a diagonally pinched pocket counts as a lake and not as coast. The loop is gone. The crimson field geometry is one connected component, 1798 mm of ink = 461 edges × 1.3 mm × 3 passes. A cylinder-aware guard keeps only the largest component and is proven to drop 0 edges. The only other crimson is the r02 1.00 ruler tick and its label |
| S1 | key: FK named, each rung's site range, SINGLE SPINS NOT DRAWN, same mono on the ruling, x = 15 | FIXED. The key lines are `RULED  THE HELD FK CLUSTER`, `FREE FK CLUSTERS  1 2 3 PASSES`, `SITES  30 TO 49  50 TO 154  155 UP` and `SINGLE SPINS NOT DRAWN  NOR UNDER 30`. All are 1.8 mm mono, in ruling gaps, on x = 15 |
| S2 | 3-pass rung typical (≈ ≥ 155), 0 % under-inked, per-rung counts | FIXED. The 3-pass cut is 155. Each of seeds 3, 7 and 13 has exactly one free cluster ≥ 155 (170 / 441 / 403). Every hull edge carries its cluster's rung: an edge shared by two drawn clusters takes the heavier rung, and an edge that is also coast is inked crimson at 3 passes. So 0 % is under-inked. Counts are below |
| S3 | print a check the sheet proves: ruled fraction vs Onsager m | FIXED (it was deferred, but the colophon was rewritten anyway). `UNDER 0.80 TC  0.977  ONSAGER M 0.969`. The first number is the held fraction on the ruled rows, over columns with T/Tc < 0.80. The all-rows value is 0.976. The second number is Onsager–Yang m averaged over the same columns. The unverifiable energy line is removed |
| A1, A3, A7 | — | stay fixed (no chart, one mono face, ruled sea is the cold body) |
| A5, A13, S4, S5, S6 | — | dropped in LEDGER (merged or COASTLINE-only). Not reopened |

## What changed from parent
- **The hot side became negative space.** r02 had 4,743 / 1,776 / 502 bond sticks and 2,819 dots. r04 draws the closed hull of 42 FK clusters and nothing else. The sheet now reads: ruled order → one red coast → a mosaic of heavy coastlines 1.0–1.3 Tc → a few islands → bare cream from about 1.45 Tc.
- **The coast is one line by construction.** The outside is 4-connected, and the seam is placed so the hull crosses it exactly once.
- **The ruled sea moved half a cell.** Rules sit on lattice lines, so every stroke in the field lies on one 1.3 mm grid. Where a hull edge already inks a rule's line, the rule yields (37 cells). Ruled coverage is still exactly the held cells.
- **Type.** CRITICAL is set vertically as a 3-pass, 18 mm spine at x = 15 in its own slot of the sea. The r02 colophon tail (`BONDS …`, `ENERGY VS ONSAGER …`) is replaced by the S1 key and the S3 check. The key has 10 lines, 11 including `TC IS A PLACE`.
- **Seam placement (display only).** The strip is periodic in y, so the configuration is shown rolled by 111 rows. This is an exact translation: the sampler, the FK draw and every statistic are unchanged. It is the roll at which the coast crosses the seam once and the seam touches the fewest drawn-cluster sites (14, against 29 unrolled).
- Unchanged: the sampler, the lattice (212 × 137 at 1.3 mm), the T ramp, the reservoir coupling, the FK bond draw and its key, the thermometer ruler, and 2 pens with 1 swap.

## Measurements / computations (seed 7)
- FK frontier (vertical crimson edges): mean 1.031 Tc, σ 0.063, range 0.933–1.183, x̄ = 93.4 mm. There are 461 hull edges; r02 had 487 with 8-connected outside, and the 26-edge difference is the pinched pockets now counted as lakes. The held cluster is 26.1 % of the lattice. Wolff frozen fraction 0.27. The energy RMS vs Onsager is 0.013 per band, the same as r02 (same chain). It is no longer printed.
- Free FK clusters drawn (≥ 30 sites): 42.
  - 1 pass (30–49): 25 clusters, 928 edges.
  - 2 passes (50–154): 16 clusters, 1,070 edges.
  - 3 passes (≥ 155): 1 cluster of 441 sites, 198 edges.
  - 72 cluster edges coincide with the coast and are inked crimson.
  - The largest drawn sizes are 441, 154, 133, 119, 99, 95, 94, 84, 81 and 68.
- Cut choice. This is the census of free clusters by cut, with the last number counting those whose mean column is past 1.36 Tc:

  | cut | s7 total | s7 past 1.36 Tc | s3 total | s3 past 1.36 Tc | s13 total | s13 past 1.36 Tc |
  |---|---|---|---|---|---|---|
  | 10 | 314 | 140 | 322 | 147 | 310 | 138 |
  | 20 | 98 | 21 | 106 | 24 | 102 | 31 |
  | 25 | 71 | 14 | 67 | 11 | 61 | 10 |
  | 30 | 42 | 7 | 45 | 5 | 41 | 4 |
  | 40 | 24 | 1 | 24 | 1 | 24 | 1 |

  30 is the smallest cut at which all three seeds leave a 61 × 81 mm cell-empty window on the hot side (cut 25 fails on seeds 7 and 13).
- Top rung populated: the largest free cluster is 441 (s7), 170 (s3) and 403 (s13). In each seed there is exactly one ≥ 155.
- S3: held fraction on the ruled rows is 0.977 for T/Tc 0.70–0.80 (0.976 over all rows). Onsager–Yang m, band-averaged over the same columns, is 0.969. r02's critic measured 0.973 from the ink of the text-free rows.
- Seed sweep (all pass A2/A4/A9/A12):
  - s3: coast 1.032 Tc, 1 component, thicket min gap 1.04 mm, travel/draw 0.575.
  - s13: coast 1.038 Tc, 1 component, gap 1.08 mm, travel/draw 0.565.
- Clearance method: every G1 segment is parsed from the gcode. Axis-parallel segments are grouped by coordinate. For pairs 0.45–1.3 mm apart that overlap by more than 0.3 mm, the minimum is taken. Passes of the same edge (≤ 0.3 mm apart) are excluded. The only sub-0.8 pairs left on the sheet are glyph-internal strokes of the 1.8 mm type.

## Plot budget
- Draw 11.48 m, travel 6.27 m (0.547×). 12,821 commands, 684 pen lifts. r02 had 20.75 / 20.41 m, 49,001 commands and 5,958 lifts.
- 2 pens, 1 swap: black (sea, hulls, type, ruler), then crimson (coast, 1.00 tick).
- The previewer estimates 8.9 min. At Leo's F600 with 1 s dwells, expect about 45 min: 19 min drawing, 3 min travel, and about 23 min of lift dwells.

## Self-critique (rubric)
1. Hierarchy — 7. At 3 m the read order is CRITICAL spine, then the red coast, then the black mosaic, then bare paper. The rungs are real, but the 2-pass and 3-pass hulls read only about 1.5–2.5× heavier than 1-pass in the preview. The band is a dense map, not a heavy one.
2. Grid & alignment — 8. Every field stroke sits on one 1.3 mm lattice, type is set in the rule gaps, and there is one left axis at x = 15 (title cap line and key).
3. Tension & asymmetry — 8. Ink occupies the left 45 %, the right 55 % is almost empty, and the coast is jagged at about ⅓ width.
4. Negative space — 7. There is real bare paper, shaped by the physics (cluster size falls off with T). The islands between 1.3 and 1.6 Tc keep it from being a single slab.
5. Craft for pen — 7. Plot time is about a quarter of r02's, spacing is ≥ 1.0 mm centre everywhere in the field, and there is 1 swap. Some clusters cut by the seam leave short open stubs on the top and bottom frame (x 110–140).
6. Concept legibility — 8. Order → coast → coastlines dissolving into nothing, and the key now decodes the weights and names FK.
7. Depth — 5. Declared flat (a lattice configuration; the second axis is T).

**Single worst thing:** the weight ladder is quiet. Holding ≥ 0.8 mm clear between 3-pass edges one site apart caps the pass spacing at 0.15 mm, so "heavy coastlines just past Tc" reads as a busy outline mosaic rather than as black weight. The shared edges between adjacent clusters also make that band look like a jigsaw map.

## Engine requests
- A public `Scene3D.halo_box()`: the title slot still appends to `sc._boxes`.
- A lattice helper `cell_hull(mask, exterior="4"|"8", periodic_y=True)` returning dual-lattice edges. r01, r02, r03 and r04 each re-implement it.
- `geo.offset` treats every polyline as open. Closed loops need a seam miter (worked around locally with `_closed_offset`).
