# Art critique — attention-weaving r04 · canon: deco (inferred; HANDOFF declares no canon and no `lineage:` line) · 2026-09-28
render: ~/Downloads/pp_attention_weaving_mirror-drain_v13.png (24x30 portrait, cream, 5 pens)

## Scores

| dim | score | why |
|---|---|---|
| 1 hierarchy | 7 | Wall + slit + hill hold the eye at 3 m, and SUMS TO ONE is a clear second. The upper storm and the lower green/gold fan are the same density, so neither half leads. |
| 2 grid & alignment | 6 | Type, wall and margin reeds sit on the frame. The `Z = AV` (60,157) and `V` (83,133) labels float in open paper, tied to nothing. `K` is jammed into the top-right corner. `SOFTMAX` rides the wall's right arm, away from the hill. |
| 3 tension & asymmetry | 7 | The green fan swinging down-right against the flush-left type is a real working diagonal. The slit sits near the centre (77–130 on a 10–230 field). |
| 4 negative space | 6 | The lower-left void now has a shape (the edge of the fan). The upper half runs edge to edge with no quiet zone. Gold arc tips stop about 5 mm above the `E` of ONE, which reads as collision, not decision. Two green lanes leave through the bottom frame right next to the corner (x 211/220). |
| 5 craft for pen | 6 | 5 pens against a ≤4 bar. Lane pitch 0.90 mm is barely above the floor. Double-passed heavy strokes carry no stated meaning: 3 blue arcs (y≈280, y≈220, the x≈95 riser) and 1 gold arc (x 125–150, y 105–135). Blue arcs have hard polyline elbows at x 35–95, y 210–232. Near the slit (x 85–135, y 130–180) the gold is chopped into dashes under 3 mm, so it reads as a dashed line, not over/under. Giant type is built from separated parallel strokes: `U` and `M` read striped, and `N` has uneven weight. Travel (17.3 m) is still longer than draw (16.1 m). |
| 6 concept legibility | 5 | "Everything drains through one hole, and the hole sums to one" does land, and the title gives the twist. But the vocabulary is a physics figure: field lines, dashed equipotentials, a density profile, and a thin cumulative curve ending in a dot marked `1.000`, which is an axis plot sitting on the aperture. The brief's weave and braid are gone. V crosses Z instead of being spun into it. |
| 7 depth & dimensionality | 5 | Over/under gaps give one layer of depth. Everything else is flat line on paper and the flatness is not declared. The dashed ellipses are meant to sit behind, but they touch the green lanes instead of stopping at them. |

avg **6.0** · min **5** · **VERDICT: FAIL**

## Reads at a glance
A red-and-blue storm of lines draining through a slot in a black wall, pouring out as a green fan to the lower right, over giant type that says SUMS TO ONE.

## Acceptance checks (BRIEF "What must be TRUE"; no encoding.md)
- Everything passes through the waist, strands in = strands out: **PARTIAL**. The footer says 38 in / 38 out and all Q/K reach the slit. But about 10 K arcs start in open paper (right ends between x 185–215, y 195–265), and every V arc starts and ends in open paper.
- Over/under is real: **PASS** at Q×K (alternating gaps). **PARTIAL** at V×Z, where gold is shredded into dashes near the slit.
- Softmax normalises (peaked, sums to one): **PASS**. One dominant hump, a shoulder and a tail. The cumulative ends at 1.000.
- V joins after the waist: **FAIL**. V is below the wall (order correct), but it never joins Z. It is a crossing family of arcs, and Z leaves the slit already green.
- Braid carries more strands than Q or K alone: **PASS on count** (38 vs about 19). **FAIL on braid**: it is a fan with no twist.
- Q·Kᵀ label, loom-reed ticks at each bundle's mouth: **FAIL / PARTIAL**. There is no Q·Kᵀ label. There are no reeds where V and K are born.

AUTHORING §6 (reference in play; judged as an interpretation, "potential flow through one slit"):
1. Main forms recognisable without colour: **PASS**. Q straight, K arcs, Z fan, and V arcs are distinguishable by geometry.
2. Secondary lines follow the form: **PASS**. The dashed ellipses follow the field.
3. Fine lines that are really two sides of one thick stroke: **PARTIAL**. The giant type's parallel strokes show as stripes (`U`, `M`).
4. Blackest regions intended: **PARTIAL**. The hill and wall are intended. The heavy blue and gold arcs are not explained.
5. Labels readable at pen width: **PARTIAL**. `K` is crushed into the corner. `SOFTMAX` touches the dashed ellipse and the blue tails.
6. Thick-pen knots at corners: **PARTIAL**. Hill ends at the slit jambs; `M`/`N` apexes.
7. Long empty travels or tiny marks with no benefit: **FAIL**. Travel is longer than draw, and gold near the slit is broken into sub-3 mm crumbs.

## Biggest weakness
The lower half now copies the top's grammar, but its strands are not strands. The gold V arcs and about 10 blue K arcs start and stop in open paper, and near the slit V is chopped into crumbs. So the "everything is continuous and forced through one throat" claim is undercut exactly where the eye checks it. On top of that, a plotted cumulative curve sits inside the aperture and turns the throat into a chart.

## Mandates
1. **V becomes continuous strands born at a reed.** Every gold strand starts at a left-margin tick (x = 10, y 95–175), with the `V` label placed at that mouth. It runs into the green fan with at most one gap per green crossing. No gold dash shorter than 3 mm anywhere in x 85–135, y 130–180. Test: zero gold ends in open paper; no sub-3 mm gold crumbs.
2. **Clear the aperture of chart furniture and unexplained weight.** Delete the thin black cumulative S-curve that runs from (78,184) to (130,206) through every strand inside the profile box, along with its end dot and `1.000` label; state Σa = 1 in the footer only. Single-pass the 3 heavy blue arcs and the heavy gold arc. Test: inside the slit box there are only strands and the hill, and the principal crimson vertical is the only doubled coloured line on the sheet.
3. **K strands reach the frame and lose their elbows.** Every blue arc's free right end (currently about 10 ending between x 185–215, y 195–265) extends to a right-margin tick at x = 230. The hard polyline corners at x 35–95, y 210–232 become tangent-continuous turns. Test: zero blue ends inside the frame; no visible corner on any blue strand at 30 cm.

## Follow-up on open mandates
There is no `LEDGER.md` for this slug. The open items tracked are Juan's REWORK note (FEEDBACK.md, on aperture_v9) and DESCRIPTION.md's "If only iterating" list.

| id | status | evidence |
|---|---|---|
| J1 bring the bottom up to the top | PARTIAL | The 80 mm parallel run-out and the bend tangle are gone. The bottom is now a radiating green fan with a crossing gold family, the same grammar as the top. But gold is shredded near the slit and born mid-air, so the bottom is still visibly the weaker half. |
| J2 smoother softmax profile, partition exact | FIXED | One smooth two-humped hill with no plateaus and no knot discs. Footer 38 in / 38 out; cumulative ends at 1.000. |
| D1 smooth area-preserving curve, labelled cumulative | FIXED | See J2. The `1.000` label is restored (this critique now asks for the curve to go; see mandate 2). |
| D2 replace cable with a fan of 38 streamlines, remove bend tangle | FIXED | The green lanes fan from the slit to the right and bottom frames with no chevron crossings. |
| D3 V as spiral arcs crossing every green lane at ≥45° with over/under | PARTIAL | The crossing angles are about 60–90° with gaps. But the arcs start and end in open paper, and near the slit the gaps reduce gold to crumbs. |

DESCRIPTION § Keep (aperture v19):
- Whole upper half untouched: **still true**. It is identical to v19, including its kinks and double-passed arcs.
- Wall as a 5-pass rule with one hole: **still true**.
- Exact partition, 38/38, Σa = 1: **still true** (per footer and profile).
- Principal crimson vertical, single and loud: **still true**.
- Giant `SUMS / TO ONE` flush-left: **still true**, but the `E` is now grazed by gold arc tips.

## Regressions vs compare-to (aperture_v19)
- **Type block now collides with the drawing.** Gold arc tips end about 5 mm above the `E` of ONE (x 150–160, y 60). In v19 the type had more than 25 mm of clear paper above it.
- **Labels lost their anchors.** In v19, `Z = AV` sat on the TO ONE baseline at the right, and `V` sat at the gold mouth on the left margin. Both now float mid-sheet (60,157) and (83,133), tied to no edge or strand.
- **Bottom-right corner crowded.** Two green lanes now exit through the bottom frame within about 20 mm of the corner. v19 terminated every lane on the right edge.
- **Pitch tightened** from 0.95 to 0.90 mm at the slit, closer to the 0.8 floor.
- Improvement for the record: travel went from 20.2 m to 17.3 m, and footer leading is now even.
