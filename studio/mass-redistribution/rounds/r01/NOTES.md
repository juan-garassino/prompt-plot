# TRANSFORMER ATTENTION AS MASS REDISTRIBUTION — r01

Recreation of `studio/mass-redistribution/ref/reference.png`, with two elements
deliberately redesigned at Juan's request.

```
.venv/bin/python scripts/render_candidate.py \
  studio/mass-redistribution/rounds/r01/piece.py --fn mass_redistribution \
  --seed 7 --colors 5 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,black \
  --out gallery/studio/massredist/current/pp_massredist_v6.png
```

Render: `gallery/studio/massredist/current/pp_massredist_v6.png` (rounds v1–v6 kept alongside).

| | |
|---|---|
| commands | 28,728 (23,063 before postprocess) |
| draw / travel | 18,532 mm / 20,454 mm |
| pen cycles | 2,831 |
| per-pen | red 2,901 · blue 2,902 · ochre 3,423 · green 3,837 · black 4,338 |
| bbox | x 10.6–198.8, y 10.6–285.0 inside the 10–200 × 10–287 drawable — 0 out-of-bounds points |

Line spacing is ≥ 0.8 mm everywhere except inside the small filled centre dots
(`fill_disc`, r ≤ 1.5 mm): Q/K hatch 0.9, matrix bar hatch 0.8, V and Z ring
pitch 1.10–1.75, Z/V spokes 0.165 rad (≥ 1.0 mm at the rim), background dotted
rings 3.7 mm pitch.

## The numbers are real

Nothing on this plate is drawn by eye. Each of the ten Q/K densities is a
3-component Gaussian mixture; sampling it at `d_k = 8` equally spaced points
gives that token's vector; the vectors are standardised (LayerNorm, which is
what puts real contrast into the scores); `S = QK^T / sqrt(8)`; `A = softmax(S)`
row-wise. The same array drives the drawn densities, the matrix, and the wedge
angles in Z.

```
A = softmax(QK^T/sqrt(8))              row sum
  q0  0.019  0.543  0.031  0.042  0.365   1.000000
  q1  0.018  0.519  0.029  0.055  0.379   1.000000
  q2  0.279  0.095  0.383  0.066  0.177   1.000000
  q3  0.449  0.014  0.410  0.084  0.042   1.000000
  q4  0.059  0.410  0.094  0.045  0.392   1.000000
```

The seed is lucky in a useful way: q0/q1/q4 form one attention pattern (keys 1
and 4), q2/q3 another (keys 0 and 2). The plate therefore shows two visibly
different rows of behaviour rather than five near-identical ones.

---

# THE TWO REDESIGNS

## 1. The softmax grid

**What the reference does.** A 5×5 lattice of dots inside a dashed rectangle,
with warped curves threading through it. It reads as a mesh with something
happening behind it. Nothing about it is `n×n`, nothing about it is a
probability, and nothing about it is softmax — swap it for any other lattice and
the plate is unchanged. It was the weakest element on the sheet.

**What it is now.** The same rectangle, same place, same size, still black,
still a matrix — but drawn as an actual matrix plate in **two registers per
row**, with a transport map between them.

- **Lower register — the matrix proper.** Row *i* is a query, column *j* a key,
  and cell (i,j) holds a hatched bar of height ∝ `A[i,j]`. The five key columns
  are ruled with fine dotted verticals through the full height, so the n×n
  structure is unmistakable. A dotted rule crosses every row at the **uniform
  share 1/n**: a bar above it is mass that key *took*, a bar below it is mass
  that key *gave up*. Redistribution is then a fact you can read off one row.

- **Upper register — the unit rail.** A heavy horizontal bar the exact width of
  the grid, cut at the cumulative sums, so its five segments have widths
  `A[i,0..4]`. **Every row's rail is exactly the same length.** That is the row
  summing to one, drawn rather than asserted — five identical bars, cut in five
  different places. It ends in a unity cap, which is also the port the green
  output leaves from.

- **Between them — the transport map.** Twenty-five short lines, each running
  from a key's seat on the **uniform lattice** (a small open circle at the cell
  centre) to the middle of the **segment softmax actually granted it** on the
  rail. Where softmax gave a key more than its 1/n, its line leans outward and
  its segment is wide; where it gave less, the line leans in hard and the
  segment collapses to a hairline. Mass being reallocated from keys to queries
  stops being a phrase in the title and becomes the slope of 25 line segments.

**Why it is better.** The reference's lattice is decoration with a matrix's
outline. This version can be *read*: you can point at a cell, follow its
transport line to the rail, and see how much of that query's one unit of
attention that key ended up holding. And because the rails are all the same
length, the constraint that makes softmax softmax is visible at a glance,
without a caption doing the work. The caption `ROW SUM = 1` above the frame is
confirmation, not explanation.

## 2. The Z vector

**What the reference does.** A green vortex of swept curves in the lower right.
It is handsome, and it is an ornament: it has no five-ness, no weights, and no
visible relationship to the V discs it is supposedly made of. `Z = AV` is
labelled but not drawn.

**What it is now.** Five **output discs**, one per query, on the same descending
arc through the same lower-right footprint, in green.

Each disc is a circle of unit area cut into five wedges. **Wedge *j* subtends
exactly `A[i,j] · 2π`** — and it is filled with value vector *v_j*'s **own
texture**: the same rings, the same dot-rings, the same radial spokes drawn on
disc *j* in the ochre V column. So each output is literally the five values,
each present in proportion to its attention weight, and the wedges close the
circle because the row sums to one.

You can therefore read composition directly off the sheet: `z_0` is mostly
`v_1`'s wide rings with a large sector of `v_4`'s tight rings, `z_3` is split
almost evenly between `v_0`'s rings and `v_2`'s spokes, and the near-zero
weights survive as hairline boundary radii rather than being quietly dropped.

Under each disc sits a five-tick **recipe bar** repeating row *i* of the matrix,
so a reader can walk one weight from a cell in the grid, along its transport
line, to the wedge that carries it.

The green bundles now also mean something: each leaves **its own row's unity
cap** — the point where that query's whole unit of mass exits the matrix — and
carries it to that row's disc, five nested lanes instead of one anonymous
sweep.

**Why it is better.** The reference's vortex says "something swirls here". This
says "`z_i` is `Σ_j A[i,j] v_j`", in the only vocabulary the plate already
uses — V's textures and A's numbers — while keeping the green, the position and
the footprint. It also closes the plate's argument: ALIGN (Q·K), TRANSPORT (the
rail and its transport map), COMPOSE (the wedges).

---

# Everything else — faithfulness notes

Matched: A4 portrait; right-aligned two-line spaced-caps title; lower-left
footer with mid-dot separators; Q's five hatched densities with left-end dots
descending at the upper left; K's five mirrored with right-end dots at the upper
right; the fraction-set `A = softmax(QK^T/√d_k)` above the grid; V's five
concentric-ring discs on a vertical rail with connector stubs at both sides;
dense many-to-many red and blue fans converging on the grid's edge ports; ochre
fans sweeping up-right from V; large faint dotted background circles, a dotted
centreline, partial dotted verticals and scattered dots and open circles.

**The three things furthest from the reference (outside the two redesigns):**

1. **Type has no serif and no italic.** The reference sets `Q K V Z` and the
   formula in an italic serif (a Computer-Modern-ish math face). The shared
   stroke font is a single-weight geometric sans — it gained lowercase during
   this build, which fixed `softmax` and `d_k`, but `Q`, `K`, `V`, `Z = AV` and
   the title are upright sans where the reference is italic serif. This is the
   single largest visual difference on the plate.

2. **The ochre V→grid fans are combed, not tangled.** In the reference the
   ochre bundles cross each other freely and some strands wander far right
   before climbing. Here each `v_j` runs to its own column port (which is
   semantically correct — the grid's bottom ports *are* the key columns), so the
   five bundles stay nested and parallel. It is tidier and more truthful than
   the reference, and noticeably less turbulent.

3. **Ink weight is uniform.** The reference varies stroke weight — hairline
   background furniture, medium connectors, heavier type and dots. Everything
   here is one pen width per colour, so the background dotted circles sit closer
   to the foreground than they do in the reference, and the grid's centre does
   not go as dark. Partly mitigated by double-passing the unit rail, its ticks
   and the heavier type, but a real multi-weight plate would need a second black
   pen.

Minor: the reference is slightly wider than A4 (aspect 0.80 vs 0.71), so the
column-to-column gaps here are tighter and the vertical runs longer; the Q/K
densities are consequently a little shorter relative to their spacing.
