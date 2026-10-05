# Science critique — resonance r06 · machine learning (transformer attention as wave interference) · 2026-09-29
render: gallery/studio/resonance/current/pp_resonance_iterate_v5.png (+ .gcode: 96,753 cmds, 4,618 pen-down strokes, 6 colour layers streamed 0→5)

Pass 2, and pass 1 re-run cold. `studio/resonance/` **still has no dossier.md and no encoding.md** (S0), so there
are no §7 check numbers, no §4 lies list and no §5 misconception. As in r05, the claim set is the plate's own
labels and equations, the "science it encodes" paragraph of DESCRIPTION.md, and the HANDOFF pen map. Every
value below was measured from the parsed `.gcode`, with pen-down strokes split by `; color=N`. Dotted paths
were rebuilt from the 0.2 mm dot circles, which sit at a 1.000 mm median pitch, and then walked for their
endpoints.

## Check numbers   quantity | claimed | recomputed | measured on sheet | OK?
| quantity | claimed | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| source centres | symmetric about x = 105 | — | (83.835, 166.285) and (126.165, 166.285), midpoint 105.000 | OK |
| source separation d | d = 35·L | 35 × 1.2096 = 42.34 | 42.330 mm, so d/L = 34.995 | OK |
| crest m meets 35−m on the axis | yes | holds when d/L is an integer | 34.995 | OK |
| crest loci (solid) | crests 1–21 solid | r = m·L | 21 loci per source, all fitting m = 1.000…21.000 to a residual σ < 0.05 mm. m ≤ 12 are full rings, m 13–21 are arcs | OK (the r05 claim/sheet mismatch is gone) |
| crest shape | real Huygens figure, which in an isotropic medium means circles | ry/rx = 1 | every locus fits an ellipse with **ry/rx = 1.1667** (m = 12: 14.515 × 16.935 mm). None fits a circle | VIOLATED (S3a, blocked by J2) |
| crest fade 22–51 dotted (stipple caps) | dotted continuation of the crests | dots on r = m·L | 296 cap dots. **72 %** lie within 0.1 L of a crest locus (median offset 0.007 L, m 17–37); a uniform scatter would put 36 % there | OK (honest crest continuation) |
| dotted halo ellipses (2 per source) | continuation of the wave field | loci r = m·L, ry/rx 1.167 | a ≈ 32.8 / 39.2 mm, **b/a = 0.69–0.70**, a/L = 27.1 / 32.4 (not integers), and the eccentricity is the opposite of the crests' | VIOLATED (S3a, blocked by J2) |
| field dots ∝ \|A\| | size = 1.1 + 22·\|A\| | A = Σ cos(k rᵢ)/√rᵢ, drawn metric | 121 filled dots (0.26–1.50 mm) plus 30 zero-size 0.06 mm ticks. corr(size, \|A\|) = **0.53** (normalised 0.44, Spearman 0.50). Radial falloff alone gives 0.39. Fit: size = 0.43 + 1.03·\|A\| | PARTIAL (S3b) |
| key count = value count | n_K = n_V | one V row per K row | K **5** rows (y 208.8…254.6), V **3** rows (y 121.2 / 128.0 / 135.1) | VIOLATED (S2, blocked by J2) |
| softmax entries = keys, Σ = 1 | one weight per key | 5 | **6** solid peaks at x 76.2 / 90.4 / 97.4 / 104.6 / 119.2 / 132.6, normalised 0.127 / 0.252 / 0.066 / 0.177 / 0.251 / 0.127 (mirror-symmetric), plus 3 dotted ghosts at 83.0 / 111.8 / 125.9 | VIOLATED (S2, blocked by J2) |
| Z = AV convexity | \|Z\| ≤ max_j \|V_j\| | ≤ 5.54 mm | Z peak **13.44 mm** (axis y 75), 2.43× the tallest V (5.54 / 4.93 / 4.02) | VIOLATED (S1c, blocked by J2) |
| Z width = V width (d_v) | equal | 42.34 mm | Z 28.63–96.87 = **68.24 mm** (1.61×) | VIOLATED (S1c) |
| Y width = Z width (d_model) | equal | 68.24 mm | Y 162.07–188.15 = **26.08 mm** | VIOLATED (S1c) |
| V → Z connector | terminates on Z | on the Z axis x 28.6–96.9 | 129-dot path from V row 3 (181.9, 120.2) along y ≈ 107, ending at **(88.9, 75.0)** on the Z axis | OK (S1a fixed) |
| softmax → Z links terminate on Z | yes | on the Z axis | 6 links end at (66.9 / 70.3 / 73.8 / 77.1 / 80.3 / 82.8, 75.0), all on Z's axis. No mid-air ends, none on Y or the MoE lane | OK (S1a fixed) |
| softmax → Z links leave from the non-zero weights | one link per solid peak | 6 solid peaks | links leave from x **76.2, 83.5 (ghost), 90.4, 97.4, 104.7, 111.8 (ghost)**. The solid peaks at 119.2 (0.251) and 132.6 (0.127) have **no link**, so 37.8 % of the drawn mass never reaches Z | **VIOLATED (new)** |
| Q·Kᵀ → hero wavelength | hero is Q·Kᵀ as interference | L derived from the Q/K carriers | hero L = 1.21 / 1.41 mm. Q/K carrier crest spacing 1.81–2.88 mm (row medians), and no row gives 1.21 | not derived (legibility) |
| Q → source 1, K → source 2 | fans converge on the hero | — | crimson fan ends x 82–97 (source 1 at 83.8), blue ends x 113–134 (source 2 at 126.2) | OK |
| top-2 of 5 experts | 2 solid / 3 ghost | 2/5 | solid lanes y 87.45 and 60.18, 3 dotted lanes | OK |
| plot stats (HANDOFF) | 4,618 cycles · 11.80 m draw · 8.23 m travel · max in-layer hop 88.2 (blue 87.5) · others ≤ 51.1 | — | 4,618 M3 · 11,800.2 mm · 8,235 mm travel excluding the final 323.6 mm park (preview total 8,558.6) · crimson 88.2, blue 87.5, black 51.1, green 43.8, gold 36.0, violet 26.2 | OK |
| feeds and dwells (HANDOFF "F600, F2000") | draw F600 | — | the gcode draws at **F1200–F2600** (35,570 moves at F1200, 16,353 at F1600, …), G0 has no F, and every dwell is **G4 P0.2** (not the 1.0 s Leo needs, per house memory) | mismatch: the 189.7 min estimate does not describe this file unless the streamer overrides feed and dwell (flag for lead, not scored) |

## Lies list   item | clean / VIOLATED (where)
(There is no dossier §4. These are the standard lies, checked one by one.)
1. **Lying geometry (hero): VIOLATED.** All 42 crest loci are ellipses with ry/rx = 1.1667 about (83.8, 166.3) and (126.2, 166.3), where an isotropic Huygens figure has circles. Held since r01, blocked by J2.
2. **Fake data continuation: VIOLATED.** There are two dotted halo ellipses per source (x 44.5–68 and 142–165.4, y 138.8–193.7) with b/a 0.70 and a/L 27.1 / 32.4, so they are not crest loci. The stipple caps are **clean**: 72 % of their dots sit on crest loci m 17–37.
3. **Decorative marks posing as data: PARTIAL.** The 151 field marks track \|A\| weakly (r 0.53, of which radial falloff alone explains 0.39). 30 of them are zero-size 0.06 mm ticks with mean normalised \|A\| of 0.23, against 0.52 for the filled dots, so the smallest marks do sit at low amplitude.
4. **Broken count / shape: VIOLATED.** 5 K rows, 3 V rows, 6 solid softmax peaks and 6 gold links feeding a single Z (blocked by J2).
5. **Invented values: VIOLATED.** The softmax heights are mirror-symmetric (0.127 / 0.252 / 0.066 / 0.177 / 0.251 / 0.127) and match no Q·Kᵀ row (blocked by J2).
6. **Broken scale: VIOLATED.** Z is 2.43× taller and 1.61× wider than V, and Y is 0.38× as wide as Z (blocked by J2).
7. **Wiring lie (forward): now PARTIAL.** Every gold leader now terminates on Z's axis, and V's connector lands at (88.9, 75.0). **But the link sources are wrong.** Two leaders leave from dotted ghost peaks (83.5 and 111.8), which should carry zero weight, while two solid peaks (119.2 and 132.6) feed nothing. The sheet therefore says Z is built from weights the softmax row marks as absent.
8. **Wiring (backward): clean at schematic level.** The ∂L/∂Q, ∂L/∂K and ∂L/∂V curves tap up to just under the Z rail (x 66.9 / 73.8 / 80.3, y 69.8) and continue into the MoE block (ends (94.7, 87.4), (104.5, 90.2), (114.3, 93.0)), and ∂L/∂A and ∂L/∂Z end at (120.6, 92.3) and (128.3, 92.5). That reads as "back from the output, through Z", which is an acceptable chain-rule schematic.
9. **Pen map vs HANDOFF: clean.** Every channel sits on the declared pen, including pen 0 carrying the softmax→Z links and the V→Z connector, now declared.
10. **J1 craft (science side): clean.** Dotted paths are 0.2 mm closed dots at a 1.000 mm median pitch (p5 0.85, p95 1.05), so "ghost / secondary" dotted semantics now read as lines.

## Scores
- truth **5**. The crest lattice topology is exact (d = 34.995 L, loci m = 1…21 to σ < 0.05 mm, caps on loci m 17–37), and the forward wiring now lands on Z. The standing algebra is still false: 5 keys against 3 values against 6 weights, Z at 2.43× max V, and crests stretched 16.7 %. All of these are blocked by J2.
- fidelity **5**. Up from 4: the links terminate correctly and the dots partly carry \|A\|. The halos are still not crest loci, the softmax heights are invented, and the new link-source error sends zero-weight ghosts into Z.
- legibility **6**. Up from 5: the path Q, K → hero → softmax → Z ← V can now be traced by eye end to end. Still missing: the hero wavelength is not derived from any Q/K carrier, the weight row cannot be traced to Q·Kᵀ, and there is no §5 misconception correction because no dossier exists.
- **VERDICT: FAIL**

## Mandates
1. **Links leave from the weights that exist (softmax row y 111.95 → Z axis y 75).** Measured: gold leaders leave from x 76.2, 83.5 (dotted ghost), 90.4, 97.4, 104.7 and 111.8 (dotted ghost). The solid peaks at 119.2 (normalised 0.251) and 132.6 (0.127) have no leader, so 37.8 % of the drawn weight mass never reaches Z. Expected: exactly one leader from each solid peak (76.2, 90.4, 97.4, 104.6, 119.2, 132.6) terminating on Z's axis (x 28.6–96.9), and no leader from the ghosts at 83.0, 111.8 and 125.9. This is J2-compatible: six leaders are kept and two are re-aimed.
2. **Field-dot size is an amplitude channel (hero surround, x 44–166, y 139–194), S3b.** Measured: 151 marks, 0.06–1.50 mm, corr(size, \|A\|) = 0.53, where the radial falloff 1/√r_min alone gives 0.39. Fit: size = 0.43 + 1.03·\|A\|, against the claimed 1.1 + 22·\|A\|. Expected: keep every position (J2) and set each size from \|A\| = \|Σ cos(2π rᵢ/L)/√rᵢ\| in the drawn metric (L = 1.2096, vertical stretch 1.1667), so that corr ≥ 0.9, with zero-size ticks only where normalised \|A\| < 0.1.
3. **Write the claim set down: dossier.md §1/§4/§5/§7 and encoding.md §3–4 (S0).** The plate is on its third workflow round with no stated science, and it shows on the sheet. The hero L (1.21 / 1.41 mm) matches no Q/K carrier (1.81–2.88 mm), the softmax row (6 mirror-symmetric peaks) is derived from nothing drawn, and the "Z = AV" label at (0.18, 0.71) sits over a Z 2.43× taller than any V. Expected: the dossier states which of these the plate claims as computed and which as schematic (J2 reproduction). Give §7 numbers for d/L = 35, the crest m-range, the halo radii, the dot law and the Z/V ratio, plus one §5 misconception the plate corrects. Anything declared schematic stops being scored as a lie. Anything declared computed must then measure true.

## Follow-up on open mandates   id | status | evidence
| id | status | evidence |
|---|---|---|
| S0 | NOT FIXED | still no dossier.md or encoding.md in `studio/resonance/` (now mandate 3) |
| S1a | **FIXED** | V connector ends at (88.9, 75.0), and the 6 softmax leaders end at x 66.9–82.8 on y 75.0, all inside Z's axis 28.63–96.87. Nothing on Y, the MoE lane or mid-air. New defect in the link *sources* (mandate 1) |
| S1b | **ACCEPTED, close** | The lead's reading (gold = the weighted value a_j·V_j flowing into Z) is accepted: it is declared in the HANDOFF pen map, it is the reference's colour, and it is internally coherent. The condition is that each gold leader leaves a non-zero weight, which mandate 1 enforces |
| S1c | NOT FIXED (blocked by J2) | Z amplitude 13.44 vs max V 5.54 (2.43×); Z width 68.24 vs V 42.34; Y width 26.08 |
| S2 | NOT FIXED (blocked by J2) | K 5 rows / V 3 rows / 6 solid peaks + 3 ghosts, mirror-symmetric heights |
| S3a | NOT FIXED (blocked by J2) | crest ry/rx 1.1667 on all 42 loci; halos b/a 0.69–0.70, a/L 27.1 / 32.4 |
| S3b | PARTIAL (deferred) | corr(size, \|A\|) 0.53 (r05's dot set: 0.09; v13's \|A\| dots now restored); target ≥ 0.9 (now mandate 2) |
| regressions | none | Everything that held in r05 still holds: d/L, Q→source 1 / K→source 2, top-2 lanes, plot stats. The r05 "solid crests 1–28 vs claimed 1–21" mismatch is resolved (1–21 on sheet) |
