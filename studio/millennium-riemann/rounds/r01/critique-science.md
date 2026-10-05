# Science critique — millennium-riemann r01 · mathematics (analytic number theory) · 2026-09-29
render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5.png (+ _truewidth.png) · gcode: gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5.gcode
thesis: FAITHFUL (5F), A3 portrait, s = 3.0 mm/u, σ = ½ at x = 148.5, t = 0 at y = 210 (y measured up)

Method: I recomputed everything independently with mpmath 1.4.1 at dps 20. I parsed the gcode into
4 colour layers: 0 = hairline Im ζ = 0 (74 strokes, 11.41 m), 1 = black Re ζ = 0 (63 strokes, 8.26 m),
2 = text + footer (713 strokes, 4.07 m), 3 = red (42 strokes, 0.17 m). Every plotted vertex of layers
0, 1 and 3 was mapped back to s = σ + it and tested against ζ. I also scanned 20 vertical lines,
comparing every true Re = 0 and Im = 0 crossing against the drawn crossings.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?

| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | γ₁…γ₅; N(50); N(102); γ₃₀ | 14.1347, 21.0220, 25.0109, 30.4249, 32.9351; 10; 30; 101.3179 | identical | 20 red crosses at ±γ₁…±γ₁₀. The centre is offset by at most 0.015 mm in x and 0.010 mm in y from (148.5, 210 ± 3γₙ) | OK |
| 2 | no zero below 14.1347; largest gap < 50 | 6.8873 (γ₁–γ₂), min 1.7687 | 6.8873 / 1.7687 | The nearest red ink on the column is 40.59 mm from the real axis (disc edge, r = 2.0 mm). Red-free span 81.2 mm, centres 84.8 mm | OK |
| 3 | Im-branch angle at ρ₁, ρ₂, ρ₄; 90° crossings | −9.05°, +12.64°, +30.79° | −9.05, +12.64, +30.79 (ρ₃ −19.15, ρ₅ −32.89) | Hairline arm tilt −9.5°, +13.9°, +32.6° (all 20 are within 2.5° of −arg ζ′(ρₙ)). Angle between the red chord segments at the centre: 86.5°, 89.3°, 87.2° at ρ₁, ρ₂, ρ₄. Range 85.5–89.6° for ρ₁…ρ₉, and **79.6–79.9° at ±ρ₁₀**. Every red vertex lies ≤ 0.021 mm from the true curve, so the deviation comes from vertex spacing and curvature, not from the geometry (ρ₁'s Im arm has only 3 vertices, 2.61 mm chord) | OK (minor) |
| 4 | right rulings t = kπ/ln 2 | 4.5324·k | 4.5324, 9.0647, 13.5971, 18.1294 | 23 hairlines at x = 281 (11 + axis + 11), pitch 13.59–13.60 mm against 13.597 expected | OK |
| 5 | trivial zeros; ζ′(σ) = 0 on the axis | −2, −4, −6, −8; −2.7173, −4.9368, −7.0746, −9.1705 | identical | Black meets the axis at σ = −1.998, −3.998, −6.001 … −14.001 (±0.02 mm). The hairline chevron vertices fall at −2.70/−2.75, −4.90/−4.95, −7.05/−7.10, −9.15/−9.20 (0.05 u marching grid). The pole arc runs σ ∈ [−2.000, 0.997], \|t\| ≤ 1.013 | OK |
| 6 | Gram 9.6669, 17.8456, 23.1703, 27.6702, 31.7180; half-Gram 14.5179, 20.6540, 25.4915, 29.7385 | same | identical (half-Gram 14.5179 is θ = −π/2) | On σ = ½ the black crosses alone at t = 29.74, 33.62 and 47.16 (and their mirrors), and the hairline crosses alone at 22 places incl. the Gram points. The half-Gram points 14.52, 20.65 and 25.49 fall inside the r = 2 mm discs, so there they are inked red | OK |
| 7 | \|ζ(30i)\|/\|ζ(1+30i)\| | 2.1851 | 2.18509686 = (30/2π)^½ exactly. Also 1.49987 at t = 14.1347 and 2.82095 at t = 50 | Right of the column: black 0.01 m (pole-arc sliver only), hairline 3.10 m. Left of it: 16.56 m | OK |
| 8 | max σ of pen-A tongue (2 < t < 102); nearest A–B | 0.715; 0.394 u (0.453 u for t ≤ 52) | 0.715 at t ≈ 61.2 (0.05 × 0.01 grid). A–B not recomputed to 0.001 | Black max σ in window = 0.637 (t = 47.42). Min A–B away from the red discs and the axis = 1.75 mm (0.58 u). The absolute minimum is 1.0 mm at the left frame clip (σ = −44). Min same-family A–A = 2.98 mm. All ≥ 0.8 mm | OK |
| 9 | ζ(½), ζ(0), \|ζ′(ρ₁)\|, ring radius | −1.4603545, −0.5, 0.79316, 0.1261 | −1.46035450881, −0.5, 0.793160433, 0.126078 | not drawn (declared) | OK |
| 10 | ψ(10.5); truncations; ln p | 7.8320; 7.7021 / 7.8185 / 7.8352; 0.6931, 1.0986, 1.6094, 1.9459 | identical | Footer = ψ₁₀₀(x) − x, **rms 0.022 mm, max 0.18 mm** against my recomputation. Drawn window x ∈ [1.50, 32.50] at 8.61 mm/u and 3.65 mm/u height (the encoding said [2, 32], 8.9 and 4.0; the numerals sit at the true x, so the scale is honest). Cliffs at 2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17 match ψ₁₀₀'s rises to ±0.02 u | OK |
| — | ζ(σ) = 2 at σ = 1.7286472; N(100) = 29 (formula 29.0023); θ min −3.5310 at 6.2898; 2nd root of θ = −π at 3.4362 | as stated | identical | — | OK |
| — | zero-set fidelity (whole field) | grid 0.05 u | — | Distance of vertices from the true set (\|Re ζ\| / \|ζ′\| resp. \|Im ζ\| / \|ζ′\|): black median 0.000, max **0.027 mm**; hairline max **0.021 mm**; red max 0.021 mm. The vertical scans at σ = −40.3 … 44.7 show every true crossing drawn (counts equal, max deviation 0.056 mm). The only mismatches sit at the 2 mm disc edges, from the 0.2 mm joint overlap | OK |
| — | conjugate mirror | exact | — | Reflection across y = 210: max deviation 0.29 mm (= my resampling step) for layers 0 and 1, and 0.09 mm for red | OK |

Encoding-claim miss (not a lie): encoding §5F/§11.3 promised field ink right/left ≤ 10 %, and I measure
**18.8 %** (3.10 m of rulings against 16.56 m). The right half still reads as quiet, but the "≥ 10 : 1 by ink"
proportion claim is false. It is the translator's estimate, not ζ.

## Lies list       item | clean / VIOLATED (where)

| # | item | status |
|---|---|---|
| 1 | left–right mirror | clean. Only 0.01 m of black lies right of the column (the pole loop), and there are no balance marks |
| 2 | zeros near the real axis | clean. No red within 40.59 mm of y = 210, and the 2 ticks sit outside the field (y 48.9–53.9, 366.1–371.1) |
| 3 | evenly spaced zeros / "32.0" | clean. Heights are exact to 0.015 mm, the gaps visibly unequal. No "32.0" |
| 4 | pole omitted from a field | n/a (no field). The pole is present implicitly as the end of the black loop at σ = 0.997 |
| 5 | invented positions | clean. Vertex residual is ≤ 0.027 mm everywhere |
| 6 | "tongues never cross σ = ½" | clean. Lone black crossings at t = ±29.74, ±33.62, ±47.16 are visible, and no caption claims otherwise |
| 7 | oblique X on an isotropic plate | clean (isotropic 3.0/3.0). Chord angles are 85.5–89.6° except ±ρ₁₀ at 79.6–79.9° (curvature at a 0.47 mm chord; vertices on-curve) |
| 8 | grey \|ζ\| tone | clean |
| 9 | footer jumps at primes only | clean. Cliffs at 4, 8, 9, 16, 25, 27, 32 are drawn and labelled at 1.6 mm |
| 10 | RH implied proved | clean, marginally. The top statement "ALL NONTRIVIAL ZEROS LIE ON THE CRITICAL LINE RE S = ½." (y ≈ 382) is declarative, but "?" (y ≈ 297) and "NOT PROVED" (y ≈ 78) qualify it |

Caption-vs-sheet falsehoods found (not on the §4 list, but they fail "is what is drawn what the caption says"):
- "RED: WHERE BOTH ARE. A ZERO OF ζ." (x = 190, y ≈ 107). Black meets hairline, un-red, at the 22 trivial
  zeros σ = −2 … −44 and at the pole s = 1 (σ = 0.994), which is not a zero. The legend is contradicted 23 times.
- "THE ZEROS CHOOSE THE SEAM OF A PICTURE THAT IS NOT SYMMETRIC." (x = 190, y ≈ 336–343). The picture IS
  exactly symmetric top–bottom (measured 0.29 mm). Only left–right fails.
- "ζ(s) = Σ n⁻ˢ = Π (1 − p⁻ˢ)⁻¹" (y ≈ 310) carries no "Re s > 1". Both sides diverge on 100 % of the drawn
  field left of σ = 1.
- The window, scale and zero count are nowhere on the sheet (0 of 713 text strokes). Dossier §4 allows
  "fewer zeros … and saying which window it is".

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL

- **truth 8.** The drawn mathematics is exemplary: both zero sets are within 0.027 mm, the 20 zeros within
  0.015 mm, the rulings at kπ/ln 2 to 0.01 mm, the trivial zeros to 0.02 mm, and ψ₁₀₀ to 0.022 mm rms.
  Two captions are literally false against the sheet (red legend, "not symmetric").
- **encoding fidelity 8.** Every channel is exact and isotropic. Red is location-only, as declared, and the
  footer numerals sit at the true x. What is missing is the window, scale and count that make "20 crosses"
  a declared crop rather than "all the zeros", plus the unmet ink-ratio claim.
- **insight legibility 7.** The phenomenon lands at 3 m: a comb on the left, ruled silence on the right, and every
  red X stacked in one undrawn column with a long empty stretch around the axis. But the most eye-catching
  un-red features, the chevron vertices on the axis and the central loop, are mislabelled by the legend.
  The only symmetry claim on the sheet contradicts the exact top–bottom mirror the viewer can see. A stranger
  counting 20 crosses under "ALL NONTRIVIAL ZEROS" is not told these are the first 10 (and their mirrors) of ≈1.2·10¹³ checked.

**VERDICT: FAIL** (legibility 7 < 8). The fixes are text-layer only. No geometry needs to move.

## Mandates        1. … 2. … 3. …

1. **Red legend contradicts the real axis.** Quantity: black–hairline meetings without red. Measured: 23
   on y = 210 (trivial zeros at σ = −2, −4, …, −44 and the pole at σ = 0.994 ≈ 1). The legend
   "RED: WHERE BOTH ARE. A ZERO OF ζ." (right void, x = 190, y ≈ 107) implies 0. Expected: the legend
   restricts red to meetings **off the real axis = nontrivial zeros**, and a line names the axis meetings,
   e.g. "ON THE REAL AXIS (THE LONG HAIRLINE) THEY ALSO MEET AT THE TRIVIAL ZEROS −2, −4, −6 … AND AT THE
   POLE S = 1." Stroke font: "−" is available, and "½" is already authored.
2. **Undeclared window, scale and zero count.** Quantity: the extent of the crop the sheet states. Measured:
   none. The plate shows σ ∈ [−44, 45], |t| ≤ 51.37 at 3.0 mm/u on both axes, 20 crosses = ±γ₁…±γ₁₀.
   Expected, per dossier §4 ("fewer zeros … and saying which window it is"): one caption line in the
   lower right void (between the rulings at y ≈ 92–107, or the band y ≈ 44–50 under the field). For example:
   "|IM S| ≤ 51.37: THE FIRST 10 ZEROS AND THEIR MIRRORS · −44 ≤ RE S ≤ 45 · 3 MM PER UNIT ON BOTH
   AXES · ≈1.2·10¹³ MORE ARE VERIFIED ABOVE." (N(3·10¹²) ≈ 1.24·10¹³ by Riemann–von Mangoldt.)
3. **Symmetry and Euler-product captions are false as printed.** Quantity: symmetry of the drawn field.
   Measured: an exact top–bottom mirror (max deviation 0.29 mm = sampling step, all layers) and a
   left–right ink ratio of 16.56 m : 3.10 m. The caption "…A PICTURE THAT IS NOT SYMMETRIC." (x = 190,
   y ≈ 336–343) should read "…NOT LEFT–RIGHT SYMMETRIC" (optionally "— ONLY TOP–BOTTOM, ζ(s̄) = conj ζ(s)").
   In the same void, "ζ(s) = Σ n⁻ˢ = Π (1 − p⁻ˢ)⁻¹" (y ≈ 310) needs its domain, "(RE S > 1)". Without it
   the formula is false over the whole drawn comb (σ ≤ 1).

## Follow-up on open mandates   id | status | evidence

Pass 1 (r01). No LEDGER.md exists for millennium-riemann, so there are no open S* mandates to follow up.
