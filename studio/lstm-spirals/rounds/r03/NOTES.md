# lstm-spirals r03 — forget-gate-vortex · parent: r01 · 2026-09-28

(r02 is an abandoned partial start and was ignored; nothing from it is used.)

## Render

```
.venv/bin/python scripts/render_candidate.py studio/lstm-spirals/rounds/r03/piece.py \
  --fn lstm_forget_vortex --seed 7 --paper a4 --orientation portrait \
  --palette dodgerblue,crimson,black \
  --out gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.png
```

- final: `gallery/studio/lstm_spirals/current/pp_lstm_spirals_forget-gate-vortex_v20.png` + `.gcode`, seed 7
  (v20 is v19 after a no-op refactor; the two gcodes are identical apart from the
  timestamp line)
- seeds 3 and 11 (`…_v18_seed3/11.png`) are visually the same plate: the seed only
  draws the distractor values x_t and shuffles seed order. The geometry comes from the
  gates, and on this task the gates depend on the write flags, not on the values.
- checks: `.venv/bin/python studio/lstm-spirals/rounds/r03/check_plate.py <gcode> 7`
- training: `.venv/bin/python studio/lstm-spirals/rounds/r03/train_lstm.py [out.npz]`
  (H=1, T=30 defaults; about 1 min)

## Mandate responses

LEDGER.md does not exist for this slug and FEEDBACK.md is empty, so there are no
J*/A*/S* rows. The binding brief is the curator note plus DESCRIPTION.md
(the forget-gate-vortex paragraph and the Weak list). Each point is answered below.

| id | mandate | response |
|---|---|---|
| C1 | Keep two black/crimson vortices on one vertical axis | FIXED. Black h_t sits above and crimson c_t below, on one vertical axis at u=0.55. Axis stubs are labelled `h_t` (top) and `c_t` (bottom), and the axis shows through both eyes. |
| C2 | Keep streamlines interleaving around the saddle | FIXED, and now it comes out of the physics. There is a true saddle between two screened vortices. The arriving input lines split at it: blue climbs the left side into the cell and black falls down the right side into the hidden state. That is r01's "black down one side, red up the other" sheaf, this time as basin colouring. |
| C3 | Cut or fold in the LSTM EQUATIONS and FLOW LEGEND blocks and the arrow/label callouts | FIXED. All of them are cut. No equation block, no legend block, no arrows, no gate leaders, no t-labels. The only text left is the title, a one-line subtitle, two axis labels and a single footer line. Each footer clause is inked in the pen it names, so the footer also works as the swatch. `c_t = f_t c_{t-1} + i_t g_t` is folded into the drawing as the colour rule. |
| C4 | PLOTTING: pens only where they carry meaning; one clean layer each with a stated order; spatial ordering; minutes per layer | FIXED. There are 3 pens, each with a stated meaning (see HANDOFF). Layer order is blue → crimson → black, light to dark, with type last in black. Per-layer budget is below. The 5 black hops over 100 mm are between the corner type blocks and the figure. |
| C5 | Name the LINEAGE | FIXED. Marcel Duchamp, *Rotoreliefs* (1935) and *Anemic Cinema* (1926). What the plate takes from them is their order: a disc of rings reads as a spiral once it turns, and here one turn is one time step. |
| D1 | [brief] Real small LSTM computes f_t and o_t; red sink strength = f_t, black = o_t | FIXED. A 1-unit LSTM is trained here on the analog latch, the weights are baked into the piece, and the forward pass runs live. Red annulus t winds with k=f_t and black annulus t with k=1−o_t. The drawn angles match the designed ones to within 0.04° (checks §2). |
| D2 | [brief] T stacked time slices; red keeps its winding (f≈1) while black resets | FIXED. There are T=12 annuli per lobe, rim = t1 and eye = now. The red hold annuli are closed rings (pitch 0.01°); the three write annuli open into 13.8° drains. The black lobe drains at 31–33° on every step. |
| D3 | [brief] labels and legend shrink to a footer line | FIXED (see C3). |
| W-concept | textbook schematic; mechanism not in the geometry | FIXED. The mechanism is the geometry: the angle of the ink is the gate value. |
| W-tension | exact 180° rotations about the sheet centre | FIXED. The lobes are unequal (circulation 1.3 : 1), the axis is off-centre (u=0.55), and the two lobes have different textures (rings vs a whirl). The saddle sheaves turn it into an S. It is still one vertical figure-eight, see Self-critique. |
| W-craft | red lines ran through the label block; plus mark on the L | FIXED. Nothing crosses any glyph. The plus marks are gone. |
| W-hierarchy | the dotted t-rings were swallowed | FIXED by removal. The t-rings are now the annuli themselves, so time is the texture rather than a dotted overlay. |
| W-grid | leaders ending nowhere, ragged right labels | FIXED. There are no leaders. Title and footer are flush-left on x=12 mm, and the axis labels are centred on the axis. |
| W-space | empty left third was residue | ARGUED. The left field is still empty, but its right edge is now the silhouette of the eight and the title sits over it. I kept it quiet on purpose because the whole plate is one figure. A critic could still read it as leftover. |
| W-depth | flat and undeclared | ARGUED, declared. Depth is carried only by claim order (the cell's rings own the paper first, so input and hidden-state lines stop where they meet them, i.e. pass behind) and by the black lobe being drawn lighter (1.35 mm vs 0.95 mm pitch). Otherwise the plate is declared flat, like a Rotorelief disc. |

## What changed from parent

- **Field.** r01 had two point sinks with free sink/vortex strengths plus an input
  drift. r03 has two co-rotating *screened* vortices (u(r)=g·r/(r²+s²)·e^(−r/λ),
  λ=25 mm) whose stream function Ψ defines **orbits**. The drawn field is
  `v = rot90∇Ψ − κ∇Ψ`, so every line crosses its orbit at exactly atan κ. κ is not
  a parameter: it is read per annulus from the gates. I rejected unscreened 1/r
  vortices after measuring them: their separatrix lobes reach only 0.41× half the
  spacing past each centre (two slivers, v2). The first per-centre-radius banding (v1)
  chopped the eccentric orbits into arcs. Banding by Ψ level fixed that.
- **Composition.** The legend and equation strip are gone. The two lobes now fill
  the height as one figure-eight on blank paper, with a weighted display title
  top-left and a one-line footer. The input stream is no longer six dots on the
  left. It is the narrow band of orbits just outside the eight near the saddle, and
  the saddle splits it between the two memories.
- **Colour.** Colour now carries a rule instead of a category. Crimson marks an
  annulus where f_t > i_t (the cell keeps), blue marks f_t < i_t (the cell is
  written), and black is the hidden state.

## Measurements / computations

**The network** (`train_lstm.py`, numpy, exact BPTT; grad-check max rel. err 7e-9 at
init; Adam 8000 steps, B=128, T=30). The task is the **analog latch**: a value
v∈U(−0.8,0.8) arrives on every step and y_t must equal the value at the last write.
Held-out MSE of the baked (5-decimal) weights on 2000 sequences: 1.5e-5 (T=12),
1.7e-5 (T=20), 2.1e-5 (T=40), 2.2e-5 (T=100), against a predict-zero baseline of
0.21. Two earlier trainings were rejected because they never used the forget gate:
{±1} bits with H=3, and analog values with H=3. Both solved the task through h-feedback
attractors with f≈0.3–0.8. With one unit the only solution left is the textbook one.

Gates on the plate's sequence (seed 7, writes at t=1,5,10):

| t | write | x_t | i | f | o | c | y |
|---|---|---|---|---|---|---|---|
| 1 | 1 | −0.28 | 0.7296 | 0.2143 | 0.9776 | +0.0526 | −0.284 |
| 2–4 | 0 | −0.56, +0.24, −0.68 | 0.0017 | 0.9989 | 0.9837 | +0.0527…0.0528 | −0.287 |
| 5 | 1 | +0.06 | 0.7300 | 0.2143 | 0.9776 | −0.0142 | +0.062 |
| 6–9 | 0 | −0.21, −0.71, +0.01, −0.74 | 0.0017 | 0.9989 | 0.9837 | −0.0141…−0.0134 | +0.060 |
| 10 | 1 | −0.11 | 0.7297 | 0.2142 | 0.9776 | +0.0194 | −0.112 |
| 11–12 | 0 | −0.69, −0.65 | 0.0017 | 0.9989 | 0.9837 | +0.0197…0.0200 | −0.116 |

y tracks the last written value within 0.02, and the distractors do not enter.

**Gate → ink, read back off the gcode** (`check_plate.py` §2: angle of every drawn
segment to its orbit, median per annulus). Red write annuli are designed 13.77° and
drawn 13.75–13.78°. Red hold annuli are designed 0.01° and drawn 0.22–0.26°; that
difference is the measurement floor (0.001 mm coordinate rounding on 0.7 mm segments
plus ring-closure joins). Black annuli are designed 31.16° at writes and 33.24° at
holds, drawn 31.15–31.20° and 33.23–33.26° (n = 130–984 segments per annulus).

**Single-centre law** (§3, RK4 at 0.05 mm step, one exact turn through a lone
screened vortex): radius ratio per turn = 0.214325 for k=0.214326, 0.998949 for
k=0.998950, and 0.022397 for k=0.022401. The radius is multiplied by the gate value
per turn to 4e-6.

**Hold rings stay rings:** every orbit's |∇Ψ| peaks on the far ray (ratio min/far is
0.998 at r=5 and 0.31 at r=45 near the saddle), so seeding rings at ≥ sep on the far
ray keeps them ≥ sep all the way round. The closure drift is 2πrκ = 0.04 mm at r=40.

**Spacing** (§4, samples every 0.4 mm): 0.65 % of samples lie within 0.8 mm of another
stroke; 0.36 % are near-parallel and side by side. Split by zone, 50 of those samples
are footer type (glyph strokes of 2.2 mm capitals) and **16 are in the field
(0.09 %)**. The weighted title is excluded because its 0.35 mm passes are the weight.

**Constants that are drawing choices, not data:** κ_in = 0.55 for the arriving input
(it has passed no gate), the envelope width of 14 mm, saddle reach ±34 mm, λ = 25 mm,
circulation ratio 1.3 : 1, black pitch 1.35 mm, cell/input pitch 0.95 mm.

## Plot budget

Measured on `…_v20.gcode`. Time estimate uses Leo settings: F600 draw, F2000 travel,
2 s per pen cycle.

| layer (order) | meaning | strokes | draw | travel | longest stroke | hops >100 mm | est. |
|---|---|---|---|---|---|---|---|
| 0 dodgerblue | write annuli + input draining into the cell | 176 | 2.99 m | 2.18 m | 53 mm | 2 | 11.9 min |
| 1 crimson | hold annuli (the cell keeps) + `c_t` | 50 | 4.06 m | 0.57 m | 273 mm (one ring) | 1 | 8.7 min |
| 2 black | hidden state, input to it, axis, all type | 245 | 6.17 m | 4.64 m | 142 mm | 5 (corner type ↔ figure) | 20.8 min |
| total | | 471 pen cycles | 13.22 m | 7.42 m | | | **≈41 min + 3 swaps** |

20,309 commands, no out-of-bounds points (x ≤ 183 mm on a 200 mm drawable). Every
stroke is short enough to be a batch boundary; the longest is one closed ring.

## Self-critique

| dimension | score | why |
|---|---|---|
| Hierarchy | 8 | The black whirl reads at 3 m, the crimson target is a clear second, the blue drains are third, the type fourth. |
| Grid & alignment | 6 | Title and footer share x=12 and the axis labels are centred, but the figure is not locked to any module and the right margin is whatever the lobes leave. |
| Tension & asymmetry | 6 | Unequal lobes, an off-centre axis and the S of the saddle sheaves. It is still one upright figure-eight: a strong but stable shape. |
| Negative space | 7 | A generous left field whose right edge is the eight's silhouette. It may still read as leftover. |
| Craft for pen | 8 | Rings are solid and evenly pitched, 0.09 % side-by-side ink in the field, 41 min on 3 clean layers. The blue input tails end on an orbit cut that is visible as a straight-ish edge at lower right. |
| Concept | 8 | The gate is the angle of the ink. A closed ring is perfect memory, and forgetting is literally a drain. "The forget gate is a drain" is the one-line twist. |
| Depth | 5 | Declared flat apart from claim-order occlusion and the lighter black pitch. |

**The single worst thing:** the heaviest mass on the sheet carries the least
information. The output gate is open on every step (o = 0.978–0.984), so the black
lobe's 12 annuli differ by 2° (31.2° vs 33.2°), which nobody will see, yet that lobe
dominates the page. The three blue drains are also identical, because the trained
gate fires the same way at every write (f = 0.2143). Both are honest to this task,
but a richer task, such as a two-unit net with a gated readout, would give the black
lobe something to say.

## Engine requests

1. `_stroke_text(..., proportional=True)` advances by the glyph's ink width but draws
   the glyph at its cell x, not its ink x. Narrow glyphs therefore run into the next
   one: `i` has ink at x=1.8 with a 1.1 advance, so `i_t` reads as `į`. The piece
   works around it locally in `_rich` by shifting each lowercase glyph to its side
   bearing. The proportional capital `I` also leaves gaps ("DRA IN").
2. `Scene3D.lines` has `pause_resume` and `over` but no **terminate** mode, where a
   line ends at its first crowded sample (classic Jobard–Lefebvre). Converging sinks
   need that; pause-resume turns their eyes into crumbs. The piece queries
   `Occupancy.crowded()` and truncates before calling `lines()`.
3. `lines()` accepts a single `Occupancy`. Two-tier spacing (a family keeps 1.35 mm
   from itself and 0.95 mm from everything else) needs a second grid registered by
   hand with `Occupancy.add`.
