# Synth — millennium-poincare after r01 ∥ r02 · 2026-09-29
route: designer
next round: r03 · parent: r02 (best so far). It ranks 1 of 2: art 7.43/7 against r01's 6.71/6, and science 9/8/7 against 8/8/7. No geometry merges in from r01. r01 stays on disk as the faithful flavour, the only round with the stuck CSF loop and the 3-D embedding.
thesis: abstract (keep it; flatness stays declared)
round: 3 of 5

## The instruction
Make the surgery instant the spine of the plate. Fork `rounds/r02/piece.py` and change nothing in the flow data, the scale, the diagonal or the type columns.

1. **Isolate the keyline.** Pull the t_s keyline out of the line layer onto its own black 0.5 layer, drawn once, not twice at 0.3. Clear a bare moat of ≥ 2.5 mm on both sides of it along its whole length. The last halo line and the first A/B rings pause inside that moat. Nothing is respaced.
2. **Hand the neck to the red cut.** At the waist the heavy line yields to the red: the keyline pauses symmetrically wherever the red caps (still radius exactly h = 0.11971 u about the cut) run within 0.8 mm of it, edge to edge at true nib widths. At t_s the caps really do replace the neck.
3. **Clean the rims.** Fix the pause rule so that a ring that pauses on a crowded rim arc stays paused for the whole arc. A's far pole and B's crown then read as continuous merged lines or clean absence, never dashes.
4. **Fix the footer.** Let it say the race is relative, NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 %. Declare the off-grid t = 0 outer line. Add one clause: outside the heavy line = before the cut, inside = after.

The 3 m read must change from "a two-hill contour map" to "one space before, one heavy instant, two dying spheres after".

## Mandates to close
1. **A1.** The keyline stands alone:
   - a ≥ 2.5 mm moat on both sides;
   - its own black 0.5 layer, single pass;
   - the caption clause.

   Gcode test: no line-layer point other than the keyline lies within 2.5 mm of it.
2. **A3.** Red off black at the waist:
   - ≥ 0.8 mm bare paper, edge to edge, between red and every black mark;
   - the red radius stays exactly h;
   - the keyline pauses symmetrically, with the per-flank pause length stated in NOTES.
3. **A2.** No rim stutter at A's far pole (x 40–140, y 30–85), A's lower-right (x 170–190, y 40–70) or B's crown (x 170–240, y 250–297). The line layer has zero strokes < 15 mm, other than whole rings near the extinction points.
4. **S1.** Footer, with every number re-verified from `snapshots.npz`:
   - "NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 % · CUT AND CAPPED AT t = 0.055";
   - "OUTERMOST LINE: t = 0 (OFF THE GRID)".

   An optional small scaled radius-bar pair is allowed in the footer column. Respacing is not.
5. **A4.** Plotting and series grammar:
   - quote per-layer minutes from `plot plate <gcode> --layers <order> --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`;
   - state the new pen order (lines 0.3 → keyline 0.5 → type → red, or justify another order);
   - add the series caption `MILLENNIUM PRIZE PROBLEMS 6 / 7` / `CLAY MATHEMATICS INSTITUTE, 2000`, ≤ 2.2 mm caps, on the x = 205 right column in the title band.

Deferred:
- **A5 (dots Ø 2.4–3 mm).** Take it only if B keeps ≥ 5 mm of bare paper.
- **Dossier corrections.** R_min 0.2167, lie #4 and §2(a) relative-only, and the encoding §4 "lobe halo merges" claim is false. They are recorded in LEDGER. Mention in NOTES that the sheet follows the corrected reading.

## Preserve
- **Flow data and alignment.** `snapshots.npz`, with 0 snapshot error; t_s = 0.054647; 33 A / 6 B rings at Δt 0.01 anchored at t_s; neck pinned pre-surgery; ψ²ds centroids held post-surgery. Science recomputed 99.8 % of ink within 0.5 mm, so do not re-solve and do not respace.
- **Layout.** 62 mm/u, axis at 62°, cut at (165, 200), ink bbox x 30–240 / y 34–297. The upper-left quiet zone (x 15–150, y 205–320) stays bare. Art scored tension 8 and grid 8.
- **Type columns.** Title, statement and SOLVED stamp stay flush at x = 15. The corner line and footer stay on the single right column at x = 205, ending at x = 282. Keep the stamp: red SOLVED, Perelman 2002–03 after Hamilton (1982), Fields 2006 + Clay 18 Mar 2010 both declined.
- **Craft.** The 0.8 mm floor on the line layer (min 0.837 mm today). Nothing crosses the keyline. The cut interior stays bare, and the first rings stay ≥ 2.5 mm off the red. The time-occlusion stack and the hysteresis pause (0.85 / 1.2 mm).
- **Lineage.** Molnár *(Dés)Ordres* 1974, named in HANDOFF. Canon 6 on cream, with red only for the events: caps, 2 points, SOLVED.

## Do not
- Do not draw the r01 grey shell, the stuck CSF loop or any globe/meridian grid. They are forbidden in [abstract], and art read them as a bowl.
- Do not shrink or offset the red caps off radius h to buy clearance. The black yields, not the red.
- Do not buy the moat by respacing or dropping any Δt line. Lines pause inside the clearance only, and the ring counts stay 33 + 6.
- Do not let any ring re-enter on a crowded arc as dashes after it has paused. That stutter was the loudest black on the sheet.
- Do not quote minutes at F600 from `audit.py` alone. The plate job's numbers come from `plot plate --dry-run`.
- Do not add a second accent colour or turn the keyline red. Red is the cut only.

## Gate
Not run: no double PASS yet (r01 FAIL/FAIL, r02 FAIL/FAIL). It runs on the first double PASS.
