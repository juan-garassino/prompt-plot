# Art critique — ising r02 · canon: UNDECLARED (judged as science_poster; evident order = Nees *Schotter*, order→disorder across the sheet) · 2026-09-28
render: gallery/studio/ising/current/pp_ising_COOLING_STRIP_v9.png (a4 landscape, cream, 2 pens)

HANDOFF carries no `canon:` and no `lineage:` line (LINEAGE rule). No encoding.md; brief = `studio/physics/ising.md`. This round implements DESCRIPTION "Next versions #2 COOLING STRIP", not the brief's hero+deck layout.

## Scores
| # | dimension | score | why |
|---|---|---|---|
| 1 | hierarchy | 6 | At 3 m: red frontier + the black clot at 1.00–1.10 Tc read first, ruled sea second. But the right ~60 % (1.2–1.8 Tc) is one even mid-grey carpet of sticks and dots, and CRITICAL is only ~9 mm cap — the title is not a 3 m element. |
| 2 | grid & alignment | 7 | Strong: every type line sits in a rule gap of the ruled sea (type locked to the 3-row pitch), left rule, ruler origin and type all hang off x=10/15. Faults: 1–3 mm rule stubs left between the x=10 rule and the C of CRITICAL (crumbs), and the ruler starts at 0.70 with no 0.70 label. |
| 3 | tension & asymmetry | 7 | Frontier at ~¼ width with one lobe thrown out to x≈130 at y≈65 — a working asymmetry. Right half has no event at all; tension dies after 1.2. |
| 4 | negative space | 4 | No bare-paper zone anywhere. Left quarter is 45 ruled lines, right 60 % is dotted to the frame on every side. The only void is the halo around the title. Nothing is shaped; the sheet is worked edge to edge. |
| 5 | craft for pen | 6 | 1 swap, rules at ~3.9 mm pitch fine. But: 3-pass bond sticks on adjacent 1.3 mm lattice lines fuse into near-solid clots (x 90–125, y 125–175); thousands of single-site dots = thousands of pen taps (49 001 commands, travel 20.4 m ≈ draw 20.8 m) — a very long, knock-heavy plot for Leo with 1 s dwells. |
| 6 | concept legibility | 7 | Order → frontier → dust reads in one glance: "TC IS A PLACE" is a real twist and the transition is a line you can point at. Held back by the top ruler (a plot axis) and by drawing FK bond sticks instead of domain walls — the free droplets read as circuit/maze glyphs, not coastlines, so "structure at every scale" is weaker than the "a phase boundary exists" message. |
| 7 | depth & dimensionality | 4 | Flat, and flatness is not declared (no canon given). The 1/2/3-pass ladder gives weight variation, not planes. |

avg **5.86** · min **4** · **VERDICT: FAIL**

## Reads at a glance
A ruled, silent left edge breaking at a jagged red coastline into a dense black thicket that dissolves into dust toward the right — order melting into noise across the sheet.

## Acceptance checks (brief `studio/physics/ising.md`; no §11 encoding exists)
| check | result |
|---|---|
| Draws domain walls (dual-lattice edges), not spins, as closed curves | FAIL — ordered domain is ruled (a fill), free droplets are FK bond sticks on the primal lattice; no closed wall loops |
| Line weight = domain scale, 1/2/3 passes, all rungs populated | PASS — visible ladder, heaviest at the frontier |
| Red = the one long-range object, scarce and loud | PASS — one crimson hull, the longest line on the sheet |
| No grid of filled squares | PASS |
| Two pens, one swap; black = type/furniture | PASS |
| Stroke-font charset only (no = / + > \|) | PASS |
| Exact-physics readout on sheet (Tc 2.269185, bonds vs Onsager 0.1464) | PARTIAL — `ENERGY VS ONSAGER RMS 0.013` and `MEAN 1.03 TC`; Tc value and bond fraction absent |
| Quiet zones exist and are shaped | FAIL |
| Title set on halo over the field | PASS (halo in the ruled sea), but at caption scale |
| Canon + lineage declared (LINEAGE rule) | FAIL — neither in HANDOFF |

## Biggest weakness
No negative space and no quiet: the sheet is inked frame to frame, and the hot side spends ~half the plot's commands on single-site dots that carry the least information and flatten the hierarchy into an even grey from 1.2 to 1.8 Tc. The frontier is the idea; everything right of it is undifferentiated texture competing with it.

## Mandates
1. **Stop drawing 1-site droplets.** No isolated dots anywhere on the sheet; state it in the footer (`SINGLE FLIPS NOT DRAWN`). Test: a 40 × 40 mm crop at x 230–270, y 20–60 contains zero isolated dots and shows ≥ 50 % bare cream; travel ≤ 0.6 × draw in the preview stats box.
2. **Unclot the frontier thicket.** In x 85–130, y 120–180 no two parallel inked strokes may sit closer than 0.8 mm clear paper — where top-rung sticks lie on adjacent lattice lines, drop one to 2 passes (or draw the droplet as its closed wall outline instead of its bonds). Test: a 2× crop of that window shows white between every pair of parallel strokes, no solid black cell larger than 2 × 2 mm.
3. **Make CRITICAL a 3 m element and clean its halo.** Cap height ≥ 18 mm, 2–3 passes (giant_type weight), flush-left at x=15 inside the ruled sea (rotate 90° up the sea if width demands), rules halo-broken with no stub shorter than 4 mm between x=10 and the first glyph. Test: title cap height measured ≥ 18 mm on the preview axes; no rule fragment < 4 mm left of the C.

(Process, not visual: add `canon:` and `lineage:` lines to HANDOFF and either declare flatness or give the field a depth device — dimension 7 stays ≤ 4 until one of those is done.)

## Follow-up on open mandates
No LEDGER.md or FEEDBACK.md exists for ising — no open A*/J* mandates to track.
DESCRIPTION.md "If only iterating" / Weak items (informal):
| item | status | evidence |
|---|---|---|
| Delete the order-parameter chart | FIXED | no chart on the sheet |
| One type system, same left axis | FIXED | title, tagline and footer all mono, all flush on x≈15 |
| Remove 1–2-site loops so mid rungs read at 3 m | NOT FIXED | 1-site dots now fill the whole right 60 % — worse than v6's small loops |
| Cold phase has no visual body | FIXED | ordered domain is a ruled sea with measured interruptions |
| Leftover band / gaps (space) | REGRESSED | v6 had bare paper left of the hero and a quiet band; r02 has no bare paper at all |
| Not declared flat (depth) | NOT FIXED | no declaration, deck (the only depth device) removed |

DESCRIPTION § Keep:
| keep item | still true? |
|---|---|
| Crimson interface = the single long-range object, scarce and loud | YES — now a vertical frontier hull; shorter and less branched than v6 but still the loudest line |
| Weight ladder 1/2/3 passes carries data, bold continents give depth planes | PARTIAL — ladder present, but on bond sticks; heavy rung fuses into clots instead of reading as continents |
| Hero cropped flush at top/right edges, window onto the torus | PARTIAL — field is full-bleed to the drawable area on three sides; the asymmetry now comes from the gradient, not the crop |
| Empty crimson 1.00 plate + blow-up rays | NO — removed with the deck (acceptable for this concept, but the best idea of v6 has no successor; the red 1.00 ruler tick does not carry it) |
| Walls drawn exactly on the dual lattice, no crowding ≥1.07 mm | NO — primal-lattice bond sticks; crowding in the frontier thicket |

## Regressions vs compare-to (gallery/studio/ising/current/pp_ising_v6.png)
- **Mark vocabulary**: v6's closed staircase wall loops (islands, continents, coastlines) became open FK bond trees — crosses, T's and combs that read as circuitry/maze, losing the "coastline map" image the brief's reference prompt asks for.
- **Negative space**: v6 had bare paper left of the hero and a quiet band under it; r02 has none.
- **Plot cost**: commands 16 446 → 49 001, travel 6.9 m → 20.4 m (travel now equals draw), driven by single-site dots.
- **Crowding**: v6 held ≥1.07 mm everywhere; r02 fuses 3-pass sticks at the frontier.
- **Title presence**: v6's widely tracked spaced caps spanned ~2/3 of the width; r02's CRITICAL is a compact ~9 mm word that owns less of the sheet.
