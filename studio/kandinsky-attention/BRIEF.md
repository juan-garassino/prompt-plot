# ATTENTION AS RESONANCE — KANDINSKY
**Reference:** `studio/kandinsky-attention/ref/reference.png` (1122×1402, ratio 0.800
→ paper `24x30` cm = 240×300 mm portrait, exactly 0.8).
**Read first:** `studio/KANDINSKY_SET.md` — the shared idiom AND the technical audit.
**Status:** to build.

Same subject as `studio/attention-passes/` and `studio/attention-weaving/`, and as
`bauhaus_relevance` / `attention_arcs` in the package. All different compositions —
read them to avoid repeating, then do something else.

## What the reference does
Portrait. Title `ATTENTION AS RESONANCE` in spaced serif caps.
- **Q** top-left in **red**: rows of marks — open rings, solid discs, triangles,
  comb/fringe glyphs — strung on dotted rules, with dashed curves sweeping down-right.
- **K** top-right in **blue**: the mirrored arrangement, with concentric-ring glyphs,
  dashed curves sweeping down-left.
- **Centre**: `QKᵀ/√d_k` over a **grid whose cells are concentric-ring "resonance"
  patterns** — ring density per cell is the score. Overlaid flat triangles (red, blue),
  a large thin circle, discs.
- Below it: `A = softmax(S)` drawn as a **curve of peaks standing on a ruled axis**,
  with open/filled circles at the feet.
- **V** bottom-left in **gold**: another glyph-row block, with dashed curves sweeping
  right.
- **Z = AV** bottom-right in **green**: half-disc and comb glyphs, the output.
- Scattered Bauhaus furniture throughout: flat triangles, discs, crosses, rules.

## What must be TRUE (and where the reference is suspect)
This is the plate with the most likely technical errors — audit it hard:
- **Softmax is per row of the score matrix.** The reference draws ONE 1-D peak curve
  beneath a 2-D grid. Decide what is actually being shown and draw something true:
  either one distribution for one selected query (say which), or a per-row treatment
  across the grid.
- **The peaks look equal-height.** Equal peaks = uniform attention = the mechanism
  doing nothing. Real attention is peaked. Make it visibly so, and make it sum to one.
- **Row counts must agree**: `Z = AV` has one row per QUERY. Count Q's rows and Z's
  rows in the reference and reconcile them.
- The score grid is `n_queries × n_keys` — check the reference's grid matches its own
  Q and K block sizes.
- Resonance is a good metaphor *if* ring density means score. Make that mapping exact
  and state it.

## Pens
`red` Q · `blue` K · `gold` V · `green` Z · `black` grid, rules, type, furniture.
Cream paper.
