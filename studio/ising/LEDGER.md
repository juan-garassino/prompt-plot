# Ledger — ising
**Best so far:** r04 — art 6.71/6 · sci 8/7/7 — ~/Downloads/pp_ising_r04_iterate_v5.png
**Route:** designer
**Round cap:** 5 designer rounds per encoding (DESIGN_RUBRIC). Used: r02 and r03 (parallel) and r04. r05 is the 4th round and r06 the last before a forced vote.
**Process gap:** `dossier.md` and `encoding.md` are still missing (science critic, third round running). The critic has been using an independent SW simulation in their place. A translator pass should write `encoding.md` from the r04 HANDOFF plus the science-critic check table before any vote.

## Rounds
| round | parent | thesis | render | art avg/min | sci t/f/l | verdict | note |
|---|---|---|---|---|---|---|---|
| r01 | — | CRITICAL: Tc hero + 5-plate axo deck + m(T) chart + footer | gallery/studio/ising/current/pp_ising_v6.png | — | — | uncritiqued (baseline) | Seeded the ledger via DESCRIPTION.md. No critic pass |
| r02 | r01 | COOLING STRIP: one landscape lattice, T 0.70→1.80 Tc along x. Ruled sea = held FK droplet, crimson hull = the frontier at 1.03 Tc | ~/Downloads/pp_ising_COOLING_STRIP_v9.png | 5.86 / 4 | 8 / 7 / 7 | FAIL / FAIL | Physics verified independently. Failed on: no bare paper, dot carpet, clotted 3-pass sticks, caption-size title, no key. Its visible hot-side coarsening gradient is now the thing r05 must win back (A14) |
| r03 | r01 | COASTLINE: full-bleed Tc torus, log8 ladder, dust as touches, Mandelbrot divider walk | ~/Downloads/pp_ising_COASTLINE_v8.png | 5.43 / 4 | 7 / 7 / 6 | FAIL / FAIL | Kept on disk as the COASTLINE flavour (S4–S6, A13 parked) |
| r04 | r02 | MERGE: r02 sheet + closed dual-lattice FK hulls (cut 30, 1/2/3 passes at 30/50/155), vertical 18 mm CRITICAL spine, FK key, Onsager-m check | ~/Downloads/pp_ising_r04_iterate_v5.png | 6.71 / 6 | 8 / 7 / 7 | FAIL / FAIL | **rank 1 (best).** Closed A2 A4 A6 A9 A10 A11 A12 S1 S2 (both critics confirmed). Draw 20.8→11.5 m, travel 0.55×. New problems: the hot half no longer reads as heat (grain deleted, not thinned), the weight ladder is invisible at 1 m (0.06/0.13 mm offsets), the title slot blanks the coldest band (truth regression vs r02), footer type sits on the rules |

## Mandates
| id | raised | by | mandate | status | closed |
|---|---|---|---|---|---|
| A1 | r01 (DESC) | art | Lower half is a scientific figure (deck + m(T) chart + colophon): delete | fixed | r02 |
| A2 | r01 (DESC) + r02 art M1 | art | No isolated single-site / tiny-droplet dots. 40×40 crop x 230–270, y 20–60 has zero isolated dots and ≥ 50 % bare; travel ≤ 0.6 × draw | fixed | r04 (art: 0 isolated, ≥ 50 % bare, travel 0.55). Must stay fixed under A14 |
| A3 | r01 (DESC) | art | One type face, one left axis | fixed | r02 |
| A4 | r01 (DESC) + r02/r03 | art | Genuinely bare paper on the hot side (≥ 25 %, a 60×80 mark-free rectangle) | fixed | r04 (art: x 250–287 mark-free, 60×80 block exists). **Test superseded from r05** by A14's "each 20×20 cell in 1.55–1.80 stays ≥ 50 % bare". The art critic's r04 note says the bare paper must be *shaped by the gradient*, not just be the data running out. The 60×80 rectangle is retired because it contradicts A14 |
| A5 | r01 (DESC) | art | Ragged halo hole behind the title | dropped | merged into A10 |
| A6 | r01 (DESC) + r02 | art | Declare flat + `canon:` / `lineage:` in HANDOFF | fixed | r04 |
| A7 | r01 (DESC) | art | Cold phase has no visual body | fixed | r02 |
| A9 | r02 | art M2 | Frontier thicket x 85–130, y 120–180: ≥ 0.8 mm clear between distinct parallel strokes, no solid cell > 2×2 mm | fixed | r04. Must hold while A15 widens the passes |
| A10 | r02 | art M3 | CRITICAL cap ≥ 18 mm, 2–3 passes, flush-left x = 15, no rule stubs < 4 mm | fixed | r04 (vertical spine). Its slot halo is now the cause of S7 |
| A11 | r02 | art | Free droplets as closed dual-lattice wall loops, not bond sticks | fixed | r04 |
| A12 | r03 | art M1 | One continuous crimson coast | fixed | r04 (1 component, 461 edges; science critic concurs) |
| A13 | r03 | art M3 | Ruler joke (divider walks) | dropped | COASTLINE flavour only |
| A14 | r04 | art M1 (+ r02 regression) | **Make the hot half visibly hot.** Across the bands T/Tc 1.15–1.35, 1.35–1.55 and 1.55–1.80, mark count and mean mark size strictly decrease band to band. The 1.55–1.80 band has ≥ 1 mark in most 20×20 mm cells and every such cell stays ≥ 50 % bare. No dots | open | — |
| A15 | r04 | art M2 | **Weight ladder reads at 1 m.** A ≥ 155-site hull stroke renders ≥ 2.5× the width of a 30–49-site stroke (3-pass band ≈ 0.6–0.8 mm solid) without breaking A9's 0.8 mm clear between distinct hulls | open | — |
| A16 | r04 | art M3 (+ r04 regression) | **Type off the rules and in tiers.** Every colophon line has ≥ 1.2 mm bare paper above and below. `TC IS A PLACE` is its own line at cap ≥ 5 mm, separated from the colophon | open | — |
| A17 | r04 | art dim 4 | Upper-left pocket x 57–95, y 165–185: sea rules stop 20–35 mm short of the red hull. Either they are drawn to the coast, or the pocket is a genuine minority lake and reads as one | open (deferred, 5-cap) | Verify in NOTES only. It may be true data |
| S1 | r02 | sci M1 | On-sheet key naming FK, rung site ranges, `SINGLE SPINS NOT DRAWN` | fixed | r04 (science confirmed). Its text must be updated if A14 changes the cut |
| S2 | r02 | sci M2 | 3-pass rung populated in the typical config (≥ 155) and uniform | fixed | r04 (seeds 7/3/13 all populated, 0 % under-inked) |
| S3 | r02 | sci M3 | The printed check must be one the ink proves: rule density vs Onsager–Yang m, band and row set stated | open (PARTIAL r04) | The 0.977 names the band the title blanked. Closes with S7 plus a restated line |
| S4 | r03 | sci M1 | Printed D = fit of printed lengths | dropped | COASTLINE only |
| S5 | r03 | sci M2 | Printed coast lengths = inked walks | dropped | COASTLINE only |
| S6 | r03 | sci M3 | Coast continuity + 4.3 mm rung | dropped | COASTLINE only. Its lesson (coast inked regardless of the cut) still applies |
| S7 | r04 | sci M1 (truth regression vs r02) | **Give the coldest band back its sea.** Rows y 57.7–186.4 at T/Tc 0.70–0.80 carry 0.000 under the title slot where 0.97 is true. Break rules only within ~1 mm of glyph strokes (letter-shaped halo). Every ruled row in 0.70–0.80 reads ≥ 0.95, and 0.800–0.825 reads ≈ 0.95 | open | — |
| S8 | r04 | sci M3 + art acceptance | **Say what a stranger can't infer.** The colophon gains `TC 2.269185 ONSAGER 1944 EXACT`, a line tying rule density to the magnetisation M, and a line naming the hot blank as disorder finer than the cut (no longer `NOR UNDER 30` alone) | open | — |
