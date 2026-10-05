# ising r07 — iterate (r05 + the Schotter ending by physics) · parent: r05 · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r07/piece.py \
  --fn ising_cooling_strip_r07 --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson,gray --out gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png
```
- Final: `gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png` / `.gcode`, seed 7.
- Seed sweep: `gallery/studio/ising/trials/pp_ising_r07_iterate_v5_s3.png`, `gallery/studio/ising/current/pp_ising_r07_iterate_v5_s13.png`.
- Iterations:
  - v1: T_max 2.30, NY 129, the coast keep-out, serpentine rules, the 5-line footer. Travel 0.52×. Worst thing: 48 parallel pairs at 0.12 mm inside the 3-pass continent (the pass-2 miter at concave corners running into the opposite pass 1 of a 1-site neck), the same knot r05 had.
  - v2: `_unknot` drops any inner-pass segment within 0.34 mm of other ink. Field knots 48 → 0.
  - v3: trimmed outline pieces under 1.5 mm are dropped (they read as debris ticks beside the coast). First seeds 3 and 13.
  - v4: A21. The `A` diagonals were hairlines because the kit's averaged-normal offset collapses at a sharp apex. A local `_title_glyph` splits a stroke at any turn > 120° before offsetting. Every other glyph is unchanged.
  - v5: closed outlines start at their lowest vertex (plot order only, no ink change). Seed-7 travel 0.525× → 0.499×, grey longest jump 208 → 105 mm. Final.

## Mandate responses
| id | mandate | status |
|---|---|---|
| A18 | grey fades to paper; 20 mm column counts strictly decrease from T≈1.3 (or x 180) to the edge; last column ≤ 3 marks and a ≥ 25 × 60 mm mark-free block; one fixed printed rule; A14 still holds | **FIXED: the ending. ARGUED: per-sample strictness.**<br>**Lever 1 worked, no fallback.** At the same cut 13, T_max was swept 1.8 → 3.2 (`census.py`, seeds 7/3/13). At NY 129, **2.30 is the smallest T_max** where the last 25 mm column holds ≤ 3 outlines and a ≥ 60 mm free run on all three seeds (2.20 fails seed 13 with 4). Sea + coast (field edge to coast mean): **49.4 / 48.7 / 60.6 mm**, above the ~45 mm floor, so the cut never moved.<br>**On the ink, seed 7:** last column (x 261.6–286.6, T 2.14–2.30) has **2 outlines**. Its longest mark-free vertical run, across the full 25 mm width, is **74.2 mm** (so there is a 25 × 74 block). Outline count per 20 mm column from T 1.3: **26, 20, 17, 15, 6, 3, 2, 2**; from x 182: **15, 6, 3, 2, 2**. It is strict except for the final tie.<br>Seeds 3 / 13: last column 1 / 2 marks, free run 106 / 77 mm. From x 182: s3 6, 10, 7, 3, 1 and s13 7, 5, 2, 0, 2.<br>**Why per-sample strictness is argued, like S7's per-row clause** (`ensemble_r07.py`, 40 independent chains of this geometry):<br>– the **expected** count per column from T 1.3 is 29.6, 21.6, 14.8, 9.7, 5.8, 4.1, 2.7, 2.1, strictly decreasing, with sd 4.2, 2.7, 4.1, 3.0, 2.2, 1.9, 1.6, 1.1;<br>– P(one configuration is strictly decreasing) is only **0.075** (from x 182: 0.10);<br>– the same test at r05's axis (0.70–1.80) fails at every cut 13–30: P_strict 0.00–0.25 (`ensemble.py`).<br>The attainable clauses hold in the ensemble: P(last ≤ 3) 0.85, P(free ≥ 60 mm) 0.90.<br>**A14 bands (count / mean sites, seed 7):** 1.15–1.35 **44 / 27.1**, 1.35–1.55 **33 / 19.5**, 1.55–1.80 **27 / 17.4**, new band 1.80–2.30 **10 / 13.7**. Strictly decreasing. s13 is strict too. s3 is strict in count (49 / 36 / 20 / 19); mean size is 26.9 / 17.75 / 18.05 / 15.05, so 1.55–1.80 is 0.3 site above 1.35–1.55. Ensemble mean size 26.9 / 20.1 / 17.5 / 15.8 is strict<br>The rule is printed: `BLANK   DISORDER FINER THAN 13 SITES` and `T OVER TC 0.70 TO 2.30` |
| A19 | the coast is where everything stops: 0 crossings; rules ≥ 0.8 mm short; no grey straddling; no 3-pass neck knots; never move the coast | **FIXED.** Every black and grey stroke is cut back to a keep-out of each crimson unit edge grown by 0.15 + 0.85 mm (exact interval subtraction on the rectilinear strokes; `_cut_away`). Measured on the gcode (`check.py`):<br>– crimson × black crossings **0**, crimson × grey **0**; r05 had 354 / 87 by the same counter, which counts touches on each of the 3 passes;<br>– minimum distance from black or grey ink to crimson ink **0.85 mm** on seeds 7, 3 and 13;<br>– 53 rule runs and 81 outline strokes trimmed on seed 7.<br>Knots: `_unknot` + the neck rule (on a 1-site neck, pass p survives only if 2p·0.35 + 0.35 ≤ pitch, so p ≤ 1). Result: **0** parallel pairs under 0.34 mm in the field; the minimum between different strokes is 0.35 mm, which is the pass gap. 41 neck + 22 knot segments dropped on seed 7.<br>The coast is untouched: 352 edges, 1 component, 0 dropped. No cluster is erased, though a few coast-side outlines are now open arcs, e.g. one 14-site outline keeps 10 % of its length |
| A20 | footer + ruler air, on the grid; shorten the field, not the type | **FIXED.** Field 137 → **129 rows** at r05's 1.178 mm pitch; type size unchanged, 5-line grid at 4.0 mm pitch.<br>– Field bottom y 36.40 to first cap line 31.00: **5.4 mm** bare.<br>– Last baseline 13.2: **3.2 mm** above the bottom margin.<br>– Tallest ruler label (red 1.00) top 197.2: **2.8 mm** under the top margin (field top lowered 189.0 → 188.4).<br>– Right column's left edge x **177.31** = the **1.60** tick exactly.<br>– `TC IS A PLACE`: **2.65 mm** clear above its cap (including the ±0.15 mm weight passes).<br>Middle column starts on the red 1.00 tick (x 83.64) |
| S9 | unpack FK; say weight peaks at Tc while count peaks past it, remeasured on the ink | **FIXED.**<br>– `FK  SPINS BONDED WITH PROB 1-EXP(-2J/T)` is on the hot column, line 2.<br>– `WEIGHT PEAKS AT TC   COUNT PEAKS PAST IT` is on the Tc column. The line is **computed**: it prints only if the drawn outlines' mean size peaks in the 1.00–1.15 band and their count peaks in a later band.<br>– Seed 7 by band (1.00–1.15 / 1.15–1.35 / 1.35–1.55 / 1.55–1.80 / 1.80–2.30), count **28 / 44 / 33 / 27 / 10**, mean sites **45.4 / 27.1 / 19.5 / 17.4 / 13.7**. s3: 30/49/36/20/19 · 32.5/26.9/17.8/18.1/15.1. s13: 24/43/30/18/7 · 31.3/28.0/21.0/18.1/16.6.<br>– Ensemble: P(count peaks past Tc) = P(weight peaks at Tc) = **1.00** |
| A2 | travel ≤ 0.6× draw on seed 7 with margin; no 248 mm tail jump; plot order + minutes per layer | **FIXED.**<br>– Seed 7 travel 6.17 m / draw 12.37 m = **0.499×**; seeds 3 / 13 0.509× / 0.537×.<br>– Longest in-layer jump: black 155 mm, crimson 158 mm (coast → ruler tick), grey 105 mm. r05 was 248.<br>– Two moves, since the pipeline re-orders by nearest neighbour and so a 2-opt inside the piece would not survive: (1) rules run serpentine; (2) closed outlines start at their lowest vertex.<br>No isolated dots: smallest outline 13 sites, and trimmed pieces < 1.5 mm are dropped. Order and minutes are in HANDOFF |
| A21 | `A` diagonals hairline in CRITICAL | **FIXED (free).** `_title_glyph` splits at a > 120° turn, so the diagonals carry 3 passes like the crossbar |
| S10 | seed-3 stray rule steps | **DEFERRED.** Seed 3 is not the plate. The r07 chain is new (NY 129, T 2.30) and s3's rule check was not re-run |
| A4 | bare hot side | **Returns, by physics.** The 1.80–2.30 band holds 10 outlines in 72 mm on seed 7 |
| A9 | ≥ 0.8 mm between distinct owners | **Holds, and improved.** Min centre distance between different owners (clusters, rules, coast ±0.15): **1.028 mm** on seeds 7, 3 and 13, 0 pairs < 0.8 (`check_a9.py`). r05 was 0.828 |
| A15 | ≥ 155 stroke ≥ 2.5× a 30–49 stroke | **Holds (geometry unchanged)** on the 376-site continent: 0.35 mm pass gap. The neck/knot rules only remove pass-2 pieces where they would have knotted |
| S1 | key names FK, rungs, what is not drawn | **Holds.** `GREY 13-29` (inked grey) / `1 PASS 30-49` / `2 PASSES 50-154` / `3 PASSES 155+`; `BLANK DISORDER FINER THAN 13 SITES`; FK now unpacked |
| S2 | top rung populated | **Holds on the plate, weaker in the ensemble.** Seed 7 has a 376-site 3-pass continent; seeds 3 and 13 have none (largest 128 / 93). P(≥ 1 cluster ≥ 155) is **0.40** in this geometry against 0.81 in r05's: the 1.00–1.15 band is now 20 columns wide instead of 29, with 129 rows instead of 137. The printed key is true on the plate |
| S3 / S7 / S8 | printed check provable from ink; coldest band ruled; stranger lines | **Hold, remeasured.** `UNDER 0.80 TC   AS DRAWN 0.984` / `ONSAGER M 0.969`. 0.9839 is the drawn rule length ÷ (13 columns × 43 rows), equal to the held fraction on those rows (0.98390). Ensemble for this geometry: 0.9691 ± 0.0077, so seed 7 sits at +1.9 σ (s3 0.977, s13 0.982). Onsager over the same 13 columns is 0.9694. The coast (min 0.95 Tc) never reaches the < 0.80 band, so no rule there is trimmed |
| A6 | canon / lineage / flat | holds (HANDOFF) |
| A10, A11, A12, A16, A17 | — | hold. Spine cap 18 mm, 3 passes, x 15. Closed hulls. One coast (1 component, seam crossed once). Line gap 2.2 mm bare. Fjord logic unchanged |
| A1, A3, A7 | — | hold |
| A5, A13, A14, S4, S5, S6, A22–A24, S11–S13 | — | dropped in LEDGER, not reopened. Nothing from r06 is used |

## What changed from parent
- **The sheet now has an ending.** The composition is r05's: spine, ruled sea, crimson coast, black continent, grey islands. What changed is the thermometer. It runs on to 2.30 Tc, so the grey islands keep shrinking and thinning for another 70 mm until heat is finer than 13 sites and the paper is bare. The fade is physics at the one printed cut. Nothing is thinned by hand.
- **The coast became a wall.** Everything black or grey now stops 0.85 mm short of the crimson, so the coast reads as a line nothing crosses. At arm's length the rules end in a clean ragged margin beside the red.
- **The footer is a 5-line grid under a shorter field.** Three columns hang from three marks: the spine axis, the red 1.00 tick and the 1.60 tick. The field lost 8 rows so that type size never changed.
- **The type column moved with Tc.** The red tick is now at x 83.6, so the sea column holds only what the rules mean. The run metadata (lattice, seed, T range, FK, wrap) moved to the hot column.
- Unchanged: sampler, FK draw, rung ladder, pass gap, 3-pass coast at ±0.15, rules on lattice lines every 3rd row, 1.178 mm pitch, pens and their meanings.

## Measurements / computations
- **T_max search, cut 13** (`census.py`; last-column outlines and free run in mm, seeds 7 / 3 / 13, NY 129):

  | T_max | last-column outlines | free run (mm) | verdict |
  |---|---|---|---|
  | 2.0 | 3 / 5 / 7 | 54 / 52 / 41 | fail |
  | 2.1 | 4 / 5 / 2 | — | fail |
  | 2.2 | 3 / 3 / 4 | 94 / 70 / 67 | fail |
  | **2.3** | **2 / 1 / 2** | **138 / 147 / 75** (lattice) | **pass** |
  | 2.4 | 2 / 1 / 1 | — | pass |
  | 2.5 | 3 / 1 / 2 | — | pass |

  Sea to coast mean at 2.3: 49.4 / 48.7 / 60.6 mm. At 2.5 it is 42.7–50.8 mm, and at 2.8 it is 40.8–43.3 mm.
- **Fallback census for the record** (0.70–1.80, cuts 13–30, NY 129/132/137, `census_cut.py` + `ensemble.py`, 32 chains):
  - no cut gives per-sample strictness better than P 0.25;
  - cut 24 would have been needed for ≤ 3 marks on all three seeds;
  - at cut 24 the band counts at 1.00–1.15 and 1.15–1.35 tie on seed 7 (21 / 21), which would have falsified the S9 line.
- **Physics (seed 7):**
  - coast mean **1.016 Tc** (σ 0.037, range 0.949–1.123), 352 edges, 1 component, held cluster 18.2 % of the lattice;
  - energy RMS against Onsager 0.011 per band; Wolff frozen 0.19;
  - seeds 3 / 13: coast 1.012 / 1.088.
- **Drawn outlines per rung:**

  | seed | grey 13–29 | 30–49 | 50–154 | ≥ 155 |
  |---|---|---|---|---|
  | 7 | 115 | 22 | 7 | 1 (376) |
  | 3 | 135 | 16 | 10 | 0 |
  | 13 | 97 | 18 | 10 | 0 |

- **Black share by band** (seed 7, 1.00–1.15 → 1.80–2.30): 0.36 / 0.30 / 0.18 / 0.04 / 0.00.
- **Ensemble** (40 chains, this geometry): column means as in A18 · P(last ≤ 3) 0.85 · P(free ≥ 60) 0.90 · held 0.70–0.80 **0.9691 ± 0.0077** · P(top rung) 0.40 · mean band count 24.4 / 48.4 / 32.2 / 20.3 / 12.5 · mean size 38.0 / 26.9 / 20.1 / 17.5 / 15.8.

## Plot budget
- **Seed 7 totals:** draw **12.37 m**, travel **6.17 m (0.499×)**, 12,097 commands, 1,128 pen lifts. Bounds X 0–286.6, Y 0–197.2 (A4 landscape). Score grade A; dominant issue efficiency (0.73, r05 0.66).
- Against r05: draw −4.2 m, travel −3.65 m, lifts −23.

  | order | pen | draw | pen-downs | travel | est. time |
  |---|---|---|---|---|---|
  | 1 | black | 8.05 m | 947 | 3.87 m | ≈ 47 min |
  | 2 | crimson | 1.27 m | 14 | 0.49 m | ≈ 3 min |
  | 3 | grey | 3.05 m | 167 | 1.81 m | ≈ 12 min |

  Time = draw at F600 + travel at F2000 + 2 s per lift. Total ≈ 62 min.
- No line is shared between layers, and black/grey never touch crimson, so the layer order is free and every stroke boundary is a batch point.

## Self-critique (rubric)
1. **Hierarchy — 8.** CRITICAL, the red coast and the black continent lead. Black islands, grey islands and paper follow in that order. The fade now ends.
2. **Grid & alignment — 8.** Three footer columns sit on the spine axis, the red tick and the 1.60 tick. CRITICAL spans the field exactly, and the footer air is measured.
3. **Tension & asymmetry — 8.** Mass is hard left and dissolves over two thirds of the sheet. The coast is the working vertical at ~⅕ width.
4. **Negative space — 8.** The right quarter is paper that the gradient reached, with a few last grey islands at 2.0–2.3 Tc as punctuation.
5. **Craft for pen — 8.** 0 coast crossings, 0 knots, A9 1.03 mm, travel 0.50×. Black still needs 947 lifts (~31 of its 47 min).
6. **Concept legibility — 8.** Order → coast → largest structure at Tc → heat finer than the cut → paper, and the colophon now says why the densest grey is not the critical place.
7. **Depth — 5.** Declared flat.

**Single worst thing:** the ruled sea is now narrower (x 37–85, about 49 mm to the coast mean, from r05's 68), so the ordered phase has less body next to the long hot side. A second, smaller one: coast-side outlines are now open arcs, and one 14-site outline keeps only 2.4 mm of wall. That is the honest cost of A19. Science risk: the top rung is populated on the plate but only in 40 % of configurations of this geometry (S2).

## Engine requests
- Carried from r05: `cell_hull` / `inward_passes` with corner-reach and neck clearance built in. This round added a neck rule, `_unknot` and `_cut_away` locally.
- `reorder_by_color` could honour stroke reversal (open strokes) and closed-loop start rotation, or accept a piece-supplied order. Today the piece can only steer the nearest-neighbour search through stroke direction and loop start points.
- `giant_type`: the averaged-normal offset collapses at sharp apices (the `A` of any weighted title). `_title_glyph` in this piece is the fix: split at a > 120° turn.
