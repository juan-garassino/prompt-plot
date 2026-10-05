# interference-annotated — r01

Exact recreation of `studio/interference-annotated/ref/reference.png`
(1122 × 1402, 0.800 aspect) as a 5-pen A4 portrait plate.

- Piece: `piece.py`, `attention_interference(rng, bounds, colors=5)`.
  **Nothing under `promptplot/` was modified** (and nothing there was reverted).
- Final render: `gallery/studio/interf_annot/current/pp_interf_annot_v8.png` (+ `.gcode`). Eight renders,
  seven real iteration rounds.
- Command:
  ```
  .venv/bin/python scripts/render_candidate.py studio/interference-annotated/rounds/r01/piece.py \
    --fn attention_interference --seed 7 --colors 5 --paper a4 --orientation portrait \
    --palette crimson,dodgerblue,goldenrod,forestgreen,black \
    --out gallery/studio/interf_annot/current/pp_interf_annot_v8.png
  ```
- Pens: 0 red (Q) · 1 blue (K) · 2 ochre (V) · 3 green (Z) · 4 black.

## Method: measured, not judged

Every landmark is a **pixel coordinate read off the reference raster** and mapped
by `Sheet`. Two scales, deliberately different:

- `l(px)` — isotropic. Nests stay circles, glyphs keep their proportions.
- `ly(px)` — vertical position only. The reference is 0.800 aspect and A4's
  drawable area is 0.686, so the layout stretches to fill the sheet.

A projected **surface** has no intrinsic aspect, so the weights disc and the Z
landscape take their vertical terms from `ly` as well. Skipping that is what made
both read ~15 % too flat in rounds 3–5, and stacking the render back into
reference-pixel space is the only reason it was caught.

**No text size is set by eye.** `_fit_cap` solves for the cap height that makes a
string exactly the width it occupies in the reference; `_block` sizes a whole
annotation block from the reference width of its widest line. The measured
annotation body is ~10 px cap on a 1402 px sheet (≈1.8 mm), and line pitch is a
uniform 16.3 px everywhere on the plate — both checked against column scans of
the raster rather than guessed.

## What each element actually is

**Q / K / V clusters.** Spiral nests at constant radial *pitch* (mm per turn, not
per radian) so a nest can never flood; `_fit`-free, 10 rings each, matching the
reference count. The connective tissue is **large thin circular arcs**, not short
links — an early round used short tangential links between nests and they read as
scribble; the reference has nothing of the sort. The bundle that drains each
cluster into the lattice node is a **spine with tapered lateral offsets**
(`_offset_spine`) rather than an integrated flow field: the curves are then
*guaranteed* to converge on the node and stay inside the cluster, which an ODE
will not promise. The spokes start near the nest **eye**, as the reference's do,
not on its rim.

**The woven lattice.** This is the element that took the most rounds to read
correctly. It is **not** two straight fans. Each node emits a fan of *parabolas* —
constant sideways acceleration — which is why the outer columns make a U (out,
vertex, back) and form the near-vertical walls of the rectangle while the inner
ones race across. Two mirrored families cross into the diamond mesh. The third
family, and the thing that makes it read as a rectangle rather than a skirt, is a
set of **full-width token rows** sagging gently under the weave; the dot grid sits
on their intersections with the 6 outermost columns each side.

**The weights disc.** Rings of a surface of revolution. The cone flank is the
**locus of the ring extremes**, not a stack of ring tops — once that was clear,
`h(r)` could be fitted directly from the raster: measuring each ring's widest
point gave `h(r) = 72·exp(−(r/79.5)^1.554)` px with a 0.35 flatten. Radii are
stepped so the *flank* gap stays constant (~1.7 mm), which is `even_contour_levels`
reasoning applied analytically — even radii bunch the flank and starve the rim.

**Z = AV.** A ridgeline of rows over an anisotropic bump, pinched to two nodes on
the axis, plus a concentric ring family at the summit. The rows alone can only
*fold*; they cannot close, and the reference's summit is a closed nest of ovals.
Both families share the same `hh()` so the rings sit on the folds rather than
floating over them.

## Overlap is a decision here, not a symptom

Twenty-two **reserved type boxes** (`KEEPOUT`) are measured off the raster, and
every geometry family — cluster curves, cluster orbits, lattice columns, lattice
rows — is cut out of them by `_reserve`. Verified numerically:

- Minimum ink distance from any geometry stroke to any glyph stroke: **0.91 mm**.
- Only 3 geometry samples anywhere on the plate are within 1.0 mm of type, and
  all three are intended: two are the radical sign's own spacing inside
  `Q·Kᵀ/√dₖ`, one is the bottom-right corner mark at 0.94 mm from the footer.
- The bottom corner marks were **moved and shortened** from their reference
  positions (to 48 / 1074 px, 32 px tall) because at the reference's own
  placement the vertical rule runs straight through "TRANSFORMERS" / "SAME". A
  corner rule through a word is a collision, not a composition.
- Every reserved box was checked to actually contain the type it reserves — one
  did not ("contextualized output" sits at py 1365–1372, the box stopped at
  1366) and was corrected.

## Honest list of differences from the reference

1. **Serif and italic type do not exist in the shared stroke font.** The
   reference sets its title and labels in a serif and its mathematics in serif
   italic; this is a single-stroke sans throughout. Known permanent gap — not
   chased. Two characters are also **missing from `_GLYPHS`** and are drawn as
   geometry inside the formula builder, not as a local glyph table:
   **`√` U+221A** and **`·` U+00B7**. Worth adding centrally.
2. **The Z landscape is fuller than the reference's.** The reference's rows
   separate cleanly in the lower half with real white between them, and its
   butterfly wings are sharper; mine fills the lens more evenly and the wings are
   soft. The row family cannot produce the reference's closed summit ovals on its
   own, so the summit is drawn as a second, ring family — a recreation of the
   appearance rather than of the generating method, and the seam is visible if
   you look for it.
3. **The clusters read busier than the reference.** The reference is a raster
   with continuous line weight: its nests fade toward their rims, its dashed
   orbits are a whisper, and a third of its curves are half-tone ghosts. At one
   pen weight all of that lands at full strength, so the same curve count reads
   denser and there is less white in the upper third than the original has.
4. The long connective arcs are exact circles; the reference's are hand-varied,
   so its cluster has a looser, less mechanical rhythm.
5. The lattice's grey "ghost" layer behind the weave (visible in the reference as
   soft second-order curves) is absent — a single pen cannot make it.
6. The reference's dotted orbit rings are finer than a 0.35 mm dash can be at
   this pen tip; mine read as short dashes rather than dots.

## Plot metrics (seed 7, A4 portrait, 5 pens)

| | |
|---|---|
| draw | 16 248 mm — red 2 641 · blue 2 502 · ochre 2 043 · green 2 484 · black 6 578 |
| travel | 12 185 mm |
| pen cycles (M3) | 2 071 |
| strokes | 2 071 (259 longer than 6 mm) |
| commands | 48 040 |
| out of bounds | 0 |

**Line spacing.** Minimum designed separation is 0.85 mm (disc ring step floor
1.35 mm, nest pitch 1.05–1.29 mm, Z summit rings 1.44 mm, lattice rows 2.8 mm).
Sampling all non-dot, non-type strokes at 0.4 mm, 30 % of samples lie within
0.8 mm of a *near-parallel* neighbour, but that figure is dominated by the four
places the composition deliberately converges to a point — the two lattice nodes,
the two Z nodes and the V read-out column — plus the three deliberately
overlapping furniture circles at each margin (min separation 0.00 mm there, as in
the reference). Away from those, nothing crowds.

**Determinism.** The piece consumes no randomness at all — it is a recreation, so
every position is measured rather than sampled. Same seed *or any seed* gives a
byte-identical command list; two `render_candidate` runs differ only in the
GCode header timestamp. Degrades correctly to `colors=1` and re-fits cleanly to
A3 landscape.
