# DALÍ ATTENTION — ENGRAVING IN FOUR NIBS
**Essence:** the same transformer stage as a surreal copper-plate engraving — melting crowned figures, a chessboard dripping into a softmax basin, a cellist with hair as a guided flow, FFN chambers as vaulted rooms — all tone made of real strokes on paper. **Status:** to reconstruct; oracle = `gallery/references/oracles/interpretive_plotter/results/verification/dali_engraving/` (24,678 paths; nibs 0.10 fine / 0.18 form / 0.25 structure / 0.35 bold; black on A3 portrait).

## The idea (the true thing)
As `cubist-repro`, drawn as surfaces rather than planes: skin and cloth are curved nets whose rows break by tone; hair and drips are guided families with a travelling highlight; deep shadow admits a crossed net; eyes and lips are protected holes.

## Pen-plotter visual (our engine)
- Skin/cloth: `surface_grid` with a `gauss_tone` shadow plan per face/torso (`bend` 15–17, `slope` ±9–19; chambers `bend` −13), rows on the 0.10 nib, cross only in shadow.
- Hair, drips, flows: `flow_family` between two authored guides, `highlight=True`, on the 0.18 nib; `dark_edge` rims on 0.35.
- Structure, labels, flows on 0.25; silhouette accents on 0.35; construction on 0.10.
- `suppress_parallel` over the hatch families before compile.

## Reference prompt
Reconstruct `ref/reference.png` — the engraving — as an authored scene. Contours first; then one material grammar per object. Judge: faces read with open eyes/lips, hair families coherent with a travelling shine, crossed skin shadow only in the dark, four nibs by role.

## Build notes
This is the deepest target and is expected to drive tuning of `engine/material.py`. Expect 12–15 h plot; Leo needs the re-zero checkpoint before this is plotted.
