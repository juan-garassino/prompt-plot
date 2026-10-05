# Art critique — millennium-p-vs-np r03 [A] · canon: RADIAL DATA-VIZ (5) on the SWISS series sheet (3), a stated hybrid · 2026-09-29
render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3_phys.png (+ `_v3.png`; gcode `_v3.gcode` parsed for every measurement below)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 8 | The levels are clear. First the red needle, then the dial mass, then the 10 mm title, then the numerals 43,658 and 91 at about 5 mm. The 0.3 core against the 0.1 corona gives the dial a dark heart. What holds it back is the 1.8 mm prose under the numerals: 6 blocks and 17 lines, all at one size, so it reads as a grey wall. |
| 2 | grid & alignment | 8 | One flush-left column at x = 15 whose right edge is x ≤ 87.3. The needle caption's cap line matches the title's (y ≈ 400). The column foot (y 276.5) clears the rim arc. Nothing floats. |
| 3 | tension & asymmetry | 8 | The centred dial is declared and forced by the width. The lopsided content carries the tension: 12 black rim contacts on the left against 1 on the right, and a carved crescent of paper inside the right rim. The needle's 11.4° lean into the empty upper right does too. |
| 4 | negative space | 8 | Both bottom corners are now clear, and the dial sits alone at the foot. The upper right (about 167 × 105 mm) is quiet, with only the 3-line needle caption at its top edge. The refuted void and the wedge after the needle are bare paper. |
| 5 | craft for pen | **6** | Spacing is clean: aggregates ≥ 1.25 mm, red tick pitch 1.345–1.357, red-to-type 10.74 mm, 2 swaps, F600. The problem is where the pen goes down. Every stroke opens with `G4 P1` (1.0 s), and the serpentine ordering starts **45 of 91 red ticks at their free tip** and **69 of 139 hairlines at their dead end**. On paper that puts a 0.5 red bead on the tick tips and a fine bead on the refutation ends, exactly where §4 says "no mark at the end". The round's own plot preview shows a bead on every tick tip, so the checking rule reads as a row of pins. Minor: the title is 5 passes at 0.18 mm pitch with a 0.3 nib. It fuses on paper, but it re-inks the same spot. |
| 6 | concept legibility | 8 | Not a schematic and not a figure. The order reads: a halving tree swept clockwise, most of it stopping, one red radius escaping as a notched rule. The counts pair 43,658 / 91 now makes the find-versus-check contrast in numbers. |
| 7 | depth & dimensionality | 8 | Flatness is declared (the measure coordinate). Depth is carried by three honest weights (0.3 exact, 0.1 aggregate, 0.5 red), and the needle leaves the disc's plane. |

avg **7.71** · min **6** · **VERDICT: FAIL** (craft < 7, avg < 8)

## Reads at a glance
At 3 m: a spiky black wheel at the foot of the sheet, one notched red needle drawn out of it up to the title, and a column of type with two big numbers on the left.

## Acceptance checks (encoding §11, [A])
1. **ONE RED RADIUS: PASS.** The red crosses the rim at (123.26, 273.99), which is 348.63°. Its first fork swings to 9 o'clock, then climbs clockwise. It runs straight to (97.83, 400.45), 4.55 mm under the top margin. There is 1 path + 91 ticks and no other red.
2. **THE CARVING: PASS.** No line ends inside ring 5. There are exactly 7 ring-6 ends, at 194.1 / 216.6 / 239.1 / 261.6 / 284.1 / 306.6 / 329.1°. Rim contacts: 13 black + the red = 14. Refuted areas are bare paper.
3. **LOPSIDED, AND THE WEDGE: PASS.** The black rim contacts are at 169.5, 227.1, 235.5, 249.6, 258.0, 280.5, 303.0, 317.1, 325.5, 332.6, 334.0, 336.8 and 339.6°. Only 169.5° is in the right half. There are 0 black points in 348.7°→360° past ring 4.
4. **CHECKING IS THE RED, AND IT COUNTS: FAIL (on paper).** The counts pass: 91 ticks, lengths 1.5 / 2.75 / 4.0 = 41 / 36 / 14, 14 side-alternating groups, even pitch. 43,658 vs 91 is captioned, and the method is named. The "no dot" clause fails. 45 ticks take their 1 s pen-down dwell at the free tip, and the plot preview shows beaded tips on the whole comb.
5. **PLOTTABLE AND CLEAN: PASS.** Layers go 0→1→2→3 with 2 swaps, F600 / G4 P1 throughout (0 × F2000). Minimum spacing is ≥ 0.8 mm. All aggregates start at ring 8, and the key says what a thin line is. It does not say *why* the weight changes at ring 8, which is borderline. No type is inside r 133.5.

AUTHORING §6 (the reference is an interpretation brief; the dial re-reads its START→SOLUTION tree):
1. Forms read without fills: PASS.
2. Shadow lines follow the surface: n/a.
3. No double-edged strokes: PASS.
4. The blackest region is intended: PASS (rings 5–8, node for node).
5. Labels at true width: PASS.
6. Thick-pen knots: **FAIL**. 1 s red dwells at the tick tips.
7. Empty travel / tiny marks: PARTIAL. Black-layer travel is 2.74 m for about 2.7 m of ink, and TEXT is 1,013 strokes (61 of 111 min).

The reference's FINDING / CHECKING pairing is now honoured in the numerals.

## Biggest weakness
Fixing the dwells to 1.0 s made stroke direction matter, and nobody re-ordered the strokes. Half the red ticks and half the refutation hairlines now start with a one-second pen-down at the end that must "simply stop". The checking comb, the plate's second read, becomes a row of beaded pins. The encoding forbids those dots, and they are the one mark a viewer at 30 cm will count.

## Mandates
1. **Pen down at the root, never at the free end.**
   - Every red tick draws outward from the needle. Test: its first point is ≤ 0.05 mm from the needle axis, 91/91 (now 46/91).
   - Every 0.1 hairline draws outward from ring 8. Test: its first point is at r = 51.2 mm, 139/139 (now 70/139).
   - Keep F600 / G4 P1.
   - Test: the gcode audit, plus the plot preview shows no bead at any tick tip or any hairline end.
2. **Set the counts side by side, as §2 promises.**
   - Put `43,658` and `91` on ONE shared baseline (≈ y 350). `43,658` sits flush-left at x = 15. `91` sits flush-right at x = 87, with the gap between them empty.
   - Each numeral keeps its own 1.8 mm label beneath it, on one shared label baseline.
   - Test: the numeral baselines are equal to ± 0.5 mm, the cap height is ≥ 4 mm, and nothing crosses x = 88.
3. **Shorten the column below the numerals.**
   - Cut the 1.8 mm key and method text from 17 lines to ≤ 13. Merge the SATLIB and BACKTRACKING blocks into one 2-line instance block. Keep the science-mandated content (S1–S3 wording), but drop the repetition.
   - Test: the column foot is at y ≥ 290 (now 276.5), and the TEXT layer is ≤ 950 strokes and ≤ 50 min (now 1,013 and 61.3 min, more than the whole drawing).

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A1 | FIXED | `43,658` and `91` are flush-left at x = 15, baselines ≈ 356 and 339 (17 mm apart), caps ≈ 5 mm, each labelled. Both corner blocks are moved into the stack. There is no type below y 276.5, the column x-max is 87.3, and the bottom corners are clear. |
| A2 | FIXED, with side effect | 0 × F2000/F1500. 2,973 × `G4 P1`. HANDOFF minutes are recomputed (≈ 111 min). The 1 s dwell now lands on free ends; see mandate 1 and Regressions. |
| A3 | NOT FIXED (deferred engine item) | The first black stroke starts at 223.6°, not in [0, 22.5). Black-layer travel is 2.74 m (r02 2.52 m). |
| S1 | FIXED (text, science to confirm) | "DPLL FINDS IT AT NODE 82." and "EACH CLAUSE TESTED AT ITS LAST VARIABLE" are present. |
| S2 | PARTIAL (science to confirm) | The disc key line and the "THIN LINE: ONE BRANCH'S DEEPEST REACH" line are present. The P/NP definitions are shortened, and "P IS INSIDE NP. EQUAL? OPEN." is absent. |
| S3 | FIXED (text) | "HOUR TICK: 1/12 OF THE CANDIDATES, REACHED CLOCKWISE, NOT EQUAL TIME." |
| S4 | FIXED | Red-to-type minimum is 10.74 mm (was 6.2). |

No FEEDBACK.md or DESCRIPTION.md exists for this slug, so there are no J* mandates or Keep items to check.

## Regressions vs compare-to (r02 `_abstract_v3_phys.png`)
- **Beaded free ends (new, caused by the A2 fix).** In r02, 0.2 s dwells at the same serpentine start points were harmless. At 1.0 s, 45 red tick tips and 69 hairline dead-ends take a pen-down bead.
- **TEXT grew from 910 → 1,013 strokes and from 48 → 61 min.** Type is now 55 % of plot time, which breaks the ledger's "TEXT ≤ about 1,000 strokes" baseline.
- **Black-layer travel went from 2.52 → 2.74 m** (A3 still open).
- The title geometry is identical to r02: 14 strokes at a 0.18 mm 5-pass. Its striped look in the r03 preview comes from the new preview renderer, not a geometry regression.
- Pens 0, 1 and 3 geometry is unchanged, and every §11 geometry check still holds.
