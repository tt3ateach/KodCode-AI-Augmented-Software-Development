# Module 3 Instructor Notes — Vibe Coding and Natural-Language-Driven Development

## Module purpose

Module 3 teaches students to start from product intent and use conversational coding tools to generate a first draft quickly, then regain engineering control.

This is the continuation of Module 2, not a contradiction. Module 2 taught disciplined AI-assisted development. Module 3 increases generation speed and autonomy, so the Module 2 habits become more important.

Core teaching line:

> Module 3 does not replace the Module 2 workflow. It stress-tests it.

## Required module identity

Module 2 question:

> How do I use AI inside a disciplined developer workflow?

Module 3 question:

> What happens when AI generates more of the first draft from product intent?

Students should leave with:

> Use vibe coding for acceleration and exploration, not blind delegation.

## Core workflow

Use this throughout:

> Brief → Explore → Contain → Generate → Review → Own

This maps to the shorter phrase:

> Brief → Generate/Contain → Review → Own

The subtlety: Stage A may feel broader and more exploratory than Module 2, but Stage B must quickly add constraints, stop conditions, and verification.

## Corrected schedule

### Core 6-hour schedule

| Segment | Time |
|---|---:|
| Definition, continuity from Module 2, workflow | 45m |
| Prompt progression and tool forms | 35m |
| Fit, risk, and verification | 40m |
| Handoff and existing codebases | 40m |
| Guided demo | 55m |
| Lab Phase 1 — first draft | 80m |
| Lab Phase 2 — ownership and API integration | 50m |
| Wrap-up | 15m |
| **Total** | **360m** |

### Expanded 7–8 hour schedule

| Segment | Time |
|---|---:|
| Definition, continuity from Module 2, workflow | 60m |
| Prompt progression and tool forms | 55m |
| Fit, risk, and verification | 55m |
| Handoff and existing codebases | 55m |
| Guided demo | 70m |
| Lab Phase 1 — first draft | 100m |
| Lab Phase 2 — ownership and API integration | 75m |
| Wrap-up | 25m |
| **Total** | **495m** |

## Optional pacing guidance

Clearly optional topics:

- detailed vendor/tool comparison;
- local/self-hosted setup;
- screenshot-to-code and visual asset generation;
- UI polish beyond core behavior;
- dark mode, details panel, advanced filtering;
- cloud-agent details beyond the workflow pattern.

Do not skip:

- Module 2 continuity;
- definition of vibe coding;
- prompt progression;
- risk and fit discussion;
- handoff problem;
- existing-codebase constraints;
- Phase 2 ownership;
- minimal end-to-end API integration.

## Teaching the “vibe” without endorsing chaos

Students may hear “vibe coding” as permission to skip discipline. Correct that immediately.

Suggested wording:

> The vibe is in the first draft. The professionalism is in what happens after.

Use “vibe coding” as a workflow category:

- start with intent;
- ask for experience options;
- generate a visible first slice;
- then constrain, inspect, test, and own.

## Existing codebase scenario

Use this scenario:

> A team has an existing admin console. Product wants quick-add, filtering, and a lightweight sprint view. The risky move is to ask AI to “redesign the dashboard.” The safer move is to map the existing app, find seams, and add the smallest vertical slice.

Teach Stage 0 for mature repos:

> Read-only orientation before broad vibe-style prompting.

## Devin-style workflow pattern

The syllabus mentions Devin-style workflows. Teach this as a pattern, not a required product:

- assign an issue or outcome;
- agent works in an isolated environment;
- agent may run longer and explore;
- result comes back as branch, PR, report, or artifact;
- developer reviews final output rather than steering every step.

Contrast:

| Workflow | Human steering | Typical result |
|---|---|---|
| conversational vibe coding | frequent steering | first draft / visible slice |
| IDE agent mode | bounded edits with local review | modified files |
| issue-driven coding agent | less continuous steering | branch, PR, report, artifact |

Important line:

> Less steering does not mean less review. It usually means more review.

## Demo advice

Use `module3_demo_runbook.md`. Do not improvise a long live AI session without fallback.

The demo should visibly show:

- a broad Stage A response;
- a narrower Stage B plan;
- at least one rejected suggestion;
- one verification failure or weak test discussion;
- one ownership cleanup;
- the Module 2 API integration plan.

## Lab facilitation tips

- During Phase 1, prevent overbuilding.
- During Phase 2, ask students to explain the code before changing it.
- Ask for one rejected/revised AI suggestion from every group.
- Reward students who catch AI mistakes.
- Do not reward visual polish more than maintainability and verification.

## Common student traps

1. Treating a good-looking UI as a good implementation.
2. Letting AI introduce dependencies because it is convenient.
3. Accepting `innerHTML`-based rendering of user text.
4. Not reading generated tests.
5. Calling the first draft “done.”
6. Skipping the API integration because localStorage works.
7. Confusing local/self-hosted tool setup with the core lesson.

## How to use the notebook with the deck

- Use slides for pacing and mental models.
- Use the notebook for deeper explanations and worked solutions.
- Use the demo runbook for exact live prompts.
- Use the lab guide for student tasks.
- Use the solution repo as fallback, not as the first thing students see.

## Exit ticket

Ask:

> What did you own after Phase 2 that you did not own after the first AI-generated draft?

Strong answers mention structure, tests, API boundary, error handling, accessibility, rejected suggestions, and explainability.
