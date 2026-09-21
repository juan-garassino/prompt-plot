# THE DOUBLE SLIT — WHAT THE CROSS TERM TAKES AWAY

**Essence:** two coherent amplitudes land on one screen; the quantum law is
|ψ₁+ψ₂|², the which-path law is |ψ₁|²+|ψ₂|², and their difference — the cross
term 2·Re(ψ₁ψ₂*) — is drawn NOWHERE. It is the blank paper between the ridges.
Interference does not create probability; it only moves it. **Status:** candidate, round r01
built at `studio/double-slit/rounds/r01/piece.py` (`double_slit_cross_term`),
A4 portrait, 2 pens, ~8.6 m of ink; NOT registered in `GENERATOR_REGISTRY`.

## The idea (the true thing)

Sibling to `studio/quantum-01/dossier.md` (Tonomura buildup, VT-1) but a
different visual truth — the dossier's **VT-3**, promoted to its own plate. VT-1
is *accumulation*; this is *contrast*. Nothing here is a restyle of the
`interference_field` generator (that is a ripple-tank scanline displacement with
seeded drops — decoration; this is a computed diffraction plate).

**The apparatus is stated, not cited.** An optical bench anyone can build:
λ = 633 nm, slit width a = 100 µm, separation d = 300 µm, screen L = 2.000 m,
one quantum at a time. No measured data is claimed, so no paper is misquoted;
what is exact is the COMPUTATION, exactly as in `black_hole` (exact Luminet
solver, chosen parameters). **d = 3a is chosen deliberately**: the third principal
maximum then falls exactly on the first envelope zero and is annihilated — the
classic *missing order*, a real, exact, and beautiful fact that also gives the
plate five broad legible fringes instead of nine cramped ones.

**Not the Tonomura biprism.** This is a real two-aperture screen, so the
single-slit envelope is genuinely there and the dossier's "no sinc²" rule — which
is specific to a biprism, which has no slit width — does not apply. Stated in the
colophon so the science critic does not cross-apply it.

Exact computation, Luminet/`black_hole` standard. For a slit of width *a*
centred at *xⱼ*, an observation screen at distance *L*, wavelength *λ*, k = 2π/λ,
the amplitude at screen position *x* is the **Rayleigh–Sommerfeld (Fresnel–
Kirchhoff) integral**, evaluated by Gauss–Legendre quadrature — no far-field
approximation:

    ψⱼ(x) = ∫[xⱼ−a/2 … xⱼ+a/2]  exp(i·k·(r−L)) · (L/r) · r^(−1/2)  dx′
    r  = sqrt(L² + (x−x′)²)
    r−L = (x−x′)² / (r+L)          ← used verbatim; no catastrophic cancellation

The common piston phase exp(ikL) divides out of every intensity. Then, from the
SAME two complex arrays:

    I_quantum(x)   = |ψ₁ + ψ₂|²          paths indistinguishable
    I_classical(x) = |ψ₁|² + |ψ₂|²       which-path known
    Δ(x)           = 2·Re(ψ₁ ψ₂*)        the cross term = the difference

In the far field these collapse to the textbook closed form
I ∝ sinc²(πa sinθ/λ)·cos²(πd sinθ/λ) — which the piece uses only as a
**verification oracle**, never as the drawn quantity (the r01 run agrees to
~1e-3 relative, reported in NOTES.md). Two exact consequences do the art:

1. `I_quantum = 2 · I_classical · cos²(πd sinθ/λ)` — the classical curve is
   exactly the **local mean** of the quantum one. Peaks reach 2×; nulls reach 0.
2. `∫Δ dx ≈ 0` over the central lobe — every unit of probability the cross term
   removes from a trench it puts on a ridge. Conservation, drawn as geometry.

The misconception corrected without a word of argument: *"interference adds
something."* It does not. The two plates carry the same ink budget; the second
one just spends it in fewer places.

## Pen-plotter visual (our engine)

A SHORT declaration on `Scene3D`. Two reliefs of the same quantity (landing
probability as height) in **ONE shared axonometric basis** — same A, CD, WY for
both; the subordinate plate shrinks its world FOOTPRINT along the free axis
only, never the projection constants. Both share the identical screen-x crop and
the identical mm-per-unit-intensity height scale, so the 2:1 peak ratio on paper
IS the physics, not a layout choice.

- **Free axis:** the pattern is invariant along the slits, so translating a plate
  along world-z is physically meaningless — which makes it the honest axis for
  staging. Stage separation is derived from the real projected extent
  (`Zc > Zw + Zh + clearance`), so the plates cannot interpenetrate.
- **HERO (lower, dominant):** `I_quantum` as a deep corrugated relief. Tall thin
  fringe blades; the engine's native hidden-line z-buffer lets near blades occlude
  far ones, and `ScreenThin` handles the crowding. The surface touches the floor
  exactly at the nulls.
- **SECOND (upper-right, ~1/3 the depth):** `I_classical` as a shallow smooth
  dune. No holes anywhere. Same width, same crop, half the height.
- **Crop:** exactly the central envelope lobe, |a·sinθ| ≤ λ. Both surfaces reach
  zero at both edges, so each relief is a closed form standing on its own floor
  and the plate edge is a physical fact rather than a framing decision — and it is
  the place where the missing third order should have been.
- **The crimson is the argument.** The zero set of `I_quantum` (found by
  golden-section minimisation on the computed intensity, never from the cos²
  formula) is ruled on the ground plane of BOTH plates, stepping forward off the
  front edge onto blank paper. From each rule a **plumb** rises to the surface
  above it. On the which-path dune the plumb is a tall bar with a cap: the
  probability that would have landed there. On the interference comb the surface
  is already on the ground, the plumb has zero length, and nothing is drawn. Same
  mark, same positions, two behaviours — that absence is the piece.
- **Axonometry, house law:** registration is by **dotted projection lines along
  constant world-x**, which in this basis is exactly the line of constant screen
  position — the physically correct registration. NEVER arrows. Black at the
  plate corners and the optic axis; red between the stations at the null
  positions.
- **Forbidden** (inherited): no trajectories, no source, no slit icon, no
  apparatus, no drawn ψ or envelope curve floating in space, no axes, no ticks,
  no legend boxes. The subject is the probability landscape, not the machine.

## Palette

Cream paper. **Two pens.** Pen 0 BLACK — both reliefs, ground lines, front rims
(2 passes), all type, black projection dotting at the envelope zeros and the optic
axis. Pen 1 CRIMSON — ONLY the zero set of |ψ₁+ψ₂|²: twelve ground rules, the
plumbs that stand on them, six dotted registration lines, and two lines of key
type. Scarce and loud. Blue/green are not needed and are not used: the piece is a
binary contrast and a third hue would invent a third category. The blank paper is
the third colour, and it is literally the cross term.

## Annotations

Own pen layer, halos reserved before any mesh is drawn (`Scene3D.halo_labels`).

- Title (giant spaced caps, flush left): `THE DOUBLE SLIT`
- Standfirst: `INTERFERENCE REDISTRIBUTES  IT DOES NOT CREATE`
- Stage 1: `1 · WHICH PATH` / `PSI1^2 + PSI2^2` / `PATHS DISTINGUISHED`
- Stage 2: `2 · INTERFERENCE` / `|PSI1 + PSI2|^2` / `PATHS INDISTINGUISHABLE`
- Right block: `THE DIFFERENCE 2 RE(PSI1 PSI2*) IS DRAWN NOWHERE` /
  `IT IS THE PAPER BETWEEN THE RIDGES` / `INTEGRAL = 0`
- Red key, once: `RED — WHERE THE PARTICLE NEVER LANDS`
- Colophon (2 mm): geometry λ / a / d / L, fringe period, the crop statement,
  `RAYLEIGH-SOMMERFELD BY GAUSS-LEGENDRE QUADRATURE  NO FAR-FIELD APPROXIMATION`,
  and the biprism disclaimer. The caption confirms; it never explains.

## Reference prompt

A science-poster plate on cream: two isometric reliefs of the same probability
landscape in one shared axonometric space — a shallow smooth dune above right, a
deep comb of fine parallel blades below it, twice as tall, cut to the floor at
regular intervals. Fine crimson curves thread both surfaces at the same screen
positions: flat trenches in the comb, high ridges on the dune. Thin dotted
projection lines tie the two stations. Flush-left spaced-caps type, a generous
empty upper-right, no axes, no apparatus, no arrows.

## Build notes

- Entry point: `double_slit_cross_term(rng, bounds, colors=3)` in
  `studio/double-slit/rounds/r01/piece.py`. Nothing under `promptplot/` is
  modified; the piece imports the engine read-only.
- Deterministic and essentially seed-free: the physics is exact, so `rng` only
  fine-tunes. Same seed → same GCode; different seeds → near-identical plate.
- Quadrature: 96-node Gauss–Legendre per slit is converged to <1e-12 relative for
  this geometry; the far-field oracle check runs in NOTES.md, not at render time.
- Craft gates: 2 pens (≤4 ✓); fringe-blade pitch on paper kept ≥0.8 mm by sizing
  the crop and letting `ScreenThin(gap_mm≈1.6·tip)` own the rest.
- Geometry is a **stated optical bench**, not a citation: λ = 633 nm, a = 100 µm,
  d = 300 µm, L = 2.000 m. No measured dataset is claimed anywhere on the plate,
  so there is nothing to misquote. (An earlier draft of this brief proposed the
  Zeilinger 1988 neutron geometry; it was dropped because those numbers could only
  have been quoted from memory. See NOTES.md.)
- Verification receipts are in `rounds/r01/NOTES.md`: quadrature convergence,
  agreement with the far-field closed form, the exact 1/2 amplitude ratio, the
  null positions, fringe visibility, and the cross-term integral.
