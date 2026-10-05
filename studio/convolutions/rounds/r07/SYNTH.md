# Synth — convolutions after r07 · 2026-09-29
route: vote
next round: none by default. If Juan votes REWORK, the next round is r08 with parent r07 (the best so far: the only science PASS, the highest art min and avg). It needs an encoding amendment v1.1 first, because A25 changes a v1 channel.

## Verdicts
| round | art avg/min | sci t/f/l | verdict |
|---|---|---|---|
| r07 iterate (one-X) | 7.29/7 | 9/9/8 | art FAIL (avg < 8) · sci **PASS** |

r07 improves on its parent r05 (6.71/6 · 9/7/7, double FAIL) in every column, with no regression in composition, grid or science marks. Art noted one soft loss: the nib-corrected dots make the Ben-Day mass lighter at 3 m. The art critic says keep it, because truth wins. It closed A18, A21, A22, A23, A24, S5, S10 and S11.

## Routing trace
- **Rule 1** does not fire. Only science passes; art is 7.29 avg against the ≥ 8 bar.
- **Rule 2** does not fire.
  - No mandate given to r07 came back NOT FIXED. All 8 carried mandates are FIXED.
  - A16 is PARTIAL for the second time, but the r06 SYNTH explicitly deferred it out of r07's top 5, and its residue has changed character. The lower-left is now shaped. What remains are lone crimson rim rings, which science confirms are TRUE responses outside X. That residue needs a key clause (S12a), not a new encoding.
  - A19 is argued and engine-blocked.
- **Rule 3** does not fire: there is no translator UNWORKABLE.
- **Rule 4** does not fire: the best so far moved from r05/r06 to r07.
- **Rule 5** does not fire: r07 is better than r05.
- **Rule 6 FIRES.** r07 is designer round 5 of 5 on the wavefront-lattice encoding (r02+r03, r04, r05+r06, r07). The curator's relaunch budget ("2 more rounds") is spent by the r05/r06 pair plus r07. So the route is **vote**, with r07 and an honest note. This is not a silent pass: art is FAIL.
- MEASUREMENTS: this is a computed plate, not a trace. Both critics rebuilt X, K and Y independently from the gcode, so there are no invented coordinates.

## Fabrication gate (run: this plate goes to Juan)
`.venv/bin/python -m promptplot preview gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.gcode --stats --score` and `plot layer … --list`:

| check | result | ok |
|---|---|---|
| bounds (a4 landscape, drawable 10–287 × 10–200) | pen-down ink bbox x 23.78–284.0, y 20.35–197.0. The top and right edges are the deliberate crop (the lattice box). The command bbox reaches 0,0 only as pen-up travel from home | clean |
| pens | 3 (crimson → dodgerblue → black), 2 swaps. The curator set no pen cap. One clean layer per meaningful pen: 0 = y > 0, 1 = y < 0, 2 = X + furniture + type | clean |
| per-layer strokes | crimson 49 (1,897 cmds) · blue 51 (2,648) · black 795 (24,589). Every dot and ring is one pen-down | sane |
| draw / travel | draw 12.65 m, travel 5.47 m (ratio 2.31). The longest travel, 322.7 mm, is the home → (284,153) keyline start | sane (A19 engine-blocked) |
| time (NOTES, Leo F600 / F2000 / 1 s dwells) | crimson 3.0 min · blue 3.5 min · black 47.2 min · total ≈ 54 min (the scorer's own estimate is 494 s at default feeds) | sane |
| floods at detail | Art checked detail crops at 16–30 px/mm with a 0.30 nib: field min gap ≥ 0.86, collars ≥ 0.62, dot-to-keyline ≥ 0.93, ring-to-keyline ≥ 0.85, no solid floods. Known sub-floor contacts: 8 stripe tips at 0.55 mm from the staircase, hatch-to-dot at 0.63 mm, and the title's chamfer knots of about 0.8 mm (A26, A27). These are near-misses, not floods | clean with the noted near-misses |
| determinism | seeds 3 / 7 / 11 give byte-identical gcode bodies | clean |
| scorer | grade A (composition 0.937, efficiency 0.797) | — |
| package drift | `git status promptplot scripts` is clean. Nothing under `promptplot/` changed in this piece's rounds, so no `studio_regression.py` / `make check` run was needed | clean |

**Gate: CLEAN.** It is plottable today in the stated order: crimson (3 min) → dodgerblue (3.5 min) → black (47 min).

## The instruction (only if Juan votes REWORK, r08 from r07)
Make the outline the loudest line on the sheet and clean up the last contacts, so r07 becomes a Lichtenstein rather than a precise dot diagram. First the translator amends `encoding.md` to v1.1:
- The X keyline goes to 3 fused passes (≈ 0.90 mm) and the card keyline to 5 (≈ 1.30 mm). This gives the width ladder card > keyline > doubled ring > hairline.
- Every dot and ring is re-clipped ≥ 0.8 mm off the widened ink.
- Then change nothing else in the lattice, kernel, stride, read set, crop, pens or key order.

## Mandates to close (REWORK only)
1. **A25**: the Pop keyline weight ladder (encoding v1.1).
2. **A26**: near-misses.
   - 8 staircase stripe tips: butt the staircase at 0 or clear it by ≥ 0.80 mm, one rule for all 8.
   - Trim the hatch so the dots at y 99.8 clear it by ≥ 0.80 mm.
   - Drop the 4.5 mm stub at (69–74, 169–171).
3. **A27**: each title glyph's connected strokes as one 3-pass band path, with no double-inked corners.
4. **S12** (optional; closes A16's residue):
   - the crimson key row gains "the window reaches X's edge";
   - add "3 outputs under the card";
   - "mean depth in cell".
   - The block must not grow.

A19 (travel, swatches mid-layer) stays engine-blocked. Do not hack around it in the piece.

## Preserve (the regression bar)
- **Science (sci r07 PASS, 9/9/8):**
  - 37×25 lattice at 7.2 mm; 5×5 LoG σ 1; valid convolution, stride 2, 17×11.
  - Read set i + j ≤ 10 (66 windows).
  - Ring counts 37/37 and signs 37/37, at pitch 1.02.
  - Y from ink gives 66/66.
  - Dot ink area ∝ x within −0.6 … +3.8 %.
  - Collar ink ∝ |w| within 0.36 %.
  - Stripes are the level sets Δd = 2.1 mm (residual median 0.003 mm).
  - The staircase is exact to 0.01 mm.
- **One X** (A21): a single open polyline per pass, ending only on the crop at (284, 153) and (166, 197). It crosses both risers unbroken.
- **Hierarchy** (A22): the 5 doubled outer rings, stripes ≤ 6 m, and the blue chain second to the card at 25 %.
- **Grid** (A23): the riser ends at (197.6, 24.2). Title and key baselines sit on lattice rows, with the shared axis at x 204.8 and a 7.2 mm riser-to-title gap.
- **Tension:** the staircase ↘ and the wing ↗ cross at the lifted card. Both bleed off the frame.
- **The lifted card** (A17): the 3.2 mm 45° shadow band, and the card as the heaviest line.
- **Plot contract:** 3 layers streamed crimson → dodgerblue → black, and seed-independent gcode.

## Do not
- Do not reopen the order or the lattice. The cap is hit, and the only open work is weight and contacts.
- Do not thicken the keyline without re-clipping. A wider keyline that touches dots or rings breaks the r01 contour-discipline bar that r07 just restored.
- Do not delete the crimson rim rings to "clean" the quiet zones. They are true K∗X responses. Key them (S12a).
- Do not raise the card by shrinking anything else. It must stay the heaviest line by its own passes.
- Do not import anything from r06 (the *Bacterio* flavour stays parked with W1–W3).

## For Juan's vote
**Plate:** `gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png` + `.gcode`. Source: `studio/convolutions/rounds/r07/piece.py::convolutions_onex`, seed 7, a4 landscape.

**Honest note:**
- Science PASSES (9/9/8). Every mark recomputes from the sheet.
- Art FAILS narrowly (7.29 avg, min 7; the best of 7 rounds). The single named gap is that the Pop keyline does not dominate: at 0.60 mm it weighs the same as the rings.
- Three cheap fixes would likely clear 8: A25 keyline weight, A26 contacts, A27 title knots. Together they are one REWORK round.

**Alternative flavours on disk:** r06 *Bacterio* (wildcard, 6.86/6), r03 sliding-window, r02 real-kernel. r01 stays the craft benchmark.
