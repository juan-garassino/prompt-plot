# Synth — neural-networks-cnn after r03 · 2026-09-28
route: designer
next round: r04 · parent: r03 (best so far: art 6.71/6 · sci 8/7/7, beating r02's 5.86/4 · 7/7/5 on every min). r02's summit mountain is the one element r03 regressed, so it comes back as a preserve mandate (A14), not as a fork.
Round budget: r04 is designer round 4 of 5. r05 is the last before a forced vote.

## The instruction
Rebuild the HEAD of the stack. Leave the four lower planes alone except for the gradient fixes below. Make the 7² CAM plane the one resolved landscape the whole sheet climbs to.
- **Interpolation.** Drop the cos²-per-unit hills. Interpolate CAM like the lower maps (bicubic, or whatever `a14` uses) so the col-3 ridge reads as a ridge and no valleys are invented between equal neighbours.
- **Rows.** Draw all 7 rows as continuous hidden-line profiles, each running unbroken across the plane.
- **Silhouette.** Give the argmax mountain a black silhouette from base to cap.
- **The binding constraint (science).** Choose the height scale as the LARGEST value at which every cell ≥ 20 % of the peak (13 cells) still shows its own summit on the sheet. Measure it by sweeping the scale, and print the pass count in NOTES. The critic's estimate is ≤ 1.9 mm/unit. You may reverse the viewing direction if the measurement shows it lets a taller scale pass. If you do, reverse it on ALL five planes and their ERF loops, and state which image edge is at the front.
- **Height progression.** The summit must still be the tallest single relief on the sheet. Where that conflicts with the scale above, lower the relief of the 14²/28² planes on a declared monotone height progression; do not raise the summit past the visibility bound. That same progression is what makes the Schotter gradient calm toward the top.
- **Crimson.** It stays exactly 4 ERF loops plus the summit. The summit isolines become closed level sets of the DRAWN field around unit (4,3), above a level you state. They sit on the black mountain, with the back half hidden by the peak and a 1 mm clear gap between black and crimson.
- **Space.** A lower peak frees vertical space. Re-solve the one equal gap G and let the stack use that space. Keep plane widths monotone on the one basis, with nothing cropped.

## Mandates to close
1. **A14 + A4 + S8: the head (one mandate, three tests).**
   - (a) Summit count: all 13 CAM cells ≥ 2.0 show a summit, including (3,3) = 6.86, (2,3) = 4.26 and (3,1) = 3.72. Report "n / 13 visible" in NOTES.
   - (b) Row count: count 7 continuous rows on the top plane, with no top-plane fragment under 4 mm and no flat zero-row that reads as a baseline rule.
   - (c) Mountain: the argmax hill has a black silhouette from base to cap and is the tallest relief on the sheet.
   - (d) Contact: no black within 1 mm of crimson.
   When art and science conflict here, science's visibility bound wins and the art is solved with the height progression (the same precedent as A6/S1).
2. **A15: a monotone Schotter gradient and resolution channel.** Row count strictly decreasing and flat pitch strictly increasing. For example: 224² at stride 6 (38 rows), 56² at stride 2 (28), 28² at stride 2 (14), 14² (14 → pitch must still increase, so pick the strides so both hold, and state them), 7² (7). Breaks per row fall strictly from bottom to top, so 28² is calmer than 56². No stroke under 3 mm anywhere. Remove the spike at x 76–81 / y 143–150 and the torn corner at x ≈ 50 / y ≈ 115. Print a per-plane table in NOTES (rows, pitch, breaks per row, shortest run).
3. **A3 (occlusion clause): ERF loops go through the hidden-line.** Wherever a nearer ridge of the same map rises in front of a loop, the loop breaks with ≥ 0.8 mm clear on each side. Test: at least one visible break on the 14² loop (back arc, x 105–125, y 185–192 in r03 coordinates) and on the 28² loop, and no crimson crossing the face of a nearer black ridge. This is the second round this clause has been asked for, **so a miss routes to the translator.**
4. **S2 (+ S7): the caption decodes the stack** in ≤ 3 flush-left lines:
   - map the resolutions to the planes ("BOTTOM → TOP 224² 56² 28² 14² 7²", or the numeral at each plane's left edge)
   - name the height ("INPUT LUMINANCE · ‖ACTIVATION‖ · CAM − MEAN, CLIPPED AT 0")
   - render the colon in "CRIMSON:" (use a word or a dash if the font has no colon)
   - "≈26 % OF IMAGE VS ONE CELL = 2 %"
   - "CENTRE-CROP"
   - if you reverse the view, the front edge
5. **A11: title double-stroke.** De-duplicate the retraced glyph strokes before the second pass, or draw the title single-pass. Measure the closest same-pen parallel in the title and report it; it must be ≥ 0.8 mm or 0.

Deferred: none of these. S6 (dossier/encoding) is process, outside the designer's reach. A12 cream is argued as tooling; repeat the engine request.

## Preserve
- **The one forward pass** (whole sheet): same `maps.npz`, argmax (4,3), front rows correlating ≥ 0.994 with their maps. Do not re-run the network or change preprocessing.
- **The four ERF loops** (lower planes): 50 %-mass moment ellipses within 0.5 mm of recompute. Each is ONE closed run, now also broken by occlusion (mandate 3), and they step right onto the summit.
- **One grammar** (every plane): horizontal hidden-line profile rows only. No column lines, mesh, ticks, drop-lines or rails, and nothing crimson between planes.
- **One projection basis** (paper = (X + 0.5 D, 0.58 D + Z), D = 0.45 W) with plane widths shrinking monotonically, right-flush at x = 195, and nothing cropped. Every ink edge ≥ 5 mm inside the frame. Title cap top ≥ 6 mm under y = 287.
- **Equal inter-layer gaps** (r03: 10.9 mm ×4). Re-solve them, still equal.
- **The diagonal and counterweight**: input full-width at the bottom-left, summit top-right, title block top-left over the empty wedge (x 10–70, y 60–215).
- **Plot economy**: under 12,000 commands, travel ≤ 0.3 × draw (r03: 9,826 cmds, 3.5 m travel against 13.3 m draw), 2 pens.
- **PIXELS without flood** (y 15–55): pitch ≥ 1.0 mm.

## Do not
- Do not buy the mountain's dominance by exceeding the visibility bound. A dramatic spike that hides the runner-up is the r03 lie.
- Do not switch the top plane to a different grammar (plan-view isolines, per-cell marks). Science offered that route, but it breaks A2's one grammar. Only take it if the height sweep proves no scale passes both the 13-cell test and a visible mountain, and show the sweep in NOTES.
- Do not force the summit isolines to lie inside cell (4,3) by reshaping the data (that is what created the cos² hills). They are level sets of the drawn field, and NOTES says where they sit.
- Do not claim "closed" for isolines whose back half is hidden: they are closed level sets, drawn visible-only. Describe exactly what the sheet shows (r03's HANDOFF was wrong on this).
- Do not leave the type axis 3 mm off the input plane's corner (x 14.5 against 17.5). Either share it exactly or separate the two by ≥ 8 mm.
- Do not add a connector, frustum, rails, label words on planes, or a sixth crimson element.
- Do not hand-roll z-buffers if `Scene3D` can do it. The rows-only surface still needs `scene._rasterize`, so repeat the engine request.

## Fabrication gate
Not run: both critics FAIL (art 6.71/6 · sci 8/7/7).
