# attention-weaving r04 — mirror-drain · parent: r03 (aperture v19) · 2026-09-28

## Render

```bash
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r04/piece.py \
  --fn attention_weaving_mirror_drain --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen \
  --out gallery/studio/attention_weaving/current/pp_attention_weaving_mirror-drain_v13.png
```

- final: `gallery/studio/attention_weaving/current/pp_attention_weaving_mirror-drain_v13.png` / `.gcode`, seed 7
  (v10 is byte-identical to v13 apart from the timestamp header)
- trail: v1–v10 seed 7 (v1 ψ-bend, v2 conformal fold (rejected), v3–v10 pitch-limited bend
  with orthogonal-trajectory V), v11 = seed 3, v12 = seed 11
- no LEDGER.md exists for this slug. Mandates below are Juan's REWORK note (J1, J2) and the
  aperture **Weak** list in DESCRIPTION.md (D1–D6).

## Mandate responses

| id | mandate | status |
|---|---|---|
| J1 | "the TOP half looks much better than the BOTTOM — bring the bottom up to the top" | **FIXED.** The bottom now uses the top's grammar: one radiating family (38 green lanes, the φ<0 streamlines of the same aperture) crossed at wide angles by one spiral family (16 gold V arcs), real over/under at every crossing. The gold V + green cable and its parallel run-out are gone. |
| J2 | "the black softmax staircase should be SMOOTHER … keep the partition exact" | **FIXED at seed 7.** The profile is now a least-curvature *histopolating* curve: its area over clump g is exactly a_g (max error 1.0e-15, measured by trapezoid on the drawn polyline). No two-knots-per-clump flats and no knot discs. It reads as one hill with a right shoulder. Caveat in Self-critique: at seeds 3 and 11 the clump means are not unimodal (width is quantised in whole filaments), so the exact curve has to ripple there. |
| D1 | [craft] profile still reads as a staircase (flats + 12 discs + flat-topped tower) | **FIXED.** This is the same change as J2. Clump boundaries are now 2.4 mm ticks on the wall line, in the 1.85 mm gaps between clumps. |
| D2 | [hierarchy] bottom = two families of parallels + 80 mm dead run-out | **FIXED.** The lanes radiate and never run parallel. All 608 V×lane crossings are on the sheet. The run-out that remains is the outer rays, the same as the top's outer Q rays, and their outlet reeds carry \|z_t\|. |
| D3 | [craft] tangle of lane chevrons at the cable's bend (0.58–0.67, 0.50–0.58) | **FIXED.** Lanes cannot cross by construction (ψ' = ψ·m(\|φ\|) is monotone in ψ at every depth). Measured: 0 lane–lane crossings and 0 V–V crossings. |
| D4 | [concept] the "double sunburst" is single; φ<0 half not drawn | **FIXED.** This round is that fix: the lower fan is the φ<0 half of the same coordinate system, joining each upper strand at the exact slit point (join error 1.4e-14 mm) with a vertical, tangent-continuous crossing. |
| D5 | [grid] footer leading inconsistent; SOFTMAX away from profile; cumulative unlabelled | **FIXED.** Footer lines sit at a constant 4.8 mm leading, and each is fitted to the room the fan's flank leaves at its height. `SOFTMAX` sits on the wall 3 mm right of the right lip. The cumulative is the running integral of the hill and ends on a disc labelled `1.000`. Both labels have halos that cut the strands under them. |
| D6 | [space] lower-left void is leftover between gold and title | **FIXED / ARGUED.** The void is now bounded by the fan's open flank, a curve of the flow itself, and it holds the title. It is larger than before, and I think that suits the concept ("the silence is the mass the softmax threw away"). It is still the emptiest region on the sheet, so a critic may call it too big. |

## What changed from parent

- **Upper half: the geometry is untouched.** Q, K, the principal query and the wall are identical code and identical RNG draws. Per-pen draw length went from crimson 2431 → 2423 mm and blue 2186 → 2167 mm. The only differences are the gaps where Q/K pass under the new profile and the two label halos.
- **Lower half rebuilt as the mirror.** The green lanes are the φ<0 streamlines of the same elliptic system. They are folded down-right by the "Z = AV bend" ψ' = ψ·(KB + (1−KB)/cosh(BR·|φ|)), with KB = 0.33 and BR = 1.30. The 180° mirror fan closes to a 60° wedge, which leaves the lower-left for the title. BR is the fastest bend the pen floor allows, and I measured the result.
- **V is a second spiral family, the mirror of K.** Each V arc is an orthogonal trajectory of the *drawn* lane field (integrated through the analytic Jacobian), pitched into a spiral. The pitch runs +5° for the heaviest value, innermost, down to −24° for the lightest, outermost, so no spiral sinks toward the slit before crossing the last lane. Both ends are mid-air, like K's start: V never touches the slit.
- **Value vectors moved to the output space.** Each V is now a 38-vector, one component per lane, which is a real Z = AV: z_t = Σ_j a_j v_j[t]. Over/under at V_j × lane t is sign(v_j[t]). The outlet reed tick at each lane's exit has length 1.2 + 4.2·|z_t|/max|z|.
- The profile is the histopolating curve described under J2. The cumulative is recomputed as its running integral.
- Type: the title is 15 mm (was 17) so `TO ONE` clears the flank. The title boxes are halos. The footer is reflowed to 4 lines fitted to the flank. `V` and `Z = AV` hang off one vertical 6 mm left of the innermost V start.
- Dotted equipotentials: above the wall they are unchanged; below it there is one arc (φ = −0.62) carried through the bend. The second arc read as scattered dashes inside the weave and was cut.
- Rejected on the way: (v1) a smoothstep bend put crossings at a median 32° and left a hockey-stick kink. (v2) The conformal fold w = L + (2c)^(2/3)(z−L)^(1/3) is exact and angle-preserving, but pulling the landings back through it crushes the left half of the lanes to a 0.27 mm pitch. A conformal map cannot fix the slit pointwise and also bend the fan, so I abandoned it. (v4–v5) Outward-pitched V left 130 of 608 crossings off the sheet. (v6–v8) Uniform inward pitch sank the heavy V toward the slit.

## Measurements / computations (seed 7, `piece.LAST_STATS`)

| claim | measured |
|---|---|
| weights sum to one | Σa = 1.0000000000 |
| peak / entropy | a_max = 0.190, H = 3.762 of 4.000 bits |
| area partition exact | max \|area_g − a_g\| = 1.03e-15 (trapezoid on the drawn polyline) |
| cumulative lands on one | 0.999999999999999 (drawn normalised to exactly 1.000) |
| profile ≥ 0 | min h = 0.0070 (foot at each lip, 4.3 mm) |
| continuity through slit | max \|lane start − landing\| = 1.4e-14 mm |
| conservation | 38 in, 38 out |
| lane pitch | slit 0.950 mm; fan min 0.897 mm (at 120.0, 166.4, just under the bend) |
| no self-crossing | lane–lane 0, V–V 0 |
| every value crosses every lane once | 608 / 608 pairs, exactly 1 crossing each |
| crossing angle V × lane | min 65.7°, median 78.9° |
| Q·Kᵀ on sheet | 113 / 352 (unchanged from r03) |
| other seeds | seed 3 and seed 11: 608/608, min angle 65.7°, pitch 0.897, area error ≤ 5e-16 |

## Plot budget (v13)

- draw 16 053 mm · travel 17 321 mm · 20 197 commands · 1 331 pen lifts · preview estimate 910 s
- 5 pens (4 swaps). Per pen draw length: black 4547 · crimson 2423 · blue 2167 · gold 1164 · green 5752 mm
- bounds X 0.0–229.7, Y 0.0–289.7 (inside 220×280 drawable + margin). Scorer: grade A, dominant issue "efficiency" (travel is high because every crossing is a gap).

## Self-critique (seven dimensions)

1. **Hierarchy — 7.** The storm, the wall and the drain now read as one double sunburst. The top still dominates. The profile is smaller and quieter than the old tower, so the "sums to one" object is less loud at 3 m.
2. **Grid & alignment — 7.** The footer is flush-left at constant leading, and the V/Z marks share one vertical. The footer's right edges are ragged against the flank by design, and `V`/`Z = AV` float in the void rather than hanging off a sheet-level line.
3. **Tension & asymmetry — 8.** A hard diagonal flank from the left lip to the bottom-right corner, with the type as mass on the silent side.
4. **Negative space — 7.** The lower-left silence is shaped by the flow, not left over. It is large, possibly too large.
5. **Craft for pen — 8.** Pitch is ≥ 0.897 mm everywhere. There are no tangles, and 608 gaps are all 1.24 mm. Gold is single-pass except the two heaviest values. The 5-pass wall and profile are unchanged.
6. **Concept — 8.** The same coordinate system above and below, Z = AV computed per lane, and V never passing through the waist. The twist ("the sunburst is a drain") now has both halves.
7. **Depth — declared flat (Deco).** Occlusion at every crossing is the only depth cue, as in r03.

**Single worst thing:** the softmax profile is exact and one hill at seed 7, but it keeps a right-hand shoulder. At other seeds (3, 11) it ripples: seed 3 gives a mesa with lip bumps, seed 11 two humps. The cause is upstream. Clump width is quantised to whole filaments, so the per-clump mean height a_g/width is not unimodal even though a_g is, and an exact-area curve has to follow it. Fixing it means re-dealing the clump widths, which moves the Q/K landings. That changes the upper half, which this round was told to keep.

## Engine requests

1. `geometry.intersections(a, b)` returning points **and angles** (vectorised). I hand-rolled `_crossings_ang` with numpy, and the pure-Python version in r03 took more than two minutes for 608 pairs.
2. A `histopolate(edges, masses)` helper in `engine/forms.py` or `kit.py`: an exact-area smooth profile for any partition plate.
3. `kit.dash()` by arclength (carried over from r03).
