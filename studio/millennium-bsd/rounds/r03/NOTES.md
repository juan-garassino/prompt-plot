# millennium-bsd r03 — iterate (abstract, the Deco pencil) · parent: r02 · 2026-09-29

**Lineage:** François Morellet, *Répartition aléatoire de 40 000 carrés suivant les chiffres pairs
et impairs d'un annuaire de téléphone* (1961). The order taken is his rule, not his look: the parity of a
number sequence decides which of two families each mark joins. Here n odd puts nP on the oval and n even puts it
on the branch.
**ORDER:** RADIAL seeded ORBITAL. **Canon:** ART DECO sheet carrying a Morellet system (stated hybrid).
Gold | black on cream. **Declared flat.**
Work order: `rounds/r02/SYNTH.md`. Two text-only borrows from r01: the series caption and the conjecture's statement.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-bsd/rounds/r03/piece.py \
  --fn bsd_zero_means_infinity --seed 7 --paper a3 --margin 15 \
  --palette dimgray,black,black,black,goldenrod --out gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.png
.venv/bin/python studio/millennium-bsd/rounds/r03/render_truewidth.py \
  gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.gcode gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7_phys.png
.venv/bin/python studio/millennium-bsd/rounds/r03/audit.py                                  # §11 + ledger checks
.venv/bin/python studio/millennium-bsd/rounds/r03/gapcheck.py gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.gcode
```
- The final PNG is `gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.png` (pen 0 previewed dimgray). Judge on `gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7_phys.png`.
- The GCODE is `gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.gcode`.
- Seed 7. The piece has no randomness: the seed-11 gcode is byte-identical below the header (diff = 0 lines).
- `l_samples.json` is r02's cache, copied. The numbers are the same as a live `lfun_lib` call.

## Mandate responses

| id | mandate | status |
|---|---|---|
| S1 | ĥ caption off by ln 10 | **FIXED.** The caption now reads `X(NP) EXACTLY. ITS DIGITS GROW AS N² × 0.0222 (= HEIGHT 0.0511 / LN 10).` Check: 0.0222 × 900 = 20.0, which matches line 30's 20 + 20 digits. The bridge column keeps `0.05111` (natural log, as in L′ = Ω·ĥ). |
| S2(a) | ≥ 60/62 oval points marked | **PARTLY FIXED, 42 → 53 / 62; 7 ARGUED.** The new marks are: 3 stubs straddling E at crossings of ≥ 10° (−9 at 15.3°, 49 at 12.5°, −53 at 37.0°), and 8 **notch stubs** for shallow meetings (17, −25, 27, −31, 33, −41, −47 at 2.9–9.4°). A notch stub is a 2.0 mm stretch of the chord's own line through the point. The egg yields across it and is joined to it end to end, so the curve changes to the chord's nib exactly at the rational point. Unmarked, with the reason for each: **−57 and 59** are 2.55 and 2.47 mm from P, under the gold disc (R 6 + 0.35 nib); no mark can exist there that is not the gold. **−15 (6.56 mm) and 43 (8.76 mm)** lie 0.54 and 0.53 mm off the tangent's centreline, where E osculates it and the egg yields to the tangent (S2c). Any own-line stub would run < 0.8 mm beside the heavy tangent. **−37, 37 and 53** are at the egg's right tip. They lie 0.72 / 0.60 / 0.47 mm off lower-index rays (chords 21, 20 and 4) that run within 1.1–1.4° of their own chord, so any own-line stub breaks the 0.8 floor. −P and 61P lie on no chord. |
| S2(b) | inner ray ends at own point or ≥ 1.5 mm from E | **FIXED.** The audit finds 0 violations. Chord 11 is carried in to its own point −12P (t 22.1 → 19.19). Chord 27 is pulled out to 1.5 mm clear (18.2 → 21.7). Chord 1 now starts at the hub circle, off E. |
| S2(c) | tangent from 7.0 mm; egg yields on the kissing side; no pass through non-own points | **FIXED.** The tangent's pass 1 spans t = 7.00 → 73.54 mm (to −2P). Its 2nd pass is offset −0.25, away from the egg. On the kissing side the egg is clipped from the disc edge to t = 10.67 mm, where separation reaches 0.8. From there to 15.34 mm, E is carried by the notch stubs of −31 and 27, and the drawn egg resumes 1.73 mm from the tangent. The tangent runs 0.53 / 0.54 mm from the E points 43 and −15. Osculation makes that unavoidable: every point of E within 10.5 mm of P is < 0.8 mm off the tangent. Neither point carries a mark or circle, so no false collinearity is drawn. No circles are faked onto the tangent. |
| A1 | gold crossing = second read; ≈ 1.4 mm non-overlapping band; rest of L on the black 0.3 | **FIXED.** s ∈ [0.85, 1.15] is 2 passes of the gold 0.7 at centreline ±0.35 mm (pitch = nib, 1.40 mm band, no spot inked twice). It is one stroke of 16.31 mm per pass. The rest of L is on the black 0.3, **layer 1 (CHORDS)**, with no new swap, and stops 0.4 mm short of the gold. The crossing measures 17.014° at (204.60, 200). In the full-page true-width png, the gold band is the heaviest stroke right of x = 140; the branch arm there is the 0.5. |
| S3(a) | statement with the cause | **FIXED** (on 2 lines, as permitted). Line 1 is `RANK E(Q) = ORD_{S=1} L(E,S);` and line 2 is `ONE POINT MAKES INFINITELY MANY, SO L VANISHES AT S = 1.` Both use 2.5 mm caps from x = 15. One line would need ≈ 242 mm and would collide with the series caption. |
| S3(b) | rank-0 foil | **FIXED.** `A CURVE WITH FINITELY MANY / POINTS (11A1) HAS / L(1) = 0.2538, NOT ZERO.` |
| S3(c) | honest status | **FIXED.** `RANK = ORDER PROVED FOR THIS / CURVE (GROSS-ZAGIER 1986, / KOLYVAGIN 1988); FULL FORMULA / CHECKED BY COMPUTATION; / OPEN IN GENERAL.` |
| S3(d) | column edge on 204.6 or 282 | **FIXED.** The right edge is 282.00, with no ink past 282. The column spans x 228.72–282.00 and is 14.23 mm clear of the lower arm. Its last baseline, 19.8, is shared with the ziggurat caption. |
| A2 | cut notes 1–4; declared crop; series caption | **FIXED.** The notes are gone, and the text at x < 140, y 250–375 is 0 samples. The ray crop is y = 368.4 = grid(81), the type grid's baseline two leads under the statement's last baseline. That is the title band's clearance line, so the crop shares the band's grid. `MILLENNIUM PRIZE PROBLEMS 7 / 7` / `CLAY MATHEMATICS INSTITUTE, 2000` is set at 2.0 mm caps, with its right edge at 282.0 and its cap line at 383.5, the same as the statement's cap line. |
| A3 (gate) | min near-parallel gap ≥ 0.80 in the gcode; kern 10/20/30 | **FIXED.** The heavy 2nd passes are trimmed (chords 6, 7: 7.0 → 11.3 / 11.5 mm). All gap floors carry a 0.015 mm guard for `_poly`'s 0.01 mm gcode grid. Without the guard, the exact 0.800 design gaps plotted at 0.792–0.799. `gapcheck.py` on the v7 gcode finds **0 near-parallel runs ≥ 1 mm under 0.80**. The check measures exact point-to-segment gaps, with the foot on the other line's ink, over layers 0, 1, 3 and 4. The 3 shallow contacts it lists are touches (≤ 0.026 mm): ray ends on the arm, and one notch butt join. Ziggurat indices 10/20/30 are kerned +0.35 mm. |
| A4 | r01 furniture | dropped (ledger) |
| S4 | §11.1 "1–7" vs formula | argued/closed (ledger). The formula is kept, with the +0.015 guard. |

## What changed from parent (composition moves)

1. **Two acts, nothing between them that explains.** The numbered notes 1–4 are deleted. The left half now holds only the fan, the egg and the ziggurat. The fan's top crops on the title band's clearance line (grid 81).
2. **The crossing is the second act.** The gold stretch is a 1.4 mm band. The rest of L drops from 0.5 to 0.3, so the gold outweighs everything right of the branch.
3. **The hub keeps what belongs to P.** The tangent now leaves the 7 mm circle like chords 2, 3, 5, 6 and 7, and the egg yields to it. Near P, where the orbit meets the egg at 3–9°, the egg is carried by its own chords: eight 2 mm own-line notches joined into the curve. The egg's last ≈ 18 mm on each side of P now reads as a line that changes nib wherever a rational point lands.
4. **The words confirm the cause.** The statement under the title (from r01) carries the causal clause. The right column gains the 11A1 foil and the honest proof status. The ziggurat caption's ln 10 error is fixed. The series caption from r01 sits top-right.
5. Unchanged from r02: the 60 exact chords, the tiers, the 29.5 mm gap (0 ink), the 52 mm/unit scale, L's geometry, the ziggurat strings, 5 layers and 3 physical swaps. One exception: the hub-LOD gap is 0.815 instead of 0.8, as a rounding guard. It moves some inner ray ends outward by ≤ 0.015/sin Δθ.

## Measurements / computations

- **Exactness.** The orbit ±61 is exact Fractions, and all of it is on E. All 60 chords are collinear with P (cross product = 0). The ziggurat strings are 30/30 exact; the lengths run 1, 1, 2, …, 40, 41, and line 30 is 20 + 20 digits.
- **L.** L′(1) = 0.30600 = 5.98692 × 0.05111. The minimum is −0.08924 at s = 0.480. L(2) = 0.38158. The crossing is at 17.014°.
- **Oval marks.** 42/62 in r02 → **53/62** in r03, counting P's gold disc. The breakdown is ray ends 42 + crossing stubs 3 + notch stubs 8, and 7 are argued (see S2a).
- **Egg right tip (x ≈ 101.6).** 7 chord strokes pass within 5 mm of the vertex, and 4 oval orbit points lie within 5 mm. Of those, −53 is marked by a 37° stub, and 53 and ±37 are floor-bound (0.47–0.72 mm off rays 4 / 20 / 21).
- **Type.** The closest type ink to any line ink is 4.85 mm.
- **Gap floor.** On the exact design geometry the minimum is 0.800 mm; on the plotted gcode, 0 runs are under 0.80.
- **Bounds.** Ink spans x 15.0–282.0 and y 15.0–401.96 (A3 portrait, margin 15).

## Plot budget

From `.venv/bin/python -m promptplot plot plate gallery/studio/millennium_bsd/current/pp_millennium_bsd_iterate_v7.gcode --layers 0,1,2,3,4 --batch-strokes 40 --paper a3:portrait --margin 15 --dry-run` (feed ≤ 500, dwell ≥ 1 s, F2000 travel, 90 s per swap):

| order | layer | pen | strokes | dry-run min |
|---|---|---|---|---|
| 0 | HAIR: fine chords 25–60 + their stubs + s-axis | black 0.1 | 62 | ~12 |
| 1 | CHORDS: medium 10–24, heavy 1–9 ×2, their stubs, L outside the gold | black 0.3 | 41 | ~11 |
| 2 | TEXT (same 0.3 pen, own layer) | black 0.3 | 1 510 | ~66 |
| 3 | CURVES: E(ℝ) (egg in 4 pieces between notches + both arms as one stroke through the vertex) | black 0.5 | 5 | ~2 |
| 4 | GOLD: P disc (6 rings) + crossing band | gold 0.7 | 7 | ~1 |

The total is 17.02 m drawn, 6.95 m travel and 15 955 commands. The dry-run ETA is **~99 min**, including the pen changes. There are 3 physical swaps (0.1 → 0.3 → 0.5 → gold). The job also pauses at the start and at the text layer, which uses the same pen. All layers are contiguous, and every stroke is batchable; the longest is one ray.

## Self-critique (rubric)

1. Hierarchy 8: fan + egg, then the gold disc, then the gold band, which now reads as a distinct mark in the right half.
2. Grid & alignment 8: one 15 mm left edge. The 282 right edge holds the series caption and the column. The crop is on grid 81, and the bottom baseline is shared.
3. Tension 8: unchanged from r02, an off-centre hub with cropped rays.
4. Negative space 8: the notes' removal restored the left field's silence.
5. Craft 7: the floor passes, and the true-width hub crop shows no floods. **Risk:** near P the egg is now beaded, with 0.5 fragments between 0.1 / 0.3 notches. At arm's length that can read as a dashed or broken egg, not as "marks".
6. Concept 8: the statement and the foil now say "zero because infinite". The science is on the sheet in words and in ink.
7. Depth 7 (declared flat).

**The single worst thing:** S2(a) stops at 53/62, not 60. The 7 unmarked points are geometry, not choice: two sit under the gold, two in the tangent's osculation, and three at the egg tip, inside the 0.8 floor of a lower ray. Reaching 60 would need either a break in the 0.8 mm floor or a mark that is not an own-line stub, such as a tick or circle, which SYNTH forbids. The notch beading near P is the price of the 8 shallow marks. A critic may prefer the clean r02 egg.

## Engine requests
- `_poly` rounds to 0.01 mm. A piece that designs to a floor must add a guard. An exposed `precision=` argument, or 3-decimal emission, would remove that need.
- `suppress_parallel(fixed=...)` (carried from r02).
- `render_candidate.py --pen-widths` (carried; this round ships `render_truewidth.py`).
