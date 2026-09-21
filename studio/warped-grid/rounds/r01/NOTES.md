# WARPED GRID — r01

Exact recreation of `studio/warped-grid/ref/reference.png` (1086 × 1448).
Entry point: `piece.py::warped_grid(rng, bounds, colors=5)`.

```
.venv/bin/python scripts/render_candidate.py studio/warped-grid/rounds/r01/piece.py \
  --fn warped_grid --seed 7 --colors 5 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black \
  --out ~/Downloads/pp_warped_grid_v1.png
```

Pens: 0 red (Q) · 1 blue (K) · 2 ochre (V) · 3 green (Z) · 4 black (lattice, A,
type, furniture). `colors < 5` folds pen indices with `_Sheet.pen()`, so the
piece still runs on a 3-pen or 1-pen caller.

## Plot budget (A4 portrait, 10 mm margins)

| pen | | draw | pen-downs |
|---|---|---|---|
| 0 | red | 2 718 mm | 99 |
| 1 | blue | 2 560 mm | 99 |
| 2 | ochre | 2 278 mm | 81 |
| 3 | green | 1 789 mm | 59 |
| 4 | black | 5 315 mm | 913 |
| **total** | | **14 661 mm** | **1 251** |

Travel after `merge_chunks` optimisation: **8 996 mm**. 63 070 commands.
Black's pen-down count is high because every lattice node, every plane node and
every graduated dot is its own short stroke; that is the plate.

## Method

Everything is authored in REFERENCE PIXELS and mapped to millimetres once, in
`_Sheet`. The plate is 3:4, the A4 drawable area is 190 × 277 mm, so the fit is
width-limited: 1 ref px = 0.17496 mm, the sheet sits centred with 11.8 mm of
extra air top and bottom.

Positions were **measured off the raster**, not judged:

- colour masks by hue (red ≈ 0°, ochre ≈ 35°, green ≈ 135°, blue ≈ 205°) →
  cluster bounding boxes and the four/four/three nest centres per cluster;
- box-blurred density peaks → nest centres (Q 158,220 · 266,131 · 397,268 ·
  261,325; K 694,220 · 807,143 · 908,268 · 824,366; V 886,1000 · 773,1074 ·
  856,1138);
- connected components → every label's footprint, the brackets, the dot
  columns, the furniture;
- row/column scans of the lattice box → node rows at y 462.7 / 481.6 / 499.8 /
  517.3 … 692.6 and the outer column x 420 → 662;
- row scans at y 805 / 926 / 945 → the A plane's back edge (372 → 712) and
  front edge (288 → 796).

Type is sized from the measured FOOTPRINT, not from the cap height: this font
is wider per cap than the plate's serif, so matching height alone overran by
~40%. `(n × d)` measures 54 × 14 px on the plate; `"(n x d)"` at cap 12.2 px
measures 55 px. `softmax` is 95 px wide on the plate → cap 16.2 px.
`Z = AV` is 108 px wide → cap 24 px (its cap on the plate is 27 px).

## What the toolkit bought, and where it needed help

- **`kit.even_contour_levels(field, spacing, quantile=0.82)`** picks the level
  step for every nest and for A's peaks. On this field it always returns a step
  FINER than the pen floor, so `_nest_levels` takes the max of it and an exact
  safety step. The safety step is analytic here: the cusp profile has
  `|dF/dr| = amp/(g0 + slope*r)`, so a level step of `amp_max` puts the
  innermost ring of the tallest cusp exactly `g0` from its neighbour.
- **Conical cusps, not Gaussians** — and not plain exponentials either. A
  Gaussian spreads its rings at the summit; `a·exp(−r/σ)` spreads them
  exponentially OUTWARD (gap ∝ e^{r/σ}), which on this plate gave 6 rings where
  the reference has 15. Measuring the reference's own ring radii (7.2, 12, 18.3,
  25, 32.8 … 154 px → gaps 4.8, 6.3, 6.7 … 19) shows the gap growing roughly
  LINEARLY with r. `_cusp_profile` integrates `1/(g0 + slope·r)`, so arithmetic
  levels land rings exactly `g0 + slope·r` apart: 0.88 mm at the eye, 2.0 mm at
  the rim, 13–14 rings on a big nest. Same lesson as before — more rings at a
  fixed pitch floor only come from a physically bigger eye, and here the
  profile makes that trade explicit.
- **Marching squares cannot draw the eye.** At a 0.82 mm grid pitch every ring
  under ~5 mm radius came back as crumbs or vanished, which is the part of a
  spiral nest that carries the plate. `_nest_eyes` emits those rings as EXACT
  circles (near its own summit a cusp is isolated, so the iso-line is a circle),
  `_too_small` drops the chains they replace, and the switch radius is
  `min(0.46·nearest-peak-distance, 0.60·rmax)` so the two passes are exactly
  complementary. A's peaks use the same split, with the circle projected through
  the plane map and lifted by its own level.
- **`kit.fill_disc` / `kit.circle` / `_stroke_text(proportional=True)` /
  `_catmull_subdivide` / `_marching_squares` / `_chain_segments`** used as-is.
- `tone_dots` was not needed: there is no tonal fill on this plate.

## Spacing

Guaranteed by construction, not by cleanup:

- nest rings: `g0 = 0.88 mm` at the eye, opening to ~2.0 mm at the rim;
- A's contours: level step = `amp_max` = 0.83 mm of vertical lift per ring;
- lattice core: `_LAT_FLOOR = 0.24` residual scale holds the innermost node
  ring ~0.86 mm off the centre;
- Z profiles: `amp_floor = 40 px` gives ~0.65 mm between profiles in the
  VALLEYS (the reference runs the same there) and 2.1 mm at the peak. Without
  that floor the profiles collapse onto the base line wherever the landscape is
  flat — 0.2 mm apart, a solid green bar. That was the single worst spacing bug
  in the piece (pen 3 went from 77% of samples under 0.8 mm to 28%).
- fans leave the eye on a short ARC (`r0 = 3 mm`), not from one point; six
  strokes sharing an origin stack inside the pen width for their first
  millimetres.

A parallel-neighbour audit still reports sub-0.8 mm samples at three places,
all of them deliberate and all of them present in the reference: the contour
SADDLES on A where two peaks' skirts meet, the fan CONVERGENCE at each arrow
tip, and the two Z anchors where the whole stack converges into a ring.

## Overlap decisions (house law)

- **Kept:** the crowding at the lattice pinch — that is the subject. The ochre
  V→A sweeps crossing the plane's front edge, and the black droplines crossing
  the Z stack: those tie two stages together.
- **Removed:** the dashed halos crossing letterforms, brackets and dot columns.
  `_TYPE_KEEPOUT` lists every label's padded footprint and halo dashes inside
  one are dropped — type wins, geometry yields. Nest sizes were pulled in
  (Q's big nest rmax 112 → 98 px) so the outermost contour clears the `Q`
  rather than grazing it.
- **Removed:** the ghost rows. The plate draws the undistorted row heights at
  25% grey straight across the lattice; one pen cannot, and dashing them across
  the field turned the whole hero into a striped background. They survive as
  short rules in the margins either side, where they read as a datum and share
  the space with nothing.
- **Removed:** the nest eye dots were sized to "look right" and swallowed the
  two innermost rings; they are now sized to fit INSIDE the innermost ring.

## The lattice warp

The one thing that resisted a clean law. Measured off the plate:

- the top and bottom rows dive ~58–74 px at the centre — 50–64% of the
  half-height;
- the outer columns slide inward only ~6–8 px over the whole height;
- at mid-height the columns sit at ±4, 10, 24, 48, 95, 115 px from the centre
  (nominal ±20, 40, 60, 81, 101, 121) — a cliff between the 5th and 4th column;
- at the centre line the rows sit at 0, 7, 13, 20, 26, 33, 41 px — a near
  uniform 0.35 scale;
- the corners do not move.

No isotropic lens does both the dive and the non-sliding columns, and the
narrow-window versions I tried (gaussian, quartic, sextic, separable) all
produced two rigid halves either side of a waist instead of one deformed
fabric. What ships is a power-law radial compression `r' = rc·(r/rc)^p` on a
metric that stretches x by 2.1 (so a horizontal displacement "costs" more than
a vertical one), with `p − 1 = 1.45`, a `0.24` residual floor for pen safety,
and a damping term that leaves the top/bottom rows their own x-spacing and the
outer columns their own y-spacing. Against the measured numbers: columns at
mid-height 5 / 14 / 27 / 49 / 73 / 108 px, rows on the centre line 5 / 10 /
16 / 26 / 37 / 50 px, corners fixed.

## Three things furthest from the reference

1. **The lattice's deformation law.** Mine reads as one deformed fabric with a
   dense core and pinned corners, but the reference's bowl is broader and its
   knot is denser and rounder; my top and bottom edges close into a slightly
   sharper V and my outer columns slide ~12 px where the plate's slide ~6. The
   reference is an AI render and its warp is not a clean map — this is a
   plausible law fitted to it, not the law.
2. **The spiral nests are radially symmetric.** The plate's Q/K/V nests are
   elongated, organically lobed fields with narrow necks between them; mine are
   sums of isotropic cusps, so they read as concentric circles with rounded
   merges. The fix is a per-nest anisotropic metric (ellipse + rotation) inside
   `_field`, `_cusp_radius` and `_nest_eyes` — the eyes would become ellipses,
   which is what the plate actually draws.
3. **Serif / italic type — known permanent gap, recorded, not chased.** The
   plate sets `Q K A V`, `Z = AV` and `Q · Kᵀ` in a serif roman/italic; the
   shared single-stroke font is a geometric sans, so the display letters read
   as a different typeface however well the metrics match.

## Font gaps for the shared table

- **`×` (U+00D7, multiplication sign) is missing.** Every shape annotation on
  this plate is `( n × d )` / `( n × n )`; I set them with lowercase `x`, which
  is close at 2.5 mm but is the wrong glyph. Worth adding centrally.
- **`·` (U+00B7, middle dot) is missing.** `Q · Kᵀ` uses a drawn dot mark at
  mid-height instead of a glyph.
- Superscript `ᵀ` is set as a small `T` raised 13 px — fine, no glyph needed.

Everything else the plate needs (lowercase for `softmax`, parentheses, `=`) is
present and `proportional=True` metrics matched the measured footprints.

## Note on the tree

Mid-session `promptplot/generative/generators.py` was reverted by a sibling
agent and the package stopped importing (`engine/kit.py` imports
`_glyph_advance`, which the reverted file did not have). It came back ~20 s
later. Nothing here touches `promptplot/`; no git checkout/restore/stash was
run from this task.
