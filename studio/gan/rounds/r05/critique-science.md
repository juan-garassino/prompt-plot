# Science critique — gan r05 · machine learning (GAN training dynamics, game theory) · 2026-09-29
render: gallery/studio/gan/trials/pp_gan_iterate_v24.png (gcode gallery/studio/gan/trials/pp_gan_iterate_v24.gcode)

Inputs: HANDOFF r05, encoding.md rev 1 (§4.1 check numbers and §9 lies list stand in for the
missing dossier), LEDGER.md (pass 2). The gcode was parsed per `; color=N` into 2,110 pen-down
strokes: blue 743 / crimson 712 / black 655. Layer order is 0 → 1 → 2. Every crossing of the
68 warps × 76 wefts was rebuilt and tested against my own run (simultaneous GDA, h 0.26, r0 0.74,
a0 0.42622) and against the ribbon cells {z_k·0.9, z_{k+1}·0.9, z_{k+1}·1.1, z_k·1.1}.

## Check numbers
| quantity | dossier (encoding §4.1) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| model / update | Dirac-GAN, f′(s)=σ(−s), simultaneous GDA | same; Mescheder sign convention: ψθ>0 = D scores the fake as fake | footer line 3 keys the faces this way | OK |
| flow Jacobian at 0 | ±0.5i (centre) | [[0,−½],[½,0]] → ±0.5i | the h→0 circle is labelled | OK |
| discrete \|λ\| at r→0 | 1.00841 | 1.0084146 | title `THE FIXED POINT REPELS` | OK |
| z_0 | (113.04, 128.91), a0 24.42° | (113.037, 128.909), 24.4206° | circle dash starts at …, 17.62°, 24.42° (phase = a0) | OK |
| lap ends (step, r) | 50 / 103 / 181 · r 1.115 / 1.688 / 2.556 | 50 / 103 / 181 · r **1.1207** / 1.6919 / 2.5563 | — | OK (lap-1 r is off by 0.006) |
| lap ratio | 1.51 (1.50–1.52 on all rays) | **1.48–1.52** (90°: 1.494/1.482/1.484 · 270°: 1.487/1.481) | footer `EACH LAP ABOUT 1.5 × WIDER`. Ribbon width at 90° is 11.2 → 19.6 mm | OK (the dossier's range is too tight) |
| crossing radii 45° | 39.3/59.0/88.7/133.2 | 39.2/59.0/88.7/133.2 | ribbon 51.6–63.4, 79.2–99.0, 118.8–146.6 (expected 53.1–64.9, 79.8–97.6, 119.9–146.5) | OK, within 1 pitch |
| crossing radii 90° | 41.1/61.4/91.2/135.0 | 41.1/61.4/**91.0**/135.0 | lap 0: **no double-pass**. 56.0–67.2, 81.2–100.8, 120.4–137.2 (crop at 138.5) | OK for laps 1–3 · lap 0 absent |
| crossing radii 180° | 46.0/69.7/106.0/161.0 | 46.0/**69.5/105.9/160.5** | 42.0–50.4 (expected 41.4–50.6). Lap 1 at the left crop is single-pass | minor dossier drift |
| crossing radii 270° | 50.3/74.9/111.0/164.7 | 50.3/74.8/110.8 | 44.8–56.0, 67.2–75.6 (crop 75.7) | OK |
| first exit | step 70, r 1.3287, (9.4, 120.9) | step 70, r 1.32870, (9.36, 120.90), left edge | `STEP 70  R 1.33  LEAVES THE CLOTH` | OK |
| in-window iterates | ≈196 | 196 | 186 in double-pass ribbon · **7 on bare paper (steps 0–6) · 3 on single-pass cloth (steps 7–9)** | **VIOLATED** (§11.4 wants 0 exceptions) |
| step length in frame | 1.25–31.5 mm; turn 6.65° → ≤13.7° | 1.254–31.539 mm; 6.653° → 13.28° | — | OK |
| median step D-ahead / G-ahead, laps 0–3 | 5.1/5.9/4.9/1.5 · 6.7/11.7/19.4/28.0 | 5.1/5.8/4.9/1.52 · 6.7/11.7/**18.4**/28.0 | long straight crimson facets at the top and SE vs smooth blue NE crawl | OK |
| hole | cloth ρ ≥ 39.98, circle 38.48 | — | min thread ink ρ 39.975 · 0 inked crossings inside · circle 53 dashes, r 38.474–38.487, max angular gap 3.08°, 360° | OK |
| sign rule | 100 % | — | **2,331 / 2,331** in-ribbon crossings correct (winner over, loser hidden) · 0 crossings with both threads inked | OK |
| basket 2/2 | 50 % ± 1 % | — | 49.9 % warp-over on the 1,545 ground crossings not next to the ribbon · **48.6 %** over all 2,197 ground crossings (224 tie-down inversions next to the ribbon + 6 other defects) | PARTIAL |
| float weight (≥3 over = double pass) | ribbon only | — | 2,287 / 2,331 in-ribbon crossings double-pass (98.1 %) · **44 single-pass** · **0 ground double-pass (no false ribbon)** | PARTIAL |
| reed / gaps | p 2.6 (2.8 allowed) · g 2.4 | — | p = 2.800 exactly, half-pitch phase residual 1e-14 · min along-thread gap 2.400 (1.9 mm of paper at 0.5 tip) · double pass 0.4 apart → 1.9 mm white | OK |
| plot ceilings | ≤2,300 pen-downs, <15k cmds, travel<draw | — | 2,110 · 14,686 · 11.98 m < 23.10 m · thread min segment 2.51 mm (276 sub-2.5 mm strokes are type glyphs) | OK |

**Dossier (encoding) errors, as findings.**
- §10 says the ribbon at step 0 is "clipped by the hole to about half width (≈3.9 mm, 1–2
  threads) … the iterate is still on cloth". That is false. At step 0 the ribbon spans
  [34.63, 42.33] mm and the cloth starts at 39.98. Only 2.35 mm (0.84 pitch, 30 % of the width)
  is on cloth, and z_0 itself sits at ρ 38.48, on bare paper.
- §11.4 ("every in-frame iterate inside cloth, 0 exceptions") contradicts §4's hole rule
  (ρ < r0 + 1.5 mm is bare). Steps 0–6 have ρ 38.48–39.98, inside the +1.5 mm margin.
- Lap ratio is 1.48–1.52, not 1.50–1.52. Some §4.1 radii drift by 0.2–0.5 mm.

## Lies list
| item | status |
|---|---|
| no "no equilibrium" | clean. `+` labelled `NASH EQUILIBRIUM θ = ψ = 0`, title `THE FIXED POINT REPELS` |
| no turn-taking vocabulary, no L-steps | clean. The footer has no answers/then/alternates. The chords are diagonal, the edges quantised only by the reed |
| no float/dash/width keyed as move, loss or speed | clean. Width is keyed only as `EACH LAP ABOUT 1.5 × WIDER` (∝ ρ, true) |
| no partial flow arc | clean. 360°, 53 × 2.5 mm dashes, phase a0, labelled `h → 0: THE FLOW CIRCLES` |
| no ink at ρ < 39.98 except `+`, labels, circle | clean. Min thread ρ 39.975, 0 black strokes in the window outside the hole |
| no number the sheet does not show | clean-ish. `STEP 0 ON THE CIRCLE` is true of r0, but no mark shows *where* on the circle step 0 is: the dash phase is invisible, and the ribbon is imperceptible there (mandate 1/3) |
| no "the cloth is the whole run" | clean. The window is the declared cut edge, and the footer tops out at y 25.3 < 37.3 |
| `BARE PAPER: CLOSER THAN THE START` | **VIOLATED (small)**. The bare disc is ρ < 39.98 mm, not < 38.48. The 1.5 mm annulus holds steps 0–6 of the run, which are not "closer than the start", on bare paper at the NE rim (angles 24°–64°) |
| no ink-on-ink / no paper in cloth except the hole | **VIOLATED (small)**. 0 ink-on-ink, but **5 crossings have neither thread inked** (paper holes in the cloth): (101.8, 80.8), (199.8, 47.2), (37.4, 108.8), (37.4, 111.6), (199.8, 195.6). The top-right corner basket is inverted at (197.0/199.8, 246.0/248.8) |

## Scores
- **truth 9**
  - All physics, keys and printed numbers recompute exactly: the sign convention, |λ|, exit
    step 70 / r 1.33, lap ratio ≈1.5, and the h→0 circle.
  - The only untruth is the hole margin. It swallows steps 0–6, and the bare paper there is not
    "closer than the start".
- **fidelity 8**
  - The face = sign(ψθ) is exact at 100 % of 2,331 crossings, with 0 false-ribbon double passes.
  - Ribbon extent = [0.9 ρ, 1.1 ρ] within one pitch on every measured ray.
  - The basket is 49.9 % away from the ribbon, and one reed carries no tone.
  - Losses: 1.9 % of in-ribbon crossings (44) drop to single pass. The whole first 66° of the
    run (steps 0–9) is not visible as ribbon. There are 5 empty crossings.
- **legibility 7**
  - The widening is readable: at 90°, laps are 11.2 → 19.6 mm.
  - But the spiral does not visibly start anywhere. It emerges at the θ = 0 seam at 12 o'clock,
    (78, 154), not from z_0 on the rim at (113.0, 128.9).
  - The straight axis seams dominate the 3 m read as a quadrant pinwheel: 67 mm of seam on
    θ = 0 and 36 mm on ψ = 0. They are true, but they compete with the spiral.
  - Nothing on the sheet tells a stranger which way along the spiral time runs, so "it only
    leads OUT" rests on the title alone.

**VERDICT: FAIL** (legibility 7 < 8)

## Mandates
1. **The run's start must be on the cloth. Steps 0–9 are invisible.**
   - Measured: 7 in-frame iterates (steps 0–6, ρ 38.48–39.73 mm) lie on bare paper inside the
     39.98 mm hole edge. Steps 7–9 fall on single-pass floats. The first double-pass ribbon
     crossing is at step 10, ≈91°, (79, 154).
   - Expected: 0 in-frame iterates without a double-pass float. A visible ribbon starts at z_0
     = (113.04, 128.91) on the circle's rim, NE arc 24°–91°.
   - Fix one of the two. (a) Drop the +1.5 mm clearance so cloth starts at r0 = 38.48, and make
     the ribbon one-sided where it would cross r0. (b) Keep the hole and change the footer to
     `BARE PAPER: CLOSER THAN THE START` only if the disc is exactly r0.
   - Also correct encoding §10/§11.4. They claim step 0 is on cloth at "half width". It is 2.35
     mm, 0.84 pitch.
2. **Float weight must mark 100 % of in-ribbon crossings, and the cloth must have no holes.**
   - Measured: 44 of 2,331 in-ribbon crossings (1.9 %) are single-pass. They sit at the NE rim
     x 79–102 / y 145–157, the left crop x 12.2–15.0 / y 114–126 and 173–176 (lap 1 reads as
     ground there), and at the edges.
   - Measured: 5 crossings have no thread inked, at (101.8, 80.8), (37.4, 108.8), (37.4, 111.6),
     (199.8, 47.2), (199.8, 195.6). The basket is inverted at the top-right corner (197–200,
     246–249).
   - Expected: double pass decided by ribbon membership, which is already exact per crossing,
     not by the "≥ 3 consecutive" proxy that fails at clips and crops. 0 empty crossings.
     Overall ground over-share 50 % ± 1 % (now 48.6 %).
3. **Show where step 0 is, so the direction of escape is legible.**
   - Measured: the circle's 53 dashes are uniform (2.5 mm at a 6.79° pitch). Their phase at
     a0 = 24.42° cannot be recovered by eye, and no mark on the sheet locates `STEP 0`, which
     the footer names.
   - Measured: the only outward cue is lap width (11.2 → 19.6 mm at 90°, 11.2 → 16.8 mm at 0°).
     The 67 mm θ = 0 and 36 mm ψ = 0 seams read first, as quadrants.
   - Expected: z_0 at (113.0, 128.9) is visibly the start, e.g. the hole's second label group
     becomes `STEP 0 · h → 0: THE FLOW CIRCLES`, set at the rim beside z_0 (still ≤ 2 groups in
     the hole). A stranger can then name the start and see each lap wider than the one before.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 title truth | FIXED, holding | `THE FIXED POINT REPELS` / `NEITHER PLAYER EVER ARRIVES`. \|λ\| = 1.00841 > 1. `+` labelled |
| S2 perceived float = Σ moves | FIXED (claim retracted, not faked) | No text keys any float, dash or width to a move. 0 ground crossings double-pass, so nothing reads as a false float. Along-thread gaps are all ≥ 2.40 mm (1.9 mm paper), so floats cannot fuse. |
| S3 hole + full circle | FIXED, holding | Min thread ρ 39.975 > 38.48. Circle 360° (max gap 3.08°), r 38.48 ± 0.01, through z_0, labelled |
| S4 simultaneous updates | FIXED, holding | No turn-taking words. Diagonal chords, no L-staircase (last round's watch item is closed) |
| S5 stats match sheet | FIXED, holding | Step 70, r 1.3287, left edge (9.36, 120.90) recomputed. Caption is now `LEAVES THE CLOTH` |
| S6 no dossier / encoding | PARTIAL | `encoding.md` rev 1 carries the §4.1 check numbers and the §9 lies list, and they recompute (see table). Still no `dossier.md`. §10 and §11.4 contain the step-0 errors above, and the lap-ratio range is too tight |
| S8 tape covers every in-frame iterate / window declared | PARTIAL | Window declared as the cut edge, and the footer is ≤ y 25.3 (was under the type at y 11–39). Old gap steps 86–89 are now covered. 186/196 in-window iterates are in double-pass ribbon, but steps 0–6 are on bare paper and 7–9 are single-pass (mandate 1) |
| S9 key on-top in words | FIXED | Footer line 3: `WARP ON TOP: D SPOTS THE FAKE (ψθ > 0) · WEFT ON TOP: G FOOLS D (ψθ < 0)`. Correct under Mescheder's convention (f′ = σ(−ψθ) → 0 when D wins, measured 1.5 vs 28.0 mm median steps on lap 3) |

No truth that held in r04 regressed.
