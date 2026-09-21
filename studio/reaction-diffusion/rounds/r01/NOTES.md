# MORPHOGENESIS — round 01 notes

Piece: `studio/reaction-diffusion/rounds/r01/piece.py`, entry
`studio_reaction_diffusion(rng, bounds, colors=3)`.
Brief: `studio/physics/reaction-diffusion.md`.
Render:
`.venv/bin/python scripts/render_candidate.py studio/reaction-diffusion/rounds/r01/piece.py --fn studio_reaction_diffusion --seed 7 --paper a4 --out ~/Downloads/pp_reaction_diffusion_v8.png`
Nothing under `promptplot/` was modified.

---

## 1. The PDE, exactly as integrated

Gray-Scott, two morphogens on a periodic `N x N` square lattice, `dx = 1`:

    du/dt = Du * lap(u)  -  u v^2  +  F (1 - u)
    dv/dt = Dv * lap(v)  +  u v^2  - (F + k) v

`lap` = the 5-point stencil `u[i+1,j] + u[i-1,j] + u[i,j+1] + u[i,j-1] - 4 u[i,j]`
built from `np.roll` (periodic in both axes — the sheet is a window onto a torus).
Time integration is explicit forward Euler in float32, in place.

| parameter | value |
|---|---|
| grid `N` | 128, periodic |
| `F` (feed) | 0.030 |
| `k` (kill) | 0.057 |
| `Du : Dv` | 0.16 : 0.08 (fixed ratio 2:1) |
| diffusion scale `s` | **0.4, 1.0, 2.0** (`Du*s`, `Dv*s`) |
| `dt` | 0.75 |
| steps | 7000 (t = 5250) |
| initial state | `u = 1`, `v = 0` everywhere |
| germ | square half-width `N/12 = 10` at (0.455, 0.415) of the box, set to `u = 0.50, v = 0.25` |
| noise | Gaussian `sigma = 0.02`, added to `u`, subtracted from `v`, ONE realization shared by all runs |
| control runs | same everything, `s = 1.0`, germ half-width 4 and 25 (8 and 50 cells wide) |

Five integrations per render, ~15 s total on this machine.

**Numerical stability.** Explicit 2D Euler needs `dt * D / dx^2 <= 0.25`. With
`Du = 0.16` and `s = 2.0`, `dt <= 0.78`. Measured: `s = 2.05` at `dt = 0.75`
diverges (`lambda` came back as `1.28e8`). So `dt = 0.75` and `s_max = 2.0` — the
five-fold range of `D` on the plate is set by the integrator, not chosen.

**The claim and the measurement.** Scaling both diffusivities by `s` is an exact
similarity of the PDE under `x -> x sqrt(s)`, so `lambda(s)/lambda(1) = sqrt(s)`.
`lambda` is measured from the radially averaged structure factor `S(q)` of
`v - <v>` (FFT, `bincount` over integer `|q|`), with `q*` the intensity-weighted
FIRST MOMENT over `[0.55 q_peak, 1.85 q_peak]` after a 3-bin smooth.

    lambda (cells)      7.5    12.1    17.4
    ratio measured     0.62    1.00    1.44
    ratio sqrt(D)      0.63    1.00    1.41      -> within 3 %

Across seeds 3 / 7 / 19 the three wavelengths moved by under 1 % (7.5, 12.1–12.2,
17.4). The seed reshuffles the maze, not the measurement.

**The germ control** (the thing that makes this an argument rather than a
picture). Gray-Scott's homogeneous state is linearly STABLE — it needs a finite
germ to nucleate, so "the seed set the length" is a real objection. Measured at
`s = 1.0`, `steps = 8000`, germ half-width swept 6x:

    germ half-width   4      8     11     16     24
    lambda        12.22  11.78  11.92  12.70  11.71

No trend, spread ±4 %. Two of those runs (half-width 4 and 25) are re-run inside
the piece and drawn as the two identical red bars under the three different ones.

---

## 2. Engine primitives used

- `Scene3D(fit="none", tip=0.35)` — the layout is authored directly in paper mm,
  so no rescue-fit is wanted.
- `Scene3D.halo_labels` — every glyph on the sheet; the relief, the frames and
  the dotted lines all open around the type.
- `Scene3D.lines(mode="pause_resume", occupancy=<shared>)` — the hero's four
  terraces are emitted top-down through ONE `Occupancy(0.82 mm)`, so the nearest
  ridge keeps its ink and the ones behind pause and resume. This is the hidden
  line: no z-buffer was hand-rolled in the piece (house law).
- `Scene3D.poly` — every flat polyline (plate frames, contours on the deck,
  dotted segments, calipers, the `S(q)` axis), halo-aware.
- `engine/geometry.py` `HalfPlane` / `Intersect` / `Rect` / `clip` — the
  projection lines are clipped exactly outside all five plate parallelograms
  (built as half-plane intersections from the rhombus corners), and every
  polyline is clipped exactly to the drawable rect so the hero's crop at the
  right paper edge is a real cut. Bounds violations: 0.
- `kit._marching_squares` + `kit._chain_segments` — the contouring machinery
  `contour_field` uses, reused unchanged.
- `kit._stroke_text` / `_text_width` / `_spaced` / `plus_mark` / `swatch_bar`.

Shared axonometric basis `A 0.500 / CD 0.260 / WY 0.620`, one set of constants
for the whole sheet. Plate spacing is derived, not eyeballed: two
same-orientation rhombi with screen half-diagonals `(A_i, B_i)`, `(A_j, B_j)` are
disjoint iff `|dx|/(A_i+A_j) + |dy|/(B_i+B_j) >= 1` (their Minkowski sum is the
rhombus of summed half-diagonals). `_rhombi_clear` asserts that for all ten pairs
including the hero, and raises if a layout edit ever breaks it.

Plot cost: 23.5 k commands, 8.8 m of draw, 7.0 m of travel, 2 pens, 1 swap.

---

## 3. What was missing / what fought back

- **A surface mesh under the hero was wrong.** Round-01a rendered the hero as
  `Scene3D.surface()` (z-buffer hidden line) with isolines laid back on it. It
  looked like crumpled foil: the 34x34 mesh aliased against a 46-cell window and
  buried the contours. Dropped entirely — the terraced level sets ARE the relief,
  and they are what a pen wants.
- **A centred square germ prints its own symmetry.** The first fields were
  bilaterally symmetric bullseyes and read as ornament. Moving the germ off
  centre fixed it; shrinking it (tried `N/16`) did not — it under-nucleated, the
  front never filled the box and `D 2.0` came out as unconverged blobs.
- **`argmax` on `S(q)` is not a measurement.** The integer-bin peak jitters by a
  whole bin between noise realizations; the printed agreement swung between 2 %
  and 7 % purely on the rng seed. The first-moment estimator fixed it (spread
  < 1 % over four seeds) and is the standard definition anyway.
- **The stroke font has no `=`, `/`, `:`, `+`.** Every annotation is written
  around that, and every line was width-checked against the 189 mm drawable
  before it went in — the first render overflowed `MORPHOGENESIS` off the sheet
  because spaced caps double the character count.
- **Not built:** a dispersion-relation panel. The linear growth rate `sigma(q)`
  would be the most direct statement of wavelength selection, but Gray-Scott's
  uniform state is linearly stable, so `sigma(q) < 0` everywhere and the honest
  curve says nothing. The Brusselator has a real Turing bifurcation and an
  analytic `q_c`, but its `Dv/Du = 8` forces `dt ~ 0.006` and ~30 k steps per
  field — 10x the render budget. Deferred, noted in the brief.

---

## 4. Self-critique against DESIGN_RUBRIC.md

Honest scores, from viewing the png only.

| dimension | score | why |
|---|---|---|
| 1 Hierarchy | 8 | hero 132 mm against 46 mm plates — 2.9:1 linear, ~8:1 area. At 3 m the relief slab is the only thing; at 1 m the deck's diagonal; at 30 cm the calipers and the `T=0` dust. |
| 2 Grid & alignment | 8 | title, caliper block and footer all flush left on `x0+1`; the four deck plates on one straight world line; hero on the same basis; spacing derived and asserted. |
| 3 Tension & asymmetry | 8 | lower-left to upper-right diagonal, hero crops at the right sheet edge, nothing centred, the deck runs off under the hero's mass. |
| 4 Negative space | 7 | the `T=0` plate is deliberately near-empty and the band between deck and hero is a shaped void crossed only by dotted lines — but the pocket between the calipers and the deck (x 60–140, y 140–175) is leftover, not composed. |
| 5 Craft for pen | 7 | 2 pens, 1 swap, 8.8 m. The `D 0.4` plate is the tightest thing on the sheet: 2.7 mm per wavelength, contour pairs ~1.3 mm apart. Over the 0.8 mm floor, but it is the first thing that would muddy with a fat nib, and it has not been plotted yet. |
| 6 Concept legibility | **6** | the weakest. The phenomenon lands — "a pattern, at three spacings, from one blank start" — and the five red bars make the claim without prose. But the *cause* (diffusion) is carried by three two-character labels and the title, not by the image, and the dominant mass is not the element that argues. A stranger reads topographic art first, physics second. |
| 7 Depth | 8 | exploded axonometry on one shared basis, terraced relief, occlusion by shared occupancy, the near plate's tone heavier than the far. Not flat, and not declared flat. |

**Average ~7.4, one dimension at 6 — this does NOT clear the bar** (avg >= 8, none
below 7). It is a round-01 candidate, not a ship.

**Single biggest weakness:** the hero is the biggest thing on the sheet but not
the arguing thing. Fix, for round 02: integrate one field with a smooth spatial
ramp in `D(x)` so a single continuous labyrinth coarsens visibly from edge to
edge, put that in the hero, and measure it at three stations with the same red
calipers. The argument then IS the dominant mass, the deck can shrink to a
control strip, and the `S(q)` inset — the only element that risks reading as a
textbook axis plot, which the rubric fails outright — can go.

**Three mandatory changes if this is kept as-is:** (1) compose the dead pocket
between the calipers and the deck, or close it by moving the caliper block down
onto the deck's baseline; (2) give the `D 0.4` plate breathing room — either
a larger world footprint for all four plates or a coarser contour decimation, so
the tightest spacing on the sheet is over 2 mm; (3) kill or radically shrink the
`S(q)` inset and let the five calipers carry the measurement alone.
