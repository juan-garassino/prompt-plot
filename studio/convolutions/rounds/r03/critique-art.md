# Art critique — convolutions r03 · canon: UNDECLARED (HANDOFF names no canon and no `lineage:` line; judged against the rubric + the reference as interpretation) · 2026-09-28
render: gallery/studio/convolutions/current/pp_convolutions_sliding-window_v10.png

## Scores

| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 7 | The contour mass X (≈150×165 mm) clearly dominates. The output lattice Y comes second, the kernel third, and the title reads at 1 m. The mass-to-lattice area ratio is below 3:1, so Y competes a little. |
| 2 | grid & alignment | 5 | No axis is shared between zones. The X sample pitch is ≈6.5 mm and the Y pitch ≈8.5 mm, so the corridor and the Y staircase do not rhyme. The X staircase step is ≈13 mm and the Y step ≈8.5 mm. The title's left edge (x≈190) and the lattice's left column (x≈195) nearly line up but do not. The title baseline sits 3 mm above the drawable edge while every other element keeps ≥10 mm. |
| 3 | tension & asymmetry | 7 | A real working diagonal runs through both X and Y, and the three masses are placed off-centre. The parent's bilateral symmetry is gone. |
| 4 | negative space | 6 | The bottom-right quiet zone (x 150–280, y 20–95) is shaped, but two dotted leashes run through it and end on nothing. The Y-window leash runs to (285, 95), about 2 mm from the drawable edge, which reads as crowding. The gap between the mass and the lattice (x 150–190) is leftover space. |
| 5 | craft for pen | 6 | Measured perpendicular ring pitch is 0.88–1.0 mm on the lower lobe (y=60). In the upper-right lobe (y≈150) the rings run at 45° and the true pitch is ≈0.6–0.8 mm at the floor. The lower lobe's medial axis (x 90–95, y 20–60) is a zipper of staggered dead-ends, one on every ring. The upper lobe has a lens slit of hairpins at (115–135, 125–140). The title's multi-pass strokes separate visibly in the N stem, and the gaps around the I glyphs are too wide ("LUT IONS"). Travel is 7.0 m against 14.2 m of draw (49%), from ≈300 tiny dots and rings. Three pens, which is good. |
| 6 | concept legibility | 4 | This is the conv-arithmetic triptych: input grid, kernel, output grid, a staircase of window positions, and leader lines between them. It has no labels, but it is still the textbook figure, and the dotted leashes act as its arrows. The mass silhouette reads as a heart or butterfly with fingerprint whorls, which is a nameable object. The link from the X corridor to the Y staircase is never drawn: the kernel's leash ends near the title and Y's leash ends at the frame. |
| 7 | depth & dimensionality | 4 | Flat, and the flatness is not declared in HANDOFF. The only depth cues are the corridor cut out of the mass and the kernel box clipping the lower lobe. Nothing reads as a plane lying over another plane. |

**avg 5.57 · min 4 · VERDICT: FAIL**

## Reads at a glance
From 3 m: a black fingerprint heart with a stepped staircase of dots cut through it, a red and blue dotted box at its foot, and a separate red and blue target grid top-right. In other words, "input, kernel, output" drawn as three separate things.

## Acceptance checks
No `encoding.md` or `BRIEF.md` exists for this slug, so there are no §11 checks. LINEAGE rule: **FAIL**, because HANDOFF has no `lineage:` line.
AUTHORING §6, with the reference in play:
1. Main forms recognisable without colour: **PASS**. The mass, lattice and kernel all read in black alone.
2. Shadow lines follow the surface: **PASS with fault**. The rings follow the mass, but the lower-lobe medial seam is a mechanical stagger, not a surface.
3. Fine lines that are really two sides of one thick stroke: **FAIL (minor)**. The title's multi-pass strokes fan apart; the N stem reads as two lines.
4. Blackest regions intended: **FAIL**. The ring field at ≈1 mm pitch with ≈0.55 mm ink is intended. The hairpin knots in the upper-lobe slit and the lower-lobe zipper are not.
5. Labels readable at actual pen width: **PASS**. The title is the only label and it is readable.
6. Thicker pen makes knots at corners or fills highlights: **FAIL**. The clipped ring ends at the staircase corners leave hooks (e.g. near (93, 130)), and the seam hairpins will fill in with a 0.5 mm nib.
7. Long empty travels or tiny marks with no benefit: **FAIL**. Travel is 49% of draw. There are about 150 black sample dots, 130 output rings, and 2 hollow circles on the kernel leash plus 2 hollow circles in X that carry no stated meaning.
As an interpretation of the reference: it keeps X, K and Y and drops the reference's decoration, which is a fair reduction. But it keeps the reference's worst trait, the three-station pipeline.

## Biggest weakness
The plate is still the textbook convolution figure (input grid, kernel box, output grid, window staircase, leader lines). The sliding-window idea only survives as parallel staircases, and nothing on the sheet connects them. The mechanism "the response lands where the window sat" is split across 150 mm of paper and never closed.

## Mandates
1. **Collapse the triptych: put each response where it is computed.** Along the X corridor, draw each crimson/blue response ring on the exact X lattice node where the kernel window sat (ring count = |response|, pen = sign), replacing the black sample dot at that node. Delete the separate 11×12 right-hand lattice and its staircase, or at most keep it as an uninked quiet zone for the title. Test: every coloured ring on the sheet sits on an X lattice node inside the stepped corridor, and no output grid stands apart.
2. **Close the medial seams of the contour mass.** On the lower lobe (x 90–95, y 20–60) and the upper-lobe lens slit (x 115–135, y 125–140), the rings must either run continuously through the core or all end on one clean medial line. No staggered dead-ends, no hairpin shorter than 2 mm. Perpendicular pitch must be ≥1.0 mm everywhere, including the 45° stretch of the upper-right lobe at y≈150. Test: at 3× zoom neither location shows a zipper, and a pitch probe normal to the rings reads ≥1.0 mm.
3. **Make the window a plane lying on the field, and declare it.** Draw a second parallel keyline 1.5 mm off the right and bottom edges of every corridor step and of the kernel box. The contour rings must stop at that shadow line, not at the window edge, so the corridor reads as a raised sheet over the thumbprint. Also delete both dotted leashes (the one to (170, 18) with its two hollow circles, and the one to (285, 95) at the frame). Test: at 1 m the corridor reads as lying on top of the mass, and no dotted line ends on empty paper.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | `studio/convolutions/LEDGER.md` and `FEEDBACK.md` do not exist. There are no open A*/J* mandates and no prior critique-art in r01/r02. |
| DESCRIPTION "sliding-window" plan | PARTIAL | Done: the diagonal path, no labels except the title, and responses as nested ring counts. Not done: the plan said "no boxes" (the kernel box and window boxes remain), responses were to stay at the stamps (they moved to a separate lattice), and stride/overlap as visible spacings (the stamp overlap cannot be read). |
| DESCRIPTION Weak: decoration (dots, brackets, plus marks) | FIXED | All removed. The only leftovers are the 4 hollow circles, which carry no meaning. |
| DESCRIPTION Weak: bilateral symmetry | FIXED | Mass left, lattice top-right, title bottom-right, with a working diagonal. |
| DESCRIPTION Weak: hairline title does not dominate | FIXED | The title is now display-weight, about 12 mm cap height. |
| DESCRIPTION Weak: undeclared flatness | NOT FIXED | Still flat and still undeclared. |
| DESCRIPTION Weak: pipeline schematic | NOT FIXED | Reduced from five stations to three, but still input → kernel → output. |

## Regressions vs compare-to (gallery/.../pp_convolutions_v1.png)
- **Contour continuity regressed.** v1's rings were continuous to the medial axis (Keep: "rings stay continuous, the dominant texture"). r03 has a staggered zipper seam on the lower lobe and a hairpin slit on the upper lobe.
- **Structural grid lost.** Keep "one axis ties three zones" and Keep "gutters equal by construction" no longer hold: no element shares an axis, and the two lattice pitches disagree.
- **Keep "two blobs as bookends"** is gone by design. Its input/output rhyme was not replaced: Y is a separate lattice with no visual rhyme to X.
- **Keep "colour as a sequence"** was replaced by colour-as-sign. That is defensible as data, but the left→right colour travel is lost.
- **Keep "receptive-field cone"** is gone. It was the only non-schematic element of v1.
- **Keep "depth by clipping, not collision"**: PARTIAL. The corridor cutaway and the kernel-box clip remain, but with no shadow they read as holes, not layers.
- Improvements, for balance: travel 13.0 → 7.0 m, commands 125.7k → 48.5k, pens 4 → 3, symmetry broken, decoration gone.
