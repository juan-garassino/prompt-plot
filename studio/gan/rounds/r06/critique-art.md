# Art critique — gan r06 · canon: De Stijl, declared flat (Mondrian, *Broadway Boogie Woogie*) · 2026-09-29
render: gallery/studio/gan/current/pp_gan_wildcard_v7.png  (compare-to: gallery/studio/gan/trials/pp_gan_iterate_v16.png, r04)

This is a wildcard round. It leaves encoding rev 1 (Albers weave) for a De Stijl lane plate, so the
§11 checks below are run as written, and most of them cannot pass by construction. It is judged
against STYLES.md §7 and the BBW lineage.

## Scores
| dim | score | note |
|---|---|---|
| 1 hierarchy | 7 | At 3 m the square spiral of coloured lanes reads first. The heavy black double-rule square (x 50–106, y 113–169) competes with it for first read: it is the darkest mass inside the image. The title is third. At 30 cm the lanes reward you: blue runs long and unbroken, crimson/gold beat in short cells. |
| 2 grid & alignment | 6 | The lane block sits on a ~20 mm gutter at the top (tagline→lane 247), the right (181→200) and the bottom (lane 52.4→footer 31.7), and crops at x = 10. That is good. Breaks: the y ≈ 212 lap stops at x 13.2 (3 mm short of the cut edge, so it neither crops nor clears). The step-0 stub (x 107–113, y 157–178) dead-ends in mid-air. `STEP 0` floats inside the square, away from the cell it names. The footer's right column ends at x 192.9, not 200. |
| 3 tension & asymmetry | 7 | The spiral centre (78, 141) sits left of the page axis and the outer lap crops on the left. Blue in NE/SW and crimson/gold in NW/SE make a pinwheel with real drive. But the + is dead-centred in a dead-centred box. |
| 4 negative space | 6 | The channels between laps grow outward (≈9 → 16 → 27 mm), and that spacing is data. But the sheet is ~80 % paper. BBW is a packed field, and here the lanes are thin 6.5 mm threads in an empty room. The black square comes within ≈1.5 mm of the step-0 stub at its top-right corner and ≈5 mm of lap 0's top lane, against 8–10 mm on the other sides. That reads as a near-miss, not a decision. |
| 5 craft for pen | 7 | Serpentine cell fills with ~1.2 mm white, ≈1 mm cell gaps, no ink-on-ink, clean corners. 7,043 commands, travel 5.7 m < draw 15.2 m. 4 pens / 3 swaps (gold → crimson → blue → black). Risks: gold on cream stock will be faint. The lattice title glyphs are malformed (the X in FIXED reads as a boxed H, the S in REPELS as a 5), and the title cap-tops sit on the y 287 margin. |
| 6 concept legibility | 6 | The orthogonal spiral says "unwinds outward from a centre", and in a square spiral the labyrinth twist of the title lands harder than it ever did in the round versions. The stride-vs-clot rhythm (blue long, crimson staccato) is a real encoding in BBW's own language. But it takes a 10-line, two-column legend plus 3 labels in a boxed `+` to decode, and that pushes it toward a keyed diagram. The caption explains rather than confirms (`A SIDE: WHERE THE RUN CROSSED AN AXIS`, `A STEP LANDS ON ITS OWN RAY FROM THE +`). |
| 7 depth & dimensionality | 7 | Declared flat and canon-flat. The flatness serves the lane reading. |

**avg 6.57 · min 6 · VERDICT: FAIL**

## Reads at a glance
A square spiral of thin blue / red / yellow lanes coiling out of a heavy black box with a `+` in it: a Mondrian maze more than a Boogie Woogie, with a heavily keyed footer.

## Acceptance checks
Known failure modes: the subject is not dead-centre overall, but the `+` is dead-centre in its own box. The footer is a furniture checklist: 5 swatch rows plus 5 explanation rows. Colour works as compositional weight (blue masses vs crimson/gold beats), not only as category. Black is the scarce accent, but the square spends too much of it.

Encoding §11 (rev 1, weave), run as written:
1. **A7 flip test: FAIL.** There is no basket ground. The ribbon is a silhouette of lanes on paper channels, which is exactly what §11.1 forbids. The wildcard drops this by design.
2. **A1 + A17 + A18 one body: PARTIAL.** Each lap traces unbroken from step 0 to its crop, with no jogs or L-blocks (A1 intent met). Width is a constant 6.5 mm, not 0.2 ρ, so FAIL on the width rule. Channels between laps are ≥ 9 mm everywhere (pass), but channel ÷ ρ is not checkable against the square metric. No white > 2 mm inside a lane (pass). The y ≈ 212 lap end at x 13.2 is a 3 mm sliver short of the window edge (fail on crop hygiene).
3. **S2 no false float: PASS (sheet side).** No text equates a cell length with a move. The gcode spot-checks belong to the science critic.
4. **S8 + S3 + S1 + S9 truths: FAIL.** `STEP 70 R 1.33 LEAVES THE CLOTH` is absent. The sheet says `STEP 125 R 1.88: FIRST BEAT OFF THE SHEET` (science critic must confirm against the square-lane rule). There is no dashed 360° circle through z_0: the h→0 flow is a solid black square. PASS: one black `+` labelled NASH EQUILIBRIUM / THETA = PSI = 0; on-top key in words (`D SPOTS THE FAKE` / `G FOOLS D`); no turn-taking words; footer below the image.
5. **Hierarchy + accent: PARTIAL.** Black inside the image appears only at the hole (pass). The first read is the quarter-alternating spiral (pass), but the black square competes with it. Graze rule: the y ≈ 212 lap clears the window edge by only 3.2 mm (fail).
6. **Plot: PARTIAL.** Commands 7,043 < 15k and travel < draw (pass). The layer spec differs: 4 layers gold → crimson → blue → black, not blue → crimson → black. Pen-downs and minutes are not stated in HANDOFF.

## Biggest weakness
It is undermassed and over-keyed. BBW's order is lanes that pack the whole rectangle so the beat IS the surface. Here seven thin 6.5 mm lanes of constant weight float in ~80 % paper. The heaviest thing inside the image is the black flow square, not the run. The data rhythm (stride vs clot) is only legible after reading a 10-line legend. The lane widths never grow, so nothing carries the eye outward to the crop, and "repels" rests on spacing alone.

## Mandates
1. **Weight advances outward (A6), and the run outweighs the black square.** Lane width must grow per lap: the innermost lap stays ≤ 6.5 mm and the outermost is ≥ 13 mm, each lap wider than the one inside it, still serpentine at ≤ 2 mm white. Then drop the flow square to a single-pass or dashed black rule so that at 3 m the outer lap, not the square, is the darkest mass. Test: squint at the png. The first black/colour mass you land on is the NE blue L at x ≈ 175–200, not the box.
2. **Crop or clear, nothing between.** The y ≈ 212 lap runs to the x = 10 cut edge like the y 55 and y 245 laps. No lane end may sit 1–6 mm from any window edge (now 3.2 mm). Resolve the square/step-0 near-miss: either the step-0 cell starts ON the square's edge (a shared junction, 0 mm) or it clears it by the same gap used between all cells. The ≈1.5 mm gap at (106, 169) goes. Test: measure every lane end and the square's four sides; each gap is 0, ≈1 mm (the cell gap), or ≥ 6 mm.
3. **The caption confirms, it does not explain.** Cut the footer from 10 lines to ≤ 4: three colour swatches with their words (`D SPOTS THE FAKE` / `G FOOLS D` / `NO STEP`) plus one line of run facts. Delete `A SIDE: WHERE THE RUN CROSSED AN AXIS` and `A STEP LANDS ON ITS OWN RAY FROM THE +`. Move `STEP 0` out of the box so it sits against the step-0 cell, or delete it. The box interior holds only the `+` and its two labels. Redraw the lattice X and S so `FIXED` and `REPELS` read without context. Test: count footer lines ≤ 4, and a stranger reads the title aloud correctly.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S2 | FIXED (by removal) | No float/length claim on the sheet. Lane cells mark landings, and no text equates length with move. |
| S6 | FIXED (upstream) / DEPARTED | encoding.md rev 1 exists, but r06 ignores it (weave → lanes, circle → square, exit step 70 → 125). |
| S8 | PARTIAL | Caption band is outside the image (footer top 31.7 < lane bottom 52.4). Iterate coverage cannot be judged from the png; for the science critic. |
| S9 | FIXED | `A STEP, D AHEAD: D SPOTS THE FAKE` / `A STEP, G AHEAD: G FOOLS D` in words. |
| A1 | FIXED | One continuous lane per lap, no jogs, L-blocks or orphans. Minor: y ≈ 212 lap ends at x 13.2 (mandate 2). |
| A4 | PARTIAL | A ~20 mm gutter module holds top/right/bottom. The interior is leftover paper, and the box interior has 4 floating labels. |
| A5 | PARTIAL | Black is scarce (square, `+`, type), but the square is too loud, and a 4th pen (gold) is added. |
| A6 | NOT FIXED | Lane width is a constant 6.5 mm on every lap. Only the channel grows. (Deferred three times; now mandate 1.) |
| A7 | NOT FIXED (abandoned) | Red Meander lineage is dropped. The figure is a silhouette on paper, the opposite of A7. Acceptable only if the wildcard lineage is adopted by the lead. |
| A17 | FIXED | Channels ≥ 9 mm between all adjacent laps, no interpenetration anywhere. |
| A18 | FIXED (by substitution) | No ladders. Serpentine cells have ~1.2 mm white. |
| A19 | PARTIAL | `MIN G MAX D V[D,G]` is back and the title spans 10–200. Cap-tops still sit on the y 287 margin, and the new lattice glyphs are malformed. |
| r05-1 crosshair seams | NOT FIXED | Colour flips stack on x ≈ 78–80 in all seven horizontal lanes and at y ≈ 142–150 on the right lanes: the cross persists as an aligned seam, though it is less static in De Stijl terms. |
| r05-2 float on cut edge | FIXED | Outer lanes stop at x 180.8 inside a 19 mm gutter. Left laps crop at x 10. |
| r05-3 demote title | FIXED (overshot) | The hollow lattice title is light, but it now loses legibility (X, S). |

## Regressions vs compare-to
- **The h→0 flow lost its truth-read.** r04's full dashed circle through step 0, labelled `h → 0: THE FLOW CIRCLES`, became a solid triple-rule black square. It is the heaviest element in the image and reads as a frame/box, not a flow.
- **Title legibility.** r04's bold stroked title read at 3 m. r06's hollow lattice alphabet misforms X and S.
- **Mass.** r04 (and r05) were a cloth: a dense, textured field. r06 is ~80 % paper with thin lanes, and the plate lost physical presence.
- **Caption bloat.** 4 footer lines → 10, with explanatory lines the r04 critique had already warned against.
- **Exit fact changed** from `STEP 70 R 1.33` (verified by sci r04) to `STEP 125 R 1.88`. The science critic must verify it.
- DESCRIPTION § Keep: the `+` on bare paper still holds (now black, inside a box). `THE FIXED POINT REPELS` / `NEITHER PLAYER EVER ARRIVES` holds. The relief, the split G/D legs and `EQUILIBRIUM / NEVER REACHED` are long superseded (not r06 regressions).
