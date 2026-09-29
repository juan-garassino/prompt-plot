# Synth — ising after r05 ∥ r06 · 2026-09-29
route: designer
next round: r07 · parent: **r05** (best so far). It wins the pair on verdict: science PASS 9/9/8 against r06's FAIL 7/7/8. r06's art is better (7.00/6 against 6.71/5), but the ledger ranks verdict first, and r06's science failures are on its own ink (merged cold dashes, a false tagline, halo-deleted dashes).

**Last round.** r07 is the 5th designer slot on this piece and the last on the COOLING STRIP encoding. After r07 the route is `vote`, pass or fail, with an honest note.

**r06 ranking:** kept on disk as the **SUNBURST** flavour (RG flow, Art Deco, `gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png`). It has the strongest hierarchy of any ising round and is worth its own future run. Its six mandates are parked in the ledger (A22–A24, S11–S13). **No merge:** the two sheets share no geometry. Nothing from r06 enters r07.

## The instruction
Keep r05's sheet exactly and give the Schotter dissolve its ending: **the right edge of the sheet must be where heat becomes finer than the cut, so the last plane, bare cream paper, arrives by physics.** r05 stops the thermometer at 1.80 Tc, where free FK clusters of 13 or more sites are still common (~31 per band), so the grey runs as uniform wallpaper to the margin.

1. **First lever: extend the hot end of the one linear T ramp** (same lattice width, same fixed cut 13, same rungs, same pens). Re-sample, and measure the smallest T_max at which three things hold on seeds 7, 3 and 13:
   - the 20 mm column hull counts (grey + black) strictly decrease from T ≈ 1.3 to the edge;
   - the last column carries ≤ 3 marks;
   - a mark-free rectangle ≥ 25 × 60 mm exists there.
2. **Fallback, only if the extension squeezes the cold sea + coast below ~45 mm of width:** keep 0.70–1.80 and raise the single fixed hull cut to the smallest value that passes the same test. Print it in the key, and re-derive the rung table and `BLANK DISORDER FINER THAN N SITES`.
3. **Take the footer's air from the field height.** Shorten the field (no smaller type) to make the room for A20.
4. **Stop every black and grey stroke at the crimson coast.**
5. **Add the two stranger lines** (FK unpacked, and weight vs count peaking apart), measured on the new ink.

## Mandates to close
1. **A18: the grey fades to paper.** 20 mm column counts strictly decrease from x ≈ 180 to the right edge. The last column holds ≤ 3 marks and a mark-free block ≥ 25 × 60 mm. The rule is fixed and printed in the key, never thinned by hand. A14's band count and mean size must still strictly decrease (recompute the bands if the T axis changes, and print the new bounds).
2. **A19: the coast is where everything stops.**
   - Zero crimson crossings by black or grey strokes (r05 has 46 black and 5 grey).
   - Sea rules end ≥ 0.8 mm short of the coast. The rows to check are y 101.8, 119.5, 140.7 and 161.9 at x 94–99.
   - No grey hull straddles the coast (x 100–108, y 120–135).
   - No 3-pass knot on a 1-site neck: keep ≥ 0.35 mm between passes there, or drop the neck to 1 pass. Example: the top-edge cluster at x ≈ 150, y ≈ 185.
   - Fix this by trimming the black and grey ends. Never move or delete a coast edge.
3. **A20: footer and ruler air, on the grid.**
   - ≥ 5 mm bare paper between the field bottom and the first footer cap line.
   - The last footer baseline sits ≥ 3 mm above the bottom margin.
   - Ruler labels sit ≥ 2 mm below the top margin.
   - The right footer column's left edge sits exactly under a ruler tick.
   - `TC IS A PLACE` has ≥ 2.5 mm clear above it.
4. **S9: two stranger lines.**
   - `FK  SPINS BONDED WITH PROB 1-EXP(-2/T)`, or an equivalent that unpacks FK.
   - A line saying weight peaks at Tc while count peaks past it. Remeasure the numbers on r07's ink before printing them.
5. **A2 (plot economy, curator note): travel ≤ 0.6× draw on seed 7, with margin** (r05 was 0.592×).
   - Order the strokes so no layer has a 248 mm nearest-neighbour tail jump. A local 2-opt in the piece is fine.
   - State the plot order and minutes per layer in HANDOFF.

Deferred:
- **A21** (the `A` diagonal weight in CRITICAL): fix it only if it costs nothing.
- **S10** (seed 3 stray rule steps): only matters if s3 becomes the plate.

## Preserve
- **The crimson coast.** One component, 3 passes at ±0.15 mm, wrapping at the seam, mean ≈ 1.03 Tc, 0 edges shared with black or grey. The only other crimson is the taller 1.00 tick and its label.
- **The ruled sea.** Rules lie on lattice lines, one per 3rd row, strictly inside the held FK cluster, and overlap no wall. The printed `AS DRAWN` value is computed from the ink rows, with the band named. r05's 0.977 against Onsager 0.969 must be recomputed if the axis changes.
- **The rung ladder.** Grey 13–29 at 1 pass; black 30–49 / 50–154 / ≥ 155 at 1/2/3 passes, grown inward at 0.35 mm, with A15 at ≈ 2.7×. A9 keeps ≥ 0.8 mm between distinct owners on all three seeds. Shared edges take the heavier rung.
- **The CRITICAL spine.** Cap 18 mm, 3 passes, x 15–33, off the lattice. The coldest band is fully ruled (S7).
- **The thermometer ruler.** Linear and exact to 1e-4, with the red, taller 1.00 tick. If T_max changes, re-tick it; add no furniture.
- **The type.** One strip under the field, three columns on the grid, tiers kept (A16).
- **Pens.** 0 black, then 1 crimson, then 2 grey, each with one meaning. Clean layers with no shared line. Every stroke is a safe batch point (curator note: no pen cap, one clean layer per meaningful pen).
- **Engine and chain.** The seed-7 chain, the FK draw, the left wall held up, the top/bottom wrap and the 1.178 mm display pitch stay. Only the ramp's T_max may change, under instruction 1.
- **HANDOFF.** `canon: science_poster`, `lineage: Nees, Schotter`, `declared: flat`.

## Do not
- **Do not** vary the cut with T, thin at random, or delete hulls by hand to make the fade. The fade is the physics at one printed rule.
- **Do not** add a 4th pen or a new mark type (dots, dashes, touches) for the hot edge. Paper is the last plane.
- **Do not** shrink type to find footer room. Shorten the field.
- **Do not** resolve coast crossings by trimming or rerouting the crimson.
- **Do not** import anything from r06: no fan, no gold, no Deco furniture. SUNBURST is its own flavour.
- **Do not** print a number measured on the lattice rather than the ink, or keep r05's census/coast numbers if the axis moved.

## Fabrication gate
Not run: science PASSed but art FAILed, so the double pass is not met. For the record, here are r05's pre-gate stats (`preview --stats --score`, `plot layer --list`):
- bounds X 0–286.6, Y 0–197.8, clean on A4 landscape;
- layers: 0 black 895 strokes / 8,907 cmds · 1 crimson 11 / 1,236 · 2 grey 245 / 3,726;
- draw 16.58 m, travel 9.82 m, 1,151 lifts, longest travel 248 mm;
- grade A, dominant issue: efficiency (0.66).

**Vote precondition:** a translator pass writes `studio/ising/encoding.md` + `dossier.md` from the r07 HANDOFF and the science check table. It has been missing for four rounds.
