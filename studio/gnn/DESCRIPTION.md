# REACH — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/gnn` |
| current render | `gallery/studio/gnn/current/pp_gnn_v1.png` |
| source | `studio/gnn/rounds/r01/piece.py::studio_gnn` |
| paper · pens | a4 portrait (210×297 mm), white preview · 0 black = hop-field terrain mesh + all type · 1 crimson = 1/2/3-hop receptive-field terraces, shortcut arcs, root disc, consensus dot · 2 forestgreen (code: BLUE) = the 12-layer mean-aggregation trajectories |
| status | unreviewed (no feedback on file) · 1 render on disk |

## In one line
Message passing drawn as a **nested / terraced** order on the exact BFS hop-distance field of a seeded small-world graph — root = summit, one hop per terrace, the 3-hop receptive field in red — with a **laminar** footer of 12-layer mean-aggregation traces meant to collapse into one consensus line.

## What is on the sheet
- **The terrain (dominant mass).** A black wireframe hidden-line mountain, ~0.86 of sheet width, spanning u≈0.07–0.93, v≈0.25–0.53. A broad ridge rises left-to-right: a lower left shoulder peaks at u≈0.28, v≈0.34, the summit is at u≈0.54, v≈0.28, and a long right flank runs down to a thin spit ending at u≈0.93, v≈0.41. The front face drops into a V-shaped keel whose point sits at u≈0.50, v≈0.53. Mesh is a crossed diagonal grid; it is densest (near solid black) on the front slope u≈0.30–0.70, v≈0.35–0.45 and on the right flank where the grid lines compress (u≈0.70–0.85, v≈0.37–0.40). A few thin elliptical contour loops are visible inside the mesh on the left shoulder and front face.
- **The red receptive field.** Around the summit, a small filled crimson disc (root, u≈0.54, v≈0.28, ~0.02 of width) inside a crimson circle, then three nested ragged crimson terrace rings stepping down the front slope (widest ring spans u≈0.29–0.66, v≈0.29–0.42). Two long crimson arcs leave the summit area: one a high parabola that lands on the left shoulder at u≈0.28, v≈0.34 (apex u≈0.44, v≈0.23, above the terrain), the other a tall narrow loop (apex u≈0.50, v≈0.23) that drops straight down to u≈0.47, v≈0.38. A short crimson tick near `ARCHIPELAGO` at u≈0.78, v≈0.41. The "islands" the docstring promises are not identifiable as separate red regions.
- **Terrain labels.** `ROOT` (u≈0.59–0.66, v≈0.27) right of the summit. `ARCHIPELAGO` (u≈0.74–0.93, v≈0.40) sitting on the right spit, halo-carved from the mesh. Scattered tiny black dashes float just outside the terrain edge (u≈0.13–0.26, v≈0.46–0.48; u≈0.68–0.87, v≈0.43–0.46) — fragments of hidden contour.
- **Title block.** `REACH` (spaced caps ~4.6 mm, u≈0.09–0.26, v≈0.08), `GNN . MESSAGE PASSING` (v≈0.115), `THREE HOPS TO SEE . TWELVE TO FORGET` (u≈0.09–0.68, v≈0.13).
- **Floating caption.** `RECEPTIVE FIELD . 3 HOPS` alone at u≈0.09–0.50, v≈0.64 — in open paper ~30 mm below the terrain keel.
- **Oversmoothing footer (second mass).** `LAMBDA2 0.98 . SPREAD PER LAYER` (v≈0.71) then `OVERSMOOTHING` (~2.6 mm, v≈0.72), both at u≈0.09. Below, ~34 green near-horizontal trajectories from u≈0.09 to u≈0.86, v≈0.74–0.84: they converge only slightly from left to right (spread ~0.10 of sheet height at K 0, ~0.07 at K 12) and clump into several near-solid green bands in the middle (v≈0.77–0.80). A short crimson dash (the consensus dot) at their right end, u≈0.87, v≈0.83. `K 0` (u≈0.09) and `K 12` (u≈0.78–0.82) under the band at v≈0.855. A 3-pen swatch stack at u≈0.89, v≈0.71–0.74.
- **Footer.** `H K . MEAN OF H K-1 OVER N V PLUS V` at u≈0.09–0.60, v≈0.93, which physically overprints `150 NODES . 11 HOPS` (u≈0.55–0.90, v≈0.93): the characters `PLUS V` and `150 N` collide into `PL1U550 VNODES`.
- **Quiet zones.** v≈0.14–0.23 above the terrain (except the red arcs poking into it) and v≈0.53–0.70 below the keel (broken only by the floating caption).

## The science it encodes
From `studio/gnn/rounds/r01/piece.py` docstring: a seeded small-world geometric graph (150 Poisson-disk nodes, kNN k=3, 3 long-range shortcut rewires, forced connected); exact BFS hop distance from one root; the continuous hop field f(p)=min_v[d(v)+|p−p_v|/L] (lower envelope of unit cones, L = median edge length) whose level sets are the k-hop receptive fields; exact mean aggregation h^(k)=D⁻¹(A+I)h^(k−1) over 12 layers, measured |λ₂|=0.98. The hero claim — "a GNN's receptive field is not a disc, it is an ARCHIPELAGO", broken into islands by shortcuts — is not visible: the red terraces read as three concentric rings plus two loose arcs, and nothing on the sheet shows a disconnected red island. The footer's collapse is also barely visible at λ₂=0.98 over 12 layers (the traces narrow by ~30 %, not to a line). The brief (`studio/nets/gnn.md`) asked for an organic node constellation with aggregation ripples; this round replaced the graph drawing with its hop field — no node or edge is drawn.

## How it got here
Single render (v1, round r01); no trials on disk and no feedback from Juan.

## Keep — what works
- The hop field as a terrain whose summit is the root — the idea that "reach" has a shape, and that the shape is ragged, is right.
- Title pair `REACH` / `THREE HOPS TO SEE . TWELVE TO FORGET` — the best line on the plate; it states both halves of the piece and has wit.
- The red pen used sparingly on the front slope: three nested terraces read at 1 m as "the part the network sees".
- The long crimson shortcut parabola vaulting from the summit to the left shoulder (apex u≈0.44, v≈0.23) — the one gesture that shows a message teleporting.
- `ARCHIPELAGO` sitting on the thin right spit, halo-cut into the mesh.

## Weak — what doesn't
- [concept] The archipelago is not drawn: no red island is separated from the main terrace nest, so the key claim needs the caption to exist.
- [concept] The oversmoothing footer is an axis plot (traces vs layer index with `K 0` / `K 12`) — the scientific-figure failure mode — and at λ₂=0.98 it does not even collapse.
- [craft] Footer text collision at u≈0.55–0.62, v≈0.93: `PLUS V` overprints `150 NODES`.
- [craft] The green trajectories stack into near-solid bands (v≈0.77–0.80) — overlap under the pen tip.
- [craft] The front slope mesh (u≈0.30–0.70, v≈0.35–0.45) and the right flank compress to near-black; stray contour dashes litter the terrain rim.
- [grid] `RECEPTIVE FIELD . 3 HOPS` floats at v≈0.64 attached to nothing; swatch stack floats right of the footer block.
- [hierarchy] Terrain and footer are two unrelated masses of similar weight; the tall top margin (v≈0.14–0.23) and the gap under the keel read as leftover.
- [tension] The mountain is centred with a symmetric V keel — reads as a centred specimen.
- [depth] Depth comes from hidden-line occlusion only; no weight or density fall-off from front to far ridge.

## Next versions
1. **true-archipelago** (mechanism) — Keep the terrain but make the islands the subject: raise hops_red or pick a root whose 3-hop set is split by shortcuts, fill each disconnected red region with its own terraced nest so at least two separate red islands sit on the sheet, joined only by crimson shortcut arcs. Cut the oversmoothing footer to a single strip or remove it. The one fact — reach is not a disc — lands without the caption.
2. **forgetting-strata** (abstract) — Transpose to LAMINAR / STRATIFIED: stack the 12 layers as horizontal strata down the whole sheet, each stratum a row of node marks whose horizontal position is its feature value; strata narrow layer by layer into a single vertical plumb line at the bottom (oversmoothing as sedimentation). The red 3-hop set is marked in the top three strata only. "Three hops to see, twelve to forget" becomes the whole composition's vertical axis.
3. **constellation-ripples** (faithful) — Return to the brief: draw the 150-node graph as a constellation with the 3 shortcut edges long and red, and the hop field as concentric ragged contour rings (not terrain) emanating from the root, with ring islands appearing around the far end of each shortcut. Flat by declaration (a star chart), with ring-weight fall-off by hop count.

**If only iterating:**
- Show at least two disconnected red receptive-field islands (each with its own terrace nest) linked by crimson shortcut arcs; test: a viewer can count the islands without reading `ARCHIPELAGO`.
- Increase the oversmoothing layer count or use a graph with smaller λ₂ so the traces visibly converge to one line at the right end, and cap trace spacing at ≥0.8 mm; test: no solid green band, final spread ≤ 1 mm.
- Fix the footer: put `H K . MEAN OF…` and `150 NODES . 11 HOPS` on separate baselines or sides, move `RECEPTIVE FIELD . 3 HOPS` up onto the terrain's keel line, and put the swatch on the footer baseline.
