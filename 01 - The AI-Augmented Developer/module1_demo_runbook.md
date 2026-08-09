# Module 1 Demo Runbook — The AI-Augmented Developer

This runbook supports the Module 1 demos. It is written for GitHub Copilot Chat/Agent Mode because Copilot is the classroom baseline, but the same prompts can be adapted to Claude Code, Codex, or another repo-aware coding assistant.

## Repository

Use:

```text
demo_repo/
```

Main files:

```text
src/retail_demo/profile_parser.py
src/retail_demo/pricing.py
src/retail_demo/legacy_parser.py
tests/test_profile_parser.py
tests/test_pricing.py
exercises/confident_intern_problem.md
```

## Prerequisites

- Python 3.11+
- VS Code or another IDE with the chosen AI tool
- GitHub Copilot Chat enabled
- Terminal open in `demo_repo/`

Setup:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e . pytest
pytest
```

Expected starting result:

```text
All existing tests pass.
```

The repository is intentionally under-defended. The point is not to show broken code; the point is to show that “working happy path” is not enough.

---

# Demo 1 — One task, four AI interaction modes

## Purpose

Make the taxonomy concrete by using the same task across several AI modes.

Task:

> Add validation to a small Python function that parses user profile data.

Target file:

```text
src/retail_demo/profile_parser.py
```

## When to run

After teaching the interaction spectrum and before the decision model, or immediately after the decision model as a practical illustration.

## Instructor setup

1. Open `demo_repo/` in VS Code.
2. Open `src/retail_demo/profile_parser.py`.
3. Open `tests/test_profile_parser.py`.
4. Run:

```bash
pytest
```

5. Explain that the existing tests pass but validate only the happy path.

## Step 1 — Assistant mode / inline completion

Instructor action:

1. Place the cursor inside `parse_user_profile`.
2. Add a comment such as:

```python
# Validate that email is present and contains '@'
```

3. Let inline suggestions appear.
4. Accept or reject one small suggestion.

Teaching point:

- Inline assistance is fast and local.
- It is useful for small, obvious edits.
- It does not understand the whole risk picture unless the context makes that clear.

Likely AI variation:

- It may suggest a minimal check for `@`.
- It may suggest raising `ValueError`.
- It may not update tests.

Debrief question:

> What did the assistant not know about the task?

## Step 2 — Chat explanation mode

Prompt to paste:

```text
Explain src/retail_demo/profile_parser.py in one paragraph. Then list the top five validation risks. Do not suggest code changes yet.
```

Expected output:

- Function reads fields from a dictionary.
- Normalizes name/email.
- Converts age to int if present.
- Converts marketing flag to `bool`.
- Risks: missing email, invalid email, negative age, unexpected types, ambiguous boolean values.

Teaching point:

- Chat is excellent for orientation.
- Read-only analysis is a safer first step than immediate editing.
- The phrase "Do not suggest code changes yet" helps keep the assistant in analysis mode.

Likely AI variation:

- It may include code suggestions anyway.
- It may overstate email validation.
- It may miss ambiguous boolean parsing.

Recovery:

Ask:

```text
Separate confirmed behavior from assumptions. Which risks can you verify directly from the code?
```

## Step 3 — Pair-programming prompt

Prompt to paste:

```text
I want to add input validation to `parse_user_profile` without changing the public return type. First propose a minimal plan. Include expected behavior, affected files, tests to add, and risks. Do not edit files yet.
```

Expected output:

- Modify `profile_parser.py`.
- Add validation for required `name` and `email`.
- Reject invalid or negative age.
- Clarify allowed values for marketing flag.
- Add tests for missing email, invalid email, invalid age, and negative age.

Teaching point:

- This is the first disciplined workflow move: plan before code.
- The assistant must expose assumptions and test strategy.

Student engagement:

Ask students:

> What is missing from the plan?

Possible answers:

- What exception type?
- Should blank names be allowed?
- How strict should email validation be?
- What should happen with unknown extra fields?
- What about privacy-sensitive logging?

## Step 4 — Agent-style bounded change

Prompt to paste after reviewing the plan:

```text
Implement the smallest safe validation change for parse_user_profile. Constraints:
- Do not add third-party dependencies.
- Preserve the UserProfile dataclass and return type.
- Raise ValueError with clear messages for invalid input.
- Add focused tests for missing email, invalid email, blank name, negative age, and unsupported marketing_opt_in values.
- Keep the diff limited to profile_parser.py and test_profile_parser.py.
After editing, summarize the diff and tell me exactly what checks to run.
```

Expected output:

- Changes in exactly two files.
- New validation helper or inline validation.
- Additional tests.
- Suggested command: `pytest tests/test_profile_parser.py` or `pytest`.

Instructor action:

Run:

```bash
pytest
```

Teaching point:

- This is bounded delegation.
- It is only appropriate because the task is clear, local, and cheap to verify.
- The instructor still owns the diff, tests, and merge decision.

Likely AI variations:

- It may add over-strict email validation.
- It may silently change `marketing_opt_in` behavior.
- It may edit README or unrelated files.
- It may write tests that simply mirror implementation details.

Failure recovery:

If the diff is too broad, say:

```text
Stop. Revert unrelated changes. Keep the diff limited to profile_parser.py and test_profile_parser.py. Explain why each remaining change is necessary.
```

If tests fail, say:

```text
Before fixing, explain the test failure and identify whether the test or implementation is wrong.
```

Debrief questions:

1. Which mode was best for orientation?
2. Which mode was best for implementation?
3. What made this safe enough for agent-style editing?
4. What would make it unsafe?

---

# Demo 2 — The confident intern problem

## Purpose

Make governance memorable. Students inspect a polished AI answer that looks helpful but contains several safety and correctness problems.

## When to run

After the "plausible incompleteness" slide and before privacy/governance.

## Required file

```text
exercises/confident_intern_problem.md
```

## Instructor action

1. Open the file.
2. Show only the “AI answer” section first.
3. Give students 4–6 minutes to annotate problems individually or in pairs.
4. Reveal the answer key.

## Student prompt

```text
This answer sounds confident. What is wrong with it? Mark issues under:
- privacy/data leakage
- invented behavior
- security risk
- missing verification
- maintainability risk
```

## Expected findings

Students should find:

- It suggests logging full user payloads, including potentially personal data.
- It invents behavior of a fictional validation library.
- It proposes committing an example token.
- It does not include tests for invalid inputs.
- It treats happy-path execution as sufficient verification.
- It recommends broad agent permission for a small task.
- It gives a confident conclusion without evidence.

## What to say while students work

> The issue is not that the answer is obviously foolish. The issue is that it is smooth enough to pass a tired reviewer.

## Debrief

Ask:

1. Which problem was easiest to spot?
2. Which problem would be easiest to miss in a real PR?
3. Which guardrail would have prevented this?
4. What policy should the team write after seeing this?

## Failure recovery

This demo does not depend on live AI. Use it whenever live tools fail or time is tight.

---

# Optional Demo 3 — Legacy code explanation

## Purpose

Show practical daily value without changing code.

Target file:

```text
src/retail_demo/legacy_parser.py
```

Prompt:

```text
Explain parse_partner_feed for three audiences:
1. a developer who may refactor it,
2. a product manager who needs to understand behavior,
3. a support engineer investigating bad partner data.
Then list risks and missing tests. Do not change code.
```

Teaching point:

- AI can translate code understanding for different audiences.
- Explanation is useful, but it is not proof.
- Ask the AI to list uncertainty and missing tests.

Expected risks:

- Silently skips short rows.
- Crashes on invalid id/spend.
- Treats any unknown status as inactive.
- Title-cases names, which may corrupt names.
- Lowercases emails without validation.

---

# Optional Demo 4 — Delegation boundary

## Purpose

Show why not every task should be delegated.

Prompt to show, not necessarily run:

```text
Implement login, session management, password reset, and role-based access control for this service. Make it production-ready.
```

Ask students:

- Why is this too broad?
- What policy decisions are missing?
- What security requirements are missing?
- What would be a safer first AI-assisted step?

Safer first prompt:

```text
Create a read-only checklist of design questions and security decisions required before implementing authentication. Do not write code.
```

Teaching point:

> Sometimes the best AI-assisted move is to ask for questions, not code.
