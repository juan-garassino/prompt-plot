# PE carpet (untitled on the sheet) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/transformer/positional-encoding` |
| current render | `gallery/neural-networks/transformer/positional-encoding/candidates/pp_pe_carpet.png` |
| source | `promptplot/generative/generators.py::pe_carpet` |
| paper · pens | a4 portrait (white preview) · 0 navy = even rows (sin channels) · 1 crimson = odd rows (cos channels) |
| status | unreviewed (candidates tier only, no feedback) · `CURATION.md`: "Watch … `pe_carpet` — fine AS a generator (decorative data texture), but not gallery compositions" · 1 render on disk |

## In one line
The sinusoidal positional-encoding matrix drawn as a **laminar/stratified** carpet — each
of 44 horizontal rows is one encoding channel, sin(pos·ω_k) or cos(pos·ω_k) with
ω_k = 10000^(−2k/64) plotted across 80 positions, so frequency falls geometrically from
the bottom row to the top.

## What is on the sheet
- **One mass, full bleed of the drawable area:** 44 horizontal waveform lines from u 0.07
  to 0.93, stacked every ≈ 5.9 mm from v 0.05 (top) to v 0.93 (bottom), alternating navy
  and crimson. Every line runs the full width, edge to edge of the margin; nothing crops
  and nothing else is drawn — no title, no labels, no furniture.
- **Bottom quarter (v 0.72–0.93), the densest and loudest zone:** fast sines. The bottom
  navy row completes ≈ 13 cycles across the sheet; frequency halves roughly every two
  pairs upward. Amplitude is 0.65 × row gap, so adjacent navy and crimson rows **cross each
  other** at every trough/crest — a braided moiré of navy and crimson.
- **Middle band (v 0.45–0.72):** long swells, 1–3 cycles across the width; sin/cos pairs
  drift in and out of phase, making lens-shaped gaps.
- **Top half (v 0.05–0.45):** the slow channels, drawn as near-straight lines. Navy (sin)
  rows tilt gently upward to the right, crimson (cos) rows gently downward, so each pair
  forms a very slight scissor that opens toward the right edge. At 2.5× zoom these flat
  lines show a stair-step micro-jitter (tiny 0.1–0.3 mm ticks along their length —
  coordinate quantisation on near-horizontal polylines).
- **The top crimson row (v 0.05)** is dead straight: cos(0) = 1 lifts it to y1, where
  `_clamp` flattens it onto the margin line.
- **Quiet zone:** none composed. The top half is visually quiet because the physics makes
  it flat, not because space was reserved.

## The science it encodes
`pe_carpet` docstring: "The transformer's sinusoidal positional encoding as a waveform
carpet. Row i draws sin(pos / 10000^(2k/d_model)) (cos on odd channels) … the exact
matrix from 'Attention Is All You Need' as a joy-division carpet. Pure formula; the seed
only jitters nothing." Exact, deterministic: d_model = 64, 44 rows (so channels 0–43 of
64 — the slowest 20 channels are not drawn), positions 0–80 across the width.
**Docstring/render mismatch:** the docstring says "slow frequencies at the bottom, fast at
the top", but row 0 (k = 0, fastest) is placed at y0, which the preview shows at the
bottom — the plate has **fast at the bottom, slow at the top**. What the plate honestly
shows: the geometric frequency ladder and the sin/cos quadrature pairing. What it does not
show: that each *column* (one position) is a unique code — the property that makes PE
work — since nothing reads vertically.

## How it got here
Single render; no trials, no feedback. Generated from the `art` generator with 2 pens.

## Keep — what works
- The frequency ladder is the whole image and it is exact: fast braid bottom, flat lines
  top — a clean density gradient that reads at 3 m as a sheet getting calmer upward.
- The navy/crimson sin/cos pairing: the two pens are not categories but quadrature
  partners, and in the bottom quarter they braid visibly.
- Laminar order is genuinely the mechanism's order (a matrix of channels), not borrowed.
- Continuous single strokes per row — fast to plot, no pen-lift clutter inside a row.

## Weak — what doesn't
- [concept] It is the textbook PE heatmap re-drawn as lines (the Joy Division reference is
  acknowledged in the docstring, which makes it a borrowed look, not a twist); the unique-
  code-per-position property is invisible.
- [hierarchy] One uniform field; no dominant element, no second or third read. The only
  structure is the top-to-bottom gradient.
- [tension] Full-width rows between both margins, dead-square; nothing crops, no
  diagonal.
- [space] The top half is empty-by-physics flat lines — 22 nearly identical horizontals
  are neither quiet space nor content.
- [craft] Adjacent rows overlap (amp 0.65 × gap → crest-to-trough crossing) — ink-on-ink
  crossings at every bottom-row extremum; the top crimson row is clamped flat onto the
  margin; the flat rows carry stair-step micro-jitter the pen will reproduce.
- [depth] Flat and undeclared (a Joy-Division carpet usually gets its depth from
  occlusion — here rows simply cross).
- [concept] Docstring says slow-bottom/fast-top; the sheet is the reverse.

## Next versions
1. **ridgeline** (faithful) — do the Joy-Division move properly: rows as occluding
   ridgelines (each row hides what is behind it, via the Scene3D hidden-line pass), viewed
   slightly from above so the fast channels become a foreground of sharp peaks and the
   slow channels recede into horizon lines. Adds depth and removes the crossings; the
   frequency ladder becomes distance.
2. **the clock face** (mechanism) — PE is a bank of clocks at geometric rates: draw each
   channel pair (sin, cos) as a point on a circle, one ring per frequency, nested
   **radially**; for one position the 32 hands point in 32 directions — that star IS the
   position's code. Draw three positions (e.g. 1, 2, 40) as three overlaid stars in three
   pens; the viewer sees neighbours nearly agree and far positions disagree. Captures the
   uniqueness property the carpet hides.
3. **barcode** (abstract) — rotate the reading: columns are positions. Threshold each
   channel's sign and draw the matrix as a vertical **lattice** of short bars (tone drives
   dash duty), so every column is a visibly different barcode — the fast channels a fine
   stripe at one edge, the slow ones broad blocks — cropped off the right frame to imply
   the sequence continues.

**If only iterating:**
1. Drop amplitude to ≤ 0.45 × row gap so no two rows cross, and stop clamping — inset the
   first row by one amplitude instead of flattening it onto the margin.
2. Replace the 22 slow rows in the top half with 6 widely spaced ones, leaving a real
   quiet band at v 0.05–0.35 for a large-scale title.
3. Fix the docstring (or flip the order) so the slow/fast placement is stated truthfully,
   and resample flat rows with fewer points so the stair-step jitter disappears.
