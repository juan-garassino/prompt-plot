# Art critique — attention-weaving r07 · canon: Art Deco, declared flat (lineage Albers, *Black-White-Gold I*) · 2026-09-29
render: `gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.png` (measured from `gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.gcode`, crops re-rendered at physical nib widths)

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 6 | The wall and the storm read first. The throat is still a narrow 10 mm spike on a raised shelf. `SUMS / TO ONE` (150 × 32 mm of ~1.1 mm black strokes) is a bigger black mass than the throat and competes with it at 3 m. The cloth is a third, weak voice |
| 2 grid & alignment | 7 | Flush-left type at x = 10, footer leading even, the right-frame exit ticks form a clean column at 3.7 mm pitch. Turns stand at uneven heights (upper y 162–169, lower 4–8 mm below lane 0), so the cloth's edges are ragged |
| 3 tension & asymmetry | 7 | A centred crown (Deco allows it) against the drain sweeping down-right and the bare left L. It works, but the lower-right drain is compact and ends early, so the diagonal is weaker than in the storm |
| 4 negative space | 7 | The left L (x 10–90, y 100–183) is clean and has an edge: the lead-in at y 86 is its floor. The quadrant x 150–230, y 30–75 is dead paper holding only `Z = AV` and the lead-out, which reads as leftover rather than shaped |
| 5 craft for pen | 7 | Gold min piece is 5.01 mm (53 pieces). Reed mouths are ≥ 3.2 mm apart, exit ticks 3.5 mm. Travel is 7.0 m against 13.2 m of draw. Strands stop above the hill band with no ink-on-ink. Against: 5 inks and 6 layers exceed the ≤ 4 bar (declared). The leftmost crimson lands on the wall arm at (76.2, 187.3), outside the slit |
| 6 concept legibility | 6 | Storm → reed → cloth reads as an order, not a schematic. But the gold does not read as ONE thread or as cloth. Most of each pick is hidden (pick 1 runs bare from y 101.7 to 134.8), so the weft shows as ~50 short gold dashes plus 15 paper-clip hairpins. At 3 m it reads as gold staples on green hairlines, not Albers' gold weave. The hill on its shelf reads as a spectrum peak on a baseline |
| 7 depth (flat declared) | 7 | Over/under is the only depth cue and it carries data at both levels: storm Q-over-K gaps, cloth gold-over-green gaps. It is consistent and readable at 30 cm |

**avg 6.71 · min 6 · VERDICT: FAIL**

## Reads at a glance
A fan of red and blue lines combs down into a notch in a heavy black bar with a small spike. Below it, green lines swing to the lower right, pinned by scattered gold staples. `SUMS TO ONE` is big and bold at the lower left.

## Acceptance checks (encoding §11)
1. **Weft closed, no crumbs: PASS (with drift).**
   - One thread: lead-in tick on the left frame, 16 picks, 15 turns (8 upper, 7 lower), lead-out tick on the right frame.
   - 0 gold ends in open paper. Min gold piece 5.01 mm.
   - Drift: the lead-in tick is at y 86.0 (spec ≈ 97) and the lead-out at y 68.3 (spec ≈ 50).
2. **Cloth is the matrix: FAIL.**
   - Bold Z11 is under gold at 4 consecutive picks (x ≈ 179–194). PASS.
   - No gold in the tight bundle under the slit. PASS.
   - **The hill stands above the 1/16 tick (y 189.77) only over x 98.4–108.4 (top pass).** That is bins 7 and 8 fully and bins 6 and 9 partially. Bin 9's mean height (189.31) sits *below* the tick, and its K lands at y 190.8, 1 mm above it. The "exactly 4 bins" count cannot be read by eye.
3. **Throat restored: FAIL.**
   - Slit 52.0 mm. PASS.
   - The profile does not leave the wall from zero height. There is a vertical step 183.6 → 186.9–187.9 at both jambs and a ~3.3 mm raised shelf across the whole slit (§9.4 violated).
   - The bold vertical meets the summit. PASS.
4. **Every thread closes: PARTIAL.**
   - 16 blue end in 16 different bins. PASS.
   - 22/22 green exits ticked, ≥ 3.5 mm apart, `11` marks the bold one. PASS.
   - Reed mouths ≥ 3.2 mm apart, 38 ticks for 38 strands. PASS.
   - **The leftmost crimson ends at x 76.2 on the left wall arm, outside the slit (jamb at 77.5).** One Q does not pass the reed.
   - Q_i = Z_i to 0.5 mm cannot be verified from the sheet, because the crimsons stop above the hill.
5. **Void and text: PASS.**
   - Crop x 10–90, y 100–150: 0 marks.
   - Above the wall only `Q`, `K` and `SOFTMAX`, and `SOFTMAX` is on the open arm.
   - `Z = AV` sits in open paper on the TO ONE baseline.
   - The bold strand registers as one line.

## Biggest weakness
The cloth, which is the whole reason for Revision 1, does not read as cloth.
- The merge rule hides the weft for long runs, so each pick survives only as a few 5–20 mm gold sticks.
- The turns are loose hairpins of mixed height standing outside the selvages.
- The cloth fills only the band y 77–170 × x 135–230, so it cannot answer the storm (J1).

Second, the throat still carries the shelf and the jamb steps that A19 and §9.4 forbid.

## Mandates
1. **Throat: kill the shelf, make the four bins readable.**
   - The black profile must leave the wall top (y 183.6) at x = 77.5 and x = 129.5 at zero height. No vertical step, and no black run at y ≈ 187 anywhere in the slit.
   - The hill must stand visibly above the 1/16 tick across the full span of bins 6–9, x 97.0–110.0. Today it is x 98.4–108.4, and bin 9's mean sits 0.46 mm below the tick.
   - Pull the leftmost crimson (now ending at (76.2, 187.3) on the wall arm) inside the slit.
   - Test: crop x 72–135, y 182–206 shows one curve that rises from both jamb corners, and the tick-level chord spans ≥ 13 mm.
2. **The selvages must read as a woven edge, not paper clips.**
   - All 15 turns use one radius (half the local pick spacing).
   - Each turn's outermost point stays ≤ 2.5 mm outside its selvage lane. Today the upper loops reach y 162–169, 3–10 mm above lane 21, and the lower hairpins hang 4–8 mm below lane 0.
   - Test: the upper turn apexes lie on one smooth curve parallel to lane 21, and the lower apexes on one curve parallel to lane 0.
3. **Give the cloth the encoded size so it can answer the storm (J1).**
   - Spread the lane exits from today's y 77.5–154.8 (3.7 mm pitch) to the encoded y 56–172 (≈ 5.5 mm pitch). The cloth then fills x 135–230 × y 56–172, and the dead quadrant x 150–230, y 30–75 shrinks to the `Z = AV` band.
   - Put the weft ends back at the encoded ticks: lead-in y ≈ 97, lead-out y ≈ 50.
   - Test: gold draw ≥ 1.5 m (today 1.1 m). The longest hidden run on any pick is ≤ 25 mm (pick 1 is 33 mm today).

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| J1 | PARTIAL | The bottom now has its own grammar: an orthogonal weave with real over/under. But it reads as sparse gold staples on a band ~40 % of the storm's width, not as a woven fan equal to the top. Only Juan closes it |
| J2 | PARTIAL | The profile is smooth, with no knots or bins drawn. But the raised shelf and the two vertical jamb steps still echo the ziggurat base |
| A7 | FIXED | Under R1 the V is one closed weft. Both ends are on frame ticks, 0 ends in open paper, min piece 5.01 mm, and there is no gold in the tight bundle |
| A11 | FIXED | `Z = AV` sits in open paper on the TO ONE baseline. `SOFTMAX` is on the open wall arm, not in a notch |
| A13 | FIXED | `SUMS / TO ONE` has uniform ~1.1 mm filled strokes, and the `M`/`N` diagonals match the stems (crop x 10–150, y 40–78) |
| A14 | FIXED | Travel is 7.04 m against 13.23 m of draw (0.53, down from 1.04) |
| A15 | argued / PARTIAL | Over/under now carries the matrix below the wall, which is real interpenetration. It still does not hold beside Albers, because the gold reads as dashes (mandate 2, mandate 3) |
| A16 | argued | 5 inks, 6 layers (the text layer was added). Declared in encoding §6 |
| A19 | PARTIAL | Slit 52.0 mm and the hill spans it. **The shelf and the jamb steps remain** (step to y ≈ 187 at x 77.5 and x 129.5). Carried into mandate 1 |
| A20 | FIXED | The Q11 caption is gone from the storm. The bold Q11 registers as one line |
| A21 | FIXED | Crop x 10–90, y 100–150 holds 0 marks |
| A22 | FIXED | Top mouths ≥ 3.2 mm apart, right mouths ≥ 3.5 mm. 38 ticks for 38 strands, none shared |

## Regressions vs compare-to (r06 v16)
- **The lower half lost mass and gesture.** r06's gold was wrong (left-entering parallels), but it filled y 100–175 edge to edge and swept. r07's cloth is a smaller patch at x 135–230, y 77–170. The quadrant x 150–230, y 30–75 is now dead paper, where r06 had green run-outs.
- **The lane fan is shorter.** r06's green ran all the way to y ≈ 28 at the right frame. r07's lanes exit only between y 77.5 and 154.8, so the drain's down-right diagonal is weaker.
- The shelf and jamb steps carried over unchanged from r06. This is not new, but R3 promised to remove them.
- The leftmost Q still lands on the wall corner outside the slit. It did in r06 too.
- **DESCRIPTION § Keep:**
  - The upper half (storm): still true, unthinned.
  - The wall as a 5-pass rule with one hole: true, and the hole is the narrowest it has been since r04.
  - Exact partition: the footer states it, and the hill area is not measurable by eye. But the tick shows bin 9 below 1/16, which contradicts a = 0.0661 visually.
  - Principal query as one straight bold crimson: true.
  - Giant flush-left type as mass: true, and better built (A13).
