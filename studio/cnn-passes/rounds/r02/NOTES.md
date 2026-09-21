# cnn-passes — r02 · TRUE MECHANISM

**Thesis.** Same two-register layout as `BRIEF.md`, but **every field on the sheet
is a real computed array**. A small CNN runs one honest forward pass and one honest
backward pass in numpy (`net.py`); `piece.py` does nothing but draw those arrays.
Where the reference is decorative, this plate is literal.

**The twist.** The pass drawn here is one the network gets **wrong**. The top
register is the answer it gives (class 1, p = 0.533); the bottom register is the
sheet telling it the answer was class 6. Backprop only exists because of the gap
between the two registers, so the plate draws the case where it does something.

Files: `net.py` (the arithmetic + `summary()`), `piece.py` (the plate).

---

## Render command

```
.venv/bin/python scripts/render_candidate.py studio/cnn-passes/rounds/r02/piece.py \
  --fn cnn_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,crimson \
  --out ~/Downloads/pp_cnn_passes_mechanism_v9.png
```

Final render: `~/Downloads/pp_cnn_passes_mechanism_v9.png` (+ `.gcode` beside it).
Earlier rounds kept at `v1 … v8` — nothing overwritten.

Print the checkable numbers with `.venv/bin/python studio/cnn-passes/rounds/r02/net.py`.

---

## Pens

| pen | colour | carries |
|---|---|---|
| 0 | black | structure, plane borders, type, furniture, the non-highlighted forward channels |
| 1 | dodgerblue | **the highlighted forward channel** — channel 0, the one with the largest `Σ\|A1\|`. Its plane is the front of every forward stack, its sheaf is blue, and the softmax winner's disc is blue. |
| 2 | crimson | the whole backward register |

Cream paper is the fourth colour: the ReLU-dead half of the plane is bare paper,
never decorated.

**3 pen swaps.** Drawn length by pen (G1 segments): black 18 248, blue 6 438,
crimson 13 903.

## Plot budget

| | |
|---|---|
| paper | A3 landscape, drawable 10–410 × 10–287 mm |
| drawn length | **19.48 m** |
| travel | 17.35 m |
| strokes (pen-downs) | 4 981 |
| commands | 58 516 |
| drawn bbox | X 13.00 – 409.50, Y 13.00 – 286.50 — inside the drawable, zero violations |
| ink density | of 37 969 inked 0.5 mm cells: 83.5 % one pass, 14.6 % two, 1.7 % three, **68 cells above three, worst 6**. Nothing floods. |
| determinism | two renders of seed 7 produce byte-identical GCode |

The only out-of-drawable coordinate in the file is the final `G0 X0 Y0` park, pen up.

---

## The proof the arithmetic is real

`net.py` differentiates by hand and checks itself against central differences:

```
GRADIENT CHECK (central differences, eps = 1e-5)
  dW1[1,2,3]: analytic +0.005550  numeric +0.005550  rel.err 3.61e-09
  dWc[40,2] : analytic +0.007782  numeric +0.007782  rel.err 1.96e-10
  dX[11,9]  : analytic +0.029143  numeric +0.029143  rel.err 2.29e-10
```

Three gradients at three different depths of the chain (input, first-layer filter,
classifier) agree with the numerical derivative to ~1e-9 relative error. That is
only possible if the conv, ReLU, max-pool routing, second conv, softmax and
cross-entropy are all genuinely wired together.

### Forward

```
X    (24,24)      min -1.0266  max +1.0519  mean -0.0000   sum|.|  199.50
W1   (4,5,5)      min -0.4554  max +1.0000  mean +0.0000   sum|.|   29.42   each kernel exactly zero-mean
A1   (4,20,20)    min -4.9660  max +4.8695  mean -0.0087   sum|.| 1418.03
R1   (4,20,20)    min  0        max +4.8695 mean +0.4388   alive 782/1600 = 0.489
P1   (4,10,10)    min  0        max +4.8695 mean +0.9380   sum|.|  375.19
A2   (6,8,8)      min -6.9935  max +3.3379  mean -0.9881   alive 111/384 = 0.289
P2   (6,4,4)      min  0        max +3.3379 mean +0.6969
z    (6,)         min -4.0284  max +1.4439
p    [0.5326, 0.0022, 0.0047, 0.0287, 0.1359, 0.2959]      sum = 1.000000
                  argmax = class 1 · target = class 6 · L = -log p_6 = 1.2178
```

### Backward

```
dz = p - y  [+0.5326, +0.0022, +0.0047, +0.0287, +0.1359, -0.7041]   sum = +0.0e+00
dWc  (96,6)       min -2.3503  max +1.7779  mean +0.0000   sum|.|   94.22
dP2  (6,4,4)      sum|.| 10.2133
dR2  (6,8,8)      sum|.| 10.2133   nonzero  96/384   <- unpool: exactly one per 2x2 window
dA2  (6,8,8)      sum|.|  4.7354   nonzero  48       <- the second ReLU mask halves it
dP1  (4,10,10)    sum|.| 13.2834
dR1  (4,20,20)    sum|.| 13.2834   nonzero 368/1600 = 0.230
dA1  (4,20,20)    sum|.| 11.2321   nonzero 309      <- 59 killed by the ReLU mask
dW1  (4,5,5)      min -0.6407  max +0.5205
dX   (24,24)      min -0.5193  max +0.4019  sum|.| 25.4683
```

Three invariants a fake would not satisfy:

1. `sum(p) = 1.000000` and `sum(dz) = +0.0e+00` exactly — softmax normalisation and
   the fact that `p - y` is a difference of two distributions.
2. `sum|dR2| == sum|dP2|` and `sum|dR1| == sum|dP1|` to the last digit: unpooling
   **moves** gradient, it never creates or destroys it.
3. `nonzero(dR1) = 368` of 1600 (23.0 %, i.e. one cell per 2×2 window minus the 32
   windows whose pooled gradient is exactly 0), and `nonzero(dA1) = 309` — the
   ReLU mask kills exactly 59. Both counts are printed in the plate's legend.

### The honest footnote on the ReLU kill

Max-pooling pre-selects the *winner* of each window, and in a ReLU'd map the winner
is almost always alive. So the mask only kills 59 of 368 — the windows that were
entirely dead. The interesting gating is therefore in the **forward** register,
where 51.1 % of the R1 plane is bare paper, and in the **mask frontier** shared by
both registers. That number is reported rather than dramatised.

---

## What each mark carries

| element | mapping |
|---|---|
| input plate `X` | Ben-Day: dot **radius** = \|X\|, filled/open = sign. The concentric rings are the chirp's real wavefronts. |
| conv planes | marching-squares isolines of the real 5×5 Gabor filters |
| feature planes `A1` | isolines of A1; the heavy two-pass closed curve is the exact **iso-0** — the ReLU frontier |
| ReLU planes `R1` | isolines of `max(0, A1)`. Where the pass zeroed, **bare paper**: 51.1 % of the plane. |
| pooling planes `P1` | one mark per pooled cell, radius = value, on the coarse 10×10 lattice — visibly half the resolution of its neighbour |
| deeper planes `A2` | isolines of A2 — fewer, smoother forms on smaller planes: resolution down, abstraction up |
| classifier bar `Wc` | 32 tick rows, length = mean \|Wc\| over 3 matrix rows each |
| softmax column | circle **area** = p_k (radius = R·√p, spiral-filled at a fixed 0.58 mm pitch), so the ink length in each disc is proportional to p_k and **the column's total ink is conserved at 1** — normalisation drawn, not asserted |
| flow sheaves | 5 dotted strands per channel; each strand's dash **duty** = that band's real row-energy in the channel's array. Bipartite fans (pool→deeper, deeper→classifier) use the real coupling `‖W2[k,c]‖` / `‖Wc block‖`. |
| `∂L/∂x` plate | same Ben-Day law, threshold raised to 14 % of peak (cells are *dropped*, never added) |
| `∂L/∂(conv)` | isolines of the real filter gradients `∂L/∂W1` |
| `∂L/∂A1` | the same array contoured — broad islands where the gradient actually lives |
| `∂L/∂(ReLU)` | the surviving gradient marks **inside the real iso-0 outline of A1** — the same curve as the forward twin, in crimson |
| `∂L/∂P1` | the real `dR1` scatter: 368 marks of 1600 cells, one per 2×2 window |
| `∂L/∂A2` | 48 surviving marks of 384 cells, drawn loud — the emptiness is the statement |
| gradient tiles | hatch **duty** = \|∂L/∂Wc\| column norm, hatch **angle** = sign of dz (+45° / −45°) |
| legend cell 1 | the drawn result IS `np.correlate(X[12], W1[0][2], 'valid')` of the two drawn traces |
| legend cell 3 | a real 4×4 patch of `R1[0]` (rows 6–9); the red cells are its real argmaxes; the 2×2 marks are the real pooled values |
| legend cells 2/4/5 | the real alive counts, the real p vector, the real L and dz |

Nothing on the sheet carries nothing. The only display liberty is a **resample**:
contoured arrays are bilinearly upsampled ×4–6 with 1–4 box passes before marching
squares, exactly what any contour plot does. Values are never altered.

## Column registration — verified, not asserted

Every gradient twin uses the **same stack spec and the same column centre** as its
forward stage (r02 originally shrank the backward stacks to 86 %, which broke the
congruence of the twin curves — fixed in round 5):

```
max |x(forward plane corner) - x(backward twin corner)| = 0.0 mm
plane sizes identical: True
```

The ReLU frontier at column 3 is therefore literally the same curve, drawn once in
black/blue above and once in crimson below, at the same size on the same column. A
thin rule between the registers carries one tick per column axis.

Ink-centroid audit (content, not geometry): C2 +0.29 mm, C3 −0.30 mm, C4 +0.18 mm,
C1 −0.92 mm, C5 −2.00 mm. C5 drifts because only 48 gradients survive there, so the
few marks pull the centroid — the planes themselves are pixel-identical.

---

## Per-round changes

**r02-v1** — first full plate. Working: axonometric stacks with true occlusion,
Gabor/A1 contours, Ben-Day input plate, two registers. Broken: the 4×6 coupling fan
collapsed into a black knot at the pool→deeper neck (and the `···` ellipsis sat
inside it); the `W1` caption crossed the register rule; softmax circles at area ∝ p
were too weakly differentiated to read as a winner; legend cells 4 and 5 collided at
the bottom; hierarchy flat — everything mid-sized.

**v2** — hierarchy and rhythm. Added `FORWARD PASS` / `BACKWARD PASS` as display
type running up the left margin (the only poster-scale type on the sheet; hairline
caption type everywhere is the lab-figure default the rubric fails). Softmax discs
became spiral fills so ink length ∝ area ∝ p — the winner is now a solid blue mass.
Column 5 forward switched from a dot lattice to contours (the "fewer, smoother
forms" story). Column 2 backward switched to a contoured field so it stops
duplicating column 3. Bundle waists made per-pair instead of one shared point.
Whole vertical rhythm re-cut so no caption crosses a rule.

**v3** — bundles re-read as dotted rather than solid (period 1.75 mm, duty capped at
0.58): 24 solid curves through a neck is a scribble, 24 dotted ones is a bundle.
`∂L/∂x` plate given a 14 % threshold and a steeper radius law, because at the
forward plate's floor every cell inked and it read as mud. Relabelled the backward
classifier column, which was calling a `∂L/∂Wc` bar `∂L/∂z`.

**v4 / v5** — the per-channel identity fans became 5-strand sheaves whose duty is
the channel's real row-energy profile (one curve per channel under-drew the
transport and the registers' flow disappeared). v4 shipped a bug — the backward
sheaves read their plane sides un-mirrored and drew solid bars straight through both
stacks; v5 fixed the direction.

**v6** — the sparse gradient planes (`∂L/∂A2`, `∂L/∂P1`, `∂L/∂(ReLU)`) drawn LOUD
rather than faint, so the emptiness reads as a statement; `∂L/∂A1` contour pitch
opened from 1.6 to 2.1 mm with more display smoothing, turning confetti into
islands; `∂L/∂W1` nest thinned; captions fixed for glyphs the stroke font lacks
(`[`, `]`, `Σ`, `−`).

**v7 / v8 / v9** — every gradient twin resized to exactly its forward stage (see
above); `∂L/∂x` plate grown to match `X`; `dW1` nest thinned once more; word spacing
in the legend; left-margin captions nudged clear of the spine.

---

## Honest critique — the weakest part

**Column 2 backward (`∂L/∂A1`) is still the weakest plane group on the sheet.**
Mathematically `∂L/∂A1 = dR1 ⊙ M1` *is* the same array that column 3 draws as the
mask's output, so the two columns are showing one array twice under two different
readings (contoured field vs. gated scatter). That is the truth of the chain rule —
ReLU's backward pass has no content of its own beyond the mask — but it means one
of the eight columns is carrying a distinction the viewer has to be told about
rather than see. The alternatives were worse: inventing a difference would have
broken the whole premise, and merging the columns would have broken the brief's
one-to-one registration.

Second weakness: **the plate is still, unavoidably, an infographic.** The brief asks
for a recreation of a labelled two-register diagram, which is exactly the shape
`DESIGN_RUBRIC.md` dimension 6 calls a schematic. I followed the brief. Where the
rubric could be honoured inside that shape I honoured it — gradient-even contour
levels, bounded dot/hatch densities, display type with real weight, a single loud
scarce accent, shaped negative space between the registers — but this plate would
not pass dimension 6 as a free studio piece and should not be judged as one.

Third, smaller: **travel (17.35 m) is almost as long as the drawn line (19.48 m).**
The dotted sheaves and the mark fields produce ~5 000 short strokes, and the
per-colour stroke optimiser cannot do much with them. It plots fine, it just plots
slowly.

## Requests for shared code (nothing under `promptplot/` was touched)

1. `render_candidate.py` loads a candidate with `spec_from_file_location` and never
   registers it in `sys.modules`. Two consequences a piece has to work around:
   `@dataclass` raises at import time (`sys.modules[cls.__module__]` is `None`), and
   a sibling module next to `piece.py` will not import without the piece pushing its
   own directory onto `sys.path`. Both are done locally here; a two-line fix in the
   loader (`sys.modules[name] = mod` before `exec_module`, and inserting the piece's
   parent on `sys.path`) would remove the trap for every future round.
2. The single-stroke font has `∂`, `σ`, `×`, `∗`, `·` but no `Σ`, no `[` `]`, no
   `−` (U+2212) and no arrow glyphs. `_stroke_text` warns and drops, which is the
   right behaviour, but a `Σ` and brackets would be worth adding for ML plates.
