# millennium-yang-mills r03 — iterate (de-chart r02: point / line / plane first) · parent: r02 · 2026-09-29

lineage: Wassily Kandinsky, *Punkt und Linie zu Fläche* (Bauhausbuch 9, 1926). The order taken is
point, line and plane as the three elements, each with weight and direction:
- vacuum = point;
- one-glueball mass shells = lines;
- two-glueball continuum = plane.

The plate is flat by declaration: the canon is flat, and the subject is a set in the (p, E) plane.
The lineage is also printed on the sheet, as the last colophon line
("AFTER KANDINSKY, PUNKT UND LINIE ZU FLAECHE, 1926.").

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-yang-mills/rounds/r03/piece.py \
  --fn yang_mills_point_line_plane_r03 --seed 7 --paper a3 --margin 15 \
  --palette darkgray,black,black,black,crimson \
  --out gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_iterate_v7.png
```

- final PNG: `gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_iterate_v7.png`
- final GCODE: `gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_iterate_v7.gcode`
- physical-width preview (each pen at its nib width on cream, 5 px/mm):
  - `gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_iterate_v7_phys.png`
  - the same image at `studio/millennium-yang-mills/rounds/r03/phys_preview_v7.png`
  - nibs used: 0.1 grey, 0.2 black for PLANE and TEXT, 0.3 black, 0.5 red.
- seed 7. Nothing on the sheet is random. Seeds 7, 11 and 23 give byte-identical gcode bodies
  (md5 a5c6aabc…).
- Leo reflow: the same call with `--paper a5 --margin 10` produces
  `gallery/studio/millennium_yang_mills/trials/pp_millennium_yang_mills_iterate_v6.png` / `.gcode`.
- Iterations:
  - v1: first build.
  - v2: floor on the spiral pitch; the missing `;` glyph swapped for `.`.
  - v3: dash pattern fitted to end on the crop; red start put exactly on the disc edge.
  - v4: A3 unchanged. v5 is the A5 reflow, whose superscript lines word-wrap badly.
  - v6: A5 fixed (segs word-wrap; colophon widened so it clears the point; plane crop drops on
    small paper).
  - v7: final A3.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | vacuum as a Ø 9–10 mm solid point | **FIXED.** One Archimedean spiral in the 0.3 black: 10 turns at a realised **0.460 mm** pitch, closed by one circle. Ink Ø **9.50 mm**, centre measured in the gcode at **(40.000, 50.000)**. The red bar's ink starts 0.05 mm above the disc's ink top (path y 55.05), so red touches the edge and never overprints the black. The first ghost dash starts on the disc edge (r = 4.79). **1 : 1 is untouched**: centre 50 → red vertex 150.000 → rim vertex 250, which is 100 : 100 mm. The disc is 9.5 mm against the 1.3 mm bar, i.e. **7.3×** the bar width (≥ 4×). |
| A2 | tags off the spine, one crop x = 262, tags in [265, 282] | **FIXED.** Measured max x per layer: GHOST, PLANE, SPECTRUM and RED all end at **262.00**; only TEXT goes further (280.87, the right frame). Text points at x < 40 with y 140–260: **0**. The tags are flush-left at x = 265, and each ink block is centred on its own line's end height. Decoded from the gcode: 2⁺⁺ 314.47 · 0⁻⁺ 320.73 · 0⁺⁺* 330.81 · 1⁺⁻ 334.62 · 2⁻⁺ 339.37 · 2Δ 348.80. Each equals √(2.22² + M²) to 0.01 mm, and the stacker moved nothing on A3. The tightest block gap is 1.17 mm (0⁺⁺*/1⁺⁻). The 0⁺⁺ has no tag; the red Δ glyph (left column, mid-gap) and the caption name it. There is no comb at the frame, because every line stops 20 mm short of it. |
| A3 | cone 6 mm dash / 4 mm gap, first dash at the disc edge | **FIXED.** 31 dashes at **6.053–6.067 mm**, gaps **4.031–4.045 mm** (±0.1). One common ×1.009 stretch makes a whole dash end exactly on the crop at (262, 272). All dashes measure 45.0000°. |
| A4 | concept legibility ≥ 7, not the textbook figure | **ARGUED / tracking.** A1 and A2 are the instruments, and both are done. Nothing on the sheet reads as an axis any more: there is no tag stack on the spine, and every line stops at one crop. The caption also literally says POINT / LINE / PLANE, and the lineage is on the sheet. What remains figure-like is the right-hand direct labelling (the J^PC names at the line ends), which the mandate itself prescribes. The critics must judge whether it holds. |
| A5 | physical-width preview every round | **FIXED.** See the `_phys.png` paths above. |
| A6 | Δ glyph apex knot | dropped in LEDGER (r01 only). The glyph here is one closed stroke. |
| A7 | strata/rim tangency near the vertex (x 40–57) | **DEFERRED.** The 0.29 mm perpendicular inset (encoding §4) is kept. The first stratum runs within 0.8 mm of the rim for ≈ 8 mm (x 49–57), and the second for ≈ 5 mm. Removing this means either a blank strip (§11.4 FAIL) or non-horizontal strata (§7 FAIL). |
| A8 | axis to x ≤ 85 | dropped in LEDGER (superseded by the half-section). |
| S1 | name the carriers in the corner caption | **FIXED.** The bottom-right block, flush-right on 282, y 18–43, lies wholly in the spacelike void, 150 mm below the cone. It reads: "THE POINT: THE VACUUM." / "EACH LINE: ONE GLUEBALL, ITS MASS THE HEIGHT OF ITS LEFT END." / "RED LINE: THE LIGHTEST GLUEBALL 0⁺⁺, MASS Δ." / "RULED PLANE: EVERY PAIR OF GLUEBALLS, FROM EXACTLY 2Δ." "GLUEBALL" and "PAIR" are both present. |
| S2 | the twist in the statement | **FIXED.** The statement is three lines under the title, flush-left on the spine, with baselines 388 / 383.7 / 379.4 and the plane top at 370: "CLASSICAL YANG-MILLS WAVES RUN AT LIGHT SPEED, ON THE DASHED LINE." / "THE QUANTUM THEORY PUTS NO STATE THERE: NO MASSLESS GLUON, ONLY MASSIVE GLUEBALLS." / "THE CONE HOLDS ONLY ITS TIP, THE VACUUM. THEN NOTHING, UP TO Δ." It contains no "proven" and no MeV. |
| S3 | superscripts ≥ 1.3 mm, sign gap ≥ 0.8 mm, 3-stroke star | **FIXED.** The signs are authored, not taken from the font. Decoded from the gcode: every `+` is **1.32 × 1.32 mm** (2 strokes), every `−` is **1.32 mm** (1 stroke), and `*` is a **3-stroke** star of Ø 1.32. The ink-path gap between signs is **1.00 mm**, which leaves 0.80 mm clear at the 0.2 nib. The J digit is 2.2 mm; the superscript sits raised 0.6 cap with a 0.25 mm kern. The caption's 0⁺⁺ and 2⁺⁺* use the same setter (1.3 mm at the 1.8 mm cap). The zero is slashless (r01). |
| S4 | "LIES ON 2Δ WITHIN ERRORS" | **FIXED.** Caption: "2⁺⁺* LIES ON 2Δ WITHIN ERRORS. STATES ABOVE 2Δ OMITTED." |

## What changed from parent

This round moves composition, not parameters.

- **The point is a point.** r02's Ø 3 foot-of-the-bar dot is now a 9.5 mm full stop at the
  cone's tip. It is the third weight on the sheet, set against the plane (upper-left) and the red
  L. Kandinsky's triad now reads bottom-left → top-left as point, line, plane.
- **The spine is no longer a scale.** The six names left the spine for a gutter at the line
  ends. The spine keeps only what the physics puts there: the red bar (Δ itself) rising from the
  point, and the left ends of the lines and strata.
- **One crop.** Everything (lines, rim, red, strata, cone) ends on one implied vertical at
  x = 262. The plane becomes a clean mass: flat top at 370, vertical right edge at 262, and the
  rim curve beneath. The frame comb is gone, and the tags live in the 20 mm between the crop and
  the frame.
- **The sheet talks.** The statement moves from a single poetic line to the twist in three
  lines. The corner caption names the four carriers, and the colophon ends on the lineage.
- **Unchanged:** scale, spine, every exact curve, the empty lens, layer order and pens.

## Measurements / computations

- Data is read at import from `data/glueball_spectrum.json`: M/Δ = (M/√σ)/3.405, with asserted
  values 1.4373, 1.5495, 1.7195, 1.7812, 1.8561. 2⁺⁺* (1.9935) is merged into the rim, 0.65 mm
  under it, and declared.
- Scale s = 100 mm/Δ on both axes. Spine x = 40, vacuum y = 50, crop p = 2.22, plane top E = 3.20.
- Min perpendicular gaps within the crop (A3):
  - 0⁺⁺→2⁺⁺ 16.18
  - 2⁺⁺→0⁻⁺ 4.86
  - 0⁻⁺→0⁺⁺* 7.95
  - **0⁺⁺*→1⁺⁻ 3.02**
  - 1⁺⁻→2⁻⁺ 3.78
  - 2⁻⁺→rim 7.61 mm
- Red above the cone at the crop is **21.48 mm** (≥ 18).
- Areas inside the crop: plane 18 732 mm², lens 10 074 mm², so **plane : lens = 1.86** (target 1.8).
- §11.1 lens clip. Every G1 segment was sampled at 0.2 mm, with the disc excluded and 1e-4 mm
  tolerance on the cone:

  | layer | strokes in the lens |
  |---|---|
  | GHOST | 0 |
  | PLANE | 0 |
  | TEXT | 0 |
  | SPECTRUM | 0 |
  | RED | 1 (the Δ bar, allowed) |

- Strata: 120 at 1.000 mm pitch, y 251…370, each ending 0.29 mm (perpendicular) off the rim,
  x ≤ 262.
- Tags: the gutter floor is set 1 mm above the lens continuation (red evaluated at the widest
  tag's far edge). The 2⁺⁺ tag bottom is at 313.15.

## Plot budget (A3 portrait, 15 mm margin)

Totals from the gcode:
- draw **24.65 m**, travel **5.22 m**;
- **13 088** commands and **1 087** pen lifts;
- 5 layers on 4 physical pens, **3 swaps**.

TEXT shares the PLANE's 0.2 black, as its own layer. Estimates use F600 (10 mm/s) plus 2.5 s per
pen cycle.

| order | layer | pen | strokes | draw | est. |
|---|---|---|---|---|---|
| 1 | GHOST | grey 0.1 | 31 dashes, apex outward | 0.19 m | **1.6 min** |
| 2 | PLANE | black 0.2 | 120 strata, boustrophedon bottom→top, batch every 20 | 18.77 m | **36.3 min** |
| 3 | TEXT | black 0.2 (same pen, own layer, no swap) | 927 | 3.42 m | **44.3 min** |
| 4 | SPECTRUM | black 0.3 | 7 (disc spiral + 5 shells + rim) | 1.68 m | **3.1 min** |
| 5 | RED | red 0.5 | 2 (Δ glyph; one bar + 0⁺⁺ stroke) | 0.59 m | **1.1 min** |
| | **total** | | | | **≈ 86 min** |

- The order runs light to dark with red last, so nothing inks over the accent. Red meets the
  disc 0.05 mm clear of its ink.
- TEXT went from 433 cycles in r02 to **927**. That is the price of S1, S2, S3 and the lineage:
  the naming caption, the three-line twist and the authored signs. It is cycle-bound
  (≈ 38.6 of its 44 min are pen cycles). With no pen cap it is accepted, but it is now the
  longest layer.
- Leo on A5 (v6): draw 7.16 m, TEXT 43.3 / PLANE 7.4 / other 3.0, for ≈ **54 min**. On A5 the
  plane top drops to clear the 6-line wrapped statement: 48 strata at 1.0 mm physical, with caps
  held at 1.8 mm.

## Self-critique (rubric, honest)

1. **Hierarchy: 8.** At 3 m the order is plane, then the red L, then the black full stop, then
   the fan. The point now holds its own weight.
2. **Grid & alignment: 8.** These all share the spine at x = 40: title, statement, strata,
   shells, red bar and point. The one crop at 262 aligns every right end, and the tags hang on
   265. Caption and colophon share the 18 mm baseline. The colophon sits on the 15 mm margin,
   off the spine grid (inherited).
3. **Tension & asymmetry: 8.** One 45° diagonal against a flat-topped mass in the upper-left. The
   lens tapers into a wedge that stays open at the crop.
4. **Negative space: 8.** The enclosed lens and the open spacelike field are two different
   silences. The lower-right field is large, and only the caption block lives in it.
5. **Craft for pen: 7.** Every spacing is analytic and above the floor, the disc is the one
   intended solid, and the dash pattern is fitted. TEXT is now 927 pen cycles (44 min).
6. **Concept legibility: 7 (hoped).** The words name point, line and plane, and the twist is
   stated. The J^PC gutter is still the most figure-like element: direct labels at line ends are
   what a good chart does.
7. **Depth: 6–7.** Flat by declaration. Weight is the only depth: ghost 0.1 < plane 0.2 < lines
   0.3 < red bar.

**Single worst thing:** the bar grows straight out of the 9.5 mm disc, so the pair can still read
as "a lollipop / pin" (a point on a stem, cf. §9.5 spirit). The mandate asks for the bar to
start at the disc edge, so the join is by design. If the art critic still reads "stem", the next
lever is a visible ≥ 3 mm gap between the disc and the bar's foot, which would make 1 : 1 a
measured interval rather than a drawn contact.

Also weak:
- The 0.1 grey cone is quiet at 3 m, so the lens's lower edge is felt more than seen.
- The 7-line corner caption is dense at 1.8 mm caps.

## Engine requests

- `scripts/render_candidate.py`: add `--pen-widths` (→ `GCodeVisualizer.preview(pen_widths=)`).
  This round used a local PIL rasteriser again, the third plate in a row to do so.
- Kit: promote authored superscript signs (≥ 1.3 mm, fixed physical sign gap, 3-stroke `*`) and
  a Δ glyph. The font's `+`/`*` collapse at superscript size.
- The `;` glyph is missing from the stroke font (silently dropped).
- `reorder_by_color` still discards authored stroke order inside TEXT. The longest travel is
  353 mm.
