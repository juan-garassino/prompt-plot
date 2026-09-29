# Synth — millennium-p-vs-np after r01 ∥ r02 · 2026-09-29
route: designer
next round: r03 · parent: r02 (best so far: art 7.86/7 against r01's 5.71/4, science min tied at 7). Merged in from r01: its P / NP definitions **text only**, not its layout.

Ranking: r02 > r01. r01 reads as a textbook dendrogram (art legibility 4), and its crown weight is structural to the unrolled layout. r01 stays on disk as the faithful flavour and is not advanced.
Fabrication gate: not run (no double PASS). A2 below is gate item #1 when a vote comes.

## The instruction
Keep r02's dial, needle and 91 ticks exactly as drawn, and make this a type-and-sheet round only: re-set every word on the sheet as **one flush-left stack at x = 15 in the left column**, so the dial sits alone on the foot of the sheet and the thesis is stated in numbers where the eye lands after the title. Order, top to bottom:
1. The title.
2. The statement.
3. **The pair `43,658` / `91` at 4–5 mm caps**, each over a 1.8 mm label (`CLAUSE TESTS TO FIND (THIS SEARCH)` / `TO CHECK THE NEEDLE`). This is the plate's second-largest type.
4. The key in plain words: the disc is all 1,048,576 candidates, angle is exact share, blank paper is refuted; past ring 8 each thin line is one branch's deepest reach; each hour tick is 1/12 of the candidates, reached clockwise.
5. The instance line.
6. The finding method line, with the clause-test convention and "found at 11:37".
7. The honest-limit line: DPLL finds the same needle at node **82**; a shortcut for every case? open.
8. r01's P / NP definitions, compressed to two lines.

Everything that used to live in the two bottom corners moves into this stack. Compress words, not type size. If the stack cannot fit between the title and the dial's upper-left rim, the only other permitted home is the existing CHECKING caption band at the top right (x ≥ 110, above y 380). The upper-right quiet below it stays empty.

## Mandates to close
1. **A1.** One left-column stack. `43,658` and `91` sit within 25 mm of each other at cap ≥ 4 mm, and 43,658 is removed from any prose. No type below y = 260. Every block except the needle caption starts at x = 15, stays left of x = 88 and clears the rim and the 11 o'clock hour tick. The 6 o'clock tick is the only mark below y = 60.
2. **S1.** DPLL caption says **82** (the find, like 7,812), not 87. State the convention beside 43,658: "EACH CLAUSE TESTED AT ITS LAST VARIABLE".
3. **S2.** Key the dial in plain words, as in the instruction, item 4. Put r01's P / NP definitions on the sheet ("P: answers found in polynomial time. NP: answers checked in polynomial time, given a certificate. P is inside NP. Equal? Open."). Retire the jargon "HAIRLINE: EACH X8 SUB-TREE".
4. **S3.** Caption the hour ticks as equal shares of the candidates, reached clockwise, not equal time. Keep "11:37".
5. **A2.** The r03 gcode is emitted at feed 600 with `G4 P1.0` pen dwells, through a round-local render wrapper that sets `config.pen.feed_rate` / `pen_up_delay` / `pen_down_delay` (model it on `rounds/r02/render_truewidth.py`). Do not edit `promptplot/`. Recompute the per-layer minutes in HANDOFF from that gcode, and state the true stroke count per layer.

Deferred: A3 (clockwise-from-12 batching). The engine's colour reorder discards authored order, so it is an engine request, not a piece mandate.

## Preserve
- **The dial**: hub (148.5, 148.5), R 128, pitch 6.4 mm per variable. Exact tree to x8 in 0.3, 139 aggregate hairlines in 0.1 from r = 51.2, rim at ring 20. All §11 checks pass and must still pass byte-for-byte on the tree layers (layers 0, 1 and 3 geometry unchanged).
- **The red radius** at 348.628°. It runs out of the disc, collinear, to (97.83, 400.45), 4.55 mm under the top margin, with its 91 ticks at 1.35 mm pitch (41/36/14 lengths, 14 side-alternating groups).
- **The wedge** 348.63°→360° holds only the red.
- **The upper-right quiet** (≈ 167 × 105 mm, right of the needle, below the CHECKING caption). The art critic called it earned.
- **The registrations**: title cap line, needle tip and CHECKING cap line all at y ≈ 400; the CHECKING caption and the bit row at the top right beside the needle.
- **The layer order and swaps**: 0 hair → 1 black → 2 text → 3 red, 2 physical swaps. No node marks, no circles.
- **The truth lines**: "THIS SEARCH, NOT THE PROBLEM" and "M/N = 4.55".

## Do not
- Do not touch the tree, the red or the ticks to make room. Type moves; ink geometry does not.
- Do not shrink type below 1.8 mm caps to make it fit. Cut words instead.
- Do not put any type within 10 mm of the red line (S4; r02 measured 6.2 mm), within 14 mm of the rim, or inside the upper-right quiet.
- Do not bring back anything from r01's layout: no Petersen tree, no "NO HAS NO CERTIFICATE", no unrolled crown.
- Do not quote the DPLL exhaustive count (87) against a find count, or any number without its basis.
- Do not claim F600 in HANDOFF unless the gcode on disk carries it.
- Do not let TEXT grow past ≈ 1,000 strokes. This round moves type; it does not add a paragraph.
- Do not add "exponential", "≠" or "proves": the sheet shows this search, not the problem.
