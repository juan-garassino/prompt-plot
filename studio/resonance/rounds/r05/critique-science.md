# Science critique — resonance r05 · machine learning (transformer attention as wave interference) · 2026-09-28
render: gallery/studio/resonance/current/pp_resonance_benchmark_kept_v7.png (+ .gcode, 48,628 cmds, 1,960 pen-down strokes, 6 colour layers)

Pass 1 (cold). `studio/resonance/` has **no dossier.md, no encoding.md, no LEDGER.md**: there are no
§7 check numbers, no §4 lies list and no §5 misconception on record. That is a finding in itself.
The claim set checked below is the plate's own caption/equations plus the "science it encodes"
paragraph of `studio/resonance/DESCRIPTION.md` and the HANDOFF pen map. Every value was measured
from the parsed `.gcode` (pen-down strokes split by `; color=N`).

## Check numbers   quantity | claimed | recomputed | measured on sheet | OK?
| quantity | claimed | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| source centres | symmetric about the centreline | u=0.40/0.60 → x 84/126 | (83.835, 166.285) and (126.165, 166.285). Midpoint x = 105.000 | OK |
| source separation d | d = 35·L | 35 × 1.2096 = 42.34 | 42.330 mm, so d/Lx = 34.996 | OK |
| crest pitch across (Lx) | 1.21 mm | — | ring rx = m × 1.2096 (m=12 → 14.515 mm) | OK |
| crest pitch down (Ly) | 1.41 mm | 1.21 × 1.167 = 1.411 | ry/rx = 16.935/14.515 = **1.1667** | matches the claim, but the geometry is wrong (see lies #1) |
| crest m meets 35−m on the axis | yes | m + n = 35 when d = 35L | holds by construction (d/L = 34.996) | OK |
| solid crests | 1–21 | — | **1–28**: full rings for m ≤ 12, then m = 13–28 only as inner arcs clipped to the lens x 92–118 | claim ≠ sheet |
| dotted crests | 22–51 | loci r = mL, same eccentricity as the rings | **none**. The dotted rings are ellipses with a = 25.72 / 32.16 / 38.9 mm, **b/a = 0.700** (rings are 1.167), and a/L = 21.26 / 26.59 / 32.1, which are not integers | VIOLATED |
| dot field ∝ \|A\| | size = 1.1 + 22·\|A\| | A = Σ cos(k rᵢ)/√rᵢ | 50 off-axis black dots, 0.61–2.16 mm. corr(size, \|A\|) = 0.09 (every variant tried, stretched or not and L = 1.21/1.30/1.41, gives \|r\| ≤ 0.19). Mean normalised \|A\| is 0.56 at the dots vs 0.41 at random points | VIOLATED (decorative) |
| key count = value count | n_K = n_V | attention needs one V row per K row | K = **5** rows, V = **3** rows | VIOLATED |
| softmax entries = keys | one weight per key, Σ = 1 | 5 | **6** solid peaks (+3 dotted ghosts) at x 76.2 / 90.4 / 97.4 / 104.6 / 119.2 / 132.6. Heights normalised 0.127 / 0.252 / 0.066 / 0.177 / 0.251 / 0.127, which is mirror-symmetric | VIOLATED |
| softmax derived from Q·Kᵀ | yes (caption) | overlap of the drawn packets on the block coordinate, row-softmax: e.g. q3 → [0.04, 0.05, **0.83**, 0.04, 0.04] | the sheet's 6-peak symmetric row matches no query row | VIOLATED |
| Z = AV amplitude | \|Z\| ≤ max_j \|V_j\| (Σa = 1, a ≥ 0) | ≤ 5.54 mm | Z peak **13.44 mm** (2.43×). V rows 5.54 / 4.93 / 4.35 | VIOLATED |
| Z = AV width (d_v) | width(Z) = width(V) | 42.3 mm | Z axis 28.6–96.9 = **68.3 mm** (1.61×) | VIOLATED |
| MoE output Y width (d_model preserved) | = width(Z) | 68.3 mm | Y 162.1–188.2 = **26.1 mm** | VIOLATED |
| top-2 of 5 experts | 2 solid / 3 ghost | 2/5 | 2 solid packet lanes (y 87.4, 60.2), 3 dotted lanes | OK |
| plot stats | 1,960 cycles · 9.97 m draw | — | 1,960 strokes · 9,972 mm draw (per layer 643/1300/781/1313/1078/4857) | OK |

## Lies list   item | clean / VIOLATED (where)
(There is no dossier §4. These are the standard lies, checked one by one.)
1. **Lying geometry (hero): VIOLATED.** In an isotropic medium the crest loci of a point source are circles. Here every crest is an ellipse with ry/rx = 1.1667 (ring m=12: 14.515 × 16.935 mm, centred (83.8, 166.3)). The caption presents it as a real Huygens figure, not an anisotropic medium.
2. **Fake data continuation (hero surround): VIOLATED.** The three dotted ellipses per source (x 44–86 / 124–165, y 139–194) look like the wave field carrying on outward. They are not crests: their eccentricity is the opposite of the rings (0.700 vs 1.167) and their radii are not multiples of L. At the poles the innermost one (b = 18.01) sits 1.07 mm outside crest 12 (ry 16.94), while at the equator it sits 11.2 mm outside.
3. **Decorative marks posing as data: VIOLATED.** 50 black dots of 0.6–2.2 mm are scattered over the rings with no relation to \|A\| (r = 0.09). The benchmark-kept brief said to remove them, and they are still there.
4. **Broken count / shape: VIOLATED.** There are 5 K rows, 3 V rows, 6 softmax peaks and 1 Z row. A, K and V must share the key axis.
5. **Invented values: VIOLATED.** The softmax heights come from no computation on the sheet: they are mirror-symmetric, there are 6 of them, and they do not match any Q·Kᵀ row.
6. **Broken scale (Z, Y): VIOLATED.** Z is 2.43× taller than any V (impossible for a convex combination) and 1.61× wider. Y is 0.38× the width of Z.
7. **Wiring lie: VIOLATED.** V's only outgoing connector (gold, 12 dashes, from (184.2, 109.9)) ends at **(164.0, 77.2)**, on the Y/MoE-output node (Y starts at x 162.1), 67 mm from Z. Of the five softmax→ links, only one lands on Z ((88.2, 75.3), inside Z's axis 28.6–96.9). Two land inside the MoE ghost lane ((115.3, 75.2), (133.6, 75.2)) and two stop in mid-air at y 85.1. Those A links are also drawn in pen 0, which the HANDOFF assigns to V: a channel mis-assignment, because A is black.
8. **Pen map vs HANDOFF: clean otherwise.** Q = crimson ×5, K = blue ×5, V = gold ×3, Z = green, MoE/Y = violet and field/softmax/∂L/∂A = black all match. The green dotted frame in the preview is not in the gcode (green bbox is 18–128 × 15–92).
9. **Craft carry-over from the open REWORK (FEEDBACK 2026-09-28): not fixed.** "Dotted" lines are still 0.50 mm micro-dashes at a **2.76 mm** pitch (∂L rails: x 27.6, 30.4, 33.1 …), and the fans and links are 1.2 mm dashes at 3.5–3.7 mm pitch. Juan asked for round dots at about 1 mm pitch, and the pitch is now coarser than v13's 2.22 mm. This is a legibility issue because dotted lines carry "ghost / secondary" meaning here.

## Scores
- truth **5**. The two-source crest lattice is correct in its topology (d = 35.00 L, crests m and 35−m kiss on the axis), but it is stretched 16.7 %. The attention algebra drawn around it is inconsistent: 5 keys, 3 values, 6 weights, Z larger than any V, and V wired to Y.
- fidelity **4**. The dotted "outer crests", the scatter dots and the softmax heights are all decorative marks presented as data. The Z and Y scales lie.
- legibility **5**. A stranger reads "two waves interfering", and the Q/K funnel into the hero works. But the jump from Q·K to interference is asserted, not shown: the hero's L = 1.21 mm matches no Q/K carrier, whose peak spacing is 1.8–2.9 mm. The softmax row cannot be traced back to anything. There is no misconception correction because §5 does not exist.
- **VERDICT: FAIL**

## Mandates
1. **Z = AV must hold in value and in wiring (lower half).** Measured: Z peak amplitude 13.44 mm and width 68.3 mm (x 28.6–96.9, y 75), against V rows of 5.54 / 4.93 / 4.35 mm amplitude and 42.3 mm width. V's connector ends at (164.0, 77.2) on Y. Expected: draw Z as Σ_j a_j·V_j sampled on V's 42.3 mm coordinate, so width(Z) = 42.3 mm and \|Z\| ≤ 5.54 mm at every x, and do not scale it up. The V connector must terminate on Z. All softmax→ links must terminate on Z's axis, not at (115.3, 75.2), (133.6, 75.2) or in mid-air at y 85.1, and they must be drawn in black (A), not in pen 0. If Y is kept, it must have the same width as Z.
2. **One key axis: n_K = n_V = n_softmax, weights computed (softmax row y 112–129, V block y 121–135).** Measured: 5 K rows, 3 V rows, 6 solid peaks plus 3 ghosts, with mirror-symmetric heights 0.127 / 0.252 / 0.066 / 0.177 / 0.251 / 0.127. Expected: 5 V rows (one per K row, same order), exactly 5 softmax peaks, and peak heights = softmax(q_i·k_j/√d) for one named query row computed from the drawn packets, with Σ = 1.000 stated. For example, the overlap on the block coordinate gives q3 → [0.04, 0.05, 0.83, 0.04, 0.04]. Mark the chosen query row on the Q block.
3. **Hero crests are circles and only crests are drawn (centre, sources at (83.8, 166.3) and (126.2, 166.3)).** Measured: ring ry/rx = 1.1667. The dotted outer rings are ellipses with b/a = 0.700 at a = 25.72 / 32.16 / 38.9 mm (21.26 / 26.59 / 32.1 L). 50 scatter dots have corr(size, \|A\|) = 0.09. Expected: ry/rx = 1.000 (one L; d = 35 L still holds). Any dotted continuation must be crest loci r = m·L for integer m with that same eccentricity. Delete the 50 scatter dots, or size them from \|A\| with r ≥ 0.9 so that dot size is an honest amplitude channel.

## Follow-up on open mandates
No LEDGER.md exists for resonance, so there are no open S* mandates to follow up. The open Juan REWORK (dotted lines) is measured **NOT FIXED** (see lies #9).
