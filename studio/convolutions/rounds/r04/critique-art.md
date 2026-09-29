# Art critique — convolutions r04 · canon: Op Art / Ben-Day (flat, one lifted plane) · lineage: Vasarely, Vega · 2026-09-28
render: gallery/studio/convolutions/trials/pp_convolutions_iterate_v9.png (gcode beside it; a4 landscape, cream; 3 pens black / crimson / dodgerblue)

## Scores

| # | dimension | score | evidence |
|---|---|---|---|
| 1 | hierarchy | 7 | At 3 m the black contour mass dominates, the boxed kernel head at the bite is clearly second, and the blue ring column on the lower lobe is third. At 30 cm the dot-area ramp and the ring counts pay off. The dominant mass is the INPUT, though, not the operation. |
| 2 | grid & alignment | 7 | The lattice is strict (14.4 mm stride-2 nodes) and the head sits on it. The legend's top row (y≈184) is level with the mass's crown (y≈185), and the title baseline (y≈26) is level with the bottom dot row (y≈25). The legend's left edge (x≈200) and the title's (x≈198) are 2 mm apart, which is close but not shared. The side margins are unequal: 14 mm clear on the left, 9 mm on the right at the title. |
| 3 | tension & asymmetry | 7 | The staircase wavefront drives a real diagonal from top-left to bottom-right, and the masses are off-centre with the weight in the upper-left. The head overlapping the bite is a chosen overlap. Nothing crops at the frame, so everything sits politely inside the margins. |
| 4 | negative space | 5 | The lower-right quadrant (x 140–285, y 20–140, about 145×120 mm) is leftover rather than shaped. It holds only the title, and the legend floats above it. The mass's closed outline stops about 15 mm short of every edge. The quiet zone makes nothing louder; it reads as where the plate ran out. |
| 5 | craft for pen | 6 | Ring pitch is fine: 1.02 mm on the response rings and about 1.07 mm in the contour nest. Problems: (a) the kernel collars are 7 concentric passes at 0.27 mm pitch (r 1.54→3.17 mm) with only 0.44 mm clear to the black dot, and in the head crop the collar already fuses into the dot; (b) the layer order is black first, crimson then blue, so colour lands on wet black; (c) travel is 5.6 m against 11.1 m of drawing (50 %), and there are sheet-crossing travels of 256 mm (blue) and 184 mm (black), mostly out to the legend swatches; (d) the diagonals of both N's in the title are hairlines against fat verticals, so the weight breaks; (e) there is a wobbly 3 mm crumb of clipped contour in the first step pocket (x≈50, y≈182). |
| 6 | concept legibility | 6 | The sweep order reads: a window has passed over a field and left a transformed wake behind a staircase front. The LoG kernel pattern (blue cross in a crimson surround) is legible. But the unswept remainder's silhouette reads as a tilted HEART with an almond eye, which is an accidental nameable object. The upper-left response rings read as scattered targets rather than an edge map. The legend explains formulas instead of confirming them ("rings = round(4\|y\|/max\|y\|)"), which is the lab-figure tell. |
| 7 | depth & dimensionality | 5 | Flatness is declared, so this is not capped at ≤4. But the one declared plane barely lifts: its 1.5 mm drop shadow is a second hairline box that reads as a registration double, not as a card above the sheet. The contour lines stopping at the shadow edge is the only real occlusion cue. |

**avg 6.14 · min 5 · VERDICT: FAIL**

Lineage check: Vega's order is a lattice DISPLACED by a hidden volume, meaning node positions bulge. Here the lattice never moves and only the dot size changes. That is Ben-Day halftone wearing the Vega name, so it would not hold its own hung beside a Vega. The lineage is borrowed surface.

## Reads at a glance
A black striped heart bitten by a dotted grid, with a red-and-blue dot badge sitting at the bite.

## Acceptance checks
There is no `encoding.md` or `BRIEF.md` for this slug. These checks come from the HANDOFF `rule:` line plus AUTHORING §6 (reference: `studio/convolutions/ref/reference.png`).

HANDOFF rule:
- Swept nodes (i+j ≤ 10) are dots and unswept nodes are rings, split by a staircase front: **PASS**. The front is a clean 2-node staircase.
- Rings centred on the node's own input sample, count 0–4 by \|y\|, no ring at y=0: **PASS**. Counts 1–4 are visible and pitch is 1.02 mm.
- x = 0 samples are paper: **PASS**. There are empty-centred rings at nodes where x=0 (e.g. lower column, left and right edges).
- Head at (5,6), 5×5 LoG, drop shadow, occludes rings and contours: **PASS** geometrically. As depth it fails (see dim 7).

AUTHORING §6 (judged as an interpretation of the reference):
1. Main forms recognisable without colour: **PASS**. The mass, lattice and head all read in black alone. The sign of the rings (crimson vs blue) is lost in monochrome.
2. Shadow lines follow the surface: **PASS**. The clipped contour stubs in the step pockets follow the ring family.
3. Fine lines that are two sides of one thick stroke: **FAIL**. The head outline plus its 1.5 mm offset shadow reads as a doubled keyline.
4. Blackest regions intended: **PASS**. The contour nest holds about 1.07 mm and the almond eye stays open.
5. Labels readable at real pen width: **PASS**. The legend reads at about 3 mm cap height. The title N diagonals are hairline (craft flaw, not a legibility failure).
6. Thicker pen makes knots or fills highlights: **FAIL**. The collar (0.27 mm pitch) sits 0.44 mm from the black dot and fuses into it already in the preview.
7. Long empty travels or excessive tiny marks: **FAIL**. 50 % travel/draw ratio, travels of 256 mm and 184 mm, 823 pen cycles, and 101 zero-radius point dots.

## Biggest weakness
The input mass is the loudest thing on the sheet and its closed outline reads as a heart floating inside the margins. So the plate's dominant form is an accidental figure, and it leaves a dead 145×120 mm quadrant behind it. The convolution (head plus wake) ends up as a detail on the edge of a heart.

## Mandates
1. **Break the closed heart outline by cropping the contour mass at the frame.** Scale or shift X so the unswept contour mass bleeds off the TOP and RIGHT drawable margins. No outer contour should close anywhere on the sheet, and no empty region larger than 80×80 mm should remain in the lower-right. Re-seat the title on the mass's bottom edge and the legend beside it, on one shared left axis (same x to within 0.5 mm). Test: at thumbnail size, nobody can say "heart".
2. **Make the kernel head a lifted plane, not a double outline.** Replace the 1.5 mm hairline offset with a shadow band at least 3 mm wide, filled with 45° hatch at about 0.9 mm pitch on the right and bottom sides only. Also draw the head's own keyline in 3 passes so it is the fattest line on the sheet (Pop canon: outlines dominate). Test: in a 1 m view the head reads as a card above the lattice, and the contour and dot marks stop at the band's outer edge.
3. **Clean the head for the pen and fix the layer order.** (a) Leave at least 0.6 mm of bare paper between every collar's inner edge and its black dot. (b) Collar pass pitch must be at least the stated nib width, with the nib stated in HANDOFF. (c) Stream crimson, then blue, then black, or state in HANDOFF why black goes first. (d) Remove the sheet-crossing travels by drawing the legend swatches last within each pen layer, in spatial order. Test: in the head crop every tap shows a paper ring between collar and dot, and the max travel between consecutive strokes is under 120 mm.

Polish (not mandates): fatten the diagonals of both N's to the vertical stroke weight, and delete the wobbly contour crumb in the first step pocket (x≈50, y≈182).

## Follow-up on open mandates
(Written after pass 1. Scores above unchanged. Compare-to: r03 `gallery/studio/convolutions/current/pp_convolutions_sliding-window_v10.png` and the r01 benchmark. There is no FEEDBACK.md, so there are no J* mandates.)

| id | status | evidence |
|---|---|---|
| A1 | FIXED | The triptych has collapsed. Every response ring sits on the X lattice at its own input node. The separate output map, the staircase copy and the leader lines are all gone. |
| A9 | FIXED as worded, not effective | The 1.5 mm shadow keyline is on the right and bottom edges, and the contour lines stop at it. The dotted leashes are deleted. The remaining hollow rings now carry a stated meaning (x=0 with y≠0). But the shadow reads as a doubled keyline, not a plane (pass-1 dim 7 = 5). Superseded by mandate 2 above. |
| A10 | FIXED | The r03 zipper in the lower lobe is gone, because that lobe is now swept dots. The upper-lobe hairpin slit is now an open almond with clean pointed tips. The 45° stretch holds about 1.07 mm pitch, and the crown valley is continuous. Residue: one wobbly 3 mm crumb in the first step pocket (x≈50, y≈182), plus faint kinks along the crown's medial crease (x≈100–105, y≈150). |
| A11 | FIXED (process) / lineage weak | HANDOFF now has both `lineage:` and `canon:` lines. The Vega claim is surface-borrowed, though: the lattice is never displaced, only the dot size changes. |
| A12 | PARTIAL | The `I` gaps are now even ("LUTIONS" reads as one word). Both N diagonals are hairlines against fat stems, so the weight still breaks on N. |
| A13 | NOT FIXED | Travel is 5.6 m against 11.1 m of drawing (50.6 %; r03 was 49 %). There is a new 256 mm sheet-crossing travel in the blue layer (legend swatch). Folded into mandate 3. |

## Regressions vs compare-to
- **Figuration (vs r03): new.** In r03 the X silhouette had a third, lower lobe, so it read as a trefoil. Sweeping that lobe into dots leaves the unswept remainder as a clean tilted HEART with an almond eye. The accidental object is now the plate's dominant form.
- **Sheet balance (vs r03).** r03's output map counterweighted the right half. Collapsing it (correctly, per A1) left the lower-right 145×120 mm empty, and the composition was not re-set to answer that. Negative space went from occupied to leftover.
- **Kernel tap craft (vs r03): new knot risk.** r03 taps were clean single discs. r04 adds a black dot inside every collar with only 0.44 mm clearance, the collar is 7 passes at 0.27 mm pitch, and the black layer streams first. In the preview the collar already fuses into the dot.
- **Title presence (vs r03).** The title shrank from about 93 mm wide to about 80 mm, and it now sits 9 mm off the right edge against 14 mm of clearance on the left.

DESCRIPTION.md § Keep (r01 benchmark):
- One axis ties three zones: **no longer true.** The layout was retired by A1/A3, which is accepted, but nothing replaced its structural axis. The legend and title miss a shared left edge by 2 mm.
- Equal gutters by construction: **no longer true** (same layout retirement).
- 14 mm gutter treated as a zone: **no longer true.** The one large empty zone is now leftover, not built.
- Depth by clipping, not collision: **HELD.** Rings stop on the staircase risers and at the head's shadow edge, and no overlap is accidental.
- Contour discipline (continuous rings, min gap ≥ 0.86 mm): **HELD.** Pitch is 1.02–1.07 mm, apart from the one step-pocket crumb.
- Colour as a sequence: **no longer true.** Colour now means sign, which is a defensible change of meaning, but the sequential colour movement is gone.
- Two blobs as bookends: **no longer true** (deliberately removed by A1).
- Receptive-field cone: **no longer true** (removed, and nothing carries receptive-field growth now).
