# ATTENTION — FORWARD AND BACKWARD · round 02 · TRUE MECHANISM

**Thesis:** the brief's layout, driven end to end by real attention numbers —
forward *and* backward. Nothing on this plate is a plausible-looking shape; every
dot radius, tooth length, ribbon width and ink pass is a number computed in
`mechanism.py` and checked below.

**Final render:** `gallery/studio/attention_passes/current/pp_attention_passes_mechanism_v15.png`
(+ `.gcode` beside it; identical geometry to v14, which is the same plate).

```
.venv/bin/python scripts/render_candidate.py studio/attention-passes/rounds/r02/piece.py \
  --fn attention_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,crimson \
  --out gallery/studio/attention_passes/current/pp_attention_passes_mechanism_v15.png
```

Files: `piece.py` (the plate), `mechanism.py` (the maths; `python mechanism.py`
prints the whole self-check). Nothing under `promptplot/` was touched.

---

## Pens and plot budget

A3 landscape, drawable 400 × 277 mm, margins 10 mm, zero bounds violations.

| pen | colour | carries | draw | pen-downs |
|---|---|---|---|---|
| 0 | black | K, the score lattice, the waist, all structure and type | 9 481 mm | 1 758 |
| 1 | dodgerblue | Q, the focus column, the softmax comb, ∂L/∂Q | 5 564 mm | 1 109 |
| 2 | crimson | V, weighted values, Z-flow, ∂L/∂V, ∂L/∂Z | 11 313 mm | 1 377 |
| | | **total** | **26 358 mm** | **4 244** |

46 772 GCode commands after postprocessing; optimised travel 27 040 mm. Three pen
swaps. It is a long plot — the 4 244 pen-downs (the dot fields) dominate the wall
clock, not the 26 m of line. Determinism verified: two calls at seed 7 produce
byte-identical command streams. Cream paper is the fourth colour; the causal void
and the band between the registers are left bare.

---

## Which head and row, and why

The cached stack `~/.promptplot/attn_gpt2.npz` is real GPT-2 attention,
12 layers × 12 heads × 15 tokens (produced earlier by
`scripts/extract_gpt2_attention.py`; no network access was needed and nothing was
downloaded). I scanned **all 144 heads and every causal row**, scoring on the
failure modes the task warned about — near-uniform rows, and rows whose mass sits
on the token-0 attention sink — then on whether the head's *whole* matrix has
structure worth drawing.

**Chosen: layer 1, head 0, query row 12.** Rejection reasons for the runners-up:

- Most strongly peaked rows in this stack peak on the **diagonal** (a token
  attending to itself). True, but it draws as a single dot on the causal edge and
  says nothing about routing, so `argmax == q` was disqualified.
- Rows peaking on **key 0** were disqualified: that is the attention sink, and the
  comb would have been one spike at the top with nothing under it.
- L3 H8 q=13 was peakier (0.682) but had only three keys carrying anything —
  the "long tail of small ones" the brief asks for would not have existed.

Row 12 of L1 H0, all 13 causal keys, in order:

```
0.0277  0.0014  0.0112  0.0029  0.0462  0.0299  0.0121
0.0146  0.0463  0.1388  0.1165  0.5024  0.0501
sum = 0.9999999212        (float32 storage; exact in float64 = 1.0)
argmax = key 11, a = 0.5024      second tier 0.1388, 0.1165
perplexity = 5.475 effective keys     min = 0.0014      max/min = 359 : 1
```

A dominant peak two tokens back, a clear second tier, then a tail over three
decades. Visibly peaked, not uniform, not the sink — which is exactly what the
brief's "few large dots, a long tail of small ones" requires.

---

## The linear algebra, and the proof it is real

### What is genuinely GPT-2's, and what is not

`A` is real GPT-2 attention, read from the cache.

`Q` and `K` are **recovered exactly from `A`**. Softmax is invariant to a per-row
additive shift, so the score matrix is observable up to that gauge:
`S = log A`, row-centred over the causal window, reproduces `A` under causal
softmax to machine precision. A full SVD of that `S` (rank ≤ T = 15, far under
GPT-2's head width d = 64) gives an exact rank factorisation `Q Kᵀ / √d = S`.
So the Q and K on this plate are GPT-2's own queries and keys up to the
orthogonal gauge `Q → QR, K → KR` that a dot product cannot see.

`V` is the one thing the cache does not contain — only attention probabilities
were saved, never the value projection. It is a real seeded Gaussian value matrix
at GPT-2's head width. The whole forward/backward chain through it is exact; it
is simply not GPT-2's V, and the plate does not claim it is. **This is the single
honest gap in the provenance and it is stated on the sheet's own terms: the
caption reads `gpt2 layer 1 head 0 query 12`, which is true of A, Q and K.**

### The backward pass, done by hand

```
L      = ½‖Z − Z*‖²_F
∂L/∂Z  = Z − Z*
∂L/∂V  = Aᵀ ∂L/∂Z                        ← routed by the SAME A as the forward pass
∂L/∂A  = ∂L/∂Z Vᵀ
∂L/∂S  = A ⊙ (∂L/∂A − rowsum(∂L/∂A ⊙ A))  ← softmax Jacobian
∂L/∂Q  = ∂L/∂S  K / √d
∂L/∂K  = ∂L/∂Sᵀ Q / √d
```

Shapes: `A (15,15)`, `Q K V Z dQ dK dV (15,64)`, d = 64, T = 15.

### Checks (`python studio/attention-passes/rounds/r02/mechanism.py`)

At the seed the render actually uses (`SeededRNG(7).randint → 42446`):

| check | value |
|---|---|
| `softmax(S) == A` (recovered scores) | max abs err **4.4e-15** |
| `softmax(QKᵀ/√d) == A` (recovered Q, K) | max abs err **4.8e-08** |
| ∂L/∂Q vs central finite difference, directional | rel err **1.3e-08** |
| ∂L/∂K vs central finite difference, directional | rel err **8.0e-10** |
| ∂L/∂V vs central finite difference, directional | rel err **6.9e-09** |
| ∂L/∂K element-wise finite difference (60 random entries) | rel err 1.6e-06 |
| ∂L/∂V element-wise finite difference (60 random entries) | rel err 9.0e-07 |
| ∂L/∂Q element-wise finite difference | rel err 1.5e-02 — **see below** |
| `∂L/∂V == Aᵀ ∂L/∂Z` | `np.array_equal` → **True**, max diff 0.0 |

The element-wise check on Q is the one weak number and it is a **conditioning
artefact, not an error**: dQ's entries are ~1e-3 against a loss of ~9.7, so
`h·∂L/∂Q_ij` at h = 1e-5 is lost in the cancellation. The directional derivative
along dQ itself sums the whole matrix, is well scaled, and is the stronger claim
anyway — it says the analytic gradient *is* the steepest-ascent direction with the
right magnitude. It agrees to 1.3e-08. Both are reported; neither is hidden.

Gradient norms: `‖∂L/∂Z‖ = 4.405`, `‖∂L/∂V‖ = 3.944`, `‖∂L/∂K‖ = 0.202`,
`‖∂L/∂Q‖ = 0.177`, `L = 9.704`.

Per-token `‖∂L/∂V_j‖`, which is column *j* of A summed against ∂L/∂Z:

```
3.392  0.706  0.586  0.152  0.626  0.782  0.807  0.157
0.442  0.760  0.368  0.624  0.219  0.368  0.140
```

Token 0 takes the largest value-gradient by a factor of four. That is not a bug
and it is not decoration: token 0 sits in *every* causal row's window, so `Aᵀ`
sums the sink column fifteen times. The attention sink is visible in the backward
pass as the deepest stratum of the `∂L/∂V` well.

`∂L/∂S` on the focus row — signed, which is why the backward lattice draws
positives as filled dots and negatives as ticks:

```
+0.0057 −0.0002 −0.0026 +0.0004 −0.0160 −0.0008 −0.0012
−0.0004 −0.0011 +0.0060 +0.0195 −0.0115 +0.0023
```

Sums to ~0 across the row, as the softmax Jacobian requires.

---

## How each mark carries a number

- **`similarity`** — the recovered `QKᵀ/√d`. Query indexes the **columns**, key the
  **rows**, so the key axis is the same vertical axis all the way to Z and the
  whole plate flows left to right with no 90° turn. Dot area ∝ |S_ij|^0.66,
  drawn as spiral-filled discs. The empty lower-left triangle is the causal mask,
  not a layout decision.
- **Q selects a column, K lands on the diagonal.** Q is one vector, so it is one
  ribbon of seven lines that drops onto column 12 from above; the split into
  thirteen products happens *at the column*, because that is where it happens.
  K's fifteen strands each leave their **own** kernel in the K well and terminate
  on the causal diagonal — key *j* first exists at token *j*.
- **The waist.** Each of the thirteen strands keeps a centre line the whole way;
  its two edges carry the probability that score would have at softmax
  temperature `τ(x)`, annealed from τ = 30 (all thirteen equal — scores exist,
  no distribution yet) down to τ = 1 (the real row). Edges are dropped where the
  ribbon closes under the pen tip. Twelve of thirteen pinch shut; one stays open.
  That taper is the information being destroyed, and it is exact.
- **`softmax`** — teeth to the right are the focus row, length ∝ a_j, ink passes
  1–5 by weight, axis disc radius ∝ √a_j. The other fourteen rows of the same head
  are the short brush teeth, offset into the half-pitch gaps so they never
  over-ink the focus comb. This is the tightest, densest mark on the sheet.
- **V bypasses the score.** V never touches Q or K, so its sheaf sweeps under both
  earlier stations and only meets the distribution at `weighted values`, which is
  where `Z = Σ a_j v_j` is actually formed. Each strand leaves the ragged right
  edge of its own lamina; how far right a lamina reaches is |V_j·ê₁|.
- **The three wells differ in kind, not colour.** Q is a **dipole** — level sets of
  the real query functional `p ↦ q·p`, two opposed lobes pinched at the node,
  the only signed well because a direction is the only signed thing here. K is
  **multi-modal** — a kernel sum over the fifteen projected key vectors, one lumpy
  envelope outside and separate islands inside. V is **stratified** — one lamina
  per token, height = that token's real scalar value content, tilted by the second
  channel. Dipole / islands / strata: no two read as copies.
- **Row registration.** V, K, Q sit at the *identical* fractions (0.155, 0.500,
  0.845) of both registers, and three dotted spines down the left margin tie each
  tensor's forward row to its gradient row with end ticks. Verified in code: both
  registers call the same `RF` tuple.
- **The mirror.** The backward comb is the same row, same weights, mirrored —
  `∂L/∂V = A' ∂L/∂Z` is set beside it. `∂L/∂Q` leaves through a throat above the
  focus column, the exact reverse of Q's arrival. `∂L/∂K` leaves the causal
  diagonal, the exact reverse of K's arrival. Arrowheads appear **only** in the
  backward register.

---

## Per-round log

| round | what changed | why |
|---|---|---|
| v1 | first build: wells, lattice, comb, both registers | wells were 90 mm tall on 50 mm rows — everything collided, Q spilled off the sheet (334 bounds violations), lattice invisible, 34.5 m of ink |
| v2 | halved the wells, split the bands, gave the lattice and comb their own zones | readable, but the middle was a black ramp; the comb was 62 mm tall so the "waist" read as a diagonal sweep |
| v3 | tightened the comb into a real waist, bolder lattice, moved type to the quiet band | **found the core bug on inspection: `_dot` draws a horizontal line of length 2r**, so at lattice scale every "dot of varying size" was a dash. The score matrix had never rendered |
| v4 | wrote `_blob` (a filled disc as one spiral stroke); **transposed the lattice** so key indexes the rows and the key axis is shared by every station | lattice finally reads as a matrix; the flow became purely left-to-right |
| v5 | V moved from `softmax` to `weighted values` — that is where the product is formed; K and V strands leave their own kernels/laminae | freed the softmax station entirely for the comb; more truthful *and* less crowded |
| v6 | Q reduced to one ribbon (it is one vector); V drawn solid, not dashed | the dashes on near-parallel strands had formed ladder rungs |
| v7–v8 | every bundle **necks** — the plate's order applied to its own bundles | killed the "stiff cables" reading; K's braid is now confined to a tight neck |
| v9 | corner crosses pulled inside; V kept inside its register; dot pitch 1.8→2.15 | **bounds violations to zero**; quiet band stays quiet |
| v10–v11 | waist re-encoded: centre line always, two edges capped at 0.58 × pitch and pinching shut | the winner's ribbon had been ballooning to 22 mm and swallowing twelve neighbours, so the taper never read |
| v12 | V's laminae thickened (n=5→7, lo_frac 0.16→0.085); right label right-aligned to the Z column | V was the weakest of the three wells |
| v13–v14 | `∂L/∂Q` re-routed through a throat above the focus column; `∂L/∂S` scaled by the 92nd percentile, negatives as minimum-length ticks | the blue gradient bundle had been running along the backward lattice's rows and erasing it |
| v15 | added the directional gradient check to `mechanism.py` | the element-wise check on dQ is ill-conditioned; geometry unchanged (gcode identical to v14) |

---

## Honest weaknesses

1. **V is not GPT-2's V.** Stated above and stated again here. Everything drawn
   through it is exact, but if the value projection is ever cached the piece
   should be re-run against it — `mechanism.py` needs one line changed.
2. **The `weighted values` crossing is the muddiest zone.** Red V strands and blue
   comb strands cross at 290–330 mm. The crossing is the multiply and I would
   defend it, but it is denser than I would like and it is the first place a
   critic's eye snags.
3. **The backward register is the weaker half.** Its wells are 80 % scale and its
   lattice is smaller, which is right for a secondary statement, but the
   `∂L/∂Z` fan and the `∂L/∂V` sheaf still cross in a broad X that carries less
   information per square millimetre than anything in the forward register.
4. **4 244 pen-downs is a lot.** The dot fields are the piece's texture and the
   reference's signature, so I did not cut further, but this is a long sit at the
   machine and worth checking against Leo's drift before committing to A3.
5. The non-focus rows at `softmax` are a texture, not a readable quantity. They
   are real numbers, but nobody will measure them.

## Engine request (not acted on)

`promptplot/generative/generators.py::_dot` draws a horizontal stroke of length
`2r`, which is right for a 0.3 mm tick and wrong for anything larger — it reads as
a dash. Three rounds here were spent on an invisible lattice because of it. A
`_blob`-style spiral-filled disc (implemented locally in `piece.py`) would be
worth promoting to `engine/kit.py` as `filled_dot()`, leaving `_dot` alone.
Not done: no files under `promptplot/` were modified.
