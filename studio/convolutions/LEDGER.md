# Ledger — convolutions
**Best so far:** r04 — art 6.14/5 · sci 9/8/7 — `~/Downloads/pp_convolutions_iterate_v9.png` (best *critiqued* round; both critics FAIL. It beats r03 on every ranking key: art min 5 > 4, sci min 7 > 5, art avg 6.14 > 5.57. r01 `gallery/studio/convolutions/current/pp_convolutions_v1.png` is still the unscored craft benchmark: it was never run through the critic pair. Its Keep items are the regression bar where the new layout has not deliberately retired them)
**Route:** designer
**Round cap:** 5 designer rounds per encoding (DESIGN_RUBRIC). Used 3 (r02 and r03 in parallel, then r04). r05 is round 4 and leaves one more before a forced vote.

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | measured reconstruction of the reference: laminar band X → 5 whorl tiles → Y, footnote row (bank · cone · maps) | `gallery/studio/convolutions/current/pp_convolutions_v1.png` | — | — | unscored benchmark | measured, not guessed; source of the Keep list in DESCRIPTION.md |
| r02 | r01 | real-kernel: same layout, everything computed (5-layer blur/ridge CNN, X's medial axis → letter Y, Ben-Day kernels, signed feature maps, RF pyramid) | `~/Downloads/pp_convolutions_real-kernel_v9.png` | 4.71/3 | 6/6/6 | FAIL · rank 3 | more schematic than r01; regressed r01's cone, depth-by-clipping and contour discipline. Kept on disk as the `real-kernel` flavour; not pursued |
| r03 | r01 | sliding-window: one thumbprint X (distance field) with a stride-2 staircase corridor, 5×5 LoG head mid-sweep, separate 11×12 output map whose blue skeleton reads Y | `~/Downloads/pp_convolutions_sliding-window_v10.png` | 5.57/4 | 8/6/5 | FAIL · rank 2 | broke the symmetry and did real arithmetic (ρ 0.92), but was still an input/kernel/output triptych; its seams regressed r01's contour continuity |
| r04 | r03 | wavefront: ONE lattice. Swept nodes (i+j ≤ 10) show X as sample dots with Y = K∗X rings on their own node; the unswept side stays distance-field rings; the LoG head sits on the Y's fork as the one plane | `~/Downloads/pp_convolutions_iterate_v9.png` | 6.14/5 | 9/8/7 | FAIL · rank 1 → parent of r05 | closed A1/A10/A11/S1/S2/S3; 59/63 bins exact, Pearson 0.98. New problems: the unswept mass reads as a HEART floating inside the margins, the lower-right 145×120 mm is leftover, the shadow reads as a doubled keyline, and collars sit 0.44 mm from their dots |

Ranking: r04 > r03 > r02, all FAIL. Art min decides first (5 > 4 > 3). Science min agrees (7 > 5, 6).

## Mandates
| id | raised | by | mandate | status | closed |
|---|---|---|---|---|---|
| A1 | r01 (DESCRIPTION) · r03 | art | Not a pipeline schematic. Collapse the triptych: every response lives on the X lattice where the window sat. No separate output panel, no staircase copy, no leader lines | fixed (art r04: FIXED) | r04 |
| A2 | r01 (DESCRIPTION) | art | Nothing is computed; the mechanism must show as a process | fixed (sci r03) | r03 |
| A3 | r01 (DESCRIPTION) | art | Bilateral symmetry about u = 0.50 caps tension | fixed (art r03) | r03 |
| A4 | r01 (DESCRIPTION) + If-only #2 | art | Decorative scatter dots, quarter brackets, plus marks, hollow square | fixed (art r03) | r03 |
| A5 | r01 (DESCRIPTION) + If-only #1 | art | Muddy starburst tiles; crossed-dash scribble in X | fixed (art r02) | r02 |
| A6 | r01 (DESCRIPTION) + If-only #3 | art | Accidental `>` pointer at `K` | fixed (art r02) | r02 |
| A7 | r01 (DESCRIPTION) | art | Stride block jammed in corner; second spine through Y | dropped (superseded by the r03 composition) | r03 |
| A8 | r01 (DESCRIPTION) | art | Hairline type, no dominant element | fixed (art r03) | r03 |
| A9 | r01 (DESCRIPTION) · r03 | art | Declare depth: 1.5 mm shadow keyline, rings stop at it; delete leashes and meaningless hollow circles | dropped. Art r04 found it "FIXED as worded, not effective" because the shadow reads as a doubled keyline. Superseded by A17 | r04 |
| A10 | r03 | art | Close the medial seams (zipper, hairpin slit, pitch ≥ 1.0 mm). **Regressed element of r01**, restored | fixed (art r04). Residue is polish: the 3 mm crumb at (50,182) and faint kinks along the crown crease at x 100–105, y≈150 | r04 |
| A11 | r03 | art | HANDOFF carries `lineage:` + declared canon | fixed as a process item (art r04). The lineage is weak, carried as A20 | r04 |
| A12 | r03 | art | Title: multi-pass strokes separate; `I` spacing; N diagonals | open (r04 PARTIAL: `I` fixed; both N diagonals are hairlines against fat stems). Polish, do it if cheap | |
| A13 | r03 | art | Travel is 49–51 % of draw | dropped (superseded by A19's measurable test: max consecutive travel < 120 mm, swatches last). The share itself is structural, because the dots are the input | r04 |
| A14 | r02 | art | r02 pen craft (fan knot, cone apex, crumbs, double frames) | dropped (r02 not continued) | r03 |
| A15 | r02 | art | r02: delete tile frames and link bars | dropped (superseded by A1) | r03 |
| A16 | r04 | art | **Kill the heart and the leftover quadrant.** Crop the unswept contour mass at the frame: scale or shift X so it bleeds off the TOP and RIGHT drawable margins. No outer contour closes anywhere on the sheet, and no empty region larger than 80×80 mm remains. Title and key sit on ONE shared left axis (same x within 0.5 mm). Test: at thumbnail size nobody can say "heart". Absorbs the r04 figuration regression and the art dim-4 (negative space) finding | open | |
| A17 | r04 | art | **The head is a lifted card.** Shadow band ≥ 3 mm wide on the right and bottom only, filled with 45° hatch at ≈0.9 mm pitch. Head keyline in 3 passes, making it the fattest line on the sheet. Field marks stop at the band's outer edge. Test: at 1 m the head reads as a card above the lattice, not as a registration double | open | |
| A18 | r04 | art + sci (merged: art M3a/b + sci M3) | **Head collars that plot and that tell the truth.** ≥ 0.6 mm bare paper between each collar's inner edge and its dot. Pass pitch ≥ the stated nib, with the nib stated in HANDOFF. Collar ink area ∝ \|w\| within ±20 % on all 25 taps: taps below one full nib ring are drawn as a single-ring ARC whose sweep angle ∝ \|w\|, so corners (≈0.08) read 3–7× the diagonals (≈0.01–0.03) instead of 1:1. Stricter of the two wordings kept | open | |
| A19 | r04 | art | **Layer order and travel.** Stream crimson → blue → black, or justify black-first in HANDOFF. Legend swatches are drawn last within each pen layer, in spatial order. Test: max travel between consecutive strokes < 120 mm (r04 had 256 mm blue and 184 mm black) | open | |
| A20 | r04 | art | Lineage is borrowed surface: Vega displaces the lattice, but r04 only resizes dots. Re-declare an honest lineage whose order the plate actually uses (a unit-grid-with-size-variation canon, or Ben-Day/Lichtenstein) or earn Vega. **Do not** displace lattice nodes: positions are the lattice the science critic recovers exactly | open, deferred (HANDOFF text; do it if cheap) | |
| S1 | r02 · r03 | science | Encoding on the sheet: X, K, Y = K∗X, sign colours, ring bins, dot area; one zero code | fixed (sci r04). The "y = 0" wording residue is carried in S8 | r04 |
| S2 | r03 | science | Inputs never hidden by outputs | fixed (sci r04: 0 of 197 hidden) | r04 |
| S3 | r03 | science | "Field X" rings must carry X | fixed. It was argued, then confirmed by sci r04: ring pitch 1.05 constant, dot area vs ring level across the front Spearman 0.91 | r04 |
| S4 | r03 | science | Y at one scale | dropped (superseded by A1). Also confirmed in r04: one ring pitch everywhere, including the key | r03 |
| S5 | r02 · r03 · r04 | science | No `dossier.md` / `encoding.md` for this slug | open (process). NOT FIXED three times, but it was never in a work order; it has been deferred every round because designers and the lead do not author it. Rule 2 is not applied because the encoding is clearly working (sci 6→8→9 truth). If it blocks a science PASS, route one translator pass to write `encoding.md` from r04's HANDOFF `rule:` line | |
| S6 | r02 | science | Signed effective RF | dropped (r02 not continued) | r03 |
| S7 | r02 | science | Kernel footprint on X | dropped (r02 not continued) | r03 |
| S8 | r04 | science (merged: sci M1 + M2 + dot-floor note) | **The key tells the truth and says what was found.** (a) One line: "blue = where X peaks (its skeleton) · crimson = where X starts · blank = X flat, ∇²X ≈ 0". (b) The zero code is honest: "no ring: \|y\| < max\|y\|/8" (21 of 34 ring-less nodes are nonzero), or draw exact zeros differently. (c) The 0.6 mm x-dot floor is removed or declared ("smallest dot: 0 < x ≤ x_min"; it covers 20 % of samples) | open | |
| S9 | r04 | science | The head hides finished outputs (4,5) +2, (4,6) −1, (5,5) −2, which are the only on-sheet proof that windows overlap by k − s = 3 | note, not a mandate. Declared in HANDOFF; if the A17 card allows it, let them read past the frame | |
