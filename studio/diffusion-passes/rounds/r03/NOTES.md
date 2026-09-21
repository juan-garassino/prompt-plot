# THE LONG WAY BACK — diffusion-passes r03 (the ABSTRACT ORDER thesis)

## STATUS — v2 IS THE APPROVED VERSION

| | |
|---|---|
| **Approved render** | `~/Downloads/pp_diffusion_passes_abstract_v2.png` / `.gcode` |
| **Approved source** | **`studio/diffusion-passes/rounds/r03/piece_v2_APPROVED.py`** — frozen, do not edit |
| **Entry point** | `diffusion_passes(rng, bounds, colors=5)` |
| **Verified** | re-rendered to `~/Downloads/pp_diffusion_passes_abstract_v2_verify.png` |
| **Verification** | draw **13427.1 mm**, travel **15101.2 mm** (visualizer reports 15120.8 — it counts the home move my parser starts after), **18301 commands** |
| **Proof** | the two gcode bodies (everything past the provenance header) are **byte-identical**, md5 `fc682e0b75a1d0c193170f710a556b2b` |

Juan's verdict on v2: *"this is also supper good."* The original v2 png/gcode were
not touched.

`piece.py` in this folder holds the **unapproved** v3–v5 exploration that ran on
after v2 was already approved. It is NOT the shipped artefact. Everything in it
is described under "Proposals" below; nothing from it has been folded into the
approved file.

**Render command (approved):**

```
.venv/bin/python scripts/render_candidate.py \
  studio/diffusion-passes/rounds/r03/piece_v2_APPROVED.py \
  --fn diffusion_passes --seed 7 --paper a3 --orientation landscape \
  --palette black,dodgerblue,mediumpurple,palevioletred,crimson \
  --out ~/Downloads/pp_diffusion_passes_abstract_v2_verify.png
```

---

## The abstract order

> **A RING OF TIME THAT FAILS TO CLOSE.** The plate is one annular crystal whose
> arc coordinate *is* diffusion time. It melts to an isotropic fog at the
> antipode and recrystallises back round to the seam — where it cannot meet
> itself, because the grain came back at a different angle. One straight chord
> crosses the void from seam to melt: the closed-form forward jump, the only
> shortcut on the sheet, and it goes one way only.

This is deliberately **not** the reference's three horizontal registers of
sampled states. The reference's *argument* is kept intact — a destruction that
is cheap and analytic, a reconstruction that is expensive and learned, and the
two being the same path in opposite directions — and transposed onto an order
the mechanism genuinely has: a **lattice-with-defects** wrapped into an
**annulus**, from the rubric's own vocabulary.

### Why this order carries the mechanism

| requirement | how the order carries it |
|---|---|
| **reversibility is the argument** | the two arcs are **mirror images about the chord**: equal arc-offset from the seam = equal *t*, on both sides. Reversibility is the plate's own symmetry, not a caption. It is enforced by construction — there is no way to draw it wrong. |
| **column registration** | becomes *reflection* registration, which is stronger: any line perpendicular to the chord crosses the same *t* twice. |
| **decay at the real schedule, late and fast** | one criterion, applied everywhere: structure of size ℓ is resolved while `√ᾱ·ℓ > 2·√(1−ᾱ)·σ`, i.e. while `SNR = ᾱ/(1−ᾱ) > (2σ/ℓ)²`. Each scale's death is a *threshold crossing of a Gaussian tail*, so it is late and fast by mathematics, not by eyeballing. Measured crossings, cosine schedule (s = 0.008): **ℓ=a/3 at u 0.247 (ᾱ 0.850) · ℓ=a at u 0.570 (ᾱ 0.386) · ℓ=2a at u 0.758 (ᾱ 0.136) · ℓ=3a at u 0.834 (ᾱ 0.065)**. |
| **isotropic end state** | sites are transported by the real DDPM map `x_t = √ᾱ·x₀ + √(1−ᾱ)·σ·ε` with **isotropic 2-D noise in the local (radial, tangential) frame**, so at *t*=T every particle is an independent round Gaussian blob with no preferred direction. |
| **a bottleneck the reconstruction must pass through** | the `√ᾱ` contraction collapses the rows onto the centreline, so the 54 mm band **pinches to a ~14 mm filament** at the melt. The prior is drawn as its own level sets — nine concentric circles at 0.5σ pitch out to 2.5σ — which is a **17.8 mm disc against a 254 mm ring**, the smallest object on the sheet and the only true circle on it (a circle *because* 𝒩(0,I) is isotropic). |
| **the reverse is a different sample, not a rewind** | the recrystallised half is a genuinely **rotated lattice, grain tilt θ = 37.4°**. The two crystals abut at the seam and do not fit. That mismatch is the entire "different sample" claim, in one angle. Annealing from a melt really does pick a fresh orientation — the melt has forgotten which way the crystal faced. |
| **cheap-analytic vs expensive-learned** | mark vocabulary, not labels. The forward half is **ruled**: whole lattice rows drawn as single continuous polylines, one pass, no cost. The reverse half is **stitched**: every bond is a discrete dash, and each free atom is a tiny *oriented step* rather than a point. You can see the return was crawled. |
| **the learned reversal** | deliberately **not drawn as apparatus.** No U-Net, no bowtie, no skip arcs — that is the schematic the rubric bans outright (dim. 6). The learned part shows up as the *asymmetry of cost*: the forward side has a chord (one evaluation, any *t* in one jump) and the reverse side has no chord at all. That absence is the argument, and the void's reverse half is labelled `NO CHORD HERE`. |

**The twist.** The viewer already holds "diffusion" as the word for heat
spreading and things mixing *irreversibly*. The plate shows entropy rising and
then, impossibly, falling — and you can see it was not a rewind, because the
crystal came back crooked. The chord is the punchline: the shortcut exists in
one direction only.

### Colour — justified, and not merely a *t* ramp

The brief flags this piece as the one place a pen ramp is a *variable*. I kept a
continuous *t* ramp but tied it to something harder: **the pen changes exactly at
a threshold crossing of the resolution criterion.** The pen therefore names *the
finest structural scale still resolved* — black while the a/3 hatch lives, blue
while the cell lives, purple at the row-pair scale, pink at the band scale,
crimson once nothing is resolved. Four boundaries, four numbers, all printed on
the sheet.

The second job the ramp does is the one that decided it: **colour is the only
quantity on this plate that is symmetric about the chord.** Geometry is not. The
eye reads *"same schedule"* from the colour mirror and *"different sample"* from
the broken geometry, in a single glance. A categorical palette could not do that.

### Style canon

**RUSSIAN CONSTRUCTIVISM** (STYLES.md §8), committed to deliberately — the
collection needs to span canons and the reference sits in quiet drafting.
Constructivism's order is *diagonal thrust*, and this mechanism has exactly one:

- the **chord** is simultaneously (a) the closed-form jump, (b) the axis of
  time-reversal symmetry and (c) the driving diagonal. Three lines collapsing to
  one as they cross the void = information going away. Its last 26 mm arrive as
  mass (`fat_outline`) landing in the prior.
- **display type as mass**, flush-left on one column grid line (`THE / LONG /
  WAY / BACK` at 24 mm with 1.1 mm weight), plus one line set *along* the
  diagonal (`ONE EVALUATION`), which is the canon's signature move.
- a **heavy black keyline at the defect** — the grain boundary bar across the
  band at the seam.
- **one scarce, loud accent**: crimson, spent only on the melt (0.83 m of 13.43 m).

Paper: **A3 landscape**, as the brief's starting point. The order wants it — the
ring is 254 mm across and the mirror axis runs at −37°, so the sheet has to be
wide enough to give the ring a 242 mm field *and* a 112 mm type column beside it
without the two touching. Portrait would have forced the ring smaller than the
type block and lost the hierarchy.

### What was deliberately avoided

Read first, then ruled out:

- `studio/diffusion/rounds/r01` ("FORM FROM NOISE") — a **vertical stack of
  warped probability-flow planes** funnelling to a waist, sampler paths as
  columns. Avoided: no stacked planes, no funnel, no vertical composition.
- `studio/diffusion-topography/rounds/r01` ("DIFFUSION AS TOPOGRAPHY") — a
  **scattered constellation of contour blobs** joined by flow arcs, i.e. a
  node-and-link map of contoured fields. Avoided: no contour nests, no blobs, no
  arcs between islands.
- the reference itself — **three horizontal registers** of sampled states with a
  bowtie U-Net between them. Avoided entirely; there is no register and no
  U-Net on this sheet.

No primitive or generator from the kit does the subject work here: the lattice,
the melt transport, the bond-survival rule, the grain tilt, the chord and the
prior's level sets are all written from scratch in the piece. Only furniture
(`giant_type`, `fat_outline`, `concentric_disc`, `dotted_circle`, `fill_rect`,
`plus_mark`, `_stroke_text`) comes from `engine/kit.py`.

---

## Plot budget (approved v2, A3 landscape, seed 7)

| pen | colour | draw | pen cycles |
|---|---|---:|---:|
| 0 | black | 10.39 m | 1319 |
| 1 | dodgerblue | 1.55 m | 521 |
| 2 | mediumpurple | 0.48 m | 271 |
| 3 | palevioletred | 0.18 m | 120 |
| 4 | crimson | 0.83 m | 344 |
| | **total** | **13.43 m** | **2575** |

Travel 15.10 m · 18301 commands · **5 pen swaps** (the brief's ramp; above the
rubric's usual 3–4, and the brief overrides here because the ramp is a variable).
Extent x 13.8–407.0, y 11.8–285.2 against a drawable 10–410 / 10–287 —
**zero bounds violations**, ~3.8 mm of margin on the tightest edge.

Seeded-deterministic: all randomness goes through the passed `SeededRNG`
(`gauss`, `uniform`); same seed → identical gcode, as the byte-identical
re-render proves.

**Before plotting:** trace the pen-up frame first (`promptplot plot frame
--paper a3:landscape`), per the standing rule. Note the sheet is A3 — Leo is
set up for A5 landscape, so this needs the larger bed or a re-render at
`--paper a5 --orientation landscape` (the piece scales through `SC` and stays
in bounds at any sheet).

---

## Round log

| round | render | what changed |
|---|---|---|
| v1 | `pp_diffusion_passes_abstract_v1.png` | first build of the order: annular lattice, DDPM transport, grain tilt, chord, ruled/stitched split, giant type. **146 bounds violations**; caption blocks overran into the ring; the melt was a diffuse scatter with no focus; a `>` glyph the stroke font does not have. |
| **v2** | **`pp_diffusion_passes_abstract_v2.png` — APPROVED** | **(1)** the prior redrawn as its own level sets — a 17.8 mm crimson bullseye at the antipode with the chord's heavy 26 mm landing on it, which is what finally made the bottleneck a focal point rather than a thin patch. **(2)** column width budgeted at 112 mm and enforced in code (`col()` logs an overflow), captions switched to unspaced type so the lines fit — all text/ring collisions gone. **(3)** ring labels moved off the right margin into the void, where the chord divides it in two and each half gets the tag that belongs to it. **(4)** `ONE EVALUATION` reset along the chord as display type at the diagonal's angle. **(5)** bounds violations 146 → **0**; diagnostics added (per-side site/bond/atom counts, extent, draw). |

Four rounds were asked for; v2 was approved at round two and the loop was
stopped there by the coordinator. Rounds v3–v5 below were already rendered
before that instruction arrived and are recorded as proposals only.

---

## Proposals for a later round — NOT in the approved file

These live in `piece.py` (v5 state) and are visible in
`~/Downloads/pp_diffusion_passes_abstract_v3/v4/v5.png`. **Juan decides.** None
of it has been merged into `piece_v2_APPROVED.py`.

### Strictly bug fixes (still left out of the approved file)

1. **Three label collisions that v2 still has.** `t 0. DATA / GRAIN BOUNDARY`
   sits on the chord's triple line at its right end; `ONE EVALUATION`'s first
   word starts inside the black crystal instead of past the band; the diagonal
   type sits on the reverse side of the chord rather than the forward side.
   These are collisions, not design choices — by the rubric's own blunt test,
   nudging them a few millimetres would relieve the crowding and nothing would
   be lost. v5 fixes all three (`t 0. DATA` moved clear of both crystal and
   mirror axis, `anc = void(56, 8.5)`, type height 6.6 → 5.6 mm so it stops
   short of the prior). I am flagging them as bug fixes and leaving them alone
   anyway, as instructed.

### Design changes (genuinely open questions, not obviously better)

2. **The lattice coarsens instead of just dissolving** (v3). The ladder says the
   2a and 3a orders outlive the a order, so bonds are attempted at ranges a, 2a,
   3a on proper k-super-lattices; when the fine bond breaks the coarse one
   carries the order. Intent: fill the purple/pink stretch — 43% of each arc in
   v2 — with real coarsening structure instead of loose debris, which is both
   truer (coarse-to-fine is *the* fact about diffusion) and denser.
   **Status: not working yet.** Gating the coarse orders on the deterministic
   ladder (v5) collapsed them to 7 / 2 bonds per side, so the purple and pink
   zones came out *emptier* than v2, not fuller. Ungated (v4) they fire as stray
   long chords across the fine crystal, which reads as error. Needs a third
   approach before it is worth showing.
3. **Lattice constant 9.0 → 7.0 mm** (v4), band 54 → 42 mm, σ 3.57 → 2.78 mm.
   Raises particle density ~2.5× and makes the ring read as a continuous band at
   3 m. Cost: 22513 commands vs 18301, and a thinner band.
4. **Four atoms per cell instead of three** (v4) — denser fog.
5. **Radial a-bonds merged into column runs** (v5) — the forward crystal reads
   as a true grid rather than a ladder, and it saves ~500 pen cycles.
6. **Reverse dashes lengthened 0.56 → 0.84, hatch shortened 0.60 → 0.42** (v5).
   This is the one change I would argue hardest for: in v2 the recrystallised
   half reads as a *hatch field*, not as the same crystal at another angle, which
   weakens the "same family, different sample" claim. In v5 it reads as a tilted
   grid of closed cells and the grain tilt is unmistakable.

---

## Honest critique — the weakest part of the approved plate

**The purple and pink stretch of the ring is filler.** Between `u` 0.570 and
0.834 — about 43% of each arc, roughly 95° of the ring — nothing is drawn but
scattered points and a few surviving dashes, because the only structures the
piece knows how to draw (a-scale bonds and a/3 hatch) are already dead there.
The mechanism says coarse order survives into that window, and the plate does
not show it. Two pens are spent on 0.66 m of ink between them, and a viewer at
one metre reads that quadrant as debris rather than as *partially melted*. It is
the one stretch where the plate stops arguing and just decorates. Proposal 2
above is the attempted fix and it does not work yet.

Runner-up: the ruled-vs-stitched distinction is a 30 cm read at best. At one
metre the forward and reverse halves look like the same material, and the whole
cheap-vs-expensive half of the argument rests on the chord and on two small tags.
If it had to be carried louder, the honest move would be to make the reverse
half's stitch *count* visible — one dash per drawn step, counted and printed —
rather than relying on dash length.

Third: five pen swaps. The brief asks for the ramp and the ramp earns its keep,
but palevioletred does 0.18 m of work for a whole pen change, which is a poor
trade on the plotter.
