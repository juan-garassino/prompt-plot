# Science critique — superposition r02 · machine learning (attention as superposed Gaussian bumps) · 2026-09-29
render: gallery/studio/superposition/current/pp_superposition_SUPERPOSITION-COMPUTED_v15.png (gcode alongside, 22 561 cmds, 1 123 pen cycles, parsed per `; color=N`)

**Process finding:** `studio/superposition/` has **no `dossier.md`, no `encoding.md`, and no `LEDGER.md`**. So there are no §7 check numbers, no §4 lies list, no §3–4 mapping, and no §5 misconception to grade against. Everything below was recomputed from `rounds/r02/head.npz` (Q, K, V, A, Z, tokens, GPT-2 small L11 H8) and measured off the gcode. The lies list is built from the HANDOFF claims and the Weak list in DESCRIPTION.md.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed (head.npz) | measured on sheet | OK? |
|---|---|---|---|---|
| A = softmax(QKᵀ/√64 + causal mask) | — | max err vs stored A = 0.0 | — | OK (internal) |
| Z = A·V | — | max err vs stored Z = 0.0; ‖Z_itself‖ = 5.33 | — | OK (internal) |
| GPT-2 provenance | — | stored check_err 4e-7…2e-6; can't re-run (no `transformers` in .venv) | not stated on sheet | UNVERIFIED |
| row " itself" (i=12) weights: hole .2558 · transformer .1401 · plot .1397 · ter .1275 · watched .1064 · pen .0563 · itself .0504 · drew .0449 · while .0368 · the .0181 · a .0123 · black .0116 · The .0001 | — | yes | softmax spikes above baseline y=113.0: 18.39 · 10.07 · 10.04 · 9.16 · 7.65 · 4.05 · 3.62 · 3.23 · 2.65 · 1.30 · 0.88 · 0.83 · none (mm) → **72.0 mm per unit, linear, every spike within 0.02 mm** | OK |
| uniform level 1/13 = .0769 | — | yes | dashed line at 118.54 = 5.54 mm = 72/13 | OK |
| number of weights above uniform | — | 5 | 5 spike markers + 5 droplines from the slice (x 68.2, 77.4, 114.2, 141.8, 151.0) | OK |
| footer caption ".26 hole + .14 transformer + .14 plot + .13 ter + .11 watched + .23 rest" | — | .256/.140/.140/.128/.106, rest .2305 | as printed (sum shows 1.01 from rounding) | OK |
| slice row → softmax ticks | — | row 12, 13 cells | cells x = 49.8 + 9.2 j, y 157.84; softmax ticks at the same 13 x | OK |
| Q→row / K→column strands | — | 15 rows at y = 225.05 − 5.6 i | crimson lands on the left edge and blue on the right edge at exactly those 15 heights; the solid "itself" strand goes from tick x 36.2 to row 12 | OK |
| pyramid mark rule | — | fits **ln(A_ij·(i+1)) at one ring per ×1.2 (0.182 nat), ring pitch 0.96 mm** | (14,14) A=.537 → 11 rings (r 1.2–10.7 mm); (1,1) A=1.0 → 3 rings (r 3.24); (12,2) → 3; (3,3) → 1; **apex (0,0) A=1.0 → blank** | consistent but UNDECLARED, and labelled "Q•Kᵀ" |
| Z (green) outer curve | — | should be the rule applied to Z = Σ a_j V_j | **exact Gaussian: amp 28.03, μ = 105.00, σ = 12.00 mm, rms residual 0.004 mm over 286 pts** | NOT A SUM |
| Z partial sums | — | 5 named terms + rest = 6 partials | **7** nested green curves, peaks 11.90 / 14.38 / 17.53 / 19.91 / 22.97 / 25.34 / 28.03; inner ones not Gaussian (rms 0.40 mm) and centres drift 99.98 → 105.0 | MISMATCH |
| peak heights vs ‖partial‖/‖Z‖ | — | .39 .49 .63 .77 .83 … 1.0 | .43 .51 .63 .71 .82 .90 1.0 | no clean match |
| V bump heights | — | ‖V_The‖ = 58.0, which is 7× any other token (5.0–8.2) | "The" bump is 9.1 mm, hole is 20.3 mm | rule unknown; not a norm |
| budget (HANDOFF) 6.78 m draw · 5.22 m travel · 1 123 cycles | — | — | 6 784.2 mm draw · 5 278.9 mm travel · 1 123 cycles | travel is off by 57 mm (minor) |

## Lies list       item | clean / VIOLATED (where)
| item | verdict |
|---|---|
| the softmax row is not computed from Q, K (the r01 lie) | **clean**: it is exact and linear, 72 mm per unit |
| the caption is not the drawn numbers | **clean** |
| "the green bell is the sum of the ochre curves above it" (DESCRIPTION next-version 1, which is this round's brief) | **VIOLATED.** The outermost green curve (x 73.7–136.3, y 23–51) is a template Gaussian with round-number parameters (μ 105.00, σ 12.00). The ochre V curves carry negative lobes (down to −4.7 mm below the V baseline at x 132–135) and σ from 1.8 to 5.5 mm, so no weighted sum of them yields an exact Gaussian. The final curve is also not the continuation of the six non-Gaussian partials inside it. |
| the black triangle shows what its label says (Q•Kᵀ) | **VIOLATED.** It shows row-normalised log-lift ln(A·n): the per-row softmax shift is removed, 1/√d is applied, and below-uniform scores are invisible. As a result the largest mass on the triangle, cell (14,14) with 11 rings at A = .537, outranks cell (1,1) (3 rings, A = 1.0), and the certain cell (0,0) at A = 1.0 is blank paper at (105, 225). |
| decorative marks posing as data | **VIOLATED (partly).** The Q "itself" curve is an exact Gaussian (σ 3.30, μ = tick 36.20, rms 0.010), and so is the Z bell. Nothing on the sheet states what a bump's height, width or position means. |
| "one stated projection rule" (HANDOFF lineage) | **VIOLATED.** No rule is stated anywhere on the sheet. The only text is the sentence, Q/K/V, "itself", Q•Kᵀ, 1/13, softmax, five token names, Z = AV and the caption. |
| Q/K ordering | clean but unexplained: Q runs reversed (token 0 at x 95.0, token 14 at x 26.4) and K runs forward (token 0 at x 115). It reads as the r01 mirror, not as data order. |
| bounds / paper | clean: everything sits inside 10–200 × 10–287. The ochre V tail touches the margin exactly at x = 10.0. |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 6**: The data is real and internally exact, and the softmax row and caption are true to 0.02 mm. But the Z bell is a template, and the triangle's label names a different quantity from the one drawn.
- **fidelity 5**: Only one channel (softmax height) carries a stated, linear scale. The triangle uses an undeclared log scale with a blank apex. The Q/K/V bump shapes have no recoverable rule. The Z shape is decorative.
- **legibility 6**: A stranger can follow the pipeline Q,K → triangle → softmax → V → Z, and "5 of 13 above uniform" lands. A scientist can't falsify the curves: no rule, no model/layer/head, no scale on the triangle. The "superposition" (Z as a visible sum) is asserted, not shown.
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **Z bell must be the computed sum.** Measured: the outer green curve (y 23–51, x 73.7–136.3) is an exact Gaussian with amp 28.03 mm, μ 105.00, σ 12.00 (rms 0.004 mm). There are 7 nested curves, but the caption has 6 terms. Expected: every green curve is Σ_{top-m} a_j·R(V_j) under the same rule R that draws the ochre V curves, re-centred at x 105. The last partial should equal R(Z_itself), with the lobes that implies. There should be exactly one curve per caption term (hole, +transformer, +plot, +ter, +watched, +rest = 6). Otherwise delete the partial-sum claim.
2. **The triangle's label and scale.** Measured: the marks encode ln(A_ij·(i+1)) at one ring per ×1.2. Cell (14,14) at A = .537 gets 11 rings (r to 10.7 mm, clipped by the base at y 141.3 and by the right edge). Cell (1,1) at A = 1.0 gets 3 rings. Cell (0,0) at A = 1.0 is blank at (105, 225). Expected, one of two options:
   - print the rule inside the triangle near "Q•Kᵀ" (y ≈ 196), e.g. "each ring = ×1.2 above uniform 1/(i+1)", and relabel it log-softmax/lift;
   - or encode A itself, so the two A = 1.0 cells are the largest marks.
   In either case, keep the (14,14) rings inside the frame.
3. **State the projection rule and the provenance, and make one inner product checkable.** Measured: the sheet has no rule, no "GPT-2 small · layer 11 · head 8", and no reason why Q is reversed. The Q "itself" curve is a bare Gaussian (σ 3.30 at x 36.20). Expected: a footer line (y ≈ 13–18) naming the rule, e.g. the Hermite basis if that is the rule, plus the model/layer/head. Add one readout that ties the curves to the triangle: itself·hole raw QK = 16.9 (scaled 2.11), the row's maximum score, drawn at its cell (12,7) = (114.2, 157.8), so ∫f_q·f_k can be checked against it.

## Follow-up on open mandates   id | status | evidence
No `studio/superposition/LEDGER.md` exists, so there are no open S* mandates to track. This was pass 1 only.
