# Art critique — convolutions r05 · canon: Pop / Ben-Day (Lichtenstein, Modern Painting) · 2026-09-29
render: gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.png  (gcode measured: gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.gcode)

No `encoding.md` or `BRIEF.md` exists for this slug. The HANDOFF `rule:` line was used as the spec.

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | At 3 m the black stripe wing (top right) dominates, and the fused 1.05 mm card keyline comes second. But the wing is the UNREAD part of X, and it carries about 93 % of the ink (15.9 m black against 0.5 m crimson and 0.7 m blue). The output Y, which is the point of the plate, is hairline rings and ranks third to fourth. The hierarchy is the wrong way round for the concept. |
| 2 | grid & alignment | 7 | The lattice is strict, the card sits on lattice nodes, and the title and top key icon share x = 201.0 / 201.2. Problems: the last staircase riser (x 197.6) runs down to y 17, 3.4 mm from the title's left edge and 3 mm below its baseline. Key and title baselines float free of the 7.2 mm row pitch. |
| 3 | tension & asymmetry | 8 | A strong lower-left to upper-right diagonal: the wavefront staircase, the wing bleeding off the top and right crop, and the card off-centre on the fork. This is the plate's best quality. |
| 4 | negative space | 6 | The one generous quiet zone (lower right, ahead of the wavefront) is filled with an 8-line key plus the title. The lower-left x = 0 corner looks like residue, with straggler empty crimson rings at (35,180), (150,64), (136,35) and (78,35). Stripes pass 1–1.5 mm from the card's shadow hatch on its right side, which reads as squeezed rather than as occlusion. |
| 5 | craft for pen | 7 | Stripe pitch is 1.07–1.19 mm everywhere (≥ 0.8). The fused keylines are intended. 3 pens, one swap each. Defects: the fold crease at about (228,183) joins two pitch families (1.07 against 1.40 mm) in a white lens whose tips touch at 0.07 mm, and there is a 0.02 mm tip contact at (150,143). Head collars are partial arcs, and Pop regularity makes them read as broken circles. Collar-to-dot bare paper is 0.53–0.59 mm. |
| 6 | concept legibility | 6 | Not a schematic. The order (a lattice with a travelling scan front) is abstract and reads: "a window has swept part of a field, leaving targets behind". But X as ONE shape does not read. The read side is a blob of near-uniform dots, and the unread side is a separately outlined wing. The key's second paragraph has to explain what the colours mean. |
| 7 | depth & dimensionality | 7 | Declared flat (Pop) with one lifted plane. The hatched 3.2 mm shadow now reads as a card, not a registration double. Against that, the stripes seem to bend around the card near (128–140, 97–140), as if the card were in the field's plane rather than lifted above it. |

**avg 6.71 · min 6 · VERDICT: FAIL**

## Reads at a glance
A black striped wing sweeps up and off the top-right corner above a dotted lattice stamped with red and blue targets. A heavy black square sits on the seam, and a staircase divides the sheet into done and not-yet-done.

## Acceptance checks
Encoding §11: none (no encoding.md). The HANDOFF `rule:` claims were checked against the gcode:
- lattice top/right edges on the crop line (y 197, x 284): PASS
- layer order crimson → dodgerblue → black: PASS
- card keyline is the fattest line on the sheet (1.05 mm fused): PASS
- staircase "top edge to bottom edge": PARTIAL. It starts at y 197 but ends at y 17, below the lattice's last row (≈ y 24), and dangles beside the title.

Lineage (Lichtenstein, *Modern Painting*): the vocabulary is honestly mapped. Dots are samples, stripes are the unread field, the keyline is the card. It would not hold beside the work yet. In Lichtenstein the keyline is everywhere and the stripes are rigid parallels. Here only the card has a keyline, and the stripes are curved, creased distance contours (closer to Riley than to Lichtenstein).

AUTHORING §6 (reference as interpretation). The plate is now a free transposition of the reference; only the X thumbprint survives as the stripe field.
1. Main forms recognisable without colour: PARTIAL. The card, staircase and wing are clear; the Y letter is not.
2. Shadow lines follow the surface: PASS. There is one 45° hatch, on the card only.
3. Fine lines that are two sides of one thick stroke: PASS. The fused keylines are 0.25–0.30 mm apart and read as one line.
4. Blackest regions intended: PASS in the wing body. FAIL at the fold lens (two families meet at 0.07 mm).
5. Labels readable at pen width: PASS.
6. Thick pen knots or filled highlights: PASS. Collars leave 0.53–0.59 mm of paper.
7. Long empty travels or excess tiny marks: FAIL. Crimson travels 142 mm, blue 177 mm and 128 mm (legend swatches drawn mid-layer).

## Biggest weakness
X is not one figure. The read part (a dot blob without an outline) and the unread part (a heavy outlined stripe wing) look like two different objects glued at the staircase. The wing, which carries the least meaning, is the loudest mass on the sheet, while the response Y is hairline. A viewer sees "a wing and a dot grid", not "one image half-converted by a sweeping window". Secondary: the stripe crease at (228,183) and the riser dangling beside the title read as accidents.

## Mandates
1. **One X, one keyline.** Draw the Y capsule's outer boundary (the x = 0 contour) as ONE continuous black keyline at the wing outline's weight (2 passes). It should wrap the read side too: around the left arm (x ≈ 20–60, y ≈ 130–185) and down both sides of the stem to its foot (≈ 108, 24), and meet the wing's outline at the staircase with no break. Test: on a 25 % thumbnail you can trace one Y letter from the stem foot to the top-left arm tip and out the top-right wing, and no black contour ends at a staircase riser.
2. **The output outranks the input.** Every response with ≥ 3 rings draws its outermost ring in 2 passes (about 0.6 mm), at nodes such as (108,64), (108,78), (108,93), (50,150) and (78,136). The blue stem column and the left-arm targets must then read at 3 m as the second-loudest element after the card, above the dot lattice. Test: at 25 % thumbnail the blue skeleton of the Y is visible as a chain of targets; today it disappears into the dots.
3. **Close the riser before the title.** End the last staircase riser at the lattice's bottom row (y ≈ 24.2), not y 17. Put the title baseline and each key block's baseline on lattice row y-values (7.2 mm pitch) so type shares the grid the dots define. Keep ≥ 7.2 mm between the riser and the title's left edge. Test: no black line runs past the lowest dot row, and the title baseline y equals a lattice row y within 0.3 mm.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A12 | FIXED | Both N diagonals now match the stem weight (title crop). |
| A16 | PARTIAL | The heart is gone: the wing bleeds off the top (y 197) and right (x 284) crop, and no outer contour closes. Title and key share the left axis (201.0 against 201.2 mm). But the empty lower-left (x 10–60, y 10–60) remains, and the lower-right quiet zone is now filled by the key instead of being shaped. |
| A17 | FIXED | Shadow band 3.2 mm, 45° hatch, right and bottom only. Keyline 4 passes fused to 1.05 mm, the fattest line on the sheet. It reads as a card at 1 m. Residue: stripes near the card's right edge look deflected rather than occluded. |
| A18 | PARTIAL | Arcs whose sweep is proportional to \|w\| are in (corner taps are visibly longer arcs than diagonals). Bare paper between collar and dot is 0.53–0.59 mm on all measured taps, short of the ≥ 0.6 mm asked. |
| A19 | PARTIAL | Order crimson → blue → black: FIXED. Travel < 120 mm: NOT FIXED. Crimson 142 mm (38,179)→(95,49), blue 177 mm (52,165)→(204,73) and 128 mm (207,40)→(79,42). Legend swatches are drawn mid-layer, not last. |
| A20 | FIXED (process) | The lineage was re-declared as Lichtenstein / Ben-Day, and dots, stripes and keyline each carry data. As a look it is only half-earned (see Acceptance). |
| S8 | observed: text present | All three wordings are on the sheet (sign line, \|y\| < max\|y\|/8, smallest dot x < 7 %). Science critic to adjudicate. |
| S9 | unchanged (declared) | The card still hides outputs (4,5), (5,5), (4,6). The HANDOFF says so. |

## Regressions vs compare-to
- **The Y skeleton is less legible than in r04.** In r04 the narrow stem column (x 73–133) with four large blue targets on x = 103 read as a stem. In r05 the read region is a fatter blob (x 20–145), so the stem targets are surrounded by dots and the letter is lost.
- **Ink balance has swung to the wing.** Black went from part of 11.1 m total in r04 to 15.9 m in r05, nearly all of it stripes. r04's rings were an open nest with air between families; r05's wing is a near-solid tone mass that outweighs the card.
- **New crease defect.** r04 had one clean lens in its crown. r05's lens at (228,183) joins two unequal pitch families (1.07 against 1.40 mm) with 0.07 mm tip contact, which reads as a tear.
- **Head colour lost its Pop mass.** r04's solid crimson and blue collars made the head the one colour-dense zone. r05's thin partial arcs make the card a black box with faint colour inside. This was a consequence of A18 (true to \|w\|), but the colour weight must come back elsewhere (mandate 2).
- **New graze:** the staircase riser now runs down beside the title (3.4 mm gap, 3 mm past the baseline).
- DESCRIPTION § Keep (r01): contour discipline (min gap ≥ 0.86) is still true across the wing body but broken at two tip contacts (0.07 and 0.02 mm). Depth by clipping still holds, in new form, through the card occluding the lattice. The single axis u = 0.50, the equal gutters, the 14 mm gutter, the two-blob bookends, the colour sequence and the cone were all deliberately retired by the r03/r04 re-layout, so they are not counted as regressions.
