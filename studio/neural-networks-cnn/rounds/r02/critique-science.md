# Science critique — neural-networks-cnn r02 · machine learning (CNNs, receptive fields) · 2026-09-28
render: gallery/neural-networks/cnn/current/pp_neural_networks_cnn_one-valley_v12.png (+ .gcode, 26641 cmds, pen0 14250.9 mm / pen1 1025.9 mm)

Process finding: `studio/neural-networks-cnn/` has **no dossier.md, no encoding.md, no LEDGER.md**. There
are no §7 check numbers, no §4 lies list, no §5 misconception to grade against. Check numbers below are
derived from the HANDOFF claims and recomputed independently (TF 2.16.2 MobileNetV2 ImageNet weights,
skimage `chelsea`, in a throwaway uv env; `.venv` has no TF). The lies list is the standard CNN/ERF set.

## Check numbers
| quantity | claim (HANDOFF) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| top-1 class, p | tiger_cat 0.43 | tiger_cat 0.4290 (center crop, PIL bicubic). Varies with resize: bilinear 0.375, lanczos 0.441, nearest 0.463; full-frame squash gives Egyptian_cat top-1 | caption "P(TIGER CAT) = 0.43" | OK (depends on preprocessing, which the sheet doesn't state) |
| CAM argmax unit | (4,3) | (4,3), CAM 18.09 (npz 18.28) | apex (145.4, 267.5); projected cell (4,3) center x=144.8; crimson isolines x 132.9–155.2 vs cell x 134.9–155.9 | OK |
| ‖block_2/5/12‖ height maps | from MobileNetV2 | corr vs npz 0.995 / 0.994 / 0.999 | not decodable (no scale) | OK (data) |
| ERF 50% ring, input 224² | 50% gradient mass | moment-ellipse holding 50% has x-width 92.3 mm, center x 103.1 | ring x 51.6–148.4 (96.8 mm, center 100.0), encloses ≈53.6% | OK |
| ERF ring, 56² | 50% | 78.1 mm, center 105.3 | 65.5–145.1 (79.6 mm, center 105.3), ≈51.5% | OK |
| ERF ring, 28² | 50% | 66.5 mm, center 114.7 | 80.0–149.2 (69.2 mm, center 114.6), ≈53.3% | OK |
| ERF ring, 14² | 50% | 57.0 mm, center 124.6 | 94.4–154.5 (60.1 mm, center 124.5), ≈53.8% | OK |
| ERF as a fraction of the layer | — | 50%-mass ellipse ≈ 27/27/27/23 % of plane area; sd_u 0.24→0.22 (roughly constant in image coordinates) | ring/plane width 0.64 / 0.61 / 0.61 / 0.59 | OK |
| top-layer height | ReLU(CAM − mean) | mean 8.283; 27/49 cells → 0 even though 48/49 raw CAM > 0 (range −0.77…18.28) | peak 10 : secondary (4,1) 5.67, drawn apex ≈67 mm, left hill ≈38 mm (6.7 mm/unit, consistent) | data OK. Threshold not stated on the sheet |
| top plane extent | 7×7 whole | front row 75.5→196 (W 120.5); back rows should end at x≈205–216 | **6 polylines stop at exactly x=200.000 (y 205.8–221.1)** | **VIOLATED (clipped)** |
| plane widths | stacked pyramid | 224/56/28/14/7 | 152.2 / 130.7 / 113.8 / 102.4 / **120.5** mm | top plane breaks the monotone shrink and uses a different basis (left edge Sx/D 0.58 vs 0.84 below) |

## Lies list
| item | status |
|---|---|
| ERF ring is not a 50% mass contour (decorative ellipse) | clean: 51.5–53.8% enclosed, centers within 0–3.1 mm |
| ring drawn about the wrong unit / wrong orientation | clean: rows run back (row 0) → front (row 6), consistent across CAM apex, rings and rails |
| ERF confused with TRF (TRF 491 px > 224 image) | clean: TRF isn't drawn, but nothing on the sheet names either one |
| feature-map resolution misdrawn | clean-ish: column crossings per scanline ≈ 40–53 / 25 / 12–16 / 7–9 for 56/28/14/7 |
| data truncated or omitted from a drawn map | **VIOLATED**: top CAM plane clipped at the right margin x=200. Col 6, rows 0–5 partly lost, incl. (1,6) = 2.57 (26% of peak) and (4,6) = 2.74 |
| scale manipulated to sharpen the story | **VIOLATED (soft)**: ReLU(CAM − mean) zeroes 55% of cells, so the peak looks more singular than the raw CAM (18.3 vs 14.0 for the runner-up). Not disclosed on the sheet |
| quantities unlabeled (stranger can't decode) | **VIOLATED**: no layer names or resolutions, no legend for crimson, no "50%" anywhere |

## Scores
truth 7 · fidelity 7 · legibility 5 · VERDICT: FAIL

The core science checks out: the forward pass, the argmax cell and all four ERF rings match to within a
few percent, and the rails correctly join the ring extremes into a cone that closes on cell (4,3). Truth
and fidelity fail on the clipped top plane, the undisclosed threshold and the top plane's odd basis and
size. Legibility fails because nothing on the sheet says what the five terrains are or what the crimson
means.

## Mandates
1. **Top CAM plane clipped (upper right, x=200, y 205–222).** Six terrain polylines end at exactly
   x=200.000. With the front row at 75.5→196 mm, the back rows should run to x≈205–216. Part of col 6,
   rows 0–5 is missing, including (1,6) = 2.57 and (4,6) = 2.74 (26–27% of the peak). Draw the whole
   plane inside the frame, on the same basis as the four planes below (Sx/W 0.225, D/W 0.27). Its width
   must be ≤ the 14² plane's 102.4 mm (it is 120.5 mm now), so the pyramid shrinks monotonically.
2. **Nothing identifies the layers or the crimson ring (whole sheet; caption at y≈232 only gives
   p=0.43).** Label the five planes: INPUT 224² · BLOCK_2 56² · BLOCK_5 28² · BLOCK_12 14² · CAM 7²
   (tiger_cat). Add a crimson key: "50% of ∂CAM(4,3) gradient mass". Add the measured contrast: the
   ring covers ≈27% of the image, the unit's own cell covers 1/49 = 2%. Without this, a stranger reads
   black waves and red loops.
3. **Top-terrain threshold not disclosed (top plane, y 190–268).** Height is ReLU(CAM − 8.28). That
   zeroes 27 of 49 cells, although 48 of 49 raw CAM values are positive (−0.77…18.28). The drawn
   peak-to-runner-up ratio is 10.0 : 5.67 against a raw 18.28 : 13.95. Either draw min-offset raw CAM,
   or print "CAM − MEAN, CLIPPED AT 0" beside the plane so the "one peak" isn't read as the model's
   raw output.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | no LEDGER.md exists for this slug; this is a pass-1 review |
