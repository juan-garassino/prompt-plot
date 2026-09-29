# Science critique — attention-weaving r07 · machine learning (transformer attention, softmax) · 2026-09-29
render: gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.png (gcode gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.gcode, 20,436 commands, 6 layers)

Inputs: HANDOFF.md, the gcode (parsed per `; color=N`), the png, `encoding.md` Revision 1.
**There is no `dossier.md` for this slug.** Its §7 check numbers and §4 lies list therefore do not
exist. I used encoding §4a/§4b/§4d as the check numbers and §9 (forbidden list) + §11 (acceptance)
as the lies list. That is a standing gap, not a fault of this round.

Method: rebuilt A from the stated rule with `promptplot.generative.rng.SeededRNG(7)`. The draws are
stdlib `rng.gauss` (the numpy path gives T = 2.3316 and does not match). Then I chained every
colour layer into threads: 22 crimson, 16 blue, 22 green lanes (bold Z11 as 5 loop pieces), and ONE
gold weft (53 pieces, exactly 2 free ends). I intersected them to read the over/under at every
crossing.

## Check numbers
| quantity | dossier (encoding §4) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| T (bisection, max row-11 = 0.190) | 2.29842 | 2.298425 | — | OK |
| row sums | 1 ± 1.1e-16 | max err 2.2e-16 | hill area/bin: max rel err 3.0e-4 (320.71 mm² total) | OK |
| Q11 a_max, argmax | 0.190, key 5 | 0.19000, key 5 | footer `a MAX 0.190` | OK |
| H(Q11) / range | 3.762 of 4; 3.76–3.94 | 3.7624; 3.762–3.940 | footer `H 3.76 / 4.00` | OK |
| full 22×16 A table | printed | matches to 4 dp (Q11 row max dev 0.0) | — | OK |
| bin order (keys) | 15,8,3,7,10,1,12,5,11,2,14,13,6,4,9,0 | identical | 16 blue landings, one per bin: bins 0…15 in x order, 16/16 distinct | OK |
| bins above 1/16 | 6–9 (keys 12,5,11,2) | 6–9 | mean height > 6.168 mm in bins 6–9 only. Pointwise the profile exceeds the tick over x 98.25–108.46 (62 % of bin 6, 100 % of 7–8, 53 % of 9) | OK |
| 1/16 tick height | mean-height scale | 6.168 mm above wall → y 189.77 | tick (129.9–132.9, 189.77) | OK |
| hill peak | ≈ 20.7 mm | — | 20.72 mm at x 102.48 (crown bin 7) | OK |
| hill zero at jambs, no step | yes | **impossible** (see M1) | h: 0 → 3.71 mm over x 77.5–78.0 and 3.57 → 0 over 129.09–129.5, shelf 3.5–4.5 mm | encoding wrong |
| gold-over count | 136 / 352 (38.6 %) | 136 (38.64 %) | **136 / 352**, all 352 crossings unambiguous (0 both-inked, 0 neither-inked) | OK |
| per-pick gold-over | 6–12 | [8,7,6,7,10,10,8,11,12,6,10,11,7,6,9,8] | same | OK |
| B rows ↔ lanes | seriated permutation, Q11 at slot 11 | — | the 22 measured lane rows are an exact bijection onto the 22 recomputed rows. Slot 11 = Q11 = `......####......` | OK |
| entries within 0.002 of 1/16 | 17; "nearest Q5×k3 0.06072" | 17; **nearest is Q15×k2 = 0.062462** (\|Δ\| 3.8e-5) | Q15×bin 9 drawn under (correct) | count OK, **named nearest wrong** |
| centroid infeasibility (R2 proof) | spread 4.1 bins, min sep 0.018 | bin-ordered: spread 1.88 bins, min sep 0.006 | — | numbers differ, conclusion (undrawable) holds a fortiori |
| storm over/under | Q over K ⇔ s_ij ≥ 0 | — | **109 / 109** storm crossings correct, using slot→query from the cloth and bin→key from the hill. This independently confirms thread identity is carried through the slit | OK |
| slit / lane pitch | 52 mm; 2.25 mm; x 78.75…126.0 | — | wall cut 77.5–129.5 (52.0). Green starts at 78.75…126.00, every diff 2.25 | OK |
| weave floors | lane pitch along pick ≥ 3.6; pick spacing ≥ 4.2; gold ≥ 5; angle ≥ 75° | — | 3.53 (**< 3.6**, 0.07 short); 4.39; 5.01; 83.5° | ~OK |
| weft topology | 1 thread, 16 picks, 15 turns, 2 ends on reed ticks | — | 1 chain, 16 × 22 crossings, ends (10.3, 86.0) and (229.7, 68.3), both on black ticks | OK |
| Q_i ↔ Z_i at wall | \|x_Q − x_Z\| ≤ 0.5 mm | — | **10/22 exceed**. Slot 0 −2.54 (Q ends at x 76.21, outside the slit), slot 1 −1.98, slot 21 +1.88, slot 2 −1.17, slot 20 +1.10 | **FAIL** |
| exits | 22 ticked, ≥ 3 mm, `11` on the bold one | — | 22 ticks at 3.55–3.81 mm pitch; `11` at y 118 | OK |
| reed mouths | ≥ 3 mm | — | min 3.23 mm, 38/38 ticked (bold Q is a loop) | OK |
| footer numbers | 22Q·16K→22Z, Σa=1, 0.190, 3.76/4.00, 52 MM, 16 bins, 2.25 MM, 136/352, tick 1/16 | all true | printed as specified | OK |

## Lies list
| item (encoding §9 / §11) | status |
|---|---|
| 1 no gold end in open paper | clean. 2 ends, both on frame ticks |
| 2 no gold in tight bundle | clean in substance. Min lane pitch along a pick is 3.53 mm vs the 3.6 floor (fabrication, not truth) |
| 3 no overridden crossing | **clean**. 352/352 follow a > 1/16 (S11 closed) |
| 4 no shelf, no jamb step | **VIOLATED** at x 77.5–78.0 and 129.1–129.5 (rise 3.7 mm in 0.5 mm, then a 3.5–4.5 mm shelf across x 78–97 and 110–129). **Forced by the data**: see M1. The encoding is what is wrong here |
| 5 no chart furniture in throat | clean. Only the 1/16 tick, outside the jamb |
| 6 no text above wall except Q, K, SOFTMAX | clean |
| 7 no second doubled strand | clean. Only Q11/Z11 are double; the passes are 0.24 mm apart |
| 8 no lane position implying weight | clean. Equal pitch 2.25, stated `ORDER ONLY` |
| 9 slit 52 mm | clean |
| 10 no arrows / leaders | clean |
| 11 storm unchanged | not checkable blind. Storm signs are 109/109 correct |
| 12 no lane–lane / pick–pick crossing | clean. Each pick crosses each lane exactly once |
| §11.4 Q_i = Z_i at same x (≤ 0.5 mm) | **VIOLATED** at 10/22 lanes. Slot 0's crimson stops at (76.21, 187.29), 1.3 mm LEFT of the slit on the jamb step, so it reads as a query stopped by the wall |
| §11.5 void x 10–90, y 100–150 | clean (0 marks) |
| `Z = AV` label | true as a schematic only. The cloth is the thresholded [A > 1/16], and V carries identity only. The caption states the threshold, so not a lie |

## Scores
- truth **8**: every number recomputes exactly; the hill area, the 352 crossings and the 109 storm signs are right. The deductions: Q0 visibly ends outside the slit, and the encoding contains two false statements (nearest-to-1/16 entry; a step-free exact hill).
- fidelity **8**: area-exact hill (3e-4), the tick sits at the exact mean-height 1/16, over/under is exact, and equal pitch is declared. The deduction: the Q→Z hand-off is displaced by up to 2.54 mm, which is more than one lane pitch.
- legibility **7**: the throat, the bold thread and the 4-pick punchline read at 30 cm. But the forced 3.5 mm floor reads as an unexplained stepped plinth (the r06 shelf again), and the plate never says what that floor means: softmax gives every key > 0. Also, the §8 count-balance twist (22 Q + 16 K → 22 warps + 16 V picks) is not on the sheet. Footer line 2 still reads `→ 22 Z`, and the gold is identified only by a lone `V`.

**VERDICT: FAIL** (legibility 7 < 8)

## Mandates
1. **Hill floor: amend the encoding, then make the floor say something.** Measured: the profile goes 0 → 3.71 mm within x 77.5–78.0, holds 3.5–4.5 mm across x 78–97 and 110–129, and drops 3.57 → 0 within x 129.09–129.5 (throat, y 183.6–188). Encoding R3 / §9.4 / §11.3 expect zero height at the jambs with no step. That is **mathematically impossible** under exact area + strict unimodality. With h non-decreasing, h ≤ mean(bin 1) = 3.76 mm on bin 0, and bin 0 must average 3.53 mm. So h must reach about 3.5 mm within ≤ 0.4 mm of the jamb. The designer drew the truth. Expected: translator deletes §9.4 / §11.3's "no step". Then pick one of two:
   (a) keep the floor and caption it (`a MIN 0.034 — NO KEY GETS ZERO`, footer, not the throat); or
   (b) switch the channel to area ∝ (a_g − a_min) and print that in the footer.
   Either way the step is explained, not hidden.
2. **Q_i → Z_i registration at the slit.** Measured \|x_Q(end) − x_Z(wall)\|: slot 0 2.54 mm (crimson ends at x 76.21, y 187.29, outside the slit's left edge 77.5), slot 1 1.98, slot 21 1.88, slot 2 1.17, slot 20 1.10; 10 of 22 lanes > 0.5 mm. Expected ≤ 0.5 mm (encoding §4b, §11.4, S9). Lives at throat x 76–128, y 187–191. Each crimson must arrive vertical at its own slot x = 103.5 + (k − 11)·2.25 before stopping 1.25 mm above the hill. Slot 0 must land inside the slit, above bin 0.
3. **Put the §8 count balance and V's role on the sheet.** Measured: footer line 2 reads `22 Q · 16 K → 22 Z`. The 16 gold picks, which are half of the "38 in = 38 out" twist and the V in `Z = AV`, are counted nowhere. The only V mark is a single letter at (12, 92). Expected (encoding §8, flagged for Juan): line 2 reads e.g. `22 Q · 16 K → 22 Z WARPS × 16 V PICKS`, so a stranger can see the spent keys come back as woven values (footer, y ≈ 27). Do not add text above the wall.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S5 | **FIXED** (encoding) / residual | `encoding.md` Rev 1 gives the seed, rule and full A. I recomputed it exactly (stdlib-gauss draws, T 2.298425). Still no `dossier.md`: no §7/§4 for future critics |
| S6 | **FIXED** | one 3 mm 1/16 tick at y 189.77 = the exact mean-height 1/16 (6.168 mm) |
| S8 | **FIXED** | lanes at equal 2.25 mm pitch, captioned `ORDER ONLY`. The measured lane rows are an exact bijection onto the queries; Z11 at slot 11 = x 103.5 |
| S9 | **PARTIAL** | identity is carried correctly (storm 109/109 and cloth 352/352 agree on the same slot→query map), but 10/22 crimson ends sit 0.53–2.54 mm off their lane. See M2 |
| S10 | **FIXED** | `11` at the Z11 exit (y 118). 22/22 exits and 38/38 reed mouths are ticked. V indexing is replaced by pick order = bin order, and it verifies (bold under gold at picks 7–10 ⇔ hill > tick in bins 7–10 from the left) |
| S11 | **FIXED** | 0 forced crossings. 352/352 follow a > 1/16, min gold piece 5.01 mm |
| regressions | none in truth | r06's exact numbers all hold. The shelf/jamb step (A19) persists, and it is forced (M1) |
