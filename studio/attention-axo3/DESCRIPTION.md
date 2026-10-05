# ATTENTION AS TOPOGRAPHY (axo3, ALIGNED) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/attention_axo3` |
| current render | `gallery/studio/attention_axo3/current/pp_attention_axo3_ALIGNED.png` (png only — no gcode paired) |
| source | **none on disk** as a live function. It is the "diamond-stack v4" of `promptplot/generative/pieces/ml.py::bauhaus_relevance` from git commit `32c9857` (2026-09-15, "attention diamond-stack v4"); the text strings `ATTENDED OUTPUT` / `CONTENT TO BE MIXED` / `KEY SPACES` no longer exist in the working tree — the function has since been rebuilt as the exploded version in `studio/attention-dag/`. Recover with `git show 32c9857:promptplot/generative/pieces/ml.py`. |
| paper · pens | 17 × 24 cm portrait (170 × 240 mm), cream · 1 crimson = Q/K wells, V terrain, explosion lines · 2 forestgreen = output terrain + `ATTENDED OUTPUT` · 3 black = plates, contours, spine, all type (no blue pen in this render) |
| status | unreviewed (no FEEDBACK.md) · 1 render on disk |

## In one line
Attention as a **tight isometric diamond stack** (stratified planes on one vertical axis) — five hidden-line plates from "query/key spaces" through dot product, softmax contours and values to a green attended-output peak, tied together by dashed droplines through the Q/K anchor columns.

## What is on the sheet
Reading top to bottom; the stack occupies u ≈ 0.14–0.78 (plate width ≈ 0.65 W), each plate a flat rhombus ≈ 0.10 H tall.

- **Title block** (v ≈ 0.11–0.13): `ATTENTION AS TOPOGRAPHY` in spaced caps (u 0.34–0.83), under it `QUERIES SHAPE CONTENT THROUGH CONTEXT`. Two crimson labels, `Q QUERIES` (u 0.35–0.44) and `K KEYS` (u 0.64–0.72), are **printed directly on top of the subtitle line** — overprint.
- **Plate 1** (v ≈ 0.15–0.25): a dense black wire grid with two elliptical wells cut into it, each holding a small crimson zig-zag mesh — left well at (0.40, 0.19), right well at (0.51, 0.22). Left label `1 QUERY     KEY SPACES` (u 0.08–0.41, v 0.17) runs into the plate's back edge; right labels `TOKENS` (0.67, 0.18) and `DIMENSIONS` (0.67–0.78, 0.22), the latter touching the plate's right corner.
- **Plate 2** (v ≈ 0.30–0.41): black wire surface with one central ridge/hill rising in the middle and the two crimson patches repeated at (0.38, 0.33) and (0.52, 0.37). Labels `2 DOT PRODUCT` (left, v 0.33), `Q . K T` (right, v 0.33), `SIMILARITY` / `LANDSCAPE` (right, v 0.40–0.41).
- **Plate 3** (v ≈ 0.47–0.57): an empty rhombus outline holding a set of ~12 **nested black contours**, horizontally elongated and lobed, centred at (0.46, 0.52), innermost rings nearly touching (dense core). Labels `3 SOFTMAX` (left), `SOFTMAX  QK  T`, `NORMALIZED`, `ATTENTION WEIGHTS` (right, v 0.49–0.53) with a short black leader crossing into the plate edge.
- **The long gap** (v ≈ 0.58–0.68): only the five dashed black verticals of the spine (at u ≈ 0.14, 0.41, 0.46, 0.51, 0.78) cross it.
- **V terrain (crimson)** hung out to the right, off the stack's axis: a flat crimson wire plate at u ≈ 0.56–0.92, v ≈ 0.69–0.75, beyond the stack's right edge. Two overlapping labels: black `4VALUES  V` (missing space, v 0.65) and crimson `V  VALUES` just right and below it. Four dashed crimson explosion lines run down-left from its corners to the output plate.
- **Plate 5 — output (green)** (v ≈ 0.79–0.88): a full green wire plate with one soft green peak at (0.46, 0.81). Labels `5 OUTPUT` (left, v 0.82), `CONTENT TO` / `BE MIXED` (right, v 0.78–0.79, belonging to V), `SOFTMAX  QK  T  V` (v 0.81) and green `ATTENDED OUTPUT` (v 0.82).
- **Footer formula** (v ≈ 0.89): `A    SOFTMAX  QK  T     Z     AV` — the `=` signs and parentheses are missing, and the green plate's front apex overprints the formula near `SOFTMAX`.
- **Quiet zones:** the lower 0.10 H of the sheet (v 0.90–0.96) and the left column below `5 OUTPUT`.

## The science it encodes
Per commit `32c9857`'s message: 1 QUERY+KEY SPACES (one sheet, two red wells) · 2 DOT PRODUCT similarity landscape · 3 SOFTMAX rings · 4 VALUES (full red terrain) · 5 OUTPUT (green attended peak); dashed Q/K anchor droplines; formulas as halo labels. Q and K anchors are the two wells; the droplines through them are meant to show the same query/key positions persisting through every stage. On the sheet the softmax contours do show one sharp core (peaked), but nothing shows normalisation, and Q and K are the **same colour and the same well shape** — they read as twins, the exact failure later briefs call out. Whether the terrains are real attention or seeded cannot be told from the render.

## How it got here
Single render, no trials in the gallery. It is an ancestor of `studio/attention-dag` (the exploded version replaced it in the package). Notable relative to the successor: it uses a single wide plate width and one axis for everything (more compact), puts V off-axis to the right, and uses green for the output — later versions moved to blue K / crimson Q / gold V. The file name `ALIGNED` suggests this was the version where the droplines were aligned to the Q/K anchors. No Juan feedback.

## Keep — what works
- The **softmax contour nest** at (0.46, 0.52) — a lobed, elongated set of rings tightening into one core is the most drawn, least schematic mark on the sheet.
- **Wells cut into plate 1** (0.40, 0.19) and (0.51, 0.22): the surface visibly dips where Q and K sit — a genuine hidden-line effect.
- **Droplines** through the Q/K anchor columns (u 0.41, 0.51) connect every stage without arrows.
- The green output peak at (0.46, 0.81) as the one colour-change at the bottom gives a clear terminal.

## Weak — what doesn't
- [concept] Numbered stages, labelled plates, a formula footer: a textbook figure. Rubric §6 NO SCHEMATICS fails outright.
- [craft] Type collisions everywhere: `Q QUERIES`/`K KEYS` over the subtitle, `1 QUERY KEY SPACES` into plate 1, `4VALUES V` + `V VALUES` duplicated and overlapping, footer formula under the green plate apex, missing `=` in the formula.
- [hierarchy] Five plates of identical width and height stacked at equal pitch — no dominant element; plate 3's outline and plate 2's mesh have the same visual weight.
- [tension] Symmetric centred stack; only the V plate breaks the axis, and it reads as ran-out-of-room rather than a decision.
- [concept] Q and K are both crimson zig-zag patches in identical wells — twins; nothing about their geometry says "query direction" vs "key field".
- [space] The 0.10 H gap between plate 3 and plate 5 is leftover: only dashed rules cross it, while text crowds the right edge at v 0.78–0.82.
- [depth] Plates never overlap or occlude one another; the depth is per-plate only.

## Next versions
1. **contour-only** (abstract) — Promote the one mark that works: a single large softmax contour nest filling 60 % of the sheet, built from the real score row with `even_contour_levels()`, its rings pulled toward the winning key. Q and K become two differently-shaped wells (a directional groove vs a scattered field of pits) that the rings flow out of; V is not drawn at all — only the green output peak where the rings close. Order: **flow-to-attractor**. One dominant mass, no stack, no numbers.
2. **folded-sheet** (lens) — Make the stack ONE continuous sheet folded like paper: plate 1 bends down into plate 2 into plate 3, so the stages are a single surface with creases (the operations), drawn with hidden-line occlusion where folds overlap. Depth by occlusion instead of dashed droplines; the fold at softmax is the tightest crease.
3. **faithful-cleaned** (faithful) — Keep the diamond stack but fix it as a record: blue K / crimson Q / gold V / green Z, distinct well geometry for Q and K, V hung on the stack's axis rather than off to the right, all labels on one right-hand column clear of every plate, formula with its `=` signs restored, and plate heights varied by stage importance (softmax plate twice as tall).

**If only iterating:**
1. Move every label to a single column at u ≥ 0.82 with nothing touching plate edges, and delete the duplicate `4VALUES V` label.
2. Recolour K blue and give the K well a different shape (a line of small pits) from the Q well (one oriented groove).
3. Double the softmax contour nest's size and let it break out of its rhombus outline — it becomes the dominant element.
