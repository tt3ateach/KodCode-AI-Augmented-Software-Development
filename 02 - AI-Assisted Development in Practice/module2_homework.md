# Module 2 Homework — Optional Exercises with Suggested Solutions

Homework is optional. Each exercise includes a suggested solution or model answer.

## Homework 1 — Extend the Work Items API

**Estimated time:** 90–150 minutes

Choose one feature:

1. Add `due_date`.
2. Add pagination.
3. Add tag support.
4. Add soft delete.
5. Add sorting.

Required deliverables:

- implementation;
- tests;
- prompt log;
- verification output;
- short reflection: what AI helped with and what required human correction.

### Suggested solution — pagination

A strong pagination solution:

1. Adds `limit: int = Query(default=50, ge=1, le=100)` and `offset: int = Query(default=0, ge=0)` to `GET /work-items`.
2. Passes `limit` and `offset` to `repository.list_items()`.
3. Uses `LIMIT ? OFFSET ?` after filters.
4. Adds tests for default behavior, `limit=1`, `offset=1`, invalid `limit=0`, and combined filters.

Strong reflection example:

```text
AI suggested returning a pagination metadata object. I rejected it because it would break the current list response shape. I kept the change backward-compatible and documented metadata as a future API version decision.
```

## Homework 2 — Legacy Code Onboarding Packet

**Estimated time:** 60–90 minutes

Produce:

- behavior summary;
- key functions;
- assumptions;
- risks;
- missing tests;
- recommended first safe change.

### Model answer

```text
The module contains status normalization and overdue detection helpers. normalize_status converts common aliases to canonical values and passes unknown statuses through. is_overdue checks due_at/due_date and returns True only when the item is unfinished and past due.

Risks: malformed date strings raise exceptions, timezone-aware and naive datetimes may be problematic, and unknown statuses pass through without validation.

Recommended first safe change: add tests before refactoring date parsing or status handling.
```

## Homework 3 — API Client Review

**Estimated time:** 45–75 minutes

Ask AI to generate a Python API client for the Work Items API. Then review it.

Checklist:

- explicit timeout;
- clear error behavior;
- no fake secrets or auth assumptions;
- no noisy comments;
- docstrings explain intent;
- tests with `httpx.MockTransport`;
- response assumptions visible.

### Suggested solution

The solution repo includes:

```text
work_items_api_solution/app/client.py
work_items_api_solution/tests/test_api_client.py
```

A strong submission rejects generated clients that:

- omit timeouts;
- swallow HTTP errors;
- print full payloads;
- invent authentication headers;
- contain comments like `# send request` that add no value.

## Homework 4 — Prompt Cookbook Contribution

**Estimated time:** 30–45 minutes

Write three prompts:

1. planning prompt;
2. debugging prompt;
3. code-review prompt.

Each prompt must include task context, constraints, expected output format, and verification/review requirement.

### Suggested solution

Planning:

```text
Do not implement yet. Given this ticket and repository context, produce a minimal implementation plan with assumptions, likely files, out-of-scope files, risks, tests, verification commands, and smallest safe slice.
```

Debugging:

```text
Analyze this failing test and stack trace. Do not patch immediately. List likely causes, evidence, the smallest check to confirm, and the first fix you would try.
```

Review:

```text
Review this diff as a review aid, not as final approval. Identify behavior changes, missing tests, privacy/security concerns, backward compatibility concerns, and questions for the human reviewer.
```
