# millennium-hodge r01 — faithful · parent: none · 2026-09-29

lineage: Naum Gabo, *Linear Construction in Space No. 1* (1942–43, Tate T00191). Order taken: a
curved surface made only of straight strings, with a void bounded by their envelopes. Here the
strings are the algebraic cycles and the void is the see-through throat. Second conversation (notes
only): Man Ray, *Objets mathématiques* (Cahiers d'Art 1936), the Poincaré-Institute string models.
Style: CONSTRUCTIVISM, Gabo/Pevsner spatial branch (encoding §1). True orthographic 3D with exact
hidden-line removal. Only the type is flat.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-hodge/rounds/r01/piece.py \
  --fn hodge_circle_is_two_lines_faithful --seed 7 --paper a3 --margin 15 \
  --palette darkgoldenrod,royalblue,darkgreen,black \
  --out gallery/studio/millennium_hodge/trials/pp_millennium_hodge_faithful_v7.png
```

- final (A3 portrait): `gallery/studio/millennium_hodge/trials/pp_millennium_hodge_faithful_v7.png` / `.gcode`
- Leo (A5 portrait, margin 10, same command with `--paper a5 --margin 10`):
  `gallery/studio/millennium_hodge/current/pp_millennium_hodge_faithful_v8.png` / `.gcode`. The LOD, declutter and stagger
  floors are re-run in paper mm, not scaled.
- physical-width preview (each pen at its nib width on cream): `phys_preview_v7.png` in this
  folder. The stock preview draws every 0.2 mm string at one fat width, so the weave looks about
  3× darker there than it will on paper.
- seed: 7. Nothing on the sheet is random, and `rng` is accepted only for the contract.
- trials: v1 used ρ −12°, no green yield and MIN_RUN 1.2. v2 moved to ρ −30°. v3 added authored
  ℚ/ℂ/∩ and N_CELL 32. v4 added the declutter pass. v5 was a v4 rerun (only CAP_MIN changed, same
  geometry). v6 was the A5 test (overlapping captions found there). v7/v8 are final.
- a render takes about 90 s: the exact visibility is bisected per string.

## Mandate responses

This slug has no LEDGER.md or FEEDBACK.md, so **there are no open J/A/S mandates**. The binding
brief is encoding §4/§9/§11 plus the curator note. Every check below was run on the **gcode
itself** (a parser splits G1 runs per colour; scripts are in the session scratchpad at
`hodge_f/{check,eye,science}.py`).

| id | requirement | status |
|---|---|---|
| §11.1 ONLY STRAIGHT STRINGS, NO OUTLINE | every blue/gold run is one straight line; no rim, contour or shading; same-colour gap ≥ 0.8 mm | FIXED: **0 of 808 blue/gold strokes have more than one G1** (max deviation from straight 0.0000 mm). No rim or silhouette is drawn. Same-colour near-parallel (\|cos\|>0.93) under 0.8 mm: hero 58 mm gold + 39 mm blue out of 28.4 m (0.3 %), closest 0.60 mm (≥ 0.48 = 2.4 × nib, so no flood). These are sampling residues of `suppress_parallel`'s 0.3 mm point grid at the fold tips |
| §11.2 ONE PINCH POINT | 6 green curves and both X strings meet at one point; staggered stops; no blot | PARTLY, see Self-critique. The circle and both X strings pass exactly through p (171.9, 285.8) mm. The five other members stop at the 1.3 mm floor (0.8 + green nib), measured from p along the sheet: 21.2 (15°), 13.8 (31.7°), 19.6 (45°), 8.1 (60°), 8.2 (75°) mm. Green–green near-parallel under 1.3 mm: 2.3 mm in total, closest 1.297 mm, so there is no blot. **ARGUED:** the pencil's left arms run from p behind the throat fold and come out on the outer wall as a fan at the eye's left tip, about 17 mm from p. That is exact hidden-line removal, not a second node, but at 3 m it reads as a second convergence next to p |
| §11.3 CIRCLE TO X, IN ORDER | closed circle → closed ellipses (31.72° grazing the bottom rim) → open curves through the rims → the X | FIXED: min z of the 31.72° ellipse is −2.0000, so it kisses the rim. The 45/60/75° members are open and leave through the rims. Nothing is closed back |
| §11.4 THE EYE | bare lens, zero ink, ≥ 28 mm tall; cells show the same eye | FIXED: the eye is 66.7 × 27.2 mm on its principal axes, **40.8 mm tall on the sheet**, tilted −30° (1 427 mm²). **0 ink samples inside** (eroded 0.25 mm, all pens). The cells use the identical projection, so their eye has the same shape and tilt |
| §11.5 HONEST ROW AND WORDS | captions exact; the cubic and the quintic exit a rim; required words present; no colour for H^{p,q}; rebus parallel | FIXED: captions read [A] · [B] · [A]+[B] · [A]+2[B] · 2[A]+3[B]. (1,2) and (2,3) each pass once through infinity and exit the rim. Text has RATIONAL, PROJECTIVE, THEOREM (LEFSCHETZ 1924) and REAL DIMENSION 8. H^{p,q} appears only in the black text layer. The rebus slashes are drawn at the measured X slants (blue −31.5°, gold +35.7°) with the same 3-pass weight |
| §9 forbidden 1–12 | | none present: no rim, contour or shading; no curved blue/gold; no blobs or C₀…C₄; no swatch for cohomology; no closed open curve; no dot at p; no axes, arrows or legend box; no ticks at crossings; no "assembled from", "Z" or "Kähler"; no ink in the eye; no punched holes (every string cut is LOD, visibility, parallel yield or the tag halo); cells use the same projection |
| curator | real parametrised surfaces; genuine cycles; honest about analogy; layers, order, minutes; lineage | Every mark is computed (proof under Measurements). The honesty line states that the open cases cannot be drawn. 4 layers in a stated order, with minutes below. Lineage is named |

## What changed from the reference (faithful = reconstruction plus stated layout fixes)

Kept from the reference: the hero leaning up-right in the upper two-thirds, a lens-shaped hole just
right of centre, a flush-left text column, a five-cell row under the hero, spaced caps top-left,
and blue + gold fine line on cream.

Layout fixes, each one a composition move:
1. **The ribbon becomes the variety.** The hand-swept ribbon is replaced by the real points of
   x²+y²−z²=1 (|z| ≤ 2), drawn only as its 2 × 96 rulings. Its envelope and the eye appear only
   where the strings end.
2. **The hole becomes the eye.** The reference's hole (measured 0.156 W × 0.060 H) is replaced by
   the exact set of sight-lines that miss the clipped surface. It is bigger (66.7 × 27.2 mm) and
   tilted with the construction.
3. **Blue/gold change meaning.** In the reference, blue ("Hodge structure") sits left at u 0.43
   and gold ("cycles") sits right at u 0.68. On this plate the colours interleave at equal weight,
   because both are algebraic cycles, [A] and [B].
4. **The right column, the gold fins, the dashed axes and the dotted construction circles are
   cut.** One flush-right corner caption states what is drawn.
5. **The row becomes genuine cycles.** C₀…C₄ (sphere, torus, genus-2, blobs) become the same
   model at k 7.97 showing [A], [B], [A]+[B], [A]+2[B] and 2[A]+3[B].
6. **The sum row is cut.** The hero's pencil *is* the sum, and the rebus ○ = ╲ + ╱ states it.
7. **The footer tagline between rules** becomes the honesty line, flush-right, with no rules.

Decisions beyond the encoding (argued):
- **Roll ρ −30° instead of −12°.** At −12° the blue X string lies at −13.5° on the sheet and the
  gold at +53.7°. The X then reads as a skewed cross, and the rebus's blue slash reads as a minus
  sign (seen in v1). At −30° the X is blue −31.5° / gold +35.7°: a true diagonal thrust and
  counter-thrust, and the rebus reads ○ = ╲ + ╱. The cost is k 33.9 instead of 37.7, because the
  rolled silhouette is wider. Waist spacing is 1.57 mm, still ≥ 0.8.
- **N_CELL 32 instead of 16.** At 16 strings the cells read as star-bursts, not surfaces (v2 crop).
  At 32 the cells are 1.11 mm at the waist and show the eye.
- **Hinge kept at α₀ = 235°.** I tried 180° and 200°. Both give *two* fans at both eye tips,
  because every pencil member crosses the throat fold. 235° keeps p and the one fan on the same
  end of the eye (probe in the scratchpad at `hodge_f/alpha.py`; the hero-only comparison image is
  `hodge_f/cmp_a0.png` there).
- **Two structural declutter passes after the LOD** (section 10 asks for both). The halving LOD
  only sees the adjacent same-family string. Where the throat folds, two sheets of the surface
  overlap on paper, and v3 measured 1.1 m of same-colour lines under 0.8 mm (closest 0.14 mm). Pass
  1 is `material.suppress_parallel` over both families. Pass 2 cuts string stretches that shadow a
  green curve or the X for more than 3 mm. Every surviving piece is still one G1.
- **MIN_RUN 4 mm.** A string run shorter than 4 mm on paper is dropped. v1 had 12 such crumbs,
  which read as a dashed eye rim.
- **Captions lead from their effective cap.** On A5 the 1.4 mm floor enlarged the small captions
  into each other (v6). Leads are now multiples of the rendered cap.

## Measurements / computations

Reference (colour masks b−r > 25 for blue, r−b > 45 & g−b > 20 for gold, a dark-text mask, and a
closed-mask BFS for the hole; u right, v down), from `hodge_f/measure_ref.py` in the scratchpad:

| element | u | v |
|---|---|---|
| hero colour mass | 0.238..0.918 | 0.032..0.500, centroid (0.540, 0.291) |
| blue / gold centroids | 0.431 / 0.681 | 0.290 / 0.293 |
| hero hole | 0.467..0.623 (0.156 W) | 0.284..0.344 (0.060 H), centre (0.538, 0.312) |
| title (2 lines) | 0.036..0.499 | 0.021–0.045, 0.057–0.087 |
| left column | 0.036..0.231 | 0.180..0.445 |
| right column (cut) | 0.809..0.971 | 0.029..0.455 |
| row C₀…C₄ | 0.128..0.927 | 0.573..0.663 |
| sums row (cut) | 0.058..0.838 | 0.716..0.839 |
| footer | 0.127..0.872 | 0.916..0.954 |

The mathematics, recomputed with `hodge_f/science.py`:
- Rulings lie on the quadric: max residual 2.7e-15 (A and B, 50 strings each).
- Pencil members lie on both the quadric (≤ 9.1e-13) and their plane z = tan ψ (n·X − 1)
  (≤ 2.1e-14). The X strings lie in the tangent plane n·X = 1 to 3.3e-16, which is the ψ = 90°
  member.
- ψ = 31.72° = ½·arctan 2: min z = −2.0000, the last whole ellipse inside the rims.
- (1,2): degree 3 (max 3 real plane hits in 300 random planes), 2 hits per A-string and 1 per
  B-string, so class [A]+2[B]. (2,3): degree 5, 3/2 hits, class 2[A]+3[B]. Each passes once
  through infinity. The fraction inside |z| ≤ 2 is 0.7048 = 2·arctan 2/π.
- Free phase c₁ (every phase gives the same class), chosen for maximum visible parameter: 290° for
  (1,2) and 30° for (2,3), in the α₀ frame.
- View: orthographic, azimuth 0, elevation 50°, roll −30°. Hero k = 33.87 mm/unit, fitted to x
  [95, 282]. Cells k = 7.97. Waist perpendicular spacing: hero 1.57 mm (N 96), cells 1.11 mm
  (N 32).
- Visibility is exact. For a surface point P, the second ray–quadric root is
  t* = −2 P·D·v / v·D·v (D = diag(1,1,−1)). P is hidden iff t* > 0 and |z(t*)| ≤ 2. Every
  visibility, LOD or halo flip is bisected to 2e-6 in s (about 0.0001 mm).
- LOD: g₁ = |P_α × P_s| / |P_s| · 2π/N on paper. The level m is the least power of 2 with
  g₁·m ≥ 0.8 mm, and string i draws iff i ≡ 0 (mod m). Index 0 (the X) is exempt.
- String counts: hero 320 LOD runs become 334 after declutter (the yields split some runs).

## Plot budget (A3, from the gcode; time = length at F600 + 2.5 s per stroke)

| order | layer | pen | strokes | draw | est. |
|---|---|---|---|---|---|
| 1 | GOLD | ochre pigment fineliner 0.2 | 407 | 14.29 m | 41 min |
| 2 | BLUE | ultramarine fineliner 0.2 | 401 | 14.09 m | 40 min |
| 3 | GREEN | deep green 0.5 | 24 | 1.36 m | 3 min |
| 4 | TEXT | black 0.3 | 935 | 3.35 m | 45 min |
| | total | 4 pens, 3 swaps | 1 767 | 33.1 m draw, 11.5 m travel, 13 259 commands | **~129 min** |

Leo A5 (v8): gold 22 min, blue 22, green 2, text 42 min, about 88 min in total. Text dominates on
A5 because its stroke count does not shrink. Batch boundary: gold and blue are emitted in index
order, boustrophedon. The pipeline's per-colour optimiser reorders strokes within a colour and
never across colours. Pen-up frame trace first.

## Self-critique (DESIGN_RUBRIC seven dimensions, 1–10)

1. Hierarchy — 7. The hero dominates (about 9× the row by area), the eye is the quiet centre and
   the rebus is a clear footnote. The heavy X (3 passes, about 0.5 mm) is correct to spec, but at
   3 m it hardly separates from the weave.
2. Composition / space — 7. The diagonal thrust is real, and there are blank bands top-right,
   around the hero and between hero and row. The hero-to-row band (about 40 mm) is slightly
   generous, because the hero is width-limited after the roll.
3. Line quality / plottability — 8. Every string is one G1. There is no flood (closest same-colour
   gap 0.60 mm, green 1.30 mm). A few fold-tip string ends are ragged (the halving fringe) but not
   dense.
4. Colour — 8. Blue and gold at equal weight give an optical grey-gold surface. Green is scarce
   (1.4 m) and is the only loud ink.
5. Type — 7. Spaced-caps title and a flush-left column. The stroke font is mechanical against the
   Gabo delicacy. The ·, ², ¹ glyphs are tiny at 2.2 mm.
6. Concept legibility — 7. Circle → ellipses → hyperbolas → X is readable, and the rebus lands it.
   The pinch at p competes with the fold fan beside it.
7. Exactness / honesty — 9. Every mark is a computed algebraic object, and the analogy and open
   cases are stated in words.

**The single worst thing:** the pencil does not read as ONE pinch point. The right-hand loops stop
8–21 mm short of p (the 1.3 mm floor for a 0.5 mm green), and the left arms emerge from behind the
throat fold as a fan about 17 mm from p. A viewer at 3 m sees convergence *toward the eye's
upper-left end*, not into the exact crossing of the X. Next round candidates: a finer green nib
(0.3 mm gives a 1.1 mm floor, so the stops move about 15 % closer), or an elevation / hinge search
that keeps the left arms in front of the fold.

## Engine requests

- **RuledLOD** (`scene3d`): the halving LOD for families of straight lines on a ruled surface
  (analytic neighbour gap from ∂P/∂α × ∂P/∂s, index-mod-2^L survival, exempt indices), sibling of
  `PolarLOD`. It is implemented locally in `string_runs`.
- **`suppress_parallel(..., keep_first=...)` / pre-registered occupancy**: a way to register
  priority paths (a hero line, a green curve) that are never cut and claim space before the
  length sort. The local workaround is the 3 mm shadow pass in `declutter`.
- **Exact quadric visibility** as a Scene3D camera mode, in place of the z-buffer, for
  analytic surfaces (the closed-form second root).
