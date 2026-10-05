# millennium-p-vs-np — encoding (VISUAL TRANSLATOR)   · Status: encoding v1 · 2026-09-28

Source of truth: `studio/millennium-p-vs-np/dossier.md` v1, visual truth **(a) THE NEEDLE IS A
RADIUS** (rank 1). Truth (c), the Petersen NO search, appears only as the faithful thesis's bottom
companion. Truth (b), the Icosian game, is **not drawn**. Data: `data/uf20-03.cnf`,
`data/search.py --json` (8,047 nodes in preorder), and `data/hamilton.py` (Petersen). The
reference `ref/reference.png` is an AI poster. It is an interpretation brief, never a bitmap
(`studio/AUTHORING.md`). No BRIEF.md, FEEDBACK.md or LEDGER.md exists yet. This is plate 2 of the
MILLENNIUM series. Theses built in parallel: **faithful [F]** and **abstract [A]**. Everything
binds both unless a line says `[F]` or `[A]`.

Translator's measurements (2026-09-28, scratch only, from the `--json` dump; every one is
reproducible from it):
- **Clause tests.** A clause is tested once at each generated node whose depth equals the clause's
  largest variable, with no short-circuit. Under that rule the backtracking search makes **43,658
  clause tests up to and including the model** (node 7,812) and **45,088 over the whole tree**.
- **Closing variables.** Clauses grouped by the variable that closes them are
  `[0,0,0,0,0,1,0,3,1,2,3,4,5,4,8,13,7,12,10,18]` for x1…x20. No clause closes before x6, which is
  *why* rings 1–5 are complete.
- **Checking is the red path.** Any root-to-leaf path tests each clause exactly once, so the red
  path alone makes the 91 tests. Checking the certificate IS the red; the search's extra cost IS
  the black.
- **Search stopped at the model ([A]).** 7,812 nodes and 3,903 conflict leaves. There are 7
  conflicts at depth 6, at 194.1°, 216.6°, 239.1°, 261.6°, 284.1°, 306.6° and 329.1° (every
  22.5°). The eighth (351.6°) comes after the needle. 69 false needles (depth-20 conflicts) come
  before the model, 3 of them in the model's own depth-8 sector.
- **Depth-8 sector aggregates ([A]).** 220 sectors are generated and 140 of them live past ring 8.
  The number of lines crossing ring d is:

  | d | 9–12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
  |---|---|---|---|---|---|---|---|---|---|
  | lines | 140 | 125 | 99 | 95 | 72 | 42 | 29 | 19 | **14** (13 black + the red) |

- **Black rim contacts ([A]).** At 169.5, 227.1, 235.5, 249.6, 258.0, 280.5, 303.0, 317.1, 325.5,
  332.6, 334.0, 336.8 and 339.6°. Only **one** lies in the right half (x₁ = FALSE). [F] adds 355.1°,
  356.5° and 359.3°.
- **Right-half extent.** The furthest reach in the right half is 0.842 R, horizontally.

---

## 1. STYLE assignment

**A stated hybrid: the RADIAL DATA-VIZ canon (5), set on the series' SWISS sheet (canon 3): cream
stock, black plus one red, flush-left spaced caps, radical negative space.** Canon 5's muted
multi-hue palette is overridden by the series palette.

**Why the order fits.** Canon 5's own rule is *angle encodes time, radius encodes track*. Here that
rule is the mechanism, word for word:
- With False-first, depth-first preorder runs in increasing angle, so **search time is angle**.
- Radius is **depth**, one ring per variable.
- Each node's arc is **exactly its share of the 2²⁰ candidates**.

Canon 5 asks for concentric, evenly pitched rings (20 variables), a radial tick scale (the hour
ticks, §4) and legibility of the data over decoration. The plate gives exactly that.
- `[A]` draws the dial.
- `[F]` draws the same measure **unrolled**: angle becomes x, the ring becomes a row. This keeps the
  reference's START-at-top, SOLUTION-at-bottom architecture without giving up the exact
  coordinate.

**Flatness is declared.** The measure coordinate is exact only in a flat, undistorted plane. Any
perspective or tilt would make equal shares of the haystack look unequal (that would be lie 3's
cousin). Depth is carried by weight instead: the node-for-node tree is 0.3, the summarised fringe
is 0.1 (§6).

**LINEAGE:** `lineage: Manfred Mohr, Cubic Limit (1973–75) and the n-dimensional hypercube works
that followed it (from 1977) (curator: verify the catalogue number of the specific sheet cited).
Order taken: a hypercube read by a rule, every mark a selected edge — the rule IS the image. Here
the cube is the 20-cube of assignments and the rule is "halve it at every ring; draw only what is
not yet refuted".`
- The text of dossier §1 would redraw the plate.
- Batch check: Riemann answers LeWitt, Navier–Stokes answers Riley, Yang–Mills answers
  Kandinsky, and Hodge answers Gabo. Mohr is free, and the Riemann encoding already reserved it
  for this plate.

## 2. The one-glance statement

> **The haystack is a disc, almost all of it eaten away; the needle is the one red radius that
> reaches the rim — and checking it is a short straight line you can count.**

**`[A]`**
- **At 3 m:** a dark wheel low on the sheet. Its hub is dense and its corona ragged, long on the
  left and short on the right. One red line leaves the hub, hooks out to 9 o'clock, climbs
  clockwise, crosses the rim at about 11:37 and keeps going straight up the sheet, out of the
  disc, nearly to the top edge.
- **At 1 m:** a thin blank sliver sits between the red hand and 12 o'clock (the search never went
  there). A dozen black rays touch the rim and stop (false needles). The outer half of the right
  side is empty. The part of the red outside the disc carries a comb of small ticks.
- **At 30 cm:**
  - There are exactly 91 ticks in three lengths.
  - The certificate is printed in DIMACS.
  - The two counts sit side by side: 43,658 clause tests to find, 91 to check.

**`[F]`**
- **At 3 m:** a wide curtain of black verticals hangs from a bracketed crown. It is short on the
  left and long on the right. One red thread descends from START at top centre, steps right, and
  drops almost at the **right edge**, not the centre, to SOLUTION.
- **At 1 m:** a short red comb is laid horizontally beneath it. On the lower left, a small
  all-black tree has no red anywhere.

## 3. The abstract ORDER

**RADIAL + NESTED.** Each ring is one more variable fixed, so each ring halves every live share
again. The carved void is refuted space. The clockwise sweep is time.

Exact mapping in one line each:
- "**A node is its exact share of the 2²⁰ candidates; a branch that stops is a refutation; red is
  the one share that survives to the rim.**"
- "**Angle is time: the search swept clockwise from 12, and the red hand shows when it found the
  needle.**"
- "**Checking is the red alone: 91 tests along it; finding was the red plus all the black.**"

`[F]` has the same order unrolled: x is the share (and the time), the row is the variable. This
names no plot and no object. A clock face appears only because the mapping *is* a sweep. It is the
twist, not an illustration (§8).

## 4. Channel mapping (Tufte: nothing drawn that encodes nothing)

Units: `[A]` R = 128 mm and ring pitch p = R/20 = **6.4 mm**. `[F]` W = 267 mm and row pitch
h = **12.5 mm**. Node p = (b₁…b_d) has measure centre m = (k + ½)/2^d (dossier §1).

| ink on paper | encodes | exact rule / range |
|---|---|---|
| angle θ `[A]` / x `[F]` | the node's share of {0,1}²⁰ **and** DFS time | `[A]` θ = 360°·m, 0° at 12 o'clock, clockwise, no rotation and no mirror. `[F]` x = 15 + 267·m. **Linear and uniform. Never stretched.** |
| radius `[A]` / row `[F]` | depth d = number of variables fixed | `[A]` r_d = d·p. `[F]` y_d = 350 − d·h (root y 350, row 20 at y 100). |
| **edge geometry** (both pens) | parent → child | Stem, fork, branch. The parent's stub runs radially (vertically in `[F]`) half a pitch past its own ring. The **fork** is an arc at r_{d}+p/2 (a bar at y_d − h/2 in `[F]`) from the parent's θ to the child's θ. Then the child's spoke (drop) runs to its ring. Draw only edges to children that were **generated**. A node with one generated child gets no fork. Never draw chords or diagonals: the red must lie ON this geometry. |
| **black 0.3** (pen A) | the exact search, node for node | `[A]` depths 0–8 (sibling spokes ≥ 1.178 mm apart at r = 7.5p). `[F]` depths 0–7 (≥ 2.086 mm). |
| **hairline 0.1** (pen B) | the exact **aggregate** of each sub-tree below the pen's resolution | One line per sector: `[A]` depth-8 sectors, 140 lines; `[F]` depth-7 sectors, 112 lines. Each line sits at the sector's centre θ (or x) and runs from its ring out to the ring of **the deepest node in that sub-tree**. There is no fork and no texture below that. The aggregation boundary is visible as the weight change and is stated in a caption. |
| a line that simply stops | a conflict leaf, or a sub-tree whose deepest node is refuted | **No mark at the end.** No dot, circle or tick. |
| blank paper inside the disc/field | refuted assignments (2²⁰ − 1 of them) | Nothing is drawn there, ever. |
| **hairline rim circle** `[A]` (pen B) | ring 20, the set of complete assignments (the haystack's surface) | One circle r = 128, split into 4 quadrant arcs for batching. A line that touches it has reached a complete candidate. |
| **12 hour ticks** `[A]` (pen B) | the time scale: each is 1/12 of the sweep = 87,381⅓ candidates | Radial hairlines r ∈ [129.5, 133.5] at 0°, 30°, … 330°. No numerals. |
| **red 0.5** (pen R), inside | the certificate's own search path | Node centres at d = 1…5 are 270°, 315°, 337.5°, 348.75°, 343.125°, converging to 348.628°. The red **substitutes** for the black edges and the aggregate of sector 247 (depth 8) `[A]` / sector 123 (depth 7) `[F]`. It is never drawn over them. |
| **red 0.5**, outside `[A]` | the needle pulled out: the verification | The straight radial continuation from the rim (r = 128) to r = 257, one stroke with the path. The 91 ticks sit on r ∈ [134, 256.9]. |
| **red chain** `[F]` | the verification | A horizontal red rule, y = 62, x ∈ [150.7, 273.57]. Its right end is on the red thread's axis. |
| **91 red ticks** (both) | one clause check each | Pitch **1.35 mm** (122.9 mm total), perpendicular to the rule. Ordered by closing variable (x6, x8, x9, … x20), and in file order within a group. **Tick length = number of literals the certificate makes true**: 1 → 1.5 mm, 2 → 2.75 mm, 3 → 4.0 mm (41 / 36 / 14). **Side alternates by group** (14 groups), so the closing variable is visible without gap cost. No tick is missing, because every clause is satisfied. |
| blank wedge 348.628° → 360° `[A]` | the search never needed after the answer | `[A]` draws only the search up to the model (preorder ≤ 7,812). The wedge is naturally empty of black. Only the red passes through it, at ring 4 (0.05 mm). |
| right-of-red strip `[F]` x ∈ [273.6, 282] | the 235 nodes after the needle, which prove it is the only one | `[F]` draws the **whole** tree (8,047). |
| **NO companion** `[F]` (pen A) | Petersen graph, Hamiltonian cycle: complete search, **no certificate** | 274 nodes in a leaf-order tidy layout. It makes **no measure claim**, and the caption says so. 72 leaves at 1.1 mm (79 mm wide), 9 levels at 5 mm. **Zero red.** |
| **not encoded (declared)** | sub-tree node counts, the 75 false needles individually, Hamiltonian truth (b), DPLL's tree | The false needles are visible only as the rim contacts of their sectors. DPLL appears only as a number in the caption. |

## 5. Composition sketch — A3 portrait 297 × 420 mm, margins 15, y measured UP from the bottom edge

**No type ever sits inside the disc or the tree field, and none in the refuted void.** So no halo is
needed anywhere.

### 5A — ABSTRACT (the dial and the needle pulled out)

- **Hub at (148.5, 148.5), R = 128.** The hour-tick ends touch the margins at 3, 6 and 9 o'clock
  (x 15.0 / 282.0, y 15.0).
  - The hub sits on the sheet's vertical axis **by necessity, and this is declared**. A dial with
    ticks that fills the width can only sit there: at R ≥ 120, 8 exact levels need the width, and
    the right fringe reaches 0.842 R.
  - The tension comes from the data and the red. All the deep ink is on the left, the right half
    is carved out past ring ~13, and the red leans 11.4° left and rises 124 mm out of the disc.
    The centred frame holding lopsided content is the control, as in Riemann [F].
- **The red, one stroke.** It runs from the hub along the path to the rim tip (123.26, 273.99), then
  straight on to **(97.8, 400.5)**. Ticks run from r = 134 (past the tick ring) to 256.9. At y = 380
  the red is at x = 101.9.
- **Title band, left column x ∈ [15, 88]** (≥ 10 mm clear of the red):
  - `P  VS  NP`: spaced caps 10 mm, baseline 390. It must end at x ≤ 88. If it cannot, drop to 8 mm.
  - Statement: 2.5 mm caps, 2–3 lines from baseline 372:
    `IF AN ANSWER IS EASY TO CHECK, IS IT EASY TO FIND?`
  - Instance line: 1.8 mm caps at y ≈ 300–330, flush-left:
    `SATLIB UF20-03 · 20 VARIABLES · 91 CLAUSES (M/N = 4.55) · 1,048,576 CANDIDATES · ONE FITS ALL 91.`
    (Use `2^20` only if the superscript ⁰ is authored.)
- **Chain caption**, flush-left at x = 110, baseline 398, 2 mm caps:
  `CHECKING: THE NEEDLE PULLED OUT — 91 CLAUSES, 273 LOOKUPS.`
  Then the certificate on the next line down:
  `1 2 3 4 −5 6 7 8 9 10 11 −12 13 −14 −15 16 17 18 −19 20`.
- **Bottom-left spandrel** [15, 62] × [15, 36], 1.8 mm caps, ≥ 8 mm outside the tick ring:
  `FINDING: BACKTRACKING X1..X20, FALSE FIRST. 7,812 NODES, 43,658 CLAUSE TESTS. FOUND AT 11:37.`
- **Bottom-right spandrel** [235, 282] × [15, 36], flush-right:
  `THIS SEARCH, NOT THE PROBLEM: UNIT PROPAGATION FINDS THE SAME NEEDLE IN 87 NODES. A SHORTCUT FOR EVERY CASE? OPEN.`
- **Dominant mass:** the dial, ≈ 51,500 mm², > 95 % of the ink. The hub (r ≤ 51.2, node for node)
  is its dark core.
- **Quiet zone:** the upper right, x ∈ [115, 282] × y ∈ [285, 390] (≈ 17,500 mm²), with nothing in
  it. It is echoed by the carved right half of the dial.
- **The one diagonal:** the red needle.

### 5F — FAITHFUL (the reference's START→SOLUTION architecture, measured and corrected)

- **Tree field** x ∈ [15, 282], rows y_d = 350 − 12.5·d, with the root at **(148.5, 350)**.
  - `START`: 1.8 mm caps centred over the root, baseline 355.
  - The crown: forks at rows 0–7 in 0.3.
  - The curtain: 112 hairlines from row 7 (y 262.5) down to each sector's deepest row. 15 reach
    row 20 (y 100), one of them red.
- **The red thread** runs from the root, steps right (x 215.3 at row 1, 248.6 at row 2, 265.3 at
  row 3, 273.7 at row 4, 269.5 at row 5, …) and converges to **x = 273.57, 96.84 % of the width**.
  The reference centred its thread; the data puts it at the right edge. The search found the
  needle almost last.
  - `SOLUTION`: 1.8 mm caps flush-right at x = 282, baseline 92.
  - The strip to the red's right (the 235 post-discovery nodes) is drawn. It proves uniqueness.
- **Carved void, left:** below row ~17, x ∈ [15, 125], y ∈ [100, 140]. All x₁ = FALSE sectors die by
  row 17, except the one at x ≈ 140 that reaches row 20. The void stays blank.
- **Top band:**
  - Title: flush-left x = 15, baseline 392, 10 mm spaced caps `P  VS  NP`.
  - Statement: 2.5 mm caps at baseline 377. This is Clay's sentence, set as: `IF IT IS EASY TO CHECK
    THAT A SOLUTION IS CORRECT, IS IT ALSO EASY TO FIND ONE?`
  - Right column: definitions flush-left at x = 190, 2 mm caps, 3 lines, baselines 398 / 391 / 384:
    `P: ANSWERS FOUND IN POLYNOMIAL TIME.` /
    `NP: ANSWERS CHECKED IN POLYNOMIAL TIME, GIVEN A CERTIFICATE.` /
    `P IS INSIDE NP. EQUAL? OPEN.`
    The reference's quote block is folded into the statement.
- **Bottom band** y ∈ [15, 88], on two columns:
  - **Left (x 15–94): the NO companion.**
    - The Petersen tree, root y = 85, bottom y = 40.
    - Caption at y 28–35, 1.8 mm caps:
      `NO HAS NO CERTIFICATE: PETERSEN GRAPH, HAMILTONIAN CYCLE? ALL 274 NODES, NOTHING RED. (LEAF ORDER, NOT TO MEASURE.)`
    - This replaces both the reference's "Hamiltonian path (example)" inset and its FINDING toy
      tree.
  - **Right (x 150.7–273.57): CHECKING.**
    - The certificate in DIMACS, 2 mm caps, baseline 72.
    - The red chain at y 62 (ticks within 58–66).
    - Caption, baseline 50: `CHECKING: 91 CLAUSES, 273 LOOKUPS — THE TESTS ALONG THE RED ALONE.`
  - **Full-width method line**, flush-left, baseline 20, 1.8 mm caps:
    `SATLIB UF20-03 · 20 VARIABLES · 91 CLAUSES · BACKTRACKING X1..X20, FALSE FIRST: 8,047 NODES, 45,088 CLAUSE TESTS · BELOW ROW 7 EACH LINE IS ONE SUB-TREE, AS DEEP AS ITS DEEPEST NODE · UNIT PROPAGATION: 87 NODES.`
- **Dominant mass:** the tree field, ≈ 66,700 mm², ≥ 15 : 1 over the bottom band.
- **Quiet zone:** the carved lower-left void, plus the band gap y ∈ [88, 100] left of the red.
- **Reference → faithful mapping:**

  | reference shows | faithful draws |
  |---|---|
  | START/SOLUTION red circles, blue waypoint rings | labels only. No circle anywhere (lie 9). |
  | a lattice of branches that cross and merge | a tree that never rejoins: bars and drops on the exact measure (lie 1) |
  | red thread wandering down the centre | red thread at its true x = 96.84 % of the width |
  | uniform bushy growth to the bottom | complete to row 5, pruned from row 6, widest at row 13, one survivor at row 20 (lie 3) |
  | "dots trailing off" at branch tips | lines that simply stop. No tips are invented (lie 2). |
  | Hamiltonian-path inset + FINDING toy tree "typically exponential" | the Petersen NO search, drawn complete, zero red. The claim is cut (lie 6). |
  | CHECKING: 5 nodes, "polynomial in the size of the solution" | 91 red ticks, "polynomial in the input" as the caption's substance (lie 5) |
  | framed boxes | no frames. The columns sit on the grid. |
  | "SAME PROBLEM. DIFFERENT WORLDS?" | cut. The method line takes the bottom. |

## 6. Pen budget — 2 inks, 3 physical pens, 4 layers (layer discipline, no cap)

| order | layer | physical pen | meaning |
|---|---|---|---|
| 1 | B · HAIRLINE | black 0.1 fineliner | the summarised search (one line per sub-tree); `[A]` also the rim and the hour scale |
| 2 | A · BLACK | black 0.3 | the search drawn node for node; `[F]` also the Petersen NO tree |
| 3 | TEXT | the same black 0.3, own layer, **no swap** | title, statement, captions, certificate |
| 4 | RED | red 0.5 | the one certificate: its search path and its check. Nothing else. |

- The order is light to dark, with red last, so nothing inks over the accent.
- This makes **2 pen swaps**.
- Red is < 3 % of the ink.
- Weight carries a truth: 0.3 means exact, 0.1 means aggregate.

## 7. Expressive levers (one decision each)

- **Proportion.**
  - `[A]`: disc diameter to red protrusion ≈ 2 : 1 by length. By ink it is ≈ 10 m black against
    0.5 m red, about 20 : 1. The red wins by colour, not by mass.
  - `[F]`: tree to bottom band ≥ 15 : 1.
- **Fill vs void.** Three silences, each a truth:
  - The refuted mass inside the rim (the carving).
  - `[A]` the 11.4° wedge after the needle.
  - The upper-right quiet (`[A]`) or the carved lower-left (`[F]`).
- **Density gradient.** Only the data's own: 140 lines at ring 12, 72 at ring 16, 14 at the rim.
  No cosmetic ramp.
- **Colour play.** One red, scarce. It is the only element that crosses the rim/field boundary.
- **Texture direction.** Two directions only: radial (commitment) and tangential (fork). In `[F]`
  these become vertical and horizontal, which is Mohr's orthogonal vocabulary. Nothing is angled
  for effect except the red's true 348.6°.

## 8. The twist

**What the viewer holds:** "a needle in a haystack". Also "it's hidden, so finding it must be
hard", and the clock face.

**What the mechanism breaks:**
- The haystack is a disc of all 2²⁰ candidates.
- The needle is **one radius**.
- The search is a clock hand that swept 348.6° of the dial, 11:37 of 12 hours, before it hit the
  needle.
- Pulled out, the needle is a short straight line with 91 notches. Checking it takes the red alone;
  finding it took the red plus everything black.

The quiet correction: the bottom-right spandrel says this cost belongs to *this search* (DPLL: 87
nodes). The viewer leaves with the real question (is there always a shortcut?), not the false
answer.

`[F]`'s twist is smaller and exact. The reference's centred thread moves to 96.84 % of the width,
and the reference's "Hamiltonian example" becomes a search with **no red at all**: NO leaves nothing
to check.

## 9. Forbidden list (binding on both; the science critic fails any of these)

1. **Branches that merge, cross or rejoin**, or any lattice. It is a tree (lie 1).
2. **Any node mark.** No circles, dots, rings, waypoint discs, START/SOLUTION circles, or marks on
   conflict ends or on rim contacts. A line that stops is the mark (lie 9).
3. **Invented branching.** No filler twigs, no forks below the aggregation depth, no dots trailing
   off, no uniform or complete fan to the rim (lies 2, 3).
4. **More than one red line**, red at any angle but 348.628° (± 0.5°), red ending short of the rim,
   or red anywhere else: no red START, no red title, no red on the Petersen tree (lie 4).
5. **Verification as one tick, 20 ticks, 5 nodes, or any count ≠ 91.** No arrowhead on the chain.
   No "polynomial in the size of the solution" (lie 5).
6. **Arrows, frames and boxes around panels, axes, gridlines, or a legend box.**
7. **Hatch, stipple, tone or type** anywhere in the refuted void or inside the rim/field.
8. **Captions** that say or imply "exponential is necessary", "this proves P ≠ NP", "NP = not
   polynomial" or "m/n = 4.26" (lies 6, 7, 10). Also any "typically exponential" without naming
   the method.
9. **Figuration:** mazes, a haystack or needle pictogram, a drawn dodecahedron or graph, clock
   numerals, a second clock hand, a clock bezel beyond the single rim circle and 12 ticks (lies 8,
   11).
10. **Measure distortion:** non-uniform angle or x, dial rotation (0° stays at 12, clockwise),
    mirroring, perspective.
11. **Chord or diagonal edges.** Edges are stem, fork and branch (arc/spoke or bar/drop), so the red
    lies on the tree.
12. `[A]`: any black in the wedge 348.628° → 360°. `[F]`: omitting the post-discovery strip.
13. Giant decorative type: no giant "?", no giant "NP". Nothing is larger than the title.

## 10. Fabrication

- **Data.**
  - `.venv/bin/python studio/millennium-p-vs-np/data/search.py --json <round>/tree.json`. Write it
    into the round, never into `data/`.
  - `[A]` uses preorder[:7812] and `[F]` uses all 8,047.
  - The Petersen tree needs a dump. Write a **new** script, `data/petersen_tree.py`, reusing
    `hamilton.py`'s graph. Do not edit the dossier's scripts.
  - Red geometry is recomputed from the model bits `11110111111010011101`, not read off the
    aggregate.
- **Spacing floors** (all centre-to-centre, measured):

  | element | `[A]` | `[F]` |
  |---|---|---|
  | exact spokes/drops at their tightest | 1.178 mm | 2.086 mm |
  | aggregate hairlines where they start (r = 51.2 / row 7) | ≥ 1.257 mm | ≥ 2.086 mm |
  | fork-arc radial clearance | p/2 = 3.2 mm | — |
  | red to nearest black past ring 8 (sector 246) | ≥ 1.77 mm | — |
  | red to sector 122 | — | ≥ 2.6 mm |
  | chain ticks (red 0.5) | 1.35 mm | 1.35 mm |
  | Petersen leaves (0.3) | — | 1.1 mm |

  Everything is ≥ 0.8 mm. No floods by construction: no fills and no tone.
- **Draw length and time on A3** (Leo F600 ≈ 10 mm/s, ≈ 2.5 s per pen cycle):

  | layer | `[A]` | `[F]` |
  |---|---|---|
  | B hairline | 6.75 m aggregates + 0.80 m rim + 0.05 m ticks, ~157 strokes → **≈ 19 min** | 11.44 m, 112 strokes → **≈ 24 min** |
  | A black | 2.77 m, ~227 DFS polylines → **≈ 14 min** | 3.24 m, ~120 polylines + Petersen ≈ 0.8 m, ~72 → **≈ 15 min** |
  | TEXT | ≈ 450 glyph strokes → **≈ 14 min** | ≈ 650 glyph strokes → **≈ 19 min** |
  | RED | 1 path+needle stroke ≈ 0.28 m + 91 ticks ≈ 0.23 m → **≈ 5 min** | thread ≈ 0.38 m + rule 0.12 m + ticks 0.23 m, 93 strokes → **≈ 5 min** |
  | **total** | **≈ 52 min, 2 swaps** | **≈ 63 min, 2 swaps** |

- **Pen cycles are earned.** There are no dotted runs and no node circles. The 91 red ticks are the
  only short strokes, and each is one clause.
- **Batching.**
  - `[A]`: all layers stream **clockwise from 12**, which is DFS order, so there is no
    sheet-crossing travel. Batch boundaries fall on depth-4 sector edges (16 batches of ≤ 22.5°).
    The rim goes in 4 quadrant arcs. The red goes last: the path outward, then the ticks
    bottom-to-top.
  - `[F]`: left to right, with batches at depth-4 column edges. The Petersen tree goes in its own
    batch at the end of layer A.
  - Re-zero check every ~15 strokes.
- **Other papers.** A3 is the design sheet.
  - **A4** means re-running at ×0.707 with `[A]` exact to depth 7 (0.3) and the red chain at
    pitch 1.1 with a 0.3 red nib. Check the chain's top clears 286.
  - **A5 (Leo) is not a scale-down.** The depth-8 spokes would fall to 0.59 mm and the chain can't
    shrink below 91 × 1.1 mm. An A5 edition needs a re-layout. **Confirm with Juan that Leo takes
    A3 before the plot job.**
  - The pen-up frame trace comes first, always.
- **Glyphs to author or avoid:** ⁰ and ⊆. Use "2^20" and "INSIDE". For → use "X1..X20". "−"
  must be a real minus in the certificate (author it if absent; "-" is acceptable).

## 11. Acceptance checks (the art critic marks each PASS/FAIL on the png)

1. **ONE RED RADIUS.** Exactly one red line reaches the rim/row 20.
   - `[A]`: it crosses the rim at 348.6° ± 0.5°, just before the 12 o'clock tick at about 11:37.
     Its first forks swing to **9 o'clock** first, then climb clockwise (270°, 315°, 337.5°,
     348.75°, back to 343.1°). Beyond the rim it continues straight and collinear to within 5 mm of
     the top margin.
   - `[F]`: it ends at x = 273.6 ± 0.5 mm, not near the centre.
2. **THE CARVING.**
   - No line ends inside ring/row 5.
   - The first ends are at ring 6: `[A]` 7 of them, evenly every 22.5° from 194° to 329°; `[F]` 8.
   - The count of lines crossing the rim/row 20 is **14 `[A]`** (13 black + red) or **15 `[F]`**
     (depth-7 sectors).
   - The refuted areas are bare paper.
3. **LOPSIDED, AND THE WEDGE.**
   - In the right half of the dial (x₁ = FALSE), or the left half of the `[F]` field, exactly one
     black line reaches the rim/row 20: `[A]` at ≈ 169.5°, `[F]` at x ≈ 140. Every other rim
     contact is on the other side.
   - `[A]`: the sliver between the red and 12 o'clock holds no black.
4. **CHECKING IS THE RED, AND IT COUNTS.** The red rule carries exactly 91 ticks at even pitch, in
   three lengths (41 short / 36 medium / 14 long), in 14 side-alternating groups. There is no
   arrow, no dot and no second red element. The captions give 43,658 `[A]` / 45,088 `[F]` clause
   tests against 91, and name the method.
5. **PLOTTABLE AND CLEAN.**
   - A `.gcode` sits beside the png, with 4 layers in the stated order and 2 swaps.
   - Minimum spacing is ≥ 0.8 mm.
   - The weight changes exactly at ring 8 `[A]` / row 7 `[F]`, and a caption says why.
   - No type touches the disc, the field or the void.
   - `[F]`: the Petersen tree has zero red, and the reference's boxes and circles are gone.
