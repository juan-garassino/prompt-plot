# orrery r03 — resonant-orbits (abstract) · parent: r01 · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/orrery/rounds/r03/piece.py \
  --fn orrery_resonant_orbits --seed 7 --paper a4 \
  --palette dodgerblue,crimson,black \
  --out gallery/studio/orrery/current/pp_orrery_resonant-orbits_v14.png
```

- final PNG: `gallery/studio/orrery/current/pp_orrery_resonant-orbits_v14.png`
- final GCODE: `gallery/studio/orrery/current/pp_orrery_resonant-orbits_v14.gcode`
- seed: 7. The piece uses no randomness: seeds 3, 7 and 11 give byte-identical G-code (re-checked on v14).
- trials v1–v13 are in `~/Downloads/pp_orrery_resonant-orbits_v*.png` (none overwritten).

## Lineage

**John Whitney Sr., *Permutations* (1968)**, early computer art made on an IBM 360 and an optical printer. The order it lends is *differential dynamics*: every element turns at its own rate, a figure appears only where those rates stand in whole-number ratio, and between those moments the figure dissolves into texture. Here the ratios are set by one attention row. The plate borrows Whitney's rule, not his look (dots on film).

Canon: RADIAL DATA-VIZ (concentric tracks, one series per ring, a typographic scale on the spine). It is flat by declaration. Depth is carried only by focus: the locked orbit is sharp and heavy, and the unlocked ones are ropes (see Self-critique).

The twist: the plate is a riddle. The crimson line asks *what does itself refer to?*, and the sheet answers it without words. Exactly one orbit closes, and it is `transformer`.

## Mandate responses

There is no `LEDGER.md` and no `FEEDBACK.md` for this slug, so there are no J/A/S rows. The binding brief is the DESCRIPTION's **resonant-orbits** paragraph plus the curator note. Its Weak items are answered below.

| id | mandate | status |
|---|---|---|
| brief | Q and K as orbiting bodies, period ratio = the dot product, a trace that closes on resonance or fills an annulus, ORBITAL order, one continuous line | **FIXED**. Each key is one continuous orbit about the query whose radial:orbital frequency ratio κ = n + δ, with δ the key's dot-product shortfall. δ = 0 closes (Bertrand), and δ > 0 precesses across its annulus. Every key is one unbroken trace per turn; it is cut only where it crosses the type spine and the left sheet edge. |
| C1 curator | no pen cap; keep every colour that carries a meaning (Q, K, V, Z, structure) | **ARGUED**. This thesis draws the score stage only (q·k → softmax), so it has three meanings and three pens: K blue, Q crimson, structure/type black. V and Z carry nothing here. Adding them would bring back the Q→K→V→Z flow diagram that this abstract thesis exists to remove (DESCRIPTION Weak: "illustration"). If Juan wants Z, the honest route is a sibling where Z is the attention-weighted superposition of the orbits. |
| C2 curator | each pen one clean colour layer, stated order and meaning | **FIXED**. Order is blue (keys) → crimson (query) → black (type): light to dark, so the black type lands last and sits on top. Each pen appears as exactly one layer (verified by the per-colour parse of the gcode). |
| C3 curator | strokes spatially ordered within a layer, batchable | **FIXED, with one engine caveat**. Blue: 117 strokes, the longest 462 mm (~55 s at F500), so any stroke boundary is a safe batch point. Every stroke is one orbit turn (or half a turn where the left crop cuts it). The pipeline's per-colour nearest-neighbour reorder overrides the authored order and leaves 6 hops over 150 mm (max 164 mm). The median hop is 20.5 mm. See Engine requests. |
| C4 curator | minutes per layer + total | **FIXED**. See Plot budget: ~70 min. |
| C5 curator | parent ran 1887 pen cycles, 97 % travel, mostly dots; dotted runs must earn their cycles | **FIXED**. There are zero dotted runs. Pen cycles fell from 1 887 to 722 (117 blue, 36 crimson, 569 black), and 79 % of those are type glyphs. Travel fell from 7.4 m to 6.6 m, against 21.1 m of draw (draw/travel 3.1, versus ~1.0 in the parent). |
| C6 curator | name the LINEAGE | **FIXED**: Whitney, *Permutations* (above, and in HANDOFF). |
| W1 concept | illustration; no quantity sets any radius/orbit | **FIXED**. Every orbit's precession is a real GPT-2 number, and nothing is depicted: no orrery, no stars, no moons. Ring radius is declared layout (token position). |
| W2 craft | monoline caps SOFTMAX, broken `Q · Kᵀ` | **FIXED by removal**. No formula type sits at the centre. The sun is a solid crimson disc. The law is in the footer as plain lowercase (`kappa = n + (s* - s) / 18.84`). |
| W3 depth | one ink weight; the sun is 17 equal rings | **FIXED**. Two physical weights now come from the mechanism itself: the locked orbit is 4 passes 0.25 mm apart (~1.1 mm band), and the unlocked orbits are 4 hairline strands. |
| W4 craft | straight V bundle; `V` label grazing its orbit | **N/A**. There is no V bundle. Every label sits in a measured halo on the spine, and orbits stop 1.2 mm clear of the type. |
| W5 space | letterbox bands top/bottom, enclosing circle short of the sheet | **FIXED**. The nest is cropped hard at the left edge (the outer seven rings, `transformer` included, run off the sheet), ~7 mm from the top margin. The lower-left 55 × 55 mm is a deliberate quiet zone, and the type block fills the lower right. |
| W6 hierarchy | satellites all similar size | **FIXED**. There is one mass (the nest, 167 mm across) and one loud line inside it (the locked orbit). The crimson sun and spine come third, and the type fourth. |
| W7 grid | corner marks align with nothing | **FIXED**. All furniture is deleted. One vertical axis, x = 70 mm (the conjunction ray), carries the sun, the spine, the 13 token labels (flush-left at +2.4), the 13 weights (flush-right at −2.4), the title, the question and the caption. |

## What changed from parent

This is a new composition, not an edit. r01 recreated an engraved orrery (four satellite systems, bundles, stars and moons around a centred sun) with nothing computed. r03 keeps only the parent's best idea, **one dominant central system**, and makes it the entire plate:

- The four satellites, the bundles, the dotted enclosing orbit, the moons, the stars and the corner marks are all deleted.
- The query is the sun. The 13 keys the query can see (causal) are 13 concentric orbits around it, the first token innermost like growth rings.
- Each orbit is drawn for the same four turns. If the key resonates, the four turns land on one path, the heaviest line on the sheet. If not, they precess into a four-strand rope whose twist is the dot-product shortfall.
- The sentence runs down the 6 o'clock ray (where every orbit starts, in conjunction), read top to bottom: *The pen plot ter drew a black hole while the transformer watched itself*. The softmax weight of each token is set on the other side of the crimson spine.
- The sun sits off-centre (u 0.33) and the nest is cropped at the left sheet edge. The type block hangs off the spine into the lower right.

Composition moves made inside the round: v1 had looped epicycles (coil springs, knotted). In v2–v3 the rings were ordered by distance back in the sentence, which put the locked ring small and near the sun. v3→v5 switched to token order, which puts the locked ring near the rim, sweeping. v5 moved from a centred to a cropped layout. v6 added the weight column on the spine. v9 replaced the epicycle with the Bertrand rosette orbit (see below). v10–v14 were amplitude, type block and caption.

## Measurements / computations

**Data.** `~/.promptplot/attn_gpt2.npz`, `attn[4, 3, 12, :13]` (GPT-2 small, layer 4, head 3, query position 12). The row is hard-coded in the piece and `check_against_npz()` returns True (allclose, rtol 1e-4). Row sum = 1.0000003. Masked positions 13–14 are 0.

The sentence is the extractor's default, *"The pen plotter drew a black hole while the transformer watched itself think."* The npz stores no token strings and no tokenizer is installed, so the tokenisation is reconstructed: 15 tokens, with `plotter` → `plot|ter`. The count is verified, because layer 4 head 11 (GPT-2's known previous-token head) puts mean weight 0.999 on position i−1 across all 15 positions. The boundaries are inferred, not verified.

Why this head: across all 144 heads, L4H3 gives `itself → transformer` the largest weight (0.557). It is the argmax of the row, and it is coreference. Perplexity of the row: 5.09.

**Law.** s* − s_j = ln a* − ln a_j (exact, since softmax is shift-invariant). δ_j = (s* − s_j) / (4 · 4.7097) = (s* − s_j) / 18.84. κ_j = n_j + δ_j, and r_j(θ) = R_j + A cos(κ_j(θ − θ0)) over θ ∈ [θ0, θ0 + 8π]. Layout: R_j = 15 + 7.5·j mm, A = 2.6 mm, n_j = round(2πR_j / 16 mm), centre (70, 172), θ0 = −90°.

| token | a | s*−s | δ | n | lobe mm | slip/turn mm | parallel <0.8 mm | ink-on-ink @0.35 mm |
|---|---|---|---|---|---|---|---|---|
| The | .1142 | 1.585 | .0841 | 6 | 15.7 | 1.32 | 55.4 % | 8.8 % |
| pen | .0583 | 2.258 | .1199 | 9 | 15.7 | 1.88 | 17.9 % | 7.2 % |
| plot | .0313 | 2.881 | .1529 | 12 | 15.7 | 2.40 | 0.6 % | 6.7 % |
| ter | .0139 | 3.689 | .1958 | 15 | 15.7 | 3.08 | 0.5 % | 6.1 % |
| drew | .0050 | 4.710 | .2500 | 18 | 15.7 | 3.93 | 0.5 % | 6.0 % |
| a | .0060 | 4.524 | .2402 | 21 | 15.7 | 3.77 | 0.4 % | 6.0 % |
| black | .0105 | 3.969 | .2107 | 24 | 15.7 | 3.31 | 0.3 % | 6.1 % |
| hole | .0625 | 2.188 | .1161 | 27 | 15.7 | 1.82 | 24.5 % | 7.4 % |
| while | .0151 | 3.606 | .1914 | 29 | 16.3 | 3.11 | 0.2 % | 6.1 % |
| the | .0522 | 2.368 | .1257 | 32 | 16.2 | 2.04 | 3.6 % | 7.0 % |
| **transformer** | **.5572** | **0** | **0** | 35 | 16.2 | **closes** | n/a (4 passes, 0.25 mm) | n/a |
| watched | .0618 | 2.198 | .1167 | 38 | 16.1 | 1.88 | 23.8 % | 7.6 % |
| itself | .0119 | 3.850 | .2044 | 41 | 16.1 | 3.29 | 0.2 % | 6.1 % |

Column definitions:
- "parallel <0.8 mm" is the share of sample points (0.15 mm resample) lying within 0.8 mm of a point on a *different turn* whose tangent is within 25°.
- "ink-on-ink" rasterises a 60° window of every turn at a 0.35 mm pen and reports the share of inked area inked by 2 or more turns: the physical flood measure.

Geometry iterations measured on the way:
- The epicycle trace of v6 (ratio 0.87, flat outer arches) scored 40–84 % "parallel <0.8" on every ring.
- The Bertrand rosette fixed the eight rings that slip ≥ 2 mm (≤ 3.6 %).
- Raising A from 2.2 to 2.6 cut The from 71.9 % to 55.4 % and pen from 38.5 % to 17.9 %.

Label halos: box = text width at 2.6 mm (weights at 2.0 mm) + 1.2 mm pad; spine corridor ±1.1 mm; knocked crumbs shorter than 4 mm are dropped (v6 left 1–3 mm cusp tips at halo edges).

`promptplot preview --score` (v13, same geometry): grade A, composition 0.927, readability 0.978, draw/travel 3.11.

## Plot budget

Leo time model: F500 draw, F1800 pen-up travel, 1 s dwell after every M3 and M5.

| layer | pen | meaning | strokes | draw | travel | longest stroke | minutes |
|---|---|---|---|---|---|---|---|
| 1st | 0 dodgerblue | keys (13 orbits) | 117 | 18.70 m | 4.16 m | 462 mm | 43.6 |
| 2nd | 1 crimson | query (sun spiral, spine, question) | 36 | 0.40 m | 0.52 m | 173 mm | 2.3 |
| 3rd | 2 black | type | 569 | 1.97 m | 1.86 m | 21 mm | 23.9 |
| total | 3 pens / 3 swaps | | 722 | 21.07 m | 6.63 m (incl. home) | | **~70 min** |

Commands: 30 333. Bounds clean (no clamp violations on v14). With `batch_strokes: 400`, blue is one batch, crimson one, and black two.

## Self-critique (seven dimensions, honest)

1. **Hierarchy 8**: the nest dominates at 3 m. The locked orbit is the only heavy line on the sheet and reads second. The sun and spine come third.
2. **Grid & alignment 8**: one axis carries everything, and weights and tokens are mirrored about the spine. The ragged right edge of the label halos (each ring resumes after its own word) is a little uneven.
3. **Tension & asymmetry 7**: off-centre sun, hard left crop, type hanging bottom-right. The nest itself is still a set of concentric circles.
4. **Negative space 7**: the lower-left quiet zone and the top-right corner are shaped by the circle. The 22 mm strip right of the nest is residue, not a decision.
5. **Craft for pen 7**: no floods (ink-on-ink 6–9 %, all at crossings) and no dots. The locked ring's four passes are deliberately 0.25 mm apart, as a weight band. The four near-locked ropes (`The`, `pen`, `hole`, `watched`) run strands closer than 0.8 mm near their crests (18–55 % of samples). They cross rather than stack, but they are under the house floor.
6. **Concept legibility 8**: one clean line among ropes; the question, the column and `.557` confirm it. It is exact, and no object is depicted.
7. **Depth 6**: declared flat. The only depth cue is focus (sharp and heavy against twisted and fine), plus the ropes' helical twist, which reads faintly as 3D.

**The single worst thing:** at 3 m the twelve unlocked orbits read as one even rope texture. The per-key shortfall (δ from 0.084 to 0.25) is legible only at reading distance, so the plate says "one locks, the rest don't" much louder than "and here is by how much". The second-worst is the near-locked ropes crowding under 0.8 mm at their crests, especially `The` (the attention sink, the innermost ring).

## Engine requests

- `postprocess.reorder_by_color` → `optimize_stroke_order` is greedy nearest-neighbour with no improvement pass. On this plate it leaves 6 blue hops over 150 mm (max 164 mm) that the authored ring-by-ring order did not have. Wanted: either a 2-opt pass after NN, or a per-layer `preserve_order` flag for pieces that author their own spatial order.
- The stroke font has no `?` or `;`. The piece draws a local `?` (a hook and a dot on the 4 × 6 grid) and avoids `;`. Both belong in `_GLYPHS`.
- `kit.giant_type` and `fat_outline` take `tip` as the pass spacing. A `weight` band at the default `tip=0.55` comes out as hollow outline letters on a 0.3 mm pen. A pen-aware default (≈0.8 × the nib) would stop that.
