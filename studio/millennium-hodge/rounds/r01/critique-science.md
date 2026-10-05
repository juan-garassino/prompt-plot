# Science critique — millennium-hodge r01 · mathematics (algebraic geometry) · 2026-09-29
render: gallery/studio/millennium_hodge/trials/pp_millennium_hodge_faithful_v7.png (+ .gcode; physical preview rounds/r01/phys_preview_v7.png)

Method: parsed the v7 gcode by `; color=N` layer (gold 407 strokes / 14.29 m, blue 401 / 14.09 m,
green 24 / 1.36 m, text 935 / 3.35 m). I recovered the projection blind from the ink. A conic fit
to the green waist-circle stroke gave k = 33.87 mm, elevation 50.00° and roll −30.00°. A least-squares
fit of all 340 hero string segments to the projected 96+96 rulings (α_i = 235° + 3.75°·i) then gave
az −0.0001°, e 49.99999°, roll −29.99998°, k 33.874, centre (188.50, 259.00). Every measurement below
comes from that recovered model, with exact ray–quadric visibility.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | rulings on x²+y²−z²=1 | <1e-14 | 4.4e-15 | all 340 hero string segments lie on the projected 96+96 rulings: median 0.0033 mm, max 0.153 mm (= the ±0.15 mm X passes); blue = family A, gold = family B | OK |
| 2 | twist 2·atan H; rim r; 3D length | 126.87°, 2.2361, 5.657 | 126.8699°, 2.23607, 5.65685 | H = 2 confirmed. The fit only closes with |z| ≤ 2 rulings. A(α₀) is 77.7 mm projected, 68.8 visible (88%), 68.8 drawn. B(α₀) is 188.9 mm, 178.5 visible (95%), 178.2 drawn | OK |
| 3 | x = 1 cuts y = ±z → A(0) ∪ B(0) | yes | A(0,s) = (1,s,s), B(0,s) = (1,−s,s) | the heavy blue line is ruling A index 0 and the heavy gold line is B index 0. They cross at (171.6, 285.8), and p is predicted at (171.9, 285.8) | OK |
| 4 | pencil types; far vertex −tan 2ψ | as stated | 0°, 15°, 31.72° ellipse; 45° parabola; 60°, 75° hyperbola; far vertex z = −0.577 / −2.000 / +1.732 / +0.577 | 15 hero green strokes map onto the six ψ members with max deviation ≤ 0.074 mm and chord error ≤ 0.032 mm. The ψ = 60° and 75° far branches (strokes 22, 23) are real and open at the rims | OK |
| 5 | last whole ellipse tan ψ = 1/φ | 0.6180, 31.72° | 0.618034, 31.7175° | strokes 17 and 19 fit ψ = 31.72° to 0.006–0.017 mm. The far vertex is at z = −2.0000 | OK |
| 6 | α = qu, β = pu has class p[A]+q[B], degree p+q | yes | max real plane hits 1, 2, 3, 5, 4, 7 = p+q; points at ∞ = \|p−q\| | row cells: cell 3 is (1,2) = [A]+2[B], c₁ = 55.0°, dev 0.006 mm (runner-up (1,3) at 4.6 mm). Cell 4 is (2,3) = 2[A]+3[B], c₁ = 272.5°, dev 0.006 mm. Cell 2 is the waist circle (1,1). Captions match | OK |
| 7 | fraction inside \|z\| ≤ 2 | 0.7048 | 0.70483 (numeric 0.7048) | cubic and quintic cells: 0.705 of the parameter is inside the rims. Visible arc = drawn arc (61.3 / 61.3 and 95.3 / 95.5 mm); drawn-but-hidden ≤ 0.24 mm | OK |
| 8 | [A]² = [B]² = 0, [A]·[B] = 1, (2,3)² = 12, p_a = 2 | yes | 0, 0, 1, 12, 2 | not drawn (text only) | OK |
| 9 | b₂ quadric 2, cubic 7, h^{2,0} = 0 | yes | χ = 4 → b₂ = 2; χ = 9 → b₂ = 7 | not drawn | OK |
| 10 | Clebsch: 27 lines, 10 each, 135 pairs, 10 Eckardt, 105 ordinary | yes | 27 lines (residual 1.3e-15), each meets 10, 135 pairs, 115 points = 10 triple + 105 ordinary | not built (rank 3) | OK |
| 11 | waist spacing 2πk/(N√2) | 1.39 mm (k = 30, N = 96) | 1.3884 mm; N_max 166 | hero k = 33.87, so 1.57 mm. Row k = 7.97 with N = 32 (HANDOFF deviation from 16), so 1.11 mm. Same-colour floor breaks, see mandate 3 | PARTIAL |

Other measurements:
- **Visibility and completeness.** Drawn-but-hidden string length is 0.0 mm (blue) and 0.1 mm (gold), so hidden-line removal is exact. 84% (A) and 83% (B) of the visible ruling length is drawn. All undrawn length is either LOD trimming where the adjacent-ruling spacing is below 0.8 mm, or near-parallel shadowing under green (25 interior gaps at 3–20° to the green tangent, 208 mm in total). Only 12 mm (A) and 10 mm (B) is unexplained. Rulings A 11–13 and B 54–55 are fully dropped.
- **The eye** is a closed see-through component of 67.7 × 28.2 mm, 1503 mm², with its major axis at 150°. Ink inside it is zero in all four layers. It is 28.2 mm tall against a minimum of 28 mm, so it passes by 0.2 mm.
- **Frame.** The hero fills x ∈ [95.0, 282.0] exactly with no crop: 0 visible samples fall past the frame.
- **Rebus.** Blue slash at 148.5°, gold at 35.7°, parallel to the X (148.47° and 35.70°). The green circle is Ø 17.6 mm.
- **Minutes** recomputed from gcode at F600 plus 2.5 s per stroke: gold 40.8, blue 40.2, green 3.3, text 44.5, total 129. This matches the HANDOFF.

## Lies list       item | clean / VIOLATED (where)
| # | item | status |
|---|---|---|
| 1 | invented ribbon/blob as a variety | clean. Every string is on x²+y²−z²=1 (median 0.003 mm) and every green curve is on its declared algebraic curve (≤ 0.074 mm) |
| 2 | colour = cohomology vs cycles | clean. The key reads "BLUE, GOLD: ITS TWO FAMILIES OF LINES [A], [B]". H^{p,q} appears only as black text, "BOOKKEEPING, NOT DRAWN" |
| 3 | bent strings | clean. All 808 blue/gold strokes are exactly one G1 (2 points) |
| 4 | reference row C₀…C₄ / Σ aᵢCᵢ | clean. The row is [A], [B], [A]+[B], [A]+2[B], 2[A]+3[B], and each class was verified by back-projection |
| 5 | non-algebraic winding captioned as a cycle | clean. (1,2) and (2,3) are coprime and lie on the surface |
| 6 | closing clipped curves | clean. No invented arcs (all green vertices are on their conics). The cubic, quintic and hyperbolas end at rims or at visibility |
| 7 | "the picture proves the conjecture" | clean. "EVERYTHING DRAWN IS A THEOREM (LEFSCHETZ 1924). THE OPEN CASES BEGIN IN REAL DIMENSION 8." |
| 8 | ℤ for ℚ / Kähler for projective | clean. "RATIONAL", H^{2p}(X,ℚ), "PROJECTIVE" |
| 9 | positive-only gluing | clean. "A RATIONAL COMBINATION OF CLASSES OF SUBVARIETIES" |
| 10 | crossing counts as evidence | clean. No ticks and no numbered hits |

Encoding forbidden list: no outline, no dot at p, no axes, zero ink in the eye, same projection for the cells (e 50°, roll −30°, α₀ 235°, k 7.97): all clean. Punched holes: none in the strings. The green trims are discussed in mandates 1 and 2.

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 9**: The mathematics is exact everywhere I could measure it: the quadric, both rulings, six pencil conics, three row classes with the right coefficients, hidden lines, and the words. It is not a 10 only because the sheet's apparent focal node is not p (mandate 1).
- **fidelity 7**: Blue = [A], gold = [B] and green = a[A]+b[B] are carried exactly. Two things fall short. The channel "p = the pinch of the green loops" puts the visible convergence at the occlusion lip, 23.6 mm from p. The 0.8 mm same-colour floor is broken beside the heavy X bands.
- **legibility 6**: The circle does run through the X crossing, and the eye, rebus and honesty line land. But the six pencil members arrive as 15 disconnected green strokes. The far hyperbola branches float alone at the top. A stranger cannot read "circle → ellipses → parabola → hyperbolas → X" as one family closing on one point. The rebus has no class brackets, so "○ = ╲ + ╱" reads as set equality. Only the headline's "IN COHOMOLOGY" guards it.
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **The pinch is not at p (hero, around (152–193, 264–286) mm).**
   - p, the X crossing, is at (171.9, 285.8). Only the ψ = 0° circle reaches it (0.00 mm).
   - The other five members stop well short on the upper-right arm. The stops are 21.2 mm (15°), 13.8 (31.7°), 19.5 (45°), 8.1 (60°) and 8.2 (75°), which is not monotone in ψ, and 60° and 75° stop at the same radius. The encoding asks for staggered stops of about 14.3, 11.6, 10.7, 7.1 and 4.5 mm, which are its 16/13/12/8/5 mm scaled to k = 33.87.
   - On the lower-left arm, all five leave their visible 0–15.7 mm run next to p undrawn. After the occlusion gap they resume only at 23.7–28.8 mm, with a further 2.4–5.2 mm visible but undrawn there.
   - The 11 lower-left arm ends therefore bunch at centroid (155, 269), 23.6 mm SW of p. That bunch is the fan the eye reads as "the pinch", but it is the occlusion lip, not the base point.
   - Expected: staggered stops monotone in ψ on both arms, drawing the visible 0–15.7 mm lower-left run to each member's stagger radius. p should be the only convergence on the sheet.
2. **The pencil is fragmented mid-surface (hero, lower-right of the eye, (201–218, 246–268) mm).**
   - The ψ = 45°, 60° and 75° members have visible stretches left undrawn: 9.7, 8.9 and 7.4 mm, at 45–54, 40–49 and 34–42 mm from p. The 15° and 31.7° members lose 1.5 and 3.4 mm the same way.
   - The cause is green–green crowding. Neighbouring members project 0.33–0.92 mm apart there, below the floor, so the arcs stop in bare paper and restart as separate strokes.
   - The expected value is 0 mm undrawn mid-curve (encoding §11.3: no open curve ends mid-surface except at its stagger stop). Six curves currently arrive as 15 hero strokes.
   - Fix it structurally, without punching:
     - change the hinge or view so the members do not converge at the throat rim;
     - or drop one member (for example 75°) so the rest clear 0.8 mm;
     - or yield only the member that is later in ψ, at the crossing, and keep the gap under 3 mm.
3. **Same-colour floor broken beside the triple-pass X (hero near p, and row cells [A] and [B]).**
   - Minimum near-parallel same-colour gap measured:
     - hero gold: 0.651 mm at (176.6, 289.3), heavy B band against a neighbour ruling;
     - hero blue: 0.606 mm at (183.5, 278.8), heavy A band;
     - row blue: 0.427 mm at (38.7, 90.8), cell [A];
     - row gold: 0.604 mm at (89.9, 94.2), cell [B].
   - Length below 0.8 mm: hero gold 36.8, hero blue 21.8, row gold 23.4, row blue 25.1 mm.
   - Expected: at least 0.8 mm everywhere (encoding §10 and §11.1). With a 0.2 mm nib, 0.43 mm leaves 0.23 mm of paper, and the [A] band will flood on paper.
   - The row runs N = 32, not 16, which halves the waist spacing to 1.11 mm. Either return the cells to N = 16 (2.5 mm), or apply the LOD floor to the X-band neighbours, measured from the outer pass rather than from the centre line.

## Follow-up on open mandates   id | status | evidence
Pass 1. There is no `studio/millennium-hodge/LEDGER.md` and no prior S* mandates.
