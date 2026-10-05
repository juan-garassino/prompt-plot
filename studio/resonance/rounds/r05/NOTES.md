# resonance r05 — benchmark-kept · parent: r01 (v13) · 2026-09-28

Faithful thesis. v13 is still the family benchmark: same composition, same six pens and meanings,
same packet and hero vocabulary. What changed is how each mark is made, what gets inked twice, and
what order it streams in on Leo. r03 is an abandoned partial round and was not used.

**Lineage.** Thomas Young, *A Course of Lectures on Natural Philosophy and the Mechanical Arts*
(1807), Plate XX Fig. 267. It is the first engraving of two-source interference, drawn as two
families of concentric circles, and the interference shows only where their lines cross. The
order it lends is **interfering**: two crest families, no tone, crossings as the result. That is
the construction of this plate's hero. Movement: the natural-philosophy engraving plate.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance/rounds/r05/piece.py \
  --fn attention_benchmark_kept --seed 7 --paper a4 --orientation portrait \
  --palette goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black \
  --out gallery/studio/resonance/current/pp_resonance_benchmark_kept_v7.png
```

- final: `gallery/studio/resonance/current/pp_resonance_benchmark_kept_v7.png` + `.gcode` (seed 7)
- The plate is **seed-independent**. r01's only random draw was the 60 scatter marks, which are
  now cut. Seeds 7, 11 and 23 give byte-identical G-code bodies (md5 `6859d04d…`).
- `--colors` defaults to the palette length (6). **The palette order is the stream order**, see
  Plot budget. It is not the siblings' index order, but every colour keeps its family meaning.

## Mandate responses

`studio/resonance/` has no LEDGER.md and no FEEDBACK.md, so there are no open J*, A* or S* rows. The
work order was the curator note plus DESCRIPTION.md's "benchmark-kept" brief and its Weak and
If-only-iterating lists:

| id | mandate | status |
|---|---|---|
| C1 | keep the family grammar (Q crimson, K blue, V goldenrod, Z green, MoE/Y violet, Huygens field as hero) | FIXED: kept, every colour keeps its meaning |
| C2 | no pen cap; keep all 6 if each carries meaning; one clean layer per pen, state the order | FIXED: 6 layers, never re-entered, streamed light to dark (see Plot budget) |
| C3 | strokes spatially ordered for batching | FIXED as far as the piece can. Neighbouring runs alternate direction (boustrophedon) so the per-colour nearest-neighbour pass walks the sheet. Longest single stroke is 429 mm (the Z carrier, 43 s). The rest belongs to the engine; see Engine requests |
| C4 | minutes per layer + total in NOTES | FIXED: table below |
| C5 | cut the waste: 3,471 pen cycles and 110 % travel, mostly dotted leaders | FIXED: **1,960 cycles (−44 %), travel 9.17 m = 92 % of draw**, estimated Leo time 150 → 98 min |
| C6 | benchmark-kept = keep v13's composition, fix craft, don't cut colours | FIXED: no element moved except the backward stack and the Z label (−10 px) |
| B1 | remove the seeded scatter dots from the rings | FIXED: all 60 cut |
| B2 | remove the stipple caps | FIXED: the dotted crest fade m = 22..51 is cut |
| B3 | backward fraction stack at 1.5× line pitch (≥ 9 mm per fraction) | FIXED in intent, ARGUED on the literal 1.5×. Measured pitch goes from 8.2 mm to 9.5 mm (1.16×) and clear air between fractions from 0.5 / **−0.9** / 0.5 / 0.5 mm (∂K overlapped ∂V) to 3.0 mm on every gap. A literal 1.5× (12.3 mm) would put the ∂Z denominator below the drawable edge, or would need type under 1.9 mm. The stack's foot stays at v13's 15 mm |
| B4 | cut to 4 pens (MoE into black, gradients black dotted) | ARGUED (superseded): the curator lifted the pen cap after DESCRIPTION.md was written. Six pens, six meanings |
| W1 | [craft] the hero reads as two bullseyes, not one field | FIXED: same crest loci, d = 35 L and guard, but crests now reach m = 28 (was 21) and are emitted interleaved by m. The families overlap across the whole central lens and their crossings build a dark core, as in the reference |
| W2 | [craft] 6 pens / 5 swaps over house limit | ARGUED: the limit is lifted, and each swap is one clean layer |
| W3 | [concept] it is a schematic (≤ 3 under NO SCHEMATICS) | DEFERRED: inherent to the benchmark. The one-field and moire-of-queries theses answer it |
| W4 | [hierarchy] everything mid-size | PARTLY: the new dark core makes the hero the heaviest mass on the sheet. The size ratios are unchanged by thesis |
| W5 | [tension] mirror-symmetric top half | DEFERRED: v13's composition is the benchmark |
| W6 | [space] no quiet zone; lower-half dotted web | PARTLY: the halos clear every label and the node keep-outs clear every node. The web itself is the reference's |
| W7 | [depth] flat, undeclared | DECLARED FLAT: a reproduction of a flat plate diagram. The only depth cue is the far-ring dot pitch, which opens outward (3.0 / 3.7 / 4.4 mm) |
| L1 | house law: dotted projection lines, NEVER arrows | FIXED: the 8 gradient arrowheads are now terminal discs, set 2 mm off each fraction |
| L2 | house law: text on its own layer with halos | FIXED (halos), ARGUED (layer): every label clips all non-type ink out of its box +0.9 mm, using the exact `engine.geometry` Rect/Union clip. Type stays on the pen of the tensor it names, because colour is the label's meaning |

## What changed from parent

Composition moves are none, by thesis. Everything below is about how each mark is made.

1. **Stroke IR plus two sheet passes.** Every helper returns `Stroke(pts_mm, pen, kind, f)`, so the
   whole sheet exists as geometry before any G-code is written. That enables:
   - **Halos.** 20 label boxes. Non-type strokes are clipped out with exact segment/boundary
     crossings, and a dot touching a box is dropped whole. Fans no longer run through
     `Q·Kᵀ/√d_k`, droplines no longer pierce `softmax`, and ochre and black dots no longer sit
     in `router`.
   - **Node keep-outs.** 269 nodes. A dot of a dotted run that lands within 0.55 mm of an open
     circle or a disc ≥ 0.4 mm is dropped. The green BACK_COL column no longer threads the five
     coloured node circles, and the Q/K guides no longer pierce the home nodes.
2. **The carrier IS the axis.** Each packet row is now one stroke, node to node. r01 drew an axis
   line and then a carrier lying on it, which is where its 29.5 mm co-incident runs came from.
3. **Dotted runs, evenly spaced by role.** The number of dots is `round(len/pitch)`, centred at
   `(k+½)·len/n`, so there is never a stub at an end and never a dot on the node a run feeds.
   Pitch is set by role: leader 2.8 · envelope 2.9 (1.2 mm dash) · projection 3.6 · register
   guides 3.6 (0.45 dash) · far rings 3.0/3.7/4.4 (opening outward). r01 used a 0.45–0.5 mm tick
   every 2.0–2.4 mm everywhere.
4. **Envelope only where it stands off the axis** (≥ 1.3 mm). In the packet tails it ran inside
   0.8 mm of the carrier for its whole length.
5. **Hero:** m = 1..28, interleaved emission, the scatter and stipple caps cut, droplines stopped
   at the crest lens (inside it a dot sits between crest lines 1.2 mm apart, which reads as mud),
   and far rings excluded only where the solid crests actually are.
6. **Ghost experts** are drawn as one dot at each carrier crest and trough that stands ≥ 0.5 mm
   off the axis. r01 dotted a 1.3 mm wave at 1.77 mm pitch, which aliased into a jumble, and
   re-dotted the rails it overlapped.
7. **Type.** Weighted glyph strokes are one pen-down: the offset passes are chained with
   alternating direction and are never more than 0.28 mm apart. r01's 3 separate passes at
   0.46 mm drew hollow double outlines under a 0.35 nib.
8. **Dots are round and solid.** At r ≤ nib/2 + 0.08 the dot is a touch. At r ≤ nib it is one
   loop. Above that it is a spiral at 0.25 mm pitch. r01's `_dot` was a horizontal tick that read
   as a dash, and its 0.3 mm spirals left holes.
9. **Backward band.** The stack is re-spaced (B3), the arrowheads are replaced by discs (L1), and
   the purple routing skeleton is walked as 3 continuous dotted paths instead of 7 fragments.

## Measurements / computations

| | v13 (r01) | r05 v7 |
|---|---|---|
| pen cycles (strokes) | 3,471 | **1,960** |
| strokes < 1.2 mm (dots/dashes) | 2,704 | 1,179 |
| draw | 10.26 m | 9.97 m |
| travel | 11.25 m (110 %) | **9.17 m (92 %)** |
| commands | 58,991 | 48,628 |
| sustained parallel crowding (< 0.8 mm, < 25°, other stroke, runs ≥ 3 mm; r01's metric) | 2,206 mm = **21.5 %**, longest 29.5 mm | 303 mm = **3.0 %**, longest 16.8 mm |
| backward stack clear air | 0.52 / −0.90 / 0.48 / 0.49 mm | 2.95 / 3.08 / 3.08 / 3.08 mm |
| bbox (piece) | 21.6–196.3 × 14.6–280.3 | 18.1–196.2 × 15.0–280.3 (drawable 10–200 × 10–287) |
| `preview --score` | A, efficiency 0.471 | A, efficiency 0.515, readability 0.567 → 0.626 |

**Hero (unchanged physics).** A = cos(k r₁)/√r₁ + cos(k r₂)/√r₂. The drawn lines are crest loci
r_s = m·L, m = 1..28 per source. d = 250 ref px = 35 L, L = 7.14 px = 1.21 mm across and 1.41 mm
down (vertical fill stretch 1.167×). `_Guard` is 0.82 mm and 25°. The solid crests are clipped to
the r01 lens (217 × 126 px). Spoke dots have r = 1.1 + 22·|A|. Black layer draw is 4.86 m, up from
4.44, all of it the extra crests.

**Dotted budget by role** (before halos and keep-outs, which remove about 90 more):

| role | pitch / dash (mm) | path | dots |
|---|---|---|---|
| projection: Q/K fans, hero droplines, V droplines, return curves | 3.6 / 0.5 | 2.05 m | 568 |
| envelope outline | 2.9 / 1.2 | 0.77 m | 268 |
| leader: row feeds, backward runs, MoE rails, skeleton | 2.8 / 0.5 | 0.53 m | 191 |
| register guides (Q/K blocks) | 3.6 / 0.45 | 0.53 m | 146 |
| far rings (3 per source, outward) | 3.0 / 3.7 / 4.4 | 0.55 m | 144 |
| softmax ghost peaks | 1.9 / 0.42 | 0.05 m | 24 |
| **total** | | **4.48 m** | **1,341** |

## Plot budget

Model (Leo-safe profile from memory): draw F600, pen-up travel F2000, `G4 P1.0` after both M3 and
M5 (2 s per cycle), 2 min per swap. The same model gives v13 138.4 + 12 = **150 min**.

Stream order = palette index = **light → dark**, so the darkest ink always lands last and no light
nib runs through wet dark ink. The goldenrod droplines and V→gather curve are crossed later by
violet, black and coloured return curves, and the black crests and softmax go last.

| # | pen | meaning | cycles | draw | travel | min |
|---|---|---|---|---|---|---|
| 0 | goldenrod | V, its feeds, ∂L/∂V | 191 | 0.64 m | 0.94 m | 7.9 |
| 1 | dodgerblue | K, its fans, ∂L/∂K | 395 | 1.30 m | 1.64 m | 16.2 |
| 2 | forestgreen | Z = AV, ∂L/∂Z, the gradient column | 108 | 0.78 m | 0.61 m | 5.2 |
| 3 | crimson | Q, its fans, ∂L/∂Q | 397 | 1.31 m | 1.55 m | 16.2 |
| 4 | darkviolet | MoE router/experts/top-2, Y, ∂L/∂Y·experts·router | 278 | 1.08 m | 1.05 m | 11.6 |
| 5 | black | interference field, softmax, title, Q·Kᵀ/√d_k, MoE header, ∂L/∂A | 591 | 4.86 m | 3.38 m | 29.5 |
| | **total** | | **1,960** | **9.97 m** | **9.17 m** | **86.5 + 12 swap = 98.5 min** |

Pen cycles are still 65 % of the time: 1,960 × 2 s = 65 min of dwell against 17 min of drawing.
What remains is the reference's own dotted vocabulary at the widest pitch that still reads as
dotted. Suggested nib: 0.3–0.4 mm. At 0.5 mm the 1.21 mm crest pitch starts to close. Longest
stroke is 429 mm (Z carrier, 43 s), so every stroke fits inside a batch.

## Self-critique (rubric, honest)

| dimension | score | why |
|---|---|---|
| hierarchy | 5 | the dark interfering core now makes the hero the heaviest mass, but it is still ~22 % of sheet width against Q/K blocks of ~27 % |
| grid & alignment | 6 | traced rows and node columns hold; centred title and fraction are the reference's |
| tension & asymmetry | 3 | mirror-symmetric top half, kept by thesis |
| negative space | 4 | labels and nodes now breathe, but the lower half is still the reference's dotted web |
| craft for pen | 8 | crowding 21.5 → 3.0 %, halos, solid dots, fused type, no arrows, even dotted rhythm, 44 % fewer lifts; still 1,960 cycles |
| concept legibility | 3 | a labelled flow diagram; NO SCHEMATICS applies by construction |
| depth | 4 | declared flat; far-ring pitch opening outward is the only depth cue |

**Single worst thing:** it is still a schematic, the Q/K → fraction → softmax → Z → MoE → ∂L flow
the rubric fails at ≤ 3. That is the benchmark's nature. Within the thesis, the worst mark is the
lower-half web: six ochre droplines, five return curves and the purple skeleton all crossing
between softmax, Z and MoE.

## Engine requests

1. **Reversal-aware stroke ordering in `postprocess.reorder_by_color`.** It picks the nearest
   stroke *start* only and never reverses a stroke. Simulated on this gcode, nearest-neighbour
   with reversal cuts in-layer travel from 8.23 m to 6.93 m (−16 %). On v13 the cut is 10.50 m to
   8.18 m. A 2-opt pass would also take out the 1–5 cross-sheet stragglers per layer (max hop
   285 mm, in black).
2. **A 2D halo pass in `engine/kit`**, i.e. `halo_clip(strokes, label_boxes, pad)` on
   `geometry.Rect/Union/clip`. `Scene3D.halo_labels` exists only for 3D scenes, so this piece
   carries its own (`_apply_halos`, ~30 lines).
3. **A dotted-run primitive with even distribution** (n = round(len/pitch), centred dots) and
   node keep-outs. Every studio piece re-implements `_dash` with a phase that leaves stubs at the
   ends.
