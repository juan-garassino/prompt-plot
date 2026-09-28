# Science critique — attention-weaving r04 · machine learning (transformer attention, softmax) · 2026-09-28
render: ~/Downloads/pp_attention_weaving_mirror-drain_v13.png (gcode: ~/Downloads/pp_attention_weaving_mirror-drain_v13.gcode, seed 7, 24x30 portrait)

Pass 1 (cold). There is **no `dossier.md`, no `encoding.md` and no `LEDGER.md`** for this slug, and that is a
finding in its own right: nothing states the §7 check numbers, the §4 lies list or the §3–4 channel
mapping. So the check numbers below are the claims printed on the sheet (the footer) plus the
"What must be TRUE" list in `BRIEF.md`. Each was measured from the gcode. Q, K and Z were rebuilt as
whole strands by chaining the fragments across their over/under gaps: 22 Q, 16 K, 38 Z and 16 V.
Doubled passes were collapsed into one strand each.

## Check numbers
| quantity | claim (sheet) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Σ A (softmax row) | 1.000 | cumulative of per-key A = 1.0000 | cumulative curve ends at y=205.98 over (77.54→129.46), labelled 1.000; ∫hill vs cumulative max err 0.00035 | OK |
| A max | 0.190 | 0.1899 (from cumulative at key ticks) | hill area in key 6 = 0.1900 | OK |
| H(A) | 3.76 / 4.00 bits | log2 16 = 4.00; H = 3.763 bits | from hill areas 3.762 | OK |
| key count | 16 (implied by 4.00 bits) | 16 | 15 clump ticks inside the slit → 16 bins | OK |
| slit width | 52 mm | 51.92 | wall gap x 77.54 → 129.46 | OK |
| strands in / out | 38 / 38 | 22 Q + 16 K = 38 | 23 Q passes + 18 K passes reach the slit (1 Q and 2 K double-passed) = 38 strands; 38 Z leave (36 right edge, 2 bottom edge) | OK as a count, **wrong as science** (see mandate 1) |
| scores cross | 113 / 352 | 22 × 16 = 352 | 113 Q×K strand pairs intersect above the wall; 0 pairs cross twice. 111 are visible; 2 fall inside the "1.000" label halo, where both strands are cut | OK as a count |
| values cross | 608 / 608 | 16 V × 38 Z = 608 | every V crosses all 38 Z (38 each), 608 crossings in total | OK |
| pitch | 0.90 mm | — | Z lane spacing at the slit: 0.95 / 1.84 mm, alternating. **Minimum Z-to-Z separation in the rope is 0.75 mm at (110.1, 163.5)**; 22 of the 37 adjacent pairs drop below 0.90 somewhere | **VIOLATED** (the caption claims a pitch no lane holds) |
| over/under | real | — | Q×K: 51 Q-over, 60 K-over, 0 both drawn, 2 neither (label halo). V×Z: 315 V-over, 293 Z-over, 0 both drawn, 0 neither | OK |

Per-key A recovered from the sheet: [.034 .038 .045 .051 .066 **.190 .139** .080 .056 .054 .046 .045 .044 .041 .037 .036]

## Lies list
There is no dossier §4, so these are checked against the BRIEF "What must be TRUE" list plus the attention maths.

| item | status |
|---|---|
| Everything passes through the waist (count in = count out) | clean. 38 in, 38 out. No Q, K or Z strand dies away from the slit or a margin. |
| Over/under is real | clean. At every crossing exactly one strand is drawn. |
| Softmax normalises (peaked, not uniform) | clean. Σ = 1.000; max is 3.04× uniform; H = 3.76 bits. |
| V joins after the waist | clean. All V ink lies at y ≤ 178.4, below the wall at 183.6. |
| Braid carries more strands than Q or K alone | clean: 38 > 22 > 16. But see the next row: the rule is itself wrong. |
| **Z = AV has one row per QUERY** | **VIOLATED** (rope, y < 183.6). The sheet draws 38 Z lanes = n_Q + n_K. Z = AV has n_Q = 22 rows. Each K strand becomes an output lane, but keys are consumed by the softmax; they never become outputs. **The brief's "count in = count out" rule is scientifically wrong** and the plate faithfully inherits it. |
| **A bin is a key; a K strand is that key** | **VIOLATED** (slit x 77.5–129.5). There are 16 K strands and 16 key bins, but K lanes per bin = [1,1,1,**0**,1,**2,2**,1,1,1,1,1,**0**,1,1,1]. Keys 4 and 13 receive no K strand. |
| Emphasis means something | **VIOLATED.** The doubled V strands are keys 6 and 7, the top two (A = .190, .139). The doubled K strands land in keys 6 and **11** (A = .046, rank 9). There is also a doubled Q (x = 103.5, key 8) with no legend. Two different rules for "bold" on one sheet. |
| Hill height reads as A | **VIOLATED (partial).** The hill is area-true but height-false. Bin widths are 2.79–5.64 mm, set by lane count. Peak/median height is 2.09, against a peak/median A of 4.21, so the eye reads the peak as half as sharp as it is. |
| Caption numbers are true | pitch 0.90 mm is **false** (0.75 mm measured). The other 8 caption numbers are exact. |

## Scores
- **truth 6**: 8 of the 9 caption numbers are exact to 3 decimals, and the softmax itself is exactly right. But the topology asserts |Z| = |Q| + |K| = 38, which contradicts Z = AV (it should be 22). K strands turn into outputs. One query's softmax row is drawn without saying which of the 22 queries owns it. The pitch caption is false.
- **fidelity 6**: the hill area and the cumulative curve are exact. Everything else is loose:
  - The lanes per key, [2,2,2,2,2,5,4,3,2,…], give shares of 0.053–0.132. The true A range is 0.034–0.190. The largest-remainder apportionment of 38·A would be [1,1,2,2,3,7,5,3,2,2,2,2,2,2,1,1].
  - Hill heights are compressed about 2× because the bins are unequal widths.
  - The K-to-key mapping is broken (two empty bins), and the bold passes follow two different rules.
  - Reed ticks mark 32 of 38 Z exits. Right-edge ticks are missing at y = 77.3, 80.1, 88.0, 93.1, 107.2 and 137.0.
  - 9 of 16 K strands start in open sheet on a diagonal from (165.6, 186.8) to (222.8, 245.1), with no reed tick.
- **legibility 7**: "SUMS TO ONE", the hill and the cumulative curve reaching 1.000 land for a stranger. "608/608 values cross" correctly shows that softmax never zeroes a value. But "113 / 352 SCORES CROSS" reads as "only a third of the scores are computed". In attention all 352 are computed and all enter the softmax. The hill has no A axis, only the cumulative endpoint.
- **VERDICT: FAIL**

## Mandates
1. **Output count (rope, below the wall, and footer "38 IN, 38 OUT").** Measured: 38 Z = AV lanes. They are the continuations of 22 Q + 16 K strands, so every key becomes an output row. Expected: n_Z = n_Q = **22** lanes, one output row per query. The 16 K strands should terminate at the aperture, where the softmax consumes them. Each Z lane is then the V-mixture for its query. Correct the footer to "22 Q · 16 K → 22 Z". The BRIEF rule "count in = count out" must be retired; it is the source of this error.
2. **Weight → mark (slit bins x 77.54–129.46, hill y 183.6–205.5).** Measured: bin widths are 2.79–5.64 mm, set by lane count. Hill height peak/median is 2.09 against an A peak/median of 4.21. Lanes per key are [2,2,2,2,2,5,4,3,2,2,2,2,2,2,2,2], a max share of 0.132 against an A max of 0.190. Expected: 16 equal bins of 51.92/16 = **3.245 mm**, so hill height ∝ A and peak/median height = 4.2. Lanes per key should be the largest-remainder apportionment of A: for 22 lanes, [1,1,1,1,1,4,3,2,1,1,1,1,1,1,1,1]. Key 6 then carries 4/22 = 0.18 of the flow.
3. **Key identity and emphasis (upper field → slit, footer).** Measured: K lanes per bin = [1,1,1,0,1,2,2,1,1,1,1,1,0,1,1,1]. The doubled K strands land in keys 6 and 11 (A = .190, .046); the doubled V strands mark keys 6 and 7; the doubled Q lands in key 8, with no legend. The footer "PITCH 0.90 MM" is contradicted by a 0.75 mm Z separation at (110.1, 163.5). Expected:
   - exactly one K strand into each of the 16 bins (K_j → bin j);
   - bold strands only on the top-2 keys, 6 and 7, for both K and V;
   - the bold Q labelled as "the query whose row is drawn";
   - either no lane pair closer than the printed pitch, or the printed pitch equal to the measured minimum.

## Follow-up on open mandates
No LEDGER.md exists for this slug, so there are no open S* mandates. Pass 1 only.
