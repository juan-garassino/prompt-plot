# Art critique — resonance-ffn r02 · canon: Op Art (lineage Riley, *Current* 1964; HANDOFF names no STYLES.md canon) · 2026-09-29
render: gallery/studio/resonance_ffn/current/pp_resonance_ffn_the-squash_v15.png (gcode alongside; A4 portrait, cream, 5 pens)

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 5 | Two violet bundles of nearly equal mass: upper ±1 band is 47 mm, lower throat is 44 mm, and both run x 87→200. Neither dominates at 3 m. The Q/K discs are a third mass of about the same weight. |
| 2 | grid & alignment | 7 | The columns are real and shared by both bundles: seam at x≈87, throat entry at x≈101, flare at x≈143, right edge at x=200, disc centres on x=24.3. The title sits on the left margin line. The lower small Q/K targets float, and nothing locks them to the bundle's axis. |
| 3 | tension & asymmetry | 5 | Each bundle is mirror-symmetric about its own axis, and the two are stacked as twins. The left/right weighting (discs, then flare) is the only asymmetry. Riley's *Current* gets its tension from phase drift across a surface. Here nothing drifts: every line is a smooth copy of its neighbour. |
| 4 | negative space | 6 | The upper-right quiet above the flare (x 100–200, y 235–287) is generous and works. The lower-left quadrant (x 10–85, y 20–150) is leftover rather than shaped: two 7 mm targets and a title float in it. The 20 mm band between the bundles is just a gap. |
| 5 | craft for pen | 5 | Violet lines are broken and restarted mid-run: 6 endpoints at x≈143 and about 14 at x≈170–176, which show as visible gaps and jogs on the lower flare. Each outer Q/K ring (r>13 mm) is split into two strokes at 3 o'clock, which puts a column of double pen-drops at x 38–49, y 181.7 (and the mirror on red). The Q/K lens is shallow-angle crossings of two colours at 0.3–0.6 mm. Violet travel jumps between the bundles 7× by >100 mm (22 jumps >40 mm), and green does 24 jumps >40 mm; travel is 61% of motion. Spacing inside each family is clean: no same-colour violet or green pair is under 0.6 mm, and the rings sit at an even 1.2 mm pitch. The dots are good: closed 0.11 mm circles at 1.00 mm pitch. |
| 6 | concept legibility | 6 | The squash reads: a line family pinched flat between two dotted rails, then released. It is not a schematic, and the order (laminar flow) is exact. It does not read as tanh *saturation*, though. Lines outside ±1 stop dead at x≈101 in a vertical cut edge instead of piling up along the rails. The lower "gradient" twin carries its meaning only as a shorter green fan, so a stranger sees the same shape twice. |
| 7 | depth & dimensionality | 5 | The flare gives the bundle a faint tube/horn volume and the nested discs read as cones. Otherwise the plate is flat, and HANDOFF does not declare that. |

avg **5.57** · min **5** · **VERDICT: FAIL**

## Reads at a glance
Two violet trumpets stacked on the right, fed through a green fan by a red and a blue target on the left edge. At 3 m it reads as "flow squeezed through a channel". It does not read as "saturation", and the second trumpet looks like a duplicate.

## Acceptance checks
No `encoding.md` or `BRIEF.md` exists for this slug, so there are no §11 checks to run. The AUTHORING §6 questions are run against the reference. The plate interprets only the reference's FFN "nonlinearity" detail, which is a legitimate abstraction.
1. Main forms recognisable without colour fills? **PASS.** The pinched bundle holds as pure line.
2. Lines follow the form rather than forming a random mesh? **PASS.** It is one coherent family per bundle.
3. Fine lines that are really two sides of one thick stroke? **PASS.** Two related faults: the split outer rings double back on themselves at 3 o'clock, and the violet restarts at x≈143 jog next to their predecessors.
4. Blackest regions intended, or accidental congestion? **FAIL.** The Q/K lens (x 15–35, y 200–207) is the densest ink on the sheet, and it is a smear of shallow crossings with half-cut red arcs, not a readable fringe.
5. Labels readable at real pen width? **PASS.** `+1`/`−1` and the title are clear. The `+1` is about 2 mm tall, which is small but legible.
6. Thicker pen knots at corners or seams? **FAIL.** There are double pen-drop blobs at every split-ring seam (x 38–49, y 181.7 and y≈227), plus restart blobs at x≈143 and x≈170–176.
7. Long empty travels or excessive tiny marks? **FAIL.** Violet crosses between bundles 7× by >100 mm and total travel is 61%. The ±1 rails cost about 200 pen cycles, which is acceptable because they are the only dots.

## Biggest weakness
The plate states its one idea twice at equal weight, and in neither statement does saturation happen. Lines beyond ±1 are simply deleted at x≈101 rather than crowding onto the rails. The lower twin changes only the green fan length, so the derivative is not visible in the violet bundle itself.

## Mandates
1. **One dominant bundle.** Make the forward bundle at least 3× the gradient bundle. The upper ±1 band should be ≥70 mm tall and the lower throat ≤25 mm tall, both keeping the shared x-columns (87 / 101 / 143 / 200). Test: measure the two throat heights on the render; ratio ≥ 2.8.
2. **Make saturation visible at the rails.** No violet line may end between x=88 and x=142. Lines entering outside ±1 must bend onto the rail and run along it through the throat, so spacing collapses toward the rails. Test: at x=120, the two lines nearest each dotted rail are ≤1.0 mm apart, while lines at the axis are ≥2.4 mm apart. For the gradient bundle, the tanh′ must show in the violet itself (an axis-hugging bulge or notch), not only in the green fan length.
3. **Continuous strokes, ordered by bundle.**
   - Every violet line is one stroke from x=87 to x=200, with zero endpoints at x≈143 or x≈170–176.
   - Every Q/K ring is a single closed stroke or one arc, with no 3 o'clock split.
   - The violet and green layers each finish one bundle before starting the other, so that no consecutive-stroke travel exceeds 60 mm.
   - Test: count endpoints in the gcode and the longest intra-layer jump.

## Follow-up on open mandates
There is no LEDGER.md for this slug. The open items are Juan's FEEDBACK.md note and DESCRIPTION.md.

| id | status | evidence |
|---|---|---|
| J (FEEDBACK 2026-09-28T23:39, REWORK v5): "KEEP THE ORIGINAL — v13/r01 is the design, keep EVERY element … the ONLY change wanted is dot continuity … applies to res_ffn" | **REGRESSED** | r02 deletes every wave packet, the black crest hero, the halos and ellipses, the scattered dots, the leaders, ∂L/∂A, V, Z and the six-pen set. The note is timestamped 23:39 and piece.py 23:44, so this round was made *after* the binding note. FEEDBACK now points its Source at r03, and this round is off-mandate by Juan's own instruction. |
| J-dots: "one round dot of fixed size, pitch ≈0.9–1.1 mm, end-anchored" | **FIXED** (where dots exist) | ±1 rails use closed 0.11 mm circles at 1.00 mm pitch (min 0.99, max 1.00), about 100 dots per rail. There are no micro-dashes. |
| DESCRIPTION Next #1 "the squash": one wide bundle, 2–3 pens, one dominant form, derivative notch below | **PARTIAL** | The bundle and flow order are built, and the schematic is gone. It uses 5 pens rather than 2–3, has two co-equal forms, and has no derivative notch in the lower violet bundle. |
| DESCRIPTION weak [space] lower third jammed | FIXED (by deletion) | The lower third is now nearly empty. |
| DESCRIPTION weak [concept] schematic | FIXED | No boxes, brackets, fractions or arrowheads remain. |
| DESCRIPTION weak [craft] six pens / five swaps | PARTIAL | Now 5 pens / 4 swaps. |

## Regressions vs compare-to (v9)
- **The black interference hero is lost.** v9's twin nested-ring crest figure with its fringe lens was the strongest ink on the sheet. It has been replaced by two coloured discs whose overlap is a muddled lens (§6 Q4 FAIL).
- **Keep item "forward dome vs backward twin peaks" is broken.** DESCRIPTION called this the best idea of the sibling. In r02 the lower violet bundle has the same squash shape as the upper, so the derivative is no longer a shape change.
- **Keep item "∂L/∂A mini-interference at 0.39 scale" is broken.** It is gone. The small lower targets are not an interference figure: they do not overlap.
- **Keep item "v9's lowercase stage type" is broken.** All stage type has been removed.
- **Keep item "top half inherits the benchmark's funnel and hero" is broken.** It is gone.
- **Keep item "one axis Z → FFN → Y across the lower sheet" holds only partially.** Horizontals persist, but as two axes rather than one.
- **Every wave packet (Q, K, V, Z, ∂L rows) has been removed.** This is exactly what Juan's binding note forbids.
- **Gains, for fairness:** travel dropped from 12.2 m to 7.9 m, the dots are correct, and the plate is no longer a schematic.
