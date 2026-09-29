# Art critique — ising r06 · canon: art_deco · 2026-09-29
render: gallery/studio/ising/current/pp_ising_r06_wildcard_v11.png  (lineage: Van Alen, Chrysler crown 1930 · declared flat)

## Scores
| # | dimension | score | note |
|---|---|---|---|
| 1 | hierarchy | 8 | The half-sunburst owns the sheet at 3 m. CRITICAL (~17 mm) is a clear second, the crimson spire plus TC hub a third, and the cartouches and caption reward 30 cm. The crimson arch is loud but scarce, which is correct. |
| 2 | grid & alignment | 7 | One strong vertical axis (zenith → hub → BLOCK → CRITICAL → caption). The ghost-dial numerals sit on one radius (measured 135–139 mm from the hub) and the ring labels 1/3/9/27 sit under their rings. Against that: both crimson arch feet stop in mid-air at about (113,67) and (198,67), 7 mm above the horizon rule and touching nothing. The horizon runs 72 mm past the right edge of the fan to x≈277 with nothing on it. |
| 3 | tension & asymmetry | 7 | Deco permits the symmetric frame. The tension comes from the data: solid black order on the left, a fraying wedge on the right, and a void where the disorder is. That works, but every piece of furniture (cartouches, type, horizon) is mirror-centred, so the only asymmetric thing is the fill. |
| 4 | negative space | 7 | The upper-right void is earned, since "under 0.23 is paper". The ghost-dial numerals 1.1, 1.25 and 1.5 shape it. The top is pinched, though: the zenith tick sits at 193 and the 0.9 and 1.1 numerals at ≈190, 7–10 mm under the margin, while the bottom band stacks CRITICAL, tagline and five caption lines with 3–5 mm gaps. The vertical rhythm is whatever was left over, not a repeated interval. |
| 5 | craft for pen | 7 | Three pens, one swap each, in a sensible gold → black → crimson order. The innermost ring (block 1, r≈39 mm) runs at about 0.98 mm ray pitch, which leaves roughly 0.6–0.7 mm clear with a 0.3–0.4 tip. That is borderline. The crimson arch crosses about 60 black rays on the left (ink on ink at every crossing). Travel is 6.6 m against 10.1 m of draw (0.65×) because of the dashed gold/black right half. Type is clean. |
| 6 | concept legibility | 7 | A stranger reads it as order on one side dissolving into paper on the other, with a spire at the turning point. The "BUT ONE" does not land from the data, though. The zenith ray is singular only because it is crimson: the 5–8 rays just right of it look the same in rings 1 and 3. The polar dial (T numerals, block-scale axis, two legend cartouches) pulls it back toward a polar plot. The T=0 / T=INF cartouches are the wit and they work. The mirror rays as Kramers–Wannier duals are invisible on the sheet. |
| 7 | depth & dimensionality | 6 | Flatness is declared, but the plate does not use Deco's own depth device, thin/thick alternation. Every ray in all four rings is the same single-pass weight, so the rings read as one comb with gaps rather than stepped setbacks. Only the double gold hub ring has any weight play. |

avg **7.00** · min **6** · VERDICT: **FAIL**

## Reads at a glance
A gold-and-black Deco sunburst rising from a horizon. Its left half is solid black and its right half frays into dashes and then paper, with a crimson onion-dome spire drawn over the top and CRITICAL set beneath it.

## Acceptance checks
There is no `encoding.md`, `BRIEF.md` or `FEEDBACK.md` for ising (the ledger records this process gap), so there are no §11 checks. Instead I checked the HANDOFF's declared encoding against the ink:
- angle = T, with the zenith as Tc and a readable dial: **PASS** (numerals 0.7–1.5 on one radius, TC 2.269185 at the hub)
- ring = 3×3 majority blocking at 1/3/9/27, readable: **PASS** (labels under rings, four ring bands visibly separated)
- dash colour = sign of the block spin: **PASS** (black ordered side, gold/black mix on the hot side, keyed in the caption)
- c < 0.23 not inked, so disorder becomes paper: **PASS** (outer rings vanish first on the hot side, an RG staircase envelope)
- arch = ξ(T) peaking at Tc: **PASS** (bell rising to the zenith)
- mirror rays = Kramers–Wannier duals: **FAIL** (nothing on the sheet shows the pairing; it lives only in the caption)
- the Tc ray is the one that does not flow ("BUT ONE"): **PARTIAL** (it is singled out by colour, not by the marks)
- lineage, would it hang beside the Chrysler crown: **PARTIAL**. The stepped cartouches and the radiating arches take the crown's order, not its look, which is good. The crown's force, though, comes from nested setbacks of increasing weight, and this fan has one weight.

## Biggest weakness
The single claim of the plate, "every ray flows to a fixed point but one", is made by colour rather than by the drawing. The zenith ray sits inside a continuum of near-identical neighbours, and the fan has no thin/thick setbacks. At 1 m the sunburst therefore reads as a uniform comb eroding gradually, not as a crown with one unbroken needle.

## Mandates
1. **Make the needle singular by space and weight.** Clear a paper channel of one ray on each side of the zenith (≈±1.5°) through all four rings. Draw the crimson Tc ray at 2–3 passes as one continuous or tightly dashed line from the gold hub rim to the zenith tick. Test: at 25 % zoom the zenith reads as one bright crimson line splitting the sun, with bare paper on both sides from y≈100 to y≈190.
2. **Stepped Deco weight by block scale.** Ring 27 at 3 passes, ring 9 at 2, rings 3 and 1 at 1, so line weight carries the coarse-graining level and the rings read as Chrysler setbacks rather than a comb with gaps. Keep ≥0.8 mm clear in ring 1: if the 3-pass outer ring or the ring-1 pitch would break that, thin ring 1 to every other ray rather than shrink the gap. Test: at 1 m the outer ring is visibly the heaviest band on the left half.
3. **Land the spire.** Both crimson arch feet, now at about (113,67) and (198,67), must end ON a structure: the horizon rule at y=60 or the outer gold hub ring. The two open spire tips at y≈190 must meet the zenith tick so the arch closes into one built needle instead of two cut curves. Test: no crimson endpoint is more than 0.5 mm from another inked line.

(The top pinch and the right horizon overrun from dims 2 and 4 are secondary. Fix them only if they follow from the three above.)

## Follow-up on open mandates
| id | status | evidence |
|---|---|---|
| A14 | PARTIAL | The heat gradient now reads: dash count and length fall visibly from 1.15 to 1.75 Tc, and the outer rings drop first. But in the 1.55–1.80 wedge only rings 1 and 3 (x≈185–205) carry marks, so most 20×20 cells in that band are empty, not "≥1 mark, ≥50 % bare". |
| A15 | NOT FIXED | There is no weight ladder at all in r06. Every ray is single-pass and the only multi-weight element is the gold hub ring (see mandate 2). |
| A16 | PARTIAL | The type is off the rules and tiered (CRITICAL / tagline / 5-line caption, ≈1.4 mm bare between caption lines). The statement line "EVERY RAY FLOWS TO A FIXED POINT BUT ONE" is ≈2.5 mm cap, under the required ≥5 mm. |
| A17 | FIXED | Obsolete. There are no sea rules or hull pocket any more, so the stop-short condition cannot occur. |
| A2 (must stay fixed) | REGRESSED | There are no isolated dots, but travel is 6597 / 10072 = 0.65× draw, above the ≤0.6 ceiling (r04 was 0.55). |
| A9 (must stay fixed) | PARTIAL | The ring-1 ray pitch is ≈0.98 mm at r≈39 mm, so clear paper between strokes is ≈0.6–0.7 mm with a 0.3–0.4 tip, under 0.8 mm clear. The crimson arch also crosses about 60 black rays. |

## Regressions vs compare-to (r04 v5)
- **The weight ladder is gone entirely.** DESCRIPTION § Keep "line weight = domain scale (1/2/3 passes)" is no longer true. r04's ladder was faint; r06 has none.
- **The frame-cropped asymmetry is gone.** r04 was flush-left with a vertical CRITICAL spine and the field running to the right margin. r06 centres every piece of furniture on one axis, so § Keep "hero cropped flush at top/right edges" is no longer true. Deco permits this, but the sheet's main asymmetry now rests on the fill alone.
- **The crimson long-range object is reduced.** § Keep "one long fractal coastline": r06 replaces it with a smooth ξ(T) arch. That is scarce and loud but no longer fractal, and its feet float.
- Travel ratio worsened from 0.55× to 0.65× draw (A2).
- § Keep "walls exactly on the dual lattice as staircases": no longer present. It survives only as an echo in the stepped cartouche frames.
- § Keep "Tc is not in the row, it IS the sheet": still true in spirit. The zenith is Tc and the whole fan is organised around it.
- Gains over r04, for balance: the hot half finally reads as heat, hierarchy is much clearer, the type is off the rules, and the art avg rose from 6.71 to 7.00 with the min unchanged at 6.
