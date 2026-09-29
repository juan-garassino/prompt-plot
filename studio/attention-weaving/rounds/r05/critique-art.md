# Art critique — attention-weaving r05 · canon: none assigned in HANDOFF (judged against BRIEF + rubric; no `lineage:` line either) · 2026-09-28
render: gallery/studio/attention_weaving/current/pp_attention_weaving_area-smooth_v7.png

## Scores

| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 7 | The fan collapsing into the slit dominates at 3 m. Giant `SUMS / TO ONE` is a clear second. The green run-out and the gold band tie for third, and neither has a reason to be there. |
| 2 | grid & alignment | 6 | The left edge is shared by type, the V reeds and the wall, and the readout block hangs off the slit's right edge (x 130). But `K` is jammed into the top-right frame corner (x ≈ 222, y ≈ 283, under the preview legend), and `Z = A V` floats on the `ONE` baseline, lined up with no geometry. |
| 3 | tension & asymmetry | 7 | The slit sits left of centre (78–130 mm), the green turns hard right, and the type counterweights bottom-left. The upper fan is close to mirror-symmetric about the crimson vertical. |
| 4 | negative space | 5 | The 5-pass black hill and the thin cumulative curve are drawn across about 15 crimson/blue strands with no gap, which is collision, not decision. `1.000` grazes blue arcs at (135, 210). The quiet zone right of the readout (130–230 × 140–180) is leftover, not shaped. |
| 5 | craft for pen | 6 | Travel (16.2 m) exceeds draw (15.6 m). The V strands dissolve into a scatter of 2–4 mm gold fragments inside the green (100–140, 90–165). Six K arcs end in open air. The `N` diagonal in the giant type is one hairline against 3-pass stems. Spacing ≥ 0.8 mm holds, and 5 pens (4 swaps) is at the limit. |
| 6 | concept legibility | 5 | "Everything through one aperture" reads at a glance. But the centre of the plate is now a plotted density curve plus its CDF, i.e. a chart, with a 4-line stats footer and a 3-line readout. The brief's braid below the waist is 28 parallel lanes with no twist. |
| 7 | depth & dimensionality | 5 | Q/K over/under gaps and the dashed compass arcs behind give a thin layer of depth. The lower half is flat parallel lanes, and no flatness is declared. |

**avg 5.86 · min 5 · VERDICT: FAIL**

## Reads at a glance
A red-and-blue sunburst drains through a hole in a black wall and leaves as a flat green cable running right, with a black bell curve sitting in the hole and `SUMS TO ONE` below.

## Acceptance checks
BRIEF "What must be TRUE" (there is no encoding.md):
- Everything passes through the waist (count in = count out): **PASS** for Q+K → Z (28 in, 28 out). **FAIL** for V: 17 gold strands are born at the left margin and die as dashes inside the green without visibly joining it.
- Over/under is real at every crossing: **PARTIAL**. Q×K is real (one strand breaks at each crossing). V×Z starts as over/under and then decays into fragments. The black hill and CDF cross Q/K strands with neither one breaking.
- Softmax normalises, visibly peaked, never uniform: **PASS**. The two-humped area hill is labelled `1.000`.
- V joins only after the waist: **PASS**.
- The braid carries more strands than Q or K alone: **PASS** (28 > 15, 13). It is not a braid, though: no twist and no ply crossings.
- `lineage:` stated in HANDOFF (rubric LINEAGE rule): **FAIL**, missing.

AUTHORING §6 (reference in play):
1. Forms recognisable without colour: **PASS**. Q is straight rays, K is arcs, V is left-entering arcs, Z is lanes.
2. Shadow lines follow the surface: **PASS** (n/a, no tonal hatch).
3. Fine lines that are two sides of one thick stroke: **PASS**.
4. Blackest regions intended: **PARTIAL**. The type and wall are intended. The hill peak laid over the double-passed crimson vertical and 6–8 strands is congestion.
5. Labels readable at pen width: **FAIL**. `1.000` grazes K strands, and `K` is pressed into the frame corner.
6. Thick pen knots at corners: **PASS (marginal)**. About 28 strands terminate onto the 5-pass hill baseline at ~1.8 mm pitch.
7. Empty travels / tiny marks with no benefit: **FAIL**. Travel exceeds draw, and the gold dissolution leaves dozens of sub-5 mm dashes.

## Biggest weakness
The bottom half is still the weak half, which is exactly what Juan flagged. Gold is a band of parallel arcs that fizzles into crumbs, and green is 28 parallel lanes with an 80 mm dead run-out (150–230 mm) to the right frame. Meanwhile the new smooth hill fixed the staircase but was laid on top of the weave as a chart, with no occlusion.

## Mandates
1. **Rebuild the lower half in the top's grammar.** Green leaves the slit as a fan that spreads to both the bottom and right frame edges; delete the 80 mm parallel run-out at x 150–230. Gold becomes one crossing family that meets every green lane at ≥ 45° with a visible gap on one strand at each crossing, and each gold strand ends on a green lane or a reed tick, never as a stub. Test: no gold segment shorter than 5 mm on the sheet, and no two adjacent green lanes stay parallel for more than 40 mm.
2. **Make the softmax hill a decision, not an overlay.** Every crimson/blue strand crossing the black hill line or the cumulative curve breaks with a ≥ 1 mm gap each side (the strands go under the profile), and the `1.000` label has ≥ 2 mm clear paper to every strand. Test: at 4× crop of (78–140, 184–215), no coloured line touches black ink.
3. **Close the K bundle and seat its label.** The six blue arcs that currently end in open air at x ≈ 160–215, y ≈ 185–240 (including both double-passed arcs) each run to a reed tick on the right frame edge, or are cut. Move `K` to mirror `Q` (x ≈ 222, y ≈ 245, right-aligned to the frame) so it is not in the top-right corner. Test: every blue strand has one end in the slit and the other on a tick.

## Follow-up on open mandates
There is no LEDGER.md. The open items are Juan's REWORK note (J) and DESCRIPTION.md § "If only iterating" (D).

| id | status | evidence |
|---|---|---|
| J1 bring the bottom up to the top | NOT FIXED | Gold is still parallel arcs from the left, green is still a vertical cable plus a parallel run-out. Only the bend tangle is gone. |
| J2 smoother softmax profile | FIXED | One C¹ two-humped hill, no steps or plateaus, no knot discs. |
| J3 keep the partition exact | FIXED (as claimed) | `Σa = 1.000000000` in the footer, cumulative ends labelled `1.000`, partition ticks on the wall. |
| D1 smooth area-preserving curve, cumulative labelled | FIXED | See J2. `1.000` label present, but it grazes K strands. |
| D2 green as a fan to bottom+right, remove bend tangle | PARTIAL | The tangle at (0.58–0.67, 0.50–0.58) is gone. The fan was not built, and the parallel run-out is intact. |
| D3 gold as ~12 spiral arcs crossing every lane ≥ 45° | NOT FIXED | 17 parallel gold arcs from the left margin, dissolving into dashes. |
| DESC weak: footer leading inconsistent | FIXED | Four footer lines on an even ~7.5 mm pitch. |
| DESC weak: `SOFTMAX` label far from profile | FIXED | Now at the slit's right shoulder (x 133). |

§ Keep check:
- Whole upper half with real Q/K over/under: **PARTIAL**. The over/under is intact, but the fan dropped from ~38 to 28 strands and reads thinner.
- Wall as a 5-pass rule with one hole: **TRUE**.
- Exact partition, 38 in / 38 out: **CHANGED**, now 28/28. It is still exact.
- Principal query as a single double-passed crimson vertical: **TRUE** (x ≈ 105).
- Giant `SUMS / TO ONE` flush-left: **TRUE**.

## Regressions vs compare-to (aperture_v19)
- The upper sunburst thinned from ~22 Q + 16 K to 15 Q + 13 K. The top-left quadrant (20–90, 210–290) is now sparse, and this is the half Juan praised.
- The softmax profile grew from a low 4–6 mm plateau to a ~30 mm hill. It now crosses about 15 Q/K strands with no occlusion. v19's low profile crossed almost none.
- A new 3-line readout (`0.416 TRANSFORMER …`) under the wall's right arm adds a second lab caption to a plate that already has a 4-line footer, pushing it further toward a scientific figure.
- Improved: the green bend tangle is gone, and the gold-in-cable dashed grid is lighter than v19's.
