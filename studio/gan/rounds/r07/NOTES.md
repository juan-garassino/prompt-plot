# gan r07 — iterate (encoding rev 1 + the rev 1.1 amendment) · parent: r05 · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/gan/rounds/r07/piece.py \
  --fn gan_meander_step --seed 7 --paper a4 --palette dodgerblue,crimson,black \
  --out gallery/studio/gan/current/pp_gan_iterate_v34.png
```
- final: `gallery/studio/gan/current/pp_gan_iterate_v34.png` + `gallery/studio/gan/current/pp_gan_iterate_v34.gcode` (seed 7, a0 0.42622)
- trials:
  - v25–v29: an earlier, interrupted pass at this round (per-step face, rim shift, membership double pass). It reached the frame (67, 118.5) @ 51.2 mm/unit with a 5-line footer. Lap 1 grazed the bottom (5.7 mm cut).
  - v30: re-crop to (66, 100) @ 51.1 and the 4-line footer.
  - v31: legend swatches (the r05 "T" hung into footer line 3).
  - v32: tie mode `bridge` (basket share 48.9 → 50.0 %).
  - v33_s11: seed 11, for comparison only (see A20).
  - v34: basket phase (1, 1), so the 2/2 block edges are off both axes.

## Mandate responses
| id | mandate | status |
|---|---|---|
| **A20** | kill the crosshair seams | **FIXED for laps 2–3 and for E/S/W. ARGUED for N laps 0–1.** The face is now the owning step's: cell k is warp-on-top iff ψ_kθ_k > 0 (2,299 / 2,299 ribbon crossings). Per-crossing sign agrees at only 2,190 (95.3 %). The difference is the seam offsets. Seam offsets from the axis at 51.1 mm/unit: N 0.32 / 0.82 / 6.04 / 15.77, E 3.44 / 3.25 / 14.65, S 6.29 / 4.38 / 8.29, W 0.45 / 1.88 / 1.41 mm. Straightedge results: y = y_eq E **0** float ends, x = x_eq S **0**, y = y_eq W **3** consecutive (pass). **x = x_eq N: 3 + 5 weft float ends** (y 140.6–146.2, then 154.6–165.8, split by a 2-row channel). Both laps' first post-axis iterates (z_10, z_61) fall inside the same half pitch (1.4 mm), so the reed puts both seams on one column boundary. No phase-locked reed ≥ 0.8 mm can separate 0.32 from 0.82. Moving the seam would be a fake offset, so I did not. The weaker check, "no single line carries two laps' seams", also FAILS for N laps 0–1 and for E laps 0–1: 3.44 and 3.25 mm both quantise to y = y_eq + 2.8. That line holds 4 + 6 warp float ends, off the axis. From lap 2 outward each quarter-seam breaks away (N x−6.0 then x−15.8, E y+14.7), so at 3 m the four seams lean into a pinwheel. Seed 11 (v33) passes every axis straightedge, but stacks three N seams on x ≈ x_eq−6, and its z_0 misses S10 by 0.7 mm. Seed 7 is kept |
| **S10** | the run starts visibly on the rim | **FIXED.** The ribbon is shifted, not clipped: [max(0.9ρ, ρ_min), +0.2ρ], ρ_min = r0 + 1.0 = 38.81 mm (0.5 mm of paper between thread ink and dash ink). At step 0 it spans 38.81–46.38 mm (full 7.56 mm). **527 / 527 in-frame iterates** have a double-pass ribbon crossing within 2.8 mm: max 2.75 (z_1). z_0 = (100.43, 115.63) is 2.63 mm from one. `STEP 0` is set at the rim beside z_0 (ink x 86.8–98.0, y 114.6), in the hole's 2nd label group with `h → 0: THE FLOW CIRCLES`. The hole has 2 groups. Footer line 3 now reads `INSIDE THE CIRCLE: CLOSER THAN THE START`: true, since ρ never drops below r0. The corrected §10 / §11.4 and lap ratio (measured 1.482–1.524) are in encoding.md § Revision 1.1 |
| **S11** | 100 % float weight, no holes, basket 50 ± 1 % | **FIXED.** Double pass by membership: **0** single-pass ribbon crossings, **0** double-pass ground crossings, **0** empty crossings (3 rim crossings flipped to the thread that can ink them). Ground over-share **1,125 / 2,252 = 49.96 %** over ALL ground crossings. Ties are now only at channel bridges (6, all to weft). The r05 tie rule skewed the share to 48.5–49.0 % at every phase. The top-right corner basket is correct: no special case |
| **A21** | crop through or clear, never ride an edge | **FIXED.** A full scan of scale × centre found (66, 100) @ 51.1 mm/unit. Window 10.0–197.6 × 38.4–254.0, edges at mid-pitch. Every lap on every edge either clears it by ≥ 6 mm (min: lap 0 L 6.2, B 7.2; lap 3 T 8.0), is cut through (inner boundary also past the edge), or keeps ≥ 8.4 mm inside AND loses ≥ 8.4 mm outside (lap 2 R: 15.7 in / 10.0 out). r05's lap-2 right sliver (4.1 mm) is gone, and there are no inner-boundary grazes. The outermost thread on every side is 1.4 mm from the cut edge by the mid-pitch law (test is "within 1.3 mm", so it passes). Longest pieces on those threads: L 28.4, R 50.8, B 39.6, T 6.0 mm. They belong to laps that the edge cuts through or cuts ≥ 8.4 mm deep, not to grazes |
| **A22** | demote the title | **FIXED.** `THE FIXED POINT REPELS` is 118.0 mm wide (x 10.0–128.0, cap 5.81 mm, one 0.3 mm weight), cap-tops at 284. The tagline shares x = 10.0. The top-right band x 130–200, y 256–287 is cream. At a 1/8 box downsample the title's mean ink over its own box is 59, against 32–44 for ribbon quarters. Its total weight (≈ 42k ink·mm²) is below a single ribbon quarter (NE lap 2 ≈ 115k). The hole is the only paper in the window. Flush edge note: x = 10.0 is ALSO the cloth's left cut edge, so title, tagline, footer and window share one line |
| A4 | shaped negative space | PARTIAL, by construction: the top-right cream and the hole are the two quiets. The ground is still a full-contrast basket (rev 1 forbids a third pen and spacing tone). If art scores ≤ 6 again, it goes to the translator as the ledger says |
| A5 | accent scarce | FIXED with A22: black in the window is only the `+`, the circle and the two hole label groups. The title is light |
| A6 | weight advances outward | FIXED with A20: width 0.2ρ (lap ratio ≈ 1.5), and the seams no longer stop the eye on one cross |
| S6 | dossier / encoding | PARTIAL: encoding.md § Revision 1.1 appended (rule, corrected §10 / §11.4, lap ratio, every check number at this frame). `dossier.md` still missing, deferred to the gate as ordered |
| A17 (watch) | channel ÷ ρ 0.22–0.28 after the re-scale | HOLDS 0.234–0.272 on 8 rays for every lap pair **except lap 0→1 at 45° (0.148, 5.7 mm) and 90° (0.183, 7.4 mm)**. ARGUED: that is the S10 rim shift pushing lap 0 outward by 4.1 mm at 45° (4.8 mm at z_0). The synth ordered full width from the rim, so the channel pays for it. It is still 2 basket columns wide, never zero |
| S1, S3, S4, S5 | truths | HOLD: `THE FIXED POINT REPELS` / `NEITHER PLAYER EVER ARRIVES`, one black `+` labelled `NASH EQUILIBRIUM` / `θ = ψ = 0`, 360° dashed circle at r0 with a dash starting at a0, no turn-taking words, `STEP 68  R 1.29  LEAVES THE CLOTH` (recomputed: step 68, r 1.2936, left edge at (6.21, 128.20)) |
| S2, S8, S9 | no false float; window declared; key in words | HOLD. The key is reworded to `WARP ON TOP: D SPOTS THE FAKE AT THAT STEP (ψθ > 0) · WEFT ON TOP: G FOOLS D AT THAT STEP (ψθ < 0)`. Footer cap-line 25.3, window from 38.4 |
| A1, A7, A18 | one body, flip test, cloth | HOLD. The ribbon is the same seamless chord-cell union. Per-step faces move WHERE the seams sit, not how the ribbon is made. No drawn edge, reed 2.8, 1.9 mm white between double floats |
| A2, A3, A13, A14, A19 | off-centre, plot craft, symmetric labels, flat, brief annotation | HOLD. The `+` is 39 mm left of the page axis and 48 mm below the window's middle. Plot figures are below. `MIN G MAX D V(D,G)` is flush right on footer line 3 |

## What changed from parent
- **Order: one face per step.** A ribbon cell takes the face of the step that computed it. The quarter seams leave the axes and lean. From lap 2 outward they spin clear of the `+`'s cross.
- **The run starts on the rim.** The ribbon is shifted, not clipped, so it has full width from z_0. `STEP 0` sits right beside z_0 inside the rim.
- **The composition moved.** The equilibrium went from (78, 113) to (66, 100) and the scale from 52 to 51.1 mm/unit. That is lower and further left than r05, so the spiral has more room to unwind up and right. The frame is the one found to crop every lap cleanly.
  - The window is 187.6 × 215.6 mm and its left edge IS the type's left edge.
  - Lap 3 now clears the top by 8 mm, which leaves a 3-row basket strip under the top cut. Lap 4 enters only the NE corner.
- **The title shrank** from 190 mm to 118 mm, one light weight. The cream band top-right is new.
- **Footer: 4 lines,** with the key on its own full-width line 4. The legend is a 2-crossing weft float on line 1 with a 2-crossing warp float centred on line 2.
- **Ties and basket.** Ties only at channel bridges. Basket phase (1, 1), so no basket block edge sits on θ = 0 or ψ = 0.

## Measurements / computations
All numbers come from `gan_meander_step.stats`, a gcode parser, and a scan script. Seed 7.

**The run**
- |λ| at r → 0 is 1.00841.
- Lap ends at steps 50 / 103 / 181 (r 1.1207 / 1.6919 / 2.5563).
- Lap ratio on the chord polygon, 8 rays: 1.482–1.524.
- Exit: step 68, r 1.2936, at (6.21, 128.20), left edge.

**Reed and ribbon**
- Reed: 67 × 77 threads, 4,551 woven crossings.
- Ribbon: 2,299 crossings.
  - Face = owning cell at 2,299 / 2,299.
  - Double-pass at 2,299 / 2,299.
- Ground: 2,252 crossings, warp-over 49.96 %.
- Ribbon span by ray (lo–hi mm, lap 0 → up):

  | ray | spans |
  |---|---|
  | 45° | 38.8–46.5 · 52.2–63.8 · 78.4–95.8 · 117.8–144.0 |
  | 90° | 38.8–46.9 · 54.3–66.3 · 80.5–98.4 · 119.4–145.9 |
  | 180° | 40.7–49.7 · 61.5–75.2 · 93.6–114.5 · 141.9–173.5 |
  | 270° | 44.5–54.3 · 66.1–80.8 · 98.0–119.7 · 145.5–177.8 |

**Rim (S10)**
- z_0…z_11 nearest double-pass ribbon crossing (mm): 2.63, 2.75, 1.88, 1.67, 1.91, 2.39, 0.47, 1.32, 1.00, 0.90, 1.10, 1.40.

**Crops (A21)**
- Scan: 11 scales (46–56 mm/unit) × centre x 56–85 × centre y 100–139 × 3 window tops.
- A graze-free frame requires every lap/edge pair to clear by ≥ 6, cut ≥ 8.4 in and ≥ 8.4 out, or pass through.
  - With "through" held to ≥ 8.4 mm of inner-boundary overshoot, no frame exists.
  - With ≥ 4 mm, a handful exist. (66, 100) @ 51 has the best margin.
  - 51.1 instead of 51.0 because at 51.0 z_1 was 2.82 mm from a double-pass crossing.

**Seams (A20)**
- See the mandate row.
- Per-crossing sign vs owning-cell face: 109 crossings differ. Those are the seams.

**Thread geometry**
- Min thread ρ 38.81 mm.
- Every along-thread gap 2.40 mm.
- Min inked thread piece 2.59 mm.

**Ink-on-ink (gcode, every segment pair of different pens)**
- 0 crossings or < 0.5 mm approaches.

**Type**
- Title 118.0 mm, cap 5.81 mm.
- Tagline baseline 271.0.
- Footer baselines 23.6 / 19.4 / 15.2 / 11.0; cap-line 25.3, 13.1 mm under the window.
- Legend swatches: weft 159.0–165.0 at y 24.5; warp x 162.0, y 17.2–23.2. Both clear lines 3 and 1 by 0.35 mm.

## Plot budget
Leo: F600 draw, G1 F2000 travel, 2.3 s per pen cycle.

| order | pen | strokes | draw | travel | est |
|---|---|---|---|---|---|
| 1 | dodgerblue (warp, D) | 700 | 11.25 m | 4.37 m | 48 min |
| 2 | crimson (weft, G) | 680 | 8.65 m | 4.49 m | 43 min |
| 3 | black (truths + type) | 644 | 2.11 m | 2.37 m | 29 min |

- Totals: **14,406 commands** (< 15k, 594 of headroom, r05 had 314), **2,024 pen-downs** (≤ 2,300), draw 22.0 m, travel 11.2 m < draw, **≈ 2 h 00** (≤ 2 h 10), 2 swaps.
- Batching: reed order, boustrophedon per layer. The longest stroke is one float, so any stroke is a safe batch boundary.
- Blue outweighs crimson (56/44). This window crops more of the D-ahead NE lap than r05 did.

## Self-critique
- **Hierarchy 7.** Ribbon first, hole second, title third. The title is now a thin line and no longer a bar. The top basket strip (lap 3 clears the top) is a little flat.
- **Grid 8.** One left edge (x 10.0) for title, tagline, window and footer. One right edge (197.6) for window, legend and brief. Footer on 4 shared baselines.
- **Tension 7.** The `+` sits low-left, and the spiral opens up-right into a cropped NE. The seams lean, but the N arm of laps 0–1 is still one short vertical (see worst thing).
- **Negative space 6.** The hole plus the top-right cream band. The basket is still full contrast (rev 1 law).
- **Craft 8.** 0 ink-on-ink, 0 empty crossings, 0 single-pass ribbon, one reed, no graze on any edge.
- **Concept 7.** "Starts at the rim, leaves the cloth" now reads: STEP 0 plus ribbon hugging the rim. Per-step face is the game's own truth.
- **Lineage 8.** Red Meander's order, unchanged.

**Single worst thing:** the N seam of laps 0 and 1 is one straight vertical on x = 66.2, 8 float ends from y 140 to 166, directly above the `+`. With the E pair on y = 102.8, it is the last trace of the crosshair. It is the data (both iterates lie within 0.82 mm of θ = 0), so it is argued, not hidden.

## Engine requests
- `kit.weave(face_fn, reed, window, gap, double="membership", ties="bridge")`: the per-crossing over/under lattice → gapped thread pieces with a membership double pass (built locally again).
- A crop-hygiene helper: `crop_report(bands, window)` → clear / cut / through per band and edge with the margins. Built locally as `stats['crops']` and the scan script.
- ψ glyph in `_GLYPHS` (still local).
