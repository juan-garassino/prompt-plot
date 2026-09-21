# cnn-passes — round r01

**Thesis: faithful recreation**, with the rubric's *OVERLAP IS A DECISION, NEVER A
SYMPTOM* outranking fidelity wherever the reference's own crowding would turn to mud
on paper.

Entry point: `cnn_passes(rng, bounds, colors=3)` in `piece.py`. Nothing outside this
directory was touched.

## Render command

```
.venv/bin/python scripts/render_candidate.py studio/cnn-passes/rounds/r01/piece.py \
  --fn cnn_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,crimson \
  --out ~/Downloads/pp_cnn_passes_faithful_v10.png
```

Final render: `~/Downloads/pp_cnn_passes_faithful_v10.png` (+ `.gcode` beside it).
v1…v10 are all kept; nothing was overwritten.

## Pens

| pen | colour | carries |
|---|---|---|
| 0 | `black` | structure, plane borders, all type, furniture, the neutral third of the flow |
| 1 | `dodgerblue` | the highlighted forward channel — its plane in every stack, its ribbon, its flow strands, `p₃` |
| 2 | `crimson` | the whole backward pass — gradient plane textures, the return ribbon, the flow, the true class's gradient tile |

Cream paper is the fourth colour: the ReLU mask's dead lobes, the register gutter and
the ribbon's lane are all bare paper, never decorated.

`colors=1` and `colors=2` fold by `i % colors` and still render.

## Plot budget (seed 7, A3 landscape)

| | |
|---|---|
| gcode commands | 72,766 |
| pen-down cycles | 5,944 |
| draw | 23.66 m |
| travel | 28.38 m |
| bbox | x 13.0 … 406.2 mm, y 13.5 … 283.2 mm |
| drawable | x 10 … 410, y 10 … 287 — **no bounds violation**, 3.0 mm of clear frame all round |
| pens | 3 (2 swaps) |
| pen share (drawn segments) | black 59 %, blue 21 %, crimson 19 % — the two accents stay scarce |

Verified: byte-identical output across two runs at seed 7, different output at
seed 11 (all randomness flows through the passed `SeededRNG`; nothing touches
global `random`). `colors=1` and `colors=2` render without error.

Travel exceeds draw because the flow is dotted: ~3,000 of the 5,944 pen cycles are
flow dashes. Dash periods were opened from 2.65 mm to 4.8 mm during the round, which
cut ~800 cycles without the flow ceasing to read as dotted.

## What is exact (not decorated)

One scalar field `field_f(u,v)` — three low-frequency sinusoids — plays the
pre-activation `A¹`, and **every other stage is computed from it**:

```
A¹ = f            R¹ = max(0, f)          P¹ = maxpool_2×2(R¹)
∂L/∂P¹ → unpool (one cell per 2×2 window, at the argmax)
       → ∂L/∂R¹ → × 1[f > 0] → ∂L/∂A¹
```

- **ReLU mask** `1[f>0]` covers **47.3 %** of the plane, cut by one full-width dead
  band and two corner lobes. The phases were chosen over a small search for the
  *shape* of the sign set, not for looks: the same silhouette has to be recognisable
  three columns later. It appears four times — flat/dotted in forward `R¹`, blank in
  backward `∂L/∂A¹`, blank in `∂L/∂(ReLU)`, and as the exact marching-squares iso-0
  knife drawn on each of those planes.
- **Pooling pair** shares one lattice: forward marks every live fine cell with a pin
  tick and each window's winner with a long tick; backward keeps only the long ticks.
  Same grid, a quarter of the marks. Windows the forward pass rectified away entirely
  get nothing in either plane — no gradient flows back through a dead window.
- **Spatial dims shrink, channels grow**: plane sizes 18.0 → 18.0 → 15.0 → 11.0 mm
  wide across `A¹ · R¹ · P¹ · A^L`; stack depths 6 · 4 · 4 · 5 · 7.
- **Softmax** of logits `(0.4, 1.1, 2.6, 0.9, −0.3, 0.2, 0.6)` gives
  `p = (0.062, 0.124, 0.556, 0.102, 0.031, 0.050, 0.075)` — `p₃` wins with 0.556.
  Circle radius ∝ √p, tick length = 15·p mm, so it is a normalised distribution with
  one clear winner.
- **Gradient tiles** carry `∂L/∂z = p − y` exactly: line count `1 + 4·|p−y|/max`, and
  the true class (|−0.444|) is the densest tile. Spacing is fixed at 0.9 mm and the
  *count* carries the magnitude — a density-by-spacing tile floods solid.
- **Input plates**: the backward ripple ladder is a quarter-period out of phase with
  the forward one, because the gradient of a ripple peaks where the ripple crosses
  zero. Hold the two plates side by side and the rings interleave.
- **Classifier bar** rows carry `|w|` quantised into 1–4 marks per row.

## The five crowding fixes (the licence, used)

1. **Flow passes behind.** Every strand and carrier is clipped out of the union of all
   plane parallelograms (+0.9 mm), the input plates, the classifier bars, the
   probability column, the `···` and every label halo, with `engine.geometry.clip`. In
   the reference the flow sits on top and the plane interiors go to mud.
2. **Waists are sized from the pen.** A bundle's pinch half-height is `n × 0.92 mm`,
   so a 60 mm fan closes to ~17 mm and never crosses the plotting floor. The
   reference's waists measure ~0.3 mm and go solid.
3. **Wider gaps.** Stacks are 4–7 planes at a 0.34 w step instead of ~8 at ~0.45 w,
   which buys 15–26 mm of clear paper in every inter-stage gap against the
   reference's ~11 mm.
4. **A 15 mm gutter** of bare paper between the registers, crossed only by the eight
   dotted column-registration ticks — which are the plate's thesis, stated in the one
   place nothing else is allowed into.
5. **Everything ≥ 1.05 mm pre-shear** (≥ 0.91 mm after the worst-case shear
   compression of ×0.864), and every dense family goes through
   `policies.enforce_line_spacing(0.78–0.80)`.

Occlusion is **exact polygon clipping**, not a z-buffer: each plane's texture and
border are cut out of the union of the *nearer* planes in its stack. These are convex
parallelograms, so `geometry.clip` is both exact and far cheaper than rasterising.

The one overlap that runs in FRONT is the highlighted ribbon, and it is paid for: a
`_Corridor` spatial hash cuts a 2.9 mm lane of bare paper through every texture and
border it crosses, so the plate's dominant mark is a decision and not a collision.

## Round by round

| round | worst failure found by reading the render | fix |
|---|---|---|
| v1 | ReLU gating invisible — the mask covered 66 % as one blob; `_guard` welded distant strokes into stray lines across the sheet; `softmax`/`p_K` ran off the right edge | searched the field's phases for a mask with a readable silhouette (47.3 %, one dead band); made `_guard`'s re-emit break on `M3` as well as `G0`; pulled the classifier end 20 mm left |
| v2 | forward pooling plane was the blackest mass on the sheet and read as mud; forward `R¹` was indistinguishable from `A¹`; stacks showed 30 % slivers where the reference shows ~45 % | one tick row instead of two; `R¹` gained gated lobes over a dotted zero baseline; deck step 0.30 → 0.34 |
| v3 | no dominant element at 3 m — two bands of equal weight; the highlighted channel hid behind every stack and read as four disconnected fragments | stitched the per-gap hot strands into ONE ribbon, five passes, running in front inside a lane cut by `_Corridor` |
| v4 | the ribbon was a flat highlighter bar across the sheet | the hot strand now runs from the previous stack's BLUE plane to the next one's (not the bundle's midline), and column drift went ±4 → ±7 mm, so it climbs and drops with the stage it belongs to |
| v5 | backward pooling plane had MORE ink than its forward twin — the exact opposite of what the brief asks to be visible; `softmax` glyphs collided | rebuilt both pooling planes on one shared lattice (`_pool_marks`); added uniform letter-tracking to all type |
| v6–v10 | `(more abstract spectra)` and `(linear + softmax)` touched; conv eyes landed behind nearer planes and two of six filters came out blank; pool ticks merged with the window rules | tighter tracking on the parenthesised second lines; whorl centres walk from the exposed corner on far planes to the centre on near ones; pool ticks turned vertical, across the grid; the `···` became solid 1.7 mm discs after a 1.4 mm dash disappeared into a field of 1.4 mm flow dashes |

## What I would fix next

1. **Travel (28.4 m) still exceeds draw (23.6 m).** The flow is ~3,000 separate
   dashes. A dash-aware stroke ordering — walk each strand's dashes in sequence rather
   than letting the global optimiser interleave them — would cut travel by a third and
   ~10 minutes off the plot. That belongs in `postprocess`, not here.
2. **The backward register's textures are more didactic than the reference's.**
   `∂L/∂(ReLU)` is a flat binary hatch where the reference has a flowing wave train.
   It is the right call (the brief demands visible gating) but it is the weakest
   passage as *drawing*; a gated wave whose amplitude decays toward the mask boundary
   would keep the silhouette and recover the family texture.
3. **The conv filter bank is the only stack with a staggered 2×3 layout** and it reads
   as a different species from the four decks beside it. Worth trying as a 6-deep deck
   with a wider step, or worth committing harder to the stagger on the backward twin.
4. **`softmax` sits alone in the top-right corner** with its rule pointing at nothing
   in particular. The reference has the same weakness; it could anchor to the bracket.
5. **The `···` is a hole in the flow but only three dots of ink.** It could carry the
   skipped depth (`L−2` say) the way the reference implies it.

## Shared-engine changes I wanted and did NOT make

Recorded here per the brief rather than made:

1. **`_GLYPHS` is missing `[`, `]`, `>` and `−` (U+2212).** All four are silently
   dropped with a warning, so `1[A¹ > 0]` and `p − y` degrade to `1 A¹ 0` and `p y`.
   I drew the three brackets locally in `_mark()` in the same 4×6 metric and
   substituted a hyphen for the minus. `Σ` and `}` are also missing (drawn locally as
   `_big_sigma` / `_brace`). The `convolutions` round hit the same wall with `σ` and
   `·` and recorded it too — five rounds have now each re-drawn the same glyphs.
2. **`kit` has no tracked-type helper.** The proportional metrics set lowercase side
   bearings tight enough that `softmax` and `non-linearity` collide glyph-to-glyph at
   caption size. `_lay()` here adds a uniform `0.17 × cap` tracking; this is the third
   piece to hand-roll it (`convolutions` has `_tracked`) and it belongs in `kit`
   beside `type_block`.
3. **`policies.enforce_line_spacing` can drop the `G0` that positions a stroke.** Its
   own docstring warns about this, and every caller re-emits from parsed runs to work
   around it. Two rounds have now written that same parser, and both first wrote it
   keyed on `G0` alone — which welds two distant strokes together and lays a stray
   line across the whole sheet. The policy should return well-formed strokes.
4. **There is no polyline-corridor Region.** `geometry.Region` is exactly right for a
   plane and exactly wrong for a 300 mm polyline (a Union of 450 rectangles is 1,800
   half-plane tests per segment). `_Corridor` here is a 25-line spatial hash used
   through `kit._clip_runs`; a `Corridor(Region)` with real `inside_intervals` would
   let it compose with the rest of the region algebra.
