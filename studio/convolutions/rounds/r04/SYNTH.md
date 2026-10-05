# Synth — convolutions after r04 · 2026-09-28
route: designer
next round: r05 · parent: r04 (best so far and also the latest. It beats r03 on art min 5 > 4, sci min 7 > 5 and art avg 6.14 > 5.57)

Routing trace:
- Rule 1 does not apply: both critics FAIL, so no fabrication gate was run.
- Rule 2 does not apply. A9 was fixed as worded and is re-raised stronger as A17. A13 and S5 were explicitly deferred every round, never put in a work order. The encoding is improving fast (sci truth 6 → 8 → 9), so the encoding is not the problem.
- Rule 4 does not apply: best-so-far moved r03 → r04. Even so, the instruction below is a composition move, because the art critic's biggest weakness is compositional.
- Rule 5 does not apply: r04 beats its parent.
- Rule 6 does not apply: r05 is designer round 4 of 5.
- MEASUREMENTS: this is a computed plate, not a trace. Every coordinate is derived (the lattice, K∗X, the distance field) and the science critic recomputed them off the gcode, so "measure the reference" is not needed.
- `promptplot/` has uncommitted edits (plot_cmd, plotjob, gallery scripts). They belong to the plot-job work, not to this piece, and no regression run is required until a gate.

## The instruction
Keep r04's single wavefront lattice and all of its arithmetic exactly. Change what the frame does to it. Scale and/or shift the X field so the UNSWEPT distance-field mass bleeds off the TOP and RIGHT drawable margins. X is a field larger than the view, so its rings run out through the frame, no outer contour ever closes, and the heart silhouette disappears.

The constraint that keeps the science true: all 66 swept windows, their dots and rings, and the head stay fully on the sheet. Only rings ahead of the front may crop. If the lattice has to shift left/down to allow this, the swept dot stem may approach the left and bottom margins, but it must not cross them.

Re-seat the reading key and the display title into what is left of the lower-right, on ONE shared left edge (±0.5 mm), with the title baseline still locked to a lattice row. Then lift the head off the lattice as a card: a ≥ 3 mm 45°-hatched shadow band on its right and bottom, and a 3-pass keyline that is the heaviest line on the sheet.

Test at thumbnail: a field being read by a card moving down-right, with the wake behind it and the field running out of the frame ahead of it. Nothing on the sheet should be nameable as an object.

## Mandates to close
1. **A16**: crop the unswept contour mass at the TOP and RIGHT frame. No closed outer contour anywhere. No empty region > 80×80 mm. Key and title on one shared left axis (±0.5 mm). Test: nobody can say "heart".
2. **A17**: the head is a lifted card.
   - Shadow band ≥ 3 mm, right and bottom only, 45° hatch at ≈0.9 mm pitch.
   - Keyline in 3 passes, the fattest line on the sheet.
   - Field marks stop at the band's outer edge.
   - Delete the 1.5 mm hairline double.
3. **S8**: the key tells the truth and states the finding.
   - (a) Add one line: `blue = where X peaks (its skeleton) · crimson = where X starts · blank = X flat` (∇²X ≈ 0).
   - (b) Change the zero wording to `no ring: |y| < max|y|/8`, or give exact zeros their own code.
   - (c) Either remove the 0.6 mm x-dot floor, or declare it in the key.
4. **A18**: head collars.
   - ≥ 0.6 mm bare paper between each collar's inner edge and its dot.
   - Pass pitch ≥ the nib, and state the nib in HANDOFF.
   - Collar ink area ∝ |w| within ±20 % on all 25 taps. A tap below one full nib ring is a single-ring ARC with sweep ∝ |w|, so the corners (≈0.08) visibly outweigh the diagonals (≈0.01–0.03).
   - Record the 25-tap area table in NOTES.
5. **A19**: stream crimson → blue → black, or justify black-first in HANDOFF. Draw legend swatches last within each pen layer. Test: max consecutive travel < 120 mm, measured in NOTES.

Deferred, do only if cheap:
- A12: fatten both N diagonals to stem weight.
- A10 residue: delete the crumb at (50,182) and the crown-crease kinks at x 100–105, y≈150.
- A20: re-declare an honest lineage in HANDOFF. Do NOT displace lattice nodes to earn Vega.
- S9: let the 3 hidden outputs read past the card, if the shadow design allows.
- S5: needs a translator/`encoding.md`. Not the designer's job this round.

## Preserve
- **All r04 arithmetic** (sci r04: truth 9):
  - 5×5 LoG, σ = 1 cell, zero-sum.
  - Valid convolution, stride 2, 11×11 output.
  - Swept set i+j ≤ 10, with the staircase front equal to the exact union of swept windows (to 0.01 lattice).
  - Rings = rint(4|y|/max|y|), centred on the node's own input sample, one ring pitch (1.02 mm) everywhere including the key.
  - 59/63 visible bins exact, Pearson 0.98, sign 29/29.
- **0 inputs hidden** (S2): first response ring r 1.98 > max dot r 1.13. Outer ring clears neighbour dots by ≥ 0.8 mm.
- **X continuity across the front** (S3): distance-field rings at 1.05 mm constant pitch, no wobble, no seams, min 1.041 mm. Dots and rings encode one X (Spearman 0.91 on the sheet).
- **The one field** (A1): no second panel, grid, inset, staircase copy or leader line.
- **Working diagonal and asymmetry** (r03/r04): the staircase front running from the top edge down-right, with the head on the Y's fork at node (5,6).
- **Depth by clipping**: rings stop on one clean line 0.85 mm outside the staircase keyline, and grazing clips are re-joined (no hooks).
- **Ben-Day head**: 25 signed taps around the samples they multiply. The blue centre collar continues the blue skeleton across the card.
- **3 pens** (black / crimson / dodgerblue), deterministic (seed-independent gcode), every ink edge ≥ 10 mm inside the drawable area except the deliberate top/right bleed of the unswept rings.

## Do not
- Do not crop anything that carries Y or the swept X. Only unswept rings may leave the sheet.
- Do not fill the freed area with a new panel, inset, thumbnail or decoration. The key and title are the only things standing apart from the field.
- Do not draw the shadow as another hairline offset box. That is the r04 "registration double".
- Do not move lattice nodes. Positions are what the science critic recovers exactly. Size is the only variable.
- Do not add explanatory formula lines beyond the one finding line. The art critic already flagged "rings = round(…)" as a lab-figure tell. Prefer shortening the existing key rows.
- Do not return to the r02 or r03 layouts, bilateral symmetry, or dotted leashes.
