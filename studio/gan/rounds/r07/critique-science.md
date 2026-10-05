# Science critique — gan r07 · machine learning (GAN training dynamics, game theory) · 2026-09-29
render: gallery/studio/gan/current/pp_gan_iterate_v34.png (gcode gallery/studio/gan/current/pp_gan_iterate_v34.gcode)

Sources: there is no `dossier.md`, so the check numbers come from `encoding.md` §4.1 plus the Revision 1.1 table ("Check numbers at the final frame"). The lies list is `encoding.md` §9.

How the numbers were measured:
- I re-simulated Dirac-GAN simultaneous GDA independently in `.venv/bin/python`: f′(s) = σ(−s), h 0.26, r0 0.74, a0 0.42622, run to r > 6 (20,001 steps).
- I parsed the gcode per `; color=N` into 2,024 strokes.
- I rebuilt every reed crossing (67 × 77) as warp passes and weft passes.
- I recomputed ribbon membership myself from the chord polygon, using lo = max(0.9ρ, r0 + 1.0 mm) and hi = lo + 0.2ρ.

## Check numbers
| quantity | dossier (encoding) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| model / sign semantics | θ ← θ − hψf′(ψθ), ψ ← ψ + hθf′(ψθ), f′ = σ(−s) | G minimises and D maximises L = f(ψθ) + f(0). In the Mescheder convention D(fake) = ψθ, so ψθ > 0 means D is winning, and f′ → 0 there (the saturating loss) | Footer: `D SPOTS THE FAKE … (ψθ > 0)` / `G FOOLS D … (ψθ < 0)` | OK |
| flow eigenvalues | ±0.5i | ±0.5i. The continuous flow conserves θ² + ψ² | Full dashed circle labelled `h → 0: THE FLOW CIRCLES` | OK |
| discrete \|λ\| at r → 0 | 1.00841 | 1.008415. r_{k+1}² = r_k²(1 + h²f′²), so r is strictly increasing | Title `THE FIXED POINT REPELS`; `INSIDE THE CIRCLE: CLOSER THAN THE START` | OK |
| scale, equilibrium | 51.1 mm/unit, (66, 100) | (as given) | `+` at (66, 100). Warps at 66 + (i+½)·2.8, wefts at 100 + (j+½)·2.8 | OK |
| z_0, r0 | (100.43, 115.63), 37.81 mm | (100.431, 115.634), 37.814 | A circle dash starts at 24.416° against a0 = 24.421°. `STEP 0` ink ends at x 98.03, 2.4 mm from z_0 | OK |
| lap ends | steps 50 / 103 / 181, r 1.1207 / 1.6919 / 2.5563 | 50 / 103 / 181 / 671, r 1.12067 / 1.69185 / 2.55633 / 3.85611 | — | OK |
| lap ratio | 1.482–1.524 | 1.482–1.524 on 8 rays (0°: 1.508–1.524, 90°: 1.482–1.493, 270°: 1.482–1.487) | `EACH LAP ABOUT 1.5 × WIDER` | OK |
| first exit | step 68, r 1.2936, (6.21, 128.20) | step 68, r 1.29364, (6.210, 128.197); step 67 at (12.89, 137.62) is in frame | `STEP 68  R 1.29  LEAVES THE CLOTH`. The lap-1 crimson ribbon runs off the left cut edge at y ≈ 115–160 | OK |
| in-frame iterates | 527, parts of 5 laps | 527, by lap 50 / 33 / 33 / 73 / 338. Runs: 0–67, 78–82, 93–124, 170–253, 2454–2791 (lap-4 crawl in the NE corner) | lap 4 is visible as blue floats at x 156–198, y 235–254 | OK |
| step-length medians, lap 0–3 | D ahead 5.1 / 5.9 / 4.9 / 1.5 · G ahead 6.7 / 11.7 / 19.4 / 28.0 (at 52 mm/unit) | D 5.0 / 5.5 / 4.7 / 1.5 · G 6.6 / 11.5 / 18.1 / 27.5 (at 51.1) | not encoded on the sheet (see Advisory 2) | OK (numbers) |
| seam offsets, first post-axis iterate | N 0.32 / 0.82 / 6.04 / 15.77 · E 3.44 / 3.25 / 14.65 · S 6.29 / 4.38 / 8.29 · W 0.45 / 1.88 / 1.41 | identical, at steps 10/61/121/252 · 46/98/173 · 36/89/165 · 21/71/129 | the face changes where my recomputed owner cell changes (next row) | OK |
| reed, woven crossings | 67 × 77, 4,551 | 67 × 77 = 5,159 crossings | 4,551 woven + 608 empty. All 608 empty crossings are at ρ ≤ 38.44 (the hole). The minimum woven crossing is at ρ 39.05 | OK |
| ribbon crossings / face / double pass | 2,299 · 2,299 · 2,299 | my own membership recompute gives 2,299 | face = sign(ψ_kθ_k) of the owning cell: 2,299/2,299. Double pass: 2,299/2,299. Sign at the crossing's own point: 2,190/2,299 = 95.3 % (declared) | OK |
| ground | 2,252; warp over 49.96 %; 0 double; 6 ties + 3 rim flips | 2,252 | warp over 1,125 = 49.96 %. 0 double-pass ground crossings. The basket rule ⌊(i+1)/2⌋ + ⌊(j+1)/2⌋ holds at 2,243/2,252: the 9 exceptions are the declared 6 ties + 3 rim flips | OK |
| ink-on-ink | 0 | — | 0 crossings where both threads are inked | OK |
| iterate → double-pass crossing | ≤ 2.75 mm | — | max 2.747 mm (step 1) | OK |
| along-thread gap / min piece | 2.40 / 2.59 mm | — | every gap is ≥ 2.40 mm (0 below). Minimum merged piece 2.59 mm | OK |
| min thread ρ | 38.81 mm (0.5 mm paper to the circle ink) | r0 + 1.0 = 38.814 | **38.62 mm** for the ink, because the ±0.2 mm offset passes reach inside the centre-line end. Examples: the blue warp at x 100.8 ending at y 116.78, beside z_0; the crimson weft at y 137.6, x 37.8–57.2. That leaves **0.31 mm** of paper to the circle ink, not 0.5 | **off by 0.19 mm** |
| channel ÷ ρ | 0.234–0.272, except lap 0→1 at 45° (0.148, 5.7 mm) and at 90° (0.183) | at 45°: lap 0 [38.81, 46.53], lap 1 from 52.2, so channel 5.67 mm = 0.147ρ | (by construction; membership matched 100 %) | OK (declared distortion) |
| plot | 14,406 cmds · 2,024 pen-downs · draw 22.0 m · travel 11.2 m | — | 14,406 · 2,024 (blue 700 / crimson 680 / black 644) · 22.01 m (11.25 / 8.65 / 2.11) · travel 11.27 m · layer order 0 → 1 → 2 | OK |

## Lies list
| item (encoding §9) | status |
|---|---|
| No "no equilibrium" | clean. The `+` is labelled `NASH EQUILIBRIUM θ = ψ = 0`, and the title says it repels |
| No turn-taking vocabulary, no L-steps | clean. `AT THAT STEP` indexes the step, not a turn. No then / answers / alternates. The ribbon is a scaled chord polygon, not legs |
| No float, dash or width keyed as a move, loss or speed | clean. The one width claim (`EACH LAP ABOUT 1.5 × WIDER`) keys width to ρ, and it is true (1.48–1.52) |
| No partial flow arc | clean. 156 dashes, r 37.809–37.821, no empty 10° bin, a dash starts at a0 |
| No ink at ρ < ρ_min except the `+`, its labels and the circle | clean on thread centre-lines (38.81). **0.19 mm residual on the ink** (offset passes at 38.62, see Advisory 1). Not a lie, a fabrication tolerance miss |
| No number the sheet does not show | clean. 0.26, 0.74, 1.5, 68 and 1.29 all recompute. 1.29 is where the ribbon crosses the cut edge |
| Window declared, not "the whole run" | clean. The cut edge is the window, `LEAVES THE CLOTH`, and the footer ink is at y ≤ 25 |
| No outline, paper channel or third pen bounding the ribbon (A7) | clean. 0 black segments in the window outside ρ 38.3 |
| No iterate dots, ticks, arrows or axis lines | clean |
| No ink-on-ink | clean (0) |
| One reed pitch, no spacing tone | clean. Every thread is at 2.8 mm pitch, with offsets of 0 / ±0.2 only |

## Scores
- **truth 9.** Every printed quantity recomputes from an independent simulation: the exit at step 68 / r 1.29, the lap ratio, h, r0, the Mescheder sign semantics, the monotone radius ("inside the circle: closer than the start") and the 360° flow circle. The per-step face is a declared rule and is captioned `AT THAT STEP`. Minus 1: `dossier.md` is still absent (S6), and the encoding still carries stale rev-1 numbers beside the rev-1.1 table.
- **encoding fidelity 8.** Membership, face, double pass and basket all hold at 100 % against my own recompute (2,299 / 2,299 / 2,299; ground 49.96 %; 0 empty crossings outside the hole; 0 ink-on-ink). The losses:
  - the rim shift moves lap 0 off the chord polygon by up to 4.8 mm (declared), and the lap 0→1 channel falls to 0.147ρ at 45°;
  - thread ink sits 0.19 mm inside the declared ρ_min;
  - the encoding's step-size channel (ribbon corners) does not render (Advisory 2). It is not claimed on the sheet.
- **insight legibility 8.**
  - It reads: a bare disc with the `+`, bands of face that widen lap by lap, and the crop.
  - `STEP 0` now marks where the run starts, 2.4 mm from z_0.
  - The key names the players and the sign in words, and the title corrects "training converges to Nash".
  - The limits:
    - the saturation mechanism (D ahead → f′ → 0 → crawl), which is the second GAN insight, is invisible;
    - `AT THAT STEP` refers to steps a stranger cannot see;
    - seams still stack on the axes: N laps 0 and 1 on x = 66, W laps 0 and 2 on y = 100.

**VERDICT: PASS** (9 / 8 / 8)

## Mandates
None required (PASS). Three non-blocking advisories:
1. **Rim clearance, 0.31 mm, not 0.5 mm.**
   - Where: the blue double-pass warp at x 100.8 ends at y 116.78, right beside z_0 (100.43, 115.63). The crimson weft pass at y 137.6 (x 37.8–57.2) also reaches ρ 38.62 mm.
   - Measured: the circle's ink is at 37.81, so paper between the inks = 0.82 − 0.50 = 0.31 mm.
   - Expected: ≥ 0.5 mm (rev 1.1 rule 2), which means offset-pass ink at ρ ≥ 38.81 mm. Clip the ±0.2 passes at ρ_min, or set ρ_min for the passes to r0 + 1.2 mm.
   - On Leo, with drift, this is the one place where blue can kiss the black dashes.
2. **The claimed step channel is sub-reed.**
   - Measured: the largest corner sagitta of the chord polygon in frame is 0.88 mm (step 253, chord 31.0 mm at R 135.8) against a 2.8 mm reed quantum. The ribbon's corners cannot be seen anywhere on the sheet.
   - What to change: strike encoding §2 "at 30 cm" and the §4 "discreteness / step size" row, or give saturation a real channel (for example step-owned tie-downs). Either way `AT THAT STEP` and `STEP 68` stay true but uncountable.
   - Not a lie, because the sheet makes no claim about step length.
3. **S6: dossier and stale numbers.**
   - `dossier.md` is still missing.
   - `encoding.md` §4, §4.1 and §5 still state the rev-1 frame as current: 52 mm/unit; (78, 113); exit step 70, r 1.3287 at (9.4, 120.9); ≈196 in-frame iterates; "min thread ρ 39.98".
   - The rev-1.1 row "min thread ρ 38.81 mm" is also wrong for the ink: it is 38.62.
   - Mark the old rows superseded, and write the dossier or a waiver before the vote.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S10 run starts visibly on the rim | **FIXED** (0.19 mm residual) | The ribbon is shifted, not clipped. My membership recompute with lo = max(0.9ρ, 38.814) matches 2,299/2,299. Every one of the 527 in-frame iterates has a double-pass crossing within 2.747 mm (≤ 2.8). z_0–z_4 (ρ 37.81–38.80) sit on the 1 mm ring with ribbon beside them. `STEP 0` is in the hole's upper label group, ink ending at x 98.03, 2.4 mm from z_0. The footer claim moved to the circle (`INSIDE THE CIRCLE: CLOSER THAN THE START`), and it is true because r is monotone. The lap ratio 1.48–1.52 is recorded. Residual: ink clearance is 0.31 mm, not the ≥ 0.5 mm the mandate specified (Advisory 1) |
| S11 double pass = membership, no holes | **FIXED** | 0 single-pass ribbon crossings (2,299/2,299 double). 0 double-pass ground crossings. 0 empty crossings outside the hole (all 608 at ρ ≤ 38.44). Basket over-share 49.96 % over all 2,252 ground crossings. The r05 hole sites and the inverted top-right corner are gone |
| S6 no dossier | **PARTIAL** (unchanged) | The rev 1.1 table recomputes except the ink-ρ row. There is no `dossier.md`, and the stale rev-1 rows are still presented as current |
| S1 title truth, `+` labelled | holding | `THE FIXED POINT REPELS`; `NASH EQUILIBRIUM θ = ψ = 0` |
| S3 hole clean, full circle | holding | 0 thread centre-line inside 38.81. The circle is 360°, starting at a0 |
| S4 simultaneous, no turn-taking | holding | The ribbon is a chord polygon, and there are no turn-taking words |
| S5 stats match the sheet | holding, re-verified for the new frame | `STEP 68 R 1.29` against the recomputed step 68, r 1.29364 at (6.21, 128.20) |
| S8 window declared | holding | cut edges x 10.0–197.6, y 38.4–254.0; footer ≤ y 25 |
| S9 on-top key in words | holding, reworded as ordered | `… D SPOTS THE FAKE AT THAT STEP (ψθ > 0) · … G FOOLS D AT THAT STEP (ψθ < 0)` |

**Truths that held in r05 and changed now:** none regressed. The per-crossing sign rule (r05 2,331/2,331) was deliberately replaced by the per-step owner rule (2,299/2,299), which agrees with the point sign at 95.3 %. The 4.7 % difference is exactly the seam offsets, and it is declared and captioned.
