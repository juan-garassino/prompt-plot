# ATTENTION AS TOPOGRAPHY — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/attention_DAG` |
| current render | `gallery/studio/attention_DAG/current/pp_attention_DAG_landscape.png` · `gallery/studio/attention_DAG/current/pp_attention_DAG_portrait.png` |
| source | `studio/attention-dag/rounds/r01/piece.py::attention_dag` → thin wrapper around `promptplot/generative/pieces/ml.py::bauhaus_relevance` |
| paper · pens | A4 landscape (and A4 portrait variant), cream · 0 dodgerblue = K landscape · 1 crimson = Q landscape (+ red peaks re-appearing on Q·Kᵀ and output) · 2 gold = V landscape (+ gold patches on output) · 3 black = computation spine, plates, all type |
| status | unreviewed (no FEEDBACK.md) · 3 renders on disk (2 current, 1 trial) |

## In one line
Scaled dot-product attention drawn as an **exploded axonometric stack of terrains** (nested/stratified planes on a vertical spine) — each stage (Q·Kᵀ, softmax, attention map, output) is a hidden-line height-field plate on a black spine, with Q, K and V as coloured terrains exploded sideways along world axes. The landscape and portrait renders are the same composition refit to the two orientations; portrait stretches the spine and leaves more air between stages.

## Lede
The attention step inside a transformer drawn as **an exploded stack of terrains**: each stage is a landscape plate on a vertical spine, with queries, keys and values entering from the sides.

## On the sheet
Four black rhombic plates stack down the centre, joined by dashed vertical rules: the query-key product with crimson peaks, an empty softmax plate, a gridded attention map with one needle spike, and a mesh output plate with gold and crimson patches. Crimson, blue and gold terrains float to the sides, tied in by dashed lines. Stage labels run down the left edge; the portrait version spreads the stages further apart.

## The science
Black marks the computation and colour marks what enters it, following attention's flow from query-key scores through softmax and the attention map to the output. Peak positions come from a synthetic example, not a trained model. The three coloured terrains are procedural shapes made to look distinct. That softmax rows sum to one is only stated in a text label.

## What is on the sheet

### Landscape (`pp_attention_DAG_landscape.png`, A4 297 × 210)
- **The spine (dominant mass, centre).** Four rhombic plates stacked on one vertical axis at u ≈ 0.40–0.60 (plate width ≈ 0.20 W), joined by three vertical dashed black rules (the plate's left corner, centre and right corner) running from v ≈ 0.37 to v ≈ 0.84:
  1. **Q·Kᵀ plate** (v ≈ 0.27–0.37): black wire-mesh terrain with a cluster of sharp crimson peaks rising out of its centre (peaks reach v ≈ 0.22). Label `Q . K T` above it at (0.50, 0.18) — the transpose is set as a detached spaced `T`, not a superscript.
  2. **Softmax plate** (v ≈ 0.39–0.48): an empty black rhombus outline, nothing inside except one tiny over-inked black ellipse at its centre (≈ 3 mm). Right label `ROWS SUM TO 1` at (0.73–0.86, 0.43).
  3. **Attention map plate** (v ≈ 0.62–0.70): a gridded black plate, front half solid grid, back half broken into dashes, with **one needle spike** (white-filled, black-outlined) at the centre rising to v ≈ 0.59. Label `ATTENTION MAP A` at (0.47–0.65, 0.53).
  4. **Output plate** (v ≈ 0.79–0.88): black mesh terrain with a gold patch (left/centre) and a crimson patch plus a small crimson spike (right of centre) sitting in it; small blue fragments at its front-left edge. Label `Z = A V` below it at (0.48–0.55, 0.90).
- **Exploded coloured terrains (second read).**
  - `Q LANDSCAPE` (crimson, label at (0.21–0.28, 0.14)): one broad smooth Gaussian hill in a dense crimson wire-mesh, plate at u ≈ 0.22–0.42, v ≈ 0.20–0.30 (≈ 0.20 W). Dashed crimson explosion lines run from its corners down-right to the Q·Kᵀ plate.
  - `K LANDSCAPE` (blue, label at (0.63–0.73, 0.14)): a spiky many-peaked blue terrain, plate at u ≈ 0.58–0.78, v ≈ 0.20–0.29; dashed blue explosion lines down-left to Q·Kᵀ. Q and K sit mirrored across the spine at the same height.
  - `V LANDSCAPE` (gold, label at (0.63–0.73, 0.49)): a broad ridged gold terrain at u ≈ 0.58–0.78, v ≈ 0.53–0.62, with two dashed gold lines running down-left into the attention-map plate's right corner.
- **Left stage column** at u ≈ 0.05, each a numeral + spaced-caps label: `1 QUERY AND KEY` (v 0.33), `2 SOFTMAX` (v 0.44), `3 ATTENTION MAP` (v 0.67), `4 OUTPUT` (v 0.83). In the stroke font the Q reads as `D`/`O` (`DUERY`).
- **Title block** top-left-centre: `ATTENTION AS TOPOGRAPHY` (spaced caps, u 0.13–0.52, v 0.07) and `QUERIES SHAPE CONTENT THROUGH CONTEXT` (small spaced caps, v 0.09).
- **Footer** bottom-right: `A = SOFTMAX(QK T)     Z = AV` at (0.62–0.96, 0.94).
- **Quiet zones:** the whole left third below the title except the four stage labels; the right third between K and V (v 0.32–0.47) and below V (v 0.66–0.90).

### Portrait (`pp_attention_DAG_portrait.png`, A4 210 × 297)
Same elements, same labels, same pens. Q and K plates widen to ≈ 0.28 W each and nearly touch the side margins (u 0.10–0.38 and 0.62–0.92, v ≈ 0.18–0.27); the spine is ≈ 0.28 W wide at u 0.37–0.65. Stage gaps grow: Q·Kᵀ at v ≈ 0.28–0.33, softmax rhombus v ≈ 0.39–0.46, attention map v ≈ 0.61–0.67 (here the grid is solid black on both halves, reading as a dark slab), output v ≈ 0.80–0.86. V LANDSCAPE sits right at u 0.62–0.92, v 0.55–0.63. The long empty dashed spine between softmax and attention map (≈ 0.15 H) is the biggest void.

## The science it encodes
From the `bauhaus_relevance` docstring (`promptplot/generative/pieces/ml.py` ≈ l.2328): black is the computation spine, colour is what enters it; Q and K are exploded out along two orthogonal world axes from Q·Kᵀ, V enters the attention map from the same side as K, output Z returns to the spine. Peak sites and heights come from an attention row (`_attention_matrix`): **with `weights=""` (the default the wrapper uses) that row is a seeded synthetic head over sinusoidal positional encodings, not GPT-2** — so the terrain is "data" only in that weak sense. The Q/K/V landscapes themselves are procedural height fields (one smooth Gaussian, one spiky multi-peak, one ridge), i.e. decoration shaped to be distinguishable. On the sheet: the softmax is shown as an empty plate with a dot, and the "attention map" is a single needle — the claim that rows sum to 1 is only stated in text (`ROWS SUM TO 1`), not visible as geometry.

## How it got here
One trial (`trials/pp_attention_DAG_landscape.png`) → current landscape. Changes: the subtitle and `Q LANDSCAPE` label used to collide (the crimson label printed over `SHAPE CONTENT THROUGH`) — now separated; `ROWS SUM TO 1` moved from under the Q·Kᵀ plate to the right of the softmax plate; the attention-map grid, formerly a dense solid black slab, now has its back half dashed; Q and K plates pulled slightly inward and down. Gained: legibility of labels, less black mass. Lost nothing notable. No Juan feedback. The family has been explicitly ruled out as a model by the newer attention plates (`attention-passes` r03 NOTES lists "exploded axonometric stack of planes, droplines, numbered stage labels flush left" as the move to avoid).

## Keep — what works
- The **hidden-line wire-mesh terrains** are well crafted: the crimson Q hill at (0.32, 0.25) and the spiky blue K field at (0.68, 0.24) read as solid surfaces with real occlusion — the one area where depth is earned.
- **Colour as provenance**: crimson peaks re-surfacing inside the black Q·Kᵀ plate (0.50, 0.30) and gold/crimson patches inside the output plate (0.50, 0.85) show "what entered" without arrows.
- The **needle spike** on the attention-map plate (0.50, 0.63) is the loudest single mark and correctly says "peaked".
- Dashed explosion lines are parallel to the axis each plate moved along, never arrowheads.

## Weak — what doesn't
- [concept] It is a textbook figure: numbered stages 1–4, labelled boxes on a spine, formulas in the footer. Rubric §6 NO SCHEMATICS — this would sit in a slide deck unchanged. Score ≤ 3 on concept.
- [hierarchy] Four plates of equal width stacked with even gaps plus three coloured plates of the same size — seven elements at one scale; nothing dominates at 3 m.
- [tension] Dead-centre vertical spine with Q/K mirrored left/right across it: centred-symmetric, the rubric's "student work" failure.
- [space] The softmax plate (0.50, 0.44) is an empty rhombus with a blot — the stage that the whole mechanism turns on is the emptiest mark on the sheet. In portrait the 0.15 H dashed gap under it is leftover, not shaped.
- [grid] Left stage labels at u 0.05 share no line with the plates they name except by row; the footer formula floats bottom-right; title is not on the spine's axis or the label column.
- [craft] The softmax centre "dot" is an over-inked ellipse; the Q glyph reads as D (`DUERY`, `D LANDSCAPE`); `Q . K T` and `QK T` set the transpose as a loose spaced T; faint travel lines criss-cross the whole sheet in preview.
- [concept] The data is synthetic by default and the Q/K/V terrains are procedural — the numbers do not drive the forms the viewer sees.
- [depth] Depth exists per plate, but the stack itself is flat-read: plates don't overlap or occlude each other.

## Next versions
1. **one-terrain** (lens) — Drop the stack. Draw only the similarity field S = Q·Kᵀ/√d as ONE large hidden-line terrain filling 70 % of the sheet, cropped at the frame, with the softmax shown as the same surface re-levelled (exp then normalised) so the one surviving peak towers and every other hill sinks below a waterline drawn as bare paper. Order: **flow-to-attractor / a flooded landscape** — softmax is the tide that drowns everything but the peak. Dominant mass, real overlap, depth by occlusion, and the mechanism (normalisation destroys scale) becomes visible geometry rather than a label.
2. **strata** (abstract) — Transpose to a **laminar / stratified** order: each stage becomes one geological layer of a single cross-section, Q and K as two tilted beds that fold into each other, softmax a thin compressed bed (the waist), V an intrusion, Z the top soil. No labels beyond a caption; the thickness of each bed is a real number (entropy per stage). Asymmetric, cropped, no spine.
3. **faithful-real** (faithful) — Keep the exploded axonometric but make it honest and composed: drive every terrain from real GPT-2 Q/K (the cached `~/.promptplot/attn_gpt2.npz`), replace the empty softmax rhombus with the actual 15 × 15 attention matrix as a terrain whose rows visibly sum to one (row ridges of equal volume), push the spine off-centre to u ≈ 0.62 with Q exploding far left and cropping at the frame, and cut the numbered stage column.

**If only iterating:**
1. Fill the softmax plate (0.50, 0.44) with the real row distribution as a terrain or ring field — no empty rhombus, no blob.
2. Move the spine to u ≈ 0.60 and let the Q LANDSCAPE grow to ≥ 0.35 W and crop at the left frame, so one element dominates and the symmetry breaks.
3. Delete the `1 … 4` stage column and the footer formula; keep only the title and the three coloured plate names, fixing the Q glyph so it no longer reads as D.
