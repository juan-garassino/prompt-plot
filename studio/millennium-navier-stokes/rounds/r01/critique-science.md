# Science critique — millennium-navier-stokes r01 · mathematical physics (fluid dynamics, PDE regularity) · 2026-09-29
render: gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.png (gcode: gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.gcode)

Method: parsed the gcode into pen-down strokes per `; color=N` (blue 643 strokes / 15.54 m · black-hairline 70 / 4.61 m ·
type 872 / 3.12 m · red 107 / 0.51 m). Rung centres were found by minimising the residual of the Burgers closed form
θ(s) = θ₀ + (Re/8π)[(1−e^{−s})/s + E₁(s)] fitted to every blue stroke, which makes each centre an exact eye rather than an
eyeballed one. Blue spacing is an exact inter-stroke nearest-point test (0.02 mm densified, 1 mm hash) plus a same-stroke
one-wrap test. I did not open piece.py, NOTES.md or SYNTH.md.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| C1 | r_max/δ (Burgers), r/r_c (L–O) | 1.12091 (s 1.25643) | 1.120906 (s 1.256431) | ring disc: tightest gap between r 23.57 and 25.12 mm, mid 24.35 = 1.107 r_c (on a 22-ring lattice) | OK |
| C2 | v_max | 0.63817 Γ/2πδ | 0.638173 | not drawn directly (it is carried by ring spacing, see C9) | OK |
| C3 | core pitch | 7.9577 rad/e-fold, 1.2665 turns, β₀ 7.162° | 7.957747, 1.266515, 7.1625° | per-stroke fit of θ vs G(s): Re = 100.00 (rung 0), 99.99 (1), 99.97 (2), 99.75 (3), 99.27 (4); arc residual median 5–9 µm | OK |
| C4 | closed form vs RK4 | r 0.406006, 8.73230 rad | closed form 0.406006 / 8.732301; my RK4 0.40600585 / 8.73230102 | — | OK |
| C5 | planar divergence | −α (2D: 0) | −α | blue: inward spirals, drawn rim→eye (start r = R exactly); black 2D: 22 closed circles, closure gap 0.000 mm, radial std ≤ 0.003 mm | OK |
| C6 | ω₀ | 7.95775 | 7.957747 | not drawn | OK |
| C7 | ladder λ=2 | 22, 11, 5.5, 2.75, 1.375, 0.6875; Σ→1.33325 | same; 1.333252 | rim radii 88.00 / 44.00 / 22.00 / 11.00 / 5.50 mm → ratios 2.000 each; δ = R/4 = 22, 11, 5.5, 2.75, 1.375; rung 5 not drawn | OK |
| C8 | ∫[…]²ds = ½ | ½ (numerics 0.49966) | 0.49500 truncated at s = 200; the tail 1/200 restores 0.5000 | not drawn | OK (the 0.49966 is truncation-dependent, which is harmless) |
| C9 | 2D eye / equal Δψ | t×4 ⇒ eye×2; tightest at ≈1.12 r_c; 24 rings | formula confirmed | 22 rings, Δψ = 0.0900 (Γ/4π units) for every step (spread 0.03 %); inner r 6.18 mm (encoding said 6.6), outer r 44.00; tightest gap 1.551 mm at 1.107 r_c; outer gap 1.979 mm | OK |
| C10 | 2026 status | forced, unverified, unforced open; 1.40 %/rung, 8.7 %/6 rungs | 1.013959, 1.086735 | red stamp: "CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH (UNVERIFIED) / WITHOUT A PUSH: OPEN"; no pitch drift across rungs (Re 99.3–100.0) | OK |
| C11 | blank eye (single arm) | 1.465 mm (d 0.8) | 1.46531 | innermost ink r: hero 1.39 mm, rungs 1–4 0.70 / 0.68 / 0.63 / 0.53 mm; min same-stroke wrap gap 1.69 / 0.83 / 0.86 / 0.88 / 0.90 mm | OK (the floor holds; the encoding's "hero eye ≈ 2.9 mm" is not what was built) |
| C12 | turns 5δ→0.5δ | 0.598 / 1.196 / 2.393 | 0.59814 / 1.19627 / 2.39255 | max turns per stroke: hero 3.72 (rim 4δ → eye) | OK |
| C13 | one arm 5δ→1.83 mm | 300 mm, 3.39 turns | 300.21 mm, 3.394 turns | the hero is truncated at 4δ (encoding allowed this); longest stroke ≈ 3.7 turns | OK |
| — | blue–blue floor ≥ 0.8 mm | encoding §10 | — | exact: **0 inter-stroke pairs < 0.8 mm**; same-stroke wraps ≥ 0.83 mm | OK |
| — | side view r²\|z\| = C | encoding §4 | — | 32 curves about axis x = 66.33 (= hero centre x, collinear), stagnation y = 110; r²\|z\| relative spread 0.04 % (r¹: 21 %, r³: 22 %); C levels 1064.5·(1,3,5,…,15), which is equal Stokes-ψ steps | OK |
| — | ladder orbit | factor 1.10, gaps 13.2/6.6/3.3/1.65 | — | a similarity orbit: step ratio 0.500/0.500/0.501, Δφ = −20.0° per step; **factor 1.225** (rim gaps 29.8/14.9/7.4/3.7 mm); fixed point L = (249.98, 43.97) vs red-ring centre (250.00, 44.00) | OK on physics; the factor departs from the encoding (composition only) |
| — | red ring | r = \|C₅−L\| + R₅, 2 passes, empty | predicted 11.84 mm | r 11.65 mm (fit std 0.18), 2 closed passes (74.3 / 72.1 mm); blue inside: 0 points; clearance to rung-4 rim 1.00 mm | OK |
| — | rung congruence | rungs 0–1 exact copies | — | 211 of 256 rung-1 seed phases coincide with rung-0 phases within 0.002 rad at 0.07° rotation (the other 45 fall in the hero's frame-cropped sector); crossing counts at 2δ: 64 and 64 | OK |

## Lies list
| item | status |
|---|---|
| 1 converging spiral presented as planar | clean ("IN SPACE: A SPIRAL · SEEN DOWN THE STRETCHING AXIS · FLUID LEAVES THROUGH THE PAGE") |
| 2 spiral streamlines for 2D vortex | clean: 22 exact closed circles, one stroke each |
| 3 2D eye that shrinks | clean ("THE EYE ONLY OPENS: t ×4 → EYE ×2") |
| 4 Burgers called blow-up/singularity/counterexample | clean (the ladder is conditional: "IF THE LADDER FINISHES…"; the eyes are blue, not red) |
| 5 fake spirals | clean: every blue stroke fits the Burgers θ(s) at Re 100 to µm residual |
| 6 ladder off ratio / pitch drift | clean: 2.000 radii, Re 99.3–100.0 in every rung |
| 7 nested rungs as one instant | clean ("COPIES, NOT ONE INSTANT") |
| 8 status lies | clean: dated, "claimed", "unverified", forced ("smooth push"), and unforced still open |
| 9 "large → small" on a 2D field | clean: that phrase sits only on the 3D ladder; the 2D note says energy runs to larger scales (Kraichnan 1967) |
| 10 saddle marked as "where it breaks" | clean: the side-view saddle is unmarked black hairline |
| 11 "turbulence is the unsolved problem" | clean (not claimed). Note that the sheet never states the question itself either (see legibility) |

## Scores
- **truth 9**: every drawn family is an exact solution, measured and not asserted: Burgers streamlines at Re = 100 (µm residual), Lamb–Oseen rings at exactly equal Δψ with the speed band at 1.11 r_c, meridional r²|z| = C at equal Stokes-ψ steps, an exact λ = 2 ladder on an exact similarity orbit whose fixed point is the red ring's centre, and a correct, dated, conditional status.
- **fidelity 9**: each channel carries its quantity to measurement precision, and the 0.8 mm floor holds exactly. Two blemishes. (a) A 6 mm type-layer dash at (276–282, 366.6) under "EVERY SCALE" encodes nothing. (b) Encoding §4 claims ink density carries ω₀ × 4 per rung, but measured perpendicular spacing at 3δ is ≈2.4 (hero), then 1.21 mm in every rung 1–4: ×2 once, then flat. Nothing on the sheet claims otherwise, so this is not scored as a lie.
- **legibility 8**: rings against spiral reads at 3 m, and the ladder plus the empty red ring read as "where it would finish". Weak points for a stranger: the sheet never says what the question is (infinite velocity at a point in finite time); "BLOW-UP" appears only in the stamp and is undefined; and "BY 4/3 T0" renders as "BY 4/3 TO".
- **VERDICT: PASS**

## Mandates
None binding (PASS). Advisories for r02, not mandates:
1. State the question once in words, e.g. in the statement line or the ladder caption: "can a smooth 3D flow reach infinite speed at a point in finite time?" At present the §5 correction is only implied.
2. The "4/3 T0" caption (≈ x 140–250, y 49) renders the subscript as the letter O ("TO"). Write "4/3 T₀" as "4/3 OF T0" or with a real subscript.
3. Remove the 6 mm dash at (276–282, 366.6) under "SAME EQUATIONS / EVERY SCALE". Also reconcile the encoding with what was built: orbit factor 1.225 not 1.10, hero eye 1.39 mm not ≈2.9 mm, ladder density ×2 then flat, not ×4 per rung.

## Follow-up on open mandates
None: r01, and there is no LEDGER.md.
