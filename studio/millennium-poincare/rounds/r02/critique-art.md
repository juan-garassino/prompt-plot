# Art critique — millennium-poincare r02 · canon: 6 MODERN SCIENCE POSTER (cream, black + crimson) · 2026-09-29
render: gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.png (judged on gallery/studio/millennium_poincare/current/pp_millennium_poincare_abstract_v4_phys.png, true nib widths)
thesis: abstract (flat by declaration)

## Scores

| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 8 | A's nest is clearly the one dominant body, the title is second, and the red circle sits at the hinge. But the loudest black on the sheet is A's dashed lower-left crescent, not the event. The 1.6 mm extinction dots vanish at 3 m. |
| 2 | grid & alignment | 8 | Title, statement and SOLVED are flush at x=15. The corner caption and the footer share one right column (x≈195). The stamp text hangs on its own indent. The colophon sits under the footer column. Clean. |
| 3 | tension & asymmetry | 8 | The mass rises on a true 62° diagonal, and the upper-left triangle is bare. The body is off-centre, low-left, with the small lobe climbing toward the caption. This is the canon's asymmetric body. |
| 4 | negative space | 7 | The quiet zone, the bare waist void and the bare discs around both points are all decisions. Against that, the outer rims of A (x 40–120, y 30–60) and B (x 170–240, y 250–297) break into dashes. The paper there reads as leftover residue, not as chosen void. |
| 5 | craft for pen | 7 | Min pen-0 gap measured on the gcode is ≥ 0.8 mm (keyline double pass excluded), and the plate needs only 1 swap. But 23 pen-0 strokes are < 6 mm and 31 are < 12 mm, all of them pause-resume stubs. The 0.5 red circle runs within 0.02 mm of the double-passed keyline (4.7 % of the red path is < 0.8 mm from black), which is a knot risk at the hinge. The gcode draws at F2000 with 0.2 s dwells, but HANDOFF budgets F600 (Leo drags at that setting). |
| 6 | concept legibility | 7 | Not a schematic, not a figure: the abstract order (one closed form splitting into two nests that each close on a point) reads. The time story does not. Past halo, keyline and future rings are the same 0.3 black at the same density, so it reads as one contour map. "Past outside and future inside the surgery instant" cannot be recovered. |
| 7 | depth & dimensionality | 7 | The flatness is declared, and the two mounds read strongly as terraced topography. The occlusion stack (cards landing on the keyline) is invisible, though. Nothing visibly *lands*, so the depth reads as one hill map, not as stacked instants. |

**avg 7.43 · min 7 · VERDICT: FAIL** (avg < 8)

## Reads at a glance
At 3 m a stranger sees a topographic map of a two-peaked island joined by a narrow pass, with a red ring in the pass. They see it as a quiet, confident mass on a diagonal. The red points in the peaks do not carry at that distance, and nothing tells them that one line is special.

## Acceptance checks (encoding §11)

1. **Branching at 3 m — PASS.** One closed dumbbell encloses two nests, each closing on a red point. B's ring count is visibly a handful against A's many. No pen-0 line crosses another (min gap ≥ 0.8 mm on the gcode).
2. **Time is honest — PASS (thin).** The gaps widen toward both points (A centre crop: inner steps ≈ 5–7 mm, rim ≈ 1.5 mm). Rings crowd at the far poles and splay at the cut. The past fan at the waist is the weak part: the left bundle of ~6 lines reads as a nearly parallel ribbon. The acceleration toward the keyline is not visible by eye.
3. **The cut — PASS.** The circle is tangent inside the neck. Ø ≈ 14.5 mm against A ≈ 170 mm wide (0.085 ≤ 0.1). The interior is bare, with ≈ 2.5 mm bare paper to A's cap-tip ring and ≈ 2.7 mm to B's, both just over the 2 mm floor. No stray red.
4. **Hierarchy and silence — PASS.** A is well over 3× any other mass. The upper-left is bare. The mass is on the diagonal and not centred. No caption touches a line (footer ≥ 15 mm from A's right rim). The min gcode gap is ≥ 0.8 mm.
5. **[abstract] Flatness declared, two mounds — PASS.** Flatness is declared in HANDOFF; NOTES is not opened, by the blindness rule. The two nests read as two mounds.

AUTHORING §6 (reference = AI globe-and-loops poster; this is an interpretation, not a trace):
1. Forms recognisable without fills — PASS.
2. Lines follow the form, not a random mesh — PASS.
3. Fine lines that are really two sides of one thick stroke — PASS (none).
4. Blackest regions intended — PARTIAL. The far-pole crowding is intended, but its dashed stubs look accidental.
5. Labels readable at true width — PASS.
6. Thicker pen knots — PARTIAL. Red 0.5 lies on the black keyline at both tangent points.
7. Excessive tiny marks — FAIL. There are 23 sub-6 mm pen-0 fragments with no visible benefit.

## Biggest weakness
The keyline (the surgery instant, the one line the whole encoding hinges on) looks like every other line. The halo, the keyline and both nests are the same black, weight and density. The plate therefore reads as a contour map of two hills, not as "the space before, the cut, the space after". Meanwhile the darkest, noisiest thing on the sheet is the dashed stutter along A's lower-left rim. The eye lands on the artefact, not on the event.

## Mandates
1. **Kill the stutter at the rims.** Along A's lower-left far pole (x 40–120, y 30–60), A's lower-right (x 170–190, y 40–70) and B's top/right rim (x 170–240, y 250–297), a paused ring must stay paused for the whole crowded arc, not re-enter as dashes. Test: the gcode has zero pen-0 strokes shorter than 8 mm (now 23 < 6 mm and 31 < 12 mm). In the crops, every rim line is either continuous or cleanly absent.
2. **Make the keyline the one line that stands alone.** Give the t_s keyline a bare moat of ≥ 2.5 mm on both sides along its full length. The keyline ranks highest in the merge rule, so the last halo line and the first ring pause inside that clearance. This is a clearance change, not a re-spacing. Test: at 1 m, the dumbbell outline reads as a single line with white paper on both sides, separating the outer (past) family from the inner (future) nests. On the gcode, no pen-0 point other than the keyline pair lies within 2.5 mm of the keyline.
3. **Take the red off the black at the waist.** Keep the circle reading as tangent, but hold ≥ 0.8 mm of bare paper between the red caps and the keyline. Do this by shrinking the drawn cap radius by ≈ 1 mm about the cut centre, or by pausing the keyline where the caps run alongside it, whichever the encoding allows. Test: no red point within 0.8 mm of any pen-0 point (now min 0.02 mm, 4.7 % of the circle). In the waist crop, a cream hairline separates red from black at both tangent points.

Polish (not mandates): the extinction points at Ø 1.6 mm do not carry at 3 m, contrary to §2's own 3-m read, so consider Ø 2.4–3 mm. Reconcile the gcode feed (F2000, 0.2 s dwell) with the Leo profile the budget assumes (F600, long dwells).

## Follow-up on open mandates
No LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists for this slug, and HANDOFF declares no compare-to (a new plate; r01 is the parallel faithful sibling, not a parent). There are no open A*/J* mandates to track and no § Keep items to check.

| id | status | evidence |
|---|---|---|
| — | — | none open |

## Regressions vs compare-to
None assessable. There is no compare-to render (new abstract plate).
