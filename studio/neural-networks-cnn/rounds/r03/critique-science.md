# Science critique — neural-networks-cnn r03 · machine learning (CNNs, receptive fields) · 2026-09-28
render: ~/Downloads/pp_neural_networks_cnn_iterate_v5.png (+ .gcode: 9826 cmds; pen0 662 polylines, 12506 mm; pen1 13 polylines, 772 mm)

Process note (S6, still open): the slug still has no `dossier.md` or `encoding.md`. The check numbers
below come from the HANDOFF claims and the round's `maps.npz`. That file is byte-identical to r02's
(md5 e8270441…), and last round it was verified against an independent TF MobileNetV2 forward pass
(map correlation 0.994–0.999, argmax (4,3)), so this round I recompute from the arrays. The lies list is
the standard CNN/ERF set used in r02. Sheet coordinates are in mm, with y up.

## Check numbers
| quantity | claim (HANDOFF) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| CAM argmax | (4,3) | (4,3), CAM 18.28, mean 8.283 | crimson isolines are centred at x 139.3. Row 4 of the top plane has x0 96.4, pitch 14.28 mm/col, so col 3 is at 139.2 and the cell spans 132.1–146.4. Isolines run x 132.2–146.3 | OK |
| top-plane transform | ReLU(CAM − mean) | 27/49 cells zero, peak 10.00 | caption: "CAM − MEAN, CLIPPED AT 0". Height is linear at 6.79 mm/unit. 11 visible summits match R·6.79 to ≤ 0.1 mm, e.g. (5,3) 25.4 mm = 3.74, (4,1) at (110.7, 249.6) = 5.67, (1,6) at (191.8, 239.7) = 2.57 | OK |
| top plane whole, same basis | width 100 (cell extent) ≤ 102.4 | drawn centre-to-centre span 100·6/7 = 85.7 | front row 90.0–175.7; back row ends 194.9 (inside margin); Sx/W 0.224, D/W 0.261 | OK |
| one basis for all planes | yes | — | Sx/W 0.223 / 0.219 / 0.224 / 0.224 / 0.224; D/W 0.260 / 0.255 / 0.262 / 0.261 / 0.261 | OK |
| plane widths (drawn) | 146 / 134.5 / 123 / 111.5 / 100 | ×(N−1)/N = 145.3 / 132.1 / 118.6 / 103.5 / 85.7 | 144.6 / 132.1 / 118.6 / 103.5 / 85.7. Monotone | OK |
| black maps are the data | input lum., ‖block_2/5/12‖ | front-row profile vs map row | corr 0.997 (pix row 222), 0.999 (a56 row 54), 0.994 (a28 row 27), 0.998 (a14 row 13) | OK |
| ERF 50 % ellipse, 224² | 50 % gradient mass | moment ellipse at 50 % mass: x 61.8–150.3, 25.9 % of plane area | loop x 61.9–150.4, closed (gap 0.01), draped (2 x-reversals) | OK (Δ ≤ 0.1 mm) |
| ERF 50 % ellipse, 56² | " | x 73.0–153.5, 25.6 % | 72.5–153.0 | OK (Δ 0.5) |
| ERF 50 % ellipse, 28² | " | x 84.4–156.7, 24.8 % | 84.4–156.6 | OK |
| ERF 50 % ellipse, 14² | " | x 98.7–159.6, 19.8 % | 98.6–159.5 | OK |
| ERF centred on the unit | — | input ERF centroid (0.641, 0.529) of the image; cell (4,3) centre (0.643, 0.500) | ring centres step right 106.2 → 112.7 → 120.5 → 129.1 → 139.3 (unit) | OK |
| "~26 % OF IMAGE VS CELL 1/49" | — | 25.9 % vs 2.04 %. The smallest region holding 50 % of the mass is 17.4 %. The caption claims only "50 % of mass", and the drawn ellipse does hold 50 % | caption line 3 | OK |
| "9 closed isolines" | closed | — | open front arcs, end gaps 2.8–13.9 mm | HANDOFF wrong (sheet is fine) |
| row counts / pitch | 38/28/28/14/7 at 1.02/1.25/1.15/2.08/3.73 | resolution 224/56/28/14/7 | rows as claimed. 56² and 28² have the **same** 28 rows; pitch is non-monotone (1.25 > 1.15). Along-row roughness is 18.3 / 15.3 / 9.5 / 3.0 / 2.7 peaks per plane width | PARTIAL |
| top-plane cells legible | — | 22 nonzero cells | **12 of 22 summits visible**. Row 0: 0 ink. Row 2: 0 ink. Rows 1 and 3: one fragment each | **FAIL** |
| p(tiger_cat) | 0.43 | 0.43 (npz top5) | caption | OK (preprocessing still unstated, S7) |

## Lies list
| item | status |
|---|---|
| ERF ring is decorative, not a 50 % mass region | clean. All four loops are the 50 %-mass moment ellipses to ≤ 0.5 mm in x |
| ring about the wrong unit / wrong orientation | clean. Front = image bottom row (confirmed by row correlation); crimson summit sits exactly in cell (4,3) |
| ERF confused with TRF (TRF 491 px > 224 image) | clean. TRF is neither drawn nor claimed |
| feature-map resolution misdrawn | **VIOLATED (soft)** — 56² and 28² planes both drawn at 28 rows; pitch 1.25 mm (56²) > 1.15 mm (28²). The 2:1 step is carried only by along-row roughness (15.3 vs 9.5) |
| data truncated or omitted from a drawn map | frame clipping is FIXED. **VIOLATED by occlusion** on the 7² plane: at a 3.73 mm row pitch under a 67.9 mm peak, 10 of 22 nonzero CAM cells never show a summit. That includes the runner-up (3,3) = 6.86 (69 % of peak, would crest at (142.4, 261.4)), (2,3) = 4.26 and (3,1) = 3.72. The CAM's col-3 ridge (rows 2–5: 4.26 / 6.86 / 10 / 3.74) reads as one isolated spike |
| scale manipulated to sharpen the story | clean now (disclosed on the sheet). Note: each cell is drawn as its own cos² hill, so there are invented valleys between equal neighbours (e.g. (4,4) 5.07 → dip 2.73 → (4,5) 4.59). Peaks are exact |
| quantities unlabeled | PARTIAL. Resolutions, the crimson key and 26 % vs 1/49 are present, but nothing says what the black maps are or that the order runs bottom→top, and the "CRIMSON:" colon renders as "." |

## Scores
truth 8 · fidelity 7 · legibility 7 · VERDICT: FAIL

The science is now right and measurably so. Every ERF ellipse sits within 0.5 mm of the recomputed
value, every front row correlates ≥ 0.994 with its map, every visible CAM summit is within 0.1 mm of
R·6.79, all five planes share one basis, and nothing is clipped. Fidelity fails because the top map
hides 45 % of its nonzero cells, including the runner-up at 69 % of the peak, and because the
resolution channel is flat between 56² and 28². Legibility fails because a stranger is told
"224² 56² 28² 14² 7²" but not which terrain is which, what the black height means, or which way the
stack reads.

## Mandates
1. **7² CAM plane hides half its data (top plane, x 90–195, y 203–279).** Row pitch is 3.73 mm and the
   height scale is 6.79 mm/unit (peak 67.9 mm), a height-to-pitch ratio of 18:1. Only 12 of 22 nonzero
   cells show a summit. Rows 0 and 2 draw no ink at all. (3,3) = 6.86 is fully hidden behind (4,3);
   it should crest at (142.4, 261.4). (2,3) = 4.26 and (3,1) = 3.72 are also gone. Expected: every cell
   ≥ 20 % of the peak shows its summit. Under this basis that needs a height scale ≤ 1.9 mm/unit so
   that (3,3) clears (4,3), or a 7² map drawn in plan (isolines or per-cell marks) with the crimson
   summit kept on (4,3).
2. **Resolution channel is flat between 56² and 28² (planes 2 and 3, y 64–100 and 111–150).** Both
   carry 28 rows, and pitch runs 1.02 / 1.25 / 1.15 / 2.08 / 3.73, which is non-monotone. Expected:
   row count strictly decreasing with resolution, keeping the 2:1 step. One option is 56² at stride 2
   (28 rows), 28² at stride 2 (14 rows), 14² at 14 rows, with pitch monotone increasing ≥ 1.0 mm. The
   other is to print the stride beside each plane.
3. **Caption does not decode the stack (x 15–85, y 219–228).** Line 1 lists "224² 56² 28² 14² 7²" left
   to right with no mapping to the bottom→top planes, and never says the black height is input
   luminance, then ‖activation‖ of block_2/5/12. "CRIMSON:" renders as "CRIMSON.". The cell fraction
   is given as 1/49 but not as 2 %. The preprocessing behind p = 0.43 (centre-crop, bicubic; S7) is
   missing. Expected: put the resolution numeral at each plane's left edge, or say "BOTTOM→TOP" and
   name the quantity ("INPUT LUMINANCE · ‖ACTIVATION‖"), render the colon, write "≈26 % OF IMAGE VS
   ONE CELL = 2 %", and add "CENTRE-CROP".

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S1 | **FIXED** | top plane whole: back row ends x 194.9 (< 195 margin), no polyline stops on a clip line (1 corner endpoint per plane). (1,6) = 2.57 visible at (191.8, 239.7). Drawn width 85.7 (cell extent 100) ≤ 102.4, monotone 144.6 → 85.7. Same basis: Sx/W 0.224, D/W 0.261 |
| S2 | **PARTIAL** | resolutions 224²…7², "50 % OF ∂CAM(4,3) GRADIENT MASS" and "~26 % OF IMAGE VS CELL 1/49" are on the sheet (26 % verified: 25.9 %). But the numerals are in a caption, not at the planes, there is no bottom→top mapping, and "2 %" is absent |
| S3 | **FIXED** | "CAM − MEAN, CLIPPED AT 0" printed. Drawn heights = ReLU(CAM − 8.283) × 6.79 mm |
| S6 | **NOT FIXED** (process) | still no dossier.md / encoding.md |
| S7 | **NOT FIXED** | caption gives p = 0.43 with no preprocessing |
| S4, S5 | n/a | dropped with the r01 line |
| regressions | none on truth | r02's verified truths (argmax, ERF rings, map data) all still hold. ERF rings are now exact 50 %-mass ellipses (r02 enclosed 51.5–53.8 %) |
