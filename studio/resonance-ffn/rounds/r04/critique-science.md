# Science critique — resonance-ffn r04 · machine learning (attention + FFN block as wave interference) · 2026-09-29
render: gallery/studio/resonance_ffn/current/pp_resonance_ffn_iterate_v5.png (+ .gcode, 90,973 cmds, 4,751 strokes, 6 layers)

Inputs: HANDOFF.md, the PNG, the gcode, and `DESCRIPTION.md` § science as the brief. I also read the parent gcode
(`gallery/studio/res_ffn/current/pp_res_ffn_v5.gcode`, which is v9/r01 output per the LEDGER) for regression
checks. **`dossier.md` and `encoding.md` still do not exist** (S0), so this critique has no §7 check numbers and no
§4 lies list. Every check below comes from the plate's own captions plus the standard attention/FFN
forward–backward identities. All measurements are parsed from the gcode by `; color=N`.

**Geometry freeze confirmed (J2).** The continuous coloured ink matches r01 on a 0.2 mm grid with ±0.4 mm tolerance:
0 mm of r01 coloured line is missing and 0 mm is new, on all 5 colour pens. The black pen differs only in type, the
FFN bracket and the dots. So every data-geometry finding below is **inherited from r01**. r04 changed only the
marks and the stream.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed / identity | measured on sheet | OK? |
|---|---|---|---|---|
| hero ring pitch / source baseline (DESCRIPTION: d = 35·L, pitch 1.21 × 1.41) | — | d/λx = 35 | axis cut y=166.5: λx = 1.211 mm; x=84 cut: λy = 1.412 mm; sources x 83.84 / 126.17, d = 42.33 mm = 34.95 λx | OK |
| ∂L/∂A twin (DESCRIPTION: d = 14·L, 1.17 pitch, 0.39 scale) | — | ∂L/∂A_j = ∂L/∂Z·v_j, independent of A's geometry | pitch 1.174 mm (0.970 × hero), baseline ≈ 16.5 mm = 0.390 × 42.33; same construction | construction as claimed, **no gradient channel** (S1) |
| softmax row (black, baseline y 116.30) | — | one query over n keys gives n weights, n = n_K = n_V | 6 stemmed peaks at x 76.2 / 90.4 / 97.4 / 104.6 / 119.2 / 133.0, heights 7.51 / 13.27 / 4.34 / 10.12 / 13.25 / 6.72 mm, plus 3 dotted ghost Λs at x 83.6 / 112.0 / 127.3 (apex 4.34 / 4.77 / 4.34 mm, 9 dots each). Q 5 rows, K 5, V 5 | **FAIL** (S3) |
| A → V leaders (ochre dot trains leaving the softmax nodes) | — | one leader per real weight | 6 leaders leave x = 76.2, **83.5**, 90.5, 97.4, 104.7, **111.8**. Two of them start from ghost nodes. **No leader** leaves the 119.2 peak (13.25 mm, joint-largest weight) or the 133.0 peak | **FAIL** |
| Z = AV (green, y 63.94, x 51.5–132.3) | — | Σa_j = 1 ⇒ \|Z\| ≤ max_j \|v_j\| | Z peak **14.19 mm**; V peaks 7.10 / 6.64 / 5.53 / 6.25 / 6.72 mm, so Z = **2.0 ×** the convex bound. LSQ Z on the 5 V rows (common u): rel. residual **1.00**; best affine-x map: 0.96 | **FAIL** |
| ∂L/∂K ∝ Q · ∂L/∂Q ∝ Σ K · ∂L/∂V_j = a_j·∂L/∂Z | — | residual → 0 | ∂L/∂K rows vs Q: rel. resid 0.54 / 0.97; ∂L/∂Q rows vs K: 0.99 / 1.00; ∂L/∂V vs ∂L/∂Z: 1.00. Row counts: 2 ∂L/∂Q vs 5 Q, 2 ∂L/∂K vs 5 K, 1 ∂L/∂V vs 5 V | **FAIL** (illustrative, uncaptioned) |
| FFN forward dome (violet, x 150.3–161.8, spine y 63.94) | — | DESCRIPTION: tanh(1.75·v)/tanh(1.75) | 5 lines per side, peaks 2.73 / 4.49 / 6.02 / 7.40 / 8.69 mm, mirror-exact to 0.01 mm; flat top on the outer line f(0.4)/f(0.5) = 0.984 | as claimed; tanh, not GELU (S2) |
| FFN nonlinearity′ (violet, x 152.1–165.6, spine y 35.68) | — | δ_in = δ_out ⊙ σ′(z). σ′ falls as \|z\| grows; tanh′ at c = 1.75 ≈ 0.91 innermost → 0.11 outermost | centre pass fraction b(½)/b_peak = **0 (innermost split, 0.61 mm gap at x 158.55–159.16)**, 0.63, 0.77, 0.84, **0.89** for forward peaks 2.73 → 8.69 mm. Notch depth 1.46+ / 1.28 / 1.08 / 0.91 / 0.75 mm, so it is not the "identical D" DESCRIPTION claims | **INVERTED** |
| FFN backward stage order (flow ◄ from ∂L/∂Y x 193 to ∂L/∂Z x 111) | — | ∂L/∂h = W₂ᵀ∂L/∂Y first, then ⊙σ′, then W₁ᵀ → ∂L/∂Z | the first stage met from ∂L/∂Y (packet x 167.5–182.1) is labelled **expandᵀ**, and the last before ∂L/∂Z (x 134.8–150.2) is labelled **projectᵀ** | **FAIL** (inherited from ref) |
| fan counts (S4) | — | n_fwd = n_bwd | 5 fwd = 5 bwd per side, 10 = 10 total | OK |
| dots (HANDOFF: r 0.15, 1.0 mm pitch) | — | — | 4,038 round closed loops, r 0.149 (0.148–0.150); nearest-neighbour median 0.99–1.00 mm on every pen. Black has 74 pairs < 0.6 mm (the scatter textures) | OK |
| stream claims | — | — | layers 720/1058/201/1082/268/1422 = 4,751 ✓; draw 14,257.6 mm ✓; in-layer travel 9.09 m + entries (file order 9.76 m) vs 9.49 m claimed ✓; hops > 80 mm: c0 140.9, c1 172.7, c5 93.3 / 89.7 ✓; feeds F1200–2600, only G4 P0.2, stated honestly ✓; each colour contiguous ✓ | OK |

## Lies list       item | clean / VIOLATED (where)
No dossier §4 exists, so these are the standard lies for this subject.
| item | status |
|---|---|
| "Z = AV" while Z exceeds every V | **VIOLATED.** The green packet at (51–132, 63.9) peaks at 14.19 mm, and no V row exceeds 7.10 mm. It is not in the span of the V rows (residual 1.00). |
| gradient drawn as a copy / a constant, not through the local derivative | **VIOLATED.** The nonlinearity′ notch at (152–166, 35.7) removes the gradient from the *least*-saturated line (split at centre) and keeps 89 % on the most-saturated one. That is the reverse of σ′. |
| backprop order | **VIOLATED.** Right-to-left from ∂L/∂Y the stages read expandᵀ → nonlinearity′ → projectᵀ. The chain rule gives projectᵀ (W₂ᵀ) → σ′ → expandᵀ (W₁ᵀ). |
| decorative marks posing as data | **VIOLATED, and worse than r01.** The three dotted ghost Λs in the softmax row are now 9 dots at 1.0 mm (r01: 4–5 dots), with apex 4.34 / 4.77 / 4.34 mm. That equals or beats the real 97.4 peak (4.34 mm), so the row reads as 9 weights. Two ghost nodes also feed V. |
| lying counts | **VIOLATED.** 5 Q / 5 K / 5 V against 6 (+3) softmax weights; 2 / 2 / 1 ∂L rows against 5 / 5 / 5. |
| FFN nonlinearity saturates (tanh) | **VIOLATED (uncaptioned).** A flat-topped bounded dome under "FFN" is still drawn. Transformer FFNs use GELU/ReLU/SwiGLU. |
| ∂L/∂A carries a gradient | **VIOLATED.** It is the hero's construction at pitch 0.970× and baseline 0.390×, with no channel for ∂L/∂Z·v_j. |
| broken / mixed scales | clean inside each element (dome mirror 0.01 mm, hero/twin pitches regular). No cross-element scale is claimed. |
| handoff caption vs file | clean. Every HANDOFF stream number checks out. |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 4.** The optics are exact (λ 1.211 × 1.412 mm, d = 35 λ), and so are the stream claims. But the sheet states four ML falsehoods in ink: Z = AV at 2× its bound, backward FFN stages in reverse chain-rule order, a σ′ notch with inverted rank order, and a saturating "FFN". The counts disagree as well.
- **fidelity 4.** No drawn quantity is computed from any other (all ∂ rows and Z have residual 0.54–1.00 against their sources). The weight→V wiring skips the largest weight and feeds two ghost nodes. The ghost peaks now read as data at full density.
- **legibility 5.** The pipeline story (Q,K → interference → softmax → V → Z → FFN → Y, with a backward row) is labelled and flow-arrowed, and a stranger can follow it. But "nonlinearity" is set 24 % tighter than r01 (16.82 → 12.84 mm). Its i-stems sit 0.15 and 0.19 mm from the neighbouring n / t (below a 0.3–0.4 mm nib), so it reads "nonlhear ty" twice. The softmax row reads as 9 peaks. A scientist stops at the reversed backward order.
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **Backward FFN order (violet foot row, labels at y ≈ 24–27).** Measured: flowing ◄ from ∂L/∂Y (x 193), the first stage (packet x 167.5–182.1) is labelled `expandᵀ`, and the last before ∂L/∂Z (x 134.8–150.2) is labelled `projectᵀ`. Expected: `projectᵀ` (W₂ᵀ) at x 167.5–182.1, nearest ∂L/∂Y, and `expandᵀ` (W₁ᵀ) at x 134.8–150.2, nearest ∂L/∂Z. This is a two-label swap. No element is added or removed, so it is J2-compatible. While resetting the type, restore r01's letter pitch for `nonlinearity` / `nonlinearity′`: 16.82 mm word width, and every i-stem ≥ 0.6 mm from its neighbours (now 0.15 / 0.19 mm).
2. **nonlinearity′ must be σ′, not a constant notch (violet, x 152.1–165.6, y 28.8–42.6).** Measured centre pass fraction: 0 (innermost line split, 0.61 mm gap), 0.63, 0.77, 0.84, 0.89 for forward peaks 2.73 / 4.49 / 6.02 / 7.40 / 8.69 mm. Expected: monotone *decreasing* with forward amplitude. For the drawn tanh at c = 1.75 that is ≈ 0.91 innermost → 0.11 outermost, i.e. b_k(u) = g_k(u)·(1 − y_k(u)²). This keeps the twin-peak mark and 5 = 5 lines, and the innermost line stays unbroken. It changes a kept element's curve, so it needs a lead/Juan ruling under J2. If that is refused, caption the row "schematic" and drop the ′ claim from DESCRIPTION.
3. **A → V → Z channel (softmax row y 116–130, ochre leaders, green Z at y 63.9).** Measured: leaders leave the ghost nodes x 83.5 / 111.8, and none leaves the real 119.2 (13.25 mm) or 133.0 (6.72 mm) peaks. The ghost Λs stand 4.34 / 4.77 / 4.34 mm (9 dots), level with the real 4.34 mm peak. Z peaks at 14.19 mm against max V 7.10 mm. Expected, all without removing anything:
   - re-anchor the leaders' start points on the six stemmed peaks;
   - drop the ghost Λ apex to ≤ 2.2 mm (< ½ the smallest real peak) so they read as sub-threshold;
   - either bring Z's envelope to ≤ 7.10 mm (blocked by J2, needs Juan) or put "schematic" beside `Z = AV`.

## Follow-up on open mandates   id | status | evidence
| id | status | evidence |
|---|---|---|
| S0 | **NOT FIXED** | `studio/resonance-ffn/dossier.md` and `encoding.md` are still absent, so there are no §7 numbers to recompute. |
| S1 | **NOT FIXED** (blocked by J2) | Twin pitch 1.174 mm = 0.970 × hero 1.211; baseline 16.5 = 0.390 × 42.33 mm. The same construction with no ∂L/∂Z·v_j channel. |
| S2 | **NOT FIXED** (blocked by J2) | The dome is still a bounded flat top (outer line f(0.4)/f(0.5) = 0.984, peaks mirror-exact) under an "FFN" bracket, with no tanh caption. |
| S3 | **NOT FIXED, legibility REGRESSED** | Still 5 Q / 5 K / 5 V vs 6 stemmed peaks. The dot fix grew the 3 ghost Λs from 4–5 dots (apex 3.7 / 4.7 / 3.7 mm in r01) to 9 dots (4.34 / 4.77 / 4.34 mm), so the row now reads as 9 weights. New related finding: the leader wiring skips the 119.2 / 133.0 peaks and feeds 2 ghost nodes. |
| S4 | **FIXED** (holds) | 5 forward = 5 backward per side (10 = 10). The innermost backward line is split at the centre by a 0.61 mm gap, which is a symptom of mandate 2. |
| S5 | **FIXED** | HANDOFF states that the file carries F1200–2600 and G4 P0.2 and that timings are on the clamped plot-plate model. The file confirms feeds {1200…2600} and dwell G4 P0.2 only. |
| regression check | — | Coloured data geometry is identical to r01 (0 mm moved beyond 0.4 mm). The truths that held in r01 still hold. The regressions are legibility only: ghost-peak density (S3), and the `nonlinearity` letter pitch compressed 24 %, which reopens A10's concern. |

New science items for the LEDGER (the lead to file): **S6** backward FFN stage order reversed (J2-compatible label swap). **S7** nonlinearity′ rank order inverted versus σ′. **S8** Z = AV exceeds the convex bound (2.0×) and the A→V leaders miswire (2 ghost origins, the largest weight unwired).
