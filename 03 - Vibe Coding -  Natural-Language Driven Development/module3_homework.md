# Module 3 Homework — Optional Exercises with Suggested Solutions

## Homework 1 — Ownership Review of an AI-Generated UI

**Estimated time:** 60–90 minutes

### Task

Use `review_exercises/flawed_generated_draft/`. Review it as if it came from an AI coding assistant.

Identify at least eight problems across:

- security/safety;
- maintainability;
- accessibility;
- testability;
- scope creep;
- API integration assumptions.

### Deliverable

A review memo with:

- findings;
- severity;
- suggested fix;
- whether the fix belongs before or after merging.

### Suggested solution summary

Strong reviews should catch:

- unsafe task rendering with `innerHTML`;
- unguarded localStorage parsing;
- duplicated event listener setup;
- monolithic file responsibilities;
- missing keyboard/focus support;
- hidden dependency or framework suggestion;
- no API error handling;
- no tests for state or API mapping;
- status mismatch between frontend `in-progress` and API `in_progress`;
- visual polish being treated as completeness.

## Homework 2 — Add One Optional Feature Safely

**Estimated time:** 90–150 minutes

### Choose one

- free-text search;
- detail panel;
- due-date display;
- keyboard focus polish;
- dark-mode toggle;
- richer priority sorting.

### Rules

- Ask AI for two approaches first.
- Choose the smaller approach.
- Preserve current core behavior.
- Add or update tests if pure logic changes.
- Run tests and perform manual browser checks.
- Record one AI suggestion you rejected.

### Suggested solution example — search

A strong solution:

- stores `filters.search` as normalized text;
- filters title, owner, and description if present;
- trims and lowercases search once;
- preserves status filtering;
- adds tests for search + status combined;
- keeps DOM behavior simple.

A weak solution:

- duplicates search logic in multiple files;
- filters by rendered text instead of state;
- fails on uppercase/lowercase;
- breaks empty-state behavior.

## Homework 3 — Vibe-to-Ownership Reflection

**Estimated time:** 30–45 minutes

### Task

Write a one-page reflection after completing the lab.

Prompts:

1. What did AI produce faster than you would have?
2. What looked good but required correction?
3. What did you reject or narrow?
4. How did you verify behavior?
5. What would you refuse to delegate next time?

### Suggested strong answer

A strong reflection names concrete artifacts: a prompt, a file, a test, a browser check, a rejected suggestion, and a remaining risk. It does not merely say “AI was useful.”

Example:

```text
AI quickly produced a working render loop and basic filtering. I rejected its suggestion to add drag-and-drop because it added scope and a dependency. I also replaced an innerHTML-based task card with DOM node creation to avoid rendering user text as HTML. I verified normalizeTask and applyFilters with node tests, checked quick-add and toggle manually in the browser, and tested API unavailable behavior by stopping the Module 2 server. I would not delegate API authentication or persistence design from a broad vibe prompt.
```
