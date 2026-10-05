# CRITICAL — description

<!-- rewritten 2026-09-29 by the studio lead when r07 went to the vote. It describes the CURRENT best version (r07, COOLING STRIP) so the next iteration starts from the truth. The r01 description (the Tc hero + temperature deck + chart) is history: see rounds/r01 and LEDGER.md. -->

| | |
|---|---|
| gallery | `gallery/studio/ising` |
| current render | `gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png` (gcode beside it; seed sweep `_s3`, `_s13`) — pending the curator's sync |
| source | `studio/ising/rounds/r07/piece.py::ising_cooling_strip_r07` (seed 7, a4 landscape, palette black,crimson,gray) |
| paper · pens | a4 landscape, cream · 0 black = ruled sea, free FK hulls ≥ 30 sites (1/2/3 passes), ruler, CRITICAL spine, type · 1 crimson = the held cluster's hull (the frontier) + the `1.00` tick · 2 grey = free FK hulls 13–29 sites |
| plot | black 947 strokes ≈ 47 min → crimson 14 ≈ 3 min → grey 167 ≈ 12 min · draw 12.37 m, travel 0.499× · no shared line between layers |
| status | r07 at vote. Art 7.43/7 FAIL · science 9/8/9 PASS. Fabrication gate clean. Juan's feedback: none recorded |

## In one line
**COOLING STRIP.** One 212 × 129 Ising lattice with temperature running linearly from 0.70 Tc at the left edge to 2.30 Tc at the right edge. The Fortuin–Kasteleyn cluster held by a fixed + wall on the left is drawn as a ruled sea. Its hull is **one crimson coast**, at mean 1.02 Tc: Tc is a *place*. Free FK clusters are drawn as closed outlines, weighted by size. They shrink and thin to the right until heat is finer than the 13-site cut, and the sheet ends in bare paper.

## Lede
A strip of the Ising magnet cooled across its **critical temperature**, drawn so that the critical point appears as a place on the sheet: one ragged crimson coast.

## On the sheet
Giant spaced capitals spell CRITICAL up the left edge, with a thermometer ruler along the top. A dense black ruled sea fills the left, bounded by one ragged crimson coastline. Beyond it, black and then grey closed outlines of smaller clusters thin out to the right until bare paper remains. Footer text in three columns carries the numbers.

## The science
One grid of tiny magnets is simulated with the temperature rising from left to right. How densely the sea is ruled shows how magnetised it is; the outlines are clusters of aligned magnets, sized by pen weight. The crimson coast sits just above the exact critical temperature, and the measured magnetisation matches the exact solution known since 1944 within simulation noise.

## What is on the sheet
Reading order:
1. CRITICAL up the left edge.
2. The ruled black sea.
3. The ragged crimson coast.
4. Black continents and islands just past it.
5. Grey islands thinning into bare cream.
6. The footer.

- **CRITICAL spine**
  - Vertical giant caps at x 15–33 (u 0.05–0.11), spanning the full field height (y 36–188).
  - 3 passes, 18 mm cap. The `A` diagonals are at full weight.
  - Off the lattice.
- **Thermometer ruler** along the field top (y ≈ 189–197)
  - Ticks every 0.05 Tc, labels 0.80 … 2.20, exact to 1e-4.
  - The `1.00` tick and label are crimson and taller, at x 83.6 (u 0.28).
- **The ruled sea** (dominant dark mass, x 37–≈ 90, u 0.12–0.30)
  - Horizontal rules on lattice lines, every 3rd row (43 rows), strictly inside the held FK cluster.
  - Rule density *is* the magnetisation.
  - Rules end 0.85 mm short of the coast.
- **The crimson coast**
  - One continuous 3-pass staircase (±0.15 mm), 352 dual-lattice edges, 1 component, wrapping top to bottom.
  - It wanders x 75–105 (u 0.25–0.35) as a near-vertical ragged wall with small fjords.
  - Nothing black or grey comes within 0.85 mm of it.
- **Black continents / islands** (x ≈ 85–195)
  - Closed hulls of free FK clusters: 30–49 sites at 1 pass, 50–154 at 2 passes, ≥ 155 at 3 passes, grown inward at 0.35 mm.
  - Seed 7 carries one 376-site 3-pass continent against the coast (x 85–110, y 55–165).
- **Grey islands** (x ≈ 90–280)
  - 1-pass closed hulls of 13–29-site clusters, 115 of them on seed 7.
  - Count per band past 1.15 Tc: 44 → 33 → 27 → 10. Mean size: 27.1 → 19.5 → 17.4 → 13.7.
- **Bare paper**
  - The right quarter thins to paper: x 240–287, y 36–110 is mark-free.
  - The last 25 mm column holds 2 outlines.
- **Footer** (y 13–31, 5 lines at 4 mm pitch, three columns hung on the grid)
  - **col 1** (x 15, on the spine axis): `RULED THE HELD FK CLUSTER` … `UNDER 0.80 TC AS DRAWN 0.984` / `ONSAGER M 0.969`.
  - **col 2** (x 83.6, on the red tick):
    - `RED HELD CLUSTER HULL MEAN 1.02 TC`
    - `TC 2.269185 ONSAGER 1944 EXACT`
    - `WEIGHT PEAKS AT TC COUNT PEAKS PAST IT`
    - `TC IS A PLACE` (large).
  - **col 3** (x 177.3, on the 1.60 tick):
    - run metadata
    - `FK SPINS BONDED WITH PROB 1-EXP(-2J/T)`
    - the key (`GREY 13-29` in grey, `1 PASS 30-49` · `2 PASSES 50-154` · `3 PASSES 155+`)
    - `BLANK DISORDER FINER THAN 13 SITES`.

## The science it encodes
2D Ising, J = 1, zero field, Tc = 2/ln(1+√2) = 2.269185.

**Lattice and sampling**
- 212 × 129 lattice at 1.178 mm display pitch, periodic in y.
- The left column is bonded to a fixed + wall. The right edge is free.
- Local temperature T/Tc = 0.70 + 1.60 (i+½)/212.
- Sampled by Swendsen–Wang with FK bonds p = 1 − e^(−2J/T) between aligned neighbours.

**Checks the science critic reproduced on the ink, on seeds 7 / 3 / 13, against an independent SW simulation of the identical lattice**
- The held density under 0.80 Tc: 0.984 against Onsager–Yang 0.969 (sim 0.969 ± 0.008).
- The hull mean at 1.02 Tc (sim 1.038 ± 0.022).
- The per-band outline census, within 1.3σ.
- The count and size peaking apart: size peaks at 1.00–1.15, count at 1.15–1.35.
- The last-column fade: 2 outlines (sim 2.08 ± 1.41).

**Caveats**
- Seed 7's hottest band is fine-grained: mean 13.7 against a sim value of 15.9 ± 1.0.
- The top rung (≥ 155) is populated in only 40–51 % of configurations, so the plate must stay seed 7 (or 3).
- `dossier.md` / `encoding.md` do not exist yet. The r07 science critique's check table is the de facto dossier.

## How it got here
- **r01** (the Tc hero + deck + chart) had no critique.
- **r02** COOLING STRIP and **r03** COASTLINE both FAILed.
- **r04** merged in closed hulls and the vertical CRITICAL spine.
- **r05** added the grey rung. Science PASSed, but the hot half became wallpaper.
- **r06** SUNBURST was the Art Deco wildcard on RG flow. It is kept as a flavour.
- **r07** gave the dissolve its ending:
  - the axis was extended to 2.30 Tc at the same cut;
  - the coast became a wall nothing crosses;
  - the footer got measured air;
  - the stranger lines were added.

Ledger: `studio/ising/LEDGER.md`.

## Keep — what works
- **The ending.** The dissolve reaches bare paper by physics at one printed rule, not by thinning by hand.
- **One crimson coast**, the single long-range object. It is continuous, wraps, and nothing crosses it (0.85 mm clearance, 0 crossings).
- **Line weight = cluster size** (grey / 1 / 2 / 3 passes). A real data ladder, with ≥ 0.8 mm between owners (1.03 mm minimum).
- **Rule density = magnetisation**, with the check printed from the ink (`AS DRAWN` beside `ONSAGER M`).
- **The CRITICAL spine** at the left edge, and the three footer columns hung on the spine axis, the red tick and a ruler tick.
- **Plot contract.** 3 pens, one clean layer each, stated order, travel ≈ 0.5×, ~1 h total.

## Weak — what doesn't
- **[hierarchy]** The crimson coast is a 1-pass-weight hairline beside 3-pass black hulls 1–2 mm away (x 85–100). At 1 m the black out-weighs the red it borders (art r07 M1 → A25).
- **[craft]** 49 black strokes under 4 mm, mostly clip residue beside the coast at x 68–100. There are also open hull ends at the wrap edges and a lone dash at (142.8, 188.4) (A26).
- **[space / tension]** The transition band (0.90–1.35 Tc) gets only ≈ 23 % of the width, so it reads as a knot of parallel black and grey outlines.
  - The coast lost r05's fjords and diagonal. It is now confined to x 75–105.
  - The ruled sea narrowed from ≈ 78 to ≈ 53 mm, and r05's black continent at x 110–175 is gone (A27, A28).
- **[fidelity]** The clearance drops the last held site from each rule run, and a pass from multi-pass hulls, at the coast (S14). The FK line omits "aligned" (S15). The red seam edges are undrawn (S16).

## Next versions
1. **COOLING STRIP r08 (rework)**
   - A printed, non-linear x(T) magnifying 0.90–1.35 Tc to ≥ 45 % of the width.
   - The sea back to ≈ 78 mm.
   - The coast at ≥ the 3-pass black weight.
   - Zero crumbs.
   - Run the translator first to write `encoding.md` + `dossier.md`.
2. **SUNBURST** (flavour, r06): RG block-spin flow as an Art Deco half-sunburst. Its parked mandates are A22–A24 / S11–S13.
3. **COASTLINE** (flavour, r03): the full-bleed critical torus with the coast as the hero.

**If only iterating:** thicken the crimson to the 3-pass band, drop or close every sub-4 mm clipped stroke, and add `INK STOPS 0.85 MM SHORT OF RED` + "alike neighbours" to the key.
