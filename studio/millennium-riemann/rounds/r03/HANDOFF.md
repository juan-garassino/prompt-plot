render: gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.png
physical-width preview (0.1 / 0.3 / 0.3 / 0.5 mm round nibs on cream — judge weight here): gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2_phys.png
gcode: gallery/studio/millennium_riemann/current/pp_millennium_riemann_iterate_v2.gcode
paper: a3 portrait, cream, margin 15
pens: 0 black 0.1 fineliner = Im ζ(s) = 0, real axis included (dimgray in the render png) · 1 black 0.3 = Re ζ(s) = 0 · 2 black 0.3 (same pen, own layer, no swap) = type · 3 red 0.5 = the 28 nontrivial zeros ρ_n (both branches through ρ_n, r = 1.6 mm, ONE one-way pass per arm, 56 strokes)
layer order: 0 → 1 → 2 → 3 (2 physical swaps) · plate-job minutes (`plot plate --layers 0,1,2,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run`): ≈ 31 / 26 / 28 / 3 min, ETA ≈ 94 min at feed ≤ 500, dwell ≥ 1 s
lineage: Sol LeWitt, Wall Drawing #46 (1970)
scale: 3.45 mm per unit on both axes; σ = ½ at x = 180 (not drawn); real axis y = 32; t ∈ [0, 97.35]
data: studio/millennium-riemann/rounds/r02/xray_abstract.json (unchanged, read in place) · studio/millennium-riemann/data/zeros.json (γ_n)
detail crop for A1: `.venv/bin/python studio/millennium-riemann/rounds/r03/render_truewidth.py <gcode> out.png 170 330 190 368 20`
audit: `.venv/bin/python studio/millennium-riemann/rounds/r03/audit_r03.py`
compare-to: gallery/studio/millennium_riemann/current/pp_millennium_riemann_abstract_v6_phys.png (r02) | reference: studio/millennium-riemann/ref/reference.png
