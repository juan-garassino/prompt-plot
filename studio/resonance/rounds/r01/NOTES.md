# ATTENTION AS RESONANCE — r01

**Task:** exact recreation of `studio/resonance/ref/attention-as-resonance.png` (1122 x 1402 px)
as a pen plot. Reproduction, not design — no element was invented or substituted.

**Entry point:** `attention_as_resonance(rng, bounds, colors=6)` in `piece.py`.
Nothing under `promptplot/` was modified.

**Render**

```
.venv/bin/python scripts/render_candidate.py studio/resonance/rounds/r01/piece.py \
  --fn attention_as_resonance --seed 7 --colors 6 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,darkviolet,black \
  --out ~/Downloads/pp_resonance_v13.png
```

`--colors 6` is required. `render_candidate.py` defaults `--colors` to 3, which folds the
six pens onto three and wrecks the colour reading.

---

## 1. Coordinate system

Everything in `piece.py` is laid out in the reference image's own pixel space, traced off
the PNG. `_Map.p(px, py)` maps a reference pixel to sheet millimetres; `_Map.s(v)` gives a
UNIFORM length so letterforms, circles, discs and arrowheads are built directly in mm and
never shear.

The reference is 1122 x 1402 (aspect 0.800). The A4 portrait drawable is 190 x 277 mm
(aspect 0.686). Rather than letterbox 40 mm of dead paper, the map fills the sheet:
horizontal scale 0.1694 mm/px, vertical 0.1976 mm/px. **Vertical distances and wave
amplitudes are therefore 16.7 % larger, in proportion, than the reference.** Circles drawn
in reference space come out 1.167x taller on the sheet — which happens to match the
reference's own slightly vertically-stretched ring lobes.

## 2. What I matched

- **Title** `ATTENTION AS RESONANCE`, spaced caps, centred, with the short centred rule and
  its single midpoint dot.
- **The wave-packet primitive** used everywhere (`wave_packet`), on an axis line, with the
  envelope outlined above and below and `· · · ·` axis continuations.
- **Q** — five rows, own carrier/width/centre per row, red, aligned node column at x=109,
  dotted continuations LEFT, six vertical dotted guides each capped with a dot, big `Q`.
- **K** — five rows, **its own traced geometry and packet table, not a mirror of Q**, blue,
  node column at x=1013, continuations RIGHT, mirrored guides, big `K`.
- **Convergence** — two nested smooth dotted Bézier curves per row (ten red, ten blue)
  fanning down into the centre, each ending on a filled dot.
- **Centre fraction** — true stacked fraction: `Q · K^T` (raised small-cap T, middle dot as
  a real filled disc) / rule / `√d_k` (radical + subscript), with the dotted ellipsis above.
- **The interference figure** — computed, see §3.
- **softmax** — label, baseline, six sharp peaks of differing height with stems, open/filled
  apex markers, eleven baseline markers, three ghost peaks, `· · ·` both ends.
- **V** — three ochre rows, own packets, `V` label, continuations right, dotted feed from
  the softmax band.
- **Z = AV** — one large green packet with a pronounced envelope and filled dots at the
  envelope extremes, four axis circles, dotted continuation left.
- **MoE** — label with a rule either side, `experts` / `top-2` / `router` annotations, the
  router as a dot inside two circles, five expert lanes of which exactly the top and bottom
  are solid with their own packets while the middle three are ghosted (dotted rail, dotted
  carrier, no envelope), converging into a second circled node, then **Y**.
- **Backward band** — five left fractions `∂L/∂Q ∂L/∂K ∂L/∂V ∂L/∂A ∂L/∂Z` in their colours,
  solid left-pointing arrowheads, dotted runs to an aligned column of open circles, and a
  dotted return curve per row sweeping up into the plate. Right: `∂L/∂Y`, `∂L/∂experts`,
  `∂L/∂router` in purple with right-pointing arrowheads and the dotted routing skeleton
  (corner turns, six circle nodes) between them.
- **Six pens** — red, blue, ochre, green, purple, black.

## 3. The maths

### Wave packets

    f(x)   = SUM_i A_i · exp(-((x - c_i)/s_i)^2) · cos(2π(x - c_i)/L_i + p_i)
    env(x) = SUM_i A_i · exp(-((x - c_i)/s_i)^2)

Each row carries 2–3 superposed packets. The small ripple visible on the reference's axes
between the main and secondary lump is not drawn separately — it falls out of two Gaussian
tails overlapping. `env` is the faint outline, drawn as a fine dashed line (a pen has no
tint). Sampling step is `min(L_i)/14`, so the fastest carrier gets 14 points per cycle.

### The interference figure

The instantaneous superposition of two point sources is

    A(x,y) = cos(k·r1)/√r1 + cos(k·r2)/√r2 ,   k = 2π/L

The reference draws its **ridge lines** — the wave crests `cos(k·r_s) = 1`, i.e. the Huygens
loci `r_s = m·L`. I tried a level set of `A` first (rounds 1–2): it draws every fringe twice
and, because `A` oscillates along the perpendicular bisector too, it closes into a lattice of
isolated blobs. That is demonstrably not the reference, so it was thrown away.

The crest construction gives, from one field and with nothing faked:

- concentric rings about each source (near a source the 1/√r weight makes that term dominate);
- the two families crossing on the hyperbolae `r1 − r2 = const` — the interference;
- tangency along the axis, cutting the lens-shaped cells that read as the fine vertical comb
  down the middle, and as an apparent third ring system at the midpoint.

Parameters: sources at reference x = 436 and 686 on y = 611, separation d = 250 px,
**L = d/35** so crest *m* of one family meets crest *35−m* of the other exactly ON the axis
instead of beating against it. Solid crests m = 1…21 (r ≤ 150 px), dotted crests m = 22…51
for the tonal fade-out, clipped away from the other lobe's solid field. Three concentric
dotted ellipses per source (a = 152/190/232, b = 0.60a) beyond that.

The dot field is sampled from the same `A`: three vertical columns of node dots at the two
sources and the midpoint, twelve radial spokes per source at five radii with dot radius
1.1 + 22·|A|, plus 60 seeded scatter marks — all with a minimum-separation test.

`_Guard` drops a crest point only when another stroke is within **0.82 mm** *and* within 25°
of parallel. A plain occupancy grid (round 3) also deleted the crossings, which are the whole
point of the figure; this one keeps every genuine crossing and removes only tangency crowding.

## 4. Plottability

Measured on the post-`merge_chunks` program, A4 portrait, seed 7:

| | |
|---|---|
| commands | 58 991 |
| strokes / pen cycles | 3 471 |
| draw | 10 264 mm |
| travel | 11 245 mm |
| bounds violations from the piece | **0** (bbox 21.6–196.3 x 14.6–280.3 mm inside a 10–200 x 10–287 drawable; the only point at the origin is postprocess's park move) |

Pen cycles per colour: red 653 · blue 669 · ochre 315 · green 180 · purple 418 · black 1 236.

**Line spacing.** Metric: resample every stroke at 0.25 mm; a sample is "crowded" if another
*stroke* has a sample within 0.8 mm whose tangent is within 25° of parallel (so crossings,
which are fine to plot, do not count). Then measure sustained runs ≥ 3 mm.

| region | draw | sustained < 0.8 mm | longest run |
|---|---|---|---|
| interference figure | 3 083 mm | 103 mm (3.3 %) | 10.5 mm |
| Q block | 1 485 mm | 327 mm (22.0 %) | 23.0 mm |
| MoE row | 1 793 mm | 432 mm (24.1 %) | 21.8 mm |
| softmax + V | 1 187 mm | 384 mm (32.4 %) | 25.8 mm |
| type + backward band | 1 229 mm | 550 mm (44.8 %) | 10.5 mm |
| **whole plate** | **10 264 mm** | **2 206 mm (21.5 %)** | **29.5 mm** |

So the hero figure is clean — the guard works. **The residual is not unresolvable detail, it
is deliberate co-incident ink, and the reference has the identical overlap:**

1. *Wave rows (Q/K/V/Z/Y/MoE, and the softmax baseline).* Every row draws a horizontal axis
   line and then a carrier that rides on it. Where the Gaussian envelope decays the carrier
   **lies on** the axis. The longest 29.5 mm run is exactly one axis line under one packet
   tail. The reference draws the axis straight through its packets too. On paper this is a
   second pass over the same line, not two lines the pen cannot separate.
2. *Envelope outlines* hug the carrier crests, as the reference's faint outline does. I tried
   standing them 0.8 mm clear (v12): it removed 0.1 % of the crowding and turned each packet
   into a dashed capsule that looks nothing like the reference, so it was reverted.
3. *Display type* (`Q K V Y Z=AV`, title, `MoE`) is thickened with offset passes at
   0.42–0.46 mm — the same trick as `kit.giant_type(weight=...)` with `tip=0.55`. Intentional.

**No two features that are meant to read as separate lines are closer than 0.8 mm.**

Suggested pen: 0.3–0.4 mm fineliner. At 0.5 mm+ the interference crests (1.21 mm apart
across, 1.41 mm down) start to close up.

## 5. Explicit deviations

- **SIX pens.** Red, blue, ochre, green, purple, black — exceeds the house 3–4 swap limit.
  Stated rather than silently dropping a colour, as instructed. Five swaps on the machine.
- **Vertical stretch 1.167x** — the reference's aspect does not fit A4 portrait (§1).
- **Typeface.** The reference is a book serif. PromptPlot's font is a single-stroke geometric
  sans with caps only, so this piece ships its own lowercase alphabet (a b c d e f g h i k l
  m n o p r s t u v w x y z) and two maths glyphs (`∂` as `@`, `√` as `#`) built in the same
  0–4 x 0–6 glyph space. The letterforms are visibly not the reference's.
- **`--colors 6` must be passed** (the render script's default of 3 would fold the palette).

## 6. What a viewer would notice, honestly

1. **Tone.** The reference is a tonal illustration: light-tint envelopes, ghosted expert
   lanes, greyed outer rings, and a solid grey smudge at the heart of the interference
   figure. A pen plot has one ink weight per pen, so every "faint" thing here is a fine dash
   or dot instead. The dark core of the interference figure simply does not exist in mine —
   it is an open line net. This is the single biggest difference and it is not fixable
   without a second, lighter pen or a halftone.
2. **The interference figure's fringe count.** The reference's crest pitch is roughly 6–7
   reference px; mine is floored at 7.14 px (1.21 mm across / 1.41 mm down) so a 0.3 mm pen
   can resolve it, and `_Guard` further thins the tangency zones. Result: my lobes read as
   two crisper bullseyes with a narrower crossing band, where the reference reads as one
   continuous field. The central comb is coarser and shorter than the reference's.
3. **Typography.** Serif vs single-stroke geometric. The title reads lighter and more
   mechanical; `Q`, `K`, `V`, `Y` are constructed letters rather than drawn ones; the
   hand-built `∂` is a recognisable partial but not the reference's italic one; lowercase
   `softmax` / `experts` / `router` are close in colour and size but not in form.
4. Smaller: my dotted work is uniform (0.4–0.5 mm dashes on ~2 mm pitch) where the
   reference's dotted lines vary in weight and density; the scattered dots on the
   interference field are placed from the field amplitude on a regular polar lattice rather
   than the reference's looser hand; the outer dotted ellipses read as clean furniture where
   the reference's are broken and faded.
5. The convergence fans have two curves per row; the reference's look like two to three with
   more variation in where each one lands.

## 7. Round log

| round | change | verdict |
|---|---|---|
| v1 | first pass; level-set interference, K mirrored from Q | K block drew on top of Q (mirror bug); interference was a lattice of blobs |
| v2 | mirror fixed, occupancy-culled level set, fractions/weights | cull shredded the contours into noise |
| v3 | **thrown out the level set**; Huygens crest construction | correct structure, but the two families did not interpenetrate |
| v4–v6 | crest radius up, graded clip solid/dotted, dot field, fans | reads as the reference's three apparent ring centres |
| v7 | K given its own traced rows and packets (no longer a mirror) | K stops looking like a flipped Q |
| v9–v11 | `_Guard` (parallel-only cull), wavelength / clip tuning | interference crowding 27 % → 3.3 % with crossings intact |
| v12 | envelope stood 0.8 mm off the crests | reverted — looked wrong, bought nothing |
| **v13** | final | — |
