# Science critique — millennium-bsd r03 · mathematics (arithmetic geometry, elliptic curves) · 2026-09-29
render: gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.png (phys `_v7_phys.png`; gcode `gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.gcode`, thesis [A], A3 portrait)

## Method

I recomputed every §7 number from scratch in `.venv/bin/python` with my own code (numpy + fractions, no scipy). The inputs were:

- an exact Fraction group law to ±220P
- a_p by Legendre counting
- Λ(s) from the smoothed series, with Γ(a,x) by quadrature
- ε fixed by the Dirichlet series at s = 3
- θ and Ω₀ by Gauss–Legendre and cross-checked by AGM

I parsed the gcode per `; color=N`: 62 / 41 / 1510 / 5 / 7 strokes, with 0 G1-while-up and 0 G0-while-down. Every vertex was mapped back with X = 30 + (x − e₃)·52 and Y = 200 + (y + ½)·52. I matched each chord-layer stroke to its exact line through P, kP and −(k+1)P, including the heavy hairpins and the 2 mm stubs. Then I measured every in-field orbit point ±1…±61 against the ink. The type was re-rasterised from layer 2 at 12–14 px/mm and read line by line.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | P..8P on E; (1,1),(1,−2) not | yes / no | yes / no (exact) | 60/60 chord families sit on their exact line: angle error ≤ 0.04° (stubs ≤ 0.23°), line-to-P offset ≤ 0.06 mm. 87 of the 96 in-field ±nP carry a mark at ≤ 0.01 mm. **0** ray ends land on E away from a rational point | OK |
| 2 | roots; mirror y = −½; egg y; gap | −1.10716, 0.26959, 0.83757; [−1.29681, 0.29681] | −1.10715987, 0.26959444, 0.83756544; [−1.296806, 0.296806] | Egg spans X ≤ 101.59 and Y 158.57–241.43 (mid 200.00). Branch vertex at X 131.13. **0** E/L/gold/axis vertices in X ∈ (101.6, 131.1). E vertices ≤ 0.01 mm off the true curve (≤ 0.09 mm at the notch cut ends) | OK |
| 3 | odd n on the egg, even n on the branch | yes | yes, n = ±1..±200 | every marked end obeys parity (oval 52 + P, branch 34/34) | OK |
| 4 | chord P, nP → −(n+1)P; tangent y = −x → (1,−1) | yes | exact collinearity for k = 2..39 | Tangent (chord 1) runs from r = 7.00 to −2P (139.57, 174.00) with 0.00° error. Chord 2 is y = 0, (35.57 → 139.57, 226). No outer end passes its R. **One stub overshoots its egg point** (M3) | OK / minor breach |
| 5 | ĥ = 0.051111408; den x(100P) 221 digits | 0.0511114 / 221 | h(x(2¹⁰P))/4¹⁰ = 0.0511114082; 221; x(200P) 887; ĥ/ln 10 = 0.022197 | Caption: `X(NP) EXACTLY. ITS DIGITS GROW AS N² × 0.0222 (= HEIGHT 0.0511 / LN 10).` Line 30 has 20 + 20 digits and 0.0222 × 900 = 19.98. The ziggurat is **30/30 exact**, character by character | OK |
| 6 | θ = 0.378917283; u(4P) 0.757835; u(6P) 0.136752; CF | as stated | 0.3789172826; 0.7578346; 0.1367518; [0;2,1,1,1,3,2,1,2,1] | not drawn (allowed) | OK |
| 7 | Ω₀, Ω_E | 2.993458646, 5.986917292 | 2.9934586462 (AGM) = 2.99345864625 (quadrature); 5.9869172925 | caption `5.98692` | OK |
| 8 | L′(1) = 0.3059997738 = Ω_E·Reg; 17.014° | as stated | 0.3059997738340524; Ω_E·Reg = 0.30599977383; 17.0141° | The two gold passes sit at ±0.35 mm (perpendicular) about the true L. They cross Y = 200 at X 205.774 / 203.395, mean s = 0.9997. Pass angles are 17.017° / 16.993°. Gold spans s 0.8485–1.1523, and black L stops at s 0.8425 / 1.1573 | OK |
| 9 | L(0) = 0; min −0.08924 at 0.478; L(0.5) −0.089049; L(1.5) 0.183965; L(2) 0.381575; Λ(1.5) = −Λ(0.5) = 0.155297; L′(0) −0.35762 | as stated | −0.0892422 at 0.478; −0.0890486; 0.1839655; 0.3815754; ±0.1552969; −0.357620 (Richardson, h = 10⁻⁴) | L runs (152.60, 200.00) → (256.60, 219.84). Max vertical error on both black strokes is **0.005 mm**. The s-axis runs X 152.6–256.6 at Y 200 and is not continued left | OK |
| 10 | a_p, N_p, EDSAC | −2,−3,−2,−1,−5,−2; 5,7,8,9,17,16; 74.746, 8.115, C 8.2314 | identical; a₃₇ = −1; 74.74598; 8.11544; 8.23143 | not drawn | OK |
| 11 | rank ladder | 0.253842; 0.759317, +0.2100; 1.73185, −0.4921 | 0.2538419 (a_p −2,−1,1,−2,1); 0.7593165, +0.20995; 1.73184 (deg-8 fit), −0.49206 | 11a1 `L(1) = 0.2538` in the right column: correct | OK |

**Dossier:** no errors. **Handoff discrepancy:** it says 53P sits "0.47–0.72 mm off rays 4/20/21". My measurement is 0.211 mm from the centreline of chord 4's second (offset) pass, and 0.464 mm from its first pass. At a 0.3 nib, 53P is inside the ink of −5P's heavy end.

## Lies list
| item | status |
|---|---|
| 1 points not on E | clean: every ray end is an exact orbit point or a crop, and 0 false contacts remain (r02 had 3) |
| 2 one connected curve | clean: 0 curve/axis/label ink in the 29.5 mm gap. Near P the egg yields to the tangent for t ∈ [7, ≈11] mm, where the tangent is 0.3–1.0 mm off true E. It then continues as fine stubs of chords 30/27 that lie ≤ 0.13 mm off E. This is sanctioned by S2(c), and the egg still reads closed |
| 3 symmetry about y = 0 | clean: egg mid Y 200.00; no axes on the curve side |
| 4 L large at 0 / positive on (0,1) | clean: L(0) sits on the axis and dips 4.64 mm |
| 5 V-bounce | clean: smooth transversal crossing at 17.0° |
| 6 decorative flow / gold | clean: gold is 6 rings at r = 1..6 mm on P plus the 2-pass crossing band, nothing else |
| 7 leftmost point (−1,0) | clean: no point labels |
| 8 closed polygon / even beads | clean |
| 9 rank = number of points | clean (`RANK 1`, "ONE POINT MAKES INFINITELY MANY") |
| 10 L(E,1) = Σaₙ/n | clean (absent) |
| encoding §9.6 "no line past the egg point" | **VIOLATED (minor):** chord 8's stub at −9P, (63.59, 241.76)–(67.18, 239.40), runs 3.3 mm past the egg into the silent x < 0 exterior (M3) |

## Scores
truth **8** · fidelity **8** · legibility **7** · VERDICT: **FAIL**

- **Truth.** Every number and every sentence on the sheet is now correct. That covers the ĥ/ln 10 caption, the causal statement (true: Kolyvagin gives L(1) ≠ 0 ⇒ rank 0), the 11a1 foil, the honest status, and all 30 x(nP). The geometry is exact to ≤ 0.01 mm. The one breach is the 3.3 mm stub overshoot.
- **Fidelity.** No false contacts and no fake void remain: within 30 mm of P, 12/18 non-P oval points are marked (r02: 2/18). But 7 in-field oval rational points are still silently unmarked (53/62; the lead asked for ≥ 60). They are exactly in the densest measure, and nothing on the sheet says so.
- **Legibility.** A scientist gets it all. A stranger gets the words, but not the picture:
  - nothing on the sheet names the gold disc as P;
  - nothing says a ray end is a rational point;
  - "NP" is used but never defined.

  So the visual half of the misconception fix (points pile up on the curve) does not land.

## Mandates
1. **The picture's rule is never stated on the sheet, so a stranger cannot read the fan as rational points.** This is the gold disc (87.6, 226), the ray ends, and the bottom-left caption Y ≈ 20–28.
   - *Measured:*
     - **0** labels name the disc as P;
     - **0** sentences say that a line through P meets the curve again at rational points, or that each ray end is one;
     - `NP` (caption) and `HEIGHT OF P` (right column) are used undefined;
     - the L-curve carries only `S = 1`, with no `L(E,S)`.

     The notes block was correctly cut (A2), but nothing replaced its one needed sentence.
   - *Expected:* one sentence of ≤ 2 lines, e.g. `P = (0,0) IS THE GOLD POINT. EVERY LINE THROUGH P MEETS THE CURVE AT TWO MORE RATIONAL POINTS; EACH RAY END IS ONE OF THE INFINITELY MANY nP.` Put it in the caption under the ziggurat (Y < 28) or at the top of the right column (Y ≈ 110–120; the lower arm is ≥ 14.9 mm away there), not in the left-hand y 250–375 zone. Optionally add `L(E,S)` at 1.6 mm near (256.6, 219.8).

2. **Seven oval rational points of drawn chords are still silently unmarked.** Measured **53/62** (+34/34 on the branch) against the ≥ 60/62 in S2(a):
   - **−57P, 59P** lie at r = 2.55 / 2.47 mm, under the 6 mm gold disc;
   - **−15P, 43P** at (91.99, 221.16) / (93.38, 219.44) lie 0.537 / 0.533 mm off the tangent, where the egg yields;
   - **−37P, 37P, 53P** at the right tip (101.55, 198.79) / (101.55, 201.21) / (100.97, 205.07) lie 0.72 / 0.59 / 0.21 mm from rays 21, 20 and 4, and each has an own-chord inner end 3.8 / 10.4 / 32 mm farther out.

   All 7 are below the 0.8 mm floor or under the disc, so marking them is probably infeasible at this scale.
   - *Expected:* either reach ≥ 60/62, or state the merge in type (e.g. `7 POINTS NEAR P AND AT THE OVAL'S RIGHT TIP LIE CLOSER THAN THE PEN CAN SEPARATE`). Today the omission sits exactly where the invariant measure is highest (right tip 1/|∇F| = 1.279), which is the one place the plate claims points pile up.

3. **Chord 8's stub runs past its egg point into the chord-free half-plane.** Upper-left egg, stroke (63.59, 241.76) → (67.18, 239.40), layer 1.
   - *Measured:* −9P is at t = −25.40 on the chord. The stub spans t ∈ [−28.70, −24.40], so **3.30 mm lies outside the egg** (end 1.02 mm off E in the x < 0 exterior) and 1.0 mm inside. The other 11 stubs are 2.0 mm, centred ±1.0 mm (the chord-52 stub is 2.7 mm).
   - *Expected:* ≤ 1.0 mm past the egg point, like the other stubs, t ∈ [−26.4, −24.4]. This restores "no chord ink left of P outside the egg" (encoding §7/§9.6).

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 ĥ caption off by ln 10 | **FIXED** | The caption reads `N² × 0.0222 (= HEIGHT 0.0511 / LN 10)`; recomputed ĥ/ln 10 = 0.022197. The bridge still says `0.05111` = HEIGHT OF P (natural log, as in L′ = Ω·ĥ) |
| S2 hub loses what belongs to P | **PARTIAL** | (a) oval marks are **53/62** (r02 42/62), with 12/18 near-P oval points now marked; still below ≥ 60 (M2). (b) **FIXED**: 0 ray inner ends lie < 1.5 mm from E off their own point. Chord 11 now starts exactly at 11P (t 19.19). Chord 27's ray end is at 1.509 mm, with its 27P carried by a stub. The r02 contacts at (94.81, 218.41), (100.52, 208.47) and (98.82, 212.12) are gone. (c) **FIXED**: the tangent starts at r = 7.00 like chords 2/3/5/6/7. The egg yields: it is clipped at 0.77 mm separation (t −11.2) upper-left, and carried by fine stubs ≤ 0.13 mm off E for t 11–15 lower-right. The nearest non-own points to the tangent, −15P and 43P, are 0.54 / 0.53 mm (r01: 0.30 / 0.36) |
| S3 zero because infinite, foil, status | **FIXED** | (a) the statement reads `RANK E(Q) = ORD(S=1) L(E,S): ONE POINT MAKES INFINITELY MANY, SO L VANISHES AT S = 1.` (true for all E/Q). (b) `A CURVE WITH FINITELY MANY POINTS (11A1) HAS L(1) = 0.2538, NOT ZERO.` (recomputed 0.2538419). (c) the status line is verbatim. (d) the right column spans X 228.72–282.00, and the nearest line ink is **14.9 mm** away |
| A1 gold crossing (science-relevant part) | FIXED (science side) | 2 passes at ±0.35 mm with a centre gap of 0.70 = nib, so no overlap. s 0.8485–1.1523 at 17.0°. The rest of L is on layer 1 (0.3) |
| A2 notes cut / series caption | observed FIXED | 0 text strokes in x < 148, y 250–375. `MILLENNIUM PRIZE PROBLEMS 7 / 7` / `CLAY MATHEMATICS INSTITUTE, 2000` sits top-right with right edge 282.0. Rays crop at Y 368.4 (art to judge the shared line) |
| A3 craft | not re-measured | art's call |

**Regressions:** none. E, the gap, the mirror, L (≤ 0.005 mm), the 17.0° crossing, gold scarcity, parity, the 30/30 digit strings and 60/60 chord exactness all hold from r02.
