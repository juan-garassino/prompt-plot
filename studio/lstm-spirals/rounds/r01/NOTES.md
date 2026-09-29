# lstm-spirals — r01

Recreation of `studio/lstm-spirals/ref/reference.png` with one correction:
**both spiral centres sit exactly on the central vertical axis.**

- Piece: `piece.py`, `lstm_spirals(rng, bounds, colors=2)` — nothing under `promptplot/` was modified.
- Final render: `gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png` (+ `.gcode`). Ten renders, six real iteration rounds.
- Command:
  ```
  .venv/bin/python scripts/render_candidate.py studio/lstm-spirals/rounds/r01/piece.py \
    --fn lstm_spirals --seed 7 --colors 2 --paper a4 --orientation portrait \
    --palette black,crimson --out gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png
  ```

## The field that was integrated

Not parametric spirals. Two **spiral sinks** (a point sink + a point vortex, both
with 1/r falloff) on the axis, integrated with RK4 on the *normalised* field so
samples land at constant arc length:

```
v(p) = Σ_k ( -m·d_k + g·rot90(d_k) ) / (|d_k|² + s²)      d_k = p − P_k
P_hidden = (cx, y0+0.662H)   P_cell = (cx, y0+0.367H)   m = 1.0, g = 3.0, s² = 4
```

A single centre gives an exact logarithmic spiral with pitch set by `g/m` — the
reference's spiral geometry falls out for free. Two of them, with **equal
strength and equal circulation**, make the radial parts cancel and the vortex
parts cancel at the midpoint, so there is a genuine **stagnation point exactly
halfway between them, on the axis**. That is the saddle where the two systems
interleave; every bend in every line near the middle of the sheet is the other
system pulling, which is what the reference's curves actually show and what a
parametric spiral cannot produce.

A third term was needed and is physically the right one: **an x_t injection
drift**, `+U·exp(−(x−x0)/L)·x̂` with `U = 0.115`, `L = 25 mm`. The left margin
sits on the two sinks' symmetry line, where the radial parts cancel and the flow
is purely *vertical* — without the drift the INPUT SEQUENCE streamlines slid
straight down the edge instead of feeding the cell. The drift is ~3% of the
local field at the centres, so both spirals and the saddle stay on the axis.

Crowd control is the engine's, not hand-rolled: one `Scene3D.occupancy(0.95)`
shared by every family, `scene.lines(..., mode="pause_resume")`. The same
`Occupancy` is queried (non-mutating) immediately before each `lines()` call so
arrowheads only land on stretches the engine will actually keep. Solid families
are emitted **first** so they get first claim and stay long; dotted gate /
information families fill what is left. Ordering matters a lot — in round 1 the
dotted families went first and chopped every solid sweep into confetti.

## What the axis-centred correction changed

It improved it, and it changed more than the two dots:

- The axis is now a real spine. INPUT → red cell-state core → saddle → black
  hidden-state core → OUTPUT is one straight read up the sheet, and the saddle
  lands *on* the line rather than beside it. In the reference the axis is a rule
  laid over two vortices that lean left; here it is the structure.
- Because the two centres are colinear and equal, the whole field is symmetric
  under a 180° rotation about the saddle. The two lobes are exact rotations of
  each other. That is coherent and it reads as inevitable — but it is *more
  diagrammatic and less hand-composed* than the reference, which gets tension
  from the black lobe being bigger and both lobes leaning off-axis.
- The lobes now stack vertically instead of leaning left, so the **left third of
  the sheet is emptier than the reference's**. The gate labels and the INPUT
  SEQUENCE block sit in more white than they do in the original. Widening the
  seed rings to r = 64 mm recovered some of it; it does not fully close.

Net: the correction is right, and I would keep it. The cost is real but small.

## Honest list of differences from the reference

1. **Symmetry.** Reference: black lobe visibly larger than red, both off-axis,
   plus two extra off-axis convergence nodes (mid-left and lower-right) that
   imply more than two singularities. Here there is exactly one stagnation
   point, on the axis, and the two lobes are congruent. Direct consequence of
   the correction; not fixable without reintroducing asymmetry.
2. **The dotted t-rings do not read as strongly.** They are drawn as eccentric
   orbits (ry = 0.78·rx, radii 30/41/52/63 mm, split into in-rect runs before
   dashing so they never draw a chord) but the dense streamline field swallows
   them except where it opens up. In the reference they are cleaner. Giving them
   priority on the occupancy grid would fix it but would chop the streamlines.
3. **Type has no serifs and no italic.** The reference sets the maths in an
   italic serif; this is a single-stroke sans. Subscripts, mixed case and
   tracking now match (`c_t`, `c_{t-1}`, `hidden state h_t`, `t = 1 … t = T`).
4. **Two characters are missing from `_GLYPHS`** and are drawn as geometry in
   `_rich()`, not as a local glyph table — **`⊙` U+2299** (drawn as a small
   circle plus a centre mark) and the **combining tilde** for `c̃` (drawn as a
   short wave over the preceding glyph). Worth adding centrally.
5. Arrowhead handedness: both fields run counter-clockwise inward. The
   reference's own arrows are mutually inconsistent (its top-of-lobe arrows read
   CCW, its far-left arrows read CW), so a single coherent circulation was
   chosen over copying them.
6. The reference's dotted "gate interaction" family sits as a clearly separate
   visual layer; here it blends into the solid families more than it should.
7. Filled dots are a small ring plus a centre stroke (the kit has no filled
   disc at this scale); they read filled at pen width, not in the preview.

## Plot metrics (seed 7, A4 portrait, 2 pens)

| | |
|---|---|
| draw | 12 662 mm (black 8 134 · red 4 528) |
| travel | 10 908 mm |
| pen cycles (M3) | 1 738 |
| strokes | 947 (151 longer than 6 mm) |
| commands | 24 376 |
| out-of-bounds | 0 (the one flagged point is `merge_chunks`' home `G0 0 0`) |

**Line spacing.** Sampling every field/ring stroke at 0.4 mm: 3.07 % of points
lie within 0.8 mm of another stroke, but 2.99 % of those are **crossings**
(local tangents more than ~20° apart — unavoidable, and present in the
reference). Points that are both closer than 0.8 mm **and near-parallel** —
the real "merges into a black patch" failure — are **0.08 %**, min separation
inside that set 0.025 mm at isolated crossing-adjacent samples. The occupancy
grid at 0.95 mm is doing its job.

Deterministic: same seed → byte-identical command list. Degrades correctly to
`colors=1` (single pen).
