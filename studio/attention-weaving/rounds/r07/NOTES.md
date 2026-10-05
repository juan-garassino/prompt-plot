# attention-weaving r07 — iterate · parent: r06 · 2026-09-29

Built on `encoding.md` **Revision 1** (ONE REED, ONE CLOTH), so this is round 1 of Revision 1 and the
designer-round cap restarts. The work order was r06/SYNTH.md, as the translator encoded it. Juan's J1
and J2 come first.

## Render

```bash
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r07/piece.py \
  --fn attention_weaving_reed --seed 7 --paper 24x30 --orientation portrait \
  --palette goldenrod,dodgerblue,crimson,darkgreen,black,black \
  --out gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.png
```

- **Final:** `gallery/studio/attention_weaving/current/pp_attention_weaving_iterate_v23.png` and `.gcode`, seed 7.
- **Seed checks:**
  - v20 = seed 3, v21 = seed 11. Both were rendered one step before the lead-in move; everything else is identical.
  - All three seeds build without a failed check.
  - Seed 3's hill shows its own data: a second shoulder in bin 8, and a right tail that falls to 0 with no step.
- **Trail (all seed 7):**
  - v17: first build of Revision 1.
  - v18: K landings moved onto streamlines (the first rule put K8 0.13 mm from Q2); reed-mouth nudging (A22).
  - v19: serpentine emission (travel 14.0 → 7.3 m); Q/K labels placed between mouths; the bold strands became one stroke.
  - v22: the K label moved clear of the preview legend.
  - v23: lead-in lowered to y 86 with `V` above it, which removed the sag.

## Mandate responses

| id | mandate | status |
|---|---|---|
| J1 | bring the bottom up to the top | **FIXED (claim; Juan closes).** The bottom now has the top's grammar, mirrored. Above the wall, a sunburst of 38 threads converges on one slit. Below it, the 22 survivors fan out of the same slit as a Deco fan-shell of nested green arcs. One gold weft of 16 picks and 15 U-turns weaves them, from a left-frame reed to a right-frame reed. The bottom is no longer parallels or loose arcs. It is a cloth with visible over/under. |
| J2 | smoother staircase, partition exact | **KEPT.** One C¹ least-curvature curve, ramp-constrained (β = 0.12, every tail step rises), area per bin exact to 2.5e-11. See A19 for the price of pinning it to zero at the jambs. |
| A1 | profile reads as staircase | closed r04, kept |
| A2 | bottom = parallels + dead run-out | **FIXED** (merged into A7). There are no parallel gold families. The picks are straight normals of the fan and rotate from 70° (pick 1) to 85° (pick 16) against the horizontal. |
| A3 | lane chevron tangle | closed, kept: 0 lane–lane crossings |
| A4 | φ<0 half not drawn | closed, kept. The warp leaves the slit perpendicular to the wall (the lanes are offsets of a curve whose tangent there is vertical). |
| A5 | footer leading | closed, kept: 4 lines at 5.0 mm leading |
| A6 / A21 | left-middle void | **FIXED.** Crop x 10–90, y 100–150 holds **0 G1 points** (checked on the gcode). Lane 0 crosses y = 150 at x = 91.55. The L is bounded by the wall, the warp flank and the gold lead-in at y 86. |
| A7 | V one closed sweeping family, lands on lane/reed, no piece < 5 mm | **FIXED by construction (R1).** V is one weft of 1,573 mm and has exactly two ends, both capped by reed ticks: left frame y 86, right frame y 68.3. Every other gold end is a merge gap flanked by green: the weft runs under that run of warps. Min gold piece is 5.008 mm (53 pieces). The picks exist only where the lanes are 3.667 mm apart along the pick, so a float can never be shorter than 2·3.667 − 2.2 = 5.13 mm. The weft's non-pick parts (turns and leads) cross 0 lanes and stay ≥ 3.01 mm from every lane. |
| A8 | K closes at reeds; every Z exit ticked | closed r06, kept: 16/16 K reach top/right reeds; 22/22 Z exits ticked |
| A9 | clear aperture | closed r06, kept. The only chart mark is the 1/16 tick, outside the slit on the right jamb's outer face (x 129.9–132.9, y = wall + 6.17). |
| A10 | hill is a decision | closed r06, kept. Q stops 1.25 mm above the hill band's top pass; K stops 0.75 mm above it. |
| A11 | labels anchored and clear | **FIXED.** `Z = AV` sits on the TO ONE baseline at x 186–212, 30 mm below the lowest lane. `SOFTMAX` is on the wall's right arm at x ≥ 140, 7 mm right of the jamb, with nothing to wedge into. `Q` and `K` share one y, chosen as the widest gap between frame mouths on both frames. `V` sits over its reed, and `11` over Z11's exit tick. |
| A12 | type block clear; lanes exit right | closed, kept: 22/22 lanes exit the right frame, y 77.3–154.6 |
| A13 | giant type craft | **FIXED.** New `_solid_text` gives every glyph segment the same construction: a 2.0 mm band filled by a serpentine at 0.30 mm pitch, so diagonals equal stems. Interior vertices that turn more than 12° get a filled round join. Terminals are flat. It is filled, not striped. Cap height is 13 mm, with baselines SUMS 63 and TO ONE 44. |
| A14 | travel > draw | **FIXED.** Travel 7.04 m against draw 13.23 m (ratio 0.53; r06 was 1.04). Alternate strands are emitted reversed so the nearest-neighbour optimiser chains them, and each bold strand is one out-and-back stroke. |
| A15 | concept reads as physics figure; braid gone | **ARGUED / addressed by R1.** Over/under now carries data at 352 cloth crossings plus 111 storm crossings. 38 threads enter the reed and 38 thread families make the cloth (§8 of the encoding). |
| A16 | 5 pens vs ≤ 4 | ARGUED (BRIEF): 5 inks, plus a separate text layer as house law |
| A17 | depth undeclared | closed r06, kept (Deco, flat) |
| A18 | lineage/canon | closed r06, kept |
| A19 | slit ≤ 52, hill spans slit, no shelf/jamb steps | **PARTIAL, with a proof.** Slit 52.0 mm, 16 × 3.25 mm bins. The hill spans the full slit and its height is **exactly 0 at both cut edges**. There is no horizontal run: the ramp rows force every tail step to rise. **But a near-vertical rise of 3.71 mm at each jamb is forced by the data.** On equal bins, bin 0's mean height is m₀ = 3.53 mm and bin 1's is m₁ = 3.76 mm (98.7 mm per unit of a). A curve that starts at 0 and does not fall must reach m₀ ≤ h(edge₀₁) ≤ m₁ inside bin 0 while averaging m₀. That confines the rise to at most (1 − m₀/m₁) ≈ 6 % of the bin, 0.20 mm. There are only three alternatives: a false hump (ringing), unequal bins (breaks S2's "height ∝ a"), or inexact area (breaks J2). Juan's "sums to one exactly" outranks this clause. §11.3 "from zero height with no vertical step" cannot be met on this data. **Flag for the lead / translator.** |
| A20 | no text in the upper field except Q/K; Q11 one line | **FIXED.** Only `Q`, `K` and `SOFTMAX` (on the wall arm) are above the wall, checked on the gcode. Q11 is two passes 0.25 mm apart drawn as one out-and-back stroke. With a 0.3 nib that is one 0.55 mm line. The encoding said 0.35; that would leave a 0.05 mm seam, so 0.25 is used and the change is stated here. |
| A22 | reed mouths ≥ 3 mm; no shared tick | **FIXED.** Min mouth gap is top 3.23 mm and right 3.50 mm. 4 K starts were nudged along their sweep (Δψ ≤ 0.04 rad) until the reed was clear. |
| S1 | 22 Q · 16 K → 22 Z | closed r06, kept. The footer reads `22 Q · 16 K → 22 Z`; encoding §8 re-reads the count rule as 38 → 38 (flag for Juan). |
| S2 | equal bins, height ∝ a, area exact | kept: 16 equal bins; peak/median bin mean 4.166; area error 2.5e-11 |
| S3 | one K per own bin | kept: 16/16 K end inside their own bin in x (`k_flow_bins` = [] — no fallback used) |
| S4 | captions true | kept. Every footer number is computed in the same call: `a MAX 0.190`, `H 3.76 / 4.00`, `SLIT 52 MM`, `2.25 MM`, `136 / 352`. |
| S5 | A checkable | **FIXED** (translator, encoding §4a). The piece reproduces it: T = 2.298425, rows sum to 1 within 1.1e-16, bin order [15, 8, 3, 7, 10, 1, 12, 5, 11, 2, 14, 13, 6, 4, 9, 0] = encoding §4a. |
| S6 | hill A axis | **FIXED minimally.** One 3 mm tick at the 1/16 mean-height level (6.17 mm), outside the slit. |
| S7 | GPT-2 row identity | dropped (ledger) |
| S8 | lane identity at the slit | **FIXED (R2).** 22 lanes at one pitch of 2.25 mm; position carries order only, and the footer says so (`LANES EQUAL PITCH 2.25 MM, ORDER ONLY`). The order is seriated on B with Hamming cost 87 (identity order: 142). Q11 is pinned at x = ax. Slot → query: [17, 16, 8, 20, 21, 18, 2, 3, 9, 5, 10, **11**, 12, 13, 14, 15, 19, 7, 1, 4, 0, 6]. |
| S9 | Q_i ends where Z_i leaves | **FIXED:** \|x_Q − x_Z\| = 0.000 mm for 22/22 (same slot x) |
| S10 | checkable rule; Z11 labelled; V indexed; every exit ticked | **FIXED.** `11` sits over Z11's exit tick. Pick order equals bin order, so picks count outward from the slit the way bins count left to right; no index text. 22/22 Z exits and both weft ends are ticked. Every K reaches its reed. |
| S11 | over/under rule vs 5 mm floor | **FIXED by construction.** 352/352 crossings obey `gold over ⇔ a_ij > 1/16` with 0 overrides and no dead band; 136 are gold-over, matching the encoding. The 5 mm floor comes from where picks are allowed to be (lane pitch along pick = 3.667 mm), not from flipping data. Z11 is under gold at exactly picks 7–10 and over at the other 12. |

## What changed from parent

- **The throat.** The slit goes back to 52 mm (r06: 73.7), with equal bins of 3.25 mm. The hill is re-solved pinned to 0 at both cut edges, so the r06 jamb verticals and the flat 3.1 mm table are gone. What remains is a forced 3.7 mm shoulder (see A19). The crown is in bin 7, with K5 and K11 either side of the centre line and Q11 landing on the summit (summit x = ax − 1.0 mm).
- **The lanes.** r06 packed Q lanes by Q11's row with a DP in clumps. Now the 22 lanes sit at one pitch, seriated, with Q11 pinned. Each K rides the streamline whose slit crossing is farthest from the lane slots, and it lands inside its own bin. The measured true K–Q separation above the hill is 1.14 mm.
- **The whole lower half is new.** The warp is **ruled by the upper selvage's normals**. The upper selvage runs from the right jamb: a 6 mm-radius hook to −28°, then a 190 mm arc to −5°, then a straight run. The lower selvage leaves the left jamb and joins, by one cubic, the offset of the upper selvage at 77 mm. Every lane is the linear blend along the same normals. So in the cloth every lane is an offset curve of the selvage, the picks (those normals) meet every lane square (min 88.6°), and the lane pitch along a pick is exactly 77/21 = 3.667 mm. The encoding's sketch (lanes to y 56–172, pick 1 from (135,105)) would have put lane 0 at x ≈ 85.8 at y = 150, inside the void. The built cloth sits higher: lanes exit at 77–155, pick 1 runs (130.5, 90) → (158.8, 167.2), and pick 16 runs (216.7, 76) → (223.9, 157.9).
- **Gold.** r06 had 16 separate reed strands. Now there is one weft: lead-in → 16 straight picks with U-turns outside both selvages → lead-out. Under-runs merge; floats and turns are drawn.
- **Type and text.** All labels move to their own black 0.3 text layer. The giant type is rebuilt (A13), and the footer is rewritten to the encoding's four lines.
- **Plotting.** Six layers light → dark: gold, blue, crimson, green, black structure, black text. Emission is serpentine.

## Measurements / computations (seed 7, `piece.LAST_STATS`)

| claim | measured |
|---|---|
| Σa (drawn row) / all rows | 1.0000000000 / within 1.1e-16 |
| T, a_max, H | 2.298425, 0.190, 3.762 of 4.000 bits |
| bins | 16 × 3.25 = 52.0 mm; Q11 above 1/16 in bins 6–9 (keys 12, 5, 11, 2) |
| hill | area error 2.5e-11; end heights 0.000 / 0.000 mm; peak 20.72 mm; peak/median bin mean 4.166; ramp β 0.12 |
| 1/16 tick | 6.17 mm above the wall (mean-height scale) |
| K | 16/16 in own bin; landing offsets from bin centre −1.15 … +1.14 mm; K drop ↔ Q min 1.14 mm; K–K crossings 0 |
| storm | 111 Q×K crossings, min angle 36.4° (r06: 26.0°); min storm piece 2.29 mm; 0 Q stubs |
| lanes | pitch 2.25 at the slit; min lane–lane 2.05 mm (at the left jamb); 0 lane–lane crossings; exits 77.3–154.6 |
| cloth | 352 crossings, angle 88.6–90°; lane pitch along picks 3.667 mm; pick spacing ≥ 4.40 mm on every lane |
| rule | 352/352 obey a > 1/16; 136 gold-over; 0 overrides |
| pieces | gold min 5.008 mm (53); green min 2.20 mm; gold ↔ un-crossed lane ≥ 3.01 mm |
| void | 0 G1 points in x 10–90, y 100–150 |
| reed | min mouth gap top 3.23, right 3.50 mm (4 K nudges) |

## Plot budget (v23, measured from the gcode)

Estimates assume 10 mm/s draw, 33 mm/s travel and 2.5 s per lift.

| layer | pen | draw | strokes | est. |
|---|---|---|---|---|
| 0 | goldenrod broad 0.7–0.8 (V weft) | 0.86 m | 53 | 3.9 min |
| 1 | dodgerblue 0.3 (K) | 2.10 m | 65 | 6.6 min |
| 2 | crimson 0.3 (Q, Q11 bold) | 2.24 m | 82 | 7.5 min |
| 3 | darkgreen 0.3 (Z warps, Z11 bold) | 3.31 m | 158 | 12.5 min |
| 4 | black 0.5 (wall, hill, tick, reeds, type) | 3.64 m | 173 | 14.4 min |
| 5 | black 0.3 (text) | 1.08 m | 334 | 16.6 min |

- **Totals:** draw 13.23 m, travel 7.04 m, 20,436 commands, ≈ 62 min, plus the frame trace and 5 pen swaps.
- **Order:** light → dark. Each layer is one clean pass and is never re-entered. Scorer grade A; its dominant issue is "efficiency" (the text layer's 334 lifts).

## Self-critique

1. **Hierarchy 7.** The throat (wall, hill, bold vertical) reads first, then the storm, then the green fan. The type is third.
2. **Grid 7.** Q/K share one y; `Z = AV` is on the TO ONE baseline; `V` sits at its reed.
3. **Tension 7.** The converging storm above answers the diverging fan below. The fan sweeps down-right against the flush-left type.
4. **Negative space 7.** The left L void is clean and shaped. The right triangle under the wall arm is quiet.
5. **Craft 7.** Every floor is met and measured.
6. **Concept 7.** Keys are consumed at the reed; values are woven back in after it; the cloth is the matrix.
7. **Depth 5.** Flat by declaration.

**Single worst thing:** the hill's two 3.7 mm jamb shoulders. The tails are nearly flat at 3.7–5.5 mm for 20 mm each side, so at 3 m it still reads as r06's "table on the wall". It is exact and it is forced, but it will be read as A19 failing.

**Second worst:** the cloth's gold reads as sparse dashes in the preview. 61 % of the weft is hidden by the merge rule, and the preview draws gold at hairline width, not the 0.8 mm nib.

## Engine requests

1. `forms.histopolate(edges, masses, pin_ends=True, ramp=β)`: this is the third plate to hand-roll it.
2. `forms.ruled_offsets(curve, D(σ), n)`: a warp family ruled by one curve's normals. Every member is an offset, so the normals are an exact orthogonal pick family.
3. `kit.weave(weft, warps, over(i, g), r, merge_under=True)`: arclength gaps plus the under-run merge.
4. `scripts/render_candidate.py --pen-widths`: preview a broad nib at its physical width. The visualizer supports it; the script does not pass it.
