render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.png
physical-width preview (0.1 / 0.3 / 0.5 mm nibs on cream): gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3_phys.png
gcode: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.gcode (G1 all F600; pen dwells G4 P1 = 1.0 s, 2,973 of them)
paper: a3 portrait, cream, margin 15
pens: 0 black 0.1 fineliner = one line per depth-8 sub-tree (runs to its deepest node) + rim (ring 20) + 12 hour ticks (previewed dimgray) · 1 black 0.3 = the backtracking search node for node, depths 0–8 · 2 black 0.3 (same pen, own layer, no swap) = type · 3 red 0.5 = the one certificate: its search path, the needle pulled out past the rim, 91 clause-check ticks
layer order: 0 → 1 → 2 → 3 (2 physical swaps); strokes 155 / 226 / 1,013 / 92; ≈ 24.1 / 20.0 / 61.3 / 5.8 min = ≈ 111 min (read from this gcode: draw+travel at 10 mm/s + real G4 seconds + 0.5 s servo per lift/drop)
geometry: pens 0, 1, 3 identical to r02 (stroke multisets, 3-decimal coords) — checker: studio/millennium-p-vs-np/rounds/r03/audit.py <r03.gcode> <r02.gcode>
lineage: Manfred Mohr, Cubic Limit (1973–75) and the hypercube works from 1977
mapping: angle = share of 2^20 = DFS order (0° at 12, clockwise) · radius = depth, 6.4 mm per variable · hub (148.5, 148.5), R = 128 · drawn: preorder 1..7,812
data: SATLIB uf20-03.cnf via studio/millennium-p-vs-np/data/search.py (run live at import)
compare-to: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3_phys.png (r02) | reference: studio/millennium-p-vs-np/ref/reference.png
