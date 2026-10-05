# millennium-bsd r02 — abstract · parent: none · 2026-09-29

**Lineage:** François Morellet, *Répartition aléatoire de 40 000 carrés suivant les chiffres pairs
et impairs d'un annuaire de téléphone* (1961). The order taken is his rule, not his look: a number
sequence's PARITY decides which of two families each mark joins, and the maker adds no taste. Here
n odd puts nP on the closed oval and n even puts it on the open branch. The root number
ε = (−1)^rank = −1 forces L to cross zero.
**ORDER:** RADIAL seeded ORBITAL, a pencil of lines through one point.
**Canon:** a stated hybrid, an ART DECO sheet (canon 2: exact ray fan, thin/thick by passes) carrying
a Morellet system. Gold | black on cream.
**Declared flat:** the 17.01° crossing and the collinearity of every chord with P hold only on one
isotropic flat plane.

## Render

```
.venv/bin/python studio/millennium-bsd/rounds/r02/compute_L.py      # once, ~80 s -> l_samples.json
.venv/bin/python scripts/render_candidate.py studio/millennium-bsd/rounds/r02/piece.py \
  --fn bsd_zero_means_infinity --seed 7 --paper a3 --margin 15 \
  --palette dimgray,black,black,black,goldenrod --out gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.png
.venv/bin/python studio/millennium-bsd/rounds/r02/render_truewidth.py \
  gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.gcode gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6_phys.png
```
- PNG: `gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.png`. Pen 0 is previewed in dimgray. It is a black 0.1 nib.
- **Physical-width preview** (judge weight on this one): `gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6_phys.png`.
  It draws 0.1 / 0.3 / 0.3 / 0.5 / gold 0.7 at nib width on cream.
- GCODE: `gallery/studio/millennium_bsd/current/pp_millennium_bsd_abstract_v6.gcode`
- Seed 7. The piece has no randomness: the seed-11 gcode is byte-identical below the header (checked
  with diff).
- The checks come from `audit.py` (encoding §11 and exactness) and `layer_stats.py` (plot budget), both in this round.
- `piece.py` reads `l_samples.json` if it is present. The numbers are the same as a live `lfun_lib` call and
  the load saves about 60 s per render. With no cache the piece recomputes the samples live.

## Mandate responses

| id | mandate | status |
|---|---|---|
| — | No FEEDBACK.md, LEDGER.md or DESCRIPTION.md exists for this slug, and the dispatch says "parent=none on disk". There are no open J*/A*/S* rows. The binding brief is encoding.md §4–§11 plus the curator note. | n/a |
| curator | use a real curve, verified as 37a1 | FIXED. E: y²+y = x³−x, [0,0,1,−1,0]. The orbit ±61 is computed in exact Fractions at import. Every point is asserted on E, and 6P = (6,14) and 8P = (21/25, −69/125) are asserted too. |
| curator | its real rational points and chord-tangent additions | FIXED. Chord k is the exact line through P, kP and −(k+1)P (the tangent for k = 1). Collinearity is asserted for all 60 chords. Odd ↔ egg parity was checked for n = 1..61. |
| curator | the real L(E,s) near s = 1 with its simple zero | FIXED. L comes from `data/lfun_lib.py` (the smoothed approximate functional equation, ε = −1), 401 samples on [0,2]. L′(1) = 0.3059997738 against LMFDB 0.30599977383405. The crossing is at (204.60, 200) at 17.014°. |
| curator | the flow between geometry and analysis is the plate's idea | FIXED as encoded: the s-axis *is* the curve's mirror y = −½ carried into the branch's mouth, at the same mm scale. The one gold ink marks the cause (P) and the witness (the crossing). The bridge L′ = Ω·ĥ is the caption. No decorative flow lines are drawn. |
| curator | PLOTTING: one clean layer per meaningful pen, stated order, batchable strokes, minutes per layer | FIXED. There are 5 contiguous layers, 0→4 (checked from the gcode), with 3 physical swaps. The longest stroke is a ≈245 mm ray, which is a valid batch boundary. Minutes per layer are in the Plot budget. |
| curator | not decoration; name the LINEAGE | FIXED. There is no ornament. Every Deco element carries data: fan = pencil, weight = height tier, ziggurat = x(nP). The lineage is Morellet. |
| enc §11.1 | chords 1–7 reach 7 mm; later chords farther; heavy nearer than fine; 3 weights | PARTLY ARGUED. The encoding's own rule, r = max(7, gap/sin Δθ), puts **11** chords at 7.0 mm (2,3,5,6,7,12,13,15,16,18,28), not 7. For example, chord 12's smallest angle to any lower chord is ≥ 8.6°, so 1.05/sin ≥ 7 is false. The "exactly 1–7" line contradicts its formula, and I kept the formula. Chord 1 (the tangent) starts at 10.5 mm, because it osculates the egg (see clearance). Chord 4 starts at 23.4 mm, on its egg point (lens rule). Median inner end is 7.0 heavy / 10.7 medium / 23.9 fine mm, and the far ends run to 50–62 mm (chords 30, 43, 53, 56, 59). No ray ink comes within 7.0 mm of the hub centre, and the disc is R 6. |
| enc §11.2 | egg closed, branch open, tip 101.6 and vertex 131.1 with nothing between; egg symmetric about 200 | PASS. The egg spans x 30.0–101.6, y 158.6–241.4, symmetric about y = 200 and not about the hub's 226. The gap band holds 0 curve points. |
| enc §11.3 | rays stop on E or at the crop; the mouth is empty but for L; no ray left of the hub outside the egg | PASS. Rays are never extended past R or past the egg point (the chord span is min..max of its two curve points). |
| enc §11.4 | L from (152.6,200), dip 4.6 mm near x = 177, crossing in gold at 17.0° ± 0.5, ending 19.8 mm up at 256.6 | PASS. Minimum −0.08924 at s = 0.480 (−4.64 mm at x = 177.6). Angle 17.014°. L(2) = 0.38158 → +19.84 mm. Gold is a substitution over s ∈ [0.85, 1.15], 16.31 mm long, and the black stops 0.3 mm inside it. |
| enc §11.5 | 5 layers, 3 swaps, spacing ≥ 0.8, no type on rays, ziggurat 1…41 chars, edge ≤ 83, ≥ 8 mm from rays | PASS. Type-to-line clearance is at least 5.05 mm. The ziggurat edge is at x = 82.8 with 11.5 mm clearance, and its line lengths are exactly 1,1,2,1,3,1,4,5,6,6,7,8,10,11,10,11,15,17,18,19,21,23,26,27,30,30,34,37,40,41. Ray spacing ≥ 0.8 mm holds by the hub-LOD construction (≥ 1.05 against heavy bands). |

## What changed from parent

There is no parent. The composition is encoding §5 [A]. The moves I made on top of it during self-rounds v1 → v6:
1. **Hub crowding along the egg (v1 → v3).** Secants of a short egg arc next to P (chords 4, 8, 24) ran
   inside a < 1.5 mm lens beside the 0.5 egg line and read as a doubled, muddy egg. I added a structural **egg-lens
   rule**, a continuation of the hub LOD. The egg is itself a curve through P, whose tangent is chord 1, so it counts
   as a lower-index line. A hub→Q stretch that never gets more than 1.6 mm from the egg now starts AT Q, on the curve,
   where its rational point is (chord 4). When Q is the far end, that half-chord is not drawn (8, 24). Then comes an
   **engine-native clearance** pass: `material.suppress_parallel` against E, at 1.0 mm and 8.1°. The only chord it
   cuts is the tangent, where it osculates. Ray ENDS on E are always restored, because a meeting, however shallow,
   is the point's mark.
2. **Pairwise heavy gap (v6).** A light ray beside a heavy (2-pass) ray now clears the band's 0.25 mm
   offset (0.8 → 1.05 mm). Chords 10, 11, 14, 17 and 20 start farther out.
3. **Grid (v4).** The ziggurat's index column is flush with the 15 mm margin. The right text column dropped 5
   baselines, so its last line shares baseline 19.8 with the ziggurat caption. Both bottom blocks now sit on one
   line, and the column top falls to y ≈ 87.
4. **Pen cycles (v5).** Glyph strokes that share a vertex are joined, which saves 53 lifts. The two branch arms are one
   stroke through the vertex.

## Measurements / computations

- Exact orbit ±61 (Fractions). ĥ is visible as digits: x(30P) = 79799551268268089761/62586636021357187216
  (41 chars).
- In-field orbit points on drawn chords: 94. **75 are marked** by a ray end or crossing. 18 egg points near P
  (chords 8, 11, 14, 17, 24, 27, 30, 33, 36, 37, 40, 43, 46, 49, 52, 53, 56, 59, all within 34 mm of P) sit
  inside their chord's hub hole or lens. They are unmarked, which is what the encoding's hub LOD implies. −P is
  correctly unmarked.
- L′(1) = 0.3059997738 = Ω_E·ĥ = 5.98692 × 0.05111. The crossing angle at equal scale is 17.014°.
- Title tracking was solved so that the last glyph ends at x = 256.6, the L-curve's s = 2 end (2.348 mm track).

## Plot budget (A3 portrait, Leo F600 ≈ 10 mm/s, ~33 mm/s travel, 2 s per pen cycle)

| order | layer | pen | draw | strokes | est. |
|---|---|---|---|---|---|
| 0 | HAIR: fine chords k 25–60 + s-axis | black 0.1 | 4.54 m | 55 | ~10 min |
| 1 | CHORDS: medium k 10–24, heavy k 1–9 ×2 passes | black 0.3 | 4.68 m | 36 | ~9 min |
| 2 | TEXT: title (5-pass), statement, wall label, ziggurat, right column | black 0.3 (no swap) | 6.88 m | 1 499 | ~63 min |
| 3 | CURVES: E(ℝ) (egg + branch as one stroke through the vertex) + L | black 0.5 | 0.71 m | 4 | ~1 min |
| 4 | GOLD: P disc (6 rings) + crossing band | gold 0.7 | 0.16 m | 7 | ~1 min |

The total is 16.97 m drawn, 6.5 m travel, 15 887 commands, **≈ 84 min, 3 swaps**. The longest travel inside a layer is 201 mm
(text, between blocks). Inside a block no travel crosses the sheet. The text layer is the one expensive run, and
465 of its characters are the ziggurat digits, which *are* ĥ. If time must be cut, cap the ziggurat at n = 24.

## Self-critique (rubric, honest)

1. Hierarchy 8: fan + curve dominate, the gold disc is second, and the gold crossing third, placed in the emptiest zone.
2. Grid & alignment 8: one 15 mm left edge (title, wall label, ziggurat index), a shared bottom baseline, and the title's right edge registered on s = 2.
3. Tension & asymmetry 8: the hub sits off-centre and above the mirror, the rays crop at the top and bottom, and the 17° diagonal is the only analytic slant.
4. Negative space 8: three silences, each a truth (left of P, the mouth, the gap), plus the quiet top-right.
5. Craft for pen 7: three weights by nib and passes. At 8–10 px/mm the title's 5-pass offsets show seams at sharp corners (S, W); on paper, at 0.18 mm pitch with a 0.3 nib, they should close.
6. Concept 7: parity-by-position and "zero is full" read. The L-curve still reads as a small inset graph to a first-time eye.
7. Depth 7 (declared flat).

**The single worst thing:** the analytic half (the L-curve on its hairline) is still the weakest-integrated element. It is a
104 × 25 mm line beside a 186 × 350 mm fan. Nothing on the curve side shows that its axis *is* the egg's mirror,
because the mirror may not be drawn there (§9.3). The viewer has to infer the shared y = 200 from the egg's symmetry.

## Engine requests

- `suppress_parallel(priority=...)`: the function orders by length only. To make the curve claim its
  space first, I pass it as guards that are artificially longer than any chord (the egg run 1.5×, the arms run past the
  field). A `fixed=` list of obstacle polylines that are never trimmed would make that honest.
- `render_candidate.py --pen-widths` (already requested by Riemann and P vs NP). This round carries `render_truewidth.py`.
