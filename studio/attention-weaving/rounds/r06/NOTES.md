# attention-weaving r06 — iterate · parent: r04 · 2026-09-28

## Render

```bash
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r06/piece.py \
  --fn attention_weaving_iterate --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen \
  --out ~/Downloads/pp_attention_weaving_iterate_v16.png
```

- final: `~/Downloads/pp_attention_weaving_iterate_v16.png` / `.gcode`, seed 7. v13 is geometrically
  identical; v16 was re-rendered after the docstring edit so the shipped code is the code that drew it.
- other seeds: v14 = seed 3, v15 = seed 11.
- trail (all seed 7): v1 first topology · v2 κ-free DP, bend BR 1.0 (lanes through the title) ·
  v3–v5 V redesign (orthogonal → constant-depth arcs → compact reed) · v6–v7 K starts carried to
  the frame · v8 every lane exits right (KB 0.225) · v9 crown at bin 3 (rejected: storm lopsided)
  · v10 crown at bin 4 · v11 opaque hill · v12–v13 storm under-run merge + edge stubs.

## Mandate responses

| id | mandate | status |
|---|---|---|
| J1 | bring the bottom up to the top | **FIXED (claim).** The bottom now uses the top's grammar, point-mirrored. K tails leave the right frame above the wall and sweep over the Q fan into the slit. V tails leave one left-margin reed below the wall and sweep across the Z fan to the selvage. Every gold strand starts at a left reed tick and ends on the outermost green lane (the selvage), 0.8 mm off it. No gold piece is under 5 mm (measured min 5.01). 336/336 V×lane pairs cross exactly once, min 55.6°, median 56.3°. 0 V–V crossings. |
| J2 | smoother staircase, partition exact | **FIXED (kept).** One C¹ curve: the least-curvature exact-area histopolant, with a ramp condition (every step on the rising side ≥ 0.2 × the local slope of the bin-mean staircase), so it can neither ring into false humps nor pin a plateau. Area per bin is exact to 1.9e-13. Min height 3.1 mm. No knot discs. The hill is opaque. |
| A7 | V continuous strands from a left reed, ≥45°, one gap per crossing, merge under-runs, no gold < 5 mm, end on lane/reed | **FIXED.** Reed: 16 ticks at x = 10, y 167.6 → 128.6, 2.6 mm pitch, with `V` over the top tick. Consecutive V-under gaps with no V-over between them merge into one gap (32 merged gaps). 18 of 336 crossings (5.4 %) are forced to V-over to keep gold ≥ 5 mm. In each case |A_ij − 1/16| ≤ 0.035, and the one closest to uniform was chosen. |
| A8 | K starts at a top/right reed, no polyline elbows, every Z exit ticked | **FIXED.** Every K is carried back to the frame. It uses its own spiral line in (φ, ψ) where that reaches the frame above the wall. Otherwise it bends toward a ray lying strictly between the two Q streamlines that bracket its start, so the carried-back part crosses no Q. The sweep→drop elbow is a quadratic fillet in (φ, ψ); the map is conformal, so the turn is tangent-continuous on paper. 0 K–K crossings. All 22 Z exits are right-frame, each ticked (tick length ∝ ‖z_i‖). |
| A9 | clear the aperture; one doubled coloured line | **FIXED.** Cumulative curve, its disc and `1.000` are deleted. `Σa = 1` appears in the footer only. No K or V is double-passed any more. The principal crimson vertical is the only doubled coloured line, labelled `Q11 · ITS ROW IS THE HILL` at its top. The dotted equipotentials are deleted too (they crossed the throat and `SOFTMAX`). |
| A10 | strands pass under the hill ≥1 mm; labels clear | **FIXED.** The hill is opaque. Every Q and K stops 1.25 mm (1 mm paper + half a pen) above the top of its 1.2 mm band. Q re-emerges as green at the slit. No coloured line touches black ink in the slit box. Label halos cut strands at pad 0.9–1.3 mm. |
| A11 | labels anchored | **FIXED.** `K` mirrors `Q` (same y, flush to the opposite frame). `Z = AV` is on the TO ONE baseline, flush right at the outlet reeds. `SOFTMAX` sits on the wall's arm 1.9 mm right of the right jamb. `V` is at its reed mouth. |
| A12 | gold ≥ 15 mm above the `E`; lanes exit right only | **FIXED.** Lowest gold is y ≈ 103.8, 21 mm above the top of SUMS (82.4) and ≈ 45 mm above the `E`. 22/22 lanes exit the right frame (fold KB 0.33 → 0.225). |
| A13 | giant type stroke craft | **DEFERRED** to r07, as the ledger says. Type code is unchanged. |
| A14 | travel > draw | **DEFERRED / improved.** Travel 14.75 m vs draw 14.23 m (ratio 0.965; r04 was 17.3 / 16.1). |
| A15 | concept reads as a physics figure | **ARGUED** (ledger). With the chart furniture gone, the throat holds only strands and the hill, and the lower half is an over/under weave. |
| A16 | 5 pens | **ARGUED** (BRIEF specifies Q, K, V, Z, black). |
| A17 | depth undeclared; ellipses touch lanes | **FIXED.** Declared flat (Deco); occlusion is the only depth cue. The dotted ellipses are removed. |
| A18 | `lineage:` + canon in HANDOFF | **FIXED.** Canon: Deco, flat. Lineage: Anni Albers, *Black-White-Gold I* (1950), over/under as information. |
| S1 | 22 Q → 22 Z; K consumed | **FIXED.** 16 K strands end on the hill. 22 Q lanes cross the slit and continue as 22 Z = AV rows, one per query: z_i = Σ_j A_ij v_j, with the full 22×16 A at the same temperature (every row sums to 1 within 1.1e-16). Footer: `22 Q · 16 K → 22 Z`. **Flag for Juan:** this retires the BRIEF rule "strand count in = strand count out". |
| S2 | equal bins, height ∝ a, Q per bin = largest remainder of 22·a | **FIXED, with a widened slit.** 16 equal bins of **4.604 mm** (slit 73.67 mm, not 51.92). The slit is widened, never unequalised, until every adjacent pair keeps ≥ 0.90 mm where tightest. The fold squeezes the fan to κ ≈ 0.8, and each K streamline needs clearance. Bin-mean height ∝ a exactly: peak/median 4.17. Q per bin = [1,1,1,1,4,3,2,1,1,1,1,1,1,1,1,1] (Hamilton on 22·a). |
| S3 | exactly one K into each bin | **FIXED.** 16/16 K end over their own bin: at the bin's centre line, 0.75 mm above the hill's top pass. The 16 landings stand one bin (4.60 mm) apart. |
| S4 | captions true | **FIXED.** The printed `MIN PITCH 0.90 MM` is the measured minimum over every adjacent pair: lanes 0.904, slit 1.075, K drop↔Q 0.940, V↔V 1.077, K↔K 2.31. "SCORES CROSS" is dropped. `GOLD OVER GREEN WHERE a > 1/16` states the V encoding. 18 crossings (5.4 %) are forced by the 5 mm rule; those are disclosed here, not on the sheet. |
| S5 | no dossier/encoding | **DEFERRED** (process; the translator owns it). |
| S6 | hill has no A axis | **DEFERRED.** With equal bins the height is now ∝ a, so the 16 K landings at bin centres are the implicit x-axis. No tick is added to the throat (A9). |
| S7 | GPT-2 row identity | n/a (dropped in the ledger; r05 flavour not continued). |

## What changed from parent

- **The wall's topology.** r04 had 38 lanes (Q + K) in weight-sized clumps on unequal bins. Now 16 equal bins. K dies on the hill over its own bin. Only Q passes.
- **Lanes are placed in flow coordinates.** A K that lands high on the hill rides a streamline that meets the slit nearer the centre (by up to cosh φ). A dynamic program places each bin's Q lanes as at most two clumps inside the bin, subject to:
  - clear of every K streamline, with the true separation above the hill = slit separation × √(sinh²φ + sin²ψ)/sin ψ;
  - each adjacent pair at max(0.95, 0.91/κ(x)), where κ is the measured fold compression at that slit position.
  The slit is widened by bisection until the program is feasible.
- **Principal query.** Q11 is pinned to the lane 0.32 mm left of the centre line. Its drift is ≈ 1 mm over the 106 mm storm, and it is the only doubled line. The other 21 queries are **seriated** onto lanes (greedy + 2-opt on the Hamming distance of their "A_ij > 1/16" patterns: 142 → 86 transitions). Query order is free; it just makes the weave coherent.
- **Crown moved from bin 5 to bin 4** (4 keys dealt left instead of 5). This is a permutation of keys, so A is unchanged. It keeps the Q storm balanced while the slit stays at 73.7 mm (bin 3 → 68.9 mm, but lopsided; bin 5 → 82 mm).
- **Hill.** A ramp-constrained exact-area histopolant, solved once on unit bins and scaled. It is opaque.
- **Storm.** Q far field unchanged (asymptotic rays do not depend on c). K φ values are rescaled so every sweep keeps r04's semi-major axis on the wider aperture. The lowest K sweep start is lifted 0.018π → 0.050π so the carried-back starts spread along the right frame instead of hugging the wall. Merge rule: storm pieces ≥ 3 mm between under-gaps; 6 merges.
- **Drain.** Fold KB 0.33 → 0.225, BR 1.30 → 1.15, so all lanes exit right. V is rebuilt as constant-depth arcs from one compact reed, ending on the selvage. Green uses the same merge rule (24 lane merges; min green piece 3.16 mm).
- **Deleted.** Cumulative curve, `1.000`, all dotted equipotentials, the bin ticks (the K landings mark the bins), and all doubled K/V passes.

## Measurements / computations (seed 7, `piece.LAST_STATS`)

| claim | measured |
|---|---|
| Σa (drawn row) | 1.0000000000; all 22 rows of A sum to 1 within 1.1e-16 |
| a_max / H | 0.190 / 3.762 of 4.000 bits |
| equal bins | 16 × 4.604375 mm = 73.67 mm |
| area over bin j = a_j | max error 1.9e-13 (relative, on the drawn polyline's trapezoids) |
| bin-mean height peak/median | 4.17 (= a peak/median, exact on equal bins) |
| Q per bin (Hamilton, 22·a) | [1,1,1,1,4,3,2,1,1,1,1,1,1,1,1,1], Σ = 22 |
| K end in own bin | 16/16 bins hit, one K each |
| in / out | 22 Q + 16 K in → 22 Z out |
| min adjacent separation | 0.904 mm (lanes 6–7 at 102.0, 154.7); slit 1.075; K-drop↔Q 0.940; V↔V 1.077; K↔K 2.31 |
| Q×K crossings | 100 on sheet, min angle 26.0° (K13 × lane 21 at 217.7, 224.0, right frame); next lowest 32.4° |
| V×Z | 336/336 pairs cross once; min 55.6°, median 56.3° |
| forced V-over crossings | 18/336, all with \|A_ij − 1/16\| ≤ 0.035 |
| min pieces | gold 5.01 mm · green 3.16 mm · storm 2.35 mm (K8 at the top frame) · 2 sub-2 mm frame/halo stubs dropped |
| self-crossings | lane–lane 0 · V–V 0 · K–K 0 |
| lane exits | 22/22 right frame |
| other seeds | seed 11: slit 72.2, min pitch 0.905, 31 forced, gold ≥ 5.02, 16/16 K in bin. Seed 3: slit 80.7, 48 forced, three empty bins (right third of the storm has no Q; the hill is a two-bin mesa) |

## Plot budget (v16)

- draw 14 231 mm · travel 14 751 mm · 15 693 commands · 778 pen lifts · preview estimate 790 s
- per pen: black 4 434 · crimson 2 277 · blue 2 053 · gold 2 075 · green 3 392 mm; 5 pens (4 swaps)
- bounds X 0–229.7, Y 0–289.7 on 24×30 portrait; scorer grade A, dominant issue "efficiency"

## Self-critique

1. **Hierarchy 7.** Wall + opaque hill + principal vertical read first. SUMS / TO ONE is second, then the two sweeping families. The storm is still the busier half.
2. **Grid & alignment 7.** Q/K mirror each other off the frame. V sits at its reed, Z = AV on the TO ONE baseline, SOFTMAX on the jamb. Top-frame reed ticks pair up 1 mm apart in four places.
3. **Tension & asymmetry 7.** The point-mirror (K tails right-above, V tails left-below) against the down-right fan and the flush-left type is a real working diagonal.
4. **Negative space 7.** The title void is shaped by the fan's flank and is now clear by ≥ 20 mm. The long low table of the hill is a quiet band inside the throat.
5. **Craft 7.** Every separation ≥ 0.90 mm, every piece ≥ 2 mm, gold ≥ 5 mm, no elbows, no ends in open paper. One Q×K crossing at 26°. Travel is still 3.6 % over draw.
6. **Concept 7.** Keys die in the hill, queries pass, values are woven in after the waist with over/under = attention above uniform. The throat is no longer a chart.
7. **Depth 5.** Declared flat; occlusion (the opaque hill, every over/under) is the only cue.

**Single worst thing:** the K tails on the right (x 170–230, y 188–230). Carried back to the frame, the low K sweeps dip before rising to their reed, which adds an S-wave rhythm r04 did not have. One of them (K13) crosses the outermost Q ray at 26°. Second worst: at equal bins the hill is a needle standing on a long 3 mm table. That is true at peak/median 4.2, but at 3 m it reads less as a "hill" than r04's did. The slit is also 42 % wider than r04's, which the 0.9 mm rule forced.

## Engine requests

1. `forms.histopolate(edges, masses, ramp=β)`: the exact-area, ramp-constrained smooth profile used here (`_histopolate_ramp`). It is the second plate that needs it.
2. `kit.weave_gaps(poly, marks, r, min_piece)`: arclength over/under gaps with under-run merging (`_merged_gaps` / `_split_by_gaps`). It replaces the circle cuts that leave crumbs.
3. Vectorised `geometry.intersections(a, b)` with angles. `_crossings_ang` is hand-rolled again.
