# gan r03 — two-players-interlaced · parent: r01 · 2026-09-28

## Render
```
.venv/bin/python scripts/render_candidate.py studio/gan/rounds/r03/piece.py \
  --fn gan_darn --seed 7 --paper a4 --palette black,crimson,dodgerblue \
  --out ~/Downloads/pp_gan_two-players-interlaced_v10.png
```
- final PNG: `~/Downloads/pp_gan_two-players-interlaced_v10.png`
- final GCODE: `~/Downloads/pp_gan_two-players-interlaced_v10.gcode`
- seed 7, A4 portrait, white/cream. (v9 has identical geometry; v10 is the one
  rendered from the final source after a docstring/import tidy.)
- self-rounds: v1 → v10 (v1 first weave · v2 run continues until it leaves the sheet, display title ·
  v3 sheet becomes a window on the run, scale 36 · v4 moves under the title are not laid ·
  v5 connected-piece filter (turned out not to be enough) · v6 drop tapes that land mostly off the sheet ·
  v7 over/under rule stated exactly, solid title · v8 legend moved off the rule line ·
  v9 composition moved up 4 mm to clear the footer · v10 final).
- seeds tried: 3, 11, 21. Seed 11 leaves a stray tape under the title. Seed 21 is still crawling
  on the sheet when it hits the iteration cap. Seed 7 kept.

## Mandate responses
`studio/gan/` has no LEDGER.md and no FEEDBACK.md. There are no open J*/A*/S* mandates, and r01 has
no critiques on file. The "Weak" list in DESCRIPTION.md is the only record we have, so I answer it here:

| id | item (DESCRIPTION § Weak) | status |
|---|---|---|
| W1 | outward spiral does not read | FIXED — the run is laid as a continuous woven tape from the hole to the sheet edge. Nothing is thinned. The laps widen 0.74 → 1.12 → 1.69 → 2.56 → 3.42 and leave the frame at the lower right |
| W2 | green mesh loudest, duel quietest | FIXED — the mesh is gone. The duel is the only mass on the sheet |
| W3 | ink floods at horn/trough | FIXED — no surface. The reed pitch is a fixed 1.8 mm everywhere, and under-thread dashes are 0.8 mm |
| W4 | green sliver past the margin | FIXED — everything is clipped to the drawable area. A tape that lands < 45 % on the sheet is not laid (6 dropped), so no slivers |
| W5 | empty top third is leftover | FIXED in part — the cloth now fills the sheet, and a lap-5 arc crops in at the top right beside the title. The top-left void is still more leftover than shaped (see self-critique) |
| W6 | footers on different baselines, swatch floats | FIXED — one footer block on the left edge with 3 baselines. The legend is flush right on footer baselines 1–2, and its swatches are real samples of each thread |
| W7 | picket-fence radial stubs | FIXED (moot) — no mesh |
| W8 | G THETA missing, D PSI present | FIXED — the legend gives both players the same form: `WEFT G MOVES THETA` / `WARP D MOVES PSI` |
| W9 | depth only from ring compression | ARGUED — the plate is a declared flat textile (the Bauhaus weaving workshop's canon). Its only depth is real over/under occlusion at 4 855 crossings |

## What changed from parent
- **The order changed, not the numbers.** r01 extruded V = f(ψθ) as a 3D saddle and scattered the run over it as thinned dashes. r03 drops the surface completely and makes the run itself the cloth. Every generator move is a horizontal tape of weft (crimson). Every discriminator answer is a vertical tape of warp (blue). Both sit on one reed phase-locked to the equilibrium.
- **The mapping, in one line:** weft = G's move · warp = D's move · float length = the leg length h·|ψ|·f′(s) or h·|θ|·f′(s) · on top = sign(ψθ) (ψθ > 0: D ahead, warp over; ψθ < 0: G ahead, weft over) · hole = inside r₀, where no thread ever crosses.
- **The sheet is a window.** The run is iterated past the sheet until it can never come back, so laps 4–5 crop against three edges and re-enter at the corners. The escape exits at the lower-right corner. Tension comes from real cropping, not from placement alone.
- **A twist, kept quiet.** A weave around a hole is a darn, and a darn is how you *fix* a hole. This one is woven outward and never closes, so the title NO FIXED POINT now does two jobs. The caption does not spell out the joke.
- **Kept from r01 (DESCRIPTION § Keep):** the equilibrium as bare paper with a single `+` · the title/tagline pair · each iteration split into a generator leg and a discriminator leg in two pens. Dropped: the saddle relief and `EQUILIBRIUM / NEVER REACHED` (the hole now says it).
- **Kept but thin:** the conserved continuous-time orbit, a dotted circle at r₀. It shows only where the discrete run has drifted more than half a tape off it (a crescent in quadrant IV). That is exact but subtle.
- Type is its own pen (black), with a display-weight title (`giant_type` 9 mm, 0.9 mm weight). The cloth stops 5 mm short of the title block by not laying those moves at all, so the edge is a whole tape, not cut threads.

## Measurements / computations
- Dirac-GAN, h = 0.26, r₀ = 0.74, a₀ = 0.4262 rad (seed 7). This is r01's run exactly: r crosses 3.42 at step 577 (r01 stopped its arena at 3.23, step 575).
- **Radius law verified per step:** max |r²ₙ₊₁/r²ₙ − (1 + h²f′(s)²)| over 6 000 steps = **6.7e-16** (machine precision).
- Lap radii at each full turn: 0.74 → 1.12 (step 50) → 1.69 (103) → 2.56 (181) → 3.42 (577) → 4.35 (3641).
- Steps that touch the sheet: **3 642**. Of these, **3 568 are in ψθ > 0** (D ahead: f′(s) → 0, the saturating crawl) and only **74 are in ψθ < 0** (G ahead: the big stairs).
- **Weft float length** (G's leg, mm on paper): ψθ < 0 median **6.23 mm**, max 35.0 mm. ψθ > 0 median **0.021 mm**, max 13.4 mm. f′(s) on sheet ranges 5.9e-4 … 1.000.
- After it leaves the sheet the run stalls: at step 6 000, r = 4.7463, s = 9.14, f′ = 1.07e-4. Growth per step is ~1 + 8e-10. This is the vanishing-gradient pathology, and it is why the cap is steps, not radius.
- **Weave:** reed pitch 1.8 mm (0.05 world units at 36 mm/unit). Tape = 0.26 world units ≈ 9.4 mm ≈ 5 threads. 141 weft rows, 111 warp columns, **4 855 crossings, 2 834 warp-over (58 %)**. Under-gap ±0.5 mm, so a 0.8 mm dash.
- Layout: equilibrium at (u, v) = (0.56, 0.515) of the drawable area (bounds fraction (0.56, 0.485) from the bottom), 36 mm per unit. The title block spans u 0.00–0.62 at the top. Footer: 3 lines at the bottom-left. Legend: flush right on the footer's first two baselines.

## Plot budget
- draw **15.0 m**, travel **20.1 m**, **33 735** commands, **5 546** pen lifts, 3 pens (black type · crimson weft · dodgerblue warp).
- The preview estimate is 16 min. On Leo (F600 draw, G4 P1.0 dwells) expect about 25 min of drawing, 10 min of travel and **about 3 h of pen-lift dwell**. Weaving is dash-bound by nature: every under-thread is a separate stroke. Plot one pen at a time (crimson 1 → blue 2 → black 0 last, so the type goes over the cloth).

## Self-critique (rubric, honest)
1. **Hierarchy — 8.** At 3 m the woven spiral is the one mass. The heavy title comes second, the footer and legend third.
2. **Grid & alignment — 7.** Title, tagline and footer share the left edge. The legend is flush right on the footer baselines. The cut at the top-right arc falls on the title-halo edge, not on a declared module.
3. **Tension & asymmetry — 7.** The centre is off-axis and the sheet crops on three sides. The run exits at the lower-right corner, and the G-ahead stairs make a working diagonal from lower-right to upper-left. But the spiral is still a round, near-concentric form sitting close to the middle.
4. **Negative space — 7.** The hole is shaped (the subject), and the gaps between laps widen with the data. The upper-left void between the title and lap 4 is leftover more than designed.
5. **Craft for pen — 7.** 1.8 mm reed, 0.8 mm dashes, no floods, no slivers, bounds clean. The 5 546 lifts make a long plot, and the dotted orbit survives only as a crescent.
6. **Concept legibility — 8.** Interlacing is a real order the mechanism has: two players, two thread systems. The rule fits in one line and is printed. Escape from the hole reads in one glance. The float-length contrast (74 big stairs against a 3 568-step crawl) is visible at 1 m.
7. **Depth — 6.** A declared flat textile. The only depth is real over/under.

**Worst thing on the sheet:** at 3 m the two thread colours blend into one purple band. The four-quadrant "who is ahead" field (blue on top in I/III, crimson on top in II/IV) only reads at about 1 m. The stairs carry the crimson and the crawl stays neutral, when the crawl should read as blue.

## Engine requests
- A kit/engine **weave primitive**: over/under crossings on a phase-locked reed with a gap rule, taking presence intervals per row/column and returning pen-tagged strokes. This is the third weave plate (loom, attention-weaving, this one), and each hand-rolls the same interval algebra.
- A **crop-hygiene policy** in `policies.py`: drop a mark group whose on-sheet fraction is below a threshold, instead of clipping it to a sliver.
