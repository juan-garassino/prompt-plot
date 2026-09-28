# Art critique — convolutions r02 · canon: UNASSIGNED (HANDOFF names no canon, no `lineage:` line) · 2026-09-28
render: ~/Downloads/pp_convolutions_real-kernel_v9.png  (gcode alongside; a4 landscape, cream; 4 pens)

No encoding.md or BRIEF.md exists for this slug, and HANDOFF declares no canon or lineage (the
rubric's LINEAGE rule requires a `lineage:` line). Judged against the generic rubric plus the
reference as an interpretation brief. Missing canon is itself a finding: nothing here commits to a
movement, so the plate defaults to technical-drawing hairline, which is what the rubric warns against.

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 5 | X (~75 mm) and Y (~70 mm) are the same size and weight, and they bracket a row of five equal tiles. Nothing is 3:1 over anything else. At 3 m you see "two blobs with a row of boxes between them". |
| 2 | grid & alignment | 6 | Left column holds (title, X, bank all start at x=13). Right edge holds (stride block and feature maps end at x=284). The top band and the bottom row are both centred on x=148. The bottom row is three modules evenly spread at left, centre and right, and the bank's baseline sits ~2 mm off the feature-maps baseline. |
| 3 | tension & asymmetry | 4 | A mirror plate. There is a dashed vertical axis at x=148, the receptive cone is centred on it, K*X sits on it, X is mirrored by Y, and the bank is mirrored by the feature maps. The only diagonals are the fan curves, and they are symmetric too. |
| 4 | negative space | 5 | The middle belt (y≈85–100, and x 60–130 / 170–240 down to the bottom row) is leftover, not shaped. It is what remains between a band and a footnote row. No zone is silent on purpose, and the dense zone (X) is not made louder by anything. |
| 5 | craft for pen | 6 | 4 pens, each with a stated meaning. Bounds are clean (13–284 × 20–195). X rings are continuous at ~1.5 mm. Failures: the **olive fan converges 7 lines onto one node at (258,126)**, an ink knot (the spacing scan puts the pen-3 hotspot exactly there). The receptive-cone apex (148,84) knots the same way. The **Y stem holds contour crumbs**, broken 3–6 mm fragments inside the stem at x≈272–280, y≈110–130: this is the "flood thinned into crumbs" failure. The highlighted bank tiles use a **double frame at 0.55 mm offset**, under the 0.8 mm floor, so on paper it will merge into one fat smudged line. The stroke font collides on the tile labels, with "blur" letters overlapping and "ridge" reading "r dge". Travel is 6.97 m against 10.06 m of draw, which is heavy. |
| 6 | concept legibility | 3 | **Schematic.** Input blob → five framed boxes joined by connector bars → output blob, plus a labelled kernel bank, a stepped pyramid annotated 5/9/13/17/21, and three captioned feature-map panels. This is a textbook CNN figure with nicer inking. The abstract order (laminar band?) does not read. The row reads as boxes-and-links. The one witty idea, X's trefoil morphing into a letter-Y through the per-layer thumbnails, is buried at thumbnail scale under the boxes. |
| 7 | depth & dimensionality | 4 | Flat and undeclared. The cone gives a faint perspective, and dashed vs solid rings give a hint of layering. Nothing overlaps or occludes anything else. |

avg **4.71** · min **3** · **VERDICT: FAIL**

## Reads at a glance
From 3 m a stranger sees a symmetric left-to-right pipeline diagram: a black blob, five dotted boxes and an olive "Y", with a kernel grid, a pyramid and three small panels beneath. They would call it a slide, not a print.

## Acceptance checks
No encoding §11 exists (no encoding.md, no BRIEF.md), so there are none to run. AUTHORING §6 against `studio/convolutions/ref/reference.png`:

| # | question | result | evidence |
|---|---|---|---|
| 1 | main forms recognisable without colour | PASS | X trefoil, tile row, cone and bank all read in monochrome. |
| 2 | shadow lines follow the surface | PASS (n/a) | No shading. X and Y rings follow their outlines. |
| 3 | fine lines really two sides of one thick stroke | PASS | The per-layer thumbnails are deliberate double rings, not traced edges. |
| 4 | blackest regions intended | FAIL | X is intended. The olive fan node (258,126), the cone apex (148,84) and the Y-stem crumbs are accidental congestion. |
| 5 | labels readable at true pen width | FAIL | "blur" and "ridge" above the tiles have overlapping glyphs, and "continuous" / "perception" / "receptive" have a collapsed `i`. At a 0.5 mm nib the tile labels close up. |
| 6 | thicker pen knots corners / fills highlights | FAIL | The 0.55 mm double frames on three bank tiles will merge. 7-way fan convergence. |
| 7 | long empty travels / tiny marks with no benefit | PARTIAL | 6.97 m of travel is 69% of the draw length. The receptive-cone dot rows (≈1 mm dots at the outer rim) are near-invisible marks. |

Interpretation vs reference: the reference is also a diagram, but its tiles are **fields**: flow-textured squares with a starburst node, joined by orbit arcs and construction curves, sitting in a sea of construction geometry. r02 has stripped the field texture and the orbit geometry and kept exactly the part of the reference that is schematic: boxes, captions and a pyramid. The interpretation moved toward the figure, not away from it.

## Biggest weakness
It is a schematic. Framed boxes joined by connector bars, captioned panels and an annotated pyramid are the apparatus of a CNN, not what convolution does. The mirror composition along x=148 then removes the only other thing that could have carried it.

## Mandates
1. **Delete the apparatus in the top band.** Remove all five rectangular tile frames and the olive connector bars between them (currently at x≈103–108, 130–135, 156–161 and 183–188, three bars per gap). Instead, run ONE continuous field band from X to Y and stamp each kernel's crimson/blue dot lattice directly ON that band as a sliding-window footprint, so the band's ring pattern visibly changes on the far side of each footprint (blurred rings widen, ridge rings sharpen). Test: the top band contains no closed rectangle and no straight link bar, and the reader sees the field change under each stamp.
2. **Break the mirror and set a 3:1 hierarchy.** Delete the dashed vertical axis at x=148. Enlarge the X field to ≥120 mm tall, cropped by the left margin. Shrink Y to ≤⅓ of X's area. Move the receptive cone off-centre so its apex sits on X's kernel patch (currently at ≈(70,130)) and it opens downward-left into the bank. Test: no element is centred on x=148, X is the single largest mass, and the bottom row is no longer three evenly spaced modules.
3. **Pen-craft pass.** (a) Stop every fan line ≥1.0 mm short of the olive node at (258,126) and of the cone apex at (148,84), or replace each node with a ring the lines touch tangentially. (b) Remove the contour crumbs in the Y stem (x≈272–280, y≈110–130): every ring either closes or is dropped. (c) Make the highlighted bank tiles' double frame ≥1.0 mm apart, or a single line at 2 passes. (d) Fix the stroke-font advance so "ridge", "blur", "continuous", "perception" and "receptive" have no touching glyphs at 3× zoom. Test: zoom any of these at 3× and see no merged strokes.

## Follow-up on open mandates
No `LEDGER.md` and no `FEEDBACK.md` exist for this slug, so there are no A*/J* ids. The open asks are DESCRIPTION.md § Next versions → `real-kernel` (the variant this round claims) and the three "If only iterating" items. They are tracked here as D1–D3 plus RK.

| id | status | evidence |
|---|---|---|
| RK tiles = signed Ben-Day kernels | FIXED | The five tiles and all nine bank cells are 5×5 disc lattices, radius ∝ \|w\|, crimson/blue by sign. They read as weights. |
| RK feature maps = true K∗X contours | PARTIAL | The edge/blur/gabor panels now visibly derive from the X trefoil (blur = nested trefoil, edge/gabor = signed lobes), so they are caused by the left of the sheet. But the per-layer thumbnails end in a letter-Y that X's rings do not produce, and three different vocabularies are in play (tile labels blur/ridge, map labels edge/blur/gabor, an unlabelled bank). |
| RK "same layout, same spine, same gutters" | PARTIAL | Gutters and baselines are kept. The spine is now broken: it runs y 200→155, drops out through the strip, and resumes y 100→85. It no longer ties the band to the cone. |
| D1 tiles: no muddy starbursts | FIXED | The rays are gone and each tile reads cleanly at 1 m. |
| D2 delete scatter dots + brackets, move stride block | PARTIAL | All ~30 dots, the quarter-brackets, the plus marks and the hollow square are gone. The stride block still sits in the top-right corner (x 263–284, y≈195) flush with the right margin. It is legible now, but the preview legend covers its first line, so check it on paper. |
| D3 no `>` pointer at K; drop 2nd spine | FIXED | The ellipses are gone entirely, which removes the pointer. The u≈0.845 spine is gone. |

## Regressions vs compare-to
Parent `gallery/studio/convolutions/current/pp_convolutions_v1.png`: r02 is cleaner, but it is **more** schematic than the benchmark, not less.
- **Receptive-field cone REGRESSED.** The Keep item ("mostly white paper inside a dashed envelope, teardrops closing at the mouth, the one lower element that reads at 1 m") has become a stepped dot-pyramid with 5/9/13/17/21 tick labels. That is a textbook receptive-field diagram, and it lost the nested-teardrop form, which was the plate's best abstract shape.
- **Depth-by-clipping REGRESSED.** Both defended overlaps from Keep are gone: the dashed ellipses passing behind the strip, and the connectors vanishing behind each tile and reappearing in the gaps. r02 has zero occlusion, which is why dimension 7 dropped to 4.
- **Contour discipline REGRESSED.** v1 measured ≥0.86 mm everywhere. r02 has crumbs in the Y stem, a 0.55 mm double frame on three bank tiles, and a 7-way ink knot at the olive fan node. None of these existed in v1.
- **Bookend rhyme weakened.** v1's X and Y were matching trefoils (input/output rhyme). Y is now a letter "Y". It is a cute pun, but it turns the output into a glyph/object and breaks the rhyme Keep praised.
- **Captions added.** "blur/ridge/blur/ridge/blur" over the tiles adds five more labels to a plate already criticised as a captioned schematic, and they are the worst-set type on the sheet.
- **Colour-as-sequence changed meaning.** The crimson→black→blue→olive→crimson travel became a sign code (crimson/blue). That is defensible because it now carries data, but the left→right colour transformation from Keep is gone except in the X-black / Y-olive endpoints.
- Kept: title block, the left x=13 edge, the right x=284 edge, the shared lower baseline and caption line, the empty gutter band, X ring continuity (with one small triangle crumb at ≈(38,142)).

Keep audit (DESCRIPTION § Keep): one axis ties three zones → **no longer true** (spine broken) · gutters equal by construction → true · 14 mm empty gutter → true · depth by clipping → **no longer true** · contour discipline → **no longer true** (Y stem, 0.55 mm frame) · colour as a sequence → partly (endpoints only) · two blobs as bookends → **weakened** (Y is a letter) · receptive-field cone → **no longer true**.
