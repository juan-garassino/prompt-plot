# Art critique — ising r04 · canon: science_poster · 2026-09-28
render: ~/Downloads/pp_ising_r04_iterate_v5.png (gcode beside it; A4 landscape, cream; seed sweep s3/s13 glanced, same structure)

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | Vertical CRITICAL (18 mm cap, 3 passes) + ruled sea is the dominant mass, red coast a clear second. The third tier fails: "TC IS A PLACE" sits in the footer at footer size, and the 1/2/3-pass hull rungs look the same weight at 1 m |
| 2 | grid & alignment | 7 | Rules start on the title's right edge (x≈36), cold wall at x=10, ruler on the top drawable edge, footer flush-left on the cold wall. But the footer is set *on* the sea rules with about 0.6 mm between baseline/cap and the rule, so it reads as ruled-notebook type and not type on a grid |
| 3 | tension & asymmetry | 7 | Hard left-heavy mass against a light right, and the coast is a working vertical. No diagonal, and the right half gives the mass nothing to push against |
| 4 | negative space | 6 | Bare paper now exists (x 250–287 is empty full-height), but it is not shaped: from T/Tc 1.2 to 1.55 there are about 10 same-size islands, then blank. It reads as the data running out. Upper-left pocket x 57–95, y 165–185: sea rules stop 20–35 mm short of the red hull, so the ruling looks unfinished. Footer lines are crowded against the rules |
| 5 | craft for pen | 7 | 2 pens, 1 colour change. Draw 11.5 m, travel 6.3 m (0.55×), 685 lifts. No coincident overdraw between distinct hulls (measured). Pass offsets are 0.10–0.15 mm, so on a real nib the rungs fuse into one line and the weight ladder is lost. Footer type clearance to rules is under 1 mm |
| 6 | concept legibility | 7 | Order, then coast, then break-up reads, and the red coast as "Tc is a place" is a real twist. Not a schematic, but the hot side does not say hot: islands at 1.4 are no smaller than at 1.15. Temperature is only legible through the ruler, which is chart furniture |
| 7 | depth & dimensionality | 6 | Declared flat (accepted). But the one device that would give flatness planes, the weight ladder, is invisible, so the field is one uniform hairline plane |

avg **6.71** · min **6** · VERDICT: **FAIL**

## Reads at a glance
A tall word CRITICAL beside a ruled black block whose right edge is a jagged red coastline. The coast breaks into black jigsaw islands that thin out to blank paper on the right.

## Acceptance checks
No encoding.md. Checks taken from the brief (`studio/physics/ising.md`, r01-era, partly superseded by the COOLING STRIP route) and the LINEAGE rule:
- Walls/hulls drawn, never spins or filled squares — **PASS**
- Line weight = size of domain, all rungs legible at 1 m — **FAIL** (populated per HANDOFF, visually one weight)
- Red scarce and loud, one long-range object — **PASS** (1 connected coast: 3 passes × 600 mm, plus the 1.00 tick/label; 16 % of draw)
- Two pens, one swap — **PASS**
- Stroke-font charset only — **PASS**
- `TC 2.269185 ONSAGER 1944 EXACT` on the sheet — **FAIL** (Tc value absent)
- Declared quiet zone — **PASS** (exists, but see dim 4)
- LINEAGE: would hold hung beside Nees's *Schotter* — **FAIL**. In Schotter the disorder is the same element progressively displaced. Here the disorder is absence, and the element does not visibly change across the hot half.
- AUTHORING §6 — N/A (no reference)

## Biggest weakness
The second axis is not drawn. T/Tc 1.2→1.8 is carried by "cluster size", but the drawn islands at 1.15, 1.3 and 1.5 are the same size, and past 1.55 there is nothing. The plate shows order and a coast, then stops. It does not show heat.

## Mandates
1. **Make the hot half visibly hot.** Across three x-bands (T/Tc 1.15–1.35, 1.35–1.55, 1.55–1.80) the drawn marks must visibly shrink and thin left to right. Draw the 10–29-site FK clusters as single short touches (≥ 2 mm, no dots) and fade them with T. Test: mark count and mean mark size strictly decrease band to band; the 1.55–1.80 band has at least one mark in most 20×20 mm cells yet stays ≥ 50 % bare (A2/A4 must stay fixed).
2. **Make the pass ladder read at 1 m.** Test: in the render, a ≥155-site hull stroke measures ≥ 2.5× the width of a 30–49-site hull stroke, and the bold continents at x 95–130 separate from the islands around them at arm's length. Widen the pass spread until the 3-pass band inks solid (≈0.6–0.8 mm), without breaking the ≥ 0.8 mm clear gap between distinct hulls.
3. **Clear the type off the rules and give it tiers.** Test: every footer text line has ≥ 1.2 mm bare paper above and below it (halo the rules around each line, or stop them 3 mm past the line's end), and "TC IS A PLACE" is set at cap ≥ 5 mm as its own line, separated from the 10-line colophon. While re-setting the colophon, add `TC 2.269185 ONSAGER 1944 EXACT`.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A2 | FIXED | 40×40 mm crop x 230–270, y 20–60: no isolated dots, ≥ 50 % bare; travel/draw 0.55; footer says `SINGLE SPINS NOT DRAWN NOR UNDER 30` |
| A4 | FIXED | x 250–287 mark-free full height; a ~60×80 mm mark-free block exists around x 228–287, y 55–135 |
| A6 | FIXED | HANDOFF carries `canon:`, `lineage:` (Schotter), `declared: flat` |
| A9 | FIXED | thicket replaced by closed hulls; no solid cells; pairs < 0.8 mm are only intended same-hull pass offsets and the title's 3 passes |
| A10 | FIXED | CRITICAL cap ≈ 18 mm, 3 passes (x 15.0/15.3/15.6), flush-left at x=15; no rule stub left of the C (set vertical, bottom-to-top) |
| A11 | FIXED | free clusters are closed dual-lattice hull loops; nothing reads as circuitry |
| A12 | FIXED | crimson has 1 coast component (3 × ~600 mm passes); the other small components are the 1.00 tick and label glyphs only |

## Regressions vs compare-to
- **The temperature gradient on the hot half is gone** (pp_ising_COOLING_STRIP_v9). The parent's 1.2→1.8 zone visibly coarsened to fine grain. The A2/A4 fix overshot: the grain was deleted, not thinned, so the right 40 % now reads as missing data instead of heat.
- **Ruled sea continuity:** in v9 the rules ran almost to the coast everywhere. In r04, rows y 165–185 stop at x≈57–60 while the hull sits at x 95–127, leaving an unexplained pocket in the upper-left.
- **"TC IS A PLACE" demoted:** in v9 it was a separate line under the title. Now it is the first line of the footer block at footer size, and the second tier of hierarchy is lost.
- DESCRIPTION § Keep: crimson single coastline — still true. Weight ladder = domain scale — PARTIAL (encoded, not visible). Dual-lattice staircase walls ≥ 1.07 mm — still true. Hero cropped top/right and the empty 1.00 plate — superseded by the COOLING STRIP layout (deck deleted under A1); only the red 1.00 tick remains of the plate idea.
- Gains to keep: draw 20.8 → 11.5 m, travel 20.4 → 6.3 m, commands 49k → 12.8k; dot carpet gone; one clean coast.
