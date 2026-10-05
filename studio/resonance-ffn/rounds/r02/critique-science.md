# Science critique — resonance-ffn r02 · machine learning (attention + FFN as wave interference) · 2026-09-29
render: gallery/studio/resonance_ffn/current/pp_resonance_ffn_the-squash_v15.png (gcode: gallery/studio/resonance_ffn/current/pp_resonance_ffn_the-squash_v15.gcode, 39,846 cmds, 526 strokes, 5 pens)

**Missing inputs, which is itself a finding.** `studio/resonance-ffn/dossier.md` and `encoding.md` do not exist, so there are
no §1 math, §4 lies list, §5 misconception or §7 check numbers to recompute. The claims checked below come from
HANDOFF.md ("fringes → tanh → linear fan"; "lower bundle = same geometry carrying the gradient, green reach = tanh′";
"±1 asymptotes"; "2 forestgreen = Z"). I built the checks from first principles and measured them from the gcode
coordinates, parsed per `; color=N`. Without a dossier, the plate's science is not pinned down anywhere.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Q / K source centres, separation d | — | — | Q (24.25, 226.10), K (24.25, 181.70); d = 44.40 mm. Lower pair (24.25, 104.77)/(24.25, 60.37), same d | — |
| ring pitch λ (crest circles) | — | — | 1.200 mm (every ring, both pairs); upper r ≤ 25.2 (21 rings), lower r ≤ 7.2 (6 rings) | OK |
| max fringe order d/λ | — | 37.0 | fringes drawn n = −24…+24 (49), orders 25–37 omitted | OK (sampled) |
| bright-fringe loci \|r₁−r₂\| = nλ | — | hyperbolae | every green stroke has dr/λ within ±0.01 of an integer | **OK, exact** |
| squash = tanh (flat band x 110–143) | — | y = c + A·tanh(g(n−n₀)) | free fit c = 203.7, A = 24.4 mm, g = 0.141/fringe, max err **0.038 mm**; with the drawn asymptotes (c 203.9, A 24.0) max err 0.37 mm | OK |
| tanh centre (bias) | — | expected on central fringe n = 0 unless a bias is stated | tanh(0) falls on fringe **n = −2.01**; the central fringe sits at u = +0.277. No caption says so | uncaptioned |
| ±1 asymptotes at the flat band | — | 228.1 / 179.3 (fit) | dotted 227.9 / 179.9, 100 dots each, pitch 1.014 ± 0.097 mm | OK (≤0.6 mm) |
| linear fan (x 143 → 199.4) | — | affine | y₁₉₉ = 1.7768·y_flat − 158.38, max resid **0.01 mm**; asymptotes 246.1/161.0 vs affine image 246.55/161.27 | OK |
| forward continuity through the squash | — | 49 in → 49 out | 49 enter at x 86.6. Only **21** cross the flat band. The 28 saturated fringes (n +9…+24, −13…−24) stop at x 100.4–107.6 with last y up to 239.3 / down to 168.5, i.e. **11.4 mm (0.47 units) outside the ±1 bound** | PARTIAL |
| green reach = tanh′ (lower fan) | — | reach = 51.9·(1−u²), peak 51.9 mm at n = −2 | r = 0.984 over 21 lines, but n = −1 **41.4** vs 50.9 (−19 %) and n = −3 **41.7** vs 50.9 (−18 %), both shorter than n = −4 (47.4, tanh′ 0.926), so the **rank order is broken**. Tails: n = −12 8.4 vs 11.1 (−24 %), n = +8 9.6 vs 11.0. The 28 saturated fringes get **0 mm where tanh′ = 0.165 → 0.003** (8.5 → 0.1 mm expected) | **FAIL** |
| backward bundle geometry | — | backprop through tanh = multiply by diag(1−u²); no saturation | lower violet = upper violet translated −121.32 mm, **max resid 0.01 mm**, 49/49 lines | **FAIL** |
| "Z = AV" (HANDOFF, pen 2) | — | Z needs softmax and V | green fan = the raw Q–K fringe pattern (≈ QKᵀ). No V and no softmax anywhere on the sheet | caption wrong |

## Lies list (no dossier §4, so these are the standard lies for this subject)
| item | status |
|---|---|
| "A transformer FFN squashes to ±1" | **VIOLATED.** The black ±1 asymptotes (y 227.9 / 179.9 at x 104–143, fanning to 246.1 / 161.0) and the subtitle "FFN · THE SQUASH" say it saturates. Transformer FFNs use ReLU (Vaswani 2017), GELU (GPT-2, BERT) or SwiGLU (LLaMA), and all of them are unbounded above. GELU's minimum is −0.170 at x = −0.752 |
| "The gradient takes the same path/shape back" / "backward re-applies the nonlinearity" | **VIOLATED.** The lower violet bundle (y 28.7–136.4) is an exact copy of the forward bundle, so the gradient is drawn pinched into a ±1 band |
| "Saturated units pass exactly zero gradient" | **VIOLATED (partial).** Green reach steps from 9.6 mm to nothing at n = +9 / −13, where tanh′ = 0.165 |
| decorative marks posing as data | **VIOLATED.** The upper fan's alternating start stagger (x 40 vs 44) is copied into the lower fan, where length IS the data, and it cuts the n = −1 and −3 reaches by 18–19 %. The lower ring count (6 vs 21) encodes nothing stated |
| "Interference cross-term ≈ Q·K" | clean. Fringe loci are exact to 0.01 λ |
| "FFN expands d → 4d, then W₂ mixes units" | not shown: 49 lines map one-to-one and W₂ is a uniform scalar gain of 1.777. Acceptable as a 1-D transfer-function picture, but uncaptioned |

## Scores
- **truth 5.** The optics and the functions are drawn exactly (hyperbolae to 0.01 λ, tanh to 0.04 mm, affine fan to 0.01 mm). The ML claim is false: a transformer FFN does not squash to ±1, and the backward pass does not re-squash the gradient.
- **fidelity 6.** tanh′, the only gradient quantity, has a broken rank order near its peak, tails 13–24 % low, and 28 channels truncated to zero. The lower bundle is a decorative copy that carries no quantity. 28/49 forward lines vanish outside ±1.
- **legibility 3.** The only words on the sheet are the title, "FFN · THE SQUASH", "+1" and "−1". Nothing names Q/K, forward/backward, ∂L, tanh′ or the direction of flow. A stranger reads two identical machines. A scientist reads "FFN = tanh" and objects.
- **VERDICT: FAIL**

## Mandates
1. **Nonlinearity truth (upper bundle, x 86.6–199.4, y 150–258; black asymptotes and subtitle).** Measured: the flat band is an exact bounded tanh (A = 24.4 mm, max err 0.038 mm) between ±1 asymptotes at y 227.9 / 179.9, captioned "FFN". Expected: a transformer FFN activation. Use GELU, x·Φ(x): positive-side lines keep linear spacing with **no upper asymptote**, negative-side lines collapse onto a single floor at **−0.170 unit** (−4.1 mm below the zero line at the current 24 mm unit), with the minimum at x = −0.752. Delete the +1 dotted line and redraw −1 as the GELU floor. Otherwise keep tanh and stop calling it an FFN (retitle it as a tanh MLP / gate).
2. **Green reach = tanh′ (lower green fan, x 33.5–85.4, y 60.4–97.0).** Measured: n = −1 **41.4 mm** and n = −3 **41.7 mm**, expected **50.9 mm** (51.9·tanh′, tanh′ = 0.980/0.981), so both are shorter than n = −4 (47.4). n = −12 is 8.4 vs 11.1 mm. The 28 saturated fringes (n +9…+24, −13…−24) have **0 mm**, expected 8.5 → 0.1 mm. Draw reach = 51.9·(1 − u_n²) exactly for all 49 fringes, with no inherited start-stagger. Where the reach is under 1 mm, draw a single dot rather than nothing, so "small" is not drawn as "zero".
3. **Backward bundle (violet, x 86.6–199.4, y 28.7–136.4) plus labels.** Measured: it is the forward bundle translated −121.32 mm (residual 0.01 mm), so the gradient is drawn saturating into a ±1 band. Expected: backprop through the nonlinearity is linear, ∂L/∂z_n = (1 − u_n²)·(W₂ᵀδ)_n. After the fan, each line's offset from the zero line should scale by tanh′_n: saturated fringes collapse toward the centre line and are not pinned to walls, and no line should follow the forward squash curve. Then put the science on the sheet: "forward" / "backward ∂L" at each bundle, flow arrows (left→right above, right→left below), "tanh′" at the green reach, Q and K at the sources, and a note if the tanh centre stays on fringe n = −2 (bias b₁). Fix the HANDOFF caption as well: the green fan is QKᵀ, not Z = AV, since there is no softmax or V on the sheet.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | No `studio/resonance-ffn/LEDGER.md` exists, so this was pass 1 only |

**Out of scope, flagged for the lead:** `studio/resonance-ffn/FEEDBACK.md` (Juan, 2026-09-28 23:39) is marked binding and applies to res_ffn: "KEEP THE ORIGINAL… keep EVERY element… the ONLY change wanted is dot continuity". r02 ("the squash", rendered 23:44) is a full redesign that removes all of those elements. The gcode also has no M0/park at the four colour changes, so the swap pauses depend on the streamer (`stream_pen_layers`).
