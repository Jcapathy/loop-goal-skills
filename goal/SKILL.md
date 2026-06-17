---
name: goal
description: >-
  Objective-mode entry point for the Loop operating cadence. Use when the user
  wants to define a desired OUTCOME — one or more measurable targets — and have
  Claude drive the Plan, Build, Test, Reflect, Improve cycle autonomously,
  logging each run, until every target is verifiably met. Triggers on /goal,
  "set a goal", "define the objective", "the outcome I want is", "run until it
  hits", "keep iterating until", "drive this to a number", "don't stop until",
  or any request that names an end-state plus a success threshold. Pairs with
  the loop skill: goal captures and sharpens the objective and its definition of
  done, then runs the loop toward it. Each outcome needs a concrete,
  evidence-checkable success criterion so TEST can judge pass or fail honestly.
  Not for vague exploration with no measurable target, and not for one-off
  single-step tasks that need no iteration.
allowed-tools: Bash Read Write Edit MultiEdit Glob Grep LS WebSearch WebFetch Task TodoWrite NotebookEdit
---

# /goal — define the outcome, let the Loop close it

`/goal` is the objective-mode entry point for the Loop skill. You state the
*outcome* you want — one or more measurable targets — and Claude runs the full
Plan → Build → Test → Reflect → Improve cycle toward it, logging every run,
looping back on failure, and stopping only when each target is verifiably met
(or a guardrail trips). `/loop` enters the cadence; `/goal` aims it.

The whole thing hinges on one rule: **every outcome must have a definition of
done that TEST can check with evidence.** A target Claude can measure is a target
Claude can close autonomously; a vague target just produces vague motion. So the
first job of `/goal` is to sharpen anything fuzzy into a concrete criterion.

---

## Inline grammar

**Quick form — a single outcome:**

```
/goal <outcome stated as a measurable end state>
```

e.g. `/goal ParryAI's injection classifier reaches >=95% recall on the held-out eval`

**Full form — one or more outcomes plus controls:**

```
/goal
1) <outcome> — done when <measurable, evidence-checkable result>
2) <outcome> — done when <result>            [after #1]
mode:  auto | checkpoint          # default: auto
stop:  <guardrail>                # default: all outcomes verified, OR 6 no-gain iterations -> pause
log:   iteration results -> wiki/learnings.md ; decisions -> wiki/decisions.md
```

List as many outcomes as you want. Use `[after #N]` or `then` to sequence them;
otherwise they are taken in order.

---

## The fields

- **Outcomes (1+).** Each is an end-state plus its definition of done — a metric
  and threshold, or a concrete observable. "≥95% recall on the held-out set,"
  not "better recall." If you give a fuzzy outcome, Claude proposes a measurable
  version and (in `checkpoint` mode) confirms it before building.
- **mode.** `auto` = run the cycle unattended, iteration after iteration, until
  done or a guardrail trips, pausing only for genuine blockers. `checkpoint` =
  pause for your go-ahead between iterations (or phases). Default `auto`.
- **stop.** The guardrails that end the run: success (all outcomes verified), a
  plateau cap (N iterations with no meaningful gain → pause and report options),
  a max-iteration or time/budget cap, and any hard blocker.
- **log.** Where each run's results land. Defaults map to your existing Loop
  state files (see below).

---

## What Claude does when you run /goal

1. **Capture & sharpen.** Parse the outcomes. Ensure each has an
   evidence-checkable done-criterion; sharpen and (in checkpoint mode) confirm
   any that are vague.
2. **Persist the objective.** Write an `## Objective` block into `LOOP_STATE.md`
   (outcomes, criteria, mode, stop rule) and add each outcome as an Open loop. If
   the project has no state yet, initialize it via the loop scaffolding first.
3. **Run the Loop** on the active outcome: Plan → Build → Test → Reflect →
   Improve, per the loop skill's playbooks.
4. **Log every run, in the same turn.** After each TEST, append an entry to
   `wiki/learnings.md` — iteration #, what changed, measured value vs. target,
   pass/fail, and where it was verified — and update **Status** plus the
   per-iteration **Active goal** in `LOOP_STATE.md`.
5. **Decide & advance.** Met → mark the outcome done, move to the next. Not met →
   REFLECT on why, IMPROVE the approach, loop back to PLAN/BUILD.
6. **Repeat** until all outcomes are verified or a guardrail trips.
7. **Close out.** Re-verify the headline metric (one passing run is not proof),
   write the run-ledger summary, and execute any "then document…" outcome — e.g.
   record the final infra + architecture in `wiki/architecture.md`.

---

## Integrity guardrails — so "done" means done

- **No pass without evidence.** Never report a target as met without running the
  real test/eval and citing the actual number.
- **Verify on held-out data, and watch the companions.** Hitting recall by
  tanking precision is not a win — name the metric you could regress and hold it.
- **Hit once ≠ achieved.** Confirm a passing result is stable (re-run / held-out)
  before declaring the outcome done.
- **Stop spinning.** On a plateau, pause and present options instead of burning
  iterations. Pause on any real blocker: missing data, ambiguous spec, external
  dependency, or an irreversible/destructive step.

---

## Worked example

```
/goal
1) ParryAI injection classifier >=95% recall on the held-out injection eval
   — done when recall >= 0.95 and precision within 2pp of baseline
2) Document the final infra + architecture in wiki/architecture.md
   — after #1 is verified
mode: auto
stop: #1 verified twice on held-out data, then complete #2; if 6 iterations
      gain <0.5pp recall, pause and report options
```

Claude logs the objective, then loops: tries an approach (BUILD), runs the eval
(TEST), records "iter 4 — added adversarial paraphrase set; recall 0.91→0.93,
precision 0.97; FAIL" to `learnings.md`, reflects, improves, and goes again —
until recall clears 0.95 on held-out data twice, then writes up the architecture
and reports done with the full ledger.

---

## Where results get logged (maps to your Loop state)

- **`LOOP_STATE.md` → `## Objective`** — the standing target(s) and stop rule
  (distinct from the per-iteration **Active goal**, which stays singular).
- **`LOOP_STATE.md` → Open loops** — one entry per outcome until met.
- **`LOOP_STATE.md` → Status** — latest TEST result + blockers.
- **`wiki/learnings.md`** — the append-only run ledger, one entry per iteration.
- **`wiki/decisions.md`** — any approach decision worth a "why."
- **`wiki/architecture.md`** — final infra/architecture when an outcome calls for it.

If you'd rather keep a tight metric table separate from reflections, say so and
the run ledger goes in its own `wiki/<objective>-runs.md` instead.

---

## Relationship to /loop

`/loop` is the cadence and the memory; `/goal` is the objective that drives them.
Use `/loop` to enter or resume a project and work phase by phase; use `/goal`
when you want to name an outcome and have the loop run itself until that outcome
is real. Everything `/goal` does is the loop cadence — it just adds the target,
the autonomy, and the run ledger on top.
