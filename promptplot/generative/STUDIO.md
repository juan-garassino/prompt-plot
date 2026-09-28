# THE STUDIO — agent team & pipeline for plotted science infographics

Goal: map what is hard to visualize (astrophysics, quantum mechanics, ML) into
simple, artistic, TRUE pen-plotter pieces. Every piece runs this pipeline; every
artifact is written to `studio/<piece-slug>/` so rounds are reviewable.


**Before reworking any piece, read `studio/<piece-slug>/FEEDBACK.md`.** It carries Juan's verdicts and notes on specific renders, written from the gallery viewer, and is an input to the DESIGNER role exactly as `encoding.md` is. `studio/QUEUE.md` lists what is open.

**Reconstructing a reference image (`studio/<slug>/ref/reference.png`)?** The method is `studio/AUTHORING.md` — an illustrator's reconstruction as an authored `Scene` (`promptplot/scene/`), never a trace. Both seats run it: `promptplot studio design <slug> --mode scene --reference img.png` in-app, or a Claude Code agent writing the Scene JSON by hand. The critic sees reference and render side by side.
## Roles

Every role except the curator and the gate is a real Claude Code agent in
`.claude/agents/`: `studio-expert`, `studio-translator`, `studio-designer`,
`studio-art-critic`, `studio-science-critic`, `studio-lead` (synthesis, the ledger, routing
and the fabrication gate). The curator is the main Claude Code session — subagents cannot
dispatch subagents.

1. **CURATOR (main loop)** — owns the series, writes the one-line brief, chains
   the agents, resolves deadlocks, final gate before Juan's vote. Series
   coherence: the collection must feel like one hand.

2. **FIELD EXPERT** (astrophysicist / quantum physicist / ML researcher — one
   agent per domain). Input: topic. Output `dossier.md`:
   - the phenomenon in ≤5 lines, the governing quantities/equations
   - three candidate **visual truths** — quantitative relationships that could
     carry a drawing (ranked; each with "why it's visually potent")
   - REAL data sources or exact formulas to use (never fake data — house rule:
     real GPT-2 attention, real Luminet solutions, real LIGO strain, …)
   - honest simplifications allowed vs. distortions that would make it a lie
   - what laypeople commonly get wrong (the piece should quietly correct it)

3. **VISUAL TRANSLATOR (information designer)**. Input: dossier. Output
   `encoding.md`:
   - the STYLE assignment for the piece — one of the four canons in STYLES.md
     (Bauhaus / Art Deco / Swiss-ITS / Pop Art), with one line on why this
     movement fits this phenomenon; all styles are line-native by house rule
   - the one-glance statement the drawing must make
   - channel mapping: which quantity → position / length / density / angle /
     pen; Tufte discipline — nothing drawn that encodes nothing
   - composition sketch in words+coordinates (A4, margins, where masses sit)
   - pen budget (≤3–4) and what each pen MEANS
   - forbidden list for this piece (e.g. "no decorative orbits")

4. **DESIGNER (builder)**. Input: encoding.md + DESIGN_RUBRIC.md + the ledger's open
   mandates. Builds a candidate in its own `studio/<slug>/rounds/rNN/piece.py` on the
   engine (never under `promptplot/`; never two designers in one round), renders to
   ~/Downloads root with a bumped `_vN`, ≥3 self-scored iterations, uncommitted.

5. **CRITIC PANEL** — two independent agents, both see the png cold:
   - **ART CRITIC**: DESIGN_RUBRIC six dimensions (avg ≥8, none <7) JUDGED
     AGAINST the piece's assigned style canon in STYLES.md (Deco may be
     symmetric; Swiss must not be; Pop must repeat meaningfully), 3 mandatory
     changes on fail → `rounds/rNN/critique-art.md`.
   - **SCIENCE CRITIC** (same domain as the expert, different instance; gets
     dossier + png, NOT the code): truth (is the physics right?), encoding
     fidelity (does the visual quantitatively match, no lying areas/scales?),
     insight legibility (does the phenomenon land?). Each ≥8. 3 mandatory
     changes on fail → `rounds/rNN/critique-science.md`.

6. **FABRICATION GATE** (no LLM): pytest green, validate_gcode clean, stroke
   spacing ≥0.8mm, pen swaps ≤4, draw time sane. Automated, non-negotiable.

## The loop

brief → EXPERT dossier → TRANSLATOR encoding → DESIGNER build/render
→ CRITIC PANEL (parallel) → fail: back to DESIGNER with both critics' mandates
→ 2 consecutive fails on the same mandate: back to TRANSLATOR (encoding is the
problem) → encoding declared unworkable: back to EXPERT for the next visual
truth → both critics pass → FABRICATION GATE → Juan votes → winner moves to
leo/, then commit.

## Iteration protocol — the files are the memory

Agents are stateless; rounds improve only because each one reads what the last one wrote.

```
studio/<slug>/
  FEEDBACK.md        Juan's verdicts (generated) — outrank everything, become J* mandates
  DESCRIPTION.md     vision review of the CURRENT version: sheet in (u,v), Keep, Weak, next
                     theses — the starting spec; seeds the ledger; refreshed at each vote
                     (the previous one is archived to history/, never overwritten)
  dossier.md         expert: truths, lies list, §7 CHECK NUMBERS the science critic recomputes
  encoding.md        translator: order, mapping, §11 ACCEPTANCE CHECKS the art critic runs
  LEDGER.md          lead: score history, best-so-far, every mandate (A*/S*/J*) + status
  rounds/rNN/        one candidate — never reworked in place; a rework is a new round
    piece.py  NOTES.md    designer (NOTES answers every open mandate by id)
    HANDOFF.md            designer → critics: render path, paper, pen meanings; no rationale
    critique-art.md       pass 1 cold score + 3 mandates; pass 2 follow-up on open mandates
    critique-science.md   check numbers recomputed + measured off the gcode; follow-up
    SYNTH.md              lead: route, next round + parent, ONE instruction, preserve list
```

The lead's routing rules: same mandate failing twice → translator; unworkable encoding →
expert; best-so-far flat for 2 rounds → a composition move or fork from the best round;
regression → parent reverts to the better round; 5-round cap → vote with an honest note.

**Running it (curator):** dispatch expert → translator → N designers in parallel (one round
each, one thesis each: `faithful` / `mechanism` / `abstract` / a named lens) → both critics
per round in parallel → lead → repeat from the SYNTH.md work order. Commit before each rework
round. Sync `~/Downloads` into `gallery/` only after the batch finishes.

**Running it as a workflow:** `.claude/workflows/studio.js` runs exactly that loop per plate,
plates in parallel. Its args come from the description index:

```
python scripts/studio_descriptions.py           # rebuild studio/DESCRIPTIONS.md (one row per plate)
python scripts/studio_descriptions.py --json    # rows with slug, theses, next_round, parent
```

Pick plates and theses from the JSON, then run the `studio` workflow with
`{plates: [{slug, theses, next_round, parent, domain}], iterations: 2}`. Each plate costs
roughly (theses × 3 + 1) agents for the fan-out and 4 per follow-up round. It stops at `vote`;
Juan's verdicts in the viewer become J* mandates for the next run.

## House rules

- Real data or exact math only; the dossier names the source.
- Previews always to ~/Downloads root; leo/ only after Juan promotes.
- Every piece: seeded, deterministic, bounded, registered, tested.
- Critics never see code or the designer's notes. Designers never grade
  themselves as final. The curator never overrides a double-fail silently.
