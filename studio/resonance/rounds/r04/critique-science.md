# Science critique — resonance r04 · machine learning (attention as wave interference) · 2026-09-29
render: gallery/studio/resonance/current/pp_resonance_one-field_v6.png (gcode gallery/studio/resonance/current/pp_resonance_one-field_v6.gcode, byte-identical to gallery/studio/resonance/current/)

Pass 1 (cold). **Process finding:** `studio/resonance/` has no `dossier.md`, `encoding.md` or
`LEDGER.md`, so there are no §7 check numbers, §4 lies list or §5 misconception to verify against.
The claims checked below are the ones printed on the sheet (caption) and in HANDOFF.md, and every
value was recomputed from first principles (two-source interference) and measured from the gcode.
851 pen-down strokes: pen 0 = 39, pen 1 = 33, pen 2 = 560 (557 dashes + 3-pass softmax line), pen 3 = 219.

## Check numbers
| quantity | claimed (sheet / handoff) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| wavelength λ | 3.4 mm | — | 3.4000 mm (Q: 34 arcs, K: 26 arcs, linear radius fit, residual ≤ 0.002 mm) | OK |
| source separation d | 6λ = 20.40 mm | 20.400 mm | 20.4001 mm = 6.0000λ (crest-fit centres Q (57.994, 232.352), K (76.006, 241.928)) | OK |
| phase constant | +0.09 rad | 2π(r0K − r0Q)/λ | r0Q 4.577, r0K 4.627 mm → 0.0935 rad | OK (rounded) |
| black = sum of Q and K, crest locus | bright-fringe crests | crests at (rQ+rK)/2 = const + mλ/2 (half-wave stagger across adjacent fringes) | residual 0.0098 cyc rms (0.033 mm), max 0.087 cyc; the no-stagger model gives 0.319 | OK |
| fringe orders | — | \|Δ\| ≤ d → m = −6…+6, 13 orders | all 13 present; 0 of 557 dashes cross a node (half-integer) line | OK |
| amplitude envelope (dash extent) | — | 2D cylindrical wave ∝ 1/√r | dash-end amplitude 2\|cos(Δφ/2)\|/√r̄: CV 0.088 (constant amplitude: 0.220, 1/r: 0.370) | OK |
| softmax peak positions | peaks on bright fringes | m = −4…+1 cross y = 78.59 at x = 27.29 / 60.86 / 90.24 / 119.25 / 150.79 / 188.48 | 27.51 / 60.91 / 90.05 / 119.00 / 150.30 / 187.80 (\|Δx\| ≤ 0.68 mm, ≤ 0.016 order) | OK |
| β from peak HEIGHTS | β 6 | softmax(6·s), s = 1/√(rQ·rK) normalised → .1954 .2313 .2176 .1716 .1163 .0679 | height shares .1956 .2316 .2175 .1716 .1160 .0676; β implied per ratio 6.00 / 6.18 / 6.02 / 6.04 / 6.03 | OK |
| β from peak WIDTHS | β 6 | exp(6·s(x)) FWHM at tallest peak = 4.73 mm | drawn FWHM 3.53 mm; all six are 75–81 % of the β=6 width → implied β ≈ 10.8 | **VIOLATED** |
| Q4·K4 cosine | cos 0.748 | arccos 0.748 = 0.7255 rad; source not stated anywhere | no channel on the sheet carries it: the only free phase is 0.0935 rad (cos = 0.9956) | **UNVERIFIABLE / decorative** |
| source markers | Q, K dots | = crest centres | dot centres sit 0.13 mm off the crest centres (below pen width) | OK |
| pen map / order | 0 Q · 1 K · 2 sum + softmax · 3 type; 0→1→2→3 | — | file order 0→1→2→3; pen 3 only in y 10.4–28.1 (caption); Q/K labels on pens 0/1 | OK |

## Lies list
(No dossier §4 exists; these are the lies this subject invites, checked one by one.)
| item | status |
|---|---|
| ink inside dark fringes (sum drawn where Q and K cancel) | clean — no dash crosses a node line; the lowest cos Δφ on black ink is −0.60, only in the near field where the 1/√r amplitude still clears the threshold |
| adjacent bright fringes drawn in phase (no half-wave stagger) | clean — stagger measured, 0.033 mm rms |
| sum crests drawn as circles instead of confocal ellipses | clean — per-dash std of (rQ+rK)/2 median 0.016 mm |
| red/blue crests drawn where Q and K coincide (the axis wedges \|m\| = 6) | clean — black takes over there (41 stray vertices per pen at the wedge edge) |
| equal-height fringes / no decay | clean — 1/√r is carried by both dash length and peak height |
| a datum printed with no quantity behind it | **VIOLATED** — "cos 0.748" (caption line 2, y ≈ 13 mm) |
| one curve, two βs (height reads β = 6, width reads β ≈ 10.8) | **VIOLATED** — softmax row, y 78.6–122.6 |
| an analogy printed as an identity | **VIOLATED** — caption line 1 "q · k = \|q\| \|k\| cos(2π(rQ − rK)/λ + 0.09)": q·k has one value per pair; the drawn field varies across the plane. The correspondence θ_qk ↔ 2πΔ/λ + φ0 is the claim, not an equality |

## Scores
truth 7 · fidelity 7 · legibility 6 · VERDICT: FAIL

The physics is excellent: a Young plate correct to 0.03 mm with the right decay and stagger, and the
softmax heights sit on the bright fringes with weights correct to 0.0004. It fails on the ML half. The
one attention datum (0.748) is decorative. The six-peak softmax is over the fringe orders of a single
Q–K pair, which is not the set of keys that attention normalises over, and the sheet never says what
the six peaks are. A stranger reads a ripple tank and some bumps, with no plotted word for "softmax",
β, "sum" or "key".

## Mandates
1. **Make cos 0.748 a drawn quantity.** Measured: the phase constant between the sources is 0.0935 rad
   (K crest radii offset 0.050 mm from Q's), so the caption's own equation gives cos 0.9956 on the
   zero-path bisector through (67.0, 237.1). Expected: φ0 = arccos 0.748 = 0.7255 rad, which means
   offsetting K's crest radii by 0.393 mm. Alternatively, keep φ0 and draw and label the hyperbola where
   cos = 0.748, at Δ/λ = +0.1006 or −0.1303. Either way the bright fringes and the six peaks move, so
   re-derive them. Put the source (model, layer, head, tokens 4·4) in a dossier with §7 numbers.
2. **The softmax row must carry one β.** Measured: height ratios imply β = 6.00–6.18, but the FWHMs
   are 4.77 / 3.53 / 3.36 / 3.58 / 4.47 / 6.49 mm against 5.91 / 4.73 / 4.45 / 4.72 / 5.56 / 7.38 mm
   for exp(6·s(x)), which implies β ≈ 10.8 (curve at y 78.6–122.6, x 10–200). Expected: draw the
   continuous exp(6·s(x)) profile, whose area shares are .223/.212/.188/.156/.124/.096. Or draw six
   stems whose heights are the discrete weights .195/.231/.218/.172/.116/.068. Under the current
   curve, the x = 27.3 bump has the largest AREA while x = 60.9 has the largest HEIGHT, so the sheet
   gives two argmaxes.
3. **Label the science on the plate (pen 3).** Measured: nothing on the sheet names the bottom curve,
   β, the six peaks, or the black-versus-colour split, and "Q4 · K4" is undefined. Expected: put
   "softmax(β · q·k) along this line" at the curve, and m = −4 … +1 (or the key they stand for) under
   the peaks at x = 27.3 / 60.9 / 90.2 / 119.3 / 150.8 / 188.5. Add a key "red / blue = Q, K alone ·
   black = Q + K where bright". Rewrite caption line 1 as a correspondence (θ_qk ↔ 2π(rQ − rK)/λ + φ0),
   not an equality, and state what the six softmax entries are in attention terms.

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| — | n/a | pass 1: `studio/resonance/LEDGER.md` does not exist; no open S* mandates |
