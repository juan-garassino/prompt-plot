# Science critique — convolutions r02 · machine learning (convolutional networks) · 2026-09-28
render: gallery/studio/convolutions/current/pp_convolutions_real-kernel_v9.png (gcode: gallery/studio/convolutions/current/pp_convolutions_real-kernel_v9.gcode, 47,743 cmds, 1,446 pen-down strokes: c0 682 · c1 382 · c2 318 · c3 64)

**Process finding:** `studio/convolutions/` has **no `dossier.md`, no `encoding.md`, no `LEDGER.md`**.
There is no §7 check-number list and no §4 lies list to grade against. Every check number below
was derived from first principles plus the pen meanings in HANDOFF, then measured on the gcode.
The studio process requires a dossier, and this round has none. That gap is a finding in its own right.

## Check numbers
quantity | dossier | recomputed | measured on sheet | OK?
---|---|---|---|---
Weight channel: dot AREA ∝ \|w\| vs radius ∝ \|w\| | — | zero-sum kernels must balance to 0 under the true encoding | ridge Σw/Σ\|w\|: **0.000 under area**, −0.34 under radius. All 6 zero-sum bank kernels ≤ 0.006, all 3 blurs = 1.000 | OK (area is honest)
Main-row kernel size / pitch | — | 5×5 | 5×5 at 3.50 mm pitch, all 5 panels | OK
blur1 = blur2 Gaussian σ (px) | — | from neighbour area ratio | ratio 0.614 → σ = 1.01 | OK
blur3 σ (px) | — | — | ratio 0.748 → **σ = 1.31**. It carries the same "blur" label as σ = 1.01 | minor
"ridge" kernel | — | zero-sum centre-surround | +centre, + orthogonal 0.29, diagonal −0.02, ring −0.15…−0.16, Σ = 0.000. This is a **negated LoG** (isotropic blob/centre-surround), not an oriented ridge filter | minor naming
Kernel bank (9) | — | identities | ∂x-DoG, ∂y-DoG (5 true zeros each), LoG, Gaussians σ small/med/large, even Gabor 0° / +45° / −45° (DC removed, Σ ≤ 0.006) | OK
Theoretical RF per layer, 1+L(k−1) | — | 5, 9, 13, 17, 21 | dot counts per row 5, 9, 13, 17, 21. Outer dashed envelope at ±2.00L px (L=2.02 → 4.00, L=4.04 → 8.04, L=4.91 → 9.79) | OK
stride 1 / padding 2 / dilation 1 | — | p=(k−1)/2=2 gives "same" | as stated | OK
RF row weights = effective RF of the drawn stack (backward from y: K5, K5∗K4, …) | — | signed product, L=5 centre row offsets 0..5: **1, 0.738, 0.203, −0.158, −0.187, −0.061** | drawn (area-normalised): **1, 0.933, 0.733, +0.483, +0.276, +0.127**. It matches the **\|K\|-chain** (1, 0.921, 0.720, 0.475, 0.263, 0.121) to ≤ 0.013 at every row. L=2 offset 3: true **−0.19**, drawn **+0.20** | **VIOLATED**
ERF growth law | — | ∝ √L | area-std per row 1.13, 1.63, 1.93, 2.32, 2.62 px ≈ 1.13√L. Middle dashed curve ≈ 1.45√L (3.24 px at L=5). Inner solid ≈ 0.75√L (1.65 px at L=5). Neither curve is labelled | shape OK, unlabelled
Y = σ(blur∘ridge∘blur∘ridge∘blur ∗ X) | — | simulated on an X distance-field proxy using the kernels read off the sheet | best IoU with drawn Y outer contour **0.81–0.84 at 3.0–3.75 mm/px**. At the 1.5 mm/px implied by the X patch: **0.53**, worse than the no-convolution baseline 0.68 | OK at ~3.3 mm/px, not at the patch scale
Receptive patch on X (kernel footprint) | — | 5 taps × field pitch (~3.3 mm, which matches the RF-diagram pitch 3.30 mm) ≈ 16.5 mm | box 41.2–48.7 × 129.2–136.8 = **7.5 mm**, 5×5 dots at **1.5 mm** pitch | **VIOLATED (~2.2× too small)**
Per-layer thumbnails | — | blur keeps shape, ridge thins it | shape IoU vs X / vs Y: L1 0.98/0.61, L2 0.56/0.79, L3 0.65/0.89, L4 0.34/0.57, L5 0.54/**0.91** | OK
Feature maps edge / blur / gabor vs the bank kernels on X | — | simulated | largest red region IoU: edge 0.79, blur 0.93, gabor 0.58 (proxy-limited). Edge + left / − right polarity is correct for the drawn ∂x kernel | OK

## Lies list (self-derived; there is no dossier §4)
item | status
---|---
Dot area inflates weights (radius ∝ w) | clean: area ∝ \|w\| exactly
Kernel sign mislabelled (red ≠ +) | clean: every zero-sum kernel balances
Theoretical RF miscounted | clean: 5/9/13/17/21 and ±2L envelope exact
RF weights shown unsigned in a network whose function depends on the negative surround | **VIOLATED**: receptive-field panel (x 115–182, y 27–84). All-black dots draw the \|w\|-path-count, which hides the negative ring at offsets 3–5
Kernel footprint on X matches the conv scale | **VIOLATED**: X patch 7.5 mm vs ~16.5 mm implied by Y and by the RF pitch
Output Y is a real computation, not a hand-drawn "Y" | clean (IoU 0.81–0.84)
Zero weights | the 5 true zeros in ∂x/∂y are drawn as tiny **black** dots. HANDOFF gives black no weight meaning, so these are uncaptioned

## Scores
truth **6** · fidelity **6** · legibility **6** · VERDICT: **FAIL**

## Mandates
1. **Receptive-field panel (x 115–182, y 27–84): draw the signed effective RF.** Row L must be the product K5∗…∗K(6−L) in red/blue, not black \|K\|-chain magnitudes. L=5 centre row, offsets 0..5: expected areas 1, 0.738, 0.203, **−0.158, −0.187, −0.061**; measured 1, 0.933, 0.733, +0.483, +0.276, +0.127. At L=2 offset 3: expected −0.19, measured +0.20. As drawn, the centre-surround stack appears to have a Gaussian, all-positive receptive field.
2. **Receptive patch on X (box 41.2–48.7 × 129.2–136.8): fix the scale.** The patch is 7.5 mm with 1.5 mm tap pitch. The Y it feeds is reproduced only at 3.0–3.75 mm/px (IoU 0.81–0.84 vs 0.53 at 1.5 mm), and the RF diagram uses 3.30 mm. Either draw the patch at ~5 × 3.3 = 16.5 mm with 3.3 mm taps, or recompute X→Y at 1.5 mm/px so all three agree.
3. **Put the encoding on the sheet.** There is no key for red = +w, blue = −w, dot area ∝ \|w\|, or black = 0. The two ERF envelopes are unlabelled: inner solid 1.65 px and middle dashed 3.24 px at L=5, against the ±10 px theoretical edge, i.e. ERF ≈ 1.45√L vs TRF 1+4L, which is the misconception this panel exists to correct. σ(·) sits once at x≈170, between kernels 4 and 5, while the olive thumbnails imply it acts after every layer. Label the √L envelope next to the "21" row, add a sign/area key, and place σ(·) so it reads as per-layer (main-row header, y≈150).

## Follow-up on open mandates
id | status | evidence
---|---|---
— | n/a | pass 1: no LEDGER.md exists for convolutions
