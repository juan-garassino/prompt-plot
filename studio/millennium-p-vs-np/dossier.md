# millennium-p-vs-np — P vs NP: the needle is one radius; the haystack is everything else
**Field expert:** theoretical computer science (computational complexity) · **Date:** 2026-09-28 · **Status:** dossier v1

Plate 2 of the MILLENNIUM series. Reference poster `ref/reference.png` read as an
interpretation brief (AUTHORING.md): what it gets right is the *pairing* — an overgrown
search on one side, one red thread and a short checked chain on the other. What it gets
wrong is everything the drawing is made of (see §4 lies: its tree merges branches, its blue
waypoints encode nothing, its search is not a search of anything). This dossier replaces the
invented tree with a real one, computed, and every number below was produced by
`data/search.py` / `data/hamilton.py` on 2026-09-28.

No existing piece or studio plate draws a search tree, SAT or a Hamiltonian search
(grep of `promptplot/generative/pieces/` and `studio/`, 2026-09-28).

---

## 1. The phenomenon (≤5 lines)

A decision problem is in **NP** when every YES answer has a short *certificate* that a
machine can check in time polynomial in the input size; it is in **P** when the answer can be
*found* in polynomial time. P ⊆ NP trivially. Clay's statement: "If it is easy to check that a
solution to a problem is correct, is it also easy to solve the problem?" (Cook and Levin,
independently, 1971). SAT was the first problem proved NP-complete (Cook 1971): a
polynomial algorithm for SAT would put all of NP in P. Nobody has one; nobody has proved
none exists.

### Governing math

- **Instance** (3-SAT): Boolean variables x₁…xₙ, a conjunction of m clauses, each an OR of 3
  literals. Here n = 20, m = 91 (m/n = 4.55, SATLIB's phase-transition setting for n = 20).
- **Candidate space**: the n-cube {0,1}ⁿ, |{0,1}²⁰| = 2²⁰ = **1,048,576** assignments.
- **Search** (the one the plate draws): chronological backtracking, variables in index order,
  **False before True**; a partial assignment (b₁…b_d) is a *conflict leaf* the moment a
  clause whose three variables are all assigned evaluates false. Every generated partial
  assignment is a node (root counted). Node at depth d owns a sub-cube of exactly
  **2^(20−d)** assignments.
- **Measure layout (exact)**: node p = (b₁…b_d) owns the angular interval
  [k/2^d, (k+1)/2^d) of one turn, k = the bits read as a binary integer, x₁ most significant,
  True = 1. Conflict leaves at depth d refute 2^(20−d) assignments each; the refuted mass plus
  the model sums to exactly 2²⁰.
- **Search time = angle**: with False-first, DFS preorder visits nodes in increasing start
  angle (ties: shallower first). The search is a clock hand sweeping clockwise.
- **Verification**: given the 20-bit certificate, evaluate all 91 clauses: 91 clause checks,
  3 × 91 = **273 literal lookups**, O(m·3) — linear in the input, not in the search.
- **Scale honesty**: the best known exact algorithm for undirected Hamiltonicity is still
  exponential, O*(1.657ⁿ) Monte Carlo (Björklund, FOCS 2010), versus O*(2ⁿ) Bellman /
  Held–Karp 1962. "Still exponential" is a statement about the best known algorithms, never
  a theorem.

---

## 2. Three candidate visual truths (ranked)

### (a) The needle is a radius — the whole search of one real 3-SAT instance as a clock ★ RANK 1

SATLIB `uf20-03` (chosen by a stated rule, not for looks: *the first file of the uf20-91 set,
in SATLIB order, with exactly one satisfying assignment*; 131 of the 1000 files qualify).
Its complete backtracking tree: **8,047 nodes, 4,023 conflict leaves, 1 model**. Drawn in the
measure layout, the tree is a disc of 2²⁰ assignments being carved away; the first pruning
happens at depth 6 (8 conflicts), the surviving fraction falls 1 → 0.875 (d 6) → 0.157
(d 12) → 0.011 (d 15) → 2⁻²⁰ (d 20). Exactly **one radius reaches the rim, at 348.628°**:
the certificate `1 2 3 4 −5 6 7 8 9 10 11 −12 13 −14 −15 16 17 18 −19 20`. The red path from
the centre is a *binary search homing onto that angle* — node centres at 270°, 315°, 337.5°,
348.75°, 343.125°, … converging to 348.628° — a real zigzag that straightens to a ray.

And the clock: because search time runs clockwise, the plate shows *when* the needle was
found — at node **7,812 of 8,047** (97.1%), i.e. the hand swept 348.6° of the dial first.
Seventy-five complete 20-bit candidates reach the rim and are refuted on the last variable
(the conflicts at depth 20): false needles, indistinguishable from the true one until checked.

**Verification side:** the same 20 bits, pulled out of the disc and laid straight, then
91 clause checks along it (41 clauses satisfied by exactly 1 literal, 36 by 2, 14 by 3):
a short, finite, countable chain against a dial of 8,047 marks.

**Why potent / the twist:** everyone holds *the needle in the haystack*. The mechanism
finishes the proverb precisely: the haystack is a disc, the needle is **one radius**, and
checking a needle takes a glance while finding it took the whole clock. Also a clock face:
the plate literally tells the time of the discovery (≈ 11:37 on a 12-hour dial:
348.63/30 = 11.62 h). **Abstract order: RADIAL + NESTED** (each ring = one more variable
fixed = one more halving of the cube; the carved void = refuted space), with the clock sweep
as the time axis. **Lineage:** Manfred Mohr's hypercube works (1970s–) — the candidate
space here *is* the 20-dimensional hypercube and the tree is its recursive halving into
sub-cubes; "the rule IS the image" is literally true (the text of §1 redraws the plate).
Secondary: Sol LeWitt's *Wall Drawings* — the certificate is an instruction a stranger can
execute exactly (that is what verification is).

### (b) Hamilton's own puzzle — the full search of the Icosian game ★ RANK 2

Hamilton's Icosian game (1856; publishing rights sold to Jaques and Son for £25, per
Wikipedia "Icosian game"): find a cycle through all 20 vertices of the dodecahedron. Clay's
own P-vs-NP page uses the Hamiltonian path as its example. The complete tree of simple paths
from one vertex: **12,538 nodes, 2,958 dead ends, 162 Hamiltonian paths, 60 of which close
into a cycle** (= the 30 undirected Hamiltonian cycles × 2 directions). The count is
labelling-free (tree of all simple paths; graph vertex-transitive). The graph is cubic, so
the root has 3 children and every other node ≤ 2: the same exact measure layout works with
thirds at the root. Visually: **60 red radii** instead of one (a YES-instance with many
certificates — a looser, different truth). Certificate check = 20 vertices distinct +
20 edges present = 40 checks. Order: RADIAL/BRANCHING. Weaker than (a): 60 needles dilute the
proverb, the tree is denser (1,818 nodes at depth 14), and a dodecahedron invites
illustration (drawing the solid is figuration — see §4).

### (c) NO has no certificate — the Petersen graph's complete, red-less search ★ RANK 3

The Petersen graph (10 vertices, 15 edges) has Hamiltonian paths but **no Hamiltonian
cycle**. Its complete search from one vertex: **274 nodes, 48 dead ends, 24 Hamiltonian
paths, 0 closing** — small enough to draw every node at full resolution. There is no red
line anywhere; the only evidence of NO is the entire tree. This is the asymmetry the
reference hides: NP promises a short proof for YES, not for NO (that is coNP; if P = NP then
NP = coNP, the converse is open). Order: BRANCHING with an empty accent layer — the loud
colour's *absence* is the verdict. Best used as a small companion to (a), not alone: on its
own it is off the Clay question's centre.

---

## 3. Real data — verified

**Instance.** SATLIB (Hoos & Stützle), Uniform Random-3-SAT, "phase transition region,
unforced filtered", set **uf20-91**: 20 vars, 91 clauses, 1000 instances, all satisfiable.
`https://www.cs.ubc.ca/~hoos/SATLIB/Benchmarks/SAT/RND3SAT/uf20-91.tar.gz` — HTTP 200,
323,695 bytes, fetched 2026-09-28. Index page `https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html`.
File copied verbatim to `studio/millennium-p-vs-np/data/uf20-03.cnf`,
sha256 `23bbf1dba20738f0b09cd18199d261e0cdf23e904e808264c7d61a16d3234f62`.
(Note: m/n = 4.55 for this set, not the asymptotic 4.26 — do not caption 4.26.)

**Computation.** `.venv/bin/python studio/millennium-p-vs-np/data/search.py` (stdlib,
deterministic; `--json out.json` dumps every node in preorder with bits, depth, k, conflict).
Cross-checked three ways: recursive DFS, level-synchronous numpy enumeration (identical
8,047), and brute force over all 2²⁰ assignments (exactly 1 model, index k = 1,015,453).

| depth d | 0 | 5 | 6 | 8 | 10 | 12 | 13 | 15 | 17 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| generated | 1 | 32 | 64 | 224 | 504 | 1136 | **1284** (widest) | 996 | 346 | 106 | 76 |
| conflicts | 0 | 0 | 8 | 80 | 74 | 494 | 791 | 633 | 208 | 68 | 75 |
| live | 1 | 32 | 56 | 144 | 430 | 642 | 493 | 363 | 138 | 38 | **1** |

Full per-depth lists are printed by the script. Depth-8 summary (for the plotting
aggregation in §6): 224 generated nodes, 80 dead on arrival, 144 live sub-trees, largest
175 nodes; 17 depth-8 sectors reach depth 20; the model's sector is k₈ = 247 (bits
11110111), its sub-tree has 65 nodes. Sum of depth-8 sub-trees 7,808 + 239 nodes above = 8,047.

**Context numbers** (same algorithm, all 1000 uf20-91 files): mean tree 6,792 nodes, median
6,180, min 1,535, max 18,959 — uf20-03 (8,047) is ordinary, not a showpiece.
**A smarter search on the same instance:** DPLL with unit propagation (same variable order,
False first) needs **87 nodes** (first model at node 82, 446 implied literals, 43 conflicts) —
92× fewer. The tree measures one algorithm, not the problem.

**Hamiltonian data (b, c).** `.venv/bin/python studio/millennium-p-vs-np/data/hamilton.py`:
dodecahedron via LCF [10,7,4,−4,−7,10,−4,7,−7,4]², Petersen as 5-cycle + pentagram + spokes.

**Literature.** Clay problem page `https://www.claymath.org/millennium/p-vs-np/` (statement
quoted in §1). Cook, "The complexity of theorem-proving procedures", STOC 1971; Karp,
"Reducibility among combinatorial problems", 1972 (21 problems, incl. directed and
undirected Hamiltonian circuit). Björklund, "Determinant sums for undirected Hamiltonicity",
FOCS 2010, arXiv:1008.0541 (O*(1.657ⁿ)).

---

## 4. Simplifications allowed vs. lies

**Allowed (state each one on the NOTES/HANDOFF):**
- Radius as any monotone function of depth (linear, sqrt, stepped rings); angle must stay the
  exact measure k/2^d — it is the one exact coordinate.
- Summarising sub-trees below the pen's resolution depth by **exact aggregates** of the real
  tree (node count, max depth, conflict count per sector) — a stated aggregation, e.g. "below
  depth 8 each sector is one mark of length = deepest depth reached". Never invented texture.
- Drawing only the search up to the discovery (7,812 nodes, angle 0 → 348.63°) and leaving
  the last 235 nodes (348.63° → 360°) as blank "never needed" paper — say which is drawn.
- Rotating the dial (0° at 12 o'clock, clockwise) and mirroring, uniformly.
- Omitting variable labels; showing the certificate as bits, signs or DIMACS literals.
- Using the Petersen tree (c) as a small NO companion.

**Lies (binding on everyone):**
1. **A tree that merges.** A backtracking search tree never rejoins (the reference's
   lattice of crossing branches). Merging states is a different algorithm (dynamic
   programming) and must not be drawn under this caption.
2. **Invented or decorative branching.** Every branch is one of the 8,047 nodes (or an exact
   aggregate of them). No filler twigs, no "dots trailing off" beyond the real leaves.
3. **A complete 2²⁰ tree** (uniform fan-out to the rim). The real tree prunes from depth 6 on
   and is widest at depth 13; showing it uniform hides what search actually is.
4. **More than one red path / a red path that ends short of the rim / a red path at any
   angle other than 348.628°.** This instance has exactly one model.
5. **Verification drawn as one tick or as 20 ticks.** Checking is 91 clause evaluations
   (273 literal lookups): linear in the formula. (The reference's "polynomial in the size of
   the solution" is wrong: polynomial in the size of the *input*.)
6. **"The tree proves P ≠ NP" / "NP problems need exponential time."** Unproven — that IS
   the open question. DPLL does this instance in 87 nodes. Never caption the tree's size as
   the problem's difficulty; caption it as *this search's* cost.
7. **"NP = not polynomial."** NP = verifiable in polynomial time (nondeterministic
   polynomial); P ⊆ NP. Any type that says otherwise is out.
8. **The maze metaphor.** Maze solving is in P (linear-time BFS); a labyrinth picture
   teaches the opposite of the theorem.
9. **Blue "waypoint" circles** on the certificate path (reference) — they encode nothing.
   Node marks exist only where a node exists and must mean something (e.g. conflict).
10. **Captioning m/n as 4.26** or claiming "the phase transition" for this file without
    saying 4.55 / SATLIB's n = 20 setting.
11. For (b): drawing the dodecahedron solid as the image (illustration, rubric §6) — the
    graph may appear only as the certificate's check, never as the subject.

---

## 5. The misconception to quietly correct

**"Hard means the answer is well hidden, so a big search proves the problem is hard."**
The plate must show the tree as the cost of *one method*, and the certificate as something
anyone can check — without asserting that the tree is unavoidable. The quiet correction lives
in one caption line naming the method ("chronological backtracking, x₁→x₂₀, false first:
8,047 nodes") and, optionally, one small counterweight: the same needle found by unit
propagation in 87 nodes. The viewer should leave with the true question — *is there always
a shortcut?* — not the false answer "no". Secondary: NP ≠ "not polynomial"; P sits inside NP.

---

## 6. Pen-plotter fit

**Naturally a line:** each tree edge (radial step between rings) and each node's sibling
arc (an arc spanning its two children's centres) — a radial dendrogram is pure strokes. The
certificate is one continuous red polyline of 20 segments. Conflict leaves need **no marks**:
a branch that simply stops is the conflict; its end is the only mark it needs.

**Density — the hard constraint (computed):** sibling separation at depth d on a ring of
radius r = R·d/20 is R·d/20·2π/2^d. For R = 130 mm: d 7 → 2.23 mm, d 8 → 1.28 mm,
**d 9 → 0.72 mm (under the 0.8 mm floor)**, d 10 → 0.40 mm. For R = 150 mm, d 9 → 0.83 mm.
So the tree is resolvable to depth 8 (R ≥ 120 mm) or 9 (R ≥ 150 mm, crop at the frame);
below that it must be the §4 exact aggregate. A node-per-mark layout of all 4,024 leaves at
0.8 mm needs a 3.2 m leaf frontier — impossible radially on A3 (area-wise it would fit a
~90 × 90 mm lattice only via an H-tree-type space-filling embedding, which loses the
time = angle truth).

**Pen cycles:** drawing the full tree edge-for-edge needs ≥ **4,023 pen-down strokes**
(odd-degree bound: 4,022 internal non-root nodes + 4,024 leaves = 8,046 odd vertices ÷ 2).
At Leo's settings (G4 P1.0 dwell on each lift and drop) that is ≈ 2.2 h of dwells alone
before any drawing — it does not earn its cycles. Aggregating at depth 8 caps the black
tree at ≈ 144–224 sector strokes + ≤ 239 upper-tree strokes (upper tree can be chained as
long DFS polylines). **Thousands of tiny node circles are out**; if node dots are wanted,
only the 75 depth-20 false needles and the one true needle have earned one.

**Layers (suggested):** (1) black fine — tree + aggregates, spatially ordered clockwise =
DFS order, which is also batch order (no sheet-crossing travel; batch boundaries at sector
edges); (2) black or grey — type/furniture; (3) red — certificate radius + the verification
chain, last, on top. One swap per pen. Draw time estimate at F600 (10 mm/s): state per layer
in HANDOFF.

**Must stay blank paper:** the refuted mass. At the rim 99.9999% of the disc is empty
(1 of 2²⁰ survives); the void carved from depth 6 outward IS the image. Also the arc
348.63° → 360° if only the pre-discovery search is drawn. No hatch, no tone in the void.

---

## 7. Check numbers

All from `.venv/bin/python studio/millennium-p-vs-np/data/search.py` unless noted.

| # | value | reproduce / measure on render |
|---|---|---|
| 1 | candidate space **2²⁰ = 1,048,576**; refuted mass 1,048,575 + 1 model | `python -c "print(2**20)"`; script line "refuted assignment mass" |
| 2 | tree **8,047 nodes, 4,023 conflict leaves, 1 model** | script; count branch ends on the gcode if drawn in full |
| 3 | certificate angle **348.628°** (k = 1,015,453 / 2²⁰) | `python -c "print(1015453/2**20*360)"`; measure the red ray's rim angle (±0.5°) |
| 4 | red path node-centre angles d1–d5: **270, 315, 337.5, 348.75, 343.125°** | script "red path centre angles"; the red path must zigzag, not be straight from d1 |
| 5 | discovery at preorder **7,812 / 8,047 = 0.9708** of the search | script "found at preorder node" |
| 6 | first pruning at **depth 6 (8 conflicts)**; no branch ends at depth ≤ 5 | script "conflicts/depth" — rings 1–5 must be complete |
| 7 | widest level **depth 13: 1,284 generated / 493 live**; live fraction at d 12 = **0.157** (642/4096) | script "live/depth" |
| 8 | **75** complete candidates refuted at depth 20 (false needles) | script "conflicts/depth"[20] |
| 9 | verification = **91 clause checks, 273 literal lookups**; true-literal histogram **41 / 36 / 14** | script "verify" lines; count red checks on the render (must be 91) |
| 10 | DPLL (unit propagation) on the same instance: **87 nodes**; all 1000 uf20-91 files by backtracking: mean **6,792** nodes | script last line "DPLL" (87); the 6,792 mean needs the full uf20-91 tarball (§3 URL) run through the same backtracking — cite only if captioned |
| 11 | (b) dodecahedron: **12,538 / 2,958 / 162 / 60**; (c) Petersen: **274 / 48 / 24 / 0** | `.venv/bin/python studio/millennium-p-vs-np/data/hamilton.py` |
| 12 | resolution: sibling gap at d 8, R 130 mm = **1.28 mm**; d 9 = **0.72 mm** (fails 0.8) | `python -c "import math;print(130*8/20*2*math.pi/256)"` |
