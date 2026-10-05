# ATTENTION AS INTERFERENCE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/interf_annot` |
| current render | `gallery/studio/interf_annot/current/pp_interf_annot_v8.png` |
| reference | `studio/interference-annotated/ref/reference.png` |
| source | `studio/interference-annotated/rounds/r01/piece.py::attention_interference` |
| paper · pens | a4 portrait, cream · 0 crimson = Q cluster · 1 dodgerblue = K cluster · 2 goldenrod = V cluster · 3 forestgreen = Z = AV landscape + output column · 4 black = QKᵀ lattice, softmax disc, axis, all type, furniture |
| status | unreviewed (no feedback) · 7 renders on disk |

## In one line
Scaled dot-product attention drawn as **interference on a vertical axis** — Q and K emit fans of curves from spiral nests that cross into a woven diamond lattice (the score matrix), which collapses into a nested cone (softmax weights), five taps from which pull V's bundle into a green ridged lens (Z = AV); a measured, pixel-for-pixel recreation of an AI-made reference poster.

## Lede
Scaled dot-product attention drawn as **interference on a vertical axis**: queries and keys cross into a woven lattice that resolves into weights and a blended output.

## On the sheet
Crimson spiral clusters (queries) fill the upper left and blue ones (keys) the upper right, their curves meeting in a black woven lattice on the central axis. Below it a stacked black cone of ellipses shows the weights. Gold curves from the right (values) feed a green ridged lens at the bottom. Small labels and corner crosses frame the page.

## The science
The plate follows the attention formula: scores from queries and keys, a softmax into weights, then a weighted mix of values. It is a visual metaphor, not a computation. No real attention weights or vectors are used; every position is measured from a reference poster, and the interference is drawn, not calculated.

## What is on the sheet
Reading order: the red/blue wings at the top, down the central axis through the black lattice and disc, into the green lens; V hangs off to the right.

- **Title**, centred at u 0.50, v 0.05: `ATTENTION AS INTERFERENCE` (spaced caps, ≈0.52 of width), below it `alignment selects and mixes context` (lower-case, spaced).
- **Central axis**: a black vertical from v≈0.10 down to an arrowhead at v≈0.46 (u 0.50), with ringed dots on it; a black dashed horizontal crosses the lattice at v≈0.36 from u 0.23 to u 0.78 with open-ring ends.
- **Q cluster** (crimson), upper left, u 0.10–0.45, v 0.08–0.33: two large spiral nests (≈10 rings, ≈0.1 of width) at u 0.18, v 0.15 and u 0.17, v 0.25, two small ones (u 0.28, v 0.22; u 0.33, v 0.30), big thin circular arcs, dotted orbits and scattered dots; ~25 curves converge into a node at u 0.43, v 0.30. Label `Q` (large, crimson) at u 0.10, v 0.11, `query`, and black `what / you / are / looking / for` below it (u 0.09, v 0.19–0.23).
- **K cluster** (dodgerblue), upper right, mirror of Q: nests at u 0.80, v 0.12; u 0.65, v 0.22; u 0.77, v 0.28 and a small one u 0.70, v 0.30; bundle converges on a node at u 0.57, v 0.30. `K`, `key`, `what / is / available / in / context` at u 0.85–0.88, v 0.12–0.24.
- **Formula** `Q·Kᵀ/√dₖ` (black, ~5 mm) straddling the axis at v 0.27, between the two nodes.
- **The lattice** (black, the densest black mass), u 0.27–0.73, v 0.30–0.47: from each node a fan of parabolic columns sweeps down and across; the two families cross into a diamond mesh, ~12 near-horizontal token rows run full width, dots at row/column crossings (crimson and blue dots in the first rows under each node). A dashed circle arc surrounds it (radius ≈0.28 of width). Labels at the sides: `emit / query / field / into / token / space` (u 0.14, v 0.32–0.37), `receptive / key / field / across / tokens` (u 0.83, v 0.32–0.37), `alignment / creates / an / interference / pattern` (u 0.74, v 0.40–0.45).
- **Softmax formula** `A = softmax(QKᵀ/√dₖ)` centred at v 0.50.
- **The weights disc** (black), u 0.34–0.66, v 0.53–0.62: ~16 nested flattened ellipses stacked into a cone with a peak at v≈0.53, a dashed outer ellipse, a horizontal axis with dots from u 0.30 to u 0.70. `weights` / `normalize / into / a probability / distribution` at u 0.21–0.28, v 0.51–0.57; `each token / receives / an attention / weight` at u 0.72, v 0.53–0.56.
- **Five taps**: open rings at u 0.46–0.54, v 0.64 under the disc; from them two black dashed drops (left), two green lines, one black line, and a bundle of goldenrod curves + one black line running right to the V cluster.
- **V cluster** (goldenrod), right, u 0.63–0.95, v 0.57–0.84: three large nests (u 0.81, v 0.63; u 0.70, v 0.69; u 0.81, v 0.77) and a small one (u 0.74, v 0.76), a thick braided bundle that fans left to the taps, dotted orbits. `V`, `value`, `the content / to be mixed` at u 0.85–0.89, v 0.58–0.66; `weighted / readout / from values` at u 0.78, v 0.83–0.85.
- **Z = AV** (forestgreen), u 0.30–0.70, v 0.78–0.92: a lens of ~30 ridged rows pinched to two nodes on a horizontal axis at v 0.84 (u 0.30 and 0.70), rising to a summit nest of ovals on the centre; the rows converge so tightly at the two pinch nodes that they ink solid green wedges. A dashed circle surrounds it; a green dotted column of ring-dots runs down the axis through it. Black horizontal axis with dots u 0.20–0.78. `a synthesized / representation / from relevant / context` (u 0.18, v 0.85–0.89). `Z = AV` (green, ~5 mm) at u 0.50, v 0.94; `contextualized output` below at v 0.97.
- **Furniture**: plus-crosses at the four corners and on both margins (u 0.06 and 0.94 at v 0.10, 0.40, 0.68, 0.94), vertical margin rules (u 0.06/0.94, v 0.29–0.40 and 0.43–0.49), a triple-circle stack on each margin at v 0.53–0.56. Corner footers at ~1.2 mm caps: `TRANSFORMERS / TURN / ALIGNMENT / INTO / MEANING` (u 0.06, v 0.93–0.97) and `SAME / INFORMATION / DIFFRENT / INTERFERENCE` (u 0.84, v 0.93–0.96) — the reference's typo reproduced.

## The science it encodes
Scaled dot-product attention, A = softmax(QKᵀ/√dₖ), Z = AV — but on this plate nothing is computed from a model: `r01/NOTES.md` states it is "Reproduction, not design": every landmark is a pixel coordinate measured off the 1122×1402 reference and mapped to the sheet; the piece consumes no randomness. The geometry is constructed to look like the reference — Q/K nests at constant radial pitch, lattice columns as parabolas (constant sideways acceleration) crossing into a diamond weave, the disc as rings of a fitted surface of revolution `h(r) = 72·exp(−(r/79.5)^1.554)` px, the Z lens as a ridgeline over an anisotropic bump plus a second ring family for the summit. No attention weights, no real Q/K vectors; the "interference" is visual metaphor. Keep-out boxes hold min 0.91 mm between geometry and glyphs. Known gaps (NOTES): no serif/italic, busier clusters than the raster reference, Z fuller than the reference.

## How it got here
Eight renders within one round (v1–v8), all on the same layout. v3: lattice as straight vertical columns and a hard rectangle, Q/K clusters with scribbly short links and a fringe of tangled curves; v4–v5: lattice columns became curved, the Z lens filled out; v6: parabolic fans crossing into a diamond weave, Q/K bundles cleaned into spines; v8: Z summit ring family added, disc radii re-stepped for even flank gaps, keep-out boxes, corner rules shortened off the footer words. Compared with the reference: layout, landmarks and label positions match closely; the reference's graded line weight, ghost curves, serif/italic type and airy lower Z rows are lost; the plate is denser and flatter-toned. Juan's feedback: none recorded.

## Keep — what works
- The vertical spine: wings → lattice → disc → lens stacked on one axis at u 0.50 with the formula at each station — a legible top-to-bottom pipeline read.
- The woven lattice (u 0.27–0.73, v 0.30–0.47): two crossing parabolic fans + token rows produce a genuine interference-like moiré from two pens' worth of sources — the best-drawn element.
- Colour as provenance: crimson Q, blue K, ochre V, green Z, black for the operations that combine them; each hue stays in its zone.
- The V bundle sweeping in from the right (u 0.55–0.70, v 0.64–0.72) — the only diagonal on the sheet and the one asymmetric mass.
- Measured-from-reference discipline and the keep-out halos: type never touches geometry.

## Weak — what doesn't
- [concept] It is a schematic: labelled formulas, captions explaining each stage, flow from inputs to outputs — exactly the textbook/slide figure § 6 fails outright (≤3). It is also a reproduction of someone else's figure, not an authored order.
- [concept] Nothing is computed; the lattice, disc and lens are shapes fitted to a picture. A real attention map (e.g. GPT-2 weights already used by `attention_arcs`) would carry data; this carries none.
- [tension] Bilaterally symmetric about the central axis in the top half (Q mirrors K, notes mirror notes); the whole sheet is a centred totem.
- [craft] Z lens: rows pinch into solid green wedges at u 0.30 and 0.70, v 0.84 (sub-0.8 mm convergence); lattice nodes at u 0.43/0.57, v 0.30 go solid black; 5 pens, 16.2 m draw + 12.2 m travel, 2 071 pen lifts.
- [craft] Stroke-font body text at ~1.8 mm and corner footers at ~1.2 mm clog into blobs (`a synthesized / representation`, `TRANSFORMERS / TURN`).
- [hierarchy] Q, K, V clusters, lattice, disc and lens are all similar mass; nothing dominates at 3 m.
- [space] The upper third is saturated edge to edge by the two wings; no quiet zone above v 0.5 except the thin band around the title.
- [grid] Margin furniture (crosses, triple circles, rules) is a checklist on both margins that shares no line with the subject.

## Next versions
1. **SCORE MATRIX AS MOIRÉ** (mechanism) — Keep only the element that works: two fans of lines, one per real query and key vector from a trained checkpoint, their crossing density set by the actual QKᵀ scores, so the moiré IS the attention map. Softmax becomes line-duty along each row; the whole sheet is one woven field with V entering as one diagonal family. Drops every caption and formula; interfering order, real data, a single dominant mass.
2. **ONE HEAD, ONE SENTENCE** (abstract) — Radial: the tokens of one real sentence set around a circle; each query's attention drawn as chords whose ink passes equal the weight; Q red/K blue only at the rim, the output Z as a green inner ring whose radius per token is ‖z‖. The pipeline reading is replaced by the phenomenon (who looks at whom) with one twist line.
3. **FAITHFUL, AUTHORED** (faithful) — If the reference poster is the goal, author it rather than trace it: rebuild the lattice from computed scores, give each cluster a graded line weight by pass count (rims 1 pass, eyes 2), move all prose off the sheet except title and the two formulas, and break the symmetry by cropping the K wing at the right edge. Retains the recognised composition while clearing craft and hierarchy.

**If only iterating:**
- Replace the Z lens and lattice-node convergences with rows that stop 1 mm short of the pinch so no solid wedges ink (u 0.30/0.70, v 0.84; u 0.43/0.57, v 0.30).
- Delete all lower-case annotation blocks and both corner footers; keep title, `Q·Kᵀ/√dₖ`, `A = softmax(…)`, `Z = AV` and the four single-letter labels.
- Scale the lattice to ≥0.6 of sheet width and shrink Q/K/V clusters by a third so the woven field dominates at 3 m.
