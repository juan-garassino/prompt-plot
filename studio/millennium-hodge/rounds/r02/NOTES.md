# millennium-hodge r02 — abstract · parent: none · 2026-09-29

lineage: Naum Gabo, *Linear Construction in Space No. 1* (1942–43, Tate T00191). Order taken: a
curved surface made only of straight strings, with a void bounded by their envelopes. Here the
strings are the algebraic cycles and the void is the see-through throat. Second conversation (notes
only): Man Ray, *Objets mathématiques* (Cahiers d'Art 1936). Mohr is not used, because p-vs-np has it.
Style: CONSTRUCTIVISM, Gabo/Pevsner spatial branch. The order is diagonal thrust against
counter-thrust, and depth is made only by tensioned straight lines. True orthographic 3D with exact
hidden-line removal. Only the type is flat.

This round has no parent. An earlier interrupted session of this same abstract seat left a
`piece.py`/`audit.py` here and renders v1–v16 in Downloads, with no NOTES. I kept its machinery:
exact visibility, halving-LOD strings, pencil stagger, the stroke-font setter and the rebus. I
rebuilt the composition, which the "What changed" section below describes.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/millennium-hodge/rounds/r02/piece.py \
  --fn hodge_circle_is_two_lines --seed 7 --paper a3 --margin 15 \
  --palette darkgoldenrod,royalblue,darkgreen,black \
  --out gallery/studio/millennium_hodge/trials/pp_millennium_hodge_abstract_v25.png
```

- final (A3 portrait): `gallery/studio/millennium_hodge/trials/pp_millennium_hodge_abstract_v25.png` / `.gcode`
- physical-width preview (each pen at its nib width on cream): `phys_preview_v25.png` in this
  folder. The stock preview draws the 0.2 mm strings about 3× too heavy.
- Leo (A5 portrait, margin 10): `gallery/studio/millennium_hodge/trials/pp_millennium_hodge_abstract_v24.png` / `.gcode`,
  with its preview at `phys_preview_v24_a5.png`. It was rendered with the same command plus
  `--paper a5 --margin 10`.
- seed: 7. Nothing on the sheet is random. Seed 3 (v26) gives byte-identical gcode (diff = 0
  lines).
- the trials in this session:
  - v17: back-wall hinge 220°. The X opened, but the pinch read at the eye tip instead of at p.
  - v18: first front-flank view.
  - v19–v21: the paper-L layout, the type column, aligned rebus and title, rim-end tags and
    MIN_RUN 5.
  - v22: a superseded A3 render.
  - v23: A5, which floated off the crop.
  - v24: A5 final.
  - v25/v26: A3 final and the seed check.
- scratch scripts (hinge survey, silhouette rows, physical preview) are in the session scratchpad
  under `hab/`.

## Mandate responses

This slug has no LEDGER.md or FEEDBACK.md, so **there are no open J/A/S mandates**. The binding
brief is encoding §4/§5A/§9/§11 plus the curator note. Checks were run on the gcode with
`audit.py` (in this folder).

| id | requirement | status |
|---|---|---|
| §11.1 only straight strings, no outline | each blue/gold run is one G1; no rim or contour; same-colour gap ≥ 0.8 mm | FIXED: **0 of 399 blue/gold strokes have more than one G1**, and the worst deviation from straight is 0.0000 mm. No rim, silhouette or shading line is drawn. Same-colour near-parallel minimum: gold 0.79 mm, blue 0.78 mm. That is 0.02 mm under the floor, at two points where a visibility-bisected string end runs past the last LOD-tested sample. It leaves 0.58 mm of paper between 0.2 mm nibs, so there is no flood. ARGUED as residue |
| §11.2 one pinch point | 6 green curves and both X strings meet at one point, with staggered stops | FIXED **by moving the hinge to the front flank** (see "What changed"). The circle and both X strings pass exactly through p = (189.6, 119.7) mm. The other members arrive from **both** sides of p and stop at the 1.3 mm floor (0.8 plus the green nib). Stops, left/right of p: 60° at 12.0/12.5 mm, 31.7° at 20.1/20.3, 45° at 24.6/25.6, 15° at 31.0/30.4, 75° at 8.5/8.5. Green–green near-parallel minimum is 1.32 mm |
| §11.3 circle to X, in order | closed circle, then ellipses (31.72° grazing the rim), then open curves out through the rims, then the X | FIXED: min z of the 31.72° ellipse is −2.000000000000001. The 45°, 60° and 75° members leave through the rims or the frame crop, and nothing is closed back |
| §11.4 the eye (A) | bare lens ≥ 45 mm tall, zero ink; gold X the longest line, uninterrupted from crop to rim | Eye FIXED: **119.5 × 50.0 mm, 4 712 mm², with 0 ink samples**. Gold X is **PARTLY met, ARGUED**. It runs from the upper-left rim (tag [B], (72, 213)) to the right-frame crop, and at 268 mm it is the longest line on the sheet (the longest ordinary gold run is 189 mm). **It is interrupted once, for 14.3 mm at (158, 145)** (s 0.53–0.72), where it passes behind the throat's front lip. The blue X has the same kind of break, 14.4 mm at (234, 143). This is exact hidden-line removal. On the front flank every hinge from α₀ 330° to 360° has this lip gap at every elevation from 48° to 54° (8.1–8.4 mm at e 48, 14.3 mm at e 50, and wider as the elevation rises). The encoding's back-wall α₀ 235 also breaks the gold (s ≈ −0.5 to −0.25) and shortens the blue to a stub. I kept e 50 for the eye rather than going to 48, which sits on the 45° degeneracy margin (|cos 2e| = 0.105) |
| §11.5 honest words | RATIONAL, PROJECTIVE, THEOREM (LEFSCHETZ 1924), REAL DIMENSION 8; no colour on H^{p,q}; rebus parallel to the X | FIXED: all four phrases are set. H^{p,q} is not drawn and has no colour. The rebus ○ = ╱ + ╲ uses slants at 27.4° (blue) and −38.2° (gold), which copy the on-sheet X |
| §9 forbidden 1–12 | | none present. The tag halos are the only non-geometric string cuts, and no string is interrupted for type anywhere else |
| curator | real surfaces, genuine cycles, honest about analogy, layers, order, minutes, lineage | Every mark is computed (proofs under Measurements). The colophon says the open cases "CANNOT BE DRAWN". There are 4 layers with a stated order and minutes (below), and the lineage is named |

**Deviations from encoding §5A, argued:**
1. **The gold X descends (−38°) instead of rising (+41°).** With p on the back wall (encoding
   α₀ 235 and the earlier session's 250) the blue X is foreshortened to 1.2–2.0 units against
   gold's 5.3. On paper it was a 70 mm stub, so the X did not read as an X (earlier v15/v16).
   Worse, the pencil members vanish behind the throat fold and resurface at the eye's tip, which
   makes a *second* convergence 25–40 mm from p. That is the "second fan" r01 also reported. On
   the front flank (α₀ = 350°) both strings are long (gold 5.0, blue 4.0 units: 94–96 % visible)
   and every pencil member passes *through* p visibly, so the pinch sits on the X crossing. For
   gold to rise at 41° at this hinge the roll would have to be +91°, which lays the hourglass on
   its side on a portrait sheet. I kept roll 0. The encoding's own rebus glyphs (blue ╱, gold ╲)
   describe exactly this X.
2. **Encoding §5A rejected the front flank "α₀ ≈ 315°, e ≈ 40°" because it loses the eye.** That
   loss comes from the 40° elevation, not from the hinge: the eye exists for every hinge at
   e > 41.8°. At e = 50° the front flank keeps both the eye and the loops, which wrap it through
   the top opening.
3. **Rebus top-right on the title band (22.5 mm), not 30 mm in the upper-left triangle.** The
   rebus is 174 mm wide at 30 mm. The upper-left paper at this scale is a 45 mm column, so the
   rebus shares the title's band, from the lower baseline to the cap line, and aligns with it
   exactly.

## What changed from parent (no parent; from the interrupted session's v15/v16)

- **Hinge 250° → 350° (front flank), roll −35° → 0°.** The X becomes the hero: two long weighted
  strings crossing in the lower lobe, with the green pencil pinched onto the crossing from both
  sides. The eye stays above it as the quiet centre.
- **The construction is pushed to the bottom-right** (k 60, centre (200, 165)). It crops at the
  right frame (about 14 mm) and the bottom frame (about 30 mm) and swallows those two edges.
  Paper opens as an **L**: the top band (title + rebus) and a left column at least 45 mm wide.
- **The type becomes one flush-left column on x = 15** (44 mm measure). Each block drops into the
  first stretch of bare paper that clears the construction's envelope by 6 mm, tested with the
  exact see-through predicate:
  - the question hangs from the statement;
  - the key centres on the waist notch, the silhouette point (0, −1, 0);
  - the honesty line stands on the bottom margin.
- **Title and rebus share one band**: 8.5 mm caps with baselines 391.5 and 377.5, and the rebus
  runs from 377.5 to 400 flush-right. The weight passes are inset so nothing crosses the frame.
- **Tags sit at the rim end** of each X string, the end that the frame does not crop. [B] and [A]
  therefore both land in the left paper column beside the type.
- **The pencil stagger now uses the halving priority** (circle and X, then 60°, then 31.7°, then
  the odd members) and tests only near-parallel neighbours (|cos| > 0.9). A member that merely
  crosses another is a point, not a flood. This is what keeps the A5 right-hand arms from being
  eaten by far crossings.
- **String crumbs under 5 mm are dropped** (MIN_RUN; the earlier value was 3). The fringe along
  the eye had read as a dashed rim.
- On small paper the construction shrinks about the bottom-right frame corner, so the crop
  survives and the type column widens by what the 1.4 mm type floor needs.

## Measurements / computations

- **View:** orthographic, azimuth 0, elevation 50°, roll 0°, hinge α₀ = 350°, H = 2, N = 96 per
  family, k = 60 mm/unit. The waist perpendicular spacing is 2πk/(96√2) = 2.78 mm.
- **Hinge survey (at e 50):**

  | α₀ | gold : blue visible length (units) | note |
  |---|---|---|
  | 250 | 5.35 : 1.18 | |
  | 235 | 5.27 : 2.03 | |
  | 220 | 5.12 : 2.65 | pencil appears on only one side of p |
  | 345 | 4.89 : 4.02 | |
  | 350 | about 4.9 : 4.1 | chosen |

  Visible fraction of the X strings at 350: gold 0.96, blue 0.94.
- **The X on paper:**
  - Blue [A] at +27.4°, from the lower-left rim (72, 58) to the right-frame crop. Its visible
    runs are 183.0 mm and 39.7 mm, separated by the 14.4 mm lip gap.
  - Gold [B] at −38.2°, from the upper-left rim (72, 213) to the right-frame crop. Its visible
    runs are 157.6 mm and 96.2 mm, separated by the 14.3 mm lip gap.
  - They cross at p = (189.6, 119.7).
  - Band: 5 passes of the 0.2 nib at 0.15 mm, about 0.8 mm.
- **Science (recomputed in-piece; the asserts run on every render):**
  - Rulings lie on x²+y²−z²=1 to 2.7e-15 (all 2×96).
  - The X strings lie in the tangent plane n·P = 1 to 2.2e-16. That is the ψ = 90° member, A(α₀) ∪ B(α₀).
  - Each drawn pencil piece is on the quadric (< 1e-12 asserted) and on its plane
    z = tan ψ (n·P − 1) (< 1e-9 asserted).
  - ψ = 31.717° = ½·arctan 2: min z = −2.0000, so it grazes the rim.
  - Visibility is exact. The second ray root is t* = −2 P·D·v / v·D·v with D = diag(1,1,−1), and
    a point is hidden iff t* > 0 and |z(t*)| ≤ 2. Flips are bisected to 1e-12 in s.
- **LOD:**
  - Each string is thinned by `Occupancy` in halving priority (index 0, then mod 8, 4, 2, 1),
    with pause-and-resume.
  - The floor is 0.88 mm tested on 0.3 mm samples, which holds ≥ 0.78 mm between segments.
  - Cross-family near-parallel (|cos| > 0.93) yields the later stretch.
  - Green shadowing over 3 mm cuts the string.
- **Eye:** 119.5 × 50.0 mm, 4 712 mm², no ink.
- **Type clearance to construction ink (mm):**

  | block | question | key | honesty | statement | title | rebus |
  |---|---|---|---|---|---|---|
  | clearance | 38.1 | 25.7 | 22.5 | 54.8 | 49.5 | 32.6 |

  Block tops are at 350.1, 185.5 and 36.8.
- **Visible string length before LOD:** 36.5 m. After LOD, gold is 17.9 m and blue 16.6 m.

## Plot budget (A3, from the gcode; time = length at F600 + 2.5 s per stroke)

| order | layer | pen | strokes | draw | est. |
|---|---|---|---|---|---|
| 1 | GOLD | ochre pigment fineliner 0.2 | 207 | 17.91 m | 38.5 min |
| 2 | BLUE | ultramarine fineliner 0.2 | 192 | 16.60 m | 35.7 min |
| 3 | GREEN | deep green 0.5 | 18 | 1.51 m | 3.3 min |
| 4 | TEXT | black 0.3 | 690 | 3.29 m | 34.2 min |
| | total | 4 pens, 3 swaps | 1 107 | 39.3 m draw, 9.7 m travel, 11 265 commands | **~112 min** |

- The order runs light to dark, so green lands over the weave and black lands last.
- Each string is one straight G1, and the longest stroke is 192 mm, so every stroke can be a
  batch boundary.
- The pipeline's within-colour reorder leaves 2–4 sheet-crossing travels per layer:
  - gold: 399 mm, from the rebus slash back to the weave;
  - blue: 277 mm;
  - green: 406 mm, from the rebus circle.

  Each is pen-up and about 3 s. The cause is that the rebus sits 250 mm from the construction.
- Leo A5 (v24): gold 5.54 m / 162 strokes / 16 min, blue 5.08 m / 135 / 14 min, green 0.38 m /
  11 / 1 min, text 1.99 m / 690 / 32 min, **~63 min**. The pen-up frame trace comes first.

## Self-critique (seven dimensions, honest)

| dimension | score | why |
|---|---|---|
| Hierarchy | 7 | At 3 m you see the string mass, then the heavy X, then the green sheaf pinched on it. The rebus is a clear second read at 1 m. The X band is only about 0.8 mm, so at 3 m it is a line, not a bar |
| Grid & alignment | 7 | Everything flush-left on x = 15. Title and rebus share one band edge to edge. The crop is on the right and bottom frames. The key's vertical position follows the notch, not a grid step |
| Tension & asymmetry | 7 | The construction is off-centre and swallows two edges, against the paper L. The X is a real thrust and counter-thrust. The 8 itself is upright (roll 0) |
| Negative space | 8 | The eye (120 × 50 mm) and the L of paper are both shaped |
| Craft for pen | 7 | Straight G1 only, no floods. The same-colour spacing has a 0.78 mm residue. The text layer costs 34 min for 3.3 m |
| Concept legibility | 7 | ○ = ╱ + ╲ sits above a real X with a circle through its crossing. The pencil reads as two fans aimed at p rather than as nested loops, because members are tangent at p and must stop 8–31 mm short of it |
| Depth | 8 | True hidden-line hyperboloid. The front lower flank, the inside back wall through the opening and the see-through eye are all readable |

**Single worst thing:** the upper lobe (about 40 % of the sheet, y 200–345) is an evenly dense
weave. The only event in it is the two far green arcs over the eye. It is the Gabo "luminous web",
but it is the largest area on the sheet and it carries the least.

## Engine requests

- `render_candidate`'s postprocess reorder produces sheet-crossing pen-up travels between an
  isolated element (a rebus) and the main mass. A "keep authored order within a colour" flag
  would let a piece's boustrophedon order survive.
