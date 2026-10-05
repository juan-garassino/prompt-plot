# DIFFUSION (Kandinsky, corrected) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/kandinsky_diffusion` |
| current render | `gallery/studio/kandinsky_diffusion/current/pp_kandinsky_diffusion_corrected_v1.png` |
| source | `studio/kandinsky-diffusion/rounds/r01/piece.py::kandinsky_diffusion` (docstring cites a `NOTES.md` that is not on disk) |
| reference | `studio/kandinsky-diffusion/ref/reference.png` (1448×1086) |
| paper · pens | custom 320 × 240 mm landscape, cream · 0 black = orbit stack, rules, checkers, type, chord · 1 crimson = fan wedges, red melt spirals, `SNR 1` mark · 2 dodgerblue = blue discs/spirals, σ quarter-circles · 3 goldenrod = gold discs, the prior's boundary circle · 4 forestgreen = serpentine-filled planes |
| status | unreviewed (no FEEDBACK.md) · 1 render on disk |

## In one line
Kandinsky's diffusion poster recast as **one straight chord in, a nest of concentric orbits out** — a colour-block composition (the data) melts left→right into a field of shrinking coloured spirals, a single ruled chord jumps straight to a Gaussian ball at the centre, and 26 concentric orbits around it (one per denoising step, inked fraction = ᾱ_t) are the reverse chain that re-emerges as a sparser colour-block sample at the right edge.

## Lede
A diffusion model drawn as a Kandinsky poster: **one straight chord jumps from data to noise**, while twenty-six concentric orbits trace the slow denoising path back.

## On the sheet
A colour-block composition at the left melts rightward into scattered blue, crimson, gold and green spirals. At the centre sits a gold circle of dots, the noise, ringed by a black stack of orbits that thin toward the middle. A single black line crosses to it. A sparser composition appears at the right edge, with a time ruler along the bottom.

## The science
Each orbit is one denoising step of a standard diffusion model, a thousand steps in all with every thirty-eighth drawn; how much of an orbit is inked follows how much of the picture remains. Colour appears only where signal outweighs noise. The one-step formula is written in text. Some encodings, such as the orbit wobble, are too subtle to see.

## What is on the sheet
Positions normalised to the sheet (u → right, v → down).

**1. The orbit stack (dominant, u 0.35–0.88, v 0.16–0.875; ≈0.53 sheet width, centre u≈0.62, v≈0.51).** 26 black concentric circles. The outer ~8 are continuous; inward they break into arcs separated by ~12 radial wedge gaps (a sunburst of blank spokes), and the innermost rings are only short tick-dashes — the stack reads as a black disc whose texture thins toward the centre. A vertical column of tiny marks with an `ā_t` label sits in the top spoke (u≈0.62, v 0.19–0.32). The stack's bottom edge dips below the time ruler (v 0.84–0.875).
- **The prior** at the centre: a goldenrod circle (≈48 mm, u 0.55–0.67, v 0.41–0.61) enclosing ~150 black dots and ~15 small black spirals; the spirals bunch along its left rim (u≈0.56–0.58).
- **The chord**: a single straight black line from a black spiral at the top-left (u≈0.07, v≈0.20) to the centre of the prior (u≈0.61, v≈0.51), crossing the green planes and the whole left half of the orbit stack.

**2. The data sample — left composition (u 0.03–0.28, v 0.20–0.78).** Kandinsky blocks drawn with pen fills: two green serpentine-filled rectangles (u 0.11–0.26, v 0.23–0.33 and u 0.19–0.26, v 0.33–0.43); a large goldenrod spiral disc (u≈0.07, v≈0.28); a large blue spiral disc (u≈0.12, v≈0.43); a vertical rule at u≈0.11 (v 0.30–0.74) and a horizontal rule at v≈0.53 (u 0.04–0.26); an outlined triangle (u 0.07–0.10, v 0.52–0.60); a black checkerboard of serpentine squares (u 0.06–0.15, v 0.53–0.70); a crimson fan-wedge of arcs (u 0.10–0.14, v 0.62–0.67). A heavy black diagonal slashes from u≈0.03, v 0.20 to u≈0.27, v 0.76.

**3. The melt (u 0.15–0.40, v 0.28–0.66).** A drift of coloured spirals and hollow rings — blue, crimson, gold, green and black, from ~8 mm down to ~1 mm — scattering rightward from the left composition and thinning toward the orbit stack; blue dominates the middle band, crimson the lower. Six long black dashed rays converge from the left composition toward the orbit stack's left edge (u 0.15–0.40, v 0.35–0.63), like a funnel.

**4. The generated sample — right composition (u 0.85–0.97, v 0.15–0.72).** A much thinner column: black serpentine checker blocks (u 0.92–0.97, v 0.17–0.26), a goldenrod spiral disc cropped by the right frame (u 0.95–0.97, v 0.29–0.36), a blue spiral (u≈0.88, v≈0.46) on the stack's rim, a horizontal rule at v≈0.53, a green serpentine rectangle (u 0.92–0.97, v 0.53–0.61), a small crimson fan (u 0.85–0.87, v 0.59–0.66), a black checker (u 0.85–0.92, v 0.63–0.72), a heavy black diagonal (u 0.88–0.97, v 0.48–0.67), and a vertical rule at u≈0.85 (v 0.18–0.72) that runs through the outer orbits.

**5. Type and furniture.**
- A Y/arrow glyph then `DIFFUSION` in giant stroke caps, u 0.04–0.50, v 0.075–0.155.
- Formula under it (v≈0.20): intended `xₜ = √ᾱₜ x₀ + √(1 − ᾱₜ) ε`, rendered as `xt = ʃa‾t x0 + ʃ ( 1 - a‾t ) c` — the √ and ε glyphs are missing.
- Top right: `S A M E  L A W  ·  D I F F E R E N T  D R A W` (u 0.58–0.93, v≈0.09) over a goldenrod spiral `≠` a blue spiral (u 0.58–0.63, v 0.12–0.14); a full rule at v≈0.16 (u 0.54–0.97); a crosshair at u≈0.88, v 0.06–0.22.
- Bottom left: `N ( 0 , I )` / `1σ  2σ  3σ` (u 0.03–0.12, v 0.76–0.78) above three blue concentric quarter-circles in the corner (u 0.03–0.13, v 0.82–0.94).
- Time ruler across the bottom (u 0.33–0.97, v≈0.84) with ticks bunched at the left and spreading right, `t = 0` and `t = T = 1000` above its ends, `√ā_t` near its centre, and a crimson tick `SNR 1` just below it at u≈0.52.
- `q ( xₜ | x₀ )   O N E  S T E P .  C L O S E D  F O R M` (v≈0.87); `p θ ( · )  × 1 0 0 0  S T E P S  ·  c θ  I N S I D E  E A C H` (v≈0.885, ε rendered as `c`); `2 6  O F  T = 1 0 0 0  ·  S T R I D E  3 8` (v≈0.93).

## The science it encodes
From the `piece.py` docstring: a DDPM with the cosine schedule, T = 1000. Stated exact mappings: orbit index = one denoising step (26 drawn, stride 38); orbit duty (inked fraction of the circumference) = ᾱ_t; orbit wobble = `√ᾱ·signal + √(1−ᾱ)·noise` on the radius; colour exists only where SNR > 1 (provenance); melt dot radius = the feature scale it stands for; melt dot position = a draw from q(x_u | x₀); ruler tick spacing = the schedule; "descending squares" = σ_t of injected noise, the fourth absent because the last step injects none; the outermost orbit is the only exact circle. Corrections to the reference it claims: the denoiser is a loop not a box, forward is one chord vs a countable reverse ladder, the noise end is isotropic and single-pen, decay is late and fast.
Observed vs claimed: the orbit wobble is not visible (rings read as clean circles); the "descending squares" are not identifiable on the sheet; the prior is not visibly isotropic (its spirals bunch on the left rim where the chord lands); the loop reads as a clock face / record rather than as 26 countable passes.

## How it got here
Single render (`corrected_v1`), no trials, no notes on disk, no feedback. The brief asks for a Kandinsky counterpart to the approved THE LONG WAY BACK (`studio/diffusion-passes/`), and demands: right sample of the same family but not a copy, iteration made legible, √ᾱ_t decay, isotropic noise end. The piece keeps the reference's left block → dot field → centre mandala → right block band but replaces the colour mandala with a black orbit stack and adds a chord borrowed from THE LONG WAY BACK.

## Keep — what works
- **The orbit stack as the loop**: 26 concentric passes around the prior is a genuinely better mechanism reading than the reference's single mandala, and its thinning-toward-centre texture (duty = ᾱ_t) is visible.
- **The chord from the data to the prior** (u 0.07 → 0.61) as one ruled line against a ladder of orbits — the forward/reverse cost asymmetry, stated with one mark.
- **The melt field** of shrinking coloured spirals (u 0.15–0.40) keeps Kandinsky's confetti while carrying scale (radius = feature size).
- **Pen fills as Bauhaus mass**: serpentine green planes and checker squares read as solid colour blocks at 1 m without flooding.
- **The time ruler with non-uniform ticks** (bunched left) — the schedule as spacing.
- **`SAME LAW · DIFFERENT DRAW`** with gold spiral `≠` blue spiral — a small, witty statement of the brief's key claim.

## Weak — what doesn't
- [concept] The centre has lost the canon: a 170 mm black concentric disc with radial gaps reads as a vinyl record or a clock, not as Kandinsky; colour — the brief's "real work" — is absent from the dominant mass.
- [hierarchy] The orbit stack takes ~0.53 of the width and nearly the full height; the data and sample compositions are squeezed into the margins (the right sample is only ~0.12 wide and is cropped by the frame), so the left→right story collapses into "one big black disc".
- [space] The orbit stack overruns the time ruler (outer rings at v 0.84–0.875 cross the ruler and its ticks) and the right vertical rule at u≈0.85 runs through its outer orbits; the chord cuts through the green planes and the whole left half of the stack; the blue spiral at u≈0.88 sits on the stack's rim.
- [concept] The prior is not isotropic on paper — its black spirals cluster on the left rim (u≈0.56–0.58), which is the one property the brief says must hold.
- [craft] Formula glyphs are missing: `√` renders as `ʃ`, `ε` as `c` (in the formula and in `c θ INSIDE EACH`).
- [concept] Six dashed converging rays from the left composition to the stack are pure diagram arrows.
- [grid] The right composition's blocks, the crosshair and `N(0, I)` quarter-circles do not share axes with the left composition or the title.
- [craft] Travel 11.8 m against 20.5 m draw; the melt field's hundreds of small spirals are many pen lifts for little tone.

## Next versions
- **coloured-orbits** (faithful × mechanism) — Keep the orbit loop but shrink it to ≈0.30 of the sheet width and colour it: each orbit drawn in the pen of the provenance still resolved at that step (colour only while SNR > 1, black after), so the stack becomes a Kandinsky concentric-circle study whose colour order encodes the schedule. Give the left and right compositions equal width (≈0.25 each) so the right sample is visibly a different draw of the same palette. Restores the canon to the centre and the band to the sheet.
- **squares-in-circles** (abstract) — Take Kandinsky's own "Squares with Concentric Circles": a 4 × 3 grid of cells, each cell one step of the reverse chain, each holding a concentric-ring motif whose colour separation and ring count are that step's √ᾱ / √(1−ᾱ) split — noise cells top-left, clean cells bottom-right. Iteration becomes legible as a count of cells; the twist is that the viewer recognises the painting before the mechanism.
- **one-chord** (lens) — Crop in on the moment of commitment: the prior ball large at the left edge (0.4 of height, isotropic stipple via `tone_dots`), the chord leaving it as the heavy Kandinsky diagonal, and the first few reverse orbits rising around it in colour as structure re-appears at SNR = 1 (crimson tick as a real boundary). Everything else cut.
- **If only iterating:**
  1. Reduce the orbit stack's outer radius so its lowest ring clears the time ruler by ≥ 8 mm (bottom at v≤0.80) and it no longer touches the right vertical rule at u≈0.85.
  2. Redraw the prior's contents as isotropic `tone_dots` with no spirals, so nothing bunches on the left rim.
  3. Replace the missing glyphs (`√`, `ε`) in the formula and bottom captions, and delete the six dashed converging rays at u 0.15–0.40.
