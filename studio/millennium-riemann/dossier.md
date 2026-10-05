# millennium-riemann — the Riemann Hypothesis: X marks the spot, and every X is on one line
**Field expert:** mathematics (analytic number theory) · **Date:** 2026-09-28 · **Status:** dossier v1

Plate 1 of the MILLENNIUM series. Reference: `ref/reference.png` (AI poster, an interpretation
brief, not ground truth; it contains four factual errors, listed in §4). Exact data for this plate
is already computed and in `data/` (see §3). Nothing in this dossier is quoted from memory: every
number was computed with mpmath 1.4.1 (`data/compute_xray.py`) or fetched from the cited paper.

## 1. The phenomenon (≤5 lines)

ζ(s) = Σ n⁻ˢ = Π_p (1 − p⁻ˢ)⁻¹ for Re s > 1, continued to all of ℂ except a simple pole at s = 1.
It vanishes at the "trivial" zeros −2, −4, −6, …, and at infinitely many "nontrivial" zeros
ρ = β + iγ inside the critical strip 0 < β < 1. They come in conjugate pairs. **RH: every one has β = ½.**
They matter because they are exactly the frequencies of the primes' deviation from smooth growth
(explicit formula below). Verified numerically for all 0 < γ ≤ 3·10¹², all of them simple (Platt & Trudgian 2021).

### Governing math

- Functional equation: ζ(s) = χ(s) ζ(1−s), χ(s) = 2ˢ πˢ⁻¹ sin(πs/2) Γ(1−s).
  |χ(σ+it)| ≈ (t/2π)^(½−σ). **The critical line is NOT a mirror for |ζ|**: the left side is louder by
  that factor. Only the completed ξ(s) = ½ s(s−1) π^(−s/2) Γ(s/2) ζ(s) satisfies ξ(s) = ξ(1−s).
- Conjugate symmetry: ζ(s̄) = conj ζ(s). The picture **is** a mirror across the real axis (t → −t).
- On the line: ζ(½+it) = e^(−iθ(t)) Z(t), with Z real (Hardy) and θ the Riemann–Siegel theta.
  So Re ζ = Z cos θ, Im ζ = −Z sin θ. Zeros of ζ on the line = sign changes of Z.
  Gram points g_n: θ(g_n) = nπ. Half-Gram points: θ = (n+½)π.
- Zero counting (Riemann–von Mangoldt): N(T) ≈ (T/2π) ln(T/2πe) + 7/8. Mean gap 2π / ln(T/2π).
- Conformality: near a simple zero ζ(s) ≈ ζ'(ρ)(s−ρ), so the curves Re ζ = 0 and Im ζ = 0 cross at
  ρ at **exactly 90°**, the Im ζ = 0 branch leaving at angle −arg ζ'(ρ) (mod 180°) from the σ-axis.
  The level set |ζ| = ε near ρ is a circle of radius ε/|ζ'(ρ)| (a linear cone, not a Gaussian).
- Explicit formula (von Mangoldt), x > 1 not a prime power:
  ψ(x) = x − Σ_ρ x^ρ/ρ − ln 2π − ½ ln(1 − x⁻²),  ψ(x) = Σ_{pᵏ ≤ x} ln p.
  Pairing ρ, ρ̄: each zero contributes the wave −(2√x/|ρ|)·cos(γ ln x − arg ρ) (on RH). ψ jumps by
  ln p at every prime POWER pᵏ. RH ⇔ ψ(x) = x + O(√x ln²x): every wave grows at the same rate √x.
- Pure numbers: ζ(0) = −½, ζ(½) = −1.4603545088, ζ(σ) = 2 at σ = 1.728647239.

## 2. Three candidate visual truths (ranked)

### (a) THE X-RAY — two ink families, and every crossing off the real axis lies on one line ★ RANK 1

Draw only two zero-sets over an **isotropic** window of the plane: the curves Re ζ(s) = 0 (pen A) and
Im ζ(s) = 0 (pen B). That is the whole plate. This is a real mathematical object with a name —
J. Arias-de-Reyna, *X-Ray of Riemann zeta-function* (2003, arXiv:math/0309433: "drawings on the
complex plane of the lines Im ζ(s)=0 and Re ζ(s)=0"). A zero of ζ is precisely where an A-curve
meets a B-curve, and by conformality every such meeting is a clean right-angle **X**.

What the computed picture actually shows (t ≤ 102, σ ∈ [−16, 12], `data/xray_contours.json`):
- **Left half-plane: a laminar comb.** Pen-A curves come in from σ = −∞ as horizontal strata and
  turn back in U-shaped tongues whose tips reach the critical line. Pen-B strata interleave with them.
  Spacing tightens with height (0.56 units between neighbours near t = 100 at σ = −10).
- **Every tongue tip straddles the line.** Each pen-A tongue crosses σ = ½ twice: once at a zero and
  once at a half-Gram point (14.1347 & 14.5179; 21.0220 & 20.6540; 25.0109 & 25.4915 …). A pen-B
  curve crosses the line at each zero, and also at each Gram point (9.6669, 17.8456, 23.1703 …).
- **Right half-plane: almost empty.** Re ζ never vanishes there in this window. Only pen-B lines
  run out to σ → +∞, flattening to the horizontals t = kπ/ln 2 = 4.5324·k. That comes from ζ ≈ 1 + 2⁻ˢ.
- **Bottom row:** pen-A lines land on the real axis exactly at the trivial zeros −2, −4, −6, −8, …;
  pen-B lines leave the real axis where ζ′(σ) = 0 (−2.7173, −4.9368, −7.0746, −9.1705). One small
  pen-A arc joins −2 to the pole at s = 1. The real axis itself is a pen-B line, because ζ is real there.

**Why it is potent — the twist.** Everyone holds "X marks the spot". Here the mechanism supplies
hundreds of millimetres of two inks weaving across the whole plane, and the only places they ever
form an X (above the real axis) all stand on **one vertical line** — nobody drew that line. RH, as a
drawing, is the claim that no X will ever be found anywhere else. The second twist is quieter.
The two halves of the plate are wildly unequal (a dense comb on the left, near silence on the right).
Yet the X's sit exactly on the seam between them. The viewer expects a mirror and gets an asymmetry
with a perfectly straight edge. Nothing in it is a plot: it has no axes and no function extruded,
just two instructions executed exactly.

**Abstract ORDER:** INTERLACED / LAMINAR. Two stratified line families whose crossings are the only
information, and those crossings self-align into a line. Suggested lineage: **Sol LeWitt, Wall
Drawings (1968–)**. The plate literally is two instructions ("every point where Re ζ = 0, in black";
"every point where Im ζ = 0, in the second ink"), and the text could redraw it. Alternative:
**Riley, *Current* (1964)** for the comb's height-dependent phase drift. It is the translator's call,
but the series should not use LeWitt twice.

### (b) THE PRIMES ARE A CHORD — the explicit formula as interfering strata ★ RANK 2

Each conjugate pair of zeros contributes one wave cos(γ_n ln x − arg ρ_n) with amplitude 2√x/|ρ_n|.
Stack rows. Row k draws the truncated ψ_k(x) − x (or the pure oscillation Σ_{n≤k} waves) over
x ∈ [2, ~50]. Row 1 is one smooth undulation. As zeros are added, the rows develop cliffs, and the
cliffs line up vertically **at the primes and prime powers**. A vertical fault opens at x = 2, 3, 4,
5, 7, 8, 9, 11, 13, … with drop ln p. The primes are never drawn; they appear as the columns where
an interference of smooth waves agrees to break. Measured convergence: ψ(10.5) = ln 2520 = 7.8320,
and the truncations give 7.7021 (10 zeros), 7.8185 (30), 7.8352 (100).

**Twist:** "the primes are random" meets "the primes are a chord", and RH is the statement that
**every voice in the chord is equally loud** (all grow as √x). One off-line zero would be one voice
growing as x^β with β > ½, and it would eventually drown the others. **ORDER:** LAMINAR / INTERFERING
(one line family, phase drift makes the surface). Lineage: Riley, *Cataract 3* (1967). This is the
best partner for the reference's "Primes:" footer, but it is not about the critical line itself,
which is why it is rank 2.

### (c) THE FIELD MADE TRUE — isophase lines drain into the zeros ★ RANK 3

This is the reference's streamline field done correctly. On a window around the strip
(σ ∈ [−1, 2], t ∈ [−T, T]), draw the level curves of arg ζ (K phase levels) and optionally of |ζ|.
Since log|ζ| is harmonic, isophase lines ARE the gradient lines of |ζ|. They pour out of the pole at
s = 1 and converge into each zero, with exactly K lines entering each simple zero. |ζ|-contours are
small circles of radius ε/|ζ'(ρ)| around each zero. ORDER: FLOW-TO-ATTRACTOR (sinks on one line,
source at s = 1). Lineage: Kandinsky, *Point and Line to Plane* (1926) (points as forces, lines
converging on them). It is rank 3 because it is the closest to "the function extruded" (a scientific
figure). It also needs an anisotropic σ-stretch to be legible (the strip is 1 unit wide and 50 tall),
and the stretch breaks the right angles. It survives only if the asymmetry, the pole and the zero-free
gap below t = 14.13 are all shown truthfully.

## 3. Real data — verified

**All computed locally, 2026-09-28, mpmath 1.4.1** (not in `.venv`; install into a scratch target,
see the docstring of `data/compute_xray.py`). Outputs already written to `data/` (uncommitted):

| file | content |
|---|---|
| `data/zeros.json` | first 100 zeros γ_n (20 digits), \|ζ'(ρ_n)\|, arg ζ'(ρ_n) in degrees; Gram and half-Gram points < 102 |
| `data/xray_contours.json` | polylines of Re ζ = 0 (`re0`, 38 pieces) and Im ζ = 0 (`im0`, 45 pieces) on σ ∈ [−16, 12], t ∈ [0, 102], grid step 0.05, matplotlib marching squares on `mp.fp.zeta`. Mirror for t < 0. Add the real axis (t = 0) as an Im = 0 line yourself. |

First zeros γ_n (cross-checked by `mp.zetazero`; they match the curator's list and the Odlyzko/LMFDB tables):
14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588, 37.586178159, 40.918719012,
43.327073281, 48.005150881, 49.773832478 | 52.9703, 56.4462, 59.3470, 60.8318, 65.1125 … γ₃₀ = 101.317851, γ₁₀₀ = 236.5242297.
Counts: N(50) = 10, N(100) = 29 (formula 29.002). Gaps for t < 50: min 1.7687 (γ₉–γ₁₀), max 6.8873 (γ₁–γ₂).

|ζ'(ρ_n)| for n = 1…5: 0.79316, 1.13684, 1.37172, 1.30394, 1.38212. arg ζ'(ρ_n): +9.046°, −12.638°, +19.152°, −30.792°, +32.891°.

Critical-line crossings, t ∈ [1, 52]:
- Im ζ = 0 at 3.4362, 9.6669*, 14.1347, 17.8456*, 21.0220, 23.1703*, 25.0109, 27.6702*, 30.4249, 31.7180*, 32.9351, 35.4672*, …
  (* = Gram point; 3.4362 is the second solution of θ = −π, since θ has its minimum −3.5310 near t = 6.29)
- Re ζ = 0 at 14.1347, 14.5179†, 20.6540†, 21.0220, 25.0109, 25.4915†, 29.7385†, 30.4249, 32.9351, 33.6238†, … († = half-Gram)

Asymmetry, |ζ(σ+it)| / |ζ(1−σ+it)| against (t/2π)^(½−σ):
t = 14.1347, σ = 0: 1.4999 vs 1.4999; t = 30, σ = 0: 2.1851 vs 2.1851; t = 50, σ = 0: 2.8209 vs 2.8209.

Sources:
- Arias-de-Reyna, *X-Ray of Riemann zeta-function*, arXiv:math/0309433 (2003) — https://arxiv.org/abs/math/0309433
- Arias de Reyna, Brent, van de Lune, *On the sign of the real part of the Riemann zeta-function*,
  arXiv:1205.4423. Re ζ(σ+it) < 0 occurs with positive density on lines σ > ½, so the pen-A tongues
  DO cross to the right of the line at larger heights — https://arxiv.org/abs/1205.4423
- Platt & Trudgian, *The Riemann hypothesis is true up to 3·10¹²*, Bull. LMS 53(3) 2021, 792–797 — https://arxiv.org/abs/2004.09765
- Primes ≤ 100 (25 of them): 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97.
  Prime powers ≤ 100: 4 8 9 16 25 27 32 49 64 81.

## 4. Simplifications allowed vs. lies

**Allowed:**
- Cropping the plane anywhere, at the frame. The comb continues to σ → −∞, and a crop that says so is honest.
- Mirroring t → −t (conjugate symmetry is exact). If mirrored, the real axis sits mid-sheet with the
  trivial-zero feet on it.
- A single **uniform** scale (mm per unit) for rank 1. For rank 3, an anisotropic σ-stretch only if
  it is uniform, stated on the sheet, and the plate stops claiming right angles.
- Marching-squares polylines at grid step ≤ 0.05 units (error < 0.01 mm at the scales in §6), and
  light smoothing below pen resolution.
- Leaving the critical line undrawn (implied by the X's), or drawing it as a hairline or ticks.
- Showing fewer zeros (10 or 30) and saying which window it is.
- For rank 2: truncating the zero sum at N and labelling N. The Gibbs overshoot at each cliff is real
  and must stay.

**Lies (binding on everyone):**
1. **A left–right mirror about Re s = ½** for |ζ|, its contours or its phase lines. The reference does
   this and it is false: |ζ(σ+it)| = (t/2π)^(½−σ)·|ζ(1−σ+it)|. Only ξ is symmetric, and a plate drawing
   ξ must say ξ.
2. **Zeros near the real axis.** No zero exists for 0 < |t| < 14.134725. The reference packs circles
   down to t ≈ 1. That stretch of the line stays empty.
3. **Evenly spaced zeros.** The gaps run 1.77–6.89 in t < 50 and shrink on average as 2π/ln(t/2π).
   A regular ladder of beads is a lie. So is the reference inset's "32.0" (true: 32.935) and its
   missing 25.01 and 30.42.
4. **The pole at s = 1 omitted** from any |ζ| or phase field. It is the source of every phase line.
5. **Invented height values or zero positions,** or zeros placed "by eye". Every γ comes from `data/zeros.json`.
6. **Claiming the pen-A tongues never cross σ = ½.** They do: the max σ reached in t ≤ 102 is 0.715,
   and at larger heights Re ζ < 0 occurs to the right of the line with positive density (arXiv:1205.4423).
   The claim is only about the X's, never about either family alone.
7. **Non-right-angle X's on an isotropic plate.** If the crossing is visibly oblique at uniform scale,
   the geometry is wrong.
8. **A grey |ζ| field translated into hatch density** and presented as data. Tone must be a stated
   quantity. The reference's grey |ζ| colour bar (10⁻⁴…10²) encodes nothing a plotter can honour.
9. **For rank 2: jumps only at primes.** ψ also jumps at prime powers 4, 8, 9, 16, 25, 27, 32, 49
   (drop ln p). If the plate wants primes only, it must switch to Riemann's R-function formula for π(x)
   and say so.
10. Any caption implying RH is proved, or that "the zeros are on the line" has been observed beyond
    the verified height 3·10¹².

## 5. The misconception to quietly correct

**"The critical line is a line of symmetry, a mirror, and the zeros sit on it because the picture is
symmetric."** The reference poster draws exactly that belief. Truth: the functional equation pairs s
with 1−s, but the modulus is lopsided by (t/2π)^(½−σ). In the X-ray the two sides do not even resemble
each other: a dense comb on the left, near-empty paper on the right. The zeros choosing the seam of a
**non**-symmetric picture is what makes RH surprising. If RH fails, off-line zeros must come in
mirror pairs (ρ and 1−ρ̄), so the symmetry would force pairs of X's. RH says it never has to.

Secondary: "the zeros are regularly spaced beads" (they repel and wander, like random-matrix
eigenvalues), and "RH is about primes being random" (it is about the error term being as small as
possible, the equal-loudness of §2b).

## 6. Pen-plotter fit

- **Naturally LINES:** the two zero-sets are one-dimensional curves already. That is the house's ideal
  (isolines, not fields). No fill, no tone, and no dotted run is needed anywhere in rank 1.
- **Pen meanings (rank 1):** A = Re ζ = 0 (black), B = Im ζ = 0 (second, quieter ink), accent (the
  series' one loud colour) = the X's only: small marks, rings, or a short bold re-stroke of both
  branches through each ρ, with the zeros from `zeros.json`. It is scarce by construction (10 marks for
  t ≤ 52, 30 for t ≤ 102). Suggested order: B → A → accent, so the loud mark lands last on top of the
  crossing.
- **Lengths (complex-plane units → multiply by the chosen mm/unit):**
  σ ∈ [−10, 10], t ∈ [0, 52]: A = 260.8 u, B = 372.6 u (+ real axis). σ ∈ [−10, 10], t ∈ [0, 102]:
  A = 695.9 u, B = 910.5 u. Full data window σ ∈ [−16, 12], t ∈ [0, 102]: A = 1103.1 u, B = 1364.0 u.
  Example: A3 portrait, t ∈ [0, 52] at 6.5 mm/u gives A = 1.70 m (2.8 min at F600 = 10 mm/s) and
  B = 2.42 m (4.0 min). Full window at 3.3 mm/u gives A = 3.64 m (6.1 min) and B = 4.50 m (7.5 min).
  About 40 pieces per pen, so pen cycles are negligible. Every stroke is long and spatially ordered
  (strata run left→right), and every polyline can be split at any vertex for batching.
- **Density risks:** the closest non-crossing approach of A and B is 0.394 u (near σ ≈ 0, t ≈ 95.8) for
  t ≤ 102, and 0.453 u for t ≤ 52. Same-family neighbours reach 0.56 u at σ = −10 near t = 100.
  - Floor: scale ≥ 2.1 mm/u keeps everything ≥ 0.8 mm.
  - **On A5 (Leo), t ≤ 102 does not fit** (≈1.5 mm/u gives 0.58 mm). Use t ≤ 52 at ≥ 2.9 mm/u, or accept A4+.
  - At each X, the two inks deliberately touch. That is the one sanctioned ink-on-ink spot.
- **Must stay blank paper:** the line segment 0 < t < 14.13 (the zero-free stretch). The right half-plane
  apart from the pen-B asymptotes: its emptiness is the truth (ζ ≈ 1; Re ζ > 0 is guaranteed for
  σ > 1.7286, where ζ(σ) = 2). Also a halo around every X, so the accent reads.
- **Type:** any caption equation from §1 is fine. "Re(s) = ½" and the first γ values are the only
  numbers the plate needs.

## 7. Check numbers

Setup for all one-liners: `import mpmath as mp; mp.mp.dps = 20` (mpmath in a scratch target), or read
`data/zeros.json` / `data/xray_contours.json`.

| # | value | reproduce |
|---|---|---|
| 1 | γ₁…γ₅ = 14.1347, 21.0220, 25.0109, 30.4249, 32.9351. N(50) = 10, N(102) = 30 (γ₃₀ = 101.3179) | `[mp.zetazero(n).imag for n in range(1,6)]`; `mp.nzeros(50)` |
| 2 | No zero on the drawn line below t = 14.1347. Lowest X at 14.1347, and the next gap 6.8873 is the largest in t < 50 | `mp.zetazero(1)`; diffs of #1 |
| 3 | Every X is 90°. The Im = 0 branch through ρ₁ is at 170.95° (−9.05°) from the σ-axis, through ρ₂ at 12.64°, through ρ₄ at 30.79° | `-mp.degrees(mp.arg(mp.zeta(mp.zetazero(n), derivative=1)))` |
| 4 | Pen-B lines on the far right flatten to t = kπ/ln 2 = 4.5324, 9.0647, 13.5971, 18.1294 …; measured at σ = 10: 4.508, 9.078, 13.614, 18.108 | `k*mp.pi/mp.log(2)`; ends of `im0` in the json |
| 5 | Pen-A lines touch the real axis at −2, −4, −6, −8 (trivial zeros). Pen-B lines leave it at −2.7173, −4.9368, −7.0746, −9.1705 | `mp.findroot(lambda s: mp.zeta(s,derivative=1), -2.7)` |
| 6 | On σ = ½ between X's: pen B crosses at Gram points 9.6669, 17.8456, 23.1703, 27.6702, 31.7180. Pen A crosses at half-Gram points 14.5179, 20.6540, 25.4915, 29.7385 | `mp.grampoint(n)`; `findroot(siegeltheta(t)-(n+.5)*pi)` |
| 7 | Asymmetry \|ζ(it+0)\| / \|ζ(1+it)\| at t = 30 is 2.1851 = (30/2π)^½. The left side is louder, so no left–right mirror | `abs(mp.zeta(30j))/abs(mp.zeta(1+30j))` |
| 8 | Pen-A tongues reach at most σ = 0.715 for 2 < t < 102 (they cross the line; only the X's are confined). Nearest A–B approach away from zeros is 0.394 u | from `re0` / `im0` in the json |
| 9 | ζ(½) = −1.4603545, ζ(0) = −0.5. \|ζ'(ρ₁)\| = 0.79316, so an \|ζ\| = 0.1 ring around ρ₁ has radius 0.1261 | `mp.zeta(0.5)`; `abs(mp.zeta(mp.zetazero(1),derivative=1))` |
| 10 | (rank 2) ψ(10.5) = ln 2520 = 7.8320. The truncation with 100 zeros gives 7.8352 (10 zeros: 7.7021). Cliff heights are ln p: 0.6931, 1.0986, 1.6094, 1.9459 at 2, 3, 5, 7 | explicit formula in §1 with `rho=[mp.zetazero(n) for n in range(1,101)]` |
