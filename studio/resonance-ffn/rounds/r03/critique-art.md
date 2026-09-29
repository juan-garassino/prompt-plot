# Art critique — resonance-ffn r03 · canon: unassigned (no encoding.md / BRIEF.md; HANDOFF names lineage only: Csuri & Shaffer, *Sine Curve Man*) · 2026-09-29
render: gallery/studio/resonance_ffn/current/pp_resonance_ffn_two-interferences_v13.png (gcode beside it) · compare-to: gallery/studio/res_ffn/current/pp_res_ffn_v9.png · reference: studio/resonance-ffn/ref/reference.png

## Scores

| dim | score | why (pass 1, cold) |
|---|---|---|
| 1 hierarchy | 8 | The black two-bullseye hero (x 37–151, y 165–232) owns the sheet at 3 m. The violet fan is a clear second and the left squiggle stack a third. The twin reads at 1 m. |
| 2 grid & alignment | 6 | Labels do not share a column. `Q` sits at x≈17, while `V`/`Z`/`∂L/∂Z` sit at x≈24 and `∂L/∂Q` at x≈22. The Q row starts at x 15 but every other row starts at x 29. Right ends vary: Q 61, V/Z 78, ∂L/∂Q 81, ∂L/∂K 159, K 174. The droplines do lock to the field centres (61/127, 81/107), which is the one real axis system. |
| 3 tension & asymmetry | 5 | The top half is a mirror: Q and K flank a centred hero at the same height. Only the lower half breaks it. This is the codebase's known failure mode, "subject dead-centre". |
| 4 negative space | 6 | The lower-right block (x 125–200, y 20–70) is leftover, not shaped. It holds one lonely ∂L/∂K row, with the title stranded 25 mm below. `Y` and `∂L/∂Y` are pressed against the right margin (x 191–197 vs 200). The quiet above Q/K is good. |
| 5 craft for pen | 7 | Dotted runs are clean: 1.00 mm round dots, end-anchored. Ring pitch in the hero is ≈1.15 mm, and 6 pens are streamed light→dark with one swap each. Against that, the fan is full of pause-resume stubs: dangling 2–5 mm segments and mid-curve gaps (crop 110–180 × 74–100). About 15 curves converge on the Y node within <0.8 mm of each other. |
| 6 concept legibility | 5 | The hero is a real abstract order (interfering). The lower half is labelled algebra rows (`V`, `Z`, `∂L/∂Z`, `∂L/∂Q`, `∂L/∂K`, `∂L/∂Y`) wired by dotted leaders into nodes, which is semi-schematic. The fan's "tanh above / derivative below" does not read. The lower family is a tangle of crossings, not a visibly derived shape. The twin's ratio −0.39 is a point reflection of a centrally symmetric figure, so the negative sign is invisible: it reads as a small copy. That is the weakest possible "function-mapped copy" for a Csuri lineage. |
| 7 depth & dimensionality | 5 | Flatness is undeclared. Some depth survives in the moiré lens and in the over/under gaps in the fan. Twin-as-distance is not argued. |

**avg 6.0 · min 5 · VERDICT: FAIL**

## Reads at a glance
A big black double-bullseye moiré eye fed by one red and one blue squiggle, a violet lens of curves at right, a stack of coloured squiggles at left, and a small copy of the eye below.

## Acceptance checks
- encoding §11: **n/a.** There is no `studio/resonance-ffn/encoding.md` and no `BRIEF.md`.
- AUTHORING §6 (reference in play; the render is judged as an interpretation of it):
  1. Main forms recognisable without colour: **PASS.** Hero, twin, fan and rows all read in monochrome.
  2. Shadow/structure lines follow the form: **PASS.** Lens diamonds follow the ring geometry.
  3. Fine lines that are really two sides of one thick stroke: **PASS.** None.
  4. Blackest regions intended: **PASS (marginal).** The hero lens bands (y 170–190, 210–230) are intentional. The twin's lens at ~1 mm crossing pitch will run near-solid with a 0.4 nib.
  5. Labels readable at real pen width: **PASS.**
  6. Pen knots at corners/nodes: **FAIL.** The fan's curves pile into the Y node (x≈190, y 102) within <0.8 mm over the last ~3 mm.
  7. Empty travels / tiny marks with no benefit: **FAIL.** Travel is fine (28 %). But the fan's pause-resume stubs are exactly "tiny marks with no visible benefit".
- As an interpretation of the reference: this is a reduction, not an interpretation. It keeps 2 of the reference's ~12 motifs (hero, gradient twin) and drops the packet funnels, softmax, FFN stages and backward stack.

## Biggest weakness
The round took the "two interferences" rewrite path and deleted most of the sheet. Q/K went from 5+5 packet rows to 1+1, and the round removed the 20 dotted fans, the hero's dotted ellipses, its scatter and its stipple caps, `QKᵀ/√d_k`, softmax, the FFN's three stages, ∂L/∂V and ∂L/∂A. What remains is a centred hero over a half-schematic lower field. It has less than v9 had and does not gain a stronger idea in exchange. Juan's binding note (FEEDBACK.md, 2026-09-28) forbids exactly this: "keep EVERY element… the ONLY change wanted is dot continuity… Do not remove, thin or replace anything". That note wins over the rubric's concept/tension scores. The next round must not chase them by redesigning.

## Mandates
1. **Rebuild the v9 / r01 sheet element-for-element and change only the dots.** Restore:
   - the five crimson Q rows and five blue K rows with their 20 dotted fans into the hero, and the `Q·Kᵀ/√d_k` fraction
   - the hero's dotted ellipses, scatter dots and stipple caps
   - the `softmax` label with its six-peak row, the five ochre V rows, and the `Z = AV` axis
   - the FFN bracket with expand / nonlinearity / project in v9's lowercase type, then `Y`
   - the full backward row: ∂L/∂Q ×2, ∂L/∂K ×2, ∂L/∂V, the ∂L/∂A twin with label, ∂L/∂Z, projectᵀ / nonlinearity′ / expandᵀ, ∂L/∂Y
   - the centred title with its rule and dot

   Apply r03's dot (one round 0.12 mm-r dot, 1.00 mm pitch, end-anchored) to every dotted path.
   Test: blink v9 against the new render. Every v9 mark is present at the same place, and only dotted runs differ.
2. **Converging dotted paths never interleave.** Where the Q/K dotted fans funnel into the hero (sheet ≈ x 85–125, y 180–215 in v9 coordinates) and where the ochre leaders fall from softmax into V/Z, keep neighbouring dotted paths ≥ 2 mm (2 pitches) apart centre-to-centre. Where they would merge, end a path early on a dot rather than letting two dot trains braid.
   Test: a 30 × 30 mm crop of the funnel shows separate dot trains, with no dot-noise patch.
3. **Keep r03's plot discipline on the full sheet.** Stream the 6 pens light → dark, one swap per pen, never re-entering a layer. Spatially order strokes within each layer so travel is ≤ 30 % of draw (v9 was 12.2 m travel for 12.1 m draw; r03 proved 28 %). No single stroke should be longer than a batch boundary. Report minutes per layer and in total in HANDOFF.
   Test: the HANDOFF stats line shows travel ≤ 30 %, 6 layers / 5 swaps, and per-layer minutes.

## Follow-up on open mandates
No LEDGER.md and no prior critique-art exist, so there are no A* mandates on record. Juan's FEEDBACK note is the only open instruction:

| id | status | evidence |
|---|---|---|
| J (dot continuity) | FIXED | Every dotted path is now round dots at 1.00 mm pitch, end-anchored (junction crop at 85–105 × 90–115). The dots read as continuous lines, with no micro-dash stutter. |
| J (keep every element, remove nothing) | REGRESSED | Removed: 8 of 10 Q/K rows, all 20 dotted fans, the hero's dotted ellipses, scatter and stipple caps, the QKᵀ/√d_k fraction, the softmax row, 1 V row, the FFN bracket and its 3 stages, both ∂L/∂Q and ∂L/∂K pairs (reduced to one each), ∂L/∂V, the ∂L/∂A / ∂L/∂Z labels, the FFN transposes, and the title rule. The render (23:41) postdates the note (23:39). |
| J (all six pens) | FIXED | 6 pens retained, one layer each. |

DESCRIPTION.md § Keep:

| keep item | still true? |
|---|---|
| v9's cleaner lowercase stage labels | NO. The stage labels are gone. |
| FFN fan: forward dome vs backward twin peaks, derivative visible as a shape change | PARTIAL. There is now one fan with tanh above and the derivative below. The lower family crosses itself heavily, whereas v9's family "never crosses", so the derivative-as-shape no longer reads. |
| ∂L/∂A mini-interference at 0.39 scale | YES. It is kept and promoted to a main figure. |
| Top half inherits the benchmark's funnel and hero intact | NO. The funnel is gone and the hero has been redrawn as a heavier crosshatch lens. |
| One axis carrying Z → FFN → Y across the lower sheet | PARTIAL. It survives as the y 102 horizon, but Z no longer rides it. |

## Regressions vs compare-to
- **Element deletion against a binding owner note.** This is the main regression, detailed in the follow-up table.
- **Hero construction.** v9's hero has fine concentric crests with a narrow midline lens, dotted ellipses and scatter. r03's has a wide, heavy crosshatch lens with dark diamond bands, so it reads as hatching rather than resonance. The dotted halo that gave v9 its atmosphere is gone.
- **FFN nonlinearity.** v9's compact non-crossing dome / notched twin has become a large fan with stubbed, broken curves and a crossing tangle below.
- **Title.** v9's centred title with rule and dot sat on the top axis. The title is now a caption in the bottom-right corner, detached from everything.
- **Improvements worth carrying back:** round continuous dots; travel down from 12.2 m to 3.2 m (101 % → 28 % of draw); commands down from 63.5k to 30k; a clean light → dark 6-layer order. Mandates 1 and 3 keep these improvements and bring back the lost elements.
