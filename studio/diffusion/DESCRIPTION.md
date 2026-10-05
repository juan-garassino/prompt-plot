# FORM FROM NOISE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/diffusion` |
| current render | `gallery/studio/diffusion/current/pp_diffusion_v1.png` |
| source | `studio/diffusion/rounds/r01/piece.py::diffusion_transport` |
| reference | none |
| paper · pens | a4 portrait, cream · 0 black = density mesh, noise scatter, type, droplines · 1 crimson = separatrix canyon + undecided-path spikes, two plus marks · 2 forestgreen = forward-SDE noise paths and their dashed envelope |
| status | unreviewed (no FEEDBACK.md, no BRIEF.md, no NOTES.md) · 1 render on disk |

## In one line
Reverse diffusion drawn as **flow to attractors on a wireframe terrain** — one broad Gaussian-prior hill at the back tears into three needle modes at the front, where the mesh's row lines are time slices p_t and its column lines are the probability-flow sampler trajectories themselves.

## Lede
Reverse diffusion drawn as a wireframe landscape: a broad hill of noise at the back **resolves into three sharp peaks**, the outcomes the sampler can choose.

## On the sheet
A black wireframe hill fills the upper middle, broad at the top and funnelling into three needle-like peaks at the front. A crimson ladder-shaped canyon runs down its centre, ending in thin crimson spikes. Jagged green noise paths wander across the hill, and black dashes scatter above its crest. Small numbers label each peak, with dashed droplines to a baseline. Spaced capital type sits at the top and bottom.

## The science
The mesh shows a diffusion model turning Gaussian noise into a three-peaked data distribution: rows are moments in time, columns are sampler paths. The green path is a real simulated noise trajectory. The crimson canyon marks where the choice of peak is still undecided. The printed peak masses are only labels and do not match the underlying mixture weights.

## What is on the sheet
All positions normalised to the sheet (u → right, v → down). Portrait; the subject occupies the upper-middle 60 %, the bottom fifth is type and paper.

**1. The terrain (dominant mass, u 0.065–0.80, v 0.24–0.73, ≈0.73 sheet width at its top).** A black quadrilateral wireframe seen in perspective from above:
- **Back/top (v 0.24–0.47)**: a wide, gently arched hill — a regular grid of ~40 columns × ~20 rows, broken by a vertical tear at u≈0.25 into a left panel (u 0.065–0.23) and the main body. Its crest is at u≈0.45, v≈0.24; its right shoulder ends in a straight right edge at u≈0.80, v 0.30–0.47.
- **Middle (v 0.47–0.60)**: the hill fractures into ~6 curved horizontal strips (torn rows with blank paper slivers between them) that sweep inward from both sides like a funnel.
- **Front (v 0.55–0.73)**: three downward **needles** — a thin left needle at u≈0.41 (tip v≈0.72), a tall central needle at u≈0.49 (base v≈0.55), a mid-size right needle at u≈0.56 (tip v≈0.66), each a tight cluster of steep mesh lines.
- **Crimson canyon**: a vertical band of crimson rungs (a ladder of short horizontal crimson strokes between two crimson rails) runs from the crest (u 0.43–0.54, v 0.24) down, narrowing, to the central needle (v≈0.55); below that, 3–4 long thin crimson triangular spikes drop from u≈0.49 to v 0.73–0.76, and a crimson cross-hatched chevron shape at u≈0.52–0.55 reaches v≈0.78. A second crimson dashed seam follows the left tear from u≈0.25, v 0.28 curving to u≈0.32, v 0.55.
- **Green forward-SDE paths**: several jagged green zigzag polylines wander over the hill (u 0.15–0.66, v 0.25–0.60), crossing mesh and crimson alike; at lower left a green dashed line (the envelope) runs diagonally from u≈0.27, v 0.55 to u≈0.36, v 0.70, and a green zigzag outlines the left needle.
- **Noise scatter**: ~120 short black dashes hover above the crest (u 0.28–0.72, v 0.22–0.30), densest at the top centre; two small crimson plus marks at u≈0.25, v 0.26 and u≈0.54, v 0.24.

**2. Mode read-out.** Mass labels at the needle tips: `0.07` (u≈0.41, v≈0.67), `.75` (u≈0.49, v≈0.55 — its leading `0` is overdrawn by the crimson spikes), `0.19` (u≈0.56, v≈0.63). Three dashed vertical droplines fall from the tips to a short horizontal baseline at v≈0.79, u 0.37–0.61.

**3. Type (hairline spaced caps, all flush-left at u≈0.07 unless noted).**
- `FORM FROM NOISE` (v≈0.10, u 0.07–0.47) and `THE PRIOR ALREADY CONTAINS THE PICTURE` (v≈0.13).
- `T 1.00   GAUSSIAN PRIOR` / `N 0 1` (v 0.21–0.23) — the terrain's back row.
- `REVERSE   PROBABILITY FLOW ODE` / `EVERY COLUMN IS ONE SAMPLER PATH` at u 0.57–0.94, v 0.30–0.31 — laid over the mesh's right shoulder; a mesh line strikes through `PROBABILITY`.
- `MODE IS CHOSEN AT T 0.12` (v≈0.455) just under the left panel.
- Green `FORWARD SDE` / `NOISE DESTROYS` at u 0.09–0.23, v 0.50–0.52.
- Crimson `SEPARATRIX` / `THE UNDECIDED PATH` at u 0.60–0.79, v 0.67–0.69.
- `T 0.015   DATA MANIFOLD` (v≈0.81); `140 SAMPLES    11 105 24` (v≈0.87); `VP SDE   BETA 0.1 - 20.0    RK4 ON THE PROBABILITY FLOW` (v≈0.885); `PUSHFORWARD MASS` at u 0.61–0.86, v≈0.90; a three-swatch bar (black / crimson / green) at u≈0.84, v 0.85–0.88.
- The font draws zero as `Ø`.

## The science it encodes
From the `piece.py` docstring: a variance-preserving diffusion model as a **deterministic transport** from the Gaussian prior to a three-mode Gaussian-mixture data law (modes −0.66 / −0.05 / 0.58, weights 0.22 / 0.47 / 0.31, σ₀ 0.10). Exact: the forward marginal p_t (a mixture stays a mixture), the score (responsibility-weighted), the probability-flow ODE `dx/dt = −½β(t)[x + score]` integrated with RK4 (a DDIM-style sampler), VP schedule β = 0.1 → 20 (Song et al.). The green path is a real seeded Euler–Maruyama forward-SDE sample against its exact ±2σ envelope. The mesh is the density landscape over (x, log-SNR): rows = time slices, columns = sampler trajectories. Where trajectories straddle a separatrix the mesh opens a canyon inked red.
Observed vs claimed: the printed mode masses (0.07 / 0.75 / 0.19, from `11 105 24` of 140 samples) are **not** the data weights (0.22 / 0.47 / 0.31) — the samples appear to start on a uniform grid, not from the prior, so the "pushforward mass" is not the mixture's mass; a viewer comparing the needles to the law would conclude the sampler is wrong. The red canyon reads as a ladder band down the centre, not as a blank crack with a red floor.

## How it got here
Single render (v1), no trials, no notes, no feedback. The docstring positions it as a successor to plotting the apparatus: "THE DRAWING IS THE MESH … nothing is overlaid on the terrain."

## Keep — what works
- **The concept "the mesh IS the sampler"**: columns-as-trajectories is a genuine abstract order (flow-to-attractor), not a schematic. Keep it as the thesis.
- **The broad hill → three needles silhouette** (wide top u 0.065–0.80 narrowing to a ~0.15-wide trio of spikes at v≈0.70): a strong funnel shape that reads "many → few" at 3 m.
- **The fracture band** at v 0.47–0.60 — torn rows with slivers of paper — is the most interesting passage: it is where noise commits.
- **Noise scatter above the crest** (v 0.22–0.30) as the prior's cloud before it lands on the hill.
- **Dashed droplines to one baseline** at v≈0.79 give the three modes a shared floor.

## Weak — what doesn't
- [craft] The **green SDE zigzags** cross the mesh, the crimson band and each other over the entire hill (u 0.15–0.66, v 0.25–0.60); they read as scribble, not as a path against an envelope.
- [concept] The **crimson canyon** is drawn as a ladder of rungs between rails (u 0.43–0.54) — an inked strip on top of the mesh, not a blank crack in it. The separatrix does not read as "undecided", and the long crimson spikes below v 0.55 obliterate the central needle.
- [concept] Printed masses 0.07 / 0.75 / 0.19 contradict the data weights 0.22 / 0.47 / 0.31 (grid-started samples) — the one number on the sheet undermines the claim.
- [space] `REVERSE PROBABILITY FLOW ODE` sits on the mesh's right shoulder with a mesh line striking through it; the `0` of `0.75` is overdrawn by crimson; `MODE IS CHOSEN AT T 0.12` grazes the left panel.
- [hierarchy] The three needles (the payoff) are small and illegible in a thicket of mesh fragments; the dominant read is the flat back hill, i.e. the prior, not the data.
- [space] The bottom fifth (v 0.80–0.95) is leftover paper holding a column of hairline type and an orphan swatch bar at u≈0.84 — not a shaped quiet zone.
- [grid] Swatch bar, `PUSHFORWARD MASS` and two crimson plus marks float off any shared axis — the furniture checklist failure.
- [tension] The subject is centred on the sheet's vertical axis with symmetric shoulders; no working diagonal.

## Next versions
- **canyon-of-paper** (mechanism) — Keep the terrain, but render the separatrix as the rubric intends: the mesh columns on either side of the knife-edge simply end, leaving a blank crack of paper that widens toward the front, with ONE crimson line on its floor. Sample starts drawn from the prior so the needle masses equal the weights (0.22 / 0.47 / 0.31) and the needle heights are proportional to them. Delete the green zigzags and draw one SDE path only, as dashes along a single column. The plate becomes exact and the red becomes scarce.
- **columns-only** (abstract) — Drop the row lines entirely: draw ~140 probability-flow trajectories as a laminar curtain descending from a uniform comb at the top edge (cropped at the frame) and braiding into three tight bundles at the bottom, bundle width = mode weight; the separatrices are the two gaps where the curtain parts. Pure flow-to-attractor order, no terrain, no depiction — scores on [concept] and [hierarchy].
- **from-behind** (lens) — Turn the camera: view the density surface from the data side so the three needles are the dominant foreground mass (0.5 of sheet height, cropped at the bottom) and the prior hill is a low horizon; the forward SDE becomes the green haze in the far distance. Depth by scale and line-weight falloff rather than by clutter.
- **If only iterating:**
  1. Remove all green zigzag paths from the hill; keep only the dashed ±2σ envelope and one green SDE path drawn along the left panel's edge.
  2. Replace the crimson rung-ladder (u 0.43–0.54, v 0.24–0.55) with a blank gap in the mesh 3–4 mm wide and a single crimson centreline on its floor; delete the crimson spikes below v 0.55.
  3. Move `REVERSE PROBABILITY FLOW ODE / EVERY COLUMN…` clear of the mesh (above the crest line, on the title's left edge at u≈0.07), and use the 0.80–0.95 band for one large mode-mass read-out on the dropline baseline.
