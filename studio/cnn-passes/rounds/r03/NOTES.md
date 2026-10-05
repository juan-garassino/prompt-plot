# cnn-passes r03 — THE MIRROR FORGETS

> ## STATUS: **v10 IS APPROVED.** Juan reviewed it and said "i love this one!".
> **The approved source is `studio/cnn-passes/rounds/r03/piece_v10_APPROVED.py`
> — frozen, never to be edited.** The approved render is
> `gallery/studio/cnn_passes/current/pp_cnn_passes_abstract_v10.png` with its `.gcode` beside it.
>
> `piece.py` in this folder is byte-for-byte the same source as of the freeze
> and is the file any future round would branch FROM — but the file of record
> is `piece_v10_APPROVED.py`.
>
> Verified by re-rendering the frozen source to
> `gallery/studio/cnn_passes/trials/pp_cnn_passes_abstract_v10_verify.png`:
> **drawing 17011.13 mm · travel 19825.54 mm · 36825 commands**, all three
> matching the approved render, and the two GCode bodies are byte-identical.
>
> Nothing in the "honest critique" section below has been folded into the
> approved file. Those are proposals for a v11+ rendered from a separate copy;
> Juan decides.

**This round does not recreate the reference.** r01 and r02 own that. The
reference is a left-to-right pipeline of stacked parallelogram planes, forward
on top and backward below. This round keeps what it is *about* — the
forward/backward mirror, the constriction of spatial detail into a class
probability, the gating and the scattering — and transposes it into a different
abstract order, per DESIGN_RUBRIC "TRANSPOSE TO AN ABSTRACT ORDER".

---

## The abstract order, in one sentence

> **NESTED ANNULI: a polar lattice that trades angular resolution for radial
> resolution turn by turn, where each band's outer half is the forward pass and
> its inner half is the gradient — so a stage and its twin share a RADIUS the
> way the reference's twins share a column.**

The forward pass runs inward and terminates as one number at the centre. The
gradient is born there and climbs back out through the same lattice, along the
same angles, into fewer of the same cells.

## Why this order carries the mechanism

The order was not chosen for looks. Every property of the geometry is a
property of the network, and the mappings are exact:

| geometry | mechanism |
|---|---|
| angular cell count of a band | spatial resolution — **halves** at every pool (256 · 256 · 128 · 128 · 64) |
| radial sub-rings of a band | channel count — **doubles** at every conv (3 · 6 · 6 · 12 · 12) |
| radius | depth. The collapse is literal: 256×3 cells at the rim, one scalar at the centre |
| arc duty inside a cell | \|activation\|. Spacing is fixed at the cell grid; **tone drives duty, never spacing** (rubric dim 5) |
| **blank paper** | relu closed — the negative lobes of that stage's angular response |
| the same blank angle on both halves of a band | the chain rule: ∂relu is the indicator of the forward mask, so the void has one address for both directions |
| crimson broken where black is continuous | max-unpool: one cell per window receives gradient, the rest get nothing |
| sector angle in the core | softmax probability. Normalisation is literally the circle **closing** |
| tick direction on the crown | sign of ∂L/∂z = p − y; outward positive, inward negative |

Two structural choices are worth naming:

- **The wide blank wedges line up radially across every band, and that
  alignment is not a layout decision — it is the low-pass.** Every stage shares
  one set of Fourier coefficients and keeps only its first *M* of them, where
  *M* scales with its cell count. That is what pooling physically is. The
  coarse structure therefore survives every stage and the fine structure does
  not, so the big voids run rim-to-core while the fine texture only exists at
  the rim. The plate's largest quiet zone is a gate decision, not leftover
  space.
- **The input band is ungated** (there is no relu on an image), so it is the
  only continuous ring family on the sheet and the densest texture — the raw
  photograph, bounding the voids that open inside it.

## The twist

A CNN's backward pass looks like its forward pass reflected. It isn't: pooling
throws away three cells in four and cannot say which, so the return trip can
only re-enter the cells the outbound happened to remember. **The mirror
forgets.** The plate is one collapse and its echo on one set of rings, and the
punchline is measured and printed on the sheet, not asserted:

- `paper the gate leaves blank — 52 %`
- `of what fired, the gradient re-enters — 47 %`
- `the corridor: out 117 mm, back 38 mm, 32 % (median angle)`

## Style canon: SWISS / INTERNATIONAL TYPOGRAPHIC (STYLES.md #3)

Committed to, not sprinkled on:

- **A documented modular grid**: 10 columns × 7 rows, 4 mm gutter, over a frame
  inset 4 mm inside the drawable area. The huge element's centre sits on the
  left edge of column 7.5 and the top line of row 4.5. The type column, the
  rules and the tables all snap to it.
- **Extreme scale contrast**: one 277 mm disc against 2.3 mm caption type, and
  a 13.4 mm headline with 1.2 mm of real stroke weight (`giant_type`) so it
  reads as mass, not as a caption.
- **Brutal asymmetry and crop**: the disc is cropped decisively at the right
  (~41 mm) and the bottom (~42 mm), clear at the top (28 mm band) and left
  (165 mm column). Nothing is centred.
- **Radical negative space**: the crescent between the orthogonal type column
  and the polar mass is a composed void — the only things allowed into it are
  the two orientation marks and the corridor's name.
- **Zero ornament**: there is no swatch bar, no corner plus-marks, no
  registration crosses. Every mark carries a number.
- **Flatness is DECLARED** (dimension 7). Swiss is a flat canon, and here the
  radius is the depth axis — it carries the entire argument — so a
  picture-plane depth cue would compete with the one thing the plate is about.
  The single depth device is occlusion where the corridor passes over the
  lattice, and that is solved analytically.

## Overlap is a decision (dimension 4)

There is exactly one overlap on the sheet: **the corridor**, one sixteenth of
the field, cut rim-to-core through all ten sub-bands. Every ring it crosses is
given a 1.15 mm gap at each of its two edges, and the gap is computed from the
corridor's own angles rather than sampled — so the corridor reads as laid *on*
the lattice. Its two edges are the two passes:

- the counter-clockwise edge runs IN — blue, whole, chevron at the core;
- the clockwise edge runs OUT — crimson, one run from the core that **stops at
  the first cell with no gradient**, chevron there, and a hairline tie across
  the corridor marking the radius where it ran out.

The corridor's angle is **chosen, not picked**: of all 256 angular cells in the
searchable arc, it sits at the one whose return is the *median*. Placed by eye
in an earlier round it reported a 100 % return — honest arithmetic saying the
opposite of what the plate argues.

Everything else keeps a sized gap: 1.15 mm between a band's forward and
backward halves, 6.0 mm between bands. That 5:1 ratio is load-bearing — at
near-parity (an earlier round used 1.7 / 3.2) the ten sub-bands read as ten
unrelated rings instead of five objects each with a black half and a crimson
half, and the mirror disappeared.

---

## Render command

```
.venv/bin/python scripts/render_candidate.py \
  studio/cnn-passes/rounds/r03/piece_v10_APPROVED.py \
  --fn cnn_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,crimson \
  --out gallery/studio/cnn_passes/current/pp_cnn_passes_abstract_v10.png
```

**Paper: A3 landscape**, as specified. The landscape format is what the order
needs: a radial collapse wants one square-ish mass, and landscape leaves a
165 mm column beside it for the flush-left Swiss type without shrinking the
disc. Portrait would either shrink the lattice below its plotting floor or push
the type under the disc, where it would stop sharing an axis with it.

## Pen assignment

| pen | colour | role | draw | strokes | share |
|---|---|---|---|---|---|
| 0 | black | the forward lattice, the corridor's rungs, all structure and type | 13 056 mm | 3 037 | 76.8 % |
| 1 | dodgerblue | the ONE tracked channel, the class it elects, the outbound edge | 1 964 mm | 202 | 11.5 % |
| 2 | crimson | the entire backward pass | 1 991 mm | 1 026 | 11.7 % |

Cream paper is the fourth colour and it is what does the gating. Blue is kept
scarce by construction: the tracked channel is inked only where it fires above
its own 74th percentile, and there is no blue at all on the input band, because
there is no "feature" yet.

## Plot budget

- **17 011 mm drawn**, 19 796 mm travel, **4 266 strokes**, 36 825 commands.
- **3 pens**, so 3 swaps (rubric allows ≤ 3–4).
- Ring pitch **1.02 mm**, above the 0.85 mm floor and the rubric's 0.8 mm.
  Computed from the radial budget at build time and clamped, so it can never
  go under the floor if the stage list changes.
- Estimated draw time ≈ **8 min at F2200**, plus travel and 2 pen swaps.
- **Inked extent X 15.1 – 406.0, Y 14.0 – 281.0** inside a drawable area of
  10–410 / 10–287. Zero bounds violations: everything is clipped exactly at the
  frame (`kit._clip_runs`), never clamped — clamping folds a stroke onto the
  margin and draws a false straight edge, which is what v1 did.
- **Determinism verified**: two runs at seed 7 produce byte-identical GCode.
  All randomness flows through the passed `SeededRNG`.

---

## Round log

**v1** — first build. Three real failures. (a) Consecutive live cells were
welded to full width, so the duty encoding only affected run *ends* and
magnitude was invisible. (b) Six leader lines fanned from different band radii
to a stacked rail and crossed each other in an X over the caption block:
collision, not composition. (c) 25 bounds violations — strokes were being
*clamped* onto the margin, drawing a false straight edge down the right side.

**v2** — welding restricted to duty ≥ 0.965; forward duty moved into
0.60–1.00 and backward into 0.20–0.62, so forward reads continuous and backward
always reads broken. All leaders deleted. GAP_FB / GAP_BAND separated to 1.15 /
6.0 so a band reads as one object. Exact frame clipping. The crimson stopped
competing with black.

**v3** — blue restricted to where the tracked channel actually fires; crimson
given a magnitude floor so it thins instead of felting; every type line cut to
fit the 118 mm column (the v2 caption ran 144 mm and spilled into the
crescent); headline rule extended to the full sheet width; the two orientation
marks moved out of the caption block they were grazing.

**v4** — the spiral thread was cut. However steep it was made it still read as
one more ring, and its crimson twin sat on top of it in purple. Its three jobs
were folded into the wedge, which had to exist anyway, giving **the corridor**.
Three long "shared spoke" rays deleted — with the corridor present they said
the same thing twice and read as damage. The ∂L/∂z crown moved out of the core
disc, where it was invisible against the elected sector's fill.

**v5** — the corridor reported a **100 % return**. Honest arithmetic, wrong
story. Also: its rungs had been placed at 134°, across a fan the gate had
emptied, so they floated on blank paper as a separate little diagram instead of
slicing material.

**v6** — the corridor angle became the **median of 256 candidates**, its return
became a single run stopping at the first dead cell (which is what happens to
one trace), and the rungs moved into the dense arc and got two passes so they
win their crossings. Return: 32 %. Top-right data block moved above the
headline rule.

**v7** — corridor search constrained to 130–190° so both edges stay on the
cropped sheet. The stage table gained **the trade drawn twice**: a cell comb
that halves down the column beside a channel comb that doubles, at one fixed
pitch. This is the single biggest legibility win in the whole round — the
resolution-for-depth trade became readable without reading.

**v8 – v10** — the two head figures were 48 % / 47 % and read as a typo; the
first now reports the *blank* (52 %), which is what the caption claims. The
input band's duty opened to 0.30–1.00 so the rim reads as fine tonal texture —
the photograph — rather than three plain circles. The corridor's name was
right-aligned against the rim, then moved off the caption's baseline entirely:
3 mm on a shared baseline is a collision however small the gap. Dead helpers
removed.

---

## Honest critique — the weakest part

*(Proposals only. NONE of this is in the approved v10 file. Anything here would
be rendered as v11+ from a separate copy, for Juan to accept or reject.)*

**The crimson half of each band does not, on its own, say "the same angles as
the black half, punctured".** It reads correctly as *sparser and broken*, which
carries unpooling; but the claim that the void has one address for both
directions is carried almost entirely by two supporting devices — the corridor's
rungs and the short register rules at the two widest closed wedges per band —
rather than by the band texture itself. A viewer at three metres gets "a
collapse, gated, with a broken echo", which is most of the argument; the
*registration* specifically needs the one-metre read. If this goes another
round, the fix is not more furniture: it is to make the forward and backward
sub-bands of one band share a single drawn envelope (a hairline that traces the
open wedge across both halves, so the pairing is one closed shape rather than
two textures that happen to align).

Second weakest: the two orientation marks (`forward` / `gradient`) in the
crescent are the only pieces of pure key on the sheet. They earn their place —
they are what assigns meaning to blue and crimson — but they are the one place
the plate explains rather than shows, and a stronger round would find a way to
let the corridor's chevrons carry it alone.
