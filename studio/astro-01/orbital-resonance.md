# ORBITAL RESONANCE — SMALL INTEGERS EMPTY THE BELT
**Essence:** where an asteroid's period is a small-integer fraction of Jupiter's,
every conjunction happens at the same place in its orbit, the tugs add instead of
cancelling, the semimajor axis swings — and the belt is swept clean. The gaps are
not missing data; they are the result. **Status:** candidate — `studio/orbital-resonance/rounds/r01/piece.py`
(`orbital_resonance_belt`), not registered in `promptplot/`.

## The idea (the true thing)

Jupiter carries 1/1047 of the Sun's mass, and it is enough. In the planar circular
restricted three-body problem (Sun + Jupiter on a fixed circular orbit + a massless
test asteroid) an orbit whose mean motion satisfies **n / n_J = p / q** with p, q
small integers is *locked*: the geometry of successive Sun–Jupiter–asteroid
conjunctions repeats instead of precessing, so Jupiter's pull is applied over and
over at the same phase. The asteroid's semimajor axis then **librates** — it swings
back and forth across a band instead of holding a lane — and on Myr timescales the
coupled eccentricity growth throws it onto a planet-crossing orbit. The survivors
are the orbits that keep their lane.

Kirkwood (1866) saw the result in the catalogue before anyone could integrate it:
the belt is empty at

| ratio | a = a_J (q/p)^(2/3) |
|---|---|
| 4:1 | 2.065 AU |
| 3:1 | 2.501 AU |
| 5:2 | 2.825 AU |
| 7:3 | 2.958 AU |
| 2:1 | 3.278 AU |

with the 2:1 forming the belt's hard outer edge. **The emptiness is the
measurement.** That is what makes this a pen subject and not a chart subject: the
only mark the physics asks for is the mark the pen does not make.

Governing relations actually used:
- equations of motion, barycentric inertial frame, G(M☉+M_J)=1, a_J=1, μ=9.5388e-4:
  **r̈ = −(1−μ)(r−r☉)/|r−r☉|³ − μ(r−r_J)/|r−r_J|³**, r☉ = −μ(cos t, sin t),
  r_J = (1−μ)(cos t, sin t).
- osculating semimajor axis from heliocentric vis-viva:
  **a = 1 / (2/|r_h| − |v_h|² / (1−μ))**.
- mean semimajor axis = a boxcar of one orbital period; **libration width
  Δa = max ā − min ā** over the run. This is the whole signal.
- resonance radius from arithmetic alone: **a_res = a_J (q/p)^(2/3)** (Kepler III).

## Pen-plotter visual (our engine)

A **map, not a plot**: the belt seen from above, drawn as ~220 real orbits.

- The Sun sits off the bottom edge; ONE radial scale (mm per AU) governs every mark
  in the piece — there is no second scale and no scale break, the flat-view analogue
  of the house "one shared axonometric basis".
- Each surviving test orbit is drawn as **one fine arc at its own mean semimajor
  axis**, sweeping the full page width and cropping at both side margins. Uniform
  comb in, so any structure on the page was carved by gravity, not by the sampler.
- **Dash duty encodes the measured libration width.** An orbit that holds its lane
  is solid; as the libration grows the arc frays into dashes; past the threshold the
  orbit is not drawn at all. The gaps therefore arrive with physically correct soft
  shoulders — fray, fray, nothing — and the hard voids are pure cream paper.
- Five **dotted crimson arcs** at a_J (q/p)^(2/3) — the arithmetic prediction, laid
  over the dynamical result. Four of them land inside a void: the integers found the
  emptiness without any integration at all. That coincidence, at line-width
  precision, is the piece.
- The **2:1 is the outer edge**: beyond 3.18 AU nothing survives, and the top quarter
  of the sheet is blank. The largest empty region in the composition is a result.
- Depth: **declared flat.** The subject is coplanar (belt inclinations mostly < 20°,
  Jupiter 1.3°) and it is a radius that is empty — any axonometric tilt would
  foreshorten the one quantity the piece exists to show. Layering is delivered by
  halo knockouts (type and the scale ray carve the field) and by the density ramp.
  Style: RADIAL DATA-VIZ / INFORMATION ARCS (STYLES.md §5), which is flat by canon.

## Palette

Cream paper. **Black** = the integrated orbits (the dynamics). **Crimson** = the
arithmetic — the five resonance radii, dotted, and nothing else; under ~250 mm of
stroke against ~25 m of black. **Type/furniture** on its own pen layer with halos
(physically a fine black nib; index 2 so it can be swapped for a 0.2 mm).
Three pens, two swaps.

## Annotations

Naked spaced caps on the grid — no boxes, no arrows, no leader lines. Title
`ORBITAL RESONANCE` flush-left in the outer void; a one-line method statement under
it. The ratio of each gap (`4 : 1`, `3 : 1`, `5 : 2`, `7 : 3`, `2 : 1`) set inside
its own void, staggered so they never stack. One dotted radial scale ray with AU
ticks (canon 5 makes the radial tick axis and scale labels mandatory). Footer: μ,
integrator, step, run length, e₀, N, and the honest caveat that only Jupiter is
present.

## Reference prompt

A cream sheet filled from the bottom edge by a vast field of fine concentric
arcs — hundreds of orbits around a sun just off the page — the field fraying into
dashes and then into nothing along four clean canyons that run the whole width, a
thin dotted crimson line lying exactly along the middle of each canyon, the whole
band stopping dead two thirds up the sheet with a quarter of the page left as bare
paper, spaced-caps type flush left in the emptiness.

## Build notes

Velocity-Verlet, dt = 0.02 (≈130 steps per asteroid orbit), 300 Jupiter periods,
~220 test particles vectorised in one numpy array — ~8 s, seeded phases only
(initial mean anomaly and longitude of perihelion), e₀ = 0.15 fixed so the comb is
uniform in everything but a. Drop rule: an orbit is not drawn when its libration
width exceeds 3 ring pitches OR 2.4× the local non-resonant background (a running
median over ±0.22 AU, which grows with a as Jupiter is approached); the void mask is
then morphologically closed so the stable island centre inside a separatrix does not
leave a stranded ring. Nothing is hand-placed. Not modelled, and said so in the
footer: Saturn, the ν₆ secular resonance that cuts the belt's inner edge, and the
Myr-scale chaotic clearing itself — the piece shows the lock, not the removal.
