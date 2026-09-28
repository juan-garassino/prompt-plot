# MLP — NONLINEAR TRANSFORMATION (the FOLD braid) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/manifold` |
| current render | `gallery/neural-networks/manifold/candidates/pp_bauhaus_manifold_MLP_FOLD_v1_seed8.png` (pixel-identical sibling: `…_FOLD_v1_seed3.png` — the seed has no visible effect) |
| source | **none on disk** for this render. It was drawn by the *interim* `bauhaus_manifold` ("the FOLD of space… streamlines fall from the INPUT plane, twist through a central petal-FOLD") added in commit `58bdb22`; commit `232622c` replaced that function with the petal-saddle 3D engine now at `promptplot/generative/pieces/ml.py::bauhaus_manifold` (see `studio/neural-networks-mlp/DESCRIPTION.md`). Brief: `studio/nets/mlp.md` |
| paper · pens | a4 portrait (210 × 297 mm), cream · 1 crimson = ~1 in 4 strands, `NONLINEAR` label, footer wave curves · 2 black = most strands, boxes, all other type |
| status | unreviewed (no FEEDBACK.md) · 6 renders on disk, all in `candidates/`; superseded in code by the `mlp` subject |

## In one line
The MLP's fold of space drawn as a **braided / twisted-ruled column** — ~100 strands leave a ring in the INPUT box, cross through two pinches in the middle and land on a ring in the OUTPUT box, so the fold is read as strands swapping sides (crimson strands are traced trajectories).

## What is on the sheet
Coordinates normalised to the A4 sheet (u → right, v → down); drawable area u 0.07–0.93, v 0.05–0.95. Only the 614 px preview exists.

1. **The braid (dominant mass)** — a column of ~100 curved strands spanning u 0.24–0.76 (0.52 W) and v 0.12–0.89 (0.77 of sheet height). At the top the strands fan out as a dense ring of arcs inside the INPUT box (the top of a cylinder seen from above); they then cross the column diagonally, forming a lattice of large diamonds whose crossings concentrate on the centre line u 0.50 at two pinches (v ≈ 0.39 and v ≈ 0.59); the envelope bulges outward at v ≈ 0.51 (u 0.28 and u 0.72); at the bottom they fan into a second ring of arcs in the OUTPUT box. Roughly 1 strand in 4 is crimson, evenly interleaved. The crossings in the middle third are nearly solid black (tens of hairlines through the same point).
2. **INPUT box / OUTPUT box** — two thin black rectangles of the same size, u 0.24–0.76: INPUT at v 0.12–0.23, OUTPUT at v 0.77–0.89. Small tick marks along their inner edges. The strand rings overflow the rectangles' left and right edges.
3. **Right-hand labels** — three letter-spaced labels at u 0.77: `L I N E A R   T R…` (v 0.27, black), `N O N L I N E A R` (v 0.50, **crimson**), `L I N E A R   T R…` (v 0.74, black). Each is **truncated** at the drawable margin (u 0.93) and continues as a thick smeared bar of overprinted strokes from u 0.93 to the paper edge u 1.00 — ink outside the margin.
4. **Title block** (top-left) — `M L P` (≈ 3.6 mm, u 0.10–0.16, v 0.07) and `N O N L I N E A R   T R A N S F O R M A T I O N` (u 0.10–0.56, v 0.10). `I N P U T   S P A C E` sits at u 0.42–0.62, v 0.09, overlapping the subtitle's right half.
5. **Bottom-left caption** — `S A M E   T O K E N S` / `D I F F E R E N T   G E O M E T R Y` / `A   R I C H E R   S P A C E` (u 0.10–0.35, v 0.86–0.89), overprinted by the lower strand fan and the OUTPUT box's left edge.
6. **`O U T P U T   S P A C E`** (u 0.45–0.62, v 0.90) — directly under the box, touching its bottom edge.
7. **Footer icon strip** (u 0.57–0.82, v 0.91–0.93) — four small black boxes joined by arrows, each holding a crimson curve: a flat line → half an arch → one sine period → two sine periods (a function being bent progressively).
8. **Quiet zones** — u 0.07–0.23 and u 0.77–0.93 beside the braid (except the three right labels): two vertical side margins, symmetric.
- Plot stats in the preview: draw 38.2 m, travel 35.6 m, 14 810 commands — the heaviest sheet in this batch.

## The science it encodes
Brief `studio/nets/mlp.md`: "a network sculpts the coordinate space its data lives in — linear transforms stretch/shear/rotate (they cannot bend), the nonlinear activation FOLDS the space so distant points are brought together and tangled points torn apart… 'Same tokens, different geometry.'" The interim function's docstring (commit `58bdb22`): "an MLP as the FOLD of space. Streamlines fall from the INPUT plane (top), twist through a central petal-FOLD".
- **What the render shows:** a twisted ruled column — every strand is a smooth parametric path from a point on the top ring to a rotated point on the bottom ring. That is a rotation/twist (a linear-looking map), not a fold: nothing on the sheet shows two regions of input landing on the same output, or a crease. The three right labels assert LINEAR / NONLINEAR / LINEAR bands, but the braid looks the same in all three bands.
- **Seeded vs computed:** seed 3 and seed 8 are identical — geometry is fully parametric; no network, no weights.

## How it got here
- **v1 / v2 (`MLP_v1_seed8`, `MLP_v2_seed3`, `MLP_v2_seed8`)** — a one-sheet **hyperboloid** of straight rulings: a waisted wireframe tower (u 0.24–0.76, v 0.13–0.86) with wavy top/bottom rims, a few horizontal ellipse rings, a tiny crimson ellipse at the waist (u 0.50, v 0.50), a dashed axis with small dots; caption `COMPRESS / TRANSFORM / EXPAND POSSIBILITY`; footer icons grid → star → star. Clean, light (21 m draw), but a wire-frame textbook object; crimson almost absent.
- **FOLD v1 (current)** — rulings become curved strands, input/output boxes and the LINEAR/NONLINEAR/LINEAR bracket labels added, crimson raised to ~25 % of strands, caption changed to `SAME TOKENS / DIFFERENT GEOMETRY / A RICHER SPACE`, footer becomes the wave-bending strip. Gained: density, colour, a stated mapping. Lost: the hyperboloid's legible waist and its lightness; labels now collide or leave the page.
- Then retired in code: commit `232622c` ("Replaces the flat folded-flower with an actual small 3D renderer") — continued as the `mlp` subject.
- No verdict from Juan on record.

## Keep — what works
- The **tall single column** occupying 0.77 of sheet height — one dominant mass, clear at 3 m.
- **Two pinch points on the centre line** (v ≈ 0.39, v ≈ 0.59) where strands swap sides — the only hint of "points brought together / torn apart"; it is the germ of a real fold.
- The **ring-to-ring framing**: the same object (a ring of points) at top and bottom, rearranged — "same tokens, different geometry" without words.
- The footer's idea (a line bending into a wave, step by step) is the clearest statement of "nonlinear" on the sheet — worth keeping as a mapping, not as an icon strip.

## Weak — what doesn't
- [craft] **Ink beyond the margin**: the three right labels are cut at u 0.93 and turn into smeared bars to the paper edge. Unplottable as is.
- [craft] Middle third floods: tens of hairlines cross at single points on the centre line; draw 38 m for a sheet that reads as grey mush at the crossings. Travel ≈ draw.
- [craft] Type collisions: `INPUT SPACE` over the subtitle, the caption overprinted by strands and the box edge, `OUTPUT SPACE` on the box line.
- [concept] The mechanism is misdrawn: a twist is not a fold. No crease, no many-to-one mapping. Plus a **schematic** skeleton (input box → labelled bands → output box + icon strip with arrows) — rubric § 6.
- [tension] Perfect left/right symmetry about u 0.50, subject dead-centre with even side margins.
- [hierarchy] Crimson used as an even 1-in-4 stripe — a category, not a scarce loud accent; no second-level element.
- [grid] Title top-left, caption bottom-left, footer bottom-right, labels right: four furniture positions on no shared line.
- [depth] The strands imply a cylinder but nothing is occluded — back strands draw over front ones, so the volume collapses into a flat lattice.
- [space] The side margins are leftover strips, not shaped.

## Next versions
1. **relu-crease** (mechanism) — Draw an actual fold: a regular lattice of points/lines (the input plane) passes through one ReLU-like crease `F(p)=p−2·max(0,−d)·n` (the alt spec already on file in `studio/nets/mlp.md`), so one half-plane is reflected onto the other; where two input regions land on the same output the line density doubles, and that doubled band is the only crimson. Order = **laminar with a fold line**, exact and one-line mappable ("density doubles where the map is two-to-one").
2. **braid-with-occlusion** (faithful) — Keep this column but make it honest 3D: strands behind the axis break around strands in front (hidden-line), crossings kept ≥ 0.8 mm apart, strand count halved; crimson reduced to 3 traced trajectories that end on output positions visibly different from their input neighbours. Put the column off-centre (u 0.35) and let the lower fan crop the bottom edge.
3. **bending-line field** (abstract) — Promote the footer idea to the whole sheet: ~60 horizontal lines from top to bottom, each the previous passed through one more layer (affine + tanh), so straight lines at the top progressively fold, pinch and overlap toward the bottom — a laminar order whose depth is the network's depth. No boxes, no labels except the title.

**If only iterating:**
1. Pull the three right labels fully inside the drawable area (end ≥ 3 mm before u 0.93) and delete the overprinted bars; clear every label from strands and box edges by ≥ 2 mm.
2. Halve the strand count and keep crossings ≥ 0.8 mm apart through the two pinches so the centre third reads as lattice, not solid black; drop crimson to ≤ 5 strands.
3. Occlude back strands behind front strands so the column reads as a volume, and move the column off the centre axis so one side margin becomes a shaped quiet zone.
