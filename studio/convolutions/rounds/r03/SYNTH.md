# Synth — convolutions after r02 + r03 (parallel) · 2026-09-28
route: designer
next round: r04 · parent: r03 (best so far — ranked over r02 on art min 4 vs 3, truth 8 vs 6, and r02 was judged *more* schematic than r01)

Ranking: r03 > r02. r02 stays on disk as the `real-kernel` flavour (its computed 5-layer stack and the
medial-axis-Y proof are real, but its layout is the textbook figure the rubric forbids); nothing from
r02 is merged into r04. Fabrication gate: not run (no double PASS). No uncommitted changes under
`promptplot/` in this piece's rounds.

## The instruction
Collapse r03's triptych into ONE field: delete the separate 11×12 output map (top-right panel, its
thin staircase and bold box) and write the output directly onto X's own lattice as a **diagonal
wavefront** — every stride-2 output node on the already-swept side of a staircase frontier
(i + j ≤ t, a valid order since output nodes are independent) shows its response `y = sum(K*patch)`
as signed rings centred on that node, so the blue skeleton-Y now emerges *inside the thumbprint*
across the swept half while the unswept half keeps its continuous distance-field rings, and the
5×5 LoG head sits on the frontier as the one plane lying on the field. The frontier keeps r03's
working diagonal (entering at the left frame, heading down-right); the freed right third becomes
quiet paper plus the title and a small reading key — enlarge or shift X into it if that raises
X's dominance, but no second panel. Put a `lineage:` line and a declared canon in HANDOFF.

## Mandates to close
1. **A1** — no separate output panel, no staircase copy, no leader lines: every coloured ring on
   the sheet sits on an X lattice node on the swept side of the frontier. Test: nothing stands apart
   from the field except title + key.
2. **S2** — inputs never hidden: inside the swept zone every input sample dot stays drawn,
   including each window's centre (the −1.00 tap). Response rings wrap *around* the centre sample
   and stop ≥ 0.8 mm short of every neighbouring sample dot — pick lattice pitch / ring pitch /
   bin count so this holds (enlarge the cell if needed). Test: 0 missing inputs in any drawn window.
3. **A10** — close the medial seams: no staggered-dead-end zipper (r03 lower lobe x 90–95, y 20–60),
   no hairpin slit (upper lobe x 115–135, y 125–140), no hairpin < 2 mm; perpendicular pitch
   ≥ 1.0 mm everywhere incl. the 45° stretch at y≈150. This is r01's contour continuity — restore it.
   Rings stop at the frontier with a clean cut, no hooks at stair corners.
4. **S1** — reading key, tiny, near the title: `X`, `K 5×5 · stride 2`, `Y = K ∗ X`; crimson = +,
   blue = −, ring count = |y| bin, dot area = x; ONE code for y = 0 (pick the dot or the hollow
   ring, not both).
5. **A9** — the head is a plane: second keyline 1.5 mm off the kernel box's right+bottom edges,
   field rings stop at that shadow line; delete both dotted leashes and every hollow circle with no
   stated meaning.

Also record in NOTES (for S3, argued): the check that thumbprint ring index = d/pitch matches the
corridor dot areas (Spearman), so the science critic can confirm the rings encode X.
Deferred: A12 (title multi-pass/I spacing), A13 (travel share — re-measure after the mark set changes).

## Preserve
- **Working diagonal + asymmetry** (r03): path entering at the left frame edge, running down-right;
  masses off-centre; no axis at u = 0.5.
- **Thumbprint X dominance** (r03, left ~60 %): distance-field rings, |∇d| = 1, constant pitch.
- **The arithmetic** (r03, sci-confirmed): 5×5 LoG σ = 1 cell, zero-sum by disc AREA, valid conv
  stride 2, responses = K∗X (ρ 0.92), deterministic regardless of seed.
- **Ben-Day kernel** (r03 head at x 104–136, y 53–85): 25 signed discs, area ∝ |w|.
- **Display title** (r03 bottom-right, `giant_type` 0.8 mm) — keep weight, fix placement ≥ 10 mm
  off the drawable edge like everything else.
- **3 pens** (black / crimson / dodgerblue), no decoration anywhere, draw ≈ 14 m.
- **r01 contour discipline**: continuous rings to the medial axis, min gap ≥ 0.86 mm (the benchmark).

## Do not
- Do not keep any second grid, panel, inset or thumbnail — that is the triptych again.
- Do not draw a response ring over an input sample or erase lattice dots to make room.
- Do not use dotted leashes, arrows or tracks that end on empty paper.
- Do not add captions beyond the title + one key strip (no `blur/ridge` style labels — r02's worst type).
- Do not return to r02's layout (tiles, fans, pyramid, footnote row) or to bilateral symmetry.
- Do not clip rings with staggered per-ring dead-ends; cut them on one clean line.
