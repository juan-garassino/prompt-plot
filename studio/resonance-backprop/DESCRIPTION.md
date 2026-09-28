# ATTENTION AS RESONANCE (forward + backward) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/res_backprop` |
| current render | `gallery/studio/res_backprop/current/pp_res_backprop_v8.png` · `gallery/studio/res_backprop/current/pp_res_backprop_v5.png` |
| source | `studio/resonance-backprop/rounds/r01/piece.py::attention_as_resonance` |
| reference | `studio/resonance-backprop/ref/reference.png` |
| paper · pens | A4 portrait, cream · 0 crimson = Q, ∂L/∂Q · 1 blue = K, ∂L/∂K · 2 ochre = V, ∂L/∂V · 3 green = Z, ∂L/∂Z · 4 black = interference, softmax, ∂L/∂A, rails, type, corner crosses |
| status | unreviewed (no FEEDBACK.md) · 8 renders on disk |

## In one line
Attention and its gradient drawn as **interfering waves folded about a horizontal mirror**: the forward pass (Q, K packets → two-source Huygens interference → softmax → Z = AV) fills the upper half, and the backward pass (∂L/∂Z → ∂L/∂A → ∂L/∂Q, ∂L/∂K, ∂L/∂V) re-draws the same packets inverted below, with a vertical rail at the left labelling "forward pass" down and "backward pass" up. The two current renders differ only in the hero's outer tonal field: **v5** has wide dotted ellipse halos and dense scatter, **v8** has a tight oval of dashed crest arcs.

## What is on the sheet
Coordinates are (u, v) on the 210 × 297 sheet.

- **Frame furniture.** Four registration crosses at (0.07, 0.11), (0.94, 0.11), (0.07, 0.89), (0.94, 0.89), with dotted ticks and dots below the top pair. Title `ATTENTION AS RESONANCE` spaced caps, centred, v 0.11, with a rule and midpoint dot. Subtitle `frequency interference • selection • backpropagation` in lowercase at v 0.14.
- **Left rail.** A vertical black bar at u 0.07. Upper half: a T-bar at v 0.19, the rotated label `forward pass`, and an arrow down to v 0.43. Lower half: an arrow up from v 0.85 to v 0.62, with the rotated label `backward pass`.
- **Q (upper-left).** Five crimson rows at v 0.19–0.29, u 0.10–0.36, with `Q` at (0.14, 0.16). The packets' amplitude exceeds the 3.5 mm row pitch, so adjacent rows' packets interpenetrate into a crimson braid at u 0.20–0.30. Node circles sit on columns at u 0.14 and u 0.28, and dotted fans descend to the hero.
- **K (upper-right).** Mirror position u 0.64–0.90, blue, with `K` at (0.87, 0.16). The same interpenetration happens at u 0.70–0.82.
- **Fraction** `Q · Kᵀ` / `√d_k` at (0.50, 0.22–0.25), with a dotted centreline through it.
- **Interference hero** at v ≈ 0.35. Two compact bullseyes of ~9 solid rings centred at (0.35, 0.35) and (0.64, 0.35), each ~20 mm across. Between them lies a flat oval "comb" of dense vertical fringe arcs (u 0.42–0.58, ±6 mm), which reads as a near-solid black lozenge. A horizontal axis runs through all three.
  - **v8**: an oval of dashed crest arcs around the whole figure (u 0.26–0.74, v 0.30–0.41) plus a few dots.
  - **v5**: much wider dotted ellipse halos (reaching u 0.10–0.90, v 0.28–0.43) plus a dense seeded dot scatter that greys the whole band.
  - Nine black droplines fall from the figure to the softmax row.
- **Softmax.** `A = softmax(QKᵀ/√d_k)` centred at v 0.45. A black baseline at v 0.49 (u 0.32–0.70) carries five sharp peaks with open apex circles.
- **V (mid-left).** Four ochre rows at v 0.48–0.54, u 0.08–0.27, again interpenetrating, with `V` at (0.12, 0.46). Dotted ochre fans sweep right under the softmax to the Z row, some looping round its right end at u 0.83.
- **Z.** A green axis at v 0.57 from u 0.17 to u 0.83. One large packet centred at u 0.50 (±14 mm, v 0.52–0.62) with a dashed diamond envelope. `Z = AV` is set below it at (0.50, 0.62).
- **Backward half.**
  - `∂L/∂Z` (green) at (0.50, 0.65), with a smaller green packet row at v 0.71 (u 0.41–0.60). Two tall dotted green arcs rise from it back to the Z row at u 0.35 and 0.65. Eight dotted green arrows fan outward left and right.
  - `∂L/∂V`: two ochre rows at the far right, u 0.78–0.90, v 0.69–0.71, labelled at (0.95, 0.70).
  - `∂L/∂A` (black) at (0.50, 0.78), over a 5-peak black row at v 0.83 (u 0.37–0.64). In v8 dotted black arrowheads point out and up from the outer peaks.
  - `∂L/∂Q`: three crimson rows at u 0.10–0.29, v 0.80–0.84, labelled at (0.11, 0.78). `∂L/∂K`: mirror blue rows at u 0.72–0.90, labelled at (0.89, 0.78). Both are reached by dotted arrowed fans.
- **Empty foot.** Below the lower crosses (v 0.89–0.97) the sheet is bare.

## The science it encodes
From `rounds/r01/NOTES.md`: the hero is the approved Huygens crest construction from `studio/resonance` (ridges of cos(k r₁)/√r₁ + cos(k r₂)/√r₂, crest loci r_s = m·L). Here the sources are wider apart (d = 352 ref px), so the multiplier became **d = 59·L** (L ≈ 1.04 mm) to keep the physical pitch. Tone is split three ways: m 1–9 solid (bullseyes), m 10–50 solid clipped to a central lens (the comb), and m 10–63 step 3 dashed in an oval (the tonal field). The `_Guard` crossing-safe cull (0.82 mm and 25°) is ported verbatim. Packet rows are traced off the reference (colour-segmented row scans), not computed from weights. The backward band is new layout. The notes argue arrowheads are correct here because "it marks gradient direction, not projection". A reproduction round: 55k commands, 11.4 m draw, 11.9 m travel, 4 054 pen cycles (v8).

## How it got here
- **v1**: with d = 35·L the pitch was 1.66 mm and the hero came out as two plain bullseyes. The switch to 59·L restored the comb.
- **v4 → v5**: a wide dotted halo field was introduced.
- **v6**: tightened.
- **v7**: heavy dashed concentric ellipses around the hero, the loudest version.
- **v8**: the dashed field pulled in to a tight oval.

The two currents are the two tonal-field theses (wide dotted vs tight dashed). The composition has been fixed since v1. No feedback from Juan.

## Keep — what works
### v8
- The tight dashed oval keeps the hero compact, so the page's centre of mass is the hero and not a grey band.
### v5
- The wide dotted halo is the closest pen reading of the reference's soft tonal field around the figure.
### both
- The fold: the forward half and its inverted backward echo, with `∂L/∂Z` directly under `Z = AV`, is the plate's one structural idea, and it reads at 1 m.
- The comb lozenge between the bullseyes is a real crest-crossing structure and the densest, most "resonant" mark on the sheet.
- The left rail's two arrows (`forward pass` down, `backward pass` up) give the sheet an edge-to-edge axis.
- The corner crosses and the centred title are a coherent engraving-plate frame.

## Weak — what doesn't
- [craft] **DOTTED LINES — Juan's note of 2026-09-28** ("should be more continuous dots"; see FEEDBACK.md). Measured on the family's `_dash_mm`: the pitch is already regular (2.22 mm ± 0.05, straight or curved), so spacing is not the fault. The fault is the mark and the gap: each 'dot' is a 0.42 mm micro-dash followed by 1.8 mm of paper, which reads as a broken dashed line, and where dotted leaders converge (Q/K fans into the field, the gradient rails) dots from neighbouring paths interleave into noise. Fix: one round dot of a single fixed size (a pen touch or a tiny closed circle, never a micro-dash), centre-to-centre pitch ≈ 0.9–1.1 mm so the line reads as continuous, pitch end-anchored so both ends carry a dot, the same pitch family-wide, and converging dotted paths spaced ≥ 2 pitches apart. Judge it on the preview at the real nib width. Plot time may grow — Juan accepts that; do not trade the dots for dashes or hairlines.
### both
- [concept] Schematic. Arrowed fans, stacked fractions and labelled stages are a backprop diagram. Only the hero is an order. § 6 caps this at ≤ 3.
- [craft] Packet rows in every block (Q, K, V, ∂L/∂Q, ∂L/∂K) have amplitudes larger than the row pitch, so neighbouring rows cross into braided knots (crimson at (0.20–0.30, 0.19–0.29), ochre at (0.10–0.20, 0.48–0.54)). The reference keeps rows apart. This is collision, not overlap by decision.
- [craft] The central comb is a near-solid black lozenge (fringes under 1 mm across a ±6 mm oval). It floods on paper.
- [hierarchy] Hero ~50 mm wide (v8) against Q/K blocks ~55 mm each and a ~140 mm Z row: the widest element is the Z axis, not the hero.
- [tension] Mirror-symmetric about u 0.50 top and bottom, with a centred title and centred Z.
- [space] Everything is packed between v 0.11 and v 0.89, yet the foot v 0.89–0.97 is dead, unshaped paper. The backward half is a thicket of dotted arrows (v 0.62–0.85).
### v5
- [space] The dotted halo and scatter grey the whole band from u 0.10 to 0.90 and collide with the Q/K fans and the V fans.
### v8
- [craft] Dashed crest arcs break into short dashes at random phase, which looks like noise, not tone.

## Next versions
1. **the fold** (abstract) — make the mirror the whole plate. One interference field in the upper half and its exact inverted twin in the lower half (the gradient is the same field read backwards), meeting at a single horizontal loss line across the sheet. Delete the packets, fractions and arrows. The rail stays as the only type. A NESTED/INTERFERING order with a real symmetry that is the mechanism, not a layout habit.
2. **gradient-as-phase** (mechanism) — keep one hero and draw backprop as a phase shift. The backward crests are the forward crests offset by half a wavelength in a second colour, so where the gradient is large the two families interleave and cross. One sheet, two pens, and the backward pass is visibly the same wave travelling back.
3. **reference-clean** (faithful) — keep the reproduction and fix the craft: scale every packet amplitude to at most 0.45 × row pitch so rows never touch, cap the comb at 1.2 mm fringe pitch, and use the v8 field.

**If only iterating:**
1. Cap every packet's amplitude at 0.45 × its row pitch, so no two rows' packets touch anywhere in Q, K, V, ∂L/∂Q or ∂L/∂K.
2. Thin the central comb so fringes are at least 1.0 mm apart. It must read as a striped lozenge, not a black one.
3. Move the whole composition down so the lower crosses sit at v 0.95, and spend the recovered ~20 mm on an extra row gap between Z and `∂L/∂Z`.
