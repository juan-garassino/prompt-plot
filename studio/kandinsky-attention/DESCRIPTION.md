# ATTENTION AS RESONANCE / POINT AND LINE TO PLANE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/kandinsky_attention` |
| current render | `gallery/studio/kandinsky_attention/current/pp_kandinsky_attention_corrected_v1.png` · `gallery/studio/kandinsky_attention/current/pp_kandinsky_attention_abstract_v1.png` |
| source | corrected: `studio/kandinsky-attention/rounds/r01/piece.py::kandinsky_attention` · abstract: `studio/kandinsky-attention/rounds/r02/piece.py::kandinsky_attention` (no NOTES.md in either round, although r01's docstring points to one) |
| paper · pens | 24 × 30 cm portrait (240 × 300 mm), cream · 0 black = grid, rings, rules, circle, type · 1 crimson = Q (argmax frames, entropy bars / the tracks) · 2 dodgerblue = K (received-mass spirals / argmax ticks) · 3 goldenrod = V (texture swatches / rim values + top-3 plane) · 4 forestgreen = Z (bar outlines / output discs) |
| status | unreviewed (no FEEDBACK.md) · 2 renders on disk, no trials |

## In one line
Real GPT-2 attention (layer 4, head 7) drawn two ways — **corrected** is an **apportioned lattice** (a causal 8 × 8 grid where every query row spends exactly eight concentric rings and every output bar is one unit long, textured by the values it bought), **abstract** is a **radial walk of conserved length** (after Kandinsky's "a line is the track of a moving point": each of 15 query rows is a crimson track of 15 steps whose lengths are its weights, so every track is 80 mm and only its endpoint — the output — differs).

## Lede
Real GPT-2 attention drawn in Kandinsky's language: **every query spends exactly one unit of attention**, shown as rings in a grid and as a track of fixed length.

## On the sheet
One version is a large triangular grid of black spirals at the centre, with crimson bars down its left side, blue spirals along the top, gold hatched swatches and green bars beneath. The other is a big black dial with gold marks around the rim, a gold triangle across it, a tangle of crimson tracks at the middle and green discs at the track ends.

## The science
Both use attention weights from GPT-2 small, layer 4, head 7. Each row of weights sums to one, so what a query pays to each value is drawn as ring counts or step lengths. Crimson is queries, blue is keys, gold is values, green is outputs. The reading of Kandinsky is an analogy, not a derivation.

## What is on the sheet

### corrected v1 (r01) — `ATTENTION AS RESONANCE`
- **Title band:** heavy spaced giant caps `ATTENTION AS RESONANCE` across u 0.05–0.94 at v 0.07, underscored by a thick black rule the full width at v 0.09.
- **K row (blue)** at v 0.14: eight blue spirals `k0`…`k7` (labels above at v 0.10) spaced across u 0.22–0.77 — `k0` large (≈ 12 mm), the rest ≈ 3–5 mm. Big outline `K` at (0.84, 0.15) with `received mass` under it. Big outline crimson `Q` at (0.08, 0.15) with `bits of doubt` under it.
- **The grid (dominant mass)** u 0.18–0.81, v 0.17–0.67 (≈ 0.63 W): a **lower-triangular** 8 × 8 lattice of 19 mm square cells, its upper-right edge a heavy black staircase (the causal mask). Every cell holds a black concentric spiral whose size/ring count is the weight — large in column k0 for rows q0–q2 and on the diagonal for q3–q7, tiny dots elsewhere. The argmax cell of every row is framed by a **crimson square** (q0–q2 on k0, then the diagonal). The q0 cell is crossed by a black X. Row labels `q0`…`q7` in crimson at u 0.05.
- **Entropy strip** left of the grid (u 0.08–0.17): one crimson triple-line bar per row, length = entropy, against two dotted verticals, scale `2  1  0` / `H bits` at v 0.67–0.69.
- **The masked triangle as a text field** (upper right of the grid): `S = QKᵀ / √d_k` (0.44–0.62, 0.23), `j > i`, `masked to minus infinity` (v 0.28–0.31), `every row : eight rings` / `apportioned by weight` (v 0.33–0.35) — the second line runs into the top of the **q7 dial**: a black circle Ø ≈ 36 mm centred (0.62, 0.33) with a crimson triple arc over its left half, crimson `q7` inside, small black tick bundles on the lower-right rim, and `one unit` under it (0.55–0.61, 0.39).
- **Caption line** v 0.66: `A = softmax ( S )   one distribution per query, not one curve per sheet`.
- **V swatches (gold)** at v 0.70–0.73: eight small textured rectangles across u 0.27–0.73 — horizontal hatch, vertical, /, \, crosshatch, dots, dashes, waves — labelled `v0`…`v7`. Outline gold `V` at (0.12, 0.72), `eight values` / `eight textures` below.
- **Z bars** v 0.77–0.94: eight green-outlined bars of identical length (u 0.27–0.73), each filled left-to-right with the value textures in segments proportional to that row's weights (`z0` all horizontal hatch; later rows mixing up to six textures). Rows `z2` and `z3` have **blank white wedges** where a diagonal-hatch segment ends in a triangle instead of filling its span. The last bar `z7` is **overprinted** by black text `one unit of attention . every bar is this long`; a black bracket under it marks the length.
- **Lower-right block:** outline green `Z` + `= AV` (0.86–0.95, 0.83), `one row` / `per query` (green), then black `gpt-2 small` / `layer 4 head 7` / `d k 64   root d k 8` / `n 8 queries 8 keys` (0.86–0.97, 0.90–0.96).
- **What is absent:** none of the reference's flat colour planes — no triangles, no discs, no quadrants, no diagonal black rules. The Kandinsky idiom survives only as the textured swatches.

### abstract v1 (r02) — `POINT AND LINE TO PLANE`
- **Title:** giant outlined caps `POINT AND LINE` / `TO PLANE` flush-left, u 0.04–0.79, v 0.03–0.17. Right of `TO PLANE` a 3-line caption (u 0.61–0.97, v 0.15–0.22): `A LINE IS THE TRACK MADE BY THE MOVING POI…` / `KANDINSKY 1926 · AND ONE ATTENTION ROW IS` / `FIFTEEN STEPS OF EXACTLY ONE UNIT OF STRIN…` — lines 1 and 3 are **truncated at the right margin** with garbled glyph fragments.
- **The dial (dominant mass):** a black double-line circle Ø ≈ 160 mm (0.67 W) centred (0.48, 0.50), a dotted inner circle (the mean reach, r ≈ 52 mm), 15 slots numbered `0`–`14` around the rim starting at the upper right. At each slot a **gold mark** sized by the value's received mass — concentric rings (shared value) or a sunburst (owned value): a big ring mandala at slot 0 (0.64, 0.27, Ø ≈ 28 mm) and a medium one at slot 4 (0.17, 0.39); small bursts elsewhere. Short **blue ticks** outside the rim at the slots some query picks as argmax. Dotted black radial stubs from rim marks inward.
- **The top-3 plane (gold):** a large triangle with vertices at slots 0, 4 and 9 — (0.65, 0.27), (0.17, 0.39), (0.51, 0.77) — filled with horizontal gold hatch at ≈ 4.6 mm; the hatch is cut away around the centre so it stops short of the knot.
- **The tracks (crimson):** 15 polylines leaving the centre (0.48, 0.50), each a chain of short steps with small dots at the joints; several shoot out long (to slot 0's mandala, toward slots 4, 9, 12), most **knot into a tight tangle within ≈ 15 mm of the centre** — the densest zone on the sheet.
- **The outputs (green):** 15 small green spiral discs at the track endpoints, joined in query order by a **green dashed polyline** that zig-zags across the dial (u 0.19–0.65, v 0.27–0.68).
- **The heavy ray (black, 3 passes):** from the centre straight up to the top frame at u ≈ 0.51, **cutting through `AND` in the title**; its dotted back-continuation runs down through the footer to the bottom margin.
- **Footer** v 0.83–0.91, three columns under spaced heads `THE ORDER` / `MEASURED` / `READ` with rules. Body text overruns column boundaries — e.g. `step j of row i runs 80 x a(i,j)` collides with `peak share`, `every track is the` with `uniform row`, `max 1.000` with `gold`, `sum a(i,j) v j` with `value 0 takes 4.23 of 15.0 units` — and the `READ` column runs past the right margin into scribbled glyphs at u 0.97–0.99. Bottom line (v 0.96): `GPT-2 SMALL · LAYER 4 · HEAD 7 · 15 TOKENS · EVERY TRACK BEGINS AT THE CENTRE AND NONE ENDS` also running into the right-margin scribble.

## The science it encodes
- **Data (both):** `~/.promptplot/attn_gpt2.npz`, GPT-2 small **layer 4, head 7** (chosen in r01 for showing both a hard attention sink on k0 — rows 0–2 — and a self/previous-token diagonal — rows 3–7). r01 docstring: the 8 × 8 crop is exact because GPT-2 is causal (row q has support only on j ≤ q), rows still sum to 1 (asserted), d_k = 64, √d_k = 8.
- **corrected (r01 docstring):** order = APPORTIONMENT — every query spends one unit, drawn as **exactly eight rings per grid row** via largest-remainder (Hamilton) apportionment so counts sum to the budget, and **one bar length per output row** filled by value textures in proportion a(i,j). It explicitly corrects the reference's errors listed in the brief: per-row softmax (a matrix, not one curve), peaked not uniform, Z has one row per query (8 = 8), grid = n_q × n_k. On the sheet this is legible: the crimson frames trace sink-then-diagonal, and every Z bar is the same length. The promised NOTES.md audit list does not exist on disk.
- **abstract (r02 docstring + code):** each row i is a track of 15 steps, step j of length 80·a(i,j) mm toward slot j's direction, so every track has total length 80 mm (row sums to 1) and its endpoint is z(i) = Σ a(i,j)·v_j with v_j the slot's unit vector. Gold mark size = column mass m_j; rings vs burst = concentration c_j (> 0.5 → owned); blue ticks = argmax; the gold triangle = the three heaviest values; the heavy black ray = the direction of the mean output z̄. Footer's measured numbers: peak share mean 0.587, max 1.000; uniform row would be 0.067; reach |z| 1.00 at row 0 down to 0.35; mean reach 0.709; value 0 takes 4.23 of 15.0 units. On the sheet the equal-length claim is not visually checkable (tracks fold back on themselves into the knot).

## How it got here
Two independent first rounds, one render each, no trials. r01 took the brief's "corrected recreation" route and dropped the reference's colour-block furniture in favour of a correct matrix; r02 abandoned the reference and went to a Kandinsky-text pun (Bauhaus Book 9) with a radial order. No Juan feedback.

## Keep — what works

### corrected v1
- The **lower-triangular grid with the heavy staircase mask** (0.18–0.81, 0.17–0.67) and the **crimson argmax frames** tracing sink → diagonal: the head's behaviour reads in one glance and is true.
- **Eight rings per row** — a strong, exact resonance mapping (ring budget is the probability mass).
- **Equal-length Z bars textured by value** (0.27–0.73, 0.77–0.94): "one unit of attention per query" made physical; texture as the value's identity is a genuinely Kandinsky-adjacent move.

### abstract v1
- **The concept and the twist**: Kandinsky's definition of a line applied to an attention row — every track the same length, only the endpoint differs. Wit, not earnestness.
- The **gold mandala at slot 0** (0.64, 0.27) as the loud sink, with the top-3 hatched triangle as the one flat colour plane — the only element that sounds like Kandinsky.
- One dominant mass (the dial) with a clear second (title) and third (footer).

## Weak — what doesn't

### corrected v1
- [concept] It is a matrix figure with a legend: labelled rows/columns, swatch key, formula, caption, specs block — §6 NO SCHEMATICS fails. The brief's Kandinsky idiom (flat planes, triangles, discs, cutting diagonals) is absent.
- [tension] Everything is on an orthogonal grid, centred columns, no diagonal — no tension device at all.
- [craft] Blank wedges inside `z2`/`z3` (hatch not filling its segment); `one unit of attention . every bar is this long` printed over the `z7` fill; `apportioned by weight` runs into the q7 dial.
- [hierarchy] The grid dominates, but the K spirals, swatches, Z bars and text blocks are all mid-weight; the q7 dial floats in the masked triangle as an inset chart.
- [depth] Flat and undeclared.

### abstract v1
- [craft] Type failures everywhere: caption lines truncated at the right margin, footer columns overprinting each other, garbled glyph scribble past the right margin at v 0.83–0.96.
- [space] The heavy black ray slices through `AND` in the title and its dotted tail through the footer — collision, not a decision; the title and the dial share no axis.
- [craft] The crimson knot within ≈ 15 mm of the centre (0.45–0.52, 0.45–0.53) is illegible ink-on-ink — the tracks that are the subject cannot be read where they start.
- [concept] The equal-length property (the pun's punchline) is invisible: folded walks do not look equal. The green dashed z-polyline zig-zagging across the dial reads as noise.
- [grid] The gold triangle's hatch, the dotted mean-reach circle, the radial stubs and the dashed green path overlap without hierarchy.

## Next versions
1. **straightened-tracks** (abstract — strongest) — Keep r02's pun and dial but make the punchline visible: draw each of the 15 tracks twice — once as the folded walk to its endpoint, and once **straightened as a ruled 80 mm bar** in a stack beside the dial (all bars identical length, segmented and coloured by which slots they spent on). The eye sees "same length, different destination" instantly. Scale the walk so the knot opens (steps ≥ 1 mm), fix all type to one flush-left column that fits, and re-aim the heavy black ray so it crops at the frame without crossing the title. Add one or two real flat Kandinsky planes that carry data (the top-3 triangle, a disc whose area is the sink's mass).
2. **resonance-planes** (faithful to the brief's idiom) — Rebuild corrected v1 in the Kandinsky colour-block canon: the causal grid stays and still holds eight rings per row, but it is tilted ≈ 15° on a dominant black diagonal rule, the argmax frames become solid crimson line-fill planes, K and Q become flat blue/red triangles whose areas are received mass and entropy, and the Z bars become a fan of equal-length textured bands radiating from the grid's corner. Cut the swatch key, formula block and specs text to one caption.
3. **one-row-concert** (lens) — Pick one query (q7) and make its row the whole plate: 8 concentric-ring "resonators" whose ring counts apportion eight (or 64) rings exactly, arranged on a Kandinsky diagonal by key index, the V textures stacked in the rings they receive, and a single green output disc whose area = 1 unit. Fewer elements, poster-scale forms, the one-distribution-per-query truth held by showing one query honestly.

**If only iterating:**
1. (abstract) Fit every text line inside the margins — caption and all three footer columns wrapped to their column width, nothing past u 0.96, no overprint.
2. (abstract) Draw the 15 tracks as straightened 80 mm segmented bars stacked beside the dial so equal length is visible, and enlarge the walks so the central knot resolves.
3. (corrected) Fix the z2/z3 hatch gaps, move `one unit of attention . every bar is this long` off the z7 bar, and replace the orthogonal layout's centred columns with one working diagonal (tilt the grid or run a heavy black rule corner-to-corner).
