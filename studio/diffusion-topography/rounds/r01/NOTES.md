# DIFFUSION AS TOPOGRAPHY — r01, exact recreation

Reference: `studio/diffusion-topography/ref/reference.png` (1448 × 1086).
Piece: `piece.py`, entry `diffusion_topography(rng, bounds, colors=4)`.
Render:

```
.venv/bin/python scripts/render_candidate.py studio/diffusion-topography/rounds/r01/piece.py \
  --fn diffusion_topography --seed 7 --colors 4 --paper a4 --orientation landscape \
  --palette dodgerblue,goldenrod,forestgreen,black --out ~/Downloads/pp_diffusion_topo_v1.png
```

Pens: 0 blue (data blob, forward flow) · 1 ochre (noise tangle, reverse flow, the
two red rule marks) · 2 green (sample terrain) · 3 black (score field, type,
furniture, dots).

## Method

Everything is authored in **reference pixel space** — coordinates transcribed off
a gridded 2× crop of the plate, quadrant by quadrant — and mapped once by `Ref`
onto the drawable area. That keeps the scatter honest: furniture sits where the
plate puts it, off-axis, rather than being re-derived onto a grid.

The map is aspect-preserving to within 6% (`sx = min(w/1448, sy·1.06)`). On A4
landscape that fills the full 277 mm width; the 6% horizontal stretch is
imperceptible and avoids letterboxing 23 mm of blank margin on each side.
Radii, dot sizes and type heights all scale by `sy`, so dots stay round.

Iterated over 14 rounds against a purpose-built comparison renderer that draws
the emitted GCode back into reference pixel space, so my output and the plate
could be stacked and 50/50 blended at identical scale.

## Fields contoured

| element | field | levels |
|---|---|---|
| `data x_0` | 8-term anisotropic Gaussian mixture: 7 rim lobes (σ 25–34 px) + one broad bridge at (198,170) σ 54 that keeps the interior rings nested instead of splitting into per-lobe bullseyes | 0.255 → 0.988 `fmax`, distance-stepped at 0.92 mm |
| `score ε_θ` | 13-term mixture: one narrow dominant peak (658,447) σ 36 plus 12 broad *shoulders* (w 0.13–0.48, σ 40–52) that bulge the level sets into the plate's star-lobed shape without becoming rival maxima | 0.030 → 0.988 `fmax`; outer 7 stepped at 2.1 mm and dashed, the nest at 0.92 mm |
| `sample x̂_0` | 14 bump/trough terms over (u, t), two narrow needle peaks (σu 0.030) at u 0.43 / 0.59 plus four negative troughs at the front, times a smooth `exp(-((u-0.5)/0.52)^4)` window | 24 ridgeline rows, hidden-line |

**Adaptive level selection** (`_even_levels`) is the piece's one real invention
and the thing that made the contours work. Evenly-spaced iso *values* bunch
wherever the field is steep — which is why the first eight rounds either flooded
solid or had to be thinned into crumbs. Instead the level steps by
`level += distance × quantile_0.82(|∇F|)` along the current contour, so rings sit
a fixed number of millimetres apart wherever they run. Using the **82nd
percentile** rather than the median matters: the gap between two rings is
narrowest where the field is steepest, so sizing by the median leaves the steep
stretches far under the pen tip. This let me drop `enforce_line_spacing` from the
blob and the score field entirely and keep every contour **continuous**, which is
the dominant visual property of the plate.

The terrain uses a front-to-back horizon buffer with a 0.76 mm clearance, so
rows that converge in the tails vanish cleanly instead of stacking into a slab.
The row *stacking offset* is windowed as well as the height, which is what makes
the terrain's left and right tails collapse to a single line, as on the plate.

The `schedule` tonal mass uses `tone_dots` (cell 1.0 mm, r 0.3) — tone drives the
probability a cell is inked, never the spacing, so it is bounded at 1 dot/mm²
and cannot read as solid.

## Measured

- draw **11.0 m**, travel **8.4 m** after the postprocess optimiser (12.1 m raw), **1891 pen cycles**, 44 745 commands
  (48 530 after the merge/postprocess pipeline).
- Line spacing, long strokes only (≥12 mm), % of resampled ink within 0.8 mm of a
  *different* stroke: blue 11.9%, green 14.6%, black 21.5%, **ochre 47.5%**.

Honest reading of that last number: the blue/green/black figures are contour and
ridgeline bundles designed at 0.92 mm that dip to ~0.7–0.8 mm where the local
gradient runs above the 82nd percentile — tight, not flooding. The ochre 47.5% is
the noise tangle, and it is different in kind: a scribble ball's contacts are
**transverse crossings**, not parallel-adjacent runs. Thinning it (tried at 0.62
and 0.80 mm) destroys the loops without reducing ink density meaningfully, so I
left it alone and cut the loop count to 36 instead. It reads as individual
wandering loops, which was the stated requirement.

## What I could not match

1. **Line density.** The plate is a raster. Its blob carries ~28 concentric rings
   across a 19 mm radius (0.66 mm pitch) and its terrain ~40 profiles across
   38 mm (0.9 mm, closing to ~0.3 mm in the flat band). Both are below what a
   0.5 mm pen can resolve. I draw 15–17 blob rings and 24 terrain rows. This is
   the single largest difference and it is a physical limit, not a modelling one.
2. **Type.** The plate is set in a serif/italic face with true subscripts
   (`ε_θ(x_t, t)`, italic `q(x_t | x_0)`, italic `x̂_0`). The shared font is
   monoline with no serifs and no italic, so all type reads upright and
   geometric. Subscripts are faked at 0.66× with a baseline drop. I set sizes and
   tracking by measuring the plate (label ascender 14 px, formula 13, caption cap
   11, title cap 15) so the type *blocks* match in width and position even though
   the letterforms do not.
3. **Missing glyphs.** The shared font lacks `ε`, `θ`, `^`, `_` and `|`, all of
   which the plate's labels need. `_EXTRA` in the piece supplies exactly those
   five on the same 4×6 cell — **reported upstream for central addition**, not a
   parallel alphabet.
4. **The red rule marks upper-left** are drawn in ochre. The plate's are a
   distinct salmon/crimson, which is a fifth colour; ochre is the nearest of the
   four pens.
5. **Grey values.** The plate modulates weight heavily — pale grey outer contours,
   faint blue hatch inside the blob, a soft grey terrain. A pen has one weight, so
   I substitute dash patterns where the plate goes pale (outer score contours, the
   stipple band inside the blob rim) and drop the faint hatch entirely.

## Other differences, smallest to largest

- Blob rings converge on two centres; the plate's converge on two centres plus a
  faint third in the upper-right lobe.
- The score field's outer dashed contours are smoother and more concentric than
  the plate's, which wander more.
- The flow curves are transcribed waypoint-by-waypoint but the plate's exact
  paths are not recoverable through the contour thicket; the fan, the crossings
  and the dot positions along them are matched, the precise curvature is not.
- The nested schedule ellipses number 7; the plate shows ~12 (0.8 mm floor again).
- `sample x̂_0`: the hat is a separate stroke over the `x`, not a composed glyph.
