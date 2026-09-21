# STYLE CANONS — the studio's movements (ALWAYS with lines)

Every piece is assigned ONE style by the curator/translator. The ART CRITIC
judges against that style's canon below, not against generic taste. Hard house
constraint across all four: everything is LINES — line work, hatching, dot
lattices, multi-pass weights. "Solid" only ever means serpentine/spiral/
concentric line fills. No element that a pen cannot draw as strokes.

## 1. BAUHAUS (1920s) — kit exists: `bauhaus.py`

Geometry as ideology. Circles/bars/quarter-discs, one accent color used
scarcely, spaced-caps type, swatch bar, M 1:80 footer.
Palette: blue | pink | black — **or** the warm poster variant red | mustard |
blue | black on CREAM paper (ref: the classic concentric-ring Bauhaus poster).
Line moves: spiral/serpentine fills, dotted orbits, crosshair rules, and the
**concentric-ring disc** (a circle filled with many tight equal-spaced rings —
the "target/phonograph" hero motif) plus half-disc / quarter-disc big-scale
compositions locked to a column grid. Critic notes: asymmetric balance required;
furniture must sit on a shared grid; when a concentric-ring disc is the hero it
must dominate at 3m and ring spacing must be dead-even (wobble reads as error).

## 2. ART DECO (1920–30s)

Machine-age luxury: sunburst ray fans, stepped ziggurat outlines, chevrons,
nested arcs, fan shells, frame ornaments, symmetric monumentality (symmetry is
ALLOWED and often right here). Thin/thick alternation via 1–3 passes.
Palette: gold | black (+ one jewel tone: emerald or crimson) on cream.
Line moves: radiating line fans with geometric spacing, concentric stepped
borders, parallel-line gradients (spacing ramps), zigzag bands.
Critic notes: demands craft precision — ray spacing must be exact; ornament is
welcome but must be rhythmic, never noisy. Type: spaced caps, wide tracking,
centered allowed.

## 3. SWISS / INTERNATIONAL TYPOGRAPHIC STYLE (1950s)

The grid is the artwork. Strict modular grid (document the module in the
code), flush-left type, extreme scale contrast (one HUGE element), radical
negative space, diagonal energy, zero ornament.
Palette: red | black on white (max 2 pens + white space as third color).
Line moves: hairline rules, line-screen tone (parallel-line halftone), massive
type set with the stroke font (letters 20–60mm tall as graphic mass),
grid-locked photography-substitute = the data drawing itself.
Critic notes: symmetric or centered = automatic fail; any element off the
module grid = fail; if nothing is huge, fail.

## 4. POP ART (1960s)

Mechanical reproduction as art: Ben-Day dot lattices (regular dot grids at
2–4 sizes = tone), fat contour outlines (3–4 passes), repetition panels (the
same motif ×4/×6 with pen-role swaps per panel), comic energy marks
(speed lines, starbursts).
Palette: primary red | blue | yellow + black outlines (4 pens).
Line moves: benday dot fills (dot = 2 tiny strokes, strict lattice), bold
multi-pass contours, panel grids with thin gutters, halftone size ramps.
Critic notes: repetition must vary MEANINGFULLY (data changes per panel, not
just color); outlines must dominate; dot lattices must be perfectly regular —
wobble reads as error, not charm.

## 5. RADIAL DATA-VIZ / INFORMATION ARCS (ref: the Bauhaus 1919–1933 timeline)

Data as a fan of concentric arcs. A half/quarter-circle spread of many FINE
concentric arc-rings, each ring one data series or one row of a time series;
angle encodes time/category, radius encodes track, arc length/gaps encode
value/duration. A radial tick axis with scale labels, small glyph markers on the
arcs, and a compact legend. Dense but AIRY — the empty center and the outer
margin breathe.
Palette: muted multi-hue on cream — pens picked as a small ordered set (e.g.
black + 3–4 desaturated hues), one hue per series; NOT loud primaries.
Line moves: `dotted_circle`/`circle` at graduated radii, partial arcs (start/end
angle per datum), fine radial tick rules, tiny stroke-font labels around the rim,
single-stroke connector marks. Critic notes: legibility of the DATA is the bar —
a stranger must decode "time going around, series stacked outward"; arcs must be
concentric and evenly pitched; never let it collapse into decorative rainbow;
scale labels + legend are mandatory (this is the one style where annotation is
the point, but it must be typographic and gridded, never boxes-and-arrows).

## 6. MODERN SCIENCE POSTER (ref: the "WEAK FORCE" plate)

One dominant celestial/physical BODY + a field whose density IS the data + a
typographic data footer. Composition in two zones: upper — a huge dark disc or
sphere (solid concentric-line fill, cropped at an edge for scale) with a FIELD of
parallel horizontal rays/scanlines streaming off it, ray spacing/length ramping
to encode intensity (a real sequential scale, densest = strongest); lower — a
dense DATA FOOTER: big spaced-caps title, 2–4 columns of fine stroke-font text,
and small inline micro-charts (bars/sparklines built from lines).
Palette: warm sequential ramp — black + crimson/orange/mustard on cream (the
ray field reads as a heat/intensity ramp), one dark mass anchoring it.
Line moves: `line_gradient()` (parallel-line density ramp = the field), big
concentric-ring or solid-spiral disc for the body, `line_screen_tone()` for the
footer micro-charts, giant spaced-caps title. Critic notes: the body must be the
loudest single element and asymmetric (never centered); the ray-field density
must map to a stated quantity (label the scale in the footer), not decoration;
the footer is data, not filler — real numbers/real curve. This style pairs with
the existing physics compositions (`black_hole_bauhaus`, `gw150914`).

## 7. DE STIJL (1910s–30s) — the abstraction benchmark

Mondrian, van Doesburg. Abstraction pushed to its limit: ONLY horizontal and
vertical black rules, enclosing blocks of red / yellow / blue on white. No
diagonal, no curve, no depicted thing, ever. Rules vary in WEIGHT; blocks vary
in size; the whole composition is asymmetric division of a rectangle.

**ORDER: orthogonal subdivision.** Use when the mechanism is a partition — a
lattice, discrete states, a basis decomposition, a routing table, a set of
disjoint regions. The subdivision must BE the data (block area ∝ a real
quantity), never a decorative Mondrian pastiche.

Pen: black rules at 2–4 passes (`giant_type`-style weight); blocks as serpentine
`fill_rect` in one primary each; cream or white stock. Brutally cheap to plot —
few, long, straight strokes. **This is the canon to reach for when a plate is
drifting toward illustration.**

## 8. RUSSIAN CONSTRUCTIVISM (1910s–20s)

Rodchenko, Lissitzky, Stenberg brothers. Design as social instrument: one
aggressive DIAGONAL axis, heavy black + red only, solid geometric masses
(wedges, discs, bars), type set along the diagonal at poster scale, radiating
line fans. Photomontage is its signature and is NOT available to a pen — the
line equivalent is a dense halftone or hatch mass standing in for the photo.

**ORDER: diagonal thrust and counter-thrust.** Use when the mechanism has a
dominant direction, a flow, a driving asymmetry, an opposition of two forces.

Pen: `fat_outline` keylines, serpentine-filled wedges, `giant_type(angle=...)`
on the diagonal, `ray_fan`. Two pens only — black and red. Loud, scarce accent.

## 9. PSYCHEDELIC (1960s)

Wes Wilson, Victor Moscoso. A revolt against Swiss cleanliness: warped melting
letterforms that fill every void, vibrating complementary colours, legibility
deliberately fought for. The vibration is an optical effect, not a pigment one,
which is why it translates to line at all.

**ORDER: continuous warp.** Use when the mechanism IS a deformation — a field
bending, a metric warping, a phase distorting, a resonance. The type warps on
the same field as the subject; one displacement function drives everything.

Pen: near-parallel line families at small angular offsets for true physical
moiré (see `moire_layers`), `domain_warp` for the ground, and type displaced by
the same warp field (`warp_type`). Complementary pen pairs sitting at equal
value so they buzz rather than separate.

## 10. MEMPHIS GROUP (1980s)

Sottsass, Milan. A postmodern rejection of good taste: squiggles, triangles and
confetti scattered against a grid ground, neon and pastel against primaries,
emotion and HUMOUR privileged over function. The one canon in this list that is
constitutionally unserious.

**ORDER: scattered primitives on a strict ground.** The tension is the whole
point — a rigid grid or terrazzo field, violated by confetti that obeys no
alignment. Use when the mechanism is noise against structure, sampling,
stochasticity, defects, or when a plate needs the earnestness knocked out of it.

Pen: `confetti_field()` over a plotted grid, `squiggle()`, `fat_outline` on the
larger masses. Deliberately more pens than usual (4), used as flat categories —
the one place this studio's "scarce accent" rule is suspended on purpose.

## Kit obligations (build as needed in the style's first piece)

- deco kit: `ray_fan()`, `stepped_border()`, `chevron_band()`, `line_gradient()`
- de stijl kit: `orthogonal_subdivision()` (weighted asymmetric rect split) —
  `fill_rect` + weighted rules already cover most of it
- constructivist kit: **`giant_type(angle=)` BUILT** (type on any axis),
  `ray_fan()`, `wedge()`
- psychedelic kit: `warp_type()` (glyphs displaced by a field), `vibrate()`
  (near-parallel families at a few degrees' offset)
- memphis kit: **`confetti_field()` BUILT**, **`squiggle()` BUILT**
- swiss kit: **`modular_grid()` BUILT**, **`giant_type()` BUILT** (stroke font at
  display sizes, with a `weight` in mm that thickens each glyph into a band —
  type as MASS); `line_screen_tone()` still to build
- pop kit: **`benday_fill()` BUILT** (dot lattice, radius carries tone),
  **`fat_outline()` BUILT** (multi-pass contour band); `panel_grid()` still to build
- bauhaus poster: **`concentric_disc()` BUILT** (circle of N even rings),
  warm-on-cream pen set
- radial data-viz kit: `arc_ring()` (partial concentric arc per datum),
  `radial_ticks()`, `rim_labels()` (stroke-font labels around a circle)
- science-poster kit: `ray_field()` (density-ramped parallel scanlines off a
  body), `data_footer()` (columns of stroke-font text + line micro-charts)

**The BUILT helpers live in `engine/kit.py`.** They went unbuilt for a long
time and the cost was concrete: with only caption-sized `type_block` and
drafting furniture available, every piece defaulted to technical drawing no
matter which style it was assigned. A canon with no tooling is a canon nobody
can follow.

Placement: shared helpers grow in `bauhaus.py` only if style-neutral; style
kits live with their first piece in `promptplot/generative/physics.py` or a
`styles_<name>.py` module once ≥2 pieces use them.
