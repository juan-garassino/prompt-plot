# GPT-2 attention contact sheet — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/transformer/attention-matrix` |
| current render | `gallery/neural-networks/transformer/attention-matrix/promoted/pp_attention_matrix_gpt2.png` |
| source | `promptplot/generative/generators.py::attention_matrix` (current) · trials: `promptplot/generative/generators.py::attention_arcs` (`layout="line"` for the L0/L5 arc scores, `layout="circle"` for the chords) · data: `scripts/extract_gpt2_attention.py` (real GPT-2 small, default sentence "The pen plotter drew a black hole while the transformer watched itself think.") |
| paper · pens | current: a4 portrait · 0 navy = strong weights (> 0.4) · 1 crimson = weights 0.07–0.4 · 2 gray = L/H labels · trials: a4 landscape, 4–6 pens, one pen per head |
| status | promoted tier on disk, **no recorded feedback** · `CURATION.md` lists `attention_matrix` as "Watch … decorative data texture, not gallery compositions" · 5 renders on disk |

## In one line
The full GPT-2 attention stack drawn as a **lattice** (12 layers × 12 heads of 15×15
tick matrices) — each tick's length is the attention weight, pen splits strong/weak —
where the arc/chord trials drew the same data as **orbital/radial** arcs converging on
the sink token.

## What is on the sheet

### current — `pp_attention_matrix_gpt2.png`
- **One dominant mass, the whole sheet:** a 12 × 12 contact sheet of small square
  panels filling the drawable area from u 0.10 to 0.93 and v 0.06 to 0.95 (≈ 0.83 W).
  Each panel ≈ 12 × 20 mm, gutters ≈ 1.8 mm; no panel frames are drawn — a panel exists
  only where its ticks are.
- **The ticks:** 15 × 15 cells per panel, each a short 45° "/" stroke whose length ∝
  weight; ticks under 0.07 are omitted. Navy (pen 0) where weight > 0.4, crimson dots-
  like ticks (pen 1) below.
- **What the data draws, top to bottom:**
  - Rows L0–L2 (v 0.06–0.30) are the busiest: crimson lower-triangular fans (the causal
    mask made visible — every panel is empty above its diagonal) and several **pure navy
    main diagonals** running top-left→bottom-right (L0 H1, L0 H3, L0 H5, L1 H11, L4 H11
    and others) — heads attending to the current/previous token.
  - From L3 downward the crimson thins to sparse scatters and **a navy vertical rule at
    the left edge of every panel** takes over — the first-token column (the attention
    sink). By L6–L10 (v 0.45–0.85) almost every panel is only that navy rule plus a few
    crimson flecks, so the lower two-thirds reads as a comb of 12 navy vertical lines
    broken by gutters every 20 mm.
  - L11 (v 0.88–0.95) revives: dense crimson fans in H0, H8, H9 bottom-left and bottom-right.
- **Type:** gray stroke-font labels only — `H0 H1 … H11` across the top (v≈0.06),
  `L0 L1 … L11` down the left edge (u≈0.08), ≈2.6 mm, hairline. No title, no footer.
- **Quiet zone:** none by design; the emptiness that exists is the upper-right half of
  every panel (the causal mask) and the thinning lower layers — structural, not composed.

### trials
- `pp_attention_gpt2_L0.png` / `pp_attention_gpt2_L5.png` (a4 landscape, 4 / 6 pens):
  15 tokens on a baseline at v≈0.81 (u 0.08–0.92), each attention weight a parabolic arc
  from query back to key, one pen per head, stacked passes for heavy weights. L5 is
  dominated by a heavy olive/brown family of nested arcs all rooted at the leftmost token
  — a fan of rainbows falling from the first word — reaching v≈0.12. Bottom 0.2 and the
  sides of the sheet are empty.
- `pp_attention_chord_gpt2.png` / `_dense` (a4 landscape, 6 pens): tokens on a circle
  (centre u 0.50, v 0.47, radius ≈ 0.28 W), chords bowed toward the centre by weight; the
  heavy olive bundle pours into the **bottom node** (u 0.50, v 0.88) from every token,
  a fountain/sheaf shape. Dense version: many more tokens, ~105 m of ink, the sheaf goes
  solid olive in its lower third and the rim is a tangle of cusped loops. Gray pen-up
  radials show through as a light spoke wheel.

## The science it encodes
`attention_matrix` docstring: "The whole model at a glance: a layers x heads contact
sheet of attention matrices, each cell a diagonal tick sized by the attention weight."
Data is **exact** real GPT-2 small attention (12 layers × 12 heads × T × T) from
`scripts/extract_gpt2_attention.py`; nothing seeded when the npz is present. Tick length =
`half * min(1, w)`, pen = `w > 0.4`. What is visibly true on the sheet: (1) the causal
triangle, (2) early previous-token/self heads as clean diagonals, (3) the **attention
sink** — deeper layers dump most of each row's mass onto token 0, drawn as the navy left-
edge rule in almost every panel from L3 down. The render shows all three. The token text
is never shown, so which words attend to which is not recoverable from the plate.

The arc/chord trials (`attention_arcs` docstring: "Attention as a musical score … ink
passes scaling with the attention weight; one pen per head") draw the same sink as the
olive fountain into one node.

## How it got here
1. Arc scores, `layout="line"`: L0 then L5 — a single layer at a time, heads as pens. The
   sink reads (fan from the first token) but the sheet is a half-dome with a dead bottom.
2. Chords, `layout="circle"`, then `_dense` — the sink becomes a fountain; dense version
   floods (olive solid) and the rim tangles.
3. The contact sheet (promoted): trades one striking shape for the whole model at once —
   gains completeness and a strong statistical read (sink comb), loses any single form.
No feedback in `studio/feedback.jsonl`.

## Keep — what works
- The **attention sink as a navy comb**: from L3 down, the left-edge navy rule in every
  panel builds 12 broken vertical lines over the lower two-thirds — the one phenomenon
  that reads at 3 m, and it is real data.
- The **causal triangle** leaves the upper-right of every panel as bare paper — negative
  space produced by the mechanism itself.
- Early-layer pure navy diagonals (L0 H1, L0 H3) — the cleanest single marks on the sheet.
- The strong/weak pen split at w = 0.4: navy is structural and scarce-ish, crimson texture.
- From the chord trials: the fountain into the bottom node — the sink as a single form
  with a direction.

## Weak — what doesn't
- [concept] It is a textbook figure: a grid of heatmaps with L/H axis labels — exactly
  the "scientific figure" and the Hinton/heatmap schematic § 6 bans. `CURATION.md` already
  says it is texture, not a composition.
- [hierarchy] 144 equal panels, equal gutters; no dominant element. The sink comb is the
  only large-scale read and it is emergent, not composed.
- [tension] Centred full-bleed grid with even margins; nothing crops the frame, no diagonal.
- [space] No shaped quiet zone; the lower-layer sparsity is leftover, not decided.
- [craft] Travel 13.8 m vs draw 3.0 m, 31 k commands — ticks of 0.12–0.6 mm are mostly
  pen lifts; many crimson ticks at the 0.12 mm floor are dots a real pen will blob.
- [craft] Labels are gray hairline 2.6 mm stroke text — caption scale on a data grid, the
  lab-figure default.
- [depth] Flat and undeclared.
- [concept] Tokens never appear; the viewer cannot tell that the sink is the first word.
- (trials) [craft] chord `_dense` floods the sheaf solid olive and knots the rim; [space]
  arc trials leave the bottom 20 % and both sides dead.

## Next versions
1. **the sink** (mechanism) — drop the contact sheet; draw only the phenomenon it
   revealed. All 144 heads' mass onto token 0 as one **flow-to-attractor**: each head a
   streamline whose ink passes ∝ its sink mass, rising layer by layer and bending into
   one heavy navy well cropped off the bottom-left corner; the few heads that resist the
   sink (the L0 diagonals, L11 fans) are the scarce crimson exceptions. One dominant
   form, a real diagonal, a genuine quiet zone where the heads have left.
2. **one line, twelve floors** (faithful) — keep the matrix language but pick one
   column of the stack: the 12 layers of a single head as **stratified** strata, stacked in
   axonometry with the z-buffer engine so later layers occlude earlier; the sink column
   becomes a rising vertical wall through the stack. Adds depth and hierarchy while
   staying exact.
3. **word by word** (lens) — the default sentence set in large type across the sheet
   (the tokens themselves are the lattice), and each word's received attention drawn
   as ink density *inside its letterforms*; "The" floods navy, the rest go pale. The twist:
   the model's attention is on the least meaningful word in the sentence.

**If only iterating:**
1. Crop to the 6 × 12 rows L3–L8 (where the sink comb is cleanest) at twice the panel size,
   so the navy comb is the dominant form and crimson becomes accent.
2. Replace the 0.12 mm floor ticks: skip weights below 0.12 entirely and draw weights
   0.12–0.4 as a fixed 0.8 mm tick with duty ∝ weight (tone drives duty, not size).
3. Put the 15 token strings, in giant type, along one edge aligned to the key axis so the
   first column is visibly labelled "The".
