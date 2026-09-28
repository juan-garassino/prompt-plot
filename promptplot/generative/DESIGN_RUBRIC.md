# Design Studio Rubric — the bar every collection piece must pass

Two-role adversarial loop: a DESIGNER (edits generator code/params, renders) and a
CRITIC (sees ONLY the rendered png, fresh eyes). A piece ships when the critic
scores **avg ≥ 8/10 with no dimension below 7** (all seven dimensions; a declared-flat piece is scored on how well the flatness serves it), over at most 5 rounds.

## The seven dimensions (1–10 each)

1. **Hierarchy** — one element dominates at 3 meters; a clear second and third read
   at 1 meter; details reward 30 cm. If everything is mid-sized, score ≤ 4.
2. **Grid & alignment** — type, furniture and subject share axes/edges. Nothing
   floats "roughly in a corner". Margins are exact and consistent.
3. **Tension & asymmetry** — off-center balance, working diagonals, elements that
   crop at the frame or overlap with intent. Centered-symmetric = student work, ≤ 4.
4. **Negative space** — emptiness is shaped, not leftover. At least one generous
   quiet zone that makes the dense zone read louder.

   **OVERLAP IS A DECISION, NEVER A SYMPTOM.** Failure mode 6 below says masters
   overlap, and that is true — but an overlap that happened because two elements
   ran out of room is not composition, it is collision, and it reads as one.
   Every overlap on the sheet must be one you would defend out loud: it builds
   depth, it ties two stages together, it crops at the frame with intent. The
   test is blunt — if nudging an element a few millimetres would relieve the
   crowding and nothing would be lost, it was crowding. Likewise spacing: gaps
   between zones are sized on purpose and repeat, they are not whatever was left
   after placing things. An element pressed against the frame, a label grazing
   geometry, a bundle threading a gap it barely fits: all crowding, all read as
   mistakes however rigorous the content behind them.
5. **Craft for pen** — line weight built from 1–3 passes with purpose; fills solid
   without flooding; no muddy ink-on-ink collisions; density plottable (≥0.8 mm
   spacing); one pen swap per colour layer (any number of
   layers — see PLOTTABLE below).

   **CONTOUR LEVELS BY GRADIENT, NOT BY VALUE.** Evenly spaced iso-VALUES
   bunch wherever the field is steep, so a contour nest floods solid in the
   steep band and then has to be thinned into crumbs, which breaks every ring.
   Step the level by `spacing x quantile(|grad F|)` instead and rings sit a
   fixed distance apart wherever they run, so they stay CONTINUOUS — usually
   the dominant visual property of a contoured plate. Use the 82nd percentile,
   not the median: the gap is narrowest where the field is steepest, so the
   median under-sizes exactly the stretches that flood. `kit.even_contour_levels()`.

   **CONTOUR EYES MUST BE CONICAL, NOT GAUSSIAN — AND MIND THE LADDER.** For a
   LINEAR cone `a - r·s` at uniform level steps the ring pitch is constant. For
   an EXPONENTIAL cusp `a·exp(-r/σ)` uniform levels are NOT enough: they put
   radii `σ·ln((k+1)/k)` apart, i.e. `σ/k` near the summit, which still floods —
   16 uniform levels on a σ=5.4 cusp measured 0.33 mm at the innermost ring.
   Build the ladder geometrically instead, `F_k = a·exp(-k·pitch/σ)`, and the
   pitch is exactly `pitch` everywhere. Corollary: **the ladder is set by the
   TIGHTEST cusp in the field**, so a small secondary beside a large primary
   drags the primary under the floor. For a Gaussian
   the ring radius goes as `σ·√(2·ln(a/F))`, whose derivative blows up at the
   summit, so the rings SPREAD exactly where you wanted them tight. Corollary
   that decides layouts: `rings × pitch ≈ σ`, so under a fixed minimum pitch
   the only way to buy more rings in a vortex is a physically BIGGER eye. A
   reference packing 20 rings into 0.3 mm cannot be matched at any pitch a pen
   can hold; enlarge the feature or accept fewer rings.

   **TONAL FILLS: tone drives DUTY, never SPACING.** A gradient whose spacing
   shrinks with darkness always floods — past some tone the spacing falls under
   the pen tip and the passage goes solid black. Use `kit.tone_dots()` (tone is
   the probability a cell is inked; one dot per cell; density bounded at
   1/cell²) or `kit.tone_hatch()` (spacing fixed, tone drives dash duty). Dots
   first unless the piece argues otherwise. Never hand-roll a stipple whose
   density is unbounded.
6. **Concept legibility** — the physics/ML idea lands in one glance without reading
   the caption. The caption confirms, never explains. **NO SCHEMATICS**: if the
   piece could appear in a textbook, a slide deck, or a Wikipedia article
   (wiring diagrams, labeled arrows between boxes/circles, axis plots), it
   fails this dimension outright (≤3). The subject is the PHENOMENON — what the
   thing DOES — never the apparatus that does it.

   **TRANSPOSE TO AN ABSTRACT ORDER — DON'T PLOT, AND DON'T DEPICT.**
   Banning schematics leaves two default failures, and both are dead ends:

   - **The scientific figure** — a relief of the quantity, a deck of parameter
     panels, a field of contours, a scatter with an inset. Honest, exact, and
     still a figure, because its form is just the function extruded.
   - **The illustration** — drawing a recognisable THING and hanging the
     mechanism on it: a loom, a comb, an abacus, a rose. This is figuration and
     it is not what this collection does. If a viewer can name an object in the
     plate that is not the mechanism itself, cut it.

   What every shipped piece actually borrows is an abstract ORDER — an
   organising geometry the mechanism genuinely HAS — and then builds the whole
   plate out of that order and nothing else:

   | piece | mechanism | abstract order |
   |---|---|---|
   | `bauhaus_loom` | matrix multiply | **INTERLACING** — over/under by sign, float by magnitude |
   | `bauhaus_gradient` | gradient descent | **FLOW TO ATTRACTORS** — basins, separatrix left as void |
   | `lstm_gates` | gated memory | **RADIAL** — hub, rim, spiral transport |
   | `bauhaus_decision` | a trained network | **A CUT THROUGH A FIELD** — the iso-0 knife, "no neuron drawn" |

   None of those depicts anything. A weaving is an interlacing rule, not a
   picture of a loom; a watershed is a flow rule, not a landscape.

   The working vocabulary of orders: radial · interlaced · laminar/stratified ·
   nested · tessellated · branching · interfering · orbital · packed ·
   flow-to-attractor · lattice-with-defects. The maths supplies the NUMBERS,
   the order supplies the FORM, and the mapping is exact and stated in one line
   ("sign is over/under"). Before any geometry, answer: **what ORDER is this?**
   If the answer names a plot, it is a figure; if it names an object, it is an
   illustration. Neither ships. A surface is a legitimate order only when the
   subject genuinely IS a field (a loss surface, a similarity field) — it is
   not a licence to extrude whatever function is to hand.

   **AND THE TWIST.** A carrier gets you an object; it does not get you wit.
   The best science images hijack something the viewer already knows and let
   the mechanism finish the sentence — "roses are red / roses are blue,
   depending on their velocity relative to you" is exactly one joke, and the
   punchline IS the Doppler shift. Nothing is decorated and nothing is
   explained. Ask what the viewer already holds — a rhyme, a proverb, a
   pictogram, an object with a fixed cultural meaning — and what breaks when
   the mechanism is substituted into it. A plate that lands the idea AND
   raises a smile beats an earnest one at equal rigour, every time.
   Earnestness is this studio's default and it is a weakness, not a virtue.

   **STYLE IS NOT OPTIONAL — AND THE COLLECTION SPANS THE CANONS.** The plate is
   drawn in a MOVEMENT's language, not in neutral drafting. This is not one
   style for the whole set: ten plates in one canon is a wallpaper sample, not a
   collection. Different subjects take different canons, chosen because the
   canon's ORDER matches the mechanism's — De Stijl for a partition,
   Constructivism for a driving asymmetry, Psychedelic for a deformation,
   Memphis for noise against structure. A plate may also HYBRIDISE two canons
   when the mechanism genuinely has two aspects (a De Stijl ground carrying
   Memphis defects, say), but a hybrid must be a stated decision, never a
   failure to choose. Whichever canon is picked, commit to it: Bauhaus wants
   structural shapes, a dominant diagonal and primary colour as MASS; Swiss
   wants a strict modular grid, brutal asymmetry and type at poster scale; Pop
   wants Ben-Day lattices and fat keylines. The kit for all three now exists in
   `engine/kit.py` — `giant_type()` (display type with real weight in mm),
   `benday_fill()`, `fat_outline()`, `concentric_disc()`, `modular_grid()`.
   Hairline type at caption size everywhere is the technical-drawing default
   and reads as a lab figure.

   **BUT THE STYLE CARRIES THE MECHANISM — IT DOES NOT REPLACE IT.** The canon
   is the LANGUAGE; the science is the CONTENT. A gorgeous Memphis plate that
   has stopped encoding its physics has failed harder than the earnest figure it
   replaced, because it fails at the one thing this collection is for. The test
   for every stylistic element: WHAT DATA IS THIS CARRYING? A Ben-Day dot's
   radius is a magnitude; a De Stijl block's area is a quantity; a
   Constructivist diagonal is a real direction in the mechanism; a confetti
   scatter is a real distribution. Anything that carries nothing is decoration,
   and decoration is cut. The exactness bar does not move by one inch when a
   canon is assigned — the numbers must still be computed, measured and
   reported exactly as before.
7. **Depth & dimensionality** — the default is NOT flat: use occlusion/overlap,
   projected 3D forms (spheres, tubes, perspective), line-weight or dash-density
   falling off with distance, tone gradients that turn planes into volumes.
   Flatness is permitted ONLY as a conscious, declared decision — either the
   assigned style canon is flat by nature (Swiss, Pop Ben-Day, classic Bauhaus)
   and the designer says so in the report, or the concept demands it. Undeclared
   flatness scores ≤ 4.

## LINEAGE — every plate answers a named work

Juan (2026-09-28): "need to be creative, plottable in the pen plotter, refer to good artistic
waves." A canon from STYLES.md is the language; a LINEAGE is the conversation. Every plate
names **one movement and one real reference work** it answers, and says in one line what
ORDER it takes from it — never its look. "Riley's *Current*: one line family whose phase
drift makes the surface" is a lineage; "Op Art style" is not.

The pen plotter has its own art history — prefer it, these artists drew with line machines
or wrote the instruction that a machine can follow:

| lineage | reference | the order it lends |
|---|---|---|
| early computer art | Georg Nees, *Schotter* (c. 1968) | order → disorder down the sheet; noise as a controlled gradient |
| early computer art | Vera Molnár, *Interruptions* (1968–69), *(Dés)Ordres* (1974) | a strict field with measured, local breaks |
| early computer art | Frieder Nake, *Hommage à Paul Klee* (1965) | a random walk bounded by horizontal strata |
| systems art | Manfred Mohr, hypercube works (1970s–) | a rule-generated projection; the rule IS the image |
| conceptual | Sol LeWitt, *Wall Drawings* (1968–) | an instruction executed exactly; the text could redraw it |
| Op Art | Bridget Riley, *Current* (1964), *Cataract 3* (1967) | one line family, phase/amplitude drift makes the surface move |
| Op Art | Victor Vasarely, *Vega* series (1957–) | a lattice swollen by a hidden volume |
| De Stijl | Piet Mondrian, *Broadway Boogie Woogie* (1942–43) | orthogonal lanes whose rhythm is the data |
| Constructivism | El Lissitzky, *Beat the Whites with the Red Wedge* (1919) | one driving diagonal against a mass |
| Bauhaus | Kandinsky, *Point and Line to Plane* (1926) | point / line / plane as forces with direction and weight |
| textile | Anni Albers's weavings | interlacing: over/under as information |
| minimalism | Agnes Martin's grids | a hand-ruled grid, tone by density alone |

Rules: the lineage is stated in the designer's HANDOFF.md (`lineage:` line) and NOTES.md;
the art critic judges whether the plate would hold its own **hung beside that work**
(concept + craft, not resemblance) and fails a plate that merely borrows a surface texture.
Two plates in one batch should not share a lineage unless the mechanism demands it.

**Plottable is part of creative.** These plates will be plotted for real on Leo, as
batched plate jobs (studio/PLOT_JOBS.md): frame → per colour layer: park, swap, stream in
stroke batches with re-zero checks → park. Juan (2026-09-28): more than 4 colours and longer
sessions are fine **as long as batching and colour changes are right**. So the rule is not a
pen cap, it is layer discipline:

- **As many pens as the mechanism has meanings** — each pen a stated meaning, each a clean
  colour layer, never re-entered after its layer (one swap per pen). State the layer order
  (usually light → dark so dark ink lands last) and why.
- **Every layer streams well in batches**: strokes spatially ordered within the layer, no
  sheet-crossing travel between consecutive strokes, no single stroke so long it cannot be
  a batch boundary.
- **Time is allowed, waste is not**: state draw length and minutes per layer and in total.
  Pen cycles are time (each lift+drop dwells on Leo): a dotted run costing thousands of
  cycles must earn them — otherwise fewer, longer dashes or one hairline.
- Always: `.gcode` beside every render, spacing ≥ 0.8 mm (2.4× the finest nib for hatch),
  no floods, bounds clean on the stated paper. A plate that only works as a PNG fails.

## The designer's expressive levers (play them consciously, every round)

- **Proportion** — scale ratios of at least 3:1 between dominant and secondary
  masses; try extreme formats (a tiny subject on a vast field, or a subject
  that swallows the frame).
- **Fill vs. void** — compose the empty space as deliberately as the ink;
  alternate packed and silent zones with rhythm.
- **Density gradients** — line/dash spacing ramps ARE the plotter's gradient:
  use them for tone, depth, motion, and emphasis (spacing 0.8→6 mm across a
  form reads as light).
- **Color play** — sequence pens as gradients across zones (blue→purple→pink),
  let two pens interleave to mix optically, keep one pen scarce and loud;
  color = compositional weight, not category labels.
- **Texture direction** — hatch/dash direction can follow form (contours),
  fight it (cross-grain tension), or stay neutral; choose, don't default.

## Known failure modes of this codebase (critic: check these first)

- Subject floating dead-center with even margins on all sides.
- Furniture checklist: swatch bar + plus marks + footer placed in corners without
  a shared grid line.
- All elements at similar scale (no dominant mass).
- Colors used as mere categories instead of compositional weights (the accent pen
  should be scarce and loud).
- Type blocks colliding with, or ignoring, the subject's geometry.
- Elements politely avoiding each other — masters overlap. But see dimension 4:
  the overlap must be chosen, not the residue of running out of room.
- **The scientific figure**: relief + parameter deck + inset chart + measured
  caption. Rigorous, and still a figure. Ask what object it is (see dimension 6).

## Designer's obligations per round

- Address every mandatory change from the critic, or argue (in the report) why not.
- Move whole compositions, not just parameters: reposition, rescale, crop at the
  frame, merge/delete furniture. Rewrite layout code freely.
- Keep: seeded determinism, margins, paper safety, tests green.

## Critic's obligations per round

- Judge ONLY the png (no code reading), against this rubric plus the piece brief.
- Score all six dimensions, name the single biggest weakness, give exactly 3
  mandatory changes (concrete, visual — "move the type block onto the bar's left
  edge", not "improve balance").
- PASS/FAIL verdict. No politeness. A pass means it could hang in a gallery.
- When a reference image is in play, judge the render as an INTERPRETATION of it
  and run the seven acceptance questions in `studio/AUTHORING.md` §6.

## TRACING IS NOT AUTHORING

Edge maps, posterisation, skeletonisation and threshold tweaks were tried on the
reference reconstructions and rejected: jagged paint boundaries, double outlines
(the two sides of one thick stroke), broken important contours, lost faces,
texture everywhere, no hierarchy. Halftones were tried here and rejected for the
same reason — a screen has no idea what it is drawing. **Author the forms; let the
engine execute the marks.** A reference image is an interpretation brief, never a
bitmap to convert. Full method: `studio/AUTHORING.md`.

## MATERIAL GRAMMAR (one grammar per material — they differ on purpose)

| material | primitive | rule |
|---|---|---|
| skin, cloth | `surface_grid` + `cut_tone` | a warped (u,v) net over the form; rows break into dashes by an authored low-frequency tone; the oblique cross family only in shadow; eyes/lips protected holes; golden-ratio phase stagger so highlights never fence |
| hair, metal, flowing surfaces | `flow_family` | two authored guides interpolated into one coherent family, clipped to the surface; a travelling highlight interrupts each track at a slightly different point; strong edge only on real dark boundaries |
| cubist planes | `hatch_polygon` + `physical_hatch` | one hatch direction per plane, aligned to that plane; **lit planes stay bare paper**; cross only selected shadows; spacing floor 2.4 × finest nib; inset ½ border + ½ hatch + 0.035 mm |
| painterly / acrylic | `brush_family`, `flow_strokes` | one **centerline with a brush width** per mark, never two edges; underpainting (broad masses) → body (flow) → accents (highlights); colour sampled from the region then quantised to a small palette; later passes cover earlier — cull the hidden |
| background atmosphere | — | omit, or a few quiet horizon lines; nothing is owed a mark because the raster has it |

Tone is always real marks and real paper — duty cycle, spacing, bare planes —
never grey. Widths are millimetres of an actual nib or brush.
