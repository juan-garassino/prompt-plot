# r03 — SOFTMAX IS A VANISHING POINT

**Thesis: abstract order, not a recreation of the reference.**

One sentence: *the plate is a pencil of lines through a single point — the raw
scores are a long rail, softmax is the vanishing point that cuts that rail down
to one, and the gradient is the same rays continued out the far side of the
apex.*

Final render: `gallery/studio/attention_passes/current/pp_attention_passes_abstract_v9.png`
(+ `.gcode` beside it, with the provenance header).

---

## The order, and why it carries the mechanism

The rubric's question is *what ORDER is this?* Not a plot, not an object. The
answer here is **projective**: one operation — *a rail cut by a pencil of
concurrent lines* — and every stage of attention is an instance of it.

| stage | the geometry | what carries the number |
|---|---|---|
| similarity | a **plane collapses onto a line**: the key cloud dropped perpendicular onto the q axis | the foot position is `s = q·kⱼ`; the perpendicular's *length* is the component the dot product destroys |
| exp | each foot opens a **cell** on the raw rail | cell width = `exp(sⱼ)`; the rail's total (`Σexp = 33.26`) is arbitrary, and the plate says so |
| **softmax** | **a pencil of 13 concurrent rays through one apex** cuts the 336 mm raw rail down to a 125 mm unit bar | the ray positions ARE the ratios; the total is forced to exactly 1 |
| merge | the unit bar's cells carry `v` as **height**, so each cell's **area** is `aⱼvⱼ` | the heavy crimson rule is `z = Σaⱼvⱼ`: the crimson standing above it has exactly the area of the paper left under it |
| **backward** | **the same rays, continued past the apex** | same ratios, order reversed (point inversion), flat top instead of a skyline, because every value gets *one* number split by *the same widths*: `∂L/∂vⱼ = aⱼ·∂L/∂z` |

**Why this is the right order.** Normalisation is projection. A pencil of
concurrent lines cuts any two parallel transversals in *identical ratios* —
that is the intercept theorem, and it is literally what softmax does to a set
of magnitudes: it throws away the total and keeps only the ratios. So the
drawing does not *illustrate* softmax; it *performs* it. The cell boundaries on
the unit bar are not drawn from the computed `aⱼ` — they are where the rays
land, and they come out equal to `aⱼ` because the geometry is the arithmetic.

**The mirror is structural, not a second register.** The reference stacks a
forward register over a mirrored backward one, with the wells drawn twice. Here
there is exactly ONE set of rays on the sheet and the backward pass is the part
of them that lies beyond the apex. You cannot make a stronger statement of "the
gradient reuses the same weights" than "it is the same lines." The order
reverses automatically (that is what a point inversion does), and the two
crimson masses state the asymmetry that matters: forward is a **jagged skyline**
(content, `vⱼ`, all different), backward is **flat-topped** (one number,
`∂L/∂z`, split by the same widths).

**And the twist.** The viewer already owns a pencil of lines through a point:
it is a **vanishing point**. Softmax is the vanishing point of attention — every
score, however large, vanishes into one — and what lies behind a vanishing point
is the mirrored world, which is where the gradient lives. The headline states
the joke, the geometry is the punchline. The apex itself is left **unpainted**
(a 4 mm hole, every ray stopping short of it): a vanishing point is not a place.

**Q, K, V differ in kind, not colour.** This was the explicit rejection reason
for a prior version, so it is the constraint I designed around first:

- **q** — ONE oriented line, unbounded, cropping at both edges of the sheet.
  It has no magnitude and no origin; its graduated tick ladder gives it a
  *sense* only. It is also the axis of the whole image (see style, below).
- **k** — a SCATTER of positions: open rings, no magnitude, each with a
  perpendicular. Nothing about a key is a quantity until it meets q.
- **v** — a field of AREAS. Content with magnitude and no position.

Line / points / areas. They cannot read as twins.

---

## Style canon

**Swiss / International Typographic**, with one declared hybrid move.

- Strict flush-left type on a single left module (x = 26 mm) for the rule,
  kicker, four-line headline and data block. Type at display scale (14 mm caps,
  0.8 mm weight — type as mass, not caption).
- Brutal asymmetry: all mass on the right half, a shaped triangular void in the
  lower left whose hypotenuse is the leftmost ray of the pencil.
- Extreme scale contrast: a 336 mm rail against a 4 mm hole.
- Zero ornament — two registration crosses, nothing else. No boxes, no arrows
  except the three backward chevrons.
- Palette `black · dodgerblue · crimson`, blue kept scarce (one line and its
  ladder) so it stays loud.

**The declared hybrid:** the *image* is raked 4.5° off the type grid, because
**q sets the axis of everything**. The query direction is arbitrary and the
construction has to live in it; the type does not, and stays orthogonal. The
tension between the two grids is the plate's only unease device, and it is
carrying a fact.

**Depth is not claimed flat.** Swiss is a flat canon, but this plate has the
oldest depth cue there is: a pencil converging on a vanishing point, reinforced
by line weight falling off from the traced winner (3 passes) to the tail
(1 pass). That is a conscious exception to the canon and it is here because the
mechanism supplies it for free.

---

## What I deliberately avoided

Read first, then ruled out:

| prior attempt | its move | avoided how |
|---|---|---|
| `bauhaus_relevance` / `studio/attention-dag` / `gallery/.../attention_dag`,`attention_axo*` | exploded axonometric stack of planes, droplines, numbered stage labels flush left | no axonometry, no stacked planes, no numbered stages, no droplines |
| `studio/resonance*`, `res_backprop` | rows of wavepackets, dotted flow arcs, interference rings, a forward register over a mirrored backward one | no wavepackets, no dotted arcs, and the mirror is one figure seen through a point rather than two registers |
| `attention_arcs` / `attention_matrix` | chords weighted by ink passes; the L×H grid of head matrices | no chords, no matrix grid |
| `bauhaus_attention` | radial sink-chord fan from one disc | the fan here converges on a *hole*, is projective rather than radial, and is not centred |
| the reference plate itself | left-to-right flow, three labelled vertical rules, three lobed dot-field wells, top/bottom registers | no flow band, no labelled vertical rules, no dotted wells, no duplicated sources |

---

## Render

```
.venv/bin/python scripts/render_candidate.py \
  studio/attention-passes/rounds/r03/piece.py \
  --fn attention_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,crimson \
  --out gallery/studio/attention_passes/current/pp_attention_passes_abstract_v9.png
```

**Paper: A3 landscape.** The order demands it. The raw rail has to be long
enough that a 2.68× crush still leaves a unit bar with twelve readable cells,
and the pencil needs horizontal room to open into a real fan rather than a
sheaf of near-parallel hairlines (that failure is visible in v1/v2). Portrait
would have forced either a short rail or an unreadable tail.

**Pens (3):**

| idx | pen | carries |
|---|---|---|
| 0 | black | the q-axis keys, all structure, the pencil, the rails, all type |
| 1 | dodgerblue | **q only** — one line and its ladder. Scarce and loud. |
| 2 | crimson | **v** — the unit bar's mass, the output level `z`, the gradient mass and `∂L/∂z` |

Cream stock is the fourth colour (the void, and the deficit notches under the
`z` rule, which are *paper doing work*).

## Plot budget (measured from the emitted GCode)

- draw **23 038 mm**, travel **14 464 mm**, **661** pen lifts, 6 317 commands
- G1 bbox `x 24.3–400.3, y 10.6–286.2` — inside the A3 drawable area
  (10–410 / 10–287), verified, no clamping
- ~**40 min** at F1800/F3000; ~**68 min** at Leo's F600 draw feed, and the
  1 s pen dwells add ~20 min on top of that — call it **1 h 20** on Leo
- minimum feature: **1.28 mm** as drawn. Unit-bar cells run
  39.6 / 28.9 / 16.5 / 14.0 / 8.1 / 5.9 / 4.5 / 2.6 / 2.2 / 1.3 / 1.0 / 0.7 mm —
  the last two fall under the pen tip (0.013 of the mass) and are **merged into
  one 1.68 mm step at their weighted-mean v** rather than drawn as a 0.7 mm
  zigzag the plotter cannot tell the truth about
- fills: 0.86 mm (unit bar, grain along the rails) / 0.72 mm (gradient mass,
  grain across them) — the two grains are the forward/backward convention
- 3 pen swaps. Trace the frame before plotting; stream per colour layer.

## Overlaps (all chosen, per "overlap is a decision")

1. The rays cross the crimson masses — that is how the cells are *divided*.
   The fill is inset 0.5 mm from every cell boundary so each ray crosses bare
   paper, not ink on ink.
2. The leftmost ray passes ~8 mm above the headline's cap line. A deliberate
   near-miss: it is the edge of the void, and the type is tucked under it.
3. The `z` rule over-runs the unit bar by 15 mm left and 9 mm right so it reads
   as a *level*, not as part of the bar.
4. Rays past the apex crop at the design box (Liang–Barsky). The backward fan
   runs off the sheet on purpose — the gradient does not stop at the frame.

---

## Per-round log

**v1** — first geometry: wedge-per-key exponential shear + pencil + unit bar
with per-cell blocks. *Failed.* Cumulative-exp boundaries crushed into the left
10 % of the raw rail, so the "fan" became one black triangle and the pencil's
rays degenerated into a sheaf of near-parallel hairlines.

**v2** — flipped q to point left so the raw rail runs wide→narrow with its
crowded end *under* the apex (a vanishing point turns crowding into angular
spread, not a smear); N=12, score scale widened. The pencil read as a fan for
the first time. Remaining: the 24-line shear band was mud; the crimson merge was
a small chart lost among the rays; chevrons pointed the wrong way.

**v3** — raw rail pushed to h=56 and the shear cut to ONE connector per key;
outer rays weighted as the funnel walls; unit bar lengthened to 150 mm. Merge
still illegible — and I found the bug: the deficit hatch was called with
`h0 > h1` and silently returned nothing, so half the merge had never drawn.

**v4** — the deficit device replaced entirely: one continuous stepped crimson
silhouette, solid fill under it, cut by a heavy `z` rule, so the balance reads
as *crimson above the line = paper below it*. Also found the bbox blow-out:
shallow rays continued past the apex reach t≈430, dragging the fit scale to
0.82. Bounded the gradient rail's length.

**v5** — Liang–Barsky clip so rays crop at the design box by intent; values
re-assigned so the mass sits where the width is; fit back to ~1.0. The plate
became legible at 3 m.

**v6/v7** — apex moved to t=268 to pull the backward mass out of the corner;
annotation moved off the geometry into two small flush stacks at the left edge;
headline up to 16 mm; connectors dropped to 1 pass so the rail, not the
plumbing, owns that zone.

**v8/v9** — sub-tip cells merged into one honest step (the right end of the bar
had been a 0.7 mm crimson zigzag); headline broken to four short lines and the
kicker shortened to `forward and backward`, which cleared its collision with
the crimson bar and with the leftmost ray; key field tightened, score spread
widened to keep the softmax visibly peaked (`a max = 0.316`).

---

## Honest critique — the weakest part

**The key field.** Twelve ring-on-a-stick marks in a row across the top third.
It states the projection correctly — the feet all land on one line, the pole
length is the discarded component, the pole weight is the key's final share —
but it is the least *designed* zone on the sheet, it reads as a picket fence at
3 m, and it is the one passage that still looks like technical drawing rather
than composition. A rework should give the cloud a real second dimension (keys
on both sides of q, or a genuinely clustered scatter) so the collapse onto the
line is a collapse of *shape*, not of a comb.

Second: the upper-right ~150 mm of the q axis crosses blank paper. I defend it
as "a direction is unbounded and runs off the sheet", and it is the plate's
quiet zone, but it is a defence rather than a design.

Third: the right end of the unit bar (1.3–2 mm cells, rays crossing them at a
shallow angle) will be a busy 20 mm on paper. It is the honest consequence of
the exponential and the merged-tail step makes it survivable, but it is the
only passage I am not sure of until it is plotted.

## Robustness

Deterministic (identical commands for the same seed) and in-bounds at seeds
7 / 3 / 11 / 21 — G1 bbox stays inside `10–410 / 10–287` at all of them, no
clamping. `G_draw` is clamped to `[0.22, 0.62]` so a seed whose `z` drifts
cannot push the backward rail off the sheet; a clamp logs a warning and does
not fire at seed 7 (`∂L/∂z = 0.457`).

## Request to the shared engine (not made — r03 touched nothing under `promptplot/`)

`engine/kit.py` has no oriented-frame fill: `fill_rect` is axis-aligned only,
so this piece carries its own `_hatch_th` (serpentine in a rotated (t,h) frame,
with a grain switch) and `_clip` (Liang–Barsky segment clip to a box). Both are
general and would be at home in `engine/kit.py` as `fill_rect_oriented(...,
angle=, grain=)` and `clip_segment(...)` — several pieces hand-roll the second
one already. Left alone here by instruction.
