# Art critique — resonance r04 · canon: Op Art (lineage Bridget Riley, *Current*, 1964; twist Young 1807) · 2026-09-29
render: gallery/studio/resonance/current/pp_resonance_one-field_v6.png (+ .gcode, measured directly: 4 contiguous colour layers; draw 10.51 m, travel 5.03 m; per layer: 0 crimson 32 strokes / 1.05 m draw, 1 blue 33 / 1.05 m, 2 black 551 / 7.06 m draw + 3.21 m travel (largest single travel 288 mm), 3 black-fine type 217 / 1.35 m draw + 1.00 m travel)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | The black fringe sunburst owns the sheet at 3 m. The heavy peak line is a clear second. But the subject, the Q·K knot where red and blue actually interfere, is a ~50 mm patch (x 33–95, y 195–275), smaller than either black lobe next to it. The loudest mass is the "sum" rather than the resonance. |
| 2 | grid & alignment | 5 | The title is flush left on the margin and the field crops at both side margins, which is good. The peaks, however, are not registered to the ray bundles that feed them. Bundle 1 lands on peak 1's right flank (x 30–42) instead of its axis (x≈28). Bundle 6 lands left of peak 6 (x≈188). The far-left lower bundle stops in mid-air at y≈118 and never reaches the baseline. The colour region ends on an arbitrary circle (r≈45 mm around the source midpoint) that no other element shares. |
| 3 | tension & asymmetry | 7 | The sources sit upper-left and the fan throws a real diagonal toward the lower right, with the title bottom-left as the counterweight. This is asymmetric and alive. |
| 4 | negative space | 6 | The dark fringes left as bare paper are the best idea on the sheet: destructive interference really is blank. The 50 mm band between the baseline and the title (y 25–75), though, is leftover and not shaped. The ray dashes also run into and through the heavy line at peaks 1–3, which is collision rather than overlap. |
| 5 | craft for pen | 5 | Crest pitch is λ 3.4 mm everywhere and there is no flood in the field. Problems: (a) at every peak tip the multi-pass heavy line closes into a solid black wedge (~3 mm tall at peak 2, x≈61 y≈118); (b) same-pen dashes cross the heavy line at peaks 1–3; (c) doubled or blobbed stroke ends at the top of the continuous arcs in the right lobe (x 120–160, y≈235); (d) in layer 2 the largest single travel is 288 mm, a sheet-crossing move, and total travel is 45 % of draw; the type layer spends 1.00 m of travel for 1.35 m of ink. |
| 6 | concept legibility | 5 | The order is right: INTERFERING, with a real two-source field, and "Q·K is Young's experiment" is a genuine twist. But the lower third is Young's textbook intensity trace, a baseline with six Gaussian peaks, which is an extruded function (a figure). The whole sheet reads as the Wikipedia double-slit diagram: sources, fringes, screen. The black "sum" is drawn with a different mark (dashes, black) from its parts (continuous red and blue), so the eye reads a style change, not a sum. |
| 7 | depth & dimensionality | 4 | Flat, and the HANDOFF does not declare it. Every crest is one weight at one pitch. Nothing swells or recedes, which is the one thing Op Art exists to do. The radiating fan gives a hint of perspective and nothing more. |

avg **5.43** · min **4** · **VERDICT: FAIL**

## Reads at a glance
From 3 m: a black dashed sunburst radiating from a small red-and-blue bullseye in the upper left, landing on a row of six spikes, in other words a two-slit physics diagram.

## Acceptance checks
There is no `encoding.md` or `BRIEF.md` for this slug, so there are no §11 checks. A reference is named, so these are the AUTHORING §6 questions, plus the lineage test:

1. Main forms recognisable without colour? **PASS.** Sources, fringes and screen read in black alone, and the labels carry Q and K.
2. Marks follow the form rather than a random mesh? **PASS**, with a caveat. The dashes follow the crest hyperbolae. The upper-left lobes break into a brick lattice of short dashes, and the colour-to-black handover is a hard circular seam.
3. Any fine lines that are really the two sides of one thick stroke? **PASS.**
4. Blackest regions intended? **FAIL.** The six peak tips flood solid, and dash-on-heavy-line crossings at peaks 1–3 add accidental black.
5. Labels readable at real pen width? **PASS.** The title caps are ~9 mm and the data lines are clear of geometry. The Q glyph is ~1 mm from the first crimson ring: tight, but it reads.
6. Thicker pen makes black knots? **FAIL.** Knots at the peak tips, at the dash/curve crossings, and at the doubled arc ends at x 120–160, y≈235.
7. Long empty travels or excessive tiny marks? **FAIL.** A 288 mm single travel in layer 2, and 3.2 m of travel against 7.1 m of draw.
- Lineage: would it hold hung beside Riley's *Current*? **FAIL.** There is no line family whose phase or amplitude drift makes the surface move. The only optical vibration is the red/blue moiré inside the 50 mm knot. The rest is sparse dashes at constant pitch.

## Biggest weakness
The plate is Young's textbook figure split in two: a fringe fan on top and an intensity graph underneath. It is not one Op-Art surface. The vibration that would make it Riley (red and blue crests crossing) is caged in a 50 mm disc, and the rest of the sheet is uniform black dashes plus a plotted curve.

## Mandates
1. **Delete the graph.** Remove the Gaussian-peak curve. The "screen" becomes one straight horizontal rule at y≈78, and the softmax weight is carried by the fringe bundles themselves (pass count or dash duty rising toward the screen in proportion to that bundle's weight). Test: no stroke in the lower third rises more than 2 mm above the screen rule, and nothing on the sheet reads as a plotted curve.
2. **Make the surface move (depth + Riley).** Within each bright-fringe bundle, the crest weight must fall off from the bundle's centreline to its flanks: centre crests continuous at 2–3 passes, flank crests single-pass and broken, with duty tracking intensity. Each bundle should read at 1 m as a rounded ridge, not a stack of equal dashes. Uncap the colour so the red and blue crests run out to at least r = 90 mm from the source midpoint, not stopping on the r≈45 mm circle. Test: no hard circular colour boundary is visible, and every bundle has a visibly heavier centreline than its edges.
3. **Craft and registration.** Every bundle ends exactly on the screen rule, and that includes the far-left bundle that now stops at y≈118. No black dash may cross or touch another black stroke; keep ≥ 1 mm clearance. Remove the doubled stroke ends at the arc tops (x 120–160, y≈235). Re-order layer 2 so that no single travel exceeds 60 mm (it is 288 mm now) and the layer's travel is ≤ 25 % of its draw. The type layer should not spend more travel than 50 % of its ink.

## Follow-up on open mandates
There is no `LEDGER.md` for this slug. Open items are taken from `FEEDBACK.md` (J1 the dotted-lines note, J2 the KEEP THE ORIGINAL note) and from DESCRIPTION.md § Next versions 1 "one-field" (N1–N4), which is the thesis this round claims.

| id | status | evidence |
|---|---|---|
| J1 dotted lines: continuous round dots at 0.9–1.1 mm | NOT FIXED | This is sidestepped rather than solved: every dotted path was deleted, and the fringe field is drawn in long dashes, the very mark Juan rejected ("do not trade the dots for dashes"). |
| J2 KEEP THE ORIGINAL: v13 is the design, keep every element, change only dot continuity | REGRESSED | Juan's note (2026-09-28 23:39) postdates this render (22:41) and binds against its whole thesis. Wave packets, halos, scattered dots, leaders, MoE, Z, V, Y and four of six pens are all removed. This round cannot become resonance; if one-field is pursued it must live as a separate sibling slug. |
| N1 crest field ~80 % of width, cropped at both side edges | FIXED | The black fringes run margin to margin, x 10–200. |
| N2 Q and K only as sources; every box, arrow and gradient label deleted | FIXED | Only two source dots, two letters and the title block remain. |
| N3 softmax as intensity along one horizontal cut, a single heavy line | PARTIAL | Delivered as asked, but the result is a plotted curve (a figure), and it is not registered to the bundles (see mandate 1). |
| N4 pen count 2–3 | PARTIAL | 4 pens: two black pens for sum/heavy and type. This is defensible as layer discipline, but not what was specified. |

**DESCRIPTION § Keep:**
- Hero construction verbatim: **NOT KEPT.** It is still crest loci, but re-parameterised (d = 6λ, λ 3.4 mm, against the approved d = 35·L, L 1.30 mm). The dense ~1 mm ring texture that made the v13 hero is gone.
- The funnel (ten crimson plus ten blue fans): **LOST.**
- Pen economy of the hero (open net, no flood): **KEPT** in the field, and broken at the peak tips.
- Packet vocabulary: **LOST.**
- MoE fork: **LOST.**

## Regressions vs compare-to (v13)
- **The waves are gone.** Juan named exactly this regression ("not to remove the waves"). All Q/K/V/Z/Y packet rows are deleted.
- **The funnel is gone.** v13's one strong gestural shape (converging dotted fans from both top corners) has no counterpart here.
- **The hero's texture is coarsened.** v13's ~1 mm-pitch double bullseye with its lens cells is replaced by 3.4 mm-pitch rings. What gave v13 its density and shimmer now looks sparse.
- **Six pens down to four.** Juan explicitly wants all six kept.
- Better than v13 (for the record, not a pass): travel fell from 11.3 m to 5.0 m, commands from 59k to 31.8k, and the pipeline schematic is gone. These are the wins the one-field thesis should carry if it becomes its own slug.
