# Synth — millennium-bsd after r03 · 2026-09-29
route: designer
next round: r04 · parent: **r02 on the ranking key (best so far), built as a MERGE.** Start from r03's `piece.py`, because it carries every r03 fix. Restore r02's closed-oval egg continuity, which is the regressed element.

Why this parent: r03 scores art 7.14/6 · sci 8/8/7, and r02 scores 7.14/7 · 7/7/7. The verdicts tie (FAIL/FAIL), and art min decides it, so rule 5 (regression) applies. The regression is local: the egg's yield beside the hub turned into beaded 1–2 mm fragments (art craft 7 → 6). Everything else r03 did is a confirmed fix and must carry over:
- S1, the ln 10 caption;
- S2(b) and S2(c), no false contacts and the tangent starting at 7 mm;
- S3, the cause, the foil and the status;
- A1, the gold band;
- A2's cut notes and series caption;
- A3(a), the 0.80 floor.

Rule 2 check: nothing is NOT FIXED twice yet. **S2(a) is PARTIAL for the first time (53/62) and A3(b) has failed once. If either misses again in r04, the route goes to translator.** Plateau check: best-so-far has been unchanged for 1 round, not 2. Even so, this round's lead move is a composition move (moving the column).

## The instruction
Make the second act one vertical unit and close the oval again. Move the whole right-hand text column off the bottom-right corner and hang it from the gold crossing: its left edge goes on the crossing vertical x = 204.6, its top sits ≤ 8 mm under `S = 1`, and it keeps ≥ 10 mm clear of the lower arm. That way the gold band, `S = 1` and the words about L read as one unit, and the bottom-right corner opens. Pay for the one sentence the sheet is missing by merging it into the column's head, not by adding lines. The column's first lines should say that the gold disc is P = (0,0), that every ray is a line through P, and that every ray end is a rational point nP. Fold `E: Y²+Y = X³−X · CREMONA 37A1 · RANK 1` into that sentence, and keep the total at ≤ 22 lines (aim for 20). At the hub, take out the beads. Give each side of the egg exactly one clean square stop where it yields to the tangent, and delete every egg piece shorter than 5 mm between x 70 and 100. The notch stubs that stay must read as the chord's own line crossing the curve, not as egg fragments. Everything else stays byte-identical to r03.

## Mandates to close
1. **A5 (the regression; preserve r02's closed oval).** Delete the egg fragments at x 74.4–79.1 / y 233.3–236.2 and at x 97.1–97.7 / y 212.9–214.1, and any egg stroke under 5 mm between x 70 and 100. Each side gets one square stop ≥ 0.8 mm from the tangent.
   - Test: a 4× true-width crop of x 60–100, y 205–245 has no egg stroke under 5 mm and no bead.
   - S2(c) must still hold: the tangent starts at 7.00 mm, and no non-own point is < 0.5 mm off it.
   - If deleting a fragment un-marks a notch-stub point, keep the stub (the chord's own line, 2 mm, on layers 0/1) and drop only the egg piece.
2. **A7 (the composition move, including A2's remainder).**
   - The column's left edge is on x = 204.6 ± 0.5, and its top is ≤ 8 mm below the `S = 1` label.
   - It is ≥ 10 mm clear of the lower arm, measured perpendicular to the arm (report the minimum).
   - There is no type in x > 215, y < 80.
   - The column has ≤ 22 lines, and every S3 sentence survives verbatim: the cause, `A CURVE WITH FINITELY MANY POINTS (11A1) HAS L(1) = 0.2538, NOT ZERO.`, the status line, and the bridge `L'(E,1) = 0.30600 = 5.98692 × 0.05111`.
   - If 22 lines cannot clear the arm at 10 mm, drop the bridge's `(Ш = 1, C = 1, NO TORSION)` line first and say so.
   - The fan's upper crop y is moved onto a *visible* edge: the cap line of the statement's 2nd line, or the title's baseline minus one lead, whichever lies on existing type. Name it in NOTES.
3. **S5 (state the rule).** The column's head carries ≤ 2 lines, e.g. `P = (0,0) IS THE GOLD POINT. EVERY RAY IS A LINE THROUGH P; EACH RAY END IS A RATIONAL POINT nP.`
   - This defines the `NP` in the ziggurat caption and `HEIGHT OF P`.
   - Optional: `L(E,S)` at 1.6 mm caps near L's right end (256.6, 219.8), ≥ 3 mm off the curve.
   - Do **not** put it in the left y 250–375 zone.
4. **S2(a) (the second attempt; translator if missed).** Either reach ≥ 60/62 marked oval points, or state the 7-point merge in type. The science critic accepts either.
   - Preferred: one clause in the S5 head or the ziggurat caption, e.g. `SEVEN nP NEAR P AND AT THE OVAL'S TIP LIE CLOSER THAN THE PEN CAN PART.`
   - It counts inside the ≤ 22-line budget.
   - Do not try to force stubs under the 0.8 floor.
5. **S6 + A3(b) (the craft nits, one line each).**
   - (S6) Trim chord 8's stub at −9P to t ∈ [−26.4, −24.4]. Today it runs (63.59, 241.76) → (67.18, 239.40), 3.30 mm past the egg.
   - (A3b) Re-kern ziggurat indices 10, 20 and 30 to a visible glyph gap ≥ 0.5 mm at the 0.3 nib. The +0.35 kern did not do it. Measure the ink gap in a 4× true-width crop of x 15–25, y 20–70 and report the number.

Deferred: none. S1, S3, A1 and A3(a) are fixed. A2 is folded into A7.

## Preserve (from r03 unless noted; must not regress)
- **The fan (r02 → r03).** 60 exact group-law chords through the gold hub (87.6, 226), in tiers heavy 1–9 ×2 / medium 10–24 / fine 25–60. The hub LOD r = max(7, 0.815/sin Δθ). 0 false contacts (S2b). The tangent starts at r = 7.00 and runs to −2P (139.57, 174.00).
- **The curve.** Egg x ≤ 101.59, y 158.57–241.43 (mid 200.00). Branch vertex 131.13. **Zero ink in the 29.5 mm gap.** One 52 mm/unit scale. **The egg reads CLOSED at 1 m. That is r02's quality, and A5 restores it.**
- **L and the gold.**
  - L runs (152.6, 200) → (256.6, 219.84), with a 4.64 mm dip.
  - The gold band is 2 passes at ±0.35 mm over s 0.85–1.15 at 17.0°, with no overlap, and it is the heaviest mark right of x = 140.
  - The rest of L is on black 0.3, layer 1.
  - Gold appears only as P's 6 rings and the band.
- **The words, all true (science r03).**
  - The two-line statement with the cause, top-left.
  - The ziggurat caption `N² × 0.0222 (= HEIGHT 0.0511 / LN 10)`.
  - The 11a1 foil, the status line verbatim, and the series caption top-right (right edge 282, cap line on the statement's cap line).
  - The ziggurat x(nP) n = 1..30, 30/30 exact, right edge ≤ 83.
- **Plot discipline.**
  - 5 layers 0 → 4, 3 physical swaps, text on its own layer.
  - Gcode near-parallel floor ≥ 0.80 with the 0.015 guard.
  - Every stroke is batchable.
  - Per-layer minutes come from the `plot plate --dry-run` table.
- The lineage line (Morellet, 1961, parity rule taken, not look) and "declared flat" stay in HANDOFF.

## Do not
- Do not add a new text block anywhere. S5 and S2(a) are paid for inside the column's ≤ 22 lines (and one clause may go in the ziggurat caption). The art critic's hierarchy complaint is that the words outweigh L. Moving the column is not permission to grow it.
- Do not "close" the oval by running the egg line back under the tangent at < 0.8 mm, and do not bridge the yield with dots or dashes. One square stop per side is the mark.
- Do not draw the mirror y = 200 through the curve side or the gap, and do not add a gold connector between the hub and the band, to make "the flow" visible. The column hanging from the crossing *is* the flow move this round (§9.3, §9.5).
- Do not move the column into x < 204.1, onto the L curve, or closer than 3 mm to the gold band.
- Do not quote a total ETA only. Quote per-layer minutes from `.venv/bin/python -m promptplot plot plate <gcode> --layers 0,1,2,3,4 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`. The text layer (≈ 66 min) must not grow.
- Do not edit anything under `promptplot/`.

## Fabrication gate
**Not run.** Both critics FAIL r03 (rule 1 is not reached). At the r04 double pass the gate checks:
- `preview --stats --score` bounds at A3 portrait, margin 15;
- `plot layer --list`: 5 layers / 3 swaps, with stroke counts ≈ 62 / 41 / ≤ 1 510 / ≤ 5 / 7;
- `plot plate --dry-run` minutes per layer;
- true-width crops of the hub (x 60–105, y 200–245), the gold band, and the moved column over the lower arm;
- the gcode near-parallel floor ≥ 0.80 (`rounds/r03/gapcheck.py`).

Open question for Juan (unchanged, not a mandate): the plate is A3-only. Confirm that Leo can take A3 after the holidays, or queue the encoding §10 A5 re-run (K = 30, ziggurat n ≤ 20).
