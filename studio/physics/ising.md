# CRITICAL — ORDER AT EVERY SCALE
**Essence:** the 2D Ising phase transition — at Tc = 2/ln(1+√2) the correlation
length diverges and magnetic domains exist at every size at once; the piece draws
the DOMAIN WALLS of a real Monte-Carlo configuration, with the pen weight of each
wall keyed to the size of the domain it encloses. **Status:** candidate —
`studio/ising/rounds/r01/piece.py` (`ising_critical`), round 01 rendered and
critiqued (`studio/ising/rounds/r01/NOTES.md`); not registered in `registry.py`.

## The idea (the true thing)
A square lattice of ±1 spins with one rule only: neighbours prefer to agree
(H = −J Σ⟨ij⟩ s_i s_j). Nothing in that rule mentions a length scale, yet at one
exact temperature the system spontaneously grows structure at EVERY length scale.
Below Tc the lattice picks a direction and orders (one sea, a few inclusions);
above Tc thermal noise wins (dust, correlated over 1–2 sites); at
**Tc = 2/ln(1+√2) = 2.269185…** (Onsager 1944, exact) the correlation length
diverges and structure is self-similar under coarse-graining.

The drawable object is NOT the spins (a grid of filled squares is a failure —
and it is not line work). It is the **domain walls**: the dual-lattice edges
between disagreeing neighbours. They form closed, nested, wandering curves, which
is exactly what a pen wants to draw.

## How the physics becomes pen (both rules exact)
1. **LINE WEIGHT = the SCALE of the domain the wall encloses.** Passes keyed to
   min(|A|,|B|) over the two domains a wall separates: 1 pass under 10 sites, 2
   under 120, 3 above. At Tc all three rungs are populated at once — scale
   invariance *drawn*, not asserted. This is what makes the hero read as
   continents / islands / specks rather than uniform noise.
2. **RED = the top rung** — min(|A|,|B|) ≥ 3 % of the lattice. In the symmetric
   sector at Tc that is one enormous fractal interface between the two coexisting
   phases: the only long-range object on the sheet.

### ⚠ The rule this brief originally proposed is WRONG — do not restore it
The first draft claimed "red iff a wall bounds a domain ≥6 % of the lattice"
produces zero red below AND above Tc. **Measured at L = 128: false.** The largest
2D Ising *spin* cluster is still 50 % at 1.15 Tc and 36 % at 1.6 Tc, with 3–4
domains over 6 % well above Tc — spin clusters percolate *at* Tc (Coniglio et
al.), so "a big domain" is not a critical signature. Also measured and rejected:
wrapping/spanning domains (the second giant domain essentially never wraps),
hull box-counting dimension (monotone in T, not peaked at Tc), and the log–log
domain-size spectrum (the Tc curve is not the straightest — R² 0.985 vs 0.995 at
1.6 Tc). See NOTES.md for the numbers.

**Declared restriction:** at Tc a finite lattice fluctuates (|m| measured in
[0.05, 0.71] over 9 seeds) and a magnetised critical configuration has no second
macroscopic domain, so nothing to ink. The hero is drawn from the **symmetric
sector** — 16 decorrelated Wolff samples from the one seeded chain, least
magnetised kept. Printed on the sheet as `SYMMETRIC SECTOR` with the resulting
|m|. Robust on seeds 3, 7, 13.

## Pen-plotter visual (our engine)
- **Hero (dominant, 0.72 W square, flush to the right and top drawable edges so
  it crops at two frame edges):** the exact Tc configuration's walls, chained into
  continuous curves, weight-tiered as above, red interface. Title set over the
  field on `Scene3D.halo_labels` so the geometry opens around it. Corner brackets
  mark the two FREE edges (the other two are the crop) and give the blow-up
  something to land on.
- **The deck (subordinate, lower-left):** five axonometric plates on ONE shared
  basis, stepping toward the viewer — T/Tc = 0.75, 0.90, **1.00**, 1.20, 1.80.
  Plate spacing is derived from the real projected extent
  (`span = 4d + 1 + (0.65 + zr)` in units of `a`), never eyeballed. Overlap is
  resolved with EXACT parallelogram `Region` clipping (`engine/geometry.py`), not
  z-order fudging. The Tc plate is **empty**: a dotted red outline with its
  content pulled out — because its content is the hero. **The deck is one pen:**
  at L = 24 a 3 % domain is 17 sites, not macroscopic in any meaningful sense, so
  the red rung belongs to the hero alone.
- **The blow-up:** dotted projection lines (house law: dotted, NEVER arrows) from
  the ghost plate to the hero's BOTTOM edge — the edge that faces the deck. The
  two rays are found automatically as the bridging edges of the convex hull of
  {ghost corners, hero bottom corners}, then clipped outside every plate and
  outside the hero, short stubs culled.
- **Temperature rule:** lives in the SAME world basis at z = +0.72, in front of
  the plates, one tick per plate, the Tc tick red and taller. No plumb lines.
- **Footer:** run parameters, the measured unsatisfied-bond fraction against the
  exact Onsager value (1 − 1/√2)/2 = 0.146447, the drawn configuration's |m| and
  domain count, and both pen rules in words. Plus a micro-chart: the **exact
  Onsager/Yang m(T)** curve with the measured plate values on it and a red
  dashed line at Tc — the knee is the transition.
- **Quiet zones:** the gutter left of the hero, and the block between the deck
  and the micro-chart.

## Palette
Cream paper. **black** = every wall below the top rung, all type, all furniture.
**red** = scarce and loud: the critical interface, the ghost plate, the Tc tick,
the Tc line on the micro-chart. Two pens, one swap.

## Annotations
`CRITICAL`, `DOMAIN WALLS AT EVERY SCALE`, `ONE RULE   NO LENGTH SCALE`,
`T IN UNITS OF TC` + `0.75 0.90 1.00 1.20 1.80` on the rule (`1.00` red),
`WOLFF AND METROPOLIS  L 128  PBC  SEED n  SYMMETRIC SECTOR`,
`TC 2.269185  ONSAGER 1944  EXACT`,
`UNSATISFIED BONDS  CHAIN ..  ONSAGER 0.1464`,
`THIS CONFIGURATION  M ..  .. DOMAINS`,
`LINE WEIGHT  THE SIZE OF THE DOMAIN THE WALL ENCLOSES`,
`RED  BOTH DOMAINS OVER 3 PCT OF THE LATTICE`, `ORDER PARAMETER  EXACT  PLATES L 24`.
The stroke font only has `-.0123456789A-Z` — no `=`, `/`, `+`, `>`, `|`.

## Reference prompt
A fine-line science poster on cream: one huge square maze of wandering closed
curves — a coastline map with continents, islands and specks all at once, one
long coastline inked in red — with a small fanned deck of five tilted plates
below left running from almost-blank to dust, one plate empty, dotted projection
lines blowing that empty plate up into the huge field.

## Build notes
Wolff single-cluster (P_add = 1 − e^(−2β)) interleaved with **checkerboard**
Metropolis sweeps (numpy; the sublattice update is exact because same-colour
sites are conditionally independent). Wolff is what defeats critical slowing down
— Metropolis alone needs τ ~ L^2.17 sweeps at Tc. Periodic boundaries; wrap bonds
are counted for the energy but never drawn, so the sheet is a window onto the
torus. Domains are exact 4-connected components (BFS); wall segments are chained
with `kit._chain_segments`. Engine: `Scene3D` (halo labels, fit="none", halo-aware
`poly`), `engine/geometry.py` `HalfPlane`/`Intersect`/`clip` for ALL occlusion and
`geo.offset` for the multi-pass weights, `kit` for type and strokes. Seed is a
fine-tune only — this is a COMPOSITION (archetype B), not a parametric family.

## Next round
The deck is the weak half: five 47 × 26 mm plates carrying less than they could,
two of them nearly empty. Either enlarge the world footprint (fewer plates, same
basis) or replace the deck with the **block-spin renormalisation cascade** —
coarse-grain the SAME Tc configuration by factors of 2 and show the successive
levels are statistically identical. That is the sharpest available statement of
scale invariance and would give the critical plate a structural difference no
neighbouring temperature can imitate.
