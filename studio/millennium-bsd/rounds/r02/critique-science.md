# Science critique — millennium-bsd r02 · mathematics (arithmetic geometry, elliptic curves) · 2026-09-29
render: gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.png (phys preview `_phys.png`; gcode gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.gcode, thesis [A], A3 portrait)

## Method

I recomputed every §7 number from scratch in `.venv/bin/python` with my own code (numpy + fractions only; no scipy or mpmath available). The inputs were:

- an exact Fraction group law to 200P
- a_p from point counts via the discriminant square-table
- Λ(s) from the smoothed series, with Γ(a,x) by Simpson in log-t
- ε fixed by the Dirichlet series at s = 3
- θ by Gauss–Legendre on ∫dt/√f

I parsed the gcode per `; color=N` layer: 55 / 36 / 1499 / 4 / 7 strokes, with 0 G1-while-up and 0 G0-while-down. I mapped every vertex back to the plane with X = 30 + (x − e₃)·52, Y = 200 + (y + ½)·52. Each of the 60 chords was matched to its exact line through P, kP and −(k+1)P. The digit block was re-rendered from the text-layer strokes at 20 px/mm and read line by line.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | P..8P on E; (1,1),(1,−2) not | yes / no | yes / no (exact) | All 60 chords match their exact line: angle error ≤ 0.03°, and every single-pass centreline passes ≤ 0.02 mm from P's centre (87.572, 226.000). 65 ray ends sit ≤ 0.4 mm from an exact ±nP and 10 more points are crossed by a ray (≤ 0.004 mm). **0** outer ends land anywhere other than an orbit point or the crop. The digit block's x(nP), n = 1..30, is **30/30 exact**, character for character (e.g. line 30 `79799551268268089761/62586636021357187216`) | OK |
| 2 | roots; mirror y = −½; egg y ∈ [−1.29681, 0.29681]; gap | −1.10716, 0.26959, 0.83757 | −1.10715987, 0.26959444, 0.83756544; egg y [−1.296806, 0.296806] | The egg spans X 30.00–101.59 and Y 158.57–241.43 (midpoint 200.00). The branch vertex is at X 131.13. There are **0** E/L/gold vertices in X ∈ (101.59, 131.13). E vertices lie ≤ 0.006 mm and segment midpoints ≤ 0.014 mm off the true curve | OK |
| 3 | odd n on egg, even n on branch | yes | yes, n = 1..200 | parity holds for every drawn ray end | OK |
| 4 | chord P, nP → −(n+1)P; tangent y = −x → (1,−1) | yes | yes for n = 1..7, exact collinearity | Chord 1 is the tangent y = −x (angle error 0.00°) ending at −2P (139.57, 174.00). Chord 2 is y = 0, running (35.57, 226) → (139.57, 226). No outer end goes past its R | OK |
| 5 | ĥ = 0.051111408; den x(100P) 221 digits | 0.0511114 / 221 | h(x(200P))/200² = 0.0511106 (→ LMFDB); 221; x(200P) 887 | Caption: `DIGITS GROW AS N² × 0.0511`. **Wrong by ln 10**: see mandate 1 | **VIOLATED on sheet** |
| 6 | θ = 0.378917283; u(4P) 0.757835; u(6P) 0.136752; CF | as stated | 0.3789172826; 0.7578346; 0.1367518; [0;2,1,1,1,3,2,1,2,1] | not drawn (allowed) | OK |
| 7 | Ω₀, Ω_E | 2.993458646, 5.986917292 | 2.9934586462, 5.9869172925 | caption `5.98692` | OK |
| 8 | L′(1) = 0.3059997738 = Ω_E·Reg; 17.014° | as stated | 0.3059996 (central diff, h = 10⁻³); Ω_E·Reg = 0.3059997738; 17.0141° | The gold crossing is 2 passes straddling L. They cross Y = 200 at X 204.9 / 204.3 (mean 204.6 = s 1.000). Local fitted angle over s ∈ [0.97, 1.03] is **17.00° / 17.11°** (mean 17.06°). Gold spans s 0.849–1.151, and black L stops at s 0.856 / 1.145 | OK |
| 9 | L(0)=0; min −0.08924 @ 0.478; L(.5) −0.089049; L(1.5) 0.183965; L(2) 0.381575; Λ(1.5) = −Λ(.5) = 0.155297; L′(0) −0.35762 | as stated | −0.0892422 @ 0.478; −0.0890486; 0.1839655; 0.3815754; ±0.1552969; −0.35735 (FD) vs −(37/4π²)L(2) = −0.35762 | L starts at (152.60, 200.00) and ends at (256.60, 219.84). Max vertical error vs my L over both black strokes is **0.005 mm**. The s-axis runs X 152.6–256.6 at Y 200.00 (s ∈ [0,2]) and is not continued left | OK |
| 10 | a_p, N_p, EDSAC | −2,−3,−2,−1,−5,−2; 5,7,8,9,17,16; 74.746, 8.115, C 8.2314 | identical; a₃₇ = −1; 74.74598; 8.11544; 8.23143 | not drawn (allowed) | OK |
| 11 | rank ladder | 0.253842; 0.759317, +0.2100; 1.73185, −0.4921 | 0.2538419; 0.75924 (FD O(h²)); +0.20995; 1.7374 (FD); −0.49206 | not drawn (allowed) | OK |

**Dossier:** no errors found.

**Encoding discrepancies (for the lead):**
- §4 says the ray ends mark "±1…±61 (96 inside the field)". Two of those 96, −P and 61P, lie on no drawn chord (k ≤ 60), so they can never be marked. The sheet marks **76** (see mandate 2).
- §4 and §11.1 give hub radii that do not match the sheet:

  | chord | encoding (mm) | measured (mm) |
  |---|---|---|
  | 1 (tangent) | 7 | 10.5 |
  | 10 | 10.2 | 13.4 |
  | 11 | 16.6 | 21.8 |
  | 56 | 46.0 | 60.4 |
  | 59 | 47.6 | 62.5 |

  Chord 4 begins at its own point −5P, 23.4 mm from the hub, which is correct because P does not lie between its two points.

## Lies list
| item | status |
|---|---|
| 1 points not on E | clean for positions: every ray end is an exact orbit point or a crop. **Visual near-violation:** 3 inner ray ends touch the 0.5 egg line at non-orbit spots (mandate 2) |
| 2 one connected curve | clean: 0 curve, axis or label ink in the 29.5 mm gap |
| 3 symmetry about y = 0 | clean: egg midpoint Y 200.00; no x or y axes; mirror drawn only as the s-axis right of X 152.6 |
| 4 L large at 0 / positive on (0,1) | clean: L(0) sits on the axis and dips 4.64 mm below it |
| 5 V-bounce | clean: transversal crossing at 17.06°, smooth |
| 6 decorative flow / gold | clean: gold is exactly 6 concentric rings at r = 1..6 mm centred on P, plus the 2-pass crossing band. Nothing else |
| 7 leftmost point (−1,0) | clean: no labels on the curve; the tip is unmarked |
| 8 closed polygon / even beads | clean: exact irrational orbit, no marks placed by eye |
| 9 rank = number of points | clean (`RANK 1`, "ONE POINT MAKES INFINITELY MANY") |
| 10 L(E,1) = Σaₙ/n | clean (absent) |

## Scores
truth **7** · fidelity **7** · legibility **7** · VERDICT: **FAIL**

The geometry is flawless: 60/60 chords exact, E and L within 0.014 mm, the crossing at 17.06°, and 30/30 digit strings exact. But three things fail:

- **Truth:** the one quantitative caption about ĥ is wrong by a factor of 2.30.
- **Fidelity:** the hub-LOD rule silently erases most of the oval's rational points near P. It also inverts the claimed "orbit's own" density gradient at the egg's right tip, and leaves three ray ends touching the curve where no rational point is.
- **Legibility:** "zero means infinity" is juxtaposed with the zero but never stated as a cause, and there is no rank-0 foil.

## Mandates
1. **The ĥ caption is off by ln 10.** Bottom-left, under ziggurat line 30, Y ≈ 27–33: `X(NP) EXACTLY. ITS DIGITS GROW AS N² × 0.0511: THE HEIGHT OF P.`
   - *Measured:* at n = 30 the rule predicts 900 × 0.0511 = **46.0 digits**, but the sheet's own line 30 has **20** digits in the numerator and 20 in the denominator. ĥ is a natural-log height: log max(|num|, den) ≈ ĥn² (45.8 at n = 30).
   - *Expected:* digits ≈ ĥn²/ln 10 = **0.0222·n²** (19.97 at n = 30; 221 at n = 100, dossier #5). Write either `DIGITS GROW AS N² × 0.0222 (= HEIGHT 0.0511 / LN 10)` or `LOG OF ITS SIZE GROWS AS N² × 0.0511, THE HEIGHT OF P`.

2. **The hub LOD erases the oval's points near P and fakes three contacts.** This is the egg arc within ~30 mm of the gold disc (87.6, 226) and the egg's right tip (101.6, 200).
   - *Measured, dropped points:* the in-field orbit points of drawn chords get a mark 76 times out of 96 (−P and 61P are unmarkable). The **18 dropped points are all on the oval**: −9, 11, −15, 17, −25, 27, −31, 33, −37, 37, −41, 43, −47, 49, −53, 53, −57, 59. The chord's r_k exceeds the point's distance from P, so its ray starts past the curve.
     - The oval shows 42/62 points and the branch 34/34.
     - **16 of the 18 oval points within 30 mm of P are blank.** That is a false void where the rule says points pile up.
     - At the egg's right tip, the highest-measure spot (1/|∇F| = 1.279), **4 of 6** points (±37, ±53) are blank.
     - 11P, 17P and 27P are listed in the ziggurat but have no mark on the curve.
   - *Measured, false contacts:* three inner ends sit 0.52–0.59 mm (centre to centre) from the 0.5 egg line, so on paper they touch it at points that are not rational:
     - the tangent (chord 1) at (94.81, 218.41), 1.76 mm from 43P. It also starts at 10.5 mm while chords 2, 3, 5, 6 and 7 start at 7.0 mm.
     - chord 11 at (100.52, 208.47), 2.6 mm from its own 11P.
     - chord 27 at (98.82, 212.12), 0.62 mm from −47P, which lies on chord 46, not 27.
   - *Expected:*
     - Every egg point of chords 1–60 is marked: ≥ 60 of 62 oval points, with only −P and 61P unmarked. One way is a short stub of the chord's own line (≥ 2 mm, straddling E) when the egg point lies inside r_k.
     - Every ray's inner end is either exactly at its own orbit point or ≥ 1.5 mm (centre) from E.
     - Otherwise, state the omission in type.

3. **The misconception is still not corrected, and the attribution still overreaches.** Right column, X 226–282, Y ≈ 20–110.
   - *Measured:* the headline is `ONE POINT MAKES INFINITELY MANY. ITS L-FUNCTION CROSSES ZERO ONCE.` It sets the two facts side by side but gives **0** causal link: no text says L(E,1) = 0 *because* the orbit is infinite. There is **0** rank-0 foil (11A1, L(1) = 0.25384). "Zero means nothing" is never named or countered.
   - *Measured, attribution:* the block still ends with `PROVED FOR THIS CURVE: GROSS-ZAGIER 1986, KOLYVAGIN 1988.` This is unchanged from r01 mandate 3. GZ + Kolyvagin give rank = order = 1 and Ш finite. The exact Ш = 1 formula was a later computation.
   - *Expected:* one line saying the zero at s = 1 is the fingerprint of infinitely many points, for example `L(E,1) = 0 BECAUSE P NEVER COMES BACK; A CURVE WITH FINITELY MANY (11A1) HAS L(1) = 0.2538`. Also change the status line to `RANK = ORDER PROVED (GROSS-ZAGIER 1986, KOLYVAGIN 1988); FULL FORMULA CHECKED BY COMPUTATION; OPEN IN GENERAL.`

## Follow-up on open mandates
No `LEDGER.md` exists for this slug, so there are no ledgered S* mandates. r02 is the sibling [A] thesis, not a revision of r01's [F] plate. The r01 mandates that carry over are tracked here for information only:

| id | status | evidence |
|---|---|---|
| r01-S1 misconception line | PARTIAL | "INFINITELY MANY" now appears (headline) and the root-number line explains the forced zero. There is still no causal "zero because infinite" and no rank-0 foil (mandate 3) |
| r01-S2 tangent does not reach P | NOT FIXED (analogue) | the [A] tangent starts 10.5 mm from P vs 7.0 mm for chords 2/3/5/6/7, and its loose end touches the egg 0.52 mm off, 1.76 mm from 43P (mandate 2) |
| r01-S3 proof attribution | NOT FIXED | identical `PROVED FOR THIS CURVE: GROSS-ZAGIER 1986, KOLYVAGIN 1988.` text |

No truth that held in r01 regressed: E, the gap, the mirror, L, the 17° crossing and gold scarcity all remain exact.
