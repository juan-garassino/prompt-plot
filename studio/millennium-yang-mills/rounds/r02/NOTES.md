# millennium-yang-mills r02 — abstract (POINT / LINE / PLANE) · parent: none · 2026-09-28

lineage: Wassily Kandinsky, *Punkt und Linie zu Fläche* (Bauhausbuch 9, 1926). Order taken:
point, line and plane as the three elements with weight and direction. Vacuum = point,
one-glueball mass shells = lines, two-glueball continuum = plane. The half-section's light
cone is the one driving diagonal.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-yang-mills/rounds/r02/piece.py \
  --fn yang_mills_point_line_plane --seed 7 --paper a3 --margin 15 \
  --palette darkgray,black,black,black,crimson \
  --out gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_abstract_v7.png
```

- final PNG: `gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_abstract_v7.png`
- final GCODE: `gallery/studio/millennium_yang_mills/current/pp_millennium_yang_mills_abstract_v7.gcode`
- seed 7. The plate is exact data with no randomness: seeds 7, 11 and 23 give byte-identical
  gcode bodies (md5 a2487016… at v6).
- Leo: the same call with `--paper a5 --margin 10` reflows correctly (checked). Strata stay at
  1.0 mm physical pitch (58 strata), and caps stay ≥ 1.8 mm with balanced line breaks.
- Iterations: v1 was the encoding's 5A as written. v2/v3 fixed the type (monospace setter, an
  authored superscript star, and no `(H,|P|)`, which collided in the proportional font). v4
  moved the names to the p < 0 staff and cropped all lines at the frame. v5–v7 covered
  small-paper reflow, title weight, one-stroke red and stroke order.

## Mandate responses

There is no LEDGER.md, FEEDBACK.md or DESCRIPTION.md for this slug, so there are no open J*/A*/S*
mandates. The binding brief is `encoding.md`. Its §9 forbidden list and §11 checks are answered below.

| id | mandate | status |
|---|---|---|
| §11.1 EMPTY TIP | no non-red ink in {p<E<√(p²+1)} | FIXED. The gcode clip over every G1 segment (0.2 mm sampling, disc excluded) finds **0 GHOST / 0 PLANE / 0 TEXT / 0 SPECTRUM** segments. The only hits are 4 RED segments, which are the Δ bar passes at x=40±0.4. |
| §11.2 ONE-TO-ONE | vacuum→0⁺⁺ = 0⁺⁺→rim; cone 45° | FIXED. The vacuum centre is at y=50, the 0⁺⁺ vertex at 150 and the rim vertex at 250, giving 100.0 : 100.0 mm. The ghost measures 45.000°. |
| §11.3 IRREGULAR STAFF | vertices 43.7/55.0/72.0/78.1/85.6 mm above red | FIXED. Computed from the JSON: 43.7, 55.0, 72.0, 78.1, 85.6, rim 100.0. Tightest perpendicular gap is 2.83 mm (0⁺⁺*/1⁺⁻). |
| §11.4 PLANE ON THE RIM | strata start on the rim, none below | FIXED. 120 strata at exactly 1.00 mm pitch, y 251…370. Each ends 0.29 mm (perpendicular) short of the rim through a per-stratum slope-corrected inset. |
| §11.5 NOTHING ON THE CONE | red ≥ 18 mm above the ruling at the stop | FIXED. At the right frame the red sits 19.85 mm above the ghost. There is one red group. |
| §9.1–13 | forbidden list | Honoured. There are no axes, ticks or frame. There is no drawn spine: the spine is implied by the left ends. No MeV, no "proven", one accent, flat by declaration. |
| 5A departure 1 | tags in a right column x∈[265,282] | ARGUED/CHANGED. In the brief's layout, the 0⁺⁺ tag at the red curve's end sits inside the lens's extension (13 TEXT segments failed the §11.1 clip). The names now sit in the p<0 column **at the vertices**, flush-right on x=36. That is where E is the rest mass itself, and it is outside the half-section by construction. |
| 5A departure 2 | shells stop at x=262 | CHANGED. With the tag column gone, every shell, the rim, the strata and the red shell crop **at** the right frame (p=2.42). The plane bleeds off the right edge, and the fan of lines exits the frame instead of stopping short. This is a deliberate crop. The tightest gap at the frame is still 2.83 mm. |

## What changed from parent

There is no parent. This is a new plate built from `encoding.md` §5A. Composition, bottom to top:

- **Point.** The vacuum, a Ø3.0 mm solid disc at (40, 50). It is the only solid mark.
- **Heavy red line.** Kandinsky's line with weight: three passes, ≈1.3 mm, rising from the
  disc edge to the 0⁺⁺ vertex. There it turns 90° and becomes the 0⁺⁺ shell, which runs out to
  the frame. The gap's measure and the gap's edge are drawn as one stroke.
- **The lens.** Blank paper between the red curve and the one grey diagonal (the light cone,
  E = p). The diagonal runs from the point to the right frame and splits the sheet. The
  lower-right triangle is the open spacelike field, the plate's quiet zone.
- **Lines.** Five fine black shells plus the rim, all leaving the spine horizontally and
  leaning into the diagonal at their measured, irregular heights.
- **Plane.** 120 iso-energy strata above the rim. The mass sits in the upper-left, is cut
  flat at E = 3.2 (y = 370) and bleeds off the right edge.
- **Names.** J^PC names (with superscript PC) and `2Δ` form a staff in the p<0 column. The
  red Δ glyph sits on that column mid-gap.
- **Type.** The title (6 mm, 3-pass weight) and statement sit flush-left on the spine. The
  colophon is flush-left on the 15 mm margin. The corner caption is flush-right on the frame
  that the lines crop at.

## Measurements / computations

- Data is read at import from `data/glueball_spectrum.json` and never typed in: M/Δ =
  (M/√σ)/3.405. Drawn shells are 1.4373, 1.5495, 1.7195, 1.7812 and 1.8561, and the code
  asserts these values. The 2⁺⁺* (1.9935) sits 0.65 mm under the rim, below the 0.8 mm floor,
  so it is merged into the rim, and the caption says so.
- Scale: s = 100 mm/Δ on both axes. Spine x=40, vacuum y=50, frame p ∈ [0, 2.42], plane top
  E = 3.20.
- Perpendicular min gaps (A3): 0⁺⁺→2⁺⁺ 14.93 · 2⁺⁺→0⁻⁺ 4.52 · 0⁻⁺→0⁺⁺* 7.40 · **0⁺⁺*→1⁺⁻ 2.83** ·
  1⁺⁻→2⁻⁺ 3.54 · 2⁻⁺→rim 7.12 mm. On A5 (k = 0.479) the tightest is 1.36 mm, still ≥ 0.8.
- Areas (A3, inside the frame): plane 19 006 mm² · lens 10 488 mm² · plane : lens = **1.81**
  (encoding target 1.8). The spacelike field (x ≥ 40) is 37 754 mm².
- Red above the cone at the frame: 19.85 mm. The lens wedge never closes on the sheet.
- The ghost starts 2.3 mm from the disc centre, at the disc edge plus 0.8 mm. It uses 29 dashes
  of 9 mm with 3 mm gaps.

## Plot budget (A3 portrait, 15 mm margin)

Totals: draw 23.5 m and travel 3.96 m. The file has 9 080 commands and 591 pen lifts. It uses
5 layers on 4 physical pens with 3 swaps: TEXT shares the PLANE's 0.2 black and is its own
layer, so it needs no swap. Estimated times use F600 (10 mm/s) plus 2.5 s per pen cycle.

| order | layer | pen | draw | strokes | est. |
|---|---|---|---|---|---|
| 1 | GHOST | grey 0.1 | 0.26 m | 29 | 1.6 min |
| 2 | PLANE | black 0.2 | 19.05 m | 120 (boustrophedon, bottom→top; batch every 20) | 36.7 min |
| 3 | TEXT | black 0.2 (same pen) | 1.89 m | 433 | 21.2 min |
| 4 | SPECTRUM | black 0.3 | 1.71 m | 7 (disc + 6 curves) | 3.1 min |
| 5 | RED | red 0.5 | 0.62 m | 2 (glyph + one bar/shell stroke) | 1.1 min |
| | **total** | | | | **≈ 64 min** |

- Order runs light to dark with red last, so no ink lands on the accent. The red starts
  0.55 mm clear of the black disc.
- Leo A5: draw 7.05 m, about 34 min. TEXT is then the longest layer at 20 min, because it is
  cycle-bound.
- One long travel remains inside TEXT (363 mm, statement → corner caption). The postprocess
  travel optimiser reorders strokes within a colour and overrides authored order; see Engine
  requests.

## Self-critique (rubric, honest)

1. **Hierarchy: 8.** At 3 m the plane is the dominant mass, the red L is second, and the fan
   of lines is third. The point is small by truth.
2. **Grid & alignment: 8.** Title, statement, strata, shells and red bar all start on x=40.
   The names and Δ are flush-right on x=36. The lines and caption share the right frame.
   The colophon sits on the 15 mm margin.
3. **Tension & asymmetry: 8.** One 45° diagonal against a flat-topped mass in the upper-left.
   Lines crop at the frame.
4. **Negative space: 8.** There are two kinds of blank, the enclosed lens and the open
   spacelike field, and they differ by physics. The lower-right is large but shaped by the
   cone.
5. **Craft for pen: 8.** Every spacing is analytic and above the floor. There is one solid
   (the disc) and a deliberate 3-pass bar. Text costs many pen cycles.
6. **Concept legibility: 7.** The empty tip reads, and so does the 1:1. **Single worst
   thing:** with a column of names beside horizontal line-starts, the left edge can still read
   as a labelled spectrum plot (Streater–Wightman) rather than a Kandinsky order. The staff is
   honest, but it is the most "figure-like" element on the sheet.
7. **Depth: 7.** Flat by declaration: the canon is flat and the subject is a plane (§1). Depth
   comes only from weight: the ghost 0.1, the plane 0.2, the lines 0.3, and the red bar.

Also weak: the grey 0.1 ghost is quiet at 3 m, so the lens's lower edge is felt more than
seen. This is intentional (the empty promise), but a critic may call it under-enclosed.

## Engine requests

- `merge_chunks` → `reorder_by_color` re-optimises stroke order within a colour and discards
  the authored, travel-planned order. It leaves greedy-nearest-neighbour tail jumps: 363 mm
  inside TEXT here. A per-piece opt-out would help, such as `GCodeCommand` metadata or a
  `preserve_order` flag on the chunk.
- The stroke font has no Δ or superscript `+`/`-`/`*`. This piece authors Δ, a 6-armed
  superscript star, and superscript placement locally in `set_text()`. They are worth
  promoting to the kit.
