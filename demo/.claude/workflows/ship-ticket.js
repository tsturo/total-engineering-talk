export const meta = {
  name: 'ship-ticket',
  description: 'Split a ticket into pieces, build them in parallel, test, review from three angles, hand back to the engineer',
  phases: [
    { title: 'Plan', detail: 'orchestrator reads the ticket and splits it' },
    { title: 'Build', detail: 'one builder per piece, in parallel' },
    { title: 'Test', detail: 'one tester per piece' },
    { title: 'Review', detail: 'code, security and product reviewers per piece' },
    { title: 'Ship', detail: 'full test run and a summary for the engineer' },
  ],
}

const ticket = args?.ticket || 'tickets/ENG-142.md'

const PLAN = {
  type: 'object',
  properties: {
    pieces: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          key: { type: 'string' },
          title: { type: 'string' },
          files: { type: 'array', items: { type: 'string' } },
          spec: { type: 'string' },
        },
        required: ['key', 'title', 'files', 'spec'],
      },
    },
  },
  required: ['pieces'],
}

const VERDICT = {
  type: 'object',
  properties: {
    ok: { type: 'boolean' },
    feedback: { type: 'string' },
  },
  required: ['ok', 'feedback'],
}

const LENSES = [
  { key: 'code', prompt: 'You review code quality: naming, structure, duplication, error handling.' },
  { key: 'security', prompt: 'You think like an attacker: injection, path traversal, unvalidated input, unsafe headers.' },
  { key: 'product', prompt: 'You think like the user: does it do what the ticket says, is the behaviour obvious, are edge cases handled.' },
]

phase('Plan')
const plan = await agent(
  `Read ${ticket}. Split it into at most 3 pieces that can be built at the same time by different people without touching the same files. Each piece gets its own files under src/, public/ or test/. Do not build anything.`,
  { label: 'orchestrator', schema: PLAN },
)
log(`${plan.pieces.length} pieces: ${plan.pieces.map(p => p.key).join(', ')}`)

const build = (piece, feedback = '') => agent(
  `Implement piece ${piece.key} "${piece.title}" of ${ticket}.\nSpec: ${piece.spec}\nOnly touch these files: ${piece.files.join(', ')}. Existing code is in src/. Add tests for your piece under test/.${feedback ? `\nA reviewer rejected the previous attempt: ${feedback}\nFix that.` : ''}`,
  { label: `build:${piece.key}`, phase: 'Build' },
)

const test = piece => agent(
  `Run npm test in this project. If tests for piece ${piece.key} "${piece.title}" fail, fix the piece (files: ${piece.files.join(', ')}) until they pass. Return what you ran and the result.`,
  { label: `test:${piece.key}`, phase: 'Test' },
)

const review = piece => parallel(LENSES.map(lens => () => agent(
  `${lens.prompt}\nReview piece ${piece.key} "${piece.title}" (files: ${piece.files.join(', ')}) against ${ticket}. Set ok=false only for a real problem, and say exactly what to change.`,
  { label: `review:${lens.key}:${piece.key}`, phase: 'Review', schema: VERDICT },
)))

const results = await pipeline(
  plan.pieces,
  piece => build(piece),
  (_, piece) => test(piece),
  (_, piece) => review(piece),
  async (verdicts, piece) => {
    const blockers = verdicts.filter(Boolean).filter(v => !v.ok)
    if (!blockers.length) return { piece: piece.key, rebuilt: false }
    log(`${piece.key}: pushed back (${blockers.length} reviewer${blockers.length > 1 ? 's' : ''})`)
    await build(piece, blockers.map(b => b.feedback).join('\n'))
    await test(piece)
    const again = await review(piece)
    return { piece: piece.key, rebuilt: true, ok: again.filter(Boolean).every(v => v.ok) }
  },
)

phase('Ship')
const summary = await agent(
  `Run npm test for the whole project. Then write a short summary for the engineer who owns ${ticket}: what was built per piece, which files changed, what the reviewers pushed back on, and what they should check by hand before merging. Do not commit.`,
  { label: 'ship' },
)

return { pieces: results.filter(Boolean), summary }
