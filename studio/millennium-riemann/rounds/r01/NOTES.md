# millennium-riemann r01 — faithful · parent: none · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-riemann/rounds/r01/piece.py \
  --fn riemann_faithful --seed 7 --paper a3 --margin 15 \
  --palette "dimgray,black,black,crimson" \
  --out gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5.png
```

- final PNG: `gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5.png` (standard preview: every layer is drawn at
  one line width, pen 0 is shown as dimgray to stand in for the 0.1 nib)
- true-width companion: `gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5_truewidth.png` (0.1 / 0.3 / 0.3 / 0.5 mm,
  made with `render_truewidth.py`; the standard preview's stats box and legend sit over the title and
  the top-right caption, so use this one to judge the type)
- GCODE: `gallery/studio/millennium_riemann/current/pp_millennium_riemann_faithful_v5.gcode`
- seed: 7. The piece uses no randomness. Seeds 3, 7 and 11 give the same command hash (`e77eec07fd` on v3).
- data: `data/xray_faithful.json` (new file, written by `rounds/r01/compute_faithful.py`, mpmath 1.4.1
  from a scratch target, 2.5 min on 8 cores). `data/xray_contours.json` and `zeros.json` are untouched.
- audit: `.venv/bin/python studio/millennium-riemann/rounds/r01/audit.py`
- lineage: Sol LeWitt, *Wall Drawing #46* (1970), "Vertical lines, not straight, not touching, covering
  the wall evenly". The order taken is an instruction executed exactly: ζ writes two instructions
  (Re ζ = 0, Im ζ = 0). Their lines are not straight and never touch except at the zeros, and every
  touch off the real axis stands in one column. The wording should be checked against the catalogue
  raisonné (encoding §1).

## Mandate responses

The plate has no FEEDBACK.md or LEDGER.md yet, so there are no J/A/S rows. The binding briefs are the
curator note and encoding §9/§11, and I answer them here.

| id | mandate | status |
|---|---|---|
| CUR-1 | interpret the reference, never trace it; grey tones become line duty | FIXED. Nothing is sampled from the raster. Only the layout was measured (table below). The grey field is replaced by two exact zero sets and there is no tone anywhere. |
| CUR-2 | compute \|ζ(s)\| on the strip for the contour field | ARGUED. The field is computed from ζ on a 0.05 grid over σ∈[−46,47], \|t\|≤54 (2.0 M evaluations). What gets drawn is the Re ζ = 0 and Im ζ = 0 zero sets, not \|ζ\| level sets, because encoding §9.4 forbids \|ζ\| contours: the \|ζ\| field would carry the reference's false left–right mirror (dossier lie 1). The \|ζ\| asymmetry still shows on the sheet as comb against silence. |
| CUR-3 | real zeros, real primes | FIXED. The 20 red crossings sit at ±γ₁…γ₁₀ from `zeros.json`. The footer is ψ₁₀₀(x)−x from the first 100 zeros, with numerals at the primes and prime powers 2…32. |
| CUR-4 | one clean layer per meaningful pen, order stated, minutes per layer | FIXED. See Plot budget. |
| CUR-5 | dotted runs must earn their cycles | FIXED. There are no dotted runs at all. |
| CUR-6 | name the lineage | FIXED (LeWitt #46, above and in HANDOFF). |
| §11.1 | ONE COLUMN: 20 centres within ±0.3 mm of x=148.5, none within ±42.4 mm of the axis | FIXED. All centres are at exactly x=148.500. The lowest is at y = 210 ± 42.40. Red begins at \|Δy\| = 40.4 mm, the edge of the r = 2 mm arm. |
| §11.2 | right angles that tilt: 90°±3°; hairline arm at −9°, +13°, +31° at ρ₁, ρ₂, ρ₄ | FIXED. On the raw marching-squares data: 89.45°, 89.23°, 88.82°, with hairline arms at −8.98°, +12.41°, +29.77° (exact: −9.05°, +12.64°, +30.79°). The drawn polylines are RDP-decimated at 0.02 mm, so a single chord at a tongue tip reads 84–89°. The position error stays ≤ 0.02 mm. |
| §11.3 | NOT A MIRROR; right-of-column ink ≤ 10 % of left | PARTLY ARGUED. Right of the column there are only hairline rulings, at pitch 13.57–13.64 mm (spec 13.60). The lower half is the exact conjugate reflection. The ink ratio is **0.188**, not ≤ 0.10: 22 rulings × 133 mm ≈ 2.9 m is irreducible in the encoding's own window σ ≤ 45. The 10 % figure was an estimate, and meeting it would mean deleting true lines. |
| §11.4 | NO OTHER MEETINGS; Gram / half-Gram lone crossings left visible | FIXED. The meetings come from the data. The minimum A–B gap away from the zeros and the real axis is 1.47 mm. The tongues crossing σ=½ at half-Gram points and the hairlines at Gram points are untouched. |
| §11.5 | PLOTTABLE: gcode, 4 layers, 2 swaps, ≥0.8 mm, no type on comb, footer cliffs aligned | FIXED. Minimum spacing is 1.47 mm (A–B) and 3.62 mm (A–A). Minimum text-to-field clearance is 3.23 mm. The cliffs at 2, 3, 4, 5, 7, 8, 9, 11, 13, 16 sit over their numerals. Bounds are clean (ink bbox 15..282 × 16..403.3, no clamp violations). |
| §9 | forbidden list | No left–right mirror, no line drawn along the column, no ladder, no axes/arrows/colour bar/inset, no rings, isotropic 3.0 mm/u, no unrelated clipping. There is no "⇔": the claim is typeset as "ζ(ρ)=0, 0<Re ρ<1 ⇒ Re ρ=½ ?". The ψ footer jumps at prime powers too. |

## What changed from the reference (the layout fixes)

The reference was measured on its 1024×1536 raster (u = x/W, v = y/H from the top):

| reference element | measured | faithful r01 |
|---|---|---|
| title "RIEMANN / HYPOTHESIS", 2 lines | u .034–.317, v .020–.073, cap ≈ 32 px | one line, 8 mm caps with 4-pass weight, flush-left x=15, baseline 395. There is not room for 2 lines at 8 mm in the 33 mm title band. |
| short rule under the title | u .034–.084, v .089 | kept: 6 mm at y=389 |
| statement, 2 lines caps | v .104–.126, cap 10 px ≈ 2.7 mm | one line of 2.5 mm caps, baseline 381, "… RE S = ½." |
| red critical line, full height | u .5005, v .027–.893 | **cut.** Two 5 mm red register ticks sit at x=148.5, outside the field |
| 23 blue rings, evenly laddered to t≈1 | rows 121…1241 | 20 red crossings at ±γ₁…γ₁₀, made of the two curves themselves. The column is empty for \|t\|<14.13. |
| streamline field, mirrored L–R and T–B | ink left : right = 0.99 : 1 | the X-ray, mirrored T–B only. Left : right ≈ 5.3 : 1. |
| arrowed Re/Im axes, 0 ½ 1 labels | v .474 | the real axis survives as a hairline (Im ζ = 0), with no arrows and no numbers |
| \|ζ\| colour bar | u .04–.07, v .56–.72 | cut (lie 8) |
| "DETAIL NEAR ZEROS" inset | u .72–.91, v .57–.76 | cut. At 3 mm/u the plate shows every crossing itself, and the inset's "32.0" was false. |
| formulas split left and right | v .30–.39 | all type moves to the right void, flush-left at x=190, each block centred between two of ζ's own rulings t≈kπ/ln2 |
| italic tagline, top right | u .78–.97 | becomes "THE ZEROS CHOOSE THE SEAM OF A PICTURE THAT IS NOT SYMMETRIC." in the upper void. The top-right corner now carries a small series caption on the same x=190 column. |
| "Primes:" dotted number line | v .915 | ψ₁₀₀(x)−x over x∈[1.5,32.5] (8.61 mm/u), y-band 24–41, prime numerals 2.2 mm and prime-power numerals 1.6 mm at y=16 |
| "ONE LINE. INFINITE CONSEQUENCES." / "SIMPLE NUMBERS…" | v .97 / right footer | dropped (encoding §5F allows it). There is no room under the footer label without crowding the margin. |

Composition moves across self-rounds:
- v1 → v2: the verified line overflowed x=282 and was split into 2 lines. The claim formula was
  set on one 3.0 mm line, because the 2-line 3.4 mm block came within 1.49 mm of a ruling. Authored "?" and a
  visible "·".
- v2 → v3: the type was regrouped into two clusters. The claim and the object (Euler product, RH claim)
  go in the upper void. LeWitt's three instructions, one per band, go in the lower void with the status line. The
  bands beside the real axis stay empty, so the widest silence sits beside the zero-free stretch.
- v4 → v5: glyph strokes are chained, heavy-title passes are linked into one pen-down per stroke, and the
  title weight went to 0.6 mm (4 passes at 0.2 mm) so it reads as solid mass.

## Measurements / computations

- X-ray: `mp.fp.zeta` on σ∈[−46,47] step 0.05, with t on half-step rows 0.025+0.05k up to 54.025, mirrored by
  ζ(s̄)=conj ζ(s). The real axis falls between grid rows, so marching squares traces it as a genuine
  Im ζ = 0 line, the Re ζ = 0 chevrons pass through it at the trivial zeros as single strokes, and s=1 is
  never evaluated. Result: 44 re0 and 55 im0 pieces, 3112 u and 4222 u before cropping.
- Mapping: x = 148.5 + 3.0(σ−½), y = 210 + 3.0t. Crop at σ∈[−44,45] and \|t\|≤51.37 (the mid-gap between γ₁₀ and γ₁₁),
  giving the field y∈[55.89, 364.11]. Clipping to the rectangle uses exact `geometry.clip`.
- Red substitution: for each ρ, the A- and B-polyline nearest (½, ±γₙ) is taken. The maximum miss is 0.014 mm
  (point-to-segment). Inside `Circle(r=2.0)` the branch goes to red, and outside `Circle(r=1.8)` it stays black or hairline, which
  gives a 0.2 mm joint. No other polyline is clipped.
- Decimation: RDP at 0.02 mm, far below the 0.1 mm nib.
- Right-field rulings at x=188: 60.45, 74.02, … 359.55 (pitch 13.57–13.64 mm, theory kπ/ln2·3 = 13.597).
- Footer check: ψ₁₀₀(10.5) = 7.8352 (dossier check #10: 7.8352, and ln 2520 = 7.8320). ψ−x ranges over
  [−3.819, +0.845], giving y-scale 3.645 mm/u.
- Min gaps: A–B 1.468 mm at (151.4, 304.5), which is the ρ₄/half-Gram tongue beside the column. A–A is 3.624 mm.

## Plot budget (A3 portrait, Leo F600 ≈ 10 mm/s, 2.5 s per pen cycle, travel at ~50 mm/s)

| order | layer | pen | draw | travel | strokes | ≈ min |
|---|---|---|---|---|---|---|
| 1 | B · HAIRLINE (Im ζ = 0, real axis included) | black 0.1 | 11.41 m | 2.03 m | 74 | 22.8 |
| 2 | A · BLACK (Re ζ = 0) | black 0.3 | 8.26 m | 1.09 m | 63 | 16.7 |
| 3 | TEXT + ψ footer (same pen as A, own layer, no swap) | black 0.3 | 4.07 m | 3.55 m | 713 | 37.7 |
| 4 | RED (ρₙ arms + 2 register ticks) | red 0.5 | 0.17 m | 0.81 m | 42 | 2.3 |

Total ≈ 80 min, 2 physical swaps, 12 077 commands. Every stroke over 300 mm is split at its tip, so it
can act as a batch boundary. The text layer is mostly pen cycles (713 glyph strokes ≈ 30 min), which is the price of the
type. The pipeline's per-colour nearest-neighbour reorder overrides the authored boustrophedon order,
and leaves one leftover long hop in the B and TEXT layers (≈ 300–360 mm). The 400 mm "red" hop is the final park to (0,0).

## Self-critique (rubric, honest)

1. Hierarchy: 8. The comb is the dominant mass at 3 m. The title and the red column come second, and the type and footer third.
   At 3 m the red is only a stack of 4 mm red flecks. It is scarce and exact, but it is not loud.
2. Grid & alignment: 8. The margins are exact at 15 and 282. The type column x=190 is shared by the corner caption and all
   void blocks, and each block is centred in a ζ ruling band. Title, statement, footer label and comb all start at x=15.
3. Tension & asymmetry: 7. The frame is centred on σ=½ by declaration, and the content is violently lopsided. The chevron's
   point into the column gives a strong horizontal thrust. There is still no diagonal beyond the comb's fan.
4. Negative space: 8. The ruled right field, the empty column stretch and the empty bands beside the axis are all real
   silences with a meaning.
5. Craft for pen: 8. Spacing is ≥ 1.47 mm, there is no fill and no ink-on-ink except the red joints, and two families are separated by weight.
   The text layer is cycle-heavy.
6. Concept legibility: 8. "Two families never touch except in one column" reads without the caption. The
   LeWitt label confirms it.
7. Depth: flat by declaration (Swiss canon plus conformality: any tilt or perspective breaks the 90° truth).

**Single worst thing:** the red accent is too small to carry the plate at poster distance. Twenty 4 mm
crossings at 0.5 mm are exact but read as flecks. The encoding fixes r = 2.0 mm (0.38 × min gap). A
rework could try r = 2.4 mm (still < ½ × 5.31 mm) or a 0.7 mm red nib before touching anything else.

## Engine requests

- `merge_chunks`/`reorder_by_color` always re-sorts strokes by nearest neighbour inside a colour. A flag
  to keep the authored order would let a piece guarantee its own batch order (bottom→top
  boustrophedon) and avoid the leftover sheet-crossing hop.
- Stroke-font glyphs authored locally here, candidates for `_GLYPHS`: ζ ρ ψ γ ½ ⇒ ? ⁻ ˢ ₙ, plus a visible "·".
- `render_candidate.py` has no `--pen-widths`, so the standard preview draws a 0.1 hairline and a 0.3
  line identically. This round works around it with a local true-width rasteriser.
