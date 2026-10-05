# Science critique — millennium-navier-stokes r02 · mathematical physics (fluid dynamics, PDE regularity) · 2026-09-29
render: gallery/studio/millennium_navier_stokes/trials/pp_millennium_navier_stokes_abstract_v15.png (+ .gcode, A3 portrait, seed 7)
Pass 1 (cold). No `LEDGER.md` exists, so there are no open S* mandates to follow up.

Measured from the gcode: 425 blue strokes / 10.94 m · 20 black rings / 2.91 m · 877 type strokes / 3.89 m · 30 red strokes / 0.24 m.
Total ink is 17.98 m. Rungs were assigned by stroke midpoint. Rung centres and radii come from the stroke bounding boxes, and the δ₀ = 20 mm fit comes from the pitch profile.

## Check numbers

| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| C1 | r(v_max)/δ | 1.12091 (s = 1.25643) | 1.1209064 (s = 1.2564312) | tightest ring gap 1.50 mm at r = 22.51 mm = **1.126 r_c** (r_c = 20) | OK |
| C2 | v_max·2πδ/Γ | 0.63817 | 0.6381727 | n/a (not drawn) | OK |
| C3 | core pitch | 7.9577 rad/e-fold, 1.2665 turns, β₀ = 7.162° | 7.957747, 1.266515, 7.1625° | median β in the hero: 7.73° at ρ 0.2–0.5 (theory 7.72), 8.91 (8.90) at 0.5–0.8, 11.39 (11.36) at δ, 27.08 (27.15) at 2δ, 48.46 (48.43) at 3δ, 62.43 (62.41) at 3.9δ | OK, exact Burgers Re_Γ = 100 |
| C4 | closed form vs RK4 | r = 0.406006δ, 8.73230 rad | 0.4060058δ, 8.7323010 rad (RK4 identical to 8 digits) | n/a | OK |
| C5 | planar div | −α vs 0 | −α / 0 | all 425 blue strokes run inward (r_start > r_end), all CCW. The 20 black rings are closed (end gap 0.000 mm) and concentric (centre scatter ≤ 0.06 mm, radial std 0.04 mm) | OK |
| C6 | ω₀ | 7.95775 | 7.957747 | n/a | OK |
| C7 | ladder λ = 2 | 22, 11, 5.5, 2.75, 1.375, 0.6875; Σ → 1.33325 | same; 1.3332520 | R = **80 : 40 : 20 : 10 : 5.02**, so the ratio is 2.00 at every step. δ₀ = **20** mm (captioned "CORE 20 MM", inside the allowed [12.8, 25.6)), so δ₅ = 0.625 mm < 0.8 and rung 5 is correctly absent. Rung 1 scaled ×2 onto the hero: median deviation 0.010 mm, 100 % within 0.3 mm. Rungs 2–4 are subsets of the same set (cull). Centres are collinear at −49.7°, with steps 144.0, 72.0, 36.0, 18.0 mm | OK (orbit factor is 1.20, not the encoding's 1.10, but still self-similar) |
| C8 | ∫[…]² ds | ½ | 0.4950 on [1e-6, 200] + 1/200 tail = 0.500 | n/a | OK |
| C9 | 2D eye / equal Δψ | tightest at ≈ 1.12 r_c | — | ln s + E₁(s) differences between successive rings with r_c = 20 mm: **0.0956 constant, CV 0.03 %** (r_c = 18 or 22 gives CV 5 %). The rings are exactly equal-Δψ. Inner ring 6.26 mm, outer ring 38.9 mm (1.95 r_c) | OK |
| C10 | 2026 status | 4^0.01 = 1.0140, 4^0.06 = 1.0867 | 1.013959, 1.086735 | stamp: "CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH · FORCED CASE NOT YET VERIFIED · CLAY: NO AWARD · WITHOUT A PUSH: OPEN". Dated, conditional, forced, unforced open | OK |
| C11 | single-arm eye | 1.465 / 1.832 / 2.453 mm | 1.4653 / 1.8316 / 2.4527 (2.93 at d 1.6) | innermost blue r: 1.36 / 0.70 / 0.69 / 0.63 / 0.51 mm (rungs 0–4). Minimum self-wrap gap: 1.62 / 0.834 / 0.829 / 0.823 / 0.855 mm. **Minimum stroke-to-stroke blue gap ≥ 0.8 mm (0 violations), red–blue ≥ 0.8 mm** | OK (the floor holds; the hero eye is 1.36 mm, not the encoding's "≈ 2.9") |
| C12 | turns 5δ → 0.5δ | 0.598 / 1.196 / 2.393 | 0.59814 / 1.19627 / 2.39255 | consistent with the fitted pitch | OK |
| C13 | one arm, 5δ₀ → 1.83 mm | 300 mm, 3.39 turns | 300.21 mm, 3.394 turns | longest hero stroke 253.8 mm (R_out = 4δ, not 5δ) | OK |

Other measurements:
- **Red ring at L.** Centre (248.36, 52.43), r = 11.50 mm, 2 closed passes. From the measured orbit, L = C₄ + 18.0 mm along the diagonal = (248.35, 52.51), and |C₅ − L| + R₅ = 9.0 + 2.5 = **11.5**, so the ring is exact. It clears rung 4's rim by 1.5 mm and contains nothing blue.
- **Separation.** Ring disc to hero rim 48.7 mm (≥ 25 required). Hero : ring-disc area = 80² : 38.9² = 4.2 : 1.
- **Red share.** 240 mm / 17 977 mm = **1.34 %**, over the encoding's "< 1 %" (the red "WITHOUT A PUSH: OPEN" line adds 96 mm).
- **Type outside the drawable area.** x ∈ [14.55, 282.32] against the [15, 282] frame, over by 0.45 mm on the left and 0.32 mm on the right.
- **Rung ink density** (length / πR²; hero taken uncropped as 2 × rung 1): **0.357, 0.714, 0.838, 0.643, 0.662 mm/mm²**. See mandate 2.

## Lies list

| # | item | status |
|---|---|---|
| 1 | converging spiral as planar flow | clean ("SEEN DOWN THE STRETCHING AXIS · THE FLUID LEAVES THROUGH THE PAGE") |
| 2 | spiral streamlines for 2D | clean (20 closed, concentric, equal-Δψ circles) |
| 3 | 2D eye shrinking | clean |
| 4 | Burgers called blow-up / singularity | clean. The hero eye is blank blue with no red mark, and the red sits only at the ladder limit L. **Borderline in the headline, see lie 8** |
| 5 | fake spirals | clean (pitch matches θ(s) to ≤ 0.1° across ρ 0.2–3.9 in rungs 0–2) |
| 6 | ladder off ratio / pitch drift | clean (2.00 exact, congruent to 0.01 mm) |
| 7 | nested rungs as one instant | clean ("NS SCALING: COPIES, NOT ONE INSTANT") |
| 8 | status lies | **Stamp clean. Headline VIOLATED in spirit** (y ≈ 380, "…THE SPIRAL IS THE THIRD DIMENSION, AND IT CAN KEEP SHRINKING."). Whether a 3D vortex can keep shrinking on its own, with finite energy and no push, is exactly the open unforced question (A)/(B). The ladder only shows that scaled copies exist. A steady Burgers vortex shrinks only when an external strain α is raised, and it has infinite energy (lie 4). As a flat assertion, the headline answers the open question "yes". |
| 9 | "large → small" on 2D | clean (Kraichnan note in the colophon) |
| 10 | 2D saddle as "where it breaks" | clean (no saddle drawn) |
| 11 | "turbulence is the unsolved problem" | clean, but the correction is never made on the sheet (see legibility) |

## Scores

- **truth: 7.** The geometry is exact everywhere it could be measured: Burgers pitch within 0.1°, Lamb–Oseen Δψ with CV 0.03 %, 2:1 rungs congruent to 0.01 mm, and the red ring exactly at the orbit limit. The stamp is correct. The one-line statement, the first sentence a stranger reads, asserts the open answer ("IT CAN KEEP SHRINKING").
- **encoding fidelity: 7.** Every blue line is a true streamline and every ring is a true isoline. The rung density channel, however, runs backwards at the end of the ladder. Density measures 0.357, 0.714, 0.838, 0.643 and 0.662 mm/mm², so rung 3 is 23 % lighter than rung 2, while ω₀ rises ×4 per rung. Even before the floor, line density scales ×2 per rung, which is √ of the ω₀ ratio. The two smallest vortices read as the weakest, which is the opposite of the physics, and no caption explains it. Minor: the red share is 1.34 % against < 1 %, the orbit factor is 1.20 against 1.10 (still self-similar), and the type sits 0.45 mm outside the frame.
- **insight legibility: 7.** Rings against spiral lands at a glance, and the "COPIES, NOT ONE INSTANT" ladder is clear. But the sheet never says what "finishing" means: vorticity or velocity becoming infinite at one point in finite time. So the §5 correction (the question is blow-up of a smooth flow, not the chaos of turbulence) does not reach a stranger. "BLOW-UP" appears only in the stamp, undefined.

**VERDICT: FAIL**

## Mandates

1. **Headline truth.** The statement line at y ≈ 380, x = 15–285 reads "…THE SPIRAL IS THE THIRD DIMENSION, AND IT CAN KEEP SHRINKING." That is an unconditional "can". The expected wording is conditional, matching C10 and lie 8. For example: "…THE SPIRAL IS THE THIRD DIMENSION — WHETHER IT CAN SHRINK TO A POINT ON ITS OWN IS THE OPEN QUESTION." The sheet must not assert, anywhere, that an unforced finite-energy vortex can shrink without end.
2. **Rung ink density must not fall as vorticity rises.** Measured density per rung (length / πR²) is 0.357, 0.714, 0.838, **0.643, 0.662** mm/mm² at rungs 3–4, centres (225.1, 79.9) and (236.7, 66.2). Rungs 3–4 have only 202 mm and 52 mm of line, 38 % and 20 % of their congruent share. The expected result is monotone non-decreasing density down the ladder, so rungs 3–4 should be ≥ 0.84 mm/mm², with saturation at the floor and no reversal. Either change the cull so it keeps density at the floor value, for example by keeping the outer arm segments and dropping only inner ends, or declare on the sheet that ink density is the pen floor and not ω. In that second case the ladder caption must carry "ω₀ ×4 PER RUNG" as text.
3. **Name what blows up.** The limit caption at x ≈ 190–262, y ≈ 40–52 ("IF THE LADDER FINISHES, IT FINISHES HERE, IN 4/3 OF THE FIRST RUNG'S TIME…") never says what finishes. The quantity is peak vorticity, ×4 per rung, and ∫sup|ω|dt = ∞ as the rungs → ∞ (BKM): infinite at one point in finite time. The word "BLOW-UP" in the stamp is otherwise undefined. The expected result is one line on the sheet, for example: "VORTICITY ×4 EACH RUNG → INFINITE AT ONE POINT IN 4/3 T₀. THAT, NOT TURBULENCE, IS THE QUESTION". This carries the dossier §5 correction to a stranger.

## Follow-up on open mandates

| id | status | evidence |
|---|---|---|
| — | n/a | No `studio/millennium-navier-stokes/LEDGER.md`, so there are no open S* mandates. Pass 1 only. |
