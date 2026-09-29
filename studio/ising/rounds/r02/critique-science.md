# Science critique — ising r02 · statistical physics (2D Ising, critical phenomena) · 2026-09-28
render: gallery/studio/ising/current/pp_ising_COOLING_STRIP_v9.png (gcode gallery/studio/ising/current/pp_ising_COOLING_STRIP_v9.gcode, 49001 cmds, 5958 strokes: pen 0 black 5944, pen 1 crimson 14)

**Missing inputs (a finding in itself):** `studio/ising/dossier.md`, `encoding.md` and `LEDGER.md` do not exist,
so there are no §7 check numbers, §4 lies list or §5 misconception to grade against. The checks below
come from the brief `studio/physics/ising.md`, the HANDOFF, and the claims printed on the sheet. Each
one is recomputed from exact results (Onsager/Yang) or from an **independent Swendsen–Wang
simulation of the declared setup**: 212 x 137, T/Tc linear 0.70 to 1.80 in x, periodic in y, left edge
coupled to a fixed + wall, right edge free. 2 x 600 plus 2 x 500 decorrelated samples, and the
connected-component labeller was checked against BFS. Sheet values are parsed from the gcode: bonds
are snapped to the 1.3 mm lattice (site centres at x = 10.4 + 1.3(i+½), y = 10.9 + 1.3(j+½)); pass
count = number of distinct perpendicular offset copies (0 / ±0.1 / 0,±0.2 mm).

## Check numbers
| quantity | claim (sheet/brief) | recomputed | measured on sheet | OK? |
|---|---|---|---|---|
| Tc | 2/ln(1+√2) | 2.269185 | used by axis | OK |
| FK critical bond prob p_c = 1−e^(−2/Tc) | — | 0.585786 = √2/(1+√2) | — | OK |
| axis T/Tc 0.70 at left → 1.80 at right, linear | HANDOFF | 1.00 at x = 85.56 mm | 23 ticks, 0.05 step, x = 10.40…286.00; 1.00 tick (red) at 85.56 | OK (exact) |
| lattice 212 x 137 at 1.3 mm | HANDOFF / colophon | 275.6 x 178.1 mm | field x 10.4–286.0, y 10.9–189.0 | OK |
| red frontier mean | `RED ITS EDGE MEAN 1.03 TC` | sim mean of the held cluster's rightmost site per row: 1.036 ± 0.019 (5–95 %: 1.007–1.067) | hull vertex mean 1.034, length-weighted 1.034, per-row rightmost 1.020, range 0.933–1.183 | OK |
| red = hull of the wall droplet | HANDOFF | rightmost rule end = rightmost hull edge | 46/46 ruled rows coincide exactly; no rule lies right of the hull | OK |
| held (ruled) density = P∞ = m(T) (Onsager–Yang) | implicit in "held droplet" | m̄ 0.70–0.80: 0.969 · 0.80–0.90: 0.929 · 0.95–1.00: 0.741; sim held 0.969 / 0.929 / 0.734 | text-free rows 30–110: 0.973 / 0.926 / 0.685; 1.00–1.05: 0.288 (sim 95 % band 0.22–0.67) | OK |
| held droplet size | — | sim 7998 ± 359 sites | ≈ 7895 (ruled-row estimate) | OK |
| free droplets 10–39 sites | "bond sticks" | sim 291 ± 15 | 290 | OK |
| free droplets 40–440 sites | "2 passes" | sim 25.5 ± 4.1 | 22 (all 2-pass, max 154) | OK |
| free droplet ≥ 441 | "3 passes" | sim P(largest free ≥ 441) = 0.046; largest free droplet 231 ± 97 | one droplet, 441 sites (cols 51–77, T 0.97–1.10, y 125–169 mm) | rare (5 % tail), true |
| dots | "droplet dots" (undeclared on sheet) | sim FK droplets of 2–9 sites: 2845 ± 55 total, 2223 ± 45 at T > 1.25 Tc | 2822 total, 2199 at T > 1.25 Tc; 0 wrap bonds drawn | OK: **one dot = one droplet of 2–9 sites** |
| singletons | not stated | sim 3738 ± 63 single-site droplets at T > 1.25 Tc (26 % of those sites) | **0 drawn** | undeclared omission |
| all FK bonds of a drawn droplet | "FK bond sticks" | loops kept (bonds > sites−1) | 154-site droplet: 164 bonds; 441-site droplet: 500 bonds | OK |
| pass rung constant within a droplet | "1/2/3 passes by droplet size" | — | 441-site droplet: 445 bonds at 3 passes, **47 at 2, 8 at 1** (11 % under-inked) | PARTIAL |
| energy vs Onsager | `ENERGY VS ONSAGER RMS 0.013` | sim with the same geometry and 600 samples: per-bond ε RMS 0.003, per-site u RMS 0.006. The printed figure's unit and sample count are not stated | cannot be verified from the sheet | UNVERIFIABLE (plausible order) |
| top/bottom wrap | "wraps top/bottom" | hull must close across the seam | enters the top at column edge 53 and the bottom at 51, closed by 2 undrawn seam edges; droplet fragments of 3/10/11 sites at rows 0–4 carry the 2-pass rung of their full torus droplet | OK |

## Lies list
No §4 lies list exists. These items come from the brief's "⚠ do not restore" block and from the HANDOFF claims.
| item | status |
|---|---|
| "big domain = critical signature" (brief's rejected rule) | clean. Red marks only the wall droplet's hull, and the caption gives its mean (1.03), not a signature claim |
| decorative marks posing as data | clean. Every dot matches a real 2–9-site FK droplet (2822 vs 2845 ± 55) |
| red strictly = frontier of the held droplet | minor. One extra 2-site closed red loop (cells (60–61, 36), T ≈ 1.02, x 88.4–91.0, y 57.7–59.0) is a diagonally pinched lake inside the held droplet, not the frontier |
| "droplets" = spin domains (a reader's default reading) | VIOLATED (caption level). The drawn clusters are stochastic Fortuin–Kasteleyn clusters, but the sheet only says `DROPLET`/`BONDS`. It never says FK, so a physicist reads them as geometric spin domains, which have a different size law |
| weight ladder legible from the sheet | VIOLATED (undeclared). The pass thresholds (10 / 40 / >154), dots = 2–9-site droplets and singletons-not-drawn appear nowhere on the sheet (colophon x 15–75, y 15–45) |

## Scores
- truth **8**. The physics is quantitatively right everywhere I could measure. The ruled density tracks
  Onsager m(T) to within 0.004 in the ordered band, the frontier sits where an independent simulation
  puts it (1.034 vs 1.036 ± 0.019), and the droplet census, the dot census and the axis are exact. It
  loses points because FK clusters are called "droplets" without naming FK, and because the printed energy
  check cannot be verified.
- encoding fidelity **7**. Each channel is data, but the key is missing from the sheet. The dots use a
  per-droplet count, not a per-site density. Single-site droplets (26 % of hot sites) are silently
  dropped. The top rung rests on one droplet whose existence is a 4.6 % event, and 11 % of that
  droplet's bonds are under-inked.
- insight legibility **7**. "Tc is a place" lands. The ruled sea stops at a red coastline next to the
  red 1.00 tick, and droplets coarsen toward it. But the sheet never says that the sea's density is the
  order parameter, or that heavier sticks mean bigger droplets. So "droplets diverge at Tc", the actual
  critical signature, is a guess for a stranger and unprovable for a scientist.

**VERDICT: FAIL**

## Mandates
1. **Key the mark code on the sheet and name the clusters.**
   - Where: the colophon, x 15–75 mm, y 15–45 mm, under `BONDS  THE FREE DROPLETS`.
   - Measured encoding: dots are one per FK droplet of 2–9 sites (2822 drawn vs 2845 ± 55 expected). Single sites are not drawn (≈3738 in the T > 1.25 Tc band alone). Stick passes are 1 for 10–39 sites (290 droplets), 2 for 40–154 (22), and 3 for one droplet of 441.
   - Expected: legend lines that state each rung with its site range (for example `DOT  2 TO 9 SITES`, `1 PASS 10 TO 39`, `2 PASS 40 AND UP`, `3 PASS ...`) plus `SINGLE SPINS NOT DRAWN`, and the word `FK` (Fortuin–Kasteleyn) on the droplet/bond lines. At present no reader can decode the weight channel.
2. **Make the 3-pass rung typical and uniform.**
   - Where: the only 3-pass droplet, 441 sites at cols 51–77 (T 0.97–1.10), y 125–169 mm next to the red hull.
   - Measured: 55 of its 500 bonds (11 %) are drawn at 1–2 passes. A free droplet of ≥ 441 sites appears in only 4.6 % of equilibrium configurations (the largest free droplet is typically 231 ± 97), so the top rung is a seed lottery.
   - Expected: every bond carries its droplet's rung (0 % under-inked). The 3-pass threshold is set where it is populated in most configurations (≥ 155 sites is exceeded with P = 0.79) and printed per mandate 1. The scale ladder then survives any seed.
3. **Print a check the sheet itself proves: ruled density = the order parameter.**
   - Where: the colophon's last line (y ≈ 16.5 mm), `ENERGY VS ONSAGER  RMS 0.013`.
   - Measured: that line has no stated unit or sample count and cannot be verified from anything drawn. Meanwhile the ruled sea's coverage in the text-free rows is 0.973 at T/Tc 0.70–0.80 and 0.926 at 0.80–0.90, against Onsager–Yang m = 0.969 and 0.929.
   - Expected: a line such as `RULED FRACTION 0.97  ONSAGER M 0.97  AT 0.75 TC`, or m(T) ticks along the frontier axis, so that the sea is read as the order parameter going to zero at the red tick. If the energy line stays, state its unit (per bond or per site) and its sample count.
   - Also: keep type halos out of the data rows or say they are halos. Across all ruled rows the coverage at 0.70–0.80 drops to 0.937 because 10–47-site halo gaps sit around the title and colophon.

## Follow-up on open mandates
No LEDGER.md exists for this slug. This is pass 1 only, so there are no open S* mandates to track.
| id | status | evidence |
|---|---|---|
| — | — | — |
