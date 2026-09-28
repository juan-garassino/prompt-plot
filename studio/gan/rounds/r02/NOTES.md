# gan r02 — escape-spiral (mechanism) · parent: r01 · 2026-09-28

lineage: Bauhaus — Kandinsky, *Point and Line to Plane* (1926). The order taken from it is his
account of the line as the trace of a point pushed by forces. Two forces acting together bend
it into a curve; two forces acting in alternation break it into an angular line. The
Dirac-GAN has both: continuous time is the curve (the closed orbit, blue dotted), and a
training step is the generator's push followed by the discriminator's answer, the angular line
that never closes. The point he starts from, the equilibrium, is the one thing on the sheet
made of bare paper.

## Render
```
.venv/bin/python scripts/render_candidate.py studio/gan/rounds/r02/piece.py \
  --fn escape_spiral --seed 7 --paper a4 --palette black,crimson,dodgerblue \
  --out ~/Downloads/pp_gan_escape-spiral_v8.png
```
- final PNG: `~/Downloads/pp_gan_escape-spiral_v8.png`
- final GCODE: `~/Downloads/pp_gan_escape-spiral_v8.gcode`
- seed 7, a4 portrait, 3 pens. Seeds 11 and 3 were also rendered
  (`pp_gan_escape-spiral_v7_s11.png`, `_v7_s3.png`) and give the same composition. The
  seed only moves the start angle a0 (0.43 / 0.57 / 0.33 rad), and those runs exit after
  551 and 598 steps. Seed 7 was kept because its exit leg crops the frame cleanest.
- trials: v1–v7 in `~/Downloads/pp_gan_escape-spiral_v*.png` (none overwritten).

## Mandate responses
There is no LEDGER.md or FEEDBACK.md for `gan`, so there are no open J/A/S mandates. The
work order below is DESCRIPTION.md § Weak plus the "If only iterating" tests. Every row is
answered.

| id | mandate | status |
|---|---|---|
| W1 [concept] | outward spiral does not read; legs scattered dashes | FIXED. The whole run is drawn with no occupancy thinning, one continuous path from the start point on the orbit to the frame, 3.8 turns. The eye can trace it end to end. The last generator leg is cut by the right frame edge. |
| W2 [hierarchy] | green mesh loudest, duel quietest | FIXED. The mesh is gone and the run is the dominant mass. Flight legs are 1–3 passes, weighted by the force g. The title is second, the key and step counts third. |
| W3 [craft] | ink floods at horn / trough / front band | FIXED (removed). No surface is drawn. Nearest ink between two different turns is more than 3 mm (grid search). The only multi-pass bands are the weight bands (0.5 mm pass gap, 0.43 mm on the title). |
| W4 [craft] | green sliver crosses margin to paper edge | FIXED. Every run is clipped exactly (Liang–Barsky) to the drawable area inset 0.5 mm. The exit leg stops on the margin. |
| W5 [space] | empty top third is leftover | FIXED by moving the composition. The equilibrium sits at (u 0.56, v 0.36), so the spiral fills the top two thirds. The quiet band (v 0.68–0.80) separates it from a bottom type band. The ψ knife runs down through that band as its column rule. |
| W6 [grid] | footers on different baselines; swatch floats | FIXED. There is one bottom baseline for the tagline and the last stats row. The title is sized to fill exactly margin → knife − 6 mm. The key starts at knife + 6 mm, so the gutter is equal on both sides, and the key's cap line equals the title's cap line. The swatch was deleted; the key samples are the real leg bands. |
| W7 [craft] | far-half radial stubs read as picket fence | FIXED (removed with the mesh). |
| W8 [concept] | G THETA missing, D PSI present | FIXED. The key reads `G PUSHES THETA` / `D ANSWERS PSI`, symmetric, each beside its real leg band. |
| W9 [depth] | depth only from ring compression | ARGUED. The plate is flat by declaration: the Bauhaus / Kandinsky plane is flat, and a plan view is the only projection where the radius growth, the one fact the plate is about, reads undistorted. The only depth-like cue is line weight tracking the force, heavy flights against hairline crawls. |
| iter-1 | spiral traceable end to end, double-passed | FIXED (1–3 passes by g). |
| iter-2 | mesh density cap | N/A. The mesh is removed, as the brief permits ("or only its sign-change lines ψθ=0 as two crossing knives"). |
| iter-3 | surface up / one baseline / remove sliver | FIXED (see W5, W6, W4). |

## What changed from parent
- **The subject flipped.** r01 was a 3D saddle with the run as decoration. r02 is the run itself, drawn in plan. The saddle is reduced to its two sign-change knives ψθ=0, where the force is exactly ½. These are dotted, and gated by the run's occupancy so they pass under it.
- **The run is shown in two grammars, and both are real.** When both legs of a step are at least 1.2 mm on paper, the step is drawn as a crimson θ-leg and a black ψ-leg with butt joints: the D band owns every corner and the G band stops at its edge, so no corner is inked twice. When the legs are shorter than the pen can resolve, the staircase is drawn as the exact polyline through the iterates, a hairline "crawl". It deviates from the staircase by less than 1.2/√2 mm.
- **Step counts per quarter-turn where the force dies** (ψθ>0) are set along each crawl arc's diagonal, e.g. `315 STEPS` on the last arc. This is the saturating-loss stall, stated as data.
- **The continuous-time orbit** (blue dotted, r = r_start) is drawn after the run and gated by its occupancy. Where the first discrete steps still lie on the orbit, the orbit gives way; it reappears where the run pulls off it.
- **The equilibrium** is a bare-paper hole with the crimson `+`. The knives stop 3.5 mm inside the orbit.
- **Layout.** Giant weighted title bottom-left, key and stats bottom-right, split by the ψ knife. The whole spiral sits off-centre and exits through the right frame.

## Measurements / computations
- Dirac-GAN, h = 0.26, r_start = 0.74, a0 = 0.4262 rad (seed 7). Simultaneous GDA stops at the first iterate that lands off the drawable area: **578 steps, r 0.74 → 3.537, 3.80 turns**.
- The exact growth law was checked on every step: `max |r²ₙ₊₁/r²ₙ − (1 + h²g²)| = 4.4e-16` (machine precision). The radius never decreases.
- The force g = σ(−ψθ) ranges 0.0072–0.9970 along the run.
- Steps per quarter-turn, in order: Q1 10, Q2 11, Q3 15, Q4 10, Q1 15, Q2 10, Q3 18, Q4 9, Q1 23, Q2 8, Q3 36, Q4 8, Q1 79, Q2 7, **Q3 315**, Q4 4 (exit). Flight quarters (ψθ<0) shrink from 11 to 7 steps as the teeth grow, while crawl quarters grow roughly exponentially (the stall goes as ~e^{r²/2}).
- 99 steps are drawn as flights and 479 as crawls: 17% of the steps carry the heavy ink.
- Placement sensitivity (measured while choosing the layout): with the equilibrium at (0.55, 0.50) and k = 22 mm, the same run needs **116,911 steps** to leave the sheet. When the frame falls inside a crawl quadrant, escape takes exponentially longer. Recorded, not drawn.
- Scale k = 31 mm per unit of (θ, ψ). Orbit radius 22.9 mm. Largest tooth ≈ 25 mm.
- No ink of two different turns lies within 3 mm of each other (sampling at 0.5 mm, grid search).

## Plot budget
- draw 5.29 m (black 4.14 m / crimson 1.08 m / blue 0.06 m), travel 6.60 m, 7,021 commands, 955 pen lifts (black 673, crimson 203, blue 79).
- 3 pens, 2 swaps.
- time: the engine estimates 5.4 min at F2200. At Leo settings (F600 draw, G1 F2000 travel, ~1 s dwell per lift/drop) it is about 9 min draw + 3 min travel + ~32 min dwells, **≈ 45 min**. The lift count is dominated by the dotted knives and the multi-pass bands.
- bounds clean: drawn X 12–199.5, Y 12–284 on a 10–200 × 10–287 drawable area.

## Self-critique
| dim | score | note |
|---|---|---|
| hierarchy | 8 | The run dominates at 3 m. The title is second. Counts and key reward 30 cm. |
| grid & alignment | 8 | Shared baseline, equal gutters, cap lines matched. The ψ knife is both the plane's axis and the type column rule. |
| tension & asymmetry | 7 | Off-centre, lopsided spiral, and the last leg is cut by the frame. The top-right corner is a little passive. |
| negative space | 7 | Bare-paper hole and a quiet band above the type. The band is shaped by the spiral's lower arc but not tightly. |
| craft for pen | 8 | Butt-jointed bands, no floods, turns ≥3 mm apart. 955 lifts is heavy for Leo. |
| concept legibility | 7 | "Every step moves further out" lands at a glance, and the curve-versus-angular-line contrast is the Kandinsky twist. But a dotted cross plus a spiral still leans toward a phase-portrait figure. |
| depth | 5 | Flat by declaration; weight-by-force is the only depth cue. |

**Single worst thing:** with its two dotted knives through the equilibrium, the plate can
still be read as a phase-plane plot, a spiral on axes, rather than a Kandinsky plane. The hairline
crawl arcs, the most interesting part (where the time goes), are the quietest ink on the sheet.

## Engine requests
- `kit.giant_type` weight bands on diagonals (N, X) come out as visibly separated passes at
  0.43 mm. A mitred band offset for single-stroke glyph polylines would close them.
