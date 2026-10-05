# millennium-riemann — encoding (VISUAL TRANSLATOR)   · Status: encoding v1 · 2026-09-28

Source of truth: `studio/millennium-riemann/dossier.md` v1, visual truth **(a) THE X-RAY**
(rank 1). Truth (b), the explicit formula, appears only as the faithful thesis's footer. Truth (c),
the isophase field, is **not drawn**. Data: `data/zeros.json` (100 zeros, Gram and half-Gram points)
and `data/xray_contours.json` (σ ∈ [−16, 12]). Both theses need a **wider window**, so recompute
it (see §10). Reference: `ref/reference.png`, an AI poster. It is an interpretation brief, never a
bitmap (`studio/AUTHORING.md`). No BRIEF.md, FEEDBACK.md or LEDGER.md exists yet.
Plate 1 of the MILLENNIUM series. Theses built in parallel: **faithful** and **abstract**.
Everything binds both unless a line says `[F]` or `[A]`.

Translator's measurement (2026-09-28, mp.fp.zeta on a 0.1 grid over σ ∈ [−50, 32], t ∈ [0, 102],
scratch only). The comb runs to the left frame at every width tried. Same-family pitch at the top
of the sheet is 1.1 u for every σ from −5 to −48, so A–B neighbours sit ≈ 0.55 u apart. Below
t ≈ 15 the strata fan down into the real axis. The right half-plane holds only pen-B rulings.

---

## 1. STYLE assignment

**A stated hybrid. SWISS / INTERNATIONAL sheet (canon 3) carrying a CONCEPTUAL instruction
drawing (LeWitt), in the Millennium palette: cream stock, black, and one red.**

Why Swiss fits the ORDER. The mechanism is built from lopsidedness and a grid. The X-ray is
radically asymmetric: a dense comb on one side of the seam and near-empty paper on the other. That
asymmetry is Swiss's "radical negative space", and here it is supplied by ζ rather than chosen.
The right half-plane also has its own ruling: pen-B lines flatten to t = kπ/ln 2. That ruling
becomes the **modular baseline grid** for the type, so the Swiss grid is ζ's own grid. Swiss asks for
one HUGE element, and the comb is it. It asks for flush-left type (supplied) and for red and black
only, with the paper as the third colour. Our two line families are one ink at two weights, so that
holds too.

Why LeWitt carries it: the plate is literally two instructions, and a stranger could redraw it
from its own caption. **Flatness is declared.** The subject is the complex plane, and the claim
that every meeting is a right angle (conformality) survives only in a flat, isotropic plane. Any
perspective, relief or tilt would break the 90° truth (dossier lie 7). The Swiss canon is flat by
nature as well.

**LINEAGE:** `lineage: Sol LeWitt, Wall Drawing #46 (1970), "Vertical lines, not straight, not
touching, covering the wall evenly" (curator: verify wording against the catalogue raisonné).
Order taken: an instruction executed exactly, whose text could redraw the wall. Here ζ writes two
such instructions ("every point where Re ζ = 0"; "every point where Im ζ = 0"), their lines are
not straight and never touch, except at the zeros, and every touch above the real axis stands in one column.`
Batch check: navier-stokes answers Riley, yang-mills Kandinsky, p-vs-np Mohr and hodge Gabo, so
LeWitt is free. The dossier's alternative (Riley, *Current*) is **not** used, because it would
share a lineage with navier-stokes.

## 2. The one-glance statement

> **Two families of lines cover the plane and never touch — except in one column, where every
> meeting is a red right-angled cross.**

- **3 m:** a dense black comb of U-shaped tongues fills the left of the sheet, all pointing right.
  Their tips stop on one invisible vertical, and each tip is pinned by a small red cross. To the
  right of it lies quiet ruled paper. Low in the column there is a long empty stretch with no red.
- **1 m:** a hairline second family threads through the comb. It meets the black only at the red
  crosses (and down on the real axis). The red crosses tilt differently from one another and are
  unevenly spaced, yet they all stand on one line that nobody drew.
- **30 cm:** each red cross is a right angle. The two instructions are printed as the caption. The
  status line reads "checked to 3·10¹², not proved".

## 3. The abstract ORDER

**INTERLACED / LAMINAR.** Two stratified families of lines. The only information is where they
meet, and the meetings self-align into a line.

Exact mapping in one line each:
- "**Black is Re ζ = 0, hairline is Im ζ = 0. A meeting is a zero. Red is only where they meet
  above the real axis.**"
- "**One scale on both axes, so every meeting is 90° and the column is exactly Re s = ½.**"

The critical line is **never drawn** in `[A]`. In `[F]` it gets two red register ticks outside the
field and nothing inside. This names no plot and no object: the plate has no axes, no function
surface and no beads.

## 4. Channel mapping (Tufte: nothing drawn that encodes nothing)

| ink on paper | encodes | exact rule / range |
|---|---|---|
| horizontal position | σ = Re s | x = X0 + s·(σ − ½). One uniform scale `s` (mm per unit) on both axes. No stretch. |
| vertical position | t = Im s | y = y_axis + s·t. `[F]` mirrors t → −t, which is exact by conjugate symmetry. `[A]` draws t ≥ 0 only, and the caption declares it. |
| **black 0.3 curves** (pen A) | the zero set Re ζ(s) = 0 | Marching squares on mp.fp.zeta at grid ≤ 0.05 u, one pass. Lines run to the frame wherever they reach it. No smoothing beyond the grid. |
| **black 0.1 hairlines** (pen B) | the zero set Im ζ(s) = 0, **including the real axis** (ζ is real there; draw t = 0 across the whole field) | Same method, one pass. Right of σ ≈ 6 these become the rulings t = kπ/ln 2 (exact to < 0.01 mm by σ = 20). |
| black–hairline crossing **on the real axis** | the trivial zeros −2, −4, −6, … and the pole s = 1 | These fall out of the data with **no accent**. Black lands at 90° on the hairline axis. |
| **red crossing** (pen R) | a nontrivial zero ρ_n = ½ + iγ_n from `zeros.json` | **Substitution, not overlay.** Inside a circle of radius r centred on (½, γ_n), the A-branch and B-branch *through ρ_n* are drawn in red, and outside it they are black and hairline. The cut is an exact `geometry.Circle` clip, with 0.2 mm red overlap at each joint. The arms follow the true curves (the A-arm curves with the tongue tip). Size is constant (r per plate, §5). It encodes location only, not \|ζ'\|. **No other line is clipped** by the circle. |
| blank column 0 < t < 14.1347 on σ = ½ | the zero-free stretch | No red and no mark in it. `[F]` mirrors this, so the gap is 2 × 14.1347 u centred on the real axis. |
| near-empty right field | the lopsidedness \|ζ(σ+it)\| = (t/2π)^(½−σ)·\|ζ(1−σ+it)\|: Re ζ > 0 for σ > 1.7286 | Only hairline rulings. Nothing is added, for balance or any other reason. |
| red register ticks `[F]` | where Re s = ½ meets the field's crop edges | Two 5 mm vertical red ticks outside the field, one above the top crop and one below the bottom crop. Nothing inside the field. |
| footer curve `[F]`, text layer | ψ₁₀₀(x) − x, the explicit formula with the first 100 zeros, x ∈ [2, 32] | Exact sum from §1 of the dossier. Cliffs of ln p at primes **and** prime powers. Gibbs ringing is kept. Primes are labelled 2.2 mm caps and prime powers 1.6 mm caps. The curve is stated, not decorative (§5F). |
| **not encoded (declared)** | \|ζ\|, arg ζ, grey tone, \|ζ'(ρ)\|, Gram points as marks | Gram and half-Gram points are *visible* as the places where one family alone crosses the column. They get no mark. |

## 5. Composition sketch — A3 portrait 297 × 420 mm, margins 15, y measured UP from the bottom edge

The two theses share the same bands: title band y ∈ [372, 405] top-left; the field below it with a
straight horizontal crop; bottom captions/footer below the field. **No type ever sits over the comb**,
so no halo is ever needed inside the field. Type lives in the title band, in the right void
between rulings, or below the field.

### 5A — ABSTRACT (the instruction drawing: upper half-plane, 28 crosses)

- s = **3.45 mm/u**. X0 = **180.0** (σ = ½, the 62 % line). Window σ ∈ [−47.33, 30.07]. The comb
  **bleeds off the left frame** (the crop is honest: the comb continues to −∞).
- Real axis at **y = 32.0**, and it is the field's bottom edge (the hairline runs the full frame width).
  The top crop is at t = **97.35**, the mid-gap between γ₂₈ = 95.871 and γ₂₉ = 98.831, so the crop
  sits 5.1 mm from both. That puts it at y = 367.9. **28 red crosses.**
- Lowest cross at y = 80.76. The empty stretch on the column is **48.8 mm** above the baseline.
- The rulings on the right sit at y = 32 + k·**15.64** mm, k = 1…21. These are the **baseline grid**. The
  text column is flush-left at **x = 206** (σ = 8, where the rulings are flat). Type sits between two
  rulings with ≥ 2.5 mm clearance, never on them.
- r = **1.6 mm**, which is 0.38 × the tightest zero gap (γ₂₇–γ₂₈ = 1.2193 u = 4.21 mm).
- Title: flush-left x = 15, baseline 395, spaced caps 8 mm: `RIEMANN  HYPOTHESIS`. Statement at 2.5 mm
  caps, baseline 384: `EVERY CROSSING ABOVE THE REAL LINE STANDS ON RE S = 1/2.`
- The right-void column (upper third, between rulings) holds the two instructions as a LeWitt wall
  label, one instruction per ruling band:
  `BLACK: EVERY POINT WHERE THE REAL PART OF ζ(S) IS ZERO.` /
  `HAIRLINE: EVERY POINT WHERE THE IMAGINARY PART OF ζ(S) IS ZERO.` /
  `RED: WHERE BOTH ARE.`
- Bottom band y ∈ [15, 27], below the baseline. Flush-left at x = 15:
  `UPPER HALF-PLANE, 0 ≤ T ≤ 97.35. ONE SCALE: 3.45 MM PER UNIT. 28 ZEROS.` Flush-right at x = 282:
  `VERIFIED TO T = 3·10¹² (PLATT–TRUDGIAN 2021). NOT PROVED.`
- **Dominant mass:** the comb and fan, x ∈ [15, 180], y ∈ [32, 368] (≈ 55 400 mm², > 90 % of the ink).
  **Quiet zone:** the ruled right field, x ∈ [186, 282] (≈ 32 000 mm² at ≈ 1/15 of the comb's ink
  density). Ink ratio ≥ 10 : 1, so the dominance comes from the data, not from layout. The diagonal
  is the fan's sweep from upper-left down into the baseline at the lower-left.

### 5F — FAITHFUL (the reference's architecture, measured and corrected)

- s = **3.0 mm/u**. **X0 = 148.5, the sheet's centre, exactly where the reference put its red line.**
  This is declared. The frame is symmetric and the content is not, so the centred axis works as the
  experiment's control. The left half is a dense chevron comb and the right half is ruled paper.
  This single decision refutes the reference's left–right mirror. Window σ ∈ [−44.0, 45.0].
- Mirrored t ∈ [−51.37, 51.37], where 51.37 is the mid-gap between γ₁₀ = 49.774 and γ₁₁ = 52.970.
  The real axis sits at **y = 210.0**, mid-field, as in the reference, and the field spans
  y ∈ [55.9, 364.1]. That gives **20 red crosses** (10 zeros and their conjugates). The true
  mirror is **horizontal**: the comb above the real axis reflects below it. The A-lines pass
  through the real axis at the trivial zeros, so each upper/lower pair is **one stroke**.
- The zero-free gap on the column is 84.8 mm, centred on the real axis. It is the reference's
  densest bead stretch, and here it is left empty.
- The rulings sit at y = 210 ± k·**13.60** mm, k = 1…11. Text column flush-left at **x = 190**
  (σ = 14.3). r = **2.0 mm** (0.38 × min gap γ₉–γ₁₀ = 1.7687 u = 5.31 mm).
- Title: flush-left x = 15, baseline 395 (8 mm caps, one line or two as the reference has).
  Statement at 2.5 mm caps: `ALL NONTRIVIAL ZEROS LIE ON THE CRITICAL LINE RE S = 1/2.`
- Right void, upper half: the tagline `THE ZEROS CHOOSE THE SEAM OF A PICTURE THAT IS NOT
  SYMMETRIC.` The corrected claim goes below it: `ζ(ρ) = 0, 0 < RE ρ < 1  ⇒  RE ρ = 1/2 ?` The
  reference's "⇔" is false, so replace it. Right void, lower half: `ζ(S) = Σ 1/Nˢ = Π (1 − P⁻ˢ)⁻¹`
  and `VERIFIED TO 3·10¹². NOT PROVED.`
- **Footer (the reference's "Primes:" strip, made true):** ψ₁₀₀(x) − x for x ∈ [2, 32], mapped to
  x ∈ [15, 282] (8.9 mm per unit) and at 4 mm per unit of height, in the band y ∈ [22, 44].
  Numerals go at y ∈ [15, 20]: primes 2 3 5 7 11 13 17 19 23 29 31 at 2.2 mm, prime powers 4 8 9 16
  25 27 at 1.6 mm. The label is flush-left above the band:
  `PSI(X) − X FROM THE FIRST 100 ZEROS: A CLIFF OF LN P AT EVERY PRIME AND PRIME POWER.` There is no
  axis line, no ticks and no arrow. The numerals are the only scale.
- Red ticks: x = 148.5, y ∈ [366, 371] and [49, 54].
- **Dominant mass:** the chevron comb x ∈ [15, 148.5], y ∈ [56, 364] (≈ 41 000 mm²). **Quiet zone:**
  the right half, ruled.
- **Reference → faithful mapping:**

  | reference shows | faithful draws |
  |---|---|
  | streamline "field" mirrored left–right and top–bottom | the X-ray: two exact zero sets, mirrored **top–bottom only**. The right half is near-empty, as ζ makes it. |
  | red critical line drawn full height | two red register ticks outside the field. The column is implied by the crosses. |
  | blue rings at evenly spaced heights, down to t ≈ 1 | red crossings at the 20 true ±γ_n. The column is empty for \|t\| < 14.13. |
  | Re/Im axes with arrows and 0, ½, 1 labels | the real axis survives as the hairline it truly is (Im ζ = 0). No arrows, no numbers. |
  | \|ζ\| grey colour bar | **cut** (lie 8) |
  | "DETAIL NEAR ZEROS" inset with "32.0" | **cut**: at 3 mm/u the plate itself shows each crossing exactly |
  | formulas split left and right | all type moves into the right void. The left belongs to the comb. |
  | "ζ(s)=0 ⇔ Re(s)=½ ?" | "ζ(ρ)=0, 0<Re ρ<1 ⇒ Re ρ = ½ ?" |
  | "Primes:" dotted number line | ψ₁₀₀(x) − x with cliffs at primes and prime powers |
  | bottom tagline "ONE LINE. INFINITE CONSEQUENCES." | optional, centred bottom is dropped. If kept, flush-left under the footer label. |

## 6. Pen budget — 2 inks, 3 physical pens, 4 layers (layer discipline, no cap)

| order | layer | physical pen | meaning |
|---|---|---|---|
| 1 | B · HAIRLINE | black 0.1 fineliner | Im ζ = 0, the real axis included |
| 2 | A · BLACK | black 0.3 | Re ζ = 0 |
| 3 | TEXT | the same black 0.3, own layer, **no swap** | title, statement, instructions, captions; `[F]` also the ψ footer (annotation register) |
| 4 | RED | red 0.5 | the nontrivial zeros, and nothing else (`[F]`: plus the 2 register ticks) |

The order runs light to dark with red last, so nothing ever inks over the accent. That makes
**2 pen swaps**. Red is < 1.5 % of the ink. Fallback, only if the art critic cannot separate the
families at 1 m: B moves to a warm grey 0.2. It is never blue, because blue would be a second
loud hue.

## 7. Expressive levers (one decision each)

- **Proportion.** `[A]` comb to void is 62 : 38 by width and ≥ 10 : 1 by ink. `[F]` is 50 : 50 by
  width and ≥ 10 : 1 by ink. That imbalance is the argument against the mirror.
- **Fill vs void.** There are three silences, each a truth: the ruled right field (ζ ≈ 1), the
  zero-free stretch of the column, and `[A]` the omitted lower half (declared).
- **Density gradient.** Only the data's own. Strata tighten upward (zero density grows like
  ln(t/2π)/2π) and fan open near the real axis. No cosmetic ramp is allowed.
- **Colour play.** One red, scarce, and only where the two instructions coincide. Weight, not hue,
  separates the families.
- **Texture direction.** Set by ζ. The strata run horizontal, cross-grain to the vertical seam they
  converge on. Nothing is re-oriented for effect.

## 8. The twist

**What the viewer holds:** "X marks the spot", and the poster belief that the critical line is a
mirror which the zeros sit on *because* the picture is symmetric (dossier §5).

**What the mechanism breaks:** the lines cover the whole plane, yet they form an X only in one column.
The column is the seam of a picture that is **not** symmetric: comb on one side, silence on the
other. Nobody drew the line. RH, as a drawing, says that no red X will ever appear off it. The
LeWitt turn is that his instruction says "not touching", and ζ's two instructions obey it everywhere
except at the zeros.

## 9. Forbidden list (binding on both; the science critic fails any of these)

1. **A left–right mirror** of anything, or any ink added to the right field "for balance".
2. **Any red, bead or mark on σ = ½ for |t| < 14.1347.** No evenly spaced ladder. Every γ comes
   from `zeros.json`, never placed by eye.
3. **Drawing the critical line.** `[A]`: nothing. `[F]`: two ticks outside the field, with no
   hairline, dots or dashes along it.
4. **Streamlines, |ζ| contours, phase lines, hatch or dot tone, or a colour bar.** Nothing from
   truth (c) and no grey from the reference.
5. **Axes, arrows, tick marks, grid lines, frame boxes, or an inset/detail box.**
6. **Rings, circles or beads around zeros.** The mark is the red crossing, made of the curves
   themselves.
7. **Anisotropic scale, rotation or perspective.** A visibly oblique red X is a geometry bug.
8. **Clipping unrelated lines** near a crossing, or halos inside the field. Type never sits on the comb.
9. **Moving, smoothing or "tidying" curves** beyond the 0.05 u marching-squares grid. The tongues
   that cross σ = ½ at half-Gram points stay exactly where they are (dossier lie 6).
10. Red on the trivial zeros, the pole, or anything other than ρ_n.
11. Any caption implying RH is proved. "⇔". The reference's "32.0". `[F]` a footer with jumps at
    primes only.
12. Giant decorative type (no giant ½). No text larger than the title.

## 10. Fabrication

- **Data.** Both windows exceed `xray_contours.json`. Recompute with `data/compute_xray.py` on a
  changed grid (mpmath in a scratch target, as its docstring says). **Write new files and never
  overwrite the existing one:** `data/xray_abstract.json` (σ ∈ [−48, 31], t ∈ [0, 98], step 0.05,
  ≈ 8 min on 8 cores) and `data/xray_faithful.json` (σ ∈ [−45, 46], t ∈ [0, 52], step 0.05,
  ≈ 5 min). Add the real axis by hand. Guard NaN at s = 1. `[F]`: mirror t → −t and join the A pieces
  through the real axis. Place the red centres at the exact (½, γ_n), not at the marching-squares
  crossing (the error is < 0.04 mm anyway).
- **Spacing floors** (measured). The nearest non-crossing A–B approach is 0.394 u, which is 1.36 mm
  in `[A]` and 1.18 mm in `[F]`. The top-of-sheet A–B pitch is ≈ 0.55 u, which is 1.9 mm in `[A]` and 1.65 mm
  in `[F]`. Same-family pitch is ≥ 1.1 u (≥ 3.3 mm). Everything is ≥ 0.8 mm. Red touches ink only
  at its own joints and centre.
- **Other papers.** A4 is uniform ×0.707: 1.36 mm drops to 0.96 mm, still above the floor. **A5 (Leo)
  is NOT a scale-down** (it would give 0.68 mm). An A5 edition must re-window to t ≤ 52 at
  s ≥ 2.9 mm/u (`[A]`: 10 crosses), and it needs the pen-up frame trace first.
- **Draw lengths and time on A3** (Leo F600 ≈ 10 mm/s, ≈ 2.5 s per pen cycle):

  | layer | `[A]` | `[F]` |
  |---|---|---|
  | B hairline | ≈ 13.9 m, ~50 strokes → **≈ 25 min** | ≈ 11.6 m, ~55 strokes → **≈ 21 min** |
  | A black | ≈ 11.4 m, ~51 strokes → **≈ 21 min** | ≈ 8.3 m, ~35 strokes (joined through the axis) → **≈ 16 min** |
  | TEXT | ≈ 400 glyph strokes → **≈ 12 min** | ≈ 550 glyph strokes + footer ≈ 0.4 m → **≈ 16 min** |
  | RED | 56 arms ≈ 0.18 m → **≈ 3 min** | 40 arms + 2 ticks ≈ 0.17 m → **≈ 2 min** |
  | **total** | **≈ 61 min, 2 swaps** | **≈ 55 min, 2 swaps** |

  No dotted runs anywhere. Every pen cycle is a whole curve or a glyph stroke.
- **Batching.** Order A and B strokes by the t of their left endpoint, bottom to top, alternating
  direction. Any stroke longer than 300 mm (the tongues run ≈ 330 mm in `[A]`) may split at a vertex
  near its U-tip. Re-zero check every ~15 strokes. Rulings go bottom to top, then the fan, then the
  comb, so there is no sheet-crossing travel. Red goes bottom to top along the column (≤ 20 mm hops).
- **Flood risks:** none by construction. There is no fill and no tone. The only ink-on-ink is at the
  red centres (red on red) and the 0.2 mm joint overlaps.
- **Glyphs missing from the stroke font** (author them, or rephrase): ζ, ρ, ψ, ½, ⇒, ⁻, ˢ.
  Available: σ Σ Π √ ∞ ≤ ≥ · ² ³ ¹. "1/2" is acceptable wherever ½ is not authored.

## 11. Acceptance checks (the art critic marks each PASS/FAIL on the png)

1. **ONE COLUMN.** Every red cross centre lies within ±0.3 mm of one vertical (x = 180.0 `[A]`,
   148.5 `[F]`). The count is exactly 28 `[A]` or 20 `[F]`, and the heights are visibly unequal. On
   that vertical there is no red within 48.8 mm of the baseline `[A]`, or within ±42.4 mm of the real
   axis `[F]`.
2. **RIGHT ANGLES THAT TILT.** At ρ₁, ρ₂ and ρ₄ the red arms meet at 90° ± 3°. The hairline (Im) arm
   leans at −9°, +13° and +31° respectively from horizontal. The tilts differ; the right angle does not.
3. **NOT A MIRROR.** Right of the column there are only hairline rulings, flattening to a pitch of
   15.64 mm `[A]` or 13.60 mm `[F]`. The ink right of the column is ≤ 10 % of the ink left of it
   (measure from the gcode). `[F]`: the lower half is the exact reflection of the upper half across
   the real axis.
4. **NO OTHER MEETINGS.** Black and hairline never touch anywhere except at the red crosses and on
   the real axis (trivial zeros at −2, −4, −6, … and s = 1). Some black tongues and hairlines do cross
   the column *alone* between crosses (half-Gram and Gram points), and they must be left visible.
5. **PLOTTABLE AND CLEAN.** A `.gcode` sits beside the png. There are 4 layers in the stated order
   with 2 swaps. The minimum spacing is ≥ 0.8 mm apart from the red joints. No type touches the comb.
   `[F]`: the footer shows distinct cliffs at 2, 3, 4, 5, 7, 8, 9, 11, 13 aligned over their numerals.
