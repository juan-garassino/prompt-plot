# Science critique — millennium-yang-mills r03 · mathematical physics (quantum Yang–Mills) · 2026-09-29
render: gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_iterate_v7.png (gcode `_v7.gcode`, phys preview `_v7_phys.png`)

The measurements come from parsing the gcode (13 088 commands). The strokes were split on `M3 ; color=N` / `M5`, which gave 31 / 120 / 927 / 7 / 2 strokes on pens 0–4. Fits use y_vac = 50, x_spine = 40 and s = 100 mm/Δ.
The glyph checks come from a physical-width re-render of the gcode strokes at 0.1/0.2/0.2/0.3/0.5 mm.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| #1 Δ/√σ, drawn Δ = s | 3.405(21); 100 mm | 3.405 (json); json M/Δ column is consistent to 5e-5 | vacuum centre (40, 50) to red vertex (40, 150.00) = **100.00 mm**. The red bar is 3 passes at x = 39.6 / 40.0 / 40.4 from y 55.05 to 150 | OK |
| #2 M/Δ of the 5 black shells | 1.4373 1.5495 1.7195 1.7812 1.8561 | same | per-stroke fit of √(E²−p²): **1.43730 1.54949 1.71953 1.78120 1.85609**, std ≤ 3.9e-5 along x ∈ [40, 262] | OK |
| #3 threshold 2Δ; 7 states < 2Δ | 6.810 √σ; 7 | 6.81; 7 | rim fit M = **2.00000** (std 3.4e-5), vertex y = 250.00. Drawn: 0⁺⁺ + 5 black shells. 2⁺⁺* is merged into the rim (0.65 mm, declared in the caption) | OK |
| #4 gap : isolated band | 1 : 1 | — | 100.00 : 100.00 mm (50 → 150 → 250 on the spine) | OK |
| #5 cone 45°; 0⁺⁺ − cone at p = 3 | 45°; 0.1623 | 0.16228 (≈ 1/6 = 0.1667) | all 31 dashes at 45.000°, 0 offset from E = p. p = 3 is off-sheet. At the stop p = 2.22 the red sits **21.48 mm** above the ruling (spec ≥ 18) | OK |
| #6 0⁺⁺ at p = 1 | √2 = 1.4142 | 1.41421 → y = 191.42 | red shell fit M = 1.000001 (std 4.7e-5, range 0.99989–1.00012) | OK |
| #7 non-red ink in the lens {\|p\| < E < √(p²+1)} | 0 | — | **0** (pens 0–3, 1e-3 tolerance). The only disc points are within r ≤ 4.60 of the apex. Red in the lens: the Δ bar plus the Δ glyph at x 27.4–36 (p < 0, outside the half-section domain; sanctioned by encoding §5A) | OK |
| #8 Chen cross-check | 1.401, 1.502 | 1.4014, 1.5024 (also 1.748, 1.784) | not drawn. The caption cites AT2020 only, so no mixing | OK |
| #9 lattice m_G/√σ | 2.468 … 3.346 | 2.468 2.867 3.060 3.205 3.269 3.312 3.308 3.346 | not used (rank-3 thesis) | OK |
| #10 ξ = 1/Δ; ring pitch | 0.2937/√σ; 0.119 fm; 0.851/Δ at r ≈ 8.4 | 0.29369; 0.11949 fm; K₁ ladder 0.25 0.40 0.62 0.92 1.32 1.80 2.36 2.99 3.66 4.38 5.13 5.91 6.71 7.54 8.37; pitch **0.851** at r = 8.37 (1/(1+1.5/r) = 0.848); massless ladder matches | not drawn | OK |
| #11 BPST ∫q = 1; half-max 0.435ρ | 1.000; 0.435 | 1.0000; 0.43498 | not drawn (correct: instantons cut) | OK |
| #12 b₀ | 11 | 11 | not drawn | OK |
| encoding §11.3 staff (mm above red vertex) | 43.7 54.9 72.0 78.1 85.6 | 43.73 54.95 71.95 78.12 85.61 | vertices y = 193.73 204.95 221.95 228.12 235.61 | OK |
| strata (plane) | pitch 1.0, on the rim with a 0.29 inset, top 370 | — | 120 strata, y 251 → 370, pitch **1.000** (min = max). Every left end is at x = 40. Right ends sit on the rim at a perpendicular inset of **0.287–0.292 mm** (99 strata) or the x = 262 crop. **0** strata below the rim or between shells | OK |
| tightest shell pair at the stop | 2.80 mm (A) | 0⁺⁺*/1⁺⁻ at p = 2.22: 3.82 vertical, **3.00 mm** perpendicular | ≥ 0.8 floor | OK |

The dossier has no errors this round. Every §7 number reproduces to the stated digits.

## Lies list
| item | status |
|---|---|
| 1 ink in the gap lens | clean (0 non-red segments; the red bar and glyph only) |
| 2 anything on the cone as a state | clean. There are only grey 6.07/4.05 mm dashes, and no black or red touches the ruling (red is ≥ 21.5 mm above it at the stop) |
| 3 non-uniform / anisotropic scale | clean. The cone is 45.000°, and every shell fits one s on both axes to 4e-5 Δ |
| 4 equally spaced ladder | clean. The vertex gaps are 43.7 / 11.2 / 17.0 / 6.2 / 7.5 / 14.4 mm |
| 5 vacuum as a band or sea | clean. It is one spiral disc centred on (40, 50) with r_ink 4.75 (Ø 9.5) |
| 6 continuum not starting at 2Δ; shell-like plane | clean. The strata are horizontal and start on E = √(p²+4) at a 0.29 mm inset |
| 7 gluon lines / knots / instantons | clean. The statement explicitly says "no massless gluon" |
| 8 MeV/GeV | clean (none on the sheet) |
| 9 "proven" | clean. The colophon reads "…Δ > 0. OPEN." |
| 10 mixing data sets | clean (AT2020 only) |
| 11 approach to the cone = asymptotic freedom | clean (not claimed) |

## Scores
- **truth 10.** Every drawn quantity is exact to ≤ 1e-4 Δ, and the lens is empty. All omissions (2⁺⁺*, states above 2Δ) are declared, and the problem statement is correctly left open.
- **fidelity 9.** Height, width, point, lines and plane each carry exactly their quantity, and the plane has uniform density at a physical pitch. There is one soft spot. The 2Δ rim is drawn in the same black 0.3 as the glueball shells, while the caption says "EACH LINE: ONE GLUEBALL". The rim is tagged `2Δ` and the plane caption names it, so this is a reading ambiguity, not a lie.
- **legibility 8.** The carriers and the twist are now on the sheet (S1, S2), and the tags are clean at nib width (S3).
  - The residuals are two phrasings. "The height of its left end" does not say *above the point, in red-bar units*. "Each line" can be read to include the rim.
  - The stock preview (the HANDOFF's primary render) still fuses `0⁺⁺*` into "0+++" at screen size. It is clean in the physical preview and on paper.

**VERDICT: PASS**

## Mandates
None: the round passes. The following are advisory, for polish only, and non-blocking:
1. Caption line 2 (bottom-right, y ≈ 38): "EACH LINE: ONE GLUEBALL" also covers the black 2Δ rim at y = 250 → 348.8. Consider "EACH CURVE BELOW THE RULED PLANE: ONE GLUEBALL, ITS MASS = ITS HEIGHT ABOVE THE POINT, IN Δ".
2. The HANDOFF's primary render is the stock preview, where the 1.32 mm superscripts and the 1.14 mm star merge. Point reviewers at `_phys.png`.
3. This is not a science mandate, only a flag for the fab gate. The gcode draws at **F1800 / F2200** (4 716 and 2 934 feed words), while the HANDOFF claims "≈ 86 min at F600". Either the feeds or the time claim is wrong.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 name the carriers | **FIXED** | The bottom-right caption reads: "THE POINT: THE VACUUM. / EACH LINE: ONE GLUEBALL, ITS MASS THE HEIGHT OF ITS LEFT END. / RED LINE: THE LIGHTEST GLUEBALL 0⁺⁺, MASS Δ. / RULED PLANE: EVERY PAIR OF GLUEBALLS, FROM EXACTLY 2Δ." "Glueball" and "pair" are both present, outside the lens and plane (0 text points inside x 38–263, y 45–371). The rim ambiguity is advisory note 1 |
| S2 twist in the statement | **FIXED** | "CLASSICAL YANG-MILLS WAVES RUN AT LIGHT SPEED, ON THE DASHED LINE. THE QUANTUM THEORY PUTS NO STATE THERE: NO MASSLESS GLUON, ONLY MASSIVE GLUEBALLS. THE CONE HOLDS ONLY ITS TIP, THE VACUUM. THEN NOTHING, UP TO Δ." There is no "proven" and no MeV |
| S3 J^PC tags readable | **FIXED** (at nib width) | The tag cap is 2.20 mm and the superscripts are **1.32 mm** (≥ 1.3). Sign centres sit 2.32 mm apart, and the ink gap between signs is 1.0 − 0.2 = 0.8 mm. `*` is **3 strokes** (2 diagonals + 1 vertical, 1.14 × 1.32 mm). Decoded rows: 2⁺⁺, 0⁻⁺, 0⁺⁺*, 1⁺⁻, 2⁻⁺, 2Δ. Each tag's centre is within 0.22 mm of its line end at x = 262 (314.47 / 320.73 / 330.80 / 334.62 / 339.37 / 348.80) |
| S4 "within errors" | **FIXED** | "2⁺⁺* LIES ON 2Δ WITHIN ERRORS. STATES ABOVE 2Δ OMITTED." |
| truths held from r02 | **no regression** | The 1 : 1, 45°, shell fits, empty lens and plane-on-rim all still hold. The vacuum grew from Ø3 to Ø9.5 (A1) with its centre still exactly at E = 0, and the red bar starts at y 55.05, just outside the disc edge at 54.75 (0.05 mm clear at nib width). The crop at x = 262 is common to all layers (A2), and the dashes are 6.07/4.05 (A3) |
