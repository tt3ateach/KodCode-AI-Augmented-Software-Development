# Work Items 0.4.0 · due dates (the correct feature)

The result of the guided build, prepared in advance. Run from this folder with your environment active:

```bash
python -m pytest -q                  # 34 passed
python scripts/verify_release.py     # tests, a temporary server, health and the business probe
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Tasks have an optional calendar due date. In a PATCH, leaving `due_date` out keeps the saved date and `"due_date": null` clears it. The API adds `overdue` to every task it returns, computed on each read against the UTC calendar day; completed tasks are never overdue. The frontend keeps Module 3's modules (`state.js`, `render.js`, `service.js`, `apiClient.js`, `app.js`); `cd app/static` and `node --test tests/*.test.mjs` runs its tests.
