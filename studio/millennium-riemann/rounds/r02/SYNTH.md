# Synth — millennium-riemann after r01 ∥ r02 · 2026-09-29
route: designer
next round: r03 · parent: r02 (best so far: the only double PASS, art 8.0/7 · sci 9/9/8). One text-only borrow from r01: the series corner caption.

Ranking: r02 > r01 on verdict (PASS/PASS against FAIL/FAIL), on art min 7 > 6 and on science min 8 > 7. r01 stays on disk as the **faithful flavour**. It is the only round with the real-prime ψ footer, and its dropped mandates (ledger A4, S5) are ready if Juan asks for it.

Why not vote: both critics pass r02, but the fabrication gate fails on one item. The detail crop of γ₂₀–γ₂₈ shows solid red knots, because the 0.5 red nib is drawn twice 0.3 mm apart, which inks every arm point twice and the centre four times. That is the same mark the art critic named as the biggest weakness. By rule 1, a gate failure routes to the designer with it as mandate #1.

## The instruction
Keep r02 as it is and make the claim's one mark legible and the type exact. Re-emit the red layer as a **single one-way pass per arm** along the same true curves, at the same r = 1.6 mm with the 0.5 nib. If one 0.5 pass still knots at γ₂₄–γ₂₈, use a 0.3 red nib, still one pass. Do not lift loudness back with radius or passes, because 28 clean crosses in a single column already make the loud accent.

Then make the text layer tell the truth and sit on the grid:
- The key reads `WHERE BOTH ARE, ABOVE THE REAL LINE.`
- Three 1.6 mm numerals `−4 −2 1` sit under the baseline at the true feet.
- The `1 BLACK` block clears its rulings by ≥ 2.5 mm.
- The statement ends on x = 180, as the title does.
- r01's series caption `MILLENNIUM PRIZE PROBLEMS 1 / 7` / `CLAY MATHEMATICS INSTITUTE, 2000` goes flush-left at x = 206 in the title band.

State the per-layer minutes from the plate-job dry-run.

## Mandates to close
1. **A1 (gate item #1).** One pass of red. Test: in a true-width 1:1 crop of x 170–190, y 330–368, every cross shows two arms with cream in all four quadrants, and no red wider than the nib except at the centre. The red layer stays 56 strokes, each one-way.
2. **S1.** The key is `3 RED — WHERE BOTH ARE, ABOVE THE REAL LINE.` It must not be contradicted by the trivial-zero meetings on y = 32 or by the pole foot at x = 181.72.
3. **S2.** Set `−4` at x = 164.48, `−2` at x = 171.38 and `1` at x = 181.72, all at y ≈ 28 with 1.6 mm caps, each centred on its foot. They must stay clear of the bottom-left caption, which ends at x ≈ 110.
4. **A2.**
   - (a) Every `1 BLACK` glyph is ≥ 2.5 mm from both bounding rulings. Today it is 2.25 mm at (225.3, 347.0) against the k = 20 ruling at y = 344.8.
   - (b) The statement's right end lands on x = 180 (solve its tracking as v6 did for the title).
   - (c) r01's series caption is set at x = 206, ≤ 2.2 mm caps, with its cap line on the title's cap line. It must not cross x = 282.
5. **A3.** HANDOFF quotes minutes per layer from `.venv/bin/python -m promptplot plot plate <gcode> --layers 0,1,2,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`. r02 gives ≈ 31 / 26 / 24 / 3 = 90 min, because the plate job caps the feed at 500 and floors dwells at 1.0 s. Delete the false "≈ 80 min at F600". Emitting F600 / G4 P1.0 in the file through a round-local wrapper is optional, and `promptplot/` must not be edited.

## Preserve (r02, measured; any drift is a regression)
- **Field.**
  - The whole field comes from `rounds/r02/xray_abstract.json`, unchanged: 3.45 mm/u isotropic, σ = ½ at x = 180, real axis y = 32, window t ∈ [0, 97.35], σ ∈ [−47.33, 30.07].
  - 28 red centres ≤ 0.05 mm from (180, 32 + 3.45γₙ).
  - The column x = 180 is **never drawn**, and nothing in red sits below y ≈ 79.
- **Right field.** The right field is ζ's own rulings only, 22 at a 15.64 mm pitch. Right/left field ink stays ≤ 10 % (today 9.6–9.8 %).
- **Separation.**
  - Every Gram and half-Gram lone crossing of the column stays visible.
  - The A–B minimum stays ≥ 1.0 mm outside the red discs and the axis, with 0 approaches under 0.8 mm.
- **Type.**
  - The heavy title's last glyph ends on x = 180.
  - The x = 15 edge is shared by the title, the statement, the comb bleed and the bottom-left caption.
  - The x = 206 axis is shared by the wall label and the bottom-right caption.
  - The LeWitt wall label stays set between the rulings, including the shared end line "PART OF ζ(S) IS ZERO."
  - The bottom-left caption stays: window, 28 zeros, one scale. The bottom-right caption stays: "VERIFIED TO T = 3·10¹² (PLATT–TRUDGIAN 2021). NOT PROVED."
- **Layers.** Order 0 hairline → 1 black → 2 type (same black pen, no swap) → 3 red, with 2 physical swaps and no dotted runs. Strokes over 300 mm are split at their U-tip.
- **Lineage.** The lineage line stays: Sol LeWitt, *Wall Drawing #46* (1970).

## Do not
- Do not enlarge r, add red passes or widen the red nib to make the accent louder. That is what made the knots.
- Do not draw the critical line, add axes or add a frame. Do not move the column or re-window to change the ink ratio, which already passes.
- Do not import r01's ψ footer, register ticks, mirror or right-void formulas. The primes belong to the faithful flavour (ledger S3, argued).
- Do not let a new numeral or caption come within 2.5 mm of a ruling or the comb, or cross the undrawn column.
- Do not quote draw times that the file or the plate job does not produce.
- Do not edit anything under `promptplot/`.

## Fabrication gate (r02, 2026-09-29)
| check | result |
|---|---|
| bounds (`preview --stats --score`) | ink [15, 282] × [15.1, 403.4] (0, 0 is the park), A3 portrait, margin 15: clean. Grade A, 723 pen cycles, 11,006 cmds |
| pens / layers (`plot layer --list`) | 4 layers / 3 physical pens / 2 swaps: 89 · 79 · 499 · 56 strokes. Sane |
| draw time (`plot plate --dry-run`) | bounds ok. 31 / 26 / 24 / 3 min ≈ 90 min at feed ≤ 500, dwell ≥ 1 s. Sane. HANDOFF's 80 min is wrong → A3 |
| floods at detail (true-width crop, γ₂₀–γ₂₈) | **FAIL.** Red double pass → 2× inking along the arms and 4× at the centres → A1 |
| regression (`promptplot/` changed mid-rounds: 2aa2ba2) | PENDING. `scripts/studio_regression.py` was still running with no output after 30 min at load ~200. It does not block a designer route, but it and `make check` must both be clean before r03 (or any later round) can go to vote |
