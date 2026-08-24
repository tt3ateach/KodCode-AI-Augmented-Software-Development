# Module 3 Hands-on Lab — Task Tracker Frontend and API Integration

## Goal

Use a vibe-coding workflow to generate a first frontend draft from a product brief, then take ownership of it and connect the core flow to the Module 2 Work Items API.

This is the key transition from Module 2:

- Module 2: disciplined AI assistance inside a conventional implementation workflow.
- Module 3: faster first draft from product intent, followed by containment, review, and ownership.

## Time budget

Core: 130 minutes  
Expanded: 175 minutes

## Phase 1 — Vibe-code the first version

### Objective

Use AI to produce a working first draft quickly, then immediately verify and inspect it.

### Core required scope

- render task cards;
- quick-add task;
- one status filter;
- toggle completion;
- local persistence;
- empty state;
- run `npm test`;
- perform manual browser verification.

### Optional stretch scope

Clearly optional. Use only if the cohort is moving quickly.

- free-text search;
- priority editing;
- multiple combined filters;
- responsive polish;
- keyboard/focus polish beyond basic form behavior;
- dark mode or detail panel.

### Constraints

- no build tooling;
- no new runtime dependencies;
- preserve the existing module structure;
- use tests for pure logic and API client behavior;
- use manual browser checks for DOM behavior;
- do not use unsafe `innerHTML` for user-provided task titles;
- stop after the agreed first slice.

### Suggested workflow

1. Read `docs/design-brief.md`.
2. Ask AI for two first-version experiences.
3. Choose the safer/smaller option.
4. Ask for a file-responsibility map.
5. Implement the first slice.
6. Run tests.
7. Open the app in the browser.
8. Inspect the diff.
9. Record one AI suggestion you rejected or revised.

### Example first prompt

```text
Read docs/design-brief.md.
Propose two useful first-version experiences for this task tracker.
Focus on visible user flow, core behavior, and what should be deliberately omitted from the first draft.
Do not edit files yet.
```

## Phase 2 — Beyond the AI: ownership and integration

### Objective

Move from “AI generated this” to “I understand, control, and can extend this.”

### Required ownership tasks

- explain file responsibilities;
- identify at least one AI-generated weakness;
- fix one maintainability or safety issue;
- improve one accessibility or UX issue;
- strengthen one test or verification checklist;
- connect the core flow to the Module 2 Work Items API.

### Required API integration scope

Assume the Module 2 API runs at:

```text
http://127.0.0.1:8000
```

Implement or verify:

- list work items;
- create work item;
- toggle status between `todo` and `done`;
- update priority;
- show a useful error message if the API is unavailable;
- keep local persistence available as fallback mode.

No authentication. No multi-user sync. No deployment.

### Good choices for Phase 2 cleanup

- replace unsafe DOM rendering with DOM node creation;
- split a monolithic render function;
- improve names around filters/state;
- handle corrupt localStorage safely;
- add missing API-client tests;
- improve keyboard/focus behavior;
- document the local/API service boundary.

## Deliverables

- working frontend;
- passing tests;
- browser verification checklist;
- prompt log;
- one rejected/revised AI suggestion;
- ownership reflection;
- working or clearly demonstrated Module 2 API integration.

## Definition of done

- Core local frontend flow works.
- API integration core flow works or is verified with tests and a running API.
- Student can explain the code structure.
- Student can identify one weakness in the first AI draft.
- Student has run tests and manual browser checks.
- Student has not treated visual polish as ownership.

# Suggested Solution Summary

A full reference solution is included in `task_tracker_frontend_solution/`.

Expected solution structure:

- `src/state.js` — pure task normalization, filtering, updating, status/priority translation.
- `src/localService.js` — localStorage-backed service with safe parsing and persistence.
- `src/apiClient.js` — small fetch-based client for the Module 2 API.
- `src/service.js` — service factory that selects local or API mode.
- `src/render.js` — safe DOM rendering using node creation, not unsafe task-title interpolation.
- `src/app.js` — event wiring and UI refresh.
- `tests/state.test.mjs` — pure logic tests.
- `tests/apiClient.test.mjs` — fetch/client mapping and error tests.

Expected verification:

```bash
cd task_tracker_frontend_solution
npm install
npm test
npm run serve
```

Optional API verification:

1. Start the Module 2 API at `http://127.0.0.1:8000`.
2. Open the frontend solution.
3. Enter `http://127.0.0.1:8000` in the API URL field and connect.
4. Add a task.
5. Toggle completion.
6. Change priority.
7. Refresh and verify that the API-backed state remains.

# Evaluation Rubric

| Criterion | Strong evidence |
|---|---|
| First draft workflow | Student used intent-led exploration, then narrowed implementation. |
| Containment | Student kept scope small and rejected broad or flashy suggestions. |
| Verification | Tests and browser checks were run and interpreted. |
| Ownership | Student can explain structure and identify risks. |
| API integration | Core local flow connects to the Module 2 API without adding unnecessary auth or architecture. |
| Reflection | Student documented at least one AI mistake, overreach, or rejected suggestion. |
