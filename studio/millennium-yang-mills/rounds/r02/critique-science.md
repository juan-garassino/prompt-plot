# Science critique — millennium-yang-mills r02 · mathematical physics (quantum Yang–Mills) · 2026-09-28
render: gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_abstract_v7.png
gcode:  gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_abstract_v7.gcode (9080 cmds; layers 0:29 / 1:120 / 2:433 / 3:7 / 4:2 strokes)
thesis: ABSTRACT (half-section p ≥ 0, spine x = 40, vacuum (40, 50), s = 100 mm/Δ)
mode: pass 1 (cold). No LEDGER.md exists for this slug.

Primary source spot-checked: pulled arXiv:2007.06422 LaTeX, `table_MK_J` rows read
3.405(21), 4.894(22), 5.276(45), 5.855(41), 6.065(40), 6.32(9), 6.788(40), which match the dossier and the JSON.
I recomputed all 20 JSON `M_over_Delta` entries from `M_over_sqrt_sigma/3.405`. None is off by more than 6e-5.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | Δ/√σ; drawn Δ = s | 3.405(21); s | 3.405 (arXiv tex) | vacuum centre (40.003, 49.97) → red vertex (40, 150.00) = **100.03 mm** | OK |
| 2 | M/Δ of 2⁺⁺, 0⁻⁺, 0⁺⁺*, 1⁺⁻, 2⁻⁺ | 1.4373 1.5495 1.7195 1.7812 1.8561 | same | each pen-3 shell was fitted with √(E²−p²) over its 606 pts: **1.4373 1.5495 1.7195 1.7812 1.8561** (spread ≤ 1e-4) | OK |
| 3 | threshold 2Δ; states below it | 6.810 √σ; 7 | 6.81; 7 | rim fits M = **2.0000** (±1e-4). Six shells are drawn and 2⁺⁺* is merged into the rim, declared in the caption ("2⁺⁺* SITS ON 2Δ"). 2⁺⁺* is (2 − 1.9935)·100 = 0.65 mm below the rim, inside its ±1.7 mm error. | OK |
| 4 | gap : isolated band | 1 : 1 | 1 : 1 | 100.03 : 100.00 mm (apex→0⁺⁺ vertex : 0⁺⁺→rim vertex) | OK |
| 5 | cone 45°; 0⁺⁺ above cone at p = 3Δ | 45°; 0.1623Δ | 0.16228 (1/6 = 0.1667 asymptotic) | all 29 dashes measure **45.000°**, with max offset from E = p of 1e-14 mm. p = 3 is off-sheet. At the stop, p = 2.42: red sits **19.85 mm** above the ruling (calc 19.847) | OK |
| 6 | lens tip: 0⁺⁺ at p = 1 | √2 = 1.4142Δ | 1.41421 | red fit M = 1.0000 (min 0.9999, max 1.0001) along 611 pts, so E(1) = 1.4142 | OK |
| 7 | non-red ink in lens {p<E<√(p²+1)}, p ≥ 0 | 0 strokes | — | Pens 0, 1 and 2 have **0** segments in the lens. Pen 3 has 35, all inside the Ø 3.07 vacuum disc (allowed). Pen 4 has 4, the Δ bar (allowed). If the lens is mirrored to p < 0, the Δ glyph (27–36, 95–105) and the "0⁺⁺" tag corner fall inside it. The half-section is declared in encoding §4/§5A, so this is not counted. | OK |
| 8 | Chen cross-check | 1.401, 1.502 | 1.4014, 1.5024 (1⁺⁻ 1.748, 2⁻⁺ 1.784) | only AT2020 is drawn. No Chen data on the sheet. | OK |
| 9 | lattice approach m_G/√σ | 2.468 … 3.346 | 2.468 2.867 3.060 3.205 3.269 3.312 3.308 3.346 | not used by this thesis | OK (dossier) |
| 10 | ξ = 1/Δ; ring pitch at r = 8.4 | 0.2937/√σ; 0.119 fm; 0.851/Δ | 0.29369; 0.11949 fm; 0.8515 (K₁ solve by quadrature) | not used | OK (dossier) |
| 11 | BPST ∫q; half-max radius | 1.000; 0.435ρ | 1.0000; 0.43498 | not used | OK (dossier) |
| 12 | b₀ SU(3) | 11 | 11 | not used | OK (dossier) |
| — | min perpendicular shell gap | enc: 2.80 mm (0⁺⁺*/1⁺⁻) | 2.82 mm (at p = 2.42) | 1⁺⁻/2⁻⁺ 3.53, 2⁺⁺/0⁻⁺ 4.51. All are above the 0.8 mm floor. | OK |
| — | continuum strata | pitch 1.0, end on rim with 0.29 inset | — | 120 strata, all horizontal, **pitch exactly 1.000**, y 251…370. **0** strata below the rim or left of the spine, and none between shells. Perpendicular end→rim gap is **0.287 / 0.291 / 0.293 mm** (min/med/max). | OK |
| — | staff on axis above red vertex | 43.7 54.9 72.0 78.1 85.6 | 43.73 54.95 71.95 78.12 85.61 | pen-3 stroke endpoints at x = 40 | OK |
| — | tags at vertex heights, correct J^PC | — | — | 0⁺⁺ 148.9, 2⁺⁺ 192.6, 0⁻⁺ 203.9, 0⁺⁺* 220.9, 1⁺⁻ 227.0, 2⁻⁺ 234.5, 2Δ 248.9. Each is its vertex − 1.1 mm (cap centred). I decoded the sign strokes and all 7 labels are correct. | OK |

Minor deviations from encoding (not truth): the cone dashes are **9.0 mm dash / 3.0 mm gap**, where the spec is 6 / 4. The first dash starts 0.8 mm off the disc edge, not on it. Tag caps are **2.2 mm**, where the spec is 1.8.

## Lies list
| item | status |
|---|---|
| 1 ink in gap lens (besides vacuum + Δ) | clean (0 segments, pens 0–2) |
| 2 anything on the light cone as a state | clean. Pens 1–4 have 0 pts within 0.6 mm of the ruling off the disc. The ruling is ghost-grey and dashed. |
| 3 non-uniform/log scale, E≠p scale | clean. 45.000° measured, and each shell fits its M to 1e-4. |
| 4 equal spacing / ladder | clean. The vertex gaps are 43.7, 11.2, 17.0, 6.2, 7.5, 14.4 mm. |
| 5 vacuum as band/sea | clean. It is one solid spiral disc, Ø 3.07 mm. |
| 6 continuum not at exactly 2Δ | clean. The strata end 0.29 mm (the physical inset) off the rim. |
| 7 gluon lines / knots / instantons | clean |
| 8 MeV/GeV | clean (none on sheet) |
| 9 "proven" | clean. The caption says "PROVE … AND THAT Δ > 0. OPEN." |
| 10 mixed data sets | clean (AT2020 only, cited) |
| 11 shells' approach to cone = asymptotic freedom | clean (not claimed) |

## Scores
truth **9** · fidelity **9** · legibility **7** · VERDICT: **FAIL**

Truth and fidelity are close to exemplary. Every curve is exact to 1e-4 Δ, the scale is isotropic, the 1:1 physics coincidence is measured at 100.03 : 100.00, and the lens is empty.

Legibility fails the §5 test for a stranger. The sheet never says what the lines, the plane or the dashed diagonal *are*. The words "glueball", "particle", "pair" and "massless/light-speed" appear nowhere. So the misconception correction ("gluons are massless like light, so the gap is a gluon mass"; the CMI twist "massless waves, massive particles") is only readable by someone who already knows the Wightman picture. The J^PC parity signs are also too small to read on the sheet.

## Mandates
1. **Name the carriers.** Measured: 0 occurrences on the sheet of "glueball", "particle" or "pair". The only gloss is "HEIGHT ENERGY, WIDTH MOMENTUM, ONE SCALE" in the bottom-right caption (x ≤ 281, y 18–30). Expected: one caption line in that block stating what each drawn element is. Each black/red line is one glueball, with its mass read at the height where it meets the left edge. The hatched plane is every pair of glueballs, starting exactly at 2Δ. It stays in the corner caption; nothing goes into the plane or the lens.
2. **Say what the empty cone means (dossier §5 twist).** Measured: the ghost ruling from (40, 50) to (282, 292) carries no meaning on the sheet. The statement at y ≈ 386 names "the light cone" but never says who would live there. Expected: one line, in the bottom-right caption or the statement, stating that the classical Yang–Mills waves travel at light speed (E = |p|, the dashed line) and that in the quantum theory no state lies on it, so there is no massless gluon. It must not contain "proven" or MeV.
3. **J^PC superscripts are illegible.** Measured on the gcode: superscript ± glyphs are **0.70 × 0.70 mm**, with **0.53 mm** between signs, drawn with a 0.2 mm nib. That is 0.32× the 2.2 mm cap. In the render, "⁻⁺" on the 2⁻⁺ (y 234.5) and 0⁻⁺ (y 203.9) tags fuses into an arrow. Expected per encoding §4: superscripts at 0.6× cap (≥ 1.1 mm at the 1.8 mm cap, 1.3 mm at the 2.2 mm cap as drawn), with a sign gap ≥ 0.8 mm (≥ 4 nib widths). Location: the tag column at x 30–36, y 149–251.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | first science pass; `studio/millennium-yang-mills/LEDGER.md` does not exist |
