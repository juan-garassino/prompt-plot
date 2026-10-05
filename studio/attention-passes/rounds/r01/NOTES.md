# ATTENTION — FORWARD AND BACKWARD · r01

Faithful recreation of `studio/attention-passes/ref/reference.png`, with the
brief's explicit licence to fix the reference's crowding.

Entry point: `attention_passes(rng, bounds, colors=3)` in `piece.py`.

---

## Render command

```
.venv/bin/python scripts/render_candidate.py studio/attention-passes/rounds/r01/piece.py \
  --fn attention_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,crimson \
  --out gallery/studio/attention_passes/current/pp_attention_passes_faithful_v12.png
```

Final render: `gallery/studio/attention_passes/current/pp_attention_passes_faithful_v12.png`
(+ `.gcode` beside it). Versions v1…v12 are all kept; nothing was overwritten.

Deterministic: two runs at seed 7 produce a byte-identical GCode body
(md5 `64567989e9548402fdf926ff15486ad3`). Seeds 3 and 11 also render in
bounds with the same bbox.

---

## Pen assignment

| pen | colour | carries |
|---|---|---|
| 0 | black | K and its gradient · the lattice · both combs · every rule, tick, cross, bead and label that is not Q's or V's |
| 1 | dodgerblue | Q and ∂L/∂Q only — the scarce pen, confined to the upper-left of each register because Q never survives past `similarity` in the forward pass |
| 2 | crimson | V and ∂L/∂V — the long horizontal in each register, and the high arc over the right half |

3 pen cycles, one per colour, in index order — no re-swaps.

## Plot budget (A3 landscape, seed 7)

| | |
|---|---|
| commands | 49 532 |
| strokes | 4 947 |
| pen cycles | 3 (black → blue → red) |
| draw | **14.90 m** — black 8.34 m / blue 1.59 m / red 4.96 m |
| travel | 20.69 m |
| bbox | 16.4 – 403.7 × 14.4 – 282.6 mm, inside the 10–410 × 10–287 drawable |
| rough time | ~14 min at F2200 draw / F3000 travel, plus 2 pen swaps |

Travel exceeds draw because roughly 60 % of the ink is DOT fields (the three
wells, the lattice, the rule beads) and every dot is its own stroke. That is
inherent to the reference's vocabulary, not slack in the path order.

## Density / paper safety

- every dot family is generated at an explicit pitch ≥ 0.80 mm:
  Q's parabola vertices 0.80, K's cone rings 1.25, V's laminae 1.45,
  the comb's ticks 1.9, the lattice 1.86 (cols) × 2.7 (rows);
- bundles pass through `enforce_line_spacing(min_dist=0.95)` **per pen**, so
  no two lines of one colour ever land inside a pen tip of each other and no
  pen thins another;
- the only deliberate multi-pass ink is the comb (one extra pass per 6 % of
  probability mass, offset 0.34 mm) and the six node squares.

---

## Row registration (the brief's hard requirement)

Measured off the built geometry:

```
Q  row y = 252.240    ∂L/∂Q y = 128.844    Δ = 123.396 mm
K  row y = 217.842    ∂L/∂K y =  94.446    Δ = 123.396 mm
V  row y = 175.800    ∂L/∂V y =  52.404    Δ = 123.396 mm
Z  row y = 209.106    ∂L/∂Z y =  85.710    Δ = 123.396 mm
```

All four twin pairs at an identical offset, all six well nodes on u = 0.165,
Z and ∂L/∂Z on u = 0.952. The left register rule carries the six row squares
so the pitch is readable straight off the margin; it is the only element
allowed to cross the gutter.

Row registration binds the WELLS, not the stages between them — so the
backward lattice and comb are squeezed to 0.80 about their own centres
(`BWD_MID`) and the wells to 0.74 (`BWD_SCALE`). That is what makes the lower
band read as the quieter echo without moving a single row.

## How Q was differentiated from K

The prior rejection of this subject was Q and K reading as twins. They are now
different in ORDER, in PROPORTION and in TOPOLOGY:

| | Q | K |
|---|---|---|
| order | **wavefront** | **field** |
| curve | confocal parabolae `r = p/(1 − cos t)` about the node | boundary of a union of discs, `F = max_i(a_i − r_i)` over 4 cusps |
| topology | OPEN arcs, never closed; vertices march left, arms open right and hand over to the bundle | CLOSED nested rings with concave merge notches, four centres |
| size | 20 × 40 mm, the flattest | 33 × 42 mm, the biggest |
| why it is true | a query is a direction: every ray leaving the focus exits parallel | a key set is a multi-modal field: several keys, one envelope |
| pitch guarantee | vertex pitch = pitch/2 = 0.80 mm exactly | |grad F| = 1, so the ring pitch is 1.25 mm everywhere by construction |

V is a third thing again — a lobed silhouette filled with horizontal laminae
at fixed 1.45 mm spacing whose dash duty is that row's value-vector norm. No
rings at all, one texture direction only.

---

## Per-round log

**r01/v1 — first build.** Measured layout in normalised (u, v), Frame mapping,
all six wells, lattice, comb, both registers.
*Failed.* Wells too small and detached from their bundles (19 mm of dead paper
between a well's edge and where its bundle started); Q and K both rendered as
dotted ovals — twins, the exact rejection this brief warns about; 52 mm of
horizontal room had to absorb 52 bundle lines, so the left third was a black
curtain; the wells overprinted their own row labels.

**v2 — restructure.** Wells moved right and enlarged onto the reference's
measured columns; bundles now start at the well's own flank with a fade-in
dotting; Q rebuilt as parabolic wavefronts; K's bundle routed into the
lattice's top edge instead of its left; red V routed under the lattice and
arcing high over the right half; halo knockout extended from bundles to wells.
*Better but:* the comb was a smudge rather than the loudest mark; the lattice
read as rows of dashes, not a grid; the fade-in made picket fences.

**v3 — weight where it belongs.** Comb given ink-passes ∝ probability, the
stray axis dots moved outside its support, tick reach up to 20.6 mm; softmax
temperature and `q*` selection made explicit; lattice squared up.
*Better but:* Q's parabolae opened the wrong way and split the well into two
wings with a void down the middle; K's outer envelope was a plain oval because
the cusps were too close for the outer levels to show any notch.

**v4 — the two real fixes.** Q's parabolae flipped to open right (vertices
march left from the focus); K's four cusps respread so even the outermost ring
shows the merge notches; the "keys enter from the top" routing abandoned — it
sent the black bundle straight through the Q well's row — and replaced with Q
owning the upper 0.56 of the lattice's left edge and K the lower 0.56. The
row/column claim moved into furniture instead: key ticks along the lattice's
top edge, query ticks down its left.

**v5 — room for the argument.** `similarity` pulled left and `softmax` pushed
right so the funnel has 26 mm to narrow in rather than 12; lattice dot radii
lifted (exponent 0.70 → 0.55) so `similarity` carries real weight; the
symmetric black "lens" on the right broken by opening the fan early (bow 0.74)
and hooking into Z late (bow 0.34).

**v6 — craft.** `_mark` rewritten from an Archimedean spiral to a chord
serpentine: the ~950 lattice dots alone were costing 50 commands each, which
is what had the plate at 64 k commands and 21 m of travel. Fade-in phase
randomised per line to kill the picket fences.

**v7 — hierarchy.** Backward stages squeezed to `BWD_MID = 0.80` about their
own centres, so the two registers stop reading as two equal bands while the
wells stay exactly registered.

**v8 — furniture.** Beads added where every fan line crosses the `weighted
values` rule, sized by the magnitude that line carries; graduated tail dots
run off the ends of the `similarity` and `weighted values` rules, matching the
comb's, so no stage axis is a bare guide line. (First pass put two of them in
the gutter and one off the sheet — now clamped per register band.)

**v10 — a real bug.** Every backward arrowhead had been pointing RIGHT for the
whole run: `_arrowhead` added a stray `+ pi` to the path tangent, and since
each backward path is built from dL/dZ on the right toward its well on the
left, that reversed it. The plate had been reading as two forward passes. One
sign removed; they now all point left, which is the brief's stated job for
these marks and the only arrowheads on the sheet.

**v11 / v12 — the comb's temperature.** 0.14 was tried and rejected: it
collapsed the distribution into two long bars on a bare spine and lost the
DENSE comb the reference is built around. 0.20 keeps ~26 ticks legible with
the top weight at 6× uniform (0.182 vs 0.029) and 8 of 34 under 0.005 — a
peak, a shoulder and a real tail.

---

## Deliberate deviations from the reference

1. **`softmax` moved from u = 0.584 to 0.618.** The narrowing between
   `similarity` and `softmax` is the plate's argument; at the reference's
   spacing it had 12 mm to happen in.
2. **Q enters the lattice's upper band and K the lower**, rather than both
   piling into the same corridor. The reference's version of this is the
   single worst mud on the sheet.
3. **24 mm of blank paper between the registers**, where the reference runs
   them together. Only the left register rule crosses it.
4. **The backward register's row pitch is the forward one exactly.** The
   reference compresses it to 95 px against 175 px, which breaks the mirror
   that is the whole point.
5. **The axis chevrons are open, the flow arrowheads are filled.** The brief
   calls the flow arrowheads the only arrowheads on the sheet; keeping the two
   axis marks as open chevrons preserves that distinction.

## What I would fix next

1. **The two almond/lens shapes** where the black fan converges into Z and
   ∂L/∂Z are the weakest formal element on the plate. They are symmetric in a
   way nothing else is, and they are the one place where a shape is doing no
   work — the density already carries the distribution, so the almond is a
   by-product of 16 beziers sharing two endpoints. Worth rebuilding as an
   asymmetric sheaf, or as a braid where the lines keep their order.
2. **Travel is 1.4× draw.** A dot-aware stroke ordering pass (sort the lattice
   and well dots into a boustrophedon rather than emitting them in generation
   order) would cut several metres without touching a single mark.
3. **The fade-in zones** (x ≈ 88–135 in each register) are still the busiest
   uncomposed area — three dotted wedges side by side. They read as the
   reference's dotted transitional band, but nothing decides where they end.
4. **The backward `similarity` lattice** at 2× subsample is close to
   disappearing. Either commit to it vanishing entirely (the gradient does not
   re-form the score matrix, it differentiates through it) or give it a
   different mark, such as ticks only.

## Engine notes

Nothing under `promptplot/` was touched. The piece uses
`engine/policies.py` (`enforce_line_spacing`, `focal_void`,
`occlude_crossings`) and `generators` (`_poly`, `_stroke_text`, `_text_width`,
`_glyph_advance`) as-is.

One engine gap worth recording, not acted on: `_mark`-style graduated dots and
`_dotted` (place dots along a polyline at a pitch) are hand-rolled here and
also exist in near-identical form in `studio/convolutions/rounds/r01/piece.py`.
They are generic enough to belong in `engine/kit.py` beside `tone_dots`.
