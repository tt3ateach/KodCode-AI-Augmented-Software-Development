# Module 3 Prompt Guide — Vibe Coding with Ownership

This guide teaches a deliberate progression:

> Stage A — Explore product intent  
> Stage B — Contain the implementation  
> Stage C — Own the result

Module 3 is intentionally different from Module 2. In Module 2, students usually enter through planning and implementation inside an existing developer workflow. In Module 3, students may start broader and closer to product intent. That does **not** remove the need for planning, review, testing, and ownership.

## Stage A — Explore product intent

### 1. Start from the brief, not from files

```text
Read docs/design-brief.md.
Propose two useful first-version experiences for this task tracker.
Focus on visible user flow, core behavior, and what should be deliberately omitted from the first draft.
Do not edit files yet.
```

### 2. Ask for product tradeoffs

```text
Compare the two first-version directions.
Which one is safer for a 90-minute classroom implementation?
Which one is easier to verify?
Which one creates less long-term ownership risk?
```

### 3. Ask for a user-flow sketch

```text
For the safer first version, describe the user flow step by step.
Use plain language, not code.
Include empty state, quick add, filtering, completion toggle, and local persistence.
```

## Stage B — Contain the implementation

### 4. Turn broad intent into a bounded slice

```text
Choose the smaller direction.
Before editing, propose the smallest vertical slice.
Include files to touch, files to avoid, responsibilities of each file, stop conditions, and verification checks.
```

### 5. Add explicit constraints

```text
Revise the plan with these constraints:
- no build tools
- no new runtime dependencies
- preserve the existing file structure
- keep generated DOM safe: do not render task text with unsafe innerHTML
- tests only for pure logic and API client behavior
- manual browser checks for DOM behavior
- stop after the core slice works
```

### 6. Existing-codebase orientation before vibe coding

Use this before broad generation inside a mature repo:

```text
Before proposing UI changes, produce a read-only map of the current app.
Identify existing seams, files that should not be rewritten, naming conventions, and likely integration points.
Do not edit files yet.
```

### 7. Stop conditions

```text
Implement only the agreed first slice.
Stop after task rendering, quick-add, one status filter, completion toggle, local persistence, and manual verification notes.
Do not add dark mode, drag-and-drop, authentication, charts, or new dependencies.
```

## Stage C — Own the result

### 8. Ask for handoff help

```text
Explain the code you just generated as if handing it to a teammate.
Include file responsibilities, data flow, state changes, assumptions, risks, and what should be reviewed manually.
```

### 9. Ask for a maintainability review

```text
Review this implementation for maintainability.
Find duplicated logic, confusing names, overly broad functions, unsafe DOM behavior, missing edge cases, and places where tests are too weak.
Do not edit yet.
```

### 10. Ask for end-to-end integration plan

```text
Plan the smallest safe integration with the Module 2 Work Items API.
Limit scope to list, create, status toggle, priority update, and error handling.
Do not add authentication.
Keep local persistence as the fallback mode.
```

### 11. Ask for ownership reflection

```text
Write a short ownership reflection:
- what AI generated well
- what you changed or rejected
- what remains risky
- how you verified behavior
- what the next human-owned improvement should be
```

## Bad prompt / better prompt

Bad:

```text
Build a task tracker app.
```

Better Stage A:

```text
Read the design brief and propose two first-version task tracker experiences.
Focus on user flow, what to omit, and what is easiest to verify.
Do not edit files yet.
```

Better Stage B:

```text
Implement the smaller slice only. Keep the existing module structure, use no new dependencies, and stop after rendering, quick-add, status filter, completion toggle, and local persistence. Tell me exactly what to test manually.
```

Better Stage C:

```text
Explain the resulting architecture and identify what must be cleaned up before another developer owns this code.
```

## Optional: tool comparison prompts

### Copilot baseline

```text
Use the existing files in this VS Code workspace. Start by explaining the plan in chat, then edit only the files needed for the agreed first slice.
```

### Claude Code plan mode

```text
Use plan mode. Explore the repo and propose a plan for the first slice without editing source files. Include risks and exact files to touch.
```

### Codex / cloud-agent style

```text
Treat this as a prototype task. Produce a branch-ready first draft, then return a summary of changed files, browser checks, risks, and what a human reviewer should focus on.
```

### Local/self-hosted tools — optional

```text
Using only this local repo and no external services, explain what a local model can safely help with and what should remain human-owned.
```

## Design-specific cautions

- UI that looks polished can still be unmaintainable.
- Screenshot-to-code workflows often produce brittle markup.
- Visual polish is optional; accessible behavior is not.
- Avoid unsafe DOM insertion for user-provided task titles.
- First drafts should be reviewed for structure, not only appearance.
