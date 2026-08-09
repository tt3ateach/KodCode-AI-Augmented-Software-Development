# Module 1 Instructor Notes — The AI-Augmented Developer

## Module identity

Module 1 is the course’s conceptual operating system. It should give students stable vocabulary and judgment criteria before they start using AI tools heavily.

The module is not a product tour. The tool landscape matters, but the durable skill is choosing the right interaction mode and keeping ownership of the result.

## Audience assumptions

- Experienced developers with Python as a prerequisite.
- A few technical product managers may be present.
- Students have commercial GitHub Copilot licenses.
- Students may arrive with very different opinions: curiosity, skepticism, hype, fear, or hands-on experience.

## Teaching goal

By the end, students should be able to answer:

1. What kind of AI interaction am I using?
2. How much responsibility am I delegating?
3. What context is safe to provide?
4. How will I verify the output?
5. What must remain human-owned?

Core phrase:

> AI changes the mechanics of software work, not the need for engineering judgment.

---

## Suggested timing

| Segment | Core time | Expanded time | Optional? |
|---|---:|---:|---|
| Opening and course frame | 10m | 15m | No |
| Taxonomy and spectrum | 25m | 30m | No |
| 2026 shift and tool landscape | 20m | 25m | Partly |
| Decision model | 20m | 25m | No |
| Governance mini-case | 20m | 30m | No |
| MCP preview | 10m | 15m | Optional |
| Exercise and debrief | 25m | 35m | No |
| Wrap-up | 10m | 15m | No |

For a strict 2-hour delivery, shorten the ecosystem discussion and make the MCP preview a two-minute teaser.

---

## Opening discussion script

Start with four “would you delegate this?” questions:

1. Would you let AI rename variables in one file?
2. Would you let AI explain a legacy module before you touch it?
3. Would you let AI implement a feature and open a PR?
4. Would you let AI touch production incident response or authentication?

Expected pattern:

- Students are usually comfortable with local, reversible tasks.
- They become more cautious as context, blast radius, and verification cost increase.
- That creates the opening for the interaction spectrum and the decision model.

Instructor line:

> The interesting question is not whether AI is useful. It is how much responsibility we can safely give it for a specific task.

---

## Slide-by-slide teaching notes

### Slide 1 — Title

Position the course as practical and developer-owned. Avoid saying “AI replaces developers.” Say that the course is about using AI as leverage while preserving engineering accountability.

### Slide 2 — Why this course exists now

Emphasize the 2026 shift: tools moved from autocomplete to repo-aware and agentic workflows. The course is timely because the operational problem changed: developers now need to design workflows, permissions, and review practices, not merely write better prompts.

### Slide 3 — Definition

Read the definition slowly. The phrase “while leaving accountability with humans” is not a legal footnote; it is the center of the course.

### Slide 4 — From autocomplete to delegated work

Use this as the main framing slide. Explain that modern tools can inspect files, edit code, run tests, connect to external tools, and create PRs. That is useful, but it changes risk.

### Slide 5 — Interaction spectrum

Walk left to right. Use one task, such as “add validation to a parser,” and explain how it changes across modes. Keep vendor names out of the first explanation.

### Slide 6 — Copilot as classroom baseline

Keep this short. Copilot is the common surface because students have licenses. It is also broad enough to demonstrate completions, chat, agentic editing, and PR/review workflows.

### Slide 7 — Current ecosystem

Do not turn this into a competition between vendors. Teach capability classes and mention examples. Make clear that the lineup will change; the classification model should survive product churn.

### Slide 8 — Assistant, pair programmer, agent

This is a vocabulary slide. Students should be able to use these terms precisely for the rest of the course.

### Slide 9 — Decision model

Spend time here. Ask students which of the five questions they currently underuse. Most developers think about task clarity and context; fewer think systematically about blast radius and verification cost.

### Slide 10 — Tool-fit examples

Use the examples to show that “AI or no AI” is too crude. The answer is often “yes, but in a constrained mode.”

### Slide 11 — Where AI is strong

Keep the tone balanced. These strengths are real. Students should feel that the course is not anti-AI.

### Slide 12 — Plausible incompleteness

This is one of the most important slides. Stress that the most dangerous outputs are often polished and mostly correct, not obviously absurd.

### Slide 13 — The confident intern problem

Use the mini-case. Let students annotate what is wrong before revealing the answer. The goal is to make governance memorable.

### Slide 14 — Privacy, IP, governance

Keep examples concrete. “Never paste secrets” is obvious but not enough. Discuss logs, stack traces, proprietary architecture, customer data, and security findings.

### Slide 15 — MCP preview

Teaser only. The point is not mechanics. The point is that connected tools expand both usefulness and risk.

### Slide 16 — Exercise

Run groups of 2–4. Give each group 4–6 tasks and ask them to classify the AI mode, safe context, and verification plan.

### Slide 17 — Takeaways

Bridge to Module 2: now that students have the mental model, Module 2 teaches the daily workflow.

---

## How to avoid tool-war conversations

Use this response pattern:

> Tool comparisons are useful only when they change the workflow decision. For this course, we care about what the tool can read, what it can change, what it can run, and how we review the result.

Then redirect to:

- context access;
- permission model;
- review workflow;
- team policy;
- cost and availability only when operationally relevant.

---

## Likely student questions

### “Is Copilot just autocomplete?”

No. Modern Copilot spans completions, chat, agentic workflows, code review, CLI/cloud capabilities, repository instructions, and MCP-related context/tooling. In this course it is the shared surface, not the only possible tool.

### “Will AI replace developers?”

Avoid hype and fear. A balanced answer:

- AI changes the task mix.
- Boilerplate and routine transformations become less differentiating.
- Problem framing, architecture judgment, testing, review, security, and product understanding become more valuable.
- Developers who can direct, verify, and integrate AI work will have higher leverage.

### “Can we trust generated tests?”

Only as drafts. Generated tests often miss edge cases, copy the same faulty assumptions as the implementation, or assert implementation details instead of behavior.

### “What is the biggest anti-pattern?”

Delegating vague, sensitive, or hard-to-verify work. A close second is accepting generated code because the explanation sounded confident.

### “Should we require prompt logs?”

For learning, yes. In production teams, it depends. The durable requirement is traceability: what changed, why it changed, how it was verified, and what human approved it.

---

## Demo summary

Use the `demo_repo/` folder. Detailed scripts are in `module1_demo_runbook.md`.

Recommended demos:

1. **One task, four interaction modes** using `src/retail_demo/profile_parser.py`.
2. **The confident intern problem** using `demo_repo/exercises/confident_intern_problem.md`.

Optional alternatives:

- Use `src/retail_demo/pricing.py` for validation and test generation.
- Use `src/retail_demo/legacy_parser.py` for legacy-code explanation.

---

## Failure recovery for live AI demos

AI output is nondeterministic. Do not fight the tool in front of the class for too long.

Use this recovery ladder:

1. Ask the AI to explain assumptions and risks before editing.
2. If it over-edits, stop and show why the diff is too broad.
3. If it produces bad tests, turn that into a teaching moment.
4. If tool integration fails, use the prepared prompt/output examples in the runbook.
5. If time is tight, skip live editing and run the confident intern mini-case.

Instructor phrase:

> A failed AI demo is not a failed class if we use it to inspect the workflow.

---

## End-of-module takeaway

Students should leave with this sentence:

> AI-augmented development is not about surrendering engineering to AI; it is about using the right level of AI assistance for the task, while keeping human ownership of quality, safety, and outcomes.
