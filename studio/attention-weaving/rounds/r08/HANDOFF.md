render: gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.png
gcode: gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.gcode
paper: 24x30 portrait (240 × 300 mm), cream
pens: 0 black = text layer (uniform key line SOFTMAXSUMSTOONE at 1/16 each, k0–k15 labels, caption) · 1 crimson = a letter (key) receiving a ≥ 1/16 (skeleton + floor(16a) rings at 0.9 mm) · 2 forestgreen = a letter receiving a < 1/16 (single skeleton)
layer order: 2 forestgreen → 1 crimson → 0 black
canon: Psychedelic (§9), declared flat
lineage: Wes Wilson, Fillmore poster for The Association (1966) — lettering stretched to fill a field, one warp through every glyph
mapping: line = one query's softmax row (22, top-down order printed in caption) · letter j = key j (S O F T M A X S U M S T O O N E) · cell width = a_ij × 158 mm measure, exact at line centre · line height = 84.76 mm × (4 − H_i bits) · between centres the query slerps (smoothstep), widths there are its real softmax
data: encoding.md §4a (seed 7, T 2.29842); 136/352 crimson; ring counts 216×0 · 122×1 · 13×2 · 1×3 (Q11·k5 = 0.190)
other seeds: gallery/studio/attention_weaving/trials/pp_attention_weaving_wildcard_v6_s3.png · gallery/studio/attention_weaving/trials/pp_attention_weaving_wildcard_v6_s11.png
compare-to: gallery/studio/attention_weaving/trials/pp_attention_weaving_iterate_v16.png (r06) | reference: studio/attention-weaving/ref/reference.png
