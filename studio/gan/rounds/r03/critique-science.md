# Science critique — gan r03 · machine learning (GAN training dynamics, game theory) · 2026-09-28
render: gallery/studio/gan/current/pp_gan_two-players-interlaced_v10.png (gcode alongside; 33735 cmds, pens black/crimson/dodgerblue)

Pass 1 (cold). `studio/gan/dossier.md`, `encoding.md` and `LEDGER.md` do not exist. **Finding:** there are
no §7 check numbers to verify and no written channel mapping beyond HANDOFF. Everything below was recomputed
from first principles: Dirac-GAN (Mescheder et al. 2018), L(θ,ψ)=f(ψθ)+f(0), f(t)=−log(1+e^−t),
f'(t)=1/(1+e^t). Simultaneous GD: θ←θ−hψf'(ψθ), ψ←ψ+hθf'(ψθ). Plate frame: centre "+" at (116.40,144.34) mm,
scale S = 26.64 mm / 0.74 = 36.0 mm per unit (taken from the dotted r0 arc).

## Check numbers
| quantity | dossier | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| equilibrium | — | unique fixed point θ=ψ=0; Jacobian eigenvalues ±i·f'(0) = ±0.5i (a centre, not an attractor) | "+" drawn at (116.4,144.3), but title says **NO FIXED POINT** | **NO** |
| gradient flow (h→0) | — | d(θ²+ψ²)/dt = 0 → circle of radius r0 | dotted arc at r = 26.63–26.65 mm (0.740) ✓, but only −100°…+10° (31 % of the circle), not in legend | partial |
| step growth | — | r²_{k+1}=r²_k(1+h²f'²) > 1, per step ×1.0084 at r→0 | spiral strictly expanding ✓ | OK |
| steps to 4.35 from 0.74, h 0.26 | — | 3638–3648 for start angle 23.1–24.4° (strongly angle-dependent: 1520–21351 over all angles) | caption "3642 STEPS"; start angle ≈23.8° | OK |
| end radius | — | first r ≥ 4.35 is 4.41 | caption "R 0.74 TO 4.35" | OK (threshold) |
| ring radii at φ=−90° | — | 34.8 / 51.7 / 76.6 / 113.8 mm | ribbon centres 34.2 / 50.9 / 76.0 / 113.6 mm | OK (≤0.8 mm) |
| ring radii at φ=+90° | — | 28.5 / 42.2 / 62.9 / 93.3 / 139.5 mm | 27.9 / 41.6 / 62.8 / 93.2 / 138.7 mm | OK |
| per-turn radius ratio | — | 1.486 / 1.482 / 1.486 | 1.488 / 1.493 / 1.495 | OK |
| over/under = sign(ψθ) | — | ψθ>0 → warp over, ψθ<0 → weft over | red stubs (under): 2729/2729 in ψθ>0; blue stubs: 1931/1978 in ψθ<0 (47 exactly on the axis); 0 true red–blue crossings | OK |
| float length = h·|ψ|·f'(s)·S (weft), h·|θ|·f'(s)·S (warp) | — | step 168 weft leg 16.0 mm, step 169 13.8 mm, min legs ~2 mm; ψθ>0 warp legs 0.06–4.4 mm | step 168 → float 25.04 mm (x160.07–185.11, y77.7–83.1); step 169 → 22.47 mm; 2.15 mm leg → 11.76 mm float; ψθ>0 warp floats 10.3–28.7 mm, corr with predicted leg −0.34, median ratio 12× | **NO** |
| centre hole (HANDOFF: inside r0 no thread) | — | r never < 0.74 (monotone) | threads down to r = 19.24 mm = 0.534 at φ≈48°; ≈217 mm of ink inside r0 | **NO** |
| path on sheet | — | 2008 mm of trajectory | 1508 mm visible (75 %); leaves the frame first at step 171, r=2.45, 2.9 turns | note |

## Lies list
No dossier §4 exists; checked against HANDOFF claims and the standard Dirac-GAN misreadings.
| item | status |
|---|---|
| "GANs have no equilibrium" (the misconception to correct) | **VIOLATED** — title "NO FIXED POINT" (top, y≈270–285) asserts it; the equilibrium exists and is the "+" |
| float length = leg length | **VIOLATED** — weft floats = leg + ≈9 mm ribbon width; ψθ>0 warp floats are ribbon cross-sections, not |Δψ| |
| centre hole = never-visited states | **VIOLATED** — ribbon ink reaches r=0.534 < r0=0.74 at (≈129,159) |
| over/under carries sign(ψθ) | clean (100 %) |
| continuous-time orbit is a closed circle | partly — correct radius, but drawn as a 110° fragment, unlabelled |
| discrete spiral geometry / direction (CCW) / growth | clean (≤0.8 mm to recomputed at 9 checkpoints) |
| caption numbers (3642 steps, h 0.26, r 0.74→4.35) | clean |

## Scores
truth 6 · fidelity 5 · legibility 6 · VERDICT: FAIL

The trajectory is exact and the over/under sign rule is perfect. It fails because the headline states the
misconception instead of correcting it, and because the float-length channel, which the handoff names as the
thing that carries the quantity, does not carry it.

## Mandates
1. **Title truth.** On the sheet: "NO FIXED POINT" (top-left, y≈270–285 mm). Recomputed: a unique Nash
   equilibrium at θ=ψ=0 with eigenvalues ±0.5i. It is a neutral centre that simultaneous GD repels
   (r² ×(1+h²f'²) every step). The sheet itself draws it as the "+" at (116.4,144.3). Expected: a title that
   says the equilibrium exists but is never reached (e.g. "THE FIXED POINT REPELS"), plus a label on the "+"
   such as "NASH EQUILIBRIUM θ=ψ=0".
2. **Float length must equal leg length (×36.0 mm/unit), or the claim goes.** Measured: weft floats are
   leg + ≈9 mm (step 168: 16.0→25.04 mm at y≈78–83, x 160–185; step 169: 13.8→22.47 mm; a 2.15 mm leg becomes
   an 11.76 mm float). In the ψθ>0 quadrants the on-top warp floats are 10.3–28.7 mm, while |Δψ| there is
   0.06–4.4 mm (corr −0.34). Expected: fitted slope 1.0 and intercept 0 ± pen tip. If floats aggregate many
   saturated steps, the float should equal the summed leg and the legend should say so. Otherwise remove
   "float length = leg" from the encoding.
3. **The r0 circle: hole and orbit.** Ribbon ink reaches r = 19.24 mm (0.534 units) at φ≈48° (≈129,159),
   with about 217 mm of thread inside r0 = 26.64 mm (0.74). Because r grows monotonically, nothing inside r0
   was ever visited. Expected: min thread radius ≥ 26.64 mm, with the ribbon laid outward from the path on
   turn 1. The dotted gradient-flow orbit has the right radius (26.64 mm) but covers only −100°…+10°. Expected:
   the full 360° circle, with a legend entry such as "h→0 GRADIENT FLOW: CIRCLE, r CONSTANT". Without it the
   core contrast (the flow circles, the discrete steps spiral out) does not come across.

Also noted, not mandated: 25 % of the trajectory is clipped by the frame, and the first exit is at r=2.45,
while the caption claims 4.35. Turns 1 and 2 merge with no gap at φ≈30–60° and ≈135°, where the ribbon
(≈11–12 mm) is as wide as the turn spacing (13.7 mm).

## Follow-up on open mandates
None. LEDGER.md does not exist, so this is the first science pass on gan.
