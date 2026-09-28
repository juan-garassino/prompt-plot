# Science critique — ising r04 · statistical physics (2D Ising, critical phenomena) · 2026-09-28
render: ~/Downloads/pp_ising_r04_iterate_v5.png (gcode ~/Downloads/pp_ising_r04_iterate_v5.gcode, 12821 cmds, 684 strokes: pen 0 black 673, pen 1 crimson 11). Seed sweep ~/Downloads/pp_ising_r04_iterate_v4_s3/_s13 parsed the same way.

**Missing inputs (third round running):** `studio/ising/dossier.md` and `encoding.md` still do not exist, so there are no §7 check numbers, no §4 lies list and no §5 misconception. The checks below use the brief (`studio/physics/ising.md`), the HANDOFF, the claims the sheet prints, and an **independent Swendsen–Wang simulation of the declared setup**:
- geometry: 212 × 137, T/Tc = 0.70 + 1.10(i+½)/212, periodic in y, left edge bonded to a fixed + wall, right edge free;
- sampling: 2 chains × 180 samples, 3 sweeps apart, after 100 burn-in sweeps; vectorised union–find labeller.

**Sheet method:**
- Lattice: x = 10.4 + 1.3 i, y = 10.9 + 1.3 j.
- Pass count on every dual edge = the number of distinct parallel copies found there. Offsets are 0 for 1 pass, ±0.06 mm for 2 passes, and 0 / ±0.13 mm for 3 passes. They are clean on all 2180 black and 461 red edges.
- Wall faces were rebuilt by cell flood-fill between the inked edges.
- Ruled-sea coverage was measured on the 46 ruled rows, y = 10.9 + 3.9 k.

## Check numbers
| quantity | claim (sheet / brief) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Tc | 2/ln(1+√2) | 2.2691853 | red 1.00 tick at x = 85.56 | OK |
| FK bond prob at Tc | — | p_c = 1−e^(−2/Tc) = 0.585786 | — | OK |
| Thermometer 0.70 → 1.80, linear | HANDOFF | 0.05 step = 12.527 mm | 23 ticks at x 10.40 … 286.00. Each tick lands on its value to 1e-4. The 1.00 tick is red and taller (191.2–194.4) | OK (exact) |
| `ONSAGER M 0.969` (mean of m over 0.70–0.80 Tc) | colophon y ≈ 28 | Onsager–Yang (1−sinh(2β)^−4)^(1/8): 0.9691 (continuous), 0.9693 (19 column centres) | printed 0.969 | OK |
| `UNDER 0.80 TC 0.977` (held-cluster density) | colophon y ≈ 28 | sim 0.9697 ± 0.0055 (5–95 %: 0.960–0.978) | Ink in that band exists only in the 12 colophon rows (y ≤ 53.8), coverage **0.982**. The other **34 of 46 ruled rows carry 0.000**: the title halo | value plausible (+1.3 σ); **not verifiable from the ink** |
| held density 0.80–0.90 (visible band) | not printed | Onsager m̄ 0.9295; sim 0.930 ± 0.011 | all 46 rows: 0.921 | OK |
| `RED ITS HULL MEAN 1.03 TC` | colophon | sim frontier-edge mean 1.032 ± 0.017 (5–95 %: 1.00–1.06) | 461 red edges, mean 1.034, range 0.933–1.183. Per-row rightmost mean 1.020 | OK |
| red = one frontier | HANDOFF | hull of the wall cluster, wraps in y | 1 component: 461 edges, all 3 passes. Open only at the seam, (65,0) ↔ (67,137): 2 undrawn wrap edges, and `TOP WRAPS` is printed. 0 edges are shared with black. The r02 2-site pinched red lake is gone | OK |
| rule ↔ free-cluster exclusivity | "ruled = held cluster" | a held site is never inside a free outline | 0 ruled-sea samples inside any drawn face | OK |
| rung thresholds 30–49 / 50–154 / ≥ 155 | legend | hull area ≥ site count | Every face bounded only by 1-pass edges has 30–48 cells. The only 3-pass cluster encloses 483 cells. 2-pass-only faces are 54–161 cells: 161 needs ≥ 7 hole sites, plausible for a porous FK cluster at 1.12 Tc | consistent |
| rung census (free FK clusters) | — | sim per configuration: 1-pass 27.0 ± 4.7, 2-pass 15.3 ± 3.6, 3-pass 1.6 ± 1.2; P(≥1 top-rung cluster) = 0.79 | face count ≈ 22 / ≈ 16 / 1 (the 1- and 2-rung counts are approximate because adjacent clusters share walls) | consistent (1-rung at −1 σ) |
| top rung populated across seeds | S2 | P = 0.79 | 3-pass edges: v5 194, s3 148, s13 155. Present in all three | OK |
| top-rung uniformity | S2 | 0 % under-inked | the 3-pass cluster: 194/194 black edges at 3 passes + 14 red (the shared frontier). 0 at 1–2 | OK |
| rightmost drawn free cluster | — | clusters ≥ 30 sites thin out quickly above 1.4 Tc | last outline centred at 1.61 Tc (x 233–247). T > 1.62: bare paper | consistent |
| held cluster size | — | sim 7990 ± 350 | same seed-7 chain as r02 (≈ 7895) | OK |

## Lies list (no dossier §4; items from the brief's rejected rules, the HANDOFF and the printed claims)
| item | status |
|---|---|
| "a big domain is the critical signature" (brief ⚠) | clean. Red is only the held cluster's frontier, and its mean is printed as 1.03, not 1.00 |
| FK clusters passed off as spin domains | clean. `FK` is on both the ruled line and the legend (r02 violation fixed) |
| decorative marks posing as data | clean. The dots are gone; every outline is a ≥ 30-site free FK cluster at its rung |
| mark code undeclared | clean. Rungs, site ranges, `SINGLE SPINS NOT DRAWN NOR UNDER 30` |
| the ruled sea = the held cluster everywhere it is drawn and **not drawn where it exists** | **VIOLATED (undeclared omission)**. The CRITICAL title deletes the sea over x 10.4–35.5, y 57.7–186.4: 25 × 129 mm, 34 of 46 ruled rows, coverage 0.000 where 0.97 is true. The restart edge at 0.800–0.825 Tc reads 0.842 against 0.949. The coldest, most-ordered band therefore reads as the emptiest ordered band |
| printed check is provable from the sheet | **VIOLATED (partial)**. `UNDER 0.80 TC 0.977` describes exactly the band the title has blanked |

## Scores
- truth **8**. Every printed number checks out against an exact result or the independent simulation: Onsager m 0.969, held density 0.977 within 1.3 σ, hull mean 1.034 against 1.032 ± 0.017, the exact axis, and a rung census inside the simulated spread. The one truth problem is by omission: the title removes the coldest 10 % of the temperature axis from 74 % of the rows.
- encoding fidelity **7**. The pen code is exemplary: three clean pass offsets, no cross-pen overlap, the ruled sea never enters a free outline, and the top rung is uniform and robust to the seed. But a channel is switched off under the type without a declaration. The printed check refers to that switched-off band, and the visible sea starts ragged 0.6–6 mm right of the 0.80 line.
- insight legibility **7**. "Tc is a place" lands: the sea ends at a red coast beside the red 1.00 tick, and the outline weight falls from 3 to 2 to 1 passes moving right (3-pass at 0.95–1.10, 2-pass to 1.42, 1-pass to 1.61). A scientist can now decode everything. A stranger cannot: `ONSAGER M` is never said to be the magnetisation, i.e. the density of the rules. Bare paper at 1.62–1.80 Tc and bare paper under the title look the same, although one is "disorder too fine to draw" and the other is "total order, hidden".

**VERDICT: FAIL** (fidelity 7, legibility 7)

## Mandates
1. **Give the coldest band back its sea.**
   - Where: x 10.4–35.5 (T/Tc 0.70–0.80), rows y 57.7–186.4, behind `CRITICAL`.
   - Measured: ruled coverage **0.000** in 34 of 46 rows. In the 0.800–0.825 band the rules restart late (leftmost rule ends at x 36.0–41.6), giving **0.842**.
   - Expected: ≈ **0.97** (Onsager 0.969; sim 0.970 ± 0.006; the sheet's own 12 colophon rows show 0.982) and 0.949 in 0.800–0.825.
   - Fix: break the rules only within ~1 mm of the glyph strokes (letter-shaped halo), or move the title off the data. Every ruled row in 0.70–0.80 should read ≥ 0.95.
2. **Make the printed check one the ink proves (S3).**
   - Where: `UNDER 0.80 TC 0.977   ONSAGER M 0.969`, colophon, x ≈ 15–78, y ≈ 28.
   - Measured: the band it names is blanked in 34/46 rows. The 0.977 is not the drawn rows (0.982 over 12 rows) and the sheet does not say what it is.
   - Fix: either restore the band (mandate 1) and print the density of the drawn rules, or restate the check on a band that is inked. On this sheet, 0.80–0.90 Tc measures **0.921** against Onsager **0.930**. Either way, say what the number is: every 3rd row as drawn, or all 137 rows.
3. **Say the two things a stranger can't infer.**
   - Where: the colophon block, x 15–95, y 11–54.
   - Measured: the word "magnetisation" (or "order") never appears. `M` is undefined. The blank hot 0.40 of the width (x 160–286: 3 outlines in ≈ 126 × 178 mm) is explained only by `NOR UNDER 30`.
   - Expected, two lines in the existing face:
     - one tying rule density to the order parameter, e.g. `RULE DENSITY IS THE MAGNETISATION M` (it falls from 0.95 at 0.85 Tc to 0.30 at 0.99 Tc on the sheet);
     - one naming the hot blank as fine disorder, e.g. `BLANK  DISORDER FINER THAN 30 SITES`.

     That way the cooling-to-order story and the "clusters largest at Tc" gradient (3 → 2 → 1 passes from 1.0 to 1.6 Tc) read without the legend math.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 (key + FK) | **FIXED** | The legend reads `FREE FK CLUSTERS 1 2 3 PASSES` / `SITES 30 TO 49  50 TO 154  155 UP` / `SINGLE SPINS NOT DRAWN  NOR UNDER 30` / `RULED  THE HELD FK CLUSTER`. Ink matches: 940 / 1046 / 194 black edges at offsets 0 / ±0.06 / 0,±0.13 mm. Every 1-pass-only face has 30–48 cells |
| S2 (top rung typical + uniform) | **FIXED** | Threshold 155. The 3-pass rung is present in seeds 7 / 3 / 13 (194 / 148 / 155 edges). Sim P(≥ 1 top-rung cluster) = 0.79. The 3-pass cluster is 100 % at 3 passes (194 black + 14 red shared, 0 under-inked) |
| S3 (printed check the sheet proves) | **PARTIAL** | The unverifiable energy line is gone and an Onsager-m check is printed and correct (0.969). But its measured 0.977 names a band the title has blanked in 34/46 rows. See mandate 2 |
| (A12, science side) one red coast | holds | 1 red component, 461 edges, 3 passes. The r02 pinched 2-site red loop is removed |
| regression vs r02 | **REGRESSED (one truth)** | r02 showed the cold band in text-free rows (0.973 against Onsager 0.969). r04 shows 0.000 there under the title. All other r02 truths still hold: frontier 1.034, exact axis, rule/hull exclusivity, 0.80–0.90 density 0.921 (r02 0.926) |
