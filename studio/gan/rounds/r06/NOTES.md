# gan r06 — wildcard (De Stijl · Mondrian, *Broadway Boogie Woogie*) · parent: r04 (name only; nothing reused but the run) · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/gan/rounds/r06/piece.py \
  --fn gan_boogie --seed 7 --paper a4 --palette gold,crimson,royalblue,black \
  --out gallery/studio/gan/current/pp_gan_wildcard_v7.png
```
- final PNG: `gallery/studio/gan/current/pp_gan_wildcard_v7.png` · GCODE: `gallery/studio/gan/current/pp_gan_wildcard_v7.gcode` · seed 7
- trials: v1–v6 (same dir), seed checks `pp_gan_wildcard_v5_s3.png`, `pp_gan_wildcard_v5_s11.png`. The layout holds on both. On s3 the `STEP 0` label hit the equilibrium label, so a guard was added.

## The order, the lineage, the canon
- **ORDER: orthogonal subdivision / lanes.** The run is squared. It is not woven, not orbital and not a staircase: none of r01–r04's orders (saddle, plan-view staircase, woven tape) survive.
- **LINEAGE: Piet Mondrian, *Broadway Boogie Woogie* (1942–43).** It lends lanes whose rhythm is the data: yellow lanes carrying small red and blue squares.
- **CANON: De Stijl (STYLES.md §7), declared flat.** There are no diagonals or curves anywhere, type included. Every glyph is an orthogonal van Doesburg–style lattice letter written for this piece. One stated deviation: the run's lanes are colour, not black rules. That is Mondrian's own New York move in the lineage work. Black is kept for the rules that are not the run (the flow square, which is 3-pass and the heaviest rule), the `+`, and the type. v2 tried a black pinwheel "whirl" rule off every lane corner, which is the canon's black-rule partition. It read as picket stubs, so it was cut (`whirl=False`, code kept).
- **TWIST:** a square spiral is a labyrinth, and a labyrinth's prize sits at its centre. Here the centre is the one square the run never re-enters. The boogie-woogie is a duet in which one player's beats stride (red, sparse) while the other's clog into solid blue as D saturates.

## The mapping (one line each, exact)
- **lane side position** = the run's crossing radius on that axis (chord-interpolated), × 38 mm/unit, + 1 mm gap. Lane width 6.5 mm, constant.
- **beat cell** = one 6.5 mm cell of lane (each side is cut into round(len/6.5) equal cells). A step lands where the ray from the equilibrium through its iterate meets the lane centreline.
- **cell colour:** blue if the steps landing there had ψθ > 0 (D ahead, "D spots the fake"). Red if ψθ < 0 (G ahead, "G fools D"). Yellow if no step landed (the run passed over).
- **black square:** half-side r0 = 0.74 → 28.12 mm. It is the h→0 flow's squared orbit, since the flow crosses every axis at r0. Its outer edge is exactly r0, and the lane starts on it at step 0.
- **`+`:** the equilibrium θ = ψ = 0, on bare paper.

## Mandate responses
| id | mandate | status |
|---|---|---|
| S2 | perceived float = Σ moves | **FIXED by removal.** No float, dash or width claims a move. The only lengths keyed are side position (crossing radius) and landing (ray). Cells are a fixed 6.5 mm module and are keyed as "a step landed here", never as a length |
| S6 | encoding.md / dossier | **ARGUED.** The translator's encoding.md (Albers weave, r05 line) is binding for the refinement, not for the wildcard. This round's mapping is stated above. §4.1 check numbers were recomputed and agree (below) |
| S8 | every in-frame iterate carries a mark; window declared | **FIXED (redefined).** Every step 0…124 lands on an in-window cell (231 in-window landings). The first beat off the sheet is keyed as `STEP 125 R 1.88: FIRST BEAT OFF THE SHEET`. The window is the lane crops at the frame. No lane runs under the footer (window y 43.8–256.8, footer top 31.8) |
| S9 | key on-top channel in words | **FIXED (analogue).** `A STEP, D AHEAD: D SPOTS THE FAKE` / `A STEP, G AHEAD: G FOOLS D` / `AHEAD: D IF PSI·THETA ABOVE 0, ELSE G` |
| A1 | one continuous body per lap, traceable, no jogs/orphans | **FIXED.** One lane from step 0 to every crop. It has no jogs: sides change only at the square corners. The only breaks are the 0.8 mm colour seams between cells |
| A4 | shaped negative space, one gutter module | **FIXED.** The paper is a second square spiral (the channel) that widens 1.5× per lap, plus the bare square. The gutter is 12 mm type↔window top and bottom |
| A5 | accent pen scarce and loud | **FIXED.** Black inside the window is only the flow square and the `+`. Red is the scarce colour (55 of 270 cells) |
| A6 | weight advances outward | **ARGUED / partial.** The lane width is constant (Mondrian's lanes are). What advances outward is the channel (×1.51 per lap) and the blue clot: lap 0 D quarters are 10–15 steps, lap 3's is 79 (a solid 90 mm blue bar on the right). The eye travels to the outer NE corner |
| A7 | lineage carries the figure | **FIXED for this lineage.** Remove the colour rule (all cells yellow) and only a square spiral remains. The crawl/stride rhythm, which is the mechanism, vanishes |
| A14 | depth declared | **ARGUED.** De Stijl is flat by nature and declared flat. Depth = none |
| A17 | ≥ 3 mm paper channel between laps | **FIXED.** The minimum channel is ≈ 12 mm (lap 0 → 1) |
| A18 | band reads as cloth | **N/A (no cloth).** Lanes are serpentine fills at the 0.8 mm floor, so each reads as a solid colour bar |
| A19 | title top clearance, title axis, `min_G max_D V(D,G)` | **FIXED.** The title spans exactly x 10.2 → 199.8 (measured). Cap-tops are on the top margin line, as the canon's masthead. `MIN G MAX D V(D,G)` sits flush right on the tagline baseline |

## Measurements / computations (seed 7)
- a0 = 0.426216 rad (24.42°), h 0.26, r0 0.74. Scale 38 mm/unit, so the flow square half-side is 28.12 mm. Equilibrium at (78, 141) mm, 27 mm left of the page axis.
- Crossings (chord k, side, r): 9 N 0.7902 · 20 W 0.8846 · 35 S 0.9666 · 45 E 1.0857 · 60 N 1.1800 · 70 W 1.3375 · 88 S 1.4376 · 97 E 1.6479 · 120 N 1.7508 · 128 W 2.0363 · 164 S 2.1304 · 172 E 2.5116 · 251 N 2.5955 · 258 W 3.0860 · 573 S 3.1636 · 580 E 3.7868. Lap ratio on each ray ≈ 1.49–1.52.
- **The rhythm (steps per quarter-turn):** D-ahead quarters take 10, 15, 15, 18, 23, 36, 79, 315 steps. G-ahead quarters take 11, 10, 10, 9, 8, 8, 7, 7 steps. The median step in the lap-3 D quarter is 0.031 units (1.2 mm). In the G quarter it is 0.68 units (25.9 mm).
- Cells drawn: 270 (blue 127, red 55, yellow 88). Colour disagreements between a landed step's sign and its cell colour: **0**.
- First beat off the sheet: step 125 (r 1.881), on lap 2's N side, which is cropped at x = 10.
- Lane clearances to the window (mm): every visible side is ≥ 8.7 inside or wholly outside. W2, W3 and S3 are outside. The top lane N3 is 9.7 under the window top, and S2 is 8.7 above the window bottom. The left crops (N2, N3, S2) cut horizontal lanes across the frame, with no grazes.

## Plot budget (from the gcode; Leo at F600 draw, 33 mm/s travel, ≈2.5 s per pen cycle)
| order | pen | meaning | draw | pen-downs | est. |
|---|---|---|---|---|---|
| 1 | gold (yellow) | the run passed over without a step | 2.96 m | 39 | ≈ 7 min |
| 2 | crimson | a step while G is ahead (G fools D) | 2.65 m | 36 | ≈ 6.5 min |
| 3 | royalblue | a step while D is ahead (D spots the fake) | 5.69 m | 15 | ≈ 10.5 min |
| 4 | black | flow square, `+`, labels, title, footer | 3.88 m | 714 | ≈ 38 min |
- Total: draw 15.19 m, travel 5.68 m (< draw), 7,043 commands, 805 pen-downs, **≈ 62 min + 3 swaps**.
- Light → dark (yellow first, black last). No two pens ever touch: cells of different colour are separated by 0.8 mm of paper, and black never enters a lane.
- Minimum colour stroke is 14 mm. The black layer's shortest strokes are type punctuation (`.` 0.3 mm).
- Batching: each colour run of cells is one serpentine stroke. The longest is the lap-3 blue bar, ≈ 1 m of ink and ≈ 100 s, which is still a clean batch boundary. Strokes are spatially ordered by the per-colour nearest-neighbour pass.

## Self-critique (honest)
- Hierarchy 7: lanes first, black square + `+` second, block title third. The lanes are only 6.5 mm, so at 3 m the read is "square spiral", not mass.
- Grid 7: the title spans the margins, the right footer column hangs from the flow square's right edge, and the lanes crop on the left frame. The lanes' own positions are data, not a grid.
- Tension 7: off-axis centre and hard left crops. The right 19 mm strip and the top band are quieter than they need to be.
- Negative space 7: the paper channel is a widening spiral. That is shaped, but it is the same shape as the ink.
- Craft 8: no ink-on-ink, fills at the floor, one lift per colour run, about an hour on Leo.
- Concept 7: squared orbit + beat colour. The crawl/stride contrast lands at 1 m (the solid blue NE bar against scattered red on yellow). It is still a phase-plane picture, only squared.
- Depth: declared flat (De Stijl).
- **Single worst thing:** it is still read in the (θ, ψ) plane. A critic can call it "r02's phase-plane spiral, squared and coloured". The order is new (lanes and beats), the geometry is not.

## Engine requests
- `kit.orthogonal_font()` / a square-lattice stroke font (the De Stijl canon forbids the house font's curves and diagonals). This piece carries one locally (`GLYPHS`, `stroke_text`, `block_text`).
- `kit.orthogonal_subdivision()` is still unbuilt. The whirl partition here is a candidate for it.
