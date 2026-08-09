# Retail Demo Repo — Module 1

This small repository supports **Module 1: The AI-Augmented Developer — Mindset and Ecosystem**.

It is intentionally tiny and imperfect so instructors can demonstrate:

- explaining unfamiliar code;
- using the same task across assistant/chat/pair-programming/agent modes;
- planning before editing;
- adding validation and tests;
- identifying unsafe AI suggestions;
- deciding when not to delegate a task.

## Suggested demo targets

| File | Demo use |
|---|---|
| `src/retail_demo/profile_parser.py` | Main demo: add validation to a small parser. |
| `src/retail_demo/pricing.py` | Alternative demo: validation and generated tests. |
| `src/retail_demo/legacy_parser.py` | Read-only legacy-code explanation demo. |
| `exercises/confident_intern_problem.md` | Governance mini-case. |
| `.github/copilot-instructions.md` | Example of repository instructions as context engineering. |

## Intentionally incomplete

- Validation is weak.
- Tests cover mostly happy paths.
- Some names and edge cases are awkward on purpose.
- The repo is small enough that students can inspect the whole diff.

## Basic setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e . pytest
pytest
```

Expected starting result:

```text
All tests pass.
```

Passing tests do **not** mean the code is production-ready. That is part of the lesson.

## Recommended first AI prompt

```text
Explain src/retail_demo/profile_parser.py in one paragraph. Then list the top five validation risks. Do not suggest code changes yet.
```

## Recommended bounded implementation prompt

```text
Implement the smallest safe validation change for parse_user_profile. Constraints:
- Do not add third-party dependencies.
- Preserve the UserProfile dataclass and return type.
- Raise ValueError with clear messages for invalid input.
- Add focused tests for missing email, invalid email, blank name, negative age, and unsupported marketing_opt_in values.
- Keep the diff limited to profile_parser.py and test_profile_parser.py.
After editing, summarize the diff and tell me exactly what checks to run.
```
