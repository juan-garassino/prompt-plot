# Science critique — millennium-hodge r03 · mathematics (algebraic geometry) · 2026-09-29
render: gallery/studio/millennium_hodge/current/pp_millennium_hodge_iterate_v4.png (+ `_v4.gcode`; physical-width preview `rounds/r03/phys_preview_v4.png`; Leo A5 `_v5_a5.gcode`)
pass: 2. I did not open piece.py, NOTES.md, audit.py or survey.py. Every number below comes from my own gcode parser and an independent exact model: an orthographic camera with a right-handed basis, and ray–quadric visibility against the stated slab −2 ≤ z ≤ 0.8. The sheet transform was **fitted, not assumed**. It converges to el 48.000°, roll −14.000°, k 62.000 mm/unit, origin (184.00, 210.00) and hinge 177.00° in my az-180 convention, which is HANDOFF's az 0 / α0 357° rotated by 180°. It reproduces all 346 non-X string strokes (the 0-offset X passes included) to a median of 0.0035 mm. p lands at (169.72, 166.14), which is HANDOFF's value exactly.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | rulings on x²+y²−z²=1 | < 1e-14 | 1.8e-15 | 172 gold + 174 blue weave strokes. Each is one 2-point G1 and lies on an exact projected ruling B(β0+2πj/96) / A(α0+2πi/96): median 0.0035 mm off, max 0.02 mm. X passes sit at offsets 0.15/0.30/0.45 mm (7 passes, a 0.9 mm band). | OK |
| 2 | twist, rim radius, 3D length (H=2) | 126.87°, 2.2361, 5.657 | 126.870°, 2.2361, 5.6569 | The slab is now **−2 ≤ z ≤ 0.8**, and the key says so. For this slab the twist is 102.09°, the rim radii are 2.2361 / 1.2806, and the length is 3.960. X ends back-project to z = −2.000: blue (30.66, 120.27), gold (268.63, 51.00). Opposite ends are at z = +0.800: blue (225.34, 184.49), gold (130.15, 212.20). | OK (asymmetric slab stated; §4 allows any stated clip) |
| 3 | tangent plane x=1 → y=±z (the X) | A(α0) ∪ B(α0) | confirmed | The X is blue idx 0 × gold idx 0, crossing at (169.72, 166.14) = proj(p). The waist circle passes 0.1 mm from p. | OK |
| 4 | pencil types; far vertex z = −tan2ψ | ellipse/parabola@45/hyperbola/X@90 | 15° −0.5774, 31.72° −2.0000, 60° +1.7321, 75° +0.5774 | All 15 non-rebus green strokes back-project to ψ = 0, 15, 31.72, 45, 60 and 75. Median deviation from the exact projected conic is 0.002–0.005 mm; 12/15 strokes stay ≤ 0.01 mm, and 3 strokes reach ≤ 0.36 mm at my sampling gaps near turning points. The 60° upper branch lies wholly above z = 0.8 and is correctly absent. The 75° upper branch runs z 0.577 → 0.800 and appears as one arc ending on the rim. | OK |
| 5 | last whole ellipse | tanψ = 1/φ = 0.6180, 31.72° | 0.618034, 31.7175° | Graze vertex z = −2.0000 projects to **(195.86, 227.57)** and is **visible** through the throat, inside the drawn arc (166.6, 233.6)→(204.9, 224.7). A bottom-rim gold string end is 2.15 mm away at (197.31, 229.16). The kiss is on the sheet (r02: hidden). | OK |
| 6 | (p,q) class: degree p+q, \|p−q\| exits | 1/2/3/5/4/7 | on quadric ≤ 4.4e-16; max plane hits 1, 2, 3, 5, 4, 7 | not drawn (abstract, no row) | n/a |
| 7 | fraction inside \|z\|≤2 | 0.7048 | 0.704833 | not drawn | n/a |
| 8 | (2,3)² = 12, genus 2 | 12, 2 | 12, 2 | not drawn | n/a |
| 9 | b₂ = 2 / 7; h^{2,0}=0 | 2, 7 | χ = 4, 9 | The key says "HERE h^{2,0}=0: EVERY CLASS IS A HODGE CLASS, AND ALL ARE BUILT FROM [A] AND [B]". | OK |
| 10 | Clebsch: 27 lines, 10 each, 135 pairs, 10 Eckardt + 105 | as stated | 27 / {10} / 135 / 115 = 10 triple + 105 double; residual 1.2e-14 | not drawn | n/a |
| 11 | waist spacing 2πk/(N√2) | 1.39 @ k30 | 1.388 @ k30 → **2.869 @ k62** | Same-colour near-parallel (\|cos\|>0.93) pairs under 0.8 mm, outside the intended X/rebus bands: **0.0 mm** gold and 0.0 mm blue. There are 0 string fragments under 8 mm on A3 and 0 on A5 (min 8.6 mm). | OK |
| — | eye (see-through, exact ray test) | ≥ 45 mm tall, zero ink | — | x 123.8–244.2, y 182.0–234.5: **120.4 × 52.5 mm**, 4315 mm². Ink more than 0.5 mm deep inside it: 0.00 mm in all four colours. | OK |
| — | hidden-line truth | no ink on hidden parts | — | Strings: 0.94 mm gold and 0.46 mm blue hidden or outside the slab, summed over the whole sheet; the worst single stroke is 0.53 mm, all endpoint rounding. Green: ≤ 0.4 mm per stroke, at occlusion edges. | OK |
| — | string coverage | LOD halving, string yields to green | — | Visible drawn: gold 14147/16306 mm (86.8 %), blue 13989/16155 mm (86.6 %). The undrawn part breaks down as: floor-LOD (a same-colour neighbour < 1.2 mm) 1680 / 1694 mm; yielding to green 416 / 396 mm; marginal 84 / 101 mm (neighbour 1.2–5 mm, right frame edge and the upper-back rim). There are no punched holes. | OK |
| — | green endpoints | rim, occlusion, frame or stagger only | — | 30 of 30 ends are classified. Six are rim ends, at z = −2.000 or +0.800. Three are frame ends at x = 282. The rest are true occlusion edges, or stagger stops near p. None ends mid-surface, and none is closed back. | OK |
| — | minutes (C2) | plot plate --dry-run | — | I re-ran it: gold 38, blue 38, green 5, text 40, ETA ~126 min, bounds OK. This matches HANDOFF. | OK |

## Lies list
| item | status |
|---|---|
| 1 invented surface | clean. Every string is an exact ruling, and every green point lies on its stated conic. |
| 2 colour = cohomology | clean. Blue = [A] and gold = [B], both cycles. Green = the curves of class [A]+[B]. No ink stands for H^{p,q}. |
| 3 bent strings | clean. All 360 gold/blue strokes are single 2-point G1 segments, including the rebus slashes. |
| 4 reference row / C₀…C₄ / Σaᵢ Cᵢ | clean (no row). |
| 5 non-algebraic winding | clean. Only the ψ-pencil is drawn. |
| 6 closing clipped curves | clean. The open members end at z = −2 / +0.8 or at x = 282. The 60° upper branch is correctly absent above the top rim. |
| 7 picture proves the conjecture | clean. "EVERYTHING DRAWN HERE IS A THEOREM (LEFSCHETZ 1924). THE OPEN CASES BEGIN IN REAL DIMENSION 8 AND CANNOT BE DRAWN." |
| 8 ℤ / Kähler | clean. "RATIONAL HODGE CLASS", "RATIONAL COMBINATION", "PROJECTIVE". |
| 9 positive-only gluing / "assembled from shapes" | clean. The rebus now reads `[○] = [╱] + [╲]` with class brackets, and the headline says "IN COHOMOLOGY". |
| 10 crossing counts | clean. There are no ticks, no numbering and no dot at p. |

## Scores
truth 9 · fidelity 9 · legibility 8 · **VERDICT: PASS**

- **Truth.** The geometry is exact everywhere I measured it. The two caption defects from r02 are fixed: the rebus is a class equation, and green is called curves, not planes. The asymmetric slab is honest and stated. It is not the dossier's symmetric |z| ≤ H, so check 2 no longer holds as written (102.09° / 1.2806 here). That is a dossier-scope note, not a lie.
- **Fidelity.** The string, X, eye and green channels are all quantitative and clean. Visible green is undrawn only in the stagger window around p, and those stops are strictly monotone in ψ. They also sit where the exact member-to-member separation reaches the 0.8 mm floor: circle and 15° meet it at about 24 mm, and 45° and 60° at about 15 mm. The X is a 7-pass band, heavier than the encoding's 3-pass band, and HANDOFF declares it.
- **Legibility.** Three things now land: the X is unbroken on both arms from rim to rim, the circle runs through p, and the 31.72° kiss is visible at the eye's upper edge. The Hodge bridge sentence is present. One weak point remains. The three ellipses stop 25–32 mm short of p, so at the pinch only the circle and the 60°/75° hyperbolas visibly reach the X. The eye still reads the fan as converging, and "circle to X" lands.

## Mandates
None binding (PASS). These are advisory, for the lead and the art critic:
1. The X crossing angle on the sheet is **67.59°** (blue +18.26°, gold −49.34°). Art mandate A1 asks for 70–110°. It is true geometry at this view, so this is art's call, not a truth defect.
2. The [A]/[B] tags sit at the lower (z = −2) ends: [A] near (24, 118) and [B] near (273, 48). Encoding §4 says upper rim ends. They are harmless, since each tag sits beside its own string.
3. If a later round changes the slab again, keep the 31.72° graze vertex visible. The bottom rim must stay at z = −2, because the kiss is exactly tan 2ψ = 2 against that rim.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 green never cut by strings; monotone stagger | **FIXED** | Visible-but-undrawn green outside the p stagger window is **0 mm** for every member (r02: 45 + 11 + 18 mm). Drawn/visible: ψ0 333.6/333.6 mm, ψ15 378.0/440.8, ψ31.72 362.8/419.2, ψ45 183.7/233.4, ψ60 240.5/263.8, ψ75 324.9/341.2; each deficit is the single window around p. Stop distances from p (both arms): **15° 31.8/31.6 · 31.72° 28.5/28.6 · 45° 25.1/25.4 · 60° 12.0/12.1 · 75° 8.5/8.6 mm**, strictly decreasing (r02: 45° out of order). Strings yield to green (416/396 mm). |
| S2 honest words | **FIXED** | (a) The rebus reads `[○]=[╱]+[╲]` in black brackets, and its slashes run parallel to the X: blue 18.26°, gold 130.66° ≡ −49.34°, both to 0.01°. (b) The key reads "GREEN: THE CURVES CUT BY PLANES TURNING ABOUT THE TANGENT LINE AT THE CROSSING. EACH ONE, CIRCLE TO X, IS [A]+[B]." (c) It also reads "HERE h^{2,0}=0: EVERY CLASS IS A HODGE CLASS, AND ALL ARE BUILT FROM [A] AND [B]." RATIONAL, PROJECTIVE, THEOREM (LEFSCHETZ 1924) and REAL DIMENSION 8 are all present. |
| C2 plate-job minutes | **FIXED** | The dry-run gives 38/38/5/40 min and an ETA of ~126 min with feed ≤ 500, matching HANDOFF. |
| A1 (art; measured for the record) | PARTIAL | Both X strings are unbroken, one stroke per pass from rim to rim: gold 212.5 mm, blue 205.0 mm, ratio 0.965. The band is 0.9 mm, heavier than the 0.5 green. The crossing is 67.59°, below the 70° floor. |
| A2 (art; measured) | FIXED | The waist circle is 97.7 % drawn (333.6/341.4 mm), with gaps only at the two eye tips: about 4.0 mm at (243.0, 191.2)→(244.2, 195.0) and about 3.7 mm at (123.8, 225.0)→(123.2, 221.4). The 31.72° graze is visible at (195.86, 227.57). |
| A3 (art; measured) | FIXED | 0 gold/blue fragments under 8 mm on A3. |
| regressions | none | Everything that held in r02 still holds: rulings, conics, hidden-line truth, 0 ink in the eye (now 52.5 mm tall vs 50.0), and 0 same-colour floor breaks. |
