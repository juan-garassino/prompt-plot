# Art critique — attention-weaving r08 · canon: Psychedelic (declared flat; lineage Wes Wilson, Fillmore 1966) · 2026-09-29
render: gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.png

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | Many crimson masses of similar weight spread over the block: row 1 `TM` (y≈283), row 5 `MA S N` (y≈230), row 8 3-ring `A` (x 50–80, y 183–203), row 13 2-ring `S` (x 10–35, y 128–150). The one 3-ring glyph (Q11·k5 = 0.190) is barely larger than the 2-ring S and does not read first. |
| 2 | grid & alignment | 7 | Flush-left x=10 and a hard justified right edge x≈168 on all 22 lines. The key line's k0–k15 labels sit under their letters. The caption's last line shares the k-label baseline (y≈16). The caption top (y≈92) aligns to nothing. |
| 3 | tension & asymmetry | 6 | Letter block left, caption low right. That is asymmetric but static: a tall rectangle plus a small rectangle, with nothing reaching across the gutter. The warp creates tension inside the block, not across the sheet. |
| 4 | negative space | 5 | A 60 × 190 mm blank column (x 170–230, y 100–290) is about 27 % of the drawable area. It is the leftover of a 158 mm measure on a 220 mm frame, not a shaped void. The Psychedelic canon says to fill every void. Inside the block there is no leading: adjacent rows' `E` arms stack as double rules 0.7–1 mm apart at x 160–168. |
| 5 | craft for pen | 6 | 3 pens with a clean light → dark order (good). Ring offsets hold 0.9 mm on the tall lines, but they collapse on the squashed ones. The inner ring of `O` at (27, 157) is a solid crimson sliver, and the middle arm of the 2-ring `E` at (163, ≈72) inks solid. The `D` counter at (40–60, 130–145) tangles. There are 30,785 commands and 23.1 m of draw (about 40 min of ink at F600 before lifts), much of it in green slivers under 3 mm wide that read as scribble. |
| 6 | concept legibility | 7 | This is not a schematic, a figure or an illustration. It is type as data, in the LeWitt / Wilson sense. "Every row sums to one, so every line is justified" is a real transposition, and the hard right edge makes it visible. But the 17-line caption *explains* the mapping (letter = key, rings = whole 1/16s, height = 4 − H, slerp) rather than confirming it. Without the caption, "red letters swell" reads, but "attention" does not, and there is no weaving on a plate titled weaving. |
| 7 | depth & dimensionality | 7 | Flatness is declared and fits the canon. The ring tubes emboss the heavy letters, and crimson/green complementaries at near-equal value do buzz. The warp is a vertical slerp shear only, so there are no near-parallel families at a few degrees' offset (`vibrate`) and no true moiré. |

**avg 6.29 · min 5 · VERDICT: FAIL**

## Reads at a glance
At 3 m: a tall wall of melting red-and-green lettering that repeats "SOFTMAX SUMS TO ONE" 22 times, with some red letters swelling into ringed tubes, a flush right edge, and a small text column and an empty strip on the right.

## Acceptance checks
The encoding §11 checks were written for Revision 1 of the aperture/weave thesis (Deco). r08 implements none of that encoding, and its HANDOFF canon (Psychedelic) contradicts encoding §1 (Deco). Every check therefore fails as written:
1. Weft closed, no crumbs — **FAIL** (there is no gold weft on the plate).
2. Cloth is the matrix, the rule is checkable — **FAIL** (no cloth, no picks, no 1/16 tick. The 352 cells exist as letters, not crossings).
3. Throat restored (A19) — **FAIL** (no wall, slit or hill).
4. Every thread closes, Q_i = Z_i — **FAIL** (no threads).
5. Void and text discipline — **FAIL** (the crop x 10–90, y 100–150 is solid lettering. No `Z = AV`).

AUTHORING §6 (reference = the braid poster, judged as an interpretation):
1. Main forms recognisable without colour — **PASS** (letterforms read in both inks).
2. Shadow lines follow the surface — **PASS / n.a.** (ring offsets follow each glyph skeleton).
3. Fine lines as the two sides of one thick stroke — **PASS** (intended: the rings *are* the offset tube).
4. Blackest regions intended — **FAIL** (the solid crimson slivers in the squashed `O` (27, 157) and the `E` (163, ≈72) are accidental).
5. Labels readable at pen width — **PASS** (k0–k15 and the caption are clear).
6. Thicker pen knots — **FAIL** (the collapsed inner rings on short lines will knot with a 0.5 mm+ nib).
7. Long travels or tiny marks — **PARTIAL** (travel 9.3 m of 23.1 m is fine, but hundreds of < 3 mm green slivers carry little).

As an interpretation of the reference: it keeps none of it. There are no threads, no over/under, no Q/K/V/Z. It answers "sums to one", not "attention as weaving".

## Biggest weakness
The plate is a strong idea set at the wrong scale for its sheet. A 158 mm justified block is parked on a 220 mm frame, which leaves an unshaped dead column. A 17-line caption then has to explain what the lettering should make self-evident. The Psychedelic canon (fill the field, one warp through everything) is only half-committed: the lettering fills its column but not the page, and the heaviest cell (Q11·k5) does not dominate.

## Mandates
1. **Take the measure to the frame and cut the caption to a footer.**
   - Justify all 22 lines to x 10–230 (220 mm, not 158 mm).
   - Move the text column into ≤ 3 lines under the key line, in y 10–24, stating facts that confirm (`A = SOFTMAX(QKᵀ/T) · 22 × 16 · SEED 7 · EVERY LINE = 1`), never the mapping.
   - Test: every line's final `E` ends at x ≈ 230. The crop x 170–230, y 30–290 is lettering. No text block sits beside the letters.
2. **Give every line air and never collapse a ring.**
   - Insert ≥ 1.5 mm of leading between adjacent lines.
   - Where a cell is too short or narrow for floor(16a) rings at 0.9 mm, the rings must stop before they meet. Drop the innermost ring rather than let it merge into the skeleton.
   - Test: at the right edge x 160–168, no two `E` arms from adjacent rows are < 1.5 mm apart. The `O` at (27, 157) and the `E` at (163, ≈72) show open white inside every ring. No solid crimson anywhere at 4× zoom.
3. **Make Q11·k5 the one loud thing.**
   - The 3-ring `A` of Q11's line must be the single largest crimson mass on the sheet: bounding-box area ≥ 1.5 × the next largest glyph (today the 2-ring `S` at x 10–35, y 128–150).
   - Get this through the line-height and width mapping, stated in the footer. Do not add a second pen or bolding.
   - Test: at 3 m the eye lands on that `A` first. Cover it, and the sheet loses its peak.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| J1 (bring bottom up to top) | NOT FIXED | Moot, not answered. Both halves are gone, including the top Juan praised. |
| J2 (smoother softmax profile, exact partition) | NOT FIXED | No profile exists. The partition survives only as line justification, and ring counts floor(16a) are a new quantised staircase. |
| A2 / A7 (V as one sweeping closed family) | NOT FIXED | No V strands on the plate. |
| A6 / A21 (shaped left-middle void, x 10–90 y 100–150 bare) | REGRESSED | The crop is dense lettering. The only void is an unshaped right column. |
| A11 (labels anchored, ≥ 2 mm clear; `Z = AV`, `SOFTMAX`) | PARTIAL | k-labels and caption are clear of all strands. `Z = AV` is absent, and `SOFTMAX` is now the subject, not a label. |
| A13 (giant type craft) | NOT FIXED | Giant `SUMS / TO ONE` was dropped (now a ~5 mm caption heading), not repaired. The hairline key line is uniform. |
| A14 (travel > draw) | FIXED | 9.3 m travel vs 23.1 m draw (0.40). |
| A15 (reads as a physics figure; braid gone) | PARTIAL | No longer a figure: type-as-data. But the braid and any weaving are still absent. |
| A16 (≤ 4 pens) | FIXED | 3 pens. |
| A19 (throat ≤ 52 mm, no shelf) | NOT FIXED | No throat. |
| A20 (no text in upper field; Q11 bold registers) | FIXED | No caption in the field. No doubled strand. |
| A22 (reed mouths ≥ 3 mm apart) | FIXED | Moot: no reeds or ticks. |

## Regressions vs compare-to (r06, pp_attention_weaving_iterate_v16.png)
- **The storm above the wall** (Q streamlines × K spirals, wide-angle over/under, falling into one slit) is deleted. This was Juan's explicitly praised half and DESCRIPTION's must-preserve.
- **The wall as a 5-pass rule with one hole** is deleted, and with it the storm/silence split.
- **The principal query as one scarce bold vertical** is gone. Q11 is now one line among 22.
- **Giant `SUMS / TO ONE` flush-left (type as mass)** is reduced to a caption heading about 5 mm tall.
- The left-middle void is filled, and a larger unshaped void appears on the right.
- Draw rose from 14.2 to 23.1 m (+62 %) and commands from 15,693 to 30,785.
- The link to the reference (threads, braid, weaving) is severed entirely.

**DESCRIPTION § Keep:** storm — no longer true. Wall with one hole — no longer true. Exact partition — true in a new form (22/22 lines justified to one measure; the 38 in / 38 out count is gone). Principal query straight bold line — no longer true. Giant flush-left type — no longer true.
