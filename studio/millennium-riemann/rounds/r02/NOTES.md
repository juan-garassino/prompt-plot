# millennium-riemann r02 — abstract · parent: none · 2026-09-28

Lineage: **Sol LeWitt, *Wall Drawing #46* (1970)**: an instruction executed exactly, whose text
could redraw the wall. ζ supplies two instructions, BLACK = every point where Re ζ(s) = 0 and
HAIRLINE = every point where Im ζ(s) = 0. RED marks where both hold. The wall label is printed on
the sheet. Canon: SWISS sheet carrying a conceptual instruction drawing. **The plate is flat on
purpose.** The 90° at every red cross exists only on a flat, isotropic plane.
ORDER: INTERLACED / LAMINAR.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-riemann/rounds/r02/piece.py \
  --fn riemann_two_instructions --seed 7 --paper a3 --margin 15 \
  --palette dimgray,black,black,crimson --out gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.png
```
- PNG: `gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.png`. Pen 0 is a black 0.1 nib. The
  render script cannot draw nib widths, so it is previewed in dimgray.
- Physical-width preview: `gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6_phys.png`. Every stroke
  is drawn at its nib width on cream. Use this one to judge weight.
- GCODE: `gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6.gcode`
- Seed 7. The piece uses no randomness: seeds 7 and 11 give byte-identical gcode (checked).
- Self-rounds v1 to v6 (see "What changed").

## Mandate responses

| id | mandate | status |
|---|---|---|
| — | No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exists for this slug yet, so there are no open J*/A*/S* rows. The binding brief is encoding.md §4, §5A, §9 and §11 plus the curator note. | n/a |
| curator | exact ζ, real zeros, real primes | FIXED. Every curve is a level-0 set of ζ computed here. The 28 red centres are γ_n read from `data/zeros.json`. Primes appear only through the explicit formula, which belongs to the faithful thesis. [A] draws no prime (encoding §4). |
| curator | one clean layer per pen, stated order, batchable, minutes per layer | FIXED. Layers run 0 → 1 → 2 → 3 in one contiguous sequence each (checked in the gcode). Longest stroke is 286 mm. Minutes per layer are listed below. There are no dotted runs. |
| curator | name the LINEAGE | FIXED. LeWitt, WD #46. The curator should verify the wording against the catalogue raisonné. |
| enc §11.1 | one column: 28 red crosses, centres ±0.3 mm on x = 180, none within 48.8 mm of the baseline | FIXED. Red centres are the exact (½, γ_n). The drawn curves pass within ≤ 0.018 mm of them. The lowest red is at y = 80.76, which leaves 48.76 mm of empty column. |
| enc §11.2 | right angles that tilt | FIXED. Measured from the contour data (0.12 u window), the crossings are 90° ± 2.5° worst case over all 28. The Im-branch at ρ1, ρ2, ρ4 sits at −9.01°, +12.63°, +30.83°, and −arg ζ′ gives −9.05°, +12.64°, +30.79°. |
| enc §11.3 | right-of-column ink ≤ 10 % of left | **ARGUED (marginal fail).** Field layers measure 2.39 m right against 22.88 m left (10.5 %). All layers, with type and the axis, give 12.7 %. The right-hand ink is only ζ's own rulings t = kπ/ln 2 (21 of them, flat to < 0.15 mm by σ = 8), plus tongue tips reaching σ ≤ 0.715 and the hairline hooks at Gram points. Nothing was added for balance and nothing can be removed without breaking "lines run to the frame". Moving the column right (X0 ≈ 186) would pass the check. It would also move σ = ½ off the 62 % line and force a data window beyond σ = −48, so I left the encoding's geometry as it is. |
| enc §11.4 | no other meetings | FIXED by construction: these are two exact zero sets. Spacing measured from the gcode: black↔hairline min 1.01 mm (at the fan's feet just above the axis, y = 33). Outside the red circles and the axis there are **0 approaches under 0.8 mm**. Half-Gram tongue tips and Gram-point hairlines cross the column alone and stay visible. |
| enc §11.5 | plottable and clean | FIXED. 4 layers in order, 2 physical swaps. No type touches the comb. Bounds are clean in v6 (v1 had 2 clamps from the title's offset passes). |

## What changed from parent (no parent — the self-rounds)

- **v1.** Built the encoding §5A sheet from the recomputed X-ray: the comb bleeds off the left
  frame, x = 180 is left undrawn, the ruled quiet field is on the right, and the LeWitt wall label
  sits between the rulings.
- **v2.** Made the title heavy (5 chained passes of the 0.3 nib, about 1 mm). It is the clear
  second in the hierarchy, as Swiss type-as-mass asks. Put the right colophon flush-left on the
  x = 206 label axis, so the sheet has three verticals: 15, 180 (implied), 206. Fixed the 2 bounds
  clamps.
- **v3.** Title strokes now split at sharp corners before thickening. The averaged-normal offset
  was pinching the N/M diagonals.
- **v4.** Red is drawn as two passes 0.3 mm apart, out-and-back, so each arm is still one
  pen-down. This makes a ~0.8 mm band, and the column of crosses now reads at arm's length.
  Title set with a single word space.
- **v5.** Tried r = 1.3 mm to see whether the top crosses curl less. They do not: tongue tips
  there turn inside about 1 mm, so every radius curls. Reverted to the encoding's r = 1.6, which
  reads better at distance.
- **v6.** Tracking is now solved so the title's last glyph ends exactly on x = 180. The title
  spans the comb, and its end marks the undrawn column from outside the field. The HAIRLINE
  instruction was re-broken so both instructions end on the same words, "PART OF ζ(S) IS ZERO."

## Measurements / computations

- **ζ on the grid:** `zeta_np.py`. This is the textbook method: Euler–Maclaurin (N = 100,
  24 Bernoulli terms) for Re s ≥ ½, and the functional equation ζ(s) = χ(s) ζ(1−s) with a
  Stirling log-Γ (12 terms, shifted to Re ≥ 25) on the left. I used it because the shared machine
  sat at load ~390, and mpmath.fp.zeta at ~1 ms/point × 3.1 M points would have taken hours.
  **Validation against mpmath.zeta at dps 30 on 4 000 random window points:** max relative
  error 1.6e-13, median 9.8e-15, and **sign agreement of Re and Im = 100 %** (printed by
  `compute_abstract.py --check`, stored in the json).
- **Grid:** σ ∈ [−48, 31] at 0.05 (1 581 columns). The t rows are half-step, 0.025 + 0.05k up to
  98.025, plus the conjugate row t = −0.025. The real axis therefore falls between rows and s = 1
  is never evaluated. Marching squares is contourpy at level 0, with no smoothing. RDP thinning at
  0.02 mm removes only collinear grid steps; the grid itself is 0.17 mm.
- **Checks against dossier §7, all reproduced from this round's data:**
  - Re ζ = 0 crosses σ = ½ at 14.1358, 14.517†, 20.6557†, 21.0216, 25.0118, 25.4904†, 29.7393†,
    30.4249, 32.9355, 33.6237†.
  - Im ζ = 0 crosses at 3.4363, 9.6669*, 14.1347, 17.8456*, 21.0221, 23.1703*, 25.0107,
    27.6702*, 30.4249, 31.718*, 32.9348, 35.4672*.
  - At σ = 30 the rulings sit at t = 4.532, 9.065, 13.597, 18.129, 22.662 (kπ/ln 2 = 4.532,
    9.065, 13.597, 18.129, 22.662).
  - Max σ reached by a Re = 0 tongue for t > 2 is 0.7151 (dossier: 0.715).
  - Also present: the pen-A arc from −2 to the pole, and pen-A feet landing at 90° on the axis at
    the trivial zeros.
- **Sheet:** x = 180 + 3.45(σ − ½), y = 32 + 3.45 t. The window is σ ∈ [−47.33, 30.07],
  t ∈ [0, 97.35] (the mid-gap of γ28 = 95.871 and γ29 = 98.831). 28 zeros.
- **Red substitution:** find the curve of each family that passes the zero (closest segment,
  miss ≤ 0.018 mm) and walk along it from the zero. Black is cut at r = 1.6 mm. Red runs the true
  curve out to r + 0.2 mm. Only that passage is cut. Every other line, and every other passage of
  the same line through the circle (for example the half-Gram leg), stays black.
- **Title tracking** is solved: (180 − 0.36) − (15 + 0.36) − ink width = 17 × track, which
  gives track = 1.88 mm at an 8 mm cap.

## Plot budget (from the v6 gcode; F600 ≈ 10 mm/s draw, 2.5 s per pen cycle)

| order | layer | pen | strokes | draw | travel | longest stroke | est. |
|---|---|---|---|---|---|---|---|
| 1 | HAIRLINE Im ζ = 0 | black 0.1 | 89 | 13.75 m | 0.84 m | 286 mm | ≈ 27 min |
| 2 | BLACK Re ζ = 0 | black 0.3 | 79 | 11.35 m | 0.87 m | 203 mm | ≈ 23 min |
| 3 | TEXT | black 0.3 (no swap) | 499 | 3.29 m | 2.48 m | 118 mm | ≈ 27 min |
| 4 | RED ρ_n | red 0.5 | 56 | 0.43 m | 0.69 m | 9 mm | ≈ 3 min |
| | **total** | 3 physical pens, 2 swaps | 723 | 28.83 m | 4.91 m | | **≈ 80 min** |

- Command count is 11 006. `preview --score` gives grade A.
- Strokes over 300 mm are split at their U-tip.
- **A3 only as designed.** A4 is a uniform ×0.707, so the 1.01 mm minimum becomes 0.71 mm near
  the axis feet (under the floor). The comb interior (1.36 mm) becomes 0.96 mm.
- An A5 (Leo) edition must re-window per encoding §10. It is not a scale-down.

## Self-critique (rubric, honest)

1. **Hierarchy 8.** The comb dominates at 3 m. The heavy title is the clear second. The red
   column reads at 1 m. At 3 m it is a fine red seam, not a shout.
2. **Grid & alignment 8.** There are three verticals: 15, the undrawn 180 (registered by the
   title's end), and 206 (label and colophon). The type sits between ζ's own rulings. The
   statement's right end registers to nothing.
3. **Tension & asymmetry 9.** The split is 62 : 38, the comb bleeds off the left, and the fan's
   diagonal sweeps into the baseline. The seam is a straight edge that nobody drew.
4. **Negative space 8.** The quiet ruled field and the 48.8 mm red-free stretch are both true.
   The empty lower right between the axis and the first ruling is large but honest.
5. **Craft for pen 8.** 0 approaches under 0.8 mm, one pen-down per red arm, no dotted runs.
   The text layer is costly (499 cycles, ≈ 27 min), which is as long as a field layer.
6. **Concept legibility 8.** Crosses exist only in one column, set against an asymmetric picture.
   The label restates the instructions and does not explain them.
7. **Depth 7 (declared flat).** Swiss is flat by nature, and flatness is what makes the 90° true.
   The weight contrast (0.1 against 0.3) is the only recession.

**The single worst thing:** at the top of the column (γ ≳ 60) the tongue tips of both families
turn inside about 1 mm. At r = 1.6 mm the true red arms therefore curl into hook shapes
("Ж / Ƴ") instead of crisp right-angled Xs. It is exact (the 90° holds at the centre), but at
arm's length the upper crosses read as red squiggles, not crossings. A smaller r does not help;
only a larger scale (fewer zeros) would.

## Engine requests

- `scripts/render_candidate.py` should pass `pen_widths` through to
  `GCodeVisualizer.preview`. A 0.1 hairline and a 0.3 line render identically in the official
  png, so this round ships a second, physical-width preview and uses a dimgray palette slot as a
  stand-in.
- `kit._offset_polyline` pinches at sharp corners because it averages the normals. A miter-capped
  or corner-splitting variant for `giant_type` weights would help; this round splits glyph strokes
  at turns over 50° locally.
