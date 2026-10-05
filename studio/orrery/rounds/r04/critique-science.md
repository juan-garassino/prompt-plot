# Science critique — orrery r04 · machine learning (transformer attention) · 2026-09-29
render: gallery/studio/orrery/current/pp_orrery_iterate_v11.png  (gcode: gallery/studio/orrery/current/pp_orrery_iterate_v11.gcode, 24 557 cmds; blue 27 / crimson 53 / black 1 084 strokes)

**Process note.** `studio/orrery/` still has no `dossier.md` and no `encoding.md`, so there is no §7, §4 or §5 to grade against. The check numbers below come from the sources HANDOFF names: `rounds/r02/gpt2_head.npz` (Q, K, A, tokens, ids), `~/.promptplot/attn_gpt2.npz` (144 heads), and the law printed on the sheet. I did not run `checks.py` (designer code under the round). This is pass 2 because LEDGER.md exists.

**Method.** I parsed the gcode per `; color=N`. The orbit centre is (105.000, 191.700): an algebraic circle fit on all 27 blue strokes gives spread ≤ 0.035 mm, and the sun spiral ends there too. For each stroke I converted to polar coordinates (angle measured from the bottom slot, CCW) and fitted r(a) = R + A·sin(κa + φ) by linear least squares with a fine grid search on κ. Residual rms is ≤ 0.007 mm on 24 strokes and ≤ 0.014 on the transformer passes. The phase step between a key's two turns is (φ₂ − φ₁)/2π mod 1.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| attn row L4H3 q12, keys 0–12 | — | softmax(K·q/8) from the npz Q, K = .1142 .0583 .0313 .0139 .0050 .0060 .0105 .0625 .0151 .0522 .5572 .0618 .0119 (vs npz A: 4e-8; vs attn_gpt2.npz: 1.0e-6). Keys 13–14 = 0 (causal) | labels .114 .058 .031 .014 .005 .006 .011 .063 .015 .052 .557 .062 .012 (.01053→.011, .06251→.063 round correctly) | OK 13/13 |
| tokens / BPE (S8) | — | npz tokens `The · pen · plot · ter · drew · a · black · hole · while · the · transformer · watched · itself`, ids 464 3112 7110 353 9859 257 2042 7604 981 262 47385 7342 2346 | same 13 strings in the slot column | OK |
| widest shortfall s* − s | — | 4.7097 (drew) = ln(w*/w) exactly | caption "drew, 4.71" | OK |
| divisor | — | 2.5 × 4.7097 = 11.774 | caption 11.77, stated as 2.5 × widest | OK |
| d per key = gap/11.77 | — | The .1346 · pen .1918 · plot .2448 · ter .3134 · drew .4001 · a .3844 · black .3372 · hole .1859 · while .3063 · the .2012 · transformer 0 · watched .1868 · itself .3271 | fitted frac(κ) .1360 · .1924 · .2461 · .3140 · .3984 · .3846 · .3378 · .1860 · .3062 · .2010 · .0005 · .1866 · .3268. Turn-to-turn phase step .1341 · .1920 · .2453 · .3136 · .3995 · .3849 · .3380 · .1858 · .3058 · .2013 · 0 · .1870 · .3265 | OK, all within ±0.0016 lobe |
| κ = n + d | — | n = 14 18 22 27 33 39 46 52 56 62 69 74 78 | κ 14.136 … 78.327; transformer 69.000 on all 3 passes, in phase (φ 1.568–1.571) | OK |
| 2 turns per key; closure after 2 turns | — | 2d ∈ [0.269, 0.800]. The distance from a whole lobe is min(2d, 1−2d), smallest for **drew, 0.200** (next: a, 0.231; The, 0.269; plot is farthest at 0.490). No miss closes | 12 keys × 2 strokes + 3 transformer passes = 27 | OK (but see mandate 2 on the caption's wording) |
| band width 1.3 + 12.7(d − 0.135) | — | The 1.295 · pen 2.022 · plot 2.694 · ter 3.566 · drew 4.667 · a 4.467 · black 3.868 · hole 1.946 · while 3.476 · the 2.141 · watched 1.957 · itself 3.740 | 1.299 · 2.029 · 2.704 · 3.576 · 4.680 · 4.479 · 3.878 · 1.951 · 3.486 · 2.146 · 1.963 · 3.750 | OK, all within +0.013 mm |
| band scale (affine, disclosed) | — | widest/narrowest d = 2.97; the formula gives −0.41 mm at d = 0 | widest/narrowest width 4.680/1.299 = **3.60** | disclosed truncated scale (lead's A8 amendment), not a lie |
| inter-band gap | — | not data | constant **2.83 mm** everywhere except around transformer (5.18 each side) | see mandate 1 |
| lobe amplitude / wavelength (not data) | — | constant | A 0.489–0.492 mm on all 27. λ 6.78–7.28 mm | OK, no fake channel |
| closing-orbit passes | — | "3 passes 0.35 mm apart" | R 76.344 / 76.711 / 77.078 → **0.367 mm** | off by 0.017 mm (mandate 2) |
| orbit coverage (S5) | — | — | transformer is one continuous 14.4°→352.7° per pass (94.0 %). The 6 % lost is only the token slot. All orbits 79.5 % (The) to 94.5 % (itself), all loss in the slot. Disc bbox x 13.7–196.3, y 101.2–282.9, inside the 10 mm margin | frame clipping gone |
| head disclosure (S6) | — | L4H3 = 0.5572, **rank 1/144** for itself→transformer; next 0.4159; mean 0.0534; 106/144 heads argmax key 0; 6/144 argmax transformer | caption: "strongest of 144 … (next .416, mean .053). 106 of 144 heads look hardest at The, the position-0 sink" + `sink` tag over `The` | OK |
| query position | — | `itself` is index 12 (0-based), i.e. the 13th of 15 tokens | caption "query itself (12 of 15)". Read 1-based, that is `watched` | ambiguous (mandate 2) |

## Lies list
Built from the sheet's own claims, because no dossier §4 exists.

| item | status |
|---|---|
| Printed weights differ from the model | clean (13/13 to 3 dp, and recomputed from Q·K) |
| The drawn drift is not the printed law | clean (κ, phase step and band width all match the law to ≤ 0.0016 lobe / 0.013 mm) |
| "an orbit closes only if … kappa whole only where d = 0" | clean. S4 fixed: 2d_max = 0.800 < 1, and the only integral κ is transformer's (69.000) |
| "after two turns the worst key is still 0.8 of a lobe out, so no miss can close" | **misleading.** The conclusion is true, but 0.8 lobe of drift is 0.2 lobe short of closure, which makes drew the miss that comes *closest* to closing. The premise inverts the margin |
| "3 passes 0.35 mm apart" | minor inaccuracy: 0.367 mm measured |
| "query itself (12 of 15)" | ambiguous off-by-one: 0-based index printed next to a 1-based "of 15" |
| "the width of its band is its miss" (readable on the sheet) | **not readable** for 6/12 keys. Band width is larger than the 2.83 mm inter-band gap for drew 4.68, a 4.48, black 3.88, itself 3.75, ter 3.58 and while 3.49, so on any ray a turn-1 strand sits closer to the neighbouring orbit's strand than to its own turn 2. The 3 o'clock ray reads as a uniform comb of 25 strands |
| Closure is visible as closure | not shown. Every turn is its own stroke, and both are cut at the slot, so the seam where turn 2 would meet turn 1 is inside the label slot. "Closes" appears only as 3 coincident passes, and "misses" as a radial offset set by construction |
| Head cherry-pick / sink hidden (r03) | clean, disclosed and true |
| Attention framed as coreference (r03) | clean ("where does this head look from itself?") |

## Scores
- truth: **8**. Data, law, constants and disclosures are all exact and verified against both npz files. What remains is caption wording: the "0.8 of a lobe" margin is inverted, "12 of 15" is an off-by-one, and 0.35 should be 0.367.
- encoding fidelity: **8**. Every channel carries its quantity to ≤ 0.013 mm / 0.0016 lobe, and there are no decorative data channels. The band scale is affine (3.60:1 drawn for 2.97:1 of d), but it is disclosed on the sheet.
- insight legibility: **7**. The thick triple ring labelled `transformer .557` answers the red question at once, and the sink disclosure lands. The plate's second reading, "the width of its band is its miss", cannot be read at a glance: 6 of 12 bands are wider than the gap to their neighbour, so strands do not visibly pair. The closure phenomenon the title names is never drawn as a closure.
- **VERDICT: FAIL**

## Mandates
1. **Make each key's two turns visibly pair.** The inter-band gap is a constant 2.83 mm (the disc, every ray, e.g. the 3 o'clock ray x 105–196 at y 191.7). It is smaller than 6 of the 12 band widths: drew 4.68, a 4.48, black 3.88, itself 3.75, ter 3.58 and while 3.49 mm. For those keys the nearest strand to turn 1 belongs to another token, and the disc reads as a uniform comb (spacings 1.30–4.68 alternating with 2.83). **Expected:** at every key, the gap to the neighbouring orbit ≥ that key's own band width + 1 mm, measured centre-line to centre-line, so that each pair is the tightest spacing around it. Two ways to get there: rescale the (still affine, still stated) band map down, e.g. 0.9–2.6 mm, and hold a ≥ 3.6 mm gap; or widen the gap and cut n / R₀ to fit the frame.
2. **Every number in the caption true as written** (black caption block, x 130–195, y 14–50). (a) "after two turns the worst key is still 0.8 of a lobe out". Measured: 2d_drew = 0.800, which is **0.200 lobe from closing**, the *smallest* margin of any miss (a 0.231, The 0.269). Expected wording: the nearest miss (drew) stays 0.2 of a lobe from closing. (b) "3 passes 0.35 mm apart": measured 0.367 mm (R 76.344/76.711/77.078). Print 0.37 or emit 0.35. (c) "query itself (12 of 15)": `itself` is index 12 zero-based, the 13th of 15 tokens. Print "13th of 15" or "position 12, counting from 0".
3. **Draw the closure the title promises.** Measured: 27 blue strokes, each exactly one turn, all cut at the token slot (left end x = 95.34, right end x 113.5–126.3). The seam where turn 2 would return onto turn 1 lies inside the slot for all 13 keys, so no closing or non-closing is ever visible. The transformer's closure is shown only as 3 coincident passes (φ 1.568–1.571, κ 69.000). **Expected:** each orbit drawn as one continuous 2-turn curve whose seam falls outside the slot, with the slot moved or the seam placed at ≥ 30° from it. At the seam, transformer lands on its own start (0 mm radial step, 0 lobe phase). Each miss visibly steps out by its band width w with phase jump d. The step at the seam then *is* the miss, and it can be read at one point per orbit.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S4 | **FIXED** | divisor 11.77 = 2.5 × 4.7097 (printed), 2 turns. 2d_max = 0.800 < 1, and fitted frac(κ_drew) = 0.398/0.400. The only integral κ is transformer's 69.000. (Caption wording of the margin: mandate 2a) |
| S5 | **PARTIAL** | Frame clipping is gone: disc x 13.7–196.3, y 101.2–282.9, inside margins. The closing orbit is continuous everywhere outside the label slot (94.0 %, 3 passes). Letter of "≥ 95 % for every orbit" not met: 79.5 % (The t1) to 94.5 % (itself t2), all lost to the slot, none to the frame. No truth consequence except the hidden seam (mandate 3) |
| S6 | **FIXED** | recomputed rank 1/144 (0.5572), next 0.4159, mean 0.0534, 106/144 argmax key 0. All printed correctly. `sink` tag on `The`. The question now asks where *this head* looks |
| S7 | **NOT FIXED** (from the critic's side) | still no `dossier.md` / `encoding.md`. HANDOFF now carries source, law and constants, which was enough to recompute everything, but there is still no §4 lies list and no §5 misconception to grade. NOTES is off-limits to this critic |
| S8 | **FIXED** | tokens and BPE ids are read from `rounds/r02/gpt2_head.npz` (`plot` 7110 + `ter` 353). The row matches Q·K/8 softmax to 4e-8 and attn_gpt2.npz to 1e-6 |
| regression check | none | every truth that held in r03 (exact weights, exact drift law, no fake amplitude channel) still holds, and tighter (±0.0016 vs ±0.003) |
