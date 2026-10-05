# DIFFUSION — FORWARD, NETWORK, REVERSE
*noising across the top, the U-Net through the middle, denoising back along the bottom*

**Reference:** `studio/diffusion-passes/ref/reference.png` (1512×1043, ratio 1.45 →
A3 landscape)
**Status:** to build. New family. **Distinct from `studio/diffusion/` and
`studio/diffusion-topography/`**, which are vertical stacked-plane compositions of
the same subject — read them only so you do not repeat them.

## Essence

Three horizontal registers that together state the whole method: the top destroys,
the bottom rebuilds, and the band between them is the only learned thing on the
sheet. The plate's argument is that the top and bottom rows are *the same sequence
in opposite directions*, and the middle is what makes the reversal possible.

## What the reference does

**Register 1 — forward process (noising), left → right**
- A row of six states: `x₀` `x_t1` `x_t2` `x_t3` `x_t4` `x_T`, separated by `···`.
- `x₀` is a **nest of concentric closed contours** of a lobed rose-like form — the
  data manifold's level sets, clean and black.
- Each successive state is the same nest **progressively perturbed**: contours
  wobble, then break into dashes, then into scattered dots, until `x_T` is an
  isotropic dot cloud with no structure left.
- Header: `forward process (noising)` with a long dashed arrow, and
  `q(xₜ | x₀) = 𝒩(√ᾱₜ x₀, (1 − ᾱₜ)I)`.
- Baseline axis: `t = 0` … `increasing noise` → … `t = T`.
- Captions: `data distribution p_data(x)` under x₀, `isotropic noise 𝒩(0, I)` under x_T.

**Register 2 — the U-Net, centred**
- Title `U-Net  ε_θ(xₜ, t)` / `predicts noise (or v, or x₀)`.
- A **horizontal bowtie**: a wide funnel of dense contour lines on the left
  contracting to a narrow waist at centre, then expanding to a wide funnel on the
  right. Encoder blue, waist purple, decoder red — the same colour ramp as register 1.
- **Skip connections** as dashed arcs arching over the top, each joining a level on
  the encoder to the mirrored level on the decoder. Labelled `skip connections`.
- `xₜ` (a red dot cloud) enters at the left with a solid arrow; `ε̂` (a grey-black
  lobed blob) exits right, captioned `predicted noise`.
- Loss at the right margin: `ℒ = 𝔼_{t,x₀,ε}[ ‖ε − ε_θ(xₜ, t)‖² ]`.

**Register 3 — reverse process (denoising), right → left**
- The mirror of register 1, running the other way: `x_T` (noise) at the right
  through `x_t1 … x_t4` back to a clean black `x₀` at the left, captioned
  `generated sample  x ~ p_θ(x)`.
- Header: `reverse process (denoising)` with a leftward dashed arrow and
  `p_θ(x_{t−1} | xₜ) = 𝒩(μ_θ(xₜ, t), σ²ₜ I)`.

**Furniture:** `DIFFUSION / probabilistic generative modeling` spaced-caps title top
left; `PEN PLOTTER` bottom left with a rule; two small right-margin keyword stacks
(`noise · schedules · score matching · denoising · generative sampling` and `latent
diffusion · text conditioning · classifier-free guidance · high-dimensional data ·
iterative refinement`); registration crosses, small filled squares, dashed
quarter-arcs in the corners.

## Colour is the time axis — note the exception

The series convention is "colour = meaning, never decoration". Here colour **is** the
meaning: a continuous ramp **black → blue → purple → pink → red** encodes t, and it
runs in the same direction in all three registers, so the U-Net's encoder (blue) and
decoder (red) sit at the same t as the states above and below them. This is the one
piece in the collection where a pen ramp is a *variable*. Keep it consistent or the
plate stops working.

## What must be TRUE

- **The top and bottom rows are the same sequence reversed.** Column registration:
  `x_t2` on top sits above its counterpart below. If that breaks, the argument dies.
- The forward noising follows the real schedule: `xₜ = √ᾱₜ x₀ + √(1−ᾱₜ) ε`. Structure
  should decay at the rate ᾱₜ actually gives, not linearly by eye — early steps
  barely change, the collapse is late and fast.
- `x_T` is **isotropic** — no residual lobe structure, no preferred direction.
- The U-Net waist is the **bottleneck**: fewest lines, lowest spatial detail. Skips
  must connect *mirrored* levels and must be what lets fine detail survive the waist.
- The reverse row is **not** a copy of the forward row played backwards: it is a
  different sample. It should arrive at a clean `x₀` that is recognisably from the
  same family but not identical to the forward row's `x₀`.

## Pens

`black` structure, type, furniture, the clean x₀ and ε̂ · then the t-ramp
`blue → purple → pink → red`. Cream paper as ground.
