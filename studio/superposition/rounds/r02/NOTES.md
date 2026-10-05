# superposition r02 — SUPERPOSITION, COMPUTED (mechanism) · parent: r01 · 2026-09-29

## Render

```
.venv/bin/python scripts/render_candidate.py studio/superposition/rounds/r02/piece.py \
  --fn superposition_computed --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,crimson,forestgreen,black \
  --out gallery/studio/superposition/current/pp_superposition_SUPERPOSITION-COMPUTED_v15.png
```

- Final: `gallery/studio/superposition/current/pp_superposition_SUPERPOSITION-COMPUTED_v15.png` + `.gcode`. A4 portrait, cream.
- Seed 7. The piece draws nothing random. Seeds 3, 7 and 11 give byte-identical gcode bodies
  (md5 `c0881eb8…` on v15).
- Data: `head.npz` in this round, written by `mechanism.py` in this round. `mechanism.py` is a
  numpy-only GPT-2 small forward pass; its IO, tokeniser and forward code are adapted from
  `studio/orrery/rounds/r02/mechanism.py`. To regenerate it:
  `.venv/bin/python studio/superposition/rounds/r02/mechanism.py --weights <model.safetensors> --aux <dir with vocab.json, merges.txt> --layer 11 --head 8`.
  Add `--dump all.npz` to save every head for a scan.
- Self-rounds: v1 → v15, 15 renders, none overwritten.

## Lineage

**Systems art: Manfred Mohr, *Cubic Limit* (1973–75).** Mohr shows a high-dimensional object
only through its projections under one stated rule, so the rule itself becomes the image. This
plate takes that order. Each of the 64-dimensional vectors in the head appears only as its
projection into one rule, `f(x) = Σ (c·e_n) φ_n(x/σ)` in the Hermite functions. Because the
rule is linear and orthonormal, the drawing keeps the algebra: overlap is dot product, and a
weighted sum of curves is the weighted sum of the vectors. The plate takes Mohr's rule and not
his look (no cube edges). No other plate in this batch cites Mohr; the ones that do cite someone
use Kandinsky, Nees, Molnár, Riley, Vasarely, Albers, Smithson, Duchamp, Whitney and Cellarius.

**Twist:** the Hermite functions are the eigenstates of the quantum harmonic oscillator. So
every vector on the sheet is drawn, exactly, as a wavefunction in superposition. The data then
supplies the punchline: in GPT-2's layer 11, head 8, the pronoun " itself" does not choose an
antecedent. It is literally `.26 hole + .14 transformer + .14 plot + .13 ter + .11 watched + .23 rest`.
The plate's last line says this in words.

## Mandate responses

`studio/superposition/` has no LEDGER.md and no FEEDBACK.md, so no J*/A*/S* rows are open. The
binding brief is the curator note plus DESCRIPTION.md § Weak and § Next versions (1).

| id | mandate | status |
|---|---|---|
| CUR-1 | Keep the cream-sheet vertical rhythm Q/K → field → softmax → V → Z | FIXED. The same five stations sit on one axis in the same order, with the same fan grammar (leave vertically, run, arrive vertically). |
| CUR-2 | No pen cap, every meaningful colour stays, each pen is one clean layer with a stated order | FIXED. 5 pens. Each pen is emitted once, as one layer. Order is light → dark: goldenrod V, blue K, crimson Q, green Z, black field/softmax/type. Reason: black lands last over everything, and green lands after the ochre strands that pour into it. |
| CUR-3 | Strokes spatially ordered for batching | FIXED. Each layer is chained greedily by nearest END, reversing strokes to suit, starting from the park point, so the pipeline's nearest-start pass reproduces the chain. Longest stroke is 184 mm (22 s). The pyramid outline is split into its 3 edges. Sheet-crossing hops inside a layer: black has 1 of 129 mm and 9 of 40–60 mm; each other layer has at most 3 over 40 mm. |
| CUR-4 | Minutes per layer and total | FIXED. See Plot budget: 53.6 min of plotting + 5 swaps = 61 min, down from ~206 min for r01. |
| CUR-5 | Most wasteful plate of the batch: 5573 pen cycles, 128 % travel; dotted lines are the cost | FIXED. **1 123 pen cycles (−80 %).** No dotted line is left. Every broken line is a dash whose duty carries data: Q/K strands are 50 % duty, and softmax→V and V→Z strands use duty = a_j / max a. Travel is 5.22 m against 6.78 m draw (77 %). About 3 m of that travel is the gaps inside dashes, 1–3 mm hops. |
| CUR-6 | Name the LINEAGE | FIXED. Mohr, *Cubic Limit*, plus the oscillator twist. |
| W-concept-1 | A schematic of the equation, a trace of someone else's figure | ARGUED / partly FIXED. The stations and their order are kept because the curator note binds them. Nothing on the sheet is traced now, and every mark is a number. The pyramid is a new order (strata, one per query, context growing downward) that the reference does not have. |
| W-concept-2 | Curves carry no data | FIXED. Every curve, cell, spike, strand duty and nest member is computed from Q, K and V. Checks are below. |
| W-tension | Perfectly symmetric about u 0.50 | PARTLY FIXED. The frame is still centred (curator rhythm), but its content is asymmetric by the data. The mass of the field sits on the diagonal (right) side, the sea is upper-left, the spike pattern is 2-left/1-centre/2-right with unequal heights, and the V row is heavier on the right. |
| W-hierarchy | The map is only 0.36 of the width | FIXED. The pyramid is 0.68 of the drawable width (129 mm), and it is the only closed black form. |
| W-craft-1 | Stipple wash reads as dirt; loose dots read as debris | FIXED. There is no stipple and no scatter. Tone is only ring count. |
| W-craft-2 | Third vortex invisible | FIXED by removal. There are no invented vortices. Each eye is one (query, key) cell above uniform. |
| W-depth | Flat, not declared | DECLARED flat. The only depth cue is over/under: the family curves go silent where a later curve would crowd an earlier one, so heavier members pass in front. |

## What changed from parent

A new composition on the same spine. r01 traced the reference's pixels. r02 keeps the five
stations and fans but rebuilds every one of them as data:

- **Q and K families are now vectors drawn in a Hermite basis.** Each token is one skewed bell
  on a ruler, one bell per token. " itself" is the only perfectly symmetric red bell, because
  the Q frame is built around it. The rulers are mirrored (token 0 at the centre) so the fans
  never cross.
- **The contour lozenge became the causal attention matrix, drawn as a pyramid.** Query i is
  stratum i and holds i+1 cells. The left edge is key 0 (the Q strands land there, one per
  row). The right edge is the diagonal (the K strands land there, one per column). Blank paper
  inside the triangle is attention below uniform.
- **The r01 axis line through the map is now the slice**: row 12, " itself". Its two end rings
  are where the itself-query strand and the itself-key strand land.
- **Softmax spikes are that row, exponentiated.** They stand under their own cells. The dashed
  line at 1/13 is uniform attention, which is also the pyramid's coastline.
- **V is the 13 values " itself" can see**, in the z frame. The two future values are open rings.
- **Z is now the partial sums in weight order.** They nest up to z, which is a pure Gaussian by
  construction, because every lopsided value cancels in the weighted sum.
- The sentence is set once at the top, and the pronoun's decomposition at the foot.

## Measurements / computations

**Provenance.** `mechanism.py` checks GPT-2 attention against HuggingFace/torch for all 12
layers: max |A_numpy − A_torch| = 4.0e-7, 6.4e-7, 1.1e-6, 2.3e-6, 1.8e-6, 1.8e-6, 2.2e-6,
1.8e-6, 1.4e-6, 1.9e-6, 1.8e-6, 7.4e-7. The piece recomputes A from Q and K itself:
|A − A_file| = 0, and |a·V − z| = 2.2e-16.

**Head choice.** I scanned all 144 heads × queries 8..14 for rows with 3–6 keys above 0.08, a
max weight of 0.2–0.55 and a sink weight under 0.2. L11H8 / " itself" was chosen because its
weight spreads over the candidate antecedents with no sink (a_The = 1e-4). L4H3 is used by
orrery and L2H9 by attention-weaving, so this head is new to the collection.

**The softmax row** (a_j for j = The … itself):
`.0001 .0563 .1397 .1275 .0449 .0123 .0116 .2558 .0368 .0181 .1401 .1064 .0504`.
The scores q·k/8 are `-5.72 .60 1.51 1.41 .37 -.93 -.99 2.11 .17 -.54 1.51 1.23 .49`.
Five keys are above uniform (1/13): plot, ter, hole, transformer, watched. These are the five
spikes above the dashed line, the five drop lines, and the five labelled V clusters.

**The pyramid.** Lift = ln(A_ij·(i+1)). Max lift is 2.086 at '.'→'.'. Row 12 lifts:
plot .597, ter .505, hole 1.202, transformer .600, watched .324, all others 0. Each cell is a
cone of height = lift and radius 11.2 mm × lift / 2.086, so every cone has slope 0.186 /mm.
The level step is 0.177 nat, which is exactly 0.95 mm ring pitch on every island. 11 levels,
98 contour chains. Check: sampled at every one of the 120 cell centres, F equals the cell's
own lift to within grid resolution, except (13,13) (0.75 vs 0.07) and (14,13) (0.36 vs 0);
the '.'→'.' corner cone spills onto them. **On the slice row every cell is exact.** So an
eye on the dashed line means that key is above uniform, and blank paper means it is not.
Where two cones overlap, their slopes add (raw minimum pitch 0.58 mm). The engine's
`Occupancy` pause-resume silenced 105 mm of ring there instead of letting it flood.

**Frames and truncation (3 Hermite modes are drawn).** These are the fraction of each vector's
squared norm that the drawing carries:
- Q (frame e0 = q_itself, e1–e2 = PCA of queries 1..14 ⊥ e0):
  `.01 .61 .67 .72 .72 .63 .61 .66 .79 .65 .55 .86 1.00 .80 .71`. " itself" is exactly 1.0,
  a pure bell.
- K (e0 = mean key of tokens 1..14): `.07 .82 .83 .84 .81 .81 .87 .82 .85 .84 .83 .88 .84 .89 .90`.
- V (e0 = ẑ, e1–e2 = PCA of a_j v_j ⊥ ẑ): `.01 .39 .90 .92 .63 .47 .16 1.00 .51 .51 .77 .69 .56`.
- The sink " The" is almost invisible in every frame (.01/.07/.01). |q| 17.1, |k| 15.4 and
  |v| 58.0 are the largest in the sentence, yet each is orthogonal to everything the head uses.
  The plate draws it faithfully as the flattest member of each family.

**The cancellation (Z).** z in its own frame = (5.3315, 0, 0) to 1e-12. The partial sums in
weight order are (φ0, φ1, φ2):
hole (1.78, −1.09, −.03) → +transformer (2.41, −.64, −.30) → +plot (3.28, −.43, .00) →
+ter (4.05, −.21, .39) → +watched (4.38, −.06, .02) → … → z (5.33, 0, 0).
The lean (φ1) falls from −1.09 to 0 as values are added: that is the visible straightening of
the green nest. 7 of the 13 partial sums stand ≥ 1.8 mm clear and are drawn.

**Scales.** Q/K share 3.1 mm/unit and σ 3.3 mm. V uses 3.2 mm/unit and σ 3.4 mm. Z uses
7.0 mm/unit and σ 12 mm (Z is drawn 2.2× taller and 3.5× wider than V). Softmax uses 72 mm per
unit attention, so hole = 18.4 mm. The pyramid has 9.2 mm cells and 5.6 mm row pitch.

**Line spacing** was audited on the final gcode. The test is: sampled at 0.4 mm, is there any
pair of distinct strokes with ≥ 3 mm of sustained near-parallel (|cos| > 0.94) contact under
0.8 mm? Result: goldenrod 0, blue 0, crimson 0, green 0, black 0. The only marks under the
floor are the solid dots, which are 0.3 mm spirals inside discs of ≤ 1.8 mm (a declared
exception, the same one r01 made). Bounds: every drawn coordinate is inside [10, 200] × [10, 287].
The only out-of-area move is the final park `G0 X0 Y0`.

## Plot budget

Leo model (`promptplot.plotjob`: draws capped at F500, travel F2000, 2 s per pen cycle, 90 s
per swap):

| order | pen | meaning | draw m | travel m | cycles | min |
|---|---|---|---:|---:|---:|---:|
| 1 | goldenrod | V (13 value curves + baseline), softmax→V and V→Z strands (duty = a_j/max a), V landing rings | 0.92 | 1.15 | 201 | 9.1 |
| 2 | dodgerblue | K family (15 key curves), K→column strands | 1.15 | 0.99 | 191 | 9.1 |
| 3 | crimson | Q family (15 query curves), Q→row strands, " itself" strand solid + apex dot | 1.08 | 0.77 | 174 | 8.3 |
| 4 | forestgreen | Z nest (7 partial sums incl. z) + baseline | 0.42 | 0.12 | 8 | 1.2 |
| 5 | black | pyramid rings + outline, slice, softmax row, drops, all type | 3.23 | 2.20 | 549 | 25.9 |
| | **total** | | **6.78** | **5.22** | **1 123** | **53.6 + 5 swaps = 61.1** |

- Commands: 22 561. The parent (r01 v16) had 68 825 commands, 5 573 cycles and ~206 min.
- 298 of the 549 black cycles are type: the top sentence, the bottom equation and the labels,
  each glyph stroke is one lift. Type is the largest single cost on the sheet, about 10 min.

## Self-critique

| dimension | score | note |
|---|---:|---|
| Hierarchy | 7 | At 3 m the black pyramid (0.68 of the width, the only closed form) leads. The red/blue curtains of fans are second, V and Z are third. The Q/K families are still busy enough to compete at the top. |
| Grid & alignment | 7 | One axis. The spikes stand exactly under their cells. Fan ends land on the triangle's edges by construction. The labels V, Z = AV and softmax sit by eye relative to their stations. |
| Tension & asymmetry | 5 | The centred spine is inherited and binding. The asymmetry is all in the data (mass on the diagonal, upper-left sea), not in the layout. |
| Negative space | 7 | The upper-left sea inside the pyramid is shaped by the mechanism (below-uniform attention). The flanks of the softmax row are quiet. The bottom band is only caption. |
| Craft for pen | 7 | 0 spacing violations, 1 123 cycles, no stroke over 184 mm. The pause-resume gaps in the families read as over/under. The '.'→'.' corner eye is cut hard by the outline. |
| Concept legibility | 7 | Rows ↔ strata ↔ spikes ↔ values ↔ nest can be traced by eye, and the last line lands the joke. The Hermite rule is invisible without NOTES, so the families read as "bells" rather than as "vectors". |
| Depth | 5 | Declared flat (a matrix and its projections are flat). Over/under gaps are the only depth. |

**The single worst thing:** the '.'→'.' eye in the pyramid's bottom-right corner. It is the
largest lift on the sheet (0.537 of '.' attends to itself), so it is the heaviest black mass.
It belongs to a query the plate is not about, and the outline clips a third of its rings.
It is true, but it pulls the eye away from the slice.

**Honest conceptual weakness:** the Q and K families show 3 of 64 dimensions (55–90 % of the
norm). Their bells are real projections, but the overlap = dot product identity holds exactly
only for " itself" against each key (φ0 alone carries q). You cannot read the map's rows off
the families by eye.

## Engine requests

1. `postprocess.optimize_stroke_order` restarts every colour layer from (0, 0) and never
   reverses a stroke. This piece pre-chains with reversal and relies on the nearest-start pass
   to reproduce the chain. A band/serpentine order with reversal in the pipeline would remove
   the last long hops.
2. `_GLYPHS['i']` / `'l'` ink sits outside their proportional advance (same bug orrery
   reported). This piece sets every label by measured ink extents (`label()` in piece.py).
3. `render_candidate.py` reports "Bounds validation: N violations" for the final park move
   `G0 X0 Y0`, which is outside the drawable area by design. That is noise worth silencing.
