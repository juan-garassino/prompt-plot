# Science critique — neural-networks-cnn r01 · machine learning (convolutional networks, receptive fields) · 2026-09-28
render: ~/Downloads/pp_neural_networks_cnn_pooling-cascade_v11.png (gcode: same stem .gcode, 11157 cmds, pens 0/1/2 = 2846/656/1168 layer cmds)

**Process finding:** `studio/neural-networks-cnn/` has **no `dossier.md`, no `encoding.md`, no `LEDGER.md`**.
There are no §7 check numbers or §4 lies list to verify against, so every check below comes from first
principles plus the HANDOFF and the on-sheet caption. That makes this round unverifiable against a stated
spec. Write the dossier before r02.

Sheet geometry, recovered from the gcode: 5 sheared cards, each 111.67 mm wide, depth vector (23.47, 65.2) mm,
front-left corners at (24.15,214.4) s=1 · (32.15,181.03) s=2 · (40.15,139.81) s=4 · (48.15,96.34) s=8 ·
(56.15,39.4) s=16. Card grids are 48x64 · 24x32 · 12x16 · 6x8 · 3x4 (width axis = 48 px).

## Check numbers   quantity | dossier | recomputed | measured on sheet | OK?
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| unclipped RF of a stride-16 unit, conv(3,5,3,3)+pool2 x4, caption order | — (caption: 50) | 1+2+1+8+2+8+4+16+8 = **50** (other kernel orders give 48/54/62) | caption "50 UNCLIPPED" | OK |
| clipped RF of the corner unit (0,0) on 48x64 | — (caption: 33x33) | -17..32 clipped → **33 x 33** | crimson on card 1: 32.90 x 32.98 px (76.53 mm vs 76.77 expected, 0.24 mm short) | OK |
| footprint of unit (0,0) on card 8 | — | 0..2 → **3 cells** | 3.00 x 3.02 | OK |
| footprint on card 4 | — | 0..6 → **7 cells** | 6.99 x 7.02 | OK |
| footprint on card 2 | — | 0..15 → **16 cells** | 15.95 wide; depth 15.59 visible (back edge hidden under card 1 at v=15.6) | OK |
| cell pitch = stride | — | 111.67/48·s mm | 2.33 / 4.65 / 9.31 / 18.6 / 37.2 mm | OK |
| strongest stride-16 unit | — | argmax of the ring map | ring counts, card 16 (front row first): [8,5,4] [4,0,2] [1,2,3] [2*,4*,5*] (*partly under card 8, read from fragments). The crimson cell (0,0) = 8, a unique max | OK (by the sheet's own encoding) |
| "where the old plate flooded" | — | parent ink (pp_cnn_dashes.gcode) rasterised 48x64: mean ink in each unit's clipped RF | parent: RF(0,0) = 1.00 (max), next 0.94. **Card 1 on the sheet: RF(0,0) = 0.81, max is RF(2,3) = 1.00** | holds for the parent, **not visible on the sheet's own input** |
| card 1 = parent plate | — | best-framing correlation, parent ink vs card-1 dashes | r = 0.60 at framing x18–189, y39–268 mm; r = 0.10 at full-page framing | weak / framing unstated |
| ring-count value scale | — | should be one scale | max rings per card 1 / 1 / 3 / 8 (cards 2/4/8/16). Every card's max fills its own cell (outer ring 0.88–0.96 of pitch) | **per-card, capped by capacity** |

## Lies list       item | clean / VIOLATED (where)
No §4 exists. These are the lies checked from first principles:
| item | status |
|---|---|
| RF drawn as the naive sum of kernels | clean. The footprints are exact and clipped, and the caption gives the unclipped 50 |
| cell size not proportional to stride | clean |
| ring count = activation value (Molnár mapping, per HANDOFF) | **VIOLATED.** Cards 2 and 4 are binary (118 and 43 occupied cells, all exactly 1 ring). Card 8 has 1–3 rings, card 16 has 1–8. The ring ceiling tracks cell capacity, not value, so "rings grow with depth" is an artefact of the drawing, not of the network |
| input card shows the previous plate's ink | **VIOLATED (partial).** All 750 card-1 dashes are the same length (0.47 cell = 1.09 mm), so the input is thresholded to on/off. The "flood" (ink density) the caption points to cannot be seen inside the crimson footprint |
| decorative marks posing as data | clean (dotted rails join real footprint corners) |

## Scores          truth 8 · fidelity 5 · legibility 6 · VERDICT: FAIL

## Mandates
1. **Ring scale is per-card capacity, not value.** Measured max rings per card: s2 = 1 (118 cells, all 1 ring), s4 = 1 (43 cells, all 1 ring), s8 = 3, s16 = 8. On every card the maximum fills the cell (0.88–0.96 of the cell pitch). Expected: one ring-per-unit scale across all four feature maps, or an explicit per-map normalisation stated on the sheet with at least 3 readable levels on every card. Cards 2 and 4 (y 139–246 mm) currently carry zero magnitude information.
2. **The input card does not show the flood the caption claims.** On card 1 (y 214–280 mm) every inked pixel is one 1.09 mm dash, 747/3072 px inked. Inside the crimson 33x33 footprint the inked density is 0.81 of the densest RF region (the back-right RF(2,3) = 1.00). In the parent plate, RF(0,0) *is* the densest (1.00 vs 0.94). Expected: card-1 marks carry graded ink density (dash length or pass count ∝ parent ink), so the footprint region reads as the densest on the sheet. Also state the raster framing: the best match is x18–189, y39–268 mm of the parent (r = 0.60), not the page (r = 0.10).
3. **No channel keys on the sheet.** The stride numerals 1/2/4/8/16 at x≈18–35 mm carry no unit ("px per cell" / stride). There is no ring legend saying rings = activation, or how many levels. The operations are listed only as a caption block (y 18–32 mm) and are not placed in the gaps between the cards they act on (expected: SOBEL 3·POOL between 1→2, GABOR 5·POOL 2→4, BINOMIAL 3·POOL 4→8, CENTRE-SURROUND 3·POOL 8→16). A stranger cannot tell why the footprint shrinks 33→16→7→3→1 cells. Also, on card 16 (y≈92–104 mm) three of 12 units (back row, values 2/4/5) are mostly hidden under card 8's front edge at v = 3.40/4, so a quarter of the payload map cannot be read.

## Follow-up on open mandates   id | status | evidence
Pass 1. There is no LEDGER.md and no open S* mandates.
