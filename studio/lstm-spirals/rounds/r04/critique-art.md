# Art critique — lstm-spirals r04 · canon: undeclared (no `canon:` line; lineage Land Art — Smithson, *Spiral Jetty* / *A Sedimentation of the Mind*; declared flat) · 2026-09-29
render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png (gcode beside it; a4 portrait; pens 0 crimson 0.5 / 1 black 0.5 / 2 black 0.3)

Measured from the gcode (re-rendered at physical widths, 16 px/mm): the red c_t line is one chain (14 plot chunks meeting end to end, eye (78.4, 48.9) → end (122.6, 254.6)), with a minimum non-local spacing of 1.04 mm. Comet-to-comet minimum is 0.83 mm, with 84 samples under 1.0 mm. All 37 proverb glyphs sit exactly 1.2 mm from their comet. The title spans y 20.57–276.72, which is exactly the red line's y-extent, and its right edge is at x = 199.4.

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 8 | One dominant object: the red-bound figure-8. The black swirl is the loudest ink inside it and the red coil clearly second. The spine title is the third read, and the proverb and colophon reward 30 cm. There is a real 3:1 between the figure and everything else. |
| 2 grid & alignment | 7 | Strong lock: the title's top and bottom are exactly the red line's extremes, and its baseline sits on the right margin. The colophon floats: its left edge (x≈152) and its top (y≈150) land on no line of the figure or the title. The proverb's word gaps come from character timing and read as uneven tracking ("B E T T E R" is tight, " T H A N" is loose, "T H E" at the waist is cramped). |
| 3 tension & asymmetry | 6 | The figure is pushed left (11.7 mm to the left margin, 53 mm to the title), which is good. But the figure itself is a mirror-stacked 8: both eyes on one vertical (x≈78), both lobes near-symmetric about it, and the waist is centred. All the energy is the swirl's rotation. There is no diagonal, and the composition is "object + spine title" poster layout. |
| 4 negative space | 7 | The waist void (y 110–140) is shaped and is the plate's best silence. The ring between the lower coil and the three outer wraps is composed. The right band (x 135–185, y 20–277) is the gap between figure and title rather than a designed field, and the colophon sits in it like a caption dropped in leftover room. |
| 5 craft for pen | 7 | Clean: no floods, every spacing ≥ 0.8 mm (red 1.04, comets 0.83), label clearance a constant 1.2 mm, 3 layers light→dark, one swap each, and the eyes are bare paper. It is marked down on the pen job. Black layer: 1,865 mm of travel for 45 comets, 16 consecutive hops over 50 mm (max 82 mm), because the comets are drawn in time order, not in space. Red layer: the one line is cut into 280 mm chunks and streamed out of chain order (13, 9, 10, 11, 12, 7, 8, 0…6), with a 173 mm hop and 13 lift/drop seams on a line whose whole claim is continuity. At 0.2 s dwell with a 0.5 crimson, each seam risks a dot. The title is a single 0.3 hairline at 12.6 mm cap height, so it has height but no mass. |
| 6 concept legibility | 7 | No schematic. "LONG SHORT-TERM MEMORY" beside one long unbroken red line and many short black strokes is a real pun, and the proverb (palest ink vs best memory) is the twist. It lands. Two things hold it down. (a) The two states never meet: the letters and comets live in the top lobe, the coil in the bottom lobe, and nothing crosses the waist, so no letter can be traced to "its" half-turn. (b) The forget signal is drowned by the potential's shape. On rays from the red eye the pitch runs 1.0–1.5 mm south but 3.6–7.3 mm north (egg-shaped well). The carry_t band (turns 7–10, about 1.3 vs 2.2 mm) is a 2:1 signal under a 5:1 geometric one, so the coil reads as "dense at the bottom" (gravity), not as forgetting. At 3 m the silhouette also names an object: an hourglass. That may be a gift (time), but it is undeclared. |
| 7 depth & dimensionality | 7 | Flatness is declared and mostly serves: the coil and swirl both read as funnels. The comet cut-rule (older cut by newer) gives a faint over/under in the dense lower-left of the swirl. There is no weight fall-off toward either eye. |

avg **7.00** · min **6** · **VERDICT: FAIL**

## Reads at a glance
At 3 m: a red hourglass. A black whirlpool of short strokes ringed by a proverb fills the upper bulb, a tight red coil the lower, one red line lashes the whole, and LONG SHORT-TERM MEMORY runs up the right edge.

## Acceptance checks
There is no `encoding.md` or `BRIEF.md` in `studio/lstm-spirals/`, so there are no §11 checks. Against the HANDOFF's own claims:
- c_t is ONE continuous line: **PASS** geometrically (the 14 chunks chain end to end). It is **FAIL** as plotted: the chunks stream out of order with 13 seams.
- red pitch floor 0.9 mm: **PASS** (measured minimum 1.04 mm).
- comets cut where a newer one comes within 1 mm: **PARTIAL** (measured minimum 0.83 mm, 84 samples under 1.0 mm).
- comets never close a turn: **PASS** (none closes by eye; longest 135 mm).
- last 12 characters wrap the whole field: **PASS** (3 outer wraps, loose end at (122.6, 254.6) inside the wraps).

AUTHORING §6 (reference in play, judged as an interpretation of the reference's two-vortex dynamical plate):
1. Main forms recognisable without colour: **PASS.** The comet grammar and the coil grammar differ, so the two lobes separate in monochrome.
2. Lines follow the surface, not a random mesh: **PASS.** Comets ride the swirl and the coil rides the well.
3. Fine lines that are two sides of one thick stroke: **PASS.** The three outer wraps are three turns, not a doubled edge.
4. Blackest regions intended: **PASS (marginal).** The densest zone is the comet convergence at x 55–75, y 180–225, at 0.83 mm centre spacing. That leaves only 0.33 mm of white at a 0.5 nib, which is intended but on the edge.
5. Labels readable at real pen width: **PASS.** Proverb caps are about 4 mm at 0.3 and the colophon about 2.2 mm with legible subscripts.
6. Thicker pen knots corners or fills highlights: **PARTIAL.** Both eyes are bare, but the 13 mid-line lift/drop seams on the 0.5 crimson are the likely knots.
7. Long empty travels / pointless tiny marks: **FAIL.** Black layer 1.87 m travel with 16 hops over 50 mm, and a red chunk hop of 173 mm. The 112 sub-2 mm strokes are all type, which is acceptable.

Against the reference as an interpretation: it keeps black-above / red-below and the two sinks. It drops the reference's heart, the saddle where both families pass through each other. The waist here is empty, so the plate shows two memories side by side rather than one memory feeding the other.

## Biggest weakness
The two states are drawn as two unrelated objects. The data that should tie them (each input character produces one comet AND half a turn of c_t) is invisible because the letters and comets are in the top lobe and the turns are in the bottom lobe, with an empty waist between them. On top of that, the red coil's only visible modulation is the egg-shaped well (north gaps 3.6–7.3 mm vs south 1.0–1.5 mm), which buries the forget-gate bands. The long line reads as "long" but not as "memory of this sentence".

## Mandates
1. **Make the waist the link, and lean it.** Offset the red eye at least 12 mm horizontally from the black eye (for example red eye to x≈95 with the black eye kept at x≈70), so the eye-to-eye line is a diagonal at least 10° off vertical. Then route something that belongs to both states through the waist band (y 115–140): either the c_t line passes up through the waist so it runs within 3 mm of every proverb letter it read, or each comet's tail crosses the waist into the red lobe. Test: in a crop of the waist at least one mark connects the lobes, and a finger on any letter, say the M of MEMORY, can follow ink to a red half-turn.
2. **Let carry_t, not the well's shape, set the coil's tone.** Make the ring pitch isotropic around the red eye: for every turn, the gap measured on the north ray and the gap on the south ray must agree within 1.5×. Today they differ by 3–5× (north 3.6–7.3 mm, south 1.0–1.5 mm). The forget events (the turns 7–10 band at about 1.3 mm) then read at 1 m as a dark ring all the way round instead of a bottom-heavy crescent. Test: ray-crossing gaps from the red eye at 0/90/180/270°, reported in NOTES, satisfy max/min ≤ 1.5 per turn. The tight band then shows as a closed dark ring in a full-page view.
3. **Stream the plate the way the user asked: batched and clean at every colour change.** Stream the red chunks in chain order so each starts exactly where the previous ended, with zero travel between them. Put the chunk seams where the line is most open (north side of the well), never in a tight band. Order the black comets spatially (nearest-endpoint, alternating direction allowed) instead of by time. Pin the colophon to a named line while touching layout: flush-left at the red outer wrap's right extreme (x≈133.6), or with its baseline on the waist centre y≈128. State the draw mm, travel mm and minutes per layer and in total in HANDOFF. Test: the parser shows red inter-chunk travel = 0, black travel ≤ 400 mm with no consecutive hop over 50 mm, and a per-layer time table in HANDOFF.

## Follow-up on open mandates
No LEDGER.md or FEEDBACK.md is on file, so there are no A*/J* ids. The r03 art mandates are the open set. r04 changed direction (DESCRIPTION "Next versions 3: memory-strata"), so they are judged in spirit.

| id | status | evidence |
|---|---|---|
| r03-M1 black vortex carries h_t's sign (three bands) | PARTIAL | The black layer now carries per-step data: sweep length = RMS(h_t), with comets from 5 to 135 mm, one per letter. Sign is not shown and there are no bands aligned to the red rhythm. |
| r03-M2 invert hierarchy + commit asymmetry + footer on a named line | PARTIAL | The axis is committed off-centre (x≈78, left), and the red line now contains the whole figure. The black swirl is still the loudest ink. The colophon's edges land on no named line (x≈152, y≈113–150). |
| r03-M3 fix the pen job (black travel < 1.5 m, no hop > 50 mm; eyes bare; no crumbs; legible subscripts) | PARTIAL | Eyes bare: FIXED. Crumbs: FIXED (0 non-type strokes under 2 mm). Subscripts: FIXED (c_t / h_t legible). Black travel: NOT FIXED, 1.87 m (from 4.49 m) with 16 hops over 50 mm. |
| DESCRIPTION Next-3 (memory-strata: one red constant-pitch line, black fragments born at input, die within a turn, scarce red / abundant black) | PARTIAL | One line, born-at-input and never-a-turn are all delivered. Constant pitch "across the whole sheet" is not: the pitch varies 1.0–7.3 mm by geometry. Red is not scarce: it holds about 3.8 m of the 8.6 m draw. |

## Regressions vs compare-to
Compare-to is r01 v10 (DESCRIPTION § Keep); r03 is also noted.
- **Keep 1, interleaving sheaves at a genuine saddle: REGRESSED (still, second round running).** r01's best passage, black down the left into red and red up the right into black, is replaced by an empty waist. This is the same loss flagged at r03, and mandate 1 targets it.
- **Keep 2, axis as spine: CHANGED.** No axis is drawn. Both eyes still stack on an implicit vertical (x≈78), and the vertical title acts as the plate's spine. That is acceptable, but the stacking is now the cause of the static tension (dim 3).
- **Keep 3, two pens as mass: STILL TRUE.** Red owns the coil and the binding line, black owns the swirl and type. It is better than r03: the blue is gone and colour is mass again.
- **Keep 4, input sequence feeding the field: STILL TRUE, improved.** The proverb letters are the real input, each comet born 1.2 mm from its letter. This is stronger than r01's six anonymous dots.
- **Keep 5, crowd control: STILL TRUE.** Red ≥ 1.04 mm, comets ≥ 0.83 mm, no floods. The comet convergence (0.83 mm) is tighter than r01's 0.08 % side-by-side, but still above the floor.
- **vs r03: title weight REGRESSED.** r03's title was stacked hairlines at poster weight. r04's spine title is a single 0.3 hairline at 12.6 mm, so it is tall but thin: it holds the edge as a line, not as a mass.
- **Improved over r01 and r03:** the schematic is fully gone, travel is down to 3.8 m (from 10.9 m and 7.4 m), there is a real trained cell over a real sentence, and the wit (proverb × title pun) is the first time this plate has made a joke.
