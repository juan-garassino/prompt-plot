# Synth — orrery after r02 + r03 (parallel theses) · 2026-09-29
route: designer
next round: r04 · parent: r03 (best so far: art 6.29/5 · sci 7/8/7, against r02's 4.86/3 · 8/6/7; both FAIL). There is one MERGE element and it is data only. Read tokens, ids and the attention row from `studio/orrery/rounds/r02/gpt2_head.npz`: same head L4H3, same sentence, BPE ids verified, numpy forward matched to torch at ≤ 2.3e-6. Take nothing visual from r02.

Fabrication gate: not run, because neither critic passed. For the record, layer lists were read off the gcode. r03 has 3 layers (117 blue / 36 crimson / 569 black strokes). r02 has 5 layers (57 / 33 / 31 / 6 / 533). Nothing under `promptplot/` changed in these rounds.

## The instruction
Fork r03 and **make the miss take space inside a disc drawn whole**. Budget the radial layout; drop the fixed 7.5 mm step. Every non-resonant key gets a band whose envelope width is one declared, monotone function of its shortfall δ. The near-locks (`The`, `watched`, `hole`, `pen`) become tight cables. The far misses (`drew`, `a`) open into annuli: for example, let each turn's guiding radius drift outward by c·(δ − δ_The), so their turns spread instead of stacking. `transformer` is the one band with no width. The radius the tight bands free up stays as bare paper between bands, so the disc gets an uneven rhythm with quiet rings in it, not a uniform rope texture. Size and place the disc so every orbit lies inside the margins, the closing orbit above all. The tension the left crop used to supply now comes from three things: the uneven band rhythm, the sun sitting off the page's centre vertical and high on the sheet, and the type block hanging low-right off the spine. Before drawing, do the arithmetic and write it in NOTES:
- A purely proportional width map tops out at δ_max/δ_min = 2.98:1, so anchor it affinely at the tightest key.
- Four strands at the 0.8 mm floor need about 2.4 mm.
- An off-centre disc of outer Ø ≤ ~175 mm leaves about 75 mm of radius for 13 bands plus gaps.
- If that does not fit, choose one of two fixes and state which: draw **three turns per orbit** (turns·δ_max < 1 then allows δ_max up to about 0.3, and it cuts about 25 % of the blue ink), or centre the disc horizontally (about 83 mm of radius) and carry the asymmetry vertically.

Finally, cut the label slot as two chord lines either side of the token column and make every orbit start and end on those chords. That one move gives every word its 2 mm halo, removes the crumbs, and lets nearest-neighbour ordering walk ring to ring along the slot, so the blue layer streams in short hops. The token rows now fall at their rings' uneven radii. Keep row pitch ≥ cap height + 1.5 mm.

## Mandates to close
1. **S5 + A8, the composition idea.** The closing `transformer` orbit is drawn 100 % outside the label slot (r03: 69.2 %), and every orbit is ≥ 95 % drawn. Band envelope = one stated affine function of δ, anchored at the tightest key. Tests: widest/narrowest envelope ≥ 3:1 on the 3 o'clock ray, ≥ 2 inter-band gaps ≥ 4 mm, and r03's "parallel < 0.8 mm" share ≤ 10 % on every band (r03: `The` 55 %). The lead amended the critic's "≤ 2 mm tight cable": the house floor wins.
2. **A10 + A11 + A9, craft, batching and labels.** Measure these on the EMITTED gcode, after the pipeline's colour reorder:
   - No in-layer travel > 60 mm (r03: 23 > 60 mm, max 164 mm, blue; r02: 184/187 mm, footer underlines).
   - Zero blue ink within 2 mm of any glyph (r03: 0.72–0.87 mm).
   - Zero blue strokes < 8 mm (r03: 32).
   - The sun spiral at ≥ 0.8 mm pitch and Ø ≥ 18 mm (r03: Ø10 at 0.47 mm).
   - The closing orbit as 3 passes ≥ 0.3 mm apart (r03: 4 at 0.25 mm), captioned as drawn heavy, not as data.
   A10 and A11 failed in both r02 and r03. A third failure routes to the translator.
3. **S4, the divisor.** turns·δ_max < 1 strictly, so no non-argmax orbit closes (r03: 18.84 = 4·4.7097 makes `drew` close exactly). With 4 turns use 23.55 (= 5 × the widest gap, so 4δ_max = 0.80). With 3 turns, derive and state the analogue. Print what the constant is on the sheet, so it no longer reads as 6π, and make the caption's "only if" true as written.
4. **S6, disclosure.** In the caption block, state that this is the strongest of 144 heads for itself→transformer (0.557; next 0.416; head mean 0.053), and that most heads (106/144) park on `The`, the position-0 attention sink. Mark `The` as the sink at its row. Reword the crimson question so it asks where *this head* looks from `itself`, not what the word refers to.
5. **A12, declarations** (failed twice). HANDOFF carries `canon:` (r03 NOTES already said RADIAL DATA-VIZ) and `flat: declared — <reason>` lines next to `lineage:`. Also close **S8** in passing: take the tokens from r02's npz and delete the "inferred" note.

Deferred: A14 (lower-left quadrant). S5 forces the disc back inside the frame, so the quiet zones will move. The art critic re-judges them in r04. S7 (no `encoding.md`/`dossier.md`): r04 NOTES must carry a check-number table (row, δ per key, turns·δ, band widths, % drawn per orbit). If rule 2 fires, the translator writes `encoding.md`. C1 (argued): three pens by meaning, flagged for Juan's vote against r02. Add a 4th pen only with a stated meaning.

## Preserve
- **The one closing orbit** as the plate's only heavy line, and the riddle it answers: the question asked in crimson, the answer given by geometry (`transformer`, .557). Art calls it the plate's twist; science finds every δ within 0.003.
- **The crimson spine and token column** on the sun's vertical: weights flush-right, tokens flush-left, the sentence read top to bottom. Title and caption flush-left on the word column (r03, x ≈ 72).
- **Sentence order = ring order**: `The` innermost, `itself` outermost.
- **The Bertrand rosette orbit law** (v9 onward): r = R + A·cos(κ(θ − θ0)), with κ = n + δ.
- **Constant amplitude A carries no data** (science: "no fake channel"). If band width becomes a δ channel, it must be the same δ, declared on the sheet.
- **Zero dotted runs; three pens, one clean layer each, light → dark** (blue keys → crimson query → black type). Plot budget table per layer in NOTES, as r03 wrote it.
- **The display-weight title** `RESONANT ORBITS`, which art found to be improved vs v6/r02.
- **Seed invariance**: byte-identical gcode across seeds 3/7/11.

## Do not
- Do not crop any orbit at the frame. The crop was r03's best art move, and it broke the science thesis (an open C cannot "close").
- Do not let the braid of a tight cable fall under 0.8 mm to make it look tight. Tight means a narrow envelope with strands that cross at steep angles, not stacked hairlines.
- Do not trust the authored stroke order. `reorder_by_color` is greedy nearest-neighbour and re-scrambled r03's ring-by-ring order. Make the geometry itself NN-friendly: every orbit's endpoints sit on the slot chords, and adjacent rings end next to each other. Then measure the emitted gcode.
- Do not bring back V, Z, satellites, stars, moons or corner marks. Do not add a pen without a stated meaning.
- Do not leave a magic constant or a false "only if" in the caption.
- Do not ship HANDOFF without `canon:`, `flat:` and `lineage:` lines.
