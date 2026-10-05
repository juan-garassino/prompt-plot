# Science critique — ising r05 · statistical physics (2D Ising, critical phenomena) · 2026-09-29
render: gallery/studio/ising/trials/pp_ising_r05_iterate_v8.png (gcode ~/Downloads/pp_ising_r05_iterate_v8.gcode: 13 869 cmds; pen 0 black 895 strokes / 10.36 m, pen 1 crimson 11 / 1.65 m, pen 2 grey 245 / 4.56 m, matching the HANDOFF). Seed sweep `_s3` / `_s13` parsed the same way.

**Missing inputs (fourth round running):** `studio/ising/dossier.md` and `encoding.md` still do not exist, so there are no §7 check numbers, no §4 lies list and no §5 misconception. The checks below use the brief (`studio/physics/ising.md`), the HANDOFF, the numbers the sheet prints, and **my own Swendsen–Wang simulation of the declared setup**:
- geometry: 212 × 137, T/Tc = 0.70 + 1.10(i+½)/212, periodic in y, left column bonded to a fixed + wall, right edge free;
- sampling: 4 chains × 150 samples, 3 sweeps apart, after 200 burn-in sweeps. The cluster census uses 100 of those samples.

**Sheet method:**
- Lattice fitted from the ink: pitch P = 249.8/212 = 1.17830 mm, cell walls at x = 36.8 + iP and y = 27.573 + jP.
- Every stroke was broken into unit dual edges, with its pass offset recovered: black 0 / 0.35 / 0.70 mm inward, red 3 passes at about ±0.1–0.15 mm normal offset, grey 1 pass.
- Faces were flood-filled between all base edges, wrapping in y. Each face was classed by its boundary rung.
- The ruled sea was measured on its 46 rows, y = 27.573 + 3kP.

## Check numbers
| quantity | claim (sheet / brief) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Tc | `TC 2.269185 ONSAGER 1944 EXACT` | 2/ln(1+√2) = 2.2691853 | printed 2.269185 | OK |
| thermometer 0.70 → 1.80, linear | HANDOFF | 0.05 step = 11.355 mm | 23 ticks, x 36.80 … 286.60. Every tick lands on its value to 3e-5. The crimson 1.00 tick sits at x 104.93 (exact 104.927) and is taller (3.2 mm against 1.8 / 0.9) | OK (exact) |
| `ONSAGER M 0.969` (mean m, 0.70–0.80 Tc) | colophon | Onsager–Yang (1−sinh(2β)^−4)^(1/8): 0.9691 (continuous), 0.9693 (19 column centres) | printed 0.969 | OK |
| `UNDER 0.80 TC AS DRAWN 0.977` | colophon | sim held density, every 3rd row, 19 columns: 0.9695 ± 0.0071 | ruled coverage over the 19 whole columns × 46 rows: **0.9771** (0.9765 on the exact 0.70–0.80 interval) | OK (matches its own ink; +1.1 σ from the sim) |
| same, seed sweep | printed s3 0.976 · s13 0.965 | — | s3 measured 0.975, s13 measured 0.964 | OK (rounding) |
| `RULE DENSITY IS THE MAGNETISATION M` | colophon | Exact Edwards–Sokal identity with a + wall: ⟨σ_x⟩⁺ = P(x ↔ wall). The sim confirms the band means track Onsager: 0.9695 / 0.9277 / 0.7934 against 0.9693 / 0.9291 / 0.8007 | Sheet by band: 0.70–0.80 **0.977**, 0.80–0.90 **0.942**, 0.90–1.00 **0.732**, 1.00–1.10 **0.165**. The sheet has 0.547 in 0.95–1.00 against a sim of 0.734 ± 0.070 (seed 7 fluctuates low there; s3 0.788, s13 0.634) | OK (an expectation identity, and one configuration is drawn) |
| `RED HELD CLUSTER HULL MEAN 1.03 TC` | colophon | sim hull-edge mean 1.032 ± 0.018 (5–95 %: 1.004–1.063). Sim edges 503 ± 86 | 461 red edges, mean **1.034**, range 0.933–1.183. s3: 1.031 (printed 1.03). s13: 1.038 (printed 1.04) | OK |
| red = one frontier | HANDOFF | the outer hull of the wall cluster, wrapping in y | 3 parallel passes, each one continuous stroke of 543 mm from y 189.0 to y 27.57. Red shares no base edge with black or grey | OK |
| held hull size | — | sim hull area 8719 ± 447; held cluster 7999 ± 350 | held face 8133 cells | OK (−1.3 σ) |
| rules ⊂ held cluster | `RULED … THE HELD FK CLUSTER` | a held site never lies inside a free outline | 0 of 2523 rule steps have neither neighbouring cell in the held face. 0 rule steps overlap any wall edge. Rightmost rule end mean 1.017 Tc, inside the red coast | OK (s3: 3/2691 stray steps at 1.02–1.08 Tc; the plate has 0) |
| rung cuts, hull area ≥ sites | `GREY 13-29 · 1 PASS 30-49 · 2 PASSES 50-154 · 3 PASSES 155+` | a hull's enclosed cells ≥ its site count | Pure-grey cluster faces: 13–30 cells. Pure 1-pass black faces: 30–48 (13 faces). The single 3-pass cluster: 481 cells, with its 0.70 mm inner pass drawn as 232 mm of ink around a ≈ 247 mm hull. Faces under the cut are pockets between touching hulls (95); none is a cut-down cluster | consistent |
| free-cluster census (whole sheet) | — | sim per configuration: 13–29 **158 ± 10** · 30–49 **29 ± 5** · 50–154 **15 ± 3** · 155+ **1.6 ± 1.1**. P(≥ 1 top-rung cluster) = 0.81 | grey **167** · 1-pass **26** · 2-pass **18** · 3-pass **1**. s3: 160 / 28 / 21 / 1. s13: 162 / 27 / 15 / 1 | OK (all within ±1 σ) |
| census by band (count · mean size) | `BLANK DISORDER FINER THAN 13 SITES`, the hot-side gradient | sim: 1.00–1.15 40.9 · 41.4 · 1.15–1.35 **74.9 ± 5.9 · 26.9** · 1.35–1.55 **51.5 ± 5.1 · 20.2** · 1.55–1.80 **32.5 ± 4.7 · 17.4** | sheet (face area): 1.00–1.15 46 · 57.7 · 1.15–1.35 **77 · 27.1** · 1.35–1.55 **50 · 20.0** · 1.55–1.80 **31 · 17.5**. Strictly decreasing in both count and size | OK. The outlines out to 1.80 Tc are real: about 31 clusters of 13+ sites are expected there |
| union hull ink by rung | — | sim unit edges 3487 ± 199 / 1112 ± 195 / 949 ± 216 / 208 ± 162 | grey 3840 · black 1-pass 1080 · 2-pass about 1060 · 3-pass about 197 | OK (grey +1.8 σ) |
| top/bottom seam | `TOP AND BOTTOM WRAP` | a wall across the seam is one edge shown twice | 18 columns carry seam edges at both y 27.57 and y 189.0, in identical columns. Every one separates a hull from exterior or from a different hull. No cluster is cut to below its rung | OK |

## Lies list (no dossier §4; items from the brief's ⚠ rules, the HANDOFF and the printed claims)
| item | status |
|---|---|
| "a big domain is the critical signature" (brief ⚠) | clean. Red is only the held FK cluster's frontier, printed as MEAN 1.03, not 1.00 |
| FK clusters passed off as spin domains | clean. `FK` appears on the ruled line and on the outline key |
| decorative marks posing as data | clean. Every outline is a free FK cluster of ≥ 13 sites at its declared rung. The per-band census matches the simulation |
| mark code undeclared | clean. Grey is keyed in grey ink; the pass rungs, the site ranges and the blank are all declared |
| the ruled sea is the held cluster, and not omitted where it exists | clean. **The r04 violation is gone.** The title spine sits at x 15–35, off the lattice. The 0.70–0.80 band is ruled in 46 of 46 rows (min 0.844) |
| the printed check is provable from the ink | clean. 0.977 is exactly the drawn coverage (0.9771), and it is labelled `AS DRAWN` with `EVERY 3RD ROW` |
| seam cuts faking small clusters | clean |

## Scores
- truth **9**. Every printed number reproduces:
  - Tc and the axis are exact.
  - The Onsager m is 0.969.
  - The drawn density is 0.977.
  - The hull mean is 1.034, against 1.032 ± 0.018.
  - The 0.80–0.90 band reads 0.942 against 0.928 ± 0.011.
  - The full rung census (167 / 26 / 18 / 1) and the per-band count and size gradient sit within 1 σ of an independent simulation, on all three seeds.

  The one soft spot is not a lie: seed 7 is sparse in 0.95–1.00 Tc (0.547 against a mean of 0.734 ± 0.070), so right at the coast the rules under-read M.
- encoding fidelity **9**.
  - Size is carried by rung with no leaks: grey faces are ≥ 13, 1-pass faces 30–48, the 3-pass cluster 481.
  - The inward pass offsets (0 / 0.35 / 0.70) are clean, and there are no cross-layer shared edges.
  - Rules never leave the held cluster or overlap a wall.
  - The wrap is honest, and every mark is data.
- insight legibility **8**.
  - The sheet now tells a stranger what the rules are (M), what the blank is (disorder finer than 13 sites), that Tc is exact, and that Tc is a place.
  - Cold sea → red coast next to the red 1.00 tick → heavy outlines at 1.0–1.15 (11 of 18 two-pass, the only 3-pass) → grey dust thinning to 1.8 all read left to right.
  - Residual gaps:
    - `FK` is never unpacked. A stranger cannot learn that it means "spins bonded with probability 1 − e^(−2J/T)".
    - The highest outline count sits at 1.15–1.35 (77), not at Tc (46). Only the weight and size, not the count, place "largest structure" at Tc, and the sheet never says count and size diverge.

**VERDICT: PASS** (9 · 9 · 8)

## Mandates
None (PASS). Advisory, if a round remains:
1. **Unpack FK in the existing face.**
   - Where: colophon line 2, x 15–95, y ≈ 23.
   - Measured: `FK` appears twice and is defined nowhere.
   - Suggested: e.g. `FK  SPINS BONDED WITH PROB 1-EXP(-2/T)`.
2. **Say that count and size peak apart.**
   - Measured: outlines per band are 46 / 77 / 50 / 31, peaking at 1.15–1.35. Mean size is 58 / 27 / 20 / 17, peaking at 1.00–1.15.
   - One colophon line, e.g. `WEIGHT PEAKS AT TC  COUNT PEAKS PAST IT`, stops the densest grey at 1.2 Tc from reading as "most critical".
3. **Hold the per-seed consistency.**
   - The printed `AS DRAWN` and `MEAN` values round-match on all three seeds (0.977 / 0.976 / 0.965 against measured 0.977 / 0.975 / 0.964). Keep these computed from the ink, not the lattice.
   - s3 has 3 of 2691 rule steps inside non-held faces at 1.02–1.08 Tc. Worth a look before s3 is ever the plate.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S3 (printed check the ink proves) | **FIXED** | `UNDER 0.80 TC  AS DRAWN 0.977  ONSAGER M 0.969`, with `RULED EVERY 3RD ROW` stated. Measured coverage over 19 columns × 46 rows is 0.9771, against the sim's 0.9695 ± 0.0071 and Onsager's 0.9693. The seeds agree too (s3 0.976/0.975, s13 0.965/0.964) |
| S7 (coldest band gets its sea back) | **FIXED** | The title moved off the lattice (spine x 15–35, lattice from x 36.8). In 0.70–0.80: 46/46 rows are ruled, mean **0.977**, min 0.844. 0.800–0.825 reads 0.958 against Onsager's 0.950. The mandate's literal "every row ≥ 0.95" is unphysical: in the sim, 17.8 ± of 46 rows fall under 0.95 by one missing site (a 0.948 row), and P(all rows ≥ 0.95) = 0.00. The sheet's 16/46 is the honest value. **This retires that test.** |
| S8 (say what a stranger can't infer) | **FIXED** | All three lines are present: `TC 2.269185 ONSAGER 1944 EXACT`, `RULE DENSITY IS THE MAGNETISATION M` (true as the Edwards–Sokal identity) and `BLANK DISORDER FINER THAN 13 SITES` (cut verified: 0 outlined faces under 13 that are clusters) |
| S1 (key + FK), S2 (top rung) | hold | The key was updated to the 13 cut and the grey rung. The 3-pass rung is populated on seeds 7 / 3 / 13 (1 / 1 / 1; sim P = 0.81) |
| A14 (science side of "hot half reads hot") | holds as truth | Counts 77 → 50 → 31 and mean sizes 27.1 → 20.0 → 17.5 across 1.15–1.35 / 1.35–1.55 / 1.55–1.80. The sim gives 74.9 → 51.5 → 32.5 and 26.9 → 20.2 → 17.4, so this gradient is the physics, not styling. There are no dots (the art-side cell test is the art critic's) |
| regressions vs r04 | none | Same seed-7 configuration: red 461 edges, mean 1.034; top-rung cluster 481 cells; rules ⊂ held cluster. No truth that held in r04 fails now |
