# ATTENTION — FORWARD AND BACKWARD / SOFTMAX IS A VANISHING POINT — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/attention_passes` |
| current render | `gallery/studio/attention_passes/current/pp_attention_passes_faithful_v12.png` · `gallery/studio/attention_passes/current/pp_attention_passes_mechanism_v15.png` · `gallery/studio/attention_passes/current/pp_attention_passes_abstract_v9.png` |
| source | faithful: `studio/attention-passes/rounds/r01/piece.py::attention_passes` · mechanism: `studio/attention-passes/rounds/r02/piece.py::attention_passes` (+ `mechanism.py`) · abstract: `studio/attention-passes/rounds/r03/piece.py::attention_passes` |
| paper · pens | A3 landscape (420 × 297), cream · 0 black = K + ∂L/∂K, lattice, comb/pencil, all structure and type · 1 dodgerblue = Q + ∂L/∂Q (scarce) · 2 crimson = V, ∂L/∂V, Z / z, ∂L/∂Z |
| status | unreviewed (no FEEDBACK.md) · 36 renders on disk (3 current, 33 trials: faithful v1–v11, mechanism v1–v14, abstract v1–v8) |

## In one line
Attention as **convergent flow then the same flow run backward** — faithful and mechanism are two-register flow plates (three source wells → similarity lattice → softmax waist → Z, mirrored below for the gradient; mechanism drives every mark from real GPT-2 L1 H0 row 12), while abstract transposes it to a **projective pencil through one vanishing point** (a 336 mm raw-score rail cut by concurrent rays down to a 125 mm unit bar; the backward pass is the same rays continued past the apex).

## What is on the sheet

### faithful v12 (r01)
- **Two registers, same row pitch.** Forward register v ≈ 0.10–0.45, backward v ≈ 0.54–0.87, with ≈ 24 mm of bare paper between them. Left label column at u ≈ 0.06: `Q` (blue, v 0.15), `K` (black, v 0.27), `V` (crimson, v 0.41), `∂L/∂Q` (blue, v 0.57), `∂L/∂K` (black, v 0.68), `∂L/∂V` (crimson, v 0.82); a dashed register rule at u 0.04 with a node dot on every row, plus loose black vertical tick bars beside K and V.
- **Wells** at u ≈ 0.10–0.21: Q a blue dotted teardrop fan (0.18, 0.15) around a filled square node; K a black dotted four-lobed clover (0.16, 0.27); V a crimson dashed/dotted oblong (0.15, 0.41). Each is followed by a dotted "fade" wedge at u 0.21–0.32. Backward wells mirror them at 80 % scale.
- **Stations**, three vertical dashed rules labelled at the top (v 0.07) in small caps: `similarity` (u 0.43), `softmax` (u 0.61), `weighted values` (u 0.81).
- **Similarity lattice** (u 0.36–0.50, v 0.13–0.37): a dense square dot grid; the blue Q fan enters its upper band, the black K fan (necked at u 0.28) its lower band. The black bundle leaves the lattice's right edge and funnels to a point at (0.54, 0.22).
- **Softmax comb** at u 0.61: horizontal black bars of varying length on the dashed rule — the longest ≈ 0.095 W at v 0.22, a second peak at v 0.31, a tail of short ticks. The loudest mark in the register.
- **V strands** (crimson) run nearly flat under the lattice at v ≈ 0.40–0.44, rise after softmax and swell into a **high crimson arch** peaking at (0.81, 0.10), falling into the `Z` node (0.92, 0.30); a symmetric black almond lens sits below the arch (u 0.68–0.91, v 0.29–0.38). Big `Z` label at (0.97, 0.30).
- **Backward register:** same geometry, sparser lattice (2× subsample), smaller comb, a lower crimson arch into `∂L/∂Z` at (0.92, 0.71), strands carrying small **left-pointing filled arrowheads**; right label `backpropagate` / `gradients` at (0.93, 0.61–0.63).
- **Bottom axis** (v 0.92): `forward pass` with arrow → under the left half, a dot at u 0.50, `← backward pass` under the right half; registration crosses in all four corners; a handful of isolated black dots scattered in the margins.

### mechanism v15 (r02)
- Same two-register frame and label column, but every bundle is **necked** and the stations moved left: `similarity` u 0.47, `softmax` u 0.64, `weighted values` u 0.79 (dotted rules; spaced-caps labels at v 0.05).
- **Q** is one blue ribbon of ~12 hairlines leaving a two-lobed dotted butterfly well (0.14–0.31, 0.07–0.24) and pinching to a point at (0.52, 0.14). **K** is a black dotted peanut well (0.10–0.32, 0.24–0.38) whose strands braid through a tight neck at (0.31, 0.30) then fan into the lattice. **V** is a stack of crimson dotted horizontal laminae (0.12–0.39, 0.39–0.52).
- **Score lattice** (u 0.42–0.52, v 0.16–0.43): rows of dots of genuinely varying size, with a **blue focus column** at u 0.51 (the chosen query's scores as blue dots).
- **Softmax waist** at u 0.64: the black bundle converges into a narrow throat (v 0.23–0.35); the comb is short horizontal ticks with **blue bars**, the longest at v 0.34, annotated `a = 0.5024` in blue at (0.66, 0.24).
- **Weighted values → Z:** crimson strands dip to v 0.52 at u 0.55, then rise in a broad S and converge with the blue strands into the `Z` node (0.93, 0.30). The crossing of red and blue at u 0.62–0.78 is the densest zone of the plate.
- **Annotation block** in the band between registers (u 0.06–0.38, v 0.54–0.59): blue `sum a = 1.000000   max a = 0.5024 at key 11`, black `softmax keeps the order and destroys the scale`, crimson `∂L/∂V = Aᵀ ∂L/∂Z    the same weights, transposed`. Right: `backpropagate` / `gradients` right-aligned (0.87–0.94, 0.60–0.62).
- **Backward register** (v 0.62–0.87): blue ∂L/∂Q bundle lifts high (v 0.61) and drops as a vertical curtain at u 0.52; black ∂L/∂K fan; backward lattice of ticks and dots; crimson ∂L/∂V strands sweep up-right across the black and blue into `∂L/∂Z` (0.93, 0.75). **All backward arrowheads — blue at u 0.57 and crimson at u 0.75 — point RIGHT**, toward ∂L/∂Z (observed in a 3× crop).
- **Bottom axis** (v 0.93): `forward pass` ——◀ • ▶—— `backward pass` — the two arrowheads point **away** from the centre dot, i.e. forward points left. Below it tiny type `gpt2  layer 1  head 0  query 12  |  15 tokens  |  d = 64`. Corner crosses at the bottom corners only.

### abstract v9 (r03)
- **The pencil (dominant mass).** ~13 black rays converge from the long raw rail down-right onto one **apex drawn as a 4 mm open circle** at (0.74, 0.78), labelled `softmax` to its right. Past the apex the rays continue as a narrower fan cropping at the bottom and right edges of the design box.
- **q axis** (the only blue): one long line raked ≈ 4.5° from (0.05, 0.31) to (0.95, 0.21), crossing the whole sheet, with a graduated tick ladder (ticks larger at the left); blue `q` at (0.06, 0.32).
- **Key field** above it: 12 black open rings on sticks of varying length standing on the q axis, u 0.13–0.54, v 0.10–0.25; three small upward arrowheads on the left sticks; large black `k` at (0.25, 0.05).
- **Raw rail**: a heavy black line from (0.08, 0.46) to (0.88, 0.37) with cell ticks, fed by thin connectors from each key foot; labels `s = q · k j` (0.07, 0.35) and `exp s` (0.07, 0.43).
- **Unit bar mass (crimson)** at u 0.49–0.79, v 0.47–0.66: a stepped skyline of densely hatched cells — two tall blocks (u 0.49–0.58 and 0.65–0.71), lower cells stepping down to the right, the last cells a tight zig-zag; the pencil rays cut through it dividing the cells. A heavy tilted crimson **`z` rule** crosses it from (0.45, 0.55) to (0.81, 0.51); crimson `z` label at (0.46, 0.55), crimson `V` at (0.61, 0.46), black `one` at (0.52, 0.67), and a stray `H` glyph at the bar's right end (0.79, 0.64).
- **Gradient mass** past the apex: a flat-topped crimson hatched block (u 0.71–0.86, v 0.84–0.93) cut by the backward rays, crimson rule under it, `∂L/∂z` label at (0.67, 0.95).
- **Type** flush-left on u 0.14 in the triangular void below-left: short heavy rule (v 0.58), `forward and backward` (v 0.60), headline `SOFTMAX / IS A / VANISHING / POINT` in 4 lines of ≈ 14 mm outlined caps (u 0.14–0.45, v 0.60–0.83), then a 3-line data block (v 0.88–0.94): `12 keys · sum exp s = 33.26 · sum a = 1.000 · a max = 0.316 · z = 0.658`, `one = 125 mm cut from 336 mm · ∂L/∂v j = 0.457 × a j · same rays`, `2 cells fall under the pen tip: 0.013 of the mass. merged`.
- **Quiet zones:** the upper-right above the q axis (u 0.55–0.95, v 0.05–0.25) and the triangle left of the leftmost ray holding the headline. One registration cross bottom-right (0.93, 0.95).

## The science it encodes
- **faithful (r01 NOTES):** a recreation of `ref/reference.png` with de-crowding — row registration (backward pitch equals forward), comb ink-passes ∝ probability at a tuned temperature, left-pointing arrowheads (a v10 bug had them pointing right). Numbers are seeded, not from a model.
- **mechanism (r02 NOTES, `mechanism.py`):** real GPT-2 attention, **layer 1, head 0, query row 12**, 13 causal keys; row sums to 1 (float64), argmax key 11 at a = 0.5024, second tier 0.1388 / 0.1165, perplexity 5.475, max/min 359:1. Q and K are recovered exactly from A up to the softmax row-shift gauge; the backward pass is computed by hand and checked by a directional gradient test. **V is not GPT-2's V** (stated in NOTES). Dot radii, tooth lengths, ribbon widths and ink passes are computed. On the sheet the peaked comb and `a = 0.5024` are visible; the reversed backward arrowheads contradict the brief's "arrowheads pointing left" and the NOTES' own claim that direction is carried by them.
- **abstract (r03 NOTES):** intercept theorem as softmax — a pencil of concurrent lines cuts two parallel transversals in identical ratios, so the unit-bar cell boundaries fall where the rays land and equal aⱼ by construction; similarity = perpendicular projection of the key cloud onto q (foot = s, pole length = discarded component); exp cell width = exp(sⱼ), Σexp = 33.26; merge area = aⱼvⱼ, the `z` rule = Σaⱼvⱼ; backward = same rays past the apex, ∂L/∂vⱼ = aⱼ · ∂L/∂z (0.457). a_max = 0.316, 12 keys; two sub-tip cells merged (0.013 of mass). The values vⱼ are assigned (seeded), not a model's.

## How it got here
- **faithful** v1→v12: layout measured from the reference; wells enlarged (v2); comb weight ∝ probability (v3); Q parabolae flipped (v4); softmax pushed right to give the narrowing room (v5); marks rebuilt as chord discs (v6); backward stages squeezed (v7); beads on weighted-values crossings (v8); **v10 fixed backward arrowheads pointing right**; v11/v12 comb temperature. Trials v3 and v6 show the comb as a tall fishbone spike stack and the Q fan crossing K diagonally over the lattice — v12 calmed both. Gained order; lost some of the reference's turbulence.
- **mechanism** v1→v15: v1 wells collided (334 bounds violations); v3 found `_dot` draws dashes so the score matrix never rendered; v4 `_blob` discs + transposed lattice; v5 V moved to `weighted values`; v6 Q reduced to one ribbon; v7–v8 every bundle necks; v10–v11 waist re-encoded; v13–v14 ∂L/∂Q re-routed through a throat so it stops erasing the backward lattice (visible trials v9 → v14: the blue gradient curtain at u 0.52 is the v14 move). v15 geometry = v14.
- **abstract** v1→v9: v1 degenerate (crushed fan); v2 q flipped so crowding becomes angular spread; v3 bug — deficit hatch silently missing; v4 stepped crimson skyline + `z` rule; v5 Liang–Barsky crop; v6/v7 apex moved, annotation pulled off the geometry; v8/v9 sub-tip cells merged, headline broken into four lines.
- No Juan feedback on any flavour.

## Keep — what works

### faithful v12
- The **softmax comb** at (0.61, 0.22) — one long bar, a second tier, a tail — is visibly peaked and the loudest mark, as the brief asks.
- **Row registration** is exact: each backward row sits on its forward twin's pitch; the mirror reads at a glance.
- Left-pointing filled arrowheads only in the backward register; open chevrons on the axis — the distinction holds.

### mechanism v15
- The **necked bundles** (K through (0.31, 0.30), the black throat at (0.64, 0.29)) make the constriction a shape, not a label.
- The **score lattice with the blue focus column** at u 0.51 reads as a real matrix of varying dots.
- `a = 0.5024` next to the longest blue bar ties the number to the mark; the three-line annotation (`softmax keeps the order and destroys the scale`) is the best caption in the family.

### abstract v9
- **The order is right and it performs the mechanism**: the pencil through the apex at (0.74, 0.78) literally computes the ratios; "the gradient is the same rays past the apex" is the strongest possible statement of weight reuse.
- **Hierarchy works**: the pencil + crimson skyline dominate at 3 m; the headline is the second read; the data block rewards 30 cm.
- **The apex left as an unpainted hole** and the rays cropping at the frame past it — chosen overlap, chosen crop.
- **Blue is scarce and loud**: one raked line across the whole sheet; the 4.5° rake of the image against the orthogonal type grid is the tension device.
- Forward skyline (jagged, vⱼ differ) vs backward flat-topped block (one number split by the same widths) — the asymmetry that matters, stated as form.

## Weak — what doesn't

### faithful v12
- [concept] It is the reference's flow diagram: labelled wells, labelled vertical stations, arrowheads, a forward/backward axis — a schematic by §6.
- [hierarchy] Six wells, two lattices, two combs, two arches at near-equal weight; the crimson arch at (0.81, 0.10) competes with the comb.
- [craft] Well textures differ (dots / dashes / dotted fans) but the Q blue teardrop and backward twins are small, busy and mechanical; the symmetric black almond lenses at (0.80, 0.33) and (0.80, 0.73) do no work (r01 NOTES agree); `s im ilar ity` letter-spacing is broken; travel 1.4× draw.
- [space] The fade-in wedges at u 0.21–0.32 are uncomposed dotted mush in both registers.

### mechanism v15
- [craft] **Backward arrowheads point right** (toward ∂L/∂Z) and the bottom axis arrows point outward — the gradient direction is visually reversed; a regression of the bug r01 fixed at v10.
- [space] The red/blue crossing at u 0.55–0.78, v 0.30–0.52 (and its backward twin at u 0.45–0.75, v 0.62–0.85) is dense crossing mud; the backward ∂L/∂V sheaf crosses ∂L/∂Z's fan in a broad X that carries little (r02 NOTES agree).
- [grid] Station labels at v 0.05 are spaced so wide (`s i m i l a r i t y`, `w e i g h t e d   v a l u e s`) that `softmax` and `weighted values` nearly run together; `backpropagate gradients` hangs off the right edge on its own.
- [concept] Still a two-register flow schematic with labelled stations; the maths is exact but the form is the reference's diagram. 4 244 pen-downs.
- [hierarchy] Q's butterfly well and V's laminae are mid-sized and equal; nothing on the left third dominates.

### abstract v9
- [grid] The **key field** at u 0.13–0.54, v 0.10–0.25 is a row of ring-on-stick marks — a picket fence and the most technical-drawing zone (r03 NOTES agree); the three tiny arrowheads on the left sticks are unexplained.
- [craft] Stray `H` glyph at the unit bar's right end (0.79, 0.64); the right end of the bar is a zig-zag of sub-2 mm cells cut by shallow rays — the one passage likely to plot muddy.
- [space] The upper-right of the q axis (u 0.55–0.95, v 0.05–0.22) is a defended void, not a composed one — nothing makes it read as intended.
- [hierarchy] The `z` rule crosses the crimson mass at a slight tilt and the `V`/`z`/`one` labels float around it without a shared baseline — the merge is the least legible stage.
- [concept] The brief's "three wells differ in kind" is answered (line / points / areas), but V has no origin on the sheet — it appears only as heights in the bar.

## Next versions
1. **vanishing-point-2** (abstract) — Keep r03's pencil, apex hole, raked q and the backward-past-the-apex idea; rebuild the key field as a genuine 2-D scatter on both sides of q (clustered, with the perpendicular drops of different lengths) so similarity reads as a plane collapsing onto a line; drive sⱼ and vⱼ from the real GPT-2 L1 H0 row 12 already solved in r02's `mechanism.py` (so a_max = 0.5024 and the skyline is real); make the backward block wider and let it crop at the sheet's lower edge. Strongest thesis: the order already performs softmax; it only needs real numbers and a key field that is composed.
2. **one-register** (mechanism) — Collapse r02 into a single register: forward strands drawn solid, the backward pass drawn as the same strands' second pass in a dashed/offset line with left-pointing arrowheads, so "the gradient reuses the same weights" is literally the same paths. Frees half the sheet for a dominant waist at 2× scale and removes the crossing mud of two registers.
3. **faithful-tuned** (faithful) — Keep r01's layout but cut the fade wedges, replace the almond lenses with ordered sheaves that keep their strand order into Z, subsample the backward lattice to ticks only, and let the crimson arch crop at the top frame so the plate gains one working diagonal.

**If only iterating:**
1. (mechanism) Flip every backward-register arrowhead and the bottom-axis heads so they point left/toward the centre as in faithful v12 — the gradient must run right-to-left.
2. (abstract) Replace the 12 ring-on-stick keys with a clustered 2-D scatter above AND below q, each key dropping a perpendicular of its true length onto q; delete the three stick arrowheads and the stray `H`.
3. (abstract) Feed r02's real row (a_max 0.5024) into r03 so the tallest crimson cell is visibly ~3× the next and the unit bar's widths are the GPT-2 weights.
