render: gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.png
physical-width preview (10 px/mm, 0.3 / 0.5 / 0.3 / 0.5 mm nibs on cream): gallery/studio/millennium_poincare/current/pp_millennium_poincare_iterate_v3_phys10.png
gcode: gallery/studio/millennium_poincare/trials/pp_millennium_poincare_iterate_v3.gcode
paper: a3 portrait, cream, margin 15
pens:
- 0 black 0.3 = the space at each instant: the t = 0 start line, 4 visible past lines, 33 A and 6 B rings
- 1 black 0.5 = the surgery instant t_s, drawn once, with a ≥ 3 mm bare moat on both sides; it pauses at the waist where the red caps take its place
- 2 black 0.3 (same pen as layer 0) = type
- 3 red 0.5 = the events: the cut (two caps at radius h), the two extinction points, SOLVED
layer order: 0 → 1 → 2 → 3 (lines → keyline → type → red)
plate-job minutes (plot plate --layers 0,1,2,3 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run): ~23 / ~2 / ~53 / ~2 min, ETA ~85 min including swaps
lineage: Vera Molnár, (Dés)Ordres (1974), nested closed figures whose deviation from the ideal form is measured ring by ring
thesis: abstract (flat by declaration: the meridian section; depth is spent on time through occlusion)
mapping:
- each closed line = the whole space at one instant, in meridian section
- one line = Δt 0.01 of Ricci time, anchored at t_s = 0.054647
- outside the heavy line = before the cut, inside = after
- scale 62 mm per unit; axis at 62°; cut at (165, 200), not drawn
merge rule: lines pause within 0.85 mm of higher-ranked ink and within 3.05 mm of the keyline; a paused ring does not re-enter as a stretch < 15 mm; a < 30 mm stretch twinning kept ink merges into it (t_s − 0.05 merges into t = 0)
data: studio/millennium-poincare/rounds/r03/snapshots.npz (identical to r02's)
compare-to: gallery/studio/millennium_poincare/current/pp_millennium_poincare_abstract_v4_phys.png (r02) | reference: studio/millennium-poincare/ref/reference.png
