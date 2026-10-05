# resonance-ffn r03 — two interferences (mechanism) · parent: r01 (v9) · 2026-09-28

**Lineage.** Early computer art: Charles Csuri and James Shaffer, *Sine Curve Man* (1967, IBM 7094
and drum plotter). A drawing and its function-mapped copy share one plotter sheet, and the function
is the content. The ORDER it lends is **a form and its transformed image, set side by side**. Here
the forward pass is the form and the backward pass is its image. The hero field is mapped by a
homothety of ratio −0.39 through the loss-side node, and each FFN streamline is mapped by d/dh. The
siblings have already taken Riley *Current* (resonance r04), Young 1807 (resonance r05) and LeWitt
(backprop r02), so this plate uses none of them.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance-ffn/rounds/r03/piece.py \
  --fn two_interferences --seed 9 --paper a4 \
  --palette goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black \
  --out gallery/studio/resonance_ffn/current/pp_resonance_ffn_two-interferences_v13.png
```

- final: `gallery/studio/resonance_ffn/current/pp_resonance_ffn_two-interferences_v13.png` and `.gcode`, **seed 9**, A4 portrait.
- The seed chooses a network. The seed is a new, exact forward/backward computation. I tried seeds 7, 9,
  22 and 26. **Seed 9** has 9 of its 12 hidden units saturated, so the derivative's twin peaks are most
  visible, and its ∂L/∂Q and ∂L/∂K are comparable. On seed 7, ∂L/∂K is 3 % of ∂L/∂Z and draws as a flat
  line.
- `--colors` defaults to the palette length (6). **Palette order = stream order.**
- v1–v12 are self-rounds and v13 is the final. Scratch seed renders are not in Downloads.

## Mandate responses

`studio/resonance-ffn/` has no LEDGER.md, so there are no A*/S* rows. The work order is FEEDBACK.md
(J1), the curator note (C1–C6), and DESCRIPTION.md's Weak list (W*) and If-only-iterating list (I*).

| id | mandate | status |
|---|---|---|
| J1 | DOTTED LINES: continuous dots at a tight constant arclength pitch, no sparse gaps, no bunching at ends, same pitch family-wide, never dashes/hairlines | **FIXED.** There is one dot: a closed loop of r = 0.12 mm that inks about 0.6 mm under a 0.35 nib. It is never a micro-dash. Pitch is **1.00 mm centre-to-centre** on every dotted path on the sheet. Each path gets n = round(L/1.0) intervals, so the pitch divides it exactly (max deviation ±0.5/L). The pitch is **end-anchored**, so both ends carry a dot. Where three dotted paths converge on the fan's left node, every end dot is ≥ 2.0 mm (2 pitches) from the others. 290 dots in total. No dotted path was replaced with a dash or a hairline. |
| C1 | keep the family grammar: Q crimson / K blue packets, two-source interference, V goldenrod, Z green, FFN violet | **FIXED.** Every colour keeps its family meaning. Q and K are carrier packets feeding the hero's two sources, and the hero is the Huygens crest construction. |
| C2 | no pen cap; 6 colours if each carries meaning; one clean layer each, order stated | **FIXED.** 6 pens and 6 meanings. Each pen is one layer that is never re-entered. They stream light → dark (see Plot budget). |
| C3 | strokes spatially ordered for batching | **FIXED.** Within each layer the order is greedy nearest-neighbour from the top-left, and a stroke may be drawn in either direction. Travel is 28 % of draw. Layers 1 and 3 each cross the sheet exactly once, from the top register to the bottom register (197 mm, the longest hop). The longest single stroke is 198 mm (a Q packet, 20 s), so every stroke fits inside a batch. |
| C4 | minutes per layer + total | **FIXED.** Table below. |
| C5 | waste: 3,725 pen cycles and 101 % travel; dotted runs must earn their cycles | **FIXED.** **605 pen cycles (−84 %)** and **travel 3.16 m = 28 % of draw**. Every dotted run is a real relation: a projection into a source, the V → Z sum bus, the Z/∂Z → node links, the hero → node → twin axis, and the mirror line. |
| C6 | name the LINEAGE | **FIXED.** Csuri & Shaffer, *Sine Curve Man* (1967). See top of file. |
| W-dots | [craft] 0.42 mm micro-dash + 1.8 mm paper reads as dashed; converging paths interleave | **FIXED** (= J1). |
| W-schematic | [concept] labelled stages, bracket, fractions, arrowheads | **PARTLY.** Cut: all stage names (expand / nonlinearity / project and their transposes), the FFN bracket, `Q·Kᵀ/√d_k`, `softmax`, all arrowheads, and the expand/project packets. Kept: single-letter tensor labels and five ∂L/∂· fractions, because colour alone cannot say "gradient". It is still a diagram at 1 m. |
| W-space | [space] lower third jammed, no gap > 3 mm | **FIXED.** The lower third now holds only the twin, two gradient rows and the right half of the fan. The closest ink-to-ink gap between zones is 5.5 mm (the fan's backward shoulder to the twin's upper-right crests). The others are ≥ 16 mm (∂Z to twin 16.2, V to hero 22.0, fan to hero 36.6), and y 13–40 (sheet) is quiet ground except for the title. |
| W-collisions | [craft] V knot, ∂Q/∂K overlaps, FFN bracket on a packet | **FIXED.** V is 4 rows at 6.4 mm pitch with peak ≤ 2.9 mm, so 0.45 × pitch holds exactly. There is one ∂Q row and one ∂K row. The bracket is gone. |
| W-hierarchy | [hierarchy] hero ~20 % of width, nothing dominates, the ochre knot is the accident | **FIXED.** The hero is 115 mm wide (**61 % of the drawable width**) and 66 mm tall. It carries 7.8 m of the 11.1 m of ink. The fan is second and the twin (0.39 scale) is third. |
| W-tension | [tension] mirror-symmetric top half, centred title | **PARTLY.** The title moved to a right-aligned foot line. The sheet is now a cross: the hero/node/twin axis at x = 94 against the horizon at y = 102, with a heavy fan on the right and a light V/Z column on the left. The hero itself stays bilaterally symmetric, because a two-source field is. |
| W-pens | [craft] 6 pens / 5 swaps | **ARGUED.** The curator lifted the cap. Each swap is one clean layer with a stated meaning. |
| W-v5type | [craft] condensed small type | **FIXED.** Every label uses the shared proportional font at tracking ≥ 1.05, and nothing touches. |
| I1 | V to three rows, amp ≤ 0.45 × pitch | **ARGUED + FIXED on amp.** 4 rows, because the model has 4 tokens and Z is literally their sum. Amplitude is ≤ 0.45 × pitch. |
| I2 | ≥ 8 mm between Z/FFN row and backward row | **FIXED.** That row structure no longer exists. The Z and ∂Z rows are 20 mm apart, straddling the horizon. |
| I3 | bracket legs on pinch nodes, lift `FFN` | **N/A.** The bracket is cut. |
| Keep-v9type | keep v9's lowercase | **N/A.** No lowercase words remain on the sheet. |
| Keep-fan | forward dome vs backward twin peaks | **KEPT AND MADE REAL.** It is no longer a hand-set notch. See Measurements. |
| Keep-twin | the ∂L/∂A mini-interference at 0.39 | **KEPT AND PROMOTED** to one of the plate's only two figures. |
| Keep-axis | one strong horizontal | **KEPT.** The fan spine plus its dotted continuation make one horizon across the whole sheet. |

## What changed from parent

r01 was a reproduction of the reference, with 20 elements on a transformer-block layout. r03 throws that
layout away and builds the sheet from one rule:

1. **The horizon is the mirror.** The fan spine runs from the left node (Z / ∂L/∂Z) to the right node
   (Y, where the loss turns the pass around). A dotted black line continues it to the left margin.
   **Everything above it is the forward pass and everything below it is the backward pass.**
2. **The two interferences.** The hero (A) sits on top. Its twin (∂L/∂A) is placed by the **homothety of
   ratio −0.39 through the left node**: reflected across the horizon and shrunk. The Q/K register feeds
   the hero's sources from above, and the ∂L/∂Q, ∂L/∂K register feeds the twin's sources from below by
   the same homothety. A single dotted vertical runs hero → node → twin.
3. **One FFN fan.** The forward nonlinearity is above the spine and its derivative is below, on the same
   hidden units and the same spine. r01 drew two separate fans on two separate rows.
4. **The left column.** The four V rows, each already multiplied by its softmax weight, gather on one
   dotted bus into Z. The ∂L/∂Z row mirrors Z below the horizon.
5. **Cut:** stage names, bracket, fractions of the score, softmax row, both expand/project packets, all
   arrowheads, the 60 random scatter dots, the stipple caps, the far dotted ellipses, and the backward
   stack's return fans.

## Measurements / computations

**The model** (`_model`, all randomness from the passed SeededRNG). There are T = 4 tokens, d = 8,
and a single head. The FFN is d_ff = 12, tanh, W1 gain 2.2/√d, with a residual y = W2·tanh(W1 z + b1)
+ z, and the loss is L = ½‖y − t‖². The backward pass is written out exactly. Seed 9:

- attention a = [0.285, 0.322, 0.191, 0.201], scores s = [0.490, 0.613, 0.091, 0.142], attended key j* = 1, L = 6.678.
- h = [−1.29, −0.32, −0.01, −3.16, 3.19, 3.07, −1.12, 3.70, −2.94, −0.25, −2.58, −1.80], so 9 of 12 units have |h| > 0.9.
- **Finite-difference check** (central, ε = 1e−6), max abs error: ∂L/∂z **1.4e−9**, ∂L/∂q **6.0e−10**, ∂L/∂k* **1.2e−9**.

**Rows: the overlap IS the dot product.** Each row is one packet: Σ cᵢ·w(x)·cos 2π(F0 + i·DF)x with
F0 = 0.19 and DF = 0.045 cycles/mm, and a shared Gaussian envelope σ = 8.7 mm. The raw harmonics
overlap by 0.22 between neighbours under that envelope. My first version (v2–v10) ignored this, and its
row overlap only correlated 0.86 with q·k over the four keys. The final version draws c = G^(−1/2)·x
(Löwdin orthonormalisation of the Gram matrix), so ∫f_a f_b = a·b holds by construction:

- q·kⱼ for j = 0..3 is 1.3859 / 1.7325 / 0.2561 / 0.4005, and the numerical overlap integrals of the drawn curves are **identical to 4 d.p.**
- Over 300 random vector pairs, max |∫f_a f_b − a·b| = **2.0e−14**.
- **Z is the sum of the V rows as drawn:** max |f_Z − Σⱼ f_{aⱼvⱼ}| = **8.9e−16**. V and Z share one mm-per-unit (1.911).
- Scales, stated: Q|K 1.006 mm/unit, V|Z 1.911 mm/unit, and all gradient rows share 1.129 mm/unit. Grouping Q|K and V|Z separately (rather than one forward scale) was a v6 decision so that Z reaches 6 mm peak.

**The fan.** The ramp is s(u) = sin(πu)². Above the spine each unit's line is FAN_UP·tanh(|h_k|·s)/tanh(max|h|),
where FAN_UP = 30 mm. Below the spine it is |∂L/∂a_k|·s·sech²(h_k s), which is the exact d/dh_k of
the line above times the upstream gradient.

- The profile is exact. Per-unit height is **square-root compressed** (height ∝ √peak). Without that, the saturated units' twin peaks were 2 mm tall next to a 21 mm linear unit. This is the plate's one monotone-but-not-linear mapping.
- **Twin peaks are not drawn, they fall out of sech².** 9 of 12 units are twin-peaked (units 0, 3–8, 10, 11). Every unit with |h| > 0.77 is twin-peaked, and none of the others is.
- Mid-span forward heights (mm): 25.8, 9.4, 0.4, 29.9, 29.9, 29.9, 24.3, 30.0, 29.9, 7.2, 29.7, 28.4. Units 3, 4 and 5 are within 0.9 mm of each other everywhere, so they **merge into one line**. That is saturation made visible: three different inputs, one output. 12 units → 10 forward lines and 12 backward lines.
- Mid-span backward heights are 0.2–1.3 mm for the saturated units (the notch) and 14–23 mm for the linear ones.
- Anti-crowding uses the family's tangent-aware `_Guard` (0.8 mm, 25°), so crossings survive. A run under 9 mm is dropped rather than plotted as a stutter.

**The hero.** d = 66 mm = 54 L, so L = 1.222 mm. Crests run m = 1..43 per source, clipped to the lens
(0.872 d × 0.50 d) and emitted interleaved by m. The right source lags by φ = ∠(q, k*) = 82.5°. That is
real, but it is only 0.28 mm of ring radius and **does not read**. The twin has d = 25.7 mm = 21 L,
L = 1.226 mm, m = 1..17, and φ = ∠(∂q, ∂k*) = 84.7°.

**Crowding** (r01's metric: another stroke of the same pen within 0.8 mm and within 25° of parallel,
resampled at 0.25 mm): **3.0 % of the plate**, against r01's ≈ 34 %. By pen it is fan 1.2 %, hero/twin
1.9 %, and packet rows 4.5–7.3 % (where the carrier decays onto its own axis at the envelope tails).

**Geometry** (sheet mm): ink bbox is x 11.9–198.4, y 13.0–268.2 inside the 10–200 × 10–287 drawable,
with 0 bounds violations. `preview --score`: grade A, composition 0.952, readability 0.986.

## Plot budget

The model is Leo-safe: draw F600, pen-up travel F2000, `G4 P1.0` after every M3 and M5 (2 s per
cycle), and 2 min per pen swap. Measured on the final `.gcode`.

Stream order is the palette index, **light → dark**. Dark ink lands last, and the only cross-colour
contacts (drop-lines into nodes, the horizon into the violet node) are laid down by black over dry
lighter ink.

| # | pen | meaning | cycles (dots) | draw | travel | min |
|---|---|---|---|---|---|---|
| 0 | goldenrod | V rows (aⱼ·vⱼ) and their sum bus | 38 (25) | 0.41 m | 0.22 m | 2.1 |
| 1 | dodgerblue | K, ∂L/∂K and their projections | 53 (35) | 0.43 m | 0.54 m | 2.8 |
| 2 | forestgreen | Z = Σ aⱼvⱼ, ∂L/∂Z and their node links | 48 (34) | 0.44 m | 0.18 m | 2.4 |
| 3 | crimson | Q, ∂L/∂Q and their projections | 51 (36) | 0.46 m | 0.57 m | 2.8 |
| 4 | darkviolet | the FFN fan (tanh above, its derivative below), spine, Y/loss node | 39 (0) | 1.56 m | 0.40 m | 4.1 |
| 5 | black | hero A, twin ∂L/∂A, hero→node→twin axis, horizon, title | 376 (161) | 7.82 m | 1.26 m | 26.2 |
| | **total** | | **605 (290)** | **11.13 m** | **3.16 m (28 %)** | **40.3 + 12 swap = 52 min** |

On the same model, r01 v9 was 3,725 cycles, 12.07 m draw and 12.23 m travel, about 155 min. The
remaining cost is black: 183 crest-arc and source-disc strokes (hero and twin, split by the lens clip and
the guard), 32 title strokes and 161 dots. That layer is 26 min of the 52.

## Self-critique (rubric)

| dimension | score | why |
|---|---|---|
| Hierarchy | 7 | The hero is unmistakable at 3 m, the fan is a clear second and the twin a third. The four ochre rows are faint by truth (flat attention), so the V column is weak at 1 m. |
| Grid & alignment | 6 | Shared axes: x = 94 (hero/node/twin), the horizon, the left column x = 29 (V, Z, ∂Z, ∂Q), and the Q/K and ∂Q/∂K rows ending exactly on their sources' verticals. The right ends of K and ∂K (sheet x 173 / 159) answer nothing. |
| Tension | 6 | The cross plus a heavy right arm against a light left column. The hero itself is symmetric and sits 11 mm left of centre, which is weak. |
| Negative space | 6 | Quiet upper-right (x 140–200, y 150–225), lower-right and a ground band. They are shaped by the cross, but the ground band holds only the title and could read as leftover. |
| Craft for pen | 7 | Continuous 1 mm dots, no micro-dashes, 3 % crowding, 605 cycles. The fan still stops short of its nodes, with staggered ends where the guard cuts, and the hero's central seam shows as a 1.5 mm white slit where the families hand over. |
| Concept | 6 | "Above the horizon the pass, below it its image" lands. So does "the derivative is the reflection". The twin peaks and the fused flat top are real. It is still a labelled diagram: five ∂L/∂· fractions and node circles. |
| Depth | 5 | Declared flat. It is a plate diagram, and the only depth cue is the twin's 0.39 recession toward the horizon. |

**The single worst thing:** the backward half of the fan. It is twelve real derivative curves, nine
of them W-shaped, and they cross each other in the lower-left and lower-right shoulders. At 1 m that
reads as a knot rather than "twin peaks". The forward dome above it is calm and correct, and the
contrast is the point, but the knot is louder than intended.

## Engine requests

- `scripts/render_candidate.py --pen-width MM`, to pass `pen_widths` to `GCodeVisualizer.preview`.
  Juan's dot note says to judge at real nib width, and the hairline preview under-draws a 0.6 mm dot. I
  judged by cropping the preview and reasoning about the nib.
- A shared `kit.dotted(pts, pitch=1.0, r=0.12)` with end-anchored pitch and a single loop dot, so the
  family pitch lives in one place instead of being copied per round.
