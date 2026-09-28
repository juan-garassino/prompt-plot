# MLP — NONLINEAR TRANSFORMATION (the petal-saddle engine) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/mlp` |
| current render | `gallery/neural-networks/mlp/promoted/pp_MLP_engine.png` (gcode beside it: `pp_MLP_engine.gcode`; plottable variants without png in `variants/`: `pp_MLP_leo`, `pp_MLP_void`, `pp_MLP_weave`, `pp_MLP_3D_landscape`, `pp_MLP_3D_leo`) |
| source | `promptplot/generative/pieces/ml.py::bauhaus_manifold` (Scene3D declaration; brief `studio/nets/mlp.md`) |
| paper · pens | a4 portrait (210 × 297 mm), cream · 0 gray (fine 0.1 pen) = the folded surface mesh + the INPUT/OUTPUT planes and their dot lattices · 1 crimson = fold-ridges, ~1 in 4 streamlines, `NONLINEAR ACTIVATION` · 2 black = the other streamlines, droplines, all other type |
| status | unreviewed (no FEEDBACK.md; sits in `promoted/`, eight earlier renders in `prior-approved/`) · 12 renders on disk (+ 6 gcode-only variants) |

## In one line
The MLP drawn as **a folded surface between two parallel planes** — a hidden-line three-petal saddle (the activation folding space) floats between an INPUT plane above and an OUTPUT plane below, and short streamlines fall through it; crimson marks the fold ridges and a few traced trajectories.

## What is on the sheet
Coordinates normalised to the A4 sheet (u → right, v → down); drawable area u 0.07–0.93, v 0.05–0.95.

1. **The folded surface (dominant mass, gray pen)** — an isometric petal-saddle meshed as a spider-web (rings + radials, radials thinning outward in LOD levels), ≈ 0.49 W wide: u 0.26–0.75, v 0.30–0.68. Three lobes read: a large **left wing** seen almost edge-on (u 0.26–0.45, v 0.38–0.62, a crescent whose outer rim at u 0.27 is a tight comb of short radials); a tall **central teardrop petal** standing upright (u 0.40–0.60, v 0.31–0.68, the densest gray, concentric rings packed ≈ 1 mm apart); a **right wing** (u 0.55–0.75, v 0.43–0.60) whose far edge is cut by a label halo. All three meet at a pole around u 0.50, v 0.52 where radials converge into a near-solid gray knot. Hidden-line works: near petals hide far ones.
2. **INPUT plane / OUTPUT plane (gray)** — two identical flat isometric rhombi spanning almost the full drawable width, u 0.10–0.91: INPUT with top vertex at v 0.26 and side vertices at v 0.36 (its near half hidden behind the surface); OUTPUT with side vertices at v 0.68 and bottom vertex at v 0.79. Each carries a sparse lattice of tiny gray tick-dots. Their outlines are the widest element on the sheet.
3. **Streamlines** — ~70 short strokes (5–15 mm), black with ~1 in 4 crimson: a sheaf falling diagonally down-right above the surface in the upper-left (u 0.30–0.50, v 0.30–0.45), a second sheaf fanning out below-right (u 0.60–0.72, v 0.58–0.70), and a band of short strokes under the surface on the OUTPUT plane (u 0.42–0.60, v 0.66–0.74). They stop and restart (pause-resume), so each reads as a dash, not a trajectory. Two columns of **vertical black dashes** stand to the far left (u 0.24 and u 0.26, v 0.38–0.66) and a few more inside the surface — droplines, reading as detached tally marks.
4. **Crimson fold-ridges** — two long straight crimson lines converging on the pole: from u 0.30 v 0.41 down to u 0.49 v 0.52 (left ridge) and a short one rising from the pole to the right (u 0.51–0.55, v 0.49–0.52), plus crimson streamline segments.
5. **Labels** — `I N P U T   S P A C E` (u 0.44–0.57, v 0.33, on the input plane) and `L I N E A R   T R A N S F O R M` (u 0.63–0.81, v 0.33); crimson `N O N L I N E A R` / `A C T I V A T I O N` (u 0.63–0.73, v 0.51 / 0.54) sitting in a halo cut out of the right wing; `O U T P U T   S P A C E` (u 0.44–0.57, v 0.70) and `L I N E A R   T R A N S F O R M` (u 0.63–0.81, v 0.71). The label halos visibly notch the mesh and streamlines.
6. **Title** — `M L P` (≈ 3.6 mm, u 0.20–0.26, v 0.22) and `N O N L I N E A R   T R A N S F O R M A T I O N` (u 0.20–0.51, v 0.24), floating just above the INPUT plane's top vertex.
7. **Quiet zones** — the entire top band v 0.05–0.21 and bottom band v 0.80–0.95 are **empty** (≈ 30 % of the sheet): the composition fill-fits to the width (the plane rhombi) and is vertically centred, leaving equal blank bands above and below.
- Plot stats: draw 11.7 m, travel 8.8 m, 11 226 commands.

## The science it encodes
Brief `studio/nets/mlp.md`: "linear transforms stretch/shear/rotate (they cannot bend), the nonlinear activation FOLDS the space so distant points are brought together and tangled points torn apart… Input plane (top, rigid grid) → matrix multiply projects/stretches it → activation folds the high-dimensional sheet → linear projection resolves it back to a flat output plane, permanently reorganised by the fold." Docstring (`bauhaus_manifold`): "a folded petal-saddle… native polar LOD (spider-web pole), depth-aware screen thinning… streamlines flow INPUT→OUTPUT with pause-resume crowd control, cross-registered against the red fold-ridges".
- **Computed exactly:** the z-buffer hidden-line surface, the polar LOD, the screen-space thinning, the streamline separation (`stream_sep` 2.2 mm), the uniform fit.
- **Seeded / parametric:** the surface is an analytic petal-saddle (`petals=3`, `fold=1.05`, `twist=1.2`), not the image of any network map; streamlines are seeded and do not start on the input lattice or land on the output lattice.
- **Not visible:** the planes are identical and unchanged — nothing shows the output "permanently reorganised by the fold"; the streamlines are too fragmented to show points brought together or torn apart.

## How it got here
- Preceded by the braided-column FOLD (see `studio/neural-networks-manifold/DESCRIPTION.md`), replaced in commit `232622c` ("Replaces the flat folded-flower with an actual small 3D renderer").
- **`pp_MLP_3D_view` (prior-approved, clean render)** — black mesh, full-strength: rhombus planes with dotted lattices and **triple tick "cable" stubs** at their side vertices, the three-petal saddle in black radial mesh with a hard black radial burst at the pole, long crimson streamlines crossing everything, labels `LINEAR TRANS…` truncated/overprinted at the right. Most graphic and legible version: strong mesh, clear pole.
- **`pp_MLP_lod` → `pp_MLP_lod3` → `pp_MLP_final`** — surface moves to a gray fine pen, planes become dashed then dash-dot, polar LOD and screen thinning arrive; in `lod` the thinning eats the type (`NONL NEAR  RANSFORMA  ON`, `NPU  SPAC`), fixed by label halos in lod3/final.
- **`pp_MLP_engine` (current)** — the same composition as a short Scene3D declaration: planes solid gray, surface cleaner at the pole (the lod3/final grey knot is lighter), type intact. Gained: plottable density, legible labels. Lost vs `3D_view`: the black mesh contrast (the surface is now a pale gray body), the pole burst, and the long continuous streamlines.
- No verdict from Juan on record.

## Keep — what works
- **Hidden-line three-petal surface** with a real sense of solid (near petals hide far ones) — the one piece of genuine depth in the neural series.
- **Spider-web polar LOD**: radials halving outward so the pole stays tight but not solid — engine craft worth preserving.
- The **sandwich**: a curved body between two flat parallel planes — flat → folded → flat is the right three-beat structure for "linear, nonlinear, linear".
- **Label halos** that notch the mesh (NONLINEAR ACTIVATION inside the right wing) — type sits in the subject rather than floating beside it.
- Gray (surface) vs black (flow) vs crimson (ridges) — three weights, correct order of loudness.

## Weak — what doesn't
- [space] **30 % of the sheet is empty and not shaped**: blank bands v 0.05–0.21 and v 0.80–0.95, equal above and below. The fill-fit is width-bound by the wide rhombi.
- [tension] Everything is centred on u 0.50: planes symmetric, surface centred, title parked above. No diagonal, nothing crops.
- [concept] It is still a textbook "manifold between input and output planes" figure with a bracket of labels (`LINEAR TRANSFORM / NONLINEAR ACTIVATION / LINEAR TRANSFORM`) — rubric § 6. The surface is an arbitrary analytic saddle, not the map an MLP computes; the planes are unchanged, so the fold changes nothing visible.
- [craft] Streamlines are chopped into 5–15 mm dashes by pause-resume and the vertical droplines at u 0.24–0.26 float free of anything — they read as tally marks, not flow. Travel 8.8 m for 11.7 m of ink.
- [hierarchy] The gray surface (the hero) is the palest element; the black streamline confetti competes with it and wins at 3 m. The plane outlines, the largest shapes, carry no data.
- [craft] The central petal's rings (≈ 1 mm) and the pole knot (u 0.50, v 0.52) approach the flooding limit for a 0.1 pen.
- [grid] Title, labels and planes don't share edges: title left edge u 0.20 aligns with nothing; right labels start at u 0.63 inside the rhombus.

## Next versions
1. **fold-the-lattice** (mechanism) — Make the planes carry the story: the INPUT plane is a regular grid of points/lines; draw its image after affine → ReLU/tanh → affine as the OUTPUT plane, so the output lattice is visibly creased and overlapped (two input cells landing on one output cell = double-inked crimson). The folded surface between them becomes the actual graph of the map (the lattice's trajectory through the layer), not an arbitrary saddle. Order = **laminar with a crease**; mapping "a cell's crimson ink counts how many inputs fold onto it".
2. **origami-crop** (lens) — Drop the planes; blow the three-petal surface up to 1.5× so it crops the left and bottom frame, keep the black mesh contrast of `pp_MLP_3D_view` with the engine's polar LOD, and let one long crimson streamline (continuous, not dashed) cross the fold from upper-left to the lower-right corner as the working diagonal. Title set large in the freed top band.
3. **stacked-sheets** (abstract) — Show depth as a stack of 4–5 thin translucent-in-line sheets, each the previous one folded once more (each a hidden-line mesh), marching diagonally up the page; the density of folds climbs with depth. Uses the engine's surface() per sheet; no labels besides the title.

**If only iterating:**
1. Re-fit the composition to the height (shrink or narrow the rhombi, or scale the surface up) so the blank bands above v 0.21 and below v 0.80 disappear or become one deliberate quiet zone on one side only.
2. Restore surface contrast: surface in black (or a heavier gray) with the plane outlines in the fine pen, so the fold is the darkest mass at 3 m, as in `pp_MLP_3D_view`.
3. Replace the dashed streamline confetti and floating droplines with ≤ 12 continuous streamlines that start on INPUT-lattice points and end on OUTPUT-lattice points, 2–3 of them crimson.
