# NO FIXED POINT — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/gan` |
| current render | `gallery/studio/gan/current/pp_gan_v1.png` |
| source | `studio/gan/rounds/r01/piece.py::minimax_duel` |
| paper · pens | a4 portrait (210×297 mm), white preview · as rendered: 2 forestgreen = surface mesh + all type · 1 crimson = generator legs, plus-mark at the equilibrium · 0 black = discriminator legs, dotted orbit, void rim. (The code names the pens PINK / BLUE / BLACK; the preview shows the default palette, and the gcode carries 4 colour indices while the preview legend lists 3.) |
| status | unreviewed (no feedback on file) · 1 render on disk |

## In one line
The Dirac-GAN's simultaneous gradient descent-ascent drawn as an **orbital** order on an exact saddle — the objective V = f(ψθ) is the relief, each iteration is a generator leg plus a discriminator leg, and the Nash point is a hole of bare paper the orbit never reaches.

## What is on the sheet
- **The saddle (dominant mass).** One draped wireframe surface, ~0.85 of sheet width, spanning u≈0.10–0.95, v≈0.39–0.80, all in green. It is a ring-and-radial polar mesh seen in axonometry: an elongated bowl whose front lip sweeps down-left into a deep curled trough (lowest point u≈0.18, v≈0.80) and whose right side pinches into a narrow horn that converges to a point at u≈0.94, v≈0.66. Radials are thinned in LOD steps, so the far (upper) half reads as broken fence-posts: short radial stubs of varying length at u≈0.35–0.65, v≈0.39–0.45. Ring spacing tightens hard along the front-lower band (v≈0.62–0.70) and in the two convergence zones (trough fold u≈0.25–0.35, v≈0.66–0.75; right horn u≈0.85–0.94, v≈0.60–0.66), where the green lines touch and nearly fill.
- **The equilibrium hole.** An empty oval of bare paper, ~0.17 of sheet width, centred u≈0.55, v≈0.58, bounded by the innermost green ring. A small crimson `+` sits at its centre. A black dotted/dashed ring and a crimson dashed ring shadow the 3rd–6th mesh rings around it.
- **The duel (staircase).** Scattered black dashes (long, oblique, running roughly along the θ axis in projection — they read as diagonal slashes lower-left) and short crimson dashes (roughly horizontal), strewn over the left half of the bowl (u≈0.12–0.45, v≈0.45–0.78) and as a crimson dashed arc on the right shoulder (u≈0.80–0.87, v≈0.40–0.52). At this scale they do not read as a connected staircase or an outward spiral; they read as sparse broken strokes laid over the mesh.
- **Type.** Top-left block: `NO FIXED` / `POINT` (spaced caps, ~3.4 mm, u≈0.06–0.28, v≈0.06–0.09, a short underline stroke beneath `P`), then `NEITHER PLAYER EVER ARRIVES` (~2 mm, u≈0.06–0.54, v≈0.11). Inside the surface under the hole, carved out of the mesh by a label halo: `EQUILIBRIUM` / `NEVER REACHED` (u≈0.50–0.65, v≈0.61–0.63). On the lower-left lip: `D   PSI` (u≈0.30–0.40, v≈0.72). The code's `G  THETA` axis label is not visible on the render. Footer left: `575 STEPS    R 0.74 TO 3.23` / `G MOVES THETA    D MOVES PSI` (v≈0.94–0.95, u≈0.06–0.55). Footer right: `MIN G MAX D V D G` (u≈0.60–0.93, v≈0.95).
- **Furniture.** A tiny three-pen swatch stack (green / crimson / black ticks) at u≈0.92, v≈0.05–0.08. A thin flat green sliver-rectangle at u≈0.95–1.00, v≈0.67 that runs from the horn tip past the margin to the paper's right edge.
- **Quiet zone.** The whole band u≈0.06–0.95, v≈0.12–0.38 is empty paper — roughly a third of the sheet, above the surface.

## The science it encodes
From the module docstring of `studio/gan/rounds/r01/piece.py`: the Dirac-GAN (Mescheder, Geiger, Nowozin 2018). Real data δ₀, generator δ_θ, discriminator D_ψ(x)=ψx, objective V(θ,ψ)=f(ψθ)+f(0) with f(t)=−log(1+e^{−t}). The mesh height is the exact V — a hyperbolic saddle in s=ψθ. Continuous time conserves θ²+ψ² (a closed orbit); the discrete simultaneous step multiplies the radius by √(1+h²f′(s)²) every iteration, so training provably spirals OUT. Parameters: h=0.26, start radius 0.74, arena radius 3.30, void radius 0.60; the footer reports 575 steps, r 0.74 → 3.23. Each iteration is drawn as a θ-leg (generator) and a ψ-leg (discriminator); leg length = gradient magnitude, so bunching marks saturation where f′→0. The dotted ring is the continuous-time orbit at the step-52 % radius.

What is computed is exact; what does not survive to the render is the *outward spiral* — the legs are occupancy-thinned into disconnected dashes, so the one fact the plate is about (radius grows every step) is not visible. The brief (`studio/nets/gan.md`) asked for two opposing terrains meeting at a decision plane with red tension arcs; this round replaced it with the Dirac-GAN saddle — a better mechanism, but nothing of the brief's "two forces facing each other" remains.

## How it got here
Single render (v1, round r01); no trials on disk and no feedback from Juan. The only history is the pivot away from the `studio/nets/gan.md` brief (twin opposing surfaces) to the one-surface Dirac-GAN.

## Keep — what works
- The equilibrium as a hole of bare paper (u≈0.55, v≈0.58) with a single crimson `+` — "the only thing made of paper" is the right idea and it reads.
- The exact objective as relief: the curled trough lower-left and the pinched horn right give the surface a real, asymmetric silhouette instead of a symmetric bowl.
- The title/tagline pair `NO FIXED POINT` / `NEITHER PLAYER EVER ARRIVES` — dry, correct, and it lands the joke the mechanism makes.
- Splitting each update into a generator leg and a discriminator leg in two pens — the counterfactual corner is a genuine idea worth keeping.
- `EQUILIBRIUM / NEVER REACHED` carved into the mesh by a halo right under the hole.

## Weak — what doesn't
- [concept] The outward spiral does not read. The legs are scattered crimson/black dashes with no continuity from the start radius to the arena edge; a viewer sees a mesh with some broken strokes on it, not a game escaping its equilibrium.
- [hierarchy] The green mesh is the loudest thing on the sheet; the duel (the subject) is the quietest. At 3 m the plate is "a green wire bowl".
- [craft] Ink floods where rings converge: the right horn (u≈0.85–0.94, v≈0.60–0.66), the trough fold (u≈0.25–0.35, v≈0.66–0.75) and the front band (v≈0.62–0.70) go near-solid green.
- [craft] The green sliver at u≈0.95–1.00, v≈0.67 crosses the margin to the paper edge — a clipping/overflow defect.
- [space] The empty top third (v≈0.12–0.38) is leftover, not shaped: the surface sits low, the title sits high, and nothing ties them.
- [grid] Footer right `MIN G MAX D V D G` and footer left sit on different baselines; the swatch stack floats in the top-right corner off any shared line (furniture-checklist failure mode).
- [craft] The top-half radial stubs (u≈0.35–0.65, v≈0.39–0.45) read as a broken picket fence rather than depth fall-off.
- [concept] `G  THETA` is missing while `D  PSI` is present — the two players are labelled asymmetrically.
- [depth] Depth comes only from ring compression; no line-weight or dash fall-off separates near lip from far rim.

## Next versions
1. **escape-spiral** (mechanism) — Make the discrete orbit the dominant mass: draw the full 575-step staircase as one continuous crimson/black zig-zag spiral in the (θ,ψ) plane, unthinned, widening from the paper hole to the frame and cropping off the sheet edge where it leaves the arena. The saddle drops to a faint, sparse dashed ring-lattice underneath (or only its sign-change lines ψθ=0 as two crossing knives). The plate then shows, at 3 m, the one exact fact: every step moves further out.
2. **two-players-interlaced** (abstract) — Transpose to INTERLACING: the generator's legs are the weft, the discriminator's legs the warp; over/under at each crossing is set by who "won" that step (sign of s), float length by gradient magnitude. The hole at the centre is where no thread crosses. Drops the 3D mesh entirely and matches the collection's strongest order; the spiral emerges as a widening woven square-spiral.
3. **faithful-duel** (faithful) — Return to the brief: two opposed surfaces — the generator terrain rising, the discriminator hanging — meeting at a zero-plane, but with the gap between them carrying the Dirac-GAN orbit as the red "tension" drawn in the plane itself. Keeps the brief's two-force symmetry broken by the spiral's drift.

**If only iterating:**
- Draw the staircase as connected polylines with no occupancy thinning, double-passed, so a continuous spiral runs from the hole rim (u≈0.55, v≈0.58) out past the surface edge; test: the spiral can be traced by eye end to end.
- Cap mesh density: at most one ring per 1.2 mm on screen and drop the radial fence stubs in the far half; test: no green region at the horn or trough reads solid.
- Move the surface up so its top rim sits on the tagline's baseline grid (v≈0.13), put the swatch and both footers on one baseline, and remove the sliver that reaches the paper edge.
