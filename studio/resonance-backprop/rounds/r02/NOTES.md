# resonance-backprop r02 — the fold · parent: r01 · 2026-09-28

Abstract thesis ("the fold", DESCRIPTION.md § Next versions 1). The mirror is the whole plate.
Above one horizontal line is the forward pass: Q and K as two coherent point sources, each drawn
as its own family of Huygens crest circles. Below it is the backward pass: the two gradients,
radiating from the sources' mirror images. There is one green line across the sheet (Z, where the
loss is read), four goldenrod beads strung on it (V: the attention weights), and the left rail with
its two words. No packets, fractions, arrows, labels or title.

**The twist is the colours.** Below the line crimson and blue have changed places, because that is
what the gradient of a resonance does. If s = Re(q·conj k), then ∂L/∂q = C·k and
∂L/∂k = conj(C)·q. The gradient that arrives at Q is K's wave, and the gradient that arrives at K is
Q's wave, conjugated. So the source under Q radiates BLUE and the source under K radiates CRIMSON:
colour says whose wave it is, position says whose gradient it is.

**Lineage.** Sol LeWitt, *Arcs, Circles & Grids* (1972), conceptual art. From it the plate takes its
ORDER, not its look: families of concentric arcs from fixed points, superimposed by one stated
rule, running out to the wall's edge. The rule here is the chain rule: reflect, swap, conjugate. The
sentence redraws the plate: "From Q and K draw crest circles every λ out to the reach; reflect both
points in the line; from Q's image draw K's circles, turned by arg C, and from K's image draw Q's,
turned by −arg C." This is deliberately not Young's 1807 plate, which is the lineage of the sibling
benchmark (resonance r05).

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance-backprop/rounds/r02/piece.py \
  --fn resonance_the_fold --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,crimson,forestgreen,black \
  --out gallery/studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.png
```

- final: `gallery/studio/resonance_backprop/trials/pp_resonance_backprop_the-fold_v5.png` + `.gcode` (seed 7, A4 portrait, cream)
- **Seed-independent.** Every mark is computed and none is sampled. Seed 11 was rendered as v6 and
  its G-code body is byte-identical to v5 (md5 `917e29ec…`).
- Trials: v1 (level pair, 2×2 grid of bullseyes, too symmetric), v2 (tilted pair, the chevron),
  v3 (amplitude-weighted passes), v4 (fold chained into one stroke, bead threshold), v5 (bead gap,
  rail type weight). v7 is a re-render after a docstring-only edit, and its body is byte-identical to
  v5.

## Mandate responses

`studio/resonance-backprop/` has no LEDGER.md and no FEEDBACK.md, so there are **no open J*, A* or
S\* rows**. The work order was the curator note plus the DESCRIPTION brief and its Weak list:

| id | mandate | status |
|---|---|---|
| C1 | keep the family grammar: Q crimson / K blue, the two-source interference field, V goldenrod, Z green | FIXED. The approved crest-locus construction (r = mλ, d = Nλ whole wavelengths, `_Guard` 0.82 mm / 25°) is kept. Q is crimson and K is blue, and the gradients keep the colour of the wave they ARE. V is goldenrod (the beads) and Z is green (the fold). The Q/K wave packets are not drawn: the brief deletes them. They survive as the sources, because each source's phasor is its packet's Fourier coefficient at the resonant carrier (the family fold, as in resonance r04), re-derived from THIS plate's r01 packets |
| C2 | no pen cap, each pen one clean layer, stated order | FIXED. 5 pens and 5 meanings, each one layer, never re-entered. Order light → dark = palette index: goldenrod, blue, crimson, green, black. Goldenrod goes first so the green fold lands over the beads (beads strung on the line). Black goes last so the rail crosses the fold's end on top |
| C3 | strokes spatially ordered for batching | FIXED. Per layer, nearest-neighbour with reversal (`_order`). Neighbouring rings are walked outward, so the whole blue or crimson layer is two spatial sweeps (upper half, then lower half) with ONE sheet-crossing jump each: 267 mm blue, 149 mm crimson. The longest stroke is the fold (556 mm, 67 s at F500), then 345 mm full rings (41 s). Every stroke is a clean batch boundary |
| C4 | minutes per layer + total | FIXED, table in Plot budget |
| C5 | waste: 4,053 pen cycles and 105 % travel, mostly dotted arcs and leaders | FIXED. **334 pen cycles (−92 %). Travel 2.60 m = 11 % of draw (was 105 %).** No dotted run exists on the sheet. Line weight is built by chaining extra passes into the SAME pen-down (costs draw, never a cycle). Only 5 strokes are under 1.2 mm, all glyph parts |
| C6 | name the lineage | FIXED: LeWitt, *Arcs, Circles & Grids* (above) |
| B1 | the fold: one field above, its exact inverted twin below, meeting at one horizontal loss line; delete packets, fractions, arrows; the rail the only type | FIXED. "Inverted" turns out to be literally true: arg C = 150°, so the gradient field is 30° short of a pure sign flip (numbers below). Rail words are the only type |
| W1 | [concept] schematic, only the hero is an order | FIXED. There are no stages, arrows or labels. The order is INTERFERING + a reflection, and the reflection is the mechanism (adjoint), not a layout habit |
| W2 | [craft] packet rows interpenetrate into knots | FIXED by deletion (no packet rows) |
| W3 | [craft] the central comb is a near-solid black lozenge | FIXED. Pitch is 3.0 mm and nothing floods. Along each Q–K axis, where the two families' crests coincide within 0.1 mm, the guard keeps one family per crossing, which leaves a seam of short dashes |
| W4 | [hierarchy] Z axis wider than the hero | FIXED. The field IS the sheet. The fold is the one full-width line, and it is the spine |
| W5 | [tension] mirror-symmetric about u 0.50 | FIXED. The fold's own symmetry is kept (it is the mechanism), but the pair runs on a 36° diagonal. The plate is a "<" chevron with its apex on the rail, the two big discs bleed off the top, bottom and right, and there is no left-right symmetry |
| W6 | [space] dead foot, arrow thicket | PARTLY. The foot is gone (the lower field bleeds off the bottom) and so is the thicket. But the quiet zones are the two left corners, not one shaped void (see Self-critique) |
| L1 | house law: never arrows | FIXED: none. The rail reads top to bottom, both words run down the sheet, and time runs down it too |
| L2 | text on its own layer with halos | FIXED. The rail is black and on its own layer. The field is clipped 6 mm right of the rail, so type never meets geometry. Beads carry a 0.5 mm exact halo cut into the rings |

## What changed from parent

Everything. r01 is a traced reproduction of the reference diagram. r02 is a different plate on the same
science:

1. **Deleted:** 15 packet rows, all fractions, the softmax row, the Z packet, every fan, leader and
   arrowhead, the corner crosses, the title and the subtitle.
2. **The hero became the plate.** Four crest families instead of one bullseye pair. The upper pair
   is the forward field and the lower pair is its reflection. They meet at the fold, which sits at
   the paper's exact half: fold the sheet on the green line and Q lands on ∂L/∂Q.
3. **The pair was tilted 36°.** Q sits 9 mm above the fold and K sits 62 mm above it. So Q and its
   image form a split coin on the line (crimson above, blue below), and K and its image are two big
   discs far above and far below that bleed off the sheet. This single move replaced the 2×2
   bullseye grid of v1.
4. **Tone from amplitude.** Ink passes = ⌊a/θ⌋ = ⌊√(R/r)⌋, capped at 3. Each source has a heavy
   core that falls to hairline at the rim, which gives the plate its only near/far.
5. **V and Z on the line.** Beads (area ∝ attention weight) are strung on a 3-pass green fold.

## Measurements / computations

All numbers are computed in `piece.py` (`fold_packets`, `head`, `_fd_check`, `build`). Nothing is traced.

**Packets → sources.** The r01 Q and K tables (5 rows each, measured off the reference in r01) are
real signals q_i(ξ), k_j(ξ). Their cosine matrix has best pair **Q row 1 × K row 5, cos 0.908**
(runners-up 0.906 Q5×K5, 0.871 Q4×K4). The overlap is S = 37 342.240. Parseval gives 37 342.2398
(rel. err 5e-9). Resonant carrier w0 = 0.556 rad/px (λ = 11.30 ref px). The phasors are
q = 1443.8 ∠−1.199 and k = 1457.8 ∠−1.067. |q| ≈ |k| (1 % apart), which is why the four discs are
the same size: the data made them equal.

**Geometry (A4 portrait, mm).** λ = 3.0, d = 30λ = 90.0 at 36°. Q (51.8, 157.5), K (124.6, 210.4),
fold y = 148.5 (paper centre), images Q′ (51.8, 139.5) and K′ (124.6, 86.6). Reach: R = (a/θ)², with
θ set so the larger forward wave reaches 88 mm. R_K = 88.0 and R_Q = 86.3; the lower families,
normalised by |C|, reach exactly the same (R_∂Q = R_K, R_∂K = R_Q). Rings per family: 28 / 29 / 29 /
28. Passes: 3 inside r ≤ R/9 (9.8 mm), 2 inside r ≤ R/4 (22 mm), 1 beyond.

**The head.** 44 tokens along the fold at 4.0 mm pitch.
s_j = 6·Re(q G_Q conj(k G_K))/S0, with S0 = max|q G_Q k G_K| = 71 860.6. Attention: max a = 0.292,
entropy 2.13 nats (8.4 effective tokens). The four beads (x = 32.5, 36.5, 40.5, 44.5; a = 0.073,
0.181, 0.292, 0.226) carry 77 % of the attention mass. The other 23 % is spread over 40 tokens whose
beads would be smaller than the fold's ink band, so they are not drawn (bead_min 0.8 mm = a ≥
0.22·max). Values are r01's third V row sampled across the tokens and normalised to max 1. Result:
Z = −0.060, z* = 1.000, L = 0.562, ∂L/∂Z = −1.060. Σ_j g_j = 1e-18: the softmax Jacobian is
zero-sum, as it must be.

**The backward pass.** C = (β/S0) Σ g_j conj(G_Qj) G_Kj = 2.99e-8 ∠**2.623 rad (150.3°)**.
∂L/∂q = C·k ∠+1.556 and ∂L/∂k = conj(C)·q ∠+2.462. Central finite differences on (Re, Im) of q
and k agree to **9.8e-9 and 1.1e-8** relative error.

- **Why the reflection is exact, not a layout choice.** The adjoint of "sample the field on the line"
  is "re-emit from the line": Φ(p) = Σ_j g_j (β/S0) k G_Kj conj(G(p, x_j)). Evaluated at Q it equals
  C·k = ∂L/∂q. A line radiates identically to both sides, so it gives the same value at Q's
  reflection. Numerically, Φ(Q) = Φ(Q′) = ∂L/∂q = 6.6e-7 + 4.361e-5 i, to every printed digit. So
  the gradient on Q really can be read at Q′.
- **The inverted twin.** arg C = 150°, 30° short of a sign flip. The lower rings slip against the
  upper ones by **1.68 mm at the Q column and 1.32 mm at the K column** (of λ = 3.0). The slips
  are opposite in sense because the two sides carry C and conj C. Where a crest lands on the fold
  from above, a near-trough lands from below: the zipper.
- The relative phase between the two sources is −0.132 rad above and −0.906 rad below, so the
  moiré bands shift by 0.83 of a band across the fold.

**Crowding.** 67 403 crest samples. The guard dropped 1 785 (2.6 %), all where a crest runs within
0.82 mm and within 25° of parallel to another stroke. That happens on the two Q–K axes (the dash
seam) and where rings graze the fold tangentially. No crossing is ever removed. Near-parallel crest
strokes of different rings never come closer than 0.82 mm. Crests end ON the fold by design, and they
stop 0.5 mm (beads) or 0.6 mm (source discs) short of a halo. A crest's extra passes sit 0.25 mm
off it inside the same pen-down (weight, not spacing).

## Plot budget

Model (PLOT_JOBS.md): draw at F500 (Leo cap), travel 2000 mm/min, 2.0 s per pen cycle, ~90 s per
swap.

| layer (stream order) | pen | meaning | draw m | travel m | cycles | min |
|---|---|---|---|---|---|---|
| 0 | goldenrod | V: attention beads (= ∂L/∂V shape) | 0.12 | 0.10 | 4 | 0.4 |
| 1 | dodgerblue | K's wave: K above, ∂L/∂Q below-left | 11.09 | 0.95 | 127 | 26.9 |
| 2 | crimson | Q's wave: Q above, ∂L/∂K below-right | 10.78 | 0.85 | 121 | 26.0 |
| 3 | forestgreen | Z: the fold, one 3-pass stroke | 0.56 | 0.08 | 1 | 1.2 |
| 4 | black | rail + 2 words | 0.47 | 0.47 | 81 | 3.9 |
| **total** | | | **23.01** | **2.60** | **334** | **58.4 + 5 swaps ≈ 66 min** |

17 232 commands. Bounds are clean on A4 (drawable 10–200 × 10–287; the only 0,0 is the park).
`preview --score`: grade A, efficiency 0.977. For comparison, the parent r01 v8 costs 4 054 cycles,
11.4 m draw and 11.9 m travel, which is ≈ 171 min on the same model. This plate draws twice the ink
in 40 % of the time.

## Self-critique

| dimension | score | why |
|---|---|---|
| Hierarchy | 7 | At 3 m you see a chevron: two big discs on the right and a split coin at the apex on the fold. At 1 m the moiré lenses, the dash seams, the heavy source cores and the beads come in. At 30 cm you get the zipper. But the two big discs are equal (the data made |q| ≈ |k|), so the dominant mass is a pair, not one |
| Grid & alignment | 6 | The fold is at the paper's exact half, it starts at the rail and runs to the margin, and the field is clipped 6 mm off the rail. The source positions come from d = 30λ at 36° and align with nothing else on the sheet |
| Tension & asymmetry | 7 | A 36° diagonal chevron with bleeds on three sides. The fold's mirror symmetry is the mechanism and is kept |
| Negative space | 5 | The field covers about 75 % of the sheet. The quiet zones are the two left corners, shaped by the Q and ∂Q rims, not one generous void. **Weakest dimension** |
| Craft for pen | 8 | 3 mm pitch, weight by chained passes, no dots, 334 cycles, every crest ends on the fold/frame analytically. One blemish: the guard cuts a ~3 mm gap into the ring tangent to the fold directly above Q and below Q′ |
| Concept legibility | 7 | Not a schematic. The swap lands in one glance IF the viewer holds the series' colour code (Q crimson, K blue). Without it the lower half reads as "the same thing mirrored" and the joke is lost. The rail's two words are the only help |
| Depth | 5 | Declared flat (LeWitt's wall drawings are flat by nature). The only depth cue is amplitude: 3 → 2 → 1 ink passes falling off from each source |

**Single worst thing:** the negative space. The right half of the sheet is wall-to-wall rings, and
the blank paper is left over in the corners rather than composed. The fix I would try next is
θ-driven: raise θ so R drops to ~70 mm and the discs float free of the top, bottom and right. I
tried that (reach 72 in the trial sheets), but K's rim then stopped 4 mm short of the top margin,
which is crowding, not space. The honest next move is a different paper proportion (landscape, or
A3 with the same mm geometry) rather than a parameter.

## Engine requests

- `giant_type(weight=…)` emits each offset pass as its own pen-down, so the rail's 2 words cost 81
  cycles where 40 would do. The sibling r05 chains passes locally. It belongs in `kit.giant_type`.
