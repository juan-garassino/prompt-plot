# ORBITAL RESONANCE — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/orbital_resonance` |
| current render | `gallery/studio/orbital_resonance/current/pp_orbital_resonance_v9_s7.png` (+ `.gcode`) |
| source | `studio/orbital-resonance/rounds/r01/piece.py::orbital_resonance_belt` — the current render is r01 (its gcode stats equal `trials/pp_orbital_resonance_r01_s7.gcode`: 27 148 commands, 24.6 m draw). The later rounds are separate theses: r02 `resonance_rank` (see `studio/resonance-rank/`), r03 `resonance_lattice` (see `studio/resonance-lattice/`), r04 `composition_with_nothing` (De Stijl, "COMPOSITION WITH RED YELLOW BLUE AND NOTHING") — **r04 has no render on disk** |
| brief | `studio/astro-01/orbital-resonance.md` |
| paper · pens | A4 portrait, cream · 0 black = the orbit arcs · 1 crimson = the five Kepler-III prediction arcs + one caption line · 2 black (a finer nib) = type, scale ray, footer |
| status | unreviewed (no FEEDBACK.md) · 19 renders on disk |

## In one line
Kirkwood gaps drawn as **nested arcs with defects**: a uniform comb of real integrated orbits seen from above, each arc solid if it holds its lane, frayed into dashes as its measured libration grows, absent when swept — so the gaps are carved by the dynamics and five crimson arcs set by arithmetic alone land inside them.

## What is on the sheet
Coordinates are (u, v) on the 210 × 297 sheet, top-left origin.

- **The arc field (dominant mass).** ~140 concentric black arcs about a centre off the sheet past the bottom-left corner, filling the lower two-thirds: at the left margin they run from v ≈ 0.29 down to v ≈ 0.82, at the right margin from v ≈ 0.52 down to the bottom margin (v ≈ 0.96). Every arc crops on at least one side and bottom margin, so the field is a quarter-disc band sweeping down-right. Pitch ≈ 1.2 mm. Inner arcs are solid and read as a dark, even slab; outward the arcs break into fixed-length dashes (~5 mm) with growing gaps.
- **The canyons.** Four white gaps cut through the field, each with a frayed shoulder of dashes on both sides: a thin one at the left edge v ≈ 0.70 (4:1), a wide ragged canyon starting at v ≈ 0.53 on the left and widening to ~8 mm as it runs to the right edge near v ≈ 0.68 (3:1, the loudest), and two thin ones at v ≈ 0.40 (5:2) and v ≈ 0.35 (7:3). Above v ≈ 0.29 (left) the field frays out entirely into a band of loose dashes and then nothing: the outer edge.
- **The top-right void.** Between the frayed outer edge and the title block, a quiet wedge ~40 % of sheet width, empty except the crimson 2:1 arc.
- **Crimson prediction arcs (pen 1).** Five dotted crimson arcs on the same centre: 2:1 runs through the empty void from (0.13, 0.23) to the right margin at (0.95, 0.45); 7:3, 5:2, 3:1 and 4:1 run inside the four canyons, each starting just right of its label and running to the right or bottom margin.
- **Ratio labels.** Flush-left column at u ≈ 0.05: `2 : 1` (v 0.22), `7 : 3` (v 0.35), `5 : 2` (v 0.40), `3 : 1` (v 0.52), `4 : 1` (v 0.69), each at the arc it names; halo knockouts open the field around them.
- **Scale ray.** A dotted black radial ray running up-right from about (0.56, 0.64) to (0.77, 0.37), ticked with `2.50`, `3.00`, `3.28`; a separate `2.00` sits in the field at (0.48, 0.80). Each tick label knocks a small hole in the arcs.
- **Title block (top-left).** `ORBITAL` / `RESONANCE` in large spaced monoline caps, u 0.05–0.73, v 0.05–0.14. Top-right: `KIRKWOOD 1866` spaced small caps at (0.70–0.95, 0.05).
- **Caption** (4 lines, u 0.05–0.71, v 0.15–0.18): `A UNIFORM COMB OF 225 ORBITS. 300 JUPITER YEARS.` / `SOLID HOLDS ITS LANE. DASHED LIBRATES. ABSENT IS SWEPT.` / `BEYOND 3.1 AU NOTHING HOLDS ITS LANE. THAT IS THE 2:1.` / (crimson) `CRIMSON. PREDICTED FROM THE INTEGERS ALONE.`
- **Inner void.** Bottom-left wedge under the innermost arc, u 0.05–0.45, v 0.82–0.93: bare paper.
- **Footer** (two pairs of lines at v ≈ 0.94–0.96): left `CR3BP. MU 9.5388E-4. VERLET DT 0.02.` / `LIBRATION IS THE SPREAD OF MEAN A.`; right `SUN AND JUPITER ONLY.` / `140 OF 225 SURVIVE`. The right footer sits on top of the arc field (knocked out by halos); the left footer's last words butt against the arcs.

## The science it encodes
From the piece docstring and `rounds/r01/NOTES.md`: a planar circular restricted three-body problem (Sun + Jupiter, μ = 9.5388e-4), integrated with velocity-Verlet (dt = 0.02, 300 Jupiter years) for 225 test particles on a comb uniform in a over 1.70–3.80 AU at e₀ = 0.18. Each orbit's osculating semimajor axis is boxcar-averaged over one period, and its **libration width** Δa = max ā − min ā is the signal. It is compared against a running-median background and a lane pitch: dash duty = 1 − 0.85·max(0.45·L, (X−1)/0.7); dropped when max(L, (X−1)/1.4) ≥ 1. Crimson arcs are Kepler III only: a = a_J (q/p)^(2/3) → 2.065 / 2.501 / 2.825 / 2.958 / 3.278 AU. Measured voids at seed 7: 4:1 2.04–2.06, 3:1 2.47–2.52, 5:2 2.81–2.83, 7:3 2.94–2.95, everything from 3.10 AU outward (2:1 overlap zone); 140/225 survive, and seeds 3 and 11 give the same boundaries. The radial scale is exact and single (no break). Honest caveats in the notes: no Saturn (no ν₆), 300 yr shows the lock not the removal, outer edge at 3.10 AU instead of 3.28. The render shows all of this: the gaps are visibly carved and the crimson lands in them. Jupiter itself is not on the sheet.

## How it got here
- **v1**: labels sat inside the field, footer text overprinted the arcs, and dashes lined up vertically across neighbouring arcs into a false grid (phase randomisation fixed that in v2).
- **v5–v8**: the current layout arrives — flush-left ratio column, title + 4-line caption, scale ray, halo knockouts. v6 s11 pushed the outer frayed band higher (to v ≈ 0.25). Variations after that are seed and small ink-ramp changes.
- **r01 s3/s7/s11 = v9**: same layout; the notes self-score Hierarchy 7, Grid 8, Tension 8, Space 9, Craft 6, Concept 7, Depth 6 (declared flat, RADIAL DATA-VIZ canon).
- The family then branched rather than iterated: r02 organ rank, r03 lattice, r04 De Stijl. No feedback from Juan on any of them.

## Keep — what works
- The mechanism is the drawing: gaps are absences carved by an integration, and the crimson is placed independently. That is the rare "emptiness is the measurement" plate.
- The 3:1 canyon at v ≈ 0.53–0.68 is ragged, wide and diagonal. It is the plate's one real tension line; keep its fraying shoulders.
- The off-sheet centre (past bottom-left) makes every arc crop and sweep one way. There is no centred subject.
- Negative space is data: the top-right void is the 2:1 overlap zone, and the lone crimson 2:1 arc crossing it is the loudest single mark.
- The flush-left column (title, caption, all ratio labels, left footer) shares one edge at u ≈ 0.05.
- One radial scale for every mark, and halo knockouts so type never crosses ink.

## Weak — what doesn't
- [hierarchy] The dominant element is a texture, not a form: an even slab of 1.2 mm arcs with no silhouette. At 3 m it reads as a grey quarter-disc with scratches.
- [concept] The cause is absent. Jupiter never appears, and a radial field with a ticked scale ray (u 0.56–0.77) sits right on the schematic/figure line. The tick labels `2.00`/`2.50`/`3.00`/`3.28` are axis furniture.
- [craft] 24.6 m draw against 28.3 m travel and ~2 200 pen cycles: the dash comb means thousands of lifts, which is exactly Leo's ink-drag risk.
- [space] The right footer (`SUN AND JUPITER ONLY` / `140 OF 225 SURVIVE`) is knocked into the densest arcs at the bottom-right. The left footer abuts arcs at u ≈ 0.52. Both read as type fighting the field.
- [depth] Declared flat, but nothing layers except the knockouts. The ink ramp is the same darkness from the inner edge to the 3:1, so the body has no lit edge.
- [tension] The four inner canyons (4:1, 5:2, 7:3) are hairline and read as noise next to the 3:1. The composition leans on a single gap.
- [grid] `KIRKWOOD 1866` top-right floats on its own, sharing no line with the title's cap height.

## Next versions
1. **jupiter-in-the-corner** (mechanism) — keep r01's field exactly and add the cause: a declared radial break with Jupiter as a crimson disc cropped at the top-right corner, and one resonant orbit's libration drawn as a crimson swing across the 3:1 canyon. The top-right void stops being leftover, the plate gets a second mass, and hierarchy moves from a texture to cause → effect.
2. **composition-with-nothing** (abstract) — render r04 (De Stijl orthogonal subdivision: rule weight = libration width, stratum height = resonance order, colour painted on the swept bands). It carries the twist the rubric asks for ("the coloured blocks are the NOTHING") in a canon that is flat by nature. It has never been rendered, so it is the cheapest unexplored thesis.
3. **belt-as-body** (faithful) — keep the r01 map but push the ink ramp (inner belt darker, outer lighter) and replace the dash comb with a few long continuous runs per arc broken once per libration excursion. That halves the travel, and the field reads as a lit body with a frayed rim instead of an even slab.

**If only iterating:**
1. Pull both footers onto one baseline in the bottom-left quiet wedge (u 0.05–0.45, v 0.90–0.95) so no footer text sits on arcs.
2. Delete the tick labels `2.00`/`2.50`/`3.00` and the dotted ray. Keep only `3.28` on the crimson 2:1, and let the ratio column carry the scale.
3. Cut travel below draw: minimum dash length 8 mm, and drop dashes shorter than 2 mm on the fraying shoulders, so pen cycles fall below ~1 200.
