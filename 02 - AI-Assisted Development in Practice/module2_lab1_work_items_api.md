# Module 2 — Lab 1: Build and Test the Work Items API

## 

## Goal

Use AI assistance to implement a small FastAPI CRUD API while preserving normal engineering discipline.

## Functional requirements

The API must support:

* `GET /health`
* `POST /work-items`
* `GET /work-items`
* `GET /work-items/{item\_id}`
* `PATCH /work-items/{item\_id}`
* `DELETE /work-items/{item\_id}`
* filtering by `status` and `priority`

Each work item includes:

* `id`
* `title`
* `description`
* `status`: `todo`, `in\_progress`, `done`
* `priority`: `low`, `medium`, `high`
* `assignee`
* `created\_at`
* `updated\_at`

## Repo

Use:

```text
work\_items\_api\_starter/
```

The starter includes failing acceptance tests. Do not delete tests to make the suite green.

## Rules

1. Ask for a plan before writing code.
2. Keep implementation steps small.
3. Do not accept a generated diff without reading it.
4. Generate or improve tests, but review assertions manually.
5. Run verification commands yourself.
6. Record at least one AI suggestion you rejected or revised.

## Suggested sequence

### Step 1 — Run the failing tests

```bash
pytest -q
```

Read the failures before asking AI to fix anything.

### Step 2 — Ask for a plan

Use the planning prompt from `module2\_prompt\_cookbook.md`.

A good plan should identify:

* `app/repository.py` as the main implementation file;
* endpoint paths and response shapes as stable;
* SQLite parameterized queries;
* tests as the contract;
* `pytest -q` and `python -m compileall app` as verification.

### Step 3 — Implement in slices

Recommended slices:

1. `create\_item` and `list\_items`;
2. `get\_item`;
3. `update\_item`;
4. `delete\_item`;
5. filtering by `status` and `priority`;
6. optional API client review.

### Step 4 — Test the tests

Open:

```text
review\_exercises/weak\_generated\_tests.py
```

Ask AI to critique the tests. Compare with:

```text
review\_exercises/corrected\_generated\_tests.py
```

### Step 5 — Verification

Minimum:

```bash
pytest -q
python -m compileall app
```

Optional manual check:

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Deliverables

* working code;
* passing test output;
* prompt log;
* one rejected/revised AI suggestion;
* short diff review summary.

## Suggested solution

A full solution is included in:

```text
work\_items\_api\_solution/
```

Expected implementation highlights:

* `create\_item()` creates and persists a `WorkItem`.
* `list\_items()` supports optional `status` and `priority` filters and returns deterministic ordering.
* `get\_item()` returns `None` for missing IDs.
* `update\_item()` preserves fields not included in the patch.
* `delete\_item()` returns `True` only when a row was deleted.
* `app/client.py` shows a compact `httpx` API client with explicit timeout and testable error handling.

Expected verification:

```bash
cd work\_items\_api\_solution
pip install -r requirements.txt
pytest -q
python -m compileall app
```

## Optional challenge cards

**Optional / skim if needed.** Choose one only if the core lab is complete:

* Add `limit` and `offset` pagination.
* Add `due\_date`.
* Add sorting.
* Add tag support.
* Add GitHub Actions status badge to README.

