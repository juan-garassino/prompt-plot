# CUBIST ATTENTION — PLANES, SYMBOLS, SEMANTIC INK
**Essence:** the transformer block as a Picasso-cubist stage — queen (Q) and king (K) as faceted heads raking a chessboard (the score matrix) with red/blue rays, the board draining through a softmax funnel, a cellist (V), an FFN facet-room table, a residual bridge. **Status:** to reconstruct; oracle = `gallery/references/oracles/interpretive_plotter/results/verification/cubist/` (7,118 paths, 4 inks × 2 nibs, A3 portrait).

## The idea (the true thing)
Attention: three named sources meet on one grid; softmax normalises; values are mixed; FFN transforms each token; the residual adds the input back. Every labelled equation on the sheet is a real step of the block and must sit on the object that performs it.

## Pen-plotter visual (our engine)
- Style preset `cubist_plate`: inks black + red + yellow + blue; nibs 0.10 and 0.50 mm; rules `CUBIST_RULES` (queen planes red, king planes blue, cello/values yellow, everything else black; hatch always 0.10; silhouettes 0.48→0.50).
- Every form is a **plane**: a `cover` polygon, one hatch direction aligned to the plane (`fills`), **lit planes bare paper**, cross-hatch only on named shadow planes.
- Chessboard from four authored corners; rank/file lines only (no per-square outlines); dark squares hatched at 36°; pieces as a shared local-frame glyph, nearer pieces later in the scene.
- Lettering as `label` marks. Registration crosses. `paper frame`.

## Reference prompt
Reconstruct `ref/reference.png` — the painting — as an authored scene. Keep what makes it recognisable (two crowned profiles, board, cellist, softmax bowl, FFN table, residual arc, the equations); drop the pigment texture entirely. Judge against the oracle for plane hierarchy, ink semantics, bare lit planes and plot budget — not pixel match.

## Build notes
Name objects exactly as `CUBIST_RULES` expects (`queen veil plane`, `king outer cloak`, `board piece 3`, `board rank 1`, `ffn expanded facet 2-1`, `Q label`…) so ink and width come from the rules.
