# CNN — FROM PIXELS TO MEANING — description

<!-- rewritten 2026-09-29 by the studio lead at the vote after r04/r05. It describes the CURRENT best (r04), not the history; the old promoted plate (bauhaus_locality, pp_cnn_dashes) is summarised under "How it got here". This is the spec the next iteration starts from: edit freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/cnn` |
| current render | `gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png` (gcode beside it). Studio round r04 |
| source | `studio/neural-networks-cnn/rounds/r04/piece.py::cnn_one_summit` (data: `rounds/r04/maps.npz`, from `compute_maps.py`) |
| paper · pens | a4 portrait, cream. Pen 0 black: five maps as horizontal hidden-line profile rows, single-pass title, 3-line caption. Pen 1 crimson: 4 ERF loops + 5 summit level-set arcs |
| status | goes to Juan's vote. Critics: art 6.43/6 FAIL · science 9/8/8 PASS. Alternative flavour `reach-dial` (r05) and the older `pooling-cascade` (r01) are on disk |

## In one line
One real MobileNetV2 forward pass on a photo of a cat, drawn as five hidden-line relief planes climbing the sheet (input luminance 224² → ‖block_2‖ 56² → ‖block_5‖ 28² → ‖block_12‖ 14² → CAM 7²). Each plane is one element (a profile row) under one parameter (resolution), after Nees's *Schotter* inverted: disorder → order. Crimson marks the measured receptive field of the one winning CAM unit on every plane and its summit at the top.

## What is on the sheet
Coordinates are sheet mm, x right, y up (a4 portrait, drawable 10–200 × 10–287).

1. **The stack**: five planes on ONE oblique basis, paper = (X + 0.5 D, 0.66 D + Z), D = 0.45 W. Widths are 146 / 134.5 / 123 / 111.5 / 100 mm, right-flush at x = 195, and each plane shears down-left, which makes a staircase diagonal. There are four equal gaps of 13.08 mm. Rows only: no mesh, ticks, rails or frustum.
   - **224² input luminance** (y ≈ 32–75): 38 rows at 1.16 mm pitch, 3 mm relief, the densest and scratchiest plane.
   - **56²** (y ≈ 88–128): 28 rows at 1.43 mm.
   - **28²** (y ≈ 143–184): 19 rows at 1.96 mm (stride 1.5, half the rows interpolated). Its back-left corner carries a real spike, the map's maximum.
   - **14²** (y ≈ 197–230): 14 rows at 2.37 mm, 9.6 mm relief.
   - **7² CAM − mean, signed** (y ≈ 243–281): 7 Catmull-Rom rows at 4.24 mm, 1.0524 mm/unit (10.5 mm above mean, 20 mm peak-to-peak). All 13 cells ≥ 20 % of the peak show a crest.
   - Rows, pitch, relief and breaks per row are all strictly monotone bottom → top.
2. **Crimson** (scarce, one pen):
   - **4 ERF loops**, the 50 %-gradient-mass moment ellipses of ∂CAM(4,3), lying on their own surfaces. They are ≈ 90 / 80 / 72 / 60 mm wide and step right toward the summit. The 28² loop has one real occlusion break.
   - **The summit**: 5 front arcs of the CAM level sets 6.91–9.41 around unit (4,3), at x 130–148, y 264–271, visible-only.
3. **Title**: `FROM / PIXELS / TO / MEANING`, single-pass, 5.4 mm cap, top-left (x 17.75–83, y 241–281) over the quiet wedge the staircase leaves.
4. **Caption**: 3 flush-left lines under the input plane at x = 17.75, the same axis as the title and the input's front-left corner. It gives bottom → top resolutions, what height means per plane, the crimson = 50 % gradient mass (~26 % of image vs one cell = 2 %), the ring levels, and MobileNetV2 / chelsea, centre-crop 300² → 224², p(tiger cat) = 0.43, front edge = image bottom.

## The science it encodes
- A single forward pass (MobileNetV2/ImageNet, skimage `chelsea`). Argmax CAM unit (4,3). ERF = Σ_c|∂CAM(4,3)/∂A| per map, summarised as the 50 %-mass ellipse.
- **Verified by the science critic (r04):**
  - front rows correlate ≥ 0.994 with their maps;
  - the ERF loops sit within 0.33 mm of recompute;
  - the rings are the Catmull-Rom level sets to 0.17 mm;
  - the hidden line draws nothing hidden;
  - 13/13 strong CAM cells are visible.
- **Honest limits:**
  - The per-plane height exaggeration (0.065 / 0.210 / 0.206 mm per activation unit) is a design progression and is not yet printed on the sheet (S9).
  - "RINGS = CAM LEVELS ABOVE 6.9" should name CAM − mean and the runner-up (S10).

## How it got here
- **r00** (`bauhaus_locality`, `pp_cnn_dashes`): seeded fbm terrains, a linear crimson frustum, an axis and labels, i.e. the Zeiler–Fergus slide.
- **r01** `pooling-cascade`: lattice cards, exact RF footprints. Kept as a flavour.
- **r02** `one-valley`: the first real data and a tall 45 mm summit, but four grammars and rails.
- **r03**: rows only, 9.8 k commands, equal gaps. Its summit was a tall crimson coil that hid 10 of 22 CAM cells.
- **r04** (current): head rebuilt with a measured height (13/13), a strictly monotone channel, single-pass title, one type axis.
- **r05** wildcard `reach-dial`: a Nightingale half rose of reach per depth. Kept as a flavour; its fidelity mandates are parked.

## Keep — what works
- **The monotone Schotter channel**: noise → calm reads bottom to top without labels, and every channel is strictly monotone.
- **One grammar and one basis**: rows only, right-flush staircase, equal gaps, no apparatus between planes.
- **Real data end to end**: the truth record above, and science's PASS.
- **The ERF loops on their surfaces**, with an honest occlusion break.
- **The shared type axis** x = 17.75 and 5 mm frame clearance all round.
- **Plot economy**: 11.5 k commands, travel 0.28 × draw, 2 clean layers (≈ 55 min black + 2 min crimson under `plot job`'s Leo guard).

## Weak — what doesn't
- [hierarchy] **The summit is the quietest mark**: an 18 × 7 mm crimson cap on 7 loose wires. This conflicts with 13/13 visibility at this pitch (see the r05 SYNTH).
- [accent] The crimson loops are hairlines that hug black rows for 24–28 mm (14² and 28² back arcs), so they are scarce but not loud.
- [craft] Rows on the 224² plane come to ≈ 0.5 mm apart (y 25–75). There is a torn-corner wiggle on 28² (x 48–52, y 143–146).
- [type] "MEANING" ends 7 mm before the top plane's front row on the same baseline. The single-pass title is the lightest mass on the sheet. The caption sits 7 mm under the input plane, against the 13 mm rhythm.
- [concept] The stacked silhouette still recalls the layered-figure slide, and the widening receptive field is carried by the caption, not by geometry.

## Next versions
- **If only iterating (r06, parent r04):** buy the summit's height with PITCH, not scale. Make the 7² plane the widest and deepest on the sheet (inverting the pyramid toward meaning, cropped at the top-right frame if needed), re-run the 13/13 sweep, then close A16 / S9 + S10 / A17 / A18 (see `rounds/r05/SYNTH.md`).
- **reach-dial** (r05): the rose, if Juan prefers the question "how far does one unit reach?". Start from RD1–RD5 in the ledger.
- **blur-as-tone**: one terrain whose sheet rows re-sample coarser upward. This is an unexplored lens from the original description.
