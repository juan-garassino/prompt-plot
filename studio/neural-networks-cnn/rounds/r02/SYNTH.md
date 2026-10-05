# Synth — neural-networks-cnn after r01 + r02 (parallel theses) · 2026-09-28
route: designer
next round: r03 · parent: r02 (best so far). Both rounds FAIL; r02 wins on art min (4 against 3) and on art avg (5.86 against 5.29), with science min tied at 5. r01 stays on disk as the `pooling-cascade` flavour. This is not a merge: the only thing r03 takes from r01 is a practice, verifying the receptive field numerically as r01's `net.py` did.

## The instruction
Keep r02's single MobileNetV2 forward pass (`maps.npz`, argmax unit (4,3), the four 50 % ERF contours) and its bottom-left → top-right diagonal. Redraw all five maps in ONE mark, the Schotter rule. Every layer is only continuous horizontal hidden-line profile rows, drawn against that layer's own z-buffer: no column lines, no cross-mesh, no vertical ticks. One row per map row, stride-thinned only where the paper pitch would fall under 1.0 mm. Row count and pitch then show resolution by themselves (224 → 56 → 28 → 14 → 7), with roughness as the only other variable. Delete the dashed crimson rails entirely. The funnel reads from the loops shrinking toward the summit, not from apparatus between planes. Crimson is then exactly: one closed, occluded ERF loop per lower layer, plus closed summit isolines drawn wholly in crimson inside cell (4,3). Black rows pen-up at the cap boundary, never switching pen mid-polyline. Rebuild the top CAM plane on the same projection basis as the lower four. Make it no wider than the 14² plane (≤ 102.4 mm) and place it wholly inside the frame, so the stack shrinks monotonically and no data is cut. Replace the caption with at most three flush-left lines on the title axis:
- the per-layer resolutions as numerals
- the crimson key "50 % OF ∂CAM(4,3) GRADIENT MASS · ≈27 % OF IMAGE vs CELL 1/49"
- "CAM − MEAN, CLIPPED AT 0 · P(TIGER CAT) = 0.43"

## Mandates to close
1. **A2**: one mark grammar. Horizontal hidden-line profile rows only. Row pitch ≥ 1.0 mm, no run under 3 mm, total commands under 12,000. Test: zoom any layer and you find only continuous horizontal profiles.
2. **A1 + A3**: no schematic apparatus and scarce, closed crimson. Delete the rails. One closed, occluded ERF loop per lower layer (blocks 5 and 12 included, unbroken). Summit isolines wholly crimson. No polyline changes pen. Nothing crimson between layers. (A1 has been NOT FIXED in both r01 and r02. A third miss routes to translator.)
3. **S1**: top CAM plane unclipped, on the shared basis, width ≤ 102.4 mm. Plane widths are monotone 152 → 131 → 114 → 102 → ≤ 102. No polyline may end on x = 200.000.
4. **S2**: resolutions as data numerals (not names), the crimson key, and the ERF ≈ 27 % against cell ≈ 2 % contrast, all in the ≤ 3-line caption.
5. **S3**: disclose ReLU(CAM − mean) on the sheet, or draw min-offset raw CAM instead. The designer chooses and says why in NOTES.

Deferred (in the ledger): A5 rhythm (re-solve gaps after A2 changes the silhouettes, see Do not), A6 frame (see Do not), A11 title double-stroke craft (r04), S7 preprocessing word, S6 dossier (process). A12 cream is argued as tooling: file an engine request for a `--paper-color` flag on `render_candidate.py` / `preview`.

## Preserve
- **The real computation** (r02, whole sheet): one forward pass, argmax (4,3) on the cat's muzzle, ERF centres and radii within 3 mm of the science critic's recompute. Do not re-run with a different image or preprocessing.
- **The diagonal** (r02): raster at the bottom-left, summit at the top-right, title block top-left as counterweight, and the empty wedge under the title (x 10–70, y 60–225) shaped by the stagger.
- **The morphology gradient** (DESCRIPTION Keep; r02 made it data): busy input at the foot, one smooth peak at the head.
- **The crimson summit as the one loud accent** (DESCRIPTION Keep): top-right, about 35 × 45 mm, first read at 3 m.
- **PIXELS without flood** (r02, y 15–55): no rows under 1.0 mm.
- **Hidden-line solidity** (r00 Keep, regressed in r02 as A4): near ridges hide far rows on every layer, including the top terrain at x 115–150, y 200–222. Profile rows drawn against the z-buffer should close this. Say so in NOTES with a measurement.

## Do not
- Do not keep the column lines "just on the top plane". One grammar means every plane.
- Do not replace the rails with any other connector (dotted lines, arrows, drop-lines, shaded cones). The loops carry the funnel alone.
- Do not crop any data map at the frame to fake tension. Science forbids truncation (S1). Keep every edge ≥ 5 mm inside the margin.
- Do not put the title's cap top within 6 mm of the top margin (r02's `FROM` touched y = 287).
- Do not let the inter-layer gaps fall out of a formula again (12 / 10 / 4 / 4). Choose equal gaps (≥ 10 mm) or a declared monotone progression, and state it.
- Do not name layers (PIXELS / EDGES / BLOCK_5 as words on the planes). Resolutions are numerals in the caption only.
- Do not re-grow crimson: four loops plus the summit. No crimson rings on the summit's neighbours.
- Do not hand-roll z-buffers if the engine can do it. If `Scene3D` lacks a rows-only surface, use the r02 workaround and repeat the engine request.

## Fabrication gate
Not run: neither round passed both critics.
