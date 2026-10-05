# superposition — r01 (EXACT RECREATION)

Reproduction of `studio/superposition/ref/reference.png`. No redesign: every
element, position, colour and mark type is transcribed from the reference.

- piece: `studio/superposition/rounds/r01/piece.py`, `def superposition(rng, bounds, colors=5)`
- render: `gallery/studio/superposition/current/pp_superposition_v16.png` (+ `.gcode`)
- command:

```
.venv/bin/python scripts/render_candidate.py studio/superposition/rounds/r01/piece.py \
  --fn superposition --seed 7 --colors 5 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black \
  --out gallery/studio/superposition/current/pp_superposition_v16.png
```

16 rounds, each one rendered and read back against the reference.

## Method

**Measure the reference, don't judge it.** Every size and position in this piece
comes off the hue-classified ink masks, not off the eye. That is what caught the
labels being ~30 % oversized in v14 after two rounds of them "looking about
right", and what produced the side-bearing numbers below.

Everything is authored in **reference pixel space** (1122 × 1402, y down) and
mapped to the drawable area at the end. Measurements were taken off the
reference by hue-classifying its ink (`red / blue / ochre / green / neutral`
masks) and reading row/column profiles, not by eye:

| feature | reference px | fraction of sheet |
|---|---|---|
| plate centre line | x = 561 | 0.500 |
| Q / K baseline | y = 312 | 0.223 |
| Q·Kᵀ axis | y = 548 | 0.391 |
| softmax baseline | y = 839 | 0.598 |
| V baseline | y = 1106 | 0.789 |
| Z baseline | y = 1316 | 0.939 |

The masks confirmed two facts the eye can miss and the piece relies on:
**K is an exact mirror of Q about x = 561** (Q baseline x∈[24,475], K x∈[646,1098]),
and **every stage is centred on x = 561** (softmax [275,847], V [30,1093],
Z [163,959], axis [199,922]).

Reference bump centres were recovered from the dotted droplines (columns of
dense single-hue ink above each baseline): Q at x = 95/137/195/232/270/306/334/
361/401/437/462, V at offsets 0, ±87, ±153, ±209, ±301, ±378, ±436 from centre,
softmax at ±0, ±75, ±145.

## Two findings worth keeping

**The map has THREE vortex centres, not two.** The brief called two; the ink
masks show a small ring cluster at (535, 519) sitting between the two big eyes
at (639, 527) and (487, 577). It is easy to miss because the outer contours
swallow it, but without it the saddle between the eyes reads wrong.

**Eyes must be CONICAL cusps, not Gaussian peaks - general lesson for
contouring for pen.** For a peak `a*exp(-r/s)` (a cone) with uniform level
steps `D`, the ring radius is `s*ln(a/F)`, so ring pitch is `s*D/a` - constant -
and the eye's total radius is just `s`. For a Gaussian peak `a*exp(-r^2/2s^2)`
the radius is `s*sqrt(2 ln(a/F))`, whose derivative blows up as `F -> a`:
**rings spread apart as you approach the summit**, the opposite of the tight
whorl the reference shows. Two consequences that generalise to any contour
piece:

- if you want a dense eye, the field has to be cusp-like there;
- ring count and ring pitch are not independent - `rings x pitch ~= s`. So for a
  given minimum pitch (here the 0.8 mm plotting floor) the only way to buy more
  rings is to make the eye physically bigger. That is the whole reason this
  plate's vortices are looser than the reference's (see gap 2 below).

## The field I contoured

Not faked rings — a real 2-D scalar field, marching-squared with
`_marching_squares` + `_chain_segments` from `generative/generators.py` on a
1.7 px grid over x∈[296,828], y∈[412,672]:

```
F(x,y) =  Σ  aᵢ · exp(−½[((x−cx)/sx)² + ((y−cy)/sy)²])      11 broad, low blobs
        + Σ  aⱼ · exp(−r_ellipse / decayⱼ)                   3 conical cusps
        + 0.195 · fbm(0.0165·x, 0.0165·y, octaves=3)         seeded lumpiness
```

The broad Gaussians only shape the outer envelope. The **cusps are conical, not
Gaussian**, because that is the only way to get evenly-spaced tight rings at a
maximum: for `a·exp(−r/σ)` with uniform level steps `Δ`, ring pitch is
`σ·Δ/a` (constant) and the eye's radius is just `σ`. A Gaussian peak does the
opposite — its rings *spread* as you approach the summit. Cusps sit at
(639, 527) σ=66, (487, 577) σ=68 (the two vortices) and (535, 519) σ=21 (the
small third cluster the reference has between them).

Level ladder is hand-set rather than uniform: three close-packed **dotted**
outer rings at 0.128 / 0.183 / 0.238 of the field range hugging the boundary,
then 12 **solid** levels at a uniform 0.062 step. Verified extents against the
reference: outer contour 524 px wide (ref 486), solid boundary 433 px (ref ≈425).

The faint grey wash is a jittered stipple gated on `F > 0.36·range`, i.e. it is
the field's own core, not a painted-in shape.

## What I matched

- Five stages, their baselines, widths, dotted baseline continuations and the
  side each tail extends from.
- Q's 21-curve family including the nested sheaf at the dominant bump, and K as
  its exact mirror.
- Droplines rising *above* the apexes to a terminal dot, the apex marker
  sequence (filled disc / open ring / bullseye) and the baseline marker row.
- Four sweeping dotted connector fans (Q→map, K→map, softmax→V diverging,
  V→Z converging), each a cubic with a **monotone** control polygon: leave the
  source vertically, run flat, arrive vertically. Getting this wrong is what
  made round 1's fans bulge outside the family they came from.
- The red / blue vertical dotted ticks at x = 271 / 851 through the outer axis
  rings; the full-height dotted centre line, black down to V and green through Z.
- The Q·Kᵀ axis with its three open rings and weighted dots, the scatter of
  nodes shed below the map, the softmax spike row with its dotted ghost family
  and the droplines descending into it from the map, V's 13 clusters with
  crossing (not concentric) nest members, Z's nested bell with its dotted wide
  ghost.
- Colour assignment: crimson Q, dodgerblue K, goldenrod V + both ochre fans,
  forestgreen Z, black for the map / softmax / centre line.

## What I could not match, and why

**1. Tonal range.** The reference draws in at least four weights per hue —
dark, mid, pale tint, near-invisible ghost. A five-pen plot has one weight per
colour. Pale ghost families are rendered as *fine-dotted* curves in the same
pen, which is the closest plottable equivalent but reads as texture, not as a
lighter tone. This is the single biggest visual difference and it makes the
whole plate read busier and flatter than the reference.

**2. Vortex density.** The reference's right eye has ~20 rings inside a 30 px
radius — ~0.3 mm apart on A4, which a pen would smear into a solid disc. Ring
pitch is `σ·Δ·range` and is bounded below by the 0.8 mm floor, so at 0.8 mm the
eye can hold `σ/4.7` rings. I enlarged the cusps (σ 57→66) to buy density and
landed on **12 rings per eye at a measured minimum 0.88 mm**. The eyes read as
open whorls, not as the reference's near-solid dark pupils. The grey wash is
likewise a stipple, not a continuous tone.

**3. Type - mostly closed since v13; what is left is letterform shape.** Two
font fixes landed mid-task and both were taken up here:

- *case*: the shared stroke font gained a lowercase alphabet and both
  `_stroke_text` and `giant_type` now take case as written, so `softmax` sets as
  `softmax` (v13 and earlier had `SOFTMAX`).
- *metrics*: `proportional=True` gives each glyph its own advance instead of a
  flat 5.6 units, and the font now carries PER-CASE side bearings (1.02 for
  capitals, 0.55 for lowercase - see the calibration table below). Combined
  with re-measuring every label against the reference's own ink boxes:
  `Z = AV` sets **109.5 px against the reference's 110** and `softmax`
  **77.9 px against 77**. Both inside 1 %. No local tracking compensation is
  used anywhere in this piece - the font metrics carry it.

The labels are no longer guessed. Sizes are read off the masks: Q/K cap 27 px,
V 25 px, Q.K^T cap 27 px, `softmax` ascender 17 px, `Z = AV` cap 23 px. (v14 had
Q/K at 34 and V at 33 - about 30 % oversized, which the re-measure caught.)

What remains is shape, not case or tracking: the font is a monoline geometric
sans, no serif and no italic, so the capitals read mechanical where the
reference is bookish. And its lowercase is drawn nearly as WIDE as its
capitals - 2.8 cell-units of ink per lowercase glyph against 2.7 for a cap -
whereas a real text face narrows lowercase relative to its em - which is WHY a
single global side bearing could not serve both cases.
That was fixed centrally by the per-case bearing; what survives it is
letterform condensation, which only redrawn glyphs would solve.

`giant_type(weight=...)` would thicken glyphs but by offsetting copies ~0.28 mm
apart, well under the floor, so all type here is single-stroke and reads lighter
than the reference's.

**4. Sheet aspect.** The reference is 1122 × 1402 (0.800); the A4 drawable area
is 190 × 277 (0.686). I map **anisotropically** so every element keeps the
reference's fraction of the sheet — the whole plate stretches ~17 % vertically
as a unit. The alternative (`_Sheet.k = sx/sy`, still in the code as a one-line
change) keeps each bell's local aspect but pays with 14 % shorter bumps and
wider gaps between stages; side by side that reads worse. **Decision confirmed: keep the stretch.**

## Other differences a viewer would notice

- The dotted halo around the map is heavier than the reference's — three dotted
  rings of equal-sized dots against the reference's progressively fainter ones.
- My V family is more regularly symmetric than the reference's, whose cluster
  heights drift slightly off-mirror.
- The reference's fan strands bundle tighter as they arrive at the map; mine
  stay more evenly separated.
- `softmax` now matches the reference's width to 1 %; what still reads
  differently is the letterform - monoline sans against a serif text face.
- Q.K^T sets 89 px against the reference's 122: the monoline caps cannot fill
  that span at a 27 px cap height, so the group is spread on glyph positions
  rather than scaled up.
- Reference node dots vary in tone as well as size; mine only vary in size.
- The Z bell's outer curve is the one dark line in the reference; here it is the
  same weight as the nest inside it (a double stroke would sit 0.19 mm off).
- Bell tails are truncated 2.8 px (≈0.47 mm) above their baseline — without
  that, a dozen tails plus the baseline all re-ink the same line for tens of mm.

## Plate stats (seed 7, A4 portrait)

```
commands     68 825
draw          8 699 mm     crimson 1278 · dodgerblue 1275 · goldenrod 2794
travel       10 950 mm     forestgreen 856 · black 2497
pen cycles    5 573        (the four dotted fans are most of this)
```

## Line spacing

Audited by sampling every stroke at 0.4 mm and counting *sustained* near-parallel
contact (|cos| > 0.94) under 0.8 mm, ignoring crossings and marks under 4 mm:

- **contour rings: clear** — no ring pair under 0.8 mm; measured eye pitch 0.88 mm min.
- **stipple tone: clear** — 6.2 px (≈1.05 mm) jittered grid.
- **type, fills, double strokes: none present.**
- **remaining hits are grazing bells inside one family** (min gap 0.02–0.04 mm
  over ~30 mm): two nested bells of similar height/width converge as they
  approach the shared baseline. This is a property of the reference drawing
  itself, and it re-inks a line once rather than building up a hatch, so I kept
  the reference's geometry instead of distorting the families apart.
- Solid ink dots use a 0.30 mm spiral pitch — a declared exception; a plotted
  dot has to be solid and every one is under 1.6 mm across.


## Side-bearing calibration (measured here, now the shared font's defaults)

`_glyph_advance` adds a side bearing per side. Measured against this reference
at matched heights, with a single global bearing of 1.1:

| label | ink sum | advance at sb=1.1 | reference | sb for an exact match |
|---|---|---|---|---|
| `Z = AV` (caps, 23 px) | 16.4 u | 113 px | 110 px | **1.02** |
| `softmax` (lowercase, 17 px) | 19.8 u | 100 px | 77 px | **0.53** |

**1.1 was well calibrated for capitals and about twice too loose for
lowercase**, because this font draws lowercase at nearly capital width (~2.8
cell units of ink against ~2.7 for a cap) while giving it only 4.0 of x-height.
A fixed bearing is therefore a far larger share of a lowercase advance. A single
global number could not serve both: 1.02 said caps were already right, and 0.53
everywhere would have collided them.

`_glyph_advance` now takes two bearings and branches on `ch.islower()`, with
**1.02 for capitals and 0.55 for lowercase**. Confirmed in v16:

| label | mine | reference | match |
|---|---|---|---|
| `softmax` | 77.9 px | 77 px | 101 % |
| `Z = AV` | 109.5 px | 110 px | 100 % |

`_ADV_CACHE` was keyed on the character alone, so a caller passing a non-default
bearing got whatever value was cached first and the result depended on call
order. It now keys on `(ch, sidebearing, sidebearing_lower)`. Regression
checked: `_glyph_advance('s')` -> 4.0, then with `sidebearing_lower=2.0` -> 6.9,
then default again -> 4.0. Nothing used a non-default bearing at the time, so
nothing was broken; it would have failed silently the first time anyone tuned
one per piece.
