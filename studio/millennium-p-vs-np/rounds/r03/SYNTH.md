# Synth — millennium-p-vs-np after r03 · 2026-09-29
route: designer
next round: r04 (round 4 of 5) · parent: **r03** (latest, argued). Best so far by the ranking rule is still r02 (art min 7 against r03's 6).

**Why r03 is the parent.** r03 fell on one dimension only: craft, 7 → 6. That fall comes from geometry r03 did not touch. r02's red ticks and hairlines have the same start points; r03 raised the dwell from 0.2 s to 1 s, the correct plot setting (A2), and that exposed the defect. Forking r02 would throw away A1, A2, S1, S3 and S4, all closed and confirmed by the critics. So the regressed element is named as mandate A5 instead of being reverted.

Scores r03: art 7.71/6 · sci 7/9/8 · FAIL (art craft 6; science truth 7 for one false caption).
Fabrication gate: not run (no double PASS). r03 gcode baseline: 155 / 226 / 1,013 / 92 strokes, ≈ 24 / 20 / 61 / 6 min, ≈ 111 min at F600 / G4 P1, 0 pen-up G1.
Route check:
- Rule 2 (translator): not triggered. S2 is NOT FIXED once, in r03. If its residue is not closed in r04, the next route is translator.
- Rule 4 (plateau): not triggered. r02 has been best for one round; one more round without a new best makes r05 a composition move by rule.
- Rule 6 (cap): r05 is the last designer round.

## The instruction
Leave the dial, needle and 91 ticks exactly where they are. Change only which end the pen lands on, and rebuild the left column as a tighter, cheaper two-level stack.

**1. Pen direction.** The pen lands on the rooted end of every line and lifts at the free end:
- each red tick is drawn outward from the needle axis;
- each 0.1 hairline is drawn outward from ring 8 (r = 51.2 mm);
- each black refutation spoke is drawn from its parent side toward its dead end.

The engine's `optimize_stroke_order` reorders strokes but never reverses them, so the direction you author is the direction Leo draws.

**2. The column.**
- Set `43,658` flush-left at x 15 and `91` flush-right at x 87 on ONE baseline, the find-versus-check contrast read left to right as encoding §2 promises. Each numeral has its own short label on a shared label baseline, and the clause-test convention stays beside 43,658.
- Below the pair, rewrite the 1.8 mm prose so it says MORE with FEWER strokes:
  - the key keeps the disc = 1,048,576 candidates, angle = exact share, and hour tick = 1/12 of the candidates, not of time;
  - blank = refuted, but the sliver past the red was never searched;
  - a thin line touching the rim is a false needle that failed only the last clause (69 before the red);
  - instance and method merge into two lines: uf20-03, m/n 4.55, backtracking false-first, 7,812 nodes, found at 11:37, DPLL node 82;
  - one honest-limit line;
  - P / NP ends with "NP: checked in polynomial time, given a certificate (the red). P is inside NP. Equal? Open."
- Cut repetition, not content, and never shrink type below 1.8 mm caps.

**Word budget (a guide; the tests below are binding):** at most 13 caption lines below the numeral labels.

## Mandates to close
1. **A5, pen down at the rooted end** (the regressed element).
   - Red: the first point of each tick is ≤ 0.05 mm from the needle axis, 91/91 (r03: 46/91).
   - Hairlines: the first point of each is at r = 51.2 mm, 139/139 (r03: 70/139).
   - Black: every layer-1 stroke that ends in a refutation (including the 7 ring-6 ends) starts on its parent side.
   - Keep F600 and `G4 P1`.
   - Prove it: extend `audit.py` to count first points per layer and print the counts in NOTES. `_phys.png` must show no bead at any tick tip or line end.
2. **S6, the wedge is unsearched, not refuted.** "BLANK PAPER IS REFUTED" is false for 348.628° → 360°, which holds 33,122 candidates (3.2 %) the search never visited. The drawn search refutes 1,015,453. Reword it, and keep the wedge empty.
3. **S2 residue, finish P / NP.** Add "given a certificate (the red)" and "P is inside NP. Equal? Open." This is S2's second attempt: if it is not fixed in r04, the route is translator.
4. **S7, name the false needles.** Add one key line saying that a thin line at the rim is a complete candidate that failed only the last clause check, with 69 before the needle. That is dossier §2's "indistinguishable until checked".
5. **A6, the pair side by side and the column shorter and cheaper.**
   - Numeral baselines are equal to ± 0.5 mm, caps ≥ 4 mm, and `91`'s ink right edge is ≤ x 88.
   - The column foot is at y ≥ 290 (r03: 276.5).
   - TEXT is ≤ 950 strokes and ≤ 50 min, read off the r04 gcode (r03: 1,013 strokes, 61.3 min).
   - S6, S7 and S2 must fit inside this budget.

Deferred:
- A3: clockwise-from-12 batching (engine keep-order flag).
- A7: the title's 5-pass re-ink (minor; gate item).

## Preserve
- **Dial geometry, byte-identical as point sets on pens 0, 1 and 3:**
  - hub (148.5, 148.5), R 128, 6.4 mm per variable;
  - the exact tree to x8 at 0.3, and 139 aggregate hairlines at 0.1 from r 51.2;
  - the rim at ring 20, and 12 hour ticks at r 129.5–133.5.

  Only stroke DIRECTION may change. `audit.py` must show the reversed strokes are the same segments.
- **The red.** 348.628°, collinear out to (97.83, 400.45). 91 ticks at 1.35 mm pitch with lengths 41/36/14, in 14 side-alternating groups, in clause order.
- **Empty space.** The wedge 348.63° → 360° holds only the red. The upper-right quiet [115, 282] × [285, 385] has no non-red ink.
- **r03's sheet moves.** One flush-left axis at x 15. Both bottom corners clear, and no type below the rim tangent. Title cap line, needle tip and CHECKING cap line registered at y ≈ 400. CHECKING caption at x 115 (type → red ≥ 10 mm; r03 measured 10.74). The single-stroke sans `I`.
- **Plot settings.** F600 on every G1, `G4 P1` dwells, via the round-local render wrapper (copy `rounds/r03/render_plot.py`). Layers in order 0 hair → 1 black → 2 text → 3 red, with 2 physical swaps. No node circles.
- **Truth lines.** "THIS SEARCH, NOT THE PROBLEM", "M/N = 4.55", "DPLL … NODE 82", "FOUND AT 11:37", "EACH CLAUSE TESTED AT ITS LAST VARIABLE", and the hour-tick "NOT EQUAL TIME" meaning.
- **Lineage.** Manfred Mohr, *Cubic Limit* (1973–75) and the 1977 hypercube works. Name it in NOTES and HANDOFF.

## Do not
- Do not reverse a stroke by editing `promptplot/` or the optimizer. Author the direction in the piece.
- Do not fix the beads by shortening the dwell. `G4 P1` is Leo's requirement (memory: slow-feeds-long-pen-dwells).
- Do not move the dial, the red or any tick to make room for type.
- Do not add a paragraph to host the three new science facts. Each one replaces words that are already there. TEXT must go down, not up.
- Do not put type within 10 mm of the red, within 14 mm of the rim, inside the upper-right quiet, or below the rim tangent.
- Do not quote the DPLL exhaustive count (87), the whole-tree 45,088, or any count without its basis.
- Do not write "exponential", "≠" or "proves". The sheet shows this search, not the problem.
