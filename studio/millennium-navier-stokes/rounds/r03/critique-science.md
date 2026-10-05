# Science critique — millennium-navier-stokes r03 · mathematical physics (fluid dynamics, PDE regularity) · 2026-09-29
render: gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_iterate_v8.png (+ `_phys.png`, `.gcode`; A3 portrait, seed 7)
Pass 2 (follow-up). This round opened `LEDGER.md` for the open S* mandates.

Measured from the gcode:
- pen 0 hero: 99 strokes, 3.86 m
- pen 1 rungs 1–4: 360 strokes, 6.41 m
- pen 2 rings: 18 closed rings, 2.37 m
- pen 3 type: 1122 strokes, 4.74 m
- pen 4 red: 2 strokes, 0.163 m
- total draw 17.532 m, which matches the HANDOFF

How the measurements were taken:
- Rungs were assigned by rim start point.
- Centres and radii come from least-squares circle fits to the stroke start points. The rim std is ≤ 0.004 mm in every rung.
- Pitch was measured from per-segment tangent angles against the radius.

## Check numbers

| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| C1 | r(v_max)/δ | 1.12091 (s = 1.25643) | 1.1209064 (s = 1.2564312) | Tightest ring gap is 1.500 mm, between rings at 18.76 / 20.26 / 21.76 mm. The minimum sits at ≈ 20.2 mm, which is 1.12 r_c for r_c = 18 | OK |
| C2 | v_max·2πδ/Γ | 0.63817 | 0.6381727 | n/a | OK |
| C3 | core pitch | 7.9577 rad/e-fold, 1.2665 turns, β₀ 7.162° | 7.957747, 1.266515, 7.1625° | Median β per rung (measured / theory at bin centre):<br>ρ 0.35: 7.80 / 7.61<br>ρ 0.65: 8.99 / 8.76<br>ρ 1.0: 11.29 / 11.24<br>ρ 2: 27.30 / 27.11<br>ρ 3: 48.31 / 48.52<br>ρ 4: 63.61 / 63.56<br>ρ 4.9: 71.65 / 71.66<br>Rungs 0 and 2–4 agree with this to ≤ 0.7°. A free fit on rung 1 gives Re 102, δ 8.9 mm (the nominal values are 100 and 9.0) | OK, exact Burgers Re_Γ = 100 |
| C4 | closed form vs RK4 | r = 0.406006δ, 8.73230 rad | closed form 0.4060058δ, 8.7323010 rad; RK4 is identical to 8 digits | n/a | OK |
| C5 | planar div | −α vs 0 | −α / 0 | Blue: every stroke runs rim → eye and every stroke turns CCW.<br>Black: 18 rings, closure gap 0.000 mm, centre scatter ≤ 0.001 mm at (178, 298), radial std ≤ 0.003 mm | OK |
| C6 | ω₀ | 7.95775 | 7.957747 | n/a. The sheet states it as "×4 EACH RUNG" | OK |
| C7 | ladder λ = 2 | 22 … 0.6875; Σ → 1.33325 | same; 1.3332520 | **Plate δ₀ = 18 mm**, captioned "CORE 18 MM" and inside [12.8, 25.6). So δ = 18 / 9 / 4.5 / 2.25 / 1.125 / 0.5625 mm, and rung 5 correctly falls under 0.8 and is not drawn.<br>R = **90.00 : 45.00 : 22.50 : 11.25 : 5.625**, which is 2.000 at every step. Hero R_out = 5δ.<br>Centres are collinear at −36.81° (±0.002°), with steps 162.00 / 81.00 / 40.50 / 20.25 mm. That is self-similar at orbit factor 1.20.<br>Rung 1 ×2 against the hero, inside the crop: median 0.16 mm, 99.6 % within 0.3 mm.<br>Rungs 2–4 ×2 are strict subsets of the rung above (100 % within 0.3 mm), so they are the cull | OK |
| C8 | ∫[…]² ds | ½ | 0.5000000 | n/a | OK |
| C9 | 2D eye / equal Δψ | tightest ≈ 1.12 r_c | — | Successive ln s + E₁(s) with r_c = 18 mm: Δ = 0.10623, **CV 0.014 %**. At r_c = 17 or 19 the CV is ≈ 3 %, so the rings are exactly equal-Δψ at r_c = δ₀.<br>Inner ring 5.95 mm, outer ring 35.00 mm (1.94 r_c). Gaps 2.58 → 1.50 → 1.86 mm | OK |
| C10 | 2026 status | 1.0140, 1.0867 | 1.013959, 1.086735 | Stamp, black, x = 282 right-aligned, y ≈ 20–31: "CLAIMED 8 SEP 2026 · BLOW-UP WITH A SMOOTH PUSH / FORCED CASE NOT YET VERIFIED · CLAY: NO AWARD / WITHOUT A PUSH: OPEN". It is dated, conditional and forced, and it says the unforced case is open | OK |
| C11 | single-arm eye | 1.465 / 1.832 / 2.453 mm | 1.4653 / 1.8316 / 2.4527 | Innermost blue r in rungs 1–4: 0.70 / 0.68 / 0.62 / 0.49 mm. The hero's centre is at (3.0, 262.8), off-frame, so its innermost visible r is 12.27 mm.<br>**Min blue–blue gap 0.824 mm, with 0 violations under 0.8**<br>Min self-wrap gap 0.829 mm<br>Red–blue gap 1.76 mm | OK |
| C12 | turns 5δ → 0.5δ | 0.598 / 1.196 / 2.393 | 0.59814 / 1.19627 / 2.39255 | consistent with the C3 fit | OK |
| C13 | one arm 5δ₀ → 1.83 mm | 300 mm, 3.39 turns | 300.21 mm, 3.394 turns | n/a at δ₀ = 18. The hero is cropped | OK |

Other measurements:
- **Red ring at L.** Centre (262.416, 68.689), r = 12.937 mm, 2 closed passes.
  - The orbit limit is L = C₀ + 324 mm along −36.807°, which is (262.41, 68.69).
  - The encoding rule gives |C₅ − L| + R₅ = 10.125 + 2.8125 = **12.9375 mm**.
  - So the ring is exact to 0.001 mm.
  - It clears rung 4's rim by 1.69 mm, and 0 blue points lie inside it.
- **Red share.** 162.6 / 17 532 mm = **0.93 %**, under 1 % (r02 was 1.34 %). The stamp moved from red to black, so red now means only "where the ladder would finish". The encoding §4 row "status → red type" has drifted. The HANDOFF declares the change, and it is not a truth defect.
- **Type in frame.** The type bbox is x ∈ [15.00, 282.00] and y ∈ [19.2, 397.8], so the r02 overhang is fixed. No type point lies within ~2 mm of any line.
- **Separation.** Ring disc to hero rim: 53.5 mm. Ring disc to rung 1: 59.8 mm. Both are ≥ 25 mm.
- **Rung ink density** (length / πR²). The hero is taken as its congruent share, 2 × rung 1 over π90².

  | rung | density (mm/mm²) |
  |---|---|
  | 0 | 0.370 |
  | 1 | 0.739 |
  | 2 | 0.825 |
  | 3 | 0.790 |
  | 4 | 0.773 |

  Rung 0 → 1 is ×2.00, the scaling. Rung 1 → 2 is only ×1.12, so the floor already binds at ¼, as the caption says. After that the density is flat within −4 % / −6 %. The r02 drop was −23 %.
- **Within-rung spacing** in rung 1, perpendicular to the flow. The stroke count halves at discrete radii: 192 → 96 → 48 → 18. As a result the gap cycles between 0.96 and 1.43 mm, ±20 % around 1.2. On the sheet this shows as 3–4 faint spiral void bands at ρ ≈ 0.6–0.8 (visible in `_phys.png`). They are seeding artefacts, not structure of the axisymmetric field. They are minor, but see advisory 2.

## Lies list

| # | item | status |
|---|---|---|
| 1 | converging spiral as planar flow | clean ("IN SPACE: A SPIRAL · SEEN DOWN THE STRETCHING AXIS · THE FLUID LEAVES THROUGH THE PAGE") |
| 2 | spiral streamlines for 2D | clean (18 closed, concentric, equal-Δψ circles) |
| 3 | 2D eye shrinking | clean ("THE EYE ONLY OPENS") |
| 4 | Burgers called blow-up | clean. Blow-up is attached only to "IF THE LADDER FINISHES". There is no red on any spiral eye |
| 5 | fake spirals | clean. Pitch matches θ(s) to ≤ 0.7° over ρ 0.35–4.9 in every rung |
| 6 | ladder off ratio / pitch drift | clean (2.000 exact, congruent to 0.16 mm, subsets below) |
| 7 | nested rungs as one instant | clean ("NS SCALING: COPIES, NOT ONE INSTANT") |
| 8 | status lies | clean. The headline is now conditional: "WHETHER IT CAN SHRINK TO A POINT ON ITS OWN IS OPEN." The stamp is correct |
| 9 | "large → small" on 2D | clean. "LARGE SCALES TO SMALLER ONES" heads the ladder caption only, and the colophon says "IN 2D, ENERGY RUNS TO LARGER SCALES (KRAICHNAN 1967)" |
| 10 | 2D saddle as "where it breaks" | clean (no saddle drawn) |
| 11 | "turbulence is the unsolved problem" | clean, and now actively corrected: "THAT BLOW-UP, NOT TURBULENCE, IS THE QUESTION." |

## Scores

- **truth: 9.** Every family is exact:
  - Burgers pitch to ≤ 0.7°
  - Lamb–Oseen Δψ CV 0.014 % at r_c = δ₀
  - rungs 2.000 : 1 and congruent
  - red ring at the orbit limit to 0.001 mm

  Every sentence on the sheet is now true and correctly conditional. That includes the headline, the blow-up definition, the 4/3 time, the pen-floor claim ("FROM 1/4 ON", measured ×1.12 at rung 2) and the stamp.
- **encoding fidelity: 9.** Every blue line is an exact streamline and every black ring is an exact isoline. Ring spacing carries speed, and rung size carries NS scaling exactly. The density channel runs ×2 then floor, which is now declared in words together with "VORTICITY ×4 EACH RUNG", so no channel misleads. Residuals:
  - a −6 % density drift over rungs 2 → 4
  - ±20 % stroke-count halving bands inside a rung
  - the status stamp moved off red (declared in the HANDOFF; encoding text drift)
- **insight legibility: 8.** "Flat = rings, space = spiral" reads at a glance. The ladder, its terminus and the definition of blow-up are now said in plain words, and the §5 correction is on the sheet. The one weakness is the dominant mass. The hero's centre sits 12 mm outside the frame, at x = 3.0, so the biggest blue form shows no eye and no core wrap. It reads as a fan of curved combs, and the spiral statement is actually carried by rung 1. The "IN SPACE: A SPIRAL" caption sits between the two, at x 15–62, y 150–165.

**VERDICT: PASS** (all ≥ 8)

## Mandates

PASS, so there are no binding mandates. Three advisories for the lead, if the art side reworks the hero:

1. **Hero core.** The hero centre is at (3.0, 262.8), 12 mm left of the x = 15 frame, and the innermost visible stroke is at r = 12.27 mm (0.68 δ₀). Moving C₀ to x ≥ 15 + 3 mm would put the eye (C11: ≈ 1.4 mm at δ₀ 18) and ≥ 1 core wrap on the sheet. The rim crop could stay as it is. The orbit must move with it (factor 1.20, ½ ratios). Then the dominant mass states "spiral" by itself.
2. **Within-rung spacing.** In rung 1 (C₁ = (132.7, 165.7), R 45) the perpendicular gap cycles between 0.96 and 1.43 mm at the arm-halving radii (ρ ≈ 0.6–0.8). That makes 3–4 spiral void bands, which suggest arm structure the axisymmetric Burgers field does not have. Stagger the terminations, or seed by J–L so the spacing stays within ±10 % of d_sep. The hero is the same set ×2.
3. **Encoding housekeeping, for the translator along with S5.** The status channel is now black type, not red. Record that red = L ring only, and δ₀ = 18 mm, R_out = 5δ.

## Follow-up on open mandates

| id | status | evidence |
|---|---|---|
| S1 | **FIXED** | Statement at y ≈ 375–382, x = 15: "FLAT, A WHIRLPOOL IS ONLY RINGS. THE SPIRAL IS THE THIRD DIMENSION. WHETHER IT CAN SHRINK TO A POINT ON ITS OWN IS OPEN." It is conditional, and "on its own" = unforced (A)/(B), which is open (C10). No line on the sheet asserts unforced shrinkage |
| S2 | **FIXED** | The limit block, right-aligned at x = 282, y ≈ 45–57, reads: "IF THE LADDER FINISHES, IT FINISHES HERE, IN 4/3 OF THE FIRST RUNG'S TIME: VORTICITY ×4 EACH RUNG, INFINITE AT ONE POINT. THAT BLOW-UP, NOT TURBULENCE, IS THE QUESTION." It names the quantity, the ×4 rate, the finite time and the §5 correction. A5 holds: there is no "T0" glyph |
| S3 | **FIXED** (declared branch) | Density is 0.370 / 0.739 / 0.825 / 0.790 / 0.773 mm/mm². It is not strictly monotone: −4 % at rung 3 and −6 % at rung 4, against r02's −23 %. The mandate's second branch is met in full: the ladder caption says "FROM 1/4 ON, THE INK IS THE 0.8 MM PEN FLOOR", the limit block says "VORTICITY ×4 EACH RUNG", and the floor measurably binds at ¼ (×1.12, not ×2) |
| — regressions | none | Every r02 truth still holds: pitch, equal Δψ, 2:1 congruence, the red ring at L, blue gap ≥ 0.8, and red–blue ≥ 0.8. r02's type overhang and 1.34 % red share are also fixed |
