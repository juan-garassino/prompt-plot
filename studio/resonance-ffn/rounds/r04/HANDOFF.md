render: gallery/studio/resonance_ffn/current/pp_resonance_ffn_iterate_v5.png
gcode: gallery/studio/resonance_ffn/current/pp_resonance_ffn_iterate_v5.gcode
seed: 7 (r01's seed — scatter positions are r01's)
paper: a4 portrait, cream · drawn on a 10 mm margin (ink x 15.4–196.5, y 15.6–280.4) — stream with --margin 10
pens (family indices kept): 0 crimson = Q, ∂L/∂Q · 1 dodgerblue = K, ∂L/∂K · 2 goldenrod = V, ∂L/∂V · 3 forestgreen = Z, ∂L/∂Z · 4 darkviolet = FFN stages, fans, Y, ∂L/∂Y · 5 black = interference figures, softmax, title, type, FFN bracket
stream order: --layers 2,1,3,0,4,5 (light → dark); each pen one layer, entered once
plate job: promptplot plot plate <gcode> --layers 2,1,3,0,4,5 --paper a4:portrait --margin 10 --batch-strokes 400 --rezero-every 800
dry-run: bounds ok · 6 layers 720/1058/201/1082/268/1422 strokes · waits: 6 swaps → done
plot (clamped plot-plate model: F500 draw, F2000 travel, dwell ≥ 1 s, 90 s/swap, 20 s/re-zero; the file itself carries F1200–2600 and G4 P0.2): 4,751 pen cycles · draw 14.26 m · travel 9.49 m (67 %) · ≈ 201 min
in-layer hops > 80 mm: crimson 141, blue 173 (two ink regions per pen), black 93 (backward row → softmax) and 90 (hero → title)
dots: dotted lines = one round loop r 0.15 mm at 1.0 mm pitch, end-anchored, phase-locked where same-pen lines run within 2 mm · textures (stipple caps, scatter) = r01's marks, one round dot each
nib: 0.3–0.4 mm fineliner
lineage: Charles Csuri & James Shaffer, Sine Curve Man (1967) — a form and its function-mapped copy on one plotter sheet
depth: flat — reproduction of a flat plate diagram
thesis: iterate — r01/v9 composition unchanged; mark-making and streaming only
compare-to: gallery/studio/res_ffn/current/pp_res_ffn_v9.png | reference: studio/resonance-ffn/ref/reference.png
