# millennium-hodge r03 — iterate · parent: r02 · 2026-09-29

lineage: Naum Gabo, *Linear Construction in Space No. 1* (1942–43, Tate T00191). Order taken: a
curved surface made only of straight strings, with a void bounded by their envelopes. Here the
strings are the algebraic cycles and the void is the see-through throat. (Man Ray, *Objets
mathématiques*, 1936, stays in notes only; Mohr is not used.)
Style: Constructivism, Gabo/Pevsner spatial branch — diagonal thrust against counter-thrust.

An earlier, interrupted session of this seat left a `piece.py` and `_iterate_v1` here, with no
NOTES and no survey (its docstring cited a `survey.py` that did not exist). I kept its machinery
(asymmetric slab, monotone stagger, 7-pass X, bracketed rebus, superscript setter, new key
words) and did the survey for real: `survey.py`, below.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-hodge/rounds/r03/piece.py \
  --fn hodge_circle_is_two_lines --seed 7 --paper a3 --margin 15 \
  --palette darkgoldenrod,royalblue,darkgreen,black \
  --out gallery/studio/millennium_hodge/current/pp_millennium_hodge_iterate_v4.png
```

- final A3 portrait: `gallery/studio/millennium_hodge/current/pp_millennium_hodge_iterate_v4.png` / `.gcode`
- physical-width preview (each pen at its nib width, cream): `rounds/r03/phys_preview_v4.png`
  (the stock preview draws the 0.2 mm strings ~3× too heavy)
- Leo A5 portrait, margin 10: `gallery/studio/millennium_hodge/current/pp_millennium_hodge_iterate_v5_a5.png` / `.gcode`,
  preview `rounds/r03/phys_preview_v5_a5.png` (same command, `--paper a5 --margin 10`)
- seed 7. Nothing is random: seed 3 gives a byte-identical gcode (diff 0 lines).
- trials: v1 (inherited: e48/357/roll −10, centred, cropped left+right), v2 (roll −20 shoved
  right — the blue went flat at 12° and the rebus slant read as a minus sign), v3 (roll −14,
  3 mm stagger step), v4 (comma glyph fix — `h^{2,0}` read as `h^{2.0}`), v5 A5.
- re-run the checks: `.venv/bin/python studio/millennium-hodge/rounds/r03/audit.py <gcode>`
  and `.venv/bin/python studio/millennium-hodge/rounds/r03/survey.py [coarse|wide|fine]`.

## Mandate responses

| id | mandate | status |
|---|---|---|
| A1 | unbroken, two-armed, heaviest X; crossing 70–110° | **PARTLY FIXED, angle ARGUED (not met).** Unbroken: gold [B] is ONE run, 212.5 of 212.5 mm, rim (130.2, 212.2) → rim (268.6, 51.0); blue [A] ONE run, 205.0 of 205.0 mm, rim (30.7, 120.3) → rim (225.3, 184.5); 0 gaps (audit §4). Blue : gold = 0.965 (≥ 0.8). Heaviest: both are 7 passes of the 0.2 nib at 0.15 mm (≈ 1.1 mm band) vs the 0.5 green; blue now has exactly the gold's passes. **Angle 67.59° — FAILS 70°.** It cannot be reached: in orthographic projection the on-sheet X angle depends only on hinge and elevation (not slab, roll, crop, k). In the 330–360 window at e 48–56 its maximum is 69.2° (hinge 330, e 48). Over **every** hinge 0–360 at e 48–56, the largest angle with blue : gold ≥ 0.8 is **68.18°** (e 48, hinge ≈ 342); 70° needs hinge ≤ 320 at e 48, where blue : gold ≤ 0.57 (the r01 stub). The two A1 clauses are jointly unsatisfiable above e 48; below 48 is the 45° degeneracy margin. 67.59° is 0.6° under the attainable maximum. **This is the rule-2 trigger in SYNTH: route to translator to re-state §11.4(A) as ≥ 65° or trade the arm ratio.** |
| A2 | circle ≥ 85 %, no gap > 8 mm; 31.72° ellipse visibly grazes the bottom rim | **FIXED.** Waist circle drawn 97.7 % of its full length; its only gaps are the true occlusions at the two eye tips, largest 3.9 mm. The 31.72° ellipse's z = −2.000000 vertex is visible and drawn at (195.9, 227.6): seen through the throat, it lies on the eye's upper edge, where the back of the bottom rim's string ends make the envelope; the green arc runs (166, 234) → (205, 225). The bottom rim is fully inside the frame (lowest string end y ≈ 22). Only the right frame crops |
| S1 | green never cut by strings; stagger strictly decreasing | **FIXED.** Audit §6 recomputes each member independently: 0 mm of visible green is undrawn outside the stagger stretch at p, for all six members. Strings yield to green (green is laid first; strings only lose > 3 mm near-parallel shadow). Stops from p (L/R, mm): 15° 31.6/31.8 · 31.72° 28.6/28.5 · 45° 25.1/25.4 · 60° 12.0/12.1 · 75° 8.5/8.6 — strictly decreasing, ≥ 3 mm steps (natural stops 30.6, 20.1, 25.1, 12.0, 8.5; a lower-ψ member is only ever shortened) |
| A3 | clean lips, no blue/gold fragment < 8 mm | **FIXED on the criterion.** Gold: 172 strokes, shortest 9.88 mm; blue: 174, shortest 8.87 mm; 0 under 8 mm (MIN_RUN 8 at LOD). Lips re-measured in the new view: left tip ≈ (118–135, 205–232), right tip ≈ (232–262, 180–205). The r02 lone dash is gone. Residual (honest): at the left tip several strings end within 3 mm of one another where they pass behind the tip, so it still reads as a small fan of ends, not a knot of stubs |
| S2 | honest words | **FIXED.** Rebus `[○] = [╱] + [╲]` with the same bracket form as the tags, slants copying the X (+18.26°, −49.34°). Key: "GREEN: THE CURVES CUT BY PLANES TURNING ABOUT THE TANGENT LINE AT THE CROSSING. EACH ONE, CIRCLE TO X, IS [A]+[B]. HERE h^{2,0}=0: EVERY CLASS IS A HODGE CLASS, AND ALL ARE BUILT FROM [A] AND [B]." The window is stated: "IN THE SLAB −2 ≤ Z ≤ 0.8". RATIONAL ×2, PROJECTIVE, THEOREM (LEFSCHETZ 1924), REAL DIMENSION 8, CANNOT BE DRAWN all kept. The comma glyph was re-authored (hooked tail) so `h^{2,0}` no longer reads `h^{2.0}` |
| C1 | genuine-cycles row | ARGUED (ledger, unchanged): lives in r01, the faithful flavour; S2's bridge line carries the fact here |
| C2 | minutes per layer from `plot plate --dry-run` | **FIXED** (see Plot budget). Note: the plate job itself caps draw feed at 500 mm/min and dwell ≥ 1 s, so the file's F2200 never streams |

## What changed from parent (composition)

- **The slab is cut to −2 ≤ z ≤ 0.8.** The top rim is the lip that severed both X strings in r02.
  Lowering it removes the occluder, so both index-0 strings are visible rim to rim. The upper
  lobe (r02's "single worst thing", 40 % of the sheet carrying nothing) shrinks to a cap.
- **View e 50 → 48, hinge 350 → 357.** At e 48 the graze vertex of the 31.72° ellipse faces the
  viewer through the throat; hinge 357 keeps blue : gold at 0.965.
- **Roll 0 → −14 and the construction moves up off the bottom frame.** It is shoved against the
  right frame, which crops the lower lobe's right flank. The whole bottom rim is on paper. The
  8 now leans; the gold X falls at −49° as the thrust to [B], and the blue rises at +18° from [A]
  as the counter-thrust.
- **k 60 → 62** keeps the eye ≥ 45 mm (0.731 unit tall at this slab).
- **The paper L is kept.** The title and rebus share the top band. The question, key and honesty
  blocks stack flush-left at x = 15, each placed on bare paper by the exact see-through test. A
  large quiet field now opens top-right, between the rebus and the cap.
- Tags never land in the eye: a new exact `View.in_eye` predicate (the sight-line runs inside the
  quadric at z = 0) guards the tag placement. Both tags sit at bottom-rim ends on bare paper.

## Measurements / computations

**Survey** (`survey.py`; exact ray–quadric visibility; unit screen coordinates → mm at k 62).
The criteria are X gap-free (A1), angle ≥ 70, circle ≥ 85 % with no gap > 8 mm, pinch from both
sides, graze vertex visible, and eye ≥ 45 mm.

| H_top | hinge | e | X gap blue/gold mm | angle ° | blue:gold | circle % / max gap mm | pinch | graze | eye mm | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.0 | 350 | 50 | 14.8 / 14.7 | 65.6 | 0.87 | 89.9 / 17.4 | yes | no | 50.8 | r02 |
| 2.0 | 330 | 48 | 6.8 / 8.5 | 69.2 | 0.68 | 94.2 / 9.9 | yes | no | 39.7 | |
| 1.0 | 357 | 48 | 0.4 / 1.0 | 67.6 | 0.97 | 97.1 / 4.9 | yes | yes | 43.1 | |
| 0.9 | 357 | 48 | 0 / 0.25 | 67.6 | 0.97 | 97.4 / 4.4 | yes | yes | 44.2 | |
| 0.85 | 357 | 48 | 0 / 0 | 67.6 | 0.97 | 97.6 / 4.2 | yes | yes | 45.3 | last gap-free H_top |
| **0.8** | **357** | **48** | **0 / 0** | **67.59** | **0.965** | **97.7 / 3.9** | **yes** | **yes** | **45.3** | **chosen** |
| 0.8 | 360 | 50 | 0 / 0 | 65.5 | 1.00 | 96.1 / 6.8 | yes | no | 53.9 | |
| 0.8 | 330 | 48 | 0 / 1.5 | 69.2 | 0.68 | 97.7 / 3.9 | yes | no | 45.3 | |
| 0.7 | 355 | 52 | 0 / 0 | 63.3 | 0.95 | 95.1 / 8.6 | yes | no | 63.9 | |
| 0.5 | 330 | 48 | 0 / 0 | 69.2 | 0.68 | 98.6 / 2.5 | yes | yes | 50.8 | max angle in window |
| 0.4 | 320 | 48 | 0 / 0 | 70.3 | 0.57 | 98.8 / 2.0 | yes | yes | 53.3 | outside the window; blue a stub |
| 0.3 | 315 | 48 | 0 / 0 | 70.9 | 0.52 | 99.1 / 1.5 | yes | yes | 55.2 | outside the window |

- The angle depends on (hinge, e) only. At e 48: hinge 360 67.6°, 345 68.0°, 330 69.2°, 315
  70.9°, 300 72.1°. It falls with e: 50 → 65.5°, 52 → 63.2°, 56 → 58.4° at hinge 360.
- The blue : gold projected length ratio at e 48: 360 1.00, 357 0.965, 345 0.83, 342 0.80,
  340 0.78, 330 0.68, 320 0.57.
- Roll and crop were surveyed on renders after the view was fixed:
  - roll −10, centred: both frames crop and the sheet is static;
  - roll −20, shoved right: the blue went to 12° and the rebus read `[—]`;
  - **roll −14, cx 184, cy 210: chosen.**
- **Exactness (the in-piece asserts run on every render):**
  - Pencil points lie on x²+y²−z²=1 to < 1e-12 and on their planes to < 1e-9.
  - Every blue/gold stroke is one 2-point G1 with 0.0000 mm deviation.
  - The graze vertex has z = −2.000000.
  - p = (169.72, 166.14) is the exact projection of (cos 357°, sin 357°, 0). The circle, both X
    strings and the staggered members all pass through it.
- **Spacing:** the minimum near-parallel gap between different strokes is gold 0.86 mm, blue
  0.85 mm, green 1.26 mm, all ≥ 0.8. (r02 had 0.78/0.79.)
- **Eye:** 4 315 mm², 123.9 × 45.8 mm (long × thick), vertical extent 52.5 mm, 0 ink samples.
- **Type clearance to construction ink (mm):**

  | block | question | key | honesty | statement | title | rebus |
  |---|---|---|---|---|---|---|
  | clearance | 78.7 | 8.8 | 29.3 | 93.1 | 87.3 | 74.9 |

- **Visible string length before LOD:** 32.4 m. Green on the sheet: 1.54 m.

## Plot budget

From `.venv/bin/python -m promptplot plot plate <gcode> --layers 0,1,2,3 --batch-strokes 40
--dry-run`. The job caps the draw feed at ≤ 500 mm/min with dwell ≥ 1 s, uses F2000 travel, and
allows 90 s per pen swap. The file's F2200 is never what streams.

| order | layer | pen | strokes | draw | A3 min | A5 strokes | A5 min |
|---|---|---|---|---|---|---|---|
| 1 | GOLD | ochre pigment fineliner 0.2 | 179 | 15.56 m | 38 | 140 | 14 |
| 2 | BLUE | ultramarine fineliner 0.2 | 181 | 15.36 m | 38 | 138 | 14 |
| 3 | GREEN | deep green 0.5 | 17 | 1.64 m | 5 | 15 | 2 |
| 4 | TEXT | black 0.3 | 875 | 4.36 m | 40 | 875 | 35 |
| | total | 4 pens, 3 swaps | 1 252 | 36.9 m draw, 9.9 m travel, 12 898 commands | **~126** | | **~72** |

The pen-up frame trace comes first. Every string is a single straight G1, so any stroke can be a
batch boundary.

## Self-critique (seven dimensions)

| dimension | score | why |
|---|---|---|
| Hierarchy | 8 | The X is now the heaviest mark at 3 m in both colours. Green pinches onto its crossing, and the weave recedes |
| Grid & alignment | 7 | Everything is flush-left on x = 15; title and rebus share one band. The key's top (291.5) comes from the paper test, not a grid step |
| Tension & asymmetry | 8 | The leaning 8 is shoved into the right frame, the gold falls as the thrust, and the paper L pushes back |
| Negative space | 7 | The eye is clean, and the new top-right field is shaped by the cap. The left eye tip is still a small fan of string ends |
| Craft for pen | 8 | Single-G1 strings, ≥ 0.85 mm spacing, 0 crumbs < 8 mm. The text layer is 40 of 126 minutes |
| Concept legibility | 7 | Closed circle through p, pencil order visible in the stagger, graze on the eye edge, and the rebus as classes. The graze is legible only if you know where to look |
| Depth | 8 | Exact hidden lines, and the back of the bottom rim is seen through the throat |

**Single worst thing:** the X crossing angle is 67.6°, not ≥ 70°. It is provably unreachable
while blue : gold stays ≥ 0.8 at e ≥ 48, and the plate still fails that clause of A1.

## Engine requests

- None new. (r02's request stands: a "keep authored order within a colour" flag on the render
  reorder.)
