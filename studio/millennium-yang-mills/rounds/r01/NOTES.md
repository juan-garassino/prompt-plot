# millennium-yang-mills r01 — faithful · parent: none · 2026-09-28

lineage: Wassily Kandinsky, *Punkt und Linie zu Fläche* (Bauhausbuch 9, 1926). Order taken:
point, line and plane as the three elements with weight and direction. Vacuum = point,
one-glueball shells = lines, two-glueball continuum = plane. Each is literally the dimension of
that spectral component in the (p, E) plane. Style: BAUHAUS (Kandinsky branch) in the Millennium
series grammar. **Flat by declaration** (encoding §1: the canon is flat and the subject is a set
in a plane).

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-yang-mills/rounds/r01/piece.py \
  --fn yang_mills_mass_gap_faithful --seed 7 --paper a3 --margin 15 \
  --palette darkgray,black,black,black,crimson \
  --out gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_faithful_v10.png
```

- final (A3 portrait): `gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_faithful_v10.png` / `.gcode`
- Leo (A5 portrait, margin 10, same command with `--paper a5 --margin 10`):
  `gallery/studio/millennium_yang_mills/trials/pp_millennium_yang_mills_faithful_v9.png` / `.gcode`
- physical-width preview (each pen at its nib width, cream):
  `studio/millennium-yang-mills/rounds/r01/phys_preview_v10.png`. The stock preview draws every
  pen at one fat width, so the 0.2 mm strata at a 1 mm pitch show as a solid black slab there.
  On paper the plane is about 20 % tone.
- seed: 7. Nothing on the sheet is random. Seeds 7, 11 and 42 give byte-identical gcode.

## Mandate responses

There is no LEDGER.md or FEEDBACK.md for this slug yet, so there are **no open J/A/S mandates**.
The binding brief is encoding.md §4/§9/§11 plus the curator note. Every check was run on the
gcode itself (script: parse G1 per colour, clip against the regions):

| id | requirement | status |
|---|---|---|
| §11.1 EMPTY TIP | no non-red ink in {\|p\|<E<√(p²+1)} | FIXED: 0 ghost / 0 plane / 0 text / 0 spectrum samples (0.2 mm sampling, vacuum disc excluded) |
| §11.2 ONE-TO-ONE | vacuum→red = red→rim ±1 mm, cone 45°±0.5° | FIXED: 100.00 / 100.00 mm; all 38 dashes 45.000° |
| §11.3 IRREGULAR STAFF | 43.7, 54.9, 72.0, 78.1, 85.6 mm above red | FIXED: 43.7, 54.9, 71.9, 78.1, 85.6. Gaps 11.2 / 17.0 / 6.2 / 7.5. Min perpendicular gap 4.04 mm |
| §11.4 PLANE ON THE RIM | strata start on the rim, none below or between shells | FIXED: 110 strata, pitch 1.000, y 261…370. Endpoint→rim 0.282–0.365 mm (inset 0.285). 0 endpoints below the rim |
| §11.5 NOTHING ON THE CONE | red ≥ 18 mm above the ruling at the stop | FIXED: 39.5 mm (left frame), 31.3 mm (x = 266), 28.7 mm (right frame). One red group. Lens enclosed to the frame |
| §9 forbidden list | 1–13 | none present: no axes/ticks/numbers/legend, no MeV, no "proven", no knots, no second accent, no text in the plane |
| curator | the GAP is the visible truth; real data; lineage; plottable layers | real AT2020 spectrum read from `data/glueball_spectrum.json`. The lens is the largest enclosed silence. Lineage named. 5 layers, stated order, minutes below |

## What changed from the reference (faithful = reconstruction plus stated layout fixes)

Kept from the reference: energy runs up the sheet, excitations above, a wide silent middle, the
red I-beam with an interrupting Δ, cream, portrait, fine black line.

The fixes, each one a composition move:
1. **The specimens become the spectrum.** The nested fine-line "specimens" at arbitrary heights are
   replaced by 6 exact hyperbolae at their measured M/Δ plus the 2Δ plane (110 iso-energy strata).
   The nesting is real: every curve shares the cone's asymptotes.
2. **Knots, tori, gold orbits and dotted construction circles are cut** (dossier lie 7). The only
   dashed element left is the cone.
3. **The vacuum band (field lines, bump, ring on a stem) is replaced by one Ø3 mm point.** The
   reference's dotted arcs over the bump become the two ghost rulings rising from it.
4. **The I-beam's ends now touch physics.** The bar starts at the disc edge and ends on the
   red curve's vertex, exactly s = 100 mm centre to vertex. There are no serifs: the disc and
   the curve's horizontal vertex are the stops.
5. **The axis moves off-centre.** The reference is dead-centred at u = 0.500. Here the axis sits
   at x = 122 (u = 0.411), and the crop is asymmetric: the left ruling exits at y = 167 and the
   right at y = 220.
6. **The title moves from bottom-centre (with flanking rules) to top-left** in the series
   grammar. It is spaced caps tracked to span exactly the plane's width [15, 266].
7. **Proportions come from the physics:** gap : isolated band = 1 : 1, where the reference has
   about 0.6 : 1 at random.

Decisions beyond the encoding (argued):
- **The red 0⁺⁺ runs frame to frame** (x 15→282), while the black shells stop at x = 266 for the
  tag column. It is the lens's upper edge, so the silence stays enclosed out to the frame, and
  the longer line gives the accent more weight. Its tag perches on it, with the baseline 0.6 mm
  clear of √(p²+1) at the tag's right end. A tag centred on the curve's end (v2–v3) put 52 text
  samples *inside* the lens, because the lens runs past where the curve stops. Rotated tags (v5)
  and "every tag on its continuation" (v4) both detached the names from their lines.
- **The Δ glyph is 8.4 mm, not the encoding's 12 mm.** 8.4 mm is the measured reference
  proportion (0.0199 H). The bar break is ±8.7 mm (measured 0.0207 H). The glyph's right leg is
  weighted by 2 extra red passes at 0.4 mm inward offset, trimmed exactly to the base and the
  left leg, which gives it the reference's Didone thick stroke.
- **The corner captions are bottom-aligned on the frame (y = 15),** not at y ∈ [18, 48]. This
  gives the vacuum 27 mm of its own silence below it.
- **Type fixes, local to the piece:** the zero loses its slash (a slashed 0 beside J^PC tags
  reads as ∅ on a plate about emptiness). The 5-spoke asterisk replaces the 6-spoke one, which
  read as "+" at superscript size. Δ is authored as a glyph. Glyphs are drawn from their own ink
  origin (the house proportional advance measured the ink but drew at the cell offset, which
  detached commas and swallowed spaces after ")").
- **Small-paper adaptation.** Pitches and caps are physical (strata 1.0 mm, inset 0.285 mm,
  dash 6/4 mm, disc 3 mm, caps ≥ 1.8 mm), so the geometry scales and the pitch never does. On A5
  (k = 0.479), 53 strata are drawn and the tag stack relaxes upward in order, ≥ 0.5 mm apart.
  The statement breaks at its sentence. The captions become one run-in block under the frame,
  because the two corners cannot hold them at a 1.8 mm cap.

## Measurements / computations

Measured on the reference (1122 × 1402 px) with colour masks and row/column scans. Coordinates
are normalised (u right, v down):
- red I-beam: bar u = 0.500 (2 px stroke), serifs u 0.487–0.513 (8.0 mm at A3 width), top v 0.4608,
  bottom v 0.6940 → **0.2332 H = 97.9 mm on an A3 height**, which is the encoding's s = 100 mm/Δ.
- Δ glyph: v 0.5678–0.5877 = 0.0199 H = **8.4 mm**, centred at the bar's midpoint (v 0.5774).
- bar break: v 0.5563–0.5977 → **±8.7 mm**.
- specimen cluster: v 0.017–0.445, ink centroid (0.500, 0.214), 2.5 % ink coverage.
- silent middle: v 0.445–0.741 (0.296 H). Vacuum band: v 0.741–0.929, u 0.020–0.979.
- title: v 0.942–0.954, u 0.407–0.647, centred, lowercase serif, letters about 4.8 mm tall.

Computed (units of Δ = M(0⁺⁺) = 3.405 √σ, AT2020 continuum limit, read from the json):
- vertices: 1, 1.4373, 1.5495, 1.7195, 1.7812, 1.8561, 2 (rim). The 2⁺⁺* (1.9935) is merged
  into the rim (0.65 mm below it) and declared in the caption. Embedded states above 2Δ are
  omitted and declared.
- shells E = √(p²+M²), sampled every 0.4 mm of x, p ∈ [−1.07, 1.44] (red: [−1.07, 1.60]).
- strata stop where the perpendicular distance to the rim equals 0.285 mm: y − rim(x) =
  d·√(1+rim′²), solved by bisection on each branch.
- 0⁺⁺ above the cone at the stops: √(p²+1) − |p| = 0.395 (p = −1.07), 0.313 (p = 1.44),
  0.287 (p = 1.60).

## Plot budget

A3 (v10): 28.18 m drawn, 4.36 m travel, 9,172 commands, 606 pen lifts, 5 colour layers on 4 inks
(3 swaps: plane and text share the black 0.2 with no swap). At Leo's F600 ≈ 10 mm/s plus
2.5 s per pen cycle:

| order | layer | pen | draw | strokes | ≈ min |
|---|---|---|---|---|---|
| 1 | GHOST light cone | grey 0.1 | 0.23 m | 38 | 2 |
| 2 | PLANE continuum | black 0.2 | 24.35 m | 110 | 45 |
| 3 | TEXT | black 0.2 (no swap) | 1.52 m | 445 | 21 |
| 4 | SPECTRUM point + 5 shells + rim | black 0.3 | 1.64 m | 7 | 3 |
| 5 | RED 0⁺⁺ + Δ bar + glyph | red 0.5 | 0.43 m | 6 | 1 |
| | **total** | | | | **≈ 72 min** |

A5 (v9): 7.98 m drawn, 2.56 m travel, ≈ 35 min. Text dominates there (445 pen cycles).
Batching: every stratum and every shell is one stroke. Shells alternate direction bottom→top, so
consecutive strokes are neighbours. The long travels are only the 4 text-block jumps and the
layer changes. Batch boundary every 20 strata for re-zero checks.

## Self-critique (rubric, honest)

1. Hierarchy **7**: the plane slab dominates at 3 m, the red U is second, the shells third, and
   the tags and captions reward 30 cm. The 8.4 mm Δ glyph is quiet at 3 m.
2. Grid & alignment **8**: the frame x = 15 holds the title, statement, captions, and shell and
   strata crops. The x = 122 axis holds the disc, bar, glyph and every vertex. The x = 266 stop
   holds the title's right edge, strata, shells and rim. The tag column is at 269. Captions sit
   on the bottom frame line.
3. Tension & asymmetry **6**: the axis is off-centre and the V is cropped asymmetrically, but the
   hyperbola family is still a broad, near-symmetric U. The encoding fixes the geometry, so there
   is little room.
4. Negative space **8**: two different silences. The enclosed lens (the gap) and the open
   spacelike field, plus the band under the vacuum.
5. Craft for pen **8**: nothing under 4.0 mm between curves, strata 1.0 mm, one solid on purpose
   (the disc), red never touches black.
6. Concept legibility **6**: the empty tip lands at 1 m once the cone is seen. The risk is that a
   critic reads a hyperbola family in a V as the Streater–Wightman textbook figure even without
   axes.
7. Depth **7 (declared flat)**.

**Single worst thing:** the twist depends on the light cone, and the cone is the faintest mark on
the sheet (0.1 grey dashes). At 3 m the viewer sees a U over a dot, not "the light cone, empty".
The encoding fixes the ghost pen, so it is kept. A darker ghost (0.2 grey) is the lever a critic
might ask for.

## Engine requests

- `scripts/render_candidate.py` has no `--pen-widths` pass-through to
  `GCodeVisualizer.preview(pen_widths=)`. Every plate with a fine-pitch fill reads as a black
  flood in the review PNG. I worked around it with a local PIL physical preview saved in the
  round directory.
- The proportional `_stroke_text` path draws each glyph at its cell offset while advancing by
  its ink width, which detaches punctuation. I worked around it locally with a re-origin.
