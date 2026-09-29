# Science critique — gan r02 · machine learning (GAN training dynamics, game theory) · 2026-09-28
render: gallery/studio/gan/current/pp_gan_escape-spiral_v8.png (gcode: gallery/studio/gan/current/pp_gan_escape-spiral_v8.gcode, a4 portrait, 3 pens)

Pass 1 (cold). No `studio/gan/dossier.md`, no `encoding.md`, no `LEDGER.md` exist. **That is a finding in itself:**
there are no §7 check numbers to recompute. The science was reverse-engineered from the gcode instead. The drawn
system was identified as the **Dirac-GAN** (Mescheder et al. 2018), L(θ,ψ)=f(θψ), f(t)=−log(1+e^−t),
f′(t)=σ(−t), vector field v=(−ψf′(θψ), θf′(θψ)). The gcode fits it with residual 1.2e-4 in the step coefficient.

Measurement method: parsed 955 pen-down strokes by `; color=N`. Grouped multi-pass legs into 100 crimson horizontal
(G, θ) and 98 black vertical (D, ψ) legs. Chained them into 13 staircase components and took the iterates
P_k=(V_{k-1}.x, H_k.y) relative to the crimson plus. Then fitted c_k = −Δθ/ψ_k = Δψ/θ_k = h·f′(θ_kψ_k) over 73
measured steps and forward-simulated 578 steps against every drawn leg.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| equilibrium (crimson plus) | — | (0,0) | plus centre (116.40, 187.28) mm. Also the exact centre of the blue circle fit (116.4001, 187.2800), and the centre that makes −Δθ/ψ = Δψ/θ hold to 0.13 % | OK |
| scale | — | — | 31.00 mm per unit (free fit) | — |
| update rule | — | simultaneous GD: Δψ uses θ_k | −Δθ/ψ_k vs Δψ/θ_k agree to 0.13 % median, 0.75 % max (73 steps). Δψ/θ_{k+1} (alternating) is off by 10–25 %. Per-step radius ratio equals √(1+c²) to 2.4e-4 | simultaneous, **but captioned as alternation** (see lies) |
| step size h | — | sheet prints "h 0.25" | **h = 0.2600**: fit rms 1.2e-4 at h=.26 vs 5.4e-3 at h=.25 (44× worse). Direct check: c = 0.2569 where f′ = 0.988, so h = 0.260 | **VIOLATED** |
| start radius r0 | — | 0.74 | blue circle R = 22.94 mm → 0.740. Trajectory start fit r0 = 0.740 at 24.4° | OK |
| h=0 orbit | — | continuous flow conserves r. RK4 to t=200: r = 0.740000 | dashed blue circle r = 22.935–22.946 mm (0.740) through the start | OK |
| steps per slow-quadrant (θψ>0) crossing | — | sim h=.26: 10*,15,15,18,23,36,79,315 (*first partial, unlabelled) | labels 15,15,18,23,36,79,315, in the correct rings and quadrants | OK at h=.26. With the printed h=.25 they would be 15,16,18,22,33,66,210 |
| total steps / final r | — | sim h=.26: r(578) = 3.526, r ≥ 3.54 at step 579. With h=.25: 463 steps to 3.54 | "578 STEPS · r 0.74 TO 3.54". The last iterate P578 sits at x = 205.5 mm, **outside the 200 mm drawable edge**. Its G leg is clipped at x = 199.5 and its D leg is absent. The last visible iterate is P577 at r = 3.41 | PARTIAL |
| simultaneous growth factor | — | √(1+h²f′²): 1.0084/step at f′=½, max 1.0332 | measured ratios 1.0052–1.0133 on the inner rings, matching c | OK |
| alternating GD from the same start (control) | — | r ∈ [0.700, 0.747] for 20 000 steps: bounded, never escapes | — | this is what "D ANSWERS" would draw |

## Lies list
No dossier §4 exists, so this list was built from the sheet's own claims.

| item | status |
|---|---|
| "G PUSHES THETA / D ANSWERS PSI" plus the staircase plus the Kandinsky "forces in alternation" lineage | **VIOLATED**. The whole spiral field is affected. Each D leg's length is hθ_k·f′, the *old* θ, so the updates are simultaneous. The L-corner (θ_{k+1}, ψ_k) is never a state of the system. If D really answered G's new θ (alternating GD), the trajectory would stay in r 0.70–0.75, inside the first ring, forever. The sheet draws divergence and labels it with the vocabulary of the non-divergent method. |
| Title "NO FIXED POINT" | **VIOLATED**, lower-left title block. v(0,0)=0: the fixed point exists and is drawn as the crimson plus at (116.4, 187.28). It is *repelling* under simultaneous GD (\|λ\| = √(1+h²f′(0)²) = 1.0084 per step), not absent. The subtitle "NEITHER PLAYER EVER ARRIVES" is correct. |
| "h 0.25" (lower-right stats) | **VIOLATED**. Measured h = 0.260. The printed h is also inconsistent with the printed step counts and "578". |
| "r 0.74 TO 3.54" | PARTIAL. r0 = 0.740 is on the sheet. 3.54 is not: step 578 is clipped at the 199.5 mm margin (lower right, y≈107.7), so the visible maximum iterate is r = 3.41. |
| black hairline = "f′ NEAR 0 · THE CRAWL" | **VIOLATED**, inner rings. 481 of 578 steps are drawn as hairline. 37 of them have f′ ∈ [0.45, 0.55], at the axis crossings: 70–114°, 165–208°, −110 to −67°, −12 to 23° on rings 1–3. There the hairline replaces a real 3.2–3.9 mm G or D leg (e.g. step 10: G leg 3.20 mm, D leg 0.02 mm). The switch rule is "shorter leg < ~1.2 mm", not f′ ≈ 0. Staircase legs go down to f′ = 0.19, so the channel is not monotone in f′. |
| leg weight (1/2/3 passes) | undeclared. Passes bin f′: 1 ≈ 0.19–0.33, 2 ≈ 0.30–0.80, 3 ≈ 0.69–1.0. That is a real quantitative channel, but the legend never says so. A stranger reads it as decoration. |
| dotted "knives" on θ=0 and ψ=0 | clean. Full-sheet dotted lines through the plus at x=116.4 and y=187.28, where θψ changes sign and each player's gradient flips. |
| blue orbit | clean. It is the exact h→0 circle through the start. |
| plus mark | clean in position. It has no legend entry, which is what lets the title contradict it. |

## Scores
- truth: **4**. The dynamics are drawn to 1e-4 precision, but three captions are false: the alternation language on a simultaneous system (the misconception the piece should correct, inverted), "NO FIXED POINT", and "h 0.25".
- encoding fidelity: **6**. Positions, step counts and the orbit are exact. The hairline channel carries two meanings under one legend line, the f′ weight bins are undeclared, and the final step is clipped off the drawable area.
- insight legibility: **6**. The widening spiral against the blue h=0 circle and the exploding step counts land for a stranger. A scientist is told the wrong mechanism (alternation, and no equilibrium).

**VERDICT: FAIL**

## Mandates
1. **Update rule vs caption: the spiral field, the legend "D ANSWERS PSI", and the lineage.** Measured: Δψ_k/θ_k = −Δθ_k/ψ_k to 0.13 % median over 73 steps (simultaneous GD). Δψ/θ_{k+1} misses by 10–25 %. Expected, if the caption were true (alternating GD, h=.26, same start): r stays in [0.700, 0.747] for 20 000 steps and never leaves the blue circle. Either re-caption as simultaneous ("G AND D STEP AT ONCE — THE CORNER IS NEVER VISITED"; the diagonal is the true step, the L-legs are its components), or keep the alternation story and draw the alternating orbit as the bounded contrast. Do not let the staircase claim an alternation the numbers do not have.
2. **Title and stats block (lower left and lower right).** "NO FIXED POINT": measured, a fixed point at (0,0), drawn as the crimson plus at (116.4, 187.28) mm. Expected: it exists and repels, with \|λ\| = √(1+h²/4) = 1.0084 per step. Retitle (e.g. "THE FIXED POINT REPELS") and add the plus to the legend as "EQUILIBRIUM". "h 0.25": measured h = 0.260 (s = 31.00 mm/unit, rms 1.2e-4). Print 0.26, or re-run at 0.25 and re-letter every step count (0.25 gives 15/16/18/22/33/66/210 and 463 steps). "r … TO 3.54": step 578 ends at x = 205.5 mm, past the 200 mm edge. Its G leg is clipped at 199.5 and its D leg is missing. Fit the spiral so P578 lands inside the margin, or stop at the last drawn iterate and print its r (3.41).
3. **The hairline channel on rings 1–3 at the four axis crossings.** Legend "f′ NEAR 0 · THE CRAWL". Measured: 37 hairline steps with f′ = 0.45–0.55, where a 3.2–3.9 mm leg is suppressed. Expected: hairline only where f′ is small (the QI/QIII crawls at f′ = 0.007–0.19 on rings 4–7). Keep the legs at the axis crossings, even when one leg is near 0 mm, or split the legend ("LEG < 1 mm" vs "CRAWL"). Also key the pass count: 1/2/3 passes = f′ bins ≈ <0.3 / 0.3–0.75 / >0.75, currently unexplained.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | no LEDGER.md for gan. This is pass 1. |
