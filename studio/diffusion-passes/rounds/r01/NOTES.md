# DIFFUSION — FORWARD, NETWORK, REVERSE · round r01

Faithful recreation of `studio/diffusion-passes/ref/reference.png` as a
three-register A3 landscape plate: noising across the top, the U-Net through
the middle, denoising back along the bottom.

## Render command

```
.venv/bin/python scripts/render_candidate.py studio/diffusion-passes/rounds/r01/piece.py \
  --fn diffusion_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,mediumpurple,palevioletred,crimson \
  --out gallery/studio/diffusion_passes/current/pp_diffusion_passes_faithful_v11.png
```

`--colors` defaults to the palette length, so the piece is called with 5 pens.
Final render: `gallery/studio/diffusion_passes/current/pp_diffusion_passes_faithful_v11.png`
(+ `.gcode` beside it).

## Pen assignment

| pen | colour | carries |
|---|---|---|
| 0 | black | structure, all type, furniture, the clean `x₀`, the isotropic `x_T`, `ε̂`, the skip arcs |
| 1 | dodgerblue | t-ramp, column `x_t1` · U-Net encoder mouth |
| 2 | mediumpurple | t-ramp, column `x_t2` · U-Net encoder depth |
| 3 | palevioletred | t-ramp, column `x_t3` · U-Net decoder depth |
| 4 | crimson | t-ramp, column `x_t4` · U-Net decoder mouth · the `x_t` input cloud |

Colour is the **time axis** on this plate, the one piece in the collection
where a pen ramp is a variable. Black bookends the ramp because `x₀` and `x_T`
are the two *pure* states — data and noise — and the ramp marks the mixture
between them. The ramp runs left→right in all three registers; the bowtie's
pen at any x is the pen of the state column directly above it (boundaries at
1/6, 1/2, 5/6 of the tube = the midpoints between columns 1..4).

## Plot budget

```
commands     69,119
pen cycles    6,741      (5 pen changes if plotted colour-by-colour)
draw          13.36 m    black 6.92 · blue 2.15 · purple 1.38 · pink 1.22 · crimson 1.68
travel        15.99 m
inked bbox    X 15.69 .. 398.74   Y 11.85 .. 283.69   mm
drawable      X 10.00 .. 410.00   Y 10.00 .. 287.00   mm   (A3 landscape)   IN BOUNDS
min spacing   RING_PITCH 0.80 mm nests · MIN_GAP 0.80 mm bowtie LOD  (pen tip 0.5)
```

Travel exceeds draw because ~2,500 speckle ticks are 0.56 mm marks. If that
matters on the machine, drop `N_SPECKLE` from 700 — the states stay legible
down to about 450.

## The ᾱₜ schedule

Cosine schedule, Nichol & Dhariwal 2021 ("Improved DDPM", eq. 17), offset
`s = 0.008`, sampled at six **evenly spaced** t:

| column | t/T | ᾱₜ | √ᾱₜ | rings kept (1 in N) | nest duty on/off mm | speckle dots |
|---|---|---|---|---|---|---|
| `x₀`   | 0.0 | 1.0000 | 1.000 | 1 | continuous | 0 |
| `x_t1` | 0.2 | 0.8987 | 0.948 | 1 | 7.11 / 0.80 | 51 |
| `x_t2` | 0.4 | 0.6475 | 0.805 | 2 | 4.96 / 2.70 | 205 |
| `x_t3` | 0.6 | 0.3408 | 0.584 | 3 | 2.45 / 4.74 | 420 |
| `x_t4` | 0.8 | 0.0940 | 0.307 | 5 | 0.59 / 5.72 | 595 |
| `x_T`  | 1.0 | 0.0000 | 0.000 | — | none | 700 |

The **linear** β schedule was tried first and rejected: at evenly spaced t it
puts √ᾱ at 1, .81, .44, .16, .04, 0, so two of the four intermediate columns
are already indistinguishable noise and the row has nothing to show. The
cosine schedule keeps the *shape* the brief asks for — early steps barely
change, the collapse is late and fast — with evenly spaced t and no fudging.

## How a state is drawn

`x_t = √ᾱₜ · x₀ + √(1−ᾱₜ) · σ · ε`, drawn as its two terms.

**SIGNAL** — the level sets of `E[x_t|x₀] = √ᾱ x₀`. Scaling a *field's values*
never moves its contours, so the nest keeps its size and its column; what the
attenuation costs it is contrast, and a pen spends contrast two ways:

- the ladder is **decimated** — a ring is still a ring only while the signal's
  level gap `√ᾱ·pitch` clears the noise's level spread
  `√(1−ᾱ)·LEVEL_NOISE·pitch` (`LEVEL_NOISE = 1.6`). That is why **fine detail
  dies first**, which is what a diffusion forward process actually does, and
  it is also the only way the nest stays off the plotting floor;
- the survivors are drawn at **duty ᾱ** (`on/(on+off) = ᾱ`);
- a slow warp of amplitude `√(1−ᾱ)·σ·0.26` carries the low-frequency share of
  the noise. Its correlation length is 3.2 R — eight plane waves at ~60 mm
  wavelength — so neighbouring rings *translate together*. At the first
  correlation length tried (0.85 R) the warp sheared one ring across the next
  and x_t1 came out as spaghetti.
- the **silhouette** (level 0) gets a duty floor of ᾱ = 0.42 and a second pass
  0.30 mm away. It is the highest-contrast contour on the form — its level
  jump is the whole field, not one ladder step — so it is the last thing the
  noise takes. That floor is what keeps a lobed outline legible inside the
  cloud at `x_t3` and `x_t4`, exactly as the reference has it.

**NOISE** — `ε` itself, as isotropic Gaussian speckle of spread σ, count
`700·(1−ᾱ)^1.15`, truncated (rejected, never clamped — clamping piles the
missing 2% onto a hard circle and gives the cloud a drawn edge) at 2.2 σ so it
stays inside its column.

**σ** is the data's own per-axis RMS spread. That makes the process
variance-preserving — `Var = ᾱ·Var(x₀) + (1−ᾱ)·σ² = Var(x₀)` for all t — which
is why every state occupies the same footprint with no fudge factor, and is
what lets a reader compare straight down a column.

**One trajectory, not six drawings.** A row shares one x₀, one smooth field
and one ε. ε is keyed to a *physical place* on the manifold (`_white(seed,
ring, arclength bucket)`) rather than to a mark index, so changing the dash
schedule with t does not reshuffle the noise: the same point of x₀ always gets
the same ε. The speckle comes from one fixed sequence, so the row simply
reveals more of the same ε as t grows.

**x_T is genuinely isotropic**: at ᾱ = 0 the signal term is gone entirely and
only the i.i.d. speckle is left. No residual lobe, no preferred direction. The
reverse row uses a *different* x₀ (4 lobes vs 3) and a different ε, so it
arrives at a clean x₀ that is recognisably of the same family but not a replay.

## The U-Net

The bowtie is the same drawing language as the states: a nested family of
closed streamlines `y = y_c ± c_j·h(x)`, pinched into a chain of lenses.

The four resolution levels **halve**, which is measured, not styled: bulge
half-heights on the reference are 107 : 62 : 33 : 17 px = 1 : .58 : .31 : .16.
The piece uses 1 : .58 : .30 : .155 with pinches of .058 / .033 / .020 / .013
between them and a waist lens at .075. The outer mouth closes on an elliptical
cap so it flares into a bell instead of a point.

**Dyadic LOD.** The perpendicular gap at refinement level L is
`dc·2^L·h(x)·cos(atan(h'))`. A required level is computed **per x** from the
profile alone and line j is drawn wherever its own trailing-zero level clears
it. Deciding per *line* (the first attempt) made the test flicker along every
bulge's steep flank and combed each lens into crumbs; per x gives clean dyadic
merges and leaves every streamline continuous between pinches. 48 lines per
side are drawn in the bells and 1 in 32 at the waist — which is why the
**waist is visibly the sparsest place on the sheet**, the one thing the plate
has to say about a U-Net.

**Skips** connect mirrored levels: arc k leaves the top of encoder bulge k and
arrives, arrowhead first, on the top of decoder bulge k, at s = .925, .465,
.235, .115 — the same four s values the bulges sit at.

## Fixes to the reference

The rubric's "OVERLAP IS A DECISION, NEVER A SYMPTOM" outranks fidelity, and
the brief's "what must be TRUE" outranks both.

1. **Column registration.** The reference's reverse row runs the colour ramp
   backwards (black, red, pink, purple, blue left→right) and puts its `x_T` at
   u 0.824 while the forward `x_T` is at u 0.905 — so no state sits above its
   counterpart and the plate's own argument is unreadable. Here both rows use
   one six-column grid and one ramp direction: column k carries the same t in
   both rows. Only the direction of *travel* differs, and that is what the
   arrows are for. This is the single largest deviation and it is deliberate.
2. **A right sidebar** (u 0.869 .. 0.980, 43 mm) holds both keyword stacks and
   the loss on one left edge. In the reference the bottom stack and the bottom
   `x_T` fight over the same 14 mm.
3. **Three separate bands** for the U-Net title, the skip-arc bundle and the
   "skip connections" label. In the reference the title overlaps the bowtie and
   the label sits inside the tube.
4. **The reverse formula and the bottom-row labels are on separate baselines.**
   In the reference the formula runs straight through the `x_t3` blob.
5. **State gaps go from 0.10 × D to 0.28 × D** (55 mm pitch, 40 mm forms).
6. Margins are matched: main content starts 10.9 mm inside the drawable on the
   left and ends 11.3 mm inside on the right.

## Font gap (a request for the shared engine, NOT made)

`promptplot.generative.generators._GLYPHS` has 88 glyphs and none of
`α ᾱ μ √ 𝒩 𝔼 ℒ ‖ [ ]`, nor sub/superscripts — so every formula on this plate
would silently lose characters (`_stroke_text` warns and advances). This round
carries a **local** math typesetter (`mtext`) with those glyphs in the same
4×6 cell metric plus a `_{..} ^{..} \R{..}` markup. It is local on purpose: I
was asked not to edit anything under `promptplot/`.

**Request:** promote the glyph table and the sub/superscript markup into
`engine/kit.py`. Four studio pieces have now hand-rolled some subset of it
(`convolutions` has a one-off `_sigma`), and every future ML/physics plate
needs the same dozen symbols.

## Per-round changes

- **v1** first full plate. Nest as a distance field, DDPM applied per mark.
  *Broken:* the smooth warp (correlation 0.85 R) sheared rings across each
  other, so `x_t1` was already spaghetti; the "skip connections" label sat
  inside the arc bundle.
- **v2** two-layer model (signal nest + speckle), correlation 3.2 R, fatter
  lobes, finer ring pitch, `ε̂` drawn clean, skip label moved above the arcs.
  *Broken:* `x_t3`/`x_t4`/`x_T` were three indistinguishable clouds.
- **v3** tried the full √ᾱ contraction on both layers plus pitch-driven ring
  decimation. *Broken:* the nest contracted out of legibility and its pitch
  fell under the floor; nest and speckle disagreed on scale.
- **v4** reverted the contraction (level sets do not move under value scaling),
  replaced pitch-decimation with the **SNR** criterion `_keep_every`. Sequence
  now reads 1, 1, 2, 3, 5.
- **v5** silhouette duty floor + lighter speckle ramp → a lobed outline
  survives inside the cloud at `x_t3`/`x_t4`, as in the reference.
- **v6** bowtie LOD moved from per-line to **per-x** (the big one: lenses stop
  being combed into crumbs); silhouette double pass; speckle truncated by
  rejection instead of clamping.
- **v7** 48 streamlines per side instead of 32 — the bells fill, and the
  bell:waist density contrast goes from 16:1 to 32:1.
- **v8–v11** sidebar becomes a real column (text fills it, its left edge
  matches the title's left margin), sidebar furniture moved onto that column,
  gutter rules centred in the 12 mm gutter, final margin balance.

## What I would fix next

1. **The `x₀` nests are coarser than the reference's.** The reference packs
   ~18 rings across a petal; at 40 mm forms and a 0.80 mm pitch a petal holds
   6–8. The rubric's own rule applies ("a reference packing 20 rings into
   0.3 mm cannot be matched at any pitch a pen can hold; enlarge the feature
   or accept fewer rings") — but the honest fix is to **enlarge**: at 52 mm
   forms the nests would carry 10–11 rings and look much closer. That needs
   the two rows' vertical budget rebalanced against the bowtie, which is a
   layout rewrite, not a parameter.
2. **`x_t4` vs `x_T` is the weakest step in the sequence.** 595 vs 700 dots
   plus a crumb of silhouette is a small difference for a whole column. Either
   push `x_t4` to t/T = 0.7 (ᾱ = 0.19, √ᾱ = 0.44) or give the surviving
   silhouette a third pass.
3. **Travel (16.0 m) exceeds draw (13.4 m)**, all of it speckle. Ordering the
   dots on a Hilbert curve inside each cloud before emitting would cut it by
   roughly half.
4. **The two innermost skip arcs are cramped** near the waist and cross each
   other. Staggering their apexes further, or dropping to three skips, would
   read better.
5. **`ε̂` is drawn as a clean contour nest** (the reference's choice) which
   sits oddly against its own caption "predicted noise". Drawing it as a nest
   whose *rings* are noise-shaped would be truer and still faithful.
