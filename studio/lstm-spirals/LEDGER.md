# Ledger — lstm-spirals
**Best so far:** r04 — art 7.00/6 · sci 6/5/6 — `gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png` (+ `.gcode`). Both critics FAIL. It ranks above r03 on every axis (art min 6 vs 5, science min 5 vs 5 with truth 6 vs 5, art avg 7.00 vs 5.71).
**Route:** designer (r05, parent r04; one practice merged from r03, see SYNTH)
**Round cap:** 5 designer rounds per encoding (DESIGN_RUBRIC). The memory-strata encoding has used 1 round (r04). No `encoding.md`, `dossier.md` or `BRIEF.md` exists for this slug, and both science passes flag it (S7).

Curator note (2026-09-29, relaying Juan's pick "maybe the lstm?"): keep two black/crimson vortices on one vertical axis and the streamlines interleaving around the saddle. Fold or cut the textbook furniture. Plot on Leo as batched plate jobs (DESIGN_RUBRIC § Plottable is part of creative): there is no pen cap, but every pen needs a meaning, each pen is one clean layer in a stated order, strokes are spatially ordered for batching, and NOTES gives minutes per layer and in total. Name the LINEAGE. Juan's own words from the harness: more than 4 colours and longer sessions are fine **as long as batching and colour changes are right**.

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | faithful: the reference double vortex (two point sinks, exact saddle) carrying the textbook LSTM label deck | `gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png` | — | — | unscored (pre-workflow) | Source of the curator's Keep list: the interleaving sheaves (black down the left, red up the right) and the axis spine. Furniture: equations, legend, gate leaders. 10.9 m travel. Keep on disk as the `faithful` flavour |
| r02 | r01 | — | — | — | — | abandoned | partial start, see `rounds/r02/ABANDONED.md`. Ignore it |
| r03 | r01 | forget-gate-vortex (Duchamp, *Rotoreliefs*): a 1-unit analog-latch LSTM. Red annuli close where f>i, blue drain where i>f, black h_t whirl | `gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.png` | 5.71/5 | 5/5/6 | FAIL · rank 2 | The Rotorelief disc of time is a real idea. But the dominant black mass is mute (o≈0.98 at every step), the blue writes collapse 3 steps into one band, the title "THE FORGET GATE IS A DRAIN" inverts f, the gate trace lives only in a .py, and black travel is 4.49 m. Interleave and axis REGRESSED vs r01. Worth keeping on disk as the `forget-gate-vortex` flavour; not iterated further |
| r04 | r01 | memory-strata (Smithson, *Spiral Jetty*): an 8-cell char LSTM reads "THE PALEST INK IS BETTER THAN THE BEST MEMORY". c_t = ONE red line, ½ turn per letter, pitch ∝ carry. h_t = 45 black comets born at their letters, sweep ∝ RMS(h) | `gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png` | 7.00/6 | 6/5/6 | FAIL · **rank 1 (best)** | Real reproducible model (the JSON reproduces loss 0.0754 exactly). The pun (LONG line vs SHORT strokes) plus the proverb make the plate's first joke. Travel 3.8 m. But the waist is an empty void (interleave REGRESSED a second time), the pitch is warped 1.2–4.6× by the teardrop and clamps 6 steps, 39 half-turns vs the caption's 45, 41/45 comets are cut to a crowd length, and the red chunks and black comets are streamed out of spatial order |

Ranking after r03/r04 (parallel theses, both forked from r01): **r04 > r03** on verdict tie, art min, science truth, art avg. r04 is the parent of r05. The visual merge from r03 is nothing. The practice merge is r03's `check_plate.py` discipline: read every data channel back off the emitted gcode and report designed vs drawn per step.

Recurring failures across both siblings:
- **C2**, the saddle interleave: REGRESSED in r03 and in r04.
- **A10**, the pen job: black-layer sheet-crossing travel (r03 4.49 m, r04 1.87 m with 16 hops > 50 mm).
- **S1**, no checkable per-step trace.

The rounds were parallel siblings, not consecutive, so rule 2 has not fired. **If r05 fails C2 or A10 again, route translator**, who then also writes `encoding.md` (S7).

## Mandates
| id | raised | by | mandate | status | closed |
|---|---|---|---|---|---|
| C1 | r03 (curator note) | curator/Juan | Keep two black/crimson vortices on one vertical axis | fixed (art r04: both eyes stack on x≈78; black above, red below) — now a Preserve item | r04 |
| C2 | r03 (curator note) | curator/Juan | Keep the streamlines interleaving around the saddle. Merged here: art r04 M1 ("make the waist the link"), science r03 S3 / r04 M3 (no drawn c→h coupling, h = o·tanh c; layers ≥ 6.82 mm apart) | open. REGRESSED r03 → r04 (parallel siblings). **Mandate #1 for r05; a third miss routes translator** | |
| C3 | r03 (curator note) | curator | Cut or fold `LSTM EQUATIONS`, `FLOW LEGEND` and the arrow/label callouts | fixed (art r03 + r04: "schematic fully gone") | r04 |
| C4 | r03 (curator note) | curator | Each pen has a stated meaning; each pen is one clean layer in a stated order | fixed (art r04: 3 layers light→dark, one swap each, meanings stated) | r04 |
| C5 | r03 (curator note) | curator | Spatially ordered strokes for batching + minutes per layer and total | merged into A10 | |
| C6 | r03 (curator note) | curator | Name the LINEAGE | fixed (r04: Smithson, *Spiral Jetty* / *A Sedimentation of the Mind*; art accepted it in the header) | r04 |
| A1 | r01 (DESCRIPTION Weak concept) | art | Textbook schematic; the mechanism is not in the geometry | fixed (art r04 concept 7, "no schematic"; science: real model, pitch tracks f̄ at corr 0.82) | r04 |
| A2 | r01 (DESCRIPTION Weak tension) | art | Congruent 180° lobes, centred | open, partial. r04: lobes 1.3:1, figure pushed left, but still a mirror-stacked 8 (tension 6). Constrained by C1 (one vertical axis), so tension must come from the waist readout, the unequal lobes and the loose red end. Deferred behind C2 | |
| A3 | r01 (DESCRIPTION Weak craft + If-only 2) | art | Red through the label block; plus mark on the L; halo round every label | fixed (art r04: label clearance a constant 1.2 mm; red ≥ 2.43 mm from type; no plus marks) | r04 |
| A4 | r01 (DESCRIPTION Weak hierarchy + If-only 3) | art | Dotted t-rings swallowed | dropped: the t-rings were removed by both theses (time is the coil itself) | |
| A5 | r01 (DESCRIPTION Weak grid) | art | Labels float in leftover white with leaders ending nowhere | fixed (art r04: spine title spans exactly the red y-extent). The colophon residue carried as A12 | r04 |
| A6 | r01 (DESCRIPTION Weak space) | art | Empty left third is residue | fixed (art r04 negative space 7: the waist void is "the plate's best silence"). The right band x 135–185 is still gap, tracked under A12 | r04 |
| A7 | r01 (DESCRIPTION Weak depth) | art | Flat and undeclared | fixed as declared flat (r04 HANDOFF `declared: flat`; art depth 7) | r04 |
| A8 | r01 (DESCRIPTION If-only 1) | art | Black vortex ~1.4× red so the lobes are unequal | fixed (r04 c_b 1.3 : c_r 1.0; separatrix 44 mm vs 30 mm) | r04 |
| A9 | r03 | art | r03 M1 (black annuli carry h's sign as 3 bands) and M2 (disc ≥ 140 mm, axis to x≈130) | dropped with the r03 thesis. r04's per-letter comet channel supersedes M1. Keep the flavour on disk | |
| A10 | r03 · r04 | art + curator + Juan | **Pen job, measured on the EMITTED gcode after `reorder_by_color`.** Red streams in chain order with 0 mm inter-chunk travel, seams on the open (north) side of the well, never inside a tight band. Black strokes spatially ordered: black travel ≤ 400 mm, no consecutive in-layer hop > 50 mm. HANDOFF has a table of draw mm, travel mm and minutes per layer and in total | open. NOT FIXED r03 (4.49 m black travel) → r04 (1.87 m, 16 hops > 50 mm; red hop 173 mm, 13 seams streamed 13,9,10,…). Parallel siblings. **A third miss routes translator** | |
| A11 | r04 | art | Lean the eye-to-eye axis ≥ 10° off vertical (red eye offset ≥ 12 mm) | argued by the lead, dropped. It contradicts curator C1 ("two vortices on one vertical axis"), and Juan's pick outranks a critic's tension fix. The critic's underlying complaint (static stack, dim 3 = 6) stays open as A2 | |
| A12 | r03 · r04 | art | Colophon / footer on a named line: flush-left at the outer wrap's right extreme (x≈133.6) or baseline on the waist centre (y≈128); not floating at x≈152 | open. Carried inside mandate #5 | |
| A13 | r04 | art + science | **carry_t, not the well's shape, sets the coil's tone.** On the 0/90/180/270° rays from the red eye, the north and south gap per turn agree within 1.5×. Today they differ 3–5× (north 3.6–7.3 mm, south 1.0–1.5 mm). gap = g0 + k·f̄_t, affine, unclamped, all 45 values distinct (today 6 steps sit on the 0.9 floor), no outward trend | open. Mandate #2 | |
| A14 | r04 | art | Spine title weight regressed vs r03 (a single 0.3 hairline at 12.6 mm cap height) | deferred: low. A heavier spine could fight the figure for 2nd place. Revisit once C2 lands | |
| A15 | r04 | art | Proverb tracking is uneven ("B E T T E R" tight, " T H A N" loose, "T H E" cramped at the waist) | deferred: low. Re-judge after the C2 readouts change the waist | |
| S1 | r03 · r04 | science | Checkable per-step trace: a data file (not .py) with T, the sequence and per-step i_t, f_t, o_t, c_t, h_t, RMS(h_t), f̄_t, plus the written definition of `carry_t` (science had to infer it at corr 0.82) | open, partial (r04 ships `lstm_weights.json`, which reproduces loss and accuracy). Carried inside mandate #2 | |
| S2 | r03 | science | Blue write = one countable annulus per step; give the gate magnitude a channel | dropped with the r03 thesis (no blue in r04). The magnitude part is carried as A13 | |
| S3 | r03 | science | Fix the o_t / "drain" claims; draw a c → h coupling | partial: "drain" title and o_t claim fixed (science r04 FIXED). The coupling is merged into C2 | |
| S4 | r04 | science | The red count matches the caption: 45 half-turns (22.5 turns), or a caption that is true as drawn (measured 39.07 half-turns: ~16.5–17.5 lobe turns + ~2.9 whole-field wraps for 12 letters). Key coils to letters, e.g. a tick per half-turn or first/last-letter marks on the lobe and the wrap. Print what the 12-letter wrap means | open. Mandate #3 | |
| S5 | r04 | science | Every comet shows its RMS(h_t) after the crowd cut: 41/45 are cut at exactly 1.00 mm, and visible sweep vs RMS corr = −0.11. Only E#32, B#34, S#36 and Y#44 read true | open. Mandate #4 | |
| S6 | r04 | science | "Permanent sediment" overclaims retention. The recomputed best cell keeps < 10 % of a write after a median of 9 and a max of 12 steps; step 0's write survives at 4.5e-9. Say it on the sheet (the 12-letter wrap may BE the horizon) | open. Merged into mandate #3 | |
| S7 | r03 · r04 | science | No `dossier.md` / `encoding.md`, so critics grade against numbers they derive themselves | open. r05 NOTES carries the check-number table. The translator writes `encoding.md` if rule 2 fires | |
