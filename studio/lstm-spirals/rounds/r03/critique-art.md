# Art critique — lstm-spirals r03 · canon: undeclared (no `canon:` line in HANDOFF; lineage Duchamp *Rotoreliefs* — judged as Op/kinetic disc work) · 2026-09-29
render: gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.png (gcode beside it; a4 portrait; pens 0 dodgerblue / 1 crimson / 2 black)

## Scores
| dim | score | why |
|---|---|---|
| 1 hierarchy | 6 | Two masses of near-equal size: black vortex (~120×140 mm) is heavier than the red/blue disc (~113 mm across the blue rim, ~86 mm of red). No 3:1 ratio, and the loud mass is the one with nothing to read (see weakness). Title is a clear third. |
| 2 grid & alignment | 5 | Axis at x≈115, 10 mm right of sheet centre: neither centred nor decisively off. Title and footer share the left edge (x≈11–12), but the footer stops at x≈160, not at the axis or the right margin. The axis is broken into four separate ticks (above h_t, inside the black eye, inside the red eye, above c_t), so there is no spine to align to. |
| 3 tension & asymmetry | 6 | The S-sweep works: blue flare out to the upper-left, black tail down to the lower-right, and the waist between them. But both centres sit on one near-central vertical and the red disc is perfectly concentric, so the stack reads static. |
| 4 negative space | 6 | The void at the saddle (x 100–125, y 150–160) is shaped and good. The left third (x 10–50, y 20–255) and right strip (x 175–200) are leftover, not composed. The black tail and the blue fringe graze at x 150–175, y 120–135: crowding, not a chosen overlap. |
| 5 craft for pen | 6 | Spacing is clean outside the title (0.36 % side-by-side, min perp 0.38 mm). Clean 0→1→2 layer order, no re-entry, 3 swaps. But the black layer draws every streamline rim→eye and then flies back out: 4.49 m of travel for 6.17 m of draw, 24 travels over 50 mm, one of 214 mm. Plate total is 7.4 m travel against 13.2 m draw. 81 strokes are under 2 mm (the crumbly blue fringe). In the title, L/S/T are triple-stacked hairlines but the M diagonals are single hairlines, so the weight is uneven. |
| 6 concept legibility | 6 | No schematic. The lower disc lands as a Rotorelief of time: closed red rings (f≈1, keep) alternating with blue in-spiralling bands at t=1,5,10 (writes), rim = first and eye = now. That is a real idea, and the check shows the drawn angles match the trained cell. But the black h_t vortex is a uniform pinwheel: annuli at 31° vs 33° cannot be told apart, so half the plate carries nothing. At a glance it reads as a hurricane or a fingerprint whorl, which is an illustration risk. |
| 7 depth & dimensionality | 5 | Flatness is undeclared. The only depth comes from the funnel pull of the converging black spiral. The red disc is a flat target: no weight fall-off toward either eye, and no over/under where the families meet. |

avg **5.71** · min **5** · **VERDICT: FAIL**

## Reads at a glance
At 3 m a stranger sees a black whirlpool standing on a red-and-blue bullseye, joined at a narrow waist like a snowman. The bullseye's alternating bands invite counting. The whirlpool does not.

## Acceptance checks
There is no `encoding.md` or `BRIEF.md` in `studio/lstm-spirals/`, so there are no §11 checks. The designer's `check_plate.py` (run, not read) reports:
- trained cell drives the plate (i/f/o/g/c/y table over 12 steps): PASS
- drawn angle per annulus matches designed (all 24 annuli within 0.25°): PASS. Note that the black annuli span only 31.2°–33.3°, which is invisible.
- single-centre law, radius ratio per turn = k_t: PASS
- spacing, 0.36 % side-by-side under 0.8 mm, min 0.38 mm: PASS (marginal)

AUTHORING §6 (reference in play; judged as an interpretation):
1. Main forms recognisable without colour: PASS. Vortex over ringed disc on one axis.
2. Lines follow the surface, not a random mesh: PASS. Every family is coherent with its field.
3. Fine lines that are two sides of one thick stroke: PARTIAL. The title glyphs are stacked hairlines; the M diagonals stay single, so its weight breaks.
4. Blackest regions intended: PASS. The title and the black spiral arms are both intended, and the black eye is left open.
5. Labels readable at real pen width: FAIL. The footer is ~2.5 mm caps with subscripts. "BLUE: i_t WRITES" reads as "l_t", and "o_t" in the black clause is a speck.
6. Thicker pen knots corners or fills highlights: PARTIAL. Stacked title corners (L foot, S turns) will knot at 0.5 mm. The black eye and the red eye each carry a black axis tick, which spoils the one highlight each vortex has.
7. Long empty travels / pointless tiny marks: FAIL. Black-layer rim-ward flybacks (4.49 m, 24 over 50 mm) and 81 sub-2 mm crumbs in the blue fringe at x 100–165, y 130–150.

## Biggest weakness
The hierarchy is inverted. The dominant mass on the sheet, the black h_t vortex, is mute: o_t≈0.98 at every step, so its 12 annuli come out as one uniform pinwheel. All the data (the keep/write rhythm) lives in the smaller disc below it. The plate's loudest ink says nothing, and it reads as a weather map.

## Mandates
1. **Make the black vortex carry h_t's sign.** The check table shows y (h) negative for t=1–4, positive for t=5–9 and negative again for t=10–12. Draw the black annuli for t=5–9 with the opposite visible treatment: reversed swirl handedness, or solid vs long-dash. The black vortex should then show three radial bands at 1 m, with the band boundaries at the same step indices as the blue write bands below. Test: count three black bands, and see that their boundaries correspond to the blue rings.
2. **Invert the hierarchy and commit the asymmetry.** Scale the red/blue disc so its blue rim is ≥140 mm across, and shrink the black vortex to ≤0.5× the disc's area. Move the shared axis to x≈130 so the left third becomes the entry zone for the input streams (blue flare and black left arm reach x≈10). End the footer line exactly at the axis x or at the right margin x=200, not at x≈160. Test: at 3 m the disc is plainly the larger mass, and the footer's right end lands on a named line.
3. **Fix the pen job and the marks that read as glitches.** In the black layer, draw alternate streamlines eye→rim (or order by nearest endpoint) so black travel drops below 1.5 m with no travel over 50 mm inside the vortex. Delete the black ticks inside both eyes: leave both eyes as bare paper, and draw the axis either as one continuous rule or not at all. Drop blue fringe fragments under 3 mm. Set footer subscripts so "i_t" cannot read as "l_t". Test: parser shows black travel under 1.5 m and fewer than 20 strokes under 2 mm, and both eyes are empty in a crop.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| none | no LEDGER.md or FEEDBACK.md on file | No A*/J* mandates exist. Against DESCRIPTION.md "Next versions 1" (forget-gate-vortex): red retains its winding — delivered (f≈1 annuli drawn as closed circles); black resets — NOT delivered (the black vortex is uniform, nothing visibly resets); labels/legend shrunk to a footer line — delivered. |

## Regressions vs compare-to (r01 v10)
- **Keep 1, interleaving sheaves: REGRESSED.** r01's best passage (black sheaf down the left into the red lobe, red sheaf up the right into the black) is gone. r03's families stay in separate lobes and touch only where the black tail grazes the blue fringe. The reference's defining interleave is lost.
- **Keep 2, axis as spine: REGRESSED.** r01 had one continuous arrowed rule through both eyes. r03 has four disconnected ticks, two of them sitting inside the eyes.
- **Keep 4, input sequence: REGRESSED.** The six source dots feeding arrowed streams from the left edge are gone. The inputs are now unsourced blue and black arms, and the left third went from labelled quiet to plain empty.
- **Keep 3, two pens as mass: CHANGED on purpose.** Blue is added as "write". The meaning is stated and the layers are clean, so this is not a regression. Red is now the more massive family.
- **Keep 5, crowd control: STILL TRUE.** Slightly worse: 0.36 % side-by-side vs r01's 0.08 %, min 0.38 mm.
- **Improved over r01:** the schematic is removed (gate labels, legend, equations), real trained-cell data is in the geometry, travel is down 10.9 m → 7.4 m, and the type is at poster weight.
