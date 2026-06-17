# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-06-16

First public release.

### Added
- **`/loop` skill** — a Plan → Build → Test → Reflect → Improve project cadence
  backed by persistent `.md` state (`LOOP_STATE.md` + a `wiki/` of decisions,
  architecture, learnings, and glossary).
- **`/goal` skill** — objective mode: declare one or more measurable outcomes and
  run the loop until each is verifiably met, with integrity guardrails.
- **pip packaging** (`pyproject.toml`, Hatchling) so the repo installs from GitHub.
- **`loop-skills install`** CLI — copies both skills into `~/.claude/skills/`
  (or `./.claude/skills/` with `--project`).
- **`loop-init`** CLI — scaffolds `LOOP_STATE.md` + `wiki/` into a project folder.
- **`allowed-tools`** frontmatter on both skills for prompt-free tool use while active.
- **`claude-settings.json`** — pre-approved Claude Code tool permissions (scoped
  Bash allow-list plus deny rules for destructive commands and secret files).
- MIT license, README, and `.gitignore`.

[Unreleased]: https://github.com/Jcapathy/loop-goal-skills/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Jcapathy/loop-goal-skills/releases/tag/v0.1.0
