# Science critique — millennium-poincare r03 · mathematics (geometric topology, Ricci flow) · 2026-09-29
render: gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.png (+ `_phys10.png`), gcode `gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.gcode`
(pass 2 — LEDGER.md open mandates A1–A5, S1)

Method: `snapshots.npz` is byte-identical to r02's. I rebuilt all 46 isochrones myself in the frame
HANDOFF states: `embed` by ∫√(1−ψ_s²)ds, neck pinned at (165, 200), axis at 62°, 62 mm/u, and each
piece's ψ²ds-centroid held at its t_s position. I then parsed every pen-down stroke of the gcode per
`; color=N` and found 0 pen-state anomalies. Layer 0 has 63 strokes and 9,966 mm of ink. Layer 1
(keyline) has 2 strokes, 716 mm. Layer 2 (type) has 1,190 strokes. Layer 3 (red) has 18 strokes.

**Independent flow check.** I wrote my own arc-length re-gridding solver. It is stable to about
t = 0.02 and drifts at the poles after that. Up to that point it matches the dossier data within
0.3 %: at t = 0.02 the neck is 0.2645 vs 0.2639, the big lobe 1.3422 vs 1.3428, and L 5.9667 vs 5.9676.
The 2-D run (n = 1) gives neck 0.3561 at t = 0.0547, against the dossier's 0.3554. At all 7
pre-surgery snapshots the neck PDE residual (ψ_t = ψ_ss − 1/ψ against `neck_track`) is ≤ 0.6 %.

**Global match.** 99.99 % of layer-0 ink lies within 0.3 mm of a recomputed isochrone, and the
maximum deviation is 0.31 mm. Layer-1 ink lies within 0.05 mm of the t_s outline. Both nests sit
0.28 mm further from the cut than my reconstruction. The red dots show the same offset. This is a
centroid-convention difference and is below the nib width.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | r² = r₀² − 4t; post-surgery slopes | −4; A −4.003, B −3.908 | A −4.020, T_A 0.3873; B −3.53 over ψ_max < 0.35 (not yet round), tail T_B ≈ 0.1171–0.1177 | A equator gaps widen inward 1.43 → 7.55 mm | OK |
| 2 | neck / big / small, R_min | 0.3143 / 1.4139 / 0.6765; R_min 0.2213 | 0.3143 / 1.4140 / 0.6765 (neck/big 0.2223); L₀ 6.0059; vol 44.574; **R_min 0.2167** (analytic, at the pole) | start-line waist 19.49 mm = 0.3143·62 | **dossier wrong (R_min), still unfolded** |
| 3 | neck −62 %, lobe −12 % | 0.3143 → 0.1197, 1.4139 → 1.2447, small → 0.4709 | −61.9 % / −12.0 % / −30.4 %; absolute neck −0.1945 u vs big lobe −0.1690 u | footer "NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 %"; red cap r 7.42 mm = 0.11971·62 | OK |
| 4 | T_pinch; d(ψ²)/dt | ≈ 0.0628; → −2 | T_pinch 0.0629 (quadratic on the last 200 track points); −1.70 at t_s | waist fan steps 3.49 · 2.53 · 2.07 · 1.76 mm (both flanks, ±0.01), accelerating inward | OK |
| 5 | event order | 0.063 < 0.1171 < 0.3873 | confirmed | on the cut-side axis, 33 A and 6 B rings are all present | OK |
| 6 | roundness L/ψ_max → π | A 3.140, B 3.185 | A 3.140, B 3.184 | last ring A 6.44 mm radius on the equator vs 6.14 / 6.71 mm along the axis (the 0.28 mm offset); B 6.12 vs 6.00 / 6.57 | OK |
| 7 | 2-D control | 0.3143 → 0.3554; A₀ 25.346; T 1.0085 | 0.3561 (independent solver); A₀ 25.347; T 1.0085 | footer "(0.314 → 0.355)" | OK |
| 8 | planar CSF | A₀ 3.3180, T 0.5281 | 3.3183, 0.5281 | not drawn (declared) | OK |
| 9 | closed geodesics; stuck loop | s 1.601 / 3.856 / 5.141; 1.975 | 1.598 / 3.855 / 5.139; 2π·0.3143 = 1.9748 | not drawn | OK |
| 10 | Gauss–Bonnet | 2π; 4π | exact | not drawn | OK |
| — | red caps | r = h | 7.422 mm | 2 semicircles, r 7.425 / 7.419 (sd < 0.01), chord 14.85 mm at 152.0° ⟂ 62° | OK |
| — | extinction points | ψ²ds-centroids | A (109.42, 95.47), B (195.26, 256.91) | A (109.29, 95.22), B (195.13, 256.66), ink Ø 1.90 | OK (0.28 mm) |
| — | Δt grid | 0.01 anchored at t_s | 5 past + 33 A + 6 B | grid lines drawn where drawn ±0.31 mm; **equator counts A 31/33, B 5/6** (see mandates) | **VIOLATED at the keyline** |
| — | time occlusion | past only outside keyline | — | 0.0 mm of past ink inside the keyline; 0.0 mm of future ink outside it | OK |
| — | floor ≥ 0.8 mm | — | — | minimum gap between distinct strokes (layers 0+1) 0.847 mm | OK |

**Dossier findings (carried from r02, still not folded back):**
- §7 #2: R_min is 0.2167, not 0.2213.
- Lie 4 / §2(a): "lobes barely move" is only relative. The big lobe loses 0.169 u, which is 87 % of the neck's 0.195 u.

## Lies list       item | clean / VIOLATED (where)
| # | item | verdict |
|---|---|---|
| 1 | tidy row of elongated loops | clean: the last rings are round (A 1.00, B 1.02 aspect) and the gaps widen inward |
| 2 | CSF shrinking the neck loop | clean (not drawn) |
| 3 | pinch under 2-D flow | clean: "EVERY CHORD A ROUND 2-SPHERE" and "IN 2-D THE SAME NECK WOULD WIDEN" |
| 4 | wrong order / visible lobe shrink | order clean (6 < 33 on the cut-side axis). The "no visible shrink" clause is a dossier defect (finding above) |
| 5 | fat-neck surgery | clean: cap 7.42 mm vs A ψ_max 77.2 mm, 1 : 10.4 |
| 6 | uneven / undeclared Δt, re-spaced | **VIOLATED (local, undeclared).** The 3.05 mm keyline moat erases grid lines that sit 0.8–3 mm from the keyline, so no line is re-spaced but the gap next to the keyline no longer means Δt. The erased lines are t_s−0.01 (6 % drawn, 504 mm moat-only loss), A t_s+0.01 (5 % drawn) and A t_s+0.02 (9 %), and B t_s+0.01 (41 %, 181 mm moat-only loss). In total ≈ 1.0 m of honest data ink is removed by the moat alone. On A's equator the first gap inside the keyline is 4.27 mm against a true 1.34 mm (≈ 3 Δt shown as 1). On B's equator it is 4.53 mm against 2.09. On-sheet counts along the equators are 31 A and 5 B. The start line is off-grid and declared on the sheet ("OUTERMOST LINE: t = 0 (OFF THE GRID)"), so the t_s−0.05 merge is honest |
| 7 | drawn surface as S³ | clean |
| 8 | "loops contract" as the proof | clean |
| 9 | credit / history | clean: Perelman 2002-03, after Hamilton (1982), Fields 2006 + Clay 18 Mar 2010 both declined, Clay 2000, arXiv IDs correct |
| 10 | extra pinches / handles | clean |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 8.** Every §7 number and every caption figure checks. The flow independently matches to ≤ 0.3 % where my solver is valid. Occlusion is exact.
- **fidelity 7.** The time scale breaks at exactly the event line. The moat's ≥ 3 mm bare band on both sides reads as elapsed time, and the lifetime count the encoding makes the reader's clock ("ring count is the lifetime") is wrong on both equators: A 31 instead of 33, B 5 instead of 6, a 17 % error in B's lifetime. r02 held all 33 + 6 on the equator rays, so this is a regression.
- **legibility 8.** The heavy line now separates past from future. The caption declares it, the relative race is stated, SOLVED is present, and the corner line lands the twist.
- **VERDICT: FAIL** (fidelity 7 < 8).

## Mandates        1. … 2. … 3. …
1. **Past side: restore t_s − 0.01.** The last past line is 6 % drawn (50 mm of ≈ 740). It is visible only at the waist fan, so the lobes carry 3 past lines instead of 4. Expected: ≥ 65 % drawn. My occlusion + 0.8 mm-floor model gives 70 % drawn with a moat of ≤ 1.5 mm centre-to-centre. Location: outside the heavy line along both lobes, e.g. A's upper flank x 60–150, y 130–175, and B's flanks x 175–240, y 225–290. The heavy line keeps its separation by its 0.5 nib, not by blanking data.
2. **Future side: the equator counts must equal the lifetimes.** Measured on the rays through each extinction point ⟂ to the axis: A shows 31 rings (t_s+0.01 and t_s+0.02 missing) and B shows 5 (t_s+0.01 missing). The first gap inside the keyline is 4.27 mm on A's equator (near (40, 136) and (178, 55)) and 4.53 mm on B's equator. Expected: 33 and 6 rings on the equators, with first gaps of 1.34 ± 0.3 mm (A) and 2.09 ± 0.3 mm (B). The model predicts B t_s+0.01 is 100 % drawable and A t_s+0.02 44 % drawable at a moat ≤ 1.2 mm. Test: re-run the equator-ray count on the gcode.
3. **Fold the dossier corrections in before the next round.**
   - §7 #2: R_min 0.2213 → **0.2167** (analytic minimum, at the poles).
   - §2(a) and lie 4: replace "lobes barely move / do not show the lobes shrinking visibly" with the measured relative statement: neck −62 % (−0.195 u, 12.1 mm at 62 mm/u) against big lobe −12 % (−0.169 u, 10.5 mm), small lobe −30 %.

   This is the source the footer's "−12 %" line is checked against. Two science rounds have flagged it, and it is still the only wrong number in the verification chain.

## Follow-up on open mandates   id | status | evidence
| id | status | evidence |
|---|---|---|
| A1 | **FIXED — but REGRESSED science (see M1/M2)** | (a) the minimum layer-0 → keyline distance is 3.048 mm, and 0 samples are < 2.5 mm. (b) The keyline is on its own layer 1 (0.5), single pass: 2 strokes, 716 mm = 734 − 2 × 8.7 mm pause. (c) "OUTSIDE THE HEAVY LINE: BEFORE THE CUT · INSIDE: AFTER" is present. The cost: ≈ 1.0 m of true grid ink is erased, and the equator counts drop 33 → 31 and 6 → 5 |
| A2 | FIXED | layer 0 has 63 strokes and the shortest is 20.74 mm, so zero strokes are < 15 mm. The rims are continuous or cleanly absent, and far-pole merges are true sub-floor convergence (15 rings within 2 mm at A's pole) |
| A3 | FIXED | red-to-keyline edge gap is 0.828 mm (0.5 + 0.5 nibs), red to layer 0 is 3.09 mm, and red to type is > 10 mm. Cap radius stays 7.42 mm = h. The keyline pauses symmetrically, 8.7 mm per flank, and its ends sit 8.76 mm from the cap centre |
| S1 | FIXED | footer reads "NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 % · CUT AND CAPPED AT t = 0.055" (recomputed −61.9 / −30.4 / −12.0 %) and "OUTERMOST LINE: t = 0 (OFF THE GRID)". Nothing is re-spaced: all ink is ≤ 0.31 mm from its isochrone |
| A4 | FIXED | the dry-run reproduces ~23 / ~2 / ~53 / ~2 min, ETA ~85 min, 4 swaps. The series caption "MILLENNIUM PRIZE PROBLEMS 6 / 7" / "CLAY MATHEMATICS INSTITUTE, 2000" sits at x 205–282, cap height 2.2 mm |
| A5 | NOT TAKEN (deferred) | dots still Ø 1.90 mm |
| Regression flag | — | r02 truth "all 33 + 6 rings found on the equator rays" no longer holds (31 + 5) |
