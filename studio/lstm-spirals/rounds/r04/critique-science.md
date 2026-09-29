# Science critique — lstm-spirals r04 · machine learning (LSTM recurrent memory, dynamical systems) · 2026-09-29
render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png (+ .gcode: 25285 cmds, 3 pens. Re-summed from the gcode: crimson 3809.9 mm in 14 pen-downs · black 3348.3 mm in 45 strokes · type 1401.1 mm in 281 strokes)

Pass 1 (cold). This slug still has no `dossier.md`, `encoding.md` or `LEDGER.md`, so there are no §7 numbers and no §4 lies list. **What is new is a checkable data file**: `rounds/r04/lstm_weights.json`. I did not open train_lstm.py or piece.py. I rebuilt the forward pass from the JSON alone: W (32×36), gate order i,f,o,g, input [x;h], a '.' start token, and the sequence ".THE PALEST INK IS BETTER THAN THE BEST MEMORY." That reproduces the file's stated metrics exactly. The per-step trace below comes from that recomputation. HANDOFF's `carry_t` has no written definition. Of the candidates, the mean forget gate f̄_t matches the coil spacing best (corr 0.82), so I tested against that.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| model loss / accuracy on target | JSON: 0.0754 nat/char, 1.0 | 0.0754, 1.000 (46 predictions, '.'-framed); without the '.' start token it is 2.549 / 0.727 | caption "TRAINED ON TWELVE SAYINGS, READS THIS ONE ONCE" | OK (corpus_lines 12, hidden 8) |
| characters T | 45 | 45 | 45 black comets, one per letter slot including 8 spaces; starts sit on the proverb ring | OK |
| red line continuity | "ONE continuous line" | — | 14 pen-downs chained with endpoint gaps of 0.000 mm and a 0.43 mm max step; geometrically one line, 3809.9 mm, eye (78.4, 48.9) → end (122.6, 254.6) | OK (plotted in 14 × ~280 mm batches, not in time order: 0–6, 7–8, 9–12, 13) |
| red half-turns about the eye | 45 (½ turn per letter; caption says "HALF A TURN PER LETTER") | 45 → 22.5 turns | **39.07 half-turns = 19.5 turns** about (78.3, 54.1). About 16.5–17.5 turns in the lobe, then **~2.9 whole-field wraps** (x=78 top crossings at y 273.3 / 275.0 / 276.7; y=200 left crossings at x 28.3 / 25.9 / 23.0; right side 2) | **NO**: 6 half-turns short; 12 wrap letters get ~¼ turn each, not ½ |
| pitch = 1.8 mm × carry_t, floor 0.9 | 0.9–1.8 mm | f̄_t 0.332–0.837 → 0.90–1.51 mm | normal gap to the next coil: tightest side 1.04–2.01 mm, mean 1.37–2.3 mm (half-turns 0–20), rising to 2.6–5.0 mm (half-turns 28–33); up-ray gaps 1.67 → 7.27 mm | relative only: corr(gap, f̄) = 0.82 (half-turns 2–29, 1-step lag). The absolute scale is broken and inflated 1.2× → 4.6× outward |
| floor clamp | floor 0.9 | 6/45 steps have f̄ < 0.5: I 0.472 · N 0.498 · K 0.469 · I 0.332 · ' ' 0.366 · Y 0.427 | min gaps at half-turns 11–15 are flat, 1.04–1.14 mm | the six strongest-forget steps are indistinguishable |
| comet sweep = RMS(h_t) of a turn | ½ to 1 | RMS(h) 0.373 (S #36) – 0.770 (T #9), all < 1 | eye fitted at (78.7, 231.7) from the cut-end ring. The **4 uncut comets** (E #32, B #34, S #36, Y #44) sweep 1.07 / 0.99 / 1.03 / 1.02 × RMS. The **other 41 are cut at exactly 1.00 mm** from a newer comet, with visible sweep 0.007–0.54 turn; corr(visible sweep, RMS) over all 45 = **−0.11** | channel intact on 4/45 |
| "tanh < 1, so none closes" | — | max RMS 0.770 | max sweep 0.77 turn | OK |
| c_t long-term memory (title / Spiral-Jetty sediment) | implied persistence across all 45 letters | per-cell mean f 0.30–0.80 (timescales 1.4–5.0 steps); the best cell's survival of a write falls < 10% after a median of 9 and a max of **12** steps; survival of step-0's write to the end is 4.5e-9 | lobe coils hold letters 1–33 as permanent sediment; the last 12 letters wrap the field, unexplained | stratum-as-kept is **not** what this model does; the "12" matches the real retention horizon, but the sheet never says so |
| c → h coupling (h = o·tanh c) | — | — | the red and black layers never come closer than 6.82 mm; no link | absent |
| clearances | — | — | black–type min 1.20 mm, red–type 2.43 mm | OK |

## Lies list       item | clean / VIOLATED (where)
(There is no dossier §4. Items come from HANDOFF, the sheet caption, and the standard LSTM lies.)
| item | status |
|---|---|
| gate values invented rather than computed | **clean**: the JSON reproduces loss 0.0754 and accuracy 1.0, and coil spacing tracks recomputed f̄_t (corr 0.82) |
| "HALF A TURN PER LETTER" (caption, x≈150–175, y≈112–125) | **VIOLATED**: 39.07 half-turns for 45 letters; the last 12 letters get ~2.9 whole-field wraps instead of 6 |
| "ONE STROKE PER LETTER" (h_t) | clean: 45 strokes |
| "NEVER A TURN" (h_t) | clean: max 0.77 turn |
| a decorative scale posing as data (coil spacing) | **VIOLATED**: outer lobe coils widen 2.6–5.0 mm (up-ray to 7.27 mm) while f̄ over those letters has no trend (predicted 1.0–1.44 mm), so the sheet reads "carry rises over time" |
| a comet's length reads as |h_t| | **VIOLATED** for 41/45: the visible length is set by the 1 mm crowd cut and grows with letter index (5.2 mm for the first T → 93 mm for H #31), not with RMS(h) |
| cell state as permanent sediment (Smithson strata; "LONG" memory) | **VIOLATED (soft)**: the real model forgets a write to < 10% within ≤ 12 steps; the lobe draws letters 1–33 as retained strata |
| "forget gate is a drain" (r03 title) | clean: gone |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- truth **6**: the model is now real and reproducible, a large gain. The caption's own count is false (39 half-turns vs 45), and the sediment metaphor claims retention the model does not have. The 12-letter wrap may be the true horizon, but that is not stated.
- encoding fidelity **5**: the pitch carries f̄_t only relatively. It is warped 1.2–4.6× by the lobe's teardrop and clamped for the 6 strongest forgets. The h channel survives on 4 of 45 comets.
- insight legibility **6**: one continuous red line against 45 broken black strokes does read as persist-vs-flicker to a stranger. But no coil is keyed to its letter, the wrap is unexplained, and h = o·tanh c is not drawn.
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **Make the red count match the caption, and say what the wrap means.** Caption "HALF A TURN PER LETTER" (x≈150–175, y≈112–125). Measured: 39.07 half-turns about the red eye (78.3, 54.1), i.e. ~16.5–17.5 lobe turns plus ~2.9 whole-field wraps (top crossings at x=78, y 273.3 / 275.0 / 276.7; the line ends at (122.6, 254.6)). Expected: 45 half-turns = 22.5 turns, so the 12 letters of " BEST MEMORY" need 6 wraps, or the caption must say ¼ turn per wrap letter. Key the coils to letters: a tick per half-turn, or first/last-letter labels on the lobe and the wrap. If 12 is the retention horizon, print it: recomputed best-cell survival falls < 10% after a max of 12 steps (median 9).
2. **Put the pitch on a true, unclamped scale.** Expected coil gap = 1.8 × f̄_t, i.e. 0.90–1.51 mm, with no outward trend. Measured mean normal gap: 1.37–2.3 mm (half-turns 0–20) → 2.6–5.0 mm (half-turns 28–33); up-ray gaps 1.67 → 7.27 mm; tightest-side gaps reach 2.01 mm, above the 1.8 ceiling. The lobe's teardrop warp inflates the outer coils up to 4.6×, and a reader sees carry rising. Also, 6/45 steps (I 0.332, ' ' 0.366, Y 0.427, K 0.469, I 0.472, N 0.498) all clamp to the 0.9 mm floor, so the plate's biggest forget looks the same as f = 0.5. Use a constant-shape (direction-normalised) spiral and an affine map, e.g. gap = g0 + k·f̄ with g0 ≥ nib clearance, so all 45 values stay distinct.
3. **Give every comet its RMS(h_t), not just the survivors.** 41/45 black comets are cut at exactly 1.00 mm from a newer comet. Their visible sweep (0.007–0.54 turn about the eye at (78.7, 231.7)) has corr −0.11 with RMS(h). Examples: the first T (start (76.2, 141.3)) has RMS 0.609 and is drawn 0.007 turn / 5.2 mm long; T #9 (start (36.7, 195.4)) has RMS 0.770, the maximum, and is drawn 0.204 turn. Only E #32, B #34, S #36 and Y #44 read true (1.07 / 0.99 / 1.03 / 1.02 × RMS). Expected: each comet's RMS stays readable after the cut. Options: an end-dot or tick at the RMS angle, a dotted continuation, or a comet thin enough to go uncut. Drawing a h ← c link (h = o·tanh c) somewhere on the sheet would also close S3.

## Follow-up on open mandates   id | status | evidence
(There is no LEDGER.md. The open mandates are the three from r03/critique-science.md, called S1–S3 here. The concept changed from Rotorelief to memory-strata.)
| id | status | evidence |
|---|---|---|
| S1 checkable trace | **PARTIAL** | `lstm_weights.json` reproduces its stated loss 0.0754 and accuracy 1.0 exactly, and T = 45 matches the 45 comets. Still missing: a dossier §7 with the per-step trace, and a written definition of `carry_t` (I had to infer f̄_t from the corr of 0.82) |
| S2 per-step readability + gate magnitude channel | **PARTIAL** | the blue collapse is gone, and a magnitude channel now exists (pitch ∝ f̄_t, sweep ∝ RMS h). But the floor clamps 6/45 steps, the shape warp inflates the scale up to 4.6×, and 41/45 comets lose their value to the crowd cut |
| S3 o_t / drain claims, c→h coupling | **PARTIAL** | FIXED: the "drain" title is gone and o_t is no longer claimed. NOT FIXED: no c→h link; the two layers stay ≥ 6.82 mm apart |
| regressions | none | nothing that held in r03 is broken now; the red one-ring-per-step honesty has become "½ turn per letter", which this sheet fails to count |
