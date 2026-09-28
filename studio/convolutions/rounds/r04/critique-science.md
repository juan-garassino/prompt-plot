# Science critique — convolutions r04 · machine learning (convolutional networks) · 2026-09-28
render: ~/Downloads/pp_convolutions_iterate_v9.png
gcode:  ~/Downloads/pp_convolutions_iterate_v9.gcode (48,372 cmds, 823 strokes: pen0 692 / pen1 70 / pen2 61; draw 11,074 mm = 9,293 black + 796 crimson + 986 blue)
pass: 2 (LEDGER.md read after the cold pass).

**Finding 0 (still open, S5) — there is no `dossier.md` and no `encoding.md` for this slug.** No §7
check numbers, §4 lies list or §5 misconception exist. Every number below is recomputed from first
principles and measured off the gcode; the lies list is the standard convolution-plate list.

Lattice recovered from dot centres: pitch 7.20 mm, node (c,r) at (16.65 + 7.2c, 18.55 + 7.2r), 25×25.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| output size (valid, stride 2) | — | (25−5)/2+1 = 11 × 11 | response rings only at even nodes (2i+2, 2j+2), i ≤ 10, j ≤ 10; ring-centres sit on the window-centre sample | OK |
| swept set i+j ≤ 10 | — | 66 nodes | every ring node satisfies i+j ≤ 10 (29 ring nodes, 0 outside) | OK |
| wavefront = ∪ of swept windows | — | boundary col 4.5 (r 23), 6.5 (r 21–22), 8.5 (r 19–20), 10.5 (r 17–18), 16.5 (r 11–12) | staircase vertices (4.49, 23.2)…(10.49, 16.6) and (16.49, 10.8)–(14.82, 12.51) in lattice units, step 14.40 mm = 2 pitches | OK (0.01 lattice) |
| dots only behind the front | — | dots ⊆ ∪ swept windows ∪ head window | 197 lattice dots, 0 outside; 25/25 inputs shown under the head | OK |
| head position / footprint | — | node (5,6) → window cols 10–14, rows 12–16, 5·7.2 = 36.0 mm | frame 85.0–121.0 × 101.4–137.4 (36.0 mm, centre (103.0, 119.4) = node (12,14)); shadow keyline offset (+1.50, −1.50) mm | OK |
| kernel shape (collar area = \|w\|) | — | mean-subtracted LoG, fitted σ = 1.01 lattice | collar annuli (ring pitch 0.19 mm radial, inner edge = x-dot + 0.45 mm): centre −1.00, ortho −0.32, (±2,0) +0.19, (±2,±1) +0.17, diag +0.035, corner +0.034; LoG(σ=1.01): −1/−0.30/+0.16/+0.15/+0.011/+0.081; rms 0.029 | OK in shape; corners under-drawn ×0.45 (see M3) |
| kernel signs | — | centre + ortho < 0, remaining 20 > 0 | 5 blue, 20 crimson | OK |
| kernel zero-sum | — | Σw = 0 | Σ/Σ\|w\| = +3.5 % (annulus model) … −9.4 % (ring-span model) | OK within quantisation |
| Y = K∗X, bins rint(4\|y\|/max\|y\|) | — | K = LoG σ=1, x = dot area (d²), max over swept nodes = 2.90 | 59/66 nodes exact; the 3 misses under the head are occluded outputs (declared), so **59/63 visible exact**; Pearson 0.98, sign 29/29; the 4 off-by-one bins (1,7) −0.42→−1, (3,3) 1.02→2, (3,4) 1.24→2, (7,3) 1.24→2 drop to 2/63 with the 0.6 mm dot floor set to x≈0.1 — within measurement | OK |
| strongest response | — | node (2,8) y = −2.90 | 4 blue rings at input (6,18) = (59.85, 148.15), the window centre of node (2,8) | OK |
| Y one scale | — | one ring pitch | rings 3.96 / 6.00 / 8.04 / 10.08 mm Ø on the lattice AND in the key (1.02 mm radial) | OK |
| X continuity across the front (LEDGER S3 check) | — | dot area ∝ d, rings = equal-Δd isolines | ring pitch 1.05 mm constant; dot area vs ring level at the nearest front crossing (13 front-adjacent nodes, ≈4.4 mm apart): Spearman 0.91, Pearson 0.92, area = 0.163·d + 0.52 | OK |
| inputs hidden by outputs | — | 0 | innermost response ring r = 1.98 mm > largest dot r = 1.13; outer bin-4 ring r = 5.04 < 6.07 to the nearest neighbour-dot edge; shadow keyline clears col-15 / row-11 dots by ≥1.0 mm | OK (0 hidden) |
| outputs hidden by the head | — | finished outputs whose centre lies in the current window: (4,5), (4,6), (5,5) | not drawn; recomputed bins +2, −1, −2 | declared (HANDOFF) |
| zero bin | — | 13 windows exactly zero (all inputs x = 0) | 34 visible ring-less nodes; 21 of them have y ≠ 0 (up to 0.115·max, e.g. node (7,0) at (117.45, 32.95)) | key wording false — M2 |
| x floor | — | area = x | 39/197 dots (20 %) clamped at 0.60 mm Ø | undeclared floor |

## Lies list (standard convolution list; no dossier §4 exists)
| item | status |
|---|---|
| kernel not zero-sum / wrong-area encoding | clean — LoG to rms 0.03, zero-sum within quantisation |
| convolution vs cross-correlation flip | clean — kernel 180°-symmetric |
| output size inconsistent with kernel/stride/padding | clean — 11×11 valid, stride 2, window 36.0 mm = 5 pitches |
| responses not actually K∗X | clean — 59/63 visible bins exact, Pearson 0.98, sign 29/29 |
| window path / wavefront mismatch | clean — staircase is the exact boundary of ∪ swept windows |
| decorative marks posing as data | clean — rings ahead of the front are X (equal Δd, continuity ρ 0.91 with the dots); no unexplained marks |
| same quantity at two scales | clean — one Y ring pitch everywhere incl. key (r03 violation fixed) |
| inputs hidden by outputs | clean — 0 inputs hidden (r03 violation fixed) |
| ambiguous / false zero | **VIOLATED (minor)** — key says "no ring: y = 0" (key block x 200–245, y ≈ 143); true for only 13 of 34 ring-less nodes, the other 21 are 0 < \|y\| < max/8 |
| quantity drawn not proportional to its declared area | **VIOLATED (minor)** — "collar area = \|w\|": all 8 smallest taps are one hairline ring; corners (w ≈ +0.08) drawn with the same ink as diagonals (w ≈ +0.01–0.03); x-dot floor 0.6 mm for 20 % of samples |

## Scores
truth 9 · fidelity 8 · legibility 7 · **VERDICT: FAIL**

- truth 9: every number the sheet asserts is real and recomputable from the sheet itself: LoG kernel, stride-2 valid geometry exact to 0.01 lattice, wavefront = union of swept windows, 59/63 response bins exact. The one false caption is the zero-bin wording.
- fidelity 8: one Y scale, no hidden inputs, X coded consistently on both sides of the front. Held back by the collar quantisation (corner = diagonal), the undeclared 0.6 mm dot floor and 3 outputs under the head (declared, but they are the two newest outputs and the only on-sheet proof that windows overlap by k−s = 3).
- legibility 7: the reading key is now on the sheet (S1) and a scientist can decode everything with a ruler. What the output *found* is never said: the blue chain down x = 103 (y 47–90, bins −4 −4 −4 −3) and the blue cluster at x 45–75, y 130–165 are X's medial axis (the ridge of the distance field, ∇²d < 0); crimson rings sit on the support edge; the blank interior is where X is locally linear (∇²X ≈ 0). The HANDOFF lineage line ("the rings are where it bends") states it, but it is not on the plate. A stranger sees the sweep but not the discovery.

## Mandates
1. **Put the finding on the sheet (legibility).** Measured: 0 words say what Y shows. The 11 blue ring nodes (6 of them bin 3–4) form two chains — x = 103.05, y 47.35–90.55 and x 45–75, y 133–163 — that coincide with the ridge of X's distance field; the 18 crimson ring nodes lie on the support edge; 13 exact-zero windows sit outside the support. Expected: one line in the key block (x 200–285, below y ≈ 140) or under CONVOLUTIONS (y ≈ 18–22): "blue = where X peaks (its skeleton) · crimson = where X starts · blank = X flat, ∇²X ≈ 0", so the plate says what the kernel found.
2. **Make the zero bin honest.** Measured: the key says "no ring: y = 0" (x 201–245, y ≈ 143), but 21 of the 34 visible ring-less nodes have y ≠ 0 (\|y\| up to 0.115·max\|y\| = 0.33, e.g. node (7,0) at (117.45, 32.95), (2,4) at (45.45, 76.15)); only 13 are exactly 0. Expected: "no ring: \|y\| < max\|y\|/8", or draw exact zeros differently from the sub-threshold bin.
3. **Make the collar areas carry \|w\| at the small taps.** Measured: all 8 smallest taps are a single hairline ring (Ø 2.46–3.10 mm). The corners (w ≈ +0.08·\|w_c\|, at (88.65,133.75), (117.45,133.75), (88.65,104.95), (117.45,104.95)) carry the same ink as the diagonals (w ≈ +0.01–0.03, at (95.85,126.55)…), so a 2.6–7× weight ratio is drawn 1:1 and the corners come out at 0.45× their LoG weight. Expected: collar annulus area ∝ \|w\| within ±20 % on all 25 taps (normalised area table −1 / −0.30 / +0.16 / +0.15 / +0.08 corners / +0.01–0.03 diag), and the 0.6 mm x-dot floor either removed or declared in the key ("smallest dot: 0 < x ≤ x_min").

Note (not a mandate): the head hides finished outputs (4,5) = +2, (4,6) = −1, (5,5) = −2 at (88.65,104.95), (88.65,119.35), (103.05,104.95). This is declared and matches art mandate A9. It costs the only direct evidence that windows overlap by 3 samples; if a later round can let them read past the frame, do so.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 | FIXED (residue → M2) | key block on sheet: `X dot area = x / no dot: x = 0`, `K 5×5 LoG, stride 2 / collar area = \|w\|`, `Y = K ∗ X / rings = round(4\|y\|/max\|y\|)`, `crimson + blue − / no ring: y = 0`; key rings share the lattice pitch (3.96/6.00/8.04 Ø); r03's double zero code (0.6 mm dot vs hollow 1.8 mm ring) is gone. Residue: the "y = 0" wording is false for 21 nodes |
| S2 | FIXED | 0 of 197 swept input samples hidden; every centre dot is kept inside its rings (r 1.13 < 1.98); K∗X recomputable at all 63 visible nodes (r03: 7/25 hidden in the strongest window) |
| S3 | FIXED (confirmed by critic) | ring pitch 1.05 mm constant = equal Δd; dot area vs ring level across the front Spearman 0.91 / Pearson 0.92 (n = 13), so dots and rings encode one X |
| S5 | NOT FIXED | still no `studio/convolutions/dossier.md` or `encoding.md` |

Regressions: none. The r03 truths (LoG kernel, stride-2 valid geometry, response = K∗X) all still hold and are tighter (ρ 0.92 → Pearson 0.98, 59/63 exact bins).
