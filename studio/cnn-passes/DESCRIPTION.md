# THE MIRROR FORGETS (CNN — forward and backward) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/cnn_passes` |
| current render | `gallery/studio/cnn_passes/current/pp_cnn_passes_abstract_v10.png` (THE MIRROR FORGETS — **approved**) |
| | `gallery/studio/cnn_passes/current/pp_cnn_passes_faithful_v10.png` (reference recreation) |
| | `gallery/studio/cnn_passes/current/pp_cnn_passes_mechanism_v9.png` (true computed CNN) |
| source | abstract: `studio/cnn-passes/rounds/r03/piece_v10_APPROVED.py::cnn_passes` (frozen; branch from `r03/piece.py`) · faithful: `studio/cnn-passes/rounds/r01/piece.py::cnn_passes` · mechanism: `studio/cnn-passes/rounds/r02/piece.py::cnn_passes` + `r02/net.py` |
| reference | `studio/cnn-passes/ref/reference.png` |
| paper · pens | a3 landscape, cream · 0 black = forward pass, structure, type · 1 dodgerblue = the one tracked forward channel / winning class · 2 crimson = the entire backward pass · cream paper = the ReLU gate |
| status | abstract v10 **PROMOTED** ("i love this one!", 2026-09-20) — frozen, never edited · faithful v10 and mechanism v9 unreviewed · 31 renders on disk |

## In one line
The forward and backward passes of a CNN drawn as **nested annuli collapsing to a core** — each ring-band is one layer, angular cell count halves at every pool while radial sub-rings double with channels, the forward half runs inward and the gradient half climbs back out, and blank paper is ReLU on both. The faithful variant keeps the reference's **laminar two-register pipeline** (forward stacks on top, gradient twins on the same columns below); the mechanism variant is the same two registers with every plane computed by a real numpy CNN.

## Lede
A convolutional network's forward pass and its backpropagated gradient drawn as **concentric rings** that run inward to a single answer and back out again.

## On the sheet
A disc of concentric rings fills the right of the sheet, cropped by the frame, with black arcs for the forward pass and crimson dashes for the gradient. Dodger blue marks one tracked channel, and blank wedges of paper cut across every ring. A blue and crimson core sits at the centre, joined to the edge by a straight corridor. Type and a stage table run down the left.

## The science
Each ring is a layer: moving inward, the angular cells halve at every pooling step while radial sub-rings multiply with channels. Blank paper is the ReLU gate, empty on both the forward and backward passes. The measured figures are printed on the sheet, but the activations are a seeded synthetic field, not a trained network.

## What is on the sheet

### abstract v10 — THE MIRROR FORGETS
**Polar mass (dominant, right 60 %).** A disc of concentric annular bands centred at u≈0.74, v≈0.64, radius ≈ 131 mm (≈0.31 sheet width; the whole disc ≈0.62 width across). It is cropped decisively by the right frame (u≈0.97) and bottom frame (v≈0.95); its outermost arc tops out at v≈0.195 and its left edge sits at u≈0.43.
- **Five bands**, each made of an outer **black** sub-band (clusters of 3–8 parallel dashed arcs, dash length ∝ activation) and an inner **crimson** sub-band (short radial columns of 2–4 tiny crimson dashes, sparse and broken), separated by a ~1 mm gap; ~6 mm of paper between bands. The outermost (input) band is three continuous-looking black rings with fine texture — the only ungated band.
- **Blue** appears only as short arc runs inside black sub-bands (one tracked channel, where it fires) — e.g. a long blue run at the bottom of the second band (u≈0.62–0.78, v≈0.85) and scattered runs on the left.
- **Blank wedges**: a huge quiet wedge in the upper-right quadrant (angles ≈ 0°–80°, u≈0.76–0.95, v≈0.25–0.58) where all inner bands are absent and only the outer ring arc passes; smaller blank wedges at ~200–240° (lower-left, u≈0.47–0.58, v≈0.70–0.88) and elsewhere. They line up radially across bands. Short straight black rules sit at the edges of the widest wedges (e.g. u≈0.51–0.54, v≈0.40 and v≈0.75–0.83) as register marks.
- **Core** (u≈0.74, v≈0.64): a blue disc of ~12 concentric rings (≈43 mm diameter) with a V-shaped opening of ~70° pointing up, in which sit ~8 black radial ticks; a black circle around it; a tiny crimson spiral dot at the exact centre inside a blank ring; an outer crimson circle (≈53 mm diameter) whose top carries a crown of short crimson ticks pointing in/out (one thick tick at ~65°); a crimson radial stub drops from its bottom.
- **The corridor** (the one overlap): a thick straight **blue** line from u≈0.41, v≈0.70 (outside the disc, in the crescent) to the core at ~170°, slicing every band; every ring it crosses has a gap at its edge. A **crimson** line runs from the core outward along the corridor's other edge and stops at u≈0.60, v≈0.59 with a chevron and a short crimson hairline tie across. Along the corridor's outer bands, a comb of ~20 short black horizontal rungs (u≈0.43–0.49, v≈0.52–0.72).

**Type column (left 33 %, Swiss flush-left).**
- `THE MIRROR` / `FORGETS` — giant stroke type, two lines, u 0.036–0.33, v 0.05–0.17 (≈13 mm caps, real stroke weight).
- Top-right data block, right-aligned to u≈0.97, v 0.13–0.17: `paper the gate leaves blank   52 %` / `of what fired, gradient re-enters   47 %` / `ring pitch   1.02 mm`.
- Full-width rule at v≈0.186 (u 0.036–0.97).
- v≈0.21: `a convolutional network / both passes. one set of rings`.
- Stage table (u 0.036–0.32, v 0.24–0.40), bracketed by rules: header `rim ——→ core`, columns `cells` / `channels`; rows `x 256 × 3 input`, `a1 256 × 6 conv relu`, `p1 128 × 6 max pool 2`, `a2 128 × 12 conv relu`, `p2 64 × 12 max pool 2`, `z 9 softmax / L`; beside each row a cell comb (halving: 14 → 14 → 7 → 7 → 4 bars) and a channel comb (doubling: 3 → 6 → 6 → 12 → 12).
- In the crescent (u 0.33–0.44, v 0.45–0.52): `forward` over a black → arrow, `gradient` (crimson) over a crimson ← arrow, `1/16 of the field`.
- Paragraph, v 0.56–0.67: `rings are layers. inward is the forward pass. / outward the gradient. every pool halves the angular / cells and doubles the channels: resolution traded for / depth until the whole field is one number. / blank paper is relu. and it is blank on BOTH passes. / pooling keeps one cell per window. so the return can / re-enter only the cells the outbound remembered.`
- Rule, then crimson line v≈0.70: `the corridor:  out 117 mm   back 38 mm   32% (median angle)`.
- ReLU strip v 0.73–0.78: a black wiggly response line on a baseline with crimson segments under the closed stretches; `relu  y = max(0, x)` and `crimson = the closed wedges`.
- Pool/unpool combs v 0.86–0.90: a black comb of 16 ticks → 8 ticks, a crimson comb beneath with gaps; `max pool 2`, `unpool: one cell per window`.
- Footer v≈0.91: `3 pens   seeded   a3 landscape` … `C N N`.

### faithful v10 — two registers after the reference
- **Top register (forward), v 0.06–0.40.** `forward` / `pass` / `(activations)` with a → arrow at u 0.04–0.10, v 0.13–0.20. Input plate `X` (u 0.04–0.11, v 0.22–0.31) filled with blue dotted ripples; label `X` / `H × W × C`. Six stage headers at v≈0.07 with parenthetical sub-lines: `convolution (kernels as wave filters)`, `feature maps (frequency responses)`, `non-linearity (ReLU)`, `pooling (downsample)`, `deeper layers (more abstract spectra)`, `classifier (linear + softmax)`. Under each header a stack of 3–5 tilted parallelogram planes (≈0.04 wide each) in shallow axonometric: concentric contours (conv, u≈0.20–0.28), wave trains (feature maps, u≈0.34–0.41), half-wave arches with blank lower halves (ReLU, u≈0.48–0.55), vertical tick lattices (pooling, u≈0.61–0.67), `•••` (u≈0.74), a deeper stack of horizontally-lined planes (u≈0.76–0.83), a tall narrow classifier bar of glyph marks (u≈0.87), then `softmax` with seven small circles `p₁ p₂ p₃ ⋮ p_K` — `p₃` filled blue with a blue tie. One plane per stack is blue. A thick **blue ribbon** weaves left→right through all the stacks at v≈0.24–0.30; a lens-shaped bundle of long dashed black and blue flow curves envelopes the whole register (v 0.16–0.36), pinching between stacks. Tensor shapes at v≈0.37–0.39: `A¹ H × W × C′`, `R¹ H × W × C′`, `P¹ H/2 × W/2 × C′`, `A^L H/2^L × W/2^L × C^L`, `W^c C^L × K`; kernel swatches `W¹ k × k × C × C′` (three small squares, one blue) at u≈0.18–0.30, v≈0.36–0.40.
- **Register gutter, v 0.43–0.50**: short vertical dotted ties at every column.
- **Bottom register (backward), v 0.51–0.83.** Crimson labels at v≈0.51: `∂L/∂(conv) (filter gradients)`, `∂L/∂A¹`, `∂L/∂(ReLU) (mask)`, `∂L/∂P¹ (unpool)`, `∂L/∂A^L`, `∂L/∂z`, `∂L/∂W^c (classifier gradients)`. `backward` / `pass` / `(gradients)` with ← arrow at left. Same columns, planes carry crimson hatch/contour textures with blank gated patches; a thick **crimson ribbon** runs right→left; crimson+black dashed flow envelope. `∂L/∂x` plate of crimson dots (u 0.04–0.11, v 0.63–0.72); `∂L/∂W¹` swatches (one crimson) at v≈0.80; right end: 7 dots → 7 small line-filled squares, one crimson. Row of annotations at v≈0.83: `∂L/∂A¹`, `1 (A¹>0)`, `1 of 2×2`, `H/2^L × W/2^L × C^L`, `p − y`.
- **Legend strip, v 0.86–0.95**, five cells split by vertical rules: `convolution = local correlation (in frequency domain)` grid `*` wave `=` wave; `non-linearity (ReLU)` axes + crimson kinked line `y = max(0, x)`; `pooling (e.g. 2 × 2)` 4×4 grid → 2×2; `softmax` fan into a dot column `σ(z)`; `loss (e.g. cross-entropy)` `L = − Σᵢ yᵢ log pᵢ`. `C N N` bottom right; registration crosses at the corners.

### mechanism v9 — the true computed CNN
- Same two-register layout. Giant rotated stroke type `FORWARD PASS` (black, u≈0.04, v 0.17–0.40) and `BACKWARD PASS` (crimson, u≈0.04, v 0.56–0.78) replace the small labels; small `activations →` and `gradients ←` beside them.
- **Forward**: input `X 24 × 24 × 1` a dot-matrix square (u 0.05–0.15, v 0.17–0.30) of solid and hollow dots; stacks of 4 tilted planes with real marching-squares contours (front plane blue): conv/feature maps (u≈0.18–0.28), `A1 20 × 20 × 4` (u≈0.32–0.43), `R1 20 × 20 × 4` (u≈0.46–0.57, thick contours with blue front), `P1 10 × 10 × 4` (dot lattices, u≈0.61–0.69), `• • •`, `A2 8 × 8 × 6` (u≈0.76–0.84, small blob contours), `Wc 96 × 6` classifier bar of horizontal ticks (u≈0.88). Between stacks: dotted hourglass fans that pinch at the midpoint. Softmax column (u≈0.94–0.97, v 0.17–0.38): `p1`…`p6` as discs whose area is the probability — p1 a large filled blue disc, p2/p3 near-invisible specks, p4–p6 growing spiral black discs. Kernel swatches `W1 5 × 5 × 1 × 4` at v≈0.44–0.49.
- A full-width black rule at v≈0.51 with a tick under every column — the mirror line. Crimson stage labels just below it.
- **Backward**: `∂L/∂x` a crimson frame with a sparse cluster of crimson dots (u 0.05–0.15, v 0.57–0.71); crimson contour stacks under each column — `∂L/∂(conv)`, `∂L/∂A1` (small isolated crimson blobs), `∂L/∂(ReLU) (mask)` (dense concentric contours), `∂L/∂P1 (unpool)` (sparse dots), `∂L/∂A2` (nearly empty planes), `∂L/∂Wc (96 × 6)` crimson bar, `∂L/∂z (per-class tiles)` six small squares with hatch density ∝ gradient. `∂L/∂W1` crimson swatches at v≈0.73–0.77.
- **Legend strip** v 0.80–0.92, five cells in ~1.2 mm type: `row 12 of X * centre row of kernel 1 = the drawn result` with three real signal traces; ReLU axes with `alive 782 of 1600 = 0.489` / `gradient killed 59 of 368` (crimson); `R1 patch (rows 6–9)` 4×4 → 2×2 with `the gradient returns to the red cell only`; softmax table `p1 0.533 … p6 0.296`, `sum p = 1.000`; `argmax = class 1, target = class 6`, `L = − log p6 = 1.2178`, `∂L/∂z = p − y` with values. `C N N` bottom right.

## The science it encodes
All three: one CNN pass and its backprop — conv → ReLU → max-pool → deeper → linear+softmax → loss, and the gradient retracing it. The brief's invariants: column registration of forward/backward twins; ReLU backward is a mask (blank where forward was zeroed); unpool scatters to one cell per window; spatial dims shrink while channels grow; softmax is normalised with one winner.
- **abstract** (`r03/NOTES.md`): exact mapping — angular cell count = spatial resolution (256·256·128·128·64, halves at each pool); radial sub-rings = channels (3·6·6·12·12); radius = depth; arc duty = |activation| (spacing fixed, tone drives duty); blank paper = ReLU closed, same angle on both halves (∂ReLU is the forward indicator); crimson broken where black is continuous = max-unpool; core sector angle = softmax probability; crown tick direction = sign of p − y. All stages share one Fourier-coefficient set truncated per stage, so the big voids align rim-to-core (that alignment IS the low-pass). Measured and printed: 52 % blank, 47 % re-entry, corridor out 117 mm / back 38 mm = 32 % at the median angle of 256 candidates. The field itself is synthetic (seeded Fourier), not a trained net.
- **faithful** (`r01/NOTES.md`): one scalar field `f(u,v)` plays A¹; R¹ = max(0,f), P¹ = maxpool, unpool at argmax, ∂L/∂A¹ = ×1[f>0] — the ReLU mask covers 47.3 %, and softmax of fixed logits gives p₃ = 0.556. Visually the mask is hard to read through the flow bundles.
- **mechanism** (`r02/NOTES.md`, `net.py`): a real small numpy CNN on a 24×24 input, one honest forward and backward pass. The twist: the net is **wrong** — predicts class 1 (p = 0.533), target is class 6, L = 1.2178. Numbers on the sheet are the checkable outputs of `net.py`.

## How it got here
- **faithful r01** v1→v10: dash periods opened 2.65 → 4.8 mm to cut ~800 pen cycles; kept as a recreation.
- **mechanism r02** v1 → v9: v1 had small `forward pass` labels and tight solid-curve connectors between stacks; v6 introduced the giant rotated `FORWARD PASS` / `BACKWARD PASS` type and dotted hourglass fans and larger softmax discs; v9 is v6 refined.
- **abstract r03** v1 → v10: v1 welded live cells (magnitude invisible), six crossing leader lines, 25 clamped bounds violations. v2 separated forward/backward duty ranges, deleted all leaders, set the 1.15 / 6.0 mm band gaps (the 5:1 ratio makes a band read as one object). v2's render still had a blue **spiral thread** and a purple overlap arc plus long radial spokes — v4 cut them and folded them into the **corridor**. v5 corridor reported 100 % return (wrong story); v6 placed it at the median of 256 candidates → 32 %. v7 added the halving/doubling combs to the stage table ("the single biggest legibility win"). v8–v10: 52 % blank instead of 48 %, input band opened to fine tonal texture, corridor caption moved off the shared baseline. Juan, on v10: **"i love this one!"** — "Rings are layers, inward is the forward pass, outward the gradient; blank paper is ReLU on BOTH passes. This is the keeper for cnn-passes."

## Keep — what works

### abstract v10
- The **radial collapse** as the order: a 262 mm disc cropped at the right and bottom frames vs a 165 mm type column — one dominant mass at 3 m, extreme scale contrast (13 mm headline against 2.3 mm captions).
- The **upper-right blank wedge** (u 0.76–0.95, v 0.25–0.58) is the plate's quiet zone *and* its data: ReLU's closed angle, aligned across every band.
- **5:1 gap ratio** (1.15 mm inside a band, 6 mm between bands): each band reads as one black/crimson pair.
- **Pen economy**: black 77 %, blue 11.5 %, crimson 11.7 % — blue only where the tracked channel fires, so blue and crimson stay scarce and loud.
- **The corridor** at u≈0.41–0.74, v≈0.59–0.70: the only overlap on the sheet, with analytic gaps where it crosses rings; blue runs whole to the core, crimson stops short with a chevron — the punchline is a length.
- The **printed measured numbers** (52 % / 47 % / out 117 back 38 / 32 %) — the twist is measured, not asserted.
- The **halving cell comb beside the doubling channel comb** in the stage table.
- The core: blue elected sector with an open V wedge, crimson crown of sign ticks — the whole net ends as one number.

### faithful v10
- Strict **column registration**: every forward stack has its gradient twin at the same u, tied by dotted verticals across the v 0.43–0.50 gutter.
- The two ribbons (blue → on top, crimson ← below) give each register one dominant line.
- The legend strip's five equal cells with vertical rules and one shared baseline.

### mechanism v9
- Giant rotated `FORWARD PASS` / `BACKWARD PASS` on the left edge — the only large type in the two-register family.
- **Softmax as disc area** (big blue p1, specks for p2/p3, growing black p4–p6) and the per-class hatch tiles below — normalisation readable without numbers.
- The **backward planes visibly sparsen** column by column (∂L/∂A2 almost empty, unpool as isolated dots) — the brief's "sparser than its forward twin" holds.
- The wrong-answer twist (class 1 predicted, class 6 true) with real numbers.

## Weak — what doesn't

### abstract v10
- [concept] The per-band pairing (same blank angle on black and crimson halves) needs the 1 m read; at 3 m the crimson half reads as "sparser" but not as "the same address" (the notes' own critique).
- [concept] `forward` / `gradient` arrows and `1/16 of the field` in the crescent (u 0.33–0.44, v 0.45–0.52) are pure key — the only place the plate explains rather than shows.
- [craft] The comb of ~20 black rungs left of the outer bands (u 0.43–0.49, v 0.52–0.72) reads at a glance as tick marks on a gauge, not as a slice through the lattice.
- [space] The straight black register rules at the wedge edges (u≈0.51–0.54, v≈0.40 and v≈0.75–0.83; u≈0.83–0.90, v≈0.62) float on blank paper and read as stray strokes.
- [grid] The stage table ends at u≈0.32 but the crimson corridor caption runs to u≈0.39 and the crescent key hangs at u 0.33–0.44 on its own axis.
- [depth] Flat by declared Swiss decision (radius is the depth axis) — acceptable, noted.

### faithful v10
- [concept] It is the reference: labelled stages, arrows, tensor shapes, a legend strip — a textbook figure by § 6 (≤ 3).
- [space] The dashed flow envelopes cross through the stacks and each other (u 0.30–0.55, v 0.15–0.35 is a thicket of blue/black dashes over plane faces) — collision, not overlap.
- [hierarchy] Everything is mid-sized: 12 stacks of similar size, all type at 1.5–2.5 mm; nothing dominates.
- [craft] The ReLU mask, the plate's key claim, is illegible under the flow; ~3,000 pen cycles are flow dashes; travel (28 m) exceeds draw (24 m).

### mechanism v9
- [concept] Still the two-register schematic with stage captions and a legend strip; the truth of the numbers does not change what the viewer sees.
- [craft] The legend strip's ~1.2 mm type (v 0.80–0.92) and the stage sub-captions are below reliable pen legibility.
- [hierarchy] Planes, fans and swatches all at one scale; the only mass is the rotated register titles.
- [tension] Two identical horizontal bands mirrored across a centre rule — calm, symmetric.

## Next versions
- **one-envelope** (abstract) — Branch v11 from `r03/piece.py` (never the frozen file). Per the notes' own proposal: give each band's black and crimson halves ONE shared hairline envelope that traces each open wedge across both halves, so a gate's void is a single closed shape spanning forward and backward. Delete the crescent key; let chevrons on the corridor carry direction alone. The registration claim moves from the 1 m read to the 3 m read — the one thing Juan's keeper still leaves to furniture.
- **wrong-answer mirror** (mechanism × abstract) — Feed the r02 `net.py` arrays into the r03 polar lattice: real activations drive arc duty, the real ReLU mask cuts the wedges, and the core shows the *wrong* elected class in blue with the true class's sector in crimson. The mirror forgets AND the net was wrong — a double punchline on an order Juan already approved.
- **mirror-fold** (lens) — Fold the faithful two-register plate into one: forward stacks above a horizontal axis, gradient twins hanging *as reflections* beneath it, each reflection drawn only in the cells that survive unpool and ReLU (blank paper where the mirror forgets). Drop the flow envelopes, captions and legend strip; the axis is the only rule. Removes the schematic furniture while keeping column registration exact.
- **If only iterating:** (on the approved abstract, in a v11 copy)
  1. Draw a crimson-and-black hairline that closes each of the three widest blank wedges across both halves of every band, so the aligned voids read as one shape per band at 3 m.
  2. Remove the `forward` / `gradient` / `1/16 of the field` block from the crescent (u 0.33–0.44, v 0.45–0.52) and end the blue corridor with a chevron at the rim.
  3. Delete the free-floating straight register rules at the wedge edges, and snap the corridor caption's right edge to the stage table's right edge (u≈0.32).
