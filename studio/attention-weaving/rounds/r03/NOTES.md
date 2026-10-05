# r03 — SUMS TO ONE

> **v10–v19 is a REWORK** against `studio/attention-weaving/FEEDBACK.md`
> (Juan, 2026-09-20, on v9): *"the black softmax should be smoother"* and
> *"the top looks much better than the bottom part"*. The two notes are
> answered in **§ REWORK** at the end; everything above still describes the
> piece. v9's source is frozen at `piece_v9.py` (`--fn attention_weaving_v9`)
> so Juan's reference point stays renderable.

**Thesis: ABSTRACT ORDER.** r01 and r02 recreate the reference braid. This round
does not. It keeps what the reference is *about* — strand craft, the
inevitability of the constriction, Q and K meeting before the waist and V only
after — and transposes it into an order that is not a top-to-bottom braid and
has no central bead column.

---

## The abstract order, in one sentence

> **Attention drawn as the potential flow through a single slit in a wall: a
> double sunburst whose mirror plane is one black rule with one hole in it —
> every streamline crosses the wall at exactly one point, inside the slit,
> because that is what the coordinate system *is*.**

Not a metaphor for a constriction. The whole sheet is the elliptic coordinate
system of the aperture:

```
z = A + c·cosh(φ + iψ)      x = ax + c·cosh(φ)·cos(ψ)
                             y = ay + c·sinh(φ)·sin(ψ)
```

* `φ > 0` is above the wall, `φ < 0` below, and **`φ = 0` IS the slit**.
* A streamline is `ψ = const`. It crosses `φ = 0` at `x = ax + c·cos(ψ)` — a
  point that is *always* inside `[ax−c, ax+c]`. "Everything passes through one
  constriction" is therefore not something the drawing asserts; it is a theorem
  about the coordinate system the drawing is made of.
* The orthogonal family `φ = const` are the confocal ellipses — the
  equipotentials of the same flow. They are the only scaffold on the sheet,
  dotted and behind, and they are real physics rather than drafting furniture.

Order in the rubric's vocabulary: **radial-bipolar / flow-through-an-aperture**.
Not interlaced-cartesian (`bauhaus_loom`), not flow-to-attractors
(`bauhaus_gradient`), not a stacked axonometric terrain (`bauhaus_relevance`,
`attention_DAG`), not a braid (the reference, r01, r02).

## And the twist

The Deco sunburst is the machine age's emblem of *radiance pouring outward*.
Here it is drawn twice, mirrored, and the mirror plane is a wall with one small
hole in it. All that radiance above; below it, a thin rope and a very large
silence. **The sunburst is a drain.** The title delivers the punchline dry:
everything in the upper half of the sheet is on its way to a number that sums
to one, and the emptiness at the bottom is the probability mass the softmax
threw away.

## Mechanism → geometry (exact, one line each)

| mechanism | geometry |
|---|---|
| `Q_i` | a streamline `ψ_i` — a query is a *direction* |
| `K_j` | a spiral that sweeps across the whole Q fan high in the sheet, then drops into the slit — a key is compared against every query it can reach |
| `s_ij` | the crossing of `K_j` and `Q_i`; **`sign(s_ij)` decides over/under** |
| softmax (width) | filament group *g* holds `p_g = round(a_g·N)` filaments, `Σp_g = N = 38`; groups packed at a constant inter-clump gap, so a heavy key is a **wide clump** and a dead key is **one crushed hairline**. Same layout at the slit and (relaxed wider) in the cable. |
| softmax (height) | the **smooth monotone profile standing on the wall**: a Fritsch–Carlson interpolant through two knots per clump, both at `ZMAX·a_g/a_max`. It is flat at exactly `a_g` across the middle of clump *g* and bends only in the outer third, so the silhouette is smooth AND every step is still its exact height and its own clump wide. Registration ticks mark every clump boundary; a disc sits at every clump centre with **area ∝ a_g**. |
| normalisation | a second, finer curve — the **cumulative** — rises monotonically across the slit and lands on a disc at exactly **1.000**. |
| conservation | **38 filaments in, 38 out.** Nothing is born below the wall, nothing dies above it. |
| `Z = AV` | the cable leaves the gate as bare green hairlines and gains its gold only where V is woven in. |
| V | `V_j` is absorbed into lane group *j* (value *j* added to lane *j*). Reaching it, it crosses every group between it and the flank — **real over/under, decided by that value vector's own components**: gold dips under where `v_j[component]` falls in its lowest quartile. |

**Key ordering.** The keys are dealt *around the peak* — heaviest at the crown,
then alternately right and left in decreasing order, two right for every one
left so the hill is skewed rather than symmetric. That is a permutation of the
key index, which attention is invariant to, and it is the same licence
`bauhaus_loom` takes when it sorts warp rows. It turns the profile into one
smooth hill instead of sixteen steps of noise, and it puts the heavy lanes down
the **core** of the cable rather than along one edge.

**Softmax temperature** is not guessed: it is solved by bisection so that
`a_max = 0.190` exactly — peaked, with a readable tail (`H = 3.762 bits` over
16 keys, against 4.000 bits for uniform).

**Over/under is done with `engine/geometry.py`'s exact clipping** — every
crossing is a `Circle` punched out of the *under* strand's polyline with
`clip(..., keep="outside")`, so the break stops exactly on the circle. No
sampling, no luck. 129 of the 400 `Q·Kᵀ` scores have their crossing on the
sheet (stated in the footer); the rest of each key's sweep runs off the frame
before it reaches those queries.

## Style canon

**ART DECO** (`STYLES.md` #2), committed deliberately. The reference sits in a
quiet drafting idiom and the collection is already heavy with Bauhaus; Deco is
unused and its order genuinely matches the mechanism — the **ray fan converging
on a focus** and the **stepped ziggurat** are the two things this piece needs
most. In use here: the double ray fan, nested arcs (the confocal
equipotentials), the stepped ziggurat (the distribution), thin/thick by pass
count, wide-tracked spaced caps at monumental scale, cream stock.

Deco permits symmetric monumentality; this plate deliberately breaks it — the
aperture sits at 0.425 W / 0.620 H, the rope leaves down-right only, V enters
from the left only, the type is flush-left in the lower void.

**Declared flatness:** the plate is flat by canon (Deco is a flat, graphic
idiom) and by subject — it is a plane flow, and depth would be a lie about it.
The only depth cue is real occlusion at every crossing, which is the subject.

## Paper and orientation

`24x30` portrait (240 × 300 mm, drawable 220 × 280 after the 10 mm margin) —
the same sheet as the reference and as r01/r02, so the three rounds are
comparable on the wall. The order wants a heavy top and a long fall: the wall
sits at 0.62 H, so the storm gets the upper 38 % and the silence the lower 62 %.
A landscape sheet would have made the wall shorter than the storm is wide and
killed the "everything must get through" pressure.

## Render command

```bash
.venv/bin/python scripts/render_candidate.py \
  studio/attention-weaving/rounds/r03/piece.py \
  --fn attention_weaving --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen \
  --out gallery/studio/attention_weaving/current/pp_attention_weaving_aperture_v19.png
```

v9 (Juan's reference for "the top is good") is frozen and still renders:

```bash
.venv/bin/python scripts/render_candidate.py \
  studio/attention-weaving/rounds/r03/piece_v9.py \
  --fn attention_weaving_v9 --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen --out <path>
```

Deterministic: re-rendering at seed 7 produces byte-identical GCode.

## Pens

| pen | colour | carries |
|---|---|---|
| 0 | black | the wall, the stepped profile, the dotted equipotentials, reeds, all type |
| 1 | crimson | **Q** — the streamlines (the principal query double-passed) |
| 2 | dodgerblue | **K** — the sweeping spirals (heavy keys double-passed) |
| 3 | goldenrod | **V** |
| 4 | darkgreen | **Z = AV** — the rope |

Cream stock. Five pens, so four swaps.

## Plot budget (v19, seed 7, 24x30 portrait)

* **Draw 19 551 mm · travel 20 233 mm · 24 329 commands · 1 201 strokes**
* per pen — black 509 strokes / green 296 / gold 186 / crimson 111 / blue 99
* **0 bounds violations**
* minimum lane pitch **0.950 mm** (over the 0.8 mm floor); the tightest black is
  the wall at 5 passes × 0.31 mm = 1.55 mm and the profile at 5 × 0.30 mm
* travel slightly exceeds draw because of the over/under gaps — they are the
  subject, so the cost is accepted

## Exactness, measured (`piece.LAST_STATS`, filled on every call)

| claim | measured |
|---|---|
| the weights sum to one | `Σa = 1.0000000000` |
| the peak is the solved target | `a_max = 0.190000` |
| the cumulative curve lands on one | `1.0000000000` |
| the smooth profile still passes through the exact weight | max knot error `0.000e+00 mm` |
| the partition tiles the slit | span `51.920000 mm` vs slit `51.920000 mm` |
| nothing is created or destroyed | 38 filaments in, 38 out, `Σp_g = 38` |
| peaked, not uniform | `H = 3.762` of `4.000` bits over 16 keys |
| plottable | min lane pitch `0.950 mm` |
| the weave is real | 113 of 352 `Q·Kᵀ` crossings on the sheet, 366 `V × lane` crossings |

## Per-round log

| round | change | why |
|---|---|---|
| **v1** | first geometry: aperture coordinate system, Q streamlines, K spirals, wall + hole, ziggurat, rope, V fan, title | prove the order works at all |
| **v2** | temperature bisection (v1 was `a_max = 0.70`, one key eating everything); crossings moved high in the sheet so the weave is visible; title split to two lines and measured; `_cut_and_emit` re-clips offset passes | 409 → 49 bounds violations; the rope was a solid slab; the softmax was degenerate |
| **v3** | filament layout rewritten as **clumps with constant gaps** (weight = clump width); dashed-before-V / solid-after-V; ziggurat aligned to the clumps | the rope was uniform tone and carried no distribution |
| **v4** | **keys sorted by weight** → the profile became a real descending ziggurat instead of 20 steps of noise; V restaged as a comb feeding the rope along its length | the softmax was illegible, V read as a decorative lens |
| **v5** | rope shortened and lifted above the title band; V absorbed early so the dash zone is compact; footer rewritten to fit | gold was over-printing "SUMS"; the dashed zone was a grey fog over half the sheet; **0 bounds violations** from here on |
| **v6** | rope layout **relaxes** from the slit packing to a wider packing downstream (clumps separate as the flow relaxes); V made to dive across the rope | the clumps washed out downstream; V ran alongside the rope instead of through it |
| **v7** | V's approach handle put on the rope normal on the side V actually arrives from (v6 sent it on a 55 mm hook) | the gold knotted into an obvious error |
| **v8** | V entry band narrowed to 40 mm, dash coarsened to 4.6/1.7 | the lower half was three equal horizontal bands; now gold is a compact bundle and the lower-left void is bigger |
| **v9** | equipotentials tightened to read as dotted arcs rather than scattered dashes; V dive steepened | **shipped; Juan: REWORK** |
| **v10** | `_pchip` monotone interpolant replaces the ziggurat; 24 keys; cumulative curve; graduated knot discs (`fill_disc`, not `_dot`); steep cable; per-component over/under | note 1 + note 2, first attempt |
| **v11** | keys re-dealt around the peak (v10's monotone sort + linear height gave a cliff against a flat line); dash dropped; gauge rebuilt from real lane positions | the profile was smooth and unreadable; the lower half was grey fog |
| **v12** | `a_max` 0.30 → 0.20; two-sided V comb; gold dominant (under only in its lowest quartile); gauge cut | the hill was a needle; the weave was mush; the gauge read as a scratch |
| **v13** | 24 keys → 16, `n_q` → 22; right-hand bundle's shared waist removed | the right gold folded into a bowtie; clumps too narrow for the hill to breathe |
| **v14** | **two knots per clump** → flat tops, so the curve is smooth *and* every step is its exact height and width; right entries re-ordered to follow their targets | the peak was still a needle; the bowtie persisted |
| **v15** | back to one-sided gold; `a_max` 0.17, `ZMAX` 0.062·H | the right-hand gold read as a flat mirror band and flattened the bottom again |
| **v16** | `a_max` 0.19, `ZMAX` 0.080·H, wider flats, flare spread earlier | v15 over-corrected — the hill had shrunk to a bump on the wall |
| **v17** | seven-knot spine (five overshot the turn); profile to 5 passes | two dense ink knots at the cable's bend |
| **v18–v19** | labels moved clear of the slit and each other; `LAST_STATS` hook so every exactness claim is measured rather than asserted | final |

## REWORK — v10 to v19 (against `FEEDBACK.md`, 2026-09-20)

### Note 1 — "the black softmax should be smoother", without faking the numbers

Four things changed, and every one of them is checkable in the table above.

1. **A monotone interpolant replaces the staircase.** `_pchip()` is
   Fritsch–Carlson: it *interpolates* every knot and provably cannot overshoot,
   so a smooth curve through the weights is still exactly the weights. Measured
   knot error against the exact `a_g` at every clump centre: **0.000e+00 mm**.
2. **Two knots per clump, not one.** The first attempt (one knot at the clump
   centre) turned the peak into a needle. The curve now carries a knot at
   `lo + 0.26·w` and `hi − 0.26·w`, both at `a_g`, so each clump has a genuine
   **flat top at its exact height across the middle of its own width** and only
   bends in the outer third. Smooth silhouette, exact steps.
3. **The keys are re-dealt around the peak.** Sorted-descending (v9) plus a
   linear height axis gave a cliff against a flat line — smooth, and unreadable.
   Dealing heaviest-at-the-crown then alternately right/left (2:1, so it is
   skewed not symmetric) makes one asymmetric hill. Still a permutation of the
   key index, which attention is invariant to.
4. **Proportions and a second curve.** 24 keys → **16**, so each clump is wide
   enough for its flat to show; `a_max` 0.300 → **0.190** (still 3.0× uniform,
   `H = 3.762` of 4.000 bits) so the shoulders exist; `ZMAX` tuned to 0.080·H so
   the hill is a hill, not a spike. The **cumulative** is drawn as a second,
   finer monotone curve rising across the slit to a disc at exactly **1.000** —
   the title of the piece, stated as geometry. Registration ticks still mark
   every clump boundary and a disc of **area ∝ a_g** sits at every clump centre,
   so the partition is visibly discrete underneath the smooth silhouette.

Nothing about exactness moved: `Σa = 1.0000000000`, the partition still tiles
the slit to the micron (51.920000 mm of 51.920000 mm), 38 filaments in and out.

### Note 2 — "the top looks much better than the bottom part"

The upper half was not touched. Six changes to the lower half:

1. **The cable falls steeply out of the gate, then turns hard.** v9's lazy S ran
   the cable almost parallel to the gold, so the two families lay alongside each
   other and the weave could not read. The cable is now near-vertical exactly
   where V cuts it, so **every crossing is at about 55°** — an event, not an
   overlap. (Seven spine knots, not five: the five-knot Catmull overshot the turn
   and left two dense ink knots at the bend, visible in v13–v16.)
2. **The cable holds the slit's width through the weave**, then flares into the
   exit reed. It used to expand immediately, which diluted the crossing zone.
3. **The gold is loud.** V filaments are now 2–3 passes each and there are 16 of
   them, not 24 hairlines — the coordinator's suggested 8–10 in spirit, arrived
   at by lowering the key count rather than by dropping any value vector.
4. **Over/under is decided per crossing, from the value matrix.** A lane is one
   component of `v_j`, so the sign at each crossing is `sign(v_j[component])` —
   real data, exactly as `sign(s_ij)` is upstream. And gold dips **under only in
   its own lowest quartile**, so one family is dominant, which is what a weave
   actually looks like. 366 real `V × lane` crossings.
5. **The dashed cable head is gone.** With 366 crossing gaps in the same zone,
   dashing turned the whole lower half into grey fog. The arrival of the gold is
   a better marker for `Z = AV` than a dash ever was, and it is the reference's
   own device ("V is spun into the braid").
6. **Two experiments were tried and cut**, both visible in the version trail: a
   black gauge across the cable (v10–v11 — read as a scratch, not a scale) and a
   two-sided V comb entering from both flanks (v12–v14 — halved the crossings
   and filled the right void, but the right-hand bundle read as a flat mirror of
   the left and flattened the composition again). One-sided gold plus a large
   L-shaped silence down the right and across the bottom is the stronger answer.

## Honest weakest part

**The cable's run-out.** From the weave to the right rim the cable is 80 mm of
smooth, evenly-fanning green with nothing happening in it — it carries the clump
grouping (you can count the groups at the reed) but no event. It is the one
passage on the sheet that is filling space rather than arguing. If it gets
another round the answer is either to crop it at the frame much sooner, or to
give it the thing I cut: a real registration incident, built from the lane
positions rather than from the spine.

Second: **113 of the 352 `Q·Kᵀ` scores have their crossing on the sheet.** Stated
in the footer rather than hidden, but a family of K spirals where every key
sweeps every query *and* all of them still fall into one slit is a geometry
problem I have not solved.

Third, smaller: the **gold bundle is sixteen near-parallel arcs** across the
left. It is loud and it crosses well, but as a gesture it is more even than the
crimson/blue storm above it.

## Requests for the shared engine (NOT made — `promptplot/` untouched)

1. `geometry.py` has no polyline↔polyline intersection helper. Every piece that
   wants real over/under between two free curves has to hand-roll a bbox-culled
   segment sweep (`_crossings` here). `geometry.intersections(a, b)` belongs in
   the engine next to `clip`.
2. A `dash(poly, on, off)` by arclength is likewise re-implemented per piece
   (`_dash` here). `kit.dash()` would be a one-line win.
3. `kit.giant_type` has no multi-line/leading helper, so the two-line title
   sets its own baseline arithmetic.
