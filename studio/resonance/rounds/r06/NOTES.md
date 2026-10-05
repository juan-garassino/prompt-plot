# resonance r06 — iterate · parent: r10 (= r01/v13 + Juan's continuous dots) · 2026-09-29

v13's composition, every element and all six pens are where r10 has them. This round changes only
how marks are made (r05's Stroke IR plus a dot resolver) and how the sheet streams (an order that
the engine's own stroke walk reproduces). Lineage: Thomas Young, *Lectures on Natural Philosophy*
(1807), Plate XX Fig. 267 (interfering). The plate is declared flat.

## Render

```
.venv/bin/python scripts/render_candidate.py studio/resonance/rounds/r06/piece.py \
  --fn attention_resonance_iterate --seed 7 --paper a4 --orientation portrait \
  --palette goldenrod,dodgerblue,forestgreen,crimson,darkviolet,black \
  --out gallery/studio/resonance/current/pp_resonance_iterate_v5.png
```

- final: `gallery/studio/resonance/current/pp_resonance_iterate_v5.png` + `gallery/studio/resonance/current/pp_resonance_iterate_v5.gcode`, seed 7
  (seed 7 reproduces v13's 60 seeded scatter marks).
- Seeds 11 and 23 move only those 60 marks. Structure is identical: 4,610 / 4,611 cycles, 189.4 /
  189.5 min, the same max hop on every layer.
- The palette order is the stream order (light → dark). Each colour keeps its family meaning.
- Build time is about 2 CPU-minutes, almost all of it the orientation search (see Engine requests).
- Self-rounds: v1 (IR + resolver), v2 (tour search; the connector cut the MoE rule), v3 (channel
  route; blue regressed to a 132 mm hop), v4 (dead-end steering by dot spacing), v5 (node/ink raster
  pad).

## Mandate responses

| id | mandate | status |
|---|---|---|
| J1 | continuous round dots, 0.9–1.1 mm, end-anchored, converging paths phase-locked | **FIXED.** Every dotted-line dot is the same mark: one 0.1 mm loop, which inks a round ⌀0.55 mm dot under a 0.35 nib. It is never a tick or a dash. ∂L/∂Q rail, measured on the gcode: 28 dots from x 29.98 to 56.32 (the run is 29.98–56.57; the end dot slid 0.25 mm off the node keep-out), pitch median **1.000** mm, max 1.006. The one short step (0.75 mm) is next to the node. Same-pen dot nearest-neighbour median per pen is 0.95–1.00 mm. The gcode has **0** straight marks of 0.3–1.2 mm on any dotted line. The 8 such strokes that exist are glyph parts: the hyphen in `top-2`, the `t` crossbars and the `L` feet. Phase-lock: same-pen paths closer than 2 mm anchor their dots on the earlier path's dots (941 lock anchors). Dot pairs are ≥ 0.60 mm apart, exact before the gcode's 0.01 mm rounding (≥ 0.59 after). Dots sit 1.0 mm apart and are never re-pitched per role. |
| J2 | keep the original: every element, at v13 positions | **HELD** (Juan closes). All present: 5 Q + 5 K + 3 V packet rows, Z, 2 solid + 3 ghost expert lanes, Y, 6 softmax peaks + 3 ghosts, 20 fans with their terminals, 12 guides, 14 droplines, the three Z taps, 5 + 3 ∂L fractions **with arrowheads**, the purple skeleton, every node and every label. Field (spokes + 60 scatter): **179 of v13's 185**. 33 of them slid ≤ 0.6 mm off a crest line that would have swallowed them; 6 found no clear spot. Stipple caps (crest fade m 22–51): **220 of v13's 236 marks**, one round dot per v13 mark at v13's position. 66 slid ≤ 0.6 mm. Of the 16 lost, 9 sat inside the `softmax` label box (v13 overprinted the letters), 2 on a node and 5 had no clear spot. Halo ellipses: v13 draws **2 per source**. Its a = 152 px ellipse lies wholly inside the crest reach, so it has zero points in v13 as well. They are now 8 arcs. Moves > 1 mm: the ∂L stack (r05's re-spacing), the link and V-connector end points (S1a), nothing else. |
| A13 | continuous dot exposed mud, chords/stub, `-` ticks | **FIXED.** (a) The caps are v13's own mark positions (220 dots), not r10's 1 mm re-dotting (which gave 1,215 cycles of mud across the crimson and blue fans and the caps). At 4× crop they read as stipple, with no flood. (b) Each halo ellipse is split into its own arcs by circular run-finding. Each arc end is bisected to lie exactly ON the crest keep-out circle. There are no chords at y ≈ 141/191 and no right-hand stub. (c) There are 0 ticks: every `_fdot` is a touch, a loop or a spiral by radius (r05's `_disc_mm`). |
| A4 | batching and waste | **FIXED**, with the 80 mm cap **ARGUED on 2 layers**. Max in-layer hop: gold 36.0, green 43.8, violet 26.2, black 51.1 mm. Blue is 87.5 and crimson 88.2 mm, which equal their geometric floors (87.5 and 88.3). The floor is the MST bottleneck of the pen's ink. Each of those pens has two clusters, the Q/K block and its ∂L group, with no ink of that pen between them, so no order can do better without inventing ink. r10 had 250 mm. Invisible cycles: **0** dots in a label halo, **0** on a node (ring + 0.55 mm), **0** within 0.45 mm of same-pen solid ink (min 0.568 mm). Co-incident ink: the carrier IS the axis. The straight axis is drawn only under each packet, where the carrier leaves it, so the v13 look holds and nothing is inked twice. Ghost rails and ghost carriers overlapped in v13; they now share their dots through the resolver. Travel **8.23 m ≤ draw + dots × 1 mm = 15.36 m**. The batch table is below. Order: light → dark. |
| A5 | collisions without deleting | **FIXED.** V rows: each lower packet is occluded under the upper row's envelope + 0.6 mm (lower packet hidden). Crossings between different rows' gold carriers: **0** (they crossed at x 140–150 in r10). `router`: haloed, so no dot or line of any pen is inside its box. Z taps: each tap now runs from Z's axis down ONTO its return curve. The curve carries a shared dot exactly at the junction, and each tap is one continuous dotted run into its curve. |
| S1a | softmax→ links and V's connector end on Z's axis | **FIXED.** The 6 links keep v13's launch at the softmax baseline, re-aimed to end at x = 66.9 / 70.3 / 73.8 / 77.1 / 80.3 / 82.8 mm, y = 75.00. That is **0.00 mm off Z's axis**, with the final dot on the axis. Three of them land where the crimson, blue and gold taps leave the axis below, so a_j·V_j visibly runs through Z into ∂L. V's connector keeps its v13 start at V row 3's right end. It hooks down and runs the clear channel between the softmax baseline and the MoE header (y ≈ 107.2 mm: 4.7 mm under the softmax baseline, 3.8 mm above the header text), then ends ON Z's axis at x = 88.9 mm. It no longer ends on Y (164, 77). All stay gold. |
| S1b | links in gold vs black | **ARGUED** (lead's position, for the critic): gold = the weighted value a_j·V_j flowing into Z. |
| A3 | ∂L stack clear air | **CARRIED** from r05. Clear air is 2.95 / 3.08 / 3.08 / 3.08 mm at a 9.48 mm pitch, type 11.5 px, and the stack's foot is unchanged. |
| A9 | declare depth | **FIXED**: HANDOFF declares the plate flat. |
| A12 | right ∂L labels on no common edge; uneven side margins | **DEFERRED** to r07 (ledger: mandate cap). |
| S0 | no dossier/encoding for resonance | **DEFERRED**: curator/expert. |
| S1c | Z = AV scale | **BLOCKED by J2** (changes v13's big green packet). |
| S2 | one key axis (n_K = n_V = n_softmax) | **BLOCKED by J2** (changes element counts). |
| S3a | hero crests are ellipses | **BLOCKED by J2** (changes the hero's stretch). |
| S3b | field dot size vs \|A\| | **DEFERRED** to r07 (ledger). Sizes and positions are v13's, except 33 dots slid ≤ 0.6 mm. |
| A1 A2 A6 A7 A8 A10 A11 | (dropped in the ledger, superseded by J2 or the pen-cap lift) | no action |

House law note: the 8 ∂L arrowheads are kept because J2 and the SYNTH name them. The "never
arrows" law governs projection lines. The heads also carried a latent v13 bug: the fill ran from
the back edge to the back edge (`frac = 1 − |y|/hb`), so they plotted with a notch. They are now
solid, and each is one pen-down instead of 1 + 5.

## What changed from parent

No composition move except the mandated re-wiring. The work was on marks and streaming:

1. **Stroke IR.** r10's geometry is ported onto r05's IR. Helpers register solid strokes, dotted
   paths and dot textures on the sheet. G-code is written only after three passes:
   - halos (r05's exact Rect/Union clip);
   - the dot resolver;
   - the tour.
2. **The dot resolver** (new). Dotted LINES get anchors (both ends, polyline corners, junctions,
   and phase-lock projections of earlier same-pen dots within 2 mm), with 1.0 mm fill between
   them. Each dot may slide ≤ 0.35 mm along its own path to the nearest clear gap. A dot is
   placed only if it is:
   - ≥ 0.55 mm from same-pen solid ink;
   - ≥ 0.60 mm from any same-pen dot (checked exactly);
   - outside every label halo and every node keep-out.

   So a dropline crossing the crest net puts its dots between crests, and a dot that would land
   on a line is not drawn. TEXTURES keep v13's mark positions (reconstructed from r01's
   `_dash_mm` phase), one round dot per mark, sliding ≤ 0.6 mm only when the exact spot is
   invisible.
3. **The tour.**
   - `postprocess.reorder_by_color` re-derives stroke order by nearest START from (0, 0) and
     never reverses. The one lever a piece has is which end each stroke starts at, and which
     vertex each loop starts at. The piece therefore runs a reversal- and rotation-aware
     nearest-neighbour walk, then a local search over orientations scored against an exact,
     prefix-cached re-implementation of the engine's walk. It emits in that walk's order.
   - Checked: the engine re-derives the identical order. The hops on the v5 gcode equal the
     piece's own, to 0.1 mm.
   - Each Z tap is a dead-end branch. Two local dot spacings inside J1's band decide the walk
     there: the first tap dot sits 0.8 mm above the junction while the next curve dot sits
     1.1 mm on, and the curve dot where the walk re-enters steps 0.85 mm back and 1.15 mm
     forward. The pen draws the tap in passing and leaves the cluster from the curve's far end.
     That took blue from 132 mm to its 87.5 mm floor.
4. **Carrier = axis; envelope split into runs.** The envelope no longer draws chords between
   packets. Envelope dashes are 1.3 mm in v13's 2.4 mm period (the same count), which keeps them
   dashes and out of the micro-dash range. Weighted type is fused into one pen-down per glyph
   stroke.
5. **V rows occluded; S1a re-aim; taps joined; arrowheads solid** (see mandates).

## Measurements / computations

| | v13 (r01) | r10 | **r06 v5** |
|---|---|---|---|
| pen cycles | 3,471 | 6,092 | **4,618** |
| draw | 10.26 m | 10.99 m | 11.80 m |
| travel (incl. layer approaches) | 11.30 m (110 %) | 12.60 m (115 %) | **8.23 m (70 %)** |
| longest in-layer hop | — | 250 mm | **88.2 mm** (floor-bound) |
| dash-like dot marks (v13: sub-1.2 mm dashes; r10: 0.3 mm ticks) | 2,704 | 2,237 | **0** |
| Leo time (model below) | ~150 min | 239.7 min | **189.7 min** |
| `preview --score` | A, efficiency 0.471 | — | A, efficiency 0.586, focal balance 0.968 |

Resolver ledger (seed 7):
- **Dotted lines:** 3,283 dots placed. 836 candidate positions were not inked because they fell on
  same-pen ink, in a halo or on a node. Most are droplines crossing the crest lens and fans
  crossing guides.
- **Crest fade:** 220 of 236.
- **Field:** 179 of 185.
- **Halo arcs:** 8.

Hop floors (MST bottleneck of each pen's ink): gold 6.1, blue 87.5, green 7.2, crimson 88.3,
violet 5.9, black 51.1 mm.

## Plot budget

Leo model: 2 s per pen cycle, F600 draw, F2000 travel, 2 min per swap. Minutes include each
layer's approach from the previous layer's end. The final park to (0,0) is not counted; it is the
engine's 323.6 mm "longest travel".

| # | pen | meaning | cycles | dots | draw m | travel m | max hop mm | min |
|---|---|---|---|---|---|---|---|---|
| 0 | goldenrod | V, softmax→Z links, V→Z, ∂L/∂V | 620 | 520 | 1.01 | 0.89 | 36.0 | 22.8 |
| 1 | dodgerblue | K, fans, ∂L/∂K | 1,033 | 834 | 1.89 | 1.46 | 87.5 (floor 87.5) | 38.4 |
| 2 | forestgreen | Z = AV, ∂L/∂Z, gradient column | 239 | 167 | 0.92 | 0.49 | 43.8 | 9.9 |
| 3 | crimson | Q, fans, ∂L/∂Q | 991 | 796 | 1.88 | 1.44 | 88.2 (floor 88.3) | 36.9 |
| 4 | darkviolet | MoE, Y, ∂L/∂Y·experts·router | 525 | 355 | 1.35 | 0.82 | 26.2 | 20.2 |
| 5 | black | field, softmax, title, fraction, MoE header, ∂L/∂A | 1,210 | 884 | 4.75 | 2.50 | 51.1 (floor 51.1) | 49.6 |
| | **total** | | **4,618** | **3,556** | **11.80** | **8.23** | | **177.7 + 6 swaps × 2 = 189.7 min** |

**Stream order, light → dark.** Gold, blue, green, crimson, violet, black. The darkest inks land
last, so no light nib runs through wet dark ink. Gold's links and channel are crossed later by the
return curves, and the black field goes on top. With `plot layer` this is simply colour 0..5 in
order.

**Batches** (`promptplot plot layer <gcode> <colour> --strokes S:E`; ≤ 300 cycles each). Cuts fall
on cluster boundaries first (hops > 40 mm), then on the largest hop near an even split:

| pen | colour | --strokes | cycles | draw m | travel m | min | region x, y (mm) |
|---|---|---|---|---|---|---|---|
| goldenrod | 0 | 0:231 | 232 | 0.18 | 0.28 | 8.2 | 18–185, 34–121 (∂L/∂V, links) |
| goldenrod | 0 | 232:425 | 194 | 0.71 | 0.39 | 7.8 | 79–187, 75–145 (V block, channel) |
| goldenrod | 0 | 426:619 | 194 | 0.12 | 0.26 | 6.8 | 67–114, 49–110 (links, return curve) |
| dodgerblue | 1 | 0:118 | 119 | 0.11 | 0.22 | 4.3 | 18–105, 43–90 (∂L/∂K, tap, return) |
| dodgerblue | 1 | 119:328 | 210 | 0.14 | 0.28 | 7.4 | 117–152, 175–267 (fan tips, guides) |
| dodgerblue | 1 | 329:574 | 246 | 1.11 | 0.30 | 10.2 | 130–182, 201–269 (K rows) |
| dodgerblue | 1 | 575:820 | 246 | 0.17 | 0.29 | 8.6 | 114–135, 180–228 (fans) |
| dodgerblue | 1 | 821:1032 | 212 | 0.37 | 0.44 | 7.9 | 113–191, 200–269 (fans, K label) |
| forestgreen | 2 | 0:238 | 239 | 0.92 | 0.73 | 9.9 | 18–134, 15–99 (whole layer) |
| crimson | 3 | 0:101 | 102 | 0.10 | 0.15 | 3.6 | 18–95, 53–88 (∂L/∂Q, tap, return) |
| crimson | 3 | 102:378 | 277 | 0.42 | 0.41 | 10.1 | 28–96, 175–250 (fans, guides) |
| crimson | 3 | 379:583 | 205 | 0.35 | 0.25 | 7.5 | 28–85, 200–255 (Q rows) |
| crimson | 3 | 584:820 | 237 | 0.90 | 0.40 | 9.6 | 19–86, 201–269 (Q rows, label) |
| crimson | 3 | 821:990 | 170 | 0.11 | 0.25 | 6.0 | 40–97, 206–236 (fans) |
| darkviolet | 4 | 0:262 | 263 | 0.90 | 0.44 | 10.5 | 92–196, 55–92 (router, lanes, Y) |
| darkviolet | 4 | 263:524 | 262 | 0.44 | 0.52 | 9.7 | 97–196, 23–97 (skeleton, ∂L fractions) |
| black | 5 | 0:141 | 142 | 0.41 | 0.31 | 5.6 | 18–146, 24–129 (∂L/∂A, MoE header) |
| black | 5 | 142:332 | 191 | 0.97 | 0.27 | 8.1 | 76–141, 111–183 (softmax, droplines) |
| black | 5 | 333:617 | 285 | 0.74 | 0.55 | 11.0 | 44–158, 101–197 (hero right, field) |
| black | 5 | 618:882 | 265 | 1.18 | 0.60 | 11.1 | 37–109, 112–197 (hero left) |
| black | 5 | 883:1175 | 293 | 0.88 | 0.66 | 11.6 | 69–173, 137–222 (upper cap, fraction) |
| black | 5 | 1176:1209 | 34 | 0.57 | 0.25 | 2.2 | 45–162, 272–280 (title) |

Nib: 0.3–0.4 mm. At 0.5 mm the dot gaps (0.45 mm) and the 1.21 mm crest pitch start to close.
Longest single stroke: the Z carrier, 0.43 m (43 s).

## Self-critique

| dimension | score | why |
|---|---|---|
| hierarchy | 5 | v13's: the hero is the heaviest mass but only ~22 % of the sheet width. Kept by J2 |
| grid & alignment | 6 | traced rows, node columns and the ∂L ladder share axes. A12's ragged right ∂L edge remains |
| tension & asymmetry | 4 | mirror-symmetric top half, kept by J2 |
| negative space | 4 | labels and nodes breathe, and dots no longer sit on ink. The lower half is still v13's web, now with one more long gold run |
| craft for pen | 8 | one dot mark, 1.0 mm pitch, phase-locked, 0 invisible cycles, 0 co-incident ink, solid heads, 70 % travel, floor-bound hops, −24 % cycles vs r10 |
| concept legibility | 3 | a labelled pipeline (NO SCHEMATICS), inherent to the benchmark |
| depth | 4 | declared flat |

**Single worst thing:** V's connector. S1a makes it end on Z, and the only clean route from V's
right end to Z is the channel under softmax. It now reads as a ~70 mm horizontal gold rail
4.7 mm under the softmax baseline, close to a second baseline. The re-aimed links then join
it into a fan above Z. It is honest wiring, but it adds weight to the busiest half of the sheet.
If the critic rejects it, the alternative is to start the connector at V's left end instead of its
right end (a > 1 mm move that J2 would have to allow).

## Engine requests

1. **Let a piece keep its order.** `postprocess.reorder_by_color` should accept a `preserve_order`
   flag or program metadata, or at least be reversal-aware with a 2-opt pass. This piece carries
   ~250 lines of tour code, and ~2 CPU-minutes of orientation search against a re-implementation
   of the engine's nearest-start walk. The only reason is that the walk is the sole authority on
   stroke order.
2. **A 2D dot resolver in `engine/kit`.** It would provide anchors plus fill, phase-lock, slide to
   a clear gap, and halo/node/ink rules on a raster plus an exact dot grid. r05 asked for a
   dotted-run primitive; this round is that primitive. It should live once, for resonance-backprop
   and resonance-ffn too.
3. **A `halo_clip` for 2D** (r05's request stands).
