# ATTENTION AS RESONANCE (FFN) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/res_ffn` |
| current render | `gallery/studio/res_ffn/current/pp_res_ffn_v9.png` · `gallery/studio/res_ffn/current/pp_res_ffn_v5.png` |
| source | `studio/resonance-ffn/rounds/r01/piece.py::attention_as_resonance_ffn` |
| reference | `studio/resonance-ffn/ref/reference.png` |
| paper · pens | A4 portrait, cream · 0 crimson = Q, ∂L/∂Q · 1 blue = K, ∂L/∂K · 2 ochre = V, ∂L/∂V · 3 green = Z, ∂L/∂Z · 4 violet = FFN stages, Y, ∂L/∂Y · 5 black = interference figures, softmax, title, FFN bracket |
| status | unreviewed (no FEEDBACK.md) · 9 renders on disk |

## In one line
The `resonance` plate with its MoE fork swapped for a feed-forward block, drawn as **interfering waves then a pinched streamline bundle**. The top half is identical to v13 (Q, K packets → two-source Huygens interference → softmax). Below, Z = AV runs into expand → nonlinearity → project → Y, and one backward row mirrors it all at the foot, including a miniature second interference figure for ∂L/∂A. The two current renders are near-identical: **v5** has cramped/condensed small type and a bulb-shaped nonlinearity; **v9** has cleaner lowercase glyphs and a barrel-shaped nonlinearity.

## Lede
Attention drawn as **resonance between two wave families**, followed through a feed-forward block and back again as gradients.

## On the sheet
The upper half shows crimson query and blue key wave packets converging on a black two-bullseye interference figure at the centre, with a softmax row below. Lower on the sheet an ochre value knot and a green output packet lead right into a bracketed feed-forward block of violet strokes. A smaller copy of the interference figure and stacked gradient labels run along the bottom.

## The science
The interference figure is computed from crest circles of two point sources, cos(k r₁)/√r₁ + cos(k r₂)/√r₂. The feed-forward block is a fan of lines that flatten at the top like a tanh squash; going backward, each line gets the same notch, standing for the derivative. Wave packets and labels are traced from a reference, not model weights.

## What is on the sheet
Coordinates are (u, v) on the 210 × 297 sheet.

- **Top half (v 0.06–0.62), as in `resonance` v13.** The title with a rule and dot at v 0.06–0.08. Crimson Q (u 0.09–0.36) and blue K (u 0.64–0.91) blocks of five packet rows at v 0.14–0.30, with big `Q` and `K` at v 0.12. Twenty dotted fans converge on the hero. The `Q · Kᵀ / √d_k` fraction sits at (0.50, 0.28–0.31). The two-bullseye crest figure is centred at (0.40, 0.44) and (0.60, 0.44), with its small midline lens clusters, dotted ellipses, scatter dots and stipple caps. `softmax` at (0.50, 0.57), and a six-peak black softmax row on a baseline at v 0.61 (u 0.27–0.74).
- **V (mid-right).** Five ochre rows at v 0.65–0.72, u 0.63–0.91, with `V` at (0.88, 0.62). The central packets overlap heavily into one ochre knot at u 0.73–0.80. Dotted ochre curves fall from the softmax nodes down-right into V, and down-left to Z.
- **Z row.** Green `Z = AV` at (0.29, 0.74). A green axis at v 0.78 from u 0.19 to u 0.63, with a big packet centred at u 0.46 (±14 mm, v 0.73–0.83) and dotted continuations left.
- **FFN block (right, same axis).** A black bracket with `FFN` centred on it at (0.76, 0.74), spanning u 0.63–0.85. Three violet stages sit between pinch nodes:
  - `expand`: a packet at u 0.63–0.71.
  - `nonlinearity`: a bundle of ~7 streamlines pinched to points at both ends, forming a flat-topped dome at u 0.72–0.78 between two dotted vertical guides.
  - `project`: a packet at u 0.79–0.85.
  - Stage names in small lowercase at v 0.82. Then an open circle, `Y` at (0.90, 0.75), and a dotted continuation.
- **Backward row (foot, v ≈ 0.88).** Left: a stacked column of `∂L/∂Q` (two short crimson rows, v 0.83–0.86), `∂L/∂K` (two blue rows, v 0.88–0.90), `∂L/∂V` (one ochre row, v 0.93), at u 0.08–0.28. Each has a left arrowhead, and rows within a colour overlap each other. Centre: a miniature two-bullseye interference figure at u 0.38–0.47 (~18 mm wide), labelled `∂L/∂A` below at (0.42, 0.93). Then a green `∂L/∂Z` packet at u 0.55–0.63 with its label at (0.59, 0.94). Then the violet FFN mirrored: `projectᵀ`, `nonlinearity′` (now with twin peaks and a central notch), `expandᵀ` at u 0.64–0.88, labels at v 0.93. `∂L/∂Y` at the far right (0.93, 0.88). A dotted green curve drops from the Z row to ∂L/∂Z, and a dotted violet curve from Y to ∂L/∂Y.
- **Empty foot.** v 0.95–0.97 bare.

## The science it encodes
From `rounds/r01/NOTES.md`: the hero is the approved crest construction reused verbatim (d = 35·L, pitch 1.21 × 1.41 mm). The ∂L/∂A figure is the same object at 0.39 scale with d = 14·L (L = 6.93 ref px, 1.17 mm pitch), keeping the hero's proportions (m_solid/n = 0.60, clip a/d = 1.09, b/d = 0.63), so "it reads as the same object shrunk". **The FFN fan** is the one new construction: offset_k(u) = a_k·sin(πu)^{p_k}. Forward passes through tanh(c·v)/tanh(c) with c = 1.75 (the flat top of a squashing nonlinearity). Backward subtracts an absolute notch D·exp(−((u−½)/w)²), with D = 0.26·amp identical for every line, so the family never crosses: that twin-peak dip "is the derivative". Packet rows are traced off the reference. Plot stats (v9): 63.5k commands, 12.1 m draw, 12.2 m travel, 6 pens.

## How it got here
- **v1–v3**: early layout passes (not sampled).
- **v4, v6, v7, v8**: the same composition throughout. Changes are in the FFN fan (notch made absolute instead of scaled, which cut backward crowding 82 % → 62 % per the notes) and in the small-type glyphs.
- **v5 and v9 are both kept current**: the type/fan variants.

No feedback from Juan.

## Keep — what works
### v9
- The cleaner lowercase for `expand / nonlinearity / project` and the transposes. Keep v9's type.
### both
- The FFN nonlinearity fan: forward dome vs backward twin peaks is a genuinely new mark, not a packet, and the derivative is visible as a shape change. It is the best idea this sibling adds to the family.
- The ∂L/∂A mini-interference echoes the hero at 0.39 scale: a real rhyme between forward and backward.
- The top half inherits the benchmark's funnel and hero intact.
- One axis carries Z → FFN → Y across the whole lower sheet at v 0.78, a strong horizontal.

## Weak — what doesn't
- [craft] **DOTTED LINES — Juan's note of 2026-09-28** ("should be more continuous dots"; see FEEDBACK.md). Measured on the family's `_dash_mm`: the pitch is already regular (2.22 mm ± 0.05, straight or curved), so spacing is not the fault. The fault is the mark and the gap: each 'dot' is a 0.42 mm micro-dash followed by 1.8 mm of paper, which reads as a broken dashed line, and where dotted leaders converge (Q/K fans into the field, the gradient rails) dots from neighbouring paths interleave into noise. Fix: one round dot of a single fixed size (a pen touch or a tiny closed circle, never a micro-dash), centre-to-centre pitch ≈ 0.9–1.1 mm so the line reads as continuous, pitch end-anchored so both ends carry a dot, the same pitch family-wide, and converging dotted paths spaced ≥ 2 pitches apart. Judge it on the preview at the real nib width. Plot time may grow — Juan accepts that; do not trade the dots for dashes or hairlines.
### both
- [concept] Schematic, as with every attention sibling. Labelled stages, a bracket, fractions and arrowheads make a transformer-block diagram (§ 6 ≤ 3).
- [space] The lower third is jammed. V rows (v 0.65–0.72), the Z packet (to v 0.83), the FFN labels (v 0.82) and the backward row (v 0.83–0.95) leave no gap over 3 mm. The Z packet's lower envelope nearly meets the ∂L/∂Q rows at u 0.30–0.45.
- [craft] Packets overlap within the V block (ochre knot at u 0.73–0.80) and within the ∂L/∂Q / ∂L/∂K pairs, which are collisions. The FFN bracket's right leg lands on the `project` packet at (0.85, 0.74).
- [hierarchy] The hero is ~20 % of the sheet width and the Z packet is as tall as the hero's rings. Nothing dominates. The heaviest ink is the hero plus the ochre knot, which is an accident.
- [tension] Top-half mirror symmetry and centred title, the same as the benchmark.
- [craft] Six pens / five swaps.
### v5
- [craft] The small type is condensed until glyphs touch (`nonlinearity`, `softmax`), which is illegible at 30 cm.

## Next versions
1. **the squash** (abstract) — make the FFN fan the plate. A single wide streamline bundle across the sheet, fed on the left by the interference field's crest intensities (the attention output), squashed through tanh in the middle (the flat top), and fanned out at the right. Below it, the same bundle with the derivative notch. Delete the Q/K blocks, the fractions and the stage names. FLOW order, two or three pens, and one dominant form.
2. **two interferences** (mechanism) — build the plate on the rhyme this sibling discovered. The large hero on top and its 0.39-scale gradient twin below, the only two figures, joined by one FFN fan between them. The forward/backward relationship becomes the composition instead of a row of labels.
3. **ffn-clean** (faithful) — keep the reproduction and give the lower third room: drop V to three rows (as the benchmark), cap packet amplitudes at 0.45 × pitch, lower the backward row to v 0.92, and use v9's type.

**If only iterating:**
1. Reduce V to three rows with amplitude at most 0.45 × pitch, so the ochre knot at (0.73–0.80, 0.65–0.72) disappears.
2. Open a clear gap of at least 8 mm between the Z/FFN row's lowest ink and the backward row's highest ink. Shrink the Z packet to ±10 mm if needed.
3. Shorten the FFN bracket so both legs end on pinch nodes, not on packet crests, and lift `FFN` 2 mm clear of the bracket line.
