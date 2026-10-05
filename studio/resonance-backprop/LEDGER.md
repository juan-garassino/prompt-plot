# Ledger — resonance-backprop
**Best so far:** **r04** (the eligible best), art 5.71/4 · sci 4/3/6.
- Plate render: `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.png`. Plate gcode: `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.gcode`.
- r04 is r01 with v5's field rebuilt, J1 dots and stream order. It is the first critiqued round that honours J2.
- r03 still leads on raw score (art 5.71/4 · sci 7/6/6), but it is **J2-ineligible**: its thesis deletes what Juan bound. Juan's mandates outrank the score order, so r03 cannot be best for this slug. It stays a flavour.

**Route:** designer. Next is r05, with parent r04.

**Round cap:** 5 designer rounds per encoding (DESIGN_RUBRIC). Rounds used: r02, r03, r04. **r05 is round 4 of 5.** If r05 FAILs, r06 is the last designer round, and after it the plate goes to vote with an honest note.

**Flag for Juan (three items):**
1. **v5 vs v8 field.** The lead picked v5's dotted field, and r04 rebuilt it from measurements. Juan can overrule.
2. **Science cannot PASS on this thesis while J2 stands.** The r04 science critic measured wrong algebra everywhere it could:
   - 5 keys against 4 values;
   - 3-row gradients for 5-row Q and K;
   - Z at 2.75× the convex bound of the V rows;
   - ∂L/∂V that is not a_j·∂L/∂Z;
   - A derivable from nothing drawn.

   This is all inherited from the traced reference packets (r01). Fixing it adds rows and recomputes every packet's shape, and J2 forbids exactly that.
   - These findings are parked as **S1/S3/S4 `open — blocked by J2`**.
   - The critic asks Juan directly: does "keep the original" cover the *traced* packet shapes, or may they be recomputed in place (same positions, pens and look class)?
   - Only the comb (S2) and the one reversed arrowhead are fixable inside J2.
3. **Packet braids (A2) and the dead foot (A6)** stay blocked by J2 until Juan rules.

**Family note (resonance · resonance-ffn · resonance-backprop, reworked in parallel).**
- Keep the shared grammar: Q crimson / K blue packets, the two-source field, V goldenrod, Z green.
- The r04 art critique found the continuous dot turns a *texture* into mass when texture and leader share one mark size. That is the same failure as resonance A13 ("stipple caps flood to mud") and resonance-ffn A4b.
- The **two-class dot** here gives the family its answer:
  - leader dots are 0.30 mm circles at 1.0 mm (r10's DOT_R);
  - field/texture dots are single pen touches at their own positions.

  Recommend the sibling leads adopt the same split, so the three plates hang as one series.

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | reproduction of `ref/reference.png` (v1–v8) | `gallery/studio/res_backprop/current/pp_res_backprop_v5.png` (Juan's) · `…/v8.png` (= code on disk) | — | — | pre-workflow; Juan REWORK on v5: "KEEP THE ORIGINAL … only dot continuity" (J2) | THE DESIGN. v8 gcode: 4,053 pen cycles (layer 0 769 · 1 766 · 2 578 · 3 431 · 4 1,509 strokes), 11.39 m draw, 11.90 m travel (105 %), ≈ 165 min on the PLOT_JOBS Leo model |
| r02 | r01 | the fold (abstract): four crest families mirrored about one green loss line, Q/K colours swapped below; lineage LeWitt *Arcs, Circles & Grids* | `gallery/studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.png` | 5.71/4 | 5/5/4 | FAIL · **J2-ineligible** | Deletes every packet, halo, leader, the title and the frame (J2 REGRESSED). Craft gains: 334 cycles, 11 % travel. → flavour `the-fold` |
| r03 | r01 | gradient-as-phase (mechanism): one black two-source field, ∂L/∂Q / ∂L/∂K crests on-crest or λ/2 off by the sign of g; lineage Riley *Current* | `gallery/studio/res_backprop/current/pp_res_backprop_gradient-as-phase_v9.png` | 5.71/4 | 7/6/6 | FAIL · score leader · **J2-ineligible** | Deletes the packet blocks, fans, halos and the backward band (J2 REGRESSED). Sign rule exact. → flavour `gradient-as-phase` |
| r04 | r01 | iterate: r01 with v5's field measured and rebuilt (22×2 dotted crest rings + 3×2 halo ellipses), J1 dots everywhere, marks→sheet passes (`_realize`, `_order`), `plate.py` stream-order gcode; lineage Helmholtz *On the Sensations of Tone* (1863) | `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.png` (+ `_plate.gcode`, `_nib_{subtitle,densest,comb,dq_fan}.png`) | 5.71/4 | 4/3/6 | FAIL · **eligible best** | J2 kept: the critic's element audit finds nothing removed. J1's mark is right: 0.30 mm circles, 1.00 mm median, 0 coincident. Lineage FIXED, type FIXED, comb gate FIXED. Craft regression vs v5: every field dot is full leader size, so the band inks as dark as the bullseyes (tone inverted vs the reference). Leaders stab into packets; V loops cross the Z diamond. Budget: 5,652 cycles · 14.11 m draw · 11.69 m travel (83 %) · 230 min. Black batch 0 spans 190×158 mm; blue has one 106 mm hop and crimson one 138 mm hop. Science: the drawn wave physics is exact (d = 59.000 L, rings to 5 µm), the comb is one source's rings only, and the attention algebra is inherited-wrong (blocked by J2) |

**Ranking after r04.**
- **Eligible for this slug:** r04, the only critiqued J2-honouring round.
- **Ineligible:** r03 > r02, as flavours.
- **Regression rule vs parent r01:** r01 was never critiqued, so there is no score regression to measure.
- The art critic names one regression against v5: the hero's **light tonal field** went heavy. It is recorded as preserve-mandate A7: v5's haze tone must come back without losing a dot.
- **Translator rule not triggered:**
  - J1 was PARTIAL in r03, but r03 was a parallel, J2-ineligible flavour with 88 dots, not r04's parent line. In r04 the mark itself is FIXED; only the converging clause is open.
  - A9 went from NOT FIXED (r03, a different plate) to PARTIAL (r04), with measured progress: travel 105 % → 83 %, 5 single-entry layers.
  - Both are ordering and weight problems, not encoding problems.
- **Plateau rule:** the eligible best moved r01 → r04, so no plateau.

## Flavours (house law: one subject, several flavours)
- **r03 gradient-as-phase** is kept on disk. It is the strongest alternative and a candidate for its own slug (`res-backprop-phase`, curator to decide). Its mandates travel with it:
  - art: phase jog, off-centre crop, one-sweep batching, type ≥ 4 mm caps;
  - science: a caption that states the sign rule, A drawn, patch extent ∝ |g|, a verifiable colophon.
- **r02 the-fold** is kept on disk as a weaker second flavour. Its science is broken: beads where QKᵀ = 0, a seam break, a decorative Z.

## Mandates
| id | raised | by | mandate | status | closed |
|---|---|---|---|---|---|
| J1 | 2026-09-28 (DESCRIPTION Weak "DOTTED LINES", FEEDBACK) | Juan | Dotted lines read as continuous dots. Every dot is ONE round dot of one fixed size per class (a pen touch or tiny closed circle, never a micro-dash). Centre pitch 0.9–1.1 mm, end-anchored, the same pitch family-wide. Converging dotted paths sit ≥ 2 pitches apart or are phase-locked. Judged at real nib width. Never trade dots for dashes or hairlines; plot time may grow | open. r04 PARTIAL (art) / measured OK (science): the mark is fixed (0.30 mm circles, 1.00 mm median, 0 coincident, 0 micro-dashes). The converging clause is missed at the ∂L/∂Q / ∂L/∂K arrowhead fans (heads ≈ 1.6 mm apart, touching) and in 371 black texture pairs < 0.8 mm. Both are carried inside A7 and A14. Only Juan closes | |
| J2 | 2026-09-28 23:39 (FEEDBACK REWORK on v5) | Juan | KEEP THE ORIGINAL: r01 is the design. Keep EVERY element: all wave packets, the dotted halos/ellipses round the field, the scattered dots, the leaders and arrowheads, the rail, the frame, all five pens. Do not remove, thin or replace anything to save plot time. (The note's "MoE / six pens" wording is the resonance sibling's; here it is five pens, no MoE) | open. r02 REGRESSED, r03 REGRESSED, **r04 FIXED pending Juan** (the art critic's element audit finds nothing removed). Only Juan closes | |
| A1 | DESCRIPTION Weak [concept] | art | Schematic: arrowed fans, stacked fractions, labelled stages (≤ 3) | dropped: superseded by J2. Answered by the r02/r03 flavours | r03 |
| A2 | DESCRIPTION Weak [craft] + it-1 · r04 art | art | Packet amplitude > row pitch braids rows into knots (Q, K, V, ∂L/∂Q, ∂L/∂K); cap at 0.45 × pitch | open — **blocked by J2**. r04 NOT FIXED (untouched, per SYNTH). Needs Juan. Not a translator count | |
| A3 | DESCRIPTION Weak [craft] + it-2 | art | Central comb is a near-solid black lozenge | **fixed**. r04 art critic confirms the `_nib_comb` crop shows ≈ 1.2 mm pitch with ≈ 0.85 mm of paper, a striped lozenge. Re-check if S2 changes the comb's curves | r04 |
| A4 | DESCRIPTION Weak [hierarchy] | art | Z axis wider than the hero | dropped: superseded by J2 | r03 |
| A5 | DESCRIPTION Weak [tension] | art | Mirror-symmetric, centred title/Z | dropped: superseded by J2 | r03 |
| A6 | DESCRIPTION Weak [space] + it-3 · r04 art | art | Dead foot v 0.89–0.97; move the composition down | open — **blocked by J2** (composition move). r04 NOT FIXED. Needs Juan | |
| A7 | DESCRIPTION Weak v5 [space] · **r04 art M1 (merged, stricter)** · r04 art regression vs v5 | art | **Two-class dots in the hero band, restoring v5's haze without losing a dot.** Every field and texture dot (the dotted crest arcs, the three halo ellipse pairs and the scatter) becomes ONE pen touch (≈ nib diameter, no drawn circle). Keep every dot's count and position. Leader/fan/dropline/guide/envelope dots stay 0.30 mm circles. The 371 black texture pairs < 0.8 mm are slid apart ALONG their own crest circle or ellipse to ≥ 0.8 mm, never off the locus (science: the field dots are on-locus to ±0.03 mm) and never deleted. The halos still pass under the lowest Q/K packet rows, so they yield there by the existing clearance. Test: at arm's length the bullseyes + comb are the darkest marks in x 40–170, y 165–215; the halo reads a clear step lighter than the Q/K leaders; the densest-scatter nib crop has no touching doublets | open. r04 PARTIAL: dots round, labels clear, but same size for both classes, so the band went black | |
| A8 | DESCRIPTION Weak v8 [craft] | art | v8 dashed crest arcs break into noise | dropped: superseded by J1 + the v5-field decision | r03 |
| A9 | curator note 2026-09-28 · DESIGN_RUBRIC § PLOTTABLE · Juan 2026-09-29 ("batch correctly … colour changes correctly … more than 4 colours, longer session") · r03 art M3 · **r04 art M3 (merged)** | curator + Juan + art | Plot discipline. Five pens, each ONE clean layer, never re-entered, light→dark. Strokes spatially ordered and reversal-aware so every 400-stroke batch is one contiguous sheet region. Black batches ≤ ~100 × 80 mm each; the sparse furniture (crosses, rail, title) is ordered as its own frame loop at the start or end of black, not smeared across a content batch. Black travel ≤ 4.3 m (r04: 5.30 m). This replaces the critic's "≤ 0.6 × black draw", because pen touches shrink the draw denominator, which makes that ratio meaningless. No in-layer hop > 80 mm except layer entry and, per pen with two ink clusters that have no ink between them (blue and crimson: the upper block and the lower block, ≥ 104 mm vertical gap), exactly ONE inter-cluster hop within 10 mm of the minimum cluster-to-cluster distance (crimson r04: 138 mm, ~30 mm over). No invisible cycles. Chained glyphs. NOTES: per-layer cycles, draw, travel and minutes plus the total on the PLOT_JOBS model, the batch table with bbox per batch, and the session plan | open. r04 PARTIAL: 5 layers entered once, 83 % travel, 230 min stated. Black batches up to 190 × 158 mm; black travel > draw; crimson hop 30 mm over its minimum. The single inter-cluster hop is **argued (accepted)**: there is no ink of that colour between v 0.32 and v 0.67, so no order avoids it | |
| A10 | curator note · DESIGN_RUBRIC § LINEAGE | curator | Name ONE movement + ONE real work and the ORDER it lends; declare depth | **fixed** (r04 art critic confirms): Helmholtz, *On the Sensations of Tone* (1863), stacked partials → one compound wave; flat, declared | r04 |
| A11 | r03 art (dim 5, Q5) | art | Small type open at 0.35 mm nib | **fixed** (r04 art critic confirms `_nib_subtitle` open) | r04 |
| A12 | house law "never arrows" vs r01 NOTES | lead | Arrowheads in the backward band | argued (accepted): they mark gradient direction, not projection | r03 |
| A13 | r04 art (dim 2) | art | `QK T` in `A = softmax(QKᵀ/√d_k)` has a visible gap before the superscript. The softmax label sits under the halo rim with no set gap | open, low. Deferred to r06 (mandate cap). A kerning fix ≤ 1 mm is allowed in r05 if it is free | |
| A14 | **r04 art M2** + r04 science (opposing arrowhead) + J1 converging clause | art + science | **No leader enters a packet.** Every ∂L/∂Q and ∂L/∂K arrowhead stops ≥ 1.5 mm outside its block's outer dotted envelope (crimson x 30–60, y 45–62; blue mirrored x 150–180). Converging heads sit ≥ 2 mm apart with no two triangles touching. Do this by trimming the leader end along its own path, not by moving its source. The goldenrod V loops **yield** (occlude) where they cross the Z packet envelope + 1.5 mm (x 80–130, y 115–140): same path, gap at the packet, never rerouted or removed. The ∂L/∂Z → ∂L/∂V edge's head at x 152.5 (◁) is flipped to ▷, so both heads point the gradient's way | open (new; J2-compatible) | |
| S0 | r02 + r03 + r04 science | science | No `dossier.md` / `encoding.md`, so no §7 check numbers. r04 science: commission a dossier fixing A, V, the target and d_k | open: curator/expert. Not a designer mandate | |
| S1 | r04 science M1 | science | Token and shape consistency: V needs a 5th row; ∂L/∂K and ∂L/∂V need 5 rows; ∂L/∂Q needs 1 or 5 rows; one dimension axis per space (Q = K = ∂L/∂Q = ∂L/∂K width; V = Z = ∂L/∂Z = ∂L/∂V width) | open — **blocked by J2**: it changes element counts and packet widths (the r03 SYNTH already forbade count changes). Needs Juan. Not a translator count | |
| S2 | r04 science M2 (comb clause) + DESCRIPTION § Keep ("a real crest-crossing structure") | science | The hero comb is S₁ circles only (m 14–45, 0 S₂ arcs), 0.66 L off the two-source crests at the lens edge, and bows toward Q on a mirror plate. The fringes must be the two-source standing-wave crests: the hyperbolae r₁ − r₂ = const, symmetric about x 104.83, same lens, same count, same 1.042 mm on-axis pitch, same pen. The reference's own comb is symmetric (`ref/reference.png` hero crop) | open (new). **J2-compatible**: a computed element corrected to the rule it claims, with element, position, count, pen and look class (a striped lozenge) unchanged. Inherited from r01, not introduced by r04 | |
| S3 | r04 science M2 (A, Z clauses) | science | A derived from something drawn, with the rule stated; Z = Σ a_j V_j with \|Z\| ≤ max\|V_j\| and residual < 5 % | open — **blocked by J2** (recomputes the traced Z and softmax shapes). Needs Juan | |
| S4 | r04 science M3 | science | Backward chain: ∂L/∂V_j = a_j·∂L/∂Z; ∂L/∂A index-aligned with A; ∂L/∂Q, ∂L/∂K ∝ \|∂L/∂S\| (the softmax shift-invariance as the plate's §5) | open — **blocked by J2** (recomputes traced packets). The arrowhead-direction clause moved to A14. Needs Juan | |
| S-fold | r02 science M1–M3 | science | beads where QKᵀ = 0 · seam phase · channel labels | dropped for this slug: travels with flavour `the-fold` | r03 |
| S-phase | r03 science M1–M3 | science | caption/sign key · source of A · \|g\|-proportional patches, verifiable colophon | dropped for this slug: travels with flavour `gradient-as-phase` | r03 |

## Engine requests (from r04 NOTES; for the curator / pp-improve, never a designer edit under `promptplot/`)
1. `order="as_emitted"` / `STREAM_ORDER` switch in `render_candidate.py` / `run_pipeline`. `reorder_by_color` undoes a piece's batch-aware order, which is why r04 ships `plate.py`.
2. The i/j tittle in `_GLYPHS` fuses into the stem under about 3 mm caps at a 0.35 nib.
3. The `kit.fill_disc(spacing=0.45)` default is larger than the nib.
4. A shared `kit.round_dot(x, y, r)` (closed 8-gon) plus `kit.pen_touch(x, y)`, so all three siblings share one dot per class.
