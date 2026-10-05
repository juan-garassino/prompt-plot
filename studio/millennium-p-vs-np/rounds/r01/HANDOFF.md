render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.png
render-truewidth: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6_truewidth.png (pens at 0.1/0.3/0.3/0.5 mm; in the standard preview the stats box and legend sit over the title)
gcode: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.gcode
paper: a3 portrait, cream, margin 15
pens: 0 black 0.1 (preview dimgray) = the search below row 7, one line per depth-7 sub-tree, as deep as its deepest node · 1 black 0.3 = the search rows 0–7 node for node + the Petersen NO tree · 2 black 0.3 (same pen, own layer) = type · 3 red 0.5 = the one certificate: its search path root→row 20, and its 91 clause checks
layer order: 0 → 1 → 2 → 3, 2 swaps; ≈ 24 / 18 / 52 / 6 min ≈ 100 min at F600
lineage: Manfred Mohr, Cubic Limit (1973–75) and the hypercube works from 1977 — a hypercube read by a rule; here the 20-cube halved at every row, drawn only where not refuted
scale: x = 15 + 267·m (m = node's exact share of 2^20); row d at y = 350 − 12.5·d; red ends x = 273.57, y = 100
data: SATLIB uf20-03 (studio/millennium-p-vs-np/data/uf20-03.cnf); tree dump rounds/r01/tree.json; Petersen computed in piece.py
compare-to: none (new plate) | reference: studio/millennium-p-vs-np/ref/reference.png
