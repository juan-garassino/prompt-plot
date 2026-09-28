export const meta = {
  name: 'studio',
  description: 'Iterate PromptPlot studio plates from their DESCRIPTION.md: parallel thesis designers, art + science critics, lead, follow-up rounds until a vote',
  whenToUse: 'Newer versions of existing studio plates. args = {plates: [{slug, theses, next_round, parent, domain?, note?, fresh?, topic?, pre?}], iterations, explore_every?}. fresh=true runs expert + translator first; every explore_every-th follow-up (default 2, 0 = never) adds a WILDCARD designer beside the refinement.. Build plates from `python scripts/studio_descriptions.py --json`.',
  phases: [
    { title: 'Research', detail: 'new plates only: studio-expert dossier, then studio-translator encoding' },
    { title: 'Design', detail: 'one studio-designer per thesis, each in its own round' },
    { title: 'Critique', detail: 'studio-art-critic + studio-science-critic per round, blind to code' },
    { title: 'Lead', detail: 'studio-lead ranks/merges, keeps LEDGER.md, writes SYNTH.md, routes' },
    { title: 'Iterate', detail: 'follow-up rounds from the SYNTH work order until vote or the cap' },
  ],
}

const PLATES = (args && args.plates) || []
const ITERATIONS = args && args.iterations != null ? args.iterations : 2
const EXPLORE_EVERY = args && args.explore_every != null ? args.explore_every : 2
const rr = (n) => 'r' + String(n).padStart(2, '0')

// Juan: "remember that you need to try different styles". Every non-faithful design job gets
// a canon from STYLES.md, rotated so parallel theses and sibling plates land on different
// movements. The default "modern science poster" look is left out on purpose — it is what
// the studio falls back to. Faithful keeps its reference's style; iterate keeps its parent's.
const CANONS = [
  'DE STIJL (STYLES.md §7)', 'PSYCHEDELIC (§9)', 'SWISS / INTERNATIONAL TYPOGRAPHIC (§3)',
  'MEMPHIS GROUP (§10)', 'RUSSIAN CONSTRUCTIVISM (§8)', 'ART DECO (§2)', 'POP ART (§4)',
  'RADIAL DATA-VIZ / INFORMATION ARCS (§5)', 'BAUHAUS (§1)',
]
const canonFor = (plateIdx, slot) => CANONS[(plateIdx * 2 + slot) % CANONS.length]

const LEAD = {
  type: 'object', additionalProperties: false,
  required: ['route', 'best_round', 'best_scores', 'next_parent', 'instruction'],
  properties: {
    route: { type: 'string', enum: ['designer', 'translator', 'expert', 'vote', 'done'] },
    best_round: { type: 'string' },
    best_scores: { type: 'string', description: 'art avg/min · sci truth/fidelity/legibility' },
    next_parent: { type: 'string', description: 'round the next designer should fork from, e.g. r05' },
    instruction: { type: 'string', description: 'the one-paragraph SYNTH work order' },
  },
}

function designerPrompt(p, round, thesis, parent, instruction, canon) {
  const brief = thesis === 'wildcard'
    ? `WILDCARD round — a COMPLETELY DIFFERENT approach, deliberately. Do not start from any earlier round's composition or code: read them (and LEDGER.md) only to learn what NOT to repeat. Choose an abstract ORDER and a LINEAGE that no earlier round of this plate used. Keep only the truth (dossier.md or DESCRIPTION.md § The science it encodes) and Juan's FEEDBACK.md. Build it to the same finish as any round — this is exploration, not a sketch.`
    : thesis === 'iterate'
    ? `Your work order is the latest SYNTH.md for this slug${instruction ? ` — in short: ${instruction}` : ''}. With no SYNTH yet, the "If only iterating" mandates in DESCRIPTION.md are your work order.`
    : p.fresh
      ? `This is a NEW plate. Your brief is studio/${p.slug}/encoding.md (read dossier.md too) and the reference studio/${p.slug}/ref/reference.png. Your thesis "${thesis}" is defined in your agent file (faithful = an illustrator's reconstruction of the reference per studio/AUTHORING.md — MEASURED, never traced; mechanism = every mark computed from the real mathematics in the dossier; abstract = transpose to an abstract ORDER under a named LINEAGE).`
      : `Your brief is the "${thesis}" paragraph in studio/${p.slug}/DESCRIPTION.md § Next versions.`
  const style = canon
    ? `\nSTYLE: work in the ${canon} canon — read that section of promptplot/generative/STYLES.md and commit to it (the rubric's "STYLE IS NOT OPTIONAL"; the style must still carry the mechanism). Sibling theses and plates were given different canons so the collection spans movements; change it only with a reason stated in NOTES.md. Put a \`canon:\` line in HANDOFF.md.`
    : thesis === 'faithful' ? `\nSTYLE: keep the reference's own style; put a \`canon:\` line in HANDOFF.md naming the closest canon.` : ''
  return `slug=${p.slug} round=${round} thesis=${thesis} parent=${parent || 'none on disk — rebuild from DESCRIPTION.md § What is on the sheet'}.
${brief}
Other designers may be building sibling rounds of this slug right now — stay inside studio/${p.slug}/rounds/${round}/ and put "${thesis}" in your render filename.${style}${p.note ? `\nCURATOR NOTE (binding for this plate): ${p.note}` : ''}`
}

function critique(p, round, phase) {
  return parallel([
    () => agent(`slug=${p.slug} round=${round}. Critique this round (HANDOFF: studio/${p.slug}/rounds/${round}/HANDOFF.md).`,
      { agentType: 'studio-art-critic', label: `art:${p.slug}/${round}`, phase }),
    () => agent(`slug=${p.slug} round=${round} domain=${p.domain || 'infer it from DESCRIPTION.md'}. Verify this round (HANDOFF: studio/${p.slug}/rounds/${round}/HANDOFF.md).`,
      { agentType: 'studio-science-critic', label: `sci:${p.slug}/${round}`, phase }),
  ])
}

function lead(p, rounds, nextRound, phase, wildcard) {
  const many = rounds.length > 1 ? ' They are parallel theses: rank them, then pick one parent or write a MERGE instruction.' : ''
  const wild = wildcard ? ` ${wildcard} is a WILDCARD (a deliberately different approach): judge it on its own merits; if it beats the refinement line, make it the new parent; if it loses but carries one idea worth keeping, name that idea in SYNTH.md.` : ''
  return agent(`slug=${p.slug}. Rounds just critiqued: ${rounds.join(', ')}.${many}${wild} Update LEDGER.md, write SYNTH.md in the latest critiqued round, and return your routing. The next free round is ${nextRound}.${p.note ? ` Curator note for this plate (enforce it in routing and the gate): ${p.note}` : ''}`,
    { agentType: 'studio-lead', schema: LEAD, label: `lead:${p.slug}`, phase })
}

async function research(p) {
  const ref = `studio/${p.slug}/ref/reference.png`
  await agent(`slug=${p.slug} domain=${p.domain || 'mathematics'}. NEW plate — topic: ${p.topic || p.slug}. A reference poster (AI-made, an interpretation brief, not ground truth) is at ${ref}: look at it. Write studio/${p.slug}/dossier.md.${p.note ? ` Curator note: ${p.note}` : ''}`,
    { agentType: 'studio-expert', label: `expert:${p.slug}`, phase: 'Research' })
  await agent(`slug=${p.slug}. NEW plate — topic: ${p.topic || p.slug}. Translate studio/${p.slug}/dossier.md into studio/${p.slug}/encoding.md; the reference is ${ref}. Designers will build these theses in parallel: ${(p.theses || []).join(', ')} — make the encoding serve all of them.${p.note ? ` Curator note: ${p.note}` : ''}`,
    { agentType: 'studio-translator', label: `translator:${p.slug}`, phase: 'Research' })
}

async function runPlate(p, pi) {
  if (p.fresh) await research(p)
  if (p.pre === 'translator' || p.pre === 'expert') {
    // a relaunch of a plate the lead routed back: run that stage before any designer
    await agent(`slug=${p.slug}. The studio lead routed this piece to you. Read studio/${p.slug}/LEDGER.md and the latest rounds/*/SYNTH.md first; do what the route asks.${p.note ? ` Curator note: ${p.note}` : ''}`,
      { agentType: p.pre === 'expert' ? 'studio-expert' : 'studio-translator', label: `${p.pre}:${p.slug}`, phase: 'Research' })
  }
  let n = p.next_round || 1
  const theses = p.theses && p.theses.length ? p.theses : ['iterate']
  const first = theses.map((t, ti) => ({ t, round: rr(n++), canon: (t === 'faithful' || t === 'iterate') ? null : canonFor(pi, ti) }))

  const built = (await pipeline(
    first,
    (c) => agent(designerPrompt(p, c.round, c.t, p.parent, null, c.canon), { agentType: 'studio-designer', label: `design:${p.slug}/${c.round}:${c.t}`, phase: 'Design' })
      .then((rep) => (rep ? c : null)),
    (c) => (c ? critique(p, c.round, 'Critique').then(() => c.round) : null),
  )).filter(Boolean)

  if (!built.length) {
    log(`${p.slug}: no candidate was built`)
    return { slug: p.slug, route: 'failed', rounds: [] }
  }

  let verdict = await lead(p, built, rr(n), 'Lead')
  const rounds = [...built]
  log(`${p.slug}: ${built.join(', ')} → best ${verdict && verdict.best_round} (${verdict && verdict.best_scores}) · route ${verdict && verdict.route}`)

  for (let i = 0; i < ITERATIONS && verdict && verdict.route !== 'vote' && verdict.route !== 'done'; i++) {
    if (verdict.route === 'translator' || verdict.route === 'expert') {
      await agent(`slug=${p.slug}. The studio lead routed this piece to you: ${verdict.instruction} Read studio/${p.slug}/LEDGER.md and the latest SYNTH.md first.`,
        { agentType: verdict.route === 'expert' ? 'studio-expert' : 'studio-translator', label: `${verdict.route}:${p.slug}`, phase: 'Iterate' })
    }
    const exploring = EXPLORE_EVERY > 0 && i % EXPLORE_EVERY === 0
    const jobs = [{ t: 'iterate', round: rr(n++), parent: verdict.next_parent, instruction: verdict.instruction }]
    if (exploring) jobs.push({ t: 'wildcard', round: rr(n++), parent: null, canon: canonFor(pi, 4 + 2 * i) })
    const done = (await pipeline(
      jobs,
      (j) => agent(designerPrompt(p, j.round, j.t, j.parent, j.instruction, j.canon),
        { agentType: 'studio-designer', label: `design:${p.slug}/${j.round}${j.t === 'wildcard' ? ':wildcard' : ''}`, phase: 'Iterate' })
        .then((rep) => (rep ? j : null)),
      (j) => (j ? critique(p, j.round, 'Iterate').then(() => j) : null),
    )).filter(Boolean)
    if (!done.length) break
    const round = done.map((j) => j.round).join(', ')
    rounds.push(...done.map((j) => j.round))
    const wild = done.find((j) => j.t === 'wildcard')
    verdict = await lead(p, done.map((j) => j.round), rr(n), 'Iterate', wild ? wild.round : null)
    log(`${p.slug}: ${round} → best ${verdict && verdict.best_round} (${verdict && verdict.best_scores}) · route ${verdict && verdict.route}`)
  }

  return {
    slug: p.slug,
    rounds,
    best_round: verdict && verdict.best_round,
    best_scores: verdict && verdict.best_scores,
    route: verdict && verdict.route,
    next: verdict && verdict.instruction,
  }
}

if (!PLATES.length) {
  log('no plates in args — pass {plates: [...]} built from scripts/studio_descriptions.py --json')
  return []
}
log(`${PLATES.length} plate(s), up to ${ITERATIONS} follow-up round(s) each`)
const results = await parallel(PLATES.map((p, pi) => () => runPlate(p, pi)))
return results.filter(Boolean)
