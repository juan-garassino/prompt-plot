# Science critique — resonance-backprop r02 · machine learning (attention fwd+bwd as wave interference) · 2026-09-29
render: gallery/studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.png (gcode: gallery/studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.gcode, 17 232 cmds, 334 pen-down strokes: pen0 4 · pen1 127 · pen2 121 · pen3 1 · pen4 81)

Pass 1 (no LEDGER.md exists). **Dossier finding:** `studio/resonance-backprop/` has no `dossier.md`,
no `encoding.md` and no `LEDGER.md`, so there are no §7 check numbers, §4 lies list or §5 misconception
to verify against. The checks below are derived from HANDOFF.md (pen meanings), DESCRIPTION.md
(stated science: Huygens crest loci r = m·λ, "the fold" = the gradient field is the same field read
backwards), and textbook attention backprop (∂L/∂Q = ∂L/∂S·K/√d_k, ∂L/∂K = (∂L/∂S)ᵀ·Q/√d_k).
Context: Juan's FEEDBACK of 2026-09-28 23:39, which came after this render, says to keep the r01/v13 design.
That makes "the fold" direction moot, but it does not change the grades below.

## Check numbers
| quantity | dossier | recomputed / expected | measured on sheet | OK? |
|---|---|---|---|---|
| crest pitch λ (all 4 families) | — (r01 desc: L≈1.04) | constant within a family | 3.000 mm, all four families, residual ≤0.007 mm | OK |
| source centres | — | Q, K above the fold; ∂L/∂Q, ∂L/∂K mirrored | Q (51.80,157.50) · K (124.61,210.40) · ∂L/∂Q (51.80,139.50) · ∂L/∂K (124.61,86.60) | OK |
| mirror about fold y=148.5 | — | dy error 0 | ≤0.001 mm (both pairs), dx 0.000 | OK |
| Q–K separation | — | — | 90.00 mm = 30.00 λ (61 antinodal hyperbolae) | OK |
| pen of ∂L/∂Q / ∂L/∂K | — | ∂L/∂Q is built from K → K's pen; ∂L/∂K from Q → Q's pen | ∂L/∂Q blue (K pen), ∂L/∂K crimson (Q pen) | OK |
| seam phase (fwd crest vs bwd crest at the fold) | — | 0 (exact twin) or λ/2 = 1.50 mm (sign-inverted twin), same for both pairs | Q→∂L/∂Q −1.31 mm, K→∂L/∂K +1.31 mm (0.437 λ, 157°, opposite signs) | NO |
| relative Q–K phase (sets where the fringes fall) | — | the same above and below if it is a twin | upper 0.06 mm (0.02 λ), lower 0.44 mm (0.147 λ) | NO |
| where Q and K fields overlap on the fold | — | attention should sit here | x 62.8–135.9 mm (upper), 65.2–137.6 (lower) | — |
| attention beads (pen 0) position | — | inside x 62.8–135.9 | x 32.5, 36.5, 40.5, 44.5 @ y 148.5; 101–111 mm from K, whose outermost crest is 87.5 mm | NO |
| attention bead weights | — | one query, one key drawn → softmax over 1 key = [1.0] | r 0.856/1.344/1.704/1.500 mm → area share 0.095/0.235/0.377/0.293 (4 unequal entries, 3 keys not drawn) | NO |
| amplitude ∝ 1/√r (2-D Huygens) | — | a(84.6)/a(24.6) = 0.54; a(12.7)/a(3.6) = 0.53 | passes 3 (r<10) · 2 (12.7–21.7) · 1 (r≥24.6, flat to 87.5): 1.00 and 0.67 | PARTIAL |
| bwd amplitude vs fwd | — | ∂L/∂Q magnitude set by ∂L/∂S, not equal to Q | the same pass schedule and extent as forward (asserted equal) | UNSUPPORTED |
| sheet bounds (A4 210×297) | — | inside the margin | x 13.0–200.0, y 10.0–287.0 | OK |

## Lies list  (no dossier §4; derived)
| item | status |
|---|---|
| Colour swap in the backward half (∂L/∂Q in K's pen, ∂L/∂K in Q's pen) | clean. This is the sheet's one true backprop fact. |
| "The gradient is the same field read backwards" (exact twin) | VIOLATED, partial. Geometry mirrors to 0.001 mm, but every crest breaks at the fold y=148.5 by 1.31 mm, and the lower fringe pattern is shifted 0.127 λ relative to the mirror of the upper one. |
| Goldenrod beads = attention A | VIOLATED. They sit at x 32.5–44.5 on the fold, outside K's field, so the drawing's own QKᵀ is zero there. They show 4 unequal weights with one key drawn. Pen 0 is also named "V", which conflates V with A. |
| Green fold = Z / loss line | VIOLATED (decorative). It is a 3-pass rule, y 148.2/148.5/148.8, x 15–200. It carries no value of Z = AV or of L. V and ∂L/∂V have no wave anywhere. |
| Crossing-guard cull posing as structure | VIOLATED (minor). 1.9–4.1 % of ring arc is removed, 90–96 % of it at crossing angle <25°, in the Q–K lens. Gaps sit nearer crest coincidence than chance (mean \|Δφ/λ−½\| 0.36 vs 0.25 baseline). That removes ink at the constructive crossings, which are the resonance the plate is about. Only ~40 % of those gaps are covered by the other pen. |
| Amplitude decay | VIOLATED (partial). It is quantised 3/2/1 passes and flat from 24.6 to 87.5 mm, where the true 1/√r falls by ×0.54. |
| r01 packet braids / black comb lozenge | clean. Both are gone. The closest crest spacing is set by two 3 mm families. |
| Rail direction | clean-ish. No arrowheads. "forward pass" (y 208–228) and "backward pass" (y 69–90) name the halves but not the flow. |

## Scores
- truth: **5**. The mirror geometry and the colour swap are right. But the attention beads sit where QKᵀ = 0 on the sheet and are unequal with one key. The seam is a 157° break that is neither a twin nor an inversion. Z, V and ∂L/∂V are claimed in the pen key but absent from the sheet.
- encoding fidelity: **5**. The bead areas are anchored to nothing drawn. The green line is a rule posing as Z. Amplitude is flat over 63 mm of radius. The backward amplitude is asserted equal to the forward one. The cull deletes ink at constructive crossings.
- insight legibility: **4**. There are no Q, K, ∂L/∂Q, ∂L/∂K, A or V labels. A stranger sees two ring pairs, a green rule and four yellow dots. The swap, the only real insight, is invisible without a key. The misconception correction is undefined (no §5).
- **VERDICT: FAIL**

## Mandates
1. **Attention beads (pen 0).** Measured at x 32.5/36.5/40.5/44.5, y 148.5, 101–111 mm from K, whose outermost crest is at 87.5 mm, with area share 0.095/0.235/0.377/0.293. Expected: they sit inside the fold's Q–K overlap (x 62.8–135.9 mm, y 148.5), and their areas are computed from the drawn field (e.g. crest-coincidence intensity at the bead points, then softmax). Draw ≥2 key sources so a softmax over several keys exists. With the single K on the sheet, the only true weight is 1.0.
2. **Seam phase at the fold (y = 148.5, whole width x 21–200).** Measured: Q→∂L/∂Q crests offset −1.31 mm and K→∂L/∂K +1.31 mm (0.437 λ, opposite signs). The Q–K relative phase is 0.06 mm above and 0.44 mm below. Expected: one declared, shared offset, either 0.00 mm (the twin) or 1.50 mm = λ/2 (a sign-inverted gradient), with the relative phase equal above and below so the lower fringes mirror the upper ones.
3. **Channel identity (legibility).** Measured: 0 of the 4 wave sources carry a label, and the only type is "forward pass"/"backward pass" on the rail at x 13–16. Expected: Q at (51.8,157.5), K at (124.6,210.4), ∂L/∂Q at (51.8,139.5) and ∂L/∂K at (124.6,86.6) each labelled beside its source dot, and A labelled at the beads. Then the one correct insight reads without a key: ∂L/∂Q is drawn in K's pen because it is made of K. Either give the green fold a quantity (Z or L) or stop claiming it as Z in the pen plan.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | pass 1; no LEDGER.md exists for this slug |
