# Science critique — attention-weaving r05 · machine learning (transformer attention, softmax) · 2026-09-28
render: gallery/studio/attention_weaving/current/pp_attention_weaving_area-smooth_v7.png (gcode: gallery/studio/attention_weaving/current/pp_attention_weaving_area-smooth_v7.gcode, 17 302 cmds, 5 pens)

**Missing inputs (finding):** there is no `studio/attention-weaving/dossier.md`, `encoding.md`, or `LEDGER.md`,
so there are no §7 check numbers, no §4 lies list, and no §5 misconception to grade against. The check numbers below
were recomputed from the data the HANDOFF names (GPT-2 small L2 H9, row ` itself`, cached
`~/.promptplot/attn_gpt2.npz`, default sentence "The pen plotter drew a black hole while the transformer watched itself
think."). The token indices were checked against the GPT-2 vocab: `Ġplotter` is not a single token, so it splits into
` plot`+`ter`, giving 15 tokens with ` transformer`=10, ` watched`=11, ` itself`=12. The lies list is the BRIEF's
"What must be TRUE".

Measured from the gcode, not the PNG. Wall at y=183.6. Aperture x∈[77.54, 129.46] (51.92 mm). The hill is scaled so 1.0 = 28.0 mm.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| a_max (key) | — | 0.4159 (` transformer`, idx 10) | caption "0.416 TRANSFORMER"; hill peak x=110.38 inside transformer bin [101.34,112.51] | OK |
| a_2, a_3 | — | 0.3769 watched · 0.1112 itself | "0.377 WATCHED · 0.111 ITSELF" | OK |
| visible keys for row 12 | — | 13 (keys 13 ` think`, 14 `.` causally masked, A=0) | 13 K strands reach the wall | OK (count) |
| entropy H / max | — | 1.984 / log2 13 = 3.700 bits | "H = 1.98 OF 3.70 BITS" | OK |
| Σa | — | float64 sum of stored float32 row = 0.999999963 | "Σa = 1.000000000" | nit: 9 d.p. is past float32 precision. It is only true after renormalising, so state that or print 7 d.p. |
| hill area per key partition | — | a_j | ∫ per bin / total: max abs error 1.2e-4 (0.5 % rel) over all 13 bins | OK |
| cumulative curve at ticks | — | cumsum a | max abs error 1e-4; ends at 28.0 mm = "1.000" | OK |
| "58 OF 195 SCORES CROSS" | — | 15 Q × 13 K = 195 pairs | chained Q×K strand crossings: 58 pairs cross, once each (banded matrix) | number OK, **meaning false**: these are geometric crossings, not QKᵀ scores |
| "NONE MASKED" | — | row 12 of a causal head has 2 masked keys (13, 14). Across the 15×13 Q×K grid, 78 pairs are causally masked | caption says none | **VIOLATED** |
| strands in / out | — | brief: out > Q or K alone | 15 Q + 13 K = 28 at the wall → 28 green lanes at the wall → 28 at the right reed | OK |
| K strand j lands in partition j | — | 13/13 | K strands in sentence order land at x=80.5, 85.0, 89.4, 93.8, 98.1, 102.4, 106.9, 109.9, 113.6, 116.6, **119.6 (double = transformer)**, **122.6 (double = watched)**, 126.3. Only 3/13 (The, watched, itself) are in their own bin | **VIOLATED** |
| Z lane share per key vs a | — | a: 0.416 / 0.377 / 0.111 / tail(keys 1–9) 0.070 / The 0.026 | lanes 7/7/3/9/2 of 28 → 0.250 / 0.250 / 0.107 / 0.321 / 0.071 | **VIOLATED** (floor of 1 lane per key, then largest remainder) |
| hill bin widths | — | equal, or else height stops meaning weight | [4.28, 2.17×9, 11.17, 11.17, 5.78] mm, set by lane count | **VIOLATED** (heights lie, see fidelity) |

## Lies list (BRIEF "What must be TRUE")
| item | status |
|---|---|
| Everything passes through the waist (count in = count out) | clean. 15 Q and 13 K reach the aperture (3 Q and 3 K stop at y≈184.8–185.5 under the 4-pass hill baseline), and 28 lanes leave. Nothing is born below the wall. |
| Over/under is real | clean. 0 drawn-ink crossings Q×K and V×Z. At the 67 Q×K crossings, Q is on top 41 times and K 26 times. At the V×Z crossings, V is on top 186 times and Z 44 times. Both directions occur, so it is a weave, not a layer. |
| Softmax normalises, peaked not uniform | clean on area (hill areas = a to 1.2e-4, CDF ends 1.000, H 1.98 of 3.70 bits) |
| V joins after the waist | clean. Gold y_max = 179.2 < wall 183.6, and all 13 V strands start at the left reed y=137.0–178.8. |
| Braid carries more strands than Q or K alone | clean (28 vs 15 and 13) |
| Bundles terminate in margin reeds | **VIOLATED**: 7 of 13 K strands start in mid-air at (165.6,186.8), (172.8,191.6), (180.8,197.7), (189.3,205.2), (198.5,214.4), (208.3,225.6), (218.6,239.0), with no reed tick. The K reed has only 6 ticks (top 56.6, 83.9, 111.4, 149.1; right 255.1, 276.2). |
| Caption tells the truth | **VIOLATED**: "NONE MASKED" is false for a causal row 12. "SCORES CROSS" labels drawing geometry as QKᵀ scores. |
| Key identity carried through the weave | **VIOLATED**: the double-passed K "transformer" enters the aperture at x=119.6, which is inside **watched's** partition and 9.2 mm right of the transformer peak. 10/13 K strands feed another key's bin. |

## Scores
- **truth 6**: every data number printed is correct: a_max, top-3, H, the CDF, hill areas, and 58/195. But "NONE MASKED" is false. "SCORES CROSS" names a geometric count as scores. The argmax key's filament is delivered into the wrong key's partition. 14 of the 15 Q strands, including the queries of future tokens 13 and 14, are routed through a softmax row they take no part in.
- **encoding fidelity 5**: the hill *area* is exact, but its x-axis bins are sized by lane count, so the *height* the eye reads is wrong. ` itself` mean height is 10.93 mm = 0.52× transformer, where the true ratio is 0.27. The left-wall jump is 9.25 mm = 0.33× peak for a=0.026, where the true ratio is 0.06. The Z=AV rope gives each key at least 1 lane: transformer and watched both get 7 lanes (0.416 vs 0.377 drawn equal), and the 9-key tail holds 32 % of the rope for 7 % of the mass (4.6×). The V weight is binary (3 passes vs 2): ` itself` (0.111) is drawn like a 0.0008 key.
- **insight legibility 6**: the aperture, the hill and "SUMS TO ONE" land with a stranger, and the bottom half now matches the top in craft. But the 13 partitions carry no token labels (only three numbers set off to the right). There is no Q·Kᵀ label. "58 OF 195 SCORES CROSS" cannot be decoded by a scientist or a stranger. No misconception correction is identifiable (no dossier §5).
- **VERDICT: FAIL**

## Mandates
1. **Hill x-axis: stop letting bin width lie about height.** The partition ticks at y=181.2–184.2 sit at x=77.54, 81.82, 83.99 … 101.34, 112.51, 123.68, 129.46, giving widths [4.28, 2.17×9, 11.17, 11.17, 5.78] mm. Measured mean hill heights are itself 10.93 mm vs transformer 21.18 mm (0.52), and the left-wall jump is 9.25 mm at x=77.54 (0.33 of the 28.0 mm peak). Expected: height ∝ a_j, so itself/transformer = 0.267 and The/transformer = 0.062. Two ways to fix it: (a) use equal-width bins (51.92/13 = 3.99 mm) and keep area-exactness, or (b) make bin width ∝ a_j and flatten the top. Keep the 1.2e-4 area accuracy. Lives in the aperture, x 77.5–129.5, y 183.6–211.6.
2. **Z=AV rope lanes must be allocated ∝ a, not floor-1.** At the right reed (x=229.4, y 72.6–135.5) and the wall exits (x 79.2–127.8), the lanes per key are transformer 7, watched 7, itself 3, The 2, and 1 each for keys 1–9. That gives shares 0.250/0.250/0.107/0.071/0.321. Expected: 0.416/0.377/0.111/0.026/0.070. With 28 lanes that is ≈ 12/11/3/1/1 (tail keys merged or given sub-lane thickness), or lane pitch/pen passes ∝ a_j. Transformer must visibly out-weigh watched (0.416 vs 0.377). Give the ` itself` V strand (0.111, left reed) more ink than the 0.0008 keys: today both are 2 passes.
3. **Q·Kᵀ layer: identity and captions.** K_transformer (double-passed, wall x=119.6) and K_watched (x=122.6) both land in watched's bin [112.51, 123.68]. Only 3/13 K strands land in their own key's bin. Expected: K_j enters partition j, so K_transformer lands inside [101.34, 112.51] under the peak at x=110.38. Seven K strands begin in mid-air (x 165–219, y 187–239) with no reed tick. Expected: 13 K reed ticks. In the caption block, y≈40–47: "NONE MASKED" is false. Row 12 has 2 causally masked keys (think, .), so state "2 MASKED (CAUSAL)" or draw their strands stopping at the wall. "58 OF 195 SCORES CROSS" (measured 58, correct) counts drawn crossings, not scores: relabel it or encode an actual quantity (e.g. q_itself·k_j).

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | no `LEDGER.md` exists for this slug; pass 1 only |
