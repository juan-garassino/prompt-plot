# THE GESTURE LAYER — a mark-making module for the engine

**References:**
- `studio/gesture-engine/ref/reference.png` — a charcoal gesture drawing. THE TARGET
  QUALITY. Study it.
- `studio/gesture-engine/ref/test_subject.png` — a dense cubist ink drawing, the hard
  test case.

## The gap this fills

`promptplot/generative/engine/` has `scene3d.py` (where surfaces go), `kit.py` (2D
furniture), `geometry.py` (exact CAD ops), `policies.py` (anti-crowding) and
`looks.py` (effects). Every one answers **where the line goes**. None answers **what
kind of mark it is**. So every piece in the collection inherits the same uniform
machine stroke.

Juan's words: *"needs to be single lines drawing. like if was done by a human! not
line segments. or barcode like. but truly different lengths segments depending of
what is representing"* — and *"this should then be part of the engine. exactly none
of those had it."*

## What a gesture drawing actually does

From the reference:
- **One continuous stroke describes one whole form.** The sweep of the back is a
  single mark. Length is decided by the FORM, never by a cell size or dash parameter.
- **Overshoot** — strokes run past their endpoints and cross each other. The
  construction lines are left visible; they are part of the drawing.
- **Searching strokes** — the same contour found two or three times, slightly offset.
  A confident single line is *less* human than three approximate ones.
- **Weight varies** — some strokes dark and committed, others faint feelers.
- **Most of the paper is blank.** Weak structure is never drawn at all.

## Why every current generator fails it

`line_halftone`, `scribble_halftone`, `scribble_portrait` all emit **a field of marks
on a grid**. The cell size sets the length, so every mark is the same length — that
is exactly the "barcode" quality Juan is rejecting. The form never gets to decide how
long its stroke is. Measured on the test subject: `scribble_halftone` gives 5,714 pen
cycles of uniform 5.2 mm dashes. The reference drawing would be a few hundred strokes
of wildly differing length.

## What to build

A module that turns **structure into strokes**, usable two ways:
1. **From an image** — extract the drawing's forms and render them as gestures.
2. **From a piece's own geometry** — any existing polyline should be renderable as a
   gesture rather than as a clean machine line. This is what makes it an ENGINE layer
   rather than another image generator, and it is the more important of the two.

Shape suggestion, not a mandate:
```python
def gesture(poly, overshoot=..., searching=..., weight=..., jitter=...) -> list[poly]
def gestures_from_image(path, ...) -> list[poly]   # long chains, form-decided length
```

## What must be TRUE

- **Stroke length must be decided by the form**, and you must MEASURE it: report the
  distribution of stroke lengths (min / median / max / histogram). A tight
  distribution means you built another screen and failed. The reference would show a
  broad spread over an order of magnitude.
- **Stroke count is low.** Hundreds, not thousands. If you emit 5,000 marks it is not
  a gesture drawing.
- **Blank paper is a result, not an accident** — report the fraction of the sheet left
  untouched.
- Deterministic from the seed, like everything else.
- It must be plottable: report draw / travel / pen cycles, and stay in bounds.

## Where your code goes — IMPORTANT

Develop as a **standalone module in your own round directory**:
`studio/gesture-engine/rounds/rNN/gesture.py`, plus a `demo.py` piece that renders
proof. **Do NOT edit anything under `promptplot/`.** The winning approach gets
promoted into `engine/` afterwards, deliberately, by Juan's call — that is how this
lands in the engine without three agents fighting over one shared file.
