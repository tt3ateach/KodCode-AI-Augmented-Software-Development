# Design Brief — Task Tracker Frontend

## Product scenario

An engineering team wants a lightweight browser-based task tracker for work during a sprint.

The first version should feel useful quickly, but it should remain small enough that a developer can read, verify, and own the generated code.

## Core user needs for the first draft

A developer should be able to:

1. see current tasks at a glance;
2. add a task quickly;
3. filter tasks by status;
4. mark a task complete or reopen it;
5. keep local data between browser refreshes;
6. understand what happens when there are no visible tasks.

The brief intentionally does **not** prescribe a JavaScript module structure. The first implementation plan should propose one.

## Constraints

- Use plain browser JavaScript, HTML, and CSS.
- No build tooling.
- No new runtime dependencies.
- Keep the first slice small and reviewable.
- Render user-provided task titles safely; do not interpret task text as HTML.
- Use automated tests where they add clear value, especially for pure logic.
- Use manual browser checks for DOM behavior.

## Optional stretch ideas

Only use these if the core first draft is already working and verified:

- free-text search;
- priority editing;
- combined filters;
- responsive polish;
- keyboard/focus polish beyond basic form behavior;
- dark mode;
- task detail panel.

## Later ownership/integration requirement

After the local first draft has been generated, reviewed, and cleaned up, connect the core flow to the Module 2 Work Items API at:

```text
http://127.0.0.1:8000
```

Keep that integration intentionally small:

- list work items;
- create a work item;
- toggle status between `todo` and `done`;
- update priority;
- show a useful error if the API is unavailable;
- retain local mode as fallback.

No authentication, deployment, or multi-user synchronization is required.
