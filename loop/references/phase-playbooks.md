# Phase Playbooks

Depth for each of the five Loop phases. The SKILL.md gives the one-line version;
this is the field manual. Read the section for whichever phase you're entering.

---

## 1. PLAN

**Entry question:** What is the smallest valuable thing to ship next, and how
will we know it worked?

**Do:**
- Write exactly **one** iteration goal. If you have three, the other two are the
  next iterations — park them in open loops.
- Define **success criteria** concretely enough that TEST can judge pass/fail
  without re-asking the user. "Login works" is weak; "a new user can sign up,
  receive a verification email, and log in on mobile Safari" is testable.
- Note the **approach** in a sentence or two and the **top risk**.
- Size it down until you believe you can close the loop in one to a few sessions.

**Hand off to:**
- `project-management-skill` — for PRDs, MoSCoW prioritization, or multi-feature
  scoping. Link the output in `wiki/overview.md`.
- `engineering:architecture` / `engineering:system-design` — when the plan
  hinges on a design decision (record the ADR in `wiki/decisions.md`).

**Anti-patterns:**
- Planning five iterations deep. Plan one, sketch the rest.
- Vague success criteria — they make TEST meaningless and REFLECT hollow.

**Exit artifact:** `LOOP_STATE.md` "Active goal" + "Success criteria" updated.

---

## 2. BUILD

**Entry question:** What's the smallest version of the thing that satisfies the
goal?

**Do:**
- Build the thinnest slice that meets the success criteria. Resist gold-plating;
  extra polish is a future iteration if it earns one.
- Use the right specialist skill for the artifact rather than hand-rolling:
  - documents → `docx`; slide decks → `pptx`; spreadsheets/models → `xlsx`;
    PDFs → `pdf`; landing pages / UI → `frontend-design`.
  - code review / debugging → `engineering:*`; MCP servers → `mcp-builder`.
- Capture decisions **as you make them** in `wiki/decisions.md`: one line for
  what, one line for why. The "why" is the part that pays off later.

**Anti-patterns:**
- Building far past the goal "while I'm in here." That's an unplanned iteration
  with no success criteria.
- Making architectural decisions silently. Undocumented choices become
  next-quarter's mysteries.

**Exit artifact:** working output + any new entries in `wiki/decisions.md`.

---

## 3. TEST

**Entry question:** Does it actually meet the success criteria from PLAN?

**Do:**
- Check against the **written** criteria, not your gut. Re-open the PLAN block.
- Actually exercise it: run the tests, open the file, click the flow, read the
  generated doc. For anything visual, view it. For code, run it.
- Record the result in `LOOP_STATE.md`: pass, or fail + what broke.
- A failure is the loop succeeding — it caught something before the user did.
  Log the defect and loop back to BUILD (or PLAN if the goal was wrong).

**Hand off to:**
- `engineering:testing-strategy` — to design what "tested" should mean.
- `engineering:code-review` — security/correctness/perf review of a change.
- `engineering:debug` — structured diagnosis when something breaks.

**Anti-patterns:**
- "Looks right to me" with no execution.
- Moving the goalposts to make a failing build pass. Change the criteria in PLAN
  deliberately if they were wrong; don't quietly lower the bar.

**Exit artifact:** pass/fail + defects recorded in `LOOP_STATE.md`.

---

## 4. REFLECT

**Entry question:** What did this iteration teach us?

This is the highest-leverage, most-skipped phase. It is what turns a sequence of
builds into a compounding advantage.

**Do:**
- Write a short, honest entry in `wiki/learnings.md`, dated and tagged to the
  iteration. Cover: what worked, what surprised us, what to change, what is now
  de-risked or proven.
- Update the "Last reflection" block in `LOOP_STATE.md` with the 1-2 line gist.
- Be honest about misses. A reflection that only lists wins teaches nothing.

**Anti-patterns:**
- Skipping it because "the build worked." Especially then — capture *why* it
  worked so it's repeatable.
- Letting it sprawl into an essay. Two sharp sentences beat two pages.

**Exit artifact:** new `wiki/learnings.md` entry + `LOOP_STATE.md` reflection block.

---

## 5. IMPROVE

**Entry question:** Given what we learned, what's the next goal — and should the
process itself change?

**Do:**
- Convert the reflection into the **next iteration's goal** (this becomes the
  next PLAN).
- When a learning is reusable, improve the *process*: add a wiki page, a
  checklist, a template, or a project-specific tweak to the loop. This is how the
  pipeline gets sharper over time instead of repeating mistakes.
- Close the iteration in `LOOP_STATE.md`: increment the iteration counter, move
  completed open-loops into the wiki, set the new active goal, reset phase to
  PLAN.

**Anti-patterns:**
- Treating IMPROVE as just "pick the next task." The process-improvement half is
  what separates Loop from a to-do list.
- Carrying a bloated open-loops list. Graduate or kill stale items.

**Exit artifact:** iteration closed, next goal set, `LOOP_STATE.md` reset to PLAN.

---

## Collapsing phases for speed

When the user wants to move fast on something small, run all five phases in a
single quick pass: state the goal, build it, eyeball-test it, log a one-line
reflection, set the next goal. The discipline is preserved (goal + reflection
still get written) without the ceremony slowing anyone down. The cadence serves
the work — never the reverse.
