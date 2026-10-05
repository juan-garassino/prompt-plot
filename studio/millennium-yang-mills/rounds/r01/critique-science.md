# Science critique — millennium-yang-mills r01 · mathematical physics (quantum Yang–Mills gauge theory) · 2026-09-29
render: gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_faithful_v10.png (+ .gcode, 9172 cmds; physical-width preview rounds/r01/phys_preview_v10.png)

Method: gcode parsed per `; color=N` layer into strokes (pen0 38 dashes / pen1 110 strata / pen2 445 text strokes / pen3 7 / pen4 6).
Sheet frame read from geometry: vacuum centre (122.00, 60.00), s = 100 mm per Δ on both axes (p = (x−122)/100, E = (y−60)/100).

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | Δ/√σ ; Δ drawn = s | 3.405(21) ; apex→0⁺⁺ | 3.405 (json) | vacuum centre y 60.00 → red vertex y 160.00 = **100.00 mm** | OK |
| 2 | M/Δ 2⁺⁺,0⁻⁺,0⁺⁺*,1⁺⁻,2⁻⁺ | 1.4373 1.5495 1.7195 1.7812 1.8561 | 1.4373 1.5495 1.7195 1.7812 1.8561 | vertices at x=122: y 203.73 / 214.95 / 231.95 / 238.12 / 245.61 → **1.4373 1.5495 1.7195 1.7812 1.8561** (43.73, 54.95, 71.95, 78.12, 85.61 mm above red vertex); every shell fits √(p²+M²) to **≤ 0.010 mm** (vertices and chord midpoints) | OK |
| 3 | threshold 2Δ; states below | 6.810 √σ; 7 | 6.810; 7 (json flags agree) | rim vertex y 260.00 (E = 2.0000), fit ≤ 0.007 mm; 6 lines below it drawn + 2⁺⁺* merged (declared in caption) | OK |
| 4 | gap : isolated band | 1 : 1 | 1 : 1 | 100.00 : 100.00 mm | OK |
| 5 | cone half-angle; √10−3 | 45°; 0.1623 | 45°; 0.16228 (vs 1/6 = 0.1667) | all 38 dashes at **45.000°**, 6.00 mm dash / 4.00 mm gap; p=3 off-sheet (frame p ≤ 1.60) — red sits 28.7 mm above cone at right stop (20.3 mm ⟂, spec ≥ 18) | OK |
| 6 | 0⁺⁺ at p=1 | √2 = 1.4142 | 1.41421 | red polyline fits √(p²+1) to 0.008 mm over p ∈ [−1.07, 1.60] | OK |
| 7 | non-red ink in lens | 0 strokes | — | clipped every G1 (0.05 mm tol): pen0 **0**, pen1 **0**, pen2 **0**, pen3 only the vacuum spiral (r ≤ 1.35 mm, 7.5 mm of ink), pen4 125 mm (Δ bar + Δ glyph, allowed in faithful) | OK |
| 8 | Chen ratios | 1.401, 1.502 | 1.401, 1.502 (1⁺⁻ 1.748, 2⁻⁺ 1.784) | not drawn; drawn set is AT2020 only | OK |
| 9 | lattice m_G/√σ | 2.468 … 3.346 | 2.468 2.867 3.060 3.205 3.269 3.312 3.308 3.346 | §2c not used | OK (n/a) |
| 10 | ξ = 1/Δ; ring pitch | 0.2937/√σ, 0.119 fm; 0.851 at r≈8.4 | 0.29369; 0.1195 fm; exact K₁ e-fold ladder 0.25,0.40,0.62,…,7.54,8.37 with pitch 0.851 at r=8.37 (asymptotic 1/(1+1.5/r) = 0.848) | §2b not used | OK (n/a) |
| 11 | BPST charge; half-max | 1.000; 0.435ρ | 1.0000; 0.43498 | not drawn (correctly) | OK (n/a) |
| 12 | b₀ SU(3) | 11 | 11 | not drawn | OK (n/a) |

Other measurements: strata **110**, all horizontal, pitch **1.000 mm** exactly, y 261…370 (E 2.01…3.10); every stratum end on the rim sits **0.283–0.287 mm** ⟂ from it (spec 0.29); none below the rim, none between shells. Vacuum spiral r = 1.35 mm (+0.15 half-nib = Ø 3.0 ink). Red Δ bar y 61.9→101.3 and 118.7→160.0 (starts 0.4 mm clear of disc ink; touches 0⁺⁺ vertex exactly); red glyph 8.9 × 8.4 mm centred at E = 0.500 (spec 12 mm — cosmetic). Min ⟂ gap between neighbouring shells ≈ 4.0 mm (0⁺⁺*/1⁺⁻). Tags centred on each black exit (±0.1 mm); 0⁺⁺ tag 2.04 mm above the red.
Dossier itself: all 12 check numbers reproduce; json M/Δ column consistent with M/√σ ÷ 3.405 for all 20 states. No dossier error found.

## Lies list       item | clean / VIOLATED (where)
| # | lie | status |
|---|---|---|
| 1 | anything in gap lens but vacuum + Δ measure | clean — 0 non-red segments; red = bar + glyph only |
| 2 | anything on the cone as a state | clean — no pen1–4 ink within 0.6 mm of either ruling outside the disc; cone dashed grey |
| 3 | non-uniform / anisotropic scale | clean — 45.000°, vertex heights exact to 0.01 mm on one s |
| 4 | equally spaced ladder | clean — vertex gaps 43.7, 11.2, 17.0, 6.2, 7.5, 14.4 mm |
| 5 | vacuum as band/sea | clean — one Ø 3 mm solid disc |
| 6 | continuum not at 2Δ / as shells | clean — strata start 0.28 mm off the rim, horizontal (not shell-parallel) |
| 7 | gluon line / glueball shapes / instantons | clean — no knots, no gluon label |
| 8 | MeV without caveat | clean — no MeV/GeV anywhere; Δ is the unit |
| 9 | "proven" | clean — "CLAY PROBLEM: PROVE … OPEN." |
| 10 | mixing data sets | clean — AT2020 only |
| 11 | shells→cone = asymptotic freedom | clean — not claimed |
Note (not a violation): caption "2⁺⁺* SITS ON 2Δ" — it is 1.9935 ± 0.017 Δ, 0.65 mm below the rim; "ON 2Δ WITHIN ERRORS" is the exact statement.

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 9** — every drawn quantity is right to 0.01 mm; the only looseness is "sits on 2Δ" (within errors, not on).
- **encoding fidelity 8** — all channels quantitative and exact; one crop inconsistency: the red 0⁺⁺ runs to p = 1.60 (x 282) while the six black curves and the plane stop at p = 1.44 (x 266), leaving ≈ 940 mm² of the continuum region (x 266–282, rim→y 370) as blank paper — the same blank that elsewhere encodes "no state".
- **insight legibility 7** — the empty lens lands instantly for a physicist; for a stranger the sheet never says what the three elements are or why an empty light cone is surprising. On-sheet text contains 0 occurrences of "glueball"/"particle"/"continuum", no gloss for the J^PC tags, and no word on the classical waves travelling at light speed (the CMI twist, dossier §1/§5) or "no gluon" (the misconception, §5). The correction is present in the geometry but not readable.
- **VERDICT: FAIL** (legibility 7 < 8)

## Mandates        1. … 2. … 3. …
1. **Name point / line / plane on the sheet** — measured: 0 words identify the disc, the 7 curves or the 110 strata (lower-left caption band y 15–28, 4 lines). Expected: one caption line there mapping them, e.g. `POINT: THE VACUUM. LINES: ONE GLUEBALL EACH, E = √(p²+M²). PLANE: TWO GLUEBALLS, FROM 2Δ UP.` — text stays in the E < 0 band, nothing enters the lens or the plane.
2. **Put the twist in the statement** — measured: statement (baseline ≈ 386, y 385–388) says only "THE LIGHT CONE HOLDS ONLY ITS TIP, THE VACUUM. THEN NOTHING, UP TO Δ."; 0 words on why the cone matters. Expected: add the CMI clause and the misconception fix, e.g. `CLASSICAL YANG-MILLS WAVES RUN AT LIGHT SPEED, ON THE DASHED CONE. THE QUANTUM THEORY PUTS NOTHING THERE: NO GLUON, ONLY MASSIVE GLUEBALLS.` Keep ≥ 14 mm clear of the strata top (y 370), as now.
3. **One momentum crop for every element** — measured: red 0⁺⁺ ends at x 282.0 (p 1.60, y 248.68) while black shells, rim and strata end at x 266.0 (p 1.44); the 0⁺⁺ tag (x 269–273, y 242.1–244.4) is left 2.04 mm above a red line that then runs 9 mm past it through the tag column, and ≈ 940 mm² of continuum region (x 266–282, y 306–370) is unstrata'd blank. Expected: stop the red at x = 266 (exit y 235.32) and centre its tag on 235.3 like the other six — or carry curves, rim and strata all to x = 282 — so no in-frame continuum reads as empty.

## Follow-up on open mandates   id | status | evidence
None — r01, no LEDGER for this slug (pass 1 only).
