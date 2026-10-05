# Science critique — millennium-bsd r01 · mathematics (arithmetic geometry, elliptic curves) · 2026-09-29
render: gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5_truewidth.png (gcode gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5.gcode, thesis [F], A3 portrait)

Method: every §7 number was recomputed from scratch in `.venv/bin/python` (numpy + fractions only, own code, no project data files): an exact Fraction group law to 200P; a_p by Legendre counting; Λ(s) by the smoothed series with Γ(a,x) by quadrature; ε chosen by the Dirichlet series at s = 3. The gcode was parsed per `; color=N` layer (45/52/1561/53/6 strokes) and mapped back to the plane through the encoding's map (X = 30 + (x − e₃)·52, Y = 200 + (y + ½)·52).

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | P..8P on E; (1,1),(1,−2) not | yes / no | yes / no (exact Fractions) | 47 circle centres match the exact ±nP (n ≤ 30) within 0.002 mm, and the max plane residual \|F\| is 2.4e-4. All 8 labels on the sheet are true points. 11P–14P in the continuation text are exact | OK |
| 2 | roots, mirror, egg y-range, gap | −1.10716, 0.26959, 0.83757; [−1.29681, 0.29681] | −1.10715987, 0.26959444, 0.83756544; [−1.296806, 0.296806] | the egg spans Y 158.57–241.43 (midpoint 200.00 = mirror), X 30.00–101.59. The branch vertex is at 131.13. There is **0** E ink in X ∈ (101.62, 131.08), so the gap is 29.5 mm. E vertices lie ≤ 0.007 mm off the true curve | OK |
| 3 | odd n on egg, even n on branch | yes | yes for n = 1..200 | 29 circles on the egg, 18 on the branch, parity consistent | OK |
| 4 | chord P,nP → −(n+1)P; tangent y = −x → (1,−1) | yes | yes (slope −1, x³ − x² = 0 ⇒ x = 1) | the chords are y = 0 (0.000°/180°), y = x (45.003°) and y = −x (−45.000°). Each extension passes ≤ 0.006 mm from P's centre, and each ends 0.78 mm short of its orbit-circle centre (the circle edge). Negation dashes sit at plane x = −1.00004 and +0.99996, spanning Y 175.1–224.9 and bisected by Y = 200 | OK |
| 5 | ĥ = 0.051111408; den x(100P) 221 digits | 0.0511114 / 221 | h(x(200P))/200² = 0.0511106 (→ LMFDB value); 221 digits; x(200P) 887 | caption `LOG H(X(NP)) ~ 0.0511 N²` and `0.05111` | OK |
| 6 | θ = 0.378917283, u(4P) 0.757835, u(6P) 0.136752, CF | as stated | 0.378916 (quadrature error 3e-6); u(4P) 0.757835; u(6P) 0.136752; CF [0;2,1,1,1,3,2,1,2,1] | not drawn on [F] (allowed) | OK |
| 7 | Ω₀, Ω_E | 2.993458646, 5.986917292 | 2.9934586462, 5.9869172925 (AGM) | caption `5.98692` = REAL PERIOD | OK |
| 8 | L′(1) = 0.3059997738 = Ω_E·Reg; 17.014° | as stated | 0.30599977 (central difference); Ω_E·Reg = 0.30599977383; atan = 17.0141° | gold crossing centre (204.6, 200.008); per-pass fitted angles **17.027° / 16.994°** (mean 17.01°) | OK |
| 9 | L(0)=0, min −0.08924 @ 0.478, L(.5) −0.089049, L(1.5) 0.183965, L(2) 0.381575, Λ(1.5) = −Λ(0.5) = 0.155297, L′(0) −0.35762 | as stated | −0.0892422 @ 0.478, −0.0890486, 0.1839655, 0.3815754, ±0.1552969, −0.3576205 | L starts (152.57, 200.00) and ends (256.57, 219.84) (pred. 219.84). The minimum is at (176.84, 195.36) (pred. s 0.478 → 177.46, 195.36). Max vertical error over 25 samples is 0.016 mm. The s-axis runs Y 200 over X 152.57–256.57 = s ∈ [0, 2] | OK |
| 10 | a_p, N_p, EDSAC product | −2,−3,−2,−1,−5,−2; 5,7,8,9,17,16; 74.746, 8.115, C 8.2314 | identical; 74.74598; 8.11544; 8.23143 | not drawn (allowed) | OK |
| 11 | rank ladder | 0.253842; 0.759317, +0.2100; 1.73185, −0.4921 | 0.2538419; 0.75930 (FD), +0.20995; 1.7332 (FD h = 0.01, O(h²)), −0.49206 | not drawn (allowed) | OK |

Dossier findings: none wrong. Encoding nit: §4/§11 say "48 open circles". 48 is the in-field orbit count *including* P, so 47 circles + 1 gold disc is correct, and the sheet's "(47)" is right.

## Lies list
| item | status |
|---|---|
| 1 points not on E | clean (47/47 circles and 8/8 labels exact; (1,1)/(1,−2) absent) |
| 2 one connected curve | clean (0 ink points / 0 segments in the gap band; 29.5 mm bare) |
| 3 symmetry about y = 0 | clean (egg midpoint Y 200.00 = y = −½; negations bisected at 200.0; no x/y axes) |
| 4 L large at 0 / positive on (0,1) | clean (L(0) on the axis; dip 4.64 mm below) |
| 5 V-bounce | clean (transversal, 17.01°, smooth; black L stops at s 0.855/1.145, gold spans 0.849–1.150) |
| 6 decorative flow | clean (gold = 5 concentric rings at P (r 0.25–4.0, centre error ≤ 0.001 mm) + crossing band; nothing else) |
| 7 leftmost point (−1,0) | clean (−3P label at (35.57, 226); the tip (30, 200) is unlabelled. The circle at X 30.04 is a genuine orbit point, x = −1.1064) |
| 8 closed polygon / even beads | clean (exact orbit; egg nearest-neighbour spacing 3.98–11.64 mm) |
| 9 rank = number of points | clean (`E(Q) = ZP`, "ONE GENERATOR") |
| 10 L(E,1) = Σaₙ/n | clean (absent) |

## Scores
truth **9** · fidelity **9** · legibility **7** · VERDICT: **FAIL**

Truth and fidelity are excellent. Every mark is exact to ≤ 0.02 mm and one 52 mm/unit scale carries x, y, s and L, so the 17.0° claim holds. Legibility fails on the plate's own thesis. §5 ("zero means infinity") is not on the sheet, and the hub reads broken for a stranger.

## Mandates
1. **The misconception correction is missing. Type, right column / left paragraph.**
   - *Measured:* there are 0 occurrences of INFINITE/INFINITELY/∞ in any type. The only orbit-count line is `OPEN CIRCLES: EVERY NP, N = -30 .. 30, ON THE SHEET (47)` (left block, Y ≈ 275). It frames E(Q) as a finite set of 47. Nothing says that L(E,1) = 0 *because* the orbit is infinite. Nothing gives the rank-0 foil (11a1 L(1) = 0.25384 ≠ 0).
   - *Expected:* one line in the right column (X 226–282, between the crossing text at Y ≈ 180 and the bridge) saying that L vanishes at s = 1 because P generates infinitely many points, and that a rank-0 curve has L(1) ≠ 0 (11A1: 0.2538). Recast "(47)" as "47 OF INFINITELY MANY".
2. **The tangent at P does not reach P. Chord y = −x, hub at (87.57, 226).**
   - *Measured:* the tangent is inked from (95.57, 218.00) to (138.79, 174.78). Its inner end is **11.3 mm** from P's centre, 7.3 mm outside the 4.0 mm gold disc, while y = 0 and y = x start at **4.8 mm**. The nearest circle to that loose end is the orbit point at (96.59, 214.87), 3.3 mm away, so the segment reads as a chord from that point, not the tangent at P, and the one-glance "every line passes through P" breaks. The gap is geometrically honest: circles at (91.99, 221.16) and (82.24, 230.83) lie only 0.30 and 0.36 mm off the tangent, and inking through them would fake collinearity. So do not simply extend it.
   - *Expected:* the tangent's belonging to P is made explicit on the sheet. Label it `TANGENT AT P` (1.8 mm, on the segment's outer side), and/or have the caption say the n = 1 line is the tangent. Keep the inner end clear of those two circles.
3. **The proof attribution overreaches. Right column, Y ≈ 99–108, under the full leading-term identity.**
   - *Measured:* `PROVED FOR THIS CURVE: GROSS-ZAGIER 1986, KOLYVAGIN 1988` sits directly under `L'(E,1) = 5.98692 × 0.05111 … (SHA = 1 …)`. GZ + Kolyvagin prove rank = ord = 1 and that Ш is finite for this curve. The exact Ш = 1 (the full formula) was verified later by computation.
   - *Expected:* `RANK = ORDER PROVED FOR THIS CURVE (GROSS-ZAGIER 1986, KOLYVAGIN 1988); FULL FORMULA VERIFIED BY COMPUTATION; OPEN IN GENERAL.`

## Follow-up on open mandates
n/a. This is pass 1 (r01), with no LEDGER.md for this slug.
