# Science critique — orrery r02 · machine learning (transformer attention) · 2026-09-28
render: gallery/studio/orrery/current/pp_orrery_orbits-that-mean_v13.png (+ .gcode, 22354 cmds, 5 pens, a4 portrait)

Pass 1 (cold). **Process finding:** `studio/orrery/` has no `dossier.md`, no `encoding.md`
and no `LEDGER.md` — so there are no §7 check numbers, no §4 lies list and no §5
misconception to grade against. The check numbers below are ones I derived myself from the
HANDOFF's claims. The lies list is my own reading of those claims.

**Data provenance, verified independently.** I wrote a fresh numpy GPT-2-small forward pass
from the raw safetensors weights, with token ids checked against vocab.json. Layer 4, head 3
reproduces `gpt2_head.npz` Q/K/V/A/Z to a max abs error of 4.7e-7. The data is real.

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| A[itself→transformer] | — | 0.5572 (11.14 × 5 %) | groove 11.144 turns; 11 ochre lines | OK |
| A[itself→The] | — | 0.1142 (2.28) | groove 2.285 turns; 2 lines | OK |
| A[→hole / watched / pen / the] | — | .0625/.0618/.0583/.0522 | grooves 1.250/1.237/1.165/1.044 turns; 1 line each | OK |
| A[→plot / while / ter / itself / black / a / drew] | — | .0313/.0151/.0139/.0119/.0105/.0060/.0050 | grooves .625/.303/.279/.237/.210/.121/.100 turns | OK (all 13 grooves exact to 0.003 turn) |
| Σ grooves vs Σ ochre lines | — | 20.00 turns = 100 % | grooves 20.00 turns; **ribbons 18 lines = 90 %** | MISMATCH vs legend "one turn = one ochre line" |
| groove pitch | — | constant | 0.850 mm/turn, ±0.002 | OK |
| groove end angle = token angle | — | 150°−10°·j | every groove ends at its token's angle (The 150° … itself 30°) | OK |
| \|q_itself\| | — | 11.317 | dot at 11.36 units (0.911 mm/unit); **label "\|q\| = 12"** | dot OK / label WRONG |
| \|k_j\| (15 keys) | — | 7.39 … 28.53 | dot radii match to ≤0.07 units, shared 0.911 mm/unit with Q | OK |
| \|v_j\| (15 values) | — | 0.713 … 4.725 | dot radii match to ≤0.05 units at 4.444 mm/unit | OK |
| \|z\| | — | 2.589 | green ring r=27.00 mm → **10.43 mm/unit** (V panel: 4.444) | value OK, SCALE ≠ V |
| \|a₁₀v₁₀\| (deferent) | — | 2.265 | ochre ring r=23.62 mm (10.43 scale) | value OK, drawn larger than \|v₁₀\|=4.065 (18.07 mm) |
| epicycle step lengths | — | \|a_j v_j\| = .295/.238/.213/.163/.115 | 0.183/0.131/0.118/0.063/0.045 — an exact orthogonal projection onto span(a₁₀v₁₀, z) | UNDERSTATED 1.6–2.6× |
| epicycle node radii | — | \|S_k\| 2.265→2.582 | projected \|S_k\| matches to ≤0.012; chain ends 26.92 mm vs z dot 27.00 (last 3 terms dropped) | OK (0.08 mm) |
| causal mask | — | " think", "." masked | open circles on K, V and dial (−20°/−10°, dial 10°/20°) | OK |
| keys ≥ 2.5 % | — | The, pen, plot, hole, the, transformer, watched | big dots on K/V/dial; K hairlines to their own tick (≤1.55 mm); Q hairlines to those same 7 ticks | OK |
| ribbons per key | — | 2,1,1,1,1,11,1 | The 2, pen 1, plot 1, hole 1, the 1, transformer 11 (fanned bundle), watched 1 | OK (rounding) |
| sentence order | — | left→right | planets −150°→−10° CCW; dial 150°→30° | OK |

## Lies list       item | clean / VIOLATED (where)
| item | status |
|---|---|
| Data is the stated model/layer/head/query | clean (independent recompute, 4.7e-7) |
| 1 turn = 5 % attention | clean (13/13 grooves, 20.00 turns) |
| "one turn = one ochre line = 5 %" | **VIOLATED**: the legend (lower left, ~y 45 mm) equates the two, but the ribbons total 18 lines (90 %) against 20 turns. Six keys (6.2 % of the mass) have grooves but no line, and the rounding is not disclosed |
| Q and K on a shared scale (they meet in a dot product) | clean (0.911 mm/unit both) |
| V and Z on a shared scale (z = Σ a_j v_j lives in V-space; \|z\| ≤ max\|v\|) | **VIOLATED**: Z panel is 10.43 mm/unit, V panel is 4.444 mm/unit (2.35×). \|z\|=2.59 is drawn at 27 mm, bigger than the V graticule's "5" ring (22.2 mm). The 0.557-scaled a₁₀v₁₀ deferent (23.6 mm) is drawn 1.31× larger than v₁₀ itself (18.1 mm) |
| Epicycle = one token's contribution | **VIOLATED**: the radii are projected lengths, 38–62 % short, rank flipped at steps 6/7, no caption says "projection" (Z panel, 105–110, 90–94) |
| Norm labels are measurements | **VIOLATED**: "\|q\| = 12" (37, 231) labels the graticule's outer ring, but the query's norm is 11.32. "\|k\| = 28": 4 keys exceed it (max 28.53). "\|v\| = 5": max is 4.73. Graticule values written in value notation |
| "ring = the norm of a row" | partly VIOLATED: on Q/K/V the rings are unlabelled graticules (steps of 4 units on Q/K, 1 unit on V). Only the dot radius, and the Z ring, is a norm |
| Decorative marks posing as data | the ✳ at (105, 98.5) and the doubled r=52 dial rim (an identical stroke inked twice) have no key |

## Scores          truth · fidelity · legibility · VERDICT: PASS | FAIL
- **truth 8**: the data, the attention row, all 43 norms, the order and the mask are exact. What is wrong is the captions ("\|q\| = 12", "ring = the norm").
- **encoding fidelity 6**: V and Z are drawn at different scales, which inflates z and a·v. The epicycles understate each contribution. The ochre lines carry 90 % of the mass under a legend that says 100 %.
- **insight legibility 7**: the headline lands, because " itself" → " transformer" (55.7 %) shows as the 11-turn outer groove, an 11-line bundle and the blue underline. A stranger still cannot read the graticule steps, the Z panel's relation to V, the epicycles or the ✳. There is no written misconception correction (no dossier §5).
- **VERDICT: FAIL**

## Mandates        1. … 2. … 3. …
1. **Put V and Z on one scale.** Measured: the Z panel (centre 105, 67) is at 10.43 mm/unit, so the \|z\|=2.589 ring is r=27.00 mm and the a₁₀v₁₀ deferent (2.265) is r=23.62 mm. The V planet (centre 175.9, 101.6) is at 4.444 mm/unit, so v₁₀ (4.065) sits at 18.07 mm. Expected: both at 4.444 mm/unit, giving a \|z\| ring of 11.51 mm and a deferent of 10.07 mm. The other option is a Z-panel graticule labelled in the same units, with a printed "×2.35" and a z dot drawn inside the V panel. Either way, a·v must never be drawn bigger than v.
2. **Make each epicycle radius the true contribution \|a_j v_j\|.** Measured: the steps are projections onto span(a₁₀v₁₀, z), drawn as circles of r = 1.91 / 1.36 / 1.23 / 0.66 / 0.47 mm. Expected at 10.43 mm/unit: 3.08 (hole) / 2.48 (watched) / 2.22 (pen) / 1.70 (the) / 1.20 (plot). That is 1.6–2.6× larger, and the rank must be preserved. The chain at (105–110, 90–94) should embed each step at true length while keeping \|S_k\| (the triangle inequality guarantees such a 2D embedding exists) and close on the z dot (it is 0.08 mm short today). The alternative is to caption it "projected onto (a·v_transformer, z)".
3. **Make every printed number true.** "\|q\| = 12" at (37, 231) should read the query's norm, \|q_itself\| = 11.3 (measured dot 11.36). Move graticule values to their rings as plain numbers (Q/K steps of 4, V steps of 1). The same applies to "\|k\| = 28" (max 28.53) and "\|v\| = 5" (max 4.73). The legend "one turn = one ochre line = 5 %" (lower left) is false as written: 20.00 turns against 18 lines, with 6.2 % of the mass on six keys getting no line. Either draw the remainder (e.g. one dashed ochre line carrying the pooled 6.2 % plus rounding), or print "lines rounded to 5 %; keys < 2.5 % omitted". Also either key or remove the ✳ at (105, 98.5).

## Follow-up on open mandates   id | status | evidence
No `studio/orrery/LEDGER.md` exists, so there are no open S* mandates. This is pass 1 only.
