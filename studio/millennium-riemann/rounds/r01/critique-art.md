# Art critique — millennium-riemann r01 · canon: SWISS sheet + LeWitt instruction drawing (stated hybrid) · 2026-09-29
render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5_truewidth.png (judged; also re-rendered from gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5.gcode at 20 px/mm for crops)
thesis: FAITHFUL

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 8 | The comb owns the sheet at 3 m. The red column reads second at 1 m. The right-void type and the ψ footer come third. The 8 mm single-stroke title is thin but correctly subordinate. |
| 2 | grid & alignment | 8 | x = 15 carries the title, statement, field edge, footer label and footer curve. x = 190 carries the header block and every right-void line. The right-void type sits between ζ's own rulings, so the Swiss grid really is ζ's grid. The footer numerals sit under their cliffs. The ticks are on x = 148.5. |
| 3 | tension & asymmetry | **6** | Left against right is strongly lopsided, and that part is excellent. But the real axis sits at y = 210, the page's exact mid-height, and the column sits at x = 148.5, the exact mid-width. The comb mirrors top to bottom into one big ">" arrowhead, and it points at the pole loop at the dead centre of the sheet. At 3 m it reads as a centred emblem: the rubric's first known failure mode, and "centered = fail" in the Swiss canon. It is declared as the control, but it still costs the sheet its tension. |
| 4 | negative space | 8 | Three real silences: the ruled right field, the 84.8 mm zero-free stretch of the column, and the calm band around the real axis on the right. Seven type rows in the right void eat some of that silence, and the empty band between the tagline and the Euler product looks like leftover space, not a chosen gap. |
| 5 | craft for pen | 8 | Measured on the gcode, every non-red pair of strokes from different layers is ≥ 0.8 mm apart, excluding the real-axis crossings. There are no floods and no knots. The chevron apexes at the trivial zeros turn with a radius of about 0.5 mm but stay vertical at the axis. 4 layers, 2 swaps. The red arms are cleanly substituted with no stray overlap. Note: the gcode draws at **F2200 with 0.2 s dwells**, but HANDOFF quotes "≈ 80 min at F600" (Leo's working feed and dwell are F600 and G4 P1.0). |
| 6 | concept legibility | 7 | The order reads: two families, one column of red right-angled crosses, silence on the right. But the only closed form on the sheet is the black Re ζ = 0 loop around the pole, sitting on the real axis at the page centre. It carries no caption, so a stranger reads it as a "bead on the axis", which is exactly the reference's lie. It also steals the focal point from the red column. The chevron meetings on the real axis are not explained anywhere on the sheet either. |
| 7 | depth & dimensionality | 7 | The flatness is declared, and it serves conformality. The 0.1/0.3 alternation gives the strata a woven rhythm, but there is no other depth play. |

**avg 7.43 · min 6 · VERDICT: FAIL** (tension 6 < 7)

## Reads at a glance
A black arrowhead of U-tongues fills the left half and points at a small black ring in the dead centre. It is stitched along its tip by a column of tiny red crosses with a long red-free gap around the middle. The right half is quiet ruled paper carrying type.

## Acceptance checks (encoding §11)
1. **ONE COLUMN: PASS.** 20 red crosses, each passing within 0.3 mm of (148.5, 210 ± 3γₙ). The heights are visibly unequal. There is no red within ±42.4 mm of the real axis. The ticks sit at y 48.9–53.9 and 366.1–371.1.
2. **RIGHT ANGLES THAT TILT: PASS.** A PCA fit of each arm within 0.8 mm of the centre gives: ρ₁ hairline −9.4°, meet 89.3°; ρ₂ +12.6°, meet 89.7°; ρ₄ +31.0°, meet 89.4°.
3. **NOT A MIRROR: FAIL (numeric only).** The lower half is the exact reflection of the upper, and right of the column there are only hairline rulings (plus the right half of the pole loop and the half-Gram tongue tips). But the ink right of x = 148.5 is 3.11 m against 16.56 m on the left, which is **18.8 %** and above the ≤ 10 % bar. Nothing was added. The rulings to x = 282 simply cost more than the encoding estimated. The lead should either re-set the threshold or accept it. It is not a design defect.
4. **NO OTHER MEETINGS: PASS.** There are no cross-layer approaches under 0.8 mm outside the red discs and the real axis. Tongues and hairlines crossing the column alone (Gram and half-Gram) are left visible at several heights.
5. **PLOTTABLE AND CLEAN: PASS.** The gcode sits beside the png. Layers run 0 → 1 → 2 → 3 with 2 swaps, spacing is ≥ 0.8 mm, and no type touches the comb. The footer cliffs at 2, 3, 4, 5, 7, 8, 9, 11 and 13 sit over their numerals (8 and 9 small but distinct). The feed and dwell mismatch in the Craft row is flagged, not failed.

AUTHORING §6 (reference in play, judged as an interpretation):
1. Main forms recognisable without fills: PASS.
2. Lines follow the form: PASS. Both families are ζ's own level sets.
3. Fine lines as two sides of one thick stroke: none. PASS.
4. Blackest regions intended: PASS. The top-left comb holds an even pitch with no congestion.
5. Labels readable at true width: PARTIAL. "⇒" is drawn at about ⅓ cap height and "½" is tiny, both in the statement and in the conjecture line. The slashed zero turns "ζ(ρ) = Ø" into "ζ(ρ) = ∅" on a maths plate.
6. Thick-pen knots: PASS. The 0.5 red joints are clean, and the 0.3 chevron apexes do not blot.
7. Long empty travels or pointless tiny marks: PASS.

As an interpretation the architecture is right. It keeps the reference's centred seam, the top-to-bottom mirror, the title and statement, the formulas and the primes strip, and it replaces each lie with the true object. The drawing is stronger than the poster it answers.

## Biggest weakness
The composition lands on the dead centre. The real axis at the exact mid-height and the column at the exact mid-width make four quadrants meet at the uncaptioned pole loop. The sheet reads as a centred emblem (an arrowhead aimed at a ring) when it should be a Swiss asymmetric field, and the one closed shape on the plate pulls the eye away from the red column.

## Mandates
1. **Take the real axis off the page's mid-height.** Enlarge the ψ₁₀₀(x) − x footer into a real second element: a band ≥ 40 mm tall with the curve at ≥ 2× its current amplitude. Lift the field (drop the scale to about 2.8 mm/u; the 1.18 mm floor becomes ≈ 1.10 mm) so the real axis sits at **y ≥ 228**, not 210. The pole loop must no longer sit at the sheet's centre point (148.5, 210). Test: measure the real-axis y in the gcode, and measure the footer band height.
2. **Caption the pole loop and the axis meetings in the right void**, in the ruling band that contains the real axis (x = 190, between the rulings at y_axis ± 13.6, clear of the loop by ≥ 5 mm). Suggested text: `THE RING IS RE ζ = 0 AROUND THE POLE S = 1. ON THE REAL LINE THE FAMILIES ALSO MEET AT −2, −4, −6 … (NO RED).` Test: a stranger can read at 1 m why the only closed curve is there and why it is black.
3. **Fix the maths type.** Use unslashed 0 in every mathematical expression ("ζ(ρ) = 0, 0 < RE ρ < 1"). Draw "⇒" at ≥ 0.8 × cap height and at the same stroke weight. Draw "½" with its numerals at ≥ 0.6 × cap height, in the statement and the conjecture line alike. Set "ψ(X) − X" at the same cap height as the rest of the footer label. Test: no Ø anywhere a digit means zero, and the arrow and fraction measure at those heights in a crop.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | — | Round 1. No LEDGER.md or FEEDBACK.md exists, so there are no open A*/J* mandates. |

## Regressions vs compare-to
None to judge: HANDOFF gives compare-to as none (new plate), and no DESCRIPTION.md § Keep exists.
