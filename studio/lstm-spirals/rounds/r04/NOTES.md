# lstm-spirals r04 — memory-strata · parent: r01 · 2026-09-28

Lineage: Land Art. Robert Smithson, *Spiral Jetty* (1970), read through his essay *A Sedimentation
of the Mind* (1968). The order this plate takes from it is **one continuous coil, where walking
the coil means walking through time, laid down as sediment**. The red cell-state line is that
coil. The twist is the proverb that the network reads: *THE PALEST INK IS BETTER THAN THE BEST
MEMORY*, plotted in ink. Canon: Swiss. The title is set at poster scale as a spine, there is one
huge form, and the negative space is radical. The plate is declared flat (see self-critique).

## Render

```
.venv/bin/python scripts/render_candidate.py studio/lstm-spirals/rounds/r04/piece.py \
  --fn lstm_memory_strata --seed 7 --paper a4 --palette crimson,black,black \
  --out gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png
```

- Final: `gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png` + `.gcode`. The geometry is identical to v17.
- Seed 7. **The plate has no randomness.** Seeds 3, 7 and 11 give byte-identical gcode bodies
  (md5 `45d67a…` at v14 and `5674a6…` at v17/v18). The weights and the proverb determine the sheet.
- Trials v1–v17 are in `~/Downloads/pp_lstm_spirals_memory-strata_v*.png`. None was overwritten.
- Files in this round: `piece.py` (the plate), `train_lstm.py` (the offline trainer, run once) and
  `lstm_weights.json` (the trained weights, which the piece runs forward at render time).

## Mandate responses

`LEDGER.md` and `FEEDBACK.md` do not exist for this slug, so there are no numbered J/A/S rows.
The binding brief is the curator note, and the work order is the Weak list in DESCRIPTION.md.
Both are answered below.

| id | mandate | response |
|---|---|---|
| CUR-1 | Keep two black/crimson vortices on one vertical axis | **FIXED/KEPT.** The black eye is at (78.4, 228.8) and the red eye at (78.4, 52.9), on one vertical axis. The saddle is between them at (78.4, 129.4). |
| CUR-2 | Keep the streamlines interleaving around the saddle | **ARGUED (partial).** The four families meet the saddle from its four sectors: the red lobe's last loop from below, the black lobe's tip (THE…Y comets and letters) from above, and the red wrap loops pinching from the left and right. Together they draw the saddle's hyperbolic portrait. They do not cross the separatrix. In this order the cell orbit and the hidden state live on either side of it by construction, so the waist stays blank paper, like the separatrix in `bauhaus_gradient`. |
| CUR-3 | Fold or cut 'LSTM EQUATIONS', 'FLOW LEGEND', and the arrow/label callouts | **FIXED.** No equations block, legend, arrows, leaders or t-labels remain. The gate equations are now the geometry: the forget gate sets the red pitch, and the tanh bound means no black stroke closes a turn. The only type left is the input itself, the spine title, and an 11-line colophon. |
| CUR-4 | Plotting: pens only with meaning, clean layers with a stated order, spatial ordering, minutes per layer | **FIXED.** There are 3 pens, and each has one meaning. Layers run crimson → black → type (see Plot budget). The red line is cut into ≤280 mm strokes so every stroke can be a batch boundary. The longest stroke is 280 mm and the largest in-layer hop is 173 mm. |
| CUR-5 | Name the LINEAGE | **FIXED.** Smithson, *Spiral Jetty* / *A Sedimentation of the Mind* (above). |
| W-concept | It reproduces a textbook schematic, and the mechanism is not in the geometry | **FIXED.** The plate is a real trained LSTM run forward at render time. Carry and RMS(h) are drawn exactly (see Measurements). |
| W-tension | Congruent 180° lobes, centred | **FIXED.** Lobe weights are c_b=1.3 and c_r=1.0, so the black lobe is larger (its separatrix reaches 44 mm above the eye, the red one 30 mm below). The axis sits at 0.36 W with a 57 mm quiet column and the spine on the right. |
| W-craft | Red through a label; plus mark on the L | **FIXED.** The closest approach between pens is 1.06 mm (black to type), and red never comes within 1.5 mm of another pen. There are no plus marks. |
| W-hierarchy | The third layer (dotted t-rings) is swallowed | **FIXED by removal.** There are three layers with three different roles, and nothing is dotted. |
| W-grid | Left labels float in leftover white | **FIXED.** The spine title's inked length is set to span the figure exactly, from the red coil at y=19.9 to the red crown at y=277.0 (cap height 12.5 mm). The colophon is centred on the saddle's horizontal and right-aligned to the title gutter (9 mm). |
| W-space | The empty left third is residue | **FIXED.** The white is the waist void between the lobes, the two eyes, and the right column, all shaped by the separatrix. |
| W-depth | Flat and undeclared | **ARGUED / declared flat.** The subject is a planar potential. Its depth is the nesting: the red wrap encloses the text ring, which encloses the whorl, which encloses the eye. |

## What changed from parent

- **Order: from a double vortex with a textbook label deck to NESTED on one complex potential.**
  The potential is F(z) = 1.3·log(z−z_b) + 1.0·log(z−z_r). Its separatrix happens to be an
  upright ∞, which is an hourglass. It was not drawn; it falls out of the field.
- **The red is ONE line.** It grows outward from the red eye like tree rings: half a loop per
  character, with a pitch of 1.8 mm × carry per loop. The first 34 characters coil inside the red
  lobe and form the dense strata. The last 12, " BEST MEMORY", leave the lobe and wrap the whole
  field. In the plate, long memory holds the short, and the words doing the holding are BEST MEMORY.
- **The black is 45 strokes, one per character.** Each is born just inside its letter on the rim
  of the black lobe and falls toward the black eye. None can close a turn. Comets are laid newest
  first, and an older one dies where it meets a newer one. The first word, THE, keeps only
  5/8/17 mm of its 136/135/126 mm sweeps.
- **The input is the type.** The proverb is set around the black lobe's rim at the separatrix
  offset (letter height + 2.2 mm), reading clockwise from the saddle.
- **Furniture:** all of it was cut. What remains is a vertical spine title, LONG SHORT-TERM MEMORY,
  and a small colophon at the waist.
- **Composition moves across the trials:** v1–v2 had 46 full peanut loops, the figure ran off the
  sheet and it was all red. From v3, a turn is a fixed angle of the potential. v5 put the text on
  the physical separatrix offset so it reaches the saddle. From v9, comets die instead of stuttering
  through pause-resume. v11 set half a turn per character, which cut red from 10.3 m to 3.8 m. v12
  scaled and moved the figure to 0.36 W and put the colophon at the saddle. v13 dropped the dotted
  separatrix, which collided with the red. v15 merged red strokes to kill the joint seam. v17 set
  comet separation to 1.0 mm.

## Measurements / computations

**The network (real):** `train_lstm.py` trains a one-layer LSTM with 8 cells. It is character
level, with a 28-symbol vocabulary. The corpus is 12 sayings about memory and writing, and the
target proverb is one of them. Training uses full BPTT with Adam (4000 steps, all lines in one
masked batch) and forget bias 1.
- Finite-difference gradient check: worst relative error 8.3e-7.
- Corpus loss 3.33 → 0.082 nats/char.
- On the proverb: 0.075 nats/char, next-character accuracy 1.000 (memorised).
- The piece runs the forward pass itself (`run_lstm`) over "." plus the proverb, which is 46 steps.

**Drawn quantities, per character:**
- `carry_t = |f_t ⊙ c_{t−1}| / |c_{t−1}|` is the fraction of the cell norm the forget gate carries
  across that character. Range 0.38–0.95, mean 0.73.
- `pitch_t = max(0.9, 1.8·carry_t)` mm. Five characters sit on the 0.9 floor: the start token,
  P, N, the second I, and B.
- `RMS(h_t)` ranges 0.37–0.77, mean 0.60. Each comet sweeps RMS(h_t) × 2π·c_b of the angle σ.
  The largest |h| entry over the whole run is 0.9973, which is below 1 as tanh requires.

**Field:**
- Eye separation L = 175.9 mm. The saddle sits at z_s = (c_b z_r + c_r z_b)/(c_b+c_r), where F′ = 0.
- The separatrix is traced by rays from each eye (march 0.5 mm, then bisect 40 times, tolerance 1e-3 in ρ).
- The red line and the comets are followed by Newton continuation in (ρ, σ), with the two
  arguments unwrapped so σ never jumps a log branch. The red line steps adaptively at ≤0.4 mm of
  paper per sample, which is what removed a faceted cusp at the saddle, where |F′|→0.
- Pitch is held at each loop's tightest point: Δρ = pitch · max|F′| over the last full loop.
- Comet inflow: dρ/dσ = −μ, with μ = 0.45.

**Comets:** the swept length would be 4557 mm; 3348 mm is drawn (73.5 %), and 37 of 45 comets
are cut by a newer comet. The eight that keep their whole sweep are S (of IS), R, T (of THAN),
E (of the second THE), B, S (of BEST), E (of MEMORY) and Y.

**Spacing:** sampled at 0.25 mm, there are **zero** near-parallel sample pairs under 0.8 mm
within the red layer (stroke joints excluded) or within the black layer. The closest approach
between pens is 1.06 mm (black to type). Red never comes within ~1.5 mm of black or type.

**Bounds:** the extent is x 22–200, y 19.9–277, inside the drawable 10–200 × 10–287. There are
no clamp violations.

## Plot budget

| layer (order) | pen | strokes | draw | in-layer travel | ~min on Leo* |
|---|---|---|---|---|---|
| 0 first | crimson 0.5 — the cell state | 14 (≤280 mm each) | 3.81 m | 0.23 m | 6.9 |
| 1 | black 0.5 — hidden-state comets | 45 | 3.35 m | 1.86 m | 8.0 |
| 2 last | black 0.3 — type (proverb, spine, colophon) | 281 | 1.40 m | 1.24 m | 12.3 |

\* Assumes F600 draw, about F2000 travel and about 2 s of lift and drop dwell per stroke.
**Total ≈ 27 min**, plus 2 pen swaps and the frame trace.

- Whole file: 25,285 commands, draw 8.56 m, travel 3.81 m (including home and layer hops), 340 pen lifts.
- The previewer grades it A (composition 0.93).
- Layer order is light to dark, so the black comets and type land on top.
- The type is its own layer (house law) and goes last, so glyphs are never over-inked.
- Stroke order within each layer is the pipeline's per-colour nearest-neighbour. Red strokes
  chain end-to-start.

## Self-critique (rubric)

1. **Hierarchy: 8.** At 3 m the red hourglass/∞ and the black whorl in its upper bulb carry the
   sheet. The spine title reads second and the proverb ring third. The pitch rhythm of the strata
   and the colophon reward 30 cm.
2. **Grid & alignment: 8.** There is one axis. The title spans exactly the figure's red extents,
   and the colophon sits on the saddle's horizontal, right-aligned to the title gutter. The
   figure's left edge (22 mm) does not share a line with anything, which is a small loss.
3. **Tension & asymmetry: 7.** The lobes are unequal (1.3 : 1), the mass is left, the column and
   spine are right, and the red end hangs loose on the upper-right shoulder. The figure itself is
   still near-bilateral about its axis. Only the pinwheel's handedness and the red end break it.
4. **Negative space: 8.** The waist void, the two eyes and the right column are all shaped by the
   separatrix. Nothing is leftover residue.
5. **Craft for pen: 8.** Spacing is clean (above), there are no floods and nothing collides across
   layers. The red is batchable. Type is hairline at 3.2 mm, and the colophon at 1.6 mm is small.
6. **Concept legibility: 8.** One continuous line versus 45 broken strokes is the whole point, and
   it lands without the caption. The proverb, and BEST MEMORY being the loops that enclose, are the
   wit. The gate mapping still needs the colophon to be decoded.
7. **Depth: 6 (declared flat).** Depth is nesting only. There is no line-weight fall-off into the
   eyes.

**Single worst thing:** the saddle is a void and not an interleave. The curator liked the r01
sheaves crossing between the lobes, and this order keeps the two memories on either side of the
separatrix, so they never cross. The second worst is the comet overwrite: 26 % of the swept
length is cut, so a comet's drawn length equals RMS(h) only for the 8 uncut comets. The rule is
stated, but it is still a loss of direct readability.

## Engine requests

- `Scene3D.lines(mode="stop")`: cut a line at its first crowded sample and never resume. This is
  the "overwrite" semantics. It was done here with `Occupancy.crowded()/add()` directly.
- `kit.text_on_path(text, polyline, h)`: glyphs along a curve with tangent-aligned baselines.
  `glyph_on_curve` is local to this piece.
- `render_candidate.py --pen-widths`: the preview draws every pen at one width, so the declared
  0.5/0.5/0.3 hierarchy is invisible in the PNG.
