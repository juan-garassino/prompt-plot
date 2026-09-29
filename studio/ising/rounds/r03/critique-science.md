# Science critique — ising r03 · statistical physics (2D Ising at Tc) · 2026-09-28
render: gallery/studio/ising/current/pp_ising_COASTLINE_v8.png (gcode gallery/studio/ising/current/pp_ising_COASTLINE_v8.gcode, 28118 cmds, a4 portrait)

**Missing inputs (finding):** `studio/ising/dossier.md`, `encoding.md` and `LEDGER.md` do not exist.
There are no §7 check numbers, no §4 lies list and no §5 misconception. Checks below use the brief
(`studio/physics/ising.md`), the HANDOFF, and the numbers the sheet itself prints.

Method: parsed the gcode per pen. Lattice pitch fitted from wall coordinates, a = 1.0716 mm,
origin (10.699, 29.12), 176 × 240 cells, which matches the printed "176 X 240". Every dual edge was
probed at its midpoint to count parallel passes per pen. The spin field was rebuilt by wall parity
and the domains relabelled on the torus. Dust (1218 dashes, 0.44 mm, at domain centroids) was
counted per region to bound the true domain sizes.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Tc = 2/ln(1+√2) | — (brief 2.269185) | 2.2691853 | not printed ("ISING AT TC") | OK |
| Onsager unsatisfied-bond fraction (1−1/√2)/2 | — (brief 0.146447) | 0.1464466 | "ONSAGER 0.1464" | OK |
| Bonds in the drawn configuration | — | drawn walls plus wrap give 6037/84480 = 0.0715; dust domains are undrawn, and ≥4 edges × 1218 gives ≥ 0.129 | "BONDS 0.1455" | consistent; cannot be checked exactly (dust walls not inked) |
| Lattice | — | — | 176 × 240 at 1.0716 mm, every boundary edge empty (torus seam not drawn) | OK |
| Red rule: smaller domain ≥ 4096 (9.7 % of N) | — | — | red on exactly 1 domain pair (24597 / 13950 sites, dust absorbed); every red edge has exactly 4 passes; 0 edges carry both pens | OK |
| Black tiers ⌊log8 min(A,B)⌋ | — | — | 5924 / 5949 wall edges agree. The 25 exceptions are 2 small loci where undrawn dust walls confuse the reconstruction | OK |
| Tier populations (τ = 379/187 predicts ×8.46 per rung) | — | 8^(τ−1) = 8.46 | 107 (1-pass) : 8 (2-pass) : 1 (3-pass) : 2 giants, plus 1218 dust, a ratio of about ×13 and ×8 | consistent with Tc |
| Coast length, 1.1 mm "ruler" | — | red lattice edges 2232 × 1.0716 = 2391.8 mm; a true divider walk at a gives 2253.6 to 2260.1 mm | "2.39 M WITH A 1.1 MM RULER" | method mismatch: this is an edge count, not a ruler walk |
| Coast length, 4.3 mm ruler (4a = 4.286) | — | 318 steps: 1363 mm, or 1390 mm with remainders | "1.40 M WITH 4.3 MM" (not drawn) | ≈ OK (+0.7 to 2.7 %) |
| Coast length, 17 mm ruler (16a = 17.146) | — | 48 steps: 823 mm, or 905 mm with remainders | "0.95 M WITH 17 MM DOTTED". The drawn walk is **49 chords × 17.15 = 840.1 mm** (56 vertex circles, 7 walks, every chord 17.14 to 17.15) | **VIOLATED**: the dotted walk on the sheet is 0.84 m |
| Richardson dimension D = 1 − slope | — | the sheet's own three lengths give **1.333** (pairwise 1.386 / 1.280); my divider walks give 1.33 to 1.36; the drawn 0.84 m gives 1.38 | "DIMENSION 1.29" | **VIOLATED**: not derivable from the printed lengths |
| Exact hull dimension | — | spin-domain interface at Tc = SLE₃, d = 1 + 3/8 = 11/8 = 1.375 (FK would be 5/3) | "EXACT 11 OVER 8" | OK |
| Coast continuity | — | the giant-giant interface should have no interior dangling ends | 2 gaps of one edge (1.07 mm): x = 80.40, y 103.0–104.1, and x = 166.08, y 213.4–214.5. Both sit beside dust marks: an interface edge touching a sub-8 domain is dropped. The dotted walk stops at the first gap, at (78.1, 99.8) and (79.3, 107.3) | VIOLATED (minor) |

## Lies list (no dossier §4 exists, so I used the brief and the sheet's own claims)
| item | status |
|---|---|
| Grid of filled spins instead of walls | clean: walls only, dust as one touch |
| Line weight = size of the enclosed domain (log8 rungs) | clean: 99.6 % of edges verified, the rest is reconstruction ambiguity |
| Red = only the interface between the two macroscopic phases | clean: one domain pair, 4 passes |
| Printed coast lengths are what the rulers on the sheet measure | **VIOLATED**: 17 mm dotted walk inked = 0.840 m, printed 0.95 m. The 1.1 mm figure is a lattice edge count (2.39 m); a 1.07 mm divider gives 2.25 m |
| Printed dimension follows from the printed measurements | **VIOLATED**: 1.29 printed, the three printed pairs fit to 1.33 (footer line 1, y ≈ 17 mm) |
| Coastline drawn as one continuous curve | **VIOLATED (minor)**: 2 one-edge gaps where dust touches the interface (x 80.4 / y 103.6; x 166.1 / y 214.0) |
| Sampling/selection declared on the sheet | open: the brief's "SYMMETRIC SECTOR" and |m| declaration no longer appear. Reconstructed |m| is about 0.2 with dust absorbed. Declare it if the least-magnetised sample is still being selected |

## Scores
truth **7** · fidelity **7** · legibility **6** · VERDICT: **FAIL**

- truth: the physics is right. Tc, Onsager, 11/8, the tier rule, the red rule, and a configuration consistent with Tc (bond bound, τ-consistent rung counts, two coexisting giants). The plate's headline numbers are not: the dimension is not the fit of its own data, and the 17 mm length is not the dotted walk.
- fidelity: pen encoding is exemplary (exact 1/2/3/4 passes, no cross-pen overlap). But only one of the three rulers is inked, the "1.1 mm ruler" is a different method (edge count), and dust suppression cuts the coast in two places.
- legibility: "HOW LONG IS THE COAST" plus the red strands and the black 17 mm chords makes the chord-vs-wiggle idea visible. The actual Richardson insight (length grows as the ruler shrinks) exists only as one line of 2 mm type. A stranger sees one ruler, not three. There is no §5 misconception to test.

## Mandates
1. **Dimension.** Printed `DIMENSION 1.29` (footer line 1, y ≈ 17 mm, x ≈ 170 mm). The three printed (ruler, length) pairs, (1.07, 2.39), (4.29, 1.40), (17.15, 0.95), fit to D = **1.333**. My independent divider walks on the gcode's red lattice give 1.33 to 1.36. Print the slope of the numbers actually shown on the sheet, from one stated fit. If more rulers go into the fit, print them.
2. **Lengths must be the marks.** The 17 mm dotted walk inked on the sheet is 49 chords × 17.146 mm = **0.840 m**, printed **0.95 m**. The ≈110 mm difference is undrawn tails and fragments. The "1.1 mm ruler" figure 2.39 m is 2232 lattice edges × 1.0716 mm (a Manhattan count). A divider walk at 1.07 mm gives **2.25 m**. Use one method at all three rungs (divider with the same remainder rule), and make the dotted rung equal what is inked: draw the tails, or print 0.84 m.
3. **Coast continuity + the missing rung.** The red interface has 2 dangling gaps of one lattice edge each, at (x 80.40, y 103.0–104.1) and (x 166.08, y 213.4–214.5). They appear where a dust domain touches the interface and its edge is suppressed, and the walk dies at the first gap ((78.1, 99.8) / (79.3, 107.3)). Expected: 0 interior dangling ends, with interface edges inked red regardless of the dust rule. Also, the 4.3 mm rung (318 steps, ≈1.36–1.39 m) has no mark anywhere. Ink it on at least one shared stretch, e.g. the 769-edge strand from (199.3, 153.4) to (196.1, 29.1), so all three rulers can be compared on the paper and not only in the footer.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | `studio/ising/LEDGER.md` does not exist; no S* mandates to follow up |
