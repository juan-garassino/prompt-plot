# Art critique — millennium-bsd r02 · canon: ART DECO + Morellet system (thesis [A]) · 2026-09-29
render: gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.png (+ `_phys.png` true-width, `.gcode` measured)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | The fan and gold hub win at 3 m with no contest. The second act, "one line crosses zero once, in gold", fails at 3 m: the gold is 15.6 mm of a single 0.7 pass on a thin 104 mm curve, and the hub disc outshouts it. The notes block and the caption block both sit at the same mid weight and compete for third place with the ziggurat. |
| 2 | grid & alignment | 7 | Good: title, subtitle, notes and ziggurat share x = 15, and the title's right end (256.6) lands exactly on L's end (256.6). Floating: the caption block (x 226.0–279.3) is on no axis (not the 282 margin, not the crossing x 204.6). The fan's top crop (y = 365) misses the notes' top (361.8) by 3 mm, so it reads as a clip box, not a decision. |
| 3 | tension & asymmetry | 8 | Hub left of centre, the branch's two arms cropping top and bottom as working diagonals, L cantilevered into the empty mouth. Deco's monumentality without the symmetry trap, and the off-mirror hub breaks the egg's symmetry as the encoding promised. |
| 4 | negative space | 7 | The mouth of the "<" is a real, shaped void, and the math made it (no chord can enter). The rays-free zone left of the hub reads. The upper-left quadrant between the notes and the egg top is leftover. The ziggurat top (≈150) sits about 8 mm under the egg bottom (158.6), close enough to read as parked there. |
| 5 | craft for pen | 7 | The hub recedes cleanly: no ray enters the 6 mm disc, 11 half-rays stop at exactly 7.0 mm, and there is no spider-web. 3 swaps, 5 clean layers. But: the minimum centreline gap is 0.75 mm (two heavy 2-pass chords ending at the branch vertex, (131.2,197.3)/(131.1,202.5)), and about 23 pairs sit at 0.75–0.80 mm. At 2 × 0.3 nib that is ~0.2 mm of paper between them, so an ink knot is likely. The type layer is 1,499 lifts and ≈63 of 84 min. The two-digit ziggurat indices 10/20/30 are kerned into a blob. |
| 6 | concept legibility | 7 | Not a schematic. The textbook's 3-chord figure became one radial order of 60 chords, and "every line through one point, stopping on the curve" lands without reading. Weaknesses: (a) Morellet's rule is parity → *mark family*, but here odd/even is only inferable from where a ray ends, and note 3 has to say it; (b) the numbered notes 1–4 *explain* the plate, and the rubric says a caption only confirms; (c) L on a hairline axis is still a small function chart. |
| 7 | depth & dimensionality | 7 | Declared flat (Deco sunburst plus a flat-plane claim of 17°), and the declaration is honest. The three weight tiers give a near/far reading (heavy chords reach the hub, hairlines stop farther out). The flatness serves the plate but does no more than that. |

**avg 7.14 · min 7 · VERDICT: FAIL** (avg < 8)

## Reads at a glance
A black sunburst bursts from a gold disc, caught by a closed oval on the left and a huge open "<" on the right. A thin line sits in the mouth, and its gold is only visible from 1 m.

## Acceptance checks

Encoding §11 (measured from the gcode):
1. **ONE HUB, RECEDING: PASS.** All 76 chord strokes lie within 0.3 mm of (87.6, 226) (the only outlier is the s-axis, which is not a ray). The gold disc's r is 6.03, the nearest ray start is 7.0, and no ray enters. 11 half-rays sit on the 7 mm circle and later ones start at 8.1–13.5+ mm. 3 weights are present, and heavy ones reach closest (visible in the hub crop).
2. **TWO PIECES, ONE MIRROR: PASS.** The egg is closed at x 30.0–101.6 and y 158.57–241.43, symmetric about 200. The branch vertex is at 131.1. No curve, axis or label lies between them (chords only).
3. **LINES STOP ON THE CURVE: PASS.** Every far endpoint satisfies y²+y = x³−x (residual < 0.02) or sits at the crop (y = 15 / 365). The only exception is one heavy chord's 0.25 mm second-pass offset. Zero chord samples lie left of the hub outside the egg. The mouth holds only L, its axis, "S = 1" and the caption type.
4. **ONE CROSSING, NOT A TOUCH: PASS.** Starts at (152.6, 200). Minimum 195.36 (4.64 mm dip). Crosses at x = 205.09 (0.5 mm right of the spec'd 204.6) at 17.1°. Ends at (256.6, 219.84). Gold is the only colour on the right half. Only sub-0.1 mm hooks appear at the gold/black butt joints, with no visible corner.
5. **PLOTTABLE, LAYERED, TRUE: PASS (marginal).** The .gcode is present with layer order 0→1→2→3→4 and 3 physical swaps. Spacing is at the floor by construction but dips to 0.75 mm at one heavy pair (see craft). No type touches geometry: the nearest is 5.05 mm ("S = 1" to the gold) and the ziggurat is 11.5 mm from the nearest ray. The ziggurat runs 1→41 characters with a parabolic right edge at 82.8 ≤ 83.

AUTHORING §6 (reference = AI poster; judged as interpretation):
1. Main forms recognisable without fills: **PASS**. Egg, branch and fan all read in pure line.
2. Shadow lines follow the surface: **N/A**. The plate is flat with no shading, as declared.
3. Fine lines that are really two sides of one thick stroke: **PASS**. Heavy chords are out-and-back at 0.25 mm and merge under a 0.3 nib. They look striped only in the preview.
4. Blackest regions intended: **PARTIAL**. The densest zone is the wedge where heavy chords converge on the branch vertex (x 95–135, y 170–205). The pencil makes it, but it holds the 0.75 mm pair.
5. Labels readable at true width: **PASS with a nit**. The indices 10/20/30 blob together.
6. Thick pen knots: **PASS**. The gold disc's concentric fill is intended and the gold/black joints butt cleanly.
7. Excess tiny marks or long travels: **PARTIAL**. Type is 1,499 lifts and ≈75 % of plot time, and the explanatory notes block buys nothing visible.

Interpretation verdict: a real transposition. The reference's 3-chord textbook figure became a 60-chord Deco pencil, and the reference's decorative gold ribbon became gold that carries meaning. The L half has kept the reference's chart grammar, which is the one place the plate still reads as a figure.

## Biggest weakness
The plate has one act and a footnote. The fan is gallery-grade, but the second half of the one-glance statement, the gold crossing, reads only at arm's length. Nothing visual ties it to the fan: the mirror y = 200 that joins them is invisible on the curve side by rule, and the eye does not make the jump. Meanwhile two text blocks (the notes 1–4 and the caption) explain what the image should be doing by itself, and they eat three-quarters of the plot time.

## Mandates
1. **Make the gold crossing the second read at 3 m.** Draw the gold stretch s ∈ [0.85, 1.15] as 3 parallel gold passes at 0.35 mm offset (≈1.4 mm band), and drop the rest of L from pen 3 (0.5) to the 0.3 black. Test: in the full-page true-width png downscaled to 25 %, the gold stretch is visible as a distinct gold mark, and it is the heaviest stroke right of x = 140.
2. **Cut the numbered notes block 1–4** (x 15–77, y 322–362). At most one confirming clause may go into the subtitle line. Then run the upper rays to a crop line shared with the subtitle's clearance (one y used for both the ray crop and the top of the free zone), instead of the orphan y = 365. Test: no text lies between y = 250 and y = 375 on the left, and the ray tops end on a y that another element's edge also uses.
3. **Put the caption block on an axis, and fix the two craft nits.** The caption's left edge goes to x = 204.6 (the crossing vertical, shared with the centre of "S = 1") or its right edge to the 282 margin, whichever keeps it clear of the lower branch arm. Also: (a) trim the second pass of the two heavy chords that end at the branch vertex (131.2, 197.3) / (131.1, 202.5) so their centreline gap is ≥ 0.8 mm; (b) re-kern the ziggurat indices 10/20/30 so the two digits do not touch at 0.3 nib. Test: caption edge x ∈ {204.6, 282} ± 0.5; the gcode's minimum near-parallel gap is ≥ 0.80 mm; "10", "20" and "30" show a visible gap in the true-width crop.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | — | No LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists for millennium-bsd. HANDOFF has compare-to: none (new [A] plate; r01 is the sibling faithful thesis). There are no open A*/J* mandates to track. |

## Regressions vs compare-to
None assessable. This is the first render of thesis [A], and there is no parent render or § Keep list.
