# Art critique — neural-networks-cnn r04 · canon: none declared (lineage: Nees, *Schotter*) · 2026-09-29
render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png (gcode beside it)

There is no `encoding.md` or `BRIEF.md` in the slug. The plate is judged against the HANDOFF thesis and lineage, `studio/nets/cnn.md` and DESIGN_RUBRIC. The HANDOFF names no STYLES.md canon, so the plate is judged as an answer to *Schotter*. Coordinates are sheet mm (x right, y up), as in the preview axes. The preview is white; cream is not docked (A12).

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 6 | At 3 m the dominant mass is the black input plane (y 32–75), not the destination. The meaning, a CAM summit, is the smallest element on the sheet: five crimson arcs about 18 × 7 mm at x 130–148, y 264–271, sitting on a gentle 7-row hump. The four ERF loops are single crimson hairlines, so they are scarce but not loud. The title is hairline, single-pass type. The second and third reads are fine at 1 m, and the rows reward 30 cm. |
| 2 grid & alignment | 7 | This is real. Every plane is right-flush at x = 195. The type axis x = 17.75 is shared by the title, the caption and the input plane's front-left corner. The four inter-plane gaps are equal at 13.08 mm. The title top (y 281) matches the top plane's back row. |
| 3 tension & asymmetry | 7 | Right-flush planes that shear down-left build a real staircase diagonal. A quiet triangle opens on the left, and the title hangs in its top. Nothing crops at the frame, and the stack's width only runs 1.46 : 1 (146 → 100 mm). |
| 4 negative space | 6 | The quiet triangle (x 17–60, y 80–235) is shaped by the staircase, which is good. Two gaps are leftovers. "MEANING" ends at x ≈ 83 on the same baseline (y ≈ 241) that the top plane's front row starts at, x ≈ 90, so there is 7 mm between word and line and it reads as a collision. The caption's top line (y ≈ 24.5) sits about 7 mm under the input front row (y ≈ 32), half the declared 13.08 mm rhythm. |
| 5 craft for pen | 6 | Two pens, clean layers, 11.5 k commands, no floods. Measured on the gcode: no terrain stroke is under 3 mm (every short stroke is a glyph). **Rows on the 224² plane come under the 0.8 mm floor**: about 3,200 samples at a 0.15 mm step (y 25–75), plus 232 on the 14² plane (y 200–225), with a minimum near 0.5 mm. A stray hook climbs about 5 mm up-left at the 28² back-left corner (x 78–82, y 180–184). The crimson 28² loop breaks at x 113–117, y 166–169 and resumes lower, then hugs a black ridge for about 10 mm, so on paper the break reads as a slip, not occlusion. |
| 6 concept legibility | 6 | The laminar order lands without the caption: resolution collapses and texture calms up the sheet. This is *Schotter* inverted (disorder → order), and the progression is now monotone. The receptive field does not land. Four near-equal crimson ovals (≈ 90 / 80 / 72 / 60 mm wide), unconnected to the summit, read as "the same blob on each plane". That one small cell at the top sees a quarter of every map below only reads through line 2 of the caption. The stack of five reliefs plus a measured caption stays close to the rubric's "scientific figure", and there is no twist. |
| 7 depth & dimensionality | 7 | Hidden-line profile rows on one oblique basis with real occlusion breaks give solid planes from 224² to 14². The input plane's 3 mm relief reads as texture on a slab, which is correct. The 7² plane is 7 wires at a 4.24 mm pitch and reads as loose lines, not a surface. |
| **avg** | **6.43** | |
| **min** | **6** | |
| **VERDICT** | **FAIL** | |

## Reads at a glance
Five sheared slabs of horizontal scan-lines stack up the sheet, dense and scratchy at the bottom and thinning to a few wavy lines at the top. Faint red ovals sit on the slabs, and a small red target sits on the top one. At 3 m the red barely registers.

## Acceptance checks
No encoding §11 exists, so these come from the brief (`studio/nets/cnn.md`). No reference is in play, so AUTHORING §6 does not apply.
- A vertical stack of 4–5 hidden-line terrains — **PASS** (5 planes, occluded rows)
- Fine and busy at the bottom → few, tall and smooth at the top — **PASS** (rows 38/28/19/14/7, relief 3 → 20 mm, breaks per row falling)
- The tallest HIGH peak in red — **PARTIAL** (red sits on the argmax crest, but the crest does not read as the tallest form)
- A red receptive-field window on each layer, connected up a column — **FAIL by design** (the loops are present, the column was deleted under A1; the widening is left unreadable)
- The left axis and layer labels — **FAIL by design** (removed per rubric NO SCHEMATICS, which is correct)
- Title FROM PIXELS TO MEANING — **PASS**
- Black and red only, cream — **PASS** (preview white, tooling)
- A bottom mini-diagram — **FAIL by design** (absent, which is correct)
- Rubric failure modes: dead-centre subject — PASS. Furniture checklist — PASS. Elements at similar scale — **PARTIAL** (five slabs at 1.46 : 1). Accent scarce and loud — **PARTIAL** (scarce, not loud). Type against geometry — **FAIL** ("MEANING" against the top plane's front row). Scientific figure — **PARTIAL**.

## Biggest weakness
The thing the plate exists to say has become the quietest mark on the sheet: one cell of meaning sees a quarter of the image. The summit is an 18 × 7 mm crimson target on a mild hump. The four receptive-field loops are hairline ovals of almost equal size, and 46–70 % of each loop's length runs within 0.5 mm of black rows. So at 3 m the plate is a density gradient with no destination, and the red story needs the caption.

## Mandates
1. **Make the 7² summit the reading destination.** The argmax crest must read as a mountain at a 1/6-scale thumbnail. The crimson cap's bounding box must be ≥ 30 × 12 mm on paper (now ≈ 18 × 7 at x 130–148, y 264–271). It must be carried by a black hidden-line crest that is visibly the tallest single rise on the sheet, and the 7² rows must read as one surface, not loose wires. Test: in the thumbnail, the eye lands on the red summit before the input plane.
2. **Make the crimson loops the loudest line on each plane.** Draw them heavier than any black row, with a double pass or a wider nib. No crimson run may lie parallel within 0.5 mm of a black row for more than 3 mm (now 46–70 % of each loop's length is within 0.5 mm). The 28² occlusion break at x 113–117, y 166–169 must resume at the same height on the far side of the occluding ridge, so it cannot read as a slip. Test: at the 1/6 thumbnail all four loops and the summit are visible as one crimson family.
3. **Craft floor and declared gaps.** Test each of these on the gcode and on the sheet:
   - (a) zero black–black approaches under 0.8 mm outside the type (now about 3,200 samples on the 224² plane at y 25–75, minimum ≈ 0.5 mm);
   - (b) delete the hook at x 78–82, y 180–184;
   - (c) caption-to-input-plane gap = 13.08 mm (now ≈ 7). The title must clear the top plane's front row by ≥ 13 mm (now 7 mm, from x 83 to x 90 on y ≈ 241).

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A3 | PARTIAL | The loops stay closed and crimson, and the 28² loop now carries 1 break. The 14² loop has no break, which the test asked for. The 28² break resumes lower and hugs the black ridge for about 10 mm (x 117–127, y 166–169), so it reads as a slip. |
| A4 | PARTIAL | There is no flat baseline row, and all 7 rows are present, reaching x ≈ 190. The back rows beside the cap are dashed (x 113–125, y 268–273), and the plane reads as 7 wires, not a solid surface. |
| A11 | FIXED | The title is single-pass. The crop shows no doubled strokes. |
| A12 | argued | The preview is still white. Tooling, not docked. |
| A14 | PARTIAL (worse than r03 on "destination") | The crimson now sits on the surface, not floating (fixed), and 0 mm of ring comes within 0.5 mm of black. But the argmax is no longer a mountain or the tallest-reading form: the cap is ≈ 18 × 7 mm against r02's ≈ 45 × 55 mm silhouette and r03's ≈ 15 × 45 mm coil. |
| A15 | PARTIAL | Rows 38/28/19/14/7 and pitch 1.16/1.43/1.96/2.37/4.24 are strictly monotone. Breaks per row fall strictly (28² is calmer than 56²). No terrain stroke is under 3 mm. **The spike is NOT removed**: it moved up with the plane to x 78–82, y 180–184. The torn front-left corner of 28² persists as a wiggle at x ≈ 48–52, y ≈ 143–146. |
| A5 (preserve) | holds | Four equal 13.08 mm gaps. |
| A6 (preserve) | holds | Title top y 281, right edges x 195, input bottom y ≈ 15 (bbox 17.75–195 × 15.05–281). |
| A7 residue | FIXED | Title, caption and the input corner share x = 17.75. |
| A8 (preserve) | REGRESSED (partial) | There is no flood, but input-plane rows come under 0.8 mm again (minimum ≈ 0.5 mm; see mandate 3a). |

Rule-2 watch: A3's occlusion clause is PARTIAL, not NOT FIXED. A15 is PARTIAL, but its named spike clause specifically is NOT FIXED.

## Regressions vs compare-to
- **Summit (vs r02 and vs r03).** r02 had a 45 × 55 mm black mountain with a crimson cap. r03 had a 45 mm-tall crimson coil. r04 has an 18 × 7 mm target on a low hump, so the top of the sheet lost its destination. The r03 top plane's big black hills (up to 30 mm rise) have also gone, and the plane is now 7 near-flat wires.
- **Title weight.** Going single-pass fixed A11 but turned the title into hairline caption-weight type at poster size. In r03 it was the sheet's second mass, and now it is the lightest thing on the sheet.
- **Title vs top plane.** r03 had about 15 mm between "MEANING" and the top plane. In r04 the front row starts 7 mm after the "G" on the same baseline.
- **Caption placement.** r03 kept the caption under the title in the quiet triangle. In r04 it sits in a 7 mm slot under the input plane, which breaks the 13.08 mm rhythm.
- **Row floor.** r03 had the input plane clean at a 1.02 mm pitch (A8 held). r04 has sub-0.8 mm approaches on the 224² plane.
- Improvements held: one grammar, equal gaps (10.9 → 13.08), monotone resolution/relief/fragmentation, frame clearance, shared type axis, crimson no longer floating over paper.

DESCRIPTION § Keep:
- Morphology gradient up the stack: **true**, and stronger than ever (monotone).
- Single crimson summit as the one loud accent: **weakened**. It is present and scarce but too small to be loud.
- Dashed rails fanning upward: **no longer true**. They were deleted under A1 on purpose, and the receptive-field widening has no carrier now (mandates 1 and 2).
- Rightward stagger / diagonal: **true** (right-flush shear staircase).
- Hidden-line occlusion with solid surfaces: **true for 224²–14²**. The 7² plane reads as wires.
