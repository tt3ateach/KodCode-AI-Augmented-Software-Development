# Work Items 0.4.0 · starting point for Tasks C and D

This is the feature built in the demo, with one defect left in it: a PATCH that sends `"due_date": null`
does not clear the saved date. The original 16 tests still pass, because they were written before due dates
existed. The new due-date tests are not included: writing one is your job. The agreed contract is in
`docs/feature_contract.md`.

## Before you start
Open this folder as your VS Code workspace, select the class interpreter as in your Student Guide, and
commit the starting point, so you can review the assistant's changes later:
```bash
git init
git add -A
git commit -m start
```

## Task C · 15 minutes · Copilot Agent mode
**Minimum:** your own failing REQ-03 test, the smallest fix, and the full-suite result.

1. Write one test for REQ-03 (clearing a date) yourselves, in `tests/test_student_feature.py`, from your
   Task A example or the contract's clearing example. Use the existing `client` fixture; the test
   `test_patch_work_item_preserves_unspecified_fields` in `tests/test_work_items_api.py` shows the pattern.
2. Run only your file: `python -m pytest -q tests/test_student_feature.py`. Expect `1 failed`, and check
   that it fails because the date is still there.
3. Only now ask the assistant for the fix:
   ```text
   My test in tests/test_student_feature.py checks REQ-03 in docs/feature_contract.md and currently fails.
   Explain why it fails, then propose the smallest fix in app/repository.py. Do not change the test.
   Afterwards, explain why a title-only PATCH must still keep the date.
   ```
   Review the change with `git diff` before you keep it.
4. Run the full suite with `python -m pytest -q` and record the result.

Edit only `app/repository.py` and `tests/test_student_feature.py`. The assistant's working rules are in
`AGENTS.md`.

## Task D · 5 minutes · Copilot Ask mode
Use the prompt in your Student Guide. It reads `scripts/verify_release.py`; edit nothing.

To run the app: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`, then open
http://127.0.0.1:8000/. If port 8000 is busy, use `--port 8001`.
