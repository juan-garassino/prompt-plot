# resonance-ffn r04 — iterate · parent: r01 (v9) · 2026-09-29

**Lineage.** Charles Csuri & James Shaffer, *Sine Curve Man* (1967, IBM 7094 and drum
plotter). The ORDER it lends is a form and its function-mapped copy on one plotter sheet. Here
that is the forward FFN row with its transposed, reversed backward row, and the hero field with
its 0.39-scale ∂L/∂A copy. **Depth: flat. This is a reproduction of a flat plate diagram.**

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance-ffn/rounds/r04/piece.py \
  --fn attention_as_resonance_ffn_iterate --seed 7 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,darkviolet,black \
  --out gallery/studio/resonance_ffn/current/pp_resonance_ffn_iterate_v5.png
```

- Final files: `gallery/studio/resonance_ffn/current/pp_resonance_ffn_iterate_v5.png` and `.gcode`. Seed **7** is r01's seed, so the 60 + 46 random scatter positions are r01's.
- The v5 G-code body is byte-identical to v4. v5 only re-renders after two non-geometric edits: a docstring change and a removed debug line.
- Self-rounds: v1 (IR and dots), v2 (phase-locking, arrow fill, bracket, prime), v3 (textures kept, polish), v4 (orders on 0.01 mm coordinates, so the file order equals the computed order).
- Seeds 3 and 11 were built too. The seed only moves 60 hero and 46 twin scatter dots. Seed 11 streams worse (a 159 mm black hop) and seed 3 is equivalent. **Seed 7 is kept, because J2 keeps r01's scatter positions.**
- Plate job rehearsal (`promptplot plot plate … --layers 2,1,3,0,4,5 --paper a4:portrait --margin 10 --dry-run`) on the identical v4 body:

```
  layer 1: colour 2  720 strokes  ~28 min
  layer 2: colour 1  1058 strokes  ~41 min
  layer 3: colour 3  201 strokes  ~9 min
  layer 4: colour 0  1082 strokes  ~42 min
  layer 5: colour 4  268 strokes  ~12 min
  layer 6: colour 5  1422 strokes  ~60 min
  bounds ok · batches of 400 · re-zero every 2000 · feed ≤ 500 · dwell ≥ 1s · ETA ~201 min
dry-run: 91045 commands, 67215 inked segments, waits: swap, swap, swap, swap, swap, swap → done
```

**`--margin 10` is required.** The plate is drawn on the render's 10 mm margin (ink bbox x 15.4–196.5, y 15.6–280.4), and `plot plate` defaults to 15 mm, which would refuse layers at x > 195.

## Mandate responses

| id | mandate | status |
|---|---|---|
| J1 | Continuous round dots at a 0.9–1.1 mm pitch, end-anchored, never micro-dashes; converging paths kept apart | **FIXED.** One family dot is used on every dotted LINE: a closed loop with r = 0.15 mm (inks ≈ 0.65 mm under a 0.35 nib) at a 1.0 mm pitch, end-anchored (n = round(L/1.0), n + 1 dots). Across all 241 trains, consecutive surviving dots have a median of **0.998 mm**, p5 0.90 and p95 1.02. The isolated ∂L/∂Y drop curve has a median of **1.019 mm**. **0** non-type open strokes of 0.3–1.2 mm. Every mark that was a dot is a loop (4,032 closed loops). Where a train ends on a node disc, its end dot is removed by the node keep-out, so the last visible dot sits ≥ 0.55 mm from the node edge and the node is the end mark. That covers both ends of the ∂L/∂Y drop curve (Y circle → end disc). |
| J2 | Keep the original: every element at r01's position | **KEPT.** Section by section, this is r01 transcribed with its reference-pixel coordinates, packet tables, crest maths (d = 35·L and d = 14·L), FFN fan and rng call order unchanged. Present on the sheet: 5 + 5 Q/K rows, 20 fans, 12 Q/K verticals, `Q·Kᵀ/√d_k`, the hero, 12 halo arcs, 214/215 scatter dots, 232/264 stipple marks, softmax with 6 peaks, 3 ghosts and 11 base marks, 5 V rows, 6 + 5 ochre falls, Z = AV, the bracket, expand / nonlinearity / project, Y and its continuation, ∂L/∂Q ×2, ∂L/∂K ×2, ∂L/∂V, 5 return fans, the ∂L/∂A twin, ∂L/∂Z, projectᵀ / nonlinearity′ / expandᵀ, ∂L/∂Y, 6 arrowheads, both drop curves, and the title with rule and dot. Moves ≤ 1 mm, except the A5 bracket legs, `FFN` (+2 mm) and `∂L/∂A` (−0.8 mm). |
| A1 | Plot discipline: 6 clean layers, contiguous batches, no hop > 80 mm, no invisible cycles, fused type, plus budget, batches, session and dry-run | **FIXED except 4 hops, ARGUED below.** 6 layers, each entered once, streamed light→dark with `--layers 2,1,3,0,4,5`. The file order is proven equal to the computed order, stroke for stroke on all 6 pens. Travel is **9.49 m for 14.26 m of draw (67 %)**, against a limit of draw + dots × 1 mm = 18.37 m. Parent: 11.53 m, 96 % on the same model. **0** family dots within 0.30 mm of same-pen ink, **0** in label boxes, **0** co-incident (< 0.6 mm), **0** on nodes. Type weight passes, arrowheads and discs are each one pen-down. **Hops > 80 mm:** crimson 141 and blue 173 are forced, because each pen has two ink regions (the Q/K block with fans vs the ∂L stack at the foot) and the closest points of those regions are 131 / 141 mm apart. Black 93 is the backward row → softmax. Black 90 is hero → title. `_polish` removed a 134 mm and a 94 mm black straggler and a 93 mm ochre one, but these two survived 150 flip trials. Budget, batch table and session plan are below. |
| A2 | Lineage + declared depth | **FIXED.** Csuri & Shaffer, *Sine Curve Man* (1967); flat. Restated in the HANDOFF. |
| A3 | Converging dotted paths never interleave | **FIXED on most of the sheet, PARTIAL in the funnel.** `_lay_trains` phase-locks each dotted line to any earlier same-pen line running within 2 mm and within 37° of parallel, placing its dots at the projections of that line's dots. A line that closes to < 0.9 mm at one of its ends stops early on a dot: 82 mm were trimmed over the whole sheet, and **no path was deleted**. Result: of the dots that run beside a parallel same-pen train within 2 mm, **461 sit side by side** and **166 are still offset by 0.25–0.75 mm** (114 in the Q/K funnel, 39 in the ochre falls, 13 in the backward row). Those 166 are where three trains cross at shallow angles and one line cannot lock to two neighbours. |
| A4 | (a) halo chords/stub (b) stipple flood (c) `-` ticks | **FIXED.** (a) Each halo ellipse is cut into its real arcs: the keep-out edge is found by 30-step bisection, so every arc stops ON the curve, and the arc through the parameter seam is joined across it. No chord at y ≈ 191/140 and no stub at x ≈ 150 (hero crop checked at 8 px/mm). r01's envelope outlines had the same filtered-and-joined chord bug and are cut into runs as well. (b) The stipple caps keep r01's 264 dash positions, one dot each, never re-pitched, and show no flood in a 24 px/mm crop. 22 stipple dots were removed where the lower cap ran into `softmax` (16) and under ∂L/∂A (6); 11 others landed < 0.35 mm on another texture mark. (c) 0 ticks: `_fdot` is a loop for r ≤ 0.32 and r01's spiral disc above that. |
| A5 | Bracket legs, `FFN` lift, prime, ∂L/∂A air | **FIXED.** The legs are aimed at the pinch nodes N0 (722, 1129) and N3 (1000, 1129) and stop 2.2 mm below the bar. The right leg no longer lands on project's crest, and it clears the N3 dotted column by 1.6 mm. `FFN` is lifted 2 mm: glyph bottom 76.61 mm vs bar 74.21 mm. The prime is a raised stroke 0.50 mm after the `y` ink, from cap height down to 0.68 cap. ∂L/∂A has **1.54 mm** of clear air (edge to edge, measured against all black ink): the label moved down 0.8 mm and its halo is 1.5 mm. |
| A6 | Packet overlaps / V knot | **DEFERRED — blocked by J2** (Juan to rule). |
| A7 | ≥ 8 mm lower-third gap | **DEFERRED — blocked by J2.** |
| A8 | Schematic / symmetric / no dominant | dropped (r03), superseded by J2. |
| A9 | Six pens | dropped (r03). Six meanings kept. |
| A10 | v5 condensed type | closed (r03). v9's lowercase and tracking are kept exactly. For the critic: `nonlinearity` at 12 px cap is 2.03 mm tall and still reads `l`/`i` loosely at 0.35 nib, the same as v9. |
| S0 | No dossier/encoding | **DEFERRED:** curator/expert. |
| S1 | Twin is a scaled copy; no channel carries ∂L/∂A | **DEFERRED — blocked by J2.** |
| S2 | tanh dome vs GELU | **DEFERRED — blocked by J2.** |
| S3 | n_K = n_V = n_softmax (5/5/6) | **DEFERRED — blocked by J2.** |
| S4 | Same streamline count forward and backward | **CHECKED, equal.** The forward dome has **10** streamlines (5 per side) and the backward twin peaks have **10** (5 per side), counted in `FAN_STATS` at emission. None is missing and none was removed. |
| S5 | Handoff must not claim feeds the file lacks | **FIXED.** The file carries F1200–2600 and `G4 P0.2` (post-processor dwells). All timings here are the **clamped `plot plate` model**: F500 draw, 2000 mm/min travel, dwells floored to 1.0 s (2 s per pen cycle), 90 s per swap, 20 s per re-zero. |

## What changed from parent

Not a composition move. J2 forbids one, and the sheet is v9's. What changed is the mark and the stream.

1. **Stroke IR.** r01 wrote G-code as it drew. Here every section appends `Mark`s to a `Sheet`, and six passes run before emission: `_lay_trains`, `_dedupe_axes`, `_clean_dots`, rounding, `_order` and `_polish`.
2. **The dot.** r01 drew 0.42–0.85 mm micro-dashes on a 1.9–2.2 mm period. Now there is one round dot at a 1.0 mm pitch on every dotted line, including the wave-packet envelope outlines. Those were 0.85 mm dashes, and the synth's "0 micro-dashes 0.3–1.2 mm anywhere" test covers them. The only real dash left is r01's 2.6 mm axis into the ∂L/∂A figure. The `· · · ·` continuations are now family-dotted spans over r01's extent.
3. **Textures** (hero and twin crest fade = stipple caps, and the scatter) keep r01's marks: one dot at each r01 dash centre, and scatter at r01's radius and position.
4. **Carrier is the axis.** The straight row axis is removed only where the packet's envelope is < 0.15 mm, which is where the carrier already lies on it. The carrier is extended to the row's end nodes. The axis still crosses every packet.
5. **Arrowheads are solid.** r01's fill used `frac = 1 − |y|/hb`, which gave a zero-length centre line and hollow heads. It is now `|y|/hb`, so each head is filled base to edge as r01's docstring intended, in one pen-down.
6. **A5 collisions** (above).

## Measurements / computations

- **Dot laying:** 241 dotted trains, 749 phase-locked dot positions, 82.1 mm trimmed at converging ends.
- **Dots removed by the invisibility pass:** 75 in label halos, 447 on nodes, 739 within 0.30 mm of same-pen ink (crossings and envelope-on-crest), 330 co-incident. Each of these sat on ink or on another dot, so none could be seen.
- **Textures:** stipple 264 → 232 (−22 under labels, −11 co-incident; 88 %). Scatter 215 → 214 (99.5 %).
  - The ±5 % target is met for scatter. It is missed for stipple only by the label halos that A5 asks for.
  - Stipple and scatter dots on a crest line are **kept**. A 0.65 mm dot on a 0.35 mm line reads as a bead, as in the reference, so they are not "invisible".
- **Ordering proof:** `_greedy_by_start` reimplements `postprocess.optimize_stroke_order`. Parsing the rendered G-code and comparing per-colour stroke starts with the built order gives **first divergence: none**, on all 6 pens (1082 / 1058 / 720 / 201 / 268 / 1422 strokes). Before rounding to the file's 0.01 mm, black diverged at a near-tie. `_polish` used 1 flip on ochre and 11 on black.
- **Clearances:** ∂L/∂A 1.54 mm clear. `FFN` 2.05 mm clear of the bar. Right bracket leg to the N3 column top 1.6 mm.
- **Parent on the same model** (`current/pp_res_ffn_v5.gcode` = v9 output): 3,725 cycles, 12.07 m draw, 11.53 m in-layer travel (96 %), 164 min. Its hops were crimson 140, blue 173, gold 98 and black 91.

## Plot budget

Clamped `plot plate` model (F500 draw, 2000 mm/min travel, dwell ≥ 1 s ⇒ 2 s per cycle, 90 s per swap, 20 s per re-zero). Stream order is **light → dark: `--layers 2,1,3,0,4,5`**. Gold, blue, green and crimson go down first. Violet and black land last on dry lighter ink, where they cross it: the black droplines through ochre falls, the bracket over violet, the stage columns over the violet spine.

| # | pen | meaning | cycles | dots* | draw m | travel m | longest in-layer hop | min |
|---|---|---|---|---|---|---|---|---|
| 1 | 2 goldenrod | V rows, softmax→V feeds, V→Z bundle, ∂L/∂V | 720 | 680 | 1.89 | 1.34 | 61 | 28.5 |
| 2 | 1 dodgerblue | K rows + fans, ∂L/∂K ×2 | 1058 | 1004 | 2.35 | 1.88 | 173 (region change) | 40.9 |
| 3 | 3 forestgreen | Z = AV, ∂L/∂Z, drop curve | 201 | 169 | 0.99 | 0.47 | 37 | 8.9 |
| 4 | 0 crimson | Q rows + fans, ∂L/∂Q ×2 | 1082 | 1031 | 2.32 | 1.93 | 141 (region change) | 41.7 |
| 5 | 4 darkviolet | FFN stages, fans, Y, ∂L/∂Y | 268 | 216 | 1.21 | 0.61 | 37 | 11.7 |
| 6 | 5 black | hero, twin, softmax, type, bracket | 1422 | 1016 | 5.49 | 3.27 | 93 | 60.2 |
| | **total** | | **4,751** | **4,116** | **14.26** | **9.49 (67 %)** | | **191.8 + 6 × 90 s + 2 × 20 s ≈ 201 min** |

\* Strokes with extent < 0.7 mm: family dots, stipple, small scatter, small node discs.

**Batch table** (`--batch-strokes 400`, the plate job's resume granularity; the same ranges work as `plot layer … --strokes S:E`):

| layer | pen | batch `--strokes` | region (sheet mm) | min | cum. min (incl. 90 s swap before each layer) |
|---|---|---|---|---|---|
| 1 | 2 gold | 0:400 | ∂L/∂V row + return fan, then V→Z bundle into the V block (x 15–191, y 17–115) | 15.9 | 17 |
| 1 | 2 gold | 400:720 | V block, feeds, right column (x 104–191, y 70–114) | 12.5 | 30 |
| 2 | 1 blue | 0:400 | ∂L/∂K stack (strokes 0:123), **hop at 123** → K fans (x 15–182, y 24–250) | 15.1 | 47 |
| 2 | 1 blue | 400:800 | K rows (x 115–183, y 199–267) | 15.9 | 62 |
| 2 | 1 blue | 800:1058 | K rows, verticals, K glyph (x 113–192, y 183–269) | 9.9 | 72 |
| 3 | 3 green | 0:201 | Z row, ∂L/∂Z, drop curve (x 41–133, y 18–80) | 8.9 | 83 |
| 4 | 0 crimson | 0:400 | ∂L/∂Q stack (0:136), **hop at 136** → Q fans (x 15–96, y 38–262) | 16.0 | 100 |
| 4 | 0 crimson | 400:800 | Q rows (x 18–89, y 200–269) | 15.2 | 115 |
| 4 | 0 crimson | 800:1082 | Q rows, verticals, Q glyph (x 18–97, y 178–268) | 10.4 | 126 |
| 5 | 4 violet | 0:268 | FFN forward + backward rows (x 132–196, y 27–75) | 11.7 | 139 |
| 6 | 5 black | 0:400 | twin, backward labels (0:357), **hop at 357** → softmax, lower hero (x 57–179, y 16–187) | 16.2 | 157 |
| 6 | 5 black | 400:800 | hero (x 54–141, y 116–198) | 18.3 | 175 |
| 6 | 5 black | 800:1200 | hero, halos, fraction (x 44–166, y 116–222) | 15.5 | 191 |
| 6 | 5 black | 1200:1422 | hero right, **hop at 1388** → title (x 37–173, y 116–280) | 10.2 | 201 |

**Session plan** (≈ 3 h 20 min of machine time plus swaps; frame trace first, on A4 portrait, margin 10):

```
promptplot plot plate gallery/studio/resonance_ffn/current/pp_resonance_ffn_iterate_v5.gcode \
  --layers 2,1,3,0,4,5 --paper a4:portrait --margin 10 --batch-strokes 400 --rezero-every 800
```

- **Session A, ≈ 83 min:** gold, blue, green. Stop point: the green layer's end, i.e. the crimson swap wait. Park is automatic at every swap wait. Ctrl-C once at any batch end pauses, and `promptplot plot plate --resume <JOB_ID>` resumes (origin check first).
- **Session B, ≈ 57 min:** crimson, violet. Stop at the black swap wait.
- **Session C, ≈ 62 min:** black. It is the longest layer. The natural pause is after batch 800:1200 (hero done, only the right hero and the title left).
- **Re-zero checks.** Every swap wait counts as an origin check, and no layer exceeds 1,422 strokes. `--rezero-every 800` therefore adds exactly one mid-layer check in each long layer, at blue stroke 800, crimson stroke 800 and black stroke 800. Each lands on a batch boundary, after the head has left the lower region, which is where Leo's drift would show first. That is +60 s on the model.
- Ink: blue and crimson each lay ≈ 1,000 dots. On a fineliner that is ~40 min of continuous touch-downs, so check the tip between batches 1 and 2.

## Self-critique

| dimension | score | why |
|---|---|---|
| Hierarchy | 5 | v9's own hierarchy, unchanged. But continuous dots make the 20 Q/K fans and the ochre falls the loudest marks on the upper and middle sheet. They now compete with the hero where v9's faint dashes deferred to it. |
| Grid & alignment | 6 | r01's traced grid, untouched. Bracket legs now point at their nodes. |
| Tension | 4 | Mirror-symmetric top and centred title, as in v9. Frozen by J2. |
| Negative space | 4 | The lower third is still jammed (A7, blocked). The bare foot at v 0.95–0.97 survives. |
| Craft for pen | 7 | One round dot everywhere, pitch 0.998 mm median, 0 ticks, 0 micro-dashes, 0 invisible family dots, solid arrowheads, arcs stop on their curves, file order = computed order, 67 % travel. Against that: 166 dots still offset in crossings, and 2 black hops over 80 mm. |
| Concept | 4 | Still a labelled transformer-block diagram (§6 ≤ 3 by rule), unchanged by design. |
| Depth | 3 | Flat, declared. |

**The single worst thing:** the Q/K funnel. With every dotted line now a continuous 1 mm train, the 20 fans read as a heavy crimson and blue rope bundle converging on the hero's upper flanks. Where three fans cross at a shallow angle (sheet ≈ x 86–92 / 118–124, y 195–220), 114 dots still sit off-phase and read as speckle. The mark is right. The fan geometry is r01's, and it was drawn for faint dashes.

## Engine requests

1. **Let a piece's stroke order survive the render.** `postprocess.reorder_by_color` → `optimize_stroke_order` re-sorts every colour by nearest START from (0,0), with no reversal. A piece can only steer it by stroke direction (`_polish` here). A `ColorConfig.optimize=False` or a `render_candidate.py --keep-order` would let region-banded orders through. The 90–93 mm black hops need that.
2. **Region-aligned batches in `plot plate`.** Accept `--batches` as explicit stroke boundaries per layer, e.g. blue `0:123,123:…`, so a batch never straddles a region change.
3. **A shared `kit.dotted(pts, pitch=1.0, r=0.15)`** with end-anchoring and phase-locking. The family dot is now copied across resonance, resonance-backprop and resonance-ffn.
4. **`render_candidate.py --pen-width MM`** passing `pen_widths` to the preview. Here, nib-width judging was done with a local crop renderer.
