# millennium-poincare r01 — faithful · parent: none · 2026-09-29

lineage: Vera Molnár, *(Dés)Ordres* (1974). The order taken is nested closed figures whose
deviation from the ideal form is measured ring by ring. Here each ring is the whole space at one
instant of Ricci flow, and the deviation (a pear with a cap) decays until each nest is round and
vanishes.
style: canon 6, MODERN SCIENCE POSTER, on the series' cream sheet (black + crimson, crimson scarce).

## Render
```
.venv/bin/python -W ignore studio/millennium-poincare/rounds/r01/compute.py   # ≈ 6 min, writes isochrones.npz
.venv/bin/python scripts/render_candidate.py studio/millennium-poincare/rounds/r01/piece.py \
  --fn poincare_faithful --seed 7 --paper a3 --palette dimgray,black,black,crimson \
  --out gallery/studio/millennium_poincare/current/pp_millennium_poincare_faithful_v7.png
.venv/bin/python studio/millennium-poincare/rounds/r01/audit.py gallery/studio/millennium_poincare/current/pp_millennium_poincare_faithful_v7.gcode
```
- final: `gallery/studio/millennium_poincare/current/pp_millennium_poincare_faithful_v7.png` + `.gcode`, true-width preview
  `gallery/studio/millennium_poincare/current/pp_millennium_poincare_faithful_v7_truewidth.png` (pens at 0.1/0.3/0.3/0.5 mm, no stats box).
- seed 7. The piece uses no randomness, so seeds 3 and 7 produce identical commands (checked).
- trials: v1 → v7. v1 had the first layout. v2 scaled up and added the footer. v3 added pause
  hysteresis. v4 tried β = 35° and was rejected. v5 shifted the plate right. v6 fixed shell
  crowding. v7 clips rings to the keyline and has the larger SOLVED.

## Mandate responses
| id | mandate | status |
|---|---|---|
| — | No LEDGER.md, FEEDBACK.md or DESCRIPTION.md exists for this slug (new plate, first round). There are no open J*/A*/S* rows. | n/a |
| brief | encoding.md §4 / §5 `[faithful]` / §6 / §9 / §11 | followed; deviations are listed under Measurements |

## What changed from parent
No parent. These are the reference's layout faults and how each one was fixed:
1. The body's diagonal steepened from 44° (measured on the reference) to **62°**. The body went
   from ≈90 % of the sheet width to ≈65 %, which opens the upper-left quiet triangle.
2. The reference's **filmstrip of 7 shrinking ellipses is cut** (lie 1: they stay elongated and
   their gaps shrink). Its lower-right corner now holds the data footer.
3. **"A loop contracts to a point"** and its leader line are cut (forbidden 13). The only red loop
   left is the one that does **not** contract.
4. The full wireframe survives only as the **back half-shell of the surgery instant**, seen past
   the cut face. It is grey, with solid parallels and **dashed half-meridians**, which is the
   reference's own solid/dashed vocabulary. The cut face carries the flow's isochrones.
5. The gold point became **two red extinction points**. There is no ochre pen.
6. The three bottom-edge captions collapsed into one colophon. The corner caption keeps the
   reference form (4 short spaced-caps lines flush right + short rule) but carries the plate's
   line: TO PROVE / IT IS ONE SPHERE / THE FLOW / CUTS IT IN TWO.
7. The title is kept on two lines as in the reference, at the **measured** cap height (6 mm; the
   reference is 19 px of 1402 = 5.7 mm on A3). The encoding's 8 mm was about 40 % oversize. The
   statement is 3.2 mm, sheared to italic as in the reference.

## Measurements / computations
**Reference (1122 × 1402 px):**
- title x 75–399, y 75–139, cap 19 px
- rule y 159
- statement y 183–263, pitch 30 px
- corner caption right edge x 1047 (u .933), pitch 22 px, cap 7 px
- body x 64–1069, y 159–1179
- bottom captions v .905–.950

**Data** (`compute.py`, a copy of `data/run_neckpinch.py`'s path: same N = 400, same adaptive step,
same surgery at h = 0.12). Every solver state is kept, and the snapshot is the state *nearest*
each target time. There is **no interpolation at all**.
- t_s = **0.0546465** (reproduces the npz). Neck at t_s = 0.11971.
- Max |t_snap − t_target| = **1.79e-5** (< 1e-4). The pre-surgery solver step is ≤ 4.5e-5.
- T_ext A = **0.38734** (slope −4.003), B = **0.11714** (slope −3.908). This matches dossier check #1/#5.
- Rings: **A 33, B 6**. That is t_s + 0.01k while t < T_ext.
- Pole-to-pole grows from **4.001 → 4.335** (t = 0 → t_s, neck-pinned).
- Neck ψ at t = 0, t_s−0.05 … t_s−0.01, t_s: 0.3143 · 0.3037 · 0.2786 · 0.2501 · 0.2169 · 0.1760 · 0.1197.
  Lobe A goes 1.4139 → 1.2447 (−12 %) against the neck's −62 %.
- The 2-D control figure (0.314 → 0.355) is quoted from the dossier's npz run. It was not re-run here.

**Mapping.**
- 62 mm/unit. Axis at φ = 62°, tilted **β = 40°**, with the A end toward the viewer.
- Cut point at sheet (156, 199).
- Section (z, ρ) → sheet: z·cosβ along the axis, ρ along the in-picture normal.
- Shell point (z, ψ, θ): the along-axis position gains ψ·sinθ·sinβ. Every parallel is an ellipse
  with minor/major = sin 40° = 0.643 (one basis).

**Alignment.**
- Pre-surgery lines: the neck minimum (parabolic refinement) is pinned at z = 0.
- Keyline: the cut node i_s is pinned at z = 0.
- Pieces: each ψ²ds-centroid is held at its t_s position (the capped A0/B0 coincide with the
  keyline + caps).

**Time-occlusion.** Each past line is hidden under every later past card plus the keyline card.
Fraction of each line clipped:

| line | clipped |
|---|---|
| start | 35.3 % |
| t_s−0.05 | 32.8 % |
| t_s−0.04 | 29.7 % |
| t_s−0.03 | 24.5 % |
| t_s−0.02 | 24.3 % |
| t_s−0.01 | 23.9 % |

The encoding said 21–24 % for the halo. The two earliest lines lose more, because at 62 mm/u the
keyline overruns them over a longer stretch of both poles.

**DEVIATION: future rings clipped to the keyline card.** With centroid pinning, A's rings
overshoot the t_s outline at A's far pole by up to **1.73 mm on the sheet**. The encoding
measured ≤ 0.65 mm. Uncorrected, A3 drew about 44 mm of line *outside* the keyline, where it
read as a past line. Rings are therefore clipped to the inside of the keyline card, and the merge
rule then folds them in. After the clip, no drawn ring sample lies outside the keyline (checked).
The B nest is exact: zero overshoot and perfect nesting.

**Merge rule.**
- Ranking: keyline, start line, then |t − t_s|.
- Implemented with the engine's `Occupancy` (sep 0.85 mm on 0.2 mm samples, which guarantees the
  0.8 mm floor), pause–resume, and fragments < 2 mm culled.
- **Added: pause hysteresis.** A clear gap shorter than 5 mm between two paused stretches stays
  paused. Without it the far-pole merge band was a comb of 2–4 mm crumbs (v2). With it, the rings
  taper cleanly into the band (v3+).
- Merge losses: A1 65 %, A2 47 %, A3–A6 32–45 %, A7–A18 6–37 %, A19–A33 0 %. The halo loses
  6–11 %, except t_s−0.05, which loses 86 % into the start line ("the first step merges into the
  start line").

**Shell (L0).**
- Back half of the t_s surface of revolution. The engine's `Scene3D.surface()` rasterizes a
  161 × 73 (s, θ) grid for the z-buffer, and its own mesh is discarded.
- Drawn on top of that z-buffer, tested with the public `Scene3D.visible()`:
  - parallels at Δs = 0.075 (each a round 2-sphere), 241 samples on the half-circle
  - half-meridians every 15°, dashed 2.2 / 1.5 mm
  - the exact silhouette (sin θ = −(ρ'/z')·tanβ)
- Everything is then clipped to outside the union of all cards.
- Crowd control per family uses `Occupancy` (per-run registration), standing in for ScreenThin on
  free lines.
- The crescent reaches **29.9 mm** beyond the keyline along −axis (≥ 8 mm ✓).

**Red.**
- Caps: two semicircles of radius h = 0.1197 u = 7.42 mm. They end ON the keyline (distance 0.00 mm)
  and together read as one foreshortened circle. Nothing is drawn inside.
- Gap from the cut circle to the first rings: A1 **3.0 mm**, B1 **3.7 mm**, the halo 3.5 mm (≥ 2 ✓).
- Stuck loop: the front half of the t = 0 neck parallel (ψ = 0.3143, length 2π·0.3143 = 1.975).
  Its span is 39.0 mm against the cut circle's 14.8 mm (**2.63×** ✓). The gap to the caps is
  6.8 mm. The back half is hidden under the cards.
- Extinction points: Ø1.6 mm spiral fill at 0.4 mm pitch. The last ring sits 4.8–6.4 mm around
  each point, measured on the foreshortened sheet.

**§11 self-check.**
1. One keyline encloses two nests, each closing on its own red point (6 vs 33); no line crosses
   the keyline ✓
2. Gaps widen toward each point. Rings crowd at the far poles and splay at the cut, and the halo
   fans at the waist ✓
3. The circle is tangent inside the neck, Ø14.8 mm, which is under 1/10 of A's 180 mm width. Its
   interior is bare, with ≥ 3 mm to the first ring ✓
4. A's nest dominates, and the upper-left quiet zone is bare. The minimum gcode gap per layer is
   0.92 / 0.86 / 0.89 mm ✓
5. One basis. The shell shows only outside the cards. The loop is 2.6× the circle and never
   touches it ✓

## Plot budget
Measured by `audit.py` on the v7 gcode. Time model: F600 draw, 2.5 s per lift+drop, travel 33 mm/s.

| layer | pen | meaning | draw | strokes | longest | ≈ min | min gap |
|---|---|---|---|---|---|---|---|
| L0 | black 0.1 (preview dimgray) | the body at the cut instant: back half-shell | 1.69 m | 161 | 144 mm | 9.8 | 0.92 mm |
| L1 | black 0.3 | the space at each instant | 10.98 m | 81 | 629 mm (keyline, ×2) | 22.9 | 0.86 mm |
| L2 | black 0.3 (own layer) | type | 3.46 m | 1052 | 19 mm | 51.6 | 0.89 mm |
| L3 | red 0.5 | events: 2 caps, loop, 2 points, SOLVED | 0.17 m | 12 | 51 mm | 1.1 | — |

- **Total: 16.3 m of ink, ≈ 85 min, 3 swaps.** Bounds are x 15.0–282.0, y 17.0–404.9 (A3
  portrait, margin 15).
- L1 stroke order: start line → halo (outer → inner) → keyline ×2 (identical retrace; each pass is
  a batch boundary of 63 s) → B rings (outer → inner) → A rings (outer → inner).
- The type layer is 60 % of the plot time because of pen cycles (1052 lifts).

## Self-critique (rubric)
| dimension | score | why |
|---|---|---|
| Hierarchy | 8 | A's nest dominates, the B nest and the waist come second, the red events third |
| Grid & alignment | 7 | Title, statement, stamp and colophon share x = 15. The footer and colophon share baseline y = 17. The footer's left edge x = 204 aligns to nothing in the figure. |
| Tension & asymmetry | 7 | The 62° diagonal works, the mass is off-centre, and the crescent weights the lower-left |
| Negative space | 7 | The upper-left quiet zone is shaped. The right column between the corner caption and the footer (x 225–282, y 130–375) is leftover rather than designed. |
| Craft for pen | 8 | Every layer is ≥ 0.8 mm. Merge bands taper cleanly, there are no floods, the red is clean. The type layer is expensive. |
| Concept legibility | 7 | The branching nest and the two points read at 3 m. The pinched waist is short and reads as an X-saddle more than a tube. |
| Depth | 7 | The back half-shell crescent plus the stacked cards give real depth. On the upper flank the section reads flat. |

**Single worst thing:** the t_s section silhouette reads as a pear/vase more than a dumbbell. The
dossier's profile has A's maximum radius near its far pole, and cos 40° foreshortening shortens
the axis. The waist is a short X-shaped saddle. The shell appears only at A's pole, so the "body"
reads as a bowl the nest sits in, not as the reference's continuous dumbbell skin.

## Engine requests
- `Scene3D.depth_field(SX, SY, DEP)`: rasterize without emitting the grid mesh, so bespoke lines
  (parallels at Δs, dashed meridians, silhouettes) can be tested with `visible()`. Here the mesh is
  drawn into a throwaway scene and discarded.
- `Scene3D.lines(..., min_frag=, bridge=)`: fragment culling plus pause hysteresis in the native
  pause–resume, so merge bands never become crumbs. `lines()` also has no per-sample depth
  occlusion *and* halo in one call for 2-D section lines.
- ScreenThin for free (non-grid) line families. Today it only works inside `surface()`.
