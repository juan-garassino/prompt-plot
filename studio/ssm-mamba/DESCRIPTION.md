# THE RECEDING HORIZON — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/ssm_mamba` |
| current render | `gallery/studio/ssm_mamba/current/pp_ssm_mamba_v7_s7.png` (seed 7, chosen; `v7_s11`, `v7_s23` are sibling seeds in trials) |
| source | `studio/ssm-mamba/rounds/r01/piece.py::receding_horizon` |
| paper · pens | a4 portrait (210×297 mm), white preview · 0 black = state corridor mesh, horizon hatching, clock ticks, rule, all black type · 1 crimson = selection events (corridor seams, tooth edges, projection dashes, stems, `SELECTION` label) · 2 forestgreen = the longest-reach trace and `REACH` label only |
| status | unreviewed (no feedback on file) · 12 renders on disk (v1–v7, several seeds) |

## In one line
A selective state-space (Mamba S6) scan drawn as a **laminar** order — a hidden-line corridor of 40 channel states along time above its own memory horizon, a 45° sawtooth that grows one token per token and is cut to zero wherever the learned step Δt fires — with both plates sharing one axonometric metric so a tooth's length on paper is its reach in tokens.

## Lede
A Mamba-style memory scan drawn as **a corridor of memory above a receding horizon**, where each token chooses how far back it can still see.

## On the sheet
A black woven wireframe band descends across the sheet from upper left to centre right, crossed by four crimson seams. Beneath it a black rule carries clock ticks and hatched sawtooth teeth that end in crimson cliffs, lined up with the seams above. A short green line marks the deepest memory. Large spaced titles sit at the top and small labels run along the bottom.

## The science
The corridor comes from a real model with 40 memory channels that forget at different speeds and a learned step that jumps at topic boundaries. The horizon is the computed memory length: it grows one token per token, then drops to zero where the step fires. Both plates share one scale, so tooth length equals reach. The inputs are synthetic.

## What is on the sheet
- **The state corridor (dominant mass).** A black woven wireframe band descending left-to-right across the sheet, bleeding off both side margins: at the left edge it spans v≈0.29–0.38, at the right edge v≈0.49–0.58; ~0.90 of sheet width. The far-left third is a tall, open, wavy surface with big folds and sparse mesh (u≈0.05–0.40, v≈0.29–0.45); toward the right it flattens into tightly hatched stacked folds with dark seams (u≈0.55–0.95, v≈0.40–0.58). Four crimson seams run across the corridor's folds (transverse profiles at the selection events) — at u≈0.07–0.14, v≈0.29–0.33; u≈0.07–0.28, v≈0.30–0.37; u≈0.37–0.48, v≈0.40–0.47; u≈0.64–0.86, v≈0.48–0.53.
- **The horizon shadow (second mass).** Beneath and parallel to the corridor, a straight black rule descends from u≈0.05, v≈0.48 to u≈0.95, v≈0.69, carrying short black clock ticks of varying height above it (clustered in bursts of 3–5 at each selection event). Hanging below the rule are sawtooth teeth filled with parallel black hatching at ~1.6 mm: each tooth ramps down along the rule and ends in a vertical cliff edged in crimson. Five full teeth: cliffs at u≈0.13, 0.28, 0.52, 0.63, 0.87; the tooth after u≈0.63 is the deepest (to v≈0.79). Crimson dashed projection lines drop vertically from each corridor seam to its cliff (u≈0.13, 0.28, 0.52, 0.63); black and green dashed verticals at u≈0.84–0.88 connect the corridor's front edge to the rule.
- **The reach.** A green double line running along the deepest tooth, parallel to the rule, from u≈0.64, v≈0.62 to u≈0.86, v≈0.67, capped by short green verticals at both ends.
- **Type.** Title `THE  RECEDING` / `HORIZON` in giant thin spaced caps (u≈0.05–0.67, v≈0.05–0.11), its top edge touching the drawable frame, underline under the `H`. `EVERY TOKEN CHOOSES HOW FAR BACK IT CAN SEE` (u≈0.05–0.82, v≈0.15), `SELECTIVE STATE SPACE . S6` (v≈0.17). Stage label `1  THE SCAN` / `STATE H T N` / `40 CHANNELS . LOG SPACED A N` (u≈0.55–0.92, v≈0.24–0.26). `SLOW . A 0.15` (u≈0.23–0.38, v≈0.27) above the corridor's far end. Crimson `SELECTION . DT FIRES` / `MEMORY CUT TO ZERO` (u≈0.52–0.80, v≈0.31–0.33). `FAST . A 2.60` (u≈0.18–0.33, v≈0.50) between the corridor and the rule.
- **Legend row (three columns, v≈0.74–0.77).** `2  THE HORIZON` / `LAG . TOKENS BACK` / `SAME PITCH AS TIME` (u≈0.06–0.28); `INTERNAL CLOCK` / `ONE TICK PER UNIT OF S` / `TICKS BUNCH AS IT RACES` (u≈0.40–0.60); green `REACH` / `18 TOKENS BACK` / `DEEPEST MEMORY` (u≈0.68–0.85). A black dashed vertical from the corridor passes down through the REACH column at u≈0.84.
- **Step strip (v≈0.86–0.92).** A black baseline with fine ticks from u≈0.05 to u≈0.77; four tall crimson stems at u≈0.12, 0.28, 0.52, 0.63 (in x-register with the cliffs) and one shorter black stem at u≈0.38. Caption `DT T . THE LEARNED STEP` / `SOFTPLUS OF A LINEAR READ OF X T` (u≈0.05–0.37, v≈0.93–0.94). Footer equation `H T   EXP -A DT T   H T-1   B T X T` (u≈0.30–0.93, v≈0.95) — `=`, `(`, `)`, `·`, `+` do not render.
- **Furniture.** 3-pen swatch stack at u≈0.92, v≈0.05–0.08.
- **Quiet zones.** The band v≈0.18–0.28 between subtitle and corridor (only the stage labels sit in it), and v≈0.79–0.85 below the teeth on the left.

## The science it encodes
From `studio/ssm-mamba/rounds/r01/NOTES.md`: a real diagonal S6 block with exact zero-order-hold discretisation over 40 log-spaced channels (a₀=0.15 … a₃₉=2.60). Two token features (salience s_t, signal u_t) from seeded fbm/value noise with topic-boundary events; Δt_t=softplus(−1.55+9.0·s_t) (~0.26 idle, ~7 at a boundary), Ā=exp(−aΔt), B̄=(1−Ā)/a·B_t, h_tn=Ā h_(t−1)n + B̄ u_t — the corridor's height is h normalised per channel. The model clock S_t=ΣΔt gives the ticks. The e⁻¹ horizon H(t) in tokens is solved exactly; it is a sawtooth by proof (grows one token per token after a cut, then a cliff). Selection events = {t : a_slow·Δt ≥ 1}; the reach t*=argmax H. The lag axis uses the same world pitch as time, so the green reach (18 tokens) equals the tooth length. The notes self-score avg ≈7.4 with negative space at 6 — not passing — and name the biggest weakness: the shadow repeats the corridor's gesture.

What reads on the sheet: the sawtooth-and-cliff rhythm, and the red register lines tying cuts in the corridor to cliffs in the shadow. What does not: that the shadow's depth axis is lag, not a second spatial axis (the notes flag this too), and the timescale gradient across the 40 channels.

## How it got here
- **v1**: corridor and shadow overlapped in the upper-left half; labels collided inside the geometry; floor plate too close so the corridor dipped through the rule (the collision the notes say "killed v1 and v2").
- **v5 (s7, s23)**: the two plates separated onto one shared basis with a proper floor offset; green "LONGEST REACH" label first placed on the teeth; clock ticks and stem strip added.
- **v6 (s7, s23)**: corridor made wavier and cropped at both edges; reach label moved into the legend row.
- **v7 (s7 chosen, s11 "best terrain form", s23)**: legend reorganised into three columns, REACH in green; final tuning.
Gained: separation, register, legibility. Unchanged: two parallel descending bands at the same angle. No feedback from Juan on file.

## Keep — what works
- The sawtooth horizon: hatched teeth with crimson cliffs along a single rule (u≈0.05–0.95, v≈0.48–0.79) — the plate's signature silhouette; it reads "grows, then gets wiped" before the caption.
- Crimson as event only: seams, cliffs, projection dashes and step stems all derive from one set and share vertical register (u≈0.13, 0.28, 0.52, 0.63).
- The corridor cropped at both side edges — no first token, no last token.
- Depth-aware thinning: the corridor's far/past end is open and sparse, the near/recent end tight — "the past literally fades".
- Title/tagline `THE RECEDING HORIZON` / `EVERY TOKEN CHOOSES HOW FAR BACK IT CAN SEE`.
- Green used exactly once (the reach) — scarce and loud.

## Weak — what doesn't
- [tension] Corridor and shadow are two parallel descending bands at the same angle; nothing opposes, nothing overlaps with intent (the notes' own single biggest weakness).
- [space] Two voids of similar size (v≈0.18–0.28 and v≈0.79–0.85) — neither shaped, the upper one ~30 mm doing little.
- [concept] The lag axis reads as a second surface, not as "tokens back"; the dimension is only stated at caption size in the legend.
- [craft] Equation footer loses `=`, `(`, `)`, `+`, `·` — reads `H T   EXP -A DT T   H T-1   B T X T`; the title's top edge sits on the frame.
- [craft] The corridor's right third (u≈0.60–0.95, v≈0.45–0.58) stacks folds into near-muddy hatching.
- [hierarchy] Corridor vs shadow is ~2:1 in weight, not the 3:1 the rubric asks; the step strip at the bottom repeats the stems a third time and dilutes.
- [grid] The dashed verticals at u≈0.84–0.88 cut through the REACH legend column.

## Next versions
1. **opposed-shadow** (mechanism) — Keep the corridor's angle but rotate/foreshorten the horizon plate so its teeth grow TOWARD the viewer (lag as depth into the sheet), and let the teeth overlap the corridor's near edge with intent — the cut in the state and the cliff in memory become one crossing event. Breaks the parallel-bands parity and makes lag unmistakably a different axis.
2. **one-sawtooth** (abstract) — Transpose to STRATIFIED: drop the corridor surface; draw the 40 channels as 40 horizontal strata of sawtooth horizons stacked down the sheet, slow channels on top with long teeth, fast channels at the bottom with short teeth, all cut at the same crimson verticals. The whole sheet becomes one lattice of memory spans; the timescale gradient is visible as tooth length shrinking downward, and selection is a vertical knife through all strata.
3. **corridor-swallows** (lens) — Enlarge the corridor to ~60 % of the sheet (cropping top and both sides), reduce the horizon to a narrow, very loud crimson/black fringe along its near edge, and spend the upper void on the input stream u_t in x-register as a thin dash rhythm. Hierarchy goes to 3:1 and both voids are spent.

**If only iterating:**
- Put a dimensioned bracket on the deepest tooth reading `LAG 0 … 18 TOKENS` at ≥2.5 mm type; test: a viewer names the shadow's axis without reading the legend.
- Spend the upper void: move the input stream u_t (as a dash rhythm in x-register with the stems) into v≈0.18–0.28 and delete the bottom step strip; test: only one large quiet zone remains.
- Fix glyphs (`=`, `(`, `)`, `+`, `·`) in the footer equation and drop the title 3 mm off the frame.
