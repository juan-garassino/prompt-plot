# Science critique — superposition r03 · machine learning (attention as superposed Gaussian bumps) · 2026-09-29
render: gallery/studio/superposition/current/pp_superposition_INTERFERENCE_FIELD_v9.png (gcode: gallery/studio/superposition/current/pp_superposition_INTERFERENCE_FIELD_v9.gcode)

Pass 1 (cold). There is no LEDGER.md, so there are no open mandates to follow up.

**Process finding:** `studio/superposition/` has **no `dossier.md` and no `encoding.md`**. That means there is no §1 math,
no §4 lies list, no §5 misconception and no §7 check numbers to verify against. The claims checked below
come from the HANDOFF pen legend and the on-sheet caption. The check numbers were derived here from
`rounds/r03/gpt2_head.npz`, the stated source. Provenance cannot be checked offline: `transformers` is not
installed and there are no GPT-2 weights cached, so "GPT-2 small L5H5" is taken on trust. The data is
internally consistent, and its pattern is the known induction signature of head 5.5.

Coordinate frame recovered from the gcode: key j at x = 50.62 + 9.25·j and query i at y = 244.38 − 9.25·i
(16 tokens; the tick positions match to 0.01 mm).

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| A = softmax(causal(QKᵀ/8)) from stored Q,K | — (no dossier) | max err vs stored A 3.5e-8; Z = AV err 1.8e-7 | — | OK |
| induction stripe: argmax A[i] for i = 8..15 | — | key i−7 (1..8), weights .87 .93 .72 .70 .98 .81 .82 .65 | eyes at cells (8,1)(9,2)(10,3)(11,4)(12,5)(13,6)(14,7)(15,8), centres within 0.1 cell | OK |
| attention sink, col 0, rows 0–7 | — | .95–1.00 | contoured column at x = 50.6, y 178.8–248 | OK |
| attention field = Σ A_ij·G(σ) | — | — | the 42 contours are isolines of Σ A_ij G(σ = 4.20 mm = 0.454 cell), CV along a contour 0.095 % | exact |
| field range | ≤ 1 (a probability) | A max 1.000 | **field max 1.173; 6 contours at levels 1.01 / 1.13 (177.9 mm of ink)** | **VIOLATED** |
| contour levels | — | — | 0.028 .056 .106 .187 .304 .46 .644 .837 1.01 1.13 (not linear) | noted |
| equal weight ⇒ equal rings | — | A(1,0) = 1.000, A(12,5) = 0.980 | 10 rings vs 8 rings (sink column inflated +17 % by vertical kernel overlap) | **VIOLATED** |
| causal knife | x + y = 295 through the diagonal cells | — | knife x + y = 299.62 (0.25 cell past the diagonal); 0 contour points overshoot | OK |
| softmax profile = row 15 | — | A15: key0 .295, key8 .652 | Σ A15,j G(4.2) × 24.0 mm/unit, rms 0.009 mm; peaks 7.09 / 15.73 mm (ratio .451 vs .452) | OK |
| profile = "section cut" of the field at y = 105.62 | — | field on the cut line ≠ row (spill from row 14) | fit of section vs profile rms 0.82 mm; field on the cut at key 7 = 0.16 → 3 contours meet the cut at x 108.6–118.5, but the profile is empty there (A15,7 = 0.03 lies under the 0.8 mm floor) | PARTIAL |
| profile mass shown | 1.0 | keys 0 + 8 = 0.947 | 5.3 % dropped silently by the 0.8 mm draw floor | minor |
| V→Z dash duty = attention | — | .295 / .652 | 1.474 / 4.998 = **0.295** (22 dashes); 3.262 / 4.999 = **0.653** (8 dashes) | exact |
| K ruler = SVD of QKᵀ (4 channels) | — | right singular vectors of the unmasked QKᵀ/8, σ = 41.4, 21.9, 17.0, 15.5 (top 4 = 91 % of energy) | blue lines inner→outer correlate \|r\| = 1.000 with v₀..v₃ | OK |
| Q ruler | — | left singular vectors u₀..u₃ | red lines inner (x 29.8)→outer correlate \|r\| = 1.000 with u₀..u₃ | OK |
| ruler amplitude ∝ channel weight | — | σ₀/σ₃ = 2.67 (√: 1.63) | **equalized:** blue p2p 4.22 / 4.78 / 4.74 / 4.60 mm; red 2.75 / 5.63 / 5.17 / 4.25 mm | **VIOLATED** |
| V chords | — | rank-3 projection of V (top-3 SVD, 78 % of V energy) | the 16 chords are rank 3; R² = 0.998 on V·Vt[:3]; chord 0 peak 0.91 mm (the sink's near-null value, true) | OK (undeclared basis) |
| Z = AV (green) | — | true z₁₅ chord = Σ A15,j chord_j | matches with rms 0.10 mm, **but drawn ×4.03 horizontal and ×3.99 vertical**; peak 14.05 mm vs the largest V chord 9.0 mm and chord 8 at 4.39 mm; true peak at V scale 3.51 mm | **VIOLATED (scale)** |
| budget | HANDOFF 6.10 m draw / 3.14 m travel / 320 cycles | — | 6102.1 mm / 3209.3 mm / 320 | OK (travel +2 %) |

## Lies list
No dossier §4 exists. These are the lies found by measurement:
| item | clean / VIOLATED (where) |
|---|---|
| probability field drawn above 1 | VIOLATED — sink column x = 50.6, y 178.8–245.5: one 1.01 contour plus five 1.13 eyes (rows 1–5). Attention cannot take these values. |
| ring count ≠ weight | VIOLATED — the sink column gets +2 rings over induction cells of the same weight (kernel overlap, σ = 0.454 cell) |
| amplified output posing at input scale | VIOLATED — Z bell (x 149–189, y 25.6–39.7) is ×4 with no mark, so the convex combination looks 1.6× taller than its tallest input and 3.2× taller than chord 8 |
| channel importance flattened | VIOLATED — Q/K rulers (x 10–31, y 258–283) are drawn at equal amplitude although σ₀ = 2.67·σ₃ |
| section cut ≠ section | PARTIAL — the profile is row A15 exactly, but 3 contours cross the cut line at key 7 where the profile shows nothing |
| decorative marks | clean — every stroke measured maps to data (contours, rulers, chords, dashes, Z, profile) |
| causal mask | clean |

## Scores
truth **7** · fidelity **6** · legibility **5** · VERDICT: **FAIL**

- truth 7: the data is real and correctly computed. Every curve is an exact function of it: contours at CV 0.1 %, dashes to 3 decimals, Z to 0.1 mm. But the "attention field" has contours at 1.01 and 1.13, and the section cut is not the drawn field's section.
- fidelity 6: three broken scales. Z is ×4 and unmarked, the ruler channels are equalized, and the kernel overlap inflates the sink by 17 %.
- legibility 5: no token names on either ruler. A stranger cannot read that the stripe is "previous occurrence → next token". The duty = attention code is unexplained, and so are the ruler channels and the V chord basis. No station labels (Q/K/V/Z) and no §5 misconception to land.

## Mandates
1. **Attention field exceeds 1.** Measured: field max 1.173 and six contours at levels 1.01 / 1.13 (177.9 mm), all in the sink column at x = 50.6, y 178.8–245.5. A = 1.000 at (1,0) gets 10 rings, while A = 0.980 at (12,5) gets 8. Expected: the field at every cell centre equals A_ij within 2 %, max ≤ 1.0, no level ≥ 1.0, and equal weights get equal ring counts. Fix it by normalizing by the kernel-overlap sum, or by narrowing to σ ≤ 0.30 cell (≈ 2.8 mm), where neighbour spill is ≤ 0.4 %. The same fix makes the y = 105.62 cut a true section (today it is 0.82 mm rms off the profile, and 3 contours meet the cut at key 7 above an empty profile).
2. **Z = AV drawn at ×4 without a scale.** Measured: the green curve (x 149.2–189.1, baseline y 25.62) is the true z₁₅ chord at ×4.03 horizontal and ×3.99 vertical. Its peak is 14.05 mm, against 9.0 mm for the largest V chord and 4.39 mm for chord 8 on the V row (y 61.62). Expected: draw it at the V chords' scale (peak 3.51 mm, width ~9 mm), or put a declared "×4" on the sheet with a 1× ghost, so the weighted sum never looks larger than what it sums.
3. **Rulers carry neither token identity nor channel weight.** Measured: 0 of 16 token labels at the K ticks (y 257.9–259.1, x = 50.62 + 9.25·j) and the Q ticks (x 35–36.2). The channel amplitudes are equal (blue p2p 4.2–4.8 mm, red 2.8–5.6 mm) although σ = 41.4 : 21.9 : 17.0 : 15.5. Expected: 16 token labels per ruler, so the i−7 stripe reads as "Every→wave, wave→that…". Scale the channel amplitude ∝ √σ (6.4 : 4.7 : 4.1 : 3.9, i.e. outer channel ≈ 0.61 of inner), and add one legend line for "dash duty = attention weight".

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | — | there is no LEDGER.md, so this is pass 1 with no open S* mandates |
