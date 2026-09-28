render: ~/Downloads/pp_convolutions_iterate_v9.png
gcode: ~/Downloads/pp_convolutions_iterate_v9.gcode
paper: a4 landscape, cream
pens: 0 black = X (distance-field rings ahead of the wavefront, sample dots behind it, dot area = x), staircase wavefront + head keylines, key, title · 1 crimson = y > 0 response rings + positive kernel taps (collar area = |w|) · 2 dodgerblue = y < 0 response rings + negative kernel taps
rule: Y = K∗X valid, stride 2 (11×11); swept nodes i + j ≤ 10; rings centred on the node's own input sample, count = rint(4|y|/max|y|), no ring = 0; head = node (5,6), 5×5 LoG, 1.5 mm drop shadow; x = 0 samples are paper
lineage: Victor Vasarely, Vega series (1957–) — a lattice swollen by a hidden volume: the dots are the thumbprint's distance volume, the rings are where it bends
canon: Op Art / Ben-Day, declared flat except one plane (the kernel head, drop shadow, occludes rings and 3 finished outputs)
compare-to: ~/Downloads/pp_convolutions_sliding-window_v10.png (parent r03) | gallery/studio/convolutions/current/pp_convolutions_v1.png (r01 benchmark) | reference: studio/convolutions/ref/reference.png
