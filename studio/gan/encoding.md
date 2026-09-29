# gan — encoding (VISUAL TRANSLATOR)   · Status: encoding v1 · 2026-09-29

Input: `DESCRIPTION.md`, `LEDGER.md`, `rounds/r04/{SYNTH,NOTES,critique-art,critique-science}.md`,
r03/r04 renders. No `dossier.md` exists, so the science truths, the check numbers (§4.1) and the
lies list (§9a) are recorded here. They were recomputed for this encoding with the r04 run
(h 0.26, r0 0.74, seed 7, a0 0.42622) and agree with sci r04. Round count restarts at **r05**
(5 designer rounds max on this encoding).

## Revision 1 — 2026-09-29

This replaces the implicit encoding of r03–r04 (their HANDOFF `rule:` lines): "a tape laid on paper
is the run; along a leg, a float = the summed move; the leader's thread is on top".

Why it had to change (rule 2: A1 and A7 each failed twice, and S2 pulls against A1):
- **S2 made the tape rubble (A1).** A float can equal a summed move only if the tape follows
  axis-aligned legs. Axis-aligned legs mean L-blocks and jogs.
- **Continuity needed filler that broke S2.** A continuous tape needed across/turn threads that
  carry nothing. Those fused with the exact floats, so S2 was true in the gcode and false on paper.
- **A tape on paper is a silhouette (A7).** With the flip removed, the image read the same.

The change is to the ORDER and the mapping, not the wording:
1. **Invert figure and ground (Red Meander proper).** The whole window is cloth. The run is not
   cut out of paper. It is the region where one thread floats on top, set in a balanced basket
   ground made of the same two threads.
2. **No float claims a length.** The quantities move to geometry: the ribbon's centre polygon
   corners are the iterates, its width is 0.2 × ρ, and the face is sign(ψθ).

What remains exact from r04: the run, the hole, the flow circle, the sign rule, the exit step,
and the title.

## 1. STYLE assignment

**BAUHAUS weaving workshop, declared flat.** Lineage: **Anni Albers, *Red Meander* (1954)**. It lends
this ORDER: a path that exists only as a change of structure in a continuous woven body. The linen
ground and the red meander are made of the same interlacing. Only which thread is on top differs.

Why this fits: the Dirac-GAN game already has a native weaving grammar.
- Two players become two thread families. G moves θ, so G is the weft (horizontal). D moves ψ, so
  D is the warp (vertical).
- At every state one player is ahead, which is sign(ψθ). "Ahead" becomes "on top".
- An order where the figure is on-top-ness itself is the only one where S2, A1 and A7 stop
  competing. Nothing has to be cut out, and nothing has to be measured along a float.

## 2. The one-glance statement

**A woven spiral that unwinds away from a hole nobody ever wove.**

- **At 3 m:** a panel of violet-grey cloth. A ribbon of saturated colour grows out of it. The
  ribbon turns crimson, then blue, then crimson, then blue, once per quarter-turn, and gets wider
  on every lap until the frame crops it. It starts at the rim of a bare paper disc that holds one
  black `+`.
- **At 1 m:** the ribbon is not outlined. It is where one family of threads runs unbroken while
  everywhere else the two families take turns in a checker.
- **At 30 cm:** the ribbon's edges have corners at every training step. The corners are long and
  far apart where G fools D, and close together where D spots the fake and the gradient dies.

## 3. The abstract ORDER

**INTERLACING — figure by float.** It is not a plot, and it is not a picture of a loom.

One-line mapping:
- **On the run:** the thread on top is the player who is winning at that state (sign ψθ).
- **Everywhere else:** neither thread is on top (a 2/2 basket).
- **The hole:** bare paper. The run can never come back closer than it started.

The spiral is not drawn. It is what you see when on-top stops alternating.

## 4. Channel mapping

Frame: 52 mm per world unit (r0 0.74 = 38.48 mm). Equilibrium θ = ψ = 0 at **(78, 113) mm**
(moved 4 mm down from r04; see §5). Weft x = θ, warp y = ψ. A4 portrait, drawable x 10–200,
y 10–287.

| quantity | channel | exact rule |
|---|---|---|
| state space (θ, ψ) | the cloth: one reed of warps (blue, vertical) and wefts (crimson, horizontal) at pitch **p = 2.6 mm** | lattice phase-locked **half a pitch** off the equilibrium, x_i = 78 + (i+½)p and y_j = 113 + (j+½)p. No thread lies on θ = 0 or ψ = 0, so every crossing has a non-zero sign. One pitch everywhere: tone never comes from spacing |
| the run (iterates z_k, k = 0…) | the **ribbon**: the chord polygon z_0 z_1 z_2 … scaled about the equilibrium by s ∈ [1−β, 1+β], **β = 0.10** | each step's cell is the quad {z_k(1−β), z_{k+1}(1−β), z_{k+1}(1+β), z_k(1+β)}. Neighbouring cells share their radial edge exactly, so the union is one seamless band from step 0 to the frame. A crossing is "in the ribbon" if it lies in any cell. Chords are straight because both players update at once (the step is the diagonal, not an L) |
| distance from equilibrium ρ | ribbon width = **0.2 ρ** (self-similar) | on every ray the ribbon spans [0.9 ρ, 1.1 ρ] of that lap's crossing radius ρ. Laps grow ≈1.51× per turn, so width does too. The basket channel between laps is ≈0.25 ρ (measured minimum 9.9 mm, lap 0→1 at 45°). Width claims ρ only. It is never keyed as speed or loss |
| who is winning at a state = sign(ψθ) | **which thread is on top at an in-ribbon crossing** | ψθ > 0: warp (D) over, "D SPOTS THE FAKE". ψθ < 0: weft (G) over, "G FOOLS D". Evaluated at the crossing's own (θ, ψ). The face flips exactly where the ribbon crosses an axis, as a seam of weave, not a drawn line |
| states the run does not pass | **2/2 basket** (hopsack) | warp over iff ⌊i/2⌋+⌊j/2⌋ is even. Each thread goes over 2, under 2, so exactly 50 % of crossings each way: "neither ahead". No diagonal, so no false direction |
| unreachable states (ρ < r0: the radius only grows) | **bare paper** | no crossing with r < 38.48 + 1.5 mm is woven |
| discreteness / step size | the ribbon's **corners**, at the radial lines through each z_k | corner spacing along the centre = step length: 1.25–31.5 mm in frame. Turn per step is 6.65° at step 0 and ≤ 13.7° in frame. Long straight facets where G fools D, smooth where D saturates. Nothing is added to mark steps |
| h → 0 gradient flow | black dashed circle, r = 38.48 mm, full 360°, through z_0 (a0 = 24.42°) | 2.5 mm dashes, starting at a0 |
| the Nash equilibrium (exists, repels) | one black `+` on bare paper, 3 passes, arms 7 mm | labelled `NASH EQUILIBRIUM  θ = ψ = 0` |
| float weight | **a run of ≥ 3 consecutive over-crossings is drawn out and back** (double pass, 0.4 mm apart). Runs of ≤ 2 are single pass | carries "on top without a break", the same channel as the face. It makes the ribbon heavier than the ground. The ribbon's line density is 0.77 /mm against the ground's 0.47 /mm, where the ground alone would otherwise out-ink the single-pass ribbon |

**How a thread is drawn (the one rendering rule).**
- Walk each thread across its crossings. A run of consecutive "over" crossings a…b is inked from
  half a pitch before a, plus g/2, to half a pitch after b, minus g/2.
- Everything else is hidden. The **under-gap g = 2.4 mm** leaves ≥ 1.9 mm of paper along the
  thread at the 0.5 mm tip, and clears a double-pass float by ≥ 0.5 mm of paper on each side.
- Resulting ink: basket dash 3p − g = **5.4 mm**, the shortest possible dash 2p − g = **2.8 mm**,
  ribbon floats as long as the ribbon's chord.
- In the ribbon the losing family is under at every crossing, so it is fully hidden there.
- Threads end at the window edge and at ρ = 39.98 mm (the hole).

Tufte check: every mark is a thread, a type glyph, the `+` or the flow circle. Every thread segment
carries one bit (over/under) at a real (θ, ψ).

### 4.1 Check numbers (no dossier.md exists)

These are the numbers the science critic checks against. They were recomputed 2026-09-29 and agree
with sci r04.

| quantity | value |
|---|---|
| model | Dirac-GAN, f(t) = −log(1+e^−t), f′(s) = σ(−s), simultaneous GDA: θ ← θ − hψf′(ψθ), ψ ← ψ + hθf′(ψθ) |
| h, r0, seed, a0 | 0.26, 0.74, 7, 0.42622 rad (24.42°). z_0 at (113.04, 128.91) with the new centre |
| equilibrium | θ = ψ = 0 exists. The flow Jacobian has eigenvalues ±0.5i (a centre) |
| discrete repulsion | \|λ\| = √(1 + h²f′²) = **1.00841 / step** at r → 0 |
| lap radius ratio | **1.51** (1.50–1.52 on all rays). Laps end at steps 50, 103, 181 (r 1.115, 1.688, 2.556) |
| crossing radii (mm) | 45°: 39.3 / 59.0 / 88.7 / 133.2 · 90°: 41.1 / 61.4 / 91.2 / 135.0 · 180°: 46.0 / 69.7 / 106.0 / 161.0 · 270°: 50.3 / 74.9 / 111.0 / 164.7 |
| first exit | **step 70, r 1.3287**, through the left edge at (9.4, 120.9) |
| in-frame iterates | ≈196 in window x 10–200, y 37.3–251.5 (sci r04 counted 211 in its window). Recount against the final window and print nothing that depends on the count |
| step length in frame, median by lap 0/1/2/3 | ψθ > 0 (D ahead): 5.1 / 5.9 / 4.9 / **1.5** mm. ψθ < 0 (G ahead): 6.7 / 11.7 / 19.4 / **28.0** mm. This is saturation: when D spots the fake, f′ → 0 and play crawls |
| hole | cloth starts at ρ ≥ 39.98 mm. Circle at 38.48 mm |

## 5. Composition sketch

A4 **portrait** 210 × 297 mm, margins 10 mm. Origin bottom-left, y up.

- **Window (the cloth, the dominant mass):** x 10–200, y **37.3–251.5** mm, 190 × 214 mm, about 70 %
  of the drawable sheet. That is more than 10:1 over the title block.
  - The cloth's straight cut edge IS the declared window (S8). No frame line is drawn.
  - Paper inside the window: only the hole.
- **Hole:** centre **(78, 113)**, bare disc r 38.48 mm (spans x 39.5–116.5, y 74.5–151.5). It is
  27 mm left of the page axis and low: the one shaped quiet zone. It keeps A2.
- **Crops (no grazes, measured):**
  - lap 1 is cut on the left (8.7 of 14.0 mm) and the bottom (6.8/15.0).
  - lap 2 is cut on the left, right (22.1/26.2) and bottom.
  - lap 3 is cut on all four sides; top 10.1 of 27.0.
  - lap 0 clears every edge by ≥ 17 mm. Lap 2 clears the top by 38 mm.
  - Rule: every lap either clears an edge by ≥ 6 mm or the edge cuts through ≥ ⅓ of its width.
  - This is why the centre moved from (78, 117) to (78, 113) and the window top from 260.2 to
    251.5. With r04's frame, lap 1 grazed the bottom (2.8 of 15 mm).
  - The exit stays step 70 at the left edge.
- **Type bands.**
  - **Title:** `THE FIXED POINT REPELS`, flush x = 10, set to end exactly on x = 200 (width 190 mm,
    cap ≈ 9.3 mm, A19). Cap-tops at y ≤ 284 (3 mm under the top margin, A19).
  - **Tagline:** `NEITHER PLAYER EVER ARRIVES`, spaced caps 2.4 mm, baseline y = 263.5. That leaves
    12.0 mm to the window top.
  - **Footer:** 4 lines, 1.7 mm caps, pitch 4.2, baselines y 11.0 / 15.2 / 19.4 / 23.6. The cap-line
    at 25.3 leaves a 12.0 mm gutter to the window.
  - Left column flush x = 10. Legend flush right on x = 200, on footer baselines 1–2.
- **Inside the hole (at most 2 label groups):**
  - the `+` with `NASH EQUILIBRIUM` / `θ = ψ = 0` centred on x = 78, just above and below it;
  - `h → 0: THE FLOW CIRCLES`, one line, 2 mm caps, inside the lower rim.
  - Nothing else.
- **Footer text** (no turn-taking words, no number the sheet does not show):
  1. `H 0.26 · STEP 0 ON THE CIRCLE R 0.74 · EACH LAP ABOUT 1.5 × WIDER` · legend `▬ WEFT  G  MOVES THETA`
  2. `STEP 70  R 1.33  LEAVES THE CLOTH` · legend `‖ WARP  D  MOVES PSI`
  3. `WARP ON TOP: D SPOTS THE FAKE (ψθ > 0) · WEFT ON TOP: G FOOLS D (ψθ < 0)` (S9)
  4. `BASKET: STATES THE RUN NEVER CROSSES · BARE PAPER: CLOSER THAN THE START · MIN G MAX D V(D,G)` (A19, the brief's annotation)

  Swatches are real samples: a 3-crossing crimson float and a 3-crossing blue float.

## 6. Pen budget: 3 pens, each a clean layer, plotted in this order

| order | pen | MEANING | carries | estimate |
|---|---|---|---|---|
| 1 | **dodgerblue** 0.5 mm | **D, the discriminator, moves ψ** (warp) | every warp: ribbon floats where ψθ > 0, basket dashes, legend swatch | ≈ 11.5 m draw, ≈ 850 pen-downs, **≈ 48 min** on Leo |
| 2 | **crimson** 0.5 mm | **G, the generator, moves θ** (weft) | every weft: ribbon floats where ψθ < 0, basket dashes, legend swatch | ≈ 10.5 m, ≈ 800 pen-downs, **≈ 45 min** |
| 3 | **black** 0.3–0.5 mm | **the fixed truths + text** | `+` (3 passes), h→0 dashed circle, hole labels, title, tagline, footer. Text is its own layer. It sits on bare paper only, so it needs no halos | ≈ 2.7 m, ≈ 400 pen-downs, **≈ 18 min** |

- **Order:** light to dark. Dodgerblue is lighter than crimson, and black lands last. Over/under is
  drawn as geometry (gaps), so layer order never decides what is on top.
- **Totals:** ≈ 25 m draw, ≈ 2,050 pen-downs, **≈ 1 h 55 min** on Leo (F600, G4 P1.0 dwells),
  2 swaps.
- **Ceilings (hard):** ≤ 2,300 pen-downs, commands < 15k, travel < draw, ≤ 2 h 10 min.
  If a ceiling is broken, raise p toward 2.8 mm (ribbon white 1.9 mm, still ≤ 2). Never drop the
  double pass or the basket.
- **Batching:** within each layer, threads go in reed order, boustrophedon (warp i bottom → top,
  warp i+1 top → bottom). No stroke crosses the sheet between batches. The longest single stroke is
  one float (≤ ≈ 45 mm), so any stroke can be a batch boundary.

## 7. Expressive levers (one decision each)

- **Proportion:** the cloth is more than 10:1 over the type. Ribbon to ground area is ≈ 1:1 (19.2k to
  18.2k mm²). The figure wins by weight (double pass) and saturation, not by area.
- **Fill / void:** the whole window is fill. The **only void is the hole**, and it is the loudest
  quiet zone the plate can have, because it is the only paper in 40,000 mm² of cloth. The paper
  between laps is gone on purpose. It was r04's rubble and residue.
- **Density gradient:** none by spacing (one reed). Weight is the only gradient: double-pass
  floats against single-pass basket. **A6, outward weight:** the ribbon width grows as 0.2 ρ, so
  each lap is 1.5× heavier than the last and the eye is carried outward to the crop.
- **Colour play / A5:** crimson and blue are the two players and stay co-equal (≈ 48/52 of cloth
  ink). The duel is symmetric, and making one player an "accent" would lie. The scarce, loud element
  is the hole with its **black `+`**. Black appears in the window ONLY as the `+`, the circle and
  two hole labels, so the eye's one landing point has its own pen role.
- **Texture direction:** set by the players. Blue face = vertical grain, crimson face = horizontal
  grain, basket = no grain. Grain direction flips with the face at every axis seam, so the
  quarter-turn rhythm reads even in greyscale.

## 8. The twist

The viewer already holds **the labyrinth / the whirlpool**: a spiral is a path to its centre.
Drains empty into it, a labyrinth's prize sits in it, "training converges" to it. Albers's
*Red Meander* is itself a maze path.

The mechanism breaks it: this spiral only leads OUT. Its centre is the one patch of the cloth that
was never woven. The title says it flatly (`THE FIXED POINT REPELS`). The tagline, `NEITHER PLAYER
EVER ARRIVES`, is the labyrinth read backwards.

## 9. Forbidden list

**Science lies (§4 of the dossier that does not exist, S6):**
- No "no equilibrium / there is no Nash point". It exists and it repels.
- No turn-taking vocabulary (answers / then / alternates / responds / takes turns). The updates
  are simultaneous. No L-shaped steps either.
- No float, dash or width keyed as a move, a loss or a speed. The only keyed channels are on-top,
  the hole, the circle, and the exit.
- No partial flow arc. The h→0 circle is complete and passes through step 0.
- No ink inside ρ < 39.98 mm except the `+`, its labels and the circle.
- No number printed that the sheet does not show.
- No "the cloth is the whole run": the window is declared.

**Visual failure modes:**
- **No paper channel, outline, selvedge line or colour change that bounds the ribbon (A7).** The
  ribbon exists only as face. Therefore **no grey or third pen for the ground**: the same two
  threads everywhere.
- No per-run L-blocks, axis-aligned step rectangles, jogs or orphan blocks (A1). The ribbon's edge
  is quantised only by the reed, ≤ one pitch.
- No plain 1/1 ground (it doubles the lifts). No twill (a false diagonal). No twill or basket
  reversal on the axes (it would draw crosshairs, A15).
- No iterate dots, ticks, ties or step numbers. The steps are the ribbon's corners.
- No arrows, crosshairs, axis lines, parameter stacks or legend boxes (A15).
- No ink-on-ink crossing, anywhere.
- No spacing-driven tone. One reed pitch for the whole window.
- No lap grazing the frame (§5 rule). No type inside the window except in the hole.
- No re-centring onto the page axis. No second label cluster in the hole.

## 10. Fabrication

- **Spacing:** the reed is 2.6 mm, above the 0.8 mm floor and 2.4× the finest nib.
  - Ribbon: double pass 0.4 mm apart, visible white between floats **1.7 mm** (A18 ≤ 2 mm).
  - Basket: dash 5.4 mm, gap 5.0 mm along the thread.
  - Under-gap 2.4 mm. Minimum inked segment 2.8 mm (≥ 2.5, A3).
- **Flood risks:**
  - The ribbon near step 0 is clipped by the hole to about half width (≈ 3.9 mm, 1–2 threads). That
    is acceptable, and the iterate is still on cloth.
  - The saturated NE crawl at the right edge (x 195–200, y 171–180; 63 in-frame steps < 3 mm) is
    smooth ribbon. There is no per-step mark there, so nothing to flood.
  - The black `+` has 3 passes on bare paper only.
- **Plot budget:** ≈ 25 m draw, ≈ 2,050 pen-downs, ≈ 1 h 55 min total, blue 48 / crimson 45 /
  black 18 min. Hard ceilings are in §6. The designer reports measured values from the gcode.
- **Determinism:** seed 7 → a0 0.42622 rad, as r04. Seeded only through `SeededRNG`. `.gcode` beside
  the render.
- **Engine requests already on file (r04):** kit weave primitive, crop hygiene, ψ glyph. This
  encoding needs only one more: `weave(crossing_rule)`, a per-crossing over/under lattice → gapped
  segments with a double pass for runs of ≥ 3 crossings. Build it in the piece if the kit lacks it.

## 11. Acceptance checks (pass/fail, on the png unless noted)

1. **A7, the flip test.** Inside the window there is no paper and no drawn line anywhere except
   the hole. The ribbon is visible only as a region where one family runs unbroken.
   - Pass if the critic can say: "set every crossing to the basket rule and the sheet becomes a
     uniform checker; the spiral and its crimson/blue quarters vanish."
   - Fail if any outline, paper channel, pen change or weight change bounds the ribbon other than
     float vs basket.
2. **A1 + A17 + A18, one body.**
   - Trace the ribbon from step 0 on the circle to each crop. It is never interrupted, and neither
     edge steps by more than one reed pitch (2.6 mm) anywhere.
   - Width on any ray = 0.2 ρ ± 2.6 mm.
   - The basket channel between adjacent laps is ≥ 9 mm at N/E/S/W, and channel ÷ ρ stays within
     0.22–0.28 all round.
   - Inside the ribbon, no white gap wider than 2 mm across the floats.
   - No cloth fragment under 6 mm that is not cut by the window edge.
3. **S2, no false float.** No text on the sheet equates any float, dash or width with a move.
   Science spot-checks on the gcode:
   - 10 ribbon corners lie on the radial lines through z_k within 0.1 mm (via the chord polygon);
   - the ribbon spans [0.9 ρ, 1.1 ρ] on 8 rays;
   - over/under = sign(ψθ) at 100 % of in-ribbon crossings;
   - basket over-share = 50 % ± 1 %;
   - every along-thread gap is ≥ 1.9 mm of visible paper.
4. **S8 + S3 + S1 + S9, truths on the sheet.**
   - Every in-frame iterate lies on the ribbon centreline, inside cloth (0 exceptions).
   - The footer lies entirely below y 37.3 and the window is the cloth's cut edge.
   - The caption says `STEP 70 R 1.33 LEAVES THE CLOTH`.
   - No thread at ρ < 39.98 mm.
   - The dashed circle is 360°, passes through z_0 and is labelled.
   - Exactly one black `+`, labelled `NASH EQUILIBRIUM θ = ψ = 0`.
   - The on-top key appears in words, as `D SPOTS THE FAKE` / `G FOOLS D`.
   - No turn-taking word anywhere.
5. **Hierarchy + accent (A5, A6).**
   - At 3 m the first read is the saturated ribbon alternating crimson/blue by quarter-turn,
     widening outward. The second read is the white hole with its `+`. The third is the title.
   - Inside the window, black appears only in the hole.
   - No lap grazes the frame: each clears an edge by ≥ 6 mm or is cut through ≥ ⅓ of its width.
6. **Plot (A3).** Measured from the gcode:
   - pen-downs ≤ 2,300;
   - commands < 15k;
   - travel < draw;
   - minimum inked segment ≥ 2.5 mm;
   - 0 ink-on-ink crossings;
   - 3 layers in the order blue → crimson → black, each with its minutes stated;
   - total Leo time ≤ 2 h 10 min.

## Revision 1.1 — 2026-09-29 (amendment, built in r07)

An amendment to rev 1, not a new encoding: the ORDER (figure by float in a 2/2 basket) is
unchanged. Only where the face is evaluated moves, the ribbon's behaviour at the rim, the
double-pass rule and the frame. Round count continues: r07 = round 2 of 5 on rev 1.

### The rules that change

1. **Per-step face (replaces §4 "evaluated at the crossing's own (θ, ψ)").** Ribbon cell k, the
   quad between the radial lines through z_k and z_{k+1}, is **warp-on-top iff ψ_kθ_k > 0**, weft-on-top
   otherwise. The move z_k → z_{k+1} is computed from f′(ψ_kθ_k), so the player who was winning AT
   THAT STEP owns the whole cell. A seam is where consecutive cells change owner: it lies on the
   radial line through the lap's **first post-axis iterate**, never on the axis itself (unless the
   iterate is closer than half a pitch to it, see below). Nothing is drawn to mark it.
2. **Rim shift, never clip (replaces §10 "clipped by the hole").** On every ray the ribbon spans
   **[lo, lo + 0.2 ρ]** with **lo = max(0.9 ρ, ρ_min)**, ρ the chord-polygon radius. ρ_min = r0 + 1.0 mm
   is the smallest crossing radius whose thread ink (0.25 mm half-width) keeps 0.5 mm of paper to the
   dashed circle's ink (0.25 mm half-width). The hole's bare disc is therefore ρ < r0 + 1.0 mm, and the
   ribbon keeps its full 0.2 ρ width from the rim outward.
3. **Double pass by membership (replaces §4 "run of ≥ 3 consecutive over-crossings").** A float is
   drawn out-and-back exactly over its ribbon crossings (± half a pitch), single pass over any ground
   crossings it also covers. 0 single-pass ribbon crossings, 0 double-pass ground crossings.
4. **Tie-downs only where a float would bridge a channel.** A ribbon float ends by going under at the
   next ground crossing only when the basket run beyond it would carry it onto the next lap's float.
   Basket phase (1, 1): warp over iff ⌊(i+1)/2⌋ + ⌊(j+1)/2⌋ is even, so no 2/2 block edge lies on
   θ = 0 or ψ = 0.
5. **Mid-pitch window + crop rule (replaces §5's "⅓ of the width").** The cloth's cut edges fall half
   way between two threads (x = x_eq + i·p). Every lap, on every edge, either **clears** it by ≥ 6 mm,
   or is **cut through** (its inner boundary crosses the edge too), or keeps **≥ 8.4 mm inside and loses
   ≥ 8.4 mm outside** (no graze, no sliver).
6. **§11.3 now reads:** over/under = **sign(ψ_kθ_k) of the owning cell** at 100 % of in-ribbon
   crossings. (Per crossing, sign(ψθ) at the crossing's own point agrees at 95.3 % only: the
   difference is exactly the seam offsets, which is the point of the amendment.)

### Corrected claims

- **§10 was false** ("step 0 clipped to half width, ≈ 3.9 mm, still on cloth"). Under rev 1 the
  ribbon at step 0 spanned [34.63, 42.33] mm with cloth only from 39.98: 2.35 mm, 0.84 pitch, and
  z_0 itself on bare paper. Under rev 1.1 it spans [38.81, 46.38] mm at 51.1 mm/unit (full 7.56 mm,
  2.7 pitches) and z_0 (ρ 37.81, on the dashed circle) has a double-pass ribbon crossing 2.63 mm away.
- **§11.4 now reads:** every in-frame iterate has an in-ribbon **double-pass** crossing within one
  reed pitch (2.8 mm). z_0…z_4 (ρ 37.81–38.80) lie on the 1.0 mm clearance ring between the dashed
  circle and the cloth edge, each with a double-pass ribbon crossing ≤ 2.75 mm away. The footer claim
  moved from "bare paper" to the circle: `INSIDE THE CIRCLE: CLOSER THAN THE START` is true of the
  dashed circle at r0 (no iterate ever has ρ < r0), and the clearance ring is not claimed.
- **Lap ratio is 1.48–1.52**, not 1.50–1.52: measured on the chord polygon along 8 rays,
  **1.482–1.524** (90° and 270° run 1.48–1.49; 0° and 180° reach 1.52). Lap ends: steps 50 / 103 /
  181, r 1.1207 / 1.6919 / 2.5563 (the rev-1 table's 1.115 was off by 0.006).

### What the per-step rule does to the seams (seed 7, a0 0.42622)

Offsets of each lap's first post-axis iterate from the axis, at 51.1 mm/unit:
N 0.32 / 0.82 / 6.04 / 15.77 mm (steps 10, 61, 121, 252) · E 3.44 / 3.25 / 14.65 (46, 98, 173) ·
S 6.29 / 4.38 / 8.29 (36, 89, 165) · W 0.45 / 1.88 / 1.41 (21, 71, 129).

The reed quantises a seam to the nearest half-pitch boundary. Where two laps' offsets fall in the
same half pitch, their seams share one straight line **by the data, not by drawing**:
- **N, laps 0 and 1** (0.32 and 0.82 mm, both inside the 1.4 mm half pitch): the seams of both laps sit
  on x = x_eq. A straightedge there touches 3 + 5 weft float ends (runs 3 and 5, split by a 2-row
  channel). This is the only straightedge failure.
- **E, laps 0 and 1** (3.44 and 3.25 mm, both between 1.4 and 4.2): both seams sit on y = y_eq + 2.8,
  off the axis (0 float ends on y = y_eq).
- W: 3 consecutive float ends on y = y_eq (pass, ≤ 3). S: 0.
Laps 2 and 3 break away (N 6.0 and 15.8 mm, E 14.7 mm), so the four quarter-seams lean into a
pinwheel. Separating laps 0 and 1 on N would need a reed finer than 0.5 mm, or a false offset.
(For reference only: seed 11, a0 0.5676, passes every axis straightedge but stacks three N seams
on x ≈ x_eq − 6 instead, and misses the S10 rim distance by 0.7 mm. The encoding keeps seed 7.)

### Check numbers at the final frame (r07, `pp_gan_iterate_v34`)

| quantity | value |
|---|---|
| scale, equilibrium | 51.1 mm/unit, (66.0, 100.0) mm, 39 mm left of the page axis |
| r0, ρ_min (cloth edge) | 37.81 mm, 38.81 mm |
| window (cut edges, mid-pitch) | x 10.0–197.6, y 38.4–254.0 (187.6 × 215.6 mm) |
| reed | p 2.8 mm, 67 warps × 77 wefts, 4,551 woven crossings |
| ribbon | 2,299 crossings; face = owning cell 2,299 / 2,299; double-pass 2,299 / 2,299 |
| ground | 2,252 crossings; warp over 1,125 = **49.96 %**; 0 double-pass; 6 ties, 3 rim flips |
| empty crossings | 0 (none with neither thread inked) |
| in-frame iterates | 527 (the window holds parts of 5 laps); max distance to a double-pass ribbon crossing 2.75 mm |
| first exit | **step 68, r 1.2936**, through the left edge at (6.21, 128.20) |
| crops (lap: L / R / B / T) | 0: clear 6.2 / 70.3 / 7.2 / 107.1 · 1: through / clear 38.6 / through / clear 87.6 · 2: through / cut 15.7 in + 10.0 out / through / clear 55.2 · 3: through ×3 / clear 8.0 · 4: through / through / clear / through |
| channel ÷ ρ, 8 rays | 0.234–0.272 everywhere except lap 0→1 at 45° (0.148, 5.7 mm) and 90° (0.183, 7.4 mm), where the rim shift pushes lap 0 outward (4.8 mm at z_0, 4.1 mm at 45°) |
| thread geometry | min thread ρ 38.81 mm; every along-thread gap 2.40 mm; min inked piece 2.59 mm; 0 ink-on-ink between pens |
| title | `THE FIXED POINT REPELS` 118.0 mm wide (cap 5.81 mm), x 10.0–128.0, cap-tops 284 |
| plot | 14,406 cmds · 2,024 pen-downs · draw 22.0 m · travel 11.2 m · blue 48 / crimson 43 / black 29 min ≈ 2 h 00 |
