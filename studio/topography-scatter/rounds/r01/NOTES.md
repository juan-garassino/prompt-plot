# ATTENTION AS TOPOGRAPHY — exact recreation, r01

Reference: `studio/topography-scatter/ref/reference.png` (1510 × 1041).
Entry point: `attention_as_topography(rng, bounds, colors=4)` in `piece.py`.
Pens: **0 red · 1 blue · 2 ochre · 3 black**.

Render:

```
.venv/bin/python scripts/render_candidate.py studio/topography-scatter/rounds/r01/piece.py \
  --fn attention_as_topography --seed 7 --paper a4 --orientation landscape --colors 4 \
  --palette crimson,dodgerblue,goldenrod,black --out ~/Downloads/pp_topo_scatter_v16.png
```

Plot cost (A4 landscape, 10 mm margins): **36 318 commands · 14 564 mm drawn ·
8 849 mm travel · 1 318 pen cycles**. Per pen: red 2 168 mm, blue 2 025 mm,
ochre 3 206 mm, black 7 165 mm. Nothing in `promptplot/` was modified by this
piece.

## Method

Everything is placed in normalised sheet coordinates `(u, v)` — `u` = 0 left…1
right, `v` = 0 top…1 bottom — read off the reference, then mapped into the
drawable area by `P(u, v)`. That keeps the piece paper-size-agnostic while
preserving the reference's asymmetric, deliberately off-grid placement.

Positions were **measured, not eyeballed**, wherever measurement was possible:

- **Blob silhouettes** — not invented. The red / blue / ochre pixel masks were
  box-blurred, the largest component isolated, and its boundary extracted with
  `_marching_squares` + `_chain_segments`, then resampled to 72 points. Those
  loops are baked in as `Q_OUT` / `K_OUT` / `V_OUT` and Catmull-smoothed at
  render time. So the amoeba outlines are the reference's actual outlines.
- **Black nodes** — a connected-component pass over the reference's dark pixels
  (filled, roughly circular, ≥ 5 px) gave 23 dot centres and radii; those are the
  `dots` table in `_furniture` and the `spec` table in `_dot_column`.
- **Dot column** — a column scan at `u ∈ [0.435, 0.475]` gave every dot's `v`
  and diameter, the little ring at `v = 0.634`, the dashed gap at 0.765–0.819
  and the plus bar at `v = 0.8415` with a 30 px half-width.
- **Contour nest** — a densest-30 px-window search over the `QK^T` region put the
  summit at `u = 0.4238, v = 0.4035`. That is exactly where the sharp gaussian sits.
- **Terrain profile** — a per-column topmost/bottommost black scan gave base
  `v = 0.838`, summit `v = 0.715` at `u = 0.700` (so 0.123 v ≈ 23 mm of relief),
  a second mass at `u ≈ 0.79`, and troughs to `v = 0.904`. `AMP`, `VBASE` and
  the peak/dip `u` positions are set from those numbers.

## How the expensive elements are made

**The scribble fills.** `_scribble()` lays a serpentine of rows at a fixed
perpendicular spacing and displaces every sample by smooth 2-D value noise
(`rng.noise2d`), so the rows meander instead of ruling. Each blob gets **two**
near-orthogonal passes at **0.86 mm and 0.92 mm**, then a 0.26 mm keyline band.
Runs are clipped by point-in-polygon against a 0.45 mm inward offset of the
traced outline.

There were three passes until r13. Two crossing passes at ~0.9 mm already put
effective coverage at roughly one pen width; the third (1.75 mm) pushed it past
that and the fill flooded solid. Dropped it — see "anti-crowding" below.

**The tonal fill in `softmax`.** Now `kit.tone_dots`. The obvious construction —
let tone drive the stipple spacing — floods the moment spacing falls under the
pen tip, which is exactly what v8 did at the dark end. `tone_dots` makes that
impossible: tone sets the *probability* a cell is inked, one dot per cell, cell
never below the tip, so peak density is capped at 1/cell² dots per mm². At
`cell = 0.85, r = 0.18` the ceiling is 1.38 dots/mm², which cannot read as solid.
The piece supplies `tone(x, y)` by inverting the ellipse transform to local
`(s, t)`, returning 0 outside the lens and a left-to-right ramp inside it — so
the lens shape and the rounded right tip are carried by the tone function, not
by clipping afterwards.

**The terrain.** This is a **profile stack**, not a hidden-line surface. The
reference's curves cross one another freely — near rows pass straight through
far ones — which a z-buffered `Scene3D.surface()` cannot produce and would
actively fight. So `_terrain` draws 25 rows of `h(u, v)` directly, where `h` is a
sum of 2-D gaussians whose **centres sit at or beyond the depth extremes**
(`cv = -0.12`, `cv = 1.12`, …) with large `sigma_v`. That makes each mass's height
vary *monotonically* from the far row to the near row, so the profiles open into
nested fans; two masses fanning in opposite depth directions cross, which is the
reference's whole character. Baseline drift between rows is tiny (0.009 v) —
essentially all of the vertical spread is height difference, which is why the
stack collapses to a thin bundle where the ground is flat and blooms at the
summits. A smoothstep envelope at both `u` ends produces the reference's
convergence to a point at left and right.

**The contour map** uses `_marching_squares` on a **domain-warped** field (the warp
is what stops the rings reading as a bullseye), with iso-levels chosen from a
nominal gaussian so ring *radii* grow like `k**1.08` — dense nest at the summit,
open rings on the flanks. The outermost two levels are drawn dashed.

## Anti-crowding (applied to every fill on the plate)

Per the standing rule, no fill on this plate lets tone or density drive spacing
below the pen tip:

| fill | mechanism | bound |
|---|---|---|
| `softmax` gradient | `tone_dots` | ≤ 1.38 dots/mm² at `cell = 0.85` |
| Q / K / V blobs | 2 × meandering serpentine | every pass ≥ 0.86 mm |
| black nodes (`_disc`) | spiral, pitch 0.34 mm (= tip), ≥ 3 turns | solid by intent, never overdrawn |
| filled square, keylines | fixed-pitch offsets | fixed |

`tone_hatch` is the parallel-line alternative if Juan wants to compare the
ellipse as lines rather than a cloud — the tone function is already written and
only the call site changes.

## Type

The shared font gained a lowercase alphabet and `_stroke_text` stopped
upper-casing, so the local glyph table this piece used to carry for `softmax`
has been deleted; the caption now sets lower case from the shared font.
`_tracked_text` remains as a thin wrapper that only overrides the *advance* —
the reference letterspaces the title wide (3.9 mm pitch at 2.8 mm caps) and sets
`softmax` slightly tight. `_bold_text` fakes weight by re-stroking each glyph on
a small circle.

## What I matched

- Landscape sheet, asymmetric scatter, large white reserves, elements off-axis.
- Q / K / V silhouettes (traced), their pens, their positions, their interior
  black nodes and the thin node-to-edge linework, the two loose red dots.
- Title block bottom-left, three lines of spaced caps at the measured 39 mm
  width, with the short rule below-right.
- `QK^T` with a raised T; `softmax` in lower case; `Z` and `Z = AV`.
- The contour map's position, footprint and tight summit nest; dashed outer rings
  plus the two dashed outriders that wander off right.
- The softmax ellipse's centre, length, height and slight upward tilt; the lens
  mass sitting left-of-centre inside it and ending well before the rim, ramping
  from nothing at the left tip to full density at the right.
- The dot column: every dot's height and size, the small ring, the threading
  spine, the dashed gap, the big plus, the lone dot at `v = 0.936`.
- The terrain's base height, relief, summit position, second mass, trough depth,
  left/right convergence, and the dashed tail onto its right-hand node.
- Connector bundles: red from Q rising then plunging into the contour's left
  flank (solid / dashed / dash-dot / fine variants), blue from K as a
  down-bulging hammock that lifts at the right, ochre from V sweeping far
  down-left and looping back into Z.
- Furniture: the top-middle arc-plus-step corner, the long verticals at
  `u = 0.300 / 0.4307 / 0.452`, the red dash-dot pair with its crossing rule, the
  dashed plus at `u ≈ 0.566`, the right-hand bracket and big quarter arc, the
  lower-left arc, the rectangle / bracket / filled square / long rule cluster at
  bottom right, and ~20 loose dots at their measured sizes.

## What I could not match, and why

- **Serif type.** The reference's `Q K V Z` and `QK^T` are a serif face. The
  shared font is **monoline geometric — no serifs, no italic, no stroke
  contrast**. Case is solved; the letterform is not, and it is not fixable from
  a piece file. Recorded as a permanent gap.
- **Hairline delicacy.** The reference was plotted with a very fine pen; every
  line is a true hairline and the sheet breathes. That is a pen choice, not a
  geometry choice — the matplotlib preview draws every stroke at the same visual
  weight, so my renders read heavier than the reference everywhere. On paper with
  a 0.1–0.2 mm nib the gap narrows considerably.
- **Fill saturation, in the other direction now.** The reference's blobs are a
  near-solid wash at what looks like ~0.3 mm pitch. Holding every pass at
  ≥ 0.86 mm and dropping the third pass means mine read as an open mesh —
  *lighter* than the reference, where earlier rounds were heavier. This is the
  deliberate cost of the anti-crowding rule and I have not tried to claw it back.
- **The reference's exact contour topology.** Domain warping gives irregular,
  organic rings, but not the reference's specific lobes — its left-flank concave
  notch and the particular rings that merge into figure-eights are accidents of
  that sheet's field and cannot be recovered from the image at ring level.
- **Photographic stipple.** The reference's softmax ramp is a continuous
  photographic gradient that goes genuinely black at the right. A bounded dot
  cloud tops out at mid-grey by construction. Right mechanism, lighter result —
  and per Juan's instruction, deliberately so.

## Differences a viewer would notice

1. **The blob fills are lighter and more open than the reference's**, which are
   solid saturated colour. Mine read as a fine mesh with the paper showing
   through — a direct consequence of the ≥ 0.86 mm-per-pass anti-crowding rule.
2. **The softmax mass is mid-grey, not black.** The reference ramps to a solid
   dark lens; the bounded dot cloud cannot, so the element reads lighter and more
   airy than the reference's, and the dark end is a texture rather than a mass.
3. **The contour blob is more convex than the reference's.** Mine is a warped
   ellipse; the reference is distinctly lobed, with a notch on the left and a
   tail running down-right, and its outer rings are more widely and unevenly
   spaced. The nest is also denser in mine — it approaches a solid spiral where
   the reference keeps visible white between its innermost rings.
4. Terrain rows bunch into a slightly heavier band along the base than the
   reference's do, and my summits are marginally rounder.
5. Connector bundles are more regularly spaced than the reference's, which fan
   with a looser, hand-placed rhythm — mine still read slightly "generated".
6. Labels are sans-serif (see above) and the loose furniture, while scattered,
   is a touch more uniform in length than the reference's.

## Rounds

16 renders. r1 established layout; r2 densified the scribble and fixed type
metrics; r3 added contour domain warp; r4 retuned terrain masses; **r5 was the
structural turn** — switching the terrain from small-`sigma_v` bumps (which piled
rows on top of each other) to large-`sigma_v`, edge-centred masses that fan;
r6–r9 folded in the pixel measurements (contour nest, terrain base/summit,
trough depth) and the blue hammock; r10–r12 spread the ochre front, moved the
red dive left, widened the contour footprint and lightened the keylines; **r13
replaced the softmax fill with `tone_dots`** and dropped the third scribble pass
after Juan flagged the flooding; r14–r16 tuned cell size, adopted the shared
lowercase font and gave the node discs a turn floor so they close instead of
printing as rings.
