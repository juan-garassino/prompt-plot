# millennium-poincare r02 — abstract · parent: none · 2026-09-29

Lineage: **Vera Molnár, *(Dés)Ordres* (1974)**: nested closed figures whose deviation from the
ideal form is measured ring by ring. I take its order, not its look. Here the deviation (a pear
with a cap) is removed by Ricci flow, ring by ring, until each nest is round and vanishes.
There are no squares and no jitter, and every ring is solver output. Canon 6, MODERN SCIENCE
POSTER, on the series' cream sheet: one body, a field whose density IS the data, a data footer.
ORDER: BRANCHING NEST → two FLOW-TO-ATTRACTOR nests, stacked by time-occlusion.

**Flatness declared.** The meridian plane is the only place the profile embeds honestly
(dossier lie 7). Depth is spent on TIME through the occlusion stack: later cards lie on top of
earlier ones, so each nest reads as a terraced mound whose height is its remaining lifetime.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-poincare/rounds/r02/piece.py \
  --fn poincare_two_nests --seed 7 --paper a3 --margin 15 \
  --palette black,black,crimson --out gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.png
.venv/bin/python studio/millennium-poincare/rounds/r02/render_truewidth.py \
  gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.gcode gallery/studio/millennium_poincare/current/pp_millennium_poincare_abstract_v4_phys.png 0 0 297 420 5
.venv/bin/python studio/millennium-poincare/rounds/r02/audit.py gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.gcode
```
- PNG: `gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.png`. The stock preview puts its legend
  over the top-right caption, so judge from `_phys.png`, which draws every stroke at its nib width.
- GCODE: `gallery/studio/millennium_poincare/trials/pp_millennium_poincare_abstract_v4.gcode`
- Seed 7. The piece uses no randomness. Seed 11 (`_v5`) produces byte-identical gcode (diff checked).
- Data: `run_snapshots.py` → `snapshots.npz`. It must exist before the piece is imported. Re-run
  it with `.venv/bin/python -W ignore studio/millennium-poincare/rounds/r02/run_snapshots.py`
  (≈100 s CPU).

## Mandate responses

| id | mandate | status |
|---|---|---|
| — | No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exists for this slug, so there are no open J*/A*/S* rows. The dispatch pointed at "DESCRIPTION.md § What is on the sheet", but that file does not exist. The binding brief is encoding.md §3–§11 plus the curator note. | n/a |
| curator | loops/surface from a real flow | FIXED. Every black line is an isochrone of rotationally symmetric Ricci flow on S³ (Angenent–Knopf form), from the dossier's solver. No curve is drawn by hand. |
| curator | may say SOLVED | FIXED. SOLVED is in red in the stamp. Hamilton is named. Fields 2006 and Clay 2010 are both marked declined. |
| curator | one clean layer per pen, stated order, batchable, minutes per layer | FIXED. Layers run 0 → 1 → 2. The line layer runs start → halo (outer→inner) → keyline ×2 → B (outer→inner) → A (outer→inner), with nearest-end chaining inside each line. The longest stroke is the keyline, 734 mm ≈ 73 s, which is a clean batch boundary. Minutes are listed below. |
| curator | name the LINEAGE | FIXED. Molnár, (Dés)Ordres, 1974. |
| enc §4 data | snapshots exactly at 0, t_s ± 0.01k; report max \|t_snap − t_target\| | FIXED. **max \|t_snap − t_target\| = 0.0**. Each explicit step that would overshoot a target is shortened to land on it. No interpolation is used anywhere. |
| enc §4 Δt | Δt = 0.01 anchored at t_s, no re-spacing | FIXED. There are 5 past lines (t_s − 0.05 … t_s − 0.01), plus t = 0, the keyline t_s, **33 A rings** (t_s + 0.01 … + 0.33) and **6 B rings** (… + 0.06). |
| enc §3 occlusion | past lines clipped by later cards; NOTES state clip + pole-to-pole growth | FIXED. Pole-to-pole length is 4.0006 (t=0) → 4.0433 → 4.1218 → 4.1867 → 4.2408 → 4.2878 → **4.3346** (t_s). Occluded fractions: start 31.3 %, t_s−0.05 29.0 %, −0.04 26.2 %, −0.03 21.7 %, −0.02 21.4 %, −0.01 21.5 %. The encoding predicted 21–24 %. The two oldest lines lose more because five later cards overrun their poles. |
| enc merge | rank by \|t − t_s\|, pause within 0.8 mm (Occupancy), cull < 2 mm | FIXED, with one stated addition: **hysteresis**. A line pauses at < 0.85 mm (sample-to-sample, which is where 0.8 governs) and resumes only once it is 1.2 mm clear. That second threshold is a second engine `Occupancy` fed the same samples. Without it, rings running at ≈ 0.8 mm near A's far pole flickered into 1–3 mm crumbs (v2). The minimum 2 mm cull is unchanged. |
| enc §11.1 | two nests, each on its own red point; 6 vs 33; nothing crosses the keyline | PASS. Measured on the gcode: **minimum gap between different strokes of the line layer = 0.837 mm, 0 samples under 0.8 mm**. Nothing crosses anything. |
| enc §11.2 | gaps widen toward each point; crowd at far poles; halo fans at the waist | PASS. This falls out of the data (see crops). |
| enc §11.3 | cut circle tangent inside keyline, Ø ≤ 1/10 of A, bare interior, ≥ 2 mm to first ring | PASS. Ø / A width = 0.0962 (h = 0.11971, A keyline ψ_max = 1.2447). Nearest non-keyline ink is **3.09 mm** clear of the red ink edge. The interior is bare. |
| enc §11.4 | A ≥ 3× any mass; quiet zone bare; diagonal; no caption touches a line | PASS. The closest text box to any line is 14.7 mm. The upper-left x 15–150, y 205–320 is bare. |
| enc §11.5 [abstract] | flatness declared, two mounds | Declared above. The mound read is carried only by the occlusion terracing, which is subtle at 3 m. |
| enc §4 dot | Ø 1.6 mm, bare ≥ 5 mm | **ARGUED: Ø 1.9 mm.** At 1.6 the dots vanished at arm's length next to the 14.8 mm cut circle. 1.9 is the largest size that still keeps ≥ 5 mm of bare paper: A 5.33 mm, B 5.02 mm. |
| enc §5 scale | 60 mm/u, cut ≈ (168, 215) | ADJUSTED within the allowed range: **62 mm/u, cut (165, 200)**. At 60 the mass floated 54 mm off the bottom edge. Now the ink bbox is x 30.1–239.9, y 33.8–296.8, ≥ 15 mm inside the margin everywhere and never cropped. |
| enc §6 colophon | bottom-left if ≥ 8 mm clear of A, else under footer | Under the footer: A's lowest ink is 34 mm, so bottom-left would have had 4 mm. |

## What changed (self-rounds; no parent)

- **v1.** Built the full system: solver snapshots, neck/centroid alignment, time-occlusion, the
  merge, red events and type. Three problems: 45 bounds clamps (the acute on É poked above the
  sheet), the engine's proportional type broken ("s mply", "homeomorph c"), and the mass
  floating high.
- **v2.** Re-set the title baseline from the ink top of É. Wrote proportional metrics
  measured from glyph ink. Moved the whole body down and left and scaled it 60 → 62, so the
  pear sits on the rising diagonal and the upper-left stays empty. Crops: the waist was
  clean, but the far pole of A was crumbs.
- **v3.** Pause/resume hysteresis (1.2 mm resume). Line-layer strokes 140 → 101. Dots Ø 2.0.
  Non-breaking spaces in the footer so `t = 0.055` and `∂g/∂t = −2 Ric` never split.
- **v4.** The corner caption now sits on the footer's flush-left axis x = 205, with tracking
  solved so it ends exactly on x = 282. The right side of the sheet now has one text column,
  top and bottom. Dots Ø 1.9 so B keeps 5 mm bare. The "THE CUT" orphan is fixed.

## Measurements / computations

- **Solver re-run** (`run_snapshots.py`, a copy of `data/run_neckpinch.py`):
  - t_s = **0.054646502** (matches the npz 0.0546465023).
  - h_cut = 0.119710, cut index 267 / 400.
  - T_ext_A = **0.387343** (slope −4.0033), T_ext_B = **0.117140** (slope −3.9080). All match
    dossier §7.
  - Snapshot error 0.
- **Alignment.** Pre-surgery lines pin the neck minimum (a parabola through 5 nodes) at u = 0.
  Post-surgery lines hold each piece's ψ²ds centroid at its t_s value: c_A = −1.914, c_B = +1.035
  (u units, cut at u = −0.0046).
  - Cap tips relative to the cut, at 62 mm/u: A is +7.2 mm at t_s, then −11.6 / −24.2 / −31.4 mm
    at t_s + 0.01 / 0.02 / 0.03. B is −7.7 mm at t_s, then +11.9 / +25.8 / +34.7 mm. The caps
    retract fast, and the first future rings sit well clear of the red circle.
- **Occlusion.** This is exact. Vertices are classified by point-in-polygon (matplotlib Path),
  and every in/out transition is cut ON the covering card's edge by a vectorised segment–edge
  intersection. The keyline is never occluded (sacred). Future rings are occluded only by later
  rings of their own piece. Where A's early rings stick out past the next ring or the keyline
  (≤ 0.65 mm), the merge silences them.
- **Floor.** Measured on the final gcode by `audit.py`: minimum 0.837 mm between different line
  strokes, 0 samples under 0.8.

## Plot budget (audit.py on v4 gcode; F600 = 10 mm/s, 2.5 s per lift/drop, travel 50 mm/s)

| layer | pen | strokes | draw | travel | longest | ≈ min |
|---|---|---|---|---|---|---|
| 0 lines | black 0.3 | 101 | 12.91 m | 1.61 m | 734 mm (keyline) | 26.3 |
| 1 type | black 0.3 (own layer) | 972 | 4.82 m | 3.82 m | 95 mm | 49.8 |
| 2 red | red 0.5 | 18 | 0.26 m | 0.77 m | 37 mm | 1.4 |
| total | 1 physical swap | 1 091 | 17.99 m | 6.2 m | | **≈ 77.5** |

Re-zero points fall naturally at the region boundaries: after the halo, after the keyline, and
after B. Type is the time sink: 972 lifts, twice the encoding's estimate.

## Self-critique (seven rubric dimensions)

1. Hierarchy **8**. A's nest dominates at 3 m, the waist with its red circle is second, B is
   third, and the red points are last.
2. Grid & alignment **8**. There are two text axes, x = 15 (title, statement, stamp) and x = 205
   (corner caption + footer + colophon). The title's display tracking leaves a wide word gap
   in THE  POINCARÉ.
3. Tension & asymmetry **8**. The 62° diagonal runs with the heavy mass low-left against the
   light lobe high-right, and nothing is centred.
4. Negative space **7**. The upper-left quiet zone works. The band between the stamp and B
   (y ≈ 300–330) is generous but slightly undecided.
5. Craft for pen **7**. The floor holds, there are no floods, red lands last, and the keyline is
   retraced exactly. The far-pole rim of A is still a shingle of paused dashes. That is honest
   (it is where the geometry stands still), but it is the one passage that reads as texture
   rather than line.
6. Concept / order / twist **8**. One shape splits at a hair-thin waist into two nests, and the
   ring count is the lifetime. The corner line "to prove it is one sphere, the flow cuts it in
   two" lands the twist. There is no CSF loop in this thesis (forbidden in [abstract]).
7. Depth **5**. Flat by declaration. The time-occlusion terraces are real but subtle, and at
   3 m the two "mounds" read more as concentric targets than as relief.

**Single worst thing:** A's far-pole rim (lower-left, around (40–90, 35–80) mm). Rings k = 1–6
and the past lines run at 0.8–1.2 mm, so pause/resume leaves overlapping dashes where a viewer
may expect continuous rings.

## Engine requests

- `generators._stroke_text(..., proportional=True)` advances by `_glyph_advance` but draws each
  glyph at its un-normalised x offset. Narrow glyphs ('i' ink at x = 1.8, advance 1.1) collide
  with the next glyph, which rendered "simply" as "s mply". Fix: shift each glyph by −ink_xmin + ½
  bearing. This piece works around it locally (`_metrics`).
- `geometry.Polygon.inside_intervals` is pure-Python O(segments × edges). Clipping 40 isochrone
  rings against unions of later cards took more than 10 minutes on the loaded machine. A
  vectorised numpy path, or a bbox-tree edge prefilter, would make cover-occlusion of dense
  ring families practical. This piece uses a local vectorised clip.
- `Occupancy` could take an optional `resume_sep` (hysteresis) for `Scene3D.lines(mode="pause_resume")`.
  This piece emulates it with two Occupancy grids.
