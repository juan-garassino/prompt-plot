# THE KANDINSKY SET — shared note for three plates

Three references in one idiom, new to this collection: **Kandinsky / Bauhaus
colour-block**, not the fine technical drafting of the rest. Flat geometric planes
(triangles, quadrants, checkerboards), hard primaries (red / blue / yellow / green /
black) on warm cream, heavy black rules cutting diagonally across, concentric circle
mandalas, floating dots at many scales, small serif/mono captions.

Members: `studio/kandinsky-diffusion/`, `studio/kandinsky-attention/`,
`studio/kandinsky-latent-diffusion/`.

## Drawing flat colour on a pen plotter

There is no fill. A "flat plane" is a **line-fill**: hatch, serpentine, spiral,
cross-hatch — and the fill's direction and pitch become part of the design. Kandinsky's
flat blocks must become *textured* blocks, and which texture goes where is a decision
to make deliberately, not a default. Different planes should not all be 45° hatch.

## THE TECHNICAL AUDIT — read this before drawing anything

**Juan's note on these three: "some of those have some wrong technical things."**

These references were not made by someone checking the algorithm. Your job is NOT to
reproduce their errors faithfully. **Audit the reference against the real algorithm
first, list every technical error you find, and draw the CORRECTED version.** Then
record in NOTES.md, as an explicit list: what the reference shows, why it is wrong,
and what you drew instead.

Known-suspect points to check (there may be more — and one of these may turn out to
be defensible, in which case say so and keep it):

- **Iteration.** Denoising is a loop, run once per timestep. A reference that draws
  the denoiser as a single box passed through once is telling you sampling is one
  step. It is not.
- **Softmax is per row.** `A = softmax(S)` applied to a matrix gives a *matrix* — one
  normalised distribution per query. A single 1-D curve under a 2-D score grid is at
  best ambiguous and at worst wrong. And a row of equal-height peaks is a *uniform*
  distribution, which is the opposite of attention selecting anything.
- **Shape agreement.** `Z = AV` has one output row per QUERY, not per value. If Q has
  n rows then Z has n rows. Count the rows in the reference and check they agree.
- **The round trip is lossy.** In latent diffusion the `z₀` the sampler produces is
  NOT the `z₀` the encoder made, and `x̃` is not `x`. Labelling both ends identically
  claims the autoencoder is lossless. Draw the difference.
- **Conditioning enters the denoiser, never the forward process.** Noising is
  unconditional. If a reference routes `c` into the noising row, that is an error.
- **Cross-attention is at several resolutions** in a real U-Net, not only the
  bottleneck.
- **The schedule.** Structure decays as `√ᾱ_t`, so it barely moves early and collapses
  late and fast. A linear-looking dissolve across evenly spaced states is wrong.

Correctness outranks fidelity here — the whole point of this collection is that the
style carries a mechanism that is actually true. See `DESIGN_RUBRIC.md`, "BUT THE
STYLE CARRIES THE MECHANISM".
