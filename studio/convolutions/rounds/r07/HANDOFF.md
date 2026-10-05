render: gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png
gcode: gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.gcode
paper: a4 landscape, cream
pens: 0 crimson = y > 0 (X bends up): response rings, positive kernel-tap collars, key icons rows 5 and 3 · 1 dodgerblue = y < 0 (X bends down): response rings, negative collars, key icons rows 7 and 2 · 2 black = X (dots behind the front, stripes ahead of it, the x = 0 keyline), the staircase, the card keyline + shadow hatch, then the text layer (key text, title)
nib: 0.30 mm fineliner on every pen. Keyline 2 passes (pass 2 offset 0.30 mm outward). Doubled outer ring +0.25 mm (fused 0.55 mm). Collar passes 0.32 mm pitch. Card keyline 4 passes at 0.25 mm (fused 1.05 mm). Title 0.5 mm weight in 3 passes per segment
layer order: crimson → dodgerblue → black (palette index = stream order)
encoding: studio/convolutions/encoding.md v1 (codifies r05; this round follows §4/§5/§9/§11)
rule: X = cell-mean distance (6×6 quadrature) to the x = 0 outline of a 3-capsule Y whose unread arm leaves the image at the top-right; input lattice 37×25 at 7.2 mm, top and right edges on the crop; Y = K∗X valid, stride 2 (17×11); read windows i + j ≤ 10 (66); rings centred on the node's own input sample, count = rint(4|y|/max|y|), max over read nodes = 18.731, no ring = |y| < max|y|/8, outer ring doubled for |bin| ≥ 3; K = 5×5 LoG σ = 1 cell, zero-sum, collar ink = 19.285 mm²·|w|; dot inked Ø = 2.56·√(x/37.26), centreline Ø = inked − 0.30, no dot for x < 1.5 mm; stripes = level sets d = k·2.1 mm; the keyline is ONE open polyline per pass, ends only on the crop
declared omissions: (a) the last riser stops at y 24.2 (row 0 is x = 0 across its width); (b) the card hides outputs (4,5) 0, (5,5) −3, (4,6) −2; (c) X is cell-averaged, not point-sampled
lineage: Roy Lichtenstein, Modern Painting series (1966–70): Ben-Day dot lattice, parallel stripes and one heavy black keyline as the whole vocabulary
canon: Pop / Ben-Day (STYLES §4): dot area = value, outlines dominate; flat except one lifted plane (the kernel card)
compare-to: gallery/studio/convolutions/trials/pp_convolutions_iterate_v20.png (parent r05) | gallery/studio/convolutions/current/pp_convolutions_v1.png (r01 benchmark) | reference: studio/convolutions/ref/reference.png
