# Art critique — millennium-bsd r03 · canon: ART DECO (+ Morellet system, declared flat) · 2026-09-29
render: gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7_phys.png (judged; preview `_v7.png`, gcode `_v7.gcode` used for measurement)

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | Title, then the gold hub, then the fan is a clear order. The second act is still small: L is a 104 × 25 mm island in the mouth, and the bottom-right text column (22 lines, grown from 13) now outweighs it. The gold band does win the right half. |
| 2 | grid & alignment | 7 | The left column is locked at x = 15 (title, statement, ziggurat), and the series caption and right column share x ≈ 228. The L panel (152.6 → 256.6) lines up with nothing on the sheet. The upper rays crop at y = 368.4 and the lowest type glyph sits at 376.6, so there are two horizontals 8 mm apart instead of one declared line. |
| 3 | tension & asymmetry | 8 | The off-centre hub, the huge diagonal of the branch and the open right field are strong Deco monumentality that is broken on purpose. |
| 4 | negative space | 8 | The mouth void and the upper-right field are chosen. The bottom band now carries text in both corners at the same baseline, with rays in between, and is busier than the top. |
| 5 | craft for pen | 6 | The egg's upper-right arc next to the hub breaks into a beaded, stitched run. Egg ink stops at (72.8, 237.4) and (98.8, 211.3), with 1–2 mm fragments at x 74.4–79.1 / y 233–236 and at x 97.2–97.7 / y 213–214. At 0.5 mm these read as ink knots right beside the focal point. Ziggurat indices 20 and 30 still fuse at the 0.3 nib. The layers, the 3 swaps and the ≥ 0.80 floor (per HANDOFF) are fine. |
| 6 | concept legibility | 7 | "One point rules every line, and the lines stop on the curve" reads. The link between geometry and analysis (the reference's whole idea) depends on an invisible shared y = 200, so L reads as a separate chart. The parity rule (odd lands on the oval, even on the branch) comes across only as "two destinations". |
| 7 | depth & dimensionality | 7 | Flatness is declared and correct for the claim. The three weights plus the gold give real layering. |

**avg 7.14 · min 6 · VERDICT: FAIL**

## Reads at a glance
A gold coin shoots a black sunburst whose rays stop sharp on a left oval and a giant "<". In the empty mouth a small line dips and crosses its hairline in a short gold dash. Numeral tables fill both bottom corners.

## Acceptance checks
Encoding §11:
1. ONE HUB, RECEDING: **PASS.** All 77 rays longer than 6 mm pass within 0.03 mm of (87.6, 226), measured from the gcode. None enters the disc. There are 3 weights, and heavy/medium rays reach 7.0 mm while fine ones start at 9.6–16 mm. The recession is real but subtle at 3 m; the hub reads as a full ring of starts.
2. TWO PIECES, ONE MIRROR: **FAIL.** The tips are right: 101.59 / 131.13, which is 29.5 mm apart, with nothing between them. Top and bottom (241.43 / 158.57) are symmetric about 200. But the egg does not read as closed. Its ink breaks over x 72.8 → 98.8, which is 7.8 mm and 4.2 mm beyond the disc edge, and the break is filled with bead fragments. The yield is legitimate (S2c). Its execution is not.
3. LINES STOP ON THE CURVE: **PASS.** The mouth holds only L, its axis and type. No ray lies left of the hub outside the egg.
4. ONE CROSSING, NOT A TOUCH: **PASS.** L starts at (152.6, 200), its minimum is 195.36 (a 4.64 mm dip), it crosses at ≈ 204.6 at ≈ 16.9°, and it ends at (256.6, 219.84). There are no corners. Gold is the only colour on the right half.
5. PLOTTABLE, LAYERED, TRUE: **PASS.** The gcode has 5 layers (0 → 4) and 3 physical swaps, and HANDOFF gives the gap floor as ≥ 0.80. The ziggurat's right edge is at 82.8 (≤ 83) and sits about 11 mm clear of the nearest ray. No type touches a ray. I did not verify the coordinate truth; that is for science.

AUTHORING §6 (reference = interpretation brief):
1. Forms recognisable without fills: PASS.
2. Shading follows the surface: N/A (flat by declaration). The rays follow the group law: PASS.
3. Fine lines that are two sides of one thick stroke: PASS. The gold band is 2 passes at nib pitch and reads as one 1.4 mm band, as intended.
4. Blackest regions intended: PASS. They are the heavy bundle into the lower arm and the hub.
5. Labels readable at true width: PARTIAL. Indices 20 and 30 fuse.
6. Thick pen knots: **FAIL.** The beaded egg fragments at the hub.
7. Tiny marks with no benefit: FAIL on the egg fragments. The 24 chord stubs are meaningful.

Interpretation: the reference's idea is a flow that carries geometry into analysis. The plate replaces it with a shared mirror line that nobody sees. That is honest (a gold flow would be decorative gold, §9.5), but the bridge is left to the caption.

## Biggest weakness
The one place every eye lands, the gold hub, is where the craft breaks. The egg's upper-right arc turns into a stitched, beaded dash-run just before the disc, and a smaller one sits on the lower-right side. It reads as a plotter glitch and not a decision, and it costs the "closed oval" read.

## Mandates
1. **Make the egg's yield one clean cut per side.** Delete the egg fragments at x 74.4–79.1 / y 233.3–236.2 and at x 97.1–97.7 / y 212.9–214.1, and any egg piece shorter than 5 mm between x 70 and 100. The egg ink then ends at exactly one point on each side of the disc and the tangent takes over from there, so S2c stays satisfied. Test: in a 4× crop of x 60–100, y 205–245 there is no egg stroke shorter than 5 mm and no bead. The two egg ends are single square stops, each ≥ 0.8 mm from the tangent.
2. **Hang the right column from the gold crossing.** Move the whole right-hand text block into the mouth. Its left edge goes on x = 204.6 ± 0.5, which is the crossing vertical and matches S3(d). Its top sits ≤ 8 mm below the `S = 1` label. Keep ≥ 10 mm clearance from the lower arm. Leave the region x > 215, y < 80 empty of type. Test: the gold dash, `S = 1` and the caption form one vertical unit on the 25 % thumbnail. The bottom-right corner is open, so the two bottom corners no longer mirror each other as furniture.
3. **Un-fuse the ziggurat indices.** Re-kern 10, 20 and 30 so the two digits have a visible gap of ≥ 0.5 mm at the 0.3 nib (this is A3b, carried). Test: a 4× crop of x 15–25, y 20–70 shows two separate glyphs for every two-digit index.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A1 | FIXED | At 25 % the gold stretch is a distinct 1.4 mm gold band. It is the heaviest mark right of x = 140, L is now black 0.3, and the 16.9° angle is kept. It still reads as a dash more than an event at 3 m; that is a scale issue, not a regression. |
| A2 | PARTIAL | The notes block is gone, and the left side is clean between y 250 and 375. The series caption sits top-right, cap line on the statement's, right edge ≤ 282. The upper-ray crop (368.4) still shares no edge with another element: the lowest type is at 376.6. |
| A3(a) | FIXED (per HANDOFF) | The gcode near-parallel minimum is stated as ≥ 0.80. The branch-vertex heavy pair no longer reads doubled in the crop. |
| A3(b) | NOT FIXED | Indices 20 and 30 still fuse at the 0.3 nib (idx crop). Carried as mandate 3. |
| J* | — | There is no FEEDBACK.md and no DESCRIPTION.md, so there are no J mandates and no Keep list. |

## Regressions vs compare-to
- **The egg's upper-right arc** was one continuous 0.5 line into the disc in r02. It is now broken and beaded over about 12 mm beyond the disc, and the lower-right arc near the hub has the same beads. This came from implementing S2(c)/(a), and it is the reason craft falls to 6.
- **The bottom-right column grew from 13 to 22 lines** (because of S3). It is now the heaviest mass right of centre after the branch, and it outweighs the L panel it explains. Hierarchy did not gain from A1 as much as it should have.
- The statement is now two lines with a subscript formula. It still reads, and it is correctly left-aligned; not a regression, noted only.
- Kept from r02: the fan, the weight hierarchy, the mouth void, the ziggurat edge and the left column alignment.
