# ATTENTION AS TOPOGRAPHY — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/transformer/attention-topography` |
| current render | `gallery/neural-networks/transformer/attention-topography/promoted/pp_attention_axo2.png` (siblings in the same `promoted/` tier: `pp_attention_axo.png`, `pp_attention_v4.png`, `pp_attention_stack.png`, `pp_attention_dag.png`, `pp_attention_dag2.png`) |
| source | `promptplot/generative/pieces/ml.py::bauhaus_relevance` (studio wrapper: `studio/attention-dag/rounds/r01/piece.py::attention_dag`) · **the code has moved on**: the current docstring describes Q and K exploded sideways along two orthogonal axes around Q·Kᵀ, which is the `dag`/`dag2` layout, not the axo2 vertical stack; axo2 is an earlier state of the same function (the "isometric DIAMOND STACK" of `CLAUDE.md`) · brief: `studio/nets/transformer.md` |
| paper · pens | a4 portrait preview frame (INDEX records the gcode as 17x24), cream · 1 crimson = Q/K well floors, V terrain, V explosion lines, Q/K/V labels · 2 forest green = output terrain + "ATTENDED OUTPUT" · 3 black = Q/K and Q·Kᵀ planes, softmax rings, droplines, all other type · (pen 0 blue unused in axo2) |
| status | promoted tier on disk, **no recorded feedback** · 24 renders on disk |

## In one line
The attention computation drawn as a **stratified** exploded-axonometric stack — five
diamond plates on one vertical spine (Q/K wells → Q·Kᵀ similarity relief → softmax rings
→ V terrain → output peak), where the query·key anchor sites drop straight down through
every stratum as dashed droplines.

## What is on the sheet

### current — `pp_attention_axo2.png`
- **Dominant mass:** a vertical column of five isometric diamond plates on a shared
  axonometric basis, centred on u 0.47, filling v 0.12–0.89; each diamond ≈ 0.65 W wide
  (u 0.14–0.79). Five black dashed droplines (u 0.14, 0.42, 0.47, 0.52, 0.79) run from
  plate 1 down to plate 5 and tie the stack together.
- **Plate 1 (v 0.14–0.30), black mesh:** a flat 24×24 grid with two sunken wells whose
  floors are crimson zig-zag mesh — one at (0.42, 0.21), one at (0.52, 0.26). The plate's
  bottom vertex overlaps plate 2's top vertex at (0.47, 0.29), producing a small dense
  black lozenge knot where the two meshes coincide.
- **Plate 2 (v 0.29–0.45), black mesh:** a central peak at (0.47, 0.33) flanked by two
  crimson-capped bumps at (0.42, 0.32) and (0.52, 0.37).
- **Stage 3 (v 0.47–0.59):** no plate — only ~11 black closed contour rings, a two-lobed
  kidney centred (0.47, 0.52), ≈ 0.20 W wide, tightest rings at the centre; plus a stray
  black "<" wedge: two long lines from the left dropline at (0.14, 0.52) to (0.47, 0.44)
  and (0.47, 0.60) — the left half of a diamond whose right half is missing, so it reads
  as an arrowhead pointing left.
- **Stage 4 (v 0.59–0.69), crimson:** a small undulating V terrain displaced to the right
  (u 0.56–0.91), its right corner at the drawable margin. Four crimson dashed explosion
  lines run from its corners down-left to the green plate's corners.
- **Plate 5 (v 0.73–0.89), green:** a flat mesh with one sharp central spike at (0.47, 0.76).
- **Type** (all spaced-caps stroke font; the Q glyph renders like a "D"):
  - title `ATTENTION AS TOPOGRAPHY` centred (u 0.18–0.73, v 0.10); subtitle
    `QUERIES SHAPE CONTENT THROUGH CONTEXT` (v 0.14) — both centred.
  - crimson `Q QUERIES` (u 0.21, v 0.17) and crimson `K KEYS` (u 0.63, v 0.17) — K is in
    the same crimson as Q.
  - left column of numbered stage labels at u 0.12: `1 QUERY   KEY SPACES` (v 0.19),
    `2 DOT PRODUCT` (v 0.36), `3 SOFTMAX` (v 0.52), `5 OUTPUT` (v 0.79); stage 4's label
    sits right instead: `4VALUES V` (black, u 0.64, v 0.58, missing space) directly above
    crimson `V VALUES` (u 0.72, v 0.59) — a duplicated label.
  - right column at u 0.67–0.72: `TOKENS`, `DIMENSIONS`, `Q . K T`, `SIMILARITY` /
    `LANDSCAPE`, `SOFTMAX QK T` / `NORMALIZED` / `ATTENTION WEIGHTS`, `CONTENT TO` /
    `BE MIXED`, `SOFTMAX QK T V` / green `ATTENDED OUTPUT`.
  - footer `A  SOFTMAX QK T   Z   AV` (u 0.39–0.87, v 0.90) — the formulas with the `=`
    and `ᵀ` dropped.
- **Overlaps observed:** `1 QUERY KEY SPACES` and `TOKENS`/`DIMENSIONS` cut notches into
  plate 1's mesh (label halos) so its edges stair-step; `5 OUTPUT` sits on the green
  plate's left corner where a crimson dashed line enters; black droplines pass straight
  through the green mesh and the softmax rings.
- **Quiet zone:** the left third between plate 2 and plate 5 (u 0.14–0.40, v 0.46–0.72),
  crossed only by the wedge and a dropline; the band below the footer.

### siblings on disk (for the trail)
- `pp_attention_v4.png`: same stack, but V is a full-width crimson plate on the spine,
  blue dashed V-anchor droplines with small arrowheads, and crimson curved lines bowing
  from the plate-1 wells down to plate 2.
- `pp_attention_stack.png`: six plates on a flatter projection filling u 0.12–0.91,
  canvas grid with crimson arrows, one crimson Q·K patch, open softmax ellipses, green
  attention-map relief, black V, black output with a green inlay; green bar-chart `Z`
  bottom-left.
- `pp_attention_dag2.png`: the DAG layout — two wireframe landscapes top (crimson-tipped
  "Q LANDSCAPE" left, "K LANDSCAPE" right), triple parallel arrows (crimson, blue)
  converging on "Q K  THE INTERFERENCE", black triple arrows to a flat softmax ring
  ellipse, a green "THE ATTENTION MAP" peak, "V LANDSCAPE" black terrain right, green
  arrows into a black+green "OUTPUT" terrain, a green bar chart "Z". Title top-left in
  two lines, 4-pen swatch top-right.

## The science it encodes
Brief (`studio/nets/transformer.md`): Q and K collide to raise a similarity landscape,
softmax turns it into a distribution drawn as contour rings, V is a separate semantic
terrain, O = AV pulls V's terrain up where probability is high. Docstring
(`bauhaus_relevance`): "Peak sites and heights come from a real attention row
(checkpoint/GPT-2 via `weights`), so the terrain is data, not decoration." In code the row
is `_attention_matrix(...)` (seeded synthetic unless `weights=` is passed), normalised,
and the query with the largest max is taken; everything else — the well shapes, V
terrain, the output spike — is analytic Gaussian relief placed at those sites. On axo2
the chain is legible only as a stage sequence: the output spike does not visibly derive
from the V terrain (V is off to the side, its bumps don't match the spike), and the two
wells + peak are too symmetric to read as data. Treat axo2 as a **diagram of the
pipeline**, not a measured field.

## How it got here
From the candidates: `pp_bauhaus_attention_seed3_v2` (a ray fan from a blue spiral
"sink" disc on the left, GPT-2 sink chords — CURATION: REWORK, "ray fan is thin, lower-
left dead") → `pp_XFMR_TOPO_v1–v3` (a five-layer 3D relief stack: canvas grid with
crimson arrows, three deep cones, open softmax ellipses, smooth V sheet, output sheet; the
first "AS TOPOGRAPHY" composition, dense and heavy, labels collide with mesh) →
`pp_XFMR_basin_v*` (one black terrain with crimson peaks above and a blue well below —
single-field thesis, most sculptural, lots of dead lower sheet) → the engine reorg
(Scene3D) produced the promoted set: `stack` (6 plates, flatter) → `v4` / `axo` / `axo2`
(the diamond stack; axo2 moves V off the spine and adds crimson explosion lines) →
`dag` / `dag2` (the landscapes exploded apart, joined by triple arrows). The code now
builds the dag family. Gained: a shared projection basis, occlusion-correct meshes,
anchors carried through every stage. Lost: the mass and drama of the XFMR_TOPO cones and
the basin's single sculpted field. No feedback in `studio/feedback.jsonl`.

## Keep — what works
- The single shared axonometric basis: all five plates are the same diamond, so the
  stack reads as one object and the vertical rhythm (plates every ≈ 0.16 H) is exact.
- The droplines: five dashed verticals carrying the query·key anchor sites through every
  stage are the plate's best idea — the same x means the same token all the way down.
- Crimson as the scarce accent inside black structure: the crimson well floors on plate 1
  and caps on plate 2 are small and loud.
- The green output spike at (0.47, 0.76) on its flat plate — the single cleanest form on
  the sheet; the green pen appears nowhere else except its label.
- The quiet left third between plates 2 and 5 — open paper that lets the stack breathe.

## Weak — what doesn't
- [concept] It is a textbook pipeline — five numbered stages with labels on both sides,
  a formula footer, and a wedge that reads as an arrow. § 6 NO SCHEMATICS: a slide on
  "how attention works". The abstract order is "stack of stages", which names a diagram.
- [concept] The data claim doesn't show: symmetric Gaussian wells, a V terrain unrelated
  to the output spike. O = AV is asserted by the labels, not by the geometry.
- [hierarchy] Five plates of equal size and weight; no dominant element. The output spike
  is small; the busiest plate (1) is at the top where it competes with the title.
- [tension] Centred title, centred subtitle, centred stack on a centred spine; V's
  sideways shift is the only asymmetry and it pins V against the right margin.
- [space] The overlap of plate 1's bottom vertex with plate 2's top vertex at
  (0.47, 0.29) is collision, not composition — a dense knot a few mm of spacing would
  remove. The stray "<" wedge at stage 3 is a leftover half-plate.
- [craft] Label halos notch plate 1's mesh (stair-stepped holes at the left edge and at
  `TOKENS`/`DIMENSIONS`); `5 OUTPUT` sits on a plate corner under a crimson dashed line;
  droplines are drawn through the green mesh and the softmax rings (ink-on-ink).
- [craft] Type: the Q glyph reads as D (`D QUERIES`, `D . K T`), `4VALUES V` is missing a
  space, V is labelled twice, `ᵀ`/`=` drop out of every formula. Hairline caption type
  throughout — the lab-figure default.
- [craft] K is drawn in crimson like Q even though the brief assigns K blue; the blue pen
  exists and is unused.
- [depth] The 3D is real (axonometric meshes with hidden lines) but every plate is almost
  flat; depth comes only from stacking, not from form.

## Next versions
1. **one field** (abstract) — collapse the pipeline into a single similarity **field**
   (legitimate here: attention IS a field over key space) seen once, large: the Q·Kᵀ
   relief of one real query row as the dominant mass at ≈ 0.8 W, cropped off the right
   frame, the softmax as a waterline that floods everything below it, V as the ground
   texture and O as what survives above the water. The basin trial's sculptural single
   form with the droplines' honesty. One plate, one idea, a real quiet zone.
2. **the sink tower** (mechanism) — keep the stack but make it the real 12 GPT-2 layers of
   one head, drawn as strata whose peaks all migrate onto token 0 as depth increases
   (the attention sink); the dropline at token 0 becomes the loud crimson column. The
   stack then encodes a phenomenon, not a procedure, and has a dominant element.
3. **Q meets K** (lens) — only the collision: the Q landscape and the K landscape as two
   interpenetrating meshes (red and blue, true 3D occlusion) whose intersection curve —
   where they are equal — is drawn black and heavy. The twist: attention is where two
   landscapes meet; no stages, no labels but the title.

**If only iterating:**
1. Separate plates 1 and 2 by ≥ 6 mm at their shared vertex so the knot at (0.47, 0.29)
   disappears, and delete the stray "<" wedge at stage 3.
2. Draw K in the blue pen (label and the K well floor) so Q and K are distinguishable,
   fix the Q glyph, and remove the duplicate `4VALUES V` label.
3. Make the output spike the dominant mass: scale plate 5 to ≈ 0.9 W and let it crop
   the bottom and left frame, with the four upper plates shrunk to ≈ 0.45 W stacked above
   its peak.
