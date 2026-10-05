# attention-weaving — encoding (VISUAL TRANSLATOR) · Status: encoding v1 = **Revision 1** of the aperture thesis · 2026-09-29

## Revision 1 — 2026-09-29

The aperture thesis ran r03–r06 on an unwritten encoding. The science critic never had a
dossier or an encoding to check against, so this file is derived from BRIEF.md,
DESCRIPTION.md, LEDGER.md, the r04–r06 critiques and the r06 SYNTH. **This is a revised
encoding, not a written-down copy of the old one. The designer-round cap restarts: r07 is
round 1 of Revision 1.** Everything above the wall keeps its order. Three mappings change.

| # | what changed | old (r04–r06, implicit) | new | forced by |
|---|---|---|---|---|
| R1 | **What V is below the wall** | 16 separate gold strands from a left reed, crossing the lane bundle wherever it lay, ending near the selvage | **one continuous gold weft of 16 picks.** Pick g = the value of the key in hill bin g. Each pick crosses all 22 lanes at ~90°. The weft turns around the two selvage lanes, and each of its two ends lands on a reed tick. Picks exist only where the lanes are ≥ 3.6 mm apart, so a float can never be shorter than 5 mm | J1, A7 (failed r04/r05/r06), A21, S11 |
| R2 | **What a lane's position in the slit means** | Q11's row cut into 22 quanta, but captioned as "22 queries" | **position is only the query's order.** The 22 lanes sit at one equal pitch (2.25 mm) and are seriated. Q11 is pinned at the centre line. No weight is claimed by position; the hill alone carries a | S8, S9, A19 |
| R3 | **The slit and the hill** | 73.7 mm slit; crown in bin 4; hill on a raised shelf with jamb steps | **52 mm slit.** Crown in bin 7, next to the centre line. The hill spans the full slit and is zero at both cut edges (no shelf, no jamb step). Each K lands at the point of maximum clearance inside its own bin | A19, A22, hierarchy (art dim 1) |

**Proof that the old lane rule could not be kept** (S8, option "each Z_i at its own row
centroid Σ_j A_ij·x_j"), measured on the seeded A below: the rows are near-uniform
(H = 3.76–3.94 bits of 4.00), so the 22 centroids fall within 4.1 bins of each other.
Their minimum separation is 0.018 bins under the best seriation found (random search:
0.037 bins). At 3.25 mm bins that is ≤ 0.12 mm, and holding a 0.9 mm pitch would need a
slit of ≥ 400 mm. **The centroid is true but cannot be drawn with a pen.** So position
carries order, which is the honest alternative the science critic allowed. R2 states it
on the sheet.

---

## 1. STYLE assignment

**ART DECO, declared flat** (unchanged from r06), plus the lineage **Anni Albers,
*Black-White-Gold I* (1950)**: interlacing, with over/under as information.

Why Deco's order fits: Deco's two signature ornaments are the **sunburst converging on
one point** and the **fan shell**, which is a radiating fan crossed by nested arcs.
The mechanism has exactly these two orders, one on each side of the constriction. Above
the wall, a storm of scores converges on one slit. Below it, the surviving threads fan
out and are crossed by nested arcs of gold (the weave). Deco also allows the
**symmetric crown** that R3 puts at the throat. Asymmetry lives in the drain, which
sweeps down-right, and in the flush-left type. Flat is honest: occlusion (over/under,
the opaque hill) is the only depth cue, and it carries data at every crossing.

## 2. The one-glance statement

**A storm of red and blue threads is combed through one narrow reed in a black wall.
Only the red come out, turned green, and a single gold thread weaves them into cloth.**

- At 3 m: a black wall with one bright notch, a hill standing in it, and one bold line
  falling straight onto the hill's summit. A storm above; a woven gold-and-green fan
  below-right; a bare field left.
- At 1 m: the blue threads stop on the hill. The gold is one thread, turning back at
  both edges of the fan.
- At 30 cm: the bold green lane is covered by gold at exactly the four middle picks. Those
  are the four bins where the hill stands above the 1/16 tick.

## 3. The abstract ORDER

**FLOW TO ONE ATTRACTOR (above) → a REED (the slit) → INTERLACING (below).**
Two orders are joined at one constriction. That is the brief's "everything passes
through the waist", made literal as a loom's reed.

One-line mappings, exact:
- **A key is a thread the reed stops. A query is a thread it passes.**
  - The 16 K end on the hill, one per equal bin.
  - The 22 Q cross the slit at one pitch and continue as the 22 Z warps.
- **The hill is Q11's row.** The area over bin g equals a_g exactly. The bins are equal,
  so the mean height over bin g is ∝ a_g. Σ = 1 appears as area, not as a label.
- **Gold over green ⇔ a_ij > 1/16.** Warp i (query i) crosses pick g (the value of the
  key in bin g). The 352 crossings of the cloth **are** the 22×16 attention matrix.
- **Storm over/under (unchanged):** Q over K where s_ij ≥ 0.

## 4. Channel mapping

### 4a. The numbers (closes S5) — seed 7, generation rule

These are the same draws as r03–r06, so r06's `LAST_STATS` reproduce:
- d = 16. Q_i, K_j ~ unit(N(0, I₁₆)) for i < 22, j < 16, drawn in that order. V_j = the
  first 16 components of unit(N(0, I₃₈)). All draws come from the one `SeededRNG(7)`
  stream.
- The principal query is P = 11. Five keys are tilted toward Q_P, then renormalised:
  K_j ← w·Q_P + √(1−w²)·K_j for (j, w) = (5, .90), (11, .70), (2, .54), (14, .40),
  (8, .30).
- s_ij = √d·Q_i·K_j.
- T is found by 64-step bisection on [0.05, 30] such that max softmax(s_P / T) = 0.190.
  This gives T = 2.29842.
- A_ij = softmax_j(s_ij / T). Every row sums to 1 within 1.1e-16.
- Q11's row: a_max 0.190 (key 5), H = 3.762 of 4.000 bits.

**The full matrix A (rows = queries, columns = keys in index order; bold = a > 1/16):**

| q \ key | k0 | k1 | k2 | k3 | k4 | k5 | k6 | k7 | k8 | k9 | k10 | k11 | k12 | k13 | k14 | k15 | Σ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q0 | 0.0395 | **0.0881** | 0.0593 | 0.0592 | 0.0486 | 0.0551 | **0.0666** | 0.0165 | 0.0623 | 0.0516 | **0.0739** | 0.0619 | **0.0895** | **0.0999** | 0.0389 | **0.0891** | 1.0000 |
| Q1 | 0.0336 | 0.0559 | 0.0503 | **0.0729** | 0.0617 | 0.0354 | 0.0306 | 0.0526 | **0.0727** | 0.0571 | **0.1114** | 0.0433 | 0.0527 | **0.0773** | **0.1176** | **0.0750** | 1.0000 |
| Q2 | 0.0566 | **0.1028** | 0.0566 | 0.0326 | 0.0362 | **0.0693** | **0.1109** | 0.0537 | 0.0446 | **0.1170** | 0.0500 | **0.0725** | 0.0329 | **0.0637** | **0.0732** | 0.0273 | 1.0000 |
| Q3 | 0.0548 | **0.0956** | 0.0618 | 0.0262 | 0.0496 | **0.0838** | **0.0729** | 0.0439 | 0.0530 | **0.1253** | 0.0368 | **0.0730** | 0.0432 | 0.0561 | **0.0789** | 0.0452 | 1.0000 |
| Q4 | 0.0394 | **0.1064** | 0.0398 | 0.0348 | 0.0448 | 0.0545 | **0.1016** | 0.0412 | **0.1305** | 0.0358 | **0.0880** | 0.0287 | 0.0360 | **0.0627** | **0.0968** | 0.0591 | 1.0000 |
| Q5 | **0.1241** | 0.0476 | 0.0372 | 0.0607 | 0.0511 | 0.0485 | 0.0461 | **0.1133** | 0.0375 | **0.1191** | 0.0489 | **0.0646** | 0.0442 | 0.0600 | 0.0541 | 0.0430 | 1.0000 |
| Q6 | 0.0407 | **0.0900** | 0.0408 | 0.0354 | 0.0453 | **0.0733** | 0.0535 | 0.0379 | **0.0769** | 0.0213 | **0.0647** | 0.0460 | **0.0714** | **0.1503** | 0.0391 | **0.1134** | 1.0000 |
| Q7 | 0.0261 | 0.0422 | 0.0599 | **0.1021** | **0.0635** | 0.0557 | 0.0478 | 0.0540 | 0.0451 | 0.0399 | **0.0895** | **0.0993** | **0.0658** | 0.0428 | **0.0976** | **0.0687** | 1.0000 |
| Q8 | 0.0359 | 0.0535 | 0.0277 | 0.0418 | **0.0781** | 0.0497 | **0.0694** | 0.0392 | **0.0990** | 0.0267 | **0.0697** | 0.0413 | **0.0807** | **0.1168** | 0.0380 | **0.1326** | 1.0000 |
| Q9 | 0.0501 | 0.0566 | 0.0458 | 0.0534 | 0.0329 | 0.0574 | 0.0401 | **0.0689** | 0.0596 | **0.1598** | **0.0629** | **0.0738** | 0.0523 | 0.0492 | **0.0990** | 0.0381 | 1.0000 |
| Q10 | **0.0759** | 0.0528 | **0.1295** | 0.0340 | 0.0584 | **0.0785** | 0.0616 | **0.1021** | 0.0495 | **0.0701** | 0.0249 | 0.0596 | **0.0652** | 0.0491 | 0.0499 | 0.0392 | 1.0000 |
| **Q11** | 0.0341 | 0.0557 | **0.0661** | 0.0440 | 0.0406 | **0.1900** | 0.0448 | 0.0451 | 0.0381 | 0.0365 | 0.0506 | **0.1393** | **0.0793** | 0.0461 | 0.0540 | 0.0358 | 1.0000 |
| Q12 | 0.0491 | **0.0636** | **0.1500** | **0.0653** | 0.0272 | **0.0833** | 0.0468 | 0.0452 | 0.0428 | 0.0555 | 0.0451 | **0.1090** | **0.0760** | 0.0307 | 0.0550 | 0.0553 | 1.0000 |
| Q13 | **0.0856** | **0.1594** | **0.0874** | 0.0418 | 0.0546 | **0.0862** | 0.0335 | 0.0297 | 0.0363 | 0.0289 | 0.0431 | **0.0720** | 0.0515 | 0.0547 | 0.0505 | **0.0847** | 1.0000 |
| Q14 | **0.0889** | **0.0724** | **0.0975** | **0.0775** | 0.0446 | 0.0485 | 0.0479 | **0.0936** | 0.0392 | 0.0444 | 0.0540 | **0.0626** | 0.0534 | **0.0749** | 0.0476 | 0.0531 | 1.0000 |
| Q15 | **0.1761** | 0.0531 | 0.0625 | **0.0675** | **0.0867** | 0.0292 | 0.0532 | **0.1161** | 0.0326 | **0.0671** | 0.0277 | 0.0379 | 0.0350 | 0.0560 | 0.0377 | 0.0617 | 1.0000 |
| Q16 | **0.0861** | 0.0421 | 0.0394 | 0.0427 | **0.1066** | **0.0787** | **0.1211** | 0.0552 | 0.0573 | 0.0343 | 0.0429 | 0.0512 | 0.0570 | **0.0645** | 0.0373 | **0.0836** | 1.0000 |
| Q17 | **0.0962** | 0.0613 | 0.0435 | 0.0327 | 0.0456 | 0.0257 | **0.0813** | **0.0938** | **0.0672** | **0.1110** | 0.0376 | 0.0266 | 0.0280 | **0.0662** | **0.0760** | **0.1073** | 1.0000 |
| Q18 | 0.0287 | **0.1199** | **0.0709** | 0.0386 | 0.0275 | **0.0655** | 0.0342 | 0.0385 | 0.0529 | **0.0829** | **0.0881** | **0.0780** | 0.0603 | **0.0795** | **0.1020** | 0.0324 | 1.0000 |
| Q19 | **0.0773** | 0.0399 | 0.0565 | **0.0951** | **0.1778** | 0.0397 | 0.0526 | 0.0383 | 0.0332 | **0.0761** | 0.0530 | 0.0564 | **0.0777** | 0.0518 | 0.0371 | 0.0376 | 1.0000 |
| Q20 | 0.0277 | 0.0577 | 0.0221 | 0.0488 | **0.0691** | **0.1090** | 0.0470 | 0.0384 | **0.0728** | 0.0461 | **0.1318** | **0.0647** | 0.0516 | 0.0340 | **0.1372** | 0.0419 | 1.0000 |
| Q21 | 0.0600 | **0.1062** | 0.0615 | 0.0479 | 0.0290 | **0.0645** | 0.0277 | **0.1024** | **0.0635** | 0.0554 | **0.0714** | **0.0652** | 0.0453 | **0.0713** | **0.0829** | 0.0457 | 1.0000 |

**Bin order (the hill, left → right; this is also pick order, slit outward).** Keys are
sorted by Q11's a (descending) and dealt alternately about the crown into bins
7, 8, 6, 9, 5, 10, 4, 11, 3, 12, 2, 13, 1, 14, 0, 15:

| bin | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| key | 15 | 8 | 3 | 7 | 10 | 1 | 12 | **5** | 11 | 2 | 14 | 13 | 6 | 4 | 9 | 0 |
| a (Q11) | .0358 | .0381 | .0440 | .0451 | .0506 | .0557 | .0793 | **.1900** | .1393 | .0661 | .0540 | .0461 | .0448 | .0406 | .0365 | .0341 |

The bin means rise strictly to the crown and fall strictly after it, so a unimodal
exact-area curve exists. **Q11 is above 1/16 in bins 6–9 exactly: four contiguous
bins.** Those are keys 12, 5, 11 and 2, which are Q11's only above-uniform keys.

**The weave, B = [a_ij > 1/16]** (rows = queries, columns = bins 0…15 = picks 1…16;
`#` = gold over). There are 136 of 352 gold-over crossings (38.6 %):
```
Q0  #...###....##...   Q11 ......####......
Q1  ###.#.....##....   Q12 ..#..#####......
Q2  .....#.##.###.#.   Q13 #....#.###.....#
Q3  .....#.##.#.#.#.   Q14 ..##.#..##.#...#
Q4  .#..##....###...   Q15 ..##.........###
Q5  ...#....#.....##   Q16 #......#...###.#
Q6  ##..####...#....   Q17 ##.#......###.##
Q7  #.#.#.#.#.#..#..   Q18 ....##.#####..#.
Q8  ##..#.#....###..   Q19 ..#...#......###
Q9  ...##...#.#...#.   Q20 .#..#..##.#..#..
Q10 ...#..##.#....##   Q21 .#.###.##.##....
```
- 17 entries lie within 0.002 of 1/16. The nearest is Q5 × k3 at 0.06072. They are
  decided exactly by the rule; **there is no dead band and no override** (S11 is closed
  by construction, see 4c).
- The per-pick gold-over count runs 6 to 12. Every pick shows gold, and none is solid.

### 4b. Channel table

| quantity | channel | exact rule / range |
|---|---|---|
| Softmax row of Q11, a_g (16 values) | **area of the black hill** over equal bin g | Area over bin g = a_g (error ≤ 1e-12). The curve is C¹ and least-curvature. Height is **0 at both jambs**, it rises strictly to one summit and falls strictly after. Peak ≈ 0.074·H ≈ 20.7 mm. 5 passes over 1.2 mm, opaque |
| Uniform level 1/16 | **one 3 mm black tick** on the outer face of the right jamb, at the hill's height for a = 1/16 (mean-height scale) | This is the only chart mark in the throat. It is the threshold the cloth uses (closes S6 minimally; S10) |
| Key identity j | **which bin** K_j ends in | K_j ends on the hill **inside bin(j)**, at the point of maximum clearance from every lane: ≥ 1.12 mm from lanes, ≥ 0.45 mm inside the bin edges. 0.75 mm above the top pass. Table in 4d |
| Query identity i | **one continuous thread**: crimson above the hill, green below the wall | The same ψ-streamline throughout. \|x_Q − x_Z\| ≤ 0.5 mm at the wall (replaces S9) |
| Query order along the slit | lane slot k = 0…21, **equal pitch 2.25 mm** | x_k = ax + (k − 11)·2.25, so the lanes run from ax − 24.75 to ax + 22.5. The order is **free** (attention is permutation-invariant), so it is seriated on B (greedy + 2-opt on Hamming distance, bin-ordered columns), with **Q11 pinned at k = 11, x = ax** (ψ = π/2, the one straight streamline) |
| Score sign s_ij | storm over/under | Q over K ⇔ s_ij ≥ 0 (r06 rule, unchanged). Gap radius 1.15 mm |
| Value j (the key in bin g) | **pick g of the gold weft** (g = 1 nearest the slit … 16 nearest the frame) | Pick order = bin order, so the reader counts picks outward the way they count bins left to right. **No index text is needed** (S10) |
| a_ij vs 1/16 | **over/under at warp i × pick g** | Gold over ⇔ a_ij > 1/16, at all 352 crossings. The under-strand gets a gap of radius r = 1.1 mm |
| "Principal query" | **the one bold strand**: 2 passes at 0.35 mm offset, same direction, gaps cut once for the pair | Runs top reed → summit → slit → through the cloth → right reed. It is bold in both colours (one thread), and it is the **only** multi-pass coloured stroke |
| Consumption (16 K stop, 22 Q pass) | **counts at the reed** | 38 threads above (22 Q + 16 K). 38 thread families in the cloth (22 warps + 16 picks). See §8 |

Nothing drawn encodes nothing. The turns of the weft carry "these 16 picks are one value
matrix V, one row per pick". They are the physical rule of weft, not ornament. The lead-in
and lead-out are the weft's two ends.

### 4c. Why the over/under rule and the 5 mm floor are now compatible (S11)

A gold piece is either a float (a run of consecutive gold-over crossings) or a turn.
- **Merge rule (gold only):** the gold between two consecutive gold-under crossings on a
  pick is removed. The weft is hidden under that run of warps.
- **Shortest float:** a single gold-over at lane i spans from lane i−1's gap to lane i+1's
  gap: 2·s − 2·r, where s is the lane pitch measured along the pick. With the weave
  floor **s ≥ 3.6 mm** and r = 1.1 mm, that is ≥ 5.0 mm.
- A float at a selvage runs on into a turn, so it is always longer.

The 5 mm floor is therefore met **by where the picks are allowed to be**, not by
overriding data:
- There are 0 forced crossings. The caption is true at 352/352.
- Green is never merged. Each gold-over cuts one 2.2 mm gap in its warp. Pick spacing
  **≥ 4.2 mm along every lane** keeps each green piece ≥ 2.0 mm.
- The weave floor is exactly why the picks stay out of the tight bundle under the slit.
  There, the warp runs bare, as it does in a loom before the first pick.

### 4d. Fit at the slit (A19 × pitch) — measured on the slot plan

| quantity | value |
|---|---|
| slit | **52.0 mm**, c = 26.0, ax = x0 + 0.425·W = 103.5 mm, wall y = 183.6 |
| bins | 16 × 3.25 mm |
| lanes | 22 at 2.25 mm, x = ax − 24.75 … ax + 22.5. Jamb clearance 1.25 mm (left) and 3.50 mm (right) |
| K landing offset from bin centre (bins 0…15) | +.75, −.25, +1.00, 0, −1.00, +.25, −.75, +.50, −.50, +.75, −.25, +1.00, 0, −1.00, +.25, −.12 mm. **All inside their own bin** |
| min K–lane | 1.12 mm (≥ 0.92 floor). K–K ≥ 2.25 mm |
| summit | K5 at ax − 1.12 (crown bin 7) and K11 at ax + 1.12 (bin 8). **Q11 at ax lands between its two strongest keys**, on the summit |
| below the wall | lane pitch at the slit is 2.25 mm, and it may only grow downstream. The fold must never squeeze it below 0.95 mm, which was r06's worst κ |

It fits in 52 mm with a margin. r06 needed 73.7 mm only because four lanes piled into
one bin (Q11's apportionment). R2 removes the pile. The slit is set by the wall, not
by the pitch.

## 5. Composition sketch

Paper: 24 × 30 cm portrait (240 × 300), cream. Drawable area x 10–230, y 10–290
(10 mm margins, as r06). Coordinates are in mm, y up.

- **Wall (structural axis):** y = 183.6, 5-pass black, frame to frame, broken only by the
  slit x 77.5–129.5. It divides storm (top 106 mm) from aftermath (bottom 174 mm).
- **Throat (focal point):** hill x 77.5–129.5, rising to ≈ 204 at x ≈ 102. The bold
  strand is the vertical at x = 103.5, from the top reed (y 290) to the summit. The 1/16
  tick sits at x 129.5–132.5. `SOFTMAX` (text layer) sits on the wall's right arm top:
  x ≥ 136, baseline 185.6, with no notch around it.
- **Storm (dominant mass):** x 10–230, y 186–290. 22 Q + 16 K, geometry as r06. Q rays
  come from their new slit slots. Q/K mouths on the top and right reeds are ≥ 3 mm apart.
  `Q` at the left frame and `K` at the right frame, as r06. **No other text above the
  wall.**
- **Drain, warp only (x 78–165, y 150–183):**
  - The first ~20 mm below the slit are the φ < 0 streamlines: each lane leaves the
    wall perpendicular to it.
  - Then the drain map carries them down-right as a band.
  - The lane order at the slit (left → right) becomes lower → upper selvage.
  - 0 lane–lane crossings.
- **The cloth (second mass, ≈ 7,000 mm²):**
  - A wedge bounded by lane 0 (lower selvage) and lane 21 (upper selvage).
  - Pick 1 runs from ≈ (135, 105) on lane 0 to ≈ (160, 176) on lane 21.
  - Pick 16 runs from ≈ (222, 58) to ≈ (224, 172).
  - Picks are orthogonal trajectories of the lane field. They open like a fan-shell,
    from tilted near the throat to vertical at the frame.
  - The upper selvage stays ≥ 8 mm below the wall's underside wherever turns wrap it.
  - Lanes exit the right frame at y 56–172 (pitch ≈ 5.5 mm). Every exit is ticked, with
    ticks ≥ 3 mm apart.
  - The bold lane's exit tick carries `11` (text layer).
- **The weft's two ends:**
  - Lead-in: from a gold reed tick on the **left frame at y ≈ 97**, running nearly
    level (rising ≤ 12 mm) to join pick 1 outside lane 0. It is the floor of the void.
    `V` (text layer) sits under its first 5 mm, x 10–14, baseline 89.
  - Lead-out: from pick 16's lower end down to a gold reed tick on the **right frame at
    y ≈ 50**, ≥ 3 mm below lane 0's exit.
- **Type, flush-left x = 10:**
  - `SUMS` / `TO ONE`: cap height **13 mm** (down from 17, so the throat out-shouts it).
    TO ONE baseline 44, SUMS baseline 63.
  - `Z = AV` on the TO ONE baseline, x 168–212, in open paper under lane 0 (lane 0 at
    x 168–212 is ≥ 8 mm above its caps).
  - 4 footer lines, y 12–32, even leading. Every number must be the measured value:
    1. `ATTENTION AS WEAVING · ONE REED, ONE CLOTH`
    2. `22 Q · 16 K → 22 Z   Σa = 1   a MAX 0.190   H 3.76 / 4.00 BITS`
    3. `SLIT 52 MM · 16 EQUAL BINS · LANES EQUAL PITCH 2.25 MM, ORDER ONLY`
    4. `BOLD = QUERY 11, ITS ROW IS THE HILL · GOLD OVER GREEN WHERE a > 1/16 (136 / 352) · TICK = 1/16`
- **Dominant mass ratio:** storm ≈ 23,300 mm² : cloth ≈ 7,000 mm² ≈ **3.3 : 1**. The type
  block (≈ 150 × 32) is the third mass. Hierarchy by value: the throat (the only heavy
  black mid-sheet, carrying the bold strand's landing) reads first. J1 asks for the
  bottom to have equal **grammar**, not equal size.
- **Quiet zone (shaped):** an L of bare paper, x 10–77, y 100–183. Its edges are the
  wall above, the warp bundle and lower selvage on the right, and the gold lead-in
  below. It contains the A21 crop x 10–90, y 100–150. A second quiet band, x 165–228,
  y 10–40, holds only `Z = AV` and the lead-out tick.

## 6. Pen budget

**5 inks, 6 layers.** This exceeds the ≤ 4 bar, and it is stated: under the PLOTTABLE
rule each pen carries one meaning, has one clean layer and is never re-entered. The
BRIEF specifies Q/K/V/Z + black (A16, argued). Layer order is light → dark, so the
darkest ink lands last and black reed ticks and the wall cover strand ends.

| layer | pen | meaning | carries |
|---|---|---|---|
| 1 | goldenrod, **broad 0.7–0.8 mm** (gel / POSCA PC-1MR) | **the values V** (one weft) | lead-in, 16 picks (floats only), 15 turns, lead-out, 2 gold reed ticks |
| 2 | dodgerblue 0.3 | **keys K** (consumed) | 16 K spirals, top/right reed → hill |
| 3 | crimson 0.3 | **queries Q** | 22 Q streamlines; Q11 double pass |
| 4 | darkgreen 0.3 | **outputs Z = AV** (the warp) | 22 lanes wall → right frame; bold Z11 double pass |
| 5 | black 0.5 | **structure** | wall (5 passes), hill (5 passes), 1/16 tick, all reed ticks, giant `SUMS / TO ONE` |
| 6 | black 0.3 | **text layer** (house law) | `Q`, `K`, `SOFTMAX`, `V`, `11`, `Z = AV`, footer. Halo 1.3 mm cut into every strand it sits near |

All labels move to the black text layer. Colour identification comes from adjacency.
This is a change from r06's coloured labels, required by the text-layer law.

## 7. Expressive levers — one decision each

- **Proportion:** storm : cloth ≈ 3.3 : 1. Giant type drops to 13 mm caps. The slit
  (52 mm) is 0.24 W, the narrowest, loudest thing.
- **Fill vs void:** three zones run packed (storm) → silent (the left L) → packed (the
  cloth). The bare warp under the slit is a half-tone between them.
- **Density gradient:**
  - The cloth's cells grow from ~3.6 × 4.2 mm at pick 1 to ~5.5 × 6 mm at pick 16. The
    fan-shell opens toward the frame.
  - The storm keeps its native density: Q rays crowd the centre and flare at the flanks.
  - Both ramps are consequences of the geometry, not added.
- **Colour play:**
  - Crimson becomes green through the slit (same thread, new role).
  - Gold appears only below the wall.
  - The bold strand is the one scarce loud line, in both its colours.
  - The broad gold nib makes the floats read as woven gold at 3 m (Albers' gold)
    against hairline warps.
- **Texture direction:** the weft is **orthogonal** to the warp (≥ 75°, the weave's own
  rule). This contrasts with the storm's oblique K×Q crossings (26–90°). Oblique above
  (turbulence), orthogonal below (cloth).

## 8. The twist

**What the viewer holds:**
- "Sums to one" (a probability is a partition).
- A loom's reed: a comb every warp thread must pass through.
- The brief's promise that "strand count in = strand count out".

**What the mechanism breaks:**
- The reed does not just space the threads; it **eats** some. All 16 blue threads stop
  on the hill that is their softmax weight, and only the red pass.
- Yet the count still balances. 38 threads enter the reed (22 Q + 16 K), and 38 thread
  families make the cloth (22 warps + 16 picks). The keys are spent at the reed, and the
  values they unlock are woven back in **after** it.
- So the brief's rule survives in a truer form: count in = count out, with the second 16
  changing from K to V.
- The brief's "braid carries more strands than Q or K alone" holds: 38 > 22 (A15's open
  objection).
- **Flag for Juan:** this reading replaces S1's retirement of the rule.

The punchline is at 30 cm. The bold thread that fell onto the summit is covered by gold
at exactly the four picks whose bins stand above the 1/16 tick. The hill is that
thread's row; the cloth is everyone's.

## 9. Forbidden list

1. **No gold end in open paper.** The weft has exactly two ends, both on reed ticks. A
   strand ending 0.5–1.5 mm short of a lane does not count as "landing" (a SYNTH "do not").
2. **No gold inside the tight bundle.** No pick where adjacent lanes along it are
   < 3.6 mm apart. No "one long gap under the bundle" trick (it is moot now).
3. **No overridden crossing.** The rule a > 1/16 decides all 352 crossings, with no dead
   band, no "forced V-over", and no disclosure-only exceptions.
4. **No shelf and no jamb step.** The hill's height is 0 at both cut edges, with no
   horizontal black run between the wall and the profile. No bin ticks and no knot discs
   on the curve.
5. **No chart furniture in the throat.** No cumulative curve, `1.000`, dotted ellipses or
   equipotentials. The 1/16 tick sits outside the slit on the jamb's outer face.
6. **No text above the wall** except `Q`, `K` and `SOFTMAX` (on the wall arm). No
   "Q11 · ITS ROW …" caption.
7. **No second doubled strand.** Only the principal thread is bold. K and V are single
   pass; gold weight comes from its nib, not from passes.
8. **No lane position implying weight.** Equal pitch at the slit, stated in the footer.
   No clumps.
9. **No widening the slit to buy pitch.** The slit is 52 mm (a SYNTH "do not").
10. **No arrows, no leader lines, no compass circles, no registration dots.** The
    reference's drafting scaffold stays retired.
11. **No re-seeding or thinning of the storm.** Q rays move only because their slit slots
    moved (R2). K keeps r06's sweep/reed logic.
12. **No lane–lane, pick–pick or K–K crossing.** Lanes exit the right frame only.

## 10. Fabrication

- **Spacing floors:**
  - Parallel strands: ≥ 0.9 mm (house law ≥ 0.8). Measured at the slit: lanes 2.25 mm,
    K–lane 1.12 mm.
  - Weave cells: ≥ 3.6 mm lane pitch along picks, ≥ 4.2 mm pick spacing along lanes.
  - Gold to anything it does not cross: ≥ 1.5 mm (broad nib).
  - No hatch on this plate. If one is added, the floor is 2.4 × 0.3 = 0.72 mm.
- **Gaps:** storm r = 1.15 mm (r06). Cloth r = 1.1 mm.
  - Gold over green: green gap half-width = 0.15 + 0.4 + 0.55 paper.
  - Green over gold: gold gap likewise.
  - Strands stop 1.25 mm above the hill's top pass.
- **Pieces:** gold ≥ 5 mm; green ≥ 2 mm; storm ≥ 2.3 mm; stubs < 2 mm dropped at halos only.
- **Flood risk:**
  - The summit has K5 / Q11×2 / K11 within 2.3 mm, above a 5-pass black curve. The
    strands stop above the hill band, so there is no ink-on-ink.
  - Broad gold floats never touch green (gaps).
  - The wall's 5 passes are at 0.25 mm pitch (a solid bar, intended).
- **Batching / order within each layer:**
  - Gold: follow the weft path from the lead-in to the lead-out (boustrophedon), float
    by float.
  - Green and crimson: lanes serpentine in slot order.
  - Blue: by reed position.
  - Black: wall, hill, tick, reeds clockwise, then type.
  - Text: top → bottom.
  - Never a sheet-crossing travel between consecutive strokes. Target travel < draw
    (A14; r06 was 1.04).
- **Estimated draw / time** at F600 (10 mm/s) and ≈ 2.5 s per lift cycle (lift + dwell +
  drop + dwell, per Leo's slow-feed settings):

| layer | draw | pieces | minutes |
|---|---|---|---|
| gold | ≈ 1.1 m | ≈ 70 | ≈ 5 |
| blue | ≈ 2.1 m | ≈ 70 | ≈ 6.5 |
| crimson | ≈ 2.4 m | ≈ 80 | ≈ 7.5 |
| green | ≈ 4.3 m | ≈ 160 | ≈ 14 |
| black structure | ≈ 3.6 m | ≈ 140 | ≈ 12 |
| black text | ≈ 0.9 m | ≈ 120 | ≈ 6.5 |
| **total** | **≈ 14.4 m** | | **≈ 52 min** |

  Add the frame trace and 5 swaps. The designer reports the measured numbers per layer.

## 11. Acceptance checks (art critic marks each PASS/FAIL from the png; mm = preview axes)

1. **Weft closed, no crumbs.**
   - The gold is one thread: follow it from the left-frame tick (y ≈ 97) through 16 picks
     and 15 turns to the right-frame tick (y ≈ 50).
   - **0 gold ends in open paper.** Every gold end is a reed tick or a merge gap flanked
     by green on both sides.
   - **0 gold pieces < 5 mm.**
2. **The cloth is the matrix, and the rule is checkable.**
   - Every pick crosses all 22 lanes once, at ≥ 75°.
   - The bold green lane is under gold at **exactly 4 picks, the 7th–10th counted from
     the slit**, and over gold at the other 12.
   - The hill stands above the 1/16 tick over exactly **4 bins, the 7th–10th counted from
     the left** (count bins by the 16 blue landings).
   - No gold piece lies where adjacent lanes are < 3.6 mm apart (the bare warp under the
     slit shows no gold).
3. **Throat restored (A19).**
   - Slit ≤ 52 mm.
   - The black profile leaves the wall at **both cut edges from zero height**, with no
     vertical step and no horizontal black run between wall and profile. It rises to one
     summit.
   - The bold vertical meets that summit (Q11 at the centre line, the two strongest keys
     on either side).
4. **Every thread closes, and Q_i = Z_i.**
   - 16 blue end on the hill, each inside a different bin.
   - 22 crimson meet the hill, and 22 green leave the wall at the same x (≤ 0.5 mm).
   - 22/22 green exits are ticked on the right frame, ≥ 3 mm apart, and `11` marks the
     bold one.
   - Top/right reed mouths are all ≥ 3 mm apart, with no tick shared by two strands (A22).
5. **Void and text discipline (A21, A20, A11).**
   - Crop x 10–90, y 100–150: **0 marks of any colour.**
   - Above the wall there is no text except `Q`, `K` and `SOFTMAX`, and `SOFTMAX` is not
     in a notch.
   - `Z = AV` is on the TO ONE baseline with ≥ 3 mm of bare paper around it.
   - The bold strand reads as ONE line (the two passes register), never two.
