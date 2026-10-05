# Science critique — convolutions r06 · machine learning (convolutional networks) · 2026-09-29
render: gallery/studio/convolutions/trials/pp_convolutions_wildcard_v22.png
gcode:  gallery/studio/convolutions/trials/pp_convolutions_wildcard_v22.gcode (20,276 cmds, 997 strokes: pen0 orange 13 / pen1 crimson 242 / pen2 blue 25 / pen3 black 717; draw 389 / 2,863 / 518 / 10,577 mm; stream order 0→1→2→3 monotonic, as HANDOFF says)
pass: 2 (LEDGER.md read after the cold pass).

**Finding 0 (S5, still open): there is no `dossier.md` or `encoding.md` for this slug.** No §7 check
numbers, §4 lies list or §5 misconception exist. Every number below is recomputed from the HANDOFF
`rule:` line and first principles, then measured off the gcode.

X was recovered from the gcode: there are 98 black nested-triangle markers (16-vertex strokes, bbox 2.26 × 1.95 mm).
One of them is the key swatch at (200.66, 41.4), so X has 97 impulses. Each impulse sits at its triangle's
**centroid** (bbox centre − 0.325 mm in y). Fitting the offset gives a median field error of 0.001 at the
centroid, against 0.029 at the bbox centre and 0.057 at the base.
The kernels as stated: K(p) = exp(−|p|²/2σ²)·cos(2π p·n/λ), with n normal to the bars, σ 9.6 mm and λ 12 mm. The blur is exp(−|p|²/2·3.6²). Both peak at 1.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| X = 97 unit impulses | — | x = 1 each | 97 identical markers, 0 with other black ink within 1.6 mm of the centre; K1 43 · K2 4 · K3 22 inside the cards | OK |
| K1 line = level 0.35 of K1∗X, bars 30° | — | Σ over all 97 impulses | 92 crimson contours: \|K∗X − 0.35\| median 0.002 (≤ 0.01 on 91/92). The 120° convention fails (median −0.06, p90 1.5) | OK |
| K2 line = level 0.35, bars 120° | — | same | 25 blue contours: \|err\| p90 0.002, max 0.003. The 30° convention fails | OK |
| K3 line = level 0.35, blur σ 3.6 | — | single-impulse radius σ√(2 ln(1/0.35)) = 5.216 mm | 11 orange contours, err p90 0.001. Isolated circles r = 5.224 / 5.235 / 5.241 mm (fit residual ≤ 0.03), centred ≤ 0.035 mm from their impulse | OK |
| "exact sum over ALL impulses on the sheet" | — | inside-card impulses alone would give different contours | the drawn lines only fit if outside-card impulses are included: inside-only error p90 0.20 (K1) / 0.30 (K2), against 0.0035 / 0.0020 with all 97 | OK (proved) |
| solid = K∗X > 1.25 | — | one impulse peaks at 1.00, so a solid needs ≥ 2 | 6,834 / 6,843 fill samples ≥ 1.25 (9 at 1.249). K1 has 17 components > 1.25 in the card, all filled. K2 max in card 1.001, so no solid (correct). K3 max 1.30 at (124.5, 42.0): one sliver, drawn | OK |
| fill inset ≥ 0.8 mm inside the line | — | — | fill → 0.35 line min 0.81 mm (p1 0.82) | OK |
| solid fill pitch 0.8 mm | — | — | cross-sections at (109.4, 23.2), (92.4, 38.2), (72.9, 43.8): gaps 0.80 / 0.80 / 0.80 / 0.81; hatch at 30° (29.4–30.2) | OK |
| grid pitch 12 mm = λ | — | λ = 12 | verticals x 182.66 → 278.66 step 12.00; horizontals y 22.2 → 70.2 step 12.00 | OK (see note) |
| isolated K1 stamp exists (the kernel itself is on the sheet) | — | neighbour interference < 0.35 | impulse (27.8, 106.4): max neighbour term within 14 mm = 0.18; (65.9, 152.0): 0.14 | OK, but unmarked |
| signed field K1∗X, K2∗X | — | gabor is signed | K1 in card: area ≥ +0.35 = 3,860 mm², **≤ −0.35 = 3,851 mm²**; ≥ +1.25 = 638 mm², **≤ −1.25 = 572 mm²**; range −2.72 … +2.91. K2: ≤ −0.35 = 781 mm², min −0.83 | **negative half silent** (lie 1) |

Note on the grid: the pitch equals λ exactly. But the bars run at 30° / 120° and the grid at 0° / 90°, so the ruler
cannot be laid against any bar. An isolated gabor's visible bar spacing is the side-lobe peak at 11.55 mm, not 12,
because the envelope pulls the peak in. The statement is true; as a ruler it is weak.

## Lies list (standard convolution list; no dossier §4 exists)
| item | status |
|---|---|
| responses not actually K∗X | clean. All 128 level contours on the analytic sum, field error ≤ 0.003 (K2, K3) and ≤ 0.01 (K1) |
| window shows a local sum instead of the global one | clean. Outside-card impulses are provably included |
| kernel mislabelled (orientation, σ, type) | clean. 30° / 120° verified against the swapped convention; the blur circle radius matches σ 3.6 to 0.02 mm |
| convolution vs correlation flip | clean. Both kernels are 180°-symmetric |
| "solid = only a sum" false | clean. Single peak = 1.00 < 1.25, and every solid sits where ≥ 2 stamps add |
| inputs hidden by outputs | clean. The triangles plot last, with halos; 0 collisions |
| broken scale / ruler | clean (pitch 12.00). Weak, see note |
| **ambiguous zero / one-sided signed field** | **VIOLATED.** Blank paper inside K1 means "≈ 0" and also "trough down to −2.72". The deepest trough, (110.3, 41.0), lies between the two big solid bands; 572 mm² of the card is ≤ −1.25, as strong as the solids, and it is undrawn and undeclared. The key only says "line K∗X = 0.35" |
| decorative marks posing as data | minor. The card shadows are black 45° hatch (194 strokes). The key's "solid" swatch is also black hatch, while real solids are coloured 30° hatch, so a stranger can read the shadow bands as data |
| units | minor. "σ 9.6" and "σ 3.6" carry no unit (mm only by inference from the grid line) |

## Scores
truth 9 · fidelity 7 · legibility 7 · **VERDICT: FAIL**

- **truth 9.** Every assertion on the sheet is exact and recomputable from the sheet. X, three kernels, levels, the solid threshold, pitch and grid all check to ≤ 0.003 in field value or ≤ 0.02 mm. Only the unit-less σ keeps it from 10.
- **fidelity 7.** The positive half of each signed map is encoded perfectly, but the negative half (equal in area, and in K1 equal in magnitude) is blank paper, indistinguishable from zero. r04 carried sign on two pens; r06 dropped that channel. The one K3 solid (peak 1.30) is mostly under the halo of the impulse at (125.16, 41.62): 60 % of its 1.25 boundary is not drawn.
- **legibility 7.** "every squiggle is a sum" and "solid … only a sum (one impulse alone peaks at 1)" land: a stranger can see stamps merging into solid bands. Four things do not land:
  - Nothing says the three cards are **three filters of one conv layer on the same X**, i.e. three feature maps.
  - Nothing connects the plate to convolutional networks: no "feature map", "filter" or "layer", and no "first-layer CNN filters are Gabors".
  - The bare kernel (δ ∗ K = K) is on the sheet at (27.8, 106.4) but is not pointed to.
  - Cancellation, the other half of "a sum", is invisible.

## Mandates
1. **Draw or declare the negative half of the gabor maps (fidelity).**
   - Measured: inside K1, K∗X ≤ −0.35 over 3,851 mm² (the ≥ +0.35 area is 3,860 mm²) and ≤ −1.25 over 572 mm² (solid area 638 mm²). The minimum is −2.72 at (110.3, 41.0), between the two big crimson solid bands. In K2 the minimum is −0.83, around (224, 139). All of it is blank paper, the same code as zero.
   - Expected: the −0.35 level drawn as a dashed line in the card's own pen, optionally with ≤ −1.25 as sparse dots, and one key line "dashed = K∗X = −0.35 (troughs cancel)". The minimum acceptable fix is a key line "blank = K∗X < 0.35, including troughs to −2.7".
   - This restores the sign channel r04 carried (S1) and shows that sums also cancel.
2. **Say what the three cards are, and tie it to CNNs (legibility).**
   - Measured: 0 words on the sheet say "filter", "feature map" or "layer". The key block (x 190–285, y 12–45) explains marks, not structure.
   - Expected: one plain line under the subtitle (y ≈ 175, x 40–150) or in the key, e.g. "one input X · three filters → three feature maps of one conv layer · each triangle stamps a copy of the filter, overlaps add". Also a leader-free marker or label at the isolated K1 stamp (27.8, 106.4), e.g. "alone: the filter itself", so the reader sees δ ∗ K = K before the sums.
3. **Make the furniture unmistakable from data, and state units (fidelity/truth).**
   - Measured: the card shadows are black 45° hatch, 194 strokes, on the K2 right edge and the K3 right and bottom edges. The key's "solid" swatch (≈ x 194–203, y 29) is drawn in black hatch, but real solids are coloured 30° hatch at 0.80 mm pitch. The σ labels read "σ 9.6" and "σ 3.6" with no unit.
   - Expected: the key's solid swatch drawn in a card colour (or labelled "hatch in the card's colour"), so black hatch means shadow only. "σ 9.6 mm", "σ 3.6 mm", "λ 12 mm" in the card labels.
   - Optional: rotate the 12 mm grid swatch to 30° / 120°, or add one tick pair across an isolated K2 stamp, so λ can actually be read off a bar family.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S5 (no dossier/encoding) | NOT FIXED | still absent. Fourth round. It now blocks the lies/misconception check on a completely new thesis; route one translator pass for `encoding.md` from this HANDOFF `rule:` line |
| S8 (key tells the truth, says what was found) | PARTIAL | (a) FIXED in the new thesis: the finding is on the sheet ("every squiggle is a sum", "only a sum, one impulse alone peaks at 1"), verified true. (b) REGRESSED in kind: the zero code is ambiguous again, because blank paper now also covers troughs to −2.72 (mandate 1). (c) FIXED: the x floor is gone, all impulses are unit markers, and x = 1 is declared |
| S9 (head hides outputs) | superseded | no head / window in r06 |
| A18 (science half: collar area ∝ \|w\|) | superseded | no collars. The kernel is shown as its impulse response instead, which is exact (r = 5.224 vs 5.216 mm) |
| regression check (truths held in r04) | **REGRESSED: sign** | r04 encoded sign(y) on two pens (S1, closed r04). r06 encodes only K∗X ≥ 0.35, so half of each signed gabor map is unencoded. S1's "one zero code" also no longer holds |
