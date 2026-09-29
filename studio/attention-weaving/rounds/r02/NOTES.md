# ATTENTION AS WEAVING — round r02

**Thesis: TRUE MECHANISM.** The weaving is the style; the numbers are the substance.
Every filament's path, every crossing's over/under, every bead's area and the whole
braid below the waist are computed from one real attention layer. Nothing on the
sheet is geometry pretending to be maths.

---

## Render

```
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r02/piece.py \
  --fn attention_weaving --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen \
  --out gallery/studio/attention_weaving/current/pp_attention_weaving_mechanism_v20.png
```

**Final render:** `gallery/studio/attention_weaving/current/pp_attention_weaving_mechanism_v20.png`
(+ `…v20.gcode`, provenance header written by `render_candidate.py`).

`--paper 24x30` was accepted (`PaperConfig.from_size` reads it as centimetres →
240 × 300 mm, ratio 0.800, exactly the reference). No fallback to A3 was needed.
Drawable area after the 10 mm margins is 220 × 280 mm.

## Pens (5 + cream paper)

| idx | pen | carries |
|---|---|---|
| 0 | black | title, reeds, softmax beads, dotted scaffold, mass rules |
| 1 | crimson | **Q** — token i as a query, above the waist |
| 2 | dodgerblue | **K** — token j as a key, above the waist |
| 3 | goldenrod | **V** — token j as a value, below the waist |
| 4 | darkgreen | **Z = AV** — token i's output, below the waist |

## Plot budget (post-pipeline, measured)

| | |
|---|---|
| pen-down | **20 273 mm** |
| travel | 20 296 mm |
| strokes (pen lifts) | 1 695 |
| commands | 37 595 |
| pen swaps | 4 (5 colour layers) |
| est. wall clock | **≈ 42 min** @ F1800 draw / F2600 rapid / 0.8 s per lift |
| per pen | black 1 957 · crimson 4 679 · dodgerblue 4 612 · goldenrod 6 146 · darkgreen 2 878 mm |

**Paper safety.** 34 783 inked 0.5 mm cells. 75.4 % take one pass, 21.0 % two,
3.0 % three, 0.60 % four or more, max 6 (3 cells). Nothing floods.
**Bounds:** piece bbox 10.00–230.00 × 10.67–282.96 mm — inside the drawable area,
**0 clamps** from `validate_bounds`. **Deterministic:** identical re-run at seed 7.

---

## The numbers — is the attention real?

### Source

`~/.promptplot/attn_gpt2.npz`, written 2026-09-12 by
`scripts/extract_gpt2_attention.py` (HuggingFace `gpt2`, CPU). Shape
`(12, 12, 15, 15)` = (layers, heads, tokens, tokens). Text = that script's default:

> "The pen plotter drew a black hole while the transformer watched itself think."

tokenised to 15 tokens: `The · pen · plot · ter · drew · a · black · hole · while ·
the · transformer · watched · itself · think · .`

Rows sum to **1.000000000** (min = max to 9 dp). The piece ships a numpy fallback
(`_numpy_attention`: real Q/K/V, real scaled dot product, real causal mask, real
softmax) that only runs if the cache is missing; the footer prints which one was used
(`gpt2-l2h9` on this render). Torch is not installed here, so nothing was downloaded.

### Which head, and why

**Layer 2, head 9.** It is a *coreference* head on this sentence, not a positional
or sink head, and its rows are peaked without being degenerate:

| query row | top keys |
|---|---|
| ` watched` | **transformer 0.764**, hole 0.100 |
| ` itself` | **transformer 0.416, watched 0.377**, itself 0.111 |
| ` think` | itself 0.388, watched 0.248, transformer 0.154 |

Selection was a sweep over all 144 heads on three measured criteria — attention-sink
mass on token 0 below 0.35 (l2h9 = 0.205), normalised row entropy in 0.35–0.85, and a
high spread of per-row entropy (l2h9 std 0.143). The near-uniform heads (l0h8, l0h2,
normalised entropy ≈ 0.93) and the degenerate ones (l4h11, entropy 0.003) were
rejected on those numbers, not by eye: a near-uniform head braids into mush, which is
the failure mode this piece was warned about.

**Query row q\* = 12, the token ` itself`.** The sentence is *the transformer watched
itself think*; the plate's waist is that word, and the head resolves it to
` transformer`. The plate is attention drawn by the thing it is about.

### 1 — the softmax waist is a real normalised row

`A[12, :]` in full, top to bottom of the bead column, bead AREA ∝ weight:

```
The 0.0257   pen 0.0008   plot 0.0012   ter 0.0009   drew 0.0030   a 0.0010
black 0.0097  hole 0.0201  while 0.0132  the 0.0206
transformer 0.4159   watched 0.3769   itself 0.1112
think 0.0000   . 0.0000      (causally masked -> drawn as empty rings)
SUM = 1.000000000      max = 0.4159      top-3 = 0.9040
normalised entropy H/log(13) = 0.536,  effective support exp(H) = 3.96 of 13
```

Peaked, with a long light tail — never a uniform stack. The two masked keys are the
only open rings in the column, so the causal mask is visible at the waist.

### 2 — which strands cross where, and which floats over

`log A` is decomposed by least squares over the 120 unmasked entries:

```
log A[i,j] = a_i + b_j + r[i,j]        R² of the additive part = 0.8185
a (query effects)  +1.486 … −3.382
b (key effects)    −3.381 … +1.549
r (residual)       −1.763 … +2.206,  mean|r| = 0.587,  50.0 % positive
```

* The **additive part** sets **WHERE**: `a_i` and `b_j` drive each filament's easing
  exponent `α_i = clip(exp(0.40·â_i))`, `β_j`, its reach past the waist axis and its
  peak height, so the crossing point of q_i and k_j is a deterministic function of
  `a_i` and `b_j` alone.
* The **residual** sets **HOW**: `sign(r[i,j])` decides which filament floats over at
  the crossing — 120 independent real decisions, split exactly 50/50.
* Together the two halves carry `log A` with nothing discarded.

Measured on the drawn geometry: **225 of 225 (i, j) pairs cross at least once**;
216 cross exactly once, 9 cross three times, 243 Q×K crossings in total. Distance of
each pair's deepest crossing from the waist against its weight:

```
Spearman(A[i,j], distance to waist) = +0.705
Pearson(log A[i,j], distance)       = +0.766
median distance, heaviest quartile 77.6 mm ; lightest quartile 56.0 mm
```

**Honest deviation from the brief.** The brief asked for heavy pairs to cross *near*
the waist. The built geometry does the opposite, strongly and monotonically: a heavy
query and a heavy key both reach furthest past the axis and peak highest, so a heavy
pair meets **high and wide** and a weak pair is squeezed down into the throat. I
tried the inversion (rounds v17/v19): flipping the reach ordering did **not** flip the
measured sign (it fell to +0.28 and +0.36 respectively, because the attention
deflection in §3 dominates the radial ordering) and it knotted the red bundle into a
tangle on the right. I kept the strong, clean encoding and am reporting its direction
rather than claiming the brief's.

A further 123 crossings lie in the **causally masked triangle** (`j > i`). Those have
no score at all, so they get their own rule — the key always floats over, the query
always ducks — which makes the causal mask a visibly different interlacing regime.

### 3 — the deflection is attention acting on the sheet

Over the open sheet each query filament is displaced from its lane by exactly how far
its attention-weighted mean of the *key* filaments' positions departs from the
**uniform-attention** mean over the same causal support:

```
Δy_i(x) = env(t) · Σ_j ( A[i,j] − u_i[j] ) · y_k=j(x),    u_i[j] = 1/(i+1) for j ≤ i
```

Key filaments get the transpose (column-normalised). One pass, computed off the
undeflected positions, so there is no circularity; `env` is zero at the reed and zero
at the funnel, and because it is a *deviation* a flat row runs straight while a peaked
row swings hard toward the key it has locked on. Soft-capped at 21 mm (tanh) and
7-point smoothed, with a soft ceiling below the title band.

### 4 — Z = AV is the real product

The rope's cross-section **is** the value matrix, rigidly rotating:

```
V_j = ρ_j·(cos φ_j, sin φ_j)      φ_j = 2π j/T                (token position)
                                  ρ_j = 0.55 + 0.45·rank_j/(T−1)
                                        rank by total attention mass received
Z   = A @ V                       |V| 0.550…1.000   |Z| 0.400…1.000
‖Z − Σ_j A[i,j]·V_j‖∞ = 1.11e−16   (exact to machine precision)
```

Because rotation is linear, the green filament i sits at `R(θ(t))·(AV)_i` at every
height — **literally at the attention-weighted mean of where the ochre filaments are,
measurable on the paper with a ruler.** Rows sum to 1, so every green strand is a
convex combination and lies inside the ochre sheath (verified: max|Z| ≤ max|V|).

How distributed a row is shows as how far its strand swings:

```
corr(|Z_i|, exp(−H_i)) = 0.835
effective support exp(H_i): 1.0 1.6 2.1 3.5 3.2 4.8 6.3 4.4 4.9 5.8 7.8 2.6 4.0 5.3 7.2
```

A peaked row (row 11, ` watched`, exp(H)=2.6) swings wide and tracks one ochre strand;
a flat row (row 10, ` transformer`, exp(H)=7.8) stays in the quiet core, braided
through many. The green cross-section is drawn at 0.62× the ochre scale so the two
families separate on paper — a stated uniform scale; the internal geometry of Z is the
exact product.

### 5 — other marks, all measured

* Left/right reed **lane widths** are proportional to real quantities (Q: the row's
  effective support; K: the mass that key receives) — the reed is irregular by
  measurement, not decoration.
* Filled red beads: each query's **heaviest real crossing**, diameter ∝ √A.
* Open blue rings: each key's heaviest real crossing.
* Black rings on the diagonal: the **self-attention crossing** q_i × k_i — the one
  crossing every token has — sized by A[i,i].
* Right-hand dotted rule: beads = mass each key receives across the sentence.
* Bottom dotted rule: beads = |Z_i|, the output magnitudes.
* Line weight: filaments in the top ~40 % by mass are drawn as 2 passes at 0.28 mm
  (one thicker line under a 0.5 mm pen).

---

## Strand accounting through the waist

A filament is a **token position**; its colour is the projection it is playing.

```
above:  15 crimson q_i  +  15 dodgerblue k_j   =  30
below:  15 darkgreen z_i +  15 goldenrod  v_j  =  30
```

`q_i → z_i` (same index: the output row index *is* the query row index) and
`k_j → v_j` (same token: key and value are two projections of one token). **30 in,
30 out**; nothing is born below the waist and nothing dies above it. V only appears as
V *after* the softmax, which is the order of operations `Z = AV` demands: Q and K meet
before, V only after. The ochre bundle turns at a **selvage peg** on the left margin —
the reference's left-hand reed read as the point where the value threads turn, which
is what a reed does in a real loom.

## How over/under is implemented

Two steps, both exact, both in `piece.py` (nothing under `promptplot/` was touched):

1. **`_crossings(strands)`** — every pairwise crossing found in closed form
   (segment–segment determinant, parameters `t, u ∈ [0,1]`), bucketed through a 5 mm
   spatial hash. No sampling, no tolerance fudge.
2. **`_cut_runs(pts, cuts, r)`** — the losing filament is split with the engine's
   exact clipper: a `geometry.Union` of `geometry.Circle(px, py, gap/2)` around the
   crossing points, and `Circle.inside_intervals` + `geometry._complement` give the
   kept parameter intervals per segment. A cut curve therefore stops **exactly on the
   circle**, never at a sampled vertex — this is `geometry.clip`'s interval algebra,
   applied segment-local so it stays fast at ~30 filaments × 300+ samples.

Who loses is always data:

| crossing | decided by |
|---|---|
| q_i × k_j, unmasked | `sign(r[i,j])` — the residual of `log A` |
| q_i × k_j, masked (j > i) | the key always over, the query ducks (the mask made visible) |
| q_i × q_k | `a_i` vs `a_k` |
| k_j × k_l | `b_j` vs `b_l` |
| anything in the rope | the real out-of-plane coordinate `w` of `R(θ(t))·V_j` / `·Z_i` — true 3-D occlusion of a twisted rope, not a pattern |

Gaps: 2.05 mm in the weave, 1.25 mm in the rope. The engine's `occlude_crossings`
was **not** used: it only ever cuts between *different* pens, and this piece needs
same-pen (Q×Q, V×V) occlusion too, and needs the winner chosen by the data rather
than by draw order or alternating parity.

---

## Round log

| v | change | why |
|---|---|---|
| v1 | first geometry: full Q/K swap, parallel throat, rope with rotating V/Z cross-section | baseline |
| v2 | pinch (hourglass) replaced the parallel throat; vertical spread at the hand-over; slots ordered by rope phase | v1's throat was 15 lines in 4.8 mm — a solid ink slab, unplottable |
| v3 | flat launch off the reed (`x^α`, α<1; `y^γ`, γ>1); shorter overshoot; selvage peg | v2's strands left the reed vertically and the funnel formed two parallelogram slabs |
| v4 | **cone rule**: peak height tied to reach (`y_pk = yw + 12 + 1.34·reach`) | v3 still hairpinned — a far-reaching strand with no height to turn in ran horizontally |
| v5–v7 | γ capped; per-strand peak scatter; tangent-continuous V rejoin; margin inset; data punctuation | corner artefacts, 171 bounds clamps |
| v8–v9 | reed lanes sized by real quantities; bead contrast; label moves | mechanical even reeds; beads read as uniform dots |
| **v10–v12** | **attention as the deflection** — first as a pull toward the weighted mean (collapsed the bundle onto one line), then as the **deviation from uniform attention**, soft-capped and smoothed | the lens was two laminar fans grazing; this is what made it a weave |
| v14–v16 | opened the lens (reach 10–44 mm, cone 1.34); causal-diagonal rings; soft ceiling under the title | crossings were compressed into a 40 mm band; a hard ceiling stacked threads onto one ruled line |
| v17 / v19 | tried inverting the reach so heavy pairs cross *near* the waist | it knotted the red bundle and the measured Spearman only went to +0.28 / +0.36 — rejected, reported |
| **v20** | v19's wider lens + the original (non-inverted) reach; code claims corrected to match measurement | final: ρ = +0.705, 243 crossings, clean composition, 0 clamps |

## Known deviations from the brief

1. **15 filaments per bundle, not 18–24.** T is the sentence's real token count. I
   would only get 20 by using the uncaptioned 46-token extraction whose source text is
   not recoverable, and provenance is the whole point of this round.
2. **The waist is ~36 mm wide**, not the reference's ~4 % of the sheet. 30 filaments
   through a 9 mm throat is 0.3 mm pitch — under the pen tip. At 36 mm the pitch is
   0.97 mm and the constriction still reads (the weave above is 220 mm wide, a 6:1
   pinch). The bead column sits in a clear 8.8 mm channel between the two ribbons.
3. **Crossing distance runs the other way** — see §2 above, measured and reported.
4. The Q·Kᵀ lens is still the piece's softest zone; see the critique below.

## Self-critique — weakest part

The **Q·Kᵀ lens**. It is the thesis and it is the least resolved region. The two
bundles cross at a shallow angle over a wide, fairly flat band rather than in the
reference's big turbulent diamond, so at three metres the plate reads as *two fans
meeting* before it reads as *one cloth*. The over/under is real and visible up close —
the colour swap through the lens (crimson exits right of the waist axis, dodgerblue
left) is the clearest possible proof the bundles genuinely interpenetrated — but the
interlacing does not yet dominate the way `bauhaus_loom`'s does, because 15 + 15
smooth filaments simply cannot produce the reference's density. Second-weakest: the
bottom `|Z|` rule still reads as generic drafting furniture rather than as data,
despite its beads being real output magnitudes.
