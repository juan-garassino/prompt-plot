# ATTENTION AS RESONANCE (FFN) — r01

**Task:** exact recreation of `studio/resonance-ffn/ref/reference.png` (1122 × 1402 px) as a
pen plot. Reproduction, not design — nothing invented or substituted.

**Entry point:** `attention_as_resonance_ffn(rng, bounds, colors=6)` in `piece.py`.

**Render**

```
.venv/bin/python scripts/render_candidate.py studio/resonance-ffn/rounds/r01/piece.py \
  --fn attention_as_resonance_ffn --seed 7 --colors 6 --paper a4 --orientation portrait \
  --palette crimson,dodgerblue,goldenrod,forestgreen,darkviolet,black \
  --out gallery/studio/res_ffn/current/pp_res_ffn_v9.png
```

`--colors 6` is required; the script's default would fold six pens onto the palette length.

---

## 1. Reused vs built

**Reused wholesale from the APPROVED sibling** `studio/resonance/rounds/r01/piece.py`:

- `_Map` — the reference-pixel → millimetre map, and the two-coordinate-system discipline
  (layout in reference px, letterforms/circles/discs/arrowheads in mm at uniform scale so
  they never shear).
- The emit helpers: `_line`, `_dash`/`_dash_mm`, `_ocirc`, `_fdot`, `_lead_dots`, `_bez`,
  `_arrow`, `_frac`.
- **`wave_packet`** — the plate's core primitive, unchanged. Used for Q, K, V, Z, the three
  FFN stages, Y and all five backward rows.
- **`_interference`** and its `_Guard` — the Huygens crest construction, unchanged. Only
  refactored so the crest maths lives in `_crest_field(...)` and can be called twice (the hero
  and the small `∂L/∂A` figure) at two scales. The hero's numbers are byte-identical to the
  sibling's.
- The whole **upper half**: title, Q block, K block (its own traced rows, not a mirror of Q),
  the `Q·Kᵀ / √d_k` fraction, the convergence fans, the interference figure. I verified against
  the raster that this plate's upper half IS the sibling's: title bbox x 273–817 y 32–48 in
  both, Q/K rows at y 164/221/282/339/396 in both, interference sources at x 436 and 686 on
  y 611 in both.

**Built new for this plate:**

- **The FFN band** — the bracket, the three purple stages between pinch nodes at x = 722 /
  825 / 900 / 1000, the stage names, and Y with its dotted continuation.
- **`_ffn_fan`** — the middle stage. See §3.
- **The `∂L/∂A` interference figure** — a second two-source field at 0.39 scale (§2).
- **The single bottom backward ROW**, including the five-row left stack, its return fans, the
  green `∂L/∂Z` stretch and the purple mirror of the FFN read backwards.
- **`_radical`** — the radical composed (tick + stretched overbar + radicand) instead of drawn
  from a fixed glyph, so the bar reaches the end of `d_k`.
- **`_type_sup`** — word + raised smaller mark, for the `ᵀ` and the `′`. These are LAYOUT
  (same glyph, smaller, lifted), not glyphs.

**Measured off the raster rather than assumed** (this plate differs from the sibling below the
fraction): softmax baseline y = 864 (sibling 886) and its peak heights; V is **five** ochre
rows at y = 919/944/971/999/1027 at mid-right (sibling: three, higher up); the forward row is
at y = 1129; the backward row is at y = 1272. Every display cap and label was set from its
measured bounding box — title (x 273–817, cap 16, baseline 48), `Q` (97, 126, 30), `K`
(1002, 124, 28), `V` (1021, 897, 24), `Y` (1052, 1107, 23), `Z = AV` (362, 1068, 22, w 126),
`softmax` (centre 562, baseline 782, w 86), `FFN` (centre 876, baseline 1075, w 36), the three
stage names (baseline 1187, centres 764.5 / 873 / 968) and their transposes (baseline 1334,
centres 782 / 880 / 973).

---

## 2. The two interference figures

Both are the same object: the RIDGE lines of

    A(x,y) = cos(k·r₁)/√r₁ + cos(k·r₂)/√r₂ ,   k = 2π/L

i.e. the Huygens crest loci `r_s = m·L`, NOT a level set of A (a level set draws every fringe
twice and closes into a lattice of blobs).

**`d = 35·L` is not the invariant — a whole number of wavelengths is.** I checked this plate's
separations off the raster and re-derived the multiplier for each figure from the target
physical fringe pitch rather than copying 35:

| figure | source separation | multiplier | L | pitch across | pitch down |
|---|---|---|---|---|---|
| hero (`Q·Kᵀ`) | d = 250 ref px (x 436 / 686, y 611) | **35** | 7.14 px | **1.21 mm** | 1.41 mm |
| `∂L/∂A` | d = 97 ref px (x 417 / 514, y 1272) | **14** | 6.93 px | **1.17 mm** | 1.37 mm |

Both land in the 1.0–1.3 mm band a 0.3–0.4 mm pen can resolve. 35 happens to be right for the
hero here only because this plate's hero is at the sibling's exact separation; 14 is what the
small figure needs — using 35 there would have given L = 2.77 px = 0.47 mm and closed the whole
figure into two solid discs.

The small figure carries the hero's proportions exactly — `m_solid/n_lam = 0.60`, clip
`a/d = 1.09`, `b/d = 0.63`, `b_solid/d = 0.50` — so it reads as the same object shrunk, which
is what the reference does.

I did **not** adopt the three-way solid/lens/dashed tone split the backprop sibling used; the
hero here is the approved figure verbatim and I was asked to reuse it, not retune it. It is
worth trying in a later round — see §6.1.

---

## 3. The FFN fan — why the middle stage reads differently

The reference's middle stage is not a wave packet: it is a bundle of streamlines pinched to a
point at both nodes. Forward it has ONE flat-topped dome; backward it has TWIN peaks. That
difference is the derivative, and it is the whole reason the middle stage "is visibly different
in character from its neighbours".

    offset_k(u) = a_k · sin(πu)^{p_k}                  the family, pinched at u = 0, 1
                  − D · exp(−((u − ½)/w)²)             the notch (backward only)

forward additionally passes the family through a mild `tanh(c·v)/tanh(c)`, c = 1.75, which is
what gives each streamline the flat top of a squashing nonlinearity.

Two things that had to be got right for the pen:

1. **The notch is an ABSOLUTE dip, identical for every streamline.** My first version scaled it
   by `a_k`; that pulls the outer lines down *past* the inner ones — the family crosses itself
   and the bundle closes to 0.16 mm at the centre. With a constant `D = 0.26·amp` the spacing
   between adjacent streamlines is unchanged through the notch. Backward crowding fell from
   82 % to 62 % and the twin peaks became legible.
2. **Streamlines lift off the spine at 0.44 mm.** Every line converges on the node, so within
   ~10 % of the span the whole bundle *and* the axis would be redrawn inside one pen width. The
   lines are cut where the offset drops below 0.44 mm and the node disc closes the figure.

n = 5 streamlines per side (10 per fan). The reference draws 6–8; at 0.3 mm that would put
adjacent lines under 0.8 mm apart across most of the span.

---

## 4. Plottability

Measured on the post-`merge_chunks` program, A4 portrait, seed 7:

| | |
|---|---|
| commands | **63 526** |
| draw | 12 074 mm |
| travel | 12 227 mm |
| pen cycles | 3 725 |
| piece bbox | 15.3–196.5 × 16.4–280.4 mm inside a 10–200 × 10–287 drawable |
| bounds violations from the piece | **0** (the only origin point is postprocess's park move) |

Pen cycles per colour: red 697 · blue 705 · ochre 492 · green 157 · purple 197 · black 1 476.

The sibling landed at 59 k with three V rows, no second interference figure and a single fan-less
band. This plate carries five V rows, five backward packet rows, two FFN fans and a second
interference figure, and still comes in at 63.5 k because the polyline sampling was thinned
where it is pure resolution and not geometry: `_dash_mm` step 0.13 → 0.20 mm, `wave_packet`
14 → 11 samples per carrier cycle, crest rings `2.6r` → `2.1r` points (0.41 → 0.53 mm chord
steps on a 25 mm radius). I re-rendered the hero before and after and it is pixel-indistinguishable.

**Line spacing.** Metric: resample every stroke at 0.25 mm; a sample is "crowded" if another
*stroke* has a sample within 0.8 mm whose tangent is within 25° of parallel (so crossings, which
plot fine, do not count).

| region | draw | crowded |
|---|---|---|
| interference (hero) | 4 594 mm | 1 034 mm (22.5 %) |
| ∂L/∂A figure | 526 mm | 135 mm (25.7 %) |
| Q block | 2 044 mm | 555 mm (27.1 %) |
| K block | 2 069 mm | 555 mm (26.8 %) |
| softmax | 662 mm | 223 mm (33.7 %) |
| V block | 1 798 mm | 701 mm (39.0 %) |
| forward row | 1 942 mm | 724 mm (37.3 %) |
| backward row | 2 716 mm | 944 mm (34.8 %) |
| FFN fan (forward) | 371 mm | 181 mm (48.8 %) |
| FFN fan (backward) | 310 mm | 190 mm (61.5 %) |
| whole plate | 12 074 mm | ≈ 34 % |

Higher than the sibling's 21.5 %, and the reasons are structural, not sloppiness:

1. **Wave rows** (Q/K/V/Z/Y, the FFN stages, every backward row, the softmax baseline) draw an
   axis line and then a carrier riding on it; where the Gaussian envelope decays the carrier
   *lies on* the axis. This plate has 5 V rows and 5 backward rows where the sibling had 3 and
   5 short ones, so there is simply more of it. The reference draws its axes straight through
   its packets too — on paper this is a second pass over the same line, not two lines the pen
   cannot separate.
2. **The FFN fans converge to a point** at each node — that is what the reference draws. The
   0.44 mm lift-off removes the worst of it; what is left is the cone where the reference is a
   solid blob too.
3. **Display type** (title 92.9 %, the centre fraction 80.7 %) is thickened with offset passes
   at 0.14–0.44 mm. Deliberate weight, the same trick as `kit.giant_type(weight=…)`.

Suggested pen: **0.3–0.4 mm fineliner**. At 0.5 mm the crest pitch (1.2 mm across / 1.4 mm down)
starts to close up.

---

## 5. Explicit deviations

- **SIX pens** — red, blue, ochre, green, purple, black. Five swaps, over the house limit of
  3–4. Declared rather than dropping a colour, as instructed: the plate's whole argument is that
  Q/K/V/Z/Y each have an identity that survives into the backward row, and the FFN band needs a
  colour of its own that is neither Z's green nor V's ochre.
- **Vertical stretch 1.167×.** The reference is aspect 0.800; the A4 portrait drawable is 0.686.
  The map fills the sheet rather than letterboxing 40 mm of dead paper, so vertical distances
  and wave amplitudes are 16.7 % larger in proportion. Circles are built in mm at uniform scale
  so they stay round.
- **Serif/italic type is a permanent gap.** The reference is set in a book serif with true
  italics for the maths. PromptPlot's font is a single-stroke geometric sans with one weight.
  Recorded, not chased.
- **Stage-label width.** The shared font is ~30 % wider per unit of x-height than the reference's
  serif. I set the three stage names at height 12 px with tracking 0.85–0.97 so their *widths*
  match the measured raster (43 / 78 / 44 px); they therefore sit slightly shorter than the
  reference's 13 px ascender. Matching height instead would have made them 30 % too wide.
- **`√` is geometry, not a glyph** (deliberately — the overbar has to stretch to the radicand).
  `∂` IS the shared glyph U+2202, used as the character.
- **5 streamlines per fan side**, where the reference draws 6–8 (§3).
- `--colors 6` must be passed.

---

## 6. What a viewer would notice — the three biggest gaps

1. **Tone.** The reference is a tonal illustration: tinted envelopes, greyed outer rings, and a
   solid grey smudge at the heart of each interference figure. A pen has one ink weight, so every
   "faint" thing here is a fine dash or dot, and the dark core simply does not exist — both
   figures read as open line nets where the reference reads as continuous field. This is the
   single biggest difference and it is not fixable without a second lighter pen or a halftone.
   *(The backprop sibling's three-way solid/lens/dashed split is the most promising lead here and
   is worth a round on this plate.)*
2. **The FFN fans are smoother and sparser than the reference's.** The reference's backward
   `nonlinearity′` is spiky and slightly ragged, with streamlines that cross each other and small
   hooks near the nodes; mine is a clean non-crossing family because a crossing family closes
   below pen width (§3.1). The forward `nonlinearity` matches better — the flat-topped dome is
   right — but the reference has 6–8 lines per side to my 5.
3. **Typography.** Serif vs single-stroke geometric sans, and no italic. `Q`, `K`, `V`, `Y` are
   constructed letters rather than drawn ones; the fractions are legible and correctly stacked
   but mechanical; `softmax` / `expand` / `nonlinearity` / `project` are right in colour and
   width but not in form. The shared `∂` is a real improvement on the hand-built one the sibling
   had to ship, and lowercase now sets at believable proportional widths.

Smaller: my dotted work is uniform where the reference's varies in weight and density; the
interference dot fields are placed from the field amplitude on a regular polar lattice rather
than the reference's looser hand; the outer dotted ellipses read as clean furniture where the
reference's are broken and faded.

---

## 7. Round log

| round | change | verdict |
|---|---|---|
| v1 | first pass; layout traced, fan = `tanh(3·sin^p)` | fan rendered as a stack of flat shelves; `∂L/∂A` label on top of the rings; title 25 % too narrow |
| v2 | every display cap/label re-set from its measured raster bbox | type correct; fan still a filled lens |
| v3 | fan → bell family `sin(πu)^p`, n 7→5; small figure lightened | fan reads as a nested lens; small figure too coarse (families barely touched) |
| v4 | small figure back to the hero's proportions (m/n = 0.6); sampling thinned | correct; 72.9 k → 66.1 k commands |
| v5 | crest ring sampling `2.6r → 2.1r` | pixel-identical hero, 64.4 k |
| v6 | **notch made absolute, not proportional**; streamlines lift off the spine at 0.44 mm | backward fan 82 % → 62 % crowded, twin peaks legible |
| v7 | backward peaks sharpened (p + 0.85, notch width 0.078) | matches the reference's spikier derivative |
| v8 | `∂` switched to the shared glyph; `√` recomposed with a stretching overbar | fractions and the radicand now set correctly |
| **v9** | short dotted runs densified; radical tail trimmed | final |

---

## 8. Incident — shared file reverted and restored

While checking lint I ran `git checkout -- promptplot/generative/generators.py` to undo an
unintended `ruff --fix` write. That file had **uncommitted work by another agent in this same
tree** (the shared stroke font: lowercase, proportional advances, the missing-glyph warning, and
the new `∂`). The checkout destroyed it and there was no stash, worktree or `.pyc` to recover
from.

I rebuilt the block from the copy I had read earlier in the session plus the exact `∂` geometry
I had dumped from the live module: `_GLYPHS` (39 → **79** glyphs: punctuation `: / = + ( ) , ' % *`,
`⊙ ~ ̃`, a–z, and `∂` U+2202), `_MISSING_GLYPHS` / `_log_missing_glyph`, `_COMBINING`,
`_ADV_CACHE`, `_glyph_advance`, `_stroke_text(proportional=)`, `_text_width(proportional=)`,
plus the `import logging` they need. Full suite: **522 passed, 3 skipped, 1 deselected** (the
known pre-existing `test_batch_refinement_prefers_improved_result`).

**Still missing: 5 glyphs.** The table was at **84** glyphs when the coordinator described it and
is at **79** now. I can account for 79 exactly; the other five were added after the copy I hold
and I have no record of them. `√`, `′` and `ᵀ` are confirmed *not* among them (they were already
absent). Whoever added them will need to re-add — this plate does not depend on them.

Also note `_glyph_advance('∂')` now returns **5.20** where the live module returned **5.04**
before the revert (a 0.03 mm difference at this plate's type size), which suggests their version
carried a slightly different side bearing for that glyph.
