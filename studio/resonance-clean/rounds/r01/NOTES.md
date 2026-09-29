# ATTENTION AS RESONANCE — exact recreation, round 01

Reference: `studio/resonance-clean/ref/reference.png` (1122 x 1402 px).
Piece: `piece.py :: attention_as_resonance(rng, bounds, colors=5)`.
Render: `gallery/studio/resonance/trials/pp_resonance_clean_v1.png`.

```
.venv/bin/python scripts/render_candidate.py studio/resonance-clean/rounds/r01/piece.py \
  --fn attention_as_resonance --seed 7 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black --colors 5 \
  --out gallery/studio/resonance/trials/pp_resonance_clean_v1.png
```

Plot cost: **49,682 commands · 35,209 draw moves (G1) · 2,894 pen-down cycles
(M3) · 2,895 travels (G0) · 9,443 mm drawn · 9,201 mm travel.**
No stippled cloud anywhere — the interference figure is computed geometry, which
is both truer and roughly 2x cheaper than the 98k-command stipple route.

## How the reference is carried over

Every coordinate in `piece.py` is a **measurement off the reference raster**, in
reference pixels, mapped once by `_fit()`: a single uniform width-fit of the
content box (45, 25)–(1085, 1340) into the A4 drawable area (10, 10)–(200, 287).
That is 0.1827 mm per reference px; the content is 190 x 240 mm, centred
vertically with 18.4 mm of slack top and bottom (the reference content box is
proportionally wider than A4, so width-fit is the only way to keep circles
circular). `P(rx, ry)` and `L(d)` are the only places the mapping appears, so the
layout is the reference's, not mine.

## The maths

### Wave packets — one helper, used for all sixteen

`packet_curves(y, xa, xb, lobes)` with `lobes = [(c, sigma, A, T, phi), ...]`:

```
env(x) = SUM_i  A_i * exp(-((x - c_i)^2) / (2 sigma_i^2))
wav(x) = SUM_i  A_i * exp(-((x - c_i)^2) / (2 sigma_i^2)) * sin(2 pi (x - c_i)/T_i + phi_i)
```

drawn as `y + wav(x)`, with `y +/- env(x)` traced as the faint outline. Sampling
is 13 points per shortest carrier period, so the crests never alias. The envelope
trace is split by `_trim()` into runs standing clear of the axis, so it appears
only where the packet is actually present — as in the reference.

Per-row parameters (centre, sigma, amplitude, carrier period, phase) are read off
the reference row by row: Q/K rows 1–5 and V rows 1–5 each carry one main lobe,
several carry a second smaller one, and rows 1/3/5 of Q carry a lower-frequency
"ghost" packet drawn dotted. Z is one large packet (sigma 58 px, A 80 px,
T 15.3 px) with four small flanking lobes at +/-91 and +/-164 px that produce the
two side bulges and the "eye" crossings on the axis.

### The interference figure — Huygens crest ridges

**This construction is the approved one, ported verbatim from the sibling plate
`studio/resonance/rounds/r01/piece.py :: _interference`. It was not reinvented.**

Two sources at `(561 -/+ 125, 611)`, separation `d = 250` reference px. A crest of
the wave from source *s* is the locus `r_s = m L`. Drawing both crest families is
exactly

```
cos(k r1) = 1    and    cos(k r2) = 1,     k = 2 pi / L
```

i.e. the **ridge lines** of the instantaneous superposition
`A = cos(k r1)/sqrt(r1) + cos(k r2)/sqrt(r2)` — not a level set of it. A level set
draws every fringe twice and closes into a lattice of blobs; that approach was
tried on the sibling plate and thrown out.

The one choice that makes the figure work: `d = 35 L` exactly, so crest *m* of one
family meets crest *35 - m* of the other **on** the axis instead of beating
against it. That single constraint produces all three of the reference's apparent
ring centres — the two lobes and the lens cells at the midpoint — with nothing
faked. `L = 250/35 = 7.14 ref px = 1.30 mm`.

Crests 1–21 are solid, clipped to an ellipse (218 x 126 px). Crests 22–51 are
dotted and clipped to a wider ellipse (272 x 158 px) — that is the pen's only
honest way to render the reference's outward tonal fade. Three sparse dotted
ellipses per source (a = 152/190/232, b = 0.60 a) ride outside.

The axis dot field is placed from the field value `|A(x, y)|` itself, so dot size
tracks real constructive interference.

**Anti-crowding.** Two crest families run *tangent* along the axis, the one place
a pen cannot resolve them. A plain occupancy grid also deletes the *crossings*,
which are the whole point, so `_Guard` rejects a point only when a nearby point of
a different stroke is within **0.82 mm AND within 25 degrees of parallel**
(`|u.v| > 0.906`). Real crossings pass straight through, tangencies get culled.

### softmax

Sum of seven super-Lorentzians on the baseline:
`y(x) = SUM_i h_i / (1 + ((x - c_i)/w_i)^2)^1.5`, with `w_i` 4–5.6 ref px, which
gives the reference's needle apexes with long merging tails. A fainter dotted
ghost distribution sits behind it, as in the reference.

### Convergence fans

Catmull–Rom splines through 6 hand-placed waypoints each, dotted. Q's six red
curves sweep right to x ~ 500 then dive down-left into the figure's upper-left
quadrant, ending on the vertical droplines at x = 314…466 with filled end dots;
K is the exact mirror about x = 557. The ochre softmax→V fan is nested so it does
not self-cross (leftmost start descends earliest, reaching the lowest V row); the
V→Z fan sweeps down-left into the Z packet's upper right.

## What I could not match, and why

1. **Type — case now matches, the serif does not.** A lowercase alphabet has
   since been merged into the shared font (`_GLYPHS`, 75 glyphs), and both
   `giant_type` and `_stroke_text` now take each character as written with a
   capital only as fallback. So this piece sets **`softmax`** and **`√d_k`** in
   real lowercase — correct word-shape, correct f/t and d ascenders, correct
   subscript. That was the loud half of the problem and it is gone. What remains
   is that the shared font is a single-stroke geometric mono: the reference's
   Didone serif (thick/thin contrast, bracketed serifs) and its *italic*
   subscript `k` are still out of reach, so Q, K, V, "Z = AV" and the title read
   as clean stencil forms rather than serif ones. Letterspacing is matched by
   measurement (title advance = 1.33 x cap height; `softmax` at x-height 13 ref
   px, 96 px wide against the reference's 12.7 px / 90 px). `√` has no glyph and
   is drawn as an explicit polyline. **No local glyph table is carried in this
   piece — everything comes from the shared font.**
2. **Tone.** The reference is a raster with continuous grey: its wavefronts fade
   smoothly from near-black at the source to pale at the rim, and its packet
   envelopes are watercolour-soft. A pen has exactly one value. The fade is
   approximated in two steps (solid crests → dotted crests) and the envelopes are
   fine-dashed. In the matplotlib preview my figure therefore reads considerably
   blacker than the reference; on paper with a 0.1 mm nib at 1.30 mm crest spacing
   the ink coverage is ~8%, which will sit much closer to the reference than the
   preview suggests. Judge this one on paper.
3. **Line spacing floor.** Crest spacing is 1.30 mm and the guard enforces 0.82 mm
   between near-parallel strokes. Inside the central comb the two families cross
   at shallow angles by construction, so *crossing* strokes do come closer than
   0.8 mm — that is inherent to an interference plate and is what the reference
   shows too. Nothing runs parallel below 0.82 mm.
4. **The reference's exact fan curves.** The red/blue/ochre dotted sweeps are
   reconstructed from their visible endpoints and apex, not solved; individual
   curvature differs even though the bundle shape and endpoints land.

## Differences a viewer would notice, ranked

1. The interference figure is heavier and flatter in value than the reference's
   soft grey gradient; its dotted outer crests read as a distinct texture change
   where the reference simply fades. (Expect this to narrow a lot on paper — see
   note 2 above.)
2. The letterforms are geometric single-stroke where the reference is a Didone
   serif, and the subscript `k` is upright where the reference italicises it.
   Case, word-shape and spacing now match; only the typeface does not.
3. The packet envelopes are visible dashed outlines rather than near-invisible
   ghost curves, so the Q/K/V rows carry more line than the reference does.
4. The reference's cream stock and warm ink tints are absent (pen colour is flat).
5. Fan curves differ in detail — same bundle, same endpoints, different curvature.
6. The Z side "eyes" are drawn as explicit small ellipses; in the reference they
   emerge from envelope crossings and are softer.

## Round log

- r1–r2: layout blocked out; interference drawn as two full wavefront discs.
  Dashing the rings to fake tone destroyed line quality — reverted.
- r3–r6: aperture-clipped families, progressive spacing. Size corrected from
  R = 198 to R = 134 ref px after measuring the reference's ring centres directly.
- r7–r10: leaf/slab radiation apertures to recover the central fringe band; got
  the band but never the reference's cell structure at the midpoint.
- r11: **replaced the whole figure with the approved sibling construction**
  (Huygens ridges, d = 35 L, crossing-safe guard). Also slowed every carrier by
  ~1.4x after a side-by-side of the Q block showed my packets were markedly
  higher-frequency than the reference, and switched the "...." axis continuations
  from dashes to round filled dots.
- r12: lowercase landed in the shared font. Set `softmax` and `√d_k` in real
  lowercase (x-height is 4/6 of the cell where caps fill 6/6, so the label was
  resized 13 -> 18 ref px and tracking tightened 1.16 -> 0.80 to hold its
  measured width), and trimmed glyph `weight` throughout — the fraction was
  reading bold against the reference's light serif.
