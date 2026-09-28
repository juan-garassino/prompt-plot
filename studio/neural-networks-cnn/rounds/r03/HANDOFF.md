render: ~/Downloads/pp_neural_networks_cnn_iterate_v5.png
gcode: ~/Downloads/pp_neural_networks_cnn_iterate_v5.gcode
paper: a4 portrait, cream (preview renders white: no paper-colour flag in render_candidate.py)
pens: 0 black = the five maps as horizontal hidden-line profile rows only, title, 3-line caption · 1 crimson = effective receptive field of CAM unit (4,3): one closed 50 %-gradient-mass ellipse per lower map (4 loops) + 9 closed isolines of unit (4,3)'s own hill inside its cell
data: same arrays as r02 (studio/neural-networks-cnn/rounds/r03/maps.npz = r02's): MobileNetV2 ImageNet on skimage "chelsea"; maps bottom→top = input luminance 224², ‖block_2‖ 56², ‖block_5‖ 28², ‖block_12‖ 14², ReLU(CAM − mean) 7², tiger_cat p = 0.43, argmax (4,3)
rows: 38 / 28 / 28 / 14 / 7 at flat pitch 1.02 / 1.25 / 1.15 / 2.08 / 3.73 mm (strides 6 / 2 / 1 / 1 / 1)
top-layer interpolation: each CAM unit a cos² hill of radius one cell at its exact value, p=6-norm envelope (lower maps bicubic, input pixel rows 2-px means)
geometry: one basis for all planes; widths 146 / 134.5 / 123 / 111.5 / 100 mm; ink bbox x 15–195, y 15–281; measured inter-layer ink gaps 10.9 / 10.9 / 10.8 / 10.9 mm
lineage: Georg Nees, *Schotter* (c. 1968)
compare-to: ~/Downloads/pp_neural_networks_cnn_one-valley_v12.png (r02) | reference: none
