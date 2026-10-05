# millennium-poincare r03 — iterate (abstract thesis kept) · parent: r02 · 2026-09-29

Lineage: **Vera Molnár, *(Dés)Ordres* (1974)**, unchanged. Canon 6 on cream, with red only for
the events. The flatness stays declared: this is the meridian section.

## Render

```
.venv/bin/python -W ignore scripts/render_candidate.py studio/millennium-poincare/rounds/r03/piece.py \
  --fn poincare_two_nests --seed 7 --paper a3 --margin 15 \
  --palette black,black,black,crimson --out gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.png
.venv/bin/python studio/millennium-poincare/rounds/r03/render_truewidth.py \
  gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.gcode gallery/studio/millennium_poincare/current/pp_millennium_poincare_iterate_v3_phys10.png 0 0 297 420 10
.venv/bin/python studio/millennium-poincare/rounds/r03/audit.py gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.gcode
```

- **Final PNG:** `gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.png`
- **True-width preview:** `gallery/studio/millennium_poincare/current/pp_millennium_poincare_iterate_v3_phys10.png`, at 10 px/mm. Judge from this one.
  - The 5 px/mm `_v3_phys.png` rounds both 0.3 and 0.5 to 2 px, so the keyline looks thin there.
- **GCODE:** `gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.gcode`
- **Seed 7.** Seed 11 (`_v4`) gives byte-identical gcode apart from the header lines (diff checked). The piece uses no randomness.
- **Data:** `snapshots.npz` is byte-identical to r02's (`cmp`). Nothing was re-solved.
- **Earlier self-rounds:** `_v1` and `_v2`.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | keyline alone: own black 0.5 layer, single pass, ≥ 2.5 mm moat, caption clause | **FIXED.** Layer 1 (black 0.5) draws the keyline once, as 2 strokes of 481.2 and 235.3 mm. They split only at the red cut (see A3). The moat is two engine `Occupancy` grids fed the keyline: lines pause within 3.05 mm and resume at 3.4 mm (hysteresis). Nothing is respaced. **Gcode test:** min distance from any layer-0 point to the keyline centre-line is **3.049 mm**, with **0 points < 2.5 mm**. The moat swallows the last halo line (t_s−0.01, 44 mm survives, as two 22 mm stubs flanking the cut, where its 3.49 mm waist step clears the moat) and the first A rings (A1 21 mm = its cap tip under the circle, A2 36.7 mm). This is the declared pause, not a drop: every line still exists in the solver set, and ring counts stay 33 + 6. The caption clause "OUTSIDE THE HEAVY LINE: BEFORE THE CUT · INSIDE: AFTER" is its own footer paragraph. |
| A3 | red off black at the waist, radius exactly h, keyline yields symmetrically | **FIXED.** The caps are unchanged: centre-line radius h = 0.11971 u = 7.422 mm about the cut. The keyline pauses wherever its centre-line runs within 1.32 mm of the cap circle (0.8 clear + 0.25 red half-nib + 0.25 key half-nib + 0.02). **Pause per flank:** 8.70 mm of arc (8.69 mm chord) on each side, midpoints (158.3, 203.3) and (171.4, 196.2). The two flanks are symmetric to 10⁻¹³ mm. **Gcode test, true nib widths:** caps→keyline min edge-to-edge **0.829 mm**, caps→line layer **3.088 mm**, all red→type **5.34 mm**. 0 red samples < 0.8 mm from any black. |
| A2 | no rim stutter; zero line strokes < 15 mm except whole rings | **FIXED.** The merge now has four clauses (see `merge()`): MOAT, FLOOR (0.85 / 1.2 mm hysteresis as r02), ARC and TWIN. **ARC:** once a ring has paused, a drawn stretch < 15 mm is a stutter and is dropped, so the ring stays paused over the whole crowded arc. Whole rings are exempt. 9 stretches were dropped. **TWIN:** a stretch < 30 mm running within 1.5 mm of kept ink over > 60 % of its length is that line's twin. Exactly one stretch matches: t_s−0.05's last 16.2 mm, running at 0.85–1.2 mm beside t = 0 on B's right rim (236, 246). It was already 90 % merged in r02, so that line now merges fully into t = 0. **Gcode:** layer-0 strokes went 101 → **63**. **Shortest stroke 20.7 mm; 0 strokes < 15 mm.** In the crops of A's far pole, A's lower-right and B's crown, every ring either runs continuous or ends once, cleanly, in a staggered fan against the moat. None re-enters. |
| S1 | footer: relative race, off-grid start line, clause | **FIXED.** The numbers are computed at render time from `snapshots.npz` (`race_numbers()`): neck 0.31433 → 0.11971 (**−61.9 %**), small lobe 0.67650 → 0.47091 (**−30.4 %**), large lobe 1.41389 → 1.24469 (**−12.0 %**), t_s 0.054647. The footer reads "NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 % · CUT AND CAPPED AT t = 0.055" and "…COUNTED FROM THE CUT. OUTERMOST LINE: t = 0 (OFF THE GRID)". I did not add the optional radius bars: the footer is already seven paragraphs, and bars would be a second ruler competing with the nest. No line is respaced. |
| A4 | plate-job minutes, pen order, series caption | **FIXED.** Pen order is lines 0.3 → keyline 0.5 → type 0.3 → red 0.5. Minutes come from `plot plate … --dry-run` (see Plot budget). The series caption, "MILLENNIUM PRIZE PROBLEMS 6 / 7" / "CLAY MATHEMATICS INSTITUTE, 2000", sits at 2.2 mm caps on the x = 205 column. Its two baselines are registered on the statement's two baselines, and the tracking (0.383 mm) is solved so the longer line ends on x = 282. |
| A5 | extinction dots Ø 2.4–3 mm if B keeps ≥ 5 mm bare | **DEFERRED (argued).** At Ø 1.9, B's bare disc is 5.02 mm. At Ø 2.4 it would be 4.77 mm, which breaks the stated condition. Dots stay Ø 1.9. |
| A6 / A7 / S2 / S3 | r01-only (shell, lift, CSF caption, shell caption) | Dropped in LEDGER for the abstract line. Not applicable: no shell, no CSF loop, and the body is where r02 put it. |
| — | Dossier corrections (R_min 0.2167, lie #4 / §2(a) relative only, enc §4 "lobe halo merges" false) | The sheet follows the corrected reading. It states the race as **relative** percentages, draws the true absolute lobe loss (10.5 mm), and claims no lobe-halo merge. The only merges are at the poles, plus the one declared TWIN (t_s−0.05 into t = 0). |

## What changed from parent

- **The heavy instant is the spine.** r02 was one family of 46 equal lines. r03 has three strata:
  - the past halo outside;
  - one heavy 0.5 dumbbell outline, alone in a ≥ 3 mm bare channel on both sides;
  - the two dying nests inside.

  The moat is what makes the weight read: at 1 m the outline separates from both families as a single line with paper on either side.
- **Surgery happens in the ink.** At the waist the heavy line stops 8.7 mm short on each flank, and the red caps take its place. The keyline's two strokes are "before" the cut on each side. They are joined only by the red.
- **The rims are resolved as fans, not dashes.** A paused ring never comes back on the same crowded arc. The result is that rings approaching the keyline end in staggered, feathered terminations (A's far pole, A's right flank), which read as hidden-line cards landing.
- **Type.**
  - The footer gains the before/after clause, the off-grid start line and the relative race.
  - The title band gains the series caption on the right column.
- **Unchanged:**
  - flow data;
  - 62 mm/u, 62° axis, cut (165, 200);
  - both type columns, the quiet zone and the stamp;
  - red caps at h, dots Ø 1.9;
  - time-occlusion and hysteresis.

## Measurements / computations

- **Snapshots.** `snapshots.npz` is identical to r02's. Solver numbers carried over: t_s = 0.054647, h = 0.119710, T_A 0.387343, T_B 0.117140.
- **Ring survival.** All 33 A and 6 B rings are present as ink. A first TWIN variant with no length cap would have swallowed whole rings A10, A12 and A14, which run at ≈ 1.5 mm on the rim. I rejected it and capped TWIN at 30 mm. Final drawn length per line, in mm (fragment count in brackets):
  - start 511 (2) · t_s−0.05 0 (merged into t = 0) · −0.04 496 (2) · −0.03 523 (2) · −0.02 492 (2) · −0.01 44 (2, moat) · key 734;
  - A1 21 (1) · A2 37 (1) · A3 137 (3) · A4 179 (3) · A5 215 (3) · A6 258 (3) · A7 265 (4) · A8 244 (3) · A9–A33 one stroke each (296 → 40);
  - B1 87 (2) · B2–B6 one stroke each (181 · 152 · 123 · 90 · 39).

  A7's shortest piece is a 20.7 mm stretch on A's right flank at (166–170, 95–116). It lies between two moat pauses and outside the named rim boxes. It is the shortest stroke on the layer.
- **Floor.** Min gap between different layer-0 strokes is **0.850 mm**; 0 samples < 0.8.
- **Cut.** Ø / A width 0.0962. Bare paper from the red ink edge to the nearest line-layer ink is 3.09 mm. The interior is bare.
- **Dots.** Bare disc A 5.33 mm, B 5.02 mm.
- **Text.** The nearest text box to any line is 14.7 mm. The ink bbox is x 30.1–239.9, y 36.9–296.8.

## Plot budget

`plot plate gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.gcode --layers 0,1,2,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run` (feed ≤ 500, dwell ≥ 1 s, bounds ok):

| order | layer | pen | strokes | draw (audit) | plate-job min |
|---|---|---|---|---|---|
| 1 | 0 lines | black 0.3 | 63 | 9.97 m | **~23** |
| 2 | 1 keyline | black 0.5 | 2 | 0.72 m | **~2** |
| 3 | 2 type | black 0.3 (same pen as layer 0) | 1 190 | 5.49 m | **~53** |
| 4 | 3 red | red 0.5 | 18 | 0.26 m | **~2** |
| | total | 3 physical pens, 4 swap waits | 1 273 | 16.44 m draw, 6.55 m travel | **ETA ~85 min** (incl. 90 s per swap) |

The dry run issued 52 300 commands and 45 876 inked segments. The mandated order costs a return to the 0.3 black after the 0.5. Plotting type before the keyline would save one swap (about 1.5 min). I kept the stated order.

## Self-critique (seven rubric dimensions)

1. **Hierarchy 8.** The nest is first and the heavy outline second. The red cut sits at the hinge.
   The extinction dots are still small at 3 m.
2. **Grid & alignment 8.** Two text columns, x = 15 and x = 205. The series caption registers on the
   statement's baselines.
3. **Tension 8.** Unchanged diagonal. The bare upper-left holds.
4. **Negative space 8.** The moat adds a continuous cream channel around the whole form. The
   rim terminations are now chosen absence, not residue.
5. **Craft 8.** Floor 0.85 mm, moat 3.05 mm, red clearance 0.829 mm, no stroke < 20.7 mm, one keyline
   pass. Type is 62 % of plot time (1 190 lifts).
6. **Concept 8.** The 3 m read is now "outside, one heavy instant, two dying spheres inside",
   stated on the sheet. The waist shows surgery literally: the heavy line gives way to red.
7. **Depth 6.** Still flat by declaration. The occlusion fans at the rims read more as landing cards
   than in r02, but it is not relief.

**Single worst thing:** the waist carries four orphan marks around the red circle:
- the two 22 mm stubs of t_s−0.01 outside the keyline;
- A1's ∩ cap tip and B1's ∪ cap tip inside it.

Each one is honest: those are the only stretches where those lines clear the moat. But together they make a small busy asterisk around the event, where a bare stage would read cleaner. The only way to remove them is to drop Δt lines, which is forbidden, so they stay.

## Engine requests

- The r02 requests stand: proportional-glyph offset in `_stroke_text`, a vectorised `Polygon.inside_intervals`, and `Occupancy(resume_sep=)` hysteresis.
- New: `Scene3D.lines(mode="pause_resume")` could take `min_run=` (drop post-pause stretches shorter than N mm) and `keep_out=` (a sacred line's moat). This piece emulates both with extra `Occupancy` grids.
