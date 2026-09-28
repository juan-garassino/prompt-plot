# Encoder-block weights (QUERY · KEY · VALUE · FFN 1 · FFN 2) / PARAMETER FIELD — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/transformer/weights` |
| current render | `gallery/neural-networks/transformer/weights/promoted/pp_weights_block.png` |
| source | current: `promptplot/generative/generators.py::weight_matrix` (`tensor="block"`) — **not** `bauhaus_weights`, whose name the batch lists · trials: `promptplot/generative/pieces/ml.py::bauhaus_weights` (PARAMETER FIELD) |
| paper · pens | a4 landscape, white preview · current: 0 navy = positive weights ("/") · 1 crimson = negative weights ("\\") · 2 gray = panel labels + head separators · trials: 0 dodgerblue = positive discs · 1 deeppink = negative discs · 2 black = dividers, type, swatch |
| status | promoted tier on disk, **no recorded feedback** · `CURATION.md`: `bauhaus_weights` **REWORK** ("three EQUAL panels = the exact 'no hierarchy' fail; even dot field, flat, borderline schematic (Hinton grid)"); `weight_matrix` on the "Watch … decorative data texture, not gallery compositions" list · 3 renders on disk |

## In one line
A transformer encoder block's five weight matrices drawn as a **lattice** of tick fields
(a plotter Hinton diagram) — every weight a diagonal tick, length ∝ |w|, "/" navy for
positive, "\\" crimson for negative; the earlier PARAMETER FIELD trials drew only Q|K|V as
a lattice of spiral discs, radius ∝ |w|, blue/pink by sign.

## What is on the sheet

### current — `pp_weights_block.png`
- **Five rectangular tick fields tiling the entire drawable area** with ≈ 6 mm gutters and
  no frames — the panels themselves touch the margin on all four sides:
  - top row (v 0.10–0.42), three equal panels: `QUERY` (u 0.05–0.34), `KEY`
    (u 0.36–0.64), `VALUE` (u 0.67–0.95);
  - bottom row (v 0.48–0.93): `FFN 1` wide (u 0.05–0.64) and `FFN 2` narrower
    (u 0.66–0.95).
- **Texture:** each cell holds one short 45° tick; ticks below 0.12 mm are skipped, so the
  fields read as a speckle of navy and crimson flecks with irregular white gaps. In QUERY /
  KEY / VALUE five gray vertical hairlines split each panel into six head columns; some
  columns are visibly denser than others (e.g. QUERY's second and fourth columns).
  FFN 1 (wider than tall in cells) reads as a fine, faintly diagonal-banded tweed; FFN 2
  (many more rows than columns in the same height) packs ticks into tiny vertical stacks — the finest, most speckled field.
- **Type:** gray hairline stroke labels ≈ 3.6 mm, centred above each panel: `QUERY`,
  `KEY`, `VALUE` (v 0.07), `FFN 1`, `FFN 2` (v 0.46). No title, no footer.
- **Quiet zone:** none — only the 6 mm gutters.

### trials — `pp_bauhaus_weights_seed1_v1.png` → `_v2.png` (PARAMETER FIELD)
- Three equal square-ish panels of small spiral-filled discs on a strict grid, centred
  on the sheet (u 0.10–0.91, v 0.12–0.62 in v1; v 0.12–0.66 in v2), separated by two black
  vertical rules at u 0.33 and u 0.64. Blue discs = positive, pink = negative, radius by
  magnitude; v1 packs ≈ 16 × 26 cells per panel, v2 ≈ 14 × 22 with larger discs, bolder.
- Letters `Q`, `K`, `V` under each panel (v 0.69 / 0.71). `PARAMETER` / `FIELD` spaced
  caps with a short underline bottom-left (u 0.06, v 0.82–0.86). `M 1 80` bottom-right
  (u 0.85, v 0.91), a `+` mark at (0.90, 0.84), a tiny black/blue/pink swatch stack at
  top-right (0.93, 0.08). The lower third of the sheet is empty except the type.

## The science it encodes
`weight_matrix` docstring: "Trained weight matrices as tick-field panels (a plotter Hinton
diagram). Every weight is a diagonal tick: length ∝ |w| (99th-percentile normalized),
direction / for positive and \\ for negative … `block` = the whole encoder block on one
page … Fallback without a checkpoint: seeded gaussians" (actually seeded *uniform* ±1 in
the code). With a `.keras` checkpoint the Q/K/V dense kernels (reshaped heads × dim) and
the two FFN kernels are read via h5py; the gray separators mark the 6 heads. Whether this
render used a checkpoint is not recorded; the uneven head-column densities in QUERY hint
at trained weights, but no block, diagonal or low-rank structure is visible — at this
scale trained and random fields look nearly the same.
`bauhaus_weights` docstring: "A true Hinton diagram in the Bauhaus language: Q | K | V
panels on a strict grid, every weight a solid circle — radius by magnitude, blue positive,
pink negative. Trained weights when a checkpoint is given." `M 1 80` is its model tag.

## How it got here
`bauhaus_weights` v1 → v2 (both in `prior-approved/`): fewer, larger discs; otherwise the
same three-equal-panel layout. CURATION then judged it REWORK for no hierarchy. The
promoted render swaps to the `weight_matrix` generator: gains the whole block (FFN
included), the head separators and sign-by-direction; loses the Bauhaus type, the discs'
graphic weight, and every quiet zone. No feedback in `studio/feedback.jsonl`.

## Keep — what works
- Sign by tick direction ("/" vs "\\") is readable even with one pen; with two pens sign is
  doubly encoded. A clean, exact mapping.
- The block layout's proportion is data: FFN 1 is wider because it has more columns — the
  panel areas are the true matrix shapes (the only honest hierarchy on the sheet).
- Head separators: the six head columns are a real structure of the Q/K/V matrices and
  the only thing that breaks the texture into readable units.
- From the trials: discs whose area carries |w| have real graphic mass; blue/pink as a
  scarce-vs-common pair; the PARAMETER FIELD type block anchored bottom-left.

## Weak — what doesn't
- [concept] A Hinton diagram is a textbook figure (§ 6 NO SCHEMATICS); five labelled panels
  make it a slide of "the parameters of a transformer block".
- [hierarchy] Current: five fields of identical texture; no dominant element. Trials: three
  equal panels — CURATION's exact complaint.
- [space] Current: the fields fill the drawable area edge to edge; 6 mm gutters are the only
  white. Nothing is quiet, so nothing is loud.
- [tension] Both versions are dead-square grids, centred or full-bleed, no diagonal,
  nothing cropped.
- [craft] Current: 186 k commands, 53 m of travel for 19.5 m of ink — every tick is its own
  pen cycle; FFN 2's ticks are sub-millimetre dots the pen will blob; unplottable in
  practice.
- [craft] Gray hairline labels at 3.6 mm — lab-figure type.
- [concept] No structure of a trained matrix is visible (no low-rank banding, no outlier
  channels); the plate cannot be told apart from noise.
- [depth] Flat, undeclared, in both versions.

## Next versions
1. **one matrix, sorted** (faithful) — draw only W_Q of one real layer, huge (≈ 0.9 W), with
   rows and columns permuted by their leading singular vectors so trained structure shows
   as bands and blocks; ticks become fixed-length dashes whose duty carries |w| (tone drives
   duty), K and V appear as two small inset panels cropped at the frame. One dominant
   field, visible structure, plottable density.
2. **the outlier channels** (mechanism) — trained transformers have a handful of residual
   dimensions with huge weights across every matrix. Draw all five matrices as faint
   texture and let those few channels run through the whole block as loud crimson
   continuous bars — a **lattice with defects**. The defects are the phenomenon; the
   texture is the ground.
3. **spectrum** (abstract) — replace the pixels with the singular values: each matrix as a
   **nested** set of concentric rings whose radii are its singular values, the five
   matrices as five ring-sets of different sizes overlapping on one axis. It shows the
   effective rank (how quickly the rings collapse), which is the property that matters,
   and it gives the plate a single radial form instead of a grid.

**If only iterating:**
1. Render with `tensor="qkv"` or a single `ffn1` panel at full sheet and leave ≥ 30 % of the
   sheet as a quiet band for a large-scale title, instead of five panels full-bleed.
2. Raise `min_tick` to 0.6 mm and merge consecutive same-sign ticks along a row into one
   stroke, targeting < 20 k commands and travel < draw.
3. Permute rows/columns by mean weight (as `bauhaus_loom` does) so same-sign regions cluster
   visibly; if nothing clusters, the checkpoint is not being loaded — confirm the render
   uses trained weights before any other change.
