# Synth — resonance-backprop after r02 ∥ r03 (parallel) · 2026-09-29
route: designer
next round: r04 · parent: **r01** (Juan's "original", with v5's tonal field). Chosen by Juan's verdict and the regression rule, not by score. MERGE: named stroke and batching machinery from r03, r02 and the resonance r10/r05 siblings. No thesis from either flavour.

**Ranking.** r03 (art 5.71/4 · sci 7/6/6) beats r02 (5.71/4 · 5/5/4) on scores, but:
- both FAIL;
- both REGRESS J2 (they delete the packet blocks, the halos, the leaders and the backward band);
- Juan ranks the original above any rework: "the original was much more beautiful — we just needed the dot lines to be more continuous, not to remove the waves".

r03 is kept on disk as the `gradient-as-phase` flavour, the strongest alternative and a candidate for its own slug. r02 is kept as the `the-fold` flavour.

**Fabrication gate:** not run, because neither round is a double PASS. Baseline for r04 to beat, read from r01's v8 gcode (`plot layer --list`):
- per layer: 0 crimson 769 · 1 blue 766 · 2 gold 578 · 3 green 431 · 4 black 1,509 strokes;
- total 4,053 pen cycles, 11.39 m draw, 11.90 m travel (105 %).

Continuous dots will roughly double the cycle count; resonance r10 went from 3,471 to 6,092 cycles. Expect a plate job of ~4–5 h on Leo. Juan accepts the long session, provided batching and colour changes are right. The waste is what must go.

## The instruction
**Measure the reference first.** Juan's REWORK sits on `gallery/studio/res_backprop/current/pp_res_backprop_v5.png`, but `rounds/r01/piece.py` renders v8, and v5's gcode was overwritten. So:
- Read v5's tonal field off that PNG in mm, using its printed axes: the dotted crest-arc field inside the wide oval, every nested dotted halo ellipse (extent, centre, count) and the scatter-dot field (count, the extent it covers, radius classes).
- Record those as `(u, v)` MEASUREMENTS in NOTES.
- Fork `rounds/r01/piece.py` to `rounds/r04/piece.py` and rebuild v5's field in place of v8's dashed oval.

Everything else stays exactly where r01 draws it:
- every element, all five pens and their meanings;
- the title and the four corner crosses;
- the rail, with both arrows;
- the Q, K, V, Z and ∂L/∂· packets;
- the hero, the softmax row, the fans, the droplines, the arrowheads and the fractions.

Then change only how marks are made and how the sheet streams:
1. **Continuous dots, in two classes.**
   - **Dotted LINES** (fans, leaders, droplines, guides, rails, axis continuations, halo ellipses, dotted crest arcs, the backward arrows' shafts, packet envelopes): one round dot every 1.0 mm, end-anchored. Use resonance r10's constants (`DOT_PITCH = 1.0`, `DOT_R = 0.15`, `DOT_MAX = 0.6`) so the three sibling plates share one dot, and r03's end-anchored `_dotted` (n = round(len/pitch), n + 1 dots).
   - **TEXTURES** (the scatter field and the beaded dropline columns): keep v5's mark count and positions, and make each mark one round dot or one solid disc by radius. Never re-pitch a texture to 1 mm: that is the mud in resonance r10.
2. **Earn every cycle.** Drop only dots that would be invisible:
   - within 0.3 mm of other same-pen ink;
   - inside a label box plus 0.9 mm (use r03's exact `Rect`/`Union` halo clip);
   - on a node disc;
   - on a co-incident duplicate path.
   Where same-pen dotted paths run closer than 2 mm (the paired Q and K fans, the ochre V fans, the green ∂L/∂Z fans), phase-lock their dots across the pair.
   Chain every multi-pass glyph into one pen-down (resonance r05's fused type; r02's `giant_type` engine request).
3. **Stream it as a Leo plate job.**
   - Order every colour layer reversal-aware and spatially contiguous (r03's `_order`, nearest end with reversal), so each 400-stroke batch of `promptplot plot plate --batch-strokes 400` is one region of the sheet.
   - Stream light→dark: goldenrod, dodgerblue, forestgreen, crimson, black. Say why in NOTES.
   - In NOTES, give per-layer cycles, draw, travel and minutes, plus the total, on the PLOT_JOBS model (F500 draw, 2000 mm/min travel, 2.0 s per cycle, 90 s per swap, 20 s per re-zero).
   - Also give the batch table as `--strokes S:E` ranges per layer, and a session plan: where a 4–5 h plate can pause at a batch boundary and resume.

## Mandates to close
1. **J2 — keep the original.** Test: an element-for-element diff against v5.png, all at r01 positions (≤ 1 mm moves):
   - 5 + 5 Q/K rows, 4 V rows, the Z packet;
   - the fraction, the 5 softmax peaks, 4 ghosts and 9 baseline markers, the 9 droplines;
   - the hero (bullseyes m 1–9, comb m 10–50 in the lens, d = 59·L, `_Guard` 0.82 mm / 25°);
   - v5's halo ellipses and scatter (±5 % count);
   - the whole backward band with every arrowhead: ∂L/∂Z, ∂L/∂A, ∂L/∂Q, ∂L/∂K, ∂L/∂V;
   - the rail with both arrows and words, the title, subtitle and 4 crosses.
2. **J1 — continuous dots.** Test on the gcode:
   - on an isolated leader (the ∂L/∂Q fan), the same-pen dot nearest-neighbour median is 0.9–1.1 mm, with a dot at both ends;
   - 0 micro-dashes of 0.3–1.2 mm on any dotted line;
   - the paired fans read as parallel dotted lines, not interleaved noise, at 0.35 mm nib width (crop and look);
   - the v8 dashed oval is gone because v5's dotted field replaces it.
3. **A9 — plot discipline** (Juan 2026-09-29: more than 4 colours and a long session, *if batching and colour changes are right*):
   - five layers, each entered once, in the stated order;
   - no in-layer G0 > 80 mm except layer entry;
   - total travel ≤ draw + dot count × 1.0 mm;
   - 0 invisible dots (the four rules above);
   - the NOTES budget, batch table and session plan;
   - bounds clean on A4 portrait.
4. **A7 — v5's greying band, without deleting.** The scatter and halos must not cross the Q/K/V fans or any label. Occlude or halo the texture where a fan or word passes, keep its count, and crop the densest 20 × 20 mm of the field at nib width to show 0 flood.
5. **A10 + A11 — lineage and small type.**
   - Name one movement and one real work and the ORDER it lends. It must differ from the siblings and flavours: Young 1807, LeWitt and Riley are taken. A suggestion to test, not impose: Helmholtz, *On the Sensations of Tone* (1863), wave-composition figures: rows of partial waves summed into one compound wave, which is Q·K → A → Z = AV as a plate order.
   - Declare "flat — a reproduction of a flat plate diagram" in HANDOFF.
   - Crop the subtitle `frequency interference • selection • backpropagation` at 0.35 mm nib. If it clogs, loosen the tracking only.

Deferred in the ledger: A3 (comb flood), which the gate checks with a nib-width crop in NOTES and which becomes a mandate only if it floods. Blocked by J2 until Juan rules: A2 (packet braids), A6 (dead foot / move down). S0 (no dossier/encoding) is for the curator/expert, not the designer.

## Preserve
- **r01's whole composition** (DESCRIPTION § What is on the sheet):
  - the title, rule and dot at v 0.11, the subtitle at v 0.14, and the four crosses with their dotted ticks;
  - the left rail at u 0.07 (`forward pass` ↓ at v 0.19–0.43, `backward pass` ↑ at v 0.62–0.85);
  - Q (u 0.10–0.36) and K (u 0.64–0.90) at v 0.19–0.29;
  - `Q·Kᵀ/√d_k` at (0.50, 0.22–0.25);
  - the hero at v 0.35 (sources at u 0.35 and 0.64, the comb lozenge, the axis, the end circles, the beaded columns);
  - softmax at v 0.45–0.49, V at mid-left, Z at v 0.57 with `Z = AV` below it;
  - the backward band v 0.62–0.85 with ∂L/∂Z directly under Z (**the fold, the plate's one structural idea**).
- **Five pens, five meanings** — Q/∂L/∂Q crimson, K/∂L/∂K blue, V/∂L/∂V goldenrod, Z/∂L/∂Z green, and black for the field, softmax, ∂L/∂A, rails, type and crosses. This is the family grammar shared with resonance and resonance-ffn.
- **v5's wide dotted halo** (DESCRIPTION § Keep: "the closest pen reading of the reference's soft tonal field").
- **From the flavours, craft only:** r03's end-anchored `_dotted`, exact label halos and reversal-aware `_order`; the plot-budget table format from r02 and r03.

## Do not
- Do not cut, thin, simplify or replace any element to save time or cycles. r02 and r03 both did, and Juan rejected it.
- Do not re-use v8's dashed crest oval, and do not draw any dotted line as dashes or a hairline.
- Do not re-pitch textures (scatter, beaded columns) to 1 mm.
- Do not cap packet amplitudes, thin the comb, move the composition or change element counts. A2, A3 and A6 wait for Juan or the gate.
- Do not start a new thesis. The fold, the phase and one-field ideas live in the flavours.
- Do not stream in pen-index order without saying why, and do not leave greedy stragglers that cross the sheet mid-layer.
- Do not re-enter a colour layer after its swap.
