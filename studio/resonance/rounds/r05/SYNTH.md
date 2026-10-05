# Synth — resonance after r04 ∥ r05 (parallel) · 2026-09-29
route: designer
next round: r06 · parent: **r10** (= r01/v13 byte for byte plus Juan's continuous dots). Chosen by Juan's verdict and the regression rule, not by score. MERGE: named stroke machinery comes from r05, nothing comes from r04.

Ranking: r04 (art 5.43/4 · sci 7/7/6) > r05 (4.71/3 · 5/4/5) on scores, but both FAIL and both
REGRESS Juan's binding notes. r04 deletes the whole apparatus (J2) and draws dashes (J1). r05 cuts
the scatter dots, stipple caps and crest fade (J2) and thins the dots (J1). Juan, after seeing both
reworks: "the original was much more beautiful — we just needed the dot lines to be more
continuous, not to remove the waves". So the parent is r10.

r04 is kept on disk as the `one-field` flavour, a candidate for its own slug. r05 v7 is kept as
the "economy" flavour.

Lineage (carry r05's; distinct from the siblings' Csuri / LeWitt / Riley): **Thomas Young,
*Lectures on Natural Philosophy* (1807), Plate XX Fig. 267.** It is the natural-philosophy
engraving plate, and it lends the INTERFERING order: two concentric crest families, where the
result exists only where they cross.

Fabrication gate: not a double PASS, so it was not run as a gate. Baseline read on r10's gcode
(`preview --stats --score`, `plot layer --list`) for r06 to beat:
- 6,092 pen cycles; per layer 0 crimson 1,215 · 1 blue 1,238 · 2 gold 571 · 3 green 286 · 4 violet 666 · 5 black 2,116.
- 10.99 m draw, 12.89 m travel (117 %), longest travel 285 mm. Bounds X 0–196.3, Y 0–280.3.
- ≈ 240 min on Leo (2 s per cycle, F600 draw, F2000 travel, 2 min per swap).

Juan accepts the length. The waste is the part to remove.

## The instruction
Fork r10 and keep v13's composition, every element and all six pens exactly where they are.
Change only how marks are made and how the sheet streams: this round makes Juan's
continuous-dot plate plottable as a batched Leo job.

1. **Move r10's geometry onto r05's stroke IR.** Every helper returns
   `Stroke(pts, pen, kind)`, so the whole sheet exists as geometry before G-code is written.
   With that IR in place, apply only r05's non-destructive sheet passes:
   - label halos (clip dots out of each label box + 0.9 mm);
   - node keep-outs (0.55 mm);
   - "the carrier IS the axis" (no co-incident duplicate ink);
   - fused multi-pass type;
   - round solid dots for every `_fdot` (touch, loop or spiral by radius, never a `-` tick);
   - the ∂L stack at 3 mm clear air.
2. **Draw dots in two classes.** DOTTED LINES (fans, droplines, leaders, guides, rails, ghost
   lanes, halo ellipses, backward runs) keep r10's 1.0 mm end-anchored round dots, laid in
   run order. TEXTURES (the crest fade-out m 22–51 that forms the stipple caps, and the
   spoke/scatter field) are not lines. They keep v13's mark count and positions, and each mark
   becomes one round dot. Do not re-pitch them to 1 mm: that is the mud in r10.
3. **Stream it well.** Order every colour layer reversal-aware and spatially contiguous. Stream
   light→dark: gold, blue, green, crimson, violet, black. In NOTES, give per-layer batches as
   `--strokes S:E` ranges of ≤ ~300 cycles, each a contiguous region of the sheet.

## Mandates to close
1. **J1** — continuous dots. Test on the gcode:
   - on an isolated leader (the ∂L/∂Q rail), the same-pen dot nearest-neighbour median is 0.9–1.1 mm, with a dot on both ends;
   - every dot is one fixed-size round mark (0 micro-dashes of 0.3–1.2 mm on any dotted line);
   - where two same-pen dotted paths run closer than 2 mm (the paired Q/K fans), dots are phase-locked across the pair so they read as parallel dotted lines, not interleaved noise;
   - judge at 0.35 mm nib width.
2. **J2** — keep the original. Test:
   - element-for-element diff against v13: all 5+5+3 packet rows, 1 Z, 2+3 MoE lanes, Y, 6 softmax peaks + 3 ghosts, the scatter/spoke field (same count ±5 %), stipple caps, 3 halo ellipses per source, every leader and arrowhead, and every label;
   - all at v13 positions (≤ 1 mm moves, except the ∂L stack re-spacing).
3. **A13** — what the continuous dot exposed:
   - stipple caps at v13 density with 0 flood at 4× crop;
   - each halo ellipse drawn as its own arc, ending on the ellipse (no flat horizontal dotted chords at y ≈ 141 / 191, no vertical stub on the right ellipse — the reference draws whole ellipses; stop them at the crest keep-out ON the curve);
   - 0 `-` tick dots anywhere.
4. **A4** — batching and waste. Test:
   - no consecutive in-layer travel > 80 mm (r10: 285 mm);
   - 0 dots within 0.3 mm of other same-pen ink, 0 inside a label box, 0 on a node;
   - no two identical/co-incident paths;
   - total travel ≤ draw + (dot count × 1.0 mm);
   - NOTES table: cycles, draw, travel and minutes per layer and in total (Leo model above), the layer order with why, and the batch ranges.

   Pen cycles may exceed v13's 3,471. That is accepted, provided every cycle is a visible dot.
5. **A5 + S1a** — collisions and wiring without deleting anything:
   - gold V rows 2/3 carriers no longer run through each other (occlude the lower packet under the upper envelope, or re-pitch ≤ 2 mm within the V block);
   - no fan, dropline or return curve crosses the word `router` (halo);
   - the three Z taps (x ≈ 67/74/80) each join their ∂L return curve as one continuous dotted path;
   - every softmax→ link and V's connector terminates ON Z's axis (x 28.6–96.9, y ≈ 75), not on Y (164, 77), a ghost lane or mid-air (y 85.1);
   - keep them gold (S1b: the lead's position, gold = a_j·V_j into Z; the science critic rules in pass 2).

Deferred (ledger): A9 (declare flat in HANDOFF, one line — do it), A12 margins (r07), S3b |A|-sized dots (r07). Blocked by J2 until Juan rules: S1c Z/Y scale, S2 key counts, S3a hero ellipse stretch.

## Preserve
- **v13's whole composition** (r01/r10). This covers:
  - the title with its rule and dot (v 0.06);
  - Q (u 0.09–0.36) and K (u 0.64–0.91) packet blocks, with guides and node columns;
  - `Q·Kᵀ/√d_k` at (0.50, 0.28–0.31);
  - the hero at (0.40/0.60, 0.44): crests m 1–21 solid, d = 35 L, `_Guard` 0.82 mm / 25°, the two diamond-lens clusters on the midline, axis and end circles;
  - the three dotted halo ellipses per source;
  - softmax with 6 peaks + 3 ghosts at v 0.62;
  - V, Z = AV, MoE with 2 solid + 3 ghost lanes, and Y;
  - the ∂L band, arrowheads included.
- **The funnel:** ten crimson + ten blue dotted fans converging on the hero's upper rim. At r10's 1 mm pitch they now read as drawn curves; keep that.
- **Six pens, six meanings:** Q crimson, K blue, V goldenrod, Z green, MoE/Y/∂L-MoE violet, black for the field, softmax, type and ∂L/∂A. This is the family grammar shared with resonance-backprop and resonance-ffn.
- **From r05, critic-confirmed:** the ∂L stack at a 10 mm pitch with 3 mm clear air; the light→dark layer order, each pen one contiguous layer.

## Do not
- Do not cut, thin or replace anything to save plot time (r05's mistake). Do not delete the scatter dots, stipple caps, crest fade, halos or leaders.
- Do not widen the dot pitch per role (r05: 2.8–4.4 mm), and do not use dashes or hairlines for dotted lines (r04).
- Do not extend the solid crests to m = 28 or add a crosshatch lens: it made a toothed seam in r05.
- Do not move, rescale or de-symmetrise the composition (A1/A7/A8 are dropped under J2). Do not "fix" the science by changing Z's size, the element counts or the hero's stretch: those wait for Juan.
- Do not re-pitch the stipple caps or field to 1 mm (r10's mud).
- Do not stream in pen-index order without stating why, and do not leave greedy stragglers that cross the sheet.
