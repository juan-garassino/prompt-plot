# Ledger — gan
**Best so far:** **r07** — art 7.57/7 · sci 9/8/8 — `~/Downloads/pp_gan_iterate_v34.png` (gcode `~/Downloads/pp_gan_iterate_v34.gcode`). Science PASS, art FAIL (avg 7.57 < 8). It beats r05 on every tie-break key:
- verdict: one PASS against none;
- art min: 7 vs 6;
- sci min: 8 vs 7;
- art avg: 7.57 vs 7.14.

**Route:** designer → r08, parent r07 (best so far and latest). The rules were applied in order:
- **Rule 1** does not fire: art FAILs.
- **Rule 2** does not fire.
  - A20 was raised by art r05 and first put on a work order in r07, where it came back PARTIAL. That is one not-fixed round, not two.
  - A17 regressed for the first time.
  - A4 improved (6 → 7), above the ledger's translator threshold of ≤ 6.
  - A5 and A6 are PARTIAL for new causes: the hole's type, and the first-turn fusion. Those causes are now carried as A23, A17 and A20.
- **Rules 3–5** do not fire: no UNWORKABLE, best-so-far moved (r05 → r07), and r07 is better than its parent.
- **Rule 6** does not fire yet (see the cap below).

**Round cap:** 5 designer rounds per encoding (DESIGN_RUBRIC). Encoding rev 1, with its amendments 1.1 and 1.2, has used 2 (r05, r07). r08 is 3 of 5. The **curator's relaunch** of batch 1 granted 2 more rounds: r07 and r08. **r08 is the last round of the relaunch.** After r08 is critiqued, route to `vote` with the best round and an honest note, even if art still FAILs. Any mandate that is then NOT FIXED for the second consecutive round (e.g. A20) is recorded as a translator question for a later batch, not run now.

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | Dirac-GAN saddle: the exact V = f(ψθ) as a 3D polar mesh, with the GDA run scattered over it as occupancy-thinned G/D dashes. The equilibrium is a paper hole with a crimson `+` | `gallery/studio/gan/current/pp_gan_v1.png` | — | — | unscored benchmark | Never run through the critic pair. Source of the DESCRIPTION.md Keep and Weak lists |
| r02 | r01 | escape-spiral (Kandinsky): the run in plan view as a θ/ψ-leg staircase, with a crawl hairline, knives, the full h→0 circle, and a giant title | `gallery/studio/gan/current/pp_gan_escape-spiral_v8.png` | 6.0/4 | 4/6/6 | FAIL · rank 6 | A phase-plane figure with turn-taking vocabulary. Kept on disk as the `escape-spiral` flavour |
| r03 | r01 | two-players-interlaced (Albers): the run as a woven tape, G = crimson weft, D = blue warp | `gallery/studio/gan/current/pp_gan_two-players-interlaced_v10.png` | 6.57/6 | 6/5/6 | FAIL · rank 5 | Centred target, float ≠ leg, orbit only an arc. Superseded by r05's full cloth |
| r04 | r03 (+ r02's circle) | iterate: outward L-blocks of summed moves, turn squares, `+` at (78, 117), 52 mm/unit | `gallery/studio/gan/trials/pp_gan_iterate_v16.png` | 6.29/6 | 8/7/8 | FAIL · rank 4 | Tape broke into rubble (A1), and the flip test failed (A7). Sent to the translator → `encoding.md` rev 1 |
| r05 | r04 | iterate on encoding rev 1 (Red Meander proper): the whole window is cloth, with one reed 2.8 mm. The ribbon is the chord polygon × [0.9, 1.1], its face is sign(ψθ) per crossing, with double-pass floats on a 2/2 basket ground | `gallery/studio/gan/trials/pp_gan_iterate_v24.png` | 7.14/6 | 9/8/7 | FAIL · rank 2 | A1 and A7 fixed, 0 ink-on-ink. Weaknesses: crosshair seams on the axes, steps 0–9 invisible, a float riding the x = 200 cut, a loud title |
| r06 | r04 (name only) | wildcard, De Stijl / *Broadway Boogie Woogie*: the run squared into a lane spiral, 6.5 mm cells blue / crimson / gold | `gallery/studio/gan/current/pp_gan_wildcard_v7.png` | 6.57/6 | 8/7/8 | FAIL · rank 3 · kept as the `boogie` flavour | Undermassed, over-keyed, order undocumented. Not continued. Its mandates are parked below |
| **r07** | r05 | **iterate on rev 1 + rev 1.1**: each ribbon cell takes the face of the step that owns it (ψ_kθ_k), so the seams lean off the axes. The ribbon is shifted at the rim (full 0.2ρ from ρ_min = r0 + 1 mm), with `STEP 0` beside z_0. Re-cropped at (66, 100) @ 51.1 mm/unit with edges at mid-pitch. Title 118 mm flush left, top-right cream | `~/Downloads/pp_gan_iterate_v34.png` | **7.57/7** | **9/8/8** | art FAIL · **sci PASS** · **rank 1 (best)** | See the r07 detail below |

**r07 detail.**
- Held:
  - S10, S11, A21 and A22 are all FIXED.
  - 527/527 iterates are within 2.75 mm of a double-pass crossing.
  - Membership, face and double pass are 2,299/2,299; the basket is 49.96 %; there are 0 empty crossings outside the hole and 0 ink-on-ink.
  - 3 layers: blue 48 / crimson 43 / black 29 min ≈ 2 h 00, 14,406 cmds.
- Cost:
  - The rim shift collapsed the lap 0→1 channel at 45° and 90° (5.7 mm, 0.148ρ). A17 regressed, and laps 0 and 1 fuse into one blue wedge NE of the hole.
  - The N seams of laps 0 and 1 still share x ≈ 66.6 (3 + 5 float ends), and science also notes W laps 0 and 2 on y = 100.
  - `h → 0` moved up beside `STEP 0`, so the disc is spent on type.
  - The offset-pass ink reaches ρ 38.62: 0.31 mm of paper to the dashes, not 0.5.

**Ranking:** r07 > r05 > r06 > r04 > r03 > r02. r05 stays on disk as the parent state of rev 1. There is no merge: r07 already contains everything r05 had that worked.

## Mandates
| id | raised | by | mandate | status | closed |
|---|---|---|---|---|---|
| A17 | r04 · **r07** | art (M1) + sci r07 fidelity | **The lap 0→1 channel must be reopened on N/NE.** Lap 0's double-pass outer edge and lap 1's inner edge are separated by ≥ 3 clear basket crossings (≥ 8.4 mm), with no float tail through the channel. Channel ÷ ρ must be 0.22–0.28 on all 8 rays. Look at x 85–125, y 135–175. S10's 2.8 mm test must not be undone. **Lead's resolution of A17 vs S10:** the r06 SYNTH asked for "full 0.2ρ width from the rim", but the critic's own S10 test is the 2.8 mm test, so full width yields. Lap 0 is `[max(0.9ρ, ρ_min), max(1.1ρ, ρ_min + w_floor)]`, with w_floor ≥ 1.5 pitch (4.2 mm). The outer edge stays on the true chord polygon, the inner edge is pinned at the rim, and the ribbon grows out of the hole. This is recorded as rev 1.2 | **regressed** r07 (fixed r05) → r08 #1 | |
| A20 | r05 | art (+sci r07 legibility) | **Kill the crosshair seams.** On each of the four axis half-lines (x = x_eq N/S, y = y_eq E/W), a straightedge touches ≤ 3 consecutive float ends **across all laps combined**. r07: N laps 0 + 1 give 3 + 5, and W laps 0 + 2 share y = 100. **This is fixed by the data, never by a fake offset.** Search a0 (seed) for a start where no two laps' first post-axis iterates quantise into the same half pitch on any axis, while S10, A21 and the new A17 still hold. Report the search table. Scale cannot separate the offsets, because they scale with mm/unit | **PARTIAL** r07 (E/S lean clear; N and W stack) → r08 #2 | |
| A23 | r07 | art (M3 + grid note) | **The hole goes back to the `+`.** `h → 0: THE FLOW CIRCLES` returns to the lower rim, centred on x_eq, with its baseline ≈ 6 mm above the circle's bottom. `STEP 0` stays beside z_0. `NASH EQUILIBRIUM` / `θ = ψ = 0` becomes one tight pair under the `+`. Test: at a 1/8 downsample the `+` is the darkest mark in the disc, no label is within 8 mm of the rim at z_0's angle except `STEP 0`, and the upper-right quadrant of the disc is empty paper. Also: the footer's flush-right edge moves to the cloth's right cut edge (197.6 in r07, or wherever r08's window ends): one right edge, not two 2.4 mm apart. Folds in A5 | open → r08 #3 | |
| S12 | r07 | sci (Advisory 1) | **Rim ink clearance ≥ 0.5 mm.** The ±0.2 mm offset passes reach ρ 38.62 (the blue warp at x 100.8 ending at y 116.78 beside z_0, and the crimson weft at y 137.6). That leaves 0.31 mm of paper to the dashes. Clip every pass, offsets included, at ρ_min, so that ink ρ ≥ r0 + 1.0 mm. Measure it on the gcode. This is fabrication: on Leo, with drift, this is where blue kisses black | open → r08 #4 | |
| S6 | r02 · r03 · r04 · r05 · r07 | science | **Dossier and stale numbers.** The vote follows r08, so this can no longer be deferred. Do all of the following: write `studio/gan/dossier.md` (model, sign semantics, all check numbers with how they were computed) or an explicit waiver line in r08 NOTES naming who accepted it; mark encoding §4, §4.1 and §5's rev-1 frame rows `SUPERSEDED by rev 1.1/1.2`; strike §2 "at 30 cm" and the §4 "discreteness / step size" row (Advisory 2: max corner sagitta 0.88 mm < 2.8 mm reed); append `## Revision 1.2` (the A17 lap-0 rule, the S12 clip, the final a0, all check numbers at the r08 frame) | PARTIAL (encoding rev 1.1 exists; no dossier; stale rows) → r08 #5 | |
| A4 | r01 (W5) · r03 · r04 · r05 · r07 | art | Shaped negative space | PARTIAL, improving (6 → 7 in r07): the hole plus the top-right cream. A23 gives the disc back as paper. The translator threshold (≤ 6) was not hit. Deferred: carried by A23 | |
| A5 | r02 · r03 · r04 · r05 · r07 | art | Accent pen scarce and loud | PARTIAL: the title is fixed, but the `+` competes with its own labels → folded into A23 | |
| A6 | r02 · r03 · r05 · r07 | art | Weight advances outward | PARTIAL: E/S/W lean outward, but the N straightedge and the fused first turn stall the eye → closes with A17 + A20. Not carried separately | |
| S10 | r05 | science (M1 + M3 merged) | Run starts visibly on the rim: every in-frame iterate has a double-pass crossing within 2.8 mm, `STEP 0` beside z_0, the footer disc claim true | **fixed** (sci r07: 527/527, max 2.747 mm; art r07 confirms). **Preserve under A17's lap-0 rule.** The ink residual is split out as S12 | r07 |
| S11 | r05 | science (M2) | Float weight 100 % of ribbon, no holes, basket 50 ± 1 % | **fixed** (sci r07: 0 single-pass ribbon, 0 double-pass ground, 0 empty outside the hole, 49.96 %) | r07 |
| A21 | r05 | art | Crop through or clear, never ride a cut edge | **fixed** (art r07). Watch: lap 0 clears the left edge by only 6.2 mm, and lap 1's exit tip shows 1–2-crossing stubs at x 10–14. A new a0 re-crops, so re-run the full crop scan | r07 |
| A22 | r05 | art | Demote the title (≤ 120 mm, flush left, the top-right cream) | **fixed** (art r07: 118 mm; at 1/8 the ribbon and hole outweigh it) | r07 |
| S9 | r04 | science | Key the on-top channel in words | fixed, holding, reworded to `AT THAT STEP` (sci r07) | r05 |
| S1 | r02 · r03 | science | Title truth; the `+` labelled | fixed, holding (sci r07) | r04 |
| S2 | r03 · r04 | science | Perceived float = Σ moves | fixed, holding (sci + art r07) | r05 |
| S3 | r03 · r02(art) | science+art | Hole with no thread inside; full labelled h→0 circle | fixed, holding (sci r07: 156 dashes, 360°, dash at a0) | r04 |
| S4 | r02 | science | Simultaneous updates, no turn-taking | fixed, holding | r04 |
| S5 | r02 · r03 | science | Stats match the sheet | fixed, holding, re-verified (`STEP 68 R 1.29`) | r04 |
| S8 | r04 | science | Window declared | fixed, holding | r05 |
| A1 | r01 · r03 · r04 | art | One continuous body per lap | fixed, holding (art r07). The fusion of laps 0 and 1 is carried as A17, not A1 | r05 |
| A7 | r03 · r04 | art | Figure carried by on-top, not silhouette | fixed, holding (art r07 flip test PASS) | r05 |
| A18 | r04 | art | Cloth, not ladders | fixed, holding | r05 |
| A19 | r04 | art | Title cap-tops, title end axis, `min_G max_D V(D,G)` | fixed, holding | r05 |
| A2 | r02 · r03 | art | Off-centre, hard crops | fixed, holding (art r07 tension 8) | r04 |
| A3 | r03 | art | Plot craft | fixed, holding (r07: 14,406 cmds, 2,024 pen-downs, min inked 2.59). Art watch: double-pass floats 0.4 mm apart with a 0.5 mm tip may furrow. Check on the first physical test | r04 |
| A13 | r01 (W9) | art | Symmetric player labels | fixed, holding | r04 |
| A14 | r01 · r02 | art | Declare depth or flatness | argued and accepted: flat weaving canon (art r07 depth 8) | — |
| A15 | r02 | art | No figure furniture | dropped as a mandate, kept as a Do-not | r03 |
| A16, S7, A8–A12 | r01–r02 | — | as recorded earlier | dropped/fixed | r02–r03 |

### Parked — science Advisory 2 (not a mandate)
The saturation mechanism (D ahead → f′ → 0 → crawl), GAN's second insight, has no channel on the sheet. The step-size channel the encoding claimed is sub-reed. The claim is struck under S6. Giving saturation a real channel (e.g. step-owned tie-downs) would be a rev 2 question for a later batch. It must not be attempted in r08.

### Parked — `boogie` flavour (r06), not carried
These would be the work order only if Juan asks for the De Stijl flavour:
- **lane width grows per lap** (≤ 6.5 → ≥ 13 mm) and the black flow square is demoted to a single rule (art);
- **crop or clear:** no lane end 1–6 mm from an edge; resolve the square/step-0 near-miss (art);
- **footer ≤ 4 lines** and redrawn lattice X / S (art);
- **gold = "no step" only:** equal-angle cells, 0 steps in gold (sci);
- **declare** the 42 beats under the footer (sci);
- **sides centred** on the crossing radius, and the order written into an encoding (sci).
