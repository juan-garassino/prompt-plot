# gan r04 — iterate · parent: r03 (MERGE: r02's full h→0 circle) · 2026-09-28

## Render
```
.venv/bin/python scripts/render_candidate.py studio/gan/rounds/r04/piece.py \
  --fn gan_repels --seed 7 --paper a4 --palette black,crimson,dodgerblue \
  --out ~/Downloads/pp_gan_iterate_v16.png
```
- final PNG: `~/Downloads/pp_gan_iterate_v16.png`
- final GCODE: `~/Downloads/pp_gan_iterate_v16.gcode`
- seed 7, A4 portrait, cream (preview on white). Seeds 3 and 11 (`pp_gan_iterate_v8_s3/_s11`) change the
  start angle by < 0.1 rad and give the same composition. Seed 7 is the mandated run.
- self-rounds v1 → v16. v1–v2: exact tapes only, each leg's own family. The ribbon broke into single-family
  hatch fragments with no weave (rejected). v3: along/across/turn tapes, so both families everywhere and a
  real woven ribbon. v4: selvedge hairpins, which read as outlined boxes (dropped). v5–v6: serpentine
  line direction (travel falls below draw) and a debris filter. v7: over-thread drawn as a double pass.
  v9: scale 52, so lap 4 meets the top gutter line. v10–v16: label placement, the ≥4-threads crop rule,
  ink-on-ink fix at dash ends, legend swatches, and the rule line restated.

## Mandate responses
| id | mandate | status |
|---|---|---|
| S1 | Title truth | FIXED. The title is `THE FIXED POINT REPELS`, the tagline `NEITHER PLAYER EVER ARRIVES` is kept, and the + is labelled `NASH EQUILIBRIUM` / `θ = ψ = 0`. No sheet text claims the equilibrium is absent. θ and ψ are drawn locally at cap height, because the house font has no ψ and its θ reads as a dot at label size |
| S2 | Float = leg | FIXED for the along-floats, and the rule line is RESTATED to what the marks carry. Every over-float that runs ALONG its leg equals the summed leg of one consecutive stretch of its player's steps (×52 mm/unit). Fit over 149 uncropped along over-floats: slope 1.0000, intercept 0.0000 mm, max residual 3e-14 mm. The threads that cross the tape ACROSS, and the turn squares, carry the tape width (median 9.9 mm, max 12.8 mm), not a move. Without them there is no weave and no single ribbon (v1–v2), so the legend line says `ALONG THE TAPE: A FLOAT = ITS PLAYER'S RUN OF MOVES, SUMMED` |
| S3 | Hole + full orbit | FIXED. Minimum thread radius is 40.19 mm against r0 = 38.48 mm, with no ink inside r0: every tape is laid outward of the outward L, 1.5 mm clear. The h→0 flow is a complete 360° dashed circle at r0, starting at the start angle a0, and is labelled `h → 0: THE FLOW CIRCLES`. r03's 110° arc is deleted |
| S4 | No turn-taking words | HELD. No sheet text uses answers, then or alternates |
| S5 | Stats match the sheet | FIXED. The footer gives `STEP 70  R 1.33  LEAVES THE SHEET`: the first state outside the cloth window is step 70 at r = 1.3287. `H 0.26` and `R 0.74` are exact |
| S6 | No dossier/encoding | DEFERRED (process). Every channel formula is on the HANDOFF `rule:` line |
| S7 | r02 hairline key | n/a (dropped in ledger) |
| A1 | One unbroken ribbon | FIXED by construction. Each run's outward L carries a G band, a D band and a TURN square at its convex corner, so the tape is continuous with one width (9 mm + 1.5 mm clear). The NW/SE staircases are the same ribbon as the NE/SW arcs, both families are present everywhere, and there are no bare-warp bridges. A debris pass drops scraps under 60 mm² or with fewer than 4 threads, and a tape needs at least 4 of its threads in the window |
| A2 | Off-centre crop | FIXED. The + is at x = 78 mm, 27 mm left of 105. The left edge crops laps 2, 3 and 4. The bottom gutter line crops lap 2 and the lap-3 corner. Lap 4 meets the top gutter line. The sheet is an asymmetric window |
| A3 | Plot craft | FIXED. The shortest inked thread segment is 2.50 mm (under-dashes are 2.6 mm). Travel 10.36 m < draw 14.97 m. 13,962 commands (< 15k). Checked ink-on-ink crossings: 0 |
| A4 | 12 mm gutter | FIXED. The tagline baseline is 12.0 mm above the top cloth line, and the footer cap-line 12.0 mm below the bottom cloth line. Both are hard crop lines of the window |
| A5 | Accent scarce | NOT WORSE. The + is crimson again, but crimson is still half the ink |
| A6 | Weight advancing outward | DEFERRED (r05), as the ledger says |
| A7 | Lineage as silhouette | PARTIAL. The over-thread is now a double pass, so each quadrant has a colour face: crimson-faced where G leads (NW/SE), blue-faced where D leads (NE/SW). That pinwheel is carried by which thread is on top. The spiral silhouette is still the dominant figure, so watch the critic |
| A8–A12 | (closed) | held: no mesh, no floods, every clip on the window edge, shared baselines, no picket stubs |
| A13 | Symmetric legend | HELD: `WEFT G MOVES THETA` / `WARP D MOVES PSI`. Each swatch is a real over-pair sample |
| A14 | Declared flat | HELD. Bauhaus weaving canon, depth from over/under and double-pass weight only |
| A15 | No figure furniture | HELD. No crosshairs, a 2-row legend, no parameter stack |
| A16 | EQUILIBRIUM / NEVER REACHED | dropped (superseded by S1 label) |

## What changed from parent
- **The tape is built from the run's geometry, not a centred stripe.** Steps are grouped into runs:
  consecutive steps, same quadrant, same leader, each closed once the leader's summed move reaches
  2.5 mm. A run is drawn as the L of its two summed moves, taking the corner of larger radius (the outward
  L; the updates are simultaneous, so either L is a drawing convention). Each leg gets a band on its
  outward side. The ALONG family spans exactly the leg, the ACROSS family fills the band's width, and a
  TURN square fills the convex corner. Along wins where they overlap.
- **The weave is a real over/under with plottable cells.** The over-thread (sign of ψθ) rides in pairs on
  two dents of every three of the 1.8 mm reed and is drawn out and back (0.3 mm), so the leader's thread
  is heavier. The under-thread uses every dent and shows as 2.6 mm dashes in the third dent. Under-threads
  also duck across seam gaps, so no under-thread shows through a gap in an over-thread.
- **The composition moved.** The + moved to (78, 117) mm and the scale went from 36 to 52 mm/unit. The
  cloth lives in a window bounded by two 12 mm gutter lines (tagline and footer) and the side margins,
  and is cropped hard on the left, bottom and top.
- **Title and labels.** The title is `THE FIXED POINT REPELS`. The hole carries the crimson + labelled
  `NASH EQUILIBRIUM` / `θ = ψ = 0`, and the full dashed flow circle labelled `h → 0: THE FLOW CIRCLES`.
- **Footer.** 4 lines on shared baselines, with the legend on lines 1–2. The footer carries the exit step
  and radius, the on-top rule, and the aggregation line.

## Measurements / computations
- Run: h 0.26, r0 0.74, a0 0.42622 (seed 7). The run is identical to r01/r03. 3,639 states were followed
  until the run cannot touch the window, grouped into 295 runs.
- Float fit, along over-floats not cut by frame or axis: n = 149, slope 1.000000, intercept 0.000000 mm,
  max |residual| 3.2e-14 mm. Runs per float: 1 → 58, 2 → 51, 3 → 32, 4 → 7, 5 → 1. Adjacent runs in one
  row join, and a float never crosses an axis, so a float is always one consecutive same-leader stretch.
  Along float lengths: 2.59 / 7.66 / 25.29 mm (min / median / max).
- Across/turn over-floats: 264 of them, 2.73 / 9.9 / 12.8 mm (min / median / max). They carry the tape
  width.
- Crossings: 3,009 under-thread ducks. Over/under is set per crossing by the sign of x·y about the
  equilibrium. The gcode check finds 0 places where a crimson and a blue segment cross with both inked.
- Hole: minimum thread radius 40.19 mm, r0 38.48 mm, so a clearance of 1.71 mm. The flow circle is 53
  dashes of 2.5 mm, starting at a0, covering 360°.
- Window: x 10–200, y 37.3–260.2 mm. Tagline baseline 272.2, footer cap-line 25.3, so the gutter is 12.0 mm
  at both ends. The run first leaves the window at step 70, r = 1.3287.
- Crop hygiene: 347 leg bands not laid (< 45 % in the window, or fewer than 4 threads in it), 1 debris
  scrap dropped.

## Plot budget
- draw **14.97 m**, travel **10.36 m**, **13,962** commands, **1,987** pen-downs. By pen: black 557,
  crimson 740, blue 690. 3 pens.
- Preview estimate: 11.5 min. On Leo (F600 draw, G4 P1.0 dwells): about 25 min drawing, about 5 min
  travel, and about 66 min of lift dwells, so about 1 h 40 min. r03 needed about 3 h of dwells for 5,546
  lifts.
- Order: crimson 1, then blue 2, then black 0 last (type over the cloth).

## Self-critique (rubric)
1. Hierarchy — 7. The woven spiral dominates, the title comes second, the footer third. All laps carry
   equal weight (A6 is still open).
2. Grid & alignment — 7. The cloth window is set by the two gutter lines and the margins. Title, tagline,
   footer and the left crop share x = 10. The legend is flush right on footer baselines 1–2. The + sits
   on no type line.
3. Tension & asymmetry — 7. The + is off-centre low-left, with hard crops left, bottom and top, and the
   arcs sweep up and right. The rings are still near-concentric.
4. Negative space — 6. The hole is the one designed quiet zone. The wedge in the upper right and the
   band between the lap-1 bottom and the crop are leftovers.
5. Craft for pen — 8. No segment under 2.5 mm, no ink-on-ink, travel below draw, 1,987 lifts, no floods.
6. Concept legibility — 7. The title is true, the hole is labelled, the full flow circle sits against the
   escaping tape, and the face colour flips by quadrant. It is still a spiral at 3 m.
7. Depth — 6. Declared flat. The double-pass over-thread gives a real front/back at 1 m.

**Worst thing on the sheet:** it is still a round, near-concentric spiral target seen through a window.
The figure is the tape's silhouette more than the weave (A7). The pinwheel of colour faces reads at 1 m,
not at 3 m. If the art critic says "spiral in a woven costume" again, route rule 2 applies.
Second worst: the across/turn threads are over-floats that do not carry a move, which is why the rule
line had to say "ALONG THE TAPE".

## Engine requests
- A kit weave primitive: lines with along/fill priority, over/under by a sign field, pair dents, dash
  floor, and serpentine direction. This is the fourth weave plate to hand-roll it.
- A crop-hygiene policy: drop connected scraps below an area or thread count (`_cloth_keep` here).
- The house font needs ψ, and a cap-height θ.
