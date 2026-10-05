# NAVIER-STOKES — description

| | |
|---|---|
| gallery | `gallery/studio/millennium_navier_stokes` |
| current render | `pp_millennium_navier_stokes_abstract_v16_a4.png` (A4 fallback of the r02 A3 trial `_abstract_v15`; r02 HANDOFF files it under `current/`) |
| source | `studio/millennium-navier-stokes/rounds/r02/piece.py::navier_stokes_blaze` |
| paper · pens | A4 portrait, cream, margin 15 · 0 royalblue 0.3 = 3D Burgers streamlines (hero + 4 half-scale rungs) · 1 black 0.1 = 2D Lamb–Oseen rings · 2 black 0.3 = all type · 3 crimson 0.5 = empty limit ring + `WITHOUT A PUSH: OPEN` · order blue → black rings → black type → red |
| status | r02 abstract thesis, ledger rank 3 of 3 (art FAIL · science FAIL) · no FEEDBACK.md · plate 3 of the MILLENNIUM series · route: translator → r04 |

## In one line
A whirlpool drawn twice: flat, it is **only a target of closed black rings**; in three dimensions it becomes a blue inward spiral that repeats itself at half, quarter, eighth and sixteenth size down a diagonal, ending at an empty red circle where the Navier–Stokes question lives.

## Lede
A whirlpool drawn twice: flat, it is only closed rings; in three dimensions it is a **spiral that repeats at half size**, down to an empty red circle.

## On the sheet
A large royal-blue spiral winds inward at the upper left, its left side cut by the margin. At upper right sits a fine black target of concentric rings. Four ever-smaller blue copies of the spiral step down a diagonal to the lower right, ending at an empty crimson circle. Black captions label each form; the title runs across the top.

## The science
The black rings are the exact streamlines of a flat Lamb–Oseen vortex, which cannot blow up. The blue spiral is the Burgers vortex, a real 3D solution, whose inward curl comes from stretching along the axis. The ladder uses scaling symmetry: copies, not a simulated collapse. The geometry shows that symmetry only; the 2026 claim and the open question are stated in text.

## What is on the sheet
- **Title** top-left: `N A V I E R - S T O K E S` spaced caps, u ≈ 0.07–0.93, v ≈ 0.08; statement at v ≈ 0.13: `FLAT, A WHIRLPOOL IS ONLY RINGS. THE SPIRAL IS THE THIRD DIMENSION, AND IT CAN KEEP SHRINKING.`
- **Hero spiral (blue, dominant).** Evenly spaced streamlines winding inward to a small bare eye at (0.22, 0.35); radius ≈ 0.26 W, spanning v ≈ 0.18–0.54, sliced off by a straight vertical edge at the left margin (u ≈ 0.07). Outer lines run almost radially, then wrap into one tight coil of about two turns. Caption beneath at u 0.07, v ≈ 0.56–0.58: `IN SPACE: A SPIRAL` / `SEEN DOWN THE STRETCHING AXIS` / `THE FLUID LEAVES THROUGH THE PAGE`.
- **Ring disc (black hairline).** About fourteen concentric circles centred at (0.755, 0.31), radius ≈ 0.12 W, wide empty eye, gaps narrowest in a middle band. Caption above, flush right at u 0.93, v ≈ 0.16–0.18: `IN THE PLANE: RINGS` / `THE EYE ONLY OPENS` / `PROVED SMOOTH`.
- **The ladder (blue).** Four copies of the hero, each half the previous size, step down a straight diagonal: (0.52, 0.61), (0.67, 0.73), (0.745, 0.79), (0.78, 0.83). The third is a crown of short strokes; the fourth, a few stubs. Caption flush right, v ≈ 0.59–0.62: `THE SAME SOLUTION` / `AT 1/2, 1/4, 1/8, 1/16` / `NS SCALING: COPIES,` / `NOT ONE INSTANT`.
- **The red ring** at (0.82, 0.86), ≈ 0.075 W across, empty, just past the last rung.
- **Terminus block**, flush right on u ≈ 0.765, v ≈ 0.86–0.91: `IF THE LADDER FINISHES, IT FINISHES HERE,` / `IN 4/3 OF THE FIRST RUNG'S TIME.` / `THE PEN STOPS AT 0.8 MM FIRST.`, then in black `CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH` / `FORCED CASE NOT YET VERIFIED · CLAY: NO AWARD`, and in red `WITHOUT A PUSH: OPEN`.
- **Notes corner** bottom-left, v ≈ 0.93–0.94: `BURGERS 1948 / LAMB-OSEEN / RE = 100 / CORE 13 MM` / `IN 2D, ENERGY RUNS TO LARGER SCALES (KRAICHNAN 1967)`.

## The science it encodes
The Navier–Stokes problem asks whether a smooth, finite-energy 3D flow can, on its own, concentrate until velocity becomes infinite at a point in finite time. In 2D this is proved impossible, and the black disc shows why: the streamlines of a planar vortex (Lamb–Oseen) are exact closed circles, and its core only widens with time. The rings are spaced at equal steps of the stream function, so their spacing encodes speed — tightest where the swirl is fastest.

The blue hero is the Burgers vortex, an exact steady 3D solution, seen down its axis. Its streamlines genuinely spiral inward because fluid is stretched out along the axis — through the page. That stretching is the one mechanism absent in the plane, so the spiral is the visible footprint of the third dimension. Every curve is computed from the closed-form streamline, not drawn freehand.

The ladder uses the equations' scaling symmetry: halve the size and the same vortex reappears, congruent, with vorticity ×4 and a lifetime ÷4; the rung times sum to 4/3 of the first. These are copies, as the caption says, not a simulated collapse — Burgers itself never blows up. The red ring marks where an endless ladder would finish; the smaller rungs fall below the pen's 0.8 mm resolution, so it stays empty. The headline's "it can keep shrinking", the 2026 claim and the open unforced case are stated in text only; the geometry shows the symmetry, not an answer.

## How it got here
r02 was the abstract thesis, run in parallel with r01's faithful plate: the same exact vortex families, but on a straight diagonal (orbit factor 1.20), with no side view, type on the margin axes and the hero cropped on the left; this A4 render is the scaled fallback of its A3 trial `_v15`. Critics failed it on the headline asserting the open answer and on a density reversal at rungs 3–4, and called the ladder "a string of blue badges", yet its hero (eye on paper, 2+ turns visible) and off-axis ring disc were judged the best of all rounds. r03 fixed every science mandate from it but lost the hero's eye to a deeper crop, so the ladder-as-badges problem has gone to the translator for an encoding v2 before r04.
