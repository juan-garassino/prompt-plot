# convolutions r04 — iterate · parent: r03 · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/convolutions/rounds/r04/piece.py \
  --fn convolutions_wavefront --seed 7 --paper a4 --orientation landscape \
  --palette black,crimson,dodgerblue \
  --out ~/Downloads/pp_convolutions_iterate_v9.png
```

- final PNG: `~/Downloads/pp_convolutions_iterate_v9.png`
- final GCODE: `~/Downloads/pp_convolutions_iterate_v9.gcode`
- seed 7. The piece uses no randomness: r03's ±0.12-pitch fbm wobble is gone because it
  was what pushed the 45° stretches under pitch. Seeds 3, 7 and 11 give byte-identical
  gcode (md5 `7feda169…` for v9 s7 and s3; v5 s3/s7/s11 also matched each other).
- self-rounds v1 → v9:
  - v1: first single-field layout.
  - v2: floor dots pruned to needed inputs, collars.
  - v3: x = 0 drawn as paper, title set on the ink box, key in fixed-advance type.
  - v4: frontier keyline.
  - v5: key wording, seed check.
  - v6: grazing-clip bridge, which removed the 0.13 mm near-touch at a stair corner.
  - v7 (`_t11` variant): T = 11 with the head on the right-arm root. Rejected because
    it leaves triangular ring slivers and shrinks the ring mass to one lobe.
  - v8: every ink edge ≥ 10 mm inside the drawable area.
  - v9: lint only, same geometry as v8.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | Collapse the triptych: every response on the X lattice, no separate output panel, no staircase copy, no leader lines | FIXED. The 11×12 map, its thin staircase and bold box, the corridor and both leashes are deleted. Y = K∗X is an 11×11 valid stride-2 output drawn only as rings centred on the X node where its window was centred. Nothing stands apart from the field except the title and the key. |
| S2 | Inputs never hidden; rings wrap the centre sample and stop ≥ 0.8 mm short of the neighbours | FIXED. Measured on the gcode: 32 drawn responses, 0 inputs with x > 0 missing from their windows. Dot → nearest coloured mark is ≥ 0.825 mm outside the head. Analytically, first ring R1 = 1.98 against a max dot of 1.13 gives 0.85, and the outer ring 5.04 against a neighbour dot 7.2 mm away gives ≥ 0.854. The centre tap sample is drawn inside every ring set. **Declared:** the head plane lies on 3 finished outputs, (4,5) +2, (5,5) −2 and (4,6) −1, and hides their rings (depth by occlusion). Their 25 inputs stay visible through the collars. **Declared:** x = 0 samples are paper, because dot area = x and the key says "no dot: x = 0". |
| A10 | Close the medial seams; pitch ≥ 1.0 mm everywhere; clean cut at the frontier | FIXED. No wobble: the pitch is exactly the level step 1.05 because \|∇d\| = 1. Ring↔ring over all 47 ring strokes, sampled at 0.25 mm: min 1.041, p1 1.044, median 1.050, 0 % under 0.8. Closed level loops thinner than 2 mm (2·area/perimeter) are dropped, so the upper-lobe hairpin slit is now one clean lens eye. The lower-lobe zipper is gone: that lobe is on the swept side now, and the house `enforce_line_spacing` guard that chopped the chevron tips is no longer used. Rings stop on one line 0.85 mm outside the staircase keyline. Grazing clips (< 1.2 mm cut) are re-joined, so there are no hooks. |
| S1 | Put the encoding on the sheet | FIXED. One key strip top-right, with real marks as icons: `X  dot area = x / no dot: x = 0` · `K  5×5 LoG, stride 2 / collar area = \|w\|` · `Y = K ∗ X / rings = round(4\|y\| / max\|y\|)` · `crimson +  blue − / no ring: y = 0`. There is one code for y = 0 (no ring), and the 1.8 mm hollow "saw nothing" ring is gone. |
| A9 | The head is a plane: second keyline 1.5 mm off its right and bottom edges, rings stop at it; delete leashes and meaningless hollow circles | FIXED. The head is a heavy double keyline plus an L-shaped shadow keyline 1.5 mm off its right and bottom edges. Field rings stop 0.85 mm outside that shadow. Leashes: 0. The only hollow circles left are response rings around x = 0 samples (5 crimson ones at the rim), and the key explains them. |
| A11 | HANDOFF `lineage:` line and declared canon | FIXED. Vasarely, *Vega*; canon Op Art / Ben-Day, declared flat apart from one plane. |
| S3 | (argued) The thumbprint rings carry X | CHECKED. Ring index floor(d/pitch) at each cell centre vs the dot-area value (cell mean of d), over all 272 interior cells: Spearman **0.998**. On the 18 frontier-row cells, the rings on one side of the cut and the dots on the other: Spearman **0.986**, mean \|P − d_centre\| = 0.14 mm. |
| A12 | Title multi-pass strokes separate; `I` spacing | FIXED, pulled forward from r05 because it was cheap. The title is set glyph by glyph on its ink box (shift by its own left ink edge, advance = ink width + one bearing), so the serifed `I` is centred. Weight 0.8 mm is drawn in 4 passes at 0.25 mm instead of 3 at 0.4. |
| A13 | Travel share | DEFERRED, re-measured. Travel 5.60 m against 11.07 m draw (51 %), from 394 sample dots plus 119 ring sets. Structural: the dots are the input. The pipeline already orders strokes within each colour. |
| S5 | No dossier/encoding for this slug | DEFERRED (process; outside a designer round). |

## What changed from parent

- **Three stations → one field.** r03 was input grid → kernel box → output grid. r04 is a
  single lattice with a wavefront crossing it.
- **The wavefront.** Output nodes with i + j ≤ 10 (j counted from the bottom) are "swept".
  The union of their windows is the read region, bounded by a staircase keyline (tread =
  stride = 2 cells). The frontier runs from the top edge down-right to the right edge, the
  working diagonal. Behind it, X appears as its samples (dot area = x). Ahead of it, X is
  still continuous distance-field rings.
- **Y inside X.** Every swept node with a non-zero bin carries its real y as rings centred on
  its own input sample. The zero-sum LoG only sees curvature, so behind the frontier the blue
  skeleton grows inside the thumbprint: the stem (four −4 nodes) and the left arm, with
  crimson rings on the rim.
- **The head sits on the fork.** Node (5,6) has y = −14.2 (bin −3), is the Y's junction and
  is the first node of the next anti-diagonal. It is a plane with a drop shadow. Each of its
  25 taps is a Ben-Day collar around the sample it multiplies, so the blue centre collar
  continues the blue skeleton across the plane. The right arm is still ahead of the
  wavefront, in rings.
- **Freed right third.** It is quiet paper, with the key top-aligned to X's highest sample row
  and the display title's baseline on X's lowest sample row.
- **X enlarged** from 6.5 mm to 7.2 mm cells (25 × 25 = 180 mm) so the 4-ring response
  fits between samples.

## Measurements / computations

- **K:** 5×5 LoG, σ = 1 cell. Centre −0.9813, max +0.1540, Σ = −1.7e−16.
- **X:**
  - P = cell average of d, using a 6×6 midpoint quadrature per 7.2 mm cell. Max 31.97 mm.
  - 272 interior cells.
- **Y:**
  - Valid convolution, stride 2, 11×11. max\|y\| = 17.90. Bin = rint(4\|y\|/max).
  - All nodes: −4:5, −3:5, −2:10, −1:6, 0:58, +1:27, +2:9, +3:1.
  - Swept (66 nodes): −4:4, −3:2, −2:4, −1:3, 0:34, +1:14, +2:5. 32 are drawn, 3 of them
    under the head.
- **Head overlap:** 21 of the head's 25 cells were already read by past windows
  (k − s = 3 overlap in both axes). This is the reason the head must show its inputs rather
  than cover them.
- **Collars:**
  - Area = a0·\|w\| with a0 = 24.62 mm² per unit w. Crimson total 52.19 mm², blue total
    52.19 mm² (zero-sum on paper).
  - Hole = sample radius + 0.45 mm.
  - Collars thinner than 0.28 mm are a single circle: the ±1 diagonals and corners. Their
    true area (0.8–1.8 mm²) is below what a nib can ink, which is the plotting floor.
- **Checkable from the sheet:** K∗X was recomputed from dot areas measured off the gcode
  (r → x = (r/1.13)²·max) for the 32 drawn nodes. Spearman 0.988, Pearson 0.995, sign agrees
  32/32.
- **Spacing (final gcode):**

  | pair | min | notes |
  |---|---|---|
  | thumbprint ring↔ring | 1.041 | p1 1.044 |
  | ring end → staircase/head keyline | 0.850 | |
  | outline 2nd pass | 0.28 outward | one heavy line, by design |
  | sample dot → foreign colour mark | 0.825 | |
  | response ring ↔ ring | 1.02 | |
  | collar hole | 0.45 | |

## Plot budget

| | |
|---|---|
| draw | 11.07 m (black 9.29, crimson 0.80, blue 0.99) |
| travel | 5.60 m (51 %) |
| commands | 48,372 |
| pen-down cycles | 823 |
| pens | 3 (2 swaps) |
| ink bbox | x 23.5–277.4, y 25.4–187.0, ≥ 10 mm inside the drawable area on every side |
| est. time | 7.6 min at preview feeds; about 50 min at Leo's F600 draw with 1 s dwells (823 lifts ≈ 27 min of it) |

## Self-critique (rubric)

| dimension | score | notes |
|---|---|---|
| Hierarchy | 7 | One mass (the trefoil) dominates. The head is the colour focal point, the title is third and the key is tiny. The ring half is visibly heavier than the dot half, which reads as "unread = dense, read = sampled". That is intended, but it pulls weight to the upper-right. |
| Grid & alignment | 8 | One lattice. The frontier treads are the stride. The key's first row sits on X's top sample row and the title baseline on its bottom sample row. The right column keeps a 10 mm ink margin. |
| Tension | 7 | The staircase diagonal cuts the mass and the head sits on the fork. The frontier enters at the lattice's top edge (x ≈ 49), not literally the left frame edge: with windows 5 cells wide, a frontier through the fork cannot start on the left edge. T = 8 does, but then the Y is barely swept. |
| Negative space | 7 | The right third and lower-right are quiet. The swept half's rim now reads as the trefoil (x = 0 is paper). There is a small ring tab above the frontier's first step (x 48–63, y 180–185). |
| Craft for pen | 8 | Pitch is exact, there are no seams and no hooks, and every gap is ≥ 0.8 mm. Travel is still 51 %. |
| Concept legibility | 7 | "A thumbprint being read into a letter Y": the blue stem and arm grow behind the wavefront and the head sits on the fork. Without the key, the collars could still be mistaken for +1 rings (they hug the dot; rings stand 0.85 mm off it). |
| Depth | 6 | Declared flat (Op Art / Ben-Day) apart from one plane, the head, with a drop shadow that occludes rings and 3 outputs. |

**Single worst thing:** the swept half is still a regular dot lattice with target rings. It
reads as "sampled" but also a little like a data grid. The five hollow crimson rings on
x = 0 cells at the rim (e.g. (30,120), (73,33)) are the least self-explanatory marks on the
sheet.

## Lineage

Victor Vasarely, *Vega* series (1957–): a lattice swollen by a hidden volume. Here the
lattice's dots are swollen by the thumbprint's distance volume, and the rings are where
that volume bends.

## Engine requests

- `kit` has no rectilinear-mask → polygon tracer or mitred rectilinear offset. Both are
  written locally (`_mask_ring`, `_grow_rectilinear`).
- `geometry.clip` could take a `min_gap` so pieces separated by a grazing cut are re-joined
  (local `_bridge`).
- `giant_type(proportional=True)` advances by ink width but draws each glyph at its font
  origin, so glyphs whose ink does not start at x = 0 (serifed `I`, `1`) sit off-centre. The
  local `_title` sets on the ink box.
