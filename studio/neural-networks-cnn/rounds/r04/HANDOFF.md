render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png
gcode: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.gcode
paper: a4 portrait, cream (preview renders white: no paper-colour flag in render_candidate.py)
pens: 0 black = the five maps as horizontal hidden-line profile rows only, single-pass title, 3-line caption · 1 crimson = effective receptive field of CAM unit (4,3): one 50 %-gradient-mass ellipse per lower map (4 loops; the 28² loop has 1 occlusion break, so 2 runs) + 5 level-set arcs of the drawn CAM around (4,3) at 6.91 / 7.57 / 8.23 / 8.85 / 9.41, visible front arcs only (NOT closed on paper)
plot order: layer 1 pen 0 black (maps, then title, then caption; 815 runs, ≈ 50 min at F600 with 1 s dwells) · layer 2 pen 1 crimson (10 runs, ≈ 2 min)
data: same arrays as r02/r03 (rounds/r04/maps.npz): MobileNetV2 ImageNet on skimage "chelsea", centre-crop 300² → 224²; bottom → top = input luminance 224², ‖block_2‖ 56², ‖block_5‖ 28², ‖block_12‖ 14², CAM − mean 7² (SIGNED, not clipped); tiger_cat p = 0.43; argmax (4,3)
top plane: bicubic Catmull-Rom (passes through unit values); height 1.0524 mm per CAM unit (peak 10.5 mm above mean, 20.0 mm peak-to-peak); crests shown on sheet 13 / 13
rows: 38 / 28 / 19 / 14 / 7 · flat pitch 1.16 / 1.43 / 1.96 / 2.37 / 4.24 mm · relief 3.0 / 3.2 / 7.0 / 9.6 / 20.0 mm · breaks per row 3.45 / 2.89 / 2.16 / 0.86 / 0.57
geometry: one basis for all planes, paper = (X + 0.5 D, 0.66 D + Z), D = 0.45 W (KY 0.58 → 0.66 vs r03); widths 146 / 134.5 / 123 / 111.5 / 100 mm, right-flush x = 195; equal gap 13.08 mm; ink bbox x 17.75–195.0, y 15.05–281.0; type axis x = 17.75 = input plane front-left corner
budget: 11,537 commands · draw 13.86 m · travel 3.83 m · 825 lifts · 2 pens
lineage: Georg Nees, *Schotter* (c. 1968)
compare-to: gallery/neural-networks/cnn/trials/pp_neural_networks_cnn_iterate_v5.png (r03) | gallery/neural-networks/cnn/current/pp_neural_networks_cnn_one-valley_v12.png (r02 summit) | reference: none
