# Synth — neural-networks-cnn after r04 + r05 (parallel) · 2026-09-29
route: vote
next round: none before the vote. If Juan returns REWORK, the next round is **r06 · parent r04** (best so far, and the only round on this slug with a passing critic).
Round budget: all 5 designer rounds are used (r01–r05; there is no `encoding.md`, so they share one budget). The curator's batch-1 relaunch granted 2 rounds, r04 and r05. Rule 6 fires, and this is **not a silent pass**: art FAILS on the plate that goes to the vote.

## Ranking (parallel theses)
**r04 > r03 > r05 > r02 > r01.**
- **r04 wins:** art 6.43/6 · sci 9/8/8, science PASS. It is the first passing critic on this slug.
- **r05** (art 6.71/6 · sci 8/6/7) has the better art avg, but loses on verdict and on science min, because its fidelity fails (rings deleted and inflated).
- **No merge:** the dial and the stack share no geometry.
- **r05 stays on disk as the `reach-dial` flavour**, a different question ("it could see the whole picture, it looks at a quarter of it"), with the best tension on the slug (8). Its mandates are parked in the ledger as RD1–RD5.

## The instruction
**For Juan's vote:** judge **r04** (`gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png`) as the one-valley stack. Its science is exact end to end:
- 13/13 strong CAM crests are visible.
- The ERF loops are within 0.33 mm.
- The rings are exact level sets.
- Rows, pitch and fragmentation are strictly monotone from 224² to 7².

Its art fails for one reason: **the summit is the quietest mark on the sheet** (an 18 × 7 mm crimson cap on a 10.5 mm hump). The designer's sweep shows this is a genuine conflict inside the encoding, not a tuning miss. With rows-only hidden-line at a 4.24 mm top-plane pitch, any height above ≈ 1.05–1.08 mm/CAM unit hides the runner-up (3,3), which sits one row behind the peak. So "a tall mountain" (A14) and "every strong cell visible" (S8) cannot both hold on this plane.

Show **r05** (`gallery/neural-networks/cnn/current/pp_neural_networks_cnn_wildcard_v14.png`) beside it as the alternative flavour, and **r03** (`gallery/neural-networks/cnn/trials/pp_neural_networks_cnn_iterate_v5.png`) as the tall-but-dishonest summit it replaced.

**If REWORK on r04, the r06 work order is a composition move, not a parameter:** the visibility bound scales with the top plane's row pitch, so buy the summit's height with PITCH.
- Break the width-monotone rule for the 7² plane only: make it the widest and deepest plane on the sheet, cropped by the top-right frame if it must be. That inverts the pyramid toward meaning.
- Re-run the 13/13 sweep at the new pitch.
- Keep one projection basis. Get pitch from the plane's footprint, never from a per-plane KY.

## Mandates to close (only on REWORK → r06, max 5)
1. **A14 + A4: the head is the destination.** The crimson cap is ≥ 30 × 12 mm, carried by the tallest black crest on the sheet, and the 7² rows read as a surface. This must be solved by the top plane's footprint and pitch (above) **with S8's 13/13 still passing**. Print the new sweep table in NOTES. If no footprint that fits A4 passes both, say so, and the translator writes `encoding.md` with a different head grammar.
2. **A16: crimson reads as its own line.** No crimson run parallel within 0.8 mm of black for > 5 mm: break the black under it. The 28² occlusion break resumes at the same height. Heavier crimson, with a double pass ≥ 0.8 mm apart.
3. **S9 + S10: the caption discloses.** "HEIGHT SCALED PER MAP" (or one activation scale for 56²/28²/14²). "RINGS = CAM − MEAN 6.9 → 9.4 (ABOVE RUNNER-UP 6.86)".
4. **A17: craft floor and gaps.** Zero black–black approaches under 0.8 mm on 224² (r04 min 0.5 mm, y 25–75). Remove the torn-corner wiggle at x 48–52, y 143–146. Caption-to-input gap = G.
5. **A18: type against geometry.** "MEANING" clears the top plane by ≥ 13 mm, and the title regains weight with no parallel closer than 0.8 mm.

Deferred: S6 (process, the translator's job). A12 (cream preview, tooling, argued).

## Preserve
- **The one forward pass** (`maps.npz`, argmax (4,3), front rows correlating ≥ 0.994). Do not re-run it.
- **S8 13/13** on the top plane, with Catmull-Rom interpolation and no cos² hills.
- **The four ERF loops** as 50 %-mass ellipses within 0.33 mm, lying ON their surfaces, with the 28² break real.
- **The summit rings** as exact level sets of the drawn field, described as visible-only front arcs.
- **The monotone Schotter channel** (lower four planes): rows 38/28/19/14, strictly rising pitch, strictly falling breaks per row, no terrain stroke under 3 mm.
- **The 28² corner spike**: it is the map maximum, so it stays (A15 argued).
- **The shared type axis** x = 17.75 (title, caption, input front-left corner). Right-flush planes at x = 195. Equal gaps (re-solve them, still equal).
- **Plot economy**: ≤ 12 k commands, travel ≤ 0.3 × draw, 2 pens, 2 clean layers.

## Do not
- Do not buy the summit with height scale past the visibility bound. That is r03's lie, and science will fail it.
- Do not change KY or the basis per plane to get pitch. One basis; the pitch comes from the footprint.
- Do not delete the 28² corner spike as a "hook". It is data.
- Do not state a feed or dwell the file does not carry. The HANDOFF must describe the gcode (G1).

## Fabrication gate (r04, `gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.gcode`)
Run under rule 6 (forced vote) and the curator's note, even though art FAILS.

| check | result |
|---|---|
| bounds | ink x 17.75–195.0, y 15.05–281.0, inside A4 portrait drawable 10–200 × 10–287. The `preview --stats` bbox's 0,0 is the home travel only. **clean** |
| pens / layers | 2 pens, one clean layer each, **stated order**: `plot layer --list` gives color 0 black, 815 strokes / 11,007 cmds (maps → title → caption), then color 1 crimson, 10 strokes / 530 cmds. No pen cap applies (curator), and each pen is one meaningful layer. **clean** |
| batchable | every run is a self-contained pen-down stroke, so a layer can be batched at any run boundary. **clean** |
| minutes per layer | at `plot job`'s stream-time guard (G1 capped F500, G4 floored 1.0 s): black ≈ 28 min draw + ≈ 27 min dwells + travel ≈ **55–58 min**; crimson ≈ **2 min**. The raw file (F2200, G4 P0.2) previews at 8 min. **sane** |
| score | grade A, 11,537 cmds, draw/travel 3.63, 825 lifts, longest travel 303 mm (return home) |
| floods at detail | the lead cropped the densest zone (224² front, x 20–90, y 25–80) and the summit: rows separate everywhere and there is no solid ink. The sub-0.8 mm approaches art measured (min ≈ 0.5 mm) are real but local; that is craft debt A17, not a flood. **clean** |
| feed / dwell | the file is F2200 / G4 P0.2. **Stream only through `promptplot plot job`** (or the viewer's Plot panel), which applies the Leo slow-feed guard. The legacy `plot` would stream F2200. Carried as G1 |
| package regression | `promptplot/` changed during this piece's rounds (2aa2ba2 plotjob/models, 2026-09-28 23:11; docs commits), so the lead ran both halves of `make check` (re-run 2026-09-29). **`scripts/studio_regression.py`: 121 ok · 0 no-entry-point · 2 error · no drift.** Neither error is engine drift. `millennium-hodge/r03` trips its own `AssertionError: no paper for the key`, and `neural-networks-cnn/r01` hits a `net` module-name collision in the harness's shared `sys.modules` (r01 imports a sibling `net.py`; another piece's `net` loaded first). Neither touches r04. **`make test-ci`: 653 passed, 3 skipped, 1 deselected (9 m 07 s).** **clean** |
| flavour r05 (informational, not the voted plate) | `wildcard_v14.gcode`: bbox inside drawable, 4 layers in stated order: teal 442 strokes / 4,917 cmds → gold 2 / 299 → red 2 / 639 → black 1,149 / 10,577. Draw/travel 0.93 (travel > draw), 1,595 lifts, ≈ 18 / 1 / 1 / 46 min per layer. Fabricable, but uneconomic. If Juan picks `reach-dial`, add a travel mandate to RD1–RD5 (travel ≤ 0.5 × draw) |

**Gate verdict: clean → vote.** The plate is fabricable as it stands. What fails is aesthetic (art 6.43/6), and the vote carries that.
