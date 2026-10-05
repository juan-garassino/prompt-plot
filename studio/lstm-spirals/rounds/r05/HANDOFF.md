render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13.png
render (nib widths, cream): gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13_physical.png
gcode: gallery/studio/lstm_spirals/current/pp_lstm_spirals_iterate_v13.gcode
paper: a4 portrait, cream or white
pens (layer order = index order, light → dark):
  0 grey 0.3 = the output gate o_t: one thread per letter from that letter's half-turn on the red coil to its comet birth (h_t = o_t·tanh c_t); dashed, inked fraction = mean o_t over the 8 cells
  1 crimson 0.5 = the cell state c_t: ONE line, 45 half-turns about the red eye (one per letter, odd letters the top half); ring gap = 0.8 mm + 0.8 mm × mean f_t, isotropic and unclamped
  2 black 0.5 = the hidden state h_t: one comet per letter, sweeping RMS(h_t) of a turn; newer cuts older where within 1 mm; each comet's root (before its one 1 mm break) = 8 mm × RMS(h_t), never cut
  3 black 0.3 = type: the proverb (the input) on the black rim, spine title, colophon
data: real trained 8-cell char LSTM (lstm_weights.json, loss 0.0754, acc 1.0) run forward over "THE PALEST INK IS BETTER THAN THE BEST MEMORY"; trace: studio/lstm-spirals/rounds/r05/trace.json; readback: studio/lstm-spirals/rounds/r05/check_plate.py <gcode>
lineage: Robert Smithson, Spiral Jetty (1970) / A Sedimentation of the Mind (1968) — the coil; Naum Gabo, Linear Construction in Space No. 2 (1949) — the strung threads
canon: Swiss
declared: flat

pen job (emitted gcode, F600 draw / 2000 travel / 1 s per lift):
| layer | strokes | draw mm | travel mm | max hop mm | min |
|---|---|---|---|---|---|
| 0 grey | 1145 | 7038 | 2722 | 44.2 | 32.2 |
| 1 crimson | 5 (chain order, 0.000 mm between) | 2934 | 0 | 0 | 5.1 |
| 2 black comets | 88 | 2902 | 379 | 19.3 | 6.5 |
| 3 type | 628 | 2087 | 1851 | 111.7 | 14.9 |
| total | 1866 | 14962 | 4952 | | 58.7 + 3 swaps |
colophon: flush-left at x = 141.65 (rightmost figure ink), first baseline on the saddle horizontal y = 132.0

compare-to: gallery/studio/lstm_spirals/current/pp_lstm_spirals_memory-strata_v18.png (r04) | gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png (r01) | reference: studio/lstm-spirals/ref/reference.png
