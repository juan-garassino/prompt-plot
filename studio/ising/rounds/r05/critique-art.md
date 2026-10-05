# Art critique — ising r05 · canon: science_poster · 2026-09-29
render: gallery/studio/ising/trials/pp_ising_r05_iterate_v8.png (gcode beside it; A4 landscape, cream, 3 pens)

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | The ruled black sea, the red coast and the bold 3-pass continents at x 105–175 are the loud mass, and the CRITICAL spine is a clear typographic first. The grey rung adds a real third tier. The right 45 % is one mid-weight grey texture with no internal hierarchy, and `TC IS A PLACE` (~5 mm cap) is squeezed into the footer's middle column |
| 2 | grid & alignment | 7 | Good shared axes: the footer's left column is flush with the spine at x=15, the middle column starts exactly under the red 1.00 tick (x≈105), and the right column ends flush at the field's right edge (x 286.6). Against that, the right column's left edge (x≈187, T≈1.33) sits on no tick. The footer is jammed: about 4 mm between the field bottom (y 27) and the first cap line, and the last baseline about 1 mm off the bottom margin. The ruler labels touch the top margin |
| 3 | tension & asymmetry | 7 | Hard left-heavy mass, one working vertical (the coast), and a weight ramp left to right. Isolated black ≥30-site islands at T 1.4–1.6 give the right side a few accents. There is still no diagonal or crop, and every element sits inside one full-bleed rectangle |
| 4 | negative space | 5 | The sheet has no quiet zone left. The r04 bare hot edge (x 250–287) now carries about 20 grey islands at the same density as T 1.35. Every region from the spine to the right margin is filled edge to edge, and the footer is pressed into the bottom margin. Emptiness exists only as the gaps between confetti |
| 5 | craft for pen | 7 | 3 pens, 2 swaps, clean layers: 0 coincident segments within or across layers. Distinct hulls stay ≥ 1.17 mm apart (measured). Pass offsets are now 0.35 mm, so the ladder is physical. Faults: black strokes cross the crimson coast 46 times and grey strokes cross it 5 times. Examples: sea rules at y 101.8, 119.5, 140.7, 161.9 run past the coast at x≈94–99, and grey hulls poke through the coast at x≈100–108, y 120–135. The 3-pass inward offset collapses into small knots in 1-site necks (28 gaps at 0.12 mm; for example the top-edge cluster at x≈150, y≈185). Travel 9.8 m against 16.6 m draw (0.59×, at the limit), 1151 pen-downs |
| 6 | concept legibility | 7 | Order, then a red coast, then break-up reads in one glance, and "Tc is a place" lands. It is not a schematic. But the dissolve stops halfway: black islands turn grey around T 1.3 and then nothing changes to the right edge. Heat reads as a constant texture, not rising disorder, and the top ruler is still chart furniture carrying the temperature reading |
| 7 | depth & dimensionality | 7 | Declared flat (accepted). The black/grey/paper tonal tiers now give real planes: the grey recedes and the 3-pass continents come forward. The last plane, paper, never arrives |

avg **6.71** · min **5** · VERDICT: **FAIL**

## Reads at a glance
A tall CRITICAL beside a ruled black block whose right edge is a jagged red coast. The coast breaks into bold black islands, then into an even field of small grey islands that runs unchanged to the right edge.

## Acceptance checks
No `encoding.md` (process gap still open). Checks taken from the brief (`studio/physics/ising.md`), HANDOFF's own claims and the LINEAGE rule:
- Walls/hulls drawn, never spins or filled squares: **PASS**
- Line weight = cluster size, rungs legible at 1 m: **PASS** (0.35 mm pass offsets; a 3-pass hull ≈ 0.7 mm + nib, about 3× a single pass)
- Red scarce and loud, one long-range object: **PASS** (1.7 m, 11 pen-downs: the coast plus the 1.00 tick and label)
- Each pen one stated meaning, clean layers, no line shared: **PASS** (0 coincident segments), with the caveat that 51 strokes cross the crimson coast
- Stroke-font charset only: **PASS**
- `TC 2.269185 ONSAGER 1944 EXACT` on the sheet: **PASS**
- A declared, generous quiet zone: **FAIL**
- HANDOFF's own claim "black islands → grey islands → paper": **FAIL**. Paper never arrives. Grey count goes up across the hot bands (20 → 25 → 27 loops) and mean grey loop area is flat (29 → 25 → 24 mm²)
- LINEAGE: would hold beside Nees's *Schotter*: **FAIL**. Schotter's element keeps changing all the way down the sheet. Here the element changes once (black to grey at ~1.3 Tc) and then repeats unchanged for 100 mm
- AUTHORING §6: N/A (no reference)

## Biggest weakness
The grey rung fixed the empty hot half by turning it into wallpaper. From T 1.3 to 1.8 the sheet is one uniform grey confetti, with the same count and size of island in every 20 mm column. So the gradient stops at the second step, the only quiet zone is gone, and the Schotter dissolve has no end.

## Mandates
1. **The grey must fade to paper.** In 20 mm columns from x 180 to x 287, the grey+black loop count strictly decreases column to column. The last column (x 262–287, T ≈ 1.70–1.80) carries ≤ 3 marks and contains a mark-free rectangle ≥ 25 × 60 mm. If the honest cut has to scale with T (e.g. keyed to the correlation length), state the rule in the key. Do not thin by fiat.
2. **The coast is where everything stops.** Zero crossings between the crimson layer and any black or grey stroke (now 46 black and 5 grey). Every sea rule ends ≥ 0.8 mm short of the coast; see the rows at y 101.8, 119.5, 140.7 and 161.9 near x 94–99. No grey hull straddles the coast; see x 100–108, y 120–135. While there, no 3-pass hull may collapse into a knot: passes on opposite sides of a 1-site neck keep ≥ 0.35 mm, or that neck drops to 1 pass (e.g. the top-edge cluster at x≈150, y≈185).
3. **Give the footer and ruler air, on the grid.** Get the room by shortening the field, not by shrinking type. At least 5 mm of bare paper between the field bottom and the first footer cap line. The last footer baseline ≥ 3 mm above the bottom margin. Ruler labels ≥ 2 mm below the top margin. The right footer column's left edge sits exactly under a ruler tick (1.30 or 1.40). `TC IS A PLACE` gets ≥ 2.5 mm clear above it, separating it from the colophon line above.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A2 | FIXED (holds) | No dots or single-site marks anywhere; the grey rung starts at 13 sites. Travel/draw 0.59, just inside 0.6 |
| A4 | REGRESSED | Superseded by A14, but the "shaped bare paper" intent is lost: x 250–287 now holds about 20 grey islands, and no mark-free block ≥ 25 × 60 mm exists on the hot side |
| A9 | FIXED (holds) | Distinct hulls ≥ 1.17 mm apart in all layer pairs (measured). Pairs under 0.8 mm are same-hull pass offsets, plus small neck knots (see M2) |
| A14 | PARTIAL | The letter of the test passes on combined loops: counts 36 → 31 → 29, mean area 51 → 31 → 26 mm² across 1.15–1.35 / 1.35–1.55 / 1.55–1.80. It fails in the eye: grey count rises 20 → 25 → 27 at flat size, so the hot half reads as one texture. Every 20 × 20 cell in the last band has a mark and is ≥ 50 % bare; no dots |
| A15 | FIXED | Pass offset 0.35 mm (was 0.10–0.15). The 3-pass continents read about 3× a 1-pass hull at arm's length. A9 clearance is kept |
| A16 | FIXED | Colophon moved below the field, off the rules. Line gaps ≥ 1.2 mm. `TC IS A PLACE` is its own line at ~5 mm cap. Separation from the colophon line above is only ~1 mm (see M3) |
| A17 | FIXED | Rows y 165–185 now run to x≈110–118, up to the red hull. The pocket is gone |
| S3 | FIXED (art side) | `UNDER 0.80 TC AS DRAWN 0.977 ONSAGER M 0.969` now names a band that is fully drawn. The science critic owns the number |
| S7 | FIXED | CRITICAL moved into its own spine column x 15–33, left of the cold-wall rule. Every row at T 0.70–0.80 runs unbroken from x 36 |
| S8 | FIXED | `TC 2.269185 ONSAGER 1944 EXACT`, `RULE DENSITY IS THE MAGNETISATION M`, `BLANK  DISORDER FINER THAN 13 SITES` are all on the sheet |

## Regressions vs compare-to
- **The hot-side bare paper is gone** (r04 x 250–287 was empty full height). The fix for "the data runs out" overshot into "the data never thins". r04 had the ending and no gradient. r05 has the second step and no ending.
- **New cross-pen collisions:** grey hulls straddle the crimson coast (5 crossings; r04 had no grey), and black rules punch through it at several rows.
- **Footer crowding moved rather than solved:** it is off the rules now, but pressed between the field and the bottom margin (~1 mm clearance).
- **Cost up:** draw 11.5 → 16.6 m, travel 6.3 → 9.8 m, pen-downs 685 → 1151, one more pen swap. Acceptable if the grey earns it, and right now its right half does not.
- DESCRIPTION § Keep: crimson single coastline: **still true** (one coast, but see M2 crossings). Weight = domain scale: **now true and visible** (improved). Dual-lattice staircase walls ≥ 1.07 mm: **still true** (1.178 mm pitch). Hero cropped top/right and the empty 1.00 plate: **superseded** by the COOLING STRIP layout; only the red 1.00 tick survives, and it still works.
- Polish, not a regression: in the spine the `A` diagonals are single hairlines while its crossbar and every other letter are 3-pass. Pick one weight.
