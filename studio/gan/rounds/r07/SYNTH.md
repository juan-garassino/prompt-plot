# Synth — gan after r07 · 2026-09-29
route: designer
next round: r08 · parent: **r07** (best so far AND latest: art 7.57/7 · sci 9/8/8 PASS, `gallery/studio/gan/current/pp_gan_iterate_v34.png`)

**r07 is the new best.**
- Science PASSES (9/8/8).
- Art FAILS only on its average (7.57, min 7).
- It beats r05 on verdict, art min, sci min and art avg.

**The relaunch ends at r08.** The curator granted batch 1 two more rounds, r07 and r08, so r08 is the **last round** before `vote`. It is also round 3 of 5 on encoding rev 1, with its amendments 1.1 and 1.2. Make it a finishing round: one idea, no new thesis.

## The instruction
Give the spiral's **first turn** its air back and give the **hole** back to the `+`. r07 fixed where the run starts, but it did so by pushing lap 0 outward into lap 1. Above-right of the hole the first two turns now fuse into one blue wedge, crossed by a straight seam that points at the `+`. The hole beneath them is spent on type. Fix that one region as a composition, in three moves.

**1. Rebuild lap 0 as a ribbon that grows out of the rim** (rev 1.2).
- Span: `[max(0.9ρ, ρ_min), max(1.1ρ, ρ_min + w_floor)]`, with w_floor ≥ 1.5 pitch (4.2 mm).
- The outer edge stays on the true chord polygon; only the inner edge is pinned at the rim.
- From ρ ≈ ρ_min/0.9 outward it is the normal [0.9ρ, 1.1ρ] ribbon, so every later lap is unchanged.
- The channel between laps 0 and 1 returns to ≥ 3 clear basket crossings.
- The lead decided this trade, so it is not traded silently. The critic's S10 test is the 2.8 mm test, which the tapered start still passes. "Full 0.2ρ from the rim" was my r06 means, not the mandate.
- Clip every thread pass, ±0.2 mm offsets included, at ρ_min. No ink may sit inside r0 + 1.0 mm.

**2. Search a0 (the seed) for a start that breaks the N and W seam stacks.**
- Requirement: no two laps' first post-axis iterates quantise into the same half pitch on any of the four axis half-lines.
- Every hard check must still hold at the chosen a0: S10, the A21 crop scan and the new channel.
- Put the search table in NOTES.
- Re-crop if the a0 moves the laps.
- Recompute and print only what is then true: the exit step and r, z_0, and `STEP 0`'s position.

**3. Re-set the hole.**
- `NASH EQUILIBRIUM` / `θ = ψ = 0` becomes one tight pair under the `+`.
- `h → 0: THE FLOW CIRCLES` goes back inside the lower rim.
- `STEP 0` stays alone at z_0.
- The upper-right of the disc is empty paper.

**Write it down.** Append `## Revision 1.2` to `encoding.md`, and write `dossier.md`: the vote needs it.

## Mandates to close
1. **A17 (regressed): reopen the lap 0→1 channel.**
   - ≥ 3 clear basket crossings (≥ 8.4 mm) between lap 0's double-pass outer edge and lap 1's inner edge on the 45° and 90° rays. Look at x 85–125, y 135–175 in r07's frame.
   - No float tail through the channel.
   - Channel ÷ ρ 0.22–0.28 on all 8 rays.
   - S10 must still hold: every in-frame iterate has a double-pass ribbon crossing within 2.8 mm (r07: 527/527, max 2.747).
   - Use the lap-0 rule above. If the taper plus the 2.8 mm test cannot both hold for some iterate, report which step and by how much. Do not widen the channel by thinning later laps.
2. **A20 (PARTIAL): no axis straightedge carries two laps' seams.**
   - On each of N (x = x_eq, above), S, E and W (y = y_eq), a straightedge touches ≤ 3 consecutive float ends, **counting all laps combined**.
   - r07 fails N (3 + 5, laps 0 and 1) and science flags W (laps 0 and 2 on y = 100).
   - Fix it only by the data (a0 search). The reed stays half a pitch off the equilibrium. Scale cannot help, because the offsets scale with it.
   - If no a0 passes all the hard checks, keep the a0 with the fewest stacked float ends, print the table, and argue it. The lead records it honestly at the vote. Never fake a seam offset.
3. **A23 (new): the hole goes back to the `+`.**
   - `h → 0: THE FLOW CIRCLES` sits centred on x_eq, baseline ≈ 6 mm above the circle's bottom.
   - `NASH EQUILIBRIUM` / `θ = ψ = 0` is one tight pair under the `+`.
   - `STEP 0` stays beside z_0. No other label is within 8 mm of the rim at z_0's angle.
   - Test: at a 1/8 downsample the `+` is the darkest mark in the disc, and the upper-right quadrant of the disc is paper.
   - Also: the footer's flush-right edge (legend, `MIN G MAX D V(D,G)`, key line end) moves onto the cloth's right cut edge, so the page has one right edge.
4. **S12 (new): rim ink clearance ≥ 0.5 mm, measured on the gcode.**
   - r07's offset passes reach ρ 38.62: the blue warp at x 100.8 ending at y 116.78, and the crimson weft at y 137.6, x 37.8–57.2. That is 0.31 mm of paper to the dashes.
   - Required: every inked segment, any pen other than black, has ρ ≥ r0 + 1.0 mm.
   - Print the measured minimum.
5. **S6: dossier and encoding hygiene.** This is required for the vote, so do all four:
   - write `studio/gan/dossier.md`: the model and update equations, the Mescheder sign semantics, |λ|, lap ends and ratio, exit, seam offsets, and the membership/face/basket counts, each with how it was computed;
   - mark encoding §4, §4.1 and §5's rev-1 frame numbers `SUPERSEDED`;
   - strike §2's "at 30 cm" step-size claim and the §4 "discreteness / step size" row: the corner sagitta is 0.88 mm, below the 2.8 mm reed;
   - append `## Revision 1.2` with the lap-0 rule, the S12 clip, the final a0 and every check number at the r08 frame.

Deferred:
- **A4** (7, improving). A23 returns the disc to paper.
- **A5** and **A6.** They close through A23, A17 and A20.
- **Saturation channel** (sci Advisory 2). A rev 2 question for a later batch. Do not attempt it now.

## Preserve
Everything science PASSED in r07 must still PASS in r08.

**The run, and its faces:**
- simultaneous GDA, h 0.26, r0 0.74;
- per-step face: ribbon cell k is warp-on-top iff ψ_kθ_k > 0, at 100 % (r07 2,299/2,299).

**The cloth:**
- double pass by membership at 100 %;
- 0 double-pass ground crossings;
- 0 empty crossings outside the hole;
- basket 50 % ± 1 % over all ground crossings (r07 49.96 %), ties only at channel bridges, basket phase off both axes;
- one reed at 2.8 mm, half a pitch off the equilibrium;
- under-gap 2.4 mm, min inked piece ≥ 2.5 mm;
- 0 ink-on-ink between pens.

**Art:**
- **A7 flip test PASS:** no outline, channel line or pen change bounds the ribbon.
- **A1:** one seamless ribbon per lap from the rim to the crops, edges quantised only by the reed.
- **E, S and W seams lean outward** from lap 2 (the pinwheel). A new a0 must keep that lean.

**The start (S10):**
- `STEP 0` at the rim beside z_0 (r07: ink ends 2.4 mm from z_0);
- `INSIDE THE CIRCLE: CLOSER THAN THE START` (true, since r is monotone).

**The crops (A21):**
- window edges at mid-pitch;
- every lap on every edge clears it by ≥ 6 mm, or is cut ≥ 8.4 mm in and out, or passes through;
- re-run the full crop scan after the a0 change, and do better than r07's 6.2 mm left clearance if the scan allows.

**The page:**
- **Title band (A22):** `THE FIXED POINT REPELS` 118 mm, one light weight, flush left at the cloth's left edge; the tagline on the same edge; top-right cream band empty.
- **Truths:**
  - one black `+`;
  - a 360° dashed h→0 circle at r0, with a dash at a0;
  - `STEP N R x LEAVES THE CLOTH`, recomputed;
  - the key in words (`AT THAT STEP`);
  - no turn-taking words.
- **Footer:** 4 lines on shared baselines under the window, with the weft/warp legend drawn as real floats.

**Plot (curator law):**
- no pen cap, one clean layer per meaningful pen;
- stated order **0 dodgerblue (D, warp) → 1 crimson (G, weft) → 2 black (truths + type)**;
- boustrophedon reed order, so any float is a batch boundary;
- minutes per layer in HANDOFF;
- ceilings: < 15k cmds (r07 14,406), ≤ 2,300 pen-downs (2,024), travel < draw, ≤ 2 h 10 (≈ 2 h 00).

## Do not
- Do not evaluate the face per crossing, and do not fake a seam offset (no nudged float ends, no reed phase change, no rotated reed).
- Do not buy the channel by thinning laps 1–3, by moving lap 1 outward, or by shrinking the hole margin below r0 + 1.0 mm ink.
- Do not reinstate "full 0.2ρ from the rim". Lap 0 grows out of the rim by the rev 1.2 rule.
- Do not claim `EACH LAP ABOUT 1.5 × WIDER` unless it is re-measured at r08 on rays past the lap-0 taper. Print the range.
- Do not print any r07 number (step 68, r 1.29, z_0, 527 iterates) if the new a0 changes it.
- Do not add any drawn seam, tick, dot, arrow, third thread colour, grey ground, spacing tone or twill.
- Do not put anything in the top-right cream or the upper-right of the disc.
- Do not import anything from r06 (`boogie`).
- Do not start a new thesis. r08 is the relaunch's last round, and its output goes to Juan's vote.

## Gate
Not run as a pass gate: art FAILs, so rule 1 did not fire. Layer sanity on r07's gcode is clean:

| layer | pen | strokes | commands | est |
|---|---|---|---|---|
| 0 | dodgerblue | 700 | 4,778 | 48 min |
| 1 | crimson | 680 | 4,462 | 43 min |
| 2 | black | 644 | 5,166 | 29 min |

- Order matches the stated order.
- Bounds X 0–197.6, Y 0–284. The 0 is the home/park travel.
- 14,406 cmds, draw 22.0 m, travel 11.3 m.
- Package code: only `promptplot/generative/DESIGN_RUBRIC.md` (docs) is modified under `promptplot/`, so no regression run is required.

**At the r08 gate** (run after the r08 critiques regardless of verdict, because r08 goes to vote):
- `preview --stats --score` and `plot layer --list`;
- the S12 ρ_min on the gcode;
- a crop of the densest zone, the NE rim at the lap 0/1 channel, to confirm no flood;
- `dossier.md` present.
