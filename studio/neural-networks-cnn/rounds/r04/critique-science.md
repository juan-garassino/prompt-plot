# Science critique — neural-networks-cnn r04 · machine learning (CNNs, receptive fields) · 2026-09-29
render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_iterate_v15.png (+ .gcode: 11,537 cmds; pen0 815 runs, 13,117 mm; pen1 10 runs, 741 mm)

Process note (S6, still open): there is still no `dossier.md` or `encoding.md` for this slug. The check numbers
below come from the HANDOFF claims and `rounds/r04/maps.npz`, which is byte-identical to r02 and r03 (md5
e8270441…). r02 verified those arrays against an independent TF MobileNetV2 pass. I recomputed everything
from the arrays. Sheet coordinates are gcode mm, y up. I reconstructed the projection from the gcode and it fits
exactly: x = x0 + W·u + 0.225·W·v, y = y0 + 0.297·W·v + h·value. On the top plane x0 = 81.25 and y0 = 250.28.
Every drawn 7² row matches the 1-D Catmull-Rom of its CAM − mean row to ≤ 0.01 mm at 1.0524 mm/unit.

## Check numbers
| quantity | claim (HANDOFF) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| CAM argmax | (4,3) | (4,3); CAM 18.28, mean 8.283, peak (CAM − mean) 10.00, min −9.00 | ring stack centred x ≈ 139.9; cell (4,3) projects to (139.29, 271.41) | OK |
| top-plane height | 1.0524 mm/unit, peak 10.5, p-p 20.0 | 10.00 × 1.0524 = 10.52; 19.00 × 1.0524 = 19.99 | 11 top-plane runs fit CR(CAM − mean)·1.0524 with max error ≤ 0.01 mm; front row dips to 242.93, which is base 252.40 − 9.47 | OK |
| signed CAM disclosed | "CAM − MEAN, SIGNED" | 27 of 49 cells negative | caption line 1 | OK |
| strong cells shown (S8) | crests 13 / 13 | 13 cells with CAM − mean ≥ 2.0 (20 % of peak) | 12 crest points lie on black ink (distance ≤ 0.01 mm), including runner-up (3,3) at (142.5, 272.35). The (4,3) summit is carried by the ring stack: innermost ring 9.41 ends 1.4 mm from the peak point | OK |
| hidden-line on 7² | — | my horizon simulation with 0.8 mm clearance | 0 mm drawn where it should be hidden. Undrawn-but-visible: row 4 19.6 mm (x 130.4–150, the summit halo, which the rings replace), row 3 8.0 mm, rows 0–2 ≤ 2.2 mm | OK |
| crimson rings = CAM level sets | 6.91 / 7.57 / 8.23 / 8.85 / 9.41 | tensor-product Catmull-Rom level sets; each is closed around (4,3) only. The 6.91 set stops at row 2.984, just short of (3,3) = 6.86 | 5 front arcs, max deviation from the projected level set 0.14–0.17 mm; each draws 48–54 % of its contour, the visible front only | OK |
| ERF 50 % ellipse, 224² | 50 % gradient mass | moment ellipse, ρ 1.248, mass 0.500, area 25.9 % | loop x 61.87–150.43 vs recomputed 62.20–150.76 (Δ 0.33 mm = ½ column); closed (gap 0.00) | OK |
| ERF 50 % ellipse, 56² | " | mass 0.500, area 25.6 % | x 72.49–152.98 vs 72.49–152.98 (Δ 0.00); closed | OK |
| ERF 50 % ellipse, 28² | " | mass 0.503, area 24.8 % | x 84.37–156.61 vs 84.37–156.61 (Δ 0.00); 2 runs, occlusion break at x 108.3–111.7, y ≈ 168 | OK |
| ERF 50 % ellipse, 14² | " | mass 0.501, area 19.8 % | x 98.64–159.51 vs 98.64–159.51 (Δ 0.00); closed; my model predicts no occluded arc (depth ≤ 0) | OK |
| ERF centred on the unit | — | ERF centroids at image (u, v-from-top) (0.531, 0.643) / (0.519, 0.627) / (0.512, 0.619) / (0.506, 0.625); cell (4,3) centre is (0.500, 0.643) | loops step right toward the summit | OK |
| "~26 % OF IMAGE VS ONE CELL = 2 %" | — | input ERF 25.9 %; 1/49 = 2.04 %. (The smallest region holding 50 % is 17.4 %; the caption claims only the ellipse) | caption line 2 | OK. "on each map" is loose: 14² is 19.8 % |
| black maps are the data | lum., ‖block_2/5/12‖ | front-row profile vs map row | corr 0.995 (pix row 222), 0.999 (a56 row 54), 0.994 (a28 row 27), 0.998 (a14 row 13). All 364 lower-plane runs fit their map row, max residual ≤ 0.42 mm | OK |
| rows / pitch (A15 · S) | 38 / 28 / 19 / 14 / 7 · 1.16 / 1.43 / 1.96 / 2.37 / 4.24 | image-row stride 6 / 2 / 1.5 / 1 / 1 | 38 / 28 / 19 / 14 / 7 distinct rows; pitch 1.161 / 1.427 / 1.957 / 2.365 / 4.243. Strictly decreasing and monotone. Note that 28² is sampled at stride 1.5, so 9 of its 19 rows are interpolated between map rows | OK |
| breaks per row | 3.45 / 2.89 / 2.16 / 0.86 / 0.57 | — | runs 169/38, 109/28, 60/19, 26/14, 11/7 → 3.45 / 2.89 / 2.16 / 0.86 / 0.57; shortest run 3.02 mm | OK |
| per-plane height scale | relief 3.0 / 3.2 / 7.0 / 9.6 / 20.0 mm | data ranges 0.71 / 51.0 / 35.7 / 49.8 / 19.0 | fitted 4.04 mm/lum, then **0.065 / 0.210 / 0.206 mm per activation unit**, then 1.052 mm/CAM → relief 2.9 / 3.3 / 7.5 / 10.3 / 20.0. **Not disclosed on the sheet** (see lies list) | PARTIAL |
| one basis | D = 0.45 W, KY 0.66, widths 146 / 134.5 / 123 / 111.5 / 100 | x0 = 195 − 1.225·W·(N−½)/N per plane | left-edge row starts match (17.75, 33.72, 49.71, 68.17, 90.00, each within 0.01 mm of prediction); back rows right-flush at 195.0; ink bbox x 17.75–195, y 15.05–281.0 | OK |
| p(tiger_cat) + preprocessing (S7) | 0.43, centre-crop 300² → 224² | top5 [282: 0.43, 285: 0.25, 281: 0.18] | caption line 3 | OK |
| plot budget | 11,537 cmds, draw 13.86 m, travel 3.83 m, F600, 1 s dwells | — | 11,537 cmds, draw 13,858 mm, travel 3,822 mm ✓. **But the gcode is F2200 with G4 P0.2 dwells, not F600 / 1 s** (HANDOFF claim false; the Leo slow-feed rule is not met) | HANDOFF wrong |

## Lies list
| item | status |
|---|---|
| ERF ring is decorative, not a 50 % mass region | clean. All four loops are the 50 %-mass moment ellipses (mass 0.500–0.503), with x extents Δ ≤ 0.33 mm |
| ring about the wrong unit or orientation | clean. "FRONT EDGE = IMAGE BOTTOM" is printed and the summit sits exactly on cell (4,3) (row, col) |
| ERF confused with TRF (TRF 491 px > 224) | clean. TRF is neither drawn nor claimed |
| feature-map resolution misdrawn | clean (soft note). Row count and pitch are monotone and the resolutions are printed bottom→top. Rows are necessarily subsampled; 28² is drawn at stride 1.5 (interpolated rows), 56² at every other row |
| data truncated or omitted from a drawn map | clean. No clipping. 13/13 strong CAM cells visible. The only data ink removed is the 19.6 mm summit halo on row 4, which the exact level-set rings replace |
| scale manipulated to sharpen the story | **VIOLATED (soft, disclosure)**. Each map has its own vertical scale: 0.065 mm/unit on ‖block_2‖ against 0.210 on ‖block_5‖ (3.2×) and 0.206 on ‖block_12‖. So relief rises 3.3 → 7.5 → 10.3 → 20 mm up the stack, while the data's own spread does not rise (range 51.0 → 35.7 → 49.8, CV 0.29 → 0.22 → 0.22). The sheet says only "HEIGHT = ‖ACTIVATION‖". A reader will take "terrain grows taller toward meaning" as a property of the network; it is a design progression (declared in the HANDOFF and ledger A15, not on the sheet) |
| quantities unlabeled | mostly clean (S2 closed). The residue is "RINGS = CAM LEVELS ABOVE 6.9": the rings are CAM − mean levels (raw CAM 15.19–17.69), and the reason 6.9 was chosen (just above runner-up (3,3) = 6.86) is not said |

## Scores
truth 9 · fidelity 8 · legibility 8 · VERDICT: PASS

Every measurable claim on the sheet holds. The four ERF loops are the recomputed 50 %-mass ellipses to
≤ 0.33 mm. The five crimson arcs are the Catmull-Rom level sets of the drawn CAM to ≤ 0.17 mm. Every
top-plane row equals CR(CAM − mean)·1.0524 to 0.01 mm. The front rows correlate ≥ 0.994 with their maps.
The hidden line draws nothing that should be hidden. All 13 strong CAM cells, which r03 was missing,
now show. Row count and pitch are monotone, and the caption now decodes the stack: bottom→top, the height
quantity, signed CAM, ~26 % vs 2 %, and the preprocessing. Fidelity holds at 8, not higher, because the
per-map height scales are undisclosed and manufacture the upward relief gradient. It is one caption phrase
from clean. Legibility holds at 8: the contrast between a tiny summit ring stack (a 2 % cell) and a 25.9 %
input loop lands with the caption. The loops keep a near-constant fraction per plane, so "growth" is read
from the caption, not from the geometry.

## Mandates
PASS. Advisory for r05, the last designer round (non-blocking; the first would cost fidelity if left):
1. **Disclose the per-map height scale (caption line 1, x 17.75–191, y ≈ 22–24).** Measured: 0.065 / 0.210 /
   0.206 mm per ‖activation‖ unit on 56² / 28² / 14², so relief is 3.3 / 7.5 / 10.3 mm on data ranges 51.0 /
   35.7 / 49.8. Expected: either print "HEIGHT SCALED PER MAP" (or state the 3 → 20 mm relief progression
   as a design choice), or put 56²/28²/14² on one activation scale. At 0.065 mm/unit that gives relief
   3.3 / 2.3 / 3.2 mm.
2. **Ring units (caption line 2, right end, x ≈ 130–191, y ≈ 19).** The sheet says "CAM LEVELS ABOVE 6.9". The
   drawn rings are CAM − mean = 6.91 / 7.57 / 8.23 / 8.85 / 9.41, which is raw CAM 15.19–17.69, and the
   floor sits just above runner-up (3,3) = 6.86. Expected: "RINGS = CAM − MEAN 6.9 → 9.4 (ABOVE RUNNER-UP
   6.86)" or equivalent.
3. **Crimson ERF boundary merges with black data rows.** The 14² back arc runs 27.6 mm within 0.5 mm of a
   black row (x ≈ 118–146, y 216–220), and the 28² back arc runs 23.6 mm (x ≈ 121–145, y 166–167). In ink the
   ERF edge is indistinguishable from the row there. Expected: ≥ 0.8 mm separation, by breaking the black row
   under the crimson as the 7² summit halo already does, or ≤ 5 mm of contiguous coincidence.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S8 | **FIXED** | 13/13 cells ≥ 20 % of peak show on the sheet (12 on black ink ≤ 0.01 mm, (4,3) under the ring stack). Height scale 1.0524 mm/unit ≤ 1.9 bound. Catmull-Rom replaces the cos² hills, so there are no invented valleys: the (4,4)–(4,5) midpoint is 4.64, between 5.07 and 4.59. Runner-up (3,3) crests at (142.5, 272.35), which matches the projection |
| S2 | **FIXED** | "BOTTOM → TOP 224² 56² 28² 14² 7²"; "HEIGHT = INPUT LUMINANCE / ‖ACTIVATION‖ OF BLOCKS 2, 5, 12 / CAM − MEAN, SIGNED"; "~26% OF IMAGE VS ONE CELL = 2%" (verified 25.9 % / 2.04 %); the "CRIMSON:" colon problem is gone ("CRIMSON = …") |
| S7 | **FIXED** | "CHELSEA, CENTRE-CROP 300² → 224²" and "P(TIGER CAT) = 0.43" are on the sheet |
| A15 (sci half) | **FIXED** | rows 38/28/19/14/7 strictly decreasing; pitch 1.161/1.427/1.957/2.365/4.243 monotone; breaks per row 3.45/2.89/2.16/0.86/0.57 monotone; shortest run 3.02 mm. The per-plane exaggeration it asked for is now the undisclosed-scale note above |
| S1 | holds | top plane whole, back row ends x 195.0; one basis on all five planes (left-edge starts within 0.01 mm of prediction) |
| S3 | holds (changed) | transform changed from "clipped at 0" to "SIGNED", and the sheet says so; the drawn heights are signed CAM − mean exactly |
| S6 | **NOT FIXED** (process) | still no dossier.md / encoding.md |
| A3 (occlusion, info) | partial evidence | 28² loop has 1 occlusion break (x 108.3–111.7, y ≈ 168); 14² loop unbroken, and my surface model predicts no hidden arc there (max depth ≤ 0), so no break is owed |
| regressions | none | argmax, ERF ellipses (now Δ ≤ 0.33 mm), map data (corr ≥ 0.994) and one basis all still hold |
