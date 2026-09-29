# Synth — resonance-ffn after r02 ∥ r03 (parallel) · 2026-09-29
route: designer
next round: r04 · parent: **r01** (v9 = the code on disk = Juan's "original"). Chosen by Juan's verdict and the regression rule, not by score. MERGE: r03's stroke IR, dot and stream machinery, plus the resonance sibling's dot constants. No thesis from either flavour.

**Ranking.** r03 (art 6.00/5 · sci 6/5/5) beats r02 (5.57/5 · 5/6/3): art min ties, and science min decides. But:
- both FAIL;
- both REGRESS J2 (packets, fans, halos, scatter, FFN stages and ∂L rows deleted);
- Juan ranks the original above any rework: "the original was much more beautiful — we just needed the dot lines to be more continuous, not to remove the waves".

r03 is kept on disk as the `two-interferences` flavour and r02 as `the-squash`. Their mandates travel with them (LEDGER § Flavours).

**Fabrication gate:** not run, because neither round is a double PASS. This is the baseline r04 must beat, read from r01's gcode (`current/pp_res_ffn_v5.gcode`, which holds v9's output: same draw and command count):

| measure | value |
|---|---|
| pen cycles | 3,725 |
| strokes per layer | 0 crimson 697 · 1 blue 705 · 2 gold 492 · 3 green 157 · 4 violet 197 · 5 black 1,477 |
| draw / travel | 12.07 m draw · 12.23 m travel (101 %) |
| bounds | X 0–196.5, Y 0–280.4 |
| time on Leo | ≈ 155 min |

Continuous dots will raise the cycle count (resonance r10 went from 3,471 to 6,092). Juan accepts a longer session and more than four colours, *provided batching and colour changes are right*. Remove waste, not ink.

## The instruction
Fork `rounds/r01/piece.py` to `rounds/r04/piece.py`. Keep v9's composition, every element and all six pens exactly where r01 draws them. Change only how marks are made and how the sheet streams: this round turns Juan's continuous-dot original into a batched six-pen Leo plate job.

1. **Move r01's geometry onto r03's stroke IR.** r03's `_S`/`Stroke`, `_apply_halos` and `_order`/`_emit` let the whole sheet exist as geometry before G-code is written. Then apply only non-destructive passes:
   - label halos (clip dots out of each label box + 0.9 mm);
   - node keep-outs (0.55 mm);
   - no co-incident duplicate ink ("the carrier is the axis");
   - fused multi-pass type;
   - every `_fdot` drawn as a round touch, loop or spiral by radius, never a `-` tick.
2. **Two classes of dot.**
   - **Dotted LINES:** the 20 Q/K fans, the leader dots, softmax droplines, ochre curves into V and Z, the Z/Y continuations, green and violet drop curves to the backward row, the halo ellipses and the backward arrows' shafts. They take one family dot: `DOT_PITCH = 1.0`, `DOT_R = 0.15` (resonance r10's constants, so the three siblings share one mark), laid end-anchored as in r03's `_dots` (n = round(L/pitch), n + 1 dots).
   - **TEXTURES:** the hero's scatter dots and the midline stipple caps. They keep r01's mark count and positions, and each mark becomes one round dot. Never re-pitch a texture to 1 mm: that is resonance r10's mud.
3. **Stream it as a Leo plate job.**
   - Keep the family pen indices (0 crimson Q · 1 blue K · 2 gold V · 3 green Z · 4 violet FFN/Y · 5 black field/softmax/type).
   - Stream light→dark with `--layers 2,1,3,0,4,5` (gold, blue, green, crimson, violet, black). Say why in NOTES: dark ink lands last over dry light ink.
   - Order every layer reversal-aware and spatially contiguous, so each 400-stroke batch of `promptplot plot plate --batch-strokes 400 --paper a4:portrait` is one region of the sheet.
   - Rehearse it with `--dry-run`, and paste the output summary into NOTES.

## Mandates to close
1. **J2 — keep the original.** Test: element-for-element against v9.png, all at r01 positions (≤ 1 mm moves, except A5's bracket legs):
   - 5 + 5 Q/K packet rows and their 20 fans, plus `Q·Kᵀ/√d_k`;
   - the hero, with its dotted ellipses, scatter (same count ±5 %) and stipple caps;
   - `softmax` and its 6-peak row, the 5 V rows, and the `Z = AV` packet on its axis;
   - the FFN bracket with expand / nonlinearity / project in v9's lowercase, then Y and its continuation;
   - the full backward row: ∂L/∂Q ×2, ∂L/∂K ×2, ∂L/∂V, the ∂L/∂A twin, ∂L/∂Z, projectᵀ / nonlinearity′ / expandᵀ, ∂L/∂Y, every arrowhead and both drop curves;
   - the title with its rule and dot.
2. **J1 + A3 — continuous dots that never braid.** Test on the gcode:
   - on an isolated leader (the ∂L/∂Y drop curve), the same-pen dot nearest-neighbour median is 0.9–1.1 mm, with a dot on both ends;
   - 0 micro-dashes of 0.3–1.2 mm anywhere;
   - in a 30 × 30 mm crop of the Q/K funnel (sheet ≈ x 85–125, y 180–215) and of the softmax→V/Z ochre fall, the trains read as separate dotted lines at 0.35 mm nib width: ≥ 2 mm apart or phase-locked, and where they must merge, one ends early on a dot;
   - no path deleted.
3. **A1 — plot discipline** (Juan 2026-09-29; the curator note). Test:
   - 6 layers, each entered once, in the stated order;
   - no in-layer G0 > 80 mm except layer entry;
   - total travel ≤ draw + dot count × 1.0 mm;
   - 0 invisible dots (within 0.3 mm of same-pen ink, in a label box, on a node, co-incident);
   - bounds clean on A4 portrait.

   NOTES gives:
   - a per-layer table of cycles, draw, travel and minutes, plus the total, on the PLOT_JOBS model (F500 draw, 2000 mm/min travel, 2.0 s per cycle, 90 s per swap, 20 s per re-zero), stated as the clamped `plot plate` model (S5 — never claim feeds the file lacks);
   - the batch table as `--strokes S:E` per layer;
   - a session plan: where a 4–5 h job can stop at a batch boundary and resume (`--resume`), and where the re-zero checks fall.
4. **A4 — what continuous dots expose** (lead-observed on v9's hero crop):
   - (a) each halo ellipse is drawn as its own arc and stops ON the curve at the crest keep-out. No flat dotted chords at y ≈ 191 / 140, and no vertical stub on the right ellipse at x ≈ 150;
   - (b) the stipple caps at r01 density show 0 flood in a 4× crop;
   - (c) 0 `-` tick dots.
5. **A5 + A2 — collisions without deleting, and the lineage.**
   - Shorten the FFN bracket so both legs land on pinch nodes, not on `project`'s crest at (0.85, 0.74), and lift `FFN` 2 mm clear of the bar.
   - Set `nonlinearity′`'s prime as a raised mark ≤ 0.6 mm after the last glyph (it floats detached in v9).
   - Give `∂L/∂A` 1.5 mm of clear air under the twin.
   - Restate the lineage in HANDOFF + NOTES: Csuri & Shaffer, *Sine Curve Man* (1967), "a form and its function-mapped copy on one plotter sheet". That is the FFN row and its transposed backward row, and the hero and its 0.39 ∂L/∂A copy.
   - Declare "flat — reproduction of a flat plate diagram".
   - State the dome and twin-peak streamline counts (S4). If one is missing, restore it; never remove one.

Deferred in the ledger:
- Blocked by J2 until Juan rules: A6 (packet overlaps, V knot, ∂L pairs), A7 (≥ 8 mm lower-third gap), S1 (twin carries no ∂L/∂A), S2 (tanh vs GELU), S3 (5/5/6 counts).
- S0 (no dossier/encoding) is for the curator/expert, not the designer.

## Preserve
- **r01/v9's whole composition** (DESCRIPTION § What is on the sheet):
  - the title, rule and dot at v 0.06–0.08;
  - Q (u 0.09–0.36) and K (u 0.64–0.91) blocks at v 0.14–0.30, with their dotted fans;
  - the fraction at (0.50, 0.28–0.31);
  - the two-bullseye hero at (0.40/0.60, 0.44), byte-identical crest maths (d = 35·L, 1.21 × 1.41 mm pitch);
  - softmax and its 6 peaks at v 0.57–0.61;
  - V mid-right at v 0.65–0.72;
  - the one Z → FFN → Y axis at v 0.78;
  - the backward row at v ≈ 0.88 with the ∂L/∂A twin at 0.39 scale (d = 14·L).
- **The FFN fan:** the forward flat-topped dome against the backward twin peaks with an absolute notch (the family never crosses). DESCRIPTION calls it the best idea this sibling adds.
- **v9's lowercase stage type** (not v5's condensed type).
- **Six pens, six meanings.** This is the family grammar shared with resonance and resonance-backprop: Q crimson, K blue, V goldenrod, Z green, FFN violet, and black for the interference field, softmax, the title and the bracket.
- **From r03, craft only:** the Stroke IR, `_dots`/`_the_dot` end-anchored placement, `_apply_halos`, the reversal-aware `_order`, and the per-layer budget table format.

## Do not
- Do not cut, thin, simplify or replace any element to save time or cycles. r02 and r03 both did, and Juan rejected it.
- Do not draw any dotted line as dashes or a hairline, and do not re-pitch textures to 1 mm.
- Do not cap packet amplitudes, drop V rows, move the composition, change the dome to GELU or re-encode the twin. A6, A7, S1, S2 and S3 wait for Juan.
- Do not start a new thesis. The squash and two-interferences ideas live in the flavours.
- Do not re-enter a colour layer after its swap. Do not leave greedy stragglers that cross the sheet mid-layer. Do not stream in pen-index order without stating the `--layers` order.
- Do not claim feeds or dwells in HANDOFF that the gcode does not carry. Quote the clamped plate-job model.
- Do not run `git checkout` or any revert on shared files. r01 destroyed another agent's glyph work that way (r01 NOTES §8).
