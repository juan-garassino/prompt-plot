# Science critique — ising r07 · statistical physics (2D Ising, critical phenomena) · 2026-09-29
render: gallery/studio/ising/trials/pp_ising_r07_iterate_v5.png

The gcode is gallery/studio/ising/trials/pp_ising_r07_iterate_v5.gcode, 12,097 commands. Measured per layer:

| pen | strokes | draw |
|---|---|---|
| 0 black | 947 | 8.048 m |
| 1 crimson | 14 | 1.268 m |
| 2 grey | 167 | 3.050 m |

This matches the HANDOFF. The seed sweep (`_s3`, `_s13`) was parsed the same way.

**Missing inputs (fifth round running).** `studio/ising/dossier.md` and `encoding.md` still do not exist, so there is no §7 table, no §4 lies list and no §5 misconception. The checks below rely on three sources:
- exact results (Onsager and Yang);
- the numbers the sheet and the HANDOFF print;
- my own C Swendsen–Wang simulation of the declared setup. It uses the same lattice as the sheet: 212 × 129, T/Tc = 0.70 + 1.60(i+½)/212, periodic in y, left column bonded to a fixed + wall, right edge free, bond probability p = 1 − e^(−2K) between aligned neighbours. There are 8 chains × 150 samples, 3 sweeps apart, after 300 burn-in sweeps.

**How the sheet was measured.**
- The lattice was fitted from the ink: P = 249.8/212 = 1.17830 mm, walls at x = 36.8 + iP and y = 36.4 + jP. Every snapped stroke point sits within 0.005 mm of the grid.
- Strokes were split into unit dual edges and faces were flood-filled, wrapping in y.
- The ruled sea was read at site midpoints on its 43 rows, j = 1, 4, …, 127.
- Clearance was measured by densifying every stroke to 0.1 mm.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Tc | MISSING | 2/ln(1+√2) = 2.2691853 | printed `TC 2.269185` | OK |
| thermometer 0.70 → 2.30, linear | MISSING | a 0.05 step is 7.806 mm | 33 ticks, x 36.80 … 286.60, each on its value to within 1e-4. The crimson `1.00` tick is at x 83.64 (exact 83.6375) | OK |
| `ONSAGER M 0.969` (0.70–0.80) | MISSING | continuous mean 0.96907; mean over the 13 column centres 0.9694 | printed 0.969 | OK |
| `UNDER 0.80 TC AS DRAWN 0.984` | MISSING | sim held density, rows every 3rd, 13 columns: 0.9691 ± 0.0085 (P(≥ 0.984) = 0.045) | 9 missing sites of 559, so **0.9839**. s3 0.9767 (printed 0.977), s13 0.9821 (printed 0.982) | OK. The ink matches the print. Seed 7 is a +1.7σ draw, and Onsager's 0.969 is printed beside it |
| rule density = M, other bands | MISSING | sim / Onsager: 0.80–0.90 0.931 / 0.931 · 0.90–1.00 0.801 / 0.804 · 1.00–1.10 0.367 ± 0.10 (the held side, above Tc) | 0.948 · 0.736 · **0.100** | OK / OK / low. In 1.00–1.10 the red hull encloses 0.19 of the ruled-row sites, but the rules ink only 0.10 (see advisory 1) |
| `RED HELD CLUSTER HULL MEAN 1.02 TC` | MISSING | sim hull-edge mean 1.038 ± 0.022 (5–95 %: 1.003–1.071). Sim edges 436 ± 73. Hull area 5728 ± 359 | 352 red edges, mean **1.0179**, range 0.949–1.123. Area enclosed 5339 cells. s3 1.0131 (printed 1.01), s13 1.0867 (printed 1.09) | OK. Seed 7 is at the 18th percentile |
| red = one frontier | MISSING | the outer hull of the wall cluster, wrapping in y | 3 passes of 411 mm, each continuous from y 36.4 to 188.4, sharing no edge with black or grey. It closes only once 3 seam edges are added (cols 48, 49, 51; see advisory 3) | OK (minor) |
| rules ⊂ held cluster | MISSING | — | 0 of 1,696 rule steps lie outside the red hull. The 2-step stroke at y 58.79, x 92.2–94.5 is a hull fragment, not a rule. s3 0/1667, s13 0/1913 | OK. The r05 s3 strays are gone |
| outlines per band 28 / 44 / 33 / 27 / 10 | MISSING | sim 26.0 ± 4.9 / 48.4 ± 4.8 / 33.1 ± 4.3 / 21.8 ± 4.1 / 13.5 ± 3.6 | closed faces ≥ 13: –(coast-clipped) / 45 / **33** / **27** / **10** | OK. All bands are within 1.3σ |
| mean sites per band 45.4 / 27.1 / 19.5 / 17.4 / 13.7 | MISSING | sim 38.5 ± 7.6 / 26.3 / 20.0 / 17.4 ± 1.1 / **15.9 ± 1.0** | face area – / 30.1 / 19.6 / 17.4 / 13.8 | OK against the ink. The 1.80–2.30 value is a P = 0.003 low draw for seed 7 (s3 15.1, s13 16.7 are typical) |
| strictly decreasing past 1.15 (A14) | MISSING | sim counts 48 → 33 → 22 → 14; sizes 26 → 20 → 17 → 16 | counts 44 → 33 → 27 → 10; sizes 27.1 → 19.5 → 17.4 → 13.7 | OK |
| `WEIGHT PEAKS AT TC  COUNT PEAKS PAST IT` | MISSING | size peaks in 1.00–1.15 (38.5); count peaks in 1.15–1.35 (48.4, which is also higher per 0.05 Tc: 12.1 against 8.7) | 45.4 against 27.1; 44 against 28 (7.3 against 9.3 per 0.05 Tc) | OK |
| last 25 mm column (T 2.14–2.30) | MISSING | sim 2.08 ± 1.41 outlines | 2 outlines (13 sites each). Vertical mark-free run **74.2 mm** (y 36.4–110.6). s3: 1 outline, 106 mm run. s13: 2 outlines, 77 mm run | OK. This fade is physics, not fiat |
| top rung 155+ populated | MISSING | sim P(≥ 1 per sheet) 0.51 (0.7 ± 0.8) | seed 7: 1 three-pass cluster (0.70 mm inner pass present). s3: 1. s13: **none** | OK on the plate |
| FK bond rule | MISSING | p = 1 − e^(−2J/kT), **between aligned neighbours only** | printed `FK  SPINS BONDED WITH PROB 1-EXP(-2J/T)` | OK, but the line omits "aligned" (advisory 2) |
| clearance to crimson | MISSING | HANDOFF says ≥ 0.85 mm | black min 0.850 mm, grey min 0.850 mm, 0 crossings | OK |

## Lies list
There is no dossier §4. These items come from the brief's ⚠ rules, the HANDOFF and the printed claims.

| item | clean / VIOLATED (where) |
|---|---|
| "a big domain is the critical signature" (brief ⚠) | clean. Red is the held FK frontier, printed as `MEAN 1.02`, not 1.00 |
| FK clusters passed off as spin domains | clean. `FK` is named on the ruled line and on the outline key, and is now defined |
| decorative marks posing as data | clean. The census matches the simulation band by band. The bare hot edge is the 13-site cut acting on real physics (sim 2.1 outlines in the last 25 mm) |
| the axis stretch (0.70 → 2.30) fakes the fade | clean. The fade holds on seeds 7, 3 and 13, and it matches the simulation on the same lattice |
| printed checks provable from the ink | clean on all three seeds. `AS DRAWN` is 0.984 / 0.977 / 0.982, against 0.9839 / 0.9767 / 0.9821 measured. `MEAN` is 1.02 / 1.01 / 1.09, against 1.018 / 1.013 / 1.087 |
| rule density = M (near the coast) | soft. It is clean where the check is printed. At the coast, each rule run ends 0.85 mm short, which drops the last held site's midpoint. The 1.00–1.10 band reads 0.10 where the red hull holds 0.19 (x 83.6–99.3). The HANDOFF declares the clearance; the sheet does not |
| weight ladder at the coast | soft. Where a multi-pass hull meets the clearance, its base pass is removed and the inner passes stay, so it reads one rung lighter. Example: x 84–87, y 120–137, two lines where three belong. Declared in the HANDOFF only |
| seam honesty (`TOP AND BOTTOM WRAP`) | clean for grey and black (16 seam edges drawn). The red seam edges at x 93.4–98.1 are not drawn, which leaves a detached red U at x 95.7–96.9, y 187.2–188.4 |

## Scores
- **truth 9.** Every printed number reproduces on the ink on all three seeds. Every physical claim sits inside the independent simulation's spread on the identical lattice:
  - the band census, within 1.3σ;
  - the hull mean, at the 18th percentile;
  - the drawn M, at +1.7σ;
  - the last-column fade, typical.

  One statistic is unusual: seed 7's hottest band is fine-grained, with mean sites 13.7 against 15.9 ± 1.0. It is honestly measured and printed.
- **encoding fidelity 8.** The rung ladder, the red frontier, rules inside the held cluster and the exact ruler are all clean. Three things cost points:
  - Along the coast, the 0.85 mm clearance deletes the last held site from each rule run and lightens multi-pass hulls by one pass.
  - The red seam edges are undrawn.
  - 52 faces are bounded by mixed grey and black, because an edge shared by two hulls is inked once in one colour. This was already the case in r05.
- **insight legibility 9.** Read left to right, the sheet runs:
  1. ordered sea;
  2. one red coast beside the red `1.00` tick;
  3. the heaviest outlines just past it;
  4. grey dust thinning to 74 mm of bare paper at 2.3 Tc.

  FK is now unpacked, and `WEIGHT PEAKS AT TC  COUNT PEAKS PAST IT` names the split the eye would otherwise misread.

**VERDICT: PASS** (9 · 8 · 9)

## Mandates
None (PASS). Three advisories for any later round or the fabrication gate:
1. **Coast clearance eats held ink.**
   - Problem: rule runs end 0.85 mm before red, but a site's midpoint is 0.59 mm from its wall. In 1.00–1.10 Tc (x 83.6–99.3) the rules therefore ink 0.100 of the ruled-row sites, while the red hull holds 0.19. Multi-pass hulls also lose their base pass there (x 84–87, y 120–137).
   - Fix: end rules at ≤ 0.55 mm from the coast, or put one key line on the sheet, e.g. `INK STOPS 0.85 MM SHORT OF RED`.
2. **The FK line omits "aligned".** Replace `FK  SPINS BONDED WITH PROB 1-EXP(-2J/T)` (footer, right column, line 2) with e.g. `FK  ALIKE NEIGHBOURS BONDED WITH PROB 1-EXP(-2J/T)`. Without "aligned", a physicist reads it as bond percolation.
3. **Red seam.**
   - Problem: the red frontier's seam crossing (cols 48, 49 and 51 on the y 36.4 / 188.4 line, x 93.4–98.1) is undrawn, while grey and black draw theirs. This leaves a floating red U at x 95.7–96.9, y 187.2.
   - Fix: draw the red seam edges the same way, or print that the seam is the frame.

Also, the top rung is empty on s13 (the simulation gives P = 0.51 per sheet), so seed 7 or s3 must stay the plate.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S9 (1) unpack FK | **FIXED** | `FK  SPINS BONDED WITH PROB 1-EXP(-2J/T)` is printed, as the advisory text asked. The "aligned" nuance is advisory 2 |
| S9 (2) count and size peak apart | **FIXED** | `WEIGHT PEAKS AT TC  COUNT PEAKS PAST IT` is printed and true on the ink. Size is 45.4 against 27.1; count is 28 against 44, and also per unit T (9.3 against 11.0 per 0.05). The sim agrees (38.5 / 26.3; 26.0 / 48.4). The per-band census was remeasured on the ink: the hot bands match 33 / 27 / 10 exactly |
| S10 per-seed printed values from the ink; s3 strays | **FIXED** | `AS DRAWN` against the ink is 0.984 / 0.9839, 0.977 / 0.9767 and 0.982 / 0.9821. `MEAN` against the ink is 1.02 / 1.018, 1.01 / 1.013 and 1.09 / 1.087. s3 rule steps outside the hull: 0 of 1667 (was 3) |
| S3 printed check the ink proves | holds | 0.984 = ink, and the printed row set and band are exact (13 whole columns, rows every 3rd) |
| S7 coldest band keeps its sea | holds | 43 of 43 rows ruled in 0.70–0.80; the title spine is off-lattice |
| S1 / S2 key and top rung | hold on the plate | The key matches the cuts (13 / 30 / 50 / 155). The 3-pass rung is populated on s7 and s3 but empty on s13 (the stretched axis leaves fewer columns near Tc: sim P = 0.51) |
| A14 (science side) | holds | Past 1.15, counts fall 44 → 33 → 27 → 10 and sizes fall 27.1 → 19.5 → 17.4 → 13.7, both strictly decreasing and matching the simulation |
| truth regressions vs r05 | none | The Onsager, drawn-M, hull-mean and census checks all hold on the new 0.70–2.30 axis. The one new weakness is advisory 1 (coast clearance), which is fidelity, not truth |
| process | open | dossier.md and encoding.md are still missing (5th round). The LEDGER already makes them a precondition of the fabrication gate |
