# attention-weaving r08 — wildcard · parent: r06 (as mandated; no geometry or code inherited) · 2026-09-29

## Render
```
.venv/bin/python scripts/render_candidate.py studio/attention-weaving/rounds/r08/piece.py \
  --fn attention_weaving_wildcard --seed 7 --paper 24x30 \
  --palette black,crimson,forestgreen --out gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.png
```
- final: `gallery/studio/attention_weaving/current/pp_attention_weaving_wildcard_v8.png` + `.gcode`, seed 7 (the truth seed of encoding §4a)
- other seeds, for robustness only (the data changes with the seed): `gallery/studio/attention_weaving/trials/pp_attention_weaving_wildcard_v6_s3.png`, `…_v6_s11.png`
- trail: v1 (full width, linear slerp) → v2 (smoothstep ease, h ∝ bits) → v3 (slope-aware eroded cells) → v4 (uniform key line + footer) → v5 (158 mm measure + void column) → v6 (seeds 3/11) → v7 → v8 (caption trimmed, centres exact on the grid)

## The idea (what is new — nothing from r01–r07 survives)
- **Order:** CONTINUOUS WARP (Psychedelic, STYLES §9). No braid, aperture, hill, wall, slit, weft, streamline or spiral.
- **The twist:** a softmax row is a partition of one, and so is a line of **justified type**: letters share one fixed measure and sit flush at both margins. **Attention is typesetting.**
  - Every line of the sheet = one query's softmax row (22 lines).
  - Every letter = one key. The 16 keys in index order spell `S O F T M A X S U M S T O O N E`.
  - A letter's cell width = a_ij × the measure, exact at the line's centre.
  - Because every row sums to 1, the right edge is flush on all 22 lines and everywhere between them. A leaking softmax would set a ragged right margin.
  - The void column to the right of the measure is there so that this flush edge **can be seen**.
- **Lineage:** Wes Wilson, Fillmore poster for The Association (1966). The order it lends: lettering stretched to fill a field, one warp through every glyph, legibility fought for.
- **Canon kept (Psychedelic):**
  - One displacement function drives everything: the attention CDF of the query at height y.
  - The type is the subject, warped on that field.
  - The complementary pair crimson/green sits at near-equal value.
  - Declared **flat** (a poster canon). Depth is not claimed.

## Mandate responses
The LEDGER's open mandates are written for the aperture encoding. This wildcard retires that geometry, so most rows are answered by construction or argued as not applicable. None is skipped.

| id | mandate | response |
|---|---|---|
| J1 | bring the bottom half up to the top | **FIXED by construction (Juan closes).** The plate has no top/bottom split. All 22 lines follow one grammar, and the lower lines are as loud as the upper ones: the bottom line has Q13's `SO` + `A` at 2 rings. |
| J2 | softmax smoother, not a ziggurat; partition exact | **FIXED (Juan closes).** No profile or staircase exists. The softmax is the letter widths, and those edges are C¹ curves in y (smoothstep-eased slerp of the query). Exactness: row-sum error 2.2e-16; right-edge error 5.7e-14 mm on all 4,600 warp samples; cell edges at every line centre = x0 + W·cumsum(A_i) to 2.8e-14 mm. |
| A2 / A7 | V as one closed sweeping family, no crumbs | **ARGUED, n/a.** There is no V strand. V is not drawn (see "What is not encoded"). No stroke ends in open paper: every stroke is part of a glyph. Glyph pieces shorter than 0.6 mm are dropped where a cell closes. |
| A6 / A21 | bare left-middle void | **ARGUED / replaced.** The quiet zone is now a 52 × 180 mm bare column right of the measure (x 178–230, y 100–290). It is shaped by the flush right edge of the type. |
| A11 | labels anchored, ≥ 2 mm clear of strands | **FIXED.** All text is in the caption column or under the uniform key line. The nearest text to any coloured ink is 10 mm (the gutter). |
| A13 | giant type craft: same construction for every stroke | **FIXED in spirit.** Every glyph is built one way: a skeleton plus distance-field rings at a constant 0.9 mm pitch (level sets of distance, \|∇d\| = 1). No striped multi-pass strokes. |
| A14 | travel > draw | **FIXED.** Draw 23.12 m vs travel 9.30 m (ratio 2.49; r06 was 0.96). |
| A15 | concept reads as a physics figure; brief's braid gone | **ARGUED.** This is the wildcard's direct answer. No figure, no apparatus. The mechanism is carried by an object the viewer already holds (a justified line of text), and the braid is dropped on purpose. |
| A16 | pens > 4 | **FIXED.** 3 pens. |
| A19 | throat narrow and loud | **ARGUED, n/a** (no throat). The loud element is Q11's line: the tallest (20.1 mm) and the only 3-ring letter (`A`, a = 0.190). |
| A20 | no caption in the storm | **FIXED.** No text inside the type field. |
| A22 | reed mouths ≥ 3 mm apart | **ARGUED, n/a** (no reeds). Inter-letter ink clearance is ≥ 1.10 mm (measured). |
| S5 | encoding with A checkable | **FIXED.** Uses encoding.md §4a exactly: seed 7, same draws, T = 2.29842, A reproduces the §4a table (Q0 and Q11 rows checked digit for digit). The caption prints the line order, so each line can be matched to its row of A. |
| S6 | hill axis | **ARGUED, n/a.** The uniform key line (every a = 1/16) is the axis: compare any cell to the key line's equal cells. |
| S8 | lane identity | **FIXED by construction.** A line IS a query (row i). Order is seriated (min L1 jump between neighbours, Q11 pinned at slot 7) and printed: `19 8 4 1 20 9 7 11 12 10 14 5 15 17 3 2 18 21 0 6 16 13`. |
| S9 | Q_i and Z_i in the same bin | **ARGUED, n/a** (no Z lanes). |
| S10 | printed rule checkable; index the reed | **FIXED.** Keys are indexed k0–k15 under the uniform line. Ring count = floor(16a) is countable per letter. |
| S11 | rule vs craft floor conflict | **FIXED.** The rules are floor(16·a) rings and crimson ⇔ a ≥ 1/16, applied at 352/352 letters with no override. The nearest a to any k/16 boundary is 6.0e-4 (in sixteenths), so no rounding ambiguity. |

## What changed from parent
Everything; see "The idea". Composition moves:
- The sheet is one tall justified column: measure x 10–168 (158 mm), y 32–290.
- A **uniform key line** sits under the column. `SOFTMAXSUMSTOONE` is set in black, each cell exactly 1/16. It is not a query: by the height rule a query with H = 4 bits has zero height.
- A bare void column on the right; the caption is bottom-aligned in it to the key line's label baseline.
- Row heights are **strictly proportional to 4 − H_i bits** (84.76 mm/bit, h0 = 0). The most focused query gets the tallest line.

## Measurements / computations
- **A** (22×16) = softmax(√16·QKᵀ / T), T = 2.2984249526 (64-step bisection to a_max = 0.190).
  - Row-sum error 2.2e-16.
  - Q11 row: a_max 0.190 at k5 (`A`), then k11 `T` 0.139, k12 `O` 0.079, k2 `F` 0.066.
  - H11 = 3.762 bits, the most focused row; Q14 is the least (0.060 bits → 5.12 mm line).
- **Line heights (top → bottom, mm):** 14.77 14.07 13.83 8.69 16.08 10.91 7.92 **20.14 (Q11)** 12.10 9.11 5.12 10.76 17.62 13.03 8.65 10.83 11.63 7.15 7.68 14.59 9.14 14.18.
- **The warp:**
  - Between line centres, q(y) = slerp(Q_r, Q_{r+1}, smoothstep(f)). Every y then has a real softmax row (unit query, same K, same T); warp row-sum error 4.4e-16.
  - Line centres are inserted exactly into the 0.05 mm y-grid, so the edges there are exact.
- **Rings:** 216 letters with 0 rings (green) · 122 with 1 · 13 with 2 · 1 with 3 (Q11 × k5). Crimson = 136/352, matching encoding §4a's bold count.
- **Clearances (measured on the emitted polylines):**
  - Min distance between inks of different letters: 1.10 mm. This is the vertical leading at the right edge; the side clearance is slope-aware, CLR·sec θ per cell edge, eroded over the ring's vertical reach.
  - Ring pitch 0.9 mm (distance field).
  - Min glyph height 2.22 mm, min glyph width 1.60 mm.

## Plot budget (seed 7, v8)
| layer (stated order) | pen | meaning | draw | travel | pen cycles | est. min* |
|---|---|---|---|---|---|---|
| 1 | 2 forestgreen 0.3 | keys receiving a < 1/16 (single skeleton) | 6.84 m | 3.61 m | 298 | 26 |
| 2 | 1 crimson 0.3 | keys receiving a ≥ 1/16 (skeleton + floor(16a) rings) | 14.03 m | 3.66 m | 408 | 42 |
| 3 | 0 black 0.3 | text layer: key line, k-labels, caption | 2.25 m | 2.00 m | 628 | 31 |

- Total: 23.12 m draw, 9.30 m travel, 30,785 commands, 1,344 lifts. **About 100 min at Leo's slow settings**, plus 2 swaps and the frame trace. The promptplot estimator says 14.7 min at default feeds.
- \*Estimate: F600 = 10 mm/s draw, about 33 mm/s travel, 2.5 s per lift cycle.
- Order: green → crimson → black. Green and crimson never touch (≥ 1.1 mm), so the order only keeps the darkest, text, pen last.
- Every stroke is one glyph piece (batchable); the longest is a ring around one letter.

## Self-critique (rubric, honest)
| dimension | score | note |
|---|---|---|
| Hierarchy | 6 | At 3 m you see a vibrating crimson/green column and a void. The loudest marks are Q11's 3-ring `A` and Q15's 2-ring `S` (y ≈ 140), which compete, so there is no single dominant. |
| Grid & alignment | 8 | Measure, key line, labels and caption share x0, the measure edge and the key-line baseline. The right edge is flush to 1e-13 mm. |
| Tension & asymmetry | 7 | Flush-left column against the right void. Crimson masses drift as data "rivers" (k0 `S` down the left in the lower half). |
| Negative space | 7 | One generous shaped void (52 × 180 mm) that makes the justified edge legible. Inside the column the canon fills every void by design. |
| Craft | 7 | Clean constant-pitch rings. Thin lines (5–7 mm) flatten crimson letters into racetracks, and some green letters in steep warp zones melt into near-horizontal hairs (intended, but legibility is spent there). |
| Concept | 7 | "Justified = sums to one" lands at 1 m once you see `SOFTMAXSUMSTOONE` repeated at different widths above the uniform line. Z = AV and V are not on the sheet. |
| Depth | declared flat | Psychedelic poster canon. |

**Single worst thing:** hierarchy. No single element dominates at 3 m. Q11's line is the tallest (20.1 mm) but only 1.14× Q15's (17.6 mm), because the bits data is not extreme and the mapping is kept strictly proportional.

## What is not encoded
V and Z = AV are absent. This plate is only A = softmax(QKᵀ/T), read row by row. Adding a value carrier would dilute the one joke; if wanted, a follow-up could set each line's colour by the sign of a Z_i component.

## Engine requests
- A kit `warp_type(text, field)` (STYLES "psychedelic kit") would make this reusable. Here it is bespoke: glyph skeletons in a unit box → per-cell warp with slope-aware eroded cells → distance-field rings via contourpy.
- A polyline simplifier (`rdp`) in `engine/geometry.py`. Contour output was 272k commands before a local RDP at 0.025 mm.
