# Science critique — millennium-riemann r03 · mathematics (analytic number theory) · 2026-09-29
render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.png (+ _phys.png), gcode gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.gcode
thesis: [A] ABSTRACT, r02 polish (A3 portrait, 3.45 mm/u, σ = ½ at x = 180, real axis y = 32, t ≤ 97.35)

Method. I recomputed the dossier values with mpmath 1.4.1 in a scratch target. I parsed the gcode into strokes by `; color=N`:
89 hairline strokes (13.75 m), 79 black (11.35 m), 597 type (3.70 m) and 56 red (0.208 m; r02 had 0.43 m).
I mapped every drawn vertex back to s = σ + it and evaluated ζ directly. The distance to a zero set is taken as
|Re ζ| / |ζ'| (or |Im ζ| / |ζ'|) × 3.45 mm. I did not open piece.py, NOTES.md, SYNTH.md or any round .py,
and I did not run the round's audit script.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | γ₁…γ₅; N(50); N(102); γ₂₈/γ₂₉ | 14.1347 21.0220 25.0109 30.4249 32.9351; 10; 30; — | identical; 10; 30; 95.87063 / 98.83119 | 28 red crosses, one per γ₁…γ₂₈. Each arm passes ≤ 0.023 mm from (180, 32 + 3.45 γₙ). Top crop at y = 367.86 = t 97.35, mid-gap between γ₂₈ and γ₂₉ | OK |
| 2 | zero-free stretch; largest gap < 50 | none below 14.1347; 6.8873 | 14.134725; 6.887314 (min 1.76868; γ₂₇–γ₂₈ 1.21929) | Lowest red ink at y = 79.09 (arm tip of ρ₁; centre y = 80.76). Below that the column holds only the pole arc foot, the hairline at t = 3.436 and 9.670, and black at t = 0.813 (the pole arc) | OK |
| 3 | 90° X; Im-branch angle at ρ₁, ρ₂, ρ₄ | −9.05°, +12.64°, +30.79° | −9.0455°, +12.6380°, +30.7916° | **Chord X at 0.4 mm radius: 88.1°–90.0° (median 89.4°) on all 28.** Im arm at the centre segment: ρ₁ 171.7° (exp 171.0), ρ₂ 13.0° (12.6), ρ₄ 31.0° (30.8). The worst Im-arm error on all 28 is 4.3° on short (≤ 0.1 mm, 0.01 mm-quantised) segments. At 1.2 mm radius the drawn chords open to 80.9°–90.0°. The true curves give the same values: ρ₂₅ 81.0° true vs 80.9° drawn, ρ₁₄ 83.7 vs 83.5, ρ₂₈ 82.5 vs 82.7. That is real curvature of the tongue tip, not a geometry error | OK |
| 4 | rulings t = kπ/ln 2 | 4.5324 9.0647 13.5971 18.1294 | exact | 21 rulings + the axis end at x = 282 at y = 32 + 3.45·kπ/ln 2. Max deviation 0.00 mm (pitch 15.64) | OK |
| 5 | trivial zeros; ζ′(σ) = 0 | −2 −4 −6 −8; −2.7173 −4.9368 −7.0746 −9.1705 | −2.717263 −4.936762 −7.074597 −9.170493 | Black feet at σ = −1.999, −3.999, −6.001 … −18.001, and the pole foot at 0.999. Numerals `−4 −2 1` are centred at x = 164.48 / 171.38 / 181.72 (true 164.475 / 171.375 / 181.725), 1.6 mm caps, y 27.2–28.8 | OK |
| 6 | Gram (hairline alone) / half-Gram (black alone) on the column | 9.6669 17.8456 23.1703 27.6702 31.7180 / 14.5179 20.6540 25.4915 29.7385 | identical (g₀ = 17.8456; θ = −π/2 at 14.51792; 3.4362 also a θ = −π root) | Hairline crosses x = 180 at t = 3.436, 9.670, 17.848, 23.170 (vertex on the column), 27.669, 31.721, 35.47. Black crosses at 25.484, 29.744, 33.622. 14.518 and 20.654 lie inside the red radius of ρ₁ and ρ₂ and are drawn red, as part of the true tongue tip | OK |
| 7 | \|ζ(30i)\|/\|ζ(1+30i)\| | 2.1851 | 2.185097 = (30/2π)^½ | Ink right of x = 182 is 2.13 m against 23.18 m on the left (ratio 0.092) | OK |
| 8 | max σ of Re-tongues; nearest A–B approach | 0.715; 0.394 u | 0.715 (json) | Black max σ is 0.7145 in the upper field; the only black further right is the pole-arc foot at σ = 0.999, t = 0. Neither family's ink comes within 1.594 mm of a red centre (the substitution clip), and the red overlaps each join by 0.2 mm (r = 1.8) | OK |
| 9 | ζ(½), ζ(0), \|ζ′(ρ₁)\|, ring radius | −1.4603545, −0.5, 0.79316, 0.1261 | −1.46035451, −0.5, 0.793160, 0.126078 | not drawn (declared not encoded) | OK |
| 10 | ψ(10.5) and its truncations; ln p | 7.8320; 7.7021 / 7.8185 / 7.8352 | 7.832014; 7.702091 / 7.818531 / 7.835235; 0.6931 1.0986 1.6094 1.9459 | rank 2, not on this plate | OK |
| — | ζ(σ) = 2 | 1.728647239 | 1.7286472390 | — | OK |
| — | curve truth (every vertex on its zero set) | — | — | Hairline, 2,394 vertices: median 0.0002 mm, p99 0.008, max 0.089 mm off Im ζ = 0 at (140.59, 48.65). Black, 2,148 vertices: max 0.017 mm off Re ζ = 0. **Red, 578 vertices: max 0.023 mm** (r02: 0.177 mm, the double-pass offset). The pen mapping is confirmed: colour 0 lies on Im = 0 and colour 1 on Re = 0 | OK |
| — | completeness | — | — | 14 scanlines + 10 columns found 1,114 sign changes of Re ζ / Im ζ, and every one has ink of the right family within 0.064 mm. There are 0 misses | OK |
| — | red one-pass (A1) | — | — | 56 strokes, 2 per zero (one Re arm, one Im arm). 0 direction reversals in any arm. Two red arms come within one nib (0.5 mm) of each other only ≤ 0.52 mm from the centre, i.e. at the crossing itself | OK |

## Lies list
| item | status |
|---|---|
| 1 left–right mirror | clean. The right field holds the hairline rulings only (9.2 % of left ink). No black lies right of σ = 0.7145 above the axis |
| 2 zeros near the real axis | clean. First red at t = 14.1347; no red below y = 79.09 |
| 3 evenly spaced zeros | clean. All 28 heights come from γₙ (≤ 0.023 mm) |
| 4 pole omitted | clean / n.a. No field is drawn. The Re = 0 arc from −2 lands on the pole foot (x = 181.72), which is now labelled `1` |
| 5 invented values | clean. Every vertex was checked against ζ |
| 6 "tongues never cross σ = ½" | clean. Black crosses the column alone at 25.484 / 29.744 / 33.622 … |
| 7 oblique X's | clean. 88.1–90.0° at 0.4 mm chord. The wider-chord opening matches the true curves to ≤ 0.2° |
| 8 grey \|ζ\| tone | clean. There is no tone |
| 9 (rank 2) | n.a. |
| 10 caption implying proof | clean. The sheet says `VERIFIED TO T = 3·10¹² (PLATT–TRUDGIAN 2021). NOT PROVED.` |
| encoding §9 forbidden list | clean. The critical line is not drawn; there are no axes, rings or frames; no clipping beyond the red radius (0 mm of black/hairline inside r < 1.4); type-to-field clearance ≥ 2.76 mm; the numerals sit below the baseline, outside the field |

## Scores
truth 9 · fidelity 9 · legibility 9 · **VERDICT: PASS**

- truth 9: the drawing is ζ's X-ray. It is exact vertex by vertex, complete, and the red is now exact too (0.023 mm, where the double pass was 0.177 mm). The key no longer contradicts the axis.
- fidelity 9: position is s at one isotropic scale (feet 6.90 mm per 2 u; rulings at 3.45·π/ln 2). Weight separates Re from Im. Red is location only, at a constant r and one pass. Red is 0.8 % of draw length.
- legibility 9: the anchors `−4 −2 1` sit on the true feet, so a stranger can find σ = ½ as the point 1/2 u left of `1` and check the red column against it. The one-sided comb carries the §5 correction by itself.

## Mandates
None binding (PASS). Advisory only:
1. **Pole label.** `1` sits under a black-meets-hairline foot at (181.72, 32) where ζ = ∞, not 0. The key now restricts red to above the real line, so nothing is contradicted. But a stranger may still read `1` as a fourth zero next to `−2` and `−4`. A word such as `POLE` in the bottom-left caption would close this. Optional.
2. **Do not "fix" the wide-chord X's.** At 1.2 mm radius the red X's open to 80.9° (ρ₂₅) and 82.7° (ρ₂₈). The true curves give 81.0° and 82.5°: this is tongue-tip curvature, and the tangents at the centre are 90°. Any request to straighten the arms would violate encoding §9.9.
3. **Production note.** `plot plate --dry-run` lists 4 swap waits (one per layer), but only 2 are physical: layers 1 and 2 share the black 0.3. The operator should know to skip the prompt between colour 1 and colour 2.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 key agrees with sheet | **FIXED** | The key now reads `3 RED / WHERE BOTH ARE, / ABOVE THE REAL LINE.` There is no red on y = 32; all black–hairline meetings on the axis are unaccented, as the key now allows |
| S2 anchor σ = ½ | **FIXED** | `−4`, `−2`, `1` are centred at x = 164.48 / 171.38 / 181.72, against the true feet at 164.475 / 171.375 / 181.725 (≤ 0.005 mm). Caps are 1.6 mm, y 27.2–28.8, and the numerals are 3.2 mm below the axis hairline |
| A1 red one pass, no knot (science measurement only) | **FIXED** | 56 one-way strokes, 0 reversals. Red length 0.208 m, against 0.43 m in r02. Two arms come within a nib of each other only ≤ 0.52 mm from the centre. In the true-width crop (x 170–190, y 330–368) each mark shows two arms with cream in all four quadrants. The art critic owns the final call on the look |
| A2 type on declared lines (a) | **FIXED (a)** | The minimum type-to-field distance is 2.76 mm, at (206.73, 357.47), against 2.25 mm in r02. The series caption `MILLENNIUM PRIZE PROBLEMS 1 / 7 / CLAY MATHEMATICS INSTITUTE, 2000` is present top-right. Items (b) and (c) are for the art critic |
| A3 HANDOFF minutes = plate job | **FIXED** | I re-ran `plot plate … --dry-run`: 31 / 26 / 28 / 3 min, ETA ≈ 94 min, bounds ok. This matches the HANDOFF exactly |
| regressions | none | Every r02 truth holds: rulings 0.00 mm, feet ≤ 0.001 u, hairline max 0.089 mm (unchanged), black max 0.017 mm, completeness 0 misses, ink ratio 9.2 % (r02: 9.8 %) |
