# Science critique — convolutions r05 · machine learning (convolutional networks) · 2026-09-29
render: gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.png
gcode:  gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.gcode (74,381 cmds, 807 strokes: crimson 47 / blue 46 / black 714; draw 17,131 mm = 497 crimson + 705 blue + 15,929 black, of which 10,959 mm is the stripe field)
pass: 2 (cold pass on HANDOFF + gcode + PNG, then LEDGER.md).

**Finding 0 (S5, still open):** there is still no `dossier.md` or `encoding.md` for this slug, so there are no §7 check numbers, §4 lies list or §5 misconception to check against. Every number below is recomputed from the HANDOFF `rule:` line and measured off the gcode.

The lattice, recovered from dot centres: input node (c,r) sits at (21.2 + 7.2c, 20.6 + 7.2r). There are 216 dots, all within 0.2 mm of a node. The X value is read as dot area, x = e²/e_max², where e is the spiral's outer centreline diameter and e_max = 2.26 mm.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| output size (valid, stride 2) | — | (37−5)/2+1 × (25−5)/2+1 = 17 × 11 | response rings only at input (2i+2, 2j+2); ring centres x = 35.6 + 14.4i, y = 35.0 + 14.4j exactly | OK |
| read windows i+j ≤ 10 | — | 66 | 37 ring nodes + 26 blank + 3 under the card = 66. Every ring node has i+j ≤ 10 | OK |
| crop | — | row 24 + ½ cell = 197.0, col 36 + ½ cell = 284.0 | the stripes end at y = 197.0 and x = 284.0; the unread arm leaves through the top-right | OK |
| staircase = boundary of ∪ read windows | — | cols 4.5 (r 22.5–24.5), 6.5, 8.5, 10.5 · 24.5 (r −0.5–4.5), 22.5, 20.5, 18.5, 16.5 | vertices (53.6,197)…(96.8,141.15) and (197.6,17)…(140,110.6) = those half-cells to 0.01 mm; it runs from the top edge to the bottom edge, and only the card interrupts it | OK |
| dots ⊆ read ∪ head window | — | — | 216 dots, 0 outside; 25/25 head-window inputs drawn (4 of them head-only) | OK |
| kernel | — | 5×5 LoG σ=1, mean-subtracted: centre −1, ortho −0.290, (±2,0) +0.157, (±2,±1) +0.145, corner +0.075, diag +0.019 | collar ink length per tap / \|w\| constant to **0.38 %** on all 25 taps (63.07 mm per unit); corner/diag ink 3.93 vs 3.94 | OK |
| kernel signs · zero-sum | — | 5 −, 20 +; Σw = 0 | 5 blue, 20 crimson; + ink 136.19 mm vs − ink 136.23 mm (0.03 %) | OK |
| collar clearance / pitch | — | ≥ 0.6 mm bare, pitch ≥ nib 0.30 | bare paper 0.59–0.60 mm on all 25 taps; pass pitch 0.32 mm | OK |
| Y = K∗X bins rint(4\|y\|/max) | — | max \|y\| at node (5,2), window centre (107.6, 49.4) = 4 blue rings | **63/63 visible bins exact** (sign 37/37, Pearson 0.984) with floor dots read as x ≤ 3.5 %. At 7 %, 61/63 (misses (2,5) 1.46 and (3,5) 1.57, both on the .5 boundary) | OK |
| hidden outputs (HANDOFF: (4,5) 0, (5,5) −3, (4,6) −2) | — | +0.33 → 0 · −2.56 → −3 · −1.55 → −2 | not drawn; declared in HANDOFF only | OK (claim true) |
| zero code "no ring: \|y\| < max\|y\|/8" | — | rint(4\|y\|/m) = 0 ⇔ \|y\| < m/8 | 26 ring-less nodes = 12 exact zeros + 14 sub-threshold; the key says so | OK |
| floor "smallest: x < 7 %" | — | (0.60/2.26)² = 7.05 % | 39 dots at e = 0.60 | OK |
| Y one scale | — | one ring pitch | 1.98 / 3.00 / 4.02 / 5.04 mm radius (1.02 pitch) on the lattice AND in the key | OK |
| X is a distance field (\|∇d\| = 1) | — | d = 7.27 mm · e² | lower-arm flanks: slope 0.99 ± 0.03 e² per cell. 14 front dots whose nearest boundary is on the drawn outline: d_dot = d_outline within ±0.3 mm (e.g. (16,11) 5.9/5.9, (12,16) 23.6/23.6). Stripe perpendicular pitch 1.050 mm (5–95 % 1.044–1.057) | OK: dots and stripes encode one X |
| "exact" distance field (HANDOFF) | — | point-sampled ridge e² 4.67 | ridge e² 4.41 = box-averaged over the 7.2 mm cell (4.43). 32 of 39 floor dots are cells whose **centre** lies 0.3–3.3 mm outside the support (lower-arm flanks cols 7/17 at −2.0 mm) but which overlap it | note: X is cell-averaged, not point-sampled. It is consistent on the sheet; the HANDOFF wording is loose |
| dot INK area ∝ x | — | inked Ø = e + 0.30 nib | 93/216 dots (e ≤ 1.24) are inked >20 % over x; the floor is +75 %; median +17 %. Dynamic range 14.2:1 designed vs **8.1:1 inked**. Recomputing Y from inked areas gives 54/63 bins exact | **VIOLATED**: M1 |

## Lies list (standard convolution list; no dossier §4 exists)
| item | status |
|---|---|
| kernel not zero-sum / wrong area | clean: ink ∝ \|w\| to 0.4 %, Σ ink ± balanced to 0.03 % (A18 fixed) |
| convolution vs cross-correlation flip | clean: the kernel is 180°-symmetric |
| output size / stride / window inconsistent | clean: 17×11 valid, stride 2, window 5 × 7.2 = 36 mm, staircase exact |
| responses not actually K∗X | clean: 63/63 visible bins exact |
| same quantity at two scales | clean: one Y ring pitch, including the key |
| inputs hidden by outputs or by the card | clean: 0 hidden. Dots next to the shadow clear the hatch by ≥ 0.6 mm (e.g. (15,12) at (129.2,107.0): seg dist 1.62 mm vs ink r 0.87 mm) |
| ambiguous / false zero | clean: the key wording is now exact (S8b) |
| drawn area not ∝ declared quantity | **VIOLATED**: "X dot area = x" holds for the spiral centreline, not the ink. The 0.30 mm nib adds +17 % median and up to +75 % to the inked area of small dots (M1) |
| caption claims the drawing does not support | **VIOLATED (minor)**: the key says "blank X flat". 5 blank interior nodes sit on unit-slope ramps (\|∇d\| = 1.01): (4,3), (4,4), (6,3), (6,4) at x 93.2/122.0, y 78.2/92.6, and (3,6) at (78.8,121.4). "blue = where X peaks (skeleton)" also covers the rounded tip: (4,1), (6,1), (4,2), (6,2) sit 14.4 mm off the axis (M3) |
| decorative marks posing as data | clean in substance, but **unkeyed**: the stripe field (10.96 m, 64 % of all ink) is X's isolines at Δd = 1.05 mm, and the staircase is the read boundary. The key names neither (M2) |

## Scores
truth 9 · fidelity 7 · legibility 7 · **VERDICT: FAIL**

- **truth 9:** every number the sheet asserts is recomputable and right. The LoG kernel is exact to 0.4 %, the geometry is exact to 0.01 mm, 63/63 bins match, the dots continue the stripes to ±0.3 mm, and the hidden-output claims hold. Held back only by the "X flat" wording and the loose "exact / x = 0 is paper" HANDOFF phrasing (X is cell-averaged).
- **fidelity 7:** the kernel channel is now exemplary. The **input** channel is not: dot ink area is centreline area plus a nib annulus, which compresses x's range from 14.2:1 to 8.1:1 and inflates 93 of 216 dots by more than 20 %. This is the exact defect A18 fixed for the collars, but it was left in the dots. It was also present in r04 unmeasured, so it is not a regression.
- **legibility 7:** the finding is now on the sheet (S8a), which is the big gain. But the plate's dominant mass (the stripe field, x 83–284, y 97–197) and the staircase have no key line. A stranger cannot tell that the stripes ARE X, not yet read, or that the staircase is where the window has been. And "flat" mis-teaches what a LoG ignores (linear ramps, not flat regions).

## Mandates
1. **Dot ink area ∝ x (fidelity, input channel).** Measured: inked Ø = e + 0.30 mm. Floor dots (39, e = 0.60, e.g. (7,8) at (71.6,78.2)) are inked at 12.4 % of max against 7 % declared (+75 %). All dots with e ≤ 1.24 mm are over by more than 20 % (93/216), e.g. (8,8) at (78.8,78.2) is 19.8 % inked vs 13.8 % designed. The inked range is 8.1:1 against 14.2:1, and Y recomputed from the ink gives 54/63 bins. Expected: spiral outer centreline Ø = D·√x − 0.30 (the collar rule, applied to the dots), so inked area is within ±20 % of x on all 216 dots and Y from the ink still gives 63/63.
2. **Key the stripes and the staircase (legibility).** Measured: 0 key lines describe the stripe field (10,959 mm, 64 % of the ink, x 83–284, y 97–197) or the staircase (53.6,197)→(197.6,17). Expected: two lines in the key block (x ≈ 200–285, y 40–90), for example "stripes: X not yet read · one line per Δx = 1.05 mm" and "staircase: edge of the 66 windows read so far". Then a stranger sees one field, half read.
3. **Make the finding line exact (truth / legibility).** Measured: the key block at x 200–285, y ≈ 35 says "blank X flat, ∇²X ~ 0". But 5 blank nodes, (4,3), (4,4), (6,3), (6,4) and (3,6), sit on ramps of slope 1.01 (x 93.2/122.0, y 78.2/92.6; (78.8,121.4)). "blue: where X peaks (skeleton)" also labels tip nodes (4,1), (6,1), (4,2), (6,2) at (93.2/122.0, 49.4/63.8), 14.4 mm off the axis. Expected: "blank: X straight (flat or constant slope), ∇²X ≈ 0 · blue: X bends down (ridge and rounded tip) · crimson: X bends up (where it starts)". Optional, if cheap: one tiny note that 3 finished outputs lie under the card (S9).

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S5 | NOT FIXED | still no `studio/convolutions/dossier.md` or `encoding.md`. It is not blocking on its own (truth 9), but it forces every check to be rebuilt from HANDOFF |
| S8 (a) finding on sheet | FIXED (wording residue → M3) | key: "crimson + where X starts / blue − where X peaks (skeleton) / blank X flat, ∇²X ~ 0"; blue nodes = X's ridge + rounded tip, crimson = support edge, verified |
| S8 (b) zero code | FIXED | "no ring: \|y\| < max\|y\|/8"; 26 ring-less = 12 exact zeros + 14 sub-threshold, all consistent |
| S8 (c) dot floor | FIXED | "smallest: x < 7 %" = (0.60/2.26)² = 7.05 %; 39 floor dots. New, related finding: nib bias (M1) |
| A18 (sci half) collars | FIXED | ink ∝ \|w\| within 0.38 % on 25/25 taps (r04: corners 0.45×); corner/diag 3.93 vs 3.94; bare gap 0.59–0.60 mm; pitch 0.32 ≥ nib 0.30, nib stated in HANDOFF |
| S9 (note) | NOT CHANGED, declared | card still hides finished outputs (4,5) 0, (5,5) −3, (4,6) −2 (recomputed, all as HANDOFF states); not stated on the sheet |

Regressions: none. Every r04 truth still holds and is tighter: 59/63 → 63/63 bins, and X continuity now shows as dot-distance = outline-distance to ±0.3 mm. Layer order crimson → blue → black, as HANDOFF states. Max inter-stroke travel is 176.9 mm, from (52.0,164.6) to (203.5,73.3); that belongs to art A19.
