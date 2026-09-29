# superposition r04 — iterate (merge: r02 layout + r03 field grammar) · parent: r02 · 2026-09-29

## Render

```
.venv/bin/python scripts/render_candidate.py studio/superposition/rounds/r04/piece.py \
  --fn superposition_iterate --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,crimson,forestgreen,black,black \
  --out gallery/studio/superposition/current/pp_superposition_iterate_v15.png
```

- Final: `gallery/studio/superposition/current/pp_superposition_iterate_v15.png` + `gallery/studio/superposition/current/pp_superposition_iterate_v15.gcode`.
  A4 portrait, cream. Seed 7. Nothing is random: seeds 3, 7 and 11 give byte-identical gcode
  bodies (md5 `f17bb5fa…`).
- Data: unchanged from r02. `piece.py` reads `../r02/head.npz` (written by `../r02/mechanism.py`,
  numpy GPT-2 small forward pass matched to torch at ≤ 2.3e-6 on all 12 layers).
- Self-rounds: v1 → v15, none overwritten.

## Lineage

**Systems art: Manfred Mohr, *Cubic Limit* (1973–75).** The order it lends: a high-dimensional
object shown only through one stated projection rule, the rule being the image. Here every
64-d vector is drawn only as `f(x) = Σₖ (c·eₖ) Hₖ(x/σ)` (Hermite functions, k < 3), and the rule
is printed on the sheet. Mohr's orthogonal routing (right angles, concentric fillets, a nested
staircase) is also how the strands travel. Kept from r02; the r02 and r03 art critics failed the
hang test because the rule was invisible. It is now in the footer, and the Q/K frame is chosen
so the rule carries one checkable identity (see S3).

## Mandate responses

| id | mandate | status |
|---|---|---|
| C1 | Keep the rhythm Q/K → field → softmax → V → Z | FIXED. Q family top-left, K family top-right, then the triangle, spikes, the V band (baseline 4–187 mm = 0.97 of the width, the widest band), the Z nest (narrower). Read top to bottom, the five stations meet in that order. |
| C2 | No pen cap, one clean layer per pen, stated order | FIXED (kept). 6 pens, `layer run order [0,1,2,3,4,5]`, each entered once. |
| C3 | Spatial order for batching; no in-layer travel > 60 mm in the EMITTED gcode | FIXED. Measured on the emitted gcode: max in-layer hop is 44.3 (goldenrod), 12.2 (blue), 12.2 (crimson), 43.1 (green), 46.3 (black) and 53.8 mm (type). Zero hops > 60 mm. The ordering is chosen by simulating the pipeline's own nearest-start pass and flipping stroke directions (`_order_layer`), so the order survives `reorder_by_color`. Two structural moves made it possible: (1) the ' itself' row line is drawn on the black pen (it ended 118 mm from any crimson ink); (2) all type moved into ONE band at the foot. |
| C4 | Minutes per layer + total | FIXED, see Plot budget. |
| C5 | No dotted guides / thousands of lifts | FIXED (kept). 872 pen cycles in total. The only broken lines are duty-coded dashes (~70 cycles). |
| C6 | Name the lineage; it must hold beside the work | FIXED/ARGUED. Mohr, with the rule now printed and one identity checkable from the sheet. Whether it holds beside *Cubic Limit* is the art critic's call. |
| A1 | A schematic of the equation / a slide figure | PARTLY FIXED / ARGUED. C1 binds the five stations. The station captions are gone (no `Q·Kᵀ`, `softmax`, `1/13`, no Q/K/V letters, no ticks). Superposition is now literal: Z is built by visible addition. The routing is a Mohr-style orthogonal system rather than labelled arrows. It is still a pipeline, top to bottom. |
| A3 | Symmetric about u 0.50 | FIXED. A right triangle with its apex top-left and a double-pass knife running to the lower right. The spine leans with the data: the five drops sit at columns 2, 3, 7, 10, 11 (x 48, 59, 102, 134, 145). Z's centre is the attention-weighted mean column (6.45 → x 96.1), with the 1× ghost off to its right. Q and K are no longer mirrored in content (K keys are S-shaped, see S3). |
| A4 | Map ≥ 0.55 width, dominant | KEPT. The triangle spans x 21 → 188.4 (0.88 of the width) and y 51 → 140. It is the largest form, but see Self-critique: it is NOT the darkest. |
| A7 | Declared flat | KEPT (HANDOFF `declared:` line). |
| A8 + S1 | Superposition literal: 6 partial sums, one centre, one baseline, outermost = R(z), strands land on their curve | FIXED. The six curves are hole, +transformer, +plot, +ter, +watched, +rest. They are Σ a_j R(v_j) in V's rule, drawn at a DECLARED ×2.5 (both axes: σ 16.5 mm, 10 mm/unit), with the 1× R(z) drawn beside it on the same baseline as a dashed ghost (σ 6.6, 4 mm/unit, crest 16.0 mm). Labels `×2.5` and `×1` are printed. The outermost curve equals R(z) exactly: \|partial₆ − c_z\| = 6e-16, and c_z = (5.3315, 0, 0) because e₀ = ẑ, so R(z) is a pure H₀ by construction. **Nesting, honestly:** consecutive sums do NOT all nest. The minimum gaps between successive sums over x ∈ ±3σ are +0.16, −1.22, −1.95, +0.34, +0.08 mm. The hole sum leans (H₁ = −1.09), and +transformer and +plot straighten it (H₁ → −0.43), so the curves cross on the left flank. That is the visible cancellation of lean, and it is true. Where two sums run within 0.85 mm, the inner one pauses (engine Occupancy). Every drawn V→Z strand ends ON the curve its term creates, gap 0.000 mm (table below). |
| A9 | Field craft: continuous rings, no ghost arcs, no fragment < 3 mm, no pair < 0.8 mm, knife to the apex, no eye chopped by the frame | FIXED. Rings are the level sets of an upper envelope of equal-slope cones and capsules, so level n and n+1 are exact offsets, 0.82 mm apart everywhere. There are no ghost arcs and no lakes (0). Fragments under 3 mm are dropped (31, mostly innermost rings of radius < 0.5 mm). Black near-parallel contact under 0.8 mm is 2.8 mm in total (minimum 0.64 mm), down from 77 mm in v6. The knife runs from the true apex (21.0, 51.2) to the base corner (188.4, 139.6). All three triangle sides are drawn, so every clipped ring ends ON ink. Where a ring would graze the knife or the base at under 40°, it is cut back to 0.8 mm off the edge. No eye touches the paper frame. |
| A10 + C3 | Every connector arrives; no strokes < 1.5 mm | FIXED for every drawn element. Q strands end on the drawn left edge at their row (x 21.0). K strands end on the knife's outer pass at their column. The five black drops end ON their spike apex. The gold drops end ON their V crest. The V→Z strands end ON their partial sum (gap 0). **0 strokes under 1.5 mm outside the type layer.** The type layer has 197 glyph strokes under 1.5 mm (stroke-font glyph parts), a declared exception. Five values with a/max < 0.15 (The, a, black, while, the) send no strand: at duty ≤ 0.14 a strand is two 1.6 mm dashes 30+ mm apart and read as debris in v3–v4. Their terms still enter the +rest sum. |
| A11 | Right triangle, apex top-left, base ≥ 0.85 | FIXED: 0.88. |
| A12 | Shared edges | DEFERRED (per SYNTH). Partial alignment: the V band, softmax and field share the key columns, and the Q strands land on x 21. |
| A13 | Strip figure furniture | FIXED. No `Q·Kᵀ`, `softmax`, `1/13`, threshold, tick rows, tick axis or section cut. Between the Q/K band and the footer the only type is the five token names and `Z = AV` (plus the scale marks `×2.5` and `×1` that S1 requires). |
| S2 | Field true, stated scale, equal values get equal rings, rule printed | FIXED. Encoding: lift = ln(A·(i+1)). **Ring n sits at A·(i+1) = 1.2ⁿ, n ≥ 0; ring 0 = uniform** (printed). The field evaluated exactly at every cell centre equals the lift for every cell with lift > 0 (max relative error 0.0). One zero-lift cell, (12, 8) itself→while, reads F = 0.055 (a neighbour cone reaching 0.055 nat above uniform). That falls below any ring: its coast would have radius 0.25 mm and it is not drawn. No level sits above the maximum (11 levels, 0 … 1.82 < 2.086). Equal values get equal rings: plot (0.597) and transformer (0.600) both show 3. **Why rings are not denser:** a cone gentler than 0.232 nat/mm would reach false rings onto neighbouring cells (the binding pair is (11,8) → (12,8), 5.7 mm apart). v2–v8 used ×1.1 per 0.9 mm and put 9 false rings on cell (14,13). |
| S3 | Rule and provenance printed; one inner product checkable at its cell | FIXED. Footer line 1: GPT-2 small, L11 H8, the sentence. Footer line 2: the Hermite rule, the two frames (`Q,K: e₀ = q(itself)`, `V,Z: e₀ = z`), the ring rule and `itself·hole = 16.9/8 = 2.11`. **Checkable on the sheet:** Q and K share one frame with e₀ = q(itself)/\|q\|. So the red ' itself' curve is a pure bell, and the overlap of the drawn ' itself' curve with ANY drawn key curve equals q·k. Measured on the drawn curves: ∫ f_itself f_hole dx = 190.631 mm³ = S²σ·q·k = 1.85²·3.3·16.879 ✓. Equivalently, every blue key's bell (H₀) height is its score with ' itself' (hole 2.52 mm, the tallest; The −6.83 mm, hanging down). The cell mark is the hole eye at (12, 7): 7 rings, innermost radius 0.48 mm at the exact centre, on the slice. |
| S4 | Q/K token names on rulers | DEFERRED (per SYNTH). The five attended keys are named at the V band. |
| S5 | No dossier/encoding: check-number table in NOTES | FIXED: see Measurements. |

Dropped per LEDGER: A6 and A14. Fixed earlier and preserved: A2, A5.

## What changed from parent (r02)

- **The field.** r02's centred pyramid of summed cones (ghost arcs, crumbs, a 241 mm hop) became
  a RIGHT triangle. Key 0 is the vertical left edge, the double-pass causal knife runs from the
  true apex to the base corner, and the base is drawn. The field is the upper envelope of
  equal-slope cones, one per cell, plus one capsule per pair of neighbouring attended cells
  whose eyes merge. Merging pairs therefore become tapered teardrops (8 pairs) instead of
  pinching into necks under the pen floor. The masked future stays blank of black.
- **Strands, as Mohr routing.** Query i: down from its token, left along a nested turn band,
  down a 15-lane gutter, right onto row i. Key t: down from its token, left along a nested
  staircase, down ITS OWN COLUMN onto the knife. Every column is therefore one vertical line,
  top to bottom: blue above the knife, field inside, black drop from row 12, spike, gold drop,
  V curve. The strands leave clear of their family's ink (no riding a steep flank).
- **The spine leans with the data.** Row 12 is sliced (black line broken inside every eye).
  Its five above-uniform keys drop down their key columns to their spike apex, and on in gold
  to their V crest.
- **Z by visible addition.** Six partial sums at a declared ×2.5 with the 1× R(z) ghost. The
  strands reach one common arrival height above the nest, then drop vertically onto their own
  sum.
- **Type.** All captions deleted. Everything lives in one band at the foot: the five token names
  under V, `Z = AV ×2.5`, `×1`, the punchline caption, provenance and rule.
- **Frames.** Q and K moved from two frames (r02) to one shared frame (e₀ = q(itself)), which
  makes the overlap identity true for every drawn Q–K pair involving ' itself'. Consequence,
  and a fact about the head: the keys' largest component is a direction common to all keys,
  orthogonal to q(itself). It lands on the lean mode, so every key is S-shaped (H₁ ≈ 8–9.8).
  That lean shifts every score in a row by the same amount, which softmax cannot see. Only the
  bell part (H₀) differs between keys, and it is exactly the score.

## Measurements / computations

**Provenance.** \|A_recomputed − A_file\| = 0, \|a·V − z\| = 2.2e-16, overlap identity max error
2.1e-14. q(itself)·k(hole) = 16.879, /8 = 2.1098.

**Check-number table** (design coordinates, mm, y down; the gcode is the same plus (10, 287−y)):

| quantity | value | where on sheet | mm |
|---|---|---|---|
| cell (i, j) centre | — | x = 21 + 10.8(j+½), y = 54.09 + 5.7(i+½) | — |
| knife | key ≤ query, x = 21 + 10.8(q+1) | apex (21.0, 51.24) → (188.4, 139.59); 2nd pass +0.9 mm toward future | — |
| ring n | A·(i+1) = 1.2ⁿ, n ≥ 0 | radius = (lift − n·0.1823)/0.2223 | pitch 0.82 |
| hole (12,7) | A .2558, A·13 = 3.33, lift 1.202 | 7 rings, coast r 5.40, innermost r 0.48 | (102.0, 125.37) |
| plot (12,2) / transformer (12,10) | lift .597 / .600 | 3 visible each (innermost r .22/.24 < 0.5, dropped) | x 48.0 / 134.4 |
| ter (12,3) | lift .505 | 3 rings, coast r 2.27 | x 58.8 |
| watched (12,11) | lift .324 | 2 rings, coast r 1.46 | x 145.2 |
| '.'→'.' (14,14) | A .537, lift 2.086 | 12 rings, coast r 9.38, clipped on knife and base | (177.6, 136.74) |
| (11,8) / (10,8) / (9,9) / (6,5) / (1,1) | lift 1.323 / 1.299 / 1.209 / 1.045 / .693 | 8 / 8 / 7 / 6 / 4 rings | — |
| softmax spike j | 72 mm × A₁₂,ⱼ | baseline y 162.0, under column j | hole 18.42, transformer 10.09, plot 10.06, ter 9.18, watched 7.66, pen 4.05, itself 3.63, drew 3.23, while 2.65, the 1.30, a .88, black .83, The .01 (not drawn) |
| Q/K curve | Σ c_k H_k(x/3.3) × 1.85 mm | baseline y 19.5, Q token t at x 86 − 5.2t, K at 108 + 5.2t | ' itself' pure bell 12.9 mm |
| K bell part | H₀ height = 1.85·0.751·q·k/\|q\| | on each blue curve | hole 2.52, plot 1.80, transformer 1.80, ter 1.69, watched 1.47, The −6.83 |
| V curve j | Σ c_k H_k(x/6.6) × 4.0 mm, e₀ = ẑ | baseline y 196.5 under column j | hole crest at centre 21.2 |
| Z partial sums (×2.5) | value at centre | baseline y 262.0, centre x 96.09 (= column 6.453) | 13.22, 16.56, 24.59, 32.46, 33.03, 40.05 |
| 1× R(z) ghost | c_z = (5.3315, 0, 0) | centre x 167.1, same baseline | crest 16.02 |
| duty | ink fraction = a_j / a_max | gold strands | hole 1.000 (solid), transformer .548, plot .546, ter .498, watched .416, pen .220, itself .197, drew .176 |

**V→Z landings** (landing point, the curve its term creates, gap to that drawn curve):
pen → +rest (76.81, 241.77) 0.000 · plot → +plot (82.38, 241.87) 0.000 · ter → +ter
(99.14, 230.65) 0.000 · drew → +rest (101.81, 224.28) 0.000 · hole → hole (104.43, 255.44)
0.000 · transformer → +transformer (107.08, 251.27) 0.000 · watched → +watched (109.84, 239.14)
0.000 · itself → +rest (115.31, 241.67) 0.000. Landing x rises with token index, so no two
strands cross.

**Frames captured** (fraction of \|c\|² in the 3 drawn modes): Q
`.08 .44 .64 .73 .70 .52 .42 .64 .69 .60 .53 .68 1.00 .65 .53`; K
`.23 .69 .76 .80 .82 .79 .72 .82 .81 .81 .82 .80 .74 .76 .67`; V
`.01 .39 .90 .92 .63 .47 .16 1.00 .51 .51 .77 .69 .56`.

**Spacing audit** on the emitted gcode (0.4 mm samples, different strokes of one pen, \|cos\| > 0.94,
< 0.8 mm): goldenrod 0.8 mm (min 0.58), blue 2.8 mm (min 0.36, one strand start beside a K
flank), crimson 0, green 0, black 2.8 mm (min 0.64). Type: 334 mm glyph-internal, a declared
exception, as in r03.

## Plot budget

Leo model (the same as `promptplot.plotjob`): draw at F500, travel at 2000 mm/min, 2 s per pen
cycle, 90 s per swap. Travel includes each layer's entry move.

| order | pen | meaning | strokes | draw m | travel m | max in-layer hop | min |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | goldenrod | V (13 value curves + baseline + 2 future rings), softmax→V drops, V→Z strands (duty-coded) | 106 | 1.09 | 0.70 | 44.3 | 6.1 |
| 2 | dodgerblue | K family (15 keys), K staircase strands to the knife | 73 | 2.32 | 0.44 | 12.2 | 7.3 |
| 3 | crimson | Q family (15 queries), Q gutter strands to the rows | 56 | 2.24 | 0.33 | 12.2 | 6.5 |
| 4 | forestgreen | Z: 6 partial sums (×2.5), baseline, 1× R(z) ghost (dashed) | 23 | 0.62 | 0.35 | 43.1 | 2.2 |
| 5 | black | field rings, triangle (knife ×2, base, left edge), row-12 slice, drops, softmax | 156 | 2.77 | 0.87 | 46.3 | 11.2 |
| 6 | fine black | type (token names, Z = AV, ×2.5, ×1, caption, 2 footer lines) | 458 | 0.91 | 0.89 | 53.8 | 17.5 |
| | **total** | | **872** | **9.95** | **3.58** | | **50.8 + 6 swaps ≈ 59.8** |

- Order light → dark: the black lands after every colour it crosses, and type goes last on its own
  fine pen.
- 38 120 commands. The engine scorer grades it A (0.984 composition, 0.868 efficiency). Its
  "longest travel 248.8 mm" is a between-layer entry or park move, not an in-layer hop.
- Type is the largest cycle cost (458 of 872, ~15 min).

## Self-critique

| dimension | score | note |
|---|---:|---|
| Hierarchy | 6 | The triangle is the largest form, and the double knife gives it the plate's heaviest line. But the red/blue routing up top is darker in ink than the field. The field is truthfully sparse: one row of this head mostly attends below uniform. The green nest is a clear third. |
| Grid & alignment | 7 | Every key column is one vertical from the K staircase through field, spike and V. The Q strands land on x 21. The Z group centres on the attention barycentre, not on a grid line. |
| Tension & asymmetry | 7 | Right triangle, diagonal knife, leaning spine, ghost off to the right. The top pair of families is still a near-mirror. |
| Negative space | 6 | The masked future holds the blue staircase (as the SYNTH asked), so it is not blank. The lower-left and lower-right around Z are open but unassigned. |
| Craft for pen | 8 | Constant 0.82 mm ring pitch, 0 hops > 60 mm, 0 non-type crumbs, residual contact ≤ 2.8 mm per pen, 872 cycles, ~60 min. |
| Concept legibility | 6 | Z = Σ a_j v_j now reads as addition (six sums, the lean straightening, the 1× ghost). It is still a top-to-bottom pipeline. |
| Depth | 5 | Declared flat. Over/under only: drops pass under eyes, strands pierce outer sums. |

**The single worst thing:** the field does not command the sheet. With cones steep enough that
no cell shows false rings (the S2 test), the eyes cannot be bigger than the 5.7 mm row pitch
allows. The black mass is a constellation plus the '.'→'.' wedge, and the red gutter/turn band
out-inks it at 3 m.

## Engine requests

1. `postprocess.optimize_stroke_order` restarts every colour from (0, 0) and never reverses a
   stroke. This piece simulates that pass and searches stroke directions around it
   (`_order_layer`, ~20 s per render). A serpentine/2-opt order with reversal in the pipeline
   would remove the need.
2. A `kit.duty_dash(polyline, duty, period, min_dash)` whose dashes start and end on the
   polyline's ends (so a strand touches both of its targets). This is the third piece that
   hand-rolls it.
3. `_GLYPHS['i']` advance bug (still worked around by measuring ink extents).
