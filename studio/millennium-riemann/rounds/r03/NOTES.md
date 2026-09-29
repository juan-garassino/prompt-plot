# millennium-riemann r03 — iterate (abstract, polish) · parent: r02 · 2026-09-29

Lineage (unchanged): **Sol LeWitt, *Wall Drawing #46* (1970)**. An instruction is executed exactly,
and its text could redraw the wall. Canon: SWISS sheet, flat on purpose. ORDER: INTERLACED /
LAMINAR. Work order: `rounds/r02/SYNTH.md`. It is a polish round, and **the field is not touched**.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-riemann/rounds/r03/piece.py \
  --fn riemann_two_instructions --seed 7 --paper a3 --margin 15 \
  --palette dimgray,black,black,crimson --out gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.png
.venv/bin/python studio/millennium-riemann/rounds/r03/render_truewidth.py \
  gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.gcode gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2_phys.png 0 0 297 420 5
```
- **Final PNG:** `gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.png`. Pen 0 (the 0.1 hairline) is
  previewed in dimgray.
- **Physical-width preview (judge on this):** `gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2_phys.png`.
  It is drawn with 0.1 / 0.3 / 0.3 / 0.5 round nibs on cream, supersampled 4×.
- **GCODE:** `gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.gcode`
- **Seed 7.** The piece uses no randomness. The seed-11 gcode is byte-identical, comments aside.
- **Self-rounds:**
  - v1: red single pass plus all the type mandates.
  - v2: pen-cycle economy in the text layer. Nothing visible changed.
- **Audit:** `.venv/bin/python studio/millennium-riemann/rounds/r03/audit_r03.py`
- **Field data:** read, unchanged, from `../r02/xray_abstract.json`. It is not copied, so it cannot drift.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | One pass of red. Two arms with cream in all 4 quadrants in the 1:1 crop x 170–190, y 330–368. 56 one-way strokes | **FIXED.** Each arm is now the true curve `ra` / `rb` drawn once, one-way, from exit(R+0.2) to exit(R+0.2). The out-and-back ±0.15 mm offset pair is deleted. The red layer has 56 strokes and 0.21 m of ink (r02: 0.43 m). The longest stroke is 4.1 mm. Audit: **0 of 56 arms come back under their own nib** (arc gap > 1 mm, distance < 0.5 mm). The two arms of a cross overlap only within **0.516 mm of the centre**, which is the geometric minimum for a 0.5 nib at 90°. In the true-width crop of γ₂₄–γ₂₈, every mark is two thin arcs crossing, with cream in all four quadrants and no blob. The **0.5 nib is kept** because the 0.3 fallback was not needed. r = 1.6 mm and RED_OVER = 0.2 mm are unchanged. |
| S1 | Key must read `3 RED — WHERE BOTH ARE, ABOVE THE REAL LINE.` | **FIXED.** The block uses the same heading-plus-instruction form as blocks 1 and 2: `3  RED` / `WHERE BOTH ARE,` / `ABOVE THE REAL LINE.` The sentence is too wide for one 76 mm line at 2.2 mm caps, so it breaks at the comma. The trivial-zero meetings on y = 32 and the pole foot are now outside the key's claim, and the key matches the statement ("ABOVE THE REAL LINE"). |
| S2 | `−4 −2 1` at x = 164.48 / 171.38 / 181.72, y ≈ 28, 1.6 mm caps, centred | **FIXED.** Positions are computed, not typed: sx(−4) = 164.475, sx(−2) = 171.375, sx(1) = 181.725. Each numeral string's ink box is centred on its foot, and the cap mid-height sits at y = 28.0 (baseline 27.2, top 28.8). Clearance to the real axis and the feet is **3.20 mm** for all three. The `1` ink spans x 181.46–181.99, so it clears the column. It is asserted that no numeral vertex lies within 0.5 mm of x = 180. The bottom-left caption ends at x = 110.26, far from the numerals. |
| A2a | Every `1 BLACK` glyph ≥ 2.5 mm from its rulings | **FIXED.** Each label block's **ink box, descenders included**, is centred between the **actual** field lines measured over its own x-span. r02 centred between the nominal kπ/ln 2 values, but the real rulings sit about 0.2 mm off those near x = 206, and the ζ descender was not counted. The lead is tightened from 1.75 to 1.6 cap for all three blocks. Every glyph is then asserted ≥ 2.5 mm from every hairline/black run. Measured centreline clearance: **k=20 2.76 mm · k=19 2.88 mm · k=18 3.20 mm** (r02 k=20: 2.25). |
| A2b | Statement ends on x = 180 | **FIXED.** The tracking is solved from the last glyph's real ink extent (`solve_track`): track = 0.649 mm at a 2.5 mm cap (r02 used 0.30). The '.' ink ends on x = 180.000, directly under the title's last pass. The statement stays above the field (y = 384 > 367.86), so nothing is drawn on the column. |
| A2c | r01 series caption flush-left at x = 206, ≤ 2.2 mm caps, cap line on the title's cap line, must not cross x = 282 | **FIXED.** `MILLENNIUM PRIZE PROBLEMS  1 / 7` / `CLAY MATHEMATICS INSTITUTE, 2000` are set at 2.2 mm caps with track 0.22 mm (the wall label's), and the line pitch is 3.96 mm. The first line's cap line is at y = 403.36, which is the title's outer-pass cap line (395 + 8 + 0.36). Both lines are asserted to end ≤ 282. They measure about 278, so the block is near-justified against the frame. |
| A3 | HANDOFF quotes plate-job minutes, not "80 min at F600" | **FIXED.** The minutes come from `plot plate … --dry-run` on the v2 gcode: **31 / 26 / 28 / 3 min, ETA ≈ 94 min** at feed ≤ 500, dwell ≥ 1 s and 90 s per swap. The text layer went from 24 to 28 min because the mandated type (caption, a third key line, numerals) adds about 100 glyph strokes. Title chaining claws back 21 of those pen-downs. The optional F600 wrapper was not done: the plate job already caps the feed. |
| S3 | real primes | ARGUED earlier (closed 2026-09-29). r03 carries no ψ footer, as the SYNTH requires. |
| S4 | \|ζ\| contour field | ARGUED earlier (closed 2026-09-29). Encoding §9.4. |
| A4, S5 | r01 mandates | DROPPED earlier. r01 is not the parent. |
| gate | studio regression + `make check` clean before vote | **DEFERRED to the lead.** `scripts/studio_regression.py` was launched on this machine at load ~210. See the report for its state at hand-in. `make check` was not run here, because the coverage run writes shared report files while sibling agents are active. r03 edits nothing under `promptplot/`. |

## What changed from parent

Nothing in the field moved. Every change is a mark-making or type decision:
1. **The claim's mark is drawn once.** Each red arm is one one-way stroke along the true curve.
   The out-and-back 0.8 mm band that made knots is gone. The accent is now a crisp X or curled X
   at 0.5 mm rather than a lump. Loudness was not added back with radius or passes.
2. **The head is one block registered on the column.** Title and statement both end on x = 180.
   The series caption on x = 206 shares the title's cap line, so the sheet's head now has the same
   two verticals as its body (180 implied, 206 drawn by type).
3. **The key agrees with the sheet.** The RED instruction now says "ABOVE THE REAL LINE" and has
   the same three-line shape as BLACK and HAIRLINE. The three label blocks are optically centred
   in their ruling bands using the real curves.
4. **σ = ½ is anchored without drawing it.** The numerals −4, −2 and 1 sit under the true feet.
   With 3.45 mm/u, a stranger can count that the red column is ½ unit left of the pole foot.
5. **Plotting economy (invisible).**
   - Glyph strokes that share an endpoint are chained.
   - The title's corner-split pieces are re-joined into one pen-down per glyph stroke. The hop sits
     inside the 1 mm glyph mass.
   - The text layer is now ordered bottom-up by nearest end, like the field layers.
   - Result: text 625 → 597 strokes, travel 5.30 → 4.96 m.

## Measurements / computations

- Red centre miss (curve to exact (½, γₙ)): max **0.0178 mm**, the same as r02. There are 28 centres
  on x = 180, the lowest red ink is at y = 79.09, and the lowest centre is at y = 80.77.
- Arm angles are unchanged from r02, because the curves are unchanged. For example γ₁: A +80.2°,
  B −9.1°, diff 89.3°.
- Ink right/left of x = 180, field layers only (hair + black + red, measured above the axis):
  2.29 m / 22.75 m = **10.10 %**. r02 measured **10.45 %** by this same method. The drop comes from
  halving the red; the critics' method gave 9.6–9.8 % for r02, so r03 is lower on theirs as well.
  Right-side ink is ζ's rulings and hooks only.
- The hairline and black layers are byte-for-byte r02's geometry. The run count, 89 / 79 strokes,
  and the 13.75 / 11.35 m of ink all match r02. The A–B minimum and the lone Gram crossings are
  therefore inherited unchanged.
- Label clearance is measured on 0.05 mm-densified glyph points against 0.05 mm-densified field
  polylines, centreline to centreline. The ruling bands measured at x 206–282 are k=20
  [344.906, 360.208], k=19 [329.179, 344.734] and k=18 [313.451, 329.099].
- Statement track is solved as (180 − 15 − 55·2.333 − 2.3·(2.5/6)) / 55 = 0.649 mm.

## Plot budget (v2 gcode; minutes from `plot plate --dry-run --batch-strokes 40`)

| order | layer | pen | strokes | draw | travel | longest | plate-job min |
|---|---|---|---|---|---|---|---|
| 1 | HAIRLINE Im ζ = 0 | black 0.1 | 89 | 13.75 m | 0.87 m | 286 mm | ≈ 31 |
| 2 | BLACK Re ζ = 0 | black 0.3 | 79 | 11.35 m | 0.87 m | 203 mm | ≈ 26 |
| 3 | TEXT | black 0.3 (same pen, no swap) | 597 | 3.70 m | 2.54 m | 132 mm | ≈ 28 |
| 4 | RED ρₙ | red 0.5 | 56 | 0.21 m | 0.68 m | 4 mm | ≈ 3 |
| | **total** | 3 physical pens, 2 swaps | 821 pen cycles | 29.01 m | 4.96 m | | **ETA ≈ 94 min** |

- Travel is attributed to the layer that precedes each move.
- 11,256 commands. `preview --score`: grade A.
- Ink bbox [15.0, 282.0] × [15.08, 403.36]. Bounds are ok at A3 portrait with margin 15.
- There are no dotted runs.
- The sheet is A3 only, as designed; an A5 Leo edition would be a re-window (encoding §10).

## Self-critique (seven dimensions)

1. **Hierarchy 8.** The comb still dominates and the title is second. The red is now the third
   voice and is quieter than in r02: crisp at 1:1, a fine seam at arm's length.
2. **Grid & alignment 9.** Head and statement both end on 180. The caption, label and colophon are
   all on 206. The caption shares the title's cap line. The label blocks are optically centred on
   the real rulings.
3. **Tension & asymmetry 9.** Unchanged: 62 : 38, with the comb bleeding off the left.
4. **Negative space 8.** Unchanged. The upper right now carries the caption, which fills the one
   un-registered corner the series grammar asked for.
5. **Craft for pen 9.** No spot is inked twice under the red nib outside the centre. Red is one
   one-way pen-down per arm. The text layer has 28 fewer pen-downs than a naive set, and its travel
   is ordered.
6. **Concept legibility 9.** The key no longer lies on the axis, and the numerals let the column be
   checked as Re s = ½.
7. **Depth 7 (declared flat).** Unchanged.

**The single worst thing:** the red accent is now honest but small. At 3–4 m it reads as a
thin red seam of 28 hooks rather than a column of shouts. The top ~10 crosses are curled Xs
because the tongue tips turn inside about 1 mm (exact, see r02). The SYNTH forbids buying back
loudness with radius, passes or nib, so this is accepted. If Juan wants it louder, the honest lever
is fewer zeros at a larger scale (a re-window), not a heavier mark.

The second worst: the text layer costs 28 min for 3.7 m of ink. That is 597 pen cycles of
2.2 mm type, and it is inherent to a stroke-font wall label.

## Engine requests

- `scripts/render_candidate.py` should accept `--pen-widths` so that the official PNG shows nib
  weight. r03 ships a round-local 4× supersampled true-width raster (`render_truewidth.py`, round
  joins and caps) as the stand-in.
- `kit` could offer a `chain_glyph` / corner-safe heavy-type helper. Both are round-local here.
