# lstm-spirals r05 — iterate (THE READOUT) · parent: r04 · 2026-09-29

Lineage. The coil is still Robert Smithson, *Spiral Jetty* (1970) / *A Sedimentation of the Mind*
(1968): one continuous coil, and walking it means walking through time. The new layer is Naum Gabo,
*Linear Construction in Space No. 2* (1949): threads strung under tension between two forms, which
make a surface out of lines alone. Here the 45 grey threads are strung from the red coil to the black
lobe. Canon: Swiss. There is one axis, a spine title, and radical negative space. Declared flat.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/lstm-spirals/rounds/r05/piece.py \
  --fn lstm_readout --seed 7 --paper a4 --palette darkgray,crimson,black,black \
  --out gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13.png
.venv/bin/python studio/lstm-spirals/rounds/r05/render_physical.py \
  gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13.gcode gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13_physical.png
.venv/bin/python studio/lstm-spirals/rounds/r05/piece.py            # writes trace.json
.venv/bin/python studio/lstm-spirals/rounds/r05/check_plate.py gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13.gcode
```

- Final render: `gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13.png` plus `.gcode`. The seed is 7.
- `_physical.png` is the same gcode redrawn at nib widths (grey 0.3, crimson 0.5, black 0.5, type
  0.3) on cream. `render_candidate` draws every pen at one width, so the grey looks about twice as
  heavy there as it will on paper. Judge the hierarchy from the physical render.
- **The plate has no randomness.** The gcode bodies for seed 3 and seed 7 are byte-identical
  (md5 `097db775…`).
- Trials v1–v12 are in `~/Downloads/pp_lstm_spirals_iterate_v*.png`. Nothing was overwritten.
- Files in this round:
  - `piece.py`: the plate.
  - `trace.json`: every per-step quantity with its written definition.
  - `check_plate.py`: reads every channel back off the emitted gcode.
  - `render_physical.py`: the nib-width preview.
  - `lstm_weights.json` and `train_lstm.py`: copied unchanged from r04.
- Runtime is about 3 minutes, most of it the pen-job ordering search.

## Mandate responses

| id | mandate | response |
|---|---|---|
| C1 | two vortices on one vertical axis | **KEPT.** The red eye is at (78.4, 50.2), the black eye at (78.4, 226.1) and the saddle at (78.4, 132.0). All three sit on x = 78.4. |
| C2 | the saddle interleave; the c→h coupling (art M1, science S3/M3) | **FIXED.** h_t = o_t·tanh(c_t) is now drawn as 45 grey threads. Each one starts ON its own half-turn of the red coil (check: 45/45 on the right half-turn, drawn start ≤ 0.009 mm from the red line) and ends at its own comet birth (45/45 within 0.01 mm; the limit was 1.5 mm). All 45 cross the saddle's horizontal: 22 west of the saddle in a 30 mm sheaf and 23 east in a 31.6 mm sheaf, the innermost 2.1 mm from the saddle and the minimum gap 1.2 mm. They split there the way the field does. A finger on the M of MEMORY follows its thread down the east sheaf to half-turn 41. See the capacity arithmetic below. |
| C5 → A10 | Leo pen job | see A10 |
| A2 | static mirror-stacked 8 (tension) | **DEFERRED (partly moved).** C1 keeps the axis vertical. The diagonal energy now comes from the thread sheaves: the chevrons converge on the saddle, the lanes peel off at the letters, and the spokes fan out of the coil. The figure is still close to bilateral. |
| A10 | red in chain order with 0 mm inter-chunk travel; black ≤ 400 mm, no hop > 50; threads no hop > 60; one clean layer each; per-layer table | **FIXED, measured on the emitted gcode after `reorder_by_color`.** Red: 5 chunks, 0.000 mm between chunks, streamed in chain order. Every seam is due north of the eye, at the north point of an open (above-median-gap) top half-turn. Comets: 379 mm travel, max hop 19.3 mm. Threads: max hop 44.2 mm. The layers stream as [0, 1, 2, 3], each once, never re-entered. The table is under Plot budget. **Not fixed:** the type layer (not in the mandate) still has two hops over 50 mm (75.7 and 111.7, between the spine title and the ring). |
| A12 | colophon on a named line | **FIXED.** The colophon is flush-left on the vertical through the figure's rightmost ink (x = 141.65, the east lane's extreme), and its first baseline sits on the saddle's horizontal (y = 132.0). |
| A13 | carry_t, not the well's shape, sets the tone: isotropic, affine, unclamped, all 45 distinct | **FIXED.** The coil is circular about the red eye. gap_t = 0.8 mm + 0.8 mm × mean f_t, with no clamp and no floor hit. Designed gaps run 1.065–1.470 mm and all 45 are distinct. Read back off the gcode, the per-half-turn radial growth recovers mean f to within 0.0055. On the E/N/W/S rays the worst per-turn max/min ratio is **1.12** (the mandate was ≤ 1.5; r04 was 3–5). There is no outward trend: turn 1 averages 1.40 mm and turn 21 averages 1.32 mm. |
| A14 | spine title weight | **DEFERRED.** Still a 0.3 hairline. The grey sheaves already take second place. |
| A15 | proverb tracking | **ARGUED.** The letters are now evenly spaced by arc (7.2 mm step). The uneven look in r04 came from spaces. |
| S1 | checkable per-step trace | **FIXED.** `trace.json` holds, for each of the 45 letters, per-cell i, f, o, g, c and h; the means; carry; RMS(h); the gap; the half-turn geometry; the thread path, start, side and rank; the birth; comet root, full and drawn lengths; and the retention horizon. It also carries written definitions of every mapped quantity (`carry` is defined but not drawn this round) and the model metadata (loss 0.0754, accuracy 1.0). |
| S3 | the c→h coupling | merged into C2, **FIXED** |
| S4 | count equals the caption; key coils to letters | **FIXED.** Drawn half-turns about the red eye: **45.000**. The caption says "45 HALF-TURNS, ONE PER LETTER." Every half-turn is keyed to its letter by its thread. r04's whole-field wraps are gone: all 45 half-turns coil the red eye. |
| S5 | every comet shows its RMS(h) | **FIXED.** Each comet's root, the stretch before its single 1 mm break, is 8 mm × RMS(h_t) long. All roots are reserved before any comet is laid, so none is ever cut. `check_plate` reads RMS for 45/45 within 0.21 % (the limit was 5 %). The newest-cuts-oldest overwrite is kept: 5/45 comets run to their full sweep and the mean drawn fraction is 0.72. |
| S6 | print the 12-step horizon; sediment must not overclaim | **FIXED.** The colophon reads "A WRITE FADES BELOW 10 % IN 12 LETTERS. THE OUTER 6 TURNS, ' BEST MEMORY', ARE ALL IT HOLDS." That is recomputed: max 12 and median 9 over the 34 writes with 12+ steps left, and the last 11 writes run out of sentence first. The inner coil is therefore what the cell has already forgotten. |
| S7 | no encoding.md | **ARGUED / deferred.** The check-number table is below, and `trace.json` plus `check_plate.py` are the machine-readable equivalent. |
| C3, C4, C6, A1, A3–A9, A11, S2 | closed or dropped in LEDGER | still hold: no furniture or arrows; 4 pens, one meaning each; lineage named; no plus marks; label halo ≥ 1.2 mm |

### Capacity arithmetic (C2, done before drawing)

- The r04 pinch was about 17 mm. 45 threads at the 0.8 mm floor need 36 mm across any cut, and at a
  1.1 mm design pitch they need 49.5 mm.
- **Choice: split the family on both sides of the saddle, and let the field widen the waist.** Each
  sheaf crosses the saddle's horizontal on its own side, 22 + 23 threads. The lanes are level sets
  of the lane metric D = u/√|∇u|, with u = (ρ − ρ_s)/|∇ρ|. D equals the true distance to the
  separatrix arms at the waist and is within a few percent of it on the flanks.
- Measured at y = 132.0: west sheaf x 46.3–76.2 (30 mm, 22 threads), east sheaf x 80.5–112.1
  (31.6 mm, 23 threads). Minimum gap 1.20 mm. Innermost threads 2.2 mm and 2.1 mm from the saddle.
- The waist letters (T H E … / … O R Y) take the innermost lanes and pass within ~3 mm of the saddle.
  The flank letters climb outer lanes and wrap the lobes. The lanes stack by destination and peel off
  one at a time, so the grey band tapers to a single line over the top of the black lobe.

## What changed from parent

- **The waist is the readout.** In r04 the two memories sat on either side of an empty separatrix.
  Now the output gate strings them together: 45 grey threads, one per letter, from its half-turn to
  its comet.
  - Each thread leaves the coil on the potential's orthogonal σ-line. These cross the rings at 75–90°
    (mean 83°) and split at the saddle.
  - It then steps out to its lane along the lane metric's normal, so it crosses other lanes at right
    angles.
  - It rides the lane around the lobe and dives into its letter on the black σ-line, landing 1.2 mm
    behind the glyph.
  - The sheaves converge on the saddle as two chevrons. This is r01's interleave (and the reference's
    saddle convergence) rebuilt as a measured coupling.
- **The coil is honest.**
  - It is circular about the red eye, so it is isotropic.
  - The gap is affine in mean f_t and unclamped.
  - There are exactly 45 half-turns, with a 6 mm bare eye.
  - r04's field-wide red wraps (12 letters, 39 half-turns counted) were dropped. The outer 6 turns of
    the same coil are the 12-letter horizon, and the colophon says so.
- **Comets keep the overwrite wit and show the true value.** Every comet has a reserved root gauge
  (RMS × 8 mm), then a 1 mm break, then the sweep that newer comets cut.
- **The pen job is designed against the emitted order.** The piece replicates the pipeline's
  per-colour greedy on the 0.01 mm output grid. An earlier trial (v10/v11) lost the thread-layer
  optimisation to sub-0.01 mm ties: optimised hops of 44 mm came out as 183 mm. The piece:
  - seams the red due north, which keeps chain order;
  - alternates comet direction in and out around the rim;
  - flips stranded grey dashes and glyph strokes until no in-layer hop exceeds 45 mm where possible.
- **Composition moves across trials:**
  - v1: the first sheaf, where u-lanes flared 2× at the waist.
  - v3: u/|∇u| pinched too hard.
  - v4: u/√|∇u| gave the smooth hourglass.
  - v6: the dilated stack stopped lanes pinching at peel points (965 → 86 near-parallel pairs).
  - v9: spokes moved onto the lane normal, which made them boxy and was reverted.
  - v10: σ-spokes plus normal joins.
  - v12: optimisation on the rounded grid.
  - v13: the gauge was shortened to 8 mm after 14 mm roots touched at the black lobe's tip (0.45 mm).
  - Axis moved to 0.36 W so the colophon fits between the figure and the spine.

## Measurements / computations

**Model (real, unchanged from r04).**
- The 8-cell char LSTM from `lstm_weights.json` runs forward over "." plus the proverb: 46 steps,
  45 drawn.
- Loss 0.0754 nats/char, next-character accuracy 1.000.
- Largest |h| over the run is 0.997 (< 1).
- Per-letter ranges: mean f 0.332–0.837, mean o 0.486–0.966, RMS(h) 0.373–0.770.

**Check-number table** (designed vs read back off the v13 gcode by `check_plate.py`):

| quantity | designed | drawn (gcode) | OK |
|---|---|---|---|
| red half-turns about the eye | 45 | 45.000 | ✓ |
| gap_t = 0.8 + 0.8·mean f (mm) | 1.065–1.470, 45 distinct | 1.066–1.471; mean f recovered ±0.0055 | ✓ |
| isotropy, worst per-turn E/N/W/S ratio | ≤ 1.5 | 1.12 (21 turns) | ✓ |
| thread k starts on half-turn k | 45 | 45/45, ≤ 0.009 mm off the red line | ✓ |
| thread k ends at birth k (≤ 1.5 mm) | 45 | 45/45, max 0.01 mm | ✓ |
| thread inked fraction = mean o_t | 0.486–0.966 | max err 0.001, corr 1.0000 | ✓ |
| comet root = 8 mm × RMS(h) | 2.98–6.16 mm | 45/45, max rel err 0.21 % | ✓ |
| retention horizon | — | max 12, median 9 (recomputed from f) | printed |
| red chunks inter-chunk travel | 0 | 0.000 mm, chain order | ✓ |
| layers | 0 → 1 → 2 → 3 | [0, 1, 2, 3], each once | ✓ |

**Spacing** (gcode, samples every 0.4 mm, side-by-side near-parallel pairs under 0.8 mm):
- grey–grey: 55 pairs. Most sit at 0.79 mm (lanes at the saddle chevrons); the minimum is 0.68 mm at
  the east shoulder.
- red, black and cross-pen: 0.
- r04 black had 84 samples under 1.0 mm. Red self-spacing is ≥ 1.07 mm.

**Other measurements:**
- Crossings: 121 thread pairs are not nested. These are the half-turn parity inversions: odd letters
  own the top half of each turn and even letters the bottom half, so on each side the two parities
  leave the coil from different quadrants. Every such crossing is grey over grey, at a right angle,
  on the coil's shoulders.
- Thread lengths are 71–331 mm, 9.05 m in all.

## Plot budget (emitted gcode; Leo at F600 draw, 2000 mm/min travel, 1 s per lift+drop)

| layer (order) | pen | strokes = cycles | draw mm | in-layer travel mm | max hop mm | hops > 50 | min |
|---|---|---|---|---|---|---|---|
| 0 | grey 0.3, o_t threads | 1145 | 7038 | 2722 | 44.2 | 0 | 32.2 |
| 1 | crimson 0.5, c_t coil | 5 | 2934 | 0 | 0.0 | 0 | 5.1 |
| 2 | black 0.5, h_t comets | 88 | 2902 | 379 | 19.3 | 0 | 6.5 |
| 3 | black 0.3, type | 628 | 2087 | 1851 | 111.7 | 2 | 14.9 |
| **total** | 4 pens | 1866 | 14962 | 4952 | | | **58.7 + 3 swaps** (~65 min with frame trace and swaps) |

- The grey layer is the long session: 1145 dash lifts. Its travel is mostly the dash gaps themselves
  (Σ gap ≈ 2.0 m).
- Batching: every stroke is a clean boundary, and red chunks are 273–835 mm (about 0.5–1.4 min each).
- Bounds: x 0–199.4, y 17.6–268.4 inside the a4 drawable area.

## Self-critique (rubric)

1. **Hierarchy: 8.** In the physical render the red coil and the black whorl (both 0.5) carry the
   sheet, and the grey 8 binds them quietly. In the one-width preview the grey reads heavier than it
   will plot.
2. **Grid: 7.** One axis. The title spans the figure's ink exactly (17.6 → 268.4). The colophon sits
   on the rightmost-ink vertical and the saddle horizontal. The figure's left edge shares no line
   with anything.
3. **Tension: 6.** Still a bilateral stack (C1). The chevrons and the peel-off taper add movement but
   no diagonal.
4. **Negative space: 7.** The waist gap between the sheaves is kept, as are the bare eyes and the
   right column. The upper right (x 150–185, y 150–270) is plain gap.
5. **Craft: 7.** No floods. 55 grey pairs sit just under 0.8 mm. The coil's shoulders carry a woven
   patch of grey–grey right-angle crossings. Bottom-half spokes leave the coil to the SW/SE and their
   lanes cup under it (the "ears" at x ≈ 30–50 and 120–140, y ≈ 20–45).
6. **Concept: 8.** One continuous red line against 45 short black strokes, strung together by the
   output gate. Every mark is traceable letter to half-turn to thread to comet, and the colophon
   decodes each channel.
7. **Depth: 6 (declared flat).** Depth is the over/under of the pen order (grey under red and black)
   and the nesting.

**Single worst thing:** the shoulders of the coil. Because of half-turn parity, alternate letters
must leave the coil from opposite half-planes. About 60 grey crossings per side therefore pile up
around 10 o'clock and 2 o'clock on the coil, and the bottom-half spokes throw lanes under the coil.
Everything else in the thread layer is ordered; that corner is a weave rather than a sheaf.

## Engine requests

- `render_candidate.py --pen-widths` (or the physical preview by default). The grey sheaf is judged
  at the wrong weight without it. This round ships `render_physical.py` as a workaround.
- `postprocess.reorder_by_color(..., keep_order=True)`: stream a colour's strokes in authored order.
  Pieces currently have to replicate the greedy and optimise against 0.01 mm rounding ties.
- The visualizer silently switches to a dark background for `silver` (`_needs_dark_bg`). A light
  grey pen then previews as dark paper.
