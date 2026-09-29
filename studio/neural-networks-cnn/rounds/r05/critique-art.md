# Art critique — neural-networks-cnn r05 · canon: RADIAL DATA-VIZ (STYLES §5, declared flat) · 2026-09-29
render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.png

This round is a wildcard. It drops the terrain stack and redraws the piece as a Nightingale-style half rose. Scored cold against STYLES §5 and the rubric. No `encoding.md` exists, so the acceptance checks below come from the brief (`studio/nets/cnn.md`) and the §5 canon.

## Scores
| dim | score | note |
|---|---|---|
| 1 hierarchy | 7 | The order is clear: the title, then the teal fan, then the rim brackets, then the notes. But the gold half-mass line carries the subtitle's claim ("A QUARTER OF IT") and it is the weakest mark on the sheet. In wedges IN–3 (x 23–60, y 185–200) it is buried inside the teal arcs. |
| 2 grid & alignment | 6 | Text sits on two unrelated columns: title, subtitle, legend and caption at x ≈ 112, notes at x ≈ 157. Neither column comes from the dial's geometry. The three notes are spaced evenly down the right side (y ≈ 225 / 165 / 102) and none sits beside the wedge it describes (the IN, 12 and 7² notes sit beside wedges 4, 8 and 10). The px-scale labels are tightly kerned: "160" at both ends of the diameter has 6 and 0 touching. |
| 3 tension & asymmetry | 8 | A half dial with its hub pinned 13 mm from the left margin, text taking the right side, and the rose visibly heavier at 12 o'clock than at 6. A real, committed asymmetry. |
| 4 negative space | 7 | The empty lower-left quadrant (reach falling to 0 at wedges 13–C1) is a chosen void and it is the statement. The red sawtooth runs straight through it, though, and the right column is three floating paragraphs in 90 mm of air. |
| 5 craft for pen | 7 | Petal pitch is about 1.0–1.3 mm (≥ 0.8), no floods, 4 pens and 3 swaps. Against that: travel 5.96 m is more than draw 5.52 m, there are 1,595 lifts, the rim wedges IN/S/0 break into sub-mm dot dashes (many lifts for little ink), the black layer takes 46 min (mostly type), and tick marks nearly touch the digits "4" and "7" on the rim. |
| 6 concept legibility | 6 | The radial order reads: angle is depth and reach shrinks clockwise to nothing. Fine under §5. But the plate is still a chart. It has a px axis on the diameter, a 3-row legend, a 5-line methods caption and three explanatory notes, and the notes and caption explain instead of confirming. With the text removed, a stranger sees "a fan that shrinks" and not "one unit that could see everything but looks at a quarter". |
| 7 depth & dimensionality | 6 | Declared flat. The only layering is dotted rings behind the petals and the red rim over the black tick ring. The red and gold lines lie on the same plane as everything else. |

**avg 6.71 · min 6 · VERDICT: FAIL**

## Reads at a glance
At 3 m: a half rose of blue concentric dashes, dense at 12 o'clock and dying away clockwise, inside a red rim that holds for a quarter turn and then falls apart in a jagged line toward the hub.

## Acceptance checks
No `encoding.md` exists (ledger item S6), so these come from the brief and the §5 canon.
- Brief idea: one unit's receptive field grows with depth (shown here backwards, as one unit's reach into the input) — **PASS**
- Brief idea: spatial resolution falls as abstraction rises — **PASS** (outer bracket ring 224² → 7²). The bracket labels say it in type; the marks do not show it.
- Brief palette: black + one red accent — **FAIL** (four hues; allowed under §5's "muted multi-hue", but red is no longer scarce)
- §5: concentric arcs, even pitch within a series — **PASS**
- §5: angle = category, radius = track, clear to a stranger — **PASS** (wedge labels IN…C1 plus the brackets)
- §5: scale labels and a compact legend — **PASS**
- §5: small glyph markers on the arcs — **FAIL** (none)
- §5: empty centre and outer margin breathe — **PASS** (R0 12 mm, outer margin ≥ 6 mm)
- §5: typographic, gridded annotation, never boxes-and-arrows — **PARTIAL** (no boxes, but the text sits on an ungridded two-column layout)
- Rubric: NO SCHEMATICS / scientific figure — **PARTIAL** (it is data-viz by canon, but the px axis, legend and 5-line caption push it toward a figure)

## Biggest weakness
The two lines that carry the plate's claim are drawn as noise:
- **Red (theoretical edge):** from wedge 9 clockwise it becomes a diagonal sawtooth (x 23–135, y 75–130) that reads as a stock chart, not a polar-area rose.
- **Gold (half-mass):** this is what "IT LOOKS AT A QUARTER OF IT" rests on, and it is the thinnest and most hidden mark on the sheet.

The distance between red and gold is the story, and neither line can be read as a clean shape.

## Mandates
1. **Make red and gold true polar-area steps.** In each wedge, draw one arc at constant radius across the full wedge, and join neighbouring wedges only with a radial riser on the gutter ray. No diagonal segments. Test: every non-arc segment of the red and gold lines lies on a ray through the hub (23, 148.5), and the red line from wedge 9 to C1 steps down without ever rising.
2. **Make the gold half-mass ring the loudest data line.** Double-pass it (second pass 0.6–0.8 mm outside) and cut every teal dash within 1.2 mm of it, so it reads as one unbroken ribbon at 3 m. Test: crop wedges IN–3 (x 23–70, y 180–205). The gold is continuous and no teal dash touches it.
3. **Put all type on one column taken from the dial, and anchor each note to its wedge.**
   - Title, subtitle, notes, legend and caption share one left edge. Use x = 112 (the title's), or the rim's x-extent + 8 mm.
   - Each note's first baseline sits at the y of the rim label it describes: the block-12 note at y ≈ 62 by label "12", the 7² note by the 7² bracket at y ≈ 25. Move the legend and caption so they stay clear.
   - Space the digits of "160" at both diameter ends by ≥ 0.5 mm.

   Test: exactly one text left edge on the sheet, and each note is level with its wedge label.

## Follow-up on open mandates
r05 changes route from the terrain stack (r03) to a radial rose. Most open terrain mandates no longer apply; each is marked by what is on the sheet.

| id | status | evidence |
|---|---|---|
| A3 (crimson scarce, closed occluded loops, occlusion breaks) | NOT FIXED | Moot as worded (there are no loops), but the scarcity half has gone backwards. Red is now a 250 mm rim-plus-sawtooth line, the longest coloured mark on the sheet. |
| A4 (top terrain solid, 7 continuous rows) | NOT FIXED | Superseded: no terrain on the sheet. |
| A11 (title strokes doubled ~0.6 mm) | FIXED | "THE REACH OF ONE UNIT" is single-stroke at zoom (crop x 915–1060 px). No parallel duplicates. |
| A12 (preview on cream) | NOT FIXED | The preview is still white. Tooling item, argued. Not docked. |
| A14 (preserve the r02/r03 summit as the reading destination) | REGRESSED | No summit and no single accent destination. The eye now ends on the title, not on data. |
| A15 (monotone gradient, no stroke < 3 mm) | PARTIAL | The clockwise decay of petal extent is monotone to the eye, but the red edge line is not monotone (sawtooth rises at wedges 10, 11, 13–15). The rim wedges IN/S/0 are made of dashes under 1 mm. |
| S2 (caption decodes the stack, numerals mapped) | PARTIAL | The resolution numerals now map to the wedges through the bracket ring (clear). But the caption has grown to 5 lines plus 3 notes, which is explaining, not confirming. |
| S7 (centre-crop preprocessing stated) | FIXED | The caption reads "CHELSEA, CENTRE-CROP TIGER CAT 0.43". |
| S8 (7² CAM plane shows every cell) | NOT FIXED | Superseded: there is no CAM plane. Only unit (4,3) is shown, and the runner-up cells are absent. |

## Regressions vs compare-to (r03, iterate_v5)
- **Accent scarcity gone.** r03 had one crimson accent family. r05 uses four hues and a long red line, which breaks DESCRIPTION Keep "single crimson summit as the one loud accent": **no longer true.**
- **Travel economy.** r03 had travel 3.5 m against 13.3 m draw. r05 has travel 5.96 m against 5.52 m draw, so it travels more than it inks. Commands went from 9.8 k to 16.4 k, and lifts are now 1,595.
- **Reading destination.** r03 ended on the CAM summit at the top. r05 has no data destination, and the subtitle claim rests on the faintest line.
- **Morphology gradient** (Keep): **no longer true** as a shape. Resolution loss is now stated in bracket type (224² → 7²), not built from marks.
- **Hidden-line solidity** (Keep): N/A (declared flat).
- **Rightward stagger / diagonal** (Keep): replaced by a left-pinned half dial. Tension is stronger (8 vs 7), so this is a change, not a regression.
- **Gains to keep:** no stacked-figure silhouette (A1's leftover problem is gone), a single-stroke title (A11), preprocessing stated (S7), and a chosen void at 6 o'clock.
