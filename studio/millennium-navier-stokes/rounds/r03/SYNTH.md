# Synth — millennium-navier-stokes after r03 · 2026-09-29
route: **translator**. Amend `encoding.md` to v2, then designer r04.
next round: r04 · parent: **r03's piece.py**. It is the latest round and the science-clean state: sci PASS 9/9/8, with S1, S2 and S3 closed in it. r04 must **restore r02's hero geometry and disc placement**. r03 regressed both, and they are the preserve list below. Best so far stays **r01** (art 6.71/6 · sci 9/9/8). r03 ties it on verdict and loses on art min (5 against 6).

Why translator (route rule 2):
- The badges diagnosis is now mandate **A7**, and it was NOT FIXED in two consecutive rounds.
  - r02 art: "every vortex cut out as a circle… a string of blue badges".
  - r03 art: "rungs 1–4 are still round cut-outs on a ruler line, which reads as 'badges on a string'… the badge diagnosis is repeated for the third time. The lead should weigh it".
- The r03 designer: "rungs 1–4 are still four complete discs in white space with self-similar gaps… inside those constraints I could not make them one surface."
- Those constraints are the encoding's own. §4 draws each rung as a disc truncated at R_out, with self-similar rim gaps \|C_n − C_{n+1}\| = k·(R_n + R_{n+1}). A2 added a ≥ 8 mm hero → rung gap. No layout move can dissolve badges that the channel table defines.
- The terminus defect **A9** is also an encoding rule. §4 sets the red ring at r = \|C₅ − L\| + R₅ = 12.94 mm. That is larger than rung 3 (11.25) and rung 4 (5.63), so at 3 m the ladder "ends at a bigger circle".

## The instruction
Translator: rewrite the ladder so the cascade is **one self-similar surface that drains into a point**, not five discs on a ruler, and keep it exact.
- **Start from the r03 designer's proposal** (`rounds/r03/NOTES.md` § Self-critique). Bound each rung by its cell in the multiplicatively-weighted Voronoi tiling of the orbit, not by a circle. The boundary between rungs n and n+1 is the Apollonius circle |x − C_n| = 2|x − C_{n+1}|.
  - Because L = 2C_{n+1} − C_n is the similarity's fixed point, every boundary passes through L. Its diameter runs from C_n + ⅔(C_{n+1} − C_n) (= 6δ_n at factor 1.20) to L.
  - So the cells form a pencil of circles all tangent at L, and the tiling is exactly invariant under "scale ½ about L".
  - Every point is still on its own rung's exact Burgers streamline. Neighbouring rungs meet one pen floor apart along a shared arc.
- Decide and write down:
  - the outer cap for the hero cell (≈ 7δ₀, and what the frame crops);
  - how streamlines end at a cell boundary (stop ≥ 0.8 mm short, never pause-resume);
  - whether "NS SCALING: COPIES, NOT ONE INSTANT" is still true of a tiled surface, and what caption makes it so;
  - that the A2 "≥ 8 mm to rung 1" and "rim" tests are retired.
- If you reject the Apollonius tiling, give an alternative that passes the same test: at 3 m no rung reads as a free-standing disc.
- **Replace the terminus rule** so the red mark continues the diminishing series. Options: a red dot or ring smaller than rung 4 at L, or the tangency point of the pencil marked in red. The enclosure meaning ("everything the pen cannot draw") moves into the caption, not the geometry.
- **Re-place the hero** so its **eye is on paper**. C₀ sits inside the frame, at x ≈ 40–50 per art or ≥ 18 per science, and the frame crops only far-field arms, as r02 had it. Re-solve δ₀ and the orbit length so L stays on A3 (r03 found δ₀ 20 at factor 1.20 puts L off-sheet, so δ₀ 18 was used). Restate the dominance rule by visible area and ink (hero ≥ 3× rung 1, pen-0 ink > rung 1).
- **Put the disc back off-axis upper-right** (r02 placement). Tie every caption to its element within 12–15 mm.
- **Do the housekeeping (S5).** §2's headline still says "…and it can keep shrinking", which is the S1 lie; replace it with r03's conditional statement. Record factor 1.20, δ₀, R_out, the hero on its own 0.5 mm blue nib, the stamp in black, and red = L mark only.

Then r04 designer builds on r03's code against encoding v2.

## Mandates to close
1. **A7 — the ladder is one surface, not badges** (encoding: rung boundary, gap rule). Test for r04: at 3 m no rung reads as a free-standing disc in white space. The critic's tension score must not repeat the badge diagnosis.
2. **A9 — the terminus continues the series** (encoding: red rule). Test: going down the diagonal, every successive closed form is smaller than the one before, the red mark included, and 0 blue lies within 0.8 mm of red.
3. **A8 — the hero's eye is on paper** (regression from r02; encoding §5 placement). Test: the bare eye and ≥ 1½ inner turns are inside the frame, it is the largest complete spiral on the sheet, pen-0 draw > rung 1 draw, and the frame still crops the far field over a long height.
4. **A10 — captions anchored, disc off-axis, type budget.** Test: disc centre x ≥ 213.5, right rim ≤ 10 mm from 282, no caption > 15 mm from what it names, type < 35 % of plot minutes (r03: 57/104).
5. **S5 — encoding housekeeping.** Test: encoding v2 §2 and §4–§6 describe what r03 built, plus the v2 changes. No sentence in the encoding asserts that an unforced vortex shrinks.

Deferred: S6 (within-rung halving bands, an advisory under a PASS; revisit if v2 keeps the halving cull) and A6 (travel).

## Preserve
- **Science state of r03, verbatim.** Blue is the closed-form Burgers θ(s) at Re_Γ = 100, with pitch within 0.7° over ρ 0.35–4.9 in every rung. There are 18 Lamb–Oseen rings at equal Δψ (CV 0.014 % at r_c = δ₀). Ladder radii are exactly 2.000:1 and the congruent copies are measured to 0.16 mm. Rung 5 is absent below the 0.8 mm floor. The blue floor is **0.824 mm with 0 violations**.
- **r03's words.** These stay on the sheet exactly:
  - statement: "FLAT, A WHIRLPOOL IS ONLY RINGS. THE SPIRAL IS THE THIRD DIMENSION. / WHETHER IT CAN SHRINK TO A POINT ON ITS OWN IS OPEN."
  - "IF THE LADDER FINISHES, IT FINISHES HERE, IN 4/3 OF THE FIRST RUNG'S TIME: VORTICITY ×4 EACH RUNG, INFINITE AT ONE POINT. THAT BLOW-UP, NOT TURBULENCE, IS THE QUESTION."
  - the dated stamp;
  - "FROM 1/4 ON, THE INK IS THE 0.8 MM PEN FLOOR";
  - the Kraichnan clause (notes corner, bottom-left);
  - "LARGE SCALES TO SMALLER ONES" on the 3D ladder only.

  No "T0" glyph.
- **r03 craft wins.**
  - The hero on its own **0.5 mm blue nib**, which makes it the heaviest blue at physical width.
  - Rings on black 0.3, sharing a pen with type (no swap).
  - The title passes 0.25 mm apart under a 0.3 nib.
  - Type flush **by ink** on x = 15 / x = 282, bbox exactly [15.00, 282.00], last baseline y = 20.
  - ≤ 7 caption blocks.
  - Red < 1 % (r03: 0.93 %).
  - Every judgement made on a `_phys.png` rendered with `pen_widths=`.
- **r02's hero and disc (restore these, which r03 regressed).** The hero eye on paper (r02 had it at (62, 272)) with 2+ turns visible, cropped by the x = 15 frame through far-field arms only. The black ring disc upper-right, off-axis (r02: centre x 228, right rim ≈ 267), with its caption directly beside it on x = 282.
- **Layout bones.** One straight diagonal from the hero at top-left to the red mark at bottom-right. The bare lower-left quiet triangle, with only the notes corner. The title and statement top-left on x = 15.
- **Plot budget table** in NOTES and HANDOFF: strokes, draw, travel and minutes per layer, in the order blue 0.5 → blue 0.3 → black rings → black type → red. This is a curator requirement. Streamlines ≥ 0.8 mm, and each rung batchable as its own re-zero point.
- **Lineage:** Bridget Riley, *Blaze 1* (1962), named in NOTES. The Apollonius pencil is also a live conversation with Riley's *Blaze* and *Current*: tangent circle families as a surface. The translator may cite it.

## Do not
- Do not crop the hero through its core. The r03 crop met A2's letter and destroyed the hero's spiral. The frame cuts far-field arms only.
- Do not let the red mark be bigger than the last rung, and do not "fix" it by drawing blue inside it.
- Do not move the disc toward the sheet centre to fill a void. The void was the caption's fault; anchor the captions instead.
- Do not add a rung outline, a boundary stroke, a halo box or any furniture to make the tiling "read". A cell boundary is where streamlines stop, never a drawn line (encoding §4: rung outline circles are deliberately not encoded).
- Do not change Re or δ between rungs, and do not tune spirals by eye. Re-measure the red position at L after any orbit change.
- Do not revive the side view (abstract line; r01 keeps it as the faithful flavour).
- Translator: do not re-open the style, the lineage or the three-family palette. The science is PASS. Amend only §2 (headline), §4 (rung boundary, terminus, δ₀ / R_out / orbit numbers), §5 (placements, retired tests) and §6 (pens: the 0.5 hero nib, the black stamp).

## Gate
Not run. No round has a double PASS (r03: art FAIL 6.00/5, sci PASS). Nothing under `promptplot/` was changed by this piece's rounds. Engine requests are logged in r03 NOTES and not built: a `--pen-widths` flag on `render_candidate.py` and an inked x-extent from `_stroke_text`.
