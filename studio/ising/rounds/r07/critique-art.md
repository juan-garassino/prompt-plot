# Art critique — ising r07 · canon: science_poster · 2026-09-29
render: gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png (seed sweep s3 / s13 checked; same structure, s3 identical verdict)

## Scores
| dim | score | note |
|---|---|---|
| 1 hierarchy | 7 | Ruled sea is the loud mass at 3 m, CRITICAL spine second, the scatter third. But the hero line, the crimson coast, is a 1-pass hairline sitting against 3-pass black hulls 1–2 mm to its right (x 85–100, y 55–160). At 1 m the black out-weighs the red it borders. |
| 2 grid & alignment | 8 | Ruler, lattice, cold-wall rule and spine share edges. Footer col 1 is flush with CRITICAL at x 15, col 2 sits under the crimson 1.00 tick, col 3 left edge is exactly on the 177.3 tick. The top-edge field is 2.2 mm under the ruler baseline, which is tight but deliberate. |
| 3 tension & asymmetry | 8 | Strong left-heavy dissolve. The coast is now an almost vertical ragged wall (lateral excursion ≈ 30 mm, x 75–105) with no working diagonal. |
| 4 negative space | 7 | The hot tail finally goes to paper (x 240–287, y 36–110 is bare). The 1.05–1.35 band is a tangle: black and grey outlines run parallel at the 1.18 mm lattice pitch and read as doubled lines, not as shaped density. The right third is an even sprinkle until the last 40 mm. |
| 5 craft for pen | 7 | 3 clean layers, stated order, crimson clearance measured at 0.85 mm with no stroke under 0.8 mm, bounds clean, 62 min. **49 black strokes under 4 mm** in the field, 40 of them in x 68–100 along the coast: clip residue, not marks. There are also open hull ends at the top and bottom wrap edges, and a lone 2.35 mm dash at (142.8, 188.4) under the 1.40 tick. |
| 6 concept legibility | 8 | Order → disorder at a place: the ruled field holds, breaks at one red coast, and dissolves into shrinking outlines, then paper. It is an abstract order (lattice-with-defects plus a Schotter gradient), not a schematic. `TC IS A PLACE` is the twist and it lands. The ruler is a stated thermometer scale, which is allowed by the canon. |
| 7 depth & dimensionality | 7 | Declared flat. Flatness serves a lattice configuration. The pass-weight ladder gives a modest near/far read, but only in the 1.0–1.3 band. |

**avg 7.43 · min 7 · VERDICT: FAIL** (avg < 8)

Lineage (Nees, *Schotter*): the dissolve now ends in paper as it should. Hung beside Schotter, though, it lacks Schotter's single progressive element. Here the element changes identity at the coast (rules become outlines), and the transition band is a knot rather than a gradient.

## Reads at a glance
At 3 m you see a black ruled block on the left, torn along a thin red edge, crumbling into ever smaller outlined islands that thin out to bare cream on the right, with CRITICAL standing up the left edge.

## Acceptance checks
No `encoding.md` and no `BRIEF.md` exist for ising (the ledger process gap is still open), so there are no §11 checks to run. I checked the HANDOFF's claims against the ink (gcode) instead:
- Crimson clearance ≥ 0.85 mm from black and grey: **PASS** (measured min 0.85, 0 samples under 0.8)
- Last 25 mm column holds 2 outlines: **PASS** ((269,114), (278,121), both grey)
- Hot-side column fade, x 180→287 in 20 mm columns: 18 / 9 / 4 / 2 / 2 / 0. **PARTIAL** (tie at 240/260)
- Bounds: gcode X 15–286.6, Y 13.05–197.2, inside the drawable area; footer 3.05 mm above the bottom margin, ruler labels 2.8 mm below the top margin: **PASS**
- 3 pens with one layer each and a stated order: **PASS**
- AUTHORING §6: N/A (no reference)

## Biggest weakness
The coast, the one object the whole plate exists to show, is the thinnest line in its own neighbourhood. It is a 1-pass crimson hairline boxed in by 3-pass black hulls and a litter of sub-4 mm black crumbs left by the clearance clip. The band where the transition happens (x 70–130) reads as a scribbled knot rather than a place.

## Mandates
1. **The coast out-weighs everything it touches.** Draw the crimson hull at ≥ the 3-pass black weight (≈ 0.7 mm band). Test: nowhere in x 70–110 does a black stroke read heavier than the crimson line beside it. If that breaks the 0.85 mm clearance, the neighbouring black hull steps back, not the red.
2. **Zero crumbs.** No black or grey field stroke under 4 mm (r07 has 49; the clusters are at (84.9–86.3, 57.6–58.6), (86.8–93.0, 115–124), (77.9–79.2, 101–112)). A hull cut by the coast clearance either closes along the 0.85 mm offset or is dropped whole. Hulls cut by the top/bottom wrap close on the field edge line or are omitted. The lone dash at (142.8, 188.4) goes. Test: a stroke-length census of the field (y 36–189, x > 38) shows min ≥ 4 mm.
3. **Give the transition room: magnify 0.90–1.35 Tc on the axis.** Use a non-linear, printed x(T) (the ruler ticks show it) so the band 0.90–1.35 takes ≥ 45 % of the field width (r07: ≈ 23 %), while the hot tail compresses and keeps A18's fade and the bare last column. Tests: the coast's lateral excursion is ≥ 45 mm (r07 ≈ 30 mm, r05 ≈ 55 mm), and no two distinct outlines in x 90–140 run parallel for > 10 mm at the 1.18 mm pitch.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A18 | PARTIAL | Hull counts by 20 mm column from x 180: 18/9/4/2/2/0. The last column has ≤ 3 marks and a mark-free block ≈ 45 × 74 mm (x 240–287, y 36–110) exists. The strict decrease breaks on a 2 = 2 tie at x 240/260. The A14 preserve holds: across 1.15–1.35 / 1.35–1.55 / 1.55–1.80 the printed count is 44/33/27 and the mean size 27.1/19.5/17.4, both strictly decreasing |
| A19 | FIXED | Measured min crimson-to-black and crimson-to-grey distance is 0.85 mm, so there are 0 crossings. Rules end short of the coast. No 3-pass knot visible at the top edge. Side effect: the clip left 49 sub-4 mm black stubs (see mandate 2) |
| A20 | FIXED | Field bottom 36.4 vs footer top 31.0 (5.4 mm). Last footer baseline 13.05, which is 3.05 mm above the margin (just passes). Ruler labels 2.8 mm below the top margin. Col 3 left edge 177.31 is on the 177.3 tick. `TC IS A PLACE` has ≈ 3 mm clear above |
| S9 | FIXED | `FK SPINS BONDED WITH PROB 1-EXP(-2J/T)` and `WEIGHT PEAKS AT TC COUNT PEAKS PAST IT` are both on the sheet |
| S10 | NOT FIXED (deferred) | Seed 7 is still the plate, so it does not bite. Not verifiable by eye |
| A21 | FIXED | The `A` diagonals are now at the same heavy weight as the rest of the spine |

## Regressions vs compare-to (r05 v8)
- **The dark body shrank.** Stretching the axis to 2.30 narrowed the ruled sea from ≈ 78 mm (x 37–115) to ≈ 53 mm (x 37–90), and the 3-pass black continent mass that r05 carried in x 110–175 is gone. The canon's "one dark mass anchoring it" is weaker, and CRITICAL now nearly rivals the sea for weight.
- **The coast lost its fjords and its diagonal.** In r05 it wandered x 90–145 with a top-left to bottom-right drift and the big bay at y 40–60. In r07 it is a near-vertical ragged wall confined to x 75–105. Tension is down.
- **New clip crumbs.** 49 black strokes under 4 mm (r05 crossed the coast instead). Fixing A19 by clipping traded a crossing for litter.
- Improvements that hold: the hot tail fades to paper (A18 mostly), the footer has air (A20), draw 16.6 → 12.4 m, and travel 0.59× → 0.50×.

DESCRIPTION.md § Keep:
- The crimson interface is the single long-range object, scarce and loud. **Still true in form, weakened in weight**: it is scarce, but it is not loud at 1 m (mandate 1).
- Line weight = domain scale (1/2/3 passes). **True.**
- Hero cropped flush at the top and right edges. **Superseded** by the COOLING STRIP encoding; the field crops flush at top and bottom (wrap) only.
- Empty crimson `1.00` plate. **Transposed**: it survives as the lone crimson 1.00 ruler tick, which is aligned over footer col 2. Still true in spirit.
- Walls on the dual lattice as staircases ≥ 1.07 mm. **True** (1.178 mm pitch).
