# resonance-backprop r04 — iterate · parent: r01 · 2026-09-29

**Lineage.** 19th-century physiological acoustics, the graphic method. The reference work is Hermann von Helmholtz,
*Die Lehre von den Tonempfindungen / On the Sensations of Tone* (1863), and specifically its wave-composition
figures. Those figures stack rows of partial waves on shared axes, one above another, and sum them into a single
compound wave drawn below.

The ORDER the plate borrows is **stacked partials → one sum → the sum read back**:
- the Q and K rows are the partials;
- the two-source field is their superposition;
- A selects from it;
- Z = AV is the compound wave;
- the backward band re-reads the same stack upward.

This lineage is distinct from Young (the resonance sibling), LeWitt (the flavour `the-fold`) and Riley (the flavour
`gradient-as-phase`).

**Depth.** Flat, declared: this is a reproduction of a flat plate diagram, and no depth is claimed.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance-backprop/rounds/r04/piece.py \
  --fn attention_as_resonance --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,forestgreen,crimson,black \
  --out gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3.png
.venv/bin/python studio/resonance-backprop/rounds/r04/plate.py \
  --out gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.gcode --png
```

- **Final render:** `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3.png`, seed 7.
- **Plotting gcode:** `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.gcode`, with its preview in `_v3_plate.png`.
  - This file is the one to plot. It is written by `plate.py`, which runs the same postprocess stages as the render
    (arcs, bounds, pen safety, dwells) but skips the per-colour nearest-START reorder. That reorder restarts from
    (0, 0) and cannot reverse a stroke, so it would undo the stream order built by the piece.
  - The drawing is identical to the render. Only the stroke order differs.
  - The file is deterministic: a re-run is byte-identical apart from the timestamp line.
- `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3.gcode` is the render pipeline's gcode. It has the same marks in greedy
  order and is **not** for plotting.
- **Nib-width crops** (0.35 mm, from the plate gcode): `~/Downloads/pp_res_backprop_iterate_v3_nib_{subtitle,densest,comb,dq_fan}.png`.
- **Seed.** Seed 7 is the only seed that reproduces v5: the ten seeded scatter draws are r01's at seed 7, and v5's
  scatter was measured at those exact positions. Seeds 11 and 3 move only those scatter discs (5,651 and 5,650 cycles,
  229.9 min).

**Iterations**
- **v1** — The first build. Its crossings were over-culled: the second crest family lost a dot within 0.95 mm of any
  first-family dot, so it was decimated at every crossing. The serpentine sweep ran in a fixed direction, which left
  a hop of more than 80 mm in every layer.
- **v2** — Two dots now count as duplicates only when their inks touch (centres < 0.65 mm apart). Each row is entered
  from the nearer end. Paths are trimmed to their visible extent before end-anchoring.
- **v3** — Three changes:
  - packet envelopes lifted 0.8 mm off the crest tips;
  - the i-tittle kept open at nib width;
  - solid discs spiral at 0.30 mm pitch instead of 0.45.

## Mandate responses

| id | mandate | status |
|---|---|---|
| J2 | KEEP THE ORIGINAL: every element, all five pens, nothing removed to save time | **FIXED.** See the element diff against v5 below. Every r01 block is called in r01's order with r01's tables and coordinates. Two sub-1-mm mark moves, both inside J2's 1 mm tolerance and both made so a mark reads: (a) packet envelopes stand 0.8 mm off the crest tips (drawn ON the tips, 60 % of their dots were invisible); (b) the subtitle i/j tittle is lifted 0.33 mm (it was fusing into the stem, so "i" read as "l"). **Honest caveat:** the dotted *ghost waves* inside the Q/K/V/∂L packets lie under their own packets' solid ink along almost their whole length, so only 43 of their dots survive the invisibility rule. The geometry is kept in the file, and the softmax and ∂L/∂A ghost peaks read clearly. In v5 those packet ghosts were already indistinguishable from the crests |
| J1 | continuous dots: one round dot of one size, pitch 0.9–1.1 mm, end-anchored, converging paths phase-locked, no micro-dashes | **FIXED.** Every dotted line is a closed 8-gon of r 0.15 mm (r10's DOT_R), which inks to 0.65 mm at a 0.35 nib, placed every 1.0 mm with n = round(len/1.0) and n + 1 dots. Same-pen nearest-neighbour distance (10/50/90 %): ∂L/∂Q fan 0.987/**0.999**/1.010 (isolated leader) · Q fans 0.917/0.994/1.018 · V fans 0.801/0.995/1.012 · ∂L/∂Z fans 0.978/0.988/1.003 · black field 0.736/0.990/1.044. Paths are trimmed past nodes, arrowheads, labels and same-pen ink before anchoring, so each leader ends with a dot one clean gap short of its arrowhead (crop `_nib_dq_fan`). 88 paths are phase-locked to a parallel neighbour (anchors within 2 mm and 25°), and the paired fans read as parallel dotted lines at nib width (crop). There are **0 open straight strokes of 0.3–1.2 mm on any dotted line**: the scan finds 23, and all 23 are single-stroke glyph segments (rail labels, the subtitle, the fraction and formula strokes). v8's dashed oval is gone |
| A9 | plot discipline: one clean layer per pen, light→dark, spatial order, no hop > 80 mm, no invisible cycles, chained glyphs, budget + batches + session plan | **PARTIAL.** Five layers, each entered once, in index order = stream order: goldenrod, dodgerblue, forestgreen, crimson, black. Bounds: 0 violations. Travel is 11.69 m, below the ceiling of draw + dots × 1 mm = 14.11 + 4.84 = 18.95 m. Weighted glyph passes, the ∂ partial's second pass and every arrowhead (outline + hatch) are chained into one pen-down. The invisible-dot rules are applied by construction (counts below). **Not met:** one in-layer hop above 80 mm in dodgerblue (106 mm) and one in crimson (138 mm). Each is the single jump between that pen's two clusters, the Q/K block above and the ∂L/∂Q/∂L/∂K block below, which have no ink of that colour between v 0.32 and v 0.67. The vertical gap alone is ≥ 104 mm, so no order can avoid it; the crimson hop could be about 30 mm shorter with a row-direction look-ahead. Goldenrod, forestgreen and black have no hop above 72 mm |
| A7 | v5's grey band must not cross the Q/K/V fans or labels; keep the texture count; crop the densest field zone | **FIXED.** Black field dots (crest arcs, halos) keep 0.4 mm of paper to every other pen's ink and to every coloured fan centreline: 358 dots yield, so the field sits behind the fans. Dots whose centre is in a label box + 0.9 mm are dropped (37; exact `geometry.Rect`/`Union`). TEXTURE keeps its count and positions: 98 marks = 90 beads + 8 scatter discs, the same as r01 and v5, each one round dot or one solid disc by radius. When a fan meets a texture mark, the fan yields. The densest 20 × 20 mm is (104–124, 196–216) mm, 2,395 black vertices, and at nib width it is open, with no flood (`_nib_densest`) |
| A10 | name one movement + one work + the ORDER; declare depth | **FIXED.** Helmholtz, *On the Sensations of Tone* (1863): stacked partials summed into one compound wave. Flat, declared |
| A11 | small type open at 0.35 mm nib; subtitle crop | **FIXED.** Crop `_nib_subtitle`: the letters are open. The one fault was the i-tittle fusing into its stem ("selectlon"). The tittle is lifted 0.33 mm, which leaves 0.3 mm of paper, and is now a round dot. Tracking, text, position and size are unchanged |
| A3 | comb flood, gate check only | **CHECKED, no flood.** Crop `_nib_comb`: the fringes are 1.04 mm pitch, about 0.69 mm of paper between them at the 0.35 nib. It reads as a striped lozenge. The crest count is unchanged (m 10–50, d = 59 L, `_Guard` 0.82 mm / 25°) |
| A2 | packet braids | **DEFERRED — blocked by J2** (untouched, per SYNTH) |
| A6 | dead foot, move down | **DEFERRED — blocked by J2** (untouched) |
| A12 | arrowheads in the backward band | ARGUED (accepted, r03). Kept, now each one pen-down |
| S0 | no dossier/encoding | not a designer mandate (curator/expert) |
| A1, A4, A5, A8, S-fold, S-phase | — | dropped in the LEDGER (superseded or flavour-only) and not acted on |

### Element diff against v5 (J2 test)
- **Unchanged** (r01 code and coordinates, 0 mm move):
  - 5 + 5 Q/K rows with their nodes and verticals, 4 V rows, the Z packet with its eyes;
  - `Q·Kᵀ/√d_k`, the softmax row: 5 peaks, 4 ghost peaks and 9 baseline markers;
  - the 9 droplines up and down, the beaded columns;
  - the hero: bullseyes m 1–9, comb m 10–50 inside the lens, d = 59 L, `_Guard` 0.82 mm / 25°, the axis with its end circles and dot runs;
  - the whole backward band: ∂L/∂Z, ∂L/∂A, ∂L/∂Q, ∂L/∂K and ∂L/∂V, with all 38 arrowheads and every fan;
  - the rail with both arrows and both words, the title, rule and dot, the subtitle, the 4 crosses and their dotted ticks.
- **Rebuilt from v5's measurements** in place of v8's oval (below): 22 × 2 dotted crest rings and 3 × 2 halo
  ellipses. The field spans u 0.103–0.895, v 0.276–0.426, against v5's measured u 0.10–0.90, v 0.28–0.43.
- **Count:** 1,777 field dots at 1.0 mm, against v5's 1,643 visible field marks at 1.4–1.6 mm pitch (+8 %). Scatter:
  8 discs, the same as v5.

## What changed from parent

This is not a composition move: J2 freezes the composition. What changed is how every mark is made, and how the
sheet streams.

1. **The tonal field is v5's, not v8's.** The dashed crest oval is replaced by the field measured off v5: dotted
   crest arcs plus three dotted halo ellipses per source.
2. **The primitives emit MARKS, not gcode.** A mark is a line, node, texture, type, arrow or dotted PATH. Two sheet
   passes then see the whole plate:
   - `_realize` dots every path at the family pitch, phase-locks near-parallel same-pen neighbours, and drops only
     invisible dots;
   - `_order` streams the pens light→dark. Each layer is a serpentine sweep of 30 mm cells, starting at the bottom
     row (the head parks bottom-left), with each row entered from the nearer end and a reversal-aware nearest-end
     walk inside each cell.
3. **Glyph passes and arrowheads are chained.** `giant_type` is re-implemented locally: same glyphs, passes and
   advances, but boustrophedon-chained.
4. **Pens are re-indexed into stream order**, with meanings unchanged:
   - 0 goldenrod = V, ∂L/∂V
   - 1 blue = K, ∂L/∂K
   - 2 green = Z, ∂L/∂Z
   - 3 crimson = Q, ∂L/∂Q
   - 4 black = field, softmax, ∂L/∂A, rail, type, crosses

## Measurements / computations

### v5's tonal field, measured off `gallery/studio/res_backprop/current/pp_res_backprop_v5.png`

**Calibration.** The paper outline in the PNG gives x 0 → column 161 and x 210 → column 1590 (6.805 px/mm), and
y 0 → row 2150 and y 297 → row 130 (6.801 px/mm).

**Isolating the field.** The r01 code was rendered with parts 3, 4 and the scatter disabled (the "base"). Its black
mask was dilated by 2 px and subtracted from v5's black mask. That leaves 1,688 connected components inside the
hero, 1,680 of them in the band. Each was mapped back to reference px through r01's `_fit`: 0.174632 mm/px, origin
(10, 267.949) mm.

**Classification** (λ = 352/59 = 5.966 ref px = 1.042 mm):

| class | rule | count | (u, v) |
|---|---|---|---|
| **dotted crest arcs** | r_s / λ within 0.17 of an integer m ∈ {10, 13, …, 73} (step 3, 22 rings per source; the histogram peaks sit only on that ladder) | 1,125 | sources at u 0.353 / 0.646, v 0.351 |
| crest clip | boundary \|dy\| per \|dx\| bin: 128 / 120 / 114 / 97 / 72 / 48 / 15 px at \|dx\| 0 / 100 / 160 / 200 / 280 / 300 / 340 → ellipse centred (560, 448), **a 352, b 128 px** | — | centre (0.499, 0.351), u 0.207–0.792, v 0.276–0.426 |
| crest holes | min distance to either source 58.7 px = R_BULL + 5 (bullseye pad); the comb lens 100 × 40 px also empty | — | pad radius 10.25 mm; lens 17.5 × 7.0 mm half-axes |
| **dotted halo ellipses** | best fit per ring (dots within 2.5 px): **centred on each source, b = 0.40 a, a = 196 / 245.5 / 300 px**. Hits 63 / 87 / 116 (left) and 57 / 86 / 117 (right) | 518 | half-widths u ±0.163 / ±0.204 / ±0.250; half-heights v ±0.046 / ±0.058 / ±0.071; the outer pair spans u 0.103–0.895 |
| halo gaps | angular coverage: full except the lens crossing and ±~20° at both axis ends of the a = 196 pair (where the Q/K fans run in); r04 gets these gaps from the fan clearance rather than hard-coding them | — | — |
| **scatter** | 37 residual components. Eight of them are exactly r01's seeded draws (seed 7): ref (454, 364), (651, 345), (582, 416), (295, 450), (282, 432), (302, 350), (515, 526), (334, 382). Two draws, (636, 555) and (606, 423), are rejected by `place()` | 8 discs | (0.411, 0.302), (0.517, 0.332), (0.462, 0.397), (0.279, 0.352), (0.268, 0.342), (0.285, 0.293), (0.311, 0.312), (0.574, 0.291) |
| scatter radius classes | ink radius 0.32 (dot) ×3; 0.50–0.59 ×4; 0.69 ×1 mm | | |
| beaded columns | the same y-ladder as r01 (CY ± 22 j, j = 1..5) on all 9 droplines | 90 | — |

- **v5 dot pitch:** crest arcs 1.32–1.56 mm (median about 1.4), halos 1.58–1.61 mm.
- **Finding:** DESCRIPTION's "dense seeded dot scatter that greys the whole band" is really the dotted crest arcs at
  about 1.4 mm pitch. The seeded scatter is only r01's 10 draws, of which 8 are placed.

### r04 dot accounting (v3, from `piece.STATS`)

**Kept:** 4,835 dots.
- fan 1,675
- field 1,777
- envelope 715
- guide 448
- dropline 177
- ghost 43

**Dropped as invisible:** 2,463 in total.
- 795 co-incident (inks touch another dot, centres < 0.65 mm): 629 at crest/crest and crest/halo crossings, 140 in
  fans, 14 in envelopes, 12 in guides
- 695 with less than 0.3 mm of paper to same-pen ink: 533 envelope dots on braided neighbour rows, 53 ghost dots,
  44 fan dots, 35 field dots, 21 guide dots, 9 dropline dots
- 578 on a node (centre within r_ink + 0.525 mm of a node, disc, bead or arrowhead)
- 358 in the field-behind-other-pens clearance
- 37 in label boxes

## Plot budget

The model is PLOT_JOBS: F500 draw, 2000 mm/min travel, 2.0 s per pen cycle, 90 s per swap. The table is from
`plate.py`.

| order | pen | cycles | draw m | travel m | layer entry mm | max in-layer hop mm | hops > 80 | min |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 goldenrod | 769 | 1.75 | 1.52 | 155 | 38.1 | 0 | 31.4 |
| 2 | 1 dodgerblue | 839 | 2.79 | 1.81 | 110 | 106.4 | 1 | 35.9 |
| 3 | 2 forestgreen | 532 | 1.78 | 1.42 | 167 | 70.0 | 0 | 23.5 |
| 4 | 3 crimson | 832 | 2.79 | 1.65 | 69 | 138.2 | 1 | 35.6 |
| 5 | 4 black | 2,680 | 5.00 | 5.30 | 185 | 71.9 | 0 | 103.5 |
| **total** | 5 pens | **5,652** | **14.11** | **11.69** (83 % of draw) | | | | **230.0 min = 3.83 h** + frame trace + 2 re-zero checks (≈ 1 min) |

- **Against the baseline:** v8 had 4,053 cycles, 11.39 m draw and 11.90 m travel (105 %). Cycles rise 39 % because
  every dotted line is now continuous dots; travel falls to 83 % of draw.
- **Preview stats** (`preview --stats --score` on the plate gcode): 94,702 commands, grade A, 11.93 m travel
  including the layer entries and the final park.

**Why light → dark:**
- A dark nib dragged through light ink is invisible, but a light nib dragged through wet black carries black into
  goldenrod and blue. So the light pens go first.
- Black lands last, which also puts the field, the type and the crosses on top of the colour, as the reference does.
- Goldenrod is the lightest, then blue, then green, then crimson.

**Batch table** (`promptplot plot plate FILE --batch-strokes 400`, i.e. `--strokes S:E` per layer, with the sheet
region each batch covers in mm):

| layer | --strokes | region x | region y | note |
|---|---|---|---|---|
| 0 goldenrod | 0:400 | 60.6–199.3 | 80.4–148.8 | ∂L/∂V, the connector, the right-hand V/Z fans |
| 0 goldenrod | 400:769 | 16.2–90.1 | 131.0–164.1 | the V block and the left fans |
| 1 dodgerblue | 0:400 | 126.4–190.7 | 41.0–209.5 | ∂L/∂K block, then the one cluster jump up to the K fans |
| 1 dodgerblue | 400:800 | 124.9–188.1 | 192.2–247.6 | the K fans and rows |
| 1 dodgerblue | 800:839 | 150.2–188.1 | 240.3–252.2 | the top K rows and the letter |
| 2 forestgreen | 0:400 | 63.3–146.4 | 66.6–119.9 | ∂L/∂Z, its fans and the returns |
| 2 forestgreen | 400:532 | 35.7–174.1 | 90.3–143.4 | the Z row |
| 3 crimson | 0:400 | 19.3–80.5 | 41.0–208.7 | ∂L/∂Q block, then the one cluster jump to the Q fans |
| 3 crimson | 400:800 | 22.0–85.1 | 192.2–252.2 | the Q fans and rows |
| 3 crimson | 800:832 | 39.9–70.5 | 239.9–250.5 | the top Q rows and the letter |
| 4 black | 0:400 | 10.2–200.0 | 29.1–186.6 | the lower half, a sparse sweep: crosses, rail, ∂L/∂A, softmax |
| 4 black | 400:800 | 60.4–141.5 | 150.0–180.2 | the lower field band |
| 4 black | 800:1200 | 121.6–188.1 | 150.0–207.1 | the right end of the field |
| 4 black | 1200:1600 | 97.3–150.2 | 179.9–210.1 | the right half of the upper field, and the comb |
| 4 black | 1600:2000 | 59.4–120.1 | 179.9–210.1 | the left half of the upper field, bullseye L |
| 4 black | 2000:2400 | 12.4–96.0 | 179.9–242.1 | the left field end, the rail, the fraction |
| 4 black | 2400:2680 | 10.2–200.0 | 209.8–267.9 | the top band: title, subtitle, crosses |

**Session plan** (a 3.8 h plate; pause only at a batch boundary, with `p` in the terminal or Pause in the viewer, and
resume with `promptplot plot plate FILE --resume JOB_ID`, which waits for the origin check):
- **Session A, ≈ 92 min.** Frame trace, then goldenrod, dodgerblue and forestgreen (three swaps). Stop after the
  green layer completes; a layer end is the cleanest pause.
- **Session B, ≈ 36 min.** Resume, swap to crimson, run the whole layer.
- **Session C1, ≈ 47 min.** Swap to black, then `--strokes 0:1200`: the lower half and the lower and right field.
  Pause at the 1,200 boundary.
- **Session C2, ≈ 57 min.** Resume black 1200:2680: the upper field, the comb, the left end and the top band.
- Use `--rezero-every 2000`, which gives one extra origin check inside black at stroke 2,000 (≈ 20 s). A swap wait
  also counts as a re-zero check.
- Black is the registration-critical layer, since the field must sit inside the coloured fans, so if Leo has drifted
  by then, re-zero before C1.

## Self-critique (seven rubric dimensions, honest)

| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 5 | Unchanged from r01: the Z axis and the Q/K blocks still compete with the hero. The dotted field now reads as a mid-grey halo that makes the hero the largest single mass, which helps a little |
| 2 | grid & alignment | 6 | r01's traced grid, untouched |
| 3 | tension & asymmetry | 4 | Mirror-symmetric, frozen by J2 |
| 4 | negative space | 5 | The dead foot (A6) is frozen. The field no longer collides with the fans and labels, so the band reads as a halo instead of grey mud |
| 5 | craft for pen | 7 | Continuous round dots at a 1.00 mm median everywhere, phase-locked pairs, open type, an open comb, no floods, chained glyphs, spiral discs under the nib pitch. Two cluster hops above 80 mm, and the braided packet rows (A2) remain |
| 6 | concept legibility | 4 | Still a schematic: arrows, fractions, stages. J2 keeps it; Helmholtz's figures were schematics too, which is the argument |
| 7 | depth | 4 | Flat, declared |

**The single worst thing on the sheet** is the braided Q/K/V/∂L packet rows (A2). Adjacent rows' packets
interpenetrate into knots, and now that the envelopes are lifted and dotted the knots are even more visible, with
dots riding through the neighbouring row's crests. It is blocked by J2 until Juan rules.

## Engine requests

1. **A `--keep-order` / `order="as_emitted"` switch on the render pipeline.** `run_pipeline` always runs
   `reorder_by_color`, whose nearest-start pass from (0, 0) cannot reverse strokes and undoes a piece's own
   batch-aware order. That is why this round ships `plate.py`. `render_candidate.py` could honour a piece attribute
   such as `STREAM_ORDER = "as_emitted"`.
2. **The i/j tittle in `_GLYPHS`** sits 1.0 glyph unit above the stem. At cap heights under about 3 mm and a 0.35 mm
   nib it fuses into the stem. The central font could lift it by `max(0, 0.3 + nib − 1.0·sc)`, or `giant_type` could
   take a `nib=` argument.
3. **`kit.fill_disc(spacing=0.45)`** leaves a visible spiral at a 0.35 mm nib. Its default should be ≤ the nib.
4. `_dot` (a 2r hairline tick) is still the family's "dot" in r10. A closed-8-gon `round_dot(x, y, r)` in `kit`
   would give all three sibling plates the same round dot.
