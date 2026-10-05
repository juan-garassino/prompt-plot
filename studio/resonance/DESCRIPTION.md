# ATTENTION AS RESONANCE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/resonance` (its trials also hold the `resonance-clean` sibling: `pp_resonance_clean_v1..v10`) |
| current render | `gallery/studio/resonance/current/pp_resonance_v13.png` (+ `.gcode`) |
| source | `studio/resonance/rounds/r01/piece.py::attention_as_resonance` (sibling: `studio/resonance-clean/rounds/r01/piece.py::attention_as_resonance`) |
| reference | `studio/resonance/ref/attention-as-resonance.png` |
| paper · pens | A4 portrait, cream · 0 crimson = Q · 1 blue = K · 2 ochre = V · 3 green = Z · 4 violet = MoE, Y, their gradients · 5 black = interference figure, softmax, title, fraction |
| status | unreviewed (no FEEDBACK.md). The sibling notes call its interference construction "APPROVED" and port it verbatim, which makes this plate the benchmark · 23 renders on disk (13 own + 10 `resonance_clean`) |

## In one line
A transformer block drawn as **interfering waves**: Q and K are rows of Gaussian wave packets whose dot product is shown as a real two-source Huygens interference figure (crest loci r = m·L, d = 35·L), then softmax peaks, Z = AV, a mixture-of-experts fork and a gradient band. Siblings: **backprop** replaces MoE with a full mirrored backward pass; **ffn** replaces MoE with an FFN stage and a single backward row; **clean** stops at Z.

## Lede
Attention drawn as **interference between two wave families**: queries and keys are wave packets meeting in a central ripple pattern, followed by a mixture-of-experts step.

## On the sheet
Crimson query packets sit top left and blue key packets top right, with dotted curves funnelling down into two black bullseyes of concentric rings at the centre. Below are a black softmax row of peaks, ochre value packets at mid-right, and a green output packet at lower left. Violet lanes fork through a router at lower right, and stacked gradient labels run along the bottom.

## The science
The central figure is computed, not drawn by hand: two point sources send out rings of wave crests, and the pattern marks where crests from both meet. The wave packets, softmax peaks, expert lanes and gradients are copied from a reference diagram rather than derived from a model, so they illustrate the idea instead of measuring it.

## What is on the sheet
Coordinates are (u, v) on the 210 × 297 sheet. The plate is bilaterally symmetric in its top half and reads top to bottom.

- **The interference figure (hero), centre.** Two bullseyes of solid black concentric crest rings centred at (0.40, 0.44) and (0.60, 0.44), each ~42 mm across, with ~0.8–1.4 mm ring pitch. Where the families cross down the midline (u 0.50) they cut small diamond/lens cells, stacked in two little clusters above and below the axis. A black horizontal axis runs through both centres (u 0.29–0.71), with open circles at the sources and ends. Around them: two sparse dotted ellipses per source (reaching u 0.21–0.79, v 0.35–0.51), seeded black dots of several sizes scattered over the rings, and a dotted stipple cap above and below the midpoint. Crimson and blue terminal dots from the fans land on its upper rim.
- **Q block (top-left).** Five crimson wave-packet rows at v 0.14, 0.18, 0.22, 0.26, 0.30, spanning u 0.09–0.36. Each row has 2–3 packets on a straight axis with a dashed envelope outline, `· · · ·` continuations to the left, open/filled nodes on a shared node column at u 0.14, and six dotted vertical guides capped with dots. A large crimson `Q` sits at (0.14, 0.12).
- **K block (top-right).** The mirror position, u 0.64–0.91, with its own (not mirrored) packets. A large blue `K` sits at (0.86, 0.12).
- **Convergence fans.** Two dotted Bézier curves per row, crimson from Q and blue from K, drop and converge on the hero's upper rim between u 0.40 and 0.60 (v 0.30–0.37). Together they draw a V-shaped funnel.
- **Fraction** `Q · Kᵀ` / rule / `√d_k`, centred at (0.50, 0.28–0.31), with a dotted ellipsis above.
- **Title**: `ATTENTION AS RESONANCE` spaced caps, centred, u 0.21–0.78, v 0.06, with a short rule and a midpoint dot beneath.
- **softmax.** The label `softmax` at (0.50, 0.55). Below it, a black baseline at v 0.62 (u 0.27–0.74) with six sharp peaks of different heights on stems, open/filled apex markers, and three ghost peaks. Dotted droplines tie it up to the hero.
- **V (mid-right).** Three ochre packet rows at v 0.54–0.59, u 0.60–0.90, and `V` at (0.88, 0.52).
- **Z = AV (lower-left).** Green label at (0.18, 0.71). One big green packet (±13 mm) on an axis at v 0.75 spanning u 0.09–0.44, its envelope marked with filled dots top and bottom.
- **MoE (lower-right).** `— MoE —` at (0.62, 0.66), with `experts`, `top-2` and `router` in violet. The router is a dot in two circles at (0.48, 0.75). Five violet lanes fork out: the top (v 0.71) and bottom (v 0.79) lanes are solid with packets, and the middle three are dotted ghosts. They converge into a second circled node at (0.76, 0.75), then comes the `Y` packet to u 0.90, with `Y` at (0.88, 0.71).
- **Backward band (bottom).** Left: five stacked fractions `∂L/∂Q` (crimson), `∂L/∂K` (blue), `∂L/∂V` (ochre), `∂L/∂A` (black), `∂L/∂Z` (green), in a column at u 0.09–0.12, v 0.82–0.95. Each has a left arrowhead, a dotted run to an open circle on a node column at u 0.28, and a dotted return curve sweeping up-right into the plate. Right: violet `∂L/∂Y`, `∂L/∂experts`, `∂L/∂router` at u 0.90–0.94, v 0.80–0.92, with a right-angled dotted routing skeleton and circle nodes.
- **Many dotted ochre / violet / coloured curves** criss-cross the lower half between softmax, V, Z and MoE.

## The science it encodes
From `rounds/r01/NOTES.md` and the docstring. **Wave packets**: f(x) = Σ Aᵢ·exp(−((x−cᵢ)/sᵢ)²)·cos(2π(x−cᵢ)/Lᵢ + pᵢ), with the envelope drawn dashed. The per-row parameters are traced off the reference, not derived from a model. **Interference**: the ridge lines of A = cos(k r₁)/√r₁ + cos(k r₂)/√r₂, i.e. crest circles r_s = m·L. Sources are separated by d = 35·L exactly, so crest m meets crest 35−m on the axis. Crests 1–21 are solid, 22–51 dotted, and L = 1.30 mm (1.21 across / 1.41 down after the 1.167× vertical stretch). A parallel-only `_Guard` (0.82 mm and 25°) keeps crossings and cut interference crowding from 27 % to 3.3 %. The level-set approach (v1–v2) was rejected because it "draws every fringe twice and closes into a lattice of blobs". The dot field is sampled from |A| (1.1 + 22·|A|) plus 60 seeded scatter marks. Everything else (softmax peaks, MoE lanes, gradients) is reproduction of the reference diagram, not computation. It is a **reproduction** round ("no element was invented"), with 6 pens and 5 swaps, 10.3 m draw, 11.3 m travel, and 59k commands.

## How it got here
Round log in NOTES § 7:
- **v1**: level-set interference produced a stippled blob lattice (visible as a dense dotted mass), and a mirror bug meant K drew solid blue axis lines straight across the Q block.
- **v2**: occupancy-culled level set shredded into noise.
- **v3**: the Huygens crest construction replaced it.
- **v4–v6**: graded solid/dotted clip, dot field, fans. v6 already has today's composition.
- **v7**: K got its own traced packets.
- **v9–v11**: `_Guard` and wavelength tuning.
- **v12**: envelopes offset 0.8 mm from crests; reverted.
- **v13**: final.

The **resonance-clean** trials (`pp_resonance_clean_v1..v10`, 5 pens, no MoE, no backward band, V moved lower-right, Z centred at the bottom) show the hero filled into two near-solid grey discs (v5), then with a pinched hourglass comb between them (v10). They are flooded where v13 is open. No feedback from Juan.

## Keep — what works
- The hero is real physics, and the construction (crest loci, d as a whole number of wavelengths, crossing-safe guard) is the approved one, reused by every sibling. Keep it verbatim.
- The funnel: ten crimson and ten blue dotted fans converging from both upper corners onto the hero's rim. This is the plate's one strong gestural shape.
- The pen economy of the hero: open line net, no flood, ~3 % sustained crowding.
- The packet vocabulary (carrier × Gaussian with dashed envelope) is consistent everywhere, so Q, K, V, Z and Y read as one family.
- The MoE fork (u 0.48–0.76): two solid lanes and three ghost lanes is an honest pen rendering of "top-2".

## Weak — what doesn't
- [craft] **DOTTED LINES — Juan's note of 2026-09-28** ("should be more continuous dots"; see FEEDBACK.md). Measured on the family's `_dash_mm`: the pitch is already regular (2.22 mm ± 0.05, straight or curved), so spacing is not the fault. The fault is the mark and the gap: each 'dot' is a 0.42 mm micro-dash followed by 1.8 mm of paper, which reads as a broken dashed line, and where dotted leaders converge (Q/K fans into the field, the gradient rails) dots from neighbouring paths interleave into noise. Fix: one round dot of a single fixed size (a pen touch or a tiny closed circle, never a micro-dash), centre-to-centre pitch ≈ 0.9–1.1 mm so the line reads as continuous, pitch end-anchored so both ends carry a dot, the same pitch family-wide, and converging dotted paths spaced ≥ 2 pitches apart. Judge it on the preview at the real nib width. Plot time may grow — Juan accepts that; do not trade the dots for dashes or hairlines.
- [concept] It is a schematic. Labelled boxes-and-arrows flow (Q, K → fraction → softmax → Z → MoE → Y → ∂L/∂·, with arrowheads) is exactly the textbook/slide figure that § 6 fails at ≤ 3. Only the hero is an ORDER; the rest depicts the apparatus.
- [hierarchy] Everything is mid-size. The hero is ~20 % of sheet width, the Q/K blocks each ~27 %, Z ~35 %, MoE ~28 %. Nothing dominates at 3 m.
- [tension] Top half is mirror-symmetric about u 0.50 with a centred title: student-work symmetry. Only the lower half breaks it.
- [craft] Six pens, five swaps (house limit 3–4). The seeded black scatter dots over the rings muddy the crest net. The left `∂L/∂·` fraction stack is crammed: each numerator `∂L` nearly touches the previous denominator (u 0.09–0.12, v 0.82–0.95).
- [space] No generous quiet zone. The lower half (v 0.60–0.95) is a web of dotted cross-curves from softmax to V, Z and MoE, and the gaps are whatever was left.
- [depth] Flat and undeclared: one weight per pen, and no near/far in the figure.
- [craft] The midline "comb" of the reference is reduced to two small diamond clusters. The reference's dark core has no pen equivalent here, so the hero reads as two separate bullseyes rather than one interfering field.

## Next versions
1. **one-field** (abstract) — the plate IS the interference figure: blow the two-source crest field up to ~80 % of sheet width, cropped at both side edges. Q and K become only the two sources (their packets folded into the phase and wavelength of each source), softmax is read off as the intensity along one horizontal cut drawn as a single heavy line, and every box, arrow and gradient label is deleted. Hierarchy, the NO SCHEMATICS rule and the pen count (2–3) are all fixed in one move, and the approved construction is kept.
2. **moire-of-queries** (mechanism) — a whole row of query sources along the top edge and key sources along the bottom. Each Q·K pair interferes, and attention weight is where the crest families align into bright bands. The sheet becomes an INTERFERING order carrying real (e.g. GPT-2) attention numbers, with no labels beyond the title.
3. **benchmark-kept** (faithful) — keep v13 as the reproduction benchmark and only fix craft: cut to 4 pens (MoE into black, gradients as black dotted), remove the seeded scatter dots from the rings, and give the backward fraction stack 1.5× line pitch.

**If only iterating:**
1. Delete the 60 seeded scatter dots and the stipple caps from the hero, so the crest net is pure lines with only the |A|-sampled spoke dots.
2. Scale the hero up 1.5× (to ~u 0.25–0.75) and shrink the Q/K blocks to 70 %, so one element clearly dominates.
3. Re-space the left `∂L/∂·` stack to at least 9 mm per fraction (or cut it to three), so no numerator touches the fraction above.
