# Synth — ising after r07 · 2026-09-29
route: **vote** (rule 6: round cap. The relaunch's 2 rounds were r05 ∥ r06 and r07. The r06 SYNTH declared r07 the last COOLING STRIP round.)
plate for the vote: **r07, seed 7**. `gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png` + `.gcode`. Seed sweep `_s3` / `_s13` on disk.
next round if Juan votes REWORK: **r08 · parent r07** (best so far). Run `pre: translator` first; see the Process note.

**Honest note for the vote.** Science PASSes r07 at 9/8/9: every printed number reproduces on the ink on 3 seeds, and the independent simulation on the identical lattice agrees band by band. Art FAILs it at avg 7.43, min 7. That is the best art score this piece has had (r05 6.71/5, r06 7.00/6), but it is still below the bar. No ising round has passed art. The three reasons are concrete and fixable:
- the crimson coast is a hairline beside 3-pass black;
- 49 clip crumbs;
- the transition band is squeezed into ≈ 23 % of the width.

This is a plate that tells the truth and reads at 3 m. It is not a finished poster.

**Ranking.**
1. **r07** (FAIL/PASS, art min 7).
2. **r05** (FAIL/PASS, art min 5). It keeps the wider ruled sea and the black continent that r07 lost.
3. **r06** SUNBURST flavour.
4. **r04**.

Flavours on disk: r06 SUNBURST, r03 COASTLINE.

## The instruction
For r08, only if REWORK. Keep r07's sheet, pens, chain and printed checks, and **give the transition its width**. Replace the linear thermometer with one printed, monotone x(T) (piecewise-linear is enough, and the ruler ticks must show it) under two constraints:
- the band 0.90–1.35 Tc takes ≥ 45 % of the field width;
- the cold sea is ≈ 78 mm wide again, as in r05. The hot tail is compressed, but its last 25 mm column still ends in bare paper by the fixed 13-site cut.

Re-sample the chain on that axis. Then redraw the coast so it is the heaviest line on the sheet, at ≥ the 3-pass black band (≈ 0.7 mm). Where that eats into the 0.85 mm clearance, the black steps back, never the red. Draw its seam edges.

Close every clipped hull along the clearance offset, or drop it whole, so no field stroke is shorter than 4 mm.

Remeasure every printed number on the new ink.

## Mandates to close (r08)
1. **A27, give the transition room.** The non-linear, printed x(T) described above.
   - 0.90–1.35 Tc covers ≥ 45 % of the field width.
   - The coast's lateral excursion is ≥ 45 mm.
   - No two distinct outlines in x 90–140 run parallel for > 10 mm at the 1.18 mm pitch.
   - The simulation runs on the same T(x), not the old one.
   - A28 is preserved: the ruled sea is ≈ 78 mm wide and a 3-pass continent is present on the plate seed.
2. **A25, the coast out-weighs everything it touches.**
   - Crimson is drawn at ≥ the 3-pass black weight (3–5 passes, or a wider pass gap).
   - Test: in x 70–110 no black stroke reads heavier than the red beside it.
   - The ≥ 0.85 mm clearance is measured from the red band's outer pass.
   - S16: draw the red seam edges (cols 48/49/51 today) and remove the floating red U at x 95.7–96.9, y 187.2.
3. **A26, zero crumbs.**
   - A stroke-length census of the field (y 36–189, x > 38) gives min ≥ 4 mm (r07 has 49 under 4 mm).
   - A coast-clipped hull closes along the clearance offset or is dropped whole.
   - A wrap-cut hull closes on the field edge line or is omitted.
   - The lone dash at (142.8, 188.4) goes.
4. **S14 + S15, two key-line fixes.**
   - Add `INK STOPS 0.85 MM SHORT OF RED` to the key. This keeps A19's clearance and makes the 1.00–1.10 rule deficit honest.
   - Change the FK line to `FK  ALIKE NEIGHBOURS BONDED WITH PROB 1-EXP(-2J/T)`.
5. **A18 / A14, re-prove the ending on the new axis.**
   - Last 25 mm column ≤ 3 outlines, plus a ≥ 25 × 60 mm mark-free block.
   - Band count and mean size strictly decrease past 1.15 Tc.
   - Per-sample column strictness stays **argued**. Report ensemble means, as r07 did.

Deferred: S2b (top rung P 0.40–0.51 in this geometry). The magnified 1.00–1.15 band should raise it. Check it, but it is not a mandate.

## Preserve (r07, named with where)
- **The ending.** x 240–287, y 36–110 is bare paper that the physics reached, with 2 grey outlines in the last column. The rule is printed as `BLANK DISORDER FINER THAN 13 SITES`.
- **The clean coast wall.** Crimson × black/grey crossings 0, minimum clearance 0.85 mm, 0 knots under 0.34 mm, and A9's 1.028 mm minimum between owners.
- **The footer grid.**
  - 5 lines at 4.0 mm pitch.
  - Col 1 flush at x 15, col 2 on the red 1.00 tick, col 3 on a ruler tick. If the axis changes, re-hang cols 2 and 3 on ticks.
  - Air measured: 5.4 / 3.05 / 2.8 / 2.65 mm (A20).
- **The CRITICAL spine.** Cap 18 mm, 3 passes, x 15–33, off-lattice, with the `A` at full weight (A21).
- **Printed checks computed from the ink.**
  - `AS DRAWN` against `ONSAGER M` on 0.70–0.80. Keep the band cold, and if the axis moves, recompute both numbers.
  - `MEAN` hull T.
  - The conditional `WEIGHT PEAKS AT TC COUNT PEAKS PAST IT` line.
- **Pens and plot contract (curator note).**
  - 0 black (rules, hulls ≥ 30 at 1/2/3 passes, type), 1 crimson (coast + 1.00 tick), 2 grey (hulls 13–29).
  - One layer per pen, order black → crimson → grey, minutes per layer stated.
  - No line shared between layers.
  - Travel ≤ 0.55× draw (r07 0.499×). Serpentine rules and closed loops starting at their lowest vertex.
- **HANDOFF.** `canon: science_poster`, `lineage: Nees, Schotter`, `declared: flat`.

## Do not
- **Do not** fix A19's crumbs by pulling the clearance back under 0.8 mm, or by moving or trimming the crimson.
- **Do not** make the axis non-linear without printing it. Every tick must sit on its value. No unprinted warp, and no axis that makes the cut vary with T.
- **Do not** narrow the ruled sea again (r07's 53 mm is the regression). The magnification comes from the hot tail.
- **Do not** add a 4th pen or a new mark type. Paper is the last plane.
- **Do not** import anything from r06 (SUNBURST) or r03 (COASTLINE).
- **Do not** print a number measured on the lattice rather than on the ink. Carry no r07 census into r08.

## Fabrication gate (r07, seed 7) — CLEAN
Run on 2026-09-29 against `gallery/studio/ising/trials/pp_ising_r07_iterate_v5.gcode`.
- `preview --stats --score`:
  - draw 12,366 mm, travel 6,172 mm (0.499×);
  - 1,128 pen cycles, 12,097 commands;
  - longest travel 158 mm;
  - bounds X 0–286.6, Y 0–197.2, clean on A4 landscape 297 × 210. The 0,0 is home/park; ink runs X 15–286.6, Y 13.05–197.2;
  - grade A, dominant issue efficiency (0.732).
- `plot layer --list`: color 0 has 947 strokes / 8,614 cmds · color 1 has 14 / 974 · color 2 has 167 / 2,509. 3 pens, one layer each. This matches HANDOFF and the science critic's parse.
- Draw time: ≈ 62 min at F600 / F2000 / 2 s per lift. By layer: black ≈ 47 min, crimson ≈ 3, grey ≈ 12.
- Floods: none. I cropped the densest zone (x 70–130, y 100–160) from the gcode and looked at it:
  - the 3-pass hulls hold their 0.35 mm pass gap;
  - there are no solid cells, and the crimson keeps clear;
  - the sub-4 mm stubs are visible there. They are an art defect (A26), not a fabrication fault, and each is just one extra lift.
- Nothing under `promptplot/` or `scripts/` changed during this piece's rounds (`git status`), so there was no regression run and no `make check` was needed.
- Seed: plate is seed 7, where the top rung is populated. Do not swap to s13, whose top rung is empty (S2b).

## Process
`dossier.md` and `encoding.md` are still missing. The r06 SYNTH made them a vote precondition. **I am overruling that for this vote**, because routing to the translator would also spawn a designer round past the cap, and the science critic's independent-simulation table (`critique-science.md`, r05 and r07) has served as the dossier on two PASSes. If Juan votes REWORK, relaunch ising with `pre: translator`. The translator writes `encoding.md` (with the non-linear x(T) of A27 as the channel map) and `dossier.md`, both from r07 HANDOFF + NOTES and the r07 science check table, before r08 is built.
