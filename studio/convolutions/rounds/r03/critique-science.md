# Science critique — convolutions r03 · machine learning (convolutional networks) · 2026-09-28
render: ~/Downloads/pp_convolutions_sliding-window_v10.png
gcode:  ~/Downloads/pp_convolutions_sliding-window_v10.gcode (48,505 cmds, 750 strokes: pen0 489 / pen1 136 / pen2 125)
pass: 1 (cold). `studio/convolutions/LEDGER.md` does not exist.

**Finding 0 — there is no dossier.md and no encoding.md for this slug.** No §7 check numbers, no §4
lies list, no §5 misconception exist to check against. Everything below is recomputed from first
principles and measured off the gcode; the lies list is the standard convolution-plate list.
Encoding was inferred from the marks: kernel weight ∝ disc AREA (the only reading that makes it
zero-sum), X ∝ lattice-dot area, Y = signed ring count (crimson +, blue −, 0.6 mm black dot = 0).

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| kernel size / pitch | — | 5×5 | 5×5 taps at 6.5 mm = input lattice pitch 6.5 mm | OK |
| kernel shape | — | mean-subtracted inverted LoG, fitted σ = 0.995 lattice | tap areas normalised: centre −1.000, ortho −0.292, diag +0.032, (±2,0) +0.157, (±2,±1) +0.144, corner +0.074; LoG model −1/−0.286/+0.022/+0.156/+0.143/+0.073, rms err 0.005 | OK |
| kernel zero-sum (area) | — | Σw = 0 | +55.20 vs −54.16 mm², Σw/Σ\|w\| = 0.95 % (diameter-reading would give Σ = +16.4 → area is the encoding) | OK |
| stride | — | 2 lattice = 13.0 mm | track centres (29.25,160.25)→(42.25,147.25)→…→(120.25,69.25), Δ = (13,−13); future markers at (146.25,43.25),(159.25,30.25) | OK |
| output size (valid, s=2) | — | 25×27 input → (25−5)/2+1 = 11 × (27−5)/2+1 = 12 | map 11 cols × 12 rows at 8.5 mm | OK |
| window corridor = ∪ of past windows | — | x 13.0–123.5, y 66.0–176.5 (centre ± 16.25) | staircase outline vertices exactly (13,176.5)…(123.5,86)/(91,66) | OK |
| scan ↔ map rhyme | — | 7 past cells + 1 current | Y staircase bbox 190.5–250 × 129–188.5 (7 cells) + bold box 250–259 × 120–129 = kernel box (104–136, 53–85) position k=6 | OK |
| track responses vs map | — | X-side ring = Y cell | k=−1..6: 0,−1,−2,0,+2,−3,0,+2 on both panels, all 8 agree | OK |
| Y = K*X (13 map cells whose window is ≥19/25 visible) | — | K*X from dot areas, hidden samples quadratic-filled | signed Spearman 0.92, Pearson 0.94; 10/13 signs agree, the 3 disagreements are |est| ≤ 13.7 vs max 37.3 | OK (within noise) |
| strongest track response | — | cannot be recomputed | k=4 (94.25,95.25) drawn −3 but 7/25 window inputs are hidden on the sheet | UNVERIFIABLE |
| ring spacing of "field X" | — | should vary with X | bottom lobe y=50: 1.03–1.07 mm constant across the whole section (46 rings); right lobe 1.0–1.6 mm | encodes shape, not value |
| ink budget | — | — | total 14,178 mm; trefoil contour nest 8,531 mm = 60 %; pen1+pen2 (all data colour) 2,164 mm = 15 % | — |

## Lies list (standard convolution list; no dossier §4 exists)
| item | status |
|---|---|
| kernel not zero-sum / wrong-area encoding | clean — area-encoded, zero-sum to 0.95 % |
| convolution vs cross-correlation flip | clean — kernel is 180°-symmetric, flip is moot |
| output size inconsistent with kernel/stride/padding | clean — 11×12 = valid, stride 2 |
| responses not actually K*X | clean within measurement (ρ = 0.92 on 13 cells) |
| window path / map path mismatch | clean — corridor, staircase, bold box, dotted future tracks all agree |
| decorative marks posing as data | **VIOLATED** — the trefoil nest (60 % of ink, labelled "field X" in HANDOFF) is a constant-pitch distance nest (1.03–1.07 mm across the bottom lobe); it draws X's outline, not X. X's values exist only as corridor dots |
| same quantity at two scales | **VIOLATED** — Y level 3 is an 11.4 mm ring on the X corridor (94.25,95.25) and a 5.9 mm ring on the map (237.25,141.75); level 2 is 7.6 mm vs 4.1 mm |
| inputs hidden by outputs | **VIOLATED** — X-side response rings erase the centre sample of every past window (the −1.00 tap = 46 % of negative kernel mass) and the halo at (94.25,95.25) deletes 4 more samples |
| ambiguous zero | minor — Y≈0 is a 0.6 mm black dot, identical to the X-floor lattice dot; zero-response window centres on X are hollow 1.8 mm rings (two codes for one value) |

## Scores
truth 8 · fidelity 6 · legibility 5 · **VERDICT: FAIL**

- truth 8: the arithmetic is real — LoG kernel to 0.5 % rms, zero-sum, valid stride-2 geometry exact to 0.01 mm, map agrees with recomputed K*X (ρ 0.92). Held back because the dominant term of every drawn track response is hidden, so the sheet cannot prove its own strongest number.
- fidelity 6: three channel faults above (decorative "X" mass, two Y scales, occluded inputs). The Y ring quantisation (0–4) is coarse; e.g. est. −18.7 drawn −1 while est. +12.7 drawn +2 — possibly a per-sign normalisation, undeclared.
- legibility 5: the sheet has **zero** labels besides CONVOLUTIONS — no X, K, Y, no ∗, no stride, no sign/ring key. The corridor↔staircase rhyme is elegant and a scientist can decode it with a ruler; a stranger cannot tell what a ring, a colour, or the right-hand grid is. No §5 misconception exists to land.

## Mandates
1. **Reading key (legibility).** Measured: 0 labels, 0 legends on sheet (only the title at y≈13–22). Expected: `X` on the input lattice, `K` (5×5, stride 2) at the kernel box (104–136, 53–85), `Y = K ∗ X` above the map (x 190–285, y≈197), and one key strip giving crimson = + / blue = −, 1–4 rings = |Y| bins, black dot = 0.
2. **Stop hiding the inputs the response depends on.** Measured: centre samples missing at all 7 past window centres (29.25,160.25)…(107.25,82.25); 5 samples deleted around (94.25,95.25); window k=4 has 7/25 inputs invisible, so its −3 cannot be recomputed. Expected: 0 missing inputs in every past window — draw the response only on the Y map (or offset it off the lattice), keep the centre dot (weight −1.00, 25 of 54.2 mm² negative mass) visible.
3. **Make "field X" carry X, and give Y one scale.** Measured: trefoil nest pitch 1.03–1.07 mm constant across the bottom lobe (y=50), 8,531 mm = 60 % of ink, uncorrelated with the corridor dot sizes (0.6 → 2.24 mm); Y level 3 drawn 11.4 mm on X vs 5.9 mm on the map. Expected: rings as true isolines of X at equal ΔX (pitch ∝ 1/|∇X|, so density reads X and the saturated core opens up), or the value dots extended over the field; one ring pitch (0.9 mm radial) for Y on both panels.

## Follow-up on open mandates
id | status | evidence
— | — | no LEDGER.md for convolutions; first science pass.
