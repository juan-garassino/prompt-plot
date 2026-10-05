# ORBITAL RESONANCE (lattice with defects) — description

<!-- written 2026-09-28 from a vision review. This is the spec the studio workflow iterates from: edit it freely. -->

| | |
|---|---|
| gallery | `gallery/studio/resonance_lattice` |
| current render | `gallery/studio/resonance_lattice/current/pp_resonance_lattice_v2.png` (no gcode on disk) |
| source | `studio/orbital-resonance/rounds/r03/piece.py::resonance_lattice` (the batch listed none: this is round r03 of the **orbital-resonance** family, not a sibling of the attention "resonance" plates) |
| paper · pens | A4 landscape, cream · 0 black = the lattice · 1 crimson = four Kepler-III threads · 2 black (finer nib) = type |
| status | unreviewed (no FEEDBACK.md) · 2 renders on disk |

## In one line
Kirkwood gaps drawn as **a lattice with defects**: one column per test orbit, one row per strobe of Jupiter's period. Columns are vacant where the period is commensurate with Jupiter's, and the neighbouring columns snake by exactly their measured libration, so each vacancy channel carries a relaxation field.

## What is on the sheet
Coordinates are (u, v) on the 297 × 210 sheet.

- **The lattice (dominant mass).** A sheared parallelogram band of quadrilateral cells, leaning ~50° up-right. Its bottom edge is a horizontal line at v ≈ 0.88 from u 0.04 to u 0.52, and its top edge is at v ≈ 0.31 from u 0.35 to u 0.82. It has about 40 rows at ~3 mm pitch, with cells ~2 mm wide. It splits into four blocks:
  - **Block 1 (inner belt)**, u 0.04–0.16 at the foot to 0.35–0.47 at the head: clean regular grid, the calmest zone.
  - **3:1 channel**, a white diagonal lane ~4 mm wide with a solid crimson thread down its middle, from (0.18, 0.88) to (0.49, 0.31). The block edges on both sides visibly bulge toward and away from the thread (the relaxation snake).
  - **Block 2**, regular but with more wobble near its right edge.
  - **5:2 and 7:3 threads**, from (0.36, 0.88)–(0.67, 0.31) and (0.43, 0.88)–(0.74, 0.31). The channels are barely open: cells touch the crimson on both sides, and the narrow block 3 between them is crumpled.
  - **Block 4 (outer)**, u 0.44–0.52 at the foot to 0.75–0.82 at the head: cells collapse into crossing, non-quadrilateral polygons. Its right edge is a ragged sawtooth.
- **The 2:1 void.** An empty wedge right of block 4, holding a lone crimson thread from (0.61, 0.88) to (0.93, 0.31). It is the loudest quiet on the sheet.
- **Ratio labels** above the head of each thread at v ≈ 0.29: `3 : 1` (u 0.47), `5 : 2` and `7 : 3` run together as `5 : 27 : 3` (u 0.64–0.72), and `2 : 1` (u 0.93).
- **Title block (top-left).** `ORBITAL` / `RESONANCE` large spaced monoline caps, u 0.03–0.37, v 0.05–0.14. Caption at v 0.18–0.20: `A SITE IS ITS ORBIT. ITS PLACE IS ITS SEMIMAJOR AXIS.` / `COMMENSURABLE COLUMNS ARE FORBIDDEN. THE REST RELAX.`
- **Top-right**, right-aligned to the margin: `68 OF 96 SITES OCCUPIED` (v 0.07) over `KIRKWOOD 1866` (v 0.09).
- **Footer (bottom-right)**, u 0.48–0.97, v 0.91–0.93: `CIRCULAR RESTRICTED 3-BODY. MU 9.5388E-4. VERLET DT 0.02. 300 JUPITER YEARS.` / `ROWS ARE STROBES OF JUPITER. RELAXATION DRAWN AT TRUE LATTICE SCALE.`
- **Quiet zones.** A large empty triangle at top-left under the caption (u 0.03–0.33, v 0.22–0.75), and the 2:1 wedge at right.

## The science it encodes
From the r03 docstring: r01's integration, unchanged (planar CR3BP, μ = 9.5388e-4, velocity-Verlet, 300 Jupiter years), with 96 test particles. A column's x is the orbit's measured mean semimajor axis at that strobe, and a row is one strobe of Jupiter's period. Vacant columns are the commensurate ones, and the neighbours snake "by exactly the libration the integration measured, at true lattice scale, with no gain applied". The crimson threads are Kepler III only. On the render, the snake is visible at the 3:1 channel edges and as the crumpling of the outer block, which is the 2:1 overlap zone's chaos made visible. 5:2 and 7:3 do not read as vacancies. The shear itself (why the band leans) is not explained on the sheet.

## How it got here
- **v1**: the outer blocks were only horizontal rungs with broken, ragged verticals, so the lattice dissolved into floating dashes right of the 5:2.
- **v2 (current)**: the verticals are closed into full cells everywhere, so the outer block reads as a crumpled mesh instead of scattered rungs. It gains a continuous material and loses some of the "breaking apart" reading.
- No feedback from Juan.

## Keep — what works
- The ORDER is right, and it is the one the rubric names: lattice-with-defects. Nothing is depicted.
- The gradient from a perfect grid (block 1) to a crumpled mesh (block 4) to nothing (the 2:1 wedge) is the whole physics as one left-to-right read.
- The 3:1 channel, with bulging edges and a crimson thread, is the best "defect with a relaxation field" on the sheet.
- The lone crimson 2:1 thread in the empty wedge.
- The shear gives the sheet a working diagonal, and the band crops nothing, so it is an object on the field.

## Weak — what doesn't
- [concept] 5:2 and 7:3 are not vacancies: the cells touch their crimson threads, and the labels collide into `5 : 27 : 3`. Two of four claims are invisible.
- [hierarchy] The lattice is one even-weight mesh. Nothing distinguishes a snaking column from a still one except geometry that needs 30 cm.
- [space] The top-left triangle (about a quarter of the sheet) is leftover rather than shaped. The title block floats in it with no relation to the band's edge.
- [craft] Block 4's crossing, collapsed cells put ink on ink in a 3–5 mm tangle (u 0.60–0.80, v 0.35–0.75). Many edges there fall under 0.8 mm.
- [grid] The labels sit at v 0.29 on the head line, but the footer and title share no edge with the band. `68 OF 96 SITES OCCUPIED` and `KIRKWOOD 1866` are two sizes stacked on one right edge.
- [depth] Flat with no declaration. Line weight does not change with relaxation magnitude.

## Next versions
1. **relaxation-weight** (mechanism) — keep the lattice and make the snake the loudest thing: draw each column's stroke weight (1–3 passes) proportional to its measured libration, so the columns around every vacancy thicken into dark halos that fade with distance. Hierarchy then comes from the physics, and 5:2 and 7:3 read even where the channel is narrow.
2. **unsheared-crystal** (abstract) — drop the shear: an upright crystal lattice (rows horizontal, columns vertical) cropped at the top and bottom of the sheet so it is infinite in time, with the vacancy channels as true vertical white columns. The dislocation field stays exact, and the plate reads as a crystal defect micrograph in a Swiss grid.
3. **lattice-meets-belt** (lens) — hybridise with r01: the lattice rows bent onto the belt's arcs, so each strobe row becomes an arc and the vacancy channels become the canyons. It keeps r01's sweep and gains r03's crystalline order.

**If only iterating:**
1. Separate the `5 : 2` and `7 : 3` labels (stagger one above the other, or set them at the foot) so they never touch.
2. Clear a 2-pitch vacancy either side of the 5:2 and 7:3 threads, so four clear white lanes read at 1 m.
3. Set the title block's baseline on the lattice head line (v 0.31) or its left edge on the band's left edge, so the top-left void is shaped by an alignment.
