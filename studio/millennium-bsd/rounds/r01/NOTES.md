# millennium-bsd r01 — faithful · parent: none · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/millennium-bsd/rounds/r01/piece.py \
  --fn bsd_faithful --seed 7 --paper a3 --colors 5 \
  --palette dimgray,black,black,black,goldenrod \
  --out gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5.png
.venv/bin/python studio/millennium-bsd/rounds/r01/render_truewidth.py \
  gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5.gcode gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5_truewidth.png 0 0 297 420 5
```
Final: `gallery/studio/millennium_bsd/current/pp_millennium_bsd_faithful_v5.png` (preview), `…_v5_truewidth.png` (nibs at
physical width, the one to judge), `…_v5.gcode`. Seed 7. The piece consumes no randomness: every
mark is exact. Seed 11 gives the same gcode byte for byte apart from the header comment (checked).
Trials: v1 through v4 in ~/Downloads.

## Mandate responses
No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exists for this slug yet, so there are no J*/A*/S*
rows. The binding brief is encoding.md §4/§9/§11 plus the curator note.

| id | mandate | status |
|---|---|---|
| curator | a real curve (37a1), real rational points and chord-tangent additions | FIXED. The exact group law is in Fractions, `assert y²+y == x³−x` holds for all ±30 multiples, and the 3 chords are the pencil through P. |
| curator | the real L(E,s) near s=1 with a simple zero | FIXED. 289 samples come from `data/lfun_lib.py` (ε = −1). min −0.08924 at s = 0.475, L(2) = 0.38158, L′(1) = 0.30600, crossing at 17.014°. |
| curator | the flow between geometry and analysis is the plate's idea | FIXED, but only weakly (see Self-critique). The s-axis is the curve's mirror y = −½ at the curve's own mm scale. The dashed negation steps are bisected on that same line. The caption states the bridge in words. |
| curator | name the LINEAGE | FIXED. See the lineage note below. |
| curator | plottable: one layer per pen, stated order, minutes per layer | FIXED. See Plot budget. |
| §11.2 | two pieces, one mirror, 29.5 mm bare gap | FIXED. The egg's right tip is at (101.6, 200), the branch vertex at (131.1, 200), and nothing lies between them. |
| §11.3 | exactly 3 chords at 0°/45°/−45° through the disc, 48 open circles | FIXED, with an ARGUED deviation. 47 circles plus P as the gold disc make the encoding's 48 in-field multiples. The tangent chord starts 11.2 mm from P (see change 6). |
| §11.4 | one crossing, not a touch, 17.0° ± 0.5°, gold the only colour on the right | FIXED |
| §11.5 | 5 layers, 3 swaps, no type touches a ray | FIXED. Minimum text-to-ink distance is 1.81 mm. P's label moved off the y = x chord and the egg. |
| §9.1–9.14 | forbidden list | FIXED. No off-curve point, no joined components, no axes, arrows, ticks or grid, no decorative gold, no V. |

**Lineage.** It is Morellet's parity rule, as the encoding states: parity decides the family. Odd n
falls on the oval and even n on the branch, and the root number −1 forces the crossing. On the
faithful plate it is carried by position alone: the open circles fall on the oval or the branch.
The drawing vocabulary is the reference's own: the textbook chord-tangent figure beside an
L-graph. The sheet is a flat Deco hybrid, gold and black on cream.

## What changed from parent (the reference) — layout fixes, each listed
1. **Two components.** The egg over [e₃, e₂] and the branch over x ≥ e₁ have no curve ink for
   e₂ < x < e₁. The reference drew one connected wiggle.
2. **Mirror y = −½, not y = 0.** No x/y axes. The mirror appears only as the s-axis, inside the
   branch's mouth.
3. **Every marked point is real.** The reference's (1,1) and (1,−2) are not on E and are gone.
   The circles are all nP, |n| ≤ 30, that fall in the field. They crowd at the egg's right tip,
   which is the invariant measure ds/|∇F| made visible.
4. **The construction is a true staircase.** The tangent y = −x runs P → −2P. The negation x = 1
   takes −2P to 2P. The chord y = 0 joins −3P, P and 2P. The negation x = −1 takes −3P to 3P.
   The chord y = x joins 3P, P and −4P. The staircase stops there, and the orbit continues as
   text (6P…14P).
5. **L on the curve's own scale.** S = 52 mm per unit for x, y, s and L alike. L(0) = 0, L is
   negative on (0,1), and it crosses transversally in gold at 17.0°. There is no V, no vertical
   axis and no arrow. "simple zero (order 1)" became `ONE CROSSING, NOT A TOUCH: ORDER 1.`
6. **The tangent kisses.** Tangent and egg separate as κt²/2, which measured 0.13 mm at 4 mm and
   0.70 mm at 10 mm. The tangent line therefore starts where it is 0.9 mm clear of the egg
   (11.2 mm from P, by bisection). The curve carries the contact.
7. **Gold ornaments and threads cut** (lie 6). Gold marks exactly two things, P and the crossing.
8. **Title flush-left** (series grammar). The reference's tagline "geometry meets analysis" is
   kept as the first words of a two-line statement.
9. **Proximity.** `E : Y²+Y = X³−X` sits right above the figure, as in the reference. The
   equation sits right under the figure, larger than the encoding's 4.5 mm (5.5 mm, heavy),
   because the reference gives it a 126 mm line. The analysis caption, bridge and status became
   one flush-left column directly under the L-curve (x = 215) instead of the encoding's separate
   bottom-right block, so the caption stays beside its graph as in the reference.

Self-rounds: v1 was an earlier session of this round. It had the right column overflowing to
x = 289 (clipped glyphs), the P label on the egg, an `(Ш…)` glyph blob and a `|N|` misread.
v2 regrouped the columns, fixed the widths, rephrased and moved the equation up. v3 started the
kissing tangent at the floor and moved the E label to the figure. v4 added the bridge caption.
v5 restored the dashed negation steps, which a min-length filter had dropped in v3 and v4.

## Measurements / computations
- **Reference** (1122×1402 px, u = x/W, v from top): title u .097–.900, v .133–.163. The E label is
  at v .293–.320. The figure band is v .330–.720. Circles are Ø 1.2 % W. The equation spans u
  .287–.711 at v .785–.812. The lower 16 % is blank. On this plate the blank bottom is kept, and
  the lower arm runs through it to the crop.
- **Curve.** 37a1: e₃ = −1.1071599, e₂ = 0.2695944, e₁ = 0.8375654. Egg top and bottom are at
  sheet y 241.4 / 158.6, symmetric about 200. Every orbit point satisfies y²+y = x³−x in exact
  rationals. 48 multiples fall in the field, and the minimum circle separation is 3.99 mm.
- **L(E,s)** from `data/lfun_lib.py`. L(0.5) = −0.089049, L(1.5) = 0.183965, L(2) = 0.381575,
  L′(1) = 0.3059997738 = Ω·Reg = 5.98692 × 0.05111 (verify_bsd.py re-run 2026-09-29). atan(L′(1))
  = 17.014°. The gold stretch covers s ∈ [0.85, 1.15], 2 passes 0.3 mm apart.
- **Height caption** checked on the orbit. log max(|num|, den) of x(nP) / n² = 0.05081 (n = 10),
  0.05086 (n = 20), 0.05092 (n = 30), which tends to 0.0511.
- **Clearances.** Text to any ink is at least 1.81 mm. Every column line was measured to fit
  x ≤ 282, and the build asserts it.

## Plot budget (A3 portrait, from the v5 gcode; Leo ≈10 mm/s draw, ≈2 s per pen cycle)
| order | layer | pen | draw | strokes | est. |
|---|---|---|---|---|---|
| 1 | HAIR | black 0.1 | 0.15 m | 45 (dashes + s-axis) | ≈ 2 min |
| 2 | CHORDS | black 0.3 | 0.60 m | 52 (3 chords, 47 circles) | ≈ 3 min |
| 3 | TEXT | same 0.3, own layer, no swap | 6.93 m | 1 561 | ≈ 66 min |
| 4 | CURVES | black 0.5 | 0.61 m | 53 (E broken at circles + L) | ≈ 3 min |
| 5 | GOLD | gold 0.7 | 0.10 m | 6 | ≈ 1 min |
| | total | 4 pens, 3 swaps | 8.38 m draw / 7.95 m travel | 19 536 commands | **≈ 75 min** |

The text is authored in block order: title, statement, corner, E label, key, equation, orbit list,
axis labels, column, point labels. Every block is a valid batch boundary; re-zero between blocks.
The title alone is 2.0 m (4 passes at 0.2 mm for the heavy caps).

## Self-critique (1–10)
1. Hierarchy **7.** Gold P and the egg with its circles dominate, and the gold crossing is the
   second loud point. The L-curve is too small to be a co-protagonist, as it is in the reference.
2. Tension / diagonals **7.** The −4P chord and the rising arm drive into the empty upper right.
   The lower arm bleeding off the bottom is honest (the orbit is unbounded).
3. Fill vs void **7.** The three silences are true: the gap, the mouth, and the half-plane left
   of P. The bottom quarter holds only the arm and 4P.
4. Density / spacing **8.** The kissing tangent is resolved structurally. Circles are ≥ 3.99 mm
   apart and text ≥ 1.8 mm from ink.
5. Colour **8.** Gold is on two things only, under 1 % of the ink.
6. Concept legibility **5.** This is still a textbook figure plus a graph (faithful to the
   reference by design). The geometry → analysis flow reads mainly through the caption.
7. Craft / plottability **7.** It is exact and layered, but the text layer (66 min) outweighs
   all the drawing layers together.

**Single worst thing:** the bridge between the two halves is carried by words, not by the
drawing. Nothing on the sheet joins the curve group to the L-curve except the shared, undrawn
mirror height. Because the encoding forbids drawing the mirror through the curve side (§4, §9.3),
the 21.5 mm vertex-to-s = 0 stretch stays bare, and the reader only learns the connection from
the column.

## Engine requests
None. Stroke type and glyphs were authored locally (double-struck ℚ and ℤ, the small S=1 subscript), because the
house font lacks double-struck letters.
