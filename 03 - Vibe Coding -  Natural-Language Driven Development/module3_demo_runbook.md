# Module 3 Demo Runbook — Vibe Coding with Ownership

This runbook gives a reproducible guided demo. It is written for Copilot in VS Code, but the prompts also work with Claude Code, Codex, or similar tools.

## Demo purpose

Show the full lifecycle:

1. start from product intent;
2. allow a broader first-draft proposal;
3. contain the implementation;
4. generate a working slice;
5. inspect and verify;
6. take ownership;
7. connect the slice to the Module 2 API.

The demo should not look like magic. It should visibly show the developer making decisions.

## Setup

Open:

```text
task_tracker_frontend_starter/
```

Run:

```bash
npm install
npm test
npm run serve
```

Expected starting state:

- the starter contains only the product brief, minimal browser shell, sample data, and a sanity test;
- `npm test` passes the starter sanity check;
- the browser shows only a placeholder shell;
- there is no predefined application module structure to complete.

Optional:

Start the Module 2 API solution at `http://127.0.0.1:8000`.

## Demo timing

Core: 55–70 minutes.  
Expanded: 80–95 minutes.

## Step 1 — Start from product intent

Open `docs/design-brief.md`.

Prompt:

```text
Read docs/design-brief.md.
Propose two useful first-version experiences for this task tracker.
Focus on visible user flow, core behavior, and what should be deliberately omitted from the first draft.
Do not edit files yet.
```

Expected response:

- one smaller version focused on quick-add, render, filter, toggle, and local persistence;
- one broader version with search, priority editing, polish, detail panel, maybe API sync;
- a recommendation about which is safer for a classroom first version.

Instructor narration:

> Notice the difference from Module 2. I am not starting with `Implement normalizeTask in state.js`. I am starting from product intent. But I still told the tool not to edit files yet.

Likely AI overreach:

- proposes dark mode, drag-and-drop, charts, authentication, rich animations, or a package/framework.

Instructor response:

```text
Good, but narrow it. Choose the smaller version. Exclude dark mode, drag-and-drop, charts, authentication, and new dependencies.
```

## Step 2 — Contain the plan

Prompt:

```text
Choose the smaller direction.
Before editing, propose the smallest vertical slice.
Include:
- files to touch
- files to avoid
- responsibility of each file
- stop conditions
- tests to run
- manual browser checks
Do not edit files yet.
```

Expected plan:

The agent should propose a **small architecture of its own**, rather than discovering a pre-created set of TODO files. A reasonable answer might separate:

- pure task/state logic;
- persistence;
- DOM rendering;
- event/bootstrap wiring;
- automated tests for pure logic;
- manual browser checks for UI behavior.

Do not require specific filenames. If the agent proposes a simpler structure that keeps responsibilities understandable and the diff reviewable, accept it.

Reject if the AI suggests:

- replacing the whole app with a framework;
- changing the lab scope;
- putting all logic into one file;
- using `innerHTML` for user-entered task titles;
- adding dependencies.

## Step 3 — Implement the first slice

Prompt:

```text
Implement only the agreed first slice using the file/responsibility plan we just approved.
Constraints:
- no build tools
- no new runtime dependencies
- create only the files needed for the approved slice
- do not copy or assume a reference-solution architecture
- do not use unsafe innerHTML for task titles
- add automated tests where they add clear value, especially for pure logic
- use manual browser checks for DOM behavior
Stop after render, quick-add, one status filter, completion toggle, local persistence, and empty state.
After editing, summarize changed files and tell me exactly what to verify.
```

Expected file changes:

- only the small set of application/test files approved in Step 2 are created or changed;
- `package.json` should not gain runtime dependencies;
- the exact filenames may vary because choosing the first-draft structure is part of the exercise.

Verification:

```bash
npm test
npm run serve
```

Manual checks:

- page loads;
- seeded tasks render;
- quick-add works;
- empty title is rejected or ignored with feedback;
- filter works;
- toggling done changes status;
- refresh preserves local tasks;
- no task title is rendered as HTML.

Instructor narration while AI works:

> This is the dangerous moment in vibe coding: the tool may generate a lot. I am not evaluating the answer by how fast it appears or how polished the UI looks. I am watching scope, file boundaries, dependencies, and verification.

## Step 4 — Review the first draft

Prompt:

```text
Review your generated implementation for handoff risk.
Identify:
- confusing file responsibilities
- unsafe DOM behavior
- missing edge cases
- weak tests
- accessibility issues
- places where visual polish hides maintainability problems
Do not edit yet.
```

Expected findings will vary with the generated first draft. Typical examples include:

- missing localStorage corruption handling;
- too much logic in one file;
- weak or missing automated tests;
- incomplete accessibility/focus handling;
- unsafe DOM rendering;
- hidden assumptions about task IDs or status values.

Do not force the draft to match the reference solution just to make these findings appear.

If AI says everything is production-ready, challenge it:

```text
Be more critical. Treat this as a first AI-generated draft that must be owned by a human developer.
What would a skeptical reviewer object to?
```

## Step 5 — Ownership cleanup

Prompt:

```text
Implement one maintainability/safety cleanup only.
Choose the highest-value cleanup from your review.
Keep the diff small and explain why this change improves ownership.
```

Good choices:

- safe DOM node creation;
- localStorage parse fallback;
- service boundary cleanup;
- stronger tests.

## Step 6 — Minimal Module 2 API integration

Prompt:

```text
Plan the smallest safe integration with the Module 2 Work Items API at http://127.0.0.1:8000.
Scope:
- list work items
- create work item
- toggle todo/done status
- update priority
- show useful error when API is unavailable
- keep localStorage as fallback mode
No authentication, no deployment, no multi-user sync.
Do not edit files yet.
```

After plan review:

```text
Implement the API integration according to the approved plan.
Keep local mode available.
Add tests for API client mapping and error handling.
Summarize manual checks.
```

Verification:

```bash
npm test
```

Manual API checks:

1. Start Module 2 API.
2. Connect frontend to `http://127.0.0.1:8000`.
3. Add task.
4. Toggle completion.
5. Update priority.
6. Refresh.
7. Stop API and confirm useful error behavior.

## Step 7 — Debrief

Ask students:

1. Where did the AI help most?
2. Where did the AI overreach?
3. Which artifact gave us confidence: UI appearance, tests, or diff review?
4. What did we own by the end that we did not own after the first draft?
5. How did Module 2 habits become more important here?

## Prepared fallback path

If live AI fails:

1. Show `task_tracker_frontend_solution/`.
2. Open `review_exercises/flawed_generated_draft/`.
3. Ask students to identify flaws.
4. Compare with the solution architecture.
5. Continue with API integration discussion.

## Expected AI deviations and recovery

| Deviation | Instructor recovery |
|---|---|
| Adds framework/dependencies | Ask for no-dependency rewrite and explain review burden. |
| Uses unsafe `innerHTML` | Turn into teachable security/ownership moment. |
| Creates monolithic `app.js` | Ask for file responsibility map and split only the highest-value seam. |
| Skips tests | Ask for pure-function tests and manual browser checklist. |
| Overbuilds UI polish | Mark as optional and return to core behavior. |
| Claims production readiness | Challenge assumptions and ask for handoff risks. |
