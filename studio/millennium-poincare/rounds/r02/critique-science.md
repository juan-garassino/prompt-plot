# Science critique — millennium-poincare r02 · mathematics (geometric topology, Ricci flow) · 2026-09-29
render: gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.png (+ `_phys.png`), gcode `gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.gcode`
(pass 1 — no LEDGER.md exists for this slug)

Method: I recomputed the analytic dumbbell myself (ρ(z) = √(ℓ²−z²)(α+β(z/ℓ−ζ)²), ℓ=2, α=0.16,
β=1.05, ζ=0.18) and checked the dossier's `data/neckpinch.npz` against the stated PDE
(ψ_t = ψ_ss − (1−ψ_s²)/ψ, evaluated at the neck minimum and the lobe maximum; the residual is
below 0.3 %). My own fixed-x explicit solver was unstable at the poles, so I did not re-run the
flow independently. I rebuilt all 46 expected isochrones from the npz in the frame the HANDOFF
states: neck pinned at (165, 200), axis at 62°, 62 mm/unit, and for each piece the ψ²ds-centroid
held at its t_s position. I then compared them against 12,914 mm of layer-0 ink parsed from the
gcode.

**Global match:** 99.79 % of layer-0 ink samples lie within 0.5 mm of a recomputed isochrone, and
99.84 % within 1 mm. The few off-curve samples sit on rings A1–A3, where my 0.005-snapshot time
interpolation is least accurate.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | r² = r₀² − 4t; post-surgery slopes | −4; A −4.003, B −3.908 | A −4.02 (fit ψ_max<0.35), T_A 0.3873; B −3.52 over ψ_max<0.35 (B is not yet round there), T_B 0.1177, and the tail ψ_max 0.092 @ 0.115 gives T ≈ 0.1171 | ring spacing on the A equator widens inward, 1.40 → 7.55 mm | OK |
| 2 | neck / big / small at t=0; R_min | 0.3143 / 1.4139 / 0.6765; 0.2213 | 0.3143 / 1.414 / 0.6765 (neck/big 0.2223); R_min 0.217 (FD) > 0; L₀ 6.0059; vol 44.574 | waist of the start line: 19.49 mm per side = 0.3143·62 | OK |
| 3 | neck −62 %, lobe −12 % by t_s | 0.3143→0.1197, 1.4139→1.2447 | t_s = 0.054647 (first neck ≤ 0.12: 0.11971), −61.9 % / −12.0 %, small lobe 0.4709 | waist keyline 7.43 / 7.42 mm per side (0.1197·62 = 7.42) | OK |
| 4 | T_pinch; d(ψ²)/dt | ≈0.0628; −1.74 → −1.78 → −2 | T_pinch 0.0630 (quadratic extrapolation); −1.61 / −1.66 / −1.69 at ψ 0.20 / 0.15 / 0.13; initial dψ/dt: formula −2.243 vs data −2.268 | waist fan steps 0.66 (merged) · 1.56 · 1.76 · 2.07 · 2.53 · 3.49 mm, accelerating inward | OK |
| 5 | event order | 0.063 < 0.1171 < 0.3873 | confirmed | B has 6 rings, A has 33 rings (all 33 + 6 found on equator rays, ±0.1 mm) | OK |
| 6 | roundness at death, L/ψ_max → π | A 3.140, B 3.185 | A 3.321 → 3.140; B 4.569 → 3.178 | last ring A: 6.43 / 6.42 mm along the axis vs 6.44 mm on the equator; B: 6.29 vs 6.12 mm | OK |
| 7 | 2-D control | widens to 0.3554; A₀ 25.346; T 1.0085 | A₀ 25.347; T = A₀/8π = 1.0085; initial 2-D neck rate +0.938 (widens). I did not re-run to 0.3554, but the sign and magnitude are consistent | caption reads "(0.314 → 0.355)" | OK (magnitude not re-solved) |
| 8 | planar CSF | A₀ 3.3180, T 0.5281 | A₀ = π(1+0.045+0.01125) = 3.3183, T 0.5281 | not drawn (declared) | OK |
| 9 | closed geodesics, stuck loop | s = 1.601 / 3.856 / 5.141; length 1.975 | s = 1.598 / 3.855 / 5.139; 2π·0.3143 = 1.9749 | not drawn in this thesis | OK |
| 10 | Gauss–Bonnet | 2π; 4π | 2π(1−ψ_s) with ψ_s = 0 → 2π exactly | not drawn | OK |
| — | red caps (cut radius h) | h = 0.12 | 0.11971·62 = 7.42 mm | 2 semicircles, 23.3 mm each ⇒ r = 7.42; diameter chord 14.85 mm at 152° (⟂ 62°); centre (164.87, 199.75) | OK |
| — | extinction points | ψ²ds-centroids | A (109.42, 95.47), B (195.26, 256.91) | A (109.29, 95.22), B (195.13, 256.66); both off by 0.28 mm; collinear with the cut at 62.0° / 242.0° | OK |
| — | Δt grid | 0.01 anchored at t_s | 5 past lines + 33 A + 6 B | A equator crossings match the recomputed t_s+0.01k within ≤ 0.02 mm (A1–A33); B equator within ≤ 0.06 mm | OK |
| — | start line (t = 0) | off-grid, declared in HANDOFF | pre-5 (t = 0.0046) sits 0.66–1.2 mm from the start line | pre-5 is inked on only 21 of 128 "free" samples, so it is ≈90 % merged. The outermost visible gap on the A equator is 3.38 mm (Δt 0.0146) against 2.0 mm neighbours. The on-sheet caption says only "ONE LINE = Δt 0.01" | minor |

**Dossier findings:**
- **(i)** Lie #4 ("do not show the lobes shrinking visibly before surgery") cannot be satisfied by
  a truthful drawing. By t_s the big lobe loses **0.169 units** of radius, which is **87 % of the
  neck's absolute loss (0.195)**: 10.5 mm against 12.1 mm at 62 mm/unit. The 62 % vs 12 % contrast
  is *relative*, not absolute. §2(a)'s "time-lines pile up on the lobes" is also false at the
  lobe equator: pre-surgery lines there are 2.0 mm apart at Δt 0.01.
- **(ii)** Encoding §4's waist-step row is labelled "mm @ 50" in a spec that is nominally 60 mm/unit
  and rendered at 62. At 62 the steps are 0.66 / 1.56 / 1.76 / 2.07 / 2.53 / 3.49 mm (measured
  identical).
- **(iii)** Encoding §4's claim "lobe halo lines merge (<0.8 mm), that merge is standing still"
  is not realized on the sheet, and could not be at a truthful scale. The only merges happen at
  the poles, where lengthening under neck-pinning drives them.

## Lies list       item | clean / VIOLATED (where)
| # | item | verdict |
|---|---|---|
| 1 | tidy row of elongated loops | clean: the rings turn round (last ring A aspect 1.00, B 1.03) and the gaps widen inward (A 1.40 → 7.55 mm) |
| 2 | CSF shrinking the neck loop | clean (not drawn) |
| 3 | pinch under 2-D flow | clean: the caption states that rings are 2-spheres and that the 2-D neck would widen |
| 4 | wrong event order / visible lobe shrinkage | order is clean (6 < 33 rings, pinch before either death). The "visible lobe shrink" clause is a dossier defect (finding i); the sheet shows the true 10.5 mm loss |
| 5 | surgery on a fat neck | clean: cap 7.42 mm vs lobe ψ_max 77.2 mm, ratio 1 : 10.4 |
| 6 | uneven or undeclared Δt | clean on the grid (±0.02 mm). The start line is off-grid and declared only in HANDOFF, not on the sheet (minor) |
| 7 | drawn surface presented as S³ | clean: "EVERY CHORD A ROUND 2-SPHERE", "IN SECTION" |
| 8 | "loops contract" as the proof | clean |
| 9 | credit / history | clean: Perelman 2002-03, after Hamilton (1982), Fields 2006 + Clay 18 Mar 2010 both declined, arXiv IDs correct |
| 10 | extra pinches / handles | clean |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 9**: every drawn line is the recomputed isochrone to ≤ 0.1 mm. Waist, caps, dots, ring
  counts and every caption number check out.
- **fidelity 8**: the time spacing is honest, and occlusion and merge follow the declared rules.
  Deductions: the keyline is 2 coincident passes (strokes of 733.9 mm, 0.00 mm offset) and so
  carries no visible channel; the start line is off-grid and not captioned on the sheet.
- **legibility 7**: the cut and the two dying nests land. But:
  - The "neck races while the lobe stands still" story does not show. The waist halo is 12.07 mm
    per side, and the big-lobe equator halo is 11.48 mm with constant 2.0 mm steps.
  - Past vs future is not coded on the sheet. The t_s line looks identical to the 45 others, so
    a stranger reads a two-hill contour map.
  - The A-pole convergence renders as 26 dash fragments of 2.2–11 mm. They look like a
    hidden-line convention.

**VERDICT: FAIL** (legibility 7 < 8)

## Mandates        1. … 2. … 3. …
1. **Relative neck-vs-lobe loss.** The quantity is fractional radius loss from t=0 to t_s:
   neck 61.9 %, big lobe 12.0 %.
   - Measured on the sheet it appears only in absolute mm. The waist fan ⟂ the 62° axis through
     (165, 200) is 12.07 mm per side (19.49 → 7.42). The big-lobe halo on the equator ray through
     (109.3, 95.2) is 11.48 mm (87.65 → 76.18, steps ≈2.0 mm).
   - The eye therefore sees equal motion. The expected read is a **5:1 relative contrast**.
   - Encode it in a true channel, not by re-spacing. Examples: halo spacing expressed as a
     fraction of the local radius at the waist vs the lobe, or a scaled on-sheet mark of
     0.314→0.120 vs 1.414→1.245.
   - Correct dossier lie #4 and encoding §4's "lobe halo merges" claim, which the true geometry
     contradicts (0.169 vs 0.195 units absolute).
2. **The t_s keyline and the direction of time.**
   - Measured: the keyline is 2 coincident passes of the same 0.3 black (strokes 46/47, 733.9 mm
     each, zero offset). On the sheet it is indistinguishable from the 5 past and 39 future
     lines.
   - Expected: the cut instant reads as the boundary between past (outside) and future (inside),
     e.g. the 0.5 nib, or a stated weight, on the 733.8 mm keyline passing tangent to the red
     caps at the waist (±7.42 mm).
   - Add one caption clause: "outside = before the cut, inside = after".
3. **A-pole fragments.** The lower-left flank of piece A, ≈(45–140, 35–85) mm, plus B's crown
   ≈(187–234, 271–297), carry **31 layer-0 fragments shorter than 15 mm (26 on A, 5 on B)**.
   They are pause/occlusion leftovers of rings A1–A13 and pre-1…pre-5, which recompute to lie
   within 2.0 mm of each other at A's pole (49.2–51.2 mm from the dot).
   - Expected: the declared merge reads as **one continuous line** where the geometry converges
     ("draw it as a merge, not a crowd", dossier §6), with no dashed look.
   - At the same time, caption the off-grid start line (t = 0; the outermost gap on the A equator
     is Δt 0.0146 = 3.38 mm).

## Follow-up on open mandates   id | status | evidence
none. There is no LEDGER.md for millennium-poincare, so this is a pass-1 cold verification.
