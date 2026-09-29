# Synth — millennium-riemann after r03 · 2026-09-29
route: vote
next round: none, pending Juan's vote. If Juan sends it back, the next round is r04 · parent r03 (best so far: the only double PASS with a clean gate, art 8.43/8 · sci 9/9/9)

Ranking: r03 > r02 > r01. r03 is r02's field byte-identical plus the polish, so it beats r02 on art min (8 > 7), science min (9 > 8) and art avg (8.43 > 8.0). All five r02 mandates (A1, A2, A3, S1, S2) were confirmed FIXED by the critics in pass 2, not on the designer's word. r01 stays on disk as the **faithful flavour**: it is the only round carrying the real primes (the ψ₁₀₀(x) − x footer), and its dropped mandates A4 / S5 are ready if Juan wants the prime companion. r02 is history only.

Lineage: Sol LeWitt, *Wall Drawing #46* (1970). The curator should check the exact title and year against the catalogue raisonné before the plate is filed.

## The instruction
No designer round is dispatched. Send r03 to Juan's vote as plate 1 / 7 of MILLENNIUM. It is the X-ray of ζ: Re ζ = 0 in black and Im ζ = 0 in hairline, exact on the upper half-plane at 3.45 mm/u. There are 28 one-pass red crosses at the real γ₁…γ₂₈ on the undrawn column Re s = ½. The right field holds only ζ's own rulings. The head follows the series grammar: a spaced-caps title top-left, a one-line statement, corner captions and one loud accent.

If Juan returns it as REWORK without a new direction, r04 (parent r03) is text-only. It adds one phrase to the bottom-left caption, e.g. `−4, −2: ZEROS ON THE LINE. 1: THE POLE.`, so that a stranger does not read `1` as a third trivial zero (S6). Nothing else moves: not the field, the red, the grid or the layers. Any J* note outranks this.

## Mandates to close (only if Juan sends it back)
1. **J\*.** Whatever Juan's REWORK note says comes first.
2. **S6.** Name the three anchors in the bottom-left caption. Do not add any more numerals: an axis is forbidden (§9.5).
3. **A6.** State once, in HANDOFF, that §11.3 is measured on layers 0 + 1 only. DESCRIPTION.md already says so.

Deferred, and not for a polish round:
- **A5** (upper crosses read as hooks). This is bounded by **S8**: the 80.9°–82.7° chord opening at 1.2 mm is true tongue-tip curvature. The only honest lever is a re-window (t ≤ 52, about 10 crosses, ≥ 2.9 mm/u). That is a thesis change for Juan to call, and it is also the natural A5 Leo edition (encoding §10).
- **S7.** An operator note, already in DESCRIPTION.md § Plot.

## Preserve (r03, measured; any drift is a regression)
- **Field.**
  - The field comes from `rounds/r02/xray_abstract.json`, unchanged: 3.45 mm/u isotropic, σ = ½ at x = 180 (never drawn), real axis y = 32, t ≤ 97.35.
  - Curve truth: hairline ≤ 0.089 mm, black ≤ 0.017 mm, red ≤ 0.023 mm from the true zero sets.
  - Completeness: 0 misses on 1,114 sign changes.
- **Red.** 56 one-way strokes, 2 per zero, r = 1.6 mm, 0.5 nib, one pass, cream in all four quadrants (crop x 170–190, y 330–368). Never fatten it back to make it louder.
- **Right field.** Only the rulings t = kπ/ln 2 at a 15.64 mm pitch. Right/left field ink 9.2–9.7 % (layers 0 + 1).
- **Type grid.**
  - Title and statement end on x = 180.
  - The series caption, wall label and bottom-right caption start on x = 206. The series caption's cap line equals the title's (403.36).
  - The wall label clears its rulings by ≥ 2.97 mm.
  - `−4 −2 1` sit on the true feet (≤ 0.005 mm), 3.2 mm under the axis.
  - The key reads `WHERE BOTH ARE, ABOVE THE REAL LINE.` The colophon reads `VERIFIED TO T = 3·10¹² (PLATT–TRUDGIAN 2021). NOT PROVED.`
- **Layers.** 0 hairline 0.1 → 1 black 0.3 → 2 type (same black 0.3, skip the prompt) → 3 red 0.5. 3 physical pens, 2 real swaps, no dotted runs.

## Do not
- Do not straighten the upper X's (S8, encoding §9.9). Do not enlarge r, add red passes or widen the red nib.
- Do not draw the critical line, an axis, a frame or more numerals.
- Do not import r01's ψ footer, ticks or mirror into this plate. The primes live in the faithful flavour (S3, argued).
- Do not scale it down to A5. An A5 Leo edition is a re-window (encoding §10).
- Do not edit anything under `promptplot/`.

## Fabrication gate — r03 (2026-09-29, run by the lead)
| check | result |
|---|---|
| bounds (`preview --stats --score`) | X[0–282] Y[0–403.4]; (0, 0) is the park. Ink [15, 282] × [15.1, 403.4]: clean at A3 portrait, margin 15. Grade A, 821 pen cycles, 11,256 cmds, draw 29.0 m, travel 4.96 m |
| pens (`plot layer --list`) | colour 0 = 89 strokes / 2,750 cmds · 1 = 79 / 2,488 · 2 = 597 / 5,213 · 3 = 56 / 805. 4 layers on 3 physical pens, 2 real swaps. No pen cap; every layer is one meaningful pen |
| draw time (`plot plate --layers 0,1,2,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`) | bounds ok · 31 / 26 / 28 / 3 min · ETA ≈ 94 min at feed ≤ 500, dwell ≥ 1 s. This matches HANDOFF and DESCRIPTION. The dry-run waits on 4 swaps; only 2 are physical (S7) |
| detail crops (true width) | γ₂₄–γ₂₈ (x 170–190, y 330–368): two arms per mark, cream in all four quadrants, no knot. Densest comb (x 15–60, y 330–370): clean gaps between the 0.1 and 0.3 families, no flood. Fan on the axis (x 15–60, y 30–70) and the feet (x 150–195, y 22–50): clean; the numerals clear the axis |
| dotted runs | none |
| regression (`scripts/studio_regression.py`) | **no drift**, exit 0. 121 pieces ok, 0 without an entry point, and 2 errors in other slugs: `neural-networks-cnn` r01 (`net.load_input`, a module-name collision between pieces) and one "no paper for the key" assert. Both are outside this piece and are not fingerprint drift |
| `make check` (test-ci half; studio-check = the line above) | **clean**, exit 0. 653 passed, 3 skipped (optional SDKs), 1 deselected (the known `test_refinement` stub-queue failure), 9 min 30 s. Together with the regression line, `make check` is clean |

Gate verdict: **CLEAN.** Route `vote`. This also closes the r02 gate's PENDING regression item.
