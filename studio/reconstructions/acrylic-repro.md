# ATTENTION AS RESONANCE — ACRYLIC IN TEN PAINTS
**Essence:** the transformer block as a Van Gogh night — Q and K as two spiral suns, their arcs meeting in a softmax funnel of light that pours into the Z = AV river, the FFN as a tree, a whirlpool and a fork, the residual as the road home — painted as brush centerlines in three stages. **Status:** to reconstruct; oracle = `gallery/references/oracles/attention_acrylic_source/` (11,163 centerlines; 10 paints; brushes 4.0 / 1.8 / 0.9 mm; A3 portrait). The oracle's generator was never saved — this reproduces its documented METHOD and is judged against its output.

## The idea (the true thing)
Same block. Colour is the time-of-night and the heat of attention; broad masses first, then flow, then sparks.

## Pen-plotter visual (our engine)
- `occlusion: paint`, `stages: [underpainting, body, accents]`, widths `[0.9, 1.8, 4.0]`, ten quantised paints (`quantize_palette` on the reference, or the oracle's `paint_plan.json` names/hexes).
- Author a few major **flow guides** (the two spirals, the funnel, the river, the road); `brush_family` around each for the underpainting (4.0) and body (1.8); `flow_strokes` on the image's orientation field for accents (0.9); colour sampled at the stroke then snapped to the palette.
- Every mark is ONE centerline with a brush width — never two edges around a paint blob. Later passes cover earlier; the compiler culls the hidden.
- Brush hardware: one well per paint (`BrushConfig.charge_positions`), reload count restarts at each swap.

## Reference prompt
Reconstruct `ref/reference.png`. Judge against `gallery/references/oracles/attention_acrylic_art_preview.png` and the oracle's numbers (~11k strokes, ~110 m painted, stage order kept). Preview at real footprint.

## Build notes
Stage proportions in the oracle: ~1,660 underpainting / ~2,880 body / ~6,500 accents. Ten swaps × three brushes = 30 passes; `--max-paints` can collapse.
