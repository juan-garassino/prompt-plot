# VOICING — THE RANK A REACTION CUTS FOR ITSELF
**Essence:** Turing morphogenesis in the Gray-Scott system — a field of two
reacting, diffusing chemicals selects ONE wavelength, set by the diffusion
constants and not by the seed that started it; the piece integrates the PDE five
times from one shared noise realization and builds the result as a RANK OF FLUE
ORGAN PIPES, each cut to eight wavelengths of the pattern wrapped around its
body. **Status:** candidate — `studio/reaction-diffusion/rounds/r02/piece.py`
(`studio_pipe_rank`), round 02 rendered on seeds 7 and 19
(`studio/reaction-diffusion/rounds/r02/NOTES.md`). Round 01 (`MORPHOGENESIS`,
`rounds/r01/piece.py`) is SUPERSEDED: same measurements, no carrier — a relief,
a deck of parameter panels and an S(q) inset, the SCIENTIFIC FIGURE failure that
DESIGN_RUBRIC dimension 6 names under TRANSPOSE, DON'T PLOT. Kept for history.
Not registered in `registry.py`.

## The idea (the true thing)
Two chemicals on a periodic square lattice. `u` is consumed, `v` is produced, by
the autocatalytic step `u + 2v -> 3v`; `u` is fed in at rate `F`, `v` is removed
at rate `F + k`; both diffuse:

    du/dt = Du grad^2 u  -  u v^2  +  F (1 - u)
    dv/dt = Dv grad^2 v  +  u v^2  - (F + k) v

Nothing in those two lines names a length. The reaction terms are local and
pointwise; the diffusion terms are isotropic. And yet a field that starts flat
does not stay flat: it fills with stripes and worms at ONE characteristic
spacing, the same spacing everywhere, reproduced from any starting blotch.

Where does the length come from? From the only place it can: the competition
between a reaction rate (`1/time`) and a diffusion constant (`length^2/time`).
Their ratio is a length squared. So the selected wavelength must scale as
`sqrt(D)`, and a piece that multiplies both diffusivities by `s` — holding
`Du:Dv`, `F`, `k`, the grid, the timestep and the initial array all fixed — must
find its pattern coarsened by exactly `sqrt(s)`.

That is the whole argument, and it is falsifiable on the sheet. **Three plates,
one initial condition, `D x0.4 / x1.0 / x2.0`.** The wavelength is measured, not
asserted: the radially averaged structure factor `S(q)` is taken by FFT and `q*`
is its intensity-weighted first moment; `lambda = N / q*`. Measured
`0.62 : 1.00 : 1.44` against the predicted `0.63 : 1.00 : 1.41` — within 3 % over
a five-fold range of `D`.

**The control is the other half of the argument** and it is the reason this is
not a pretty picture of noise. Gray-Scott's uniform state `u=1, v=0` is linearly
stable; it needs a finite germ to nucleate. So the honest objection is *the germ
set the length*. It did not: running the same `D` with the germ 8 cells wide and
50 cells wide — a factor of six — gives the same wavelength to better than 1 %.
On the plate those two are drawn as two red bars of visibly IDENTICAL length,
directly beneath three red bars of visibly DIFFERENT length. Five bars, one
glance, the whole claim.

The drawable object is the level set. A pen cannot fill a bitmap; it draws an
isoline perfectly, and the isoline of `v` *is* the pattern — the boundary between
the two chemical phases, a family of closed wandering curves. Marching squares
plus endpoint chaining, the same machinery `contour_field` uses, but the field is
a solved PDE and the level is a physical concentration.

## The carrier (what object is this)
A **rank of flue organ pipes**, built exactly — not a relief, not panels, not a
plot.

> **Every pipe is cut to eight wavelengths of the pattern wrapped around it;
> the red ladder up its front is cut from sqrt(D).**

An organ pipe is the everyday object whose entire job is the Gray-Scott
statement: broadband noise in at the mouth, ONE wavelength out, and the
wavelength belongs to the pipe, not to the wind. The mapping is structural, not
a resemblance:

| the reaction | the pipe |
|---|---|
| the seeded noise (white, scaleless) | the wind sheet at the mouth |
| the germ that nucleates it | the chiff that starts it speaking |
| the selected wavelength | the cut speaking length |
| the field that grew | the skin it is wrapped on |
| germ size | how hard you blow |

An organ builder cuts a pipe to length to get a note. Here the reaction cut its
own pipes and the rank is what it cut. A rank of pipes IS a spectrum, which is
why the round-01 S(q) inset has no reason to exist and is gone.

Carriers considered and rejected: a leopard pelt, a fingerprint, a seashell, a
meandering river (all are OTHER INSTANCES of pattern formation — the subject's
own discipline, illustration rather than transposition); a colonnade (its
intercolumniation is set by a module, but nothing goes INTO it, so the germ
control has no home); an aeolian harp (right mechanism, but strings are
one-dimensional and the field has nowhere to live); a Damascus billet (folding
sets the layer spacing, but folds are not a diffusion ratio).

## Pen-plotter visual (our engine)
One axonometric basis for the whole sheet (`A 0.500 / CD 0.260 / WY 1.000`) —
chosen once for a tall standing object: verticals unforeshortened, ground plane
raked. A pipe that must be smaller shrinks its world FOOTPRINT.

- **THE EXPERIMENT IS THE SKYLINE.** Five pipes, a crossed design, left to
  right: `D 0.4` | `GERM 8`, `D 1.0`, `GERM 50` | `D 2.0`. The three middle
  pipes share D and differ in germ by 6x — they come out the SAME HEIGHT, a flat
  plateau, over three wildly different red germ masses. The two outer pipes
  share the germ and differ in D — they step down and up. Reading the skyline is
  reading the result; no caption does it for you. The skyline also SHAPES the
  negative space: the blank upper-left the staircase opens is the quiet zone.
- **THE FALSIFICATION IS ON THE PIPE.** The black stripes on each body are the
  MEASURED field; the red ladder is the PREDICTION, eight rungs at
  `lambda(D 1.0) * sqrt(D / D 1.0)`. On the reference pipe the eighth rung lands
  on the cut. On the others it misses by the measurement error, about 2 % over
  eight wavelengths — a millimetre and a half, the 30 cm tier. If sqrt(D) were
  wrong the ladder would not fit the pipe.
- **The wrap.** The domain is periodic in both directions — a torus — so
  wrapping it round a cylinder is not a liberty, it is the literal topology of
  the simulation: the pattern closes with no seam. Isolines are contoured
  directly on the (theta, h) surface grid with `kit._marching_squares`, so they
  crowd toward the silhouettes on their own and the foreshortening IS the tone.
- **The chest.** A slab cropped at both sheet edges, in its own frame
  `E1 = (1,-0.85)` along the rank (each pipe a little nearer than the last, so
  the occlusion order is real) and `E2 = (1,1)` toward the viewer (straight down
  the screen). On its top face: the wind, then the germs. On its front face: the
  engraved nameplates.
- **The wind.** The shared noise realization contoured at its own zero level,
  coarse-grained so the dust is plottable, running under every foot and off both
  edges. White noise is isotropic, so laying it along the chest is not a
  distortion. `ONE WIND / NO PITCH IN IT`.
- **The germs.** Red masses at half the field scale (stated), serpentine-filled,
  one in front of each pipe: three equal, one tiny, one huge.
- **Hidden line.** A projected vertical cylinder is convex (an ellipse Minkowski
  a vertical segment), so each pipe's silhouette is an exact half-plane
  intersection and the further pipes are clipped outside the nearer ones with
  `engine/geometry.py`. No z-buffer is hand-rolled in the piece.

## Palette
Cream paper. **black** = every pipe, every stripe, the chest, the wind, all type.
**red** = what was PUT IN and what was PREDICTED, and nothing else: the germ
masses on the chest and the sqrt(D) ladders on the pipes. Two pens, one swap.
Type takes its own nib on a four-pen build; on three it falls back to black, and
red never carries a glyph. Diameters follow the organ builder's scaling rule
(`d ~ L^0.72`, Toepfer) — carrier grammar, not data, and said so on the sheet.

## Annotations
`VOICING`, `THE RANK A REACTION CUTS FOR ITSELF`,
`EVERY PIPE IS EIGHT WAVELENGTHS OF THE PATTERN WRAPPED ROUND IT.`,
`THE LADDER IS CUT FROM SQRT D.`,
`ONE WIND`, `NO PITCH IN IT`, `RED WENT IN`, `BLACK CAME OUT`,
nameplates `D 0.4 / G 8 / D 1.0 / G 50 / D 2.0` each over its measured lambda,
and the parameter column `GRAY-SCOTT`, `DU 0.16  DV 0.08`, `F 0.030`, `K 0.057`,
`GRID 128  PBC`, `DT 0.75`, `STEPS 7000`, `LAMBDA FROM S Q`,
`LADDER MISS 3 PCT`, `TOEPFER SCALING`, `LENGTH IS DATA`, `GERMS AT HALF SCALE`.
The stroke font carries only `A-Z 0-9 - .` — no `=`, `/`, `+`, `:`.

## Reference prompt
A fine-line engraving on cream: five tall organ pipes standing in a row on a
wind-chest, feet conical, mouths cut, bores open at the top — but their metal is
patterned all over with a labyrinth of worms that gets coarser as the pipes get
taller, and short red rungs climb the front of each one. Under them a band of
structureless speckle runs off both edges of the sheet, and in front of that a
row of solid red blocks, three the same, one tiny, one enormous. The pipe tops
make a staircase: low, then three level, then high.

## Build notes
Explicit forward Euler, 5-point periodic Laplacian, float32, `dx = 1`. Stability
needs `dt * max(Du) <= 0.25`; at `Du = 0.16` and `s = 2.0` that caps `dt` at
0.78, so `dt = 0.75` and `s = 2.05` diverges — the scale range is bounded by the
integrator, not by taste. `F = 0.030, k = 0.057` is in the labyrinth lobe of the
Pearson diagram. The germ is off-centre (0.455, 0.415) because a centred square
seed on a periodic box prints its own four-fold symmetry into the pattern and the
plate reads as decoration. `q*` is the first moment of `S(q)` over the peak band,
NOT an argmax: a bare argmax on a 128-box spectrum jitters a whole bin between
noise realizations and turned a 2 % agreement into a 7 % miss. Contours:
`kit._marching_squares` + `kit._chain_segments`, decimated to ~0.5 cell.
Engine: `Scene3D` with `fit="none"` (the layout is authored in paper mm),
`halo_labels` for all type, `lines(mode="pause_resume")` with one shared
`Occupancy` for the relief, `poly` for everything flat, and
`engine/geometry.py` `HalfPlane`/`Rect`/`clip` for the projection-line occlusion
and for the exact crop at the sheet edge. Five integrations per render (~15 s on
an Intel Mac). Seed is a fine-tune only — it reshuffles the maze, not the
measurement (λ stable to ~1 % across seeds 3, 7, 19). This is a COMPOSITION
(archetype B), not a parametric family.

## Next round
The rank stands on a chest that is three long lines; it is the thinnest part of
the object and it is doing a lot of work (it carries the wind, the germs and the
nameplates). Either build it properly — rackboard, toe holes, a visible
wind-trunk entering from the cropped edge — or drop it to a single datum line
and let the pipes float on the wind band. Second: the pipes are racked in ONE
row at almost the same depth, so the occlusion machinery is barely exercised;
a second row of the same five behind, offset, would give real depth and let the
plateau be read as a shared top edge through the gaps. Third: `D` appears only
as a two-character nameplate. If the wind trunk were drawn as five ducts of
visibly different bore feeding the five pipes, `D` would enter the object too,
and the last piece of caption could go.
