# Art critique — millennium-riemann r03 · canon: SWISS + LeWitt instruction drawing (declared hybrid) · 2026-09-29
render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.png (judged on gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2_phys.png at true nib widths; true-width crops from gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.gcode)

## Scores

| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 8 | The comb dominates at 3 m. The red column comes second, then the title, then the wall label. Red is now one thin pass: it reads as a stitched seam at 3 m and as crosses at 1 m. It is scarcer and quieter than it could be for the one mark that carries the claim. |
| 2 | grid & alignment | 9 | Measured on the gcode. The title and the statement both end at exactly x = 180.0, so the top band is locked to the column. The series caption, wall label and right footer all start at x = 206.0. The series caption's cap line (403.36) equals the title's cap line (403.36). The wall label clears its rulings by ≥ 2.97 mm. The rulings keep a 15.64 mm pitch. |
| 3 | tension & asymmetry | 9 | ζ supplies the 62 : 38 split. The comb bleeds off the left, the fan sweeps down to the lower-left, and the right is ruled silence. The type mass sits high-right, balancing the fan low-left on the diagonal. |
| 4 | negative space | 8 | Three silences, each of them true: the ruled right field, the 48.8 mm red-free stretch of the column, and the band under the statement. The lower-right half of the right field (y 32–300) is bare rulings, which is right for Swiss and right for ζ. Overlap happens only at the zeros and on the axis. |
| 5 | craft for pen | 9 | The red is one one-way pass per arm, 56 strokes. There are no knots in the γ₂₀–γ₂₈ crops and cream shows in all four quadrants. There are no floods, and A–B spacing stays well above 0.8 mm everywhere outside the discs. 4 layers, 2 physical swaps, ≈ 94 min plate job quoted from the dry-run. |
| 6 | concept legibility | 8 | The two families touch only in one column that nobody drew, and that lands before you read anything. The wall label turns a known mathematical figure (the Arias de Reyna X-ray) into an instruction drawing. It is not a schematic. |
| 7 | depth & dimensionality | 8 | Flatness is declared and argued (conformality only holds in a flat isotropic plane). The 0.1 / 0.3 weight split gives a quiet two-plane read. Unchanged from r02. |

**avg 8.43 · min 8 · VERDICT: PASS**

## Reads at a glance
At 3 m: a black curtain of tongues sweeps in from the left and fans down onto a floor line. Every tongue tip stops on one invisible vertical stitched with small red crosses, and ruled empty paper lies to the right.

## Acceptance checks (encoding §11)
1. **ONE COLUMN: PASS.** There are 56 red arms, which makes 28 crosses on one visible vertical at x ≈ 180 (the true-width crops at ρ₁, ρ₂, ρ₄ and γ₂₄–γ₂₈ are centred). The heights are visibly unequal. The lowest centre is 48.76 mm above the baseline. The lowest arm tip is at y = 79.09, which is the ρ₁ cross itself, accepted as in r02.
2. **RIGHT ANGLES THAT TILT: PASS.** In the true-width crops the Im-arm leans about −8° at ρ₁, +13° at ρ₂ and +30° at ρ₄, and each Re-arm crosses at a visual 90°.
3. **NOT A MIRROR: PASS.** Right of the column there are only hairline rulings, flattening to a 15.64 mm pitch. Black does not go past the tongue tips or the pole dome (0.01 m right). Field ink (layers 0+1) is 2.20 m right against 22.63 m left, which is **9.7 %**. The audit prints 10.10 % because it also counts the red, which sits *on* the column. By the r02 definition this is under the cap, but only just.
4. **NO OTHER MEETINGS: PASS.** No black–hairline contact appears except at the red crosses and on the real axis. The lone Gram and half-Gram hairlines that loop past the column between crosses are left visible (e.g. y ≈ 112, 141, 270, 325).
5. **PLOTTABLE AND CLEAN: PASS.** The gcode sits beside the png. There are 4 layers in order 0→1→2→3 with 2 swaps. The spacing floor is held, no type touches the comb, and the axis numerals sit 3.2 mm under the baseline.

AUTHORING §6 (the reference is an interpretation brief only: the abstract thesis drops its streamlines, mirror, beads and inset):
1. Forms read without fills: yes.
2. Shadow lines follow the surface: n/a (there is no hatch).
3. Fine lines as two sides of one stroke: no.
4. Blackest regions: the comb's upper-left density, which is intended (ζ's own pitch). The red knots are gone.
5. Labels at true width: crisp at 2.2 and 1.6 mm caps.
6. Thick pen knots: none. The 0.5 red is one pass, and the centre is the only double-ink spot.
7. Wasteful travel or tiny marks: none. Every stroke is a whole curve or glyph, and the red hops ≤ 20 mm up the column.

## Biggest weakness
From γ₂₀ upward, the red mark still reads at 1 m as a red *hook* rather than an X. The r = 1.6 mm window catches the curl of each tight tongue tip, so the Re-arm is a C-arc with the short Im-stub through it. This is truthful geometry, and the knot problem is solved, but the one-glance statement ("every meeting is a red right-angled cross") is fully delivered only in the lower two-thirds of the column.

## Mandates (PASS: polish notes)
1. **The upper crosses read as crosses.** Keep the Re-arm on the true curve. Test on the true-width crop x 170–190, y 330–368: in each γ₂₄–γ₂₈ mark the Im-arm extends at least as far past the centre as the Re-arm's chord, so the X reads before the C. Do not trade this against the constant-r rule without the translator's sign-off. If it cannot be done honestly, leave it.
2. **One definition of the ink ratio.** State in HANDOFF that §11.3 is measured on layers 0+1 (field lines, not red), so that the art and science critics and the audit report the same number (today 9.7 % vs the audit's 10.10 %).
3. **The axis numerals earn their place.** `−4 −2 1` is a partial ruler, and a stranger may ask why −6 … −14 are unlabelled. Either say in the bottom-left caption that these three anchor σ = ½, or leave them as they are. Do not add more numerals (that would make it an axis, which §9.5 forbids).

## Follow-up on open mandates

| id | status | evidence |
|---|---|---|
| A1 | FIXED | True-width crop x 170–190, y 330–368: each γ₂₄–γ₂₈ mark has two distinguishable arms, cream in all four quadrants, and no blob wider than the nib except the centre. The red layer is 56 strokes, one one-way pass per arm (audit: 0 arms re-enter their own nib; arm-vs-arm overlap ≤ 0.516 mm from centre). Against r02's lumpy "crabs" in the same crop, this is clearly better. |
| A2 | FIXED | (a) The `1 BLACK` block spans y 347.9–357.47 between rulings at 344.8 / 360.44, so the clearance is 3.1 / 2.97 mm, above 2.5. (b) The statement's right end is at x = 180.0, the same as the title. (c) The series caption is flush-left at x = 206.0, line 1 is 2.2 mm caps, and its cap line (403.36) equals the title's. |
| A3 | FIXED | HANDOFF quotes the `plot plate --dry-run` minutes 31 / 26 / 28 / 3, ETA ≈ 94 min at feed ≤ 500 and dwell ≥ 1 s. |
| S1 | FIXED (visible; the science critic owns it) | The key reads `3 RED / WHERE BOTH ARE, / ABOVE THE REAL LINE.` |
| S2 | FIXED (visible; the science critic owns it) | `−4 −2 1` in 1.6 mm caps, y 27.2–28.8, under the feet at x ≈ 164.5 / 171.4 / 181.7. |

There is no FEEDBACK.md or DESCRIPTION.md, so there are no J* mandates and no Keep list.

## Regressions vs compare-to (r02 `pp_millennium_riemann_abstract_v6_phys.png`)
- **Red presence at 3 m is lower.** Going from 0.5 × 2 passes to 1 pass makes the column read as a finer stitch than r02's specks. This was an intended trade (A1), and the result is better at 1 m. It is noted only so that no later round compensates by fattening the red back into knots.
- **The ink-ratio margin narrowed.** r02 measured 9.6 %; r03 measures 9.7 % on layers 0+1 (10.10 % with red). This is not a visual regression, but it now sits close to the §11.3 cap.
- Nothing else is worse. The comb, fan, rulings, bottom captions and title are identical to r02, and the top band is improved (series caption, x = 180 alignment).
