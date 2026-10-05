# Art critique — millennium-bsd r01 (faithful thesis [F], v5) · canon: ART DECO hybrid (Morellet system) · 2026-09-29
render: gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5_truewidth.png (preview gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5.png, gcode alongside)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 5 | At 3 m the loudest thing is the 8 mm title, then the 4.5 mm `RANK E(Q) = ORD` line. The drawing is all 0.3/0.5 single-pass line (egg, branch, 3 chords) with nothing heavier than the type. The gold disc is the only mass in the figure, and it is 8 mm. The figure has no dominant weight. |
| 2 | grid & alignment | 6 | The left column is disciplined: title, statement, equation, paragraph, RANK line and orbit list all sit flush at x = 15. The right side has two unrelated edges: the header is flush-right at 282 and the bridge block is flush-left at 215. The L-axis (152.6–256.6) and `L(E,S)` label align to neither. |
| 3 | tension & asymmetry | 7 | The branch's long diagonal arm crops at the top field line and the bottom margin, the hub sits left of centre, and the ±45° chords work as diagonals. This is real tension, and the Deco allowance for symmetry is not even needed. |
| 4 | negative space | 6 | The quiet zone above L (x 212–282, y 232–362) is shaped, and it makes the gold crossing loud. That is good. The lower third, though (y 15–95 across the full width except the arm), is leftover and not composed. Everything sits in one horizontal belt (y 150–245) plus a text band, so the sheet reads top-heavy with an empty floor. |
| 5 | craft for pen | 7 | Plottable. Open circles are clean at true width, 1.8 mm caps at 0.3 mm stay legible at 25 px/mm, and the gold is a single 16.9° band. There are 5 layers and 3 swaps. Against that: the tangent chord y = −x stops 11.3 mm from P (see check 1), and travel (8.1 m) nearly equals draw (8.4 m), with ~15 sheet-crossing hops visible in the preview. |
| 6 | concept legibility | 3 | This is a textbook figure. It has labelled coordinate points, an axis with `0`, `S = 1` and `2` under it, a plotted function, and a 6-line paragraph explaining the chord-and-tangent law. It could go into Silverman unchanged. It is true to the maths, and the gold crossing is a good idea, but the ORDER the encoding names (RADIAL: one gold point rules every line) does not read. Three thin chords make an asterisk, not a pencil, and one of them misses the hub. The caption explains rather than confirms. |
| 7 | depth & dimensionality | 6 | Flatness is declared (Deco + the isotropic-plane argument) and is legitimate. It is served weakly, though: every line is one pass at nearly one weight, so the flat plane reads as graph paper. There is none of Deco's thin/thick alternation to stack planes typographically. |

**avg 5.71 · min 3 · VERDICT: FAIL**

Canon note: the only Deco on this sheet is the palette and the spaced caps. There is no fan, no thin/thick passes and no exact ray rhythm. That is a faithful redraw of the reference in neutral drafting.

## Reads at a glance
A tidy, correct textbook diagram of an elliptic curve (an oval and an open branch threaded by three lines through a gold dot), with a small function graph and a gold tick to its right, under a large title.

## Acceptance checks (encoding §11, [F] branch)

1. **ONE HUB, RECEDING: FAIL.** Chords y = 0 and y = x end 4.8 mm from P, at the disc edge, and never enter the disc. The tangent y = −x is collinear with P but its drawn segment starts at (95.6, 218.0), 11.3 mm from P and ~7 mm outside the 4 mm disc. It floats beside the egg and does not visibly come from the gold point. (The [A]-only clauses do not apply.)
2. **TWO PIECES, ONE MIRROR: PASS.** The egg is closed and the branch open. The egg's right tip ≈ 101.6 and the branch vertex ≈ 131 leave a clean gap with no curve, axis or label (only the tangent chord crosses it, which is allowed). The egg's top and bottom (241.4 / 158.6) are symmetric about 200. The dashed negations x = ±1 are bisected by y = 200.
3. **LINES STOP ON THE CURVE: PASS.** y = 0 runs −3P → 2P, y = x runs 3P → −4P, and the tangent ends at −2P. Nothing enters the mouth, and there is no ray left of the hub outside the egg. There are 3 chords at 0° / 45° / −45°. There are 47 open circles plus P as the gold disc (= the 48 orbit points in the field), which matches the plate's own "(47)".
4. **ONE CROSSING, NOT A TOUCH: PASS.** L starts at (152.6, 200), dips to 195.36 (4.64 mm), and has gold centred at 204.58 at **16.92°** (the band's principal axis in the gcode, inside 17.0 ± 0.5). It ends at (256.57, 219.84). There is no corner, and gold is the only colour on the right half.
5. **PLOTTABLE, LAYERED, TRUE: PASS (with a note).** The gcode is beside the png, with 5 layers in §6 order and pens 1 and 2 the same physical 0.3 (3 swaps). No type touches a ray. Every labelled coordinate satisfies y² + y = x³ − x (P, ±2P, ±3P, ±4P, 5P, 6P and 7P were checked by hand). Note: the long sheet-crossing travels contradict the §10 "no sheet-crossing travel within a block" plan.

**AUTHORING §6 (reference = AI poster):**
1. Main forms recognisable without fills: **PASS.**
2. Shadow lines follow the surface: **n/a (no hatch), PASS.**
3. Fine lines that are two sides of one thick stroke: **PASS (none).**
4. Blackest regions intended: **PASS.** The only solid is the gold disc (4 rings at 1.0 mm pitch for a 0.7 nib).
5. Labels readable at true pen width: **PASS** (re-rendered at 25 px/mm: 1.8 mm digits keep open counters).
6. Thick pen knots at corners: **PASS.**
7. Long empty travels or tiny marks with no benefit: **PARTIAL.** Travel ≈ draw (8.1 m vs 8.4 m), with many cross-sheet hops between text blocks.

As an interpretation, the plate corrects every lie in the reference: the curve is in two pieces, all points are on E, L(0) = 0 with a transversal crossing, and the arrow and gold threads are cut. It does not *reinterpret* the reference, however. It keeps the reference's genre (figure plus caption) and loses its one poetic gesture (gold travelling from geometry to analysis) without replacing it with a visual one. The shared mirror/s-axis only reads if you read the caption.

## Biggest weakness
The faithful plate is still a schematic. With no dominant ink mass and no Deco line language, the only visual idea (one gold point rules every line) is carried by three single-pass chords, and the tangent, the most important of the three because it *is* 2P, does not even reach the hub. The eye goes to the title, then to a function plot.

## Mandates

1. **Reconnect the tangent to the hub.** The chord y = −x must start at the gold disc's edge (≤ 5 mm from (87.6, 226), like the other four chord ends at (92.4, 226) / (91.0, 229.4) / (84.2, 222.6) / (82.8, 226)), not at (95.6, 218.0). If the 0.8 mm floor against the egg forbids it, break the **egg** line where the tangent hugs it, never the chord. Test: all five chord ends that face P are within 5 mm of the disc centre.

2. **Make the pencil the dominant mass: a real Deco fan out of the gold hub.** Draw the true group-law chords k = 1…7 (the heavy tier: each line through P, kP and −(k+1)P, spanning egg point → branch point R and never past R) at **2 passes (0.3 + 0.25 mm offset)**, so 7 rays with ≥ 11.3° gaps leave the disc and read heavier than the single-pass 0.5 curve. Keep the dashed negations only for the first three steps. Test at 3 m: a gold-hubbed ray fan is seen before the title, and the pencil's ink length is ≥ 3× the L-curve's.

3. **Strip the schematic furniture and re-seat the type on the empty floor.** Delete the axis end labels `0` and `2` and the 6-line explanatory paragraph in the upper-left (keep `E : Y² + Y = X³ − X` and the CREMONA line). Cut the right-column text to the bridge (`L'(E,1) = 0.30600 = 5.98692 × 0.05111 = REAL PERIOD × HEIGHT OF P`) plus the status. Move the RANK equation to baseline ≈ 60 (§5) and the bridge block to x = 226, y ∈ [20, 110], wrapped so no line passes x = 282 (v1 overflowed there). Test: the band y 15–95 holds the two type masses either side of the lower arm, no text line ends beyond x = 282, and there is no numeral under the s-axis except `S = 1`.

## Follow-up on open mandates
No LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists for millennium-bsd. There are no open A*/J* mandates and no § Keep items.

| id | status | evidence |
|---|---|---|
| none | n/a | first critiqued round |

## Regressions vs compare-to (faithful_v1)
- **REGRESSED: tangent chord lost the hub.** In v1 the y = −x chord ran from the disc edge to −2P. In v5 it starts 11.3 mm out at (95.6, 218.0). This is the round's clearest regression, and it breaks §11 check 1.
- **REGRESSED: lower-third composition.** v1 anchored the floor with the RANK block (baseline ≈ 60) and the bridge (y 60–110), per §5. v5 fixed v1's right-margin overflow (bridge lines ran past x = 282 into x ≈ 290) by lifting both blocks to y 110–185, which emptied y 15–95 and crowded the mid-band. The right fix was to wrap the lines, not to move the blocks.
- **Improved:** the `P (0,0)` label now sits clear above the disc (in v1 it collided with the y = x chord), the stray rule under the title is gone, and no text leaves the frame.
