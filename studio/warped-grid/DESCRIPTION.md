# WARPED GRID — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/warped_grid` |
| current render | `gallery/studio/warped_grid/current/pp_warped_grid_v1.png` |
| reference | `studio/warped-grid/ref/reference.png` |
| source | `studio/warped-grid/rounds/r01/piece.py::warped_grid` |
| paper · pens | a4 portrait, cream · 0 crimson = Q cluster · 1 dodgerblue = K cluster · 2 goldenrod = V cluster · 3 forestgreen = Z = AV landscape · 4 black = Q·Kᵀ lattice, A plane, connectors, type, margin furniture |
| status | unreviewed (no feedback) · 1 render on disk |

## In one line
Attention drawn as **a lattice pinched by alignment** — Q and K spiral-contour clusters fan into a bow-tie-warped Q·Kᵀ grid, softmax lifts it into a perspective plane carrying five contour cones (A), and four black leads plus V's ochre bundle land on a green ridged landscape (Z = AV); a measured recreation of an AI-made reference poster.

## Lede
Self-attention drawn as a lattice **pinched by alignment**: queries and keys fan into a warped grid, which softmax lifts and blends with values.

## On the sheet
Crimson spiral clusters (queries) sit top left and blue ones (keys) top right. Below them a black dotted grid pinches into a bow-tie at the centre. Under that, a black perspective plane carries five contour cones. Four black leads and a goldenrod bundle of values drop to a green ridged landscape at lower left, labelled as the output. Small black marginal glyphs surround the main forms.

## The science
This is a measured copy of a reference poster, not a computation. Contour nests, the bow-tie warp and the cones are geometric constructions placed to match it. The mechanism, match queries to keys, turn the scores into weights, then blend the values, is carried by the labels and the layout, not by any real attention data.

## What is on the sheet
Reading order: the red and blue clusters at the top, the black lattice below them, the A plane, then Z lower left with V lower right. No title.

- **Q cluster** (crimson), u 0.10–0.50, v 0.05–0.30: four spiral/contour nests — the largest (≈0.14 of width, ~13 rings) at u 0.18, v 0.17; others at u 0.28, v 0.13; u 0.38, v 0.21; u 0.27, v 0.24 — joined by bridging rings and by long arcs with bead dots; a bundle of ~12 curves from the big nest converges to an arrow tip at u 0.49, v 0.29. A black dotted outline wraps the cluster. `Q` (crimson, hairline) at u 0.13, v 0.10. Left of it a column of six crimson dots (u 0.10, v 0.15–0.20), a small L-bracket and `(n x d)` at u 0.10–0.14, v 0.24.
- **K cluster** (dodgerblue), mirrored arrangement u 0.50–0.90, v 0.08–0.30: nests at u 0.62, v 0.18; u 0.72, v 0.13; u 0.82, v 0.21; u 0.75, v 0.25; bundle converging to u 0.51, v 0.29; blue dotted outline; `K` at u 0.86, v 0.12; a bracket and six blue dots at u 0.88–0.90, v 0.15–0.21; `(n x d)` at u 0.88, v 0.27; a small open blue ring (u 0.64, v 0.06) and a blue `+` (u 0.74, v 0.32).
- **Label** `Q·Kᵀ` (black) at u 0.50, v 0.32. Right of it a black curved stroke and a vertical arrow (u 0.58–0.63, v 0.30–0.34) — the arrow head points up into the K cluster; the hooked curve ends in mid-air.
- **The Q·Kᵀ lattice** (black, ≈0.20 wide), u 0.40–0.63, v 0.34–0.44: a square grid of ~11×13 nodes (dots at every crossing) bent into an hourglass/bow-tie — top and bottom edges sag inward to a waist at the centre, columns converge to a pinch point at u 0.50, v 0.40. Square brackets with tick marks on both sides; dots at mid-height on the brackets; `(n x n)` at u 0.64, v 0.44.
- **Arrow** down from the lattice (u 0.50, v 0.45), `softmax` (v 0.47) and a vertical stem into the A plane.
- **The A plane** (black, the densest black mass, ≈0.36 wide), a perspective grid trapezoid u 0.29–0.67, v 0.52–0.60, carrying five contour cones (three back, two front: centres ≈u 0.39/0.60 back, 0.50 centre, 0.30/0.66 front), each 6–12 concentric ellipse rings rising to a pin at the apex; the grid lines run through the rings (no hidden-line). The cone summits ink solid black. `A` (large hairline) at u 0.28, v 0.53, `(n x n)` at u 0.28, v 0.56.
- **Four black leads** drop from the A plane's front edge (u 0.46–0.50, v 0.61), run down to v 0.70 then bend left into four arrowheads on the Z crest (u 0.34–0.38, v 0.73).
- **V cluster** (goldenrod), right, u 0.49–0.90, v 0.58–0.82: three nests (u 0.78, v 0.66; u 0.68, v 0.70; u 0.75, v 0.74) with bridging arcs and bead dots, a dotted outline; its bundle leaves the A plane's right front corner (u 0.52, v 0.60) and sweeps into the nests, plus a converging fan to an arrow tip at u 0.65, v 0.72. `V` at u 0.85, v 0.62; bracket + six ochre dots at u 0.87, v 0.64–0.70; `(n x d)` at u 0.87, v 0.72.
- **Z = AV landscape** (forestgreen), u 0.14–0.66, v 0.75–0.86: ~15 ridged profiles over an undulating bump, pinched to a node at the left (u 0.14, v 0.83, with a green lead-in line) and the right (u 0.60, v 0.81), rising to a crest at u 0.36, v 0.76; open green rings on some ridges; a green dot column runs down the axis at u 0.37 through the whole stack, dense enough to read as a solid bar; black dashed arcs above and below. `Z = AV` (green, spaced) at u 0.18–0.31, v 0.78, `(n x d)` beneath.
- **Margin furniture** (black): two overlapping circles on a dashed cross (u 0.17, v 0.40); a 4×4 dot grid and a circle on a dashed cross (u 0.70–0.80, v 0.40); a stack of six horizontal lines each with one bump, beside a dot column (u 0.73–0.85, v 0.48–0.53); a small circle on a stem and a dotted line (u 0.10–0.22, v 0.63); three overlapping circles with a dashed tail (u 0.76–0.86, v 0.86); a rule with dots (u 0.70–0.84, v 0.89).
- Quiet: bottom strip v 0.90–0.97; left margin below the Q cluster.

## The science it encodes
From `r01/NOTES.md` and the docstring: a reproduction — "Every position … expressed in REFERENCE PIXELS of the 1086×1448 plate", measured by hue masks, density peaks and row scans, then mapped to mm. Nothing is computed from attention: nests are conical-cusp contour fields (`_cusp_profile`, ring gap growing linearly with r, 0.88 mm at the eye → 2.0 mm at the rim, eyes emitted as exact circles where marching squares crumbs), the lattice is a geometric warp, the A cones are contour stacks projected onto a plane, and the Z profiles use an amplitude floor so valleys stay ~0.65 mm apart. NOTES admits sub-0.8 mm spacing at A's saddles, fan convergences and the two Z anchors, "present in the reference". The mechanism (QKᵀ, softmax, AV) is labelled, not measured.

## How it got here
Single render (v1); no trials. Against the reference: the station layout, labels, brackets and furniture match. Differences visible on the sheet: the reference's Q/K are flowing contour fields that merge; here they are discrete nests connected by bridging rings and arcs. The reference's lattice pinches to a starburst point with rows intact; here it is a bow-tie whose top and bottom edges curve inward. The reference's A cones fade and its plane is airy; here the grid crosses every ring and the summits flood. The reference routes two black + two ochre leads into Z; here four black leads. The reference's curved arrow from lattice to K connects; here it hooks in mid-air. Juan's feedback: none recorded.

## Keep — what works
- The A plane (u 0.29–0.67, v 0.52–0.60): five contour cones standing on a perspective grid — the one element with real depth, and a strong mid-sheet mass.
- The bow-tie lattice's pinch (u 0.50, v 0.40): a clear, graphic image of alignment concentrating the grid.
- Conical-cusp nests with ring gaps growing with radius — evenly plottable eyes (the r01 NOTES method is worth reusing).
- Colour as provenance, black for operations; the Z crest receiving the four arrow leads (u 0.34–0.38, v 0.73) ties A to Z.

## Weak — what doesn't
- [concept] A labelled pipeline diagram (Q, K, Q·Kᵀ, softmax, A, V, Z = AV, `(n x d)` shape tags, arrows) — the textbook figure § 6 fails; and a trace of someone else's poster.
- [concept] No data: the warp, the cones and the landscape are shapes fitted to a picture, not computed from Q, K, V.
- [craft] A-cone summits flood solid black; the Z axis dot column inks as a solid green bar through the stack (u 0.37, v 0.75–0.88); Z's pinch nodes converge under the floor; 1 251 pen lifts, 63 k commands.
- [craft] The A grid runs straight through the cone rings — no hidden line, so the cones read as transparent wireframes rather than solids.
- [grid] Margin furniture (overlapping circles, dot grid, bump stack, triple circles, stem-and-ring) is a checklist of glyphs that encodes nothing and shares no axis with the subject.
- [craft] The black hook-and-arrow at u 0.58–0.63, v 0.30–0.34 dangles — its curve ends in empty space between `Q·Kᵀ` and the K cluster.
- [hierarchy] Q, K, V clusters, lattice, A plane and Z are all similar mass; nothing dominates.
- [tension] Top half symmetric (Q mirrors K about u 0.50); the V/Z diagonal is the only asymmetry.

## Next versions
1. **THE PINCH** (abstract) — Make the warped lattice the entire plate: a full-sheet node grid deformed by a real QKᵀ score field (columns pulled toward the keys each query attends to), so attention reads as a lattice-with-defects that crowds where alignment is high and relaxes where it is low; Q and K survive only as red/blue tick rulers on two edges. One dominant mass, real data, no furniture.
2. **SOFTMAX TERRAIN** (mechanism) — Promote the A plane: a large perspective plane (≥0.7 of width) of a real attention matrix, each cell a contour cone whose height is A[i,j], drawn with proper hidden-line occlusion (Scene3D), rows summing visibly to one (equal ring volume per row). Depth becomes the argument; Q/K/V/Z reduce to edge annotations.
3. **FAITHFUL, AUTHORED** (faithful) — Keep the reference composition but author the fields: merge each cluster's nests into one continuous contour field, restore the reference's starburst lattice with intact rows, route two black + two ochre leads into Z, connect the lattice→K arrow, and cut every margin glyph that carries no data.

**If only iterating:**
- Stop A-cone rings ≥ 1 mm below each summit (end the pin at the last ring) and hide grid segments inside each cone's footprint.
- Replace the Z axis dot column with ≤ 6 spaced markers so no solid green bar forms at u 0.37.
- Delete the margin furniture glyphs and the dangling hook arrow at u 0.58–0.63, v 0.30–0.34.
