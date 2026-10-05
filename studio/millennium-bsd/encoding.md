# millennium-bsd — encoding (VISUAL TRANSLATOR)   · Status: encoding v1 · 2026-09-28

Source of truth: `studio/millennium-bsd/dossier.md` v1, visual truth **(a) ZERO MEANS INFINITY**
(rank 1). Truth (b) (EDSAC Euler product) and truth (c) (rank ladder) are **not drawn**. Data:
`data/curve_37a1.json` (±nP for n ≤ 30, e_i, Ω, θ, ĥ, L on [0,2]) and `data/lfun_lib.py`.
[A] needs the orbit to ±61. Recompute it with the exact `add()` in `data/verify_bsd.py`
(Fractions, < 1 s). Reference: `ref/reference.png`, an AI poster. It is an interpretation brief
and is never traced (`studio/AUTHORING.md`). No BRIEF.md, FEEDBACK.md or LEDGER.md exists yet.
This is plate 7 of the MILLENNIUM series. Two theses are built in parallel: **faithful [F]** and
**abstract [A]**. Every rule binds both unless the line says `[F]` or `[A]`.

**Translator's measurements** (2026-09-28, scratch only, from the exact orbit): the pencil
through P has a minimum angular gap of 11.31° for chords 1–7, 0.907° by chord 30 and 0.307° by
chord 100. Chords never enter the branch's mouth, because every chord ends on the branch at its
third point R and R has the largest x on the chord. The half-plane x < 0 outside the egg holds
**no chord ink at all**, because the egg is convex and every chord runs Q → P → R or P → Q → R
with Q on the egg. Those two facts fix the composition.

---

## 1. STYLE assignment

**A stated hybrid: an ART DECO sheet (canon 2) carrying a Morellet system. Gold | black on cream,
which is Deco's own palette and the series' gold accent.**

Why Deco fits the ORDER. Deco's signature move is the **radiating line fan** with exact ray
spacing. The group law of E *is* a fan. Every rational point on the sheet is ruled by a straight
line through one point, P = (0, 0), so the whole of E(ℚ) is a sunburst with a gold hub. Deco
demands exact spacing, and here the spacing is exact: it is not even but **quasi-periodic**. It
is set by an irrational rotation (θ = 0.378917 turns per 2P, the three-gap rhythm), so no two
gaps repeat by eye and none is decorative. Deco also allows **symmetric monumentality**. E is
mirror-symmetric about y = −½, and the generator sits *off* that mirror, so the one fan breaks the
symmetry. Deco's **stepped ziggurat outline** becomes, in [A], the ragged edge of the digit block:
line n is as long as x(nP), which grows as n²·ĥ. Deco's **thin/thick alternation via passes**
carries arithmetic height (see §4). Nothing Deco-shaped is added for its look: no sunburst behind
the title, no stepped border, no chevron band (§9).

**Flatness is declared.** Deco sunbursts are flat. The mathematics demands flatness too: the
crossing angle 17.014° and the collinearity of every chord with P hold only in one isotropic flat
plane. Any tilt, perspective or depth fall-off would bend the claim.

**LINEAGE:** `lineage: François Morellet, Répartition aléatoire de 40 000 carrés suivant les
chiffres pairs et impairs d'un annuaire de téléphone (1961; 50 % / 50 %, two colours). Order taken:
a number sequence's PARITY decides which of two families each mark joins, and the maker adds no
taste. Here n odd puts nP on the closed oval and n even puts it on the open branch, and the root
number ε = (−1)^rank = −1 forces the L-function to cross zero.` Not his look (squares), his rule.
Sources are in dossier §3. Batch check: Riemann answers LeWitt, Navier–Stokes Riley, P vs NP Mohr,
Hodge Gabo and Yang–Mills Kandinsky. Poincaré's candidates are Vasarely and Molnár. Morellet is
free. Navier–Stokes rejected Deco *because* its flow runs into an axis, not out of a point. Here
the flow does run out of a point, so the canons do not collide.

## 2. The one-glance statement

> **One gold point rules every line on the sheet. Where the lines stop is where the rational
> points are, infinitely many of them. Beside the fan, one line crosses zero once, in gold.**

- **3 m** `[A]`: a black sunburst radiates from a gold disc left of centre. Its rays stop sharp
  on a closed oval (left) and on an open "<" curve (right), or they run off the top and bottom of
  the sheet. To the right, in the empty mouth of the "<", a single line crosses a hairline once,
  and that stretch is gold. A stepped block of numerals climbs the bottom-left corner.
- **3 m** `[F]`: the reference's picture, true. There is a curve in two pieces, three straight
  lines through a gold point, and small open circles that crowd on the oval's right end. To the
  right sits a curve that dips below its axis and crosses it (gold) instead of bouncing.
- **1 m**: the rays have three weights, heavy to hair, and the heavy ones reach closest to the
  hub. The oval and the "<" are mirror images about a line that is never drawn on the curve side.
  The gold crossing lies on that same line, continued.
- **30 cm**: the digits of x(nP) lengthen line by line (1, 1, 2, 1, 3, 1, 4, 5, 6 … 41 characters).
  A caption gives the bridge: `SLOPE AT THE CROSSING 0.30600 = 5.98692 × 0.05111`.

## 3. The abstract ORDER

**RADIAL seeded ORBITAL.** A pencil of lines through one point. Each line carries the orbit one
step, and the orbit falls onto two circles by parity, turning by an irrational angle. The analysis
is one line hinged on the same axis.

Exact mappings, one line each:
- "**Every line passes through the gold point. Every place a line meets the curve is a rational
  point. There are no other marks for points.**" `[A]`
- "**Odd multiples fall on the oval, even ones on the open branch. Position carries parity, so no
  colour does.**"
- "**The s-axis is the curve's own mirror line y = −½, continued into the branch's mouth. One mm
  scale serves x, y, s and L, so the gold crossing leans at 17.0°.**"

This names no object and no plot. The only graph-like element is the L-curve, and it carries no
vertical axis, no ticks and no arrows. It lives inside the curve's plane, on the curve's mirror.

## 4. Channel mapping (Tufte: nothing drawn that encodes nothing)

Plane → sheet (both theses, A3 portrait, y up from the bottom edge): **S = 52 mm per unit on
both axes.** sheet_x = 30 + (x − e₃)·52 and sheet_y = 200 + (y + ½)·52, with e₃ = −1.1071599.
The mirror y = −½ therefore sits at sheet y = 200.

| ink | encodes | exact rule / range |
|---|---|---|
| **real locus E(ℝ)**, black 0.5, 1 pass | the egg (closed, x ∈ [e₃, e₂]) and the branch (open, x ≥ e₁) of y² + y = x³ − x | Parametrise by y = (−1 ± √(4x³−4x+1))/2 with dense sampling at the tips (vertical tangents). The egg spans sheet (30…101.6) × (158.6…241.4). The branch vertex is at (131.1, 200). The upper arm leaves the field top crop (y = 365) at x = 207.0, and the lower arm leaves the bottom frame at x = 215.4. **No curve ink for e₂ < x < e₁.** |
| **gold disc**, gold, concentric rings | P = (0, 0), the generator; rank 1 = one disc | Centre (87.6, 226.0). `kit.concentric_disc`, ring pitch 1.0 mm. `[A]` Ø 12 mm (6 rings); `[F]` Ø 8 mm (4 rings). The egg line is clipped at the disc edge + 0.8 mm, so it enters and leaves the disc like a bead on a string. |
| **chord** k (a straight line) | the group law: the line through P, kP and −(k+1)P (for k = 1, the tangent at P) | The segment spans exactly from its extreme intersection with E to R (the branch point), clipped to the field. It is **never extended past R** (never into the mouth) and never past the egg point. Points come from the exact orbit, never placed by eye. |
| chord **weight tier** `[A]` | arithmetic height: how simple the chord's two points are | **Heavy** k = 1–9 (points up to 10P; denominators ≤ 2 digits): black 0.3 × 2 passes offset 0.25 mm. **Medium** k = 10–24: black 0.3, 1 pass. **Fine** k = 25–60: black 0.1, 1 pass. This is the Deco thin/thick, and it thins as ĥ·n² grows. |
| chord **inner end** (hub LOD) `[A]` | the order of construction: later chords stop farther from P | Chord k starts at r_k = max(7.0, 0.8 mm / sin Δθ_k) from P, where Δθ_k is its smallest angle to any lower-index chord. The second pass of a heavy chord starts at max(7.0, 1.35 / sin Δθ_k). Measured: chords 1–7 reach 7 mm, then chord 8 → 8.8, 10 → 10.2, 11 → 16.6, 56 → 46.0, 59 → 47.6 mm. This is **structural de-crowding. No holes are punched.** |
| ray ends on the curve `[A]` | the rational points ±1…±61 (96 inside the field) | No circle and no tick. The meeting of a ray with E is the mark. −P = (0, −1) lies on no drawn chord (its line is vertical and meets O), so it is correctly unmarked. |
| **open circles** `[F]`, black 0.3, Ø 1.6 mm | the orbit ±nP, n ≤ 30 (48 inside the field) | Minimum centre separation is 3.99 mm. E is clipped inside each circle (+0.3 mm) so every circle reads open, as in the reference. **Stop at n = 30**: n = 31 brings a pair to 1.95 mm. |
| **construction** `[F]`: 3 chords (0.3) + 2 negation steps (hairline 0.1, vertical) | the reference's construction, corrected | Tangent y = −x: P (87.6, 226) → −2P (139.6, 174). Negation x = 1: −2P → 2P (139.6, 226). Chord y = 0: −3P (35.6, 226) → P → 2P. Negation x = −1: −3P → 3P (35.6, 174). Chord y = x: 3P → P → −4P (191.6, 330). The staircase stops there, and the caption continues it with "…". The x = 2 negation would cut the L-curve, so it is **not drawn**. |
| **L(E,s)**, black 0.5 (the same pen as E) | the L-function of 37a1 on the real segment s ∈ [0, 2] | L(sheet) = (152.6 + 52·s, 200 + 52·L(E,s)). That gives s = 0 at x_plane 1.25, one scale. Values come from `Lfun('37a1').L(s, −1)` at ≥ 200 samples. Anchors: L(0) = 0 at (152.6, 200); minimum −0.08924 at s = 0.478 → (177.4, 195.4); crossing (204.6, 200); L(1.5) = 0.18397 → (230.6, 209.6); L(2) = 0.38158 → (256.6, 219.8). L is drawn, **not Λ**. |
| **gold crossing** | the simple zero at s = 1 and its slope L′(1) = 0.3060 = Ω_E·ĥ | **Substitution, not overlay.** For s ∈ [0.85, 1.15] the L-curve is gold (2 passes, offset 0.3 mm), and black stops 0.3 mm inside each end. The gold stretch is ≈ 16.3 mm long at **17.01°**. No tangent line, no dot, no ring. |
| **s-axis**, black 0.1 hairline | Re s on [0, 2], laid on the mirror y = −½ | From (152.6, 200) to (256.6, 200), exactly s ∈ [0, 2]. It is **not continued** left toward the vertex: that would draw the mirror through the curve side and the gap. |
| **digit ziggurat** `[A]`, text layer, 1.6 mm caps, mono advance 1.49 mm | ĥ(P) = 0.0511: the digits of x(nP) grow as n² | One line per n = 1…30, top to bottom, flush-left at x = 22 with a right-aligned 2-digit index column at x = 15–19.5. Each line is the exact x(nP) string ("0", "1", "-1", "2", "1/4", "6", "-5/9", "21/25", … "79799551268268089761/62586636021357187216"). Lengths are 1,1,2,1,3,1,4,5,6,6,7,8,10,11,10,11,15,17,18,19,21,23,26,27,30,30,34,37,40,41. Leading 4.2 mm, top baseline y = 150, bottom y = 28. The right edge peaks at x ≈ 83 (n = 30). Any ray must stay ≥ 8 mm away (the nearest lower ray crops the bottom at x = 94.8). If that fails, cap at n = 28 and state the cap. |
| type (text layer) | title, statement, rule, bridge, status | See §5. Type never sits on ink, except `[F]` point labels, which take halos over chords. |
| **not encoded (declared)** | Ш, Tamagawa numbers, torsion (all 1), Sato–Tate, EDSAC product, rank ladder, Λ, the three-gap lengths as marks | They are in captions at most, never as ink. |

## 5. Composition sketch — A3 portrait 297 × 420 mm, margins 15, y up from the bottom edge

Both theses share one frame: the curve, the L-curve, the gold marks and the crop lines sit at
identical coordinates, so the two renders are directly comparable. **Field** is x ∈ [15, 282],
y ∈ [15, 365], with a straight horizontal crop at y = 365 under the title band. Rays that leave
the field bleed to the crop and the bottom margin. That crop is honest, because the orbit runs off
to infinity.

**Grid.** There are two text columns: **left** x = 15 (to ≤ 84) and **right** x = 226 (to 282).
The baseline grid is 4.2 mm. The title band is y ∈ [372, 405].

- **Title** (both): flush-left x = 15, baseline 395, spaced caps 8 mm: `BIRCH AND SWINNERTON-DYER`
  (≈ 243 mm wide; break after AND if the spaced width exceeds 267). Statement at 2.5 mm caps,
  baseline 382:
  `[A]` `ONE POINT MAKES INFINITELY MANY. ITS L-FUNCTION CROSSES ZERO ONCE.`
  `[F]` `RANK E(Q) = ORDER OF VANISHING OF L(E,S) AT S = 1.`
- **Upper-left quiet block**, x ∈ [15, 80], y ∈ [255, 360]. It is chord-free by geometry (x_plane < 0,
  outside the egg).
  `[A]` the Morellet instruction, 1.8 mm caps, as a wall label: `EVERY LINE PASSES THROUGH THE
  GOLD POINT P = (0,0).` / `EVERY PLACE A LINE MEETS THE CURVE IS A RATIONAL POINT.` / `ODD
  MULTIPLES LAND ON THE OVAL, EVEN ONES ON THE OPEN BRANCH.` / `WEIGHT: HEAVY = SMALL NUMBERS.`
  `[F]` `E : Y² + Y = X³ − X`, 4 mm (the reference's label, kept) + `CREMONA 37A1 · CONDUCTOR 37`.
- **Bottom-left**, x ∈ [15, 80], y ∈ [25, 152].
  `[A]` the digit ziggurat (§4).
  `[F]` the reference's equation, flush-left, 4.5 mm: `RANK E(Q) = ORD  L(E,S)` with a 2.2 mm
  `S=1` subscript, baseline 60. Below it at 1.8 mm, the orbit's continuation: `6P = (6, 14)  7P =
  (-5/9, 8/27)  8P = (21/25, -69/125) …`, ragged, three lines.
- **Right column, bottom**, x ∈ [226, 282], y ∈ [20, 110], 1.8 mm caps, flush-left. It is clear of
  the lower arm (crop at x = 215.4) by ≥ 10 mm. The bridge:
  `L'(E,1) = 0.30600` / `= 5.98692 × 0.05111` / `= REAL PERIOD × HEIGHT OF P` / `(Ш = 1, C = 1, NO TORSION)`,
  then the status: `PROVED FOR THIS CURVE: GROSS–ZAGIER 1986, KOLYVAGIN 1988. OPEN IN GENERAL.`
  `[A]` adds: `ROOT NUMBER −1: THE COMPLETED L IS ODD ABOUT S = 1, SO IT CANNOT MISS ZERO.`
- **Right column, top**, x ∈ [212, 282], y ∈ [232, 362]: **empty in both.** This is the quiet zone
  that makes the gold crossing loud.
- **At the crossing:** `S = 1`, 1.6 mm, centred under (204.6, 200), baseline 193.
  `[F]` adds `0` and `2` under the axis ends, `L(E,S)` at 2.5 mm above-right of (256.6, 219.8), and
  `ONE CROSSING, NOT A TOUCH: ORDER 1` at 1.8 mm, baseline 180, flush-left x = 215. **No arrow.**
- `[F]` **point labels**, 1.8 mm, with halos over chords: `P (0,0)`, `2P (1,0)`, `-2P (1,-1)`,
  `3P (-1,-1)`, `-3P (-1,0)`, `-4P (2,2)`, `4P (2,-3)`, `5P (1/4,-5/8)`. Each sits on the side of
  its point **away from P**. None goes in the gap (x_plane 0.27–0.84) and none at a tip.
- **Dominant mass:** the fan plus the curve. `[A]` x ∈ [30, 216], y ∈ [15, 365], ≈ 65 000 mm², with
  ≈ 9.2 m of ink (rays + E). The next mass, the L-curve (104 × 25 mm), is more than 20 : 1 smaller.
  `[F]` has the same frame but less ink, and dominance comes from E and the three-chord asterisk
  through the gold point (0°, 45°, −45°).
- **Quiet zones:** the right column above L (~70 × 130 mm), the mouth between the arms, the upper-left
  block's margins, and the 21.5 mm of bare mirror between the branch vertex and s = 0.
- **Diagonals:** the fan supplies them. The one analytic diagonal is the gold 17°.
- **Reference → faithful mapping `[F]`:**

  | reference shows | [F] draws |
  |---|---|
  | one connected wiggly curve dipping to join the branch | egg + branch, a gap of 29.5 mm on the mirror with no curve ink |
  | mirror implied at y = 0; x- and y-axes with arrows | no axes. The mirror y = −½ appears only as the s-axis. |
  | points (1,1), (1,−2) (not on E) | −4P (2,2), 4P (2,−3), 2P (1,0), −2P (1,−1): all on E |
  | chord through (−1,0),(0,−1),(1,−2) | the pencil through P: y = 0, y = x, and the tangent y = −x |
  | vertical (1,1)–(1,−2) | the negation x = 1 from (1,−1) to (1,0), bisected by the mirror, plus x = −1 |
  | "(−1, 0)" at the egg's leftmost point | −3P = (−1, 0) sits 5.6 mm right of and 26 mm above the real tip (e₃, −½); the tip carries no label |
  | gold threads fanned from (1,1) to the zero | **cut** (lie 6). The bridge is the shared mirror/s-axis and the caption Ω × ĥ. |
  | L large at s = 0, V-bounce at 1 | L(0) = 0, negative dip, transversal gold crossing at 17.0°, rising to 0.38 |
  | "simple zero (order 1)" with an arrow | `ONE CROSSING, NOT A TOUCH: ORDER 1`, no arrow |
  | centred title, gold rule ornaments | flush-left title (series), rule ornaments cut |

## 6. Pen budget — 3 blacks + gold, 5 layers, 3 swaps (layer discipline, no cap)

| order | layer | physical pen | meaning |
|---|---|---|---|
| 1 | HAIR | black 0.1 fineliner | `[A]` fine chords k = 25–60; the s-axis. `[F]` the 2 negation steps; the s-axis. |
| 2 | CHORDS | black 0.3 | `[A]` medium chords + heavy chords (2 passes). `[F]` the 3 chords + 48 open circles. |
| 3 | TEXT | the same black 0.3, own layer, **no swap** | all type. `[A]` includes the digit ziggurat. |
| 4 | CURVES | black 0.5 | E(ℝ) and L(E,s): the two objects of the conjecture, one weight |
| 5 | GOLD | gold 0.7 (metallic gel / paint marker) | P and the crossing, and nothing else |

The order is light to dark and gold goes last. The 0.5 curves land after the rays, so each ray end
sits under the curve line (tiny overshoots are hidden). Gold sits on top of everything. Gold is
< 0.5 % of the ink, so it is scarce and loud. There are 3 swaps.

## 7. Expressive levers (one decision each)

- **Proportion.** Fan to L-curve is > 20 : 1 by area. The loudest small thing (the gold crossing)
  sits in the emptiest place.
- **Fill vs void.** There are three silences, each a truth. The half-plane left of P holds no chord
  (convexity). The mouth holds no chord (R is extreme). The gap holds no curve (two components).
  None is filled for balance.
- **Density gradient.** Only the orbit's own. Rays crowd where the invariant measure ds/|∇F|
  is high (the egg's right tip, 1.279) and thin up the branch (0.009 at (6,14)). The hub LOD rings
  thin inward. There is no cosmetic ramp.
- **Colour play.** One gold, twice: the cause (P) and the witness (the zero). The weight tiers are
  black at three nibs, not three colours.
- **Texture direction.** Every stroke direction is forced: radial from P, along E, along L, and
  horizontal in the type. The ziggurat's horizontal lines run cross-grain to the near-vertical rays
  beside them. That tension is kept.

## 8. The twist

**What the viewer holds:** "zero means nothing", and the picture of 0 as an **empty oval**.

**What the mechanism breaks:** the oval on this sheet is a 0 that is **full**. It holds half of
infinitely many rational points (every odd multiple, dense in it). The one place the analysis says
"zero" is gold *because* of that infinity: L vanishes at s = 1 exactly because P never comes back.
The second joke is in the caption for [A]. The root number −1 makes the completed L odd about s = 1,
so the line **cannot avoid** crossing. Parity said "odd rank" before a single point was found.
That is Morellet's rule (parity picks the family) played by the functional equation itself.

## 9. Forbidden list (binding on both; the science critic fails any of these)

1. **Any marked point not on E.** In particular (1,1), (1,−2), and "(−1,0)" labelled as the egg's
   tip. Every coordinate comes from the exact orbit.
2. **Joining the components:** no curve ink, mirror line, tick or label for e₂ < x < e₁. Chords
   crossing that band are allowed (they are lines, not the curve).
3. **Symmetry about y = 0**, horizontal x-/y-axes, or a mirror line drawn through the curve side.
4. **L misdrawn:** L(0) ≠ 0, L positive on (0,1), a V, a cusp, a bounce or any corner at s = 1,
   an independently scaled vertical axis (the 17.0° claim is on the plate), or Λ swapped in.
5. **Decorative gold.** Gold on anything but P and the crossing stretch: no gold threads, no gold
   rules, no gold type, no tangent line.
6. **Chords past the curve:** no line extended beyond R into the mouth or beyond the egg point, no
   second pencil (none through −P), no envelopes, rulings or string-art curves (Hodge collision).
7. **Evenly spaced anything:** evenly spaced rays or beads, a closed orbit polygon, n-fold symmetry.
8. **A spider-web hub.** All rays reaching P floods it. The LOD rule of §4 is the only hub rule.
9. **Axes with arrows, tick marks, grid lines, frame boxes, a vertical L-axis, insets, arrows of any
   kind** (the reference's "simple zero" arrow included).
10. **Hatch or tone under L**, or anywhere. The plate has no fill except the gold disc.
11. **Deco ornament that carries nothing:** sunbursts behind type, stepped borders, chevrons, the
    reference's gold rule-and-dot dividers.
12. **False text:** `L(E,1) = Σ aₙ/n`, "rank = number of points", or BSD stated as proved in general.
13. **Type over rays** (only `[F]` labels, with halos). No type larger than the title and no giant
    "0".
14. The EDSAC product, the rank ladder or Sato–Tate as ink. They are not this plate.

## 10. Fabrication

- **Data.** Orbit: extend `curve_37a1.json` to ±61 with the exact group law. Write to a **new**
  `data/orbit_61.json` and never overwrite. L: 200+ samples of `Lfun('37a1').L(s, −1)` on [0, 2]
  (≈ 1 s), taking s = 0 as exactly 0 (trivial zero).
- **Spacing floors.** Rays are held at ≥ 0.8 mm by the LOD rule, and at ≥ 1.35 mm centre-to-centre
  where a heavy (0.55 mm band) ray is involved. `[F]` circles have ≥ 2.4 mm gaps. The gold rings
  are at 1.0 mm pitch for a 0.7 nib. The first 7 chords converge at 7 mm with a smallest gap of
  11.31°, giving 1.37 mm there. Ray ends meet E at points whose separation is ≥ 1.4 mm (±61).
- **Draw length and time on A3** (Leo F600 ≈ 10 mm/s, ≈ 2 s per pen cycle incl. dwells):

  | layer | `[A]` | `[F]` |
  |---|---|---|
  | 1 HAIR 0.1 | fine rays 4.70 m + axis 0.10 m, ~55 strokes → **≈ 10 min** | 2 negations + axis 0.21 m, 3 strokes → **≈ 1 min** |
  | 2 CHORDS 0.3 | medium 2.35 m + heavy 1.38 m × 2, ~60 strokes → **≈ 11 min** | 3 chords 0.40 m + 48 circles 0.24 m → **≈ 3 min** |
  | 3 TEXT 0.3 | ≈ 870 chars (465 of them digits) ≈ 1 500 glyph strokes → **≈ 45 min** | ≈ 450 chars ≈ 800 strokes → **≈ 25 min** |
  | 4 CURVES 0.5 | E 0.63 m + L 0.11 m, 4 strokes → **≈ 2 min** | same, with E broken at 48 circles (≈ 52 strokes) → **≈ 3 min** |
  | 5 GOLD | disc 6 rings + stretch 2 × 16 mm → **≈ 2 min** | 4 rings + stretch → **≈ 2 min** |
  | **total** | **≈ 70 min, 3 swaps** | **≈ 34 min, 3 swaps** |

  The digit block is the one expensive run, and it earns its cycles: it *is* ĥ. If time must be
  cut, cap it at n = 24 (253 chars, the edge still reads as a parabola) and state the cap.
- **Batching.** Rays are sorted by angle around P, a clockwise sweep that alternates
  outward/inward. The longest ray is ≈ 260 mm, which is a valid batch boundary. Re-zero every
  ~20 strokes. Draw E as egg (1 closed stroke, broken at the disc) then branch (upper arm and lower
  arm as 2 strokes from the vertex outward). Order text by block: title → upper-left → ziggurat
  top-down → right column. There is no sheet-crossing travel within a block.
- **Flood risks.** The hub (handled by LOD + disc). The egg's right tip (densest measure, where
  rays converge from P at 31 mm range: LOD covers it). The gold 2-pass stretch (0.3 offset for a
  0.7 nib is intended as a band, ≤ 16 mm long).
- **Missing glyphs** (author them or rephrase): ℚ (write `Q` or author double-struck), Ω (write
  `REAL PERIOD`), ′ (use `'`), ° (write `DEG`), – and — (use `-`), … (use `...`), Ш (author it, or
  write `SHA`), − (use `-`). Available: ² ³ · × ≤ ε θ π Σ √ ∞ = ( ) / :.
- **Other papers.** A3 portrait is the design sheet. **Confirm with Juan that Leo takes A3.** An A4
  edition is a uniform ×0.707, except that the LOD is **recomputed** at 0.8 mm (not scaled) and the
  ziggurat caps at n = 26 at 1.4 mm. A5 is a re-run and never a scale-down: K = 30, the ziggurat
  at n ≤ 20, `[F]` circles to n ≤ 20. The pen-up frame trace comes first (house law).

## 11. Acceptance checks (the art critic marks each PASS/FAIL on the png)

1. **ONE HUB, RECEDING.** Every ray, extended, passes within ±0.3 mm of the gold disc's centre
   (87.6, 226). No ray enters the disc. `[A]` Exactly chords 1–7 reach the 7 mm
   hub circle. Later chords start visibly farther out (e.g. one at ≈ 16.6 mm, two at ≈ 46–48 mm).
   Heavy rays reach closer than fine ones, and there are 3 weights.
2. **TWO PIECES, ONE MIRROR.** The egg is closed and the branch open. The egg's right tip
   (101.6, 200) and the branch vertex (131.1, 200) are 29.5 mm apart, with no curve, axis or label
   between them. The egg's top and bottom (241.4 / 158.6) are symmetric about y = 200, **not** about
   the hub's height 226.
3. **LINES STOP ON THE CURVE.** Every ray ends on the egg, on the branch or at the crop. Inside the
   mouth (right of the branch) there is nothing but L, its axis and type. Left of the hub, outside
   the egg, there is no ray. `[F]` Exactly 3 chords at 0°, 45° and −45° through the disc, and 48
   open circles.
4. **ONE CROSSING, NOT A TOUCH.** L starts on the axis at (152.6, 200), dips 4.6 mm below it
   around x = 177, crosses at (204.6, 200) in gold at 17.0° ± 0.5°, and ends 19.8 mm above the axis
   at x = 256.6. There is no corner anywhere, and the gold is the only colour on the right half.
5. **PLOTTABLE, LAYERED, TRUE.** A `.gcode` sits beside the png, with 5 layers in the §6 order and
   3 swaps. The minimum spacing is ≥ 0.8 mm (from the gcode). No type touches a ray (`[F]` labels
   are halo'd). `[A]` The ziggurat's line lengths read 1…41 characters with a parabolic right edge
   ≤ x = 83, ≥ 8 mm clear of the nearest ray. Every labelled coordinate satisfies y² + y = x³ − x.
