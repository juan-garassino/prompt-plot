# SSM / MAMBA — round 01 — THE RECEDING HORIZON

Piece: `studio/ssm-mamba/rounds/r01/piece.py`, entry `receding_horizon`.
Renders (A4 portrait, `--colors 3`, palette `black,crimson,forestgreen`):

    .venv/bin/python scripts/render_candidate.py studio/ssm-mamba/rounds/r01/piece.py \
        --fn receding_horizon --seed 7 --paper a4 --out ~/Downloads/pp_ssm_mamba_v7_s7.png

    ~/Downloads/pp_ssm_mamba_v7_s7.png   (seed 7  — chosen)
    ~/Downloads/pp_ssm_mamba_v7_s11.png  (seed 11 — best terrain form)
    ~/Downloads/pp_ssm_mamba_v7_s23.png  (seed 23)

Earlier rounds kept for history: `pp_ssm_mamba_v1..v6*.png` in ~/Downloads.

---

## 1. The exact recurrence that was run

A real diagonal S6 block, zero-order-hold discretised. Nothing is faked or
posed; every mark below is a projection of one of these arrays.

Token stream — TWO features, because a real S6 block reads *different* learned
linear projections of the same embedding:

    s_t  SALIENCE  = 0.02 + 0.11 * fbm(0.19 t)            baseline
                     0.97 at `events` topic boundaries    (selector saturates)
                     0.55 at up to 3 half-salient tokens  (a dent, not a cut)
    u_t  SIGNAL    = level_t + 0.75 swell_t + 0.85 mid_t + 3.2 chat_t,  mean-centred
                     level  : random walk, one step per topic boundary
                     swell  : fbm at 0.035/token   (~30-token period)
                     mid    : value noise at 0.11  (~9-token period)
                     chat   : value noise at 0.55  (~2-token period)

Selective step and ZOH discretisation (`a_n` log-spaced over 40 channels,
`a_0 = 0.15` … `a_39 = 2.60`):

    dt_t      = softplus(-1.55 + 9.0 * s_t)                 ~0.26 idle, ~7.0 at a boundary
    B_t       = 0.5 + 0.5 tanh(1.2 u_t)                     input-dependent B
    Abar_tn   = exp(-a_n dt_t)
    Bbar_tn   = (1 - Abar_tn) / a_n * B_t                   exact ZOH, not the Delta*B approximation
    h_tn      = Abar_tn h_(t-1)n + Bbar_tn u_t              THE SCAN  -> the corridor's height field
    S_t       = sum_(r<=t) dt_r                             the model's own clock -> the rule's ticks
    H_n(t)    = max{ l : a_n (S_t - S_(t-l)) <= 1 }         e^-1 horizon in TOKENS, solved
                                                            by walking dt back and interpolating
                                                            the last partial step -> fractional l

Derived, never scripted:

* `fires = { t : a_slow * dt_t >= 1 }` — a selection event is defined as "one
  step erases a whole time constant of the slowest channel", i.e. `H(t) < 1`.
  Red seams, red teeth, red stems and the red projection lines all come from
  this one set.
* `t* = argmax H(t)` — the longest reach, the green trace.
* The corridor's height is `Z = (h - mean_n) / rms_n`, clipped at 1.9 sigma. The
  per-channel normalisation is the readout `C` doing its job; it is what makes
  the visible gradient across the channel axis a TIMESCALE gradient (measured
  first-difference std ramps 0.26 -> 0.61 from slow to fast) rather than a gain
  gradient.

**Why the horizon is a sawtooth, exactly.** If `dt_t > 1/a` at token `t`, then
for every later `t'` any lag reaching past `t` fails the test, so `H(t') <= t'-t`:
the horizon grows at exactly one token per token after a cut, until it saturates
on `1/(a * mean dt)`. Ramps at 45 degrees in (time, lag), then a cliff. That
silhouette is the piece.

**The shared-metric trick.** The lag axis is laid on the SAME world pitch as the
time axis, so a tooth of length 18 is exactly as long on paper as 18 tokens of
sequence. The green "longest reach" segment runs back along *time* from `t*` and
is the same length as the tooth at `t*` — the drawing states its own scale twice,
on two different axes, and they agree.

## 2. Engine primitives used

All Scene3D declaration; no z-buffer, thinning or occlusion logic in the piece.

* `Scene3D(..., fit="none", px=(900,340), tip=0.5)` — `fit="none"` is required:
  `rescue`/`fill` would scale the composition back inside the margins and undo
  the deliberate crop at both frame edges.
* `surface(SX, SY, DEP, thin=ScreenThin(gap_mm=0.95, far_mult=1.8))` — native
  hidden-line + anti-crowding. `far_mult` thins the *far* half of the corridor
  (which is the sequence's past, because depth = wx + wz here), so the past
  literally fades. That coincidence of "far" and "earlier" is the reason the
  time axis was put on `+wx`.
* `lines(..., mode="over")` — the selection seams (exact transverse profiles,
  still depth-tested so near folds occlude them) and the doubled front silhouette.
* `poly()` — shadow teeth, envelope, rule, clock ticks, lag ruler, projection
  dashes; halo-aware, so every stroke opens a gap around type.
* `halo_labels()` — all type on one pen (`_pen(3, colors)` when 4+ pens are
  mounted, black otherwise), boxes reserved BEFORE any surface is drawn.
* `occupancy(0.9)` — crowd control for the clock-tick burst: at a boundary the
  internal clock advances ~7 units inside one token, which would otherwise pile
  7 ticks into 2.7 mm of paper. The burst survives as a visibly dense cluster
  without pooling ink.
* `engine.geometry.clip(poly, Rect(...), keep="inside")` — the frame crop, exact
  closed-form segment/boundary intersections (no sample-snap stagger at the edge).

**One axonometric basis.** `A` (screen mm per world unit), `CD` (depth drop) and
`HY` (height gain) are computed once and used by both plates. The floor plate is
a pure `-wy` displacement of `floor_mm`; the channel pitch `cs` is expressed *in
token units* so both plates share one metric. `floor_mm` is not a free number: it
must exceed `height_mm + 2*Zc*CD` or the corridor's near edge dips through the
shadow's rule — that collision is exactly what killed v1 and v2.

## 3. What was missing / had to be worked around

* **`surface()` draws both grid families.** There is no way to ask for only the
  along-time family, which is the grain this subject wants. The piece accepts the
  woven mesh (house look) and gets the directional reading from the aspect ratio
  instead. A `families=("row",)` argument on `surface()` would be a real addition.
* **`ScreenThin` can only thin the family that is locally tighter**, so it can't
  express "keep the long lines, drop every third cross line". Same gap.
* **`fit="rescue"` fights cropping.** Any piece that wants to bleed off the sheet
  must use `fit="none"` and do its own clip; `_clip_cmds` here is ~25 lines of
  pen-preserving run grouping around `geometry.clip`. That grouping (commands ->
  (pen, polyline) runs -> commands) belongs in the engine — `kit._runs_from_cmds`
  drops the pen, so it could not be reused.
* **No label-collision solver.** `halo_labels` protects legibility but does not
  prevent two labels overlapping each other, and nothing clamps a label to the
  sheet. A local `LBL()` helper does the clamping; the three-column legend row is
  hand-gridded.
* `scale_footer` is right-aligned only, so the equation had to live bottom-right
  regardless of what else is there.

## 4. Self-critique against DESIGN_RUBRIC.md

Scored honestly, as if the critic only saw the png.

| Dimension | Score | Reasoning |
|---|---|---|
| 1 Hierarchy | 7 | The corridor dominates at 3 m and the sawtooth shadow is a clear second; the stem chart and legend row are a proper third. But the corridor and the shadow are the same *gesture* — two parallel descending bands — so the 3:1 dominance the rubric asks for is closer to 2:1 in perceived weight. |
| 2 Grid & alignment | 8 | Everything derives from one axonometric basis; the stem chart is in exact x-register with the corridor's token pitch; the legend row is three columns on shared baselines; title and stage blocks share the left column. |
| 3 Tension & asymmetry | 7 | Strong working diagonal, hero cropped at both side edges (and that crop is the concept: no first token, no last token). Not centred. But the two bands are parallel rather than in conflict, and nothing overlaps another element with intent — the plates politely avoid each other, which the rubric names as a failure mode. |
| 4 Negative space | 6 | The upper band (below the subtitle, above the corridor) is a deliberate quiet zone that makes the corridor read louder, and the lower-left quiet band separates the shadow from the stem chart. Honest problem: there are now TWO large voids and the upper one is close to 60 mm tall and does very little. One of them should have been spent. |
| 5 Craft for pen | 8 | ~13 m of draw, 3 pens, no swaps beyond the 3. Mesh spacing 1.17 mm (channels) / 2.66 mm (tokens); shadow teeth 1.6 mm apart; clock-tick burst capped at 0.9 mm by `Occupancy`. Nothing floods. The one soft spot is the corridor's right third, where folds stack and the weave gets close to muddy at 0.5 mm. |
| 6 Concept legibility | 8 | It is a phenomenon, not a wiring diagram: a state surface and the shadow its memory casts. The sawtooth silhouette plus the red cuts reads as "it keeps growing, then something wipes it" before the caption is read. What does NOT land without the caption is that the shadow's depth axis is *lag* rather than a second spatial axis — a viewer may read it as a second surface. |
| 7 Depth | 8 | True hidden-line occlusion, real folds, depth-aware thinning fading the past, dotted projection lines establishing the shared basis. Not flat, not declared flat. |

**Average ≈ 7.4, with Negative space at 6 — this does NOT pass the bar**
(avg ≥ 8, nothing below 7). It is a solid r01, not a shipping piece.

**Single biggest weakness:** the shadow repeats the corridor's gesture instead of
opposing it. Both are long, parallel, descending hatched bands at the same angle,
which flattens the hierarchy and leaves two unearned voids. The fix for r02 is
compositional, not parametric: break the parity — e.g. let the shadow's teeth
grow *toward the viewer* on a plate that is rotated or foreshortened relative to
the corridor, or make the corridor swallow 60 % of the sheet and reduce the
shadow to a narrow, very loud fringe that overlaps the corridor's near edge
instead of clearing it.

**Three mandatory changes for r02**
1. Break the two-parallel-bands parity: change the shadow's plate so it does not
   repeat the corridor's angle and footprint, and let the two overlap somewhere
   with intent.
2. Spend one of the two voids. The upper band should carry either the input
   stream `u_t` (in x-register, completing input -> state -> horizon) or a much
   larger title mass — not stay empty at 60 mm.
3. Make the lag axis unmistakable at a glance: a dimensioned bracket on the
   shadow reading "LAG 0 … 20 TOKENS" at full type size, not the current 1.35 mm
   ruler ticks that only reward 30 cm.
