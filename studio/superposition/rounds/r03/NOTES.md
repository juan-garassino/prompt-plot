# superposition r03 — INTERFERENCE FIELD (abstract) · parent: r01 · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/superposition/rounds/r03/piece.py \
  --fn superposition_interference_field --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,crimson,forestgreen,black,black \
  --out gallery/studio/superposition/current/pp_superposition_INTERFERENCE_FIELD_v9.png
```

- Final: `gallery/studio/superposition/current/pp_superposition_INTERFERENCE_FIELD_v9.png` + `.gcode`. A4 portrait, cream.
- Seed 7. Nothing in the piece is random. Seeds 3, 7 and 11 give byte-identical gcode bodies
  (md5 `4da23cfa…` on v8; v9's body is `f8465240…`).
- Data: `gpt2_head.npz` in this round, written by `mechanism.py` in this round:
  `.venv/bin/python studio/superposition/rounds/r03/mechanism.py --layer 5 --head 5 [--cache DIR]`.
  `mechanism.py` is the orrery r02 numpy GPT-2 forward pass, copied, with `--text`, a tensor
  cache, `--verify` and an induction-head `--scan` added.
- Self-rounds: v1 → v9, none overwritten.

## Lineage

**Op Art: Bridget Riley, *Cataract 3* (1967).** The order it lends is a single line family
whose swelling and pinching makes the surface move, with the information carried by the
drift and not by any figure. Here that family is one contour ladder. Where the model
attends, the lines swell into eyes, and ring count is weight. Where the text repeats, the
family bends into one band that runs parallel to a single straight cut (the causal mask).

The twist is the sentence: "Every wave that comes back meets itself.", written twice. In
optics, a fringe appears when a wave overlaps a delayed copy of itself. An induction head
does the same thing to a text that repeats: the second pass of the sentence attends one step
past its own first pass, and the attention matrix shows it as a fringe at exactly the delay.
The last token then predicts " Every", so the model expects the wave to come back once more.

## Mandate responses

`studio/superposition/` has no LEDGER.md and no FEEDBACK.md, so no J*/A*/S* rows are open.
The binding brief was the curator note, the INTERFERENCE FIELD paragraph and DESCRIPTION.md
§ Weak.

| id | mandate | status |
|---|---|---|
| CUR-1 | Keep the cream-sheet vertical rhythm Q/K → field → softmax → V → Z | FIXED: K ruler (top) and Q ruler (left) → field → section cut → softmax profile → V chords → Z. All five stations share one key axis, so the rhythm is now a column registration and not only a stack. |
| CUR-2 | No pen cap; each pen one clean layer with a stated order and meaning | FIXED: 6 pens, one layer each, never re-entered, light → dark (see Plot budget). |
| CUR-3 | Strokes spatially ordered for batching; minutes per layer + total | FIXED: pipeline nearest-neighbour ordering within each colour. Ruler lanes are drawn serpentine (alternate directions), which cut blue and red travel from 0.66/0.72 m to 0.41/0.41 m. Longest stroke 236 mm (the knife, 28 s at F500). Minutes: see Plot budget. |
| CUR-4 | Most wasteful plate: 5 573 pen cycles, 128 % travel, ~206 min; the dotted lines are the cost | FIXED: **320 cycles (−94 %)**, 51 % travel, **~24 min of drawing + 6 swaps ≈ 33 min**. No dotted construction line survives. The only dashed marks are the two V→Z connectors, whose duty is data (47 cycles). About half of all cycles (168) are type. |
| CUR-5 | Name the LINEAGE | FIXED: Riley, *Cataract 3*, above. |
| BRIEF-a | Collapse the pipeline into one element: a full-sheet contoured similarity field | FIXED: the field fills the upper 2/3 of the sheet (148 × 148 mm box). The coda under it is a single section through the field, not a separate diagram. |
| BRIEF-b | Eyes are the attended key positions | FIXED by construction: the field is the attention A itself, kernel-blended. Every eye sits on an (query, key) pair the head attends to. There are no invented eyes and no fbm. |
| BRIEF-c | Q and K reduced to two edge rulers (red top, blue left) that define it as an outer product | FIXED, with a swap ARGUED: the rulers are the 4 SVD mode pairs of S = QKᵀ/8 (S = Σ q_r k_rᵀ, 91 % of the energy). K is on top and Q on the left, not red on top. Rows are queries, so the softmax row and V below must share the key axis, and the top ruler must be K for the rhythm to register column by column. |
| BRIEF-d | Nested/flow order, dominant mass, asymmetric by the data, no stage labels | FIXED: no stage labels. The only type is the caption (the sentence twice, plus one meta line). The asymmetry is the causal triangle plus the data's own L-shaped path (sink column → fringe diagonal). |
| D-concept-1 | A schematic of the equation, and a traced reproduction | FIXED/ARGUED: nothing is traced, and there are no boxes or arrows. The honest risk is that it still reads as an attention heatmap (see Self-critique). |
| D-concept-2 | Curves carry no data | FIXED: every mark is GPT-2 small L5H5 output, and every scale is stated below. |
| D-tension | Perfectly symmetric about u 0.50 | FIXED: nothing on the sheet is mirrored. |
| D-hierarchy | Map ≈ 0.36 of width; nothing dominates | FIXED: the field box is 148 mm = 0.78 of the drawable width, and it is the only black mass. |
| D-craft-1 | Stipple wash reads as dirt, loose dots as debris; 69 k commands, 11 m travel | FIXED: no stipple and no scatter. 26.5 k commands, 3.2 m travel. |
| D-craft-2 | The claimed third vortex is invisible | FIXED: moot, because the field has no hand-placed vortices. Every eye is a data point. |
| D-depth | Flat, not declared | DECLARED FLAT: Riley's canon is flat, and the plate's depth device is the section cut (a plan above its own profile), not perspective. |

## What changed from parent

This is a rebuild, not a parameter pass. r01 traced an AI poster: bump families at reference
pixels and a hand-built field. r03 keeps only its rhythm and its colour-as-provenance, and
derives every mark from one real attention head.

- **The field is the hero, and it is data.** GPT-2 small, layer 5, head 5 (an induction
  head) reading the sentence twice. The first reading dumps all of its attention on token 0
  (the attention sink), which draws as a vertical column of eight eyes. At token 8 the
  sentence repeats, and the attention jumps onto a diagonal fringe one step past the
  earlier occurrence, which draws as eight eyes parallel to the knife. The future (key >
  query) is masked, so it is left as blank paper. That blank triangle is the plate's
  shaped void.
- **The section.** The field is cut through its last query row. The softmax "row" under it
  is that row's profile, drawn with the field's own kernel, so the key-0 and key-8 bells sit
  exactly under the half-eyes they come from.
- **Rulers.** Q and K are four principal channels each, drawn as lanes. Each lane is a
  natural cubic spline, exact at every token (max lattice error 0.0). The top K lane pair
  visibly repeats: first-copy against second-copy key channels correlate at 0.84 / 0.97 /
  0.99 / 0.98. The two attended keys (0 and 8, the start of each copy) are ringed on the K
  ruler, and the read-out query (15) is ringed on Q at the section.
- **V → Z.** Each value is a 3-bump chord in the uncentred principal basis of V. The sink's
  v₀ is nearly empty (|v₀| = 0.44 |v₈|) and draws almost flat. Z is the green chord at 4×.
  It is the exact A-weighted sum of the V chords, and its two connectors are dashed with
  duty = A (0.652, 0.295).
- Tried and cut on the way:
  - v1: scalar-score (pre-softmax) and log-attention fields. Spline-interpolated S makes an
    egg-crate at every lattice point, and Gaussian-blending S destroys the fringe, because
    induction scores are single-cell spikes.
  - v1: Hermite-Gauss V glyphs, which read as random squiggles.
  - v1 and v2: overlaid ruler modes (a tangle) and a 5-bump chord (unreadable).
  - v6: a nested A₈v₈ partial inside Z, cut because it grazed z under 0.8 mm for 94 mm.

## Measurements / computations

- **Forward pass:** numpy only. Verified against the cached HuggingFace torch attention
  (`~/.promptplot/attn_gpt2.npz`, the orrery sentence): max |A_numpy − A_torch| per layer,
  L0–L11 = 4.0e-7, 6.4e-7, 1.1e-6, 2.3e-6, 1.8e-6, 1.8e-6, 2.2e-6, 1.8e-6, 1.4e-6, 1.9e-6,
  1.8e-6, 7.4e-7.
- **Tokens (16):** `Every| wave| that| comes| back| meets| itself|.| Every| wave| that| comes| back| meets| itself|.`
- **Induction scan:** mean A(i → prev-occurrence + 1) over the 7 pairs (9,2) … (15,8):
  L5H1 0.858 · **L5H5 0.802** · L6H9 0.732 · L7H10 0.683 · L8H1 0.543. L5H5 was chosen over
  L5H1 because its last row is not a one-hot (H = 0.88 vs 0.21), so the softmax, V and Z
  stations carry two weights and not one.
- **Fringe weights** A(8,1) … A(15,8): 0.870, 0.927, 0.720, 0.701, 0.980, 0.808, 0.822, 0.652.
  The sink column A(0..7, 0) ranges 0.95–1.00.
- **Last row A[15]** (sums to 1.0000000): key 8 " Every" 0.6523 · key 0 "Every" 0.2949 ·
  key 7 "." 0.0297 · everything else ≤ 0.0045.
- **z check:** |A·V − z| = 8.7e-8. cos(z, v₈) = 0.986, and |z| / |v₈| = 0.754. The output
  is, to the eye, a shrunken copy of the value it attended to.
- **S = QKᵀ/8 SVD:** σ = 41.39, 21.89, 17.03, 15.54, 11.67. The top 4 hold 91.0 % of the
  energy. Rulers share one scale: 3.2 mm for the largest mode value.
- **V basis:** uncentred top-3 principal directions hold 78.2 % of V's energy. The chord
  scale is shared by V and Z (Z drawn at 4×, stated).
- **Field:**
  - A (causal, all 256 entries) is blended with an isotropic Gaussian kernel, σ = 4.2 mm on
    paper (token pitch 9.25 mm both ways, so the knife is exactly 45°).
  - It is evaluated on a 759 × 782 grid at 0.2 mm and contoured with contourpy.
  - The contours are clipped exactly to the knife x = y + ½ (cell-inclusive key ≤ query)
    with `geometry.clip`.
- **Contour ladder (Gaussian, scaled to the true max):**
  - Ring k is the level F_max·exp(−(k·p)²/2σ²), with p = 1.15 mm and F_max = 1.173. Summed
    neighbours lift the sink ridge above 1.
  - 10 levels down to the 0.02 floor.
  - An eye of weight a loses its innermost √(2σ² ln(F_max/a))/p rings, so ring count IS
    weight. Isolated-eye counts on the fringe are 8, 8, 7, 7, 8, 7, 7, 7; neighbouring eyes
    share their outer rings as the band.
  - Scaling to the max was a real fix. A ladder built for a peak of 1 pinched the ridge
    crest to 0.7 mm (209 mm of sub-floor contact in v6); v7 has 6.4 mm.
- **Visibility floor:** attention below ≈ 0.02 draws no ring, and connectors below A = 0.06
  round to no dash at the 5 mm period.
- **Line-spacing audit** (0.4 mm sampling, same pen, different strokes, |cos| > 0.94,
  < 0.8 mm):
  - black 6.4 mm: rings meeting the knife they are clipped to.
  - ochre 2.8 mm, green 5.2 mm: the valley between Z's bumps near its baseline.
  - blue 0, red 0.
  - type 131 mm at min 0.33 mm: glyph-internal strokes of 1.9–3.0 mm type, a declared
    exception.

## Plot budget

Model: draw at Leo's F500 cap, travel at 2000 mm/min, 2 s per pen cycle, 90 s per swap.

| order | pen | meaning | draw | travel | cycles | min |
|---|---|---|---|---|---|---|
| 1 | 0 goldenrod | V chords + duty-dashed V→Z connectors | 0.52 m | 0.61 m | 47 | 2.9 |
| 2 | 1 dodgerblue | K ruler (4 key channels) + key ticks | 0.60 m | 0.41 m | 20 | 2.1 |
| 3 | 2 crimson | Q ruler (4 query channels) + query ticks | 0.59 m | 0.41 m | 20 | 2.0 |
| 4 | 3 forestgreen | Z chord + baseline | 0.11 m | 0.21 m | 2 | 0.4 |
| 5 | 4 black | attention field, causal knife, section, softmax profile | 3.76 m | 1.06 m | 63 | 10.1 |
| 6 | 5 black fine (0.1 mm) | caption type | 0.53 m | 0.45 m | 168 | 6.9 |
| | | **total** | **6.10 m** | **3.14 m (51 %)** | **320** | **24.4 + 9 swaps ≈ 33** |

- **Why this order:** light → dark, so the black field lands last among the structure. Type
  goes last on its own finest pen. No two pens overlap anywhere, so the order is about
  smear risk, not occlusion.
- About 1.5 m of the travel is the six park-to-first-stroke approaches.
- 26 529 commands.

## Self-critique

| dimension | score | note |
|---|---|---|
| Hierarchy | 7 | One black mass dominates. The coda reads second and the rulers third, but the rulers are too quiet at 3 m. |
| Grid & alignment | 8 | One key axis runs K ticks → field columns → section → softmax bells → V chords. The coda shares one left edge. Q lanes end on the section, and Z is flush to the field's right edge. |
| Tension & asymmetry | 7 | The 45° knife against a parallel fringe, and an L-shaped data path. Nothing is centred. |
| Negative space | 8 | The masked future is a shaped void, and the unattended interior of the triangle is blank. |
| Craft for pen | 8 | Gaps are ≥ 1.15 mm by construction and audited. 320 cycles, no dotted runs, clean layers. |
| Concept legibility | 6 | The sink → fringe switch at the repeat is legible, and the caption confirms it. It is still an attention matrix, one step from "a field of contours". |
| Depth | 6 | Declared flat. The section (plan over profile) is the only spatial device. |

**The single worst thing:** the Q/K rulers are four thin lanes at ±3.2 mm. They do not read
as the factors of the field at a distance, and the K channels' true repetition (corr
0.84–0.99 between the two copies) is invisible at that amplitude. Bolder or fewer lanes
would crowd the top-left gutter, which is already sized against the sink ridge's outer ring.

## Engine requests

- `generators._GLYPHS['i']` is drawn at x = 1.8 but `_glyph_advance('i')` is 1.1, so `i`
  collides with the next letter ("itself" rendered "tself" in v1). Orrery r02 also reported
  this. Worked around with a local extent-measured `_set()`.
- `kit.even_contour_levels` cannot express a Gaussian ladder for kernel-blended fields,
  where ring k = F_max·exp(−(kp)²/2σ²). A `kit.gaussian_ladder(top, sigma, pitch, floor)`
  would give every blended-point field (attention, density, stipple-to-contour) exact
  pitch with ring count as weight.
- A `kit.duty_dash(polyline, period, duty)` helper: "tone drives duty" along a curve is
  hand-rolled in every piece that needs it (here `_dashed`).
