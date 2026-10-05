# Science critique — millennium-p-vs-np r02 · theoretical computer science (computational complexity) · 2026-09-29
render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_abstract_v3.png (+ _phys.png, .gcode 16,669 cmds; 4 layers: 155 / 226 / 910 / 92 pen-down strokes)

Method: independent backtracking re-implemented from `data/uf20-03.cnf` (sha256 matches the dossier),
brute force over all 2^20 assignments, and my own DPLL and Hamiltonian searches. None of the designer's or
the dossier's .py files were opened. The gcode was parsed per `; color=N` layer and every drawn sample
was polar-mapped about the hub (148.5, 148.5), then matched against the recomputed tree.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | candidate space / refuted mass | 1,048,576 / 1,048,575 + 1 | 1,048,576 / 1,048,575 + 1 (brute force: 1 model, k = 1,015,453) | caption "1,048,576 CANDIDATES. ONE FITS ALL 91" | OK |
| 2 | tree nodes / conflicts / models | 8,047 / 4,023 / 1 | 8,047 / 4,023 / 1 | Drawn up to the model: all 679 expected spokes and 226 expected fork arcs present (depths 0–8), plus 139 hairlines. 0 unexplained samples in 16,027 black-layer samples. | OK |
| 3 | certificate angle | 348.628° | 348.6281° | Red crosses the rim (r = 128.000) at **348.6277°**, at (123.26, 273.99). The outer needle is collinear at 348.6289°. Tip at r = 256.99. | OK |
| 4 | red node-centre angles d1–5 | 270 / 315 / 337.5 / 348.75 / 343.125 | same | 270.000 / 315.000 / 337.500 / 348.756 / 343.124. d6–d20 all within 0.004° of exact. It zigzags on the stem-fork-spoke geometry. | OK |
| 5 | discovery preorder | 7,812 / 8,047 = 0.9708 | 7,812, 0.97080 | Caption "7,812 NODES". Nothing is drawn past 348.628° (0 black samples in the wedge). | OK |
| 6 | first pruning at d6 (8 conflicts); none at d ≤ 5 | yes | 8 at d6 (centres every 22.5°, 194.06 → 351.56°). 7 of them come before the model. | 7 black spokes stop at ring 6: 194.1, 216.6, 239.1, 261.6, 284.1, 306.6, 329.1°. Rings 1–5 are complete. | OK |
| 7 | widest level / live fraction d12 | d13 1,284 / 493; 0.157 | 1,284 / 493; 642/4096 = 0.1567 | Hairlines crossing ring 13 = 125 (+red), matching the recomputed aggregate for the truncated search. | OK |
| 8 | false needles (d20 conflicts) | 75 | 75 (69 before the model) | 13 black hairlines reach the rim, at 169.5, 227.1, 235.5, 249.6, 258.1, 280.5, 303.0, 317.1, 325.5, 332.6, 334.0, 336.8, 339.6°. That is exactly the recomputed set of depth-8 sectors with depth-20 descendants. The 14th sector (348.05°) is the red's. | OK (aggregate, declared) |
| 9 | verification 91 checks / 273 lookups / 41·36·14 | yes | 91 / 273 / 41·36·14 | 91 red ticks at pitch 1.350 mm (1.345–1.357), r 134.7–256.2. Lengths are 1.5 mm ×41, 2.75 ×36 and 4.0 ×14. Order by closing variable matches 91/91, inner→outer. There are 14 groups with alternating sides. | OK |
| 10 | DPLL nodes / uf20-91 mean | 87 (first model at 82) / 6,792 | **87 total, first model at node 82**, 43 conflicts. The 6,792 mean was not recomputed (tarball not local; not captioned). | Caption says "UNIT PROPAGATION **FINDS** THE SAME NEEDLE IN **87** NODES". | **WRONG ON SHEET**: it finds the needle at node 82; 87 is the exhaustive tree |
| 11 | dodecahedron / Petersen | 12,538/2,958/162/60 · 274/48/24/0 | identical | not on this plate | OK |
| 12 | sibling gap d8 @R130 / d9 | 1.28 / 0.72 mm | 1.276 / 0.718 | At R = 128 the hairlines start 1.249 mm apart (min) at r = 51.2 | OK |
| — | encoding: 43,658 clause tests to model | 43,658 | 43,658 **only under no short-circuit** (every clause tested at its closing node). A short-circuiting checker makes 30,403. | Caption "43,658 CLAUSE TESTS", with the convention unstated | caveat |
| — | encoding: red to nearest black past ring 8 ≥ 1.77 mm | ≥ 1.77 | — | **1.28 mm** centre-to-centre (still ≥ 0.8 floor) | encoding claim off, not a science fail |

## Lies list
| item | status |
|---|---|
| 1 tree that merges | clean. Every black sample lies on its own node's spoke, stub or fork, and forks are disjoint by construction. |
| 2 invented branching | clean. 0 unexplained samples. The 139 hairlines = the 140 live depth-8 sectors minus the red's, each ending exactly at its sector's deepest ring (0 mismatches). |
| 3 complete 2^20 tree | clean. It prunes from ring 6, and 14 of 140 lines reach the rim. |
| 4 red count / angle / short of rim | clean. There is one red path, it reaches the rim at 348.6277°, and there is no other red element except its own 91 ticks. |
| 5 verification as 1 or 20 ticks | clean. 91 ticks. |
| 6 "tree proves P ≠ NP" | clean. "THIS SEARCH, NOT THE PROBLEM … A SHORTCUT FOR EVERY CASE? OPEN." (But the DPLL count quoted there is wrong; see Mandate 1.) |
| 7 "NP = not polynomial" | clean. Nothing false is said, though P and NP are never defined. |
| 8 maze | clean |
| 9 waypoint circles / node marks | clean. There are no dots or circles anywhere. |
| 10 m/n 4.26 | clean. "M/N = 4.55" |
| 11 dodecahedron | n/a |

## Scores
- **truth 7.** Every drawn coordinate is exact: angles to within 0.004°, all 905 tree elements present, and nothing invented. But one caption is false: "finds the same needle in 87 nodes". DPLL finds it at node 82; 87 is its full tree. The sheet therefore compares a find-count (7,812) with an exhaust-count (87). The 43,658 figure also rests on an unstated no-short-circuit convention.
- **fidelity 8.** All data channels are exact and weight-coded as declared. The 12 hour ticks are an uncaptioned scale: they mark equal shares of candidates, not equal time (see Mandate 2).
- **legibility 7.** The needle and the 91-tick check land. But the sheet never says the disc IS the 1,048,576 candidates, that angle = each branch's exact share, or that blank paper = refuted assignments. That is the core reading. The key uses jargon ("HAIRLINE", "X8 SUB-TREE").
- **VERDICT: FAIL**

## Mandates
1. **DPLL count, bottom-right spandrel (x 235–282, y 15–36).** It reads "FINDS THE SAME NEEDLE IN 87 NODES". Recomputed, DPLL with unit propagation (same order, false first) reaches the model at **node 82**; 87 is the exhaustive tree. Change it to **82**, which is the same find-basis as the 7,812 in the bottom-left. In the bottom-left spandrel, also state the clause-test convention, e.g. "43,658 CLAUSE TESTS (EACH CLAUSE AT ITS LAST VARIABLE)". A short-circuit checker makes 30,403, so the number is convention-dependent.
2. **Hour-tick scale, 12 ticks at r 129.5–133.5 every 30° (layer 0).** Uncaptioned, and "CLOCKWISE FROM 12 … FOUND AT 11:37" invites reading them as equal time. Measured, they mark equal candidate shares (87,381⅓ each), not equal search time:
   - At the 6 o'clock tick only **31.5 %** of the 8,047 nodes are done (3.78 h of "node time" against 6 h).
   - The largest gap between node fraction and angle fraction is **19.1 % of the sweep, at 168.75°**.

   Expected: one caption line stating "EACH TICK = 1/12 OF THE 1,048,576 CANDIDATES; THE SEARCH REACHES THEM IN CLOCKWISE ORDER". 11:37 is correct as a dial position, and the node-time equivalent is 11:39.
3. **The dial's reading key, instance block (x 15–88, y ≈ 285–305).** Currently 0 lines on the sheet tie the disc to the 2^20 candidates. Expected: one plain line, "THE DISC IS ALL 1,048,576 CANDIDATES; EACH BRANCH'S ANGLE IS ITS EXACT SHARE; BLANK PAPER IS REFUTED (1,048,575)". Also replace "HAIRLINE: EACH X8 SUB-TREE AS ONE LINE" with plain wording such as "PAST RING 8, EACH THIN LINE IS ONE BRANCH'S DEEPEST REACH". Optional: one short line on P ⊆ NP, so the title's two letters are defined.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | There is no `studio/millennium-p-vs-np/LEDGER.md` and no r01 science critique, so this is the first science pass. r02 is the abstract thesis; r01 was the faithful one. |

Out-of-scope notes (not scored):
- The gcode draws at F2000 with G4 P0.2 dwells, while the HANDOFF times assume F600 and Leo's standing rule is P1.0 dwells.
- Red to title/caption is 6.2 mm; the encoding asks ≥ 10.
- The first hairline stroke starts at 235°, not clockwise from 12 as the encoding's batching specifies.
