# Science critique — millennium-hodge r02 · mathematics (algebraic geometry) · 2026-09-29
render: gallery/studio/millennium_hodge/trials/pp_millennium_hodge_abstract_v25.png (+ .gcode; physical-width preview rounds/r02/phys_preview_v25.png)
pass: 1 (cold; no LEDGER.md exists). Blind: no piece.py / NOTES.md / audit.py opened. All sheet
measurements come from my own gcode parser plus an independent exact model: orthographic view, az 0,
el 50°, roll 0, H = 2, N = 96, and a proper right-handed basis (right × up = toward viewer). The
sheet transform was **fitted, not assumed**: k = 60.00 mm/unit, α0 = 350.00°, roll 0.00°, and origin
at (200.0, 165.0). The fit reproduces every one of the 373 non-rebus string strokes.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | rulings on x²+y²−z²=1 | < 1e-14 | 3.6e-15 | All 194 gold + 179 blue centre strokes lie on the exact projected rulings B(β0+2πj/96) / A(α0+2πi/96). Perpendicular deviation: median 0.003 mm, max 0.0066 mm (gcode rounds to 0.01 mm). | OK |
| 2 | string twist; rim radius; 3D length | 126.87°, 2.2361, 5.657 | 126.870°, 2.23607, 5.65685 | H = 2 is confirmed on the sheet. The gold-X top end (71.4, 212.8) back-projects to z = +2.000 and the blue-X bottom end (71.4, 58.6) to z = −2.000. The other two X ends stop at the declared frame crop x = 282. | OK |
| 3 | tangent plane x=1 ∩ Q = y=±z (the X) | A(0) ∪ B(0) | confirmed | The X is blue idx 0 × gold idx 0. The strings cross at (189.6, 119.7), which is the exact projection of p = (cos 350°, sin 350°, 0). The waist circle (ψ=0) passes 0.00 mm from p. | OK |
| 4 | pencil types; far vertex z = −tan2ψ | ellipse/parabola@45°/hyperbola/X@90° | 15° → −0.577, 60° → +1.732, 75° → +0.577 (formula exact) | The 16 non-rebus green strokes back-project to ψ = 0.00, 15.00, 31.72, 45.00, 60.00 and 75.00, with per-stroke σψ ≤ 0.03° and max deviation from the conic ≤ 0.03 mm. The open members end at \|z\| = 2.000 or at the frame, and none is closed. | OK |
| 5 | last whole ellipse | tanψ = 1/φ = 0.6180, ψ = 31.72° | 0.618034, 31.7175° | ψ = 31.72° is present (strokes at (169.9,123.8)→(129.5,154.7) and (282,145.1)→(209.8,118.3)). Its z = −2 vertex projects to (223.3, 189.1) and is **hidden** in this view, so the "grazes the rim" moment is not on the sheet. The sheet makes no claim about it. | OK (not shown) |
| 6 | (p,q) class, degree, \|p−q\| exits | 3/5/7 … | confirmed (after the projective sign flip for odd p−q) | not drawn (abstract: no row) | n/a |
| 7 | fraction inside \|z\|≤2 | 0.7048 | 0.704833 | not drawn | n/a |
| 8 | (2,3)² = 12, genus 2 | 12, 2 | 12, 2 | not drawn | n/a |
| 9 | b₂: quadric 2, cubic 7; h^{2,0}=0 | 2, 7 | χ = 4, 9 | **not stated on the sheet** (see M3) | n/a |
| 10 | Clebsch: 27 lines, 10 each, 135 pairs, 10 Eckardt + 105 = 115 points | as stated | 27 / {10} / 135 / 10 + 105 = 115; residual 3.7e-15 | not drawn | n/a |
| 11 | waist spacing 2πk/(N√2) | 1.39 mm @ k30 | 1.388 @ k30 → **2.777 @ k60** | Gold perpendicular spacing near p has a median of 2.37 mm (oblique view). Same-colour near-parallel pairs closer than 0.8 mm for more than 3 mm: **0**, apart from the intended 5-pass bands (offsets 0.15/0.30 mm) on the X and rebus. | OK |
| — | the eye (see-through) | ≥ 45 mm tall, zero ink | exact ray test | 119.5 × 50.0 mm, 4712 mm². Ink inside: gold 1.0, blue 0.8, green 0.2 mm, all endpoint rounding at the envelope. | OK |
| — | hidden-line truth | no ink on hidden parts | exact ray–quadric | Strings: 0 segments with hidden ink > 0.1 mm (max 0.02 mm). Green: ≤ 0.6 mm per member, at visibility transitions. Index-0 X runs = visible runs to 0.01 mm. | OK |
| — | string coverage | LOD halving, pause-resume | — | Visible length drawn: gold 16718/18915 mm (88%), blue 15540/17686 mm (88%). The undrawn part breaks down as: spacing-floor LOD 1709/1722 mm; near-parallel green shadow 384/313 mm (the longest single cut is 55 mm, gold idx 5, (152.7,149.6)→(104,175.5), under the ψ=75 back branch); marginal (neighbour 0.9–1.2 mm, mostly idx ±1 beside the 0.8 mm X band) 103/111 mm; text halo 3 mm. No punched holes. | OK |
| — | HANDOFF minutes | 38.5/35.7/3.3/34.2 | from gcode: 17907/600 + 207·2.5 s = 38.5; 35.7; 3.3; 34.2 | matches. *Aside (not science):* the gcode draw feed is **F2200**, not the F600 the estimate assumes. | OK |

## Lies list
| item | status |
|---|---|
| 1 invented surface | clean. Every string is an exact ruling of x²+y²−z²=1 at the stated view. |
| 2 colour = cohomology | clean. Blue = [A] and gold = [B], both cycles. No H^{p,q} ink or text-as-shape. |
| 3 bent strings | clean. All 399 gold/blue strokes are single 2-point G1 segments. |
| 4 reference row / C₀…C₄ / Σaᵢ Cᵢ | clean (no row). |
| 5 non-algebraic winding | clean (none drawn). The green is exactly the ψ-pencil. |
| 6 closing clipped curves | clean. Every green point is on its conic, and the open members end at a rim or the frame. |
| 7 picture proves the conjecture | clean. "EVERYTHING DRAWN HERE IS A THEOREM (LEFSCHETZ 1924)" and "… SUBVARIETIES? OPEN." |
| 8 ℤ / Kähler | clean. "RATIONAL" ×2, "PROJECTIVE". |
| 9 positive-only gluing / "assembled from shapes" | clean in text, **at risk in the rebus**. `○ = ╱ + ╲` has no class brackets, so it reads literally as "a circle is built from two lines" (M1). |
| 10 crossing counts | clean. |

## Scores
truth 9 · fidelity 8 · legibility 7 · **VERDICT: FAIL** (legibility < 8)

- truth: the geometry is exact everywhere I could measure it. There are two caption defects. "GREEN: PLANES ABOUT ONE TANGENT LINE" labels curves as planes, and the rebus claims equality without saying it is equality of classes.
- fidelity: the string, X and eye channels are perfect. In the green channel, 74 mm of visible class-[A]+[B] curve is simply missing mid-surface (M2), and the pinch stagger is out of order.
- legibility: the X, the pinch at p and the eye all land. Three things do not. The sheet never says *why* this surface is a Hodge case (h^{2,0}=0, so every class is Hodge and spanned by [A], [B]). The rebus teaches the §5 misconception instead of correcting it. The ψ=90 X is broken by two true 14 mm occlusion gaps, gold (147.0,153.3)→(158.2,144.5) and blue (234.0,142.7)→(246.7,149.3), so at 3 m the "two straight strings" read as four bars. Those gaps are honest at α0 = 350°. Encoding 5A's "gold X unbroken crop to rim" was written for α0 = 235°.

## Mandates
1. **Rebus is shape equality, not class equality.** Top right, x 150–282, y 377–400: the rebus reads `○ = ╱ + ╲` with 0 bracket glyphs. Expected: `[○] = [╱] + [╲]`, the same square brackets the sheet already uses for the [A]/[B] tags. Otherwise it needs an "AS CLASSES" line under it, so it states [circle] = [A] + [B] in H²(Q, ℚ). Without this, the plate's largest type asserts the dossier §5 misconception ("a circle is assembled from two lines"). Keep the slants: 27.36° and 141.77° already match the X to 0.01°.
2. **Green class-curves are missing visible arcs.** Measured visible-but-undrawn length outside the p-stagger:
   - ψ = 75° hyperbola, ~45 mm at (236.9,145.3)→(279.3,159.4), z 1.23→1.99, under the blue X band;
   - ψ = 75°, 11 mm at (142.8,155.0)→(152.8,149.6);
   - ψ = 60°, 18 mm at (142.2,149.4)→(159.8,144.9), z 1.82→2.00.

   Expected: 0 mm. A member may end only at a rim, a true occlusion boundary, the frame, or its stagger stop near p (encoding §4/§11.3). Where green conflicts with a string, the string yields (§10), not the class curve.

   Also fix the stagger order. Measured stop distances from p (189.6,119.7) are 15° → 31.0 mm, 31.72° → 20.1 mm, **45° → 24.6 mm**, 60° → 12.0 mm and 75° → 8.5 mm. Expected: strictly decreasing with ψ, so the loops visibly close onto the X in pencil order.
3. **The key must carry the Hodge bridge and label green correctly.** The left key, x 15–88, y 150–185, reads "GREEN: PLANES ABOUT ONE TANGENT LINE." Expected: green = the *curves* cut by planes turning about the tangent line at the crossing. The key also omits the one sentence that makes this plate about Hodge (measured: absent; the encoding §10 key had it). Add: "HERE h^{2,0}=0: EVERY CLASS IS A HODGE CLASS, AND ALL ARE BUILT FROM [A] AND [B]". Otherwise "EVERYTHING DRAWN HERE IS A THEOREM (LEFSCHETZ 1924)" names a theorem without saying what it guarantees on this surface.

## Follow-up on open mandates
none. This is pass 1 and `studio/millennium-hodge/LEDGER.md` does not exist yet.
