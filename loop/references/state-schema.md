# State Schema

Loop's persistent memory lives in two places inside each project folder:
`LOOP_STATE.md` (the cockpit) and `wiki/` (durable knowledge). This file defines
both, field by field. Read it when initializing a project or restructuring its
state.

---

## `LOOP_STATE.md` — the cockpit

A single, lean dashboard. It must always reflect reality because the next session
trusts it without re-deriving anything. When a section grows long, graduate the
detail into `wiki/` and keep the cockpit short.

```markdown
# LOOP STATE — <Project Name>

**Mission:** <one line: what this project is and who it's for>
**Iteration:** <N>
**Current phase:** PLAN | BUILD | TEST | REFLECT | IMPROVE
**Updated:** <YYYY-MM-DD>

## Active goal (this iteration)
<the one thing we're shipping this loop>

## Success criteria
<how TEST will judge pass/fail — concrete and checkable>

## Status
<pass/fail of the most recent TEST, current blockers, what's in flight>

## Open loops
- [ ] <next-up item — these become future iteration goals>
- [ ] <...>

## Last reflection
<1-2 line gist of the most recent REFLECT; full entry lives in wiki/learnings.md>

## Links
- Wiki index: ./wiki/index.md
- <PRD, repo, design, deploy — whatever matters>
```

**Field notes:**
- **Iteration** — integer, incremented in IMPROVE when a loop closes.
- **Current phase** — exactly one of the five. If unknown, it's PLAN.
- **Active goal** — singular. Multiple goals belong in Open loops.
- **Success criteria** — written in PLAN, read in TEST. The contract of the
  iteration.
- **Open loops** — the backlog. Keep it pruned; graduate or kill stale items.
- **Last reflection** — pointer + gist; the archive is `wiki/learnings.md`.

---

## `wiki/` — durable knowledge

One concern per file. Append-only where noted, so history is preserved.

### `index.md` — read first
A short map of the wiki: what each file holds and any project-specific pages
added over time. Update it whenever you add a page.

### `overview.md`
Mission, scope (in/out), stakeholders, key external links (repo, PRD, deploy,
designs). The "what and why" of the whole project. Relatively stable.

### `decisions.md` — append-only
Dated decision log. Every entry: **what** was decided + **why**. The why is the
asset. Example:

```markdown
## 2026-06-12 — Use Supabase for ParryAI auth + storage
**Why:** fastest path to a managed Postgres + auth with row-level security;
avoids standing up our own. Revisit if multi-region latency becomes an issue.
```

### `architecture.md`
How the project is built or how it works: components, data flow, integrations,
key constraints. Updated when the structure changes (often pointed to from a
decision).

### `learnings.md` — append-only
One entry per iteration's REFLECT. Dated, tagged to the iteration. What worked,
what surprised us, what to change, what's de-risked. This is the compounding
core of the loop.

```markdown
## Iteration 3 — 2026-06-12
- **Worked:** thin vertical slice (signup→verify→login) closed in one session.
- **Surprised:** mobile Safari cookie handling differed from desktop.
- **Change next time:** add a mobile check to the TEST criteria by default.
- **De-risked:** auth flow proven end to end.
```

### `glossary.md`
Project-specific terms, acronyms, and named concepts so a fresh session (or a
collaborator) ramps instantly.

---

## Keep the index honest; backfill lazily

The six core wiki files are the floor, but a project may not have meaningful
content for all of them yet (e.g. no real `architecture.md` on day one). Don't
manufacture filler to fill a heading, and don't let `index.md` list pages that
don't exist — an index that lies is worse than a short one. Create or flesh out
a standard page when there's actually something to record, not before. If you
inherit an `index.md` that references missing pages, fix the index rather than
backfilling empty stubs.

## Adding project-specific pages

Projects accrue their own knowledge areas (e.g. `wiki/prompt-injection-vectors.md`
for ParryAI, `wiki/persona-models.md` for Saibyl). Add files freely; just record
them in `index.md` so they're discoverable. The six core files above are the
floor, not the ceiling.

---

## Adopting an existing wiki

If a project already keeps `.md` persistent state (e.g. the Saido Agent wiki
pattern), do **not** create a parallel structure. Point `LOOP_STATE.md`'s links
at the existing directory and map the existing files onto the roles above
(overview / decisions / architecture / learnings / glossary). Add only what's
missing.
