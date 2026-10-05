render: gallery/studio/gan/current/pp_gan_iterate_v34.png
gcode: gallery/studio/gan/current/pp_gan_iterate_v34.gcode
paper: a4 portrait, cream (preview on white)
pens: 0 dodgerblue = warp = D, the discriminator (moves ψ), plotted 1st · 1 crimson = weft = G, the generator (moves θ), plotted 2nd · 2 black = the fixed truths (`+`, h→0 circle, hole labels incl. STEP 0) + all type, plotted last
encoding: studio/gan/encoding.md rev 1 + § Revision 1.1 (appended this round)
rule: one reed 2.8 mm, half a pitch off the equilibrium (66, 100) · RIBBON = chord polygon of the iterates, on every ray [max(0.9ρ, r0 + 1.0 mm), that + 0.2ρ] (shifted at the rim, never clipped) · ribbon cell k is warp-on-top iff ψ_kθ_k > 0 (the owning step), weft-on-top otherwise · double pass exactly over ribbon crossings · ground = 2/2 basket, warp over iff ⌊(i+1)/2⌋+⌊(j+1)/2⌋ even · tie-down only where a float would bridge a channel · under = 2.4 mm gap · no crossing woven at ρ < 38.81 mm · cloth window x 10.0–197.6, y 38.4–254.0 = its cut edge, edges at mid-pitch
lineage: Anni Albers, Red Meander (1954)
canon: Bauhaus weaving workshop, declared flat
run: Dirac-GAN simultaneous GDA, h 0.26, r0 0.74 (37.81 mm at 51.1 mm/unit), seed 7 → a0 0.42622, z_0 (100.43, 115.63), exit step 68 r 1.2936 at the left edge
plot: 14,406 cmds · 2,024 pen-downs · draw 22.0 m · travel 11.2 m · blue 48 / crimson 43 / black 29 min ≈ 2 h 00
compare-to: gallery/studio/gan/trials/pp_gan_iterate_v24.png (parent r05) | reference: none
