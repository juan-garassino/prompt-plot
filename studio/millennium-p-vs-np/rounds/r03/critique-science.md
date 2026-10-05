# Science critique — millennium-p-vs-np r03 · theoretical computer science (computational complexity) · 2026-09-29
render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_iterate_v3.png (+ `_phys.png`; gcode `_v3.gcode`, 17,641 cmds)

Method: blind. I did not open piece.py, NOTES.md, audit.py or data/search.py. Everything was recomputed
from `data/uf20-03.cnf` (sha256 23bbf1db… matches §3). I wrote my own brute-force check over all 2^20
assignments, my own chronological backtracking, DPLL and Hamiltonian DFS, and a gcode parser. That
parser splits the gcode into 155 / 226 / 1,013 / 92 strokes on layers 0 / 1 / 2 / 3. It then matches
every sampled point of layers 0, 1 and 3 in polar coordinates about the hub (148.5, 148.5)
(0° at 12, clockwise) against the ideal tree geometry.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | candidate space | 2^20 = 1,048,576 | 1,048,576; brute force gives exactly 1 model, k = 1,015,453 | caption "THE DISC IS ALL 1,048,576 CANDIDATES" | OK |
| 2 | tree nodes / conflicts / models | 8,047 / 4,023 / 1 | 8,047 / 4,023 / 1. Preorder start angles are non-decreasing (search time = angle holds) | drawn: preorder ≤ 7,812 (3,903 conflicts). Layer 1 (depths 0–8): 13,742 samples, 0 off-geometry, worst deviation 0.007 mm. Every pre-model element is present | OK |
| 3 | certificate angle | 348.628° | 348.6281° (1,015,453 / 2^20) | red crosses r = 128 at 348.6277°, needle tip 348.6289° at r = 256.99 (97.83, 400.45) | OK |
| 4 | red node centres d1–d5 | 270, 315, 337.5, 348.75, 343.125 | same, then 345.94, 347.34, 348.05 … | measured 270.0, 315.0, 337.495, 348.76, 343.122, 345.938, 347.338, 348.051, then converging to 348.628 at d20. The red follows the exact path at all 20 depths. 1,579 samples: only the root stub (hub → r 3.2 at 180°, the root's own centre angle) falls outside my ideal set; everything else is on-geometry | OK |
| 5 | discovery at preorder | 7,812 / 8,047 = 0.9708 | 7,812, 0.97080 | caption "7,812 NODES. FOUND AT 11:37": 348.628° / 30° = 11 h 37.3 min | OK |
| 6 | first pruning at depth 6 (8 conflicts), none at depth ≤ 5 | 8 | 8 in total, 7 pre-model at 194.06, 216.56 … 329.06°; the 8th at 351.56° comes after the model | the exact layer-1 tree implies 7 ends at ring 6 and none inside ring 5 | OK |
| 7 | widest level; live fraction at d12 | d13: 1,284 / 493; 0.157 | 1,284 / 493; 642/4096 = 0.1567 | not drawn node-for-node (aggregated past ring 8, declared) | OK |
| 8 | false needles (depth-20 conflicts) | 75 | 75 in total, 69 pre-model (3 in the model's sector 247) | 13 black rim contacts (169.5, 227.1, 235.5, 249.6, 258.0, 280.5, 303.0, 317.1, 325.5, 332.6, 334.0, 336.8, 339.6°) carry 66 of them. Only 169.5° lies in the x1 = F half | OK (not named on the sheet, see M3) |
| 9 | verification | 91 checks, 273 lookups, 41/36/14 | 91; 41/36/14; closing-variable groups [1,3,1,2,3,4,5,4,8,13,7,12,10,18] | 91 red ticks, pitch 1.345–1.357 mm, r 134.67–256.18. Lengths 1.50 ×41, 2.75 ×36, 4.00 ×14. 14 side-alternating groups match the closing-variable groups exactly. The tick sequence matches clause order (closing var, then file order), rim outward: 91/91 | OK |
| 10 | DPLL (unit propagation) | 87 nodes; mean 6,792 over uf20-91 | 87 nodes, first model at node 82, 43 conflicts. My implied-literal count is 335, against the dossier's 446 (a convention difference; not on the sheet). 6,792 not recomputed (needs the tarball; not captioned) | caption "DPLL FINDS IT AT NODE 82" | OK |
| 11 | Hamiltonian search (b)/(c) | 12,538/2,958/162/60; 274/48/24/0 | identical (dodecahedron LCF, Petersen) | not drawn | OK |
| 12 | resolution d8 / d9 at R 130 | 1.28 / 0.72 mm | 1.276 / 0.718 | R 128: ring-8 spoke gap is 1.248 mm at its tightest | OK |
| — | clause tests to find / whole tree (encoding) | 43,658 / 45,088 | 43,658 / 45,088 (each clause tested at its last variable) | "43,658 … EACH CLAUSE TESTED AT ITS LAST VARIABLE" against "91 TO CHECK" | OK |
| — | aggregates past ring 8 (encoding) | 140 (139 black + red) | 140; crossing counts 140×4, 125, 99, 95, 72, 42, 29, 19, 14 | 139 black hairlines, each at its sector centre (±0.01°), r 51.20 → deepest ring (±0.05 mm), plus the red. The crossing counts match exactly | OK |
| — | rim / hour ticks | r 128; 12 ticks at [129.5, 133.5] | — | 4 arcs, 804.34 mm (2πR = 804.25). 12 ticks at 0, 30, … 330°, r 129.5–133.5 | OK |
| — | black in the wedge 348.628° → 360° | none | — | 0 black vertices inside r < 128 | OK |
| — | red to nearest black past ring 8 (encoding §10 says ≥ 1.77 mm) | 1.77 | angular gap 1.41° × r 52 = 1.28 | **1.286 mm** (red d8 spoke 348.05° against the sector-246 hairline 346.64° at r ≈ 52). This is ≥ 0.8, so the sheet is fine; **encoding §10's 1.77 is wrong** | encoding error |
| — | red to type / type inside disc | ≥ 10 mm; none | — | 10.74 mm; the nearest type is 151.3 mm from the hub (outside the tick ring) | OK |
| — | feeds / dwells | F600, G4 P1.0 | — | 10,210 G1 at F600, 0 at F2000; 2,973 × G4 P1 | OK |

## Lies list
| item | status |
|---|---|
| 1 tree that merges | clean: 0 off-geometry samples, stem/fork/branch only |
| 2 invented or decorative branching | clean: every layer-1 element is a real pre-model node; all 139 hairlines are exact aggregates, none extra |
| 3 complete 2^20 tree | clean: rings 1–5 complete, pruning from ring 6, 14 lines reach the rim |
| 4 more than one red / short / wrong angle | clean: one red path, reaches r 128 at 348.6277°, collinear to r 257 |
| 5 verification as 1 or 20 ticks | clean: 91 ticks, lengths and grouping exact |
| 6 "tree proves P ≠ NP" | clean: "THIS SEARCH, NOT THE PROBLEM … A SHORTCUT FOR EVERY CASE? OPEN." |
| 7 "NP = not polynomial" | clean: "NP: CHECKED IN POLYNOMIAL TIME" |
| 8 maze metaphor | clean |
| 9 blue waypoint / node marks | clean: no dots or circles. The hub half-circles are the root fork at r 3.2 |
| 10 m/n 4.26 | clean: "M/N = 4.55" |
| 11 dodecahedron as image | clean (not drawn) |
| **new: key caption vs. the drawn search** | **VIOLATED (left-column key, y ≈ 322, "BLANK PAPER IS REFUTED.")** The plate draws only the search up to the needle. The blank wedge 348.628° → 360° (≈ 11 o'clock 37 to 12) holds **33,122 candidates (3.16 % of the disc) that were never searched**, not refuted. The caption turns one of the plate's three designed silences into a false claim. The drawn search refutes 1,015,453, not 1,048,575. (Source: my own r02 S2 wording, "BLANK PAPER IS REFUTED (1,048,575)". The designer rightly dropped the number, but the sentence still over-claims.) |

## Scores
truth **7** · fidelity **9** · legibility **8** · VERDICT: **FAIL**

- **Truth.** Every drawn coordinate and every number is right. One sentence in the key is false about a visible region: the unsearched wedge is called refuted. A secondary softness: P ⊆ NP is still not stated.
- **Fidelity.** Exact to 0.01 mm and 0.01° on all three data layers. Tick length, side and order encode their clause 91/91. The aggregation is stated.
- **Legibility.** The 43,658-against-91 pair now lands as one unit, the key exists, and the method caveat is there. What is missing: the wedge's meaning, and the reason 13 thin lines touch the rim.

## Mandates
1. **The wedge is unsearched, not refuted.**
   - Where: the key line "BLANK PAPER IS REFUTED." in the left column (y ≈ 322).
   - Measured: the caption implies all blank paper (1,048,575 candidates) is refuted.
   - Expected: the drawn search refutes **1,015,453**. The sliver from the red to 12 o'clock (348.628° → 360°) is **33,122 candidates (3.2 %) the search never needed to visit**.
   - Fix: reword to, e.g., "BLANK PAPER IS REFUTED — EXCEPT THE SLIVER AFTER THE RED: NEVER SEARCHED." Keep the wedge empty.
2. **Finish the P / NP definitions (S2 residue).**
   - Where: the bottom of the left column (y ≈ 280–285).
   - Measured: "P: FOUND IN POLYNOMIAL TIME. NP: CHECKED IN POLYNOMIAL TIME." It has no certificate and no inclusion.
   - Expected: r01's cleared text, which the ledger merge named. "NP: CHECKED IN POLYNOMIAL TIME, GIVEN A CERTIFICATE (THE RED)." plus "P IS INSIDE NP. EQUAL? OPEN." The certificate is the red, so the definition should point at it. P ⊆ NP is the dossier §5 secondary correction, and it is absent from the sheet.
3. **Name the false needles.**
   - Where: the 13 black hairlines that touch the rim (listed in check 8). All but 169.5° lie between 227° and 340°.
   - Measured: the key says only "THIN LINE: ONE BRANCH'S DEEPEST REACH", so nothing on the sheet says a rim contact is a complete 20-bit candidate that failed only at the last check.
   - Expected: one key line, "A THIN LINE THAT TOUCHES THE RIM: COMPLETE CANDIDATES THAT FAILED THE LAST CLAUSE (69 BEFORE THE NEEDLE)". Recomputed: 69 pre-model depth-20 conflicts in 14 sectors, 66 of them on the 13 black lines and 3 inside the red's sector. This carries dossier §2's "false needles, indistinguishable until checked", the plate's argument that checking, not finding, tells needle from straw.

Not a sheet mandate (note for the encoding owner): encoding §10's "red to nearest black past ring 8 ≥ 1.77 mm" should read **1.29 mm** (measured 1.286). It still clears 0.8 mm.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 | **FIXED** | "DPLL FINDS IT AT NODE 82": recomputed model at node 82 of 87. "EACH CLAUSE TESTED AT ITS LAST VARIABLE" sits under 43,658 (recomputed 43,658). Both counts are on a find basis |
| S2 | **PARTIAL** | Key present: "THE DISC IS ALL 1,048,576 CANDIDATES. EACH BRANCH'S ANGLE IS ITS EXACT SHARE." The hairline is re-worded in plain language ("THIN LINE: ONE BRANCH'S DEEPEST REACH"). The P/NP definitions are shortened, with no certificate and no P ⊆ NP (→ M2). "BLANK PAPER IS REFUTED" over-claims the wedge (→ M1) |
| S3 | **FIXED** | "HOUR TICK: 1/12 OF THE CANDIDATES, REACHED CLOCKWISE, NOT EQUAL TIME." The 12 ticks are measured at 30° spacing, r 129.5–133.5 |
| S4 | **FIXED** | red to nearest type: 10.74 mm (≥ 10) |
| A2 (science half) | **FIXED** | 10,210 G1 at F600, 0 at F2000; 2,973 dwells of G4 P1 (G0 rapids carry no feed, which is the art/fab critic's call) |
| regressions | none | pens 0, 1 and 3 are exact against my own recomputation. Every truth that held in r02 still holds |
