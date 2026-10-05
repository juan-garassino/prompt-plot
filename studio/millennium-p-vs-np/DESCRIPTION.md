# P VS NP — description

| | |
|---|---|
| gallery | `gallery/studio/millennium_p_vs_np` |
| current render | `gallery/studio/millennium_p_vs_np/current/pp_millennium_p_vs_np_faithful_v6.png` (+ `_truewidth.png`, `.gcode`) |
| source | `studio/millennium-p-vs-np/rounds/r01/piece.py::p_vs_np_faithful` (seed 7, no randomness) · data `data/uf20-03.cnf`, `rounds/r01/tree.json` |
| paper · pens | A3 portrait (297 × 420 mm), cream, margin 15 · 0 black 0.1 = search below row 7 (grey in the preview) · 1 black 0.3 = search rows 0–7 + Petersen tree · 2 black 0.3 (same pen, own layer) = all type · 3 red 0.5 = the certificate path + the 91-tick checking rule · ≈ 100 min, 2 swaps |
| status | r01, the faithful flavour of plate 2 / 7 (MILLENNIUM series) · critics FAIL (art 5.71/4, sci 7/9/7), ranked 2 · kept on disk; the ledger's best is r02 (radial dial) |

## In one line
The complete backtracking search of a real 20-variable SAT puzzle, drawn as **one huge pruned tree with a single red thread to the only solution** — set against a short red comb of 91 ticks, the whole cost of checking that solution once it is found.

## Lede
The full search of a real 20-variable puzzle as **one pruned tree with a single red thread** to its only solution, beside a short comb that checks it.

## On the sheet
A great black tree fills the centre, forking in eight clean rows and then hanging as a fine curtain of hairlines, longer toward the right. One red line threads down the right side to the word SOLUTION. Bottom left, a small dense black tree; bottom right, a red rule bristling with ticks. Black captions fill the top left.

## The science
The tree is the complete search of a real SAT instance: 8,047 nodes, 4,023 dead ends, one solution, each node placed by its share of the million candidates. The red path is the answer; the red ticks check it clause by clause. Drawn exactly. That the tree measures this algorithm, not the problem, and what NP leaves open are stated in text.

## What is on the sheet
- **Title block, top-left.** `P VS NP` in heavy spaced capitals (u ≈ 0.05–0.28, v ≈ 0.04–0.07); below, Clay's question (v ≈ 0.10–0.11): `IF IT IS EASY TO CHECK THAT A SOLUTION IS CORRECT, / IS IT ALSO EASY TO FIND ONE?`; then, smaller (v ≈ 0.13–0.14): `SATLIB UF20-03: 20 VARIABLES, 91 CLAUSES OF 3. / 2²⁰ = 1,048,576 CANDIDATES. ONE SATISFIES ALL 91.`
- **Right column** (u ≈ 0.61, v ≈ 0.04–0.11): `MILLENNIUM PRIZE PROBLEMS 2 / 7`, `CLAY MATHEMATICS INSTITUTE, 2000`, then `P: ANSWERS FOUND IN POLYNOMIAL TIME. / NP: ANSWERS CHECKED IN POLYNOMIAL / TIME, GIVEN A CERTIFICATE. / P IS INSIDE NP. EQUAL? OPEN.`
- **The tree (dominant mass).** `START` at (0.50, 0.15) over the root stem. Eight rows of orthogonal black 0.3 forks, each halving the width, complete through row 5 and first pruned at row 6, reach v ≈ 0.37. Below, 111 thin hairlines (grey in the preview) hang to different depths: short on the left (most stop by v ≈ 0.55–0.67), long on the right (to v ≈ 0.76). Gaps in the curtain (e.g. u ≈ 0.54–0.60) are branches ended at row 6.
- **The red thread.** One crimson polyline leaves the root, steps right row by row (u ≈ 0.72, 0.84, 0.89, 0.92), zigzags slightly, then drops at u ≈ 0.92 to v ≈ 0.76, over `SOLUTION` at (0.92, 0.78).
- **Lower-left panel** (u ≈ 0.05–0.31, v ≈ 0.80–0.90): a small dense black tree, 72 leaves like a barcode, no red. Caption (v ≈ 0.92–0.94): `NO HAS NO CERTIFICATE. PETERSEN GRAPH: DOES A HAMILTONIAN CYCLE EXIST? THE SEARCH FROM ONE VERTEX, ALL 274 NODES: NOTHING RED. LEAF ORDER, NOT TO MEASURE.`
- **Lower-right checking strip** (u ≈ 0.50–0.92): the bit row `1 2 3 4 -5 6 7 8 9 10 11 -12 13 -14 -15 16 17 18 -19 20` (v ≈ 0.83); a red rule (v ≈ 0.85) bristling with 91 red ticks of three lengths; `CHECKING: 91 CLAUSES, 273 LOOKUPS — THE TESTS ALONG THE RED ALONE.` and a four-line `FINDING:` caption (v ≈ 0.92–0.94) ending `THIS SEARCH, NOT THE PROBLEM: UNIT PROPAGATION NEEDS 87 NODES.`

## The science it encodes
P is the class of problems whose answers can be *found* in polynomial time; NP, those whose YES answers can be *checked* in polynomial time given a certificate. The sheet makes the asymmetry physical with one real instance, SATLIB uf20-03 (20 variables, 91 three-literal clauses, exactly one satisfying assignment). The tree is its complete chronological backtracking search (False first): 8,047 nodes, 4,023 dead ends, one model. Each node's horizontal position is its exact share of the 1,048,576 candidates, so left-to-right is also search order; the solution is found at node 7,812 of 8,047 — far right. Rows 0–7 are drawn node for node; below row 7 each hairline stands for a whole sub-tree, as deep as its deepest node, so a line that stops is a partial assignment already refuted by a clause. The red path is the certificate `11110111111010011101`. The red strip verifies it: one tick per clause, tick length = how many of the clause's three literals the certificate makes true (41 / 36 / 14), sides switching at each new closing variable. The Petersen panel shows the NO side: all 274 nodes of a Hamiltonian-cycle search, no cycle, nothing red. Stated in text only: NP guarantees certificates for YES answers; whether every NO has a short proof is the open NP vs coNP question (the Petersen graph itself has a short parity proof). And the tree is the cost of *this* algorithm, not of the problem — DPLL with unit propagation needs only 87 nodes.

## How it got here
Round r01, the "faithful" reading of an AI-generated reference poster: its START → SOLUTION architecture kept, its merging invented tree replaced by the real search, its blue waypoints and "typically exponential" claim cut. Six self-revisions (v1–v6) regrouped the bottom captions, tightened and weighted the title, put the definitions column on a crown stem, authored a single-stroke `I` to save pen cycles, and rewrapped the Petersen caption. Both critics failed it (the upper crown reads as a textbook dendrogram; the "NO HAS NO CERTIFICATE" wording overstates), so the series moved on to the radial-dial rounds r02–r03, keeping only this plate's P / NP definitions text; v6 stays on disk as the faithful flavour.
