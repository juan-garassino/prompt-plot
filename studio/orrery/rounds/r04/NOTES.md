# orrery r04 — iterate (resonant-orbits: the miss takes space) · parent: r03 · 2026-09-29

## Render

```
.venv/bin/python scripts/render_candidate.py studio/orrery/rounds/r04/piece.py \
  --fn orrery_resonant_iterate --seed 7 --paper a4 \
  --palette dodgerblue,crimson,black \
  --out gallery/studio/orrery/current/pp_orrery_iterate_v11.png
.venv/bin/python studio/orrery/rounds/r04/checks.py gallery/studio/orrery/current/pp_orrery_iterate_v11.gcode
```

- final PNG: `gallery/studio/orrery/current/pp_orrery_iterate_v11.png`
- final GCODE: `gallery/studio/orrery/current/pp_orrery_iterate_v11.gcode`
- seed 7. The piece uses no randomness. The gcode bodies for seeds 3, 7 and 11 (`pp_orrery_iterate_v10_s{3,7,11}.gcode`) and v11 share md5 `7b23e6d4…`.
- trials v1–v10 are in `~/Downloads/pp_orrery_iterate_v*.png`. None was overwritten.
- `checks.py` in this round measures every acceptance number below on the emitted gcode.
- Render time is about 50 s, most of it spent planning the type walk (see Measurements).

## Arithmetic first (the budget, as the synth asked)

- **Proportional map.** δ_max/δ_min = g_max/g_min = 4.7097/1.5846 = 2.97, where g = s* − s = ln a* − ln a. A width proportional to δ can never reach 3:1, so the map is affine and anchored at `The`: s(δ) = S0 + C·(δ − δ_The).
- **Floor of a tight band.** Two strands of one key, radially s apart, with breathing amplitude A = 0.5 mm, lobe 7 mm (slope 24°) and phase slip 2πδ_The = 48.5°. The perpendicular gap is ≥ 0.8 mm everywhere only if s ≥ 0.8/cos 24° + 2A·sin(24.2°) = 0.88 + 0.41 = 1.29 mm. So S0 = 1.3 mm. The measured "parallel < 0.8 mm" share on `The` is 0.2 % at 1.3 mm and 23 % at 1.15 mm.
- **Radius needed vs available.** 13 bands at a 3:1 ratio need Σ widths ≈ 24 × W_min (W_min = the tightest band), plus 12 gaps.
  - 4 turns (W_min = 2A + 3·S0 ≈ 4.8 mm) → about 114 mm of bands.
  - 3 turns (≈ 3.6 mm) → about 86 mm.
  - 2 turns (≈ 2.3 mm) → about 55 mm.
  - An off-centre disc gives about 75–80 mm of radius and a centred A4 disc about 95 mm. Sun Ø18.8 plus a 5 mm clearing uses 15 mm of that, and the transformer moats use 8.4 mm.
- **It does not fit with 3 turns off-centre, so I used both of the synth's fallbacks plus one more step.** The disc is centred horizontally, with the asymmetry carried vertically (sun at v = 0.64, type block hanging low-right, question low-left). Each key orbits **2 turns**. Blue ink is 8.67 m against r03's 18.70 m (−54 %).
- **Divisor.** With 2 turns, turns·δ_max < 1 strictly holds with D = 2.5·g_max = 11.77. Then δ_max = 0.40, 2δ_max = 0.80, and every missing key's second turn also sits s ≥ 1.3 mm off its first. No miss can close. The caption prints what 11.77 is.

## Mandate responses

| id | mandate | status |
|---|---|---|
| S5 | closing orbit drawn whole, every orbit ≥ 95 % | **FIXED for the crop; ARGUED for the slot.** Nothing is cropped by the frame: all ink lies in x 13.7–196.3, y 14.0–282.9 on a 10–200 × 10–287 drawable. `transformer` is 100 % drawn outside the label slot (3 passes, 94.0 % of 360° each; the other 6.0 % is the slot). The slot is the only cut. Drawn fraction per orbit is 79–94.5 % (table below). ≥ 95 % including the slot is geometrically impossible with labels in the disc: a word with 2 mm halos needs at least 9 mm of chord, and ≤ 18° of loss at R = 16 mm allows only 5 mm. The slot is minimised instead: a vertical left chord, and a right chord that is the least-loss straight line clearing every token by 2.1 mm |
| A8 | the miss takes space: one declared affine map, ≥ 3:1, ≥ 2 gaps ≥ 4 mm, parallel < 0.8 ≤ 10 % | **FIXED (one part argued).** Band width s_j = 1.3 + 12.7·(δ_j − 0.135) mm, printed on the sheet. The widest/narrowest envelope on the 3 o'clock ray, measured on the gcode, is **3.23:1** (drew 4.80 / The 1.48); on s itself it is 3.6:1. Gaps ≥ 4 mm: 2 (4.2 mm either side of `transformer`). Parallel < 0.8 mm: **0.0 % on every band**. ARGUED: the full sweep envelope including the ±A breathing (2A + s) is 2.47:1. v3 used a 3.1:1 full-sweep ratio, which forced the seams between bands down to 2.0 mm, *narrower* than the tight bands' own 2.2–2.5 mm. The near-locks then did not read as cables at all, so I moved the paper into the seams (2.83 mm) |
| A10 | no in-layer travel > 60 mm in the emitted gcode | **FIXED.** Max hop: blue 5.8 mm, crimson 13.3 mm, black 37.2 mm, with 0 hops > 60 mm in every layer. Blue: every turn starts and ends on a chord and turns alternate direction, so the pipeline's nearest-neighbour pass walks the rings outside-in, in 27 strokes. Type: `plan_walk` replays the pipeline's own greedy rule (`nn_walk`, the same code as `postprocess.optimize_stroke_order`) and flips stroke directions until the pipeline's walk *is* the planned walk: caption bottom-up → title → token column up → `sink` → weights down. The emitted order equals the plan (verified). The first stroke of each layer is reached from the park position (139/139/177 mm). That is a layer approach, not an in-layer hop |
| A11 | zero blue within 2 mm of glyphs | **FIXED.** The minimum blue-to-glyph distance measured on the gcode is **2.10 mm** (over every black stroke and the crimson question) |
| A9 | sun ≥ Ø18 at ≥ 0.8 mm pitch; closing orbit 3 passes ≥ 0.3 mm; zero blue < 8 mm | **FIXED.** Sun: one spiral, Ø18.75 mm measured, pitch 0.85 mm. Closing orbit: 3 passes at offsets −0.35/0/+0.35 mm, captioned "weight, not data". Blue strokes < 8 mm: **0** (the shortest blue stroke is a full turn) |
| S4 | turns·δ_max < 1 strictly; constant explained; "only if" true | **FIXED.** 2 turns, D = 11.77 = 2.5 × 4.71 (drew), so 2δ_max = 0.80. Caption: "11.77 = 2.5 x the widest shortfall (drew, 4.71): after two turns the worst key is still 0.8 of a lobe out, so no miss can close." Only `transformer` has κ whole (κ = 69.000) |
| S6 | disclose rank 1 of 144 and the sink; reword the question | **FIXED.** Caption: "the strongest of 144 heads for itself > transformer (next .416, mean .053). 106 of 144 heads look hardest at The, the position-0 sink." `sink` is set above `The` at its row. The crimson question is now "where does this head look from itself?" (recomputed from `~/.promptplot/attn_gpt2.npz`: max 0.5572, next 0.4159, mean 0.0534, 106 argmax on key 0) |
| A12 | `canon:`, `flat:` declared, `lineage:` in HANDOFF | **FIXED** (see HANDOFF) |
| S8 | tokens verified, not inferred | **FIXED.** Tokens, ids and the row are read at render time from `rounds/r02/gpt2_head.npz`: ids `464 3112 7110 353 9859 257 2042 7604 981 262 47385 7342 2346`. The BPE split is ` plot`+`ter` (ids 7110, 353). The npz check_err is ≤ 2.34e-6, and the row matches `~/.promptplot/attn_gpt2.npz` to 1.0e-6 |
| S7 | no dossier/encoding: carry the check-number table | **FIXED in NOTES** (table below). There is still no `encoding.md`, which is the translator's job if routed |
| C1 | no pen cap; a pen per meaning | **ARGUED (unchanged).** 3 meanings, 3 pens: blue = keys, crimson = query, black = type. V and Z carry nothing in the score stage this thesis draws. r02 remains the flavour that carries all five |
| C2 | each pen one clean layer, stated order | **FIXED.** Layer order in the file is [0, 1, 2]: blue → crimson → black, light to dark, each pen entered once |
| C3 | spatially ordered within a layer | **FIXED** (merged into A10, above) |
| C4 | minutes per layer + total | **FIXED** (Plot budget) |
| C5 | dotted runs must earn their cycles | **FIXED.** Zero dotted runs. Pen cycles: 27 blue, 53 crimson, 1 084 black. Type is 93 % of all lifts, and most of it is the S4/S6 disclosure caption |
| C6 | lineage | **FIXED**: Whitney, *Permutations* (HANDOFF) |
| A1 | concept is an illustration | stays FIXED: every width, slip and closure is the real row |
| A2 | SOFTMAX caps / broken Q·Kᵀ | stays FIXED (no formula glyphs at the centre; the local `.`/`0` glyphs fix the "Ø58" read of the weights) |
| A3 | one ink weight | merged into A9/A12: the closing orbit is the one heavy line; flat is declared |
| A4 | V bundle | dropped (thesis) |
| A5 | letterbox bands | stays FIXED: the disc holds a 13.7 mm margin on the left, right and top, and the caption sits on the bottom margin |
| A6 / A7 | satellites / corner marks | dropped (thesis) |
| A13 | occluding Cellarius ellipse | dropped with r02's thesis |
| A14 | shape the lower-left quadrant | **DEFERRED, partly addressed.** The crimson question now hangs flush-right on the spine at the title baseline and closes the quadrant's top edge. The area x 13–100, y 14–60 is still a quiet field bounded by the disc arc, the question and the spine |
| S1 / S2 / S3 | r02 scale/epicycle/number mandates | dropped with r02's thesis. S3's principle (every printed number true) is checked below |

## What changed from parent

This is a composition move, not a parameter diff.

- **The disc is whole, centred and high.** r03 cropped the nest at the left edge, which broke the thesis (the closing orbit was an open C). Now the disc is inside a 13.7 mm frame on three sides, with the sun at (105, 191.5).
- **Tension moved off the crop** onto four things:
  - a slanted keyhole slot (vertical left chord, right chord leaning out to clear `transformer`);
  - the uneven band rhythm;
  - a long crimson plumb line that drops from the sun through the slot to a type block sitting on the bottom margin;
  - the question hanging left of that line, the title right of it.
- **Every key is a band whose width is its miss.** The four-strand ropes are gone. Each key is two turns: the second turn is laid s(δ) further out, and it also slips δ of a lobe. Near-locks (`The` 1.3 mm, `hole` 1.95, `watched` 1.96, `pen` 2.0, `the` 2.15) are tight pairs. Far misses (`drew` 4.7, `a` 4.5, `black` 3.9, `itself` 3.75) open into quiet rings with the token set inside them. Seams between keys are a constant 2.83 mm. The closing orbit sits in 4.2 mm of paper each side.
- **Labels live in a real slot.** Two chords, every turn ending exactly on them. There are no per-word knockouts and no crumbs. Tokens flush-left and weights flush-right of the spine, each row at its band's own radius (row pitch 4.5–7.4 mm), with `sink` above `The`.
- **Type:** proportional, ink-aligned stroke type (a local fix, see Engine requests). The title is sized so it runs exactly from the word column to the disc's right edge (x 106.8 → 196.3).
- **Data** is read from r02's npz. Nothing is hard-coded.

## Measurements / computations

Check numbers, measured on the v11 gcode by `checks.py`. The sun centre fitted from the crimson spiral is (105.22, 191.49).

| token | a | s*−s | δ | 2δ | n | s mm | env @3 o'clock mm | env 2A+s mm | drawn / turn % | parallel < 0.8 |
|---|---|---|---|---|---|---|---|---|---|---|
| The | .1142 | 1.585 | .1346 | .269 | 14 | 1.30 | 1.48 | 2.30 | 81.4 / 79.2 | 0.0 % |
| pen | .0583 | 2.258 | .1918 | .384 | 18 | 2.03 | 2.41 | 3.03 | 85.2 / 83.6 | 0.0 % |
| plot | .0313 | 2.881 | .2447 | .489 | 22 | 2.70 | 3.27 | 3.70 | 87.7 / 86.6 | 0.0 % |
| ter | .0139 | 3.689 | .3133 | .627 | 27 | 3.58 | 3.80 | 4.58 | 89.6 / 88.7 | 0.0 % |
| drew | .0050 | 4.710 | .4000 | .800 | 33 | 4.68 | 4.80 | 5.68 | 91.0 / 90.3 | 0.0 % |
| a | .0060 | 4.524 | .3843 | .769 | 39 | 4.48 | 4.42 | 5.48 | 92.0 / 91.5 | 0.0 % |
| black | .0105 | 3.969 | .3371 | .674 | 46 | 3.88 | 4.73 | 4.88 | 92.6 / 92.4 | 0.0 % |
| hole | .0625 | 2.188 | .1858 | .372 | 52 | 1.95 | 1.58 | 2.95 | 93.1 / 92.9 | 0.0 % |
| while | .0151 | 3.606 | .3062 | .612 | 56 | 3.49 | 2.71 | 4.49 | 93.4 / 93.3 | 0.0 % |
| the | .0522 | 2.368 | .2011 | .402 | 62 | 2.15 | 2.54 | 3.15 | 93.7 / 93.6 | 0.0 % |
| **transformer** | **.5572** | **0** | **0** | **0** | 69 | 0 (closes) | 0.78 (3 passes) | 1.70 | 94.0 ×3 (100 % outside slot) | n/a |
| watched | .0618 | 2.198 | .1867 | .373 | 74 | 1.96 | 2.30 | 2.96 | 94.3 / 94.2 | 0.0 % |
| itself | .0119 | 3.850 | .3270 | .654 | 78 | 3.75 | 4.58 | 4.75 | 94.5 / 94.4 | 0.0 % |

Column notes:
- Row sum = 1.000; masked keys 13–14 = 0.
- "drawn / turn" is angle drawn / 360° per turn stroke, and the slot is the only loss.
- "parallel < 0.8": share of 0.15 mm samples within 0.8 mm of the key's other turn with tangents within 25° (r03's definition).
- Envelope ratio on the 3 o'clock ray: 3.23:1. On s: 4.68/1.30 = 3.6:1. Full sweep 2A+s: 2.47:1 (argued above).

Layout constants:
- Amplitude A = 0.5 mm, constant and carrying no data.
- Lobe 7 mm (n_j = round(2πR_j/7), layout).
- R_in = 15 mm; the sun is a single spiral r 9.8 mm, pitch 0.85 mm.
- Seams: the gap between band envelopes is solved so that the outer envelope lands at R = 91.3 mm. That gives a 1.83 mm envelope gap, a 2.83 mm strand-to-strand seam and a 4.2 mm moat.
- Label type: tokens 2.2 mm, weights 1.8 mm, `sink` 1.6 mm, caption 1.9 mm. All proportional, with ink-aligned glyphs.
- Halo 2.1 mm, measured 2.10.

Type walk:
- `plan_walk` is a planner that mirrors the pipeline's greedy rule.
- The piece tries caption leadings {4.2, 4.4, 4.6, 4.8} × measures {80, 84, 88} mm and keeps the layout whose *emitted* walk has the shortest longest hop: 37.2 mm, at leading 4.2 and measure 84 (10 lines).
- Before it, the same type block gave hops of 74–134 mm (v1–v6: stragglers collected after the column).

Data provenance: see S8 above.

## Plot budget

Leo model (as in r03): F500 draw, F1800 travel, 1 s dwell per pen drop and per pen lift. The emitted gcode carries 0.2 s dwells; that figure is in brackets.

| order | pen | meaning | strokes | draw | travel (in-layer + approach) | longest in-layer hop | minutes |
|---|---|---|---|---|---|---|---|
| 1 | 0 dodgerblue | keys: 12 bands × 2 turns + the closing orbit × 3 passes | 27 | 8.67 m | 0.22 m | 5.8 mm | 18.4 (17.6) |
| 2 | 1 crimson | the query: question → spine → sun spiral | 53 | 0.66 m | 0.24 m | 13.3 mm | 3.2 (1.8) |
| 3 | 2 black | type: caption, title, tokens, sink, weights | 1 084 | 3.04 m | 2.39 m | 37.2 mm | 43.5 (14.6) |
| total | 3 pens / 2 swaps | | 1 164 | 12.37 m | 3.03 m incl. home | | **≈ 65 min** (≈ 34 min at the emitted dwells) |

- Commands: 24 557.
- Blue is 27 strokes of 81–563 mm each, so any stroke boundary is a safe batch point. The whole layer is one batch at `batch_strokes: 400`, and black is three batches.
- Black time is lift-dominated (1 084 × 2 s). The disclosure caption S4/S6 asked for is about 70 % of those strokes.

## Self-critique (seven dimensions)

1. **Hierarchy 8.** The disc dominates. The heavy closing orbit reads second. The crimson sun and plumb line are third, then the title.
2. **Grid 8.**
   - One vertical (x = 105) carries the sun, the spine, the slot, the question's right edge (flush-right at 103.2) and the word column (flush-left at 106.8).
   - The title spans exactly word column → disc edge.
   - The disc keeps a 13.7 mm margin on three sides, and the caption sits on the bottom margin.
3. **Tension 6.** The disc is centred, which is the cost of fitting it whole. Asymmetry comes from:
   - the leaning slot chord;
   - the long crimson drop to a low type block;
   - question left vs title+caption right;
   - the uneven band rhythm.

   It holds, but it is calmer than r03's crop.
4. **Negative space 7.** The inner clearing around the sun, the moat around the closing orbit and the quiet rings inside the far-miss bands are all data-driven paper. The band between the disc bottom and the title (y 70–100), crossed only by the plumb line, is shaped. The lower-left field is still large.
5. **Craft 8.**
   - 0 % sub-floor parallels, no floods.
   - Sun at 0.85 mm pitch; closing orbit 3 passes 0.35 mm apart.
   - 0 blue crumbs, 2.1 mm halos, max in-layer hop 37 mm, 3 clean layers.
   - One weakness: 1 084 black lifts.
6. **Concept 7.** One closed bold line among open pairs, the answer set in its own moat, and near-locks pairing tight while far misses open. At 1 m the pairing reads, helped by each token sitting inside its own band at the slot. At 3 m the disc reads mostly as uneven concentric rings: the miss is visible as rhythm, not yet as obviously different "cables vs annuli".
7. **Depth 5, declared flat.** Focus is the only depth cue: the sharp heavy ring against the paired hairlines.

**The single worst thing:** the band structure is only moderately legible at 3 m. With two strands per key, a far-miss annulus (4.7 mm inside) sits next to 2.8 mm seams, so part of the eye still pairs strands *across* keys. The radius budget does not allow seams wider than the widest band (tested: A = 0.8 mm leaves 0.2 mm envelope gaps). Second-worst: the inner rings lose 19–21 % to the label slot.

## Engine requests

- `_stroke_text(..., proportional=True)` / `_text_width(..., proportional=True)` / `kit.giant_type(proportional=True)` advance by ink width but place each glyph at its cell origin, never shifting by the glyph's own ink minimum. So a centred glyph overlaps its neighbour: `itself` plots as "tself", `while` as "wh le". This piece carries a local `ptext` that left-aligns each glyph's ink.
- The font's `0` carries a slash (a weights column reads "Ø58"), its `.` is a 0.19 mm speck at 1.8 mm type, and there is still no `?`. All three are local overrides here.
- `postprocess.optimize_stroke_order` is greedy nearest-start, starts every colour at (0, 0), and never reverses a stroke. On type it leaves stragglers and crosses the sheet to collect them. This piece works around it with `plan_walk`, which chooses stroke directions so the greedy walk reproduces a planned one. A per-layer `preserve_order` flag, or a 2-opt pass that may reverse strokes, would make that unnecessary for every piece.
