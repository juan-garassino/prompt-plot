render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.png
gcode: gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.gcode
paper: a4 portrait, white preview (cream paper fine)
pens (= layer order, light → dark): 0 dodgerblue = write: annuli where i_t > f_t, plus input lines draining into the cell · 1 crimson = keep: annuli where f_t > i_t, plus the c_t label · 2 black = hidden state h_t, input lines draining into it, axis, all type
lineage: Marcel Duchamp, Rotoreliefs (1935) / Anemic Cinema (1926) — a disc of rings that reads as a spiral once it turns; here one turn = one time step
compare-to: gallery/studio/lstm_spirals/current/pp_lstm_spirals_v10.png (r01) | reference: studio/lstm-spirals/ref/reference.png
checks: .venv/bin/python studio/lstm-spirals/rounds/r03/check_plate.py gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.gcode 7
