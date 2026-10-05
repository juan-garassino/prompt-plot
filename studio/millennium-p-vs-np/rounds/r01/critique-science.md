# Science critique — millennium-p-vs-np r01 · theoretical computer science (computational complexity) · 2026-09-29
render: gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.png (+ _truewidth.png; gcode gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.gcode)

Method: the search was recomputed from scratch on `data/uf20-03.cnf` (sha256 matches the dossier) with a new
backtracker, a numpy brute force over all 2^20, a new DPLL, and a new Hamiltonian path enumerator.
None of the designer's .py was opened. The gcode was parsed per `; color=N` layer (0: 111 strokes,
1: 191, 2: 1055, 3: 93), and every mark was compared against the expected geometry.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | candidate space, refuted + model | 2^20 = 1,048,576; 1,048,575 + 1 | 1,048,575 + 1 (brute force: 1 model, k = 1,015,453) | caption "2^20 = 1,048,576 candidates. One satisfies all 91" | OK |
| 2 | tree nodes / conflicts / models | 8,047 / 4,023 / 1 | 8,047 / 4,023 / 1 | caption "8,047 nodes". Rows 0–7: all 239 nodes drawn exactly (58,415 of 58,415 raster samples, 0 missing, 0 extra, within 0.05 mm). Below row 7: 111 hairlines + red = 112 depth-7 sectors, each x and depth exact (0 bad) | OK |
| 3 | certificate position | 348.628° (m = 0.968428) | 348.628° | red ends at x = 273.57, y = 100.0, so m = 0.968427 (348.634°, gcode rounding 0.01 mm) | OK |
| 4 | red centres d1–d5 | 270 / 315 / 337.5 / 348.75 / 343.125° | same | red x 215.25 / 248.62 / 265.31 / 273.66 / 269.48 = expected to 0.01 mm. All 20 steps, stem-fork-drop, match to 0.01 mm | OK |
| 5 | discovery at preorder | 7,812 / 8,047 = 0.9708 | 7,812, 0.97080 | not captioned. Implied by x only. 3 hairlines to the right of the red (post-discovery strip present) | OK (not stated, see M2) |
| 6 | first pruning | depth 6, 8 conflicts | depth 6, 8 | rows 0–5 complete; exactly 8 row-6 drops end with no fork | OK |
| 7 | widest level / live fraction d12 | d13 1,284 / 493; 642/4096 = 0.157 | 1,284 / 493; 0.15674 | below aggregation depth; declared not encoded | OK (declared) |
| 8 | false needles at d20 | 75 | 75 | 14 black hairlines reach row 20 (+1 red = 15 depth-7 sectors reach d20, recomputed 15). Sector-level, as declared | OK |
| 9 | verification | 91 checks, 273 lookups, 41/36/14 | 91, 273, 41/36/14 | 91 red ticks; lengths 1.5/2.75/4.0 mm × 41/36/14; the sequence matches closing-variable order exactly; side alternates across the 14 groups (6, 8…20) exactly. Rule y = 62, x 148.5→273.57, right end on the red axis | OK |
| 10 | DPLL / uf20-91 mean | 87 nodes (first model at 82, 43 conflicts); mean 6,792 | 87, 82, 43 (implied literals 335 vs 446, convention; not captioned); mean not rerun | caption "unit propagation needs 87 nodes"; mean not captioned | OK |
| 11 | dodecahedron / Petersen | 12,538/2,958/162/60 ; 274/48/24/0 | same | Petersen tree: 274 nodes, per level 1,3,6,12,24,36,48,60,60,24 = recomputed; 72 leaves (12 d7 + 36 d8 + 24 d9) = 48 dead + 24 paths; min parallel gap 1.10 mm; zero red | OK |
| 12 | resolution | 1.28 / 0.72 mm | 1.276 / 0.718 | [F] actual: min depth-7 drop gap 2.086 mm (267/128) | OK |
| — | caption "45,088 clause tests" | — | 45,088 = every clause closed at each generated node, no early exit; with early exit on the first false clause it is 31,371 | caption states 45,088 without its convention | minor |

## Lies list
| item | status |
|---|---|
| 1 merging tree | clean. All tree ink is axis-aligned stem/bar/drop. The geometry equals the recomputed tree, so nothing rejoins |
| 2 invented branching | clean. 0 extra samples. Hairlines are exact deepest-depth aggregates (111/111) |
| 3 complete 2^20 fan | clean. Pruning is visible from row 6 |
| 4 red count / angle / short | clean. There is one red path, it ends at row 20, and its end is at 348.63° |
| 5 verification as 1 or 20 ticks | clean. There are 91, and the caption says "polynomial in the input" nowhere wrongly |
| 6 tree proves P ≠ NP | clean for the SAT half ("this search, not the problem: unit propagation needs 87 nodes"). **The Petersen caption comes close. See below** |
| 7 NP = not polynomial | clean ("NP: answers checked in polynomial time, given a certificate. P is inside NP") |
| 8 maze | clean |
| 9 waypoint circles / node marks | clean. No dots or circles in any layer. START/SOLUTION are type, not marks |
| 10 m/n = 4.26 | clean. Not captioned |
| 11 dodecahedron figuration | clean. Not drawn |
| encoding §9 7 (type in field) | clean. There is no type-layer ink with 100 < y < 350 |
| encoding §9 12 (post-discovery strip) | clean. It is present |
| **caption truth (bottom-left, y ≈ 23–35): "NO HAS NO CERTIFICATE"** | **VIOLATED (truth)**. NP promises a short certificate only for YES. Whether NO instances of Hamiltonian cycle have short certificates is the open NP vs coNP question. An unconditional "no certificate" asserts a separation that would imply P ≠ NP. For this very instance it is also false: the Petersen graph's non-Hamiltonicity has a well-known one-paragraph proof (a Hamiltonian cycle uses an even number of the 5 spokes; the 2- and 4-spoke cases each fail). The sheet only shows that *this search* offers no red, not that no certificate exists |

## Scores
truth 7 · fidelity 9 · legibility 7 · VERDICT: FAIL

- **truth 7.** The drawn science is exact to the gcode's 0.01 mm. The one false sentence sits on the companion that carries the NO half of the argument.
- **fidelity 9.** Every channel is quantitative and was measured exact. The only deviation is the chain pitch: 1.374 mm over x 148.5–273.57, against the encoding's 1.35 mm over 150.7–273.57. That is cosmetic.
- **legibility 7.** The SAT-side misconception correction lands ("this search, not the problem … 87 nodes"). But nothing on the sheet tells a stranger the three rules that make the picture readable. The tick channels are also unkeyed.

## Mandates
1. **Petersen caption truth (bottom-left block, y ≈ 23–35 mm).**
   - Measured: "NO HAS NO CERTIFICATE … NOTHING RED."
   - Expected: a claim the sheet can support. For example: "NP promises a short certificate only for YES. This search finds none: all 274 nodes, nothing red. Whether every NO has a short proof is open (NP vs coNP)."
   - Do not state or imply that NO instances provably lack certificates. For this graph one exists (the spoke-parity proof).
2. **The key to the field is missing (finding caption, y ≈ 23–35 mm, x ≥ 148).**
   - Measured: 0 of 3 reading rules appear on the sheet. Nowhere does it say that x is the exact share of the 1,048,576 candidates (each row-7 column = 8,192), that a line that stops is a partial assignment refuted by a clause, or that left→right is search order.
   - The discovery point, node 7,812 of 8,047 (97.1%), is also not stated. So the time twist and the carved-away void cannot be read by a stranger.
   - Expected: one caption line carrying these three rules plus "found at node 7,812 of 8,047".
3. **Verification chain channels are unkeyed (red rule y = 62, x 148.5–273.57; bit row y ≈ 73).**
   - Measured: tick length encodes literals made true (1.5/2.75/4.0 mm = 41/36/14, exact). Tick side encodes the 14 closing-variable groups (exact). But neither is stated, and the groups do not sit under their variable labels in the bit row above (for example, group x6 starts at x = 149.2 while "6" is at x ≈ 166). To a reader these are decorative data.
   - Expected: key both channels in the "Checking" caption (tick length = how many of the clause's 3 literals the certificate makes true; ticks switch sides at each new closing variable). Or align each group under its variable's label.
   - While editing the captions, also state the convention behind "45,088 clause tests" (every clause closed at each node, no early exit; early exit gives 31,371).

## Follow-up on open mandates
none (r01, no LEDGER.md)
