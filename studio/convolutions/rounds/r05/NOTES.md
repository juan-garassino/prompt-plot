# convolutions r05 — iterate · parent: r04 · 2026-09-29

## Render

```
.venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r05/piece.py \
  --fn convolutions_cropfield --seed 7 --paper a4 --orientation landscape \
  --palette crimson,dodgerblue,black \
  --out gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.png
```

- final PNG: `gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.png`
- final GCODE: `gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.gcode`
- seed 7. The piece draws no random numbers. The gcode bodies for seeds 3, 7 and 11 are
  byte-identical: v20 s3 = s7 (md5 `f434f6d5…`), and v17 s11 = s7.
- Provenance: this round directory already held a `piece.py` from an interrupted run of
  this same r05 dispatch. Its renders were v10–v15 and it never wrote NOTES. That run had
  built the 37×25 crop lattice, the capsule-Y X, the gauge collars, the hatched card and
  the key. I re-rendered it unchanged as v16 (= v15) and iterated from there.
- Self-rounds after v16:
  - v17: unread arm reshaped from a 150 mm wedge into a funnel that leaves the image
    through the top-right corner. Card keyline fused into one solid line. Outline passes
    run there and back. Key rings steer the crimson route.
  - v18: shadow hatch flipped to fall to the right. Bridge measures along the ring, not
    the chord. The engine spacing guardrail runs on the rings.
  - v19: the whole wavefront staircase is drawn, and the key and title move onto its
    foot column.
  - v20: each dot is one pen-down (spiral + rim), and each title segment is one pen-down
    (boustrophedon passes). 1057 → 714 black pen-downs.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A12 | Title N diagonals at stem weight | FIXED. Every glyph segment gets its own parallel passes (0.5 mm weight, 3 passes at 0.25 mm), so the N diagonals match the stems. Each segment is now one pen-down. |
| A16 | Kill the heart and the leftover quadrant: X bleeds off TOP and RIGHT, no closed outer contour, no empty region > 80×80 mm, key and title on one left axis | FIXED. The input lattice is 37×25 and ends on the crop's top and right lines. X's unread arm is a funnel (half-angle ≈ 9°) whose rings leave through the top edge (x 165–284) and the right edge (y 150–197). The outline (x = 0 level) is cut at the wavefront and the frame on both flanks, so it never closes. The whorl's eye is a lens of bare paper at about (228–250, 186–193), just inside the top edge; the rings around it are cut by the frame. Largest empty axis-aligned square in the drawable area (0.5 mm raster over all ink): **52.5 mm**, at the bottom-left corner. Key and title share x = 201.2: the title's left ink edge, the X / K / Y icons' left ink edges and the crimson sign icon all sit on it (±0.3 mm). The one exception is the blue sign icon, stepped +2.1 mm so its ring clears the crimson icon one text line above by > 0.8 mm. The title baseline is the bottom sample row, and the key rows are lattice rows 3/5/7/9. |
| A17 | The head is a lifted card: shadow band ≥ 3 mm right+bottom, 45° hatch ≈ 0.9 mm, 3-pass keyline = fattest line, field stops at the band, no hairline double | FIXED. The shadow is a 3.2 mm L-band on the right and bottom only, hatched at 45° with 0.9 mm pitch. The hatch **falls** to the right, because a rising hatch ran parallel to the unread rings leaving the card and read as more field (v17 crop). The keyline is 4 passes at 0.25 mm, which fuse into one 1.05 mm solid line, heavier than the title (0.8 mm) and the X outline (0.6 mm). Field rings stop 0.85 mm outside the band plus keyline. The 1.5 mm hairline double is deleted. Sample dots under the band stay drawn (S2: inputs are never hidden), and the hatch stops 0.9 mm short of each one (0.6 mm paper + nib), so the shadow is a tone lying on the field. |
| A18 | Collars that plot and tell the truth: ≥ 0.6 mm paper, pass pitch ≥ nib (nib in HANDOFF), ink area ∝ \|w\| ±20 % on all 25 taps, sub-ring taps = arc with sweep ∝ \|w\| | FIXED. Nib 0.30 mm (stated in HANDOFF). Collar passes sit at 0.32 mm pitch. The inner pass is laid so its ink edge is 0.60 mm clear of the dot's ink. Ink area = a0·\|w\| with a0 = 19.285 mm² per unit w: full passes first, then one clockwise arc from 12 o'clock carrying the remainder. All 25 taps are within −0.1 % of target in the polyline-length model (table below). Corners come out as 150° gauges, diagonals as 35° gauges (4×), (±2,±1) as 280°, and the centre as 4 full rings. Crimson total = blue total = 40.88 mm² (zero-sum on paper). |
| A19 | Stream crimson → blue → black; swatches last; max consecutive travel < 120 mm | PARTIAL. Layer order is crimson (pen 0) → blue (1) → black (2), streamed in index order. **Measured in-layer max travel: crimson 116.3 mm, black 104.7 mm (was 184), blue 176.9 mm.** The emission order is NOT what reaches the gcode: `postprocess.reorder_by_color` re-sorts every layer greedily by stroke *start* from (0,0). Authored "swatches last" is therefore discarded; the only levers are geometric. I used two: (1) the outline's two passes run in opposite directions, which removed black's 152 mm jump; (2) the start angles of the crimson key rings, which moves crimson's exit from the key to the side facing the card (123 → 116 mm). Blue cannot be steered this way. The greedy tour must start at the stroke nearest the origin, the stem-bottom ring at (95,49). It then walks up the stem and the head into the left arm, and the key is the only blue left, 177 mm away. No start-angle choice changes that. Engine request below. |
| A20 | Honest lineage (unit-grid/Ben-Day or earn Vega; do not displace nodes) | FIXED in HANDOFF. Re-declared as Roy Lichtenstein's *Modern Painting* series (1966–70): a Ben-Day dot lattice, fields of parallel diagonal stripes and one heavy black keyline are its whole vocabulary, and this plate uses exactly those three marks. Canon: Pop / Ben-Day (STYLES §4). No lattice node is displaced. |
| S5 | No dossier.md / encoding.md | DEFERRED (process). SYNTH: this needs a translator pass, not a designer. HANDOFF carries a full `rule:` line. |
| S8 | Key tells the truth and states the finding: (a) finding line, (b) honest zero, (c) dot floor | FIXED. (a) Three lines under the sign icons: `crimson +  where X starts`, `blue −  where X peaks (skeleton)`, `blank  X flat, ∇²X ~ 0`. (b) `no ring: \|y\| < max\|y\| / 8`. Measured over the 66 read windows: 27 are ring-less, 12 of them exactly zero, and the largest ring-less \|y\| is 0.096·max. (c) `no dot: x = 0 · smallest: x < 7%`. 39 of 216 dots sit at the 0.30 mm floor, which is where x/xmax < (0.30/1.13)² = 7.05 %. The number is computed in the piece, not typed. The r04 formula line "rings = round(4\|y\|/max\|y\|)" is shortened to "1-4 rings by \|y\|". |
| S9 | (note) the head hides 3 finished outputs | ARGUED. With the new X, the outputs whose window centre lies under the card are (4,5) bin 0, (5,5) −3 and (4,6) −2. Their centres are 3.6 mm inside the card edge. The widest of their rings (bin 3, r = 4.02 mm) would cross the edge by only 0.4 mm, which is too little to read as "past the card" and would make a hook at the keyline. Their 25 inputs stay visible through the collars. The overlap of k − s = 3 samples is still on the sheet elsewhere: every pair of neighbouring read windows shares 3 rows or columns, and the full staircase (drawn this round) makes the 2-cell treads with 5-cell windows visible. |

## What changed from parent

Composition moves, in order of weight:

1. **The frame becomes the image edge.** The 25×25 lattice floating inside the margins is
   now a 37×25 lattice that ends on the crop's top and right lines. X is no longer a
   bounded trefoil (the "heart"). It is a Y-shaped field whose stem and left arm have been
   read, and whose third arm is still unread and leaves the image through the top-right
   corner. Nothing on the sheet closes into an object.
2. **The unread arm is a funnel, not a wedge.** v16 (the interrupted run's layout)
   filled the whole upper-right quadrant with 18.5 m of black stripes, so the unread
   input outweighed the operation. The funnel opens from the card to the corner (radius
   3.6 → 6.8 → 7.6 cells). The upper-middle stays blank paper, black ink falls to 15.9 m,
   and the rings cross the arm's ridge as sharp chevrons pointing back at the kernel card.
   That ridge is the unread arm's skeleton, which is where the next blue rings would
   appear.
3. **The whole wavefront is drawn.** In r04 the staircase was drawn only where it crossed
   X. Now it runs from the image's top edge (x = 53.6) down to its bottom edge
   (x = 197.6). This produces the plate's second diagonal, descending against the
   ascending funnel, with the card at their meeting. Where X = 0 the staircase is the only
   trace of the 12 windows that read exact zeros. Its last riser is the rule the key and
   the title stand beside: their shared axis is half a cell to its right.
4. **The head is a card.** It has a fused 1.05 mm keyline and a hatched 3.2 mm shadow
   falling against the field's grain.
5. **Collars became gauges.** Ink area ∝ \|w\| on every tap, so the corners visibly
   outweigh the diagonals.

Kept exactly from r04:
- 5×5 LoG with σ = 1, zero-sum.
- Valid convolution, stride 2.
- Swept set i + j ≤ 10: the same 66 windows. With the wider lattice the output grid is
  17×11, and the 66 read windows are the same index set.
- Rings = rint(4\|y\|/max\|y\|), centred on the node's own input sample, pitch 1.02 mm
  everywhere including the key.
- X rings at 1.05 mm, and dot area = x.

## Measurements / computations

- **K:** 5×5 LoG, σ = 1 cell. Centre −0.9813, max +0.1540, Σ = −1.7e−16.
- **X:**
  - Exact Euclidean distance to the capsule-union outline, computed tiled with segment
    pruning. The tiled version was verified identical to brute force (max diff 1e−14).
  - Dot area = cell mean of d (6×6 quadrature). pmax over drawn cells is 37.26 mm; the
    unread whorl reaches 49.8 mm and is carried by rings.
- **Y:**
  - Valid convolution, stride 2, 17×11. max\|y\| over the read nodes = 18.731, which is
    also the global max.
  - Read-node bins: −4:2, −3:4, −2:4, −1:7, 0:27, +1:21, +2:1. 37 drawn response sets
    plus 2 non-zero bins under the card.
  - The head node (5,6) has y = −17.27 (bin −4): the fork, and the next node on the
    anti-diagonal.
- **X continuity across the front:**
  - Cell-mean d (dot area) vs ring index floor(d_centre/1.05) over all 457 interior cells:
    Spearman 0.997.
  - The 17 front pairs (read dot | unread neighbour's ring level): Spearman 0.956.
- **Spacing (rings after the engine guardrail, 0.25 mm samples):**
  - Min 0.801, p1 1.044, median 1.050 mm, 0.00 % under 0.8.
  - Before the guardrail, 0.42 % were under 0.8. These were chevron tips on the ridge,
    plus one 8 mm sliver at the neck that the old chord-based bridge had closed with a
    tick.
  - Rings 102 strokes, 10.5 m. Outline 2 passes × 3 pieces, 0.52 m. Staircase 0.26 m.
  - Ring ends sit 0.85 mm off the staircase, and the dots are ≥ 2.4 mm from it (3.6 − 1.13).
- **Collar table** (a0 = 19.285 mm²/unit; area in mm²; the arc is the partial pass):

  | tap (a,b) | w | target | drawn | full passes | arc |
  |---|---|---|---|---|---|
  | corners (0,0) (0,4) (4,0) (4,4) | +0.0736 | 1.420 | 1.419 | 0 | 147–153° |
  | edge (0,1) (0,3) (1,0) (1,4) (3,0) (3,4) (4,1) (4,3) | +0.1418 | 2.735 | 2.733 | 0 | 268–290° |
  | edge-mid (0,2) (2,0) (2,4) (4,2) | +0.1540 | 2.970 | 2.968 | 0 | 287–315° |
  | diagonal (1,1) (1,3) (3,1) (3,3) | +0.0187 | 0.360 | 0.360 | 0 | 35° |
  | ortho (1,2) (2,1) (2,3) (3,2) | −0.2846 | 5.488 | 5.485 | 1 | 138–157° |
  | centre (2,2) | −0.9813 | 18.925 | 18.917 | 4 | — |

  The arc angles for equal w differ by a few degrees because each hole is sized to its
  own dot.
- **Empty space:** the largest empty square is 52.5 mm (at x 10–62, y 10–62). r04 left a
  145×120 mm quadrant.
- **Bounds:** every ink edge ≥ 10 mm inside the drawable area, except the deliberate bleed
  of the unread rings and the staircase's top riser on the crop line (3 mm inside the
  drawable edge).
  - Ink bbox: black x 20.9–284.0, y 20.4–197.0; crimson x 33.6–209.2; blue x 33.6–207.3.

## Plot budget

| | |
|---|---|
| draw | 17.13 m (crimson 0.50, blue 0.71, black 15.93) |
| travel | 5.49 m (32 % of draw; r04 was 51 %) |
| commands | 74,381 |
| pen-downs | crimson 47 · blue 46 · black 714 (807 total; r04 823 with half the ink) |
| max in-layer travel | crimson 116.3 · blue 176.9 · black 104.7 mm |
| pens | 3, streamed crimson → dodgerblue → black (2 swaps) |
| est. time (Leo: F600 draw, ~F2000 travel, 1 s dwell per lift and drop) | crimson 2.9 min · blue 3.0 min · black 52.2 min (the funnel's rings are ≈ 17.5 of those minutes) · total ≈ 58 min |

## Self-critique (rubric)

| dimension | score | notes |
|---|---|---|
| Hierarchy | 7 | The card is the focal point: heaviest line, the only colour cluster, sitting where the two diagonals meet. The funnel is the biggest mass and still carries more ink than anything else, so the unread input remains loud. It is second in reading order, not first. |
| Grid & alignment | 8 | One lattice with the crop on its top and right lines. Staircase treads = stride. Key/title axis half a cell off the staircase's foot. Title baseline on the bottom sample row, and key rows on lattice rows. The blue sign icon's 2.1 mm step is the one off-axis mark. |
| Tension | 8 | Two opposed diagonals: the staircase descending top-left → bottom-right, and the funnel ascending card → top-right corner. The card sits at the crossing, and both diagonals bleed off the frame. |
| Negative space | 7 | The upper-middle band (between the left arm and the funnel) and the lower-right (beyond the staircase, holding only the key) are shaped by the two diagonals. The biggest empty square is 52 mm. The bottom-left corner is the least designed quiet. |
| Craft for pen | 7 | Every ring gap ≥ 0.80 mm, no crumbs < 3 mm, no hooks, collars 0.6 mm clear of their dots. Blue's 177 mm travel is unsolved (see A19). The black layer is 52 minutes. |
| Concept legibility | 7 | A card reads the field down a staircase: behind it a dotted wake whose blue rings trace the read arms' skeletons, ahead of it the unread arm running out of the frame. The key names the finding. |
| Depth | 7 | Declared flat apart from one plane. The card's fused keyline, hatched shadow and the rings stopping at the band read as a lifted card. The falling hatch separates the shadow from the field. |

**Single worst thing:** the funnel. It is a tapered band with a crease of chevrons down
its middle. At thumbnail size that can be named: "a feather" or "a wing". It is also still
the heaviest ink on the sheet, heavier than the operation it is waiting for.

## Engine requests

- `postprocess.reorder_by_color` / `optimize_stroke_order`: the per-layer greedy
  nearest-start tour from (0,0) discards the authored order and strands the last cluster
  (blue here: 177 mm). Two options would let a piece meet a max-travel budget:
  - honour an authored order (e.g. a `metadata.keep_order` flag);
  - add a 2-opt / or-opt pass and let open strokes be reversed.
- `geometry.clip` with a `min_gap` that measures the removed part ALONG the polyline. The
  local `_bridge` now does this. The chord version fused the two arms of a chevron whose
  tip dipped under the cut.
- A rectilinear-mask → polygon tracer (`_mask_ring`, `_grow_rectilinear`), still local.
