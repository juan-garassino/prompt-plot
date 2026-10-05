# Science critique — orrery r03 · machine learning (transformer attention) · 2026-09-29
render: gallery/studio/orrery/current/pp_orrery_resonant-orbits_v14.png  (gcode: gallery/studio/orrery/current/pp_orrery_resonant-orbits_v14.gcode, 30 333 cmds, 3 pens)

**Process finding:** `studio/orrery/` has **no `dossier.md`, no `encoding.md`, no `LEDGER.md`**. There is
no §7 check-number list, no §4 lies list, and no §5 misconception to grade against. The check
numbers below are recomputed from the source the HANDOFF names (`~/.promptplot/attn_gpt2.npz`,
`attn[4,3,12,:13]`) and from the formula printed on the sheet
(`kappa = n + (s* − s)/18.84`, `s = q·k/8`). The lies list is built from what the sheet and
HANDOFF claim. This is pass 1 because there is no ledger.

Method: I parsed the gcode per `; color=N` layer. The sun centre is (70.12, 171.89), taken from the
crimson disc's bbox. There are 13 blue orbits at R = 15 + 7.5·i mm, each a sinusoid of amplitude 2.60 mm. I fitted each
orbit's four strands against sin/cos(nθ) in the window θ ∈ [−40°, 60°], and the sorted phase steps
between strands give the measured per-turn drift δ.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| attn row L4 H3 q12, keys 0–12 | — (none) | .1142 .0583 .0313 .0139 .0050 .0060 .0105 .0625 .0151 .0522 .5572 .0618 .0119 (sum 1.000; keys 13–14 = 0, causal) | printed labels .114 .058 .031 .014 .005 .006 .011 .063 .015 .052 .557 .062 .012 | OK 13/13 |
| argmax key | — | 10 "transformer" | thick ring R=90 is the only one where the 4 strands share a phase (0.992/0.993/0.993/0.993) | OK |
| s* − s = ln(w*/w) (softmax identity, same query) | — | max gap 4.7097 ("drew") | — | OK |
| divisor 18.84 | — | 4 × 4.7097 = 18.839 → makes δ_max = 0.2500 exactly | caption prints 18.84 with no explanation | see mandate 1 |
| δ per key = gap/18.84 | — | The .084 · pen .120 · plot .153 · ter .196 · drew .250 · a .241 · black .211 · hole .116 · while .192 · the .126 · transformer .000 · watched .117 · itself .204 | measured strand steps .085 · .120 · .152 · .196 · .250 · .240 · .211 · .116 · .192 · .126 · .000 · .117 · .203 | OK, all within ±0.003 |
| κ integer on the resonant orbit | — | κ = n | fit κ = 35.00 on R=90 | OK |
| four turns each | — | 4 | 4 strands on every one of 13 orbits | OK |
| thirteen keys, one query | — | 13 causal keys at q12 | 13 orbits, 1 crimson sun | OK |
| s = q·k/8 | — | GPT-2 small d_head = 64 → √64 = 8 | caption | OK |
| amplitude (not a data channel) | — | constant | 2.58–2.61 mm on all rings (2.49 on clipped R=105 fit) | OK, no fake channel |
| head representativeness | — | L4H3 is **rank 1 of 144** heads for itself→transformer (next: L2H9 .416, L11H11 .379; mean over 144 heads .053). Only 6/144 heads put their argmax on "transformer". **106/144 put it on key 0 "The"** (the position-0 sink). | not disclosed | see mandate 3 |
| token strings | — | not verifiable (the npz holds no tokens, and no tokenizer is installed) | "plot"+"ter", 15 tokens | unverified |

## Lies list
| item | status |
|---|---|
| Printed weights differ from the npz row | clean (13/13 to 3 dp) |
| The drawn drift is not the stated formula | clean (phase steps match δ to ±0.003 on every ring) |
| Decorative marks posing as data (amplitude, lobe count) | clean: amplitude constant, n is an unlabelled integer carrier (~1 lobe per 15.7–16.2 mm of arc) |
| "an orbit closes only if it breathes a whole number of times per turn" | **VIOLATED**. The "drew" orbit (R=45, κ≈18.25) has 4δ = 1.000, so its 4-turn trace is a *closed* curve (4κ = 73 whole breaths). The divisor was set so the worst key closes. "a" (R=52.5) is at 4δ = 0.961, nearly closed. |
| "the resonant orbit closes" (the plate's thesis) | **VIOLATED on paper**. The R=90 "transformer" orbit is clipped by the left margin at x=10 (96° lost) and by the label knockout (15° lost). Only 69.2 % of it is drawn, so the one closing orbit is an open C. Rings R ≥ 60 all lose 11.5°–108.5°, and "itself" (the query's own orbit) keeps 66.5 %. |
| Resonant orbit drawn as a retrace | fudge (acceptable, but disclose it): the 4 turns of R=90 are offset radially by 0.25 mm (rmin 86.86/87.11/87.36/87.61) and ink as a 0.75 mm ribbon, not a true retrace |
| "what does itself refer to?" answered by the model | **VIOLATED (framing)**. Attention weight is not coreference. The head shown is the single most favourable of 144 and the sheet does not say so. The 2nd-tightest orbit, "The" .114 (R=15), is the position-0 attention sink, but the sheet presents it as the runner-up referent. |

## Scores
- truth: **7**. The data and mechanism are exact (every δ is right to 0.003). The caption's "only if" is false for "drew", the head is cherry-picked without disclosure, and attention is framed as reference resolution.
- encoding fidelity: **8**. Drift is linear in the logit gap and there are no decorative channels. But ink mass scales with R (token position), so low-attention outer orbits dominate the ink, and the one data-carrying closure is clipped.
- insight legibility: **7**. The thick ring on "transformer" answers the red question for a stranger. But the closure is never visible (the orbit is cut), "18.84" is an unexplained magic number that reads as ≈6π, and no misconception correction lands.
- **VERDICT: FAIL**

## Mandates
1. **Divisor makes the worst key close.** The sheet uses `kappa = n + (s*−s)/18.84`, and 18.84 = 4·ln(w*/w_min) = 18.839, so "drew" (ring R=45 mm) has δ = 0.2500 and its 4-turn trace closes (4κ = 73). That contradicts the caption line at y≈37. **Expected:** δ_max strictly below 1/4, e.g. δ_max = 0.20 → divisor 23.55 (= 5 × 4.710), so that no non-argmax orbit returns to its start within 4 turns. After that fix the least-closed orbit is "drew" at 4δ = 0.80. Also print what the constant is ("= 5 × the widest gap"), because 18.84 currently reads as 6π.
2. **The resonant orbit must be drawn closed.** Measured: the "transformer" orbit (R = 90 mm about (70.1, 171.9)) is only 69.2 % drawn, with 96° cut at the x=10 margin (y 101→237) and 15° under the label knockout. Every ring with R ≥ 60 is clipped, down to 66.5 % for "itself". **Expected:** 100 % of the R=90 orbit outside the label halo, and ≥ 95 % for every orbit. Recentre the sun and/or shrink the step (currently 7.5 mm) so that R_max + 2.76 mm fits inside the margins. For example, a sun at x=105 allows R_max + A ≤ 95, which needs a step of ≤ 7.0 mm with R0 = 15.
3. **Disclose the head selection and the sink.** Measured: L4H3's 0.557 on "transformer" is the maximum over all 144 heads (next 0.416 L2H9; head mean 0.053). Only 6/144 heads argmax on "transformer", while 106/144 argmax on key 0 "The". The sheet shows "The" .114 as the tightest non-resonant orbit (R=15) with no qualification. **Expected** in the black caption block (y≈33–40) and at the R=15 label: state that this is the strongest of 144 heads, that most heads park on "The", and that key 0 is the attention sink, not a candidate referent. Reword "what does itself refer to?" so it asks where *this head* looks, not what the model resolves.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | no `studio/orrery/LEDGER.md` exists; pass 1 only |
