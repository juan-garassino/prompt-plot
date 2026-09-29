# ATTENTION AS WEAVING — r01

Faithful recreation of `studio/attention-weaving/ref/reference.png` (1122×1402,
ratio 0.800), with the brief's explicit licence to fix the reference's crowding.

- **Piece**: `studio/attention-weaving/rounds/r01/piece.py`, entry `attention_weaving`
- **Render**: `gallery/studio/attention_weaving/current/pp_attention_weaving_faithful_v15.png` (+ `.gcode` beside it)
- **Paper**: `--paper 24x30` portrait. `PaperConfig.from_size` accepts it and reads
  it as centimetres → **240 × 300 mm**, drawable 220 × 280 mm, i.e. exactly 0.800.
  No fallback to A3 was needed.

```
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r01/piece.py \
  --fn attention_weaving --seed 7 --paper 24x30 --orientation portrait \
  --palette black,crimson,dodgerblue,goldenrod,darkgreen \
  --out gallery/studio/attention_weaving/current/pp_attention_weaving_faithful_v15.png
```

`--colors` defaults to the palette length, so the piece is called with 5 pens.
Verified deterministic: two runs at seed 7 produce byte-identical command lists.

## Pens

| pen | colour | carries |
|---|---|---|
| 0 | black | title, labels, the softmax bead grid, the dotted compass/rule scaffold, margin dots |
| 1 | crimson | **Q** — 12 filaments, top-left reed → the weave → the waist |
| 2 | dodgerblue | **K** — 12 filaments, top-right reed → the weave → the waist |
| 3 | goldenrod | **V** — 12 filaments, mid-left reed → the merge below the waist |
| 4 | darkgreen | **Z = AV** — all 36 filaments from the moment they are Z, → the exit reed |

A filament changes pen; it does not stop. Q is crimson until it leaves the bead
block and darkgreen after, because that is where `A` is born. V is goldenrod
until it reaches the rope and darkgreen after, because that is where `AV` is.
Cream paper is the sixth colour and holds the two voids.

## Plot budget

| | |
|---|---|
| commands | 30,293 |
| pen-down cycles | 1,548 |
| draw | 12.71 m |
| travel | 15.07 m (1.19 × draw) |
| pens | 5 |
| ink bbox | x 17.0…223.0, y 20.7…273.4 mm |
| clear of the sheet edge | 17.0 left / 17.0 right / 20.7 bottom / 26.6 top |
| est. on Leo (F600 draw, F2000 travel, 1 s dwells) | ≈ 80 min |

Travel is high relative to draw because a weave is, by construction, thousands
of short runs: mean drawn run is 8.2 mm. The optimiser is doing its job — mean
travel per lift is 9.7 mm.

## How over/under is implemented

Everything on the sheet is a polyline in one list, and one pass resolves every
crossing in it.

1. **Detection.** Every polyline is resampled to a uniform 0.80 mm step. All
   segments go into a 2.6 mm bucket grid keyed on their midpoint; because a
   segment is shorter than a bucket, two intersecting segments always land in
   the same or an adjacent bucket, so visiting 5 of the 9 neighbour offsets
   tests every pair **exactly once**. Intersections are the closed-form
   segment/segment solve, vectorised per bucket with numpy.

2. **Who wins.** Three rules, in order:
   - **anything beats scaffold** — the compass circles, the bead-strung rules
     and the waist's horizontal rule always break, so they read as *behind*.
     They are generated as continuous polylines, broken at crossings, and
     dashed afterwards, so the dash rhythm stays regular and only the gaps say
     "behind";
   - **a Q–K crossing inside the weave is decided by `sign(S[i, j])`**, where
     `S = QKᵀ/√d` is the pre-softmax score matrix. Positive similarity floats.
     This is `bauhaus_loom`'s rule (sign → over/under) moved from a weight
     matrix to a score matrix, and like a plain weave it is deliberately not
     globally 3D-consistent — that is what makes it a *weave*;
   - **everything else by projected depth.** In the rope that depth is real:
     `dep = R(s)·sin(θ₀_ply + Ω(s))`, the third coordinate of a filament on a
     helix about the spine. In the upper bundles it is the quadrature of the
     travelling wave each bundle rides.

3. **The break.** The loser gets an arclength interval `[l−g, l+g]` removed,
   with `g = clamp(0.55/sin θ, 0.55, 2.4) mm` — the gap widens at shallow
   crossings so the break still reads, but is capped, because uncapped a 10°
   crossing opened a 5 mm hole and the weave turned to dashes. Intervals on one
   filament are merged before cutting, so a cluster of crossings makes one clean
   opening rather than a stipple.

4. **Solid marks** (the softmax beads, the filled registration dots) are the one
   thing in front of everything. They are cut with `geometry.clip` against a
   `Circle` region, which is exact: the filament stops **on** the disc, not on
   the nearest sample. Beads open 0.72 mm of clear paper — at 0.42 mm (v2) the
   waist read as a barcode with dots on it. Open circles do **not** cut, because
   in the reference the filament is visible running through them.

5. **Type** is protected the same way: the type boxes are built before the
   scaffold and `geometry.clip`ed out of it. In the reference the top compass
   circle runs straight through the title; in v2 of this piece it printed as
   `ATTENTION--AS--WEAVING`.

### Does it hold? — the audit

Run at seed 7 (the `AUDIT` dict is filled by every call):

| | |
|---|---|
| crossings found | 2,535 |
| filament–filament | 1,964 → **1,964 breaks, exactly one per crossing** |
| of which Q–K (decided by `sign S`) | 800 |
| Q–Q / K–K / V–V (decided by depth) | 2 / 80 / 50 |
| Q–V / K–V (depth) | 432 / 600 |
| scaffold vs filament | 543 → 543 scaffold breaks |
| scaffold vs scaffold | 28 → left alone (both are dotted) |

`1964 + 543 = 2507 = breaks_total`. There is no crossing anywhere on the sheet
where both lines continue, and none where both break.

### Strand count in = strand count out

Asserted in `_strand_audit()`, which raises rather than warns:

```
filaments built            36   (12 Q + 12 K + 12 V)
entering at a margin       36
leaving at the right margin 36
```

Each filament is a single polyline from its entry tick to its exit tick. Nothing
is born below the waist and nothing dies above it. The 24 Q/K filaments each own
one of the 24 throat slots and one of the 24 vertical lines through the bead
block; the 12 V filaments join the rope below it. Exit ranks are assigned by
sorting the filaments' lateral position at the fan hand-off, so the exit reed is
in the order the rope actually delivers them and the fan adds zero crossings.

## Craft — measured clearance

Nearest-neighbour distance from every drawn point to a **different stroke of the
same pen**, counting only pairs within 15° of parallel (so genuine side-by-side
runs, not the transverse grazing every over/under necessarily has):

| pen | filaments | 1% | 5% | 10% | median | share under 0.80 mm |
|---|---|---|---|---|---|---|
| crimson Q | 12 | 0.54 | 1.26 | 1.41 | 2.46 | 1.4 % |
| blue K | 12 | 0.08 | 1.26 | 1.39 | 2.35 | 2.5 % |
| ochre V | 12 | 0.52 | 0.79 | 1.07 | 2.57 | 3.6 % |
| green Z | 36 | 0.27 | 0.63 | 0.77 | 1.05 | **10.5 %** |

The green number is the honest weak spot and it is structural, not a bug — see
"weakest part" below. It is sized for a 0.3 mm liner, not a 0.5 mm one.

One exact fix went in for it. A ply is a flat band of filaments whose centre
slides across the rope at lateral speed `v = |d lat/dl|`; its own filaments then
run oblique to the cross-section, so their **perpendicular** pitch is the pitch
you set divided by `√(1+v²)` — not the pitch you set. That, and not the ply
crossings, put 20 % of the rope under 0.8 mm in v7. Widening the band by
`√(1+v²)` (capped at 1.60) cancels it exactly and is also what a physical ply
does: constant apparent thickness. It took the green from 19.8 % to 10.5 %.

A second exact fix: `Ω` is pinned to 720° at the fan hand-off. Three plies at
θ₀ = 0/90/180 project to lat = −R, 0, +R exactly there — and `sin θ = 0` there
too, so the compensation is off and the bands are at their narrowest. It is the
one phase where all three bands are disjoint. Handing over at any other phase
freezes two plies on top of each other going the same way.

## Per-round changes

Fourteen renders. The numbered ones are the ones that changed the piece.

**v1** — first build. Ribbon bundles, funnel, bead block, 3-ply rope, unified
crossing resolver. Read: the shape was right and the over/under worked, but the
funnel mouth was a dead-straight horizontal bar (a ribbon with its normal at 0°
puts every filament on one scanline) so the weave ended in a flat-bottomed
mushroom; the rope was a sausage; the exit was a broom.

**v2** — `sag` added to the ribbon stations (`+sag·hw·λ²` in y), which bends the
reed into a parabola and gives the funnel an arc instead of a bar. Rope: R up,
w down, so the plies separate and read as three. Title tracking got a real word
space. Waist enlarged. Verdict: the rope became a braid; the funnel became a
pouch; the top compass circle was printing through the title.

**v3** — scaffold clipped out of the type boxes (type layout moved before the
scaffold so the boxes exist in time). Exit fan: freeze the plying at `S_FAN`
before blending to the comb — while the plies keep turning, their order keeps
swapping, and the fan (ordered by lat *at* `S_FAN`) then has to undo those
swaps, which is what made v2's reed a thicket. Waist widened to 1.25 mm pitch,
beads up to 1.15 mm, bead cut up to 0.72 mm, which killed the barcode read. Exit
reed given alternating dent lengths.

**v4–v5** — gap tuning. `GAP_MAX` 2.8 → 1.9 was too tight (the over/unders
stopped reading) and 2.4 with a 0.34 sine floor is the settled value. Rope
widened again and the twist re-profiled; the funnel's sag faded before the
throat so the filaments stopped ending in little loops.

**v6** — the freeze at `S_FAN` was itself a kink (C⁰ in the derivative); it is
now a smoothstep ramp over 0.05 of the rope. Spine tail lengthened and given a
shallow wave so the last 40 mm are not dead-straight. No scaffold dot may land
in a type box — one had been sitting exactly on the `·` of `Q · Kᵀ`.

**v7** — waist dropped 5 mm and the funnel given 27 mm to pinch in instead of
21, because all the crossings had been piling into the last 20 mm above the
throat. Bundle wave amplitude up to 0.25 λ (still under the swap threshold, so
no filament in a bundle crosses another in that bundle).

**v8–v12** — the spacing work described above: perpendicular-pitch
compensation, the `Ω`-phase pin at the fan, then three rounds finding the
balance between compensating the pitch (which fattens the bands) and keeping the
three plies visually distinct (which needs them thin). Settled at cap 1.60,
`R ≈ 17.5`, `w ≈ 5.5`.

**v13/v14** — no registration mark may touch another (rejection sampling at
`r₁+r₂+1.6 mm`); two 3 mm circles landing 1 mm apart is not an overlap anyone
would defend, it is the rng running out of room. v15 is the delivered render, byte-identical to v14 and produced by the final file.

## Deviations from the reference, and the weakest part

Beyond the five de-crowding changes listed in the module docstring, one honest
departure: **the rope is fatter than the reference's** (about 45 mm against
~30 mm). That is the price of 36 filaments at a plottable pitch inside three
plies that have to stay visually separate. It reads as a heavier lower-right
mass than the reference has.

**The weakest part is the Q·Kᵀ weave.** The rope below the waist is genuinely
good — three plies, real occlusion, a rope you can read the twist of. The weave
above is correct (800 Q–K crossings, every one resolved by the score's sign, all
visible as breaks) but it is compressed into a band roughly 50 × 45 mm just
above the funnel, and its silhouette is a bell. The reason is structural and I
could not design it away: two bundles that must both arrive at one 29 mm throat
have their spines converge monotonically, so the overlap — which is
`2·hw·cos θ − spine gap` — is only ever large near the funnel. Widening `hw`
enough to overlap higher up would need 75 mm-wide bundles at x = 100, which then
have to collapse by a factor of six in 25 mm. The reference's own overlap band
measures about the same height; what it has that this does not is more filaments
at a finer pitch, which is exactly what the plotter cannot hold. If this piece
gets an r02, that is where the work is.

Second weakest: the last 40 mm before the exit reed are 36 near-parallel lines.
The spine wave keeps them from being literally straight, but that zone is the
one part of the sheet where nothing is deciding anything.
