# COMPOSITION WITH RED YELLOW BLUE AND NOTHING — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/composition_nothing` |
| current render | `gallery/studio/composition_nothing/current/pp_composition_nothing_v2.png` |
| source | `studio/composition-nothing/rounds/r00/piece.py::composition_with_nothing` — **FROZEN ORIGINAL v2**, restored from the 2026-09-18 transcript and verified pixel-identical to the gallery PNG (see `rounds/r00/NOTES.md`). Render: `--seed 7 --colors 4 --paper a4 --orientation landscape --palette black,crimson,gold,dodgerblue`. Lineage: it began as round 04 of the ORBITAL RESONANCE family (brief `studio/astro-01/orbital-resonance.md`, physics notes `studio/orbital-resonance/rounds/r01/NOTES.md`). `studio/orbital-resonance/rounds/r04/piece.py` is the later drift (240 lanes, PERCENT caption) and is **not** v2. |
| paper · pens | v2 = A4 **landscape** (297 × 210, drawable 10–287 × 10–200), white · 0 black = every rule, all type · 1 crimson = the 2:1 block (first order) · 2 gold = the 5:2 block (third order) · 3 dodgerblue = the 3:1 block (second order). The 7:3 (fourth order) gets rules only, with no colour. |
| status | unreviewed (no feedback) · 6 renders on disk (v1, v2, r04_s3, r04_s7, r04_s11, r04_a3) |

## In one line
The Kirkwood gaps drawn as a **De Stijl orthogonal subdivision (stratified lattice)** of period-space: x is semimajor axis 2.26–3.34 AU, each vertical rule stands at a measured band edge with weight equal to libration width, each horizontal stratum is one resonance order with height equal to its strength, and colour is painted only on the swept-empty bands.

## What is on the sheet
Reading order: title, then the red block, then the black armature, then three small labelled blocks, then the caption.

- **Title (dominant by area).** Two lines of giant stroke type, drawn as outlined double-stroke letters rather than solid mass: `COMPOSITION WITH RED` / `YELLOW BLUE AND NOTHING`. It is flush left at u ≈ 0.05 and spans to u ≈ 0.93. Cap height is about 13 mm (≈ 0.045 W). It sits at v ≈ 0.06–0.21. Pen 0.
- **The 2:1 red block (the loudest mass).** A serpentine crimson fill at u 0.77–0.97, v 0.57–0.95 (about 59 × 80 mm, ≈ 0.20 W wide). It bleeds to the bottom and right margins and fills the whole bottom stratum. Close up, the fill lines leave hairline white banding (strong on r04_a3).
- **The full-height bar.** One heavy black vertical, about 3.8 mm wide, at u ≈ 0.765, from the bottom margin to the top margin. This is the inner edge of the 2:1 band, "where the belt stops". It runs **through the title** (it splits the `D` of RED and the `H` of NOTHING) and through the caption word `THE`.
- **Field line.** A 2.6 mm black horizontal across the full width at v ≈ 0.38. It divides the title zone from the period-space field.
- **Strata.** Horizontal rules at v ≈ 0.43, 0.49 and 0.57 split the field into four strata, bottom to top: 2:1 (80 mm tall), 3:1 (18 mm), 5:2 (12 mm), 7:3 (11 mm). Rule weight scales with strength (0.85–2.85 mm), drawn as stacked parallel strokes.
- **Vertical rule pairs** (serpentine bands, visibly beaded at the preview edges). They stop at the field line: 3:1 at u 0.22 / 0.26 · 5:2 at u 0.51 / 0.53 · 7:3 at u 0.64 / 0.65 (hairline pair) · 2:1 at u 0.765 (full height) / 0.96 (a heavy bar on the right edge, down to v 0.95).
- **Blue block (3:1).** u 0.22–0.26, v 0.49–0.57, about 12 × 18 mm. Label `3:1` in giant type (≈ 8 mm) just right of it.
- **Gold block (5:2).** u 0.51–0.53, v 0.43–0.49, about 6 × 12 mm, a postage stamp. Label `5:2` right of it.
- **7:3.** No colour. Label `7:3` at u ≈ 0.66–0.73, v ≈ 0.38–0.42; its top touches the field line.
- **2:1 label.** `2:1` centred above the red block at v ≈ 0.52, inside the 3:1 stratum. The colons are hand-drawn dots, because the stroke font has no `:`.
- **Caption row** at v ≈ 0.35, cap height ≈ 1.5 mm. It is unreadable at arm's length. Left: `KIRKWOOD 1866.  MU 9.5388E-4.  VERLET.  300 JUPITER YEARS.` Right: `28 OF 96 LANES SWEPT.  THE WHITE IS THE BELT.`
- **Quiet zone.** The lower-left ≈ 55 % of the field (u 0.03–0.76, v 0.57–0.95) is bare paper, crossed only by three pairs of vertical rules. That emptiness is the argument: white = surviving asteroids.

## The science it encodes
From the r04 docstring and `rounds/r01/NOTES.md`:

- **Model.** The planar circular restricted three-body problem (Sun + Jupiter, μ = 9.5388e-4). Test particles sit on a uniform comb in semimajor axis, e₀ = 0.18, with seeded phases. The integrator is velocity-Verlet in the inertial frame, dt = 0.02, run for 300 Jupiter years.
- **Measurement.** Libration width is max − min of the osculating *a*, boxcar-averaged over one orbital period. A lane is "vacant" when its width beats a wander threshold or its excess over the running-median background beats a threshold. Contiguous vacant lanes form bands.
- **Naming.** Bands are named by Kepler III alone: a = a_J (q/p)^(2/3) gives 3:1 at 2.50, 5:2 at 2.82, 7:3 at 2.96 and 2:1 at 3.28 AU.
- **What is exact vs. chosen.** Band edges come from the integration. Block area is width × strength. The colour-to-order mapping is a design choice.
- **Visible caveat:** the 7:3 is not robust across seeds. It is present on v2 and s3, absent on s7 and s11. The r01 notes claim "the gaps are physics, not sampling", and that holds for 3:1 / 5:2 / 2:1 but not visibly for the 7:3.
- **The joke is the physics.** The coloured rectangles are the NOTHING (swept by resonance); every white rectangle is full of asteroids.

## How it got here
- **v1.** Every vertical rule ran the full sheet height, straight through both title lines. The title read as caged.
- **v2 (current).** Only the 2:1 inner edge runs full height; all other verticals stop at the field line. Much calmer, but the one surviving bar still cuts the title and caption.
- **r04_s3 / r04_s7 / r04_s11.** Seed sweeps at A4 landscape. On s3 and s7 the caption is now the `PERCENT OF THE BELT SWEPT` wording (28.3 %, 26.7 %). The 7:3 stratum disappears on s7 and s11, so the sheet has three strata instead of four. Proportions shift noticeably with seed: on s11 the 2:1 block starts at v ≈ 0.50.
- **r04_a3.** The same composition on A3 landscape. The blocks read as solid colour with visible white banding from the fill spacing.
- No Juan feedback recorded.

## Keep — what works
- **The title-as-punchline.** Placed as a Mondrian title, it makes the physics a joke: the coloured blocks are the swept gaps and "the white is the belt".
- **Every mark carries data.** Rule position = band edge, rule weight = libration width, stratum height = order strength, colour = resonance order. There is nothing decorative on the sheet.
- **The single full-height bar at the 2:1 inner edge.** It is a real physical boundary (the belt ends there) and the only element that breaks the field line. It is a good, defensible tension.
- **The large lower-left white.** As a quiet zone it is shaped by the data, not left over.
- **Staircase of strata.** Heights fall 80 → 18 → 12 → 11 mm bottom to top, a real ordering you can read without numbers.
- **Colour discipline.** Three accents, one loud (red) and two scarce, with the 7:3 unpainted "because it is too weak" (stated in code, not on the sheet).

## Weak — what doesn't
- [space] The full-height bar at u 0.765 slices the `D` of RED, the `H` of NOTHING and the word `THE` of the caption. That overlap is a collision, not a decision: nudging the title left or ending the bar at the field line would lose nothing.
- [hierarchy] Blue (≈ 12 × 18 mm) and gold (≈ 6 × 12 mm) are postage stamps against a 59 × 80 mm red. At 3 m the sheet reads as "red block + title". Two of the three colours in the title are barely present.
- [craft] The title is outlined double-stroke giant type, not mass. Against 3–4 mm bars it reads as hairline lettering, which is the technical-drawing default the rubric warns about.
- [craft] The caption at ≈ 1.5 mm cap height is illegible in the render, and it carries the twist ("THE WHITE IS THE BELT"). The punchline is set at footnote size.
- [grid] Labels float. `7:3` touches the field line. `2:1` sits in the 3:1 stratum rather than on its own block. `3:1` and `5:2` sit beside their blocks at different offsets. There is no shared baseline.
- [concept] The seed-dependence of the 7:3 makes the composition itself seed-dependent: three strata on s7/s11, four on v2/s3. The code's claim of robustness is not visible.
- [depth] Flat by canon (De Stijl), but the flatness is not declared anywhere on the sheet or in NOTES. Undeclared.
- [craft] The serpentine block fills show white banding (r04_a3) and beaded edges on every vertical rule, so the solid masses are not solid.

## Next versions
1. **boogie-woogie** (lens) — Switch the canon's late period: *Broadway Boogie Woogie*. Each horizontal rule becomes a street made of the 240 actual test particles as small square cells. A surviving lane is a black/white cell; a swept lane is a coloured cell whose hue is the resonance order. The Kirkwood gaps then appear as coloured *runs* along every street, repeated per stratum, instead of three isolated blocks. Every lane on the sheet is a particle, the white still carries the belt, and the empty lower-left becomes a rhythm rather than a void. It stays De Stijl, and the measurement becomes countable.
2. **true-mass Mondrian** (faithful) — Keep the r04 mapping but make it paint like Mondrian:
   - Blocks are solid fills with overlapping passes and no banding.
   - Stratum height ∝ √strength (stated on the sheet), so blue and gold become masses of at least ⅓ the red's area.
   - The title is set as solid-weight type confined to its own stratum left of the full-height bar.
   - The caption is enlarged to ≥ 3.5 mm and the twist gets its own line.
   - Rules extend to the frame on all four sides.
3. **the belt, counted** (mechanism) — Invert the joke. Draw the 240 surviving orbits as hairline verticals at their true *a*, ink density ∝ survival; the swept bands then stay unpainted white slots. The only colour is one thin rule at each Kepler-III position, in red / blue / gold by order. This is less De Stijl and more laminar. It shows the evidence directly and lets the gaps be literal emptiness. Use it if the Mondrian joke is judged too dependent on the caption.

**If only iterating:**
- End the 2:1 full-height bar at the field line, or set the title entirely left of u 0.74, so no letter and no caption word is cut by a rule.
- Map stratum height to √strength (print the rule in the caption) so the blue block is ≥ 30 × 30 mm and the gold ≥ 20 × 25 mm on A4.
- Set the caption at ≥ 3.5 mm cap height, put `THE WHITE IS THE BELT.` on its own line directly under the title, and put all four ratio labels on one shared baseline just under the field line.
