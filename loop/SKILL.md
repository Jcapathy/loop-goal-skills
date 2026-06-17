---
name: loop
description: >-
  A project operating system that runs every piece of work through a disciplined
  Plan, Build, Test, Reflect, Improve cycle, backed by a persistent .md wiki so
  context survives across sessions. Use this skill whenever the user is
  starting, resuming, or shipping work on any project or build pipeline —
  including phrases like "let us work on this project", "start the loop", "run
  the loop", "resume the project", "what is next", "kick off a build", "ship
  this feature", "plan this", or "review where we are", or whenever a project
  has or should have a LOOP_STATE.md and wiki directory. Also trigger when the
  user wants a consistent build process across multiple ventures or persistent
  project memory. Prefer this skill over ad-hoc work for anything that spans
  more than one session. This is about the project-work cadence — it does NOT
  apply to programming loops (for, while, or event loops), audio or animation
  loops, or "keep me in the loop" status updates.
allowed-tools: Bash Read Write Edit MultiEdit Glob Grep LS WebSearch WebFetch Task TodoWrite NotebookEdit
---

# Loop — the project meta-skill

Loop is a reusable operating cadence for any project or build pipeline. Every
unit of work moves through five phases:

```
        ┌──────────────────────────────────────────────────┐
        ▼                                                    │
   1. PLAN ──► 2. BUILD ──► 3. TEST ──► 4. REFLECT ──► 5. IMPROVE
        │                                                    │
        └────────────── feeds the next iteration ◄───────────┘
```

The point is not bureaucracy. It is **leverage**: each pass produces working
output *and* a written reflection, so the next pass starts smarter and nothing
gets lost between sessions. The persistent state files are what make a session
that ends today pick up cleanly next week.

This skill is a *meta-skill*: it orchestrates the cadence and decides when to
hand off to other skills (docx, pptx, xlsx, engineering, project-management,
skill-creator, etc.). It does not replace them — it sequences them.

---

## First move every session: read state, then orient

Before doing anything else, find and read the project's state. Loop keeps state
in two places inside the project folder:

- `LOOP_STATE.md` — the live control file: current iteration, phase, the one
  active goal, open loops, and the last reflection. This is the cockpit.
- `wiki/` — durable knowledge: decisions, architecture, learnings, glossary,
  one file per project area. This is long-term memory.

Decision tree:

1. **State exists** → read `LOOP_STATE.md` fully, skim the `wiki/` index, then
   tell the user where things stand in 2-3 sentences and propose the next phase.
2. **No state, real project folder** → offer to initialize. Run
   `scripts/loop_init.py <project-dir>` (or create the files by hand from
   `assets/`). Confirm the project name and one-line mission first.
3. **No project folder yet** → you can still run the loop in conversation, but
   say so, and offer to create a folder so progress persists.

Never start building before you know what iteration you are on and what the
single active goal is. If the user jumps straight to "build X", that is fine —
log it as the goal, then proceed; don't make them wait.

**Trust the state, but verify it against reality.** The cockpit can drift from
what's actually on disk — a Status line may say a feature is "drafted" when no
such file exists, or the wiki index may list pages that were never created.
Before acting on a claim, glance at the actual files. When state and reality
disagree, reality wins: do the work the state assumed was done, then correct the
state in the same turn so the next session isn't misled. This reconciliation is
itself part of the loop, not a detour.

---

## The five phases

Each phase has an entry question, a job, and an exit artifact. Detailed
playbooks (checklists, anti-patterns, hand-off targets) live in
`references/phase-playbooks.md` — read it when you need depth on a phase.

### 1. PLAN — *"What is the smallest valuable thing to ship next, and how will we know it worked?"*
Define one iteration goal, the success criteria (how TEST will judge it), the
approach, and the risks. Keep iterations small — a loop you can close in one or
a few sessions beats a grand plan that never closes. Write the goal and criteria
into `LOOP_STATE.md`. For substantial features, hand off to the
`project-management-skill` (PRD/MoSCoW) and link the output in the wiki.

### 2. BUILD — *"Make the thing, the smallest version that satisfies the goal."*
Execute. Write code, draft the document, create the asset. Prefer the right
specialist skill for the artifact. Capture any decision worth remembering
(why this library, why this structure) into `wiki/decisions.md` *as you make it*,
not later — that is the habit that compounds.

### 3. TEST — *"Does it actually meet the success criteria from PLAN?"*
Verify against the criteria you wrote down, not vibes. Run the tests, check the
output, view the file, click through the flow. For code, hand off to
`engineering:testing-strategy` or `engineering:code-review`. Record pass/fail and
any defects in `LOOP_STATE.md`. If it fails, that is not a detour — it is the
loop working. Capture what broke and loop back to BUILD or PLAN.

### 4. REFLECT — *"What did this iteration teach us?"*
The phase people skip and the one that creates the compounding advantage. Write
a short, honest reflection: what worked, what surprised us, what to do
differently, what is now de-risked. Append it to `wiki/learnings.md` and update
the "Last reflection" block in `LOOP_STATE.md`. Two sentences beats nothing;
don't let it balloon.

### 5. IMPROVE — *"Given what we learned, what's the next goal — and should the process itself change?"*
Translate the reflection into the next iteration's goal (back to PLAN) and, when
warranted, into a change to how you work — a new wiki page, a checklist, a
template, even an edit to this loop for that project. Close the iteration:
increment the counter, move completed items to `wiki/`, set the next goal.

---

## Persistent state — the .md wiki

This is what makes Loop survive across sessions and scale across your ventures.
The full schema and starter content are in `references/state-schema.md`; the
drop-in templates are in `assets/`. The essentials:

```
<project>/
├── LOOP_STATE.md          # cockpit: iteration, phase, active goal, open loops
└── wiki/
    ├── index.md           # map of the wiki — read first
    ├── overview.md        # mission, scope, stakeholders, links
    ├── decisions.md       # dated decision log (what + why)
    ├── architecture.md    # how it's built / how it works
    ├── learnings.md       # reflections, one entry per iteration
    └── glossary.md        # project-specific terms
```

Rules that keep state trustworthy:

- **Update state in the same turn you do the work**, never "at the end." The
  cockpit must always reflect reality, because the next session trusts it blindly.
- **`LOOP_STATE.md` stays lean.** It is a dashboard, not an archive. When the
  open-loops or reflection sections get long, graduate detail into the `wiki/`.
- **Every decision gets a one-line "why."** Future-you (and future sessions)
  will thank present-you. A decision log without reasons is just a list of regrets.
- **Append, don't overwrite, in `learnings.md` and `decisions.md`** — the history
  is the asset.

---

## Applying Loop across multiple projects

Loop is designed to run identically across a portfolio (ParryAI, Saibyl,
Feastrio, Saido Agent, and so on). Each project gets its own `LOOP_STATE.md` and
`wiki/`; the cadence is shared, the state is per-project. To stand up a new
project, run `loop_init.py` against its folder and fill in the overview. To get a
cross-portfolio read, read each project's `LOOP_STATE.md` cockpit and summarize
the active goal + phase for each — that is your build-pipeline status board in
under a minute.

If a project already uses a `.md`-based persistent state (e.g. the Saido Agent
wiki pattern), point Loop at that directory instead of creating a parallel one —
adopt the existing files, don't duplicate them.

---

## Operating principles

- **Always be in a known phase.** If you're unsure, you're in PLAN. Say which
  phase you're entering before you act.
- **Small loops win.** Optimize for closing an iteration, not for the size of the
  plan. Momentum and a clean paper trail beat ambition.
- **Reflection is non-negotiable.** A build without a reflection is half a loop.
- **The loop serves the work, not the reverse.** If the user wants to move fast,
  collapse phases into a single quick pass — but still log the goal and a one-line
  reflection. Never let the ceremony slow down a founder who wants to ship.
  *Heuristic:* collapse when the work is small, easily reversible, or trivially
  correct; run the full, deliberate loop when the slice is novel, risky, hard to
  undo, or the riskiest unknown in the project. "Get us going" on a brand-new
  core usually deserves the full loop — that first slice is where the risk lives.
- **Hand off, don't reinvent.** Use specialist skills for artifacts; Loop's job
  is sequencing and memory.

---

## Reference files

- `references/phase-playbooks.md` — detailed per-phase checklists, anti-patterns,
  and which skill to hand off to. Read when you need depth on a phase.
- `references/state-schema.md` — full structure and field-by-field meaning of
  `LOOP_STATE.md` and the wiki. Read when initializing or restructuring state.
- `assets/LOOP_STATE.template.md` and `assets/wiki/` — starter files copied into
  a project at init.
- `scripts/loop_init.py` — scaffolds state files into a project folder.
