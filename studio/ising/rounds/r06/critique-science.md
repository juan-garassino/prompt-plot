# Science critique — ising r06 · statistical physics (2D Ising, RG block-spin flow) · 2026-09-29
render: gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png (gcode gallery/studio/ising/current/pp_ising_r06_wildcard_v11.gcode; byte-identical to v10 except the timestamp)

**Process finding (4th round running):** `studio/ising/dossier.md` and `encoding.md` still do not exist, so there is no §7 table and no §4 lies list. Every "dossier" cell below is MISSING. The check numbers were derived independently from exact results (Onsager/Yang, Kramers–Wannier duality, the exact row correlation length) and from my own C Wolff simulation. That simulation used L = 243, 150 samples per T, and 3×3 majority blocking at 17 temperatures. The measured values come from parsing the gcode: fan centre fitted at (148.50, 63.00), rms residual 0.04 mm over 570 dashes; 121 rays at 1.450° pitch from 3.00° to 177.00°; rings at r 37.7–57.3 / 60.7–80.3 / 83.7–103.3 / 106.7–126.3 mm, each with 5 slots of 3.92 mm.

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Tc = 2/ln(1+√2) | MISSING | 2.269185 (Kc 0.440687) | hub `2.269185` | OK |
| ray count / T range | MISSING | 0.63 Tc dual (KW) = 1.7484 Tc | 121 rays, 3°–177°, uniform 1.45° | OK |
| angle map: u = K̃ − K (K̃ the KW dual, sinh2K·sinh2K̃ = 1), θ = 90 − 87·u/0.44746 | MISSING | ticks 0.7→155.65°, 0.8→129.95°, 0.9→108.42°, 1.1→73.95°, 1.25→53.28°, 1.5→25.30° | 155.6, 130.0, 108.5, 74.0, 53.6, 25.3 | OK (≤0.35°). A Kc−K map would put 1.5 at 22.3° and 1.25 at 49.4°, so the caption's "K*" has to mean the dual |
| mirror rays = KW duals | MISSING | exact under u → −u | symmetric 1.45° grid about 90° | OK |
| ring-1 c vs exact Onsager nn ⟨ss⟩ (all measurable rays) | MISSING | exact formula (elliptic K) | 72 unmerged rays: rms 0.0045, mean −0.0003, max 0.0174 (at Tc). Sheet prints rms 0.0037, and the ink resolution is ±0.003 | OK |
| Tc ray c_1/c_3/c_9/c_27 | MISSING | sim L=243: 0.710±0.007 / 0.731±0.022 / 0.751±0.057 / 0.806±0.118 (exact c_1 ∞: 0.7071) | 0.724 / 0.750 / 0.745 / 0.801 (sheet prints 0.727 0.752 0.745 0.802) | OK (c_1 is +2σ, a single snapshot) |
| hot rays, c_k per ring (sample) | MISSING | sim 1.0346: .635/.564/.417/.225 · 1.0994: .555/.419/.221 · 1.2349: .454/.277 · 1.3174: .411/.228 · 1.7484: .281 | .623/.544/.382/.233 · .563/.417/blank · .453/.273 · .411/.236 · .273 | OK. The 0.23 cut is honoured: no inked dash is under 0.233 |
| cold rays, c_k | MISSING | exact c_1: 0.9052→0.852, 0.85→0.896, 0.80→0.926, 0.70→0.966. sim 0.951 ring 3: 0.900 | ring 1 at T ≤ 0.9052 (49 rays) and rings 3–27 at T ≤ 0.99 are single solid 19.0–19.6 mm strokes, implied c = 1.00 | **VIOLATED**: gaps inked over |
| arch = ξ(T): 1/ξ = 2(K̃−K) above Tc, 4(K−K̃) below | MISSING | fit r = 47.39 + 22.99·log₃ξ (ring-1 centre = b 1, 23 mm per ×3) | rms 0.32 mm, max 1.28 mm (near the zenith). ξ(3°) = 1.117 exact vs 1.119 drawn | OK. The factor 2 below Tc is correct; without it the rms is 7.2 mm |
| colour = sign (nn same-colour frequency) | MISSING | (1+c)/2 = 0.735 | 0.757 over 441 radially adjacent pairs; hot ring-1 black fraction 0.502 | OK |
| cartouches T=0 c=1 / T=∞ c=0 | MISSING | the two trivial RG sinks | as captioned | OK |

## Lies list
No dossier §4 exists. These items were audited independently:
| item | clean / VIOLATED (where) |
|---|---|
| dash length = c_k (no broken scale) | **VIOLATED**: same-colour dashes are joined across gaps under ~0.6 mm into one pen-down. The whole cold fan x 22–146, y 63–190 (ring 1 at θ 107.4°–177°; rings 3–27 at θ ≥ 91.45°) reads c = 1 where c_1 = 0.85–0.98 |
| "every ray flows to a fixed point but one" (tagline, y ≈ 32) | **VIOLATED**: under RG the Tc ray also flows to a fixed point, the nontrivial critical one. Its own dashes hold at 0.72–0.80 across b = 1…27 |
| "ANGLE = K* − K" (caption line 2) | ambiguous. In RG notation K* is the fixed-point coupling, which here is Kc, but the ink is built on the KW dual K̃ |
| "UNDER 0.23 IS PAPER" | **VIOLATED locally**: 18 of 118 inked ring-slots lose a whole dash to the arch/label halo (n = 4 instead of 5), so a blank slot appears where c = 0.28–0.51 |
| Tc ray carries sign | clean by caption (crimson overrides sign). The Tc ray has uneven passes: rings 1/3 single, rings 9/27 double (weight is not a declared channel) |
| m / ξ / Onsager numbers printed | clean |

## Scores
truth 7 · fidelity 7 · legibility 8 · VERDICT: FAIL

The physics is right. KW-dual angle, exact ξ arch, block correlations and the Onsager check all reproduce against an independent simulation. The failures are one false headline and one broken scale on the ink.

## Mandates
1. **Cold-side dash scale saturates (fidelity).** On the left half of the fan (x 22–146, y 63–190), same-colour dashes are merged into single 19.0–19.6 mm strokes. Ring 1 at T/Tc 0.905 (θ 107.4°) therefore reads c = 1.00 where exact c_1 = 0.852: the drawing should be 3.34 mm dashes with 0.58 mm gaps. Ring 3 at 0.951 Tc reads 1.00 where it should be 0.900. 49 ring-1 rays and every cold ring 3–27 are affected. Make every block spin its own pen-down of length c·3.92 mm ± 0.02. Where 3.92·(1−c) falls below the nib width (c ≳ 0.87), either widen the slot pitch or print `C ABOVE 0.87 READS SOLID`, so that the approach to the T = 0 sink (c_1 < c_3 < c_9 < c_27 → 1) is visible on the ink.
2. **Headline and caption misstate the RG (truth).** The tagline `EVERY RAY FLOWS TO A FIXED POINT BUT ONE` (y ≈ 32, x 100–200) is wrong. Rays below Tc flow to the T = 0 sink (c → 1). Rays above Tc flow to the T = ∞ sink (c → 0). The Tc ray flows to the critical fixed point, and its measured dashes stay at 0.724/0.750/0.745/0.801. Reword it, e.g. `EVERY RAY FLOWS TO ORDER OR TO NOISE  BUT ONE`. The caption `ANGLE = K* - K` also needs fixing: the tick angles (1.5 → 25.3°, 1.25 → 53.6°) prove the map is u = K̃ − K with K̃ the Kramers–Wannier dual. A Kc − K map would put them at 22.3° and 49.4°. Print it as the dual (e.g. `ANGLE = K DUAL - K = 1/2 XI`, since 1/ξ = 2(K̃−K) exactly above Tc), not K*, which a physicist reads as the fixed point.
3. **Halo deletes data (fidelity).** The key says a blank slot means c < 0.23. Yet 18 of 118 inked ring-slots have one dash cut out whole by the crimson arch or label halos. Examples: ring 1 at θ 7.35°–11.7° (T 1.65–1.70, c ≈ 0.29) and θ 21.85°–24.75°; ring 3 at θ 50.85°, 52.3°, 58.1°, 62.45°, 63.9° (c 0.25–0.33); ring 9 at 76.95°, 81.3°, 82.75°; ring 27 at 85.65°, 87.1° (c 0.28–0.43). Expected: 5 dashes in every inked ring-slot. A halo may shorten a dash, but it must never delete one. Alternatively, route the arch through the 3.92 mm slot gaps.

## Follow-up on open mandates
r06 is a wildcard with a new encoding (RG sunburst). The cooling-strip mandates are judged against their intent.
| id | status | evidence |
|---|---|---|
| S3 (printed check the ink proves) | PARTIAL | The printed `ALL RAYS VS ONSAGER RMS 0.0037` is provable on the ink for 72 rays (measured 0.0045). It is not provable for the 49 cold rays, whose ring-1 dashes are merged solid (mandate 1) |
| S7 (coldest band under the title) | FIXED | Superseded: all type sits below the horizon (y < 62). Every cold ray T 0.63–0.80 is fully inked in all four rings, and nothing is blanked by type |
| S8 (say what a stranger can't infer) | FIXED | `TC 2.269185 ONSAGER 1944 EXACT` is at the hub. `DASH LENGTH = NEIGHBOUR CORRELATION` ties the ink to the observable, and `UNDER 0.23 IS PAPER` names the blank. The M-line is moot under this encoding |
| truth regressions | none vs r04 | The Onsager and ξ checks both hold. The new truth defect (mandate 2) is new text, not a regression |
