render: gallery/studio/gan/trials/pp_gan_iterate_v24.png
gcode: gallery/studio/gan/trials/pp_gan_iterate_v24.gcode
paper: a4 portrait, cream (preview on white)
pens: 0 dodgerblue = warp = D, the discriminator (moves ψ), plotted 1st · 1 crimson = weft = G, the generator (moves θ), plotted 2nd · 2 black = the fixed truths (`+`, h→0 circle, hole labels) + all type, plotted last
encoding: studio/gan/encoding.md rev 1 (Red Meander proper)
rule: one reed, 2.8 mm, half a pitch off the equilibrium (78, 113) · RIBBON = the iterates' chord polygon × [0.9, 1.1] about the equilibrium · in the ribbon, warp over iff ψθ > 0, weft over iff ψθ < 0 · everywhere else a 2/2 basket (warp over iff ⌊i/2⌋+⌊j/2⌋ even) · a ribbon float ends by going under at the next ground crossing (tie-down) · under = 2.4 mm gap in the thread · ≥ 3 ribbon over-crossings in one piece = double pass · no crossing woven at ρ < 39.98 mm (hole) · cloth window x 10–200, y 37.3–251.5 = its cut edge
lineage: Anni Albers, Red Meander (1954)
canon: Bauhaus weaving workshop, declared flat
run: Dirac-GAN simultaneous GDA, h 0.26, r0 0.74 (38.48 mm at 52 mm/unit), seed 7 → a0 0.42622, exit step 70 r 1.3287
plot: 14,686 cmds · draw 23.10 m · travel 11.98 m · 2,110 pen-downs · blue 48 / crimson 45 / black 32 min ≈ 2 h 05
compare-to: gallery/studio/gan/trials/pp_gan_iterate_v16.png (parent r04) | gallery/studio/gan/current/pp_gan_two-players-interlaced_v10.png (r03) | reference: none
