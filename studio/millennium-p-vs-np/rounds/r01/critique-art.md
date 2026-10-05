# Art critique — millennium-p-vs-np r01 · canon: RADIAL DATA-VIZ (5) on the SWISS sheet (3), thesis [F] faithful (unrolled) · 2026-09-29
render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.png (judged on gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6_truewidth.png, 5 px/mm)

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | The tree field clearly dominates. The second read, the red thread, is a 0.5 mm line; that is under visual acuity at 3 m (≈0.9 mm), and it sits at x 273.5 between black drops at 270.5, 278.8 and 280.8, so at 3 m the needle does not read. The 10 mm title and the bottom band are all mid-sized. |
| 2 | grid & alignment | 7 | The flush-left x 15 edge is held by the title, statement, instance line, Petersen tree and caption. The checking block starts on the START/root axis (x 148.5) and ends on the red axis (273.4). SOLUTION sits flush-right at 282. The right definitions column (x ≈ 182) shares no axis with anything in the field. |
| 3 | tension & asymmetry | 5 | Rows 0–5 are a perfect centred binary pyramid, and it is the heaviest ink on the sheet (0.3 pen) at the top of the field. The top band is balanced (title left, definitions right) and so is the bottom band (tree left, chain right). The only asymmetry is the data: curtain lengths and the red at the right edge. For a Swiss sheet this is too polite. |
| 4 | negative space | 6 | The carved lower-left void (x 15–130, y 100–140) is real and shaped by the data, and it opens into the gap above the Petersen tree. The upper band and the gutter between the chain caption (y 50) and the FINDING caption (y 35) are leftover, not sized. |
| 5 | craft for pen | 6 | Spacing floors hold: hairlines ≥ 2.0 mm, red to nearest black 3.0 mm, Petersen leaves 1.1 mm. 2 swaps, no floods. But: (a) the stems of the 10 mm title are built from parallel passes that do not fuse, so P, N and S show white stripes inside the stems at true width; (b) the Petersen leaves pair up at 1.1 mm in 0.3 ink, which makes a barcode, the blackest patch on the sheet; (c) the red takes ~0.3–0.5 mm jogs at rows 8–11, which a 0.5 nib turns into kinks; (d) the preview reports 12.0 m travel against 19.9 m draw, and diagonal travels cross the sheet; the job is ≈ 100 min. |
| 6 | concept legibility | 4 | The order (nested halving, pruning as void) is exact and present. But the form is a dendrogram with START/SOLUTION labels, which is a CS-textbook backtracking figure. At 3 m a stranger sees "hierarchical-clustering plot". The twist (needle found at 96.84 %, almost last) and the finding-vs-checking ratio land only at 1 m, and only with the caption. |
| 7 | depth & dimensionality | 6 | Flatness is declared and serves the exact measure. The 0.3 → 0.1 step at row 7 gives a real crown-over-curtain layering, and the ragged skyline of stops reads as recession. It is modest. |

avg **5.71** · min **4** · **VERDICT: FAIL**

## Reads at a glance
At 3 m: a large centred black family-tree pyramid over a grey curtain of verticals, longer on the right, with small type bands above and below. The red thread is invisible at that distance.

## Acceptance checks (encoding §11, [F])
1. ONE RED RADIUS: **PASS**. One red reaches row 20. It ends at x = 273.5 (target 273.6 ± 0.5), steps right from the root and runs back to 269.5 at row 5, as specified.
2. THE CARVING: **PASS**. 32 lines cross below row 5 (complete) and 56 below row 6, so 8 first ends are at row 6. 15 lines reach row 20 (14 black + red). The refuted areas are bare.
3. LOPSIDED: **PASS**. The left half has exactly one line reaching row 20, at x = 141.2. All other rim contacts are right of the axis (182.8 … 280.8). The post-discovery strip right of the red is drawn (278.8, 280.8).
4. CHECKING IS THE RED, AND IT COUNTS: **PASS**. 91 ticks, mean pitch 1.37 mm. Lengths are 41 / 36 / 14 (≈1.5 / 2.75 / 4.0 mm). There are 14 side-alternating runs, sized 1,3,1,2,3,4,5,4,8,13,7,12,10,18, which matches the closing variables. No arrow and no dot. Captions give 45,088 against 91 and name the method (backtracking x1..x20, false first; UP 87 nodes).
5. PLOTTABLE AND CLEAN: **PASS (with craft notes)**. The .gcode sits beside the png. 4 layers, 2 swaps, spacing ≥ 0.8 mm. The weight changes at row 7 and the caption says why. No type in the field or void. The Petersen tree has zero red, and no reference boxes or circles remain.

AUTHORING §6 (reference = AI poster, interpretation brief):
1. Main forms recognisable without fills? **PASS**. The START-top / SOLUTION-bottom architecture survives, corrected.
2. Shadow lines follow surface? **N/A** (no tone by design).
3. Fine lines that are two sides of one thick stroke? **FAIL**. The title stems read as double or triple outlines.
4. Blackest regions intended? **FAIL**. The blackest patch is the Petersen leaf barcode (bottom-left companion), not the subject.
5. Labels readable at true pen width? **PASS**. All captions are legible at 1.8–2.5 mm.
6. Thick pen knots at corners? **PARTIAL**. The red 0.5 jogs at rows 8–11 kink. The title passes stripe instead of fusing.
7. Long empty travels or wasteful tiny marks? **FAIL**. 12.0 m of travel is ~60 % of the draw length, and the preview shows sheet-crossing diagonals.

Interpretation verdict: this is an honest correction of the reference, not a trace. The reference's drama (one mass, one weaving red spine down the middle) has been traded for correctness without a new drama to replace it. The red that should carry the plate is the weakest-weighted element on it.

## Biggest weakness
The plate's loudest element is the information-free part: rows 0–5 are complete by definition (no pruning until row 6), yet they form a heavy, centred, symmetric 0.3 pyramid, which makes the sheet read as a textbook dendrogram. The needle, the thesis, is a 0.5 mm red hairline pressed against the right edge, invisible at 3 m.

## Mandates
1. **Make the needle the second read at 3 m.** From the row-7 fork (y 262.5) down to row 20 (y 100), draw the red drop so its visible width is ≥ 1.2 mm: parallel red passes ≤ 0.3 mm apart that fuse, or a broader red nib. Also clear black 0.1 drops to ≥ 3 mm on each side of it (the 270.5 drop is at 3.0 now; keep it or push it). Test: in a 300-px-tall thumbnail of the true-width render, the red vertical at x 273.5 is a continuous visible line from the crown to SOLUTION.
2. **One huge element, and fused.** Set `P  VS  NP` as the sheet's poster-scale mass: cap height ≥ 25 mm, flush-left at x 15, top band. Move the definitions column down or narrow it to clear it. Build stems as solid fused strokes, with pass pitch ≤ the 0.3 nib, so no stem shows internal white stripes. Test: cap height measured ≥ 25 mm, and at true width every stem of P, N and S is solid.
3. **De-barcode the NO companion.** Widen the Petersen tree from x 15–94 to x 15–≈130 so its leaf pitch is ≥ 1.55 mm (keep ≥ 18 mm gutter to the checking block at 148.5). Its bottom band must no longer be the blackest patch on the sheet. Test: no two 0.3 verticals in the companion closer than 1.5 mm centre-to-centre, and its caption stays flush-left at x 15 on the same baseline as the FINDING caption.

(Also flagged, not a mandate: 12.0 m of travel against 19.9 m of draw. Batch text by band and order the tree strictly left to right so the sheet-crossing diagonals disappear.)

## Follow-up on open mandates
none. This is r01; no LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists for this slug.

## Regressions vs compare-to
none. compare-to: none (new plate).
