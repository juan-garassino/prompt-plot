# Science critique — millennium-poincare r01 · mathematics (geometric topology, Ricci flow) · 2026-09-29
render: gallery/studio/millennium_poincare/current/pp_millennium_poincare_faithful_v7.png (+ _truewidth.png) · gcode: gallery/studio/millennium_poincare/current/pp_millennium_poincare_faithful_v7.gcode

Method. I wrote my own rotationally symmetric Ricci-flow solver: arc-length gauge, odd-Taylor pole
regularity, RK4. It does not share code with `data/`. Validation on round S³: r² 0.24999 vs 0.25, and
L/r 3.1412. With it I recomputed the neckpinch, the surgery (cut at the neck, round hemisphere caps
of radius h), both extinctions and the 2-D control. I embedded every isochrone in the stated frame
(62 mm/u, axis 62°, β = 40°, section foreshortened ×cos β, cut point (156,199); neck pinned before
surgery, ψ²ds centroid held after) and overlaid them on the parsed gcode. Layer totals: 161 / 81 /
1052 / 12 strokes and 16.29 m of ink, which matches the HANDOFF.

## Check numbers
| # | quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|---|
| 1 | extinction slopes d(ψ²)/dt | A −4.003, B −3.908 | A −4.004, B −3.904 | last A rings ψ² step 0.0401–0.0405 per Δt 0.01 (→ −4.0) | OK |
| 2 | neck / big / small radius at t=0; ratio; R_min | 0.3143/1.4139/0.6765; 0.2223; 0.2213 | 0.3143/1.4140/0.6765; 0.2223; **R_min 0.2167** (limit at big-lobe pole) | start line r = 19.49 / 87.67 / 41.94 mm → 0.3143/1.4140/0.6765 | OK (dossier R_min 2 % high, still > 0) |
| 2b | L₀, volume | 6.0059, 44.574 | 6.0059, 44.574 | — | OK |
| 3 | t_s, neck and lobes at t_s | 0.05465; 0.1197, 1.2447, 0.4709 | 0.054582 (N = 600/1000 converged); 0.1195, 1.2448, 0.4710 | keyline neck ±7.42 mm → 0.1197; A 77.17 mm → 1.2447 | OK (Δt_s 6.5e-5) |
| 4 | T_pinch; d(ψ²)/dt | 0.0628; −1.74 → −1.78 | 0.06281; −1.746 (ψ≈0.085), −1.789 (ψ≈0.053) | — | OK |
| 5 | event order | 0.063 < 0.1171 < 0.3873 | 0.0628 < 0.11713 < 0.38733 | B rings **6**, A rings **33** (t_s + 0.01k, every ψ_max within 0.01 mm of my solver) | OK |
| 6 | L/ψ_max at death | A 3.140, B 3.185 (4.57 → 3.48 → 3.16) | A 3.140, B 3.185 (4.56 → 3.47 → 3.16) | innermost rings de-foreshortened: A 6.40/6.43 = 0.995, B 1.02 (round) | OK |
| 7 | 2-D control | 0.3554 at 0.0547; gone at 0.2405; A₀ 25.346; T 1.0085 | 0.35545; 0.24055; 25.3466; 1.00851 | footer "0.314 → 0.355" | OK |
| 8 | planar CSF | A₀ 3.3180, T 0.5281, iso 0.650 | A₀ 3.3183 (analytic π·1.05625), T 0.5281, iso 0.650 | not drawn | OK |
| 9 | geodesic parallels; stuck loop | s 1.601 / 3.856 / 5.141; length 1.975 | s 1.598 / 3.855 / 5.138; start at 1.651 → 3.854, length 1.9749; start at 1.551 dies at t = 1.572 | red arc chord 38.98 mm = 2·0.3143·62; minor/major 12.53/19.49 = 0.643 = sin 40°; endpoints on the start line (±19.49) | OK |
| 10 | Gauss–Bonnet 2π / 4π | exact | identity 2π(1−ψ_s), ψ_s = 0 | — | OK |
| — | halo neck radii t=0, t_s−0.04…−0.01, t_s | 0.3142·0.2786·0.2501·0.2169·0.1760·0.1197 | 0.3143·0.2786·0.2501·0.2168·0.1759·0.1195 | 19.49·17.28·15.51·13.45·10.91·7.42 mm (t_s−0.05 = 18.82 merged into the start line; only 23 % of that line survives) | OK |
| — | cut caps | radius h, ≤ 1/10 of A | — | chord 14.83 mm = 2·7.42 (0.1197); half-ellipse ratio cos 40°; 14.83/154.3 = 0.096; gap to first ring A 3.0 mm, B 3.6 mm; interior bare | OK |
| — | extinction points | pinned centroids | A a = −91.04, B +49.05 mm | dots at a = −90.75, +49.32 (≤ 0.3 mm) | OK |
| — | grey half-shell = back half of the t_s surface | — | back-shell extreme a = −158.7 mm | −158.3 mm; 23 parallel arcs, all on the back (−a) side; large arcs within 0.3–0.8 mm | OK |
| — | floor 0.8 mm (per pen) | — | — | L1: no crossings and no parallel run < 0.8 mm (only the keyline's identical double pass); L0: contacts are wireframe crossings only; type is ≥ 3 mm from all geometry | OK |

Constants all verify: Poincaré 1904; arXiv dates 11 Nov 2002, 10 Mar 2003 and 17 Jul 2003; Clay
award 18 Mar 2010 and its decline 1 Jul 2010; Hamilton 1982; the literature citations.

**Dossier findings.**
1. R_min is 0.2167, not 0.2213.
2. §2(a) and lie 4 ("the lobes barely move") hold only for the big lobe. The small lobe loses **30 %**
   (0.6765 → 0.4709). That is 0.206 u, which is more in absolute terms than the neck's 0.195 u.
3. Encoding §4 says the lobe halo lines "hug the keyline and merge". They do not.

## Lies list
| item | status |
|---|---|
| 1 tidy row of elongated loops | clean: rings turn round, and gaps widen inward (A 1.49 → 7.55 mm; B 2.50 → 7.32 mm) |
| 2 neck loop shrunk by CSF | clean: the red loop is drawn not shrinking. Caption caveat in mandate 1 |
| 3 2-D pinch | clean: the pinch is the 3-D profile, and the 2-D widening is in the footer (0.355 verified) |
| 4 wrong order / lobes visibly shrinking pre-surgery | order clean. The lobe clause is a dossier error: the sheet correctly shows the true 10.5 mm (A) and 12.75 mm (B) pre-cut shrink |
| 5 fat-neck surgery | clean: 1 : 10.4 |
| 6 uneven / undeclared Δt | clean: grid exact to 0.01 mm in ψ. Minor: at the neck the outermost interval (start line → t_s−0.04) is Δt 0.0146 but reads as one 0.01 step, because the t_s−0.05 line merged |
| 7 surface presented as S³ / globe | clean on the black. **At risk** on L0: an uncaptioned grey lat/long half-shell (x 36–174, y 48–141) reads as a globe, and it contradicts "EACH LINE: THE WHOLE SPACE AT ONE INSTANT" (mandate 3) |
| 8 "every loop contracts" as the proof | clean |
| 9 credit/history | clean: Hamilton named, declined, SOLVED |
| 10 extra pinches/handles | clean |

## Scores
- **truth 8.** Every drawn line is exact to ≤ 0.3 mm against an independent solver. Three caption
  claims are false or misattributed on the sheet: the red ring, "forever", and "each line".
- **fidelity 8.** Time spacing, caps, dots, loop and shell are all quantitatively exact. One
  declared Δt interval reads wrongly at the neck.
- **legibility 7.** The two nests and the order of the deaths land. The §5 correction does not: the
  caption sends the reader to the wrong red object. The "neck races while the lobes stand still"
  read is not on the sheet.

**VERDICT: FAIL**

## Mandates
1. **The "RED RING" caption points at the wrong object, and its "FOREVER" is unqualified.**
   - The only closed red ring on the sheet is the cut: chord 14.83 mm (radius h = 0.12) at (156, 199).
   - The stuck curve-shortening loop is an open 50.9 mm front half-arc. Its chord is 38.98 mm
     (2·0.3143·62), from (138.8, 208.2) to (173.2, 189.8).
   - The footer line at x ≈ 205, y ≈ 20–30 reads "RED RING … LENGTH 2π·0.314 … FOREVER". A reader
     who measures the closed ring gets 0.12, not 0.314.
   - Expected: name the two red marks separately, e.g. "RED ARC: … 2π·0.314, FOREVER ON THE FROZEN
     t = 0 SPACE" and "RED OVAL: THE CUT, RADIUS h = 0.12". The recomputed parking holds only on the
     static t = 0 metric; under the flow that neck is cut at t_s = 0.0546.
2. **The "neck races / lobes stand still" read is not on the sheet, and the footer cites only one lobe.**
   - Measured pre-cut halo band widths are 12.07 mm at the neck (19.49 → 7.42), **12.75 mm** at the
     small-lobe equator (41.94 → 29.19, a = 58 mm, around (190, 250)) and 10.50 mm at the big-lobe
     equator (87.67 → 77.17). Lobe gaps are 1.66–1.95 mm and nothing merges.
   - The footer "NECK 0.314 → 0.120 WHILE THE LOBE LOSES 12 %" (x ≈ 205, y ≈ 75) hides the small
     lobe's −30 %, which is plainly visible upper-right.
   - Expected, in the footer: "NECK −62 % · SMALL LOBE −30 % · LARGE LOBE −12 %". The race is
     relative, not absolute, so say it that way. Do not respace any line.
   - Fix dossier §2(a) and lie 4 to match.
3. **The grey half-shell is uncaptioned and falsifies "EACH LINE: THE WHOLE SPACE AT ONE INSTANT"**
   (footer, first line, x ≈ 205, y ≈ 115).
   - L0 is 161 strokes and 1.69 m of ink, bbox x 36–174, y 48–141. Its geometry is correct: the
     back-shell extreme is −158.3 mm against −158.7 mm recomputed.
   - But these lines are parallels and meridians of the t_s surface, not isochrones. With no caption
     they read as a globe (lie 7).
   - Expected: change the caption to "EACH BLACK LINE …" and add one clause, e.g. "GREY: THE SPACE AT
     THE CUT, TURNED ABOUT ITS AXIS — EACH GREY RING A 2-SPHERE".

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | first round; no LEDGER.md exists for this slug |
