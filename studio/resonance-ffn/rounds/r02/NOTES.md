# resonance-ffn r02 — the squash (abstract) · parent: r01 · 2026-09-28

**Lineage.** Op Art: Bridget Riley, *Current* (1964). One family of lines, and the spacing of that
family is the whole surface. The order it lends is **laminar**: one fan of non-crossing streamlines,
squeezed and re-opened, so line spacing is the only variable. Here the spacing is set by tanh and
tanh′. The lineage is not the family's Young (benchmark) or LeWitt (the fold).

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance-ffn/rounds/r02/piece.py \
  --fn resonance_ffn_squash --seed 7 --paper a4 \
  --palette dodgerblue,crimson,forestgreen,darkviolet,black \
  --out gallery/studio/resonance_ffn/current/pp_resonance_ffn_the-squash_v15.png
```

- final: `gallery/studio/resonance_ffn/current/pp_resonance_ffn_the-squash_v15.png` + `.gcode`, seed 7, A4 portrait, cream
- **Seed-independent.** Nothing on the plate is random. Seeds 7, 11 and 23 give byte-identical
  G-code bodies (md5 `7e1b87e9…`). v13 to v15 were code clean-ups that left the geometry unchanged
  (same md5).
- `--colors` defaults to the palette length (5). **Palette order is stream order.**

## Mandate responses

`studio/resonance-ffn/` has no LEDGER.md, so there are no open A* or S* rows. The work order is
Juan's FEEDBACK.md REWORK (J1), the curator note (C*) and DESCRIPTION.md's "the squash" brief with
its Weak list (W*).

| id | mandate | status |
|---|---|---|
| J1 | dotted lines should be continuous dots: one fixed round dot, constant pitch, end-anchored, same pitch family-wide, no dashes to save cycles | FIXED. The only dotted lines are the two ±1 asymptotes. Each dot is one round mark, a closed loop of r = 0.15 mm that a 0.35 nib inks about 0.65 mm across. Dots sit every 1.00 mm of arclength (`n = round(L/1.0)` intervals, n+1 dots, both ends carry one). No micro-dashes, no converging dotted paths. The asymptote is the one place a dotted line means something: approached, never reached |
| C1 | keep the family grammar: Q crimson, K blue, two-source field, V goldenrod, Z green, FFN violet | FIXED for Q, K, field, Z and FFN: Q and K crest circles in crimson and blue, the fringe fan (Z) green, the FFN violet. **ARGUED for V.** The plate draws the resonance pattern and its squash. No value tensor is on the sheet, so a goldenrod mark would carry nothing. Five pens, five meanings |
| C2 | no pen cap; each pen one clean layer, stated order | FIXED. 5 layers, 5 colour runs in the file, none re-entered. Stream order light to dark: blue, crimson, green, violet, black. Crimson crosses blue in the lens, green starts at the ring edge, and violet meets green only at the gate gap. Black (dots, type) lands last |
| C3 | strokes spatially ordered for batching | FIXED within the piece. Neighbouring streamlines alternate direction (boustrophedon), so the per-colour nearest-neighbour pass walks down the fan. Rings are emitted by m, and dots are emitted in path order. Longest stroke is 117 mm (about 14 s at F500), so every stroke fits in a batch. Largest in-layer hop is 205 mm (violet, forward fan to backward fan, once) |
| C4 | minutes per layer + total in NOTES | FIXED (Plot budget) |
| C5 | waste: 3,725 pen cycles and 101 % travel today; dotted runs must earn their cycles | FIXED: **526 pen cycles (−86 %)**, travel 7.6 m = **61 %** of draw. Dots are 198 of the cycles, all on the asymptotes; the other 62 black cycles are type |
| C6 | name the LINEAGE | FIXED (top) |
| B1 | the squash: the FFN fan becomes the plate, fed by the field's crest intensities, tanh in the middle (flat top), fanned right; below it the same bundle with the derivative notch | FIXED. One bundle crosses the sheet. It is born as the field's bright fringes (the loci where Q and K resonate), eases onto B·tanh(u), is crushed against the dotted ±1 asymptotes, then fans out as rays. The backward bundle is the same geometry; its left ends trace tanh′ |
| B2 | delete the Q/K blocks, fractions, stage names | FIXED. No packets, fractions, stage names or arrows. Type is the title block (bottom-left) plus "+1"/"−1" on the asymptotes |
| B3 | FLOW order, two or three pens, one dominant form | FIXED on flow and one form. **ARGUED on pens**: the curator note supersedes the 2–3 pen line. Five pens, each a family meaning |
| W1 | [concept] schematic (≤ 3) | FIXED in intent. No boxes, labels-as-explanation or arrows. What remains is one laminar fan and its echo. A critic may still read "transfer function", see Self-critique |
| W2 | [space] lower third jammed | FIXED: two quiet zones. One is the lower-left quadrant (about 70 × 45 mm, only the title). The other is the wedge between the two right fans (about 50 × 40 mm). Gap between the bundles is ≥ 14 mm at the gate and 38 mm at the frame |
| W3 | [craft] packets overlapping (ochre knot, ∂L/∂Q pairs), bracket leg on a packet | GONE with the packets. Parallel crowding is 1.1 % of violet and 0.1 % of green (below) |
| W4 | [hierarchy] nothing dominates | FIXED. The forward bundle spans the sheet width (190 × 110 mm). Second is the ring field, third the backward echo |
| W5 | [tension] mirror symmetry, centred title | FIXED. The field sits cropped at the left frame, the fans are cropped at the right frame, and the title is bottom-left. B1 = 0.28 makes the squash lopsided: 13 lines die on the top rail against 10 on the bottom |
| W6 | [craft] six pens / five swaps | ARGUED: five pens, four swaps, one clean layer each; the cap is lifted |
| W7 | v5's condensed type | N/A: stroke type at 3.0 / 2.2 mm, fixed advance, no condensing |
| L1 | house law: dotted lines, never arrows | FIXED: no arrows anywhere |
| L2 | house law: text on its own layer with halos | FIXED: all type is on black via `Scene3D.halo_labels` |
| L3 | house law: crowding solved with engine-native anti-crowding | FIXED with the engine `Occupancy` grid plus a direction test (see Engine requests). Pause-and-resume, centre-out, with a lock inside the squash |

## What changed from parent

This is a new plate, not a parameter diff. r01 reproduced the reference: Q/K packet blocks,
fraction, hero, softmax, V, Z, an FFN band with three labelled stages, a backward row and a mini
field. r02 keeps one idea from it, the FFN fan (DESCRIPTION's "best idea this sibling adds"), and
makes it the sheet:

1. **The field is the source of the fan.** Q and K sit on one vertical line at the left frame,
   cropped by it. Their bright fringes (hyperbolae `r_Q − r_K = mλ`) are the streamlines. The fan is
   the interference pattern read as lines, so it is not an invented spray.
2. **The squash is a throat.** Between the gate (x = 86) and the throat (x = 116) every line eases
   onto `B·tanh(u)`. 23 of 49 lines would sit within 0.8 mm of a ±1 asymptote. They pause and, by
   the lock, end there. The crushed lines leave a wedge of line-ends against each dotted asymptote:
   the flat top, drawn.
3. **The right fan is a linear map**, so the lines become rays, cropped by the frame.
4. **The backward is the same bundle.** It is identical right of the gate, because dL/do = 1 on
   every line. Left of the gate each line reaches back toward the sources `1 − h²` of the way. The
   green ends make a bell pointing left, and that bell is tanh′. The saturated lines have no green
   at all. Their violet stubs end at the gate: the gradient arrives and goes nowhere.
5. **The gradient's sources shrink**: round(21 × mean(1 − h²)) = **6** crest circles each, against
   the field's 21.
6. The gate is a 0.9 mm hairline of blank paper down both bundles, where green hands over to violet
   (it also absorbs pen-change misregistration).

Not kept, and why: r01's reference-traced packets, fractions, softmax, V block, stage names and
backward row. The brief deletes them, and each was part of the schematic that W1 fails.

## Measurements / computations

All from `piece.self_check()` and a G-code analysis of v15:

| quantity | value |
|---|---|
| source separation d | 37 λ = 44.4 mm, λ = 1.2 mm (the hero's crest pitch) |
| fringes drawn | m = −24…24 (49 lines), asymptotes ≤ 40.5° |
| fringe check: max \|(r_Q − r_K) − mλ\| along every line | **4.3e−14 mm** (they are the exact hyperbolae) |
| pre-activation u = y(x_throat)/18 + 0.28 | −4.16 … +4.72 |
| h = tanh(u) at m = 0, ±6, ±12, ±18, ±24 | 0.273 · 0.816/−0.526 · 0.969/−0.909 · 0.997/−0.990 · 1.000/−1.000 |
| tanh′ = 1 − h² at the same m | 0.926 · 0.334/0.723 · 0.060/0.174 · 0.007/0.020 · 0.000/0.001 |
| gradient check: \|dL/du − central FD\| max | **6.1e−11** |
| mean gradient share (survival) | **0.275** → 6 of 21 crest circles on the backward sources |
| lines within one pen floor (0.8 mm) of an asymptote | 23 of 49 (13 top / 10 bottom: the bias) |
| sustained parallel crowding (< 0.8 mm, < 25°, other stroke; r01's metric) | blue 0.6 % · crimson 0.6 % · green 0.1 % · violet 1.1 % (r01 plate: ≈ 34 %) |
| black "crowding" 29 % | false positive: adjacent dots of one asymptote are separate strokes 1.0 mm apart |
| bbox | 10.5–199.8 × 13.4–258.0 mm inside the 10–200 × 10–287 drawable; 0 violations |
| `preview --score` | A · composition 0.939 · readability 0.982 · efficiency 0.631 |

## Plot budget

Model: draw F500 (the plate-job cap), pen-up travel 2000 mm/min, 2 s per pen cycle (1 s dwell each
lift and drop), 90 s per pen swap.

| # | pen | meaning | cycles | draw | travel | min |
|---|---|---|---|---|---|---|
| 0 | dodgerblue | K crest circles (21 + 6) | 40 | 1.55 m | 0.53 m | 4.7 |
| 1 | crimson | Q crest circles (21 + 6) | 40 | 1.56 m | 0.50 m | 4.7 |
| 2 | forestgreen | Z: fringe fan; ∂L/∂Z bell | 70 | 2.65 m | 2.02 m | 8.6 |
| 3 | darkviolet | FFN: squash, throat, fans (fwd + bwd) | 116 | 6.27 m | 3.59 m | 18.2 |
| 4 | black | ±1 asymptotes (198 dots), labels, title | 260 | 0.42 m | 0.97 m | 10.0 |
| | **total** | | **526** | **12.45 m** | **7.61 m (61 %)** | **46.2 + 7.5 swap ≈ 54 min** |

Suggested nib 0.3–0.4 mm. The crest pitch is 1.2 mm (the hero's), and the closest drawn neighbours
are 0.8 mm apart by construction.

## Self-critique

| dimension | score | why |
|---|---|---|
| hierarchy | 7 | one bundle across the full width. The ring field is the loudest colour mass and almost competes; the backward echo is clearly third |
| grid & alignment | 7 | one source column (x = 24), one gate (x = 86), one throat (116–143) shared by both bundles; title on the left frame |
| tension & asymmetry | 6 | cropped field left, cropped fans right, a lopsided squash. The two stacked bundles are still a calm, almost tabular pair |
| negative space | 7 | the lower-left quadrant and the wedge between the right fans are shaped by the forms |
| craft for pen | 8 | 1 % crowding, continuous round dots at 1.0 mm, one layer per pen, 526 cycles (from 3,725), every stroke batchable. Travel is still 61 % |
| concept legibility | 6 | the squash and the dying gradient read without a caption once seen. At first glance the pair still reads as "two transfer-function diagrams", a figure risk |
| depth | 4 | **declared flat.** Op Art line-family canon, the same flatness as *Current*; no occlusion or perspective |

**Single worst thing:** the two bundles are identical right of the gate. That is exactly true
(dL/do = 1), but it spends about 40 % of the violet ink repeating itself. A critic will call the
lower right fan redundant. The difference that carries the idea, the green bell and the missing
lines, sits in a 50 × 45 mm patch at the lower left.

## Engine requests

1. **Direction-aware `Occupancy`**: a `crowded(x, y, direction, cos_max)` so crossings survive and
   only near-parallel crowding pauses. Every interference piece in the family hand-rolls this
   (`_Guard` in r01, here a thin wrapper over the engine grid).
2. **`Scene3D.lines(..., min_run=, lock=(x0, x1))`**: drop resumed stretches too short to earn a pen
   cycle, and optionally keep a paused line paused through a stretch. Without it, pause-and-resume
   flickers into dashes where a family is crushed.
3. **A continuous-dot primitive in `engine/kit`**: round mark, fixed pitch, end-anchored. The
   resonance family now needs one pitch everywhere (Juan, 2026-09-28).
4. **Reversal-aware stroke ordering** in `postprocess.reorder_by_color` (as in resonance r05): it
   never reverses a stroke, which leaves travel at 61 % here.
