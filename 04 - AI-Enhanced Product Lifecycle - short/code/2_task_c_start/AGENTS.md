# Instructions for AI assistants in this folder

This is a classroom copy of the Work Items API (FastAPI and SQLite) with the Module 3 Task Tracker frontend.

## Source of truth
- The agreed behavior is in `docs/feature_contract.md` (REQ-01 to REQ-08), handed out after Task A. If the
  code and the contract disagree, the contract wins. Point out the disagreement instead of changing the contract.

## Rules
- Plan before editing: list the files you intend to change and why. Wait for approval.
- Keep changes small and edit only the files the task names.
- Never delete, skip or weaken an existing test to make the suite pass.
- When fixing a defect, start from a failing test and show that it fails for the expected reason.
- Tests use a fixed reference day, 2026-10-04 (see `tests/conftest.py`). Never use `date.today()` or
  `datetime.now()` in tests.
- Run `python -m pytest -q` before reporting, and quote the actual result.
- Do not add dependencies.

## Layout
- `app/models.py` validation · `app/repository.py` SQLite storage · `app/overdue.py` the overdue rule
- `app/main.py` endpoints and the clock (`server_now`, `get_reference_date`)
- `app/static/src/` frontend seams: `state.js`, `render.js`, `service.js`, `apiClient.js`, `app.js`
