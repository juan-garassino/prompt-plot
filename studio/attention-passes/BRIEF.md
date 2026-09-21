# ATTENTION — FORWARD AND BACKWARD
*Q, K, V out and the gradients back, on one sheet*

**Reference:** `studio/attention-passes/ref/reference.png`
**Status:** to build. New family — NOT a rework of `studio/attention-dag/`,
`studio/resonance*/` or `bauhaus_relevance`. Those are different compositions of the
same subject; do not inherit their layout. Read them only to avoid repeating a move.

## Essence

Attention drawn as **flow between three sources and one sink, then the same flow
run backwards**. The subject is the *shape of the routing*: three distinct fields
converge through two bottlenecks (similarity, then softmax) into one output, and the
gradient retraces that path with the arrows reversed. Softmax is the waist of the
whole plate.

## What the reference does

**Top register — forward pass**
- Far left, stacked vertically: three **lobed dot-field wells** labelled `Q` (blue),
  `K` (black), `V` (red). Each well is a teardrop of dotted contour lines spiralling
  into a small filled square node, each with a different lobe shape — they must not
  read as three copies. Short vertical rules beside the labels as tick marks.
- Dense bundles of curves sweep right out of each well.
- Three **vertical dotted rules** cross the sheet, labelled at the top in lowercase
  mono: `similarity` · `softmax` · `weighted values`.
- At `similarity`: a **lattice of dots of varying size** — the QKᵀ score matrix,
  read as a grid, not a blur.
- At `softmax`: a very dense **vertical comb/spike** — dot size along the axis is the
  normalised distribution. This is the tightest, loudest mark on the sheet.
- The bundles converge right into a filled square node `Z`.

**Bottom register — backward pass**
- The same three wells mirrored, labelled `∂L/∂Q` (blue), `∂L/∂K` (black),
  `∂L/∂V` (red), on the same three rows as their forward twins.
- Flow lines carry **small arrowheads pointing left** — the only arrowheads on the
  plate, and they are what marks the direction.
- `∂L/∂Z` at the right, with the label `backpropagate gradients` above it.

**Bottom axis:** `forward pass ⟶` under the left half, `⟵ backward pass` under the
right half, a single dot between them.

Registration crosses at all four corners.

## What must be TRUE

- **Row registration**: `Q` and `∂L/∂Q` share a row; same for K and V. The mirror is
  the argument.
- **Softmax normalises** — the comb sums to one. A few large dots, a long tail of
  small ones. It must be visibly *peaked*, not a uniform column.
- **The three wells differ in kind**, not just in colour. Q is a query direction, K a
  key field, V the content being carried. Give them genuinely different geometry —
  a prior version of this subject was rejected for Q and K reading as twins.
- The backward flow into `∂L/∂V` is routed by the **same softmax weights** as the
  forward pass — V's gradient is the attention weights re-applied. Show the reuse.
- Everything between `similarity` and `softmax` is where the information is
  destroyed — that narrowing should be legible as shape.

## Pens

`blue` Q and its gradient · `black` K, structure, type · `red` V and its gradient ·
cream paper as the fourth colour.
