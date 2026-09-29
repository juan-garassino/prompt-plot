# Science critique — gan r06 · machine learning (GAN training dynamics, game theory) · 2026-09-29
render: gallery/studio/gan/current/pp_gan_wildcard_v7.png (gcode gallery/studio/gan/current/pp_gan_wildcard_v7.gcode)

**Inputs**
- HANDOFF r06.
- `encoding.md` rev 1: its §4.1 check numbers and §9 lies list. They stand in for the missing dossier.
- LEDGER.md (pass 2), and my own r05 critique for its mandates.

**Caveat.** r06 is a wildcard with a new order: a De Stijl square-spiral lane at 38 mm/unit, centred on (78, 141). `encoding.md` does not describe this order. So the channel rules come from the HANDOFF `rule:` line only.

**What I measured**
- I parsed the gcode per `; color=N` into 804 pen-down strokes:
  - gold 39, crimson 36, royalblue 15, black 714.
  - 7,043 commands.
  - Draw 15.19 m, travel 5.68 m.
- I rebuilt the run myself: simultaneous GDA, f′(s) = σ(−s), h 0.26, r0 0.74, a0 0.42622.
- I projected every iterate onto the lane polyline, then tested it against the drawn cells.

## Check numbers
| quantity | dossier (encoding §4.1 / HANDOFF) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| model / sign key | Dirac-GAN, simultaneous GDA. ψθ > 0 means D is ahead (Mescheder) | same | `DIRAC-GAN · SIMULTANEOUS STEPS · H 0.26` · `AHEAD: D IF PSI·THETA ABOVE 0, ELSE G` | OK |
| discrete \|λ\| at r→0 | 1.00841 | 1.0084146 | not printed. Title `THE FIXED POINT REPELS` | OK |
| z_0 | a0 24.42°, (113.04, 128.91) at 52 mm/unit | 24.4206°. At 38 mm/unit about (78, 141): **(103.60, 152.63)** | `STEP 0` set inside the square at y ≈ 155, beside the first blue cell (x 107.4, y 156.35). Step 0 projects to (110.37, 155.70) | OK |
| equilibrium / flow square | half-side r0 = 0.74 × 38 = 28.12 mm, centre (78, 141) | 28.12 | black square, 3 passes: x 49.88–106.12, y 112.88–169.12, so outer half-side 28.12 and centre (78.00, 141.00) exactly. `+` at (78, 141) | OK |
| side distance = axis-crossing radius (mm, 38 mm/unit) | "each side at the run's own axis-crossing radius" | r0 28.12, then 30.03 / 33.61 / 36.73 / 41.26 / 44.84 / 50.82 / 54.63 / 62.62 / 66.53 / 77.38 / 80.95 / 95.44 / 98.63 / 117.27 / 120.22 | inner ink edge = crossing radius **+1.25 mm** on all 13 drawn sides (residual < 0.01). Lane centreline = crossing radius + 4.25. The crossing radius itself lies on paper, 1.25 mm inside the lane | offset (mandate 3) |
| lap growth | 1.51 (52 mm/unit, §4.1) | E-side distances 28.12 → 41.26 → 62.62 → 95.44 give ratios 1.467 / 1.518 / 1.524 | E-lane inner edges at x 107.37 / 120.51 / 141.87 / 174.69 | OK |
| step projection | "each step lands where the ray from the + through its iterate meets the lane" | — | the best fit is the lane centreline at d + 4.25 (7 mismatches, against 9 at d + 1.25 and 232 at d). Sign colour matches in 184 of 188 steps inside y ≥ 35. The 4 near-misses fall in the 1.3 mm cell gaps. **3 steps land physically on gold corner squares** (see the lies list) | PARTIAL |
| first beat off | — | step 125, r **1.8806**. Ray meets the top-2 lane at (7.57, 211.78) | `STEP 125 R 1.88: FIRST BEAT OFF THE SHEET`. The top-2 lane is cut at x 13.14 | OK in numbers. "Sheet" is wrong: x 7.57 is on the paper, inside the 10 mm margin |
| sides off-sheet | — | W2 centre x −3.6 (steps 126–146), W3 x −43.5 (steps 256–419), E4 x 226 | not drawn | OK |
| **S3 lap-3 bottom (side 15)** | — | lane centre **y 16.5**. Steps 420–577, **42 of them inside x 10–200** | **not drawn**, because it would sit under the footer type (y 10–31) | **undeclared crop** |
| turn per step | 6.65° at step 0, ≤ 13.7° in frame | 6.65°, 12.52° at step 125, max 14.31° up to step 255 | — | OK. The §4.1 bound is slightly low |
| plot | — | — | 804 pen-downs · 7,043 commands · travel 5.68 m < draw 15.19 m | OK |

**Findings on the dossier / encoding**
- r06's order is not documented in `encoding.md`. §4.1 still quotes 52 mm/unit and centre (78, 113).
- There is no `dossier.md`.
- The HANDOFF says the lane width is 6.5 mm. The measured ink is 6.00 mm, which is 6.5 mm with a 0.5 mm tip. That is OK.

## Lies list
| item | status |
|---|---|
| no "no equilibrium" | clean. The `+` is labelled `NASH EQUILIBRIUM / THETA = PSI = 0`, and the legend says `NASH EQUILIBRIUM: IT EXISTS, IT REPELS` |
| no turn-taking vocabulary, no L-steps | clean in words (`SIMULTANEOUS STEPS`). Watch item: axis-aligned legs are the r02 staircase silhouette. Here each side is keyed as an axis crossing, not a player's move, and the colour is keyed to who is ahead, not who moves |
| no float, dash or width keyed as a move, loss or speed | clean. The lane width is a constant 6.0 mm. Gold is keyed literally, `PASSED OVER WITHOUT A STEP`. **But** that density is shaped by the square projection. Along-lane spacing is D·sec²φ·Δφ, so gold rises from **21 %** of lane length within 0–15° of an axis, to 22 % at 15–30°, to **33 %** at 30–45°. Nearly every lane corner square is gold |
| gold = no step lands (the HANDOFF rule) | **VIOLATED (small)**. Step 16 (G) lands at (40.1, 173.9) and step 80 (D) at (24.8, 82.1). Both are in gold corner cells. Step 169 (G) lands at (177.7, 57.0), inside the gold bottom-2 stroke. The crimson cell drawn for it, (174.7–180.7, 59.70–64.88), holds no step |
| no partial flow arc | clean under the declared order. The flow is a closed square, half-side r0, labelled `H TO 0: EVERY AXIS AT R 0.74, FOREVER`. That is true, because the flow conserves r. The circle's true shape is carried only in words, and z_0 itself (103.6, 152.6) lies inside the square, not on it |
| no ink inside the flow except the `+`, labels and flow | clean. Inside the square there is only the `+`, `NASH EQUILIBRIUM`, `THETA = PSI = 0` and `STEP 0` |
| no number the sheet does not show | clean-ish. `R 1.88` is the iterate's radius. The sheet shows only the lane cut at x 13.14 on a side placed at r 1.75 |
| window declared / no "the sheet is the whole run" | **VIOLATED** in two ways. First, 42 beats of side 15 (steps 420–577, lane y 13.5–19.5) fall on the drawable sheet and are hidden under the footer without a word. Second, "OFF THE SHEET" is actually off the 10 mm margin |

## Scores
- **truth 8**
  - Every printed number recomputes: step 125, r 1.8806, h 0.26, r0 0.74, the Mescheder sign key, and a flow square of exactly r0.
  - All 13 drawn sides sit at their axis-crossing radii, each with the same +1.25 mm offset.
  - The losses:
    - an undeclared crop of 42 on-sheet beats under the footer;
    - "off the sheet" means "off the margin";
    - 3 steps land in gold corner squares.
- **fidelity 7**
  - The sign rule holds per cell (184/188).
  - D's clotting is real: blue quadrants are solid except at corners. G's stride is real too.
  - But the gold channel is contaminated by projection. Corner gold is 33 % against 21 % near the axes, driven by sec²φ and not by the run.
  - Corner squares are ambiguous between two sides.
  - The lane sits 1.25–4.25 mm outside the radius the key names.
  - The order is undocumented in `encoding.md`.
- **legibility 8**
  - The outward nested growth reads at once. E-side distances run 28 → 41 → 63 → 95 mm.
  - `STEP 0` marks the start, so the r05 gap is closed.
  - The black flow square with the `+` is the one quiet centre.
  - Blue runs versus chopped crimson/gold make the saturation legible to a stranger.
  - The key explains the square-projection order in two lines.
  - Risk: gold can read as a third player, and the square as the orbit's true shape. The key covers both.

**VERDICT: FAIL** (fidelity 7 < 8)

## Mandates
1. **Gold must mean "no step" and nothing else.**
   - Measured: gold covers 21 % of the lane within 15° of an axis and **33 %** within 15° of a diagonal. That is the sec²φ stretch of radial projection onto a square: lane length per degree doubles at 45°. Almost every corner square is gold.
   - Measured: steps 16 (40.1, 173.9), 80 (24.8, 82.1) and 169 (177.7, 57.0) land inside gold corner squares.
   - Measured: the crimson cell at x 174.7–180.7, y 59.7–64.9 (bottom of the E3 lane) holds no step.
   - Expected: 0 steps in gold cells and 0 coloured cells without a step.
   - Expected: corner squares assigned to the side the ray actually meets.
   - Expected: cell size set per equal angle, so each cell spans a constant Δφ and the length varies along the side. Then gold share is flat with angle (±3 pts), and the corners stop manufacturing "passed over".
2. **Declare the window. 42 beats on the sheet are silently dropped.**
   - Measured: side 15 (lap-3 bottom, crossing radius 120.22 mm, lane centre y 16.5) carries steps 420–577. 42 of them project inside x 10–200 on the drawable sheet, under the footer (y 10–31), and are not drawn.
   - Measured: the caption `FIRST BEAT OFF THE SHEET` places step 125 at x 7.57. That point is on the paper, inside the margin.
   - Expected, one of the following:
     - (a) The key says it, e.g. `STEP 125 R 1.88: FIRST BEAT OFF THE PLATE · STEPS 420–577 PASS UNDER THIS KEY`.
     - (b) The footer is reflowed so the lap-3 bottom lane is drawn.
   - In both cases "sheet" becomes "plate" or "margin".
3. **The sides must sit where the key says, and the order must be written down (S6).**
   - Measured: on all 13 drawn sides the inner ink edge is at the axis-crossing radius **+1.25 mm**, and the lane centreline, which the steps are projected onto, is at **+4.25 mm**. Examples:
     - E0: 29.37 against r0 28.12.
     - N3: 99.88 against 98.63.
   - So the named crossing point is bare paper, 1.25 mm inside every lane.
   - Measured: `encoding.md` still specifies the weave order at 52 mm/unit and (78, 113).
   - Expected: centre the lane band on the crossing radius (d ± 3 mm), except E0, which may abut the r0 square. Otherwise the key must state the offset.
   - Expected: an encoding revision recording this order's check numbers at 38 mm/unit and (78, 141):
     - crossing radii 28.12 / 30.03 / 33.61 / 36.73 / 41.26 / 44.84 / 50.82 / 54.63 / 62.62 / 66.53 / 77.38 / 80.95 / 95.44 / 98.63 / 117.27 / 120.22 mm;
     - first off-plate beat: step 125, r 1.8806.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S2 perceived float = Σ moves | FIXED (claim retracted, holding) | No length is keyed to a move. The lane width is a constant 6.0 mm, and cell pitch is ≈ 6.4–6.5 mm per side, never keyed |
| S6 no dossier / encoding | PARTIAL, worse in scope | Still no `dossier.md`. The r06 order (square lane, 38 mm/unit, (78, 141), projection rule, gold rule) appears in no encoding. §4.1 numbers describe a different frame (mandate 3) |
| S8 every in-frame iterate covered / window declared | **REGRESSED** | Steps 0–125 and 147–255 are all on drawn lanes, except 3 on the margin side at x < 10. But 42 on-sheet beats (steps 420–577) sit under the footer undeclared. r05 had the window declared as the cut edge (mandate 2) |
| S9 key on-top in words | FIXED, holding | `A STEP, D AHEAD: D SPOTS THE FAKE` / `A STEP, G AHEAD: G FOOLS D` / `AHEAD: D IF PSI·THETA ABOVE 0, ELSE G`. Correct under f′ = σ(−ψθ) |
| r05-M1 run start on the cloth | FIXED (superseded) | Steps 0–3 project to (110.37, 155.7 → 172) inside the first blue E0 cell (y 156.35–172.17) |
| r05-M2 float weight 100 % / no holes | PARTIAL (superseded) | Its analogue: cell colour = sign holds in 184/188 steps, with 3 corner defects (mandate 1) |
| r05-M3 show where step 0 is | FIXED | `STEP 0` sits inside the square at y ≈ 155, touching the start of the E0 lane beside z_0's projection (110.4, 155.7) |

**Truths that held in r05 and changed now**
- The h→0 flow is no longer drawn as its true circle (S3). It is a closed r0 square, labelled truthfully, and consistent with the declared order. Accepted, noted.
- The lap-ratio statement (`EACH LAP ABOUT 1.5 × WIDER`) is gone. That is not a regression, because it is not claimed.
- No sign-convention or equilibrium truth regressed.
