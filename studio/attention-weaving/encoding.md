# attention-weaving — encoding (VISUAL TRANSLATOR) · Status: encoding v1.1 = **Revision 1.1** of the aperture thesis · 2026-09-29

**Revision 1.1 amends Revision 1. It does not start a new order.** The round count carries on:
r07 was round 1 of Revision 1, and **r09 is round 2 of 5.** (r08 was a wildcard on its own mapping and
does not count.) Revision 1 is kept verbatim in `encoding.rev1.md`.

## Revision 1.1 — 2026-09-29

The storm, the reed, R1 (one weft), R2 (order-only lanes), the 52 mm slit, the 16 equal bins and
every mandate r07 closed are **unchanged**. Only the three places where Revision 1 contradicted
the data or the sheet are rewritten.

| # | what changed | Revision 1 said | Revision 1.1 says | forced by |
|---|---|---|---|---|
| A1 | **The hill's floor** | the hill is 0 at both cut edges, with no step (§4b, §9.4, §11.3) | **Option (a): area stays ∝ a, so Σ area = 1 exactly.** The hill's ends float at the data's own floor: 3.49 mm left, 3.24 mm right. Each jamb becomes a **post** (a reed cheek) that rises to the **1/16 level**. The hill is strung between the posts and meets each post's inner face below the post's top. The footer names the floor: `a MIN 0.034 — NO KEY GETS ZERO`. §9.4 and §11.3 are deleted and rewritten | S12, A19 residual, J2. The r07 designer's proof, confirmed by the science critic, is below |
| A2 | **The 1/16 test** | "the hill stands above the tick over exactly 4 bins, the 7th–10th counted from the left" | **The test counts KEYS, not bin edges.** The bin edges are never drawn. The K in bins 6 and 9 land on the crown side of their bin, so exactly four blue landings stand where the hill is above the 1/16 level. The margins are large enough that the reading cannot flip (§4d, §11.6) | S12 (art read bin 9 as below the tick pointwise; science read its mean as above) |
| A3 | **The cloth: size, weave rule, turns** | lanes as ruled offsets at 3.667 mm pitch; exits y 56–172; gold merged under runs of under-lanes (61 % of the weft hidden); U-turns of mixed height | **A polar fan-shell.** Lanes are exact rays of one centre in the cloth; picks are concentric arcs. Pitch runs 4.50 → 5.55 mm and exits span y 53.5–172.9. **No merge:** gold breaks only where it passes under a lane, with a 1.8 mm gap. The gold floor is restated for stitches. The turns are semicircles of one radius, 2.4 mm, on the selvage rays | J1, A24, A23, and §5's lane 0 entering the A21 void |
| A4 | **Sheet truth** | footer line 2 `22 Q · 16 K → 22 Z`; §4a names Q5×k3 as the entry nearest 1/16; R2 proof spread 4.1 bins, min sep 0.018 | footer line 2 carries the §8 balance `22 Q · 16 K → 22 Z WARPS × 16 V PICKS`. **The entry nearest 1/16 is Q15×k2 = 0.062462** (\|Δ\| 3.8e-5). The R2 centroid spread is **1.88 bins** and the minimum separation is **0.006 bins**, in bin order | S13, S14 |

**Why the floor cannot be zero (A1).** The hill has equal 3.25 mm bins. Its area over bin g is
a_g, so the mean height over bin 0 is m₀ = 3.53 mm and over bin 1 it is m₁ = 3.76 mm.
- A curve that starts at 0 and never falls must stay ≤ m₁ on bin 0 and still average m₀ there.
- That leaves at most (1 − m₀/m₁) ≈ 6 % of the bin, about 0.2 mm, for the whole rise.
- So a ≈ 3.5 mm vertical at each jamb is **forced**. The only ways out are ringing (a false hump), unequal bins (breaks S2) or inexact area (breaks J2's "exactly").

Juan's word "sums to one" outranks the art clause. Option (b), area ∝ (a − a_min), was rejected:
- The hill would then sum to 0.454, not 1, and the giant `SUMS TO ONE` would caption a curve that does not.
- It is a truncated axis. It inflates the peak-to-median ratio of a near-uniform row (H 3.76 of 4.00 bits) and drops bin 15 to zero, which is the exact lie softmax forbids.

So the floor stays, is named in the footer, and is given a drawn form: the posts.

**Why the posts, not a fillet (A1).**
- r06's and r07's "table" read came from one shape: a near-flat top whose two ends drop straight to the baseline. It was an L-step on each side.
- A fillet only rounds that corner, and the fillet would also have to live inside bin 0's 0.2 mm, so it is still a table.
- With posts, **the vertical at each jamb belongs to the wall, and it continues past the hill's end**, up to the 1/16 level. The hill tails then read as a level strung between two cheeks, a fill in a vessel. They no longer read as a plinth standing on the wall.
- The post tops carry data: the line joining them is the uniform level 1/16. At a glance, the hill clears it only at the crown.
- The right post's top continues outward as the 3 mm 1/16 tick. The tick is kept, and now it is also structure.

**Why no-merge, and why the 5 mm floor is restated (A3).**
- r07 merged the gold under every run of under-lanes. With 216 of 352 crossings under, 61 % of the weft was hidden (pick 1 ran bare for 33 mm). The critic saw "gold staples".
- Breaking gold only at each under-lane leaves pieces of (pitch along the pick − gap).
- For the old 5 mm floor that needs a pitch ≥ 5 + 2·0.9 = 6.8 mm (the brief's 7.2 mm with r = 1.1), so 22 lanes need ≥ 143 mm across a pick.
- **The sheet cannot give that.** Lane 21 and its turns must stay ≥ 8 mm under the wall (lane 21 ≤ 172.9, apexes ≤ 174.3), and lane 0 must stay ≥ 8 mm over the `Z = AV` caps (y ≥ 53.5). That leaves 119 mm, so the pitch is at most 5.6 mm.
- The floor is therefore restated. **A7's 5 mm floor was written against crumbs in open paper**: gold scraps whose ends nothing explains. A **stitch** is a gold piece whose two ends are both under-gaps with a green line running through each. Its ends are explained by the warp it dives under. It is the woven cell itself, not a crumb.
- **Stitch floor = 2.5 mm**, ≥ 3 × the 0.8 mm gold nib, so it reads as a dash and never as a dot. The built minimum is 2.70 mm. Any other gold end (open paper) stays forbidden. The 5 mm floor survives for pieces with an open end, and by construction there are none.

---

## 1. STYLE assignment

**ART DECO, declared flat** (unchanged), plus the lineage **Anni Albers, *Black-White-Gold I*
(1950)**: interlacing, with over/under as information.

Why Deco's order fits: Deco's two signature ornaments are the **sunburst converging on one
point** and the **fan shell**, a radiating fan crossed by nested arcs. The mechanism has exactly
these two orders, one on each side of the constriction.
- Above the wall, a storm of scores converges on one slit.
- Below it, the surviving threads fan out as **rays**, and they are crossed by **16 nested gold arcs** (the weave). Revision 1.1 makes this literal: the lanes are exact rays of one centre, and the picks are concentric arcs.

Deco also allows the **symmetric crown** at the throat, now framed by two cheeks. Asymmetry lives
in the drain, which sweeps down-right, and in the flush-left type. Flat is honest: occlusion
(over/under, the opaque hill) is the only depth cue, and it carries data at every crossing.

## 2. The one-glance statement

**A storm of red and blue threads is combed through one narrow reed in a black wall. Only the
red come out, turned green, and a single gold thread weaves them into cloth.**

- **At 3 m:** a black wall with one notch between two short posts, a hill strung between them whose crown alone rises above the posts, and one bold line falling straight onto that crown. A storm above; a green fan of rays crossed by 16 gold arcs below-right; a bare field left.
- **At 1 m:** the blue threads stop on the hill. The gold is one thread: every arc is a stitched line, and it turns back around both edges of the fan in even loops.
- **At 30 cm:** the bold green ray is under gold at exactly the four middle arcs. Those are the four blue landings that stand where the hill rises above the post tops.

## 3. The abstract ORDER

**FLOW TO ONE ATTRACTOR (above) → a REED (the slit) → INTERLACING (below).** Two orders are
joined at one constriction. That is the brief's "everything passes through the waist", made
literal as a loom's reed.

One-line mappings, exact:
- **A key is a thread the reed stops. A query is a thread it passes.**
  - The 16 K end on the hill, one per equal bin.
  - The 22 Q cross the slit at one pitch and continue as the 22 Z warps.
- **The hill is Q11's row.** The area over bin g equals a_g exactly, and Σ area = 1.
  - The hill's lowest point is the row's own floor, a_min = 0.034: **no key gets zero.**
  - The posts' tops are the uniform level, 1/16.
- **Gold over green ⇔ a_ij > 1/16.** Warp i (query i) crosses pick g (the value of the key in bin g). The 352 crossings of the cloth **are** the 22×16 attention matrix, and every one is visible on both threads.
- **Storm over/under (unchanged):** Q over K where s_ij ≥ 0.

## 4. Channel mapping

### 4a. The numbers (closes S5) — seed 7, generation rule

These are the same draws as r03–r07, so r07's `LAST_STATS` reproduce:
- **Draws.** d = 16. Q_i, K_j ~ unit(N(0, I₁₆)) for i < 22, j < 16, drawn in that order. V_j = the first 16 components of unit(N(0, I₃₈)). All draws come from the one `SeededRNG(7)` stream. The critic confirmed these are the stdlib `rng.gauss` draws; the numpy path gives T = 2.3316 and does not match.
- **Tilt.** The principal query is P = 11. Five keys are tilted toward Q_P, then renormalised: K_j ← w·Q_P + √(1−w²)·K_j for (j, w) = (5, .90), (11, .70), (2, .54), (14, .40), (8, .30).
- **Scores.** s_ij = √d·Q_i·K_j.
- **Temperature.** T is found by 64-step bisection on [0.05, 30] such that max softmax(s_P / T) = 0.190. This gives T = 2.298425.
- **Weights.** A_ij = softmax_j(s_ij / T). Every row sums to 1 within 2.2e-16.
- **Q11's row:** a_max 0.190 (key 5), a_min 0.0341 (key 0), H = 3.762 of 4.000 bits.

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

(Q15×k2 prints as 0.0625 at 4 dp. Its exact value is 0.062462 < 1/16, so it is **not** bold and is
drawn under.)

**Bin order (the hill, left → right; this is also pick order, slit outward).** Keys are sorted by
Q11's a (descending) and dealt alternately about the crown into bins
7, 8, 6, 9, 5, 10, 4, 11, 3, 12, 2, 13, 1, 14, 0, 15:

| bin | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| key | 15 | 8 | 3 | 7 | 10 | 1 | 12 | **5** | 11 | 2 | 14 | 13 | 6 | 4 | 9 | 0 |
| a (Q11) | .0358 | .0381 | .0440 | .0451 | .0506 | .0557 | .0793 | **.1900** | .1393 | .0661 | .0540 | .0461 | .0448 | .0406 | .0365 | .0341 |
| bin mean, mm (98.7 mm per unit a) | 3.53 | 3.76 | 4.34 | 4.45 | 4.99 | 5.50 | 7.82 | 18.75 | 13.75 | 6.52 | 5.33 | 4.55 | 4.42 | 4.01 | 3.60 | 3.37 |

- The bin means rise strictly to the crown and fall strictly after it, so a unimodal exact-area curve exists.
- **Q11 is above 1/16 in bins 6–9 exactly: four contiguous bins.** Those are keys 12, 5, 11 and 2, which are Q11's only above-uniform keys.
- Bin 9 clears 1/16 by only 0.0036 (0.35 mm of mean height), which is why §4d places its landing.

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
- 17 entries lie within 0.002 of 1/16. **The nearest is Q15 × k2 = 0.062462** (\|Δ\| 3.8e-5, bin 9, drawn under). *(Revision 1 wrongly named Q5 × k3 = 0.06072; S14.)*
- All 17 are decided exactly by the rule. **There is no dead band and no override.**
- The per-pick gold-over count, picks 1…16, is [8, 7, 6, 7, 10, 10, 8, 11, 12, 6, 10, 11, 7, 6, 9, 8]. Every pick shows gold floats, and none is solid.
- The per-pick **under** count is 22 − that: 10–16 gaps per pick, 216 in total.

**R2 (lane position = order only), numbers corrected (S14).** Each Z_i at its own row centroid
Σ_j A_ij·x_j was rejected because it cannot be drawn:
- Recomputed in bin order by the r07 science critic, the 22 centroids fall within **1.88 bins** of each other.
- Their minimum separation is **0.006 bins**. At 3.25 mm bins that is 0.02 mm.
- Holding the 0.9 mm pen floor would need bins ≥ 150 mm, a slit ≥ 2.4 m. *(Revision 1 said 4.1 bins, 0.018 bins and ≥ 400 mm; the conclusion holds a fortiori.)*

So position carries order, and the footer says `ORDER ONLY`.

### 4b. Channel table

| quantity | channel | exact rule / range |
|---|---|---|
| Softmax row of Q11, a_g (16 values) | **area of the black hill** over equal bin g | Area over bin g = a_g / Σa (error ≤ 1e-9). The curve is C¹ and least-curvature, with **free ends** (no pin rows). The ramp condition is **β = 0.25**: every tail step rises toward the crown by ≥ β × the slope of the bin-mean staircase. This was checked feasible: area error 1.8e-12. Peak 20.72 mm at x ≈ 102.5. **End heights 3.49 mm (left) and 3.24 mm (right) above the wall line: the data's floor, not zero.** 5 passes over 1.2 mm, opaque. The hill passes stop on the posts' inner ink edges (x 77.5 and 129.5); there is no overlap |
| Floor a_min = 0.034 | **the height at which the hill meets the posts**, and the footer | Named once, in footer line 3: `a MIN 0.034 — NO KEY GETS ZERO`. **Never in the throat** |
| Uniform level 1/16 | **the tops of the two jamb posts**, plus one 3 mm tick continuing the right post's top outward | Level t = (1/16)/w_bin × hscale, recomputed in the same call (≈ 6.15 mm above the wall line with peak 20.72). The posts are the wall's 5-pass band turned up at each cut edge. Left post ink x 76.25–77.5, right post ink x 129.5–130.75. Their inner ink edges are the slit (52.0 mm). The right post's top runs on as the tick to x 133.75. Nothing else marks a level in the throat (S6, S10) |
| Key identity j | **which bin** K_j ends in | K_j ends on the hill **inside bin(j)**, 0.75 mm above the top pass. It is ≥ 0.92 mm from every lane slot and on the **same side of the 1/16 level as its bin mean, by ≥ 0.6 mm**. Among those points it takes the maximum lane clearance. This forces K12 (bin 6) to x = 99.98 and K2 (bin 9) to x = 107.00. Table in 4d |
| Query identity i | **one continuous thread**: crimson above the hill, green below the wall | The same slot throughout. **Each crimson arrives vertical at x_k = 103.5 + (k − 11)·2.25 and is vertical over its last ≥ 3 mm**, stopping 1.25 mm above the hill's top pass. \|x_Q − x_Z\| ≤ 0.5 mm for 22/22 (S9). Slot 0 lands inside the slit, 1.25 mm from the left post |
| Query order along the slit | lane slot k = 0…21, **equal pitch 2.25 mm** | Unchanged. Seriated on B, Q11 pinned at k = 11, x = ax. Slot → query: [17, 16, 8, 20, 21, 18, 2, 3, 9, 5, 10, **11**, 12, 13, 14, 15, 19, 7, 1, 4, 0, 6] (r07, Hamming cost 87) |
| Score sign s_ij | storm over/under | Q over K ⇔ s_ij ≥ 0 (unchanged). Gap radius 1.15 mm |
| Output Z_i (query i after the reed) | **lane k as a ray of the fan** | In the cloth, lane k is the exact ray θ_k = −2° + (k − 10.5)·Δθ from the fan centre O. Slot order at the slit becomes lower → upper ray (slot 0 = lane 0 = lower selvage) |
| Value j (the key in bin g) | **pick g of the gold weft**, an arc of radius R_g about O (g = 1 nearest the slit … 16 nearest the frame) | Pick order = bin order, so the reader counts picks outward the way they count bins left to right. No index text (S10) |
| a_ij vs 1/16 | **over/under at warp i × pick g** | Gold over ⇔ a_ij > 1/16, at all 352 crossings. **Gold over:** the green gets a gap of r = 1.1 mm. **Gold under:** the gold gets a gap of r = 0.9 mm. **No merging on either thread.** Every crossing is visible on both threads |
| "Principal query" | **the one bold strand**: 2 passes 0.25 mm apart, registered, one out-and-back stroke | Runs top reed → summit → slit → through the cloth → right reed. It is bold in both colours (one thread) and is the **only** multi-pass coloured stroke |
| Consumption (16 K stop, 22 Q pass) | **counts at the reed**, now printed | 38 threads above (22 Q + 16 K). 38 thread families in the cloth (22 warps + 16 picks). Footer line 2: `22 Q · 16 K → 22 Z WARPS × 16 V PICKS` (§8, S13) |

Nothing drawn encodes nothing:
- **The turns** carry "these 16 picks are one value matrix V, one row per pick". They are the physical rule of weft (it wraps the outermost warp), not ornament.
- **The lead-in and lead-out** are the weft's two ends.
- **The posts** carry the 1/16 level and mark the slit's edges.

### 4c. The weave rule and its floors (replaces Revision 1 §4c)

A gold piece is one of three things:
- a **stitch**: both ends are under-gaps;
- a **float**: it spans ≥ 1 gold-over, and both ends are under-gaps;
- a piece that runs into a turn or a lead: its ends are under-gaps or reed ticks.

There is no other kind, so there are **0 gold ends in open paper** by construction.

| rule | value | why |
|---|---|---|
| Gold under-gap | r_u = 0.9 mm (gap 1.8 mm) | 0.15 (half green nib) + 0.4 (half gold nib, the round end cap) + 0.35 mm paper |
| Green gap under gold | r_g = 1.1 mm (gap 2.2 mm) | unchanged; 1.25 around the bold lane |
| Lane pitch along a pick | = Δθ·R_g: **4.50 mm (pick 1) → 5.55 mm (pick 16)** | a polar fan; ≥ 4.3 floor |
| Shortest stitch | 4.50 − 1.8 = **2.70 mm** (floor 2.5) | see the Revision 1.1 note |
| Shortest single float | 2 × 4.50 − 1.8 = **7.2 mm** | |
| Pick spacing along every lane | = s = **4.8 mm** exactly (concentric arcs) | shortest green piece 4.8 − 2.2 = **2.6 mm** (floor 2.0) |
| Longest hidden gold run | **1.8 mm** on every pick (A24 ≤ 25) | nothing is ever merged |
| Visible gold per pick | ≥ 1 − 16 × 1.8 / 94 = **69 %** (pick 1, worst); typically 75–85 % | |
| Crossing angle | **90°** at all 352 (rays × concentric arcs) | ≥ 75° floor |

- The weave floor still keeps picks out of the tight bundle under the slit. The bare warp runs from the slit to the virtual reed R = 300, where pitch is 4.38 mm.
- 0 forced crossings. The caption is true at 352/352.

### 4d. Fit at the slit (A19 × pitch) — measured on the slot plan

| quantity | value |
|---|---|
| slit | **52.0 mm** between the posts' inner ink edges, c = 26.0, ax = 103.5 mm, wall line y = 183.6 |
| bins | 16 × 3.25 mm (edges x = 77.5 + 3.25 g), **never drawn** |
| lanes | 22 at 2.25 mm, x = 78.75 … 126.0. Clearance to the post ink: 1.25 mm (left) and 3.50 mm (right) |
| K landing, offset from bin centre (bins 0…15) | +.75, −.25, +1.00, 0, −1.00, +.25, **+1.35**, +.50, −.50, **−1.38**, −.25, +1.00, 0, −1.00, +.25, −.12 mm. **All inside their own bin.** Bins 6 and 9 moved to the crown side (K12 x 99.98, K2 x 107.00, each 0.25–0.27 mm inside its bin edge) |
| hill height under the 16 landings, minus t | bins 6–9: **+5.7, +14.5, +9.3, +1.9 mm**. Bins 5 and 10: **−0.69, −0.73 mm**. All others ≤ −1.46 mm. Every landing is ≥ 0.6 mm from the level, so a straightedge cannot misread it |
| pointwise hill above t | x ≈ 98.2–108.4. It covers 0 landings of bins 0–5 and 10–15, and all 4 landings of bins 6–9 |
| min K–lane | 0.97 mm (K12 to slot 9 at x 99.0), ≥ 0.92 floor. K–K ≥ 2.25 mm |
| summit | K5 at x 102.38 (bin 7) and K11 at x 104.62 (bin 8). **Q11 at ax lands between its two strongest keys, on the summit** |
| near-post strands | every Q and K within 6 mm of a post is vertical from y ≥ ay + t + 1.5 (≈ 191.3) down to its stop. 0 crossings with post ink; ≥ 1.0 mm of paper to it |

## 5. Composition sketch

Paper: 24 × 30 cm portrait (240 × 300), cream. Drawable area x 10–230, y 10–290 (10 mm
margins). Coordinates are in mm, y up.

- **Wall (structural axis):** y = 183.6, a 5-pass black band from frame to frame. It is broken only by the slit x 77.5–129.5 and **turns up at each cut edge into a post**: one continuous stroke per pass, with a 1.5 mm fillet at the outer corner and a square top. Each post is 1.25 mm wide and stands to the 1/16 level, y ≈ 189.75. The right post's top runs on outward as the 3 mm tick, to x 133.75.
- **Throat (focal point):**
  - The hill spans x 77.5–129.5. It meets the posts at y ≈ 187.1 (left) and ≈ 186.8 (right), each ≥ 2.5 mm below the post tops, and rises to ≈ 204.3 at x ≈ 102.5.
  - The bold strand is the vertical at x = 103.5, from the top reed (y 290) to the summit.
  - `SOFTMAX` (text layer) sits on the wall's right arm: x ≥ 140, baseline 185.6, with no notch around it.
- **Storm (dominant mass), x 10–230, y 186–290:** 22 Q + 16 K, geometry as r07.
  - The only change is the last few mm into the slit: the S9 vertical arrivals, and the near-post strands clearing the post tops.
  - `Q` at the left frame and `K` at the right frame, as r07. **No other text above the wall.**
- **The drain, bare warp (x 78–150, y 70–183):**
  - Each lane leaves the slit perpendicular to the wall, going straight down, and joins its fan ray tangentially at the **virtual reed R = 300** (8 mm before pick 1).
  - Lane pitch never decreases from the slit (2.25 mm) to the virtual reed (4.38 mm). 0 lane–lane crossings.
  - **Lane 0** (lower selvage) passes **(93.5, 150.0)** heading −60°, so it keeps 3.5 mm from the A21 crop. It joins its ray at **(138.7, 70.9)**, with minimum turn radius ≈ 21 mm.
  - **Lane 21** drops from (126.0, 183.6) and joins its ray at **(141.9, 162.4)**. It is the only lane that bottoms out and rises: the fan opens both ways about an axis falling 2°.
- **The cloth: a Deco fan-shell, the second mass (≈ 7,900 mm²):**
  - **Fan centre** O = (−156, 127), off-sheet left. **Axis** −2°. **Ray step** Δθ = 1/68.5 rad, so the fan opens 17.6°: lane 0 at −10.78°, lane 21 at +6.78°.
  - **Picks:** 16 concentric arcs, R_g = 308 + 4.8 (g − 1) mm, so R₁ = 308 and R₁₆ = 380.
    - Pick 1 runs from (146.6, 69.4) on lane 0 to (149.8, 163.4) on lane 21, 94.4 mm long.
    - Pick 16 runs from (217.3, 55.9) to (221.3, 171.9), 116.5 mm long.
    - The arcs bulge toward the frame, with a sagitta of ≈ 4 mm.
  - **Exits:** lanes exit the right frame at **y 53.5 (lane 0) … 172.9 (lane 21)**, with pitch ≥ 5.64 mm. Every exit is ticked. Z11 exits at y ≈ 116.3, and its tick carries `11` (text layer).
  - **Clearances:** lane 21 plus its turns stay ≤ 174.3, which is ≥ 8.7 mm under the wall's underside. Lane 0 is ≥ 56.9 over x 186–212, which is ≥ 8 mm above the `Z = AV` caps (top 48.6).
  - **Why the cloth is 72 mm along the lanes and not ≈ 95.** Its length is 15 × the pick spacing s. A23 requires every turn's apex to be ≤ 2.5 mm outside its selvage. A semicircle on the selvage has apex s/2, so s ≤ 5.0. With s = 4.8, the cloth is 72 mm long (x ≈ 146–224). The bare-warp drain fills x 78–146 as the fan's handle. Pushing the cloth further left would also break the dominant-mass ratio below.
- **The weft's two ends:**
  - **Lead-in:** from a gold reed tick on the **left frame at y = 84.0**, the lead-in runs level to x ≈ 98. It is 8 mm above the `SUMS` caps and forms the floor of the void.
    - It then eases down, staying ≥ 3 mm under lane 0, until it runs 2.4 mm outside lane 0 from x ≈ 139.
    - It enters pick 1 by a quarter circle of radius 2.4, centred on lane 0 2.4 mm before pick 1.
    - `V` (text layer) sits over its first 5 mm: x 11.5, baseline 87.
  - **Lead-out:** from pick 16's lane-0 end, a quarter circle of radius 2.4 runs outside lane 0, then eases to a gold reed tick on the **right frame at y = 50.0**. That is 3.5 mm below lane 0's exit tick, at x ≥ 217, clear of `Z = AV`.
- **Type, flush-left x = 10 (unchanged):**
  - `SUMS` / `TO ONE`: cap 13 mm, baselines SUMS 63 and TO ONE 44.
  - `Z = AV` (4.6 mm caps) sits on the TO ONE baseline, x ≈ 186–212, in open paper under lane 0.
  - 4 footer lines, y 12–32, 5.0 mm leading. Every number is computed in the same call:
    1. `ATTENTION AS WEAVING · ONE REED, ONE CLOTH`
    2. `22 Q · 16 K → 22 Z WARPS × 16 V PICKS   Σa = 1   a MAX 0.190   H 3.76 / 4.00 BITS`
    3. `SLIT 52 MM · 16 EQUAL BINS · LANES EQUAL PITCH 2.25 MM, ORDER ONLY · a MIN 0.034 — NO KEY GETS ZERO`
    4. `BOLD = QUERY 11, ITS ROW IS THE HILL · GOLD OVER GREEN WHERE a > 1/16 (136 / 352) · POSTS = 1/16`

    (If the stroke font has no em dash, use ` - `. Line 3 is ≈ 101 characters, ≈ 177 mm at the r07 footer size, inside x 10–230.)
- **Dominant mass ratio:** storm plus throat (220 × 107 ≈ 23,500 mm²) : cloth (≈ 7,900 mm²) ≈ **3.0 : 1**. The type block (≈ 150 × 32) is the third mass. J1 asks for equal **grammar**, not equal size: the fan-shell below answers the sunburst above.
- **Quiet zones (shaped):**
  - An L of bare paper, x 10–90, y 88–183. Its edges are the wall above, lane 0 on the right and the gold lead-in below. It contains the A21 crop x 10–90, y 100–150.
  - A quiet band x 150–230, y 10–50 holds only the footer's right end, `Z = AV` and the lead-out tick.

## 6. Pen budget

**5 inks, 6 layers.** This exceeds the ≤ 4 bar, and it is stated: each pen carries one meaning,
has one clean layer and is never re-entered. The BRIEF specifies Q/K/V/Z + black (A16, argued).
**Layer order is light → dark**, so black lands last and the reed ticks, wall and posts cover
strand ends.

| layer | pen | meaning | carries |
|---|---|---|---|
| 1 | goldenrod, **broad 0.7–0.8 mm** (gel / POSCA PC-1MR) | **the values V** (one weft) | lead-in, 16 picks (stitches and floats), 15 turns, lead-out, 2 gold reed ticks |
| 2 | dodgerblue 0.3 | **keys K** (consumed) | 16 K spirals, top/right reed → hill |
| 3 | crimson 0.3 | **queries Q** | 22 Q streamlines, vertical arrivals; Q11 double pass |
| 4 | darkgreen 0.3 | **outputs Z = AV** (the warp) | 22 lanes, wall → right frame; bold Z11 double pass |
| 5 | black 0.5 | **structure** | wall + posts (5 passes, one stroke per pass), hill (5 passes), tick, all reed ticks, giant `SUMS / TO ONE` |
| 6 | black 0.3 | **text layer** (house law) | `Q`, `K`, `SOFTMAX`, `V`, `11`, `Z = AV`, footer. Halo 1.3 mm cut into every strand near a label |

## 7. Expressive levers — one decision each

- **Proportion:** storm : cloth ≈ 3.0 : 1. The slit (52 mm between posts) is 0.24 W, the narrowest, loudest thing. The posts add black mass at the throat so it out-weighs `SUMS / TO ONE` at 3 m (r07 art dim 1).
- **Fill vs void:** packed (storm) → silent (the left L) → packed (the cloth). The bare warp fan between the slit and pick 1 is a half-tone between them.
- **Density gradient:**
  - The cloth's cells grow from 4.50 × 4.8 mm at pick 1 to 5.55 × 4.8 mm at pick 16, so the fan-shell opens toward the frame.
  - The storm keeps its native density.
  - Both ramps are consequences of the geometry, not added.
- **Colour play:**
  - Crimson becomes green through the slit (same thread, new role).
  - Gold appears only below the wall.
  - The bold strand is the one scarce loud line.
  - The broad gold nib, now visible on ≥ 69 % of every pick, makes 16 gold arcs read at 3 m as Albers' gold against hairline green rays.
- **Texture direction:** the weft is exactly orthogonal to the warp (90°). This contrasts with the storm's oblique K×Q crossings (≥ 36°). Oblique above (turbulence), orthogonal below (cloth).

## 8. The twist

**What the viewer holds:**
- "Sums to one" (a probability is a partition).
- A loom's reed: a comb every warp thread must pass through.
- The brief's promise that "strand count in = strand count out".

**What the mechanism breaks:**
- The reed does not just space the threads; it **eats** some. All 16 blue threads stop on the hill that is their softmax weight, and only the red pass.
- Yet the count still balances. 38 threads enter the reed (22 Q + 16 K), and 38 thread families make the cloth (22 warps + 16 picks). The keys are spent at the reed, and the values they unlock are woven back in **after** it.
- So the brief's rule survives in a truer form: count in = count out, with the second 16 changing from K to V. **Revision 1.1 prints it** (footer line 2).
- A second, smaller break: the hill never touches the wall. Softmax gives every key something (a_min = 0.034), so the reed's floor is never bare. **Flag for Juan** (with the 38 → 38 reading, which replaces S1's retirement of the rule).

The punchline is at 30 cm. The bold thread that fell onto the summit is covered by gold at
exactly the four arcs whose keys stand where the hill rises above the posts. The hill is that
thread's row; the cloth is everyone's.

## 9. Forbidden list

1. **No gold end in open paper.** The weft has exactly two free ends, both on reed ticks. Every other gold end is an under-gap with a green line through it.
2. **No gold inside the tight bundle.** No pick inside the virtual reed R = 300 (lane pitch there < 4.38 mm).
3. **No overridden crossing and no merge.** The rule a > 1/16 decides all 352 crossings. There is no dead band and no "forced V-over". No run of under-crossings is merged into one hidden stretch, on either thread.
4. **No L-step and no shelf.** *(Rewritten; Revision 1's "zero height, no step" is deleted as impossible.)*
   - The hill never meets the wall line. It meets the posts only, below their tops (≥ 2.5 mm).
   - The only verticals in the throat are the two posts. No bin ticks and no knot discs on the curve.
   - No false hump, unequal bins or inexact area to fake a zero floor.
5. **No chart furniture in the throat.** No cumulative curve, `1.000`, dotted ellipses, equipotentials or a `NO KEY GETS ZERO` label. The floor is named in the footer only. The 1/16 tick sits outside the slit, on the right post.
6. **No text above the wall** except `Q`, `K` and `SOFTMAX` (on the wall arm).
7. **No second doubled strand.** Only the principal thread is bold. K and V are single pass; gold weight comes from its nib.
8. **No lane position implying weight.** Equal pitch at the slit, stated in the footer. No clumps.
9. **No widening the slit to buy pitch.** 52 mm between the posts' inner ink edges.
10. **No arrows, leader lines, compass circles or registration dots.**
11. **No re-seeding or thinning of the storm.** Q rays change only in their final vertical arrival (S9) and in clearing the posts.
12. **No lane–lane, pick–pick or K–K crossing.** Lanes exit the right frame only.
13. **No lane, gold or label in the A21 crop** x 10–90, y 100–150. No cloth growth into it.
14. **No turn of a second radius and no loop apex > 2.5 mm outside its selvage.**

## 10. Fabrication

- **Spacing floors:**
  - Parallel strands ≥ 0.9 mm (house law ≥ 0.8).
  - Weave: lane pitch along picks ≥ 4.3 mm (built 4.50), pick spacing along lanes 4.8 mm.
  - Gold to anything it does not cross ≥ 1.5 mm. The lead-in and lead-out run 2.4 mm outside lane 0.
  - Strands ≥ 1.0 mm of paper from post ink.
  - No hatch on this plate.
- **Gaps:** storm r = 1.15 mm. Green under gold r = 1.1 mm. Gold under green r = 0.9 mm. Strands stop 1.25 mm (Q) and 0.75 mm (K) above the hill's top pass.
- **Pieces:** gold stitches ≥ 2.5 mm (built 2.70), gold floats ≥ 7.2 mm; green ≥ 2.0 mm (built 2.6); storm ≥ 2.3 mm.
- **Flood risk:**
  - The summit is as r07.
  - The posts and the wall are one 5-pass band at 0.25 mm pitch (a solid bar, intended).
  - The hill butts the posts without overlap.
  - Gold never touches green (every crossing is gapped on one thread).
- **Order within each layer (serpentine, batchable):**
  - **Gold:** follow the weft from the lead-in to the lead-out, arc by arc (the weft is already a boustrophedon).
  - **Green and crimson:** serpentine in slot order.
  - **Blue:** by reed position.
  - **Black:** left wall arm + left post, hill, right post + tick + right arm, reeds clockwise, then type.
  - **Text:** top → bottom.
  - Never a sheet-crossing travel between consecutive strokes. Target travel < draw (A14; r07 0.53).
- **Estimated draw / time** at F600 (10 mm/s) and ≈ 2.5 s per lift cycle:

| layer | draw | pieces | minutes |
|---|---|---|---|
| gold | ≈ 1.57 m (weft 1.96 m − 216 × 1.8 mm) | ≈ 217 | ≈ 11.7 |
| blue | ≈ 2.1 m | ≈ 65 | ≈ 6.6 |
| crimson | ≈ 2.25 m | ≈ 82 | ≈ 7.5 |
| green | ≈ 3.9 m (longer fan lanes) | ≈ 160 | ≈ 13.5 |
| black structure | ≈ 3.7 m | ≈ 173 | ≈ 14.6 |
| black text | ≈ 1.15 m | ≈ 345 | ≈ 17 |
| **total** | **≈ 14.7 m** | | **≈ 71 min** |

  Add the frame trace and 5 swaps. The gold layer grows from 3.9 to ≈ 11.7 min, because
  visibility costs lifts (217 stitches). This is the price of J1 and is stated. The designer
  reports the measured numbers per layer, and **a nib-width preview**
  (`GCodeVisualizer.preview(pen_widths=)`, gold at 0.8 mm) next to the hairline png.

## 11. Acceptance checks (art critic marks each PASS/FAIL from the png; mm = preview axes; use the nib-width preview for gold)

1. **Weft closed, no crumbs.**
   - One gold path: from the left-frame tick at **y 84.0 ± 1**, through 16 arcs and 15 turns, to the right-frame tick at **y 50.0 ± 1**.
   - **Every gold end is either one of those two ticks or a gap with a green line through it.** 0 gold ends in open paper.
   - **0 gold pieces < 2.5 mm.**
2. **The cloth answers the storm (J1, A24).**
   - Pick 1 lies at x ≈ 146–150 and pick 16 at x ≈ 217–222.
   - The 22 green exit ticks span **y 53.5 … 172.9 ± 1.5**, ≥ 5 mm apart.
   - Lane 0 is ≥ 8 mm above the `Z = AV` caps.
   - **On every arc, gold is visible over ≥ 65 % of its length between lane 0 and lane 21, and no gold gap is longer than 2.0 mm.** The HANDOFF gives the gcode figure, gold draw ≥ 1.5 m, and the critic spot-checks 3 arcs.
   - Each arc reads as ONE stitched gold line, not as separate dashes.
3. **A woven selvage (A23).**
   - All 15 turns are semicircles of **one radius, 2.4 ± 0.2 mm**.
   - Each apex is **2.4 ± 0.3 mm outside** its selvage lane: 8 above lane 21, 7 below lane 0.
   - The 8 upper apexes lie on one straight line parallel to lane 21, and the 7 lower apexes on one parallel to lane 0 (deviation ≤ 0.3 mm).
4. **The cloth is the matrix.**
   - Every arc crosses all 22 green rays once, at 90 ± 3°.
   - The bold green ray is under gold at **exactly 4 arcs, the 7th–10th from the slit**, and over gold at the other 12.
   - No gold lies inside the virtual reed: the bare warp under the slit shows no gold.
5. **Throat: an honest floor (A19, S12, J2).**
   - Slit 52.0 ± 0.3 mm between the posts' inner ink edges.
   - **Each jamb is a post** that rises from the wall in one stroke to a square top. The left post's top is level with the right post's top, and the right one runs on as the 3 mm tick.
   - **The hill's two ends meet the posts' inner faces at 3.0–3.8 mm above the wall line, and each post continues ≥ 2.5 mm above that meeting point.**
   - The hill never touches the wall line. There is no vertical in the throat except the two posts.
   - Test crop x 72–136, y 182–206: two posts, one smooth curve strung between them, its crown alone rising above the post tops.
   - The bold vertical meets the summit (Q11 at the centre line, between K5 and K11).
   - Footer line 3 contains `a MIN 0.034 — NO KEY GETS ZERO`.
6. **The 1/16 test (eye = gcode).** Lay a straightedge through the two post tops (y ≈ 189.75, the tick's level).
   - **Exactly four blue landings stand over hill that is above the straightedge: the 7th, 8th, 9th and 10th from the left.** The hill's middle pass under each is ≥ 1.5 mm above it (built: +5.7, +14.5, +9.3, +1.9).
   - Under each of the other 12 landings, the middle pass is ≥ 0.6 mm below it (built: bins 5 and 10 −0.69 and −0.73; all others ≤ −1.46).
   - The science critic checks the same four keys by bin mean (bins 6–9 = keys 12, 5, 11, 2). **Bin edges are not part of the test**; they are not drawn.
7. **Every thread closes, and Q_i = Z_i (S9).**
   - Each of the 22 crimsons is vertical over its last ≥ 3 mm, at the same x as the green that leaves the wall below it (≤ 0.5 mm, 22/22).
   - The leftmost crimson ends inside the slit, ≥ 1.0 mm of paper from the left post.
   - No strand crosses a post.
   - 16 blue end on the hill, each in a different bin.
   - 22/22 green exits are ticked, and `11` marks the bold one.
   - Top/right reed mouths are all ≥ 3 mm apart, with no shared tick (A22).
8. **Void and text discipline (A21, A20, A11, S13).**
   - Crop x 10–90, y 100–150: **0 marks of any colour.**
   - Above the wall there is no text except `Q`, `K` and `SOFTMAX`, and `SOFTMAX` is not in a notch.
   - `Z = AV` is on the TO ONE baseline with ≥ 3 mm of bare paper around it.
   - **Footer line 2 reads `22 Q · 16 K → 22 Z WARPS × 16 V PICKS`.**
   - The bold strand reads as ONE line, never two.
