# orrery r02 — orbits-that-mean (mechanism) · parent: r01 · 2026-09-28

## Render

```
.venv/bin/python scripts/render_candidate.py studio/orrery/rounds/r02/piece.py \
  --fn orrery_orbits_that_mean --seed 7 --paper a4 \
  --palette goldenrod,dodgerblue,crimson,forestgreen,black \
  --out gallery/studio/orrery/current/pp_orrery_orbits-that-mean_v13.png
```

- Final: `gallery/studio/orrery/current/pp_orrery_orbits-that-mean_v13.png` + `.gcode`, A4 portrait, cream.
- Seed: 7. The piece draws nothing random, so the seed does not matter: seeds 3, 7 and 11
  give byte-identical gcode bodies (md5 `13b9c13d…` on v12, checked).
- Data: `gpt2_head.npz` (in this round), written by `mechanism.py` (in this round). To
  regenerate it: `.venv/bin/python studio/orrery/rounds/r02/mechanism.py --layer 4 --head 3 --upto 4`
  (it fetches GPT-2 small by HTTP range request, or pass `--weights model.safetensors --aux <dir>`).
- Self-rounds: v1 → v13 (13 renders, none overwritten).

## Lineage

**Baroque celestial cartography: Andreas Cellarius, *Harmonia Macrocosmica* (1660–61),**
especially the Ptolemaic plates (*Planisphaerium Ptolemaicum*). The order it lends is a
cosmology stated as nested orbits whose radii are the measured numbers, together with
Ptolemy's epicycles, where one motion is built as a sum of circles. The plate borrows that
order, not the look: every ring is a measurement, and Z = AV is drawn as Ptolemy drew a
planet, as a chain of weighted circular motions that closes exactly on the answer. The twist
(the part meant to be funny) is that a 17th-century device for faking the sky with a sum of
circles turns out to be an exact picture of attention's weighted sum.

## Mandate responses

`studio/orrery/` has no LEDGER.md and no FEEDBACK.md, so no J*/A*/S* rows are open. The
binding brief was the curator note plus DESCRIPTION.md § Weak and § Next versions (1). All of
them are answered here:

| id | mandate | status |
|---|---|---|
| CUR-1 | Keep every pen that carries a meaning (Q, K, V, Z, structure); each pen is one clean layer with a stated order and meaning | FIXED: 5 pens, one layer each, light → dark: goldenrod V, blue K, crimson Q, green Z, black structure/type. Each pen is used only in its own layer. |
| CUR-2 | Strokes spatially ordered within a layer so it streams in batches | FIXED: pipeline nearest-neighbour ordering within each colour. Q and K strands alternate direction (planet→tick, tick→planet), which removed the empty return flights: blue travel 0.95 → 0.63 m, red 0.85 → 0.57 m. Every spiral groove is split into one stroke per turn, so the longest stroke is 327 mm (the double rim) ≈ 33 s at F600. |
| CUR-3 | State minutes per layer and in total | FIXED: see Plot budget (43 min + 4 swaps). |
| CUR-4 | 1 887 pen cycles and 97 % travel, mostly dotted runs; dotted runs must earn their cycles | FIXED: 660 cycles (−65 %) and 46 % travel (5.13 m vs 11.23 m draw). The only dotted run left is the head's orbit (97 dashes of 2.2 mm). Every other dotted line from r01 (orbits, axes, sight lines) is cut or solid. About 400 of the 533 black cycles are type. |
| CUR-5 | Name the LINEAGE | FIXED: Cellarius, above. |
| D-concept | Illustration: no quantity sets any radius, orbit or bundle width | FIXED: every radius, turn, line count, bearing and epicycle is a GPT-2 number (see Mapping). Nothing was invented except the layout positions of the four hubs. |
| D-type | `SOFTMAX` in caps, broken `Q · Kᵀ` | FIXED: lowercase `softmax`. `Q·Kᵀ` now has a real centred dot (a 0.9 mm spiral disc, because the engine's `·` glyph is a 0.15 mm square). All type is laid out from measured glyph extents (engine `i` bug, see Engine requests). |
| D-depth | One ink weight; the sun is a flat target of 17 equal rings | PARTLY FIXED: the sun is now 13 bands of very different mass. The transformer band is 11 grooves at 0.85 mm; the smallest keys are single arcs of 36–108°. The rim is double-passed. The plate stays flat on purpose, see Self-critique. |
| D-V | V bundle straight and mechanical; `V` label grazing its orbit | FIXED: V is now 7 ribbons that drop out of their planets and swing into Z, nested so they never cross. `V` sits clear. |
| D-space | Letterbox bands top and bottom | FIXED: composed in A4 mm from scratch, not fitted from a 4:5 bitmap. The title sits 10 mm below the margin and the sentence caption runs along the bottom margin. |
| D-hierarchy | Satellites all similar in size | FIXED by data: K 26 mm, Z 27 mm, V 21 mm, Q 10.6 mm (Q and K share one scale, so the query system really is smaller). |
| D-grid | Corner marks aligned with nothing | FIXED: registration marks sit on the drawable corners. The title, sun, Z hub and star share the centre vertical. The key is set flush left on Q's axis. |

## What changed from parent

This is a rebuild, not a parameter pass. r01 traced a bitmap; r02 keeps its composition idea
(a sun inside one dotted orbit with four systems riding it) and derives every mark from a
real GPT-2 head.

- **The sun is the softmax row** of " itself" in GPT-2 small, layer 4, head 3. Out of all
  144 heads, this is the one where " itself" attends most to " transformer" (0.557): the
  coreference head. Each key is one spiral groove of 20·A turns at 0.85 mm pitch. Grooves
  nest lightest-inside, so " transformer" is the heavy outer band (11.14 turns). The 13 random
  node clusters of r01 are gone.
- **The dial is the sentence.** One tick per token runs left→right across the sun's top, and
  each groove ends under its own tick. The two future tokens (" think", ".") are open rings:
  the causal mask.
- **The systems carry every row of Q, K and V.** Radius = the true 64-d norm, bearing = the
  token's place in the sentence, mirrored so each system hands its sentence to the sun.
  Rings are the norm scale, and the axis is labelled with the outer ring's value.
- **The dot product is a meeting.** A red hairline from the query and a blue hairline from
  key j meet at key j's tick, for the 7 keys that earn a line.
- **Values are ribbons whose width is attention:** round(20·A) lines each, 18 lines total.
  They drop out of V and swing into Z, nested left→right.
- **Z is Ptolemy:** the 13 weighted values A_j·v_j chained head to tail (largest first) on a
  deferent with epicycles. The chain closes exactly on z under z's pole star.
- **Cut from r01:** the moons, the field dots, three sight lines, the dash-dot axes, and three
  of the four stars. The one star left is z's pole.
- Layouts tried and rejected on the way (all in Downloads, v1–v12):
  - v1: bearing = true 64-d angle to the query/output. Exact and mechanistic, but the centred
    keys all sit 86–101° from q (near-orthogonality in 64-d), so K collapsed into a comb of
    colliding dots.
  - v8: ribbons as orthogonal lanes. Countable, but it read as a PCB harness.
  - v5–v7: the Q/K crown with loops. Fixed by arriving at each tick between the radial and
    the way home.

## Measurements / computations

- **Forward pass (numpy, no torch)**, in `mechanism.py`: hand-written byte-level BPE (vocab +
  merges), hand-parsed safetensors, LN → causal MHA → gelu MLP. Max |A_numpy − A_torch| per
  layer against the cached HuggingFace stack `~/.promptplot/attn_gpt2.npz`, layers 0–11:
  4.0e-7, 6.4e-7, 1.1e-6, 2.3e-6, 1.8e-6, 1.8e-6, 2.2e-6, 1.8e-6, 1.4e-6, 1.9e-6, 1.8e-6,
  7.4e-7. The saved head is layer 4 (2.3e-6 max over layers 0–4).
- Tokens (15): `The| pen| plot|ter| drew| a| black| hole| while| the| transformer| watched| itself| think|.`
- **Head scan** (A[" itself" → " transformer"]): L4H3 0.557 · L2H9 0.416 · L11H11 0.379 ·
  L3H6 0.358; every other head < 0.29. L2H9 is used by the attention-weaving sibling, so it
  was avoided.
- **The row A[itself, 0..12]** (sums to 1): transformer .5572 · The .1142 · hole .0625 ·
  watched .0618 · pen .0583 · the .0522 · plot .0313 · while .0151 · ter .0139 · itself .0119 ·
  black .0105 · a .0060 · drew .0050.
- **Turns (20·A):** 11.14, 2.28, 1.25, 1.24, 1.17, 1.04, 0.63, 0.30, 0.28, 0.24, 0.21, 0.12,
  0.10. **Ribbon lines (round):** 11, 2, 1, 1, 1, 1, 1 = 18 lines (90 % of the mass). The six
  keys under 2.5 % draw none (10.2 % together) and appear only as their grooves.
- **Norms:**
  - |q|: The 1.95, the rest 9.66–11.65 (itself 11.32).
  - |k|: The 7.39, the rest 20.71–28.53.
  - |v|: The 0.71, the rest 2.92–4.73.
  - |z| = 2.589.
  - The attention sink " The" has the smallest query, key and value of the sentence and
    still takes 11 % of the attention.
- **Checks:** |A·V − z| = 4.1e-8. The epicycle chain (projected on ẑ and the first principal
  direction orthogonal to it) closes on z to 1.1e-7. The transformer arm alone is
  (2.215 along ẑ, +0.472 across). All 12 other arms pull back across (every one has a
  negative e2 component), and that is what brings the sum back onto the pole.
- **Scales:** Q and K share 0.911 mm/unit (one space); V 4.44 mm/unit; Z 10.43 mm/unit
  (stated on the plate only as the ring labels; Z's rings are at |z| = 1, 2 and 2.589).
- **Sun geometry:** core 9 mm; 20 turns × 0.85 mm = 17 mm of grooves plus 13 gaps × 2 mm, so
  the rim is at R = 52 mm (sun diameter = 55 % of the drawable width). Junction ticks sit at
  R + 4.2.
- **Spacing:** groove pitch 0.85 mm; ribbon pitch 0.9 mm; gaps 2.0–2.4 mm. The only marks
  under the 0.8 mm floor are the planet dots, which are single spirals at 0.3 mm pitch inside
  discs of ≤ 2.6 mm (a dot must read solid; same exemption r01 declared).

## Plot budget

Leo model (as in `gallery/PRINT.md`): F600 draw, F2000 travel, 2 s dwell per pen cycle.

| order | pen | meaning | draw m | travel m | cycles | min |
|---|---|---|---:|---:|---:|---:|
| 1 | goldenrod | V: value planets and norm rings, the ribbons (1 line = 5 %), Z's deferent and epicycles | 1.81 | 1.10 | 57 | 5.5 |
| 2 | dodgerblue | K: key planets and norm rings, key → tick hairlines, `transformer` underline | 1.36 | 0.63 | 33 | 3.7 |
| 3 | crimson | Q: query planets and norm rings, the query's fan of hairlines, `itself` underline | 0.71 | 0.57 | 31 | 2.5 |
| 4 | forestgreen | Z: norm rings, hub, pole, z itself | 0.44 | 0.19 | 6 | 1.0 |
| 5 | black | sun grooves, dial, rim, head's orbit, z's star, all type, registration | 6.92 | 2.63 | 533 | 30.6 |
| | **total** | | **11.23** | **5.13** | **660** | **43.3 + 4 swaps** |

- Commands: 22 354. Bounds: drawn marks inside [10, 200] × [10, 287].
- Parent (same model): 7.68 m draw, 7.45 m travel, 1 887 cycles ≈ 79 min.
- Why this order: lightest ink first so black lands last over everything. Green comes after
  the ochre epicycles so z's ring sits on top of them.
- Sheet-crossing hops: the only long travels are layer entries. The blue and red underlines
  in the caption are the first stroke of their layers, so the long hop falls on the swap
  boundary and never inside a batch.

## Self-critique

| dimension | score | note |
|---|---:|---|
| Hierarchy | 8 | At 3 m the sun wins (104 mm, the only black mass). K and the ochre river are second; Q, Z and type are third. The heavy outer band reads as one thing. |
| Grid & alignment | 7 | Centre vertical: title, sun, star, Z. The key sits on Q's axis and the registration marks on the drawable corners. The K and V letters are placed by eye relative to their systems. |
| Tension & asymmetry | 7 | K high right and heavy, Q small high left, the ochre river the one long diagonal from lower right into Z. The sun is centred, as in the reference. |
| Negative space | 7 | The left third between Q and the key is quiet, and the band above the caption is quiet. Some of that emptiness is leftover rather than shaped. |
| Craft for pen | 7 | Spacing holds and nothing floods. The stroke font is crude at 1.9 mm. The blue strands cross K's lower rings on their way out. |
| Concept legibility | 7 | Countable at 30 cm: 11 turns, 11 lines, "transformer" and "itself" underlined in the sentence. The epicycle twist only reads up close. Risk: a critic may call the orrery an object; the defence is that it is an orbital ORDER where every orbit is a measurement. |
| Depth | 5 | Declared flat: an engraved planisphere is flat by nature. Depth comes only from mass (dense band vs single arcs), the double rim and the ribbons passing over the head's orbit. |

**The single worst thing:** the Q/K crown above the sun. Fourteen hairlines cross each other
and K's lower rings before meeting at the ticks. It is readable, but it is the busiest and
least designed 40 mm of the sheet.

**The honest conceptual weakness:** the Q/K/V systems show true norms at sentence bearings,
but norms are not why " transformer" wins (its key norm, 23.2, is average). The mechanism is
carried by the sun, the ribbons and Z. v1 tried the mechanistic bearing (the true angle to
the query) and it collapsed, because every centred key is 86–101° from q.

## Engine requests

1. `generators._GLYPHS['i']`: the glyph sits at x = 1.8 but `_glyph_advance('i')` is 1.1, so
   in proportional mode `i` prints over the next letter ("itself" renders as "tself"). This
   piece works around it with its own layout from measured glyph extents (`layout()`).
2. `_GLYPHS['·']` is a 0.3-unit square (0.15 mm at 3 mm cap): invisible. It should be a
   ~0.8-unit disc.
3. `_GLYPHS['|']` has zero width, so bar-delimited norms (`|k|`) crowd.
4. `postprocess.optimize_stroke_order` never reverses a stroke. Fans that share one endpoint
   pay a full return flight per stroke unless the piece alternates directions by hand, as
   this one does.
