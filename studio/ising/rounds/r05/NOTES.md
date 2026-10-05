# ising r05 — iterate (r04 + the hot half drawn as heat) · parent: r04 · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r05/piece.py \
  --fn ising_cooling_strip_r05 --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson,gray --out gallery/studio/ising/trials/pp_ising_r05_iterate_v8.png
```
- Final: `gallery/studio/ising/trials/pp_ising_r05_iterate_v8.png` / `.gcode`, seed 7 (the same chain as r02/r04).
- Seed sweep: `gallery/studio/ising/trials/pp_ising_r05_iterate_v8_s3.png`, `gallery/studio/ising/current/pp_ising_r05_iterate_v8_s13.png`.
- Iterations:
  - v1: cut 8, the smallest cut passing SYNTH's (a)–(c). The hot half became a uniform carpet of rings (rejected).
  - v2: cut 13, inward rungs at a 0.31 mm pass gap, title column and type strip.
  - v3/v4: CRITICAL tracked out to span the field exactly; type regrouped into three blocks by meaning.
  - v5: pass gap 0.35 mm, so the 3-pass band measures 2.67× a 1-pass stroke. Its worst thing: the islands thinned with T but did not visibly shrink, and the 13–49 rung was one undifferentiated black.
  - v6: re-render of v5, geometry byte-identical (the session was relaunched and this check confirms it).
  - v7: **the hairline rung gets its own grey pen.** 13–29 sites become 1 grey pass. The r04 black rungs 30–49 / 50–154 / ≥ 155 at 1/2/3 passes are restored exactly as SYNTH's "Preserve" asked. The key's `GREY 13-29` is inked in grey.
  - v8: inner passes are dropped on any edge where a corner miter reaches within 0.8 mm of another owner's parallel line (0.95 mm for the coast). This fixes an A9 break found on seeds 3 and 13 (0.33 mm to the coast). Seed 7 is unchanged: 0 edges cut.

## Mandate responses
| id | mandate | status |
|---|---|---|
| S7 | coldest band gets its sea back; rows 0.70–0.80 ≥ 0.95; 0.800–0.825 ≈ 0.95 | **FIXED (title and type off the data), ARGUED per-row.** Nothing overlays the field. Every ruled row in 0.70–0.80 carries exactly its held cells in ink, and that ink is 100 % black rules: grey and hull ink on those rule lines both measure 0.0000 on seeds 7/3/13.<br>Mean over 46 rows is **0.977** against Onsager 0.969, and 0.800–0.825 reads **0.958**. 16 of 46 rows are under 0.95 (min 0.844). Those rows have 2–3 of the band's 21 cells unheld (minority droplets), which is true data: one missing cell already gives 0.952.<br>The letter-shaped halo was not used. Rotated stems run parallel to the rules and cut ~18 of a 25 mm row, so a halo cannot pass ≥ 0.95. The science critic's other option was taken: the title left the data |
| A14 | hot half visibly hot: count and mean size strictly fall across 1.15–1.35 / 1.35–1.55 / 1.55–1.80; most 20×20 cells in the last band hold a mark and stay ≥ 50 % bare; no dots | **FIXED, and now it reads in tone as well as count.**<br>Hull count / mean sites, band by band: seed 7 **76/50/31**, 24.6/19.7/17.4; seed 3 71/51/35, 27.4/20.1/16.9; seed 13 74/39/37, 26.2/21.0/18.5.<br>Share of hulls drawn black (≥ 30 sites) across 1.00–1.15 / 1.15–1.35 / 1.35–1.55 / 1.55–1.80: seed 7 **0.49 / 0.18 / 0.12 / 0.03**; seed 3 0.46/0.27/0.12/0.03; seed 13 0.32/0.30/0.08/0.03. The hot edge is grey islands on cream.<br>Last band: 24/24 cells hold ink, max ink 10.9 %. Smallest hull is 13 sites, ≥ 4.7 mm across |
| A2 | no isolated dot marks; travel ≤ 0.6 × draw | **FIXED on seed 7, narrowly.** The crop holds only closed hulls ≥ 13 sites (≥ 4.7 mm). Travel is 9.82 m against 16.58 m draw, **0.592×** (v5 was 0.53×). The third pen costs ~1.06 m of travel.<br>**Seeds 3 and 13 measure 0.630× and 0.631×, over the bar.** Ordering is the pipeline's per-colour nearest neighbour; see Engine requests |
| A4 | bare hot side (superseded by A14) | superseded, see A14 |
| A9 | ≥ 0.8 mm clear between distinct parallel strokes, no solid cell > 2×2 mm | **FIXED on all three seeds (v8).** Checked over every axis-parallel pair from different owners (hulls, rules, coast ±0.15) overlapping by > 0.3 mm. Minimum centre distance is **0.828 mm** on seeds 7, 3 and 13, one same-rung corner each; the next is 1.03 mm.<br>v7 had 0.33 mm (seed 3) and 0.68 mm (seed 13) coast–hull pairs, where a 2/3-pass corner miter reached past its edge's cell. v8 drops the inner pass on those edges: 0 / 5 / 1 edges on seeds 7 / 3 / 13 |
| A15 | ≥ 155-site stroke ≥ 2.5× a 30–49-site stroke, 3-pass solid, A9 holds | **FIXED (unchanged from v5).** In the PNG, the contiguous dark run across the 3-pass band is 8.0 px against 3.0 px for 1 pass: **2.67×**. Geometric width is 1.11 mm against 0.41 mm. The 30–49 rung is 1 black pass again, as in r04 |
| A16 | ≥ 1.2 mm bare above/below every colophon line; `TC IS A PLACE` own line, cap ≥ 5 mm | **FIXED.** Type sits in a strip under the field, 3.6 mm line pitch, so ink-to-ink bare is **1.4 mm**. `TC IS A PLACE` is a 5.2 mm cap on its own baseline, starting on the Tc column (x 104.9) |
| A17 | upper-left rule pocket, verify | **ARGUED: true data.** In r04's pocket (cols 36–65, rows 3–18), of 480 cells: 345 held, 104 outside (a coast-connected fjord the crimson hull wraps), and 31 in droplets of 1–4 sites |
| S3 | printed check the ink proves; band and row set stated | **FIXED.** The sheet prints `UNDER 0.80 TC  AS DRAWN 0.977  ONSAGER M 0.969` under `RULED EVERY 3RD ROW`. The value is drawn rule coverage over the 46 drawn rows at T/Tc < 0.80, equal to the held fraction there (0.97712) |
| S8 | `TC 2.269185 ONSAGER 1944 EXACT`; rule density = M; hot blank named | **FIXED.** On the sheet: `TC 2.269185   ONSAGER 1944   EXACT`, `RULE DENSITY IS THE MAGNETISATION M`, `BLANK   DISORDER FINER THAN 13 SITES` |
| S1 | key names FK, rung ranges, what is not drawn | **FIXED (updated for the grey rung).** `OUTLINED   FREE FK CLUSTERS BY SITE COUNT` / `GREY 13-29   1 PASS 30-49   2 PASSES 50-154   3 PASSES 155+`, with `GREY 13-29` inked in the grey pen / `BLANK   DISORDER FINER THAN 13 SITES` |
| S2 | top rung populated + uniform | **FIXED (holds).** One ≥ 155 cluster on each of seeds 7/3/13 (441 / 170 / 403). Shared edges take the heavier rung, so a grey hull's edge shared with a black hull is drawn black |
| A6 | canon / lineage / flat | holds (HANDOFF) |
| A10 | CRITICAL cap ≥ 18, 2–3 passes, x = 15, no stubs | holds. Cap 18.0 mm, 3 passes, cap line at x = 15, own column, no rule stubs |
| A11, A12 | closed hulls; one crimson coast | hold. 461 coast edges, 1 component, 0 dropped, seam crossed once. Seeds 3 and 13 are also 1 component |
| A1, A3, A7 | — | hold |
| A5, A13, S4, S5, S6 | — | dropped in LEDGER, not reopened |

## What changed from parent
- **The hot half is heat, in three registers at one fixed cut.**
  1. *Count:* every free FK droplet of ≥ 13 sites is drawn (203 hulls, r04 had 42), thinning 76 → 50 → 31 across the hot bands.
  2. *Weight:* 3-pass continent → 2-pass → 1-pass black.
  3. *Tone:* the hairline rung (13–29 sites) is a grey pen.

  The sheet now reads: ruled order → crimson coast → one heavy black continent → a black-and-grey mosaic at 1.05–1.3 Tc → grey islands thinning to cream at 1.8. The grey also decodes the mosaic: the big clusters now read as islands against the small ones. In v5 they were one maze.
- **Why a pen and not a mark.** A single nib has no stroke finer than one pass, so SYNTH's "hairline rung below the current 1-pass rung" needs a lighter ink. Dashes (duty) would be a new mark, and the SYNTH banned new small-rung marks. They would also add ~1,500 pen lifts. The curator note lifts the pen cap: "one clean layer per meaningful pen". Grey means one thing: FK clusters of 13–29 sites.
- **Cut choice (argued, unchanged since v2).** SYNTH's smallest-passing cut is 8, but at cut 8 the hot half is an even carpet (enclosed area falls only 2.4×). Cut 13 is the smallest cut that passes (a)–(c) *and* lets the hot-band enclosed area fall ≥ 3.5× on all three seeds. Cut 12 fails seed 13 at 3.2×; cuts 14 and 16 fail strict count on seed 13.
- **Weight grows inward.** Pass k is the exact rectilinear miter offset k × 0.35 mm into the droplet. An inner pass is dropped on an edge if the line one site in belongs to someone else (r05 v2). From v8 it is also dropped if the corner miter's reach crosses 0.8 mm of another owner's parallel line.
- **The title and type left the data** (from v2). The display pitch is 1.178 mm; the simulated lattice, sampler, chain, FK draw and seam roll (111) are untouched.
- Unchanged: the coast (3 crimson passes at ±0.15 mm), rules on lattice lines every 3rd row, the thermometer.

## Measurements / computations (seed 7 unless stated)
- **Physics.**
  - Coast: mean 1.031 Tc (σ 0.063), 461 edges, 1 component; held cluster 26.1 % of the lattice.
  - Energy RMS vs Onsager: 0.013 per band. Wolff frozen fraction: 0.27.
  - Seeds 3 / 13: coast 1.032 / 1.038 Tc; printed density 0.976 / 0.965 against Onsager 0.969.
- **Drawn droplets per rung.**

  | seed | grey 13–29 | 1 pass 30–49 | 2 passes 50–154 | 3 passes ≥ 155 |
  |---|---|---|---|---|
  | 7 | 161 | 25 | 16 | 1 (441) |
  | 3 | 156 | 29 | 15 | 1 |
  | 13 | 156 | 27 | 13 | 1 |

- **Black share by band** (seed 7):

  | band | hulls | black | share |
  |---|---|---|---|
  | 1.00–1.15 | 39 | 19 | 0.49 |
  | 1.15–1.35 | 76 | 14 | 0.18 |
  | 1.35–1.55 | 50 | 6 | 0.12 |
  | 1.55–1.80 | 31 | 1 | 0.03 |

- **Hot-band census by cut** (count per band on seeds 7 / 3 / 13):
  - cut 8: 145/125/113 · 142/130/107 · 138/117/114
  - cut 12: 88/60/42 · 81/66/43 · 81/50/48
  - cut 13: 76/50/31 · 71/51/35 · 74/39/37
  - cut 15: 62/35/18 · 63/35/22 · 60/30/29
- **S7 on the ink.** 46 rows, mean 0.9765, min 0.844; the held fraction on the same rows is 0.97712. Band 0.800–0.825 reads 0.958. The rule-line ink under 0.80 Tc is 100 % black rules.
- **A9** (centre-to-centre minimum between distinct owners, next value after it): seed 7 0.828 (then 1.03); seed 3 0.828; seed 13 0.828. Corner edges cut: 0 / 5 / 1.
- **A15:** 1 pass 3.0 px, 3 passes 8.0 px → 2.67×.

## Plot budget
- **Seed 7 totals:** draw **16.58 m**, travel **9.82 m (0.59×)**, 13,869 commands, 1,151 pen lifts. Seeds 3 / 13: 16.38 / 16.01 m draw, 0.63× travel on both.
- **3 pens, 2 swaps, in file order:**

  | order | pen | draw | pen-downs | travel | est. time |
  |---|---|---|---|---|---|
  | 1 | black: rules, black hulls, cold wall, thermometer, CRITICAL, type | 10.36 m | 895 | ~7.1 m | ≈ 51 min |
  | 2 | crimson: coast, 1.00 tick + label | 1.65 m | 11 | — | ≈ 3 min |
  | 3 | grey: 13–29 hulls, `GREY 13-29` | 4.56 m | 245 | ~2.4 m | ≈ 17 min |

  Times assume Leo at F600 draw, F2000 travel and ~2 s per lift.
- No line is shared between layers (shared edges belong to one owner), so the layer order is free.
- Every stroke is a closed hull, an inward pass or a straight rule, so any stroke boundary is a safe batch point.
- Grey pen: a grey fineliner of the same nib as the black (≈ 0.3–0.4 mm). The rung is a tone step, not a width step.

## Self-critique (rubric)
1. Hierarchy — 8. CRITICAL and the crimson coast lead. Next come the 3-pass continent, then black islands, then the grey haze, then the type tiers. Grey is a genuine third value; before it, every island shouted at the same volume.
2. Grid & alignment — 8. One left axis (x = 15). The title spans exactly the field height; `TC IS A PLACE` hangs on the Tc column; the key is flush to the field's right edge.
3. Tension & asymmetry — 8. The mass sits left of centre and dissolves right; the coast is the working vertical at ⅓ width.
4. Negative space — 8. The bare paper is shaped by the gradient, and the grey lets the hot quarter read as paper with marks, not marks on paper.
5. Craft for pen — 7. Clearance holds on three seeds and every layer is batchable. Costs: a third pen and swap, and travel at 0.59× (0.63× on the other seeds). Black still carries 895 lifts.
6. Concept legibility — 8. Order → coast → largest clusters at Tc → greying fine disorder, with the key self-inked. A stranger gets M, Tc exact, and what the blank means.
7. Depth — 5. Declared flat.

**Single worst thing:** plot economy. Travel is 0.59× on seed 7 but 0.63× on seeds 3 and 13, so A2's travel clause holds only on the chosen seed. The black layer still needs ~51 min on Leo, mostly pen lifts. Second: a handful of black 30–49 hulls far out at 1.4–1.7 Tc (true data) read as loud punctuation in the grey field.

## Deviations from SYNTH (flagged)
- **2 pens → 3 pens.** SYNTH preserved "2 pens, 1 swap". The curator note ("no pen cap, one clean layer per meaningful pen") overrides it, and the grey pen is the only way to draw SYNTH's own "hairline rung below the 1-pass rung" with one nib width.
- **Display pitch 1.178 mm** instead of 1.3 mm. The simulated lattice is unchanged; this is what let the title and type leave the data (S7).
- **Letter-shaped halo replaced by moving the title off the field.** The calculation is in the S7 row.
- **Cut 13, not 8.** See "What changed".

## Engine requests
- `cell_hull(mask, exterior="4", periodic_y=True)` returning *directed* loops (interior side known) plus `inward_passes(loop, n, gap, clear=)` with the corner-reach clearance test built in. This round wrote `droplet_loops` / `_trace_loops` / `_offset_loop` / `_crowds` locally. Five rounds have re-implemented dual-lattice hulls.
- A 2-opt (or Or-opt) pass after `reorder_by_color`'s per-colour nearest neighbour. On 900-stroke layers the NN tail jumps (longest travel 248 mm) are what hold travel at 0.59–0.63×.
