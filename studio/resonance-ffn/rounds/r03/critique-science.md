# Science critique — resonance-ffn r03 · machine learning (attention + FFN block as wave interference) · 2026-09-29
render: gallery/studio/resonance_ffn/current/pp_resonance_ffn_two-interferences_v13.png (+ .gcode, 30 045 cmds, 605 strokes, 6 layers)

Inputs: HANDOFF.md, the PNG, the gcode. **There is no `dossier.md`, no `encoding.md`, no `LEDGER.md` for this
slug.** So there are no §1 formulas, no §4 lies list and no §7 check numbers to recompute. That missing
paperwork is itself a finding. Everything below is checked against (a) the handoff's claims and (b) the
standard attention/FFN forward-backward identities. `DESCRIPTION.md` was read as the brief, since no dossier
exists. All measurements come from parsing the gcode by `; color=N`.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed (identity) | measured on sheet | OK? |
|---|---|---|---|---|
| Z = Σ a_j·v_j (green y=112 vs 4 goldenrod rows y=143.2/136.8/130.4/124.0, x 29–78) | — | Z − ΣV ≡ 0, scale 1 | max \|Z−ΣV\| 0.040 mm (gcode quantum 0.01), LSQ scale 0.9996 | OK |
| ∂L/∂k_j = (∂L/∂s_j/√d)·q → ∂L/∂K ∝ Q | — | residual 0 | ∂L/∂K = 0.7657·Q, rel. resid 1.8 % (lag 3.06 mm = centring of 52.13 vs 46 mm rows) | OK |
| ∂L/∂q = Σ_j (∂L/∂s_j/√d)·k_j | — | ∝ K only if 1 key | ∂L/∂Q = 0.959·K + 12.6 % rel. residual, so ≥2 keys exist in the computation but only 1 K row is drawn | OK math / NOT drawn |
| FFN forward y = H·tanh(z_k·sin²πu), u=(x−94)/97 | — | — | all 8 visible violet upper lines fit with max resid ≤ 0.012 mm, H = 30.03 mm, p = 2.000; z = 3.702, 3.189, 2.581, 1.801, 1.290, 1.120, 0.326, 0.248 | OK |
| FFN backward = −λ_k·sin²πu·sech²(z_k sin²πu) (chain rule: upstream × tanh′) | — | z_k of each backward line = z_k of its forward twin | 11 backward lines, max resid ≤ 0.016 mm; 8 pair exactly (3.703↔3.702, 3.191↔3.189, 2.581↔2.581, 1.800↔1.801, 1.290↔1.290, 1.120↔1.120, 0.325↔0.326, 0.247↔0.248); **3 have no forward line: \|z\| = 3.163, 2.942, 0.013** | PARTIAL |
| saturated centre gradient λ·sech²(z) | — | → 0 as z grows | z=3.70: 0.22 mm; z=3.19: 1.07 mm; z=0.33: 20.4 mm | OK |
| hero field A (black, sources (61,198),(127,198)) | — | should carry a_j (≥4 weights, Σ=1) | ring pitch 1.2220 mm both sources, baseline 66.00 mm, relative phase 0.279 mm = 0.228 cyc; no channel with 4 values | NOT ENCODED |
| twin field ∂L/∂A (sources (81.13,64.56),(106.87,64.56)) | — | ∂L/∂A_j = ∂L/∂Z·v_j, independent of A | pitch 1.2230/1.2255 mm (= hero), phase 0.287 mm = 0.234 cyc (= hero within 0.006 cyc, under gcode quantum), baseline 25.74 = 0.390 × 66.00 | VIOLATED (copy of A) |
| handoff "homothety ratio −0.39 through fan node (94,102)" | — | homothety scales pitch to 0.477 mm | centres: y-ratio −0.39 ✓, x-ratio **+0.39** (Q-side stays left); pitch unscaled 1.22 mm | claim inaccurate |
| dots: round, r 0.12, 1.00 mm pitch, 290 | — | — | 290 dots, r 0.117–0.119; pitch c0 0.97 (0.92–1.04), c1/c3 1.02, c2 0.97, c5 1.00 | OK |
| handoff plot: F600, 1 s dwells, 6 swaps | — | — | gcode feeds F1200–F2600, dwells G4 P0.2 only, 5 swaps (6 layers); travel 3.29 m (preview) vs 3.16 claimed | claim ≠ file |

## Lies list       item | clean / VIOLATED (where)
There is no dossier §4, so this list uses the standard plate lies.
| item | status |
|---|---|
| decorative mark posing as data | **VIOLATED**. The black twin at (94, 64.6) is captioned ∂L/∂A but is the hero's pitch and phase at 0.39 baseline. It carries no gradient number. |
| quantity claimed but no channel carries it | **VIOLATED**. A (the attention weights) is not readable anywhere. V-row rms 1.154/0.743/0.200/0.237 mm confounds a_j with \|v_j\|, and there is no softmax row. |
| lying counts | **VIOLATED**. The FFN fan (x 94–191, y 76–132) has 11 backward lines but only 8 forward. The key/value count is 1 K row (x 127–173, y 254) against 4 V rows. |
| broken / mixed scales | clean. V, Z share one scale (sum exact); Q/∂L/∂K share one; the fan shares H = 30.03 mm. |
| sign folded silently | **SUSPECT**. 8/8 forward tanh lines sit above the spine and 11/11 backward lines sit below it. Only magnitudes are drawn, and no caption says so. |
| handoff caption vs file | VIOLATED (minor). The "homothety" is really scale plus mirror, with pitch unscaled. The handoff says F600/1 s dwells; the file has F1600/0.2 s. It says 6 swaps; the file has 5. |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 6**: Every equation that is actually drawn is exact to gcode resolution: Z=ΣV, ∂L/∂K∝Q, tanh/tanh′ chain rule. But two captions are false. The twin is not ∂L/∂A. "K" is one key out of at least 2 (the ∂L/∂Q residual proves it), set against 4 values.
- **fidelity 5**: Neither black field carries its matrix: A has no channel, and ∂L/∂A is a copy of A. Three hidden units have no forward line (z=3.163 is merged 0.11 mm into z=3.19, z=2.942 is erased despite 1.1 mm clearance, z=0.013 is buried 0.39 mm into the spine). Signs are folded.
- **legibility 5**: The hero, the twin and the fan carry no label at all: no A, no ∂L/∂A, no tanh / tanh′, no FFN. The title "ATTENTION AS RESONANCE" does not mention the FFN. A stranger reads two bullseye pairs and a violet lens. A scientist cannot match forward to backward lines, because the counts differ (8 vs 11). The strongest insight on the sheet is the saturated tanh line whose gradient notch goes to 0 (0.22 mm at z=3.70). It is invisible without an asymptote rail and labels.
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **The two black fields must carry A and ∂L/∂A (hero (61–127, 198); twin (81–107, 64.6)).** Measured: twin pitch 1.223 mm and phase 0.234 cyc, identical to the hero's 1.222 mm / 0.228 cyc; only the baseline differs (25.74 = 0.39 × 66.00 mm). No channel holds the 4 attention weights. Expected: the hero encodes a_j (4 values, Σ=1, e.g. per-key fringe weight or ring count). The twin encodes ∂L/∂A_j = ∂L/∂Z·v_j (signed) through the same channel, measurably different from the hero. Label both "A" and "∂L/∂A". If that can't be done, drop the ∂L/∂A caption.
2. **Draw every key the computation uses (K block x 127–173, y 254; ∂L/∂K at y 42.7).** Measured: 1 K row against 4 V rows. ∂L/∂Q = 0.959·K leaves a 12.6 % residual, which proves the other keys exist. Expected: one K row per V row (4), and one ∂L/∂K row per key, each ∝ q. The drawn one already holds (∂L/∂K = 0.766·Q, 1.8 % resid); keep that.
3. **The FFN fan must show every hidden unit once forward and once backward, with sign and saturation readable (violet, x 94–191).** Measured: 11 backward lines against 8 forward. The forward lines for |z| = 3.163, 2.942 and 0.013 are missing; the saturated tops of z=2.58 and z=3.19 are erased where they merge. All lines share one sign. Expected: 11 = 11, with coincident lines kept as registered lanes rather than deleted. Carry negative pre-activations or gradients through a channel (or caption "|·|"). Draw the H = 30.03 mm tanh asymptote and label the fan "tanh" / "tanh′".

## Follow-up on open mandates   id | status | evidence
No LEDGER.md exists for resonance-ffn, so there are no open S* mandates to follow up. This is pass 1.

Out of scope for science, but it blocks the round: `studio/resonance-ffn/FEEDBACK.md` (Juan, 2026-09-28 23:39, binding for res_ffn) says "KEEP THE ORIGINAL — v13 (rounds/r01) is the design … ONLY change … dot continuity". r03 ("two interferences") is a different composition, and it removed the V-knot, the softmax row, the packets and the labels.
