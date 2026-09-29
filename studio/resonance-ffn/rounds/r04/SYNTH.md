# Synth — resonance-ffn after r04 · 2026-09-29
route: designer
next round: **r05** (round 4 of 5) · parent: **r04** — latest AND eligible best (art 5.00/3 · sci 4/4/5, both FAIL). r04 is the first critiqued round that honours J2 (science: 0 mm of r01's coloured ink moved; art: every element present) and it carries J1's bead, the Stroke IR and the light→dark plate job, which r01 lacks. Where r04 regressed against v9 (type, halo ends, scatter footprint), restore from r01/v9 — those are named below, not a reason to fork r01 again.

**Fabrication gate:** not run — not a double PASS. Baseline r05 must hold or beat (science-verified on the r04 gcode): 6 layers 720 / 1058 / 201 / 1082 / 268 / 1422 = 4,751 pen cycles · 14.26 m draw · 9.49 m travel (67 %) · bounds x 15.4–196.5, y 15.6–280.4 on A4 portrait, margin 10 · in-layer hops > 80 mm: crimson 141, blue 173 (accepted: one forced region change each), black 93 and 90 (not accepted) · ≈ 201 min on the clamped plate model. Juan accepts a longer session and six colours *if* the batching and colour changes are right — so waste goes, ink stays.

## The instruction
Fork `rounds/r04/piece.py` to `rounds/r05/piece.py` and make r04 read like v9 again with J1's bead in it — same composition, same six pens, no element added or removed: first put back the three looks r04 lost against `gallery/studio/res_ffn/current/pp_res_ffn_v9.png` (the stage type's width, the halo ellipses reaching the field, the scatter's small specks), then give every place where same-pen bead trains now meet — the Q/K fan tips, the ochre rope into Z, the four FFN pinch nodes — the discipline the continuous dot demands (≥ 2 mm apart, or all but one ending on a dot, the axis alone reaching a node), then swap the two backward FFN labels into chain-rule order, and finally re-sweep the black layer bottom→top in one pass (∂L/∂A twin and backward labels → bracket/FFN → softmax → hero → fraction → title) and cut the batch table at region boundaries so each Leo batch is one place on the sheet. Judge every fix in 4× crops at 0.35 mm nib width, side by side with the same crop of v9.

## Mandates to close
1. **J2 — restore three looks r04 regressed (A10 · A11 · A12).** Test, each against v9.png:
   - **A10 type:** `nonlinearity` (y ≈ 55) and `nonlinearity′` (y ≈ 26) at v9's word width, measured off v9.png (r01 ≈ 16.82 mm; r04 12.84 mm). The code passes the same `tracking` as r01, so the shared glyph metrics changed underneath: set the tracking from the measurement, not from r01's number. Every i/l stem ≥ 0.6 mm clear of its neighbours; the 4× crop reads "nonlinearity", not "nonlhearty". Check `expand`, `project`, `softmax`, `projectᵀ`, `expandᵀ` the same way.
   - **A11 halo ends:** the six `)(` halo arcs must end ON the field, not ≈ 10 mm short in open paper at (≈ 70, 192) / (≈ 70, 140) and mirror. Replace the circular keep-out (21λ + 8 px round each source) with the real crest ink + 0.55 mm, so each arc runs until it meets the outermost ring it passes behind. Test: every halo-arc endpoint within 1.0 mm of black crest ink; 0 chords; 0 stubs; arc length per ellipse ≥ r04's.
   - **A12 scatter:** the 214 scatter marks ink no larger than their v9 footprint (measure v9.png; r04 draws discs up to ≈ 1.5 mm). Same count and positions; a mark whose disc would sit > 50 % on a crest line may nudge ≤ 0.6 mm into the adjacent trough. Never delete one.
2. **A3 + art M1 — same-pen bead bundles.** Zones: the crimson fan tips x 78–92 / blue x 118–132, y 190–215 (166 dots still off-phase in r04); the ochre 5-train rope (105, 85) → (97, 65); the V leader stubs piercing the ochre dotted ")" at x ≈ 185. Test: in a 4× crop of each zone, no two same-pen trains run < 2.0 mm centre-to-centre for more than 5 mm, and no dots from different trains touch. Where trains must meet, all but one end on a dot (trimming allowed, as r04's 82 mm); **no path deleted**. Report off-phase dots per zone (target 0 in the funnel). A second NOT FIXED fires rule 2.
3. **A5 + art M3 — the FFN block.** Near each of the four pinch nodes (x ≈ 144 / 158 / 165 / 178 at y 64 and y 35), end every non-axis streamline where it comes within 0.8 mm of its neighbour, so only the axis line reaches the node — no solid violet wedge in a 4× crop, and still 5 + 5 lines forward and backward (S4 must hold). The bracket legs end ON the expand/project pinch nodes (not in air beside the crests); the black bracket touches no violet ink; ≥ 1.5 mm between the dome's dotted top envelope (x ≈ 158, y ≈ 73) and the bar or `FFN`. A second NOT FIXED fires rule 2.
4. **S6 — backward FFN order (J2-compatible: two words swap).** Flowing ◄ from ∂L/∂Y, the stage at packet x 167.5–182.1 is labelled `projectᵀ` (W₂ᵀ) and the stage at x 134.8–150.2 `expandᵀ` (W₁ᵀ); `nonlinearity′` stays in the middle. No packet moves. State in HANDOFF that this corrects the reference.
5. **A1 — the Leo plate job, finished.**
   - **Black is one bottom→top sweep:** no in-layer G0 > 80 mm on black (r04: 93 backward row → softmax, 90 hero → title). Route through the bracket/`FFN` at y ≈ 74, and enter the title from the fraction.
   - Crimson 141 / blue 173 stay as the only forced hops (argued, accepted).
   - Travel ≤ r04's 9.49 m; cycles ≤ r04's 4,751 + whatever A11 adds (report the delta).
   - **Region-aligned batches:** the batch table in NOTES cuts at every region change, as `plot layer <gcode> <pen> --strokes S:E` ranges, each ≤ 400 strokes and ≤ ≈ 20 min on the clamped model. Where `plot plate --batch-strokes 400` would straddle a region change, name that batch.
   - Re-paste the `plot plate … --layers 2,1,3,0,4,5 --paper a4:portrait --margin 10 --dry-run` summary.
   - Keep the per-layer minutes table, the total, and the session plan (stop points at swap waits) on the clamped model (F500 draw, 2000 mm/min travel, 2 s/cycle, 90 s/swap, 20 s/re-zero). Never claim feeds the file lacks.

Deferred (ledger, with reasons): A6, A7, S1, S2, S3, **S7** (σ′ rank inverted — recomputes a kept curve) and **S8** (A→V wiring, ghost Λs, Z at 2× bound) are blocked by J2 and wait for Juan's ruling on whether traced shapes may be recomputed in place. **A13** (bead weight vs hierarchy) is family-level: DOT_R stays the shared 0.15 mm until Juan decides for all three siblings. S0 (dossier/encoding) is the curator's.

## Preserve
- **J2 as r04 holds it:** every coloured stroke of r01 at r01's position (science: 0 mm moved). That covers:
  - the title, rule and dot (v 0.06–0.08);
  - 5 + 5 Q/K rows with their 20 fans and 12 verticals, and `Q·Kᵀ/√d_k`;
  - the two-bullseye hero (d = 35 λ, λ 1.211 × 1.412 mm), its halos, 214 scatter and 232 stipple dots;
  - softmax with its 6 peaks + 3 ghosts, 5 V rows and the ochre falls;
  - `Z = AV` on the single Z → FFN → Y axis at y ≈ 64;
  - the FFN bracket with expand / nonlinearity / project, then Y and its continuation;
  - the full backward row with the ∂L/∂A twin (0.39 scale), 6 arrowheads and both drop curves.
- **J1's bead:** one closed loop, r 0.15 mm, 1.0 mm pitch, end-anchored, phase-locked. It is on every dotted line: NN median 0.998 mm, 0 micro-dashes, 0 `-` ticks. It is the family constant shared with resonance and resonance-backprop.
- **The textures rule:** stipple caps and scatter keep r01's mark count and positions, one round dot each, and are never re-pitched to 1 mm. The stipple caps have no flood (A4b, confirmed).
- **A4 (a) confirmed:** no halo chords at y ≈ 191 / 140 and no stub at x ≈ 150. A11 extends the arcs along the curve and must not bring a chord back.
- **A5 parts confirmed:**
  - the `′` sits ≤ 0.6 mm after `nonlinearity`;
  - `∂L/∂A` has 1.5 mm of clear air under the twin;
  - `FFN` is lifted 2 mm.
- **The stream:**
  - six layers, each entered once, streamed light→dark with `--layers 2,1,3,0,4,5`;
  - the file order is proven equal to the computed order (the `_greedy_by_start` / `_polish` machinery);
  - the invisibility pass leaves 0 dots on same-pen ink, in label boxes, on nodes, or co-incident;
  - arrowheads are solid, one pen-down each.
- **Lineage and depth:** Csuri & Shaffer, *Sine Curve Man* (1967), "a form and its function-mapped copy on one plotter sheet"; flat. Restate it in HANDOFF.

## Do not
- Do not delete, thin or replace any element, and do not re-pitch a texture to 1 mm. J2 binds, and Juan rejected r02/r03 for exactly this.
- Do not "fix" the halos by closing them with chords or by deleting the arcs. They end ON the ring they pass behind.
- Do not trust r01's `tracking` numbers for the type. Measure v9.png. The glyph metrics under them have moved.
- Do not change DOT_R, DOT_PITCH or the bead mark on this sibling alone (A13 is family-level).
- Do not recompute the σ′ notch, the Z envelope, the ghost Λs or the leader origins (S7/S8/S3 wait for Juan). Only the S6 label swap is in scope.
- Do not re-enter a colour layer, and do not let the renderer's nearest-start re-sort undo the black sweep. Prove file order = computed order again on all 6 pens.
- Do not run `git checkout` or any revert on shared files (`generators.py` glyphs included). If the type needs different metrics, set them in the piece.
