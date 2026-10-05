# Art critique — superposition r03 · canon: Op Art (lineage Riley, *Cataract 3*) · 2026-09-29
render: gallery/studio/superposition/current/pp_superposition_INTERFERENCE_FIELD_v9.png
(gcode read for measurements only: gallery/studio/superposition/current/pp_superposition_INTERFERENCE_FIELD_v9.gcode)

No `encoding.md` or `BRIEF.md` exists for this slug, so the canon is taken from HANDOFF's
lineage line (Op Art / Riley). There are no §1/§2/§9/§11 items to check. The reference is in
play, so the AUTHORING §6 questions are answered below.

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | The black contour triangle dominates at 3 m, and the Q and K rulers read second. But the loudest mass is the sink column (x 39–60, y 180–254: 18 rings at 1.15 mm), not the induction diagonal, which is what this head actually does. The lower third (V chord, dashes, Z, caption) has no rank. It is an appendix. |
| 2 | grid & alignment | 6 | The rulers, the softmax axis and the caption share the matrix edges x 37.6 / 194.0, which is good. The Z group floats in the lower-right corner: its baseline overshoots to x 196, its left end sits at x 144 on no axis, and it is not on the V→Z line. The Q ruler sits 10.5 mm from the left edge while the right margin is 14 mm. |
| 3 | tension & asymmetry | 5 | The causal knife gives one real diagonal and the L-frame of rulers is off-centre. Everything else is a vertical stack of horizontal strips (ruler / matrix / profile / chord / caption). Nothing crops at the frame and nothing overlaps with intent. |
| 4 | negative space | 5 | The empty upper-right triangle is a real, shaped void (the causal mask), and it is the best decision on the sheet. The bottom 70 mm is leftover space: the dashes stop in mid-air, and there are unassigned holes at (40–140, 70–80) and (110–190, 18–40) around the caption. |
| 5 | craft for pen | 6 | Spacing is clean: minimum 0.97 mm, 1.10–1.17 mm across the sink column. No floods, 6 clean layers in light→dark order, 320 pen cycles, about 24 min. Three defects: (a) the knife starts at (50.6, 249.0) but the contours rise to (44.7, 254.3), so the 7 outer rings are clipped along an UNDRAWN line at the apex; (b) the dashed V→Z connectors end at y 44.2, while Z's crest is at 39.7, so they miss their target by about 4.5 mm; (c) a ring at (125, 106) is sliced in half by the section cut. |
| 6 | concept legibility | 3 | This is a textbook figure: a contoured attention heatmap with marginal waveform rulers, tick rows, a profile plot on a tick axis, a signal on a baseline and a formula. It is the "scientific figure" failure word for word. Riley's order (one line family whose swelling IS the information) is claimed in HANDOFF and appears nowhere on the sheet. The contours are iso-lines, not a family. |
| 7 | depth & dimensionality | 3 | Flat, and the flatness is not declared. Op Art's whole move is optical depth from a line family's modulation, and this sheet has none. |

**avg 4.86 · min 3 · VERDICT: FAIL**

## Reads at a glance
At 3 m this reads as a contour plot of a lower-triangular matrix with wiggly marginal plots and a chart strip under it. It looks like a journal figure, not a Riley.

## Acceptance checks
No encoding §11 exists, so there is nothing to mark.

AUTHORING §6 (reference = studio/superposition/ref/reference.png):
1. Main forms recognisable without colour: **FAIL**. The matrix reads. The V chord and Z do not read as stages, and the reference's Q/K/V bump *families* are reduced to 4 single lines per ruler.
2. Shade lines follow the surface: **PASS**. Contours follow the field. There is no random mesh.
3. Fine lines that are two sides of one thick stroke: **PASS**. None.
4. Blackest regions intended: **PASS (with note)**. The sink column is intended, but it outranks the induction diagonal (see hierarchy).
5. Labels readable at pen width: **PASS**. The caption is about 3 mm. The formula line is about 2 mm and the Kᵀ superscript is marginal.
6. Thicker pen knots at corners: **FAIL**. At the knife apex, 7 rings end on an undrawn diagonal at 1.1 mm pitch. A 0.5 mm nib makes a toothed wedge there with no closing line.
7. Long empty travels / tiny marks with no benefit: **PASS**. Travel is 3.2 m against 6.1 m of draw (high, but each layer's long hop is its single entry travel), and there are only 320 cycles.

## Biggest weakness
The plate is still a figure. The r02→r03 move to INTERFERENCE FIELD made the matrix dominant and computed, but it rendered the matrix as a contour heatmap surrounded by plot furniture (tick rows, a profile plot, a section cut, a chord on a baseline). The claimed Riley order, a single line family whose pinching and swelling carries attention, is absent. Nothing on the sheet could hang beside *Cataract 3*.

## Mandates
1. **Replace the contour nest inside the triangle with ONE row-line family.** Draw ≥ 60 near-horizontal lines at a fixed pitch between y 106 and y 254, one per query position. Each runs from the matrix's left edge x 37.6 to the knife, and its local vertical displacement and pitch pinch are driven by that row's attention weights. The sink column and the induction diagonal should then appear as the family swelling and bunching, not as iso-rings. Test: zero closed loops inside the triangle, every line touches both the left edge and the knife, and no gap between neighbours falls under 0.8 mm.
2. **Strip the figure furniture and fix the knife.** Delete the blue tick row (y ≈ 259), the red tick column (x ≈ 36), the black tick axis and baseline at y 84.6, the softmax profile plot, and the section cut at y 105.6. The only straight line left on the sheet is the causal knife, and it must run to the true apex: it starts at or above the highest inked point of the family (currently (44.7, 254.3), while the knife starts at (50.6, 249.0)). Test: no tick marks and no straight horizontal baselines anywhere, and no stroke ends on an undrawn line.
3. **Rebuild the bottom 70 mm as one composed zone on the matrix's grid.** V and Z must share an edge with the matrix (x 37.6 or x 194.0). Every V→Z strand must end ON the Z curve (gap 0 mm; currently 4.5 mm short at (158, 44.2)). Z must be at least 100 mm wide rather than a 52 mm curve parked in the corner. If Z cannot be made visibly the weighted sum of the V strands, fold V/Z into the field and leave the bottom as a deliberate quiet band holding only the caption. Test: no element's left or right end in y < 70 lies off x 37.6 / 194.0, and no dashed stroke terminates in empty paper.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | — | There is no `studio/superposition/LEDGER.md` or `FEEDBACK.md`, so no A*/J* mandates are open. Against DESCRIPTION.md "If only iterating": stipple and debris dots deleted (**FIXED**, no loose dots on the sheet); map ≥ 0.55 sheet width and off-axis (**FIXED**, about 156 mm of 210, right-weighted); third vortex visible or removed (**FIXED**, the field is now computed and there is no stray whorl). |

DESCRIPTION.md § Keep:
- Vertical spine of five stations on u 0.50: **no longer true** (a deliberate consequence of direction 2, and acceptable).
- Evenly pitched contour map with conical eyes: **true in craft** (rings 1.10–1.17 mm, continuous), but the two eyes are now a chain of small whorls, and contour nests are the wrong grammar for the stated Riley lineage (see M1).
- Dotted connector fans that visibly carry Q/K in and V into Z: **not true**. Only two dashed V→Z strokes remain, and they miss Z.
- Colour as provenance with black for operations: **true**.
- Wide V against narrow Z as a contraction: **partial**. V is a single full-width chord and Z a small 2-hump curve in the corner, so the contraction does not read as a sum.

## Regressions vs compare-to (v16)
- **Superposition itself is gone.** v16's Q/K/V/Z were families of overlapping bumps (the literal superposition in the title). r03 has 4 single lines per ruler, one V chord and one Z curve. The plate named SUPERPOSITION no longer shows anything superposed.
- **Connector fans lost** (a Keep item). v16 carried the provenance colours into the field and into Z with about 40 strands. r03 has 2 dashed strokes that do not reach their target.
- **Z collapsed.** v16's nested 10-bell green mass was the plate's second-strongest form. r03's Z is a 52 mm single curve that is the weakest element on the sheet.
- **Richness and line density.** The reference's graded families and v16's layered curves gave the sheet texture at 30 cm. r03 is sparse outside the matrix, and at 30 cm the rulers reward nothing.
- Gains to keep: dominant, asymmetric, computed field; debris removed; travel 11.1 m → 3.2 m; commands 69 k → 26.5 k; spacing floor respected.
