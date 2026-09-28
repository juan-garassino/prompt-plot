export const meta = {
  name: 'studio',
  description: 'Iterate PromptPlot studio plates from their DESCRIPTION.md: parallel thesis designers, art + science critics, lead, follow-up rounds until a vote',
  whenToUse: 'Newer versions of existing studio plates. args = {plates: [{slug, theses, next_round, parent, domain?, note?}], iterations}. Build plates from `python scripts/studio_descriptions.py --json`.',
  phases: [
    { title: 'Design', detail: 'one studio-designer per thesis, each in its own round' },
    { title: 'Critique', detail: 'studio-art-critic + studio-science-critic per round, blind to code' },
    { title: 'Lead', detail: 'studio-lead ranks/merges, keeps LEDGER.md, writes SYNTH.md, routes' },
    { title: 'Iterate', detail: 'follow-up rounds from the SYNTH work order until vote or the cap' },
  ],
}

const PLATES = (args && args.plates) || []
const ITERATIONS = args && args.iterations != null ? args.iterations : 2
const rr = (n) => 'r' + String(n).padStart(2, '0')

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

function designerPrompt(p, round, thesis, parent, instruction) {
  const brief = thesis === 'iterate'
    ? `Your work order is the latest SYNTH.md for this slug${instruction ? ` — in short: ${instruction}` : ''}. With no SYNTH yet, the "If only iterating" mandates in DESCRIPTION.md are your work order.`
    : `Your brief is the "${thesis}" paragraph in studio/${p.slug}/DESCRIPTION.md § Next versions.`
  return `slug=${p.slug} round=${round} thesis=${thesis} parent=${parent || 'none on disk — rebuild from DESCRIPTION.md § What is on the sheet'}.
${brief}
Other designers may be building sibling rounds of this slug right now — stay inside studio/${p.slug}/rounds/${round}/ and put "${thesis}" in your render filename.${p.note ? `\nCURATOR NOTE (binding for this plate): ${p.note}` : ''}`
}

function critique(p, round, phase) {
  return parallel([
    () => agent(`slug=${p.slug} round=${round}. Critique this round (HANDOFF: studio/${p.slug}/rounds/${round}/HANDOFF.md).`,
      { agentType: 'studio-art-critic', label: `art:${p.slug}/${round}`, phase }),
    () => agent(`slug=${p.slug} round=${round} domain=${p.domain || 'infer it from DESCRIPTION.md'}. Verify this round (HANDOFF: studio/${p.slug}/rounds/${round}/HANDOFF.md).`,
      { agentType: 'studio-science-critic', label: `sci:${p.slug}/${round}`, phase }),
  ])
}

function lead(p, rounds, nextRound, phase) {
  const many = rounds.length > 1 ? ' They are parallel theses: rank them, then pick one parent or write a MERGE instruction.' : ''
  return agent(`slug=${p.slug}. Rounds just critiqued: ${rounds.join(', ')}.${many} Update LEDGER.md, write SYNTH.md in the latest critiqued round, and return your routing. The next free round is ${nextRound}.${p.note ? ` Curator note for this plate (enforce it in routing and the gate): ${p.note}` : ''}`,
    { agentType: 'studio-lead', schema: LEAD, label: `lead:${p.slug}`, phase })
}

async function runPlate(p) {
  let n = p.next_round || 1
  const theses = p.theses && p.theses.length ? p.theses : ['iterate']
  const first = theses.map((t) => ({ t, round: rr(n++) }))

  const built = (await pipeline(
    first,
    (c) => agent(designerPrompt(p, c.round, c.t, p.parent), { agentType: 'studio-designer', label: `design:${p.slug}/${c.round}:${c.t}`, phase: 'Design' })
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
    const round = rr(n++)
    const rep = await agent(designerPrompt(p, round, 'iterate', verdict.next_parent, verdict.instruction),
      { agentType: 'studio-designer', label: `design:${p.slug}/${round}`, phase: 'Iterate' })
    if (!rep) break
    await critique(p, round, 'Iterate')
    rounds.push(round)
    verdict = await lead(p, [round], rr(n), 'Iterate')
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
const results = await parallel(PLATES.map((p) => () => runPlate(p)))
return results.filter(Boolean)
