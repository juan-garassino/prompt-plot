# neural-networks-cnn r04 — iterate · parent: r03 · 2026-09-29

Lineage: Georg Nees, *Schotter* (c. 1968). One element (a hidden-line profile row) under one
parameter (the map's resolution). Work order: r03 `SYNTH.md`, which asks for a rebuilt head.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/neural-networks-cnn/rounds/r04/piece.py \
  --fn cnn_one_summit --seed 7 --paper a4 --palette black,crimson \
  --out gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png
```

- Final: `gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png` + `.gcode`, seed 7, a4 portrait.
- Self-rounds: v6 (the unfinished draft already in this directory) through v14. All are kept.
  v8–v12 were rendered with the dev override `PP_CNN_SCALE=1.08`, which skips the sweep. v13,
  v14 and v15 ran the real sweep.
- The seed does nothing. `rng` is only handed to `Scene3D`, which never reads it.
- `maps.npz` and `compute_maps.py` are unchanged copies of r02/r03's. It is the same forward pass,
  not re-run.
- Runtime is about 5 min on this machine (load average around 300). Most of it is the scale sweep,
  which re-draws the real top plane 8 times.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | No schematics | **holds**. No rails, frustum, card edges or connectors. All crimson sits on a plane. |
| A2 | One grammar, pitch ≥ 1.0, no run < 3 mm, < 12k cmds | **holds**. Horizontal hidden-line rows only on all 5 maps. Shortest map run: 3.9 / 3.6 / 3.0 / 6.6 / 11.1 mm. Shortest crimson run: 7.3 mm. 11,537 commands. The type strokes are glyphs and are not counted. |
| A3 | ERF loops go through the hidden-line; ≥ 1 break on the 14² and 28² loops | **PARTLY FIXED + ARGUED**. The 28² and 14² loops now lie ON their own bicubic surface (+0.25 mm) instead of floating at crest height, and are tested against that map's z-buffer. Hidden stretches under 0.6 mm are treated as grazing noise; each real hidden stretch is widened by 0.8 mm clear on each side. **28²: 1 occlusion break** (2.0 mm hidden, ≈ 3.6 mm gap, on the back arc near x 108, y 166), so the loop is 2 runs. **14²: no break, and none can honestly exist.** The loop was measured on the true surface at relief 4.5 / 6 / 8 / 10 / 12 / 16 mm, with both the engine bias and a tight 0.3 bias: 0 hidden samples every time. The loop's back arc runs ON the big hill ((4..7, 3..5), value 0.93), not behind it. r03 read as "crimson crossing the hill's face" because the loop floated at crest height. Now it climbs the hill's front face and comes down its back, so no crimson crosses a nearer black ridge anywhere. Forcing a break would be a fake occlusion. The 224²/56² loops ride 0.4 mm over a local crest envelope, because on those raster-noise maps "occlusion" would only be single-pixel flicker. |
| A4 | Top plane is one solid surface: 7 rows, no fragment < 4 mm, no flat baseline | **FIXED on count, fragments and baseline; PARTIAL on "each row unbroken"**. All 7 rows are drawn. The CAM is signed about its mean, so there is no clipped flat row. The shortest top-plane fragment is 11.1 mm. There are 11 runs on 7 rows: row 4 splits at the crimson cap, and rows 0–3 break where they pass behind the peak or come within 0.8 mm of a nearer row (pause-resume). |
| A5 | Equal gaps | **holds, re-solved**. One gap G = 13.08 mm is solved by bisection on the row envelopes (up from 10.9, because the summit is lower). |
| A6 | Frame clearance | **holds**. Ink bbox is x 17.75–195.0, y 15.05–281.0. The title's ink top is 6.0 mm under y = 287. |
| A7 | One flush-left type axis | **FIXED (the r03 residue)**. The title and caption start at x = 17.75, which is exactly the front-left end of the input plane's front row (measured on the gcode: 17.75 / 17.75). |
| A8 | PIXELS no flood | **holds**. 38 rows at 1.16 mm. Same-pen parallel ink closer than 0.7 mm: 25.6 mm out of 4.74 m (0.5 %). |
| A9 / A10 | Diagonal; one computation | **hold**. |
| A11 | Title double strokes | **FIXED: single pass**. The weighted two-pass inline type measured 0.30 / 0.35 / 0.39 mm between passes at the acute joins of N / M / A, and cutting the later pass left a dashed stencil (v8, rejected). So the title is drawn in one pass. Closest same-pen parallel in the title: 2.55 mm, with none under 0.8 mm. |
| A12 | Cream preview | **ARGUED (tooling)**. See Engine requests. |
| A13 | Face-on Molnár lattice | dropped on this line (ledger). |
| A14 | The r02 summit mountain: black silhouette base→cap, tallest relief, no black within 1 mm of crimson | **PARTIAL**. The argmax hill's row-4 profile is black from its base up to the lowest ring, and crimson from there to the cap. The CAM plane is the tallest relief on the sheet: 20.0 mm peak-to-peak and 10.5 mm above its mean, against 9.6 / 7.0 / 3.2 / 3.0 mm below it. Black–crimson minimum is **1.01 mm**. **But it is no longer r02's 45 mm mountain, and cannot be under S8.** See the sweep: the runner-up (3,3) sits one row directly behind the peak on a monotone shoulder, and any scale above ≈ 1.08 mm/unit hides it. Science wins, as the SYNTH rules. |
| A15 | Monotone Schotter gradient and resolution channel | **FIXED**. Rows 38 / 28 / 19 / 14 / 7 (strict), flat pitch 1.16 / 1.43 / 1.96 / 2.37 / 4.24 mm (strict), breaks per row 3.45 / 2.89 / 2.16 / 0.86 / 0.57 (strict). No map run is under 3 mm. See the per-plane table. **Spike (r03 x 76–81 / y 143–150, now at x ≈ 76, y ≈ 180, the 28² back-left corner): ARGUED, kept.** It is ‖block_5‖ unit (0,0), the **maximum of the whole 28² map** (normalised 1.00; the 99th percentile is 0.82), a zero-padding corner response. Removing it would erase the map's peak. The torn front-left corner is gone: 28² now has 19 rows at 1.96 mm, not 28 at 1.15. |
| S1 | Top plane whole, one basis, monotone widths | **holds**. Widths 146 / 134.5 / 123 / 111.5 / 100, right-flush at x = 195, nothing cropped. The basis is one basis for all five planes, but **KY changed 0.58 → 0.66 on every plane** (see "What changed"). |
| S2 (+S7) | Caption decodes the stack | **FIXED**. Three flush-left lines under the input plane: `BOTTOM → TOP 224² 56² 28² 14² 7²  HEIGHT = INPUT LUMINANCE / ‖ACTIVATION‖ OF BLOCKS 2, 5, 12 / CAM − MEAN, SIGNED` · `CRIMSON = 50% OF THE GRADIENT MASS OF ∂CAM(4,3) ON EACH MAP (~26% OF IMAGE VS ONE CELL = 2%)  RINGS = CAM LEVELS ABOVE 6.9` · `MOBILENETV2 / IMAGENET  CHELSEA, CENTRE-CROP 300² → 224²  P(TIGER CAT) = 0.43  FRONT EDGE = IMAGE BOTTOM`. There is no colon: the font's colon is two 0.1 mm specks at 1.5 mm cap height, so "=" is used, as the SYNTH allows. |
| S3 | Disclose the top transform | **holds, changed**. The top plane is now CAM − mean, **signed** (not clipped), and the caption says so. |
| S4, S5 | pooling-cascade | dropped (ledger). |
| S6 | No dossier/encoding | **DEFERRED** (process; the translator writes it). |
| S8 | Every CAM cell ≥ 20 % of peak shows its own summit | **FIXED: 13 / 13 on the sheet**. Tested on the placed ink: each crest point has kept black ink within 0.3 mm, including (3,3) = 6.86, (2,3) = 4.26 and (3,1) = 3.72. The argmax is covered by its 5 rings. Interpolation is bicubic (Catmull-Rom interpolates, so every drawn row passes exactly through its 7 unit values). There are no cos² hills and no invented valleys. |

## What changed from parent

- **The head is rebuilt, and its height is measured, not chosen.** The 7×7 CAM is bicubic like
  every other map and signed about its mean. Its height scale is the largest at which all 13
  strong crests survive on the sheet. The sweep re-runs the real top-plane drawing (hidden-line,
  rings, pause-resume, the 4 mm fragment rule) and looks for each crest in the kept ink. The
  bisection passes 1.084. The placed sheet then steps down 1 % at a time until the check passes
  on the final raster, landing at **1.0524 mm per CAM unit** (peak 10.5 mm, against r03's 67.9).
- **Summit rings** are closed level sets of the drawn field about unit (4,3). The lowest is
  **6.908**, the lowest level whose component holds no other unit centre (runner-up (3,3) =
  6.858). The levels are 6.91 / 7.57 / 8.23 / 8.85 / 9.41, each the next level that sits
  ≥ 1.1 mm on paper from the previous ring along the front, left and right rays. They are drawn
  outermost first, visible-only, with pause-resume at 0.8 mm. So what the sheet shows is **5
  front arcs (horseshoes) on the cap; the back arcs are hidden or silenced where the back slope
  foreshortens them together, and they yield 1 mm to the rows behind the peak**. The rings are
  NOT closed on paper. Rows at or in front of the peak row stop inside the lowest ring and 1 mm
  short of crimson.
- **The basis opened, uniformly.** KY went from 0.58 to 0.66 on all five planes. The lower summit
  had freed about 50 mm of height, which r04's first draft spent as 23 mm gaps. The larger depth
  pitch raises the top-plane row pitch from 3.73 to 4.24 mm, and pitch is the only thing the
  visibility bound depends on. It is still one basis (paper = (X + 0.5 D, 0.66 D + Z),
  D = 0.45 W) with the same monotone widths. This departs from the SYNTH's "preserve 0.58".
- **Relief is a declared progression**: 3.0 / 3.2 / 7.0 / 9.6 mm per normalised unit, then the
  CAM at 20.0 mm peak-to-peak. The 28² value is the lowest that gives its ERF loop a real
  occlusion (A3; there is no break at 6 mm). The 14² value is the lowest above 28² that keeps
  breaks per row strictly above the CAM plane's (A15).
- **28² is drawn with 19 rows at 1.5-unit stride** (bicubic between unit rows), so the row count
  falls strictly.
- **Type moved.** The title is single-pass, 5.4 mm cap with 2.1× leading, so "MEANING" ends at
  x 81.8, 8 mm short of the top plane's front row. The caption left the wedge under the title and
  now sits under the input plane: three long lines on the same x = 17.75 axis, with the stack
  lifted 17 mm to make room.
- **Closed-ring RDP bug fixed.** The r03 simplifier collapsed exactly-closed loops to 2 points,
  which dropped 3 of 4 ERF loops in v7.

## Measurements / computations

**CAM visibility sweep** (the real top-plane drawing at origin (0,0); `n/13` = strong crests with
kept ink ≤ 0.3 mm away):

| s mm/unit | 0.6 | 0.8 | 1.0 | 1.05 | 1.1 | 1.2 | 1.4 | 1.9 | 2.5 | 4.0 | 6.79 (r03) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| shown | 13 | 13 | 13 | 12 | 11 | 11 | 10 | 9 | 9 | 9 | 9 |
| missing | – | – | – | (3,1) | (3,1),(3,3) | same | +(2,3) | +(3,2) | … | … | (2,3),(3,1),(3,2),(3,3) |

The pass/fail edge sits between 1.0 and 1.1 and flickers with raster quantisation (the bisection
found 1.084 passing, the table 1.05 failing). That is why the scale is re-verified on the placed
sheet (1.0524 → 13/13).

Alternatives tried, and why they don't raise the bound:
- **Deeper view** (KY 0.58 / 0.66 / 0.74): 1.0 passes and 1.2 fails at every KY. The
  interpolated shoulder between rows 4 and 3 is the occluder, not the row nodes.
- **Shear** (KX 1.0, and KX −0.5 mirrored): both fail at 1.3.
- **Other view directions**, by the node bound (k·pitch − 0.8)/Δz: front = image bottom 1.10,
  top 0.55, left 0.70, right 0.56. Bottom-front, the current view, is the best of the four.

Conclusion for the SYNTH's Do-not: no rows-only scale gives both 13/13 and r02's tall
mountain. I kept the one grammar and a modest mountain rather than switch the head to
plan-view isolines. That call is argued here, not assumed.

**Per-plane Schotter table** (kept ink, v15):

| map | rows | stride | flat pitch mm | relief mm | black runs | breaks/row | median run mm | shortest mm | ink m |
|---|---|---|---|---|---|---|---|---|---|
| input luminance 224² | 38 | 6 px | 1.16 | 3.0 | 169 | 3.45 | 19.8 | 3.9 | 4.74 |
| ‖block_2‖ 56² | 28 | 2 | 1.43 | 3.2 | 109 | 2.89 | 22.0 | 3.6 | 3.39 |
| ‖block_5‖ 28² | 19 | 1.5 | 1.96 | 7.0 | 60 | 2.16 | 23.9 | 3.0 | 1.89 |
| ‖block_12‖ 14² | 14 | 1 | 2.37 | 9.6 | 26 | 0.86 | 44.6 | 6.6 | 1.34 |
| CAM − mean 7² | 7 | 1 | 4.24 | 20.0 p-p (1.0524/unit) | 11 | 0.57 | 36.6 | 11.1 | 0.53 |

**ERF loops** use the same `erf_ellipse` as r03, so centres, radii and mass are unchanged: 50 %
mass held 0.500 / 0.500 / 0.503 / 0.501; area 25.9 / 25.6 / 24.8 / 19.8 % of each map.
Occlusion: 0 / 0 / 1 break (2.0 mm hidden) / 0.

**Crowding** (same pen, |cos| > 0.93, different runs, measured on the gcode):
- ink closer than 0.7 mm: PIXELS 25.6 mm (0.5 %), 56² 0, 28² 0.4 mm, 14² 5.2 mm, CAM 0.
- ink closer than 0.8 mm: 291 / 5.8 / 1.8 / 20 / 0.6 mm.
- crimson: 0 at either threshold (top-plane ring minimum 1.03 mm).
- caption: font-inherent.

**Not re-measured this round:** front-row correlation with the map rows. The row code is r03's;
only the linear height scale changed, and correlation is invariant to that.

## Plot budget

- **11,537 commands** · draw 13.86 m (black 13.12, crimson 0.74) · travel 3.83 m
  (0.28 × draw) · 825 pen lifts · 2 pens, one swap.
- Layer order, one clean layer per pen:
  1. **pen 0 black**: the five maps nearest-neighbour from the origin, then the title, then the
     caption. 815 runs. At Leo's F600 with ~1 s dwells on each lift and landing: ≈ 22 min draw
     + ≈ 27 min dwells + ≈ 2 min travel ≈ **50 min**.
  2. **pen 1 crimson**: 4 ERF loops (the 28² loop in 2 runs) + 5 summit arcs. 10 runs, 0.74 m,
     ≈ **2 min**.
- Every run is a self-contained pen-down stroke, so a layer can be batched at any run boundary.

## Self-critique

| dim | score | why |
|---|---|---|
| Hierarchy | 5 | The heaviest mass is still the bottom raster. The head is now a calm 7-row plane with a small crimson horseshoe cap: a real destination, but a quiet one. At 3 m the 14² plane with its big crimson loop competes with it. |
| Grid & alignment | 8 | One type axis exactly on the input corner (17.75), right-flush planes at 195, one equal gap, 5 mm clearance on every side. |
| Tension & asymmetry | 7 | Same staircase diagonal. "MEANING" now runs toward the top plane's front row (8 mm gap), which reads as a lead-in. |
| Negative space | 7 | Equal 13 mm gaps and the empty wedge under the title, now bigger because the caption moved to the bottom. |
| Craft for pen | 7 | Monotone breaks, no map stub under 3 mm, loops closed or honestly broken, clean single-pass title, travel 0.28×. The 28² loop has a 2–3 mm tooth where it follows the bicubic surface (x ≈ 155, y ≈ 163). |
| Concept legibility | 7 | Noise → calm is now strictly monotone and the caption decodes the stack. The head says "the class evidence is one ridge": argmax plus its shoulder. |
| Depth | 7 | True hidden-line everywhere, including the loops on 28²/14²; 13/13 crests visible. |

**Single worst thing:** the summit is modest. A 10.5 mm hill with a 5-arc crimson cap is honest,
since the runner-up sits one row behind it, but it does not have r02's presence. The sweep shows
that under this grammar and data it cannot, so the next move is compositional, not a parameter.

## Engine requests

1. `Scene3D.field(SX, SY, DEP)`: rasterise a z-buffer without drawing. Rows-only surfaces still
   call the private `scene._rasterize` (repeat).
2. `Scene3D.visible(..., bias=)` / a documented bias. The default 0.02 × depth span (≈ 2 mm here)
   decides whether a loop on its own surface counts as occluded.
3. `scripts/render_candidate.py --paper-color cream` (A12, repeat).
4. `_marching_squares` is pure Python (≈ 1 s per level on 121²). The ring-level sweep is slow
   because of it.
5. The stroke font's `:` and `·` are 0.1 mm specks at caption size. They need a minimum dot size.
