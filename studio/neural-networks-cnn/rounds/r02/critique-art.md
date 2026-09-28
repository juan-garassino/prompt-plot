# Art critique — neural-networks-cnn r02 · canon: none declared (lineage: Nees, *Schotter*) · 2026-09-28
render: ~/Downloads/pp_neural_networks_cnn_one-valley_v12.png

No `encoding.md` or `BRIEF.md` in the slug. The plate is judged against the HANDOFF thesis and lineage, `studio/nets/cnn.md` and DESIGN_RUBRIC. The HANDOFF names no STYLES.md canon, so the plate is judged as an answer to *Schotter*. Coordinates below are sheet mm (x right, y up), as in the preview axes. The drawable margin is 10 mm (x 10–200, y 10–287).

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 7 | At 3 m you see the tall peak with its crimson cap (x 115–160, y 225–268) first. The giant 4-line title comes second and the noisy stack third. The one weakness is that the four crimson ERF loops on the lower layers (the bottom one is ≈95 × 25 mm) pull the eye away from the summit. The accent is no longer scarce. |
| 2 grid & alignment | 6 | The title, caption and the bottom layer's left edge share x = 10, which is good. `F R O M`'s cap top sits on the top margin (y ≈ 287) with 0 mm clearance. The top terrain's right edge (x ≈ 200) and the bottom layer's left edge (x = 10) end exactly on the margin as straight clip lines. They read as "stopped by the frame", not "cropped through it". The right ends of the layers step ragged (200 / 198 / 186 / 188 / 200). |
| 3 tension & asymmetry | 7 | There is a real diagonal from the peak at top-right down to the full-width raster at bottom-left, and the heavy title block in the upper left counterweights it. This is the first time the stack is not a centred totem. |
| 4 negative space | 6 | The empty wedge under the title (x 10–70, y 60–225) is shaped by the stagger, and it works. The gaps between layers are not designed: ≈12 mm under the peak, ≈10, then ≈4 mm (block_12 front edge y ≈ 104 against block_2 back edge y ≈ 99) and ≈4 mm (y ≈ 60 against y ≈ 55). The lower half is congested and the upper half breathes, with no stated reason. The crimson dashed rails run across the surfaces of the terrains, which is collision, not decided overlap. |
| 5 craft for pen | 5 | 2 pens, no floods, and the bottom raster no longer goes solid (a real gain). Problems: (a) 26,641 commands with 12.6 m travel against 15.3 m draw, because block_5 (y 100–140) and block_12 (y 150–185) are shredded into hundreds of 1–3 mm stubs and isolated ticks, and Leo drags ink on every lift. (b) The crimson isolines on the peak alternate crimson and black along the same ring (x 125–150, y 235–250), so one curve is split between two pens and registration will show. (c) Small ink knots at the left summit (x ≈ 105, y ≈ 238: a closed mini-loop plus a hook) and at x ≈ 126, y ≈ 237. (d) Title strokes are doubled ≈0.6 mm apart and will merge. (e) Some front-row pairs on the bottom raster at the left (x 10–25, y 15–22) sit ≈0.7 mm apart. (f) The render is on white, but HANDOFF says cream. |
| 6 concept legibility | 4 | Real data (MobileNetV2 on a real image, a real argmax unit and a computed ERF) is a big step up. Read bottom to top, "noise distils to one peak" lands without labels. But the form is still the Zeiler–Fergus/Distill figure: stacked projected activation reliefs joined by a dashed receptive-field frustum. That is the rubric's "scientific figure: a relief of the quantity", with the frustum as apparatus. The *Schotter* order (one element, one controlled parameter, order → disorder) is not the plate's rule, because each layer uses a different mark grammar: scanlines, dense quad mesh, shredded mesh, smooth mesh with contours. There is no twist: `P(TIGER CAT) = 0.43` sits in the caption and is not on the sheet. |
| 7 depth & dimensionality | 6 | Projected reliefs and a stacked recession. Hidden-line is inconsistent. On the top terrain the far rows run straight through the nearer hill (x 115–150, y 200–222), so that surface reads as transparent wire. The crimson rails are not occluded by the terrains they cross. There is no line-weight or density falloff between layers. |

avg **5.86** · min **4** · **VERDICT: FAIL**

## Reads at a glance
At 3 m a stranger sees a stack of wireframe landscapes, noisy at the bottom and settling into one big red-tipped mountain at top-right: a CNN feature-hierarchy figure with a very large title.

## Acceptance checks
(No encoding §11. These checks come from the HANDOFF thesis and lineage.)
- Top peak = CAM of the top-1 class, argmax unit's isolines in crimson: **PASS**. One clear summit, and the crimson cap sits on it.
- ERF 50 % ring on each of the four lower layers, as a readable closed footprint: **PARTIAL**. Input (y 15–40) and block_2 (y 65–90) carry closed loops. On block_5 (y 110–130) and block_12 (y 158–180) the crimson breaks into ridge-following arcs and fragments that read as crimson contours of noise, not a footprint.
- Order → disorder down the sheet (*Schotter*): **PASS as a gradient, FAIL as a lineage**. The disorder does increase downward, but *Schotter* gets there with one element under one controlled parameter. Here the element changes on every layer, so it would not hold its own hung beside Nees.
- No schematic: **FAIL**. The dashed receptive-field frustum joining stacked layer planes is the textbook apparatus.
- Plottable (≥0.8 mm, ≤4 pens, bounds clean, sane lifts): **PARTIAL**. Pens and bounds are fine; the stub debris, the split-pen rings and the title touching the margin fail.
- Paper cream: **FAIL**. The render is on white.

## Biggest weakness
The plate has real data but no single rule. Four layers are drawn in four different mark languages and tied together by a dashed frustum, so the result is an accurate activation figure rather than the *Schotter*-grade "one mark, one parameter, order dissolving to noise" it claims to answer.

## Mandates
1. **One mark grammar on every layer.** Draw all five maps with the same element: the bottom layer's horizontal profile rows (hidden-line, no cross-mesh). Let only row pitch (fine at the input, coarse at the CAM) and roughness change with depth. Row pitch ≥1.0 mm everywhere, and no run shorter than 3 mm. Test: zoom any layer and find only continuous horizontal profile lines; no vertical mesh ticks anywhere on the sheet; total commands < 12,000.
2. **Delete the dashed crimson rails, and make every crimson footprint one closed, occluded curve.** Keep exactly one crimson loop per lower layer (the ERF 50 % contour, smoothed to a single closed ring) and the summit isolines. Each isoline must be drawn wholly in crimson, never alternating with black along one ring. Nearer terrain must hide crimson behind it. Also fix the top terrain's hidden-line so far rows stop at the nearer hill's silhouette (x 115–150, y 200–222). Test: no crimson between layers; blocks 5 and 12 each show one unbroken crimson loop; no line crosses the interior of a nearer ridge.
3. **Set the vertical rhythm and clear the frame.** Make the inter-layer gaps either equal (≥10 mm each) or a declared monotone progression (e.g. 14 / 11 / 8 / 5 mm growing tighter toward the noise). The current 12 / 10 / 4 / 4 is not a rhythm. Drop the title so `F R O M`'s cap top is ≥6 mm below the top margin. Either pull the top terrain's right edge ≥5 mm inside x = 200, or push it past the frame so the crop visibly cuts through mesh. Render on cream. Test: measure the gaps; the title clears y = 281; no element's edge coincides with a margin line.

## Follow-up on open mandates
No `LEDGER.md` or `FEEDBACK.md` exists for this slug. Open mandates checked below are r01's art mandates (r01-M*) and DESCRIPTION § Next versions 2 (one-valley, which this round executes) / § If only iterating.
| id | status | evidence |
|---|---|---|
| r01-M1 face-on Molnár lattice, no projection/frustum | NOT FIXED | The designer switched to the one-valley direction. Projection and the dashed frustum are both present. |
| r01-M2 one cell rule; crimson the largest mass | PARTIAL | The crimson summit is now dominant (≈35 × 45 mm), but there is still no single mark rule: four grammars across the layers. |
| r01-M3 type one axis, ≥5 mm inside margin, deck ≤2 lines | PARTIAL | Deck cut to one line and one flush-left axis at x = 10 (fixed), but `FROM` touches the top margin (0 mm). |
| NV-2 real activation maps, peak where the object is | FIXED | HANDOFF: MobileNetV2 on "chelsea", CAM top layer, computed argmax unit and ERF. |
| NV-2 drop axis + layer labels | FIXED | No axis, no layer names. |
| NV-2 PIXELS the full bottom width, no flood | FIXED | The input raster spans x 10–200, and the rows are separable. |
| NV-2 / iter-1 crimson through the z-buffer | NOT FIXED | The dashed rails still draw over the surfaces of the terrains they cross (e.g. x 120–135, y 195–240 on the top terrain). |
| iter-2 no debris | PARTIAL | No floating quads, but block_5 and block_12 are shredded into stubs and ticks. |
| iter-3 diagonal that crops the frame | PARTIAL | The diagonal is strong, but the terrains stop on the margin lines rather than cropping through the frame. |

DESCRIPTION § Keep:
- Morphology gradient up the stack: **still true, stronger.** It now comes from real data.
- Single crimson summit as the scarce, loud accent: **partial.** The summit leads, but four ERF loops and the rails spend crimson across the whole sheet.
- Dashed rails fanning upward: **no longer true.** They now converge upward, which is physically correct for a fixed-size drawing of shrinking maps. Mandate 2 deletes them.
- Rightward stagger: **still true, pushed to a real diagonal.**
- Hidden-line occlusion on the terrains: **regressed.** See below.

## Regressions vs compare-to (pp_cnn_dashes)
- **Hidden-line lost on the top terrain.** The parent's surfaces read as solid. In r02 the far rows run through the nearer hill (x 115–150, y 200–222), so the most important surface reads as transparent wire.
- **Mesh continuity lost on the middle layers.** The parent's EDGES/TEXTURES were continuous quad meshes. r02's block_5 and block_12 are crumbs, so commands rise from 18,102 to 26,641 and there are more lifts, even though the travel ratio improved (0.99 → 0.82).
- **Crimson no longer scarce.** The parent kept crimson to the summit plus whisper rails. r02 adds four large ERF loops and a crimson/black alternating ring on the cap.
- **Paper tone lost again.** The parent previews on cream; r02 previews on white, even though HANDOFF says cream. This regression was already flagged in r01.
- **Title pressed against the frame.** The parent title sat ≈15 mm inside; r02's `FROM` touches the top margin.
- Gains to bank: real data end to end; the PIXELS flood is gone; the axis and labels are gone; there is a genuine diagonal; the caption is one line.
