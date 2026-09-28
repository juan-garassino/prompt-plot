# convolutions r03 — sliding-window (abstract) · parent: r01 · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r03/piece.py \
  --fn convolutions_sliding_window --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson,dodgerblue \
  --out ~/Downloads/pp_convolutions_sliding-window_v10.png
```

- final PNG: `~/Downloads/pp_convolutions_sliding-window_v10.png`
- final GCODE: `~/Downloads/pp_convolutions_sliding-window_v10.gcode`
- seed 7. Seeds 3 and 11 were also rendered (`_v8_s3`, `_v8_s11`). The seed only moves the
  ±0.12-pitch fbm wobble in the thumbprint rings, and the three renders look the same at
  sheet scale. Every number on the plate is deterministic and does not depend on the seed.
- self-rounds: v1 → v10 (v9 and v10 have identical geometry; v10 only has lint fixes)

## Mandate responses

There is no `LEDGER.md` or `FEEDBACK.md` for this slug, so there are no open J*/A*/S*
mandates. The table below answers the **Weak** list in `DESCRIPTION.md` instead, since that
is the current work order for this thesis.

| id | mandate (DESCRIPTION § Weak) | status |
|---|---|---|
| W1 | [concept] pipeline schematic, operator labels, captioned insets | FIXED. No operator labels, no captions and no inset panels. The only type is the title. The plate is one order: a lattice with a travelling window. |
| W2 | [concept] nothing computed; the mechanism is never shown as a process | FIXED. X is sampled into real cell averages and K is a real 5×5 zero-sum LoG. Every stamp's rings and every node of Y is `sum(K * patch)`, stride 2. The window is shown mid-sweep: finished stamps, the kernel on the current stamp, and dotted future stops. |
| W3 | [tension] bilateral symmetry about u = 0.5 | FIXED. One working diagonal runs from the left frame edge (it crops there) down to the bottom-right corner of the lattice. The masses are asymmetric: X at the left and full height, Y top-right, the title bottom-right, and the lower-right quadrant left empty. |
| W4 | [concept] ~30 decorative dots, brackets, plus marks, hollow square | FIXED. All deleted. Every mark on the sheet carries a number (see Measurements). |
| W5 | [craft] muddy starburst tiles; crossed-dash scribble inside blob X | FIXED (by removal). There are no tiles and no rays. The kernel is 25 signed Ben-Day discs. |
| W6 | [craft] accidental `>` pointer at the `K` | FIXED (removed). There are no arrows. Dotted projection tracks only. |
| W7 | [space] stride/padding block jammed into a corner; spine through blob Y | FIXED (removed). Stride is drawn as a spacing, not written as a word. There are no spines. |
| W8 | [hierarchy] hairline caption type everywhere; no dominant element | FIXED. The thumbprint X is the dominant mass. The kernel head is the loudest colour. The title is `giant_type` with 0.8 mm weight, set exactly to the output map's width. |
| W9 | [depth] undeclared flatness | ARGUED. Flat by decision (Swiss/constructivist lattice). The only depth is layering by knock-out: the corridor cuts the rings, and the kernel sits over the pixels it reads. Rings stop 0.85 mm short of every corridor edge. |

## What changed from parent

This is a new composition. It is not a respacing of r01.

- **Deleted:** the five-tile strip, both connector fans, the dashed ellipses, both spines, the
  kernel bank, the receptive-field cone, the feature maps, the title block, the
  stride/padding block and all furniture.
- **X (left 60 %)** is one large field. It is a trefoil distance-field thumbprint on a
  162.5 × 182 mm lattice of 6.5 mm cells, and it is the dominant mass. The lobes are
  rotated (φ₃ = −π/2) so the medial axis is an upright **Y**.
- **The sweep:** a staircase corridor cut diagonally through the thumbprint, entering at the
  left frame edge. Inside the corridor the continuous rings are replaced by what they became:
  lattice samples, where dot area is the pixel value. Each finished stamp leaves nested rings
  at its centre. The count is proportional to |y| and the pen gives the sign. Silent stamps
  leave a hollow 0.9 mm ring ("looked, saw nothing").
- **The head:** the kernel itself, drawn as a heavy square holding 25 signed discs, sitting on
  stamp 7 of 11. Past it, a dotted track with hollow markers shows the stops still to come.
- **Y (top-right)** is the complete output map in the same count/sign grammar. It rhymes with
  the sweep: a thin staircase over the nodes already produced, a heavy square on the node the
  head is writing now, and a dotted diagonal through the nodes still to come.
- **The twist:** a symmetric zero-sum kernel is blind to every linear ramp, and a distance
  field is a ramp almost everywhere. So the map the window returns is the trefoil's
  **skeleton**, which reads as a blue letter **Y** inside a crimson outline. X convolved is Y.
- Kept from r01: the distance-field ring construction (|∇d| = 1), `_iso_chains`, `_dash`,
  `_guard_spacing`, the 13 mm frame, and the stroke-font helpers.

## Measurements / computations

**Kernel.** 5×5 LoG, σ = 1 cell. The centre weight is −0.981, the max is +0.154 and the sum
is −1.7e−16. Linear-ramp test: `sum(K*(a+bI+cJ))` for three random ramps gives −2.8e−16,
1.6e−15 and −2.7e−15, which is exactly zero.

**Input.** The pixel value is the cell average of d over a 6×6 midpoint quadrature per 6.5 mm
cell. The pixel max is 31.2 mm.

**Output.** Valid convolution at stride 2 gives an 11 × 12 output. max|y| = 15.47.
Ring count = rint(4·|y|/max).

| count | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 |
|---|---|---|---|---|---|---|---|---|
| nodes | 5 | 9 | 6 | 12 | 59 | 28 | 12 | 1 |

45 % of the output nodes are silent.

**Where the negative response sits.** 16 of the 20 nodes with count ≤ −2 lie within one cell
(6.5 mm) of the medial ridge. The median distance is 2.6 mm, measured to the ridge mask
(|∇d| < 0.9, d > 1 mm). The other 4 are −2 flank nodes of the arms. The 5-cell footprint
smears the ridge by about one cell.

**Where the positive response sits.** The 13 nodes with count ≥ +2 have a median distance of
2.0 mm to the outline.

**Sweep path.** Output nodes (0,10) → (10,0), down-right. In order:

| t | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 (head) | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| y | 0.83 | −5.12 | −7.28 | −1.22 | +6.31 | −10.21 | −0.84 | +6.46 | 0.11 | 0 | 0 |
| rings | 0 | −1 | −2 | 0 | +2 | −3 | 0 | +2 | 0 | 0 | 0 |

- The finished stamps 0–6 are drawn in X, and the same seven nodes carry the staircase in Y.
  They were checked to be identical values.
- Stamps overlap by k − s = 3 cells, so the stair tread is 2 cells = 13 mm and the corridor
  width is 5 cells = 32.5 mm.
- Dilation is 1: taps sit on adjacent cells.

**Spacing.** Measured on the final gcode by sampling at 0.3 mm and taking the nearest point on
a different stroke:

| family | min | p1 | median | share < 0.8 mm |
|---|---|---|---|---|
| thumbprint ring↔ring (116 strokes) | 0.69 | 0.98 | 1.00 | < 0.005 % (isolated points at medial-axis corners after the house `enforce_line_spacing` guard) |
| thumbprint ring↔outline | 0.91 | 0.93 | — | 0 |
| Y-map rings, crimson / blue | 0.89 / 0.80 | 0.89 / 0.88 | 0.90 | 0 |
| stamp rings | 1.89 | — | — | 0 |

- The Y centre mark (r 0.25) is 0.90 mm from the first ring.
- The Y outermost ring (3.85) leaves 0.80 mm to the next node.
- The second outline pass is offset 0.28 mm OUTWARD along the normal. It is one heavy line,
  and it keeps ring 1 at full pitch.

## Plot budget

| | |
|---|---|
| draw | 14.18 m (black 12.01, crimson 0.86, blue 1.30) |
| travel | 6.99 m |
| commands | 48,505 |
| pen-down cycles | 750 |
| pens | 3 (2 swaps) |
| bounds | ink x 13.0 … 284.2, y 13.0 … 194.8. The only (0,0) is the pipeline's park move. |
| est. time | 9.6 min at the preview feeds; about 25–30 min at Leo's F600 |

## Self-critique (rubric)

| dimension | score | notes |
|---|---|---|
| Hierarchy | 7 | The thumbprint dominates at 3 m. The kernel head is the loudest focal point. Y is second and the title third. The corridor's black pixel discs compete a little with the coloured stamp rings. |
| Grid & alignment | 8 | The lattice starts at the left frame edge. Y is flush to the top/right frame. The title is exactly Y's width and flush to its left edge and the frame bottom. X's track and Y's track end on their lattice corners. |
| Tension | 8 | One working diagonal, cropped at the left frame. The composition is asymmetric. |
| Negative space | 7 | The lower-right quadrant is shaped quiet paper, and the dotted track runs into it. The strip between X's right lobe and Y (about 20 mm) is a bit tight. |
| Craft for pen | 8 | Spacing is ≥ 0.8 mm everywhere apart from isolated medial-axis points. Tone is carried by dot area on a fixed 6.5 mm lattice. Rings stop 0.85 mm short of the corridor. |
| Concept legibility | 7 | The sliding window reads as a process: done, now, to come. The Y-from-X punchline lands at thumbnail scale. Still, the output map is a regular grid of targets and sits close to "a chart". |
| Depth | 6 | Declared flat. The only layering is knock-out. |

**Single worst thing:** the output map Y is a full 11×12 lattice of small targets, and its
crimson +1 speckle (28 nodes) makes it read as a data grid. The blue Y reads, but it does
not jump. A future round could put X and Y on one shared lattice, or draw Y as the corridor's
own continuation, so it stops looking like a separate panel.

## Engine requests (optional)

- `kit` has no normal-offset for a closed ring. I wrote `_offset_out` locally for the outward
  second outline pass. `forms`/`geometry` have `offset` for regions, but nothing
  lightweight for a polyline ring.
