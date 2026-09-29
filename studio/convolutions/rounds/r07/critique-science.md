# Science critique — convolutions r07 · machine learning (convolutional networks) · 2026-09-29
render: gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.png
gcode:  gallery/studio/convolutions/trials/pp_convolutions_iterate_v30.gcode (29,134 cmds, 895 strokes: pen0 crimson 49 / pen1 dodgerblue 51 / pen2 black 795; draw 0.50 / 0.85 / 11.30 m; stream order 0→1→2 monotonic)
pass: 2 (LEDGER.md read after the cold pass). There is no dossier.md; the check numbers are encoding.md §4b / §11.

Method (independent of the designer's code). X was rebuilt from the sheet itself. The keyline's d = 0 pass (stroke 894) was closed along the crop to make the region. X is the 6×6-quadrature cell mean of max(d, 0) at every lattice sample. The kernel was recomputed from the LoG formula. Y = K∗X (valid, stride 2) was computed and compared with the rings, collars, dots and stripes parsed from the gcode.

## Check numbers
| quantity | dossier (encoding §4b) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| output grid | 17 × 11 | (37−5)/2+1 × (25−5)/2+1 = 17 × 11 | ring centres on (35.6+14.4i, 35.0+14.4j) | OK |
| read windows | 66 = 37 ring + 26 blank + 3 under card | Σ(11−j) = 66; bins give 37 non-zero visible, 26 zero visible, 3 hidden | 37 ring nodes, 0 missing, 0 extra | OK |
| K = 5×5 LoG σ 1 | −0.9813 · −0.2846 · +0.1540 · +0.1418 · +0.0736 · +0.0187 · Σ 0 · 5 neg | K = ½((r²−2)e^{−r²/2} − mean) gives exactly these values; Σ = 0; 5 negative; K∗u = 0, K∗u² = +4.75 (so crimson = bends up is the right sign) | — | OK |
| max \|y\| over read nodes | 18.731 | 18.731, from X rebuilt off the drawn keyline | — | OK |
| read-node bins | −4:2 −3:4 −2:4 −1:7 0:27 +1:21 +2:1 | identical | ring counts 37/37 exact, sign 37/37, radii 1.98/3.00/4.02/5.04 (pitch 1.02) | OK |
| doubled outer ring, \|bin\| ≥ 3 | 5 nodes | (1,8) −4, (5,2) −4, (3,7) −3, (5,3) −3, (5,4) −3 | exactly these 5, 2nd pass at +0.25 mm (5.29 / 4.27) | OK |
| hidden under card | (4,5) 0 · (5,5) −3 · (4,6) −2 | 0 · −3 · −2 | not drawn; declared in HANDOFF | OK (declared) |
| Y from **inked** dot areas | 66/66 bins exact | 66/66 bins, 39/39 signs (max\|y\| 18.875) | — | OK |
| dots drawn | 180 (x ≥ 1.5) | 176 in the read union + 4 in the head window = 180 | 180 single pen-downs on lattice nodes, 0 missing, 0 extra | OK |
| dropped samples | 36, all ≤ 1.16 mm; next 1.62 | 36, max 1.157; next 1.615 | none drawn | OK |
| dot inked area ∝ x (S10) | within ±20 % | Ø_ink = 2.56·√(x/37.26) | centreline 0.24–2.27 mm, inked = cl + 0.30; area error −0.6 … +3.8 % on 180/180 (0 beyond ±20 %); spiral pitch 0.25 | OK |
| cell-mean vs point sample | declared (c) | at the edge, the point-sampled x would put the area off by up to +23.6 % | HANDOFF says "cell-mean distance" | OK (declared) |
| collar ink ∝ \|w\| | within 0.4 %; crimson = blue within 0.1 % | 19.285·\|w\| mm² | 25/25 taps −0.19 … +0.36 %; crimson 40.857 vs blue 40.862 mm² (−0.01 %); signs 25/25; bare gap to dot 0.618–0.629 mm | OK |
| stripes = level sets of d, Δd 2.1 | 2.10 ± 0.05 | d from the drawn keyline (1,070 points where d ≤ crop distance, so the result is exact) | level residual median 0.003, p95 0.008, max 0.080 mm; levels k = 1…18; 0 stripe points on the read side; stripe ink 5.18 m (≤ 6 m) | OK |
| keyline | one open polyline per pass, ≈ 581 mm, ends on the crop | — | 2 strokes, 583.1 / 583.4 mm; ends (165.99, 197) and (284, 153.2); pass 2 offset 0.300 mm (p1–p99 0.291–0.308), 100 % outside X; stem foot (107.46, 27.80) | OK |
| staircase | union boundary; last riser stops at (197.6, 24.2) | corners (53.6+14.4i, 197−14.4i) | vertices exact to 0.01 mm; ends at (197.6, 24.2); hidden only behind the card; row 0 max x = 0.0 | OK |
| X area in crop | 21,277 · read 9,541 · unread 11,736 | 21,262 · 9,531 · 11,731 (0.25 mm grid) | — | OK (0.1 %) |
| card | 89.6–125.6 × 103.4–139.4, 4 passes at 0.25 mm | = head window (5,6) | 89.6 → 88.85 in 0.25 steps | OK |

## Lies list (encoding §9a)
| item | status |
|---|---|
| kernel not zero-sum / collar ink not ∝ \|w\| | clean (Σw = 0; 25/25 within 0.36 %) |
| convolution vs cross-correlation flip | clean (K is 180°-symmetric) |
| output size / stride / window inconsistent | clean (17×11, stride 2, 36 mm windows, staircase exact) |
| rings not actually K∗X | clean (37/37 visible bins, 37/37 signs) |
| same quantity at two scales | clean (key rings at r 1.979 / 3.00 / 4.018 + 4.27, same as the sheet) |
| inputs hidden by outputs | clean (min bare gap from dot ink to any other mark is 0.57 mm; hatch clipped round the row-11 dots; rings ≥ 0.85 mm off keyline ink) |
| drawn area not ∝ quantity (S10) | clean (−0.6 … +3.8 %; key dots 0.10 / 0.40 / 1.00 of max area) |
| false zero | clean (no dot ⇔ x < 1.5, no ring ⇔ \|y\| < max/8; both keyed) |
| caption not supported | clean (finding rows verbatim; blank nodes: 18 outside X (flat 0) + 9 on interior ramps, so "flat or constant slope" is exact) |
| decorative marks posing as data | clean (every mark type has a key row) |
| declared omissions (a)(b)(c) | clean as declared (riser at 24.2 over x = 0; 3 outputs under the card; cell-mean worded in HANDOFF) |

## Scores
truth 9 · fidelity 9 · legibility 8 · **VERDICT: PASS**

- **truth 9.** Every quantitative claim on the sheet recomputes from the sheet alone. This includes the field, kernel, bins, dot areas, stripe levels, staircase and key wording. The sign convention (crimson = ∇² > 0) is verified on u². Not 10: "dot area = depth in keyline" is a cell mean, and that is said only in HANDOFF. At the rim a point-sampled reading is 24 % off.
- **fidelity 9.** Every channel is exact and uses one scale: area ∝ x, ring count ∝ \|y\|, pen = sign, collar ink ∝ \|w\|, stripe = isoline at 2.1 mm. Not 10: 3 of 66 outputs, including a −3 target, are hidden by the card and are not keyed on the sheet. One node, (5,1), sits 0.018 from a bin edge (q = 2.482). It is correct, but it is the fragile one.
- **legibility 8.** The key now names every mark and states the three-way finding in plain words. The stem shows rim / blank / spine / blank / rim in rows y 78–107. Two things weaken it for a stranger. First, 10 of 22 crimson targets sit on bare paper outside the keyline with no dot (d down to −9.4 mm), and nothing says why ("the window reaches X's edge"). Second, only 9 blank nodes lie on the interior ramps (9 of 38 read nodes inside X), so the "mostly nothing" twist rests on few samples.

## Mandates
None: the round passes. The notes below do not block and are optional for any flavour continuation:
1. Crimson rings outside X. 10/22 crimson nodes have signed d from −9.4 to −0.4 mm, e.g. (0,10) at (35.6, 179.0) and (1,5) at (50.0, 107.0). They sit on dotless paper. Expected: one key clause such as "(where it starts: the window reaches X's edge)". The key currently says only "(where it starts)".
2. Card-hidden outputs. (5,5) = −3 and (4,6) = −2 lie under the card at (107.6, 107.0) and (93.2, 121.4) and appear only in HANDOFF. Expected, optionally: a key note "3 outputs under the card" (S9 accepted as is).
3. Cell mean. Key row 9 says "depth in keyline", but the dots encode the cell-mean depth; edge dots would be up to +23.6 % off as a point reading. Expected, optionally: "mean depth in cell". This is declared in HANDOFF, so it is not a violation.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| S5 (no dossier / encoding) | FIXED | encoding.md v1 exists with §4b check numbers, §9a lies list and §11 checks; all checked above |
| S10 (dot ink area ∝ x) | FIXED | inked = centreline + 0.30; area error −0.6 … +3.8 % on 180/180 (r05: 93/216 over +20 %); Y from ink 66/66 bins (r05: 54/63) |
| S11 (key names every mark, exact finding) | FIXED | 8 rows verbatim to encoding §5 (stripes, staircase, finding lines); block x 204.95–277.0, y 20.2–87.8 incl. title; icon centres at baseline + 1.1 on 35.0 … 85.4; left ink 204.8; no formula line |
| S9 (card hides outputs) | argued, held | still (4,5) 0, (5,5) −3, (4,6) −2 hidden; declared in HANDOFF |
| A18 science half (collars) | held, and the art residue is now met | ink ∝ \|w\| to 0.36 %; bare gap 0.618–0.629 mm ≥ 0.60 on 25/25 |
| regression check (S1 sign, S2 no hidden inputs, S3 dots = outline distance, S8 key truth) | no regressions | sign 37/37 on two pens; 0 dots covered; dot x rebuilt from the drawn keyline matches every dot to ±0.013 mm Ø; zero codes keyed |
