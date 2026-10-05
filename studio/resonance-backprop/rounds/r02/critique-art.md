# Art critique — resonance-backprop r02 · canon: none assigned (no encoding.md / BRIEF.md; judged against the HANDOFF lineage, Sol LeWitt *Arcs, Circles & Grids*, plus DESIGN_RUBRIC) · 2026-09-29
render: gallery/studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.png (gcode beside it; a4 portrait, cream, 5 pens)

## Scores
| # | dimension | score | evidence |
|---|---|---|---|
| 1 | hierarchy | 5 | Four bullseye families of similar weight. The two big ones (blue at (125,210), red at (125,87)) are the same size, so neither leads. The green fold is a single thin horizon, and the V beads (4 dots, 14 mm run at x 32–46) don't register at 3 m. Nothing reads first. |
| 2 | grid & alignment | 7 | Sources sit on two columns (x≈52, x≈125) and are an exact mirror pair across the fold (52,157.5↔52,139.5; 125,210↔125,87). Rail at x=15 T-joins the fold, and arcs clip cleanly at x=21/200 and y=10/287. The beads are off the column: they stop 6 mm short of x=52. |
| 3 | tension & asymmetry | 6 | The fold sits at y=148.5, exactly half of the 297 mm sheet. The sources form a rotated Z, which helps, but the sheet is split into equal halves, and the mass is right-heavy with only the rail on the left to balance it. |
| 4 | negative space | 4 | 3 mm ring texture runs edge to edge. The only voids are two leftover wedges where the arcs fail to reach (bottom-left x20–85/y10–55, top-left x20–85/y240–287). They are residue, not shaped space, and there is no quiet zone that makes a dense zone louder. |
| 5 | craft for pen | 7 | Ring pitch is exactly 3.00 mm. Weight falls off by pass count on purpose (3 turns, then 2, then 1, outward). 334 pen cycles, 2.6 m travel against 23 m draw, and 5 layers in order 0→4 with no re-entry. Flags: the gold beads are 0.30 mm-pitch spiral discs up to 3.1 mm across, a solid knot on paper, and green (layer 3) then overdraws them. Feed is F2600 with G4 P0.2 dwells, which is against the Leo slow-feed/long-dwell rule (F600, P1.0). |
| 6 | concept legibility | 6 | This is an abstract order (radial interference), not a schematic and not an illustration. The colour swap across the fold (∂L/∂Q carried by K's wave, ∂L/∂K by Q's) is a real twist. But it is a hue-only fact, so in monochrome it reads as a plain mirror. V/attention is invisible, and Z is a flat line carrying no data. |
| 7 | depth & dimensionality | 5 | Pass-count falloff gives near/far, and the dashing at crossings gives over/under. Otherwise the plate is flat, and the HANDOFF does not declare the flatness. |

**avg 5.71 · min 4 · VERDICT: FAIL**

## Reads at a glance
From 3 m a stranger sees red and blue target ripples interlocking over the whole sheet, cut by a green horizon, with the colours trading sides below the line. That reads as op-art wallpaper. It does not say "gradients flow back through attention".

## Acceptance checks
No encoding.md §11 exists for this slug, so there are no §11 checks. With the reference in play, here are AUTHORING §6's seven questions, judging r02 as an interpretation of the reference:
1. Main forms recognisable without colour fills? **FAIL.** The forms (four targets and a horizon) survive, but the plate's one idea, the Q/K swap across the fold, lives only in hue.
2. Shadow lines follow the surface? **PASS (n/a).** There is no shading. The arcs are the surface.
3. Fine lines that are two sides of one thick stroke? **PASS.** Each ring is a single centreline, weight comes from 1–3 turns.
4. Blackest regions intended? **PARTIAL.** The 3-turn inner bands are intended. The gold bead discs (0.30 mm spiral pitch) are accidental knots.
5. Labels readable at real pen width? **PASS.** "forward pass" / "backward pass" are about 4 mm, set in rail gaps, clear of geometry.
6. Thicker pen makes black knots? **FAIL.** The beads, and the green line drawn through them.
7. Long empty travels or pointless tiny marks? **PASS.** Travel is 2.6 m, max hop 126 mm (on the rail layer), and the 41 tiny marks are glyphs.

Interpretation verdict: the reference's order (Q/K packets → crest interference → softmax peaks → Z = AV → the mirrored backward band) has been reduced to two of its seven stages. V, A, Z and ∂L/∂A/∂L/∂V are absent or token.

Lineage: the plate takes LeWitt's rule (arc families from fixed points, superimposed by one stated instruction), and the crossing arcs make an honest curvilinear grid. Hung beside *Arcs, Circles & Grids* it would lose on restraint: loud equal-value hues and no ground grid for the arcs to argue with.

## Biggest weakness
The sheet is an evenly weighted, edge-to-edge carpet of 3 mm rings with no dominant form and no shaped quiet. The mechanism survives only as a colour swap and four 3 mm beads, so the plate's idea is carried by nothing an eye lands on.

## Mandates
1. **Shape a quiet zone and pick a dominant.** Let the upper-right blue K family run to the frame as the single largest mass. Stop the lower-right red family at radius ≤ 45 mm, so the rectangle x 140–200 / y 10–50 is bare paper. Test: no ink in that rectangle, and one family is visibly ≥ 2× the area of any other.
2. **Make the backward half readable in monochrome.** Draw every ring below the fold dashed, with dash duty falling with radius (solid near the source, then ≤ 30 % duty at the frame). Keep every ring above the fold solid. Test: in a greyscale print the upper half is solid rings, the lower half is broken rings, and the swap still reads.
3. **Make V a real row on the fold, and fix its craft.** Spread the goldenrod beads along the full fold, x 21–200, with ≥ 8 beads whose diameter is the attention weight (largest ≥ 8 mm). Build each bead as concentric rings at ≥ 0.8 mm pitch, not a 0.30 mm solid spiral. Break the green fold at each bead so no green lies inside gold. Test: bead row visible at 3 m, ring pitch ≥ 0.8 mm, zero green inside any bead.

## Follow-up on open mandates
There is no LEDGER.md, so no A*/J* ids are recorded. Below are Juan's binding FEEDBACK note and DESCRIPTION.md's "If only iterating" items.

| id | status | evidence |
|---|---|---|
| J (FEEDBACK 2026-09-28T23:39, "KEEP THE ORIGINAL — keep every element, only fix dot continuity; don't remove to save plot time") | **REGRESSED** | r02 removes every packet row, the halos, the scattered dots, the leaders, the comb and the title. It is the opposite of the note. Timing: the note postdates this render (22:49), but it binds the next round. |
| iter-1 amplitude cap ≤ 0.45 × row pitch | NOT FIXED (moot) | The packet rows were deleted rather than capped. |
| iter-2 comb fringes ≥ 1.0 mm | NOT FIXED (moot) | The comb was deleted rather than thinned. |
| iter-3 move composition down, use the dead foot | PARTIAL | The foot is now inked (arcs to y=10), but by filling the whole sheet with rings, not by the requested shift. |

**DESCRIPTION § Keep:**
- v8 tight dashed oval: GONE.
- v5 wide dotted halo: GONE.
- The fold with ∂L/∂Z under Z = AV: PARTIAL. The fold survives as a mirrored echo, but Z = AV and ∂L/∂Z are gone.
- Comb lozenge: GONE.
- Rail with two arrows: PARTIAL. The words stay, the arrowheads and direction are gone.
- Corner crosses and centred title: GONE.

## Regressions vs compare-to (gallery/studio/res_backprop/current/pp_res_backprop_v8.png)
- **Every data stage is gone.** The Q/K/V packets, softmax A peaks, the Z = AV packet, ∂L/∂Z, ∂L/∂A, ∂L/∂V, all formulas and the title/subtitle. v8 was a (too literal) seven-stage read; r02 is a two-stage read.
- **V dropped** from a 4-row packet block to four 3 mm dots. The 5-pen plate is now effectively two pens.
- **The rail lost its arrowheads**, so forward-down and backward-up no longer read.
- **The engraving-plate frame is gone** (corner crosses and title).
- **Genuine gains** worth carrying into the r01-based rework: no braided packet knots, no flooded comb, no dotted-arrow thicket, 334 pen cycles vs 4 054, 2.6 m travel vs 11.9 m, and exact 3.00 mm arc pitch with pass-count weight falloff.
- **Binding direction:** Juan's note supersedes this round's approach. The next round should restart from r01/v13 with only dot continuity changed. Mandates 1–3 above apply only if "the-fold" continues as a separate alternative plate.
