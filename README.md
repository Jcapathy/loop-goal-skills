# loop-goal-skills

Two companion [Agent Skills](https://agentskills.io) from **Saido Labs** that turn Claude
into a disciplined, self-driving build partner: **`loop`** gives every project a
repeatable Plan → Build → Test → Reflect → Improve cadence backed by a persistent
`.md` wiki, and **`goal`** lets you declare a measurable outcome and have Claude run
that cadence until the outcome is verifiably met.

They work in **Claude Code** (CLI) and **Cowork**, and follow the open Agent Skills
standard so they port to any tool that supports it.

---

## What's inside

```
loop-goal-skills/
├── loop/                       # the /loop skill
│   ├── SKILL.md                # cadence, phases, operating principles
│   ├── references/
│   │   ├── phase-playbooks.md   # per-phase checklists, anti-patterns, hand-offs
│   │   └── state-schema.md      # field-by-field spec for LOOP_STATE.md + wiki/
│   ├── assets/
│   │   ├── LOOP_STATE.template.md
│   │   └── wiki/                # starter wiki (index, overview, decisions, …)
│   └── scripts/
│       └── loop_init.py         # scaffolds state files into a project folder
├── goal/                       # the /goal skill
│   └── SKILL.md                # objective-mode entry point that drives the loop
├── loop_goal_skills/           # pip package: `loop-skills` + `loop-init` CLIs
├── pyproject.toml              # packaging (pip install from GitHub)
├── claude-settings.json        # optional pre-approved tool permissions (Claude Code)
├── LICENSE                     # MIT
└── README.md
```

---

## The skills

### `/loop` — the project meta-skill
A reusable operating cadence for any project or build pipeline. Every unit of work
moves through five phases — **Plan → Build → Test → Reflect → Improve** — and each
pass writes both working output *and* a short reflection, so the next pass starts
smarter and nothing is lost between sessions. State lives in two places per project:

- `LOOP_STATE.md` — the cockpit: current iteration, phase, the one active goal, open
  loops, last reflection.
- `wiki/` — durable knowledge: decisions, architecture, learnings, glossary.

`loop` is a *meta-skill*: it sequences the work and hands off to specialist skills
(docs, slides, engineering, etc.) rather than replacing them.

### `/goal` — define the outcome, let the loop close it
The objective-mode entry point. You state one or more **measurable outcomes**, and
Claude runs the loop toward them — logging every run, looping back on failure, and
stopping only when each target is verifiably met (or a guardrail trips). The whole
thing hinges on one rule: **every outcome needs a definition of done that TEST can
check with evidence.**

```
/goal
1) ParryAI injection classifier ≥95% recall on the held-out injection eval
   — done when recall ≥ 0.95 and precision within 2pp of baseline
2) Document the final infra + architecture in wiki/architecture.md  — after #1
mode: auto
stop: #1 verified twice on held-out data, then do #2; if 6 iterations gain <0.5pp recall, pause and report
```

Built-in integrity guardrails: no "pass" without citing the real number, verify on
held-out data, watch the metric you could regress, and pause on a plateau or a genuine
blocker instead of spinning.

---

## Install

### pip (installer CLI) — recommended

Install straight from GitHub, then run the bundled installer to copy both skills
into your Claude skills directory:

```bash
pip install git+https://github.com/Jcapathy/loop-goal-skills.git

loop-skills install             # → ~/.claude/skills/   (loop + goal, all projects)
loop-skills install --project   # → ./.claude/skills/   (current repo only)
```

Start a new Claude Code session and invoke with `/loop` or `/goal` (they also
auto-trigger when your wording matches their description).

The package also installs **`loop-init`**, which scaffolds a project's persistent
state from the bundled templates:

```bash
loop-init ./ParryAI --name ParryAI --mission "Prompt-injection armor for LLM apps"
# creates ParryAI/LOOP_STATE.md and ParryAI/wiki/
```

### Manual (copy the folders)
No pip? Copy each skill folder into your skills directory — user-level (all projects)
or project-level (one repo):

```bash
# user-level (available everywhere)
cp -r loop ~/.claude/skills/loop
cp -r goal ~/.claude/skills/goal

# or project-level
mkdir -p .claude/skills && cp -r loop goal .claude/skills/
```

Start a new session; the skills are auto-discovered. Invoke with `/loop` or `/goal`
(they also auto-trigger when your wording matches their description).

### Cowork
Each skill folder can be zipped to a `.skill` package and installed with the **Save
skill** button, or added via **Settings → Capabilities**. Invoke with `/loop` / `/goal`.

---

## Pre-approved tools & autonomy (Claude Code)

Both `SKILL.md` files declare an `allowed-tools` line so Claude can use Bash, Read,
Write, Edit, Glob, Grep, and friends **without a permission prompt while the skill is
active**. For persistent, always-on pre-approval, merge `claude-settings.json` into
your `~/.claude/settings.json` (or a project `.claude/settings.json`). It fully allows
the file/search/web tools and **scopes Bash** to a common dev stack (python, pip,
pytest, node, npm, git), with a `deny` block for destructive commands and secret files.

> ⚠️ Merge the `permissions` block into an existing `settings.json` — don't overwrite
> the whole file. Bash command-scoping enforcement has known edge cases in Claude Code;
> for fully hands-off runs, launch with `--permission-mode acceptEdits` (or, in a
> contained repo, `--dangerously-skip-permissions`).

Autonomous within a run, persistent across runs: the `LOOP_STATE.md` + `wiki/` files
let a new session pick up the same objective and run ledger exactly where the last one
left off.

---

## Changelog

Version history is tracked in [CHANGELOG.md](CHANGELOG.md), following
[Keep a Changelog](https://keepachangelog.com) and [SemVer](https://semver.org).
Latest: **v0.1.0**.

---

## License

Released under the [MIT License](LICENSE) — © 2026 Saido Labs LLC. Free to use, modify,
and redistribute with attribution.
