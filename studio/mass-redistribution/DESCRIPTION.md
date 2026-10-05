# TRANSFORMER ATTENTION AS MASS REDISTRIBUTION — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/massredist` |
| current render | `gallery/studio/massredist/current/pp_massredist_v6.png` |
| reference | `studio/mass-redistribution/ref/reference.png` |
| source | `studio/mass-redistribution/rounds/r01/piece.py::mass_redistribution` |
| paper · pens | a4 portrait, cream · 0 crimson = Q densities + bundles · 1 dodgerblue = K densities + bundles · 2 goldenrod = V discs + bundles · 3 forestgreen = Z output discs + bundles · 4 black = softmax matrix, formula, title, dotted construction circles |
| status | unreviewed (no feedback) · 6 renders on disk |

## In one line
Single-head attention drawn as **transport between five stations** — Q and K density curves pour ribbon bundles into a central 5×5 softmax matrix whose rows are drawn as equal-length "unit rails" cut at the attention weights, and ochre V bundles leave the matrix to be recombined as five green output pies whose wedge angles are A[i,j]·2π, filled with each value's texture; a recreation of an AI-made reference with the matrix and Z deliberately redesigned.

## Lede
Single-head attention drawn as transport between five stations: **attention redistributes mass** from queries and keys through a softmax matrix into values and outputs.

## On the sheet
Crimson query curves sit at the upper left and blue key curves at the upper right, their ribbons converging on a black five-by-five matrix at the centre. Gold value discs run down the left, and green output pies cascade diagonally to the lower right. Dotted black circles and a title at the top right complete the sheet.

## The science
The query and key densities are random mixtures sampled into eight-dimensional vectors, then run through the real attention formula, softmax of QK transposed over root d_k. The resulting weights cut the matrix rails and set every output pie's wedge angles. The values and queries are synthetic, not taken from a trained model.

## What is on the sheet
Reading order: the red and blue bundles converging on the black matrix at centre, then the ochre and green bundles fanning down, then the V column and the Z cascade.

- **Title**, top right: `TRANSFORMER ATTENTION` (spaced hairline caps, u 0.31–0.95, v 0.04; its last letters `ION` run to the drawable edge), `AS MASS REDISTRIBUTION` beneath at u 0.48–0.95, v 0.06.
- **Q stack** (crimson), u 0.08–0.30, v 0.12–0.40: `Q` letter (u 0.12, v 0.11); five baselines with a small ring at the left end (u 0.08) at v 0.16, 0.22, 0.27, 0.32, 0.37; on each a vertically hatched multi-peak density (3 bumps, ≈0.10 wide); two dotted verticals at u 0.19 and 0.26. From each baseline's right end (u 0.26) a bundle of ~6 crimson curves sweeps right and crosses the others to the five row entries of the matrix (u 0.41, v 0.29–0.39) — a woven ribbon, the densest red mass.
- **K stack** (dodgerblue), mirror at u 0.73–0.95, v 0.13–0.52: `K` (u 0.84, v 0.15), five baselines at v 0.25, 0.30, 0.36, 0.41, 0.47 with hatched densities and end rings at u 0.93; bundles from u 0.73 sweep left into the matrix's right edge, crossing each other and the green bundles in a tangle at u 0.62–0.73, v 0.27–0.47.
- **Formula** `A = softmax (QKᵀ/√dₖ)` in black with tall stroke parentheses, u 0.40–0.63, v 0.19–0.24.
- **The softmax matrix** (the black centre, ≈0.20 of width): caption `ROW SUM = 1` (v 0.25) over a dashed rectangle u 0.41–0.63, v 0.26–0.47. Five horizontal bands, each: a heavy top rail with small tick notches where it is cut into five segments; five short transport strokes per band, each from a small open circle on the cell grid slanting up to its rail segment; a hatched bar in some cells (heights = A[i,j]) sitting on a dotted uniform-share line; a heavy base rule; dotted column dividers. Each rail ends at the right in a small ringed dot (the output port, u 0.62).
- **Ochre bundles**: five thick ribbon bundles leave the matrix bottom (u 0.45–0.58, v 0.47) and arc down-left to the V discs.
- **V column** (goldenrod), u 0.06–0.33, v 0.48–0.84: `V` at u 0.07, v 0.49; a vertical spine at u 0.08 with five ticks; five discs (≈0.07 wide) at v 0.53, 0.58, 0.64, 0.70, 0.75, each a different texture — concentric rings / dot rings / radial spokes / dot rings / rings; each receives its bundle from the right.
- **Green bundles**: five bundles leave the rail ports at u 0.62, v 0.27–0.39, run straight DOWN across the matrix's right columns and through the blue K tangle, then fan out down-right to the Z discs (u 0.55–0.90, v 0.47–0.88).
- **Z cascade** (forestgreen), down-right diagonal: `Z = AV` (u 0.73–0.95, v 0.39); five pie discs (≈0.07–0.08 of width) at (u 0.65, v 0.61), (u 0.74, v 0.64), (u 0.82, v 0.69), (u 0.90, v 0.78), (u 0.81, v 0.87), each cut into wedges filled with ring arcs / spokes / dots copied from the V textures; under each a small five-tick "recipe" bar. Incoming bundles pass over the first disc's rim. The last disc sits ≈8 mm above the bottom drawable edge.
- **Construction layer** (black, dotted): large dotted circles and arcs sprawling across the whole sheet (around the Q stack, behind the matrix, around V, around Z), a dotted vertical axis at u 0.50 from v 0.08 to v 0.95, scattered small open rings and dots.
- **Footer**: a dotted rule and `ALIGN • TRANSPORT • COMPOSE` (spaced caps) at u 0.08–0.46, v 0.92.

## The science it encodes
From the docstring and `r01/NOTES.md`: each of the ten Q/K densities is a seeded 3-component Gaussian mixture; sampling it at d_k = 8 points gives the token vector; vectors are LayerNorm-standardised; S = QKᵀ/√8, A = softmax(S) row-wise — computed, printed in NOTES (rows sum to 1.000000; q0/q1/q4 attend to keys 1 and 4, q2/q3 to keys 0 and 2). The same A drives the hatched bar heights, the rail cut positions, the transport strokes' slope, and the Z wedge angles (A[i,j]·2π). V textures are decorative identities, not computed values; Q/K "vectors" are samples of drawn curves, not a trained model. The two-pattern structure is visible in the matrix (rows 1, 2, 5 share bars in columns 2 and 5; rows 3, 4 in columns 1 and 3); the "equal-length rail" and transport-map reading needs 30 cm and is not legible at 1 m.

## How it got here
Six renders, one round. v2: `A = SOFTMAX(...)` in caps, matrix with denser hatch bars, construction circles heavier, `Z = AV` near the discs; v3: bundles and discs unchanged, matrix bars simplified; v4: formula switched to lower-case `softmax`; v5–v6: construction circles thinned, Z label raised, disc cascade spacing adjusted. Composition never moved. Relative to the reference: the reference's matrix is a 5×5 dot lattice with warped threads and its Z is a green vortex; both were replaced (per NOTES, at Juan's request) by the rail/bar matrix and the five pie discs. Lost from the reference: its airy line weight, the Z vortex's single sweeping mass, and the big quiet zones — this plate is busier. Juan's feedback: none recorded (the redesign request is cited only in NOTES).

## Keep — what works
- Real, coupled numbers: one A matrix drives the bars, the rails and the Z wedges — every mark in the middle and lower right is data.
- The Z pies: each output literally made of the five value textures in proportion to its weights — the best idea on the plate ("Z = AV" drawn, not labelled).
- The crimson and blue ribbon bundles crossing into the matrix (u 0.26–0.41 and u 0.63–0.73) — strong colour masses with real weave.
- Colour-as-provenance with black reserved for the operation (the matrix and formula).
- The V column's five distinct textures as identities that reappear inside the Z wedges.

## Weak — what doesn't
- [concept] A schematic pipeline: labelled stations (Q, K, V, Z), a formula, arrows-by-bundle from inputs to outputs, construction circles — the textbook/slide figure § 6 fails. It is also a reproduction of someone else's layout.
- [craft] The five green bundles run vertically over the matrix's right columns (u 0.58–0.63, v 0.30–0.47) and then through the blue tangle — ink-on-ink collisions across three pens, in the one place that must be readable. Green strokes also cross the first Z disc's rim.
- [craft] 18.5 m draw + 20.5 m travel, 2 831 pen cycles, 5 pens; the matrix cells are ~8 mm wide with 0.8 mm hatch and sub-2 mm transport strokes — the redesign's key read is at the edge of plottable.
- [hierarchy] Q, K, matrix, V and Z are all mid-sized; the matrix — the concept — is only ≈0.20 of the width and loses to the bundles at 3 m.
- [space] The dotted construction circles fill every gap; no quiet zone anywhere; the title presses into the right drawable edge and the last Z disc nearly reaches the bottom edge.
- [grid] Q stack and K stack sit at different heights (v 0.12 vs 0.15 start, different pitches); V and Z share no axis; the footer floats.
- [tension] The Z cascade to the lower right is the only diagonal; the top half is a symmetric Q-matrix-K bridge.
- [depth] Entirely flat, not declared.

## Next versions
1. **ONE UNIT, FIVE CUTS** (mechanism) — Make the redesigned matrix the whole plate: five full-width unit rails (one per query) stacked as the dominant mass, each cut at its real A[i,j], with the 25 transport strokes grown into long ribbons from uniform seats to granted segments. Q/K/V stations shrink to a thin border of token marks; construction circles and formula go. Redistribution becomes the dominant visual fact; one pen swap fewer; hierarchy and concept both rise.
2. **THE MIXING DISCS** (abstract) — Promote the Z pies: five large discs, each a pie of the five V textures by weight, arranged radially around a small central matrix; the sheet reads as five blends of the same five materials (packed/radial order), with no bundles at all. A viewer sees "same ingredients, different recipes" without a caption.
3. **FAITHFUL, DECLUTTERED** (faithful) — Keep the reference's composition but author it: drop the dotted construction layer, route the green bundles from the matrix bottom (never across cells), enlarge the matrix to 0.35 of width, align Q and K stacks on shared baselines, and give the Z cascade a clear gutter from the frame.

**If only iterating:**
- Reroute the green bundles to leave from the matrix's bottom edge (like the ochre ones) so no green stroke crosses a matrix cell or the blue tangle.
- Delete the dotted construction circles and scattered rings; keep only the vertical axis.
- Scale the matrix to ≥ 0.30 of sheet width (cells ≥ 12 mm) and pull the title and last Z disc ≥ 6 mm off the frame.
