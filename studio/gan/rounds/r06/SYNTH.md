# Synth — gan after r05 ∥ r06 · 2026-09-29
route: designer
next round: r07 · parent: **r05** (best so far: art 7.14/6 · sci 9/8/7, `gallery/studio/gan/trials/pp_gan_iterate_v24.png`)

r05 and r06 were parallel theses: the encoding rev 1 refinement against the De Stijl wildcard.
- **r05 wins.** It has the higher art avg (7.14 vs 6.57) and higher sci truth and fidelity (9/8 vs 8/7), with the mins tied at 6 and 7.
- **No merge.** r06's lane geometry cannot sit on rev 1's cloth. Its one transferable idea, naming the start at the rim, is already S10.
- r06 stays on disk as the `boogie` flavour. Its mandates are parked in the ledger.

Encoding count: r07 is round **2 of 5** on encoding rev 1, built with the **rev 1.1 amendment** below. The order is still figure-by-float in a 2/2 basket; only the point where the face is evaluated moves, plus the ribbon's behaviour at the rim.

## The instruction
Give the r05 cloth one change of order: **each ribbon cell takes the face of the step that owns it**.

**The face rule.**
- Cell k (between z_k and z_{k+1}) is warp-on-top iff ψ_kθ_k > 0. It is not evaluated per crossing.
- This is the discrete game's own truth: the move z_k → z_{k+1} is computed from f′(ψ_kθ_k).

**What it does to the seams.**
- Each lap's colour change moves off the axes onto the ray through its first post-axis iterate. The four straight x = 78 / y = 113 seams become a leaning pinwheel of short seams.
- The lead's computation at 52 mm/unit, (78, 113), gives these seam offsets from the axis:
  - N: 0.3 / 0.8 / 6.1 / 16.0 mm (steps 10, 61, 121, 252);
  - E: 3.5 / 3.3 / 14.9;
  - S: 6.4 / 4.5 / 8.4;
  - W: 0.5 / 1.9 / 1.4, mostly cropped.

**Then re-crop so no lap slivers against an edge.**
- You may move the centre and the scale, keeping the `+` ≥ 20 mm off the page axis.
- Recompute and print only what is then true, including the exit step and radius.

**Shift the ribbon at the rim, don't clip it.**
- It keeps its full 0.2ρ width from the rim outward, so the run visibly starts at z_0.
- Mark `STEP 0` at the rim.

**Shrink the title** to ≤ 120 mm, flush left, so the top-right becomes cream.

**Write down what changed.**
- Append a `## Revision 1.1` section to `encoding.md`:
  - the per-step face rule;
  - the shifted rim ribbon;
  - the corrected §10 / §11.4 claims;
  - lap ratio 1.48–1.52;
  - every check number at your final centre and scale.
- Replace §11.3's "sign(ψθ) at 100 % of crossings" with "sign(ψ_kθ_k) of the owning cell at 100 %".

## Mandates to close
1. **A20: kill the crosshair seams** (per-step face).
   - Critic's test: a straightedge on x = 78 or y = 113 (either half) touches ≤ 3 consecutive float ends of one seam.
   - The data puts the N-side seams of laps 0–1 within 1 mm of x = 78. If they are the only failures, report their row counts and offsets, and argue them in NOTES against the weaker check: "no single straight line carries the seams of two laps". Do not fake an offset. The art critic judges.
   - Reword S9 to match: `WARP ON TOP: D SPOTS THE FAKE AT THAT STEP (ψθ > 0) · WEFT ON TOP: G FOOLS D AT THAT STEP (ψθ < 0)`.
2. **S10: the run starts visibly on the rim.**
   - The ribbon spans [max(0.9ρ, ρ_min), that + 0.2ρ]. ρ_min is the smallest crossing radius whose thread ink keeps ≥ 0.5 mm of paper to the dashed circle's ink.
   - Every in-frame iterate k has an in-ribbon double-pass crossing within 2.8 mm (r05: steps 0–9 fail).
   - Put `STEP 0` beside z_0, as part of the hole's 2nd label group (≤ 2 groups).
   - The footer's bare-paper line becomes true of the drawn disc, e.g. `INSIDE THE CIRCLE: CLOSER THAN THE START`.
3. **S11: 100 % float weight, no holes.**
   - Double pass by ribbon membership, not "≥ 3 consecutive". Result: 0 single-pass in-ribbon crossings and 0 double-pass ground crossings.
   - 0 crossings with neither thread inked. r05 had 5: (101.8, 80.8), (37.4, 108.8), (37.4, 111.6), (199.8, 47.2), (199.8, 195.6).
   - The top-right corner basket is correct.
   - Basket over-share is 50 % ± 1 % over ALL ground crossings (r05: 48.6 %). If the tie-downs skew it, alternate them warp/weft.
4. **A21: crop through or clear, never ride an edge.**
   - Window edges fall at mid-pitch between threads (x = x_eq + i·p).
   - Every lap either clears each edge by ≥ 6 mm or keeps ≥ 8.4 mm (3 pitches) visible past the cut. r05's lap-2 right sliver was 4.1 mm.
   - No float within 1.3 mm of a window edge for more than 20 mm.
   - Channel ÷ ρ holds 0.22–0.28 after the re-scale (A17 watch).
5. **A22: demote the title** (A5 residual, A4 lever).
   - `THE FIXED POINT REPELS` ≤ 120 mm wide, flush left at x = 10. The tagline shares that left edge.
   - Test: at a 1/8 downsample the ribbon quarters and the hole both out-weigh the title.

Deferred:
- **A4** (quiet ground). If art r07 still scores negative space ≤ 6 after A22, the loud basket goes to the translator as a rev 2 question: rev 1 forbids a third pen and spacing tone.
- **A6.** It closes with A20.
- **S6 `dossier.md`.** It is needed at the gate, or it gets an explicit waiver.

## Preserve
- **The A7 flip test (art r05 PASS).** No outline, channel, pen change or drawn line bounds the ribbon. The figure is float against basket only. Per-step faces change WHERE a seam is, never HOW the ribbon is made.
- **A1:** one seamless chord-cell ribbon from the rim to the crops, with edges quantised only by the reed.
- **The cloth itself:**
  - one reed at 2.8 mm, phase-locked half a pitch off the equilibrium;
  - under-gap 2.4 mm (1.9 mm of paper);
  - ≤ 2 mm white between double-pass floats (A18);
  - 0 ink-on-ink.
- **The hole:**
  - bare paper;
  - black `+` labelled `NASH EQUILIBRIUM` / `θ = ψ = 0`;
  - a 360° dashed h→0 circle at r0, phased at a0, labelled.
- **Truths that must hold (S1, S3, S4, S5):** `THE FIXED POINT REPELS` / `NEITHER PLAYER EVER ARRIVES`, and no turn-taking words.
- **Type bands and gutters:**
  - footer 4 lines below the window;
  - 12 mm gutters;
  - `MIN G MAX D V(D,G)` flush right;
  - `WEFT G MOVES θ` / `WARP D MOVES ψ` swatches as real floats.
- **Plot (curator law, holds in r05):**
  - no pen cap, one clean layer per meaningful pen;
  - stated order **0 dodgerblue (D, warp) → 1 crimson (G, weft) → 2 black (truths + type)**. The r05 gate `--list` gives 743 / 712 / 655 strokes;
  - boustrophedon reed order, so any float is a batch boundary;
  - minutes per layer in HANDOFF;
  - ceilings: < 15k commands, ≤ 2,300 pen-downs, travel < draw, ≤ 2 h 10. r05 sits at 14,686 commands, so buy headroom from the shorter title, not from the cloth.

## Do not
- Do not evaluate the face per crossing anywhere in the ribbon. Do not add any drawn seam, tick or colour edge to "show" the step: the seam is only where the face flips.
- Do not rotate the reed against the page. A rotated cross is still a cross, and it breaks `WEFT G MOVES θ`.
- Do not clip the ribbon to a sliver at the hole. Do not shrink the hole margin until thread ink touches the circle's dashes.
- Do not print r05's `STEP 70 R 1.33` if the re-crop changes the exit. Recompute it.
- Do not lose the top-right cream to a relocated legend or tagline.
- No third thread colour or grey ground. No spacing-driven tone. No twill. No iterate dots.
- Do not import anything from r06 (lanes, lattice type, gold, the square). It is a separate flavour.

## Gate
Not run: both critics FAIL, so rule 1 did not fire. Layer sanity on r05's gcode (`plot layer --list`) is clean: 3 layers in the stated order, 4,744 / 4,530 / 5,412 commands. Nothing under `promptplot/` changed in this piece's rounds, so no regression run is required.
