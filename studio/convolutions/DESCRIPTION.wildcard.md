# CONVOLUTIONS (every squiggle is a sum) — description

<!-- site text for one plate of this folder (prints.json `describe`); written 2026-10-11 from a vision review -->

## Lede
Three different lenses look at the same scattered set of points, and each one sees a completely different pattern. The plate's tagline says it plainly: every squiggle is a sum.

## On the sheet
Small black triangles are scattered across the whole sheet; each one is a single "impulse", one bright pixel and nothing else. Over them sit three bold frames, each holding a different kernel. On the left, a big circle where crimson contours stretch into long diagonal strokes, leaning at 30°. On the right, an inverted triangle full of blue ellipses tilted the other way, at 120°. In the middle, a tilted square where soft orange blobs wrap around the points.

Where the strokes pile up densely, the lines fill in with solid hatching. A ruled grid in the lower right sets the scale, and the key beside it gives the rules: a thin line marks where the response equals 0.35, and solid fill marks where it climbs above 1.25.

## The science
Convolution is *linear*, and that one word explains the whole plate. If you know how a kernel responds to a single bright point, you know how it responds to anything: you just add up its response to every point. Each kernel stamps its own little signature around each triangle. Two Gabor filters — wave-shaped kernels, close cousins of the edge detectors in your own visual cortex — stamp short striped bars, one at 30° and one at 120°. A Gaussian blur stamps a soft round bump. Where triangles sit close together, the stamps overlap and add up.

The fill threshold is chosen to prove the point: a single impulse can never get above 1 on its own, so every solid patch you see is somewhere two or three nearby points have added up to more than 1.25 — a pattern no single point could make. The grid spacing, 12 mm, is exactly the wavelength of the two Gabor filters, so you can measure the stripes against it. Same points, three lenses, three different worlds — which is what the first layer of a CNN is doing with dozens of filters at once.

