# Science critique — gan r04 · machine learning (GAN training dynamics, game theory) · 2026-09-28
render: gallery/studio/gan/trials/pp_gan_iterate_v16.png (gcode `gallery/studio/gan/trials/pp_gan_iterate_v16.gcode`: 13,962 cmds, 1,987 pen-down strokes, pens black/crimson/dodgerblue)

Pass 2. `studio/gan/dossier.md` and `encoding.md` still do not exist, so every number below was recomputed from
first principles. Model: Dirac-GAN (Mescheder et al. 2018), f(t) = −log(1+e^−t), f′(t) = 1/(1+e^t),
simultaneous GD θ ← θ − hψf′(ψθ), ψ ← ψ + hθf′(ψθ), h = 0.26.
Sheet frame, measured from the gcode: the crimson `+` is at (78.0, 117.0). The dashed circle has r = 38.47–38.49 mm,
so the scale is 52.0 mm/unit at r0 = 0.74. I fitted the start angle to the float endpoints and got 24.42°, a sharp
optimum. That puts step 0 at (113.04, 132.91), exactly on the dashed circle, and weft x = θ, warp y = ψ.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| equilibrium | — | unique fixed point θ=ψ=0. Flow Jacobian eigenvalues ±0.5i (a centre) | crimson `+` at (78.0,117.0), labelled `NASH EQUILIBRIUM` / `θ = ψ = 0`. Title `THE FIXED POINT REPELS` | OK |
| discrete repulsion | — | GD eigenvalues 1 ± 0.13i, \|λ\| = √(1+h²f′²) = 1.00841/step at r→0 | spiral strictly outward. Tape inner edge on the φ=90° axis at 42.7 / 63.0 / 92.9 / 136.6 mm vs trajectory 41.1 / 61.5 / 91.6 / 135.0 (+1.5 declared clearance) | OK |
| radius ratio per lap | — | 1.514 / 1.510 / 1.511 (laps end at steps 50, 103, 181) | tape at φ=90°: 63.0/42.7 = 1.48, 92.9/63.0 = 1.47, 136.6/92.9 = 1.47 (staircase corners shift it ≤1 mm) | OK |
| h→0 gradient flow | — | d(θ²+ψ²)/dt = 0, so a circle of radius r0 = 0.74 = 38.48 mm | dashed circle r 38.47–38.49 over the full 360° (largest angular gap 3.1°, the dash gap), passes through step 0, labelled `h → 0: THE FLOW CIRCLES` | OK |
| centre hole | — | r never drops below 0.74 | minimum thread radius: crimson 40.33 mm, blue 40.07 mm (> 38.48). Only the `+` is inside | OK |
| `STEP 70 R 1.33 LEAVES THE SHEET` | — | first iterate outside the frame is step 70, r = 1.329, at (9.4,124.9) | caption | OK |
| `H 0.26`, `STEP 0 ON THE CIRCLE R 0.74` | — | h = 0.26 reproduces 163 float endpoints to <0.1 mm. Start r = 0.740 | caption | OK |
| over/under = sign(ψθ) | — | ψθ>0 → warp over, ψθ<0 → weft over | crimson over 175/175 in ψθ<0. Blue over 275/277 in ψθ>0 (the other 2 are the legend swatch). Unders mirror it (560 / 408) | OK (100 %) |
| along-leg float = Σ moves × 52 | — | weft: Σ\|Δθ\|, warp: Σ\|Δψ\| | 163 floats have both ends on iterate coordinates (≤0.1 mm), e.g. warp x=115.65: 132.91→147.41 = steps 0–4 = 14.50 mm. Axis-crossing floats stop at the axis −0.6 mm (weft y=160.05: 32.40 vs Σ 32.68) | OK in gcode |
| turn-square floats | — | HANDOFF: tape width 9.0 | 161 fixed **9.9 mm** floats (10.5 − 0.6 bind). 143 of them start 0.6 mm past a run end. They are 30 % of crimson along-ink (564/1896 mm) and 46 % of blue (1030/2253 mm). **All 161 sit end to end with a run float across a 0.6 mm gap. With a 0.5 mm tip that leaves 0.1 mm of paper** | **NO (perceived)** |
| across-band threads | — | tape width 9.0 | 70 across floats of exactly 9.0 mm. Axis band thickness 9.0–9.2 mm | OK |
| tape coverage | — | every in-frame iterate has tape | 211 in-frame iterates. 21 have no thread within 6 mm. Steps 69 and 74 are at the frame edge (fine). **Steps 86–89** (r 1.42–1.45, (58.5,45.8)→(82.5,42.0)) are an interior break with the nearest type 16.7 mm away. Steps 150–161 and 167–169 (r 2.09–2.33) run under the footer (y 11–39) | **NO** |

## Lies list
There is no dossier §4. Checked against the HANDOFF rule, the r03 lies, and the standard Dirac-GAN misreadings.
| item | status |
|---|---|
| "GANs have no equilibrium" | clean. The title now says it exists and repels, and the `+` is labelled |
| flow orbit shown as a fragment | clean. Full 360° circle, labelled |
| ink inside r0 (never-visited states) | clean. Minimum 40.07 mm vs 38.48 |
| alternation vocabulary (answers / then / alternates) | clean on the sheet (`G MOVES THETA` / `D MOVES PSI`). The L staircase still *looks* turn-based, but no caption says so |
| caption numbers | clean (h 0.26, r0 0.74, exit at step 70 / r 1.33) |
| `ALONG THE TAPE: A FLOAT = ITS PLAYER'S RUN OF MOVES, SUMMED` (footer, y≈13) | **VIOLATED as perceived.** True in the gcode. On paper, every one of the 161 turn-square floats (constant 9.9 mm) merges with the run float before it across a 0.1 mm visible gap, so those floats read as run + 10.5 mm. Example: the warp column at x=115.65 reads 132.91→157.91 = 25.0 mm, while the run is 14.50 mm |
| the tape is the run, end to end, inside the window | **VIOLATED.** 4 on-sheet steps (86–89) have no tape, so the ribbon breaks at x≈50–93, y≈37–47. The path also passes under the footer caption (steps 150–169) |

## Scores
truth 8 · fidelity 7 · legibility 8 · VERDICT: FAIL

This is a large step up from r03. S1 and S3 are closed. The gcode floats are exact to 0.1 mm along every leg, and
the sign channel is 100 %. It fails on fidelity because of what the paper shows. The 0.6 mm binds are finer than
the 0.5 mm tip, so floats fuse with the constant turn squares, and the caption's float = run claim is false for
every float that meets a turn. The ribbon also drops four interior on-sheet steps.

## Mandates
1. **Perceived float = Σ moves (S2 residual).** Measured: 161 turn-square floats of 9.9 mm each, 30 % of the
   crimson and 46 % of the blue along-ink. Every one abuts a run float across a 0.6 mm bind, which leaves 0.1 mm
   of paper at the 0.5 mm tip. So the NE/SW warp columns read as run + 10.5 mm. Example: x=115.65, y 132.91–157.91
   reads 25.0 mm against Σ|Δψ| = 14.50. Expected: any over-thread chain with gaps < 1.5 mm equals Σ moves × 52 ±
   0.5 mm. That means a bind gap ≥ 2 mm (≥ 4× tip) at every run end, and turn squares in a visibly different
   structure (plain-weave pairs, or unders only) so that no float continues into a square. Otherwise restate the
   footer line (y≈13).
2. **The tape must cover every in-frame step, or the window must be declared.** Measured: steps 86–89 (r
   1.42–1.45) sit on the sheet at (58.5,45.8)→(82.5,42.0) with no thread within 6 mm. That is a ribbon break at
   x≈50–93, y≈37–47, between the SW arm and the bottom band. Steps 150–161 and 167–169 (r 2.09–2.33) run
   through the footer type (y 11–39). Expected: 0 in-frame iterates without tape. Either raise the footer / trim
   the plot window so the caption band is outside it (drawn edge + caption `WINDOW`), or lay the tape there.
3. **Key the on-top channel in words, and write the dossier (S6).** Measured: the only key is a formula (footer
   line 3, y≈22: `ON TOP: WARP IF PSI THETA > 0, WEFT IF < 0`). A stranger cannot read what the crossing means.
   Expected: a gloss such as `WARP ON TOP: D SPOTS THE FAKE (ψθ > 0) · WEFT ON TOP: G FOOLS D (ψθ < 0)`. In
   Mescheder's convention the fake logit is ψθ, and D ascends f(ψθ). Also expected: `dossier.md` §4/§7 with the
   numbers in this file (|λ| 1.00841, lap ratio 1.51, exit at step 70 / r 1.329, r0 38.48 mm at 52 mm/unit), so
   the next round is checked against a written source.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 title truth | **FIXED** | title `THE FIXED POINT REPELS`, subtitle `NEITHER PLAYER EVER ARRIVES`, `+` labelled `NASH EQUILIBRIUM θ = ψ = 0`. Recomputed \|λ\| = 1.00841 |
| S2 float = leg | **PARTIAL** | gcode: 163 along-leg floats equal Σ moves × 52 to <0.1 mm (slope 1, intercept 0). Sheet: 161 constant 9.9 mm turn floats fuse with them at a 0.6 mm bind (0.1 mm visible at a 0.5 mm tip). See mandate 1 |
| S3 hole + orbit | **FIXED** | min thread r 40.07 mm > r0 38.48. Circle full 360°, r 38.47–38.49, through step 0, labelled `h → 0: THE FLOW CIRCLES` |
| S4 update vocabulary | FIXED (holds) | no answers / alternates / then on the sheet. Watch item: the L staircase is visually turn-based |
| S5 stats / window note | **FIXED** for the window note | `STEP 70 R 1.33 LEAVES THE SHEET` recomputed exactly (step 70, r 1.329, x 9.4). New: an interior gap and the path under the footer (mandate 2) |
| S6 dossier / encoding | **NOT FIXED** | neither file exists. The HANDOFF `rule:` line was precise enough to verify against (mandate 3) |
| S7 | dropped (r03) | — |
| A13 (art, confirm) | confirmed on the sheet | legend symmetric: `WEFT G MOVES THETA` / `WARP D MOVES PSI` |

Regression check against r03's held truths: the sign rule (100 %), the spiral geometry, and h 0.26 all still hold.
No regressions.
