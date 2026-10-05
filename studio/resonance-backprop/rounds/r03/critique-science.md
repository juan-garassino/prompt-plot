# Science critique — resonance-backprop r03 · machine learning (attention fwd+bwd as wave interference) · 2026-09-29
render: gallery/studio/res_backprop/current/pp_res_backprop_gradient-as-phase_v9.png (gcode: gallery/studio/res_backprop/current/pp_res_backprop_gradient-as-phase_v9.gcode, 57 205 cmds, 585 pen-down strokes: pen0 14 · pen1 100 · pen2 15 · pen3 102 · pen4 354)

This is pass 1 with a follow-up. **Dossier finding (still open from r02):** `studio/resonance-backprop/`
has no `dossier.md`, no `encoding.md` and no `LEDGER.md`. There are no §7 check numbers, no §4 lies list
and no §5 misconception to check against. The checks below come from three places:
- the HANDOFF thesis: ∂L/∂q = βg·k, so the gradient crest sits ON the forward crest when g > 0 (V₂, V₃) and λ/2 OFF it when g < 0 (V₁);
- the sheet's own colophon: L = Σ(Z−V₁)²/2, λ = 3 mm, d = 10λ, β = 1;
- textbook attention backprop: g_j = ∂L/∂s_j = a_j·δ·(V_j − Z) with δ = Z − V₁; ∂L/∂q = β Σ g_j k_j; ∂L/∂k_j = β g_j q.

All vectors were recovered from the gcode polylines: rows Z, V₁ and ∂L/∂Z, and the V₁/V₂/V₃ packets inside the field.
Context: Juan's FEEDBACK (2026-09-28 23:39) asks to keep the r01/v13 design. This thesis round departs from it. That is not a science grade, but the lead should know.

## Check numbers
| quantity | dossier | recomputed / expected | measured on sheet | OK? |
|---|---|---|---|---|
| λ (black crest pitch, both sources) | — (colophon 3 mm) | 3.000 mm | radii m·3.000 ± 0.003 mm, m = 1…24, about both centres | OK |
| source separation d | — (colophon 10λ) | 30.00 mm | Q (96.0,156.1) to K (123.4,143.9) = 29.993 mm = 9.998 λ | OK |
| packet carrier wavelength | — | = λ | Q 3.02 · K 3.02 · V₁ row 3.00 · V₂/V₃/V₁-patch 2.98 mm | OK |
| drawn Q vs K packet | — | — | identical (corr 1.000, amplitude 4.63 mm both) | note |
| ∂L/∂Z row = Z − V₁ | — | coefficient 1, residual 0 | coefficient 1.0000, relative residual 0.28 % (rows at y 56.0 / 42.0 / 28.0, x 54.4–81.6) | OK |
| V₁ patch = V₁ target row | — | same vector | corr 0.99996 over x-window 2.2–97.8 %, y-scale 1/2.173 | OK |
| V₁+V₂+V₃ | — | — | ‖ΣV‖/‖V₁‖ = 0.013 (three 120° phase-shifted packets; Gram off-diagonal −0.50) | note |
| A implied by Z = AV (on the simplex) | — | a_j ≥ 0, Σ = 1 | a = [0.416, 0.327, 0.257], residual 3.4 %; log-spacing 0.242/0.242 → s = [+0.242, 0, −0.242] + c | OK (implicit only) |
| sign of g_j = a_j δ·(V_j − Z) | — (HANDOFF: g₁<0, g₂,g₃>0) | g₁ = −a₁‖δ‖² < 0 always | g/‖δ‖² = [−0.416, +0.251, +0.165], Σ = 0 | OK |
| ∂L/∂Q crests (crimson, on K's rings) | — | V₂, V₃: 0 λ; V₁: 0.5 λ | V₂: 27 arcs, offset −0.001 λ · V₃: 12 arcs, 0.000 λ · V₁: 15 of 16 arcs at 0.500 λ (r_K 25.5–55.5); 1 arc at 0.000 λ (r_K 60.0, (144–146, 200)) | OK / 1 stray |
| ∂L/∂K crests (blue, on Q's rings) | — | same rule | V₂: 22 arcs, 0.000 λ · V₃: 7, −0.001 λ · V₁: 21 of 23 at 0.500 λ (r_Q 31.5–61.5); 2 arcs at 0.000 λ (r_Q 66.0, (153,188) and (145,199)) | OK / 2 stray |
| "recoloured" vs "interleaved" | — | g>0: black replaced; g<0: black kept, colour between | V₂/V₃: ≤ 4 % of colour ink has a same-centre black ring under it. V₁: black kept, colour sits 1.50 mm (λ/2) from it | OK |
| gradient magnitude \|g\| ratio V₁:V₂:V₃ | — | 2.52 : 1.52 : 1 | patch ink crimson 443 : 353 : 182 mm = 2.44 : 1.94 : 1 · blue 443 : 342 : 151 = 2.93 : 2.26 : 1 | ordinal only |
| A from patch placement (fringe phase at patch centre, β = 1) | — | should give [0.416, 0.327, 0.257] | cos 2πΔr/λ = [0.557, 0.495, −0.643] → softmax [0.446, 0.419, 0.134] | NO |
| L = Σ(Z−V₁)²/2 | 1.365 (colophon) | no units or dimension on the sheet | ½·mean(δ²) in drawn mm = 1.25 (full row), 1.31 (window). Not recomputable | UNVERIFIABLE |
| one step: L 1.365 → 1.198 | colophon | needs η and the updated variable | neither is on the sheet | UNVERIFIABLE |
| "47536 tokens" | colophon | — | no quantity on the sheet corresponds to it. There are 3 tokens | UNVERIFIABLE |
| crossing-guard gaps in black rings | — | should not target resonance | 13–14 % of ring samples inside the other disk are gaps; 38–40 % of them are near constructive phase vs 35 % baseline | ~clean (slight bias) |
| sheet bounds (A4 210×297) | — | inside margin | x 10.0–200.0, y 12.0–285.0 | OK |
| HANDOFF plot stats | 585 cycles · 11.35 m · 3.99 m | — | 585 strokes · draw 11.352 m · travel 4.038 m (preview) | OK (travel +1 %) |

## Lies list  (no dossier §4; derived)
| item | status |
|---|---|
| Gradient-as-phase sign rule (g>0 on crest, g<0 λ/2 off) | clean. It is exact to 0.001 λ on 104 of 107 gradient arcs. **VIOLATED (minor)** on the 3 edge arcs of the g<0 patch V₁, which are on-crest: crimson r_K 60.0 at (144.4–145.8, 199.6–200.1); blue r_Q 66.0 at (153–154, 188) and (145–146, 199). About 8 mm, ~1 % of V₁'s colour ink. |
| Subtitle "the backward pass is the same wave, half a wavelength over" (x ≈ 48–145, y ≈ 266) | **VIOLATED (caption).** Only V₁ (g<0) is half a wavelength over. V₂ and V₃, 2 of 3 patches and 61 % of the gradient arcs, are at 0 offset. The caption states the exception as the rule. |
| Pen swap (∂L/∂Q crimson drawn on K's rings; ∂L/∂K blue on Q's rings) | clean. ∂L/∂q = βg·k and ∂L/∂k = βg·q hold, and the geometry follows the source vector. |
| ∂L/∂Z = Z − V₁ | clean (residual 0.28 %). |
| Z = AV | clean. Z is a positive convex mix of the drawn V's (residual 3.4 %). A itself is not drawn anywhere. |
| "Attention as resonance": field placement selects the V's | **VIOLATED (implicit).** Softmax of the interference phase at the three patch centres gives [0.446, 0.419, 0.134]. The weights Z actually uses are [0.416, 0.327, 0.257]. Only one K source is drawn for three tokens with different scores, so the sheet has no source for s_j. |
| Gradient magnitude | not lying, but not encoded quantitatively. The ordering V₁ > V₂ > V₃ is right. V₂ is over-inked by 28 % (crimson) and 49 % (blue) relative to \|g\|. |
| Colophon numbers (L 1.365 → 1.198, 47536 tokens) | **UNVERIFIABLE.** They are stated as measurements, but no units, η, dimension or token definition appears on the sheet. |
| r02 violations (misplaced A-beads, decorative green fold, 1.31 mm seam break) | gone. |

## Scores
- truth: **7**. The core mechanism is right and drawn exactly: the sign of g_j, the λ/2 phase flip, ∂L/∂Z = Z − V₁, the pen swap, λ and d. Three things pull it down. The subtitle generalises the g<0 case to the whole backward pass. Three stray on-crest arcs sit in the g<0 patch. The field placement that the title calls "resonance" does not produce the attention weights the sheet uses, and the colophon numbers cannot be checked.
- encoding fidelity: **6**. The phase channel is exact (±0.001 λ). A has no channel: it appears only implicitly in Z's shape, and the one K source cannot give three scores. \|g\| is ordinal only (2.44–2.93 : 1.94–2.26 : 1 vs 2.52 : 1.52 : 1).
- insight legibility: **6**. Q, K, V₁–V₃, Z, V₁-target and ∂L/∂Z are now labelled, a big step up from r02's four unlabelled sources. But the ∂L/∂Q and ∂L/∂K crest families carry no label. The sign rule and the g values are nowhere on the sheet. A stranger sees three coloured patches, one striped differently, and a caption telling them all three are half a wavelength over.
- **VERDICT: FAIL**

## Mandates
1. **Caption and sign key (subtitle y ≈ 266, patches V₁ (133.3,183.3), V₂ (83.3,120.2), V₃ (118.8,106.5)).** Measured: the subtitle says the backward pass is "half a wavelength over", but the offsets are 0.000 λ at V₂ (27 crimson + 22 blue arcs) and V₃ (12 + 7), and 0.500 λ only at V₁. There are also 3 on-crest arcs inside V₁ (crimson r_K 60.0 at (145,200); blue r_Q 66.0 at (153,188) and (145,199)). Expected:
   - the caption states the rule (g > 0 → on the crest, g < 0 → λ/2 over);
   - each patch carries its sign or value, g/‖Z−V₁‖² = −0.416 / +0.251 / +0.165;
   - the two gradient families are labelled ∂L/∂Q (crimson) and ∂L/∂K (blue) at the patches;
   - all V₁ arcs sit at 0.500 λ, with 0 stray on-crest arcs.
2. **Source of the attention weights (field patches and the single K at (123.4,143.9)).** Measured: A is not drawn. The weights Z actually uses are [0.416, 0.327, 0.257], i.e. s = [+0.242, 0, −0.242]. The plate's own resonance reading, softmax(β·cos 2πΔr/λ) at the patch centres, gives [0.446, 0.419, 0.134]. Only one key source exists for three tokens. Expected, one of two:
   - place the patches so that the interference phase at each centre reproduces s (Δs = 0.242 between neighbours);
   - draw the three keys or the three weights, e.g. a_j beside each V_j label.
   Either way, "attention as resonance" should be something you can read off the sheet.
3. **Gradient magnitude and the colophon (patches; colophon at x ≈ 123–195, y ≈ 30–37).** Measured: the patch ink ratios V₁:V₂:V₃ are 2.44:1.94:1 (crimson) and 2.93:2.26:1 (blue), against \|g\| = 2.52:1.52:1. "L 1.365 → 1.198" and "47536 tokens" have no recomputable source on the sheet: ½·mean((Z−V₁)²) in drawn mm is 1.25 (row) / 1.31 (window), and there are 3 tokens. Expected:
   - patch extent (arc count × arc length) ∝ \|g\| to within ±10 %, or a sheet note that the patches are sign-only;
   - the colophon states units, dimension and η so that 1.365 and 1.198 can be recomputed, and "47536 tokens" is explained or removed.

## Follow-up on open mandates
No LEDGER.md exists. These rows track the r02 science mandates (rounds/r02/critique-science.md).
| id | status | evidence |
|---|---|---|
| r02-S1 attention beads misplaced / unequal with one key | PARTIAL | The beads are gone, so no false A is drawn. Three V tokens now exist with a valid implied softmax [0.416, 0.327, 0.257]. But A is still not drawn, still only one K source exists, and placement does not reproduce A (mandate 2). |
| r02-S2 seam phase undeclared (1.31 mm, opposite signs) | FIXED | The offsets are now declared and exact: 0.000 ± 0.001 λ (g>0) and 0.500 λ (g<0) on 104 of 107 arcs, the same for both families. The 3 stray edge arcs are carried in mandate 1. |
| r02-S3 channel identity / decorative green fold | PARTIAL | Q, K, V₁–V₃, Z = AV, V₁ and ∂L/∂Z are labelled. Green now carries Z and ∂L/∂Z, and ∂L/∂Z = Z − V₁ holds to 0.28 %. The ∂L/∂Q and ∂L/∂K crests are still unlabelled (mandate 1). |
| regressions | none | Every truth that held in r02 still holds: the pen swap, λ constant, sources inside bounds. |
