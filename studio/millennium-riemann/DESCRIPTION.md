# RIEMANN HYPOTHESIS — MILLENNIUM 1 / 7 — description

<!-- written 2026-09-29 by the studio lead at the vote after r03. It describes the CURRENT best (r03), not the history. This is the spec the next iteration starts from: edit freely. -->

| | |
|---|---|
| series | MILLENNIUM PRIZE PROBLEMS, plate 1 of 7 (Riemann, P vs NP, Navier–Stokes, Yang–Mills, Hodge, Poincaré, BSD) |
| current render | `gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2_phys.png`. This is the true-width preview (0.1 / 0.3 / 0.3 / 0.5 nibs); judge here. Flat png `_v2.png` and gcode `_v2.gcode` sit beside it. Studio round r03 |
| source | `studio/millennium-riemann/rounds/r03/piece.py::riemann_two_instructions`, seed 7 (deterministic). Field data: `rounds/r02/xray_abstract.json`, read in place. Zeros: `data/zeros.json` |
| paper · pens | A3 portrait, cream, margin 15. Pen 0 black 0.1 fineliner = Im ζ = 0 plus the real axis. Pen 1 black 0.3 = Re ζ = 0. Pen 2 = the same black 0.3 on its own layer = type. Pen 3 red 0.5 = the 28 nontrivial zeros |
| lineage | Sol LeWitt, *Wall Drawing #46* (1970). An instruction executed exactly; the wall label is the instruction. The exact title and year still need a check against the catalogue raisonné |
| status | goes to Juan's vote. Critics: art 8.43/8 PASS · science 9/9/9 PASS. The fabrication gate is clean. Alternative flavour: `faithful` (r01, the reference's centred mirror, carrying the real-prime ψ footer) is on disk |

## In one line
The X-ray of ζ: every curve where Re ζ(s) = 0 (black) and where Im ζ(s) = 0 (hairline), computed exactly on the upper half-plane at one isotropic scale. Every meeting above the real line is marked with a red cross, and all 28 fall on one vertical, Re s = ½, which is never drawn. The hypothesis is the column that nobody drew.

## What is on the sheet
Sheet mm, x right, y up. One scale on both axes: 3.45 mm per unit. σ = ½ is at x = 180. The real axis is y = 32, and t runs 0 → 97.35 (top crop at y = 367.86, mid-gap between γ₂₈ and γ₂₉).

1. **The comb** (left 62 %): black Re-tongues and hairline Im-curves sweep in from the left edge, bleeding off x = 15. Each tongue tip turns just short of the column. Near the axis the lines fan down onto the real line, landing on the trivial zeros −2, −4, … −18. The Re = 0 arc from −2 lands on the pole foot at s = 1.
2. **The column** x = 180 (undrawn): 28 red crosses at the exact (½, γₙ), from γ₁ = 14.1347 (y = 80.77) to γ₂₈ = 95.8706. Each cross is the two true branches through ρₙ inside r = 1.6 mm, drawn in one pass. The spacing is visibly unequal, and there is a 48.8 mm red-free stretch above the axis. Lone Gram and half-Gram crossings between the zeros are left visible.
3. **The right field** (38 %): only ζ's own hairline rulings, which flatten to t = kπ/ln 2 at a 15.64 mm pitch. Field ink right of the column is ≈ 9.5 % of the ink on the left. §11.3 measures this on the field layers 0 + 1, excluding the red.
4. **Head**: `RIEMANN HYPOTHESIS`, heavy spaced caps top-left from x = 15, ending on x = 180. Under it the statement `EVERY CROSSING ABOVE THE REAL LINE STANDS ON RE S = 1/2.` also ends on x = 180. Top-right on x = 206, at the title's cap line: `MILLENNIUM PRIZE PROBLEMS  1 / 7` / `CLAY MATHEMATICS INSTITUTE, 2000`.
5. **Wall label** (x = 206, set between rulings k = 18–20): `1 BLACK — EVERY POINT WHERE THE REAL PART OF ζ(S) IS ZERO.` · `2 HAIRLINE — … IMAGINARY PART …` · `3 RED — WHERE BOTH ARE, ABOVE THE REAL LINE.`
6. **Anchors**: `−4 −2 1` in 1.6 mm caps, 3.2 mm under the axis at the true feet (x = 164.48 / 171.38 / 181.72).
7. **Captions**: bottom-left `UPPER HALF-PLANE, 0 ≤ T ≤ 97.35. 28 ZEROS. / ONE SCALE ON BOTH AXES: 3.45 MM PER UNIT.` Bottom-right `VERIFIED TO T = 3·10¹² (PLATT–TRUDGIAN 2021). NOT PROVED.`

## The science it encodes
- ζ is computed on the whole window and validated against mpmath at dps 30. The zero sets of Re ζ and Im ζ are drawn instead of |ζ| levels, because |ζ| contours carry the reference's left–right mirror lie (encoding §9.4).
- **Verified by the science critic (r03):**
  - every hairline vertex is within 0.089 mm of Im ζ = 0, every black vertex within 0.017 mm of Re ζ = 0, and every red vertex within 0.023 mm of its branch;
  - 1,114 scanline sign changes have 0 misses;
  - the X's are 88.1°–90.0° at 0.4 mm chord;
  - the Im-arm tilts at ρ₁ / ρ₂ / ρ₄ are −9.05° / +12.64° / +30.79°;
  - the rulings are exact.
- **Honest limits:**
  - No primes are on this plate; they belong to the faithful flavour.
  - `1` is the pole, not a zero, and the sheet does not yet say so in words (S6).
  - Above γ₂₀ the red reads as a hook at 1 m because the tongue tips curl inside r = 1.6 mm. This is true geometry and must not be straightened (S8).

## Plot (Leo, after the holidays)
| order | layer | pen | strokes | draw | plate-job min |
|---|---|---|---|---|---|
| 1 | hairline Im ζ = 0 | black 0.1 | 89 | 13.75 m | ≈ 31 |
| 2 | black Re ζ = 0 | black 0.3 | 79 | 11.35 m | ≈ 26 |
| 3 | type | black 0.3 (**same pen: skip the swap prompt**) | 597 | 3.70 m | ≈ 28 |
| 4 | red ρₙ | red 0.5 | 56 | 0.21 m | ≈ 3 |

- Minutes are from `promptplot plot plate <gcode> --layers 0,1,2,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`, at feed ≤ 500 and dwell ≥ 1 s: **ETA ≈ 94 min**.
- 3 physical pens and 2 real swaps. The dry-run prompts 4 times; skip the colour 1 → 2 prompt.
- 821 pen cycles, no dotted runs. The ink bbox is [15, 282] × [15.1, 403.4].
- **A3 only.** An A5 Leo edition is a re-window (t ≤ 52, ≈ 10 crosses, ≥ 2.9 mm/u), not a scale-down (encoding §10). Always trace the pen-up frame first.

## How it got here
- **r01** `faithful`: the reference's centred architecture, corrected (mirror top–bottom, ψ₁₀₀ prime footer). It failed on a centred ">" emblem and a key contradicted on the axis. Kept as the prime-carrying flavour.
- **r02** `abstract`: the LeWitt instruction drawing, a one-sided comb and an undrawn column. Double PASS, but the gate failed on red knots (the 0.5 nib drawn twice).
- **r03** (current): r02's field byte-identical. Red is one pass. The key is restricted to above the real line. The anchors are added. The head is registered on x = 180, and the series caption is on x = 206.

## Keep — what works
- **The undrawn column**: 28 exact red crosses on a line that is not there, and the one-sided comb carries the "not a mirror" correction by itself.
- **Exactness end to end**: the truth record above. Every mark is ζ's.
- **Two verticals organise the sheet**: x = 180 (implied by the tongue tips, the title end and the statement end) and x = 206 (caption, wall label, colophon). Plus the shared x = 15 edge.
- **The wall label set between ζ's own rulings**: the key is the instruction.
- **One-pass red**: no knots, and cream shows in all four quadrants.

## Weak — what doesn't
- [hierarchy] Red at 3 m is a thin stitched seam, not a column of shouts. Its loudness was deliberately traded away to fix the knots.
- [accent] From γ₂₀ up the crosses read as hooks (A5). Honest lever: a re-window, not a heavier mark.
- [legibility] `1` under the pole foot can be misread as a third trivial zero (S6).
- [cost] Type costs 28 min for 3.7 m of ink, because a stroke-font wall label is expensive.

## Next versions
- **If only iterating (r04, parent r03):** add one caption phrase naming `−4, −2` as zeros and `1` as the pole (S6). Nothing else moves: not the field, the red or the grid.
- **Louder-accent re-window**: fewer zeros at a larger scale (e.g. t ≤ 52, 10 crosses), so every mark is a full X. This is also the natural A5 Leo edition.
- **faithful** (r01): the mirror and the real primes, if Juan wants the prime companion. Start from ledger A4 / S5.
