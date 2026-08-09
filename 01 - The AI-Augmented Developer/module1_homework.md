# Module 1 Homework — The AI-Augmented Developer

These homework exercises are optional but recommended. They are designed to make the Module 1 decision model concrete before students start using AI heavily in Module 2.

---

## Homework 1 — AI Tool-Fit Decision Memo

### Goal

Practice choosing the right AI interaction mode for realistic engineering tasks.

### Estimated time

30–45 minutes.

### Scenario

You joined a product team that is adopting AI tools. The team lead asks you to classify a backlog of tasks by the amount of AI delegation that is appropriate.

### Student task

For each task below, choose one recommended mode:

- Inline assistant
- Chat assistant
- AI pair programmer
- IDE agent
- Coding/cloud agent
- Human-led with AI support only

For each task, justify the choice using:

- task clarity;
- context required;
- blast radius;
- verification cost;
- privacy/security risk.

### Task list

| # | Task |
|---:|---|
| 1 | Write docstrings for a small utility module. |
| 2 | Explain a 400-line legacy parser before anyone changes it. |
| 3 | Generate unit tests for a pure date-formatting function. |
| 4 | Refactor authentication middleware shared by three services. |
| 5 | Summarize a long bug thread into reproduction steps. |
| 6 | Build a prototype internal admin screen for a demo. |
| 7 | Add a database migration that changes customer billing state. |
| 8 | Draft a changelog from merged pull requests. |
| 9 | Fix a flaky test in a non-critical package. |
| 10 | Create a script that rotates production secrets. |

### Expected deliverable

A short memo or table with one row per task.

Suggested columns:

| Task | Recommended AI mode | Safe context to provide | Verification plan | Main risk |
|---|---|---|---|---|

### Optional stretch

Add one task from your own work and classify it using the same model.

---

## Suggested solution — Homework 1

There is not always one perfect answer. The table below gives strong default classifications and acceptable alternatives.

| # | Recommended mode | Reasoning | Verification plan |
|---:|---|---|---|
| 1 | Inline assistant or chat assistant | Low risk, local, easy to inspect. | Read generated docstrings against code. |
| 2 | Chat assistant / AI pair programmer | Read-only orientation is a good use case; no code changes needed yet. | Spot-check explanation against actual code. Ask AI to list uncertainty. |
| 3 | AI pair programmer | Useful draft task, but tests can encode wrong assumptions. | Review assertions, add edge cases manually, run tests. |
| 4 | Human-led with AI support only | Auth has high blast radius and policy/security complexity. | Human design review, security review, targeted AI use for small subtasks only. |
| 5 | Chat assistant | Summarization is low risk if reviewed; context may include sensitive info, so redact. | Compare summary to thread; verify reproduction steps. |
| 6 | IDE agent or coding/cloud agent | Prototype is suitable for broader generation if clearly marked as non-production. | Manual review, accessibility checks, smoke tests. |
| 7 | Human-led with AI support only | Billing state and migrations are high blast-radius, hard-to-undo changes. | Human design, migration rehearsal, rollback plan, data checks. |
| 8 | Chat assistant or workflow | Text generation over merged PRs is a good low-risk workflow. | Compare with PR list; edit for release accuracy. |
| 9 | AI pair programmer or IDE agent | Bounded if the package is non-critical and tests can verify. | Run the test repeatedly; inspect for overfitting or sleep-based fixes. |
| 10 | Human-led with AI support only | Secrets operations are high risk; AI can help draft a checklist, not directly act. | Manual implementation, peer review, dry-run, logging review. |

### Review rubric

| Criterion | Strong answer |
|---|---|
| Uses the decision model | Mentions clarity, context, blast radius, verification, and privacy/security. |
| Avoids blind delegation | Keeps high-risk tasks human-led. |
| Defines safe context | Redacts or limits sensitive information. |
| Plans verification | Includes tests, diff review, manual review, or rollback where appropriate. |
| Allows nuance | Notes acceptable alternatives for low/medium-risk tasks. |

### Discussion notes for next class

Ask students:

1. Which tasks created disagreement?
2. Which task seemed easy until you considered blast radius?
3. Which tasks are safe for AI only if the team has good tests?
4. What company policy would make the classification easier?

---

## Homework 2 — Team AI Usage Agreement

### Goal

Draft a one-page AI usage agreement for a development team.

### Estimated time

30–45 minutes.

### Scenario

Your team is beginning to use AI assistants and coding agents. The engineering manager wants a short policy that is practical enough for daily use.

### Student task

Write a one-page policy covering:

- allowed tools;
- data that must not be pasted;
- review requirements;
- acceptable agent permissions;
- when human approval is required;
- how to record AI-assisted work;
- what to do when AI output is uncertain.

### Expected deliverable

A one-page Markdown policy.

### Optional stretch

Add a small “permission ladder” for AI tools.

Example:

1. Suggest text only.
2. Edit files after approval.
3. Run tests after approval.
4. Open PR after approval.
5. Deploy: never without explicit human-controlled process.

---

## Suggested solution — Homework 2

# Sample Team AI Usage Agreement

## Purpose

We use AI tools to accelerate development, improve understanding, and reduce repetitive work. AI output is treated as a draft until reviewed and verified by a team member.

## Approved uses

- Code explanation and onboarding.
- Boilerplate and scaffolding.
- Test and documentation drafts.
- Refactoring suggestions.
- PR summaries and changelog drafts.
- Bounded implementation tasks with clear acceptance criteria.

## Restricted uses

AI must not be allowed to make unreviewed changes to:

- authentication and authorization;
- payment or billing logic;
- secrets and credential management;
- production deployment scripts;
- database migrations affecting customer data;
- incident response actions.

AI can assist with these areas only in read-only or advisory mode unless the team explicitly approves a narrow task.

## Data handling

Never paste:

- secrets, keys, tokens, or credentials;
- live customer data;
- regulated personal data;
- production database dumps;
- non-public vulnerability details unless approved for the tool and context.

Redact logs and stack traces before sharing. Use synthetic examples when possible.

## Review requirements

Before accepting AI-generated code:

- inspect the diff;
- run tests and relevant checks;
- verify edge cases and failure modes;
- review security-sensitive behavior;
- confirm the change fits architecture and conventions;
- record meaningful AI-generated changes in the PR description when appropriate.

## Agent permissions

Default permission level is read-only. Agents may edit files only in a branch or local workspace. Agents may run commands only after the developer reviews the command. Agents must not deploy, rotate secrets, change production data, or merge PRs.

## Human approval gates

Human approval is required before:

- merging a PR;
- changing customer-visible behavior;
- modifying auth, billing, secrets, or data migrations;
- running destructive commands;
- sending external communications generated by AI.

## Uncertainty rule

When AI output includes assumptions, missing context, or uncertain behavior, the developer must either verify the claim independently or reject/redo the output.

### Why this solution is strong

- It distinguishes assistant use from agent permissions.
- It gives practical allowed/restricted use cases.
- It includes concrete data-handling rules.
- It keeps review, merge, and production risk human-owned.
- It is short enough for a team to actually use.

---

## Grading / review rubric

| Criterion | Strong answer |
|---|---|
| Practicality | Policy is short enough to use and specific enough to guide behavior. |
| Data safety | Secrets, customer data, and regulated data are clearly restricted. |
| Permission boundaries | Read/write/run/deploy permissions are separated. |
| Review discipline | Human review and verification are explicit. |
| Risk awareness | High-blast-radius areas are treated differently from low-risk tasks. |
