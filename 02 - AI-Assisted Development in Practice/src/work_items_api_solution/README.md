# Work Items API — Module 2 Lab Repo

This repository supports Module 2 of the AI-Augmented Software Development course.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## AI-assisted workflow

1. Ask for a plan before code.
2. Use tests as executable requirements.
3. Keep changes small and reviewable.
4. Review generated tests manually.
5. Run verification commands yourself.
6. Record one AI suggestion you rejected or revised.

## Useful files

- `app/main.py` — FastAPI endpoints.
- `app/models.py` — Pydantic models and enums.
- `app/repository.py` — persistence behavior; main Lab 1 implementation target.
- `app/client.py` — API-client example in the solution repo.
- `tests/` — acceptance tests.
- `lab2_assets/legacy_work_item_logic.py` — legacy-code explanation and test-generation lab.
- `.github/copilot-instructions.md` — repository-level AI context.
- `.github/prompts/` — reusable planning and review prompts.
- `review_exercises/` — generated-test critique assets.


## Solution note

All tests should pass.
