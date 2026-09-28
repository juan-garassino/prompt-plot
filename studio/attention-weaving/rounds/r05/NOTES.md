# attention-weaving r05 — area-smooth (mechanism) · parent: r03 · 2026-09-28

## Render

```bash
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r05/piece.py \
  --fn attention_weaving_area_smooth --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen \
  --out ~/Downloads/pp_attention_weaving_area-smooth_v7.png
```

- final PNG: `~/Downloads/pp_attention_weaving_area-smooth_v7.png`
- final GCODE: `~/Downloads/pp_attention_weaving_area-smooth_v7.gcode`
- seed 7. The geometry does **not depend on the seed**: nothing is random any more (the
  numbers are GPT-2's). Seed 3 gives a byte-identical body, only the header differs. `rng`
  is used only by the numpy fallback if `~/.promptplot/attn_gpt2.npz` is missing.
- trail: v1 (first histopolant, spike on the left jamb from linear extrapolation) → v2
  (clamped ends: flat shelves at both jambs, clump pitch 0.95 → 1.50 mm) → v3 (end knots on the
  jambs, natural: the right side lands clean, but the left became a needle) → v4 (left end
  level g'=0, right natural) → v5 (top-3 key labels stacked; v4's single line ran off the
  sheet) → v6 (crumb filter, label halo 1.8 mm) → **v7** (hill 0.082 H → 0.100 H).

## Mandate responses

There is no `LEDGER.md` for this slug. The open mandates are Juan's REWORK note (J1, J2) and
the Weak list in `DESCRIPTION.md` for aperture v19 (D1–D6).

| id | mandate | status |
|---|---|---|
| J1 | "the black softmax staircase should be SMOOTHER … keep the partition exact (sums to one)" | **FIXED.** The profile is now one C² curve with no flat tops and no knot discs. Exactness moved from knot height to **area**: the trapezoid area of the drawn polyline over each clump's span equals a_j with a max error of 1.1e-16. The cumulative is the running integral of that same polyline and hits every partial sum at every clump boundary (max err 8.9e-16), ending at 1.000. |
| J2 | "the TOP half looks much better than the BOTTOM — bring the bottom up to the top" | **DEFERRED** to the mirror-drain thesis, which a sibling round is building now. This thesis is the softmax. What I did change in the bottom: the lane tangle is gone (D2), and the V over/under is real data instead of seeded vectors. The bottom is still two families of near-parallel lines and still has the 80 mm run-out. |
| D1 | [craft] profile reads as a staircase with ~12 knot discs | **FIXED** (see J1). Knot discs removed. The partition is shown only as a ruler: 12 black ticks hanging under the hole's baseline, each in the gap between two clumps. |
| D2 | [craft] tangle of chevrons at the cable's bend (0.58–0.67, 0.50–0.58) | **FIXED.** Cause: r03 built the lane normals from the chord between spine knots, so the normal jumped at every knot. r05 uses the Catmull-Rom analytic tangent, so the normals are continuous. Measured: 0 crossings between adjacent lanes over all 27 pairs. |
| D3 | [grid] footer leading uneven; SOFTMAX label away from the profile; cumulative unlabelled | **FIXED.** One leading for all four footer lines (0.026 H). `SOFTMAX` sits against the right jamb, 3.4 mm from the hill. The cumulative ends on a disc labelled `1.000`. The three heaviest keys are named under the wall's right arm. Every label has a halo that clips strands and scaffold. |
| D4 | [concept] φ < 0 half of the coordinate system not drawn | **DEFERRED** to mirror-drain (sibling round). |
| D5 | [space] lower-left void is leftover space, not a shaped one | **DEFERRED**, same reason. The composition below the wall is unchanged. |
| D6 | [hierarchy] bottom does not match the top | Same as J2: **DEFERRED**. |

## What changed from parent

1. **The numbers are real, and every field on the sheet comes from one row.** r03 drew random
   seeded Q/K/V with a temperature solved to a target a_max. r05 reads GPT-2 small, layer 2,
   head 9 (the r02 cache) on "The pen plotter drew a black hole while the transformer watched
   itself think." The slit holds the row of the query ` itself` (q* = 12) over the 13 keys that
   query can see, **in sentence order with no permutation**. Queries are the 15 tokens and keys
   are the 13 visible ones, so N = 28 filaments go in and 28 come out.
2. **The softmax is a histopolant, not an interpolant.** Width still carries the *quantised*
   weight (p_j filaments). **Area** now carries the *exact* weight, so the height is a density
   and the silhouette is a single hill:
   - A tooth at the left jamb for `The`, GPT-2's first-token attention sink.
   - A low, rippled tail. The small bump is `black / hole / while / the`.
   - One broad hill over `transformer | watched`, with its peak over `transformer`.
   - A shoulder down to `itself`, which meets the right jamb.

   The right jamb is where the causal mask starts: tokens 13 and 14 cannot be attended to.
3. **The causal mask shows up in the geometry.** Keys and queries both land in sentence order,
   and every K spiral sweeps in from the right. So a key only ever crosses the queries that come
   after it in the sentence, i.e. the ones allowed to see it. **None of the 78 masked pairs cross
   anywhere on the sheet.** The footer says `NONE MASKED`. The code has a wider-gap "hidden key"
   branch for masked crossings, but it never fires.
4. **Over/under is real data in both weaves.** For Q×K the sign comes from the centred
   log-attention, c_ij = log A_ij − mean_{k≤i} log A_ik. Softmax is shift-invariant, so this is
   exactly the scaled score minus its row mean. For V×lane, gold goes over a lane of clump k iff
   a_j ≥ a_k, so the heavier value rides on top.
5. Clump pitch went from 0.95 to 1.50 mm. The heavy clumps got wider, so the hill is wide rather
   than a needle, and the plotting floor has more margin.
6. Craft: crumbs shorter than 0.9 mm left by crossing gaps are dropped, dotted crumbs under
   0.6 mm are dropped, and labels have halos.

## Measurements / computations

All values come from `piece.LAST_STATS`, recomputed on every call.

| claim | measured |
|---|---|
| source | GPT-2 small L2 H9, row ` itself`, keys 0–12 |
| row a_j | The .025657 · pen .000762 · plot .001165 · ter .000854 · drew .003034 · a .000963 · black .009723 · hole .020061 · while .013228 · the .020580 · **transformer .415891** · **watched .376887** · itself .111196 |
| Σa (float64 after renormalising the float32 cache) | 1.0000000000000002 → printed `Σa = 1.000000000` |
| entropy | H = 1.984 of log2 13 = 3.700 bits |
| filaments per clump p_j | [2,1,1,1,1,1,1,1,1,1,7,7,3], Σ = 28 = 15 Q + 13 K |
| partition tiles the slit | 51.920 of 51.920 mm |
| **per-clump area error of the drawn hill** | max 1.1e-16 (Newton on the 13 knot values of g, trapezoid on the plotted vertices) |
| hill area | 568.63 mm² ≡ 1.000 (transformer 236.49 mm² = 0.415891 × 568.63) |
| cumulative at clump boundaries vs exact partial sums | max err 8.9e-16; end = 0.9999999999999993 |
| density floor | f_min / f_max = 0.0055 (strictly positive by construction, f = exp g) |
| peak position | u = 0.457 (over `transformer`) |
| Q·Kᵀ crossings on the sheet | 58 of 195 pairs; 0 of the 78 masked pairs cross |
| V × lane crossings | 140, gold over in 97 |
| lane-lane crossings in the cable | 0 (r03 had the chevron tangle) |
| min lane pitch | 1.50 mm (floor 0.8) |

**The histopolant.** f(x) = exp(g(x)), where g is a cubic spline with one knot per clump.
Interior knots sit at the clump centres and the two end knots sit on the jambs. The left end
has g′ = 0 so the sink rises level instead of as a needle; the right end is natural. The grid
includes every clump edge, so each bin's area is the area of the polyline that is actually
plotted. The 13 equations ∫_bin f = a_j are solved by damped Newton with the analytic Jacobian
∫_bin f·φ_k.

## Plot budget

- draw **15.63 m** · travel 16.25 m · **17,302 commands** · 859 pen lifts · 5 pens (4 swaps)
- parent v19: draw 19.55 m / travel 20.23 m / 24,329 commands. r05 has 10 fewer filaments,
  so it is about 20% lighter.
- estimated time 869 s at the file's feeds. On Leo at F600 with 1 s dwells, expect roughly 1.5–2 h.
- bbox X 10.62–229.70, Y 12.41–289.70: inside the 10 mm margin, 0 bounds violations.
- `preview --score` grade: A.

## Self-critique (rubric, 1–5)

- **Concept 4.** The softmax now makes two exact claims at once: filaments are the quantised
  weight and area is the exact weight. The mask is visible twice, as the right jamb and as the
  absence of masked crossings. The attention sink is visible as the left tooth.
- **Hierarchy 3.** The hill is bigger (0.10 H) but it is still a small object inside a big
  storm. The giant title still outweighs it.
- **Craft 4.** No staircase, no discs, no chevrons, no crumbs, labels with halos. The left tooth
  can read as a glitch until you know it is the sink.
- **Grid 4.** The footer is regular and the labels hug the slit.
- **Space 3.** Unchanged from parent: the L-shaped void and the green run-out.
- **Tension/asymmetry 3.** The hill now leans right. The bottom still lies flat.
- **Top/bottom parity 2.** Juan's note 2 is still open.
- **The single worst thing:** the bottom half. It is still 13 near-parallel gold arcs meeting a
  near-parallel green cable, followed by 80 mm of green with nothing happening in it. That is
  exactly what Juan flagged, and this round did not address it.

Second: the top storm is sparser than v19 (15 Q + 13 K against 22 + 16) because the real
sentence has 15 tokens. The upper-left has only 3 crimson streamlines. The storm keeps its
character but not its density.

## Engine requests

1. `geometry.intersections(poly_a, poly_b)`: still hand-rolled here as `_crossings` (same as r03).
2. `kit.dash` / minimum-run filter after `clip`: every over/under piece needs to drop crumbs
   shorter than the pen tip.
3. A histopolation primitive (`material.histopolant(edges, areas)` → an area-exact positive
   smooth profile). Any "the distribution sums to one" plate could use it.
