# ising r06 — wildcard (THE SUNBURST: RG fan, Art Deco) · parent: r04 (nominal; nothing inherited) · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/ising/rounds/r06/piece.py \
  --fn ising_rg_sunburst --seed 7 --paper a4 --orientation landscape \
  --palette darkgoldenrod,black,crimson --out gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png
```
- final: `gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png` / `.gcode`, seed 7 (v11 is v10 with only the docstring changed; the gcode is byte-identical apart from comments)
- seed sweep, same code: `gallery/studio/ising/trials/pp_ising_r06_wildcard_v10_s3.png`, `…_v10_s13.png`
- history: v1–v3 were row-spin rays (kept as `draft_rowspins_v3.py`). v4 switched to correlation duty. v5 added the dial, hub medallion and new colophon (the last line was clamped off the sheet). v6 fixed the fit. v7 added the cartouches, but they had broken offsets and collided with the colophon. **v8 is an accidental re-render of v7** (a failed edit). v9 fixed the cartouches and the colophon. v10 gave the hub a larger TC.
- sample cache: `rounds/r06/cache_rg_s7_ff6a62c0c8.npz`, `cache_rg_s3_50cce63f84.npz` and `cache_rg_s13_e4e7d6bbb5.npz`. A cold cache takes 8–14 min per seed. Sampler: `rounds/r06/ising_rg.py`.

## Mandate responses
The wildcard deliberately drops the r02/r04 sheet: no cooling strip, no FK hulls, no sea rules, no coast. Many open mandates therefore target geometry that no longer exists. Each one is answered by the nearest equivalent here.

| id | mandate | status |
|---|---|---|
| A14 | Hot half visibly hot, decreasing by band, no dots | **FIXED in kind.** The hot half is drawn as heat: rays thin out ring by ring into paper. Measured on seed 7: 1.15–1.35 has 17 rays, 165 inked cells, mean dash 1.53 mm. 1.35–1.55 has 14 rays, 75 cells, 1.47 mm. 1.55–1.75 has 13 rays, 65 cells, 1.26 mm. Per ray that is 9.7 → 5.4 → 5.0 cells, so count and size both fall strictly. Seeds 3 and 13 give the same shape. Shortest drawn dash is 0.9 mm (hard floor), and the shortest ring-0 dash is 1.14 mm. No dots |
| A15 | Weight ladder reads at 1 m | **ARGUED.** There is no hull ladder here. The hierarchy is: crimson arch (2 passes) and the Tc ray (2 passes); CRITICAL with 0.9 mm stems; the hub gold ring (2 passes); then hairline rays. Weight marks the fixed-point objects, not domain size |
| A16 | Type off the rules, in tiers | **FIXED.** No text crosses any geometry. The tiers are: CRITICAL (16 mm cap), tagline (2.4 mm), 5-line colophon (1.7 mm cap at 3.4 mm pitch, so 1.7 mm bare between lines), and the hub medallion TC (8 mm cap) with 2.269185 and ONSAGER 1944 EXACT |
| A17 | Upper-left sea pocket | **N/A** (no sea). Dropped with the COOLING STRIP geometry |
| S3 | The printed check must be one the ink proves | **FIXED in kind.** The printed `TC RAY 0.727 0.752 0.745 0.802` are exactly the four crimson dash lengths ÷ 3.92 mm pitch (2.85 / 2.95 / 2.92 / 3.15 mm). `ALL RAYS VS ONSAGER RMS 0.0037` compares the ring-1 (block 1) dash length of every ray against exact −U/2 |
| S7 | Coldest band gets its sea back (no text blanking data) | **FIXED in kind.** No text sits over data anywhere. The only breaks in rays are 1.6 mm occlusion gaps where a ray crosses the crimson arch |
| S8 | Say what a stranger can't infer | **FIXED.** The sheet prints `TC 2.269185 ONSAGER 1944 EXACT` in the hub, says dash length = neighbour correlation, and names the blank as `UNDER 0.23 IS PAPER`. The fixed points are named in the cartouches (`T = 0 C = 1`, `T = INF C = 0`) |
| A2 (keep) | No isolated dots | holds (0.9 mm floor, see A14) |

## What changed from parent
It is a different plate, not a revision. The ORDER moves from a single configuration, window or strip (r01–r05) to a **radial + nested stepped sunburst**. The lineage moves from Nees/Schotter to the **Chrysler crown, Van Alen 1930**. The phenomenon moves from "domain walls at Tc" to **the renormalisation-group flow**: what a configuration looks like after 0, 1, 2 and 3 Kadanoff steps. Tc is the one temperature where that does not change.
- **Angle = temperature**, linear in the duality variable u = K* − K. The zenith is exactly Tc, and mirrored rays are exact Kramers–Wannier duals, so the Deco bilateral symmetry is the model's self-duality. The left/right *asymmetry* of the ink is the physics: order vs. disorder.
- **Ring = one 3×3 majority blocking** (block sizes 1, 3, 9, 27, labelled on the horizon). The rings are stepped terraces separated by 3.4 mm paper arcs.
- **Dash = one block spin** of row 0 at that level (black up, gold down). Its length is c_k(T) × pitch, the measured whole-lattice neighbour correlation at that level. Tone drives duty, never spacing. Cold rays close into solid rays, hot rays dissolve outward into paper, and the ray at Tc (crimson, 2 passes) keeps roughly the same dash ring after ring.
- **Crimson arch** = block size equals the exact Onsager ξ(T). It never closes over the zenith because ξ → ∞. The hot flank sits log₃2 = 0.63 of a ring further out than its dual cold flank (ξ+/ξ− = 2 exactly).
- **Dial**: gold numerals 0.7 to 1.5 at their exact duality angles. The scale is non-linear and compressed near Tc. The hot numerals stand on the ghost rim of rays that flowed away.
- **Two stepped Deco cartouches** hold the fixed points and flank the title. T = 0 is a closed mini-sunburst (the rule applied at c = 1). T = ∞ is honestly empty (the rule at c = 0), with only its hub.
- The type is one centred Deco system: condensed caps with a thick-stem/thin-bar contrast for the title, and wide-tracked caps for the rest.

## Measurements / computations
- 121 independent lattices, 243² periodic. u is linear over ±0.45, giving T/Tc from 0.629 to 1.755. The 34 lattices with exact ξ > 3 run 20 Metropolis sweeps and then 90 Swendsen–Wang sweeps. The other 87 run 120 checkerboard Metropolis sweeps (3-colour mask, because L is odd). Cold lattices start all-up, hot ones random. The cold sector is chosen up (Z2, stated).
- Ring-1 neighbour correlation against exact Onsager −U/2, across all 121 rays: RMS **0.0037** (s7), 0.0034 (s3), 0.0039 (s13). Mean residual +0.0002.
  - The largest residual is the Tc ray itself: 0.727 vs 0.7071, +0.020. The single-sample SD at Tc for N = 59049 is about 0.008 (from C(Tc, L) ≈ 3), so this is about 2.4σ on seed 7. Seeds 3 and 13 give 0.716 and 0.712. It is printed on the sheet as is, with no cherry-picking.
- RG flow of c_k (rings 1, 3, 9, 27), seed 7:
  - 0.63 Tc: 0.981 1.000 1.000 1.000
  - 0.90 Tc: 0.854 0.962 1.000 1.000
  - **Tc: 0.727 0.752 0.745 0.802**
  - 1.05 Tc: 0.608 0.506 0.322 0.210
  - 1.24 Tc: 0.454 0.274 0.089 0.037
  - 1.75 Tc: 0.274 0.095 −0.040 −0.037
- The Tc ray on the other seeds:
  - s3: 0.716 0.764 0.813 0.901
  - s13: 0.712 0.729 0.734 0.753
  - The upward drift at the outer rings is a finite-size effect. At block 27 the whole lattice is only 9×9 blocks, and a finite system at Tc carries a sizeable |m| (0.60 / 0.69 / 0.76 / 0.90 on s7). "The Tc ray holds" is therefore approximate at ring 4. The sheet prints the four numbers so a reader can see the drift.
- Paper threshold: dash floor 0.9 mm ÷ pitch 3.92 mm means correlation under 0.23 is not inked (printed). 680 of 2420 cell slots were dropped, all on the hot side of the zenith or at the arch.
- Ray pitch at the innermost radius (36 mm) is 0.91 mm centre to centre, which is ≥ 0.8 mm.
- Seed choice: seed 7 is the studio default. It was not chosen by the Tc statistic; seed 13 would have looked "better".

## Plot budget (v11, seed 7)
| order | pen | meaning | draw | travel | pen lifts |
|---|---|---|---|---|---|
| 1 | 0 gold (darkgoldenrod) | down block spins + Deco furniture (dial, hub rings, cartouche outer frames) | 1.13 m | 1.87 m | 294 |
| 2 | 1 black | up block spins, horizon, cartouche inner frames, T = 0 mini-fan, all black type | 8.14 m | 3.91 m | 1292 |
| 3 | 2 crimson | Tc ray (2 passes), ξ arch (2 passes), zenith tick, hub TC type | 0.80 m | 0.80 m | 88 |

- Totals: draw 10.07 m, travel 6.60 m (0.66 × draw), 13,227 commands, 3 pens, 2 swaps.
- Estimated time at F600 draw with a 1 s dwell per lift:
  - gold ≈ 2 min ink + ≈ 5 min lifts;
  - black ≈ 14 min ink + ≈ 22 min lifts;
  - crimson ≈ 1.5 min + 1.5 min.
  - About 45–50 min in all. Every layer batches cleanly by ray.
- Travel is high relative to draw because every dash is its own stroke (1,674 lifts). The rays are ordered boustrophedon so each layer walks the fan once.

## Self-critique (Art Deco canon)
| dim | score | note |
|---|---|---|
| concept | 8 | The RG flow is the picture. Symmetry = duality, the blank = the hot fixed point, and the one crimson ray = the unstable fixed point |
| hierarchy | 7 | At 3 m you read the solid half-sunburst, the crimson arch/ray, CRITICAL, then the cartouches. The hub medallion competes a little with the title |
| grid / symmetry | 8 | Centred monument on one vertical axis, with mirrored cartouches and ring labels |
| space | 6 | The hot void is shaped by the data (stepped at ring edges). But the dial numerals 1.25 and 1.5 float alone in it, and the upper-right corner is simply empty |
| craft | 7 | Exact ray spacing, 3.4 mm terrace gaps, clean occlusion at the arch. Inner ring-0 rays at 0.91 mm pitch read grey |
| style (Deco) | 8 | Sunburst, stepped terraces, ziggurat cartouches, gold/black + crimson jewel, thick/thin caps, nested hub rings |
| science | 8 | Real arrays throughout, exact Tc/ξ/duality, and a printed check that equals the ink. The Tc ray drifts at ring 4 (finite size, stated) |

**Single worst thing:** gold carries two meanings (down spin *and* ornament). In the hot half, the gold dashes are data but read as decoration. In a critique of the hub, the gold rings could be taken for data.

## Engine requests
- A `deco` kit (`ray_fan`, `stepped_border`/`ziggurat`, `deco_type` with stem weight) is still unbuilt (STYLES.md kit obligations). This piece hand-rolls `_ziggurat` and `_deco_type` locally. Both are candidates for `engine/kit.py`.
