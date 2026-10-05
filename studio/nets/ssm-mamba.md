# SSM / MAMBA — SELECTIVE STATE, THE SCAN
**Essence:** the memory horizon is a *function of the input*. A selective SSM has
no fixed context: its discretisation step `dt` is read off the token, so the
model's internal clock races on novel tokens and stands still on predictable
ones — the horizon recedes, then is guillotined. **Status:** r01 built
(`studio/ssm-mamba/rounds/r01/piece.py`, `receding_horizon`).

## The idea
A continuous-time linear system `h'(t) = A h(t) + B x(t)`, zero-order-hold
discretised into a scan. In S4 the step is constant, so the piece would be a
helix sliced at regular intervals. In **Mamba/S6, `dt`, `B` and `C` are
input-dependent**, and that is the only thing worth drawing: the slicing is
*irregular by design*, and the per-step decay `exp(-a_n dt_t)` makes the memory
horizon stretch and contract along the sequence.

The exact quantity the piece is built on: with `S_t = sum_(r<=t) dt_r` (the
model's own clock),

    retention(t <- s) = exp(-a_n (S_t - S_s))
    H_n(t) = max{ l : a_n (S_t - S_(t-l)) <= 1 }        the e^-1 horizon, in TOKENS

`H(t)` is a **sawtooth**: it grows exactly one token per token (memory receding)
and collapses to zero at any step where `a dt_t >= 1` (one token erases a whole
time constant). That sawtooth IS selectivity, and it is computed, not drawn.

## Pen-plotter visual (our engine) — as built
Two plates on **one shared axonometric basis** (the lower plate is a pure `-wy`
drop from the upper, so corresponding corners stay in register):

1. **THE SCAN** (dominant) — a long isometric corridor: the state `h_tn` over
   (time x channel), hidden-line `Scene3D.surface()`, cropped at BOTH frame
   edges because a sequence model has no first and no last token. The timescales
   `a_n` are log-spaced, so the grain ramps across the channel axis: slow swells
   at the back, token-scale chatter at the front. **Red transverse seams** at the
   tokens where the selector fires — the state is wiped and rebuilt.
2. **THE HORIZON** (second read) — a hatched cast shadow below it. One tooth per
   token, its length exactly `H(t)` in tokens, laid on the **same world pitch as
   the time axis**, so the horizon can be read off by eye against the token
   pitch. Red envelope = the receding silhouette, broken at every guillotine.
   A thin inner stub curve = the fastest channel's horizon (1–2 tokens).
3. **THE CLOCK RULE** — the shadow's near edge carries one tick per unit of
   internal time `S`. Ticks are far apart where the model idles and bunch into a
   burst where `dt` fires: the warped clock, drawn as a ruler.

Dotted projection lines (never arrows) drop each selection seam onto the pinch
it causes, and drop the corridor's world corners onto the floor plate.

## Deliberate departures from the first draft of this brief
- The brief asked for slicing planes **at regular intervals**. That is S4, not
  Mamba. The slices here are placed by the selector and are therefore irregular
  — the whole point.
- The brief asked for the sliced helix to project onto "a lower grid = discrete
  outputs". A grid of outputs is a schematic (DESIGN_RUBRIC §6). The lower plate
  instead carries the *memory horizon*, which is the phenomenon the
  discretisation actually produces.
- A helix/ribbon was rejected: an LSTM piece already owns the ribbon idiom
  (`bauhaus_conveyor`, THE LONG NOW — a flat 2D band whose thickness is |c_t|).
  This piece is 3D, has a channel axis (multi-timescale, which an LSTM cell
  state does not have), and its subject is the horizon, not the carry.

## Palette
black = the state surface, the shadow teeth, the clock rule, type;
red (crimson) = selection — the seams, the last long tooth before each cut, the
receding envelope; third pen (green) = the single longest reach, traced back
along time, cross-grain against the teeth. Cream paper is the fourth colour.

## Annotations
`h_t = exp(-a dt_t) h_(t-1) + B_t x_t`, `SELECTION . DT FIRES`,
`LAG . TOKENS BACK . SAME PITCH AS TIME`, `ONE TICK PER UNIT OF S`,
`DT T . THE LEARNED STEP` (stem chart, in x-register with the corridor).

## Reference prompt
Mechanical pen plotter, warm cream paper. A long isometric wireframe corridor of
state runs from upper-left to lower-right and is cut off by both edges of the
sheet; its surface is smooth swells at the far edge and fine chatter at the near
edge; thin red lines cut straight across it at irregular intervals. Beneath it,
on the same axonometric grid, a hatched shadow of parallel ruled teeth whose
lengths form a sawtooth — long diagonal ramps ending in vertical cliffs — with a
red line along the tooth tips. Fine dotted vertical projection lines connect the
red cuts above to the cliffs below. 0.3 mm black, 0.1 mm red. Zero gradients or
fills; tone only from line density.

## Build notes
`Scene3D` declaration only: one `surface()` (native `ScreenThin` anti-crowding,
`far_mult` fading the past), `lines(mode="over")` for the selection seams and the
front silhouette, `poly()` for the shadow/rule/ticks, `halo_labels()` for type,
`occupancy()` to keep the tick burst plottable, and `engine.geometry.clip` +
`Rect` for the exact frame crop (`fit="none"` — a rescue fit would undo the
crop). No z-buffer or thinning is hand-rolled in the piece.

Pairs with Flow Matching (both continuous-dynamics pieces) and stands opposite
`bauhaus_conveyor` (LSTM) in the memory family.
