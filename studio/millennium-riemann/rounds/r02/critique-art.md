# Art critique — millennium-riemann r02 · canon: SWISS + LeWitt instruction drawing (declared hybrid) · 2026-09-29
render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.png (judged mainly on gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6_phys.png, true nib widths on cream) · gcode gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.gcode

## Scores

| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 8 | The comb dominates at 3 m. The red column comes second, the title third and the wall label fourth. At 1 m the red marks read as "red asterisks pinning tongue tips", not yet as right-angled crosses (see weakness). |
| 2 | grid & alignment | 8 | x = 15 is a real shared edge (title, statement, comb bleed, left footer). x = 206 is shared by the wall label and the right footer. Rulings sit at an exact 15.64 mm pitch (measured 15.63–15.64 over 21 gaps), and the label sits between them. Two small faults: the "PART OF ζ(S) IS ZERO." line sits 2.25 mm from the k = 20 ruling (the spec is ≥ 2.5 mm), and the title's right end (x ≈ 137) aligns to nothing. |
| 3 | tension & asymmetry | 9 | ζ supplies the 62 : 38 split. The comb bleeds off the left edge, the fan sweeps down to the lower-left into the baseline, and the right side is ruled silence. Nothing is centred. |
| 4 | negative space | 8 | Three shaped silences, each of them true: the ruled right field, the 48.8 mm red-free stretch of the column, and the band between the statement and the field. Line overlap only happens at zeros and on the real axis, so every overlap is a decision. |
| 5 | craft for pen | 7 | Outside the zero discs the closest A–B approach is 1.60 mm, with no site under 1.0 mm. There are no floods and no loose stroke ends inside the field. Layer order is 0→1→2→3 (2 physical swaps), the ruling pitch is exact, and there are no kinks over 12° outside tight tongue tips. Against: the red is 0.5 nib × 2 passes on r = 1.6 mm arms, so at the top zeros each mark is a lumpy knot (the arm is ~3× as long as the nib is wide, and the centre gets 4 passes). The gcode also streams draws at **F2000 with G4 P0.2 dwells**, while HANDOFF quotes F600 timing and Leo needs F600 / P1.0. |
| 6 | concept legibility | 8 | The order (two instruction families, touching only in one column that nobody drew) lands before you read the caption. The twist works because the seam belongs to a picture that is not symmetric. Held back by: it sits close to Arias de Reyna's published "X-ray of ζ" figure, and the LeWitt wall label is what lifts it out of that. |
| 7 | depth & dimensionality | 8 | Flatness is declared and argued: conformality means the 90° only survives in a flat isotropic plane. The 0.1 against 0.3 weight gives a quiet two-plane read. |

**avg 8.0 · min 7 · VERDICT: PASS** (at the bar, no margin)

## Reads at a glance
At 3 m: a black curtain of tongues sweeps in from the left and fans down into a floor line. Every tongue tip stops on one invisible vertical marked by a column of red specks, with ruled empty paper to the right.

## Acceptance checks (encoding §11, measured on the gcode)
1. **ONE COLUMN: PASS.** There are 28 red crosses. Each red branch passes within 0.13–0.15 mm of (180.0, 32 + 3.45·γₙ), inside the ±0.3 mm tolerance, and the heights are visibly unequal. The lowest centre is 48.76 mm above the baseline. Strictly, the lowest red *arm tip* reaches y = 79.0, which is 47.0 mm above the baseline. That is the ρ₁ cross itself and I accept it.
2. **RIGHT ANGLES THAT TILT: PASS.** At the centre, all 28 crosses meet at 87.5°–90.0°. The hairline arm leans −8.5° at ρ₁, +12.6° at ρ₂ and +30.4° at ρ₄ (spec: −9 / +13 / +31).
3. **NOT A MIRROR: PASS.** Right of x = 180 there are hairline rulings only. Black never goes past x = 181.72 (tongue tips and the pole dome), and 22 rulings sit at a 15.64 mm pitch. In the field (layers 0+1), right-of-column ink is 2.20 m against 22.90 m on the left, a ratio of **9.6 %**, just under the 10 % cap.
4. **NO OTHER MEETINGS: PASS.** No layer-0/layer-1 approach is under 1.6 mm outside the 28 zero discs and the real axis. The Gram and half-Gram hairline loops that go around the tongue tips past the column are left visible (e.g. y ≈ 112, 141, 270, 325).
5. **PLOTTABLE AND CLEAN: PASS, with a flag.** The gcode sits beside the png. There are 4 layers in the stated order with 2 swaps, the minimum spacing is ≥ 0.8 mm, no type touches the comb, and bounds are [15, 282] × [15.1, 403.4]. Flag: F2000 draw feed and 0.2 s dwells do not match the F600 timing in HANDOFF (see craft). Type-to-ruling clearance is 2.25 mm against the 2.5 mm spec.

AUTHORING §6: the reference is an interpretation brief only. This abstract thesis intentionally drops its streamlines, mirror, beads and inset.
1. Forms read without fills: yes.
2. Shadow lines follow the surface: n/a (there is no hatch).
3. Fine lines as two sides of one stroke: no.
4. Blackest regions: only the red knots, and they are intended but heavier than they need to be.
5. Labels at true width: yes, crisp.
6. Thick pen knots: the 0.5 red × 2 passes knots at the top zeros (γ₂₄–γ₂₈).
7. Wasteful travel or tiny marks: no. 56 red arms, 499 glyph strokes, and every line stroke is a whole curve.

## Biggest weakness
The one mark that carries the whole claim, the red right-angled cross, does not read as a cross at 1 m. The r = 1.6 mm window catches the curl of the tongue tip, so the Re-arm is a C-shaped arc. The 0.5 nib drawn twice then fattens that arc and the short hairline stub into a lumpy red "crab" or asterisk, especially from γ₂₀ upward where the tongues are tight. The geometry is exact (90° ± 2.5° measured), but the eye gets a blot, not a crossing.

## Mandates (PASS: polish notes, up to 3)
1. **Make the red read as a crossing at 1 m.** Draw the red layer in **one pass** (drop the second), or at a 0.3 nib, keeping r = 1.6 mm. Test: in a 1:1 crop of γ₂₄–γ₂₈ (x 170–190, y 330–368) at true width, each mark shows two distinguishable arms with cream visible in all four quadrants around the centre, and no filled red blob wider than the nib at the centre.
2. **Put the type on its own grid line.** Move the "1 BLACK" block down (or tighten its leading) so that every glyph is ≥ 2.5 mm from both bounding rulings. Measured today: 2.25 mm at (225.3, 347.0) against the k = 20 ruling at y = 344.8. Make the title's right end or the statement's right end land on a declared line (x = 180 is the natural one, the column), so the top band belongs to the same grid as the field.
3. **Emit Leo-ready gcode.** Draw feed F600 and pen dwells G4 P1.0 (the house setting for Leo), so the gcode beside the png is what the HANDOFF's ≈ 80 min estimate describes. Test: `grep -c F2000` on the gcode returns 0 for G1 draw moves, and the dwell lines read P1.0.

## Follow-up on open mandates
None. There is no LEDGER.md, FEEDBACK.md or DESCRIPTION.md for this slug yet, and HANDOFF gives compare-to: none (new plate).

| id | status | evidence |
|---|---|---|
| — | — | no open A*/J* mandates on record |

## Regressions vs compare-to
None assessable (no parent render). The sibling faithful r01 is still in progress and is not a compare-to.
