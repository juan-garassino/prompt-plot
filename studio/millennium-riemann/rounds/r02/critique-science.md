# Science critique — millennium-riemann r02 · mathematics (analytic number theory) · 2026-09-29
render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.png (+ _phys.png), gcode gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.gcode
thesis: [A] ABSTRACT, the LeWitt instruction drawing (A3 portrait, 3.45 mm/u, σ = ½ at x = 180, real axis y = 32)

Method. I recomputed the dossier values with mpmath 1.4.1 in a scratch target. I parsed the gcode into strokes by `; color=N`:
89 hairline strokes (13.75 m), 79 black (11.35 m), 499 type (3.29 m) and 56 red (0.43 m), in layer order 0→1→2→3.
I did not trust the plate's own data. I mapped every drawn vertex back to s = σ + it and evaluated
ζ directly. The distance to a zero set is taken as |Re ζ| / |ζ'| (or |Im ζ| / |ζ'|) × 3.45 mm.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | γ₁…γ₅; N(50); N(102); γ₃₀ | 14.1347 21.0220 25.0109 30.4249 32.9351; 10; 30; 101.3179 | identical; 10; 30; 101.31785 | 28 red crosses. Centres are within 0.051 mm (perpendicular) of (180, 32 + 3.45 γₙ) for n = 1…28. Top crop at y = 367.86 = t 97.35 (between γ₂₈ = 95.871 and γ₂₉ = 98.831) | OK |
| 2 | zero-free stretch; max gap | none below 14.1347; 6.8873 (γ₁–γ₂) | 14.134725; 6.88731 | The lowest red ink is at y = 79.0 (the arm tip). The centre is at y = 80.94 vs 80.765 expected, which is the double-pass offset (see #3). The column between y = 32.5 and 78 holds only the pole arc (t < 1.1) and the lone hairline crossings at t = 3.436 and 9.67 | OK |
| 3 | 90° X; Im-branch angle at ρ₁, ρ₂, ρ₄ | −9.05°, +12.64°, +30.79° | −9.0455°, +12.6380°, +30.7916° | All 28 X's measure 88.1°–90.0° (tangents on the midline of the double-pass arms; worst deviation 1.9°). Im arm at ρ₁ 171.5° (−8.5°), ρ₂ 13.7°, ρ₄ 30.8°. Largest Im-arm error over all 28 is 2.5° | OK |
| 4 | rulings t = kπ/ln 2; at σ = 10: 4.508, 9.078, 13.614, 18.108 | 4.5324 9.0647 13.5971 18.1294 | kπ/ln 2 exact; at σ = 10 findroot gives 4.5082, 9.0776, 13.6142, 18.1080 | At x = 282 (σ = 30.07) the hairlines end at y = 47.64, 63.27, 78.91, 94.55 … 360.37. That is 22 of 22 matching 32 + 3.45·kπ/ln 2 to 0.01 mm (pitch 15.64) | OK |
| 5 | trivial zeros; ζ′(σ) = 0 | −2 −4 −6 −8; −2.7173 −4.9368 −7.0746 −9.1705 | identical (−9.170493) | Black feet at σ = −1.999, −3.999, −6.001, −8.001 … −14.001. Hairline feet at σ = −2.749, −4.900, −7.100, −9.149 (≤ 0.037 u = 0.13 mm, which is marching-squares grid error) | OK |
| 6 | Gram (B alone on the column) / half-Gram (A alone) | 9.6669 17.8456 23.1703 27.6702 31.7180 / 14.5179 20.6540 25.4915 29.7385 | identical (3.4362 is also a θ = −π root) | Hairline crosses x = 180 at t = 3.436, 9.670, 17.848, 23.171, 27.669, 31.721, 35.47. Black crosses at 25.484, 29.744, 33.622. 14.518 and 20.654 fall inside the red radius of ρ₁ and ρ₂ (1.32 / 1.27 mm), so they are drawn in red as part of the true tongue tip | OK |
| 7 | \|ζ(30i)\|/\|ζ(1+30i)\| | 2.1851 | 2.18510 = (30/2π)^½ | Ink right of x = 182 is 2.23 m against 22.87 m on the left (ratio 0.098). No black lies right of σ = 0.715 | OK |
| 8 | max σ of Re-tongues; nearest A–B approach | 0.715; 0.394 u | 0.715 from `xray_contours.json`; 0.3943 u at (0, 95.79), which is 0.5 u from ρ₂₈ | Black max x = 180.74 → σ = 0.7145 (t = 61.2). Nearest A–B approach away from red and the axis is 1.47 mm = 0.427 u at (177.9, 359.3). No A–B contact < 0.3 mm anywhere except the red centres and the axis | OK |
| 9 | ζ(½), ζ(0), \|ζ′(ρ₁)\|, ring radius at 0.1 | −1.4603545, −0.5, 0.79316, 0.1261 | −1.46035451, −0.5, 0.793160, 0.126078 | not drawn (declared not encoded) | OK |
| 10 | ψ(10.5) and its truncations | 7.8320; 7.7021 (10), 7.8185 (30), 7.8352 (100) | 7.832014; 7.702091; 7.818531; 7.835235 | rank 2, not on this plate | OK |
| — | ζ(σ) = 2 | σ = 1.728647239 | 1.728647239 | — | OK |
| — | curve truth: every vertex on its zero set | — | — | hairline: median 0.0002 mm, max 0.089 mm off Im ζ = 0. Black: max 0.017 mm off Re ζ = 0 (segment midpoints ≤ 0.044 mm). Red: every point ≤ 0.177 mm from a zero set, which is the ±0.15 mm double-pass offset | OK |
| — | completeness (nothing missing) | — | — | Scanlines at 40 heights and 16 columns found 2 124 sign changes of Re ζ / Im ζ, and every one has ink of the right family within 0.15 mm. The 9 hits at 0.150–0.153 mm are inside red arms, at the double-pass offset | OK |
| — | scale isotropy | 3.45 mm/u both axes | — | Horizontal: trivial-zero feet are 6.90 mm apart per 2 u (3.450). Vertical: ruling pitch 15.64 mm = 3.45·π/ln 2 | OK |

## Lies list
| item | status |
|---|---|
| 1 left–right mirror | clean. Right field is hairline rulings only (9.8 % of left ink); no black beyond σ = 0.7145 |
| 2 zeros near the real axis | clean. First red at t = 14.1347; the column is empty of red below y = 79.0 |
| 3 evenly spaced zeros | clean. All 28 heights come from γₙ (≤ 0.05 mm); the gaps visibly run 4.21–23.8 mm |
| 4 pole omitted | clean / n.a. No field is drawn. The Re = 0 arc from −2 lands vertically on the axis at the pole (x = 181.72) |
| 5 invented values | clean. Every vertex was checked against ζ directly |
| 6 "tongues never cross σ = ½" | clean. Black crosses the column alone at the half-Gram points 25.48 / 29.74 / 33.62 …; nothing on the sheet claims otherwise |
| 7 oblique X's | clean. 90° ± 1.9° on all 28 |
| 8 grey \|ζ\| tone | clean. There is no tone anywhere |
| 9 (rank 2) | n.a. |
| 10 caption implying proof | clean. The footer says "VERIFIED TO T = 3·10¹² (PLATT–TRUDGIAN 2021). NOT PROVED." The subtitle states a fact about the drawn window |
| encoding forbidden list §9 | clean. The critical line is not drawn; there are no axes, frames or rings; there is no clipping outside the red radius; text-to-field clearance ≥ 2.25 mm |

## Scores
truth 9 · fidelity 9 · legibility 8 · **VERDICT: PASS**

- truth 9: the drawing is ζ's X-ray, verified vertex by vertex and complete. It loses a point for caption precision (advisory 1).
- fidelity 9: each channel is quantitative (position is s at one scale; weight separates Re from Im; red is location only at a constant size, as declared). Red is 1.5 % of draw length.
- legibility 8: at 1 m the plate reads as a dense comb, a single seam of red and a ruled silence. The one-sided asymmetry (§5) is carried by the data itself. It is held back because nothing on the sheet anchors where σ = ½ sits (advisory 2).

## Mandates
None binding (PASS). Advisory for the next round:
1. **Key text vs sheet.** The key says `3 RED — WHERE BOTH ARE.` But black meets the hairline on the real axis at 7+ trivial zeros (x = 171.38, 164.48 … 129.97, y = 32), where both parts are zero and there is no red. It also meets it at the pole (x = 181.72, y = 32), where ζ = ∞ and is not zero. Say `WHERE BOTH ARE, ABOVE THE REAL LINE.` so the key agrees with the subtitle and with what is drawn.
2. **Location of Re s = ½.** "One scale, 3.45 mm per unit" gives no origin, so a stranger cannot confirm that the red column is σ = ½. The only anchors are unlabelled: the pole foot at x = 181.72 and the trivial-zero feet at −2, −4, … along y = 32. Tiny numerals below the baseline (`−4 −2 1`, at x = 164.48, 171.38, 181.72, y ≈ 29) would let the claim be checked on the sheet without drawing the line.
3. **Production, not science.** The gcode draws at F2000, but HANDOFF quotes ≈ 80 min "at F600". Leo's memory note calls for F600 draw feeds. Either the file or the handoff is wrong.

## Follow-up on open mandates
No `LEDGER.md` exists for millennium-riemann, so there are no open S* mandates. This is first-pass verification of the abstract thesis.
