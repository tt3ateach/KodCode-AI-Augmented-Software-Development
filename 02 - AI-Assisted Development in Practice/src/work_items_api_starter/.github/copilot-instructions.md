# Copilot Instructions — Work Items API

- Use Python 3.11+ and FastAPI idioms.
- Keep endpoint paths and response shapes stable unless explicitly requested.
- Prefer the smallest safe change.
- Run `pytest -q` before considering work complete.
- Do not introduce external services or network dependencies.
- Use parameterized SQL for user-controlled values.
- For nontrivial changes, produce a plan before editing.
- When generating tests, make assertions explicit and include negative cases.
- Mention assumptions, risks, and verification steps in summaries.
- Do not paste or invent secrets, tokens, credentials, or customer data.
