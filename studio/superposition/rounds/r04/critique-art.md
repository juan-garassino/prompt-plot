# Art critique — superposition r04 · canon: none assigned in HANDOFF; judged against the stated lineage (systems art, Manfred Mohr *Cubic Limit*) + rubric · 2026-09-29
render: gallery/studio/superposition/current/pp_superposition_iterate_v15.png (gcode alongside) · a4 portrait, cream · 6 pens

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 7 | The black right triangle plus the red elbow bundle own the top half at 3 m; spikes → V → Z read second/third. But at blur (σ≈6 mm) the red bundle (mean ink 15.2) outweighs the triangle interior (10.8): the routing competes with the field, and Z, the answer of the mechanism, is the weakest mass on the sheet |
| 2 grid & alignment | 6 | Good: K strands drop on their columns onto the knife, Q elbows land on their rows at the vertical leg, spikes hang from the column eyes. Bad: five different left edges (red bundle x≈14, triangle/spike base x=30, V base x=15, Z base x=40, `Z = AV` x≈44, footer centred); red outer elbow sits ~4 mm inside the margin; K waves run to x≈200 at the right margin; Q and K baselines kiss end to end at x≈105 with a ~3 mm gap |
| 3 tension & asymmetry | 7 | The descending knife is a real working diagonal; red-from-the-left vs blue-from-above is asymmetric by the data. Lower half falls back to a centred column (V and Z both on x≈105) |
| 4 negative space | 6 | The masked future above the knife is shaped paper and good. Lower-left quadrant (x 10–60, y 25–85) and the pocket right of Z (x 130–170, y 25–60) are leftover, not composed; the `×1` ghost floats alone in the corner |
| 5 craft for pen | 7 | Contour eyes closed and even (~1.0–1.2 mm pitch, no floods); nested elbows ~1 mm pitch with round corners; 6 clean layers, 872 cycles, max in-layer hop 53.8 mm. Against: the 2-pass knife plots as two separate hairlines with a paper gap (a double outline, not a bold rule); dozens of short gold dash fragments (V negative lobes, V→Z strands); the six Z partial sums start and stop in mid-air instead of on the baseline |
| 6 concept legibility | 6 | Captions are gone and the field is a true causal triangle — no longer a slide. But the plate still reads top-to-bottom as the attention pipeline (Q,K → A → softmax → V → Z) with literal wiring into the matrix. The title word "superposition" is not yet what the eye sees: the Z curves cross and splay rather than visibly stacking. The joke sentence lives only at 30 cm |
| 7 depth & dimensionality | 6 | Declared flat (over/under only). At 3 m the over/under breaks in the Q/K/V families read as broken lines, not as weaving; the flatness is tolerated rather than exploited |

avg **6.43** · min **6** · VERDICT: **FAIL**

## Reads at a glance
A red comb of nested right-angle wires and a blue comb of drops feeding a black triangle of bullseyes, over a gold wave row that dribbles dashes into a small green bell — a well-drawn attention flowchart.

## Acceptance checks
No `encoding.md` / `BRIEF.md` exists for this slug, so there are no §11 checks. Reference in play → AUTHORING §6:
1. Main forms recognisable without colour fills — **PASS** (Q/K bands, triangle, spike row, V band, Z stack all separable in line alone).
2. Shadow/tone lines follow the surface — **PASS** (contour rings follow the attention field; conical, evenly pitched).
3. Fine lines that are really two sides of one thick stroke — **FAIL** (the 2-pass knife renders as two parallel hairlines ~0.8 mm apart; reads as a double outline).
4. Blackest regions intended — **PASS** (the eye at (123,172) and the corner eye are the real row maxima).
5. Labels readable at actual pen width — **FAIL** (footer line 3 — the Hermite rule, `ring n: A(i+1)=1.2ⁿ`, `itself·hole = 16.9/8 = 2.11` — is ~1.5 mm with subscripts, marginal at a fine nib; `plot` under the V baseline is touched by a gold curve at its `t`).
6. Thicker pen black knots at corners / filled eye highlights — **PASS** with a watch on the needle-slot core of the (123,172) eye.
7. Long empty travels / tiny marks with no benefit — **FAIL** (travel is fine; the V→Z dashed stair-steps and the dashed V negative lobes are many tiny marks that read as debris between y 30–90).
Interpretation of the reference: an honest rebuild (causal triangle for Q·Kᵀ, computed bells), not a trace. It has lost the reference's organising image — nested bells sharing a centre — in Q/K and in Z.
Lineage hang test (Mohr, *Cubic Limit*): not yet. The orthogonal nested red routing is the only Mohr-like passage; the rule is printed at caption size; beside Mohr this reads as a six-colour diagram.

## Biggest weakness
The superposition itself — the lower third — is the weakest part of the plate. The V→Z transfer breaks into dashed stair-step fragments. The six green partial sums cross each other and end in mid-air, and they sit small and centred. So the title's one literal claim ("Z is the stacked sum of the gold curves") is not visible, while the upper half's wiring is the loudest thing on the sheet.

## Mandates
1. **Z stack, y 20–90.** All six partial sums must start and end ON the green baseline, with no curve end in the air and no two sums crossing. The gold V→Z strands become continuous lines, with ink fraction carried by 1–3 passes, not dash duty, and each one ends exactly on the green sum it adds (gap 0 at a 30 cm crop). Test: zero gold fragments shorter than 3 mm between y 25 and y 88, and zero green stroke endpoints above the baseline.
2. **Make the field, not the routing, the darkest mass.** Test: after a ~6 mm Gaussian blur, the mean ink inside the triangle must exceed the mean ink of the red elbow bundle (now 10.8 vs 15.2). Do it by raising the triangle to ≥ 110 mm tall, apex at y ≥ 250 and base kept ≥ 0.85 of width, and by pulling the red bundle in: its outermost elbow no further left than x = 20, so the lanes stop fanning out to the margin. Delete or absorb the single-ring micro-circles, those ≤ 1.5 mm across, so the field reads as a mass and not as scattered bullseyes.
3. **One left edge, clear margins, clear labels.** The V baseline, spike baseline, Z baseline, `Z = AV` and all three footer lines start on x = 30, the triangle's vertical leg. The outermost red elbow must sit ≥ 6 mm inside the margin (x ≥ 16), and the K waves end by x ≤ 194. Open a stated Q|K gutter of ≥ 6 mm at x≈105. Every V token label keeps ≥ 1.5 mm of paper from gold ink. Set the footer rule line at ≥ 2.2 mm cap height, or cut it to `itself·hole = 2.11`.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| C1 vertical rhythm | FIXED | Q\|K top → triangle → spikes → V → Z stations all present in order, top to bottom |
| C3 in-layer hop ≤ 60 mm | FIXED | HANDOFF: max in-layer hop 53.8 mm; no sheet-crossing ghost travel visible inside a layer |
| C6 lineage holds when hung | PARTIAL | orthogonal nested routing is Mohr-like, and the rule is printed, but at 1.5 mm in the footer; beside *Cubic Limit* it reads as a diagram |
| A1 slide figure | PARTIAL | captions `Q·Kᵀ`, `softmax`, `1/13` are gone; the staged pipeline plus literal wiring still reads as a figure (concept 6, up from 3) |
| A3 symmetry | PARTIAL | the upper half is asymmetric (right triangle, red from the left, blue from above); V and Z are still centred on x≈105 |
| A4 dominance (keep r03's) | REGRESSED | triangle is only ~90 mm tall against r03's ~150 mm, and holds scattered eyes rather than a mass; the red bundle out-inks it at blur |
| A8 superposition literal | PARTIAL | six nested sums plus a ×1 ghost, one per caption term; but the sums cross, start and end mid-air, and several strands pass through sums without landing |
| A9 field craft | PARTIAL | rings closed and continuous, knife runs to the true apex and corner; the corner eye is still chopped by knife and base; ≤ 1 mm single circles persist as crumbs |
| A10 connectors arrive | PARTIAL | Q elbows land on their rows at the leg, K drops land on the knife (FIXED part); V→Z strands are dashed stair-steps, some ending between sums |
| A11 right triangle | FIXED | vertical leg at x=30, knife descends to the right, base 30→200 = 0.89 of the drawable width, apex top-left |
| A12 shared edges | NOT FIXED | five different left edges (14 / 15 / 30 / 40 / 44) plus a centred footer |
| A13 strip furniture | FIXED | only token names, `Z = AV`, the `×2.5`/`×1` scale marks (required by S1) and the footer remain |
| S1 (in A8) Z scale | FIXED (art side) | `×2.5` is declared on the sheet with a dashed 1× ghost |
| S2 field labelled | n/a art | rule `ring n: A(i+1) = 1.2ⁿ` is printed in the footer; the numbers are for the science critic |
| S3 rule + provenance on sheet | FIXED (legibility-limited) | footer carries GPT-2 small L11 H8, the sentence, the Hermite rule and `itself·hole = 16.9/8 = 2.11`; line 3 is too small (see mandate 3) |
| S4 token identity | NOT FIXED (deferred) | Q/K bands carry no token marks; the query " itself" is no longer flagged in the Q band (r02 had a label plus a marker) |

DESCRIPTION § Keep:
- Vertical spine with a mass/line alternation — **still true** (triangle / spikes / V / Z alternate), though the stations no longer share one axis.
- Two-eyed conical contour map with even rings — **craft still true** (conical, even pitch); the two-eyed identity is replaced by data eyes.
- Connector fans that leave vertically, run flat and arrive — **true for Q/K** (orthogonal elbows, better than r02's dashes); **not true for V→Z** (diagonal dashed stair-steps).
- Colour as provenance, black for operations — **true**.
- V widest band against a narrow Z — **weakened**: the Z baseline now runs x 40–193 to carry the ×1 ghost, so the contraction reads less.

## Regressions vs compare-to
- **vs r02 (parent):** the Z stack lost its shared-centre nesting. r02's 7 bells were concentric around one peak; r04's sums skew left, cross and end in the air. This is the reference's key image, and it got worse.
- **vs r02:** the Q/K families shrank to ~15 mm tall and are chopped by over/under gaps, so at 3 m they read as broken lines. r02's families were taller and continuous. The query " itself" marker in the Q band is gone.
- **vs r02:** the V band is denser and dashed below the baseline, and now grazes its own token labels (`plot`).
- **vs r03 (field grammar donor):** the field lost r03's continuous, dominant ring mass. It is back to isolated bullseyes in a mostly empty triangle, which is the exact r02 criticism, and the triangle is ~60 mm shorter.
- **Improved, and keep:** the knife now runs to the true apex; the Q/K strands arrive; the station captions are gone; black spike droplines hang from the column eyes; the layer discipline holds (6 layers, 872 cycles, 53.8 mm max hop).
