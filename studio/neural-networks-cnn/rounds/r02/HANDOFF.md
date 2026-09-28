render: ~/Downloads/pp_neural_networks_cnn_one-valley_v12.png
gcode: ~/Downloads/pp_neural_networks_cnn_one-valley_v12.gcode
paper: a4 portrait, cream
pens: 0 black = terrains, type · 1 crimson = receptive field of the one argmax unit: ERF ellipse rings (50 % gradient mass) on the four lower layers, dashed rails, the isolines inside the unit's cell on the top peak
data: MobileNetV2 (Keras ImageNet weights) on skimage "chelsea" (224²); layers bottom→top = input luminance, ‖block_2‖ 56², ‖block_5‖ 28², ‖block_12‖ 14², ReLU(CAM − mean) 7² for top-1 tiger_cat p=0.43; argmax unit (4,3); arrays in studio/neural-networks-cnn/rounds/r02/maps.npz
lineage: Georg Nees, *Schotter* (c. 1968) — order→disorder down the sheet: one peak at the head, raster noise at the foot
compare-to: gallery/neural-networks/cnn/promoted/pp_cnn_dashes.png | reference: none
