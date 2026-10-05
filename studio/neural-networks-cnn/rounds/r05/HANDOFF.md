render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.png
gcode: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.gcode
paper: a4 portrait, cream (preview renders white: no paper-colour flag in render_candidate.py)
canon: RADIAL DATA-VIZ / INFORMATION ARCS (STYLES §5) — declared flat
lineage: Florence Nightingale, polar-area "rose" (Diagram of the Causes of Mortality, 1858), via the Bauhaus 1919–1933 radial timeline — one wedge per period, the datum as length inside it
order: radial dial — angle = conv layers applied (clockwise from 12 o'clock = input, 0 → 52 at 6 o'clock = Conv_1), one wedge per tapped depth (20), wedge width ∝ layers; radius = Chebyshev distance from the centre of CAM unit (4,3) in INPUT px, 0 → 160 px (farthest pixel is 159 px away)
pens (plot order): 0 cadetblue = ERF petals: one concentric arc per ring of that layer's grid (ring pitch = stride, input binned at 2 px), arc length = ring's share of Σ_c|∂cam(4,3)/∂A|, longest ring of each wedge = full wedge · 1 darkgoldenrod = half-mass radius per depth (continuous, interpolated), one line stepping through the gutters · 2 indianred = exact theoretical RF edge per depth (+ half a ring), one line; edges beyond 160 px drawn ON the rim · 3 black = px scale on the diameter, layer ticks, block ids, resolution brackets, dotted 64/128 px rings, title, notes, legend, caption
data: studio/neural-networks-cnn/rounds/r05/reach.npz from compute_reach.py — same MobileNetV2/ImageNet pass on skimage "chelsea" (centre-crop 300² → bicubic 224²) as r02–r04, gradients tapped at all 20 depths; g_input/g_block_2/g_block_5/g_block_12/cam bit-identical to r03/maps.npz; tiger_cat p = 0.429, argmax (4,3), unit RF centre (row 159, col 127); gradient exactly 0 outside the theoretical RF at every depth
key numbers on the sheet: input edge 245 px, half-mass 56 px (113² px square = 25.4 % of image); block 12 edge 112 px, half-mass 43 px; block 16 edge 0, half-mass 0
geometry: hub (23, 148.5) mm, R0 12 mm, R1 117 mm, 0.656 mm/px; ink bbox x 15.0–193.6, y 16.2–281.5
plot: 4 layers, one swap each; draw 5.52 m, travel 5.96 m, 16,432 commands, 1,595 lifts; ≈ 18 / 1 / 1 / 46 min per layer at Leo settings
compare-to: gallery/neural-networks/cnn/trials/pp_neural_networks_cnn_iterate_v5.png (r03) | reference: none
