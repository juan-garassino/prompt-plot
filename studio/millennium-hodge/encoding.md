# millennium-hodge — encoding (VISUAL TRANSLATOR)   · Status: encoding v1 · 2026-09-28

Source of truth: `studio/millennium-hodge/dossier.md`, visual truth **(a) A CIRCLE IS TWO STRAIGHT
LINES** (rank 1), with **(b)** (p,q) windings as the faithful thesis's lower row. (c) Clebsch is
not built. Reference: `ref/reference.png`, an AI poster. It is an interpretation brief only and is
never traced (`studio/AUTHORING.md`). No FEEDBACK.md, BRIEF.md or LEDGER.md exists yet. This is
plate 5 of the MILLENNIUM series. Two theses are built in parallel, **faithful** and **abstract**.
§1–4 and §6–11 bind both, and §5 gives one composition per thesis.

The view numbers below come from a translator's sketch study, which used the exact ray–quadric
visibility test described in §10. The study scripts are in the session scratchpad and are not
piece code. Designers re-measure every number in their own piece.

---

## 1. STYLE assignment

**CONSTRUCTIVISM, Gabo/Pevsner spatial branch** (the *Realistic Manifesto*, 1920: "we renounce
volume… we affirm depth as the only plastic form of space"). It is **not** the Rodchenko
poster branch. The series palette (cream, blue, gold) replaces black and red.

The canon was chosen because its ORDER fits the mathematics. STYLES.md §8 gives
Constructivism's order as **diagonal thrust and counter-thrust**. A doubly ruled quadric is
exactly that: every blue string leans at +45° to the horizontal circles and every gold string
leans at −45°, and the surface is nothing but those two opposed families. The canon's crossing
diagonals are also the plate's punchline, the X at ψ = 90°. The spatial branch adds the
second rule, which suits this subject: volume is never outlined, and depth is made only by
tensioned straight lines. The surface is therefore never contoured. Its curvature exists only as
the envelope of its strings.

**Depth is the default and it is kept.** The plate uses a true orthographic 3D view with exact
hidden-line removal. Nothing is declared flat except the type.

**Lineage:** Naum Gabo, *Linear Construction in Space No. 1* (1942–43, Tate T00191). The order it
lends is a curved surface made only of straight strings, with a lens-shaped void bounded by string
envelopes. The plate's see-through "eye" (§5) is Gabo's void, produced by the mathematics.
Second conversation (in NOTES only): Man Ray's *Objets mathématiques* (1936), the Poincaré models
Gabo's stringing came from. **Mohr is not used**: millennium-p-vs-np already answers Mohr, and
two plates in one batch must not share a lineage. Mohr would only return if the Clebsch plate (c)
is ever built as a separate piece.

## 2. The one-glance statement

> **A circle, slid through its family, becomes two straight strings, and to cohomology it
> never changed.**

At 3 m the viewer sees a luminous blue-and-gold string construction with a hole of bare paper
through its middle, a bundle of green loops pinched to a single point, and one heavy blue and
gold X crossing at that point. At 30 cm they read `○ = ╱ + ╲` and find that it is a theorem.

## 3. The abstract ORDER

**INTERLACED (two opposed ruling families) carrying a NESTED FAN (the conic pencil hinged at p,
closing onto the X).** It is not a figure: nothing is plotted against an axis. It is not an
illustration either: the only object on the sheet is the variety itself, whose real points are
the strings.

Exact mapping, one line each:
- "**Blue is [A], gold is [B], green is a sum of both, so a curve's colour is its class.**"
  Green is the subtractive mix of blue and yellow, so the mix is the algebra.
- "**Every green curve is [A]+[B]. The last one IS one blue string plus one gold string.**"

## 4. Channel mapping (Tufte: nothing drawn that encodes nothing)

Surface: **x² + y² − z² = 1, clipped at |z| ≤ H = 2** (rim radius √5, and each string turns
2·arctan 2 = 126.87° of azimuth).

| ink on paper | encodes | exact rule / range |
|---|---|---|
| **blue string** | one line of family A: A(α,s) = (cos α − s sin α, sin α + s cos α, s), a cycle of class [A] | **N = 96** strings, α_i = α₀ + 2πi/96 with **index 0 at α₀ = the hinge p**. Each visible run is **one straight G1**, rim to rim, cut only by visibility and LOD (§10). Blue 0.2, 1 pass. |
| **gold string** | one line of family B: B(β,s) = (cos β + s sin β, sin β − s cos β, s), class [B] | Same rule, β_j = α₀ + 2πj/96. Gold 0.2, 1 pass. |
| string density, silhouette thinning | none. It is the real envelope of the rulings (the surface is never outlined) | The strings thin by **halving LOD** where same-family spacing drops below 0.8 mm (§10). The contour is implied by where strings end. |
| **green curve** | a real algebraic curve of class a[A]+b[B] with a,b ≥ 1 | Green 0.5, 1 pass, resampled at ≤ 0.3 mm chord error. It lies on the quadric to machine precision. |
| **the pencil** (hero): 6 green curves through p | the plane z = tan ψ·(x−1) rotated about ℓ (the tangent line at p), **every member of class [A]+[B]** | ψ = **0°** (the waist circle), **15°** (ellipse), **31.72° = ½·arctan 2** (the last whole ellipse, which kisses the bottom rim at z = −2), **45°** (parabola), **60°, 75°** (hyperbolas). Open members **exit through the rims and are never closed**. |
| **the X**: blue string index 0 and gold string index 0, **3 passes** each | the ψ = 90° member, the tangent plane x = 1 cutting y = ±z: A(α₀) ∪ B(α₀), class [A]+[B] | These are the same two strings as index 0, drawn at weight: 3 passes offset 0.15 mm, about a 0.5 mm band. They are the only weighted strings, and they survive every LOD level, rim to rim. |
| **the point p** | the base point of the pencil, where the circle and the X meet | **It is not drawn.** It is the crossing of the X and the pinch of the green loops. There is no disc, dot or ring. |
| **the eye**: bare paper through the throat | the see-through channel: lines of sight that miss the clipped surface entirely. It is real geometry and it exists only for elevation > 41.8° at H = 2 | No ink, ever. It is the plate's quiet zone. |
| (faithful row) **green (p,q) curve** in a small copy of the model | α = q·u + c₁, β = p·u + c₂, **class p[A]+q[B]**, degree p+q | Cells: **[A]** (blue index-0 string at 3 passes), **[B]** (gold index-0 string at 3 passes), **[A]+[B]** (green waist circle), **[A]+2[B]** (p,q = 1,2, the twisted cubic), **2[A]+3[B]** (2,3, the rational quintic). The phase c₁ (with c₂ = 0) is free, because every phase gives a curve of the same class (it is a projective automorphism of ℙ¹×ℙ¹). Pick the phase that maximises the visible arc. Measured at e = 50° with the viewer at azimuth 0: (1,2) c₁ ≈ 55°, (2,3) c₁ ≈ 90°, which gives 0.68 and 0.64 of the parameter visible against the 0.705 inside the rims. |
| **rebus** `○ = ╱ + ╲` | [circle] = [A] + [B] in H²(Q, ℚ), **as classes, not as sets** | The circle glyph is green, `╱` is blue, `╲` is gold, and `=` and `+` are black text. The slants copy the on-sheet slants of the X's blue and gold strings. It replaces the reference's "Σ aᵢCᵢ = [Z]". |
| class tags **[A]**, **[B]** (text layer) | the names of the two generators | One each, at the upper rim end of the X's blue and gold strings, outside the weave. |
| **not encoded (declared)** | complex points (the complex quadric is S²×S²; its real points are the torus drawn), H^{p,q} as a shape, any open case | These are stated in the captions only (§10). |

## 5. Composition sketch — A3 portrait 297 × 420 mm, margins 15, y measured UP from the bottom edge

**Shared view (house law: one projection basis per sheet).** Orthographic projection.
- The viewer is at azimuth 0° and **elevation e = 50°**. The allowed range is 48°–54°. The
  elevation must stay ≥ 3° away from 45°, because at 45° some strings project to points.
- The hinge is **α₀ = 235°**: p = (cos 235°, sin 235°, 0), which puts p on the back wall 55° off
  the back centre. It is seen from inside, through the top opening.
- In this view the X's gold string runs essentially rim to rim (about 95% visible). The X's blue string
  crosses p with a shorter lower arm (about 88% visible). The pencil is about 90% visible, and the
  eye opens to about 2.0k × 0.83k (76 × 31 mm at k = 38).
- The front-flank alternative (α₀ ≈ 315°, e ≈ 40°) shows a complete X but loses both the nested
  loops and the eye. It is **rejected**.
- Screen roll ρ is per thesis. Every sub-model on the sheet (the row cells) uses the identical e,
  α₀-frame and ρ. A cell shrinks its k, and never its projection.

### 5F — FAITHFUL (the reference's architecture, every form replaced by a real one)

- **Hero:** k ≈ 38 mm per unit and ρ = −12°. The axis leans the way the reference's ribbon leans,
  and the gold X-string becomes the steep thrust at about 54°. The hero is fitted inside
  **x ∈ [95, 282], y ∈ [140, 378]**, centred near (190, 258). Designers set k to fill that box
  (36–38).
- The eye sits just right of and below the sheet's centre-right, at about (195, 250). p sits at
  the eye's upper-left.
- **Title** "HODGE / CONJECTURE" is on two lines of spaced caps, 9 mm, flush-left at x = 15, with
  baselines at 396 and 382.
- **Statement** is on two lines at 2.8 mm, baselines 370 and 364: `IN COHOMOLOGY A CIRCLE /
  IS TWO STRAIGHT LINES.`
- **Left column** is x ∈ [15, 88] and flush-left. It never enters the weave.
  - y ≈ 300–345: the conjecture, verbatim in meaning, with *rational* and *projective* stated.
  - y ≈ 262: `H^k(X,C) = ⊕ H^{p,q}`, labelled "(TEXT, NOT A SHAPE)" in words: "THE HODGE
    DECOMPOSITION — BOOKKEEPING, NOT DRAWN".
  - y ≈ 190–220: the key, which reads "BLUE, GOLD: THE TWO FAMILIES OF LINES [A], [B]. GREEN:
    A CURVE OF CLASS a[A]+b[B]."
- **Top-right corner caption** is flush-right at x = 282, y ∈ [398, 405]: `REAL POINTS OF
  X²+Y²−Z²=1 · |Z| ≤ 2 · ORTHOGRAPHIC`.
- **Row:** a header at baseline 124, flush-left: `EVERY CURVE ON IT IS a[A]+b[B]`.
  - Five cells, each with its box in y ∈ [60, 114]. Each is 44 mm wide, and x is
    15 + i·55.75 (i = 0…4), so the row runs flush with both margins.
  - Each cell is the same model at k ≈ 9 with **N = 16** strings per family. Its waist spacing is
    2.5 mm.
  - Captions are flush-left under each cell: the class at 2.4 mm caps (baseline 51), and the name
    at 1.8 mm caps (baseline 46): LINE · LINE · CONIC · TWISTED CUBIC · QUINTIC.
- **Footer:** the rebus is flush-left at x = 15, y ∈ [18, 36], with the circle at Ø 18 mm. The
  honesty line is flush-right at x = 282, on two lines at 2.2 mm, baselines 28 and 22:
  `EVERYTHING DRAWN IS A THEOREM (LEFSCHETZ 1924). / THE OPEN CASES BEGIN IN REAL DIMENSION 8.`
- **Dominant mass:** the hero is about 32 000 mm² against about 8 600 mm² for the whole row
  (≥ 3.7 : 1), and about 19 : 1 against any single cell.
- **Quiet zones:** the eye, and the left column below the key (y ∈ [140, 185]).
- **Reference → faithful mapping:**

  | reference shows | faithful draws |
  |---|---|
  | hand-swept twisted ribbon (no variety) | the string hyperboloid x²+y²−z²=1, never outlined |
  | blue = "Hodge structure", gold = "algebraic cycles" | blue = [A] and gold = [B]: **both** are algebraic cycles. H^{p,q} appears only as text |
  | gold stepped "fins" on the right | **cut** |
  | dashed axes and dotted construction circles | **cut** (no axes) |
  | the central hole of the ribbon | **the eye**: a real see-through channel |
  | row C₀…C₄ (sphere, torus, genus-2, blobs) | row [A], [B], [A]+[B], [A]+2[B], 2[A]+3[B]: genuine curves on the same surface |
  | row a₁C₀+a₂C₁ … Σ aᵢCᵢ = [Z] over overlapping blobs | **cut**. The hero's pencil *is* the sum, and the rebus states it |
  | italic captions, left and right columns | one flush-left column at x = 15, plus one corner caption |
  | footer tagline between rules | the honesty line (no rules) |

### 5A — ABSTRACT (one construction, swallowing the frame)

- **Hero only, no row.** Here k ≈ 60 and ρ = −25°, with the centre near (165, 215).
- The construction **crops at the left frame (lower-left) and the right frame**. Strings end
  exactly on the drawable frame line (x = 15 / 282), and this is a stated crop, not a rim.
- The gold X-string runs as one **unbroken straight thrust at about 41°**, from the lower-left crop
  to the upper-right rim. It is the longest single line on the sheet. The blue X-string crosses it
  at about 153° as the counter-thrust.
- The eye is about 120 × 50 mm and tilted −25°. It is the sheet's quiet centre. The green loops
  wrap it from p.
- Title "HODGE / CONJECTURE" is at 10 mm spaced caps, flush-left x = 15, baselines 398 and 384.
  The statement is at 372.
- The **rebus is set large**, 30 mm tall, flush-left at x = 15, y ∈ [318, 348], in the paper
  triangle above the construction's upper-left envelope. Its `╱` and `╲` are parallel to the real
  X strings below. This is Constructivist giant type whose strokes are the data.
- The bottom band is y ∈ [15, 42]. The colophon is flush-left there (the conjecture and the
  honesty line, 2.2 mm), and the corner caption is flush-right.
- **Dominant mass:** the construction, about 70% of the sheet. The rebus is the clear second
  element and the eye is the third.
- **Quiet zones:** the eye and the upper-left triangle around the type.
- Before the title is placed, designers must check that the upper-left paper triangle is really
  empty. If the top hyperbola intrudes, lower k, and never halo-punch.

## 6. Pen budget — 4 inks, 4 layers (no cap, layer discipline)

| order | layer | physical pen | meaning |
|---|---|---|---|
| 1 | GOLD | ochre/gold **pigment fineliner 0.2** (not metallic gel, because gel is ≥ 0.5 mm and floods the envelope) | family B, the [B] cycles. It includes the X's gold string (3 passes) and the rebus `╲` |
| 2 | BLUE | ultramarine fineliner 0.2 | family A, the [A] cycles. It includes the X's blue string (3 passes) and the rebus `╱` |
| 3 | GREEN | deep green 0.5 | sums a[A]+b[B]: the pencil, the row curves, and the rebus circle. It is the one loud accent and it is scarce (about 3–5 m against about 25–36 m of strings) |
| 4 | TEXT | black 0.3, its own layer | title, statement, captions, tags, and the rebus `=` / `+` |

The order runs light to dark: green lands over the weave and black lands last. Each layer is
entered once, which gives **3 swaps**. Text never sits on the weave. Where a tag has to approach
string ends, a text halo (pad 1.4 mm) is cut from the **strings** at compile time. This is the
house text-halo law, and it is the only place any string is interrupted for a non-geometric
reason.

## 7. Expressive levers (one decision each)

- **Proportion:** hero : row ≥ 3.7 : 1 (F). In A the construction swallows the frame. In both, the
  eye is the only large blank inside the construction.
- **Fill vs void:** the weave is the fill. The void is the eye, which is not a leftover: it is the
  exact set of sight-lines that miss the surface. Paper outside the envelope is left untouched.
- **Density gradient:** there is no cosmetic ramp. The only gradient is the real one, spacing
  collapsing toward the envelope and the eye's corners, which the LOD turns into a halving fringe.
- **Colour play:** blue and gold interleave at equal weight and read optically as one surface.
  Green is their mix and the only loud colour. The X is the one place blue and gold go heavy.
- **Texture direction:** the strings run at ±45° to the circles, so they fight the green loops
  cross-grain everywhere. That keeps green legible without a single occlusion gap.

## 8. The twist

**What the viewer holds:** squaring the circle is the proverb for the impossible, and a circle is
the one figure with no straight part.

**What the mechanism breaks:** on this surface one continuous algebraic family carries the circle,
through ellipses, a parabola and hyperbolas, onto a pair of straight lines. In cohomology the class
never moves: [○] = [A] + [B]. The circle is not *made of* the two lines. It is *equal to them as a
class*. That quietly corrects the misconception (dossier §5) that the conjecture is about
assembling shapes, because "represented" is far looser than "built from". The rebus is the joke,
and the pencil proves it.

## 9. Forbidden list (binding on both theses; the science critic fails any of these)

1. **Any drawn surface outline, rim ellipse, silhouette contour or shading.** The model is only
   strings, and rims are implied by string ends. (The rims are themselves [A]+[B] conics, and
   drawing them green would add two false pencil members.)
2. **A curved or bent string.** Every blue or gold run is one straight G1.
3. **Ribbons, blobs, fins, spheres, tori or genus-2 shapes**, anything labelled C₀…C₄, and
   "a₁C₀ + a₂C₁" or "Σ aᵢCᵢ = [Z]" over decorative shapes.
4. **A colour or swatch assigned to H^{p,q}, "Hodge structure" or "cohomology".** Blue and gold
   are both algebraic cycles.
5. **Closing an open curve.** Hyperbola, parabola and (p,q) arcs end at the rims (or at the frame
   crop, in A).
6. **A dot, disc or ring at p**, or any "focal" ornament. The crossing is the node.
7. **Axes, dashed centre lines, dotted orbits, construction circles, arrows, leader lines or a
   legend box.**
8. **Crossing-count invitations**, such as tick marks at intersections or numbered hits.
9. **"Every shape is assembled from simple shapes"**, "Z" for coefficients, "Kähler" for
   projective, or any claim that the plate shows an open case or a non-algebraic Hodge class.
10. **Ink in the eye**, or text on or haloed into the weave beyond the tag halos in §6.
11. **Punching holes to relieve crowding.** Crowding is resolved only by LOD, pause-resume and the
    pencil stagger (§10).
12. (F) **Row cells in a different projection** than the hero. (A) **Any second hero, row or
    inset.**

## 10. Fabrication (Leo: F600 is about 10 mm/s, and each pen cycle with dwells is about 2.5 s)

- **Visibility is exact, not a z-buffer.** A sample P is visible iff the ray P + t·v (t > 0)
  meets no root of (P+tv)·diag(1,1,−1)·(P+tv) = 1 with |z| ≤ 2. This is a closed-form quadratic.
  Runs are split where visibility flips, and each split is bisected to 0.01 mm. This keeps every
  string a straight run.
- **Spacing floor:** 0.8 mm, which is ≥ 2.4 × 0.2 = 0.48.
  - Waist perpendicular spacing is 2π·k/(96√2): 1.76 mm (F, k = 38), 2.78 mm (A, k = 60), and
    2.5 mm in the row cells (k = 9, N = 16).
  - **String LOD by halving:** where a string's projected distance to its same-family neighbour
    falls below 0.8 mm, only strings with index ≡ 0 mod 2 continue. The next level keeps
    ≡ 0 mod 4, then mod 8. Silenced strings **pause and resume** (`Scene3D.lines(mode=
    "pause_resume")`) rather than dying, with at most two extra runs per string.
  - Index 0 (the X) survives every level.
  - Any cross-family pair that is near-parallel (|cos| > 0.93) and closer than 0.8 mm yields the
    later-drawn stretch (`material.suppress_parallel` semantics).
- **Pencil stagger (the "halo around p", done structurally):** all six conics are tangent to ℓ at
  p.
  - The circle (ψ = 0°) and the X reach p.
  - Each other member stops at the radius where its gap to the nearest continuing member falls
    below 0.8 mm + nib.
  - Measured along strings at k = 38, the gaps reach 1.2 mm at about 16 (0°/15°), 13 (15°/31.7°),
    12 (31.7°/45°), 8 (45°/60°) and 5 mm (60°/75°) from p. The stops are staggered, so the loops
    visibly pinch into p.
  - Strings are **not** cleared around p. They are not congested there, and clearing them would
    be a punched hole.
- **Green over strings:** crossings are allowed, since they are points and the ±45° weave meets the
  loops cross-grain. Only near-parallel shadowing (under 0.8 mm for over 3 mm) cuts the string
  locally.
- **Batching:** strings are drawn in index order and boustrophedon (i top→bottom, i+1
  bottom→top), so each stroke starts next to where the last one ended. There is a batch boundary
  and re-zero check every 12 strings. Green is drawn ψ ascending, then row cells left to right.
  Text is drawn line by line. No stroke is longer than about 330 mm (A), and none crosses the sheet
  on travel.
- **Estimated time on A3** (visible string length is measured before LOD trimming; designers report
  real numbers in HANDOFF):

  | layer | faithful | abstract |
  |---|---|---|
  | GOLD | hero about 12 m + row 2.4 m, about 370 runs → about 24 + 15 = **39 min** | about 18 m after crop, about 220 runs → about 30 + 9 = **39 min** |
  | BLUE | same → **39 min** | same → **39 min** |
  | GREEN | about 3 m, about 20 strokes → **6 min** | about 4.5 m, about 12 strokes → **8 min** |
  | TEXT | about 450 glyph strokes → **20 min** | about 300 → **13 min** |
  | **total** | **about 105 min, 3 swaps** | **about 100 min, 3 swaps** |

- **Leo A5 (×0.5):** hero waist spacing is 0.88 mm (F) and 1.39 mm (A), so the floor still holds.
  Row cells at k = 4.5 would be 1.25 mm, which is fine. The pencil stops halve too, and the rule
  is re-run and never scaled. Text stays ≥ 1.8 mm caps (A3) and ≥ 1.4 mm on A5. The pen-up frame
  trace comes first.
- **Flood risks:**
  - The envelope and the eye corners are handled by the LOD.
  - The X's 3-pass band against neighbour strings is fine: index ±1 sits 1.76 mm off at the waist,
    leaving ≥ 1.2 mm of paper.
  - The p pinch is handled by the stagger.
  - Gel gold is banned.
- **Captions** (stroke font: author missing glyphs such as [ ], ², ⊕, ± and the slash strokes, as
  the yang-mills Δ was authored). Content is fixed and the wording may be tightened:
  - Conjecture: `X SMOOTH COMPLEX PROJECTIVE. IS EVERY RATIONAL HODGE CLASS — H^{2p}(X,Q) ∩ H^{p,p}
    — A RATIONAL COMBINATION OF CLASSES OF SUBVARIETIES? (CLAY · DELIGNE)`
  - Key: `REAL POINTS OF THE COMPLEX QUADRIC P1×P1. BLUE, GOLD: ITS TWO FAMILIES OF LINES [A], [B].
    GREEN: CURVES OF CLASS a[A]+b[B]. HERE EVERY CLASS IS HODGE AND ALGEBRAIC.`
  - Honesty: `EVERYTHING DRAWN IS A THEOREM (LEFSCHETZ 1924). THE OPEN CASES BEGIN IN REAL DIMENSION 8
    AND CANNOT BE DRAWN.`
- **Lineage line (HANDOFF/NOTES):** `lineage: Naum Gabo, Linear Construction in Space No. 1
  (1942–43). Order taken: a curved surface made only of straight strings, with a void bounded by
  their envelopes. Here the strings are the algebraic cycles and the void is the see-through
  throat.`

## 11. Acceptance checks (the art critic marks each PASS/FAIL on the png; the science critic re-runs the gcode checks)

1. **ONLY STRAIGHT STRINGS, NO OUTLINE.** Every blue or gold run is straight: in the gcode, each
   run's points are collinear within 0.01 mm. On the png, no curve of blue or gold appears
   anywhere, and there is no rim, contour or shading line. The silhouette is readable only as
   string ends thinning in halving steps, with no solid blue or gold band anywhere (same-colour
   gap ≥ 0.8 mm).
2. **ONE PINCH POINT.** All six green curves and both X strings meet at one point. At 30 cm the
   green loops visibly narrow into it at staggered lengths, with no green blot. The circle and the
   X both touch it.
3. **CIRCLE TO X, IN ORDER.** Read outward from p: a closed circle, then closed ellipses (the
   31.72° one grazing the bottom rim's string ends), then open curves leaving through the rims,
   then the heavy blue and gold X. No open green curve is closed back or ends mid-surface except
   at its stagger stop near p.
4. **THE EYE.** A lens of bare paper passes through the throat. It is bounded only by string
   envelopes, contains zero ink, and is ≥ 28 mm tall (F, A3) or ≥ 45 mm tall (A).
   - (F) The five row cells show the same eye shape and tilt as the hero, scaled.
   - (A) The gold X-string is the longest straight line on the sheet and is uninterrupted from
     crop to rim.
5. **HONEST ROW AND HONEST WORDS.**
   - (F) The captions read exactly [A], [B], [A]+[B], [A]+2[B], 2[A]+3[B]. The cubic and the
     quintic each visibly leave through a rim (|p−q| = 1), and no cell shows a closed blob.
   - (Both) The text contains "RATIONAL", "PROJECTIVE", "THEOREM (LEFSCHETZ 1924)" and "REAL
     DIMENSION 8".
   - (Both) No colour is attached to H^{p,q}.
   - (Both) The rebus reads green ○ = blue ╱ + gold ╲, with the slants parallel to the X.
