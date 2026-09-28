# DECISION SURFACE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/neural-networks/decision-surface` |
| current render | `gallery/neural-networks/decision-surface/candidates/pp_bauhaus_decision_v3_seed21.png` (seeded readout; the trained-weights siblings are `pp_bauhaus_decision_v3_REAL_seed5.png` / `_seed13.png`) |
| source | `promptplot/generative/pieces/ml.py::bauhaus_decision` |
| paper · pens | a4 portrait (210 × 297 mm), cream · 0 dodgerblue = class +1 points · 1 deeppink = class −1 points · 2 black = the iso-0 knife, ±margin shoulders, type, swatch, plus mark |
| status | unreviewed in the viewer (no FEEDBACK.md; the project CLAUDE.md lists `bauhaus_decision` as APPROVED) · 13 renders on disk, all in `candidates/` — no promoted file |

## In one line
A trained network's classification drawn as **a cut through a field** — the bold black knife is the exact iso-0 contour of f(u,v)=Σ aᵢ·tanh(Wᵢ·[u,v]+bᵢ), the two thin shoulders are f=±margin, and every dot is coloured by the true sign of f (blue +1 upper-right, pink −1 lower-left).

## What is on the sheet
Coordinates normalised to the A4 sheet (u → right, v → down); drawable area u 0.07–0.93, v 0.05–0.95. Only the 614 px preview exists, so stroke-level detail is approximate.

1. **The knife (dominant mark)** — one heavy black curve, ≈ 1 mm wide (five offset passes −0.5…+0.5 mm), entering at the left margin u 0.11, v 0.25, running almost level for ≈ 15 mm, then bending into a long descending diagonal through the centre (u 0.36 v 0.34 → u 0.60 v 0.63) and easing out flat at the bottom-right, ending at u 0.90, v 0.88. Total run ≈ 0.95 of sheet height. It reads as a single stroke of an S, slightly concave toward the lower-left. At its left end the offset passes misregister into a visible step/notch about 1 mm from the start.
2. **The shoulders (two hairlines, f = ±margin)** — not parallel to the knife:
   - *upper (blue-side) shoulder*: starts at u 0.24, v 0.13, just under the subtitle, runs down close beside the knife (≈ 6–8 mm off) to u 0.55 v 0.45, then **peels away** and flattens horizontally to the right margin at u 0.90, v 0.50. This opens a large blue-side lagoon between it and the knife's lower tail.
   - *lower (pink-side) shoulder*: starts at the left margin u 0.10, v 0.39, rises to a low hump at u 0.26 v 0.37, then descends nearly straight to end mid-sheet at u 0.72, v 0.91 — cutting across the pink field rather than hugging the knife.
   - The corridor between the two shoulders is ≈ 25 mm wide at the top and ≈ 50 mm wide at the lower right — the margin is visibly non-uniform.
3. **The point clouds** — ≈ 40 small blue tight-spiral dots (≈ 2 mm) scattered over the upper-right region (u 0.35–0.90, v 0.15–0.45), and ≈ 80 small pink dots filling the lower-left region (u 0.10–0.65, v 0.40–0.90). Density is uniform-random, clumpy in places (twin dots almost touching at u 0.28 v 0.51, u 0.30 v 0.55). No dot sits inside the corridor.
4. **Support-vector discs** — ~10 larger spiral discs (≈ 4 mm): blue at u 0.31 v 0.26, u 0.69 v 0.52, u 0.70 v 0.53, u 0.84 v 0.51, u 0.85 v 0.54; pink at u 0.22 v 0.38, u 0.31 v 0.36, u 0.37 v 0.41, u 0.41 v 0.43, u 0.64 v 0.76. Most pink discs sit **on** the lower shoulder line (the line runs through them).
5. **Title block** (top-left, flush to the margin) — `D E C I S I O N` / `S U R F A C E` (≈ 3 mm caps, two lines, u 0.10–0.28, v 0.08–0.11) with a short underline under the first letters of SURFACE, then `T H E   C U T   T H R O U G H   I N P U T   S P A C E` (≈ 2 mm, u 0.10–0.58, v 0.14).
6. **Swatch** (top-right corner, u 0.89, v 0.07–0.09) — a tiny stack of black / blue / pink ticks, 2.6 mm; in the preview it is half-buried under the matplotlib legend.
7. **Plus mark** — one small black `+` sitting directly on the knife at u 0.77, v 0.81.
8. **Footer** (bottom-right, u 0.61–0.89, v 0.94) — intended `F(X)=SIGN(W.X+B)`; the parentheses and `=` don't render, it reads `F X   S I G N   W . X   B`.
9. **Quiet zones** — the band v 0.15–0.20 across the top (only the upper shoulder's start), the blue lagoon between upper shoulder and knife tail (u 0.60–0.90, v 0.52–0.85, sparsely dotted), and the whole left edge below v 0.85.

## The science it encodes
From the docstring (`promptplot/generative/pieces/ml.py::bauhaus_decision`): "a neural network drawn as its decision FUNCTION, not its wiring. A small readout f(u,v)=Σ aᵢ·tanh(Wᵢ·[u,v]+bᵢ) scores the input plane; the bold black knife is the EXACT iso-0 contour (marching squares), flanked by ±margin shoulders and the hidden-unit hyperplane creases the cut visibly kinks on (the fingerprint of composition — no neuron drawn). Every dot is coloured by the TRUE sign of f."
- **Computed exactly:** the iso-0 and ±margin contours by marching squares on a 140² grid; every point's colour is sign(f) at that point; points with |f| < 0.7·margin are rejected (the corridor), 0.7–1.5·margin become support discs (max 5 per class).
- **Seeded:** in this render (no `weights=`), W₁, b₁, a are seeded Gaussians with 6 hidden units; the point positions are uniform random, rejection-sampled 1 blue : 2 pink. The `_REAL` renders feed columns of a trained GPT-style query matrix — which is a real weight tensor but not a classifier trained on these points, so "trained" is honest only about the numbers, not the task.
- **Not visible:** the docstring's "hidden-unit hyperplane creases the cut visibly kinks on" — the crease lines are no longer drawn (they were in v1), and on this seed the cut is a smooth S with no readable kink. "Support vectors" are points near the margin, not an SVM solution.

## How it got here
- **v1 (`v1_seed3`)** — near-vertical knife plus several parallel thin shoulder contours, and **straight black hyperplane creases** (the tanh units' zero lines) crossing the whole field in an X. Shows the composition-of-hyperplanes idea literally; reads as a textbook overlay.
- **v2 (`v2_seed3`, `v2_seed42`)** — creases removed; the knife becomes a clean diagonal S from lower-left to upper-right with **tightly parallel shoulders** (a true corridor ≈ 5 mm wide in seed3), blue above-left, pink below-right, support discs strung along the shoulders. The cleanest, most legible version: the cut reads as one engineered object.
- **v3 (`v3_seed21` current, `v3_REAL_seed5/13`)** — margin normalised to the 88th percentile of |f|, so shoulders now spread far from the knife where the field is shallow. Gained: the cut flips to a descending diagonal (upper-left → lower-right) and the corridor opens with real variation (the margin's geometry actually shows the field's slope). Lost: the corridor stops reading as a corridor — the shoulders wander off independently (upper one goes horizontal, lower one cuts through the pink cloud).
- No verdict from Juan on record.

## Keep — what works
- **One heavy knife + two hairlines** — the clearest weight hierarchy in the series: at 3 m the sheet is one black S-diagonal.
- The knife as a **long diagonal that uses the full sheet height** (v 0.25 → 0.88), entering at the left margin and ending at the right — it is the working diagonal of the composition.
- **Colour = sign, exactly** — no dot is on the wrong side; the two hues meet only across the corridor, so the boundary is legible even without the black line.
- **The empty corridor**: clean paper hugging the cut (|f| < 0.7·margin) — negative space that carries data (the margin).
- 1 blue : 2 pink mass ratio makes pink the loud field and blue the quiet one.

## Weak — what doesn't
- [concept] It is a **scatter plot with a decision boundary** — the canonical ML-textbook figure (rubric § 6: "a scatter with an inset… still a figure"). The order is right (a cut through a field) but it is rendered in plot vocabulary: dots on white, a curve, a caption formula.
- [craft] The shoulders are not a corridor: the upper one peels off to horizontal at u 0.55 v 0.45 and the lower one ends mid-sheet at u 0.72 v 0.91, running **through** the pink support discs. The ±margin read is lost; they look like two unrelated curves.
- [craft] The knife's left end has a misregistered step (the five offset passes don't align at the chain start, u 0.11 v 0.25). Footer loses `(`, `)` and `=`.
- [hierarchy] Below the knife there is no second level: 120 near-identical 2 mm dots are a uniform texture; the ~10 support discs are barely bigger (4 mm vs 2 mm) and don't read as a tier.
- [space] Point density is uniform random, so the fields are evenly sprinkled — no tone gradient toward or away from the cut; the quiet zones are accidents of the seed (the blue lagoon), not decisions.
- [grid] Title block, swatch, plus mark and footer are the rubric's "furniture checklist" in four corners with no shared line; the plus mark sits on the knife for no stated reason.
- [depth] Entirely flat and undeclared — no occlusion, no weight falloff, no tonal volume. The field f is a surface but nothing shows its height.
- [tension] The S-diagonal is good, but everything else is evenly distributed; nothing crops at the frame.

## Next versions
1. **field-as-tone** (mechanism) — Draw f itself, not samples of it: `tone_dots` (or `tone_hatch`) with duty = |f| on each side, blue above and pink below, so the paper is darkest far from the cut and goes to **bare paper exactly at the corridor**. The iso-0 knife stays the one heavy black line; shoulders become the edge where tone starts, so the margin is shown by ink, not by two hairlines. Contour levels spaced by gradient (rubric § 5). Kills the scatter-plot reading and turns the flat figure into a surface with volume.
2. **folded-paper** (abstract) — Composition-of-hyperplanes as a **lattice with folds**: each hidden unit is a crease across a regular line field (parallel hatch in one direction), and at each crease the hatch direction rotates by that unit's weight; the knife is where the accumulated folds cancel. The viewer sees a flat sheet of lines refracted into a boundary. Brings back v1's creases as the ORDER, not as overlay lines.
3. **seed-exact corridor** (faithful) — v2's parallel corridor with v3's descending diagonal: fix the margin as a constant physical offset of the knife (± 4 mm) with support discs only where the true |f| is within the band, dot density ramping with |f| so the clouds thicken away from the cut, one pen scarce (blue as 10 % of marks), and title/footer locked to the knife's entry and exit points.

**If only iterating:**
1. Make the two shoulders run parallel to the knife along its whole length (constant visual gap, or clip them to the knife's extent) so the corridor reads as one band; no shoulder may pass through a support disc.
2. Scale point density with |f| (sparse near the corridor, dense far away) so each colour field becomes a tone gradient, and make support discs ≥ 3× the small dots.
3. Fix the knife's start-of-chain offset step and the footer glyphs (`(`, `)`, `=`), and align title block left edge, knife entry point and footer baseline on shared lines.
