# Science critique — resonance-backprop r04 · machine learning (attention fwd+bwd as wave interference) · 2026-09-29
render: gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3.png — measured on the plate gcode gallery/studio/res_backprop/current/pp_res_backprop_iterate_v3_plate.gcode (94 702 cmds, 5 652 pen-down strokes: pen0 769 · pen1 839 · pen2 532 · pen3 832 · pen4 2 680). Parent geometry cross-checked against gallery/studio/res_backprop/current/pp_res_backprop_v8.gcode (r01).

**Dossier finding (S0, still open):** there is no `dossier.md` and no `encoding.md`, so there are no §7 check numbers, no §4 lies list and no §5 misconception. The claim set below comes from four places:
- the sheet's own captions (`A = softmax(QKᵀ/√d_k)`, `Z = AV`, ∂L/∂Z → ∂L/∂A → ∂L/∂Q, ∂L/∂K, ∂L/∂V);
- the HANDOFF pen key;
- DESCRIPTION § science: crest loci r = m·L, d = 59·L, L ≈ 1.04 mm, the comb described as "a real crest-crossing structure";
- textbook single-head attention backprop: ∂L/∂V_j = a_j·∂L/∂Z; ∂L/∂S = A⊙(∂L/∂A − A·∂L/∂A); ∂L/∂K_j = ∂L/∂S_j·q/√d_k.

How rows were measured: every packet row was pulled out of the gcode as y(x) about its own axis. Cross-block checks use each block's packet extent as the dimension axis, because the sheet gives no shared one. Within-block checks do not depend on that choice.

## Check numbers
| quantity | dossier / claim | recomputed / expected | measured on sheet | OK? |
|---|---|---|---|---|
| source centres | — | on one axis, symmetric | S₁ (74.090, 192.682) · S₂ (135.561, 192.682); midpoint 104.826 | OK |
| L (crest pitch) | ≈ 1.04 mm (DESCRIPTION) | — | ring 9 radius 9.377 → L = 1.04189 mm | OK |
| d / L | 59 | 61.471 / 1.04189 = 58.9996 | 59.000 | OK |
| bullseye rings m = 1…9, both sources | r = m·L | 1.042 … 9.377 mm | all 18 closed rings on m·L within 0.005 mm. Identical to v8 | OK |
| comb (black, x 88.5–121.0, y ±6.56 mm) | two-source crest structure | standing-wave crests of cos kr₁/√r₁ + cos kr₂/√r₂ are hyperbolae r₁ − r₂ = const, symmetric about x = 104.83 | 64 arcs, **all S₁ circles** m = 14…45 (two per m, split at the axis), **zero S₂ arcs**. They match the crest positions on the axis only. At the lens edge they sit 0.66 L off the two-source crest line on both halves (m 25–34: 0.66–0.68 L). Every arc bows toward S₁. Identical in v8, so this is inherited | NO |
| tonal field dots on crest circles | crest loci | chance of landing within ±0.03 mm of a crest ≈ 6 % per family | 1 851 black dots in the hero box: 787 on S₁ circles, 589 on S₂ circles (m 10–92), 76 on both | OK (on-locus) |
| where the field's crest fragments break | an interference field would keep them where the other wave agrees | constructive share ≫ 0.5 | share with cos(k·r_other) > 0: 0.494 (S₁ dots), 0.460 (S₂ dots); mean cos −0.045 / −0.049. The break points are random with respect to interference | decorative |
| three dotted halo ellipses | "tonal field" | a two-source locus would be confocal: r₁ + r₂ = const, b = √(a² − 30.74²) | a/b = 66.1/16.7, 76.9/19.7, 93.0/22.7 mm (aspect 3.9–4.1). r₁ + r₂ spans 69–130, 72–141 and 83–142 mm along each ellipse. Confocal b would be 58.5 / 70.5 / 87.8 mm | not a locus (decorative) |
| A peaks (y-base 150.94) | softmax: 5 positive entries summing to 1 | positive ✓ | x 73.89 / 89.97 / 104.83 / 119.31 / 135.39; heights 4.54 / 9.61 / 10.84 / 10.48 / 5.94 mm → shares 0.110 / 0.232 / 0.262 / 0.253 / 0.143 (areas 0.112 / 0.231 / 0.251 / 0.252 / 0.153) | form OK |
| A from anything drawn | A = softmax(QKᵀ/√d_k) | — | The hero is exactly symmetric, yet A is not: 0.110 vs 0.143 and 0.232 vs 0.253. On-axis two-source intensity (1/√r₁ + 1/√r₂)² is 0.159 at x 89.98 and 0.130 at the midpoint, the opposite ordering to A. Softmax of the drawn Q·K cosines does not reproduce it for any query row (best-matching row 3 gives 0.18 / 0.28 / 0.20 / 0.18 / 0.15) | UNVERIFIABLE |
| token count: K rows = V rows = A entries | n keys = n values = len(a) | 5 = 5 = 5 | K **5** (y 241.06 … 210.14) · V **4** (y 154.09, 148.32, 142.74, 137.15) · A **5** peaks | NO |
| gradient shapes | ∂L/∂X has the shape of X | ∂L/∂K 5 rows · ∂L/∂V = V rows · ∂L/∂Q = query rows | ∂L/∂Q **3** (Q has 5) · ∂L/∂K **3** (K has 5) · ∂L/∂V **2** (V has 4) | NO |
| shared dimension axis | same-space vectors drawn at the same width | Q = K = ∂L/∂Q = ∂L/∂K; V = Z = ∂L/∂Z = ∂L/∂V | packet extents: Q 44.0 · K 43.3 · ∂L/∂Q 30.5 · ∂L/∂K 32.8 · V 29.6 · Z 48.9 · ∂L/∂Z 31.4 · ∂L/∂V 23.2 mm | NO |
| Z = AV, amplitude bound | convex mix: \|Z\| ≤ max\|V_j\| | ≤ 4.40 mm | Z amplitude 12.10 mm = 2.75× the largest V (V: 4.40 / 3.79 / 4.15 / 3.77) | NO |
| Z = AV, shape | Z = Σ a_j V_j | residual ≈ 0 | best non-negative fit of Z on the 4 V rows: residual 94 %. Drawn A·V vs Z corr −0.50 (A₁–₄) / −0.14 (A₂–₅) | NO |
| ∂L/∂V_j = a_j·∂L/∂Z | rows are positive multiples of ∂L/∂Z, gain = a_j ≤ 0.262 | corr +1.00; gain ≤ 0.262 | corr with ∂L/∂Z +0.78 / −0.39; the two rows correlate −0.58 with each other. Amplitude gain 3.70 / 8.88 = 0.417 and 4.13 / 8.88 = 0.465 | NO |
| ∂L/∂A (y-base 49.5) | index-aligned with A | peaks under A's x | x 85.77 / 96.41 / 104.83 / 113.25 / 124.35 (A: 73.89 … 135.39), offsets +11.9 / +6.4 / 0 / −6.1 / −11.0 mm. Heights 10.11 / 8.37 / 9.78 / 8.36 / 10.45 mm, all positive and within ±11 % | NO (alignment) |
| ∂L/∂S implied by the sheet's own A and ∂L/∂A | A⊙(g − A·g) | [+0.10, −0.20, +0.15, −0.22, +0.18] mm-equivalent, Σ = 0; max 2.1 % of ∂L/∂A | ∂L/∂Q / ∂L/∂K are drawn at 3.78–5.14 mm amplitude, 76–100 % of Q / K (4.94–6.83) and above ∂L/∂V. The rows show no alternating sign | NO |
| pen key (HANDOFF) | 0 V · 1 K · 2 Z · 3 Q · 4 black | — | gold = V + ∂L/∂V · blue = K + ∂L/∂K · green = Z + ∂L/∂Z · crimson = Q + ∂L/∂Q · black = rest; order 0→1→2→3→4, each entered once | OK |
| budget (HANDOFF) | 5 652 cycles · 14.11 m · 11.69 m · 230 min | PLOT_JOBS model: 28.2 + 5.8 + 188.4 + 6.0 = 228.5 min, plus re-zero ≈ 230 | 5 652 · 14.112 m · 11.692 m | OK |
| sheet bounds (A4 210 × 297) | inside the margin | — | x 10.17–200.00, y 29.05–267.95 | OK |
| dot mark (J1, info) | one round dot, pitch 0.9–1.1 mm | — | every dot is a 0.30 mm closed circle; nearest-neighbour pitch median 0.99–1.00 mm on all pens; 1st percentile 0.66–0.76 mm (converging paths); 0 coincident | OK |

## Lies list  (no dossier §4; derived from captions + DESCRIPTION)
| item | status |
|---|---|
| Bullseyes as crest circles r = m·L, d = 59 L | clean (exact to 0.005 mm) |
| Comb as "crest-crossing / interference" structure (x 88.5–121.0, y 186.1–199.2) | **VIOLATED (inherited from r01).** It is one source's rings (S₁ m 14–45) with zero S₂ arcs. It is right on the axis and 0.66 L off the two-source crests at ±6.5 mm. It bows toward Q across the whole lens on an otherwise mirror-symmetric plate |
| Dotted field as interference tone | clean as locus: 1 376 dots are on crest circles. **Decorative** as tone: the fragments break at random phase (constructive share 0.49 / 0.46). The 3 halo ellipses (aspect ≈ 4) are not confocal and not a field locus. J2 keeps them; they must not be captioned as data |
| `A = softmax(QKᵀ/√d_k)` (y 150–166) | **UNVERIFIABLE.** Nothing drawn produces it. A symmetric field gives an asymmetric A, and axis intensity ranks the other way |
| `Z = AV` (y 115–140) | **VIOLATED.** 4 values for 5 weights. \|Z\| = 2.75× the convex bound. NNLS residual 94 % |
| ∂L/∂V (x 160–184, y 82–96) | **VIOLATED.** Not positive multiples of ∂L/∂Z (corr +0.78 / −0.39), gain 0.42–0.47 > max a_j 0.262, 2 rows for 4 values |
| ∂L/∂Q, ∂L/∂K shape | **VIOLATED.** 3 rows each for 5-row Q and K |
| ∂L/∂A → ∂L/∂Q, ∂L/∂K magnitude | **VIOLATED.** The sheet's own near-uniform ∂L/∂A cancels through the softmax (∂L/∂S ≤ 2.1 % of it), yet the gradient packets are drawn near full size |
| Arrow direction on the ∂L/∂Z → ∂L/∂V edge (y 85.8) | **VIOLATED (minor).** Opposing heads: ▷ at x 139–141 and ◁ at x 152.5–154 |
| Rail "backward pass ↑" (x 13, y 45–112) | ambiguous. The internal arrows run down and out to ∂L/∂Q / ∂L/∂K, while the rail points up. It is defensible as "back toward Q, K at the top", but that is not stated |

## Scores
- truth: **4**. The wave physics that is drawn is exact: d = 59.000 L, rings m·L to 5 µm, 1 376 field dots on crest circles. But the attention algebra the captions assert does not hold anywhere it can be measured:
  - 5 keys against 4 values;
  - Z = 2.75× the convex bound of the V's;
  - ∂L/∂V is not a_j·∂L/∂Z;
  - three gradient blocks have the wrong row count;
  - the gradient into Q and K is drawn large when the sheet's own softmax Jacobian makes it ≈ 2 %.

  The hero comb, the "resonance", is one source's rings and not a two-source structure. Most of this is inherited from the reference reproduction (r01); r04 did not introduce it.
- encoding fidelity: **3**. There is no shared dimension axis: same-space vectors are drawn at 23–49 mm. Packet amplitude carries no consistent scale (Z vs V, ∂L/∂V vs ∂L/∂Z). A has no source channel. ∂L/∂A is not index-aligned with A. The halo ellipses and the random-phase fragment gaps are decoration sitting inside a data field. What holds: the pen = tensor key is clean, and the crest loci are exact.
- insight legibility: **6**. The fold, the pen key, the labels and the rail read at 1 m. A stranger gets "Q and K interfere → a selection → Z, then gradients flow back." A scientist immediately sees the 5-vs-4 token count and the 3-row gradients. No misconception correction is defined (no §5).
- **VERDICT: FAIL**

## Mandates
1. **Token and shape consistency (V block x 22–52, y 137–154; ∂L/∂Q x 30–61 and ∂L/∂K x 147–181, y 47–60; ∂L/∂V x 160–184, y 85–92).**
   - Measured: K 5 rows, V 4 rows, A 5 peaks; ∂L/∂Q 3, ∂L/∂K 3, ∂L/∂V 2 rows. Packet widths for vectors that live in the same space run 23.2–48.9 mm.
   - Expected: V gets a 5th row, one per key and per A peak. ∂L/∂K and ∂L/∂V have 5 rows. ∂L/∂Q has as many rows as the queries shown (1 if Z is one output row, else 5). One dimension axis per space: Q, K, ∂L/∂Q, ∂L/∂K at one width, and V, Z, ∂L/∂Z, ∂L/∂V at one width.
   - This is additive and J2-compatible: no element is removed.
2. **The forward chain: hero comb → A → Z (comb x 88.5–121.0, y 192.7 ± 6.6; A row y 150.9; Z row y 127.9).**
   - Comb measured: S₁ circles only (m 14–45, 0 S₂ arcs), 0.66 L off the two-source crest at the lens edge. Expected: comb fringes are the standing-wave crests of both sources, i.e. hyperbolae r₁ − r₂ = const, symmetric about x 104.83. Keep the same count, pitch (1.042 mm on axis) and lens.
   - A measured: shares 0.110 / 0.232 / 0.262 / 0.253 / 0.143, not derivable from anything drawn. Expected: A is computed from something on the sheet, with the rule stated. For example, softmax of the drawn field's amplitude at the 5 dropline feet, or softmax(q·k_j/√d_k) from the drawn Q, K rows.
   - Z measured: amplitude 12.10 mm against the convex bound 4.40, NNLS residual 94 %, corr with drawn A·V −0.50. Expected: Z = Σ a_j V_j from the drawn A and V on the shared axis, so that \|Z\| ≤ max \|V_j\| (or a stated gain) and the residual is < 5 %.
3. **The backward chain: ∂L/∂V, ∂L/∂A, ∂L/∂S (∂L/∂V x 160–184, y 82–96; ∂L/∂A y 49.5, x 76.7–135.9; ∂L/∂Q / ∂L/∂K packets y 42–65).**
   - ∂L/∂V measured: corr with ∂L/∂Z +0.78 / −0.39, gains 0.417 / 0.465. Expected: each row = a_j·∂L/∂Z, with corr 1.00 and gain = a_j (≤ 0.262).
   - ∂L/∂A measured: peaks at x 85.8 / 96.4 / 104.8 / 113.3 / 124.4, offset up to 11.9 mm from A's 73.9 … 135.4. Heights are near-uniform (±11 %), which gives ∂L/∂S = A⊙(g − A·g) = [+0.10, −0.20, +0.15, −0.22, +0.18], only 2.1 % of ∂L/∂A. Meanwhile ∂L/∂Q / ∂L/∂K are drawn at 3.8–5.1 mm.
   - Expected: ∂L/∂A_j = ∂L/∂Z·V_j (signed), each peak under its A peak. ∂L/∂K_j = ∂L/∂S_j·q/√d_k, so the ∂L/∂K rows are signed multiples of one query row, with amplitude ∝ \|∂L/∂S_j\|.
   - Also fix the ∂L/∂V edge's opposing arrowheads (◁ at x 152.5 should be ▷).
   - This is the natural §5: softmax is shift-invariant, so a uniform upstream gradient reaches neither Q nor K. Draw it, don't contradict it.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S0 no dossier/encoding → no §7 check numbers | NOT FIXED | `studio/resonance-backprop/` still has no `dossier.md` / `encoding.md`. The check set above is derived. The lead/curator should commission a dossier that fixes A, V, the target, and d_k, so the three mandates have numbers to hit |
| S-fold, S-phase | n/a | dropped for this slug in the LEDGER; they travel with their flavours |
| regressions vs the r01 parent (v8) | none | Bullseye rings m 1–9 identical (same ink per ring). Comb identical: S₁ m 14–45 in both, so its error is inherited, not new. d = 59 L unchanged. The v8 dashed field (both sources, m 10–61 step 3) is replaced by dotted fragments that stay on the crest circles (±0.03 mm), so no truth held in r01 and lost now |
| J1 dot continuity (Juan's; measured for the lead) | measured OK | 0.30 mm closed-circle dots only, pitch median 0.99–1.00 mm on all 5 pens, 0 coincident; 1st-percentile spacing 0.66–0.76 mm where paths converge |
| J2 note for the lead | — | M1 is additive. M2 and M3 recompute packet contents and the comb curvature but keep every element, its position and its pen. Juan should rule whether "keep the original" covers the traced (non-computed) packet shapes |
