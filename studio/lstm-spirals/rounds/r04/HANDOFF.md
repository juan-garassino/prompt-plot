render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png
gcode: gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.gcode
paper: a4 portrait, cream or white
pens (layer order = index order, light → dark): 0 crimson 0.5 = the cell state c_t: ONE continuous line, half a turn round the red eye per character, pitch = 1.8 mm × carry_t (the forget gate's carried fraction), floor 0.9 mm; the last 12 characters (" BEST MEMORY") wrap the whole field · 1 black 0.5 = the hidden state h_t: one comet per character, born at its letter, sweeping RMS(h_t) of one turn toward the black eye (tanh < 1, so none closes); older comets are cut where a newer one comes within 1 mm · 2 black 0.3 = type: the proverb (the input sequence) round the black lobe, the spine title, the colophon
data: a real trained 8-cell char LSTM (train_lstm.py → lstm_weights.json) run forward at render time over "THE PALEST INK IS BETTER THAN THE BEST MEMORY"
lineage: Land Art — Robert Smithson, Spiral Jetty (1970) / A Sedimentation of the Mind (1968): one continuous coil whose walk is time, laid as sediment
declared: flat (a planar potential; depth is nesting only)
compare-to: gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png | reference: studio/lstm-spirals/ref/reference.png
