# Synth — superposition after r02 ∥ r03 · 2026-09-29
route: designer
next round: r04 · parent: **r02 (merge base)**, plus r03's field grammar and plot discipline. By the house ranking r03 is best-so-far on the last tie-break only (art avg 4.86 vs 4.71; art min 3 = 3, science min 5 = 5). The curator note decides the parent: Juan picked this plate for its vertical rhythm, and only r02 keeps it. r03 broke it (Q moved to a side ruler, V and Z became single curves)

## The instruction
Fork r02 and keep its data (GPT-2 small L11H8, query " itself", `rounds/r02/head.npz` + `mechanism.py`), its Hermite projection rule and its five stations top to bottom. Then do two things. Make one black mass command the sheet, and make the title literal. **The mass:** redraw the causal matrix in r03's shape and grammar, as a RIGHT triangle. Key 0 is the vertical edge on the left, the causal knife runs down to the lower right, the apex is top-left, and the base spans ≥ 0.85 of the drawable width. Contour it with r03's kernel-blended ladder, normalised so the field at every cell centre equals the value you encode. Rings are continuous and on a constant pitch. The masked future is blank paper, cut by one drawn knife that reaches the true apex. **The inputs:** keep the reference's pair on top, the Q family top-left and the K family top-right. Q strands leave their family, run down a left gutter and arrive horizontally on their rows. K strands leave vertically, step left in a nested non-crossing staircase and arrive on the knife at their diagonal cell. **The spine:** the " itself" row drops its five above-uniform keys straight down their key columns into the softmax spikes and on to their V clusters. Softmax and V now register under the triangle's columns, so the spine leans with the data and does not sit on u 0.50. **The one new idea, Z by visible addition:** draw six green partial sums, `hole`, `+transformer`, `+plot`, `+ter`, `+watched`, `+rest`. They share one centre and one baseline and use the V rule and the V scale (or a declared `×k` with the 1× curve drawn as a ghost). The last one is exactly R(z). Every gold V→Z strand ends ON the green curve its term creates. Delete the station captions. One footer line on the fine black pen states the rule, the provenance and one checkable inner product.

## Mandates to close
1. **C1 (curator / Juan): keep the rhythm Q/K → field → softmax → V → Z.** Q and K stay as families on top (not side rulers), then the field, then the spikes, then the widest V band, then the Z nest. Test: reading top to bottom meets the five stations in that order, and V is still the widest band (≥ 0.85 of the width) against a narrower Z.
2. **A8 + S1: superposition is literal.** Exactly 6 green curves, one per footer term. Each is Σ over its top-m terms of a_j·R(V_j), under the same R and scale as the gold V curves or behind a printed `×k` with a 1× ghost. They are nested on one centre with no crossing, and the outermost equals R(z) (no template Gaussian with round-number μ/σ). NOTES must state that the ẑ-aligned frame makes R(z) a pure φ0 by construction. Test: every gold strand terminates on a green curve (gap 0 mm), and a science re-fit of the outermost curve against R(z) gives an rms under 0.05 mm.
3. **S2 + A9 + A11: the field is true, continuous, dominant and asymmetric.** Choose one encoding, A or lift ln(A·(i+1)), and draw it: the field at each cell centre is within 2 % of the value, no contour level sits above the encoded maximum (for A, no level ≥ 1.0), and equal values get equal ring counts (normalise the kernel overlap). Print the rule in the footer, e.g. "ring = ×1.2 above uniform 1/(i+1)". Test: zero black pairs under 0.8 mm inside the triangle, no contour fragment under 3 mm, no ring ends on an undrawn line, the (14,14) and every other eye lies wholly inside the frame, and the triangle is the darkest and largest element at thumbnail size.
4. **A10 + C3: every connector arrives, and every layer batches.** Every Q strand ends on its row edge, every K strand on its diagonal cell and every V→Z strand on its green curve. There are no strokes under 1.5 mm (r02 had 102 gold crumbs), no dotted runs, and every dash is duty-coded through one helper (r03's `_dashed`). Test on the **emitted** gcode, after the pipeline's per-colour reorder: no in-layer travel over 60 mm (r02 had 241 mm black and 103 mm gold). The budget table lists minutes per layer and in total. Target ≤ 900 pen cycles and ≤ 75 min including swaps; that is a ceiling to stay under, not a goal to reach.
5. **S3 + C6: the Mohr rule is visible.** The footer (y ≈ 13–20, fine black pen, plotted last) names `GPT-2 small · layer 11 · head 8 · query " itself"`, the Hermite rule f(x) = Σ (c·eₙ) φₙ(x/σ) with its 3 modes, and one checkable readout: itself·hole = 16.9 raw / 2.11 scaled, with a small mark at cell (12, hole) in the triangle. Test: the art critic can run Mohr's hang test ("the rule is the image"), and the science critic can recover every bump's meaning from the sheet alone. NOTES must carry a check-number table (quantity · value · where · mm) for every mark rule. This closes S5 for this round.

Deferred: A12 (shared edges; revisit r05), S4 (Q/K token names; the five attended keys stay labelled), A13 is folded into the instruction (captions deleted, rule text only in the footer).

## Preserve
- **r02 data and provenance:** `rounds/r02/mechanism.py` + `head.npz` (numpy forward matched to torch at ≤ 2.3e-6), A recomputed from Q and K with |A − A_file| = 0.
- **r02 softmax row:** exact and linear at 72 mm per unit attention. Science measured every spike within 0.02 mm; keep that scale.
- **r02 footer caption:** ".26 hole + .14 transformer + .14 plot + .13 ter + .11 watched + .23 rest" is true as printed, and the six green curves must match its six terms.
- **r03 field craft:** 1.10–1.17 mm continuous rings, the causal void as the plate's best negative space, one black mass dominant at 3 m (A4, fixed in r03).
- **r03 exact duty-coded dashes** (duty = a_j to 3 decimals) and its serpentine lane order.
- **Plot discipline from both rounds:** one pen per meaning, each layer entered once, light → dark (goldenrod V → dodgerblue K → crimson Q → forestgreen Z → black field and softmax → fine black type), no stipple, no debris, no dotted guides.
- **Colour as provenance with black for operations** (r01 Keep #4), and the wide V band against a narrower Z (r01 Keep #5).
- **HANDOFF lines:** `declared: flat — <reason>` (A7, fixed in r02, lost in r03) and `lineage: Manfred Mohr, Cubic Limit (1973–75) — <order it lends>`.

## Do not
- Do not draw any curve as a template: no Gaussian with round-number μ/σ standing in for a computed sum. Do not draw Z at an undeclared scale.
- Do not let the field exceed its encoded maximum, and do not label it `Q·Kᵀ` when it draws something else.
- Do not clip rings along a line that is not drawn. Do not chop an eye with the frame. Do not leave crumbs where two cones overlap.
- Do not end any strand in mid-air or on nothing.
- Do not bring back figure furniture: no tick rows, tick axis, section cut, dashed 1/13 threshold, or `softmax` / `Q·Kᵀ` / `1/13` captions.
- Do not switch data or head. Do not import r03's induction sentence, SVD rulers or Riley row-line family (A14 dropped).
- Do not trust the pipeline's nearest-start pass to reproduce your chain. It restarts every colour from (0, 0) and never reverses. Measure the hops on the emitted gcode.
- Do not buy tone with dots. A long session is allowed, but thousands of lifts are not.

## Fabrication gate
Not run, because neither critic passed. Sanity check for the record (`promptplot plot layer <gcode> --list`): r02 has 5 layers (201 / 191 / 174 / 8 / 549 strokes), each entered once. r03 has 6 layers (47 / 20 / 20 / 2 / 63 / 168 strokes), each entered once. No file under `promptplot/` changed in this piece's rounds, so the regression suite is not required.

## Flavours kept on disk
- r01 `faithful`: the measured reference recreation, Juan's pick, unscored.
- r03 `interference`: the induction-head field with the best field craft. Its S2/A9 fixes carry into r04.
- r02 is the merge base and is not kept as a separate flavour unless r04 regresses it.
