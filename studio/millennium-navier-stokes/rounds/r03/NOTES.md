# millennium-navier-stokes r03 — iterate (merge of r02 code + r01 wording) · parent: r02 · 2026-09-29

Lineage: **Bridget Riley, *Blaze 1* (1962), National Galleries of Scotland.** The order taken is one line family at constant spacing, whose curvature drift alone makes the surface turn. In the plane, a vortex really is circles (black, Lamb–Oseen). The spiral exists only in space (blue, Burgers).

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-navier-stokes/rounds/r03/piece.py \
  --fn navier_stokes_falling --seed 7 --paper a3 --margin 15 \
  --palette royalblue,royalblue,black,black,crimson \
  --out gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_iterate_v8.png
```

- **Final:** `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_iterate_v8.png` + `.gcode` (A3 portrait, seed 7).
- **Physical-width preview** (A1 mandate; judge the tone from this one): `gallery/studio/millennium_navier_stokes/current/pp_millennium_navier_stokes_iterate_v8_phys.png`. It was made with `GCodeVisualizer.preview(..., pen_widths={0:0.5, 1:0.3, 2:0.3, 3:0.3, 4:0.5})` on the same program. `render_candidate.py` has no `--pen-widths` flag, so I used a scratch driver that calls the same function and the same `merge_chunks`.
- Seeds: 7 (v5), 11 (v6) and 23 (v7) were rendered before the final C₀ shift. They are indistinguishable. Their blue strokes are 466 / 464 / 467, and the blue floor is 0.823 mm in all three. The rng only drives the per-arm termination dither. 7 is kept.
- Iteration trail:
  - v1: R_out 5δ, δ₀ 18, hero eye off the frame.
  - v2: hero moved to its own 0.5 mm blue nib, and the OPEN line split.
  - v3: the ring disc moved, the ladder caption cut to 4 lines, red limited to the ring alone.
  - v4: the disc moved onto the hero's row, centre x 178.
  - v5: title passes merged (tip 0.25 under a 0.3 nib).
  - v6–v7: seeds.
  - v8: C₀ moved from (7, 268) to (3, 262.8), which lengthens the frame crop and adds 11 mm between the hero and the statement.

## Mandate responses

| id | mandate | status |
|---|---|---|
| S1 | headline truth: conditional | **FIXED.** Statement (2 lines, x = 15): "FLAT, A WHIRLPOOL IS ONLY RINGS. THE SPIRAL IS THE THIRD DIMENSION. / WHETHER IT CAN SHRINK TO A POINT ON ITS OWN IS OPEN." The first sentence is r01's wording. Nothing on the sheet asserts that an unforced vortex shrinks. The terminus is phrased as an IF ("IF THE LADDER FINISHES, IT FINISHES HERE, IN 4/3 OF THE FIRST RUNG'S TIME:") |
| A2 | hero R_out = 5δ, hard crop ≥ 170 mm, ≤ ½ rim, far arms ≥ 8 mm from rung 1, orbit carried, hero not the palest | **FIXED, with two numbers ARGUED.** (a) R_out = 5δ on every rung, so the ratios stay exactly 2:1. **δ₀ = 18, not 20.** At δ₀ = 20 the 1.20 orbit is 1.2·3·100 = 360 mm long, and with the hero cropped at x = 15, L would land at y ≈ 3, off the sheet. At δ₀ = 18 the orbit is 324 mm and the hero R is 90 mm (up from 80). (b) C₀ = (3, 262.8): the eye is 12 mm beyond the left frame. **Rim visible 45.7 %** (≤ 50 %). (c) The frame's chord through the field is **178.4 mm** (y 173.6–352.0). Strokes actually clipped by the frame span **166.2 mm** (y 175.2–341.5). The top 10 mm cannot be crossed: at the top of a CCW inflow the arms run down-left at 72° to the circle, so a stroke that starts on-sheet reaches x = 15 about 11 mm below the rim. Any hero with ≤ ½ rim therefore caps the clipped span at chord − 11 ≈ 169. I report both numbers; the critic should pick the one the mandate means. (d) Hero ink to rung-1 ink is **27.0 mm** (≥ 8). The orbit moved with the hero: ½ ratios, factor 1.20, red ring exactly at L. (e) The tone comes from **duty, not spacing**. The hero is drawn with a **0.5 mm blue nib**, rungs 1–4 with 0.3 mm. That is the scaling applied to the nib as well as to the spacing: rung 0 = rung 1 ×2 in line pitch AND in line weight (0.5 is the nearest real nib to 2 × 0.3). Rungs 2–4 sit at the nib floor, just as they sit at the spacing floor. Duty: hero 0.5/2.4 = 21 %, rung 1 0.3/1.2 = 25 %. Ink area: hero 3.86 m × 0.5 = 1930 mm², rung 1 4.70 m × 0.3 = 1410 mm². In the physical preview the hero is the heaviest blue mass on the sheet |
| S3 | rung density non-decreasing | **FIXED by the declared route in S3's own text, with a real improvement in the numbers. Strict monotonicity: NOT met, reasons below.** Measured length/πR² with R = 5δ_n (the hero is uncropped, i.e. 2 × rung 1 by congruence): **0.370 / 0.739 / 0.825 / 0.790 / 0.772.** r02 was 0.357 / 0.714 / 0.838 / 0.643 / 0.662. The reversal at rungs 3–4 dropped from −23 % to −4 % / −2 %. Cause of r02's reversal: its fixed 2.4 mm minimum stroke threw away every other surviving rim arm on rungs 3–4. r03 scales the minimum with the rung (the hero's rim-arm rule RIM_MIN·d_sep·δ_n, floored at 1 mm), so rung 4 keeps 24 arms instead of 12. **The synth's premise is wrong:** r01's cull does not "rise ×2 then stay flat". From r01's own NOTES the densities are 0.847 / 0.842 / 0.710 / 0.673 (R 44 / 22 / 11 / 5.5), which falls 20 %. I measured why the remaining 2–4 % cannot be removed by any cull. Once the floor bites, the rung-n structure at a given ρ = r/δ is identical in mm: the rim spacing of the kept arms is 1.40 mm on rungs 2, 3 and 4, and the halvings happen at the same ρ. The only difference is the bare eye plus the single-arm core, whose size is set by the 0.8 mm floor in *mm*. So it takes a growing share of a smaller rung (eye ≈ 1.5 mm radius: 0.4 % of rung 2's area, 1.8 % of rung 3's, 7 % of rung 4's). I tested a refill pass, where the remainder of every cut arm is re-admitted wherever it clears the floor. It added **0** strokes, because a cut arm's remainder is always within the floor of its surviving neighbours. The sheet therefore declares it: the ladder caption reads "FROM 1/4 ON, THE INK IS THE 0.8 MM PEN FLOOR" and the terminus reads "VORTICITY ×4 EACH RUNG" |
| A1 | rings on 0.3, physical preview | **FIXED.** Rings are layer 2, black 0.3 mm, the same pen as type (layer 3), with no swap. `_phys.png` was rendered with `pen_widths=`. In it the disc's weight matches rung 1's line weight, is below the hero's, and is no longer the darkest mass |
| A3 + S2 | terminus block on x = 282, ≤ 7 blocks, red < 1 %, glyphs inside [15, 282], define blow-up | **FIXED.** There is one terminus block under the red ring, flush right by *inked* extent at **x = 282.00**, with the last baseline at **y = 20.0** and the top baseline at 47.7 (the ring bottom is at 55.8). It reads: "IF THE LADDER FINISHES, IT FINISHES HERE, / IN 4/3 OF THE FIRST RUNG'S TIME: / VORTICITY ×4 EACH RUNG, INFINITE AT ONE POINT. / THAT BLOW-UP, NOT TURBULENCE, IS THE QUESTION." Then, after a half-line gap: "CLAIMED 8 SEP 2026: BLOW-UP WITH A SMOOTH PUSH / FORCED CASE NOT YET VERIFIED · CLAY: NO AWARD / WITHOUT A PUSH: OPEN". **7 blocks:** title, statement, ring caption, hero caption, ladder caption, terminus, notes. **Red = 0.16 m / 17.53 m = 0.93 %**, the ring only (2 passes). All status type is black, so the open question is drawn, not written twice. **Type x-range on the gcode is [15.00, 282.00].** Every flush edge is aligned by ink, not by font advance, and the title is fitted to the measure by its inked width. No "T0" glyph (A5 holds) |
| A6 | travel heavy | DEFERRED (ledger). 14.9 m travel against 17.5 m draw. The rim → eye returns are mandated |
| S5 | encoding housekeeping | DEFERRED (ledger). This round also moves δ₀ to 18 and R_out to 5δ; the translator should record both |
| A4, S4 | — | dropped in the ledger; not revived |

## What changed from parent

- **The hero became a field off the edge.** Its eye moved from on-sheet (62, 272) to 12 mm beyond the left frame, and R grew from 80 to 90 mm (5δ). The frame now cuts the field's full height, and what shows is the outer 2–5δ inflow plus a few tight core wraps against the frame. It no longer reads as a disc.
- **Tone by nib, not spacing.** The hero has its own 0.5 mm blue layer, and it is now the heaviest blue on the sheet at physical width. r02's hero was the palest.
- **The ring disc moved onto the hero's row, between the field and the right axis,** at (178, 298), 53.5 mm of bare paper from any blue. Rings against spiral is now one side glance at one height. r02's disc sat in the far corner. Its caption stays flush on x = 282 at the disc's centre height.
- **One terminus block** on x = 282 under the red ring replaces r02's two blocks on the stray x ≈ 231 edge.
- **Words.** The statement is conditional. Blow-up is defined as vorticity ×4 per rung → infinite at one point in 4/3 of the first rung's time. "Not turbulence" is written on the sheet. The ladder caption carries "LARGE SCALES TO SMALLER ONES" (3D ladder only) and declares the pen floor.
- **Cull** scales its minimum stroke with the rung (see S3).
- **Title** passes are 0.25 mm apart under a 0.3 nib, so they merge into one 0.8 mm stroke. r02's 0.45 mm spacing drew a visible triple line.

## Measurements / computations

- Physics is unchanged from r02, with the same functions: E₁(1) = 0.2193839, the closed form matches RK4 to 8 digits, and the core dθ/d ln r = −7.9577. Re_Γ = 100, δ₀ = 18 mm (inside [12.8, 25.6), so δ₅ = 0.5625 < 0.8 and rung 5 is correctly absent), d_sep = 2.4 mm in the hero.
- J–L master field: 192 rim arms (base 6 × 2⁵), with infill adding none at 5δ. The eye of the master set is 0.075 δ.
- **Ladder:** R = 90 / 45 / 22.5 / 11.25 / 5.625 mm, **ratio 2.000**. Centres are (3, 262.8), (132.71, 165.74), (197.56, 117.22), (229.99, 92.95), (246.20, 80.82), and L = (262.42, 68.69). Centre steps are 162.0 / 81.0 / 40.5 / 20.25 mm, and C₄ → L is 20.25. They are collinear to 2.5e-14°. Rim gaps are 27.0 / 13.5 / 6.75 / 3.37 mm.
- **Red ring:** r = |C₅ − L| + R₅ = 10.125 + 2.8125 = **12.94 mm** at L; the drawn radii are 12.932–12.944. The nearest blue is 14.68 mm from L, a centre-line gap of 1.74 mm. Nothing blue lies inside.
- **Cull per rung** (in → trimmed / removed → kept; min stroke):

  | rung | in | trimmed | removed | kept | min stroke | drawn | uncut | length/πR² |
  |---|---|---|---|---|---|---|---|---|
  | 0 hero | 103 frame pieces | 0 | 4 (crop fragments) | 99 | 7.2 mm | 3.86 m | 9.40 m | 0.370 (uncropped) |
  | 1 | 192 | 1 | 0 | 192 | 3.6 | 4.70 m | 4.70 m | 0.739 (congruent) |
  | 2 | 192 | 192 | 96 | 96 | 1.8 | 1.31 m | 2.35 m | 0.825 |
  | 3 | 192 | 192 | 144 | 48 | 1.0 | 0.31 m | 1.18 m | 0.790 |
  | 4 | 192 | 192 | 168 | 24 | 1.0 | 0.08 m | 0.59 m | 0.772 |

- **Lamb–Oseen disc:** r_c = 18 mm out to 2 r_c = 35.0 mm. **18 rings** at equal Δψ = 0.10623 (Γ/4π units). The inner ring is 5.95 mm. The tightest gap is **1.500 mm**, centred at 1.084 r_c (the speed maximum is 1.121 r_c; this is the discrete-ring offset). The outer gap is 1.86 mm. Each ring is one closed stroke, and seams are staggered by the golden angle.
- **Blue floor on the gcode** (0.1 mm resample, same-stroke pairs excluded within 1.2 mm of arc, both blue layers together): **min gap 0.824 mm, 0 pairs < 0.8.**
- Hero ink to rung-1 ink is 27.0 mm. The disc's outer ring to the nearest blue is 53.5 mm.
- Type is inside [15.00, 282.00]. `promptplot preview --stats --score`: grade A, efficiency 0.539 (the dominant issue, from the rim → eye returns).

## Plot budget

Leo: F600 = 10 mm/s draw, G0 ≈ 33 mm/s, 2.5 s per lift/drop cycle. Order: **blue 0.5 → blue 0.3 → black 0.3 rings → black 0.3 type (same pen, no swap) → red.** That is 3 swaps.

| layer | pen | content | strokes | draw | travel | ≈ min |
|---|---|---|---|---|---|---|
| 0 | BLUE 0.5 | hero, rim → eye, angular sweep | 99 | 3.86 m | 3.96 m | 13 |
| 1 | BLUE 0.3 | rungs 1–4, batched per rung | 360 | 6.40 m | 5.30 m | 28 |
| 2 | BLACK 0.3 | 18 rings, inner → outer | 18 | 2.37 m | 0.58 m | 5 |
| 3 | BLACK 0.3 | type (same pen as layer 2) | 1122 | 4.74 m | 4.61 m | 57 |
| 4 | RED 0.5 | empty ring at L, 2 passes | 2 | 0.16 m | 0.31 m | 0.5 |
| **total** | | | 1601 | **17.53 m** | 14.93 m | **≈ 104 min, 3 swaps** |

There are 54,452 commands. The longest stroke is one hero arm of about 250 mm (≈ 25 s), so every stroke is a batch boundary, and the rungs are natural re-zero points. The A3 question for Leo is still open (encoding §5); the A4 fallback was not re-rendered this round.

## Self-critique (from the physical preview)

1. **Hierarchy 8.** The hero field is now the heaviest blue and the largest mass, running off the edge. The disc reads second and rung 1 third.
2. **Grid 8.** Everything hangs on x = 15 or x = 282, flush by ink, with the title fitted to the measure. The terminus sits under the ring.
3. **Tension 6.** One diagonal, and the hero is cropped hard. But rungs 1–4 are still **four complete discs in white space with self-similar gaps.** The work order locks factor 1.20 and ≥ 8 mm between the hero and rung 1, and inside those constraints I could not make them one surface.
4. **Negative space 7.** The lower-left quiet triangle is bare. A leftover pocket remains at x 215–282, y 225–280, between the ring caption and the ladder caption.
5. **Craft for pen 8.** Floor 0.824 mm, 0 violations. Rings are closed, the title strokes merge, and red is 0.93 %. Type is 57 of 104 minutes (1122 pen cycles). Travel is heavy.
6. **Concept 8.** Rings against spiral is a side glance at one height. The words are honest: conditional statement, blow-up defined, "not turbulence", the claim dated.
7. **Depth 6.** It is declared flat, and the only recession is the orbit.

**Single worst thing: the ladder still reads as badges.** Rung 1 at mid-sheet is a complete, perfectly circular spiral disc, and rungs 2–4 are smaller copies set on white with gaps. The hero crop fixed the hero, not the ladder. By the translator watch, this should route to **translator**.

A proposal for the translator (not built; it contradicts A2's ≥ 8 mm gap and "rim" test): bound each rung by the **multiplicatively-weighted Voronoi cell of the orbit instead of a circle**. The boundary between rungs n and n+1 is the Apollonius circle |x − C_n| = 2|x − C_{n+1}|. It passes through L for every n, with diameter from P_n = C_n + ⅔(C_{n+1} − C_n) (at exactly 6δ_n) to L. So all cell boundaries form a **pencil of circles mutually tangent at L**, and the tiling is exactly invariant under "scale ½ about L". With a cap of about 7δ, neighbouring rungs share an arc boundary one pen floor apart. The ladder would become one self-similar surface draining into the red ring rather than discs on a line, and it would still be exact, since every point stays on its own rung's streamline.

## Engine requests

- `scripts/render_candidate.py`: a `--pen-widths 0.5,0.3,…` flag passing `pen_widths=` to `GCodeVisualizer.preview`. The studio mandates physical previews and the script cannot make one.
- `generators._stroke_text`: return or expose the inked x-extent. Right-aligning by `_text_width` leaves the trailing advance inside the measure, which put r02's flush edges 0.3–0.6 mm off.
- Carried from r02: glyphs `½ ¼ ⅛ δ Γ ω ψ`, and a proportional mode that spaces `I` correctly.
