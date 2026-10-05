# Synth — lstm-spirals after r03 + r04 (parallel theses) · 2026-09-29
route: designer
next round: r05 · parent: r04 (best so far: art 7.00/6 · sci 6/5/6, against r03's 5.71/5 · 5/5/6; both FAIL). Take nothing visual from r03. Take one practice from it: its `check_plate.py` habit. Ship `rounds/r05/check_plate.py`, which reads every data channel back off the EMITTED gcode and prints designed vs drawn per letter.

Fabrication gate: not run, because neither critic passed. For the record, `plot layer --list` on r04 v18 gives: color 0 = 14 strokes, color 1 = 45 strokes, color 2 = 281 strokes, with bounds x 22–200, y 19.9–277 on a4 portrait. Nothing under `promptplot/` changed in these rounds.

Rule-2 watch: C2 (the saddle interleave) and A10 (the pen job) failed in both r03 and r04. The two rounds were parallel siblings, so the rule has not fired. **A third miss on either routes translator.**

## The instruction
Fork r04 and **turn the empty waist into the readout: h_t = o_t · tanh(c_t), drawn as 45 thin threads**. Each thread leaves its letter's half-turn on the red coil and ends at that letter's comet birth on the black lobe's rim. That brings back r01's interleaving sheaves, the one thing Juan's pick asked to keep, and this time every line in the sheaf is a measured coupling instead of a decorative flow.

Route each thread along the potential's orthogonal (σ) lines, so it crosses the coil at right angles and splits at the saddle the way the field does:
- threads for letters near the waist (T H E … / … R Y) pass through the saddle band;
- threads for flank letters climb around the outside of the red wraps, the black-side family down the left and the red-side up the right, as in r01.

Before drawing, do the arithmetic and write it in NOTES. The waist pinch today is about 17 mm at y≈128, and 45 threads at the 0.8 mm floor need about 36 mm across any cut. So either open the waist (eye separation or the lobe ratio, keeping both eyes on ONE vertical axis) or split the family between the waist and the two outer flanks, and state which you chose. The figure currently sits 11.7 mm from the left margin, so it may have to move right or shrink to give the left flank room.

The threads carry o_t: dash duty = mean o_t over the 8 cells, defined in the trace file. They are allowed to be a **4th pen with that one stated meaning**: the output gate, its own clean layer, the lightest ink, drawn light→dark before the comets. They must stay the quietest ink on the sheet so the red-bound 8 remains the dominant object. Every thread may cross red; none may run parallel to red or black closer than 0.8 mm.

## Mandates to close
1. **C2, the saddle interleave, c → h coupling** (curator/Juan; art r04 M1; science r03 S3 / r04 M3). Tests:
   - a crop of the waist shows marks that connect the lobes;
   - a finger on any letter, e.g. the M of MEMORY, follows ink to its own red half-turn;
   - `check_plate.py` reports thread k starts on half-turn k and ends ≤ 1.5 mm from comet k's birth, for all 45;
   - the red and black families are now linked. Today they stay ≥ 6.82 mm apart.
2. **A13 + S1, the pitch channel and a checkable trace.** Make the spiral constant-shape (direction-normalised), with gap = g0 + k·f̄_t (affine, g0 ≥ 0.8 mm, unclamped). Tests:
   - on the 0/90/180/270° rays, the per-turn gaps agree within 1.5× (today north 3.6–7.3 mm vs south 1.0–1.5 mm);
   - all 45 gaps are distinct (today 6 steps sit on the 0.9 floor: I .332, ' ' .366, Y .427, K .469, I .472, N .498);
   - there is no outward trend.

   Ship `rounds/r05/trace.json` with the sequence and per-step i, f, o (per cell and mean), c, h, RMS(h), f̄, and the written definitions of carry_t and every mapped quantity.
3. **S4 + S6, true count and the retention horizon.** The red line makes exactly 45 half-turns, or the caption says what is actually drawn (today 39.07 half-turns against the caption's "HALF A TURN PER LETTER"). Key coils to letters: a tick per half-turn, or first/last-letter marks at the lobe start, the lobe/wrap boundary and the end. Print what the 12-letter wrap means. The model's best cell keeps < 10 % of a write after at most 12 steps (median 9), so that is the horizon, and "sediment" must not claim more retention than that.
4. **S5, every comet shows its RMS(h_t).** Today 41/45 are cut at 1.00 mm and the visible sweep correlates with RMS at −0.11. Keep the newest-cuts-oldest overwrite, which is the wit, and put the true value on the sheet anyway: a tick or end-dot at the RMS angle, or a dotted continuation past the cut. The tick can be where the o_t thread lands. Test: `check_plate.py` reads RMS for all 45 within 5 %.
5. **A10 + A12, the Leo pen job, measured on the EMITTED gcode after `reorder_by_color`.**
   - Red: inter-chunk travel = 0 mm, streamed in chain order, seams only on the open north side of the well, never inside a tight band. Measure the emitted order; do not trust the authored order.
   - Black comets: spatially ordered, travel ≤ 400 mm, no consecutive hop > 50 mm.
   - The new thread layer: no hop > 60 mm.
   - Each pen is one clean layer with one swap, never re-entered.
   - HANDOFF carries a table of draw mm, travel mm, pen cycles and minutes per layer and in total.
   - Pin the colophon to a named line: flush-left at the outer wrap's right extreme, or baseline on the waist centre.

Deferred:
- A2 (static stack), constrained by C1. The readout sheaf is expected to supply the diagonal energy.
- A14 (spine title weight) and A15 (proverb tracking): re-judge after the waist changes.
- S7 (`encoding.md`): r05 NOTES carries the check-number table. The translator writes `encoding.md` if rule 2 fires.

Argued/dropped: A11 (lean the axis ≥ 10°). It contradicts the curator's Keep of one vertical axis.

## Preserve
- **Both eyes on one vertical axis**, black h_t above (lobe c_b 1.3) and red c_t below (c_r 1.0). This is the curator's Keep (C1), r04 at x≈78.4.
- **The pun that lands**: ONE unbroken red line (c_t) against many short black strokes (h_t) beside `LONG SHORT-TERM MEMORY`. Red stays one geometric chain.
- **The proverb as the input** set round the black lobe's rim, each comet born 1.2 mm from its letter. Art calls this stronger than r01's six anonymous dots.
- **The real model**: the 8-cell char LSTM, `lstm_weights.json`, forward pass at render time. It reproduces loss 0.0754 and acc 1.0, and seeds 3/7/11 give byte-identical gcode.
- **"Never a turn"**: max comet sweep 0.77 turn, because tanh < 1.
- **The spine title's lock**: its inked length equals the red line's y-extent (20.6–276.7), right edge on the margin at x≈199.4.
- **Bare eyes** (no axis ticks inside either eye), zero non-type crumbs < 2 mm, label clearance ≥ 1.2 mm, red ≥ 1.04 mm self-spacing.
- **No furniture**: no equations, legend, arrows, leaders, t-labels or plus marks (C3).
- **Lineage**: Smithson, *Spiral Jetty* / *A Sedimentation of the Mind*: one continuous coil whose walk is time. **Declared flat**.

## Do not
- Do not lean or split the axis to buy tension. Juan's Keep wins over the critic's lean.
- Do not fill the waist with a decorative sheaf. Every thread is one letter's h = o·tanh(c), traceable in `check_plate.py`, or it is not drawn.
- Do not let 45 threads stack under 0.8 mm at the saddle. Do the capacity arithmetic first and widen the waist or split the family.
- Do not add a pen without a stated meaning. The 4th pen is o_t and nothing else, and it must not be re-entered after its layer.
- Do not trust authored stroke order. The pipeline's greedy nearest-neighbour re-scrambled r04's red chunks (13, 9, 10, …). Make the geometry NN-friendly and measure the emitted gcode.
- Do not let the well's shape carry a signal the caption attributes to the forget gate. Do not clamp the strongest forgets to a floor.
- Do not print a count the sheet does not draw ("half a turn per letter" at 39 half-turns).
- Do not ship HANDOFF without `canon:` (r04 NOTES said Swiss; HANDOFF omitted it), `declared: flat` and `lineage:` lines.
