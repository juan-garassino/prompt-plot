# Synth — resonance-backprop after r04 · 2026-09-29
route: designer
next round: r05 · parent: **r04** (latest = eligible best). r04 is r01 + v5's measured field + J1 dots + stream order, and the art critic's element audit confirms nothing was removed. r03 still leads on raw score but is J2-ineligible, so it stays a flavour and is not a parent.
round: 4 of 5. If r05 FAILs, r06 is the last designer round, and after it the plate goes to vote with an honest note.

**Scores r04.**
- Art 5.71/4, FAIL. Hierarchy 7, grid 6, tension 6, space 5, craft 6, concept 4, depth 6.
- Science 4/3/6, FAIL. Truth and fidelity are held down mostly by traced-packet algebra that J2 freezes (S1/S3/S4, parked for Juan).

**Translator rule not triggered.** J1's *mark* is fixed and only its converging clause is open. A9 moved NOT FIXED → PARTIAL with measured gains: travel 105 % → 83 %, 5 single-entry layers. Both are weight and order problems inside a frozen encoding, not an encoding failure.

**Fabrication gate:** not run as a pass gate, because there is no double PASS. Read for the record on `gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.gcode`:
- `plot layer --list`: 5 layers, 0 goldenrod 769 · 1 dodgerblue 839 · 2 forestgreen 532 · 3 crimson 832 · 4 black 2,680 strokes. Matches NOTES.
- Bounds x 10.17–200.00, y 29.05–267.95: clean on A4 portrait (science critic).
- 5,652 cycles, 14.11 m draw, 11.69 m travel, 230 min on the PLOT_JOBS model.
- `promptplot/` changed during this piece's rounds (`2aa2ba2`, plot plate jobs, 2026-09-28 23:11). So when the plate reaches vote, the gate must also run `scripts/studio_regression.py` and `make check`.

## The instruction
**Re-rank the ink on r04's sheet. Keep every mark where it is and change only how heavy each class of mark is, so the plate reads the way the reference does.** The target reading: two bullseyes and the comb are the blackest things in the band, the interference field is a soft haze of pen touches round them, the coloured leaders are a mid-weight between, and nothing stabs into anything.
1. **The field.** Fork `rounds/r04/piece.py` and make every *field/texture* dot a single pen touch at its existing position: the 22×2 dotted crest rings, the 3×2 halo ellipses and the scatter. A pen touch is one pen-down with no drawn circle, inking ≈ the nib diameter.
   - Verify in the plate gcode that each touch survives the pipeline as one cycle. If a zero-length G1 is dropped, use a ≤ 0.05 mm closed micro-loop.
   - Where two field dots sit < 0.8 mm apart, slide one ALONG its own circle or ellipse to ≥ 0.8 mm. Never move a dot off its locus, and never delete one.
   - Leave every leader/fan/dropline/guide/envelope dot as r04's 0.30 mm circle at 1.0 mm pitch. That is the family's line dot.
2. **The collisions.**
   - Trim each ∂L/∂Q / ∂L/∂K leader along its own path, so its arrowhead stops ≥ 1.5 mm outside the packet envelope and ≥ 2 mm from the next head.
   - Let the goldenrod V loops yield (a gap on the same path) where they cross the Z packet envelope + 1.5 mm.
   - Flip the ◁ head at x 152.5 on the ∂L/∂Z → ∂L/∂V edge to ▷.
3. **The comb.** Rebuild it as the true two-source standing-wave crests: the hyperbolae r₁ − r₂ = const, symmetric about x 104.83, in the same lens, with the same crest count and the same 1.042 mm on-axis pitch. This replaces r01's S₁-only circles. The reference's comb is symmetric too.
4. **The stream.** Re-batch black into compact regions:
   - one frame loop for the crosses, rail and title;
   - then content batches of ≤ ~100 × 80 mm.

   End the crimson upper block on the stroke nearest the lower block. Aim for the same ~230 min session with fuller, tighter batches, so Leo is saturated.

## Mandates to close
1. **J2 — keep the original** (only Juan closes; r04 FIXED pending Juan). Hold it.
   - Test: the art critic's element audit against v5 finds the same inventory. That means 5 + 5 Q/K rows, 4 V rows, Z, all five ∂L blocks, every halo, the scatter (8 discs), every leader and all 38 arrowheads, the rail, the crosses, the title and the five pens.
   - The field dot count is unchanged from r04: 1,777 field + 98 texture, ±0 except dots slid along their locus.
   - No element moves > 1 mm except leader tips trimmed along their own paths.
2. **A7 — two-class dots, v5's haze back** (merged with J1's converging clause for the field; art M1).
   - Test 1: at arm's length the bullseyes + comb are the darkest marks in x 40–170, y 165–215.
   - Test 2: the halos read a clear step lighter than the Q/K leaders.
   - Test 3: a 4× nib crop (0.35 mm) of the densest 20 × 20 mm shows no touching doublets.
   - Test 4 (on the gcode): 0 black field-dot pairs with centres < 0.8 mm, and every field dot within 0.03 mm of its crest circle or ellipse.
3. **A14 — no leader enters a packet** (art M2 + science arrowhead + J1's converging clause for heads).
   - Test 1: nib crops of both backward corners (crimson x 30–60, y 45–62; blue x 150–180) show paper ≥ 1.5 mm between every head and the packet's dotted envelope.
   - Test 2: head-to-head ≥ 2 mm, with no triangles touching.
   - Test 3: the Z-diamond crop (x 80–130, y 115–140) shows ≥ 1.5 mm of paper between goldenrod dots and green packet ink.
   - Test 4: both heads on the y 85.8 edge point from ∂L/∂Z toward ∂L/∂V.
4. **A9 — plot discipline** (Juan: "batch correctly to saturate Leo … colour changes correctly … more than 4 colours, longer session").
   - Five layers, each entered once, light→dark (goldenrod, dodgerblue, forestgreen, crimson, black). Say why.
   - Every 400-stroke batch is one region. Give each batch's bbox in the NOTES batch table. Black content batches are ≤ ~100 × 80 mm, and the furniture is one frame-loop batch.
   - Black travel ≤ 4.3 m (r04: 5.30).
   - Per pen, no in-layer hop > 80 mm except layer entry, plus at most ONE inter-cluster hop for blue and crimson, within 10 mm of the minimum cluster-to-cluster distance (crimson r04: 138 mm, ~30 over).
   - NOTES must give the per-layer cycles, draw, travel and minutes plus the total (PLOT_JOBS model), the batch table and the session plan.
   - Run `promptplot plot plate <gcode> --paper a4:portrait --dry-run` and paste its summary. Leo's default frame is A5 landscape, so A4 portrait must be stated.
5. **S2 — the comb is a two-source structure.**
   - Test: every comb fringe satisfies r₁ − r₂ = const to ≤ 0.02 mm along its length, with the set symmetric about x 104.83.
   - The on-axis pitch stays 1.042 mm and the count and lens are unchanged.
   - Re-crop `_nib_comb` at 0.35 mm: still a striped lozenge, ≥ 0.6 mm paper between fringes (A3 must not regress).

Deferred in the ledger:
- A13 (the `QK T` superscript gap and the softmax label under the halo rim) goes to r06. A kerning fix ≤ 1 mm is fine if it is free.
- Blocked by J2, for Juan: A2 (braids), A6 (dead foot), S1 (token and row counts), S3 (A and Z derivation), S4 (backward algebra).
- S0 (the dossier) is for the curator.

## Preserve
- **Everything r04 got right, confirmed by the critics:**
  - the whole r01 composition at r01 coordinates (DESCRIPTION § What is on the sheet);
  - the fold with ∂L/∂Z under `Z = AV`;
  - the rail, the crosses, the title/rule/dot and the subtitle.
- **The bullseyes, confirmed by the science critic:** m 1–9 on m·L to 5 µm, d = 59.000 L.
- **The leader dot (J1 mark):** 0.30 mm circles, 1.00 mm median pitch, end-anchored, phase-locked pairs, 0 micro-dashes. Do not change it; the family shares it with resonance r10.
- **Five pens, five meanings, stream order = index order:** 0 goldenrod V/∂L/∂V · 1 dodgerblue K/∂L/∂K · 2 forestgreen Z/∂L/∂Z · 3 crimson Q/∂L/∂Q · 4 black field, softmax, ∂L/∂A, rail, type, crosses. This is the family grammar with resonance and resonance-ffn.
- **v5's measured field geometry** (rings m 10–73 step 3, halos b = 0.40a at a = 196/245.5/300 ref px, 8 scatter discs at seed 7). Only the mark weight changes.
- **The machinery:**
  - `_realize` / `_order` / `plate.py` (stream-order gcode, byte-deterministic);
  - chained glyphs and arrowheads;
  - the label halos;
  - the open subtitle, including the lifted i-tittle;
  - spiral discs at 0.30 mm.
- **Lineage** Helmholtz 1863 (stacked partials → one compound wave). Depth: flat, declared.

## Do not
- Do not delete, thin or re-pitch any dot to lighten the band. Lighten it by the *mark* (a pen touch), not by count. This is J2, and r02/r03 were rejected for it.
- Do not move a field dot off its crest circle or ellipse to de-clump it. Slide it along the locus.
- Do not reroute or remove the V loops or the ∂L leaders. Trim the tips along their own path, and let a loop yield with a gap.
- Do not change the leader dot size, the pitch or the dot family. Only the field/texture class changes.
- Do not cap packet amplitudes, add or remove rows, move the composition, or recompute Q/K/V/Z/∂L packet shapes. A2, A6, S1, S3 and S4 wait for Juan.
- Do not let the comb change its count, lens, pitch or pen while fixing its curvature.
- Do not ship the render pipeline's greedy gcode as the plate. `plate.py`'s stream-order file is the one to plot.
- Do not edit anything under `promptplot/` from the piece. The engine requests go in NOTES.
