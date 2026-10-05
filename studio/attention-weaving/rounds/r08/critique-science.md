# Science critique — attention-weaving r08 · machine learning (transformer attention, softmax) · 2026-09-29
render: gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.png (gcode `gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.gcode`, 30,785 cmds, 1,344 strokes)

Wildcard round: SOFTMAXSUMSTOONE set 22 times, one line per query. `studio/attention-weaving/dossier.md`
**does not exist**, so the check numbers are taken from encoding.md §4a (data) and the HANDOFF
mapping. Everything was recomputed from the §4a generation rule: `SeededRNG(7)` `gauss` draws,
Q then K, tilts, s = √d·Q·K, and T by bisection.

## Check numbers
| quantity | dossier / claim | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| T (bisection, a_max(Q11) = 0.190) | 2.29842 | 2.298425 | caption "T 2.298" | OK |
| A matrix 22×16 (§4a table) | table | max abs diff vs table at 4 dp = 0.0000; bold pattern 0 mismatches | — | OK |
| row sums | 1 ± 1.1e-16 | 2.2e-16 | every line spans the 158 mm measure (x 10–168); all 330 interior cell edges sit in ink-free gaps at the line centre, min clearance 0.61 mm | OK |
| crimson count a > 1/16 | 136/352 | 136 (0 ties at exactly 1/16) | 352/352 cells have the correct colour at the line centre (0 mismatches) | OK |
| rings floor(16a) | 216×0 · 122×1 · 13×2 · 1×3 | 216 · 122 · 13 · 1; the 3 is Q11·k5 = 0.1900 | 128/136 crimson cells show skeleton × (1+2r) crossings; the 8 unresolved are M/X cells where rings merge in the V (Q19k4, Q20k4, Q10k9, Q15k9, Q3k9, Q18k9, Q0k6, Q16k4). Ring pitch ≈ 1.0 mm | OK |
| H range | 3.762 – 3.940 bits | 3.7624 (Q11) – 3.9396 (Q14) | — | OK |
| line height 84.76·(4 − H) | Σ = 258 mm | 257.996 mm; 5.12 (Q14) – 20.14 mm (Q11) | the 21 band boundaries, predicted from the caption's top-down order, match the glyph gaps to ≤ 0.01 mm (skeletons inset 0.55 mm) | OK |
| line order (caption) | 19 8 4 1 20 9 7 11 12 10 14 5 15 17 3 2 18 21 0 6 16 13 | — | confirmed by the heights and by 352/352 colours | OK |
| cell width = 158·a, exact at line centre | 2.61 – 30.02 mm | same | edges fall in the gaps (above). Green O/M/N/U glyph extents = 0.94·158a − 1.1 (r 0.92; side bearings) | OK at centre only |
| between centres the query slerps | disclosed | — | ink edges fit the slerped-query softmax at f = 0.2/0.4/0.48 (clearance ≥ 0.64 mm) but do **not** fit the line's own row (clearance 0.002 mm) | true as disclosed; see mandate 2 |
| off-centre deviation | not stated | at the band edges: worst Q11·k5, a 0.190 → 0.079 (30.0 → 12.5 mm); median per-row max 0.038 (6.0 mm); **100/352 cells** fall on the other side of 1/16 at one of their band edges | — | **FAIL (fidelity)** |
| key line "every a = 1/16" | 9.875 mm cells | 158/16 = 9.875 | key-line interior edges clear the glyph ink by ≥ 0.49 mm; the 16 k-labels sit centred within 0.9 mm | OK |
| caption formula `A = SOFTMAX(QKᵀ/T)  T 2.298` | — | taken literally (unit Q, K): a_max(Q11) = **0.0848**, 155/352 > 1/16 | the sheet draws a_max 0.190 and 136/352 | **FALSE** (the √d = 4 factor is missing; T_eff = 0.575) |

## Lies list
There is no dossier §4, so the lies checked are encoding §9 where it still applies, plus the HANDOFF claims.

| item | status |
|---|---|
| "No overridden crossing" (colour decided by a > 1/16 at all cells, no dead band) | clean. 352/352 at the line centre |
| "Every row sums to 1, so every line is justified" | clean. This holds at every y, including slerped rows, because each is a real softmax |
| "Its cell is a of the line" (caption, text block x 176–229, y ≈ 88–93) | **VIOLATED off-centre.** It is true only on the unmarked centre line. 100/352 cells swing across 1/16 by their band edges. The caption's "between lines the query slerps" discloses the mechanism but not its size |
| Printed formula matches the drawn data (caption x 176–229, y ≈ 38) | **VIOLATED.** `SOFTMAX(QKᵀ/T)` with T 2.298 reproduces a_max 0.085, not 0.190 |
| HANDOFF "layer order 2 forestgreen → 1 crimson → 0 black" | **VIOLATED in the gcode.** The file runs 0 → 1 → 2 (black first). Black never overlaps colour on this plate, so this is a fabrication-statement error, not a data error |
| No decorative mark posing as data | clean. Every mark is a data letter, the key line, labels or caption. No frame, rules or ornaments |

## Scores
truth **7** · fidelity **7** · legibility **8** · VERDICT: **FAIL**

- truth 7: all the data is exact and every count is true. One printed formula is false, and it is the one line a scientist would use to reproduce the sheet.
- fidelity 7: colour, line height and centre widths are exact. But width is the loudest channel, and across most of each glyph's height it shows an interpolated query that does not exist in the data. On 28 % of cells it disagrees with the colour.
- legibility 8: "every line is justified = sums to one" and "attention is nearly uniform" (lines that look almost like the 1/16 key line) both land at a glance. Row identity needs counting 22 lines against a 22-number list, and the exact-reading line is invisible.

## Mandates
1. **Caption formula (text block, x 176–229, y ≈ 38–41).** Measured: `A = SOFTMAX(QKᵀ/T)  T 2.298`, which recomputes to a_max(Q11) = 0.0848 and 155/352 above 1/16. Expected: a formula that reproduces the drawn a_max 0.190 and 136/352. Print `A = SOFTMAX(√d·QKᵀ/T)` (with Q, K unit) or `T/√d = 0.575`.
2. **Off-centre widths (all 22 lines, x 10–168).** Measured: widths follow the slerped query everywhere except the unmarked centre line. At band edges the worst is Q11·k5 at 12.5 mm against 30.0 mm (a 0.079 vs 0.190), the median row error is 6.0 mm, and 100/352 cells are on the wrong side of 1/16 relative to their colour. Expected: |width − 158·a_row| ≤ 0.5 mm over at least the middle 60 % of each band, with the slerp confined to the inter-line transition, and 0 colour/width threshold disagreements inside a band. The alternative is to mark every line centre on the sheet, so the exact reading can be found.
3. **Row identity and centre marker (right edge, x 168–175, at each line centre y_c).** Measured: 0 row labels. The only key is a 22-number list in the caption, and the reader has to count lines to use it. Expected: 22 query indices (black text layer), each on its line's centre within 0.5 mm: Q19 at y 286.2, …, Q11 at y 193.7, …, Q13 at y 39.1. This also marks the one height where mandate 2's exact width lives.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S5 | **FIXED** (A part) | encoding.md §4a now carries A and its rule. Recomputed: T 2.298425, table diff 0.0000 at 4 dp, 136 bold = 136. **`dossier.md` is still absent**, so there are no §1/§4/§5/§7 to check against |
| S6 | FIXED (superseded) | r08 has no hill. The key line at y 20–28 is a scale bar (a = 1/16 = 9.875 mm per cell), exact to 0.49 mm clearance |
| S8 | FIXED | each line is one query's own row. Band heights match the caption order to 0.01 mm, and colour is right at 352/352 |
| S9 | N/A (superseded) | there are no Q/Z threads in r08 |
| S10 | PARTIAL | the rule is printed and the colour is checkable at every cell. The width is checkable only on an unmarked line, and rows are unlabelled (mandate 3) |
| S11 | FIXED | there is no forced or overridden cell. Colour is exact at 352/352. The residual width/colour disagreement off-centre is new (mandate 2), not an override |
| regression | **FLAG** | r06 had every printed number true (S4). r08's printed formula is false (mandate 1). The HANDOFF layer order is also wrong against the gcode |
