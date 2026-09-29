# Synth — superposition after r04 · 2026-09-29
route: **translator**, then designer
next round: r05 · parent: **r04 (best so far, by rule)**. Art min is 6 against r03's 3, and science min is 7 against r03's 5. r04 is the first round that is best outright rather than on a tie-break

## Why translator (rule 2, first match)
- **S5 was NOT FIXED in r02, r03 and r04.** There is no `dossier.md` and no `encoding.md`. Each science critic has graded against numbers it re-derived from `head.npz`, and it may not read NOTES, so r04's check-number table cannot close S5. Only an encoding closes it.
- **A12 (shared edges) was NOT FIXED in r03 and r04.** The lead deferred it both times, so this alone would not fire the rule. It does belong in a composition sketch, though, and designers keep leaving it out.
- **A8 and A10 are PARTIAL for the third round running, and both are channel conflicts, not build bugs:**
  - A8: the true partial sums cross, because the H₁ lean cancels. The reference image is nested bells.
  - A10: science verified dash duty = a_j/a_max exactly. Art reads the dashes as debris.

  Deciding which channel carries these is the translator's job.

The encoding is **not** unworkable. Science scored r04 at 9/8/7, with every mark exact. So the translator **codifies r04's working encoding**, resolves the two channel conflicts, and writes the mm composition sketch. It does not replace the thesis.

## The instruction
**Translator:** write `studio/superposition/encoding.md` from r04. There is no dossier, so derive it from r04's `piece.py`, its HANDOFF and the two r04 critiques, and say so in the file. Keep what r04 proved:
- GPT-2 small L11H8, query " itself", `rounds/r02/head.npz`;
- the Hermite rule, with Q/K e₀ = q(itself) and V/Z e₀ = ẑ;
- the lift rings at A·(i+1) = 1.2ⁿ with 0.82 mm pitch;
- softmax at 72 mm per unit;
- Z at a declared ×k with a 1× ghost;
- Mohr, *Cubic Limit* / hypercube works, as the lineage: the rule is the image.

Then make four decisions the designer cannot make.

**(a) Z nesting.** The six partials have monotone ẑ-components: c₀ = 13.37 < 18.13 < 24.61 < 30.38 < 32.92 < 40.05 mm at ×2.5. Choose one of two options and state it as a channel rule:
- draw the nest as ẑ-component bells that share one centre and nest by construction (declared on the sheet, outermost still exactly R(z)), and carry the lean somewhere smaller and true; or
- keep the full partials and make the crossing the intended event.

Either way, every green curve starts and ends ON the baseline, with no Occupancy pause inside the nest. Z becomes the answer's mass, not the weakest element; a larger declared ×k is allowed.

**(b) The strand weight channel.** Pick one of duty, pass count or lane count. It must read as continuous lines from V into Z, with no fragment under 3 mm between V and Z. Add a stated floor for a_j (or a strand for every a_j > 0).

**(c) An A4 portrait mm sketch that makes the triangle dominant again.** The triangle is ≥ 110 mm tall and keeps its base at ≥ 0.85 of the width. Its interior out-inks the red elbow bundle at a 6 mm blur. Take the height from the dashed V→Z stair-step zone and the red gutter's fan-out, not from Z. Use one left edge (x = the triangle leg) for every baseline, `Z = AV` and the footer, plus a Q|K gutter of ≥ 6 mm.

**(d) Token identity and the rule, as a legible sheet element:**
- mark " itself" on its Q curve, "hole" on its K curve, "itself" on row 12, and a mark at cell (12,7);
- state e₁, e₂, σ and mm per unit;
- keep the footer cap height ≥ 2.2 mm, or cut the footer.

Write §11 acceptance checks for every mandate below. Write §6 as a Leo plate job, with minutes per layer and the stated order.

**Designer (r05):** fork r04's `piece.py` and build exactly what the encoding says.

## Mandates to close
1. **S5 (rule 2 trigger): `encoding.md` exists, and both critics grade r05 against it.** It needs §4 channel table, §5 mm sketch, §6 pen/plot budget, §7 check numbers (reuse r04's NOTES table: softmax spikes, ring radii, K bell heights, partial c₀, landing points) and §11 acceptance checks. Test: the science critic's check-number table has a filled "dossier/encoding" column.
2. **A8 + A10 + S6: superposition is visible, and it is the answer.**
   - 6 green curves (or the encoding's declared ẑ-nest), one per caption term.
   - Zero green endpoints above the baseline.
   - Either no two sums crossing, or crossings the encoding declares.
   - Every V→Z strand continuous and ending ON its curve (gap ≤ 0.01 mm, as r04).
   - Zero gold fragments < 3 mm between the V baseline and Z.
   - The strand floor printed or all 13 strands drawn.
   - Z's blurred ink is no longer the weakest station.
3. **A4 (regressed; preserve r03's dominance) + A9 + S2: the field commands the sheet and stays true.**
   - Triangle ≥ 110 mm tall.
   - Blur test: interior ink > red bundle ink (r04: 10.8 vs 15.2).
   - Outermost red elbow at x ≥ 20.
   - No single-ring circles ≤ 1.5 mm across.
   - The '.'→'.' corner eye no longer chopped: a larger row pitch lets it fit, or it clips on the knife only.
   - Cell (12,8) is outside every ring 0, so 120/120 cell centres read within 2 %.
   - Still no level above the encoded maximum, and equal lifts still get equal rings.
4. **S4 + S3 + A16: the sheet can be read and falsified by a stranger.**
   - Q/K token identity: at minimum " itself" and "hole" named on their curves, "itself" on row 12, and a mark at cell (12,7).
   - The complete projection rule (e₁, e₂, σ 3.3 / 6.6 / 16.5 mm, 1.389 / 3.006 mm per unit, or r05's values).
   - Footer cap height ≥ 2.2 mm, or cut to `itself·hole = 2.11`.
   - Every V token label keeps ≥ 1.5 mm of paper from gold ink.
   - The Q/K families tall enough (r02-scale) that the over/under breaks read as weaving, not as broken lines.
5. **A12 + A15 + A3: one grid, one bold knife, and a lower half that leans with the data.**
   - The V, spike and Z baselines, `Z = AV` and the footer share the triangle leg's x.
   - The red bundle sits ≥ 6 mm inside the margin, and the K waves end by x 194.
   - The knife is ONE bold rule: passes ≤ 0.3 mm apart, or a stated wide-nib pen.
   - V/Z no longer both centred on x ≈ 105.

Deferred: C6 and A1 (both follow from 2 and 3; the art critic re-runs the Mohr hang test on r05).

## Preserve (r04, measured by the critics; do not regress)
- **C1 rhythm:** the Q|K pair on top → triangle → softmax spikes → V (the widest band, ≥ 0.85 of the width) → Z (narrower) → footer, read top to bottom.
- **Science exactness:**
  - softmax spikes ≤ 0.005 mm at 72 mm per unit (y ≈ 125, under the key columns);
  - ring rule r = 0.8194·(log₁.₂ L − n), fitted to 0.014 mm;
  - Hermite c₀ ≤ 0.04 mm on all 30 Q/K curves;
  - the overlap identity ∫f_itself·f_hole ∝ q·k;
  - partial sums ≤ 0.03 mm, with ×2.5 declared plus the dashed 1× ghost;
  - strands landing ≤ 0.01 mm;
  - the caption ".26 hole + .14 transformer + .14 plot + .13 ter + .11 watched + .23 rest".
- **Field geometry:** right triangle with the apex top-left and the leg at x 30. The knife runs from the true apex to the base corner. The masked future is paper. Eyes are conical, with a constant 0.82 mm pitch and no ghost arcs.
- **Connectors:** Q strands land on their rows at the leg, and K strands drop down their own column onto the knife. Every key column is one vertical from the K staircase to the V curve.
- **Plot discipline:**
  - 6 layers, light → dark: goldenrod → dodgerblue → crimson → forestgreen → black → fine black type. Each is entered once.
  - Max in-layer hop 53.8 mm on the emitted gcode (`_order_layer` simulates the pipeline pass).
  - 872 cycles, ~60 min, no dotted runs.
  - Gate r04: bounds X 0–199.3, Y 0–282.3 on A4; layers of 106/73/56/23/156/458 strokes.
- **HANDOFF lines:** `lineage:` (Mohr) and `declared: flat` with its reason. No station captions (A13).

## Do not
- Do not make eyes bigger with gentler cones. Below 0.232 nat/mm they put false rings on neighbours, e.g. (11,8) → (12,8). Grow the row pitch (a taller triangle) instead.
- Do not buy Z mass with dots, stipple or a template curve. No round-number μ/σ.
- Do not let the engine's Occupancy pause-resume act inside the Z nest. Curve ends in mid-air were the art critic's top complaint.
- Do not let strand weight become debris. No dash shorter than 3 mm anywhere between V and Z.
- Do not add captions (`Q·Kᵀ`, `softmax`, `1/13`, ticks) to buy legibility. Token names, scale marks and the rule are the only type allowed.
- Do not grow the type layer. It is already 458 of 872 cycles. New token labels are paid for by cutting footer words.
- Do not switch head, data or lineage. Do not import r03's rulers or its Riley row-line family.
- Do not report budget figures from the design model. Measure travel on the emitted gcode (r04 understated it: 3.58 m against 3.77 m).

## Plot budget for r05 (curator note: Leo, batched plate jobs, DESIGN_RUBRIC § PLOTTABLE)
- **No pen cap.** Every meaning keeps its pen. A wide-nib knife pen is allowed as a 7th stated layer if the encoding chooses it.
- **Each pen is one clean layer, entered once, in a stated order.** Strokes are spatially ordered for batching, and no in-layer hop exceeds 60 mm on the emitted gcode. No stroke is so long it cannot be a batch boundary.
- **NOTES states minutes per layer and in total**, using the Leo model: F500 draw, 2000 mm/min travel, 2 s per cycle, 90 s per swap.
- **Ceiling: ≤ 1 000 pen cycles and ≤ 75 min including swaps.** That compares with r01's 5 573 cycles and 206 min. A long session is allowed; dot-lifts are not.

## Fabrication gate
Not run as a pass gate: both critics FAIL. Stats on r04 are recorded for the curator:
- `preview --stats --score`: grade A, 872 lifts, draw 9 949.6 mm, travel 3 768.5 mm (ratio 2.64), bounds X 0–199.3 · Y 0–282.3 (clean on A4). The longest travel is 248.8 mm, a between-layer entry or park move.
- `plot layer --list`: 6 layers, 106 / 73 / 56 / 23 / 156 / 458 strokes, each entered once.
- No file under `promptplot/` changed in this piece's rounds, so the regression suite is not required.

## Flavours kept on disk
- r01 `faithful`: the reference recreation, Juan's pick, the nested-bell image.
- r03 `interference`: the dominant induction-head field.
- r04 is the lineage going forward.
