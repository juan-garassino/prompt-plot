# FORWARD PASS / (misfiled) superformula bloom — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/perceptron` |
| current render | `gallery/neural-networks/perceptron/promoted/pp_superformula_bloom_seed25.png` (the only file in `promoted/`) · the real perceptron-family head is `gallery/neural-networks/perceptron/candidates/prior-approved/pp_bauhaus_loom_FORWARDPASS_APPROVED.png` |
| source | `promptplot/generative/pieces/ml.py::bauhaus_loom` (FORWARD PASS) · the promoted png is `promptplot/generative/generators.py::superformula_bloom` · trials: `pieces/ml.py::bauhaus_settling`, `pieces/ml.py::bauhaus_perceptron` (KILLED, deregistered) |
| paper · pens | bloom: a4 portrait, 1 pen (purple preview = pen 0) · loom: a4 landscape · 0 blue = warp threads · 1 pink = weft threads (long floats doubled) · 2 black = selvage frame + type · bloom fx variants: 17x24 cm, 3 pens (skyblue / hotpink / gold) |
| status | promoted tier on disk, **no recorded feedback** · loom = APPROVED (CLAUDE.md, BAUHAUS UNIVERSUM) · `bauhaus_perceptron` = KILLED (CURATION.md) · 15 renders on disk |

**Filing bug, read first.** `scripts/gallery_import.py` routes on the regex
`loom|forwardpass|perceptron|settling` → `neural-networks/perceptron`. `loom` matches
"b**loom**", so `pp_superformula_bloom_seed25.png` (promoted) and the three
`pp_fx_*_bloom_*` variants landed in this subject by accident (`gallery/MOVES.tsv`
lines 170, 262–271). They are generative curves, not a perceptron. This file describes
both, but the family the studio should iterate is FORWARD PASS.

## In one line
A weight matrix drawn as **interlacing** — sign is over/under (blue warp on top where
w ≥ 0, pink weft on top where w < 0), magnitude is float length; the misfiled bloom is
a **nested/orbital** stack of 42 rotating superformula shells carrying no ML mapping at all.

## What is on the sheet

### promoted — `pp_superformula_bloom_seed25.png` (a4 portrait, 1 pen)
- **Dominant mass:** one nested bloom of 42 closed superformula outlines, centred at
  (u 0.50, v 0.50), spanning u 0.10–0.90 and v 0.21–0.80 — ≈ 0.80 of sheet width.
  Outline is a lumpy, roughly 5–6-lobed disc; the outer shells bulge furthest toward
  the right (u≈0.90, v≈0.50) and lower-left (u≈0.10, v≈0.45).
- **Centre:** a small open eye ≈ 0.03 W across at (0.50, 0.50); the innermost ~8 rings
  are tight, faceted polygons with visible sampling kinks (jagged, not smooth).
- **Fold seams:** because each shell rotates 2° the lobes slide over one another and
  the outlines pile into three crisp crease lines — upper-left (u 0.21→0.55, v 0.43→0.36),
  right (a long arc from u 0.78, v 0.33 sweeping down and left to u 0.60, v 0.66, ending
  in a row of small cusps along the bottom right at v≈0.66), lower-left (u 0.33→0.36,
  v 0.60→0.72). Along each crease the ring spacing collapses to near zero and small
  saw-tooth spikes appear.
- **Quiet zone:** the whole band v 0.80–0.95 below the bloom and v 0.05–0.20 above it
  is blank paper; no type, no furniture anywhere on the sheet.

### variants — `pp_fx_echo_dashrain_bloom_seed3.png` (and siblings)
- A different seed's bloom (≈7 soft lobes, a 7-arm pinwheel of fold seams from the
  centre) echoed in three pens (skyblue, hotpink, gold) with a few-mm drift per copy,
  so every outline is a triple rainbow line; fills u 0.15–0.93, v 0.22–0.78 on 17x24.
- Gold vertical dash-rain fills all remaining paper edge to edge; a hotpink dash halo
  hugs the bloom's rim. The rain meets the frame on all four sides.

### loom family head — `pp_bauhaus_loom_FORWARDPASS_APPROVED.png` (a4 landscape, 3 pens)
- **Dominant mass:** a single woven rectangle (the "cloth") from u 0.06 to 0.93, v 0.16 to
  0.86 — ≈ 0.87 W — framed by one thin black selvage rectangle.
- **Inside:** 52 vertical blue warp threads × 34 horizontal pink weft rows at ≈5 × 4.4 mm
  pitch. Each thread is broken into segments: a blue segment wherever warp is on top,
  a pink segment wherever weft is on top, a short gap at each crossing where the lower
  thread ducks under. Pink floats range from a 1-cell tick to runs of ~12 cells; floats
  longer than 2.4 cells get a second pass 0.25 mm below, so they read bolder. Visual
  texture: a scatter of bold pink dashes over a blue-and-pink tick field.
  **No visible clustering** — the long pink floats are spread evenly across the whole
  cloth, no block or diagonal structure reads.
- **Type:** top-left above the cloth, spaced caps: `FORWARD PASS` (u 0.06, v 0.06,
  ≈3 mm) with a short underline, then `THE WEIGHTS WOVEN` (v 0.10, ≈2.2 mm; the comma in
  the code does not render). Footer bottom-right, right-aligned to the cloth edge:
  `LAYER Q  52X34  WARP IN WEFT OUT` (u 0.50–0.93, v 0.93; the `=` signs do not render).
- **Furniture:** a tiny black/blue/pink swatch stack at top-right (u 0.93, v 0.08).
- **Quiet zone:** none worth the name — the cloth fills the drawable area; only the
  ~6 % title band and the footer band are empty.

### earlier trials
- `pp_bauhaus_perceptron_seed5_v2.png` (a4 landscape): a 6-8-8-3 MLP wiring diagram —
  blue concentric-ring input discs (u 0.17), black open circles in two hidden columns
  (u 0.39, 0.61), pink output discs (u 0.83), black connection lines of 1–3 passes, one
  pink winning path, and a solid black vertical hatch bar (u 0.60–0.63, full height)
  behind the third column. Title `FORWARD / PASS` top-left, `M 1 80` bottom-right.
- `pp_bauhaus_settling_v1_seed14 / v3_seed5` (a4 portrait): `SETTLING` / `THE LINE THAT
  ERRORS BUILT` top-left, blue dots (class +) scattered upper-right, pink open circles
  (class −) lower half, a few ringed large discs for the most-influential errors; v3
  adds a fan of ~16 black boundary lines converging on one pivot near (0.58, 0.50) and
  the pink settled cut. Footer `W  Y X  15 UPDATES` bottom-right. Lower-left and the
  whole left third empty.

## The science it encodes
- **Loom** (`bauhaus_loom` docstring): "a real weight matrix woven as warp/weft threads,
  over/under by sign, float by magnitude." With `weights=` it loads the Q matrix of a
  checkpoint (`_load_qkv(...)[0]`); otherwise a **seeded uniform random 96×96 matrix**.
  Block-mean downsample to 52×34, then rows and columns are **sorted by mean weight**
  (a permutation that leaves the function unchanged) so same-sign regions should
  cluster. Exact: sign → which thread is on top at every crossing; float doubled when
  the run is > 2.4 cells. Footer claims "LAYER Q". The render shows no clustering, which
  is what a random matrix gives after the sort — so the approved render very likely
  encodes **seeded noise, not trained weights**; the "LAYER Q" caption is then untrue.
  Note also: "float by magnitude" is only indirect — float length is a run of same-sign
  cells, not |w|; |w| drives nothing except the 92nd-percentile norm used by an unused
  `strong()` helper.
- **Settling** (`bauhaus_settling` docstring): real online Rosenblatt updates on a
  seeded separable cloud; successive boundary positions ghost from wild to settled; the
  2–3 errors that rotated the line most are the large discs. Exact algorithm, seeded data.
- **Bloom** (`generators.py::superformula_bloom`): Gielis superformula, seed picks
  m, n1–n3; 42 shells scaled 0.06→1 with a cumulative 2°/shell twist. Pure decoration —
  it encodes no perceptron mechanism.

## How it got here
1. `bauhaus_perceptron` v1→v2 (2026-09-12/13, identical hashes): an MLP wiring diagram.
   KILLED in `CURATION.md`: "wiring diagram — a schematic cannot be art". Lost nothing worth
   keeping except the idea of one scarce pink path.
2. `bauhaus_settling` v1→v3 (2026-09-13): the perceptron as its learning motion. v1 was
   only dots and three rings (nearly empty sheet, 734 mm of ink); v2/v3 added the fan of
   ghost boundaries and the pink settled knife. Gained a real mechanism; lost to a sheet
   that is still mostly scatter and a fan pivoting dead-centre. Never promoted.
3. `bauhaus_loom` FORWARD PASS v1 → v2 → APPROVED: the matrix as weaving. Changes are
   minor (title block tightened, swatch, footer); the approved version is the one listed
   as the INTERLACING exemplar in `DESIGN_RUBRIC.md` § 6.
4. The superformula bloom + fx variants arrived via the `loom`⊂`bloom` regex bug.

No feedback recorded in `studio/feedback.jsonl` for this subject.

## Keep — what works
- The mapping "sign = over/under" is exact, one-line, and visible at every crossing of
  the loom — the purest statement of the rubric's abstract-order rule in the collection.
- Two pens split by role (blue = input axis / warp, pink = output axis / weft); the
  doubled long pink floats are the only bold marks, so pink reads as the loud pen.
- The cloth as the whole sheet: a dominant mass at ≈ 0.87 W with type sitting outside it
  on the cloth's left edge (title) and right edge (footer) — shared axes, no floating.
- Bloom: the three fold seams (upper-left, right arc, lower-left) are the only strong
  event in that plate and read as geological creases — worth borrowing as a *mechanism*
  (lines forced together) if anything is taken from it.
- Settling: the idea that the perceptron is its **boundary in motion**, with the
  causes (the misclassified points) drawn as scarce big discs.

## Weak — what doesn't
- [concept] The promoted png of this subject is not a perceptron at all — it is a
  generic superformula bloom promoted into the wrong family. Fix the filing before any
  judgement is based on it.
- [concept] Loom: the matrix is seeded noise (no clustering visible), yet the footer says
  `LAYER Q`. The permutation-sort that should reveal structure reveals nothing, so the
  plate is a random weave; the claim and the ink disagree.
- [hierarchy] Loom: everything is the same scale — 52×34 equal cells, a near-uniform
  texture edge to edge; no dominant region, no second or third read at 1 m. At 3 m it is
  a pink-blue tweed swatch.
- [space] Loom: no quiet zone at all; the cloth fills the drawable area and the title
  band is only ≈6 % of height. Nothing makes the dense zone louder.
- [tension] Loom: centred rectangle with even margins and an edge-aligned footer — the
  "subject floating dead-centre" failure mode, just larger.
- [depth] Loom: flat, and flatness is not declared; the over/under gap is the only depth
  cue and at 0.34 × pitch it is too small to read as a real interlace.
- [craft] Loom: travel 21.4 m > draw 16.1 m (12.5 k commands of 1-cell ticks) — the
  tick field is expensive and mostly pen-lifts.
- [craft] Bloom: innermost ~8 rings are faceted polygons with jagged kinks; along the
  three fold seams ring spacing collapses to 0 and saw-tooth cusps appear (ink pooling).
- [tension] Bloom: centred on the sheet with even side margins and blank top and bottom
  bands — dead-centre subject.
- [concept] Settling: reads as a scatter plot with a line fan — the scientific-figure
  failure; the pivot sits near the centre and the left third is empty by accident.

## Next versions
1. **trained-cloth** (faithful) — keep the loom exactly, but weave a **real trained**
   matrix (a checkpoint's Q, or a trained perceptron on a real dataset) after the mean
   sort, so same-sign regions visibly cluster into bands and a block diagonal. Crop the
   cloth off one edge (let the warp run past the right frame) and open a genuine quiet
   band for the title. Scores higher on concept (the caption becomes true) and
   hierarchy (clusters give a dominant pink field vs a blue field).
2. **settling-weave** (mechanism) — fuse the two perceptron strands: the cloth is woven
   row-by-row as training proceeds; each Rosenblatt update rewrites one weft pick, so
   the top of the cloth is noisy and the bottom converges into the settled pattern — the
   learning curve becomes the cloth's own gradient from chaos to order, one pink pick
   marking each update that flipped a sign. Time becomes the vertical axis without a
   chart axis anywhere; gives the plate a direction and a quiet (settled) zone.
3. **the tear** (lens) — a single enlarged patch of cloth (8×6 threads at ~25 mm pitch)
   with a real 3D interlace (threads with thickness, occlusion at every crossing via the
   z-buffer engine) so over/under is physically legible, and one thread snapped where
   the weight crosses zero, frayed ends crossing the frame. Buys depth and a single loud
   event; the twist is that "a perceptron is a fabric, and a dead weight is a broken thread".

**If only iterating:**
1. Re-file `pp_superformula_bloom_seed25.png` and the three `pp_fx_*bloom*` variants
   out of this subject (fix the `loom` regex to `\bloom|bauhaus_loom`), and promote the
   loom APPROVED render as this subject's current.
2. Render the loom with `weights=<trained ckpt>` and confirm by eye that pink and blue
   separate into at least two contiguous regions after the sort; if they do not, the
   footer `LAYER Q` comes off.
3. Shrink the cloth to ≈ 0.62 W, push it against the right frame (crop the last ~6 warps)
   and give the left 0.30 W to a large-scale title set on the cloth's top edge.
