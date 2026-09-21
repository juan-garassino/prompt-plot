# ATTENTION AS WEAVING
*Q and K interleave, softmax is the waist, V is spun into the braid*

**Reference:** `studio/attention-weaving/ref/reference.png` (1122×1402, ratio 0.800 —
plot on custom paper `--paper 24x30` portrait, which is exactly 0.8)
**Status:** to build. New family. Distinct from `studio/attention-passes/` (a
forward/backward technical plate) and from `bauhaus_loom` (a perceptron drawn as an
Anni Albers weaving). This one is a **braid**, not a woven cloth and not a diagram.

## Essence

Attention as **strand craft**. Four bundles of continuous filaments enter from the
margins, two of them interleave, all of them are drawn through a single narrow waist,
and what leaves is a rope. The subject is the *constriction*: every strand in the
sheet must pass through the softmax bead-column, and the piece is built to make that
throat feel inevitable.

## What the reference does

**Title** `ATTENTION AS WEAVING` in wide-spaced serif caps across the top.

**Four bundles, each ~18–24 smooth filaments, each its own pen:**
- `Q` **red** — enters top-left from a column of margin ticks, sweeps down-right.
- `K` **blue** — enters top-right from a column of margin ticks, sweeps down-left.
- Q and K **interleave in the upper middle** under the label `Q · Kᵀ` — genuine
  over/under crossings, strands passing through each other, not two bundles merely
  overlapping. This is the only place on the sheet where two colours weave.
- `V` **ochre/gold** — enters at mid-left, sweeps right and down, and is *spun in
  below the waist*, not before it.
- `Z = AV` **dark green** — leaves at bottom-right into a column of margin ticks.

**The softmax waist** — dead centre, the narrowest point: the Q·Kᵀ weave collapses
into a tight vertical **column of small beads** (a few dozen dots, sized by weight),
crossed by a horizontal dotted rule, labelled `softmax` in small lowercase italic
beside it. Above the waist the sheet is wide and crossing; below it the strands
re-expand as a **twisting rope** — a real braid with visible over/under, tightening
as it turns down-right.

**Construction geometry, all dotted, all behind:** large compass circles (several,
overlapping, centred on the waist and the bundle mouths), vertical dotted rules with
beads strung on them, open circles and filled dots of varying size scattered as
registration marks. These are drafting scaffold — they must read as *behind* the
strands and must never compete with them.

**Margins:** each bundle terminates in a column of short ticks at the sheet edge,
like a loom's reed. Open circles of varying diameter punctuate the bundles.

## What must be TRUE

- **Everything passes through the waist.** Strand count in = strand count out. If a
  filament is born below the waist or dies above it, the piece is lying.
- **Over/under is real** — at every crossing one strand is continuous and the other
  breaks. Use the engine's occlusion, not luck. This is what separates weaving from
  overlap, and the rubric's OVERLAP IS A DECISION rule applies hardest here.
- **Softmax normalises**: the bead column's sizes sum to one — a few heavy beads and
  a tail of light ones, visibly peaked, never a uniform stack.
- **V joins after the waist**, because `Z = AV` applies the weights to V. The order
  of operations is the composition. Q and K meet *before*, V only *after*.
- The braid below the waist should carry **more strands than either Q or K alone** —
  it is the merge.

## Pens

`red` Q · `blue` K · `ochre` V · `dark green` Z=AV · black for title, ticks and
scaffold · cream paper. Five pens plus paper — the widest palette in the series, so
colour separation must do real work.
