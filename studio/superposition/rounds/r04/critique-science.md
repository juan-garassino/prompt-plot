# Science critique — superposition r04 · machine learning (attention as superposed Gaussian bumps) · 2026-09-29
render: gallery/studio/superposition/current/pp_superposition_iterate_v15.png (gcode: gallery/studio/superposition/current/pp_superposition_iterate_v15.gcode, 38 120 cmds, 872 pen cycles, parsed per `; color=N`)

This is pass 1 plus pass 2 (LEDGER open).

**Process finding (S5, still open):** there is no `dossier.md` or `encoding.md`, so there are no §7 check numbers, no §4 lies list and no §5 misconception. The ledger says r04 NOTES carries the check table, but the blindness rule forbids opening NOTES. So every number below was recomputed from `rounds/r02/head.npz` (Q, K, V, A, Z, GPT-2 small L11 H8) and measured off the gcode.

Frame recovered from the gcode:
- key/value column j is at x = 36.4 + 10.8·j and query row i at y = 161.66 + 5.70·(12 − i);
- the Q curves are centred at x = 96 − 5.2·i and the K curves at x = 118 + 5.2·j;
- the V baseline is at y = 90.5, the Z baseline at y = 25.0 and the softmax baseline at y = 125.0.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed (head.npz) | measured on sheet | OK? |
|---|---|---|---|---|
| A = softmax(causal(QKᵀ/8)), Z = AV | — | max err 0.0 / 0.0 | — | OK |
| provenance: GPT-2 small L11 H8, and the sentence | — | stored check_err ≤ 2.3e-6 (can't re-run offline) | printed in the footer, sentence verbatim | OK (on trust) |
| itself·hole raw / scaled | — | 16.879 / 2.1098 (row maximum = hole) | footer "16.9/8 = 2.11" | OK |
| softmax row, 72 mm/unit | — | a₁₂ = .2558 hole … .0001 The | 12 Gaussian spikes (σ 1.15 mm) at the column x's. Peak err ≤ 0.005 mm for every token. The (0.007 mm) is correctly absent | OK |
| drops from row 12 to the spikes | — | 5 keys above 1/13 | 5 drops at x 58.0, 68.8, 112.0, 144.4, 155.2 (plot, ter, hole, transformer, watched) | OK |
| drop dash duty = a_j / a_max | — | .548 .546 .498 .416, hole 1.0 | 144.4: 3.85/7.04 = .547 · 58.0: 4.07/7.45 = .546 · 68.8: 3.27/6.55 = .499 · 155.2: 3.04/7.32 = .415 · 112.0 solid | OK |
| triangle ring rule "ring n: A·(i+1) = 1.2ⁿ" | — | r_n = s·(log₁.₂ A(i+1) − n) | all 89 closed rings fit with **s = 0.8194 mm/ring, max residual 0.014 mm**. Merged blobs keep their own-cell horizontal widths. Rings with r < 0.2 mm are dropped (floor) | OK |
| cells below uniform stay blank | — | 70 cells with lift < 1 | 119/120 cells correct. **(12,8) " while", lift 0.479, sits 0.36 mm inside ring 0 of the (11,8)/(10,8) blob** (bottom of that contour at y 161.30, row line at 161.66, x 122.8) | 1 VIOLATION |
| equal values → equal ring counts | — | (1,1) 2.00 · (7,4) 2.075 · (7,7) 2.07 | 4 · 4 · 4 | OK |
| Q/K rule "f = Σₖ (c·eₖ)Hₖ(x/σ), k<3, e₀ = q(itself)" | — | c₀ = q̂·vec. Q itself = pure Gaussian | Q itself: Gaussian a 12.923, σ 3.301, μ 33.60, rms 0.006 → **1.389 mm/unit**. Fitting normalised physicists' Hermite functions to all 30 Q/K curves gives c₀ = 1.389·(vec·q̂) within ≤ 0.04 mm on every token. e₁ and e₂ recover as orthonormal ⊥ q̂ (\|e₁\| 1.0002, \|e₂\| 0.9998, e₁·e₂ 2e-4). e₁ ≈ top PC of Q∪K ⊥ q̂ (\|cos\| 0.997) | OK (e₁, e₂, σ and the scale are not on the sheet) |
| overlap = score | — | since q_itself = \|q\|e₀, ∫f_q f_k = s²σ√π·(q·k) exactly | hole K curve c₀ 2.521 mm vs Q itself 12.923 mm → (12.923/1.389)(2.521/1.389) = 16.88 | OK |
| V rule, e₀ = ẑ | — | c₀ = v·ẑ | V at **3.006 mm/unit, σ 6.60**. c₀ matches s·v·ẑ within ≤ 0.01 mm on the long fragments of 12 tokens. think and "." are open rings (A = 0) | OK |
| Z 1× ghost | — | R(z) = \|z\|·s Gaussian | dashed Gaussian a 16.025, σ 6.597, μ 177.09, rms 0.005 | OK |
| Z at ×2.5 | — | ×2.5 on both axes | outer curve a 40.04, σ 16.50 → ×2.499 height, ×2.501 width, declared "×2.5" | OK |
| Z partial sums (caption terms) | — | c₀ = 2.5·s·(partial·ẑ): 13.376 · 18.132 · 24.622 · 30.396 · 32.933 · 40.062 | 6 green curves, c₀ 13.37 · 18.13 · 24.61 · 30.38 · 32.92 · 40.05 (≤ 0.03 mm) = hole, +transformer, +plot, +ter, +watched, +rest | OK |
| V→Z strands land ON their partial | — | — | hole→P0 gap 0.00 · transformer→P1 0.00 · plot→P2 0.00 · ter→P3 0.01 · watched→P4 0.01 · pen/drew/itself→P5 ≤ 0.01 mm | OK |
| caption ".26 hole + .14 transformer + .14 plot + .13 ter + .11 watched + .23 rest" | — | .2558/.1401/.1397/.1275/.1064, rest .2305 | as printed | OK |
| budget | 9.95 m draw · 3.58 m travel · 872 cycles · max hop 53.8 | — | 9 949.6 mm · **3 768.5 mm** · 872 · 53.8 mm | travel +5.3 % (HANDOFF understates) |

## Lies list       item | clean / VIOLATED (where)
There is no dossier §4. The items below come from the HANDOFF claims and the prior S mandates.

| item | verdict |
|---|---|
| Z is a template, not a sum (r02 lie) | **clean.** 6 partials, each exact to ≤ 0.03 mm. The full Z is a Gaussian only because e₀ = ẑ, which is stated |
| amplified output posing at input scale (r03 lie) | **clean.** ×2.5 is exact on both axes and declared, with a dashed 1× ghost at 16.03 mm |
| triangle labelled as something it doesn't draw | **clean.** The Q·Kᵀ caption is gone and the lift rule is printed. The blank (0,0) is correct under the rule (A = 1 = uniform for a 1-key row) |
| probability/lift field spilling onto cells it doesn't hold | **VIOLATED, one cell.** (12,8) " while" (A .0368 < 1/13), on the featured itself row, is enclosed by ring 0 of the (11,8)/(10,8) blob at (122.8, 161.66) |
| "ink fraction = a_j / max a" on strands | clean for all 8 strands drawn. **Partial:** 5 attended tokens (while .0368, the .0181, a .0123, black .0116, The .0001; Σ .0789) feed P5 but get no strand, and no floor is stated |
| one stated projection rule (Mohr) | clean in substance, but **incomplete.** e₁, e₂, σ and mm/unit (Q/K 1.389, V/Z 3.006) are not on the sheet, so a reader cannot reconstruct a curve |
| decorative marks posing as data | clean. Every curve, ring, spike, dash and strand measured maps to the data |
| causal mask / knife | clean. Blue strands land on the outer knife pass (e.g. key 0 at (36.4, 233.93)) and crimson strands land on their rows at x = 31 |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 9**: every channel is an exact function of the real head:
  - softmax to 0.005 mm;
  - rings to 0.014 mm;
  - Q/K/V Hermite c₀ to ≤ 0.04 mm;
  - partial sums to 0.03 mm;
  - strands to 0.01 mm.

  One cell spills: (12,8). The HANDOFF travel figure is off by 5 %.
- **fidelity 8**: every scale is linear or log-declared, and ×2.5 is marked with its ghost. It is held back by the unstated e₁/e₂/σ/scale, the 5 strandless attended tokens, and the (12,8) spill.
- **legibility 7**:
  - A scientist can falsify the sheet: the rule, the provenance and itself·hole = 2.11 are all printed, and the overlap integral is exactly ∝ q·k.
  - A stranger cannot tell which band is Q and which is K. Neither family carries a token name.
  - The two curves whose product is printed are unmarked: the itself query at x 33.6 and the hole key at x 154.4.
  - The triangle's rows and columns are unnamed, so "row 12 = itself" is invisible.
  - The only readable story starts at the V labels.
- **VERDICT: FAIL** (legibility 7 < 8)

## Mandates        1. … 2. … 3. …
1. **Token identity on Q/K and the triangle (reopens S4).**
   - Measured: 0 token labels on the crimson band (y 261–281, centres x = 96 − 5.2i) and 0 on the blue band (centres x = 118 + 5.2j). The itself query is the pure Gaussian at x 33.6 (a 12.92 mm, σ 3.30). The hole key has c₀ 2.52 mm at x 154.4. Neither is marked. There is no "itself" at the row-12 slice (y 161.66).
   - Expected (token names are allowed by A13):
     - put "itself" under the x 33.6 query curve and "hole" under the x 154.4 key curve;
     - put "itself" at the left end of the row-12 slice (x ≈ 31, y 161.66);
     - so the footer's 16.9/8 = 2.11 traces to two marked curves and one cell (12,7) = (112.0, 161.66).
2. **Cell (12,8) spill.**
   - Measured: " while", A = .0368 (lift 0.479 < 1), at (122.8, 161.66) lies 0.36 mm inside ring 0 of the (11,8)/(10,8) blob, whose outer contour bottoms at y 161.30.
   - Expected: no cell with A·(i+1) < 1 inside any ring 0. Every cell centre should read its own value within 2 % (119/120 do today). Clip the blended contours at the row mid-lines (±2.85 mm) or tighten the blend so the (11,8) ring 0 stops above y 164.5.
3. **Complete the stated rule and the strand set.**
   - Measured: the footer (y ≈ 10.5) names e₀ only. e₁ and e₂ recover as an orthonormal pair ⊥ e₀ (e₁ ≈ top PC of Q∪K ⊥ q̂, \|cos\| .997). σ (Q/K 3.30 mm, V 6.60 mm, Z 16.50 mm) and amplitude (Q/K 1.389 mm/unit, V/Z 3.006 mm/unit) are unstated. 8 V→Z strands are drawn for 13 attended tokens: while/the/a/black/The (Σ a = .0789) are in P5 with no strand.
   - Expected:
     - append "e₁,e₂ = top PCs ⊥ e₀ · σ 3.3/6.6 mm · 1.39/3.01 mm per unit" (or the true definitions) to the rule line;
     - either draw a strand for every a_j > 0 at duty a_j/.2558, or print the floor ("strands for a ≥ .04");
     - correct the HANDOFF travel from 3.58 m to 3.77 m.

## Follow-up on open mandates   id | status | evidence
| id | status | evidence |
|---|---|---|
| S1 (→A8) Z = computed sum, same rule and scale, or ×k + 1× ghost | **FIXED** | 6 partials, c₀ within 0.03 mm of 2.5·s·(partial·ẑ). ×2.499 / ×2.501 declared "×2.5". Dashed 1× ghost a 16.03 mm = 3.006·\|z\|. Strands land on their partial at ≤ 0.01 mm |
| S2 field labelled as drawn, stated scale, equal values → equal rings, centre within 2 % | **PARTIAL** | The rule is printed and the false Q·Kᵀ label is gone. Rings fit r = 0.8194(log₁.₂L − n) to 0.014 mm over 89 rings, and equal lifts get 4/4/4 rings. 119/120 cell centres are correct. (12,8) spills (mandate 2) |
| S3 rule + provenance + one checkable inner product at its cell | **PARTIAL** | Provenance and the sentence are printed. The Hermite/e₀ rule is printed and verified (c₀ ≤ 0.04 mm). itself·hole = 16.9/8 = 2.11 is correct, but it appears only in the footer: not at cell (12,7), and neither curve is marked. e₁, e₂, σ and scale are unstated (mandate 3) |
| S4 token identity / channel weight | **REOPENED, NOT FIXED** | 0 Q/K token labels. Channel weight now lives in c₀ = vec·e₀, which is exact (mandate 1) |
| S5 no dossier / encoding | **NOT FIXED** | Neither file exists, and the critic cannot read NOTES under the blindness rule |
| regressions | none | The softmax row (≤ 0.005 mm), caption, provenance and 5-drop count all held from r02 |
