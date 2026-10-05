# Art critique — millennium-navier-stokes r01 · canon: OP ART line field (Riley) on a BAUHAUS poster sheet · 2026-09-29
render: gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_faithful_v6.png (gcode beside it; measured from the gcode, not only the preview)

## Scores

| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 7 | The hero dominates by area (3.4× rung 1 after the frame crop). Rung 1 is the darkest blue object on the sheet: 256 strokes at 1.2 mm pitch in a quarter of the hero's area. Its tight rim comb reads like a drawn circle edge. The black ring disc is drawn at 0.1 mm against 0.3 mm blue, so on paper the "calm counterweight" will look pale grey. The preview hides this because it draws every pen at the same weight. |
| 2 | grid & alignment | 6 | There are eight separate text blocks. The left axis x=15 holds (title, statement, side-view caption, notes), and so does the right axis x=282 (ring caption, corner, stamp). The two lower-middle captions sit on two different right edges (x≈218 ladder, x≈225 limit) about 60 mm apart, and they float. "4/3 T0" is set in the same glyph weight, so it reads as "BY 4/3 TO". |
| 3 | tension & asymmetry | 6 | The hero is cropped left, the ladder curls down the right, and the disc sits off-axis, so the asymmetry is real. But the sheet is seven round objects (hero, target, circular-windowed side view, rungs 1–4, red ring), each set in its own gap of roughly equal size. The eye hops from exhibit to exhibit. The C₀→L orbit, meant to be the one driving diagonal, reads as a scatter and not as a sweep. |
| 4 | negative space | 7 | The voids that carry data are right: bare spiral eyes, the open ring-disc eye, an empty red ring. The lower-left zone is about 65 % bare. The gaps between exhibits are leftover space and not shaped space. |
| 5 | craft for pen | 8 | Blue–blue gaps are all at or above 0.8 mm on the gcode (0 violations across 643 blue strokes). Red to blue is 0.85 mm. The 22 rings are single closed strokes, with the tightest gap 1.55 mm at r≈25 mm. There are 2 swaps, and no floods or knots in the eyes. Two problems: travel is 17.3 m against 23.8 m of draw, and red is 2.1 % of the ink against a budget under 1 % because the stamp runs long. |
| 6 | concept legibility | 7 | Rings against spiral reads at 3 m, and the ladder of halvings reads. The terminus reads less well. The red ring (R 11.8) is larger than rung 3 (R 11) and twice rung 4, and rung 4 sits on its shoulder 0.85 mm away, so the limit looks like a satellite and not a vanishing point. The side view is the textbook stagnation-flow diagram, which is the most schematic element on the sheet. |
| 7 | depth & dimensionality | 6 | Flatness is declared and lineage-honest. The declared depth device, recession along a similarity orbit, does not read as recession, because the rungs spread over a 200 mm arc with large gaps. The Monge elevation adds a second projection, but it is presented as a separate exhibit. |

avg **6.71** · min **6** · **VERDICT: FAIL**

## Reads at a glance
A big cropped blue whirlpool spilling down the right side into smaller and smaller copies ending at a red circle, a black target top-right, and a black X-saddle bottom-left, each with its own caption: a well-made specimen board, not yet one image.

## Acceptance checks (encoding §11)
1. **Rings vs spiral at 3 m — PASS.** 22 closed concentric strokes with no ends. The hero is an inward spiral. Bare paper from the disc to the nearest blue is 31 mm (rung 1) and 33 mm (hero). The two never share a texture. (Caveat: the 0.1 mm nib, see hierarchy.)
2. **The ladder is exact — PASS.** Five rungs with R = 88 / 44 / 22 / 11 / 5.3. Rung 1 scaled ×2 about its centre lands on hero strokes with a median distance of 0.18 mm, and 100 % of samples are within 0.3 mm. The centres fit a ½-scale orbit with Δφ≈−20°, and the predicted limit (249.6, 44.2) matches the red ring centre (250.0, 44.0). The Δφ value is not stated in HANDOFF.
3. **The pen floor is honest — PASS.** Every rung has a bare eye. There are 0 blue points inside the red ring. Red appears only in the ring and the stamp. The minimum blue–blue gap is ≥ 0.8 mm (0 violating pairs).
4. **Hierarchy and silence — PASS (marginal).** The hero is 3.4× rung 1, just above the 3× bar. The lower-left zone is at least 40 % bare with the elevation in it. No caption sits on lines, and nothing presses the frame except the intended crop.
5. **Status wording — PASS.** "CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH (UNVERIFIED) / WITHOUT A PUSH: OPEN". It has the date, claimed/unverified, the forced case and the open unforced case. "LARGE SCALES TO SMALLER ONES" appears only on the ladder.

AUTHORING §6 (reference in play):
1. Forms recognisable without colour: **yes**.
2. Lines follow the form rather than a random mesh: **yes**, every blue line is a streamline.
3. Fine lines that are really two sides of one thick stroke: **no**.
4. Blackest regions intended: **partly**. The rung 1 density is the intended ω×4, but it out-weighs the hero.
5. Labels readable at the real pen: **mostly**. "4/3 T0" reads as "TO".
6. Knots from a thicker pen: **no**.
7. Long travels or pointless tiny marks: **travel is heavy** (17.3 m). The stubs on rungs 3–4 earn their place (the fray).

As an interpretation, the reference's one continuous gesture (wave feeding vortex, zoom inset) has become four exhibits. The physics is truer, but the single sweep is lost.

## Biggest weakness
The sheet is a specimen board. It holds seven round exhibits spaced at roughly equal gaps, and each carries its own caption block. The side view's circular window adds a seventh disc to the quiet corner. Neither the Riley surface (one field that moves) nor the Bauhaus diagonal (one driving line) takes over. On paper, the 0.1 mm rings also weaken the one comparison the plate exists for: rings against spiral with the same Γ.

## Mandates
1. **Draw the 22 rings with the 0.3 mm nib used for the blue** (black 0.3, which can be the type pen), and render the preview at physical widths (`pen_widths=`) so the critic sees what the paper will show. Test: the pen plan lists the rings at 0.3 mm, and in the physical-width preview the black disc's line weight matches the hero's at 3 m.
2. **Give the side view a rectangular window instead of the circular clip.** The window's left edge sits on x = 15, it is ≤ 90 × 70 mm, it keeps the one dotted projection line up to the hero, and its caption goes directly under it on x = 15. Test: the sheet has exactly one non-round mass (the side view), and it shares the left axis with the title and the notes.
3. **Consolidate the type onto the three axes.** The ladder caption and the limit caption share one exact right edge (they are now at x≈218 and x≈225), or they merge into one block under rung 2. Keep the number of caption blocks at 7 or fewer, including title and stamp. Set the time symbol so it cannot read as "TO" (a smaller, lowered 0, or "T₀" in a distinct glyph). Test: no caption right edge falls outside {x=282, the one shared ladder edge}, and "4/3 T₀" is unambiguous at 30 cm.

Secondary (not a mandate): rung 4's stubs are 0.85 mm from the red ring. That meets spec, but the two touch at 3 m, and the ring (R 11.8) outsizes rung 3. Look at this after the three mandates, because the ring radius follows from the §4 enclosure rule (|C₅−L|+R₅ ≈ 9.0+2.75), not from the encoding's "≈7 mm" estimate. The rule and the estimate disagree, and the lead should reconcile them. Also shorten the stamp so red stays under 1 % of the ink.

## Follow-up on open mandates
id | status | evidence
— | — | This is r01. There is no LEDGER.md, FEEDBACK.md or DESCRIPTION.md for this slug, so there are no open A*/J* mandates and no § Keep items.

## Regressions vs compare-to
None. The compare-to is "none (r01)", so this is the baseline round.
